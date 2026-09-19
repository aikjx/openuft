#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT v12 Line 1: Gravitational RW s=-2
Leaver three-term recurrence derivation + QNM gate.

Uses Cook-Zalutskiy / qnm library D0-D4 coefficient formulation.
E349 : s=-2 three-term recurrence coefficients
Gate : l=2 n=0  -> 0.3736716844 - 0.0889623157 i  (>=6 digits)
       l=2 n=1  -> 0.3467109969 - 0.2739148753 i  (>=6 digits)
"""

import time
t0 = time.time()

import numpy as np
from scipy.optimize import root as sp_root
import sympy as sp

print("=" * 74)
print("TUFT v12 LINE 1: GRAVITATIONAL REGGE-WHEELER s=-2")
print("Leaver Recurrence Coefficient Derivation + QNM Gate")
print("=" * 74)

# ======================================================================
# PART 1: SYMBOLIC DERIVATION OF D0-D4 (Cook-Zalutskiy / Leaver)
# ======================================================================
z, w, s_sym = sp.symbols('z omega s')
l = sp.symbols('l', positive=True)
A = l*(l+1) - s_sym*(s_sym+1)  # separation constant for Schwarzschild

# Schwarzschild a=0:
root = 1
r_p, r_m = 2, 0
sigma_p = 2*w  # m=2, a=0: (2*omega*r_p - m*a)/(2*root) = 2*omega
# Actually for m=2: sigma_p = (2*omega*r_p - m*a)/(2*root) = 2*omega
sigma_p = 2*w
sigma_m = 0

zeta = 1j*w
xi   = -s_sym - 1j*sigma_p
eta  = -1j*sigma_m

p     = root * zeta
alpha_p = 1 + s_sym + xi + eta - 2*zeta + s_sym
gamma_p = 1 + s_sym + 2*eta
delta_p = 1 + s_sym + 2*xi

sigma_param = (A + 0 - 8*w**2
    + p*(2*alpha_p + gamma_p - delta_p)
    + (1+s_sym - 0.5*(gamma_p+delta_p)) * (s_sym + 0.5*(gamma_p+delta_p)))

D0 = delta_p
D1 = 4*p - 2*alpha_p + gamma_p - delta_p - 2
D2 = 2*alpha_p - gamma_p + 2
D3 = alpha_p*(4*p - delta_p) - sigma_param
D4 = alpha_p*(alpha_p - gamma_p + 1)

# Substitute s=-2, m=2 (sigma_p=2w, sigma_m=0)
D0_s2 = sp.simplify(D0.subs(s_sym, -2))
D1_s2 = sp.simplify(D1.subs(s_sym, -2))
D2_s2 = sp.simplify(D2.subs(s_sym, -2))
D3_s2 = sp.simplify(D3.subs(s_sym, -2))
D4_s2 = sp.simplify(D4.subs(s_sym, -2))

print("\n--- E349a: D0-D4 coefficients for s=-2, a=0, m=2 ---")
print("  D0 =", sp.expand(D0_s2))
print("  D1 =", sp.expand(D1_s2))
print("  D2 =", sp.expand(D2_s2))
print("  D3 =", sp.expand(D3_s2))
print("  D4 =", sp.expand(D4_s2))

# Also compute s=0 for comparison
D0_s0 = sp.simplify(D0.subs(s_sym, 0))
D1_s0 = sp.simplify(D1.subs(s_sym, 0))
D2_s0 = sp.simplify(D2.subs(s_sym, 0))
D3_s0 = sp.simplify(D3.subs(s_sym, 0))
D4_s0 = sp.simplify(D4.subs(s_sym, 0))

print("\n--- E348: D0-D4 for s=0 scalar (comparison) ---")
print("  D0 =", sp.expand(D0_s0))
print("  D1 =", sp.expand(D1_s0))
print("  D2 =", sp.expand(D2_s0))
print("  D3 =", sp.expand(D3_s0))
print("  D4 =", sp.expand(D4_s0))

# ======================================================================
# PART 2: THREE-TERM RECURRENCE
# ======================================================================
n_s = sp.symbols('n')

def make_recurrence(D0, D1, D2, D3, D4):
    alpha_n = sp.expand(n_s**2 + (D0+1)*n_s + D0)
    beta_n  = sp.expand(-2*n_s**2 + (D1+2)*n_s + D3)
    gamma_n = sp.expand(n_s**2 + (D2-3)*n_s + D4 - D2 + 2)
    return alpha_n, beta_n, gamma_n

a_s2, b_s2, g_s2 = make_recurrence(D0_s2, D1_s2, D2_s2, D3_s2, D4_s2)
a_s0, b_s0, g_s0 = make_recurrence(D0_s0, D1_s0, D2_s0, D3_s0, D4_s0)

print("\n" + "=" * 74)
print("E348   s=0 SCALAR:")
print("=" * 74)
print("  alpha_n =", a_s0)
print("  beta_n  =", b_s0)
print("  gamma_n =", g_s0)

print("\n" + "=" * 74)
print("E349b  s=-2 GRAVITATIONAL RW:")
print("=" * 74)
print("  alpha_n =", a_s2)
print("  beta_n  =", b_s2)
print("  gamma_n =", g_s2)

# ======================================================================
# PART 3: NUMERICAL QNM SOLVER
# ======================================================================
print("\n" + "=" * 74)
print("PART 3: NUMERICAL QNM SOLVER")
print("=" * 74)

# Lambdify
alpha_fn = sp.lambdify((n_s, w, l), a_s2, 'numpy')
beta_fn  = sp.lambdify((n_s, w, l), b_s2, 'numpy')
gamma_fn = sp.lambdify((n_s, w, l), g_s2, 'numpy')

def quant(wc, lv, N):
    """Quantization: beta_0 - alpha_0 * C_1 = 0
    where C_n = gamma_n / (beta_n - alpha_n * C_{n+1})."""
    C = 0j  # C_{N+1} = 0
    for n in range(N, 0, -1):
        an = alpha_fn(n, wc, lv)
        bn = beta_fn(n, wc, lv)
        gn = gamma_fn(n, wc, lv)
        C = gn / (bn - an * C)
    a0 = alpha_fn(0, wc, lv)
    b0 = beta_fn(0, wc, lv)
    return b0 - a0 * C

# sanity
w_test = 0.3 + 0.5j
print(f"  Sanity: quant(0.3+0.5i, l=2, N=200) = {quant(w_test, 2, 200):.6e}")

# ---- benchmarks ----
bench = {
    (2, 0): complex(0.37367168441804166, -0.0889623156889341),
    (2, 1): complex(0.34671099687909240, -0.2739148752911987),
}

def solve_gate(lv, nm, N, guess):
    def rr(x):
        wc = complex(x[0], x[1])
        r = quant(wc, lv, N)
        return [r.real, r.imag]
    sol = sp_root(rr, [guess.real, guess.imag], method='hybr',
                  options={'xtol': 1e-13, 'maxfev': 5000})
    wc = complex(sol.x[0], sol.x[1])
    return wc, abs(quant(wc, lv, N))

# ======================================================================
# PART 4: GATE + CONVERGENCE
# ======================================================================
print("\n--- Gate results (M=1, l=2) ---")
print(f"{'N':>6} | {'mode':>10} | {'Re(omega)':>22} | {'Im(omega)':>22} | |res|      | digits")
print("-" * 95)

results = {}
for (lv, nm), bm in bench.items():
    for N in [100, 200, 400]:
        wc, res = solve_gate(lv, nm, N, bm)
        diff = abs(wc - bm)
        digits = 99 if diff == 0 else max(0, -int(np.floor(np.log10(diff))))
        results[(lv, nm, N)] = (wc, res, diff, digits)
        print(f"{N:>6} | l={lv} n={nm:<2} | {wc.real: .16e} | {wc.imag: .16e} | {res:.2e} | {digits}")

print("\n--- Benchmark comparison (N=400) ---")
for (lv, nm), bm in bench.items():
    wc, res, diff, digits = results[(lv, nm, 400)]
    print(f"  l={lv} n={nm}: ours={wc:.15e}, bench={bm:.15e}, diff={diff:.2e}, digits={digits}")

all_pass = all(results[(lv, nm, 400)][3] >= 6 and results[(lv, nm, 400)][1] < 1e-6
               for (lv, nm) in bench)
print(f"\n  GATE: {'PASS' if all_pass else 'FAIL'}")

elapsed = time.time() - t0
print(f"\nTotal wall-clock: {elapsed:.2f} s")
print("=" * 74)
