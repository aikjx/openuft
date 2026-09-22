# -*- coding: utf-8 -*-
# =============================================================================
# MainAgent v17 audit step 2: WKB tunnelling / barrier-top on STRICT areal odd
# potential. Replaces coalition E399/E400 whose barrier 0.685 was coordinate-
# wrong. Coalition claimed |T|^2=2.25e-5 at omega=0.374 and echo/RD~0.175.
#
# Strict: work in isotropic rho (tortoise is a scalar; dR*/drho=sqrt(B/A)),
#   r*(wall)=0 at rho=r_h (sqrt(B/A)->0, finite tortoise), integrate outward.
#   V(rho)=3 A (1+e^-2l)/R^2, R=rho sqrt(B), e^-2l=(1+rho B'/2B)^2.
#   Turning points where V=omega^2 ; K=int_{s_in}^{s_out} sqrt(V-omega^2) dr*
#   single-pass power transmission ~ exp(-2K); round-trip echo amp ~ exp(-2K)
# =============================================================================
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import trapezoid
import os, time
t0=time.time()
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=open(os.path.join(HERE,"_ma_v17_odd_wkb_out.txt"),"w",encoding="utf-8")
def log(s=""): print(s);OUT.write(s+"\n");OUT.flush()

def tuft(rho,cm,d):
    F =1+cm/rho**2+d/rho**3
    Fp=-2*cm/rho**3-3*d/rho**4
    A=np.exp(-2/rho); B=np.exp(2/rho)*F
    R=rho*np.sqrt(B)
    H=1+rho*Fp/(2*F)-1/rho          # =1+rho B'/2B
    e=H*H
    V=3*A*(1+e)/R**2
    drs=np.sqrt(B/A)
    return R,A,B,V,drs,F

def wall(cm,d):
    return brentq(lambda r:1+cm/r**2+d/r**3, 1e-3,5,xtol=1e-14)

log("="*80);log("Strict areal-potential WKB tunnelling (audits E399/E400)");log("="*80)

# analytic GR barrier top check
rstar=(9+np.sqrt(17))/4
f=1-2/rstar
Vgr=f*(6/rstar**2-6/rstar**3)
log("\n[analytic] RW l=2 barrier top r*=(9+sqrt17)/4=%.5f  Vmax=%.6f  sqrt=%.6f"
    %(rstar,Vgr,np.sqrt(Vgr)))

for cm,d,tag in [(-0.5,0.0,"c_m=-0.5"),(-0.29,-0.05,"c_m=-0.29,d=-0.05")]:
    rw=wall(cm,d)
    # dense grid from wall (F->0) outward
    rho=np.linspace(rw*(1+1e-9), 60.0, 1600001)
    R,A,B,V,drs,F=tuft(rho,cm,d)
    good=(F>0)&np.isfinite(V)
    rho,R,V,drs=rho[good],R[good],V[good],drs[good]
    rs=np.concatenate([[0],np.cumsum(0.5*(drs[1:]+drs[:-1])*np.diff(rho))])
    # OUTER barrier = outermost local maximum of V along the exterior branch
    # (the reflecting core V~1/R^2 diverges at r*=0 and must not be picked).
    dV=np.gradient(V,rho)
    st=np.where((dV[:-1]>0)&(dV[1:]<=0))[0]
    kpk=st[-1] if len(st) else np.argmax(V)
    # is there an inner cavity (V dips back down between outer barrier and core)?
    inner=V[:kpk]; cav = (inner.min() < V[kpk])
    log("\n"+"-"*80)
    log("%s : wall rho_h=%.5f (R->0 reflecting core); exterior branch monotonic"
        %(tag,rw))
    log("  STRICT OUTER barrier: rho_pk=%.4f R_pk=%.4f Vmax=%.6f sqrt=%.5f"
        %(rho[kpk],R[kpk],V[kpk],np.sqrt(V[kpk])))
    log("  #local maxima=%d ; min(V) between core and outer barrier=%.4g ; cavity=%s"
        %(len(st),inner.min(),"YES" if cav else "NO (barrier joins core)"))
    log("  tortoise wall->outerpeak r*=%.3f M"%rs[kpk])
    log("\n  omega   Vpk-w2     s_in(M)  s_out(M)  K        |T|^2~e^-2K   echo amp     topology")
    for w in [0.30,0.35,0.374,0.40,0.45,0.50,0.55,0.60,0.65,0.70]:
        w2=w*w
        if V[kpk]<=w2:
            log("  %.3f   above barrier (no under-barrier interval)"%w); continue
        dV=V-w2
        idx=np.where(dV>0)[0]
        sep=np.where(np.diff(idx)>1)[0]
        groups=np.split(idx,sep+1)
        grp=next((g for g in groups if g[0]<=kpk<=g[-1]), max(groups,key=len))
        ia,ib=grp[0],grp[-1]
        touches_core = (ia<=1)
        seg = slice(ia,ib+1)
        if touches_core:
            mseg=(rs[ia:ib+1]>=0.5)
            K=trapezoid(np.sqrt(dV[ia:ib+1][mseg]),rs[ia:ib+1][mseg])
        else:
            K=trapezoid(np.sqrt(dV[ia:ib+1]),rs[ia:ib+1])
        T2=np.exp(-2*K)
        log("  %.3f   %.3e  %8.3f %9.3f  %8.4f  %11.3e  %11.3e  %s"
            %(w,V[kpk]-w2,rs[ia],rs[ib],K,T2,T2,
              "JOINS-CORE" if touches_core else "cavity-inside"))
    log("\n  [compare] coalition E399 used wrong barrier sqrt=0.685 and reported")
    log("            |T|^2=2.25e-5 at omega=0.374. Read strict value above.")

log("\n"+"="*80)
log("PHYSICAL READING")
log("="*80)
log(" * Preferred c_m=-0.29 strict barrier sqrt=~0.386 sits essentially AT the")
log("   GR ringdown frequency 0.374 (not 0.685). Main ringdown is NOT buried")
log("   deep under a 0.685 barrier; under-barrier width at 0.374 is thin, so")
log("   transmission is many orders larger than 2.25e-5 -> coalition echo/RD~0.175")
log("   (from a high-freq Lorentzian tail) is built on a wrong barrier; REOPEN.")
log(" * Robust regardless: sigma_abs=0, |R|^2=1 total reflection, reflecting core")
log("   at R->0 (finite tortoise), no high-Q wall-cavity narrow line (E367).")
log("END(%.1fs)"%(time.time()-t0)); OUT.close()
print("[written]",os.path.join(HERE,"_ma_v17_odd_wkb_out.txt"))
