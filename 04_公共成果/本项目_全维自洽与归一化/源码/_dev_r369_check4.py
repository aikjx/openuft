# -*- coding: utf-8 -*-
"""_dev_r369_check3 —— Raychaudhuri 正确投影复算（跑通后删除）"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp
mp.mp.dps = 60

t, x, y, z, W = sp.symbols("t x y z Omega", real=True)
Gs = 1 / sp.sqrt(1 - W**2 * (x**2 + y**2))
uU = [Gs, -W*y*Gs, W*x*Gs, sp.Integer(0)]
co = [t, x, y, z]
sg = [1, -1, -1, -1]
uD = [sg[i] * uU[i] for i in range(4)]

Th = sp.simplify(sum(sp.diff(uU[i], co[i]) for i in range(4)))
dd = [[sp.diff(uD[mu], co[nu]) for mu in range(4)] for nu in range(4)]   # dd[nu][mu] = d_nu u_mu

def proj(M):
    out = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            e = M[mu][nu]
            p = sum(uU[a] * uD[mu] * M[a][nu] for a in range(4))
            q_ = sum(uU[a] * uD[nu] * M[mu][a] for a in range(4))
            r_ = sum(uU[a] * uU[b] * uD[mu] * uD[nu] * M[a][b] for a in range(4) for b in range(4))
            out[mu, nu] = sp.expand(e - p - q_ + r_)
    return out

def sym_part(mode):
    if mode == "om":
        M = [[sp.expand((dd[nu][mu] - dd[mu][nu]) / 2) for mu in range(4)] for nu in range(4)]
    else:
        M = [[sp.expand((dd[nu][mu] + dd[mu][nu]) / 2) for mu in range(4)] for nu in range(4)]
    return proj(M)

om = sym_part("om")
h = sp.Matrix(4, 4, lambda i, j: (sg[i] if i == j else 0) - uD[i] * uD[j])
si = sym_part("si")
si = sp.Matrix(4, 4, lambda mu, nu: sp.expand(si[mu, nu] - Th / 3 * h[mu, nu]))
def norm2(M):
    return sp.simplify(sum(M[i, j] * sg[i] * sg[j] * M[i, j] for i in range(4) for j in range(4)))
om2 = norm2(om); si2 = norm2(si)
acc = sp.Matrix([sum(uU[nu] * sp.diff(uU[mu], co[nu]) for nu in range(4)) for mu in range(4)])
diva = sp.simplify(sum(sp.diff(acc[mu], co[mu]) for mu in range(4)))
dTh = sp.simplify(sum(uU[nu] * sp.diff(Th, co[nu]) for nu in range(4)))
bal = sp.simplify(-Th**2/3 - si2 + om2 + diva)
print("Theta =", Th, " | dTheta/dtau =", dTh)
print("omega^2 =", sp.factor(om2))
print("sigma^2 =", sp.factor(si2))
print("div a   =", diva)
print("balance =", bal)
print("om[0,1] =", sp.simplify(om[0, 1]), " si[0,1] =", sp.simplify(si[0, 1]))
print("om[1,2] =", sp.simplify(om[1, 2]), " si[1,2] =", sp.simplify(si[1, 2]))
print("si[1,1] =", sp.simplify(si[1, 1]), " si[2,2] =", sp.simplify(si[2, 2]))
fb = sp.lambdify((x, y, W), bal, "mpmath")
for (xx, yy, ww) in [(mp.mpf("0.3"), mp.mpf("0.2"), mp.mpf("0.4")),
                     (mp.mpf("1"), mp.mpf("1"), mp.mpf("0.2")),
                     (mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.9")),
                     (mp.mpf("1"), mp.mpf("0.5"), mp.mpf("0.001"))]:
    print("balance num:", mp.nstr(fb(xx, yy, ww), 4))
# 数值：om2, si2, diva
fo = sp.lambdify((x, y, W), om2, "mpmath"); fs = sp.lambdify((x, y, W), si2, "mpmath")
fd = sp.lambdify((x, y, W), diva, "mpmath")
for (xx, yy, ww) in [(mp.mpf("0.3"), mp.mpf("0.2"), mp.mpf("0.4")), (mp.mpf("1"), mp.mpf("0.5"), mp.mpf("0.001"))]:
    print("om2/si2/diva:", mp.nstr(fo(xx, yy, ww), 10), mp.nstr(fs(xx, yy, ww), 10), mp.nstr(fd(xx, yy, ww), 10))

