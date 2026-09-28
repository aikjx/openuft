import numpy as np
import matplotlib.pyplot as plt

# ====================== 1. 定义核心物理常数（国际单位制） ======================
# 库仑常数 1/(4πε₀) (N·m²/C²)
k_coulomb = 8.988e9  
# 真空中的光速 c (m/s)
c = 2.998e8          
# 元电荷 e (C)，单个质子/电子的电荷量
e = 1.602e-19        
# 地球表面重力加速度 g (m/s²)，用于量级对比
g_earth = 9.81       

# ====================== 2. 定义引力场强度计算核心函数 ======================
def calculate_gravitational_field(q, omega, r0, R):
    """
    计算ZUFT框架下匀速圆周运动正电荷产生的引力场强度
    公式：A = (|q| * ω² * r0) / (4πε₀ * c² * R) = |q| * ω² * r0 * k_coulomb / (c² * R)
    
    参数说明（均为国际单位制）：
    q: 电荷量 (C)，正电荷输入正值，负电荷输入负值（取绝对值计算）
    omega: 角速度 (rad/s)
    r0: 电荷轨道半径 (m)
    R: 观测点到轨道中心的距离 (m)
    
    返回值：
    A: 引力场强度 (m/s²)
    A_ratio: 引力场强度与地球重力加速度的比值（便于量级对比）
    """
    # 核心公式计算引力场强度
    A = (np.abs(q) * (omega **2) * r0 * k_coulomb) / ((c** 2) * R)
    # 计算与地球重力的比值
    A_ratio = A / g_earth
    return A, A_ratio

# ====================== 3. 示例1：极端物理场景计算（原文档参数） ======================
print("===== 极端场景计算结果（原文档参数） =====")
# 极端场景参数（原文档设定）
q_extreme = e          # 单个质子电荷 (C)
omega_extreme = 1e16   # 角速度 (rad/s)
r0_extreme = 1e-10     # 轨道半径 (m，原子尺度)
R_extreme = 0.1        # 观测距离 (m)

# 计算场强
A_extreme, A_ratio_extreme = calculate_gravitational_field(
    q=q_extreme,
    omega=omega_extreme,
    r0=r0_extreme,
    R=R_extreme
)

# 输出结果（保留2位有效数字）
print(f"电荷量：{q_extreme:.2e} C (单个质子电荷)")
print(f"角速度：{omega_extreme:.1e} rad/s")
print(f"轨道半径：{r0_extreme:.1e} m")
print(f"观测距离：{R_extreme} m")
print(f"引力场强度：{A_extreme:.2e} m/s²")
print(f"与地球重力的比值：{A_ratio_extreme:.2e} 倍（约1/{1/A_ratio_extreme:.1e} 地球重力）")

# ====================== 4. 示例2：参数变化对场强的影响（可视化） ======================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 基础参考参数（固定值）
q_base = 1e-6          # 参考电荷量 (C，微库级)
omega_base = 1e9       # 参考角速度 (rad/s)
r0_base = 1e-3         # 参考轨道半径 (m，毫米级)
R_base = 1.0           # 参考观测距离 (m)

# --- 子图1：场强随观测距离R的变化（验证1/R衰减） ---
R_range = np.linspace(0.1, 10, 100)  # 观测距离范围：0.1~10m
A_R = [calculate_gravitational_field(q_base, omega_base, r0_base, R)[0] for R in R_range]
axes[0].plot(R_range, A_R, 'b-', linewidth=2, label='引力场强度')
axes[0].set_xlabel('观测距离 R (m)')
axes[0].set_ylabel('引力场强度 A (m/s²)')
axes[0].set_title('场强随观测距离的变化（验证1/R衰减）')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# --- 子图2：场强随角速度ω的变化（验证正比于ω²） ---
omega_range = np.logspace(6, 12, 100)  # 角速度范围：1e6~1e12 rad/s（对数刻度）
A_omega = [calculate_gravitational_field(q_base, omega, r0_base, R_base)[0] for omega in omega_range]
axes[1].plot(omega_range, A_omega, 'r-', linewidth=2, label='引力场强度')
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set_xlabel('角速度 ω (rad/s)（对数刻度）')
axes[1].set_ylabel('引力场强度 A (m/s²)（对数刻度）')
axes[1].set_title('场强随角速度的变化（验证正比于ω²）')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

# --- 子图3：场强随电荷量q的变化（验证线性正比） ---
q_range = np.linspace(1e-9, 1e-5, 100)  # 电荷量范围：1nC~10μC
A_q = [calculate_gravitational_field(q, omega_base, r0_base, R_base)[0] for q in q_range]
axes[2].plot(q_range * 1e6, A_q, 'g-', linewidth=2, label='引力场强度')
axes[2].set_xlabel('电荷量 q (μC)')
axes[2].set_ylabel('引力场强度 A (m/s²)')
axes[2].set_title('场强随电荷量的变化（验证线性正比）')
axes[2].grid(True, alpha=0.3)
axes[2].legend()

plt.tight_layout()
plt.savefig('ZUFT引力场强度分析.png', dpi=300, bbox_inches='tight')
plt.show()

# ====================== 5. 示例3：自定义参数计算（可修改下方参数） ======================
print("\n===== 自定义参数计算结果 =====")
# 可自行修改以下参数，计算任意场景的场强
q_custom = 1e-5       # 自定义电荷量 (C)
omega_custom = 1e10   # 自定义角速度 (rad/s)
r0_custom = 0.01      # 自定义轨道半径 (m)
R_custom = 0.5        # 自定义观测距离 (m)

A_custom, A_ratio_custom = calculate_gravitational_field(
    q=q_custom,
    omega=omega_custom,
    r0=r0_custom,
    R=R_custom
)
print(f"自定义参数：")
print(f"  电荷量：{q_custom:.2e} C")
print(f"  角速度：{omega_custom:.2e} rad/s")
print(f"  轨道半径：{r0_custom:.2e} m")
print(f"  观测距离：{R_custom:.2e} m")
print(f"计算结果：")
print(f"  引力场强度：{A_custom:.2e} m/s²")
print(f"  与地球重力的比值：{A_ratio_custom:.2e} 倍")