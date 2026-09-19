# -*- coding: utf-8 -*-
# =============================================================================
# MainAgent v17 INDEPENDENT audit of coalition E391-E400 odd-parity potential
# -----------------------------------------------------------------------------
# SUSPECTED FLAW in tuft_v17_odd_potential.py:
#   TUFT metric is given in ISOTROPIC coordinate rho:
#       ds^2 = -A(rho) dt^2 + B(rho)( d rho^2 + rho^2 dOmega^2 )
#   but the coalition builds the RW odd potential as if rho were the
#   AREAL radius:  e^{-2lambda}=1/B,  V=3A/rho^2 (1+1/B).
#   The Regge-Wheeler equation needs the AREAL radius R = rho sqrt(B).
#
# STRICT areal-radius pipeline (this script):
#   R(rho)   = rho sqrt(B)
#   J=dR/drho= sqrt(B)*(1 + rho B'/2B)
#   g_RR     = B/J^2  ->  e^{-2lambda} = J^2/B = (1 + rho B'/2B)^2
#   e^{2nu}  = A
#   V_odd(R) = A [ l(l+1)/R^2 - 6 m(R)/R^3 ],  m/R = (1/2)(1-e^{-2lambda})
#            = 3 A (1 + e^{-2lambda}) / R^2         (l=2)
#   dR*/dR   = sqrt(g_RR/A);  equivalently dR*/drho = sqrt(B/A)
#
# REAL GR GATE: exact Schwarzschild isotropic metric
#   x=1/(2rho), A=((1-x)/(1+x))^2, B=(1+x)^4, R=rho(1+x)^2
#   MUST reproduce RW V=(1-2/R)[6/R^2-6/R^3]:
#   barrier top Vmax=4/27=0.148148 , sqrt=0.384900 , at R=3.
#   (the coalition "gate" 0.685 is NOT a GR value; GR is 0.3849)
# =============================================================================
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import trapezoid
import os, time

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "_ma_v17_odd_areal_out.txt"), "w",
           encoding="utf-8")
def log(s=""):
    print(s); OUT.write(s+"\n"); OUT.flush()

# -----------------------------------------------------------------------------
# 1. REAL GR GATE: exact Schwarzschild in isotropic coordinates
# -----------------------------------------------------------------------------
def gr_AB(rho):
    x = 1.0/(2.0*rho)
    A = ((1.0-x)/(1.0+x))**2
    B = (1.0+x)**4
    return A, B

def areal_quantities(ABfunc, rho, *par):
    """Return R, e^{-2lambda}, A from isotropic (A,B), complex-step dR/drho."""
    h = 1e-12
    def R_of(q):
        A, B = ABfunc(q, *par)
        return q*np.sqrt(B)
    R  = R_of(rho)
    J  = np.imag(R_of(rho+1j*h))/h          # dR/drho, complex-step (exact-ish)
    A, B = ABfunc(rho, *par)
    e2mlambda = (J/np.sqrt(B))**2           # = J^2/B = (1+rho B'/2B)^2
    return R, e2mlambda, A, J, B

def Vodd_strict(ABfunc, rho, *par):
    R, e2ml, A, J, B = areal_quantities(ABfunc, rho, *par)
    return 3.0*A*(1.0+e2ml)/R**2, R, e2ml, A, J, B

def Vodd_wrong(ABfunc, rho, *par):
    """Coalition convention: isotropic r used as areal, e^-2lambda=1/B."""
    A, B = ABfunc(rho, *par)
    return 3.0*A*(1.0+1.0/B)/rho**2

log("="*80)
log("MainAgent v17 independent audit : strict AREAL-radius odd potential")
log("="*80)

# GR gate on a fine rho grid (exterior branch rho>0.5 i.e. R>2)
rho_g = np.linspace(0.5001, 200.0, 400001)
R_g, em2l_g, A_g, J_g, B_g = areal_quantities(gr_AB, rho_g)
V_g = 3.0*A_g*(1.0+em2l_g)/R_g**2
ext = J_g > 0
V_RW_exact = (1.0-2.0/R_g[ext])*(6.0/R_g[ext]**2 - 6.0/R_g[ext]**3)
im = np.argmax(V_g[ext]); R_ext = R_g[ext]
log("\n[REAL GR GATE] exact Schwarzschild isotropic -> areal pipeline")
log("  strict V  barrier: R_peak=%.6f  Vmax=%.8f  sqrt=%.8f"
    % (R_ext[im], V_g[ext][im], np.sqrt(V_g[ext][im])))
