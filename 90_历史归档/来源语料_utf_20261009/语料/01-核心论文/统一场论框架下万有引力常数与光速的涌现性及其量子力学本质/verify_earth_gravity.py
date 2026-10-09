#!/usr/bin/env python3
"""
验证地球表面重力加速度的计算
"""

# 地球基本参数
M = 5.972e24  # kg，地球质量
R = 6.371e6  # m，地球平均半径
g_exp = 9.81  # m/s²，实际测量的地球表面重力加速度

# 统一场论计算的万有引力常数
G_theo = 6.6743021e-11  # m³·kg⁻¹·s⁻²

print("=== 地球表面重力加速度计算验证 ===")
print(f"地球质量 M = {M:.4e} kg")
print(f"地球平均半径 R = {R:.4e} m")
print(f"实际测量重力加速度 g_exp = {g_exp} m/s²")
print(f"统一场论计算的万有引力常数 G_theo = {G_theo:.8e} m³·kg⁻¹·s⁻²")

# 计算分子
print(f"\n=== 分步计算 ===")
numerator = G_theo * M
print(f"分子 G_theo * M = {numerator:.4e} m³·s⁻²")

# 计算分母
denominator = R ** 2
print(f"分母 R² = {denominator:.4e} m²")

# 计算理论重力加速度
g_theo = numerator / denominator
print(f"理论重力加速度 g_theo = {g_theo:.6f} m/s²")

# 计算相对误差
relative_error = abs((g_theo - g_exp) / g_exp) * 100
print(f"相对误差 = {relative_error:.6f}%")

# 与论文结果比较
print(f"\n=== 结果比较 ===")
paper_g_theo = 9.81998  # m/s²，论文中理论重力加速度
paper_relative_error = 0.1017  # %，论文中相对误差

print(f"论文中理论重力加速度: {paper_g_theo} m/s²")
print(f"Python计算理论重力加速度: {g_theo:.6f} m/s²")
print(f"理论重力加速度一致: {abs(g_theo - paper_g_theo) < 1e-5}")

print(f"\n论文中相对误差: {paper_relative_error}%")
print(f"Python计算相对误差: {relative_error:.6f}%")
print(f"相对误差一致: {abs(relative_error - paper_relative_error) < 1e-4}")

# 额外验证：使用更精确的计算
print(f"\n=== 更精确的计算结果 ===")
print(f"分子 G_theo * M = {G_theo * M:.12e} m³·s⁻²")
print(f"分母 R² = {R ** 2:.12e} m²")
print(f"理论重力加速度 g_theo = {g_theo:.12f} m/s²")
print(f"相对误差 = {relative_error:.12f}%")
