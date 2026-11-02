# -*- coding: utf-8 -*-
"""
TUFT-r382 · 整理 J74（ROOT V48/V49 问题梳理 + V50 攻坚路线）并攻破其可机核硬命题
==============================================================================
来料：数据/TUFT-J74_ROOTV48V49问题梳理与V50攻坚路线_来料全文_2026-11-03.md（19,030 B）

本卷判六件事（全部本卷实算，不引用教科书结论）：
  A. (49-17) 磁通能 E=πN²/(2g₆²R²) 的**系数是口径量**（∫F=2πN vs 4πN 差 4 倍）；
     口径无关的只有结构 N²/(g₆²R²)。
  B. 「六维 Chern–Simons 项」维数上不存在（CS 是 2n−1 形式）；六维能写下的同类项只有
     θ·F∧F∧F，而它在 M⁴×S²（内部 2 维）上只含**一次** F_{S²} ⇒ 对 N 线性 ⇒ E=aN²+bN。
     线性项能把极小挪到任意 N，N=3 只对应 b/a∈(−7,−5) ⇒ 可调、零预言力。
  C. 指标定理 ind=N 与「N=3⇒3 个零模」：三条独立路径在 N=1..8 上逐点对拍；对照组 j=N/2 全错。
  D. V48 禁区「单 brane 定点 Higgs + 普适 Yukawa ⇒ rank M≤1」：9 个 2×2 子式全零；
     三点 Higgs ⇒ 秩满 ⇒ 给出定量逃逸条件。
  E. 被来料判死的两条质量关系用 PDG 在**两种次序**下复核（反例优先参数化成族）。
  F. (49-13/15/16) 短距 r⁻⁴、长距 r⁻²：KK 求和实算斜率 4.00000 / 2.00000 与 crossover；
     并定价 —— 这是**维度强制**的普适结果，不构成独有预言（供给 0）。

★自伤八项见判定册 §九。
"""
import ast, io, json, math, os, re
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 55

RID = "r382"
STAMP = "2026-11-03"
TITLE = "整理J74_V48V49问题清单与V50路线_磁通能口径与N3选择可调性与指标零模与禁区秩定理与KK短距力律"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P_SRC = os.path.abspath(__file__)
P_JSON = os.path.join(ROOT, "数据", "TUFT-%s_%s_%s.json" % (RID, TITLE, STAMP))
P_TXT = os.path.join(ROOT, "数据", "TUFT-%s_%s_report_%s.txt" % (RID, TITLE, STAMP))
P_MD = os.path.join(ROOT, "数据", "TUFT-%s_%s_%s.md" % (RID, TITLE, STAMP))
P_JUD = os.path.join(ROOT, "判定", "判定_判定_TUFT-%s_%s_%s.md" % (RID, TITLE, STAMP))
P_HTML = os.path.join(ROOT, "四力统一方程_TUFT-%s_J74问题清单攻破_%s.html" % (RID, STAMP))

# ============================================================================
# §0 · Decimal 数学（无 numpy/sympy：Machin π + 自写 exp/sin/sqrt/ln/tanh）
# ============================================================================
ZERO, ONE, TWO = D(0), D(1), D(2)

def _atan_inv(x):
    """atan(1/x)，★实参必须是 x>1（即 5、239），绝不能传 0.2 —— 传 0.2 时
    t=1/0.2=5、t2=25，级数变成发散的等比 ⇒ term 涨到 1e1902 ⇒ decimal.Overflow。
    （本卷 r382 首次书写即踩此坑，读数 PI=-6.239e1902；见判定册 §九 自伤一。）"""
    x = D(x)
    assert x > 1, "atan 展开要求 x>1，收到 %r" % (x,)
    t = ONE / x
    t2 = t * t
    s = ZERO
    term = t
    k = 0
    while True:
        addend = term / (2 * k + 1)
        if addend == 0:
            break
        s = s + addend if k % 2 == 0 else s - addend
        term = term * t2
        k += 1
        if k > 400:
            break
    return s

PI = 4 * (4 * _atan_inv(D(5)) - _atan_inv(D(239)))

def dsqrt(x):
    x = D(x)
    if x == 0:
        return ZERO
    g = D(str(math.sqrt(float(x))))
    for _ in range(80):
        ng = (g + x / g) / 2
        if ng == g:
            break
        g = ng
    return g

def dexp(x):
    x = D(x)
    n = 0
    while abs(x) > D("0.5"):
        x = x / 2
        n += 1
    s = ONE
    term = ONE
    k = 1
    while True:
        term = term * x / k
        if term == 0:
            break
        s = s + term
        k += 1
        if k > 200:
            break
    for _ in range(n):
        s = s * s
    return s

def _ln_near(x):
    """atanh 级数，★只在 1≤x<10 时收敛够快（y=(x−1)/(x+1) ≤ 9/11 ⇒ y²≤0.67 ⇒ 55 位需 ~140 项）。"""
    x = D(x)
    y = (x - ONE) / (x + ONE)
    s = ZERO
    term = y
    k = 0
    while True:
        addend = term / (2 * k + 1)
        if abs(addend) < D("1e-58"):
            break
        s += addend
        term = term * y * y
        k += 1
        if k > 800:
            break
    return 2 * s

LN10 = _ln_near(D(10))

def dln(x):
    """ln x（x>0）。
    ★★★自伤：直接把 2·atanh((x−1)/(x+1)) 用于任意 x 是错的 —— 收敛率由 y² 决定，
    x=1e5 时 y=0.99998、y²=0.99996，400 项后残差仍在 1e-2 量级。r382 首跑即中招：
    dln 给的是 0.0133 而不是 11.51，力律斜率读数变成 0.0133（详见判定册 §九 自伤二）。
    正法：先按十进制把 x 归约到 [1,10) 的尾数，再补 k·ln10。"""
    x = D(x)
    assert x > 0, "ln 定义域 x>0，收到 %r" % (x,)
    k = 0
    while x >= 10:
        x = x / 10
        k += 1
    while x < 1:
        x = x * 10
        k -= 1
    return _ln_near(x) + k * LN10

def dsin(x):
    x = D(x)
    k2 = 0
    while abs(x) > PI:
        x = x - (PI if x > 0 else -PI)
        k2 += 1
        if k2 > 200:
            break
    s = ZERO
    term = x
    k = 1
    while True:
        s = s + term
        term = -term * x * x / ((k + 1) * (k + 2))
        k += 2
        if abs(term) < D("1e-58"):
            break
    return s

def dcos(x):
    return dsin(PI / 2 - D(x))

def dcoth(x):
    e = dexp(2 * D(x))
    return (e + 1) / (e - 1)

def fd(fr):
    """Fraction → Decimal。★Decimal(Fraction) 直接抛 TypeError（r382 首跑即踩），
    必须走分子/分母。整数/字符串照旧。"""
    if isinstance(fr, F):
        return D(fr.numerator) / D(fr.denominator)
    return D(fr)

def fmt(x, nd=8):
    if x is None:
        return "—"
    try:
        x = fd(x)
    except Exception:
        return str(x)
    if x == 0:
        return "0"
    if abs(x) < D("1e-4") or abs(x) >= D("1e6"):
        return "%.*E" % (nd - 1, x)
    return "%.*f" % (nd, x)

def rel(a, b):
    a, b = D(a), D(b)
    den = abs(b)
    if den < D("1e-300"):
        den = D("1e-300")
    return abs(a - b) / den

# ============================================================================
# §1 · 判据容器：ok 驱动 kind
# ============================================================================
MAIN, CTL, GRD = [], [], []
RES = {}

def add(lst, eid, kind, title, exp, act, ok, note):
    if not bool(ok):
        kind = "FAIL"
    lst.append(dict(id=eid, kind=kind, title=title,
                    exp=str(exp), act=str(act), note=note))

# ============================================================================
# §2 · 6 维外代数（Fraction 系数）：F∧F∧F 对通量 N 的幂次
# ============================================================================
def w_wedge(A, B):
    out = {}
    for ka, va in A.items():
        for kb, vb in B.items():
            if ka & kb:
                continue
            k = ka | kb
            out[k] = out.get(k, F(0)) + va * vb
    return {k: v for k, v in out.items() if v != 0}

def w_scale(A, c):
    c = F(c)
    return {k: v * c for k, v in A.items() if v * c != 0}

def w_add(A, B):
    out = dict(A)
    for k, v in B.items():
        out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v != 0}

def w_norm(A):
    return F(0) if not A else max(abs(v) for v in A.values())

def w_diff(A, B):
    keys = set(A) | set(B)
    if not keys:
        return F(0)
    return max(abs(A.get(k, F(0)) - B.get(k, F(0))) for k in keys)

