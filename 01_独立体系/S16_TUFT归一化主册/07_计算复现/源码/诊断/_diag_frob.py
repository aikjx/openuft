# -*- coding: utf-8 -*-
"""Correct inner Frobenius peeling: derive a_k from accurate near-wall U expansion."""
import math, time
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares

cm_t, d_t = -0.29, -0.05
BETA = (1.0 + math.sqrt(1.0 + 4.0/3.0))/2.0
MU = 2.0/3.0
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

def build_rho(b, t0=1e-11):
    def rhs(_t,y): return [b*np.exp(-2.0/y[0])/np.sqrt(h_of(y[0]))]
    y0 = [RHO_H + K_ASC*(b*t0)**(2.0/3.0)]
    sol = solve_ivp(rhs,(t0,10.0),y0,method='DOP853',rtol=1e-13,atol=1e-15,dense_output=True)
    return sol

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

# Step 1: derive U_m coefficients from near-wall data on real s-axis
# Use real b_fit for accurate near-wall expansion
b_fit = 4.0
sol_fit = build_rho(b_fit)
# sample s near wall
s_sample = np.logspace(-5, -0.5, 500)
t_sample = s_sample / b_fit
rho_sample = sol_fit.sol(t_sample)[0].real
U_sample = V_of(rho_sample) - 1.0/(3.0*s_sample**2)

# Fit U = sum_m U[m] s^{m*mu} for m = -4..6
m_list = list(range(-4, 7))
powers = [m*MU for m in m_list]
X = np.column_stack([s_sample**p for p in powers])
coef, *_ = np.linalg.lstsq(X, U_sample, rcond=None)
Ud = {m: coef[i] for i,m in enumerate(m_list)}
print("U coefficients from near-wall fit:")
for m in m_list:
    print("  U[%+d] = s^(%+.2f) = %.8e"%(m, m*MU, Ud[m]))

# Step 2: Frobenius recurrence P = sum a_k s^{k*mu}
# P'' + 2 beta/s P' - U P = 0
def frob(Ud, K=15):
    a = np.zeros(K+1); a[0]=1.0
    for k in range(1, K+1):
        p = k*MU
        # coefficient: a_k p(p-1+2 beta) = sum_j U[k-3-j] a_j
        rhs = 0.0
        for j in range(k):
            m = k-3-j
            rhs += Ud.get(m, 0.0)*a[j]
        a[k] = rhs/(p*(p-1.0+2.0*BETA))
    return a

for K in (5, 8, 12, 15):
    a_coef = frob(Ud, K)
    print("\nFrobenius a_k (K=%d):"%K)
    for k in range(K+1):
        if abs(a_coef[k]) > 1e-10:
            print("  a[%d] s^(%+.2f) = %.8e"%(k, k*MU, a_coef[k]))

# Step 3: build pencil with Frobenius peeling
def build_pencil_frob(N, b, a_coef, Kuse):
    z,D,D2 = cheb_gauss(N)
    omz = 1.0-z; t = (1.0+z)/omz; s = b*t
    sol = build_rho(b)
    rho = sol.sol(t)[0]
    g = omz**2/(2.0*b); gp = -omz/b
    Vv = V_of(rho)
    # P(s) = sum a_k s^{k*mu}, derivatives
    P = np.zeros_like(s, dtype=complex); Pp=P.copy(); Ppp=P.copy()
    for k in range(min(Kuse+1, len(a_coef))):
        p = k*MU
        P  += a_coef[k]*s**p
        Pp += a_coef[k]*p*s**(p-1.0)
        Ppp+= a_coef[k]*p*(p-1.0)*s**(p-2.0)
    U = Vv - 1.0/(3.0*s**2)
    C10 = 2.0*Pp/P + 2.0*BETA/s
    C00 = Ppp/P + 2.0*BETA*Pp/(s*P) - U
    Q0 = np.diag(g**2)@D2 + np.diag(g*gp+C10*g)@D + np.diag(C00)
    Q1 = 1j*(np.diag(2.0*g)@D + np.diag(C10))
    return Q0, Q1

b = complex(3.0, 1.5)
print("\n=== Solve with Frobenius peeling ===")
print("ANCHOR = %.12f %+.12fi"%(ANCHOR.real,ANCHOR.imag))
for K in (0, 3, 5, 8, 12):  # K=0 = simple peel
    a_coef = frob(Ud, max(K,12))
    for N in (60, 90):
        Q0,Q1 = build_pencil_frob(N, b, a_coef, K)
        w = beyn(Q0, Q1, ANCHOR, 0.008, nc=300)
        err = abs(w-ANCHOR); dig=-math.log10(err) if err>0 else 20
        print("  K=%2d N=%3d: w=%.12f %+.12fi  |err|=%.3e %.1f dig"%(K,N,w.real,w.imag,err,dig))
