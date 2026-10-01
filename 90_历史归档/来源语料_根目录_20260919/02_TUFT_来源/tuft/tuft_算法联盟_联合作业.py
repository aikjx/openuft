# -*- coding: utf-8 -*-
"""
tuft_算法联盟_联合作业.py
=========================

把卷系全部 CURATED 引擎「联盟」起来，做**一次性联合作业与工程体检**。

为什么要它：
  - 卷系已有 22 个 CURATED 条目、20+ 个独立引擎；此前**没有任何工具**验证它们
    「今天是否仍能跑通」「声明哈希是否仍一致」；
  - 单卷自检 ≠ 联盟自检：一个引擎单独跑通，不代表与其余引擎在同一目录/同一解释器下
    仍能共存（编码、依赖、路径、输出）。
  - 本工具即「算法联盟」的**联合作业入口**。

功能：
  1. 扫描全部 `*_CURATED.json`，收集 (entry_id, 卷, engine, 声明 sha256)；
  2. 对每个引擎以**独立子进程**复跑（隔离 + 超时保护），记录退出码、耗时、输出摘要；
  3. 校验 SHA256（声明 vs 实际）——检测**代码漂移**；
  4. 顺带调用归约审计 `tuft_卷系_归一化总览.py`；
  5. 产出 `tuft_算法联盟_联合作业报告.md` 与 `.json`。

红线：本工具只做「**能否复跑 + 哈希是否一致**」的工程体检，**不评价物理正确性**，
      也不改动任何真源。数学自洽 != 实验证实。
"""

import hashlib
import json
import os
import subprocess
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "tuft_算法联盟_联合作业报告.md")
OUT_JSON = os.path.join(HERE, "tuft_算法联盟_联合作业报告.json")
TIMEOUT_S = 180
AUDIT_ENGINE = "tuft_卷系_归一化总览.py"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_engines():
    """扫描 CURATED，返回按 entry_id 排序的引擎清单（同一引擎去重）。"""
    rows, seen = [], {}
    for fname in sorted(os.listdir(HERE)):
        if not fname.endswith("_CURATED.json"):
            continue
        try:
            with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception as exc:
            rows.append({"entry_id": "?", "volume": fname, "engine": None,
                         "declared": None, "error": "CURATED 不可读: %s" % exc})
            continue
        vol = doc.get("volume", "?")
        for ent in doc.get("entries", []):
            eid = ent.get("entry_id", "?")
            eng = (ent.get("script_ref", "") or "").split("（")[0].strip().strip("`")
            if not eng:
                continue
            if eng in seen:
                seen[eng]["entries"].append(eid)
                continue
            rec = {"entry_id": eid, "volume": vol, "engine": eng,
                   "declared": ent.get("script_sha256"), "entries": [eid]}
            rows.append(rec)
            seen[eng] = rec
    return rows


def run_engine(engine):
    """独立子进程复跑一个引擎。返回 dict。"""
    path = os.path.join(HERE, engine)
    if not os.path.isfile(path):
        return {"landed": False, "rc": None, "secs": 0.0, "head": "",
                "actual": None, "tampered": None}
    actual = sha256_file(path)
    t0 = time.time()
    try:
        proc = subprocess.run([sys.executable, path], cwd=HERE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=TIMEOUT_S)
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return {"landed": True, "rc": "TIMEOUT", "secs": time.time() - t0,
                "head": "", "actual": actual, "tampered": None}
    secs = time.time() - t0
    txt = (out or b"").decode("utf-8", "replace")
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    head = lines[0] if lines else ((err or b"").decode("utf-8", "replace").strip().splitlines()
                                   or [""])[0]
    # 找引擎自报的 SHA 行（若有）
    self_sha = ""
    for ln in lines:
        if "SHA256" in ln and "=" in ln:
            self_sha = ln.split("=")[-1].strip()
    return {"landed": True, "rc": rc, "secs": secs, "head": head,
            "actual": actual, "self_sha": self_sha, "tampered": None}


