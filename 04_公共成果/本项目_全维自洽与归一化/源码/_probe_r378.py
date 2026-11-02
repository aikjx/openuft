# -*- coding: utf-8 -*-
# r378 探针 4：修正散度公式 + mp.expm
import sys, time
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp
from fractions import Fraction
mp.mp.dps = 70
t0 = time.time()

t, p = sp.symbols("t p", real=True)
a = t**p
gf = sp.Matrix(sp.diag(-1, a**2, a**2, a**2))
sx, sy, sz = sp.symbols("x y z", real=True)
X4 = (t, sx, sy, sz)
gf_inv = sp.simplify(gf.inv())
Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for aa in range(4):
    for bb in range(4):
        for cc in range(4):
            Gam[aa][bb][cc] = sp.simplify(sum(gf_inv[aa, d] * (sp.diff(gf[d, bb], X4[cc]) + sp.diff(gf[d, cc], X4[bb]) - sp.diff(gf[bb, cc], X4[d])) for d in range(4)) / 2)
Ric = sp.Matrix(4, 4, lambda m, n: sp.simplify(sum(sp.diff(Gam[aa][m][n], X4[aa]) for aa in range(4))
                                              - sum(sp.diff(Gam[aa][aa][n], X4[m]) for aa in range(4))
                                              + sum(Gam[aa][aa][bb] * Gam[bb][m][n] for aa in range(4) for bb in range(4))
                                              - sum(Gam[aa][m][bb] * Gam[bb][aa][n] for aa in range(4) for bb in range(4))))
Rsc = sp.simplify(sum(gf_inv[m, n] * Ric[m, n] for m in range(4) for n in range(4)))

def div_up(T):
    Tup = gf_inv * T * gf_inv
    return [sp.simplify(sum(sp.diff(Tup[m, aa], X4[m]) + sum(Gam[m][m][r] * Tup[r, aa] for r in range(4))
                           + sum(Gam[aa][m][r] * Tup[m, r] for r in range(4)) for m in range(4))) for aa in range(4)]

G = sp.Matrix(4, 4, lambda m, n: sp.simplify(Ric[m, n] - Rsc * gf[m, n] / 2))
Gw = sp.Matrix(4, 4, lambda m, n: sp.simplify(Ric[m, n] - Rsc * gf[m, n] / 4))
print("P2d div G =", div_up(G))
print("P2d div Gwrong =", div_up(Gw), " t=%.1f" % (time.time() - t0))

