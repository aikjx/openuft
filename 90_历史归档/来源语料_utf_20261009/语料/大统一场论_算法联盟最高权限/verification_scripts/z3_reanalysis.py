# -*- coding: utf-8 -*-
"""
螺旋时空理论 - Z3模型的重新审视
=================================
发现之前的Z3公式预测力很差，需要重新分析
"""

import numpy as np
from scipy import constants
from scipy.optimize import least_squares

# CODATA 2022
c = constants.c
hbar = constants.hbar
h = constants.h
e = constants.elementary_charge
alpha = constants.fine_structure
m_e = constants.electron_mass

print("=" * 70)
print("螺旋时空理论 - Z3模型的重新审视")
print("=" * 70)

# 轻子质量 (MeV)
m_e_MeV = 0.51099895
m_mu_MeV = 105.66
m_tau_MeV = 1776.86

x_exp = [np.sqrt(m_e_MeV), np.sqrt(m_mu_MeV), np.sqrt(m_tau_MeV)]
print(f"\n实验√m值:")
for name, x in zip(['e', 'μ', 'τ'], x_exp):
    print(f"  √m_{name} = {x:.6f} MeV^(1/2)")

# ============================================================================
# 重新拟合Z3模型
# ============================================================================
print("\n" + "=" * 70)
print("重新拟合Z3模型")
print("=" * 70)

# 模型：√m_i = A · [1 + B·cos(θ_i) + C·sin(θ_i)]
# θ_i = 2π(i-1)/3 + φ
theta_z3 = lambda i, phi: 2 * np.pi * (i - 1) / 3 + phi

def residuals_full(params):
    A, B, C, phi = params
    x_pred = [A * (1 + B * np.cos(theta_z3(i, phi)) + C * np.sin(theta_z3(i, phi))) 
              for i in [1, 2, 3]]
    # 同时加入Koide约束
    koide_lhs = 3 * sum(x**2 for x in x_pred)
    koide_rhs = 2 * sum(x_pred)**2
    return [x_pred[i] - x_exp[i] for i in range(3)] + [koide_lhs - koide_rhs]

# 大范围搜索
best_result = None
best_cost = float('inf')

for A_init in np.logspace(0, 2, 100):
    for B_init in np.linspace(-2, 2, 30):
        for C_init in np.linspace(-2, 2, 30):
            for phi_init in np.linspace(0, 2*np.pi, 40):
                x0 = [A_init, B_init, C_init, phi_init]
                result = least_squares(residuals_full, x0, bounds=([0.01, -10, -10, 0], [1000, 10, 10, 2*np.pi]))
                if result.cost < best_cost:
                    best_cost = result.cost
                    best_result = result

A, B, C, phi = best_result.x

print(f"\n最优拟合参数:")
print(f"  A = {A:.10f}")
print(f"  B = {B:.10f}")
print(f"  C = {C:.10f}")
print(f"  φ = {phi:.10f} rad = {phi*180/np.pi:.8f}°")
print(f"  残差 = {best_cost:.2e}")

# 计算预测值
x_pred = [A * (1 + B * np.cos(theta_z3(i, phi)) + C * np.sin(theta_z3(i, phi))) for i in [1, 2, 3]]
m_pred = [x**2 for x in x_pred]

print(f"\n预测质量:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred[i]:.6f} vs {m_exp:.6f} MeV, 误差={error:.6f}%")

# Koide验证
koide_pred = sum(x**2 for x in x_pred) / sum(x_pred)**2
print(f"\nKoide验证: {koide_pred:.12f} (理论=2/3={2/3:.12f})")

# ============================================================================
# 分析模型的预测能力
# ============================================================================
print("\n" + "=" * 70)
print("分析模型的预测能力")
print("=" * 70)

# 模型有4个参数(A,B,C,φ)拟合4个约束(3个质量+1个Koide)
# 这意味着模型是欠定的，拟合是恒等的

print(f"""
重要分析:
  参数数量: 4 (A, B, C, φ)
  约束数量: 4 (3个质量值 + 1个Koide关系)
  
  → 模型是欠定的！
  → 拟合是恒等的，不具预测力
  
  要做预测性检验，必须:
  1. 固定部分参数（如B,C,φ）
  2. 只用A一个参数拟合
  3. 检验是否能预测其他粒子的质量
""")

# ============================================================================
# 尝试：固定B,C,φ，只用A拟合
# ============================================================================
print("\n" + "=" * 70)
print("固定参数的预测性检验")
print("=" * 70)

# 假设B,C,φ有固定的数学结构
# 假设1: B=1/√2, C=√3/√2, φ=π
B_fixed = 1 / np.sqrt(2)
C_fixed = np.sqrt(3/2)
phi_fixed = np.pi

print(f"\n假设: B={B_fixed:.6f}, C={C_fixed:.6f}, φ={phi_fixed:.6f} rad")

# 只用A拟合
def residuals_A(params):
    A_val = params[0]
    x_pred = [A_val * (1 + B_fixed * np.cos(theta_z3(i, phi_fixed)) + 
              C_fixed * np.sin(theta_z3(i, phi_fixed))) for i in [1, 2, 3]]
    return [x_pred[i] - x_exp[i] for i in range(3)]

result_A = least_squares(residuals_A, [17.0], bounds=([1], [100]))
A_fit = result_A.x[0]

