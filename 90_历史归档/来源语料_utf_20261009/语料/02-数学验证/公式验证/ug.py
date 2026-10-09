import numpy as np
from scipy import constants
import mpmath as mp
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置seaborn样式
sns.set_style("whitegrid")
sns.set_palette("husl")

def calculate_ug_from_G_precisely(G_value=None, method='mpmath'):
    """
    根据 G = 4πc²/μg 计算 μg
    
    参数:
    G_value: 引力常数值 (m³kg⁻¹s⁻²)，默认使用 CODATA 2018 值
    method: 计算方法 ('numpy', 'scipy', 'mpmath')
    """
    
    # CODATA 2018 引力常数值
    G_codata = 6.67430e-11  # m³kg⁻¹s⁻²
    
    if G_value is None:
        G = G_codata
    else:
        G = G_value
    
    if method == 'numpy':
        # 使用 NumPy 进行计算
        c = constants.c  # 光速
        pi = np.pi
        
        # 计算 μg = 4πc²/G
        ug_numpy = 4 * pi * c**2 / G
        return ug_numpy, 'NumPy (double precision)'
    
    elif method == 'scipy':
        # 使用 SciPy 常量
        c = constants.c
        pi = constants.pi
        
        ug_scipy = 4 * pi * c**2 / G
        return ug_scipy, 'SciPy (double precision)'
    
    elif method == 'mpmath':
        # 使用 mpmath 进行高精度计算
        mp.mp.dps = 50  # 设置 50 位十进制精度
        
        # 高精度常量
        G_mp = mp.mpf(G)
        c_mp = mp.mpf('299792458')  # 精确的光速值 (m/s)
        pi_mp = mp.pi()
        
        # 高精度计算
        ug_mpmath = 4 * pi_mp * c_mp**2 / G_mp
        
        return ug_mpmath, f'mpmath (50 decimal places)'
    
    else:
        raise ValueError("method must be 'numpy', 'scipy', or 'mpmath'")

def verify_Z_equation(G_value=None, c_value=None, method='mpmath'):
    """
    验证引力光速统一方程 Z = Gc/2
    
    参数:
    G_value: 引力常数值 (m³kg⁻¹s⁻²)，默认使用 CODATA 2018 值
    c_value: 光速值 (m/s)，默认使用精确值 299792458
    method: 计算方法 ('numpy', 'scipy', 'mpmath')
    
    返回:
    Z: 张祥前常数，单位 kg⁻¹·m⁴·s⁻³
    """
    # CODATA 2018 引力常数值
    G_codata = 6.67430e-11  # m³kg⁻¹s⁻²
    c_exact = 299792458     # 精确的光速值 (m/s)
    
    if G_value is None:
        G = G_codata
    else:
        G = G_value
        
    if c_value is None:
        c = c_exact
    else:
        c = c_value
    
    if method == 'numpy':
        # 使用 NumPy 进行计算
        Z_numpy = G * c / 2
        return Z_numpy, 'NumPy (double precision)'
        
    elif method == 'scipy':
        # 使用 SciPy 常量
        Z_scipy = G * c / 2
        return Z_scipy, 'SciPy (double precision)'
        
    elif method == 'mpmath':
        # 使用 mpmath 进行高精度计算
        mp.mp.dps = 50  # 设置 50 位十进制精度
        
        # 高精度常量
        G_mp = mp.mpf(G)
        c_mp = mp.mpf(str(c))
        
        # 高精度计算 Z = Gc/2
        Z_mpmath = G_mp * c_mp / 2
        
        return Z_mpmath, f'mpmath (50 decimal places)'
        
    else:
        raise ValueError("method must be 'numpy', 'scipy', or 'mpmath'")
        

