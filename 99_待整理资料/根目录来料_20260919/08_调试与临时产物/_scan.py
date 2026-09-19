# -*- coding: utf-8 -*-
"""Dense PML scan: find stable QNM across alpha/region/N."""
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

def solve(N, r_pmin, r_pmax, n_in, n_out, alpha):
    i_pmin=n_in; i_pmax=N-1-n_out
    h=(r_pmax-r_pmin)/(i_pmax-i_pmin)
    drds=np.ones(N,dtype=complex); rstar=np.zeros(N,dtype=complex)
    c=1+1j*alpha
    for i in range(i_pmin,i_pmax+1): rstar[i]=r_pmin+(i-i_pmin)*h
    for i in range(0,i_pmin): rstar[i]=r_pmin-c*((i_pmin-i)*h); drds[i]=c
    for i in range(i_pmax+1,N): rstar[i]=r_pmax+c*((i-i_pmax)*h); drds[i]=c
    V=V_rw(r_from_rstar(rstar),l)
    A=np.zeros((N,N),dtype=complex); B=np.zeros((N,N),dtype=complex)
    for i in range(N):
        row={}
        if i>=2 and i<=N-3:
            row[i-2]=1/(12*h**2);row[i-1]=-16/(12*h**2);row[i]=30/(12*h**2)
            row[i+1]=-16/(12*h**2);row[i+2]=1/(12*h**2)
        else:
            row[i]=2/h**2
            if i>0:row[i-1]=-1/h**2
            if i<N-1:row[i+1]=-1/h**2
        for j,co in row.items(): A[i,j]=co
        A[i,i]+=drds[i]**2*V[i]; B[i,i]=drds[i]**2
    ev=eigvals(A,B)
    return np.sqrt(ev), h

tgt=0.37367-0.08896j
print("scan (h and selected mode nearest target):")
for (rpmin,rpmax,nin,nout) in [(-10,40,150,250),(-15,55,200,350),(-20,80,250,500)]:
    for alpha in [0.25,0.4,0.55,0.7]:
        for N in [1000,1600]:
            ws,h=solve(N,rpmin,rpmax,nin,nout,alpha)
            w=ws[np.argmin(np.abs(ws-tgt))]
            print(f"[{rpmin},{rpmax}] pml{nin},{nout} a={alpha} N={N} h={h:.4f}: {w.real:.5f}{w.imag:+.5f}i")
