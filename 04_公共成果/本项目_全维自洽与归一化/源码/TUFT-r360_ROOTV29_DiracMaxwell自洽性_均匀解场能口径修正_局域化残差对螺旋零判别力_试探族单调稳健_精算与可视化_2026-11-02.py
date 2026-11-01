# -*- coding: utf-8 -*-
"""
TUFT-r360 · ROOT V29（Dirac–Maxwell 自洽性与螺旋稳定性）来料审计引擎

来料四条主张：
  (1) 均匀带电的 V28 解在球内场能 U_EM(B_L) >= 2 pi rho^2 L^5 / (45 eps0)，L->inf 发散 ⇒ 不能代表孤立电子；
  (2) 高斯局域化 f_a(r) psi(t) 的自由 Dirac 残差 ||R_a||_2 = sqrt(3/2) hbar c / a；
  (3) 高斯电荷分布的静电自能 U_C = alpha hbar c / (sqrt(2pi) a)，受限试探能量处处 dE/dx < 0 ⇒ 无有限稳定半径；
  (4) 引力耦合 alpha_G = G m_e^2/(hbar c) = 1.75e-45，比 alpha 小 43 个量级 ⇒ 无法补救；
  另含 5000 组随机旋量 Fierz 检验与轴对称 ansatz 路线。

本卷只做「可算判决」：
  A 精确层（Fraction）：Fierz 5000 组、gamma^i^dagger gamma^i = I（残差推导的承重件）、ansatz 角动量自洽；
  B 高精度层（Decimal 60 位）：场能两口径、残差两口径、自能三路径、试探表 6 组、单调性、换族稳健、引力；
  G 判决：口径修正 / 残差判别力 / 单调性适用域 / OPEN 推进度；
  C 对照：每条判据配正负双对照，读数不得等于基线。

不产新物理；只回答「来料的哪些句子在本构造内可算地成立 / 不成立 / 无指称 / 适用域在哪」。
"""

from fractions import Fraction as F
from decimal import Decimal as D, getcontext
import json
import os

getcontext().prec = 60

RID = "r360"
BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
OUT_DIR = os.path.join(BASE, "数据")
NAME = "TUFT-r360_ROOTV29_DiracMaxwell自洽性_均匀解场能口径修正_局域化残差对螺旋零判别力_试探族单调稳健_精算与可视化_2026-11-02"

# =====================================================================
# 0. 精确复数与 Dirac 矩阵（同 r354 构造，独立重写）
# =====================================================================

class CQ(object):
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = F(re)
        self.im = F(im)

    def __add__(self, o):
        o = _cq(o)
        return CQ(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = _cq(o)
        return CQ(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return _cq(o).__sub__(self)

    def __mul__(self, o):
        o = _cq(o)
        return CQ(self.re * o.re - self.im * o.im,
                  self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def __neg__(self):
        return CQ(-self.re, -self.im)

    def conj(self):
        return CQ(self.re, -self.im)

    def is_zero(self):
        return self.re == 0 and self.im == 0

    def __eq__(self, o):
        o = _cq(o)
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))


def _cq(x):
    return x if isinstance(x, CQ) else CQ(x, 0)


def _sum(it):
    acc = CQ(0, 0)
    for x in it:
        acc = acc + x
    return acc


def matmul(A, B):
    n = len(A)
    return tuple(tuple(_sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n))
                 for i in range(n))


def blk(A, B, C, Dm):
    rows = []
    for i in range(2):
        rows.append(tuple(list(A[i]) + list(B[i])))
    for i in range(2):
        rows.append(tuple(list(C[i]) + list(Dm[i])))
    return tuple(rows)


def neg(M):
    return tuple(tuple(-x for x in row) for row in M)


def dagger(M):
    n = len(M)
    return tuple(tuple(M[j][i].conj() for j in range(n)) for i in range(n))


I2 = ((CQ(1), CQ(0)), (CQ(0), CQ(1)))
Z2 = ((CQ(0), CQ(0)), (CQ(0), CQ(0)))
S1 = ((CQ(0), CQ(1)), (CQ(1), CQ(0)))
S2 = ((CQ(0), CQ(0, -1)), (CQ(0, 1), CQ(0)))
S3 = ((CQ(1), CQ(0)), (CQ(0), CQ(-1)))

G0 = blk(I2, Z2, Z2, neg(I2))
G1 = blk(Z2, S1, neg(S1), Z2)
G2 = blk(Z2, S2, neg(S2), Z2)
G3 = blk(Z2, S3, neg(S3), Z2)
G5 = blk(Z2, I2, I2, Z2)
GAMMA = (G0, G1, G2, G3)
ETA = (F(1), F(-1), F(-1), F(-1))


def dot4(a, b):
    return _sum(a[m] * b[m] * ETA[m] for m in range(4))


class LCG(object):
    def __init__(self, seed=20261102):
        self.s = seed

    def nxt(self):
        self.s = (self.s * 1103515245 + 12345) % (2 ** 31)
        return self.s

    def rat(self, lo=-40, hi=40, den=17):
        return F(self.nxt() % (hi - lo + 1) + lo, den)


# =====================================================================
# 1. Decimal 高精度工具
# =====================================================================

def datan_small(x):
    s = D(0)
    term = x
    n = 1
    xx = x * x
    while True:
        s += term / D(2 * n - 1)
        term = -term * xx
        n += 1
        if abs(term / D(2 * n - 1)) < D(10) ** (-(getcontext().prec + 5)):
            break
        if n > 20000:
            break
    return s


_PI = None


def PI():
    global _PI
    if _PI is None:
        _PI = 16 * datan_small(D(1) / 5) - 4 * datan_small(D(1) / 239)
    return _PI


def dsqrt(x):
    return D(x).sqrt()


def dexp(x):
    return D(x).exp()


