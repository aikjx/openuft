import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 用于3D绘图
import math

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ===================== 1. 核心函数定义（修正光速约束） =====================
def zuft_spiral_trajectory(R0=1.0, omega=0.8, c=1.0, t_range=(0, 10), num_points=1000):
    """
    生成张祥前统一场论的空间螺旋运动轨迹（满足光速约束 (R0ω)² + vz² = c²）
    :param R0: 螺旋圆周半径（空间旋转特征尺度）
    :param omega: 角速度（空间旋转频率）
    :param c: 光速（合速度，归一化为1）
    :param t_range: 时间范围
    :param num_points: 采样点数
    :return: x,y,z 轨迹坐标数组 + 横向/纵向/合速度（验证约束）
    """
    # 步骤1：计算横向速度（切向速度），确保 (R0ω)² ≤ c²（避免虚数）
    v_perp = R0 * omega
    if v_perp >= c:
        raise ValueError(f"横向速度{v_perp}≥光速{c}，违反约束！请减小R0或omega")
    
    # 步骤2：根据光速约束计算纵向速度 vz = √(c² - (R0ω)²)
    v_z = np.sqrt(c**2 - v_perp**2)
    print(f"=== 光速约束验证 ===")
    print(f"横向速度 v⊥ = R0×ω = {R0}×{omega} = {v_perp:.6f}")
    print(f"纵向速度 vz = √(c² - v⊥²) = √({c}² - {v_perp:.6f}²) = {v_z:.6f}")
    print(f"合速度 √(v⊥² + vz²) = √({v_perp:.6f}² + {v_z:.6f}²) = {np.sqrt(v_perp**2 + v_z**2):.6f} = c（光速）")
    
    # 步骤3：生成时间序列和轨迹坐标
    t = np.linspace(t_range[0], t_range[1], num_points)
    x = R0 * np.cos(omega * t)  # 横向圆周运动（x轴）
    y = R0 * np.sin(omega * t)  # 横向圆周运动（y轴）
    z = v_z * t                 # 纵向直线运动（z轴，速度为vz，满足光速约束）
    
    # 步骤4：计算速度（验证导数结果）
    v_x = -R0 * omega * np.sin(omega * t)  # x方向速度（位置对t求导）
    v_y = R0 * omega * np.cos(omega * t)   # y方向速度（位置对t求导）
    v_total = np.sqrt(v_x**2 + v_y**2 + v_z**2)  # 合速度（恒等于c）
    
    return x, y, z, t, v_perp, v_z, v_total

def e_approximation_by_zuft(n_list):
    """
    基于ZUFT空间连续演化模型计算e的近似值（(1+1/n)^n）
    :param n_list: 离散步数列表（n→∞时收敛到e）
    :return: e近似值列表、误差列表
    """
    e_standard = math.e  # 标准自然常数e
    e_approx_list = []
    error_list = []
    
    for n in n_list:
        e_approx = (1 + 1/n) ** n
        e_approx_list.append(e_approx)
        error = abs(e_approx - e_standard)
        error_list.append(error)
    
    return e_approx_list, error_list

# ===================== 2. 主程序：可视化+验证（满足光速约束） =====================
if __name__ == "__main__":
    # -------------------- 2.1 配置参数（满足光速约束） --------------------
    R0 = 1.0    # 螺旋半径
    omega = 0.6 # 角速度（调整此值确保 v⊥=R0×omega < c）
    c = 1.0     # 光速（归一化为1，核心常数）
    t_range = (0, 10)
    num_points = 1000
    
    # -------------------- 2.2 生成轨迹数据（验证光速约束） --------------------
    x, y, z, t, v_perp, v_z, v_total = zuft_spiral_trajectory(R0, omega, c, t_range, num_points)
    
    # -------------------- 2.3 绘制3D螺旋轨迹 --------------------
    fig = plt.figure(figsize=(15, 6))
    
    # 子图1：3D螺旋轨迹（满足光速约束）
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(x, y, z, color='#2E86AB', linewidth=2, label=f'ZUFT螺旋轨迹（合速度=c={c}）')
    ax1.set_xlabel('X (横向旋转)', fontsize=10)
    ax1.set_ylabel('Y (横向旋转)', fontsize=10)
    ax1.set_zlabel('Z (纵向运动)', fontsize=10)
    ax1.set_title('张祥前统一场论：空间螺旋运动（满足光速约束）', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 子图2：合速度验证（恒等于光速c）
    ax2 = fig.add_subplot(122)
    ax2.plot(t, v_total, color='#A23B72', linewidth=2, label='实时合速度')
    ax2.axhline(y=c, color='#F18F01', linestyle='--', linewidth=2, label=f'光速c={c}')
    ax2.set_xlabel('时间 t', fontsize=10)
    ax2.set_ylabel('合速度', fontsize=10)
    ax2.set_title('合速度验证（恒等于光速c）', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # -------------------- 2.4 e的收敛性验证（保留原逻辑） --------------------
    # 生成n的取值（从1到10000，覆盖离散→连续过程）
    n_list = np.linspace(1, 10000, 1000, dtype=int)
    e_approx, error = e_approximation_by_zuft(n_list)
    e_standard = math.e  # 标准e值
    
    # 新建图展示e的收敛性
    fig2 = plt.figure(figsize=(12, 5))
    ax3 = fig2.add_subplot(111)
    ax3.plot(n_list, e_approx, color='#A23B72', linewidth=2, label=f'e近似值 (标准值={e_standard:.10f})')
    ax3.axhline(y=e_standard, color='#F18F01', linestyle='--', linewidth=2, label='标准e值')
    ax3_twin = ax3.twinx()
    ax3_twin.plot(n_list, error, color='#C73E1D', linewidth=1.5, alpha=0.7, label='误差')
    
    ax3.set_xlabel('离散步数n (n→∞为连续运动)', fontsize=10)
    ax3.set_ylabel('e近似值', fontsize=10, color='#A23B72')
    ax3_twin.set_ylabel('与标准e的误差', fontsize=10, color='#C73E1D')
    ax3.set_title('ZUFT模型收敛到自然常数e的过程', fontsize=12, fontweight='bold')
    ax3.set_xscale('log')
    ax3.grid(alpha=0.3)
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=9)
    
    # 调整布局并显示图表
    plt.tight_layout()
    plt.show()
    
    # -------------------- 2.5 数值输出（保留原逻辑） --------------------
    print("\n" + "="*80)
    print("基于ZUFT空间螺旋运动的自然常数e验证结果（满足光速约束）")
    print("="*80)
    key_n = [1, 10, 100, 1000, 10000]
    key_e_approx, key_error = e_approximation_by_zuft(key_n)
    
    for i in range(len(key_n)):
        print(f"n = {key_n[i]:>5d} → e近似值 = {key_e_approx[i]:.10f} | 误差 = {key_error[i]:.15f}")
    
    print("="*80)
    print(f"标准自然常数e = {e_standard:.15f}")
    print(f"当n→∞时，ZUFT模型收敛值 = {e_approx[-1]:.15f}（最终误差 = {error[-1]:.15f}）")
    print("="*80)