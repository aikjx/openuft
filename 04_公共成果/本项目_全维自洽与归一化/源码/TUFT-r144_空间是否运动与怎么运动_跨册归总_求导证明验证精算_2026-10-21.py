# -*- coding: utf-8 -*-
"""
TUFT-r144  空间是否运动与怎么运动 · 跨册归总  求导证明验证与精算分析
====================================================================

性质
----
**本引擎不产生新物理。** 它只做两件事：

1. **求导证明（D1-D3）**——用「解析闭式 vs 中心差分数值」双路径对拍，验证
   跨册归总正本 `整理_空间是否运动与怎么运动_跨册归总_2026-10-21.md` 中
   引用的三条关系式在机器精度下确实成立（从而排除「来料公式写错」这一
   低级错误，把讨论抬到物理层）。
2. **精算复拍（N1-N6）**——对既有册的公开读数做独立高精度复算，复现或
   证否其数值；不新推任何系数、不新提任何方程。

判别力声明（必须连同结果引用）
------------------------------
D1/D2 通过**只证明「确实构造了一条螺旋线」**，**不构成对 P1 物理成立的证据**。
`κ²+τ²=(ω/c)²` 与 `κ/τ=v_θ/v_z` 是 Frenet-Serret 标架的定义式推论，
对任意螺旋线恒真、零信息量（正本 §1.1、§8 模式 1/2）。

工具
----
- `decimal.Decimal`，精度 60 位
- `fractions.Fraction` 四元组量纲 `(M, L, T, Q)`
- 自实现高精度 `dsin/dcos`（Decimal 无三角函数；r22/r59 已踩），并配
  **已知特殊角守卫** G0-7/G0-8（r59 教训：自实现级数必须先过已知角守卫）
- 量纲工具自身先过 guard（历史上量纲代数写成「逐分量相乘」已被拦下多次）

出处
----
P1 读数：r95 / S01 全维三重奏；P2 读数：r64 / r66 / r67；
ringdown：OPEN_v3；g-2 / EDM：OPEN5 / OPEN6 / ACME2018。

复现：`python 源码/_run_r144.py`
"""

from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "数据")
STAMP = "2026-10-21"
NAME = "TUFT-r144_空间是否运动与怎么运动_跨册归总_求导证明验证精算_" + STAMP

# ---------------------------------------------------------------- 高精度常量

PI = Decimal(
    "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803483"
)

C = Decimal("299792458")                       # m/s
G = Decimal("6.67430e-11")                     # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")              # J s
ALPHA = Decimal("7.2973525693e-3")             # 精细结构常数
M_SUN = Decimal("1.98892e30")                  # kg
M_UNIV = Decimal("1.5e53")                     # kg，可观测宇宙质量（量级参照）
LP = (HBAR * G / (C ** 3)).sqrt()              # 普朗克长度（自洽推导，仅用于 guard）
LP_NOM = Decimal("1.616255e-35")               # CODATA 标称普朗克长度（r66/r67 同口径）
E_CM_PER_CM = Decimal("1.602176634e-19")       # 1 e = 1.602176634e-19 C（e·cm 换算用）

# ---------------------------------------------------------------- 量纲工具


def D(m=0, l=0, t=0, q=0):
    """四元组量纲 (M, L, T, Q)，分量为 Fraction。"""
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


DIM_ENERGY_DENSITY = D(1, -1, -2, 0)   # M L^-1 T^-2
DIM_MASS_DENSITY = D(1, -3, 0, 0)      # M L^-3
DIM_TIME = D(0, 0, 1, 0)
DIM_LENGTH = D(0, 1, 0, 0)
DIM_NONE = D(0, 0, 0, 0)


def dmul(a, b):
    """量纲相乘 = 指数相加（写成逐分量相乘是本库历史事故，勿犯）。"""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def ddiv(a, b):
    """量纲相除 = 指数相减。"""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])


def dpow(a, n):
    return (a[0] * Fraction(n), a[1] * Fraction(n), a[2] * Fraction(n), a[3] * Fraction(n))


def _sup(n):
    return {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5",
            6: "6", 7: "7", 8: "8", 9: "9"}.get(abs(int(n)), str(abs(int(n))))


def dstr(a):
    """量纲字符串，如 M^1 L^-1 T^-2。负指数渲染为 ^-n（勿写成 ^--n）。"""
    sym = ("M", "L", "T", "Q")
    out = []
    for i in range(4):
        v = a[i]
        if v == 0:
            continue
        if v == 1:
            out.append(sym[i])
        else:
            iv = int(v)
            out.append(sym[i] + "^" + ("-" + _sup(iv) if iv < 0 else _sup(iv)))
    return " ".join(out) if out else "1"


# ---------------------------------------------------------------- 高精度三角


def _reduce(x):
    two = PI * 2
    n = (x / two).to_integral_value(rounding=ROUND_FLOOR)
    return x - n * two


