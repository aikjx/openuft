"""
v5.6 · 调试兰姆移位积分
"""
import math
import numpy as np
from scipy.integrate import simpson, quad
import warnings
warnings.filterwarnings("ignore")

c = 299792458.0
hbar = 1.054571817e-34
alpha = 7.2973525693e-3
m_e = 9.1093837015e-31
e_charge = 1.602176634e-19
eps_0 = 8.8541878128e-12
h_planck = 6.62607015e-34
pi = math.pi

R_e = hbar / (m_e * c)
a0 = 4*pi*eps_0*hbar**2/(m_e*e_charge**2)

def R_2S(r):
    return (1/(2*math.sqrt(2)*a0**1.5)) * (2 - r/a0) * math.exp(-r/(2*a0))

def V_ring(r):
    return e_charge / (4*pi*eps_0*math.sqrt(r**2 + R_e**2))

def V_coul(r):
    return e_charge / (4*pi*eps_0*r)

# Debug: print integrand at key points
print("Debug integrand at key r values:")
for r in [1e-30, 1e-20, 1e-15, 0.01*R_e, 0.1*R_e, R_e, 0.1*a0, a0, 2*a0, 5*a0]:
    r20 = R_2S(r)
    rho = r20**2 * r**2
    dV = V_coul(r) - V_ring(r)
    integrand = rho * dV
    print(f"  r={r:.4e}: R={r20:.4e}, ρ={rho:.4e}, δV={dV:.4e}, ρδV={integrand:.4e}")

# Manual integration with trapezoid
print("\nManual trapezoid integration:")
r_grid = np.logspace(np.log10(1e-30), np.log10(50*a0), 50000)
integrand_grid = np.array([R_2S(r)**2 * r**2 * (V_coul(r) - V_ring(r)) for r in r_grid])
# Manual trapezoid
dlogr = np.log(r_grid[1]/r_grid[0])  # uniform in log
integral = 0
for i in range(len(r_grid)-1):
    r1, r2 = r_grid[i], r_grid[i+1]
    f1, f2 = integrand_grid[i], integrand_grid[i+1]
    # trapezoid: ∫f dr ≈ (f1+f2)/2 * (r2-r1)
    integral += (f1 + f2) / 2 * (r2 - r1)
print(f"  Trapezoid (log-grid): ΔE = {integral:.10e} J")
print(f"  δf = {integral/h_planck/1e6:.4f} MHz")

# Now with the correct density: |R|² r² is the probability density per r
# The integral ∫|R|² r² dr = 1
# The energy shift is ∫|R|² r² δV dr
# But |R|² r² has units of [1/length], and δV has units of [energy]
# So the integral has units of [energy], which is correct.

# Let me check if the issue is with the r² factor
print("\nChecking density without r²:")
for r in [1e-15, R_e, a0]:
    density_without_r2 = R_2S(r)**2
    density_with_r2 = R_2S(r)**2 * r**2
    print(f"  r={r:.4e}: |R|²={density_without_r2:.4e}, |R|²r²={density_with_r2:.4e}")

# Check: ∫|R|² dr vs ∫|R|² r² dr
norm1, _ = quad(lambda r: R_2S(r)**2, 0, 50*a0, limit=500)
norm2, _ = quad(lambda r: R_2S(r)**2 * r**2, 0, 50*a0, limit=500)
print(f"\n∫|R|² dr = {norm1:.6e}")
print(f"∫|R|² r² dr = {norm2:.6e}")
print(f"Expected: ∫|R|² r² dr = 1 (normalized)")

# Direct integration with quad, carefully
print("\nDirect quad integration:")
def full_integrand(r):
    return R_2S(r)**2 * r**2 * (V_coul(r) - V_ring(r))

E_full, err = quad(full_integrand, 1e-30, 50*a0, limit=2000)
print(f"  ΔE = {E_full:.10e} J ± {err:.2e}")
print(f"  δf = {E_full/h_planck/1e6:.4f} MHz")

# Check: most of the contribution should come from r ~ a0
# where the probability density peaks
print("\nProbability density peak location:")
rho = lambda r: R_2S(r)**2 * r**2
# Find peak
r_test = np.logspace(np.log10(0.01*R_e), np.log10(10*a0), 10000)
rho_vals = np.array([rho(r) for r in r_test])
peak_idx = np.argmax(rho_vals)
print(f"  Peak at r = {r_test[peak_idx]:.4e} m = {r_test[peak_idx]/a0:.4f} a₀")
print(f"  Peak value = {rho_vals[peak_idx]:.4e}")
print(f"  V_Coul at peak = {V_coul(r_test[peak_idx]):.4e} J")
print(f"  V_ring at peak = {V_ring(r_test[peak_idx]):.4e} J")
print(f"  δV at peak = {V_coul(r_test[peak_idx]) - V_ring(r_test[peak_idx]):.4e} J")
