# -*- coding: utf-8 -*-
"""Diagnostic: print QNM-window spectrum of Robin eigenproblem."""
import numpy as np
from scipy.special import lambertw
from scipy.linalg import eigvals

M=1.0; l=2
def r_from_rstar(rstar):
    rstar=np.asarray(rstar,dtype=complex)
    return 2*M*(1+lambertw(rstar/(2*M)-1.0))
def V_rw(r,l=2):
    r=np.asarray(r,dtype=complex); f=1-2*M/r
    return f*(l*(l+1)/r**2-6*M/r**3)

def solve(N, rs_min, rs_max):
    rs=np.linspace(rs_min,rs_max,N); h=rs[1]-rs[0]
    V=V_rw(r_from_rstar(rs).real,l).real
    M0=np.zeros((N,N),dtype=complex); M1=np.zeros((N,N),dtype=complex)
    for i in range(N):
        if i==0:
            M0[0,0]=-(2/h**2)-V[0]; M0[0,1]=2/h**2; M1[0,0]=2j/h
        elif i==N-1:
            M0[N-1,N-1]=-(2/h**2)-V[N-1]; M0[N-1,N-2]=2/h**2; M1[N-1,N-1]=2j/h
        else:
            M0[i,i-1]=1/h**2; M0[i,i]=-(2/h**2)-V[i]; M0[i,i+1]=1/h**2
    H=np.zeros((2*N,2*N),dtype=complex)
    H[0:N,N:2*N]=np.eye(N); H[N:2*N,0:N]=-M0; H[N:2*N,N:2*N]=-M1
    return eigvals(H), h

ev,h=solve(800,-20.0,80.0)
sel=[w for w in ev if 0.1<w.real<0.7 and -0.4<w.imag<-0.01]
sel.sort(key=lambda w:-w.imag)
print("h=",h,"N eigenvals:",len(ev))
print("modes in window (Re 0.1-0.7, Im -0.4..-0.01):")
for w in sel[:25]:
    print(f"  {w.real:.5f}{w.imag:+.5f}i")