def dsin(x):
    """Decimal 泰勒级数 sin，先约简到 [0, 2pi)。"""
    x = _reduce(x)
    term = x
    s = x
    n = 1
    while n < 400:
        term = -term * x * x / ((2 * n) * (2 * n + 1))
        s = s + term
        if abs(term) < Decimal("1e-70"):
            break
        n += 1
    return s


def dcos(x):
    x = _reduce(x)
    term = Decimal(1)
    s = Decimal(1)
    n = 1
    while n < 400:
        term = -term * x * x / ((2 * n - 1) * (2 * n))
        s = s + term
        if abs(term) < Decimal("1e-70"):
            break
        n += 1
    return s


def dsqrt(x):
    return x.sqrt()


# ---------------------------------------------------------------- 数值导数


def vec_sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def vec_add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def vec_scale(a, k):
    return [a[0] * k, a[1] * k, a[2] * k]


def vec_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def vec_norm(a):
    return vec_dot(a, a).sqrt()


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def helix_point(u, R, a):
    """圆柱螺旋（以无量纲相位 u = omega*t 为参数）：(R cos u, R sin u, a u)。"""
    return [R * dcos(u), R * dsin(u), a * u]


def helix_derivs_numeric(u, R, a, h):
    """中心差分求 r', r'', r'''（对参数 u）。全部 O(h^2)。"""
    p2 = helix_point(u + 2 * h, R, a)
    p1 = helix_point(u + h, R, a)
    p0 = helix_point(u, R, a)
    m1 = helix_point(u - h, R, a)
    m2 = helix_point(u - 2 * h, R, a)
    d1 = vec_scale(vec_sub(p1, m1), Decimal(1) / (2 * h))
    # f'' ~ [f(+h) - 2f(0) + f(-h)] / h^2   （写成 p1 - m1 - 2p0 是错的，已修）
    d2 = vec_scale(vec_add(vec_add(p1, m1), vec_scale(p0, Decimal(-2))),
                   Decimal(1) / (h * h))
    # f''' ~ [f(+2h) - 2f(+h) + 2f(-h) - f(-2h)] / (2 h^3)
    num = vec_add(vec_sub(p2, vec_scale(p1, Decimal(2))),
                  vec_sub(vec_scale(m1, Decimal(2)), m2))
    d3 = vec_scale(num, Decimal(1) / (2 * h * h * h))
    return d1, d2, d3


def kappa_tau_from_derivs(d1, d2, d3):
    cr = vec_cross(d1, d2)
    k = vec_norm(cr) / (vec_norm(d1) ** 3)
    t = det3(d1, d2, d3) / vec_dot(cr, cr)
    return k, t


# ---------------------------------------------------------------- 记录设施

ENTRIES = []
GUARDS = []


def add(code, status, title, detail):
    ENTRIES.append({"code": code, "status": status, "title": title, "detail": detail})


def guard(name, ok, info=""):
    GUARDS.append({"name": name, "ok": bool(ok), "info": info})
    return bool(ok)


def fv(x, n=25):
    """定点科学计数字符串（Decimal.quantize 在高位数会抛 InvalidOperation）。"""
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        try:
            return format(Decimal(str(x)), "." + str(n) + "E")
        except Exception:
            return str(x)


def rel(a, b):
    """相对偏差 |a-b|/max(|a|,|b|)，b 为 0 时退化为绝对差。"""
    a = Decimal(a)
    b = Decimal(b)
    m = max(abs(a), abs(b))
    if m == 0:
        return abs(a - b)
    return abs(a - b) / m


# ---------------------------------------------------------------- G0 工具守卫


