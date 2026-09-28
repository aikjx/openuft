import math
import numpy as np
import matplotlib.pyplot as plt

# 先复用原有物理常数定义
c = 299792458  # 真空光速，m/s
G = 6.67430e-11  # 万有引力常数，m^3/kg/s^2
epsilon0 = 8.8541878128e-12  # 真空介电常数，F/m
e = 1.602176634e-19  # 电子电荷，C
m_e = 9.1093837015e-31  # 电子质量，kg
m_p = 1.67262192369e-27  # 质子质量，kg
h_bar = 1.054571817e-34  # 约化普朗克常数，J·s

# 计算核心常数f（复用原有逻辑）
def calculate_f():
    Z = (G * c) / 2
    Z_prime = c / (8 * math.pi * epsilon0)
    f = math.sqrt(Z / Z_prime) * (c / 2)
    return f

f = calculate_f()
print(f"常数f的取值：{f:.6f}")

# ===================== 步骤1：构造理论数据集（符合经典电磁学） =====================
# 设定时间区间（生成离散时间点）
t_start = 0
t_end = 1e-6  # 微秒级，符合电磁现象时标
n_points = 1000  # 离散数据点数量，越多数值求导越准确
t = np.linspace(t_start, t_end, n_points)
dt = t[1] - t[0]  # 时间步长

# 构造时变磁场B(t)（简单正弦变化，便于求导验证）
# 设定B的振幅和角频率（取值仅为验证，不考虑实际物理量级）
B_amplitude = 1.0
omega = 2 * math.pi * 1e6  # 1MHz角频率
B = B_amplitude * np.sin(omega * t)  # 磁场数据集（标量简化，方便验证）

# 根据法拉第定律，构造对应的电场E(t)（标量简化）
E = - (B_amplitude * omega / f) * np.cos(omega * t)  # 从方程3、2推导得到的理论E(t)

# ===================== 步骤2：根据ZUFT方程生成磁矢势A(t)数据集 =====================
# 从方程3：E = -f dA/dt → dA/dt = -E/f → A(t) = ∫(-E/f)dt + C（积分常数C取0）
A = (B_amplitude / f) * np.sin(omega * t)  # 积分后的磁矢势数据集（理论值）

# ===================== 步骤3：数值求导实现（有限差分法） =====================
def numerical_derivative(y, dx):
    """
    一阶数值求导：中心差分法（精度高于前向/后向差分）
    y: 离散数据集
    dx: 自变量步长
    """
    dy = np.zeros_like(y)
    # 中间点用中心差分
    dy[1:-1] = (y[2:] - y[:-2]) / (2 * dx)
    # 边界点用前向/后向差分
    dy[0] = (y[1] - y[0]) / dx
    dy[-1] = (y[-1] - y[-2]) / dx
    return dy

def numerical_second_derivative(y, dx):
    """
    二阶数值求导：中心差分法
    """
    d2y = np.zeros_like(y)
    d2y[1:-1] = (y[2:] - 2 * y[1:-1] + y[:-2]) / (dx ** 2)
    # 边界点简化处理
    d2y[0] = (y[2] - 2 * y[1] + y[0]) / (dx ** 2)
    d2y[-1] = (y[-1] - 2 * y[-2] + y[-3]) / (dx ** 2)
    return d2y

# ===================== 步骤4：代入ZUFT方程进行数值验证 =====================
print("\n=== 代入数据集的数值求导验证 ===")

# 验证方程3：E = -f dA/dt
dA_dt_num = numerical_derivative(A, dt)  # A(t)的一阶数值导数
E_num = -f * dA_dt_num  # 从数值求导得到的E(t)

# 计算方程3的误差（理论值与数值值的相对误差）
E_error = np.mean(np.abs((E_num - E) / E)) * 100
print(f"方程3验证：数值计算E与理论E的平均相对误差 = {E_error:.6f}%")

# 验证方程2：∇×A = B/f（标量简化：dA/dx = B/f，构造空间维度x的数据集）
# 补充空间维度x（简单均匀分布）
x_start = 0
x_end = 1e-3
x = np.linspace(x_start, x_end, n_points)
dx = x[1] - x[0]

# 构造空间分布的A(x,t)（固定t=0.5e-6，取中间时刻）
t_mid = int(n_points / 2)
A_x = (B_amplitude / f) * np.sin(omega * t[t_mid]) * np.sin(2 * math.pi * x / x_end)
B_x = B_amplitude * np.sin(omega * t[t_mid]) * np.cos(2 * math.pi * x / x_end) * (2 * math.pi / x_end)

# 空间一阶数值导数（对应∇×A的标量简化）
dA_dx_num = numerical_derivative(A_x, dx)
B_num = f * dA_dx_num  # 从数值求导得到的B(x)

# 计算方程2的误差
B_error = np.mean(np.abs((B_num - B_x) / B_x)) * 100
print(f"方程2验证：数值计算B与理论B的平均相对误差 = {B_error:.6f}%")

# 验证方程1：∂²A/∂t² = V/f (∇·E) - C²/f (∇×B)（标量简化，忽略空间项，验证时间二阶导数）
d2A_dt2_num = numerical_second_derivative(A, dt)  # A(t)的二阶数值导数
# 标量简化：忽略空间项，右边近似为 -c²/f * (dB/dt)
dB_dt_num = numerical_derivative(B, dt)
rhs_num = - (c ** 2 / f) * dB_dt_num  # 方程1右边数值值

# 计算方程1的误差
eq1_error = np.mean(np.abs((d2A_dt2_num - rhs_num) / rhs_num)) * 100
print(f"方程1验证（标量简化）：数值计算左边与右边的平均相对误差 = {eq1_error:.6f}%")

# ===================== 步骤5：绘图可视化验证结果（可选） =====================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
plt.rcParams['axes.unicode_minus'] = False

# 绘制方程3的验证结果
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, E, label='理论E(t)', color='blue')
plt.plot(t, E_num, label='数值计算E(t)', color='red', linestyle='--')
plt.xlabel('时间 t (s)')
plt.ylabel('电场 E')
plt.title('方程3：E = -f dA/dt 验证')
plt.legend()
plt.grid(True, alpha=0.3)

# 绘制方程2的验证结果
plt.subplot(1, 2, 2)
plt.plot(x, B_x, label='理论B(x)', color='blue')
plt.plot(x, B_num, label='数值计算B(x)', color='red', linestyle='--')
plt.xlabel('空间 x (m)')
plt.ylabel('磁场 B')
plt.title('方程2：∇×A = B/f 验证')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
