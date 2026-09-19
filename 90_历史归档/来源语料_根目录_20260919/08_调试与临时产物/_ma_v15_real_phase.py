# -*- coding: utf-8 -*-
"""
MainAgent v15 - STABLE real-frequency reflection phase (independent IVP).
Bypasses ill-posed complex-QNM pole search. TUFT wall W1 Neumann, integrate
OUTWARD on real omega axis; far-field decompose psi=C+ e^{iws}+C- e^{-iws},
r(w)=C+/C-. Perfect wall: conserved flux Im(psi*psi')=0 -> |r|=1 (self-check).
arg r=2delta, round-trip delay tau=d(arg r)/dw. Sharp 2pi winding + narrow tall
tau peak = high-Q cavity mode; smooth phase tau~2L = no new discrete spectrum.
A=e^-2/r; B=e^2/r(1+c_m/r^2+d/r^3); ds/dr=e^2/r sqrt(1+c_m/r^2+d/r^3); V=e^-2/r 6/r^2.
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
def P(*a):print(*a,flush=True)
DS=0.02; SMAX=120.0
def build(cm,dd):
    roots=np.roots([1.0,0.0,cm,dd]); rh=min(x.real for x in roots if abs(x.imag)<1e-8 and x.real>0)
    Nr=600000; rhi=SMAX+30.0
    r=np.linspace(rh,rhi,Nr+1)
    q=np.sqrt(np.maximum(1+cm/r**2+dd/r**3,0.0)); dsdr=np.exp(2/r)*q; dr=r[1]-r[0]
    s=np.concatenate([[0.0],np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*dr)])
    V=np.exp(-2/r)*6/r**2
    n=int(SMAX/DS); sg=np.linspace(0,n*DS,n+1); Vg=np.interp(sg,s,V)
    L=s[np.argmin(np.abs(r-1.0))]
    return rh,L,Vg
def reflection(Vg,omega,sout):
    N=int(sout/DS); w2=omega*omega
    u=np.array([1.0,0.0])
    for k in range(N):
        a1=w2-Vg[k]; a2=w2-Vg[k+1]
        x,y=u;
        k1=np.array([y,a1*x])
        u2=u+0.5*DS*k1; k2=np.array([u2[1],a1*u2[0]])
        u3=u+0.5*DS*k2; k3=np.array([u3[1],a1*u3[0]])
        u4=u+DS*k3;     k4=np.array([u4[1],a2*u4[0]])
        u=u+DS/6*(k1+2*k2+2*k3+k4)
    psi,p=u
    Cp=(psi+p/(1j*omega))/2; Cm=(psi-p/(1j*omega))/2
    return Cp/Cm, np.imag(np.conj(psi)*p)
def run(cm,dd):
    rh,L,Vg=build(cm,dd)
    om=np.round(np.unique(np.concatenate([
        np.linspace(.15,.30,7),np.linspace(.32,.45,14),np.linspace(.50,.85,8),
        np.linspace(.86,.96,11),np.linspace(1.0,1.2,5)])),5)
    P("="*88);P("TUFT wall c_m=%g d=%g | r_h=%.4f M  L(wall->r=1)=%.3f  2L=%.3f M = %.3f ms @30Msun"%(
        cm,dd,rh,L,2*L,2*L*4.9256*30/1000));P("="*88)
    out={}
    for sout in (80.0,120.0):
        R=[];J=[]
        for w in om:
            r,j=reflection(Vg,w,sout); R.append(r); J.append(j)
        out[sout]=(np.array(R),np.array(J))
    R80,J80=out[80.0]; R120,J120=out[120.0]
    P("flux/|r| self-check (both must be ~0 = perfect reflection), and s_out 80 vs 120 convergence:")
    P("  %-7s %-11s %-11s %-11s %-11s %-11s"%("w","||r|-1|80","||r|-1|120","d(arg)","flux80","flux120"))
    a80=np.angle(R80); a120=np.angle(R120)
    for i in range(0,len(om),2):
        P("  %-7.3f %-11.2e %-11.2e %-11.2e %-11.2e %-11.2e"%(
            om[i],abs(abs(R80[i])-1),abs(abs(R120[i])-1),
            abs(np.sin(a80[i]-a120[i])),J80[i],J120[i]))
    ph=np.unwrap(a120); tau=np.gradient(ph,om)
    P("\n  %-7s %-10s %-11s %-9s %s"%("w","arg(unw)","tau(M)","tau/2L","note"))
    for i in range(len(om)):
        n=""
        if abs(om[i]-.3737)<.012:n="<- GR QNM Re 0.3737"
        if abs(om[i]-np.sqrt(6*np.exp(-2)))<.012:n="<- sqrt(Vmax)=0.9011"
        P("  %-7.3f %-10.3f %-11.3f %-9.2f %s"%(om[i],ph[i],tau[i],tau[i]/(2*L),n))
    pk=np.nanmax(np.abs(tau));iw=int(np.nanargmax(np.abs(tau)))
    P("\n  max|tau|=%.2f M at w=%.3f (tau/2L=%.2f)."%(pk,om[iw],pk/(2*L)))
    return om,ph,tau,L
res={}
for cm,dd in [(-0.5,0.0),(-0.29,-0.05)]:
    res[cm]=run(cm,dd)
P("\nDone.")