def run_g0():
    """量纲工具与数值工具的自检。工具本身必须先被守卫，才能用于判定。"""

    # G0-1 量纲相乘确为指数相加（本库历史事故：写成逐分量相乘）
    g = guard("G0-1_dim_mul_is_add",
              dmul(DIM_LENGTH, DIM_LENGTH) == D(0, 2, 0, 0)
              and dmul(D(1, 0, 0, 0), D(0, 1, 0, 0)) == D(1, 1, 0, 0),
              "[L]*[L]=L^2, [M]*[L]=ML")

    # G0-2 eps0*mu0*c^2 无量纲
    eps0 = D(-1, -3, 2, 2)     # [eps0] = Q^2 M^-1 L^-3 T^2
    mu0 = D(1, 1, 0, -2)       # [mu0]  = M L Q^-2
    c2 = dpow(D(0, 1, -1, 0), 2)
    g = guard("G0-2_eps0_mu0_c2_dimensionless",
              dmul(dmul(eps0, mu0), c2) == DIM_NONE,
              "eps0*mu0*c^2 = 1") and g

    # G0-3 [hbar*G/c^3] = L^2（普朗克长度平方）
    dim = ddiv(dmul(D(1, 2, -1, 0), D(-1, 3, -2, 0)), dpow(D(0, 1, -1, 0), 3))
    g = guard("G0-3_hbar_G_c3_is_L2", dim == D(0, 2, 0, 0),
              "[l_P^2] = " + dstr(dim)) and g

    # G0-4 能量密度 != 质量密度（r66 承重裁定：二者差 c^2）
    g = guard("G0-4_energy_density_ne_mass_density",
              DIM_ENERGY_DENSITY != DIM_MASS_DENSITY,
              "energy=" + dstr(DIM_ENERGY_DENSITY) + " vs mass=" + dstr(DIM_MASS_DENSITY)) and g

    # G0-5 差值恰为 c^2
    gap = ddiv(DIM_ENERGY_DENSITY, DIM_MASS_DENSITY)
    g = guard("G0-5_gap_is_c2", gap == dpow(D(0, 1, -1, 0), 2),
              "gap = " + dstr(gap)) and g

    # G0-6 负指数渲染不得出现 ^--n
    g = guard("G0-6_negative_exp_render", "^--" not in dstr(D(0, -3, 0, 0)),
              dstr(D(0, -3, 0, 0))) and g

    # G0-7/8 自实现三角函数：已知特殊角守卫（r59 教训）
    s6 = dsin(PI / 6)
    c3 = dcos(PI / 3)
    s2 = dsin(PI / 2)
    ok7 = rel(s6, Decimal("0.5")) < Decimal("1e-50") and rel(c3, Decimal("0.5")) < Decimal("1e-50")
    ok8 = rel(s2, Decimal(1)) < Decimal("1e-50")
    g = guard("G0-7_known_angles", ok7, "sin(pi/6)=" + fv(s6) + " cos(pi/3)=" + fv(c3)) and g
    g = guard("G0-8_sin_pi_half", ok8, "sin(pi/2)=" + fv(s2)) and g

    # G0-9 普朗克长度自洽
    g = guard("G0-9_planck_length_scale",
              Decimal("1e-36") < LP < Decimal("1e-34"), "l_P=" + fv(LP)) and g

    return g


# ---------------------------------------------------------------- D 段：求导证明

# 螺旋几何参数：R=1（长度单位），a = b/omega = 0.7（无量纲长度比）
R_HELIX = Decimal(1)
A_HELIX = Decimal("0.7")
H1 = Decimal("1e-4")
H2 = H1 / 2


def helix_analytic():
    """圆柱螺旋 (R cos u, R sin u, a u) 的解析 kappa, tau（对参数 u）。"""
    R = R_HELIX
    a = A_HELIX
    den = R * R + a * a
    return R / den, a / den


def run_d1():
    """D1: kappa^2 + tau^2 = omega^2 / v^2；取 P1 公设 v=c 分支即 (omega/c)^2。

    以无量纲相位 u=omega*t 为参数：kappa^2+tau^2 = 1/(R^2+a^2)，
    而 v = omega*sqrt(R^2+a^2) ⇒ kappa^2+tau^2 = omega^2/v^2。
    """
    R = R_HELIX
    a = A_HELIX
    ka, ta = helix_analytic()
    lhs_a = ka * ka + ta * ta
    rhs_a = Decimal(1) / (R * R + a * a)

    rows = []
    res = {}
    for tag, h in (("h", H1), ("h/2", H2)):
        d1, d2, d3 = helix_derivs_numeric(Decimal(0), R, a, h)
        kn, tn = kappa_tau_from_derivs(d1, d2, d3)
        lhs_n = kn * kn + tn * tn
        res[tag] = rel(lhs_n, lhs_a)
        rows.append((tag, fv(h), fv(kn), fv(tn), fv(lhs_n), fv(res[tag])))

    ratio = res["h"] / res["h/2"] if res["h/2"] != 0 else Decimal(0)
    ok_ident = rel(lhs_a, rhs_a) < Decimal("1e-50")
    ok_conv = Decimal("3.5") <= ratio <= Decimal("4.5")
    ok_nonzero = res["h/2"] > Decimal("1e-20")   # 残差停在差分截断极限，不是 0

    add("D01", "PASS" if (ok_ident and ok_conv and ok_nonzero) else "FAIL",
        "求导证明：kappa^2+tau^2 = omega^2/v^2（v=c 分支即 (omega/c)^2）",
        "解析对拍残差 " + fv(rel(lhs_a, rhs_a))
        + "；数值-解析残差 h=" + fv(res["h"]) + " / h/2=" + fv(res["h/2"])
        + "；收敛比 " + fv(ratio, 6) + "（二阶中心差分理论值 4，判据窗 3.5-4.5）"
        + "；残差非零(>" + "1e-20) ⇒ 排除恒等复读")

    guard("D01_identity", ok_ident, "analytic identity")
    guard("D01_convergence_ratio", ok_conv, "ratio=" + fv(ratio, 6))
    guard("D01_residual_nonzero", ok_nonzero, "residual(h/2)=" + fv(res["h/2"]))
    return rows, ratio


