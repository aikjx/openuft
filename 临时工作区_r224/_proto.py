# -*- coding: utf-8 -*-
"""r224 原型：圆轨道稳定性解析判据 x=r_c/lam < phi 的数值复核。"""
import math

MU = 1.32712440018e20   # GM_sun


def U(m, r, lam):
    """单位质量有效势（引力 K<0）：U = -mu e^{-r/lam}/r + h^2/(2r^2)。"""
    return None  # 占位


def circular_condition(r, lam):
    """圆轨道：h^2 = mu e^{-r/lam}(r^2/lam + r)。"""
    return MU * math.exp(-r / lam) * (r * r / lam + r)


def U2_at_circular(r, lam):
    """在圆轨道处的 U''（代入 h^2 的圆轨道值）。"""
    h2 = circular_condition(r, lam)
    # U'' = mu e^{-r/lam}[-1/(lam^2 r) - 2/(lam r^2) - 2/r^3] + 3 h^2/r^4
    return (MU * math.exp(-r / lam)
            * (-1.0 / (lam * lam * r) - 2.0 / (lam * r * r) - 2.0 / (r ** 3))
            + 3.0 * h2 / (r ** 4))


def U2_closed(r, lam):
    """解析闭式：mu e^{-x}/r^3 * (-x^2 + x + 1)，x=r/lam。"""
    x = r / lam
    return MU * math.exp(-x) / (r ** 3) * (-x * x + x + 1.0)


if __name__ == "__main__":
    lam = 1.0e14
    print("lam = %.3e" % lam)
    print("  x=r/lam   U''(numeric)      U''(closed)     rel-diff    stable?")
    for x in (0.5, 1.0, 1.5, 1.618, 1.62, 1.7, 2.0, 3.0):
        r = x * lam
        a = U2_at_circular(r, lam)
        b = U2_closed(r, lam)
        print("  %-9.4f %+.6e  %+.6e  %.2e   %s"
              % (x, a, b, abs(a - b) / max(abs(b), 1e-300), "yes" if a > 0 else "NO"))

    # 求根：解 -x^2 + x + 1 = 0
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    print("\n解析根 x* = (1+sqrt5)/2 = %.10f  (黄金比 phi)" % phi)

    # 数值二分求 U'' 变号点
    lo, hi = 0.1, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if U2_at_circular(mid * lam, lam) > 0:
            lo = mid
        else:
            hi = mid
    print("数值二分变号点 x = %.10f  (与 phi 相对差 %.2e)"
          % (lo, abs(lo - phi) / phi))

    # 太阳系：稳定圆轨道要求的 lam 下界 = r/phi
    print("\n== 各行星稳定圆轨道所要求的 lam 下界（lam > r/phi）==")
    for nm, a in (("Mercury", 5.7909050e10), ("Venus", 1.0820948e11),
                  ("Earth", 1.4959787e11), ("Mars", 2.2793664e11),
                  ("Jupiter", 7.7854720e11), ("Neptune", 4.5034437e12)):
        print("  %-8s a=%9.4e m  lam_min = %.4e m = %.3f AU"
              % (nm, a, a / phi, a / phi / 1.495978707e11))
