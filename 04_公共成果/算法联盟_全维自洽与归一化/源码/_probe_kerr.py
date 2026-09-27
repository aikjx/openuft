# -*- coding: utf-8 -*-
"""临时探针：Kerr 符号 Christoffel/Riemann/Weyl 标量耗时与正确性。"""
import time, sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

t0 = time.time()
M, a = sp.symbols("M a", real=True)
r, th = sp.symbols("r theta", real=True)
t, ph = sp.symbols("t phi", real=True)
coords = [t, r, th, ph]

Sig = r**2 + a**2 * sp.cos(th)**2
Del = r**2 - 2 * M * r + a**2

g = sp.zeros(4, 4)
g[0, 0] = -(1 - 2 * M * r / Sig)
g[0, 3] = -2 * M * a * r * sp.sin(th)**2 / Sig
g[3, 0] = g[0, 3]
g[1, 1] = Sig / Del
g[2, 2] = Sig
g[3, 3] = sp.sin(th)**2 / Sig * ((r**2 + a**2)**2 - a**2 * Del * sp.sin(th)**2)
print("度规构造 %.2fs" % (time.time() - t0))

ginv = g.inv()
print("逆矩阵 %.2fs" % (time.time() - t0))

# Christoffel (不 simplify)
Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for A in range(4):
    for B in range(4):
        for C in range(4):
            s = 0
            for D in range(4):
                s += ginv[A, D] * (sp.diff(g[D, C], coords[B]) +
                                   sp.diff(g[D, B], coords[C]) -
                                   sp.diff(g[B, C], coords[D]))
            Gam[A][B][C] = sp.cancel(s / 2)
print("Christoffel %.2fs" % (time.time() - t0))

# dGam
dGam = [[[[sp.diff(Gam[A][B][C], coords[D]) for D in range(4)] for C in range(4)] for B in range(4)] for A in range(4)]
print("dChristoffel %.2fs" % (time.time() - t0))

# Riemann 上指标 R^A_BCD，先做 l^mu 收缩：R_{mu nu rho sig} l^mu
I = sp.I
l = sp.Matrix([(r**2 + a**2) / Del, 1, 0, a / Del])
n = sp.Matrix([(r**2 + a**2) / (2 * Sig), -Del / (2 * Sig), 0, a / (2 * Sig)])
mb = sp.Matrix([I * a * sp.sin(th), 0, 1, I / sp.sin(th)]) / (sp.sqrt(2) * (r - I * a * sp.cos(th)))
m = sp.Matrix([-I * a * sp.sin(th), 0, 1, -I / sp.sin(th)]) / (sp.sqrt(2) * (r + I * a * sp.cos(th)))


def riemann_exprs():
    R = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for A in range(4):
        for B in range(4):
            for C in range(4):
                for D in range(C + 1, 4):
                    s = dGam[A][B][D][C] - dGam[A][B][C][D]
                    for E in range(4):
                        s += Gam[A][C][E] * Gam[E][B][D] - Gam[A][D][E] * Gam[E][B][C]
                    R[A][B][C][D] = s
                    R[A][B][D][C] = -s
    return R


Rup = riemann_exprs()
print("Riemann(up) %.2fs" % (time.time() - t0))

# 只算 Ricci（收缩）先
Ric = sp.zeros(4, 4)
for B in range(4):
    for D in range(4):
        s = 0
        for A in range(4):
            s += Rup[A][B][A][D]
        Ric[B, D] = sp.cancel(s)
print("Ricci %.2fs" % (time.time() - t0))

pt = {M: sp.Rational(1), a: sp.Rational(1, 2), r: sp.Rational(7, 2), th: sp.Rational(1, 1)}
print("Ricci 数值抽查:", [[sp.N(Ric[i, j].subs(pt), 20) for j in range(4)] for i in range(2)])
print("耗时 %.2fs" % (time.time() - t0))

# Weyl 标量 Psi2 = R_{mu nu rho sig} l^mu m^nu mbar^rho n^sig (真空下 C=R)
# 逐步收缩：先 R_{mu nu rho sig} -> 降指标
Rdn = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
for MU in range(4):
    for NU in range(4):
        for RHO in range(4):
            for SIG in range(4):
                s = 0
                for A in range(4):
                    s += g[MU, A] * Rup[A][NU][RHO][SIG]
                Rdn[MU][NU][RHO][SIG] = s
print("降指标 %.2fs" % (time.time() - t0))


def contract(expr4, vec):
    out = [[[sp.expand(expr4[x][y][z][0] * vec[0] + expr4[x][y][z][1] * vec[1] +
                       expr4[x][y][z][2] * vec[2] + expr4[x][y][z][3] * vec[3])
             for z in range(4)] for y in range(4)] for x in range(4)]
    return out


S1 = contract(Rdn, l)          # S1[nu][rho][sig]
S2 = [[sp.expand(S1[x][0][z] * m[0] + S1[x][1][z] * m[1] + S1[x][2][z] * m[2] + S1[x][3][z] * m[3])
       for z in range(4)] for x in range(4)]
S3 = [sp.expand(S2[0][z] * mb[0] + S2[1][z] * mb[1] + S2[2][z] * mb[2] + S2[3][z] * mb[3]) for z in range(4)]
psi2 = sp.expand(S3[0] * n[0] + S3[1] * n[1] + S3[2] * n[2] + S3[3] * n[3])
print("Psi2 表达式 %.2fs" % (time.time() - t0))
val = sp.simplify(psi2.subs(pt))
print("Psi2 数值:", sp.N(val, 25))
target = -1 / (sp.Rational(7, 2) - I * sp.Rational(1, 2) * sp.cos(sp.Rational(1, 1)))**3
print("目标 -M/(r-ia cos th)^3:", sp.N(target, 25))
print("差:", sp.N(sp.simplify(val - target), 25))
print("总耗时 %.2fs" % (time.time() - t0))
