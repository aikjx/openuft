# -*- coding: utf-8 -*-
"""Tabulate tortoise s(rho) by direct quadrature, invert for rho(s)."""
import math, time
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline

cm_t, d_t = -0.29, -0.05
BETA = (1.0 + math.sqrt(1.0 + 4.0/3.0))/2.0
RHO_H = brentq(lambda r: r**3 + cm_t*r + d_t, 0.55, 0.65)
HP = -2.0*cm_t/RHO_H**3 - 3.0*d_t/RHO_H**4
ANCHOR = 0.434445178 - 0.056449760j

def h_of(rho): return 1.0 + cm_t/rho**2 + d_t/rho**3
def hp_of(rho): return -2.0*cm_t/rho**3 - 3.0*d_t/rho**4
def V_of(rho):
    A = np.exp(-2.0/rho); B = np.exp(2.0/rho)*h_of(rho); R = rho*np.sqrt(B)
    q = 1.0 + (rho/2.0)*(-2.0/rho**2 + hp_of(rho)/h_of(rho))
    return 3.0*A*(1.0+q*q)/R**2

# Build s(rho) table by quadrature: s = integral from rho_h to rho of e^{2/rho'} sqrt(h) drho'
# Near wall integrand ~ sqrt(HP*(rho'-rho_h)), use substitution u=sqrt(rho'-rho_h)
def s_of_rho(rho):
    """Tortoise s(rho) = int_{rho_h}^{rho} e^{2/r'} sqrt(h(r')) dr'."""
    if rho <= RHO_H: return 0.0
    # integrate with near-wall substitution
    def integrand(r):
        return np.exp(2.0/r)*np.sqrt(max(0.0, h_of(r)))
    # split near wall
    delta = rho - RHO_H
    if delta < 0.1:
        # use u substitution: r = rho_h + u^2, dr = 2u du, integrand ~ sqrt(HP)*u
        val, _ = quad(lambda u: 2*u*integrand(RHO_H+u**2), 0, math.sqrt(delta),
                     limit=200, epsabs=1e-14, epsrel=1e-13)
    else:
        near, _ = quad(lambda u: 2*u*integrand(RHO_H+u**2), 0, math.sqrt(0.1),
                      limit=200, epsabs=1e-14, epsrel=1e-13)
        far, _ = quad(integrand, RHO_H+0.1, rho, limit=200, epsabs=1e-14, epsrel=1e-13)
        val = near + far
    return val

# Build table
rho_table = np.concatenate([
    RHO_H + np.logspace(-8, -1, 200),  # near wall
    np.linspace(RHO_H+0.1, 10.0, 500),
    np.linspace(10.0, 100.0, 100)
])
rho_table = np.unique(rho_table)
s_table = np.array([s_of_rho(r) for r in rho_table])
# Build spline s(rho), invert to rho(s)
# s increases monotonically with rho
s_to_rho = CubicSpline(s_table, rho_table, extrapolate=True)

def rho_of_s(s_val):
    """rho(s) via table lookup. s can be complex: use magnitude, physical depends on |s|."""
    sv = np.abs(s_val)
    return s_to_rho(sv)

def cheb_gauss(N):
    j=np.arange(1,N+1); th=np.pi*(j-0.5)/N
    z=np.cos(th); w=((-1.0)**(j-1))*np.sin(th)
    zi,zj=np.meshgrid(z,z,indexing='ij'); wi,wj=np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'): D=(wj/wi)/(zi-zj)
    np.fill_diagonal(D,0.0); np.fill_diagonal(D,-D.sum(axis=1))
    return z,D,D@D

def build_pencil(N, b):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    # rho from table (real s magnitude)
    rho = rho_of_s(s)
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1

def beyn(Q0, Q1, center, radius, nc=300):
    n = Q0.shape[0]
    rng = np.random.default_rng(0)
    Vv = rng.standard_normal((n,1)) + 1j*rng.standard_normal((n,1))
    th = 2*np.pi*np.arange(nc)/nc
    zz = center + radius*np.exp(1j*th)
    wq = radius*np.exp(1j*th)/nc
    B0 = np.zeros((n,1),dtype=complex); B1 = np.zeros_like(B0)
    for k in range(nc):
        lu = lu_factor(Q0 + zz[k]*Q1)
        X = lu_solve(lu, Vv)
        B0 += X*wq[k]; B1 += zz[k]*X*wq[k]
    return complex((B0.conj().T@B1)[0,0]/(B0.conj().T@B0)[0,0])

print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
# Verify table
print("s(rho_h+0.1)=%.6f  rho(s)=%.6f (should be ~%.4f)"%(s_of_rho(RHO_H+0.1), RHO_H+0.1, RHO_H+0.1))
print("s(1.0)=%.6f  rho(s)=%.6f"%(s_of_rho(1.0), 1.0))
print()

for bR,bI in [(3.0,1.5),(3.5,1.5),(4.0,1.5),(3.0,2.0)]:
    b = complex(bR,bI)
    for N in (60, 90, 120):
        Q0,Q1 = build_pencil(N, b)
        w = beyn(Q0, Q1, ANCHOR, 0.008, nc=300)
        err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
        print("b=%.1f%+.1fi N=%3d: w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(bR,bI,N,w.real,w.imag,err,dig))
    print()
