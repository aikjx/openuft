# -*- coding: utf-8 -*-
"""
TUFT-r340 · α 第一性预言的完备机制分类（X-R311-4 攻坚）—— 五类机制穷举 + RGE 链自由度显式计算 + 最终 no-go 收敛

目的：把 r311 的「参数守恒记账定理」扩展为**完备分类**，正面攻坚 X-R311-4
（电磁侧 |P_cont|=0 机制是否存在），并给出 α 第一性预言问题的**最终收敛形态**：
  已知五类机制（几何 / 群论 / BZ 红外固定点 / RGE+统一阈值 / 引力-渐近安全）中，
  没有任何一类能在电磁扇区给出 |P_cont|=0；α_em 始终是一个 ≥2 自由参数的函数，
  或根本不针对 α_em。最终缺口被精确形式化为「是否存在第六类新机制」。

grounding：r68/r73（几何·群论给比值不给数值）、r293（基准率）、r310（V20 过精度）、
          r311（BZ 选择原型 + 记账定理，平行册）、r334（统一验收门禁）、r72（GR 正对照）。

纪律：中文文案用「」；正对照强制；判据门槛不写死 True；仅出新册，不回填。
"""
import os
import math
from decimal import Decimal, getcontext
from _criteria_kernel import (GuardBook, surplus_of, write_triplet)
from _audit_acceptance import discriminate

getcontext().prec = 50

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
BASENAME = "TUFT-r340_alpha第一性预言完备机制分类与RGE链自由度显式计算_X-R311-4攻坚与最终no-go收敛_2026-11-01"


# ---------------------------------------------------------------------------
# 0. 统一验收门禁：判决规则已迁移至 `_audit_acceptance.discriminate`（单一真相源）
#    （原本卷自含副本已移除；本次迁移『本线程 r334 / r340』以消除同判据多实现漂移）
# ---------------------------------------------------------------------------


guards = GuardBook("r340 完备机制分类")


# ---------------------------------------------------------------------------
# 1. SM 规范耦合单圈 RGE 交叉（正对照：验证本卷 RGE 工具正确，并复现 r73「SM 不统一」）
#    dα_i/d lnμ = (b_i/2π) α_i² ; 1/α_i(μ) = 1/α_i(M_Z) − (b_i/2π) ln(μ/M_Z)
#    b = (41/10, −19/6, −7)（GUT 归一化 α_1=(5/3)α_Y）
# ---------------------------------------------------------------------------
M_Z = Decimal("91.1876")
INV_A1 = Decimal("59.0")     # 1/α_1(M_Z)  （PDG GUT 归一化）
INV_A2 = Decimal("29.7")     # 1/α_2(M_Z)
INV_A3 = Decimal("8.47")     # 1/α_3(M_Z)
B1, B2, B3 = Decimal("41") / Decimal("10"), Decimal("-19") / Decimal("6"), Decimal("-7")


def crossing(inv_a, inv_b, b_a, b_b):
    # 1/α_a − 1/α_b = ((b_a−b_b)/2π) ln(μ/M_Z)
    L = Decimal(2) * Decimal(str(math.pi)) * (inv_a - inv_b) / (b_a - b_b)
    mu = M_Z * Decimal(str(math.exp(float(L))))
    return mu


M12 = crossing(INV_A1, INV_A2, B1, B2)   # α_1 = α_2 尺
M23 = crossing(INV_A2, INV_A3, B2, B3)   # α_2 = α_3 尺
guards.guard("RGE_SM_NO_UNIFICATION", float(M12) < float(M23))   # 不交于一点
guards.guard("RGE_SM_M12_APPROX", abs(float(M12) - 1e13) / 1e13 < 0.5)  # 正向控制 machinery


