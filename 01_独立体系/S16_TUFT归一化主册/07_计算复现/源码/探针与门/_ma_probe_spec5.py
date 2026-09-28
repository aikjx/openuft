# -*- coding: utf-8 -*-
"""_ma_probe_spec5.py — calibrate spectral framework on Regge-Wheeler (analytic known)
RW: f^2 psi'' + f f' psi' + (w^2 - V_RW) psi = 0,  V_RW = 6 f (r-1)/r^3,  f=1-2/r
Known: w0 = 0.37367168441804166 - 0.08896231568893410j  (l=2)
Test: does Jansen compactification + derivative BC + Chebyshev give det(M(w0))~0?"""
import numpy as np
import math
sys_path = r'D:\a10\aikjx\code\my_lib'

def cheb_gauss(N):
    j  = np.arange(1, N+1)
    th = np.pi*(j-0.5)/N
    z  = np.cos(th)
    w  = ((-1.0)**(j-1))*np.sin(th)
    zi, zj = np.meshgrid(z, z, indexing='ij')
    wi, wj = np.meshgrid(w, w, indexing='ij')
    with np.errstate(divide='ignore', invalid='ignore'):
        D = (wj/wi)/(zi-zj)
    np.fill_diagonal(D, 0.0)
    np.fill_diagonal(D, -D.sum(axis=1))
    return z, D, D@D

def assemble_rw(w, N, b):
    z, D, D2 = cheb_gauss(N)
    omz = 1.0 - z
    r = 2.0 + b*(1.0+z)/omz            # Jansen: r in [2, inf)
    f = 1.0 - 2.0/r
    fp = 2.0/r**2
    V = 6.0*f*(r-1.0)/r**3
    # dr/dz and d2r/dz2
    # r = 2 + b(1+z)/(1-z) => dr/dz = 2b/(1-z)^2 ; d2r/dz2 = 4b/(1-z)^3
    dzd = (1.0-z)**2/(2.0*b)           # dz/dr = (1-z)^2/(2b)
    d2z = -(1.0-z)**3/(2.0*b*b)        # d2z/dr2
    # psi_rr = dzdr^2 D2 + d2zdr2 D ;  psi_r = dzdr D
    Lop = (np.diag(f*f*dzd**2)@D2 + np.diag(f*f*d2z)@D
           + np.diag(f*fp*dzd)@D)
    M = Lop + np.diag(w*w - V)
    # boundary rows: incoming horizon (r->2): psi ~ e^{-i w r*} ~ (r-2)^{-2iw}?
    # For RW QNM: psi ~ (r-2)^{-2 i w} at horizon (ingoing), psi ~ e^{i w r} at inf
    # d psi/dr = -(2 i w)/(r-2) psi  near horizon
    idx_h = int(np.argmin(z))          # z->-1 -> r->2 (closest)
    M[idx_h,:] = dzd[idx_h]*D[idx_h,:]
    M[idx_h,idx_h] += 2j*w/(r[idx_h]-2.0)   # psi' - (-2iw/(r-2))psi = psi' + 2iw/(r-2)psi = 0
    # outgoing at inf: psi ~ e^{i w r} => psi' = i w psi
    idx_inf = int(np.argmax(z))
    M[idx_inf,:] = dzd[idx_inf]*D[idx_inf,:]
    M[idx_inf,idx_inf] -= 1j*w
    return M

w0 = 0.37367168441804166 - 0.08896231568893410j
for NN in (40, 60, 80):
    for bb in (complex(4.0,0.5), complex(8.0,0.5), complex(4.0,0.0)):
        M = assemble_rw(w0, NN, bb)
        s_ = np.linalg.svd(M, compute_uv=False)
        print('N=%d b=%s: sigma_min=%.3e cond=%.2e' % (NN, bb, s_[-1], s_[0]/s_[-1]))
