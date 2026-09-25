# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 一键批量校验

用法：
    python run_all_checks.py            # 生成 audit_report.md（汇总）
    python run_all_checks.py --stdout   # 只打印，不落盘

行为：
    1. 顺序执行 spiral_geometry_audit.py（数值/量纲独立复算）
    2. 顺序执行 csv_validate.py（CSV 元数据卫生）
    3. 聚合计数，输出 audit_report.md

红线：只聚合，不修改任何 verdict；不改写源 CSV 与源 md。
"""

import importlib
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def load(name):
    if name in sys.modules:
        return importlib.reload(sys.modules[name])
    return importlib.import_module(name)


def block(title, mod, results):
    lines = []
    c = mod.counts()
    lines.append("## " + title)
    lines.append("")
    lines.append("| 判定 | 计数 |")
    lines.append("|------|------|")
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        lines.append("| " + k + " | " + str(c.get(k, 0)) + " |")
    lines.append("")
    lines.append("| 条目 | 判定 | 结论 |")
    lines.append("|------|------|------|")
    for r in results:
        lines.append("| " + r["id"] + " | " + r["verdict"] + " | " +
                     r["title"].replace("|", "/") + " |")
    lines.append("")
    lines.append("### 明细")
    lines.append("")
    cur = None
    for r in results:
        sec = r.get("sec")
        if sec and sec != cur:
            cur = sec
            lines.append("#### " + sec)
            lines.append("")
        lines.append("**" + r["id"] + " · [" + r["verdict"] + "] " + r["title"] + "**")
        lines.append("")
        lines.append(r["detail"])
        lines.append("")
    return lines, c


def main():
    m1 = load("spiral_geometry_audit")
    r1 = m1.run()
    m2 = load("csv_validate")
    r2 = m2.run()

    b1, c1 = block("一 · 数值与量纲独立复算（spiral_geometry_audit.py）", m1, r1)
    b2, c2 = block("二 · CSV 元数据卫生校验（csv_validate.py）", m2, r2)

    total = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for c in (c1, c2):
        for k in total:
            total[k] += c.get(k, 0)

    head = []
    head.append("# 空间螺旋几何化统一场论 · 一键校验审计报告")
    head.append("")
    head.append("> 生成：`run_all_checks.py`（= spiral_geometry_audit.py + csv_validate.py）")
    head.append("> 依赖：仅 Python 标准库。**本报告保留全部原始矛盾输出，不做任何美化修正。**")
    head.append("")
    head.append("## 总汇总")
    head.append("")
    head.append("| 判定 | 计数 | 含义 |")
    head.append("|------|------|------|")
    head.append("| PASS | " + str(total["PASS"]) + " | 数值/量纲自洽（**不含**物理真伪判定） |")
    head.append("| FAIL | " + str(total["FAIL"]) + " | 数值矛盾或量纲不自洽 |")
    head.append("| BOUNDARY | " + str(total["BOUNDARY"]) + " | 条件成立 / 口径漂移 / 待定 |")
    head.append("| INFO | " + str(total["INFO"]) + " | 恒等式、统计信息（无物理信息量） |")
    head.append("")
    head.append("> **红线提醒**：PASS 只代表「未被本次复算推翻」。本体系 L3（第一性推导/可检验预言）计数为 0，")
    head.append("> 多数 PASS 落在 L0/L1（恒等式与参数化重述）。数学自洽 ≠ 实验证实。")
    head.append("")

    text = "\n".join(head + b1 + b2)

    if "--stdout" in sys.argv:
        print(text)
        return 0

    out = os.path.join(HERE, "audit_report.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print("")
    print("[written] " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
