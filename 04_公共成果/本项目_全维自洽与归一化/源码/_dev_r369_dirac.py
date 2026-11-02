# -*- coding: utf-8 -*-
"""_dev_r369_dirac —— 定位 Dirac 残差 1.0 的分量与点位（跑通后删除）"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import mpmath as mp
mp.mp.dps = 70
ALPHA0 = mp.mpf(1) / mp.mpf("137.035999177")
HST = mp.mpf("1e-15")

def R3f(x, y, z):
    return mp.sqrt(x * x + y * y + z * z)

def psi_set(alpha_v, qfac=1.0):
    Gv = mp.sqrt(1 - alpha_v ** 2)
    Qv = alpha_v / (1 + Gv) * qfac
    Nv = mp.sqrt((2 * alpha_v) ** (2 * Gv + 1) / ((1 + Qv * Qv) * mp.gamma(2 * Gv + 1)))
    PF = Nv / mp.sqrt(4 * mp.pi)

    def rad(r):
        return PF * r ** (Gv - 1) * mp.e ** (-alpha_v * r)

    def n1(x, y, z):
        return rad(R3f(x, y, z))

    def z0(x, y, z):
        return mp.mpf(0)

    def p3i(x, y, z):
        r = R3f(x, y, z)
        return Qv * (z / r) * rad(r)

    def p4r(x, y, z):
        r = R3f(x, y, z)
        return -Qv * (y / r) * rad(r)

    def p4i(x, y, z):
        r = R3f(x, y, z)
        return Qv * (x / r) * rad(r)

    return Gv, Qv, [(n1, z0), (z0, z0), (z0, p3i), (p4r, p4i)]

def pder(f, x, y, z, var):
    if var == 0:
        return (f(x - 2*HST, y, z) - 8*f(x - HST, y, z) + 8*f(x + HST, y, z) - f(x + 2*HST, y, z)) / (12*HST)
    if var == 1:
        return (f(x, y - 2*HST, z) - 8*f(x, y - HST, z) + 8*f(x, y + HST, z) - f(x, y + 2*HST, z)) / (12*HST)
    return (f(x, y, z - 2*HST) - 8*f(x, y, z - HST) + 8*f(x, y, z + HST) - f(x, y, z + 2*HST)) / (12*HST)

def resid(alpha_v, pt):
    Gv, Qv, CP = psi_set(alpha_v)
    x, y, z = pt
    I = mp.mpc(0, 1)
    ps = [mp.mpc(CP[k][0](x, y, z), CP[k][1](x, y, z)) for k in range(4)]
    d = [[mp.mpc(pder(CP[k][0], x, y, z, v), pder(CP[k][1], x, y, z, v))
          for v in range(3)] for k in range(4)]
    r = R3f(x, y, z)
    E = Gv
    T0 = [-I*d[2][2], -I*d[3][0], -d[3][1], ps[0], -alpha_v/r*ps[0], -E*ps[0]]
    T1 = [-I*d[2][0], d[2][1], I*d[3][2], -alpha_v/r*ps[1], -E*ps[1]]
    T2 = [-I*d[0][2], -d[1][0], -I*d[1][1], -ps[2], -alpha_v/r*ps[2], -E*ps[2]]
    T3 = [-I*d[0][0], d[0][1], I*d[1][2], -ps[3], -alpha_v/r*ps[3], -E*ps[3]]
    out = []
    for T in (T0, T1, T2, T3):
        Lk = sum(T)
        den = sum(abs(t) for t in T)
        out.append(abs(Lk)/den if den > 0 else mp.mpf(0))
    return out

for pt in [(100, 40, 90), (137, 0, 0), (30, -60, 110), (2, 1, 1), (mp.mpf("0.5"), mp.mpf("0.3"), mp.mpf("0.7"))]:
    pt = tuple(mp.mpf(v) for v in pt)
    print([mp.nstr(v, 4) for v in resid(ALPHA0, pt)])
