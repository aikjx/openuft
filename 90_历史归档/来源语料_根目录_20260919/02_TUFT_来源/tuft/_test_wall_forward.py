"""验证：反射壁腔模真根判据（稳定前向射击法，优化版）。
墙在 r_s=2.05M，域 [r_s, ∞)，墙 Dirichlet Ψ(r_s)=0，无穷远出波。
从墙 u_s 向前积分，读出波残差 G = Ψ'(u_max)-iωΨ(u_max)；腔模 G→0。
向前积分稳定：出波随 u 增长、入波衰减，非腔模 |G|~e^{+|Imω|u_max} 增大。
判据：腔模钟频随 u_max 稳定；箱模漂移。
"""
import numpy as np
import sys

M = 1.0
r_s = 2.05
u_s = r_s + 2.0 * M * np.log(r_s / (2.0 * M) - 1.0)

DU = 0.03
U_MAX_TOT = 2600.0
NU = int(round((U_MAX_TOT - u_s) / DU)) + 1
ugrid = u_s + np.arange(NU) * DU


def build_V():
    c = ugrid / (2.0 * M) - 1.0
    y = np.where(c > 1.0, c, np.exp(c))
    y = np.maximum(y, 1e-12)
    for _ in range(50):
        f = y + np.log(y) - c
        y = y - f / (1.0 + 1.0 / y)
        y = np.maximum(y, 1e-14)
    r = 2.0 * M * (1.0 + y)
    fr = 1.0 - 2.0 * M / r
    return fr * (6.0 / r ** 2 - 6.0 * M / r ** 3)   # l=2


VG = build_V()


def V_of_u(u):
    idx = int(round((u - u_s) / DU))
    if idx < 0:
        idx = 0
    if idx >= NU:
        idx = NU - 1
    return VG[idx]


def shoot_forward(omega, u_max, du=DU):
    n = int(round((u_max - u_s) / du))
    if n < 1:
        n = 1
    P = 0.0 + 0j
    dP = 1.0 + 0j
    # 局部 RK4（V 用最近网格点）
    for k in range(n):
        u0 = u_s + k * du
        u1 = u0 + du
        Vv = V_of_u(u0)
        Vv2 = V_of_u(u1)

        def rhs(Pv, dPv, Vv_loc):
            return dPv, -(omega ** 2 - Vv_loc) * Pv

        k1P, k1d = rhs(P, dP, Vv)
        k2P, k2d = rhs(P + du / 2 * k1P, dP + du / 2 * k1d, Vv2)
        k3P, k3d = rhs(P + du / 2 * k2P, dP + du / 2 * k2d, Vv2)
        k4P, k4d = rhs(P + du * k3P, dP + du * k3d, Vv2)
        P = P + du / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + du / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    return dP - 1j * omega * P


def find_mode(center, half_re, half_im, ng_re, ng_im, u_max):
    best = None
    bestv = 1e30
    cr, ci = center
    sys.stdout.write("  scan u_max=%d ..." % u_max)
    sys.stdout.flush()
    for wr in np.linspace(cr - half_re, cr + half_re, ng_re):
        for wi in np.linspace(ci - half_im, ci + half_im, ng_im):
            w = complex(wr, wi)
            g = abs(shoot_forward(w, u_max))
            if g < bestv:
                bestv = g
                best = w
    sys.stdout.write(" best |G|=%.2e\n" % bestv)
    sys.stdout.flush()
    # Newton 精修
    w = best
    for _ in range(120):
        g0 = shoot_forward(w, u_max)
        h = 1e-7
        gr = (shoot_forward(w + h, u_max) - shoot_forward(w - h, u_max)) / (2 * h)
        gi = (shoot_forward(w + 1j * h, u_max) - shoot_forward(w - 1j * h, u_max)) / (2j * h)
        deriv = 0.5 * (gr + 1j * gi)
        if abs(deriv) < 1e-30:
            break
        s = g0 / deriv
        w = w - s
        if abs(s) < 1e-13:
            break
    return w, abs(shoot_forward(w, u_max))


print("u_s = %.6f  (forward shooting, Dirichlet wall + outgoing at inf)" % u_s)
print("coarse scan @ u_max=600:")
w0, g0 = find_mode((0.41, -0.03), 0.10, 0.08, 22, 20, 600.0)
print("  -> candidate mode  %.6f %+.6fi   |G|=%.3e" % (w0.real, w0.imag, g0))

print("\nu_max-convergence check (true mode: stable; box: drifts):")
for um in (300.0, 600.0, 1200.0, 2400.0):
    g = shoot_forward(w0, um)
    print("  u_max=%-5d  omega=%.6f%+.6fi  |G|=%.3e" % (int(um), w0.real, w0.imag, abs(g)))
