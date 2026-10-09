# -*- coding: utf-8 -*-
"""
GAQ-UFT 几何公理的量纲审计 + 螺旋线恒等式数值验证 + 宇宙学参数核对
==================================================================
核心审计问题：公理 κ²+τ²=(ωℓ_P/c)² 的字面量纲是否自洽？
答案：字面不自洽（左 1/L²，右无量纲）；可自然修复为 κ²+τ²=(ω/c)²=k²，
     其普朗克归一化形式 (κℓ_P)²+(τℓ_P)²=(ωℓ_P/c)² 才是无量纲自洽的写法。
运行：python verify_geometry.py
"""
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print(" [A] 螺旋线的曲率-挠率恒等式：κ²+τ²=1/(r²+p²)=k²")
print("="*78)
# 圆螺旋：x=r cos(t), y=r sin(t), z=p t，t 为无量纲参数
# κ = r/(r²+p²),  τ = p/(r²+p²),  ⇒ κ²+τ² = 1/(r²+p²)
r, p = mp.mpf("3"), mp.mpf("4")   # 半径与螺距参数
k = mp.sqrt(1/(r**2+p**2))        # 波数
kappa = r/(r**2+p**2)
tau   = p/(r**2+p**2)
print(f"  r=3, p=4：κ={mp.nstr(kappa,10)}, τ={mp.nstr(tau,10)}")
print(f"  κ²+τ² = {mp.nstr(kappa**2+tau**2, 12)}")
print(f"  1/(r²+p²) = {mp.nstr(1/(r**2+p**2), 12)}")
print(f"  k²=(ω/c)² = {mp.nstr(k**2, 12)}")
print(f"  相对偏差 = {mp.nstr(abs(kappa**2+tau**2-1/(r**2+p**2))/(1/(r**2+p**2)), 6)}")
print(f"  结论：对螺旋线，κ²+τ²=1/(r²+p²) 精确成立（这是经典微分几何事实）。")
print(f"       '公理'的几何内容可理解为：曲线上每点的'总弯曲密度'κ²+τ² 等于")
print(f"       对应波动模式的波数平方 k²=(ω/c)²。")
print()
print("  —— 量纲审计 ——")
print("  字面形式 κ²+τ²=(ωℓ_P/c)²：")
print("    κ,τ 量纲 1/L ⇒ 左端量纲 1/L²")
print("    (ωℓ_P/c)²: ω(1/T)·ℓ_P(L)·c(L/T)⁻¹ ⇒ 无量纲 ⇒ 右端量纲 1")
print("    判定：字面量纲不自洽（L⁻² ≠ 1）→ 记为审计项 OPEN-D1")
print("  修复：引入普朗克归一化曲率 κ̃=κℓ_P, τ̃=τℓ_P ⇒")
print("        κ̃²+τ̃²=(ωℓ_P/c)² 两端均无量纲，自洽；等价于 κ²+τ²=(ω/c)²=k²")
print("  建议全书统一采用归一化写法，字面式仅作为'物理直觉'使用。")

print()
print("="*78)
print(" [B] 宇宙学参数核对（Planck 2018, TT+TE+EE+lowE+lensing+BAO）")
print("="*78)
Ob_h2 = mp.mpf("0.02242")   # 重子密度
Oc_h2 = mp.mpf("0.11933")   # 冷暗物质密度
h_pl  = mp.mpf("0.6736")    # h=H0/(100km/s/Mpc)
H0_pl = 100*h_pl
ns    = mp.mpf("0.9649")    # 标量谱指数
s8    = mp.mpf("0.8111")    # 密度涨落振幅
OL    = mp.mpf("0.6847")    # 暗能量密度参数
Om    = mp.mpf("0.3153")    # 物质密度参数
age   = mp.mpf("13.797")    # 宇宙年龄 Gyr
print(f"  Ω_b h² = {Ob_h2},  Ω_c h² = {Oc_h2}")
print(f"  Ω_b+Ω_c (h²加权) = {mp.nstr(Ob_h2+Oc_h2, 6)}")
print(f"  H0 = {H0_pl} km/s/Mpc,  h = {h_pl}")
print(f"  n_s = {ns},  σ8 = {s8},  Ω_Λ = {OL},  Ω_m = {Om}")
print(f"  Ω_m+Ω_Λ = {mp.nstr(Om+OL, 6)}  （平坦宇宙应≈1）")
print(f"  宇宙年龄 = {age} Gyr")
# 物质-辐射等量时代（近似）: z_eq ≈ 2.4e4 Ω_m h²
Om_h2 = Om*h_pl**2
z_eq = mp.mpf("2.4e4")*Om_h2
print(f"  物质-辐射等量红移 z_eq ≈ 2.4e4·Ω_m h² = {mp.nstr(z_eq, 6)}（量级 ~3400，与 Planck 一致）")
# 哈勃年龄(近似) 1/H0 换算
H0_s = H0_pl*mp.mpf("1000")/(mp.mpf("3.08567758e22"))  # km/s/Mpc→1/s (1Mpc=3.0857e22 m)
Hubble_time_Gyr = (1/H0_s)/(mp.mpf("3.15576e16"))      # 1秒→年: 3.15576e7; 1Gyr=3.15576e16s
print(f"  哈勃时间 1/H0 = {mp.nstr(Hubble_time_Gyr, 6)} Gyr")
print(f"  年龄/哈勃时间 = {mp.nstr(age/Hubble_time_Gyr, 6)}（ΛCDM 中≈0.96）")

print()
print("="*78)
print(" [C] 普朗克归一化的几何-频率关系数值示例")
print("="*78)
lP = mp.sqrt(mp.mpf("6.67430e-11")*mp.mpf("1.054571817e-34")/mp.mpf("299792458")**3)
cval = mp.mpf("299792458")
# 取光子能量 1 eV 对应角频率 ω=E/ħ
E_eV = mp.mpf("1"); eV_J = mp.mpf("1.602176634e-19")
hbar = mp.mpf("1.054571817e-34")
w = E_eV*eV_J/hbar
k = w/cval
k_lP = k*lP
print(f"  1 eV 光子：ω = {mp.nstr(w, 6)} rad/s")
print(f"  波数 k=ω/c = {mp.nstr(k, 6)} 1/m")
print(f"  k·ℓ_P = {mp.nstr(k_lP, 6)}（普朗克归一化波数，无量纲）")
print(f"  ⇒ 若 κ²+τ²=k² 且 κ≈τ（等权螺旋）：κ≈τ≈k/√2 = {mp.nstr(k/mp.sqrt(mp.mpf(2)), 6)} 1/m")
print(f"  框架内容：'频率决定几何'——能量越高，世界线弯曲密度越大。")
print(f"  注意：这描述了'几何与频率的对应'，是否由此导出引力/电磁力需独立推导（OPEN）。")
print()
print("量纲审计与数值验证完成。见附录 C 与 code/verify_geometry.py。")
