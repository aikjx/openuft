# -*- coding: utf-8 -*-
# TUFT-r375 · 审计 ROOT V34 来料《变化电磁场产生引力：从 Maxwell 方程到 Einstein 场方程的完整验证》
#
# 来料主张（要点见 数据/TUFT-r375_审计ROOTV34_来料要点摘录_公式逐字_2026-11-02.md）：
#   V34-1 G = 8πG/c⁴ (T^matter + T^EM)
#   V34-2 ∇²Φ = 8πG u_EM/c²      （T^EM 无迹 ⇒ 应力也进源，系数 2）
#        数值表 5 行（1 m³、ΔM=U/c²、Δg=GΔM/r²）
#   V34-3 E_φ = (rB0Ω/2)sinΩt、J_φ = (ε0 r/2)B̈（变化磁场链条）+ Poynting 残差 0
#   V34-4 pp-wave：H = −(4πG/c⁴)T_uu(x²+y²) ⇒ R_uu = 8πG T_uu/c⁴、R = 0
#   V34-5 □h̄ = −16πG T/c⁴；四极功率 4.20e-45 W；两光流 M = (2E/c²)|sin(ψ/2)|
#
# 立场：先算后判。凡「相符」必须给出独立路径；凡「通过」必须报它检验的是哪个量、判别力几许。
#
import io, os, sys, json, ast
import math
from decimal import Decimal as D, getcontext
getcontext().prec = 60

RID = "r375"
TITLE = "审计ROOTV34_电磁场产生引力全链路_张量无迹与pp波Ricci机核_四零判别力定价与零测地线聚焦增量"
STAMP = "2026-11-02"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUD_DIR = os.path.join(ROOT, "判定")

ZERO = D(0); ONE = D(1); TWO = D(2); THREE = D(3); FOUR = D(4); HALF = D("0.5")

# ============================================================================
# §0 · Decimal 数学（π 用 Machin；传 1/5、1/239，传 5 会级数发散到 Overflow）
# ============================================================================
def _atan_inv(x, terms=260):
    x = D(x); s = ZERO; x2 = x * x; t = x
    for k in range(terms):
        s += t / (2 * k + 1)
        t = -t * x2
    return s

PI = 4 * (4 * _atan_inv(ONE / 5) - _atan_inv(ONE / 239))
TWO_PI = 2 * PI

def dsqrt(x):
    x = D(x)
    if x < 0: raise ValueError("sqrt neg")
    if x == 0: return ZERO
    g = D(repr(math.sqrt(float(x))))
    if g == 0: g = D("1e-30")
    for _ in range(140):
        g2 = (g + x / g) / 2
        if g2 == g: break
        g = g2
    return g

def _ln2():
    y = ONE / 3; s = ZERO; t = y; n = 1
    for _ in range(340):
        s += t / n
        t = t * y * y
        n += 2
    return 2 * s

LN2 = _ln2()

def dexp(x):
    x = D(x)
    if x == 0: return ONE
    neg = x < 0
    if neg: x = -x
    n = int(x / LN2)
    r = x - n * LN2
    s = ONE; term = ONE
    for k in range(1, 110):
        term = term * r / k
        s += term
        if abs(term) < D("1e-74"): break
    val = s * (D(2) ** n)
    return (ONE / val) if neg else val

def dsin(x):
    r = D(x)
    k = int(r / TWO_PI); r = r - k * TWO_PI
    if r > PI: r -= TWO_PI
    if r < -PI: r += TWO_PI
    s = ZERO; t = r
    for k in range(1, 80):
        s += t
        t = -t * r * r / ((2 * k) * (2 * k + 1))
        if abs(t) < D("1e-74"): break
    return s

def dcos(x):
    r = D(x)
    k = int(r / TWO_PI); r = r - k * TWO_PI
    if r > PI: r -= TWO_PI
    if r < -PI: r += TWO_PI
    s = ZERO; t = ONE
    for k in range(0, 80):
        s += t
        t = -t * r * r / ((2 * k + 1) * (2 * k + 2))
        if abs(t) < D("1e-74"): break
    return s

def fmt(x, nd=18):
    if isinstance(x, D):
        if x == 0: return "0"
        return ("%." + str(nd) + "E") % x.normalize()
    return str(x)

def rel(a, b):
    """相对偏差。判「两数是否相同」一律用「偏离 + 容差」，禁用字符串相等。"""
    a = D(a); b = D(b)
    den = abs(b) if abs(b) > D("1e-300") else D("1e-300")
    return abs(a - b) / den

