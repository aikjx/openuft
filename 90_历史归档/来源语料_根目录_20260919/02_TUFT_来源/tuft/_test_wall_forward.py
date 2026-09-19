"""验证：反射壁腔模真根判据（稳定法）。
TUFT 墙在 r_s=2.05M，域为 [r_s, ∞)，墙 Dirichlet Ψ(r_s)=0，无穷远出波 BC。
（视界 r=2M 在墙之内被挖去，故腔模 = 墙 Dirichlet + 无穷远出波 的共振，
非 R25 的视界正则 QNM。）

稳定射击法：从墙 u_s 向前（u 增大）积分，墙处 Ψ=0, Ψ'=1，到 u_max 读
G = Ψ'(u_max) - iω Ψ(u_max)（出波残差）。腔模 = G(ω)=0。
向前积分稳定：出波 e^{+iωu} 随 u 增长，入波 e^{-iωu} 衰减，故非腔模的 |G|
随 u_max 按 e^{+|Imω| u_max} 增大、腔模的 G→0 且与 u_max 无关。
判据：u_max 增大时钟频是否稳定（真腔模）还是漂移（箱模）。
"""
import numpy as np

M = 1.0
r_s = 2.05
u_s = r_s + 2.0 * M * np.log(r_s / (2.0 * M) - 1.0)   # ≈ -5.33


def r_of_rstar(u):
    """解 r* = r + 2M ln(r/2M-1) 求 r>2M（Newton）。"""
    c = u / (2.0 * M) - 1.0
    y = c if c > 0 else np.exp(c)          # y = r/(2M)-1
    y = max(y, 1e-12)
    for _ in range(60):
        f = y + np.log(y) - c
        if abs(f) < 1e-15:
            break
        y = y - f / (1.0 + 1.0 / y)
    return 2.0 * M * (1.0 + y)


def V_at_u(u):
    r = r_of_rstar(u)
    if r <= 2.0 * M:
        return 1e30
    f = 1.0 - 2.0 * M / r
    return float(f * (6.0 / r ** 2 - 6.0 * M / r ** 3))   # l=2: ell(ell+1)=6


def shoot_forward(omega, u_max, du=0.01):
    n = int(round((u_max - u_s) / du))
    if n < 1:
        n = 1
    us = np.linspace(u_s, u_max, n + 1)
    P = 0.0 + 0j
    dP = 1.0 + 0j                       # 墙 Dirichlet: P=0, P'=1

    def rhs(Pv, dPv, uv):
        return dPv, -(omega ** 2 - V_at_u(uv)) * Pv

    for k in range(n):
        h = us[k + 1] - us[k]
        Vv = V_at_u(us[k])
        Vv2 = V_at_u(us[k + 1])
        k1P, k1d = rhs(P, dP, Vv)
        k2P, k2d = rhs(P + h / 2 * k1P, dP + h / 2 * k1d, Vv2)
        k3P, k3d = rhs(P + h / 2 * k2P, dP + h / 2 * k2d, Vv2)
        k4P, k4d = rhs(P + h * k3P, dP + h * k3d, Vv2)
        P = P + h / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + h / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    # 出波残差：真腔模 G→0
    return dP - 1j * omega * P


def find_mode(center, half_re, half_im, ng_re, ng_im, u_max, du=0.01):
    best = None
    bestv = 1e30
    cr, ci = center
    for wr in np.linspace(cr - half_re, cr + half_re, ng_re):
        for wi in np.linspace(ci - half_im, ci + half_im, ng_im):
            w = complex(wr, wi)
            g = abs(shoot_forward(w, u_max, du))
            if g < bestv:
                bestv = g
                best = w
    # Newton 精修
    w = best
    for _ in range(200):
        g0 = shoot_forward(w, u_max, du)
        h = 1e-7
        gr = (shoot_forward(w + h, u_max, du) - shoot_forward(w - h, u_max, du)) / (2 * h)
        gi = (shoot_forward(w + 1j * h, u_max, du) - shoot_forward(w - 1j * h, u_max, du)) / (2j * h)
        # 用复数导数近似：解 [g'(w)] dw = -g0
        deriv = (gr + 1j * gi) * 0.5
        if abs(deriv) < 1e-30:
            break
        s = g0 / deriv
        w = w - s
        if abs(s) < 1e-13:
            break
    return w, abs(shoot_forward(w, u_max, du))


print("u_s = %.6f" % u_s)
# 在 R21/R24 邻域粗扫，找最小 |G|
centers = [(0.40794, -0.02606), (0.409880, -0.029576), (0.41, -0.03), (0.45, -0.009)]
for um in (300, 600, 1200, 2400):
    print("\n=== u_max = %d ===" % um)
    for ctr in centers:
        w, g = find_mode(ctr, 0.06, 0.05, 26, 22, um)
        print("  seed %9s%9s -> mode %.6f%+.6fi  |G|=%.3e"
              % (("%.3f" % ctr[0]), ("%.4f" % ctr[1]),
                 w.real, w.imag, g))
