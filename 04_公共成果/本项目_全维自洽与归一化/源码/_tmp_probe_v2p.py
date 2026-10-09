# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import sympy as sp

x, t = sp.symbols('x t', real=True)
a, lam, Om, cc, mm = sp.symbols('a lam Omega c m', positive=True)

A = sp.sqrt(2 * a / lam)
k = sp.sqrt(a)
f = A * sp.sech(k * x)
expr = -sp.diff(f, x, 2) + a * f - lam * f ** 3
s1 = sp.simplify(sp.expand_trig(sp.simplify(expr)))
print("P-04 sech residual (simplify):", s1)
vals = []
try:
    import mpmath as mp
    mp.mp.dps = 40

    def res_numeric(av, lv):
        ff = mp.sqrt(2 * mp.mpf(av) / mp.mpf(lv)) / mp.cosh(mp.sqrt(mp.mpf(av)) * mp.mpf(0.7))
        # numeric second derivative via mpmath diff
        g = lambda xx: mp.sqrt(2 * mp.mpf(av) / mp.mpf(lv)) / mp.cosh(mp.sqrt(mp.mpf(av)) * xx)
        d2 = mp.diff(g, mp.mpf(0.7), 2)
        return -d2 + mp.mpf(av) * ff - mp.mpf(lv) * ff ** 3

    print("numeric residual:", mp.nstr(res_numeric(1.3, 0.7), 8))
except Exception as e:
    print("numeric err", e)

# virial integrals
A2 = A ** 2
k2 = k ** 2
T = sp.integrate(sp.diff(f, x) ** 2, (x, -sp.oo, sp.oo))
print("T =", sp.simplify(T))
Vpot = sp.integrate(a * f ** 2 - lam * f ** 4 / 2, (x, -sp.oo, sp.oo))
print("V =", sp.simplify(Vpot))
try:
    print("T/V =", sp.simplify(T / Vpot))
except Exception as e:
    print("ratio err", e)