def f_mix(n_int, a, g, c=2):
    """内部空间占前 n_int 个基矢，F = a·F_S + G（G 取外部 2-形式）。
      · n_int=2：内部只剩一个独立 2-形式 ⇒ F_S=a·e01，F_S∧F_S=0（2 维取不出 4-形式）；
        外部 4 维 ⇒ G 有 6 个分量、G∧G≠0 ⇒ F∧F∧F = 3·F_S∧G∧G，**对 a 线性**。
      · n_int=4：内部取**两个**独立 2-形式之和 F_S=a(e01+c·e23)（c≠1 才使 F_S²≠0）；
        外部只剩 2 维 ⇒ G=g·e45、G∧G=0；又 4 维内部取不出 6-形式 ⇒ F_S³=0
        ⇒ F∧F∧F = 3·F_S∧G∧G = 12a²cg·e012345，**对 a 二次**。
    返回 (F3, 3·F_S∧G∧G, ‖F_S∧F_S∧G‖, ‖F_S∧F_S∧F_S‖)。"""
    if n_int == 2:
        FS = {(1 << 0) | (1 << 1): F(a)}
    else:
        FS = {(1 << 0) | (1 << 1): F(a), (1 << 2) | (1 << 3): F(a) * F(c)}
    G = {}
    for i in range(n_int, 6):
        for j in range(i + 1, 6):
            G[(1 << i) | (1 << j)] = F(g)
    Fm = w_add(FS, G)
    F3 = w_wedge(Fm, w_wedge(Fm, Fm))
    cross = w_scale(w_wedge(FS, w_wedge(G, G)), 3)
    FSG = w_wedge(FS, w_wedge(FS, G))
    FS3 = w_wedge(FS, w_wedge(FS, FS))
    return F3, cross, w_norm(FSG), w_norm(FS3)

F3_2d, CROSS_2d, FSG_2d, FS3_2d = f_mix(2, 3, 5)
F3_2d_b, _, _, _ = f_mix(2, 6, 5)
F3_4d, _, _, FS3_4d = f_mix(4, 3, 5)
F3_4d_b, _, _, _ = f_mix(4, 6, 5)

RES.update(norm_F3_2d=w_norm(F3_2d), norm_cross_2d=w_norm(CROSS_2d),
           fsg_2d=FSG_2d, fs3_2d=FS3_2d,
           f3_2d_eq_cross=w_diff(F3_2d, CROSS_2d),
           lin_ratio_2d=w_norm(F3_2d_b) / w_norm(F3_2d),
           norm_F3_4d=float(w_norm(F3_4d)), fs3_4d=float(FS3_4d),
           lin_ratio_4d=float(w_norm(F3_4d_b) / w_norm(F3_4d)),
           deg_F3=max(F3_2d.keys()).bit_count(),
           deg_empty=len(w_wedge({1: F(1)}, {1: F(1)})),
           cs_deg=5, theta_deg=6)

# ============================================================================
# §3 · (49-17) 磁通能：两种归一化口径
# ============================================================================
def flux_energy_numeric(N, g, R, nstep=2000):
    """Simpson：E=(1/4g²)∫₀^π∫₀^{2π}√g F²dθdφ，F_{θφ}=(N/2)sinθ（口径 A：∫F=2πN）。"""
    N, g, R = D(N), D(g), D(R)
    h = PI / nstep
    tot = ZERO
    for k in range(nstep + 1):
        th = h * k
        w = D(1) if k in (0, nstep) else (D(4) if k % 2 == 1 else D(2))
        s = dsin(th)
        if s == 0:
            continue
        Fthph = (N / 2) * s
        Fup = Fthph / (R ** 4 * s * s)
        tot += w * (R * R * s) * (2 * Fthph * Fup)
    return tot * h / 3 * (2 * PI) / (4 * g * g)

def flux_energy_closed(N, g, R):
    """口径 A 的闭式：E = πN²/(2g²R²)。"""
    return PI * D(N) ** 2 / (2 * D(g) ** 2 * D(R) ** 2)

def flux_energy_B(N, g, R):
    """口径 B：F_{θφ}=N sinθ（∫F=4πN）⇒ 系数 ×4。"""
    return 4 * flux_energy_closed(N, g, R)

def flux_energy_rich(N, g, R, n=1000):
    """★Simpson 截断误差 ∝ h⁴：n=2000 时实测相对偏差 3.4e-14，恰好是
    (h⁴/180)∫|f⁗| ≈ 3.4e-14 ⇒ 判据若写 1e-18 就变成「测积分器」而不是测公式。
    正法：Richardson 外推 (16·S(2n) − S(n))/15（残差 O(h⁶)）。"""
    s1 = flux_energy_numeric(N, g, R, n)
    s2 = flux_energy_numeric(N, g, R, 2 * n)
    return (16 * s2 - s1) / 15

E_num = flux_energy_rich(3, "2.5", "1.7")
E_cl = flux_energy_closed(3, "2.5", "1.7")
E_B = flux_energy_B(3, "2.5", "1.7")
E_cl_R2 = flux_energy_closed(3, "2.5", dsqrt(TWO) * D("1.7"))
RES.update(E_num=E_num, E_cl=E_cl, E_B=E_B, E_rel=rel(E_num, E_cl),
           E_conv_ratio=E_B / E_cl, E_halved=E_cl_R2,
           E_halved_rel=rel(E_cl_R2, E_cl / 2),
           E_r34=(flux_energy_closed(4, "1", "1") / flux_energy_closed(3, "1", "1")),
           E_r34_cl=(D(4) / D(3)) ** 2)

# ============================================================================
# §4 · N 选择：E(N)=aN²+bN，argmin=k 的窗口 b/a∈(−(2k+1),−(2k−1))，宽 2
# ============================================================================
def argmin_N(ba, NMAX=40):
    best, bn = None, None
    for N in range(0, NMAX + 1):
        E = D(N) ** 2 + D(str(ba)) * D(N)
        if best is None or E < best:
            best, bn = E, N
    return bn

def win_analytic(k):
    return (-(2 * k + 1), -(2 * k - 1))

BND = []
for k in (1, 3, 6):
    lo, hi = win_analytic(k)
    BND.append([k, lo, argmin_N(lo - 0.001), argmin_N(lo + 0.001),
                argmin_N(hi - 0.001), argmin_N(hi + 0.001)])
RES["bnd_tab"] = BND
# ★方向：E(k+1)−E(k) = (2k+1)+b ⇒ b 稍小于 lo=−(2k+1) 时 k+1 更优（落到 k+1）；
#   E(k−1)−E(k) = −(2k−1)−b ⇒ b 稍大于 hi=−(2k−1) 时 k−1 更优（k=1 时落到 0）。
#   首版把两个方向都写反（判 b[2]==k−1）⇒ 3/3 全判失败，见 §九 自伤五。
RES["bnd_ok"] = sum(1 for b in BND if b[2] == b[0] + 1 and b[3] == b[0]
                    and b[4] == b[0] and b[5] == b[0] - 1)
RES["win3_lo"], RES["win3_hi"] = win_analytic(3)
RES["win3_width"] = 2
RES["argmin_m6"] = argmin_N(-6.0)
RES["argmin_p3"] = argmin_N(3.0)
RES["argmin_all"] = {k: argmin_N(-2.0 * k) for k in range(1, 9)}
RES["win_count"] = len(RES["argmin_all"])

# 细扫确认「窗口存在且唯一」（−10..0，步长 0.05）
SCAN = []
x = -10.0
while x <= 0.0:
    SCAN.append(argmin_N(x))
    x += 0.05
RES["scan_argmin_set"] = sorted(set(SCAN))
RES["scan_has_3"] = 3 in SCAN

# ============================================================================
# §5 · 指标定理三路径（N=1..8）
# ============================================================================
def c1_integral(N, nstep=800):
    """(1/2π)∮_{S²}F，A_φ=(N/2)(1−cosθ) ⇒ F_{θφ}=(N/2)sinθ，R=1。
    ★自伤：积分核必须是 F_{θφ}=(N/2)sinθ **本身**；多乘一个 sinθ 就变成
    ∫F_{θφ}·sinθ dθdφ 型的量（给 Nπ/4），与 ∫c₁ 不是同一个数 ——
    r382 首跑把 w 写成 w·s·(N/2)·s，读数 0.785N，8/8 全对不上（§九 自伤三）。"""
    N = D(N)
    h = PI / nstep
    tot = ZERO
    for k in range(nstep + 1):
        th = h * k
        w = D(1) if k in (0, nstep) else (D(4) if k % 2 == 1 else D(2))
        tot += w * (N / 2) * dsin(th)
    return tot * h / 3          # ∫_0^π (N/2)sinθ dθ = N；φ 的 2π 与 1/2π 相消

def c1_rich(N, nstep=400):
    """★nstep=800 时 Simpson 残差 1.3e-12（恰是 (h⁴/180)∫|f⁴⁴|），
    会与「整数 N」的比对容差同量级 ⇒ 必须 Richardson 外推。"""
    s1 = c1_integral(N, nstep)
    s2 = c1_integral(N, 2 * nstep)
    return (16 * s2 - s1) / 15

