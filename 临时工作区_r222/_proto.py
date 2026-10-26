# -*- coding: utf-8 -*-
"""r222 核心数值原型：求导对拍 + Binet 积分求近心点进动 + lambda 反解。"""
import math

# ---- 常数 ----
GM_SUN = 1.32712440018e20      # m^3/s^2
C0 = 299792458.0
PLANETS = [  # name, a(m), e
    ("Mercury", 5.7909050e10, 0.205630),
    ("Venus", 1.0820948e11, 0.006772),
    ("Earth", 1.4959787e11, 0.016710),
    ("Mars", 2.2793664e11, 0.093394),
]


def gr_precession(a, e):
    """GR 每转进动 6*pi*GM/(c^2 a (1-e^2)) [rad/rev]。"""
    return 6.0 * math.pi * GM_SUN / (C0 * C0 * a * (1.0 - e * e))


def yukawa_precession(a, e, lam, nstep=2000000):
    """Binet: u'' = (mu/h^2)(1+1/(u*lam))exp(-1/(u*lam)) - u
    初值取近心点 u0=1/(a(1-e)), u'=0；积分到下一个近心点，返回每转进动 rad。
    lam=None 或 inf 表示纯 1/r^2。"""
    mu_h2 = 1.0 / (a * (1.0 - e * e))
    inv_lam = 0.0 if lam is None else 1.0 / lam

    def acc(u):
        if inv_lam == 0.0:
            return mu_h2 - u
        x = inv_lam / u                      # = 1/(u*lam) = r/lam
        if x > 700.0:
            return -u                        # exp(-x) 下溢，力已指数消失
        return mu_h2 * (1.0 + x) * math.exp(-x) - u

    # 粗积分到略超过 pi（先过远心点），再细找下一个近心点
    u = 1.0 / (a * (1.0 - e))
    v = 0.0
    # theta 总跨度约 2*pi + 小量；用固定步数覆盖 [0, 2*pi+2e-4]
    th_tot = 2.0 * math.pi + 2.0e-4
    h = th_tot / nstep
    th = 0.0
    prev_v = v
    crossed = None
    for i in range(nstep):
        # RK4 on (u, v=u')
        k1u, k1v = v, acc(u)
        k2u, k2v = v + 0.5 * h * k1v, acc(u + 0.5 * h * k1u)
        k3u, k3v = v + 0.5 * h * k2v, acc(u + 0.5 * h * k2u)
        k4u, k4v = v + h * k3v, acc(u + h * k3u)
        un = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        th += h
        # 近心点 = u 极大 = u' 由正变负（发生在 theta ~ 2*pi；u' 由负变正是远心点 ~ pi）
        if vn < 0.0 and prev_v >= 0.0 and i > nstep // 2:
            crossed = th - h + h * (0.0 - prev_v) / (vn - prev_v)
            break
        u, v, prev_v = un, vn, vn
    if crossed is None:
        return None
    return crossed - 2.0 * math.pi


if __name__ == "__main__":
    print("== GR precession (rad/rev) ==")
    for nm, a, e in PLANETS:
        print("  %-8s %.6e" % (nm, gr_precession(a, e)))

    print("== lambda -> precession (Mercury) ==")
    a, e = PLANETS[0][1], PLANETS[0][2]
    tgt = gr_precession(a, e)
    print("  target(Mercury GR) = %.6e" % tgt)
    for lam in (1e12, 3e13, 1e14, 3e14, 1e15, 1e16, None):
        d = yukawa_precession(a, e, lam, nstep=400000)
        print("  lam=%-10s  domega=%s" % (lam, "%.6e" % d if d is not None else "None"))
