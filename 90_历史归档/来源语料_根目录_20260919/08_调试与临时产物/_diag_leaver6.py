# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

# 正确递推:
# alpha_n = n(n-4iw)
# beta_n  = -(2n^2-2n + l(l+1) + 1)
# gamma_n = (n-1)^2

def forward_series(w, ell, N=2000):
    a = [complex(1.0,0.0)]
    alpha1 = 1.0*(1.0-4.0j*w)
    beta1  = -(ell*(ell+1)+1.0)
    a.append(-beta1*a[0]/alpha1)
    for n in range(2, N+1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        an = -(beta*a[n-1] + gamma*a[n-2])/alpha
        a.append(an)
    return a

def leaver_R1(w, ell, N=2000):
    R = 0.0+0.0j
    for n in range(N, 1, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        R = -gamma/(beta + alpha*R)
    return R

ell = 2
w = complex(0.37367, -0.08896)
a = forward_series(w, ell, N=2000)
print("Forward (corrected beta):")
for n in [1,10,50,100,300,500,1000,1500,2000]:
    r = abs(a[n])/abs(a[n-1])
    print(f"  n={n:5d}  |a_n|={abs(a[n]):.6e}  ratio={r:.6f}")

R1 = leaver_R1(w, ell, N=2000)
target = (ell*(ell+1)+1)/(1.0-4.0j*w)
print(f"\nR1_down={R1.real:+.6e}{R1.imag:+.6e}i")
print(f"target ={target.real:+.6e}{target.imag:+.6e}i")
print(f"|F|={abs(R1-target):.3e}")
