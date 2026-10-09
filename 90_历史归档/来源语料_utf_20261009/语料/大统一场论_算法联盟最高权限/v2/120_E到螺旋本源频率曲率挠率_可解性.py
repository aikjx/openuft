#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
120_E到螺旋本源频率曲率挠率_可解性.py
算法联盟最高权限 · 给定 E=ℏω 能否反推螺旋本源 {ω, κ, τ}?
核心: 频率能, 曲率挠率"模"能, 单个κ/τ不能(α自由)
"""
from mpmath import mp, mpf, sqrt, pi
mp.dps = 40

hbar = mpf('1.05457181764615639e-34')
c    = mpf('299792458')
me   = mpf('9.1093837015e-31')
alpha= mpf('1')/mpf('137.035999084')

print("="*70)
print("E=ℏω → 本源频率/曲率/挠率 可解性精算")
print("="*70)

# 电子能量
E = me*c**2
print(f"\n[输入] 电子 E = m_e·c² = {mp.nstr(E,6)} J")

# 1. 本源频率
omega = E/hbar
print(f"\n[1] 本源频率 ω = E/ℏ = {mp.nstr(omega,6)} rad/s  ✅ 可确定")
print(f"    校验 ω = m_e c²/ℏ = {mp.nstr(me*c**2/hbar,6)} 一致")

# 2. 曲率挠率模
K = omega/c
print(f"\n[2] 曲率挠率模 √(κ²+τ²) = ω/c = {mp.nstr(K,6)} m⁻¹  ✅ 可确定")
print(f"    校验 = m_e·c/ℏ = {mp.nstr(me*c/hbar,6)} 一致")
print(f"    = 电子约化Compton波长倒数 1/λ̄_C = {mp.nstr(1/(hbar/(me*c)),6)}")

# 3. 单个 κ, τ —— 是否可确定?
print(f"\n[3] 单个 κ, τ 能否由 E 唯一确定?")
print(f"    已知: κ²+τ² = K² (圆),  α = τ/κ (倾角, 自由)")
print(f"    解:  κ = K/√(1+α²),  τ = αK/√(1+α²)")
print(f"    α 是自由参数 → κ,τ 在一个圆上, 非唯一!")

# 展示: 不同 α 给出不同 κ,τ 但同一模 K
print(f"\n    同一 E(=同一 K)下, 不同 α 的 κ,τ:")
for a in [mpf('0.001'), alpha, mpf('0.1'), mpf('1')]:
    kap = K/sqrt(1+a*a)
    tau = a*kap
    print(f"      α={mp.nstr(a,4)}: κ={mp.nstr(kap,6)}, τ={mp.nstr(tau,6)}, "
          f"√(κ²+τ²)={mp.nstr(sqrt(kap*kap+tau*tau),6)} (固定)")
print(f"\n    模 √(κ²+τ²) 全部= {mp.nstr(K,6)} 不变, 但 κ,τ 各自值随 α 变!")

# 真实电子(用真实α)时的 κ,τ
kap_e = K/sqrt(1+alpha*alpha)
tau_e = alpha*kap_e
print(f"\n[4] 真实电子(α=1/137.036):")
print(f"    κ_e = K/√(1+α²) = {mp.nstr(kap_e,6)} m⁻¹")
print(f"    τ_e = α·κ_e     = {mp.nstr(tau_e,6)} m⁻¹")
print(f"    τ/κ = {mp.nstr(tau_e/kap_e,6)} = α ✓")
print(f"    κ_e/τ_e 比值 = {mp.nstr(kap_e/tau_e,6)} = 1/α ✓")

# 结论
print("\n" + "="*70)
print("[结论]")
print("  1. 本源频率 ω = E/ℏ  ✅ 由 E 唯一确定")
print("  2. 曲率挠率模 √(κ²+τ²) = ω/c = E/(ℏc)  ✅ 由 E 唯一确定")
print("  3. 单个 κ, τ ❌ 不能由 E 唯一确定 (α=τ/κ 是自由参数)")
print("  4. κ²+τ²=K² 是一个圆, E 只定半径 K, 不定圆上位置(倾角α)")
print("  5. 要定单个 κ,τ 需额外知道 α (NG-Iα, 需 A3)")
print("="*70)
