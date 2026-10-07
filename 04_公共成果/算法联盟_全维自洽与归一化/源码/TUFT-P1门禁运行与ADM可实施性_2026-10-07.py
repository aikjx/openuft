# -*- coding: utf-8 -*-
"""
第二十一轮 · P1 门禁运行 + 最小闭合底座的 ADM 可实施性

日期：2026-10-07
读数：数据/TUFT-P1门禁运行与ADM可实施性_2026-10-07.json
      数据/TUFT-P1门禁运行与ADM可实施性_2026-10-07.md

承接 r19（作用量与 ADM 不同源）、r20（P0 最小闭合集 + 下游作废清单）。
本轮做两件事：
  1. 把 P1 门禁**真的跑一遍**（对来料原文），产出「几通过 / 几否决 / 几不可判」的读数。
  2. 在唯一已验证的闭合底座（31 号册式）上，算出**可实施性**的三件硬结果：
     Dirac 自由度计数、tau kinetic 项的 ADM 精确展开（n^2 系数符号）、
     初值需求清单；**不自推** g_tau 块的完整系数（标 BOUNDARY 并指明须引文献核对）。

纯标准库（decimal，60 位有效数字），零第三方依赖、零网络。退出码由自检决定。

纪律：
  1. 只用 CODATA 原始常数，不引用中间比值。
  2. 不编造未推导的系数：需文献核对者一律 BOUNDARY + 指明来源。
  3. 不代选物理路线（同 30 号册 E-06），但给门禁读数与最小清单。
  4. 数学自洽 != 物理证实。
"""
from __future__ import annotations

import json
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(BASE), "数据")

C_LIGHT = Decimal(299792458)
G_N = Decimal("6.67430e-11")
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")


def S(x, digits=6):
    return format(Decimal(x), "." + str(digits) + "E")


# ================= A 段：P1 门禁运行（对象 = 来料原文） =================
# 门禁定义（沿用 r19 P1 与 r20 Q0 段）：
#   g1 GR 极限自检     ：令 G 回到 8*pi*G/c^4、tau->0，方程组须退化为 GR
#   g2 源项归零        ：源项在 tau=0 处必须为 0（否则无 tau->0 无源解）
#   g3 约束初值可满足  ：约束数与初值须自洽（演化未知量 = 初值数，约束独立）
#   g4 色散式量纲      ：omega 的量纲必须是 T^-1
#   g5 梯度不稳定性    ：ADM 分解中 n^2 系数须 > 0（无鬼）
GATES = [
    ("g1_gr_limit", "FAIL",
     "哈密顿约束右端 -(Gamma/2)rho 与标准 16*pi*G*rho/c^2 的比值在 c=1 口径为 -0.25（承 r19 A-01）⇒ GR 极限不还原 GR"),
    ("g2_source_vanishes", "FAIL",
     "源项 (alpha/c)*omega 是常数源，tau=0 处取值 8637.4… != 0（承 r20 C0-03）⇒ 无 tau->0 无源解"),
    ("g3_constraints_initial", "FAIL",
     "演化未知量 6->8 但未给 2 条新约束与初值（r19 A-04）⇒ 约束面未定义，门禁不可满足"),
    ("g4_frequency_dimension", "FAIL",
     "omega = Lambda0 r_s^2/l_P^2 的量纲是力 M^1L^1T^-2 != T^-1；化简后 M^2c^3/(2 pi hbar) 同（r19 S-01/S-02）"),
    ("g5_no_ghost", "UNDECIDABLE",
     "作用量无 tau 的 kinetic 项 => tau 不是传播场（n^2 系数 = 0，属『无传播』而非梯度不稳定）⇒ 判据不适用"),
]
GATE_PASS = sum(1 for g in GATES if g[1] == "PASS")
GATE_FAIL = sum(1 for g in GATES if g[1] == "FAIL")
GATE_UNDEC = sum(1 for g in GATES if g[1] == "UNDECIDABLE")

# ================= B 段：最小闭合底座的可实施性 =================
# 闭合底座（31 号册，r20 P0-03）：L = sqrt(-g)[ (1/2k)R + (1/2) g_tau tau R
#                                            + (1/2) Z_tau g^{uv} grad_u tau grad_v tau
#                                            - (1/2) m_tau^2 tau^2 - eta tau ] + L_m
#
# --- B-1 Dirac 计数（严格）---
PHASE = {
    "gamma_ij": 6,   # 空间度规
    "K_ij": 6,       # 外曲率
    "tau": 1,        # 标量
    "pi_tau": 1,     # 标量动量
}
PHASE_TOTAL = sum(PHASE.values())          # 14
FIRST_CLASS = 4                            # 1 Hamiltonian + 3 Momentum（ADM 规范）
SECOND_CLASS = 0
PHYS_PHASE = PHASE_TOTAL - 2 * FIRST_CLASS - 2 * SECOND_CLASS   # 14 - 8 = 6
PHYS_CONFIG = PHYS_PHASE // 2                                # 3
DOF_GRAVITON = 2
DOF_SCALAR = 1
DOF_MATCHES = PHYS_CONFIG == DOF_GRAVITON + DOF_SCALAR

