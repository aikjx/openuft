# -*- coding: utf-8 -*-
# =============================================================================
# MainAgent v18 independent re-run / audit of coalition E407-E414
# Checks:
#  (1) GR RW |R|^2 at w=0.37367 (coalition says 0.531; E386 curve implies lower)
#  (2) TUFT strict-areal reflection IVP: |R|^2=1, and GROUP DELAY computed both
#      raw argR and phase-shifted to the CORE phi=argR-2 w s_out ; coalition
#      differentiated raw argR (suspect: should carry a 2 s_out constant).
#  (3) echo separation ratio 2L/tau_d (mass-independent) + mass convention.
# =============================================================================
import numpy as np
from scipy.integrate import solve_ivp, trapezoid
from scipy.optimize import brentq
import os, time
t0=time.time()
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=open(os.path.join(HERE,"_ma_v18_realfreq_out.txt"),"w",encoding="utf-8")
def log(s=""): print(s);OUT.write(str(s)+"\n");OUT.flush()

cm,dd=-0.29,-0.05

# ---------- TUFT strict areal potential on tortoise s ----------
rho_h=brentq(lambda r: r**3+cm*r+dd,1e-3,5,xtol=1e-14)
rho=np.linspace(rho_h*1.0008,250.0,900001)
A=np.exp(-2/rho); F=1+cm/rho**2+dd/rho**3; B=np.exp(2/rho)*F
q=-2/rho**2+(-2*cm/rho**3-3*dd/rho**4)/F
J=np.sqrt(B)*(1+0.5*rho*q)
R=rho*np.sqrt(B); em2=(J/np.sqrt(B))**2
V=3*A*(1+em2)/R**2
drs=np.sqrt(B/A)
s=np.concatenate([[0],np.cumsum(0.5*(drs[1:]+drs[:-1])*np.diff(rho))])
# OUTER barrier peak (exclude core R<2.5)
iout=np.where(R>2.5)[0]; ipk=iout[np.argmax(V[iout])]
L=s[ipk]                       # wall(s=0)->outer peak
log("TUFT c=-.29: rho_h=%.5f outer peak R=%.4f Vmax=%.6f sqrt=%.5f"%(
    rho_h,R[ipk],V[ipk],np.sqrt(V[ipk])))
log("wall->peak tortoise L=%.4f M ; echo free round trip 2L=%.4f M"%(L,2*L))
def VT(x): return np.interp(x,s,V)

# ---------- generic IVP reflection ----------
def reflect(geom, s0,s1,y0,w,Vf,rtol=1e-10):
    def rhs(xx,y):
        return [y[1],-(w*w-Vf(xx))*y[0]]
    sol=solve_ivp(rhs,(s0,s1),y0,method="DOP853",rtol=rtol,atol=1e-12,max_step=1.0)
    psi,dp=sol.y[0,-1],sol.y[1,-1]
    a=(psi-dp/(1j*w))/2      # ingoing e^{-iws}
    b=(psi+dp/(1j*w))/2      # outgoing e^{+iws}
    return a,b,b/a

# ---------- (1) GR RW gate ----------
Rg=np.linspace(2.0005,400.0,800001)
rs=Rg+2*np.log((Rg-2)/2); Vg=(1-2/Rg)*(6/Rg**2-6/Rg**3)
def VGR(x): return np.interp(x,rs,Vg)
log("\n[GR gate] Schwarzschild RW l=2, horizon ingoing launch s_in=-120 -> 150")
log("  omega   |R_GR|^2   unitarity|a|2-|b|2")
gr={}
for w in [0.30,0.35,0.37367,0.40,0.45,0.50,0.60,0.90]:
    psi0=np.exp(-1j*w*(-120)); a,b,rR=reflect("gr",-120,150,[psi0,-1j*w*psi0],w,VGR)
    gr[w]=abs(rR)**2
    log("  %.4f  %.5f   %.6f"%(w,abs(rR)**2,abs(a)**2-abs(b)**2))
log("  coalition E407 reported |R_GR|^2@0.374=0.531 ; E386 curve .30=.944/.40=.305")

# ---------- (2) TUFT reflection, DENSE frequency, both phase conventions ---
s_out=160.0
ws=np.round(np.arange(0.30,0.7001,0.01),3)
ws=np.sort(np.unique(np.concatenate([ws,np.round(np.arange(0.35,0.4501,0.0025),4)])))
R2=[];argraw=[]
for w in ws:
    a,b,rR=reflect("t",0,s_out,[1+0j,0j],w,VT)
    R2.append(abs(rR)**2); argraw.append(np.angle(rR))
R2=np.array(R2); argraw=np.array(argraw)
phi_core=np.unwrap(argraw)-2*ws*s_out      # shift reference plane to core s=0
phi_raw =np.unwrap(argraw)
tau_core=np.gradient(phi_core,ws)
tau_raw =np.gradient(phi_raw ,ws)
log("\n[TUFT] |R|^2 max dev = %.3e (expect 0)"%np.max(np.abs(R2-1)))
log("  group delay statistics (M):")
for name,tt in [("RAW argR (coalition convention)",tau_raw),
                ("CORE-shifted phi=argR-2ws_out  ",tau_core)]:
    band=(ws>=0.50)&(ws<=0.70); bandm=(ws>=0.35)&(ws<=0.50)
    log("  %s : mean tau(.50-.70)=%.2f  mean tau(.35-.50)=%.2f  range[%.1f,%.1f]"%(
        name,tt[band].mean(),tt[bandm].mean(),tt.min(),tt.max()))
log("  free round trip 2L=%.2f M  (above-barrier tau should approach this)"%(2*L))
# sample rows
log("\n  omega   |R|^2      phi_core(rad)  tau_core(M)")
for i in range(0,len(ws),4):
    log("  %.4f  %.6f  %+10.4f  %+9.2f"%(ws[i],R2[i],phi_core[i],tau_core[i]))

# ---------- (3) separation ratio + mass convention ----------
GMu=4.9256e-6
log("\n[echo separation] mass-INDEPENDENT ratio")
tau_d_geom=1/0.088962        # ringdown e-fold in M
Dt=2*L
log("  2L=%.3f M , ringdown e-fold tau_d=1/|w_i|=%.3f M , Dt/tau_d=%.3f"%(
    Dt,tau_d_geom,Dt/tau_d_geom))
log("  ringdown amplitude at echo return = exp(-Dt/tau_d)=%.3f"%np.exp(-Dt/tau_d_geom))
for Mf in [30.0,60.0]:
    Mt=GMu*Mf
    log("  M_final=%.0f Msun: f0=%.0f Hz, tau_d=%.2f ms, 2L=%.2f ms (ratio fixed %.2f)"%(
        Mf,0.37367/(2*np.pi*Mt),Mt/0.088962*1e3,Dt*Mt*1e3,Dt/tau_d_geom))
log("  note: 30+30 merger leaves remnant M_f~57-60 Msun (v18 used 30); ratio unaffected")
log("\nEND(%.1fs)"%(time.time()-t0));OUT.close()
print("[written]")