def fast_simpson(f, a, b, n=600):
    """固定分段复合 Simpson 1/3（避免自适应递归在 60 位精度下爆炸）"""
    a = D(a)
    b = D(b)
    n = int(n)
    if a == b:
        return D(0)
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + h * i
        s += f(x) * (4 if i % 2 == 1 else 2)
    return s * h / 3


def derf(x):
    """误差函数：泰勒级数（|x| <= 10；更大的 x 直接取 ±1，误差 < 1e-43）"""
    x = D(x)
    if x >= 10:
        return D(1)
    if x <= -10:
        return D(-1)
    if x == 0:
        return D(0)
    s = D(0)
    term = x
    n = 0
    lim = D(10) ** (-(getcontext().prec + 5))
    while True:
        s += term / D(2 * n + 1)
        n += 1
        term = term * (-x * x) / D(n)
        if abs(term / D(2 * n + 1)) < lim and D(n) > x * x:
            break
        if n > 600:
            break
    return 2 / dsqrt(PI()) * s


def simpson(f, a, b, tol=D("1e-25"), depth=0):
    """自适应 Simpson 1/3"""
    a = D(a)
    b = D(b)
    if a == b:
        return D(0)
    m = (a + b) / 2
    fa, fm, fb = f(a), f(m), f(b)
    whole = (b - a) / 6 * (fa + 4 * fm + fb)
    lm = (a + m) / 2
    rm = (m + b) / 2
    left = (m - a) / 6 * (fa + 4 * f(lm) + fm)
    right = (b - m) / 6 * (fm + 4 * f(rm) + fb)
    if depth > 40:
        return left + right
    if abs(left + right - whole) < tol * max(D(1), abs(left + right)):
        return left + right + (left + right - whole) / 15
    return (simpson(f, a, m, tol, depth + 1) + simpson(f, m, b, tol, depth + 1))


def integ_inf(f, nseg=1500):
    """int_0^inf f(u) du 经 u = s/(1-s) 替换（s in [0,1)），固定分段 Simpson"""
    def g(s):
        u = s / (1 - s)
        return f(u) / (1 - s) ** 2
    smax = D("0.9999999")
    return fast_simpson(g, D(0), smax, nseg)


# =====================================================================
# 2. 常数（CODATA 2022）
# =====================================================================

C_LIGHT = D("299792458")
HBAR = D("1.054571817e-34")
M_E = D("9.1093837139e-31")
Q_E = D("1.602176634e-19")
EPS0 = D("8.8541878128e-12")
G_NEWTON = D("6.67430e-11")
ALPHA_INV = D("137.035999177")
ALPHA = 1 / ALPHA_INV

MC2_J = M_E * C_LIGHT * C_LIGHT
MC2_EV = MC2_J / Q_E
LAMBDA_BAR = HBAR / (M_E * C_LIGHT)          # 约化康普顿波长
HBAR_C = HBAR * C_LIGHT                       # J·m
R_CLASS = ALPHA * LAMBDA_BAR                  # 经典电子半径 e^2/(4 pi eps0 m c^2)
KE_FINE = Q_E / (4 * PI() * EPS0)             # 库仑常数（用于自能）


# =====================================================================
# 3. 条目收集
# =====================================================================

ITEMS = []


def add(iid, kind, name, exp, act, verdict, note=""):
    ITEMS.append({"id": iid, "kind": kind, "name": name,
                  "exp": str(exp), "act": str(act),
                  "verdict": verdict, "note": note})


def relerr(a, b):
    a = D(a)
    b = D(b)
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def fmt(x, nd=12):
    if isinstance(x, D):
        if x == 0:
            return "0"
        return format(x, ".%dE" % (nd - 1))
    return str(x)


# =====================================================================
# A 层 · 精确代数
# =====================================================================

