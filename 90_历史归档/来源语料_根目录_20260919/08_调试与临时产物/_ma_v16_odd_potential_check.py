# -*- coding: utf-8 -*-
"""
Audit of the TUFT 'gravitational s=-2 barrier' V_old=e^{-2/r} l(l+1)/r^2.
In areal-radius coordinates ds^2=e^{2nu}dt^2-e^{2lambda}dr^2-r^2 dO^2, the
Chandrasekhar axial (odd) potential carries a spin term that is -6M/r^3 in
Schwarzschild; the standard general-metric replacement is M -> M_eff(r) with
e^{-2lambda}=1-2 M_eff/r. The TUFT work to date DROPPED that spin term.
This quantifies the barrier shift (leading-term estimate only; a metric with a
scalar source needs the full odd-perturbation derivation -- flagged, not claimed
exact here).
"""
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import numpy as np
def P(*a):print(*a,flush=True)
r=np.linspace(0.55,60,2_000_001)
def barriers(cm,dd,tag):
    B=np.exp(2/r)*(1+cm/r**2+dd/r**3)
    e2nu=np.exp(-2/r)
    em2lam=1/B
    M_eff=0.5*r*(1-em2lam)
    Vold=e2nu*6/r**2
    Vnew=e2nu*(6/r**2-6*M_eff/r**3)
    def peak(V):
        i=np.argmax(V);return r[i],V[i],np.sqrt(max(V[i],0))
    ro,vo,so=peak(Vold);rn,vn,sn=peak(Vnew)
    P("%-22s OLD V=e^-2/r 6/r^2 : r_pk=%.3f Vmax=%.4f sqrt=%.4f"%(tag,ro,vo,so))
    P("%-22s corrected odd    : r_pk=%.3f vmax=%.4f sqrt=%.4f   (Vmax x%.3f, sqrt x%.3f)"%(
        "",rn,vn,sn,vn/vo,sn/so))
    P("")
P("l=2. OLD = centrifugal-only (used in v15/coalition). NEW = with -6 M_eff/r^3 spin term.")
P("Schwarzschild reference: V=f(6/r^2-6/r^3), Vmax=4/27=0.1481, sqrt=0.3849, r_pk=3.")
P("="*84)
barriers(0.0,0.0,"TUFT c=0 (pure Yilmaz)")
barriers(-0.5,0.0,"TUFT c=-0.5")
barriers(-0.29,-0.05,"TUFT c=-0.29")
P("Implication: the 'barrier top sqrt(Vmax)=0.90' / wide delay-arch centre 0.89-0.915")
P("used by v15 E368 and coalition v16 is computed WITHOUT the s=-2 spin term.")
P("Including the leading spin term moves sqrt(Vmax) down to ~0.65-0.75 and shifts the")
P("peak outward. Exact value needs the full odd-parity perturbation on the TUFT metric")
P("(scalar-source contributions included) -> must be derived, not assumed.")
P("Robust regardless: |R|^2=1 (wall, flux); NO high-Q cavity line (smooth wall+barrier).")
