# -*- coding: utf-8 -*-
import numpy as np
from scipy.linalg import eig
from scipy.interpolate import CubicSpline
def cheb(N):
    y=np.cos(np.pi*np.arange(N+1)/N)
    c=np.r_[2.0,np.ones(N-1),2.0]*(-1.0)**np.arange(N+1)
    Y=np.tile(y,(N+1,1)); dY=Y-Y.T
    D=(c[:,None]/c[None,:])/(dY+np.eye(N+1)); D=D-np.diag(D.sum(1)); return D,y
r=np.concatenate([np.linspace(2+1e-12,3.0,50000),np.linspace(3.0,10.0,50000),np.linspace(10.0,600,60000)])
r=np.unique(r); rst=r+2*np.log(r/2-1); f=1-2/r
V=f*(6/r**2-6/r**3); o=np.argsort(rst); Vspl=CubicSpline(rst[o],V[o])
rs_min,rs_max=rst[0],rst[-1]
CAT=0.3736716844-0.0889623157j

def run(N,R,a,sgn):
    D,y=cheb(N)
    K=R/np.sinh(a)
    x=K*np.sinh(a*y)                 # r*，端点 ±R
    g=K*a*np.cosh(a*y); gp=K*a*a*np.sinh(a*y)
    Dx=(D.T/g).T
    D2=(D.T/g**2).T - (D.T*(gp/g**3)).T
    Vcol=np.clip(np.array([float(Vspl(xi)) if (rs_min-1<=xi<=rs_max+1) else 0.0 for xi in x]),0,None)
    n=N+1; I=np.eye(n); Z=np.zeros((n,n))
    A2=I.copy(); A1=np.zeros((n,n),complex); A0=D2-np.diag(Vcol)
    A0[0,:]=Dx[0,:]; A1[0,0]=-sgn*1j; A2[0,:]=0          # 外端
    A0[n-1,:]=Dx[n-1,:]; A1[n-1,n-1]=+sgn*1j; A2[n-1,:]=0 # 内端
    M=np.vstack([np.hstack([A0,A1]),np.hstack([Z,I])])
    Bm=np.vstack([np.hstack([Z,-A2]),np.hstack([I,Z])])
    w,_=eig(M,Bm); w=np.asarray(w).ravel()
    w=w[np.isfinite(w.real)&np.isfinite(w.imag)]
    wl=w[(w.real>0.15)&(w.real<0.7)&(w.imag>-0.4)&(w.imag<0.4)]
    return wl

for sgn in [+1,-1]:
  print("##### boundary sgn =",sgn,"(+1 = 内入射e^-iw r* / 外出射e^+iw r*)",flush=True)
  for (N,R,a) in [(250,120,3.0),(350,150,3.0),(500,200,3.0)]:
    wl=run(N,R,a,sgn)
    # 下半平面近 catalog
    low=wl[wl.imag<0]
    pick = low[np.argsort(np.abs(low-CAT))][:5] if len(low) else []
    print(" N=%d R=%d a=%g  #lower=%d"%(N,R,a,len(low)),flush=True)
    for z in pick: print("    %.7f %+.7f i |d|=%.2e"%(z.real,z.imag,abs(z-CAT)),flush=True)
