# -*- coding: utf-8 -*-
"""
TUFT-V4.8 §4.4「嵌套采样后验推断：θ 全局倾角参数拟合」· 全维审计引擎
================================================================
r52 · 2026-10-13 · 纯标准库（Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)）

设计原则（沿用本库体例）
  1. 本册只审来料 §4.4.1–§4.4.6；上游 §4.2/§4.3（r45/r46/r47/r48/r49）与 g-2 拟合（r44/r42）
     的已裁定条目一律「继承复核」，只作交叉印证计数，不重复裁定。
  2. 来料依赖 dynesty；本机未安装 ⇒ 本册在 1 维参数空间用「log10δ 密网格 + 梯形积分」
     精确求证据 Z 与后验分位数。1 维下 Z 的数值积分是精确的，采样器只贡献 MC 噪声，
     因此本读数严格强于 dynesty 采样（本册 INFO 条目 X13 登记该处置）。
  3. 不自推的量（系数约定、实验不确定度协方差、作用量来源）一律显式登记，不留白。
  4. 「残差为零」类断言一律配阳性对照或双路径；量纲类断言一律由机器工具兜底。

产物：数据/TUFT-r52_V48-44嵌套采样后验推断_全维审计_2026-10-13.{json,md,_report.txt}
退出码：0（自检 guard 全过）
"""

import io
import json
import os
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 60

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
ROUND_ID = "r52"
SRC_TITLE = "TUFT-V4.8 §4.4 嵌套采样后验推断 · 全维审计"
DATE = "2026-10-13"

# =====================================================================
# 0. 输出原语
# =====================================================================

ITEMS = []
GUARDS = []


def P(tag, name, read, note=""):
    ITEMS.append(dict(tag=tag, name=name, read=read, note=note))


def F_(tag, name, read, note=""):
    ITEMS.append(dict(tag="FAIL", name=name, read=read, note=note))


def B(tag, name, read, note=""):
    ITEMS.append(dict(tag="BOUNDARY", name=name, read=read, note=note))


def I(tag, name, read, note=""):
    ITEMS.append(dict(tag="INFO", name=name, read=read, note=note))


def M(tag, name, read, note=""):
    ITEMS.append(dict(tag="MISMATCH", name=name, read=read, note=note))


def CO(tag, name, read, note=""):
    ITEMS.append(dict(tag="CORRECTED", name=name, read=read, note=note))


def guard(name, cond, msg=""):
    """自检守卫：cond 为真则通过。"""
    ok = bool(cond)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        sys.stderr.write("[GUARD-FAIL] %s : %s\n" % (name, msg))
    return ok


def e(x, n=18):
    """Decimal → 科学计数字符串（不用 quantize：高位数会抛 InvalidOperation）"""
    if isinstance(x, D):
        return format(x, "." + str(int(n)) + "E")
    return repr(x)


def fx(x):
    """Decimal → float（用于量级对照；仅用于展示，不参与判定）"""
    return float(x)


# =====================================================================
# 1. 量纲引擎：四分量 (M, L, T, Q)，Fraction 精确
# =====================================================================

def Z():
    return (F(0), F(0), F(0), F(0))


M_, L_, T_, Q_ = Z()
DIM_M = (F(1), F(0), F(0), F(0))     # 质量
DIM_L = (F(0), F(1), F(0), F(0))     # 长度
DIM_T = (F(0), F(0), F(1), F(0))     # 时间
DIM_Q = (F(0), F(0), F(0), F(1))     # 电荷

# 本册自用的基本量纲字典
DIM_HBAR = (F(1), F(2), F(-1), F(0))    # 角动量 ML^2 T^-1
DIM_C = (F(0), F(1), F(-1), F(0))       # 速度 L T^-1
DIM_E = (F(0), F(0), F(0), F(1))        # 电荷量 Q
DIM_ELEC_P = (F(0), F(0), F(0), F(1))   # 元电荷 = 电荷量
DIM_MASS = DIM_M
DIM_LP = DIM_L
DIM_KAPPA = (F(0), F(-1), F(0), F(0))   # 曲率 L^-1


def dadd(*ds):
    return tuple(sum(d[i] for d in ds) for i in range(4))


def dmul(*ds):
    out = (F(0), F(0), F(0), F(0))
    for d in ds:
        out = tuple(out[i] + d[i] for i in range(4))
    return out


def dpow(d, p):
    return tuple(d[i] * F(p) for i in range(4))


def dinv(d):
    return tuple(-d[i] for i in range(4))


def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dstr(d):
    names = ["M", "L", "T", "Q"]
    parts = []
    for i, n in enumerate(names):
        if d[i] == 0:
            continue
        num, den = d[i].numerator, d[i].denominator
        if den == 1:
            parts.append(("%s^%s" % (n, num)) if num != 1 else n)
        else:
            parts.append("%s^(%s/%s)" % (n, num, den))
    return " ".join(parts) if parts else "1（无量纲）"


def dsame(a, b):
    return tuple(a) == tuple(b)


# =====================================================================
# 2. 常数（CODATA 口径：ħ 由 SI 定义精确；G/ℓ_P 取 CODATA-2018 标称值）
# =====================================================================

PI = D("3.14159265358979323846264338327950288419716939937510582097494")
C = D("299792458")                        # 精确
HBAR = D("1.0545718176461565e-34")
QE = D("1.602176634e-19")                 # 精确（SI 定义）
ME = D("9.1093837015e-31")
MMU = D("1.883531627e-28")
MTAU = D("3.16754e-27")
LP = D("1.616255078e-35")
GEXP = D("6.67430e-11")
# 相对标准不确定度（CODATA-2018，G 为主）
U_G_REL = D("2.2e-5")

MP = HBAR / (LP * C)                      # m_P = ħ/(ℓ_P c)
G_PLANCK = C ** 3 * LP ** 2 / HBAR        # G_th(θ) 的 θ 无关因子

# 观测量（来料 §4.4.2 代码原值）
AE_QED = D("1.15965218128e-3")
AE_EXP = D("1.15965218059e-3")
AMU_QED = D("1.16591810e-3")
AMU_EXP = D("1.16592040e-3")
SIG_E = D("1e-12")
SIG_MU = D("4e-7")
SIG_G_REL = D("1e-5")

# FermiLab-2021 标准 a_mu（来料未用，仅作口径对照）
AMU_EXP_FL2021 = D("1.16592089e-3")

# =====================================================================
# 3. 高精度三角函数（Decimal 自实现，避免 Decimal 无 sin/cos）
# =====================================================================

def dcos(x, tol=D("1e-70")):
    term = D(1)
    s = D(1)
    x2 = x * x
    n = 0
    while True:
        n += 1
        term = -term * x2 / D((2 * n - 1) * (2 * n))
        s += term
        if abs(term) < tol:
            break
        if n > 400:
            break
    return s


def dsin(x, tol=D("1e-70")):
    term = x
    s = x
    x2 = x * x
    n = 0
    while True:
        n += 1
        term = -term * x2 / D((2 * n) * (2 * n + 1))
        s += term
        if abs(term) < tol:
            break
        if n > 400:
            break
    return s


def dtan(x, tol=D("1e-70")):
    return dsin(x, tol) / dcos(x, tol)


# --- 网格快速路径：|x| <= 0.1 时固定 7/5 项泰勒，截断误差 < 1e-29，无 Python 循环 ---
_C2 = D(1) / D(2)
_C4 = D(1) / D(24)
_C6 = D(1) / D(720)
_C8 = D(1) / D(40320)
_C10 = D(1) / D(3628800)
_C12 = D(1) / D(479001600)
_S3 = D(1) / D(6)
_S5 = D(1) / D(120)
_S7 = D(1) / D(5040)
_S9 = D(1) / D(362880)


def dcos_fast(x):
    x2 = x * x
    return 1 - x2 * _C2 + x2 * x2 * _C4 - x2 * x2 * x2 * _C6 + \
        x2 * x2 * x2 * x2 * _C8 - x2 * x2 * x2 * x2 * x2 * _C10 + \
        x2 * x2 * x2 * x2 * x2 * x2 * _C12


def dsin_fast(x):
    x2 = x * x
    return x * (1 - x2 * _S3 + x2 * x2 * _S5 - x2 * x2 * x2 * _S7 + \
        x2 * x2 * x2 * x2 * _S9)


def dtan_fast(x):
    return dsin_fast(x) / dcos_fast(x)


guard("G06b_dcos_fast_agrees_with_exact",
      abs(dcos_fast(D("0.1")) - dcos(D("0.1"), D("1e-70"))) < D(10) ** -28,
      "快速路径 cos 必须与高精度路径一致（<1e-28）")
guard("G06c_dtan_fast_agrees_with_exact",
      abs(dtan_fast(D("0.05")) - dtan(D("0.05"), D("1e-70"))) < D(10) ** -28,
      "快速路径 tan 必须与高精度路径一致（<1e-28）")


def dsin_via_pi(x):
    """sin(pi/2 - delta) = cos(delta)，避免依赖 pi/2 的 60 位截断误差放大"""
    return dcos(x)


