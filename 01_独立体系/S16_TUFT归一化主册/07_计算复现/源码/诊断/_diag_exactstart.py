# -*- coding: utf-8 -*-
"""Start ODE at finite rho (no asymptotic IC), high-accuracy spectral solve."""
import math, time
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

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

def s_of_rho(rho):
    """Exact tortoise s(rho) = integral from rho_h to rho of e^{2/r'} sqrt(h) dr'."""
    if rho <= RHO_H: return 0.0
    # near wall substitution u = sqrt(r-rho_h)
    delta = min(rho - RHO_H, 0.05)
    near, _ = quad(lambda u: 2*u*np.exp(2.0/(RHO_H+u**2))*np.sqrt(h_of(RHO_H+u**2)),
                  0, math.sqrt(delta), limit=100, epsabs=1e-14, epsrel=1e-13)
    if rho - RHO_H > 0.05:
        far, _ = quad(lambda r: np.exp(2.0/r)*np.sqrt(h_of(r)),
                     RHO_H+0.05, rho, limit=100, epsabs=1e-14, epsrel=1e-13)
        return near + far
    return near

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
    # Use exact s(rho) to find rho(s): integrate d rho/d s = e^{2/rho} sqrt(h)
    # Start from a known point: at s=0, rho=rho_h. Integrate in |s|.
    # For complex s = b*t, integrate along t with complex b.
    # But start from s_start = s(rho_h + 0.001) computed exactly.
    rho_start = RHO_H + 0.001
    s_start = s_of_rho(rho_start)
    # t_start = s_start / |b| (real scale), then complex contour s = b*t
    # Actually: physical s_real corresponds to t_real = s_real/|b|... 
    # Let's just integrate complex ODE starting from (t_start, rho_start)
    t_start = s_start / abs(b)
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = np.array([rho_start], dtype=complex)
    t_max = float(t.max())*1.0001 + 1.0
    sol = solve_ivp(rhs,(t_start,t_max),y0,method='DOP853',
                   rtol=1e-13,atol=1e-15,dense_output=True)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1

def beyn(Q0, Q1, center, radius, nc=400):
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

b = complex(3.5, 1.5)
print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
print("Starting ODE from rho_h+0.001 (exact s), b=%s"%b)
for N in (60, 90, 120):
    t0=time.time()
    Q0,Q1 = build_pencil(N, b)
    w = beyn(Q0, Q1, ANCHOR, 0.005, nc=400)
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    print("  N=%3d: w=%.12f %+.12fi  |err|=%.3e %.1f dig (%.1fs)"%(N,w.real,w.imag,err,dig,time.time()-t0))