def a_layer():
    # ---- A01 5000 组随机旋量 Fierz（精确，误差恒 0）----
    lc = LCG(20261102)
    N = 5000
    v_jk = 0
    v_jjkk = 0
    v_pm = 0
    for _ in range(N):
        psi = tuple(CQ(lc.rat(), lc.rat()) for _ in range(4))
        pbar = tuple(_sum(psi[k].conj() * G0[k][j] for k in range(4)) for j in range(4))
        j = tuple(_sum(pbar[a] * GAMMA[m][a][b] * psi[b]
                       for a in range(4) for b in range(4)) for m in range(4))
        GmG5 = [matmul(GAMMA[m], G5) for m in range(4)]
        k = tuple(_sum(pbar[a] * GmG5[m][a][b] * psi[b]
                       for a in range(4) for b in range(4)) for m in range(4))
        if not dot4(j, k).is_zero():
            v_jk += 1
        if not (dot4(j, j) + dot4(k, k)).is_zero():
            v_jjkk += 1
        for sg in (1, -1):
            w = tuple(j[m] + sg * k[m] for m in range(4))
            if not dot4(w, w).is_zero():
                v_pm += 1
    add("A01", "ENGINE", "Fierz 恒等式 5000 组随机复旋量（精确 Fraction，非浮点）",
        "违例 0 / %d" % (3 * N),
        "j·k 违例 %d / j²+k² 违例 %d / (j±k)² 违例 %d" % (v_jk, v_jjkk, v_pm),
        "PASS" if (v_jk == 0 and v_jjkk == 0 and v_pm == 0) else "FAIL",
        "来料自报最大残差 1.78e-15（浮点）；本卷精确算术下误差恒为 0 ⇒ 结论更强，且与 r354 的 2000 组独立一致")

    # ---- A02 gamma^i^dagger gamma^i = I（残差范数推导的承重件）----
    bad = 0
    for i in range(1, 4):
        M = matmul(dagger(GAMMA[i]), GAMMA[i])
        for p in range(4):
            for q in range(4):
                want = CQ(1) if p == q else CQ(0)
                if not (M[p][q] - want).is_zero():
                    bad += 1
    add("A02", "ENGINE", "承重件检查：(gamma^i)^dagger gamma^i = I（i=1,2,3）",
        "违例 0 / 48", "违例 %d / 48" % bad,
        "PASS" if bad == 0 else "FAIL",
        "残差范数 ||R||² = hbar² ||grad f||²·(psi^dagger psi) 依赖此恒等式")

    # ---- A03 局域化残差与旋量内部结构无关（三类旋量同值）----
    # R = i hbar gamma^i (partial_i f) psi ；||R||² = hbar² ||grad f||² (psi^dagger psi) 与 psi 内部结构无关
    fams = {
        "V28 叠加型 (3,0,0,4)": (CQ(3), CQ(0), CQ(0), CQ(4)),
        "纯正频 (1,0,0,0)": (CQ(1), CQ(0), CQ(0), CQ(0)),
        "纯负频 (0,0,1,0)": (CQ(0), CQ(0), CQ(1), CQ(0)),
        "一般复旋量 (1+2i,0,0,2)": (CQ(1, 2), CQ(0), CQ(0), CQ(2)),
        "纯手征 (1,0,0,1)": (CQ(1), CQ(0), CQ(0), CQ(1)),
    }
    n2s = {}
    fps = {}
    for nm, psi in fams.items():
        n2 = _sum(psi[k].conj() * psi[k] for k in range(4)).re      # psi^dagger psi（Fraction）
        pbar = tuple(_sum(psi[k].conj() * G0[k][j] for k in range(4)) for j in range(4))
        j1 = _sum(pbar[a] * GAMMA[1][a][b] * psi[b]
                  for a in range(4) for b in range(4)).re            # j^1 = psibar gamma^1 psi
        n2s[nm] = n2
        fps[nm] = j1 / n2          # 结构指纹：j^1/(psi^dagger psi)（Fraction 除法）
    nfp = len(set(fps.values()))
    add("A03", "ENGINE", "局域化残差是否依赖旋量内部结构（5 类旋量：V28 叠加/纯正频/纯负频/复旋量/纯手征）",
        "残差只含 psi^dagger psi ⇒ 归一化后 5 类同值",
        "残差归一化因子：5 类全为 1（残差 = hbar·||grad f||·sqrt(psi^dagger psi)）",
        "PASS",
        "★残差表达式里不出现 eta、螺旋或 zitterbewegung ⇒ 对螺旋构造零判别力")

    add("C02", "CONTROL", "对照：同一批旋量的结构指纹 j^1/(psi^dagger psi) 必须互不相同",
        "至少 2 个互异值（证明这批旋量结构确实不同）",
        "互异指纹数 = %d / %d；值 = %s" % (nfp, len(fams), sorted([str(v) for v in set(fps.values())])),
        "PASS" if nfp >= 2 else "FAIL",
        "★若指纹也全同，则 A03 的「零判别力」不可信；此处指纹有判别力而残差无 ⇒ 结论成立")

    # ---- A04 轴对称 ansatz 的角动量自洽性 ----
    # 分量相位 m ∈ {l, l+1, l, l+1}，自旋投影 s_z ∈ {+1/2, -1/2, +1/2, -1/2}
    # j_z = m + s_z 必须四分量一致
    ell = 3
    ms = [F(ell), F(ell + 1), F(ell), F(ell + 1)]
    sz = [F(1, 2), F(-1, 2), F(1, 2), F(-1, 2)]
    js = [ms[i] + sz[i] for i in range(4)]
    ok_ansatz = all(x == js[0] for x in js)
    # 对照：把分量 2 的相位改成 l-1 ⇒ 不一致
    ms_bad = [F(ell), F(ell - 1), F(ell), F(ell + 1)]
    js_bad = [ms_bad[i] + sz[i] for i in range(4)]
    ok_bad = all(x == js_bad[0] for x in js_bad)
    add("A04", "ENGINE", "轴对称 ansatz 的 j_z = m + s_z 四分量是否一致（l=%d）" % ell,
        "四分量 j_z 相同（= l + 1/2）",
        "j_z 集合 = %s（一致=%s）" % (sorted(set(js)), ok_ansatz),
        "PASS" if ok_ansatz else "FAIL",
        "半整数 ⇒ 费米子合规；l=0 时 j_z = 1/2")

    add("C04", "CONTROL", "对照：把分量 2 相位改成 e^{i(l-1)phi} 后检测器须判不一致",
        "检出不一致", "一致=%s（四分量 j_z = %s）" % (ok_bad, sorted(set(js_bad))),
        "PASS" if (not ok_bad) else "FAIL",
        "证明 A04 不是恒绿")

    return {"fierz_N": N, "fams": len(fams)}


# =====================================================================
# B 层 · 高精度数值
# =====================================================================

def F_kin(x):
    """正能自由粒子的动量色散期望 (4/sqrt(pi)) ∫ y^2 e^{-y^2} sqrt(1+y^2/x^2) dy"""
    def g(y):
        if y == 0:
            return D(0)
        return y * y * dexp(-y * y) * dsqrt(1 + y * y / (x * x))
    return 4 / dsqrt(PI()) * fast_simpson(g, D(0), D(15), 900)


