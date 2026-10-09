import numpy as np
from scipy.constants import c, epsilon_0, hbar, e, G, m_e, m_p, alpha, pi
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import ScalarFormatter

def calculate_Z_prime():
    """计算Z'的值"""
    return c / (8 * pi * epsilon_0)

def calculate_Z():
    """计算Z的值（注意：此定义基于张祥前理论，与主流物理学不同）"""
    # 注意：在主流物理学中，G和c是独立常数，此定义存在物理意义问题
    return G * c / 2

def create_professional_plots():
    """创建专业的可视化图表"""
    print("=== 创建专业可视化图表 ===")
    
    Z = calculate_Z()
    Z_prime = calculate_Z_prime()
    
    # 1. 常数关系的详细图表
    create_constants_relationship_chart(Z, Z_prime)
    
    # 2. 力强比的详细分析
    create_force_ratio_analysis()
    
    # 3. Z'与其他物理常数的关系
    create_physical_constants_relationship()
    
    # 4. 几何因子的可视化
    create_geometry_factor_visualization()
    
    # 5. 精细结构常数关联图表
    create_fine_structure_constant_chart(Z_prime)

def create_constants_relationship_chart(Z, Z_prime):
    """创建常数关系的详细图表"""
    print("\n1. 创建常数关系图表")
    
    # 计算相关常数
    vacuum_impedance = np.sqrt((1/(epsilon_0 * c**2)) / epsilon_0)
    coulomb_constant = 1/(4 * pi * epsilon_0)
    
    # 准备数据
    constants = [
        "引力耦合常数 Z", 
        "电磁光速几何耦合常数 Z'", 
        "库仑常数 1/(4πε₀)", 
        "真空阻抗 Z₀"
    ]
    
    values = [Z, Z_prime, coulomb_constant, vacuum_impedance]
    log_values = np.log10(values)
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    bars = plt.bar(constants, log_values, alpha=0.8)
    
    # 自定义颜色
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # 添加数值标签
    for i, (value, log_val) in enumerate(zip(values, log_values)):
        plt.text(i, log_val + 0.1, f"{value:.2e}", ha='center', va='bottom', fontsize=10)
    
    # 设置图表属性
    plt.ylabel('对数刻度 (log10)', fontsize=12)
    plt.title('物理常数对比分析', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('constants_relationship_detailed.png', dpi=300, bbox_inches='tight')
    print("常数关系图表已保存为 'constants_relationship_detailed.png'")

def create_force_ratio_analysis():
    """创建力强比的详细分析图表"""
    print("\n2. 创建力强比分析图表")
    
    Z = calculate_Z()
    Z_prime = calculate_Z_prime()
    Z_ratio = Z_prime / Z
    
    # 计算不同粒子组合的力比
    particles = ['电子-电子', '质子-电子', '质子-质子']
    mass_combinations = [m_e*m_e, m_p*m_e, m_p*m_p]
    
    # 计算实际力比和理论力比
    actual_ratios = []
    theory_ratios = []
    for mass_comb in mass_combinations:
        # 实际力比
        actual_ratio = (e**2/(4*pi*epsilon_0)) / (G*mass_comb)
        actual_ratios.append(actual_ratio)
        
        # 理论力比
        theory_ratio = Z_ratio * (e**2/mass_comb)
        theory_ratios.append(theory_ratio)
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 位置
    x = np.arange(len(particles))
    width = 0.35
    
    # 绘制柱状图
    plt.bar(x - width/2, np.log10(actual_ratios), width, label='实际力比', alpha=0.8, color='#1f77b4')
    plt.bar(x + width/2, np.log10(theory_ratios), width, label='理论力比', alpha=0.8, color='#ff7f0e')
    
    # 添加误差线
    for i, (actual, theory) in enumerate(zip(actual_ratios, theory_ratios)):
        error = abs(actual - theory)/actual
        plt.errorbar(i - width/2, np.log10(actual), yerr=error/2, fmt='none', c='black', capsize=3)
        plt.errorbar(i + width/2, np.log10(theory), yerr=error/2, fmt='none', c='black', capsize=3)
    
    # 添加数值标签
    for i, (actual, theory) in enumerate(zip(actual_ratios, theory_ratios)):
        plt.text(i - width/2, np.log10(actual) + 0.2, f"{actual:.1e}", ha='center', va='bottom', fontsize=9)
        plt.text(i + width/2, np.log10(theory) + 0.2, f"{theory:.1e}", ha='center', va='bottom', fontsize=9)
    
    # 设置图表属性
    plt.xlabel('粒子组合', fontsize=12)
    plt.ylabel('电磁力/引力比 (log10)', fontsize=12)
    plt.title('不同粒子组合的力强比分析', fontsize=14, fontweight='bold')
    plt.xticks(x, particles, fontsize=11)
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('force_ratio_analysis_detailed.png', dpi=300, bbox_inches='tight')
    print("力强比分析图表已保存为 'force_ratio_analysis_detailed.png'")

def create_physical_constants_relationship():
    """创建Z'与其他物理常数的关系图表"""
    print("\n3. 创建物理常数关系图表")
    
    Z_prime = calculate_Z_prime()
    
    # 计算与Z'相关的其他常数
    constants = {
        "光速 c": c,
        "真空介电常数 ε₀": epsilon_0,
        "基本电荷 e": e,
        "约化普朗克常数 ħ": hbar,
        "精细结构常数 α": alpha
    }
    
    # 创建相关性分析
    plt.figure(figsize=(12, 8))
    
    # 准备数据
    const_names = list(constants.keys())
    const_values = list(constants.values())
    log_values = np.log10(const_values)
    
    # 计算与Z'的相关性
    z_prime_log = np.log10(Z_prime)
    correlations = []
    
    for name, value in constants.items():
        # 计算基于公式的相关性
        if name == "光速 c":
            # Z' ∝ c
            corr = z_prime_log - np.log10(value)
        elif name == "真空介电常数 ε₀":
            # Z' ∝ 1/ε₀
            corr = z_prime_log + np.log10(value)
        elif name == "基本电荷 e":
            # 从 α = e²Z'/(ħc) 推导
            corr = np.log10(alpha) + np.log10(hbar) + np.log10(c) - 2*np.log10(value) - z_prime_log
        elif name == "约化普朗克常数 ħ":
            # 从 α = e²Z'/(ħc) 推导
            corr = np.log10(alpha) + 2*np.log10(e) + z_prime_log - np.log10(c) - np.log10(value)
        elif name == "精细结构常数 α":
            # α = e²Z'/(ħc)
            corr = 2*np.log10(e) + z_prime_log - np.log10(hbar) - np.log10(c) - np.log10(value)
        correlations.append(abs(corr))
    
    # 绘制图表
    x = np.arange(len(const_names))
    width = 0.4
    
    plt.bar(x - width/2, log_values, width, label='常数数值 (log10)', alpha=0.8, color='#1f77b4')
    plt.bar(x + width/2, correlations, width, label='与Z\'的相关性', alpha=0.8, color='#ff7f0e')
    
    # 设置图表属性
    plt.xlabel('物理常数', fontsize=12)
    plt.ylabel('数值/相关性', fontsize=12)
    plt.title('Z\'与其他物理常数的关系分析', fontsize=14, fontweight='bold')
    plt.xticks(x, const_names, rotation=45, ha='right', fontsize=11)
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('physical_constants_relationship.png', dpi=300, bbox_inches='tight')
    print("物理常数关系图表已保存为 'physical_constants_relationship.png'")

def create_geometry_factor_visualization():
    """创建几何因子的可视化图表"""
    print("\n4. 创建几何因子可视化图表")
    
    # 几何因子数据
    factors = ["经典电磁学 (4π)", "张祥前理论 (8π)", "双层螺旋叠加因子 (2)"]
    values = [4*pi, 8*pi, 2]
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 绘制饼图展示几何因子关系
    plt.subplot(1, 2, 1)
    plt.pie([1, 1], labels=['左旋螺旋', '右旋螺旋'], autopct='%1.1f%%', 
            colors=['#1f77b4', '#ff7f0e'], startangle=90)
    plt.title('双层螺旋结构', fontsize=12, fontweight='bold')
    
    # 绘制柱状图比较几何因子
    plt.subplot(1, 2, 2)
    plt.bar(factors, values, alpha=0.8, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.ylabel('几何因子数值', fontsize=12)
    plt.title('几何因子对比', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('geometry_factor_visualization.png', dpi=300, bbox_inches='tight')
    print("几何因子可视化图表已保存为 'geometry_factor_visualization.png'")

def create_fine_structure_constant_chart(Z_prime):
    """创建精细结构常数关联图表"""
    print("\n5. 创建精细结构常数关联图表")
    
    # 从Z'计算精细结构常数（正确公式）
    alpha_calc = e**2 * Z_prime / (hbar * c)
    
    # 比较计算值与标准值
    print(f"计算的精细结构常数 α: {alpha_calc:.10e}")
    print(f"标准精细结构常数 α: {alpha:.10e}")
    print(f"相对误差: {abs(alpha_calc - alpha)/alpha:.10e}")
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 绘制公式关联
    formulas = [
        "Z' = c/(8πε₀)",
        "α = e²Z'/(ħc)",  # 修正后的公式
        "Z = Gc/2",
        "Z'/Z ≈ 1.346×10²⁰"
    ]
    
    # 绘制公式可视化
    plt.text(0.1, 0.8, formulas[0], fontsize=14, fontweight='bold')
    plt.text(0.1, 0.6, formulas[1], fontsize=14, fontweight='bold')
    plt.text(0.1, 0.4, formulas[2], fontsize=14, fontweight='bold')
    plt.text(0.1, 0.2, formulas[3], fontsize=14, fontweight='bold')
    
    # 添加关联箭头
    plt.arrow(0.3, 0.75, 0.2, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
    plt.arrow(0.3, 0.55, 0.2, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
    plt.arrow(0.3, 0.35, 0.2, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
    
    # 添加说明
    plt.text(0.6, 0.7, "联系电磁与引力", fontsize=12, style='italic')
    plt.text(0.6, 0.5, "连接宏观与微观", fontsize=12, style='italic')
    plt.text(0.6, 0.3, "揭示力强差异根源", fontsize=12, style='italic')
    
    # 设置图表属性
    plt.axis('off')
    plt.title('精细结构常数与Z\'的关联', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('fine_structure_constant_chart.png', dpi=300, bbox_inches='tight')
    print("精细结构常数关联图表已保存为 'fine_structure_constant_chart.png'")

if __name__ == "__main__":
    create_professional_plots()
    print("\n=== 专业可视化图表创建完成 ===")
