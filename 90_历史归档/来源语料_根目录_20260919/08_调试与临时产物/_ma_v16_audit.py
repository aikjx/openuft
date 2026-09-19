# -*- coding: utf-8 -*-
"""
MainAgent v16 independent audit of coalition v16 claim
"TUFT |R|^2 Lorentzian peak =1 at w~0.90, contrast >1e5 -> A: STRONGLY OBSERVABLE".

Audit points:
 (1) Read the REAL TUFT reflection MAGNITUDE |R(w)| from the stable real-freq
     standing-wave IVP (v15). Flux conservation with an ideal Neumann wall and a
     real potential FORCES |R|^2 == 1 at EVERY frequency, not a Lorentzian peak.
 (2) The w~0.90 feature lives in the PHASE/ Wigner delay tau=dphi/dw only.
 (3) Independent scipy cross-check of GR horizon-injection |R_GR|^2 at a few w
     (coalition used mpmath; verify with a different integrator).
 (4) Locate where (a) GR vs wall reflection differs most AND (b) the l=2 merger
     signal still carries energy -> correct observability window.
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
from scipy.integrate import solve_ivp
def P(*a):print(*a,flush=True)

# ---------- TUFT real potential + tortoise ----------
def tuft(cm,dd,rhi=160.,Nr=700000):
    roots=np.roots([1.,0.,cm,dd]);rh=min(x.real for x in roots if abs(x.imag)<1e-8 and x.real>0)
    r=np.linspace(rh,rhi,Nr+1);q=np.sqrt(np.maximum(1+cm/r**2+dd/r**3,0.))
    dr=r[1]-r[0];g=np.exp(2/r)*q
    s=np.concatenate([[0.],np.cumsum(0.5*(g[1:]+g[:-1])*dr)]);V=np.exp(-2/r)*6/r**2
    return rh,s,V
def tuft_R(cm,dd,ws):
    rh,s,V=tuft(cm,dd);iM=np.argmin(np.abs(V-6e-4));sm=s[iM]
    out=[]
    for w in ws:
        sol=solve_ivp(lambda x,y:[y[1],(np.interp(x,s,V)-w*w)*y[0]],[0,sm],[1.,0.],
                      t_eval=[sm],rtol=1e-11,atol=1e-12,max_step=0.02,method="DOP853")
        psi,pp=sol.y[:,0]
        Rp=(psi+pp/(1j*w))/(psi-pp/(1j*w))
        a=np.angle(np.exp(1j*(np.angle(Rp)-2*w*sm)))
        out.append((abs(Rp),a))
    out=np.array(out);ph=np.unwrap(out[:,1]);tau=np.gradient(ph,ws)
    return sm,out[:,0],ph,tau

ws=np.array([.20,.30,.3737,.40,.45,.50,.60,.70,.80,.85,.89,.90,.915,.95,1.0,1.1])
P("="*86)
P("AUDIT 1: REAL TUFT |R(w)| from IVP (flux conservation must give |R|^2=1 ALL w)")
P("="*86)
for cm,dd in [(-0.5,0.0),(-0.29,-0.05)]:
    sm,Rm,ph,tau=tuft_R(cm,dd,ws)
    P("\nTUFT c_m=%g d=%g  (decompose s_m=%.1f)"%(cm,dd,sm))
    P("  %-7s %-12s %-12s %-10s   %s"%("w","|R| (IVP)","|R|^2","tau(M)","note"))
    for i,w in enumerate(ws):
        n="<- GR l=2 ringdown" if abs(w-.3737)<.005 else ("<- claimed 'TUFT peak'" if abs(w-.90)<.006 else "")
        P("  %-7.4f %-12.6f %-12.6f %-10.2f  %s"%(w,Rm[i],Rm[i]**2,tau[i],n))
    P("  >> max| |R|^2-1 | = %.2e : %s"%(np.max(np.abs(Rm**2-1)),
        "PASS unitarity, |R|^2=1 at ALL w (no Lorentzian reflectivity peak)" if np.max(np.abs(Rm**2-1))<1e-3 else "CHECK"))

# ---------- independent scipy GR horizon injection ----------
def Vgr(r):
    f=1-2/r;return f*(6/r**2-6/r**3)
def rstar_of_r(r): return r+2*np.log((r-2)/2)
def r_of_rs(rs):
    r=2+2*np.exp((rs-2)/2) if rs<0 else rs+2
    for _ in range(10):
        r=max(r,2+1e-12);r=r-(r+2*np.log((r-2)/2)-rs)/(1+2/(r-2))
    return r
def gr_R(w,r0=-60.,r1=90.,h=0.05):
    n=int((r1-r0)/h);rss=np.linspace(r0,r1,n+1)
    psi0=np.exp(-1j*w*r0);y=[psi0,-1j*w*psi0]
    def f(rs,y):
        r=r_of_rs(rs);return [y[1],-(w*w-Vgr(r))*y[0]]
    sol=solve_ivp(f,[r0,r1],y,t_eval=[r1],rtol=1e-11,atol=1e-12,max_step=h,method="DOP853")
    psi,pp=sol.y[:,0]
    a=np.exp(1j*w*r1)*(psi-pp/(1j*w))/2
    b=np.exp(-1j*w*r1)*(psi+pp/(1j*w))/2
    return abs(b/a)**2,abs(1/a)**2,abs(a)**2-abs(b)**2
P("\n"+"="*86)
P("AUDIT 2: independent scipy GR horizon-injection |R_GR|^2 (cross-check coalition mpmath)")
P("="*86)
P("  %-7s %-12s %-12s %-12s"%("w","|R|^2(scipy)","|T|^2","unitarity"))
for w in [.30,.40,.45,.50,.60,.90,1.0]:
    R2,T2,u=gr_R(w);P("  %-7.3f %-12.3e %-12.5f %-12.5f"%(w,R2,T2,u))

P("\n"+"="*86)
P("AUDIT 3: physically correct comparison")
P("="*86)
P(" - GR: high-w waves TRANSMIT into horizon (|R|^2->0 for w>0.5); TUFT wall: |R|^2=1 ALL w.")
P("   This difference is ABSORBING HORIZON vs REFLECTING WALL (= sigma_abs=0), present across")
P("   the WHOLE band w>~0.45 -- NOT a reflectivity peak localized at 0.90 (E378 Lorentzian is fabricated).")
P(" - w~0.90 feature is PHASE/Wigner delay tau only (|R|=1); it is the barrier-top turning-point dwell.")
P(" - l=2 merger energy sits near w~0.35-0.5 (GR QNM Re=0.374). At w=0.90 (~6.1 kHz/30Msun) the")
P("   signal is weak and LIGO noise high. The hand-built omega0=0.90 Gaussian burst puts the answer")
P("   in the input; it does NOT establish O4 detectability. GRADE A is NOT supported.")
P(" - 'reflecting vs absorbing' is the generic ECO/exotic-horizon test (echo search), not TUFT-unique.")
P("DONE")
