# -*- coding: utf-8 -*-
import numpy as np

def forward_series(w, ell, N=2000):
    a = [complex(1.0,0.0)]
    alpha1 = 1.0*(1.0-4.0j*w)
    beta1  = -(2.0*ell*(ell+1)+1.0)
    a.append(-beta1*a[0]/alpha1)
    for n in range(2, N+1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + 2.0*ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        an = -(beta*a[n-1] + gamma*a[n-2])/alpha
        a.append(an)
    return a

ell = 2
for wtest in [complex(0.37367,-0.08896), complex(0.37367,+0.08896)]:
    a = forward_series(wtest, ell, N=2000)
    print(f"w={wtest}")
    for n in [1,10,50,100,300,500,1000,1500,2000]:
        r = abs(a[n])/abs(a[n-1])
        print(f"  n={n:5d}  |a_n|={abs(a[n]):.6e}  ratio={r:.6f}")
    print()
