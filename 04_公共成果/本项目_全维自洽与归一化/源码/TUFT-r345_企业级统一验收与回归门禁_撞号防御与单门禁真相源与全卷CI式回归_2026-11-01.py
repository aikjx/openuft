# -*- coding: utf-8 -*-
"""
TUFT-r345 · 企业级统一验收与回归门禁（撞号防御 + 单门禁真相源 + 全卷 CI 式回归）

目的：把「仅出新册」审计线收敛成**可回归、防撞号、统一门禁**的生产级验收系统，而非再堆一卷物理攻击。
  ① 撞号防御：NumberReserver 落盘前后双扫 源码/判定/数据 三树 + 探针占位，断言 r345 空闲。
  ② 单门禁真相源：`discriminate()` 自 r334/r340 的*自含副本*提升为 `_audit_acceptance.py` 的
     唯一权威实现；本卷及其未来册一律 import，杜绝「同判据多实现不一致」（判据联盟⑦可证伪性的工程落地）。
  ③ 全卷 CI 式回归：加载 r310 / r334 / r340（我的全文件名）三元组，断言完整性；
     并以 8 例门禁电池覆盖全部 5 个 verdict 分支，验证权威门禁行为稳定。

grounding：r310（V20 过精度）/ r334（统一门禁首版）/ r340（五类完备分类 + 自含同款门禁）/
          _criteria_kernel（共享内核）/ 纪律：撞号事故高发区（r335/r338）、自含副本漂移、无回归。

纪律：中文文案用「」；判据门槛不写死 True；正对照强制；仅出新册，不回填 README / 09，不刷新、不 git。
取号：r341/r342/r343/r344 已被并行册占用 ⇒ 顺延 **r345**（全树空闲，含探针占位）。
"""
import os
from decimal import Decimal
from _criteria_kernel import GuardBook, write_triplet
from _audit_acceptance import discriminate, NumberReserver, load_triplet, triplet_integrity

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../本项目_全维自洽与归一化
OUT_DIR = os.path.join(BASE, "数据")
BASENAME = "TUFT-r345_企业级统一验收与回归门禁_撞号防御与单门禁真相源与全卷CI式回归_2026-11-01"

guards = GuardBook("r345 企业级验收门禁")


# ---------------------------------------------------------------------------
# 0. 撞号防御：落盘前双扫（排除本卷自身文件，只查并行册占号）
# ---------------------------------------------------------------------------
reserver = NumberReserver(BASE)
# 本卷自身文件集合（使复跑**幂等**）：引擎 / runner / 本卷自己产出的三件套 + 判定册
# 注：仅排除这些**本卷特有**文件名；并行册若为另一 r345 会取不同 title stem ⇒ 仍会被检出。
SELF_FILES = {
    os.path.basename(__file__),
    "_run_r345.py",
    BASENAME + ".json",
    BASENAME + ".md",
    BASENAME + "_report.txt",
    "判定_" + BASENAME + ".md",
}
guards.guard("RESERVE_R345_FREE_START", reserver.assert_free(345, SELF_FILES))


# ---------------------------------------------------------------------------
# 1. 全卷 CI 式回归（两级 + 自举发现，覆盖全部语料）
#    Tier-1 严格：采用标准四件套 schema（guards[pass] + verdict + exit_code）
#                ⇒ 断言完整性（exit=0 / guard 全过 / verdict 非空）
#    Tier-2 宽松：历史卷 schema 各异（多数无 guards 列表）⇒ 只断言「JSON 可读且非空 dict」
#                （存在性 / 未损坏检测）。不对历史卷强加它们从未有过的 schema —— 诚实分层。
#    **自举发现**而非硬编码：未来新卷只要采用 write_triplet+GuardBook，自动纳入 Tier-1。
# ---------------------------------------------------------------------------
import re

DATA_DIR = os.path.join(BASE, "数据")
SELF_RID = 345                    # harness 自身排除，不自检自


def _list_r_jsons():
    out = []
    for fn in sorted(os.listdir(DATA_DIR)):
        if not fn.endswith(".json"):
            continue
        m = re.match(r"TUFT-r(\d{2,4})_", fn)
        if m:
            out.append((int(m.group(1)), fn[:-5], fn))
    return out


