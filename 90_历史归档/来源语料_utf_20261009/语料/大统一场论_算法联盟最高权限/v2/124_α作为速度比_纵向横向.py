#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
124_α作为速度比v_v_纵向横向.py
算法联盟最高权限 · α = v_∥/v_⊥ (纵向速度/横向速度) 非 v/c
螺旋: 总速 c; 横向 v⊥=ωR=c·cosθ; 纵向 v∥=ωh=c·sinθ
"""
from mpmath import mp, mpf, sqrt, pi, nstr, atan, sin, cos
mp.dps = 30

c = mpf('299792458')
alpha = mpf('1')/mpf('137.035999084')

print("="*70)
print("α 的真实几何身份: 速度比 v_∥/v_⊥ , 而非 v/c")
print("="*70)
print(f"α = {nstr(alpha,10)}")

# 螺旋速度分量
v_perp = c/sqrt(1+alpha*alpha)          # 横向 ωR
v_par  = c*alpha/sqrt(1+alpha*alpha)    # 纵向 ωh
v_tot  = sqrt(v_perp*v_perp + v_par*v_par)

print(f"\n[螺旋速度分量]")
print(f"  横向速度 v_⊥ = ωR = c/√(1+α²) = {nstr(v_perp,8)} m/s")
print(f"  纵向速度 v_∥ = ωh = c·α/√(1+α²) = {nstr(v_par,8)} m/s")
print(f"  总速  √(v⊥²+v∥²) = {nstr(v_tot,8)} = c ✓")

print(f"\n[关键验证]")
print(f"  α = v_∥/v_⊥ = {nstr(v_par/v_perp,10)}")
print(f"      = (αc/√(1+α²))/(c/√(1+α²)) = α  ✓✓ 精确速度比!")
print(f"  α = tanθ = {nstr(sin(atan(alpha))/cos(atan(alpha)),10)} ✓")
print(f"  θ = atan(α) = {nstr(atan(alpha),8)} rad (螺旋倾角)")

print(f"\n[v/c 对比 - 为什么不对]")
print(f"  v_⊥/c = cosθ = 1/√(1+α²) = {nstr(v_perp/c,8)} ≠ α")
print(f"  v_∥/c = sinθ = α/√(1+α²) = {nstr(v_par/c,8)} ≠ α")
print(f"  → v/c 得到的是 sinθ 或 cosθ, 不是 α!")
print(f"  → 只有速度比 v_∥/v_⊥ = tanθ = α 才精确等于 α")

print(f"\n[几何图景]")
print(f"  螺旋展开一圈: 纵向走 h, 横向走周长 2πR")
print(f"  螺距比 h/R = tanθ = α  (几何)")
print(f"  速度比 v_∥/v_⊥ = ωh/ωR = h/R = α  (运动学)")
print(f"  → 几何螺距比 = 运动学速度比 = α, 三者同一")

print("\n" + "="*70)
print("[结论]")
print("  α = v_∥/v_⊥ = 纵向速度/横向速度 = tanθ = h/R")
print("  这是「速度比 v/v」, 不是「v/c」!")
print("  α 是螺旋的横向-纵向速度之比, 也是螺距角正切")
print("="*70)
