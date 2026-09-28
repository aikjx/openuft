# -*- coding: utf-8 -*-
"""Diagnose TUFT static pole drift with N. Reproduce v50 pencil, sweep N."""
import math
import numpy as np
from scipy.linalg import eig
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

cm_t, d_t = -0.29, -0.05
BETA = (1.0 + math.sqrt(1.0 + 4.0/3.0))/2.0
MU = 2.0/3.0
RHO_H = brentq(lambda r: r**3 + cm_t*r + d_t, 0.55, 0.65)
HP = -2.0*cm_t/RHO_H**3 - 3.0*d_t/RHO_H**4
K_ASC = ((1.5)/(math.exp(2.0/RHO_H)*math.sqrt(HP)))**(2.0/3.0)
ANCHOR = 0.434445178 - 0.056449760j

def h_of(rho): return 1.0 + cm_t/rho**2 + d_t/rho**3
def hp_of(rho): return -2.0*cm_t/rho**3 - 3.0*d_t/rho**4
def V_of(rho):
    A = np.exp(-2.0/rho); B = np.exp(2.0/rho)*h_of(rho)
    R = rho*np.sqrt(B)
    q = 1.0 + (rho/2.0)*(-2.0/rho**2 + hp_of(rho)/h_of(rho))
    return 3.0*A*(1.0+q*q)/R**2

def cheb_gauss(N):
    j = np.arange(1,N+1); th = np.pi*(j-0.5)/N
    z = np.cos(th); w = ((-1.0)**(j-1))*np.sin(th)
    zi,zj = np.meshgrid(z,z,indexing='ij'); wi,wj = np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'): D=(wj/wi)/(zi-zj)
    np.fill_diagonal(D,0.0); np.fill_diagonal(D,-D.sum(axis=1))
    return z,D,D@D

def rho_vs_t(b,tmax,t0=1e-9):
    y0 = np.array([RHO_H + K_ASC*(b*t0)**(2.0/3.0)],dtype=complex)
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    sol = solve_ivp(rhs,(t0,tmax),y0,method='DOP853',rtol=1e-12,atol=1e-14,dense_output=True)
    return sol

def fit_U(sol,b,lo,hi,npts=240):
    tt = np.logspace(math.log10(lo/b),math.log10(hi/b),npts)
    rr = sol.sol(tt)[0].real
    s = b*tt
    U = V_of(rr) - 1.0/(3.0*s**2)
    powers = [-4.0/3.0,-2.0/3.0,0.0,2.0/3.0,4.0/3.0]
    X = np.column_stack([s**p for p in powers])
    coef,*_ = np.linalg.lstsq(X,U,rcond=None)
    return {(-2+k):coef[k] for k in range(5)}

def frob_a(Ud,K=12):
    a = np.zeros(K+1); a[0]=1.0
    for m in range(-2,K-2):
        k=m+3
        if k>K: break
        rhs = sum(Ud.get(m-j,0.0)*a[j] for j in range(k+1))
        p = k*MU
        a[k] = rhs/(p*(p-1.0+2.0*BETA))
    return a

def tuft_pencil(N,b,b_fit,lo,hi,Ktrunc,t0=1e-9):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    sol = rho_vs_t(b,float(t.max())*1.0001+1.0,t0=t0)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    sol_fit = rho_vs_t(b_fit,8.0)
    Ud = fit_U(sol_fit,b_fit,lo,hi)
    a12 = frob_a(Ud,Ktrunc)
    P = np.zeros_like(s,dtype=complex); Pp=P.copy(); Ppp=P.copy()
    for k,ak in enumerate(a12):
        if ak==0.0: continue
        p = k*MU
        P  += ak*s**p
        Pp += ak*p*s**(p-1.0)
        Ppp+= ak*p*(p-1.0)*s**(p-2.0)
    U = V_of(rho) - 1.0/(3.0*s**2)
    C10 = 2.0*Pp/P + 2.0*BETA/s
    C00 = Ppp/P + 2.0*BETA*Pp/(s*P) - U
    Q0 = np.diag(g**2)@D2 + np.diag(g*gp+C10*g)@D + np.diag(C00)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(C10))
    return Q0,Q1

def solve(N,b,b_fit,lo,hi,Ktrunc):
    Q0,Q1 = tuft_pencil(N,b,b_fit,lo,hi,Ktrunc)
    ev = eig(-Q0,Q1,right=False); ev=ev[np.isfinite(ev)]
    w = complex(ev[np.argmin(np.abs(ev-ANCHOR))])
    return w

print("ANCHOR = %.9f %+.9fi"%(ANCHOR.real,ANCHOR.imag))
print("RHO_H = %.9f  HP=%.6f  K_ASC=%.6f"%(RHO_H,HP,K_ASC))
print("BETA = %.9f"%BETA)
print()
# reproduce v50 defaults
b_t = complex(4.0,0.5); b_fit=4.0; lo=1e-3; hi=0.30; Ktrunc=12
print("=== v50 defaults: b=%s b_fit=%.0f lo=%.1e hi=%.2f K=%d ==="%(b_t,b_fit,lo,hi,Ktrunc))
for N in (60,90,120):
    w = solve(N,b_t,b_fit,lo,hi,5)  # v50 uses a12[:5]
    err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
    print("  N=%3d  w=%.9f %+.9fi  |err|=%.3e  %.1f dig"%(N,w.real,w.imag,err,dig))