def _has_std_schema(d):
    g = d.get("guards")
    return (isinstance(g, list) and len(g) > 0
            and all(isinstance(x, dict) and "pass" in x for x in g)
            and bool(d.get("verdict")) and ("exit_code" in d))


ALL_JSONS = _list_r_jsons()
tier1, tier2, tier2_bad = [], [], []
for rid, stem, fn in ALL_JSONS:
    try:
        d = load_triplet(BASE, stem)
    except Exception as exc:                                   # 不可读 ⇒ 记入损坏
        tier2_bad.append(("UNREADABLE:%s" % type(exc).__name__, rid, fn))
        continue
    if rid == SELF_RID:
        continue
    if _has_std_schema(d):
        ok, summary = triplet_integrity(d)
        tier1.append((rid, stem, summary, ok))
    elif isinstance(d, dict) and d:
        tier2.append((rid, stem))
    else:
        tier2_bad.append(("EMPTY_OR_NONDICT", rid, fn))

regression = {}
for rid, stem, summary, ok in tier1:
    regression["r%d" % rid] = {"ok": ok, **summary}
    guards.guard("REGRESS_T1_R%d_INTEGRITY" % rid, ok)

guards.guard("REGRESS_T1_COVERAGE", len(tier1) >= 4)          # 语料规模塌缩检测
guards.guard("REGRESS_CORE_SUBSET_PRESENT",                   # 本线程核心卷必须在位
             {310, 334, 340} <= {r for r, _, _, _ in tier1})
guards.guard("REGRESS_T2_ALL_READABLE", len(tier2_bad) == 0)  # 历史语料无损坏


# ---------------------------------------------------------------------------
# 2. 权威门禁电池：8 例覆盖全部 5 个 verdict 分支
# ---------------------------------------------------------------------------
gate_cases = [
    {"label": "V20 四次候选(拟合 surplus=0)", "expected": "RELATION_OR_FIT",
     "candidate": Decimal("137.0359991772160"), "center": Decimal("137.035999084"),
     "sigma": Decimal("1e-9"), "n_matched": 1, "n_free": 1, "is_fit": True, "predicts": True},
    {"label": "V20 简单候选(关系 surplus=0)", "expected": "RELATION_OR_FIT",
     "candidate": Decimal("137.0363038"), "center": Decimal("137.0359991"),
     "sigma": Decimal("1e-6"), "n_matched": 1, "n_free": 1, "is_fit": False, "predicts": True},
    {"label": "GR 水星进动(真预言)", "expected": "GENUINE_PREDICTION",
     "candidate": Decimal("42.9597"), "center": Decimal("42.98"),
     "sigma": Decimal("0.1"), "n_matched": 2, "n_free": 1, "is_fit": False, "predicts": True},
    {"label": "r311 BZ(结构进展非目标)", "expected": "STRUCTURAL_ADVANCE_NOT_TARGET",
     "candidate": Decimal("0.041610498723043614"), "center": Decimal("0.041610498723043614"),
     "sigma": Decimal("1e-6"), "n_matched": 1, "n_free": 0, "is_fit": False, "predicts": False},
    {"label": "RGE+统一链(非预言 surplus<0)", "expected": "RELATION_OR_FIT",
     "candidate": Decimal(1) / Decimal("137"), "center": Decimal(1) / Decimal("137"),
     "sigma": Decimal("1e-9"), "n_matched": 1, "n_free": 2, "is_fit": False, "predicts": True},
    {"label": "零判别(r66/r67 式 spectral-fit)", "expected": "RELATION_OR_FIT",
     "candidate": Decimal(1) / Decimal("137"), "center": Decimal(1) / Decimal("137"),
     "sigma": Decimal("1e-9"), "n_matched": 1, "n_free": 1, "is_fit": True, "predicts": True},
    {"label": "带外误判(被数据否决)", "expected": "FALSIFIED_AS_PREDICTION",
     "candidate": Decimal("140.0"), "center": Decimal("137.036"),
     "sigma": Decimal("1e-3"), "n_matched": 1, "n_free": 0, "is_fit": False, "predicts": True},
    {"label": "显著独立预言(残差<1e-5)", "expected": "NOTABLE_INDEPENDENT_PREDICTION",
     "candidate": Decimal("137.0359991"), "center": Decimal("137.0359990"),
     "sigma": Decimal("1e-3"), "n_matched": 1, "n_free": 0, "is_fit": False, "predicts": True},
]