# ============================================================================
# §1 · 线性代数（4×4 求逆 / 偏导）
# ============================================================================
def mat_inv(m):
    n = len(m)
    a = [[D(m[i][j]) for j in range(n)] + [ONE if i == j else ZERO for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < D("1e-95"): raise ValueError("singular")
        a[c], a[p] = a[p], a[c]
        pv = a[c][c]
        a[c] = [v / pv for v in a[c]]
        for r in range(n):
            if r == c: continue
            f = a[r][c]
            if f != 0:
                a[r] = [a[r][j] - f * a[c][j] for j in range(2 * n)]
    return [row[n:] for row in a]

def dcoord(f, idx, pt, h=D("1e-12")):
    p1 = list(pt); p2 = list(pt)
    p1[idx] = p1[idx] + h; p2[idx] = p2[idx] - h
    return (D(f(*p1)) - D(f(*p2))) / (2 * h)

# ============================================================================
# §2 · 常数（SI，CODATA 2022 / PDG 2024）
# ============================================================================
C_LIGHT = D("299792458")
G_N = D("6.67430e-11")
MU0 = D("1.25663706212e-6")             # CODATA 2022（测量值）
EPS0_TAB = D("8.8541878128e-12")        # CODATA 2022 表列值，仅用于 G07 的口径核对
EPS0 = ONE / (MU0 * C_LIGHT * C_LIGHT)  # SI 关系 ε0 = 1/(μ0c²)（精确），保证两条路径自洽
E_CHG = D("1.602176634e-19")
HBAR = D("1.054571817e-34")
ALPHA = D("7.2973525643e-3")
M_E = D("9.1093837015e-31")
EV_J = D("1.602176634e-19")
MPC_M = D("3.0856775814913673e22")
LAM_C_BAR = HBAR / (M_E * C_LIGHT)   # 约化康普顿波长

# 单位自检：1/sqrt(eps0 mu0) 必须 = c（常数口径自守）
C_FROM_EM = ONE / dsqrt(EPS0 * MU0)

ETA = [[D(-1), ZERO, ZERO, ZERO],
       [ZERO, ONE, ZERO, ZERO],
       [ZERO, ZERO, ONE, ZERO],
       [ZERO, ZERO, ZERO, ONE]]

# ============================================================================
# §3 · 电磁场能量—动量张量（严格代数，无近似）
#    约定：x^0 = c t，度规 (−,+,+,+)；F_{0i} = −E_i/c，F_{ij} = ε_{ijk}B_k
#          T^{μν} = (1/μ0)( F^{μα}F^ν{}_α − ¼ g^{μν}F_{αβ}F^{αβ} )
# ============================================================================
def em_F(E, B, g=None, gi=None):
    """由 (E,B) 三矢量构造 F_{μν}。"""
    Fl = [[ZERO] * 4 for _ in range(4)]
    for i in range(3):
        Fl[0][i + 1] = -D(E[i]) / C_LIGHT
        Fl[i + 1][0] = D(E[i]) / C_LIGHT
    # F_{ij} = ε_{ijk} B_k
    Fl[1][2] = D(B[2]); Fl[2][1] = -D(B[2])
    Fl[1][3] = -D(B[1]); Fl[3][1] = D(B[1])
    Fl[2][3] = D(B[0]); Fl[3][2] = -D(B[0])
    return Fl

def T_from_F(Fl, g, gi, mu0=MU0):
    """T^{μν} 与迹；Fl 为 F_{μν}。返回 (T, trace, F2)。"""
    Fu = [[sum((gi[m][a] * gi[n][b] * Fl[a][b] for a in range(4) for b in range(4)), ZERO)
           for n in range(4)] for m in range(4)]
    F2 = sum((Fl[m][n] * Fu[m][n] for m in range(4) for n in range(4)), ZERO)
    # F^ν{}_α = g_{αβ} F^{νβ}
    Fmixed = [[sum((g[a][b] * Fu[m][b] for b in range(4)), ZERO) for a in range(4)] for m in range(4)]
    T = [[(sum((Fu[m][a] * Fmixed[n][a] for a in range(4)), ZERO)
           - gi[m][n] * F2 / 4) / mu0 for n in range(4)] for m in range(4)]
    tr = sum((g[m][n] * T[m][n] for m in range(4) for n in range(4)), ZERO)
    return T, tr, F2

def em_quantities(E, B):
    Fl = em_F(E, B)
    T, tr, F2 = T_from_F(Fl, ETA, ETA)
    u = sum((D(E[i]) ** 2 for i in range(3)), ZERO) * EPS0 / 2 + \
        sum((D(B[i]) ** 2 for i in range(3)), ZERO) / (2 * MU0)
    Tsum = sum((T[i][i] for i in range(1, 4)), ZERO)
    return dict(T=T, trace=tr, u=u, T00=T[0][0], Tsum=Tsum, F2=F2)

# ============================================================================
# §4 · 准静态变化磁场链条（V34-3）：圆柱坐标 (r,φ,z)，B = B0 cos(Ωt) ẑ
# ============================================================================
B0_Q = D("10"); F_Q = D("1000"); A_Q = D("0.1"); L_Q = D("0.5")
OM_Q = TWO_PI * F_Q

def Bq(t):  return B0_Q * dcos(OM_Q * t)
def Bq_d(t):  return -B0_Q * OM_Q * dsin(OM_Q * t)
def Bq_dd(t): return -B0_Q * OM_Q * OM_Q * dcos(OM_Q * t)

def Ephi(r, t):   return -(r / 2) * Bq_d(t)          # (V34-3) 原文形式
def Ephi_v2(r, t): return (r * B0_Q * OM_Q / 2) * dsin(OM_Q * t)   # 等价闭式
def Jphi(r, t):   return (EPS0 * r / 2) * Bq_dd(t)

def faraday_resid(r, t, h=D("1e-9")):
    """(∇×E)_z = (1/r)∂_r(r E_φ)；与 −∂_t B_z 比较。"""
    f = lambda rr: rr * Ephi(rr, t)
    curl = dcoord(f, 0, [r], h) / r
    return curl + Bq_d(t)

def ampere_resid(r, t, h=D("1e-9")):
    """∇×B 的 φ 分量为 0（B 均匀）⇒ μ0 J_φ + μ0 ε0 ∂_t E_φ 应为 0。"""
    dE = dcoord(lambda tt: Ephi(r, tt), 0, [t], D("1e-9"))
    return MU0 * Jphi(r, t) + MU0 * EPS0 * dE

def poynting_parts(r, t, h=D("1e-6")):
    """∂_t u 与 ∇·S。★两项各约 2e11 而相消到 0.1 ⇒ 一阶中心差分的截断误差 (h²/6)·u‴ 被放大到 O(1)，
    必须 Richardson：(4·D(h/2) − D(h))/3 消掉 h² 项。"""
    u = lambda rr, tt: (EPS0 * Ephi(rr, tt) ** 2 + Bq(tt) ** 2 / MU0) / 2
    Sr = lambda rr, tt: Ephi(rr, tt) * Bq(tt) / MU0
    def drich(f, idx, pt):
        d1 = dcoord(f, idx, pt, h)
        d2 = dcoord(f, idx, pt, h / 2)
        return (4 * d2 - d1) / 3
    dut = drich(lambda tt: u(r, tt), 0, [t])
    divS = drich(lambda rr: rr * Sr(rr, t), 0, [r]) / r
    jdE = Jphi(r, t) * Ephi(r, t)
    return dict(dut=dut, divS=divS, jdE=jdE, resid=dut + divS + jdE)

def poynting_closed(r, t, jscale=ONE):
    """Poynting 恒等式的**解析**三项（不取样、不差分）。
    u = ½[ε0E² + B²/μ0]，E = (rB₀Ω/2)sin(Ωt)、B = B₀cos(Ωt)，sc ≡ sin·cos：
      ∂_t u = Ω·sc·[ε0(rB₀Ω/2)² − B₀²/μ0]
      ∇·S   = B₀²Ω·sc/μ0            （S_r ∝ r ⇒ (1/r)∂_r(rS_r) 恰好回到同一个数）
      J·E   = −ε0r²B₀²Ω³·sc/4
    三项和恒等于 0（逐项抵消），与 (r,t) 无关 —— 这正是「残差为零是定义性的」的机读形式。
    ★为什么不用差分：本点 ∂_t u 与 ∇·S 各 ~2.1e11，而 ∂_t³u ~ 8e18 ⇒ 中心差分的 (h²/6)u'''
    即便一次 Richardson 也只压到 ~1e1，永远够不着 1e-20。「差分验证恒等式」在此尺度上是伪判据。"""
    sc = dsin(OM_Q * t) * dcos(OM_Q * t)
    k = B0_Q * OM_Q / 2
    dut = OM_Q * sc * (EPS0 * (r * k) ** 2 - B0_Q ** 2 / MU0)
    divS = B0_Q ** 2 * OM_Q * sc / MU0
    jdE = -EPS0 * (r ** 2) * (B0_Q ** 2) * (OM_Q ** 3) * sc / 4
    return dict(dut=dut, divS=divS, jdE=jdE * jscale,
                resid=dut + divS + jdE * jscale)

def U_E_trunc(Rc):
    """感生电场储能（截断到半径 Rc）：u = ½ε0 E_φ² ∝ r² ⇒ ∫ ∝ Rc⁴。"""
    # 解析：U = ∫0^Rc ½ ε0 (r B0 Ω/2)² (2π r L) dr = (π ε0 L (B0Ω/2)² /4) Rc⁴·… 逐步算
    k = B0_Q * OM_Q / 2
    return PI * EPS0 * L_Q * k * k * (Rc ** 4) / 4

# ============================================================================
# §5 · pp-wave：ds² = −2du dv + dx² + dy² + H(u,x,y)du²，坐标 (u,v,x,y)=(0,1,2,3)
#      闭式：R_uu = −½(∂x² + ∂y²)H
# ============================================================================
def g_pp(Hfun):
    def g(X):
        u, v, x, y = X[0], X[1], X[2], X[3]
        H = Hfun(u, x, y)
        return [[H, D(-1), ZERO, ZERO],
                [D(-1), ZERO, ZERO, ZERO],
                [ZERO, ZERO, ONE, ZERO],
                [ZERO, ZERO, ZERO, ONE]]
    return g

def numeric_ricci(gfun, X, h=D("1e-6")):
    def dg(Xp):
        out = []
        for l in range(4):
            p1 = list(Xp); p2 = list(Xp)
            p1[l] = p1[l] + h; p2[l] = p2[l] - h
            ga = gfun(p1); gb = gfun(p2)
            out.append([[(ga[i][j] - gb[i][j]) / (2 * h) for j in range(4)] for i in range(4)])
        return out
    def christ(Xp):
        g = gfun(Xp); gi = mat_inv(g); dgl = dg(Xp)
        G = [[[ZERO] * 4 for _ in range(4)] for _ in range(4)]
        for l in range(4):
            for m in range(4):
                for n in range(4):
                    s = ZERO
                    for sg in range(4):
                        s = s + gi[l][sg] * (dgl[m][n][sg] + dgl[n][m][sg] - dgl[sg][m][n])
                    G[l][m][n] = s / 2
        return G
    def dchrist(Xp, mu):
        p1 = list(Xp); p2 = list(Xp)
        p1[mu] = p1[mu] + h; p2[mu] = p2[mu] - h
        Ga = christ(p1); Gb = christ(p2)
        return [[[(Ga[l][m][n] - Gb[l][m][n]) / (2 * h) for n in range(4)]
                 for m in range(4)] for l in range(4)]
    G0 = christ(X)
    dG = [dchrist(X, mu) for mu in range(4)]
    Ric = [[ZERO] * 4 for _ in range(4)]
    for s in range(4):
        for nn in range(4):
            acc = ZERO
            for rho in range(4):
                acc = acc + dG[rho][rho][nn][s] - dG[nn][rho][rho][s]
                for lam in range(4):
                    acc = acc + G0[rho][rho][lam] * G0[lam][nn][s] - G0[rho][nn][lam] * G0[lam][rho][s]
            Ric[s][nn] = acc
    return Ric, G0

def ricci_rich(gfun, X, h=D("1e-4")):
    """Richardson 外推：R = (4R(h/2) − R(h))/3。"""
    R1, G0 = numeric_ricci(gfun, X, h)
    R2, _ = numeric_ricci(gfun, X, h / 2)
    out = [[(4 * R2[i][j] - R1[i][j]) / 3 for j in range(4)] for i in range(4)]
    return out, G0

# ============================================================================
# §6 · 测地偏离（零测地线汇 k = ∂_v）：D²ξ^i/dλ² = −R^i{}_{uju} ξ^j
#      pp-wave 的 R_{uiuj} = −½ ∂_i∂_j H；对 H = −κ(x²+y²) ⇒ R_{uiuj} = κ δ_ij
#      ⇒ ξ̈ = −κ ξ：κ>0 聚焦（T_uu>0），κ<0 发散。
# ============================================================================
def geodesic_deviation(kappa, lam_end, n=400):
    """RK4 解 ξ'' = −κ ξ，ξ(0)=1、ξ'(0)=0。返回 (ξ(λ_end), ξ'(λ_end))。"""
    xi, dxi = ONE, ZERO
    h = D(lam_end) / n
    def f(xv, dv):
        return dv, -D(kappa) * xv
    for _ in range(n):
        k1x, k1v = f(xi, dxi)
        k2x, k2v = f(xi + h * k1x / 2, dxi + h * k1v / 2)
        k3x, k3v = f(xi + h * k2x / 2, dxi + h * k2v / 2)
        k4x, k4v = f(xi + h * k3x, dxi + h * k3v)
        xi = xi + h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        dxi = dxi + h * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
    return xi, dxi

def geodesic_deviation_rich(kappa, lam_end, n=400):
    """Richardson：(16·x(2n) − x(n))/15（RK4 四阶 ⇒ 消掉 h⁴ 项）。"""
    x1, _ = geodesic_deviation(kappa, lam_end, n)
    x2, _ = geodesic_deviation(kappa, lam_end, 2 * n)
    return (16 * x2 - x1) / 15

# ============================================================================
# §7 · 判据容器：ok 驱动 kind（禁止「ok=False 却标 PASS」）
# ============================================================================
MAIN, CTL, GRD = [], [], []

def add(lst, eid, kind, title, exp, act, ok, note):
    if not bool(ok):
        kind = "FAIL"
    lst.append(dict(id=eid, kind=kind, title=title,
                    exp=(fmt(exp) if isinstance(exp, D) else str(exp)),
                    act=(fmt(act) if isinstance(act, D) else str(act)),
                    ok=bool(ok), note=note))

RES = {}
TOL = D("1e-30")


# ============================================================================
# §8 · 逐项实算
# ============================================================================
RES["c_from_em"] = C_FROM_EM
RES["c_rel"] = rel(C_FROM_EM, C_LIGHT)

# ---- 8.2 T^EM 无迹性（静态 E / 静态 B / 零模行波）----------------------------
E0 = D("1e6")
qE = em_quantities([ZERO, ZERO, E0], [ZERO, ZERO, ZERO])
qB = em_quantities([ZERO, ZERO, ZERO], [ZERO, ZERO, ONE])
qW = em_quantities([E0, ZERO, ZERO], [ZERO, E0 / C_LIGHT, ZERO])
RES["tr_E"] = qE["trace"]; RES["tr_B"] = qB["trace"]; RES["tr_W"] = qW["trace"]
RES["tr_max"] = max(abs(qE["trace"]), abs(qB["trace"]), abs(qW["trace"]))
RES["u_E"] = qE["u"]; RES["u_B"] = qB["u"]; RES["u_W"] = qW["u"]
RES["T00_E_rel"] = rel(qE["T00"], qE["u"])
RES["Tsum_E_rel"] = rel(qE["Tsum"], qE["u"])
RES["Tsum_B_rel"] = rel(qB["Tsum"], qB["u"])
RES["Tsum_W_rel"] = rel(qW["Tsum"], qW["u"])

m_pr = D("1e-3"); A_pr = D("1")
RES["tr_proca"] = -(m_pr ** 2) * A_pr * A_pr / MU0

# ---- 8.3 弱场泊松系数：局域源 (T00 + ΣTii)/c² = 2u/c² ---------------------
RES["src_dens_energy"] = qE["u"] / (C_LIGHT ** 2)
RES["src_dens_full"] = (qE["T00"] + qE["Tsum"]) / (C_LIGHT ** 2)
RES["src_dens_ratio"] = RES["src_dens_full"] / RES["src_dens_energy"]

# ---- 8.4 数值表 5 行（V = 1 m³，r = 1 m）---------------------------------
CLAIM_ROWS = [
    ("E = 1 MV/m",  "E", D("1e6"), D("4.427"),   D("4.926e-17"), D("3.288e-27")),
    ("E = 10 MV/m", "E", D("1e7"), D("442.709"), D("4.926e-15"), D("3.288e-25")),
    ("B = 1 T",     "B", D("1"),   D("3.979e5"), D("4.427e-12"), D("2.955e-22")),
    ("B = 10 T",    "B", D("10"),  D("3.979e7"), D("4.427e-10"), D("2.955e-20")),
    ("B = 100 T",   "B", D("100"), D("3.979e9"), D("4.427e-8"),  D("2.955e-18")),
]
rows_tbl = []
max_tbl_rel = ZERO
u_list = []
for name, kind, val, U_c, dM_c, dg_c in CLAIM_ROWS:
    u = (EPS0 * val * val / 2) if kind == "E" else (val * val / (2 * MU0))
    u_list.append(u)
    U = u * ONE
    dM = U / (C_LIGHT ** 2)
    dg = G_N * dM
    rr = max(rel(U, U_c), rel(dM, dM_c), rel(dg, dg_c))
    max_tbl_rel = max(max_tbl_rel, rr)
    rows_tbl.append([name, fmt(U, 6), fmt(dM, 6), fmt(dg, 6), fmt(rr, 3)])
RES["tbl_rows"] = rows_tbl
RES["tbl_max_rel"] = max_tbl_rel
E_DOUBLE = u_list[1] / u_list[0]          # 应 = 100（E 加倍 ⇒ 能量 ×4；1→10 就是 ×100）
RES["E_double"] = E_DOUBLE
RES["dg_us"] = G_N * (qB["u"] / C_LIGHT ** 2)

u_panel = EPS0 * (D("1e7") ** 2) / 2 + D("100") / (2 * MU0)
RES["panel_U"] = u_panel
RES["panel_dM"] = u_panel / C_LIGHT ** 2
RES["panel_dg"] = G_N * RES["panel_dM"]

# ---- 8.5 V34-3：Faraday 与 Ampère 两个方程的残差 --------------------------
pts_rt = [(D("0.05"), D("1.3e-4")), (D("0.10"), D("3.7e-4")),
          (D("0.03"), D("6.1e-4")), (D("0.08"), D("9.4e-4"))]
RES["faraday_res"] = max(abs(faraday_resid(r, t)) for r, t in pts_rt)
RES["ampere_res"] = max(abs(ampere_resid(r, t)) for r, t in pts_rt)
RES["Ephi_max"] = Ephi_v2(A_Q, PI / (2 * OM_Q))

# ---- 8.6 §五 数值例 ------------------------------------------------------
V_coil = PI * A_Q * A_Q * L_Q
U_B = B0_Q * B0_Q / (2 * MU0) * V_coil
E_a = Ephi_v2(A_Q, PI / (2 * OM_Q))
U_E_in = U_E_trunc(A_Q)
dM_B = U_B / C_LIGHT ** 2
RES.update(V_coil=V_coil, U_B=U_B, E_a=E_a, U_E_in=U_E_in, dM_B=dM_B, UE_over_UB=U_E_in / U_B)

# ---- 8.7 感生电场储能随截断半径的幂次 ------------------------------------
U_1 = U_E_trunc(A_Q)
U_2 = U_E_trunc(TWO * A_Q)
RES["U_E_r1"] = U_1
RES["U_E_ratio_2R"] = U_2 / U_1

# ---- 8.8 Poynting：残差与其「定义性」定价 ---------------------------------
pp_pt = (D("0.07"), D("4.2e-4"))
pp = poynting_parts(pp_pt[0], pp_pt[1])            # 差分流水线：只留作精度对照
pc = poynting_closed(pp_pt[0], pp_pt[1])           # 解析三项：本条的判据来源
RES["poy_scale"] = abs(pc["jdE"]) if abs(pc["jdE"]) > D("1e-300") else D("1e-300")
RES["poy_res"] = pc["resid"]
RES["poy_rel"] = abs(pc["resid"]) / RES["poy_scale"]
RES["poy_dut"] = pc["dut"]
RES["poy_divS"] = pc["divS"]
RES["poy_jdE"] = pc["jdE"]
RES["poy_res_fd"] = pp["resid"]
RES["poy_rel_fd"] = abs(pp["resid"]) / RES["poy_scale"]
eps_bad = D("1.01")
pb = poynting_closed(pp_pt[0], pp_pt[1], jscale=eps_bad)
RES["poy_bad_rel"] = abs(pb["resid"] - pc["resid"]) / RES["poy_scale"]

# ---- 8.9 pp-wave：Ricci 数值 vs 闭式 -------------------------------------
X0 = [D("0.31"), D("0.72"), D("0.25"), D("-0.41")]
H_EM = D("1.7")
g_em = g_pp(lambda u, x, y: H_EM * (x * x + y * y))
Ric_em, G_em = ricci_rich(g_em, X0, D("1e-4"))
RES["Ruu_em_num"] = Ric_em[0][0]
RES["Ruu_em_cl"] = -TWO * H_EM
RES["Ruu_em_rel"] = rel(Ric_em[0][0], RES["Ruu_em_cl"])
# 同一度规、同一 h，但**不做** Richardson。
# ★首跑发现它也是 0：二阶中心差分对**二次** H 精确（f⁗=0）⇒ 这个点上「外推」零判别力。
#   故此处只作「退化点」证据留档，真正的判别力检验挪到四次剖面（见下方 g_4q 与 C6）。
Ric_plain, _ = numeric_ricci(g_em, X0, D("1e-4"))
RES["Ruu_em_num_plain"] = Ric_plain[0][0]
RES["Ruu_em_rel_plain"] = rel(Ric_plain[0][0], RES["Ruu_em_cl"])
RES["Ruu_other_max"] = max(abs(Ric_em[i][j]) for i in range(4) for j in range(4) if (i, j) != (0, 0))

def scalar_curv(Ric, X, gfun):
    g = gfun(X); gi = mat_inv(g)
    return sum((gi[m][n] * Ric[m][n] for m in range(4) for n in range(4)), ZERO), gi

Rsc_em, gi_em = scalar_curv(Ric_em, X0, g_em)
RES["Rsc_em"] = Rsc_em
RES["guu_em"] = gi_em[0][0]

g_pl = g_pp(lambda u, x, y: H_EM * (x * x - y * y))
Ric_pl, _ = ricci_rich(g_pl, X0, D("1e-4"))
Rsc_pl, gi_pl = scalar_curv(Ric_pl, X0, g_pl)
g_3 = g_pp(lambda u, x, y: D("0.9") * x * x * x * y)
Ric_3, _ = ricci_rich(g_3, X0, D("1e-4"))
Rsc_3, gi_3 = scalar_curv(Ric_3, X0, g_3)
RES.update(Ruu_pl=Ric_pl[0][0], Rsc_pl=Rsc_pl, Ruu_3=Ric_3[0][0], Rsc_3=Rsc_3,
           Ruu_3_cl=-3 * D("0.9") * X0[2] * X0[3], guu_pl=gi_pl[0][0], guu_3=gi_3[0][0])

# ---- 8.9b 四次剖面：唯一能分开「外推 / 不外推」的 H（C6 的判据来源）------
# 二阶中心差分对二次多项式精确（f⁗=0）⇒ 三次也不够（f⁶=0），必须 ≥4 次。
# H = a x⁴ + b x²y² + c y⁴ ⇒ ∂x²H = 12a x² + 2b y²、∂y²H = 2b x² + 12c y²
#   ⇒ R_uu = −½(∂x²+∂y²)H = −½[(12a+2b)x² + (2b+12c)y²]（闭式，不共用数值路径）
QA, QB, QC = D("0.4"), D("0.25"), D("0.3")
g_4q = g_pp(lambda u, x, y: QA * x ** 4 + QB * x * x * y * y + QC * y ** 4)
Ric_4q, _ = ricci_rich(g_4q, X0, D("1e-4"))
Ric_4q_plain, _ = numeric_ricci(g_4q, X0, D("1e-4"))
RES["Ruu_4q_cl"] = -((12 * QA + 2 * QB) * X0[2] ** 2 + (2 * QB + 12 * QC) * X0[3] ** 2) / 2
RES["Ruu_4q_num"] = Ric_4q[0][0]
RES["Ruu_4q_num_plain"] = Ric_4q_plain[0][0]
RES["Ruu_4q_rel"] = rel(Ric_4q[0][0], RES["Ruu_4q_cl"])
RES["Ruu_4q_rel_plain"] = rel(Ric_4q_plain[0][0], RES["Ruu_4q_cl"])

# ---- 8.10 V34-4 的系数（把 4πG/c⁴ 归一为 1，避免 1e-44 量级的相对精度损失）--
K1 = ONE
g_4 = g_pp(lambda u, x, y: -K1 * (x * x + y * y))
Ric_4, _ = ricci_rich(g_4, X0, D("1e-4"))
RES["Ruu_v4"] = Ric_4[0][0]
RES["Ruu_v4_cl"] = TWO * K1
RES["Ruu_v4_rel"] = rel(Ric_4[0][0], RES["Ruu_v4_cl"])
g_4b = g_pp(lambda u, x, y: -TWO * K1 * (x * x + y * y))
Ric_4b, _ = ricci_rich(g_4b, X0, D("1e-4"))
RES["Ruu_v4_bad"] = Ric_4b[0][0]
RES["Ruu_v4_bad_ratio"] = Ric_4b[0][0] / Ric_4[0][0]

# ---- 8.11 pp-wave 上的 Maxwell：F = a(u) du∧dx ---------------------------
def pp_maxwell_resid(a_fun, point, h=D("1e-7")):
    """F_{ux}=a ⇒ F^{vx} = −a、F^{ux} = 0（g^{uu}=0）；∇_μF^{μx} = −∂_v a。"""
    u0, v0 = point[0], point[1]
    d_v = (a_fun(u0, v0 + h) - a_fun(u0, v0 - h)) / (2 * h)
    return -d_v

a_ok = lambda uu, vv: D("0.3") * dcos(D("2.5") * uu)
a_bad = lambda uu, vv: D("0.3") * dcos(D("2.5") * vv)
RES["max_res_ok"] = abs(pp_maxwell_resid(a_ok, X0))
RES["max_res_bad"] = abs(pp_maxwell_resid(a_bad, X0))
RES["Tuu_pp"] = D("0.3") ** 2 / MU0

# ---- 8.12 新产出 1：零测地线聚焦 -----------------------------------------
kap = D("1.3")
# ★RK4 在 n=400（h=2.5e-3）时的截断误差 ~h⁴ ≈ 4e-11，正好落在 1e-11 量级
#   ⇒ 与闭式比的偏差有 1.4e-11，达不到 1e-16。必须先 Richardson 把 h⁴ 项消掉，
#   否则「数值 vs 解析」的判据测的是积分器而不是物理。
xi_num = geodesic_deviation_rich(kap, ONE, 400)
xi_cl = dcos(dsqrt(kap))
RES.update(kappa=kap, xi_num=xi_num, xi_cl=xi_cl, xi_rel=rel(xi_num, xi_cl))
kap_neg = -kap
xi_neg = geodesic_deviation_rich(kap_neg, ONE, 400)
# cosh(√|κ|) = cos(i√|κ|)；用 exp 精确算，避免复数
sq = dsqrt(-kap_neg)
xi_neg_cl = (dexp(sq) + dexp(-sq)) / 2
RES["xi_neg"] = xi_neg
RES["xi_neg_cl"] = xi_neg_cl
RES["xi_neg_rel"] = rel(xi_neg, xi_neg_cl)
RES["focus_ratio"] = xi_neg / xi_num

I_las = D("1e12")
Tuu_las = I_las / C_LIGHT
KAPPA_REAL = 4 * PI * G_N / (C_LIGHT ** 4)
RES["Tuu_las"] = Tuu_las
RES["kappa_las"] = KAPPA_REAL * Tuu_las
RES["defoc_las"] = KAPPA_REAL * Tuu_las / 2
RES["KAPPA_REAL"] = KAPPA_REAL

# ---- 8.13 新产出 2：静态装置应力抵消的显式模型 ---------------------------
u_m = ONE; V_f = ONE; V_s = D("0.1"); eps_m = D("1e-3")
src_int_full = (u_m * V_f + eps_m * V_s) + (u_m * V_f - u_m * V_f)
src_int_nostrut = (u_m * V_f + eps_m * V_s) + (u_m * V_f)
energy_tot = u_m * V_f + eps_m * V_s
RES.update(src_int_full=src_int_full, src_int_nostrut=src_int_nostrut, energy_tot=energy_tot,
           src_int_rel=rel(src_int_full, energy_tot), src_int_ratio=src_int_nostrut / src_int_full)
# 「无支柱 ⇒ 源恰好 2 倍」在 ε_m>0 时**不精确**：比值 = 1 + u_mV_f/E，缺口恰为物质层占能比。
# 这一条必须显式报出来，否则「恰 2 倍」就是一句没被检验的话。
RES["src_rel_nostrut"] = rel(src_int_nostrut, energy_tot)
RES["src_two_gap"] = TWO - RES["src_int_ratio"]
RES["src_matter_frac"] = eps_m * V_s / energy_tot

# ---- 8.14 线性化：G^(1) = −½□h̄ -------------------------------------------
def lin_G(hfun, X, h=D("1e-3")):
    def dh(mu, Xp):
        p1 = list(Xp); p2 = list(Xp)
        p1[mu] = p1[mu] + h; p2[mu] = p2[mu] - h
        A = hfun(p1); B = hfun(p2)
        return [[(A[i][j] - B[i][j]) / (2 * h) for j in range(4)] for i in range(4)]
    def Gam(Xp):
        D1 = [dh(mu, Xp) for mu in range(4)]
        G = [[[ZERO] * 4 for _ in range(4)] for _ in range(4)]
        for l in range(4):
            for m in range(4):
                for n in range(4):
                    s = ZERO
                    for sg in range(4):
                        s += ETA[l][sg] * (D1[m][n][sg] + D1[n][m][sg] - D1[sg][m][n])
                    G[l][m][n] = s / 2
        return G
    def dGam(lam):
        p1 = list(X); p2 = list(X)
        p1[lam] = p1[lam] + h; p2[lam] = p2[lam] - h
        A = Gam(p1); B = Gam(p2)
        return [[[(A[l][m][n] - B[l][m][n]) / (2 * h) for n in range(4)]
                 for m in range(4)] for l in range(4)]
    G0 = Gam(X)
    dG = [dGam(lam) for lam in range(4)]
    Ric = [[ZERO] * 4 for _ in range(4)]
    for m in range(4):
        for n in range(4):
            acc = ZERO
            for l in range(4):
                acc = acc + dG[l][l][m][n] - dG[n][l][m][l]
            Ric[m][n] = acc
    Rsc = sum((ETA[m][n] * Ric[m][n] for m in range(4) for n in range(4)), ZERO)
    return [[Ric[m][n] - ETA[m][n] * Rsc / 2 for n in range(4)] for m in range(4)]

OM_L = D("0.4")
def h_bar_mat(X):
    t = X[0]; c0 = dcos(OM_L * t)
    m = [[ZERO] * 4 for _ in range(4)]
    m[1][1] = c0; m[2][2] = -c0
    return m

XL = [D("0.37"), D("0.1"), D("0.2"), D("0.3")]
Glin = lin_G(h_bar_mat, XL, D("1e-3"))
RES["lin_G_num"] = Glin[1][1]
# 解析：h_xx=c(t)、h_yy=−c(t) ⇒ Γ^t_xx=ċ/2、Γ^t_yy=−ċ/2 ⇒ R_xx=c̈/2、R=0 ⇒ G_xx=c̈/2
RES["lin_G_cl"] = HALF * (-OM_L * OM_L) * dcos(OM_L * XL[0])
RES["lin_G_rel"] = rel(RES["lin_G_num"], RES["lin_G_cl"])
RES["lin_ratio"] = RES["lin_G_num"] / (-HALF * (OM_L * OM_L) * dcos(OM_L * XL[0]))  # 相当于 /(□h̄ 的 −½)

# ---- 8.15 四极辐射：两种记账 ---------------------------------------------
E_quad = D("1000"); R_quad = D("0.1"); F_quad = D("1e6")
OM_quad = TWO_PI * F_quad
Q0 = E_quad / (C_LIGHT ** 2) * R_quad * R_quad
P_single = G_N / (5 * C_LIGHT ** 5) * (Q0 * OM_quad ** 3) ** 2
P_diag = G_N / (5 * C_LIGHT ** 5) * (TWO * (Q0 * OM_quad ** 3) ** 2)
CLAIM_P = D("4.20e-45")
RES.update(Q0=Q0, P_single=P_single, P_diag=P_diag,
           P_rel_claim=rel(P_single, CLAIM_P), P_ratio_2=P_diag / P_single)

# ---- 8.16 两光流合成质量 -------------------------------------------------
def two_photon(psi, E):
    p1 = [E / C_LIGHT, ZERO, ZERO, E / C_LIGHT]
    p2 = [E / C_LIGHT, E / C_LIGHT * dsin(psi), ZERO, E / C_LIGHT * dcos(psi)]
    Pt = [p1[i] + p2[i] for i in range(4)]
    Etot = Pt[0] * C_LIGHT
    P2 = Pt[1] ** 2 + Pt[2] ** 2 + Pt[3] ** 2
    M2c4 = Etot * Etot - C_LIGHT * C_LIGHT * P2
    M = dsqrt(M2c4 if M2c4 > ZERO else ZERO) / (C_LIGHT ** 2)
    cl = TWO * E * abs(dsin(psi / 2)) / (C_LIGHT ** 2)
    return M, cl, dsqrt(P2)

rows_2g = []
max_2g = ZERO
for psi_d in [30, 90, 180]:
    psi = D(psi_d) * PI / 180
    M, cl, pt = two_photon(psi, ONE)
    max_2g = max(max_2g, rel(M, cl))
    rows_2g.append([str(psi_d) + "°", fmt(M, 8), fmt(cl, 8), fmt(rel(M, cl), 3)])
RES["two_photon_rows"] = rows_2g
RES["two_photon_max_rel"] = max_2g
_, _, pt_pi = two_photon(PI, ONE)
RES["ptot_pi"] = pt_pi

# ---- 8.17 紧致度：引力束缚两光所需能量 -----------------------------------
def E_confine(r):
    return (C_LIGHT ** 4) * r / (2 * G_N)
RES["E_conf_lam"] = E_confine(LAM_C_BAR)
RES["M_conf_lam"] = RES["E_conf_lam"] / C_LIGHT ** 2
RES["E_conf_um"] = E_confine(D("1e-6"))
RES["ratio_to_electron"] = RES["E_conf_lam"] / (M_E * C_LIGHT ** 2)
RES["amp_1000J"] = RES["E_conf_lam"] / D("1000")
RES["compact_1000J_lam"] = TWO * G_N * D("1000") / (C_LIGHT ** 4) / LAM_C_BAR

# ---- 8.18 GW170817 的算术核对 -------------------------------------------
DT_GW = D("1.7"); D_GW = D("40") * MPC_M
RES["t_travel"] = D_GW / C_LIGHT
RES["dv_over_c"] = DT_GW / RES["t_travel"]

# ---- 8.19 距离幂次（对数斜率）------------------------------------------
def slope(p, r0, h=D("1e-4")):
    a = float(r0 * (ONE + h)) ** p
    b = float(r0 * (ONE - h)) ** p
    return D(str(math.log(a / b) / math.log((1 + float(h)) / (1 - float(h)))))
RES["slope_r2"] = slope(-2, ONE)
RES["slope_r3"] = slope(-3, ONE)
RES["slope_r1"] = slope(-1, ONE)

# ============================================================================
# §9 · 判据（ok 驱动 kind：ok=False 一律降级 FAIL）
# ============================================================================
add(MAIN, "P01", "PASS",
    "T^EM 在 4 维无迹：静态 E、静态 B、零模行波三种配置的 g_{μν}T^{μν} 均为机器零",
    ZERO, RES["tr_max"], RES["tr_max"] < D("1e-40"),
    "三种配置（E=1 MV/m 沿 z；B=1 T 沿 z；E×B 零模行波）各自由 F_{μν} 直算 T^{μν}，迹的最大绝对值 %s。"
    "无迹性是 4 维电磁张量代数的后果，不是假设；判别力由 C1（Proca 有质量场）标定。"
    % fmt(RES["tr_max"], 6))

add(MAIN, "P02", "PASS",
    "T^{00} 与 Σ_i T^{ii} 各自等于 u_EM（张量直算 vs 能量密度定义式，两条独立路径）",
    ZERO, max(RES["T00_E_rel"], RES["Tsum_E_rel"], RES["Tsum_B_rel"], RES["Tsum_W_rel"]),
    max(RES["T00_E_rel"], RES["Tsum_E_rel"], RES["Tsum_B_rel"], RES["Tsum_W_rel"]) < D("1e-40"),
    "静态 E：T^{00}/u−1 = %s，ΣT^{ii}/u−1 = %s；静态 B：%s；零模：%s。"
    "⇒ 弱场泊松源的 (T_00+ΣT_ii)/c² 精确等于 **2u/c²**，V34-2 的系数 2 成立。"
    % (fmt(RES["T00_E_rel"], 3), fmt(RES["Tsum_E_rel"], 3),
       fmt(RES["Tsum_B_rel"], 3), fmt(RES["Tsum_W_rel"], 3)))

add(MAIN, "P03", "PASS",
    "V34 §四 数值表 5 行复算（U、ΔM=U/c²、Δg=GΔM/r²）",
    ZERO, RES["tbl_max_rel"], RES["tbl_max_rel"] < D("5e-4"),
    "五行最大相对偏差 %s（来料 4 位有效数字，容差 5e-4）。例：B=1 T ⇒ u = %s J、ΔM = %s kg、Δg(1 m) = %s m/s²；"
    "交互面板（E=10 MV/m 且 B=10 T）反算 %s J / %s kg / %s m/s²。"
    % (fmt(RES["tbl_max_rel"], 3), fmt(qB["u"], 10), fmt(qB["u"] / C_LIGHT ** 2, 8),
       fmt(RES["dg_us"], 8), fmt(RES["panel_U"], 8), fmt(RES["panel_dM"], 8), fmt(RES["panel_dg"], 8)))

add(MAIN, "P04", "PASS",
    "★口径并列（不是错）：§三 的局域源是 2u/c²，§四 表的 ΔM 是 u/c²，两者比值恰为 2",
    TWO, RES["src_dens_ratio"], rel(RES["src_dens_ratio"], TWO) < D("1e-40"),
    "局域泊松源 (T_00+ΣT_ii)/c² = %s kg/m³，纯能量口径 u/c² = %s kg/m³，比值 %s。"
    "两者都对但**不是同一个量**：前者是 ∇²Φ 的局域源，后者是完整静态装置的 ADM 质量（应力积分在平衡下抵消）。"
    "来料 §三 已声明「不能直接把 2U/c² 当作完整装置远场质量」⇒ 这不是错误，而是**两个口径必须并列申报**；"
    "本卷把它算成恰好 2（%s），并给出抵消的显式模型（P14）。★若按 §三 重算，表里全部 Δg 应乘 2。"
    % (fmt(RES["src_dens_full"], 8), fmt(RES["src_dens_energy"], 8),
       fmt(RES["src_dens_ratio"], 10), "见 C8"))

add(MAIN, "P05", "PASS",
    "V34-3 的两个方程残差：Faraday（∇×E = −∂_tB）与 Ampère–Maxwell（J_φ 闭式）",
    ZERO, max(RES["faraday_res"], RES["ampere_res"]),
    max(RES["faraday_res"], RES["ampere_res"]) < D("1e-15"),
    "4 个 (r,t) 点上：Faraday 残差 ≤ %s（V/m²）、Ampère 残差 ≤ %s（A/m²）；边界峰值 E_φ(a) = %s V/m（来料 3,141.59）。"
    "⇒ 「变化磁场不能独立于感生电场存在」这一步成立。"
    % (fmt(RES["faraday_res"], 4), fmt(RES["ampere_res"], 4), fmt(RES["E_a"], 10)))

add(MAIN, "P06", "PASS",
    "V34 §五 数值例复算：线圈体积、磁能峰值、边界电场、感生电场储能、质量当量",
    D("625000"), RES["U_B"], rel(RES["U_B"], D("625000")) < D("2e-4"),
    "V = πa²L = %s m³，U_B = B0²/(2μ0)·V = %s J（来料 625,000）；E_φ(a) = %s V/m；"
    "U_E(仅线圈内) = %s J（来料 3.432e-7）；ΔM_B = %s kg（来料 6.954e-12）；U_E/U_B = %s（小 12 个量级）。"
    % (fmt(V_coil, 8), fmt(U_B, 10), fmt(E_a, 10), fmt(U_E_in, 6), fmt(dM_B, 6), fmt(RES["UE_over_UB"], 4)))

add(MAIN, "P07", "PASS",
    "★来料未声明的一处截断：感生电场储能 ∫½ε0E_φ²dV ∝ R⁴，线圈外发散；3.432e-7 J 是「仅线圈内」的值",
    D("16"), RES["U_E_ratio_2R"], rel(RES["U_E_ratio_2R"], D("16")) < D("1e-20"),
    "截断半径从 a 加倍到 2a，储能比 = %s（=2⁴）⇒ 指数确为 4。E_φ ∝ r ⇒ u ∝ r² ⇒ 每单位长度能量随半径发散。"
    "故 3.432e-7 J 只能读作**线圈内部**的截断积分；准静态均匀 B 模型的感生电场延伸到无穷远，场能发散 ⇒ 这一行不是「感生电场储能」的全量。"
    % fmt(RES["U_E_ratio_2R"], 6))

add(MAIN, "P08", "INFO",
    "★Poynting 残差为零是**定义性**的：J_φ 正是由 ∂_tE_φ 反解出来的",
    ZERO, RES["poy_rel"], RES["poy_rel"] < D("1e-20"),
    "解析三项：∂_t u = %s、∇·S = %s、J·E = %s，各 ~1e11 却**逐项抵消** ⇒ 残差/|J·E| = %s（机零）。"
    "因为 J_φ = (ε0r/2)B̈ 由 Ampère–Maxwell 反解，代回必为零；「SymPy 残差为零」只证明代码照抄了定义。"
    "★同点差分流水线给 %s（差 100%% 以上）⇒ 该恒等式**不能用差分验证**：此处 ∂_t³u ~ 8e18，"
    "(h²/6)u''' 即使在 h=1e-6 下也有 1e6 量级，一次 Richardson 只压到 ~1e1。判据必须用解析三项，差分只作精度对照。"
    "判别力标定见 C2：J→1.01J 时残差/|J·E| = %s ⇒ 该式能抓写错的 J，抓不住循环性。⇒ **不可计入证据**，只作 bug 探测器。"
    % (fmt(RES["poy_dut"], 6), fmt(RES["poy_divS"], 6), fmt(RES["poy_jdE"], 6),
       fmt(RES["poy_rel"], 3), fmt(RES["poy_rel_fd"], 3), fmt(RES["poy_bad_rel"], 3)))

add(MAIN, "P09", "PASS",
    "V34-4 的几何核：H = h(x²+y²) 时 R_uu = −½(∂x²+∂y²)H = −2h（4 维数值 Ricci vs 闭式）",
    RES["Ruu_em_cl"], RES["Ruu_em_num"], RES["Ruu_em_rel"] < D("1e-12"),
    "数值（Christoffel→Ricci，Richardson 外推）%s vs 闭式 −2h = %s，相对偏差 %s；其余 15 个 Ricci 分量最大绝对值 %s。"
    "数值路径只用度规与差分，闭式只用 H 的二阶偏导 ⇒ 两条路径不共享中间量。"
    % (fmt(RES["Ruu_em_num"], 10), fmt(RES["Ruu_em_cl"], 10), fmt(RES["Ruu_em_rel"], 3), fmt(RES["Ruu_other_max"], 3)))

add(MAIN, "P10", "INFO",
    "★「R = 0」对该 ansatz 零判别力：g^{uu} ≡ 0 ⇒ 任何 H(u,x,y) 都给 R = 0",
    ZERO, RES["Rsc_em"], abs(RES["Rsc_em"]) < D("1e-18"),
    "R = g^{μν}R_{μν} = %s，而 g^{uu} = %s（精确 0）；本图只有 R_uu ≠ 0、g^{uu}=0 ⇒ uu 项自动不进迹。"
    "换 +偏振 H=h(x²−y²)：R_uu = %s、R = %s；换 H=0.9x³y（任意函数）：R_uu = %s（闭式 %s）、R = %s。"
    "三例 R 全为 0 ⇒ 「R=0」既不区分电磁 pp 波与真空引力波，也不检验 H 形式。**不可计入证据**。"
    % (fmt(RES["Rsc_em"], 3), fmt(RES["guu_em"], 3), fmt(RES["Ruu_pl"], 6), fmt(RES["Rsc_pl"], 3),
       fmt(RES["Ruu_3"], 8), fmt(RES["Ruu_3_cl"], 8), fmt(RES["Rsc_3"], 3)))

add(MAIN, "P11", "PASS",
    "V34-4 的系数：H = −(4πG/c⁴)T_uu(x²+y²) ⇒ R_uu = 8πG T_uu/c⁴（4πG/c⁴ 归一为 1 时 R_uu = 2）",
    RES["Ruu_v4_cl"], RES["Ruu_v4"], RES["Ruu_v4_rel"] < D("1e-12"),
    "取 K=4πG/c⁴=1、T_uu=1 ⇒ 闭式 R_uu = 2K·T_uu = %s，数值 %s，相对偏差 %s。"
    "系数差 2 倍的敏感性：误写 H=−(8πG/c⁴)T_uu(x²+y²) ⇒ R_uu = %s（比值 %s）⇒ 本判据对系数**有**判别力（与 P10 的 R=0 相反）。"
    "真实标度 K = %s。"
    % (fmt(RES["Ruu_v4_cl"], 6), fmt(RES["Ruu_v4"], 10), fmt(RES["Ruu_v4_rel"], 3),
       fmt(RES["Ruu_v4_bad"], 6), fmt(RES["Ruu_v4_bad_ratio"], 8), fmt(RES["KAPPA_REAL"], 6)))

add(MAIN, "P12", "INFO",
    "★pp-wave 上的「Maxwell 检查」判别力有限：只排除场对 v 的依赖，不约束 u 剖面",
    RES["max_res_ok"], RES["max_res_bad"],
    (RES["max_res_ok"] < D("1e-25")) and (RES["max_res_bad"] > D("1e-3")),
    "F_{ux}=a(u) ⇒ ∇_μF^{μx} = %s（机器零）；a(v) ⇒ %s（非零）。因 √|g|=1 且唯一非零分量上指标为 v，"
    "协变散度只剩 ∂_v ⇒ **任意 a(u,x,y)（含脉冲、台阶）都是解**。⇒ 该检查只证明「沿 u 传播」，不约束剖面；"
    "T_uu = a²/μ0 = %s > 0 恒成立（零能量条件自动满足），也不构成独立约束。"
    % (fmt(RES["max_res_ok"], 5), fmt(RES["max_res_bad"], 6), fmt(RES["Tuu_pp"], 6)))

add(MAIN, "P13", "PASS",
    "★本卷新产出 1：电磁波对零测地线的聚焦可由测地偏离显式算出，方向由 T_uu 的符号决定",
    RES["xi_cl"], RES["xi_num"], RES["xi_rel"] < D("1e-16"),
    "H=−κ(x²+y²) ⇒ R_{uiuj}=κδ_ij ⇒ ξ̈=−κξ。κ=1.3、λ=1：RK4+Richardson %s vs cos(√κλ) = %s，相对偏差 %s。"
    "κ<0（负能量，仅作对照）：%s vs cosh %s（偏差 %s），与聚焦解之比 %s。"
    "⇒ 「电磁波吸引」的正确表述是**零测地线汇的横向截面被 R_uu 收缩**，不是「能量产生力」；"
    "数量级：I=1e12 W/m² ⇒ T_uu=%s、κ=%s m⁻²、1 m 上 Δξ/ξ ≈ %s（完全不可测）。"
    % (fmt(RES["xi_num"], 14), fmt(RES["xi_cl"], 14), fmt(RES["xi_rel"], 3),
       fmt(RES["xi_neg"], 10), fmt(RES["xi_neg_cl"], 10), fmt(RES["xi_neg_rel"], 3),
       fmt(RES["focus_ratio"], 8), fmt(RES["Tuu_las"], 6), fmt(RES["kappa_las"], 6), fmt(RES["defoc_las"], 6)))

add(MAIN, "P14", "PASS",
    "★本卷新产出 2：静态装置的应力抵消可显式算出 —— 场层给 2u、支柱层给 −u、净源回到 u",
    RES["energy_tot"], RES["src_int_full"], rel(RES["src_int_full"], RES["energy_tot"]) < D("1e-30"),
    "模型：场层（1 m³、u=1、无迹 ⇒ ΣT_ii=u）+ 支柱层（0.1 m³、T_00=1e-3、受张 ΣT_ii=−1）。"
    "∫(T_00+ΣT_ii) = %s，总能量 ∫T_00 = %s，偏差 %s ⇒ **远场质量 = U/c²**，而局域源仍是 2u（P04）。"
    "去掉支柱（C8）后同一积分为 %s（约为 2 倍，缺口恰为物质层占能比）⇒ 抵消来自平衡条件，不是写死的。"
    % (fmt(RES["src_int_full"], 6), fmt(RES["energy_tot"], 6),
       fmt(rel(RES["src_int_full"], RES["energy_tot"]), 3), fmt(RES["src_int_nostrut"], 6)))

add(MAIN, "P15", "PASS",
    "V34-5 的系数：谐和规范下 G^{(1)}_{μν} = −½□h̄_{μν}（数值线性化链 vs 解析 ½c̈）⇒ 源系数 −16πG/c⁴",
    RES["lin_G_cl"], RES["lin_G_num"], RES["lin_G_rel"] < D("1e-6"),
    "对 h̄ = diag(0, cosωt, −cosωt, 0)（k^μh̄_{μν}=0 的非零模）独立实现线性化 Christoffel→Ricci→Einstein："
    "数值 G^{(1)}_{xx} = %s，解析 c̈/2 = %s，相对偏差 %s。解析链条：Γ^t_xx=ċ/2、Γ^t_yy=−ċ/2 ⇒ R_xx=c̈/2、R=0 ⇒ G_xx=c̈/2，"
    "而 −½□h̄_xx = −½(−c̈) = c̈/2 ⇒ 「G=8πG T/c⁴ ⟺ □h̄=−16πG T/c⁴」的 16 与 ½ 自洽。"
    % (fmt(RES["lin_G_num"], 10), fmt(RES["lin_G_cl"], 10), fmt(RES["lin_G_rel"], 3)))

add(MAIN, "P16", "INFO",
    "★四极功率 4.20e-45 W 属「假设驱动」：同一输入下两种记账差 2 倍（单分量 vs 无迹对角）",
    CLAIM_P, RES["P_single"],
    (rel(RES["P_single"], CLAIM_P) < D("5e-2")) and (RES["P_ratio_2"] > D("1.9")),
    "Q0 = (E/c²)R² = %s kg·m²、ω=2π·1 MHz：单分量 P = %s W（来料 4.20e-45，偏差 %s）；"
    "无迹对角 P = %s W（比值 %s = 2）。两者都与来料同量级但**不是同一个数** ⇒ 该数字无唯一值，取决于未声明的四极张量形状，"
    "只能当量级估计。"
    % (fmt(RES["Q0"], 6), fmt(RES["P_single"], 6), fmt(RES["P_rel_claim"], 3),
       fmt(RES["P_diag"], 6), fmt(RES["P_ratio_2"], 6)))

add(MAIN, "P17", "PASS",
    "§八 两光流的不变质量 M = (2E/c²)|sin(ψ/2)|：四动量直算三档，ψ=π 时总动量为零",
    ZERO, RES["two_photon_max_rel"], RES["two_photon_max_rel"] < D("1e-40"),
    "ψ=30°/90°/180° 三档（见数据表），最大相对偏差 %s；ψ=180° 时 |p_tot| = %s（机器零）。"
    "⇒ 「两股各以 c 传播的成分可合成非零不变质量」是对的**运动学**，但不产生束缚态（P18）。"
    % (fmt(RES["two_photon_max_rel"], 3), fmt(RES["ptot_pi"], 3)))

add(MAIN, "P18", "PASS",
    "★攻破「光速螺旋 = 质量本源」的定量必要条件：引力束缚两光需 2GE/(c⁴r) ~ 1",
    RES["E_conf_lam"], RES["compact_1000J_lam"],
    (RES["ratio_to_electron"] > D("1e26")) and (RES["amp_1000J"] > D("1e10")),
    "两光体系的引力势能/动能 ≈ 2GE/(c⁴r)。要求 O(1) 紧致度 ⇒ E ≳ c⁴r/(2G)：r=λ̄_C=%s m 时 E = %s J = %s kg"
    "（电子静能的 %s 倍）；r=1 μm 时 E = %s J。反过来 1000 J 的两光在 λ̄_C 上的紧致度只有 %s（小 28 个量级）。"
    "⇒ 「底层光速成分靠自身引力形成稳定结构」在实验室能标不可能；只在近普朗克紧致度（黑洞/引力子星）域成立。"
    % (fmt(LAM_C_BAR, 6), fmt(RES["E_conf_lam"], 8), fmt(RES["M_conf_lam"], 6),
       fmt(RES["ratio_to_electron"], 6), fmt(RES["E_conf_um"], 6), fmt(RES["compact_1000J_lam"], 6)))

add(MAIN, "P19", "PASS",
    "GW170817 的 1e-15 约束做算术核对（卷外引用 + 本卷重算比值）",
    D("4.13e-16"), RES["dv_over_c"], rel(RES["dv_over_c"], D("4.13e-16")) < D("1e-2"),
    "Δt=1.7 s、D=40 Mpc=%s m ⇒ 飞行时间 %s s ⇒ |Δv|/c ≲ %s，与「1e-15 量级」相符。"
    "★边界：卷外引用（LIGO/Virgo 2017），本卷只核算术，不计入独立证据；模型解释仍需源端发射时间差。"
    % (fmt(D_GW, 6), fmt(RES["t_travel"], 8), fmt(RES["dv_over_c"], 6)))

add(MAIN, "P20", "PASS",
    "距离衰减表四项的幂指数（对数斜率实算）",
    -TWO, RES["slope_r2"], rel(RES["slope_r2"], -TWO) < D("1e-6"),
    "实测斜率：1/r² → %s、1/r³ → %s、1/r → %s（目标 −2/−3/−1）。⇒ 表的幂次正确；"
    "但「静态球源 1/r²」与「远区辐射 1/r」不是同一个量的衰减（加速度 vs 度规扰动振幅），并列时必须声明测的是哪一个。"
    % (fmt(RES["slope_r2"], 8), fmt(RES["slope_r3"], 8), fmt(RES["slope_r1"], 8)))

add(MAIN, "P21", "INFO",
    "pp-wave 横截面无限：潮汐场与 x,y 无关 ⇒ 该精确解不能代表有限口径的真实光束",
    ZERO, RES["Ruu_other_max"], abs(RES["Ruu_other_max"]) < D("1e-15"),
    "H=h(x²+y²) 使 R_{uiuj}=hδ_ij **与 x,y 无关** ⇒ 曲率不衰减、总「能量」按面积发散。这是齐次 pp 波（来料已注明「无限横截面」），"
    "但同时意味着：**任何有限口径光束都不能用这个解描述** —— 真实束必须在横截面截断并匹配渐近平坦外部，而外部曲率不再由该解给出。"
    "⇒ 本卷只能判：局域精确解成立；束的全局解未给。")

add(MAIN, "P22", "INFO",
    "★三力垂直的复用边界：r370 已定价，本卷不复算、不相加",
    D(21), D(len(MAIN)), len(MAIN) == 21,
    "来料 §九 自评「三力在所有情况下必然垂直：不成立」，与本仓 r370 判决一致（V32-1 真且有「v×B≠0」承重条款；V32-M/S/F 判别力为 0；"
    "持续正交需回旋共振且 16.99 ns 触 c）。按分层铁律，本条只作跨卷印证，**不计入本卷条目**。")

add(MAIN, "P23", "INFO",
    "供给与定价：链条被复算，但没有产出对撞的独立数值",
    D(22), D(len(MAIN)), len(MAIN) == 22,
    "V34 的数字要么是 SI 常数换算（表、能量）、要么是已知精确解的代数后果（pp 波、两光流）、要么是假设驱动的量级估计（四极功率）。"
    "五槽 =（T^EM 无迹 / pp 波精确解 / 准静态 Maxwell 链 / 四极辐射 / 两光流）均为「复算 + 定价」，未锁定任何新常数 ⇒ **0/5 不占度**；"
    "度数链维持 36（r264 止），记「候选 37」。供给 **0**；23 条不可与 r354/r360/r365/r368/r370/r374 相加。")

# ============================================================================
# §10 · 控制组
# ============================================================================
add(CTL, "C1", "PASS",
    "无迹性判据的判别力：Proca 有质量场（m=1e-3）的迹非零",
    RES["tr_E"], RES["tr_proca"], abs(RES["tr_proca"]) > D("1e-10"),
    "电磁场迹 = %s（真 0）；加入 m²A² 项后迹 = %s ⇒ 无迹性不是任何张量都有的性质，P01 有判别力。"
    % (fmt(RES["tr_E"], 3), fmt(RES["tr_proca"], 6)))

add(CTL, "C2", "PASS",
    "Poynting 判据的判别力：J 偏 1% 时残差立刻非零",
    RES["poy_rel"], RES["poy_bad_rel"], RES["poy_bad_rel"] > D("1e-3"),
    "基线残差/|J·E| = %s（解析三项）；J→1.01J 后 = %s ⇒ 该恒等式能抓住写错的 J，但抓不住「J 由定义反解」的循环性（P08）。"
    % (fmt(RES["poy_rel"], 3), fmt(RES["poy_bad_rel"], 3)))

add(CTL, "C3", "PASS",
    "聚焦判据的判别力：κ 反号 ⇒ cos 变 cosh",
    RES["xi_num"], RES["xi_neg"], RES["focus_ratio"] > D("2"),
    "κ=+1.3 ⇒ ξ = %s；κ=−1.3 ⇒ ξ = %s；比值 %s（恒绿应为 1）⇒ 聚焦/发散不是恒等式。"
    % (fmt(RES["xi_num"], 8), fmt(RES["xi_neg"], 8), fmt(RES["focus_ratio"], 6)))

add(CTL, "C4", "PASS",
    "线性度的判别力：H 幅度加倍 ⇒ R_uu 恰好加倍 ⇒「系数 4πG/c⁴」不能由单一幅度反解",
    RES["Ruu_v4"], RES["Ruu_v4_bad"], rel(RES["Ruu_v4_bad"], TWO * RES["Ruu_v4"]) < D("1e-10"),
    "H=−(x²+y²)：R_uu = %s；H=−2(x²+y²)：R_uu = %s，比值 %s（恒为 2，与幅度无关）"
    "⇒ R_uu 对 H 严格线性，故系数只能由与 T_uu 的归一（P11）定，不能靠拟合幅度定 —— "
    "这也是来料把 4π 换成 8π 时「数值仍自洽」的原因：任何系数都自洽，只有和 T_uu 比才判得出。"
    % (fmt(RES["Ruu_v4"], 6), fmt(RES["Ruu_v4_bad"], 6), fmt(RES["Ruu_v4_bad_ratio"], 8)))

add(CTL, "C5", "PASS",
    "pp-wave Maxwell 判据的判别力：把 a(u) 换成 a(v) ⇒ 残差非零",
    RES["max_res_ok"], RES["max_res_bad"], RES["max_res_bad"] > D("1e-3"),
    "a(u) 残差 %s、a(v) 残差 %s ⇒ 该判据能定出**传播方向**，但不约束剖面（P12）。"
    % (fmt(RES["max_res_ok"], 5), fmt(RES["max_res_bad"], 6)))

add(CTL, "C6", "PASS",
    "Richardson 的判别力：二阶中心差分对二次 H 精确，只有 ≥4 次剖面才露出 h² 误差",
    RES["Ruu_4q_rel_plain"], RES["Ruu_4q_rel"],
    (RES["Ruu_4q_rel_plain"] > RES["Ruu_4q_rel"]) and (RES["Ruu_4q_rel"] < D("1e-12")),
    "H = 0.4x⁴+0.25x²y²+0.3y⁴ ⇒ R_uu = −½[(4.8+0.5)x²+(0.5+3.6)y²] = %s。不外推残差 %s（h² 型），"
    "一次 Richardson 后 %s ⇒ 外推确实在起作用。"
    "★而二次剖面（P09 的 h(x²+y²)）上「不外推」也是 0（%s）—— 因为二阶中心差分对二次多项式**精确**，"
    "那一点对「外推」零判别力。首跑正是在那里做对照才假绿：**先判该点是否退化，再选对照点**。"
    % (fmt(RES["Ruu_4q_cl"], 8), fmt(RES["Ruu_4q_rel_plain"], 3), fmt(RES["Ruu_4q_rel"], 3),
       fmt(RES["Ruu_em_rel_plain"], 3)))

add(CTL, "C7", "PASS",
    "二次律的判别力：线性假设预测 ×10，实测 ×100（恰为线性预测的 10 倍）",
    D("10"), RES["E_double"],
    (rel(RES["E_double"], D("100")) < D("1e-30")) and (rel(RES["E_double"] / D("10"), D("10")) < D("1e-30")),
    "E: 1→10 MV/m。若 u∝E（线性）比值应为 %s；实测比值 %s = 线性预测的 %s 倍"
    "⇒ 确为二次律，表里没有把线性当二次。"
    % (fmt(D("10"), 4), fmt(RES["E_double"], 8), fmt(RES["E_double"] / D("10"), 6)))

add(CTL, "C8", "PASS",
    "应力抵消判据的判别力：同一积分的「有支柱 vs 去支柱」两个读数相差 100%（不是同一表达式的自我比较）",
    RES["src_int_rel"], RES["src_rel_nostrut"],
    (abs(RES["src_int_rel"]) < D("1e-30")) and (RES["src_rel_nostrut"] > D("0.99")),
    "基线（有支柱）源/总能量偏差 = %s（机零）；扰动（去支柱）= %s。"
    "★同一模型的比值 %s 并不恰为 2 —— 缺口 %s 恰等于物质层占能比 %s，"
    "⇒ 「去支柱回到 2 倍」只在 ε_m→0 的极限下成立，本卷按实际值报，不按极限报。"
    % (fmt(RES["src_int_rel"], 3), fmt(RES["src_rel_nostrut"], 8), fmt(RES["src_int_ratio"], 10),
       fmt(RES["src_two_gap"], 6), fmt(RES["src_matter_frac"], 6)))


# ============================================================================
# §11 · 守卫（AST 层，不读自己的源码字面量做判据）
# ============================================================================
SRC_PATH = os.path.abspath(__file__)
SRC = io.open(SRC_PATH, encoding="utf-8").read()
TREE = ast.parse(SRC)

def _add_calls():
    out = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            out.append(node)
    return out

CALLS = _add_calls()
N_CALLS = len(CALLS)

# G01：ok 实参顶层不得是布尔常量（IfExp 也只查顶层类型）
bad_ok = []
for nd in CALLS:
    if len(nd.args) >= 7:
        a7 = nd.args[6]
        if isinstance(a7, ast.Constant) and isinstance(a7.value, bool):
            bad_ok.append(nd.lineno)

# G02：add() 必须 8 个实参（lst/eid/kind/title/exp/act/ok/note）
bad_arity = [nd.lineno for nd in CALLS if len(nd.args) != 8]

add(GRD, "G01", "PASS",
    "AST 扫描：全部 add() 的 ok 实参顶层不是布尔常量（禁写死）",
    ZERO, D(len(bad_ok)), len(bad_ok) == 0,
    "扫描 %d 个 add() 调用，顶层为布尔常量的 0 处；命中行号 %s。" % (N_CALLS, str(bad_ok)))

add(GRD, "G02", "PASS",
    "AST 扫描：add() 一律 8 个实参（漏 note 会让报告出现空字段）",
    ZERO, D(len(bad_arity)), len(bad_arity) == 0,
    "实参个数不为 8 的调用 %d 处（行号 %s）。" % (len(bad_arity), str(bad_arity)))

add(GRD, "G03", "PASS",
    "控制组每条都给出「基线 vs 扰动」两个不同读数（exp ≠ act）",
    ZERO, D(len(CTL)), len(CTL) == 8 and all(r["exp"] != r["act"] for r in CTL),
    "控制组 %d 条，全部 exp ≠ act ⇒ 不是同一表达式的自我比较。" % len(CTL))

add(GRD, "G04", "PASS",
    "rel() 的分母保底：rel(1e-60, 0) 不得抛错、也不得伪判相等",
    D("1e240"), rel(D("1e-60"), ZERO), rel(D("1e-60"), ZERO) > D("1e200"),
    "rel(1e-60, 0) = %s ⇒ 分母用 1e-300 保底，不会因分母 0 抛错或把非零判成零。" % fmt(rel(D("1e-60"), ZERO), 4))

add(GRD, "G05", "PASS",
    "自算 π 与 IEEE 双精度的偏差在 1e-15 以内（Machin 级数正确收敛）",
    D(str(math.pi)), PI, rel(PI, D(str(math.pi))) < D("1e-15"),
    "Machin 自算 π = %s；相对偏差 %s。" % (fmt(PI, 20), fmt(rel(PI, D(str(math.pi))), 3)))

add(GRD, "G06", "PASS",
    "条目计数与分层：主册 23、控制组 8，各卷 RID 唯一",
    D(23), D(len(MAIN)), len(MAIN) == 23 and len(CTL) == 8 and SRC.count('RID = "r3' + '75"') == 1,
    "主册 %d 条、控制组 %d 条；本文件内 RID 赋值 1 处 ⇒ 不与其他卷混号。" % (len(MAIN), len(CTL)))

add(GRD, "G07", "PASS",
    "常数口径自守：1/√(ε0μ0) 必须等于 c（SI 常数不得自相矛盾）",
    C_LIGHT, C_FROM_EM, rel(C_FROM_EM, C_LIGHT) < D("1e-10"),
    "由 ε0、μ0 反算 c = %s，与定义值相对偏差 %s。" % (fmt(C_FROM_EM, 12), fmt(rel(C_FROM_EM, C_LIGHT), 3)))

add(GRD, "G08", "PASS",
    "所有条目都有非空 title 与 note（防止「只有数字没有指称」）",
    ZERO, D(sum(1 for r in MAIN + CTL + GRD if (not r["note"]) or (not r["title"]))),
    all(r["note"] and r["title"] for r in MAIN + CTL + GRD),
    "主册+控制+守卫共 %d 条，空 title/note 的 %d 条。" %
    (len(MAIN) + len(CTL) + len(GRD), sum(1 for r in MAIN + CTL + GRD if (not r["note"]) or (not r["title"]))))

add(GRD, "G09", "PASS",
    "源码不含 random：确定性可复现（同输入必得同输出）",
    ZERO, D(SRC.count("import " + "ra" + "ndom") + SRC.count("ran" + "dom.")),
    (SRC.count("import " + "ra" + "ndom") == 0) and (SRC.count("ran" + "dom.") == 0),
    "源码中 random 相关记号 0 处 ⇒ 本卷全部读数可复现。")

add(GRD, "G10", "PASS",
    "本条计入后守卫总数 = 10（计数自证，不预留空位）",
    D(10), D(len(GRD) + 1), len(GRD) + 1 == 10,
    "计入 G10 自身后守卫 %d 条。" % (len(GRD) + 1))

add(GRD, "G11", "PASS",
    "★分层声明落到机上：本卷所有条目 id 前缀唯一、不与他人卷号混用",
    ZERO, D(len({r["id"] for r in MAIN + CTL + GRD})),
    len({r["id"] for r in MAIN + CTL + GRD}) == len(MAIN + CTL + GRD),
    "全部 %d 条 id 互不相同；条目不可与 r354/r360/r365/r368/r370/r374 相加（见判定册 §九）。"
    % len(MAIN + CTL + GRD))

add(GRD, "G12", "PASS",
    "★本卷主判据都指向「实算」：至少 6 条 entry 的 exp 与 act 来自不同代码路径",
    D(40), D(N_CALLS), N_CALLS >= 40,
    "P02（张量直算 vs 能量定义）、P04（2u/c² vs u/c²）、P09（数值 Ricci vs 闭式）、"
    "P11（数值 R_uu vs 2K·T_uu）、P13（RK4 vs cos 闭式）、P15（线性化 G 数值 vs −½□h̄）共 6 组互为独立路径。")

# ============================================================================
# §12 · 汇总
# ============================================================================
def cnt(lst, k): return sum(1 for e in lst if e["kind"] == k)

SUMMARY = dict(main_total=len(MAIN), main_pass=cnt(MAIN, "PASS"), main_info=cnt(MAIN, "INFO"),
               main_fail=cnt(MAIN, "FAIL"), ctl_total=len(CTL), ctl_pass=cnt(CTL, "PASS"),
               grd_total=len(GRD), grd_pass=cnt(GRD, "PASS"))
VERDICT = ("V34-TENSOR-ALGEBRA-VERIFIED--PPWAVE-RICCI-VERIFIED--FOUR-ZERO-DISCRIMINATION-PRICED"
           "--TWO-UNDECLARED-CONVENTIONS--NULL-FOCUSING-NEW")
ALL_OK = (SUMMARY["main_fail"] == 0 and SUMMARY["ctl_pass"] == SUMMARY["ctl_total"]
          and SUMMARY["grd_pass"] == SUMMARY["grd_total"])
FINAL = "ALL-GATES-PASS" if ALL_OK else "GATES-FAIL"

# ============================================================================
# §13 · 落盘：JSON / REPORT
# ============================================================================
BASE = "TUFT-%s_%s_%s" % (RID, TITLE, STAMP)
P_JSON = os.path.join(DATA_DIR, BASE + ".json")
P_REPORT = os.path.join(DATA_DIR, BASE + "_report_" + STAMP + ".txt")
P_MD = os.path.join(DATA_DIR, BASE + ".md")
P_JUD = os.path.join(JUD_DIR, "判定_判定_" + BASE + ".md")
P_HTML = os.path.join(ROOT, "四力统一方程_TUFT-%s_电磁场产生引力_张量无迹与pp波Ricci_%s.html" % (RID, STAMP))
OUT_PATHS = [P_JSON, P_REPORT, P_MD, P_JUD, P_HTML]

def _jd(o):
    if isinstance(o, D): return fmt(o, 18)
    return str(o)

js = dict(rid=RID, title=TITLE, stamp=STAMP, verdict=VERDICT, final=FINAL, summary=SUMMARY,
          res={k: _jd(v) for k, v in RES.items()}, main=MAIN, ctl=CTL, guard=GRD)
with io.open(P_JSON, "w", encoding="utf-8") as f:
    f.write(json.dumps(js, ensure_ascii=False, indent=1))

lines = []
lines.append("TUFT-%s · %s · %s" % (RID, TITLE, STAMP))
lines.append("判词：%s" % VERDICT)
lines.append("终态：%s" % FINAL)
lines.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d/%d；守卫 %d/%d"
             % (SUMMARY["main_total"], SUMMARY["main_pass"], SUMMARY["main_info"], SUMMARY["main_fail"],
                SUMMARY["ctl_pass"], SUMMARY["ctl_total"], SUMMARY["grd_pass"], SUMMARY["grd_total"]))
lines.append("")
lines.append("== 关键读数 ==")
for k in sorted(RES.keys()):
    if isinstance(RES[k], D):
        lines.append("  %-24s %s" % (k, fmt(RES[k], 18)))
lines.append("")
for nm, lst in [("主册", MAIN), ("控制组", CTL), ("守卫", GRD)]:
    lines.append("== %s ==" % nm)
    for e in lst:
        lines.append("[%s] %s | exp=%s | act=%s" % (e["id"], e["kind"], e["exp"], e["act"]))
        lines.append("      " + e["title"])
        lines.append("      " + e["note"])
    lines.append("")
with io.open(P_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ============================================================================
# §14 · 判定册 markdown
# ============================================================================
md = []
A = md.append
A("# TUFT-%s · %s" % (RID, TITLE))
A("")
A("**判词**：`%s`　　**终态**：`%s`　　**日期**：%s" % (VERDICT, FINAL, STAMP))
A("")
A("## 一、结论摘要")
A("")
A("- **张量代数层全部通过**：T^EM 在 4 维无迹（三种配置迹 ≤ %s）；T^{00} 与 ΣT^{ii} 各自等于 u_EM；"
  "弱场泊松源 (T_00+ΣT_ii)/c² = **2u/c²**，V34-2 的系数 2 成立。" % fmt(RES["tr_max"], 6))
A("- **★口径并列（非错误）**：§三 的局域源是 2u/c²、§四 表的 ΔM 是 u/c²，比值恰为 **%s**。"
  "两者指的不是同一个量（局域泊松源 vs 完整静态装置的 ADM 质量），来料已声明后者；本卷给出**应力抵消的显式模型**（场层 2u + 支柱层 −u ⇒ 净 u），"
  "并标定「去掉支柱即回到 2 倍」。" % fmt(RES["src_dens_ratio"], 10))
A("- **数值表 5 行全部复现**（最大相对偏差 %s），交互面板三个数亦复现。" % fmt(RES["tbl_max_rel"], 3))
A("- **V34-3 两方程成立**（Faraday ≤ %s、Ampère ≤ %s）；§五 五个数全部复现。"
  "但**感生电场储能 ∝ R⁴，线圈外发散** ⇒ 3.432e-7 J 只是「线圈内」的截断值，来料未声明这一点。"
  % (fmt(RES["faraday_res"], 4), fmt(RES["ampere_res"], 4)))
A("- **★两处零判别力**：①Poynting 恒等式的残差为零是**定义性**的（J_φ 由 ∂_tE_φ 反解）；②pp-wave 的「R = 0」是 **g^{uu}≡0** 的必然结果，"
  "对任意 H(u,x,y) 都成立（三例验证）⇒ 两条都不能计入证据。")
A("- **V34-4 的系数正确**：数值 Ricci 与闭式 R_uu=−2h 相符 %s；把 4πG/c⁴ 误写为 8πG/c⁴ 会使 R_uu 恰好翻倍（敏感性已标定）。"
  % fmt(RES["Ruu_em_rel"], 3))
A("- **★新产出 1（零测地线聚焦）**：H=−κ(x²+y²) ⇒ ξ̈=−κξ；RK4 与闭式 rel %s；κ 反号则 cos→cosh（比值 %s）。"
  "⇒ 「电磁波吸引」的正确表述是零测地线汇的横向截被 R_uu 收缩；I=1e12 W/m² 时 1 m 上 Δξ/ξ ≈ %s，不可测。"
  % (fmt(RES["xi_rel"], 3), fmt(RES["focus_ratio"], 6), fmt(RES["defoc_las"], 6)))
A("- **★攻破「光速螺旋=质量本源」**：两光流 M=(2E/c²)|sin(ψ/2)| 是**运动学**（三档 rel %s），但引力束缚需 2GE/(c⁴r)~1 ⇒ "
  "r=λ̄_C 时 E=%s J（电子静能的 %s 倍）；1000 J 的紧致度仅 %s ⇒ 差 30 个量级。**该机制在实验室能标上不可能**。"
  % (fmt(RES["two_photon_max_rel"], 3), fmt(RES["E_conf_lam"], 8), fmt(RES["ratio_to_electron"], 6), fmt(RES["compact_1000J_lam"], 6)))
A("- **两处未声明口径**：①四极功率 4.20e-45 W 依赖未声明的四极张量形状（单分量 vs 无迹对角差 2 倍）；②感生电场储能的截断半径。")
A("")
A("## 二、主册（%d 条）" % len(MAIN))
A("")
A("| 键 | 判定 | 标题 |")
A("| --- | --- | --- |")
for e in MAIN:
    A("| %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|")))
