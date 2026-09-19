"""验证：反射壁腔模 = 无穷远出波 Jost 解 f_out 在墙处取零 f_out(u_s)=0。
稳定法：在固定适中 u_0（势≈0，渐近 e^{+iωu} 成立）处种入纯出波，向后积分到墙
u_s，读 Ψ(u_s)。真腔模 f_out(u_s)=0 对任意 u_0 成立（与 u_0 无关）；箱模的
"零点" 随 u_0 漂移。
对比：此前前向/变 u_max 射击都因"出波归一化随 u_max 振荡"而只找到箱模伪根。
"""
import numpy as np
import sys

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


def shoot_back(omega, u_0, du=DU):
    """种入纯出波 Ψ(u_0)=1, Ψ'(u_0)=iω，向后积分到 u_s，返回 Ψ(u_s)。"""
    n = int(round((u_0 - u_s) / du))
    if n < 1:
        n = 1
    P = 1.0 + 0j
    dP = 1j * omega

    def rhs(Pv, dPv, uv):
        return dPv, -(omega ** 2 - V_of_u(uv)) * Pv

    for k in range(n):
        u0 = u_0 - k * du
        u1 = u0 - du
        Vv = V_of_u(u0)
        Vv2 = V_of_u(u1)
        k1P, k1d = rhs(P, dP, Vv)
        k2P, k2d = rhs(P + du / 2 * k1P, dP + du / 2 * k1d, Vv2)
        k3P, k3d = rhs(P + du / 2 * k2P, dP + du / 2 * k2d, Vv2)
        k4P, k4d = rhs(P + du * k3P, dP + du * k3d, Vv2)
        P = P + du / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + du / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    return P


def refine(omega, u_0):
    w = complex(omega)
    for _ in range(120):
        g0 = shoot_back(w, u_0)
        h = 1e-7
        gr = (shoot_back(w + h, u_0) - shoot_back(w - h, u_0)) / (2 * h)
        gi = (shoot_back(w + 1j * h, u_0) - shoot_back(w - 1j * h, u_0)) / (2j * h)
        deriv = 0.5 * (gr + 1j * gi)
        if abs(deriv) < 1e-30:
            break
        s = g0 / deriv
        w = w - s
        if abs(s) < 1e-13:
            break
    return w, abs(shoot_back(w, u_0))


print("u_s = %.6f   seed outgoing Jost at fixed u_0, integrate back to wall" % u_s)
print("RW barrier peak V0~0.151 => sqrt(V0)~0.389 : true TRAPPED cavity modes need wR<0.389")
U0 = 60.0
# 低于势垒：Re in [0.10,0.39]，Im in [-0.15,-0.0005]
cands = []
for wr in np.linspace(0.10, 0.39, 30):
    for wi in np.linspace(-0.15, -0.0005, 35):
        w = complex(wr, wi)
        g = abs(shoot_back(w, U0))
        cands.append((g, w))
cands.sort(key=lambda t: t[0])
print("  top-6 smallest |Psi(u_s)| (u_0=%.0f):" % U0)
for g, w in cands[:6]:
    print("    |Psi|=%.3e  omega=%.5f%+.5fi" % (g, w.real, w.imag))

bestv, best = cands[0]
w, g = refine(best, U0)
print("  refined mode = %.6f%+.6fi  |Psi(u_s)|=%.3e" % (w.real, w.imag, g))

print("\nu_0-independence (true mode: |Psi(u_s)|->0 for ALL u_0):")
for u0 in (40.0, 60.0, 90.0, 140.0):
    Pw = shoot_back(w, u0)
    print("  u_0=%-5.0f  |Psi(u_s)|=%.3e" % (u0, abs(Pw)))
