import sympy as sp

# 定义符号变量
t = sp.Symbol('t')
Omega = sp.Function('Omega')(t)
r = sp.Function('r')(t)
vec_r = sp.Matrix([sp.Function('x')(t), sp.Function('y')(t), sp.Function('z')(t)])
k = sp.Symbol('k')
k_prime = sp.Symbol("k'")
epsilon0 = sp.Symbol('epsilon0')

# 速度矢量
dvec_r = vec_r.diff(t)

print("=== 电荷定义方程求导验证 ===")
# 电荷定义方程: q = k'k * (1/Omega**2) * dOmega/dt
q = k_prime * k * (1/Omega**2) * Omega.diff(t)
print(f"电荷定义方程: q = {q}")

# 求导得到电流 I = dq/dt
I = q.diff(t)
print(f"\n电流表达式: I = {I}")

# 简化表达式
simplified_I = sp.simplify(I)
print(f"\n简化后的电流表达式: I = {simplified_I}")

print("\n=== 电场定义方程求导验证 ===")
# 电场定义方程: E = - (k*k')/(4*pi*epsilon0*Omega**2) * dOmega/dt * vec_r/r**3
E = - (k * k_prime) / (4 * sp.pi * epsilon0 * Omega**2) * Omega.diff(t) * vec_r / r**3
print(f"电场定义方程: E = {E}")

# 求导得到电场的时间变化率 dE/dt
dE_dt = E.diff(t)
print(f"\n电场时间变化率: dE/dt = {dE_dt}")

# 简化表达式
simplified_dE_dt = sp.simplify(dE_dt)
print(f"\n简化后的电场时间变化率: dE/dt = {simplified_dE_dt}")

print("\n=== 经典电磁学兼容性验证 ===")
# 从电荷定义方程解出 k'k * dOmega/dt / Omega^2
q_expr = k_prime * k * (1/Omega**2) * Omega.diff(t)
print(f"电荷定义方程: q = {q_expr}")

# 定义表达式 k*k'*dOmega/dt/Omega^2
sub_expr = k * k_prime * Omega.diff(t) / Omega**2
print(f"\n要替换的表达式: k*k'*dOmega/dt/Omega^2 = {sub_expr}")

# 代入电场定义方程
E_expr = - (k * k_prime) / (4 * sp.pi * epsilon0 * Omega**2) * Omega.diff(t) * vec_r / r**3
print(f"\n原始电场定义方程: E = {E_expr}")

# 替换 k*k' * dOmega/dt / Omega^2 为 q
E_coulomb = E_expr.subs(sub_expr, q)
print(f"\n代入后的电场表达式: E = {E_coulomb}")

# 手动构建库仑定律形式进行比较
E_coulomb_law = - q * vec_r / (4 * sp.pi * epsilon0 * r**3)
print(f"\n库仑定律形式: E = {E_coulomb_law}")

# 检查是否一致
print(f"\n是否与库仑定律一致: {E_coulomb == E_coulomb_law}")

print("\n验证完成!")