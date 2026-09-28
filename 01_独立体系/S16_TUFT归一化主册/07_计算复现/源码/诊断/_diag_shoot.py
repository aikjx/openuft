# -*- coding: utf-8 -*-
"""Shooting solver for TUFT static QNM pole.
Integrate coupled [rho(s), psi(s), psi_s(s)] from wall to infinity, match outgoing.
"""
import math, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.optimize import root as scipy_root

cm_t, d_t = -0.29, -0.05
BETA = (1.0 + math.sqrt(1.0 + 4.0/3.0))/2.0
RHO_H = brentq(lambda r: r**3 + cm_t*r + d_t, 0.55, 0.65)
HP = -2.0*cm_t/RHO_H**3 - 3.0*d_t/RHO_H**4
K_ASC = ((3.0/2.0)/(math.exp(2.0/RHO_H)*math.sqrt(HP)))**(2.0/3.0)
ANCHOR = 0.434445178 - 0.056449760j

def h_of(rho): return 1.0 + cm_t/rho**2 + d_t/rho**3
def hp_of(rho): return -2.0*cm_t/rho**3 - 3.0*d_t/rho**4
def V_of(rho):
    A = np.exp(-2.0/rho); B = np.exp(2.0/rho)*h_of(rho); R = rho*np.sqrt(B)
    q = 1.0 + (rho/2.0)*(-2.0/rho**2 + hp_of(rho)/h_of(rho))
    return 3.0*A*(1.0+q*q)/R**2

def rhs(s, y, w):
    """y = [rho, psi, psi_s]. Coupled ODE in tortoise s."""
    rho, psi, psi_s = y
    drho_ds = np.exp(2.0/rho)*np.sqrt(h_of(rho))
    V = V_of(rho)
    psi_ss = (V - w*w)*psi
    return [drho_ds, psi_s, psi_ss]

def shooting_residual(w, s_min=1e-6, s_max=30.0):
    """Integrate from wall to s_max, return log-derivative mismatch."""
    rho0 = RHO_H + K_ASC * s_min**(2.0/3.0)
    psi0 = s_min**BETA
    psi_s0 = BETA * s_min**(BETA - 1.0)
    y0 = [rho0, psi0, psi_s0]
    sol = solve_ivp(lambda s,y: rhs(s,y,w), (s_min, s_max), y0,
                   method='DOP853', rtol=1e-12, atol=1e-14, dense_output=False,
                   max_step=0.5)
    if not sol.success:
        return 1e10+0j
    rho_f, psi_f, psi_s_f = sol.y[:,-1]
    # outgoing: psi_s/psi -> iw (plus correction from V~6/s^2)
    # At finite s_max, outgoing wave has psi ~ e^{iws} s^{-1} (from 6/s^2 barrier)
    # log-derivative = iw - 1/s (leading correction)
    target = 1j*w - 1.0/s_max
    return complex(psi_s_f/psi_f) - target

# Find root using complex Newton
print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
print("Shooting: TUFT static QNM pole")
print("="*60)

# Scan: residual as function of w near anchor
w_guess = 0.434 - 0.056j
print("\nResidual near guess:")
for dw in [0.0, 0.001, -0.001, 0.001j, -0.001j]:
    w = w_guess + dw
    r = shooting_residual(w)
    print("  w=%.6f%+.6fi  residual=%.6e%+.6ei  |r|=%.3e"%(w.real,w.imag,r.real,r.imag,abs(r)))

# Complex Newton
print("\nComplex Newton iteration:")
w = complex(w_guess)
for it in range(30):
    r0 = shooting_residual(w)
    eps = 1e-7
    # numerical derivative
    rr = shooting_residual(w+eps)
    ri = shooting_residual(w+1j*eps)
    dw_real = (rr-r0)/eps
    dw_imag = (ri-r0)/(1j*eps)
    # solve 2x2: [Re dw_real, Re dw_imag; Im dw_real, Im dw_imag] step = -r
    J = np.array([[dw_real.real, dw_imag.real],[dw_real.imag, dw_imag.imag]])
    try:
        step = np.linalg.solve(J, [-r0.real, -r0.imag])
    except:
        break
    w_new = w + step[0] + 1j*step[1]
    print("  iter %d: w=%.12f%+.12fi  |r|=%.3e  step=%.2e"%(it,w_new.real,w_new.imag,abs(r0),abs(complex(step[0]+1j*step[1]))))
    if abs(w_new-w) < 1e-13:
        w = w_new; break
    w = w_new

err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
print("\nFinal: w=%.12f %+.12fi"%(w.real,w.imag))
print("Anchor: %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
print("|err|=%.3e  %.1f digits"%(err,dig))
