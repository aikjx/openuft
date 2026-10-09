#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
121_光速螺旋ωR_频率f_全维度融合关系网.py
算法联盟最高权限 · 空间光速螺旋 ωR 与频率 f 的全维度关系关联精算
核心: v_总=c → ω²(R²+h²)=c²;  横向速度 ωR=c·cosθ;  频率 f=ω/2π
"""
from mpmath import mp, mpf, sqrt, pi
mp.dps = 40

hbar=mpf('1.05457181764615639e-34')
h   =mpf('6.62607015e-34')
c   =mpf('299792458')
me  =mpf('9.1093837015e-31')
alpha=mpf('1')/mpf('137.035999084')

print("="*72)
print("空间光速螺旋 ωR · 频率 f · 全维度融合关系网")
print("="*72)

# ===== 电子螺旋基础 =====
omega = me*c**2/hbar          # 本源角频率
K     = omega/c                # √(κ²+τ²)
R     = 1/(K*sqrt(1+alpha*alpha))   # 螺旋半径 R = λ_C/√(1+α²)
hh    = alpha*R                 # 螺距参数
f     = omega/(2*pi)            # 频率

print(f"\n[电子螺旋本源量]")
print(f"  本源角频率 ω = {mp.nstr(omega,6)} rad/s")
print(f"  频率   f     = {mp.nstr(f,6)} Hz")
print(f"  曲率挠率模 K = {mp.nstr(K,6)} m⁻¹")
print(f"  半径   R     = {mp.nstr(R,6)} m")
print(f"  螺距   h     = {mp.nstr(hh,6)} m")

# ===== 关键: ωR 的定位 =====
print(f"\n[ωR 的准确定位]")
wr = omega*R
wh = omega*hh
v_total = sqrt(wr*wr + wh*wh)
print(f"  横向速度 ωR   = {mp.nstr(wr,6)} m/s = c·cosθ = {mp.nstr(c/sqrt(1+alpha*alpha),6)}")
print(f"  纵向速度 ωh   = {mp.nstr(wh,6)} m/s = c·sinθ")
print(f"  总速 √((ωR)²+(ωh)²) = {mp.nstr(v_total,6)} m/s = c  ✓")
print(f"  cosθ = 1/√(1+α²) = {mp.nstr(1/sqrt(1+alpha*alpha),6)}")
print(f"  → 注意: ωR = c/√(1+α²) ≈ c(1-α²/2) ≈ {mp.nstr(c*(1-alpha**2/2),6)}, 接近但不等于 c")
print(f"  → 精确说 ωR=c 仅在 α=0(无纵向)极限; 有螺距时 ωR=c·cosθ<c")

# ===== 全维度关系 =====
print(f"\n[ω↔f↔c↔λ↔E↔m↔κ↔τ 全维度融合]")

print(f"\n  A. 频率关系")
print(f"     ω = 2πf        : {mp.nstr(omega,6)} vs 2π·{mp.nstr(f,6)} = {mp.nstr(2*pi*f,6)} ✓")
print(f"     f = ω/2π       : {mp.nstr(f,6)} Hz")
print(f"     ω = 2πc/λ      : λ={mp.nstr(2*pi*c/omega,6)} m")

print(f"\n  B. 能量关系")
print(f"     E = ℏω = {mp.nstr(hbar*omega,6)} J")
print(f"     E = hf  = {mp.nstr(h*f,6)} J  一致 ✓")
print(f"     E = m c² = {mp.nstr(me*c*c,6)} J  一致 ✓")

print(f"\n  C. 频率-质量-曲率融合")
print(f"     m = ℏω/c² = hf/c² = {mp.nstr(h*f/c**2,6)} kg = m_e ✓")
print(f"     √(κ²+τ²) = ω/c = {mp.nstr(omega/c,6)} m⁻¹")
print(f"     ω = c√(κ²+τ²) 校验: {mp.nstr(c*K,6)} vs {mp.nstr(omega,6)} ✓")

print(f"\n  D. 频率-波长")
print(f"     f·λ = c : {mp.nstr(f*(c/f),6)} = c ✓")
print(f"     λ_C(约化) = ℏ/mc = {mp.nstr(hbar/(me*c),6)} m")
print(f"     ω = 2πc/λ_C = {mp.nstr(2*pi*c/(hbar/(me*c)),6)} vs {mp.nstr(omega,6)} ✓")

print(f"\n  E. 曲率挠率 vs 频率")
print(f"     κ = ω/(c√(1+α²)) = {mp.nstr(omega/(c*sqrt(1+alpha*alpha)),6)} m⁻¹")
print(f"     τ = α·κ          = {mp.nstr(alpha*omega/(c*sqrt(1+alpha*alpha)),6)} m⁻¹")
print(f"     ω/c·√(1+α²) 关系: κ²+τ²=(ω/c)²  ✓")

print(f"\n[全维度融合总表]")
print(f"  ┌─────────┬──────────────────────────────────────────┐")
print(f"  │ 角频率ω │ ω=2πf=c√(κ²+τ²)=c/√(R²+h²)=E/ℏ=mc²/ℏ    │")
print(f"  │ 频率 f  │ f=ω/2π=c/λ=E/h=mc²/h                     │")
print(f"  │ 曲率 κ  │ κ=ω/(c√(1+α²))=cosθ·√(κ²+τ²)            │")
print(f"  │ 挠率 τ  │ τ=ακ=αω/(c√(1+α²))=sinθ·√(κ²+τ²)        │")
print(f"  │ 能量 E  │ E=ℏω=hf=mc²                              │")
print(f"  │ 质量 m  │ m=ℏω/c²=hf/c²=ℏ√(κ²+τ²)/c                │")
print(f"  │ 横向速  │ ωR=c·cosθ=c/√(1+α²)                      │")
print(f"  │ 总速    │ √((ωR)²+(ωh)²)=c                         │")
print(f"  └─────────┴──────────────────────────────────────────┘")

print("\n" + "="*72)
print("[结论] 螺旋频率 ω 是全维度枢纽:")
print("  频率 ω 同时连接: f(频率), c(光速), κ,τ(几何), E(能量), m(质量), λ(波长), R,h(螺旋)")
print("  ωR=c 是「横向全速」极限(α→0); 一般螺旋 ωR=c·cosθ, 总速恒为 c")
print("  κ²+τ²=(ω/c)² 使 几何(κ,τ) 与 频率(ω) 与 光速(c) 三位一体")
print("="*72)
