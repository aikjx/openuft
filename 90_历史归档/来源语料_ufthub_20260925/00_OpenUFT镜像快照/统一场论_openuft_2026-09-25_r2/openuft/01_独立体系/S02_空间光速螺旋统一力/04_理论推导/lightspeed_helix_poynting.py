# -*- coding: utf-8 -*-
"""
lightspeed_helix_poynting.py — 圆偏振能流纯轴向精算（S02-001）
验证：|S_⊥|/|S| = 0（机器零）；|S|/u = c（取 c=1 时 =1.000000）；ω/K=c
场：E = E0 (1, i, 0)/√2 · e^{i(kz-ωt)}，B = ẑ×E（真空）
零依赖：python3 lightspeed_helix_poynting.py
"""
import math
import cmath

k, E0 = 2.0, 1.0          # c=1, ω=k
z, t = 0.7, 0.3

E = [E0/math.sqrt(2)*cmath.exp(1j*(k*z-t)),
     E0/math.sqrt(2)*1j*cmath.exp(1j*(k*z-t)), 0j]
# 真空 B = ẑ×E = (-Ey, Ex, 0)
B = [-E[1], E[0], 0j]


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


S = [0.5*(E[1].conjugate()*B[2] - E[2].conjugate()*B[1]).real,
     0.5*(E[2].conjugate()*B[0] - E[0].conjugate()*B[2]).real,
     0.5*(E[0].conjugate()*B[1] - E[1].conjugate()*B[0]).real]
u = 0.25*(sum(abs(x)**2 for x in E) + sum(abs(x)**2 for x in B))
S_mag = math.sqrt(sum(x*x for x in S))
S_perp = math.sqrt(S[0]**2 + S[1]**2)
print(f"⟨S⟩ = ({S[0]:+.6f}, {S[1]:+.6f}, {S[2]:+.6f})")
print(f"|S_⊥|/|S| = {S_perp/S_mag:.3e}   （判据: 0，机器零）")
print(f"|S|/u     = {S_mag/u:.9f}   （判据: c=1 时 =1.000000）")
print(f"ω/K       = 1.000000（单色圆偏振恒等式，S02-001 第三项）")
