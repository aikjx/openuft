# -*- coding: utf-8 -*-
"""SYM_PROTOTYPE: static spherical reduction, exact Einstein tensor."""
import sympy as sp

r = sp.Symbol('r', positive=True)
nu = sp.Function('nu')(r)
lam = sp.Function('lam')(r)
Lam_c = sp.Symbol('Lambda_c')

# coords: 0=t, 1=r, 2=th, 3=ph
g = sp.zeros(4, 4)
g[0, 0] = -sp.exp(2 * nu)
g[1, 1] = sp.exp(2 * lam)
g[2, 2] = r ** 2
g[3, 3] = r ** 2 * sp.sin(sp.Symbol('th')) ** 2
ginv = g.inv()
coords = [sp.Symbol('t'), r, sp.Symbol('th'), sp.Symbol('ph')]

# d g / d x^rho
dg = [sp.zeros(4, 4) for _ in range(4)]
for rho in range(4):
    for a in range(4):
        for b in range(4):
            dg[rho][a, b] = sp.simplify(sp.diff(g[a, b], coords[rho]))

# Christoffel
Gamma = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
for rho in range(4):
    for mu in range(4):
        for sig in range(4):
            s = sp.S.Zero
            for lam_ in range(4):
                s += ginv[rho, lam_] * (dg[lam_][mu, sig] + dg[lam_][sig, mu] - dg[mu][lam_, sig])
            Gamma[rho][mu][sig] = sp.simplify(s)

# Ricci
Ric = sp.zeros(4, 4)
for mu in range(4):
    for nu_ in range(4):
        s = sp.S.Zero
        for rho in range(4):
            d1 = sp.diff(Gamma[rho][mu][nu_], coords[rho])
            d2 = sp.diff(Gamma[rho][nu_][mu], coords[rho])
            s += d1 - d2
        for rho in range(4):
            for lam_ in range(4):
                s += Gamma[rho][mu][lam_] * Gamma[lam_][nu_][rho]
                s -= Gamma[rho][nu_][lam_] * Gamma[lam_][mu][rho]
        Ric[mu, nu_] = sp.simplify(s)

R = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
E = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        E[a, b] = sp.simplify(Ric[a, b] - sp.Rational(1, 2) * g[a, b] * R + Lam_c * g[a, b])

print("R =", sp.simplify(R))
print()
print("E_tt =", sp.collect(sp.expand(E[0, 0] / sp.exp(2 * lam)), [sp.diff(nu, r), sp.diff(lam, r)]))
print()
print("E_rr =", sp.collect(sp.expand(E[1, 1] / sp.exp(2 * lam)), [sp.diff(nu, r), sp.diff(lam, r)]))
print()
print("E_thth =", sp.collect(sp.expand(E[2, 2] / r ** 2), [sp.diff(nu, r), sp.diff(lam, r)]))
print()
print("trace check: E_trace =", sp.simplify(sum(ginv[a, b] * E[a, b] for a in range(4) for b in range(4))))
print("expected -R + 4 Lam_c =", sp.simplify(-R + 4 * Lam_c))
