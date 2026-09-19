# -*- coding: utf-8 -*-
"""Convergence of the TUFT barrier-top broad delay feature vs decomposition
point s_m (residual V threshold) and integrator step, c_m=-0.29 d=-0.05.
A physical feature: peak location ~sqrt(Vmax)=0.90 and height stable as s_m
moves out and step shrinks. Low-w negative tau is residual-V/grid artifact and
should shrink as s_m moves out."""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
from scipy.integrate import solve_ivp
def P(*a):print(*a,flush=True)
cm,dd=-0.29,-0.05
Nr=700000;rhi=160.
roots=np.roots([1.,0.,cm,dd]);rh=min(x.real for x in roots if abs(x.imag)<1e-8 and x.real>0)
r=np.linspace(rh,rhi,Nr+1);q=np.sqrt(np.maximum(1+cm/r**2+dd/r**3,0.))
dr=r[1]-r[0];s=np.concatenate([[0.],np.cumsum(0.5*((np.exp(2/r)*q)[1:]+(np.exp(2/r)*q)[:-1])*dr)])
V=np.exp(-2/r)*6/r**2
def sm_of_Vthr(thr): return s[np.argmin(np.abs(V-thr))], V[np.argmin(np.abs(V-thr))]
ws=np.round(np.unique(np.concatenate([np.linspace(.30,.70,17),np.linspace(.72,1.02,61),
                                     np.linspace(.10,.28,4),np.linspace(1.04,1.2,5)])),5)
def curve(sm,ms):
    ph=[]
    for w in ws:
        sol=solve_ivp(lambda x,y:[y[1],(np.interp(x,s,V)-w*w)*y[0]],[0,sm],[1.,0.],
                      t_eval=[sm],rtol=1e-11,atol=1e-12,max_step=ms,method="DOP853")
        psi,pp=sol.y[:,0];Rp=(psi+pp/(1j*w))/(psi-pp/(1j*w))
        a=np.angle(np.exp(1j*(np.angle(Rp)-2*w*sm)));ph.append(a)
    phu=np.unwrap(np.array(ph));return np.gradient(phu,ws)
P("c_m=-0.29 d=-0.05 ; sqrt(Vmax)=%.4f"%(np.sqrt(6*np.exp(-2))))
P("%-10s %-9s %-8s %-12s %-12s %-12s %-12s"%("Vthr","s_m","step","peak w","peak tau","tau@.3737","tau@.89"))
for thr,ms in [(2e-3,0.02),(6e-4,0.02),(2e-4,0.02),(2e-4,0.01)]:
    sm,vth=sm_of_Vthr(thr);tau=curve(sm,ms)
    i0=int(np.argmin(np.abs(ws-0.7)));seg=np.arange(i0,len(ws))
    ip=seg[np.argmax(tau[seg])]
    def at(w):return tau[np.argmin(np.abs(ws-w))]
    P("%-10.0e %-9.2f %-8.3f %-12.4f %-12.2f %-12.2f %-12.2f"%(
        thr,sm,ms,ws[ip],tau[ip],at(.3737),at(.89)))
P("\nFeature robust if peak w stays 0.88-0.92 and peak tau within ~15% across rows.")
