import sympy as sp
from sympy.vector import CoordSys3D, divergence, curl, gradient

# 定义三维坐标系
R = CoordSys3D('R')

# 定义符号常量
f, c, t = sp.symbols('f c t', real=True, positive=True)
v_x, v_y, v_z = sp.symbols('v_x v_y v_z', real=True)

# 定义向量场 A(x, y, z, t)
A_x = sp.Function('A_x')(R.x, R.y, R.z, t)
A_y = sp.Function('A_y')(R.x, R.y, R.z, t)
A_z = sp.Function('A_z')(R.x, R.y, R.z, t)
A = A_x*R.i + A_y*R.j + A_z*R.k

# 定义速度向量 v
v = v_x*R.i + v_y*R.j + v_z*R.k

print("=== 1. 磁矢势方程验证：∇ × A = B/f ===")
# 计算 A 的旋度
curl_A = curl(A)
print(f"旋度 ∇ × A = {curl_A}")

# 从方程 ∇ × A = B/f 解出 B
B = f * curl_A
print(f"磁感应强度 B = f(∇ × A) = {B}")

print("\n=== 2. 电场生成方程验证：E = -f ∂A/∂t ===")
# 计算 A 的时间偏导数
A_dt = sp.diff(A_x, t)*R.i + sp.diff(A_y, t)*R.j + sp.diff(A_z, t)*R.k
print(f"∂A/∂t = {A_dt}")

# 计算电场 E
E = -f * A_dt
print(f"电场 E = -f ∂A/∂t = {E}")

print("\n=== 3. 电场散度项验证：∇·E ===")
# 计算 E 的散度
div_E = divergence(E)
print(f"∇·E = {div_E}")

# 代入 E = -f ∂A/∂t，验证 ∇·E = -f ∂(∇·A)/∂t
div_E_substituted = -f * sp.diff(divergence(A), t)
print(f"-f ∂(∇·A)/∂t = {div_E_substituted}")

# 验证是否相等
is_div_equal = sp.simplify(div_E - div_E_substituted) == 0
print(f"∇·E 是否等于 -f ∂(∇·A)/∂t：{is_div_equal}")

print("\n=== 4. 磁场旋度项验证：∇ × B ===")
# 计算 B 的旋度
curl_B = curl(B)
print(f"∇ × B = {curl_B}")

# 使用向量恒等式：∇ × (∇ × A) = ∇(∇·A) - ∇²A
# 验证 ∇ × B = f(∇(∇·A) - ∇²A)
# 计算向量场 A 的拉普拉斯算子
laplacian_Ax = sp.diff(A_x, R.x, 2) + sp.diff(A_x, R.y, 2) + sp.diff(A_x, R.z, 2)
laplacian_Ay = sp.diff(A_y, R.x, 2) + sp.diff(A_y, R.y, 2) + sp.diff(A_y, R.z, 2)
laplacian_Az = sp.diff(A_z, R.x, 2) + sp.diff(A_z, R.y, 2) + sp.diff(A_z, R.z, 2)
laplacian_A_vector = laplacian_Ax*R.i + laplacian_Ay*R.j + laplacian_Az*R.k
curl_B_identity = f * (gradient(divergence(A)) - laplacian_A_vector)
print(f"f(∇(∇·A) - ∇²A) = {curl_B_identity}")

# 简化并验证
is_curl_equal = sp.simplify(curl_B - curl_B_identity) == 0
print(f"∇ × B 是否等于 f(∇(∇·A) - ∇²A)：{is_curl_equal}")

print("\n=== 5. 波动方程验证：∂²A/∂t² = (v/f)(∇·E) - (c²/f)(∇×B) ===")
# 计算 A 的二阶时间偏导数
A_dtt = sp.diff(A_x, t, 2)*R.i + sp.diff(A_y, t, 2)*R.j + sp.diff(A_z, t, 2)*R.k
print(f"∂²A/∂t² = {A_dtt}")

# 计算波动方程右侧
right_side = (v/f)*div_E - (c**2/f)*curl_B
print(f"波动方程右侧 = (v/f)(∇·E) - (c²/f)(∇×B) = {right_side}")

# 代入已知关系化简右侧
right_side_simplified = (v/f)*(-f * sp.diff(divergence(A), t)) - (c**2/f)*(f * (gradient(divergence(A)) - laplacian_A_vector))
right_side_simplified = sp.simplify(right_side_simplified)
print(f"化简后右侧 = {right_side_simplified}")

# 验证波动方程
is_wave_equal = sp.simplify(A_dtt - right_side_simplified) == 0
print(f"波动方程是否自洽：{is_wave_equal}")

print("\n=== 6. 特殊情况验证：无散场（∇·A = 0）===\n")
# 假设 A 是无散场，即 ∇·A = 0
A_solenoidal = A.subs(divergence(A), 0)

print("无散场下：")
print(f"∇·A = {divergence(A_solenoidal)}")

# 波动方程简化
wave_eq_solenoidal = right_side_simplified.subs(divergence(A), 0)
print(f"波动方程简化为：∂²A/∂t² = {wave_eq_solenoidal}")

# 验证是否为经典波动方程
is_classical_wave = sp.simplify(wave_eq_solenoidal - c**2 * laplacian_A_vector) == 0
print(f"是否退化为经典波动方程 ∂²A/∂t² = c²∇²A：{is_classical_wave}")