# pp-wave 再验
u, v, xx, yy = sp.symbols("u v x y", real=True)
H = xx**2 + yy**2
gp = sp.Matrix([[H, -sp.Rational(1, 2), 0, 0], [-sp.Rational(1, 2), 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
XP = (u, v, xx, yy)
gp_inv = sp.simplify(gp.inv())
GamP = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for aa in range(4):
    for bb in range(4):
        for cc in range(4):
            GamP[aa][bb][cc] = sp.simplify(sum(gp_inv[aa, d] * (sp.diff(gp[d, bb], XP[cc]) + sp.diff(gp[d, cc], XP[bb]) - sp.diff(gp[bb, cc], XP[d])) for d in range(4)) / 2)
RicP = sp.Matrix(4, 4, lambda m, n: sp.simplify(sum(sp.diff(GamP[aa][m][n], XP[aa]) for aa in range(4))
                                                - sum(sp.diff(GamP[aa][aa][n], XP[m]) for aa in range(4))
                                                + sum(GamP[aa][aa][bb] * GamP[bb][m][n] for aa in range(4) for bb in range(4))
                                                - sum(GamP[aa][m][bb] * GamP[bb][aa][n] for aa in range(4) for bb in range(4))))
RscP = sp.simplify(sum(gp_inv[m, n] * RicP[m, n] for m in range(4) for n in range(4)))
EinP = sp.Matrix(4, 4, lambda m, n: sp.simplify(RicP[m, n] - RscP * gp[m, n] / 2))
EinPup = gp_inv * EinP * gp_inv
divP = [sp.simplify(sum(sp.diff(EinPup[m, aa], XP[m]) + sum(GamP[m][m][r] * EinPup[r, aa] for r in range(4)) + sum(GamP[aa][m][r] * EinPup[m, r] for r in range(4)) for m in range(4))) for aa in range(4)]
print("P2e pp-wave G_uu =", EinP[0, 0], " div =", divP)

# P6 全局协变
s1 = mp.matrix([[0, 1], [1, 0]]); s2 = mp.matrix([[0, -1j], [1j, 0]]); s3 = mp.matrix([[1, 0], [0, -1]])
sig = [s1, s2, s3]
def fA(k, i, X):
    return (mp.sin(mp.mpf("1.3") * X[0] + k + i) + mp.cos(mp.mpf("0.7") * X[1] - 2 * k + i)
            + X[2] ** 2 * (mp.mpf(0.1) * k + mp.mpf(0.2)) + X[3] * (mp.mpf(0.3) - mp.mpf(0.1) * i))
def dfA(k, i, X, m):
    if m == 0:
        return mp.mpf("1.3") * mp.cos(mp.mpf("1.3") * X[0] + k + i)
    if m == 1:
        return -mp.mpf("0.7") * mp.sin(mp.mpf("0.7") * X[1] - 2 * k + i)
    if m == 2:
        return 2 * X[2] * (mp.mpf(0.1) * k + mp.mpf(0.2))
    return mp.mpf("0.3") - mp.mpf(0.1) * i
def A_mat(m, X):
    return sum(fA(m, a, X) * sig[a] for a in range(3)) / 2
def dA_mat(m, n, X):
    return sum(dfA(m, a, X, n) * sig[a] for a in range(3)) / 2
GG = mp.mpf("0.7")
def F_exact(X):
    return {(m, n): dA_mat(n, m, X) - dA_mat(m, n, X) - 1j * GG * (A_mat(m, X) * A_mat(n, X) - A_mat(n, X) * A_mat(m, X)) for m in range(4) for n in range(4)}
X0 = [mp.mpf("0.91"), mp.mpf("1.27"), mp.mpf("0.63"), mp.mpf("1.05")]
al = [lambda X, a=a: fA(10 + a, a, X) for a in range(3)]
M = sum(al[a](X0) * sig[a] for a in range(3)) / 2
Uc = mp.expm(1j * GG * M)
F = F_exact(X0)
mx = 0
for m in range(4):
    for n in range(4):
        Fp = (Uc * dA_mat(n, m, X0) * Uc.H) - (Uc * dA_mat(m, n, X0) * Uc.H) - 1j * GG * (Uc * A_mat(m, X0) * Uc.H * Uc * A_mat(n, X0) * Uc.H - Uc * A_mat(n, X0) * Uc.H * Uc * A_mat(m, X0) * Uc.H)
        rhs = Uc * F[(m, n)] * Uc.H
        for aa in range(2):
            for bb in range(2):
                mx = max(mx, abs(Fp[aa, bb] - rhs[aa, bb]))
print("P6 global residual =", mp.nstr(mx, 5), " t=%.1f" % (time.time() - t0))

# P7 γ
I2 = sp.eye(2); Z2 = sp.zeros(2, 2)
s1s = sp.Matrix([[0, 1], [1, 0]]); s2s = sp.Matrix([[0, -sp.I], [sp.I, 0]]); s3s = sp.Matrix([[1, 0], [0, -1]])
g0 = sp.Matrix(sp.BlockMatrix([[I2, Z2], [Z2, -I2]]))
gi = [sp.Matrix(sp.BlockMatrix([[Z2, si], [-si, Z2]])) for si in (s1s, s2s, s3s)]
g5 = sp.I * g0 * gi[0] * gi[1] * gi[2]
print("P7 g5 =", g5.tolist(), " g5^2 =", sp.simplify(g5 * g5)[0, 0], " herm =", sp.simplify(g5.H - g5) == sp.zeros(4, 4))
print("P7 g0 g0 g0 =", sp.simplify(g0 * g0 * g0)[0, 0], " g0 g5 g0 =", sp.simplify(g0 * g5 * g0).tolist())

# P8 异常
fields = [(6, Fraction(1, 6)), (3, Fraction(-2, 3)), (3, Fraction(1, 3)), (2, Fraction(-1, 2)), (1, Fraction(1))]
Y1 = sum(n * Y for n, Y in fields); Y3 = sum(n * Y ** 3 for n, Y in fields)
T2Y = sum(n * Fraction(1, 4) * Y for n, Y in fields if n in (6, 2))
SU3Y = sum(n / 3 * Y for n, Y in fields if n in (6, 3))
print("P8 =", Y1, Y3, T2Y, SU3Y)
bad = [(6, Fraction(1, 6)), (3, Fraction(-2, 3)), (3, Fraction(-1, 2)), (2, Fraction(-1, 2)), (1, Fraction(1))]
print("P8 bad Y3 =", sum(n * Y ** 3 for n, Y in bad))

# P9 Green
print("P9 lap(1/r)@1.3 =", mp.nstr(mp.diff(lambda rr: mp.diff(lambda s: 1 / s, rr), mp.mpf("1.3")), 4), " -4pi =", mp.nstr(-4 * mp.pi, 10))
print("P9 (lap-1)Yukawa@1.3 =", mp.nstr(mp.diff(lambda rr: mp.diff(lambda s: mp.e ** (-s) / s, rr), mp.mpf("1.3")) - mp.e ** (-mp.mpf("1.3")) / mp.mpf("1.3"), 4))

# P10 单圈
aem_inv = mp.mpf("127.95"); sw2 = mp.mpf("0.23122"); as_inv = 1 / mp.mpf("0.1180")
a1i = mp.mpf(3) / 5 * (1 - sw2) * aem_inv; a2i = sw2 * aem_inv; a3i = as_inv
b1, b2, b3 = mp.mpf(41) / 10, mp.mpf(-19) / 6, mp.mpf(-7)
L12 = 2 * mp.pi * (a1i - a2i) / (b1 - b2); L23 = 2 * mp.pi * (a2i - a3i) / (b2 - b3)
MZ = mp.mpf("91.1876"); mu12 = MZ * mp.e ** L12; mu23 = MZ * mp.e ** L23
al1 = lambda L: a1i - b1 / (2 * mp.pi) * L; al3 = lambda L: a3i - b3 / (2 * mp.pi) * L
d = al3(L12) - al1(L12)
print("P10 ai =", [mp.nstr(x, 10) for x in (a1i, a2i, a3i)])
print("P10 mu12=%s mu23=%s ratio=%s mismatch=%s rel=%s" % (mp.nstr(mu12, 8), mp.nstr(mu23, 8), mp.nstr(mu23 / mu12, 5), mp.nstr(d, 5), mp.nstr(abs(d) / al1(L12), 4)))
print("total %.1f s" % (time.time() - t0))
