# -*- coding: utf-8 -*-
"""
lightspeed_helix_spin.py — 每光子自旋精算（S02-002）
验证：圆偏振单色平面波每光子自旋 = 1.000000 ℏ
公式：自旋密度 s_z = Im(E*×E)_z/(2ω)；光子数密度 n = ⟨u⟩/ℏω
零依赖：python3 lightspeed_helix_spin.py
"""
import math
import cmath

k, E0 = 2.0, 1.0
z, t = 0.7, 0.3
hbar = 1.0

E = [E0/math.sqrt(2)*cmath.exp(1j*(k*z-t)),
     E0/math.sqrt(2)*1j*cmath.exp(1j*(k*z-t)), 0j]
spin_density = (E[0].conjugate()*E[1] - E[1].conjugate()*E[0]).imag / (2*k)
u = 0.25*(sum(abs(x)**2 for x in E) + sum(abs(x)**2 for x in E))  # |B|=|E|
n_photon = u / (k*hbar)
spin_per_photon = spin_density / n_photon
print(f"自旋密度 s_z  = {spin_density:+.9f}")
print(f"光子数密度 n  = {n_photon:.9f}")
print(f"每光子自旋    = {spin_per_photon:.9f} ℏ   （判据: 1.000000，S02-002）")
print(f"残差          = {abs(spin_per_photon-1.0):.3e}")
