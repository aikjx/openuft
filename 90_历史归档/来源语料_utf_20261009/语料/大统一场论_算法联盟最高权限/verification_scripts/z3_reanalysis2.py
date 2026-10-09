# -*- coding: utf-8 -*-
"""
螺旋时空理论 - Z3模型的简化分析
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
print("螺旋时空理论 - Z3模型的简化分析")
print("=" * 70)

# 轻子质量 (MeV)
m_e_MeV = 0.51099895
m_mu_MeV = 105.66
m_tau_MeV = 1776.86

x_exp = [np.sqrt(m_e_MeV), np.sqrt(m_mu_MeV), np.sqrt(m_tau_MeV)]
print(f"\n实验√m值:")
for name, x in zip(['e', 'μ', 'τ'], x_exp):
    print(f"  √m_{name} = {x:.6f} MeV^(1/2)")

theta_z3 = lambda i, phi: 2 * np.pi * (i - 1) / 3 + phi

# ============================================================================
# 模型1: 4参数一般模型
# ============================================================================
print("\n" + "=" * 70)
print("模型1: 4参数一般模型")
print("√m_i = A·[1 + B·cos(θ_i) + C·sin(θ_i)]")
print("=" * 70)

def residuals_4param(params):
    A, B, C, phi = params
    x_pred = [A * (1 + B * np.cos(theta_z3(i, phi)) + C * np.sin(theta_z3(i, phi))) 
              for i in [1, 2, 3]]
    koide_lhs = 3 * sum(x**2 for x in x_pred)
    koide_rhs = 2 * sum(x_pred)**2
    return [x_pred[i] - x_exp[i] for i in range(3)] + [koide_lhs - koide_rhs]

# 使用多起点，但更高效
best_result = None
best_cost = float('inf')

# 更智能的初始点
initial_points = [
    [17.7, 1/np.sqrt(2), np.sqrt(3/2), np.pi],
    [17.7, 0.7, 1.2, 3.14],
    [17.7, 1.0, 1.0, 3.5],
    [15, 0.5, 1.5, 2.5],
    [20, 0.8, 1.0, 4.0],
]

for x0 in initial_points:
    result = least_squares(residuals_4param, x0, bounds=([0.1, -10, -10, 0], [1000, 10, 10, 2*np.pi]))
    if result.cost < best_cost:
        best_cost = result.cost
        best_result = result

A, B, C, phi = best_result.x

print(f"\n最优参数:")
print(f"  A = {A:.10f}")
print(f"  B = {B:.10f}")
print(f"  C = {C:.10f}")
print(f"  φ = {phi:.10f} rad = {phi*180/np.pi:.8f}°")
print(f"  残差 = {best_cost:.2e}")

# 预测
x_pred = [A * (1 + B * np.cos(theta_z3(i, phi)) + C * np.sin(theta_z3(i, phi))) for i in [1, 2, 3]]
m_pred = [x**2 for x in x_pred]

print(f"\n预测质量:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred[i]:.6f} vs {m_exp:.6f} MeV, 误差={error:.6f}%")

koide_pred = sum(x**2 for x in x_pred) / sum(x_pred)**2
print(f"\nKoide: {koide_pred:.12f} (理论=2/3)")

# ============================================================================
# 模型2: 2参数简化模型
# ============================================================================
print("\n" + "=" * 70)
print("模型2: 2参数简化模型")
print("√m_i = A·cos²(θ_i + φ)")
print("=" * 70)

def residuals_cos2(params):
    A_val, phi_val = params
    x_pred = [A_val * np.cos(theta_z3(i, phi_val))**2 for i in [1, 2, 3]]
    return [x_pred[i] - x_exp[i] for i in range(3)]

best_cos2 = None
best_cost_cos2 = float('inf')

for A_init in [10, 20, 50, 100, 200]:
    for phi_init in np.linspace(-np.pi/3, np.pi/3, 20):
        result = least_squares(residuals_cos2, [A_init, phi_init], 
                             bounds=([0.1, -np.pi], [1000, np.pi]))
        if result.cost < best_cost_cos2:
            best_cost_cos2 = result.cost
            best_cos2 = result

A_cos2, phi_cos2 = best_cos2.x

x_pred_cos2 = [A_cos2 * np.cos(theta_z3(i, phi_cos2))**2 for i in [1, 2, 3]]
m_pred_cos2 = [x**2 for x in x_pred_cos2]

print(f"\n最优参数:")
print(f"  A = {A_cos2:.10f}")
print(f"  φ = {phi_cos2:.10f} rad = {phi_cos2*180/np.pi:.8f}°")
print(f"  残差 = {best_cost_cos2:.2e}")

print(f"\n预测质量:")
for i, (name, m_exp) in enumerate([('e', m_e_MeV), ('μ', m_mu_MeV), ('τ', m_tau_MeV)]):
    error = abs(m_pred_cos2[i] - m_exp) / m_exp * 100
    print(f"  {name}: {m_pred_cos2[i]:.6f} vs {m_exp:.6f} MeV, 误差={error:.6f}%")

koide_cos2 = sum(x**2 for x in x_pred_cos2) / sum(x_pred_cos2)**2
print(f"\nKoide: {koide_cos2:.12f} (理论=2/3)")

# ============================================================================
# 分析：模型的参数数量vs预测能力
# ============================================================================
print("\n" + "=" * 70)
print("分析：参数数量vs预测能力")
print("=" * 70)

print(f"""
模型对比:
  4参数模型: 
    参数: A, B, C, φ (4个参数)
    约束: 3个质量 + 1个Koide (4个约束)
    → 刚好拟合，无预测力
    
  2参数cos²模型:
    参数: A, φ (2个参数)
    约束: 3个质量 (3个约束)
    → 过定约束，有预测力！
    