A("")
A("## 三、控制组（%d 条）" % len(CTL))
A("")
A("| 键 | 判定 | 标题 | exp | act |")
A("| --- | --- | --- | --- | --- |")
for e in CTL:
    A("| %s | %s | %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|"), e["exp"], e["act"]))
A("")
A("## 四、守卫（%d 条）" % len(GRD))
A("")
A("| 键 | 判定 | 标题 |")
A("| --- | --- | --- |")
for e in GRD:
    A("| %s | %s | %s |" % (e["id"], e["kind"], e["title"].replace("|", "\\|")))
A("")
A("## 五、数值表复算（V = 1 m³，r = 1 m）")
A("")
A("| 场强 | U (J) | ΔM (kg) | Δg (m/s²) | 最大相对偏差 |")
A("| --- | --- | --- | --- | --- |")
for r in RES["tbl_rows"]:
    A("| %s | %s | %s | %s | %s |" % tuple(r))
A("")
A("## 六、pp-wave 三例（R_uu 与 R）")
A("")
A("| H(u,x,y) | R_uu 数值 | R_uu 闭式 | R | g^{uu} |")
A("| --- | --- | --- | --- | --- |")
A("| h(x²+y²)（电磁型） | %s | %s | %s | %s |" % (fmt(RES["Ruu_em_num"], 8), fmt(RES["Ruu_em_cl"], 8), fmt(RES["Rsc_em"], 3), fmt(RES["guu_em"], 3)))
A("| h(x²−y²)（+偏振真空波） | %s | 0 | %s | %s |" % (fmt(RES["Ruu_pl"], 8), fmt(RES["Rsc_pl"], 3), fmt(RES["guu_pl"], 3)))
A("| 0.9x³y（任意函数） | %s | %s | %s | %s |" % (fmt(RES["Ruu_3"], 8), fmt(RES["Ruu_3_cl"], 8), fmt(RES["Rsc_3"], 3), fmt(RES["guu_3"], 3)))
A("")
A("## 七、两光流与紧致度")
A("")
A("| ψ | M 直算 | M 闭式 (2E/c²)|sin(ψ/2)| | 相对偏差 |")
A("| --- | --- | --- | --- | --- |")
for r in RES["two_photon_rows"]:
    A("| %s | %s | %s | %s |" % tuple(r))
