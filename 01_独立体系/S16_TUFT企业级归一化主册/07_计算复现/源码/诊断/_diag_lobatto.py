# -*- coding: utf-8 -*-
"""Chebyshev-Lobatto (with endpoints) + explicit boundary rows."""
import math, time
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.integrate import solve_ivp
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

def cheb_lobatto(N):
    """Chebyshev-Lobatto nodes z_j = cos(pi j/N), j=0..N. D, D2 matrices."""
    j = np.arange(N+1)
    z = np.cos(np.pi*j/N)
    # barycentric weights
    w = np.ones(N+1); w[0]=0.5; w[-1]=0.5
    w[1::2] = -w[1::2]
    zi,zj = np.meshgrid(z,z,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'):
        D = (w[:,None]/w[None,:])/(zi-zj)
    np.fill_diagonal(D,0.0)
    np.fill_diagonal(D,-D.sum(axis=1))
    D2 = D@D
    return z, D, D2

def build_pencil(N, b, t0=1e-11):
    z,D,D2 = cheb_lobatto(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    # fix s at z=-1 (wall): t=0, s=0 -> limit
    s[0] = 0.0  # wall
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    t_nodes = t[1:]  # skip t=0
    sol = solve_ivp(rhs,(t0,float(t.max())*1.0001+1.0),y0,method='DOP853',
                   rtol=1e-13,atol=1e-15,dense_output=True)
    rho = np.zeros_like(s)
    rho[0] = RHO_H  # wall
    rho[1:] = sol.sol(t_nodes)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    g[0] = 0; gp[0] = 0  # wall limit
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    # Wall boundary row (z=-1, index 0): F=0 (reflecting, psi=s^beta F, s=0 => F finite)
    # Actually after peel psi=s^beta e^{iws} F, at s=0 psi=0 automatically.
    # Replace wall row with: F(0)=1 gauge? No, use derivative condition.
    # Better: wall row = first row of Q0,Q1 replaced with [1,0,0,...] F_0 = 0
    Q0[0,:] = 0; Q0[0,0] = 1.0; Q1[0,:] = 0
    # Infinity row (z=+1, index N): outgoing already in peel, replace with gauge
    Q0[-1,:] = 0; Q0[-1,-1] = 1.0; Q1[-1,:] = 0
    return Q0, Q1

def beyn(Q0, Q1, center, radius=0.005, nc=300):
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
print("Chebyshev-Lobatto + boundary rows, b=%s"%b)
print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
for N in (59, 89, 119):
    Q0,Q1 = build_pencil(N, b)
    w = beyn(Q0, Q1, ANCHOR)
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    print("  N=%3d: w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(N+1,w.real,w.imag,err,dig))
