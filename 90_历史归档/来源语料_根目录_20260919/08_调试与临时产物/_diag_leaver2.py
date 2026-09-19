# -*- coding: utf-8 -*-
import numpy as np

def leaver_R1_trace(w, ell, N=500):
    R = 0.0+0.0j
    for n in range(N, 1, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1))
        gamma = n*(n-2.0)
        denom = beta + alpha*R
        R = -gamma/denom
        if n in [N, N-1, N-2, N//2, 100, 50, 20, 10, 5, 4, 3, 2]:
            print(f"  n={n:5d}  R_{{n-1}}={R.real:+.6e}{R.imag:+.6e}i  |R|={abs(R):.3e}  denom={denom.real:+.3e}{denom.imag:+.3e}i")
    return R

w = complex(0.37367, -0.08896)
print("w=", w)
R1 = leaver_R1_trace(w, 2, N=500)
print("R1=", R1)
target = 6.0/(1.0-4.0j*w)
print("target=", target)
