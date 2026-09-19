# -*- coding: utf-8 -*-
"""
TUFT v10 线一·续: 标量 KG Leaver 系数严格推导 (2i w convention) + 三模态收敛表
New equation line: E337.

Schwarzschild M=1, r_h=2, f=1-2/r, R=r*psi.
Tortoise: dr*/dr = 1/f = r/(r-2)  =>  r* = r + 2 ln|r/2 - 1|   (coeff 2)
Variable: z = 1 - 2/r   (z=0 horizon, z->1 infinity)
Radial eq: d2R/dr*2 + [w^2 - V] R = 0,  V = f l(l+1)/r^2.

Gauge: R = exp(i w r*) u(z).  Then u obeys an ODE with NO exponentials.
Near horizon z->0: r* ~ 2 ln z, so exp(i w r*) ~ z^{2 i w}.
Horizon Frobenius on R: rho = +- 2 i w  (indicial rho^2 + 4 w^2 = 0).
Ingoing branch: R ~ exp(-i w r*) ~ z^{-2 i w}.  Hence u = exp(-i w r*) R ~ z^{-4 i w}.
Leaver ansatz:
   R(z) = exp(i w r*) * z^{-4 i w} * S(z),  S(z) = sum a_n z^n.
(this is the "2 i w convention": net horizon exponent on z is -2 i w.)
"""
import time, io, os
import numpy as np
import sympy as sp
from scipy.optimize import root

out = io.StringIO()
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.write(s + "\n")

t0 = time.time()
p("="*78)
p("TUFT v10 LINE1 CONT: SCALAR KG LEAVER COEFFICIENTS (2i w convention)")
p("New equation line: E337")
p("="*78)

# ---------- symbolic setup ----------
r, z = sp.symbols('r z', positive=True)
w, lam = sp.symbols('omega lambda')   # lambda = l(l+1)
M = sp.Integer(1)
f = 1 - 2*M/r
rstar = r + 2*M*sp.log(r/(2*M) - 1)
r_inz = 2*M/(1-z)
rstar_inz = sp.simplify(rstar.subs(r, r_inz))

p("[E337] Schwarzschild scalar radial, M=1, r_h=2, f=1-2/r")
p("[E338] r* = r + 2 ln|r/2 - 1|   (coeff 2; dr*/dr = r/(r-2))")
p("[E339] z = 1 - 2/r ;  r = 2/(1-z)")
p("[E340] r*(z) =", sp.simplify(rstar_inz))

# dz/dr* = (dz/dr)/(dr*/dr) = (2/r^2) / (r/(r-2)) = 2(r-2)/r^3
dz_drstar = sp.simplify((2/r**2) / (1/f))
A = sp.simplify(dz_drstar.subs(r, r_inz))   # = z(1-z)^2/2
Apr = sp.diff(A, z)
p("[E341] A(z)=dz/dr* =", A)

# ODE for R in z:  R_zz + P R_z + Q R = 0
# Scalar KG potential: V = f[l(l+1)/r^2 + f f'/r] = f[l(l+1)/r^2 + 2M/r^3].
# (The ff'/r term is REQUIRED: without it l=0 has V=0 and no QNM.)
fp = 2*M/r**2
V = f*(lam/r**2 + fp/r)
V_inz = sp.simplify(V.subs(r, r_inz))
Pz = sp.simplify(Apr/A)
Qz = sp.simplify((w**2 - V_inz)/A**2)
p("[E342] P(z) =", sp.together(sp.cancel(Pz)))
p("       Q(z) =", sp.together(sp.cancel(Qz)))

# indicial
p("[E343] horizon indicial: rho^2 + 4 w^2 = 0  => rho = +- 2 i w")

# ---------- gauge transform R = exp(i w r*) u ----------
# u_z = dr*/dz = 1/A
rs_z = 1/A
rs_zz = sp.diff(rs_z, z)
P_u = sp.simplify(Pz + 2*sp.I*w*rs_z)
Q_u = sp.simplify(Qz + sp.I*w*Pz*rs_z + sp.I*w*rs_zz - w**2*rs_z**2)
p("[E344] u-equation (R = e^{i w r*} u):  u_zz + Pu u_z + Qu u = 0")
p("       Pu(z) =", sp.together(sp.cancel(P_u)))
p("       Qu(z) =", sp.together(sp.cancel(Q_u)))