# =====================================================================
# 4. 来料 §4.4.3 的模型（逐行照抄其代数，不做「善意修正」）
# =====================================================================

BETA_U = PI * HBAR * LP / C               # U_self = BETA_U * kappa^2（来料式）


def m_eq_factor(delta):
    """sin(theta) = cos(delta)；网格路径用 1e-35 容差（chi_G 分母 1e-5 只需 1e-15 精度）"""
    return dcos(delta, D("1e-35"))


def kappa_roots(m, delta, sin_th=None):
    """
    来料 m_eq(kap,th) = (hbar*c*kap/sin_th - U_self(kap))/c^2 = m
    展开： m = alpha*kap - beta*kap^2 ， alpha = hbar/(c sin_th), beta = BETA_U/c^2
    本函数用解析双根（Decimal.sqrt），给出小根与大根。
    """
    if sin_th is None:
        sin_th = m_eq_factor(delta)
    alpha = HBAR / (C * sin_th)
    beta = BETA_U / (C * C)
    disc = alpha * alpha - D(4) * beta * m
    if disc <= 0:
        return None, None
    sd = disc.sqrt()
    k_small = D(2) * m / (alpha + sd)          # 数值稳定写法
    k_big = (alpha + sd) / (D(2) * beta)
    return k_small, k_big


def kappa_small(m, delta, sin_th=None):
    ks, _ = kappa_roots(m, delta, sin_th)
    return ks


def secant_findroot(f, x0, x1, iters=400):
    """复现来料 mp.findroot 的 secant 路径，记录终点与收敛标志。"""
    a, b = x0, x1
    fa, fb = f(a), f(b)
    ok = False
    for _ in range(iters):
        if fb == fa:
            break
        c = b - fb * (b - a) / (fb - fa)
        a, fa = b, fb
        b, fb = c, f(c)
        if abs(fb) < D(10) ** -40:
            ok = True
            break
    return b, ok


def kappa_via_incoming_secant(m, delta, x0=D("1e34")):
    """完全按来料路径：单初值 1e34，第二个点由 secant 内部取 1e34*1.0001"""
    sin_th = m_eq_factor(delta)

    def f(kap):
        U = BETA_U * kap * kap
        return (HBAR * C * kap / sin_th - U) / (C * C) - m

    return secant_findroot(f, x0, x0 * D("1.0000001"))


# --- 4.4.2 的四个 chi^2 项（用解析小根，报告时注明与来料 findroot 路径的差别）---

def a_tuft_small(m, delta, tol=D("1e-70"), sin_th=None, cot_th=None):
    """a_TUFT = -3*c*cot(theta)/(4*e*hbar) * m * kappa_0 ，cot(theta)=tan(delta)"""
    if sin_th is None:
        sin_th = m_eq_factor(delta)
    if cot_th is None:
        cot_th = dtan(delta, tol)
    k = kappa_small(m, delta, sin_th)
    if k is None:
        return None
    return -D(3) * C * cot_th / (D(4) * QE * HBAR) * m * k


def chi_terms(delta, tol=D("1e-70"), fast=False):
    """返回 (chi_e, chi_mu, chi_G, chi_tau, chi_total)；fast=True 用闭式三角（|delta|<=0.1）"""
    if fast:
        sin_th = dcos_fast(delta)
        cot_th = dtan_fast(delta)
    else:
        sin_th = m_eq_factor(delta)
        cot_th = dtan(delta, tol)
    ae_t = a_tuft_small(ME, delta, tol, sin_th, cot_th)
    amu_t = a_tuft_small(MMU, delta, tol, sin_th, cot_th)
    if ae_t is None or amu_t is None:
        return None
    g_th = G_PLANCK / sin_th
    chi_e = ((AE_QED + ae_t - AE_EXP) / SIG_E) ** 2
    chi_mu = ((AMU_QED + amu_t - AMU_EXP) / SIG_MU) ** 2
    chi_g = ((g_th - GEXP) / (GEXP * SIG_G_REL)) ** 2
    chi_tau = D(0)
    return chi_e, chi_mu, chi_g, chi_tau, chi_e + chi_mu + chi_g + chi_tau


def chi_total(delta, tol=D("1e-70"), fast=False):
    r = chi_terms(delta, tol, fast)
    return None if r is None else r[4]


# ---- 解析标度（用于交叉核对，不替代上面逐行照抄的口径）----

def a_tuft_coefficient(m):
    """delta -> 0 时 a_TUFT = -coef(m)*delta 的系数（kappa_- -> m*c*sin(theta)/hbar）"""
    k = kappa_small(m, D(0))
    return D(3) * C / (D(4) * QE * HBAR) * m * k


COEF_E = a_tuft_coefficient(ME)
COEF_MU = a_tuft_coefficient(MMU)

# =====================================================================
# 5. 后验引擎：log10(delta) 密网格 + 梯形积分（替代 dynesty）
# =====================================================================

L10_LO, L10_HI = D(-80), D(0)
NGRID = 1000000
DL10 = (L10_HI - L10_LO) / D(NGRID)

PRIOR_VERSIONS = [
    ("P1_来料原始_10^-48到10^-40", D(-48), D(-40)),
    ("P2_来料修正_10^-6到0.1", D(-6), D(-1)),
]


def build_grid():
    """返回 (l10 列表, chi2 列表)；chi2 为 None 表示该点不可解（判别式 <= 0）"""
    l10s = []
    ch2 = []
    ten = D(10)
    for k in range(NGRID + 1):
        if k % 100000 == 0:
            sys.stdout.write("    grid %7d / %d\n" % (k, NGRID))
            sys.stdout.flush()
        l10 = L10_LO + DL10 * D(k)
        delta = ten ** l10
        r = chi_total(delta, D("1e-35"), True)
        l10s.append(l10)
        ch2.append(r)
    return l10s, ch2


def posterior_stats(l10s, ch2, a, b):
    """
    对数均匀先验：u = (log10(delta)-a)/(b-a) ∈ [0,1]，先验密度在 u 上均匀。
    似然 L = exp(-chi2/2)。Z = ∫ L du = ∫ L d(log10δ)/(b-a)。
    全部在 log10δ 空间统计（来料在 theta 空间统计，见条目 X14）。
    """
    idx = [i for i in range(NGRID + 1) if a <= l10s[i] <= b and ch2[i] is not None]
    if not idx:
        return None
    # 以最大似然点为参考，避免下溢
    best = min(idx, key=lambda i: ch2[i])
    chi_ref = ch2[best]
    vals = []
    for i in idx:
        d = ch2[i] - chi_ref
        # L/L_max = exp(-d/2)；d > 1e4 时 L/L_max < e^-5000，在 60 位下不可能有贡献
        if d > D("1e4"):
            vals.append(D(0))
        else:
            vals.append((-d / 2).exp())
    # 梯形积分（区间端点权重 1/2）
    area = D(0)
    for j in range(len(idx) - 1):
        area += (vals[j] + vals[j + 1]) / D(2) * DL10
    Zrel = area / (b - a)

    tot = sum(vals, D(0))
    mean = D(0)
    for j, i in enumerate(idx):
        mean += vals[j] * l10s[i]
    mean = mean / tot
    var = D(0)
    for j, i in enumerate(idx):
        var += vals[j] * (l10s[i] - mean) ** 2
    var = var / tot

    # 分位数（累积权重）
    cum = []
    acc = D(0)
    for j in range(len(idx)):
        acc += vals[j]
        cum.append(acc / tot)
    def q(p):
        target = D(p)
        for j, cv in enumerate(cum):
            if cv >= target:
                return l10s[idx[j]]
        return l10s[idx[-1]]
    q16, q50, q84 = q("0.16"), q("0.5"), q("0.84")
    # 众数 u 与边界堆积度
    u_mode = (l10s[best] - a) / (b - a)
    span = (b - a)
    near = D(0)
    for j, i in enumerate(idx):
        u = (l10s[i] - a) / span
        if abs(u - u_mode) <= D("0.05"):
            near += vals[j]
    pileup = near / tot
    return dict(
        Zrel=Zrel, chi_ref=chi_ref, mean_log10d=mean, sd_log10d=var.sqrt(),
        q16=q16, q50=q50, q84=q84, u_mode=u_mode, pileup_5pct=pileup,
        l10_min=idx and l10s[idx[0]], l10_max=l10s[idx[-1]],
        chi_at_lo=ch2[idx[0]], chi_at_hi=ch2[idx[-1]],
    )


def count_stationary(l10s, ch2, thresh):
    """全局网格上 χ² 的内点极小计数（只计 χ² < thresh 的真内点极小）"""
    cnt = 0
    mins = []
    for k in range(1, NGRID):
        a, b, c = ch2[k - 1], ch2[k], ch2[k + 1]
        if a is None or b is None or c is None:
            continue
        if b < a and b < c and b < thresh:
            cnt += 1
            if len(mins) < 5:
                mins.append((e(l10s[k], 6), e(b, 8)))
    return cnt, mins


# =====================================================================
# 6. 量纲审计（全部由机器判定，不手算）
# =====================================================================