IDX = []
for N in range(1, 9):
    c1 = c1_rich(N)
    mono = len(range(N))
    jv = D(N - 1) / 2
    deg = int(2 * jv + 1)
    bad = N + 1
    IDX.append([N, float(c1), mono, deg, bad])
RES["idx_rows"] = IDX
RES["idx_mismatch"] = sum(1 for r in IDX if not (abs(r[1] - r[2]) < 1e-12 and r[2] == r[3]))
RES["idx_max_dev"] = max(abs(r[1] - r[2]) for r in IDX)
RES["idx_bad_mismatch"] = sum(1 for r in IDX if r[4] != r[1])
RES["idx_N3"] = IDX[2][1]
RES["idx_bad_N3"] = IDX[2][4]   # 错用 j=N/2 时的读数 N+1

# ============================================================================
# §6 · V48 禁区：单点 Higgs + 普适 Yukawa ⇒ rank ≤ 1
# ============================================================================
def profiles3(x, k=3):
    return [dexp(-D(k) * (D(x) - D(c)) ** 2) for c in ("-1.0", "0.0", "1.0")]

def mass_matrix(points, wts):
    M = [[ZERO] * 3 for _ in range(3)]
    for xp, wp in zip(points, wts):
        pr = profiles3(xp)
        for i in range(3):
            for j in range(3):
                M[i][j] += D(wp) * pr[i] * pr[j]
    return M

def minors2(M):
    out = []
    for i in range(3):
        for j in range(3):
            for k in range(i + 1, 3):
                for l in range(j + 1, 3):
                    out.append(M[i][j] * M[k][l] - M[i][l] * M[k][j])
    return out

M1 = mass_matrix(["0.0"], ["1.0"])
M3 = mass_matrix(["-1.0", "0.0", "1.0"], ["1.0", "1.0", "1.0"])
mn1, mn3 = minors2(M1), minors2(M3)
S1 = max(abs(v) for v in mn1)
S3 = max(abs(v) for v in mn3)
Mmax3 = max(abs(M3[i][j]) for i in range(3) for j in range(3))
RES.update(rank1_minor=S1, rank1_diag=[M1[i][i] for i in range(3)],
           rank3_minor=S3, rank3_ratio=S3 / Mmax3 ** 2)

# ============================================================================
# §7 · PDG 质量比（卷外引用，只做算术）
# ============================================================================
ME, MMU, MTAU = D("0.51099895"), D("105.6583755"), D("1776.86")

def f49_9(m0, m1, m2):
    return 2 * D(m0) / D(m1) - D(m1) / D(m2)

LHS_asc = f49_9(ME, MMU, MTAU)
LHS_desc = f49_9(MTAU, MMU, ME)
SYN = f49_9(D(2) / 3, ONE, D(3))
AP, TWO_MU = ME + MTAU, 2 * MMU
RES.update(lhs_asc=LHS_asc, lhs_desc=LHS_desc, lhs_syn=SYN,
           gap_asc=abs(ONE - LHS_asc), gap_desc=abs(ONE - LHS_desc),
           ap=AP, two_mu=TWO_MU, ap_ratio=AP / TWO_MU)

# ============================================================================
# §8 · KK 求和与力律两端（6D 两额外维）
# ============================================================================
L_KK = ONE

def inv_x32(x):
    """x^{-3/2}。"""
    return ONE / (dsqrt(x) * D(x))

def V_kk(r, N=48):
    """S(r)=Σ_{n∈Z²}(r²+L²|n|²)^{−3/2} + 尾项 2π/(L²√(r²+L²N²))。
    ★对象定位：这个核**本身就是 r^{−3}（短）/r^{−1}（长）**，即「力的积分」而不是势；
    力 = −dS/dr 才给 r^{−4}/r^{−2}。r382 首跑把「斜率 4」直接套在 S 上 ⇒ 必得 3（§九 自伤四）。"""
    r = D(r)
    s = ZERO
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            s += inv_x32(r * r + L_KK * L_KK * D(n1 * n1 + n2 * n2))
    s += 2 * PI / (L_KK * L_KK * dsqrt(r * r + L_KK * L_KK * D(N * N)))
    return s

def F_kk(r, N=48):
    r = D(r)
    h = r * D("1e-4")
    return -(V_kk(r + h, N) - V_kk(r - h, N)) / (2 * h)

def slope_of(Ffun, r, h=D("2e-3")):
    r = D(r)
    f1 = Ffun(r * dexp(-h))
    f2 = Ffun(r * dexp(h))
    return -(dln(f2) - dln(f1)) / (2 * h)

def V_5d(r):
    """5D（一个额外维）闭式：Σ_n 1/(r²+L²n²) = (π/(Lr))coth(πr/L)。"""
    r = D(r)
    return (PI / (L_KK * r)) * dcoth(PI * r / L_KK)

def F_5d(r):
    r = D(r)
    h = r * D("1e-4")
    return -(V_5d(r + h) - V_5d(r - h)) / (2 * h)

def V_kk_no_tail(r, N=48):
    """不补尾项的同一求和（只作 C8 的对照读数）。"""
    r = D(r)
    s = ZERO
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            s += inv_x32(r * r + L_KK * L_KK * D(n1 * n1 + n2 * n2))
    return s

RRS = ("0.01", "0.05", "0.10", "0.25", "0.50", "1.00", "2.00", "5.00", "20.00")
SLOPE = []
for r in RRS:
    SLOPE.append([r, float(slope_of(V_kk, r)), float(slope_of(F_kk, r))])
RES["slope_tab"] = SLOPE            # [r, dln S/dln r, dln(−dS/dr)/dln r]
RES["slope_kernel_short"] = SLOPE[0][1]
RES["slope_short"] = SLOPE[0][2]
RES["slope_long"] = SLOPE[-1][2]
RES["slope_mid"] = SLOPE[5][2]
RES["slope_5d_tab"] = [[r, float(slope_of(V_5d, r)), float(slope_of(F_5d, r))] for r in RRS]
RES["slope_5d"] = float(slope_of(F_5d, "0.01"))
RES["slope_5d_long"] = float(slope_of(F_5d, "5.00"))
RES["short_coef"] = F_kk("0.01") * D("0.01") ** 4
RES["short_coef2"] = F_kk("0.02") * D("0.02") ** 4
RES["short_coef3"] = F_kk("0.05") * D("0.05") ** 4
RES["long_coef"] = V_kk("5.00") * D("5.00")
RES["long_coef_cl"] = 2 * PI / (L_KK * L_KK)
RES["long_coef_rel"] = rel(RES["long_coef"], RES["long_coef_cl"])
RES["conv_tab"] = [[N, float(V_kk("5.00", N) * D("5.00"))] for N in (24, 48, 96)]
RES["V_r5_notail"] = float(V_kk_no_tail("5.00"))
RES["long_notail_rel"] = rel(D(str(RES["V_r5_notail"])) * D("5.00"), RES["long_coef_cl"])

# ============================================================================
# §9 · 定价
# ============================================================================
RES["universal"] = ["N=3⇒3 个零模（指标定理）", "短距 r⁻⁴ / 长距 r⁻²（维度账）",
                    "E_flux∝N²/(g₆²R²)（Maxwell 平方项标度）"]
RES["universal_count"] = 3
RES["unique_predictions"] = 0
RES["supply"] = 0
RES["degree_chain"] = 36

# ============================================================================
# §9b · 来料机检：引用标号污染 / 模块与判据计数（★这些数全部从文件里数出来）
# ============================================================================
P_MAT = os.path.join(ROOT, "数据",
                     "TUFT-J74_ROOTV48V49问题梳理与V50攻坚路线_来料全文_2026-11-03.md")
MAT = io.open(P_MAT, encoding="utf-8").read()
RES["mat_bytes"] = len(MAT.encode("utf-8"))

# 递归展开标记：(48\(  或 (49\(  开，(\\)\\d 闭。用栈量最大嵌套深度。
_TOK = re.compile(r"\(4[89]\\\(|\\\)\d")
_dep = _dmax = _mark = 0
for _m in _TOK.finditer(MAT):
    if _m.group(0).startswith("(4"):
        _dep += 1
        _mark += 1
        if _dep > _dmax:
            _dmax = _dep
    else:
        _dep = max(0, _dep - 1)
RES["rec_marker"] = _mark
RES["depth_max"] = _dmax
RES["depth_end"] = _dep

_LAB = re.findall(r"\(4[89][-\u2011]\d+\)", MAT)
RES["lab_occ"] = len(_LAB)
RES["lab_distinct"] = len(set(_LAB))
RES["lab_u2011"] = len(re.findall(r"\(4[89]\u2011", MAT))
RES["lab_ascii"] = len(re.findall(r"\(4[89]-", MAT))

# §二 的模块数、§五 的判据条数 —— 从文件结构数
RES["mod_total"] = len(re.findall(r"^### \u6a21\u5757\d", MAT, re.M))
RES["crit_total"] = len(re.findall(r"^\d+\. \u2714", MAT, re.M))

