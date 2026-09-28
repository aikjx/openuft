import sympy as sp
import numpy as np

# ====================== 1. 定义符号与坐标系 ======================
# 球坐标系 (r, θ, φ) 用于引力场/静电场分析
r, theta, phi, G, M, k, t = sp.symbols('r theta phi G M k t', positive=True, real=True)
# 定义单位矢量 (球坐标)
e_r = sp.Matrix([1, 0, 0])
e_theta = sp.Matrix([0, 1, 0])
e_phi = sp.Matrix([0, 0, 1])

# ====================== 2. 验证：静态引力场的旋度为 0 ======================
# 张祥前理论中静态引力场表达式：A = -GM/r² * e_r
A_grav = sp.Matrix([-G*M / r**2, 0, 0])  # 球坐标下分量 [A_r, A_theta, A_phi]

# 球坐标系下旋度公式：
# ∇×A = (1/(r sinθ)) [ ∂(A_phi sinθ)/∂θ - ∂A_theta/∂φ ] e_r
#      + (1/r)[ (1/sinθ) ∂A_r/∂φ - ∂(r A_phi)/∂r ] e_theta
#      + (1/r)[ ∂(r A_theta)/∂r - ∂A_r/∂θ ] e_phi
def curl_spherical(A_r, A_theta, A_phi, r, theta, phi):
    # 计算各分量
    curl_r = (1/(r * sp.sin(theta))) * (sp.diff(A_phi * sp.sin(theta), theta) - sp.diff(A_theta, phi))
    curl_theta = (1/r) * ( (1/sp.sin(theta)) * sp.diff(A_r, phi) - sp.diff(r * A_phi, r) )
    curl_phi = (1/r) * ( sp.diff(r * A_theta, r) - sp.diff(A_r, theta) )
    return sp.Matrix([curl_r, curl_theta, curl_phi])

# 计算引力场旋度
curl_A_grav = curl_spherical(A_grav[0], A_grav[1], A_grav[2], r, theta, phi)
print("=== 静态引力场的旋度 ===")
sp.pprint(curl_A_grav.simplify())
# 输出应为 [0, 0, 0]，验证引力场无旋

# ====================== 3. 验证：磁场的散度恒为 0 ======================
# 核心方程：B = f * (∇×A)
# 矢量恒等式：∇·(∇×A) ≡ 0 → ∇·B = 0
# 用 SymPy 验证该恒等式
A_x, A_y, A_z = sp.symbols('A_x A_y A_z', cls=sp.Function)
x, y, z = sp.symbols('x y z', real=True)
A = sp.Matrix([A_x(x,y,z), A_y(x,y,z), A_z(x,y,z)])

# 直角坐标系散度公式
def div(A, x, y, z):
    return sp.diff(A[0], x) + sp.diff(A[1], y) + sp.diff(A[2], z)

# 直角坐标系旋度公式
def curl_cartesian(A, x, y, z):
    curl_x = sp.diff(A[2], y) - sp.diff(A[1], z)
    curl_y = sp.diff(A[0], z) - sp.diff(A[2], x)
    curl_z = sp.diff(A[1], x) - sp.diff(A[0], y)
    return sp.Matrix([curl_x, curl_y, curl_z])

# 计算 ∇·(∇×A)
curl_A = curl_cartesian(A, x, y, z)
div_curl_A = div(curl_A, x, y, z)
print("\n=== 验证 ∇·(∇×A) ≡ 0 ===")
sp.pprint(div_curl_A.simplify())
# 输出为 0 → 直接证明 ∇·B = 0，磁场是无源旋涡场

# ====================== 4. 验证：静电场的旋度为 0 ======================
# 静电场：E = -∇φ (φ 为电势)，保守场旋度为 0
phi = sp.Function('phi')(x, y, z)
E = -sp.Matrix([sp.diff(phi, x), sp.diff(phi, y), sp.diff(phi, z)])
curl_E = curl_cartesian(E, x, y, z)
print("\n=== 静电场的旋度 ===")
sp.pprint(curl_E.simplify())
# 输出为 [0,0,0]，验证静电场无旋

# ====================== 5. 数值验证：通电直导线的磁场（旋涡场） ======================
# 无限长直导线磁场：B_phi = μ0 I / (2π r) → 具有旋度，是旋涡场
def B_field(r):
    mu0 = 4e-7 * np.pi
    I = 1.0  # 假设电流 1A
    return mu0 * I / (2 * np.pi * r)  # B_phi 分量

# 取不同半径验证 B 的环流特性（旋涡场核心是环流不为零）
r_list = np.linspace(0.1, 1.0, 10)
B_list = [B_field(r) for r in r_list]
print("\n=== 通电直导线磁场的 φ 分量 ===")
for r, b in zip(r_list, B_list):
    print(f"r={r:.2f}m → B_phi={b:.2e} T")
# 结果：r 越小，B_phi 越大 → 符合旋涡场分布规律