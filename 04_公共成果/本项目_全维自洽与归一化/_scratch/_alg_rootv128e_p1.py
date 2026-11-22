# -*- coding: utf-8 -*-
"""
ROOT V128 第五册 · 大 lambda 扫描空转与整体幅度不可辨识性
=============================================================
性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

对象锁定
--------
ROOT V128 的 Yukawa 型第五力势

    Phi(r) = -(mu/r) * (1 + alpha * exp(-r/lambda))        mu = G M

本册只问一个问题：**在这个势里，哪些参数组合是真正可观测的？**

结论（先给）
-----------
`alpha` 本身不是可观测参数。在 lambda -> infinity 的退耦极限里，
`alpha` 只是一个质量重标定因子，与 `M` 精确简并。唯一被约束的是

    beta = alpha / lambda^2

理由是代数：把 exp(-r/lambda) 展开，常数项 alpha 乘 1/r 就是 mu 的重标定，
首个形状项是 -alpha r / (2 lambda^2)，这是一个**常数径向加速度**，
其量级正是 alpha/lambda^2。

因此任何沿 lambda 扫描、报告 "alpha < bound(lambda)" 的做法，在大 lambda 端
是同一个 beta 约束除以 lambda^2 的换算式，不携带新信息。

本册机读验证：第三册 11 个 lambda 格点上 sigma_beta = sigma_alpha/lambda^2
在 lambda >= 30 AU 之后收敛（相对变化 < 1e-3）。

红线
----
- 不宣称攻破统一场论。本册不产生任何新物理，只做参数可辨识性分析。
- 独立实验预言 0。
- 第三册读数以继承方式读取（同一 JSON），不重拟合、不改判词。
- 若机核判据与第三册登记值冲突，报负读数，不改第三册。
"""

import ast
import hashlib
import json
import os
import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

STEM = "_ALG_rootv128e_largelambda_vacuity_recompute"
DATE = "2026-11-22"

# ---------------------------------------------------------------- 路径（唯一构造）
def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_json():
    """第三册机读件（跨册继承的唯一来源）。"""
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json")


# ---------------------------------------------------------------- Decimal 工具
def Dq(x):
    """字符串/整数 -> 高精度 Decimal（禁裸 float 入口）。"""
    if isinstance(x, D):
        return x
    if isinstance(x, int):
        return D(x)
    return D(str(x))


_PI_CACHE = {}


def dpi():
    if "v" in _PI_CACHE:
        return _PI_CACHE["v"]
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239)
    def atan_inv(n):
        n = Dq(n)
        x = D(1) / n
        x2 = x * x
        s = D(0)
        term = x
        k = 0
        while True:
            t = term / (2 * k + 1)
            if k % 2 == 0:
                s += t
            else:
                s -= t
            term *= x2
            k += 1
            if abs(t) < D("1e-62"):
                break
        return s

    v = 16 * atan_inv(5) - 4 * atan_inv(239)
    _PI_CACHE["v"] = v
    return v


def dsin(x):
    x = x % (2 * dpi())
    if x > dpi():
        x -= 2 * dpi()
    s = D(0)
    term = x
    k = 1
    while True:
        s += term
        term = -term * x * x / Dq((k + 1) * (k + 2))
        k += 2
        if abs(term) < D("1e-58"):
            break
    return s


def dcos(x):
    return dsin(x + dpi() / 2)


def dsqrt(x):
    return Dq(x).sqrt()


def rel(a, b):
    """相对偏离。b=0 时退化为绝对偏离（并标量级）。"""
    a = Dq(a)
    b = Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def fmt(x, nd=6):
    """科学计数（零值不写指数）。"""
    x = Dq(x)
    if x == 0:
        return "0"
    return "%.*E" % (nd, x)


def fstr(x, nd=6):
    x = Dq(x)
    if x == 0:
        return "0"
    return ("%." + str(nd) + "E") % x


# ---------------------------------------------------------------- 势与泛函
def phi_const_shift(x, mu, c0):
    """Phi = -(mu/x) (1 - c0)。c0 = 常数偏移（零方向）。"""
    return -(Dq(mu) / Dq(x)) * (D(1) - Dq(c0))


def phi_yukawa(x, mu, alpha, lam):
    """V128 原势。"""
    x = Dq(x)
    lam = Dq(lam)
    return -(Dq(mu) / x) * (D(1) + Dq(alpha) * (-x / lam).exp())


def simpson(f, a, b, n):
    """复合 Simpson 1/3，n 必须为偶数。"""
    a = Dq(a)
    b = Dq(b)
    if n % 2:
        n += 1
    h = (b - a) / Dq(n)
    s = f(a) + f(b)
    for i in range(1, n):
        s += (D(4) if i % 2 else D(2)) * f(a + h * Dq(i))
    return s * h / D(3)


def simpson_pair(f, a, b, n):
    """两路：S(n) 与 S(2n)，用于 Richardson / 收敛检查。"""
    s1 = simpson(f, a, b, n)
    s2 = simpson(f, a, b, 2 * n)
    ext = (D(16) * s2 - s1) / D(15)
    return s1, s2, ext


def shapiro_potential_integral(b, lmax, n, phi):
    """I = int_{-L}^{L} Phi(sqrt(b^2+l^2)) dl，用偶性折成 2*int_0^L。"""
    b = Dq(b)
    lmax = Dq(lmax)

    def g(l):
        return phi(dsqrt(b * b + l * l))

    return 2 * simpson(g, D(0), lmax, n)


def shapiro_asinh_exact(b, lmax):
    """int_{-L}^{L} dl/sqrt(b^2+l^2) = 2 asinh(L/b)，asinh = ln(x+sqrt(x^2+1))。"""
    b = Dq(b)
    x = Dq(lmax) / b
    return 2 * (x + dsqrt(x * x + 1)).ln()


def deflection_kernel_integral(b, lmax, n):
    """J = int_{-L}^{L} b/(b^2+l^2)^{3/2} dl，用偶性折成 2*int_0^L。"""
    b = Dq(b)
    lmax = Dq(lmax)

    def g(l):
        r2 = b * b + l * l
        return b / (r2 * dsqrt(r2))

    return 2 * simpson(g, D(0), lmax, n)


def deflection_kernel_exact(b, lmax):
    """闭式：2L/(b^2 sqrt(b^2+L^2))。"""
    b = Dq(b)
    lm = Dq(lmax)
    return 2 * lm / (b * b * dsqrt(b * b + lm * lm))


def period_of(a, mu):
    return 2 * dpi() * (Dq(a) ** D("1.5")) / dsqrt(mu)


def kepler_E(M, e):
    """解 E - e sin E = M，Newton。"""
    M = Dq(M)
    e = Dq(e)
    E = M if e < D("0.8") else dpi()
    for _ in range(200):
        f = E - e * dsin(E) - M
        fp = D(1) - e * dcos(E)
        d = f / fp
        E -= d
        if abs(d) < D("1e-55"):
            break
    return E