def compare_all_methods():
    """比较不同方法的计算结果"""
    
    print("=== 计算 μg = 4πc²/G 的不同精度方法 ===\n")
    
    # NumPy 方法
    ug_np, method_np = calculate_ug_from_G_precisely(method='numpy')
    print(f"{method_np}:")
    print(f"  μg = {ug_np:.15e}")
    print(f"  单位: m·kg⁻¹ (根据公式推导)")
    print()
    
    # SciPy 方法
    ug_sc, method_sc = calculate_ug_from_G_precisely(method='scipy')
    print(f"{method_sc}:")
    print(f"  μg = {ug_sc:.15e}")
    print(f"  单位: m·kg⁻¹")
    print()
    
    # mpmath 高精度方法
    ug_mp, method_mp = calculate_ug_from_G_precisely(method='mpmath')
    print(f"{method_mp}:")
    print(f"  μg = {ug_mp}")
    print(f"  单位: m·kg⁻¹")
    print()
    
    # 精度比较
    print("=== 精度比较 ===")
    print(f"NumPy vs SciPy 差异: {abs(ug_np - ug_sc):.2e}")
    print(f"相对误差: {abs(ug_np - ug_sc)/ug_np*100:.2e}%")
    print()
    
    # 使用用户提供的 G 值
    print("=== 使用用户提供的 G = 4πc²/μg 反推 μg ===")
    # 如果这是标准引力常数公式，我们可以验证
    G_calculated = 4 * np.pi * constants.c**2 / ug_np
    print(f"验证: 4πc²/μg = {G_calculated:.6e}")
    print(f"与 CODATA G = {constants.G:.6e} 的差异: {abs(G_calculated - constants.G):.2e}")

# 安装依赖 (如果需要)
# pip install numpy scipy mpmath

def compare_Z_methods():
    """比较不同方法计算Z=Gc/2的结果"""
    
    print("\n=== 验证引力光速统一方程 Z = Gc/2 ===\n")
    
    # NumPy 方法
    Z_np, method_np = verify_Z_equation(method='numpy')
    print(f"{method_np}:")
    print(f"  Z = {Z_np:.15e}")
    print(f"  单位: kg⁻¹·m⁴·s⁻³ (空间发散密度流)")
    print()
    
    # SciPy 方法
    Z_sc, method_sc = verify_Z_equation(method='scipy')
    print(f"{method_sc}:")
    print(f"  Z = {Z_sc:.15e}")
    print(f"  单位: kg⁻¹·m⁴·s⁻³")
    print()
    
    # mpmath 高精度方法
    Z_mp, method_mp = verify_Z_equation(method='mpmath')
    print(f"{method_mp}:")
    print(f"  Z = {Z_mp}")
    print(f"  单位: kg⁻¹·m⁴·s⁻³")
    print()
    
    # 验证 Z=0.01 近似值的误差
    Z_approx = 0.01
    rel_error = abs(float(Z_mp) - Z_approx) / float(Z_mp) * 100
    print(f"=== Z=0.01 近似值误差分析 ===")
    print(f"精确值 Z = {float(Z_mp):.10f}")
    print(f"近似值 Z ≈ 0.01")
    print(f"绝对误差: {abs(float(Z_mp) - Z_approx):.10f}")
    print(f"相对误差: {rel_error:.6f}%")
    
    # 反向验证: 从Z计算G
    G_from_Z = 2 * float(Z_mp) / constants.c
    print(f"\n=== 反向验证: 从 Z 计算 G ===")
    print(f"G = 2Z/c = {G_from_Z:.15e}")
    print(f"与 CODATA G = {constants.G:.15e} 的差异: {abs(G_from_Z - constants.G):.2e}")
    print(f"相对误差: {abs(G_from_Z - constants.G)/constants.G*100:.6f}%")

