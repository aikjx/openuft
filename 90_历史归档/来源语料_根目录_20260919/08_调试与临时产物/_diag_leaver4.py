# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

def leaver_R2_asym(w, ell, N=2000):
    """用渐近值初始化的向下连分数"""
    # 渐近分支: p_+ (decaying), R_n -> 1 - (p+1)/n
    p_coeff = 4.0j*w - 1.0
    disc = np.sqrt(p_coeff**2 + 4.0*ell*(ell+1))
    p_plus = (-p_coeff + disc)/2.0  # decaying branch (larger real part)
    # R_{N+1} ~ 1 - (p_plus+1)/(N+1)
    R = 1.0 - (p_plus+1)/(N+1)
    for n in range(N, 2, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1))
        gamma = n*(n-2.0)
        denom = beta + alpha*R
        R = -gamma/denom
    return R

w = complex(0.37367, -0.08896)
ell = 2
for N in [200, 500, 1000, 2000, 4000, 8000]:
    R2 = leaver_R2_asym(w, ell, N)
    alpha2 = 2.0*(2.0-4.0j*w)
    beta2  = -(8.0 - 4.0 + 6.0)
    R2_h = -beta2/alpha2
    print(f"N={N:5d}  R2={R2.real:+.6e}{R2.imag:+.6e}i  R2_h={R2_h.real:+.6e}{R2_h.imag:+.6e}i  |F|={abs(R2-R2_h):.3e}")
