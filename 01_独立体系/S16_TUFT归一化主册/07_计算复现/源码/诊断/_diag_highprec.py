# -*- coding: utf-8 -*-
"""High-precision test: v24 simple peel + Beyn contour + Rayleigh refinement."""
import math, time
import numpy as np
from scipy.linalg import eig, lu_factor, lu_solve
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

def build_pencil(N, b, t0=1e-8):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    # integrate rho(t)
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    sol = solve_ivp(rhs,(t0,float(t.max())*1.0001+1.0),y0,method='DOP853',
                   rtol=1e-12,atol=1e-14,dense_output=True)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    q21 = BETA*(BETA-1.0)/s**2 - Vv
    q_z = g*gp + 2.0*g*BETA/s
    Q0 = np.diag(g**2)@D2 + np.diag(q_z)@D + np.diag(q21)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(2.0*BETA/s))
    return Q0, Q1

def beyn_pole(Q0, Q1, center, radius=0.02, nc=128):
    """Extract eigenvalues in contour via Beyn contour integral, rank 1."""
    n = Q0.shape[0]
    rng = np.random.default_rng(0)
    Vv = rng.standard_normal((n,1)) + 1j*rng.standard_normal((n,1))
    th = 2*np.pi*np.arange(nc)/nc
    zz = center + radius*np.exp(1j*th)
    wq = radius*np.exp(1j*th)/nc
    B0 = np.zeros((n,1),dtype=complex); B1 = np.zeros_like(B0)
    for k in range(nc):
        Mw = Q0 + zz[k]*Q1
        lu = lu_factor(Mw)
        X = lu_solve(lu, Vv)
        B0 += X*wq[k]; B1 += zz[k]*X*wq[k]
    return (B0.conj().T@B1)[0,0]/(B0.conj().T@B0)[0,0]

def refine(Q0, Q1, w0, iters=20):
    """Rayleigh/Newton refinement for linear pencil Q0 + w Q1 = 0.
    Solve generalized eig near w0, then iterate eigenpair correction."""
    w = complex(w0)
    for _ in range(iters):
        # compute residual nullspace via LU of L(w)
        Lm = Q0 + w*Q1
        # get right nullvector: solve Lm @ F = small using inverse on random
        lu = lu_factor(Lm)
        rng = np.random.default_rng(1)
        Vv = rng.standard_normal((Q0.shape[0],1)) + 1j*rng.standard_normal((Q0.shape[0],1))
        F = lu_solve(lu, Vv)  # this is (Lm)^{-1} Vv, dominated by nullspace
        F = F/np.linalg.norm(F)
        # left nullvector: solve Lm^H U = Vv
        luh = lu_solve(lu, Vv, trans=1)
        U = luh/np.linalg.norm(luh)
        # Rayleigh correction: w_new = w - (U† L(w) F)/(U† Q1 F)
        # but L(w)F ~ residual; use eigenpair Newton:
        # (Q0 + w Q1) F ≈ resid, solve (Q0+wQ1) dF + Q1 F dw = -resid
        resid = Q0@F + w*(Q1@F)
        num = U.conj().T @ resid
        den = U.conj().T @ Q1 @ F
        dw = -num/den
        w_new = w + complex(dw)
        if abs(w_new - w) < 1e-14:
            w = w_new; break
        w = w_new
    return w

b = complex(4.0, 0.5)
print("ANCHOR = %.9f %+.9fi"%(ANCHOR.real,ANCHOR.imag))
print("RHO_H=%.9f K_ASC=%.6f BETA=%.9f"%(RHO_H,K_ASC,BETA))
print()
for N in (60, 90, 120):
    t0=time.time()
    Q0,Q1 = build_pencil(N, b, t0=1e-8)
    # rough pole via generalized eig
    ev = eig(-Q0, Q1, right=False); ev=ev[np.isfinite(ev)]
    w_rough = complex(ev[np.argmin(np.abs(ev-ANCHOR))])
    # Beyn isolation
    w_beyn = beyn_pole(Q0, Q1, ANCHOR, radius=0.02, nc=128)
    # refine
    w_ref = refine(Q0, Q1, w_beyn, iters=30)
    err = abs(w_ref-ANCHOR); dig = -math.log10(err) if err>0 else 20
    err_rough = abs(w_rough-ANCHOR)
    print("N=%3d rough=%.9f%+.9fi (|err|=%.2e)  beyn=%.9f%+.9fi  ref=%.9f%+.9fi  |err|=%.3e %.1fdig (%.1fs)"
          %(N,w_rough.real,w_rough.imag,err_rough,w_beyn.real,w_beyn.imag,w_ref.real,w_ref.imag,err,dig,time.time()-t0))