# horizon indicial for u: sigma^2 + 4 i w sigma = 0 -> sigma = 0, -4 i w
# ingoing branch: sigma = -4 i w.  Set u = z^{-4 i w} S(z).
# factor z^{-4 i w}: v = z^{4 i w} u  (so u = z^{-4iw} v, v analytic)
# Derive ODE for v.
Sfun = sp.Function('S')(z)
u_expr = z**(-4*sp.I*w) * Sfun
uz = sp.diff(u_expr, z)
uzz = sp.diff(uz, z)
Lu = sp.simplify(uzz + P_u*uz + Q_u*u_expr)
op = sp.simplify(Lu / z**(-4*sp.I*w))   # operator acting on S (no S in denom)
p("[E345] operator on S after u = z^{-4 i w} S:")
op = sp.together(sp.cancel(op))
p("       L[S] =", op)

Spp = sp.diff(Sfun,(z,2)); Sp = sp.diff(Sfun,z)
op_num, op_den = sp.together(op).as_numer_denom()
op_num = sp.expand(op_num)
A2 = sp.expand(op_num.coeff(Spp))
A1 = sp.expand(op_num.coeff(Sp))
A0 = sp.expand(op_num.coeff(Sfun))
p("[E346] A2 S'' + A1 S' + A0 S  (numerator over", op_den, "):")
p("       A2 =", sp.simplify(A2))
p("       A1 =", sp.simplify(A1))
p("       A0 =", sp.simplify(A0))

# The equation is numerator/denom = 0, i.e. numerator = 0.
# A2/A1/A0 are already polynomial in z (no further clearing needed).
A2p = sp.expand(A2)
A1p = sp.expand(A1)
A0p = sp.expand(A0)
p("[E347] numerator coefficients (already polynomial in z):")
p("       A2p =", sp.simplify(sp.factor(A2p)))
p("       A1p =", sp.simplify(sp.factor(A1p)))
p("       A0p =", sp.simplify(sp.factor(A0p)))

P2 = sp.Poly(sp.expand(A2p), z)
P1 = sp.Poly(sp.expand(A1p), z)
P0 = sp.Poly(sp.expand(A0p), z)
def coeff_at(P, k):
    if k < 0 or k > P.degree(): return sp.Integer(0)
    return sp.expand(P.coeff_monomial(z**k))

n = sp.symbols('n', integer=True, nonnegative=True)
def collect_recurrence():
    cn = sp.Integer(0); ch = sp.Integer(0); cp = sp.Integer(0)
    # A2p S'':  i + k - 2 = n => k = n - i + 2 ; coeff k(k-1)
    for i in range(0, P2.degree()+1):
        c = coeff_at(P2, i); kk = n - i + 2
        if kk == n+1: cn += (n+1)*n*c
        elif kk == n: ch += n*(n-1)*c
        elif kk == n-1: cp += (n-1)*(n-2)*c
    # A1p S' :  i + k - 1 = n => k = n - i + 1 ; coeff k
    for i in range(0, P1.degree()+1):
        c = coeff_at(P1, i); kk = n - i + 1
        if kk == n+1: cn += (n+1)*c
        elif kk == n: ch += n*c
        elif kk == n-1: cp += (n-1)*c
    # A0p S  :  i + k = n => k = n - i
    for i in range(0, P0.degree()+1):
        c = coeff_at(P0, i); kk = n - i
        if kk == n+1: cn += c
        elif kk == n: ch += c
        elif kk == n-1: cp += c
    return sp.simplify(cn), sp.simplify(ch), sp.simplify(cp)

alpha_n, beta_n, gamma_n = collect_recurrence()
p("")
p("[E348] THREE-TERM RECURRENCE: alpha_n a_{n+1} + beta_n a_n + gamma_n a_{n-1} = 0")
p("       alpha_n =", sp.simplify(sp.factor(alpha_n)))
p("       beta_n  =", sp.simplify(sp.factor(beta_n)))
p("       gamma_n =", sp.simplify(sp.factor(gamma_n)))
p("")
p("[E349] expanded (for codegen):")
p("       alpha_n =", sp.expand(alpha_n))
p("       beta_n  =", sp.expand(beta_n))
p("       gamma_n =", sp.expand(gamma_n))

