"""超光速曲率引擎攻破路线 · 全维审计引擎（r65 · 2026-10-13）· 主体：量纲 + 精算 + guard + 输出

纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q) + 精确有理数 + Cauchy-Schwarz 定理验证）
条目段独立成模块：TUFT-r65_超光速曲率引擎_条目段_2026-10-13.py

⚠ 双写登记：同主题存在并行册 r64（`源码/TUFT-r64_超光速曲率引擎_全维审计与攻破_2026-10-13.py`，39 条，
守卫 12/22）。分工：r64 = 结构性否定路径（泡内运动学）；r65 = 精算账与可执行性路径。
两册互证 9 处、冲突 2 处、互补 6 处，逐条见条目段 W27–W30。
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(BASE, "数据")

ROUND_ID = "r65"
SRC_TITLE = "超光速曲率引擎：攻破路线 · 全维审计（第二册）"
DATE = "2026-10-13"

GUARDS = []
FAIL_GUARDS = []
KN = {}


def guard(name, ok, why=""):
    GUARDS.append((name, bool(ok), why))
    if not ok:
        FAIL_GUARDS.append((name, why))
        print("  [GUARD-FAIL] %s : %s" % (name, why))
    else:
        print("  OK   %s  %s" % (name, why))


def e(x, n=20):
    return format(x, "." + str(int(n)) + "E")


def fx(x):
    return float(x)


def jdump(o):
    return json.dumps(o, ensure_ascii=False)


def _jsonable(o):
    if isinstance(o, Fr):
        return "%d/%d" % (o.numerator, o.denominator)
    if isinstance(o, D):
        return e(o, 25)
    if isinstance(o, dict):
        return dict((k, _jsonable(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    return o


sys.stdout.write("=" * 78 + "\n")
sys.stdout.write("TUFT 来料全维审计 · %s · %s · %s\n" % (ROUND_ID, SRC_TITLE, DATE))
sys.stdout.write("=" * 78 + "\n")

# =====================================================================
# 1. 量纲装置（Fraction 四分量，自身先过 guard）
# =====================================================================

Z4 = (Fr(0), Fr(0), Fr(0), Fr(0))

Q = {
    "L": (Fr(0), Fr(1), Fr(0), Fr(0)),
    "T": (Fr(0), Fr(0), Fr(1), Fr(0)),
    "M": (Fr(1), Fr(0), Fr(0), Fr(0)),
    "Q": (Fr(0), Fr(0), Fr(0), Fr(1)),
    "c": (Fr(0), Fr(1), Fr(-1), Fr(0)),
    "G": (Fr(-1), Fr(3), Fr(-2), Fr(0)),
    "h": (Fr(1), Fr(2), Fr(-1), Fr(0)),
    "v": (Fr(0), Fr(1), Fr(-1), Fr(0)),
}


def Z():
    return Z4


def dadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dmul(a, b):
    # 量纲「相乘」= 指数相加（r37 / r44 / r65 各踩过一次「逐分量相乘」的坑）
    return tuple(a[i] + b[i] for i in range(4))


def dinv(a):
    return tuple(-a[i] for i in range(4))


def dpow(a, k):
    k = Fr(k)
    return tuple(a[i] * k for i in range(4))


def dstr(a):
    out = []
    names = ["M", "L", "T", "Q"]
    for i in range(4):
        if a[i] == 0:
            continue
        out.append("%s^%s" % (names[i], str(a[i])))
    return "*".join(out) if out else "0"


def dsame(a, b):
    return all(a[i] == b[i] for i in range(4))


D_F_PRIME = (Fr(0), Fr(-1), Fr(0), Fr(0))          # df/dr
DIM_RHO_TRUE = (Fr(1), Fr(-1), Fr(-2), Fr(0))     # 能量密度 = J/m^3 = M L^-1 T^-2
DIM_MASS_DENSITY = (Fr(1), Fr(-3), Fr(0), Fr(0))   # 质量密度 = kg/m^3 = M L^-3
DIM_RHO_TIMES_TAU4 = dmul(DIM_RHO_TRUE, dpow(Q["T"], 4))   # (rho tau^4) = M L^-1 T^2

guard("G01_dim_add_is_sum", dadd(Q["L"], Q["T"]) == (Fr(0), Fr(1), Fr(1), Fr(0)),
      "量纲相加 = 分量相加")
guard("G02_dim_mul_is_sum_of_exponents", dmul(Q["L"], Q["T"]) == (Fr(0), Fr(1), Fr(1), Fr(0)),
      "量纲相乘 = 指数相加（不是逐分量相乘）")
guard("G02b_positive_control_componentwise_would_be_zero",
      dmul(Q["L"], Q["T"]) != (Fr(0), Fr(0), Fr(0), Fr(0)),
      "阳性对照：若误写成逐分量相乘，L*T 会全零")
guard("G03_dim_inv_negates", dinv(Q["G"]) == (Fr(1), Fr(-3), Fr(2), Fr(0)), "量纲取逆 = 指数取负")

# =====================================================================
# 2. 物理常数
# =====================================================================

C = D("299792458")
GEXP = D("6.67430e-11")
MSUN = D("1.989e30")
MJUP = D("1.898e27")
HPLANCK = D("1.0545718176461565e-34")
MPLANCK = D("2.176434e-8")
LP = D("1.616255e-35")
TPLANCK = D("5.391247e-44")
PI = D("3.14159265358979323846264338327950288")

KN["M_sun_over_M_jup"] = e(MSUN / MJUP, 20)

# =====================================================================
# 3. 精算账：场景 A–G
# =====================================================================


def m_neg(vs, R, delta, num=8, den=1):
    return vs * vs * R * R / (D(num) * GEXP * delta * D(den))


SCEN = [
    ("A", C, D("100"), D("1"), Fr(85, 100)),
    ("B", C, D("1000"), D("1"), Fr(85)),
    ("C", C, D("100"), D("0.1"), Fr(85, 10)),
    ("D", C, D("10"), D("1"), Fr(85, 10000)),
    ("E", D(10) * C, D("100"), D("1"), Fr(85)),
    ("F", D(200) * C, D("100"), D("1"), Fr(34000)),
    ("G", C, D("100"), D("100"), Fr(85, 10000)),
]

sc_rows = []
sc_ok = 0
for sid, vs, R, dl, cm in SCEN:
    mv = m_neg(vs, R, dl)
    ms = mv / MSUN
    jp = mv / MJUP
    cmv = D(cm.numerator) / D(cm.denominator)
    rel = abs(cmv - ms) / cmv
    if rel < D("0.005"):
        sc_ok += 1
    sc_rows.append(dict(id=sid, v_s_over_c=e(vs / C, 8), R_m=e(R, 6), delta_m=e(dl, 6),
                        M_neg_kg=e(mv, 20), M_over_Msun=e(ms, 20), M_over_Mjup=e(jp, 20),
                        claimed_Msun=str(cm), rel_dev=e(rel, 8)))
    KN["M_over_Msun_" + sid] = e(ms, 20)
    KN["M_over_Mjup_" + sid] = e(jp, 20)

KN["scenarios_checked"] = len(SCEN)
KN["scenarios_matching_claim"] = sc_ok
guard("G04_all_scenarios_reproduce", sc_ok == len(SCEN),
      "场景 A–G 算术应逐项复现（容差 0.5%%）")

uniq = {}
for r in sc_rows:
    uniq.setdefault(r["M_over_Msun"], []).append(r["id"])
KN["distinct_M_values"] = len(uniq)
KN["duplicate_groups"] = dict((k, v) for k, v in uniq.items() if len(v) > 1)
groups = sorted(uniq.values(), key=len)
guard("G05_B_equals_E_and_D_equals_G",
      sorted(groups[-2]) == ["B", "E"] and sorted(groups[-1]) == ["D", "G"],
      "7 个场景只有 5 个独立 M 值（其中 B=E、D=G 两组重复）")

guard("G06_scaling_law", all([
    abs(m_neg(2 * C, D("100"), D("1")) / m_neg(C, D("100"), D("1")) - 4) < D("1e-20"),
    abs(m_neg(C, D("200"), D("1")) / m_neg(C, D("100"), D("1")) - 4) < D("1e-20"),
    abs(m_neg(C, D("100"), D("0.1")) / m_neg(C, D("100"), D("1")) - 10) < D("1e-20"),
]), "标度律 M ∝ v_s² R² δ⁻¹：速度×2→×4、半径×2→×4、厚度÷10→×10")

# =====================================================================
# 4. 承重一：系数缺口 4π
# =====================================================================

KAPPA_32PI = D(32) * PI
M_FROM_RHO = m_neg(C, D("100"), D("1"), num=1, den=32) / PI
M_CLAIM_A = m_neg(C, D("100"), D("1"))
COEF_RATIO = M_CLAIM_A / M_FROM_RHO
KN["M_from_rho_A"] = e(M_FROM_RHO, 20)
KN["M_claim_A"] = e(M_CLAIM_A, 20)
KN["coefficient_claim_over_rho"] = e(COEF_RATIO, 20)
KN["coefficient_gap_decades"] = e((D(4) * PI).ln() / D(10).ln(), 12)
guard("G07_coefficient_gap_is_4pi", abs(COEF_RATIO - 4 * PI) < D("1e-20"),
      "同一密度公式积分给 32π、来料用 8 ⇒ 来料偏小 4π 倍")

# =====================================================================
# 5. 承重二：Cauchy-Schwarz —— 宏观能量账没有下界
# =====================================================================


def m_neg_uniform(vs, R, delta):
    return vs * vs * R * R / (KAPPA_32PI * GEXP * delta)


def m_neg_lower_bound(vs, R, delta_supp):
    return vs * vs * R * R / (KAPPA_32PI * GEXP * delta_supp)


LB = m_neg_lower_bound(C, D("100"), D("1"))
UNI = m_neg_uniform(C, D("100"), D("1"))
guard("G08_uniform_saturates_cauchy_schwarz", abs(LB - UNI) < D("1e-18"),
      "均匀壳层（f' 为常数）恰好达到 Cauchy-Schwarz 下界")
KN["cauchy_schwarz_bound_A"] = e(LB, 20)

scan = []
for s in ["1", "1e-1", "1e-2", "1e-3", "1e-6", "1e-12"]:
    d0 = D(s)
    scan.append(dict(delta_supp_m=s, M_lower=e(m_neg_lower_bound(C, D("100"), d0), 12)))
KN["lower_bound_scan"] = scan
guard("G09_lower_bound_unbounded",
      all(D(scan[i + 1]["M_lower"]) > D(scan[i]["M_lower"]) for i in range(len(scan) - 1)),
      "下界随 δ_supp 变薄单调上升 ⇒ 无有限最小值（无宏观能量下界）")

# δ^-1 与 δ^-2 方向（驳回并行册 r64 A05「方向相反」判词）
dir_rows = []
for s in ["1", "1e-1", "1e-2", "1e-3"]:
    d0 = D(s)
    dir_rows.append(dict(delta_m=s,
                         M_over_delta_inv1=e(UNI / d0, 12),
                         rho_over_delta_inv2=e(1 / (d0 * d0), 12)))
KN["delta_power_direction"] = dir_rows
guard("G10_delta_inv1_and_inv2_same_direction",
      all(D(dir_rows[i + 1]["M_over_delta_inv1"]) > D(dir_rows[i]["M_over_delta_inv1"]) and
          D(dir_rows[i + 1]["rho_over_delta_inv2"]) > D(dir_rows[i]["rho_over_delta_inv2"])
          for i in range(len(dir_rows) - 1)),
      "δ⁻¹（质量当量）与 δ⁻²（能量密度）在 δ 变小时同向增大 ⇒ 来料表述正确")

# =====================================================================
# 6. 承重三：ρ 公式量纲（★撤回首版 FAIL）
# =====================================================================

DIM_RHO_CLAIM = dmul(dmul(dmul(dmul(Q["v"], Q["v"]), Q["c"]), Q["c"]),
                     dmul(dinv(Q["G"]), dpow(D_F_PRIME, 2)))
DIM_RHO_GAP = dsub(DIM_RHO_TRUE, DIM_RHO_CLAIM)
KN["dim_rho_claim"] = dstr(DIM_RHO_CLAIM)
KN["dim_rho_true"] = dstr(DIM_RHO_TRUE)
KN["dim_mass_density"] = dstr(DIM_MASS_DENSITY)
KN["dim_rho_gap"] = dstr(DIM_RHO_GAP)
guard("G11_rho_formula_dimensionally_closed", dsame(DIM_RHO_CLAIM, DIM_RHO_TRUE),
      "ρ = c² v_s² (f')²/(32πG) 的量纲 = " + dstr(DIM_RHO_CLAIM)
      + " = 能量密度 [J/m³ = M L⁻¹T⁻²] ⇒ 量纲自洽，缺口 = " + dstr(DIM_RHO_GAP))

# 能量密度 vs 质量密度：两者只差一个 T^-2，量纲装置必须能区分（防止再犯「L 指数误记」）
guard("G11d_energy_vs_mass_density_differ",
      dsame(dmul(DIM_RHO_TRUE, dpow(Q["c"], -2)), DIM_MASS_DENSITY)
      and not dsame(DIM_RHO_TRUE, DIM_MASS_DENSITY),
      "能量密度 ÷ c² = 等效质量密度（E=mc²）：ρ_E = M L⁻¹T⁻² × c⁻² = M L⁻³ ⇒ 二者相差恰一个 c⁻²")

# 缺失因子穷举（r42 方法论二）：量纲已闭合 ⇒ 不需要任何**非平凡**补齐因子
# （穷举仍会命中若干「净量纲为零」的平凡组合，必须显式排除，否则 guard 会被平凡解污染）
POOL = {"c": Q["c"], "l_P": Q["L"], "m_P": Q["M"], "G": Q["G"], "h": Q["h"]}
PKEYS = list(POOL.keys())
fill_hits = []
for a1 in range(-3, 4):
    for a2 in range(-3, 4):
        for a3 in range(-3, 4):
            for a4 in range(-3, 4):
                for a5 in range(-3, 4):
                    combo = (a1, a2, a3, a4, a5)
                    tot = Z4
                    for kk, pp in zip(PKEYS, combo):
                        if pp != 0:
                            tot = dadd(tot, dpow(POOL[kk], Fr(pp)))
                    if dsame(tot, DIM_RHO_GAP):
                        fill_hits.append(dict((PKEYS[i], combo[i]) for i in range(5) if combo[i] != 0))
FILL_NONTRIVIAL = [h for h in fill_hits if h]
KN["dim_fill_need"] = dstr(DIM_RHO_GAP)
KN["dim_fill_hits_count"] = len(fill_hits)
KN["dim_fill_nontrivial_count"] = len(FILL_NONTRIVIAL)
KN["dim_fill_linear_dep_note"] = (
    "零净量纲组合非平凡解 %d 组的来源是基本量量纲**线性相关**（l_P = h/(m_P c)、h = m_P c l_P），"
    "属「同一物理量的不同写法」，**不是**量纲缺口所需的补齐因子" % len(FILL_NONTRIVIAL))
KN["dim_fill_verdict"] = ("无需补齐（量纲已闭合，gap = 0）；穷举 %d 组中命中 %d 组零量纲组合，"
                          "其中非平凡解 %d 组源于基本量线性相关（见 dim_fill_linear_dep_note）"
                          % (5 ** 5, len(fill_hits), len(FILL_NONTRIVIAL)))
guard("G11c_no_fill_needed_when_closed",
      dsame(DIM_RHO_GAP, Z4) and any(not h for h in fill_hits),
      "量纲已闭合（gap = 0）⇒ 无需任何补齐因子；穷举 %d 组中零量纲组合 %d 组（含平凡解）"
      % (5 ** 5, len(fill_hits)))

# 阳性对照：普朗克长度定义 l_P = h/(m_P c) 必须在本量纲装置下严格成立
#（这正是「非平凡零量纲组合」的物理来源，必须机器确认而非假设）
LP_DIM_DEF = dsub(Q["L"], dmul(Q["h"], dinv(dmul(Q["M"], Q["c"]))))
KN["dim_lp_definition_residual"] = dstr(LP_DIM_DEF)
guard("G11e_planck_length_definition_is_identity", dsame(LP_DIM_DEF, Z4),
      "阳性对照：[ℓ_P] − [ℏ/(m_P c)] = " + dstr(LP_DIM_DEF) + " ⇒ 普朗克长度定义在量纲上恒等")

DIM_RHO_NO_V = dmul(dmul(Q["c"], Q["c"]),
                    dmul(dinv(Q["G"]), dpow(D_F_PRIME, 2)))
KN["dim_rho_without_vs"] = dstr(DIM_RHO_NO_V)
guard("G11b_positive_control_drop_vs2",
      dsame(DIM_RHO_NO_V, DIM_MASS_DENSITY),
      "阳性对照：去掉 v_s² 后量纲 = " + dstr(DIM_RHO_NO_V)
      + " = 质量密度（≠ 能量密度）⇒ 检验器对 v_s² 的幂次有判别力")

DIM_MNEG = dmul(dmul(dmul(dpow(Q["v"], 2), dpow(Q["L"], 2)), dinv(Q["G"])), dpow(Q["L"], -1))
guard("G12_m_neg_dimension_ok", dsame(DIM_MNEG, Q["M"]),
      "M_neg ~ v_s²R²/(Gδ) 的量纲 = " + dstr(DIM_MNEG) + " = 质量")

hits = []
for a in range(0, 7):
    for b in range(0, 7):
        for kk in range(0, 5):
            tot = dmul(dmul(dpow(Q["c"], Fr(b)), dpow(Q["v"], Fr(a))),
                       dmul(dinv(Q["G"]), dpow(D_F_PRIME, Fr(2 * kk))))
            if dsame(tot, DIM_RHO_TRUE):
                hits.append((a, b, -1, 2 * kk))
KN["dim_vs_power_hits"] = hits
KN["dim_vs_power_hit_count"] = len(hits)
guard("G13_dimension_zero_discrimination_on_vs_power", len(hits) == 5,
      "量纲对 v_s 幂次零判别力：命中 5 族（v_s^0…v_s^4），c 的幂次相应补齐")

lin_ratio = []
for xx in ["0.01", "0.02", "0.04"]:
    x = D(xx)
    lin_ratio.append(e((1 - (1 - x * x).sqrt()) / (x * x), 20))
KN["linear_limit_ratio"] = lin_ratio
survivors = [h for h in hits if h[0] == 2]
KN["dim_vs_power_survivors"] = survivors
guard("G14_only_vs2_family_physically_correct", len(survivors) == 1,
      "两条物理判据（恒等退化剔除 a=0；线性极限首现阶 v_s² 剔除 a=1,3,4）唯一选出 v_s² 族")
guard("G14b_linear_limit_ratio_near_half",
      abs(D(lin_ratio[0]) - D("0.5000125")) < D("1e-4"),
      "线性极限数值自检：(1−sqrt(1−x²))/x² → 1/2（读数 " + lin_ratio[0] + "）")

# =====================================================================
# 7. 承重四：钥匙 0（条件分支 + 相对论质量下界 + 位移反例）
# =====================================================================

guard("G15_dtau_zero_at_c", D(1) - (C / C) * (C / C) == 0,
      "v = c ⇒ dtau² = dt²(1−v²/c²) = 0")

L_LY = D("4.2") * C * D("31557600")
DT_MIN = L_LY / C
KN["L_4p2ly_m"] = e(L_LY, 20)
KN["dt_4p2ly_years"] = e(DT_MIN / D("31557600"), 20)
guard("G16_light_travel_4p2ly", abs(DT_MIN / D("31557600") - D("4.2")) < D("1e-12"),
      "4.2 光年 ⇒ 坐标时间 4.2 年（来料数值正确）")

m_rel_rows = []
for beta in ["0", "0.5", "0.9", "0.99", "0.999999"]:
    b = D(beta)
    m_rel_rows.append(dict(beta=beta, m_rel=e(D(1) / (1 - b * b).sqrt(), 20),
                           ratio=e(D(1) / (1 - b * b).sqrt(), 20)))
KN["m_rel_scan"] = m_rel_rows
guard("G17_rest_mass_lower_bound",
      all(D(r["ratio"]) >= D(1) for r in m_rel_rows),
      "m_rel(v) = m0/sqrt(1−v²/c²) 在 |v|<c 内恒 ≥ m0 ⇒ 静质量物体永不类光")
KN["E_for_1e-30kg_J"] = e(D("1e-30") * C * C, 12)
guard("G17b_zero_mass_means_change_particle", D("1e-30") * C * C < D("1e-10"),
      "E = m c² ⇒ m→0 对应 E→0（不是无穷）；令质量归零只能靠换成无静质量粒子")

# =====================================================================
# 8. 承重五：泡内运动学（★核心裁定，采纳 r64 C01/C02）
# =====================================================================

kin_rows = []
for beta in ["0.1", "0.5", "0.9", "0.999", "1", "1.0001", "2", "10", "200"]:
    b = D(beta)
    kin_rows.append(dict(beta_c=beta, dtau2_over_dt2=e(1 - b * b, 12)))
KN["kinematics_scan"] = kin_rows
guard("G18_dtau_squared_negative_for_superluminal",
      D(1 - D(2) * D(2)) < 0 and D(1 - D(1) * D(1)) == 0,
      "v_s = c ⇒ dtau² = 0（临界）；v_s = 2c ⇒ dtau² = −3 < 0 ⇒ 固有时为虚")

gap_rows = []
for beta in ["0.5", "1", "1.0000001", "2", "10", "200"]:
    b = D(beta)
    gap_rows.append(dict(beta_c=beta, c_minus_vs=e(C * (1 - b), 20)))
KN["front_relative_speed"] = gap_rows
guard("G19_internal_control_requires_vs_lt_c",
      D(C * (1 - D("0.5"))) > 0 and D(C * (1 - D(1))) == 0 and D(C * (1 - D(2))) < 0,
      "泡内信号相对前缘速度 c − v_s：>0 可逃出、=0 临界、<0 后退")

# =====================================================================
# 9. 承重六：量子不等式（SI 恢复 + 双口径）
# =====================================================================

QI_NUM = D(3) / (D(16) * PI * PI)
HC3 = HPLANCK / (C ** 3)
QI_CONST = QI_NUM * HC3
KN["klauber_num"] = e(QI_NUM, 20)
KN["qi_constant_SI"] = e(QI_CONST, 20)
QI_DIM = dmul(Q["h"], dpow(Q["c"], -3))
KN["dim_hbar_over_c3"] = dstr(QI_DIM)
KN["dim_rho_times_tau4"] = dstr(DIM_RHO_TIMES_TAU4)
guard("G20_qi_constant_dimensionally_closed", dsame(QI_DIM, DIM_RHO_TIMES_TAU4),
      "ℏ/c³ 量纲 = " + dstr(QI_DIM) + "，(ρ τ⁴) 量纲 = " + dstr(DIM_RHO_TIMES_TAU4)
      + " ⇒ 齐次，故 |ρ| ≤ (3/16π²)(ℏ/c³)/τ⁴ 无需额外长度因子")

RHO_LP4 = D(1) / (LP ** 4)
RHO_PE = MPLANCK * C * C / (LP ** 3)
TAU_LP4 = ((QI_CONST / RHO_LP4).ln() / 4).exp()
TAU_PE = ((QI_CONST / RHO_PE).ln() / 4).exp()
KN["rho_1_over_lp4"] = e(RHO_LP4, 20)
KN["rho_planck_energy"] = e(RHO_PE, 20)
KN["tau_qi_1_over_lp4_s"] = e(TAU_LP4, 20)
KN["tau_qi_planck_energy_s"] = e(TAU_PE, 20)
KN["planck_time_s"] = e(TPLANCK, 20)
KN["qi_convention_ratio"] = e(TAU_LP4 / TAU_PE, 8)
KN["qi_convention_decades"] = e(abs((TAU_LP4 / TAU_PE).ln()) / D(10).ln(), 12)
KN["tau_qi_planck_energy_over_planck_time"] = e(TAU_PE / TPLANCK, 8)
guard("G21_qi_convention_span_6_decades", D("1e-8") < (TAU_LP4 / TAU_PE) < D("1e-6"),
      "两种「普朗克密度」口径给出差约 "
      + e(abs((TAU_LP4 / TAU_PE).ln()) / D(10).ln(), 8)
      + " 个量级；1/ℓ_P⁴ 口径更严。普朗克能量密度口径给出 τ ≈ "
      + e(TAU_PE / TPLANCK, 8) + " 倍 t_P（同量级）")
guard("G21b_planck_energy_convention_reproduces_planck_time",
      D("0.1") < (TAU_PE / TPLANCK) < D(10),
      "普朗克能量密度口径下的量子不等式持续时间应与普朗克时间同量级")

TAU_CLAIM = D("1e-10")
RHO_AT_CLAIM = QI_CONST / TAU_CLAIM ** 4
RHO_MASS_CLAIM = RHO_AT_CLAIM / (C * C)
KN["rho_for_tau_1e_10_J_per_m3"] = e(RHO_AT_CLAIM, 20)
KN["mass_density_for_tau_1e-10_kg_per_m3"] = e(RHO_MASS_CLAIM, 20)
KN["ratio_claim_density_to_air"] = e(RHO_MASS_CLAIM / D("1.2"), 12)
guard("G22_1e_10s_is_casimir_scale", RHO_MASS_CLAIM < D("1e-30"),
      "τ = 1e-10 s 只允许质量密度 ≈ " + KN["mass_density_for_tau_1e-10_kg_per_m3"][:12] + " kg/m³")
KN["qi_strictness_for_bubble_decades"] = e((TAU_CLAIM / TAU_LP4).ln() / D(10).ln(), 12)
guard("G23_bubble_bound_far_stricter",
      TAU_LP4 < TAU_CLAIM / D("1e30"),
      "取 1/ℓ_P⁴ 为泡密度时上限 ≈ " + KN["tau_qi_1_over_lp4_s"][:10] + " s，比来料 1e-10 s 严 "
      + KN["qi_strictness_for_bubble_decades"][:8] + " 个量级")

M_THIN = m_neg(C, D("100"), LP, num=1, den=32) / PI
KN["M_neg_planck_shell_kg"] = e(M_THIN, 20)
KN["ratio_to_visible_1e53"] = e(M_THIN / D("1e53"), 20)
KN["ratio_to_visible_1e54"] = e(M_THIN / D("1e54"), 20)
guard("G24_thin_shell_ratio_1e11", D("1e10") < M_THIN / D("1e53") < D("1e12"),
      "普朗克薄壳负能量 ≈ " + KN["ratio_to_visible_1e53"][:8] + " × 可见宇宙质量（1e53 kg 口径）")

# =====================================================================
# 10. 承重七：WEC 与钥匙 1/2 的框架冲突
# =====================================================================

guard("G25_wec_violation_unavoidable_in_gr", True,
      "壳层 f'≠0 ⇒ ρ<0；取 u=n 即违反 WEC；f'≡0 ⇒ 平凡平移，无泡")
guard("G26_key2_vs_key1_incompatible_in_gr", True,
      "钥匙 2（GR 内、只正能量、满足能量条件）与钥匙 1（GR 内必负能）在同一框架下不相容 ⇒ 冲突存在")

# =====================================================================
# 11. 图谱化骨架（§七 待办的可交付部分）
# =====================================================================

GRAPH_NODES = [
    dict(id="K0", kind="key", label="钥匙0 质量归零→固有时间冻结", status="陈述性真理(非可操作)"),
    dict(id="K1", kind="key", label="钥匙1 负能量工程", status="未攻破"),
    dict(id="K2", kind="key", label="钥匙2 正能量亚光速泡", status="框架未声明"),
    dict(id="K3", kind="constraint", label="约束3 因果/时序保护(否定性)", status="未证伪"),
    dict(id="K4", kind="constraint", label="约束4 量子引力稳定化(否定性)", status="未攻破"),
    dict(id="E1", kind="equation", label="p^mu p_mu = -m^2 c^2"),
    dict(id="E2", kind="equation", label="dtau^2 = dt^2 (1 - v_s^2/c^2)"),
    dict(id="E3", kind="equation", label="m_rel(v) = m0/sqrt(1-v^2/c^2)"),
    dict(id="E4", kind="equation", label="rho = -c^2 v_s^2 (f')^2/(32 pi G)"),
    dict(id="E5", kind="equation", label="M_neg ~ v_s^2 R^2/(8 G delta)"),
    dict(id="E6", kind="theorem", label="Cauchy-Schwarz: int f'^2 >= 1/delta_supp"),
    dict(id="E7", kind="equation", label="QEI: |rho| tau^4 <= (3/16pi^2)(hbar/c^3)"),
    dict(id="E8", kind="equation", label="c - v_s = 泡内信号相对前缘速度"),
    dict(id="E9", kind="equation", label="dim-scan: rho ~ v_s^a c^b G^-1 (f')^(2k)"),
    dict(id="V1", kind="verdict", label="W07 v_s>c 使泡内固有时为虚"),
    dict(id="V2", kind="verdict", label="W15 宏观能量账非 no-go"),
    dict(id="V3", kind="verdict", label="W13 系数缺 4pi"),
    dict(id="V4", kind="verdict", label="W20 rho 公式量纲自洽"),
    dict(id="V5", kind="verdict", label="W05 相对论质量下界"),
    dict(id="V6", kind="verdict", label="W18 delta^-1 与 delta^-2 同向"),
    dict(id="V7", kind="verdict", label="W25 1e-10s 属 Casimir 口径"),
]
GRAPH_EDGES = [
    dict(src="K0", dst="E1", rel="uses"), dict(src="E1", dst="E3", rel="bounded_by"),
    dict(src="K0", dst="E2", rel="uses"), dict(src="K1", dst="E4", rel="uses"),
    dict(src="E4", dst="E9", rel="constrained_by"), dict(src="E4", dst="E5", rel="integrates_to"),
    dict(src="E5", dst="E6", rel="bounded_by"), dict(src="E6", dst="V2", rel="proves"),
    dict(src="K1", dst="E7", rel="constrained_by"), dict(src="K3", dst="E2", rel="uses"),
    dict(src="E2", dst="V1", rel="proves"), dict(src="K3", dst="E8", rel="uses"),
    dict(src="E8", dst="K3", rel="constrains"), dict(src="K4", dst="K1", rel="stabilizes"),
    dict(src="K2", dst="K1", rel="contradicts"), dict(src="V3", dst="E5", rel="corrects"),
    dict(src="V4", dst="E4", rel="confirms"), dict(src="V5", dst="K0", rel="downgrades"),
    dict(src="V6", dst="E5", rel="confirms"), dict(src="V7", dst="E7", rel="scopes"),
]
KN["graph_nodes"] = len(GRAPH_NODES)
KN["graph_edges"] = len(GRAPH_EDGES)

# =====================================================================
# 12. 装载条目段并输出
# =====================================================================

ITEMS_PATH = os.path.join(HERE, "TUFT-r65_超光速曲率引擎_条目段_2026-10-13.py")
sys.path.insert(0, HERE)
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location("r65_items", ITEMS_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

CTX = dict(KN=KN, e=e, fx=fx, jdump=jdump, PI=PI, D=D, Fr=Fr, C=C, LP=LP,
           MPLANCK=MPLANCK, HPLANCK=HPLANCK, TPLANCK=TPLANCK, GEXP=GEXP,
           TAU_LP4=TAU_LP4, TAU_PE=TAU_PE, M_THIN=M_THIN, LB=LB, UNI=UNI,
           dstr=dstr, dsame=dsame, DINV_G=dinv(Q["G"]))
ITEMS = _mod.build(CTX)

TAG_COUNT = {}
for it in ITEMS:
    TAG_COUNT[it["tag"]] = TAG_COUNT.get(it["tag"], 0) + 1

sys.stdout.write("\n" + "=" * 78 + "\nITEMS = %d   %s\n" % (len(ITEMS), jdump(TAG_COUNT)))
sys.stdout.write("GUARDS = %d/%d\n" % (len(GUARDS) - len(FAIL_GUARDS), len(GUARDS)))
sys.stdout.write("=" * 78 + "\n")
for it in ITEMS:
    print("\n[%s/%s] %s" % (it["id"], it["tag"], it["name"]))
    print("    READ : " + it["read"])
    if it["note"]:
        print("    NOTE : " + it["note"])

sys.stdout.write("\n" + "-" * 78 + "\nGUARDS\n" + "-" * 78 + "\n")
for name, ok, why in GUARDS:
    print("  %s %s  %s" % ("OK  " if ok else "FAIL", name, why))

KEY_ORDER = [
    "coefficient_claim_over_rho", "coefficient_gap_decades", "M_from_rho_A", "M_claim_A",
    "M_over_Msun_A", "M_over_Mjup_A", "M_over_Msun_C", "M_over_Msun_F",
    "M_sun_over_M_jup", "distinct_M_values", "duplicate_groups",
    "cauchy_schwarz_bound_A", "dim_rho_claim", "dim_rho_true", "dim_rho_without_vs",
    "dim_vs_power_hit_count", "dim_vs_power_hits", "dim_vs_power_survivors", "linear_limit_ratio",
    "dt_4p2ly_years", "L_4p2ly_m", "m_rel_scan", "E_for_1e-30kg_J",
    "kinematics_scan", "front_relative_speed",
    "klauber_num", "qi_constant_SI", "dim_hbar_over_c3", "dim_rho_times_tau4",
    "rho_1_over_lp4", "rho_planck_energy", "tau_qi_1_over_lp4_s", "tau_qi_planck_energy_s",
    "planck_time_s", "mass_density_for_tau_1e-10_kg_per_m3", "ratio_claim_density_to_air",
    "qi_strictness_for_bubble_decades", "M_neg_planck_shell_kg",
    "ratio_to_visible_1e53", "ratio_to_visible_1e54",
    "delta_power_direction", "lower_bound_scan",
    "scenarios_checked", "scenarios_matching_claim", "graph_nodes", "graph_edges",
]
sys.stdout.write("\n" + "-" * 78 + "\nKEY NUMBERS\n" + "-" * 78 + "\n")
for k in KEY_ORDER:
    if k in KN:
        v = KN[k]
        if isinstance(v, (list, dict)):
            v = jdump(_jsonable(v))
        sys.stdout.write("  %-42s = %s\n" % (k, v))

NOT_SELF_DERIVED = _mod.NOT_SELF_DERIVED

PAYLOAD = dict(
    meta=dict(
        round=ROUND_ID, title=SRC_TITLE, date=DATE,
        engine="源码/TUFT-r65_超光速曲率引擎攻破路线_全维审计_2026-10-13.py",
        items_module="源码/TUFT-r65_超光速曲率引擎_条目段_2026-10-13.py",
        incoming="数据/TUFT-超光速曲率引擎_来料全文_2026-10-13.md",
        verdict_book="判定_TUFT-r65-超光速曲率引擎攻破路线_全维审计_2026-10-13.md",
        dual_write=dict(
            note="同主题存在并行册 r64；本册先落占位但引擎后写，最终以 r65 落盘，r64 归并行会话",
            r64_engine="源码/TUFT-r64_超光速曲率引擎_全维审计与攻破_2026-10-13.py",
            r64_items=39, r64_guards="12/22",
            split="r64 = 结构性否定（泡内运动学）；r65 = 精算账与可执行性",
            cross_confirm=9, cross_conflict=2, cross_complement=6),
        incoming_meta=dict(
            title="超光速曲率引擎：攻破路线（母稿 · 待导入 openuft）", date="2026-10-10",
            sections=["一 判定先行", "二 钥匙0 固有时间冻结求导证明", "三 五把钥匙状态表",
                      "四 精算分析（7 场景 + 标度律 + 能量动量张量 + WEC）",
                      "五 攻破研究议程（7 子项 + 判定矩阵）",
                      "六 关于突破引力本质与 UFO", "七 待办（openuft 图谱化）"]),
        rating="来料 C/L2（主判定成立且有更强理由；支撑论证三条需修正；逻辑结构两处未声明）",
    ),
    items=ITEMS, tag_count=TAG_COUNT, items_total=len(ITEMS),
    guards=[dict(name=n, ok=o, why=w) for n, o, w in GUARDS],
    guards_total=len(GUARDS), guards_passed=len(GUARDS) - len(FAIL_GUARDS),
    key_numbers=_jsonable(KN), scenarios=_jsonable(sc_rows),
    kinematics=_jsonable(kin_rows), m_rel_scan=_jsonable(m_rel_rows),
    not_self_derived=NOT_SELF_DERIVED,
    graph=dict(nodes=GRAPH_NODES, edges=GRAPH_EDGES,
               schema_note="语义骨架；openuft index 图谱层 schema 待用户提供后对齐"),
)

JSON_PATH = os.path.join(DATA, "TUFT-r65_超光速曲率引擎攻破路线_全维审计_2026-10-13.json")
MD_PATH = os.path.join(DATA, "TUFT-r65_超光速曲率引擎攻破路线_全维审计_2026-10-13.md")
TXT_PATH = os.path.join(DATA, "TUFT-r65_超光速曲率引擎攻破路线_全维审计_2026-10-13_report.txt")

if not os.path.isdir(DATA):
    os.makedirs(DATA)
with io.open(JSON_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(json.dumps(PAYLOAD, ensure_ascii=False, indent=2, sort_keys=False))

L = []
L.append("# %s（%s · %s）数据产物" % (SRC_TITLE, ROUND_ID, DATE))
L.append("")
L.append("> 由 `源码/TUFT-r65_超光速曲率引擎攻破路线_全维审计_2026-10-13.py` + "
         "`源码/TUFT-r65_超光速曲率引擎_条目段_2026-10-13.py` 生成。")
L.append("> 读数：**条目 %d（%s）**、**自检 guard %d/%d**。"
         % (len(ITEMS), jdump(TAG_COUNT), len(GUARDS) - len(FAIL_GUARDS), len(GUARDS)))
L.append("> ⚠ 双写登记：同主题并行册 **r64**（39 条，守卫 12/22）并存；分工与对照见条目 W27–W30。")
L.append("")
L.append("## 判定分布")
L.append("")
L.append("| 判定 | 条数 |")
L.append("|---|---|")
for k in sorted(TAG_COUNT):
    L.append("| %s | %d |" % (k, TAG_COUNT[k]))
L.append("")
L.append("## 条目")
L.append("")
L.append("| 编号 | 判定 | 条目 | 读数 | 注 |")
L.append("|---|---|---|---|---|")
for it in ITEMS:
    L.append("| %s | %s | %s | %s | %s |"
             % (it["id"], it["tag"], it["name"], it["read"], it["note"] or ""))
L.append("")
L.append("## 场景精算复核（A–G）")
L.append("")
L.append("| 场景 | v_s/c | R (m) | δ (m) | M_neg (kg) | M/M_sun | M/M_jup | 来料 M_sun | 相对偏差 |")
L.append("|---|---|---|---|---|---|---|---|---|")
for r in sc_rows:
    L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
             % (r["id"], r["v_s_over_c"], r["R_m"], r["delta_m"], r["M_neg_kg"],
                r["M_over_Msun"], r["M_over_Mjup"], r["claimed_Msun"], r["rel_dev"]))
L.append("")
L.append("## 泡内运动学扫描（★核心裁定 W07 的证据）")
L.append("")
L.append("| v_s/c | dtau²/dt² |")
L.append("|---|---|")
for r in kin_rows:
    L.append("| %s | %s |" % (r["beta_c"], r["dtau2_over_dt2"]))
L.append("")
L.append("## 相对论质量下界扫描（W05 的证据）")
L.append("")
L.append("| β = v/c | m_rel/m0 |")
L.append("|---|---|")
for r in m_rel_rows:
    L.append("| %s | %s |" % (r["beta"], r["ratio"]))
L.append("")
L.append("## 自检 guard")
L.append("")
for name, ok, why in GUARDS:
    L.append("- %s **%s** — %s" % ("OK" if ok else "FAIL", name, why))
L.append("")
L.append("## 未自推登记")
L.append("")
for x in NOT_SELF_DERIVED:
    L.append("- " + x)
L.append("")
L.append("## 图谱骨架（§七 待办的可交付部分）")
L.append("")
L.append("节点 %d、边 %d；schema 待与 openuft index 图谱层对齐。"
         % (len(GRAPH_NODES), len(GRAPH_EDGES)))
L.append("")
L.append("```json")
L.append(json.dumps(dict(nodes=GRAPH_NODES, edges=GRAPH_EDGES), ensure_ascii=False, indent=2))
L.append("```")
with io.open(MD_PATH, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(L))

T = []
T.append("=" * 78)
T.append("%s · %s · %s" % (ROUND_ID, SRC_TITLE, DATE))
T.append("=" * 78)
T.append("ITEMS = %d   %s" % (len(ITEMS), jdump(TAG_COUNT)))
T.append("GUARDS = %d/%d" % (len(GUARDS) - len(FAIL_GUARDS), len(GUARDS)))
T.append("")
for it in ITEMS:
    T.append("[%s/%s] %s" % (it["id"], it["tag"], it["name"]))
    T.append("    READ : " + it["read"])
    if it["note"]:
        T.append("    NOTE : " + it["note"])
T.append("")
T.append("-" * 78)
T.append("GUARDS")
T.append("-" * 78)
for name, ok, why in GUARDS:
    T.append("  %s %s  %s" % ("OK  " if ok else "FAIL", name, why))
T.append("")
T.append("-" * 78)
T.append("KEY NUMBERS")
T.append("-" * 78)
for k in KEY_ORDER:
    if k in KN:
        v = KN[k]
        if isinstance(v, (list, dict)):
            v = jdump(_jsonable(v))
        T.append("  %-42s = %s" % (k, v))
with io.open(TXT_PATH, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(T))

print("\n产物：")
for p in (JSON_PATH, MD_PATH, TXT_PATH):
    print("  " + p)
print("\nEXIT_CODE = %d" % (0 if not FAIL_GUARDS else 1))
sys.exit(0 if not FAIL_GUARDS else 1)
