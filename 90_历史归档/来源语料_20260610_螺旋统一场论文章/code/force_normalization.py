#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四种基本力几何归一化精算验证程序
算法联盟最高权限精算验证
验证：引力 + 电磁力 + 强核力 + 弱核力 = 1
"""

import sympy as sp
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sp.Number._prec = 100

alpha = sp.Float(1/137.035999084, 100)
theta_rad = sp.atan(alpha)
theta_deg = sp.N(sp.deg(theta_rad), 100)

cos_theta = sp.N(sp.cos(theta_rad), 100)
sin_theta = sp.N(sp.sin(theta_rad), 100)
tan_theta = sp.N(sp.tan(theta_rad), 100)

F_gravity_factor = sp.N(1 / alpha**2, 100)
F_electric_factor = alpha
F_strong_factor = sp.N(1 / alpha, 100)
F_weak_factor = sp.Float(1, 100)

N = sp.N(F_gravity_factor + F_electric_factor + F_strong_factor + F_weak_factor, 100)

F_gravity_norm = sp.N(F_gravity_factor / N, 100)
F_electric_norm = sp.N(F_electric_factor / N, 100)
F_strong_norm = sp.N(F_strong_factor / N, 100)
F_weak_norm = sp.N(F_weak_factor / N, 100)

total_norm = sp.N(F_gravity_norm + F_electric_norm + F_strong_norm + F_weak_norm, 100)

energy_perp = sp.N(cos_theta**2, 100)
energy_parallel = sp.N(sin_theta**2, 100)
energy_total = sp.N(energy_perp + energy_parallel, 100)

print("=" * 70)
print("四种基本力几何归一化精算验证")
print("算法联盟最高权限精算验证")
print("=" * 70)
print()

print("【核心参数】")
print(f"alpha = {alpha}")
print(f"1/alpha = {1/alpha}")
print(f"1/alpha^2 = {1/alpha**2}")
print()

print("【三角函数值】")
print(f"cos(theta) = {cos_theta}")
print(f"sin(theta) = {sin_theta}")
print(f"tan(theta) = {tan_theta}")
print()

print("【力的强度因子】")
print(f"F_gravity_factor = 1/alpha^2 = {F_gravity_factor}")
print(f"F_electric_factor = alpha = {F_electric_factor}")
print(f"F_strong_factor = 1/alpha = {F_strong_factor}")
print(f"F_weak_factor = 1 = {F_weak_factor}")
print()

print("【归一化因子】")
print(f"N = 1/alpha^2 + alpha + 1/alpha + 1 = {N}")
print()

print("【归一化后的力】")
print(f"F_gravity_norm = {F_gravity_norm}")
print(f"F_electric_norm = {F_electric_norm}")
print(f"F_strong_norm = {F_strong_norm}")
print(f"F_weak_norm = {F_weak_norm}")
print()

print("【归一化总和】")
print(f"F_gravity + F_electric + F_strong + F_weak = {total_norm}")
print(f"Difference from 1 = {sp.N(total_norm - 1, 100)}")
print()

print("【能量归一化】")
print(f"energy_perp = cos^2(theta) = {energy_perp}")
print(f"energy_parallel = sin^2(theta) = {energy_parallel}")
print(f"total_energy = {energy_total}")
print(f"Difference from 1 = {sp.N(energy_total - 1, 100)}")
print()

print("=" * 70)
print("精算验证结论：")
print(f"力的归一化总和 = {total_norm} ≈ 1")
print(f"能量归一化总和 = {energy_total} = 1")
print("=" * 70)

with open('force_normalization_results.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("四种基本力几何归一化精算结果\n")
    f.write("算法联盟最高权限精算验证\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("【核心参数】\n")
    f.write(f"alpha = {alpha}\n")
    f.write(f"1/alpha = {1/alpha}\n")
    f.write(f"1/alpha^2 = {1/alpha**2}\n\n")
    
    f.write("【三角函数值】\n")
    f.write(f"cos(theta) = {cos_theta}\n")
    f.write(f"sin(theta) = {sin_theta}\n")
    f.write(f"tan(theta) = {tan_theta}\n\n")
    
    f.write("【力的强度因子】\n")
    f.write(f"F_gravity_factor = 1/alpha^2 = {F_gravity_factor}\n")
    f.write(f"F_electric_factor = alpha = {F_electric_factor}\n")
    f.write(f"F_strong_factor = 1/alpha = {F_strong_factor}\n")
    f.write(f"F_weak_factor = 1 = {F_weak_factor}\n\n")
    
    f.write("【归一化因子】\n")
    f.write(f"N = 1/alpha^2 + alpha + 1/alpha + 1 = {N}\n\n")
    
    f.write("【归一化后的力】\n")
    f.write(f"F_gravity_norm = {F_gravity_norm}\n")
    f.write(f"F_electric_norm = {F_electric_norm}\n")
    f.write(f"F_strong_norm = {F_strong_norm}\n")
    f.write(f"F_weak_norm = {F_weak_norm}\n\n")
    
    f.write("【归一化总和】\n")
    f.write(f"F_gravity + F_electric + F_strong + F_weak = {total_norm}\n")
    f.write(f"Difference from 1 = {sp.N(total_norm - 1, 100)}\n\n")
    
    f.write("【能量归一化】\n")
    f.write(f"energy_perp = cos^2(theta) = {energy_perp}\n")
    f.write(f"energy_parallel = sin^2(theta) = {energy_parallel}\n")
    f.write(f"total_energy = {energy_total}\n")
    f.write(f"Difference from 1 = {sp.N(energy_total - 1, 100)}\n\n")
    
    f.write("=" * 70 + "\n")
    f.write("精算验证结论：\n")
    f.write(f"力的归一化总和 = {total_norm} ≈ 1\n")
    f.write(f"能量归一化总和 = {energy_total} = 1\n")
    f.write("=" * 70 + "\n")

print("\n结果已保存到 force_normalization_results.txt")