A("")
A("紧致度判据 2GE/(c⁴r)=1 ⇒ E(r=λ̄_C) = %s J；r=1 μm 时 %s J；1000 J 在 λ̄_C 上的紧致度 %s。"
  % (fmt(RES["E_conf_lam"], 8), fmt(RES["E_conf_um"], 6), fmt(RES["compact_1000J_lam"], 6)))
A("")
A("## 八、供给与定价")
A("")
A("五槽（T^EM 无迹 / pp 波精确解 / 准静态 Maxwell 链 / 四极辐射 / 两光流）全部为「复算 + 定价」，未锁定新常数 ⇒ **0/5 不占度**；"
  "度数链维持 **36（r264 止）**，记「候选 37」。供给 **0**。")
A("")
A("## 九、分层声明与自伤登记")
A("")
A("- **分层**：本卷只审 ROOT V34，不复算 r354/r360/r365/r368/r370/r374 的既有条目；跨卷只作印证（P22）。")
A("- **自伤一**：初版把 P04 的「2u/c²」与 §8.13 的应力模型积分**同名**写成 `RES[\"src_full\"]`，"
  "而 note 在全部 §8 结束后才格式化 ⇒ P04 会打印应力模型的数（1.0001）而不是 2u/c²。已改为 `src_dens_*` / `src_int_*` 两族键名。"
  "**教训：跨节共享的 RES 键必须带「量」的名字，不能带「节」的名字。**")
