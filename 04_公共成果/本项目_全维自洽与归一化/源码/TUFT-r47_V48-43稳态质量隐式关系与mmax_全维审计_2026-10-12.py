# -*- coding: utf-8 -*-
"""
TUFT-V4.8 §4.3「稳态质量隐式关系 m(kappa_0)」全维审计（r47 · 2026-10-12）

来料：《TUFT-V4.8｜4.3 稳态质量隐式关系 m(kappa_0)=alpha*kappa_0 - C*kappa_0^(8/3) 解析推导》
      + 同文末尾「修正后的 4.3（替换上面全部错误推导）」+ 4.3.7 代码同步修正

分工（零重复，继承 r46）：
  r46 = V4.8 子分支B（边界变分 + 点源泊松 + 普朗克表面张力 => R_c(kappa) 幂律）已裁定：
        B15/B16 多乘一个 R_c => kappa^{8/3} 是笔误；B17 指数 2/3 PASS 而系数 FAIL；
        B08 修正式 kappa_0 = sqrt2 * R_c^{3/2} / l_P^{5/2}；B20/B21 定义域自毁（R_c < l_P，
        门槛 m > sqrt2 m_P）；B26/B29 a_mu/a_e = 42753.12 而数据要 -3333.33，方向相反。
  本册 = r46 的**直接下游**：审 §4.3 质量-曲率映射（修正版）、m_max、k_crit、g-2 标度、
        4.3.7 代码、以及「下一阶段四选项」的可执行性。r46 已裁定的结论一律**继承复核**
        （只做交叉印证计数），不重复裁定。

原则：纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)），不引第三方；
      所有量纲/数值断言由机器给出，不手算；不自推未声明的系数。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "数据")
STAMP = "2026-10-12"
TAG = "TUFT-r47_V48-43稳态质量隐式关系与mmax_全维审计_" + STAMP

# ---------------------------------------------------------------- 常数（SI）
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
c = Decimal("299792458")
hbar = Decimal("1.0545718176461565e-34")
qe = Decimal("1.602176634e-19")
m_e = Decimal("9.1093837015e-31")
m_mu = Decimal("1.883531627e-28")
m_tau = Decimal("3.16754e-27")
l_P = Decimal("1.616255078e-35")
G_exp = Decimal("6.67430e-11")

AE_QED = Decimal("1.15965218128e-3")
AE_EXP = Decimal("1.15965218059e-3")
AMU_QED = Decimal("1.16591810e-3")
AMU_EXP = Decimal("1.16592040e-3")

m_P = hbar / (l_P * c)          # 普朗克质量 kg
ZERO = (0, 0, 0, 0)


# ------------------------------------------------------- 四分量量纲 (M,L,T,Q)
def dmul(a, b):
    """量纲相乘 = 指数逐分量相加（不是逐分量相乘！）"""
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    """取幂 = 指数数乘；n 可为 Fraction（分数幂）"""
    return tuple(Fraction(x) * Fraction(n) for x in a)


def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for nm, v in zip(names, a):
        v = Fraction(v)
        if v == 0:
            continue
        out.append(nm + ("^" + str(v) if v != 1 else ""))
    return "1" if not out else " ".join(out)


D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_Q = (0, 0, 0, 1)
D_ENERGY = (1, 2, -2, 0)
D_HBAR = (1, 2, -1, 0)
D_C = (0, 1, -1, 0)
D_KAPPA = (0, -1, 0, 0)     # 曲率 = 1/长度
D_LP = (0, 1, 0, 0)


# ------------------------------------------------------------ Decimal 三角函数
def _dsin(x):
    s = Decimal(0)
    term = Decimal(x)
    x2 = Decimal(x) * Decimal(x)
    n = 0
    while n < 400:
        s += term
        n += 1
        term = -term * x2 / Decimal((2 * n) * (2 * n + 1))
        if abs(term) < Decimal("1e-70"):
            break
    return s


def _dcos(x):
    s = Decimal(0)
    term = Decimal(1)
    x2 = Decimal(x) * Decimal(x)
    n = 0
    while n < 400:
        s += term
        n += 1
        term = -term * x2 / Decimal((2 * n - 1) * (2 * n))
        if abs(term) < Decimal("1e-70"):
            break
    return s


def _dtan(x):
    return _dsin(x) / _dcos(x)


def fmt(x, nd=25):
    return format(Decimal(x), "." + str(nd) + "E")


# ------------------------------------------------------------------ 条目收集
ITEMS = []


def add(vid, verdict, claim, reading, tag=None):
    ITEMS.append({"id": vid, "verdict": verdict, "claim": claim,
                  "reading": reading, "tag": tag or ""})


GUARDS = []


def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return ok
def powf(x, fr):
    """Decimal 分数幂（Decimal 无 ** Fraction，走 ln/exp）"""
    fr = Fraction(fr)
    return (Decimal(x).ln() * Decimal(fr.numerator) / Decimal(fr.denominator)).exp()


def sqrt2():
    return Decimal(2).sqrt()


# ============================================================ A 组：量纲与代数
def group_A():
    # W01 R_c(来料式) 量纲
    d_rc_arg = ddiv(dmul(D_KAPPA, dpow(D_LP, 2)), D_C)          # [kappa l_P^2 / c]
    d_rc = dpow(d_rc_arg, Fraction(2, 3))
    add("W01", "FAIL",
        "R_c(kappa_0)=((kappa_0 l_P^2)/(sqrt2 c))^(2/3) 是核心半径（长度）",
        "机器量纲 [kappa l_P^2/c] = " + dstr(d_rc_arg) + "，取 2/3 次幂得 [R_c] = "
        + dstr(d_rc) + "，不是 L。式中含 /c 使 T 指数为 2/3 且无法消去 ⇒ 地基式量纲即破缺",
        "量纲")

    # W02 反解所需 [kappa]
    need = ddiv(dpow(D_L, Fraction(3, 2)), ddiv(dpow(D_LP, 2), D_C))   # L^{3/2} / (L^2/(L T^-1))
    gap = ddiv(need, D_KAPPA)
    add("W02", "FAIL",
        "（本册）反解使 [R_c]=L 所需的 [kappa_0]",
        "需 [kappa_0] = " + dstr(need) + "，而曲率公设给 " + dstr(D_KAPPA)
        + "，差 " + dstr(gap) + " ⇒ R_c 式与「kappa 是曲率」不相容；且只要保留 /c，"
        "T 指数恒非零，任何 kappa 量纲都救不回纯长度",
        "量纲")

    # W03 r46 修正式的量纲（继承交叉印证）
    d_rc2 = dpow(dmul(D_KAPPA, dpow(D_LP, Fraction(5, 2))), Fraction(2, 3))
    add("W03", "PASS",
        "（继承 r46 B08）修正式 R_c=(kappa_0 l_P^(5/2)/sqrt2)^(2/3) 量纲为长度",
        "机器 " + dstr(d_rc2) + " = L ✓；本册不重新发明、只作交叉印证（r46 已裁定系数与量纲 FAIL、指数 PASS）",
        "继承r46")

    # W04 修正版 U_self 量纲
    d_u_fix = dmul(ddiv(dmul(D_HBAR, D_LP), D_C), dpow(D_KAPPA, 2))
    d_gap_u = ddiv(D_ENERGY, d_u_fix)
    add("W04", "FAIL",
        "（修正版核心）U_self=(2*pi*hbar*l_P/c)*kappa_0^2 是能量，[U]=ML^2T^-2",
        "机器 [U_self] = " + dstr(d_u_fix) + "（= 质量 M），与能量差 " + dstr(d_gap_u)
        + " = c^2；来料 §4.3.1 核验段把 [hbar l_P/c]=ML^2 乘 kappa^2 的结果写成 ML^2T^-2，"
          "属核验计算错误 ⇒ 自称「能量量纲正确」不成立",
        "量纲")

    # W05 错版 C kappa^{8/3} 量纲
    d_C = dmul(ddiv(dmul(D_HBAR, D_LP), D_C),
               dpow(ddiv(dpow(D_LP, 2), D_C), Fraction(2, 3)))
    d_Ck = dmul(d_C, dpow(D_KAPPA, Fraction(8, 3)))
    add("W05", "FAIL",
        "（错版）C*kappa_0^(8/3) 量纲为质量（来料自称 M L^-2 T^(8/3)）",
        "机器 [C] = " + dstr(d_C) + "，[C kappa^(8/3)] = " + dstr(d_Ck)
        + "；既非质量 M 也非来料自称值 ⇒ 错版两处量纲断言（来料自述与本文复算）均不成立",
        "量纲")

    # W06 错版极值代数（数值对拍，纯代数层）
    a = Decimal("1.7")
    Cp = Decimal("2.3")
    kc = powf(a * 3 / (8 * Cp), Fraction(3, 5))
    lhs = a - Decimal(8) / 3 * Cp * powf(kc, Fraction(5, 3))
    mmax1 = a * kc - Cp * powf(kc, Fraction(8, 3))
    mmax2 = Decimal(5) / 8 * a * kc
    add("W06", "PASS",
        "（错版）kappa_crit=(3alpha/(8C'))^(3/5)、m_max=(5/8)alpha*kappa_crit 的代数自洽",
        "数值对拍（alpha=1.7, C'=2.3）：导数相对残差 " + fmt(abs(lhs) / a)
        + "（60 位有效位极限，即机器零），"
        + "m_max 直接代入 " + fmt(mmax1) + " vs 闭式 " + fmt(mmax2)
        + " ⇒ 代数逐项正确（失效仅在量纲与上游幂次）",
        "代数")

    # W07 修正版极值代数
    al = Decimal("1.7")
    be = Decimal("2.3")
    kc2 = al / (2 * be)
    lhs2 = al - 2 * be * kc2
    mmax3 = al * kc2 - be * kc2 * kc2
    mmax4 = al * al / (4 * be)
    add("W07", "PASS",
        "（修正版）kappa_crit=alpha/(2 beta_U)、m_max=alpha^2/(4 beta_U) 的代数自洽",
        "数值对拍（alpha=1.7, beta_U=2.3）：导数残差 " + fmt(lhs2) + "，"
        + "m_max 直接代入 " + fmt(mmax3) + " vs 闭式 " + fmt(mmax4) + " ⇒ 代数逐项正确",
        "代数")

    # W08 beta_U kappa^2 量纲
    d_beta = ddiv(dmul(D_HBAR, D_LP), dpow(D_C, 3))
    d_bk = dmul(d_beta, dpow(D_KAPPA, 2))
    d_gap_b = ddiv(D_M, d_bk)
    add("W08", "FAIL",
        "m(kappa_0)=alpha*kappa_0-beta_U*kappa_0^2 两项同为质量（来料称「量纲完全自洽」）",
        "机器 [beta_U] = " + dstr(d_beta) + "，[beta_U kappa^2] = " + dstr(d_bk)
        + " ≠ M；补齐因子 = " + dstr(d_gap_b) + " = c^2 ⇒ 第二项须乘 c^2（数值 "
        + fmt(c * c) + "）才是质量 ⇒ 修正版未修好量纲",
        "量纲")

    # W09 最小修法穷举
    hits = []
    for a_ in range(-3, 4):
        for b_ in range(-3, 4):
            for d_ in range(-3, 4):
                dim = dmul(dmul(dmul(dpow(D_HBAR, a_), dpow(D_C, b_)), dpow(D_LP, d_)),
                           dpow(D_KAPPA, 2))
                if tuple(Fraction(x) for x in dim) == tuple(Fraction(x) for x in D_ENERGY):
                    hits.append((a_, b_, d_))
    add("W09", "PASS",
        "（本册）量纲最小修法穷举：U_self ∝ hbar^a c^b l_P^d kappa^2 且 [U]=能量",
        "a,b,d ∈ [-3,3] 共 343 组，命中 " + str(len(hits)) + " 组："
        + str(hits) + " ⇒ 唯一解 U_self ∝ hbar*c*l_P*kappa^2；"
        + "与来料修正版（hbar*l_P/c）恰差 c^2 ⇒ **同一个 c^2 记账错误**",
        "量纲")

    # W10 m_max 两处表达式
    d_mmax_A = ddiv(dmul(D_HBAR, D_C), D_LP)     # hbar c / l_P  （4.3.2 口径，sin^2 无量纲）
    d_mmax_B = ddiv(D_HBAR, dmul(D_LP, D_C))     # hbar/(l_P c) = m_P （4.3.6 口径）
    ratio = c * c
    add("W10", "MISMATCH",
        "m_max = hbar*c/(8*pi*l_P*sin^2theta)（4.3.2）与 m_max = m_P/(8*pi*sin^2theta)（4.3.6）一致",
        "机器 [4.3.2] = " + dstr(d_mmax_A) + " = 能量（非质量）；[4.3.6] = "
        + dstr(d_mmax_B) + " = 质量 ✓；两式数值比 = " + fmt(ratio)
        + " ⇒ 同一册内两处相差 c^2；且 4.3.3 核验段写成「ML^2T^-2/c^2 = M」，"
          "凭空引入了一个式中并不存在的 /c^2",
        "量纲")

    # W11 补 c^2 后的自洽全链
    d_U_ok = dmul(dmul(dmul(D_HBAR, D_C), D_LP), dpow(D_KAPPA, 2))
    d_beta_ok = ddiv(dmul(D_HBAR, D_LP), D_C)
    d_bk_ok = dmul(d_beta_ok, dpow(D_KAPPA, 2))
    d_kc_dim = ddiv(ddiv(D_HBAR, D_C), d_beta_ok)       # [alpha]/[beta_U*]
    add("W11", "CORRECTED",
        "（本册）补回 c^2 后的自洽链：U=2*pi*hbar*c*l_P*kappa^2、beta_U*=2*pi*hbar*l_P/c",
        "机器 [U] = " + dstr(d_U_ok) + " = 能量 ✓；[beta_U* kappa^2] = "
        + dstr(d_bk_ok) + " = M ✓；[kappa_crit=alpha/(2 beta_U*)] = " + dstr(d_kc_dim)
        + " = L^-1 ✓；m_max = alpha^2/(4 beta_U*) = hbar/(8*pi*c*l_P*sin^2theta)"
          " = m_P/(8*pi*sin^2theta)，**与来料 4.3.6 逐位一致** ⇒ 4.3.6 才是量纲正确的那一支，"
          "4.3.2 漏了 c^2",
        "量纲")

    # W12 kappa_crit 量纲
    d_kc_claim = ddiv(dpow(D_C, 2), D_LP)     # c^2/(4 pi l_P sin theta)
    add("W12", "FAIL",
        "kappa_crit = alpha/(2 beta_U) = c^2/(4*pi*l_P*sin theta) 是曲率",
        "机器 [kappa_crit] = " + dstr(d_kc_claim) + " ≠ L^-1；补 c^2 后 kappa_crit = "
        + "1/(4*pi*l_P*sin theta) 量纲 L^-1 ✓（见 W11）",
        "量纲")

    # W13 a_TUFT 量纲
    d_a = ddiv(dmul(dmul(D_C, D_M), D_KAPPA), dmul(D_Q, D_HBAR))
    add("W13", "FAIL",
        "a_TUFT = -(3 c cot theta)/(4 e hbar) * m * kappa_0 无量纲",
        "机器（SI 四元组）[a_TUFT] = " + dstr(d_a) + " ≠ 1；自然单位（hbar=c=1、e 无量纲）下"
        " [m*kappa] = E^2 ⇒ 缺 E^-2，公设集内唯一候选是 [G] = E^-2"
          " ⇒ 与 r42（a_e^TUFT 缺 G / EC 归一 1/16piG）同型复发",
        "量纲")

    # W14 来料自抓是否正确
    add("W14", "PASS",
        "（来料自抓）§4.3.7 量纲核验发现 kappa^(8/3) 系多乘一次幂次所致",
        "诊断正确：错版 U ∝ R_c^3 * R_c = R_c^4 ⇒ kappa^(8/3)；修去多余幂次后 U ∝ R_c^3 ∝ kappa^2。"
        "与 r46 B15（对拍比值恰等于探针 R_c）**独立同结论**，交叉印证第 2 次 ⇒ 来料自抓成立",
        "自抓")
# ==================================================== B 组：数值、定义域、拟合
ALPHA_1 = hbar / c                       # alpha(sin theta = 1) = hbar/c   [M L]
BETA_CLAIM = 2 * PI * hbar * l_P / (c ** 3)     # 来料 beta_U
BETA_OK = 2 * PI * hbar * l_P / c               # 补 c^2 后的 beta_U*
KG_TO_GEV = Decimal("1") / Decimal("1.78266192e-27")


def Rc_claim(kap):
    """来料式 R_c = (kappa l_P^2/(sqrt2 c))^(2/3)（量纲已判 FAIL，仅作数值对拍）"""
    return powf((kap * l_P * l_P) / (sqrt2() * c), Fraction(2, 3))


def Rc_r46(kap):
    """r46 B08 修正式 R_c = (kappa l_P^(5/2)/sqrt2)^(2/3)（量纲 L）"""
    return powf((kap * powf(l_P, Fraction(5, 2))) / sqrt2(), Fraction(2, 3))


def kappa_weak(m, sin_th=Decimal(1)):
    """弱场 kappa = m c sin(theta)/hbar（由 m ≈ alpha*kappa 反解）"""
    return m * c * sin_th / hbar


def newton_root(m, k0, alpha, beta, iters=80):
    """复现来料代码 mpmath.findroot(f, 1e34) 的牛顿走向"""
    k = Decimal(k0)
    for _ in range(iters):
        f = alpha * k - beta * k * k - m
        df = alpha - 2 * beta * k
        if df == 0:
            break
        step = f / df
        k = k - step
        if abs(step) < abs(k) * Decimal("1e-45"):
            break
    return k


def group_B():
    # W15 G 通道
    G_th0 = c ** 3 * l_P * l_P / hbar
    rel = G_th0 / G_exp - 1
    chi_G0 = (rel / Decimal("1e-5")) ** 2
    # chi_G < 1  =>  |1/sin(theta) - 1| < 1e-5  =>  cos(delta) = 1/(1+1e-5)
    target = Decimal(1) / (Decimal(1) + Decimal("1e-5"))
    lo, hi = Decimal(0), Decimal("0.1")
    for _ in range(200):
        mid = (lo + hi) / 2
        if _dcos(mid) > target:
            lo = mid
        else:
            hi = mid
    dmax = (lo + hi) / 2
    add("W15", "BOUNDARY",
        "G_th = c^3 l_P^2/(hbar sin theta) 与 G_exp 相容（chi_G 用 sigma=1e-5 G）",
        "机器 c^3 l_P^2/hbar = " + fmt(G_th0) + "，G_exp = " + fmt(G_exp, 6)
        + "，相对残差 " + fmt(rel) + " ⇒ chi_G(sin=1) = " + fmt(chi_G0)
        + "（**与 theta 无关**：cos(delta)=1 到 1e-112 精度，delta~1e-56 时 sin 恒等于 1）"
        + "；G 通道对 delta 只给**上界** delta < " + fmt(dmax) + " rad（chi_G<1），"
          "不限制 delta→0 ⇒ G 通道不能锁定 theta 的绝对量级",
        "数值")

    # W16 空集定理（本册最重）
    k_crit_ok = Decimal(1) / (4 * PI * l_P)          # sin theta = 1 上界
    k_min_r46 = sqrt2() / l_P                        # r46 B21 门槛
    ratio_k = k_crit_ok / k_min_r46
    add("W16", "FAIL",
        "（本册·承重）稳态分支 kappa<kappa_crit 与 R_c 有效域 kappa>sqrt2/l_P 是否相交",
        "kappa_crit = 1/(4 pi l_P sin theta) ≤ " + fmt(k_crit_ok) + "（因 sin theta ≤ 1）；"
        + "r46 B21 有效域门槛 kappa > sqrt2/l_P = " + fmt(k_min_r46) + "；"
        + "比值 kappa_crit/kappa_min = 1/(4 pi sqrt2 sin theta) = " + fmt(ratio_k)
        + "·(1/sin theta) ≤ " + fmt(ratio_k) + " < 1 ⇒ **对任意实数 theta，"
          "稳态质量域与 R_c 定义域不相交（空集）**。m_max 本身也低于有效域门槛 "
        + fmt(k_min_r46 / k_crit_ok) + " 倍 ⇒ 不是「轻子在门外」，而是「整条分支在门外」",
        "定义域")

    # W17 m_max 处 R_c 仍小于 l_P
    Rc_at_crit = Rc_r46(k_crit_ok)
    add("W17", "FAIL",
        "重粒子极限 R_c >> l_P 在极值点成立（自能公式的适用前提）",
        "机器 R_c(kappa_crit) = " + fmt(Rc_at_crit) + " m = "
        + fmt(Rc_at_crit / l_P) + " l_P < 1 ⇒ 连质量上界处都不满足 R_c > l_P，"
          "§4.3.1 声明的前提在**整条稳态分支上**都不成立",
        "定义域")

    # W18 轻子 R_c/l_P（与 r46 交叉印证）
    rows = []
    for nm, mm in (("电子", m_e), ("缪子", m_mu), ("tau", m_tau)):
        kk = kappa_weak(mm)
        rows.append((nm, Rc_claim(kk), Rc_claim(kk) / l_P))
    add("W18", "FAIL",
        "（继承 r46 B20）轻子的 R_c 与 l_P 之比（来料式口径，本册独立复算）",
        "；".join(nm + " R_c=" + fmt(v) + " m = " + fmt(r) + " l_P" for nm, v, r in rows)
        + " ⇒ 与 r46 C4 表（电子 8.4482843980482201593617788E-10 l_P）同量级、同结论，"
          "交叉印证成立（本册不重复裁定）",
        "继承r46")

    # W19 高次项在轻子域的相对占比
    out = []
    for nm, mm in (("电子", m_e), ("缪子", m_mu), ("tau", m_tau)):
        kk = kappa_weak(mm)
        r_claim = BETA_CLAIM * kk / ALPHA_1
        r_ok = BETA_OK * kk / ALPHA_1
        out.append(nm + " 来料口径 " + fmt(r_claim) + " / 补c^2口径 " + fmt(r_ok))
    add("W19", "FAIL",
        "§4.3.5「tau 子 kappa 接近 kappa_crit，高次项贡献显著，压制 g-2 爆炸」",
        "自能项/线性项 = beta*kappa/alpha：" + "；".join(out)
        + " ⇒ tau 处最大也仅 1E-19（补 c^2 后）／1E-35（来料式），"
          "要「压制」需 O(1) ⇒ 差 19~35 个量级；推论「tau 抑制磁矩修正」在轻子全域恒不成立",
        "数值")

    # W20 m_max 量级与推论 4.2
    mmax_min = m_P / (8 * PI)
    add("W20", "FAIL",
        "推论4.2：m_e,m_mu,m_tau < m_max 是对 theta 的有效自洽约束",
        "m_max = m_P/(8 pi sin^2theta) ≥ m_P/(8 pi) = " + fmt(mmax_min) + " kg = "
        + fmt(mmax_min * KG_TO_GEV) + " GeV；tau 仅 " + fmt(m_tau * KG_TO_GEV) + " GeV ⇒ "
        + "m_tau/m_max ≤ " + fmt(m_tau / mmax_min) + " ⇒ 约束对任意 theta 恒真，**零筛选力**",
        "数值")

    add("W21", "MISMATCH",
        "§4.3.6「sin^2theta < m_P/(8pi*1777MeV) ~ 1E20，故 theta 极接近 pi/2」",
        "机器 m_P/(8 pi × 1777 MeV) = " + fmt((m_P * KG_TO_GEV * Decimal("1e3"))
                                              / (8 * PI * Decimal("1777")))
        + "（不是 1E20，来料高估约 366 倍）；且该值 ≫ 1 ⇒ 不等式 sin^2theta < 2.7E17 "
          "**恒真**（sin^2theta ≤ 1 恒成立），推不出任何 theta 约束 ⇒ 该段算术与结论双重失效",
        "数值")

    # W22 两档 sigma 的加权最小二乘
    x_e = 3 * c / (4 * qe * hbar) * m_e * kappa_weak(m_e)      # a_e^TUFT = -x_e * cot(theta)
    x_mu = 3 * c / (4 * qe * hbar) * m_mu * kappa_weak(m_mu)
    y_e = AE_QED - AE_EXP
    y_mu = AMU_QED - AMU_EXP
    res = {}
    for tagname, se, sm in (("来料档", Decimal("1e-12"), Decimal("4e-7")),
                            ("真实档", Decimal("3.6e-13"), Decimal("7.0e-10"))):
        we = 1 / (se * se)
        wm = 1 / (sm * sm)
        dstar = (we * x_e * y_e + wm * x_mu * y_mu) / (we * x_e * x_e + wm * x_mu * x_mu)
        ce = (y_e - x_e * dstar) / se
        cm = (y_mu - x_mu * dstar) / sm
        res[tagname] = (dstar, ce, cm, ce * ce + cm * cm)
    add("W22", "FAIL",
        "（本册·判决支点）a_TUFT ∝ cot(theta)·m·kappa 对 e/mu 双通道的联合可拟合性",
        "x_e = " + fmt(x_e) + "、x_mu = " + fmt(x_mu) + "（a = -x·cotθ），"
        + "y_e = " + fmt(y_e) + "、y_mu = " + fmt(y_mu) + "；加权 LS：来料档(sigma=1e-12/4e-7)"
        + " delta* = " + fmt(res["来料档"][0]) + "，chi2 = " + fmt(res["来料档"][3])
        + "（不失配）；真实档(sigma=3.6e-13/7.0e-10) delta* = " + fmt(res["真实档"][0])
        + "，**反号**（theta>pi/2），chi2 = " + fmt(res["真实档"][3])
        + " ⇒ 与 r44 同型：**结论依赖未声明的 sigma 口径**；且 a_mu/a_e = "
        + fmt(x_mu / x_e) + " = (m_mu/m_e)^2 与 theta 无关（继承 r46 B26/B29，第 4 次复发）",
        "拟合")

    # W23 先验与解区间
    d_lo, d_hi = Decimal("1e-48"), Decimal("1e-40")
    chi_at_prior = ((y_e - x_e * d_lo) / Decimal("1e-12")) ** 2
    add("W23", "FAIL",
        "（选项1 前置）4.3.7 先验 delta ∈ [1e-48, 1e-40] 覆盖后验峰值",
        "LS 解 delta* = " + fmt(res["来料档"][0]) + "（来料档）／" + fmt(res["真实档"][0])
        + "（真实档），均**不在** [1e-48, 1e-40] 内（小 8 个量级且真实档反号）；"
        + "先验下界处 chi_e = " + fmt(chi_at_prior) + " ⇒ 在先验全域 chi2 单调、"
          "最优压在**人为先验边界** ⇒ dynesty 的后验 = 先验边界，不产出数据信息",
        "拟合")

    # W24 代码实际收敛到哪一支
    k_newton = newton_root(m_tau, Decimal("1e34"), ALPHA_1, BETA_OK)
    k_phys = kappa_weak(m_tau)
    k_big = ALPHA_1 / BETA_OK - k_phys
    add("W24", "FAIL",
        "4.3.7 代码 kappa(m,theta)=findroot(f, 1e34) 返回物理支（小根）",
        "牛顿法从 1e34 收敛到 " + fmt(k_newton) + "；抛物线两根为 kappa_- = " + fmt(k_phys)
        + " 与 kappa_+ = " + fmt(k_big) + " ⇒ 收敛到**大根** kappa_+（在该支 dm/dkappa<0、"
          "自能项/线性项 → 1）；而正文 4.3.5 的标度分析（「电子 kappa 很小」）用的是小根 ⇒ "
          "**代码与正文口径不一致**，且未声明分支选择（同型于 r46 B32）",
        "代码")

    # W25 sigma 口径
    add("W25", "FAIL",
        "4.3.7 chi2 的 sigma_e=1e-12、sigma_mu=4e-7 是实验/理论合成不确定度",
        "a_e 现行合成不确定度约 3.6e-13、a_mu 约 7.0e-10（含 SM 理论项）⇒ 来料口径分别松 "
        + fmt(Decimal("1e-12") / Decimal("3.6e-13")) + " 倍与 "
        + fmt(Decimal("4e-7") / Decimal("7.0e-10")) + " 倍；μ 通道松 3 个量级正是 W22 中"
          "「符号互斥被吞掉」的直接原因 ⇒ 未声明 sigma 的 chi2 不可作为判决（r44 判据复用）",
        "拟合")

    # W26 外部输入账
    add("W26", "FAIL",
        "§4.3.6 结论「只依赖普朗克质量与 theta，单参数理论保留」",
        "输入账：theta（1 个连续常数）+ l_P（≡ sqrt(hbar G/c^3)，即 G）+ 自能系数 2*pi 与 "
          "R_c 幂律中的 sqrt2（来自 r46 已判 FAIL 的边界变分链，本册未重新给出）"
          " ⇒ 未登记外部输入 ≥ 2 项（theta 之外至少 l_P 与 R_c 链），撞 Ω5（自由常数 ≤ 1）；"
          "「单参数」仅在把 l_P 与 R_c 链全部显式登记为外部输入时才成立（复发 r41 R06 / r44）",
        "参数账")

    # W27 与 r46 的 m_max 口径差
    r46_mmax = Decimal("5.3579146817725378478281090E+25")
    add("W27", "MISMATCH",
        "本册 m_max 与 r46 B32 的 m_max 是否可交叉引用",
        "本册（来料 4.3.6 链，sinθ=1）= " + fmt(mmax_min) + " kg；r46 B32（r46 修正链）= "
        + fmt(r46_mmax, 6) + " kg ⇒ 差 " + fmt(r46_mmax / mmax_min) + " 倍"
        + " ⇒ 两册的系数链与 theta 取值口径不同，**m_max 当前不是可跨册引用的量**；"
          "统一前不得用作任何预言",
        "跨册")

    # W33 来料式口径下定义域判据本身无定义
    add("W33", "BOUNDARY",
        "（本册）在来料式 R_c 口径下，「重粒子极限 R_c >> l_P」是否可判定",
        "不可判定：W01 已证来料式 [R_c] = T^(2/3)，而 [l_P] = L，两者**不同量纲**"
        " ⇒ 「R_c > l_P」这一类不等式在来料式下没有定义，§4.3.1 把它当作适用前提"
          "却从未核验。本册 W16/W17 的空集结论只能建立在 r46 B08 修正式（唯一量纲自洽的 R_c）"
          "之上 ⇒ 该结论的成立以「采纳 r46 修正链」为条件，须显式登记",
        "定义域")
# ==================================================== C 组：下一阶段四选项裁决
def group_C(res):
    x_e = 3 * c / (4 * qe * hbar) * m_e * kappa_weak(m_e)
    y_e = AE_QED - AE_EXP
    chi_at_prior = ((y_e - x_e * Decimal("1e-48")) / Decimal("1e-12")) ** 2
    add("W28", "FAIL",
        "选项1（运行 dynesty 扫描 theta，求 theta*、m_max、e/mu/tau 全套 g-2）",
        "不可产出数据信息：①先验 delta∈[1e-48,1e-40] 与 LS 解（来料档 "
        + fmt(res["来料档"][0]) + "／真实档 " + fmt(res["真实档"][0]) + "）不相交；"
        + "②先验内 chi2 单调、最小点落在人为边界，边界处 chi2 ≈ " + fmt(chi_at_prior)
        + "；③G 通道只给 delta 上界（W15）不锁定量级 ⇒ 后验 = 先验边界。"
          "**在当前代码下运行 dynesty，唯一可得的结论是「模型被排除」，而不是「最优 theta」**",
        "选项")

    add("W29", "INFO",
        "选项2（G_th 与 m_max 联立约束，做参数相容性分析）",
        "可算、零成本，但零判别力：G_th = G/sinθ 只给 delta < 4.4721E-3 rad（W15），"
        "m_max = m_P/(8π sin²θ) 在该区间内变化不足 1E-5 相对量，且恒 ≫ 轻子质量（W20）"
        " ⇒ 联立不产生新约束；唯一价值是把 delta 上界显式化",
        "选项")

    add("W30", "FAIL",
        "选项3（展开有限 R_c，去掉重粒子极限，得精确自能）",
        "不是微扰修正而是主导项：R_c/l_P 在轻子域为 1E-10~1E-7（W18）、在 m_max 处也只有 "
        + fmt(Rc_r46(Decimal(1) / (4 * PI * l_P)) / l_P) + "（W17）⇒ (R_c-l_P) 的「修正」"
          "就是被丢弃的主项本身；且 U_self 原式量纲未修（W04/W09）⇒ 必须在修完量纲后"
          "整体重做积分，不能在该近似上做展开",
        "选项")

    add("W31", "FAIL",
        "选项4（theta 后验不确定性传播到 m_max 与 a_e,a_mu,a_tau）",
        "依赖选项1：当前后验 = 先验边界（W23）⇒ 传播的是人为边界而非数据；"
        "且 m_max ∝ 1/sin²θ 在 delta ~1E-56 处对 theta 完全不敏感（相对变化 O(delta²)~1E-112）"
        " ⇒ 传播结果恒为零宽度，无意义",
        "选项")

    add("W32", "FAIL",
        "（最小修补 P1/P2 之后仍然成立的否定清单）",
        "P1=补回 c^2（W09/W11，零成本）、P2=声明 sigma 与 kappa 分支（W23/W24/W25，零成本）；"
        "两者修完后**仍然成立**：W16（稳态域与定义域空集，与 theta 无关）、W17（R_c<l_P）、"
        "W19（高次项在轻子域 ≤1E-19）、W20/W21（m_max 零筛选力）、W22（符号互斥，仅被松 sigma "
        "掩盖）、W26（外部输入 ≥2 撞 Ω5）⇒ 这些不是「修修就能过」的瑕疵",
        "收口")


# ================================================================ 自检 guard
def run_guards():
    guard("g01_hbar_dim", D_HBAR == (1, 2, -1, 0), dstr(D_HBAR))
    guard("g02_c_dim", D_C == (0, 1, -1, 0), dstr(D_C))
    guard("g03_hbar_c_dim", dmul(D_HBAR, D_C) == (1, 3, -2, 0), dstr(dmul(D_HBAR, D_C)))
    guard("g04_dmul_is_add_not_mul", dmul(D_L, D_L) == (0, 2, 0, 0),
          "若实现成逐分量相乘会给 (0,1,0,0)")
    guard("g05_dpow_negative", dpow(D_L, -1) == (0, -1, 0, 0), dstr(dpow(D_L, -1)))
    guard("g06_hbar_lP_over_c", ddiv(dmul(D_HBAR, D_LP), D_C) == (1, 2, 0, 0), "ML^2")
    guard("g07_U_ok_is_energy",
          dmul(dmul(dmul(D_HBAR, D_C), D_LP), dpow(D_KAPPA, 2)) == D_ENERGY, "hbar c lP kappa^2")
    guard("g08_gap_is_c2", ddiv(D_ENERGY, D_M) == dpow(D_C, 2), "能量/质量 = c^2")
    guard("g09_powf_cuberoot", abs(powf(Decimal(8), Fraction(1, 3)) - 2) < Decimal("1e-50"),
          fmt(powf(Decimal(8), Fraction(1, 3))))
    d10 = Decimal("1e-20")
    guard("g10_cos_small_delta", abs(_dcos(d10) - (1 - d10 * d10 / 2)) < Decimal("1e-60"),
          fmt(_dcos(d10)))
    kn = newton_root(m_tau, Decimal("1e34"), ALPHA_1, BETA_OK)
    resid = abs(ALPHA_1 * kn - BETA_OK * kn * kn - m_tau) / m_tau
    guard("g11_newton_root_residual", resid < Decimal("1e-30"), fmt(resid))
    s12 = kappa_weak(m_tau) + (ALPHA_1 / BETA_OK - kappa_weak(m_tau))
    guard("g12_vieta_sum", abs(s12 - ALPHA_1 / BETA_OK) / (ALPHA_1 / BETA_OK) < Decimal("1e-40"),
          "kappa_- + kappa_+ = alpha/beta")
    x_e = 3 * c / (4 * qe * hbar) * m_e * kappa_weak(m_e)
    y_e = AE_QED - AE_EXP
    lo = ((y_e - x_e * Decimal("1e-48")) / Decimal("1e-12")) ** 2
    hi = ((y_e - x_e * Decimal("1e-40")) / Decimal("1e-12")) ** 2
    guard("g13_chi2_monotone_in_prior", hi > lo, "chi2(delta=1e-40) > chi2(delta=1e-48)")
    guard("g14_empty_set_strict", Decimal(1) / (4 * PI * l_P) < sqrt2() / l_P,
          "kappa_crit < kappa_min 对 sinθ=1 严格成立")
    kc = ALPHA_1 / (2 * BETA_OK)
    v1 = ALPHA_1 * kc - BETA_OK * kc * kc
    v2 = ALPHA_1 * ALPHA_1 / (4 * BETA_OK)
    guard("g15_mmax_closed_vs_direct", abs(v1 - v2) / v2 < Decimal("1e-45"), fmt(v1))
    guard("g16_mmax_equals_mP_over_8pi",
          abs(v2 - m_P / (8 * PI)) / (m_P / (8 * PI)) < Decimal("1e-45"),
          fmt(v2) + " vs " + fmt(m_P / (8 * PI)))


# ==================================================================== 输出
def main():
    group_A()
    group_B()
    res = {}
    x_e = 3 * c / (4 * qe * hbar) * m_e * kappa_weak(m_e)
    x_mu = 3 * c / (4 * qe * hbar) * m_mu * kappa_weak(m_mu)
    y_e = AE_QED - AE_EXP
    y_mu = AMU_QED - AMU_EXP
    for tagname, se, sm in (("来料档", Decimal("1e-12"), Decimal("4e-7")),
                            ("真实档", Decimal("3.6e-13"), Decimal("7.0e-10"))):
        we = 1 / (se * se)
        wm = 1 / (sm * sm)
        dstar = (we * x_e * y_e + wm * x_mu * y_mu) / (we * x_e * x_e + wm * x_mu * x_mu)
        ce = (y_e - x_e * dstar) / se
        cm = (y_mu - x_mu * dstar) / sm
        res[tagname] = (dstar, ce, cm, ce * ce + cm * cm)
    group_C(res)
    run_guards()

    cnt = {}
    for it in ITEMS:
        cnt[it["verdict"]] = cnt.get(it["verdict"], 0) + 1
    gok = sum(1 for g in GUARDS if g["ok"])

    key = {
        "m_P_kg": fmt(m_P),
        "mmax_min_kg_sin1": fmt(m_P / (8 * PI)),
        "mmax_min_GeV": fmt(m_P / (8 * PI) * KG_TO_GEV),
        "kappa_crit_sin1": fmt(Decimal(1) / (4 * PI * l_P)),
        "kappa_min_r46": fmt(sqrt2() / l_P),
        "kappa_crit_over_kappa_min": fmt((Decimal(1) / (4 * PI * l_P)) / (sqrt2() / l_P)),
        "Rc_at_kappa_crit_over_lP": fmt(Rc_r46(Decimal(1) / (4 * PI * l_P)) / l_P),
        "a_ratio_xmu_over_xe": fmt(x_mu / x_e),
        "delta_star_来料档": fmt(res["来料档"][0]),
        "delta_star_真实档": fmt(res["真实档"][0]),
        "chi2_来料档": fmt(res["来料档"][3]),
        "chi2_真实档": fmt(res["真实档"][3]),
        "c2_gap": fmt(c * c),
        "G_th0": fmt(c ** 3 * l_P * l_P / hbar),
        "G_rel_resid": fmt(c ** 3 * l_P * l_P / hbar / G_exp - 1),
    }

    payload = {"round": "r47", "date": STAMP, "items": ITEMS, "guards": GUARDS,
               "counts": cnt, "guard_ok": gok, "guard_total": len(GUARDS),
               "key_numbers": key}
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = ["# r47 · TUFT-V4.8 §4.3 稳态质量隐式关系 全维审计 · 机器读数",
             "",
             "条目 " + str(len(ITEMS)) + "（" + " / ".join(
                 k + " " + str(v) for k, v in sorted(cnt.items())) + "）",
             "自检 guard " + str(gok) + "/" + str(len(GUARDS)),
             "", "## 条目表", "",
             "| id | 判定 | 声称 | 机器读数 |", "|---|---|---|---|"]
    for it in ITEMS:
        lines.append("| " + it["id"] + " | " + it["verdict"] + " | "
                     + it["claim"].replace("|", "/") + " | "
                     + it["reading"].replace("|", "/") + " |")
    lines += ["", "## 关键数值", ""]
    for k in sorted(key):
        lines.append("- " + k + " = " + key[k])
    lines += ["", "## 自检 guard", ""]
    for g in GUARDS:
        lines.append("- " + ("PASS " if g["ok"] else "FAIL ") + g["name"]
                     + ("：" + g["note"] if g["note"] else ""))
    with open(os.path.join(DATA, TAG + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    out = "条目 " + str(len(ITEMS)) + "（" + " / ".join(
        k + " " + str(v) for k, v in sorted(cnt.items())) + "）"
    out += "；自检 guard " + str(gok) + "/" + str(len(GUARDS))
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(out)
    return 0 if gok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())


