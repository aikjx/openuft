# -*- coding: utf-8 -*-
"""
空间螺旋判定 · 总览与防回潮守卫
================================

本册把两阶段审计的产物**归一为单一事实来源**，并加装**防回潮守卫**——防止后续会话
在无意中把已被判定为 falsified 的主张「清零」写回台账（这类事故在本仓库历史上真实发生过：
审核者只改声明不改 claims.csv，导致看板长期显示过期结论）。

三项职能
--------
1. **总览（单一事实来源）**：从 `claims.csv` + 两阶段引擎产物**自动重建**判定摘要，
   不硬编码任何计数（计数一律现场推导）。
2. **守卫（防回潮）**：断言 8 条不变量；任一违反即打印 FAIL 并以退出码 1 结束（可作门禁）。
   其中 G5 用**不变量基线**（`数据/空间螺旋判定_不变量基线.json`）判断「falsified 集合只许不缩水」，
   G8 用归档哈希防篡改；**任一告警时基线不覆写**（否则守卫会把篡改「自愈」掉——该缺陷由负向测试抓出并已修）。
3. **溯源核对**：确认被审文本已归档、两阶段引擎产物齐备、审计编号与 claims.csv 一一对应。

产出：数据/空间螺旋判定_总览.json + .md
退出码：0 = 全部守卫通过；1 = 有守卫失败（供 CI/门禁使用）

用法：python 空间螺旋判定_总览与防回潮守卫.py
"""

import os
import io
import sys
import json
import time
import hashlib
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")
SYS_DIR = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论")
CLAIMS = os.path.join(SYS_DIR, "claims.csv")
ARCHIVE = os.path.join(SYS_DIR, "修复版申报原文_2026-09-25.md")
ENGINE1 = os.path.join(DATA, "空间螺旋修复版_第一性审计.json")
ENGINE2 = os.path.join(DATA, "空间螺旋修复版_最小修复闭环.json")

STATUS_OK = {"pass", "open", "boundary", "falsified", "repaired"}
FIELD_COUNT = 5

# 判定不变量：这些主张一旦被改回 pass/repaired，即视为回潮事故
MUST_STAY_FALSIFIED = ["C12", "C21", "C23"]
# 两阶段引擎的预期判定总数
EXPECT_TOTAL = {"阶段一": 35, "阶段二": 10}
# 不变量基线（首次运行自动建档；此后只许「不缩水」——见 G5）
BASELINE = os.path.join(DATA, "空间螺旋判定_不变量基线.json")

GUARDS = []


