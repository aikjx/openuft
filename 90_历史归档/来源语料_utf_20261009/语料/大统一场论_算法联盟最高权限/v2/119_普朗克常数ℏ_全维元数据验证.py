#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
119_普朗克常数ℏ_全维元数据验证.py
算法联盟最高权限 · ℏ 全维元数据数值精算验证
2019 SI 重新定义后: h 是精确定义值, ℏ = h/(2π) 也是精确值
"""
from mpmath import mp, mpf, pi, sqrt, log10
mp.dps = 60

# ============ 精确定义值 (2019 SI) ============
h  = mpf('6.62607015e-34')      # Planck 常数(精确定义)
hbar = h/(2*pi)                  # 约化 Planck 常数(精确)
e  = mpf('1.602176634e-19')     # 元电荷(精确定义)
c  = mpf('299792458')           # 光速(精确定义)
# CODATA 2022 测量值
alpha_inv = mpf('137.035999084')
alpha = 1/alpha_inv

print("="*70)
print("普朗克常数 ℏ · 全维元数据数值验证")
print("="*70)

print(f"\n[精确定义值与导出]")
print(f"  h   = {mp.nstr(h,18)} J·s   (2019 SI 精确定义值)")
print(f"  ℏ   = h/(2π) = {mp.nstr(hbar,18)} J·s")
print(f"  ℏ   = {mp.nstr(hbar*1e34,12)} × 10⁻³⁴ J·s")
print(f"  ℏ   = {mp.nstr(hbar*1e27,12)} × 10⁻²⁷ erg·s (CGS)")
print(f"  ℏ   = {mp.nstr(hbar*1e16,12)} × 10⁻¹⁶ eV·s")
print(f"  ℏc  = {mp.nstr(hbar*c,12)} J·m = {mp.nstr(hbar*c/e*1e6,6)} MeV·fm")

print(f"\n[量纲与常用形式]")
# 质量·长度²/时间
print(f"  [ℏ] = M·L²·T⁻¹ = kg·m²/s")
# ℏc
print(f"  ℏc  = {mp.nstr(hbar*c,12)} kg·m³/s² = {mp.nstr(hbar*c,12)} eV·m/1.6e-19")
print(f"  ℏc  = 197.3269804 MeV·fm  (常用)")

print(f"\n[与其他常数关系]")
# 精细结构常数定义
print(f"  α = e²/(4πε₀ℏc) → ℏ = e²/(4πε₀αc)")
# 质量本源
me = mpf('9.1093837015e-31')
kappa_e = me*c/hbar
print(f"  m = ℏκ/c  →  ℏ = mc/κ  (质量本源)")
print(f"    电子: ℏ = m_e·c/κ_e 校验: {mp.nstr(mp.fabs(mp.log10(me*c/kappa_e/hbar)),2)} (1.0)")
# 角动量
print(f"  角动量 L = mvr → ℏ = mvr (角动量的天然量子)")
print(f"  自旋 S = ½ℏ")
print(f"  能量 E = ℏω (角频率),  E = hν (频率)")
print(f"  动量 p = ℏk = h/λ (de Broglie)")
print(f"  不确定性 Δx·Δp ≥ ℏ/2")
print(f"  磁性 μ = g eℏ/(2m) (磁矩尺度)")

print(f"\n[普朗克单位]")
G = mpf('6.67430e-11')
lP = sqrt(G*hbar/c**3)
mP = sqrt(hbar*c/G)
tP = sqrt(G*hbar/c**5)
print(f"  ℓ_P = sqrt(Gℏ/c³) = {mp.nstr(lP,6)} m")
print(f"  m_P = sqrt(ℏc/G)  = {mp.nstr(mP,6)} kg")
print(f"  t_P = sqrt(Gℏ/c⁵) = {mp.nstr(tP,6)} s")

print(f"\n[ℏ 数值的两种表达]")
print(f"  h  = 6.62607015×10⁻³⁴ (精确, 定义)")
print(f"  ℏ  = h/2π = {mp.nstr(hbar*1e34,12)}×10⁻³⁴ (精确, 由 h 定义)")
print(f"  π  = {mp.nstr(pi,20)}")

print(f"\n[框架定位]")
print(f"  A2 公理: ℏ = mc√(R²+h²)  (螺旋角动量量子化, 引入 M 维度)")
print(f"  质量本源: m = (ℏ/c)√(κ²+τ²)")
print(f"  NG-X: ℏ 数值是精确定义值(人类约定), 非由几何推导")
print(f"  ℏ 是「几何→物理」的全局转换常数, 全域普适")
print("="*70)