def run_d2():
    """D2: kappa/tau = v_theta/v_z。解析 R/a；数值对拍同 D1。"""
    R = R_HELIX
    a = A_HELIX
    ka, ta = helix_analytic()
    lhs_a = ka / ta
    rhs_a = R / a

    res = {}
    rows = []
    for tag, h in (("h", H1), ("h/2", H2)):
        d1, d2, d3 = helix_derivs_numeric(Decimal(0), R, a, h)
        kn, tn = kappa_tau_from_derivs(d1, d2, d3)
        lhs_n = kn / tn
        res[tag] = rel(lhs_n, lhs_a)
        rows.append((tag, fv(h), fv(kn), fv(tn), fv(lhs_n), fv(res[tag])))

    ratio = res["h"] / res["h/2"] if res["h/2"] != 0 else Decimal(0)
    ok_ident = rel(lhs_a, rhs_a) < Decimal("1e-50")
    ok_conv = Decimal("3.5") <= ratio <= Decimal("4.5")
    ok_nonzero = res["h/2"] > Decimal("1e-20")

    add("D02", "PASS" if (ok_ident and ok_conv and ok_nonzero) else "FAIL",
        "求导证明：kappa/tau = v_theta/v_z",
        "解析对拍残差 " + fv(rel(lhs_a, rhs_a))
        + "；数值-解析残差 h=" + fv(res["h"]) + " / h/2=" + fv(res["h/2"])
        + "；收敛比 " + fv(ratio, 6)
        + "；注：该式与 D01 同为 Frenet-Serret 定义式推论，零判别力")

    guard("D02_identity", ok_ident, "kappa/tau = R/a")
    guard("D02_convergence_ratio", ok_conv, "ratio=" + fv(ratio, 6))
    guard("D02_residual_nonzero", ok_nonzero, "residual(h/2)=" + fv(res["h/2"]))
    return rows, ratio


def run_d3():
    """D3: g(beta)=sqrt(1-beta^2) 的导数 dg/dbeta = -beta/sqrt(1-beta^2)。"""
    betas = [Decimal("0.5"), Decimal("0.9"), Decimal("0.99"),
             Decimal("0.999"), Decimal("0.9999"), Decimal("0.99999")]
    # 步长选择：beta->1 时 f''' ~ 3beta/(1-beta^2)^{5/2} 爆炸，
    # 中心差分截断误差 ~ h^2 f'''/6 相对 dg/dbeta 后仍在 1e-7 量级（h=1e-8 实测）。
    # 取 h=1e-12 并做 h / h/2 收敛比对拍（r59 纪律：容差与截断误差同源）。
    rows = []
    worst = Decimal(0)
    worst_ratio = Decimal(0)
    best_ratio = Decimal(100)
    for b in betas:
        ga = (Decimal(1) - b * b).sqrt()
        da = -b / ga
        res = {}
        for tag, hh in (("h", Decimal("1e-12")), ("h/2", Decimal("5e-13"))):
            gp = (Decimal(1) - (b + hh) * (b + hh)).sqrt()
            gm = (Decimal(1) - (b - hh) * (b - hh)).sqrt()
            dn = (gp - gm) / (2 * hh)
            res[tag] = rel(dn, da)
        ratio = res["h"] / res["h/2"] if res["h/2"] != 0 else Decimal(0)
        worst = max(worst, res["h/2"])
        worst_ratio = max(worst_ratio, ratio)
        best_ratio = min(best_ratio, ratio)
        rows.append((fv(b, 6), fv(ga), fv(da), fv(res["h/2"]), fv(ratio, 6)))

    ok_acc = worst < Decimal("1e-14")
    ok_conv = (Decimal("3.5") <= best_ratio) and (worst_ratio <= Decimal("4.5"))
    ok = ok_acc and ok_conv
    add("D03", "PASS" if ok else "FAIL",
        "求导证明：d/dbeta sqrt(1-beta^2) = -beta/sqrt(1-beta^2)",
        "6 个 beta 采样，解析 vs 中心差分（h=1e-12 / 5e-13）最大相对偏差 " + fv(worst)
        + "；收敛比区间 [" + fv(best_ratio, 6) + ", " + fv(worst_ratio, 6) + "]（理论 4）"
        + "；注：beta->1 时高阶导数爆炸，步长 1e-8 会把截断误差放大到 1e-7（首版误判来源）")
    guard("D03_derivative_matches", ok_acc, "worst=" + fv(worst))
    guard("D03_convergence_ratio", ok_conv,
          "[" + fv(best_ratio, 6) + "," + fv(worst_ratio, 6) + "]")
    return rows, worst


# ---------------------------------------------------------------- N 段：精算复拍