log("  RW closed-form   : R=3.000000  Vmax=4/27=%.8f  sqrt=%.8f"
    % (4.0/27.0, np.sqrt(4.0/27.0)))
log("  max |V_strict - V_RW|/V_RW over exterior = %.3e"
    % np.max(np.abs(V_g[ext]-V_RW_exact)/np.maximum(V_RW_exact,1e-30)))
gate_ok = abs(R_ext[im]-3.0)<2e-3 and abs(np.sqrt(V_g[ext][im])-np.sqrt(4/27))<2e-4
log("  -> STRICT GR GATE: %s" % ("PASS" if gate_ok else "FAIL"))

# show the coalition-style pipeline applied to GR (what 0.685-style gives)
Vw_g = Vodd_wrong(gr_AB, rho_g)
imw = np.argmax(Vw_g[ext])
log("  [control] coalition-style (isotropic r, 1/B) on GR: sqrt(Vmax)=%.6f at rho=%.4f"
    % (np.sqrt(Vw_g[ext][imw]), rho_g[ext][imw]))
log("            (demonstrates that convention is NOT the RW barrier)")

# -----------------------------------------------------------------------------
# 2. TUFT isotropic metric, strict areal pipeline
# -----------------------------------------------------------------------------
def tuft_AB(rho, cm, d):
    F = 1.0 + cm/rho**2 + d/rho**3
    A = np.exp(-2.0/rho)
    B = np.exp(2.0/rho)*F
    return A, B

def wall_radius(cm, d):
    if abs(cm) < 1e-13 and abs(d) < 1e-13: return None
    return brentq(lambda r: 1.0+cm/r**2+d/r**3, 1e-3, 5.0, xtol=1e-14)

def neck_radius(cm, d):
    # J=0  <=>  H=1+rho B'/2B = 0 ; analytic: H=1 + rho F'/(2F) - 1/rho
    def F(q):  return 1.0+cm/q**2+d/q**3
    def Fp(q): return -2.0*cm/q**3 - 3.0*d/q**4
    def H(q):  return 1.0 + q*Fp(q)/(2.0*F(q)) - 1.0/q
    # bracket outside the wall
    lo = (wall_radius(cm,d) or 0.5)*1.001
    # scan to find sign change
    qs = np.linspace(lo, 5.0, 200000)
    Hs = np.array([H(q) if F(q)>0 else np.nan for q in qs])
    good = np.isfinite(Hs)
    qs, Hs = qs[good], Hs[good]
    s = np.sign(Hs)
    idx = np.where(s[1:]*s[:-1] < 0)[0]
    if len(idx)==0: return None
    return brentq(H, qs[idx[0]], qs[idx[0]+1], xtol=1e-13)

cases = [(0.0,0.0,"c_m=0,d=0"),(-0.5,0.0,"c_m=-0.5,d=0"),
         (-0.29,-0.05,"c_m=-0.29,d=-0.05")]

log("\n"+"="*80)
log("[TUFT] strict areal-radius barrier  vs  coalition isotropic/1-B result")
log("="*80)
hdr = "  %-18s %8s %8s | %-26s | %-26s" % (
    "case","r_wall","R_neck","STRICT areal (R_peak,Vmax,sqrt)","COALITION 1/B (rho,Vmax,sqrt)")
log(hdr); log("  "+"-"*100)