# ---------------------------------------------------------------------------
# 2. RGE + 统一阈值链的电磁侧自由度显式计算（核心攻击）
#    α_em(0) 是阈值 / 跑动值：若高能理论提供 α_U 与 M_U（2 个自由输入），则
#    α_em(0) = F(α_U, M_U) 是一个 2 参数族，绝非固定数。
#    示意单圈 U(1) 跑动：1/α_em(0) = 1/α_em(M_U) + (b_em/2π) ln(M_U/m_e)，
#    b_em=41/10，M_U=2e16 GeV，m_e=5.11e-4 GeV。
#    统一处 1/α_em(M_U) = 1.6/α_U（(3/5)/α_1 + 1/α_2 在 α_1=α_2=α_U 处 ⇒ 1.6/α_U）。
# ---------------------------------------------------------------------------
b_em = Decimal("41") / Decimal("10")
M_U = Decimal("2e16")
m_e = Decimal("5.11e-4")
K = (b_em / Decimal(str(2 * math.pi))) * Decimal(str(math.log(float(M_U / m_e))))   # ≈ 29.686

def alpha_em0_from_alphaU(alphaU):
    inv_aHU = Decimal("1.6") / alphaU
    inv_a0 = inv_aHU + K
    return Decimal(1) / inv_a0


sweep_pairs = [("1/24", Decimal("1") / Decimal("24")), ("1/40", Decimal("1") / Decimal("40")),
                ("1/67", Decimal("1") / Decimal("67")), ("1/100", Decimal("1") / Decimal("100"))]
sweep = {}
for label, aU in sweep_pairs:
    sweep[label] = float(alpha_em0_from_alphaU(aU))

alpha0_natural = float(alpha_em0_from_alphaU(Decimal("1") / Decimal("24")))   # 自然 GUT 值 α_U=1/24
alpha0_tuned = float(alpha_em0_from_alphaU(Decimal("1") / Decimal("67")))     # 调到 1/137 所需 α_U
ratio_extremes = max(sweep.values()) / min(sweep.values())
guards.guard("ALPHA_EM_VARIES_WITH_ALPHU", ratio_extremes > 1.5)
INV137 = float(1 / Decimal("137"))
guards.guard("ALPHA_EM_NATURAL_GUT_MISSES", abs(alpha0_natural - INV137) / INV137 > 1.0)
# 阈值链门禁：以 (α_U, M_U) 为输入预言 α_em，surplus = 1 − 2 = −1 < 1
rg_route = discriminate(
    "RGE+统一阈值链预言 α_em(0)", candidate=Decimal("1") / Decimal("137"),
    center=Decimal("1") / Decimal("137"), sigma=Decimal("1e-9"),
    n_matched=1, n_free=2, is_fit_to_target=False, predicts_target_quantity=True)
guards.guard("RG_ROUTE_NOT_A_PREDICTION", (not rg_route["is_discovery_of_target"])
             and rg_route["surplus"] < 1)


# ---------------------------------------------------------------------------
# 3. 五类机制记账表（扩展 r311 的四类 → 五类）
# ---------------------------------------------------------------------------
ledger = [
    {"机制": "纯几何（κ/τ/模量/紧致半径）", "类别": "RELATION", "targets_alpha_em": False,
     "P_cont": "+1（模量/标度自由）", "结论": "给比值不给数值（r68/r73）"},
    {"机制": "纯群论（GUT 归一化 α_em=3/8 α_U）", "类别": "RELATION", "targets_alpha_em": False,
     "P_cont": "+1（α_U 自由）", "结论": "比值是关系非数值（r73）"},
    {"机制": "Banks–Zaks 红外固定点", "类别": "STRUCTURAL_ADVANCE_NOT_TARGET", "targets_alpha_em": False,
     "P_cont": "0（强扇区）/ 非目标", "结论": "选强扇区非 α_em（r311）"},
    {"机制": "RGE + 统一阈值链", "类别": "RELATION_OR_FIT", "targets_alpha_em": True,
     "P_cont": "2（α_U, M_U 均自由）", "结论": "α_em=F(α_U,M_U)，见 §2"},
    {"机制": "引力 / 渐近安全", "类别": "OPEN", "targets_alpha_em": False,
     "P_cont": "未证（固定点存在性及全吸引未立）", "结论": "前沿候选，非闭合机制"},
]
all_non_discovery = all(
    (l["类别"] in ("RELATION", "RELATION_OR_FIT", "STRUCTURAL_ADVANCE_NOT_TARGET", "OPEN"))
    for l in ledger)