# ---------- numeric ----------
p("")
p("="*78)
p("NUMERICAL: Leaver continued fraction -> QNM roots")
p("="*78)

def make_coeffs(ll, ww):
    ww = complex(ww); lamv = ll*(ll+1)
    sub = {w: ww, lam: lamv}
    ae = sp.expand(alpha_n).subs(sub)
    be = sp.expand(beta_n).subs(sub)
    ge = sp.expand(gamma_n).subs(sub)
    fa = sp.lambdify(n, ae, 'numpy')
    fb = sp.lambdify(n, be, 'numpy')
    fg = sp.lambdify(n, ge, 'numpy')
    return fa, fb, fg

def cf_residual(ll, ww, N=200):
    fa, fb, fg = make_coeffs(ll, ww)
    # recurrence: alpha_n a_{n+1} + beta_n a_n + gamma_n a_{n-1} = 0
    # r_n = a_{n+1}/a_n.  Backward: r_{n-1} = -gamma_n/(alpha_n r_n + beta_n).
    # tail: r_N = a_{N+1}/a_N = 0.
    r = 0.0+0.0j
    for nn in range(N, 0, -1):
        an = complex(fa(nn)); bn = complex(fb(nn)); gn = complex(fg(nn))
        denom = an*r + bn
        if abs(denom) < 1e-300:
            r = 0.0+0.0j
        else:
            r = -gn/denom
    a0 = complex(fa(0)); b0 = complex(fb(0))
    return a0*r + b0

bench = {0: complex(0.110456,-0.104899),
         1: complex(0.292936,-0.097660),
         2: complex(0.483644,-0.096759)}

p("")
p("Benchmark (M=1):")
for ll, wb in bench.items():
    p(f"   l={ll}: w = {wb.real:.6f} {wb.imag:+.6f} i")
p("")
p(f"{'l':>3} {'N':>5} {'Re(w)':>13} {'Im(w)':>13} {'|resid|':>10} {'dRe(bench)':>11} {'dIm(bench)':>11}")
p("-"*82)

results = {}
for ll in [0,1,2]:
    wb = bench[ll]
    for N in [100,200,400]:
        def F(x):
            try:
                r = cf_residual(ll, complex(x[0],x[1]), N=N)
                return [float(r.real), float(r.imag)]
            except Exception:
                return [1e10,1e10]
        sol = root(F, [wb.real, wb.imag], tol=1e-14, method='hybr',
                   options={'maxfev':5000})
        wr = complex(sol.x[0], sol.x[1])
        res = abs(cf_residual(ll, wr, N=N))
        dRe = wr.real - wb.real; dIm = wr.imag - wb.imag
        p(f"{ll:>3} {N:>5} {wr.real:>13.7f} {wr.imag:>13.7f} {res:>10.2e} {dRe:>11.2e} {dIm:>11.2e}")
        results[(ll,N)] = (wr, res, dRe, dIm)
    p("-"*82)

p("")
p("VERDICT (pass = |w_400 - bench| < 1e-6 AND |w_400 - w_200| < 1e-6):")
allpass = True
for ll in [0,1,2]:
    w200 = results[(ll,200)][0]; w400 = results[(ll,400)][0]
    shift = abs(w400-w200)
    db = complex(results[(ll,400)][2], results[(ll,400)][3])
    ok = (abs(db) < 1e-6) and (shift < 1e-6)
    allpass &= ok
    p(f"   l={ll}: |w400-w200|={shift:.2e}  |w400-bench|={abs(db):.2e}  -> {'PASS' if ok else 'MARGINAL/FAIL'}")
p("")
p(f"OVERALL: {'THREE-DOOR PASS' if allpass else 'NOT PASS'}")
p(f"Elapsed: {time.time()-t0:.2f} s")
p("="*78)

outpath = r"D:\a10\aikjx\code\my_lib\tuft_v10_line1_scalar_out.txt"
with open(outpath, "w", encoding="utf-8") as fh:
    fh.write(out.getvalue())
print("\n[written]", outpath)