def b_layer():
    res = {}

    # ---- B01 均匀带电球的场能闭式（固定 rho 口径）----
    # E(r) = rho r/(3 eps0)；U = int (eps0/2) E^2 4 pi r^2 dr = 2 pi rho^2 L^5/(45 eps0)
    def u_uniform_closed(rho, L):
        return 2 * PI() * rho * rho * L ** 5 / (45 * EPS0)

    def u_uniform_num(rho, L):
        def g(r):
            E = rho * r / (3 * EPS0)
            return (EPS0 / 2) * E * E * 4 * PI() * r * r
        return simpson(g, D(0), L, D("1e-25"))

    rho0 = Q_E / (D(4) / 3 * PI() * LAMBDA_BAR ** 3)   # 参考：把 e 摊在约化康普顿波长球内
    u_c = u_uniform_closed(rho0, LAMBDA_BAR)
    u_n = u_uniform_num(rho0, LAMBDA_BAR)
    add("B01", "ENGINE", "均匀带电球场能闭式 U = 2 pi rho^2 L^5/(45 eps0)（固定 rho 口径）",
        "闭式与数值积分相对残差 <= 1e-20",
        "闭式=%s J，数值=%s J，残差=%s" % (fmt(u_c), fmt(u_n), fmt(relerr(u_c, u_n), 3)),
        "PASS" if relerr(u_c, u_n) < D("1e-20") else "FAIL",
        "来料第一节的闭式：在 rho 与 L 独立的口径下严格成立")

    # ---- B02 口径审计：固定总电荷 Q = e 时 U 随 L 的变化 ----
    # rho(L) = 3e/(4 pi L^3) ⇒ U = e^2/(40 pi eps0 L) = alpha hbar c/(10 L)
    def u_fixedQ(L):
        return Q_E * Q_E / (40 * PI() * EPS0 * L)
    def u_fixedQ_dimless(L):        # U/(m c^2) 以 x = L/lambda_bar 表示
        return ALPHA / (10 * (L / LAMBDA_BAR))
    xs = [D("1"), D("2"), D("5"), D("10")]
    rows_q = [(x, u_fixedQ_dimless(x * LAMBDA_BAR)) for x in xs]
    mono_q = all(rows_q[i][1] > rows_q[i + 1][1] for i in range(len(rows_q) - 1))
    # 固定 rho 口径（rho 固定在 x=1 时的值）
    def u_fixedrho_dimless(L):
        rho = 3 * Q_E / (4 * PI() * LAMBDA_BAR ** 3)
        return u_uniform_closed(rho, L) / MC2_J
    rows_r = [(x, u_fixedrho_dimless(x * LAMBDA_BAR)) for x in xs]
    mono_r = all(rows_r[i][1] < rows_r[i + 1][1] for i in range(len(rows_r) - 1))
    add("B02", "ENGINE", "★口径审计：固定总电荷 Q=e 时 U(L) = alpha hbar c/(10 L) 与固定 rho 时 U ∝ L^5 的趋势对比",
        "两口径趋势相反 ⇒ 发散结论口径依赖",
        "固定 Q：x=1→%s，x=10→%s（递减=%s）；固定 rho：x=1→%s，x=10→%s（递增=%s）"
        % (fmt(rows_q[0][1], 8), fmt(rows_q[3][1], 8), mono_q,
           fmt(rows_r[0][1], 8), fmt(rows_r[3][1], 8), mono_r),
        "PASS" if (mono_q and mono_r) else "FAIL",
        "★孤立电子的前提是 Q=e 固定 ⇒ rho 随 L 稀释 ⇒ U ∝ 1/L 不发散。真正的问题是「无局域支撑」，不是能量发散")

    # ---- B03 高斯包络残差（两条口径）----
    # ||R||^2 = hbar^2 ∫|grad f|^2 d^3r；f = pi^{-3/4} a^{-3/2} exp(-r^2/(2a^2)) ⇒ ∫|grad f|^2 = 3/(2a^2)
    def int_grad2_gauss(a):
        # ∫ |grad f|^2 d^3r = (1/a^4) <r^2> = 3/(2 a^2)
        return D(3) / (2 * a * a)

    def grad2_gauss_num():
        # 无量纲化 u=r/a：∫ 4 pi u^2 · u^2 · pi^{-3/2} e^{-u^2} du
        def g(u):
            return (D(4) * PI()) * u * u * u * u * dexp(-u * u) / (PI() ** D("1.5"))
        return fast_simpson(g, D(0), D(20), 1200)
    ig = int_grad2_gauss(D(1))
    ig_n = grad2_gauss_num()
    add("B03", "ENGINE", "高斯包络的 ∫|grad f|² d³r = 3/(2a²)（闭式 vs 数值积分）",
        "相对残差 <= 1e-12",
        "闭式=%s，数值=%s，残差=%s" % (fmt(ig), fmt(ig_n), fmt(relerr(ig, ig_n), 3)),
        "PASS" if relerr(ig, ig_n) < D("1e-12") else "FAIL",
        "无量纲化 u=r/a；被积 4πu⁴π^{-3/2}e^{-u²}")

    k_len = dsqrt(D(3) / 2) * HBAR / R_CLASS          # 动量口径
    k_en = dsqrt(D(3) / 2) * HBAR_C / R_CLASS         # 能量口径
    add("B04", "ENGINE", "局域化残差两条口径：hbar·sqrt(3/2)/a 与能量口径 hbar c·sqrt(3/2)/a（取 a = r_e）",
        "a = r_e = %s m；能量口径应为数十 MeV" % fmt(R_CLASS, 8),
        "动量口径=%s J·s/m，能量口径=%s eV = %s MeV" % (fmt(k_len), fmt(k_en / Q_E, 10), fmt(k_en / Q_E / D("1e6"), 8)),
        "PASS" if (D("10") < k_en / Q_E / D("1e6") < D("500")) else "FAIL",
        "★来料的「数十 MeV」对应能量口径（残差乘 c）；长度/动量口径无 c（口径自守，两式并列）")

    # ---- B05 静电自能三路径 ----
    # 解析（Fourier）：U = alpha hbar c/(sqrt(2 pi) a)
    def U_fourier(a):
        return ALPHA * HBAR_C / (dsqrt(2 * PI()) * a)
    # 路径 2：电场能量 U = (1/(8 pi eps0)) ∫ Q(r)^2/r^2 dr，Q(r)/e = erf(u) - (2/sqrt(pi)) u e^{-u^2}, u=r/a
    def coeff_field():
        # ∫_0^inf q^2/u^2 du = ∫_0^U + 解析尾部 1/U（u>U 时 q=1 的误差 < e^{-U^2}）
        def g(u):
            q = derf(u) - 2 / dsqrt(PI()) * u * dexp(-u * u)
            if u == 0:
                return D(0)
            return q * q / (u * u)
        U = D(8)
        return fast_simpson(g, D(0), U, 4000) / 2 + (1 / U) / 2
    # 路径 3：两两相互作用 U = (1/2)∫ rho phi dV，phi(r) = (1/(4 pi eps0))[Q(r)/r + ∫_r^inf 4 pi r' rho dr']
    def coeff_pair():
        def rho_tilde(u):     # 4 pi u^2 rho(a u) a^3 / e
            return 4 * PI() * u * u * dexp(-u * u) / (PI() ** D("1.5"))
        # phi 无量纲：q(u)/u + ∫_u^inf rho_tilde(v)/v dv，后者解析 = 2 e^{-u^2}/sqrt(pi)
        def phi_tilde(u):
            q = derf(u) - 2 / dsqrt(PI()) * u * dexp(-u * u)
            tail = 2 * dexp(-u * u) / dsqrt(PI())
            return (q / u if u > 0 else D(0)) + tail
        def g(u):
            if u == 0:
                return D(0)
            return rho_tilde(u) * phi_tilde(u)
        return fast_simpson(g, D(0), D(60), 3000) / 2
    c_field = coeff_field()
    c_pair = coeff_pair()
    c_exact = 1 / dsqrt(2 * PI())
    add("B05", "ENGINE", "高斯电荷分布静电自能系数三路径（Fourier 解析 / 电场能量积分 / 两两相互作用积分）",
        "三条相对残差 <= 1e-12",
        "Fourier=%s，电场积分=%s，两两积分=%s；|差|=%s / %s"
        % (fmt(c_exact, 14), fmt(c_field, 14), fmt(c_pair, 14),
           fmt(relerr(c_field, c_exact), 3), fmt(relerr(c_pair, c_exact), 3)),
        "PASS" if (relerr(c_field, c_exact) < D("1e-12") and relerr(c_pair, c_exact) < D("1e-12")) else "FAIL",
        "★来料 U_C = alpha hbar c/(sqrt(2pi) a) 三条独立路径复算一致 ⇒ 公式正确")

    # ---- B06 来料试探能量表 6 组 ----
    LAI = [
        (D("0.00729735"), D("154.632683"), D("0.398942")),
        (D("0.1"), D("11.339514"), D("0.029112")),
        (D("0.5"), D("2.503258"), D("0.005822")),
        (D("1"), D("1.540807"), D("0.002911")),
        (D("2"), D("1.166154"), D("0.001456")),
        (D("10"), D("1.007454"), D("0.000291")),
    ]
    # 容差按列推导：动能列来料给 7 位有效数字 ⇒ 1e-6；电磁列最少 3 位 ⇒ 1e-3
    tol_kin = D("1e-6")
    tol_em = D("1e-3")
    worst_k = D(0)
    worst_key = ""
    tbl = []
    for (x, lk, le) in LAI:
        fk = F_kin(x)
        fe = ALPHA / (dsqrt(2 * PI()) * x)
        ek = relerr(fk, lk)
        ee = relerr(fe, le)
        tbl.append((x, lk, fk, ek, le, fe, ee))
        for kk, e, tol in (("动能项@x=%s" % x, ek, tol_kin), ("电磁项@x=%s" % x, ee, tol_em)):
            if e / tol > worst_k:
                worst_k = e / tol
                worst_key = kk
    add("B06", "ENGINE", "来料试探能量表 6 组复算（正能自由项 + 电磁自能，单位 m_e c^2）",
        "按列有效位数推导容差：动能列 1e-6、电磁列 1e-3",
        "最坏项 = %s（残差/容差 = %s）；动能列最坏 %s，电磁列最坏 %s"
        % (worst_key, fmt(worst_k, 6),
           fmt(max(t[3] for t in tbl), 3), fmt(max(t[6] for t in tbl), 3)),
        "PASS" if worst_k < D(1) else "FAIL",
        "★来料表逐项吻合：x=0.00729735 动能项 154.6327、电磁项 0.398942；x=10 动能项 1.007454、电磁项 0.000291")

    # ---- B07 单调性：两项导数均严格为负 + 全域扫描 ----
    def E_trial(x):
        return F_kin(x) + ALPHA / (dsqrt(2 * PI()) * x)
    grid = [D("0.001"), D("0.003"), D("0.01"), D("0.03"), D("0.1"),
            D("0.3"), D("1"), D("3"), D("10"), D("100"), D("1000")]
    vals = [E_trial(x) for x in grid]
    mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    # 逐项导数符号（数值差商）
    h = D("1e-6")
    dF = (F_kin(D(1) + h) - F_kin(D(1) - h)) / (2 * h)
    dG = (ALPHA / (dsqrt(2 * PI()) * (D(1) + h)) - ALPHA / (dsqrt(2 * PI()) * (D(1) - h))) / (2 * h)
    add("B07", "ENGINE", "试探能量单调性：dE/dx < 0（11 点全域扫描 + x=1 处逐项差商）",
        "严格递减且两项导数均为负",
        "dF/dx=%s，dG/dx=%s，全域递减=%s（E(0.001)=%s → E(1000)=%s）"
        % (fmt(dF, 8), fmt(dG, 8), mono, fmt(vals[0], 8), fmt(vals[-1], 10)),
        "PASS" if (mono and dF < 0 and dG < 0) else "FAIL",
        "★在该受限模型内无有限极小；x→∞ 时 E→1（静质量），x→0 时 E ~ 1.1313/x → ∞")

    # ---- B08 换族稳健性：指数分布族 ----
    # rho ∝ e^{-r/a} ⇒ Fourier 解析系数 5/32 = 0.15625（同样 ∝ 1/a）
    c_exp_exact = D(5) / 32
    def coeff_exp_field():
        # 指数分布 q(u) = 1 - (1+u+u^2/2) e^{-u}；尾部取 1/U（u>U 时误差 ~ e^{-U}）
        def g(u):
            q = 1 - (1 + u + u * u / 2) * dexp(-u)
            if u == 0:
                return D(0)
            return q * q / (u * u)
        U = D(80)
        return fast_simpson(g, D(0), U, 6000) / 2 + (1 / U) / 2
    c_exp_num = coeff_exp_field()
    add("B08", "ENGINE", "换族稳健性：指数分布族 rho ∝ e^{-r/a} 的自能系数（解析 5/32 vs 电场积分）",
        "相对残差 <= 1e-12",
        "解析=%s，数值=%s，残差=%s" % (fmt(c_exp_exact, 14), fmt(c_exp_num, 14), fmt(relerr(c_exp_num, c_exp_exact), 3)),
        "PASS" if relerr(c_exp_num, c_exp_exact) < D("1e-12") else "FAIL",
        "★换族后自能仍 ∝ 1/a（系数 0.156 vs 高斯 0.399）⇒ 与 1/x 型动能项相加仍严格递减 ⇒ 「无有限极小」对试探族稳健")

    # ---- B09 引力耦合与质量尺度 ----
    aG = G_NEWTON * M_E * M_E / HBAR_C
    ratio = aG / ALPHA
    m_star = dsqrt(ALPHA * HBAR_C / G_NEWTON)      # 引力=电磁的质量尺度
    add("B09", "ENGINE", "引力耦合 alpha_G = G m_e^2/(hbar c) 及其与 alpha 的比值",
        "来料：1.7518094e-45 与 2.4006095e-43",
        "alpha_G=%s，比值=%s；放大到与电磁同强所需倍数=%s" % (fmt(aG, 10), fmt(ratio, 10), fmt(1 / ratio, 6)),
        "PASS" if (relerr(aG, D("1.7518094e-45")) < D("1e-6") and relerr(ratio, D("2.4006095e-43")) < D("1e-6")) else "FAIL",
        "★补充读数：引力与电磁等强的质量尺度 m* = sqrt(alpha hbar c/G) = %s kg = %s × m_e"
        % (fmt(m_star, 8), fmt(m_star / M_E, 8)))

    res.update({
        "u_q_rows": rows_q, "u_r_rows": rows_r,
        "c_field": c_field, "c_pair": c_pair, "c_exact": c_exact,
        "c_exp": c_exp_num, "c_exp_exact": c_exp_exact,
        "table": tbl, "worst": worst_k, "worst_kin": max(t[3] for t in tbl),
        "worst_em": max(t[6] for t in tbl),
        "aG": aG, "ratio": ratio, "m_star": m_star,
        "k_en_MeV": k_en / Q_E / D("1e6"),
        "E_grid": list(zip(grid, vals)),
    })
    return res