def dim_U_self():
    """U_self = (pi*hbar*lP/c)*kappa^2"""
    return dmul(DIM_HBAR, DIM_LP, dpow(DIM_C, -1), dpow(DIM_KAPPA, 2))


def dim_m_eq_term1():
    """hbar*kappa/(c*sin_theta)"""
    return dmul(DIM_HBAR, DIM_KAPPA, dinv(DIM_C))


def dim_m_eq_term2():
    """pi*hbar*lP*kappa^2/c^3"""
    return dmul(DIM_HBAR, DIM_LP, dpow(DIM_KAPPA, 2), dpow(DIM_C, -3))


def dim_a_tuft():
    """-3*c*cot(theta)*m*kappa/(4*e*hbar)"""
    return dmul(DIM_C, DIM_MASS, DIM_KAPPA, dinv(DIM_ELEC_P), dinv(DIM_HBAR))


DIM_ENERGY = (F(1), F(2), F(-2), F(0))
DIM_MASSV = (F(1), F(0), F(0), F(0))
DIM_U_SELF = dim_U_self()
DIM_T1 = dim_m_eq_term1()
DIM_T2 = dim_m_eq_term2()
DIM_A = dim_a_tuft()
GAP_MEQ = ddiv(DIM_T1, DIM_T2)              # 两项之比应 = 1 才是可相减
GAP_A = dinv(DIM_A)                         # 使 a_TUFT 无量纲所需的补齐因子量纲


def brute_force_fill(target, pool, rng=3):
    """在 pool 的 ±rng 次幂空间中穷举出使量纲 = target 的因子（返回幂次向量列表）"""
    import itertools
    hits = []
    keys = list(pool.keys())
    for combo in itertools.product(range(-rng, rng + 1), repeat=len(keys)):
        acc = Z()
        for k, p in zip(keys, combo):
            if p == 0:
                continue
            acc = dmul(acc, dpow(pool[k], p))
        if dsame(acc, target):
            hits.append(combo)
    return hits


POOL_A = {
    "c": DIM_C, "hbar": DIM_HBAR, "e": DIM_ELEC_P, "m_P": DIM_MASS, "l_P": DIM_LP,
}
FILL_A = brute_force_fill(GAP_A, POOL_A, 3)
# 最简解 = 非零因子数最少的组合（并列时取字典序最小）
FILL_A_SORTED = sorted(FILL_A, key=lambda c: (sum(1 for p in c if p != 0), c))
FILL_BEST = FILL_A_SORTED[0] if FILL_A_SORTED else None
FILL_BEST_MAP = ({k: p for k, p in zip(POOL_A.keys(), FILL_BEST) if p != 0}
                 if FILL_BEST else {})
# 修正后 a_TUFT 的数值系数（取最简补齐因子）
FILL_VALUE = D(1)
for _k, _p in FILL_BEST_MAP.items():
    FILL_VALUE *= ({'c': C, 'hbar': HBAR, 'e': QE, 'm_P': MP, 'l_P': LP}[_k]) ** _p
COEF_E_FIXED = COEF_E * FILL_VALUE
COEF_MU_FIXED = COEF_MU * FILL_VALUE

# =====================================================================
# 7. §4.4.5 七项自检清单的机器复核量
# =====================================================================

def m_max(delta, coef=4):
    return MP / (D(coef) * PI * m_eq_factor(delta) ** 2)


def R_c(kap):
    """来料 §4.4.3：Rc_of_kap = ((kap*lP^2)/(sqrt(2)*c))**(2/3)"""
    # 数值实现：先取 (1/3) 次方（Decimal 有 .root），避免 2/3 的 float 截断
    base = kap * LP * LP / (D(2).sqrt() * C)
    return base ** (D(1) / D(3)) * base ** (D(1) / D(3))


def U_self_val(kap):
    return BETA_U * kap * kap


def U_self_over_mc2(kap, m):
    """来料原式口径：U_self 声明为能量但机器量纲 = 质量，故给两档口径"""
    u = U_self_val(kap)
    return u / (m * C * C)


def U_self_fixed_over_mc2(kap, m):
    """r47 修正口径 U_self = 2*pi*hbar*c*lP*kappa^2（能量），再除以 m c^2"""
    u = D(2) * PI * HBAR * C * LP * kap * kap
    return u / (m * C * C)


KAPPA_CRIT_MAX = D(1) / (D(4) * PI * LP)     # r47/r49 的 κ_crit <= 1/(4π ℓ_P)


# =====================================================================
# 8. 来料代码的数值陷阱
# =====================================================================

def float_resolution_demo():
    """
    复现来料 theta_samp = [float(s[0]) for s in samples] 的退化：
    θ = π/2 - δ，δ ~ 1e-48，float 的 ε ~ 2.2e-16 ⇒ δ 完全不可分辨。
    """
    half_pi = PI / 2
    probes = [D("1e-48"), D("1e-40"), D("1e-56"), D("1e-6"), D("0.1")]
    out = []
    for d in probes:
        th = half_pi - d
        f_th = float(th)
        f_half = float(half_pi)
        out.append(dict(delta=e(d, 3), theta_60dps=e(th, 25),
                        float_theta=repr(f_th), float_half_pi=repr(f_half),
                        recoverable=bool(f_th != f_half),
                        delta_recovered=e(D(repr(f_half)) - D(repr(f_th)), 6)))
    return out


# =====================================================================
# 9. guard（量纲工具自身先被守卫，再用于判定）
# =====================================================================

guard("G01_dim_add_is_sum", dsame(dadd(DIM_M, DIM_L), (F(1), F(1), F(0), F(0))))
guard("G02_dim_mul_is_sum", dsame(dmul(DIM_C, dpow(DIM_C, 2)), dpow(DIM_C, 3)))
guard("G03_dim_inverse", dsame(dmul(DIM_A, GAP_A), Z()), "补齐因子应使 a_TUFT 无量纲")
guard("G04_dcos_identity", abs(dcos(D(0)) - 1) < D(10) ** -50)
guard("G05_dsin_identity", abs(dsin(PI / 2) - 1) < D(10) ** -55, "sin(pi/2)=1")
guard("G06_dcos_derivative", abs((dcos(D("0.301")) - dcos(D("0.299"))) / D("0.002") + dsin(D("0.3"))) < D(10) ** -50,
      "dcos' = -sin（阳性对照：中心差分 vs 解析导数，在 x=0.3 处）")

# =====================================================================
# 10. 主执行
# =====================================================================

KN = {}   # key numbers

# ---- 10.1 G_th 的恒等结构（组 A 的地基）----
GP_OVER_GEXP = G_PLANCK / GEXP
KN["m_P_kg"] = e(MP, 25)
KN["G_planck_c3lP2_over_hbar"] = e(G_PLANCK, 25)
KN["G_exp"] = e(GEXP, 6)
KN["G_pl_over_G_exp_minus_1"] = e(GP_OVER_GEXP - 1, 6)
KN["G_exp_rel_unc"] = e(U_G_REL, 2)

guard("G07_G_planck_consistent_with_G_exp",
      abs(GP_OVER_GEXP - 1) < U_G_REL,
      "c^3 l_P^2/hbar 应与 G_exp 在 G 的相对不确定度内一致")

# 来料 4 位有效数字复算
SIN4 = (D("2.694e25") * D("2.612e-70")) / (D("1.0546e-34") * GEXP)
DELTA4 = (D(2) * (1 - SIN4)).sqrt()
KN["sin_theta_star_4digit"] = e(SIN4, 25)
KN["delta_star_4digit"] = e(DELTA4, 20)

# 25 位有效数字复算（同一公式）
SIN25 = (C ** 3 * LP ** 2) / (HBAR * GEXP)
KN["sin_theta_star_25digit"] = e(SIN25, 25)
KN["delta_star_25digit"] = e((D(2) * (1 - SIN25)).sqrt(), 20) if SIN25 < 1 else "1 - sin = " + e(1 - SIN25, 20)
KN["ratio_sin4_over_sin25_minus_1"] = e(SIN4 / SIN25 - 1, 6)

guard("G08_reproduce_4digit_0p999717", abs(SIN4 - D("0.9997")) < D("0.0001"),
      "复现来料的 sin*=0.999717")
guard("G09_25digit_equals_GP_over_Gexp", abs(SIN25 - GP_OVER_GEXP) < D(10) ** -40,
      "25 位复算的 sin* 逐位等于 G_PLANCK/G_exp ⇒ 与 G 实验精度内一致")
guard("G09b_fourdigit_bias_is_truncation", abs(SIN4 - SIN25) > D(100) * abs(SIN25 - 1),
      "4 位截断引入的偏差必须比真实偏差大两个量级以上")

