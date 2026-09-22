# -*- coding: utf-8 -*-
import sys, numpy as np
from scipy.linalg import eig
sys.path.insert(0,r"D:\a10\aikjx\code\my_lib")
# 复用主脚本里的势与 cheb（直接内联，避免执行其主体）
from scipy.interpolate import CubicSpline
exec(open(r"D:\a10\aikjx\code\my_lib\_ma_v21_pole.py",encoding="utf-8").read().split("# =====")[0].split("def build_GR")[0]) if False else None

def cheb(N):
    y=np.cos(np.pi*np.arange(N+1)/N)
    c=np.r_[2.0,np.ones(N-1),2.0]*(-1.0)**np.arange(N+1)
    Y=np.tile(y,(N+1,1)); dY=Y-Y.T
    D=(c[:,None]/c[None,:])/(dY+np.eye(N+1)); D=D-np.diag(D.sum(1))
    return D,y

ell=2
r=np.concatenate([np.linspace(2+1e-12,3.0,40000),np.linspace(3.0,10.0,40000),np.linspace(10.0,400,40000)])
r=np.unique(r); rst=r+2*np.log(r/2-1); f=1-2/r
V=f*(6/r**2-6/r**3)
o=np.argsort(rst); Vspl=CubicSpline(rst[o],V[o])
CAT=0.3736716844-0.0889623157j

for N,R in [(200,60.0),(200,80.0)]:
    D,y=cheb(N); x=R*y; Dx=D/R
    D2=Dx@Dx
    Vcol=np.clip(np.array([float(Vspl(float(xi))) for xi in x]),0,None)
    n=N+1; I=np.eye(n); Z=np.zeros((n,n))
    A2=I.copy(); A1=np.zeros((n,n),complex); A0=D2-np.diag(Vcol)
    # 外 idx0 出射 +; 内 idxN 入射 -
    A0[0,:]=Dx[0,:]; A1[0,0]=-1j; A2[0,:]=0
    A0[N,:]=Dx[N,:]; A1[N,N]=+1j; A2[N,:]=0
    M=np.vstack([np.hstack([A0,A1]),np.hstack([Z,I])])
    Bm=np.vstack([np.hstack([Z,-A2]),np.hstack([I,Z])])
    w,_=eig(M,Bm); w=np.asarray(w).ravel()
    wf=w[np.isfinite(w.real)&np.isfinite(w.imag)]
    print("=== N=%d R=%g  total finite=%d"%(N,R,len(wf)),flush=True)
    near=wf[np.argsort(np.abs(wf-CAT))][:12]
    for z in near: print("   %.6f %+.6f i  |d|=%.3e"%(z.real,z.imag,abs(z-CAT)),flush=True)
    low=wf[(abs(wf.imag)<0.3)&(wf.real>0)&(wf.real<1)&(wf.imag<0)]
    print("   #modes with Re in(0,1), Im in(-.3,0):",len(low),flush=True)
