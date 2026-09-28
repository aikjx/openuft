import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 1. 量纲一致性验证 =====================
# 定义量纲的基本单位：L(长度), T(时间), M(质量), I(电流)
# 量纲用字典表示，键为基本单位，值为指数
dim_L = {'L': 1, 'T': 0, 'M': 0, 'I': 0}
dim_T = {'L': 0, 'T': 1, 'M': 0, 'I': 0}
dim_M = {'L': 0, 'T': 0, 'M': 1, 'I': 0}
dim_I = {'L': 0, 'T': 0, 'M': 0, 'I': 1}

# 定义场量的量纲（根据论文中的定义）
# 引力场 A: [L T^-2]
dim_A = {'L': 1, 'T': -2, 'M': 0, 'I': 0}
# 旋度算子 ∇×: [L^-1]
dim_curl = {'L': -1, 'T': 0, 'M': 0, 'I': 0}
# 左边 ∇×A 的量纲: [L^-1] * [L T^-2] = [T^-2]
dim_left = {
    'L': dim_curl['L'] + dim_A['L'],
    'T': dim_curl['T'] + dim_A['T'],
    'M': dim_curl['M'] + dim_A['M'],
    'I': dim_curl['I'] + dim_A['I']
}

# 右边 B/f 的量纲: B的量纲[M T^-2 I^-1] / f的量纲[M I^-1] = [T^-2]
dim_B = {'L': 0, 'T': -2, 'M': 1, 'I': -1}
dim_f = {'L': 0, 'T': 0, 'M': 1, 'I': -1}
dim_right = {
    'L': dim_B['L'] - dim_f['L'],
    'T': dim_B['T'] - dim_f['T'],
    'M': dim_B['M'] - dim_f['M'],
    'I': dim_B['I'] - dim_f['I']
}

# 输出量纲验证结果
print("===== 量纲一致性验证 =====")
print(f"左边 ∇×A 的量纲: {dim_left}")
print(f"右边 B/f 的量纲: {dim_right}")
print(f"量纲是否一致: {dim_left == dim_right}")

# ===================== 2. 数学自洽性验证 =====================
# 核心：验证 ∇·(∇×A) = 0，从而推导 ∇·B = 0
# 步骤：构造三维引力场 A → 计算旋度 → 计算旋度的散度 → 验证是否趋近于0

def gradient_field(f, dx=1, dy=1, dz=1):
    """计算标量场的梯度（三维）"""
    gx, gy, gz = np.gradient(f, dx, dy, dz)
    return np.array([gx, gy, gz])

def curl_field(A, dx=1, dy=1, dz=1):
    """计算矢量场的旋度 ∇×A
    A: 三维矢量场，shape为(3, Nx, Ny, Nz)
    返回旋度场 curl_A，shape同A
    """
    Ax, Ay, Az = A
    # 计算各分量的偏导数（注意：使用 indexing='ij' 时，axis=0对应x，axis=1对应y，axis=2对应z）
    dAz_dy = np.gradient(Az, dy, axis=1)  # ∂Az/∂y
    dAy_dz = np.gradient(Ay, dz, axis=2)  # ∂Ay/∂z
    dAx_dz = np.gradient(Ax, dz, axis=2)  # ∂Ax/∂z
    dAz_dx = np.gradient(Az, dx, axis=0)  # ∂Az/∂x
    dAy_dx = np.gradient(Ay, dx, axis=0)  # ∂Ay/∂x
    dAx_dy = np.gradient(Ax, dy, axis=1)  # ∂Ax/∂y
    
    # 旋度公式：∇×A = (∂Az/∂y - ∂Ay/∂z)i + (∂Ax/∂z - ∂Az/∂x)j + (∂Ay/∂x - ∂Ax/∂y)k
    curl_x = dAz_dy - dAy_dz
    curl_y = dAx_dz - dAz_dx
    curl_z = dAy_dx - dAx_dy
    return np.array([curl_x, curl_y, curl_z])

def divergence_field(F, dx=1, dy=1, dz=1):
    """计算矢量场的散度 ∇·F"""
    Fx, Fy, Fz = F
    dFx_dx = np.gradient(Fx, dx, axis=0)
    dFy_dy = np.gradient(Fy, dy, axis=1)
    dFz_dz = np.gradient(Fz, dz, axis=2)
    return dFx_dx + dFy_dy + dFz_dz

# 构造三维网格
N = 50
x = np.linspace(-10, 10, N)
y = np.linspace(-10, 10, N)
z = np.linspace(-10, 10, N)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# 构造一个示例引力场 A (满足任意光滑矢量场)
# 示例：A = (-y, x, 0) * t^-2  （时间因子t^-2保证量纲为[L T^-2]）
t = 1.0  # 设定时间参数
Ax = -Y / (t**2)
Ay = X / (t**2)
Az = np.zeros_like(Z)
A_field = np.array([Ax, Ay, Az])

# 计算旋度 ∇×A
curl_A = curl_field(A_field, dx=x[1]-x[0], dy=y[1]-y[0], dz=z[1]-z[0])
# 计算旋度的散度 ∇·(∇×A)
div_curl_A = divergence_field(curl_A, dx=x[1]-x[0], dy=y[1]-y[0], dz=z[1]-z[0])

# 验证散度是否趋近于0（数值计算存在微小误差）
max_div = np.max(np.abs(div_curl_A))
print("\n===== 数学自洽性验证 =====")
print(f"∇·(∇×A) 的最大值: {max_div:.10e}")
print(f"是否满足 ∇·(∇×A) ≈ 0: {max_div < 1e-10}")
print(f"推导结论：∇·B = ∇·(f·∇×A) = f·∇·(∇×A) ≈ 0，与磁场高斯定律一致")

# ===================== 3. 可视化旋度场 =====================
# 取z=0平面的截面可视化
z_slice = N // 2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 原引力场 A 的截面
ax1.quiver(X[:, :, z_slice], Y[:, :, z_slice], 
           A_field[0, :, :, z_slice], A_field[1, :, :, z_slice],
           color='blue', alpha=0.6, scale=100, scale_units='xy')
ax1.set_title('引力场 A (z=0截面)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')

# 旋度场 ∇×A 的截面
ax2.quiver(X[:, :, z_slice], Y[:, :, z_slice], 
           curl_A[0, :, :, z_slice], curl_A[1, :, :, z_slice],
           color='red', alpha=0.6, scale=10, scale_units='xy')
ax2.set_title('旋度场 ∇×A (z=0截面)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()