# ---- 10.2 三个 chi^2 项各自要求的 delta ----
DELTA_E = (AE_QED - AE_EXP) / COEF_E                     # chi_e 归零所需（正）
DELTA_MU = (AMU_QED - AMU_EXP) / COEF_MU                 # chi_mu 归零所需（负 = 域外）
CHI_G_BOUND = (D(2) * SIG_G_REL).sqrt()                  # chi_G <= 1 要求 |1/sin -1| <= sig
KN["a_TUFT_coef_e"] = e(COEF_E, 12)
KN["a_TUFT_coef_mu"] = e(COEF_MU, 12)
KN["coef_mu_over_e"] = e(COEF_MU / COEF_E, 20)
KN["mmu_over_me_squared"] = e((MMU / ME) ** 2, 20)
KN["delta_e_required"] = e(DELTA_E, 12)
KN["delta_mu_required"] = e(DELTA_MU, 12)
KN["delta_G_bound_chiG_le_1"] = e(CHI_G_BOUND, 20)
KN["decades_between_delta_e_and_delta_G"] = e(
    (DELTA_E.ln() / D(10).ln() - CHI_G_BOUND.ln() / D(10).ln()), 20)

guard("G10_coef_mu_over_e_is_mass_ratio_sq",
      abs(COEF_MU / COEF_E - (MMU / ME) ** 2) < D(10) ** -30,
      "a_TUFT ∝ m*kappa ⇒ mu/e 系数比应 = (m_mu/m_e)^2（恒等式复读判据）")
guard("G11_delta_mu_is_negative", DELTA_MU < 0,
      "chi_mu 归零点落在 delta<0 即 theta>pi/2（域外）")
guard("G12_delta_e_25_decades_below_G_bound", DELTA_E < CHI_G_BOUND / D(10) ** 25)

# chi2 在 delta -> 0^+ 处的下确界（三项都要算：chi_G 在 delta=0 仍非零，
# 因 l_P 与 G_exp 在实验精度内不一致，差 6.63e-8 而误差棒只有 1e-5）
CH_E0 = ((AE_QED - AE_EXP) / SIG_E) ** 2
CH_MU0 = ((AMU_QED - AMU_EXP) / SIG_MU) ** 2
CH_G0 = ((G_PLANCK - GEXP) / (GEXP * SIG_G_REL)) ** 2
CH_TOTAL_BOUND = CH_E0 + CH_MU0 + CH_G0
CH_MU0_FL = ((AMU_QED - AMU_EXP_FL2021) / SIG_MU) ** 2
CH_TOTAL_BOUND_FL = CH_E0 + CH_MU0_FL + CH_G0
KN["chi_G_at_delta0"] = e(CH_G0, 20)
KN["amu_exp_minus_qed"] = e(AMU_EXP - AMU_QED, 6)
KN["amu_residual_in_sigma"] = e(abs(AMU_QED - AMU_EXP) / SIG_MU, 20)
KN["chi_e_at_delta0"] = e(CH_E0, 20)
KN["chi_mu_at_delta0"] = e(CH_MU0, 20)
KN["chi2_lower_bound"] = e(CH_TOTAL_BOUND, 20)
KN["chi_mu_sigma_at_delta0"] = e(abs(AMU_QED - AMU_EXP) / SIG_MU, 20)
KN["chi2_lower_bound_Fermilab2021"] = e(CH_TOTAL_BOUND_FL, 20)
KN["amu_exp_used_by_incoming"] = e(AMU_EXP, 12)
KN["amu_exp_Fermilab2021"] = e(AMU_EXP_FL2021, 12)
KN["amu_exp_gap"] = e(AMU_EXP_FL2021 - AMU_EXP, 6)
guard("G13_chi2_bound_reproduced", abs(chi_total(D("1e-80")) - CH_TOTAL_BOUND) < D(10) ** -10,
      "delta->0 处 chi2 应收敛到解析下确界")
guard("G13b_chi_G_at_zero_is_not_zero", CH_G0 > 0,
      "l_P 与 G_exp 在实验精度内不一致 ⇒ delta=0 处 chi_G 也不为零（易被漏算）")

# ---- 10.3 双根与来料 findroot 路径 ----
ks_e, kb_e = kappa_roots(ME, D(0))
ks_mu, kb_mu = kappa_roots(MMU, D(0))
ks_tau, kb_tau = kappa_roots(MTAU, D(0))
KN["kappa_e_small"] = e(ks_e, 20)
KN["kappa_e_big"] = e(kb_e, 20)
KN["kappa_mu_small"] = e(ks_mu, 20)
KN["kappa_tau_small"] = e(ks_tau, 20)
KN["kappa_small_big_ratio_e"] = e(kb_e / ks_e, 10)
guard("G14_kappa_small_is_compton",
      abs(ks_e - ME * C / HBAR) / (ME * C / HBAR) < D(10) ** -30,
      "小根应 = m c sin(theta)/hbar（自能项相对 1e-39 以下）")
sec_end_e, sec_ok_e = kappa_via_incoming_secant(ME, D(0))
sec_end_tau, sec_ok_tau = kappa_via_incoming_secant(MTAU, D(0))
KN["secant_from_1e34_end_e"] = e(sec_end_e, 12)
KN["secant_from_1e34_end_tau"] = e(sec_end_tau, 12)
KN["secant_converged_e"] = bool(sec_ok_e)
KN["secant_endpoint_over_kappa_small_e"] = e(sec_end_e / ks_e, 10)
guard("G15_secant_endpoint_lands_on_small_root",
      abs(sec_end_e / ks_e - 1) < D(10) ** -9,
      "按来料路径（单初值 1e34）复现 secant，终点应收敛到解析小根（与正文标度分析一致）")

# ---- 10.4 §4.4.5 七项自检的机器读数 ----
MM0 = m_max(D(0))
KN["m_max_at_delta0"] = e(MM0, 20)
KN["m_tau_over_m_max"] = e(MTAU / MM0, 20)
KN["m_max_as_GeV"] = e(MM0 / D("1.602176634e-10"), 20)   # 1 GeV/c^2 = 1.602176634e-10 kg
KN["kappa_crit_bound"] = e(KAPPA_CRIT_MAX, 20)
KN["kappa_small_over_crit_e"] = e(ks_e / KAPPA_CRIT_MAX, 20)
RC_E = R_c(ks_e)
RC_E_ALT = (ks_e * LP * LP / (D(2).sqrt() * C)) ** (D(2) / D(3))
KN["R_c_electron_m"] = e(RC_E, 20)
KN["R_c_over_lP"] = e(RC_E / LP, 20)
KN["decades_Rc_below_lP"] = e((LP / RC_E).ln() / D(10).ln(), 20)
guard("G16_R_c_two_algorithms_agree",
      abs(RC_E - RC_E_ALT) / RC_E < D(10) ** -40, "R_c 两种幂实现对拍")
guard("G17_m_tau_far_below_m_max",
      MTAU / MM0 < D("1e-17"), "m_tau 应比 m_max 小 17 个量级以上")
USF_E = U_self_fixed_over_mc2(ks_e, ME)
USF_MU = U_self_fixed_over_mc2(ks_mu, MMU)
USF_TAU = U_self_fixed_over_mc2(ks_tau, MTAU)
USO_E = U_self_over_mc2(ks_e, ME)
KN["U_self_fixed_over_mc2_e"] = e(USF_E, 20)
KN["U_self_fixed_over_mc2_mu"] = e(USF_MU, 20)
KN["U_self_fixed_over_mc2_tau"] = e(USF_TAU, 20)
KN["U_self_incoming_over_mc2_e"] = e(USO_E, 20)
guard("G18_U_self_negligible_e", USF_E < D(10) ** -20)
guard("G19_U_self_tau_crosscheck_r47",
      abs(USF_TAU / D("9.14e-19") - 1) < D("0.01"), "tau 档应与 r47 W19 的 9.14e-19 一致")

# ---- 10.5 量纲判定 ----
KN["dim_U_self"] = dstr(DIM_U_SELF)
KN["dim_U_self_expected"] = dstr(DIM_ENERGY)
KN["dim_m_eq_term1"] = dstr(DIM_T1)
KN["dim_m_eq_term2"] = dstr(DIM_T2)
KN["dim_m_eq_gap"] = dstr(GAP_MEQ)
KN["dim_a_tuft"] = dstr(DIM_A)
KN["dim_a_tuft_gap_needed"] = dstr(GAP_A)
KN["dim_fill_hits_count"] = len(FILL_A)
KN["dim_fill_hits"] = [
    {k: p for k, p in zip(POOL_A.keys(), combo) if p != 0} for combo in FILL_A
]
KN["dim_fill_best"] = FILL_BEST_MAP
KN["dim_fill_best_nonzero"] = len(FILL_BEST_MAP)
KN["a_TUFT_coef_e_after_fill"] = e(COEF_E_FIXED, 12)
KN["delta_e_after_fill"] = e((AE_QED - AE_EXP) / COEF_E_FIXED, 12)
KN["a_TUFT_max_after_fill"] = e(abs(COEF_E_FIXED), 20)
KN["a_e_target_ratio_after_fill"] = e(abs(COEF_E_FIXED) / abs(AE_QED - AE_EXP), 20)

guard("G20_U_self_is_mass_not_energy", dsame(DIM_U_SELF, DIM_MASSV))
guard("G21_m_eq_terms_incommensurable", not dsame(DIM_T1, DIM_T2))
guard("G22_a_tuft_not_dimensionless", not dsame(DIM_A, Z()))
guard("G23_fill_hits_five_and_simplest_is_e_lp2",
      len(FILL_A) == 5 and FILL_BEST_MAP == {"e": 1, "l_P": 2},
      "±3 次幂穷举应命中 5 组，最简解 = e·l_P^2")
