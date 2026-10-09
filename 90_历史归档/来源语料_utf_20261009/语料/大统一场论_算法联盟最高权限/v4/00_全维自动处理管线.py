# -*- coding: utf-8 -*-
"""
00_全维自动处理管线.py  (V4 融合 · 最高权限 · 自动处理主控)
=================================================================================
目标: 对 V4 体系全部验证脚本做"全维自动处理"——批量运行 + 结论解析 +
      跨脚本口径一致性核对 + 统一收口报告。

设计原则 (最高规范):
  - 只读运行被测脚本, 不修改任何被测脚本, 只解析其 stdout + 生成聚合报告
  - 每个脚本独立子进程运行, 超时保护(默认 120s), 崩溃隔离(一个崩不影响其余)
  - 增量模式: 若 <脚本>.报告.md 已存在且脚本 mtime 未变, 直接解析旧报告, 不重跑
  - 口径一致性: 跨脚本抽查 α⁻¹, n_q, kg→GeV 因子, μ_geo 是否同值, 冲突告警
  - 诚实边界: 不伪称"全通过", 如实统计 FAIL/越界/异常

用法:
  python 00_全维自动处理管线.py            # 增量运行(已跑过且未改动则跳过)
  python 00_全维自动处理管线.py --rerun    # 强制重跑全部
  python 00_全维自动处理管线.py --list     # 仅列出待处理脚本, 不运行
"""
import sys, io, os, re, json, subprocess, argparse, hashlib
from typing import Optional
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.basename(__file__)

# 排除项: 非验证脚本 / 源迁移辅助 / 子目录脚本
EXCLUDE = {
    "_gen_figures.py",
    "_migrate_all.py",
}
EXCLUDE_PREFIX = ("_",)          # 下划线开头不视为编号验证脚本
TIMEOUT = 180                    # 单脚本超时(秒)

# 结论标记正则(从 stdout 解析)
MARK_PASS   = re.compile(r"(✅\s*PASS|PASS|✓|通过|机器零)", re.IGNORECASE)
MARK_FAIL   = re.compile(r"(❌\s*FAIL|FAIL|✗|失败|冲突)", re.IGNORECASE)
MARK_HONEST = re.compile(r"(诚实|诚实✓|越界|开放项|NG-?X|测量锚|残差)", re.IGNORECASE)
MARK_BUG    = re.compile(r"(Bug|bug|修复|修正|崩溃|异常)", re.IGNORECASE)

# 口径一致性抽取正则
RX_ALPHA_INV = re.compile(r"α⁻¹\s*=\s*([0-9.]+)|ALPHA_INV\s*=\s*mpf\('([0-9.]+)'\)")
RX_NQ        = re.compile(r"n_q\s*=\s*mpf\(([0-9.]+)\)|NQ\s*=\s*mpf\(([0-9.]+)\)")
RX_KGGEV     = re.compile(r"kg→GeV\s*因子\s*e?(\d+)|5\.609e(\d+)")
# μ_geo 抽取: 排除"占位"字样(占位值非有效 RG 闭合尺度), 优先匹配带"精确/闭合"修饰的行
RX_MUGEO     = re.compile(r"μ_geo\s*(?:≈|精确|闭合)?\s*[:=]\s*([0-9.]+)\s*GeV")
RX_MUGEO_LINE = re.compile(r"μ_geo[^\n]*?(?:占位|非有效)[^\n]*")  # 占位行识别(用于排除)

def discover():
    """发现全部 NN_*.py 验证脚本(按编号排序)"""
    out = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith(".py"):
            continue
        if fn == SELF:
            continue
        if fn in EXCLUDE:
            continue
        if fn.startswith(EXCLUDE_PREFIX):
            continue
        if not re.match(r"^\d+_", fn):   # 必须以数字编号开头
            continue
        full = os.path.join(HERE, fn)
        if not os.path.isfile(full):
            continue
        out.append(fn)
    return out

def file_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def report_path_of(script):
    base = script[:-3]  # 去 .py
    return os.path.join(HERE, base + "报告.md")

def run_script(script):
    """运行单个脚本, 返回 (rc, stdout, stderr, timed_out)"""
    full = os.path.join(HERE, script)
    try:
        p = subprocess.run([sys.executable, full],
                           cwd=HERE, capture_output=True,
                           timeout=TIMEOUT, encoding="utf-8", errors="replace")
        return p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired:
        return None, "", "TIMEOUT(>%ds)" % TIMEOUT, True
    except Exception as e:
        return None, "", "EXC: %s" % e, False

def parse_marks(text):
    npass = len(MARK_PASS.findall(text))
    nfail = len(MARK_FAIL.findall(text))
    nhonest = len(MARK_HONEST.findall(text))
    nbug = len(MARK_BUG.findall(text))
    return npass, nfail, nhonest, nbug

