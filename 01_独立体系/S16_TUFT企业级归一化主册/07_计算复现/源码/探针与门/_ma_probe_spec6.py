# -*- coding: utf-8 -*-
"""_ma_probe_spec6.py — RW calibration: try Lobatto endpoints + larger b-imag; find why sigma_min doesn't shrink"""
import numpy as np

def cheb_lobatto(N):
    """Chebyshev-Lobatto nodes INCLUDING endpoints ±1 + D."""
    x = np.cos(np.pi*np.arange(N+1)/N)
    D = np.zeros((N+1, N+1))
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                ci = 2.0 if (i==0 or i==N) else 1.0
                cj = 2.0 if (j==0 or j==N) else 1.0
                D[i,j] = (ci/cj)*((-1.0)**(i+j))/(x[i]-x[j])
    for i in range(N+1):
        xi = x[i]
        if i==0: D[i,i] = (2*N*N+1)/6.0
        elif i==N: D[i,i] = -(2*N*N+1)/6.0
        else: D[i,i] = -xi/(2*(1-xi*xi))
    return x, D, D@D

w0 = 0.37367168441804166 - 0.08896231568893410j

def assemble_rw_lob(w, N, b):
    z, D, D2 = cheb_lobatto(N)
    omz = 1.0 - z
    r = 2.0 + b*(1.0+z)/omz
    f = 1.0 - 2.0/r
    fp = 2.0/r**2
    V = 6.0*f*(r-1.0)/r**3
    dzd = (1.0-z)**2/(2.0*b)
    d2z = -(1.0-z)**3/(2.0*b*b)
    Lop = (np.diag(f*f*dzd**2)@D2 + np.diag(f*f*d2z)@D + np.diag(f*fp*dzd)@D)
    M = Lop + np.diag(w*w - V)
    # interior points only: remove endpoint rows (index 0 = r->inf? r=2+b(1+z)/(1-z): z=+1->inf, z=-1->r=2)
    # z=+1 -> r->inf (idx 0); z=-1 -> r=2 (idx N)
    keep = np.arange(1, N)
    M = M[np.ix_(keep, keep)]
    # boundary via asymptotic relations replacing last kept row (near horizon) and first kept row (near inf)?
    # Simpler: use horizon Frobenius at the two endpoints as algebraic constraints via bordering:
    # We instead enforce: psi ~ (r-2)^{-2iw} at r=2, psi ~ e^{iwr} at inf, using endpoint rows as constraints.
    # Endpoint r=2 (z=-1): psi'(z=-1) relation from psi ~ (r-2)^p, p=-2iw: dpsi/dr = p/(r-2) psi -> singular; 
    #   use the row that replaces: approximate with psi(-1)=0? Not QNM-appropriate.
    # Give up endpoint handling: use 'one-sided' by evaluating ODE at interior + impose psi' at first interior matches e^{iwr}:
    return M

# Alternative clean approach: Jansen 2017 exact: r=2b/(1-z) for Schwarzschild? Use r=2/(1-z) with map r = 2 + ... 
# Let's just test convergence of sigma_min vs N for Lobatto interior-only (no BC rows) — spectral spurious?
for NN in (40, 80, 160):
    M = assemble_rw_lob(w0, NN, complex(4.0,0.5))
    s_ = np.linalg.svd(M, compute_uv=False)
    print('N=%d interior-only: sigma_min=%.3e cond=%.2e' % (NN, s_[-1], s_[0]/s_[-1]))
