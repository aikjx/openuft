# -*- coding: utf-8 -*-
"""
ROOT V128 第七册 · 「换观测量」出路的可算自审

性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

本册要判的命题（本链自己提出的，必须反噬自己）
------------------------------------------------
第四册说「整体幅度对近点进动零信息，打破它要换观测量」。
第五册说「换观测量也不行——Eötvös 通道结构性失效」。
第六册说「零假设处 λ 的 Fisher 列精确为零」。
三册都把「换观测量（测距 / GM 独立标定 / Shapiro / LLR / 脉冲星计时）」
列为唯一剩下的出口，但**从未判它**。本册判它。

命题 S：把观测量从近点进动换成别的引力势泛函，
        就能在 beta=0 处测出 λ。

核心论证（严格，且可机读）
--------------------------
势  Phi(r; beta, lambda) = -(mu/r)(1 + beta*lambda^2*exp(-r/lambda))

在 beta = 0 处，Phi ≡ -mu/r  **逐点不含 lambda**，所以

    dPhi/dlambda |_{beta=0} = 0

对任意观测量 Q[Phi]（不必线性！），链式法则给

    dQ/dlambda |_{beta=0} = ∫ (delta Q / delta Phi) * (dPhi/dlambda) = 0

⇒ 命题 S 为假。而且这与「线性泛函」无关：即使 Q = ∫ w Phi^2，
只要 Phi 本身在 beta=0 处不含 lambda，导数仍精确为零。

边界（必须同时给）
------------------
beta != 0 时 Phi 含 λ 的形状，所有观测量的 λ 导数恢复非零 ⇒
「不可辨识」严格限于零假设，不是「Yukawa 的 λ 永远不可测」。
本册用注入-恢复正对照机读这条边界。

红线：不宣称攻破统一场论；不产生新物理；独立实验预言 0。
      本册不引入任何外部读数，纯结构与可辨识性分析。
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

STEM = "_ALG_rootv128g_observable_swap_audit"
DATE = "2026-11-22"


def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_5():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128e_largelambda_vacuity_recompute_2026-11-22.json")


def upstream_6():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128f_beta_fisher_recompute_2026-11-22.json")


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


def fmt(x, nd=6):
    if Dq(x) == 0:
        return "0"
    return ("%." + str(nd) + "E") % Dq(x)


def rel(a, b):
    a, b = Dq(a), Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ------------------------------------------------------------------ 物理核
AU = D("149597870700")


def phi(r, beta, lam, mu=D(1)):
    """Yukawa 势，用 beta = alpha/lam^2 参数化。r, lam 同单位（AU）。"""
    r, lam, beta = Dq(r), Dq(lam), Dq(beta)
    return -(mu / r) * (D(1) + beta * lam * lam * (-r / lam).exp())


def simpson(f, a, b, n):
    a, b = Dq(a), Dq(b)
    if n % 2:
        n += 1
    h = (b - a) / Dq(n)
    s = f(a) + f(b)
    for i in range(1, n):
        s += (D(4) if i % 2 else D(2)) * f(a + h * Dq(i))
    return s * h / D(3)


# ------------------------------------------------------------------ 五类观测量（势的泛函）
# 单位刻意统一为「势的量纲 × 路径长度」，只比较可辨识性结构，不冒充物理读数。
OBSERVABLES = [
    ("shapiro",      "Shapiro 延迟（沿视线积分势）"),
    ("light_bend",   "光线偏折（横向梯度积分）"),
    ("redshift",     "引力红移（两端势差）"),
    ("range",        "雷达测距往返（沿路径积分势的一阶修正）"),
    ("orbital_T",    "轨道周期（势决定的特征时标）"),
]


def observable(name, beta, lam, weight=1):
    """Q[Phi]。weight 只用于制造不同权重，不改变可辨识性结论。"""
    w = Dq(weight)
    lam = Dq(lam)
    if name == "shapiro":
        b = D("1")
        return w * 2 * simpson(lambda l: phi((b * b + l * l).sqrt(), beta, lam),
                               D(0), D(20), 400)
    if name == "light_bend":
        b = D("1")

        def integrand(l):
            r = (b * b + l * l).sqrt()
            # 横向梯度：dPhi/dr * b/r；用中心差分避免解析式混入 lambda
            h = D("1e-7")
            d = (phi(r + h, beta, lam) - phi(r - h, beta, lam)) / (2 * h)
            return d * b / r
        return w * 2 * simpson(integrand, D(0), D(20), 400)
    if name == "redshift":
        return w * (phi(D("1.2"), beta, lam) - phi(D("1.0"), beta, lam))
    if name == "range":
        return w * simpson(lambda l: phi(D("1.0") + l, beta, lam), D(0), D(2), 200)
    if name == "orbital_T":
        # T ∝ a^{3/2}/sqrt(mu_eff)；mu_eff 由 r=1 处的势给出（只做结构比较）
        mu_eff = -phi(D(1), beta, lam)
        return w / mu_eff.sqrt()
    raise ValueError(name)


def nonlinear_observable(beta, lam):
    """非线性泛函 Q = ∫ Phi^2 dl：验证结论与泛函是否线性无关。"""
    return simpson(lambda l: phi(D("1.0") + l, beta, lam) ** 2, D(0), D(2), 200)


def d_lambda(Qfun, beta, lam, rel_step=D("1e-5")):
    """中心差分 + Richardson 求 dQ/dlambda。"""
    l = Dq(lam)
    h = l * rel_step

    def one(step):
        return (Qfun(l + step) - Qfun(l - step)) / (2 * step)

    a, b = one(h), one(h / 2)
    return (D(4) * b - a) / D(3)


def d_beta(Qfun, beta, lam, h=D("1e-7")):
    b = Dq(beta)

    def one(step):
        return (Qfun(b + step) - Qfun(b - step)) / (2 * step)

    a, bb = one(h), one(h / 2)
    return (D(4) * bb - a) / D(3)