if __name__ == "__main__":
    # 执行 μg 计算比较
    compare_all_methods()
    
    # 执行 Z 方程验证
    compare_Z_methods()
    
    # 如果你有特定的 G 值，可以这样使用
    print("\n=== 使用特定 G 值计算 ===")
    G_custom = 6.67430e-11  # 替换为你需要的 G 值
    ug_custom = calculate_ug_from_G_precisely(G_value=G_custom, method='mpmath')
    print(f"使用 G = {G_custom:.6e} 时:")
    print(f"  μg = {ug_custom[0]}")
    
    # 从特定G值计算Z
    Z_custom = verify_Z_equation(G_value=G_custom, method='mpmath')
    print(f"  Z = {Z_custom[0]}")

# 绘图函数

def plot_Z_precision():
    """绘制Z值的精确性验证图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 计算精确Z值
    Z_exact, _ = verify_Z_equation(method='mpmath')
    Z_exact = float(Z_exact)
    Z_approx = 0.01
    
    # 创建数据点
    methods = ['近似值 Z≈0.01', '精确值 Z']
    Z_values = [Z_approx, Z_exact]
    errors = [abs(Z_approx - Z_exact) / Z_exact * 100, 0]
    
    # 绘制柱状图
    bars = ax.bar(methods, Z_values, color=['#ff7675', '#74b9ff'])
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, 
                f'{height:.10f}', 
                ha='center', va='bottom')
    
    # 添加误差线
    ax.errorbar(methods[0], Z_approx, yerr=abs(Z_approx - Z_exact), 
                fmt='none', ecolor='red', capsize=5, label=f'误差: {errors[0]:.6f}%')
    
    # 设置图表属性
    ax.set_title('Z值的精确性验证', fontsize=14)
    ax.set_ylabel('Z值 (kg⁻¹·m⁴·s⁻³)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 显示图表
    plt.tight_layout()
    plt.savefig('Z值精确性验证.png', dpi=300)
    plt.close()

def plot_geometric_factor():
    """绘制几何因子2的证明图（立体角积分与投影分析）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 图1：立体角投影效率随极角θ的变化
    theta = np.linspace(0, np.pi, 1000)
    projection_efficiency = np.abs(np.cos(theta))
    
    ax1.plot(theta, projection_efficiency, 'b-', linewidth=2)
    ax1.fill_between(theta, projection_efficiency, alpha=0.2, color='blue')
    
    # 添加平均投影效率线
    avg_efficiency = 1/2
    ax1.axhline(y=avg_efficiency, color='r', linestyle='--', 
                label=f'平均投影效率 = {avg_efficiency}')
    
    ax1.set_title('投影效率随极角θ的变化', fontsize=12)
    ax1.set_xlabel('极角θ (弧度)', fontsize=10)
    ax1.set_ylabel('投影效率 μ(θ)=|cosθ|', fontsize=10)
    ax1.set_xlim(0, np.pi)
    ax1.set_ylim(0, 1.1)
    ax1.grid(True)
    ax1.legend()
    
    # 图2：立体角积分计算几何因子
    # 模拟三维各向同性场向二维平面的投影
    # 使用蒙特卡洛方法计算平均投影效率
    np.random.seed(42)  # 设置随机种子以获得可重复的结果
    n_samples = 10000
    theta_samples = np.arccos(2 * np.random.rand(n_samples) - 1)  # 均匀采样立体角
    projection_samples = np.abs(np.cos(theta_samples))
    
    avg_projection = np.mean(projection_samples)
    geometric_factor = 1 / avg_projection  # 几何因子η=2
    
    # 绘制采样分布
    ax2.hist(projection_samples, bins=50, density=True, alpha=0.6, color='green')
    ax2.axvline(x=avg_projection, color='purple', linestyle='--', 
                label=f'平均投影效率 = {avg_projection:.6f}')
    ax2.axvline(x=1/2, color='red', linestyle=':', 
                label=f'理论值 = 1/2')
    
    ax2.set_title('投影效率采样分布', fontsize=12)
    ax2.set_xlabel('投影效率 μ', fontsize=10)
    ax2.set_ylabel('概率密度', fontsize=10)
    ax2.set_xlim(0, 1)
    ax2.grid(True)
    ax2.legend()
    
    # 添加整体标题
    plt.suptitle('几何因子2的数学证明：三维到二维投影的统计特性', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 为suptitle留出空间
    plt.savefig('几何因子2的证明.png', dpi=300)
    plt.close()

def plot_G_c_Z_relationship():
    """绘制G、c与Z之间的关系图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 图1：Z随G的变化（固定c）
    G_range = np.linspace(constants.G * 0.9, constants.G * 1.1, 100)
    Z_vs_G = G_range * constants.c / 2
    
    ax1.plot(G_range, Z_vs_G, 'g-', linewidth=2)
    ax1.axvline(x=constants.G, color='red', linestyle='--', label=f'CODATA G = {constants.G:.3e}')
    
    # 获取精确Z值
    Z_exact, _ = verify_Z_equation(method='mpmath')
    ax1.axhline(y=float(Z_exact), color='blue', linestyle='--', label=f'精确Z = {float(Z_exact):.10f}')
    
    ax1.set_title('Z随G的变化（固定c）', fontsize=12)
    ax1.set_xlabel('引力常数G (m³kg⁻¹s⁻²)', fontsize=10)
    ax1.set_ylabel('张祥前常数Z (kg⁻¹·m⁴·s⁻³)', fontsize=10)
    ax1.grid(True)
    ax1.legend()
    
    # 使用科学计数法
    ax1.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(axis='x', style='sci', scilimits=(-2, 2))
    
    # 图2：Z随c的变化（固定G）
    c_range = np.linspace(constants.c * 0.9, constants.c * 1.1, 100)
    Z_vs_c = constants.G * c_range / 2
    
    ax2.plot(c_range, Z_vs_c, 'r-', linewidth=2)
    ax2.axvline(x=constants.c, color='green', linestyle='--', label=f'光速c = {constants.c:.3e}')
    ax2.axhline(y=float(Z_exact), color='blue', linestyle='--', label=f'精确Z = {float(Z_exact):.10f}')
    
    ax2.set_title('Z随c的变化（固定G）', fontsize=12)
    ax2.set_xlabel('光速c (m/s)', fontsize=10)
    ax2.set_ylabel('张祥前常数Z (kg⁻¹·m⁴·s⁻³)', fontsize=10)
    ax2.grid(True)
    ax2.legend()
    
    # 使用科学计数法
    ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis='x', style='sci', scilimits=(-2, 2))
    
    # 添加整体标题
    plt.suptitle('引力光速统一方程 Z = Gc/2 的参数关系分析', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 为suptitle留出空间
    plt.savefig('G_c_Z关系分析.png', dpi=300)
    plt.close()

def create_all_plots():
    """创建所有论文图表"""
    print("\n=== 创建论文图表 ===")
    
    # 绘制Z值的精确性验证图
    plot_Z_precision()
    print("已创建: Z值精确性验证.png")
    
    # 绘制几何因子2的证明图
    plot_geometric_factor()
    print("已创建: 几何因子2的证明.png")
    
    # 绘制G、c与Z之间的关系图
    plot_G_c_Z_relationship()
    print("已创建: G_c_Z关系分析.png")

if __name__ == "__main__":
    # 执行 μg 计算比较
    compare_all_methods()
    
    # 执行 Z 方程验证
    compare_Z_methods()
    
    # 如果你有特定的 G 值，可以这样使用
    print("\n=== 使用特定 G 值计算 ===")
    G_custom = 6.67430e-11  # 替换为你需要的 G 值
    ug_custom = calculate_ug_from_G_precisely(G_value=G_custom, method='mpmath')
    print(f"使用 G = {G_custom:.6e} 时:")
    print(f"  μg = {ug_custom[0]}")
    
    # 从特定G值计算Z
    Z_custom = verify_Z_equation(G_value=G_custom, method='mpmath')
    print(f"  Z = {Z_custom[0]}")
    
    # 创建论文图表
    create_all_plots()