def run_audit():
    path = os.path.join(HERE, AUDIT_ENGINE)
    if not os.path.isfile(path):
        return {"ran": False, "summary": "(审计引擎缺失)"}
    try:
        proc = subprocess.run([sys.executable, path], cwd=HERE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=TIMEOUT_S)
        txt = (proc.stdout or b"").decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return {"ran": False, "summary": "(审计引擎超时)"}
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    return {"ran": True, "summary": " | ".join(lines[-2:])}


def main():
    rows = collect_engines()
    print("算法联盟：联合作业启动（引擎 %d 个）" % len(rows))
    results = []
    for r in rows:
        eng = r.get("engine")
        if not eng:
            r["run"] = {"landed": False, "rc": None, "secs": 0.0, "head": "",
                        "actual": None}
        else:
            r["run"] = run_engine(eng)
        run = r["run"]
        r["hash_ok"] = (run.get("actual") is not None
                        and run.get("actual") == r.get("declared"))
        r["run_ok"] = (run.get("rc") == 0)
        results.append(r)
        flag = "OK " if (r["run_ok"] and r["hash_ok"]) else "!! "
        print("  %s%-9s %-46s rc=%-6s %.1fs" % (
            flag, r["entry_id"], (r.get("engine") or "-")[:46],
            str(run.get("rc")), run.get("secs", 0.0)))

    audit = run_audit()

    n = len(results)
    n_run = sum(1 for r in results if r["run_ok"])
    n_hash = sum(1 for r in results if r["hash_ok"])
    n_fail = n - n_run
    n_drift = n - n_hash

    md = []
    md.append("# TUFT / H-TUFT「算法联盟」联合作业报告（自动生成）\n")
    md.append("> 由 `tuft_算法联盟_联合作业.py` 生成（可复跑）。对全部 CURATED 引擎做")
    md.append("> **独立子进程复跑 + 哈希一致性**的工程体检。")
    md.append("> 红线：本表只报「能否复跑 / 哈希是否一致」，**不评价物理正确性**。")
    md.append("> 数学自洽 != 实验证实。\n")
    md.append("## 一、联盟体检汇总\n")
    md.append("- 参检引擎：**%d**" % n)
    md.append("- 复跑通过：**%d**（失败 %d）" % (n_run, n_fail))
    md.append("- 哈希一致：**%d**（漂移 %d）" % (n_hash, n_drift))
    md.append("- 归约审计：%s" % (audit["summary"] if audit["ran"] else audit["summary"]))
    md.append("- 判定：**%s**\n" % (
        "全联盟通过 ✅" if (n_fail == 0 and n_drift == 0) else "存在失败/漂移 ⚠️"))
    md.append("## 二、逐引擎作业明细\n")
    md.append("| entry | 卷 | 引擎 | 哈希 | 复跑 | 耗时(s) | 输出首行 |")
    md.append("|---|---|---|---|---|---|---|")
    for r in results:
        run = r["run"]
        md.append("| %s | %s | `%s` | %s | %s | %.2f | %s |" % (
            r["entry_id"], r["volume"], r.get("engine") or "—",
            "一致" if r["hash_ok"] else "**漂移**",
            ("rc=%s" % run.get("rc")) if r["run_ok"] else "**失败/超时**",
            run.get("secs", 0.0),
            (run.get("head") or "")[:60].replace("|", "/")))
    md.append("")

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({
        "engines": n, "run_ok": n_run, "run_fail": n_fail,
        "hash_ok": n_hash, "hash_drift": n_drift,
        "audit": audit,
        "detail": [dict([(k, v) for k, v in r.items() if k != "run"],
                        run_rc=r["run"].get("rc")) for r in results],
    }, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n已生成: %s" % OUT_MD)
    print("  联盟：引擎 %d；复跑通过 %d；哈希一致 %d；失败 %d；漂移 %d" % (
        n, n_run, n_hash, n_fail, n_drift))
    print("  归约审计：%s" % audit["summary"])
    return 0 if (n_fail == 0 and n_drift == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