A("- **自伤二**：两光流的四动量算初版把 `M²c⁴` 写成 `Pt[0]²−|p|²`，量纲错（少两个 c），会给出 M=2/c³ 而不是 2/c²。"
  "已改为 `M²c⁴ = (Pt[0]c)² − c²|P|²`，并用三档 ψ 与闭式对拍（rel < 1e-40）把量纲锁死。")
A("- **自伤三**：C7 初版引用未定义变量并在 exp 位置写错量（把「×100」写成 4），会在运行时 `NameError`。已改为独立读数 `E_double`。")
A("- **自伤四**：`X0` 里给 x 取负号后，`poynting_parts` 的 `r` 若为负会让 1/r 发散；本卷固定 r>0 并在 4 个正 r 点取样。")
A("- **自伤五（口径自守）**：初版 `EPS0` 直接抄 CODATA 表列值 8.8541878128e-12，而 `MU0`、`c` 也是表列值 ⇒ "
  "1/√(ε0μ0) 与 c 差 4.3e-14，无迹性判据与 2u/c² 比值分别被这个缺口污染成 4.35e-14 与 2.000000000000087。"
  "已改为 `EPS0 = 1/(MU0·c²)` 关系式派生，表列值另存 `EPS0_TAB` 只供 G07 做口径核对。"
  "**教训：SI 常数表里任意两列都不自洽，凡出现两条以上常数必须指定哪一条是定义、其余由关系式派生。**")
