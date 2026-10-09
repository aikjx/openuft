import sympy as sp

# 定义符号变量
t, x, y, z, c, kx, ky, kz, omega = sp.symbols('t x y z c kx ky kz omega')
r = sp.Function('r')(x, y, z, t)

# 定义三维空间波动方程
wave_eq = sp.Eq(sp.diff(r, t, 2), c**2 * (sp.diff(r, x, 2) + sp.diff(r, y, 2) + sp.diff(r, z, 2)))
print("空间波动方程：")
print(wave_eq)

# 验证三维平面波解（波矢为k）
vec_k = sp.Matrix([kx, ky, kz])
vec_x = sp.Matrix([x, y, z])
k_dot_x = vec_k.dot(vec_x)
plane_wave_3d = sp.exp(sp.I * (k_dot_x - omega*t))

# 代入波动方程并化简
substituted = wave_eq.subs(r, plane_wave_3d)
simplified = sp.simplify(substituted)
print("\n三维平面波解代入后的简化方程：")
print(simplified)

# 求解色散关系
omega_solutions = sp.solve(simplified, omega)
print("\n色散关系解：")
for sol in omega_solutions:
    print(f"ω = {sol}")

# 波速计算（假设波沿x方向传播）
solution_x_dir = simplified.subs([(ky, 0), (kz, 0)])
omega_x_solutions = sp.solve(solution_x_dir, omega)
print("\n沿x方向传播的色散关系：")
for sol in omega_x_solutions:
    print(f"ω = {sol}")
    wave_speed = sol / kx
    print(f"波速 v = ω/kx = {wave_speed}")

# 验证一维通解形式
tau1 = t - x/c
tau2 = t + x/c
f = sp.Function('f')(tau1)
g = sp.Function('g')(tau2)
one_d_general_solution = f + g

# 计算一维波动方程的两边
left_side = sp.diff(one_d_general_solution, t, 2)
right_side = c**2 * sp.diff(one_d_general_solution, x, 2)
verification_result = sp.simplify(left_side - right_side)
print("\n一维通解验证结果（应为0）：")
print(verification_result)

# 验证三维通解的完备性（通过叠加原理）
print("\n三维通解叠加原理验证：")
# 创建两个不同波矢的平面波
plane_wave1 = sp.exp(sp.I * ((kx + 1)*x + (ky + 1)*y + (kz + 1)*z - omega*t))
plane_wave2 = sp.exp(sp.I * ((kx - 1)*x + (ky - 1)*y + (kz - 1)*z - omega*t))
# 叠加两个平面波
superposition = plane_wave1 + plane_wave2
# 代入波动方程
superposition_substituted = wave_eq.subs(r, superposition)
superposition_simplified = sp.simplify(superposition_substituted)
print("叠加波解代入波动方程的结果（应为0）：")
print(sp.simplify(superposition_simplified.lhs - superposition_simplified.rhs))