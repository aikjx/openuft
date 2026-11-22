# -*- coding: utf-8 -*-
"""
ROOT V128 第六册 · beta 参数化的独立 Fisher 重拟合与零假设处的 lambda 不可辨识性

性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

问题（第五册留下的唯一有增量方向）
----------------------------------
第五册证明：把 alpha 上界除以 lambda^2 得到的 beta 上界在大 lambda 端恒定，
所以 6 个尾部格点只给 1 份信息。但那是**对已发布约束的再解释**，不是从数据
出发的独立重拟合。本册做后者：在 (beta, lambda) 参数化上直接构造 Fisher 矩阵，
问一个第五册没判的问题——

    **在零假设 beta = 0 处，lambda 本身可辨识吗？**

答案（先给）
-----------
不可辨识，且是精确的，不是精度问题：

    y_i = beta * G_i(lambda),   G_i = lambda^2 K_i
    dy_i/dlambda = beta * G_i'(lambda)

在 beta = 0 处 d y / d lambda 逐分量为 0 => Fisher 矩阵 lambda 列/行全 0
=> det F = 0 => sigma_lambda 的 Cramer-Rao 下界发散。

推论：任何「最佳拟合 lambda」都不是数据结论；第三册的 Δchi2 峰 0.444/0.448
是 beta 自由 profile 在噪声上的起伏，不是 lambda 被测定。

口径与复用
----------
- 进动核 K 用第三册同一闭式（对 e 精确、对 alpha 一阶），本册独立实现；
  用第三册 JSON 的 sigma_alpha 做两路互验（同源，不能算独立证据）。
- 观测表沿用第三册的一手读数（Pitjev & Pitjeva / Fienga et al.）。
- 本册不重判 V128，不重拟合星历，不修正第三册任何判词。

红线：不宣称攻破统一场论；独立实验预言 0；不产生新物理。
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

STEM = "_ALG_rootv128f_beta_fisher_recompute"
DATE = "2026-11-22"


def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_json():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json")


# ------------------------------------------------------------------ Decimal
def Dq(x):
    if isinstance(x, D):
        return x
    if isinstance(x, int):
        return D(x)
    return D(str(x))


_PI = {}


def PI():
    if "v" not in _PI:
        def atan_inv(n):
            n = Dq(n)
            x = D(1) / n
            x2 = x * x
            s = D(0)
            t = x
            k = 0
            while True:
                q = t / Dq(2 * k + 1)
                s += q if k % 2 == 0 else -q
                t *= x2
                k += 1
                if abs(q) < D("1e-62"):
                    break
            return s
        _PI["v"] = 16 * atan_inv(5) - 4 * atan_inv(239)
    return _PI["v"]


def fstr(x, nd=6):
    x = Dq(x)
    if x == 0:
        return "0"
    return ("%." + str(nd) + "E") % x


def rel(a, b):
    a, b = Dq(a), Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ------------------------------------------------------------------ 常数与行星
AU = D("149597870700")
ARCSEC = D(180) / PI() * D(3600)
CENTURY_DAYS = D("36525")
MAS = D("1e-3")

PLANETS = {
    "Mercury": {"a": D("0.38709893"), "e": D("0.20563069"), "P": D("87.9691")},
    "Venus":   {"a": D("0.72333199"), "e": D("0.00677323"), "P": D("224.7008")},
    "Earth":   {"a": D("1.00000011"), "e": D("0.01671022"), "P": D("365.2564")},
    "Mars":    {"a": D("1.52366231"), "e": D("0.09341233"), "P": D("686.9800")},
    "Jupiter": {"a": D("5.20288700"), "e": D("0.04838624"), "P": D("4332.5890")},
    "Saturn":  {"a": D("9.53667594"), "e": D("0.05386179"), "P": D("10759.2200")},
}

DATASETS = {
    "EPM2011": [("Mercury", "-2.0", "3.0"), ("Venus", "2.6", "1.6"),
                ("Earth", "0.19", "0.19"), ("Mars", "-0.020", "0.037"),
                ("Jupiter", "58.7", "28.3"), ("Saturn", "-0.32", "0.47")],
    "INPOP10a": [("Mercury", "0.4", "0.6"), ("Venus", "0.2", "1.5"),
                 ("Earth", "-0.2", "0.9"), ("Mars", "-0.04", "0.15"),
                 ("Jupiter", "-41", "42"), ("Saturn", "0.15", "0.65")],
}

NAMES = [r[0] for r in DATASETS["EPM2011"]]


# ------------------------------------------------------------------ 核（第三册同口径，独立实现）
def bessI1(z):
    z = Dq(z)
    hz = z / 2
    pw = hz
    s = D(0)
    k = 0
    fact = D(1)
    while True:
        t = pw / (fact * fact * D(k + 1))
        s += t
        if abs(t) < D("1e-70"):
            break
        k += 1
        fact *= D(k)
        pw *= hz * hz
    return s


def K_per_orbit(name, lam):
    """单位 alpha 的每圈进动（弧度），对 e 精确、对 alpha 一阶。"""
    p = PLANETS[name]
    a = p["a"] * AU
    e = p["e"]
    rho = a / Dq(lam)
    if e == 0:
        return PI() * rho * rho * (-rho).exp()
    return (2 * PI() * a * (D(1) - e * e).sqrt() / (e * Dq(lam))
            * (-rho).exp() * bessI1(a * e / Dq(lam)))


def K_arcsec_cy(name, lam):
    p = PLANETS[name]
    return K_per_orbit(name, lam) * (CENTURY_DAYS / p["P"]) * ARCSEC


def K_vector(lam):
    return [K_arcsec_cy(n, lam) for n in NAMES]


def G_vector(lam):
    """beta = alpha/lam^2 参数化下的核：G = lam^2 * K。"""
    l = Dq(lam)
    return [l * l * k for k in K_vector(l)]


def dK_vector(lam):
    """K 对 lam 的中心差分 + Richardson（消 h^2）。"""
    l = Dq(lam)
    h = l * D("1e-7")

    def one(step):
        kp = K_vector(l + step)
        km = K_vector(l - step)
        return [(kp[i] - km[i]) / (2 * step) for i in range(len(NAMES))]

    a = one(h)
    b = one(h / 2)
    return [(D(4) * b[i] - a[i]) / D(3) for i in range(len(NAMES))]


def dG_vector(lam):
    """G 对 lam 的中心差分 + Richardson。"""
    l = Dq(lam)
    h = l * D("1e-7")

    def one(step):
        gp = G_vector(l + step)
        gm = G_vector(l - step)
        return [(gp[i] - gm[i]) / (2 * step) for i in range(len(NAMES))]

    a = one(h)
    b = one(h / 2)
    return [(D(4) * b[i] - a[i]) / D(3) for i in range(len(NAMES))]


# ------------------------------------------------------------------  Fisher
def fisher_AB(ds, lam, alpha, param):
    """返回 2x2 Fisher 矩阵；param='alpha' 用 (alpha,lam)，'beta' 用 (beta,lam)。"""
    sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
    K = K_vector(lam)
    dK = dK_vector(lam)
    if param == "alpha":
        v0 = K
        v1 = [Dq(alpha) * dK[i] for i in range(len(K))]
    else:
        G = G_vector(lam)
        dG = dG_vector(lam)
        beta = Dq(alpha) / (Dq(lam) * Dq(lam))
        v0 = G
        v1 = [beta * dG[i] for i in range(len(G))]
    f00 = sum(v0[i] * v0[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    f01 = sum(v0[i] * v1[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    f11 = sum(v1[i] * v1[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    return f00, f01, f11


def det2(f):
    return f[0] * f[2] - f[1] * f[1]


def cr_bounds(f):
    """2 参数 Fisher 逆的对角元（方差下界）。奇异时返回 None。"""
    d = det2(f)
    if d == 0:
        return None
    return f[2] / d, f[0] / d


def linear_fit(ds, lam, kind):
    """单参数线性拟合。返回 (hat, sigma, chi2_0, delta_chi2)。"""
    obs = [Dq(r[1]) * MAS for r in DATASETS[ds]]
    sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
    k = K_vector(lam) if kind == "alpha" else G_vector(lam)
    num = D(0)
    den = D(0)
    c0 = D(0)
    for i in range(len(k)):
        w = k[i] / sig[i]
        num += w * (obs[i] / sig[i])
        den += w * w
        c0 += (obs[i] / sig[i]) ** 2
    if den == 0:
        return None, None, c0, D(0)
    hat = num / den
    sd = D(1) / den.sqrt()
    return hat, sd, c0, c0 - (num * num / den)
