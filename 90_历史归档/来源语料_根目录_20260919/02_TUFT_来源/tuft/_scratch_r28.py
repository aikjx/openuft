# -*- coding: utf-8 -*-
"""原型 v3：检查 ODE 极点阶数与最小分母，判定递推阶数。"""
import sympy as sp

y = sp.symbols("y")
rp, rm, om, A, aa = sp.symbols("r_p r_m omega A aa")
s = sp.Integer(-2)
D = rp - rm
r = (rp - y * rm) / (1 - y)
Dlt = y * D ** 2 / (1 - y) ** 2
K = (r ** 2 + rp * rm) * om - aa
lam = A + rp * rm * om ** 2 - 2 * aa * om
V = K ** 2 / Dlt - 2 * sp.I * s * (r - (rp + rm) / 2) * K / Dlt + 4 * sp.I * s * om * r - lam
W = (s + 1) / y + 2 * s / (1 - y)
U = V / (y * (1 - y) ** 2)
sip = (om * rp * (rp + rm) - aa) / D
sim = (om * rm * (rp + rm) - aa) / D
u = -s - sp.I * sip
v = -1 + s + sp.I * sim
rho = sp.I * om * D / (1 - y) ** 2 + u / y + (u + v) / (1 - y)
P = 2 * rho + W
Q = sp.diff(rho, y) + rho ** 2 + W * rho + U

Ode = sp.Function("S")(y)
expr = sp.diff(Ode, y, 2) + P * sp.diff(Ode, y) + Q * Ode

for mul in [y * (1 - y) ** 2, y * (1 - y) ** 3, y ** 2 * (1 - y) ** 3, y ** 2 * (1 - y) ** 4,
            y ** 2 * (1 - y) ** 5, y ** 2 * (1 - y) ** 6]:
    E2 = sp.cancel(expr * mul)
    num, den = sp.fraction(E2)
    if y not in den.free_symbols:
        poly = sp.expand(num / den)
        c2 = sp.expand(poly.coeff(sp.Derivative(Ode, y, 2)))
        c1 = sp.expand(poly.coeff(sp.Derivative(Ode, y)))
        c0 = sp.expand(poly.coeff(Ode))
        print("mul=%s den=const  degs=(%s,%s,%s)" % (mul, sp.degree(c2, y), sp.degree(c1, y), sp.degree(c0, y)))
    else:
        print("mul=%s 未清净" % mul)
