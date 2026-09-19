# -*- coding: utf-8 -*-
"""
v2 real-frequency reflection phase (SIGN-FIXED psi''=(V-w^2)psi; scipy DOP853).
Standing-wave IVP from wall Neumann psi(0)=1,psi'(0)=0. Decompose at a FIXED
near-outside point s_m where V~0: C+/-=(psi +/- psi'/(iw))/2. Shift the trivial
propagation phase to the wall reference: phi(w)=arg(C+/C-) - 2*w*s_m.
Resonance delay tau=d phi/d w. Free wall -> phi=0,tau=0. A leaky cavity ->
~2pi winding + tall narrow tau at its modes.
Control: toy square barrier must show modes near w_n~n*pi/L. Then TUFT.
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
from scipy.integrate import solve_ivp
def P(*a):print(*a,flush=True)

def phase_curve(Vfun,s_m,ws,max_step=0.02,label=""):
    ph=[]
    for w in ws:
        sol=solve_ivp(lambda s,y:[y[1],(Vfun(s)-w*w)*y[0]],[0,s_m],[1.0,0.0],
                      t_eval=[s_m],rtol=1e-11,atol=1e-12,max_step=max_step,method="DOP853")
        psi,pp=sol.y[:,0]
        Rp=(psi+pp/(1j*w))/(psi-pp/(1j*w))      # C+/C-
        a=np.angle(Rp)-2*w*s_m                   # shift to wall reference s=0
        ph.append(np.angle(np.exp(1j*a)))        # wrap to (-pi,pi]
    ph=np.array(ph); phu=np.unwrap(ph)
    tau=np.gradient(phu,ws)
    return phu,tau

# ---- toy cavity: must produce resonance peaks ----
L,WB,VB=2.93,1.5,3.0; sm=L+WB+8.0
Vtoy=lambda s: VB if (L<=s<=L+WB) else 0.0
wt=np.linspace(0.3,2.6,461)
pht,taut=phase_curve(Vtoy,sm,wt)
P("TOY cavity L=2.93 Vb=3 WB=1.5 ; FP modes ~ pi/L=%.3f, 2pi/L=%.3f"%(np.pi/L,2*np.pi/L))
# find positive delay peaks
pk=np.where((taut[1:-1]>taut[:-2])&(taut[1:-1]>taut[2:])&(taut[1:-1]>2.0))[0]+1
P("resonance delay peaks (w, tau M, tau/2L):")
for i in pk: P("  w=%.4f tau=%.2f  tau/2L=%.2f  (n=wL/pi=%.2f)"%(wt[i],taut[i],taut[i]/(2*L),wt[i]*L/np.pi))
if len(pk)==0: P("  *** NO PEAK -> engine still suspect ***")

# ---- TUFT real potential ----
def tuft_table(cm,dd,rhi=130.0,Nr=700000):
    roots=np.roots([1.,0.,cm,dd]); rh=min(x.real for x in roots if abs(x.imag)<1e-8 and x.real>0)
    r=np.linspace(rh,rhi,Nr+1);q=np.sqrt(np.maximum(1+cm/r**2+dd/r**3,0.))
    dsdr=np.exp(2/r)*q;dr=r[1]-r[0]
    s=np.concatenate([[0.],np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*dr)])
    V=np.exp(-2/r)*6/r**2
    return rh,s,V,r
def tuft_run(cm,dd):
    rh,s,V,r=tuft_table(cm,dd)
    Lc=s[np.argmin(np.abs(r-1.0))]
    iM=np.argmin(np.abs(V-6e-4)); sm=s[iM]
    Vfun=lambda x: np.interp(x,s,V)
    ws=np.round(np.concatenate([np.linspace(.30,.50,41),np.linspace(.52,.95,87),
                                np.linspace(.96,1.25,30)]),5)
    ws=np.unique(ws)
    ph,tau=phase_curve(Vfun,sm,ws,max_step=0.02)
    P("\n"+"="*80);P("TUFT c_m=%g d=%g r_h=%.4f L=%.3f ; decompose at s_m=%.2f (V=%.1e), ref=wall"%(
        cm,dd,rh,Lc,sm,V[iM]));P("="*80)
    P("  %-7s %-9s %-10s %-9s %s"%("w","phi","tau(M)","tau/2L","note"))
    for i in range(0,len(ws),3):
        n=""
        if abs(ws[i]-.3737)<.012:n="<- GR QNM Re"
        if abs(ws[i]-np.sqrt(6*np.exp(-2)))<.012:n="<- sqrt(Vmax)"
        P("  %-7.3f %-9.3f %-10.3f %-9.2f %s"%(ws[i],ph[i],tau[i],tau[i]/(2*Lc),n))
    pk_t=np.nanmax(np.abs(tau));iw=int(np.nanargmax(np.abs(tau)))
    P("  max|tau|=%.2f M at %.3f (tau/2L=%.2f); toy shows tall peaks at modes -> flat here = no cavity mode"%(
        pk_t,ws[iw],pk_t/(2*Lc)))
    return ws,ph,tau
for cm,dd in [(-0.5,0.0),(-0.29,-0.05)]: tuft_run(cm,dd)
P("\nDone.")