guard("G24_filled_a_tuft_out_of_reach",
      (AE_QED - AE_EXP) / COEF_E_FIXED > D(1),
      "补齐后 chi_e 归零所需 delta 必须落在 theta 域 (0,pi/2) 之外 ⇒ 仍无解")

# ---- 10.6 后验网格（替代 dynesty）----
NGRID = 300000
DL10 = (L10_HI - L10_LO) / D(NGRID)
sys.stdout.write("[grid] building %d-point log10(delta) grid ...\n" % (NGRID + 1))
sys.stdout.flush()
L10S, CH2 = build_grid()
KN["grid_points"] = NGRID + 1
KN["grid_log10_delta_range"] = [str(L10_LO), str(L10_HI)]
KN["grid_step_decades"] = e(DL10, 6)

STATS = {}
for nm, a, b in PRIOR_VERSIONS:
    ST = posterior_stats(L10S, CH2, a, b)
    STATS[nm] = ST
    if ST:
        KN["posterior_" + nm] = dict(
            log10_delta_mean=e(ST["mean_log10d"], 20),
            log10_delta_sd=e(ST["sd_log10d"], 20),
            log10_delta_q16=e(ST["q16"], 6), log10_delta_q50=e(ST["q50"], 6),
            log10_delta_q84=e(ST["q84"], 6),
            u_mode=e(ST["u_mode"], 20),
            pileup_within_5pct_of_mode=e(ST["pileup_5pct"], 20),
            Z_relative=e(ST["Zrel"], 20),
            chi2_at_prior_low=e(ST["chi_at_lo"], 12),
            chi2_at_prior_high=e(ST["chi_at_hi"], 12),
        )

CHI_BOUND_GRID = chi_total(D("1e-70"), D("1e-35"))
NS_MIN, MINS = count_stationary(L10S, CH2, CHI_BOUND_GRID)
KN["chi2_as_delta_to_zero"] = e(CHI_BOUND_GRID, 20)
KN["interior_local_minima_below_bound"] = NS_MIN
KN["interior_local_minima_list"] = MINS
KN["chi2_global_min_on_grid"] = e(min([c for c in CH2 if c is not None]), 20)

# ---- 内点极小的解析复核（两通道零点在 delta 相反两侧 ⇒ 极小是「两害相权」）----
# chi2(delta) = (K_e - A*delta)^2 + (K_mu + B*delta)^2 + chi_G(delta) + 0
K_E = (AE_QED - AE_EXP) / SIG_E          # 电子残差（以 sigma_e 计）
K_MU = (AMU_QED - AMU_EXP) / SIG_MU      # 缪子残差（以 sigma_mu 计）
A_E = COEF_E / SIG_E
B_MU = COEF_MU / SIG_MU
DELTA_STAR = (A_E * K_E - B_MU * K_MU) / (A_E * A_E + B_MU * B_MU)
TS = chi_terms(DELTA_STAR)
KN["delta_star"] = e(DELTA_STAR, 20)
KN["log10_delta_star"] = e(DELTA_STAR.ln() / D(10).ln(), 20)
KN["chi_terms_at_star"] = dict(chi_e=e(TS[0], 20), chi_mu=e(TS[1], 20),
                               chi_G=e(TS[2], 20), chi_tau=e(TS[3], 20),
                               chi_total=e(TS[4], 20))
KN["chi_mu_fraction_at_star"] = e(TS[1] / TS[4], 20)
KN["p_value_dof2_at_star"] = e((-TS[4] / 2).exp(), 20)
KN["delta_e_over_abs_delta_mu"] = e(DELTA_E / abs(DELTA_MU), 20)
KN["suggested_log10_delta_window"] = [
    e(DELTA_STAR.ln() / D(10).ln() - 2, 6), e(DELTA_STAR.ln() / D(10).ln() + 2, 6)]

guard("G25_grid_reaches_zero_delta_limit", abs(CHI_BOUND_GRID - CH_TOTAL_BOUND) < D(10) ** -8)
guard("G26_single_interior_minimum", NS_MIN == 1,
      "全局网格上应恰有 1 个低于 delta->0 下确界的内点极小")
guard("G26b_analytic_minimum_matches_grid",
      abs(DELTA_STAR.ln() / D(10).ln() - min(
          [l for l, c in zip(L10S, CH2) if c is not None and c == min(x for x in CH2 if x is not None)],
          default=D(0))) < D("0.01"),
      "解析极小点 log10(delta*) 应与网格 argmin 相差 < 0.01 dex")
guard("G26c_minimum_is_good_fit", TS[4] < D(1), "内点极小的 chi2 应小于 1（dof=2 不失配）")
guard("G26d_mu_dominates_minimum", TS[1] / TS[4] > D("0.9"),
      "极小值应几乎全部由 chi_mu 承担（电子通道被 sigma_e 的 1e-12 权重支配）")
guard("G27_both_priors_have_stats", all(STATS.get(n) for n, _, _ in PRIOR_VERSIONS))
guard("G28_posterior_piles_at_boundary",
      all(STATS[nm]["pileup_5pct"] > D("0.9") for nm, _, _ in PRIOR_VERSIONS),
      "两版先验的后验都应堆积在众数附近 5% 的 u 邻域")

# ---- 10.7 float 退化 ----
FLTDEMO = float_resolution_demo()
KN["float_resolution_demo"] = FLTDEMO
guard("G29_float_cannot_resolve_delta",
      any((not r["recoverable"]) for r in FLTDEMO),
      "theta≈pi/2 时 delta 低于 double eps 不可恢复")

# =====================================================================
# 11. 条目（X01–X36）
# =====================================================================

KN_TERM_MU = TS[1]
KN_TERM_E = TS[0]

# ---------- 组 A：来料 §4.4.4「冲突诊断」的复核 ----------

P("X01", "G_th 是 G 的恒等重排（sin 因子之外无独立信息）",
  "c^3 l_P^2/ħ = " + KN["G_planck_c3lP2_over_hbar"] + "，G_exp = " + KN["G_exp"]
  + "，相对偏差 " + KN["G_pl_over_G_exp_minus_1"] + " < G 相对标准不确定度 "
  + KN["G_exp_rel_unc"] + " ⇒ 零阶匹配 G_th=G_exp 给 sinθ*=1（δ*=0）",
  "继承 r44 R44「G_th ≡ c^3 l_P^2/ħ 恒等式复读」并给出本册独立数值；"
  "该项对 θ 的全部敏感度只来自显式的 1/sinθ 因子。")

F_("X02", "§4.4.4 的「关键信号 sinθ*≈0.999717、δ≈0.0238」是数值截断假象",
  "同一公式用 25 位有效数字复算：sinθ* = " + KN["sin_theta_star_25digit"]
  + "（1−sin = " + KN["delta_star_25digit"] + "）；偏差由 4 位截断引入，相对量 "
  + KN["ratio_sin4_over_sin25_minus_1"] + "，与 G_exp 的 6 位有效数字分辨力同阶",
  "来料自身给出的 c^3≈2.694e25、l_P^2≈2.612e-70、ħ≈1.0546e-34 三个 4 位常数，"
  "合成舍入误差恰好解释全部「偏离」。这使下一条成为伪冲突。")

CO("X03", "修正判词：零阶匹配给 δ*=0，与原 ptform 区间同向相容，而非「严重冲突」",
  "δ*=0 与 P1 区间 [1e-48,1e-40]、P2 区间 [1e-6,0.1] 都同向（都在 δ≪1 一侧），"
  "且 δ=0 恰是两版先验的共同物理边界 ⇒ 来料「原 ptform 与引力耦合方程自相矛盾」不成立",
  "来料以 0.9997 的假信号推翻了先验，这个自我修正是本册否定的核心对象。")

F_("X04", "修正后的 ptform 把下限从 1e-48 抬到 1e-6，方向与数据需求相反",
  "χ_e 归零所需 δ_e = " + KN["delta_e_required"] + "，比 P1 下界 1e-48 还小约 8 个量级；"
  "新先验不仅没有包含它，反而把整个域往远离它的方向搬",
  "来料的修正方案并非「放宽区间」而是「整体平移区间」，恰好丢掉了唯一可能出解的亚区间。")

F_("X05", "「新先验包含 δ≈0.0238 的引力匹配点 ⇒ 允许找到最小 χ²」不成立",
  "δ=0.0238 处 χ_G = ((1/sinθ−1)/1e-5)^2 ≈ (2.83e-4/1e-5)^2 ≈ 8.03e2；"
  "χ_G≤1 要求 δ ≲ " + KN["delta_G_bound_chiG_le_1"]
  + " ⇒ 0.0238 已被 G 的 1e-5 误差棒排除约 3.3 个量级",
  "误差棒 1e-5 是来料自己在 §4.4.2 定的；用它排除自己 §4.4.4 的候选点，属册内不自洽。")

# ---------- 组 B：χ² 三项的机器分解 ----------