results={}
for cm,d,tag in cases:
    rw = wall_radius(cm,d)
    rk = neck_radius(cm,d)
    # exterior areal branch: rho from just outside neck outward
    rho_lo = (rk*1.0005) if rk else 1.0005
    rho = np.linspace(rho_lo, 300.0, 600001)
    R, em2l, A, J, B = areal_quantities(tuft_AB, rho, cm, d)
    V = 3.0*A*(1.0+em2l)/R**2
    ok = (J>0)&(R>0)&np.isfinite(V)
    R,V,rho2,em2l,A2 = R[ok],V[ok],rho[ok],em2l[ok],A[ok]
    k = np.argmax(V)
    Rp,Vp,sp = R[k],V[k],np.sqrt(V[k])
    # coalition wrong
    Vw = Vodd_wrong(tuft_AB, rho2, cm, d)
    kw = np.argmax(Vw)
    rw_pk, Vwp, swp = rho2[kw], Vw[kw], np.sqrt(Vw[kw])
    results[tag]=dict(rw=rw,rk=rk,Rp=Rp,Vp=Vp,sp=sp,
                      R=R,V=V,em2l=em2l,A=A2,rho=rho2,
                      rw_pk=rw_pk,Vwp=Vwp,swp=swp)
    log("  %-18s %8s %8s | R=%9.4f V=%.6f sqrt=%.6f | rho=%9.4f V=%.6f sqrt=%.6f"
        % (tag,
           ("%.4f"%rw) if rw else "none",
           ("%.4f"%rk) if rk else "none",
           Rp,Vp,sp, rw_pk,Vwp,swp))

# -----------------------------------------------------------------------------
# 3. behaviour at wall / neck (areal picture)
# -----------------------------------------------------------------------------
log("\n"+"="*80)
log("[WALL / NECK diagnostics] areal radius R(rho) and e^-2lambda")
log("="*80)
for cm,d,tag in cases:
    rw = wall_radius(cm,d); rk = neck_radius(cm,d)
    log("\n  %s:" % tag)
    if rw:
        probe = rw*(1+np.array([1e-6,1e-5,1e-4,1e-3,1e-2]))
        for q in probe:
            R,em2l,A,J,B = areal_quantities(tuft_AB, q, cm, d)
            V=3*A*(1+em2l)/R**2
            log("    near WALL rho=%.6f : R=%.6f e^-2l=%.3e A=%.5f V=%.4g J=%.3e"
                % (q,R,em2l,A,V,J))
    if rk:
        probe = rk*(1+np.array([-0.01,-0.001,0.0,0.001,0.01]))
        for q in probe:
            if q<=0: continue
            R,em2l,A,J,B = areal_quantities(tuft_AB, q, cm, d)
            V=3*A*(1+em2l)/R**2
            log("    near NECK rho=%.6f : R=%.6f e^-2l=%.4f A=%.5f V=%.4g J=%.3e"
                % (q,R,em2l,A,V,J))

# -----------------------------------------------------------------------------
# 4. tortoise connectivity through the neck (is wall reachable from infinity?)
# -----------------------------------------------------------------------------
log("\n"+"="*80)
log("[TORTOISE] dR*/drho=sqrt(B/A); does r* diverge at neck (horizon-like)?")
log("="*80)
for cm,d,tag in cases:
    rk = neck_radius(cm,d)
    if not rk:
        log("  %s: no finite neck (c=0 throat at rho=1)."%tag)
        rk=1.0
    # integrate r* from far in toward neck, inspect slope growth
    rho = np.linspace(rk*1.0001, rk*3.0, 20000)
    A,B = tuft_AB(rho, cm, d)
    deriv = np.sqrt(np.maximum(B/A,0))
    rs = np.concatenate([[0],np.cumsum(0.5*(deriv[1:]+deriv[:-1])*np.diff(rho))])
    log("  %s: neck rho_n=%.5f ; sqrt(B/A) at (1.001,1.01,1.1)rho_n = %s"
        % (tag,rk,
           ["%.3g"%np.sqrt(np.maximum(tuft_AB(q,cm,d)[1]/tuft_AB(q,cm,d)[0],0))
            for q in [rk*1.001,rk*1.01,rk*1.1]]))

log("\n"+"="*80)
log("SUMMARY")
log("="*80)
log("  REAL GR barrier sqrt(Vmax)=0.38490 @R=3 (Schwarzschild RW 4/27).")
log("  Coalition 'gate' 0.685 uses isotropic r as areal radius AND e^-2l=1/B;")
log("  it is a coordinate-convention artifact, not the GR limit.")
for tag in ["c_m=0,d=0","c_m=-0.5,d=0","c_m=-0.29,d=-0.05"]:
    r=results[tag]
    log("  %-16s STRICT sqrt(Vmax)=%.4f @R=%.4f | coalition 1/B sqrt=%.4f"
        % (tag,r["sp"],r["Rp"],r["swp"]))
log("\nEND (%.1f s)"%(time.time()-t0))
OUT.close()
print("[written]", os.path.join(HERE,"_ma_v17_odd_areal_out.txt"))
