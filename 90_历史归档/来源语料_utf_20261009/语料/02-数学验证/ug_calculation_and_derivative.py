import numpy as np
from scipy import constants
import sympy as sp
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

def calculate_ug_from_G():
    """
    根据公式 G = 4πc²/μg 计算 μg 的值
    返回: μg 的数值和单位
    """
    # 基本物理常数
    G = constants.G  # 引力常数, m³·kg⁻¹·s⁻²
    c = constants.c  # 光速, m/s
    pi = constants.pi  # 圆周率
    
    # 计算 μg = 4πc²/G
    ug = 4 * pi * c**2 / G
    
    print("=== 计算 μg 的值 ===")
    print(f"引力常数 G = {G:.10e} m³·kg⁻¹·s⁻²")
    print(f"光速 c = {c:.10e} m/s")
    print(f"圆周率 π = {pi:.10f}")
    print(f"根据公式 G = 4πc²/μg，计算得：")
    print(f"μg = 4πc²/G = {ug:.10e} m·kg⁻¹")
    
    return ug

def symbolic_derivative():
    """
    使用SymPy对公式 G = 4πc²/μg 进行符号求导
    """
    # 定义符号变量
    G_sym, c_sym, pi_sym, ug_sym = sp.symbols('G c π μ_g')
    
    # 定义公式 G = 4πc²/μg
    equation = sp.Eq(G_sym, 4 * pi_sym * c_sym**2 / ug_sym)
    
    print("\n=== 符号求导分析 ===")
    print(f"原公式: {equation}")
    
    # 1. 求解μg的表达式
    ug_expr = sp.solve(equation, ug_sym)[0]
    print(f"求解μg: μ_g = {ug_expr}")
    
    # 2. 对G关于μg求导
    dG_dug = sp.diff(4 * pi_sym * c_sym**2 / ug_sym, ug_sym)
    print(f"dG/dμ_g = {dG_dug}")
    
    # 3. 对μg关于G求导
    dug_dG = sp.diff(ug_expr, G_sym)
    print(f"dμ_g/dG = {dug_dG}")
    
    # 4. 对μg关于c求导
    dug_dc = sp.diff(ug_expr, c_sym)
    print(f"dμ_g/dc = {dug_dc}")
    
    return equation, ug_expr, dG_dug, dug_dG, dug_dc

def numerical_derivative_analysis():
    """
    进行数值导数分析，可视化G和c变化对μg的影响
    """
    # 计算标准值
    G_std = constants.G
    c_std = constants.c
    pi = constants.pi
    ug_std = 4 * pi * c_std**2 / G_std
    
    # 创建数据点
    G_variation = np.linspace(G_std * 0.95, G_std * 1.05, 100)
    c_variation = np.linspace(c_std * 0.95, c_std * 1.05, 100)
    
    # 计算对应的μg值
    ug_G_variation = 4 * pi * c_std**2 / G_variation
    ug_c_variation = 4 * pi * c_variation**2 / G_std
    
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 绘制G变化对μg的影响
    ax1.plot(G_variation, ug_G_variation, 'b-', linewidth=2)
    ax1.axvline(x=G_std, color='r', linestyle='--', label=f'标准G值: {G_std:.2e}')
    ax1.axhline(y=ug_std, color='g', linestyle='--', label=f'标准μg值: {ug_std:.2e}')
    ax1.set_title('G变化对μg的影响', fontsize=14)
    ax1.set_xlabel('引力常数G (m³·kg⁻¹·s⁻²)', fontsize=12)
    ax1.set_ylabel('空间-质量耦合常数μg (m·kg⁻¹)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # 绘制c变化对μg的影响
    ax2.plot(c_variation, ug_c_variation, 'r-', linewidth=2)
    ax2.axvline(x=c_std, color='b', linestyle='--', label=f'标准c值: {c_std:.2e}')
    ax2.axhline(y=ug_std, color='g', linestyle='--', label=f'标准μg值: {ug_std:.2e}')
    ax2.set_title('c变化对μg的影响', fontsize=14)
    ax2.set_xlabel('光速c (m/s)', fontsize=12)
    ax2.set_ylabel('空间-质量耦合常数μg (m·kg⁻¹)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    # 设置科学计数法显示
    ax1.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    ax2.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    
    plt.tight_layout()
    plt.savefig('ug变化敏感性分析.png', dpi=300)
    plt.close()
    
    print("\n=== 数值导数分析完成 ===")
    print("已生成 'ug变化敏感性分析.png' 图表，显示G和c变化对μg的影响")

def verify_consistency():
    """
    验证计算结果的一致性
    """
    # 计算μg
    ug = calculate_ug_from_G()
    
    # 反向验证G
    G_calculated = 4 * constants.pi * constants.c**2 / ug
    G_actual = constants.G
    
    error = abs(G_calculated - G_actual) / G_actual * 100
    
    print("\n=== 结果一致性验证 ===")
    print(f"反向计算G = 4πc²/μg = {G_calculated:.10e} m³·kg⁻¹·s⁻²")
    print(f"CODATA G值 = {G_actual:.10e} m³·kg⁻¹·s⁻²")
    print(f"相对误差 = {error:.10f}%")
    print(f"计算精度: {'极高' if error < 1e-6 else '高' if error < 1e-3 else '一般'}")

def main():
    """
    主函数
    """
    print("=== G = 4πc²/μg 公式分析与求导演示 ===\n")
    
    # 1. 计算ug的值
    verify_consistency()
    
    # 2. 符号求导
    symbolic_derivative()
    
    # 3. 数值导数分析
    numerical_derivative_analysis()
    
    print("\n=== 分析完成 ===")
    print(f"空间-质量耦合常数μg的值约为 {calculate_ug_from_G():.3e} m·kg⁻¹")
    print("注：此值表示空间与质量之间的耦合强度，在统一场论中具有重要物理意义。")

if __name__ == "__main__":
    main()