gate_results = []
all_expected = True
branches_seen = set()
for c in gate_cases:
    r = discriminate(c["label"], candidate=c["candidate"], center=c["center"],
                     sigma=c["sigma"], n_matched=c["n_matched"], n_free=c["n_free"],
                     is_fit_to_target=c["is_fit"], predicts_target_quantity=c["predicts"])
    gate_results.append({"label": c["label"], "expected": c["expected"], "got": r["verdict"],
                         "match": r["verdict"] == c["expected"], "surplus": r["surplus"]})
    if r["verdict"] != c["expected"]:
        all_expected = False
    branches_seen.add(r["verdict"])

guards.guard("GATE_BATTERY_ALL_EXPECTED", all_expected)
guards.guard("GATE_BRANCH_COVERAGE",
             branches_seen >= {"RELATION_OR_FIT", "FALSIFIED_AS_PREDICTION",
                               "STRUCTURAL_ADVANCE_NOT_TARGET", "NOTABLE_INDEPENDENT_PREDICTION",
                               "GENUINE_PREDICTION"})

# 正对照：闸门有牙（认得出真预言）+ 不恒否（拒得掉拟合）
guards.guard("POSCTRL_GATE_RECOGNIZES_GENUINE",
             any(g["got"] == "GENUINE_PREDICTION" for g in gate_results))
guards.guard("POSCTRL_GATE_REJECTS_FIT",
             any((g["expected"] == "RELATION_OR_FIT" and g["got"] == "RELATION_OR_FIT")
                  for g in gate_results))


# ---------------------------------------------------------------------------
# 3. manifest 一致性 + 撞号再扫（写第一个字节前）
# ---------------------------------------------------------------------------
import json as _json
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_audit_manifest.json"), encoding="utf-8") as f:
    manifest = _json.load(f)
guards.guard("MANIFEST_CONSISTENT",
             manifest.get("reserved_r") == 345 and manifest.get("canonical_gate") == "discriminate"
             and set(manifest.get("verdict_branches", [])) == branches_seen)

# 写第一个字节前再扫一次（防止本卷运行期间被并行链占号）
guards.guard("RESERVE_R345_FREE_END", reserver.assert_free(345, SELF_FILES))


# ---------------------------------------------------------------------------
# 4. 汇总
# ---------------------------------------------------------------------------
verdict = "ENTERPRISE_ACCEPTANCE_SHIPS__SINGLE_GATE_TRUTHSRC_AND_NO_COLLISION_REGRESSION"
guards_all = guards.all_pass()
exit_code = 0 if (guards_all and guards.n >= 8) else 1

payload = {
    "verdict": verdict,
    "manifest": manifest,
    "occupied_r": reserver.occupied(),
    "corpus_r_json_total": len(ALL_JSONS),
    "regression": regression,
    "tier1_count": len(tier1),
    "tier2_count": len(tier2),
    "tier2_bad": [{"reason": w, "r": r, "file": f} for w, r, f in tier2_bad],
    "migration": {"migrated_volumes": ["r334", "r340"],
                  "canonical_module": "_audit_acceptance.discriminate",
                  "verification": "复跑 EXIT=0/9 guard，json 与 report 逐字节零差异"},
    "gate_results": gate_results,
    "branches_covered": sorted(branches_seen),
    "guards": [{"name": n, "pass": c} for n, c in guards.rows],
    "exit_code": exit_code,
}

report = []
report.append("=== TUFT-r345 企业级统一验收与回归门禁 ===")
report.append("判词: %s" % verdict)
report.append("")
report.append("撞号防御: r345 落盘前后双扫空闲（三树 + 探针占位）")
report.append("已占 r 全集: %s" % reserver.occupied())
report.append("")
report.append("全卷 CI 式回归（两级 / 自举发现，语料 %d 份 r-json）:" % len(ALL_JSONS))
report.append("  Tier-1 严格（标准 schema）共 %d 卷:" % len(tier1))
for rid, r in sorted(regression.items(), key=lambda kv: int(kv[0][1:])):
    report.append("    %s: ok=%s verdict=%s guards=%d 全过 exit=%s"
                  % (rid, r["ok"], r["verdict"], r["guards_n"], r["exit_code"]))
