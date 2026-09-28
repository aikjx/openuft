# -*- coding: utf-8 -*-
"""Verify E475 frame-dragging first-principles integral."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

cm_t, d_t = -0.29, -0.05
RHO_H = brentq(lambda r: r**3 + cm_t*r + d_t, 0.55, 0.65)

def h_of(rho): return 1.0 + cm_t/rho**2 + d_t/rho**3

def integrand(rp):
    return 1.0/(rp**4 * np.exp(2.0/rp) * h_of(rp)**1.5)

# Omega_F(rho)/a = 6 * integral from rho to inf of integrand(rp) drp
def Omega_F(rho):
    val, err = quad(integrand, rho, np.inf, limit=200, epsabs=1e-14, epsrel=1e-14)
    return 6.0*val

print("RHO_H = %.9f"%RHO_H)
print("E475 frame-dragging: Omega_F(rho)/a = 6 * int_rho^inf dr'/(r'^4 e^{2/r'} h^{3/2})")
print()
print("%10s %18s %18s %12s"%("rho","Omega_F/a","2/rho^3 (GR)","ratio"))
for rho in (0.7, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0):
    of = Omega_F(rho)
    gr = 2.0/rho**3
    print("%10.4f %18.10f %18.10f %12.6f"%(rho, of, gr, of/gr))

# Near wall behavior
print()
print("Near wall (rho -> RHO_H):")
for dr in (0.1, 0.01, 0.001, 0.0001):
    rho = RHO_H + dr
    of = Omega_F(rho)
    print("  rho-rho_h=%.4f  Omega_F/a=%.6f  ~1/sqrt(delta)=%.4f"%(dr, of, 1.0/np.sqrt(dr)))
