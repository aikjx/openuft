# -*- coding: utf-8 -*-
"""r225 原型：闭式 kappa/omega 与 RK4 Binet 互印、维里残差、尺度分层、闭式 lambda 反解。"""
import math

GM_SUN = 1.32712440018e20
C_LIGHT = 299792458.0
AU = 1.495978707e11
RS_SUN = 2.0 * GM_SUN / (C_LIGHT ** 2)


def yukawa_precession(a, e, lam, nstep=400000):
    mu_h2 = 1.0 / (a * (1.0 - e * e))
    inv_lam = 0.0 if lam is None else 1.0 / lam

    def acc(u):
        if inv_lam == 0.0:
            return mu_h2 - u
        x = inv_lam / u
        if x > 700.0:
            return -u
        if u <= 0.0:
            return -u
        return mu_h2 * (1.0 + x) * math.exp(-x) - u

    u = 1.0 / (a * (1.0 - e))
    v = 0.0
    th_tot = 2.0 * math.pi + 2.0e-4
    h = th_tot / nstep
    th = 0.0
    prev_v = v
    for i in range(nstep):
        k1u, k1v = v, acc(u)
        k2u, k2v = v + 0.5 * h * k1v, acc(u + 0.5 * h * k1u)
        k3u, k3v = v + 0.5 * h * k2v, acc(u + 0.5 * h * k2u)
        k4u, k4v = v + h * k3v, acc(u + h * k3u)
        un = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        th += h
        if vn < 0.0 and prev_v >= 0.0 and i > nstep // 2:
            crossed = th - h + h * (0.0 - prev_v) / (vn - prev_v)
            return crossed - 2.0 * math.pi
        if un <= 0.0:
            return None
        u, v, prev_v = un, vn, vn
    return None


def closed_domega(x):
    """近点角进动闭式（圆轨道极限）：2*pi*(omega/kappa - 1)。"""
    if x >= 1.618033988749895:
        return None
    return 2.0 * math.pi * (math.sqrt((1.0 + x) / (1.0 + x - x * x)) - 1.0)


print("=== [1] 闭式 vs RK4：小偏心率极限 ===")
print("RS_SUN = %.4f m" % RS_SUN)
for e in (0.001, 0.01, 0.05, 0.2, 0.2056, 0.4):
    a = 5.7909e10
    lam = 1.433e14
    x = a / lam
    num = yukawa_precession(a, e, lam, nstep=200000)
    clo = closed_domega(x)
    small = math.pi * x * x
    print("e=%.4f  RK4=%.6e  闭式=%.6e  小x近似=%.6e  RK4/闭式=%.6f  RK4/小x=%.6f"
          % (e, num, clo, small, num / clo, num / small))

print()
print("=== [2] 幂律检验：RK4 的 domega 对 lambda 的指数 ===")
a = 5.7909e10
e = 0.2056
pts = []
for lam in (5e13, 1e14, 2e14, 5e14):
    d = yukawa_precession(a, e, lam, nstep=200000)
    pts.append((lam, d))
    print("lam=%.3e  domega=%.6e" % (lam, d))
for i in range(len(pts) - 1):
    l1, d1 = pts[i]
    l2, d2 = pts[i + 1]
    p = math.log(d1 / d2) / math.log(l2 / l1)
    print("指数 p = %.6f" % p)

print()
print("=== [3] 闭式 lambda 反解（水星）与 r223 RK4 值 1.433e14 m 对照 ===")
a_m = 5.7909e10
e_m = 0.20563
domega_gr = 6.0 * math.pi * GM_SUN / (C_LIGHT ** 2 * a_m * (1 - e_m * e_m))
print("GR 水星进动 = %.6e rad/rev" % domega_gr)
# 闭式：pi*(a/lam)^2 = domega  => lam = a*sqrt(pi/domega)
lam_closed_merc = a_m * math.sqrt(math.pi / domega_gr)
# 等价于 a^{3/2} sqrt((1-e^2)/(3 rs))
lam_alt = (a_m ** 1.5) * math.sqrt((1 - e_m * e_m) / (3.0 * RS_SUN))
print("闭式 lam = %.6e m = %.3f AU" % (lam_closed_merc, lam_closed_merc / AU))
print("等价式 lam = %.6e m = %.3f AU" % (lam_alt, lam_alt / AU))
print("r223 RK4 lam_fit = 1.433e14 m = %.3f AU" % (1.433e14 / AU))
print("相对差 = %.3e" % (abs(lam_closed_merc - 1.433e14) / 1.433e14))

print()
print("=== [4] 各行星闭式 lambda 反解（lambda ∝ a^{3/2} sqrt(1-e^2)）===")
planets = [("Mercury", 0.38710, 0.20563), ("Venus", 0.72333, 0.00677),
           ("Earth", 1.00000, 0.01671), ("Mars", 1.52371, 0.09339),
           ("Jupiter", 5.20289, 0.04839), ("Saturn", 9.53668, 0.05386),
           ("Uranus", 19.18916, 0.04726), ("Neptune", 30.06992, 0.00859)]
