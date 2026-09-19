# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

# 修正: V = f(l(l+1)/r^2 + f'/r), f=1-2/r, f'=2/r^2
# ODE: x(1-x)^2 y'' + (1-4x+3x^2-4iw)y' - (l(l+1)+1-x) y = 0
# 递推: alpha_n = n(n-4iw)
#        beta_n  = -(2n^2-2n+2l(l+1)+1)
#        gamma_n = (n-1)^2

def forward_series(w, ell, N=300):
    a = [complex(1.0,0.0)]
    # n=1: gamma_1=0, alpha_1 a1 + beta_1 a0 = 0
    alpha1 = 1.0*(1.0-4.0j*w)
    beta1  = -(2.0-2.0+2.0*ell*(ell+1)+1.0)
    a.append(-beta1*a[0]/alpha1)
    for n in range(2, N+1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + 2.0*ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        an = -(beta*a[n-1] + gamma*a[n-2])/alpha
        a.append(an)
    return a

def leaver_R_down(w, ell, N=2000):
    """向下连分数: R_{n-1} = -gamma_n/(beta_n + alpha_n R_n), R_{N+1}=0, 到 R_1"""
    R = 0.0+0.0j
    for n in range(N, 1, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + 2.0*ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        denom = beta + alpha*R
        R = -gamma/denom
    return R  # R_1

w = complex(0.37367, -0.08896)
ell = 2
a = forward_series(w, ell, N=300)
print("Forward series at w=0.37367-0.08896i (corrected):")
for n in [0,1,2,5,10,20,50,100,200,300]:
    r = abs(a[n])/abs(a[n-1]) if n>0 else float('nan')
    print(f"  n={n:4d}  |a_n|={abs(a[n]):.6e}  ratio={r:.6f}")

# 向下连分数
R1 = leaver_R_down(w, ell, N=2000)
target = (2*ell*(ell+1)+1)/(1.0-4.0j*w)
print(f"\nR1_down = {R1.real:+.6e}{R1.imag:+.6e}i")
print(f"R1_target(horizon) = {target.real:+.6e}{target.imag:+.6e}i")
print(f"|F| = {abs(R1-target):.3e}")
