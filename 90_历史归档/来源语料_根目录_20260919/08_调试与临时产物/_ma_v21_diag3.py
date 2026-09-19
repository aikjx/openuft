# -*- coding: utf-8 -*-
import numpy as np
from scipy.linalg import eig
from scipy.interpolate import CubicSpline
def cheb(N):
    y=np.cos(np.pi*np.arange(N+1)/N)
    c=np.r_[2.0,np.ones(N-1),2.0]*(-1.0)**np.arange(N+1)
    Y=np.tile(y,(N+1,1)); dY=Y-Y.T
    D=(c[:,None]/c[None,:])/(dY+np.eye(N+1)); D=D-np.diag(D.sum(1)); return D,y
r=np.concatenate([np.linspace(2+1e-12,3.0,60000),np.linspace(3.0,10.0,60000),np.linspace(10.0,900,80000)])
r=np.unique(r); rst=r+2*np.log(r/2-1); f=1-2/r
V=f*(6/r**2-6/r**3); o=np.argsort(rst); Vspl=CubicSpline(rst[o],V[o])
rs_min,rs_max=rst[0],rst[-1]
CAT=0.3736716844-0.0889623157j
def run(N,R,a):
    D,y=cheb(N); K=R/np.sinh(a)
    x=K*np.sinh(a*y); g=K*a*np.cosh(a*y); gp=K*a*a*np.sinh(a*y)
    Dx=(D.T/g).T; D2=(D.T/g**2).T-(D.T*(gp/g**3)).T
    Vcol=np.clip(np.array([float(Vspl(xi)) if (rs_min-1<=xi<=rs_max+1) else 0.0 for xi in x]),0,None)
    n=N+1; I=np.eye(n); Z=np.zeros((n,n))
    A2=I.copy(); A1=np.zeros((n,n),complex); A0=D2-np.diag(Vcol)
    A0[0,:]=Dx[0,:]; A1[0,0]=-1j; A2[0,:]=0
    A0[n-1,:]=Dx[n-1,:]; A1[n-1,n-1]=+1j; A2[n-1,:]=0
    M=np.vstack([np.hstack([A0,A1]),np.hstack([Z,I])])
    Bm=np.vstack([np.hstack([Z,-A2]),np.hstack([I,Z])])
    w,_=eig(M,Bm); w=np.asarray(w).ravel()
    w=w[np.isfinite(w.real)&np.isfinite(w.imag)]
    low=w[(w.real>0.2)&(w.real<0.55)&(w.imag>-0.2)&(w.imag<0)]
    return low[np.argmin(np.abs(low-CAT))]
for (N,R,a) in [(650,250,3.0),(800,300,2.5),(900,350,3.0)]:
    z=run(N,R,a)
    print("N=%d R=%d a=%g -> %.9f %+.9f i  |d|=%.3e"%(N,R,a,z.real,z.imag,abs(z-CAT)),flush=True)
