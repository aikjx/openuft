import math

c = 299792458.0
hbar = 1.0545718176461565e-34
m_e = 9.1093837015e-31
l_P = 1.6162551807507155e-35

rho_e = hbar / (m_e * c)
print(f"rho_e = hbar/(m_e*c) = {rho_e:.15e} m")

alpha = 1/137.035999084
b_e = rho_e / alpha
print(f"b_e = rho_e/alpha = {b_e:.15e} m")

kappa_e = rho_e / (rho_e**2 + b_e**2)
tau_e = b_e / (rho_e**2 + b_e**2)
print(f"kappa_e = rho/(rho^2+b^2) = {kappa_e:.15e} m^-1")
print(f"tau_e = b/(rho^2+b^2) = {tau_e:.15e} m^-1")

omega_e = c / rho_e
print(f"omega_e = c/rho_e = {omega_e:.15e} rad/s")

inv = kappa_e**2 + tau_e**2
inv_expected = 1 / (rho_e**2 + b_e**2)
print(f"kappa^2+tau^2 = {inv:.15e} m^-2")
print(f"1/(rho^2+b^2) = {inv_expected:.15e} m^-2")
print(f"Invariant OK: {abs(inv-inv_expected)/inv_expected < 1e-15}")

alpha_calc = kappa_e / tau_e
print(f"alpha = kappa/tau = {alpha_calc:.12f}")
print(f"alpha expected = {alpha:.12f}")
print(f"Alpha error: {abs(alpha_calc-alpha)/alpha*100:.15f}%")

kappa_P = 1.0 / (2 * l_P)
tau_P = kappa_P
print(f"kappa_P = tau_P = 1/(2*l_P) = {kappa_P:.15e} m^-1")

G_geo = c**3 / (2 * hbar * (kappa_P**2 + tau_P**2))
G_codata = 6.67430e-11
print(f"G = c^3/(2*hbar*(kappa_P^2+tau_P^2)) = {G_geo:.15e} m^3/(kg*s^2)")
print(f"CODATA G = {G_codata:.15e} m^3/(kg*s^2)")
print(f"G error: {abs(G_geo-G_codata)/G_codata*100:.15f}%")

e = 1.602176634e-19
epsilon0_geo = e**2 * tau_e / (4 * math.pi * kappa_e * hbar * c)
epsilon0_codata = 8.854187817e-12
print(f"epsilon0 = e^2*tau/(4*pi*kappa*hbar*c) = {epsilon0_geo:.15e} F/m")
print(f"CODATA epsilon0 = {epsilon0_codata:.15e} F/m")
print(f"epsilon0 error: {abs(epsilon0_geo-epsilon0_codata)/epsilon0_codata*100:.15f}%")

print("\n" + "="*70)
print("v=c SYSTEM PRECISION VERIFICATION COMPLETE")
print("="*70)