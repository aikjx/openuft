import sympy as sp
import numpy as np

# 定义符号变量
t = sp.Symbol('t')
r = sp.Function('r')(t)
omega = sp.Symbol('omega')
h = sp.Symbol('h')
lmbda = sp.Symbol('lambda')

# 1. 螺旋时空方程的位置矢量
x = r * sp.cos(omega * t)
y = r * sp.sin(omega * t)
z = h * t

# 2. 计算速度矢量（一阶导数）
vx = sp.diff(x, t)
vy = sp.diff(y, t)
vz = sp.diff(z, t)

print("=== 速度矢量计算 ===")
print(f"vx = {vx}")
print(f"vy = {vy}")
print(f"vz = {vz}")
print()

# 3. 应用演化假设 dr/dt = lambda * r
dr_dt = lmbda * r
vx_subs = vx.subs(sp.diff(r, t), dr_dt)
vy_subs = vy.subs(sp.diff(r, t), dr_dt)

print("=== 代入演化假设后的速度矢量 ===")
print(f"vx_subs = {vx_subs}")
print(f"vy_subs = {vy_subs}")
print(f"vz = {vz}")
print()

# 4. 计算横向速度的模
v_perp_squared = vx_subs**2 + vy_subs**2
v_perp_squared_simplified = sp.simplify(v_perp_squared)
v_perp = sp.sqrt(v_perp_squared_simplified)

print("=== 横向速度的模 ===")
print(f"v_perp^2 = {v_perp_squared}")
print(f"v_perp^2 (简化后) = {v_perp_squared_simplified}")
print(f"v_perp = {v_perp}")
print()

# 5. 验证微分方程的解
print("=== 演化微分方程的解 ===")
diff_eq = sp.Eq(sp.diff(r, t), lmbda * r)
sol = sp.dsolve(diff_eq, r)
print(f"微分方程: {diff_eq}")
print(f"通解: {sol}")
print()

# 6. 数值验证
def numerical_verification():
    print("=== 数值验证 ===")
    # 设定参数
    omega_val = 2 * np.pi  # 角频率
    lmbda_val = 0.5  # 演化常数
    h_val = 1.0  # 纵向速度
    r0 = 1.0  # 初始半径
    
    # 时间点
    t_val = 1.0
    
    # 计算r(t) = r0 * e^(lambda * t)
    r_val = r0 * np.exp(lmbda_val * t_val)
    
    # 计算速度分量
    vx_num = lmbda_val * r_val * np.cos(omega_val * t_val) - r_val * omega_val * np.sin(omega_val * t_val)
    vy_num = lmbda_val * r_val * np.sin(omega_val * t_val) + r_val * omega_val * np.cos(omega_val * t_val)
    vz_num = h_val
    
    # 计算横向速度的模
    v_perp_num = np.sqrt(vx_num**2 + vy_num**2)
    v_perp_analytic = r_val * np.sqrt(lmbda_val**2 + omega_val**2)
    
    print(f"参数值:")
    print(f"omega = {omega_val}, lambda = {lmbda_val}, h = {h_val}, r0 = {r0}, t = {t_val}")
    print()
    print(f"r(t) = {r_val}")
    print()
    print(f"速度分量:")
    print(f"vx = {vx_num}")
    print(f"vy = {vy_num}")
    print(f"vz = {vz_num}")
    print()
    print(f"横向速度:")
    print(f"数值计算: {v_perp_num}")
    print(f"解析解: {v_perp_analytic}")
    print(f"误差: {abs(v_perp_num - v_perp_analytic):.10f}")

numerical_verification()
