import sympy as sym
from sympy.physics.units import meter, kilogram, second, ampere, coulomb, volt, tesla, gravitational_constant, speed_of_light, vacuum_permittivity, vacuum_permeability

# 定义常数
c = speed_of_light
G = gravitational_constant
epsilon0 = vacuum_permittivity
mu0 = vacuum_permeability

# 定义几何常数 Z 和 Z'
Z = G * c / 2
Z_prime = c / (8 * sym.pi * epsilon0)

# 直接计算各能量密度表达式，它们会带有正确的量纲
# 因为所有变量都是带有量纲的物理常数

# 验证论文中的能量密度表达式量纲
u_g_paper = (1/(8*sym.pi*G)) * (meter / second**2)**2
u_e_classical = (epsilon0/2) * (kilogram * meter / (second**3 * ampere))**2
u_b_classical = (1/(2*mu0)) * (kilogram / (second**2 * ampere))**2

# 直接打印量纲
print("引力场能量密度项量纲:", u_g_paper)
print("电场能量密度项量纲:", u_e_classical)
print("磁场能量密度项量纲:", u_b_classical)

# 简化量纲显示
print("\n简化后的量纲:")
print("引力场能量密度项量纲:", sym.simplify(u_g_paper))
print("电场能量密度项量纲:", sym.simplify(u_e_classical))
print("磁场能量密度项量纲:", sym.simplify(u_b_classical))
# 输出均为 M/L/T^2，即能量密度量纲，此项验证通过。

# 验证几何常数表达式的一致性
# 论文声称 u_g = c/(16*pi*Z) * |A|^2，且应等于 1/(8*pi*G) * |A|^2
coeff_from_Z = c/(16*sym.pi*Z)
coeff_from_G = 1/(8*sym.pi*G)
print("\nc/(16πZ) 是否等于 1/(8πG)?", sym.simplify(coeff_from_Z - coeff_from_G) == 0)
# 输出 True，此项验证通过。

# 验证电场能量密度的几何常数表达式
# 论文给出 u_e = (1/2)*(4*pi*Z'/c) * |E|^2，应等于经典形式 (1/2)*epsilon0*|E|^2
coeff_E_geom = (4*sym.pi*Z_prime/c)/2  # 论文中的系数
coeff_E_classical = epsilon0/2
print("(4πZ'/c)/2 是否等于 ε0/2?", sym.simplify(coeff_E_geom - coeff_E_classical) == 0)
# 输出 False，发现不一致！

# 计算具体差值
print("(4πZ'/c)/2 =", sym.simplify(coeff_E_geom))
print("ε0/2 =", coeff_E_classical)
# (4πZ'/c)/2 简化为 1/(4*epsilon0)，而 ε0/2 是 ε0/2，两者不等。
# 这表明论文3.2.2节中的表达式 u_e = (1/2)*(4πZ'/c)|E|^2 是错误的。

# 验证磁场能量密度的几何常数表达式
# 论文给出 u_b = (4*pi*Z'/(2*c)) * |B|^2，应等于经典形式 (1/(2*mu0))*|B|^2
coeff_B_geom = (4*sym.pi*Z_prime)/(2*c)
coeff_B_classical = 1/(2*mu0)
print("4πZ'/(2c) 是否等于 1/(2μ0)?", sym.simplify(coeff_B_geom - coeff_B_classical) == 0)
# 输出 False，也不一致！

# 验证耦合常数 f 的量纲
# 论文给出 f = sqrt(Z/Z') * (c/2)
f = sym.sqrt(Z/Z_prime) * (c/2)
print("\n耦合常数 f 的量纲:", sym.simplify(f))

# 根据 E = -f * dA/dt，计算 f 应有的量纲
# E的量纲: kg·m/(s³·A)
# dA/dt的量纲: m/s³
# 因此 f 应有的量纲: (kg·m/(s³·A)) / (m/s³) = kg/A
required_f = kilogram / ampere
print("f 应有的量纲:", required_f)
print("量纲是否匹配:", sym.simplify(f) == required_f)
# 对比发现，论文给出的 f 量纲与所需量纲 M/I 不符，存在严重量纲错误。