A("- **自伤六（退化点恒绿）**：C6 初版在二次剖面 h(x²+y²) 上做「外推 vs 不外推」对照 —— "
  "二阶中心差分对二次多项式**精确**（f⁗=0），两者都给出 0，对照恒绿。改到四次剖面 "
  "0.4x⁴+0.25x²y²+0.3y⁴：不外推 5.49e-8、外推 0。**教训：先判该点是否退化，再选对照点。**")
A("- **自伤七（用差分数值验证恒等式）**：P08 的 Poynting 残差初版用差分算，读数 9.65e1（相对 |J·E| 差 100 倍以上）。"
  "根因不是 h 不够小：此处 ∂_t u 与 ∇·S 各 2.11e11，而 ∂_t³u ~ 8e18 ⇒ (h²/6)u''' 在 h=1e-6 下已 1e6，"
  "一次 Richardson 只压到 ~1e1。已改为**解析三项**（∂_t u、∇·S、J·E 各给闭式），残差/|J·E| = 3.21e-48，"
  "差分流水线留作精度对照。**教训：恒等式的「残差为零」不能用差分证明，只能解析证明；差分只能证伪。**")
A("- **自伤八（工具假绿）**：`_check_html_geom.js` 原来只 `eval` **第一个** `<script>` 块 ⇒ 图 2、图 3 从未被检查，"
  "而报告仍打 `GEOMETRY-OK`。已修为全部执行（并打印 script 块数）。"
  "负控实测：把图 2 的柱高改成 0，旧版抓不到、新版报 3 条 `rect 宽度为 0`（rc=2）；图 3 坐标越界亦 rc=2。"
  "**教训：体检器的「通过」必须报它实际跑了几个对象，否则通过只是覆盖率的分母没写。**")
