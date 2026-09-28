# -*- coding: utf-8 -*-
"""t0 sensitivity + multi-seed Beyn averaging."""
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

def cheb_gauss(N):
    j=np.arange(1,N+1); th=np.pi*(j-0.5)/N
    z=np.cos(th); w=((-1.0)**(j-1))*np.sin(th)
    zi,zj=np.meshgrid(z,z,indexing='ij'); wi,wj=np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'): D=(wj/wi)/(zi-zj)
    np.fill_diagonal(D,0.0); np.fill_diagonal(D,-D.sum(axis=1))
    return z,D,D@D

def build_pencil(N, b, t0=1e-11):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    sol = solve_ivp(rhs,(t0,float(t.max())*1.0001+1.0),y0,method='DOP853',
                   rtol=1e-13,atol=1e-15,dense_output=True)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1

def beyn_avg(Q0, Q1, center, radius, nc=400, nseeds=5):
    n = Q0.shape[0]
    th = 2*np.pi*np.arange(nc)/nc
    zz = center + radius*np.exp(1j*th)
    wq = radius*np.exp(1j*th)/nc
    vals=[]
    for seed in range(nseeds):
        rng = np.random.default_rng(seed)
        Vv = rng.standard_normal((n,1)) + 1j*rng.standard_normal((n,1))
        B0 = np.zeros((n,1),dtype=complex); B1 = np.zeros_like(B0)
        for k in range(nc):
            lu = lu_factor(Q0 + zz[k]*Q1)
            X = lu_solve(lu, Vv)
            B0 += X*wq[k]; B1 += zz[k]*X*wq[k]
        vals.append(complex((B0.conj().T@B1)[0,0]/(B0.conj().T@B0)[0,0]))
    return np.mean(vals), vals

b = complex(3.5, 1.5)
N = 90
print("t0 sensitivity, N=90, b=%s:"%b)
for t0 in (1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13):
    Q0,Q1 = build_pencil(N, b, t0=t0)
    w, vals = beyn_avg(Q0, Q1, ANCHOR, 0.005, nc=400, nseeds=3)
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    spread = max(abs(v-w) for v in vals)
    print("  t0=%.0e: w=%.12f %+.12fi  |err|=%.3e %.1f dig spread=%.1e"%(t0,w.real,w.imag,err,dig,spread))

# N=120 best
print("\nN=120, best:")
Q0,Q1 = build_pencil(120, b, t0=1e-11)
w, vals = beyn_avg(Q0, Q1, ANCHOR, 0.005, nc=400, nseeds=3)
err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
print("  w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(w.real,w.imag,err,dig))
