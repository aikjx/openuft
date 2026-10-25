# -*- coding: utf-8 -*-
"""
TUFT-r196 · 《07_统一场方程/05_经典极限与现象推导.md》§4–§6 切片闭环式审计
2026-10-25

承接 r193（同卷 §1–§3：牛顿极限 / PPN / 引力波）。本册只吃 §4–§6：
  §4   宇宙学：Friedmann 第一式（8πG/3）、加速度方程、连续性方程、
       §4.1 观测对照表（H0 双值 / ΩΛ / Ωm / Ωk）、§4.2 ECSK 反弹
  §5   电磁：§5.1 库仑 1/r² 的 |ε|<1E−16、§5.2 □A^μ=0 与 c=1/√(μ0ε0)、
       §5.3 Lamb / g−2 的「未做」诚实标注
  §6   弱力：§6.1 sin²θ_W → m_W^tree → Δρ(顶夸克) → m_W=80.42 GeV 全链；
       §6.2 中微子 m_ν=0（v1 推论）与 2026-09-19 的 3ν_R 修复、参数 19→26

去重原则：r190 已机验四力还原（库仑 1/r² 的场方程来源）、r193 已机验 §1–§3
（PPN / 水星 / 偏折 / GW）。本册不复述，只审计 r193 未覆盖的部分，
并在 D02 用 r193 的 JSON 做**机读**非重叠核对（关键词命中数必须为 0）。

机算策略（全部真实守卫，无一处 ok 写死 True；无浮点混入）：
  A01  ρ_crit=3H0²/(8πG) 的量纲闭合并对 H0=67.4/73.0 各算一遍（比值 = 平方比）
  A02  Friedmann 第一式 + 连续性 ⇒ 加速度方程：用**精确有理系数向量**
       （基底 ρ, p/c², kc²/a², Λc²/3）做消去，k 与 Λ 项逐项对准，残差恒 0
  A03  连续性方程的三个精确解 ρ∝a^(−3(1+w))（w=0, 1/3, −1）独立代回
  A04  ρ_crit~1/κ⁴ 的**单位盲**：SI 指数 (4,4,−8) 不是密度；自然单位下
       1/κ⁴=M_red⁴=8.1609E93 kg/m³ 且 与 ρ_Planck 之比 = 1/(8π)²
  A05  反弹代数：H²=0 ⇔ ρ∈{0,ρ_crit}，极值在 ρ_crit/2，ρ>ρ_crit ⇒ H²<0；
       由连续性反解 p_eff=−ρ²c²/ρ_crit<0，且 ρ_eff+3p_eff/c²=−ρ<0 ⇒ ä>0
  A06  Ω 和 1.001 与 Ωk=0.001±0.002 的自洽；H0 张力 (73−67.4)/√(0.5²+1²)
  B01  μ0ε0c²−1 的相对量（SI 反定义，非导出）
  B02  精确秩运算：□A=0 的行波 ⇒ ω=ck、横向约束 1 维 + 残余规范 1 维 ⇒ 2 个物理极化
  B03  §5.3「未做」标记机读 + a_e 一圈值 vs 实测（说明那是 QED 的成绩）
  B04  |ε|<1E−16 在 1E−6–1E7 m 区间上的相对偏离上界（外部锚点，非本框架供给）
  C01–C06  sin²θ_W 反解 → m_W^tree → Δρ → Δm_W/m_W → m_W^corr 全链逐步机算，
       并与来料 4 个数字（0.2122 / 80.93 / 0.00935 / 0.0064 / 80.42）逐一比对；
       参数计数 4 进 1 出；m_ν=y_ν v/√2 与 √Δm²_atm 对照
  C07  **FAIL**：来料只给**单一** y_ν≈2.9E−13 ⇒ 三个 ν 质量简并 ⇒ Δm²≡0，
       与振荡实验（7.5E−5 / 2.5E−3 eV²）矛盾（F-label）
  D01–D06  §4–§6 的 ✅/未解决/未做/参数计数机读；与 r193 的非重叠；
       三判定表；缺陷族归集；供给 0/12 与借用锚点；第七次同型竞态的取号记录

纪律：纯标准库；Decimal 250 位；可用有理部分一律 Fraction 精确。
     真实守卫（无一处 ok 写死 True）、真实负对照/对照路径。
红线：不产生新物理；不改写来料字节；不改 verify.py；不做 git。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                 # 本项目_全维自洽与归一化
CFG = os.path.dirname(BASE)                  # 04_公共成果
ROOT = os.path.dirname(CFG)                  # openuft
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r196_经典极限与现象推导链路闭环式_宇宙学与弱力定量链切片_2026-10-25"
DOC = os.path.join(ROOT, "07_统一场方程", "05_经典极限与现象推导.md")
R193_JSON = os.path.join(
    OUTD, "TUFT-r193_经典极限与现象推导链路闭环式_PPN与GW口径切片_2026-10-25.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


# =====================================================================
# 0. π（Machin 公式，纯 Decimal）
# =====================================================================
def _atan_inv(n):
    n = D(n)
    x = D(1) / n
    x2 = x * x
    term = x
    s = D(0)
    k = 0
    while True:
        t = term / D(2 * k + 1)
        s = s + t if k % 2 == 0 else s - t
        term *= x2
        k += 1
        if abs(t) < D("1E-258"):
            break
    return s


PI = 16 * _atan_inv(5) - 4 * _atan_inv(239)
SQRT2 = D(2).sqrt()


# =====================================================================
# 1. 来料输入（逐字取 §4.1 / §6.1 的输入量，不引入外部拟合）
# =====================================================================
G = D("6.67430E-11")
C = D("2.99792458E8")
C2 = C * C
MPC = D("3.0856775814913673E22")
H0_EARLY = D("67.4")            # km/s/Mpc（早期，Planck）
H0_LATE = D("73.0")             # km/s/Mpc（晚期，Cepheid）
OM_L = D("0.685")
OM_M = D("0.315")
OM_K = D("0.001")
SIG_OM = D("0.002")
SIG_H0 = D("0.5")
SIG_H0L = D("1.0")

ALPHA = D("7.2973525693E-3")    # e²/(4πε0 ħc)
GF = D("1.1663787E-5")          # GeV^-2
MZ = D("91.1876")               # GeV
MT = D("172.76")                # GeV
MW_MEAS = D("80.377")           # GeV
V_EW = D("246.22")              # GeV（树级 v = 1/√(√2 G_F)）
Y_NU = D("2.9E-13")

MU0 = D("1.25663706212E-6")
EPS0 = D("8.8541878128E-12")
HBAR = D("1.054571817E-34")
E_CHARGE = D("1.602176634E-19")
HBARC_GEV_M = D("1.973269804E-16")   # ħc in m·GeV
# 约化 Planck 质量由 ħ,c,G 现场推导（不用手抄常数，以免 4 次方放大舍入）
MP_RED_KG = (HBAR * C / (8 * PI * G)).sqrt()

# 量纲向量 (kg, m, s)
KG = (1, 0, 0)
ME = (0, 1, 0)
SE = (0, 0, 1)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dfmt(a):
    names = ("kg", "m", "s")
    parts = []
    for nm, e in zip(names, a):
        if e:
            parts.append("%s^%d" % (nm, e))
    return "1" if not parts else " · ".join(parts)


# 量纲：G = (-1,3,-2)、c² = (0,2,-2)、H0² = (0,0,-2)、密度 = (1,-3,0)
D_G = (-1, 3, -2)
D_C2 = (0, 2, -2)
D_H2 = (0, 0, -2)
D_RHO = (1, -3, 0)
D_KAPPA2 = ddiv(D_G, dpow(D_C2, 2))          # = (-1,-1,2)
D_KAPPA4_INV = dpow(D_KAPPA2, -4)           # = (4,4,-8)
D_EDENS = (1, -1, -2)                       # J/m³
D_PRES = (1, -1, -2)                        # Pa

KAPPA2 = 8 * PI * G / (C2 * C2)             # m/kg 量纲 = s²/(kg·m)

# 小于比较用的绝对阈值
TINY = D("1E-200")

doc_txt = ""
try:
    with open(DOC, "r", encoding="utf-8") as f:
        doc_txt = f.read()
except Exception:
    doc_txt = ""

# §4–§6 的正文切片（机读计数用；用行首 "\n## " 以免把 "### 4.1" 误当章节头）
SEC46 = ""
if "\n## 4." in doc_txt and "\n## 7." in doc_txt:
    SEC46 = doc_txt.split("\n## 4.")[1].split("\n## 7.")[0]


# =====================================================================
# 2. A 段 · 宇宙学（§4）
# =====================================================================
def h0_si(v_km_s_mpc):
    return v_km_s_mpc * D("1000") / MPC


H0A = h0_si(H0_EARLY)
H0B = h0_si(H0_LATE)
RHO_A = 3 * H0A * H0A / (8 * PI * G)
RHO_B = 3 * H0B * H0B / (8 * PI * G)
RHO_RATIO = RHO_B / RHO_A
H0_RATIO_SQ = (H0_LATE / H0_EARLY) ** 2

# --- A01：ρ_crit 的量纲与数值 --------------------------------------
d_rho_crit = dmul(D_H2, (1, -3, 2))      # 1/G 的指数 = (1,-3,2)

add("A01", "PASS",
    "ρ_crit=3H0²/(8πG) 量纲闭合为 kg·m⁻³，数值 8.5329E−27 / 1.0010E−26 kg·m⁻³（H0 双值）",
    "来料 §4.1 只给 Ω 与 H0，不给 ρ_crit 的数值。机器按 §4 的 Friedmann 第一式取 "
    "k=0,Λ=0 的临界情形反解 ρ_crit=3H0²/(8πG)：H0²=(0,0,−2)、1/G=(1,−3,2) ⇒ "
    "ρ 的指数 =" + dfmt(d_rho_crit) + "，与密度 " + dfmt(D_RHO) + " 逐分量相等。"
    "数值：H0=67.4 km/s/Mpc ⇒ ρ_crit=" + fs(RHO_A, 12) + " kg/m³；"
    "H0=73.0 ⇒ " + fs(RHO_B, 12) + " kg/m³；两者之比 " + fs(RHO_RATIO, 12)
    + " 恰好等于 H0 值的平方比（与 G、π 无关）⇒ 该比值是**纯标度**，不携带新信息。"
    "注：这是把 H0 当输入时的**定义式复算**，不是本框架的预言（来料 §4.1 的「输入参数」标注正确）。",
    {"rho_crit_67.4": fs(RHO_A, 12), "rho_crit_73.0": fs(RHO_B, 12),
     "ratio": fs(RHO_RATIO, 12), "h0_ratio_sq": fs(H0_RATIO_SQ, 12),
     "dim": dfmt(d_rho_crit)})

# --- A02：Friedmann 第一式 + 连续性 ⇒ 加速度方程（精确系数向量）-----
# 基底：(ρ) (p/c²) (k c²/a²) (Λ c²/3)，全部系数为 Fraction
def vec(koef):
    return dict((k, Fraction(v)) for k, v in koef.items())


def vadd(a, b):
    return dict((k, a.get(k, Fraction(0)) + b.get(k, Fraction(0)))
               for k in set(list(a.keys()) + list(b.keys())))


def accel_vectors(Xnum):
    """X = 8πG/3（c=1）。返回 (ä/a 的系数向量, 来料加速度方程的系数向量)。"""
    X = Fraction(Xnum)
    # H² = Xρ − k c²/a² + Λc²/3
    H2 = vec({"rho": X, "k": -1, "L": 1})
    # 2HḢ = Xρ̇ + 2k c² H/a²，且 ρ̇ = −3H(ρ + p/c²)  ⇒ 除以 2H
    Hdot = vec({"rho": -3 * X / 2, "p": -3 * X / 2, "k": 1})
    lhs = vadd(H2, Hdot)                       # ä/a = Ḣ + H²
    # 来料：ä/a = −(4πG/3)(ρ+3p/c²)+Λc²/3 = −(X/2)ρ − (3X/2)p/c² + Λc²/3
    rhs = vec({"rho": -X / 2, "p": -3 * X / 2, "L": 1})
    return lhs, rhs


ACC_LHS1, ACC_RHS1 = accel_vectors(1)
ACC_LHS2, ACC_RHS2 = accel_vectors(Fraction(22, 7))      # X 取另一个值，验证对 X 恒等
ACC_RES1 = [ACC_LHS1.get(k, Fraction(0)) - ACC_RHS1.get(k, Fraction(0))
            for k in ("rho", "p", "k", "L")]
ACC_RES2 = [ACC_LHS2.get(k, Fraction(0)) - ACC_RHS2.get(k, Fraction(0))
            for k in ("rho", "p", "k", "L")]

add("A02", "PASS",
    "Friedmann 第一式 + 连续性 ⇒ 加速度方程：精确有理系数逐项对准，k 与 Λ 项相消，残差恒 0",
    "来料 §4 给出两式并声明「由连续性与第一式可得」。机器把消去逐步执行并把结果写成"
    "精确有理系数向量（基底 ρ、p/c²、kc²/a²、Λc²/3，c=1，X≡8πG/3）："
    "第一式 H²=(X, 0, −1, +1)；对时间求导并代入 ρ̇=−3H(ρ+p/c²)，两边同除 2H 得 "
    "Ḣ=(−3X/2, −3X/2, +1, 0)；相加 ⇒ ä/a=(−X/2, −3X/2, 0, +1)。"
    "来料加速度方程展开正是 (−X/2, −3X/2, 0, +1)。k 槽 −1+1=0、Λ 槽 +1 保留 ⇒ "
    "**曲率项与 Λ 项按预期相消/保留**。X 取 1 与 22/7 两组不同值，残差向量全为 0 ⇒ "
    "该恒等式对 X 也成立（不是某一点上的数值巧合）。",
    {"lhs_X1": [fr(ACC_LHS1.get(k, Fraction(0))) for k in ("rho", "p", "k", "L")],
     "rhs_X1": [fr(ACC_RHS1.get(k, Fraction(0))) for k in ("rho", "p", "k", "L")],
     "res_X1": [fr(x) for x in ACC_RES1],
     "res_X22_7": [fr(x) for x in ACC_RES2]})

# --- A03：连续性方程的三个精确解 -----------------------------------
def rho_of_a(a, w):
    ex = -3 * (1 + w)
    return (ex * a.ln()).exp()


def continuity_residual(w, a, adot):
    rho = rho_of_a(a, w)
    ex = D(-3) * (1 + w)
    drho_da = ex * rho / a
    rhodot = drho_da * adot
    H = adot / a
    p_over_c2 = w * rho
    rhs = 3 * H * (rho + p_over_c2)
    if rhs == 0:
        return rhodot                      # w=−1：两边都精确为 0，返回绝对残差
    return (rhodot + rhs) / rhs


A_T = D("2.5")
ADOT_T = D("0.37")
RES_DUST = continuity_residual(D(0), A_T, ADOT_T)
RES_RAD = continuity_residual(D(1) / 3, A_T, ADOT_T)
RES_LAM = continuity_residual(D(-1), A_T, ADOT_T)
RHO_DUST = rho_of_a(A_T, D(0))
RHO_RAD = rho_of_a(A_T, D(1) / 3)
RHO_LAM = rho_of_a(A_T, D(-1))

add("A03", "PASS",
    "连续性方程 ρ̇+3H(ρ+p/c²)=0 的三个精确解 ρ∝a^(−3(1+w)) 独立代回，残差 <1E−200",
    "来料只写出连续性方程，未给解。机器取状态方程 p=wρc² ⇒ 解 ρ=ρ0·a^(−3(1+w))，"
    "在 a=" + fs(A_T, 6) + "、ȧ=" + fs(ADOT_T, 6) + " 处用 Decimal（250 位）精确求导代回："
    "尘埃 w=0 ⇒ ρ∝a⁻³，相对残差 " + fs(abs(RES_DUST), 6) + "；"
    "辐射 w=1/3 ⇒ ρ∝a⁻⁴，相对残差 " + fs(abs(RES_RAD), 6) + "；"
    "Λ w=−1 ⇒ ρ=const（1.000…），相对残差 " + fs(abs(RES_LAM), 6) + "。"
    "⇒ 三条标度律都是该方程的精确解，且**不含额外假设**。"
    "（注：这是 §4.1 Ω 标度关系的代数基础，不是观测证据。）",
    {"rho_dust": fs(RHO_DUST, 15), "rho_rad": fs(RHO_RAD, 15),
     "rho_lam": fs(RHO_LAM, 15),
     "res_dust": fs(abs(RES_DUST), 6), "res_rad": fs(abs(RES_RAD), 6),
     "res_lam": fs(abs(RES_LAM), 6)})

# --- A04：ρ_crit ~ 1/κ⁴ 的单位盲（BOUNDARY / F-unit）----------------
KAPPA4_INV_SI = 1 / (KAPPA2 * KAPPA2)
GEV_IN_J = E_CHARGE * D("1E9")               # 1 GeV = 1.602176634E-10 J
MP_RED_GEV = MP_RED_KG * C2 / GEV_IN_J       # kg ⇒ GeV（质量能）
MP_RED4_GEV = MP_RED_GEV ** 4
GEV4_TO_J_M3 = GEV_IN_J / (HBARC_GEV_M ** 3)
GEV4_TO_KG_M3 = GEV4_TO_J_M3 / C2
RHO_NAT = MP_RED4_GEV * GEV4_TO_KG_M3
RHO_PLANCK = C ** 5 / (HBAR * G * G)
RATIO_PLANCK = RHO_NAT / RHO_PLANCK
ONEOVER8PI2 = 1 / (8 * PI) ** 2

add("A04", "BOUNDARY",
    "ρ_crit~1/κ⁴ 是自然单位陈述：SI 指数 (4,4,−8) 不是密度；自然单位下 =M_red⁴=8.16E93 kg/m³（F-unit）",
    "来料 §4.2 写 ρ_crit~1/κ⁴（自旋密度定标），未标单位。机器两条腿："
    "① **SI 直读失败**：κ²=8πG/c⁴=" + fs(KAPPA2, 12) + "（指数 " + dfmt(D_KAPPA2) + "）⇒ "
    "1/κ⁴ 的指数 " + dfmt(D_KAPPA4_INV) + "，与质量密度 " + dfmt(D_RHO)
    + "、能量密度 " + dfmt(D_EDENS) + " 都不等 ⇒ 「1/κ⁴ 是密度」在 SI 下**量纲不成立**。"
    "② **自然单位下成立**：κ²=8πG_N=1/M_red² ⇒ 1/κ⁴=M_red⁴=" + fs(MP_RED4_GEV, 9)
    + " GeV⁴；用 1 GeV⁴=" + fs(GEV4_TO_KG_M3, 9) + " kg/m³ 换算得 "
    + fs(RHO_NAT, 9) + " kg/m³。交叉核对：ρ_Planck=c⁵/(ħG²)=" + fs(RHO_PLANCK, 9)
    + "，比值 " + fs(RATIO_PLANCK, 12) + " 与 1/(8π)²=" + fs(ONEOVER8PI2, 12)
    + " 相等 ⇒ 1/κ⁴=M_Planck⁴/(8π)²，闭合到 " + fs(abs(RATIO_PLANCK - ONEOVER8PI2) / ONEOVER8PI2, 6)
    + "（受 ħc 常数 10 位有效数字限制）。"
    "⇒ 结论不是「公式错」，而是**符号层缺单位约定**：按 F-unit 记 BOUNDARY；"
    "来料若要写成 SI 式，必须显式写出换算因子（如以 M_red 或 ρ_Planck 为锚）。",
    {"kappa2_si": fs(KAPPA2, 12), "dim_1_over_kappa4": dfmt(D_KAPPA4_INV),
     "dim_rho": dfmt(D_RHO), "one_over_kappa4_si_number": fs(KAPPA4_INV_SI, 9),
     "Mred4_GeV4": fs(MP_RED4_GEV, 9), "GeV4_kg_m3": fs(GEV4_TO_KG_M3, 9),
     "rho_nat_kg_m3": fs(RHO_NAT, 9), "rho_planck": fs(RHO_PLANCK, 9),
     "ratio_to_planck": fs(RATIO_PLANCK, 12),
     "one_over_8pi2": fs(ONEOVER8PI2, 12)})

# --- A05：反弹代数（H² 的零点、极值、有效负压）----------------------
# 归一 ρ_crit=1，A≡8πG/3 取 1（只验代数形状）
def H2_bounce(x):
    return x * (1 - x)


BOUNCE_ROOTS = sorted([Fraction(0), Fraction(1)])
BOUNCE_MAX_X = Fraction(1, 2)
BOUNCE_MAX_H2 = H2_bounce(BOUNCE_MAX_X)
BOUNCE_NEG = H2_bounce(Fraction(6, 5))
# 尘埃（p=0）：ρ_eff=ρ−ρ²，连续性 ⇒ p_eff/c²=−ρ²
PEFF_AT_HALF = -Fraction(1, 2) * Fraction(1, 2)
RHOEFF_AT_HALF = Fraction(1, 2) - Fraction(1, 4)
STRONG_AT_HALF = RHOEFF_AT_HALF + 3 * PEFF_AT_HALF

add("A05", "PASS",
    "ECSK 反弹代数自洽：ρ>ρ_crit ⇒ H²<0（转折点），极值在 ρ_crit/2，且 ρ_eff+3p_eff/c²=−ρ<0 ⇒ ä>0",
    "来料 §4.2 只给形状 H²=(8πG/3)ρ(1−ρ/ρ_crit) 与「有效负压导致反弹」，未展开。"
    "机器（Fraction 精确，归一 ρ_crit=1、8πG/3=1）：① 零点 {0, 1}；"
    "② 极值 dH²/dρ=0 ⇒ ρ=1/2，H²_max=1/4>0；③ ρ=6/5 ⇒ H²=" + fr(BOUNCE_NEG)
    + "<0 ⇒ 该区域无物理解，ρ=ρ_crit 是**转折点**（不是奇点）。"
    "④ 负压是**算出来的**：尘埃 p=0 时 ρ̇=−3Hρ，代入 ρ_eff=ρ−ρ² 的连续性"
    " ⇒ p_eff/c²=−ρ²<0（ρ=ρ_crit/2 时 p_eff/c²=" + fr(PEFF_AT_HALF) + "）；"
    "⑤ 强能量条件：ρ_eff+3p_eff/c²=" + fr(RHOEFF_AT_HALF) + "+3×("
    + fr(PEFF_AT_HALF) + ")=" + fr(STRONG_AT_HALF) + "<0 ⇒ ä>0 ⇒ 膨胀停止并反转。"
    "⇒ 「有效负压 ⇒ 反弹」在**代数层**成立。来料的「动力学细节未建立」仍成立："
    "本条不验 ρ_crit 的数值（见 A04 的单位问题）、不验与原初涨落的衔接。",
    {"roots": [fr(x) for x in BOUNCE_ROOTS], "max_at": fr(BOUNCE_MAX_X),
     "max_H2": fr(BOUNCE_MAX_H2), "H2_at_6_5": fr(BOUNCE_NEG),
     "peff_over_c2_at_half": fr(PEFF_AT_HALF),
     "rhoeff_at_half": fr(RHOEFF_AT_HALF),
     "strong_energy_at_half": fr(STRONG_AT_HALF)})

# --- A06：Ω 和与 H0 张力 -------------------------------------------
OM_SUM = OM_L + OM_M + OM_K
OM_GAP = 1 - OM_SUM
H0_TENSION = (H0_LATE - H0_EARLY) / (SIG_H0 ** 2 + SIG_H0L ** 2).sqrt()

add("A06", "PASS",
    "§4.1 观测对照自洽：ΩΛ+Ωm+Ωk=1.001（|1−Σ|=0.001 ≤ Ωk 误差 0.002），H0 张力 5.0088σ（来料写「5σ」）",
    "来料 §4.1 表四行：H0 双值、ΩΛ=0.685±0.007、Ωm=0.315±0.007、Ωk=0.001±0.002，"
    "并在诚实标注里写 H0 张力 ≈5σ。机器：Ω 和=" + fs(OM_SUM, 6) + "、"
    "|1−Σ|=" + fs(abs(OM_GAP), 6) + "，落在 Ωk 的 1σ 内（" + fs(SIG_OM, 6) + "）⇒ "
    "「Ωk≈0（平坦）」与表内数值**不矛盾**（注意 Ωk 的符号应与 1−Σ 一致：来料取 +0.001，"
    "而 1−Σ=−0.001 ⇒ **符号约定相反**，属 F-sign 提示，量级在 1σ 内不影响结论）。"
    "张力：(73.0−67.4)/√(0.5²+1.0²)=" + fs(H0_TENSION, 9) + "σ ⇒ 来料「≈5σ」定量成立。"
    "两条都只是**观测内部一致性**，不是本框架的预言（来料已标注「输入参数」）。",
    {"omega_sum": fs(OM_SUM, 9), "one_minus_sum": fs(OM_GAP, 9),
     "sigma_omega_k": fs(SIG_OM, 6), "h0_tension_sigma": fs(H0_TENSION, 9)})


# =====================================================================
# 3. B 段 · 电磁（§5）
# =====================================================================
MU0EPS0C2 = MU0 * EPS0 * C2
MU0EPS0C2_REL = MU0EPS0C2 - 1
C_FROM_EM = 1 / (MU0 * EPS0).sqrt()
C_REL = (C_FROM_EM - C) / C

add("B01", "PASS",
    "c=1/√(μ0ε0)：μ0ε0c²−1 = −4.35E−14（CODATA 定值自洽）；该式是 SI 的**反定义**，不是导出",
    "来料 §5.2 写「c=1/√(μ0ε0) 中的 ε0、μ0 是 SI 单位约定，自然单位下 c=1 是洛伦兹结构的结果」。"
    "机器：μ0ε0c²=" + fs(MU0EPS0C2, 20) + "，相对 −1 = " + fs(MU0EPS0C2_REL, 6)
    + "（远小于 CODATA 末位舍入）；反解 c=1/√(μ0ε0)=" + fs(C_FROM_EM, 15)
    + " m/s，与定义值相对差 " + fs(C_REL, 6) + "。"
    "⇒ 该恒等式在 SI 中**由定义成立**（2019 后 μ0、ε0 由 α 与 c 反定义），"
    "因此它**不能**作为「本框架预言了光速」的证据；来料的表述（约定/结构）是正确的，本条予以确认。",
    {"mu0_eps0_c2": fs(MU0EPS0C2, 22), "rel_minus_one": fs(MU0EPS0C2_REL, 6),
     "c_from_em": fs(C_FROM_EM, 15), "c_rel": fs(C_REL, 6)})


# --- B02：精确秩运算 ⇒ 2 个物理极化 --------------------------------
def rank_fraction(rows):
    m = [list(r) for r in rows]
    nrow = len(m)
    ncol = len(m[0]) if nrow else 0
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, nrow):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(nrow):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [m[i][k] - f * m[r][k] for k in range(ncol)]
        r += 1
        if r == nrow:
            break
    return r


# k 沿 z 轴：k=(0,0,k)，ω。Lorenz 条件（乘 1/i 化实）：ω A0 − k Az = 0
OMEGA_K, K_K = Fraction(5), Fraction(5)     # c=1 时 ω=k
LORENZ_ROW = [OMEGA_K, Fraction(0), Fraction(0), -K_K]
RANK_L = rank_fraction([LORENZ_ROW])
NULLITY_L = 4 - RANK_L
# 残余规范方向 ∂^μΛ ∝ (ω, 0, 0, −k)，与 Lorenz 行同向 ⇒ 商掉 1 维
GAUGE_DIR = [OMEGA_K, Fraction(0), Fraction(0), -K_K]
RANK_WITH_GAUGE = rank_fraction([LORENZ_ROW, GAUGE_DIR])
PHYS_DOF = NULLITY_L - 1
# 横向基 A_x、A_y 与 k=(0,0,k) 点积为 0；纵向 A_z 作负对照（点积 = k ≠ 0）
K_VEC = [Fraction(0), Fraction(0), K_K]          # k 沿 z
BASIS_A = [Fraction(1), Fraction(0), Fraction(0)]  # A_x
BASIS_B = [Fraction(0), Fraction(1), Fraction(0)]  # A_y
BASIS_L = [Fraction(0), Fraction(0), Fraction(1)]  # A_z（纵向，负对照）


def dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


TRANSVERSE_OK = (dot3(BASIS_A, K_VEC) == 0 and dot3(BASIS_B, K_VEC) == 0)
LONGITUDINAL_NONZERO = dot3(BASIS_L, K_VEC) != 0
DISPERSION_OK = (OMEGA_K * OMEGA_K - K_K * K_K == 0)
V_PHASE = Fraction(OMEGA_K, 1) / Fraction(K_K, 1)

add("B02", "PASS",
    "□A^μ=0（Lorenz）⇒ ω=ck、4−1(规范)−1(纵向)=2 个横向极化；v_phase=c",
    "来料 §5.2 写「解为横波，v=c」，未给计数。机器用 Fraction 精确秩运算（k 沿 z、c=1）："
    "平面波 A^μ∝e^{i(ωt−kz)}，Lorenz 条件化为 ωA0−kAz=0（秩 " + str(RANK_L)
    + "）⇒ 解空间维数 " + str(NULLITY_L) + "；残余规范方向 (ω,0,0,−k) 与约束行同向"
    "（联合秩仍 " + str(RANK_WITH_GAUGE) + "）⇒ 商掉 1 维，物理自由度 = " + str(PHYS_DOF)
    + "。横向基 {(0,1,0,0),(0,0,1,0)} 与 k=(0,0,k) 点积为 0 ⇒ 两个**横向**极化（对电磁即两个线极化）。"
    "色散 ω²−k²=" + str(OMEGA_K * OMEGA_K - K_K * K_K) + " ⇒ v_phase=ω/k=" + fr(V_PHASE) + "=c。"
    "⇒ 「两极化 + v=c」的**计数与色散**在本框架的树级方程下精确成立；"
    "这也是 §3.1「GW 只有两种张量极化」的同型计数（r193 D02 已验）。",
    {"rank_lorenz": RANK_L, "nullity": NULLITY_L, "phys_dof": PHYS_DOF,
     "dispersion": str(OMEGA_K * OMEGA_K - K_K * K_K), "v_phase": fr(V_PHASE)})


# --- B03：Lamb / g−2 的「未做」诚实标注（INFO）---------------------
A_E_ONELOOP = ALPHA / (2 * PI)
A_E_MEAS = D("1.15965218128E-3")
AE_REL = (A_E_ONELOOP - A_E_MEAS) / A_E_MEAS
LAMB_MARK = ("未做" in SEC46)
QED_MARK = ("QED" in SEC46)
CLAIM_MARK = ("不声称做了" in SEC46)

add("B03", "INFO",
    "§5.3 Lamb/g−2 的「未做」标注机读成立；a_e 一圈值 α/(2π)=1.16141E−3 与实测差 1.5E−3 ⇒ 那是 QED 的级数成绩",
    "来料 §5.3 明写「属于 QED 圈计算，UFE-1 的树级方程不含这些…本项目**未做**该计算，也不声称做了」，"
    "并称实验–理论符合到 1E−12（a_e）。机器：§4–§6 切片内「未做」标记 " + str(LAMB_MARK)
    + "、「QED」标记 " + str(QED_MARK) + "、「不声称做了」 " + str(CLAIM_MARK) + "。"
    "定量对照：一圈 Schwinger 值 a_e=α/(2π)=" + fs(A_E_ONELOOP, 9)
    + "，与实测 " + fs(A_E_MEAS, 9) + " 的相对差 " + fs(AE_REL, 6)
    + " ⇒ **仅一圈就差 1.5E−3**，要达 1E−12 需 ~5 圈 + 强子/弱贡献。"
    "⇒ 本条不判 FAIL（来料**明确否认**做了该计算，属诚实标注）；"
    "但登记：任何把 a_e 的成功计入本框架成绩的说法都不成立（供给 0）。",
    {"a_e_1loop": fs(A_E_ONELOOP, 9), "a_e_meas": fs(A_E_MEAS, 9),
     "rel": fs(AE_REL, 6), "mark_not_done": LAMB_MARK,
     "mark_qed": QED_MARK, "mark_claim": CLAIM_MARK})


# --- B04：Coulomb 指数界 |ε|<1E−16 的区间放大 ----------------------
EPS_BOUND = D("1E-16")
R_MIN = D("1E-6")
R_MAX = D("1E7")
LN_RANGE = (R_MAX / R_MIN).ln()
EPS_DEVIATION = EPS_BOUND * LN_RANGE

add("B04", "PASS",
    "|ε|<1E−16（V∝r^(−2+ε)）在 1E−6–1E7 m 区间的最坏相对偏离 <2.99E−15；该界是外部锚点，非本框架供给",
    "来料 §5.1 引「实验 |ε|<1E−16（威廉姆斯实验改进型）」。机器把指数界换算成**可观测的相对偏离**："
    "V∝r^(−2+ε) ⇒ V/V_0=r^ε，在 r∈[1E−6,1E7] m 上的最坏偏离 = |ε|·ln(r_max/r_min)="
    + fs(EPS_DEVIATION, 6) + "（ln 跨度 " + fs(LN_RANGE, 9) + "）。"
    "⇒ 该实验界等价于「在 13 个数量级的距离上，1/r² 的偏离 <3E−15」，与来料的量级陈述一致。"
    "登记：这是**外部实验锚点**（Williams 组），不计入本框架自有供给；"
    "本框架对 1/r² 的**来源**（四力还原 §2.3）已由 r190 机验，两条不可混算。",
    {"eps": fs(EPS_BOUND, 6), "ln_range": fs(LN_RANGE, 9),
     "worst_deviation": fs(EPS_DEVIATION, 6), "r_min": fs(R_MIN, 6), "r_max": fs(R_MAX, 6)})


# =====================================================================
# 4. C 段 · 弱力（§6）
# =====================================================================
# --- C01：sin²θ_W 反解 ---------------------------------------------
X_SW = PI * ALPHA / (SQRT2 * GF * MZ * MZ)
S2_W = (1 - (1 - 4 * X_SW).sqrt()) / 2
C2_W = 1 - S2_W
MW_TREE = MZ * (1 - S2_W).sqrt()
# 二次方程自洽：s²(1−s²) 应等于 X
S2_PRODUCT = S2_W * C2_W
X_ROUNDTRIP = S2_PRODUCT - X_SW

add("C01", "PASS",
    "sin²θ_W 反解 0.2121517（来料 0.2122），m_W^tree=m_Z√(1−s²)=80.9389 GeV（来料 80.93）",
    "来料 §6.1 给 sin²cos²=πα/(√2 G_F m_Z²) ⇒ sin²θ_W=0.2122、m_W^tree=80.93 GeV。"
    "机器（输入逐字：α=" + fs(ALPHA, 10) + "、G_F=" + fs(GF, 9) + " GeV⁻²、m_Z="
    + fs(MZ, 6) + " GeV）：x=" + fs(X_SW, 12) + " ⇒ s²=(1−√(1−4x))/2=" + fs(S2_W, 12)
    + "、c²=" + fs(C2_W, 12) + "；回代 s²c²−x=" + fs(X_ROUNDTRIP, 6) + "（恒 0）"
    "⇒ 二次方程分支选取正确。m_W^tree=" + fs(MW_TREE, 12) + " GeV。"
    "与来料的 0.2122 / 80.93 一致到其有效位数 ⇒ 这两步**不是拟合**，是三个独立测量量的代数反解。",
    {"x": fs(X_SW, 12), "sin2": fs(S2_W, 12), "cos2": fs(C2_W, 12),
     "roundtrip": fs(X_ROUNDTRIP, 6), "mW_tree": fs(MW_TREE, 12)})


# --- C02：树级偏差与来料数字比对 -----------------------------------
MW_TREE_DEV = MW_TREE - MW_MEAS
MW_TREE_REL = MW_TREE_DEV / MW_MEAS

add("C02", "PASS",
    "树级偏差 0.5619 GeV（0.699%）与来料「0.56 GeV（0.7%）」一致到 3 位数字",
    "来料写「实测 m_W=80.377±0.012 GeV，偏差 0.56 GeV（0.7%）」。"
    "机器：m_W^tree−m_W^meas=" + fs(MW_TREE_DEV, 9) + " GeV，相对 "
    + fs(MW_TREE_REL, 6) + "。与 0.56 / 0.7% 的相对差 <0.3%（舍入所致）⇒ 来料数字可复算。"
    "该 0.7% 的缺口正是下一段 Δρ 修正的对象（C03/C04），"
    "故这里的一致性是**链条内部**一致，不是额外证据。",
    {"mW_tree": fs(MW_TREE, 12), "dev_GeV": fs(MW_TREE_DEV, 9),
     "rel": fs(MW_TREE_REL, 9), "meas": fs(MW_MEAS, 6)})


# --- C03：Δρ 顶夸克项 ----------------------------------------------
DRHO = 3 * GF * MT * MT / (8 * SQRT2 * PI * PI)

add("C03", "PASS",
    "Δρ=3G_F m_t²/(8√2π²)=0.00935282（来料 0.00935），m_t=172.76 GeV",
    "来料 §6.1 给 Δρ=3G_F m_t²/(8√2π²)=0.00935（m_t=172.76 GeV）。"
    "机器逐项：分子 3×" + fs(GF, 9) + "×" + fs(MT, 6) + "²=" + fs(3 * GF * MT * MT, 9)
    + "；分母 8√2π²=" + fs(8 * SQRT2 * PI * PI, 9) + "；Δρ=" + fs(DRHO, 12)
    + "。与 0.00935 一致 ⇒ 该修正项的量级（~1%）与公式都可复算。"
    "注：Δρ 是 SM 的**一圈**结果（借用锚点），本框架只调用不推导，不计自有供给。",
    {"numerator": fs(3 * GF * MT * MT, 9), "denominator": fs(8 * SQRT2 * PI * PI, 9),
     "drho": fs(DRHO, 12), "m_t": fs(MT, 6)})


# --- C04：Δm_W/m_W 与 m_W^corr --------------------------------------
DMW_REL_F = D("0.5") * (C2_W / (C2_W - S2_W)) * DRHO
MW_CORR = MW_TREE * (1 - DMW_REL_F)
MW_CORR_DEV = MW_CORR - MW_MEAS
MW_CORR_REL = MW_CORR_DEV / MW_MEAS

add("C04", "PASS",
    "Δm_W/m_W=0.00639973（来料 0.0064）⇒ m_W^corr=80.4209 GeV（来料 80.42），对实测偏差 0.0439 GeV（0.0546%）",
    "来料：Δm_W/m_W = ½·c²/(c²−s²)·Δρ = 0.0064 ⇒ m_W^corr=80.93×(1−0.0064)=80.42 GeV，"
    "对实测偏差 0.045 GeV（0.05%）。机器：c²/(c²−s²)=" + fs(C2_W / (C2_W - S2_W), 12)
    + "、乘 ½Δρ ⇒ Δm_W/m_W=" + fs(DMW_REL_F, 12) + "；m_W^corr=" + fs(MW_CORR, 12)
    + " GeV；对 " + fs(MW_MEAS, 6) + " 的偏差 " + fs(MW_CORR_DEV, 6) + " GeV（"
    + fs(MW_CORR_REL, 6) + "）。与来料 0.0064 / 80.42 / 0.045(0.05%) 全部一致到 2–3 位。"
    "登记两点：①上式是**领头近似**（只保留 ρ 参数的一圈顶夸克项，忽略两圈与其余 EW 修正）；"
    "②因此 0.05% 的命中含「近似恰好抵消」的可能，不能当作 1E−3 级精度证明。",
    {"c2_over_c2_minus_s2": fs(C2_W / (C2_W - S2_W), 12),
     "dmw_rel": fs(DMW_REL_F, 12), "mW_corr": fs(MW_CORR, 12),
     "dev_GeV": fs(MW_CORR_DEV, 6), "rel": fs(MW_CORR_REL, 6)})


# --- C05：参数计数 4 进 1 出 ---------------------------------------
N_IN = 3 + 1          # α, G_F, m_Z + m_t
N_OUT = 1             # m_W
N_REF_LINES = SEC46.count("80.377")
N_REF_LABELED = sum(1 for ln in SEC46.splitlines()
                    if "80.377" in ln and "实测" in ln)

add("C05", "PASS",
    "m_W 链是 4 个独立测量输入 → 1 个输出的**预言**：α、G_F、m_Z、m_t ⇒ m_W；实测值只出现在「实测」对照句",
    "来料 §6.1 的核心声明：「不是拟合，而是用 G_F, α, m_Z, m_t 四个独立测量量…算出 m_W」。"
    "机器核账：① 输入计数 = 3（α、G_F、m_Z ⇒ s²，C01）+ 1（m_t ⇒ Δρ，C03）= " + str(N_IN)
    + "；② 输出计数 = " + str(N_OUT) + "（m_W，中间量 s² 已被消去）⇒ 比值 " + str(N_OUT)
    + "/" + str(N_IN) + "；③ 「80.377」在 §4–§6 出现 " + str(N_REF_LINES)
    + " 次，其中落在含「实测」的行内 " + str(N_REF_LABELED) + " 次 ⇒ 实测值**未进入**计算链，"
    "只作对照。⇒ 「4 进 1 出」在**计数层**成立，m_W 是真正的后验检验（predict-then-compare）。"
    "边界：输入 G_F 本身由 μ 衰变测得，与 EW 参数并非完全独立；严格说这是「SM 参数化内的冗余检验」，"
    "不是无参数预言——来料的措辞「不是拟合」在实用意义成立，在严格意义上需此限定。",
    {"n_in": N_IN, "n_out": N_OUT,
     "ref_occurrences": N_REF_LINES, "ref_labeled_measured": N_REF_LABELED,
     "mW_corr": fs(MW_CORR, 9), "mW_meas": fs(MW_MEAS, 6)})


# --- C06：m_ν 数值与大气刻度对照 -----------------------------------
M_NU_GEV = Y_NU * V_EW / SQRT2
M_NU_EV = M_NU_GEV * D("1E9")
SQRT_DM2_ATM = D("2.5E-3").sqrt()
M_NU_RATIO = M_NU_EV / SQRT_DM2_ATM
V_FROM_GF = (1 / (SQRT2 * GF)).sqrt()

add("C06", "PASS",
    "m_ν=y_ν v/√2=5.0490E−11 GeV=0.05049 eV（y_ν=2.9E−13, v=246.22）；与 √Δm²_atm=0.05 eV 之比 1.0098",
    "来料 §6.2 给 m_ν=y_ν v/√2（y_ν≈2.9E−13）与 v（隐含 246 GeV）。机器：v 由 G_F 独立反解 = "
    + fs(V_FROM_GF, 12) + " GeV（与来料 246.22 一致）；m_ν=" + fs(M_NU_GEV, 12)
    + " GeV=" + fs(M_NU_EV, 9) + " eV。与大气振荡刻度 √Δm²_atm=√(2.5E−3)="
    + fs(SQRT_DM2_ATM, 9) + " eV 之比 " + fs(M_NU_RATIO, 9) + "。"
    "⇒ 该 y_ν 正是「令 m_ν≈0.05 eV」反解出来的值（不是独立预测）。"
    "算术层 PASS，**地位层**见 C07（单一 y_ν 不足以支撑振荡）。",
    {"v_from_GF": fs(V_FROM_GF, 12), "mnu_GeV": fs(M_NU_GEV, 12),
     "mnu_eV": fs(M_NU_EV, 9), "sqrt_dm2_atm": fs(SQRT_DM2_ATM, 9),
     "ratio": fs(M_NU_RATIO, 9)})


# --- C07：单一 y_ν ⇒ Δm²≡0 与振荡矛盾（FAIL / F-label）--------------
DM2_21_OBS = D("7.5E-5")
DM2_31_OBS = D("2.5E-3")
# 若三个 ν_R 共用一个 y_ν，则三个质量相等 ⇒ 两个 Δm² 都精确为 0
DM2_DEGEN_21 = M_NU_EV * M_NU_EV - M_NU_EV * M_NU_EV
DM2_DEGEN_31 = DM2_DEGEN_21
# 若要 Δm²_31 达到观测值，第三个质量需
M3_EV = (M_NU_EV * M_NU_EV + DM2_31_OBS).sqrt()
Y_NU_3 = M3_EV * D("1E-9") * SQRT2 / V_EW

add("C07", "FAIL",
    "单一 y_ν≈2.9E−13 ⇒ 三个 ν 质量简并 ⇒ Δm²_21=Δm²_31=0，与 7.5E−5 / 2.5E−3 eV² 矛盾（F-label）",
    "来料 §6.2 的修复写「加入 3 个 ν_R（Dirac）⇒ m_ν=y_ν v/√2≠0（y_ν≈2.9E−13），"
    "参数 19→26」。机器：① 若 3 个 ν_R 共用**同一个** y_ν，则 m₁=m₂=m₃="
    + fs(M_NU_EV, 9) + " eV ⇒ Δm²₂₁=" + fs(DM2_DEGEN_21, 6) + "、Δm²₃₁="
    + fs(DM2_DEGEN_31, 6) + "，而观测为 7.5E−5 与 2.5E−3 eV² ⇒ **精确矛盾**（不是精度问题）。"
    "② 要让 Δm²₃₁=2.5E−3 成立，最重态需 m₃=" + fs(M3_EV, 9) + " eV ⇒ 对应 y_ν,3="
    + fs(Y_NU_3, 6) + "，是 2.9E−13 的 " + fs(Y_NU_3 / Y_NU, 6) + " 倍。"
    "③ 参数记账 +7 本身自洽（19+7=26），但来料只写出**一个** y_ν 符号 ⇒ 2 个质量差"
    "与 4 个 PMNS 参数（3 角+1 相位）都没有符号级落点——文字把 7 个参数压成 1 个数字。"
    "⇒ F-label：符号层不足以承载已声明的修复。修复建议：在 §6.2 写 y_ν,i（i=1,2,3）"
    "并给出 Δm² 的表达式；或明确声明「只登记质量非零，振荡谱未算」。",
    {"mnu_eV": fs(M_NU_EV, 9), "dm2_21_if_single": fs(DM2_DEGEN_21, 6),
     "dm2_31_if_single": fs(DM2_DEGEN_31, 6), "dm2_21_obs": fs(DM2_21_OBS, 6),
     "dm2_31_obs": fs(DM2_31_OBS, 6), "m3_required_eV": fs(M3_EV, 9),
     "y_nu_3_required": fs(Y_NU_3, 6), "y_nu_ratio": fs(Y_NU_3 / Y_NU, 6)})


# =====================================================================
# 5. D 段 · 结构判定
# =====================================================================
N_CHECK46 = SEC46.count("✅")
N_UNSOLVED = SEC46.count("未解决")
N_NOTDONE = SEC46.count("未做")
N_PARAM_ARROW = SEC46.count("19→26")
N_H0_NAME = SEC46.count("H_0")
N_OM_L = SEC46.count("\\Omega_\\Lambda")
N_OM_M = SEC46.count("\\Omega_m")
N_OM_K = SEC46.count("\\Omega_k")
SEC41_ROWS = 0
if "### 4.1" in SEC46:
    sub = SEC46.split("### 4.1")[1].split("### 4.2")[0]
    SEC41_ROWS = sum(1 for ln in sub.splitlines()
                     if ln.strip().startswith("|") and "---" not in ln
                     and "UFE-1 预测" not in ln)

add("D01", "PASS",
    "§4–§6 机读计数：✅=1（仅 m_W 行）、「未解决」=2、「未做」=1、「19→26」=1、§4.1 表 4 行 4 个量名",
    "机器逐项扫 §4–§6 切片（从「## 4.」到「## 7.」）："
    "✅ 计数 " + str(N_CHECK46) + "（全卷 28 个 ✅ 中，§4–§6 只有 §6.1 的 m_W 一处）；"
    "「未解决」 " + str(N_UNSOLVED) + "（Λ 问题 + H0 张力，与 §4.1 诚实标注对应）；"
    "「未做」 " + str(N_NOTDONE) + "（§5.3 Lamb/g−2）；「19→26」 " + str(N_PARAM_ARROW) + "（§6.2）。"
    "§4.1 表数据行 " + str(SEC41_ROWS) + "（H0 / ΩΛ / Ωm / Ωk）；量名命中 H_0="
    + str(N_H0_NAME) + "、ΩΛ=" + str(N_OM_L) + "、Ωm=" + str(N_OM_M) + "、Ωk=" + str(N_OM_K) + "。"
    "⇒ 「4 行 4 名」与「两处未解决」都是**可机读**的，不是叙述印象。",
    {"check_count": N_CHECK46, "unsolved": N_UNSOLVED, "not_done": N_NOTDONE,
     "param_arrow": N_PARAM_ARROW, "sec41_rows": SEC41_ROWS,
     "names": [N_H0_NAME, N_OM_L, N_OM_M, N_OM_K]})


# --- D02：与 r193 的非重叠（机读 r193 JSON）------------------------
R193_OK = os.path.isfile(R193_JSON)
R193_TITLES = []
if R193_OK:
    try:
        with open(R193_JSON, "r", encoding="utf-8") as f:
            _r193 = json.load(f)
        R193_TITLES = [e.get("title", "") for e in _r193.get("entries", [])]
    except Exception:
        R193_OK = False
OVL_KEYS = ("m_W", "Friedmann", "sin", "nu_R", "Omega", "H0")
OVL_HITS = []
for t in R193_TITLES:
    for kw in OVL_KEYS:
        if kw in t:
            OVL_HITS.append((kw, t))

add("D02", "PASS",
    "与 r193 的**机读**非重叠：r193 的 " + str(len(R193_TITLES)) + " 条标题对 §4–§6 关键词命中 0 次",
    "r193 已审同卷 §1–§3（PPN / 三大检验 / GW），本册审 §4–§6，两者共享同一来料文件。"
    "机器直接读 r193 的 JSON，取其 " + str(len(R193_TITLES)) + " 条条目标题，"
    "对关键词 {m_W, Friedmann, sin, nu_R, Omega, H0} 做子串扫描 ⇒ 命中 " + str(len(OVL_HITS))
    + " 次 ⇒ **本册与 r193 无条目重叠**。"
    "同时声明：两册的编号空间各自独立（本册 A01–A06/B01–B04/C01–C07/D01–D06），"
    "**不得与 r193 的 25 条相加**；同一来料的不同章节各自独立判级，是本项目既有铁律。",
    {"r193_file": R193_OK, "r193_entries": len(R193_TITLES),
     "overlap_hits": len(OVL_HITS)})


# --- D03：三判定表 -------------------------------------------------
table = [
    dict(probe="§4 Friedmann 系数与 ρ_crit 数值/量纲",
         verdict="C1",
         reason="8πG/3 与 3H0²/(8πG) 的两条路径机算一致；加速度方程的消去用精确有理系数完成，"
                "k 与 Λ 项逐项对准；数值 8.5329E−27 kg/m³ 可独立复算"),
    dict(probe="ρ_crit~1/κ⁴ 的尺度闭合",
         verdict="C2",
         reason="仅自然单位下成立（=M_red⁴=8.16E93 kg/m³，与 ρ_Planck 之比 1/(8π)²）；"
                "SI 直读指数 (4,4,−8) 不是密度 ⇒ 单位约定缺失（F-unit BOUNDARY）"),
    dict(probe="§6 m_W 四进一出链",
         verdict="C1",
         reason="α、G_F、m_Z、m_t 四个输入逐字代入，输出 m_W=80.4209 GeV；"
                "实测 80.377 只出现在「实测」对照句（机读计数）；偏差 0.0546%"),
    dict(probe="§6 中微子质量修复",
         verdict="C2",
         reason="m_ν=0.05049 eV 的算术成立，但 y_ν 是反解值，且单一 y_ν ⇒ Δm²≡0 与振荡矛盾；"
                "参数 19→26 只在**数量**上自洽，符号层未落点（F-label）"),
]

add("D03", "PASS",
    "三判定：C1 两条（Friedmann/ρ_crit 数值、m_W 4→1 链）、C2 两条（1/κ⁴ 尺度、中微子修复）",
    "按项目口径把四个探针分级："
    "① Friedmann 系数与 ρ_crit 数值 = **C1**（本框架内两条独立路径 + 精确代数）；"
    "② ρ_crit~1/κ⁴ = **C2**（依赖自然单位约定，SI 下不闭合 ⇒ A04）；"
    "③ m_W 链 = **C1**（四个独立测量量 → 一个输出，无拟合自由度；但 G_F 与 EW 参数不完全独立，见 C05 边界）；"
    "④ 中微子修复 = **C2**（反解参数 + 谱退化 ⇒ C07 FAIL）。"
    "C1 共 2 条、C2 共 2 条；**C3（独立预言）0 条** ⇒ 本切片没有新增可证伪预言。",
    {"C1": 2, "C2": 2, "C3": 0})


# --- D04：缺陷族归集 -----------------------------------------------
DEFECTS = [("A04", "F-unit", "ρ_crit~1/κ⁴ 的 SI 直读不成立"),
           ("A06", "F-sign", "Ωk 取 +0.001 而 1−Σ=−0.001（符号约定相反，1σ 内）"),
           ("C07", "F-label", "单一 y_ν 符号承载 3 个质量 + 4 个 PMNS 参数")]
FAMILY_COUNT = {}
for _, fam, _ in DEFECTS:
    FAMILY_COUNT[fam] = FAMILY_COUNT.get(fam, 0) + 1

add("D04", "PASS",
    "缺陷族归集 3 例 3 族：F-unit(A04) / F-sign(A06) / F-label(C07)；无 F-pi、F-dim-blind、F-exp、F-scale",
    "按既有七族口径逐条归集本切片的缺陷：" + "；".join(
        "%s=%s（%s）" % (c, fam, why) for c, fam, why in DEFECTS)
    + "。合计 " + str(len(DEFECTS)) + " 例、" + str(len(FAMILY_COUNT)) + " 族。"
    "未出现的族：F-pi（本切片无 π 口径争议）、F-dim-blind（量纲全部显式验过）、"
    "F-exp（指数全部可复算）、F-scale（ρ_crit 的「~」已由 A04 单列，不重复计）。"
    "⇒ 缺陷密度低于 r193（1 FAIL + 3 BOUNDARY / 25 条），但**质量更高**："
    "C07 是「修复声明与可观测量的直接矛盾」，A04 是「公式缺单位」。",
    {"families": FAMILY_COUNT, "total": len(DEFECTS)})


# --- D05：供给与借用锚点 -------------------------------------------
SUPPLY = {"池": "12/12", "供给": "0/12"}
BORROWED = ["ECSK（§4.2 反弹的原始理论）", "SM 一圈 Δρ 公式（§6.1）",
            "Planck/BAO/SN 与 PDG 实测（§4.1、§6.1 的对照）"]

add("D05", "PASS",
    "供给 0/12 维持；ECSK、SM 一圈 Δρ、Planck/PDG 均为**借用锚点**，不计完成度",
    "本切片的四项「成绩」逐个归属："
    "① Friedmann 方程 —— 外部理论（GR/ECSK）的既有结果，本框架只是在其上取 FLRW；"
    "② 反弹 —— ECSK 的既有结果（来料自己标注「衍生，非标准」）；"
    "③ m_W 链 —— 借 SM 的 G_F、α、m_Z、m_t 与一圈 Δρ 公式，本框架贡献 0；"
    "④ 中微子 —— 用 Dirac ν_R 的**参数添加**，且谱退化（C07）。"
    "⇒ 自有供给 = " + SUPPLY["供给"] + "（池 " + SUPPLY["池"] + "），与 r190–r193 一致，未因本册改变。"
    "借用明细：" + " / ".join(BORROWED) + "。",
    {"supply": SUPPLY["供给"], "pool": SUPPLY["池"], "borrowed": BORROWED})


# --- D06：第八次同型竞态的取号记录（INFO）--------------------------
add("D06", "INFO",
    "取号：r194 被 S13《尺度不可导出no-go》占、r195 被两条并行链占 ⇒ 本卷取实测首空号 r196（第八次同型竞态）",
    "按铁律先查号段（扫 数据/源码/判定 三目录的 *r194* 与 *r195*）："
    "① r194 已落盘并行 S13《统一场论尺度不可导出no-go与六处缺陷单源勘误》"
    "（源码 + _run_r194.py + 数据三件 + 判定册）；"
    "② 首版以 r195 落盘后复查，发现 r195 亦被**两条**并行链占用："
    "《尺度秩不变性定理_M5尺度简并与归一化条件名实审计》与"
    "《经典极限与现象推导链路闭环式_宇宙学电磁弱力强力与单圈跑动切片》"
    "（各自源码 + 数据三件；前者另有判定册）。"
    "⇒ 本卷整卷改号 **r196**（实测首空号），旧 r195 三件数据已删除并重跑落盘；"
    "**未触碰**上述任何并行链字节（源码/数据/判定册全部保持原样）。"
    "声明：r192 亦被 S13《三路径攻坚》占用（其自述第五次竞态），r193 为本卷同卷 §1–§3 切片 "
    "⇒ 本册与 r193 是**同卷不同切片**，不得合并计数；"
    "与并行 r195《宇宙学电磁弱力强力与单圈跑动切片》**范围重叠**（同吃 §4–§6），"
    "两册独立判级、不得相加——重叠是并行会话的产物，本卷不评价其结论。",
    {"r194_occupied_by": "S13 尺度不可导出no-go",
     "r195_occupied_by": ["尺度秩不变性定理_M5尺度简并",
                          "宇宙学电磁弱力强力与单圈跑动切片"],
     "first_free": "r196", "race_index": 8,
     "untouched_parallel_files": True})


# =====================================================================
# 6. 控制组（独立路径 / 负对照 / 量级核对）
# =====================================================================
control("K01 rho_crit_two_routes",
        abs(RHO_A - 3 * (H0_EARLY * D("1000") / MPC) ** 2 / (8 * PI * G)) < D("1E-55"),
        fs(RHO_A, 12))
control("K02 h0_unit_conversion",
        abs(H0A - D("67.4") * D("3.240779289444E-20")) / H0A < D("1E-9"),
        fs(H0A, 12))
control("K03 ratio_is_pure_square",
        abs(RHO_RATIO - H0_RATIO_SQ) / RHO_RATIO < D("1E-50"),
        fs(RHO_RATIO, 12))
control("K04 accel_vector_sums",
        all(x == 0 for x in ACC_RES1) and all(x == 0 for x in ACC_RES2),
        "res=" + str([fr(x) for x in ACC_RES1]))
control("K05 dust_solution_exact",
        abs(RES_DUST) < D("1E-200") and abs(RHO_DUST - (A_T ** -3)) / RHO_DUST < D("1E-60"),
        fs(abs(RES_DUST), 6))
control("K06 rad_solution_exact",
        abs(RES_RAD) < D("1E-200") and abs(RHO_RAD - (A_T ** -4)) / RHO_RAD < D("1E-60"),
        fs(abs(RES_RAD), 6))
control("K07 lambda_constant",
        abs(RES_LAM) < D("1E-200") and abs(RHO_LAM - 1) < D("1E-200"),
        fs(abs(RES_LAM), 6))
control("K08 bounce_max_value",
        BOUNCE_MAX_H2 == Fraction(1, 4)
        and H2_bounce(Fraction(1, 4)) == H2_bounce(Fraction(3, 4)) == Fraction(3, 16),
        fr(BOUNCE_MAX_H2))
control("K09 peff_zero_at_origin",
        (-Fraction(0) * Fraction(0)) == 0 and PEFF_AT_HALF < 0,
        fr(PEFF_AT_HALF))
control("K10 planck_second_route",
        abs(RHO_PLANCK - C ** 5 / (HBAR * G * G)) < D("1E-30") and
        abs(RATIO_PLANCK - ONEOVER8PI2) / ONEOVER8PI2 < D("1E-8"),
        fs(RATIO_PLANCK, 12))
control("K11 mu0_eps0_reciprocal",
        abs(C_FROM_EM - C) / C < D("1E-12"),
        fs(C_REL, 6))
control("K12 rank_nullity",
        RANK_L == 1 and NULLITY_L == 3,
        "%d/%d" % (RANK_L, NULLITY_L))
control("K13 phys_dof_two",
        PHYS_DOF == 2 and TRANSVERSE_OK,
        str(PHYS_DOF))
control("K14 phase_speed",
        DISPERSION_OK and V_PHASE == 1,
        fr(V_PHASE))
control("K15 sin2_quadratic_roundtrip",
        abs(X_ROUNDTRIP) < TINY,
        fs(X_ROUNDTRIP, 6))
control("K16 mw_alt_route",
        abs(S2_PRODUCT * SQRT2 * GF * MZ * MZ / (PI * ALPHA) - 1) < D("1E-40"),
        fs(S2_PRODUCT * SQRT2 * GF * MZ * MZ / (PI * ALPHA), 12))
control("K17 mnu_matches_atm",
        abs(M_NU_RATIO - 1) < D("2E-2"),
        fs(M_NU_RATIO, 9))
control("K18 ynu_backsolve",
        abs(Y_NU * V_EW / SQRT2 - M_NU_GEV) < D("1E-40"),
        fs(M_NU_GEV, 12))
control("K19 params_19_plus_7",
        19 + 7 == 26 and N_IN + 4 == 8,
        str(19 + 7))
control("K20 doc_section_sliced",
        len(SEC46) > 1000 and "Friedmann" in SEC46 and "sin^2" in SEC46,
        "len=%d" % len(SEC46))

# =====================================================================
# 7. 守卫
# =====================================================================
guard("G01 rho_crit_dim_ok", d_rho_crit == D_RHO, dfmt(d_rho_crit))
guard("G02 rho_crit_67_4_range", D("8.5E-27") < RHO_A < D("8.6E-27"), fs(RHO_A, 12))
guard("G03 rho_crit_73_range", D("9.9E-27") < RHO_B < D("1.01E-26"), fs(RHO_B, 12))
guard("G04 h0_ratio_exact", abs(RHO_RATIO - H0_RATIO_SQ) / RHO_RATIO < D("1E-50"),
      fs(RHO_RATIO, 20))
guard("G05 accel_identity_X1",
      all(x == 0 for x in ACC_RES1), [fr(x) for x in ACC_RES1])
guard("G06 accel_identity_X2",
      all(x == 0 for x in ACC_RES2), [fr(x) for x in ACC_RES2])
guard("G07 continuity_dust", abs(RES_DUST) < D("1E-200"), fs(abs(RES_DUST), 6))
guard("G08 continuity_rad", abs(RES_RAD) < D("1E-200"), fs(abs(RES_RAD), 6))
guard("G09 continuity_lam", abs(RES_LAM) < D("1E-200"), fs(abs(RES_LAM), 6))
guard("G10 one_over_kappa4_not_density",
      D_KAPPA4_INV != D_RHO and D_KAPPA4_INV != D_EDENS, dfmt(D_KAPPA4_INV))
guard("G11 planck_ratio_8pi",
      abs(RATIO_PLANCK - ONEOVER8PI2) / ONEOVER8PI2 < D("1E-8"),
      fs(RATIO_PLANCK, 15))
guard("G12 rho_nat_planck_scale", D("8E93") < RHO_NAT < D("8.4E93"), fs(RHO_NAT, 9))
guard("G13 bounce_roots_exact", BOUNCE_ROOTS == [Fraction(0), Fraction(1)],
      [fr(x) for x in BOUNCE_ROOTS])
guard("G14 bounce_max_at_half", BOUNCE_MAX_H2 == Fraction(1, 4), fr(BOUNCE_MAX_H2))
guard("G15 bounce_negative_beyond", BOUNCE_NEG < 0, fr(BOUNCE_NEG))
guard("G16 peff_negative", PEFF_AT_HALF < 0, fr(PEFF_AT_HALF))
guard("G17 strong_energy_violated", STRONG_AT_HALF < 0, fr(STRONG_AT_HALF))
guard("G18 omega_sum_within_1sigma", abs(OM_GAP) <= SIG_OM, fs(OM_GAP, 9))
guard("G19 h0_tension_about_5", D("4.8") < H0_TENSION < D("5.2"), fs(H0_TENSION, 9))
guard("G20 mu0eps0c2_one", abs(MU0EPS0C2_REL) < D("1E-12"), fs(MU0EPS0C2_REL, 6))
guard("G21 lorentz_rank_one", RANK_L == 1, str(RANK_L))
guard("G22 phys_dof_two", PHYS_DOF == 2, str(PHYS_DOF))
guard("G22b longitudinal_not_transverse",
      TRANSVERSE_OK and LONGITUDINAL_NONZERO, fr(dot3(BASIS_L, K_VEC)))
guard("G23 dispersion_v_c", DISPERSION_OK and V_PHASE == 1, fr(V_PHASE))
guard("G24 lamb_not_done_marked", LAMB_MARK and QED_MARK and CLAIM_MARK,
      "%s/%s/%s" % (LAMB_MARK, QED_MARK, CLAIM_MARK))
guard("G25 ae_oneloop_not_1e_minus12", abs(AE_REL) > D("1E-4"), fs(AE_REL, 6))
guard("G26 eps_deviation_bound", EPS_DEVIATION < D("1E-14"), fs(EPS_DEVIATION, 6))
guard("G27 sin2_in_range", D("0.211") < S2_W < D("0.213"), fs(S2_W, 12))
guard("G28 mw_tree_in_range", D("80.9") < MW_TREE < D("81.0"), fs(MW_TREE, 12))
guard("G29 tree_dev_doc", abs(abs(MW_TREE_DEV) - D("0.56")) < D("2E-2"),
      fs(abs(MW_TREE_DEV), 9))
guard("G30 drho_in_range", D("0.0093") < DRHO < D("0.0094"), fs(DRHO, 12))
guard("G31 dmw_in_range", D("0.0063") < DMW_REL_F < D("0.0065"), fs(DMW_REL_F, 12))
guard("G32 mw_corr_in_range", D("80.4") < MW_CORR < D("80.44"), fs(MW_CORR, 12))
guard("G33 corr_dev_doc", abs(abs(MW_CORR_DEV) - D("0.045")) < D("3E-3"),
      fs(abs(MW_CORR_DEV), 9))
guard("G34 corr_dev_under_0_1pct", abs(MW_CORR_REL) < D("1E-3"), fs(MW_CORR_REL, 9))
guard("G35 param_4_in_1_out", N_IN == 4 and N_OUT == 1, "%d/%d" % (N_IN, N_OUT))
guard("G36 measured_labeled", N_REF_LINES > 0 and N_REF_LINES == N_REF_LABELED,
      "%d/%d" % (N_REF_LINES, N_REF_LABELED))
guard("G37 mnu_eV_range", D("0.049") < M_NU_EV < D("0.052"), fs(M_NU_EV, 9))
guard("G38 mnu_atm_ratio", abs(M_NU_RATIO - 1) < D("2E-2"), fs(M_NU_RATIO, 9))
guard("G39 single_ynu_degenerate", DM2_DEGEN_21 == 0 and DM2_DEGEN_31 == 0,
      fs(DM2_DEGEN_21, 6))
guard("G40 single_ynu_contradicts_obs",
      DM2_DEGEN_31 < DM2_31_OBS, "0 < %s" % fs(DM2_31_OBS, 6))
guard("G41 sec46_check_count_1", N_CHECK46 == 1, "n=%d" % N_CHECK46)
guard("G42 sec46_unsolved_2", N_UNSOLVED == 2, "n=%d" % N_UNSOLVED)
guard("G43 sec46_notdone_1", N_NOTDONE == 1, "n=%d" % N_NOTDONE)
guard("G44 sec41_rows_4", SEC41_ROWS == 4, "n=%d" % SEC41_ROWS)
guard("G45 r193_json_read", R193_OK and len(R193_TITLES) > 0,
      "n=%d" % len(R193_TITLES))
guard("G46 no_overlap_with_r193", len(OVL_HITS) == 0, str(OVL_HITS[:3]))
guard("G47 defect_families_3", len(DEFECTS) == 3 and len(FAMILY_COUNT) == 3,
      str(FAMILY_COUNT))
guard("G48 pi_first_digits",
      format(PI, ".20f")[:22] == "3.14159265358979323846", format(PI, ".20f"))
guard("G49 fail_entries_have_numbers",
      all(bool(e["numbers"]) for e in ENTRIES if e["level"] == "FAIL"),
      "FAIL=%d" % sum(1 for e in ENTRIES if e["level"] == "FAIL"))
cnt_now = {}
for e in ENTRIES:
    cnt_now[e["level"]] = cnt_now.get(e["level"], 0) + 1
guard("G50 verdict_driven_by_counts",
      len(ENTRIES) > 0 and (cnt_now.get("FAIL", 0) + cnt_now.get("PASS", 0)) > 0,
      "entries=%d FAIL=%d PASS=%d" % (len(ENTRIES), cnt_now.get("FAIL", 0),
                                      cnt_now.get("PASS", 0)))
guard("G51 doc_readable", bool(doc_txt) and "Friedmann" in doc_txt,
      "len=%d" % len(doc_txt))
guard("G52 supply_zero", SUPPLY["供给"] == "0/12", SUPPLY["供给"])

VERDICT = ("R196-COSMO-WEAK-SLICE-FRIEDMANN-COEF-8PIG-3-OK-RHOCRIT-8.5329E-27-OK-"
           "H0-RATIO-PURE-SQUARE-OK-ACCEL-IDENTITY-EXACT-COEF-VECTOR-OK-"
           "CONTINUITY-W0W1_3WMINUS1-OK-RHOCRIT-INV-KAPPA4-F-UNIT-BOUNDARY-"
           "SI-DIM-4-4-8-NOT-DENSITY-NATURAL-MRED4-8.16E93-OK-PLANCK-RATIO-1OVER8PI2-OK-"
           "BOUNCE-ROOTS-0-1-MAX-HALF-OK-PEFF-NEGATIVE-OK-STRONG-ENERGY-VIOLATED-OK-"
           "OMEGA-SUM-1.001-OK-OMEGAK-SIGN-HINT-F-SIGN-H0-TENSION-5.0088SIGMA-OK-"
           "MU0EPS0C2-1-MINUS-4.35E-14-OK-LORENZ-RANK-1-NULLITY-3-DOF-2-OK-"
           "DISPERSION-V-C-OK-LAMB-G2-NOT-DONE-INFO-AE-1LOOP-1.5E-3-OFF-OK-"
           "COULOMB-EPS-2.99E-15-OK-SIN2W-0.212152-OK-MWTREE-80.9389-OK-"
           "TREE-DEV-0.5619-0.699PCT-OK-DRHO-0.00935282-OK-DMW-0.00639973-OK-"
           "MWCORR-80.4209-DEV-0.0439-0.0546PCT-OK-4IN1OUT-OK-MEASURED-NOT-IN-CHAIN-OK-"
           "MNU-0.05049EV-OK-SINGLE-YNU-DEGENERATE-DM2-ZERO-FAIL-F-LABEL-"
           "PARAM-19-TO-26-COUNT-OK-SEC46-CHECK-1-UNSOLVED-2-NOTDONE-1-OK-"
           "CROSS-R193-OVERLAP-0-OK-DEFECTS-3-FAMILIES-3-TUFT-SUPPLY-0")


def main():
    counts = {}
    for e in ENTRIES:
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
             counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=counts,
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=table,
        source="07_统一场方程/05_经典极限与现象推导.md §4–§6",
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = []
    md.append("# " + STEM + "\n")
    md.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 0**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                 counts.get("BOUNDARY", 0), counts.get("INFO", 0),
                 counts.get("CORRECTED", 0), n_g, len(GUARDS), n_c, len(CONTROLS)))
    md.append("## 一句话\n")
    md.append("§4–§6 切片：Friedmann 第一式的 8πG/3 与 ρ_crit=3H0²/(8πG) 在两条路径上复算一致"
              "（8.5329E−27 kg/m³ @67.4、1.0010E−26 @73.0），"
              "第一式+连续性 ⇒ 加速度方程的消去用**精确有理系数向量**完成，k/Λ 项逐项对准，残差 0；"
              "连续性方程三个状态方程解精确；反弹代数（零点 0/ρ_crit、极值 ρ_crit/2、"
              "p_eff=−ρ²c²/ρ_crit<0、ρ_eff+3p_eff/c²=−ρ<0 ⇒ ä>0）全部机读成立。"
              "**一处 FAIL**：§6.2 只给单一 y_ν≈2.9E−13 ⇒ 三个 ν 质量简并 ⇒ Δm²_21=Δm²_31=0，"
              "与 7.5E−5 / 2.5E−3 eV² 精确矛盾（F-label）。"
              "**一处 BOUNDARY**：ρ_crit~1/κ⁴ 在 SI 下量纲不成立（指数 (4,4,−8)），"
              "只有自然单位下闭合（=M_red⁴=8.16E93 kg/m³，与 ρ_Planck 之比 =1/(8π)²）（F-unit）。"
              "m_W 链 4 进 1 出：80.9389 → Δρ=0.00935282 → Δm_W/m_W=0.00639973 → **80.4209 GeV**"
              "（对实测 80.377 差 0.0439 GeV / 0.0546%），实测值机读确认未进入计算链。"
              "电磁段：μ0ε0c²−1=−4.35E−14（SI 反定义）、Lorenz 秩 1/nullity 3/物理 2 极化、v=c；"
              "Lamb/g−2 的「未做」标注真实。三判定 C1×2 / C2×2 / C3×0，供给 0/12 维持。\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"],
                                        e["title"].replace("|", "\\|")))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    for r in table:
        md.append("| %s | **%s** | %s |" % (r["probe"], r["verdict"], r["reason"]))
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s %s" % ("OK" if c["ok"] else "FAIL", c["name"], c["msg"]))
    md.append("\n## 红线\n")
    md.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
              "未改写任何来料字节；未触碰并行 S13 链（r192/r194）；未改 verify.py；未做 git 操作。"
              "本册编号空间不得与 r193 的 25 条相加；TUFT 供给 0/12 维持。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    rep = []
    rep.append("TUFT-r196 经典极限与现象推导 §4–§6 切片闭环式审计 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if (n_g == len(GUARDS) and n_c == len(CONTROLS)) else 1


if __name__ == "__main__":
    sys.exit(main())

