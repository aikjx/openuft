# -*- coding: utf-8 -*-
"""_dev_r369_check —— r369 动手前的数学试算（跑通后删除）"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp
mp.mp.dps = 70

# ---------- 1) 2q = (1+q^2)a ----------
a, g = sp.symbols("a g", positive=True)
q = a / (1 + g)
expr = sp.simplify(sp.expand((2 * q - (1 + q**2) * a) * (1 + g)**2))
print("2q identity residual:", expr)

# ---------- 2) Dirac-Coulomb 1s1/2 残差 ----------
AL = mp.mpf(1) / mp.mpf("137.035999177")
G = mp.sqrt(1 - AL * AL)
Q = AL / (1 + G)
GN = mp.gamma(2 * G + 1)
NORM = mp.sqrt((2 * AL) ** (2 * G + 1) / ((1 + Q * Q) * GN))
PREF = NORM / mp.sqrt(4 * mp.pi)
print("gamma-1 =", mp.nstr(G - 1, 8), " q =", mp.nstr(Q, 10), " N =", mp.nstr(PREF, 6))

def rad(r):
    return PREF * r**(G - 1) * mp.e**(-AL * r)

def norm1(x, y, z):
    return rad(mp.sqrt(x * x + y * y + z * z))

def z0(x, y, z):
    return mp.mpf(0)

def p3i(x, y, z):
    r = mp.sqrt(x * x + y * y + z * z)
    return Q * (z / r) * rad(r)

def p4r(x, y, z):
    r = mp.sqrt(x * x + y * y + z * z)
    return -Q * (y / r) * rad(r)

def p4i(x, y, z):
    r = mp.sqrt(x * x + y * y + z * z)
    return Q * (x / r) * rad(r)

CP = [(norm1, z0), (z0, z0), (z0, p3i), (p4r, p4i)]

HST = mp.mpf("1e-15")
def pder(f, x, y, z, var):
    if var == 0:
        return (f(x - 2*HST, y, z) - 8*f(x - HST, y, z) + 8*f(x + HST, y, z) - f(x + 2*HST, y, z)) / (12*HST)
    if var == 1:
        return (f(x, y - 2*HST, z) - 8*f(x, y - HST, z) + 8*f(x, y + HST, z) - f(x, y + 2*HST, z)) / (12*HST)
    return (f(x, y, z - 2*HST) - 8*f(x, y, z - HST) + 8*f(x, y, z + HST) - f(x, y, z + 2*HST)) / (12*HST)

def dv(k, x, y, z, var):
    re, im = CP[k]
    return mp.mpc(pder(re, x, y, z, var), pder(im, x, y, z, var))

def val(k, x, y, z):
    re, im = CP[k]
    return mp.mpc(re(x, y, z), im(x, y, z))

def resid(x, y, z, qscale=1.0):
    ps = [val(k, x, y, z) for k in range(4)]
    ps[2] *= qscale
    ps[3] *= qscale
    d = [[dv(k, x, y, z, v) for v in range(3)] for k in range(4)]
    r = mp.sqrt(x * x + y * y + z * z)
    I = mp.mpc(0, 1)
    E = G
    L0 = -I * (d[2][2] + (d[3][0] - I * d[3][1])) + ps[0] - AL / r * ps[0] - E * ps[0]
    L1 = -I * ((d[2][0] + I * d[2][1]) - d[3][2]) - AL / r * ps[1] - E * ps[1]
    L2 = -I * (d[0][2] + (d[1][0] - I * d[1][1])) - ps[2] - AL / r * ps[2] - E * ps[2]
    L3 = -I * ((d[0][0] + I * d[0][1]) - d[1][2]) - ps[3] - AL / r * ps[3] - E * ps[3]
    L = [L0, L1, L2, L3]
    out = []
    for k in range(4):
        den = mp.mpf(0)
        for v in range(3):
            den += abs(d[k][v])
        den += abs(ps[k]) + abs(AL / r * ps[k]) + abs(E * ps[k])
        out.append(abs(L[k]) / den if den > 0 else mp.mpf(0))
    return max(out), [abs(x) for x in L]

for pt in [(100, 40, 90), (137, 0, 0), (30, -60, 110), (0.5, 0.3, 0.7)]:
    mx, abs_ = resid(*pt)
    print("pt", pt, "rel =", mp.nstr(mx, 5))
print("teeth q*(1+1e-3):", mp.nstr(resid(100, 40, 90, 1.001)[0], 5))
print("teeth q*(1+1e-6):", mp.nstr(resid(100, 40, 90, 1.000001)[0], 5))

# ---------- 3) 归一化 / <r> ----------
Gam = mp.gamma(2 * G + 2) / (2 * AL)**(2 * G + 2)
print("N^2 check:", mp.nstr(NORM**2 - (2 * AL)**(2 * G + 1) / ((1 + Q * Q) * GN), 5))
print("<r> closed =", mp.nstr((2 * G + 1) / (2 * AL), 20))
# 直接积分
f_int = lambda rr: (1 + Q*Q) * (NORM * rr**(G-1) * mp.e**(-AL*rr))**2 * rr**3
print("<r> quad  =", mp.nstr(mp.quad(f_int, [0, mp.inf]), 20))
f_nrm = lambda rr: (1 + Q*Q) * (NORM * rr**(G-1) * mp.e**(-AL*rr))**2 * rr**2
print("norm quad =", mp.nstr(mp.quad(f_nrm, [0, mp.inf]), 20))

# ---------- 4) Raychaudhuri 平直刚体旋转 ----------
t, x, y, z, W = sp.symbols("t x y z Omega", real=True)
Gs = 1 / sp.sqrt(1 - W**2 * (x**2 + y**2))
ue = sp.Matrix([Gs, -W * y * Gs, W * x * Gs, 0])
co = [t, x, y, z]
ul = sp.Matrix([Gs, W * y * Gs, -W * x * Gs, 0])
sg = [1, -1, -1, -1]
Th = sum(sp.diff(ue[i], co[i]) for i in range(4))
print("Theta =", sp.simplify(Th))
dd = sp.Matrix(4, 4, lambda nu, mu: sp.diff(ul[mu], co[nu]))
om = sp.Matrix(4, 4, lambda mu, nu: (dd[nu, mu] - dd[mu, nu]) / 2)
si = sp.Matrix(4, 4, lambda mu, nu: (dd[nu, mu] + dd[mu, nu]) / 2 - (Th / 3) * (sp.Matrix(4, 4, lambda i, j: sg[i] if i == j else 0)[mu, nu] + ul[mu] * ul[nu]))
def up(M, i, j):
    return sg[i] * sg[j] * M[i, j]
om2 = sp.simplify(sum(om[i, j] * up(om, i, j) for i in range(4) for j in range(4)))
si2 = sp.simplify(sum(si[i, j] * up(si, i, j) for i in range(4) for j in range(4)))
acc = sp.Matrix([sum(ue[nu] * sp.diff(ue[mu], co[nu]) for nu in range(4)) for mu in range(4)])
diva = sum(sp.diff(acc[mu], co[mu]) for mu in range(4))
bal = sp.simplify(-Th**2 / 3 - si2 + om2 + diva)
print("omega^2 =", sp.simplify(om2))
print("sigma^2 =", sp.simplify(si2))
print("div a   =", sp.simplify(diva))
print("balance =", bal)
f_bal = sp.lambdify((x, y, W), bal, "mpmath")
for (xx, yy, ww) in [(mp.mpf("0.3"), mp.mpf("0.2"), mp.mpf("0.4")), (mp.mpf("1"), mp.mpf("1"), mp.mpf("0.2"))]:
    print("balance num:", mp.nstr(f_bal(xx, yy, ww), 6))
f_om = sp.lambdify((x, y, W), om2, "mpmath")
f_di = sp.lambdify((x, y, W), diva, "mpmath")
for (xx, yy, ww) in [(mp.mpf("0.3"), mp.mpf("0.2"), mp.mpf("0.4")), (mp.mpf("1"), mp.mpf("1"), mp.mpf("0.2"))]:
    print("om2,diva:", mp.nstr(f_om(xx, yy, ww), 8), mp.nstr(f_di(xx, yy, ww), 8))
