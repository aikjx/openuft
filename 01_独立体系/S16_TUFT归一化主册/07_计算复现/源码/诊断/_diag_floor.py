# -*- coding: utf-8 -*-
"""Debug the 5e-9 floor: ODE tolerance, direct s-integration, Frobenius correction."""
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

def rho_of_s_direct(s_nodes, rtol=1e-14):
    """Integrate d rho/d s = e^{2/rho} sqrt(h(rho)) directly in s, from wall."""
    s0 = float(np.min(np.abs(s_nodes)))
    # near-wall IC: rho = rho_h + K s^{2/3}
    y0 = [RHO_H + K_ASC * s0**(2.0/3.0)]
    def rhs(_s, y):
        r = y[0]
        return [np.exp(2.0/r)*np.sqrt(h_of(r))]
    s_max = float(np.max(np.abs(s_nodes)))*1.01
    sol = solve_ivp(rhs, (s0, s_max), y0, method='DOP853',
                   rtol=rtol, atol=1e-16, dense_output=True)
    # s_nodes are complex; integrate magnitude then evaluate along contour
    # Actually integrate along the complex s contour: ds = |ds| e^{i angle}
    # Better: integrate in |s| with angle fixed = angle(b)
    return sol

def build_pencil_v2(N, b, rtol=1e-13, frob_terms=0):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    # integrate rho(t) with tight tolerance
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    t0 = 1e-11
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    sol = solve_ivp(rhs,(t0,float(t.max())*1.0001+1.0),y0,method='DOP853',
                   rtol=rtol,atol=1e-16,dense_output=True)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1, s, rho

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

b = complex(3.0, 1.5)
N = 90
print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
print("N=%d b=%s"%(N,b))
print()
for rtol in (1e-12, 1e-13, 1e-14):
    Q0,Q1,s,rho = build_pencil_v2(N, b, rtol=rtol)
    w = beyn(Q0, Q1, ANCHOR, 0.008, nc=300)
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    print("rtol=%.0e: w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(rtol,w.real,w.imag,err,dig))

# Try smaller Beyn radius
print()
Q0,Q1,s,rho = build_pencil_v2(N, b, rtol=1e-14)
for rad in (0.02, 0.01, 0.005, 0.002):
    w = beyn(Q0, Q1, ANCHOR, rad, nc=400)
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    print("radius=%.3f: w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(rad,w.real,w.imag,err,dig))

# Check rho accuracy: compare ODE at fine nodes
print()
print("rho(s) at smallest node: |s|=%.6f  rho=%.10f"%(abs(s[0]), rho[0]))
print("  expected near-wall: rho_h + K*s^(2/3) = %.10f"%(RHO_H + K_ASC*s[0]**(2.0/3.0)))