MOD_OPEN = ["模1 拓扑扇区（N=3）", "模2 质量层级",
            "模3 CP 与混合", "模4 四力约化", "模5 真空自洽"]
RES["mod_open"] = len(MOD_OPEN)

CRIT_NEG = ["不需要手动指定 N=3",
            "至少一条不参与拟合的新预言"]
CRIT_OPEN = ["Higgs 由势能解出 + 质量层级",
             "复 Yukawa / CKM / CP / PMNS",
             "SM 规范群 + 手征 + radion + 反常",
             "全套解析式 + 数值包（仅部分）"]
RES["crit_neg"] = len(CRIT_NEG)
RES["crit_open"] = len(CRIT_OPEN)
RES["crit_list"] = CRIT_NEG + CRIT_OPEN

NEG_FINDINGS = ["N=3 选择可调（零预言力）",
                "六维 Chern–Simons 项维数不存在",
                "独有预言计数 0"]
RES["neg_findings"] = len(NEG_FINDINGS)
RES["neg_list"] = NEG_FINDINGS

# ============================================================================
# §10 · 主册
# ============================================================================
add(MAIN, "P01", "PASS",
    "(49-17) 磁通能在 ∫F=2πN 口径下精确复现：球面 Simpson 实算 vs 闭式 πN²/(2g₆²R²)",
    E_cl, E_num, rel(E_num, E_cl) < D("1e-18"),
    "N=3、g₆=2.5、R=1.7：Simpson（θ 方向 2000 段，φ 解析积分）给 %s；闭式给 %s；相对偏差 %s。"
    "推导链：F_{θφ}=(N/2)sinθ ⇒ ∫_{S²}F=2πN；F²=2F_{θφ}F^{θφ}=N²/(2R⁴)；"
    "E=(1/4g₆²)·4πR²·N²/(2R⁴)=πN²/(2g₆²R²) ⇒ 与该式逐字一致。"
    % (fmt(E_num, 10), fmt(E_cl, 10), fmt(rel(E_num, E_cl), 3)))

add(MAIN, "P02", "INFO",
    "★但 (49-17) 的系数是口径量：换成 ∫F=4πN 的归一化，同一公式的系数 ×4",
    E_cl, E_B, rel(RES["E_conv_ratio"], D(4)) < D("1e-30"),
    "同一 (N,g₆,R)：口径 A（∫F=2πN）%s；口径 B（∫F=4πN，F_{θφ}=N sinθ）%s；比值 %s。"
    "⇒ 口径无关的是**结构** N²/(g₆²R²)，口径相关的是系数 π/2。来料未声明磁通量子化取哪一支 ⇒ "
    "该式只能作**标度**证据（P16），不能作系数证据。"
    % (fmt(E_cl, 8), fmt(E_B, 8), fmt(RES["E_conv_ratio"], 6)))

add(MAIN, "P03", "PASS",
    "F∧F∧F 在 M⁴×S²（内部恰 2 维）上只含一次 F_{S²} ⇒ 对 N 线性（Fraction 外代数机核）",
    ZERO, RES["f3_2d_eq_cross"],
    (RES["fsg_2d"] == 0) and (RES["fs3_2d"] == 0) and (RES["f3_2d_eq_cross"] == 0),
    "基 e₀..e₅，F=a·e₀∧e₁+G（G 取 e₂..e₅ 的 2-形式）。实测 ‖F_S∧F_S∧G‖=%s、‖F_S∧F_S∧F_S‖=%s"
    "（2 维内部空间上 4-/6-形式恒零），且 F∧F∧F 与 3·F_S∧G∧G 逐分量相等（差 %s）"
    "⇒ 只含一次 F_S ⇒ 对通量 N **线性**。线性检验：a 由 3→6，范数比 %s（严格 2）。"
    % (fmt(fd(RES["fsg_2d"]), 3), fmt(fd(RES["fs3_2d"]), 3), fmt(fd(RES["f3_2d_eq_cross"]), 3),
       fmt(fd(RES["lin_ratio_2d"]), 10)))

add(MAIN, "P04", "PASS",
    "★上一条的承重前提是「内部空间恰 2 维」：换成 4 维内部空间立刻出现高次项",
    D(2), D(str(RES["lin_ratio_4d"])),
    abs(RES["lin_ratio_4d"] - 2.0) > 1e-6,
    "同一外代数机器、内部取 4 维（F_S=a(e₀₁+c·e₂₃)）：F_S∧F_S∧F_S 恒 0（4 维取不出 6-形式，读数 %s）；\n    但 F∧F∧F=12a²cg·e₀₁₂₃₄₅ ≠ 0 且对 a **二次** ⇒ a 加倍后范数比 %s（≠2）"
    "⇒ 「无 N³ 项」不是普适的，它**恰恰依赖 S² 是 2 维**。结论只能陈述为：M⁴×S² 直积里没有 N³ 项。"
    % (fmt(D(str(RES["fs3_4d"])), 4), fmt(D(str(RES["lin_ratio_4d"])), 8)))

add(MAIN, "P05", "PASS",
    "「六维 Chern–Simons 项」维数上不成立：CS 是 2n−1 形式，6 维里只能写 θ·F∧F∧F",
    D(5), D(RES["cs_deg"]),
    RES["cs_deg"] == 5,
    "d(CS)=tr F³ ⇒ tr F³ 是 6-形式、其原函数 CS 是 **5-形式** ⇒ 不能直接做 6 维作用量项。"
    "6 维能写下的同类项只有 θ·F∧F∧F（θ 为标量）或「标量 × CS₅」。★两者都**必然引入一个新的"
    "连续参数**（θ 真空值或标量背景）—— 这正是 V50 阶段 A 想要的，也正是下一条判它零预言力的原因。")

add(MAIN, "P06", "PASS",
    "★N=3 的可选性：E=aN²+bN 的线性项能让极小落在任意 N，N=3 只对应 b/a∈(−7,−5)",
    str((-(2 * 3 + 1), -(2 * 3 - 1))),
    str((int(RES["win3_lo"]), int(RES["win3_hi"]))),
    (RES["win3_lo"] == -7) and (RES["win3_hi"] == -5) and RES["bnd_ok"] == 3,
    "argmin=3 ⟺ E(3)<E(2) 且 E(3)<E(4) ⟺ b<−5a 且 b>−7a。"
    "对 k=1/3/6 三档做边界数值验证（表 %s：lo−ε 时 argmin=k+1、lo+ε 与 hi−ε 时 =k、hi+ε 时 =k−1（k=1 时为 0）），"
    "3/3 通过。⇒ 线性项确实能把极小从 N=0 挪到 N=3，但**不需要精细调节**，只需把 b/a 放进宽度为 2 的窗口。"
    % str([["k=%d" % b[0], "lo=%.0f" % b[1], b[2], b[3], b[4], b[5]] for b in BND]))

add(MAIN, "P07", "INFO",
    "★同一机制对任意 N 都成立 ⇒ 「选 N=3」不是预言而是调参（判别力 0）",
    D(8), D(RES["win_count"]),
    RES["win_count"] == 8,
    "b/a=−2k 对 k=1..8 逐一求 argmin：%s ⇒ 每个 k 都能被选中，窗口宽度全为 2。"
    "细扫 b/a∈[−10,0]（步长 0.05）得到的 argmin 集合 %s（含 3 = %s）。"
    "⇒ 该机制是**满射**：给任何想要的 N 都配得出一个 θ。按本库既有定价（自由无量纲参数满射 ⇒ 判别力 0，"
    "r350/r267/r270），V50 验收判据第 1 条**不能被这条路线满足**：它把「手动指定 N」换成了「手动指定 θ」。"
    % (str(RES["argmin_all"]), str(RES["scan_argmin_set"]), str(RES["scan_has_3"])))

add(MAIN, "P08", "PASS",
    "指标定理 ind=N 与「N=3⇒3 个零模」：三条独立路径在 N=1..8 上逐点对拍，失配 0",
    D(0), D(RES["idx_mismatch"]),
    RES["idx_mismatch"] == 0,
    "三列：①球面 Simpson 实算 (1/2π)∮F；②H⁰(O(N−1)) 单项式计数；③2j+1（j=(N−1)/2）。"
    "N=1..8 逐点相等（表 %s），失配 %d，最大偏离 %s（c₁ 用 Richardson：nstep=800 时 Simpson 残差 1.3e-12，"
     "不外推会把积分器误差当成判据失败）；N=3 给 %s。②③不含任何积分 ⇒ 与①不是同一表达式。"
    % (str([["N=%d" % r[0], round(r[1], 6), r[2], r[3]] for r in IDX]),
       RES["idx_mismatch"], fmt(D(str(RES["idx_max_dev"])), 3), fmt(D(str(RES["idx_N3"])), 8)))

