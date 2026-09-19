# -*- coding: utf-8 -*-
"""严格符号推导: Schwarzschild 标量 KG (M=1) -> Leaver 三项递推."""
import sympy as sp

z, w, l = sp.symbols('z w l', real=False)
n = sp.symbols('n', integer=True, positive=True)

# ---- ODE (*) in z, R_zz + P R_z + Q R = 0 ----
P = (1 - 3*z)/(z*(1 - z))
Q = 4*w**2/(z**2*(1-z)**4) - l*(l+1)/(z*(1-z)**2)

# ---- Leaver prefactor (drop constant 2^{-2iw}) ----
# R = exp(2 i w/(1-z)) * z^{-2 i w} * (1-z^2)^{i w} * F(z)
F = sp.Function('F')(z)
pref = sp.exp(2*sp.I*w/(1-z)) * z**(-2*sp.I*w) * (1-z*z)**(sp.I*w)
R = pref*F

# apply ODE operator, divide out pref (and exp), collect coeffs of F,F',F''
expr = sp.diff(R, z, 2) + P*sp.diff(R, z) + Q*R
expr = sp.simplify(expr/pref)
# now expr = A2 F'' + A1 F' + A0 F
A2 = sp.expand(sp.collect(sp.expand(expr), sp.diff(F,z,2)).coeff(sp.diff(F,z,2)))
A1 = sp.expand(sp.collect(sp.expand(expr), sp.diff(F,z)).coeff(sp.diff(F,z)))
A0 = sp.simplify(expr - A2*sp.diff(F,z,2) - A1*sp.diff(F,z))

print("=== F(z) ODE (prefactor removed) ===")
print("A2 =", sp.simplify(A2))
print("A1 =", sp.simplify(sp.together(A1)))
print("A0 =", sp.simplify(sp.together(A0)))

# multiply ODE through by common denominator to get polynomial coeffs
A0t = sp.together(A0)
A1t = sp.together(A1)
A2t = sp.together(A2)
# denom of A2
den = sp.together(A2).as_numer_denom()[1]
print("\ncommon denom (A2):", sp.factor(den))
poly0 = sp.expand(A0*den)
poly1 = sp.expand(A1*den)
poly2 = sp.expand(A2*den)
print("\nAfter multiplying by denom:")
print(" poly2 F'' + poly1 F' + poly0 F = 0")
print(" poly2 =", sp.factor(poly2))
print(" poly1 =", sp.factor(poly1))
print(" poly0 =", sp.factor(poly0))
