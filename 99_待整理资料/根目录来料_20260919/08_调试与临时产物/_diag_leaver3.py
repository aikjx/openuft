# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

def leaver_R2( w, ell, N=1200):
    """向下连分数算 R_2 = a_2/a_1 (infinity 边界)"""
    R = 0.0+0.0j  # R_{N+1}
    for n in range(N, 2, -1):  # n = N..3, 算 R_{n-1}, 最后得到 R_2
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1))
        gamma = n*(n-2.0)
        denom = beta + alpha*R
        R = -gamma/denom
    return R  # R_2

def F(w, ell):
    R2 = leaver_R2(w, ell, N=1500)
    # horizon: n=2, gamma_2=0 => alpha_2 R_2 + beta_2 = 0 => R2 = -beta_2/alpha_2
    alpha2 = 2.0*(2.0-4.0j*w)
    beta2  = -(2.0*4 - 4.0 + ell*(ell+1))
    R2_h = -beta2/alpha2
    return R2 - R2_h

w = complex(0.37367, -0.08896)
ell = 2
for N in [200, 500, 1000, 2000, 4000]:
    R2 = leaver_R2(w, ell, N)
    alpha2 = 2.0*(2.0-4.0j*w)
    beta2  = -(8.0 - 4.0 + 6.0)
    R2_h = -beta2/alpha2
    print(f"N={N:5d}  R2_down={R2.real:+.6e}{R2.imag:+.6e}i  R2_h={R2_h.real:+.6e}{R2_h.imag:+.6e}i  |F|={abs(R2-R2_h):.3e}")

# 搜索根
def J(x):
    ww = complex(x[0], x[1])
    f = F(ww, 2)
    return [f.real, f.imag]
sol = root(J, [0.373, -0.09], method="hybr", tol=1e-12, options={"xtol":1e-12,"maxfev":3000})
wfound = complex(sol.x[0], sol.x[1])
print("root l=2,n=0:", wfound, " err=", abs(wfound-complex(0.37367,-0.08896)))
