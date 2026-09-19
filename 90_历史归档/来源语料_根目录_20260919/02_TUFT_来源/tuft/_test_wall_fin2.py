"""决定版检验：RW 反射壁腔模是否真极点（u_0 无关性）。
对每个 u_0 独立精修使 |f_in(u_s)| 最小的 ω；若精修后 ω 随 u_0 漂移 => 箱模；
若稳定 => 真极点。"""
import numpy as np

M = 1.0
r_s = 2.05
u_s = r_s + 2.0 * M * np.log(r_s / (2.0 * M) - 1.0)
DU = 0.02
U_MAX_TOT = 400.0
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
    return fr * (6.0 / r ** 2 - 6.0 * M / r ** 3)


VG = build_V()


def V_of_u(u):
    idx = int(round((u - u_s) / DU))
    idx = max(0, min(NU - 1, idx))
    return VG[idx]


def shoot_back_in(omega, u_0, du=DU):
    n = int(round((u_0 - u_s) / du))
    P = 1.0 + 0j
    dP = -1j * omega

    def rhs(Pv, dPv, uv):
        return dPv, -(omega ** 2 - V_of_u(uv)) * Pv

    for k in range(n):
        u0 = u_0 - k * du
        u1 = u0 - du
        k1P, k1d = rhs(P, dP, u0)
        k2P, k2d = rhs(P + du / 2 * k1P, dP + du / 2 * k1d, u1)
        k3P, k3d = rhs(P + du / 2 * k2P, dP + du / 2 * k2d, u1)
        k4P, k4d = rhs(P + du * k3P, dP + du * k3d, u1)
        P = P + du / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + du / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    return P


def refine(omega, u_0):
    w = complex(omega)
    for _ in range(150):
        g0 = shoot_back_in(w, u_0)
        h = 1e-7
        gr = (shoot_back_in(w + h, u_0) - shoot_back_in(w - h, u_0)) / (2 * h)
        gi = (shoot_back_in(w + 1j * h, u_0) - shoot_back_in(w - 1j * h, u_0)) / (2j * h)
        deriv = 0.5 * (gr + 1j * gi)
        if abs(deriv) < 1e-30:
            break
        s = g0 / deriv
        w = w - s
        if abs(s) < 1e-13:
            break
    return w, abs(shoot_back_in(w, u_0))


seed = 0.42 - 0.03j
print("对每个 u_0 从同种子精修 |f_in(u_s)| 最小点，看 ω 是否随 u_0 漂移：")
for u0 in (40.0, 60.0, 90.0, 120.0, 160.0, 240.0):
    w, g = refine(seed, u0)
    print("  u_0=%-5.0f  mode=%.6f%+.6fi  |f_in(u_s)|=%.3e" % (u0, w.real, w.imag, g))
