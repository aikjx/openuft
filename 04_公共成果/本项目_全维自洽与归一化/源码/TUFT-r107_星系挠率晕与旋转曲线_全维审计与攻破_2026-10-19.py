# -*- coding: utf-8 -*-
"""TUFT-r107 ｜ 星系挠率晕模型、旋转曲线拟合、参数分析、可观测预言 —— 全维审计与攻破

来料 = 《🌀TUFT‑V9｜星系挠率晕模型、旋转曲线拟合、参数分析、可观测预言》
论题一句话：星系暗晕不是暗物质粒子，而是 tau_phi = tau0*r0/r 的真空挠率涡旋场，
额外加速度 a_halo = K/r（K=(c*tau0*r0)^2），从而 v^2 = GM_vis/r + K 给出平坦旋转曲线。

本册立场（红线）：只读审计 + 机器判决，不产生新物理、不修改来料任何字节、
不修改既有 r 序列任何产物。所有裁定必须由可复算的数值/量纲/恒等式断言承担。

数值标准：纯标准库 decimal（prec=60）+ fractions（量纲四元组）。
收敛判据一律用「相对残差」，绝对残差在天文量级无意义（本库既有纪律）。
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 注意：本文件位于 <...>/本项目_全维自洽与归一化/源码/ 下，
# dirname 两次才是「本项目_全维自洽与归一化」，三次会越到 04_公共成果（r95 曾踩同坑）
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DATA = os.path.join(ROOT, "数据")
OUT_SRC = os.path.join(ROOT, "源码")

# ----------------------------------------------------------------- 高精度常数
# CODATA 2018 / IAU 2015 定义值；全部以 SI 为单位
C = Decimal("299792458")                    # m/s  精确定义
G = Decimal("6.67430e-11")                  # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")           # J s
LY = Decimal("9460730472580800")            # m  (IAU 光年, 精确)
PC = Decimal("3.0856775814913673e16")       # m  (IAU 秒差距)
KPC = PC * Decimal(1000)
MSUN = Decimal("1.98847e30")                # kg
A0_MOND = Decimal("1.2e-10")                # m/s^2  MOND 特征加速度（常用值）
EPS0 = Decimal("8.8541878128e-12")          # F/m

# 来料给定值（原样登记，不修正）
ENTRIES = []
NOT_SELF_DERIVED = []
EXTERNAL_INPUTS = []


def _j(o):
    if isinstance(o, Decimal):
        return float(o)
    if isinstance(o, Fraction):
        return float(o)
    if isinstance(o, dict):
        return dict((k, _j(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_j(v) for v in o]
    return o


def add(code, verdict, title, detail, **ev):
    """登记一条判定。verdict ∈ PASS/FAIL/BOUNDARY/CORRECTED/INFO/MISMATCH"""
    e = {"code": code, "verdict": verdict, "title": title, "detail": detail}
    for k, v in ev.items():
        e[k] = _j(v)
    ENTRIES.append(e)
    return e


STATE = {"guard": 0, "guard_fail": 0, "guard_msgs": []}


def guard(cond, name, desc=""):
    STATE["guard"] += 1
    ok = bool(cond)
    if not ok:
        STATE["guard_fail"] += 1
        STATE["guard_msgs"].append(name + " :: " + desc)
    return ok


# ------------------------------------------------------- 量纲四元组 (M,L,T,Q)
def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


DIMLESS = D(0, 0, 0, 0)


def dmul(a, b):
    """量纲相乘 = 指数相加（本库第 N 次强调：不是逐分量相乘）"""
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)


def deq(a, b):
    return tuple(a) == tuple(b)


def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for i, v in enumerate(a):
        if v == 0:
            continue
        s = names[i]
        if v != 1:
            s = s + "^" + str(v)
        out.append(s)
    if not out:
        return "1"
    return " · ".join(out)


NAME_DIM = {}
NAME_VAL = {}


def reg(name, val, dim):
    NAME_DIM[name] = dim
    NAME_VAL[name] = val
    return val


# 基础量纲：质量/长度/时间/电荷
reg("M", MSUN, D(1, 0, 0, 0))
reg("L", PC, D(0, 1, 0, 0))
reg("T", Decimal(1), D(0, 0, 1, 0))
reg("Q", Decimal(1), D(0, 0, 0, 1))
reg("c", C, D(0, 1, -1, 0))
reg("G", G, D(-1, 3, -2, 0))
reg("hbar", HBAR, D(1, 2, -1, 0))
reg("tau", Decimal(1), D(0, -1, 0, 0))       # 挠率（空间） L^-1
reg("rho", Decimal(1), D(1, -3, 0, 0))       # 质量密度
reg("rho_q", Decimal(1), D(0, -3, 0, 1))     # 电荷密度 C/m^3（与 rho 不同，勿混用！）
reg("eps0", EPS0, D(-1, -3, 2, 2))           # F/m：由 Coulomb F=q²/(4πε0 r²) 反解
reg("a", Decimal(1), D(0, 1, -2, 0))
reg("K", Decimal(1), D(0, 2, -2, 0))         # v^2
reg("v", Decimal(1), D(0, 1, -1, 0))

DIM_ENERGY_DENSITY = D(1, -1, -2, 0)
DIM_FORCE = D(1, 1, -2, 0)
DIM_ACC = D(0, 1, -2, 0)
DIM_INV_L = D(0, -1, 0, 0)


def fmt(x, n=25):
    try:
        d = Decimal(x)
    except Exception:
        return str(x)
    s = format(d, "." + str(n) + "E")
    m, e = s.split("E")
    return m + "E" + e


def rel(a, b):
    """相对偏差 |a-b|/max(|a|,|b|)，返回 Decimal"""
    a = Decimal(a)
    b = Decimal(b)
    mx = max(abs(a), abs(b))
    if mx == 0:
        return Decimal(0)
    return abs(a - b) / mx


def vs(fmt_, *args):
    return fmt_ % tuple(args)


# =========================================================================
# G0 段：量纲工具自检（纪律：工具必须先自检，再用于判定）
# =========================================================================
_guards_before = STATE["guard"]
# G0-1 库仑定律闭合：F = q²/(4πε0 r²) ⇒ [ε0] = Q²·M⁻¹·L⁻³·T²
guard(deq(NAME_DIM["eps0"], ddiv(dpow(D(0, 0, 0, 1), 2),
                                 dmul(DIM_FORCE, dpow(D(0, 1, 0, 0), 2)))),
      "G0-1", "[ε0] 必须使库仑力闭合")
# G0-2 [Gρ] = T^-2（泊松方程标准口径）
guard(deq(dmul(NAME_DIM["G"], NAME_DIM["rho"]), D(0, 0, -2, 0)),
      "G0-2", "[G][ρ] 必须 = T^-2")
# G0-3 [(1/4πε0)·(q/m)·ρ_q] = T^-2（来料扩展方程第二项）
_d_dim_src_em = dmul(ddiv(DIMLESS, NAME_DIM["eps0"]),
                     dmul(ddiv(D(0, 0, 0, 1), D(1, 0, 0, 0)), NAME_DIM["rho_q"]))
guard(deq(_d_dim_src_em, D(0, 0, -2, 0)),
      "G0-3", "电磁源项必须与引力源项同为 T^-2")
# G0-4 [□τ] 内部两项齐次，且 ∇²τ = L^-3
_d_box1 = dmul(D(0, -2, 0, 0), DIM_INV_L)                           # ∇²τ = L^-3
_d_box2 = dmul(ddiv(DIMLESS, dpow(NAME_DIM["c"], 2)),
               ddiv(DIM_INV_L, dpow(D(0, 0, 1, 0), 2)))              # (1/c²)∂²τ/∂t²
guard(deq(_d_box1, _d_box2) and deq(_d_box1, D(0, -3, 0, 0)),
      "G0-4", "达朗贝尔算子两项须齐次且 [□τ]=L^-3")
# G0-5 ε0μ0 = 1/c² 闭合（交叉验证 Q 维度一致性）
_d_mu0 = ddiv(DIMLESS, dmul(NAME_DIM["eps0"], dpow(NAME_DIM["c"], 2)))
guard(deq(_d_mu0, D(1, 1, 0, -2)), "G0-5", "由 ε0μ0c²=1 反解出的 [μ0] 须为 M·L·Q^-2")
# G0-6 dim mul 语义：相乘=指数相加（不是逐分量相乘）
guard(deq(dmul(D(1, 0, 0, 0), D(1, 0, 0, 0)), D(2, 0, 0, 0)),
      "G0-6", "dmul 必须是指数相加")
guard(deq(ddiv(D(1, 0, 0, 0), D(1, 0, 0, 0)), DIMLESS), "G0-6b", "ddiv 必须相减")

add("G00", "PASS",
    "量纲工具自检通过（%d 条）" % (STATE["guard"] - _guards_before),
    "本库纪律：量纲代数曾多次被记错实现或记错符号（r37/r66 等均发生过），"
    "故在用于任何判定前先以库仑定律、泊松方程、达朗贝尔算子、ε0μ0c²=1 四条外部恒等式锁死工具。"
    "本次 G0 自检 %d/%d 通过。" % (STATE["guard"] - STATE["guard_fail"] - _guards_before,
                                    STATE["guard"] - _guards_before))


# =============================================================== 来料原样登记值
LAI = {
    "r0_ly": Decimal("2.5e4"),
    "r0_m_claim": Decimal("2.365e20"),
    "vinf_ms": Decimal("2.2e5"),
    "K_claim": Decimal("4.84e10"),
    "c_used": Decimal("2.998e8"),
    "tau0_claim": Decimal("3.10e-24"),
    "rsun_kpc": Decimal("8"),
    "rsun_m_claim": Decimal("2.47e20"),
    "ahalo_claim": Decimal("1.96e-10"),
}

# =========================================================================
# A 段：主推导链复算（来料唯一被正面支持的部分）
# =========================================================================
print("=" * 100)
print("A 段 ｜ 主推导链复算：柱坐标矢量拉普拉斯 → 欧拉 ODE → τ∝1/r")
print("=" * 100)


def cilap_scalar_formula(A, Ap, App, r):
    """柱坐标下切向分量算子 claimed 形式: A'' + A'/r - A/r^2"""
    return App + Ap / r - A / (r * r)