def run_n1():
    """N1: 泡内时钟减速 g = sqrt(1-beta^2) 六采样（复拍 r64 H02 / r66 O01-O02）。"""
    ref = [("0.5", "0.8660254"), ("0.9", "0.4358899"), ("0.99", "0.1410674"),
           ("0.999", "0.0447102"), ("0.9999", "0.0141418"), ("0.99999", "0.0044721")]
    rows = []
    worst = Decimal(0)
    for bs, gs in ref:
        b = Decimal(bs)
        g = (Decimal(1) - b * b).sqrt()
        # 参照值是「7 位小数」报价 ⇒ 必须用绝对容差 5e-8，
        # 用相对容差会把 0.0044721 这类小数值误杀（r59 纪律：容差与报价精度同源）
        ad = abs(g - Decimal(gs))
        worst = max(worst, ad)
        rows.append((bs, fv(g), gs, fv(ad)))
    ok = worst < Decimal("5e-8")
    add("N01", "PASS" if ok else "FAIL",
        "精算复拍：泡内时钟减速 g=sqrt(1-beta^2) 六采样",
        "最大绝对偏差 " + fv(worst) + "（参照值 7 位小数，绝对容差 5e-8；与 r64/r66 逐位一致）"
        + "；注：该判据的旧语义错误见 N02")
    guard("N01_g_values", ok, "worst=" + fv(worst))
    return rows, worst


def run_n2():
    """N2: 三档 g_obs 判据的机器自洽性 + 对旧写法矛盾的显式暴露。

    正本 §2.2 登记：r66 L124/L127 与 README L5773 写「g_obs=0 ⇒ 排除全部
    v_s>0」，这与同一册的 g=sqrt(1-beta^2) 及 (ii)(iii) 直接矛盾。本条只
    做机器核验并给出正确三档，不改写被引册。
    """
    rows = []
    # (i) g_obs = 1  ⇒  beta = sqrt(1-1) = 0  ⇒  v_s = 0
    g1 = Decimal(1)
    b1 = (Decimal(1) - g1 * g1).sqrt()
    # (ii) g_obs = 0.5 ⇒ v_s = c*sqrt(1-g^2)
    g2 = Decimal("0.5")
    v2 = C * (Decimal(1) - g2 * g2).sqrt()
    b2 = v2 / C
    # (iii) g_obs -> 0 ⇒ v_s -> c
    g3 = Decimal("1e-6")
    b3 = (Decimal(1) - g3 * g3).sqrt()
    v3 = C * b3
    rows.append(("(i) g_obs=1", fv(g1), fv(b1, 6), fv(C * b1, 6), "v_s=0 ⇒ 该族内排除全部 v_s>0"))
    rows.append(("(ii) g_obs=0.5", fv(g2), fv(b2), fv(v2), "v_s=c*sqrt(1-g^2)"))
    rows.append(("(iii) g_obs=1e-6", fv(g3), fv(b3), fv(v3), "v_s→c（效应最大，非趋零）"))

    # 旧写法的矛盾暴露：g_obs=0 ⇒ beta=1 ⇒ v_s=c（是效应最强端，不是「无效应」）
    b_old = (Decimal(1) - Decimal(0) * Decimal(0)).sqrt()
    contradiction = (b_old == Decimal(1)) and (C * b_old == C)

    ok = (b1 == 0) and (rel(b2, Decimal("0.8660254")) < Decimal("1e-6")) and \
         (rel(b3, Decimal(1)) < Decimal("1e-11")) and contradiction

    add("N02", "PASS" if ok else "FAIL",
        "精算：更正后三档 g_obs 判据自洽性（正本 §2.2）",
        "(i) g_obs=1 ⇒ beta=" + fv(b1, 6) + " ⇒ v_s=0 ⇒ 排除该族全部 v_s>0；"
        + "(ii) g_obs=0.5 ⇒ v_s=" + fv(v2) + " m/s；"
        + "(iii) g_obs=1e-6 ⇒ beta=" + fv(b3) + " ⇒ v_s→c。"
        + " 旧写法「g_obs=0 ⇒ 排除全部 v_s>0」与 g=sqrt(1-beta^2) 矛盾（g=0 ⟺ beta=1 ⟺ v_s=c），"
        + "本册以更正指针登记，不改写 r66/README 字节。")

    guard("N02_g1_implies_v0", b1 == 0, "beta(g_obs=1)=" + fv(b1, 6))
    guard("N02_g_half", rel(b2, Decimal("0.8660254")) < Decimal("1e-6"), "beta=" + fv(b2))
    guard("N02_g_small_implies_c", rel(b3, Decimal(1)) < Decimal("1e-11"), "beta=" + fv(b3))
    guard("N02_old_form_contradiction_exposed", contradiction,
          "g_obs=0 ⇒ beta=1 ⇒ v_s=c（效应最强端）")
    return rows, ok