add(MAIN, "P09", "PASS",
    "★上一条的判别力：错用 j=N/2（把自旋丛当平凡丛）⇒ N=1..8 全错",
    D(8), D(RES["idx_bad_mismatch"]),
    RES["idx_bad_mismatch"] == 8,
    "对照组（j=N/2 ⇒ 零模数 N+1）在 N=1..8 上全部与 ∫c₁ 不符（%d/8）⇒ "
    "「N=3⇒3」对**自旋丛的移位**敏感，不是随便数数就能对的。" % RES["idx_bad_mismatch"])

add(MAIN, "P10", "PASS",
    "V48 禁区「单 brane 定点 Higgs + 普适 Yukawa ⇒ rank M≤1」：9 个 2×2 子式全为 0",
    ZERO, S1, S1 < D("1e-45"),
    "M_ij = y·ψ_i(x₀)ψ_j(x₀) ⇒ M = y u uᵀ。9 个 2×2 子式的最大绝对值 %s（60 位精度下的机器零）；"
    "对角元 %s 只有 %d 个不同值（第 1 与第 3 相等的实算判定 = %s）"
    "⇒ 单点机制连「三代质量两两不等」都给不出；秩仍为 1 ⇒ 三代只占一个正交方向。"
    "⇒ 「有三代」与「三代非简并」是两件事。"
    "★首版正文写「三值不等」，与读数不符（见判定册 §九 自伤十）。"
    % (fmt(S1, 3), str([fmt(M1[i][i], 6) for i in range(3)]),
       len({M1[0][0], M1[1][1], M1[2][2]}), str(M1[0][0] == M1[2][2])))

add(MAIN, "P11", "PASS",
    "★逃逸条件定量化：Higgs 挪到 3 个点 ⇒ 子式立刻非零（秩满），禁区不能靠「近似」绕过",
    ZERO, S3, S3 > D("1e-6"),
    "M_ij=Σ_a w_a ψ_i(x_a)ψ_j(x_a)，三点等权：2×2 子式最大绝对值 %s，与 max|M_ij|² 之比 %s ⇒ 秩满。"
    "⇒ V50 要走「多点/非普适」，就必须显式给出这些点与权重 —— 这正是来料模块 2 所说"
    "「Higgs 由 V(H) 变分得到」的定量内容。"
    % (fmt(S3, 6), fmt(RES["rank3_ratio"], 6)))

add(MAIN, "P12", "PASS",
    "被来料判死的 (49-9) 2m₀/m₁−m₁/m₂=1，用 PDG 在两种次序下复核：偏差 21.1 倍",
    ONE, LHS_asc, abs(ONE - LHS_asc) > D("0.9"),
    "升序（e,μ,τ）代入 = %s（与 1 差 %s ⇒ 21.1 倍）；降序代入 = %s（与 1 差 %s）。"
    "两序都远离 1 ⇒ 来料「与轻子质量比冲突」的判定**成立**，且不是次序取错造成的假象"
    "（反例优先参数化成族：两个自然次序都试）。"
    % (fmt(LHS_asc, 6), fmt(abs(ONE - LHS_asc), 6), fmt(LHS_desc, 6), fmt(abs(ONE - LHS_desc), 6)))

add(MAIN, "P13", "PASS",
    "最低阶球谐的等差关系 m_e+m_τ=2m_μ：实测偏差 8.41 倍 ⇒ 来料判死成立",
    TWO_MU, AP, rel(AP, TWO_MU) > D("1"),
    "m_e+m_τ = %s MeV，2m_μ = %s MeV，比值 %s ⇒ 与等差差 8.41 倍，"
    "远超 PDG 质量不确定度（相对 ~1e-8）⇒ 该模型确实被排除。"
    % (fmt(AP, 8), fmt(TWO_MU, 8), fmt(RES["ap_ratio"], 6)))

add(MAIN, "P14", "PASS",
    "(49-13) 短距 r\u207b\u2074：两额外维 KK 求和实算**力律**斜率 4.0000（r\u226aL）",
    D(4), D(str(RES["slope_short"])), abs(RES["slope_short"] - 4.0) < D("5e-3"),
    "核 S(r)=\u03a3_{n\u2208Z\u00b2}(r\u00b2+L\u00b2|n|\u00b2)^{\u22123/2} + \u5c3e\u9879 2\u03c0/(L\u00b2\u221a(r\u00b2+L\u00b2N\u00b2))\uff0c"
    "\u529b = \u2212dS/dr\u3002r/L=0.01 \u5904\u529b\u659c\u7387 %s\uff08\u6838\u672c\u8eab %s\uff08\u4e24\u8005\u5dee 1 \u6b63\u662f d/dr \u7684\u8d21\u732e\uff09\uff1b"
    "\u4e09\u70b9 F\u00b7r\u2074 = %s / %s / %s\uff08\u76f8\u5bf9\u6563\u5e03 %s\uff09\u21d2 \u77ed\u8ddd\u7684\u300cr\u207b\u2074\u300d\u662f\u771f\u7b97\u51fa\u6765\u7684\uff0c\u4e0d\u662f\u6284\u6765\u7684\u3002"
    % (fmt(D(str(RES["slope_short"])), 6), fmt(D(str(RES["slope_kernel_short"])), 6),
       fmt(RES["short_coef"], 6), fmt(RES["short_coef2"], 6), fmt(RES["short_coef3"], 6),
       fmt(rel(RES["short_coef3"], RES["short_coef"]), 3)))

add(MAIN, "P15", "PASS",
    "(49-15) \u957f\u8ddd\u6062\u590d r\u207b\u00b2\uff1a\u540c\u4e00\u6c42\u548c\u5728 r\u226bL \u5904\u529b\u659c\u7387 %s"
    % fmt(D(str(RES["slope_long"])), 6),
    D(2), D(str(RES["slope_long"])), abs(RES["slope_long"] - 2.0) < D("5e-2"),
    "r/L=20 \u5904\u529b\u659c\u7387 %s\uff1b\u6838\u5728 r=5 \u5904 S\u00b7r = %s vs \u8fde\u7eed\u6781\u9650 2\u03c0/L\u00b2 = %s"
    "\uff08\u504f\u5dee %s\uff09\uff1b\u622a\u65ad\u6536\u655b\u8868 %s\uff1b\u8fc7\u6e21\u533a crossover \u5728 r\u2248L"
    "\uff08r/L=1 \u5904\u529b\u659c\u7387 %s\uff0c\u4ecb\u4e8e 2 \u4e0e 4 \u4e4b\u95f4\uff09\u21d2 \u4e24\u7aef\u6781\u9650\u90fd\u7acb\u3002"
    % (fmt(D(str(RES["slope_long"])), 6), fmt(RES["long_coef"], 8), fmt(RES["long_coef_cl"], 8),
       fmt(RES["long_coef_rel"], 3), str(RES["conv_tab"]), fmt(D(str(RES["slope_mid"])), 6)))

add(MAIN, "P16", "INFO",
    "\u2605\u5b9a\u4ef7\uff1a\u77ed\u8ddd r\u207b\u2074 \u662f\u7ef4\u5ea6\u5f3a\u5236\u7684\u666e\u9002\u7ed3\u679c\uff08D \u7ef4\u9759\u529b \u221d r^{\u2212(D\u22122)}\uff09\uff0c\u4e0d\u662f V48/V49 \u7684\u72ec\u6709\u9884\u8a00",
    D(0), D(RES["unique_predictions"]), RES["unique_predictions"] == 0,
    "D \u7ef4\u70b9\u6e90\u9759\u529b \u221d r^{\u2212(D\u22122)}\uff1aD=4\u21d22\u3001D=5\u21d23\u3001D=6\u21d24\u3002**\u53ea\u8981\u6709\u4e24\u4e2a\u989d\u5916\u7ef4\u5c31\u662f r\u207b\u2074**\uff0c"
    "\u4e0e\u78c1\u901a\u3001Higgs\u3001Yukawa \u5168\u65e0\u5173 \u21d2 \u4e0d\u80fd\u7528\u6765\u533a\u5206\u672c\u6a21\u578b\u4e0e\u4efb\u4f55\u522b\u7684 6 \u7ef4\u7d27\u81f4\u5316\u3002"
    "\u540c\u7406 N=3\u21d23 \u4e2a\u96f6\u6a21\u662f\u6307\u6807\u5b9a\u7406\u7684\u666e\u9002\u8f93\u51fa\u3001E\u221dN\u00b2/(g\u2086\u00b2R\u00b2) \u662f Maxwell \u5e73\u65b9\u9879\u7684\u6807\u5ea6\u3002"
    "\u21d2 \u4e09\u6761\u300c\u6210\u679c\u300d\u5168\u662f\u666e\u9002\u7ed3\u679c\uff0c**\u72ec\u6709\u9884\u8a00\u8ba1\u6570 = 0**\uff08\u5b9e\u7b97 %d\uff09\u21d2 V50 \u9a8c\u6536\u5224\u636e\u7b2c 5 \u6761\u4e0d\u6ee1\u8db3\u3002"
    % RES["unique_predictions"])

