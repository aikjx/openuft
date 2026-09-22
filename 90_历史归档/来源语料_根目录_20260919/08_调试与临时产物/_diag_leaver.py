# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

def leaver_R1(w, ell, N=1200):
    R = 0.0+0.0j
    for n in range(N, 1, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1))
        gamma = n*(n-2.0)
        denom = beta + alpha*R
        R = -gamma/denom
    return R

w = complex(0.37367, -0.08896)
ell = 2
for N in [100, 500, 1000, 2000, 4000]:
    R1 = leaver_R1(w, ell, N)
    target = ell*(ell+1)/(1.0-4.0j*w)
    print(f"N={N:5d}  R1={R1.real:+.6e}{R1.imag:+.6e}i  target={target.real:+.6e}{target.imag:+.6e}i  F={abs(R1-target):.3e}")
