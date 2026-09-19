# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root

def leaver_R1(w, ell, N=2000):
    R = 0.0+0.0j
    for n in range(N, 1, -1):
        alpha = n*(n-4.0j*w)
        beta  = -(2.0*n*n - 2.0*n + ell*(ell+1)+1.0)
        gamma = (n-1.0)**2
        R = -gamma/(beta + alpha*R)
    return R

def F(x, ell=2):
    w = complex(x[0], x[1])
    R1 = leaver_R1(w, ell, N=2000)
    target = (ell*(ell+1)+1.0)/(1.0-4.0j*w)
    r = R1 - target
    return [r.real, r.imag]

for guess in [[0.373,-0.09],[0.46,-0.04],[0.5,-0.1]]:
    sol = root(F, guess, method="hybr", tol=1e-13, options={"xtol":1e-13,"maxfev":5000})
    wf = complex(sol.x[0], sol.x[1])
    print(f"guess={guess} -> w = {wf.real:.6f}{wf.imag:+.6f}i")
