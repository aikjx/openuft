# -*- coding: utf-8 -*-
"""
_ma_gateB_exactOA.py
GATE B 精确 O(a) 结构（第三独立，v49 三项微扰的修正版）
========================================================================
v49 FAIL 根因确认（对照重跑 out）：
  (i)   diag(-2 a m/(r^2+a^2))   近似 -2am/r^2 —— 错
  (ii)  diag(+2 a m f/r^2)       —— 错（符号/结构）
  (iii) i a m 2(r-1)/r^3 g D     导数耦合 —— 错：4i(r-1)K/Delta 的 O(a) 是常数对角项！

精确 O(a)（Hughes 4.3 完整展开，s=-2）：
  V = V0 + a V1 + O(a^2)
  K = r^2 w - a m + O(a^2)
  K^2 = r^4 w^2 - 2 a m r^2 w + O(a^2)
  4i(r-1)K = 4i(r-1) r^2 w - 4i(r-1) a m + O(a^2)
  Delta = r(r-2) + O(a^2)
  lambda = sA(aw) - 2 a m w + a^2 w^2 ;  sA(aw) = sA(0) + a w * dlam + O((aw)^2)
  => V1 (w 系数) = +2 m r^2/(r(r-2)) - 2 m + m*dlam   [对角]
     V1 (常数)   = -4 i m (r-1)/(r(r-2))              [对角，虚部！]
  dlam = d(sA)/dc|0 —— 数值标定（不 import qnm）
"""
import numpy as np
import math, sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
from scipy.linalg import eig, null_space

GR_N0 = 0.37367168441804166 - 0.08896231568893410j
GR_SPLIT_SLOPE = 0.2515323

def angular_sep_const(c, s, l, m, Nmat=28):
    lmin = max(abs(s), abs(m))
    def F(l):
        t1=(l+1)**2-m*m; t2=(l+1)**2-s*s
        if t1<=0 or t2<=0: return 0.0
        return math.sqrt(t1/((2*l+3)*(2*l+1)))*math.sqrt(t2)/(l+1)
    def G(l):
        if l==0: return 0.0
        t1=l*l-m*m; t2=l*l-s*s
        if t1<=0 or t2<=0: return 0.0
        return math.sqrt(t1/(4*l*l-1))*math.sqrt(t2)/l
    def H(l):
        if l==0 or s==0: return 0.0
        return -m*s/(l*(l+1))
    def A(l): return F(l)*F(l+1)
    def D_(l): return F(l)*(H(l+1)+H(l))
    def B(l): return F(l)*G(l+1)+G(l)*F(l-1)+H(l)*H(l)
    def E(l): return G(l)*(H(l-1)+H(l))
    def Cc(l): return G(l)*G(l-1)
    Nn=Nmat; lvals=[lmin+i for i in range(Nn)]
    Mm=np.zeros((Nn,Nn),dtype=complex)
    for i,lp in enumerate(lvals):
        for j,lc in enumerate(lvals):
            d=lc-lp
            if d==-2: Mm[i,j]=-c**2*A(lc)
            elif d==-1: Mm[i,j]=-c**2*D_(lc)+2*c*s*F(lc)
            elif d==0: Mm[i,j]=lp*(lp+1)-s*(s+1)-c**2*B(lp)+2*c*s*H(lp)
            elif d==1: Mm[i,j]=-c**2*E(lc)+2*c*s*G(lc)
            elif d==2: Mm[i,j]=-c**2*Cc(lc)
    ev=np.linalg.eigvals(Mm)
    tgt=l*(l+1)-s*(s+1)
    return complex(min(ev,key=lambda e:abs(e-tgt)))

def dlam_scan():
    """数值标定 d(sA)/dc 在 c=0：sA(eps)-sA(0))/eps"""
    eps = 1e-4
    d = (angular_sep_const(eps,-2,2,2) - angular_sep_const(0.0,-2,2,2))/eps
    return d

