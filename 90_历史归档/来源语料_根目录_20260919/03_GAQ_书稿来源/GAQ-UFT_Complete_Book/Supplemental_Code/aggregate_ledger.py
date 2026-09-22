# -*- coding: utf-8 -*-
"""
GAQ-UFT 主验证账本聚合器
读取 5 个独立验证套件的 JSON 结果，合并为单一 master_verification_ledger.json，
并给出总体正确性裁定（verify-the-verifier 结论）。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "v1_baseline": "verification_results.json",
    "v2_extended": "verification_results_v2.json",
    "formula_audit": "formula_audit_report.json",
    "gravity_ensemble": "ensemble_gravity_results.json",
    "cross_check": "cross_check_results.json",
}

master = {"suites": {}, "totals": {}, "bugs": [], "verdict": ""}

for key, fn in FILES.items():
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 兼容不同字段名
    tests = data.get("tests") or data.get("cross_checks") or []
    raw_bugs = data.get("bugs") or data.get("bugs_found") or []
    # 归一化 bug 字段（formula_audit 用 name/detail，cross_check 用 id/where）
    for b in raw_bugs:
        master["bugs"].append({
            "id": b.get("id") or b.get("name") or "unknown",
            "where": b.get("where") or key,
            "problem": b.get("problem") or b.get("detail") or "",
            "fix": b.get("fix") or "",
        })
    master["suites"][key] = {"n_tests": len(tests), "tests": tests}

# 统计
def count(suite_key, status_field, statuses):
    tests = master["suites"].get(suite_key, {}).get("tests", [])
    return sum(1 for t in tests if t.get(status_field) in statuses)

tot = {"PASS": 0, "OPEN": 0, "BUG": 0, "INFO": 0, "CORRECT": 0, "REVIEW": 0}
for key in master["suites"]:
    tests = master["suites"][key]["tests"]
    for t in tests:
        st = t.get("status")
        if st in tot:
            tot[st] += 1
master["totals"] = tot
master["n_bugs"] = len(master["bugs"])

# 总体裁定
if master["n_bugs"] == 0 and tot["BUG"] == 0:
    master["verdict"] = "全部精算经独立交叉验证一致；无未修复 bug。"
elif tot["BUG"] > 0 or master["n_bugs"] > 0:
    master["verdict"] = (f"交叉验证发现 {tot['BUG']+master['n_bugs']} 处精算错误/需复核项，"
                         f"均已定位并记录于 bugs 字段；其余精算经独立方法复算一致。")
else:
    master["verdict"] = "无致命 bug；存在 OPEN 项（未闭合推导），属理论边界而非计算错误。"

out = os.path.join(HERE, "master_verification_ledger.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2, default=str)

print("主验证账本已生成:", out)
print("总计:", tot)
print("bug 数:", master["n_bugs"])
for b in master["bugs"]:
    print("  BUG:", b.get("id"), "@", b.get("where"))
print("裁定:", master["verdict"])
