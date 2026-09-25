"""
自动化 Worker (RPA / IP 任务)
============================
职责链路:
  Redis 队列取任务 -> CDP 连接常驻 Chromium 打开页面 -> 截图写共享卷
  -> 调 OCR 服务识别(只传共享卷路径, 零图片序列化) -> 结果回写 MySQL + Redis

任务协议 (Redis LPUSH rpa:tasks '<json>'):
{
  "task_no": "T20260910001",        # 必填, 唯一编号
  "url": "https://example.com",    # 必填, 目标页面
  "actions": [                      # 可选, 简单动作序列
     {"type": "click", "selector": "#id"},
     {"type": "fill",  "selector": "input[name=k]", "value": "关键词"},
     {"type": "wait", "ms": 1000}
  ],
  "need_ocr": true,                 # 是否对截图做 OCR
  "full_page": false
}

扩展点: handle_task() 中按 task_type 增加你的业务逻辑即可, 框架代码不用动。
"""
import os
import json
import time
import uuid
import traceback
import asyncio
from datetime import datetime

import redis
import pymysql
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from playwright.async_api import async_playwright

# ---------------------------------------------------------------- 环境配置
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASK_QUEUE = os.getenv("TASK_QUEUE", "rpa:tasks")
RESULT_QUEUE = os.getenv("RESULT_QUEUE", "rpa:results")
BROWSER_CDP = os.getenv("BROWSER_CDP", "http://browser:9222")
OCR_URL = os.getenv("OCR_URL", "http://ocr:8000/ocr")
SHARED_DIR = "/data"
CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", "2"))
PAGE_TIMEOUT = int(os.getenv("PAGE_TIMEOUT", "60000"))

MYSQL_CONF = dict(
    host=os.getenv("MYSQL_HOST", "mysql"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "appuser"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DATABASE", "appdb"),
    charset="utf8mb4", autocommit=True,
)

PROXY = None
if os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY"):
    p = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    PROXY = {"server": p}

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


# ---------------------------------------------------------------- 数据库
def db():
    return pymysql.connect(**MYSQL_CONF)


def save_result(task_no, status, result_text="", snapshot="", err=""):
    sql = """INSERT INTO rpa_task(task_no, task_type, status, result_text,
                                  snapshot_path, err_msg, updated_at)
             VALUES(%s,'web',%s,%s,%s,%s,NOW())
             ON DUPLICATE KEY UPDATE status=VALUES(status),
                  result_text=VALUES(result_text),
                  snapshot_path=VALUES(snapshot_path),
                  err_msg=VALUES(err_msg), updated_at=NOW()"""
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (task_no, status, result_text, snapshot, err[:1000]))


# ---------------------------------------------------------------- OCR 调用
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def call_ocr(path: str):
    resp = requests.post(OCR_URL, json={"path": path}, timeout=120)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------- 单任务
async def handle_task(pw, task: dict):
    task_no = task.get("task_no") or uuid.uuid4().hex
    url = task["url"]
    os.makedirs(SHARED_DIR, exist_ok=True)
    snapshot = f"{SHARED_DIR}/{task_no}.png"
    save_result(task_no, 1, snapshot=snapshot)  # 执行中

    browser = await pw.chromium.connect_over_cdp(BROWSER_CDP)
    try:
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            proxy=PROXY, locale="zh-CN", ignore_https_errors=True,
        )
        page = await ctx.new_page()
        page.set_default_timeout(PAGE_TIMEOUT)
        await page.goto(url, wait_until="domcontentloaded")

        for act in task.get("actions", []):
            t = act.get("type")
            if t == "click":
                await page.click(act["selector"])
            elif t == "fill":
                await page.fill(act["selector"], str(act.get("value", "")))
            elif t == "wait":
                await page.wait_for_timeout(int(act.get("ms", 500)))
            elif t == "scroll":
                await page.mouse.wheel(0, int(act.get("dy", 800)))

        await page.wait_for_timeout(500)
        await page.screenshot(path=snapshot, full_page=bool(task.get("full_page")))

        result_text = ""
        if task.get("need_ocr", False):
            ocr = call_ocr(snapshot)
            result_text = ocr.get("text", "")

        save_result(task_no, 2, result_text, snapshot)
        r.lpush(RESULT_QUEUE, json.dumps(
            {"task_no": task_no, "status": 2, "snapshot": snapshot,
             "text": result_text, "ts": datetime.now().isoformat()},
            ensure_ascii=False))
        print(f"[worker] done {task_no}", flush=True)
        await ctx.close()
    finally:
        await browser.close()


# ---------------------------------------------------------------- 消费循环
async def worker_slot(slot_id, pw):
    """每个并发槽串行处理, 崩溃自动续跑, 不退出进程"""
    while True:
        task = {}
        try:
            # BRPOP 阻塞取任务, 0=永久等待
            item = r.brpop(TASK_QUEUE, timeout=5)
            if not item:
                continue
            _, raw = item
            task = json.loads(raw)
            t0 = time.time()
            await handle_task(pw, task)
            print(f"[worker-{slot_id}] cost {time.time()-t0:.1f}s", flush=True)
        except Exception:  # noqa 单任务失败不拖垮整个 worker
            err = traceback.format_exc()
            print(f"[worker-{slot_id}] error:\n{err}", flush=True)
            try:
                save_result(task.get("task_no", "unknown"), 3, err=err)
            except Exception:
                pass
            await asyncio.sleep(1)


async def main():
    # 等待依赖服务就绪
    for name, url in [("browser", BROWSER_CDP), ("ocr", OCR_URL.replace("/ocr", "/health"))]:
        for i in range(30):
            try:
                requests.get(url, timeout=3)
                break
            except Exception:
                print(f"[worker] waiting {name} ...", flush=True)
                await asyncio.sleep(2)

    async with async_playwright() as pw:
        slots = [worker_slot(i, pw) for i in range(CONCURRENCY)]
        await asyncio.gather(*slots)


if __name__ == "__main__":
    asyncio.run(main())