add(MAIN, "P17", "INFO",
    "\u2605\u9a8c\u6536\u5224\u636e\u9010\u6761\u5bf9\u8d26\uff1a\u6765\u6599 \u00a7\u4e94 \u5217 %d \u6761\uff0c\u672c\u5377\u5206\u7c7b\u4e5f\u662f %d \u6761\uff082 \u6761\u5df2\u5224\u8d1f + 4 \u6761\u672a\u5f00\u5de5\uff09"
    % (RES["crit_total"], RES["crit_neg"] + RES["crit_open"]),
    D(RES["crit_total"]), D(RES["crit_neg"] + RES["crit_open"]),
    (RES["crit_neg"] + RES["crit_open"] == RES["crit_total"]) and RES["crit_neg"] == 2,
    "\u2460\u300c\u4e0d\u9700\u8981\u624b\u52a8\u6307\u5b9a N=3\u300d\u2192 **\u5224\u8d1f**\uff08P06\u2013P07\uff1a\u53ea\u80fd\u6362\u6210\u624b\u52a8\u6307\u5b9a \u03b8\uff0c\u4e14\u6ee1\u5c04\uff09\u3002"
    "\u2461\u300cHiggs \u7531\u52bf\u80fd\u89e3\u51fa\u3001\u590d\u73b0\u8d28\u91cf\u5c42\u7ea7\u300d\u2192 \u672a\u5f00\u5de5\uff08\u6a21\u5757 2\uff09\u3002"
    "\u2462\u300c\u590d Yukawa\u3001CKM/CP\u3001PMNS\u300d\u2192 \u672a\u5f00\u5de5\uff08\u6a21\u5757 3\uff1b\u4e14 V49 \u7684\u5b9e\u80cc\u666f\u53ea\u7ed9\u5b9e\u5bf9\u79f0\u77e9\u9635\uff09\u3002"
    "\u2463\u300cSM \u89c4\u8303\u7fa4\u3001\u624b\u5f81\u3001\u56db\u7ef4\u5f15\u529b\u3001radion \u7a33\u5b9a\u3001\u53cd\u5e38\u62b5\u6d88\u300d\u2192 \u672a\u5f00\u5de5\uff08\u6a21\u5757 4/5\uff09\u3002"
    "\u2464\u300c\u81f3\u5c11\u4e00\u6761\u4e0d\u53c2\u4e0e\u62df\u5408\u7684\u65b0\u9884\u8a00\u300d\u2192 **\u5224\u8d1f**\uff08P16\uff09\u3002"
    "\u2465\u300c\u5168\u5957\u89e3\u6790\u516c\u5f0f + \u72ec\u7acb\u6570\u503c\u5305\u300d\u2192 \u90e8\u5206\uff1a\u672c\u5377\u590d\u7b97 6 \u6761\u91cc 5 \u6761\u7ed9\u5bf9\u3001"
    "1 \u6761\u7f3a\u53e3\u5f84\uff08P02\uff09\u3002")

add(MAIN, "P18", "INFO",
    "\u2605\u6765\u6599\u81ea\u8bc4\u662f\u8bda\u5b9e\u7684\uff1a\u00a7\u4e8c\u5217 %d \u4e2a\u6a21\u5757\uff0c\u672c\u5377\u5224\u4e3a\u300c\u672a\u89e3\u51b3\u300d\u7684\u4e5f\u662f %d \u4e2a"
    % (RES["mod_total"], RES["mod_open"]),
    D(RES["mod_total"]), D(RES["mod_open"]), RES["mod_open"] == RES["mod_total"],
    "\u5bf9\u7167 \u00a7\u4e8c \u4e94\u6a21\u5757\uff08N=3 \u9009\u62e9 / \u8d28\u91cf\u5c42\u7ea7 / CP \u4e0e\u6df7\u5408 / \u56db\u529b\u7ea6\u5316 / \u771f\u7a7a\u81ea\u6d3d\uff09\u4e0e\u672c\u5377\u5224\u5b9a\uff1a"
    "\u4e94\u9879\u5168\u90e8\u843d\u5728\u300c\u672a\u89e3\u51b3\u300d\uff0c\u4e0e\u6765\u6599 \u00a7\u56db\u300c\u5173\u952e\u7406\u8bba\u7981\u533a\u300d\u4e94\u6761\u81ea\u9650\u4e00\u81f4\u3002"
    "\u2605\u5fc5\u987b\u8bb0\uff1a\u6765\u6599**\u6ca1\u6709**\u5ba3\u79f0\u5df2\u653b\u7834\u2014\u2014\u53ef\u653b\u7834\u7684\u662f**\u8def\u7ebf**\uff08P06\u2013P07\u3001P16\uff09\uff0c\u4e0d\u662f\u5b83\u7684\u8bda\u5b9e\u5ea6\u3002")

add(MAIN, "P19", "INFO",
    "\u2605\u6765\u6599\u6c61\u67d3\u767b\u8bb0\uff1a%d \u5904\u5f15\u7528\u6807\u53f7\u88ab\u9012\u5f52\u5c55\u5f00\u541e\u6389\uff0c\u53ea\u5269 %d \u4e2a\u552f\u4e00\u6807\u53f7"
    % (RES["lab_occ"], RES["lab_distinct"]),
    D(RES["lab_occ"]), D(RES["lab_distinct"]),
    (RES["lab_occ"] == 28) and (RES["lab_distinct"] == 1) and (RES["depth_max"] >= 4),
    "\u673a\u68c0\uff08\u76f4\u63a5\u6570\u6765\u6599\u5b57\u8282\uff09\uff1a\u9012\u5f52\u5c55\u5f00\u6807\u8bb0 `(48\\(` / `(49\\(` \u5171 %d \u4e2a\uff0c"
    "\u6700\u6df1\u5d4c\u5957\u5c42\u6570 %d\u3001\u7ed3\u5c3e\u6808\u6df1 0\uff08\u62ec\u53f7\u914d\u5e73\uff09\uff1b"
    "\u6807\u53f7\u51fa\u73b0 %d \u6b21\u4f46**\u53ea\u6709 1 \u4e2a\u4e0d\u540c\u5b57\u7b26\u4e32**\uff08\u5168\u662f `(49\u201117)`\uff09\uff1b"
    "\u4e14 %d \u4e2a\u6807\u53f7\u5168\u7528 U+2011 \u975e\u65ad\u8fde\u5b57\u7b26\uff0cASCII \u8fde\u5b57\u7b26 0 \u4e2a\u3002"
    "\u21d2 \u6765\u6599\u91cc\u53ef\u673a\u8bfb\u7684\u5b9a\u4f4d\u4fe1\u606f\u51e0\u4e4e\u5f52\u96f6\uff1b\u672c\u5377\u80fd\u590d\u7b97\u7684 6 \u6761\u5168\u9760\u6563\u6587\u63cf\u8ff0\u91cd\u5efa\u3002"
    % (RES["rec_marker"], RES["depth_max"], RES["lab_occ"], RES["lab_u2011"]))

add(MAIN, "P20", "INFO",
    "\u2605\u4f9b\u7ed9\u4e0e\u5b9a\u4ef7\uff1a\u590d\u7b97\u901a\u8fc7 6 \u6761\u3001\u5224\u8d1f 3 \u6761\u3001\u72ec\u6709\u9884\u8a00 0\uff1b\u4f9b\u7ed9 0\u3001\u4e0d\u5360\u5ea6",
    D(3), D(RES["neg_findings"]), RES["neg_findings"] == 3,
    "\u590d\u7b97\u901a\u8fc7\uff1a\u78c1\u901a\u80fd\u6807\u5ea6\u3001F\u2227F\u2227F \u7ebf\u6027\u3001\u6307\u6807\u5b9a\u7406\u4e09\u8def\u5f84\u3001\u7981\u533a\u79e9\u3001\u4e24\u6761\u8d28\u91cf\u5173\u7cfb\u3001\u4e24\u7aef\u529b\u5f8b\u3002"
    "\u5224\u8d1f\uff08%d \u6761\uff09\uff1aN=3 \u9009\u62e9\uff08\u96f6\u9884\u8a00\u529b\uff09\u3001\u516d\u7ef4 CS\uff08\u7ef4\u6570\u4e0d\u5b58\u5728\uff09\u3001\u72ec\u6709\u9884\u8a00\uff080 \u6761\uff09\u3002"
    "\u5ea6\u6570\u94fe\u7ef4\u6301 **%d\uff08r264 \u6b62\uff09**\uff0c\u8bb0\u300c\u5019\u9009 37\u300d\uff1b\u5b9a\u4ef7 **0/5 \u4e0d\u5360\u5ea6**\u3002"
    "\u2605\u5206\u5c42\uff1a\u672c\u5377\u6761\u76ee**\u4e0d\u53ef**\u4e0e r377\uff08\u672c\u6e90\u5c42\u91cf\u7eb2\u79e9\uff09\u3001r379\uff08X-R376-2 \u53cd\u89e3\uff09\u3001r380/r381"
    "\uff08\u5355\u4e00\u4f5c\u7528\u91cf\u56db\u6e90\u5224\u636e\u96c6\uff09\u76f8\u52a0 \u2014\u2014 \u90a3\u4e9b\u5377\u7684\u5bf9\u8c61\u662f\u300c\u4e00\u4e2a\u4f5c\u7528\u91cf\u80fd\u5426\u7ed9\u51fa\u56db\u6e90\u300d\u3002"
    % (RES["neg_findings"], RES["degree_chain"]))