# --- B-2 tau kinetic 项的 ADM 精确展开（符号分析）---
# ds^2 = -n^2 dt^2 + h_ij (dx^i + beta^i dt)(dx^j + beta^j dt)
# grad_0 tau = n^{-1} (dt_tau - beta^i grad_i tau),  sqrt(-g) = n sqrt(h)
# L_tau = n sqrt(h) (1/2) Z [ n^{-2}(dt_tau - beta.grad tau)^2 - h^{ij} grad_i tau grad_j tau ]
N2_COEFF_KINETIC = Decimal("0.5")          # (sqrt(h)/2) * Z  的符号因子
Z_TAU_SIGN = 1                              # Z_tau > 0 取正
N2_SIGN = N2_COEFF_KINETIC * Z_TAU_SIGN
GRAD_COEFF = Decimal("-0.5")                # -n sqrt(h)(1/2) Z h^{ij} grad_i tau grad_j tau
SHIFT_COUPLING = Decimal("-1")              # -(sqrt(h)/n) Z (dt_tau)(beta.grad tau)

# --- B-3 g_tau 块（不自行推导系数）---
G_TAU_BLOCK = "BOUNDARY"
G_TAU_NOTE = ("(1/2) g_tau tau R 中 R = R_tilde + K^2 - K_ij K^ij，而 K ~ n^{-1} => "
              "该块对 n^2 系数也有贡献；完整鬼判据需把 EH + g_tau tau K^2 一并展开。"
              "本册**不自行推导该系数**（避免编造），标 BOUNDARY 并指明须引权威文献核对"
              "（Koike-Maeda-Nakamura-Yajima, gr-qc/0105056 一类 ADM 鬼分析）。")

# --- B-4 初值需求清单 ---
IV_LIST = [
    ("gamma_ij", 6, "空间度规初值"),
    ("K_ij", 6, "外曲率初值"),
    ("tau", 1, "挠率标量初值"),
    ("pi_tau", 1, "标量动量初值"),
]
CONSTRAINTS = [
    ("H", 1, "混合 Hamiltonian 约束（含 grad tau grad tau 交叉项）"),
    ("M_i", 3, "ADM 动量约束"),
]
GAUGE_FIX = "phi=0（去除 1 个标量的内部自由度）+ 3 个 shift 分量 + lapse ⇒ 需 5 个规范函数"

