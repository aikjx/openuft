# -*- coding: utf-8 -*-
import sympy as sp

r = sp.Symbol('r', positive=True)
nu = sp.Function('nu')(r)
lam = sp.Function('lam')(r)
th = sp.Symbol('th')

g = sp.zeros(4, 4)
g[0, 0] = -sp.exp(2 * nu)
g[1, 1] = sp.exp(2 * lam)
g[2, 2] = r ** 2
g[3, 3] = r ** 2 * sp.sin(th) ** 2
ginv = g.inv()
coords = [sp.Symbol('t'), r, th, sp.Symbol('ph')]

dg = [sp.zeros(4, 4) for _ in range(4)]
for rho in range(4):
    for a in range(4):
        for b in range(4):
            dg[rho][a, b] = sp.simplify(sp.diff(g[a, b], coords[rho]))

Gamma = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
for rho in range(4):
    for mu in range(4):
        for sig in range(4):
            s = sp.S.Zero
            for L in range(4):
                s += ginv[rho, L] * (dg[L][mu, sig] + dg[L][sig, mu] - dg[mu][L, sig])
            Gamma[rho][mu][sig] = sp.simplify(s / 2)

tests = [(0, 1, 1), (1, 0, 0), (1, 1, 1), (1, 2, 2), (2, 1, 2), (2, 0, 0)]
for (a, b, c) in tests:
    print("Gamma^%d_%d%d = %s" % (a, b, c, sp.simplify(Gamma[a][b][c])))
print()
print("dg[1] (d/dr):")
for a in range(4):
    for b in range(4):
        if dg[1][a, b] != 0:
            print("  d%d_dr%d = %s" % (a, b, sp.simplify(dg[1][a, b])))
print()
print("dg[3] (d/dphi):", [sp.simplify(dg[3][a, b]) for a in range(4) for b in range(4) if dg[3][a, b] != 0])

Ric = sp.zeros(4, 4)
for mu in range(4):
    for nu_ in range(4):
        s = sp.S.Zero
        for rho in range(4):
            s += sp.diff(Gamma[rho][mu][nu_], coords[rho]) - sp.diff(Gamma[rho][nu_][mu], coords[rho])
        for rho in range(4):
            for L in range(4):
                s += Gamma[rho][mu][L] * Gamma[L][nu_][rho] - Gamma[rho][nu_][L] * Gamma[L][mu][rho]
        Ric[mu, nu_] = sp.simplify(s)
print()
for (a, b) in [(0, 0), (1, 1), (2, 2)]:
    print("Ric_%d%d = %s" % (a, b, sp.simplify(Ric[a, b])))
