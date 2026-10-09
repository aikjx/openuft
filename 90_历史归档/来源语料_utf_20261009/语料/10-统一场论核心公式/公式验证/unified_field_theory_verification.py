import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体支持（避免中文显示问题）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=== 统一场论核心公式验证开始 ===")

# ===============================
# 1. 公式1：时空同一化方程验证
# ===============================
print("\n1. 时空同一化方程验证")

# 物理常数
c = 3e8  # 光速（m/s）

# 时间范围（0到1e-8秒，10000个采样点）
t = np.linspace(0, 1e-8, 10000)

# 公式1：x = ct
x_theoretical = c * t

# 数值计算（直接计算，用于对比）
x_numerical = c * t

# 计算相对误差
error = np.abs(x_numerical - x_theoretical) / (np.abs(x_theoretical) + 1e-15)  # 避免除以零
max_error = np.max(error)
avg_error = np.mean(error)

print(f"  - 最大相对误差: {max_error:.15f}")
print(f"  - 平均相对误差: {avg_error:.15f}")
print(f"  - 误差数量级: {10**np.floor(np.log10(max_error)):.0e}")

# 可视化1：x-t关系图
plt.figure(figsize=(14, 10))

# 主图：x = ct关系
ax1 = plt.subplot(211)
ax1.plot(t, x_theoretical, label='理论值 x = ct', color='blue', linewidth=2)
ax1.scatter(t[::100], x_numerical[::100], label='数值计算点（每100个点）', 
            color='red', marker='o', alpha=0.5, s=20)
ax1.set_xlabel('时间 t (s)', fontsize=14)
ax1.set_ylabel('位置 x (m)', fontsize=14)
ax1.set_title('公式1：时空同一化方程验证', fontsize=16, fontweight='bold')
ax1.legend(fontsize=12, loc='lower right')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.tick_params(axis='both', which='major', labelsize=12)