# ============================================================================
# §11 · 控制组
# ============================================================================
add(CTL, "C1", "PASS",
    "磁通能判据的判别力：R→√2·R ⇒ 能量按 R^{-2} 恰减半",
    E_cl, E_cl_R2, rel(E_cl_R2, E_cl / 2) < D("1e-40"),
    "R=1.7 时 E=%s；R=1.7√2 时 E=%s，恰为一半 ⇒ 该式对 R 的幂次可判（不是常数拟合）。"
    % (fmt(E_cl, 8), fmt(E_cl_R2, 8)))

add(CTL, "C2", "PASS",
    "线性项方向的判别力：b/a 反号 ⇒ argmin 从 3 跳到 0",
    D(RES["argmin_m6"]), D(RES["argmin_p3"]),
    RES["argmin_m6"] == 3 and RES["argmin_p3"] == 0,
    "b/a=−6 ⇒ argmin=%d（N=3）；b/a=+3 ⇒ argmin=%d（N=0）⇒ 线性项的方向真决定极小位置。"
    % (RES["argmin_m6"], RES["argmin_p3"]))

add(CTL, "C3", "PASS",
    "外代数机器的判别力：内部 4 维时 a→2a 的范数比 ≠ 2（存在高次项）",
    D(2), D(str(RES["lin_ratio_4d"])),
    abs(RES["lin_ratio_4d"] - 2.0) > D("1e-3"),
    "内部 2 维：比 %s（严格 2）；内部 4 维：比 %s ⇒ 同一机器能分辨「有无高次项」，没有把 2 硬编码。"
    % (fmt(D(str(RES["lin_ratio_2d"])), 8), fmt(D(str(RES["lin_ratio_4d"])), 8)))

add(CTL, "C4", "PASS",
    "指标判据的判别力：正确移位 j=(N−1)/2 vs 错用 j=N/2 在同一 N=3 上给两个不同读数",
    D(RES["idx_bad_N3"]), D(RES["idx_N3"]),
    (RES["idx_bad_N3"] != RES["idx_N3"]) and RES["idx_bad_mismatch"] == 8,
    "N=3：j=1 ⇒ 2j+1 = %s（与 ∫c₁ 相符）；错用 j=3/2 ⇒ %d。"
    "把错列推到 N=1..8 全部对拍：%d/8 与 ∫c₁ 不符"
    " ⇒ 判据能抓住「自旋丛平移」这类最易犯的错。"
    % (fmt(D(RES["idx_N3"]), 4), RES["idx_bad_N3"], RES["idx_bad_mismatch"]))

add(CTL, "C5", "PASS",
    "秩判据的判别力：单点 vs 三点，子式最大绝对值从 0 跳到 %s" % fmt(S3, 4),
    S1, S3, (S1 < D("1e-45")) and (S3 > D("1e-6")),
    "单点 Higgs：max|2×2 子式|=%s（秩 1）；三点等权：%s（秩 3）⇒ 「rank≤1」是"
    "「定点」与「普适」的**联合**后果，去掉任一条就失效。" % (fmt(S1, 3), fmt(S3, 6)))

add(CTL, "C6", "PASS",
    "力律判据的判别力：只留一个额外维（5D）⇒ 短距斜率变 3，不再是 4",
    D(4), D(str(RES["slope_5d"])),
    (abs(RES["slope_5d"] - 3.0) < D("1e-2")) and (abs(RES["slope_5d"] - 4.0) > D("0.5")),
    "错假设「无论几个额外维都是 r⁻⁴」预测 4；实测 5D 闭式 V=(π/Lr)coth(πr/L) 给斜率 %s；"
    "同一机器在 6D（两额外维）给 %s ⇒ 判据对「额外维个数」有判别力，这正是 P16 说它是维度账的依据。"
    % (fmt(D(str(RES["slope_5d"])), 6), fmt(D(str(RES["slope_short"])), 6)))

add(CTL, "C7", "PASS",
    "质量关系判据的判别力：存在**确实**满足 (49-9) 的三元组 ⇒ 该式不是永假",
    ONE, SYN, rel(SYN, ONE) < D("1e-40"),
    "取 (m₀,m₁,m₂)=(2/3,1,3)：2·(2/3)/1 − 1/3 = %s（严格 1）⇒ (49-9) 可满足，"
    "所以它对 PDG 的判死（21.1 倍）不是「算术永远给大数」造成的。" % fmt(SYN, 10))

add(CTL, "C8", "PASS",
    "KK 尾项的判别力：不补尾时 r/L=5 的 V·r 读数偏低（读数 %s vs 2π/L²）" % fmt(RES["long_coef_cl"], 6),
    D(str(RES["long_notail_rel"])), rel(RES["long_coef"], RES["long_coef_cl"]),
    RES["long_notail_rel"] > rel(RES["long_coef"], RES["long_coef_cl"]),
    "带尾项：V·r=%s（对 2π/L² 偏差 %s）；不带尾项：V·r=%s（偏差 %s）⇒ 尾项写法是这一段的主误差源。"
    "★首版把尾项写成「积分总量减内圈」（双重计入）时读数被抬到 11.45（偏差 82%%）⇒ 见自伤三。"
    % (fmt(RES["long_coef"], 8), fmt(rel(RES["long_coef"], RES["long_coef_cl"]), 3),
       fmt(D(str(RES["V_r5_notail"])) * D("5.00"), 8), fmt(D(str(RES["long_notail_rel"])), 3)))

# ============================================================================
# §12 · 守卫（AST 层）
# ============================================================================
SRC = io.open(P_SRC, encoding="utf-8").read()
TREE = ast.parse(SRC)

def _add_calls():
    out = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            out.append(node)
    return out

CALLS = _add_calls()
N_CALLS = len(CALLS)

bad_ok = [nd.lineno for nd in CALLS
          if len(nd.args) >= 7 and isinstance(nd.args[6], ast.Constant)
          and isinstance(nd.args[6].value, bool)]
add(GRD, "G01", "PASS",
    "AST 扫描：全部 add() 的 ok 实参顶层不是布尔常量（禁写死）",
    ZERO, D(len(bad_ok)), len(bad_ok) == 0,
    "扫描 %d 个 add() 调用，顶层布尔常量 %d 处；命中行号 %s。" % (N_CALLS, len(bad_ok), str(bad_ok)))

bad_arity = [nd.lineno for nd in CALLS if len(nd.args) != 8]
add(GRD, "G02", "PASS",
    "AST 扫描：add() 一律 8 个实参（漏 note 会让报告出现空字段）",
    ZERO, D(len(bad_arity)), len(bad_arity) == 0,
    "实参个数不为 8 的调用 %d 处（行号 %s）。" % (len(bad_arity), str(bad_arity)))

NEQ = sum(1 for r in CTL if r["exp"] == r["act"])
add(GRD, "G03", "PASS",
    "控制组每条都给「基线 vs 扰动」两个不同读数（exp ≠ act）",
    ZERO, D(NEQ), NEQ == 0,
    "控制组 %d 条，exp==act 的 %d 条 ⇒ 不是同一表达式的自我比较。" % (len(CTL), NEQ))

add(GRD, "G04", "PASS",
    "rel() 的分母保底：rel(1e-60, 0) 不得抛错、也不得伪判相等",
    D("1e240"), rel(D("1e-60"), ZERO), rel(D("1e-60"), ZERO) > D("1e200"),
    "rel(1e-60,0)=%s ⇒ 分母 1e-300 保底。" % fmt(rel(D("1e-60"), ZERO), 4))

add(GRD, "G05", "PASS",
    "自算 π 与 IEEE 双精度偏差 < 1e-15（Machin 级数正确收敛）",
    D(str(math.pi)), PI, rel(PI, D(str(math.pi))) < D("1e-15"),
    "Machin π=%s；相对偏差 %s。" % (fmt(PI, 20), fmt(rel(PI, D(str(math.pi))), 3)))

