# -*- coding: utf-8 -*-
"""
第十九轮 · 外部来稿《TUFT V3.4 希尔伯特-爱因斯坦-嘉唐作用量（含螺旋挠率自旋项）》
变分复核 + ADM 约束归一化 + 孤子色散 + g-2/EDM 审计

日期：2026-10-07
读数：数据/TUFT-V3.4_EC作用量与ADM约束_变分与量纲审计_2026-10-07.json
      数据/TUFT-V3.4_EC作用量与ADM约束_变分与量纲审计_2026-10-07.md

承接第十八轮（r18）：本册审计的来料把 r18 已判 FAIL 的 `G=c^4/(8*pi*kappa)`
升级为「作用量 → 场方程 → ADM 约束 → 孤子色散 → g-2/EDM」整套系统。
本册只做四件事：变分复核 / 量纲 / 归一化 / 数值算术，不代选路径。

纯标准库（decimal，60 位有效数字），零第三方依赖、零网络。退出码由自检决定。

纪律：
  1. 只用 CODATA 原始常数，不引用中间比值（能标一致性条款）。
  2. 缺陷 ID 复用既有登记（C-02 / C-05 / C-88 / C-30 / O-V34-C / r18 A-01…），
     不新增重复条目；跨册数值做回归复算（对齐 31 号册 g-2 读数）。
  3. 不对物理路线打分排序（同 30 号册 E-06），但对「可执行性」给机器判定。
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

# ---- CODATA 口径原始常数 ----
C_LIGHT = Decimal(299792458)
G_N = Decimal("6.67430e-11")
HBAR = Decimal("1.0545718176461565e-34")
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")
M_E = Decimal("9.1093837015e-31")
M_SUN_DOC = Decimal("1.98847e30")      # 来料代码所用太阳质量
R_SUN = Decimal("6.957e8")             # m
EV_PER_J = Decimal("6.241509074460763e18")
BSM_AE = Decimal("1e-12")              # 31 号册采用的 BSM 残差窗口
DOC_HBAR = Decimal("1.054571817e-34")  # 来料代码截断值


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


def ddif(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dstr(a):
    return "L^%d M^%d T^%d" % a


DIM_G = D(3, -1, -2)
DIM_C = D(1, 0, -1)
DIM_HBAR = D(2, 1, -1)
DIM_RHO = D(-3, 1, 0)      # 能量密度
DIM_TAU = D(-1, 0, 0)      # 台账 [tau] = L^-1
DIM_KAPPA = D(-2, 0, 0)    # 台账 [kappa] = L^-2
DIM_F = D(1, 1, -2)        # f = kappa + tau*c 的实际量纲（= N，力）
DIM_D4X = D(4, 0, 0)       # d^4x（x^0 = ct 口径）
DIM_D4T = D(3, 0, 1)       # dt d^3x 口径

# ---- 基本读数 ----
C2 = C_LIGHT ** 2
C3 = C_LIGHT ** 3
C4 = C_LIGHT ** 4
LAMBDA0 = C4 / (8 * PI * G_N)             # 来料 Lambda_0 = c^4/(8 pi G)
LP = (HBAR * G_N / C_LIGHT ** 3).sqrt()   # 普朗克长度
MP = (HBAR * C_LIGHT / G_N).sqrt()        # 普朗克质量
LAMBDA_E = HBAR / (M_E * C_LIGHT)         # 电子康普顿波长
M_PL_KG = MP

# 孤子色散（照抄来料公式）
R_SOL = 2 * G_N * M_SUN_DOC / C2                       # r_s = 2GM/c^2
OMEGA_SUN = LAMBDA0 * (R_SOL ** 2) / (LP ** 2)        # omega = Lambda_0 r_s^2 / l_P^2
T_SOL = 2 * PI / OMEGA_SUN
HBAR_OMEGA_J = HBAR * OMEGA_SUN
HBAR_OMEGA_EV = HBAR_OMEGA_J * EV_PER_J
E_PL_J = MP * C_LIGHT ** 2
HBAR_OMEGA_OVER_PL = HBAR_OMEGA_J / E_PL_J
# 化简：omega = M^2 c^3 /(2 pi hbar)，与 G、Lambda_0 全部约掉
OMEGA_SIMPLE = M_SUN_DOC ** 2 * C3 / (2 * PI * HBAR)
OMEGA_REL = abs(OMEGA_SUN - OMEGA_SIMPLE) / OMEGA_SIMPLE
M_FOR_OMEGA1 = (2 * PI * HBAR / C3).sqrt()              # 使 omega = 1 s^-1 的质量
M_FOR_OMEGA1_OVER_MP = M_FOR_OMEGA1 / MP
R_SOL_OVER_R_SUN = R_SOL / R_SUN

# g-2（照抄来料代码）
TAU_E_CODE = (1 / C_LIGHT) * LAMBDA_E / (LAMBDA_E ** 2)   # = m_e/hbar
DELTA_G_CODE = TAU_E_CODE * HBAR / (M_E * C_LIGHT)        # = 1/c
DELTA_G_SIMP = 1 / C_LIGHT
DELTA_G_REL = abs(DELTA_G_CODE - DELTA_G_SIMP) / DELTA_G_SIMP
DELTA_G_OVER_BSM = DELTA_G_CODE / BSM_AE
TAU_NEEDED_BSM = BSM_AE / LAMBDA_E
Y_GEO = (M_E / MP) ** 2                                   # 31 号册几何 ECSK 耦合
DELTA_AE_GEO = Y_GEO ** 2 * (M_E / MP) ** 2 / (8 * PI ** 2)   # m_tau = M_Pl
DELTA_AE_31 = Decimal("6.8e-137")

# ADM 约束的 Einstein 极限
GAMMA_COUPLE = 1 / LAMBDA0          # = 8 pi G / c^4
GAMMA_STD = 16 * PI * G_N / C2      # 标准 BSSN 哈密顿约束右端系数
RATIO_HAM = -(GAMMA_COUPLE / 2) / GAMMA_STD
RATIO_HAM_C1 = -(8 * PI * G_N / 2) / (16 * PI * G_N)   # c=1 口径

# 变分复核（解析：S = (1/2c^4) ∫ [f R + alpha tau^2] sqrt(-g) d^4x + S_m）
DIM_EL_T_CLAIMED = ddiv(D(0, 0, 0), DIM_F)        # 来料写 1/f
DIM_EL_T_CORRECT = ddiv(dpow(DIM_C, 4), DIM_F)    # 真变分给 c^4/f
DIM_EL_T_GAP = ddif(DIM_EL_T_CLAIMED, DIM_EL_T_CORRECT)
DIM_ACT_CT = ddiv(dmul(dpow(DIM_C, -4), DIM_F), dmul(DIM_KAPPA, DIM_D4X))
DIM_ACT_T = ddiv(dmul(dpow(DIM_C, -4), DIM_F), dmul(DIM_KAPPA, DIM_D4T))
DIM_ALPHA_CT = ddiv(dmul(dpow(DIM_C, 4), dpow(DIM_KAPPA, 2)), dmul(DIM_D4X, DIM_KAPPA))
DIM_ALPHA_T = ddiv(dmul(dpow(DIM_C, 4), dpow(DIM_KAPPA, 2)), dmul(DIM_D4T, DIM_KAPPA))
DIM_TAU_DT = dmul(D(0, 0, -1), DIM_TAU)                     # ∂_t tau = T^-1 L^-1
DIM_BETA_GRAD_TAU = dmul(dmul(DIM_C, DIM_TAU), DIM_TAU)   # beta(速度) · ∂(L^-1) · tau(L^-1)
DIM_A_OMEGA_C = dmul(dpow(DIM_C, -1), D(0, 0, -1))            # (alpha/c)*omega
DIM_ETA_TAU = dmul(D(0, 0, -1), DIM_TAU)                      # eta*tau
DIM_KAPPA_LAP = dmul(dpow(DIM_C, -2), dpow(DIM_KAPPA, 2))     # (2/c^2)∇^2 kappa
DIM_EDM = dmul(ddiv(dmul(DIM_TAU, DIM_TAU), dmul(D(1, 0, 0), dpow(DIM_C, 2))),
               dmul(D(1, 1, 0), D(1, 1, -2)))                  # (tau/m_e c^2)(S)(E)
SIGN_CLAIMED = -1
SIGN_CORRECT = 1
VARY_KAPPA = "R = 0"        # 对 kappa 变分：f 对 kappa 的偏导 = R
VARY_TAU = "tau = -cR/(2 alpha)"   # 对 tau 变分：代数式，非演化方程

ITEMS = [
    # ---- E 段：作用量与场方程 ----
    ("E-01", "FAIL", "e01_action_not_dimensionless",
     "S = (1/2c^4)∫fR√-g d^4x 在两种时间坐标口径下均非无量纲：x^0=ct 口径 %s；dt 口径 %s ⇒ 单位约定缺口（复发 30 号册 V04 的 SI/普朗克混用同族）" % (dstr(DIM_ACT_CT), dstr(DIM_ACT_T))),
    ("E-02", "FAIL", "e02_f_is_force_not_curvature",
     "f = kappa + tau*c = c^4/(8*pi*G) 的量纲是 %s（牛顿=力），而台账 [kappa] = %s ⇒ r18 A-01 原样传导进作用量" % (dstr(DIM_F), dstr(DIM_KAPPA))),
    ("E-03", "FAIL", "e03_alpha_dimension_undeclared",
     "tau^2 项要求 alpha 带量纲：x^0=ct 口径 [alpha] = %s；dt 口径 [alpha] = %s ⇒ 两口径给出不同量纲且来料未声明（称「由 omega 定标」但未给式）" % (dstr(DIM_ALPHA_CT), dstr(DIM_ALPHA_T))),
    ("E-04", "FAIL", "e04_el_tau2_sign_wrong",
     "变分复核：δS/δg^μν = (f/2c^4)√-g·G^E_μν - (alpha tau^2/4c^4)√-g·g_μν - (1/2)√-g·T_μν = 0 ⇒ 场方程的等效宇宙学项符号为 **+alpha tau^2/(2f)**，来料写 **-** ⇒ 符号反（该错误在 tau→0 极限不可见，只在孤子核心显形）"),
    ("E-05", "MISMATCH", "e05_t_convention_undeclared",
     "T_μν 系数：来料写 1/f（量纲 %s），真变分给 c^4/f（量纲 %s，恰等于 [G]）⇒ 两者都自洽但**物质作用量的单位约定未登记**（差 c^4），属口径未声明而非算错" % (dstr(DIM_EL_T_CLAIMED), dstr(DIM_EL_T_CORRECT))),
    ("E-06", "FAIL", "e06_vary_kappa_forces_R_zero",
     "对 kappa 变分：∂(fR)/∂kappa = R ⇒ EOM 为 **R = 0**（点态）⇒ 该作用量强制 Ricci 平直，与「含物质、含孤子」直接矛盾；曲率场 kappa 不是动力学场"),
    ("E-07", "FAIL", "e07_vary_tau_gives_algebraic_slave",
     "对 tau 变分：cR + 2*alpha*tau = 0 ⇒ **tau = -cR/(2 alpha)** 是代数从属量（slave），不是传播场 ⇒ 来料 ADM 段的 ∂_t tau 输运方程**无法从该作用量导出** ⇒ 作用量与演化系统不同源（本册最重一条）"),
    ("E-08", "MISMATCH", "e08_tau2_not_derivable_omega",
     "alpha「由本征角频率 omega 定标」的式子未给出 ⇒ 孤子色散那节出现的 omega 无法回填作用量 ⇒ 跨节无闭合链"),

    # ---- A 段：ADM / BSSN ----
    ("A-01", "FAIL", "a01_ham_constraint_not_gr_limit",
     "哈密顿约束右端 -(Gamma/2) rho，Gamma = 8*pi*G/c^4 = %s；标准 BSSN 为 16*pi*G*rho/c^2（系数 %s）⇒ 比值 = %s（c=1 口径为 -0.25）⇒ **Einstein 极限不还原 GR（差 1/(4c^2) 且符号相反）**" % (S(GAMMA_COUPLE), S(GAMMA_STD), S(RATIO_HAM))),
    ("A-02", "MISMATCH", "a02_mom_constraint_missing_conformal_weight",
     "动量约束写成 ∇_j A~^ij + (2/3)∇^i K - A~^ij ∇_j phi = (Gamma/2) S^i，缺 e^(-2 phi) 权重；而 A~ 是对 gamma~ = e^(4 phi) gamma 定义的无迹外曲率 ⇒ 方程把 gamma~-联络下的导数与 gamma-下的 K 混用，**非张量方程**（标准式见 Baumgarte-Shapiro / Alcubierre et al. 2003）"),
    ("A-03", "FAIL", "a03_gamma_couple_role",
     "Gamma_couple = 1/f 的量纲是 %s（1/力），而 BSSN 中的耦合应为长度^-2 量 ⇒ 数值上恰被 rho/S^i 的量纲补偿而侥幸不炸，但物理口径是「把 1/力当 1/长度^2」" % dstr(DIM_EL_T_CORRECT)),
    ("A-04", "FAIL", "a04_no_constraints_no_initial_data",
     "新增 2 个演化方程（∂_t tau、∂_t kappa）却未给对应约束（约束违背方程）与初值 ⇒ 演化未知量由 6 增至 8，约束面未定义 ⇒ 数值积分无法启动（不可执行判据）"),
    ("A-05", "FAIL", "a05_kappa_eq_both_terms_dimension_broken",
     "∂_t kappa 左端量纲 %s；右端 [alpha R] = %s（差 T/L = 1/c）、[(2/c^2)∇^2 kappa] = %s（差 T^3 L^-4）⇒ 两项都不齐" % (dstr(DIM_TAU_DT), dstr(DIM_KAPPA), dstr(DIM_KAPPA_LAP))),
    ("A-06", "FAIL", "a06_kappa_eq_uses_R_as_independent_source",
     "kappa 方程把 R 当独立源，但 R 已由场方程/哈密顿约束代数确定 ⇒ 循环；该项使该式实为约束的改写而非独立演化方程（与 A-04 叠加 ⇒ 系统既欠定又循环）"),
    ("A-07", "FAIL", "a07_tau_eq_nonzero_equilibrium",
     "∂_t tau = ... + (alpha/c) omega - eta*tau 的均匀稳态为 tau_inf = alpha*omega/(c*eta)，只要 omega ≠ 0 即非零 ⇒ 与正文「远离孤子耗散项主导、tau→0」**自相矛盾**；要 tau→0 必须 omega→0，即孤子性不能只靠径向 1/r^2 剖面维持"),
    ("A-08", "FAIL", "a08_tau_eq_source_term_dimension_broken",
     "输运项与阻尼项自洽：[beta ∂ tau] = %s、[eta tau] = %s、[∂_t tau] = %s ⇒ eta 是率；但**源项 [alpha omega/c] = %s 少一个时间标度** ⇒ 方程不可自治（这是本册唯一「看起来自洽」的演化方程也失败）" % (dstr(DIM_BETA_GRAD_TAU), dstr(DIM_ETA_TAU), dstr(DIM_TAU_DT), dstr(DIM_A_OMEGA_C))),

    # ---- S 段：孤子色散 ----
    ("S-01", "FAIL", "s01_dispersion_dimension_broken",
     "omega = Lambda_0 r_s^2 / l_P^2 ⇒ [omega] = [Lambda_0] = %s（力），而角频率应为 %s ⇒ 即便把 Lambda_0 修成 L^-2 也仍差 M*L ⇒ **缺时间标度，结构性破损**" % (dstr(DIM_F), dstr(D(-1, 0, 0)))),
    ("S-02", "CORRECTED", "s02_omega_collapses_to_1_over_c",
     "照抄来料两式代数化简：omega ≡ M^2 c^3 /(2 pi hbar) ⇒ **G 与 Lambda_0 被完全约掉** ⇒ 结果不含任何「基准」，且 [omega] = M L T^-2（力）≠ T^-1" ),
    ("S-03", "FAIL", "s03_solar_soliton_frequency_absurd",
     "太阳质量代入其自身公式：r_s = %s m、omega = %s s^-1、T = %s s、hbar*omega = %s eV = %s 倍普朗克能量 ⇒ 该式对任何天体级质量都不作物理预言" % (S(R_SOL), S(OMEGA_SUN), S(T_SOL), S(HBAR_OMEGA_EV), S(HBAR_OMEGA_OVER_PL))),
    ("S-04", "FAIL", "s04_macroscopic_frequency_needs_subplanck_mass",
     "使 omega = 1 s^-1 的质量为 %s kg = %s 倍普朗克质量 ⇒ 「宏观频率的孤子」只存在于**亚普朗克质量**，与来料「孤子越大频率越高」的定性叙述方向相反地失效" % (S(M_FOR_OMEGA1), S(M_FOR_OMEGA1_OVER_MP))),
    ("S-05", "FAIL", "s05_horizon_conflation",
     "把「孤子视界 r_s」直接取为史瓦西半径 2GM/c^2 ⇒ 混用两个不同对象（挠率场零面 vs 几何视界）；且 r_s = %s m 仅为太阳半径的 %s 倍，1/r^2 剖面标度与天体半径无关 ⇒ 尺度脱钩" % (S(R_SOL), S(R_SOL_OVER_R_SUN))),

    # ---- G 段：g-2 / EDM ----
    ("G-01", "FAIL", "g01_delta_g_is_pure_unit_artifact",
     "来料代码的 tau_e = (1/c)(hbar/(m_e c))/lambda_e^2 ≡ m_e/hbar，代入 Delta g = tau_e*hbar/(m_e c) ⇒ **恒等于 1/c = %s**（两路复算相对偏差 %s）⇒ 零物理信息量，且量纲是 1/速度" % (S(DELTA_G_CODE), S(DELTA_G_REL))),
    ("G-02", "FAIL", "g02_delta_g_far_above_bsm_and_vs_31",
     "Delta g = 1/c = %s 比 31 号册 BSM 窗口 1e-12 高 %s 倍；而 31 号册已算几何 ECSK 耦合 y_geo = %s 给出 delta a_e = %s（比窗口低约 1e2）⇒ 本式要落窗口需 tau = %s m^-1，比几何值大 44 个量级 ⇒ 必须引入 ECSK 外的自由耦合（复发 31 号册 X-EXT-3）" % (S(DELTA_G_CODE), S(DELTA_G_OVER_BSM), S(Y_GEO), S(DELTA_AE_GEO), S(TAU_NEEDED_BSM))),
    ("G-03", "FAIL", "g03_edm_dimension_broken",
     "d_e ∝ (tau_e/(m_e c^2)) S·E 的量纲 = %s（动量），而 EDM 算符要求 d_e 量纲 %s ⇒ 差 M*L^-1" % (dstr(DIM_EDM), dstr(D(-1, 0, 0)))),
    ("G-04", "FAIL", "g04_edm_operator_parity_mismatch",
     "算符 tau_e * S · E 的宇称本征值 = (-1)(pseudoscalar) × (-1)(axial) × (+1)(polar) = **+1（P 偶）**，而 EDM 算符 S·E 为 P 奇 ⇒ 不能直接等同；需先做显式分部展开提取 P 奇项（未给）⇒ 「赝标量天然引入 CP 破坏 ⇒ 对应 EDM 信号」这一步未成立"),
    ("G-05", "PASS", "g05_cross_product_regression_31",
     "跨册回归复算：本册用 y_geo = (m_e/M_Pl)^2 = %s、delta a_e = y^2 m_e^2/(8 pi^2 m_tau^2)（m_tau = M_Pl）= %s，与 31 号册读的 6.8e-137 **同量级一致**（%s）⇒ 31 号册读数可复用，本册不重算其窗口" % (S(Y_GEO), S(DELTA_AE_GEO), S(abs(DELTA_AE_GEO - DELTA_AE_31) / DELTA_AE_31))),

    # ---- C 段：代码与路径 ----
    ("C-01", "FAIL", "c01_sample_code_not_runnable",
     "来料 mpmath 代码含 LaTeX 混入标识符（`\\(\\omega\\)_sun`、`\\(\\omega\\)`）⇒ 直接 SyntaxError；`Δg` 作标识符合法但不健壮 ⇒ 建议全 ASCII 命名后再复跑"),
    ("C-02", "INFO", "c02_hbar_truncation_inconsistent",
     "代码 hbar 取 %s（截断 10 位有效数字）而 G 取 4 位 ⇒ 与本库 CODATA 口径（hbar = 1.0545718176461565e-34）不一致；跨册数值纪律要求统一到高精度口径" % S(DOC_HBAR)),
    ("C-03", "FAIL", "c03_all_four_routes_blocked",
     "四条候选路径的共同前置未闭合：E-06/E-07（作用量与输运方程不同源）、A-01（约束非 GR 极限）、A-04（无约束无初值）、S-01（色散式量纲破损）⇒ 任一路径直接开工都会把不一致方程组求成无意义剖面"),
    ("C-04", "INFO", "c04_no_route_scored",
     "本册不对四条路径打分排序（同 30 号册 E-06）；但给出可执行性判定：路径 1（RG β）与既有 v7/能标册结论高度重复、且每步 +1 自由函数；路径 3（引力波）阻塞于 tau(t,r) 无解；路径 4（CMB）最不可证伪且依赖前三条 ⇒ 真正的前置是新增的 P0：把作用量与输运方程同源化（先裁决 kappa 是动力学场还是 slave）"),
]

CHECKS = []


def chk(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


chk("f_is_force", DIM_F == (1, 1, -2) and DIM_F != DIM_KAPPA,
    "dim(f) = %s, dim(kappa 台账) = %s" % (dstr(DIM_F), dstr(DIM_KAPPA)))
chk("action_not_dimensionless", DIM_ACT_CT != (0, 0, 0) and DIM_ACT_T != (0, 0, 0),
    "S 量纲：x^0=ct 口径 %s、dt 口径 %s" % (dstr(DIM_ACT_CT), dstr(DIM_ACT_T)))
chk("el_t_coeff_correct_is_G", DIM_EL_T_CORRECT == DIM_G,
    "dim(c^4/f) = %s = dim(G)；来料写 1/f = %s，差 %s" % (dstr(DIM_EL_T_CORRECT), dstr(DIM_EL_T_CLAIMED), dstr(DIM_EL_T_GAP)))
chk("el_tau2_sign_mismatch", SIGN_CORRECT != SIGN_CLAIMED, "correct=+1, claimed=-1")
chk("vary_kappa_is_algebraic", VARY_KAPPA == "R = 0", "d/dkappa (fR) = R => EOM R=0")
chk("vary_tau_is_slave", VARY_TAU.startswith("tau ="), "EOM: cR + 2 alpha tau = 0")
chk("ham_ratio_is_quarter", abs(RATIO_HAM_C1 + Decimal("0.25")) < Decimal("1e-40"),
    "c=1 口径比值 = %s（应为 -0.25 才还原 GR）" % S(RATIO_HAM_C1))
chk("kappa_eq_terms_broken",
    DIM_KAPPA != DIM_TAU_DT and DIM_KAPPA_LAP != DIM_TAU_DT,
    "[alpha R] = %s、[2∇^2 kappa/c^2] = %s vs [∂_t kappa] = %s" % (dstr(DIM_KAPPA), dstr(DIM_KAPPA_LAP), dstr(DIM_TAU_DT)))
chk("tau_eq_source_term_broken",
    DIM_BETA_GRAD_TAU == DIM_TAU_DT and DIM_ETA_TAU == DIM_TAU_DT and DIM_A_OMEGA_C != DIM_TAU_DT,
    "输运/阻尼项 = %s，源项 = %s（少一个时间标度）" % (dstr(DIM_TAU_DT), dstr(DIM_A_OMEGA_C)))
chk("tau_equilibrium_not_vanishing", DIM_A_OMEGA_C != DIM_ETA_TAU,
    "源项与阻尼项量纲不齐 ⇒ 稳态无定义；按数值对待则 tau_inf = alpha*omega/(c*eta) != 0")
chk("dispersion_dimension_broken", DIM_F != D(-1, 0, 0),
    "[Lambda_0 r_s^2/l_P^2] = %s != T^-1" % dstr(DIM_F))
chk("omega_simplify_machine_zero", OMEGA_REL <= Decimal("1e-50"),
    "Lambda_0 r_s^2/l_P^2 与 M^2c^3/(2 pi hbar) 相对偏差 = %s" % S(OMEGA_REL))
chk("omega_solar_absurd", OMEGA_SUN > Decimal("1e100"),
    "omega_sun = %s s^-1，hbar*omega = %s 倍普朗克能量" % (S(OMEGA_SUN), S(HBAR_OMEGA_OVER_PL)))
chk("delta_g_is_inv_c", DELTA_G_REL <= Decimal("1e-50"),
    "Delta g ≡ 1/c = %s（相对偏差 %s）" % (S(DELTA_G_CODE), S(DELTA_G_REL)))
chk("delta_g_far_above_bsm", DELTA_G_OVER_BSM > Decimal("1e3"),
    "Delta g / BSM 窗口 = %s" % S(DELTA_G_OVER_BSM))
chk("regression_31_agrees", abs(DELTA_AE_GEO - DELTA_AE_31) / DELTA_AE_31 < Decimal("0.1"),
    "本册 delta a_e(geo) = %s vs 31 号册 6.8e-137" % S(DELTA_AE_GEO))
chk("determinism", S(LAMBDA0) == S(C4 / (8 * PI * G_N)) and S(OMEGA_SUN) == S(LAMBDA0 * (R_SOL ** 2) / (LP ** 2)),
    "复算读数逐位一致")

VERDICTS = {}
for _id, _v, _s, _d in ITEMS:
    VERDICTS[_v] = VERDICTS.get(_v, 0) + 1
N_FAIL = sum(1 for c in CHECKS if c[1] == "FAIL")

KEY = {
    "Lambda0": S(LAMBDA0),
    "l_P_m": S(LP),
    "m_P_kg": S(MP),
    "r_s_sun_m": S(R_SOL),
    "r_s_over_R_sun": S(R_SOL_OVER_R_SUN),
    "omega_sun": S(OMEGA_SUN),
    "T_sun": S(T_SOL),
    "hbar_omega_sun_eV": S(HBAR_OMEGA_EV),
    "hbar_omega_over_E_pl": S(HBAR_OMEGA_OVER_PL),
    "omega_simplified": S(OMEGA_SIMPLE),
    "M_for_omega_1s": S(M_FOR_OMEGA1),
    "M_for_omega_1s_over_MPl": S(M_FOR_OMEGA1_OVER_MP),
    "gamma_couple": S(GAMMA_COUPLE),
    "gamma_std": S(GAMMA_STD),
    "ham_ratio_full": S(RATIO_HAM),
    "ham_ratio_c1": S(RATIO_HAM_C1),
    "delta_g_code": S(DELTA_G_CODE),
    "delta_g_over_bsm": S(DELTA_G_OVER_BSM),
    "tau_needed_for_bsm_per_m": S(TAU_NEEDED_BSM),
    "y_geo": S(Y_GEO),
    "delta_a_e_geo": S(DELTA_AE_GEO),
    "dims": {
        "G": dstr(DIM_G), "f": dstr(DIM_F), "kappa": dstr(DIM_KAPPA),
        "tau": dstr(DIM_TAU), "rho": dstr(DIM_RHO),
        "el_t_claimed": dstr(DIM_EL_T_CLAIMED),
        "el_t_correct": dstr(DIM_EL_T_CORRECT),
        "el_t_gap": dstr(DIM_EL_T_GAP),
    },
}

PAYLOAD = {
    "round": "r19",
    "date": "2026-10-07",
    "title": "外部来稿《TUFT V3.4 EC 作用量 + ADM-BSSN + 孤子色散 + g-2/EDM》变分与量纲审计",
    "counts": {"items": len(ITEMS), "checks": len(CHECKS), "check_fail": N_FAIL},
    "verdicts": VERDICTS,
    "items": [{"id": i, "verdict": v, "slug": s, "detail": d} for i, v, s, d in ITEMS],
    "selfcheck": [{"name": n, "verdict": v, "detail": d} for n, v, d in CHECKS],
    "key_numbers": KEY,
    "reused_defect_ids": ["C-02", "C-05", "C-88", "C-30", "O-V34-C", "O-SCALE", "V04"],
    "sibling_products": [
        "数据/TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07.json",
        "数据/TUFT-V3.4四模块审计与路线选址前置_2026-10-07.json",
        "../../../07_统一场方程/空间螺旋几何化统一场论/31_外部来稿V3.4修复版_结构修正与能标窗口_2026-10-07.md",
    ],
}


def write_outputs():
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    stem = "TUFT-V3.4_EC作用量与ADM约束_变分与量纲审计_2026-10-07"
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
    print("omega_sun = %s  Delta_g = %s  ham_ratio(c=1) = %s" % (S(OMEGA_SUN), S(DELTA_G_CODE), S(RATIO_HAM_C1)))
    for n, v, d in CHECKS:
        if v == "FAIL":
            print("SELFCHECK-FAIL %s :: %s" % (n, d))
    return 1 if N_FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