关键问题：
  cos²模型能否同时拟合3个质量？
  如果不能，说明Z3模型需要更多参数或不同结构
""")

# ============================================================================
# 更深入的分析：Koide关系的结构
# ============================================================================
print("\n" + "=" * 70)
print("Koide关系的结构分析")
print("=" * 70)

print(f"""
Koide关系: Σm_i = (2/3)(Σ√m_i)²

设 x_i = √m_i，则:
  3Σx_i² = 2(Σx_i)²
  → Σx_i² = 4Σ_{{i<j}}x_ix_j
  → x₁² + x₂² + x₃² = 4(x₁x₂ + x₁x₃ + x₂x₃)

这是一个关于x_i的代数约束。
对于3个变量，它定义了一个曲面。

关键问题：
  轻子质量 (0.511, 105.66, 1776.86) MeV 是否在这个曲面上？
  答案：是（Koide关系成立）
  
  但这个曲面是否与Z3对称群有关？
  答案：不确定
  
  任何3个数都可以通过适当的A,B,C,φ拟合Z3模型
  这意味着Z3模型本质上没有物理内容
""")

# ============================================================================
# 真正的预测性检验
# ============================================================================
print("\n" + "=" * 70)
print("真正的预测性检验")
print("=" * 70)

print("""
要做真正的预测性检验，需要：

1. 用轻子质量拟合模型参数
2. 用这些参数预测其他粒子的质量
3. 检验预测值与实验值的吻合程度

但目前的Z3模型有4个参数，无法做预测。
我们需要一个有物理内容的模型。

可能的方向：
  1. 从第一性原理推导B,C,φ的值
  2. 找到B,C,φ与其他物理常数的关系
  3. 构建一个参数更少的模型

或者：
  放弃Z3模型，寻找其他解释Koide关系的途径
""")

# ============================================================================
# 夸克质量的Koide关系检验
# ============================================================================
print("\n" + "=" * 70)
print("夸克质量的Koide关系检验")
print("=" * 70)

# 夸克质量 (MeV)
m_u = 2.3
m_d = 4.7
m_s = 95.0
m_c = 1270.0
m_b = 4180.0
m_t = 172760.0

print("\n轻夸克 (u, d, s):")
x_light = [np.sqrt(m_u), np.sqrt(m_d), np.sqrt(m_s)]
sum_x_light = sum(x_light)
sum_x2_light = sum(x**2 for x in x_light)
koide_light = sum_x2_light / sum_x_light**2
print(f"  √m: [{x_light[0]:.4f}, {x_light[1]:.4f}, {x_light[2]:.4f}]")
print(f"  Koide = {koide_light:.6f} (理论=2/3={2/3:.6f})")
print(f"  误差 = {abs(koide_light - 2/3)/(2/3)*100:.2f}%")

print("\n重夸克 (c, b, t):")
x_heavy = [np.sqrt(m_c), np.sqrt(m_b), np.sqrt(m_t)]
sum_x_heavy = sum(x_heavy)
sum_x2_heavy = sum(x**2 for x in x_heavy)
koide_heavy = sum_x2_heavy / sum_x_heavy**2
print(f"  √m: [{x_heavy[0]:.4f}, {x_heavy[1]:.4f}, {x_heavy[2]:.4f}]")
print(f"  Koide = {koide_heavy:.6f} (理论=2/3={2/3:.6f})")
print(f"  误差 = {abs(koide_heavy - 2/3)/(2/3)*100:.2f}%")

print("\n所有6种夸克 (u, d, s, c, b, t):")
x_all = x_light + x_heavy
sum_x_all = sum(x_all)
sum_x2_all = sum(x**2 for x in x_all)
koide_all = sum_x2_all / sum_x_all**2
print(f"  Koide (6种) = {koide_all:.6f}")

# 6粒子的推广Koide关系
# 对于n个粒子，推广的Koide关系可能是：
# Σm_i = (n-1)/n · (Σ√m_i)²  (猜测)
koide_gen = sum_x2_all / sum_x_all**2
print(f"  推广Koide (n=6): (n-1)/n = {5/6:.6f}")
print(f"  实际: {koide_all:.6f}")

# ============================================================================
# 结论
# ============================================================================
print("\n" + "=" * 70)
print("结论")
print("=" * 70)

print(f"""
1. Z3模型的问题：
   - 4参数模型可以拟合任何3个质量值
   - 模型本质上没有物理内容
   - 需要找到参数的物理起源

2. Koide关系的状态：
   - 轻子: 成立 (误差~0.001%)
   - 重夸克: 近似成立 (误差~0.4%)
   - 轻夸克: 不成立 (误差~15%)
   - Koide关系不是普遍规律

3. 下一步方向：
   a. 研究为什么轻子满足Koide关系
   b. 研究重夸克近似满足的原因
   c. 放弃Z3模型，寻找其他几何框架
   d. 回到Dirac方程和α的推导

建议：
   重新聚焦于α的推导和Dirac方程的结构
   Z3模型作为辅助工具而非核心框架
""")

print("=" * 70)
print("完成")
print("=" * 70)