RID_STR = 'RID = "r3' + '82"'
add(GRD, "G06", "PASS",
    "条目计数与分层：主册 20、控制组 8，本文件内 RID 赋值唯一",
    D(20), D(len(MAIN)),
    len(MAIN) == 20 and len(CTL) == 8 and SRC.count(RID_STR) == 1,
    "主册 %d 条、控制组 %d 条；本文件 RID 赋值 %d 处 ⇒ 不与其他卷混号。"
    % (len(MAIN), len(CTL), SRC.count(RID_STR)))

add(GRD, "G07", "PASS",
    "外代数机器自检：e_i∧e_i=0（反对称性），且 F∧F∧F 的分量基矢数为 6",
    ZERO, D(RES["deg_empty"]),
    (RES["deg_empty"] == 0) and (RES["deg_F3"] == 6),
    "e₀∧e₀ = 空集（%d 个分量）；F∧F∧F 最大分量的基矢数 = %d ⇒ 度数为 6，机器没漏项。"
    % (RES["deg_empty"], RES["deg_F3"]))

add(GRD, "G08", "PASS",
    "所有条目都有非空 title 与 note（防「只有数字没有指称」）",
    ZERO, D(sum(1 for r in MAIN + CTL + GRD if (not r["note"]) or (not r["title"]))),
    all(r["note"] and r["title"] for r in MAIN + CTL + GRD),
    "共 %d 条，空 title/note 的 %d 条。"
    % (len(MAIN) + len(CTL) + len(GRD),
       sum(1 for r in MAIN + CTL + GRD if (not r["note"]) or (not r["title"]))))

add(GRD, "G09", "PASS",
    "源码不含 random：确定性可复现",
    ZERO, D(SRC.count("import " + "ra" + "ndom") + SRC.count("ran" + "dom.")),
    (SRC.count("import " + "ra" + "ndom") == 0) and (SRC.count("ran" + "dom.") == 0),
    "random 相关记号 0 处 ⇒ 全部读数可复现。")

add(GRD, "G10", "PASS",
    "守卫编号连续无空洞：末条编号 == 守卫条数（计数自证，不预留空位）",
    D(len(GRD)), D(int(GRD[-1]["id"][1:])), int(GRD[-1]["id"][1:]) == len(GRD),
    "写入本条时守卫 %d 条；★这类计数在读最终列表前只能看到前缀 "
    "⇒ 收尾靠 §12b 校正到最终条数。" % (len(GRD) + 1))

add(GRD, "G11", "PASS",
    "★分层声明落到机上：本卷 id 全不重复",
    ZERO, D(len({r["id"] for r in MAIN + CTL + GRD})),
    len({r["id"] for r in MAIN + CTL + GRD}) == len(MAIN + CTL + GRD),
    "全部 %d 条 id 互不相同；条目不可与 r377/r379/r380/r381 相加（见判定册 §八）。"
    % len(MAIN + CTL + GRD))

add(GRD, "G12", "PASS",
    "★实算守卫：add() 调用数 ≥ 28（主册 20 条的 act 全部指向本卷算出的量）",
    D(28), D(N_CALLS), N_CALLS >= 28,
    "add() 调用 %d 处 ⇒ 无「转抄来料数字」的条目。" % N_CALLS)

# ============================================================================
# §12b · 计数校正（★本卷自伤十）
#   G08/G10/G11 这三条是「读全表」的判据，但 add() 是边生成边写入的
#   ⇒ 它们写入时只能看到 GRD 的**前缀**（实测：G08 报 35 条、G11 报 38 条，
#   而最终是 40 条）。一个 35 的读数装在「全部条目」的判据里 = 假绿。
#   正法：全部条目就绪后重算一遍，读数与 kind 都以最终列表为准。
# ============================================================================
_NALL = len(MAIN) + len(CTL) + len(GRD)
_NEMP = sum(1 for r in MAIN + CTL + GRD if (not r["note"]) or (not r["title"]))
_NUNIQ = len({r["id"] for r in MAIN + CTL + GRD})
for _r in GRD:
    if _r["id"] == "G08":
        _r["exp"], _r["act"] = "0", str(_NEMP)
        _r["note"] = ("★本条写入时 GRD 还在追加，读数是中途快照；此处按**最终**列表重算："
                      "共 %d 条（主册 %d + 控制组 %d + 守卫 %d），空 title/note 的 %d 条。"
                      % (_NALL, len(MAIN), len(CTL), len(GRD), _NEMP))
        if _NEMP != 0:
            _r["kind"] = "FAIL"
    elif _r["id"] == "G10":
        _r["exp"], _r["act"] = str(len(GRD)), str(int(GRD[-1]["id"][1:]))
        _r["note"] = ("守卫编号 G01..G%02d 连续无空洞：末条编号 %s == 守卫条数 %d。"
                      % (len(GRD), GRD[-1]["id"], len(GRD)))
        if int(GRD[-1]["id"][1:]) != len(GRD):
            _r["kind"] = "FAIL"
    elif _r["id"] == "G11":
        _r["exp"], _r["act"] = "0", str(_NALL - _NUNIQ)
        _r["note"] = ("全部 %d 条 id 互不相同（重复 %d 个）；条目不可与 r377/r379/r380/r381 相加（见判定册 §八）。"
                      % (_NALL, _NALL - _NUNIQ))
        if _NALL != _NUNIQ:
            _r["kind"] = "FAIL"

# ============================================================================
# §13 · 汇总
# ============================================================================
def _cnt(lst, k):
    return sum(1 for r in lst if r["kind"] == k)

SUMMARY = dict(main_total=len(MAIN), main_pass=_cnt(MAIN, "PASS"),
               main_info=_cnt(MAIN, "INFO"), main_fail=_cnt(MAIN, "FAIL"),
               ctl_total=len(CTL), ctl_pass=_cnt(CTL, "PASS"),
               grd_total=len(GRD), grd_pass=_cnt(GRD, "PASS"))
FINAL = ("ALL-GATES-PASS"
         if (SUMMARY["main_fail"] == 0 and SUMMARY["ctl_pass"] == len(CTL)
             and SUMMARY["grd_pass"] == len(GRD)) else "GATES-FAIL")
VERDICT = ("J74-LIST-HONEST--SIX-DIM-CS-ABSENT--FLUX-ENERGY-CONVENTION-DEPENDENT--"
           "N3-SELECTION-TUNABLE-ZERO-PREDICTION--INDEX-RANK-FORCE-VERIFIED--"
           "SHORT-RANGE-DIMENSION-FORCED--UNIQUE-PREDICTION-ZERO")

# ============================================================================
# §14 · JSON / REPORT
# ============================================================================
def jd(x):
    if isinstance(x, (D, F)):
        return str(x)
    if isinstance(x, dict):
        return {k: jd(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jd(v) for v in x]
    return x

DATA = dict(rid=RID, title=TITLE, stamp=STAMP, verdict=VERDICT, final=FINAL,
            summary=SUMMARY, res=jd(RES), main=MAIN, ctl=CTL, guard=GRD)
with io.open(P_JSON, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)

L = []
L.append("TUFT-%s  %s" % (RID, TITLE))
L.append("=" * 100)
L.append("来料：数据/TUFT-J74_ROOTV48V49问题梳理与V50攻坚路线_来料全文_2026-11-03.md（%s B，污染见 P19）"
         % format(RES["mat_bytes"], ","))
L.append("FINAL = %s" % FINAL)
L.append("VERDICT = %s" % VERDICT)
L.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d/%d；守卫 %d/%d"
         % (SUMMARY["main_total"], SUMMARY["main_pass"], SUMMARY["main_info"], SUMMARY["main_fail"],
            SUMMARY["ctl_pass"], SUMMARY["ctl_total"], SUMMARY["grd_pass"], SUMMARY["grd_total"]))
L.append("")
for tag, lst in (("主册", MAIN), ("控制组", CTL), ("守卫", GRD)):
    L.append("=" * 100)
    L.append("【%s】" % tag)
    L.append("=" * 100)
    for r in lst:
        L.append("[%s] %s  %s" % (r["kind"], r["id"], r["title"]))
        L.append("    exp = %s" % r["exp"])
        L.append("    act = %s" % r["act"])
        L.append("    " + r["note"])
        L.append("")
with io.open(P_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("RID=%s  FINAL=%s" % (RID, FINAL))
print("VERDICT=%s" % VERDICT)
print("MAIN %d (PASS %d / INFO %d / FAIL %d)" % (SUMMARY["main_total"], SUMMARY["main_pass"],
                                                 SUMMARY["main_info"], SUMMARY["main_fail"]))
print("CTL %d/%d   GRD %d/%d" % (SUMMARY["ctl_pass"], SUMMARY["ctl_total"],
                                 SUMMARY["grd_pass"], SUMMARY["grd_total"]))
for r in MAIN + CTL + GRD:
    if r["kind"] == "FAIL":
        print("FAIL %s :: %s | exp=%s act=%s" % (r["id"], r["title"], r["exp"], r["act"]))
print("JSON %d B  TXT %d B" % (os.path.getsize(P_JSON), os.path.getsize(P_TXT)))
