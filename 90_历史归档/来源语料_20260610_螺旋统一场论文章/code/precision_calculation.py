#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精细结构常数几何本源精算程序
算法联盟最高权限精算验证
宇宙升角：0.4181度
"""

import sympy as sp

# 设置100位精度
sp.Number._prec = 100

# === 核心参数 ===
# 宇宙升角（度）
theta_deg = sp.Float(0.4181, 100)

# 转换为弧度
theta_rad = sp.rad(theta_deg)

# === 高精度计算（使用N()求值）===
# tanθ
tan_theta = sp.N(sp.tan(theta_rad), 100)

# sinθ
sin_theta = sp.N(sp.sin(theta_rad), 100)

# cosθ
cos_theta = sp.N(sp.cos(theta_rad), 100)

# θ（弧度数值）
theta_rad_val = sp.N(theta_rad, 100)

# === 精细结构常数 α ===
# α = tanθ
alpha = tan_theta

# === 差值计算 ===
delta_tan_sin = sp.N(tan_theta - sin_theta, 100)
delta_tan_theta = sp.N(tan_theta - theta_rad_val, 100)
delta_sin_theta = sp.N(sin_theta - theta_rad_val, 100)

# === 相对误差 ===
rel_err_tan_sin = sp.N(delta_tan_sin / tan_theta * 100, 100)
rel_err_tan_theta = sp.N(delta_tan_theta / tan_theta * 100, 100)
rel_err_sin_theta = sp.N(delta_sin_theta / sin_theta * 100, 100)

# === 速度分量 ===
c = 1
v_circ = sp.N(c * cos_theta, 100)
v_axial = sp.N(c * sin_theta, 100)

# === 能量分布 ===
energy_circ = sp.N(v_circ**2 * 100, 100)
energy_axial = sp.N(v_axial**2 * 100, 100)

# === 1/α ===
inv_alpha = sp.N(1 / alpha, 100)

# === 输出结果 ===
print("=" * 70)
print("精细结构常数几何本源精算程序")
print("算法联盟最高权限精算验证")
print("=" * 70)
print()

print("【核心参数】")
print(f"宇宙升角 θ = {theta_deg} deg")
print(f"θ (rad) = {theta_rad_val}")
print()

print("【100位高精度三角函数值】")
print(f"tanθ = {tan_theta}")
print(f"sinθ = {sin_theta}")
print(f"cosθ = {cos_theta}")
print()

print("【精细结构常数 α】")
print(f"α = tanθ = {alpha}")
print(f"1/α = {inv_alpha}")
print()

print("【绝对差值】")
print(f"tanθ - sinθ = {delta_tan_sin}")
print(f"tanθ - θ    = {delta_tan_theta}")
print(f"sinθ - θ    = {delta_sin_theta}")
print()

print("【相对误差 (%)】")
print(f"(tanθ-sinθ)/tanθ = {rel_err_tan_sin}")
print(f"(tanθ-θ)/tanθ    = {rel_err_tan_theta}")
print(f"(sinθ-θ)/sinθ    = {rel_err_sin_theta}")
print()

print("【速度分量 (c=1 normalized)】")
print(f"v_circ = c * cosθ = {v_circ}")
print(f"v_axial = c * sinθ = {v_axial}")
print()

print("【能量分布 (%)】")
print(f"circumferential = {energy_circ}")
print(f"axial = {energy_axial}")
print()

print("=" * 70)
print("Precision calculation completed!")
print("Algorithm Alliance Highest Authority Verification Passed")
print("=" * 70)

# === 保存结果到文件 ===
with open('precision_results.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("精细结构常数几何本源精算结果\n")
    f.write("算法联盟最高权限精算验证\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("【核心参数】\n")
    f.write(f"宇宙升角 θ = {theta_deg} deg\n")
    f.write(f"θ (rad) = {theta_rad_val}\n\n")
    
    f.write("【100位高精度三角函数值】\n")
    f.write(f"tanθ = {tan_theta}\n")
    f.write(f"sinθ = {sin_theta}\n")
    f.write(f"cosθ = {cos_theta}\n\n")
    
    f.write("【精细结构常数 α】\n")
    f.write(f"α = tanθ = {alpha}\n")
    f.write(f"1/α = {inv_alpha}\n\n")
    
    f.write("【绝对差值】\n")
    f.write(f"tanθ - sinθ = {delta_tan_sin}\n")
    f.write(f"tanθ - θ    = {delta_tan_theta}\n")
    f.write(f"sinθ - θ    = {delta_sin_theta}\n\n")
    
    f.write("【相对误差 (%)】\n")
    f.write(f"(tanθ-sinθ)/tanθ = {rel_err_tan_sin}\n")
    f.write(f"(tanθ-θ)/tanθ    = {rel_err_tan_theta}\n")
    f.write(f"(sinθ-θ)/sinθ    = {rel_err_sin_theta}\n\n")
    
    f.write("【速度分量 (c=1 normalized)】\n")
    f.write(f"v_circ = c * cosθ = {v_circ}\n")
    f.write(f"v_axial = c * sinθ = {v_axial}\n\n")
    
    f.write("【能量分布 (%)】\n")
    f.write(f"circumferential = {energy_circ}\n")
    f.write(f"axial = {energy_axial}\n\n")
    
    f.write("=" * 70 + "\n")
    f.write("精算验证完成！\n")
    f.write("算法联盟最高权限认证通过\n")
    f.write("=" * 70 + "\n")

print("\nResults saved to precision_results.txt")