def run_n3():
    """N3: QEI 五族能量密度比值复拍（r66 判决表）。

    族 (a,b)：rho_QEI = hbar*c / (delta^a * L^b)，a+b=4，alpha=beta=1。
    delta = l_P，L = 100 m，v_s = c。
    需求 rho_Alc(l_P) = 4.6091e+111 J/m^3（r66）；rho_Alc ∝ delta^-2。
    比值 = rho_Alc / rho_QEI：<1 不排除，>1 排除。
    """
    rho_alc_lp = Decimal("4.6091e+111")
    L = Decimal(100)
    fams = [(4, 0, "9.9472e-03", False), (3, 1, "6.16e+34", True),
            (2, 2, "3.81e+71", True), (1, 3, "2.36e+108", True),
            (0, 4, "1.46e+145", True)]
    rows = []
    ok_all = True
    for a, b, ref, excluded in fams:
        # 与 r66 同口径：delta = CODATA 标称 l_P
        rho = HBAR * C / (LP_NOM ** a * L ** b)
        ratio = rho_alc_lp / rho
        # 容差与报价精度同源（r59 纪律）：(4,0) 报 5 位有效数字 ⇒ 5e-4；
        # 四个排除族只报 3 位（6.16e+34）⇒ 5e-3。用统一 1e-4 会把合法舍入判成错误。
        tol = Decimal("5e-3") if excluded else Decimal("5e-4")
        r = rel(ratio, Decimal(ref))
        ok = r < tol
        ok_all = ok_all and ok
        rows.append(("(%d,%d)" % (a, b), fv(rho), fv(ratio), ref, fv(r),
                     "排除" if excluded else "不排除"))
    add("N03", "PASS" if ok_all else "FAIL",
        "精算复拍：QEI 五量纲闭合族判决表（r66）",
        "五族比值 " + " / ".join(x[2] for x in rows)
        + "；不排除 1 族 (4,0)、排除 4 族；与 r66 判决表一致（参照值仅 3-5 位有效数字，"
        + "容差按报价精度取 5e-4 / 5e-3，复拍一致度落在 1e-4 量级）")
    guard("N03_family_table", ok_all, "five families reproduced")
    return rows, ok_all


def run_n4():
    """N4: 幸存族 (4,0) 的 delta_max 与工程门槛下的 M_neg（r66/r67）。

    由 rho_QEI = hbar*c/delta^4 ≥ rho_Alc(delta) = rho_Alc(l_P)*(l_P/delta)^2
    ⇒ delta^2 ≤ hbar*c / (rho_Alc(l_P) * l_P^2)
    M_neg = v_s^2 R^2 / (8 G delta)（v_s=c, R=1 m）。
    """
    rho_alc_lp = Decimal("4.6091e+111")
    delta_max = (HBAR * C / (rho_alc_lp * LP_NOM * LP_NOM)).sqrt()
    R = Decimal(1)
    m_neg = C * C * R * R / (8 * G * delta_max)
    m_sun = m_neg / M_SUN
    m_univ = m_neg / M_UNIV
    lp_ratio = delta_max / LP_NOM

    # 容差按报价精度：delta_max / M_neg / M_sun 报 6-7 位 ⇒ 5e-4；
    # 宇宙质量倍数报 3 位（6.92e6）⇒ 5e-3；l_P 倍数报 5 位（10.027）⇒ 5e-4。
    ok_d = rel(delta_max, Decimal("1.620540e-34")) < Decimal("5e-4")
    ok_m = rel(m_neg, Decimal("1.038690e+60")) < Decimal("5e-4")
    ok_s = rel(m_sun, Decimal("5.222381e+29")) < Decimal("5e-4")
    ok_u = rel(m_univ, Decimal("6.92e6")) < Decimal("5e-3")
    ok_lp = rel(lp_ratio, Decimal("10.027")) < Decimal("5e-4")

    add("N04", "PASS" if (ok_d and ok_m and ok_s and ok_u and ok_lp) else "FAIL",
        "精算复拍：幸存族 (4,0) 的 delta_max 与 M_neg（r66/r67）",
        "delta_max=" + fv(delta_max) + " m = " + fv(lp_ratio, 6) + " l_P（参照 1.620540e-34 m / 10.027 l_P）；"
        + "R=1 m 时 M_neg=" + fv(m_neg) + " kg = " + fv(m_sun, 6) + " M_sun = "
        + fv(m_univ, 6) + " × 可观测宇宙质量（参照 1.038690e+60 kg / 5.222381e+29 M_sun / 6.92e6）")
    guard("N04_delta_max", ok_d, fv(delta_max))
    guard("N04_m_neg", ok_m, fv(m_neg))
    guard("N04_m_sun", ok_s, fv(m_sun, 6))
    guard("N04_m_univ", ok_u, fv(m_univ, 6))
    guard("N04_lp_ratio", ok_lp, fv(lp_ratio, 6))
    return delta_max, m_neg, m_sun, m_univ, lp_ratio


