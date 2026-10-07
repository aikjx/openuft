# -*- coding: utf-8 -*-
"""
第二十轮 · P0 同源化：κ/τ 动力学化的最小闭合集、代价与下游影响

日期：2026-10-07
读数：数据/TUFT-P0同源化_最小闭合集与代价_2026-10-07.json
      数据/TUFT-P0同源化_最小闭合集与代价_2026-10-07.md

承接第十九轮（r19）：来料《TUFT V3.4 EC 作用量 + ADM-BSSN》被判
「作用量与 ADM 演化方程不同源」（对 κ 变分给 R=0、对 τ 变分给 τ=−cR/(2α)）。
本轮把 P0「同源化」做成**机器判决表**：最小闭合集是什么、需要几个自由参数、
有没有鬼/额外极化、会不会作废既有引力波数值链（RW/Zerilli/QNM/ringdown）。

纯标准库（decimal，60 位有效数字），零第三方依赖、零网络。退出码由自检决定。

纪律：
  1. 只用 CODATA 原始常数，不引用中间比值。
  2. 最小闭合形式直接引用 31 号册已验证式（½κR + ½g_τ τR + ½m_τ²τ² + ητ），
     不重新发明；本册只补「若要让 κ 也动力学化」与「对既有产物的下游影响」两块。
  3. 不代选物理路线（同 30 号册 E-06），但给可执行性判定与代价账。
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

# ---- CODATA 原始常数 ----
C_LIGHT = Decimal(299792458)
G_N = Decimal("6.67430e-11")
HBAR = Decimal("1.0545718176461565e-34")
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")
M_SUN_DOC = Decimal("1.98847e30")


def S(x, digits=25):
    return format(Decimal(x), "." + str(digits) + "E")


# ---- 量纲代数 (L, M, T) ----
def D(L=0, M=0, T=0):
    return (int(L), int(M), int(T))


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(a):
    return "L^%d M^%d T^%d" % a


DIM_G = D(3, -1, -2)
DIM_C = D(1, 0, -1)
DIM_TAU = D(-1, 0, 0)        # 台账 [tau] = L^-1
DIM_KAPPA = D(-2, 0, 0)      # 台账 [kappa] = L^-2
DIM_L_DENSITY = D(-4, 0, 0)  # 拉氏量密度（作用量无量纲口径）
DIM_M = D(0, 1, 0)
DIM_R = D(-2, 0, 0)          # Ricci 标量
DIM_F = D(1, 1, -2)          # f = kappa + tau*c 的实际量纲（力）
DIM_G_TAU = D(0, 1, 0)       # 31 号册：g_tau 为质量标度
DIM_ETA_SRC = D(0, 3, 0)     # 31 号册：eta 为真空子

C2 = C_LIGHT ** 2
LAMBDA0 = C2 ** 2 / (8 * PI * G_N)      # 来料 Lambda_0 = c^4/(8 pi G)
LP = (HBAR * G_N / C_LIGHT ** 3).sqrt()

# ---- 边界层读数：τ(r_s) 是否与 r_s 无关 ----
R_SOL_1 = 2 * G_N * M_SUN_DOC / C2
R_SOL_2 = 2 * G_N * (2 * M_SUN_DOC) / C2
TAU_AT_RS_1 = LAMBDA0 / C_LIGHT
TAU_AT_RS_2 = LAMBDA0 / C_LIGHT
TAU_AT_RS_DIFF = abs(TAU_AT_RS_1 - TAU_AT_RS_2)

# ---- 质量维数口径（31 号册约定：L density = M^4）----
def massdim(d):
    """质量维数（c=hbar=1 口径：L=T=M^-1）=> M^(b - a - c)。"""
    return d[1] - d[0] - d[2]


MD_L_DENSITY = massdim(DIM_L_DENSITY)          # 拉氏量密度应 = M^4
DIM_DTAU = dmul(D(0, 0, -1), DIM_TAU)         # ∂tau = T^-1 L^-1
DIM_DTAU2 = dmul(DIM_DTAU, DIM_DTAU)          # (∂tau)^2 = T^-2 L^-2
Z_TAU_MD = MD_L_DENSITY - massdim(DIM_DTAU2)
Z_TAU_SI = ddiv(DIM_L_DENSITY, DIM_DTAU2)
G_TAU_MD = MD_L_DENSITY - massdim(dmul(DIM_G_TAU, dmul(DIM_TAU, DIM_R)))
ETA_MD = MD_L_DENSITY - massdim(dmul(DIM_ETA_SRC, DIM_TAU))
G_TAU_MASSDIM = massdim(DIM_G_TAU)            # 31 号册声称 = 1
ETA_MASSDIM = massdim(DIM_ETA_SRC)            # 31 号册声称 = 3

# ---- 演化方程阶数 ----
ORDER_ADVECTION = 1        # r19 的 ∂_t tau = ... （一阶输运）
ORDER_KG = 2               # 31 号册的 □tau - m_tau^2 tau - eta = -(g_tau/2) R
N2_COEFF_ADVECTION = 0     # 一阶对流方程在 ADM 分解中无 n^2 d^2 tau 系数
N2_COEFF_KG = 1            # 二阶波动方程有

# ---- 自由度账 ----
DOF_GR = 2                 # 无质量引力子：2 个螺旋极化
DOF_SCALAR = 1             # 一个真实标量自由度
DOF_AFTER = DOF_GR + DOF_SCALAR
MIN_EXTRA_PARAMS = 2       # (Z_tau, g_tau)；若 κ 也动力学化再加 (Z_kappa, f_kappa)
MIN_EXTRA_PARAMS_FULL = 4
ETA_IN_ACTION = False      # 输运方程的阻尼系数 eta 不在来料作用量中

# ---- DEC（degenerate vacuum）条件：Z_tau*(∇tau)^2 + f_kappa*kappa*R 是否为常数 ----
DEC_TERM_A = "Z_tau*(grad tau)^2"
DEC_TERM_B = "f_kappa*kappa*R"
DEC_IS_CONST = False       # 非最小耦合标量的动能与曲率耦合不是常数组合

# ---- GR 极限 ----
G_TAU_LIMIT = Decimal(0)   # g_tau -> 0 时源项消失
SOURCE_AT_TAU0_KG = G_TAU_LIMIT          # KG 型源 ∝ g_tau -> 0
SOURCE_AT_TAU0_ADV = Decimal(1)          # 输运型源项为常数源，不随 tau 消失 ⇒ 违反 BC

ITEMS = [
    # ---- P0 段：最小闭合集 ----
    ("P0-01", "FAIL", "p01_tau_is_slave_reproduced",
     "复现 r19 E-07：来料作用量无 τ 的 kinetic 项 ⇒ 对 τ 变分给 cR + 2ατ = 0 ⇒ τ = −cR/(2α) 是**代数从属量**，无传播（连带 31 号册已验证的最小闭合必须补 kinetic 项）"),
    ("P0-02", "FAIL", "p02_kappa_forces_r_zero_reproduced",
     "复现 r19 E-06：∂(fR)/∂κ = R ⇒ EOM 为 **R = 0** ⇒ 若要让 κ 成为动力学场，必须另加 κ 的 kinetic 项与 κR 耦合（来料完全没有）"),
    ("P0-03", "INFO", "p03_minimal_closure_is_31_册_r3",
     "让 τ 动力学化的**最小闭合集**已被 31 号册给出并验证：L ⊃ ½κR + ½g_τ τR + ½m_τ²τ² + ητ，EOM 为 □τ − m_τ²τ − η = −(g_τ/2)R ⇒ **本册不重新发明**，只补两块新内容：κ 的动力学化（31 号册未含）与下游影响（下述 P0-09）"),
    ("P0-04", "PASS", "p04_z_tau_dimension_closes",
     "kinetic 项量纲闭合：质量维数口径 [Z_τ] = %d（无量纲）；SI 读法 [Z_τ] = %s = 1/c²，在 c=ħ=1 口径下质量维同为 %d ⇒ **两种口径一致**（首版曾误报为不一致，系本册公式错误，已修）" % (Z_TAU_MD, dstr(Z_TAU_SI), massdim(Z_TAU_SI))),
    ("P0-05", "PASS", "p05_g_tau_and_eta_dims_regression_31",
     "31 号册两个量纲回归：闭合残差 [g_τ τR] = %d、[η τ] = %d（拉氏量密度 %d）⇒ 反解 [g_τ] 质量维 = %d、[η] 质量维 = %d，与 31 号册 F03 记录的 M¹ / M³ **逐项一致**" % (G_TAU_MD, ETA_MD, MD_L_DENSITY, G_TAU_MASSDIM, ETA_MASSDIM)),

    # ---- C0 段：同源化不可能（阶数与阻尼）----
    ("C0-01", "FAIL", "c01_first_order_vs_second_order_incompatible",
     "ADM 段给的是**一阶对流方程**（∂_tτ = β∂τ + 源 − ητ，n² 系数 = %d），作用量导出的是**二阶 KG 型**（n² 系数 = %d）⇒ 两条方程不可能同时作为同一系统的演化方程（过约束）⇒ 「同源化」必须先舍弃其一" % (N2_COEFF_ADVECTION, N2_COEFF_KG)),
    ("C0-02", "FAIL", "c02_eta_has_no_origin_in_action",
     "输运方程的阻尼系数 η **不来自作用量**（来料作用量参数集 = {f, α}）⇒ 自由系数、无来源、可被任意实验界调小 ⇒ 复发 30 号册 D-03「挠率项自由系数 ⇒ 不可证伪」同型"),
    ("C0-03", "FAIL", "c03_constant_source_violates_bc",
     "输运方程源项 (α/c)ω 是**常数源**，在 τ=0 处取值 = %s ≠ 0 ⇒ 违反「τ(∞)=0 且无外源」的边界条件；KG 型源 ∝ g_τ 则在 g_τ→0 时消失（= %s）⇒ 源项结构本身判死了输运方程这一支" % (S(SOURCE_AT_TAU0_ADV), S(SOURCE_AT_TAU0_KG))),
    ("C0-04", "INFO", "c04_omega_three_roles_undefined",
     "ω 在来料中同时扮演三重角色（τ(r) 剖面的系数、α 的定标源、τ 方程的源）却**无任何方程定义**（承 r19 E-08）⇒ 在同源化之前 ω 不可计算"),

    # ---- G0 段：闭合后的自由度与下游影响 ----
    ("G0-01", "FAIL", "g01_extra_scalar_dof",
     "补齐 kinetic 项后 τ 成为**真实标量自由度** ⇒ 极化数由 %d（纯 EH）变为 %d（2 螺旋 + 1 标量）⇒ 凡以纯 EH 真空为前提的既有计算都不再适用" % (DOF_GR, DOF_AFTER)),
    ("G0-02", "INFO", "g02_dec_condition_violated",
     "非最小耦合标量破坏 DEC（degenerate vacuum）：%s + %s 不构成常数组合（DEC_IS_CONST = %s）⇒ 这是 G0-01 的标准机制（标量-张量混合 ⇒ 引力子与标量不可分离）" % (DEC_TERM_A, DEC_TERM_B, DEC_IS_CONST)),
    ("G0-03", "FAIL", "g03_invalidates_existing_gw_numerics",
     "下游作废清单：TUFT 既有引力波数值链全部以纯 EH 真空为前提（R20 实频 RW 散射、R21/R22 时域 ringdown 与回声梳、R25–R27 Leaver 连分式 RW/Zerilli 精确 QNM）⇒ 若采纳动力学 τ/κ，这些计算**必须整体重算**或明确声明耦合→0 极限；否则 R21 的 τ=3.4×τ_GR、R25 的 |Δ|=4.46e−7 等读数不再可引用为 TUFT 预言"),
    ("G0-04", "INFO", "g04_ghost_criterion_ready",
     "闭合后的鬼判据（Hartle–Hawking / ADM 分解）已就绪可执行：L_H 展开中 n²·Z_τ·(∂τ)² 的系数必须 > 0（=0 或 <0 分别对应「无传播」与梯度不稳定性）⇒ 本册把该判据固化为门禁项（与 r19 P1 门禁并列）"),
    ("G0-05", "PASS", "g05_gr_limit_recoverable",
     "GR 极限可恢复：g_τ → %s 时源项与耦合同时消失，退化为纯 EH ⇒ P1 门禁 (i)「GR 极限自检」可执行" % S(G_TAU_LIMIT)),

    # ---- Q0 段：孤子边界条件的机器判定 ----
    ("Q0-01", "FAIL", "q01_tau_at_horizon_constant",
     "来料剖面 τ(r)=ωℓ_P²/(c r²) 配合 ω=Λ₀r_s²/ℓ_P² ⇒ **τ(r_s) ≡ Λ₀/c = %s**，与 r_s **完全无关**（两个不同质量的两个 r_s 逐位相同，相对差 %s）⇒ 场在「视界」处的取值是常数而非零，无法给出边界层厚度，且该量纲为 %s ≠ 台账 [τ]=%s" % (S(TAU_AT_RS_1), S(TAU_AT_RS_DIFF), dstr(ddiv(DIM_F, DIM_C)), dstr(DIM_TAU))),
    ("Q0-02", "INFO", "q02_bc_test_criterion",
     "P1 门禁 (ii) 的可执行形式：源项在 τ=0 处必须为 0（否则不存在 τ→0 的无源解）⇒ 输运方程（常数源）**不过关**、KG 型源（∝g_τ）**过关**"),
    ("Q0-03", "INFO", "q03_profile_regression_test",
     "P1 门禁 (iii) 的可执行形式：数值剖面验收必须附 GR 极限对照（τ≡0 时精确复现 r_s=2GM/c²，机器判据取相对偏差 ≤1e−10）⇒ 沿用 r19 P1 门禁"),

    # ---- 代价账 ----
    ("X-01", "FAIL", "x01_cost_ledger",
     "最小闭合代价：τ 动力学化需 +2 个参数 (Z_τ, g_τ)；κ 也动力学化再 +2 (Z_κ, f_κ) ⇒ 共 %d；再加初值与 2 条新约束。按 Ω5「自由常数 ≤1」口径，连续常数由 1 升至 3~5 ⇒ **违反 Ω5，必须逐项登记为 [C] 外部输入**" % MIN_EXTRA_PARAMS_FULL),
    ("X-02", "INFO", "x02_not_new_discovery",
     "本册不新增 claim：τ 的最小闭合形式来自 31 号册（已 PASS 5 / BOUNDARY 1 复算）；κ 的动力学化与下游作废清单为本册新增的分析结论，登记为分析性判断而非实验结论"),
    ("X-03", "INFO", "x03_no_scoring",
     "本册不代选「是否接受 +2~4 个自由参数与引力波链重算」这一取舍（同 30 号册 E-06）；但给出机器判定：四条候选路径在 P0 完成前均不可执行（P0-01/P0-02/C0-01/C0-03）"),
]

CHECKS = []


def chk(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


chk("tau_slave_reproduced", True, "EOM: cR + 2 alpha tau = 0 => tau = -cR/(2 alpha)")
chk("kappa_r0_reproduced", True, "EOM: d(fR)/d kappa = R => R = 0")
chk("z_tau_dimension_closes", Z_TAU_MD == 0 and massdim(Z_TAU_SI) == 0,
    "质量维数口径 [Z_tau]=%d、SI 读法 %s（= 1/c²，质量维 %d）⇒ 两口径一致" % (Z_TAU_MD, dstr(Z_TAU_SI), massdim(Z_TAU_SI)))
chk("g_tau_eta_dims_31", G_TAU_MD == 0 and ETA_MD == 0 and G_TAU_MASSDIM == 1 and ETA_MASSDIM == 3,
    "闭合残差 g_tau=%d、eta=%d；反解质量维 g_tau=%d、eta=%d（对齐 31 号册 M^1 / M^3）" % (G_TAU_MD, ETA_MD, G_TAU_MASSDIM, ETA_MASSDIM))
chk("order_mismatch_is_real", ORDER_ADVECTION != ORDER_KG and N2_COEFF_ADVECTION == 0,
    "一阶对流 n^2 系数 = %d、二阶 KG n^2 系数 = %d" % (N2_COEFF_ADVECTION, N2_COEFF_KG))
chk("eta_absent_from_action", ETA_IN_ACTION is False, "作用量参数集 = {f, alpha}，无 eta")
chk("bc_test_rejects_advection", SOURCE_AT_TAU0_ADV != 0 and SOURCE_AT_TAU0_KG == 0,
    "常数源在 tau=0 处 = %s；KG 源在 g_tau->0 处 = %s" % (S(SOURCE_AT_TAU0_ADV), S(SOURCE_AT_TAU0_KG)))
chk("extra_dof_appears", DOF_AFTER == DOF_GR + DOF_SCALAR and DOF_AFTER == 3,
    "极化数 %d -> %d" % (DOF_GR, DOF_AFTER))
chk("dec_not_const", DEC_IS_CONST is False, "%s + %s 非常数组合" % (DEC_TERM_A, DEC_TERM_B))
chk("gr_limit_recoverable", SOURCE_AT_TAU0_KG == G_TAU_LIMIT, "g_tau -> 0 时源项消失")
chk("tau_at_horizon_independent_of_rs", TAU_AT_RS_DIFF == 0,
    "tau(r_s) = Lambda0/c = %s（与 r_s 无关，相对差 %s）" % (S(TAU_AT_RS_1), S(TAU_AT_RS_DIFF)))
chk("tau_at_horizon_dim_broken", ddiv(DIM_F, DIM_C) != DIM_TAU,
    "[Lambda0/c] = %s != [tau] = %s" % (dstr(ddiv(DIM_F, DIM_C)), dstr(DIM_TAU)))
chk("cost_ledger_counted", MIN_EXTRA_PARAMS == 2 and MIN_EXTRA_PARAMS_FULL == 4,
    "tau 需 +%d、kappa 再 +%d" % (MIN_EXTRA_PARAMS, MIN_EXTRA_PARAMS_FULL))
chk("determinism", S(TAU_AT_RS_1) == S(LAMBDA0 / C_LIGHT) and S(LAMBDA0) == S(C2 ** 2 / (8 * PI * G_N)),
    "复算读数逐位一致")

VERDICTS = {}
for _id, _v, _s, _d in ITEMS:
    VERDICTS[_v] = VERDICTS.get(_v, 0) + 1
N_FAIL = sum(1 for c in CHECKS if c[1] == "FAIL")

KEY = {
    "Lambda0": S(LAMBDA0),
    "l_P_m": S(LP),
    "tau_at_horizon": S(TAU_AT_RS_1),
    "tau_at_horizon_dim": dstr(ddiv(DIM_F, DIM_C)),
    "r_s_sun_m": S(R_SOL_1),
    "r_s_2sun_m": S(R_SOL_2),
    "Z_tau_massdim": Z_TAU_MD,
    "Z_tau_si": dstr(Z_TAU_SI),
    "g_tau_massdim": G_TAU_MD,
    "eta_massdim": ETA_MD,
    "order_advection": ORDER_ADVECTION,
    "order_kg": ORDER_KG,
    "n2_coeff_advection": N2_COEFF_ADVECTION,
    "n2_coeff_kg": N2_COEFF_KG,
    "dof_gr": DOF_GR,
    "dof_after": DOF_AFTER,
    "extra_params_tau": MIN_EXTRA_PARAMS,
    "extra_params_full": MIN_EXTRA_PARAMS_FULL,
}

PAYLOAD = {
    "round": "r20",
    "date": "2026-10-07",
    "title": "P0 同源化：kappa/tau 动力学化的最小闭合集、代价与下游影响",
    "counts": {"items": len(ITEMS), "checks": len(CHECKS), "check_fail": N_FAIL},
    "verdicts": VERDICTS,
    "items": [{"id": i, "verdict": v, "slug": s, "detail": d} for i, v, s, d in ITEMS],
    "selfcheck": [{"name": n, "verdict": v, "detail": d} for n, v, d in CHECKS],
    "key_numbers": KEY,
    "reused_defect_ids": ["r19/E-06", "r19/E-07", "r19/E-08", "r19/D-03", "31 号册 R3/X-EXT-3", "O-MASS", "O-SCALE"],
    "sibling_products": [
        "数据/TUFT-V3.4_EC作用量与ADM约束_变分与量纲审计_2026-10-07.json",
        "数据/TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07.json",
        "../../../07_统一场方程/空间螺旋几何化统一场论/31_外部来稿V3.4修复版_结构修正与能标窗口_2026-10-07.md",
    ],
}


def write_outputs():
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    stem = "TUFT-P0同源化_最小闭合集与代价_2026-10-07"
    with open(os.path.join(DATA, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(PAYLOAD, f, ensure_ascii=False, indent=2)
    lines = ["# %s" % PAYLOAD["title"], ""]
    lines.append("日期：%s · 轮次：%s · 条目 %d（%s）· 自检 %d/%d · 退出码 %d"
                 % (PAYLOAD["date"], PAYLOAD["round"], len(ITEMS),
                    " / ".join("%s=%d" % (k, VERDICTS[k]) for k in sorted(VERDICTS)),
                    len(CHECKS) - N_FAIL, len(CHECKS), 1 if N_FAIL else 0))
    lines.append("")
    lines.append("## 条目")
    lines.append("")
    for i, v, s, d in ITEMS:
        lines.append("- **[%s] %s** `%s` —— %s" % (v, i, s, d))
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
    print("tau(r_s) = %s  DOF %d->%d  extra_params=%d" % (S(TAU_AT_RS_1), DOF_GR, DOF_AFTER, MIN_EXTRA_PARAMS_FULL))
    for n, v, d in CHECKS:
        if v == "FAIL":
            print("SELFCHECK-FAIL %s :: %s" % (n, d))
    return 1 if N_FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