def cheb_gauss(N):
    j=np.arange(1,N+1); th=np.pi*(j-0.5)/N
    z=np.cos(th); w=((-1.0)**(j-1))*np.sin(th)
    zi,zj=np.meshgrid(z,z,indexing='ij'); wi,wj=np.meshgrid(w,w,indexing='ij')
    with np.errstate(divide='ignore',invalid='ignore'):
        D=(wj/wi)/(zi-zj)
    np.fill_diagonal(D,0.0); np.fill_diagonal(D,-D.sum(axis=1))
    return z,D,D@D

def gateB_exact(N=60,b=complex(4.0,0.5)):
    # ---- v49 骨架：RW QEP（门 A 已 PASS 同款）----
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
    # ---- a=0 eigenpair（Beyn 或直接 eig companion）----
    n=Q0.shape[0]; Z=np.zeros_like(Q0); I=np.eye(n)
    M=np.block([[Z,I],[-Q0,-Q1]]); Lm=np.block([[I,Z],[Z,Q2]])
    evb,rvb=eig(M,Lm,right=True)
    kb=np.argmin(np.abs(evb-GR_N0)); w0=evb[kb]; vv=rvb[:n,kb]
    Lwb=Q0+w0*Q1+w0*w0*Q2
    uu=null_space(Lwb.conj().T)[:,0]
    den=uu.conj()@(Q1+2*w0*Q2)@vv
    # ---- 精确 O(a) dQ1：w-系数对角 = 2m r^2/(r(r-2)) - 2m + m*dlam ----
    dlam = dlam_scan()
    dQ1_diag = 2.0*(r*r)/(r*rm2) - 2.0 + 1.0*dlam
    # 注意：v49 peel 骨架中 Q1 对应 w 系数矩阵（i(...)D 项），Q0 含 V 的 w 独立部分。
    # dQ1 必须以骨架量纲嵌入：V1 的 w 系数项直接作为 Q1 的 O(a) 修正（对角）。
    dQ1 = np.diag(dQ1_diag)
    ccoef = -(uu.conj()@(w0*dQ1)@vv)/den
    splitR_a = 4.0*ccoef.real
    prograde_a = 2.0*ccoef.real
    splitI_a = 4.0*ccoef.imag
    # ---- 常数项（虚部来源）4i(r-1)K/Delta O(a)：-4 i m (r-1)/(r(r-2)) ----
    dQ0_diag = -4j*1.0*(r-1.0)/(r*rm2)
    dQ0 = np.diag(dQ0_diag)
    ccoef0 = -(uu.conj()@(dQ0)@vv)/den
    splitR_a0 = 4.0*ccoef0.real
    splitI_a0 = 4.0*ccoef0.imag
    out = []
    out.append("sA'(0) = %.6f (数值标定)" % complex(dlam).real)
    out.append("a=0 eigenpair w=%.12f%+.12fi |err|=%.2e"%(w0.real,w0.imag,abs(w0-GR_N0)))
    out.append("[w-系数 dQ1]  c=%.6f%+.6fi  splitR/a=%.6f  prograde/a=%.6f  splitI/a=%.6f"%(
        ccoef.real,ccoef.imag,splitR_a,prograde_a,splitI_a))
    out.append("  vs 靶: splitR/a=0.2515323 prograde=0.12577 splitI/a=2*0.0039917=0.0079834")
    out.append("[常数项 dQ0]  c=%.6f%+.6fi  splitR/a=%.6f  splitI/a=%.6f"%(
        ccoef0.real,ccoef0.imag,splitR_a0,splitI_a0))
    okR = abs(splitR_a/GR_SPLIT_SLOPE-1.0)<5e-4
    out.append("GATE B (w-系数 splitR/a): %s"%("PASS" if okR else "FAIL"))
    return out

if __name__=='__main__':
    print("="*78)
    print("GATE B 精确 O(a) 结构（第三独立）")
    print("="*78)
    for line in gateB_exact():
        print(line)
