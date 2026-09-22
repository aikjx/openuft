# -*- coding: utf-8 -*-
"""
GR sensitivity check for the real-frequency IVP engine.
Schwarzschild RW s=-2,l=2: start horizon-INGOING psi=e^{-i w s_in} at deep
s_in, integrate OUTWARD (stable IVP), decompose at infinity:
psi = C- e^{-iws} (incident) + C+ e^{iws} (reflected); R_GR=C+/C-.
Expect: conserved flux j=Im(psi* psi')=-w throughout (engine check, !=0 unlike
the wall); |R_GR|<1, |R|^2: ~1 low w (full reflection) -> ~0 high w (capture),
transition across l=2 barrier w~0.3-0.5 (QNM Re 0.3737 leaves structure).
If the engine resolves this known GR frequency structure, the TUFT wall's
featureless flat phase (sibling script) is a genuine physical null, not blindness.
s(r)=r+2 ln(r/2-1); V=f(6/r^2-6/r^3), f=1-2/r.
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
def P(*a):print(*a,flush=True)
SIN=-11.0; SOUT=120.0; DS=0.02
# build s(r) from r=2+delta .. rhi
Nr=700000; rlo=2.0+2.0*np.exp((SIN-2.0)/2.0); rhi=SOUT+30.0
r=np.linspace(rlo,rhi,Nr+1); f=1-2/r; Vr=f*(6/r**2-6/r**3)
dsdr=1.0/f; dr=r[1]-r[0]
s=np.concatenate([[SIN],SIN+np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*dr)])
n=int((SOUT-SIN)/DS); sg=SIN+np.arange(n+1)*DS; Vg=np.interp(sg,s,Vr)
P("GR table: r in [%.2e,%.1f], s in [%.1f,%.1f], N=%d, V(s_in)=%.2e"%(
 rlo,rhi,sg[0],sg[-1],n+1,Vg[0]))
def gr_R(w):
    psi=complex(np.exp(-1j*w*SIN)); p=-1j*w*psi
    j0=np.imag(np.conj(psi)*p)
    w2=w*w
    for k in range(n):
        a1=w2-Vg[k]; a2=w2-Vg[k+1]
        k1=np.array([p,a1*psi]);u2=np.array([psi,p])+0.5*DS*k1
        k2=np.array([u2[1],a1*u2[0]]);u3=np.array([psi,p])+0.5*DS*k2
        k3=np.array([u3[1],a1*u3[0]]);u4=np.array([psi,p])+DS*k3
        k4=np.array([u4[1],a2*u4[0]])
        psi,p=np.array([psi,p])+DS/6*(k1+2*k2+2*k3+k4)
    Cp=(psi+p/(1j*w))/2; Cm=(psi-p/(1j*w))/2
    jf=np.imag(np.conj(psi)*p)
    return Cp/Cm, j0, jf
P("\n  %-7s %-9s %-9s %-12s %-10s %s"%("w","|R|","|R|^2","flux j_f/-w","arg R","note"))
ws=np.round(np.concatenate([np.linspace(.10,.30,9),np.linspace(.32,.50,19),
                           np.linspace(.55,.90,8),np.linspace(1.0,1.4,5)]),4)
for w in ws:
    R,j0,jf=gr_R(w)
    n_=""
    if abs(w-.3737)<.012:n="<- GR QNM Re"
    if abs(w-np.sqrt(6*np.exp(-2)))<.012:n="<- sqrt(Vmax)"
    P("  %-7.3f %-9.4f %-9.4f %-12.5f %-10.4f %s"%(w,abs(R),abs(R)**2,jf/(-w),np.angle(R),n_))
P("\nInterpretation: |R|^2 must drop ~1 -> ~0 through w~0.3-0.5 (absorptive GR),")
P("flux ratio must be 1 (conservation). A strong w-dependence here proves the")
P("engine WOULD see a resonance; TUFT wall flat phase is therefore a true null.")