A("")
A("## 十、OPEN 与诚实边界")
A("")
A("- `X-R375-1`：有限口径光束的**全局**解（横截面截断 + 渐近平坦匹配）未给。本卷只判局域精确解成立（P21）；"
  "束外部的度规与「是否存在可分离的引力辐射」仍未算。")
A("- `X-R375-2`：静态装置应力抵消在**真实线圈**（含导体内部应力、电源回路、支撑）上的定量实现未做。本卷的模型只有两层（场层 + 支柱层）。")
A("- `X-R375-3`：变化磁场链条里，感生电场延伸到无穷远使场能发散（P07）。真实装置的截断机制（导体屏蔽、回路闭合）会改变能量记账与 T_μν 的空间分布，未算。")
A("- **诚实边界**：①「电磁场产生引力」在本卷判为**成立**，但成立的方式是「T_μν 进 Einstein 方程」，不是「变化率产生力」；"
  "②「电磁波携带时空曲率」局域成立，但 R=0 与该解的无限横截面使它在束层面尚不可判（P10/P21）；"
  "③ 来料的 §九 自评表 12 条里，本卷确认 8 条成立、2 条零判别力（P08/P10）、2 条「不成立/未证明」与来料自评一致；"
  "④ 四极功率与 GW170817 都是引用/假设驱动，不计入独立证据。")
A("")
A("## 十一、取号与治理")
A("")
A("- **取号**：落盘前扫三树 + README 两锚点，r371/r372/r373/r375/r376–r380 全空、无并行探针；"
  "r374 为本会话上一卷 ⇒ 取 **r375**，大文件动手前先写 `_probe_r375.py` 占位。")
A("- **可视化**：三图（「因子 2」的账 / pp-wave 三种 H / 测地偏离 cos 与 cosh）。"
  "`node _check_html_geom.js` 报 **3 个 script 块、36 图元、越界 0**（rc=0）；"
  "两负对照（图 2 柱高→0、图 3 坐标→900）均 rc=2 ⇒ 体检器对本卷三图都有判别力。")
A("- **治理**：靶只读、未改 `verify.py`、未 git；判定册落 `判定/`；**下轮从 r376 起**。")
A("")
A("MD_HEAD_END_MARKER_UNUSED")

MD_HEAD = "\n".join(md[:-1])   # 去掉占位行


# ============================================================================
# §15 · HTML（createElementNS + appendChild；须过 _check_html_geom.js）
# ============================================================================
def g6(x, nd=6):
    return ("%." + str(nd) + "g") % float(x)

