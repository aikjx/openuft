# -*- coding: utf-8 -*-
import numpy as np

def forward_series(w, ell, N=200):
    """前向递推 a_0=1, 返回 a_n 列表"""
    a = [complex(1.0,0.0), complex(0.0,0.0)]
    # n=1: alpha1 a1 + beta1 a0 = 0
    alpha1 = 1.0*(1.0-4.0j*w)
    beta1  = -(2.0-2.0+ell*(ell+1))
    a[1] = -beta1*a[0]/alpha1
    for n in range(2, N+1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1))
        gamma = n*(n-2.0)
        # alpha a_n + beta a_{n-1} + gamma a_{n-2} = 0
        an = -(beta*a[n-1] + gamma*a[n-2])/alpha
        a.append(an)
    return a

w = complex(0.37367, -0.08896)
ell = 2
a = forward_series(w, ell, N=300)
print("n     |a_n|         ratio |a_n/a_{n-1}|")
for n in [0,1,2,3,5,10,20,50,100,150,200,250,300]:
    r = abs(a[n])/abs(a[n-1]) if n>0 else float('nan')
    print(f"{n:4d}  {abs(a[n]):.6e}   {r:.6f}")
print()
print("If decaying branch, |a_n| should decrease as n increases (ratio <1).")
print("If growing, ratio >1 and |a_n| blows up.")