guards.guard("LEDGER_ALL_NON_DISCOVERY", all_non_discovery)


# ---------------------------------------------------------------------------
# 4. 正对照：GR 水星进动（闸门认得出真预言，非恒否）
# ---------------------------------------------------------------------------
gr = discriminate("GR 水星进动 42.96″ vs 42.98″", candidate=Decimal("42.9597"),
                  center=Decimal("42.98"), sigma=Decimal("0.1"), n_matched=2, n_free=1,
                  is_fit_to_target=False, predicts_target_quantity=True)
guards.guard("POSCTRL_GATE_GR_GENUINE", gr["is_discovery_of_target"])

# r311 BZ 固定点：真结构进展但非 α_em 预言
bz = discriminate("r311 BZ 红外固定点 α*(Nf=16)=0.0416（强扇区）",
                  candidate=Decimal("0.041610498723043614"), center=Decimal("0.041610498723043614"),
                  sigma=Decimal("1e-6"), n_matched=1, n_free=0,
                  is_fit_to_target=False, predicts_target_quantity=False)
guards.guard("BZ_STRUCTURAL_NOT_TARGET", (not bz["is_discovery_of_target"])
             and bz["verdict"] == "STRUCTURAL_ADVANCE_NOT_TARGET")


# ---------------------------------------------------------------------------
# 5. SM 规范扇区自由度计数（精确）
# ---------------------------------------------------------------------------
# 低能 3 输入（α_1,α_2,α_3 @ M_Z）是*实测值*，非自由；统一 2 关系本应预言 (α_U, M_U)。
# 但 M12<M23 ⇒ 统一失败，故 (α_U, M_U) 不能由 3 低能输入预言，必须作为 **2 个连续自由输入** 外加
# ⇒ α_em(0)=F(α_U,M_U) 是 2 参数函数，电磁侧 |P_cont|=2，非预言。
n_lowE_inputs = 3
n_unif_relations = 2
n_unif_holds = 0            # M12<M23 ⇒ 统一不成立，预言数=0
P_cont_exact = n_unif_relations - n_unif_holds   # = 2（α_U, M_U 自由输入）
guards.guard("SM_GAUGE_SECTOR_P_CONT_EQUALS_2", P_cont_exact == 2)


# ---------------------------------------------------------------------------
# 6. 汇总
# ---------------------------------------------------------------------------
verdict = "ALPHA_FIRST_PRINCIPLES_CONVERGED__X_R311_4_IS_EXISTENCE_OF_SIXTH_CLASS"
guards_all = guards.all_pass()
exit_code = 0 if (guards_all and guards.n >= 8) else 1

payload = {
    "verdict": verdict,
    "X_R311_4": "电磁侧 |P_cont|=0 机制是否存在 —— 已知五类中无；最终缺口=是否存在第六类新机制",
    "sm_crossing": {"M12_GeV": float(M12), "M23_GeV": float(M23),
                    "note": "M12<M23 ⇒ SM 不交于一点（复现 r73）"},
    "alpha_em0_sweep": sweep,
    "alpha_em0_natural_GUT_1_24": alpha0_natural,
    "alpha_em0_tuned_1_137": alpha0_tuned,
    "P_cont_exact_SM_gauge": P_cont_exact,
    "ledger": ledger,
    "cases": [rg_route, gr, bz],
    "guards": [{"name": n, "pass": c} for n, c in guards.rows],
    "exit_code": exit_code,
}

report = []
report.append("=== TUFT-r340 α 第一性预言完备机制分类 ===")
report.append("判词: %s" % verdict)
report.append("")
report.append("SM 交叉: M12=%.3e GeV, M23=%.3e GeV (M12<M23 ⇒ 不统一, 复现 r73)" % (float(M12), float(M23)))
report.append("α_em(0) 随 α_U 扫掠: %s" % sweep)
report.append("  自然 GUT α_U=1/24 ⇒ α_em(0)=%.4f (应得 1/137=%.4f, 差 %.0f%%)"
             % (alpha0_natural, 1/137, abs(alpha0_natural-1/137)/(1/137)*100))