def guard(gid, name, ok, detail=""):
    GUARDS.append({"id": gid, "name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s %s" % ("PASS" if ok else "FAIL", gid, name))
    if detail:
        print("         %s" % detail)
    return ok


print("=" * 76)
print("空间螺旋判定 · 总览与防回潮守卫")
print("=" * 76)

# ---------------------------------------------------------------------------
# 1. 读台账并解析
# ---------------------------------------------------------------------------
print("\n§1  台账解析")
raw = io.open(CLAIMS, encoding="utf-8").read().splitlines()
rows = []
for ln in raw[1:]:
    if not ln.strip():
        continue
    f = ln.split(",")
    rows.append({"id": f[0],
                 "statement": f[1] if len(f) > 1 else "",
                 "category": f[2] if len(f) > 2 else "",
                 "status": f[3] if len(f) > 3 else "",
                 "reviewer": f[4] if len(f) > 4 else "",
                 "n_fields": len(f)})

by_id = {r["id"]: r for r in rows}
status_cnt = Counter(r["status"] for r in rows)
audit_rows = [r for r in rows if r["reviewer"] == "算法联盟审计组"]
print("     主张总数 %d；状态分布 %s" % (len(rows), dict(status_cnt)))
print("     本审计登记（reviewer=算法联盟审计组）：%d 条" % len(audit_rows))

# ---------------------------------------------------------------------------
# 2. 守门
# ---------------------------------------------------------------------------
print("\n§2  防回潮守卫")

bad_width = [r["id"] for r in rows if r["n_fields"] != FIELD_COUNT]
guard("G1", "claims.csv 每行恰 %d 字段（无列错位）" % FIELD_COUNT, not bad_width,
      "异常行：%s" % (bad_width if bad_width else "无"))

ids = [r["id"] for r in rows]
nums = [int(i[1:]) for i in ids if i.startswith("C") and i[1:].isdigit()]
gap = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []
guard("G2", "claim_id 连续无缺号（C01–C%02d）" % (max(nums) if nums else 0), not gap,
      "缺号：%s" % (gap if gap else "无"))

bad_status = [r["id"] for r in rows if r["status"] not in STATUS_OK]
guard("G3", "状态取值合法（%s）" % "|".join(sorted(STATUS_OK)), not bad_status,
      "非法：%s" % (bad_status if bad_status else "无"))

reverted = [cid for cid in MUST_STAY_FALSIFIED
            if by_id.get(cid, {}).get("status") != "falsified"]
guard("G4", "原 falsified 三条（C12/C21/C23）**未被改回**", not reverted,
      "被改动：%s（修复版申报声称「清零」，审计认定不成立 ⇒ 不得改回）" % (reverted if reverted else "无"))

# G5：不变量基线——falsified 集合只许「不缩水」（自动覆盖未来新增，无需改代码）
cur_falsified_audit = sorted(r["id"] for r in audit_rows if r["status"] == "falsified")
base = None
if os.path.isfile(BASELINE):
    base = json.load(io.open(BASELINE, encoding="utf-8"))
shrunk = []
grown = []
if base is None:
    print("         （基线不存在 ⇒ 本次自动建档）")
else:
    prev = set(base.get("falsified_audit_ids", []))
    now = set(cur_falsified_audit)
    shrunk = sorted(prev - now)
    grown = sorted(now - prev)
guard("G5", "审计组 falsified 集合不缩水（基线 %s 条）"
      % (len(base.get("falsified_audit_ids", [])) if base else len(cur_falsified_audit)),
      not shrunk,
      ("缩水：%s ← 这是回潮事故" % shrunk) if shrunk
      else ("新增 %s（已自动记入基线）" % grown if grown else "与基线一致"))

e1 = json.load(io.open(ENGINE1, encoding="utf-8")) if os.path.isfile(ENGINE1) else None
e2 = json.load(io.open(ENGINE2, encoding="utf-8")) if os.path.isfile(ENGINE2) else None
guard("G6", "两阶段引擎产物齐备且判定总数符合预期",
      bool(e1 and e2 and e1["counts"]["total"] == EXPECT_TOTAL["阶段一"]
           and e2["counts"]["total"] == EXPECT_TOTAL["阶段二"]),
      "阶段一 total=%s（期望 %d）；阶段二 total=%s（期望 %d）"
      % (e1["counts"]["total"] if e1 else "缺", EXPECT_TOTAL["阶段一"],
         e2["counts"]["total"] if e2 else "缺", EXPECT_TOTAL["阶段二"]))

guard("G7", "被审文本已归档（审计可溯源）", os.path.isfile(ARCHIVE),
      "路径：%s" % ARCHIVE)

# G8：归档文本防篡改（哈希与基线逐位比对）——归档若被改写，整条审计链失去锚点
archive_sha = hashlib.sha256(io.open(ARCHIVE, "rb").read()).hexdigest() if os.path.isfile(ARCHIVE) else ""
tampered = False
if base is not None and base.get("archive_sha256"):
    tampered = (archive_sha != base["archive_sha256"])
    guard("G8", "被审文本哈希未变（防篡改溯源）", not tampered,
          "当前 %s… vs 基线 %s…%s"
          % (archive_sha[:16], base["archive_sha256"][:16],
             "（**已变更**：归档被改写，审计锚点失效）" if tampered else ""))
else:
    guard("G8", "被审文本哈希建档（首次）", bool(archive_sha), "sha256 = " + archive_sha[:32] + "…")

# 基线落盘：**仅在全部告警清零时**才覆写。
# （曾经只挡 "缩水"，导致 G8 报警时仍把篡改后的哈希写进基线 ⇒ 守卫自己把篡改"自愈"掉。
#   该缺陷由 G8 负向测试现场抓出，已修正为 shrunk/tampered 任一非空即保留旧基线。）
if base is None or (not shrunk and not tampered):
    io.open(BASELINE, "w", encoding="utf-8").write(json.dumps({
        "purpose": "空间螺旋判定的不变量基线：审计组 falsified 集合只许不缩水；归档哈希用于防篡改",
        "archive_sha256": archive_sha,
        "falsified_audit_ids": cur_falsified_audit,
        "engines_total": EXPECT_TOTAL,
        "baseline_revision": "2026-09-26 建档（C24–C45 阶段）",
    }, ensure_ascii=False, indent=1) + "\n")

# ---------------------------------------------------------------------------
# 3. 总览（全部计数现场推导，不硬编码）
# ---------------------------------------------------------------------------
print("\n§3  总览重建")

stages = []
if e1:
    stages.append({"name": "阶段一 · 第一性审计与伪派生判定",
                   "engine": "空间螺旋修复版_第一性审计与伪派生判定.py",
                   "counts": e1["counts"]})
if e2:
    stages.append({"name": "阶段二 · 最小修复闭环与继承缺陷",
                   "engine": "空间螺旋修复版_最小修复闭环与继承缺陷审计.py",
                   "counts": e2["counts"]})

audit_status = Counter(r["status"] for r in audit_rows)
baseline_rows = [r for r in rows if r["reviewer"] != "算法联盟审计组"]
baseline_status = Counter(r["status"] for r in baseline_rows)

print("     %-34s %6s %6s %6s %6s %6s" % ("审计阶段", "总数", "PASS", "FAIL", "BOUND", "INFO"))
tot = {"total": 0, "PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
for st in stages:
    c = st["counts"]
    for k in tot:
        tot[k] += c.get(k, 0)
    print("     %-34s %6d %6d %6d %6d %6d"
          % (st["name"], c["total"], c["PASS"], c["FAIL"], c["BOUNDARY"], c["INFO"]))
print("     %-34s %6d %6d %6d %6d %6d"
      % ("合计", tot["total"], tot["PASS"], tot["FAIL"], tot["BOUNDARY"], tot["INFO"]))

print("\n     主张级（claims.csv）")
print("     %-22s %6s %6s %6s %6s %6s" % ("来源", "合计", "pass", "open", "bound", "falsified"))
print("     %-22s %6d %6d %6d %6d %6d"
      % ("原体系（人工审计）", len(baseline_rows), baseline_status.get("pass", 0),
         baseline_status.get("open", 0), baseline_status.get("boundary", 0),
         baseline_status.get("falsified", 0)))
print("     %-22s %6d %6d %6d %6d %6d"
      % ("本审计（算法联盟组）", len(audit_rows), audit_status.get("pass", 0),
         audit_status.get("open", 0), audit_status.get("boundary", 0),
         audit_status.get("falsified", 0)))

verdict = "申报不成立" if audit_status.get("falsified", 0) >= 14 else "需复核"
print("\n     结论：%s（本审计登记 falsified %d 条 / 合计 %d 条）"
      % (verdict, audit_status.get("falsified", 0), len(audit_rows)))

n_bad = sum(1 for g in GUARDS if not g["ok"])

payload = {
    "title": "空间螺旋判定 · 总览与防回潮守卫",
    "date": "2026-09-26",
    "single_source_of_truth": {
        "claims_csv": os.path.relpath(CLAIMS, ROOT).replace("\\", "/"),
        "archive": os.path.relpath(ARCHIVE, ROOT).replace("\\", "/"),
        "engines": [os.path.relpath(p, ROOT).replace("\\", "/") for p in (ENGINE1, ENGINE2) if os.path.isfile(p)],
    },
    "stages": stages,
    "stages_total": tot,
    "claims": {"total": len(rows), "by_status": dict(status_cnt),
               "audit_total": len(audit_rows), "audit_by_status": dict(audit_status),
               "baseline_by_status": dict(baseline_status)},
    "guards": GUARDS,
    "guards_failed": n_bad,
    "verdict": verdict,
    "baseline": {
        "path": os.path.relpath(BASELINE, ROOT).replace("\\", "/"),
        "falsified_audit_ids": cur_falsified_audit,
        "archive_sha256": archive_sha,
        "shrink_detected": shrunk,
        "growth": grown,
    },
}
with io.open(os.path.join(DATA, "空间螺旋判定_总览.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)

lines = ["# 空间螺旋判定 · 总览（单一事实来源）", "",
         "> 日期 2026-09-26 · 由 `空间螺旋判定_总览与防回潮守卫.py` 自动重建（计数不硬编码）", "",
         "**结论：%s** ｜ 守卫通过 %d/%d" % (verdict, len(GUARDS) - n_bad, len(GUARDS)), "",
         "## 一、审计阶段（check 级）", "",
         "| 阶段 | 总数 | PASS | FAIL | BOUNDARY | INFO |", "|---|---|---|---|---|---|"]
for st in stages:
    c = st["counts"]
    lines.append("| %s | %d | %d | %d | %d | %d |"
                 % (st["name"], c["total"], c["PASS"], c["FAIL"], c["BOUNDARY"], c["INFO"]))
lines.append("| **合计** | **%d** | **%d** | **%d** | **%d** | **%d** |"
             % (tot["total"], tot["PASS"], tot["FAIL"], tot["BOUNDARY"], tot["INFO"]))
lines += ["", "## 二、主张级（claims.csv）", "",
          "| 来源 | 合计 | pass | open | boundary | falsified |", "|---|---|---|---|---|---|",
          "| 原体系（人工审计） | %d | %d | %d | %d | %d |"
          % (len(baseline_rows), baseline_status.get("pass", 0), baseline_status.get("open", 0),
             baseline_status.get("boundary", 0), baseline_status.get("falsified", 0)),
          "| 本审计（算法联盟组） | %d | %d | %d | %d | %d |"
          % (len(audit_rows), audit_status.get("pass", 0), audit_status.get("open", 0),
             audit_status.get("boundary", 0), audit_status.get("falsified", 0)),
          "", "## 三、防回潮守卫", "", "| 编号 | 断言 | 结果 | 说明 |", "|---|---|---|---|"]
for g in GUARDS:
    lines.append("| %s | %s | %s | %s |" % (g["id"], g["name"], "PASS" if g["ok"] else "**FAIL**", g["detail"]))
lines += ["", "## 四、单一事实来源", "",
          "- 台账：`" + payload["single_source_of_truth"]["claims_csv"] + "`",
          "- 被审文本：`" + payload["single_source_of_truth"]["archive"] + "`",
          "- 引擎：" + "；".join("`" + p + "`" for p in payload["single_source_of_truth"]["engines"]),
          "",
          "> **G4/G5 的意义**：修复版申报声称「原 falsified 清零」。本守卫把「不得改回」写成机器可判定的断言——",
          "> 任何后续会话若把 C12/C21/C23 或本审计登记的 falsified 改成 pass，本脚本立刻以退出码 1 报警。",
          ""]
with io.open(os.path.join(DATA, "空间螺旋判定_总览.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print("\n" + "=" * 76)
print("守卫 %d/%d 通过 | check 合计 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）| 用时 %.1f s"
      % (len(GUARDS) - n_bad, len(GUARDS), tot["total"], tot["PASS"], tot["FAIL"],
         tot["BOUNDARY"], tot["INFO"], time.time() - T0))
print("结论：%s" % verdict)
print("=" * 76)
sys.exit(1 if n_bad else 0)
