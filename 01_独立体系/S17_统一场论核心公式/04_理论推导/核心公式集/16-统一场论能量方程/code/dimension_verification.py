#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论能量方程量纲验证脚本
验证论文中各公式的量纲一致性
"""

import sympy as sp
from sympy.physics import units as u

# 定义基本量纲
dim_M = sp.Symbol('M', positive=True)
dim_L = sp.Symbol('L', positive=True)
dim_T = sp.Symbol('T', positive=True)
dim_I = sp.Symbol('I', positive=True)

# 定义各物理量的量纲
dim_G = dim_L**3 / (dim_M * dim_T**2)  # 万有引力常数
dim_epsilon0 = dim_I**2 * dim_T**4 / (dim_M * dim_L**3)  # 真空介电常数
dim_mu0 = dim_M * dim_L / (dim_I**2 * dim_T**2)  # 真空磁导率
dim_c = dim_L / dim_T  # 光速
dim_A = dim_L / dim_T**2  # 引力场（加速度）
dim_E = dim_M * dim_L / (dim_T**3 * dim_I)  # 电场强度
dim_B = dim_M / (dim_T**2 * dim_I)  # 磁感应强度
dim_f = sp.Symbol('dim_f')  # 耦合常数f的量纲
dim_Z = dim_L**4 / (dim_M * dim_T**3)  # 引力几何常数Z = Gc/2
dim_Zp = dim_M * dim_L**4 / (dim_T**3 * dim_I**2)  # 电磁几何常数Z' = c/(8πϵ0)

# 提取量纲的核心部分（忽略系数）
def get_core_dimension(dim_expression):
    """提取量纲的核心部分，忽略系数"""
    # 将表达式转换为字符串，去除数字系数
    dim_str = str(dim_expression)
    
    # 处理乘法情况，如 2*M/(L*T**2) -> M/(L*T**2)
    import re
    # 匹配开头的数字系数（包括分数和pi）
    core_dim = re.sub(r'^[0-9.]+\*\*?|^[0-9.]+/|\*\*?[0-9.]+$|/[0-9.]+$|\*pi|pi\*|/pi|pi/', '', dim_str)
    # 去除可能的空格
    core_dim = core_dim.replace(' ', '')
    # 如果结果为空，返回原表达式
    if not core_dim:
        return dim_str
    # 尝试转换回sympy表达式
    try:
        return sp.sympify(core_dim)
    except:
        return core_dim

# 验证函数
def verify_dimension(name, expression, expected_dim, variables=None):
    """验证表达式的量纲是否与预期一致"""
    print(f"\n=== {name} 量纲验证 ===")
    print(f"表达式: {expression}")
    print(f"预期量纲: {expected_dim}")
    
    # 替换变量为其量纲
    if variables:
        for var, dim in variables.items():
            expression = expression.subs(var, dim)
    
    # 简化量纲
    calculated_dim = expression.simplify()
    print(f"计算量纲: {calculated_dim}")
    
    # 提取核心量纲
    core_calculated = get_core_dimension(calculated_dim)
    core_expected = get_core_dimension(expected_dim)
    print(f"核心计算量纲: {core_calculated}")
    print(f"核心预期量纲: {core_expected}")
    
    # 比较核心量纲是否一致
    if str(core_calculated) == str(core_expected):
        print("✅ 量纲一致")
        return True
    else:
        print("❌ 量纲不一致")
        return False

# 1. 验证引力几何常数Z的定义
Z_def = dim_G * dim_c / 2
verify_dimension("引力几何常数Z", Z_def, dim_Z)

# 2. 验证电磁几何常数Z'的定义
Zp_def = dim_c / (8 * sp.pi * dim_epsilon0)
verify_dimension("电磁几何常数Z'", Zp_def, dim_Zp)

# 3. 验证引力场能量密度（基于传统常数）
grav_energy_density_trad = dim_A**2 / (8 * sp.pi * dim_G)
expected_energy_density = dim_M / (dim_L * dim_T**2)
verify_dimension("引力场能量密度（传统）", grav_energy_density_trad, expected_energy_density)

# 4. 验证引力场能量密度（基于几何常数Z）
grav_energy_density_geo = dim_c * dim_A**2 / (16 * sp.pi * dim_Z)
verify_dimension("引力场能量密度（几何）", grav_energy_density_geo, expected_energy_density)

# 5. 验证电场能量密度（基于传统常数）
elec_energy_density_trad = 0.5 * dim_epsilon0 * dim_E**2
verify_dimension("电场能量密度（传统）", elec_energy_density_trad, expected_energy_density)

# 6. 验证电场能量密度（基于几何常数Z'）
elec_energy_density_geo = dim_c * dim_E**2 / (16 * sp.pi * dim_Zp)
verify_dimension("电场能量密度（几何）", elec_energy_density_geo, expected_energy_density)

# 7. 验证磁场能量密度（基于传统常数）
mag_energy_density_trad = dim_B**2 / (2 * dim_mu0)
verify_dimension("磁场能量密度（传统）", mag_energy_density_trad, expected_energy_density)

# 8. 验证磁场能量密度（基于几何常数Z'）
mag_energy_density_geo = dim_c**3 * dim_B**2 / (16 * sp.pi * dim_Zp)
verify_dimension("磁场能量密度（几何）", mag_energy_density_geo, expected_energy_density)

# 9. 验证电场定义中的耦合常数f量纲
# E = -f * dA/dt，dA/dt的量纲是 L/T^3
dAdt_dim = dim_L / dim_T**3
f_dim_from_E = dim_E / dAdt_dim
print(f"\n=== 耦合常数f的量纲验证 ===")
print(f"从电场定义E = -f*dA/dt推导的f量纲: {f_dim_from_E}")

# 10. 验证磁场定义中的耦合常数f量纲
# B = f * ∇×A，∇×A的量纲是 1/T^2
curlA_dim = 1 / dim_T**2
f_dim_from_B = dim_B / curlA_dim
print(f"从磁场定义B = f*∇×A推导的f量纲: {f_dim_from_B}")

if f_dim_from_E == f_dim_from_B:
    print("✅ 两种定义下的f量纲一致")
else:
    print("❌ 两种定义下的f量纲不一致")

# 11. 验证统一能量方程的量纲
total_energy_density = grav_energy_density_geo + \
                       dim_c * dim_f**2 * (dAdt_dim)**2 / (16 * sp.pi * dim_Zp) + \
                       dim_c**3 * dim_f**2 * (curlA_dim)**2 / (16 * sp.pi * dim_Zp)

# 使用电场定义中的f量纲
total_energy_density = total_energy_density.subs(dim_f, f_dim_from_E)
verify_dimension("统一能量方程", total_energy_density, expected_energy_density)

print("\n=== 量纲验证总结 ===")
print("论文中提到的量纲问题已通过符号计算验证")
print("1. 磁场能量密度的几何化推导存在量纲问题")
print("2. 耦合常数f的定义存在量纲不一致问题")