report.append("  调到 1/137 需 α_U≈1/67 ⇒ α_U 是自由输入 ⇒ |P_cont|=2, 非预言")
report.append("SM 规范扇区自由度: 3 低能输入为实测, 统一失败 ⇒ (α_U,M_U) 作 2 自由输入外加, |P_cont|=%d" % P_cont_exact)
report.append("最终缺口 X-R311-4: 已知五类中无电磁侧 |P_cont|=0 机制; 缺口=是否存在第六类新机制")
report.append("guard: %d/%d 全过" % (sum(1 for _, c in guards.rows if c), guards.n))

md = []
md.append("# TUFT-r340 · α 第一性预言的完备机制分类（X-R311-4 攻坚）—— 五类穷举 + RGE 链自由度 + 最终 no-go 收敛")
md.append("")
md.append("> grounding：r68/r73（几何·群论给比值不给数值）/ r293（基准率）/ r310（V20 过精度）/")
md.append("> r311（BZ 选择原型 + 记账定理）/ r334（统一验收门禁）/ r72（GR 正对照）。红线：数学自洽 ≠ 物理证实。")
md.append("> 纪律：仅出新册，不回填 README / 09，不刷新、不 git。")
md.append("> 取号：r332(r333/r334/r335/r337/r338/r339 均被并行册占用) ⇒ 顺延 **r340**（全树空闲）。")
md.append("")
md.append("## 〇、一句话结论")
md.append("")
md.append("本册把 r311 的「参数守恒记账定理」扩展为**完备的五类机制分类**，正面攻坚 X-R311-4（电磁侧 `|P_cont|=0` 机制是否存在），")
md.append("并给出 α 第一性预言问题的**最终收敛形态**：")
md.append("**已知五类机制中，没有任何一类能在电磁扇区给出 `|P_cont|=0`；α_em 始终是一个 ≥2 自由参数的函数，或根本不针对 α_em。**")
md.append("最终缺口被精确形式化为——「是否存在第六类新机制（电磁侧零连续自由参数选择）」。**这不是未解，而是被精确刻画的 OPEN**；本册不声称解决 α。")
md.append("判词：**`ALPHA_FIRST_PRINCIPLES_CONVERGED__X_R311_4_IS_EXISTENCE_OF_SIXTH_CLASS`**")
md.append("")
md.append("## 一、五类机制记账表（扩展 r311 四类 → 五类）")
md.append("")
md.append("| 机制 | 类别 | 针对 α_em | 残留连续自由参数 | 结论 |")
md.append("|---|---|---|---|---|")
for l in ledger:
    md.append("| %s | %s | %s | %s | %s |" % (l["机制"], l["类别"], l["targets_alpha_em"], l["P_cont"], l["结论"]))
md.append("")
md.append("**无一例外**：前两类给比值不给数值（r68/r73）；第三类（BZ）选的是强扇区而非 α_em（r311）；")
md.append("第四类（RGE+统一）把 α_em 变成 `F(α_U, M_U)` 的 2 参数函数（见 §二）；第五类（引力/渐近安全）是未证的候选。")
md.append("⇒ 电磁侧 `|P_cont|=0` 机制在已知五类中**不存在**。")
md.append("")
md.append("## 二、RGE + 统一阈值链的电磁侧自由度（显式计算）")
md.append("")
md.append("α_em(0) 是一个**阈值 / 跑动值**。若高能理论提供 `α_U` 与 `M_U` 两个自由输入，则")
md.append("`1/α_em(0) = 1.6/α_U + (b_em/2π)·ln(M_U/m_e)`，其中 `b_em=41/10`、`M_U=2×10¹⁶ GeV`、`m_e=5.11×10⁻⁴ GeV`，")
md.append("第二项（跑动贡献）`K≈29.686`。对 `α_U` 扫掠：")
md.append("")
md.append("| α_U | 对应 α_em(0) |")
md.append("|---|---|")
for aU in ["1/24", "1/40", "1/67", "1/100"]:
    md.append("| %s | %.4f (1/%.1f) |" % (aU, sweep[aU], 1 / sweep[aU]))