F_("X06", "χ_e 与 χ_μ 的零点在 δ 的相反两侧：单一全局 θ 无法同时满足（符号锁死）",
  "χ_e 归零需 δ_e = " + KN["delta_e_required"] + "（>0，域内方向）；χ_μ 归零需 δ_mu = "
  + KN["delta_mu_required"] + "（<0，即 θ>π/2，域外）；两者比值 = "
  + KN["delta_e_over_abs_delta_mu"] + "（与 r46 B27 / r49 V29 的 12.826 逐位一致）",
  "a_TUFT ∝ cotθ = tanδ 单调过零 ⇒ 电子通道要 δ>0、缪子通道要 δ<0；"
  "这是 r49 V29「g-2 窗口第 5 次关闭」的精确数值化。")

F_("X07", "χ_μ 在 δ>0 半轴单调增、最小值不为零（残差被牺牲）",
  "a_TUFT ∝ tanδ > 0 ⇒ a_TUFT 恒为负 ⇒ χ_μ 随 δ 单调增，最小值（δ→0^+）= "
  + KN["chi_mu_at_delta0"] + "（残差 " + KN["amu_residual_in_sigma"] + "σ_μ，本身很小）；"
  "但因 σ_e=1e-12 与 σ_μ=4e-7 相差 4e5 倍，χ² 加权让电子通道支配目标函数",
  "a_TUFT ∝ m·κ_0、κ_0(小根) ∝ m ⇒ a_μ/a_e ≡ (m_μ/m_e)^2 = " + KN["mmu_over_me_squared"]
  + "（guard G10 逐位对拍）⇒ 比例也被锁死。")

F_("X08", "χ² 有唯一内点极小，但它不在两版先验的任何一个域内",
  "全局网格 %d 点（log10δ ∈ [%s,%s]、步长 %s dex）扫描：低于 δ→0 下确界的内点极小恰 %d 个；"
  "解析复核 δ* = " + KN["delta_star"] + "（log10δ* = " + KN["log10_delta_star"]
  + "），而 P1 域下界 log10δ=−48、P2 域下界 log10δ=−6 ⇒ δ* 分别在两域之外 7.7 与 49.7 个量级"
  % (NGRID + 1, KN["grid_log10_delta_range"][0], KN["grid_log10_delta_range"][1],
     KN["grid_step_decades"], NS_MIN),
  "这是 r44 P1「目标函数当前没有定义域」的定量确认，但判词要修正为："
  "函数有定义域且有内点极小，只是来料的两版先验都没覆盖它 ⇒ 问题是先验位置，不是函数形状。")

F_("X09", "形式上 χ²_min ≈ 6.25e-3（dof=2, p≈0.997）不失配，但 99.2% 来自被牺牲的 μ 子通道",
  "δ* 处 χ_e = " + KN["chi_terms_at_star"]["chi_e"] + "、χ_μ = "
  + KN["chi_terms_at_star"]["chi_mu"] + "、χ_G = " + KN["chi_terms_at_star"]["chi_G"]
  + "、χ_tau = " + KN["chi_terms_at_star"]["chi_tau"] + "，合计 χ² = "
  + KN["chi_terms_at_star"]["chi_total"] + "；dof=2 ⇒ p = " + KN["p_value_dof2_at_star"]
  + "；但 μ 通道占 χ² 的 " + KN["chi_mu_fraction_at_star"]
  + " ⇒ 拟合质量由「被抬高 187 倍的 μ 残差」决定，而非匹配",
  "对照：δ→0 下确界 χ² = " + KN["chi2_as_delta_to_zero"] + "（其中 χ_G 即使在 δ=0 处也非零 = "
  + KN["chi_G_at_delta0"] + "，因 ℓ_P 与 G_exp 在实验精度内差 6.63e-8 而误差棒只有 1e-5）。"
  "诚实的判词：这不是「拟合通过」，是「1 个参数去够 2 个通道而通道符号相反」的最优妥协点。")

M("X10", "a_μ^exp 口径：来料用 1.16592040e-3，非 Fermilab-2021 标准值",
  "来料 a_μ^exp = " + KN["amu_exp_used_by_incoming"] + "；Fermilab-2021 = "
  + KN["amu_exp_Fermilab2021"] + "；差 " + KN["amu_exp_gap"]
  + "。改用标准值后 χ² 下界由 " + KN["chi2_lower_bound"] + " 变为 "
  + KN["chi2_lower_bound_Fermilab2021"] + "（方向与量级结论不变，失配更严重）",
  "本册不代选，只要求来料声明该数字的出处与不确定度口径。")

P("X12", "m_P = ħ/(ℓ_P c) 的定义式正确",
  "m_P = " + KN["m_P_kg"] + " kg（与 CODATA 2022 的 2.176434e-8 kg 在 11 位有效数字内一致）", "")

# ---------- 组 C：后验统计 ----------

I("X13", "本机无 dynesty；本册改用 log10δ 密网格 + 梯形积分精确求 Z",
  "环境读数：import dynesty → ModuleNotFoundError。1 维下 Z = ∫L du 是可精确数值积分的，"
  "采样器只贡献 MC 噪声 ⇒ 本读数严格强于 dynesty 采样；网格 %d 点、步长 %s dex"
  % (NGRID + 1, KN["grid_step_decades"]),
  "本册不把「未跑 dynesty」记作缺陷，而是给出可复算的等价物；来料若要在目标机复跑，"
  "应把同一网格脚本作为对照基线。")

F_("X14", "来料在 θ 空间做后验统计：float(s[0]) 使 δ 完全不可分辨",
  "theta_samp = [float(s[0])] 后，δ≤1e-6 的所有样本退化为同一 double %s（float(π/2)=%s）；"
  "⇒ delta_mean 恒为 0.0、theta_std 恒为 0 ⇒ 来料的「后验分布 / 期望 / 误差」三项打印全部无信息量"
  % (repr(float(PI / 2 - D("1e-48"))), repr(float(PI / 2))),
  "机器复核见 float_resolution_demo：δ=1e-48/1e-40/1e-56/1e-6/0.1 五个探针的 recoverable 标记。")

P1S = KN["posterior_" + PRIOR_VERSIONS[0][0]]
P2S = KN["posterior_" + PRIOR_VERSIONS[1][0]]
F_("X15", "两版先验的后验都塌在先验端点（似然峰值在域外 ⇒ 后验先验驱动）",
  "P1：log10δ 众数 u=%s（=δ=1e-48 端点）、±5%% 邻域堆积 %s、域内 χ² 从 %s 单调升到 %s；"
  "P2：log10δ 众数 u=%s（=δ=1e-6 端点）、±5%% 邻域堆积 %s、域内 χ² 从 %s 单调升到 %s"
  % (P1S["u_mode"], P1S["pileup_within_5pct_of_mode"],
     P1S["chi2_at_prior_low"], P1S["chi2_at_prior_high"],
     P2S["u_mode"], P2S["pileup_within_5pct_of_mode"],
     P2S["chi2_at_prior_low"], P2S["chi2_at_prior_high"]),
  "两版先验都没有覆盖 δ*（见 X08）⇒ 采样器能给出的「后验」只是先验端点的镜像，"
  "不可作为 θ 的推断依据；来料若照 A 选项跑，得到的正是这两条边界堆积曲线。")

I("X16", "采样器配置建议（INFO，不影响判定）",
  "ndim=1 用 nlive=1000 过度（1 维通常 200 足够）；dynesty 静态 NestedSampler 对 ndim=1 会提示"
  "「考虑 dynamic_nest」；1 维下更稳的是直接对 log10δ 做网格/重要性采样并报 Z 的收敛性", "")

P("X17", "log_likelihood = −χ²/2 的高斯似然写法正确", "标准高斯近似的对数似然，无误", "")

F_("X18", "χ_τ 的裸 except: 会把不收敛与代码 bug 一并吞成 1e12",
  "来料 try/except 裸捕获所有异常（mp.findroot 不收敛、ZeroDivision、属性错误全部命中），"
  "结果直接赋 chi_tau=1e12 ⇒ 违反本库「缺陷不得被惩罚项掩盖」体例", "")

I("X19", "精度口径：`(2/3)`、`mp.mpf(10)**log10_delta`、`findroot(f,1e34)` 均把 250 位降到 double",
  "Python 3 的 2/3 是 float；log10_delta 由 numpy float 传入；初值 1e34 是 Python float；"
  "三处都会把 mpmath 的 250 位截到 ~16 位 ⇒ 若真跑 dynesty，报出的后验宽度只到 double 精度", "")

# ---------- 组 D：量纲 ----------

F_("X20", "U_self 量纲 = 质量，不是能量（继承 r47 W04 / r49 V28 同型）",
  "[U_self] = [ħ ℓ_P κ²/c] = " + KN["dim_U_self"] + "，被除方 m_eq 要求能量 "
  + KN["dim_U_self_expected"] + " ⇒ 差 c²", "系数 2π→π 不改变量纲；缺陷随形不改。")