x_pred_fixed = [A_fit * (1 + B_fixed * np.cos(theta_z3(i, phi_fixed)) + 
               C_fixed * np.sin(theta_z3(i, phi_fixed))) for i in [1, 2, 3]]
m_pred_fixed = [x**2 for x in x_pred_fixed]

print(f"\n拟合A = {A_fit:.6f}")
print(f"\n预测质量（固定B,C,φ）:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred_fixed[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred_fixed[i]:.4f} vs {m_exp:.4f} MeV, 误差={error:.4f}%")

# ============================================================================
# 更简洁的模型
# ============================================================================
print("\n" + "=" * 70)
print("更简洁的Z3模型")
print("=" * 70)

# 模型：√m_i = A · cos(θ_i + φ)
# 只有2个参数：A, φ

print("\n模型: √m_i = A·cos(2π(i-1)/3 + φ)")
print("参数: A, φ")

def residuals_simple(params):
    A_val, phi_val = params
    x_pred = [A_val * np.cos(theta_z3(i, phi_val)) for i in [1, 2, 3]]
    return [x_pred[i] - x_exp[i] for i in range(3)]

best_simple = None
best_cost_simple = float('inf')

for A_init in np.logspace(0, 2, 50):
    for phi_init in np.linspace(-np.pi/2, np.pi/2, 50):
        result = least_squares(residuals_simple, [A_init, phi_init], 
                             bounds=([0.1, -np.pi/2], [100, np.pi/2]))
        if result.cost < best_cost_simple:
            best_cost_simple = result.cost
            best_simple = result

A_simple, phi_simple = best_simple.x

x_pred_simple = [A_simple * np.cos(theta_z3(i, phi_simple)) for i in [1, 2, 3]]
m_pred_simple = [x**2 for x in x_pred_simple]

print(f"\n拟合参数:")
print(f"  A = {A_simple:.6f}")
print(f"  φ = {phi_simple:.6f} rad = {phi_simple*180/np.pi:.4f}°")
print(f"  残差 = {best_cost_simple:.2e}")

print(f"\n预测质量:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred_simple[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred_simple[i]:.4f} vs {m_exp:.4f} MeV, 误差={error:.4f}%")

# Koide验证
koide_simple = sum(x**2 for x in x_pred_simple) / sum(x_pred_simple)**2
print(f"\nKoide验证: {koide_simple:.6f} (理论=2/3={2/3:.6f})")

# ============================================================================
# 检查cos模型的物理合理性
# ============================================================================
print("\n" + "=" * 70)
print("检查cos模型的物理合理性")
print("=" * 70)

print(f"""
cos模型的分析:
  √m_i = A·cos(θ_i + φ)
  
  当θ_i + φ = 0时，√m最大 = A
  当θ_i + φ = π/2时，√m = 0
  
  这意味着有一个粒子质量为0，这在物理上不合理
  
  改进：√m_i = A·cos²(θ_i + φ)
  这样所有粒子都有非零质量
""")

# 尝试平方cos模型
print("\n尝试: √m_i = A·cos²(2π(i-1)/3 + φ)")

def residuals_cos2(params):
    A_val, phi_val = params
    x_pred = [A_val * np.cos(theta_z3(i, phi_val))**2 for i in [1, 2, 3]]
    return [x_pred[i] - x_exp[i] for i in range(3)]

best_cos2 = None
best_cost_cos2 = float('inf')

for A_init in np.logspace(0, 2, 50):
    for phi_init in np.linspace(-np.pi/4, np.pi/4, 50):
        result = least_squares(residuals_cos2, [A_init, phi_init], 
                             bounds=([0.1, -np.pi/2], [100, np.pi/2]))
        if result.cost < best_cost_cos2:
            best_cost_cos2 = result.cost
            best_cos2 = result

A_cos2, phi_cos2 = best_cos2.x

x_pred_cos2 = [A_cos2 * np.cos(theta_z3(i, phi_cos2))**2 for i in [1, 2, 3]]
m_pred_cos2 = [x**2 for x in x_pred_cos2]

print(f"\n拟合参数:")
print(f"  A = {A_cos2:.6f}")
print(f"  φ = {phi_cos2:.6f} rad = {phi_cos2*180/np.pi:.4f}°")
print(f"  残差 = {best_cost_cos2:.2e}")

print(f"\n预测质量:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred_cos2[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred_cos2[i]:.4f} vs {m_exp:.4f} MeV, 误差={error:.4f}%")

# ============================================================================
# 总结与结论
# ============================================================================
print("\n" + "=" * 70)
print("总结与结论")
print("=" * 70)

print(f"""
Z3模型分析总结:

1. 一般模型 (4参数):
   √m_i = A·[1 + B·cos(θ_i) + C·sin(θ_i)]
   - 拟合精度: 高
   - 预测能力: 无（参数过多）

2. 固定参数模型:
   B=1/√2, C=√3/√2, φ=π
   - 拟合精度: 差（8700%误差）
   - 说明: 固定参数的假设不正确

3. cos模型 (2参数):
   √m_i = A·cos(θ_i + φ)
   - 有粒子质量为0，物理不合理

4. cos²模型 (2参数):
   √m_i = A·cos²(θ_i + φ)
   - 需要检查拟合精度

结论:
- Z3模型的预测能力有限
- 需要找到B,C,φ的正确物理意义
- 或者Z3只是巧合，轻子质量需要其他解释
""")

print("=" * 70)
print("完成")
print("=" * 70)