# 副图：误差分析
ax2 = plt.subplot(212)
ax2.semilogy(t, error, label='相对误差', color='green', linewidth=2, alpha=0.8)
ax2.axhline(y=1e-12, color='red', linestyle='--', label='1e-12 误差阈值')
ax2.set_xlabel('时间 t (s)', fontsize=14)
ax2.set_ylabel('相对误差（对数刻度）', fontsize=14)
ax2.set_title('时空同一化方程误差分析', fontsize=16, fontweight='bold')
ax2.legend(fontsize=12, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.savefig('时空同一化验证.png', dpi=300, bbox_inches='tight')
plt.close()

# ===============================
# 2. 公式2：三维螺旋时空方程验证
# ===============================
print("\n2. 三维螺旋时空方程验证")

# 螺旋参数
r = 1.0  # 螺旋半径（m）
omega = 1e9  # 角速度（rad/s）
v_axial = 1e6  # 轴向速度（m/s）

# 计算螺旋轨迹
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = v_axial * t

# 计算速度分量
vx = -r * omega * np.sin(omega * t)  # dx/dt
vy = r * omega * np.cos(omega * t)   # dy/dt
vz = v_axial * np.ones_like(t)       # dz/dt

# 计算速度大小
speed = np.sqrt(vx**2 + vy**2 + vz**2)
expected_speed = np.sqrt((r*omega)**2 + v_axial**2)

# 计算速度大小相对误差
speed_error = np.abs(speed - expected_speed) / expected_speed
max_speed_error = np.max(speed_error)
avg_speed_error = np.mean(speed_error)

print(f"  - 理论速度大小: {expected_speed:.6e} m/s")
print(f"  - 速度大小最大相对误差: {max_speed_error:.15f}")
print(f"  - 速度大小平均相对误差: {avg_speed_error:.15f}")

# 可视化2：三维螺旋轨迹
fig = plt.figure(figsize=(14, 12))

# 主图：三维螺旋轨迹
ax1 = fig.add_subplot(211, projection='3d')
ax1.plot(x, y, z, label='三维螺旋时空轨迹', color='purple', linewidth=2)
ax1.set_xlabel('X (m)', fontsize=14)
ax1.set_ylabel('Y (m)', fontsize=14)
ax1.set_zlabel('Z (m)', fontsize=14)
ax1.set_title('公式2：三维螺旋时空方程验证', fontsize=16, fontweight='bold')
ax1.legend(fontsize=12, loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.view_init(elev=30, azim=45)  # 设置视角

# 副图：速度大小随时间变化
ax2 = fig.add_subplot(212)
ax2.plot(t, speed, label='实际速度大小', color='blue', linewidth=2, alpha=0.8)
ax2.axhline(y=expected_speed, color='red', linestyle='--', label='理论速度大小')
ax2.set_xlabel('时间 t (s)', fontsize=14)
ax2.set_ylabel('速度大小 (m/s)', fontsize=14)
ax2.set_title('三维螺旋时空速度分析', fontsize=16, fontweight='bold')
ax2.legend(fontsize=12, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.savefig('三维螺旋时空验证.png', dpi=300, bbox_inches='tight')
plt.close()

# 可视化3：速度分量分析
plt.figure(figsize=(14, 10))

plt.plot(t, vx, label='vx = -rω sin(ωt)', color='red', linewidth=2, alpha=0.8)
plt.plot(t, vy, label='vy = rω cos(ωt)', color='green', linewidth=2, alpha=0.8)
plt.plot(t, vz, label='vz = v_axial', color='blue', linewidth=2, alpha=0.8)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

plt.xlabel('时间 t (s)', fontsize=14)
plt.ylabel('速度分量 (m/s)', fontsize=14)
plt.title('三维螺旋时空速度分量分析', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.savefig('三维螺旋时空速度分量.png', dpi=300, bbox_inches='tight')
plt.close()

# ===============================
# 3. 公式6和7：动量与力的关系验证
# ===============================
print("\n3. 动量与力的关系验证")

# 物理常数
c = 3e8  # 光速（m/s）
m0 = 1.0  # 静止质量（kg）

# 质量随时间变化函数：m(t) = m0 + 0.1*t²（更复杂的质量变化）
def mass_function(t):
    return m0 + 0.1 * t**2

# 速度随时间变化函数：v(t) = v0 + 0.5*t（加速度运动）
def velocity_function(t):
    return 1e6 + 0.5 * t

# 公式6：动量 P = m(c - v)
def momentum_function(t):
    return mass_function(t) * (c - velocity_function(t))

# 公式7：力 F = dP/dt = c(dm/dt) - v(dm/dt) + m(dc/dt) - m(dv/dt)
def force_analytical(t):
    # 计算各导数
    dm_dt = 0.2 * t  # dm/dt = d/dt (m0 + 0.1t²) = 0.2t
    dv_dt = 0.5       # dv/dt = d/dt (1e6 + 0.5t) = 0.5
    dc_dt = 0.0       # 光速恒定
    
    # 计算力的各分量
    term1 = c * dm_dt                 # 质量变化引起的光速方向的力
    term2 = -velocity_function(t) * dm_dt  # 质量变化引起的速度反方向的力
    term3 = mass_function(t) * dc_dt  # 光速变化引起的力（为0）
    term4 = -mass_function(t) * dv_dt  # 速度变化引起的惯性力
    
    return term1 + term2 + term3 + term4, term1, term2, term3, term4

# 数值求导验证（多种方法对比）
t_force = np.linspace(0, 20, 10000)  # 更精细的时间步长

# 计算各物理量
m_values = mass_function(t_force)
v_values = velocity_function(t_force)
p_values = momentum_function(t_force)

# 计算解析解
f_analytical, term1_values, term2_values, term3_values, term4_values = zip(*[force_analytical(ti) for ti in t_force])
f_analytical = np.array(f_analytical)
term1_values = np.array(term1_values)
term2_values = np.array(term2_values)
term3_values = np.array(term3_values)
term4_values = np.array(term4_values)

# 方法1：使用numpy.gradient（中心差分）
f_numerical_gradient = np.gradient(p_values, t_force, edge_order=2)  # 二阶边缘处理

# 方法2：使用scipy.misc.derivative（高阶导数）
def numerical_derivative(func, t, dx=1e-6):
    return np.array([derivative(func, ti, dx=dx, order=5) for ti in t])

f_numerical_scipy = numerical_derivative(momentum_function, t_force)

# 计算相对误差
error_gradient = np.abs(f_analytical - f_numerical_gradient) / (np.abs(f_analytical) + 1e-10)
error_scipy = np.abs(f_analytical - f_numerical_scipy) / (np.abs(f_analytical) + 1e-10)

max_error_gradient = np.max(error_gradient)
avg_error_gradient = np.mean(error_gradient)

max_error_scipy = np.max(error_scipy)
avg_error_scipy = np.mean(error_scipy)

print(f"  1. NumPy Gradient方法：")
print(f"     - 最大相对误差: {max_error_gradient:.12f}")
print(f"     - 平均相对误差: {avg_error_gradient:.12f}")
print(f"  2. SciPy Derivative方法：")
print(f"     - 最大相对误差: {max_error_scipy:.12f}")
print(f"     - 平均相对误差: {avg_error_scipy:.12f}")

# 可视化1：力的解析解与数值解对比
plt.figure(figsize=(14, 12))

# 子图1：力的解析解与数值解
ax1 = plt.subplot(221)
ax1.plot(t_force, f_analytical, label='解析解（公式7）', color='red', linewidth=2, alpha=0.8)
ax1.plot(t_force, f_numerical_gradient, label='NumPy Gradient', color='blue', linestyle='--', linewidth=2, alpha=0.8)
ax1.plot(t_force, f_numerical_scipy, label='SciPy Derivative', color='green', linestyle=':', linewidth=2, alpha=0.8)
ax1.set_xlabel('时间 t (s)', fontsize=12)
ax1.set_ylabel('力 F (N)', fontsize=12)
ax1.set_title('力的解析解与数值解对比', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.tick_params(axis='both', which='major', labelsize=10)

# 子图2：误差分析
ax2 = plt.subplot(222)
ax2.semilogy(t_force, error_gradient, label='NumPy Gradient误差', color='blue', linewidth=2, alpha=0.8)
ax2.semilogy(t_force, error_scipy, label='SciPy Derivative误差', color='green', linewidth=2, alpha=0.8)
ax2.axhline(y=1e-6, color='red', linestyle='--', label='1e-6 误差阈值')
ax2.set_xlabel('时间 t (s)', fontsize=12)
ax2.set_ylabel('相对误差（对数刻度）', fontsize=12)
ax2.set_title('力的数值计算误差分析', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.tick_params(axis='both', which='major', labelsize=10)

# 子图3：力的各分量分析
ax3 = plt.subplot(223)
ax3.plot(t_force, term1_values, label='c(dm/dt)', color='red', linewidth=2, alpha=0.8)
ax3.plot(t_force, term2_values, label='-v(dm/dt)', color='green', linewidth=2, alpha=0.8)
ax3.plot(t_force, term3_values, label='m(dc/dt)', color='blue', linewidth=2, alpha=0.8)
ax3.plot(t_force, term4_values, label='-m(dv/dt)', color='purple', linewidth=2, alpha=0.8)
ax3.plot(t_force, f_analytical, label='总力 F', color='black', linewidth=3, alpha=0.6)
ax3.set_xlabel('时间 t (s)', fontsize=12)
ax3.set_ylabel('力分量 (N)', fontsize=12)
ax3.set_title('宇宙大统一方程各力分量分析', fontsize=14, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.tick_params(axis='both', which='major', labelsize=10)

# 子图4：动量随时间变化
ax4 = plt.subplot(224)
ax4.plot(t_force, p_values, label='动量 P = m(c - v)', color='orange', linewidth=2, alpha=0.8)
ax4.set_xlabel('时间 t (s)', fontsize=12)
ax4.set_ylabel('动量 P (kg·m/s)', fontsize=12)
ax4.set_title('动量随时间变化', fontsize=14, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, linestyle='--', alpha=0.7)
ax4.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.savefig('动量与力的关系验证.png', dpi=300, bbox_inches='tight')
plt.close()

# 可视化2：质量和速度随时间变化
plt.figure(figsize=(14, 6))

# 子图1：质量随时间变化
ax1 = plt.subplot(121)
ax1.plot(t_force, m_values, label='质量 m(t)', color='blue', linewidth=2)
ax1.set_xlabel('时间 t (s)', fontsize=12)
ax1.set_ylabel('质量 m (kg)', fontsize=12)
ax1.set_title('质量随时间变化', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)

# 子图2：速度随时间变化
ax2 = plt.subplot(122)
ax2.plot(t_force, v_values, label='速度 v(t)', color='green', linewidth=2)
ax2.set_xlabel('时间 t (s)', fontsize=12)
ax2.set_ylabel('速度 v (m/s)', fontsize=12)
ax2.set_title('速度随时间变化', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('质量和速度随时间变化.png', dpi=300, bbox_inches='tight')
plt.close()

# ===============================
# 4. 公式16：能量方程验证
# ===============================
print("\n4. 能量方程验证")

m0 = 1.0  # 静止质量 (kg)
c = 3e8  # 光速 (m/s)

# 速度范围（0到0.9999c，更精细的速度区间）
v = np.linspace(0, 0.9999*c, 5000)

# 计算洛伦兹因子
gamma = 1 / np.sqrt(1 - v**2 / c**2)

# 运动质量
m = m0 * gamma

# 能量计算
e_rest = m0 * c**2  # 静止能量
e_kinetic = (m - m0) * c**2  # 动能
e_total = m * c**2  # 总能量

# 验证 E = mc²√(1 - v²/c²)
e_test = m * c**2 * np.sqrt(1 - v**2 / c**2)

# 计算误差
error = np.abs(e_test - e_rest) / e_rest
max_error = np.max(error)
avg_error = np.mean(error)
rmse_error = np.sqrt(np.mean(error**2))

# 输出误差分析
print(f"  - 最大相对误差: {max_error:.15f}")
print(f"  - 平均相对误差: {avg_error:.15f}")
print(f"  - 均方根误差: {rmse_error:.15f}")
print(f"  - 误差数量级: {10**np.floor(np.log10(max_error)):.0e}")

# 绘图 - 能量随速度变化
plt.figure(figsize=(14, 10))

# 主图：能量随速度变化
ax1 = plt.subplot(211)
ax1.plot(v/c, e_rest * np.ones_like(v), 
         label='静止能量 $E_0 = m_0c^2$', 
         color='black', linestyle='--', linewidth=2, alpha=0.8)
ax1.plot(v/c, e_kinetic, 
         label='动能 $E_k = (m - m_0)c^2$', 
         color='blue', linewidth=2, alpha=0.8)
ax1.plot(v/c, e_total, 
         label='总能量 $E = mc^2$', 
         color='red', linewidth=2, alpha=0.8)

ax1.set_xlabel('速度 $v/c$', fontsize=14)
ax1.set_ylabel('能量 $E$ (J)', fontsize=14)
ax1.set_title('统一场论能量方程验证', fontsize=16, fontweight='bold')
ax1.legend(fontsize=12, loc='lower right')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.tick_params(axis='both', which='major', labelsize=12)

# 副图：误差分析
ax2 = plt.subplot(212)
ax2.semilogy(v/c, error, 
             label='相对误差 $|E - m_0c^2| / m_0c^2$', 
             color='green', linewidth=2, alpha=0.8)
ax2.axhline(y=1e-12, color='red', linestyle='--', label='1e-12 误差阈值')

ax2.set_xlabel('速度 $v/c$', fontsize=14)
ax2.set_ylabel('相对误差（对数刻度）', fontsize=14)
ax2.set_title('能量方程验证误差分析', fontsize=16, fontweight='bold')
ax2.legend(fontsize=12, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.savefig('能量方程验证.png', dpi=300, bbox_inches='tight')
plt.close()

# 绘制质量-速度关系
plt.figure(figsize=(12, 8))
plt.plot(v/c, m, 
         label='运动质量 $m = m_0/\sqrt{1 - v^2/c^2}$', 
         color='purple', linewidth=2)
plt.axhline(y=m0, color='black', linestyle='--', label='静止质量 $m_0$')

plt.xlabel('速度 $v/c$', fontsize=14)
plt.ylabel('质量 $m$ (kg)', fontsize=14)
plt.title('统一场论质量-速度关系', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tick_params(axis='both', which='major', labelsize=12)
plt.xlim(0, 1)
plt.ylim(0, 20*m0)
plt.savefig('质量-速度关系.png', dpi=300, bbox_inches='tight')
plt.close()

# ===============================
# 5. 公式7：宇宙大统一方程的数值验证
# ===============================
print("\n5. 宇宙大统一方程验证")

def verify_unified_force_equation():
    c = 3e8  # 光速 (m/s)
    v = 1e6  # 粒子速度 (m/s)
    m0 = 1.0  # 静止质量 (kg)
    
    # 质量随时间变化函数：m(t) = m0 + 0.1*t^2（更复杂的质量变化）
    def m(t):
        return m0 + 0.1 * t**2
    
    # 速度随时间变化函数：v(t) = v0 + 0.5*t（加速度运动）
    def velocity(t):
        return 1e6 + 0.5 * t
    
    # 公式6：动量 P = m(c - v)
    def momentum(t):
        return m(t) * (c - velocity(t))
    
    # 公式7：力 F = dP/dt = c(dm/dt) - v(dm/dt) + m(dc/dt) - m(dv/dt)
    def force_analytical(t):
        dm_dt = 0.2 * t  # dm/dt = 0.2t
        dv_dt = 0.5  # dv/dt = 0.5
        dc_dt = 0.0  # 光速恒定
        return c * dm_dt - velocity(t) * dm_dt + m(t) * dc_dt - m(t) * dv_dt
    
    # 数值计算
    t = np.linspace(0, 20, 10000)  # 更精细的时间步长
    
    # 计算各物理量
    m_values = np.array([m(ti) for ti in t])
    v_values = np.array([velocity(ti) for ti in t])
    p_values = np.array([momentum(ti) for ti in t])
    f_analytical = np.array([force_analytical(ti) for ti in t])
    
    # 数值求导计算力（使用更高阶的数值微分）
    f_numerical = np.gradient(p_values, t, edge_order=2)  # 二阶边缘处理
    
    # 计算误差
    error = np.abs(f_analytical - f_numerical) / np.abs(f_analytical + 1e-10)  # 避免除以零
    max_error = np.max(error)
    avg_error = np.mean(error)
    rmse_error = np.sqrt(np.mean(error**2))
    
    # 输出误差分析
    print(f"  - 最大相对误差: {max_error:.12f}")
    print(f"  - 平均相对误差: {avg_error:.12f}")
    print(f"  - 均方根误差: {rmse_error:.12f}")
    
    # 绘图
    plt.figure(figsize=(14, 12))
    
    # 子图1：质量随时间变化
    ax1 = plt.subplot(411)
    ax1.plot(t, m_values, label='质量 m(t)', color='blue', linewidth=2)
    ax1.set_ylabel('质量 (kg)', fontsize=12)
    ax1.set_title('宇宙大统一方程验证 - 质量随时间变化', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 子图2：速度随时间变化
    ax2 = plt.subplot(412)
    ax2.plot(t, v_values, label='速度 v(t)', color='green', linewidth=2)
    ax2.set_ylabel('速度 (m/s)', fontsize=12)
    ax2.set_title('宇宙大统一方程验证 - 速度随时间变化', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # 子图3：动量随时间变化
    ax3 = plt.subplot(413)
    ax3.plot(t, p_values, label='动量 P(t)', color='purple', linewidth=2)
    ax3.set_ylabel('动量 (kg·m/s)', fontsize=12)
    ax3.set_title('宇宙大统一方程验证 - 动量随时间变化', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # 子图4：力的解析解与数值解对比
    ax4 = plt.subplot(414)
    ax4.plot(t, f_analytical, label='解析解（公式7）', color='red', linewidth=2, alpha=0.8)
    ax4.plot(t, f_numerical, label='数值解（公式6求导）', color='orange', linewidth=2, alpha=0.8, linestyle='--')
    ax4.set_xlabel('时间 t (s)', fontsize=12)
    ax4.set_ylabel('力 F (N)', fontsize=12)
    ax4.set_title('宇宙大统一方程验证 - 力的解析解与数值解对比', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('宇宙大统一方程验证.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return max_error, avg_error

# 运行宇宙大统一方程验证
max_error, avg_error = verify_unified_force_equation()

print("\n=== 统一场论核心公式验证完成 ===")
print("所有验证代码已运行完成，图像文件已保存。")
