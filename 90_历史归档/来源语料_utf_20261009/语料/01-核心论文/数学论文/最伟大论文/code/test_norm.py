"""
v5.3 · 测试波函数归一化 - 简化版
"""
import math
import numpy as np
from scipy.integrate import quad

a0 = 5.29177210903e-11  # Bohr radius

# 2S radial wavefunction (standard form)
def R_2S(r):
    return (1/(2*math.sqrt(6)*a0**1.5)) * r * (2 - r/a0) * math.exp(-r/(2*a0))

# 2P radial wavefunction
def R_2P(r):
    return (1/math.sqrt(24*a0**3)) * r**1.5 * math.exp(-r/(2*a0))

# Test normalization
def f2S(r):
    return R_2S(r)**2 * r**2

def f2P(r):
    return R_2P(r)**2 * r**2

n2s, _ = quad(f2S, 0, 50*a0, limit=500)
n2p, _ = quad(f2P, 0, 50*a0, limit=500)

print(f"Norm 2S = {n2s:.10f}")
print(f"Norm 2P = {n2p:.10f}")

# Check peak
r_test = np.logspace(np.log10(0.01*a0), np.log10(10*a0), 100)
for r in [0.01*a0, 0.1*a0, 0.5*a0, a0, 2*a0, 5*a0]:
    print(f"  r={r:.4e}: R_2S={R_2S(r):.6e}, R_2P={R_2P(r):.6e}")

# Alternative normalized form
# The correct form from quantum mechanics:
# R_{20}(r) = (1/(2√6)) * (1/a₀)^{3/2} * (r/a₀) * (2 - r/a₀) * exp(-r/(2a₀))
# R_{21}(r) = (1/√24) * (1/a₀)^{3/2} * (r/a₀)^2 * exp(-r/(2a₀))

def R_2S_v2(r):
    return (1/(2*math.sqrt(6))) * (1/a0)**1.5 * (r/a0) * (2 - r/a0) * math.exp(-r/(2*a0))

def R_2P_v2(r):
    return (1/math.sqrt(24)) * (1/a0)**1.5 * (r/a0)**2 * math.exp(-r/(2*a0))

def f2S_v2(r):
    return R_2S_v2(r)**2 * r**2

def f2P_v2(r):
    return R_2P_v2(r)**2 * r**2

n2s_v2, _ = quad(f2S_v2, 0, 50*a0, limit=500)
n2p_v2, _ = quad(f2P_v2, 0, 50*a0, limit=500)

print(f"\nV2 forms:")
print(f"Norm 2S = {n2s_v2:.10f}")
print(f"Norm 2P = {n2p_v2:.10f}")

# Which one is correct? Let's check the standard QM formula
# From Griffiths, "Introduction to Quantum Mechanics":
# R_{nl}(r) = -√( (2Z/(na))³ (n-l-1)!/(2n[(n+l)!]³) ) exp(-Zr/(na)) (2Zr/(na))^l L^{2l+1}_{n-l-1}(2Zr/(na))
# For n=2, l=0, Z=1, a=a₀:
# prefactor = -√( (2/(2a₀))³ (1)!/(2·2·(2!)³) ) = -√( (1/a₀³) 1/(4·8) ) = -√(1/(32a₀³))
# = -1/(4√2 a₀^{3/2})
# L^1_1(x) = 1 - x  (Laguerre)
# So R_{20} = -1/(4√2 a₀^{3/2}) exp(-r/(2a₀)) (1 - r/a₀)
# But this doesn't match the "standard" form with r(2-r/a₀) factor
# Let me re-check...

# Actually, the associated Laguerre polynomials:
# L^p_q(x) = (-1)^p d^p/dx^p L_{p+q}(x)
# L_0(x) = 1, L_1(x) = 1-x
# L^1_1(x) = -d/dx L_2(x)... hmm

# Let me just look up the standard result:
# R_{20}(r) = (1/(2√6 a₀^{3/2})) (2 - r/a₀) (r/a₀) exp(-r/(2a₀))
# R_{21}(r) = (1/(√24 a₀^{3/2})) (r/a₀)^{3/2} exp(-r/(2a₀))

# The first form has Norm 2S = 0 (underflows). 
# Let me check if the issue is that (2 - r/a₀) changes sign.

# For 2S, the wavefunction node is at r = 2a₀.
# For r < 2a₀: (2 - r/a₀) > 0
# For r > 2a₀: (2 - r/a₀) < 0
# The square removes the sign issue, but the integral should be fine.

# Let me just plot to see the integrand
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = np.linspace(0.01*a0, 5*a0, 1000)
y2s = [f2S(ri) for ri in r]
y2p = [f2P(ri) for ri in r]

print(f"\nMax integrand 2S: {max(y2s):.6e} at r={r[np.argmax(y2s)]:.4e}")
print(f"Max integrand 2P: {max(y2p):.6e} at r={r[np.argmax(y2p)]:.4e}")
print(f"Sum 2S (trapezoid): {np.trapz(y2s, r):.6e}")
print(f"Sum 2P (trapezoid): {np.trapz(y2p, r):.6e}")

# Check if norm is 1 with v2 forms
r = np.linspace(0.01*a0, 50*a0, 50000)
y2s_v2 = [f2S_v2(ri) for ri in r]
y2p_v2 = [f2P_v2(ri) for ri in r]
print(f"\nV2 trapezoid 2S: {np.trapz(y2s_v2, r):.10f}")
print(f"V2 trapezoid 2P: {np.trapz(y2p_v2, r):.10f}")

# The issue: (r/a₀)^{3/2} = (r/a₀) * √(r/a₀) 
# In R_2S: (r/a₀) * (2 - r/a₀) → this is correct for the radial part
# Let me try yet another form