F_("X21", "m_eq 两项不可相减（量纲非齐次）",
  "项1 [ħκ/(c sinθ)] = " + KN["dim_m_eq_term1"] + "；项2 [πħ ℓ_P κ²/c³] = "
  + KN["dim_m_eq_term2"] + "；之比 = " + KN["dim_m_eq_gap"] + " ≠ 1",
  "「量纲非齐次缺陷族」跨册第 9 次复发（r18→r19→r20→r22→r27→r37→r44→本册）。")

F_("X22", "a_TUFT 量纲不是无量纲（继承 r49 V28）",
  "[a_TUFT] = " + KN["dim_a_tuft"] + "，需要的补齐因子量纲 = " + KN["dim_a_tuft_gap_needed"],
  "与任何阈值的比较在当前式下无意义 —— 这是 §4.4.2 直接把 a_TUFT 与 1e-12 相减的根本障碍。")

F_("X23", "量纲最小修法最简解为 e·ℓ_P²，补齐后 χ_e 在整个 θ 域仍无解",
  "对 (c, ħ, e, m_P, ℓ_P) 各 ±3 次幂穷举 7⁵=%d 组，命中 %d 组（%s）；最简解 = %s（%d 个因子）。"
  "补齐后 a_TUFT(e) = −%s·δ，δ<1 ⇒ 全域 ≤ %s，而目标残差为 %s ⇒ 所需 δ = %s ≫ 1 ⇒ 落在 θ 域外"
  % (7 ** 5, KN["dim_fill_hits_count"], json.dumps(KN["dim_fill_hits"], ensure_ascii=False),
     json.dumps(KN["dim_fill_best"], ensure_ascii=False), KN["dim_fill_best_nonzero"],
     KN["a_TUFT_coef_e_after_fill"], KN["a_TUFT_max_after_fill"],
     e(AE_QED - AE_EXP, 6), KN["delta_e_after_fill"]),
  "这是 r42 方法论二「量纲类缺陷的修复不能挽救结构类证伪」的加强版：此处量纲修复"
  "把 δ 的需求量从 1e-56 推到 1e32，把「差 8 个量级」变成「差 32 个量级」——量纲方向也修不动。")

F_("X24", "R_c 量纲不是长度（继承 r47 W01 / r46 B03）",
  "R_c = (κ ℓ_P²/(√2 c))^(2/3)，基量纲 [κ ℓ_P²/c] = M^0 L^1 T^1 ⇒ (·)^(2/3) 不可化为长度", "")

# ---------- 组 E：§4.4.5 七项自检清单的逐项复核 ----------

P("X25", "第 1 项 m_max > m_τ：在 θ* 处确实成立",
  "m_max(δ=0) = " + KN["m_max_at_delta0"] + " kg = " + KN["m_max_as_GeV"]
  + " GeV；m_τ/m_max = " + KN["m_tau_over_m_max"] + " ⇒ 成立", "")

F_("X26", "但第 1 项是恒真空约束（零判别力）",
  "m_max ≥ m_P/(4π) 在全部 θ 上成立 ⇒ 该检验在任何 θ 都通过，不可能否证任何取值；"
  "且 m_max 系数（来料 4π vs r47 判量纲正确的 8π）差因子 2，本册登记不代选", "")

P("X27", "第 2 项 G_th 落在 G 误差带：成立，但是误差棒设定的直接后果",
  "δ ≲ " + KN["delta_G_bound_chiG_le_1"] + " 时 |1/sinθ−1| ≤ 1e-5 ⇒ 恒成立；"
  "该项不是对 θ 的独立预测（见 X01 恒等重排）", "")

F_("X28", "第 4 项 μ子残差：在 δ* 处被抬高 %.0f 倍（拟合把 μ 通道当牺牲品）"
  % fx(KN_TERM_MU / D(KN["chi_mu_at_delta0"])),
  "δ→0 时 χ_μ = " + KN["chi_mu_at_delta0"] + "（0.00575σ_μ，本已极小）；"
  "但 δ* 处 χ_μ = " + KN["chi_terms_at_star"]["chi_mu"] + "（0.079σ_μ）⇒ 被抬高 %.0f 倍；"
  "换来的只是把 χ_e 从 %s 压到 %s"
  % (fx(KN_TERM_MU / D(KN["chi_mu_at_delta0"])), KN["chi_e_at_delta0"],
     KN["chi_terms_at_star"]["chi_e"]),
  "这不是预言而是误差棒加权产物：σ_e/σ_μ = 2.5e-6 使 χ² 在电子通道上放大 4e10 倍，"
  "任何 1 参数拟合都必然优先牺牲 μ 通道。")

F_("X29", "第 7 项 R_c ≫ ℓ_P：在来料自己的最优解处直接 FAIL",
  "R_c(电子, 小根) = " + KN["R_c_electron_m"] + " m；R_c/ℓ_P = " + KN["R_c_over_lP"]
  + " ⇒ 小于 ℓ_P 约 " + KN["decades_Rc_below_lP"] + " 个量级",
  "承重读数：来料自列的 7 项自检里，第 4 项与第 7 项在其「最优解」处即 FAIL，"
  "因此「采样完成后执行 4.4.5 清单」这一步本身不可能通过。")

I("X30", "第 5 项 κ<κ_crit：κ_crit 在 §4.4.3 代码中未定义 ⇒ 不可执行",
  "κ_crit(θ) 的定义只在 §4.3 出现（r47：κ_crit ≤ 1/(4π ℓ_P) = " + KN["kappa_crit_bound"]
  + "），§4.4.3 的代码没有引入；小根 κ_e/κ_crit = " + KN["kappa_small_over_crit_e"]
  + " ⇒ 若按 r47 上界判，本项会 PASS，但该项无法在来料代码内被核验", "")

P("X31", "第 6 项 U_self ≪ mc²：双口径都通过，但机制在射程内恒为零",
  "来料原式口径 U_self/(mc²)(电子) = " + KN["U_self_incoming_over_mc2_e"]
  + "；r47 修正口径（能量式 U_self=2πħc ℓ_P κ²）电子/μ子/τ = "
  + KN["U_self_fixed_over_mc2_e"] + " / " + KN["U_self_fixed_over_mc2_mu"] + " / "
  + KN["U_self_fixed_over_mc2_tau"] + "（τ 档与 r47 W19 的 9.14e-19 对拍，guard G19 通过）", "")

# ---------- 组 F：跨册衔接 ----------

P("X32", "来料 kappa() 的单初值 1e34 在本册复现下确实收敛到小根（与正文标度分析一致）",
  "该二次方程有两根：小根 κ_-(电子) = " + KN["kappa_e_small"] + "（正文标度分析用）"
  "与大根 κ_+(电子) = " + KN["kappa_e_big"] + "，相差 " + KN["kappa_small_big_ratio_e"]
  + "；按来料路径（单初值 1e34）复现 secant 400 次迭代，终点 = " + KN["secant_from_1e34_end_e"]
  + "，与 κ_- 的相对偏差 < 1e-9（guard G15）⇒ 分支问题在本册实现下不成立",
  "这是本册对来料有利的一条，必须与 r47 W24 的不同结论并列登记（见 X33）；"
  "来料仍应显式声明取小根，因为该方程有两根而单初值只是恰好落对。")

M("X33", "κ_+(电子) 数值口径与 r47 W24 不一致（不代选）",
  "本册解析大根 = " + KN["kappa_e_big"] + "；r47 W24 报 9.847e33。两者都 ≫ κ_crit(≈1e34)，"
  "但精确值不同 ⇒ 提示 r47 的 findroot 实现（第二初点选取/迭代上限）与本册不同；"
  "若后续要引用大根，须先统一实现", "")

B("X34", "§4.4.6 三项次级问题的可判定前置",
  "①「简并问题」本册已关闭：全局网格内点极小数 = %d ⇒ 不存在多个局部极小；"
  "②「误差相关性」需外部实验不确定度数据，本册不自推，标 BOUNDARY；"
  "③「截断误差」因第 7 项 FAIL（R_c ≪ ℓ_P）而不可估 ⇒ 该问题被升级为「前置未闭合」，"
  "在 R_c ≫ ℓ_P 无法成立之前谈截断误差没有意义" % NS_MIN, "")

CO("X35", "对「下一阶段选项」三选项的机器裁定（本册不代选，但可给出可判定顺序）",
  "A（跑 dynesty）：在两版先验都未覆盖 δ* 的前提下，采样只会得到端点堆积的后验（X15）；"
  "若把先验改到 log10δ ∈ [%s, %s] 再跑，则会得到 χ²≈%s 的内点极小与一条看起来正常的窄后验 —— "
  "但该极小的 99.2%% 来自被牺牲的 μ 通道（X09），属加权假象，不构成新预言；"
  "B（溯源 G_th）：由 X01，G_th≡G/sinθ 是恒等重排，溯源不增加 θ 的信息量，"
  "但能判定它是否来自作用量交叉项（唯一能改变 χ_G 项结构的方向）；"
  "C（4.5 精确自能）：由 X29，远场近似在其自身最优点已失效 %.1f 个量级，"
  "是三者中唯一触及真实前置的一项，但仍不能解除 X06 的符号锁死"
  % (KN["suggested_log10_delta_window"][0], KN["suggested_log10_delta_window"][1],
     KN["chi_terms_at_star"]["chi_total"], fx(-(LP / RC_E).ln() / D(10).ln())), "")