print("\n=== 7. 量纲一致性验证 ===")
# 定义基本量纲
L, M, T, I = sp.symbols('L M T I')

# 定义各物理量的量纲
A_dim = L*T**(-2)  # 引力场强度量纲
B_dim = M*T**(-2)*I**(-1)  # 磁感应强度量纲
E_dim = M*L*T**(-3)*I**(-1)  # 电场强度量纲
v_dim = L*T**(-1)  # 速度量纲
c_dim = L*T**(-1)  # 光速量纲

# 从磁矢势方程推导 f 的量纲
print("从 ∇ × A = B/f 推导 f 的量纲：")
curl_A_dim = A_dim / L  # 旋度量纲 = A_dim / L
f_dim1 = B_dim / curl_A_dim
print(f"旋度 ∇×A 的量纲：{curl_A_dim}")
print(f"B 的量纲：{B_dim}")
print(f"f 的量纲：{f_dim1} = {sp.simplify(f_dim1)}")

# 从电场生成方程验证 f 的量纲
print("\n从 E = -f ∂A/∂t 验证 f 的量纲：")
dAdt_dim = A_dim / T  # ∂A/∂t 量纲 = A_dim / T
f_dim2 = E_dim / dAdt_dim
print(f"∂A/∂t 的量纲：{dAdt_dim}")
print(f"E 的量纲：{E_dim}")
print(f"f 的量纲：{f_dim2} = {sp.simplify(f_dim2)}")

# 验证两种方法得到的量纲是否一致
is_dim_consistent = f_dim1 == f_dim2
print(f"\nf 的量纲是否一致：{is_dim_consistent}")

print("\n=== 8. 数值计算验证 ===")
# 使用数值计算验证向量场的旋度和散度
import numpy as np

# 定义一个具体的向量场 A(x, y, z, t)
def A_field(x, y, z, t):
    # 示例：A = (x²y, y²z, z²x) exp(-t)
    factor = np.exp(-t)
    return np.array([
        (x**2 * y) * factor,
        (y**2 * z) * factor,
        (z**2 * x) * factor
    ])

# 计算旋度 ∇×A
# 旋度的数值近似：使用中心差分

def curl_numerical(A_func, x, y, z, t, h=1e-6):
    # 计算 ∂A_z/∂y - ∂A_y/∂z
    A_zy_plus = A_func(x, y+h, z, t)[2]
    A_zy_minus = A_func(x, y-h, z, t)[2]
    dA_z_dy = (A_zy_plus - A_zy_minus) / (2*h)
    
    A_yz_plus = A_func(x, y, z+h, t)[1]
    A_yz_minus = A_func(x, y, z-h, t)[1]
    dA_y_dz = (A_yz_plus - A_yz_minus) / (2*h)
    curl_x = dA_z_dy - dA_y_dz
    
    # 计算 ∂A_x/∂z - ∂A_z/∂x
    A_xz_plus = A_func(x, y, z+h, t)[0]
    A_xz_minus = A_func(x, y, z-h, t)[0]
    dA_x_dz = (A_xz_plus - A_xz_minus) / (2*h)
    
    A_zx_plus = A_func(x+h, y, z, t)[2]
    A_zx_minus = A_func(x-h, y, z, t)[2]
    dA_z_dx = (A_zx_plus - A_zx_minus) / (2*h)
    curl_y = dA_x_dz - dA_z_dx
    
    # 计算 ∂A_y/∂x - ∂A_x/∂y
    A_yx_plus = A_func(x+h, y, z, t)[1]
    A_yx_minus = A_func(x-h, y, z, t)[1]
    dA_y_dx = (A_yx_plus - A_yx_minus) / (2*h)
    
    A_xy_plus = A_func(x, y+h, z, t)[0]
    A_xy_minus = A_func(x, y-h, z, t)[0]
    dA_x_dy = (A_xy_plus - A_xy_minus) / (2*h)
    curl_z = dA_y_dx - dA_x_dy
    
    return np.array([curl_x, curl_y, curl_z])

# 计算散度 ∇·A
def divergence_numerical(A_func, x, y, z, t, h=1e-6):
    A_x_plus = A_func(x+h, y, z, t)[0]
    A_x_minus = A_func(x-h, y, z, t)[0]
    dA_x_dx = (A_x_plus - A_x_minus) / (2*h)
    
    A_y_plus = A_func(x, y+h, z, t)[1]
    A_y_minus = A_func(x, y-h, z, t)[1]
    dA_y_dy = (A_y_plus - A_y_minus) / (2*h)
    
    A_z_plus = A_func(x, y, z+h, t)[2]
    A_z_minus = A_func(x, y, z-h, t)[2]
    dA_z_dz = (A_z_plus - A_z_minus) / (2*h)
    
    return dA_x_dx + dA_y_dy + dA_z_dz

# 测试点
x, y, z, t = 1.0, 1.0, 1.0, 0.0

# 计算旋度数值解
curl_num = curl_numerical(A_field, x, y, z, t)
print(f"在点 ({x}, {y}, {z}, {t}) 处：")
print(f"向量场 A = {A_field(x, y, z, t)}")
print(f"数值计算旋度 ∇×A = {curl_num}")

# 计算散度数值解
div_num = divergence_numerical(A_field, x, y, z, t)
print(f"数值计算散度 ∇·A = {div_num}")

print("\n=== 验证完成 ===")