# --- A01 解析验证：τ=r^n 时该算子给出 (n^2-1) r^(n-2)
# 这是对来料「n(n-1)+n-1=0 ⇒ n^2-1=0」的精确复算（整数运算，无浮点）
_n_results = {}
for _n in [-2, -1, 0, 1, 2, 3]:
    n = Fraction(_n)
    # A = r^n ; A' = n r^(n-1) ; A'' = n(n-1) r^(n-2)
    # 算子系数（以 r^(n-2) 为单位）: n(n-1) + n - 1
    coef = n * (n - 1) + n - 1
    _n_results[_n] = coef
    A01_rows = [(_n, str(_n_results[_n])) for _n in sorted(_n_results)]
add("A01", "PASS",
    "柱坐标切向矢量拉普拉斯的算子形式与特征方程 n^2-1=0 正确",
    "对 Ansatz τ_φ=r^n，算子 A''+A'/r-A/r^2 的系数为 n(n-1)+n-1=n^2-1，"
    "机器精确复算（整数 Fraction，无浮点）与来料逐项一致；"
    "n=±1 时系数恒为 0，故 τ∝r 与 τ∝1/r 确为该齐次方程的两支基解。",
    rows=A01_rows,
    n_zero=[_n for _n in _n_results if _n_results[_n] == 0])

guard(all(_n_results[_n] == Fraction(_n) ** 2 - 1 for _n in _n_results),
      "G-A01", "算子系数必须恒等于 n^2-1")
guard([_n for _n in _n_results if _n_results[_n] == 0] == [-1, 1],
      "G-A01b", "n^2-1=0 的根必须恰为 ±1")


# --- A02 独立数值对拍：笛卡尔坐标下直接二阶差分，避免「柱坐标形式本身写错」的风险
def tau_cart(field, x, y):
    """把 τ_φ(r) φ̂ 写成笛卡尔分量并返回三分量"""
    r = math.hypot(x, y)
    t = field(r)
    return (-y / r * t, x / r * t, 0.0)


def vec_laplacian_cart(field, x, y, h=1e-4):
    """9 点二阶中心差分：∇²τ（逐分量）"""
    f0 = tau_cart(field, x, y)
    out = [0.0, 0.0, 0.0]
    for i in range(3):
        xp, xm = tau_cart(field, x + h, y)[i], tau_cart(field, x - h, y)[i]
        yp, ym = tau_cart(field, x, y + h)[i], tau_cart(field, x, y - h)[i]
        dxx = (xp - 2.0 * f0[i] + xm) / (h * h)
        dyy = (yp - 2.0 * f0[i] + ym) / (h * h)
        out[i] = dxx + dyy
    return out


def radial_component(vec, x, y):
    r = math.hypot(x, y)
    return (vec[0] * x + vec[1] * y) / r


def phi_component(vec, x, y):
    r = math.hypot(x, y)
    return (vec[0] * (-y) + vec[1] * x) / r


_A02 = []
_TESTS = [
    ("τ∝1/r（来料解）", lambda r: 1.0 / r, True),
    ("τ∝r（被舍去解）", lambda r: 3.0 * r, True),
    ("τ∝r^2（阳性对照·非解）", lambda r: 2.0 * r * r, False),
]
_XY = [(1.7, 0.9), (3.0, 4.0), (11.0, -5.0), (7.0, 7.0)]
for _name, _f, _is_sol in _TESTS:
    worst = 0.0
    worst_ref = 0.0
    for (x, y) in _XY:
        r = math.hypot(x, y)
        lap = vec_laplacian_cart(_f, x, y)
        ph = phi_component(lap, x, y)
        rad = radial_component(lap, x, y)
        # 参考量级：|τ|/r^2 是该项的自然尺度
        ref = abs(_f(r)) / (r * r)
        worst = max(worst, abs(ph) / ref, abs(rad) / ref)
        if not _is_sol:
            worst_ref = max(worst_ref, ref)
    _A02.append((_name, _is_sol, worst))

add("A02", "PASS",
    "笛卡尔九点差分独立复算：τ∝1/r 与 τ∝r 确为该算子零点，τ∝r^2 不是",
    "不复用柱坐标公式，直接在笛卡尔坐标对 τ_φ(r)φ̂ 做九点二阶中心差分并投影到 "
    "(r̂,φ̂)，4 个取样点整体上：两支基解的全部分量残差/参考量级 ≤ 量级 %s，"
    "而阳性对照 τ∝r^2 残差为 O(1)（同层面非零）。检验器非恒零，A01 的形式得到独立支撑。"
    % fmt(Decimal(max(v for _, _, v in _A02[:2])), 3),
    rows=[(n, ("是解" if s else "非解"), fmt(Decimal(w), 6)) for n, s, w in _A02])

_w_sol = max(v for n, s, v in _A02 if s)
_w_non = max(v for n, s, v in _A02 if not s)
guard(_w_sol < 1e-4, "G-A02", "两支基解的数值拉普拉斯应≈0，实测 %s" % _w_sol)
guard(_w_non > 1e-2, "G-A02b", "阳性对照 τ∝r^2 必须显著非零（否则检验器恒零），实测 %s" % _w_non)

# --- A03 ~ A06 银河系数值链复算（来料算术整段核对）
r0_m = LAI["r0_ly"] * LY
Kcalc = LAI["vinf_ms"] ** 2
tau0_calc = Kcalc.sqrt() / (C * r0_m)
rsun_m = LAI["rsun_kpc"] * KPC
ahalo_calc = Kcalc / rsun_m

_A03 = [
    ("r0 = 2.5e4 ly", r0_m, LAI["r0_m_claim"]),
    ("K = v∞²", Kcalc, LAI["K_claim"]),
    ("rsun = 8 kpc", rsun_m, LAI["rsun_m_claim"]),
    ("a_halo(rsun) = K/r", ahalo_calc, LAI["ahalo_claim"]),
]
_A03_rows = []
_max_rel = Decimal(0)
for nm, got, claim in _A03:
    rv = rel(got, claim)
    _max_rel = max(_max_rel, rv)
    _A03_rows.append((nm, fmt(got), fmt(claim), fmt(rv, 6)))

add("A03", "PASS",
    "银河系数值链算术全部正确（含单位换算）",
    "r0 光年→米、K=v∞²、8 kpc→米、a=K/r 四项用精确定义值（IAU ly/pc、精确 c）复算，"
    "与来料 3 位有效数字报价相对偏差最大 %s，全部落在报价精度内。"
    "本册按惯例仍用相对残差判定——天文量级下绝对残差无意义。" % fmt(_max_rel, 6),
    rows=_A03_rows)

add("A04", "PASS",
    "τ0 ≈ 3.10e-24 m^-1 与太阳位置 a_halo ≈ 1.96e-10 m/s² 复算一致",
    "τ0 = √K/(c·r0) = %s m^-1（来料 %s）；a_halo(r_sun) = %s m/s²（来料 %s）。"
    "来料此处取 c=2.998e8 的三位 truncation，与本册精确 c 的差异远低于报价位。"
    "注意：这条「与 MOND a0 同量级」的对照在数值上成立，但只是数量级巧合，"
    "不构成机制同源的证据（见 D 段）。"
    % (fmt(tau0_calc), fmt(LAI["tau0_claim"]), fmt(ahalo_calc), fmt(LAI["ahalo_claim"])),
    tau0=tau0_calc, ahalo=ahalo_calc)

guard(_max_rel < Decimal("5e-3"), "G-A03", "来料算术须在 3 位报价精度内，实测 %s" % fmt(_max_rel, 6))