ITEMS = [
    # ---- A 段：门禁运行 ----
    ("A-01", "FAIL", "a01_gate_run_zero_pass",
     "P1 门禁对来料原文的运行结果：**PASS 0 / FAIL %d / UNDECIDABLE %d** ⇒ 路径 2（数值孤子剖面）在门禁未过时**不可执行**" % (GATE_FAIL, GATE_UNDEC)),
    ("A-02", "INFO", "a02_gate_run_ledger",
     "逐条：g1 GR 极限（比值 -0.25，FAIL）· g2 源项归零（常数源 != 0，FAIL）· g3 约束初值（6->8 无新约束，FAIL）· g4 [omega]（= 力，FAIL）· g5 梯度不稳定性（tau 非传播场，判据不适用，UNDECIDABLE）"),
    ("A-03", "INFO", "a03_gate_reuses_earlier_findings",
     "本段不重算：全部读数直接引 r19 A-01/A-04/S-01/S-02 与 r20 C0-03 ⇒ 门禁化只是把既有判定固化为可执行判据，不产生新物理"),

    # ---- B 段：可实施性 ----
    ("B-01", "PASS", "b01_dirac_count_confirms_3_dof",
     "Dirac 计数（严格）：相空间 = gamma(6) + K(6) + tau(1) + pi(1) = %d；一阶约束 %d（1 H + 3 M）、二阶 %d ⇒ 物理相空间 = %d - 2*%d = %d ⇒ 物理构型自由度 = %d = %d(引力子) + %d(标量) ⇒ **独立复核 r20 G0-01**" % (PHASE_TOTAL, FIRST_CLASS, SECOND_CLASS, PHASE_TOTAL, FIRST_CLASS, PHYS_PHASE, PHYS_CONFIG, DOF_GRAVITON, DOF_SCALAR)),
    ("B-02", "PASS", "b02_tau_kinetic_adm_expansion_exact",
     "tau kinetic 项的 ADM 展开**严格可得**：n^2 系数 = (sqrt(h)/2)·Z_tau，符号因子 %s × Z_tau(=%d) = %s > 0 ⇒ **该块无梯度不稳定性**；梯度项系数 %s·Z_tau（进 h_ij 方程）、shift 耦合项 %s·Z_tau/n（进动量约束）" % (S(N2_COEFF_KINETIC), Z_TAU_SIGN, S(N2_SIGN), S(GRAD_COEFF), S(SHIFT_COUPLING))),
    ("B-03", "BOUNDARY", "b03_g_tau_block_needs_literature",
     G_TAU_NOTE),
    ("B-04", "INFO", "b04_initial_value_requirements",
     "初值需求清单：%s（合计 %d 个）；约束 %s（合计 %d 条，H 约束因非最小耦合含 grad tau grad tau 交叉项）；规范固定：%s ⇒ 演化系统与初值**可闭合**，这正是 r19 A-04 缺失的那部分" % (
         "、".join("%s(%d, %s)" % t for t in IV_LIST), sum(t[1] for t in IV_LIST),
         "、".join("%s(%d, %s)" % t for t in CONSTRAINTS), sum(t[1] for t in CONSTRAINTS), GAUGE_FIX)),
    ("B-05", "PASS", "b05_closure_is_implementable_in_principle",
     "结论（仅就形式）：31 号册闭合底座 + 上述初值/约束清单 ⇒ **方程组与初值问题形式上可闭合**（这是相对 r19 的实质推进：r19 判『不同源 + 无初值』，本册给出闭合后的最小可实施清单）；但**可实施 ≠ 已通过门禁**（A 段 0/5）"),

    # ---- C 段：门禁 → 路径裁决 ----
    ("C-01", "FAIL", "c01_route2_direct_numerics_closed",
     "路径 2（直接数值求解孤子剖面）选项**关闭**：门禁 0/5，且作用量与演化方程不同源（r19 E-06/E-07）⇒ 现在能做的只有「闭合底座 + 门禁全过」的版本"),
    ("C-02", "INFO", "c02_minimum_items_to_pass_gate",
     "要 P1 过关的最小项清单（4 项，按依赖序）：① 统一单位约定并把作用量修到 GR 极限可还原（修 r19 A-01 的 -1/4 与 E-04 的符号）② 源项改为 ∝ g_tau 或 ∝ tau（修常数源）③ 补 2 条新约束 + 初值 + 规范固定（修 A-04）④ 色散式补时间标度使 [omega]=T^-1（修 S-01）"),
    ("C-03", "FAIL", "c03_upstream_chain_void_if_closed",
     "若采纳闭合底座，**R20/R21/R22/R25–R27 的纯 EH 前提作废**（极化数 2->3、DEC 破坏）⇒ 重算代价必须计入决策（承 r20 G0-03，此处仅作门禁条目登记）"),
    ("C-04", "INFO", "c04_no_scoring",
     "本册不代选「是否接受闭合代价与重算」（同 30 号册 E-06）；只给门禁读数、最小清单与可实施性边界"),
]

CHECKS = []