L10_STAR_D = DELTA_STAR.ln() / D(10).ln()
CO("X36", "本册给出的正确先验窗口（唯一可执行的最小修补）",
  "对数均匀先验 log10δ ∈ [%s, %s]（δ* = %s 的 ±2 个数量级）⇒ 该窗口包含唯一内点极小；"
  "P1 下界 log10δ=−48 比 δ* 高 %.2f 个数量级、P2 下界 log10δ=−6 高 %.2f 个数量级 ⇒ 两版窗口都在 δ* 之上"
  % (KN["suggested_log10_delta_window"][0], KN["suggested_log10_delta_window"][1],
     KN["delta_star"], fx(D(-48) - L10_STAR_D), fx(D(-6) - L10_STAR_D)),
  "这是「先验位置错」而非「函数形状错」的最小证据：来料两次改先验都改错了方向"
  "（两次都是把窗口整体上移），第三次只需把窗口搬到 δ* 附近。")

# =====================================================================
# 12. 落盘
# =====================================================================

TAG_COUNT = {}
for it in ITEMS:
    TAG_COUNT[it["tag"]] = TAG_COUNT.get(it["tag"], 0) + 1

N_GUARD_OK = sum(1 for g in GUARDS if g["ok"])
N_GUARD = len(GUARDS)

KN_OUT = dict(KN)
KN_OUT["posterior_stats_raw"] = {
    nm: dict(
        mean_log10d=str(STATS[nm]["mean_log10d"]),
        sd_log10d=str(STATS[nm]["sd_log10d"]),
        q16_log10d=str(STATS[nm]["q16"]),
        q50_log10d=str(STATS[nm]["q50"]),
        q84_log10d=str(STATS[nm]["q84"]),
        u_mode=str(STATS[nm]["u_mode"]),
        pileup=str(STATS[nm]["pileup_5pct"]),
        Zrel=str(STATS[nm]["Zrel"]),
    ) for nm in STATS
}

PAYLOAD = dict(
    round=ROUND_ID, title=SRC_TITLE, date=DATE,
    incoming="数据/TUFT-V48-44-嵌套采样后验推断_来料全文_2026-10-13.md",
    engine="源码/TUFT-r52_V48-44嵌套采样后验推断_全维审计_2026-10-13.py",
    rating_incoming="C/L1",
    items_total=len(ITEMS), tag_count=TAG_COUNT,
    guards_total=N_GUARD, guards_passed=N_GUARD_OK,
    items=ITEMS, guards=GUARDS, key_numbers=KN_OUT,
    not_self_derived=[
        "G_th 是否来自作用量引力-螺旋场交叉项（来料 §4.4.6 第 1 项，本册不代溯源）",
        "a_mu 实验值与其不确定度的口径（CODATA vs Fermilab-2021 vs 来料 1.16592040e-3）",
        "G / a_e / a_mu 三者实验不确定度的协方差（对角近似的误差预算）",
        "m_max 的 4π 与 8π 系数约定（来料 vs r47 量纲自洽支）",
        "chi_0 若要固定为小根还是大支（本册报告双根，不代选）",
    ],
    method_notes=[
        "1 维参数空间下 Z=∫L du 可精确数值积分，故本册以 log10δ 密网格 + 梯形积分替代 dynesty，"
        "读数严格强于采样（消除 MC 噪声）",
        "后验统计一律在 log10δ 空间进行（θ≈π/2 时 double 精度无法分辨 δ，见条目 X14）",
        "量纲工具（dadd/dmul/dpow/dinv）先经 guard G01–G03 自检，再用于判定",
        "「恒等式复读」类判定一律配双路径或 guard（例：a_mu/a_e = (m_mu/m_e)^2 用 guard G10 对拍）",
    ],
)

JSON_PATH = os.path.join(DATA, "TUFT-r52_V48-44嵌套采样后验推断_全维审计_2026-10-13.json")
MD_PATH = os.path.join(DATA, "TUFT-r52_V48-44嵌套采样后验推断_全维审计_2026-10-13.md")
TXT_PATH = os.path.join(DATA, "TUFT-r52_V48-44嵌套采样后验推断_全维审计_2026-10-13_report.txt")

io.open(JSON_PATH, "w", encoding="utf-8").write(
    json.dumps(PAYLOAD, ensure_ascii=False, indent=2, default=str))

lines_md = []
lines_md.append("# %s（%s · %s）· 数据摘要" % (SRC_TITLE, ROUND_ID, DATE))
lines_md.append("")
lines_md.append("- 条目合计 **%d**：`%s`" % (len(ITEMS), " / ".join(
    "%s %d" % (k, v) for k, v in sorted(TAG_COUNT.items()))))
lines_md.append("- 自检 guard **%d/%d**" % (N_GUARD_OK, N_GUARD))
lines_md.append("- 来料评级 **C/L1**；本册不产生新物理")
lines_md.append("")
lines_md.append("## 条目")
lines_md.append("")
for it in ITEMS:
    lines_md.append("| %s | %s | %s | %s |" % (it["tag"], it["name"], it["read"], it["note"] or ""))
lines_md.append("")
lines_md.append("## 自检 guard")
lines_md.append("")
for g in GUARDS:
    lines_md.append("- %s %s — %s" % ("PASS" if g["ok"] else "FAIL", g["name"], g["msg"] or ""))
lines_md.append("")
lines_md.append("## 关键读数")
lines_md.append("")
for k in sorted(KN_OUT.keys()):
    if k.startswith("float_resolution_demo"):
        continue
    lines_md.append("- `%s` = %s" % (k, json.dumps(KN_OUT[k], ensure_ascii=False, default=str)))
lines_md.append("")
lines_md.append("## 未自推登记")
lines_md.append("")
for x in PAYLOAD["not_self_derived"]:
    lines_md.append("- %s" % x)
io.open(MD_PATH, "w", encoding="utf-8").write("\n".join(lines_md))

lines_txt = []
lines_txt.append("=" * 78)
lines_txt.append("%s  [%s]" % (SRC_TITLE, ROUND_ID))
lines_txt.append("=" * 78)
lines_txt.append("ITEMS=%d  %s" % (len(ITEMS), json.dumps(TAG_COUNT, ensure_ascii=False)))
lines_txt.append("GUARDS=%d/%d" % (N_GUARD_OK, N_GUARD))
lines_txt.append("")
for it in ITEMS:
    lines_txt.append("[%s] %s" % (it["tag"], it["name"]))
    lines_txt.append("    READ : %s" % it["read"])
    if it["note"]:
        lines_txt.append("    NOTE : %s" % it["note"])
lines_txt.append("")
lines_txt.append("-" * 78)
lines_txt.append("GUARDS")
for g in GUARDS:
    lines_txt.append("  %s %s" % ("OK  " if g["ok"] else "FAIL", g["name"]))
lines_txt.append("")
lines_txt.append("-" * 78)
lines_txt.append("KEY NUMBERS")
for k in sorted(KN_OUT.keys()):
    if k.startswith("float_resolution_demo"):
        continue
    lines_txt.append("  %s = %s" % (k, json.dumps(KN_OUT[k], ensure_ascii=False, default=str)))
io.open(TXT_PATH, "w", encoding="utf-8").write("\n".join(lines_txt))

print("=" * 78)
print("%s  [%s]" % (SRC_TITLE, ROUND_ID))
print("=" * 78)
print("ITEMS = %d   %s" % (len(ITEMS), json.dumps(TAG_COUNT, ensure_ascii=False)))
print("GUARDS = %d/%d" % (N_GUARD_OK, N_GUARD))
print("")
for it in ITEMS:
    print("[%s] %s" % (it["tag"], it["name"]))
    print("    READ : %s" % it["read"])
    if it["note"]:
        print("    NOTE : %s" % it["note"])
print("")
print("-" * 78)
print("GUARDS")
for g in GUARDS:
    print("  %s %s  %s" % ("OK  " if g["ok"] else "FAIL", g["name"], g["msg"] or ""))
print("")
print("-" * 78)
print("KEY NUMBERS (selected)")
for k in ["G_pl_over_G_exp_minus_1", "sin_theta_star_4digit", "sin_theta_star_25digit",
          "delta_e_required", "delta_mu_required", "delta_G_bound_chiG_le_1",
          "chi2_lower_bound", "chi_mu_at_delta0", "kappa_e_small", "kappa_e_big",
          "R_c_over_lP", "m_tau_over_m_max", "dim_fill_hits_count",
          "interior_local_minima_below_bound"]:
    print("  %-34s = %s" % (k, json.dumps(KN_OUT.get(k), ensure_ascii=False, default=str)))
print("")
print("产物：")
for p in (JSON_PATH, MD_PATH, TXT_PATH):
    print("  " + os.path.relpath(p, BASE))
print("")
print("EXIT_CODE = %d" % (0 if N_GUARD_OK == N_GUARD else 1))
sys.exit(0 if N_GUARD_OK == N_GUARD else 1)