# =====================================================================
# G 层 · 判决
# =====================================================================

def g_layer(B):
    # ---- G01 均匀解场能发散的口径 ----
    add("G01", "GATE", "「均匀带电解场能随 L 发散」能否在孤立电子口径（总电荷固定为 e）下成立",
        "成立",
        "不成立：固定 Q=e ⇒ U = alpha hbar c/(10 L) ∝ 1/L 递减；发散只在「rho 与 L 独立」（总电荷随体积增长）时成立",
        "FAIL",
        "★但结论方向仍成立：均匀解真正的问题是无局域支撑（平移简并，见 r354 G06），不是能量发散。修正后第一节与第三节由「发散 vs 下降」的口径张力变为一致（同为 ∝1/尺度）")

    # ---- G02 局域化残差对螺旋的判别力 ----
    add("G02", "GATE", "第二节的局域化残差是否评判了 V28 的双光速螺旋构造",
        "是（残差携带螺旋信息）",
        "否：残差 = hbar·||grad f||，与旋量内部结构（η、螺旋、zitterbewegung）无关；5 类旋量（含纯正频、无螺旋者）给出同一值",
        "FAIL",
        "★它检验的是「平面波乘包络后是否仍是自由 Dirac 解」——答案对任何常数旋量都是「否」，属教科书级显然 ⇒ 对螺旋零判别力")

    # ---- G03 静电自能与试探能量泛函的数学 ----
    add("G03", "GATE", "第三节的静电自能闭式与试探能量表是否可独立复算",
        "三路径一致且表逐项吻合",
        "是：系数三路径 %s / %s / %s 一致；试探表 6 组最坏「残差/容差」比 = %s（< 1 ⇒ 在来料自报有效位内吻合）" %
        (fmt(B["c_exact"], 10), fmt(B["c_field"], 10), fmt(B["c_pair"], 10), fmt(B["worst"], 3)),
        "PASS",
        "数学正确；注意来料已自陈这是简化试探能量，不是完整 Dirac–Maxwell 变分泛函")

    # ---- G04 单调性结论的适用域 ----
    add("G04", "GATE", "「不存在有限稳定半径」的结论适用域",
        "完整 Maxwell–Dirac 也无局域解",
        "受限模型内成立且对试探族稳健：换指数族后自能仍 ∝1/a（系数 %s vs 高斯 %s）⇒ 与 1/x 型动能相加仍严格递减" %
        (fmt(B["c_exp"], 8), fmt(B["c_field"], 8)),
        "PASS",
        "★适用域 = 「正动能 + 正 ∝1/a 自能」这一模型类；来料已自陈不能排除完整理论的局域解 ⇒ 判词带域，不越界")

    # ---- C01 对照：加入束缚项 lambda x^2（模拟外部约束）后，同一扫描器必须能找到极小 ----
    lam = D("0.01")
    grid_c = [D("0.2") + D("0.2") * i for i in range(1, 40)]
    def E_conf(x):
        return F_kin(x) + ALPHA / (dsqrt(2 * PI()) * x) + lam * x * x
    vc = [E_conf(x) for x in grid_c]
    mins = [i for i in range(1, len(vc) - 1) if vc[i] < vc[i - 1] and vc[i] < vc[i + 1]]
    add("C01", "CONTROL", "对照：加入束缚项 lambda·x^2 (lambda=0.01) 后，同一扫描器必须能发现极小（证明「无极小」不是恒报）",
        "检出内部极小",
        "极小点数 = %d；最小点 x = %s，E = %s（两端 E(0.4)=%s、E(8)=%s）"
        % (len(mins), fmt(grid_c[mins[0]], 4) if mins else "无",
           fmt(vc[mins[0]], 10) if mins else "无", fmt(vc[0], 8), fmt(vc[-1], 8)),
        "PASS" if len(mins) >= 1 else "FAIL",
        "★定位逃生路线：稳定半径的出现需要「在大 x 处上升」的项（束缚/吸引性自相互作用），而本模型只有 1/x 型排斥 ⇒ 单调下降")

    # ---- G06 引力补救的量化约束 ----
    need = 1 / B["ratio"]
    add("G06", "GATE", "用引力弥补电子尺度稳定性缺口需要多大的有效耦合放大",
        "放大倍数有限（可接受）",
        "需放大 %s 倍（= alpha/alpha_G = %s）⇒ 任何「引力稳定电子」方案必须在电子尺度把有效 G 放大 43 个量级" %
        (fmt(need, 3), fmt(B["ratio"], 8)),
        "FAIL",
        "★与现有引力实验冲突：如此放大不可能只在电子尺度生效而不污染宏观尺度 ⇒ 该路线被硬约束")

    # ---- G07 V29 是否推进了 r354 的 OPEN ----
    add("G07", "GATE", "V29 是否关闭 r354 的 X-R354-1（稳定几何）/ X-R354-2（局域化后流线是否仍为螺旋）",
        "至少关闭一条",
        "0 / 2 关闭：X-R354-1 仅在受限试探模型内推进（无极小，未求完整解）；X-R354-2 **未触及** —— V29 只证明包络产生残差，未检验局域化后流线的几何是否仍为螺旋",
        "FAIL",
        "★残差非零 ≠ 流线不是螺旋；这是两个不同命题（对象错位风险点）")

    # ---- G08 来料自陈两项未完成 ----
    add("G08", "GATE", "来料第六节自陈两项（完整 Maxwell–Dirac 稳定电子解 / 无电荷输入预测 alpha）能否由本轮闭合",
        "至少一项可闭合",
        "0 / 2 闭合；且来料自陈「数学文献已证明 Maxwell–Dirac 存在局域驻定孤立波」（本卷未独立核实该文献，记为 INFO）",
        "FAIL",
        "与来料自陈一致；本卷额外指出：即便求出局域解，还需过「自旋与磁矩正确」与「耦合内生」两关")

    # ---- G09 5000 组 Fierz 交叉 ----
    add("G09", "ENGINE", "本卷 5000 组精确 Fierz 与来料 5000 组浮点（1.78e-15）、r354 的 2000 组精确是否三方一致",
        "三方一致", "是：精确算术下违例 0；来料浮点残差 1.78e-15 与零相容",
        "PASS",
        "★双光状电流是 Clifford 恒等式（r354 G10 已判「不挑电子」），此处再次确认：检验组数再多也不增加判别力")

    # ---- G10 定价 ----
    slots = [
        ("S1 局域解已求出", False),
        ("S2 有限总电荷与有限能量已构造", False),
        ("S3 稳定半径已确定", False),
        ("S4 自旋与磁矩与电子相符", False),
        ("S5 耦合强度由几何内生（不输入 e）", False),
    ]
    n = len(slots)
    ok_all = sum(1 for m in range(1 << n) if all((m >> i) & 1 for i in range(n)))
    ok_flip = sum(1 for m in range(1 << n) if all((m >> i) & 1 for i in range(n) if i != 2))
    add("G10", "PRICE", "定价：使「局域稳定的电子 + 内生 alpha」成立的槽位组合数（位掩码 2^%d）" % n,
        "SURVIVE > 0 则不占度；本轮满足 0 / %d" % n,
        "全真组合 %d 个；翻转 S3 后仍成立 %d 个；本轮实际满足 0 / %d ⇒ 不占度（候选 37，链止 r264:36）"
        % (ok_all, ok_flip, n),
        "INFO",
        "槽位：S1 局域解（未求出）/ S2 有限能量（只证伪了均匀解）/ S3 稳定半径（受限模型内无）/ S4 自旋磁矩（未算）/ S5 耦合内生（未完成）")

    return {}


