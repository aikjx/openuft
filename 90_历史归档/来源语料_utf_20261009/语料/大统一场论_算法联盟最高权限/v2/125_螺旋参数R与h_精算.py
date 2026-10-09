#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
125_螺旋参数R与h_精算.py
算法联盟最高权限 · 螺旋的两个几何参数 R(半径) 与 h(螺距参数)
螺旋参数方程: r(θ) = (R cosθ, R sinθ, h·θ)
"""
from mpmath import mp, mpf, sqrt, pi, nstr
mp.dps = 25

hbar=mpf('1.05457181764615639e-34')
c   =mpf('299792458')
me  =mpf('9.1093837015e-31')
alpha=mpf('1')/mpf('137.035999084')

print("="*72)
print("螺旋参数 R 与 h · 精算确认")
print("="*72)

# 推导 R, h (电子)
K  = me*c/hbar                 # √(κ²+τ²) = 1/λ̄_C
R  = 1/(K*sqrt(1+alpha*alpha)) # 半径 = λ̄_C/√(1+α²)
hh = alpha*R                   # 螺距参数 h = αR
p  = 2*pi*hh                   # 完整螺距(一圈高度)

print(f"\n[电子螺旋的 R 与 h]")
print(f"  R (半径)   = {nstr(R,8)} m")
print(f"  h (螺距参数)= {nstr(hh,8)} m")
print(f"  完整螺距 p = 2πh = {nstr(p,8)} m")

print(f"\n[数学定义]")
print(f"  螺旋参数方程:  r(θ) = ( R·cosθ ,  R·sinθ ,  h·θ )")
print(f"    x = R cosθ   (横向圆周运动)")
print(f"    y = R sinθ   (横向圆周运动)")
print(f"    z = h·θ      (纵向直线爬升)")

print(f"\n[R 的含义]")
print(f"  R = 螺旋在横向(xy)平面的投影圆半径")
print(f"    = 电子约化Compton波长 / √(1+α²)")
print(f"    = λ̄_C/√(1+α²) = {nstr(1/(K*sqrt(1+alpha*alpha)),8)}")
print(f"  R 决定螺旋的『粗细/横向尺度』")
print(f"  λ̄_C = ℏ/m_ec = {nstr(1/K,8)} m (约化Compton波长)")

print(f"\n[h 的含义]")
print(f"  h = 每转 1 弧度(θ增加1), 纵向z上升的距离")
print(f"    = α·R = tanθ·R  (螺距角正切 × 半径)")
print(f"  h 决定螺旋的『倾斜/纵向尺度』")
print(f"  h/R = α (倾角正切) → h 是 α 的几何化身")

print(f"\n[两参数关系]")
print(f"  螺距比 h/R = {nstr(hh/R,8)} = α ✓")
print(f"  总速度 c = √((ωR)²+(ωh)²), 与 R,h 关系:")
print(f"    ω = c/√(R²+h²) = {nstr(c/sqrt(R*R+hh*hh),8)} rad/s")

print(f"\n[物理直观]")
print(f"  R 大 → 螺旋粗(横向展开大)")
print(f"  h 大 → 螺旋陡(纵向爬升快, 倾角大)")
print(f"  α = h/R 固定两者比例 = 倾角 = 精细结构常数")

print("\n" + "="*72)
print("[结论]")
print("  R = 螺旋横向半径(尺度大小)")
print("  h = 螺距参数(纵向倾斜, 每弧度爬升高度)")
print("  二者独立决定螺旋形状: R定粗细, h定倾斜, 比值h/R=α")
print("="*72)