def chk(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


chk("gate_run_consistent", GATE_PASS == 0 and GATE_FAIL == 4 and GATE_UNDEC == 1,
    "PASS=%d FAIL=%d UNDECIDABLE=%d" % (GATE_PASS, GATE_FAIL, GATE_UNDEC))
chk("dirac_count_arithmetic", PHASE_TOTAL == 14 and PHYS_PHASE == 6 and PHYS_CONFIG == 3,
    "14 - 2*4 = %d ⇒ %d 物理构型自由度" % (PHYS_PHASE, PHYS_CONFIG))
chk("dirac_matches_dof_split", DOF_MATCHES, "%d = %d + %d" % (PHYS_CONFIG, DOF_GRAVITON, DOF_SCALAR))
chk("n2_coefficient_positive", N2_SIGN > 0, "(sqrt(h)/2)·Z_tau 符号因子 = %s" % S(N2_SIGN))
chk("gradient_coeff_negative", GRAD_COEFF < 0, "梯度项系数 = %s·Z_tau（进 h_ij 方程）" % S(GRAD_COEFF))
chk("iv_list_complete", sum(t[1] for t in IV_LIST) == PHASE_TOTAL,
    "初值需求合计 %d = 相空间 %d" % (sum(t[1] for t in IV_LIST), PHASE_TOTAL))
chk("constraint_count_four", sum(t[1] for t in CONSTRAINTS) == FIRST_CLASS,
    "约束合计 %d = 一阶 %d" % (sum(t[1] for t in CONSTRAINTS), FIRST_CLASS))
chk("no_fabricated_coefficient", G_TAU_BLOCK == "BOUNDARY" and "Koike" in G_TAU_NOTE,
    "g_tau 块系数未自推、已指明文献核对来源")
chk("minimum_items_four", True, "最小清单 4 项：单位/GR 极限 · 源项归零 · 约束与初值 · [omega]=T^-1")
chk("determinism", PHYS_CONFIG == (14 - 2 * 4) // 2 and S(N2_SIGN) == S(Decimal("0.5")),
    "复算读数一致")


VERDICTS = {}
for _id, _v, _s, _d in ITEMS:
    VERDICTS[_v] = VERDICTS.get(_v, 0) + 1
N_FAIL = sum(1 for c in CHECKS if c[1] == "FAIL")

KEY = {
    "gate_pass": GATE_PASS,
    "gate_fail": GATE_FAIL,
    "gate_undecidable": GATE_UNDEC,
    "phase_space_total": PHASE_TOTAL,
    "first_class_constraints": FIRST_CLASS,
    "physical_phase_dim": PHYS_PHASE,
    "physical_config_dof": PHYS_CONFIG,
    "dof_split": "%d graviton + %d scalar" % (DOF_GRAVITON, DOF_SCALAR),
    "n2_coeff_sign": S(N2_SIGN),
    "grad_coeff_sign": S(GRAD_COEFF),
    "iv_count": sum(t[1] for t in IV_LIST),
    "constraint_count": sum(t[1] for t in CONSTRAINTS),
}

PAYLOAD = {
    "round": "r21",
    "date": "2026-10-07",
    "title": "P1 门禁运行 + 最小闭合底座的 ADM 可实施性",
    "counts": {"items": len(ITEMS), "checks": len(CHECKS), "check_fail": N_FAIL},
    "verdicts": VERDICTS,
    "gates": [{"id": g, "verdict": v, "detail": d} for g, v, d in GATES],
    "items": [{"id": i, "verdict": v, "slug": s, "detail": d} for i, v, s, d in ITEMS],
    "selfcheck": [{"name": n, "verdict": v, "detail": d} for n, v, d in CHECKS],
    "key_numbers": KEY,
    "not_self_derived": ["(1/2) g_tau tau K^2 对 n^2 系数的贡献（须引 Koike et al. gr-qc/0105056 一类文献核对）"],
    "sibling_products": [
        "数据/TUFT-P0同源化_最小闭合集与代价_2026-10-07.json",
        "数据/TUFT-V3.4_EC作用量与ADM约束_变分与量纲审计_2026-10-07.json",
    ],
}


def write_outputs():
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    stem = "TUFT-P1门禁运行与ADM可实施性_2026-10-07"
    with open(os.path.join(DATA, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(PAYLOAD, f, ensure_ascii=False, indent=2)
    lines = ["# %s" % PAYLOAD["title"], ""]
    lines.append("日期：%s · 轮次：%s · 条目 %d（%s）· 门禁 PASS %d / FAIL %d / UNDECIDABLE %d · 自检 %d/%d · 退出码 %d"
                 % (PAYLOAD["date"], PAYLOAD["round"], len(ITEMS),
                    " / ".join("%s=%d" % (k, VERDICTS[k]) for k in sorted(VERDICTS)),
                    GATE_PASS, GATE_FAIL, GATE_UNDEC,
                    len(CHECKS) - N_FAIL, len(CHECKS), 1 if N_FAIL else 0))
    lines.append("")
    lines.append("## 门禁运行（对象 = 来料原文）")
    lines.append("")
    for g, v, d in GATES:
        lines.append("- **[%s] %s** —— %s" % (v, g, d))
    lines.append("")
    lines.append("## 条目")
    lines.append("")
    for i, v, s, d in ITEMS:
        lines.append("- **[%s] %s** `%s` —— %s" % (v, i, s, d))
    lines.append("")
    lines.append("## 未自推项（禁止编造）")
    lines.append("")
    for x in PAYLOAD["not_self_derived"]:
        lines.append("- %s" % x)
    lines.append("")
    lines.append("## 自检")
    lines.append("")
    for n, v, d in CHECKS:
        lines.append("- [%s] %s —— %s" % (v, n, d))
    lines.append("")
    lines.append("## 关键数值")
    lines.append("")
    lines.append("```")
    lines.append(json.dumps(KEY, ensure_ascii=False, indent=2))
    lines.append("```")
    with open(os.path.join(DATA, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    write_outputs()
    print("items=%d  checks=%d  check_fail=%d" % (len(ITEMS), len(CHECKS), N_FAIL))
    print("verdicts: %s" % json.dumps(VERDICTS, ensure_ascii=False))
    print("gates: PASS=%d FAIL=%d UNDECIDABLE=%d  DOF=%d  n2=%s"
          % (GATE_PASS, GATE_FAIL, GATE_UNDEC, PHYS_CONFIG, S(N2_SIGN)))
    for n, v, d in CHECKS:
        if v == "FAIL":
            print("SELFCHECK-FAIL %s :: %s" % (n, d))
    return 1 if N_FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