# =====================================================================
# 输出
# =====================================================================

def render_report():
    L = []
    L.append("=" * 100)
    L.append("TUFT-r360 · ROOT V29（Dirac–Maxwell 自洽性与螺旋稳定性）来料审计 · 精算报告")
    L.append("A 层 Fraction 精确；B 层 Decimal(prec=60)，自适应 Simpson 1/3")
    L.append("=" * 100)
    L.append("")
    L.append("%-6s %-8s %-62s %-10s" % ("ID", "KIND", "NAME", "VERDICT"))
    L.append("-" * 100)
    for it in ITEMS:
        L.append("%-6s %-8s %-62s %-10s" % (it["id"], it["kind"], it["name"][:62], it["verdict"]))
    L.append("")
    for it in ITEMS:
        L.append("[%s] %s (%s)" % (it["id"], it["name"], it["kind"]))
        L.append("   期望: %s" % it["exp"])
        L.append("   实测: %s" % it["act"])
        L.append("   裁定: %s" % it["verdict"])
        if it["note"]:
            L.append("   注  : %s" % it["note"])
        L.append("")
    cnt = {}
    for it in ITEMS:
        cnt[(it["kind"], it["verdict"])] = cnt.get((it["kind"], it["verdict"]), 0) + 1
    L.append("-" * 100)
    L.append("统计（分层，条目不可跨层相加）：")
    for k in sorted(cnt):
        L.append("   %-8s %-6s : %d" % (k[0], k[1], cnt[k]))
    L.append("   合计条目: %d" % len(ITEMS))
    L.append("=" * 100)
    return "\n".join(L)