base = None
for nm, aau, ecc in planets:
    aa = aau * AU
    lam = (aa ** 1.5) * math.sqrt((1 - ecc * ecc) / (3.0 * RS_SUN))
    if base is None:
        base = lam
    print("%-9s a=%8.4f AU  e=%.5f  lambda=%12.4e m = %10.2f AU  lam/lam_Mercury=%8.4f"
          % (nm, aau, ecc, lam, lam / AU, lam / base))

print()
print("=== [5] 维里残差 (2T+V)/|V| = x = r/lam ===")
mu = GM_SUN
for lam_au in (100.0, 957.9, 10000.0):
    lam = lam_au * AU
    row = []
    for nm, aau, ecc in (("Earth", 1.0, 0.0167), ("Jupiter", 5.20289, 0.04839),
                         ("Neptune", 30.06992, 0.00859)):
        r = aau * AU
        x = r / lam
        row.append("%s x=%.4e" % (nm, x))
    print("lambda=%10.2f AU : %s" % (lam_au, "  ".join(row)))

print()
print("=== [6] 圆轨道数值复核：2T+V 与 -V*r/lam ===")
for x in (0.01, 0.1, 0.5, 1.0, 1.5):
    lam = 1.0
    r = x
    e = math.exp(-x)
    h2 = mu * e * (r * r / lam + r)
    T = h2 / (2 * r * r)
    V = -mu * e / r
    lhs = 2 * T + V
    rhs = -V * r / lam
    print("x=%.3f  (2T+V)=%.6e  (-V r/lam)=%.6e  相对差=%.3e"
          % (x, lhs, rhs, abs(lhs - rhs) / abs(rhs)))

print()
print("=== [7] 弱/强通道切换半径（借用 PDG 耦合）===")
HBAR = 1.054571817e-34
CC = 299792458.0
GEV = 1.602176634e-10
MEV = GEV / 1000.0
lam_w = HBAR * CC / (80.369 * GEV)
lam_pi = HBAR * CC / (134.977 * MEV)
print("lam_W  = %.6e m" % lam_w)
print("lam_pi = %.6e m" % lam_pi)
g_w = 0.653
g_pi = math.sqrt(4 * math.pi * 14.3)
print("g_W=%.4f  g_pi=%.4f (g_pi^2/4pi=14.3 借用)" % (g_w, g_pi))
# |F_pi| = |F_W| :  (g_pi/g_W)^2 * (1+r/lam_pi)/(1+r/lam_w) * exp(-r/lam_pi + r/lam_w) = 1
if g_pi > g_w:
    r_star = 2.0 * math.log(g_pi / g_w) / (1.0 / lam_w - 1.0 / lam_pi)
    print("忽略 (1+r/lam) 因子的切换半径 r* = %.6e m" % r_star)

    def ratio(r):
        return (g_pi / g_w) ** 2 * (1 + r / lam_pi) / (1 + r / lam_w) * \
            math.exp(-r / lam_pi + r / lam_w)
    lo, hi = 1e-20, 1e-12
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if ratio(mid) > 1.0:
            hi = mid
        else:
            lo = mid
    print("完整式二分 r* = %.6e m  (ratio=%.6f)" % (math.sqrt(lo * hi), ratio(math.sqrt(lo * hi))))

print()
print("=== [8] 尺度分层：质子-质子（借用 PDG 耦合）===")
m_p = 1.67262192e-27
m_pl = math.sqrt(HBAR * CC / 6.67430e-11)
alpha = 7.2973525693e-3
HC = HBAR * CC
q_g = m_p / m_pl
q_e = math.sqrt(alpha)
q_w = g_w / math.sqrt(4 * math.pi)
q_pi = g_pi / math.sqrt(4 * math.pi)
print("Q_g=%.6e  Q_e=%.6e  Q_W=%.6e  Q_pi=%.6e" % (q_g, q_e, q_w, q_pi))


def Fmag(q, lam, r):
    if lam is None:
        return HC * q * q / (r * r)
    return HC * q * q * (1.0 / (r * r) + 1.0 / (r * lam)) * math.exp(-r / lam)


for r in (1e-18, 1e-16, 1e-15, 1e-14, 1e-10, 1e-2, 1.0, 1e11):
    vals = {"G": Fmag(q_g, None, r), "EM": Fmag(q_e, None, r),
            "W": Fmag(q_w, lam_w, r), "pi": Fmag(q_pi, lam_pi, r)}
    mx = max(vals.values())
    order = sorted(vals.items(), key=lambda kv: -kv[1])
    sec = order[1][1] / mx
    print("r=%9.3e  主导=%-3s 次强/主导=%.4e  | %s"
          % (r, order[0][0], sec,
             "  ".join("%s=%.3e" % (k, v) for k, v in order)))
