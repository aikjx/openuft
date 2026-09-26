# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 80

c    = mp.mpf("299792458")
G    = mp.mpf("6.67430e-11")
hbar = mp.mpf("1.0545718176461565e-34")
m_e  = mp.mpf("9.1093837015e-31")
Msun = mp.mpf("1.98847e30")
alpha_obs = mp.mpf("0.0072973525693")
arcsec_to_rad = mp.pi / (180 * 3600)

# ===== C25 =====
omega = mp.mpf("1.23558996e20")
N_topo = mp.mpf("18907")
V0    = mp.mpf("1.0")

def En(n):
    return (omega**2 / c**2) * (V0 + (n**2 * hbar**2)/(N_topo**2))
E1 = En(1)
C_couple = alpha_obs * m_e * c**2 / E1

dN_rel = mp.mpf("1e-12")
domega_rel = mp.mpf("1e-12")

print("===== C25 =====")
print("E1        =", mp.nstr(E1, 12))
print("C_couple  =", mp.nstr(C_couple, 12))
print("hbar^2/N^2=", mp.nstr(hbar**2 / N_topo**2, 6))
print("V0        =", V0)
print()
for n in range(1,7):
    En_val = En(n)
    alphan = C_couple * En_val / (m_e * c**2)
    term_n = (n**2 * hbar**2) / (N_topo**2)
    rel_err = mp.sqrt( domega_rel**2 + ( (2*term_n)/(V0 + term_n) * dN_rel )**2 )
    alpha_err = alphan * rel_err
    print("n=%d  alpha_n=%.20f  +/- %.6e  (rel deviation from alpha_obs: %.3e)"
          % (n, float(alphan), float(alpha_err),
             float(abs(alphan - alpha_obs)/alpha_obs)))

# ===== C35 =====
def planet_dphi(a, e, T_yr, beta):
    M = Msun
    h = mp.sqrt(G * M * a * (1 - e**2))
    dphi_GR_per = 6 * mp.pi * G * M / (c**2 * a * (1 - e**2))
    dphi_geo_per = (3 * mp.pi * beta / (a**2 * (1-e**2))) * (G*M)/(c**2 * a * (1-e**2))
    dphi_per = dphi_GR_per + dphi_geo_per
    N_orb_100 = 100 / T_yr
    dphi_cent = dphi_per * N_orb_100 / arcsec_to_rad
    dphi_GR_cent = dphi_GR_per * N_orb_100 / arcsec_to_rad
    dphi_geo_cent = dphi_geo_per * N_orb_100 / arcsec_to_rad
    return dphi_GR_cent, dphi_geo_cent, dphi_cent

a_mer, e_mer, T_mer = mp.mpf("5.790905e10"), mp.mpf("0.20563069"), mp.mpf("0.240846")
def residual_mer(beta):
    _, _, dp = planet_dphi(a_mer, e_mer, T_mer, beta)
    return dp - mp.mpf("43.03")
beta_opt = mp.findroot(residual_mer, 0)
print("\n===== C35 =====")
print("beta_opt =", mp.nstr(beta_opt, 12))

planets = [
    ("Mercury", a_mer, e_mer, T_mer, mp.mpf("43.03")),
    ("Venus",   mp.mpf("1.0820893e11"), mp.mpf("0.00677672"), mp.mpf("0.615197"), mp.mpf("8.62")),
    ("Earth",   mp.mpf("1.4959787e11"), mp.mpf("0.0167086"), mp.mpf("1.000017"), mp.mpf("3.84")),
]
for name, a_p, e_p, T_p, gr_pred in planets:
    dpGR, dpGeo, dpTot = planet_dphi(a_p, e_p, T_p, beta_opt)
    print("%-8s GR=%.6f  geo=%.6e  total=%.6f  residual(total-gr_pred)=%.3e"
          % (name, float(dpGR), float(dpGeo), float(dpTot), float(dpTot - gr_pred)))
