# -*- coding: utf-8 -*-
import sympy as sp

X = sp.symbols("x0 x1 x2 x3")
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

def DKG_correct():
    """正确 U(1) 协变 d'Alembertian：D_mu D^mu Phi = sum_mu eta^{mu mu} D_mu(D_mu Phi)。"""
    out = 0
    for m in range(4):
        Dm = sp.diff(Phi, X[m]) - II * be * U1A[m] * Phi          # D_mu Phi
        DmuDmu = sp.diff(Dm, X[m]) - II * be * U1A[m] * Dm        # D_mu(D_mu Phi)
        out += SGN[m] * DmuDmu                                    # eta^{mu mu} 收缩（仅此处带 SGN）
    return sp.expand(out)

c = DKG_correct()
print("DKG =", sp.sstr(c))
print("el6 - DKG =", sp.sstr(sp.expand(el6 - c)))
print("el6 + DKG =", sp.sstr(sp.expand(el6 + c)))

# ---- S3-07 with correct operator ----
Jsrc = sp.Function("J")(*X)
alpha_f = sp.Function("alpha")(*X)
src_eq_sym = (c + kap ** 2 * Phi - Jsrc)
eps_s = sp.symbols("epsilon")
exp_small = 1 + II * eps_s * alpha_f
Phi_p = sp.expand(exp_small * Phi)
Ap_new = [sp.expand(U1A[m] + eps_s * sp.diff(alpha_f, X[m]) / be) for m in range(4)]

def D2_with_correct(field, pot_arr):
    out = 0
    for m in range(4):
        Dm = sp.diff(field, X[m]) - II * be * pot_arr[m] * field
        DmuDmu = sp.diff(Dm, X[m]) - II * be * pot_arr[m] * Dm
        out += SGN[m] * DmuDmu
    return sp.expand(out)

transformed = sp.expand(D2_with_correct(Phi_p, Ap_new) + kap ** 2 * Phi_p - exp_small * Jsrc)
expected = sp.expand(exp_small * src_eq_sym)
diff7 = sp.expand(transformed - expected)
print("\nS3-07 full diff =", sp.sstr(diff7))
print("S3-07 diff coeff eps^1 =", sp.sstr(sp.expand(diff7).coeff(eps_s, 1)))
print("S3-07 diff coeff eps^2 =", sp.sstr(sp.expand(diff7).coeff(eps_s, 2)))
