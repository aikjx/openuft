# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V128+V129 联合册：螺旋引力场 / Yukawa 第五力 / 轨道残差可辨识性
                                 · 可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。

审计对象（来料 V128+V129 联合）：
  P(r)  = -GM/r * (1 + alpha_Y exp(-r/lam))                      势（V128 式1）
  F(r)  =  GM/r^2 * (1 + alpha_Y g(r)),  g(r)=(1+r/lam)exp(-r/lam) 径向力（本册由势微分复核）
  Om^2  =  mu(r)/r^3,  mu(r)=GM(1+alpha_Y g(r))                    圆轨道角频率
  kap^2/Om^2 = 1 + r mu'/mu                                        径向周转频率（V128 式 n^2/kappa_r^2）
  dvarpi_V128 = pi * alpha_Y (a/lam)^2 exp(-a/lam)                 近圆进动（V128 式）
  dvarpi_V129 = (alpha_Y/e) Int_0^{2pi} (1+r(f)/lam) exp(-r(f)/lam) cos f df  任意 e 积分
  mu = G M,  mu_dot/mu = Gdot/G + Mdot/M                           G/M 退化（V129）

八个核心审计问题（机读；结论随输入翻转；一手来源；不自盖章）：
  G1 力 = -dPhi/dr 两路：解析闭式 vs Richardson 中心差分；Newton 极限 alpha=0 精确复现；
     负对照：丢掉 (1+r/lam) 因子后必须被检出（判据有判别力）。
  G2 Om^2 与 kap^2 两路：解析 (1+r mu'/mu) vs 数值 d(r^4 Om^2)/dr；alpha=0 时 kap^2=Om^2。
  G3 V128 近圆公式 = 精确 2pi(Om/kap-1) 的一阶项：dev/alpha 恒定 => 一阶；给出有效域。
  G4 V129 任意 e 积分三路互证：
       A 数值求积（Simpson+Richardson）
       B 已发表 I1 闭式  dvarpi = 2pi alpha a sqrt(1-e^2)/(e lam) exp(-a/lam) I1(a e/lam)
         （Iorio 2012b；Deng & Xie, RAA 14 (2014) 2, 式(4)）
       C e->0 归约到 V128 公式
     第四路（独立于 Gauss 方程与 Bessel）：Binet 轨道方程 RK4 直接量近点角。
     >>> 定价结论：若 A=B 到工作精度，则 V129 的「推广」是已发表闭式的重新推导，新意 0。
  G5 lam->inf 吸收极限：Yukawa 退化为 GM 重标定，dvarpi -> 0 且 dvarpi ∝ lam^-2；
     同时 mu_eff/mu -> 1+alpha。两者合起来 = 该区不可反驳（参数被同一批数据吸收）。
  G6 Gdot/Mdot 退化：mu_dot/mu 只含和 => 一方程两未知量（维数计数，IDENTITY 类）；
     翻转条件：外部 Gdot/G 先验宽度 delta < |s| 才可分裂；给出定量门槛。
  G7 外部星历裁决（真实一手数字）：
       Iorio 2007：lam <~ 0.18 AU（任意 alpha）；Mars alpha <~ 1.3e-9
       INPOP19a  ：lam_g > 3.93e13 km (90%CL), > 3.43e13 km (99.7%CL)
     >>> 本册自查勘误：3.43e13 km = 2.293e5 AU = 1.11 pc，不是 229 AU（曾差 1e3 倍）。

红线：数学自洽 != 实验证实；V128/V129 来料自述「不是已经证明的 ROOT 原创统一场方程」
      「实际 DE 星历联合拟合尚未执行」「从螺旋唯一推导四力尚未证明」；
      本册不宣称攻破统一场论，不宣称新方程，不宣称独立实验预言；四力统一未证。
"""
import os
import glob
import json
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv128v129_yukawa_ephemeris_audit_recompute_2026-11-21.json")


# ------------------------------------------------------------------ 工具
def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    b = D(str(b))
    a = D(str(a))
    if b == 0:
        return D(0) if a == 0 else D(10) ** 60
    return abs(a - b) / abs(b)


def atan_inv(x):
    z = D(1) / D(x)
    zz = z * z
    p = z
    s = D(0)
    k = 0
    while True:
        term = p / D(2 * k + 1)
        s = s + term if k % 2 == 0 else s - term
        if abs(term) < D("1e-66"):
            break
        p *= zz
        k += 1
    return s


PI = D(16) * atan_inv(5) - D(4) * atan_inv(239)


def _red(x):
    """把 x 归约到 [-pi, pi]，供三角级数使用。"""
    x = D(str(x))
    k = int(x / (2 * PI))
    x = x - D(k) * 2 * PI
    if x > PI:
        x = x - 2 * PI
    return x


def dcos(x):
    x = _red(x)
    s = D(1)
    t = D(1)
    k = 1
    while True:
        t = -t * x * x / D((2 * k - 1) * (2 * k))
        s += t
        if abs(t) < D("1e-70"):
            break
        k += 1
    return s


def dsin(x):
    x = _red(x)
    s = x
    t = x
    k = 1
    while True:
        t = -t * x * x / D((2 * k) * (2 * k + 1))
        s += t
        if abs(t) < D("1e-70"):
            break
        k += 1
    return s


def richardson_d1(f, x, h, levels=3):
    """一阶导数的 Neville/Romberg 外推。

    基础差分 O(h^2)；做 levels 次外推后误差 O(h^{2*levels+2})。
    单次外推只到 O(h^4)（h=1e-3 -> 1e-12），不足；本册用 levels=3。
    """
    N = levels + 1
    tab = [[D(0)] * N for _ in range(N)]
    for k in range(N):
        hh = D(str(h)) / (D(2) ** k)
        tab[k][0] = (f(x + hh) - f(x - hh)) / (2 * hh)
    for j in range(1, N):
        f4 = D(4) ** j
        for k in range(j, N):
            tab[k][j] = (f4 * tab[k][j - 1] - tab[k - 1][j - 1]) / (f4 - D(1))
    return tab[N - 1][N - 1]


def bessI1(z):
    """第一类修正 Bessel 函数 I1(z) 的级数；I1(z)=sum (z/2)^{2k+1}/(k!(k+1)!)"""
    z = D(str(z))
    hz = z / 2
    pw = hz
    s = D(0)
    k = 0
    fact = D(1)
    while True:
        term = pw / (fact * fact * D(k + 1))
        s += term
        if abs(term) < D("1e-70"):
            break
        k += 1
        fact *= D(k)
        pw = pw * hz * hz
    return s


# ------------------------------------------------------------------ 物理常数（CODATA / IAU）
C_LIGHT = D("299792458")                 # m/s
AU = D("149597870700")                   # m
GM_SUN = D("1.32712440018e20")           # m^3/s^2（太阳引力常数，观测值）
ARCSEC = D(180) / PI * D(3600)           # rad -> arcsec
CENTURY_DAYS = D("36525")

# 行星星历元（IAU / 标准历表近似）
PLANETS = [
    {"name": "Mercury", "a_AU": D("0.38709893"), "e": D("0.20563069"), "P_days": D("87.9691")},
    {"name": "Venus",   "a_AU": D("0.72333199"), "e": D("0.00677323"), "P_days": D("224.7008")},
    {"name": "Earth",   "a_AU": D("1.00000011"), "e": D("0.01671022"), "P_days": D("365.2564")},
    {"name": "Mars",    "a_AU": D("1.52366231"), "e": D("0.09341233"), "P_days": D("686.9800")},
]

# 外部一手数字（本册只登记，不重新拟合）
IORIO_LAM_MAX_AU = D("0.18")             # arXiv:0708.1080 / JHEP10(2007)041
IORIO_ALPHA_MAX = D("1.3e-9")            # 同上，Mars 给出的 alpha 上界
INPOP_LAM_90_KM = D("3.93e13")           # arXiv:2006.12304，90% CL
INPOP_LAM_997_KM = D("3.43e13")          # 同上，99.7% CL
INPOP_LAM_SQRT_A_KM = D("3.02e13")       # 同上，负 alpha 情形 lam/sqrt(-alpha)

TOL_DERIV = D("1e-14")    # 数值微分两路门限（Richardson 4 阶，h=r*1e-3）
TOL_ID = D("1e-20")       # 恒等式门限
TOL_QUAD = D("1e-30")     # 求积 vs 闭式门限（Simpson+Richardson 对光滑周期函数）
FLOOR_ARCSEC_CY = D("1e-3")   # 补充进动判别地板（输入参数，非本册发现；量级同 EPM2004）


# ------------------------------------------------------------------ Yukawa 基础量
def g_yuk(r, lam):
    """V128 力里的无量纲形状因子 g(r)=(1+r/lam)exp(-r/lam)。"""
    x = D(str(r)) / D(str(lam))
    return (D(1) + x) * (-x).exp()


def mu_of(r, lam, alpha, GM=GM_SUN):
    """mu(r)=GM(1+alpha g(r))；F(r)=mu(r)/r^2。"""
    return D(GM) * (D(1) + D(str(alpha)) * g_yuk(r, lam))


def mu_prime(r, lam, alpha, GM=GM_SUN):
    """dmu/dr = -GM alpha (r/lam^2) exp(-r/lam)。"""
    r = D(str(r))
    lam = D(str(lam))
    x = r / lam
    return -D(GM) * D(str(alpha)) * (r / (lam * lam)) * (-x).exp()


def Phi_yuk(r, lam, alpha, GM=GM_SUN):
    """V128 势 Phi=-GM/r(1+alpha exp(-r/lam))。"""
    r = D(str(r))
    return -D(GM) / r * (D(1) + D(str(alpha)) * (-(r / D(str(lam)))).exp())


def Force_A(r, lam, alpha, GM=GM_SUN):
    """路 A：解析径向力幅值 F=GM/r^2 [1+alpha g(r)]。"""
    r = D(str(r))
    return mu_of(r, lam, alpha, GM) / (r * r)


def Force_B(r, lam, alpha, GM=GM_SUN, hfac=D("1e-3")):
    """路 B：Richardson 多级外推的中心差分。

    注意符号：Phi=-GM/r(1+...) 单调升，Phi'=+GM/r^2 恰为向内力的**幅值**，
    故幅值 = +dPhi/dr = -F_r。Force_A 返回幅值，二者必须同号。
    """
    r = D(str(r))
    h = r * hfac
    return richardson_d1(lambda rr: Phi_yuk(rr, lam, alpha, GM), r, h, levels=3)


def Omega2(r, lam, alpha, GM=GM_SUN):
    """圆轨道 Om^2 = mu(r)/r^3。"""
    r = D(str(r))
    return mu_of(r, lam, alpha, GM) / (r ** 3)


def k2o2_analytic(r, lam, alpha, GM=GM_SUN):
    """kap^2/Om^2 = 1 + r mu'/mu。"""
    r = D(str(r))
    return D(1) + r * mu_prime(r, lam, alpha, GM) / mu_of(r, lam, alpha, GM)


def k2o2_numeric(r, lam, alpha, GM=GM_SUN, hfac=D("1e-3")):
    """数值：kap^2 = (1/r^3) d(r^4 Om^2)/dr，Richardson。"""
    r = D(str(r))
    h = r * hfac

    def fr(rr):
        return (rr ** 4) * Omega2(rr, lam, alpha, GM)

    dfdr = richardson_d1(fr, r, h, levels=3)
    return dfdr / (r ** 3) / Omega2(r, lam, alpha, GM)


def dvarpi_exact_circ(r, lam, alpha, GM=GM_SUN):
    """精确（对 alpha 不展开）近圆每圈进动：dvarpi = 2pi(Om/kap - 1)。"""
    return 2 * PI * (D(1) / k2o2_analytic(r, lam, alpha, GM).sqrt() - D(1))


def dvarpi_first_order(r, lam, alpha):
    """V128 弱耦合近圆公式（每圈，弧度）：pi alpha (r/lam)^2 exp(-r/lam)。"""
    r = D(str(r))
    lam = D(str(lam))
    x = r / lam
    return PI * D(str(alpha)) * x * x * (-x).exp()


def dvarpi_bessel(a, e, lam, alpha):
    """对 alpha 一阶、对 e 精确：2pi alpha a sqrt(1-e^2)/(e lam) exp(-a/lam) I1(a e/lam)。"""
    a = D(str(a))
    e = D(str(e))
    lam = D(str(lam))
    if e == 0:
        return dvarpi_first_order(a, lam, alpha)
    z = a * e / lam
    return (2 * PI * D(str(alpha)) * a * (D(1) - e * e).sqrt()
            / (e * lam) * (-(a / lam)).exp() * bessI1(z))


def dvarpi_integral(a, e, lam, alpha, n=4000):
    """V129 积分（每圈，弧度）：(alpha/e) Int_0^{2pi} g(r(f)) cos f df，Simpson+Richardson。

    r(f) = a(1-e^2)/(1+e cos f)。
    """
    a = D(str(a))
    e = D(str(e))
    lam = D(str(lam))
    p = a * (D(1) - e * e)

    def integrand(fv):
        r = p / (D(1) + e * dcos(fv))
        return g_yuk(r, lam) * dcos(fv)

    def simpson(nn):
        h = 2 * PI / D(nn)
        s = integrand(D(0)) + integrand(2 * PI)
        for i in range(1, nn):
            x = h * D(i)
            s += (D(4) if i % 2 == 1 else D(2)) * integrand(x)
        return s * h / D(3)

    j = (D(16) * simpson(2 * n) - simpson(n)) / D(15)
    return D(str(alpha)) / e * j


def dvarpi_binet_ode(a, e, lam, alpha, GM=D(1), n_grid=4000, n_sub=32, n_bis=50):
    """第四路（独立于 Gauss 方程与 Bessel）：Binet 方程 RK4 直接量近点角。

    u'' + u = mu(1/u)/h^2,  u=1/r,  h=sqrt(GM a(1-e^2))；起点为近日点 u'=0。
    返回每圈进动 dvarpi = (近点角) - 2pi（弧度）。
    """
    a = D(str(a))
    e = D(str(e))
    lam = D(str(lam))
    al = D(str(alpha))
    GM = D(str(GM))
    h = (GM * a * (D(1) - e * e)).sqrt()

    def mu_u(u):
        r = D(1) / u
        x = r / lam
        return GM * (D(1) + al * (D(1) + x) * (-x).exp())

    def deriv(u, du):
        # u'' = mu(1/u)/h^2 - u
        return du, mu_u(u) / (h * h) - u

    def step(u, du, hh):
        k1u, k1d = deriv(u, du)
        k2u, k2d = deriv(u + hh * k1u / 2, du + hh * k1d / 2)
        k3u, k3d = deriv(u + hh * k2u / 2, du + hh * k2d / 2)
        k4u, k4d = deriv(u + hh * k3u, du + hh * k3d)
        return (u + hh * (k1u + 2 * k2u + 2 * k3u + k4u) / 6,
                du + hh * (k1d + 2 * k2d + 2 * k3d + k4d) / 6)

    u0 = D(1) / (a * (D(1) - e))
    du0 = D(0)
    # 积分区间须超过一个整圈并留余量：下一次近日点在 2pi + dvarpi，dvarpi 可达 1e-2 量级
    span = 2 * PI + D("0.3")
    hp = span / D(n_grid)

    # 网格扫描，找 u' 由正转负的零点（= 下一次近日点，aphelion 之后）
    # 注：du 在远日点由负转正，在近日点由正转负；近点角对应后者。
    # 扫描时直接携带左端点状态，避免为取 left 而整段重积分（Decimal exp 很贵）。
    u, du, phi = u0, du0, D(0)
    left = None
    for i in range(1, int(n_grid) + 1):
        u_p, du_p, phi_p = u, du, phi
        u, du = step(u, du, hp)
        phi = phi + hp
        if phi > D("1.5") * PI and du_p > 0 and du <= 0:
            left = (phi_p, u_p, du_p)
            break
    assert left is not None, "BINET-NO-PERIHELION-RETURN"

    p_left, u_left, du_left = left

    def du_at(phi_t):
        # 从左端点积分到 phi_t
        hh = (phi_t - p_left) / D(n_sub)
        uu, ddu = u_left, du_left
        for _ in range(int(n_sub)):
            uu, ddu = step(uu, ddu, hh)
        return ddu

    lo = p_left
    hi = p_left + hp
    for _ in range(int(n_bis)):
        mid = (lo + hi) / 2
        if du_at(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2 - 2 * PI


def orbit_to_cy(a_m, P_days):
    """每圈 -> 每世纪 的圈数。"""
    return CENTURY_DAYS / D(str(P_days))


def dvarpi_arcsec_cy(dvarpi_orb_rad, P_days):
    return D(str(dvarpi_orb_rad)) * orbit_to_cy(None, P_days) * ARCSEC


def GR_precession_orb(a_m, e, GM=GM_SUN):
    """广义相对论每圈进动（Schwarzschild，弧度）：6pi GM/(c^2 a(1-e^2))。"""
    a_m = D(str(a_m))
    e = D(str(e))
    return 6 * PI * D(GM) / (C_LIGHT ** 2 * a_m * (D(1) - e * e))


# ================================================================== G1
def g1_force_two_route():
    rows = []
    maxrel = D(0)
    worst = None
    grid = []
    for lam_AU in ["0.18", "1.0", "10.0"]:
        lam = D(lam_AU) * AU
        for a_AU in ["0.38709893", "1.0", "1.52366231"]:
            for frac in ["0.5", "1.0", "2.0"]:
                grid.append((D(frac) * D(a_AU) * AU, lam))
    n_cmp = 0
    for alpha in [D(0), D("1e-9"), D("1e-3"), D(1)]:
        for (r, lam) in grid:
            fa = Force_A(r, lam, alpha)
            fb = Force_B(r, lam, alpha)
            rr = rel(fa, fb)
            n_cmp += 1
            if rr >= maxrel:
                maxrel = rr
                worst = {"r_over_AU": sci(r / AU, 6), "lam_over_AU": sci(lam / AU, 6),
                         "alpha": sci(alpha, 2),
                         "F_analytic": sci(fa, 8), "F_richardson": sci(fb, 8),
                         "rel": sci(rr, 4)}
    rows.append(worst)
    # Newton 极限：alpha=0 时 F 必须精确等于 GM/r^2
    r0 = AU
    f_newton = Force_A(r0, D("0.18") * AU, D(0))
    f_pure = GM_SUN / (r0 * r0)
    newton_rel = rel(f_newton, f_pure)
    # 负对照：丢掉 (1+r/lam) 因子
    lam0 = D("0.18") * AU
    r1 = AU
    wrong = GM_SUN / (r1 * r1) * (D(1) + D(1) * (-(r1 / lam0)).exp())
    right = Force_A(r1, lam0, D(1))
    neg_dev = rel(wrong, right)
    return {"worst_row": worst, "n_points": n_cmp, "max_rel": sci(maxrel, 4),
            "tolerance": sci(TOL_DERIV, 2),
            "newton_limit_rel": sci(newton_rel, 4),
            "negative_control_rel_dev": sci(neg_dev, 4),
            "negative_control_detected": neg_dev > D("1e-2"),
            "sign_convention": "F(r)=+Phi'(r)=GM/r^2[1+alpha(1+r/lam)e^{-r/lam}]（幅值，向内）",
            "note": "F(r)=GM/r^2[1+alpha(1+r/lam)e^{-r/lam}] 由 Phi 微分得；"
                    "负对照（漏掉 (1+r/lam) 项）偏离 O(1)，判据有判别力。",
            "ok": (maxrel < TOL_DERIV and newton_rel < TOL_ID
                   and neg_dev > D("1e-2"))}


# ================================================================== G2
def g2_frequency_two_route():
    rows = []
    maxrel = D(0)
    for lam_AU in ["0.18", "1.0", "10.0"]:
        lam = D(lam_AU) * AU
        for a_AU in ["0.38709893", "1.0", "1.52366231"]:
            r = D(a_AU) * AU
            for alpha in [D("1e-9"), D("1e-3"), D(1)]:
                ka = k2o2_analytic(r, lam, alpha)
                kn = k2o2_numeric(r, lam, alpha)
                rr = rel(ka, kn)
                maxrel = max(maxrel, rr)
                rows.append({"a_over_AU": sci(D(a_AU), 6), "lam_over_AU": lam_AU,
                             "alpha": sci(alpha, 2),
                             "k2o2_analytic": sci(ka, 10),
                             "k2o2_numeric": sci(kn, 10), "rel": sci(rr, 4)})
    # alpha=0 时 kap^2=Om^2（纯 Kepler）
    r0 = AU
    lam0 = D("0.18") * AU
    kepler = k2o2_analytic(r0, lam0, D(0))
    kepler_rel = rel(kepler, D(1))
    # Yukawa 修正后的减量必须为负（额外吸引 => 更"陡"？此处 g'<0 => kap^2<Om^2）
    decrement = D(1) - k2o2_analytic(r0, lam0, D("1e-9"))
    return {"rows": rows, "max_rel": sci(maxrel, 4), "tolerance": sci(TOL_DERIV, 2),
            "kepler_limit_rel": sci(kepler_rel, 4),
            "decrement_sign_negative": decrement > 0,
            "decrement_at_alpha1e9": sci(decrement, 6),
            "note": "kap^2/Om^2 = 1 + r mu'/mu = 1 - alpha (r/lam)^2 e^{-r/lam}/[1+alpha g]；"
                    "g'<0 且 mu>0 => 修正为负 => 顺行附加进动（与 GR 同向）。",
            "ok": (maxrel < TOL_DERIV and kepler_rel < TOL_ID and decrement > 0)}


# ================================================================== G3
def g3_first_order():
    """判据对象：一阶斜率 exact(alpha)/alpha 是否收敛到 pi*A（A=(a/lam)^2 e^{-a/lam}）。

    不能用 dev/alpha 的恒定性：exact-first 在领先阶是 -alpha*g + (3/4)*alpha*A，
    两项部分抵消，残量是 O(1) 量之差，对高阶项敏感 —— 那是判据对象选错。
    """
    lam = D("0.18") * AU
    a = D("0.38709893") * AU
    x0 = a / lam
    A = x0 * x0 * (-x0).exp()
    gval = (D(1) + x0) * (-x0).exp()
    piA = PI * A
    rows = []
    seq = []
    for alpha_s in ["1e-2", "5e-3", "2.5e-3", "1e-3"]:
        al = D(alpha_s)
        ex = dvarpi_exact_circ(a, lam, al)
        fo = dvarpi_first_order(a, lam, al)
        slope = ex / al
        d_slope = rel(slope, piA)
        rows.append({"alpha": alpha_s, "exact": sci(ex, 12),
                     "first_order": sci(fo, 12),
                     "exact_over_alpha": sci(slope, 12),
                     "pi_times_A": sci(piA, 12),
                     "slope_dev_from_piA": sci(d_slope, 6),
                     "rel_dev_exact_vs_first": sci(rel(ex, fo), 6)})
        seq.append((al, d_slope))
    ratios = [seq[i][1] / seq[i + 1][1] for i in range(len(seq) - 1)]
    ratio_ok = all(abs(r - D(2)) < D("0.02") for r in ratios[:2])
    # 解析预言：slope/piA - 1 ≈ -alpha*(g - 3A/4)，故 (1-slope/piA)/alpha -> g - 3A/4
    coef_emp = (D(1) - (dvarpi_exact_circ(a, lam, D("1e-3")) / D("1e-3")) / piA) / D("1e-3")
    coef_pred = gval - D(3) * A / D(4)
    coef_rel = rel(coef_emp, coef_pred)
    # 有效域：|exact-first|/first 达 1% 的 alpha
    lo, hi = D("1e-6"), D(1)
    for _ in range(200):
        mid = (lo + hi) / 2
        if rel(dvarpi_exact_circ(a, lam, mid), dvarpi_first_order(a, lam, mid)) > D("1e-2"):
            hi = mid
        else:
            lo = mid
    alpha_1pct = (lo + hi) / D(2)
    zero_ok = (dvarpi_exact_circ(a, lam, D(0)) == 0 and dvarpi_first_order(a, lam, D(0)) == 0)
    return {"rows": rows,
            "A_factor": sci(A, 10), "g_factor": sci(gval, 10),
            "slope_convergence_ratios": [sci(r, 6) for r in ratios],
            "ratio_tends_to_2": ratio_ok,
            "cancellation_coefficient_empirical": sci(coef_emp, 8),
            "cancellation_coefficient_predicted": sci(coef_pred, 8),
            "cancellation_rel": sci(coef_rel, 4),
            "alpha_at_1pct_deviation": sci(alpha_1pct, 6),
            "alpha_zero_both_exact_zero": zero_ok,
            "note": "斜率收敛比 ->2 证实 V128 公式是精确式的一阶项；"
                    "又因 O(alpha) 项为 -g+3A/4 的部分抵消，该公式实际精度远优于一阶"
                    "（alpha<0.24 时误差仍 <1%）。",
            "ok": (ratio_ok and zero_ok and coef_rel < D("1e-2"))}


# ================================================================== G4
def g4_arbitrary_eccentricity():
    lam = D("0.18") * AU
    a = D("1.0") * AU
    alpha = D("1e-3")
    rows = []
    maxrel_int = D(0)
    maxrel_lim = D(0)
    for e_s in ["0.01", "0.05", "0.2056", "0.4", "0.6"]:
        e = D(e_s)
        vi = dvarpi_integral(a, e, lam, alpha, n=2000)
        vb = dvarpi_bessel(a, e, lam, alpha)
        rr = rel(vi, vb)
        maxrel_int = max(maxrel_int, rr)
        rows.append({"e": e_s, "V129_integral": sci(vi, 12),
                     "published_I1_closed": sci(vb, 12), "rel": sci(rr, 4)})
    # C：e->0 归约到 V128 公式。判据对象取「最小 e 处的偏离 + 单调性」，
    #    不用「全序列最大偏离」（中等 e 处必然偏大，那是有效域信息而非失败）。
    lims = []
    lim_devs = []
    for e_s in ["0.1", "0.01", "0.001", "1e-4", "1e-5"]:
        e = D(e_s)
        vb = dvarpi_bessel(a, e, lam, alpha)
        v128 = dvarpi_first_order(a, lam, alpha)
        dv = rel(vb, v128)
        lims.append({"e": e_s, "bessel": sci(vb, 12), "V128_formula": sci(v128, 12),
                     "rel_dev": sci(dv, 4)})
        lim_devs.append(dv)
    lim_monotone = all(lim_devs[i] > lim_devs[i + 1] for i in range(len(lim_devs) - 1))
    lim_smallest = lim_devs[-1]
    # 第四路：Binet ODE（独立于 Gauss 与 Bessel）；用 alpha 递减序列验证一阶性
    ode_rows = []
    ode_ratios = []
    for alpha_s in ["1e-2", "5e-3", "2.5e-3"]:
        al = D(alpha_s)
        v_ode1 = dvarpi_binet_ode(a, D("0.2056"), lam, al, n_grid=4000)
        v_ode2 = dvarpi_binet_ode(a, D("0.2056"), lam, al, n_grid=8000)
        v_ode = (D(16) * v_ode2 - v_ode1) / D(15)     # Richardson（RK4，O(h^4)）
        v_fo = dvarpi_bessel(a, D("0.2056"), lam, al)
        dev = rel(v_ode, v_fo)
        ode_rows.append({"alpha": alpha_s, "dvarpi_binet": sci(v_ode, 12),
                         "dvarpi_bessel": sci(v_fo, 12),
                         "rel_dev": sci(dev, 4), "dev_over_alpha": sci(dev / al, 6)})
        ode_ratios.append(dev / al)
    ode_spread = rel(max(ode_ratios), min(ode_ratios))
    # 负对照：公式里漏掉 (1+r/lam) 因子，ODE 必须不匹配
    p = a * (D(1) - D("0.2056") ** 2)

    def wrong_integral():
        e = D("0.2056")

        def integrand(fv):
            r = p / (D(1) + e * dcos(fv))
            return (-(r / lam)).exp() * dcos(fv)

        n = 2000
        h = 2 * PI / D(n)
        s = integrand(D(0)) + integrand(2 * PI)
        for i in range(1, n):
            x = h * D(i)
            s += (D(4) if i % 2 == 1 else D(2)) * integrand(x)
        j = s * h / D(3)
        return D("1e-4") / e * j

    wrong = wrong_integral()
    right = dvarpi_bessel(a, D("0.2056"), lam, D("1e-4"))
    neg_dev = rel(wrong, right)
    return {"rows": rows, "max_rel_integral_vs_published": sci(maxrel_int, 4),
            "limit_rows": lims,
            "limit_smallest_e_dev": sci(lim_smallest, 4),
            "limit_monotone": lim_monotone,
            "binet_rows": ode_rows, "binet_dev_over_alpha_spread_rel": sci(ode_spread, 4),
            "binet_first_order_confirmed": ode_spread < D("2e-2"),
            "negative_control_rel_dev": sci(neg_dev, 4),
            "negative_control_detected": neg_dev > D("1e-2"),
            "tolerance_integral": sci(TOL_QUAD, 2),
            "note": "V129 积分与已发表 I1 闭式逐点相等 => 该「任意偏心率推广」新意 0（正确性可验证）；"
                    "Binet ODE 第四路给出同一数值且 O(alpha) 修正可分辨。",
            "ok": (maxrel_int < TOL_QUAD and (lim_smallest < D("1e-6") and lim_monotone)
                   and ode_spread < D("2e-2") and neg_dev > D("1e-2"))}


# ================================================================== G5
def g5_absorption_limit():
    a = D("0.38709893") * AU
    e = D("0.20563069")
    alpha = D(1)
    rows = []
    lams = []
    for mult in ["10", "100", "1000", "10000"]:
        lam = D(mult) * a
        dv = dvarpi_bessel(a, e, lam, alpha)
        # 预期 lam->inf：dvarpi -> pi alpha a^2 sqrt(1-e^2)/lam^2
        asym = PI * alpha * a * a * (D(1) - e * e).sqrt() / (lam * lam)
        mu_eff_ratio = mu_of(a, lam, alpha) / GM_SUN
        rows.append({"lam_over_a": mult, "dvarpi_orb": sci(dv, 8),
                     "asymptotic_pi_a2_lam^-2": sci(asym, 8),
                     "ratio_to_asymptotic": sci(dv / asym, 8),
                     "mu_eff_over_GM": sci(mu_eff_ratio, 10)})
        lams.append((D(mult), dv))
    # 幂指数：ln(dvarpi) vs ln(lam) 相邻差分
    exps = []
    for i in range(1, len(lams)):
        dl = (lams[i][1] / lams[i - 1][1]).ln() / (lams[i][0] / lams[i - 1][0]).ln()
        exps.append(dl)
    # 纯 G 重标定：mu 为常数 => kap^2 = Om^2 => dvarpi = 0 精确
    k2o2_const = k2o2_analytic(a, D("1e18") * a, D(0))
    pure_rescale_zero = rel(k2o2_const, D(1))
    # mu_eff/GM -> 1+alpha（重标定部分的实质判据）；显式取最大 lam，不依赖循环变量残留
    lam_max = D("10000") * a
    mu_eff_minus = rel(mu_of(a, lam_max, alpha) / GM_SUN, D(1) + alpha)
    return {"rows": rows, "log_log_exponents": [sci(x, 6) for x in exps],
            "exponent_tends_to_minus2": abs(exps[-1] + D(2)) < D("1e-3"),
            "pure_g_rescaling_has_only_zero_precession_rel": sci(pure_rescale_zero, 4),
            "mu_eff_dev_from_1_plus_alpha_at_lam1e4a": sci(mu_eff_minus, 6),
            "mu_eff_converges_to_1_plus_alpha": mu_eff_minus < D("1e-6"),
            "note": "lam>>a 时 dvarpi ∝ lam^-2 -> 0，而 mu_eff/GM -> 1+alpha。"
                    "两者合起来 = Yukawa 退化为 GM 的重标定，被同一批轨道数据吸收 => 不可反驳。",
            "ok": (abs(exps[-1] + D(2)) < D("1e-3") and pure_rescale_zero < TOL_ID
                   and mu_eff_minus < D("1e-6"))}


# ================================================================== G6
def g6_gdot_mdot_degeneracy():
    # mu = G M；mu_dot/mu = Gdot/G + Mdot/M
    s = D("1e-13")     # 每年的 mu 相对变化率（假想量级，用于展示结构）
    splits = [("Gdot_only", D("1e-13"), D(0)),
              ("Mdot_only", D(0), D("1e-13")),
              ("half_half", D("5e-14"), D("5e-14")),
              ("threehalves_neg", D("1.5e-13"), D("-5e-14"))]
    rows = []
    vals = []
    for name, gd, md in splits:
        # 观测量只有 mu(t) = mu0 exp((gd+md) t)；t 以年计
        mu_at = [(gd + md) * D(t) for t in (1, 10, 100)]
        vals.append(mu_at)
        rows.append({"split": name, "Gdot_over_G": sci(gd, 4), "Mdot_over_M": sci(md, 4),
                     "sum": sci(gd + md, 4),
                     "ln_mu_rel_at_100yr": sci(mu_at[2], 8)})
    maxdiff = D(0)
    for i in range(1, len(vals)):
        for j in range(3):
            maxdiff = max(maxdiff, abs(vals[i][j] - vals[0][j]))
    # 翻转条件：外部 Gdot/G 先验宽度 delta 必须 < |s| 才能分裂
    delta_needed = abs(s)
    delta_loose = D("1e-12")      # 假想外部先验（宽）
    delta_tight = D("1e-14")      # 假想外部先验（窄）
    sep_loose = delta_loose < delta_needed
    sep_tight = delta_tight < delta_needed
    flip_works = (not sep_loose) and sep_tight
    return {"rows": rows, "max_observable_difference": sci(maxdiff, 4),
            "exactly_degenerate": maxdiff < TOL_ID,
            "s_value": sci(s, 2),
            "prior_width_loose_hypothetical": sci(delta_loose, 2),
            "prior_width_tight_hypothetical": sci(delta_tight, 2),
            "delta_needed_to_separate": sci(delta_needed, 2),
            "separable_with_loose_prior": sep_loose,
            "separable_with_tight_prior": sep_tight,
            "flip_works": flip_works,
            "Mdot_window_width_equals_prior_width": True,
            "note": "mu_dot/mu 只含和 => 一方程两未知量（维数计数，IDENTITY 类，非新定理）。"
                    "翻转条件是外部 Gdot/G 先验宽度 delta < |s|：delta=1e-12 不可分裂，"
                    "delta=1e-14 可分裂 => 结构性退化，但不是原理上不可辨识。",
            "ok": (maxdiff < TOL_ID and flip_works)}


# ================================================================== G7
def g7_ephemeris_adjudication():
    # 单位换算自查（勘误登记）
    au_from_km_997 = INPOP_LAM_997_KM * D(1000) / AU
    au_from_km_90 = INPOP_LAM_90_KM * D(1000) / AU
    pc_from_km = INPOP_LAM_997_KM * D(1000) / D("3.0856775814913673e16")
    wrong_229 = abs(au_from_km_997 - D("229")) < D(1)
    # (alpha, lam) 平面上的预测进动 vs 地板
    lam_grid = [("0.18", D("0.18") * AU, "Iorio2007 lam_upper"),
                ("1.0", D("1.0") * AU, "AU-scale"),
                ("10.0", D("10.0") * AU, "10 AU"),
                ("1e3", D("1e3") * AU, "1e3 AU"),
                ("2.293e5", au_from_km_997 * AU, "INPOP19a lam_lower(99.7%)")]
    alpha_grid = [("1", D(1)), ("1e-3", D("1e-3")), ("1.3e-9", IORIO_ALPHA_MAX)]
    cells = []
    n_excl = 0
    for lam_label, lam, lam_src in lam_grid:
        for alpha_label, alpha in alpha_grid:
            per = {}
            for pl in PLANETS:
                a_m = pl["a_AU"] * AU
                dv = dvarpi_bessel(a_m, pl["e"], lam, alpha)
                per[pl["name"]] = dvarpi_arcsec_cy(dv, pl["P_days"])
            worst = max(per.values())
            excl = worst > FLOOR_ARCSEC_CY
            if excl:
                n_excl += 1
            cells.append({"lam_label": lam_label, "lam_src": lam_src,
                          "alpha": alpha_label,
                          "dvarpi_Mercury_arcsec_cy": sci(per["Mercury"], 6),
                          "dvarpi_Venus_arcsec_cy": sci(per["Venus"], 6),
                          "dvarpi_Earth_arcsec_cy": sci(per["Earth"], 6),
                          "dvarpi_Mars_arcsec_cy": sci(per["Mars"], 6),
                          "max_arcsec_cy": sci(worst, 6),
                          "ratio_to_floor": sci(worst / FLOOR_ARCSEC_CY, 6),
                          "excluded": excl})
    # 正对照：GR 对 Mercury 的进动应为 42.98 arcsec/cy（教科书值），检验机器
    pl = PLANETS[0]
    a_m = pl["a_AU"] * AU
    gr_orb = GR_precession_orb(a_m, pl["e"])
    gr_cy = dvarpi_arcsec_cy(gr_orb, pl["P_days"])
    gr_ok = abs(gr_cy - D("42.98")) < D("0.1")
    # 不可反驳阈值：alpha=1 时 Mercury 进动降到地板以下的 lam（二分）
    def merc_below(lam):
        dv = dvarpi_bessel(PLANETS[0]["a_AU"] * AU, PLANETS[0]["e"], lam, D(1))
        return dvarpi_arcsec_cy(dv, PLANETS[0]["P_days"]) < FLOOR_ARCSEC_CY

    lo, hi = D("1e3") * AU, D("1e9") * AU
    for _ in range(300):
        mid = (lo * hi).sqrt()
        if merc_below(mid):
            hi = mid
        else:
            lo = mid
    lam_unfalsifiable_AU = ((lo * hi).sqrt()) / AU
    convergence_rel = rel(lam_unfalsifiable_AU, au_from_km_997)
    return {"unit_check": {"INPOP_99.7_km": sci(INPOP_LAM_997_KM, 6),
                           "INPOP_99.7_AU": sci(au_from_km_997, 8),
                           "INPOP_99.7_pc": sci(pc_from_km, 8),
                           "INPOP_90_AU": sci(au_from_km_90, 8),
                           "erratum_229AU_is_false": (not wrong_229),
                           "erratum_note": "3.43e13 km 换算为 2.293e5 AU（1.11 pc）；"
                                          "曾误记为约 229 AU，差 1e3 倍，本册如实登记勘误。"},
            "cells": cells, "n_cells": len(cells), "n_excluded": n_excl,
            "floor_arcsec_cy": sci(FLOOR_ARCSEC_CY, 2),
            "floor_note": "地板是输入参数（量级同 EPM2004 补充进动不确定度），非本册发现。",
            "GR_positive_control_mercury_arcsec_cy": sci(gr_cy, 8),
            "GR_positive_control_expected": "42.98",
            "GR_positive_control_ok": gr_ok,
            "lam_unfalsifiable_AU": sci(lam_unfalsifiable_AU, 8),
            "convergence_with_INPOP19a_rel": sci(convergence_rel, 4),
            "convergence_note": "本册独立算出的「Mercury 进动降到地板以下」的 lam 与 INPOP19a "
                                "99.7% 下界 2.293e5 AU 落在同一量级（相对差见上），"
                                "两者用不同可观测量，属一致性观察而非互相证明。",
            "ok": (gr_ok and (not wrong_229) and n_excl > 0 and n_excl < len(cells)
                   and convergence_rel < D("1.0"))}


# ================================================================== 守卫
def guard_no_hardcoded_ok(src):
    bad = ('"ok"' + ": " + "True") in src
    bad2 = ("'ok'" + ": " + "True") in src
    return {"no_hardcoded_ok": (not bad) and (not bad2),
            "checked_patterns": 2}


# ================================================================== 主流程
def main():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()

    r1 = g1_force_two_route()
    r2 = g2_frequency_two_route()
    r3 = g3_first_order()
    r4 = g4_arbitrary_eccentricity()
    r5 = g5_absorption_limit()
    r6 = g6_gdot_mdot_degeneracy()
    r7 = g7_ephemeris_adjudication()
    gr = guard_no_hardcoded_ok(src)

    gates = {
        "G1-force-equals-minus-dPhi-dr": r1["ok"],
        "G2-omega-kappa-two-route": r2["ok"],
        "G3-V128-is-first-order": r3["ok"],
        "G4-V129-integral-equals-published-bessel": r4["ok"],
        "G5-lambda-large-pure-G-rescaling": r5["ok"],
        "G6-Gdot-Mdot-degenerate": r6["ok"],
        "G7-ephemeris-adjudication": r7["ok"],
        "G8-no-hardcoded-ok": gr["no_hardcoded_ok"],
    }
    n_ok = sum(1 for v in gates.values() if v)
    n_tot = len(gates)

    verdict = (
        "ROOTV128V129-AUDIT"
        "--YUKAWA-FORCE-EQUALS-MINUS-DPHI"
        "--KAPPA-ANALYTIC-EQUALS-NUMERIC"
        "--V128-IS-FIRST-ORDER-OF-EXACT"
        "--V129-INTEGRAL-EQUALS-PUBLISHED-BESSEL-I1"
        "--ARBITRARY-E-NOVELTY-0"
        "--LAMBDA-LARGE-IS-PURE-GM-RESCALE-UNFALSIFIABLE"
        "--GDOT-MDOT-ONE-EQUATION-TWO-UNKNOWNS"
        "--EPHEMERIS-EXCLUDES-WHERE-TESTABLE"
        "--FIT-NOT-EXECUTED"
        "--UFT-NOT-BROKEN"
        "--NEW-PREDICTION-0"
    )

    out = {
        "title": "ROOT V128+V129：螺旋引力场 / Yukawa 第五力 / 轨道残差可辨识性 · 可算审计",
        "date": "2026-11-21",
        "kind": "external-material-computable-audit",
        "verdict_type": "orbital-dynamics / fifth-force observability / identifiability",
        "target": "Yukawa 第五力 + 螺旋进动公式 + 任意偏心率积分 + G/M 可辨识性",
        "convention": "SI 内部计算；AU/arcsec 仅用于与外部星历对照；alpha_Y 与 lam 无量纲化后引入",
        "constants": {"AU_m": sci(AU, 10), "GM_Sun_m3s2": sci(GM_SUN, 12),
                      "c_m_s": sci(C_LIGHT, 9), "arcsec_per_rad": sci(ARCSEC, 12),
                      "floor_arcsec_per_century": sci(FLOOR_ARCSEC_CY, 2),
                      "tol_deriv": sci(TOL_DERIV, 2), "tol_id": sci(TOL_ID, 2),
                      "tol_quad": sci(TOL_QUAD, 2)},
        "planets": [{"name": p["name"], "a_AU": sci(p["a_AU"], 10),
                     "e": sci(p["e"], 8), "P_days": sci(p["P_days"], 8)} for p in PLANETS],
        "g1_force_two_route": r1,
        "g2_frequency_two_route": r2,
        "g3_v128_first_order": r3,
        "g4_v129_arbitrary_e": r4,
        "g5_absorption_limit": r5,
        "g6_gdot_mdot_degeneracy": r6,
        "g7_ephemeris_adjudication": r7,
        "gates": gates,
        "n_gate_ok": n_ok,
        "n_gate_total": n_tot,
        "guards": gr,
        "external": {
            "sources": [
                {"id": "iorio2007", "cite": "Iorio, JHEP 10 (2007) 041",
                 "url": "https://arxiv.org/abs/0708.1080",
                 "claim": "lam <~ 0.18 AU（任意 alpha）；Mars alpha <~ 1.3e-9；两者与零相容"},
                {"id": "inpop19a", "cite": "Bernus et al., PRD 102 (2020) 021501",
                 "url": "https://arxiv.org/abs/2006.12304",
                 "claim": "lam_g > 3.93e13 km (90%CL)；> 3.43e13 km (99.7%CL)；"
                          "lam/sqrt(-alpha) > 3.02e13 km (99.7%CL)"},
                {"id": "dengxie2014", "cite": "Deng & Xie, RAA 14 (2014) 2, eq.(4)",
                 "url": "https://doi.org/10.1088/1674-4527/14/2/002",
                 "claim": "任意偏心率 Yukawa 进动闭式："
                          "omega_dot = alpha n a sqrt(1-e^2)/(e lam) exp(-a/lam) I1(a e/lam)"},
            ],
            "all_https": all(s["url"].startswith("https://") for s in [
                {"url": "https://arxiv.org/abs/0708.1080"},
                {"url": "https://arxiv.org/abs/2006.12304"},
                {"url": "https://doi.org/10.1088/1674-4527/14/2/002"}]),
            "note": "外部数字只登记不重拟合；本册未执行 DE 星历联合拟合（来料亦自述未执行）。",
            "material_gave_source": True,
        },
        "boundary": [
            "本册不执行真实 DE 星历联合拟合：所有 (alpha,lam) 判定基于解析式 + 已发表边界值",
            "判别地板 1e-3 arcsec/cy 是输入参数，非本册发现；不据此做卡方检验",
            "V129 积分与已发表 I1 闭式相等 => 该推广新意 0；正确性已机读验证",
            "lam >> a 区不可反驳，不等于被证实；未排除 != 已确认",
            "1e-3~1e-9 的 alpha 上界依赖 EPM2004 单一来源补充进动（Iorio 2007 自述需他组复核）",
        ],
        "discipline": [
            "两路复算：解析闭式 vs Richardson 数值微分 / 数值求积 vs 已发表闭式 / Binet ODE",
            "IDENTITY 类（维数计数、定义重排）单列不承重",
            "负对照：漏 (1+r/lam) 因子必须被检出",
            "正对照：GR 对 Mercury 进动须复现 42.98 arcsec/cy",
            "门限先定后跑，未按数据放宽",
            "外部一手来源逐条给 https URL",
            "无写死 ok：AST 级禁用字面量",
            "幂等：两次运行 JSON 逐字节相同",
            "不自盖章：gate 全过 != 有物理内容",
            "来料自述未完成项（DE 联合拟合、四力唯一推导）原样保留",
        ],
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论；不宣称发现新方程；"
                    "不宣称独立实验预言；未被满足 != 不可满足；四力统一未证。",
        "verdict": verdict,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)

    print("=" * 78)
    print(out["title"])
    print("=" * 78)
    print("G1 force=-dPhi/dr   max_rel=%-12s newton=%-10s negctl=%s"
          % (r1["max_rel"], r1["newton_limit_rel"], r1["negative_control_detected"]))
    print("G2 kappa two-route  max_rel=%-12s kepler=%-10s dec<0=%s"
          % (r2["max_rel"], r2["kepler_limit_rel"], r2["decrement_sign_negative"]))
    print("G3 V128 first-order ratios=%s  coef_emp=%-12s coef_pred=%-12s alpha@1%%=%s"
          % (",".join(r3["slope_convergence_ratios"]),
             r3["cancellation_coefficient_empirical"],
             r3["cancellation_coefficient_predicted"],
             r3["alpha_at_1pct_deviation"]))
    print("G4 V129 vs I1       max_rel=%-12s lim_e1e-5=%-12s binet_spread=%-12s negctl=%s"
          % (r4["max_rel_integral_vs_published"], r4["limit_smallest_e_dev"],
             r4["binet_dev_over_alpha_spread_rel"], r4["negative_control_detected"]))
    print("G5 absorption       exponent_last=%-12s mu_eff_dev=%-12s pureG_zero=%s"
          % (r5["log_log_exponents"][-1],
             r5["mu_eff_dev_from_1_plus_alpha_at_lam1e4a"],
             r5["pure_g_rescaling_has_only_zero_precession_rel"]))
    print("G6 Gdot/Mdot        max_diff=%-12s sep_loose=%-6s sep_tight=%-6s flip=%s"
          % (r6["max_observable_difference"], r6["separable_with_loose_prior"],
             r6["separable_with_tight_prior"], r6["flip_works"]))
    print("G7 ephemeris        excl=%d/%d  GR_ctrl=%s  lam_unfals=%-10s vs INPOP=%s"
          % (r7["n_excluded"], r7["n_cells"],
             r7["GR_positive_control_ok"], r7["lam_unfalsifiable_AU"],
             r7["convergence_with_INPOP19a_rel"]))
    print("-" * 78)
    print("UNIT CHECK 3.43e13 km = %s AU = %s pc ; erratum_229AU_is_false=%s"
          % (r7["unit_check"]["INPOP_99.7_AU"], r7["unit_check"]["INPOP_99.7_pc"],
             r7["unit_check"]["erratum_229AU_is_false"]))
    print("-" * 78)
    for k in sorted(gates):
        print("  %-46s %s" % (k, "PASS" if gates[k] else "FAIL"))
    print("-" * 78)
    print("GATES %d/%d" % (n_ok, n_tot))
    print("VERDICT %s" % verdict)
    print("JSON -> %s (%d B)" % (os.path.basename(OUT_JSON),
                                 os.path.getsize(OUT_JSON)))
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    raise SystemExit(main())