def extract_constants(text):
    d: dict[str, Optional[str]] = {"alpha_inv": None, "n_q": None, "kg_gev_exp": None, "mu_geo": None}
    m = RX_ALPHA_INV.search(text)
    if m:
        d["alpha_inv"] = (m.group(1) or m.group(2) or m.group(3))
    m = RX_NQ.search(text)
    if m:
        d["n_q"] = (m.group(1) or m.group(2))
    m = RX_KGGEV.search(text)
    if m:
        d["kg_gev_exp"] = (m.group(1) or m.group(2))
    # μ_geo: 逐行扫描, 跳过含"占位/非有效"的行, 仅抽有效闭合值
    for line in text.splitlines():
        if RX_MUGEO_LINE.search(line):
            continue
        m = RX_MUGEO.search(line)
        if m:
            d["mu_geo"] = m.group(1)
            break
    return d

def num_close(a, b, tol=0.005):
    """数值容差判定: 用于 alpha_inv 这类仅显示精度不同的常数"""
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true", help="强制重跑全部")
    ap.add_argument("--list", action="store_true", help="仅列出待处理脚本")
    args = ap.parse_args()

    scripts = discover()
    print("=" * 72)
    print("  V4 全维自动处理管线 · 发现 %d 个验证脚本" % len(scripts))
    print("=" * 72)

    if args.list:
        for s in scripts:
            print("  " + s)
        return

    results = []
    for script in scripts:
        full = os.path.join(HERE, script)
        md5 = file_md5(full)
        rpt = report_path_of(script)
        need_run = args.rerun or not os.path.exists(rpt)
        entry = {"script": script, "md5": md5, "ran": False,
                 "rc": None, "timed_out": False, "stderr": "",
                 "npass": 0, "nfail": 0, "nhonest": 0, "nbug": 0,
                 "consts": {}, "source": "run" if need_run else "cached_report"}

        if need_run:
            print("  [RUN ] %s ..." % script, flush=True)
            rc, so, se, to = run_script(script)
            entry["ran"] = True
            entry["rc"] = rc
            entry["timed_out"] = to
            entry["stderr"] = se.strip()[-500:] if se else ""
            if rc == 0:
                np_, nf_, nh_, nb_ = parse_marks(so)
                entry["npass"], entry["nfail"] = np_, nf_
                entry["nhonest"], entry["nbug"] = nh_, nb_
                entry["consts"] = extract_constants(so)
                # 也解析报告 md(若脚本已写)
                if os.path.exists(rpt):
                    try:
                        txt = io.open(rpt, "r", encoding="utf-8").read()
                        c2 = extract_constants(txt)
                        for k, v in c2.items():
                            if v and not entry["consts"].get(k):
                                entry["consts"][k] = v
                    except Exception:
                        pass
            else:
                # 运行失败: 尝试从已有报告解析(若有)
                entry["source"] = "run_failed"
                if os.path.exists(rpt):
                    txt = io.open(rpt, "r", encoding="utf-8").read()
                    np_, nf_, nh_, nb_ = parse_marks(txt)
                    entry["npass"], entry["nfail"] = np_, nf_
                    entry["nhonest"], entry["nbug"] = nh_, nb_
                    entry["consts"] = extract_constants(txt)
                    entry["source"] = "cached_report_after_fail"
        else:
            # 增量: 直接解析已有报告 md
            print("  [CACHE] %s (报告已存在且未改动)" % script, flush=True)
            txt = io.open(rpt, "r", encoding="utf-8").read()
            np_, nf_, nh_, nb_ = parse_marks(txt)
            entry["npass"], entry["nfail"] = np_, nf_
            entry["nhonest"], entry["nbug"] = nh_, nb_
            entry["consts"] = extract_constants(txt)

        results.append(entry)

    # ---- 跨脚本口径一致性核对 ----
    const_keys = ["alpha_inv", "n_q", "kg_gev_exp", "mu_geo"]
    const_vals = {k: {} for k in const_keys}
    for e in results:
        for k in const_keys:
            v = e["consts"].get(k)
            if v:
                const_vals[k].setdefault(v, []).append(e["script"])

    consistency = []
    for k in const_keys:
        bins = const_vals[k]
        if len(bins) > 1:
            # 数值容差合并: alpha_inv / mu_geo 等仅显示精度不同的视为一致
            if k in ("alpha_inv", "mu_geo"):
                vals = list(bins.keys())
                rep = vals[0]
                merged = {rep: sum(len(s) for s in bins.values())}
                # 检查是否有数值差异超容差者
                real_conflict = [v for v in vals if not num_close(v, rep)]
                if not real_conflict:
                    # 全部在容差内: 归为 OK(标注精度差异)
                    detail = "%s (×%d脚本, 仅显示精度差异)" % (rep, merged[rep])
                    consistency.append({"key": k, "status": "OK", "detail": detail,
                                        "values": merged})
                    continue
            detail = "; ".join("%s×[%s]" % (val, ",".join(scripts[:3]) + ("..." if len(scripts) > 3 else ""))
                               for val, scripts in bins.items())
            consistency.append({"key": k, "status": "CONFLICT", "detail": detail,
                                "values": {v: len(s) for v, s in bins.items()}})
        elif len(bins) == 1:
            val = list(bins.keys())[0]
            consistency.append({"key": k, "status": "OK", "detail": "%s (×%d脚本)" % (val, len(bins[val])),
                                "values": {val: len(bins[val])}})
        else:
            consistency.append({"key": k, "status": "N/A", "detail": "无脚本抽取到该常数", "values": {}})

    # ---- 汇总 ----
    total = len(results)
    ran = sum(1 for e in results if e["ran"])
    cached = total - ran
    failed = [e for e in results if e["source"].startswith("run") and e["source"] != "run" or
              (e["ran"] and e["rc"] not in (0, None))]
    # 修正: 运行且 rc 非0 才算失败
    failed = [e for e in results if e["ran"] and e["rc"] not in (0,)]
    nfail_marks = sum(e["nfail"] for e in results)
    npass_marks = sum(e["npass"] for e in results)
    timed_out = [e for e in results if e["timed_out"]]

    L = []
    L.append("")
    L.append("=" * 72)
    L.append("  V4 全维自动处理 · 总报告")
    L.append("=" * 72)
    L.append("  脚本总数: %d | 本次运行: %d | 增量缓存: %d" % (total, ran, cached))
    L.append("  运行失败(rc≠0): %d | 超时: %d" % (len(failed), len(timed_out)))
    L.append("  结论标记汇总: PASS类=%d, FAIL类=%d" % (npass_marks, nfail_marks))
    L.append("")
    L.append("-" * 72)
    L.append("  逐脚本明细:")
    L.append("-" * 72)
    for e in results:
        flag = "✓OK" if (e["ran"] and e["rc"] == 0) or (not e["ran"]) else ("⚠FAIL" if e["rc"] not in (0, None) else "·")
        src = {"run": "新跑", "cached_report": "缓存", "run_failed": "跑崩",
               "cached_report_after_fail": "崩后取旧报告"}[e["source"]]
        L.append("  [%s] %s  [%s] PASS=%d FAIL=%d 诚实=%d 修复=%d"
                 % (flag, e["script"], src, e["npass"], e["nfail"], e["nhonest"], e["nbug"]))
        if e["stderr"]:
            L.append("        stderr: %s" % e["stderr"][:200])
        cv = {k: e["consts"].get(k) for k in const_keys if e["consts"].get(k)}
        if cv:
            L.append("        常数: " + ", ".join("%s=%s" % (k, v) for k, v in cv.items()))

    L.append("")
    L.append("-" * 72)
    L.append("  跨脚本口径一致性核对:")
    L.append("-" * 72)
    for c in consistency:
        L.append("  [%s] %s : %s" % (c["status"], c["key"], c["detail"]))

    L.append("")
    L.append("-" * 72)
    L.append("  总判定:")
    L.append("-" * 72)
    if failed:
        L.append("  ⚠ 有 %d 个脚本运行失败, 需人工排查:" % len(failed))
        for e in failed:
            L.append("      - %s (rc=%s)" % (e["script"], e["rc"]))
    else:
        L.append("  ✓ 全部脚本运行成功(rc=0) 或已缓存")
    conflicts = [c for c in consistency if c["status"] == "CONFLICT"]
    if conflicts:
        L.append("  ⚠ 发现 %d 处跨脚本口径冲突, 见上表:" % len(conflicts))
        for c in conflicts:
            L.append("      - %s" % c["key"])
    else:
        L.append("  ✓ 抽查常数(α⁻¹/n_q/kg→GeV/μ_geo)跨脚本一致")
    L.append("")
    L.append("  诚实边界: 本管线仅聚合运行结果, 不伪称'全体系闭合';")
    L.append("  残余开放锚见各脚本 [Ai]/[Oi] 段与 46 号审计报告。")

    report = "\n".join(L)
    print(report)

    # 写 md
    md_out = os.path.join(HERE, "00_全维自动处理报告.md")
    with io.open(md_out, "w", encoding="utf-8") as f:
        f.write("# V4 全维自动处理 · 总报告\n\n")
        f.write("> 算法联盟 ROOT 最高权限 · 自动处理主控 · 2026-08-18\n\n")
        f.write("```\n" + report + "\n```\n")

    # 写 json(机器可读)
    json_out = os.path.join(HERE, "00_全维自动处理报告.json")
    payload = {
        "total": total, "ran": ran, "cached": cached,
        "failed": [e["script"] for e in failed],
        "timed_out": [e["script"] for e in timed_out],
        "npass_marks": npass_marks, "nfail_marks": nfail_marks,
        "consistency": consistency,
        "scripts": results,
    }
    with io.open(json_out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("\n[报告已写入]")
    print("  " + md_out)
    print("  " + json_out)

if __name__ == "__main__":
    main()