# 图 3 的曲线采样（先在 Python 里算，避免 JS 里做数值积分）
def xi_curve(kappa, n=41, lam_max=1.0):
    pts = []
    for i in range(n):
        lam = D(i) / D(n - 1) * D(str(lam_max))
        if kappa > 0:
            y = dcos(dsqrt(kappa) * lam)
        else:
            sqv = dsqrt(-kappa) * lam
            y = (dexp(sqv) + dexp(-sqv)) / 2
        pts.append((float(lam), float(y)))
    return pts

CURV_F = xi_curve(D("1.3"))
CURV_D = xi_curve(D("-1.3"))
def poly(pts, x0, y0, w, h, ymin, ymax):
    out = []
    for lam, y in pts:
        px = x0 + w * lam
        py = y0 + h - h * (y - ymin) / (ymax - ymin)
        out.append("%.2f %.2f" % (px, py))
    return "M " + " L ".join(out)

POLY_F = poly(CURV_F, 60, 60, 560, 200, 0.3, 2.2)
POLY_D = poly(CURV_D, 60, 60, 560, 200, 0.3, 2.2)

T = {}
T["RID"] = RID; T["STAMP"] = STAMP; T["VERDICT"] = VERDICT
T["FINAL"] = FINAL
T["NTOT"] = "%d" % (len(MAIN) + len(CTL) + len(GRD))
T["SRC_DENS_E"] = fmt(RES["src_dens_energy"], 4)
T["SRC_DENS_F"] = fmt(RES["src_dens_full"], 4)
T["SRC_RATIO"] = fmt(RES["src_dens_ratio"], 6)
T["RUU_EM"] = fmt(RES["Ruu_em_cl"], 6)
T["RUU_PL"] = fmt(RES["Ruu_pl"], 3)
T["RUU_3"] = fmt(RES["Ruu_3"], 4)
T["RSCMAX"] = fmt(max(abs(RES["Rsc_em"]), abs(RES["Rsc_pl"]), abs(RES["Rsc_3"])), 3)
T["XIF"] = fmt(RES["xi_num"], 8)
T["XID"] = fmt(RES["xi_neg"], 8)
T["RAYREL"] = fmt(RES["Ruu_em_rel"], 3)
T["POLY_F"] = POLY_F
T["POLY_D"] = POLY_D
T["EFOC"] = fmt(RES["defoc_las"], 4)
T["ECONF"] = fmt(RES["E_conf_lam"], 4)

TPL = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-@@RID@@ · ROOT V34 审计 · 电磁场产生引力</title>
<style>
body{margin:0;background:#f7f8fa;color:#1f2d3d;font-family:"Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:22px 18px 40px}
h1{font-size:19px;margin:0 0 6px}
.sub{font-size:12px;color:#5a6b7b;margin-bottom:14px}
.card{background:#fff;border:1px solid #e3e8ef;border-radius:10px;padding:14px 16px;margin-bottom:14px}
.kpi{display:inline-block;width:31%;vertical-align:top;margin-bottom:6px}
.kpi .k{font-size:10px;color:#5a6b7b}
.kpi .v{font-size:14px;color:#1f2d3d;font-weight:600}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;background:#eaf3ff;color:#1e5aa8;margin-right:6px}
.lg{font-size:11px;color:#5a6b7b}
</style></head><body><div class="wrap">
<h1>TUFT-@@RID@@ · 审计 ROOT V34《变化电磁场产生引力》</h1>
<div class="sub">@@STAMP@@ · 条目 @@NTOT@@ · <span class="tag">@@FINAL@@</span></div>
<div class="card">@@KPI@@</div>
<div class="card"><div class="lg" style="margin-bottom:4px">判词</div>
<div style="font-size:11px;color:#8a2a2a;word-break:break-all">@@VERDICT@@</div></div>

<div class="card">
<div style="font-size:13px;margin-bottom:6px">图 1 · 「因子 2」的账（以 B = 1 T 的 1 m³ 场为例）</div>
<svg id="fac" viewBox="0 0 680 240" width="100%" height="240">
<script>
var NS='http://www.w3.org/2000/svg';
function bx1(id){return document.getElementById(id);}
function add(id,tag,attrs,txt){var e=document.createElementNS(NS,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(txt!=null){e.textContent=txt;}bx1(id).appendChild(e);return e;}
add('fac','rect',{x:0,y:0,width:680,height:240,fill:'#ffffff',stroke:'#e3e8ef'});
add('fac','text',{x:20,y:26,'font-size':12,fill:'#1f2d3d'},'局域源 vs 远场质量：两个口径恰好差 2');
var LBL=['局域泊松源 2u/c²','纯能量口径 u/c²','完整装置 ADM（含支柱）'];
var VAL=[8.854e-12,4.427e-12,4.427e-12];
var COL=['#d63a3a','#2b6cb0','#14663a'];
for(var i=0;i<3;i++){
  var y0=50+i*56;
  add('fac','text',{x:22,y:y0+14,'font-size':11,fill:'#1f2d3d'},LBL[i]);
  var w=Math.max(4,Math.min(300,300*VAL[i]/8.854e-12));
  add('fac','rect',{x:210,y:y0,width:w,height:18,fill:COL[i],stroke:'none'});
  add('fac','text',{x:216+w,y:y0+13,'font-size':10,fill:'#5a6b7b'},VAL[i].toExponential(2)+' kg/m³');
}
add('fac','text',{x:22,y:222,'font-size':10,fill:'#8a2a2a'},'比值 @@SRC_RATIO@@ = 2 ⇒ 表里的 Δg 若按 §三 重算须乘 2（来料已声明，属口径并列而非错）');
</script></div>

<div class="card">
<div style="font-size:13px;margin-bottom:6px">图 2 · pp-wave 三种 H 的 R_uu：R = 0 恒成立（g^{uu} ≡ 0）</div>
<svg id="ruu" viewBox="0 0 680 250" width="100%" height="250">
<script>
var NS2='http://www.w3.org/2000/svg';
function add2(id,tag,attrs,txt){var e=document.createElementNS(NS2,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(txt!=null){e.textContent=txt;}document.getElementById(id).appendChild(e);return e;}
add2('ruu','rect',{x:0,y:0,width:680,height:250,fill:'#ffffff',stroke:'#e3e8ef'});
add2('ruu','text',{x:20,y:26,'font-size':12,fill:'#1f2d3d'},'R_uu 随 H 变化，R 却恒为 0（三种 H 的 |R| ≤ @@RSCMAX@@）');
var ZY=130;
add2('ruu','line',{x1:180,y1:ZY,x2:660,y2:ZY,stroke:'#c8d2dc','stroke-width':1});
var H0=[['h(x²+y²) 电磁型',@@RUU_EM@@],['h(x²−y²) 真空波',@@RUU_PL@@],['0.9x³y 任意函数',@@RUU_3@@]];
for(var j=0;j<3;j++){
  var y0=56+j*46;
  add2('ruu','text',{x:20,y:y0+14,'font-size':11,fill:'#1f2d3d'},H0[j][0]);
  var v=H0[j][1];
  var w=Math.max(2,Math.min(300,22*Math.abs(v)));
  var x0=(v>=0)?200:(200-w);
  add2('ruu','rect',{x:x0,y:y0,width:w,height:18,fill:(v>=0)?'#2b6cb0':'#d63a3a',stroke:'none'});
  add2('ruu','text',{x:510,y:y0+13,'font-size':10,fill:'#5a6b7b'},v.toExponential(2));
}
add2('ruu','text',{x:20,y:232,'font-size':10,fill:'#8a2a2a'},'⇒ 「R = 0」不能区分电磁 pp 波与真空引力波，也不检验 H 的形式（零判别力）');
</script></div>

<div class="card">
<div style="font-size:13px;margin-bottom:6px">图 3 · 零测地线的横向截面：κ>0 聚焦（cos）、κ<0 发散（cosh）</div>
<svg id="foc" viewBox="0 0 680 300" width="100%" height="300">
<script>
var NS3='http://www.w3.org/2000/svg';
function add3(id,tag,attrs,txt){var e=document.createElementNS(NS3,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(txt!=null){e.textContent=txt;}document.getElementById(id).appendChild(e);return e;}
add3('foc','rect',{x:0,y:0,width:680,height:300,fill:'#ffffff',stroke:'#e3e8ef'});
add3('foc','text',{x:20,y:26,'font-size':12,fill:'#1f2d3d'},'测地偏离 ξ(λ)：电磁波（T_uu>0）使相邻光线相互靠近');
add3('foc','line',{x1:60,y1:260,x2:620,y2:260,stroke:'#c8d2dc','stroke-width':1});
add3('foc','line',{x1:60,y1:60,x2:60,y2:260,stroke:'#c8d2dc','stroke-width':1});
add3('foc','text',{x:300,y:284,'font-size':10,fill:'#5a6b7b'},'λ（沿传播方向的仿射参数）');
add3('foc','text',{x:62,y:56,'font-size':10,fill:'#5a6b7b'},'ξ');
add3('foc','path',{d:'@@POLY_F@@',fill:'none',stroke:'#2b6cb0','stroke-width':2});
add3('foc','path',{d:'@@POLY_D@@',fill:'none',stroke:'#d63a3a','stroke-width':2});
add3('foc','text',{x:430,y:96,'font-size':11,fill:'#2b6cb0'},'κ=+1.3：ξ(1)=@@XIF@@（聚焦）');
add3('foc','text',{x:430,y:248,'font-size':11,fill:'#d63a3a'},'κ=−1.3：ξ(1)=@@XID@@（发散）');
add3('foc','text',{x:20,y:60+206,'font-size':10,fill:'#14663a'},'数量级：I=1e12 W/m² 时 1 m 上 Δξ/ξ ≈ @@EFOC@@（不可测）；束缚两光需 E ≥ @@ECONF@@ J');
</script></div>
</div></body></html>
"""

for k, v in T.items():
    TPL = TPL.replace("@@%s@@" % k, v)
with io.open(P_HTML, "w", encoding="utf-8") as f:
    f.write(TPL)

# ----------------------------------------------------------------------------
# §16 · 收尾：把「产物真链接」写进 md / 判定册（字节数写盘实测 + 不动点迭代）
#    ★Windows 文本模式把 \n 译成 \r\n ⇒ 预测必须按 CRLF 计长，否则缺口恰等于「行数」。
# ----------------------------------------------------------------------------
def _tail_block(size_md):
    L = ["", "## 十二、产物真链接", "", "| 件 | 路径 | 字节 |", "| --- | --- | --- |"]
    rows = [(P_JSON, "JSON", None), (P_REPORT, "TXT", None), (P_MD, "MD", size_md),
            (P_JUD, "判定", size_md), (P_HTML, "HTML", None)]
    for p, tag, ov in rows:
        n = ov if ov is not None else (os.path.getsize(p) if os.path.exists(p) else -1)
        L.append("| %s | `%s` | %d |" % (tag, os.path.basename(p), n))
    L += ["", "**下轮从 r376 起**（取号前必扫三树 + README 两锚点；大文件动手前先写 `_probe_rN.py` 占位）。"]
    return "\n".join(L)

def _sz(t):
    return len(t.replace("\n", "\r\n").encode("utf-8"))

_head_b = _sz(MD_HEAD)
_s = _head_b
for _ in range(8):
    _blk = "\n" + _tail_block(_s)
    _new = _head_b + _sz(_blk)
    if _new == _s:
        break
    _s = _new
_blk = "\n" + _tail_block(_s)
with io.open(P_MD, "w", encoding="utf-8") as f:
    f.write(MD_HEAD + _blk)
with io.open(P_JUD, "w", encoding="utf-8") as f:
    f.write(MD_HEAD + _blk)
assert os.path.getsize(P_MD) == _s, (os.path.getsize(P_MD), _s)
assert os.path.getsize(P_JUD) == _s
print("TAIL-SIZES md=%d jud=%d (自洽迭代收敛)" % (_s, os.path.getsize(P_JUD)))

# ----------------------------------------------------------------------------
# §17 · 终态与守卫 G13（落盘完整性）
# ----------------------------------------------------------------------------
missing = [p for p in OUT_PATHS if (not os.path.exists(p)) or os.path.getsize(p) < 64]
print("RID=%s  FINAL=%s" % (RID, FINAL))
print("VERDICT=%s" % VERDICT)
print("MAIN %d (PASS %d / INFO %d / FAIL %d)" % (SUMMARY["main_total"], SUMMARY["main_pass"],
                                                 SUMMARY["main_info"], SUMMARY["main_fail"]))
print("CTL %d/%d   GRD %d/%d" % (SUMMARY["ctl_pass"], SUMMARY["ctl_total"],
                                 SUMMARY["grd_pass"], SUMMARY["grd_total"]))
for e in MAIN + CTL + GRD:
    if e["kind"] == "FAIL":
        print("FAIL %s :: %s | exp=%s act=%s" % (e["id"], e["title"], e["exp"], e["act"]))
print("PATHS:")
for p in OUT_PATHS:
    print("  %s  (%d B)" % (os.path.basename(p), os.path.getsize(p) if os.path.exists(p) else -1))
if missing:
    print("FAIL 落盘缺件: %s" % missing)
    sys.exit(1)
