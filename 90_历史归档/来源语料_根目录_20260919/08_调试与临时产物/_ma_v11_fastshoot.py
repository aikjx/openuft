"""
MainAgent v11 高效独立打靶（与 Leaver 连分数/E348 完全无关的第二种方法）
- 视界纯入射 Frobenius：纯数值幂级数递推（无 sympy 符号解，毫秒级）
- 单侧从视界沿 r 向外积分 DOP853（状态 psi, q=dpsi/dr*）
- 远场用 1/r 球波渐近基 psi_+=e^{+iw r*}/r（出射）、psi_-=e^{-iw r*}/r（入射）分解
- QNM 条件：入射系数 B(w)=0；双实部 fsolve 复求根
判 8e-7 区分度，双精度足够；用 eps/R/级数阶 三重收敛表自证。
M=1, f=1-2/r, V=f*(l(l+1)/r^2 + 2/r^3)
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

def conv(a,b,K):
    c=np.zeros(K+1,dtype=complex)
    for i,ai in enumerate(a[:K+1]):
        for j,bj in enumerate(b[:K+1-i]):
            c[i+j]+=ai*bj
    return c

def frob_coeffs(omega,lam,K):
    w=omega
    # f = x/(2+x) = sum_{k>=1} (-1)^{k+1} x^k / 2^k
    F=np.zeros(K+1,dtype=complex); FP=np.zeros(K+1,dtype=complex); FPP=np.zeros(K+1,dtype=complex)
    for k in range(1,K+2):
        s=((-1.0)**(k+1))/2.0**k
        if k<=K: F[k]=s
        if k-1<=K: FP[k-1]=k*s
        if k>=2 and k-2<=K: FPP[k-2]=k*(k-1)*s
    g1=np.zeros(K+1,dtype=complex)            # 1/r=1/(2+x)
    for n in range(K+1): g1[n]=((-1.0)**n)/2.0**(n+1)
    r2=conv(g1,g1,K); r3=conv(r2,g1,K)
    H=lam*r2+2.0*r3                            # lambda/r^2 + 2/r^3
    Vc=conv(F,H,K)
    alfa=-2j*w
    P=conv(F,F,K)                              # f^2
    Q=conv(conv(F,FP,K),np.array([2*alfa+1.0]),K)   # f f'(2a+1)
    S=alfa*alfa*conv(FP,FP,K)+alfa*conv(F,FPP,K)+w*w-Vc
    a=np.zeros(K+1,dtype=complex); a[0]=1.0
    for m in range(1,K+1):
        num=0j
        for i in range(3,m+1):
            n=m-i+2; num+=P[i]*n*(n-1)*a[n]
        for i in range(2,m+1):
            n=m-i+1; num+=Q[i]*n*a[n]
        for i in range(1,m+1):
            num+=S[i]*a[m-i]
        den=P[2]*m*(m-1)+Q[1]*m+S[0]
        a[m]=-num/den
    return a

def rstar(r): return r+2*np.log(r/2.0-1.0)

def incoming_B(wrwi,l,R=400.0,eps=1e-4,K=10):
    w=complex(*wrwi); lam=complex(l*(l+1))
    a=frob_coeffs(w,lam,K)
    x=eps
    y=sum(a[m]*x**m for m in range(K+1))
    yp=sum(m*a[m]*x**(m-1) for m in range(1,K+1))
    f0=x/(2+x); fp0=2.0/(2+x)**2
    psi=f0**(-2j*w)*y
    psi_r=(-2j*w)*f0**(-2j*w-1)*fp0*y + f0**(-2j*w)*yp
    q0=f0*psi_r
    def od(r,z):
        f=1-2.0/r; V=f*(lam/r**2+2.0/r**3)
        return [z[1]/f, -(w*w-V)*z[0]/f]
    sol=solve_ivp(od,(2+eps,R),[psi,q0],method='DOP853',rtol=2e-11,atol=2e-13,
                  dense_output=False)
    psiR,qR=sol.y[:,-1]
    fR=1-2.0/R
    # psi=(A e^{+}+B e^{-})/R ; q = A f (iw/R-1/R^2)+ B f (-iw/R-1/R^2)
    up=fR*(1j*w/R-1.0/R**2); um=fR*(-1j*w/R-1.0/R**2)
    # (1/R  1/R)(A)=(psiR); (up um)(B)=(qR)
    det=(1.0/R)*um-(1.0/R)*up
    A=(psiR*um-(1.0/R)*qR)/det
    B=((1.0/R)*qR-psiR*up)/det
    return B

def root(l,seed,R=400.0,eps=1e-4,K=10):
    sol=fsolve(lambda z:[incoming_B(z,l,R,eps,K).real,incoming_B(z,l,R,eps,K).imag],
               seed,xtol=1e-12,epsfcn=1e-9,full_output=False)
    return sol

if __name__=="__main__":
    seeds={0:(0.110455,-0.104896),1:(0.292936,-0.097660),2:(0.483644,-0.096759)}
    print("=== one-sided outward direct shooting, M=1 (independent of continued fraction) ===")
    for l in (2,1,0):
        wr,wi=root(l,seeds[l])
        print(f"l={l}  R=400 eps=1e-4 K=10 :  w = {wr:.9f} {wi:+.9f} i")
    print("\n--- l=0 triple convergence (the disputed mode) ---")
    for R,eps,K in [(200,1e-3,8),(400,1e-4,10),(700,1e-5,12),(400,1e-5,12)]:
        wr,wi=root(0,seeds[0],R,eps,K)
        print(f"  R={R:4d} eps={eps:.0e} K={K:2d} : {wr:.9f} {wi:+.9f} i")
    print("\nE348 continued-fraction l=0 = 0.1104549391 -0.1048957171 i")
    print("common 7-digit ref         = 0.1104557   -0.1048957   i")