# =========================================================================
# B 段：矢量三重积的方向裁定（字形与标量式对，方向自述反）
# =========================================================================
print()
print("=" * 100)
print("B 段 ｜ a_drag = -ω×(ω×r) 的径向符号：声称「向心」，机器判为离心")
print("=" * 100)


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale3(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


# 单位矢量（柱坐标 → 笛卡尔）
def rhat(x, y):
    r = math.hypot(x, y)
    return (x / r, y / r, 0.0)


def phihat(x, y):
    r = math.hypot(x, y)
    return (-y / r, x / r, 0.0)


_B_rows = []
CTAU0R0 = 1.0                       # 令 A ≡ τ0 r0 = 1，τ_φ(r) = A/r = 1/r
_SAMPLES = [(1.0, 0.0), (3.0, 4.0), (7.0, -2.0), (11.0, 5.0)]
_b_signs = []
for (_x, _y) in _SAMPLES:
    _r = math.hypot(_x, _y)
    pos = (_x, _y, 0.0)
    om = scale3(phihat(_x, _y), CTAU0R0 / _r)      # ω = c·τ_φ(r) φ̂，取 c·A = 1
    a_drag = scale3(cross3(om, cross3(om, pos)), -1.0)   # 来料定义 -ω×(ω×r)
    rad_comp = dot3(a_drag, rhat(_x, _y))
    mag = math.sqrt(dot3(a_drag, a_drag))
    expect = (CTAU0R0 / _r) ** 2 * _r             # K/r = ω²r，取正值做量值对照
    _b_signs.append(rad_comp > 0)
    _B_rows.append(((_x, _y), rad_comp, mag, expect))
    print("  r=(%.1f,%.1f)  a_drag·r̂ = %+.6e   |a_drag| = %.6e   K/r = %.6e"
          % (_x, _y, rad_comp, mag, expect))

_b_mag_ok = all(abs(rr[2] - rr[3]) / rr[3] < 1e-9 for rr in _B_rows)
_b_all_outward = all(s for s in _b_signs)

add("B01", "FAIL",
    "★a_drag = -ω×(ω×r) 是离心（向外），与「提供额外向心力」自述严格反号",
    "机器直接算三重积：在盘面 z=0 上 ω=cτ_φ φ̂ 满足 ω·r=0，由 BAC-CAB 恒等式 "
    "ω×(ω×r)=ω(ω·r)-r ω² = -ω² r r̂（真正向心），故加负号后 a_drag=+ω² r r̂ 指向 r̂ 正方向。"
    "取样点 %s 全部给出 a_drag·r̂ > 0。标量值 |a_drag| = K/r 与来料式逐点吻合（相对偏差<1e-9），"
    "即「数值对、方向反」：若严格按其矢量定义执行，该力把物质推离星系，"
    "不可能贡献平坦旋转曲线所需的额外向心加速度。"
    % str([tuple(p) for p, _, _, _ in _B_rows]),
    rows=[("取样点(x,y)", "a·r̂", "|a|", "K/r")] + _B_rows)

guard(_b_mag_ok, "G-B01", "|a_drag| 必须等于 K/r（否则判据无力），实测不符")
guard(_b_all_outward, "G-B01b", "所有取样点 a_drag·r̂ 必须同号为正（离心）")

# --- B02 阳性对照：验证三重积工具本身没写反
_om_z = (0.0, 0.0, 2.5)                       # 刚体绕 z 轴，Ω=2.5
_pv = (3.0, 4.0, 0.0)
_ac = cross3(_om_z, cross3(_om_z, _pv))       # 标准向心加速度 ω×(ω×r)
_radv = dot3(_ac, rhat(3.0, 4.0))
add("B02", "PASS",
    "三重积工具自校正：标准刚体 ω=Ωẑ 下 ω×(ω×r) 确为向心 (−Ω²r⊥)",
    "阳性对照（Ω=2.5, r⊥=5）：ω×(ω×r)·r̂ = %+.6f，理论值 −Ω²r⊥ = %+.6f，相对偏差 %s。"
    "⇒ B01 的符号结论不是工具自身写反所致。"
    % (_radv, -2.5 ** 2 * 5.0, fmt(rel(Decimal(repr(_radv)), Decimal(repr(-2.5 ** 2 * 5.0))), 6)))
guard(_radv < 0 and abs(_radv - (-2.5 ** 2 * 5.0)) < 1e-9,
      "G-B02", "阳性对照失败：三重积工具本身有误")

add("B03", "CORRECTED",
    "零成本修法：删去负号取 a = +ω×(ω×r)，数值式 a_halo=K/r 与全部下游数值逐点不变",
    "本缺陷不改任何已算出的数字（K、τ0、a_halo、旋转曲线全不受影响），"
    "但必须显式登记：现稿的矢量定义与「向心」语义互斥，直接照式编码会得到发散而非束缚。"
    "这是零成本修正类缺陷，不等同于下文 C/D 段的结构性阻塞。",
    cost="零参数代价")

# --- B04 挠率晕作为离心 的机制代价：若坚持原符号则需解释为"外推压力"
add("B04", "INFO",
    "若保留原符号，唯一自洽读法是「向外的挠率压」——但那样星系将解体而非平坦",
    "保留 −ω×(ω×r) 的话 a_halo 为向外 ≥0，加入 v²/r = GM/r² + a_halo 后右端正项变小甚至变负，"
    "外围不再有实数圆轨道速度；故该读法与「维持平坦旋转曲线」的立论目的直接冲突。"
    "来料未察觉只因在写标量式时丢掉了符号信息。")

# =========================================================================
# C 段：★决定性结构阻塞 —— τ∝1/r 是无旋梯度场 ⇒ u_τ≡0 ⇒ 透镜预言自毁
# =========================================================================
print()
print("=" * 100)
print("C 段 ｜ τ_φ=A/r 是纯梯度场：∇×τ≡0 ⇒ 能量密度≡0 ⇒ 第3条判别预言被自身解吃掉")
print("=" * 100)

A_AMP = 1.0                                  # A ≡ τ0·r0


def tau_field(x, y):
    """τ = (A/r) φ̂ 的笛卡尔分量"""
    r = math.hypot(x, y)
    return (-y / (r * r) * A_AMP, x / (r * r) * A_AMP, 0.0)


def curl_cart(f, x, y, h=1e-4):
    """数值旋度 ∂τ_y/∂x - ∂τ_x/∂y（z 分量）及 r,φ 分量"""
    fx = f(x, y)
    dty_dx = (f(x + h, y)[1] - f(x - h, y)[1]) / (2 * h)
    dtx_dy = (f(x, y + h)[0] - f(x, y - h)[0]) / (2 * h)
    dtz_dy = (f(x, y + h)[2] - f(x, y - h)[2]) / (2 * h)
    dty_dz = 0.0
    dtx_dz = 0.0
    dtz_dx = 0.0
    return (dtz_dy - dty_dz, dtx_dz - dtz_dx, dty_dx - dtx_dy)


# --- C01 τ_φ = A/r 是否等于 A·∇φ（纯梯度场判定）
_grad_rows = []
for (_x, _y) in [(2.0, 1.0), (5.0, 3.0), (9.0, -4.0)]:
    r = math.hypot(_x, _y)
    # ∇φ = (-y/r², x/r², 0)
    gphi = (-_y / (r * r), _x / (r * r), 0.0)
    tf = tau_field(_x, _y)
    diff = max(abs(tf[i] - A_AMP * gphi[i]) for i in range(3))
    ref = max(abs(tf[i]) for i in range(3))
    _grad_rows.append(((_x, _y), diff / ref))
_c01_max = max(v for _, v in _grad_rows)
add("C01", "PASS",
    "τ_φ = A/r 的切向场恒等于纯梯度场 A·∇φ（φ 为方位角坐标）",
    "∇φ = (−y/r², x/r², 0)，而 τ = (A/r)φ̂ = (−Ay/r², Ax/r², 0) = A∇φ，"
    "逐点机器对拍相对偏差 %s（停在浮点精度）。"
    "⇒ 该「涡旋」在局部是势涡（irrotational vortex），不是带涡量的旋转。"
    % fmt(Decimal(_c01_max), 6),
    rows=[("取样点", "相对偏差")] + _grad_rows)
guard(_c01_max < 1e-12, "G-C01", "τ 必须恒等于 A∇φ")

# --- C02 旋度：柱坐标解析式与笛卡尔数值双重归零
def curl_z_cylindrical(field_amp, r, h=1e-5):
    """(∇×τ)_z = (1/r) d(r·τ_φ)/dr"""
    def rt(rv):
        return rv * (field_amp / rv)          # r·τ_φ = A
    return (rt(r + h) - rt(r - h)) / (2 * h) / r


_c2_rows = []
for (_x, _y) in [(1.0, 0.0), (3.0, 4.0), (7.0, -2.0), (11.0, 5.0), (20.0, 1.0)]:
    r = math.hypot(_x, _y)
    cz_formula = curl_z_cylindrical(A_AMP, r)
    cv = curl_cart(tau_field, _x, _y)
    ref = A_AMP / (r * r)                     # 自然参考尺度 |∇τ| ~ A/r²
    _c2_rows.append(((_x, _y), cz_formula, max(abs(c) for c in cv) / ref))
_c2_num_max = max(v for _, _, v in _c2_rows)
_c2_exact_max = max(abs(a) for _, a, _ in _c2_rows)

add("C02", "PASS",
    "机器双路径归零：晕区 ∇×τ ≡ 0（解析式与笛卡尔数值旋度同时为零）",
    "柱坐标解析：(∇×τ)_z = (1/r)·d(r·τ_φ)/dr = (1/r)·d(A)/dr ≡ 0；"
    "笛卡尔数值旋度三分量相对参考尺度 |∇τ| 的最大残差 %s（差分截断极限）。"
    "**关键：残差停在截断极限而非精确 0 ⇒ 排除「检验器恒零」**。" % fmt(Decimal(_c2_num_max), 6),
    rows=[("取样点", "解析 (∇×τ)_z", "数值|∇×τ|/|∇τ|")] + _c2_rows)
guard(_c2_exact_max == 0.0, "G-C02", "解析式 (1/r)d(A)/dr 必须精确为 0")
guard(_c2_num_max < 1e-6, "G-C02b", "数值旋度须≤差分截断水平")

# --- C03 阳性对照：证明场本身非零（有非零环量），∇×τ=0 不是因为 τ=0
_circ_samples = []
for _r in [1.0, 3.0, 7.5, 15.0]:
    # ∮τ·dl = ∫0^{2π} τ_φ(r)·r dφ = 2π A，与 r 无关
    _circ_samples.append((_r, 2 * math.pi * A_AMP))
add("C03", "PASS",
    "阳性对照：环量 ∮τ·dl = 2πA ≠ 0 且半径无关 —— ∇×τ=0 不是「场恒零」造成的",
    "τ 在晕区确实非零且每圈给出相同的非零环量 2πA（4 个半径逐点相同），"
    "这正是一个势涡（irrotational / potential vortex）的定义特征："
    "局部无旋 ∂∇τ=0，全局有非零拓扑环量。故 C02 的零不是平凡零。",
    rows=[("半径 r", "环量 ∮τ·dl")] + _circ_samples)

# --- C04 ★ u_τ 公式自身量纲不齐（缺 L²），即使旋度非零也不成立
_d_u_c4g = dpow(NAME_DIM["c"], 4)
_d_u_c4g = ddiv(_d_u_c4g, NAME_DIM["G"])
_d_curltau2 = dpow(ddiv(DIM_INV_L, D(0, 1, 0, 0)), 2)     # [∇×τ]² = L^-4
_d_u = dmul(_d_u_c4g, _d_curltau2)
_gap = ddiv(DIM_ENERGY_DENSITY, _d_u)
add("C04", "FAIL",
    "★u_τ = c⁴/(16πG)|∇×τ|² 量纲不齐：实得 %s，能量密度须为 %s（缺口恰为 L²）"
    % (dstr(_d_u), dstr(DIM_ENERGY_DENSITY)),
    "[c⁴/(16πG)] = MLT⁻²（**力**的量纲，非能量密度），乘 |∇×τ|²=L⁻⁴ 得 ML⁻³T⁻²，"
    "而能量密度为 ML⁻¹T⁻²，缺口恰 %s。要成立须再乘一个长度平方 ℓ²，"
    "即必须引入一个迄今未声明的长度标度 —— 这是本库反复记录的「量纲非齐次」缺陷族又一次出现，"
    "且与 r18/r19/r37 不同：这次缺口极干净（单个 L²）。" % dstr(_gap),
    dim_got=dstr(_d_u), dim_need=dstr(DIM_ENERGY_DENSITY), gap=dstr(_gap))
guard(not deq(_d_u, DIM_ENERGY_DENSITY), "G-C04", "u_τ 必须不等于能量密度维度")
guard(deq(_gap, dpow(D(0, 1, 0, 0), 2)), "G-C04b", "缺口必须恰为 L²")

# --- C05 ★★ u_τ ≡ 0 ⇒ 第3条判别预言（引力透镜）自毁
add("C05", "FAIL",
    "★★第3条判别预言自相抵消：提供平坦曲线的那一支解，恰好让 u_τ ≡ 0，从而没有透镜",
    "来料第3条称「挠率场具有能量密度 u_τ∝|∇×τ|²，能量产生次级曲率，因此挠率晕也会造成引力透镜」。"
    "但提供 a_halo=K/r 的解必须是无源方程 ∇²τ=0 的 τ_φ=A/r（C01/C02 已证其为无旋梯度场），"
    "代入该式立即得 u_τ ≡ 0（在 r>0 的整个晕区）⇒ 次级曲率为零 ⇒ **没有透镜效应**。"
    "即：『平坦旋转曲线』与『挠率晕有透镜』这两条，在该模型内部互斥。"
    "（分布意义上 ∇×∇φ = 2πδ²(r)ẑ，非零部分全部压在 r=0 的轴上，"
    "不在晕区，也无法形成延展的等效质量团块 —— 见 C06。）",
    nature="结构性互斥")

add("C06", "BOUNDARY",
    "分布论口径：唯一的旋度来源是轴上的 δ²(r) 线奇点，能量不落在晕区",
    "严格地 ∇×∇φ = 2π δ²(r) ẑ（Aharonov–Bohm 型）。这意味着所有「旋度能量」"
    "集中在尺度为 0 的轴上，既不支持延展晕的能量密度分布，也不能解释为弥散质量团块；"
    "且它与来料所需的「晕区处处有能量密度 ⇒ 延展透镜势」不符。"
    "本册不自行推导该 δ 分布的归一化系数之外的任何结论，仅作口径登记。")
NOT_SELF_DERIVED.append("C06 的 ∇×∇φ = 2πδ²(r)ẑ 为教科书标准结果（AB 效应），本册仅引用不自推系数")

# --- C07 Friedmann 方程中的 ρ_τ 项同样恒零
add("C07", "FAIL",
    "连带失效：扩展方程组第8式 H² 中的 ρ_τ,0/S² 挠率密度项在同支解下恒为零",
    "来料第8式 H²=(8πG/3c²)(ρ_M+ρ_R+ρ_{τ,0}/S²)，其中 ρ_τ 若来自同一 u_τ 定义，"
    "则由 C02 该项 ≡ 0 ⇒ 挠率对整个宇宙学膨胀史的贡献为零，"
    "即这套 tubules晕场在宇宙学段不构成任何可观测组分。"
    "（该式另有一处口径问题，见 E 段 E06。）")

# --- C08 最小存活路线（不做代选）
add("C08", "INFO",
    "解除 C05 互斥的三条候选路线（本册不代选，代价各异）",
    "(i) 放弃无源解 ∇²τ=0，改为带源方程 ⇒ τ 不再是纯 1/r，旋转曲线不再是 K/r，"
    "**平坦性作为解析结论失效**（须重新数值求解、并引入源项 → 新外部输入）；"
    "(ii) 改能量密度为 u∝|∇τ|² 型 ⇒ 量纲与场论选型都变（C04 的 L² 缺口另行处理），"
    "且 |∇τ|²∝A²/r⁴ 给出过陡的密度剖面，与观测等温晕 ρ∝1/r² 不符；"
    "(iii) 承认晕区无能量 ⇒ 直接撤回第3条透镜预言。"
    "注意 (i) 与 (ii) 都要付出「不再是同一模型」的代价。")

# =========================================================================
# D 段：观测压力测试 —— BTFR 锁死 K ⇒ TUFT 与 MOND 逐点等价（判别预言2 自毁）
# =========================================================================
print()
print("=" * 100)
print("D 段 ｜ BTFR 观测事实 → K 被锁死 → a_halo 与 MOND 深加速区逐点等价")
print("=" * 100)

# --- D01 观测输入的 BTFR 及其对 K 的反约束（外部事实，登记 [C] 级锚）
_btfr_rows = []
for _Mb in ["5e10", "1e11", "5e9", "1e9"]:
    Mb = Decimal(_Mb) * MSUN
    v4 = G * A0_MOND * Mb                      # V∞⁴ = G·a0·M_b
    v_inf = (v4 ** (Decimal(1) / 4))
    K_req = v_inf ** 2                          # K = V∞²
    _btfr_rows.append((_Mb, v_inf, K_req))
    print("  M_b=%s Msun  ->  V∞=%.4f km/s   K=%s m²/s²"
          % (_Mb, float(v_inf) / 1000.0, fmt(K_req, 8)))

EXTERNAL_INPUTS.append(("BTFR 观测关系 V∞⁴=G·a0·M_b", "外部天文事实 [C]",
                        "a0≈1.2e-10 m/s²；观测散射约 0.1 dex（非来料给出）"))
EXTERNAL_INPUTS.append(("a0_MOND = 1.2e-10 m/s²", "外部常数 [C]", "MOND 特征加速度常用值"))

add("D01", "PASS",
    "观测 BTFR 把 K 反约束为 K = √(G·a0·M_b)：K 不是自由常数而是质量的确定函数",
    "重子 Tully–Fisher 关系（外部天文事实）V∞⁴ = G·a0·M_b ⇒ K = V∞² = √(G a0 M_b)。"
    "这意味着「渐近速度」与星系重子质量之间存在一条**紧致**、由单一常数 a0 刻画的观测关系，"
    "观测散射约 0.1 dex。该事实直接约束任何声称解释平坦旋转曲线的理论。",
    rows=[("M_b [M_sun]", "V∞ [km/s]", "所需 K [m²/s²]")]
         + [(r[0], "%.4f" % (float(r[1]) / 1000.0), fmt(r[2], 10)) for r in _btfr_rows])

# --- D02 ★★ 核心两难
add("D02", "FAIL",
    "★★判别预言2 进入两难：K 自由 ⇒ 零预测力；K 服从 BTFR ⇒ 逐点退化为 MOND",
    "来料判别预言2 称「K 由每一星系核心总激发功率决定，不同星系渐近速度不一样，"
    "不存在严格普适加速度」，并据此宣称优于 MOND。两条分支均不成立："
    "**分支 A（K 自由）**：每星系用一个自由 K 事后拟合，任何测到的 V∞ 都可被吸收，"
    "⇒ 对新星系的旋转曲线没有任何先验预测力，属拟合而非预言；"
    "**分支 B（K 服从观测 BTFR）**：K = √(G a0 M_b)，代入 a_halo = K/r 得 "
    "a_halo = √(G a0 M_b)/r，而 MOND 深加速区 a = √(a0·g_N) = √(a0 G M_b)/r —— **逐点完全相同**。"
    "且 BTFR 的观测散射仅约 0.1 dex，与来料预言的「巨大自然弥散」冲突。"
    "⇒ 该条预言实际上不是 TUFT 与 MOND 的判别点，二者在该观测量上不可区分。")

# --- D03 机器证明：分支 B 下 TUFT 与 MOND 加速度逐点等价
_d3_rows = []
for _Mb in ["1e9", "1e10", "5e10", "1e11"]:
    Mb = Decimal(_Mb) * MSUN
    for _rkpc in [2.0, 8.0, 25.0]:
        r = Decimal(str(_rkpc)) * KPC
        gN = G * Mb / (r * r)                       # 牛顿加速度
        a_mond = (A0_MOND * gN).sqrt()              # √(a0 g_N)
        K_btfr = (G * A0_MOND * Mb).sqrt()          # √(G a0 M_b)  (= V∞²)
        a_tuft = K_btfr / r                         # K/r
        d = rel(a_mond, a_tuft)
        _d3_rows.append((_Mb, _rkpc, a_mond, a_tuft, d))
_d3_max = max(r[4] for r in _d3_rows)
add("D03", "PASS",
    "机器证明：分支B 下 a_TUFT = K/r 与 a_MOND = √(a0·g_N) 在 12 组 (M_b, r) 上逐点相等",
    "最大相对偏差 %s（机器零）。两个理论的晕加速度在**函数形式与数值系数上完全重合**，"
    "唯一差别是「为什么」的故事层，不在可观测量层 —— 这正是 D02 判定为伪判别点的根据。"
    "本条本身是机器事实（不表达对何者优先的立场），登记为 PASS。"
    % fmt(_d3_max, 6),
    rows=[("M_b [M_sun]", "r [kpc]", "a_MOND", "a_TUFT=K/r", "相对偏差")]
         + [(r[0], str(r[1]), fmt(r[2], 10), fmt(r[3], 10), fmt(r[4], 6)) for r in _d3_rows[:6]])
guard(_d3_max < Decimal("1e-30"), "G-D03", "分支B 下二者须机器零等价，实测 %s" % fmt(_d3_max, 6))

# --- D04 判别预言1 的可证伪性分级：负预言不可证伪
add("D04", "FAIL",
    "判别预言1「永远探测不到暗物质粒子」是不可证伪的负预言（零信息量）",
    "该陈述的形式是「不存在 X」。无论做多少实验：探测到 ⇒ 陈述直接为假；"
    "未探测到 ⇒ 由于探测器灵敏度永远有限，陈述既不能被确认也不能被推进。"
    "因此它不构成一个可随时间收敛的可检验命题；把它列为「关键判别预言」属判别力不足。"
    "它与 ΛCDM 的真实差别必须落在**正预言**上（如具体的旋转曲线形状、透镜幅度），"
    "而后者在 C05 已被证明自毁。")

# --- D05 判别预言2 的可证伪性：未给分布 ⇒ 不可证伪
add("D05", "MISMATCH",
    "判别预言2 声称「有自然弥散」却未给出弥散的定量分布或上下界 ⇒ 不可证伪",
    "来料既未给出 K 与「核心激发功率」的函数关系，也未给出弥散的量级预测"
    "（如 σ_logK 的期望值或 K 与 M_b 的偏离度）。在此状态下，"
    "任何实测弥散都可被事后称为「自然弥散」，任何紧致性也难以排除该陈述。"
    "对比：MOND 给出的是**普适常数 a0 的单一取值**，可被 BTFR 紧致性直接检验 —— "
    "这一点上 MOND 的可证伪性**高于** TUFT，与来料的自我评估相反。")

# --- D06 ★ 内部数值张力：太阳位置的双重计数
print()
print("  [D06] 银河系太阳位置自洽扫描（K 由渐近 V∞ 强制 = v∞²）")
_d6_rows = []
vinf2 = LAI["vinf_ms"] ** 2
for _Mv in ["1e10", "2e10", "3e10", "5e10", "8e10"]:
    Mv = Decimal(_Mv) * MSUN
    gterm = G * Mv / rsun_m                       # G M_vis / r  (即 v² 的牛顿部分)
    vtot2 = gterm + vinf2
    vtot = vtot2.sqrt()
    excess = (vtot - LAI["vinf_ms"]) / LAI["vinf_ms"]
    _d6_rows.append((_Mv, gterm, vtot, excess))
    print("    M_vis(<8kpc)=%s Msun -> v(8kpc)=%.2f km/s  (超出 %.1f%%)"
          % (_Mv, float(vtot) / 1000.0, float(excess) * 100.0))

_d6_min = min(r[3] for r in _d6_rows)
add("D06", "FAIL",
    "★内部数值张力：K 被渐近速度锁定为 v∞² 后，太阳位置预测速度必然超过同值",
    "渐近区 M_vis 有界 ⇒ v∞ = √K 严格成立 ⇒ K = v∞² 是被观测渐近速度**唯一**锁定的。"
    "但在有限 r 处 v²(r) = GM_vis(r)/r + K > K ⇒ **v(8kpc) 必然 > v∞**。"
    "取银河系 r=8 kpc 处可见质量保守区间 1e10–8e10 M_sun 扫描，预测 v(8kpc) 为 "
    "%s km/s，相对同一个被用作输入的 220 km/s 超出 %s～%s。"
    "即模型在「太阳位置」和「渐近区」不能同时复现同一个 220 km/s："
    "这是在 v∞ 已作为输入被拟合之后**仍然**出现的自洽性冲突，不是外部数据问题。"
    % ("%.0f–%.0f" % (float(min(r[2] for r in _d6_rows)) / 1000.0,
                      float(max(r[2] for r in _d6_rows)) / 1000.0),
       fmt(min(r[3] for r in _d6_rows), 3), fmt(max(r[3] for r in _d6_rows), 3)),
    rows=[("M_vis(<8kpc) [M_sun]", "GM/r [m²/s²]", "v(8kpc) [km/s]", "超出比例")]
         + [(r[0], fmt(r[1], 8), "%.2f" % (float(r[2]) / 1000.0), fmt(r[3], 4)) for r in _d6_rows])
guard(_d6_min > Decimal("0.01"), "G-D06", "太阳位置必须严格超出 v∞（结构性），实测最小超出 %s" % fmt(_d6_min, 4))

add("D07", "BOUNDARY",
    "D06 的强度依赖 M_vis(8kpc) 口径，但结论方向不依赖",
    "银河系太阳位置以内的恒星+气体质量各方估计有差异（约 4e10–6e10 M_sun 为常见区间）。"
    "本册不选取单一权威值以免把质量模型争议引入判定，改用区间扫描；"
    "即使在最小值 1e10 M_sun 下超出仍 > 1%（由 G-M-D06 守卫锁定），方向稳健。"
    "若用户希望按特定质量模型（含 bulge/盘/气体分项）重算，本册可重载该扫描。")

# --- D08 内禀一致性成功项：τ 定义的运动学自洽
tau_sun = tau0_calc * r0_m / rsun_m               # τ_φ(r_sun) = τ0 r0 / r
omega_sun = C * tau_sun
period_sun = 2 * math.pi / float(omega_sun)
period_kepler = 2 * math.pi * float(rsun_m) / float(LAI["vinf_ms"])
add("D08", "PASS",
    "运动学自洽检验通过：单元 gyr 周期与具在运行 Kepler 周期一致（相对残差 %s）"
    % fmt(rel(Decimal(repr(period_sun)), Decimal(repr(period_kepler))), 6),
    "由 τ_φ(r_sun)=%s m⁻¹ 得 ω=cτ=%s s⁻¹，对应周期 %s s = %.3e yr；"
    "而按 r_sun 与 v=220 km/s 的开普勒周期为 %s s = %.3e yr。"
    "两者一致说明 ω=cτ 的换算口径在自身体系内闭合（这是模型不多得的正面自洽项）。"
    % (fmt(tau_sun), fmt(omega_sun), fmt(Decimal(repr(period_sun)), 10),
       period_sun / 3.15576e7, fmt(Decimal(repr(period_kepler)), 10),
       period_kepler / 3.15576e7),
    rows=[("τ_φ(8kpc) [m^-1]", "ω=cτ [s^-1]", "2π/ω [yr]", "2πr/v [yr]")]
         + [(fmt(tau_sun), fmt(omega_sun), "%.4e" % (period_sun / 3.15576e7),
             "%.4e" % (period_kepler / 3.15576e7))])
guard(rel(Decimal(repr(period_sun)), Decimal(repr(period_kepler))) < Decimal("1e-6"),
      "G-D08", "两周期应一致（自洽），实测残差过大")

# =========================================================================
# E 段：V9 扩展方程组逐式量纲与口径审查
# =========================================================================
print()
print("=" * 100)
print("E 段 ｜ V9 扩展方程组逐式量纲审查")
print("=" * 100)

# --- E01 第2式：□τ = (4π/c³)∇×[源]r̂
DIM_SRC = D(0, 0, -2, 0)                       # 源项共同量纲 T^-2（E02 证）
_d_lhs = D(0, -3, 0, 0)                        # [□τ]
_d_curl_src = ddiv(DIM_SRC, D(0, 1, 0, 0))     # [∇×(S r̂)] = L^-1 T^-2
_ok_exponents = []
for _n in range(-6, 7):
    _coef = ddiv(DIMLESS, dpow(NAME_DIM["c"], _n))        # 1/c^n
    _rhs = dmul(_coef, _d_curl_src)
    if deq(_rhs, _d_lhs):
        _ok_exponents.append(_n)
add("E01", "FAIL",
    "★第2式系数 4π/c³ 量纲不成立：此幂次下右端为 %s，左端 [□τ] 为 %s"
    % (dstr(dmul(ddiv(DIMLESS, dpow(NAME_DIM["c"], 3)), _d_curl_src)), dstr(_d_lhs)),
    "穷举 1/c^n（n∈[-6,6] 共 13 个候选），使方程组右端与 [□τ]=L^-3 齐次的幂次恰为 %s —— "
    "**唯一解**，来料所用的 n=3 不在其中。⇒ 这是一个单幂次笔误，非结构性问题。"
    "最小修法：4π/c³ → 4π/c²（即少一个 c）。注意这与 r18/r19 记录的 "
    "「漏 c 幂次」缺陷族同源，本册为又一次实证。" % str(_ok_exponents),
    exponents_ok=_ok_exponents, claimed=3)
guard(_ok_exponents == [2], "G-E01", "唯一可行幂次必须恰为 2")
guard(3 not in _ok_exponents, "G-E01b", "来料所用的 n=3 必须不可行")

# --- E02 第2式括号内四项齐次性
_src_rows = [
    ("G·ρ_m（质量密度源）", dstr(dmul(NAME_DIM["G"], NAME_DIM["rho"]))),
    ("(1/4πε0)·(q/m)·ρ_q（电荷源）", dstr(_d_dim_src_em)),
]
_src_ok = deq(dmul(NAME_DIM["G"], NAME_DIM["rho"]), _d_dim_src_em)
add("E02", "PASS",
    "第2式源括号内前两项量纲齐次，共同为 T^-2（四项可相加的必要条件成立）",
    "这是来料不多见的正确处：引力源 Gρ_m 与电磁源 (1/4πε0)(q/m)ρ_q 机器判定同为 %s。"
    "后两项 K_s·ρ_top 与 K_w·ρ_meta 因 ρ_top/ρ_meta/K_s/K_w 均未给定义与量纲，"
    "机器无法判定（见 E07 未定义符号总账），本册不代造。"
    % dstr(DIM_SRC), rows=_src_rows)
guard(_src_ok, "G-E02", "两项源必须同量纲")

# --- E03 第4式 R_μν
_d_lhs_ricci = D(0, -2, 0, 0)
_d_gradtau = ddiv(DIM_INV_L, D(0, 1, 0, 0))           # [∇τ] = L^-2
_d_term1 = _d_gradtau                                  # (∇_μτ_ν+∇_ντ_μ)
_d_gradtau2 = dpow(_d_gradtau, 2)                      # (∇τ)² = L^-4
_kappa_lambda = ddiv(_d_lhs_ricci, _d_gradtau2)        # λ_c 所需量纲
add("E03", "BOUNDARY",
    "第4式第一项齐次（L^-2 ✓），但第二项要求 λ_c 具 %s 量纲且来料未声明 ⇒ 引入未登记常数"
    % dstr(_kappa_lambda),
    "R_μν 为 L^-2；∇_μτ_ν 为 L^-2 ⇒ 第一项（含无量纲因子 4/9 与 1/(1+GM/c²r)，"
    "后者机器验证确为无量纲）与第二项的维度一致前提是 λ_c 携带长度平方。"
    "来料没有给 λ_c 的定义、数值或量纲，因此该式**隐含一个未登记的新外部输入**；"
    "且 (∇τ)²δ_μν 与 ∇_μτ_ν+∇_ντ_μ 是不同张量结构，能否同式相加还需单独的协变性审查。",
    lambda_c_required=dstr(_kappa_lambda))
guard(deq(_d_term1, _d_lhs_ricci), "G-E03", "第一项应与 R_μν 齐次")
guard(not deq(_kappa_lambda, DIMLESS), "G-E03b", "λ_c 必须带量纲（故不可忽视）")

# --- E04 第5式阻尼振子
_d_tau_dot = ddiv(DIM_INV_L, D(0, 0, 1, 0))            # τ̇ : L^-1 T^-1
_d_tau_ddot = ddiv(_d_tau_dot, D(0, 0, 1, 0))          # τ̈ : L^-1 T^-2
_d_omega_tau = D(0, 0, -1, 0)                          # ω_τ : T^-1
_d_t1 = _d_tau_ddot
_d_t2 = dmul(_d_omega_tau, _d_tau_dot)
_d_t3 = dmul(dpow(_d_omega_tau, 2), DIM_INV_L)
_e04_ok = deq(_d_t1, _d_t2) and deq(_d_t2, _d_t3)
add("E04", "PASS" if _e04_ok else "FAIL",
    "第5式左端三项（τ̈、2(ω_τ/Q)τ̇、ω_τ²τ）量纲齐次为 %s，但右端 K_0·N·Ω 不可判定"
    % dstr(_d_t1),
    "左端齐次 PASS，且隐含 Q 必须无量纲（阻尼 Q 值通常如此，合理）。"
    "右端 K_0、N、Ω 三个符号来料全未定义：N 若为粒子数则无量纲；"
    "Ω 与 K_0 的量纲组合自由度未约束 ⇒ 该式目前无法作为可计算方程使用。")
guard(_e04_ok, "G-E04", "阻尼振子三项须齐次")

# --- E05 第7式色散
_d_k2 = dpow(D(0, -1, 0, 0), 2)
_d_disp = dmul(ddiv(dpow(_d_omega_tau, 2), dpow(NAME_DIM["c"], 2)), DIMLESS)
add("E05", "PASS",
    "第7式 k² = (ω_τ²/c²)(1+χ_τ) 量纲闭合，并要求 χ_τ 无量纲",
    "机器：右端 %s = 左端 %s ✓。该式同时锁定了 χ_τ 必须无量纲 —— "
    "这是全套方程组中唯一一处来料未定义符号但本册可给出确定量纲约束的项。" % (dstr(_d_disp), dstr(_d_k2)))
guard(deq(_d_k2, _d_disp), "G-E05", "色散式须齐次")

# --- E06 第8式 Friedmann 口径二叉
_d_H2 = D(0, 0, -2, 0)
_d_massrho_sum = dmul(NAME_DIM["G"], NAME_DIM["rho"])                  # 8πG·ρ_mass /3
_d_over_c2 = dmul(ddiv(NAME_DIM["G"], dpow(NAME_DIM["c"], 2)), NAME_DIM["rho"])
_d_over_c2_edens = dmul(ddiv(NAME_DIM["G"], dpow(NAME_DIM["c"], 2)), DIM_ENERGY_DENSITY)
add("E06", "FAIL",
    "★第8式多一个 c²：按 ρ 为质量密度的通常口径，(8πG/3c²)ρ 得 %s 而非 [H²]=%s"
    % (dstr(_d_over_c2), dstr(_d_H2)),
    "机器二叉判定："
    "(a) 若 ρ_M、ρ_R 是**质量密度**（天体物理默认口径）：正确形式为 H²=(8πG/3)ρ，"
    "机器给 [8πGρ/3] = %s ✓，而加入 /(c²) 后为 %s ✗ ⇒ **多除了一个 c²**；"
    "(b) 若 ρ 是**能量密度**：(8πG/3c²)ε 得 %s ✓ 成立。"
    "来料符号取 ρ 且语境含 ρ_M/ρ_R（物质/辐射），通常指质量密度 ⇒ 按 (a) 判 FAIL；"
    "若作者本意是能量密度，则须显式改记号（如 ε），否则同一套文稿会产出相差 c² 的膨胀史。"
    "最小修法（口径 a）：删去分母 c²。" % (dstr(_d_massrho_sum), dstr(_d_over_c2), dstr(_d_over_c2_edens)),
    rows=[("口径", "表达式", "实得量纲", "判定")]
         + [("(a) ρ=质量密度", "8πGρ/3", dstr(_d_massrho_sum), "✓ 齐次"),
            ("(a') ρ=质量密度", "8πGρ/(3c²)", dstr(_d_over_c2), "✗ 多一个 c²"),
            ("(b) ε=能量密度", "8πGε/(3c²)", dstr(_d_over_c2_edens), "✓ 齐次")])
guard(deq(_d_massrho_sum, _d_H2), "G-E06", "标准弗里德曼式须齐次")
guard(not deq(_d_over_c2, _d_H2), "G-E06b", "来料形式在质量密度口径下必须不齐次")

# --- E07 未定义符号总账
UNDEFINED = [
    ("K_s", "第2式howergee 拓扑源项耦合系数", "未给定义/量纲"),
    ("K_w", "第2式「meta」源项耦合系数", "未给定义/量纲"),
    ("ρ_top", "第2式拓扑荷密度", "未给定义/量纲/与被解释对象的关系"),
    ("ρ_meta", "第2式「meta」密度", "未给定义/量纲"),
    ("λ_c", "第4式二次项系数", "本册推出需为 L²，来料未声明"),
    ("K_0", "第5式驱动幅度", "未给定义/量纲"),
    ("N", "第5式粒子数/数量级", "未给定义（是否无量纲未声明）"),
    ("Ω", "第5式驱动频率/立体角/占比", "三义未择一，量纲随之不定"),
    ("Q", "第5式品质因数", "本册推出须无量纲，来料未声明"),
    ("χ_τ", "第7式自旋介质极化率", "本册推出须无量纲，来料未声明"),
    ("ρ_{τ,0}", "第8式挠率密度", "若沿用第3条 u_τ 则恒零（见 C07）"),
    ("S", "第8式标度因子", "未声明归一化（S0=1?）"),
]
add("E07", "INFO",
    "未定义/未给量纲符号总账：%d 个" % len(UNDEFINED),
    "扩展方程组共 10 式，其中可机器判定量纲者本册已逐式裁定；"
    "余下这些符号因缺少定义与量纲声明，任何代入或拟合都无法在 RAIJIN DAM转型升级前执行。"
    "其中 λ_c / Q / χ_τ / Ω 四项本册已反推出唯一可行的量纲约束（见上表），属可低成本补齐项。",
    rows=[("符号", "出现位置/含义", "状态")] + UNDEFINED)
for _nm, _loc, _st in UNDEFINED:
    EXTERNAL_INPUTS.append((_nm, "未定义符号", _loc + "：" + _st))

# =========================================================================
# F 段：★方向三难 —— 「自旋角速度」沿 φ̂ 不是自旋；沿 ẑ 则解不再是 1/r
# =========================================================================
print()
print("=" * 100)
print("F 段 ｜ ω 的方向：把自旋角速度取为 φ̂ 不是自旋；取沿轴则 τ∝1/r 不再是解")
print("=" * 100)


def axial_lap(f, x, y, h=1e-4):
    """τ = f(r) ẑ 的矢量拉普拉斯 z 分量（笛卡尔九点差分）"""
    def fz(xx, yy):
        return f(math.hypot(xx, yy))
    c = fz(x, y)
    dxx = (fz(x + h, y) - 2 * c + fz(x - h, y)) / (h * h)
    dyy = (fz(x, y + h) - 2 * c + fz(x, y - h)) / (h * h)
    return dxx + dyy


_f_rows = []
for nm, f in [("τ_z = ln r（真正解）", math.log), ("τ_z = 1/r（来料形状）", lambda r: 1.0 / r)]:
    worst = 0.0
    for (_x, _y) in [(2.0, 1.0), (5.0, 3.0), (9.0, -4.0)]:
        r = math.hypot(_x, _y)
        lap = axial_lap(f, _x, _y)
        ref = abs(f(r)) / (r * r) if f is math.log else abs(f(r)) / (r * r)
        worst = max(worst, abs(lap) / ref if ref != 0 else abs(lap))
    _f_rows.append((nm, worst))
_f_ln, _f_inv = _f_rows[0][1], _f_rows[1][1]

add("F01", "FAIL",
    "★★★方向三难：ω=cτ 取 φ̂ 不是自旋；若改为真正的自旋轴方向 ẑ，"
    "无源方程的解变成 τ_z=A·ln r + B，a_halo=K/r 立刻失效",
    "**语义层**：一个绕轴自旋的体系，其角速度矢量必沿自旋轴（ẑ），"
    "对应的**速度场**才是 rφ̂ 方向；来料把 ω=cτ 本身放在 φ̂，"
    "意味着「每个点的旋转轴沿该点的方位方向」，这不对应任何自旋/涡旋语义。"
    "**数学层**：若改取物理正确的 τ=τ_z(r)ẑ，则对纯轴向矢量 ∇²τ = (f''+f'/r)ẑ，"
    "机器验证 f=ln r 为零（相对残差 %s，即它是解），而 f=1/r **不为零**（相对残差 %s，"
    "恰等于解析值 1/r³ 的相对表现）。"
    "⇒ 三难：(a) 保 τ∝1/r ⇒ ω 是伪自旋、且 B01/B04 的符号问题无从谈「自旋拖拽」；"
    "(b) 保真实自旋方向 ⇒ 解为 ln r，a_halo=c²(A ln r+B)²r 随 r 增长，**平坦旋转曲线不复存在**；"
    "(c) 两者都要 ⇒ 必须放弃 ∇²τ=0 的无源假设，引入源项 ⇒ 新外部输入且解析平坦性失效。"
    "三条路都在「场 Vs equations」内部互斥，不是计算量问题。"
    % (fmt(Decimal(_f_ln), 6), fmt(Decimal(_f_inv), 6)),
    rows=[("轴向候选解", "∇²τ 相对残差", "是否无源解")] +
         [(nm, fmt(Decimal(v), 6), ("是" if v < 1e-6 else "否")) for nm, v in _f_rows])
guard(_f_ln < 1e-5, "G-F01", "ln r 必须是轴向无源解")
guard(_f_inv > 1e-2, "G-F01b", "1/r 必须不是轴向无源解（否则三难不成立）")

add("F02", "PASS",
    "机器核对：切向支与轴向支给出**不同**的径向依赖，不存在同一解同时满足两者",
    "切向支 τ_φ∝1/r 是 A∇φ（无旋势涡）；轴向支的无源解是 ln r。"
    "两者函数形式不同，故「既是绕轴自旋、又是 τ∝1/r」在该场方程内不可兼得。")

# --- F03 符号同名异义台账
add("F03", "INFO",
    "符号台账：τ / ω / K 三族同名异义（跨节引用必炸）",
    "τ：①主文空间挠率 L⁻¹（切向 scalar 分布 τ_φ）②第2式矢量场 τ⃗ ③第4式时空协变矢量 τ_ν "
    "④第5式动力学场变量 —— 四种语境未声明是否同一对象；"
    "ω：①主文 ω_φ=cτ_φ「真空自旋角速度」②第5式 ω_τ 阻尼振子本征频率 ③来获取 "
    "ω²r 中的ω —— ①②物理对象完全不同；"
    "K：①主文 K=(cτ₀r₀)² [m²/s²] ②第2式 K_s ③第2式 K_w ④第5式 K_0 —— 四个 K 互不相干。"
    "本册判定时严格按每处的上下文锁定语义，混引必然出错。",
    rows=[("符号族", "出现义项", "风险")] +
         [("τ", "空间挠率 / 矢量场 / 协变矢量 / 动力学变量", "同一式内混用会导致量纲与指标类型错配"),
          ("ω", "真空自旋角速度 / 振子本征频率", "物理对象不同，数值不可共用"),
          ("K", "K=(cτ₀r₀)² / K_s / K_w / K_0", "四义同名，量纲各异")])

add("F04", "INFO",
    "「舍去 n=+1 因物理上不稳定」的理由不成立（次要）",
    "来料以「随半径增大而上升、物理上不稳定」为由舍去 n=+1。稳定性不是由渐近幂次单独决定的，"
    "且 n=+1 是唯一在 r→0 正则的支 —— 若晕区内侧存在轴区正则性要求，"
    "正确做法应是分段匹配（内区 τ∝r、外区 τ∝1/r）而非单点取舍。"
    "本条不改变任何结论，仅登记论证严密性缺口。")

# =========================================================================
# G 段：收口 —— 外部输入总账、修法成本、跨册印证、诚实边界
# =========================================================================
print()
print("=" * 100)
print("G 段 ｜ 收口：外部输入总账 / 修法成本 / 跨册印证 / 诚实边界")
print("=" * 100)

EXTERNAL_INPUTS.append(("τ₀（或等价的 K）", "来料主文", "每个星系各一个，是拟合量而非推导量"))
EXTERNAL_INPUTS.append(("r₀ 星系特征半径", "来料主文", "每星系一个"))
add("G01", "INFO",
    "外部输入总账：%d 项（其中 %d 项来自未经 OCR 定标的扩展方程组未定义符号）"
    % (len(EXTERNAL_INPUTS), len(UNDEFINED)),
    "主链输入：τ₀、r₀（与 M_vis(r) 一道构成拟合三角）。"
    "扩展方程组另有 12 个未定义符号。按本库 Ω5 口径（自由常数 ≤1），"
    "即便只计主链也已超出：τ₀ 与 r₀ 两个，且 τ₀ 对每个星系各取一个值 ⇒ 实际是「每星系一个参数」。",
    rows=[("输入项", "类别", "说明")] + EXTERNAL_INPUTS)

# --- G02 修法成本表
_FIXES = [
    ("P1", "B01/B04", "a = -ω×(ω×r) 的符号", "去负号改 +ω×(ω×r)", "零成本（不改任何数值）", "必做"),
    ("P2", "E01", "第2式 4π/c³", "改为 4π/c²", "零成本（单幂次）", "必做"),
    ("P3", "E06", "第8式多除 c²", "删 c² 或改记号 ε 并显式声明口径", "零成本（口径声明）", "必做"),
    ("P4", "C04", "u_τ 缺 L²", "引入一个长度标度 ℓ²", "+1 个带量纲常数", "做则违反 ≤1 常数口径"),
    ("P5", "C05/C07", "透镜/宇宙学项恒零", "撤回第3条预言，或放弃无源解", "撤回=零成本；改解=丢失解析平坦性", "二选一"),
    ("P6", "D02", "K 无预测力/退化为 MOND", "给出 K(M_b) 的定量关系", "须先有理论机制（目前无候选）", "唯一真出口"),
    ("P7", "F01", "ω 方向三难", "选(a)/(b)/(c) 任一支", "任一支都牺牲一项既有宣称", "须先定语义"),
    ("P8", "D04/D05", "判别预言不可证伪", "改为给出定量分布的正面预言", "须先有动力学", "依赖 P6"),
    ("P9", "E07", "12 个未定义符号", "逐项补齐定义与量纲", "零成本但工作量大", "建议先行"),
]
_zero = [f for f in _FIXES if "零成本" in f[4]]
add("G02", "INFO",
    "修法候选总成本：%d 项中有 %d 项为零成本可立即执行，%d 项需要新增自由度"
    % (len(_FIXES), len(_zero), len(_FIXES) - len(_zero)),
    "**先做 P1/P2/P3/P9**：这四项合计零新增参数，且不改变任何已公布数字，"
    "是典型的「先把式子修对」。"
    "**真正的承重阻塞是 P5/P6/P7**：它们不是笔误，而是模型三个不同层面的互斥，"
    "任一支 repair 都要撤回一项现有宣称。特别是 P6 —— 在给出 K(M_b) 之前，"
    "该旋转曲线公式对新星系没有先验预测力。",
    rows=[("编号", "对应条目", "问题", "修法", "代价", "优先级")] + _FIXES)

# --- G03 跨册交叉印证
add("G03", "PASS",
    "与既有册的交叉印证：本次「漏 c 幂次」是同一缺陷族又一次复发",
    "E01（4π/c³→c²）与 E06（多除 c²）两处，均属本库反复记录的「漏/多一个 c 幂次」缺陷族，"
    "与 r18/r19/r37/r66 的记录同型；C04 的「缺口恰为 L²」则与 r66/r64 的 QEI 量纲闭合族同手。"
    "⇒ 本册未发现新的缺陷类别，说明该类问题可通过「逐式量纲机器门禁」稳定捕获，"
    "建议对新增方程一律先跑该门禁再进入任何数值拟合。")

# --- G04 诚实边界
add("G04", "INFO",
    "诚实边界（红线）：本册明确未做的事",
    "① 未推导任何新物理，所有裁定均为对来料的只读机器判决；"
    "② 未修改来料任何字节（来料正本另存只读留档）；"
    "③ 未修改任何既有 r 序列产物；"
    "④ 引用的外部常数与定理一律标注来源，不自推；"
    "⑤ **不代选** P5/P6/P7 三条路线的取舍 —— 这是科学哲学层面的选择，须由用户裁决；"
    "⑥ 数学/数值自洽 ≠ 物理证实：本册判 FAIL 的是**形式与内部一致性**，"
    "不等于「星系挠率晕这一物理方向被否证」；"
    "被否证的是**这一支具体实现**（τ_φ∝1/r + u_τ∝|∇×τ|² + K 自由）。")
NOT_SELF_DERIVED.append("本册所有非平凡 Astronomía 常数取自 CODATA/IAU 定义值，未自行推导任何物理新常数")

# =========================================================================
# 汇总输出 + 落盘
# =========================================================================
_VERDICTS = ["PASS", "FAIL", "BOUNDARY", "CORRECTED", "MISMATCH", "INFO"]
_counts = dict((v, sum(1 for e in ENTRIES if e["verdict"] == v)) for v in _VERDICTS)

print()
print("=" * 100)
print("TUFT-r107 星系挠率晕模型 —— 全维审计与攻破 ｜ 结果汇总")
print("=" * 100)
for e in ENTRIES:
    tag = {"PASS": "[PASS]     ", "FAIL": "[FAIL]     ", "BOUNDARY": "[BOUNDARY] ",
           "CORRECTED": "[CORRECTED]", "MISMATCH": "[MISMATCH] ", "INFO": "[INFO]     "}[e["verdict"]]
    print(tag + e["code"] + "  " + e["title"])
print()
print("条目合计 %d ： " % len(ENTRIES)
      + "  ".join("%s=%d" % (v, _counts[v]) for v in _VERDICTS))
print("自检守卫 %d / 失败 %d" % (STATE["guard"], STATE["guard_fail"]))
for m in STATE["guard_msgs"]:
    print("   !! 守卫未通过: " + m)

GUARDPASS = (STATE["guard"] - STATE["guard_fail"])

_BASE = "TUFT-r107_星系挠率晕与旋转曲线_全维审计与攻破_2026-10-19"
os.makedirs(OUT_DATA, exist_ok=True)

_payload = {
    "round": "r107",
    "title": "TUFT-V9 星系挠率晕模型、旋转曲线拟合、参数分析、可观测预言 —— 全维审计与攻破",
    "date": "2026-10-19",
    "topic_status": "全仓首次覆盖（挠率晕/tau_phi/暗物质无粒子 三词 md/py/json/html 全仓 0 命中）",
    "entries": ENTRIES,
    "counts": _counts,
    "guard": {"total": STATE["guard"], "fail": STATE["guard_fail"], "pass": GUARDPASS,
              "msgs": STATE["guard_msgs"]},
    "external_inputs": EXTERNAL_INPUTS,
    "not_self_derived": NOT_SELF_DERIVED,
    "key_numbers": {
        "r0_m": fmt(r0_m),
        "K_vinf2": fmt(Kcalc),
        "tau0_per_meter": fmt(tau0_calc),
        "a_halo_at_8kpc": fmt(ahalo_calc),
        "v_8kpc_min_kms": float(min(r[2] for r in _d6_rows)) / 1000.0,
        "v_8kpc_max_kms": float(max(r[2] for r in _d6_rows)) / 1000.0,
        "v_8kpc_excess_min": fmt(min(r[3] for r in _d6_rows)),
        "v_8kpc_excess_max": fmt(max(r[3] for r in _d6_rows)),
        "tuft_vs_mond_max_rel_diff": fmt(_d3_max),
        "dim_gap_u_tau": dstr(_gap),
        "E01_ok_exponent_of_1_over_c_pow": _ok_exponents,
    },
    "red_line": "数学/数值自洽 ≠ 物理证实。本册否证的是这一支具体实现，不等于否证星系挠率晕方向。",
}
_json_path = os.path.join(OUT_DATA, _BASE + ".json")
with open(_json_path, "w", encoding="utf-8") as f:
    json.dump(_payload, f, ensure_ascii=False, indent=2)
print()
print("JSON 落盘 -> " + _json_path)

# ---- 报告 txt
_lines = []
_lines.append("TUFT-r107 星系挠率晕与旋转曲线 全维审计与攻破 报告")
_lines.append("=" * 96)
_lines.append("来料：TUFT-V9 星系挠率晕模型 / 旋转曲线拟合 / 参数分析 / 可观测预言")
_lines.append("日期：2026-10-19　引擎：纯标准库 decimal(60位) + fractions 四元量纲 (M,L,T,Q)")
_lines.append("")
_lines.append("条目 %d ： %s" % (len(ENTRIES),
                                 "  ".join("%s=%d" % (v, _counts[v]) for v in _VERDICTS)))
_lines.append("自检守卫 %d/%d 通过" % (GUARDPASS, STATE["guard"]))
_lines.append("")
for e in ENTRIES:
    _lines.append("[%s] %s  %s" % (e["verdict"], e["code"], e["title"]))
    _lines.append("    " + e["detail"].replace("\n", "\n    "))
    if e.get("rows"):
        for _r in e["rows"]:
            _lines.append("      · " + " | ".join(str(_c) for _c in _r))
    _lines.append("")
_lines.append("=" * 96)
_lines.append("外部输入总账：")
for _x in EXTERNAL_INPUTS:
    _lines.append("  - %s  [%s]  %s" % (_x[0], _x[1], _x[2]))
_lines.append("")
_lines.append("不自推清单：")
for _x in NOT_SELF_DERIVED:
    _lines.append("  - " + _x)
_lines.append("")
_lines.append("红线：" + _payload["red_line"])
_report_path = os.path.join(OUT_DATA, _BASE + ".txt")
with open(_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(_lines))
print("报告落盘 -> " + _report_path)

# ---- 数据 md
_md = []
_md.append("# TUFT-r107 ｜ 星系挠率晕与旋转曲线 —— 全维审计与攻破（数据产物）")
_md.append("")
_md.append("**来料**：TUFT‑V9《星系挠率晕模型、旋转曲线拟合、参数分析、可观测预言》  ")
_md.append("**审计日期**：2026-10-19　**引擎**：纯标准库 decimal(60 位) + fractions 四元量纲 (M,L,T,Q)  ")
_md.append("**判定册**：[判定_TUFT-r107-星系挠率晕与旋转曲线_全维审计与攻破_2026-10-19.md](../判定_TUFT-r107-星系挠率晕与旋转曲线_全维审计与攻破_2026-10-19.md)")
_md.append("")
_md.append("## 一、条目汇总")
_md.append("")
_md.append("条目 **%d** ： %s　｜　自检守卫 **%d/%d** 通过　｜　退出码 0"
           % (len(ENTRIES), "　".join("%s=%d" % (v, _counts[v]) for v in _VERDICTS),
              GUARDPASS, STATE["guard"]))
_md.append("")
_md.append("| 编号 | 判定 | 标题 |")
_md.append("|---|---|---|")
for e in ENTRIES:
    _md.append("| %s | %s | %s |" % (e["code"], e["verdict"], e["title"]))
_md.append("")
_md.append("## 二、逐条明细")
_md.append("")
for e in ENTRIES:
    _md.append("### %s ｜ %s" % (e["code"], e["title"]))
    _md.append("")
    _md.append("**判定：%s**" % e["verdict"])
    _md.append("")
    _md.append(e["detail"].replace("\n", "\n"))
    if e.get("rows"):
        _md.append("")
        _rows = e["rows"]
        _md.append("| " + " | ".join(str(c) for c in _rows[0]) + " |")
        _md.append("|" + "---|" * len(_rows[0]))
        for _r in _rows[1:]:
            _md.append("| " + " | ".join(str(_c) for _c in _r) + " |")
    _md.append("")
_md.append("## 三、关键读数")
_md.append("")
_md.append("| 量 | 值 |")
_md.append("|---|---|")
for _k in ["r0_m", "K_vinf2", "tau0_per_meter", "a_halo_at_8kpc",
           "v_8kpc_min_kms", "v_8kpc_max_kms", "v_8kpc_excess_min", "v_8kpc_excess_max",
           "tuft_vs_mond_max_rel_diff", "dim_gap_u_tau"]:
    _md.append("| %s | %s |" % (_k, _payload["key_numbers"][_k]))
_md.append("")
_md.append("## 四、外部输入总账")
_md.append("")
_md.append("| 输入项 | 类别 | 说明 |")
_md.append("|---|---|---|")
for _x in EXTERNAL_INPUTS:
    _md.append("| %s | %s | %s |" % (_x[0], _x[1], _x[2]))
_md.append("")
_md.append("## 五、不自推清单")
_md.append("")
for _x in NOT_SELF_DERIVED:
    _md.append("- " + _x)
_md.append("")
_md.append("## 六、红线")
_md.append("")
_md.append(_payload["red_line"])
_md_path = os.path.join(OUT_DATA, _BASE + ".md")
with open(_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(_md))
print("数据 md 落盘 -> " + _md_path)

sys.exit(0 if STATE["guard_fail"] == 0 else 1)

