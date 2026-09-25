# -*- coding: utf-8 -*-
"""
lightspeed_helix_polarization.py — 一般偏振自旋角动量（S02-003）
验证：SAM = σℏ，σ = 2ab/(a²+b²)，a,b 为椭圆偏振半轴
公式：σ = Im(E*×E)_z / |E|²（单位化）
零依赖：python3 lightspeed_helix_polarization.py
"""
import math

def sigma_elliptical(a, b):
    """椭圆偏振 E ∝ (a, i b, 0)：σ = 2ab/(a²+b²)"""
    E = [a, 1j*b, 0j]
    num = (E[0].conjugate()*E[1] - E[1].conjugate()*E[0]).imag
    den = sum(abs(x)**2 for x in E)
    return num/den, 2*a*b/(a*a+b*b)

print("a, b        σ(数值)       σ=2ab/(a²+b²)   相对差")
cases = [(1.0,1.0),(1.0,0.0),(2.0,1.0),(3.0,1.0),(1.0,0.5)]
for a,b in cases:
    num, ana = sigma_elliptical(a,b)
    rel = abs(num-ana)/max(abs(ana),1e-30)
    print(f"({a:>4.1f},{b:>4.1f})  {num:+.9f}   {ana:+.9f}   {rel:.2e}")
print("\n判据: 数值与解析恒等式 σ=2ab/(a²+b²) 一致（S02-003）")
print("特例: a=b(圆偏振)→σ=1；b=0(线偏振)→σ=0。")