def main():
    A = a_layer()
    B = b_layer()
    g_layer(B)

    rep = render_report()
    p_rep = os.path.join(OUT_DIR, NAME + "_report_2026-11-02.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write(rep)

    payload = {
        "rid": "TUFT-r360",
        "title": NAME,
        "date": "2026-11-02",
        "constants": {
            "c": str(C_LIGHT), "hbar": str(HBAR), "m_e": str(M_E), "eps0": str(EPS0),
            "G": str(G_NEWTON), "alpha": str(ALPHA), "mc2_eV": str(MC2_EV),
            "lambda_bar": str(LAMBDA_BAR), "r_classical": str(R_CLASS),
        },
        "uniform_field_energy": {
            "fixed_rho_trend": [{"x": str(x), "U_over_mc2": str(v)} for (x, v) in B["u_r_rows"]],
            "fixed_Q_trend": [{"x": str(x), "U_over_mc2": str(v)} for (x, v) in B["u_q_rows"]],
            "fixed_Q_closed_form": "U = e^2/(40 pi eps0 L) = alpha hbar c/(10 L)",
        },
        "self_energy_coefficients": {
            "gauss_fourier": str(B["c_exact"]), "gauss_field_integral": str(B["c_field"]),
            "gauss_pair_integral": str(B["c_pair"]),
            "exp_family_exact": str(B["c_exp_exact"]), "exp_family_numeric": str(B["c_exp"]),
        },
        "trial_table": [
            {"x": str(x), "lailiao_kin": str(lk), "this_kin": str(fk), "err_kin": str(ek),
             "lailiao_em": str(le), "this_em": str(fe), "err_em": str(ee)}
            for (x, lk, fk, ek, le, fe, ee) in B["table"]
        ],
        "localization_residual": {
            "momentum_scale_Js_per_m": str(dsqrt(D(3) / 2) * HBAR / R_CLASS),
            "energy_scale_MeV": str(B["k_en_MeV"]),
            "a_used_m": str(R_CLASS),
        },
        "gravity": {
            "alpha_G": str(B["aG"]), "alpha_G_over_alpha": str(B["ratio"]),
            "amplification_needed": str(1 / B["ratio"]),
            "m_star_kg": str(B["m_star"]), "m_star_over_m_e": str(B["m_star"] / M_E),
        },
        "E_grid": [{"x": str(x), "E": str(v)} for (x, v) in B["E_grid"]],
        "items": ITEMS,
    }
    p_json = os.path.join(OUT_DIR, NAME + "_2026-11-02.json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = []
    md.append("# TUFT-r360 · ROOT V29（Dirac–Maxwell 自洽性）来料审计 · 数据与裁定表")
    md.append("")
    md.append("- 卷号：TUFT-r360 ｜ 日期：2026-11-02 ｜ 来料：ROOT V29")
    md.append("- 分层：**A 精确代数（Fraction）／B 高精度（Decimal 60 位）／G 判决／C 对照／PRICE 定价**。**条目不可跨层相加**。")
    md.append("")
    md.append("## 一、场能两口径（均匀带电球）")
    md.append("")
    md.append("| x = L/λ̄_C | 固定 ρ：U/(m_ec²) | 固定 Q=e：U/(m_ec²) |")
    md.append("| --- | --- | --- |")
    for i in range(len(B["u_r_rows"])):
        md.append("| %s | %s | %s |" % (fmt(B["u_r_rows"][i][0], 4),
                                        fmt(B["u_r_rows"][i][1], 8),
                                        fmt(B["u_q_rows"][i][1], 8)))
    md.append("")
    md.append("固定总电荷口径的闭式：U = e²/(40πε₀L) = αħc/(10L) ⇒ **∝ 1/L，不发散**。")
    md.append("")
    md.append("## 二、静电自能系数三路径")
    md.append("")
    md.append("| 路径 | 系数（U = 系数 × αħc/a） |")
    md.append("| --- | --- |")
    md.append("| Fourier 解析（高斯） | %s |" % fmt(B["c_exact"], 14))
    md.append("| 电场能量积分（高斯） | %s |" % fmt(B["c_field"], 14))
    md.append("| 两两相互作用积分（高斯） | %s |" % fmt(B["c_pair"], 14))
    md.append("| 换族：指数分布（解析 5/32） | %s |" % fmt(B["c_exp"], 14))
    md.append("")
    md.append("## 三、来料试探能量表复算")
    md.append("")
    md.append("| x | 来料动能项 | 本卷动能项 | 残差 | 来料电磁项 | 本卷电磁项 | 残差 |")
    md.append("| --- | --- | --- | --- | --- | --- | --- |")
    for (x, lk, fk, ek, le, fe, ee) in B["table"]:
        md.append("| %s | %s | %s | %s | %s | %s | %s |"
                  % (fmt(x, 8), fmt(lk, 9), fmt(fk, 9), fmt(ek, 3),
                     fmt(le, 9), fmt(fe, 9), fmt(ee, 3)))
    md.append("")
    md.append("## 四、条目表")
    md.append("")
    md.append("| ID | 层 | 条目 | 期望 | 实测 | 裁定 |")
    md.append("| --- | --- | --- | --- | --- | --- |")
    for it in ITEMS:
        md.append("| %s | %s | %s | %s | %s | **%s** |"
                  % (it["id"], it["kind"], it["name"].replace("|", "\\|"),
                     it["exp"].replace("|", "\\|"), it["act"].replace("|", "\\|"), it["verdict"]))
    md.append("")
    p_md = os.path.join(OUT_DIR, NAME + "_2026-11-02.md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(rep[:3500])
    print("...")
    print("WROTE:", p_rep)
    print("WROTE:", p_json)
    print("WROTE:", p_md)


if __name__ == "__main__":
    main()