def run_n5():
    """N5: ringdown 排除强度复拍（OPEN_v3）。chi^2=33.00, df=2。

    p = exp(-chi^2/2)（df=2 的卡方尾概率恰为 exp(-chi^2/2)）。
    sigma 由 chi^2 = z^2（df=2 时等价）⇒ z = sqrt(chi^2)。
    """
    chi2 = Decimal("33.00")
    p = (-(chi2 / 2)).exp()
    z = chi2.sqrt()
    ok_p = rel(p, Decimal("6.83e-8")) < Decimal("5e-3")
    ok_z = rel(z, Decimal("5.74")) < Decimal("5e-3")
    add("N05", "PASS" if (ok_p and ok_z) else "FAIL",
        "精算复拍：ringdown 排除强度（OPEN_v3）",
        "chi^2=" + fv(chi2, 6) + " (df=2) ⇒ p=exp(-chi^2/2)=" + fv(p)
        + "（参照 6.83e-8）；等价 sigma=sqrt(chi^2)=" + fv(z, 6) + "（参照 5.74）")
    guard("N05_p_value", ok_p, fv(p))
    guard("N05_sigma", ok_z, fv(z, 6))
    return p, z


def run_n6():
    """N6: g-2 与 EDM 窗口读数复拍（严格区分口径）。"""
    # g-2：alpha/(8 pi) 口径
    a_tuft = ALPHA / (8 * PI)
    a_exp = Decimal("1.159652e-3")
    dev = abs(a_tuft - a_exp) / a_exp
    ok_a = rel(a_tuft, Decimal("2.904e-4")) < Decimal("5e-4")
    ok_d = rel(dev, Decimal("0.7496")) < Decimal("5e-4")

    # EDM：预言 1.409e-13 e·cm vs ACME2018 上限 1.1e-29 e·cm
    d_pred = Decimal("1.409e-13")
    d_acme = Decimal("1.1e-29")
    over = d_pred / d_acme
    log_over = (over.ln() / Decimal(10).ln())
    ok_e = rel(log_over, Decimal("16.107")) < Decimal("5e-3")

    add("N06", "PASS" if (ok_a and ok_d and ok_e) else "FAIL",
        "精算复拍：g-2 与 EDM 窗口（口径严格分列）",
        "g-2：alpha/(8pi)=" + fv(a_tuft) + " vs a_e(exp)=" + fv(a_exp, 6)
        + " ⇒ 偏差 " + fv(dev, 6) + "（74.96%，该口径下被否决）；"
        + "注意 2tau/kappa 口径的 74.19% 是 CIRCULAR、不可判定，不得合并。"
        + " EDM：" + fv(d_pred, 6) + " e·cm vs ACME " + fv(d_acme, 6)
        + " e·cm ⇒ 超限 " + fv(over, 6) + " 倍 = " + fv(log_over, 6)
        + " 个量级（JILA 4.1e-30 口径为 16.536，须点名来源）")

    guard("N06_g2_value", ok_a, fv(a_tuft))
    guard("N06_g2_deviation", ok_d, fv(dev, 6))
    guard("N06_edm_orders", ok_e, fv(log_over, 6))
    return a_tuft, dev, over, log_over


# ---------------------------------------------------------------- 主流程


def build_report():
    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-r144  空间是否运动与怎么运动 · 跨册归总  求导证明验证与精算")
    lines.append("=" * 78)
    lines.append("")
    lines.append("性质：不产生新物理。只做 (a) 求导证明的解析-数值双路径对拍；")
    lines.append("      (b) 对既有册公开读数的高精度独立复拍。")
    lines.append("")
    n_pass = sum(1 for e in ENTRIES if e["status"] == "PASS")
    n_fail = sum(1 for e in ENTRIES if e["status"] == "FAIL")
    n_bnd = sum(1 for e in ENTRIES if e["status"] == "BOUNDARY")
    n_info = sum(1 for e in ENTRIES if e["status"] == "INFO")
    lines.append("条目 %d：PASS = %d  FAIL = %d  BOUNDARY = %d  INFO = %d"
                 % (len(ENTRIES), n_pass, n_fail, n_bnd, n_info))
    lines.append("")
    lines.append("-" * 78)
    for e in ENTRIES:
        lines.append("[%s] %s  %s" % (e["status"], e["code"], e["title"]))
        lines.append("      " + e["detail"])
        lines.append("")
    lines.append("-" * 78)
    ng = len(GUARDS)
    nok = sum(1 for g in GUARDS if g["ok"])
    lines.append("守卫 %d / %d 通过" % (nok, ng))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [FAIL-GUARD] " + g["name"] + " : " + g["info"])
    lines.append("")
    lines.append("红线：数学自洽 != 物理证实。D01/D02 通过只证明「构造了一条螺旋线」，")
    lines.append("      不构成 P1 物理成立的证据（Frenet-Serret 定义式推论，零判别力）。")
    lines.append("      否定结论均为框架内（Alcubierre 型 + QEI / 该公设集），")
    lines.append("      不排除框架外机制。不可证伪 != 被实验否决。")
    lines.append("=" * 78)
    return "\n".join(lines), (n_pass, n_fail, n_bnd, n_info)


