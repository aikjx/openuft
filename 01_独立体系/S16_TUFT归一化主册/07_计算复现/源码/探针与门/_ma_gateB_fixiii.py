# -*- coding: utf-8 -*-
"""
_ma_gateB_fixiii.py — 判别：v49 (iii) 导数耦合 -> 常数对角，虚部是否收敛
========================================================================
v49 (iii) = i a m 2(r-1)/r^3 g D（导数耦合）→ splitI/a=1.6017（靶 0.00798，差200倍）
理论：4i(r-1)K/Delta 的 O(a) = -4 i m (r-1)/(r(r-2)) 是常数对角，非导数耦合。
替换后验证 splitI/a 是否回到 ~0.008。
"""
import numpy as np
import math, sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
from scipy.linalg import eig, null_space

GR_N0 = 0.37367168441804166 - 0.08896231568893410j
GR_SPLIT_SLOPE = 0.2515323

def cheb_gauss(N):
    j=np.arange(1,N+1); th=np.pi*(j-0.5)/N
    z=np.cos(th); w=((-1.0)**(j-1))*np.sin(th)
    zi,zj=np.meshgrid(z,z,indexing='ij'); wi,wj=np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'):
        D=(wj/wi)/(zi-zj)
    np.fill_diagonal(D,0.0); np.fill_diagonal(D,-D.sum(axis=1))
    return z,D,D@D

def run(N=60,b=complex(4.0,0.5),mode='const'):
    z,D,D2 = cheb_gauss(N)
    omz=1.0-z
    r=2.0+b*(1.0+z)/omz
    f=1.0-2.0/r; fp=2.0/r**2
    g=omz**2/(2.0*b); gp=-omz/b; rm2=r-2.0
    alpha=1.0-4.0/(r*rm2)+2.0/r
    alphap=-2.0*(r*r-8.0*r+8.0)/(r*r*rm2*rm2)
    V=6.0*f*(r-1.0)/r**3
    Q0=np.diag(f*f*g*g)@D2+np.diag(f*f*g*gp+f*fp*g)@D+np.diag(-V)
    Q1=1j*(np.diag(2.0*alpha*f*f*g)@D+np.diag(f*f*alphap+f*fp*alpha))
    Q2=np.diag(1.0-f*f*alpha*alpha)
    n=Q0.shape[0]; Z=np.zeros_like(Q0); I=np.eye(n)
    M=np.block([[Z,I],[-Q0,-Q1]]); Lm=np.block([[I,Z],[Z,Q2]])
    evb,rvb=eig(M,Lm,right=True)
    kb=np.argmin(np.abs(evb-GR_N0)); w0=evb[kb]; vv=rvb[:n,kb]
    Lwb=Q0+w0*Q1+w0*w0*Q2
    uu=null_space(Lwb.conj().T)[:,0]
    den=uu.conj()@(Q1+2*w0*Q2)@vv
    dQ1 = (np.diag(-2.0/r**2) + np.diag(+2.0*f/r**2))  # v49 (i)+(ii)
    if mode=='deriv':   # v49 (iii)
        dQ1 = dQ1 + 1j*(np.diag(2.0*(r-1.0)/r**3)*g)@D
    elif mode=='const': # 理论常数对角 -4i(r-1)/(r(r-2))
        dQ1 = dQ1 + np.diag(-4j*(r-1.0)/(r*rm2))
    ccoef=-(uu.conj()@(w0*dQ1)@vv)/den
    splitR_a=4.0*ccoef.real; splitI_a=4.0*ccoef.imag
    print("  mode=%-7s c=%.6f%+.6fi  splitR/a=%.6f (靶 .2515323)  splitI/a=%.6f (靶 .0079834)"%(
        mode,ccoef.real,ccoef.imag,splitR_a,splitI_a))
    return splitR_a, splitI_a

if __name__=='__main__':
    print("="*78)
    print("判别：v49 (iii) 导数耦合 vs 理论常数对角")
    print("="*78)
    for mode in ('deriv','const',''):
        if mode=='':
            print("  [仅 (i)+(ii)，无 (iii)]")
            dQ1_extra=None
        run(mode=mode)
