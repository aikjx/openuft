# -*- coding: utf-8 -*-
"""_ma_probe_spec3.py — test infinity exponent candidates for spectral matrix"""
import numpy as np
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
import _ma_tuft_spin_spectral as m

w0 = 0.37367168441804166 - 0.08896231568893410j

def assemble_exp(exp_inf, exp_h=2, N=60, b=complex(4.0,0.5)):
    s, l, a, mm = -2, 2, 0.0, 2
    z, D, D2 = m.cheb_gauss(N)
    omz = 1.0 - z
    rp = 1.0 + np.sqrt(1.0 - a*a); rm = 1.0 - np.sqrt(1.0 - a*a)
    r = rp + b*(1.0 + z)/omz
    Delta = (r - rp)*(r - rm)
    dzdr = (1.0-z)**2/(2.0*b)
    d2zdr2 = -(1.0-z)**3/(2.0*b*b)
    Lop = (np.diag(Delta*dzdr**2)@D2 + np.diag(Delta*d2zdr2)@D
           - np.diag((2.0*r-2.0)*dzdr)@D)
    r2pa2 = r*r + a*a
    K2c_w2 = -(r2pa2)**2/Delta
    K2c_w  = +2.0*a*mm*r2pa2/Delta
    K2c_c  = -a*a*mm*mm/Delta
    ic_w = -4j*(r-1.0)*r2pa2/Delta
    ic_c = +4j*(r-1.0)*a*mm/Delta
    E = m.angular_sep_const(a*w0, s, l, mm)
    A2 = K2c_w2 + a*a
    A1 = K2c_w + ic_w + 8j*r - 2.0*a*mm
    A0 = K2c_c + ic_c + (E - 2.0)
    M = Lop + np.diag(A2*w0*w0 + A1*w0 + A0)
    # horizon BC (index -2-i sigma+)
    idx_h = int(np.argmin(z))
    rho0 = 2.0 + 1j*a*mm/(rp-rm); rho1 = -2j*rp/(rp-rm)
    M[idx_h,:] = dzdr[idx_h]*D[idx_h,:]
    M[idx_h,idx_h] -= rho0/(r[idx_h]-rp) + w0*rho1/(r[idx_h]-rp)
    # infinity BC: R' = (exp_inf/r + i w0) R  (s=-2 outgoing r^{exp_inf} e^{i w0 r})
    idx_inf = int(np.argmax(z))
    M[idx_inf,:] = dzdr[idx_inf]*D[idx_inf,:]
    M[idx_inf,idx_inf] -= exp_inf/r[idx_inf] + 1j*w0
    return M

for exp_inf in (3, -3, -1, 1):
    M = assemble_exp(exp_inf)
    s_ = np.linalg.svd(M, compute_uv=False)
    print('exp_inf=%+d: sigma_min=%.3e  cond=%.2e' % (exp_inf, s_[-1], s_[0]/s_[-1]))
