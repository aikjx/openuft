# -*- coding: utf-8 -*-
"""
MainAgent independent verification of organizer v5.6 E496 (A6 U_ph x 2PN coupling)
Claims to verify:
 1) deflection integral  dphi = 2*int_0^u0 sqrt(1+c_m u^2+d u^3)/sqrt(u0^2 e^{-2u0}-u^2 e^{-2u}) du - pi
    with U_ph(u)=u e^{-u} coordinate map (strict theorem)
 2) GR limit c_m=d=0: A1(1PN)=4.000000000090184 (~10.6 digits)
 3) analytic 2PN coefficient A2(c_m,d)=3.0688962660+0.7855625673 c_m+0.0001000236 d
 4) c_m=-0.29, d=-0.05: modulation = -0.211646 microarcsec (NEGATIVE detectability)
Independent implementation: own Gauss-Legendre quadrature, no import of organizer scripts.
"""
import numpy as np
from scipy.integrate import quad

# ---- exact integrand as given in v5.6 (independent re-implementation) ----
def delta_phi(u0, c_m, d, n=2000):
    # integrand of 2*int_0^u0 ... minus pi
    def f(u):
        num = np.sqrt(1.0 + c_m*u*u + d*u*u*u)
        den = np.sqrt(u0*u0*np.exp(-2.0*u0) - u*u*np.exp(-2.0*u))
        return num/den
    # Gauss-Legendre on [0,u0]
    x, w = np.polynomial.legendre.leggauss(n)
    t = 0.5*u0*(x+1.0)
    val = 0.5*u0*np.sum(w*f(t))
    return 2.0*val - np.pi

# ---- 1) GR limit: c_m=d=0, small u0, extract 1PN coefficient A1=dphi/u0 ----
for u0 in [2e-4, 1e-4, 5e-5]:
    dph = delta_phi(u0, 0.0, 0.0)
    A1 = dph/u0
    print(f"GR limit u0={u0:.1e}: dphi={dph:.12f}  A1=dphi/u0={A1:.12f}  dev from 4={A1-4.0:.3e}")

# ---- 2) c_m scan at solar-grazing u0 (v5.6 claim: modulation ~ -0.2116 muas) ----
u0_sun = 2.12250257079201e-6
c_list = [-0.369, -0.331, -0.290, -0.249, -0.218]
print("\nSun-grazing u0=%.6e, d=-0.05" % u0_sun)
base = delta_phi(u0_sun, 0.0, -0.05)   # c_m=0 baseline
# 1PN dominant = 4*u0 (arcsec->?)  actually dphi(GR) = 2*4*... check: Schwarzschild deflection=4M/b=4u0
dphi_gr = delta_phi(u0_sun, 0.0, 0.0)
print("  GR-limit dphi(1PN expected 4*u0=%.12e): %.12e ratio=%.12f" % (4*u0_sun, dphi_gr, dphi_gr/(4*u0_sun)))
muas = 2.062648e+11  # rad -> microarcsec
print("  d=-0.05 baseline(c_m=0) 2PN-part = dphi(base) - dphi_gr = %.6e rad" % (base-dphi_gr))
for cm in c_list:
    dp = delta_phi(u0_sun, cm, -0.05)
    mod = (dp - base)*muas
    print(f"  c_m={cm:+.3f}: dphi={dp:.15e}  modulation={mod:+.4f} muas")
# nominal c_m=-0.29
dp_nom = delta_phi(u0_sun, -0.29, -0.05)
mod_nom = (dp_nom-base)*muas
print("  NOMINAL c_m=-0.29: modulation=%.6f muas (claim -0.211646)" % mod_nom)
print("  claimed: 2PN mod = -1.02609069724872e-12 rad = -0.211646 muas")
mod_rad = dp_nom-base
print("  my rad value:", mod_rad, " ratio to claim:", mod_rad/(-1.02609069724872e-12))

# ---- 3) analytic A2 fit (c_m scan at fixed small u0 -> dphi = pi + A1*u0 + A2*u0^2 ...) ----
print("\nA2 extraction at u0=1e-4 (quad high precision):")
def dphi_hi(u0, c_m, d, n=4000):
    return delta_phi(u0, c_m, d, n=n)
u0s = np.array([0.5e-4, 0.75e-4, 1.0e-4, 1.25e-4, 1.5e-4])
# baseline c=0,d=0: fit A2
vals = np.array([dphi_hi(u,0.0,0.0) for u in u0s])
# dphi = pi + 4u + A2 u^2 + A3 u^3
A = np.vstack([np.ones_like(u0s), u0s, u0s**2, u0s**3])
coef, *_ = np.linalg.lstsq(A, vals - np.pi, rcond=None)
print("  GR-limit fit: A1=%.10f (expect 4) A2=%.10f (organizer scan 3.068582494365693) A3=%.10f" % (coef[1], coef[2], coef[3]))
# c_m dependence: A2(c_m) - A2(0) at d=-0.05 fixed small u0
def A2_of_cm(cm):
    vals2 = np.array([dphi_hi(u,cm,-0.05) for u in u0s])
    A = np.vstack([np.ones_like(u0s), u0s, u0s**2, u0s**3])
    c2, *_ = np.linalg.lstsq(A, vals2 - np.pi, rcond=None)
    return c2[2]
cm_scan = np.array([-0.369,-0.331,-0.290,-0.249,-0.218,0.0])
A2s = np.array([A2_of_cm(c) for c in cm_scan])
# linear fit A2 = A2_0 + k*cm  (drop cm=0 for slope? include all, d fixed -0.05)
k_fit, A2_0 = np.polyfit(cm_scan, A2s, 1)
print("  A2(c_m,d=-0.05): A2_0=%.10f k=%.10f" % (A2_0, k_fit))
print("  organizer analytic: A2=3.0688962660+0.7855625673*c_m+0.0001000236*d")
print("  -> at d=-0.05: A2_0_exp=3.0688962660-0.0000050012=3.0688912648 k_exp=0.7855625673")
print("  my A2_0 vs exp: %.6e ; my k vs exp: %.6e" % (A2_0-3.0688912648, k_fit-0.7855625673))