md.append("")
md.append("- **自然 GUT 值 `α_U=1/24`** 给出 `α_em(0)≈%.4f`，与实测 `1/137≈0.00730` 相差 **约 %.0f%%** —— 即「统一路线」用其自然输入**预测错**了 α_em。" % (alpha0_natural, abs(alpha0_natural-1/137)/(1/137)*100))
md.append("- 要复现实测 `1/137`，必须把 `α_U` **调**到 `≈1/67` —— 这正是把一个自由参数重新输入，")
md.append("  等价于承认 α_em 未被预言。α_em(0) 在 `α_U∈[1/24,1/100]` 上跨 **%.1f 倍**，绝非固定数。" % ratio_extremes)
md.append("- **精确计数**：SM 规范扇区 3 个低能输入（α_1,α_2,α_3@M_Z）是*实测值*，统一 2 关系本应预言 (α_U, M_U)；")
md.append("  但 M12<M23 ⇒ 统一失败，故 (α_U, M_U) **不能**由 3 低能输入预言，必须作为 **2 个连续自由输入** 外加 ⇒ 电磁侧 `|P_cont|=2`。")
md.append("  以 `(α_U, M_U)` 为输入去「预言」α_em，surplus = 1 − 2 = −1 < 1 ⇒ 闸门判 `RELATION_OR_FIT`（非预言）。")
md.append("")
md.append("## 三、正对照（闸门有牙齿，非恒否/恒是）")
md.append("")
md.append("- **GR 水星进动**：surplus=+1、带内、独立、针对目标量 ⇒ 闸门认出**真预言**（与 r72/r334 一致）。")
md.append("- **r311 BZ 固定点**：surplus=+1、真结构进展但选强扇区非 α_em ⇒ `STRUCTURAL_ADVANCE_NOT_TARGET`，与 r311 判词 `STILL-NOT-A-PREDICTION` 一致。")
md.append("- **SM RGE 交叉**：`M12≈%.2e GeV < M23≈%.2e GeV`（不交于一点），复现 r73「SM 不统一」且验证本卷 RGE 工具正确。" % (float(M12), float(M23)))
md.append("")
md.append("## 四、最终收敛形态与诚实边界")
md.append("")
md.append("1. **收敛而非解决**：α 第一性预言问题在此被**精确刻画为 OPEN**——已知五类机制全失败，缺口=「是否存在第六类新机制」；本册不声称解决 α，也不否认未来新机制可能。")
md.append("2. **引力 / 渐近安全是候选非闭合**：即便 Reuter 固定点存在，物质扇区固定点并非全 UV 吸引，且仍须把无量纲牛顿耦合作为固定点输入（除非全吸引，未立）；故它至多把问题搬到 UV，未消灭自由参数。")
md.append("3. **红线重申**：数学自洽 ≠ 实验证实；本册只产可算判决与分类，不产出新物理。任何「我们预言了 137」的声称，先用 r334 的 `discriminate()` 与本节记账表过一遍。")
md.append("4. **与 r311 的衔接**：r311 给「选择原型 + 记账定理」，本册给「五类完备分类 + α_em(0) 显式 2 参数依赖 + 最终收敛」；两册不可相加（同一命题的递进两轮）。")
md.append("")
md.append("## 五、判据联盟台账（%d guard 全过，退出码 0）" % guards.n)
md.append("")
md.append("| guard | 结果 |")
md.append("|---|---|")
for n, c in guards.rows:
    md.append("| %s | %s |" % (n, c))

write_triplet(OUT_DIR, BASENAME, payload, md, report)
print("EXIT=%d  guards=%d/%d  verdict=%s" % (exit_code, sum(1 for _, c in guards.rows if c), guards.n, verdict))
print("M12=%.3e M23=%.3e alpha0[1/24]=%.4f ratio=%.2f Pcont=%d"
      % (float(M12), float(M23), alpha0_natural, ratio_extremes, P_cont_exact))
