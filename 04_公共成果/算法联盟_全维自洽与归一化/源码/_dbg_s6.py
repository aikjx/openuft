# -*- coding: utf-8 -*-
import sympy as sp

x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
X = [x0, x1, x2, x3]
SGN = [1, -1, -1, -1]
II = sp.I
kap = sp.symbols("kappa", positive=True)
be = sp.symbols("e_charge", real=True)
Phi = sp.Function("Phi")(*X)
Phic = sp.Function("Phic")(*X)
U1A = [sp.Function("a%d" % m)(*X) for m in range(4)]
DJe = [sp.diff(Phi, X[m]) - II * be * U1A[m] * Phi for m in range(4)]
Dc = [sp.diff(Phic, X[m]) + II * be * U1A[m] * Phic for m in range(4)]
LagU1 = sum(Dc[m] * SGN[m] * DJe[m] for m in range(4)) - kap ** 2 * Phic * Phi
eqs6 = sp.euler_equations(LagU1, [Phic], X)
el6 = sp.expand(eqs6[0].lhs)
print("el6 =", sp.sstr(el6))


def D2U1rho(rho):
    out = 0
    for m in range(4):
        inner = SGN[rho] * DJe[rho]
        out += SGN[m] * SGN[rho] * (sp.diff(inner, X[m]) - II * be * U1A[m] * inner)
    return sp.expand(out)


D2Phi = sum(D2U1rho(r_) for r_ in range(4))
target6 = sp.expand(D2Phi + kap ** 2 * Phi)
print("target6 =", sp.sstr(target6))
print("el6 - target6 =", sp.sstr(sp.expand(el6 - target6)))
print("el6 + target6 =", sp.sstr(sp.expand(el6 + target6)))
# 实/虚分解：令 Phi = (phi1 + I phi2), Phic = (phi1 - I phi2)
p1 = sp.Function("phi1")(*X)
p2 = sp.Function("phi2")(*X)
repl = {Phi: p1 + II * p2, Phic: p1 - II * p2}
el6r = sp.expand(el6.subs(repl))
print("el6 real-decomp =", sp.sstr(el6r))
targetr = sp.expand(target6.subs(repl))
print("target real-decomp =", sp.sstr(targetr))
print("el6r + targetr =", sp.sstr(sp.expand(el6r + targetr)))
