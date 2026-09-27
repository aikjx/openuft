# -*- coding: utf-8 -*-
import numpy as np, math
C_LIGHT=299792458.0; G_N=6.67430e-11; HBAR=1.054571817e-34; M_E=9.1093837015e-31
ALPHA=1.0/137.035999084; OMEGA_DE=0.6875
E_P=math.sqrt(HBAR*C_LIGHT**5/G_N); E_EL=M_E*C_LIGHT**2/E_P
WE,WN=1.0,0.1
r=np.logspace(-3.0,2.0,400)
p0=[1e-6,0.1,0.01,2.0,1e-6,0.1,0.75,2.0]
names=["Kc","lK","r0","p","Tc","lT","O0","lO"]
def obs(pa):
    Kc,lK,r0,pw,Tc,lT,O0,lO=pa
    K=Kc*np.exp(-r/lK)/(1.0+(r/r0)**pw); T=Tc*np.exp(-r/lT); Om=OMEGA_DE+(O0-OMEGA_DE)*np.exp(-r/lO)
    E=ALPHA*np.trapezoid(K*T*Om*r**2,r)*4.0*math.pi
    N=np.trapezoid((Om-OMEGA_DE)*r**2,r)
    return WE*((E-E_EL)/E_EL)**2+WN*(N-1.0)**2
def obs_full(pa):
    Kc,lK,r0,pw,Tc,lT,O0,lO=pa
    K=Kc*np.exp(-r/lK)/(1.0+(r/r0)**pw); T=Tc*np.exp(-r/lT); Om=OMEGA_DE+(O0-OMEGA_DE)*np.exp(-r/lO)
    E=ALPHA*np.trapezoid(K*T*Om*r**2,r)*4.0*math.pi
    N=np.trapezoid((Om-OMEGA_DE)*r**2,r)
    return K,T,Om,E,N
# FD
gfd=np.zeros(8)
for i in range(8):
    h=1e-6*max(abs(p0[i]),1e-9); pl=list(p0); pm=list(p0); pl[i]+=h; pm[i]-=h
    gfd[i]=(obs(pl)-obs(pm))/(2*h)
# analytic
K,T,Om,Eval,Nval=obs_full(p0)
Kc,lK,r0,pw,Tc,lT,O0,lO=p0
x=r/r0; denom=1.0+x**pw; expO=np.exp(-r/lO)
gK=[K/Kc, K*r/lK**2, K*pw*x**pw/(r0*denom), K*np.log(x)*x**pw/denom,
    np.zeros_like(r),np.zeros_like(r),np.zeros_like(r),np.zeros_like(r)]
gT=[np.zeros_like(r),np.zeros_like(r),np.zeros_like(r),np.zeros_like(r),
    T/Tc, T*r/lT**2, np.zeros_like(r),np.zeros_like(r)]
gO=[np.zeros_like(r),np.zeros_like(r),np.zeros_like(r),np.zeros_like(r),
    np.zeros_like(r),np.zeros_like(r), expO, (O0-OMEGA_DE)*expO*r/lO**2]
print("E=%.4e N=%.4f E_EL=%.4e"%(Eval,Nval,E_EL))
print("i name   gaE          gaN          ga_chi2      gfd          ratio")
for i in range(8):
    gae=ALPHA*4.0*math.pi*np.trapezoid((gK[i]*T*Om+K*gT[i]*Om+K*T*gO[i])*r**2,r)
    gan=np.trapezoid(gO[i]*r**2,r)
    ga=2*WE*(Eval-E_EL)/E_EL**2*gae+2*WN*(Nval-1.0)*gan
    ratio=ga/gfd[i] if gfd[i]!=0 else float('nan')
    print("%d %-3s  %+.3e %+.3e  %+.3e %+.3e  %.4f"%(i,names[i],gae,gan,ga,gfd[i],ratio))
