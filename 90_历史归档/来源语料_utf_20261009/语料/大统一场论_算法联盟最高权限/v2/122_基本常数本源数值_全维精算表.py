#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
122_基本常数本源数值_全维精算表.py
算法联盟最高权限 · 所有基本常数的本源数值 + 来源分类(定义/测量/导出/循环)
"""
from mpmath import mp, mpf, sqrt, pi, nstr
mp.dps = 30

print("="*80)
print("基本常数本源数值 · 全维精算表")
print("="*80)

print("""
[分类约定]
  定义值(D)  : 2019 SI 人为约定, 精确无误差
  导出值(E)  : 由定义值+π 等精确算得
  测量值(M)  : 实验测得, 有不确定度
  循环值(C)  : 由目标量自身定义 → 无独立本源
""")

# ============ 定义值 (2019 SI) ============
c    = mpf('299792458')              # D 光速
h    = mpf('6.62607015e-34')         # D 普朗克常数
e    = mpf('1.602176634e-19')        # D 元电荷
kB   = mpf('1.380649e-23')           # D 玻尔兹曼常数
mu0  = mpf('1.25663706212e-6')       # D 真空磁导率
NA   = mpf('6.02214076e23')          # D 阿伏伽德罗
hbar = h/(2*pi)                      # E 约化普朗克
eps0 = 1/(mu0*c*c)                   # E 真空介电常数(由 c,mu0)

# ============ 测量值 (CODATA 2022) ============
alpha= mpf('1')/mpf('137.035999084') # M 精细结构常数
G    = mpf('6.67430e-11')            # M 引力常数
me   = mpf('9.1093837015e-31')       # M 电子质量
mp   = mpf('1.67262192369e-27')      # M 质子质量

# ============ 循环值 (普朗克单位) ============
lP   = sqrt(G*hbar/c**3)
mP   = sqrt(hbar*c/G)
tP   = sqrt(G*hbar/c**5)

print("="*80)
print("[1] 精确定义值 (2019 SI, 人类约定)")
print("="*80)
print(f"  c   光速       = {nstr(c,12)} m/s            [D]")
print(f"  h   普朗克常数 = {nstr(h,12)} J·s          [D]")
print(f"  e   元电荷     = {nstr(e,12)} C        [D]")
print(f"  k_B 玻尔兹曼   = {nstr(kB,12)} J/K    [D]")
print(f"  μ₀  磁导率     = {nstr(mu0,12)} N/A²      [D]")
print(f"  N_A 阿伏伽德罗 = {nstr(NA,12)} mol⁻¹     [D]")

print("="*80)
print("[2] 导出值 (由定义值精确算得)")
print("="*80)
print(f"  ℏ   = h/2π      = {nstr(hbar,12)} J·s        [E]")
print(f"  ε₀  = 1/μ₀c²    = {nstr(eps0,12)} F/m    [E]")
print(f"  ℏc  =           = {nstr(hbar*c,12)} J·m   [E]")

print("="*80)
print("[3] 测量值 (CODATA 2022, 有不确定度)")
print("="*80)
print(f"  α   = 1/137.035999084 = {nstr(alpha,12)}    [M]")
print(f"  G   = {nstr(G,12)} m³/(kg·s²)       [M]")
print(f"  m_e = {nstr(me,12)} kg          [M]")
print(f"  m_p = {nstr(mp,12)} kg          [M]")

print("="*80)
print("[4] 循环值 (普朗克单位, 由 G 定义)")
print("="*80)
print(f"  ℓ_P = sqrt(Gℏ/c³) = {nstr(lP,8)} m    [C 依赖G]")
print(f"  m_P = sqrt(ℏc/G)  = {nstr(mP,8)} kg   [C 依赖G]")
print(f"  t_P = sqrt(Gℏ/c⁵) = {nstr(tP,8)} s    [C 依赖G]")

print("="*80)
print("[5] 螺旋本源量 (由 m_e 反推, 框架)")
print("="*80)
omega = me*c*c/hbar
K = omega/c
R = 1/(K*sqrt(1+alpha*alpha))
hh = alpha*R
print(f"  ω_e 本源角频率 = {nstr(omega,6)} rad/s  [由E=mc²=ℏω]")
print(f"  √(κ²+τ²)       = {nstr(K,6)} m⁻¹   [=1/λ̄_C]")
print(f"  κ_e 曲率       = {nstr(omega/(c*sqrt(1+alpha*alpha)),6)} m⁻¹ [需α]")
print(f"  τ_e 挠率       = {nstr(alpha*omega/(c*sqrt(1+alpha*alpha)),6)} m⁻¹ [需α]")
print(f"  R_e 螺旋半径   = {nstr(R,6)} m    [需α]")
print(f"  h_e 螺距       = {nstr(hh,6)} m    [需α]")

print("="*80)
print("[6] 本源能力总结")
print("="*80)
print(f"  可精确本源(无需测量): c,h,e,kB,μ₀,NA,ℏ,ε₀  (全是人为定义)")
print(f"  必须测量:            α,G,m_e,m_p           (无理论预言)")
print(f"  循环:                ℓ_P,m_P,t_P           (由G定义)")
print(f"  螺旋量:              ω,√(κ²+τ²) 可由 m_e 反推; κ,τ,R,h 需α")
print(f"  → 没有任何常数能【由几何第一性原理】预言出数值")
print("="*80)