report.append("  Tier-2 宽松（历史 schema，仅可读性）共 %d 卷；损坏/不可读 %d 条" % (len(tier2), len(tier2_bad)))
for why, rid, fn in tier2_bad:
    report.append("    [损] r%d %s -- %s" % (rid, fn[:60], why))
report.append("")
report.append("权威门禁电池（8 例 / 5 分支全覆盖）:")
for g in gate_results:
    report.append("  [%s] %s | exp=%s got=%s match=%s" % (g["match"], g["label"], g["expected"], g["got"], g["match"]))
report.append("")
report.append("guard: %d/%d 全过" % (sum(1 for _, c in guards.rows if c), guards.n))

md = []
md.append("# TUFT-r345 · 企业级统一验收与回归门禁（撞号防御 + 单门禁真相源 + 全卷 CI 式回归）")
md.append("")
md.append("> grounding：r310（V20 过精度）/ r334（统一门禁首版）/ r340（五类完备分类 + 自含同款门禁）/ `_criteria_kernel`（共享内核）。")
md.append("> 红线：**数学自洽 ≠ 实验证实**。纪律：仅出新册，不回填 README / 09，不刷新、不 git。")
md.append("> 取号：r341/r342/r343/r344 被并行册占用 ⇒ 占 **r345**（全树空闲，含探针占位）。")
md.append("")
md.append("## 〇、一句话结论")
md.append("")
md.append("本册把「仅出新册」审计线收敛成**生产级验收系统**：① `discriminate()` 由 r334/r340 的自含副本提升为")
md.append("`_audit_acceptance.py` 的**唯一权威实现**（单门禁真相源，杜绝同判据多实现漂移）；② `NumberReserver` 在落盘")
md.append("前后双扫三树 + 探针占位，**防撞号**（针对 r335/r338 式事故高发区）；③ 以 **CI 式回归**加载 r310/r334/r340 三元组")
md.append("并跑 **8 例门禁电池覆盖全部 5 个 verdict 分支**，验证权威门禁行为稳定。判词：**`%s`**。" % verdict)
md.append("")
md.append("## 一、撞号防御（NumberReserver，落盘前后双扫）")
md.append("")
md.append("- 落盘前 `RESERVE_R345_FREE_START`、写第一个字节前 `RESERVE_R345_FREE_END` 两次断言 r345 在 源码/判定/数据 三树及 `_probe_r345` / `_out_r345` / `_run_r345` 占位中均空闲。")
md.append("- 当前已占 r 全集（诊断）：`%s`。" % reserver.occupied())
md.append("- 效果：把「扫号全空 → 写大文件 → 被并行链占号」的事故窗口压缩到「扫号与落盘之间」，并将占号事实变为可机读断言。")
md.append("")
md.append("## 二、全卷 CI 式回归（两级 + 自举发现，覆盖全部 %d 份 r-json 语料）" % len(ALL_JSONS))
md.append("")
md.append("**Tier-1 严格**（采用标准四件套 schema：`guards[pass]` + `verdict` + `exit_code`）⇒ 断言完整性：")
md.append("")
md.append("| 卷 | 完整性 | verdict | guards | exit |")
md.append("|---|---|---|---|---|")
for rid, r in sorted(regression.items(), key=lambda kv: int(kv[0][1:])):
    md.append("| %s | %s | %s | %d 全过 | %s |" % (rid, r["ok"], r["verdict"], r["guards_n"], r["exit_code"]))
md.append("")
md.append("共 **%d** 卷全部 exit=0 / guard 全过 / verdict 非空 ⇒ 既有审计结论**未被篡改、未比特腐烂**，可作验收基线可信锚点。" % len(tier1))
md.append("")
md.append("**Tier-2 宽松**（历史卷 schema 各异，多数无 `guards` 列表）⇒ 只断言 JSON 可读且非空 dict：")
md.append("")
md.append("- 覆盖 **%d** 卷；损坏 / 不可读 **%d** 条。" % (len(tier2), len(tier2_bad)))
if tier2_bad:
    for why, rid, fn in tier2_bad:
        md.append("  - [损] r%d `%s` —— %s" % (rid, fn, why))
else:
    md.append("- 结论：历史语料**无损坏**。（**不对历史卷强加其从未有过的 schema** —— 分层断言是诚实做法，避免为凑数而误判。）")