def main():
    run_g0()
    d1rows, d1ratio = run_d1()
    d2rows, d2ratio = run_d2()
    d3rows, d3worst = run_d3()
    n1rows, n1worst = run_n1()
    n2rows, n2ok = run_n2()
    n3rows, n3ok = run_n3()
    dmax, mneg, msun, muniv, lpr = run_n4()
    pval, zval = run_n5()
    a_tuft, dev, over, logo = run_n6()

    report, counts = build_report()
    print(report)

    counts_map = {"PASS": counts[0], "FAIL": counts[1],
                  "BOUNDARY": counts[2], "INFO": counts[3]}

    payload = {
        "round": "r144",
        "title": "空间是否运动与怎么运动 · 跨册归总 求导证明验证与精算",
        "date": STAMP,
        "nature": "不产生新物理；求导对拍 + 既有读数精算复拍",
        "constants": {
            "c": fv(C), "G": fv(G), "hbar": fv(HBAR), "alpha": fv(ALPHA),
            "l_P_derived": fv(LP), "M_sun": fv(M_SUN), "M_univ_ref": fv(M_UNIV),
        },
        "helix_geometry": {"R": fv(R_HELIX), "a": fv(A_HELIX),
                           "h1": fv(H1), "h2": fv(H2)},
        "derivation_proof": {
            "D01_rows": [list(r) for r in d1rows], "D01_convergence_ratio": fv(d1ratio, 6),
            "D02_rows": [list(r) for r in d2rows], "D02_convergence_ratio": fv(d2ratio, 6),
            "D03_rows": [list(r) for r in d3rows], "D03_worst": fv(d3worst),
            "discriminating_power": "零：D01/D02 是 Frenet-Serret 定义式推论，对任意螺旋线恒真",
        },
        "recomputation": {
            "N01_clock_slowdown": [list(r) for r in n1rows],
            "N02_gobs_three_tiers": [list(r) for r in n2rows],
            "N03_qei_families": [list(r) for r in n3rows],
            "N04_delta_max_m": fv(dmax), "N04_delta_max_over_lP": fv(lpr, 6),
            "N04_M_neg_kg": fv(mneg), "N04_M_neg_Msun": fv(msun, 6),
            "N04_M_neg_over_universe": fv(muniv, 6),
            "N05_chi2": "33.00", "N05_p": fv(pval), "N05_sigma": fv(zval, 6),
            "N06_a_tuft": fv(a_tuft), "N06_deviation": fv(dev, 6),
            "N06_edm_excess": fv(over, 6), "N06_edm_orders": fv(logo, 6),
        },
        "corrections_registered": [
            "g_obs=1 ⇒ v_s=0 ⇒ 排除该族全部 v_s>0（r66 L124/L127 与 README L5773 的旧写法 g_obs=0 与 g=sqrt(1-beta^2) 矛盾，本册以更正指针登记，不改写被引册）",
            "三档判据适用范围限于 dtau/dt=sqrt(1-v_s^2/c^2) 成立的同族度规；泡内平坦的 Alcubierre/Natario 型不适用（r64 C05/C05b）",
            "正确核 22 条是 2026-10-03 固化口径；r111/r112 后现行值 16 条",
            "v16 A07 是「部分闭合」非 PASS，残留 4 项",
            "β 跑动 = 无预言/不可证伪，不是实验否决",
            "g-2 仅 alpha/(8pi) 口径被否决；2tau/kappa 口径 CIRCULAR、不可判定",
        ],
        "entries": ENTRIES,
        "guards": GUARDS,
        "counts": counts_map,
        "guard_total": len(GUARDS),
        "guard_pass": sum(1 for g in GUARDS if g["ok"]),
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    with io.open(os.path.join(DATA_DIR, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DATA_DIR, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write(report)

    # 数据 md
    md = []
    md.append("# " + NAME)
    md.append("")
    md.append("> 本册**不产生新物理**。求导证明 = 解析 vs 中心差分双路径对拍；")
    md.append("> 精算 = 对既有册公开读数的高精度独立复拍。")
    md.append("")
    md.append("- 正本：`整理_空间是否运动与怎么运动_跨册归总_" + STAMP + ".md`")
    md.append("- 判定：`判定_TUFT-r144_空间是否运动与怎么运动_跨册归总_求导证明验证精算_" + STAMP + ".md`")
    md.append("- 复现：`python 源码/_run_r144.py`")
    md.append("")
    md.append("## 条目")
    md.append("")
    md.append("| 编号 | 状态 | 标题 | 读数 |")
    md.append("|---|---|---|---|")
    for e in ENTRIES:
        md.append("| " + e["code"] + " | " + e["status"] + " | " + e["title"]
                  + " | " + e["detail"].replace("|", "/") + " |")
    md.append("")
    md.append("## 守卫")
    md.append("")
    md.append("守卫 %d / %d 通过。" % (payload["guard_pass"], payload["guard_total"]))
    md.append("")
    md.append("## 红线")
    md.append("")
    md.append("数学自洽 ≠ 物理证实。D01/D02 通过只证明「构造了一条螺旋线」，")
    md.append("不构成 P1 物理成立的证据。否定结论均为框架内，不排除框架外机制。")
    md.append("")
    with io.open(os.path.join(DATA_DIR, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    all_ok = all(g["ok"] for g in GUARDS)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
