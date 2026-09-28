# -*- coding: utf-8 -*-
"""
MainAgent A6 2PN verification v2: theta-substitution to remove endpoint singularity.
u = u0 sin(theta); du = u0 cos(th) dth.
f_th = e^{u0} cos(th) * sqrt(1 + c_m u0^2 sin^2 + d u0^3 sin^3) / sqrt(1 - sin^2(th) e^{2 u0 (1 - sin th)})
dphi = 2*int_0^{pi/2} f_th dth - pi
Endpoint th->pi/2 is a removable 0/0 (finite limit), Gauss-Legendre open nodes avoid it.
"""
import numpy as np

def dphi(u0, c_m, d, n=4000):
    x, w = np.polynomial.legendre.leggauss(n)
    th = 0.25*np.pi*(x+1.0)              # map [-1,1] -> [0, pi/2]
    s = np.sin(th); c = np.cos(th)
    num = np.sqrt(1.0 + c_m*u0*u0*s*s + d*u0**3*s**3)
    den = np.sqrt(1.0 - s*s*np.exp(2.0*u0*(1.0-s)))
    f = np.exp(u0)*c*num/den
    val = 0.25*np.pi*np.sum(w*f)
    return 2.0*val - np.pi

print("== 1) GR limit A1 = dphi/u0 = 4 ==")
for u0 in [2e-3, 5e-4, 2e-4, 1e-4, 5e-5, 2e-5]:
    dp = dphi(u0,0.0,0.0)
    print(f"  u0={u0:.1e}: dphi={dp:.13e} A1={dp/u0:.12f} dev={dp/u0-4:.2e}")

print("\n== 2) sun-grazing c_m scan (u0=2.12250257079201e-6, d=-0.05) ==")
u0s = 2.12250257079201e-6
base = dphi(u0s,0.0,-0.05)
dp_gr = dphi(u0s,0.0,0.0)
muas = 2.062648e+11
print(f"  GR-limit dphi = {dp_gr:.12e} (4*u0={4*u0s:.12e}) ratio={dp_gr/(4*u0s):.10f}")
print(f"  1PN dominant = {4*u0s*muas:.6f} arcsec*muas-scale check")
for cm in [-0.369,-0.331,-0.290,-0.249,-0.218]:
    dp = dphi(u0s,cm,-0.05)
    print(f"  c_m={cm:+.3f}: mod={(dp-base)*muas:+.4f} muas")
dp_n = dphi(u0s,-0.29,-0.05)
print(f"  NOMINAL c_m=-0.29: mod rad={dp_n-base:.12e}  muas={(dp_n-base)*muas:.6f}")
print("  claim: -1.02609069724872e-12 rad, -0.211646 muas; ratio rad:", (dp_n-base)/(-1.02609069724872e-12))

print("\n== 3) A2 analytic coefficient fit ==")
def A_fit(cm, dval, n=6000):
    u0s_f = np.array([0.5e-4,0.75e-4,1.0e-4,1.25e-4,1.5e-4])
    vals = np.array([dphi(u,cm,dval,n=n) for u in u0s_f])
    A = np.vstack([np.ones_like(u0s_f),u0s_f,u0s_f**2,u0s_f**3])
    coef = np.polyfit(u0s_f, vals - np.pi, 3)  # c0+c1 u+c2 u^2+c3 u^3
    return coef[2], coef[1], coef[0]  # A1=c1, A2=c2, A3=c3 (polyfit ascending check)
a1,a2,a3 = A_fit(0.0,0.0)
print(f"  GR limit: A1={a1:.10f} A2={a2:.10f} A3={a3:.10f} (polyfit: c0=A1 order)")
print("  organizer GR scan: A2=3.068582494365693")
cm_scan = np.array([-0.369,-0.331,-0.290,-0.249,-0.218,0.0])
A2s = np.array([A_fit(c,-0.05)[1] for c in cm_scan])
k, A20 = np.polyfit(cm_scan, A2s, 1)
print(f"  A2(c_m, d=-0.05): A2_0={A20:.10f} slope={k:.10f}")
print("  organizer: A2=3.0688962660+0.7855625673*c_m+0.0001000236*d -> at d=-0.05: A2_0=3.0688912648 slope=0.7855625673")
print(f"  diff A2_0: {A20-3.0688912648:+.2e}  diff slope: {k-0.7855625673:+.2e}")