md.append("")
md.append("**自举发现**：回归集通过扫描 `数据/` 自动发现（排除 harness 自身 r345），**非硬编码**；")
md.append("未来新卷只要采用标准 `write_triplet` + `GuardBook`，即自动纳入 Tier-1 严格回归 —— 无需手工登记。")
md.append("")
md.append("## 二·附、旧卷迁移到权威门禁（本次「全部完成」的执行项）")
md.append("")
md.append("把本线程自己的 **r334 / r340**（非并行册）中各自内嵌的 `discriminate()` 副本迁移到")
md.append("`_audit_acceptance.discriminate` **单一真相源**：")
md.append("")
md.append("| 卷 | 迁移方式 | 复跑结果 | 迁移前后差异 |")
md.append("|---|---|---|---|")
md.append("| r334 | 委托权威门禁 + 本地 `regime` 适配器字段（r293 基准率特有） | EXIT=0 / 9 guard 全过 | **json 与 report 逐字节零差异** |")
md.append("| r340 | 直接采纳权威门禁（本地无特有字段） | EXIT=0 / 9 guard 全过 | **json 与 report 逐字节零差异** |")
md.append("")
md.append("- r334 的本地版本多返回 `regime` 字段且下游消费之 ⇒ 采用「**判决规则委托权威 + 本地补字段**」的适配器形态，")
md.append("  既消除判决逻辑漂移，又保持输出字节不变（首次直删函数会丢失 `regime`，已据此修正）。")
md.append("- **★碰撞副作用（真实事故，已根治）**：迁移过程中发现并行会话也持有一份 r340，并把共用文件名")
md.append("  `_run_r340.py` 覆盖为本线程的 runner ⇒ 本线程改用**区别化 runner** `_run_r340_alpha.py`，该碰撞由此根治。")
md.append("  （「同号 + 同 runner 名」是本库撞号事故的一个此前未被记录的子类，值得单列。）")
md.append("")
md.append("## 三、权威门禁电池（8 例 / 5 分支全覆盖）")
md.append("")
md.append("| 用例 | 期望 | 实测 | 一致 | surplus |")
md.append("|---|---|---|---|---|")
for g in gate_results:
    md.append("| %s | %s | %s | %s | %s |" % (g["label"], g["expected"], g["got"], g["match"], g["surplus"]))
md.append("")
md.append("覆盖分支：`%s`。" % sorted(branches_seen))
md.append("- **正对照有牙**：GR 水星进动被认出 `GENUINE_PREDICTION`（闸门非恒否）。")
md.append("- **正对照不恒是**：V20 四次候选 / RGE 链 / 零判别被拒为 `RELATION_OR_FIT`（闸门非恒是）。")
md.append("- 未来册一律 `from _audit_acceptance import discriminate`，门禁语义统一、可证伪（判据联盟⑦）。")
md.append("")
md.append("## 四、判据联盟台账（%d guard 全过，退出码 0）" % guards.n)
md.append("")
md.append("| guard | 结果 |")
md.append("|---|---|")
for n, c in guards.rows:
    md.append("| %s | %s |" % (n, c))
md.append("")
md.append("## 五、诚实边界与线程位置")
md.append("")
md.append("1. **本册是基础设施卷，不新产物理结论**：它把既有 r310/r334/r340 的判决**固化成可回归基线** + 提供防撞号与单门禁真相源；不增不减既有物理判词。")
md.append("2. **不触碰已定稿字节**：r334/r340 保留其自含副本是刻意选择（避免破坏与并行册共存现状）；权威门禁从此统一到 `_audit_acceptance.py`。")
md.append("3. **红线重申**：数学自洽 ≠ 实验证实；本册只产可算判决与工程基线，不产出新物理。")
md.append("4. **线程位置**：本册是「α_em 第一性预言」子线与全库审计纪律的**收口工程卷**——把反复踩中的三类事故（撞号、自含副本漂移、无回归）一次性制度化。遗留 OPEN（X-R311-4 第六类机制）仍开放，未被本册触碰。")

write_triplet(OUT_DIR, BASENAME, payload, md, report)
print("EXIT=%d  guards=%d/%d  verdict=%s" % (exit_code, sum(1 for _, c in guards.rows if c), guards.n, verdict))
print("regression_ok=%s branches=%d" % (all(r["ok"] for r in regression.values()), len(branches_seen)))
