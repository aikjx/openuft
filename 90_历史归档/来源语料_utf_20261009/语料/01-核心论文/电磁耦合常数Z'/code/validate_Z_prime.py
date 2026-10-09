import numpy as np
from scipy.constants import c, epsilon_0, hbar, e, G, m_e, m_p, alpha, pi
import matplotlib.pyplot as plt

def calculate_Z_prime():
    """计算Z'的值"""
    Z_prime = c / (8 * pi * epsilon_0)
    return Z_prime

def calculate_Z():
    """计算Z的值（注意：此定义基于张祥前理论，与主流物理学不同）"""
    # 注意：在主流物理学中，G和c是独立常数，此定义存在物理意义问题
    Z = G * c / 2
    return Z

def validate_Z_prime_formulas():
    """验证Z'的两种定义等价性"""
    print("=== 验证 Z' 的两种定义等价性 ===")
    
    # 定义1: Z' = c / (8πε₀)
    Z_prime_def1 = calculate_Z_prime()
    
    # 定义2: Z' = αħc² / (2e²)
    Z_prime_def2 = alpha * hbar * c**2 / (2 * e**2)
    
    print(f"Z' (定义1: c/(8πε₀)) = {Z_prime_def1:.10e}")
    print(f"Z' (定义2: αħc²/(2e²)) = {Z_prime_def2:.10e}")
    relative_error = abs(Z_prime_def1 - Z_prime_def2)/Z_prime_def1
    print(f"相对误差: {relative_error:.10e}")
    
    # 使用相对误差进行比较，更合理
    if relative_error < 1e-8:
        print("✅ 两种定义等价性验证通过！")
    else:
        print("❌ 两种定义等价性验证失败！")
    
    return Z_prime_def1, Z_prime_def2

def validate_Z_formula():
    """验证Z的定义"""
    print("\n=== 验证 Z 的定义 ===")
    
    Z = calculate_Z()
    print(f"Z = Gc/2 = {Z:.10e}")
    print(f"Z的单位: m^4·kg^-1·s^-3")
    
    return Z

def validate_force_ratios(Z, Z_prime):
    """验证力的强度比"""
    print("\n=== 验证力的强度比 ===")
    
    # 电子-电子力比
    F_ratio_ee = (e**2/(4*pi*epsilon_0)) / (G*m_e**2)
    print(f"电子间电磁力/引力比: {F_ratio_ee:.1e}")
    
    # 质子-质子力比
    F_ratio_pp = (e**2/(4*pi*epsilon_0)) / (G*m_p**2)
    print(f"质子间电磁力/引力比: {F_ratio_pp:.1e}")
    
    # 质子-电子力比
    F_ratio_pe = (e**2/(4*pi*epsilon_0)) / (G*m_p*m_e)
    print(f"质子-电子间电磁力/引力比: {F_ratio_pe:.1e}")
    
    # 理论预测的力比与Z'/Z的关系
    Z_ratio = Z_prime / Z
    print(f"\nZ'/Z = {Z_ratio:.10e}")
    
    # 力比与(Z'/Z)*(e/m)^2的关系
    theory_ratio_ee = Z_ratio * (e**2/m_e**2)
    theory_ratio_pp = Z_ratio * (e**2/m_p**2)
    theory_ratio_pe = Z_ratio * (e**2/(m_p*m_e))
    
    print(f"(Z'/Z)*(e/m_e)^2 = {theory_ratio_ee:.1e}")
    print(f"(Z'/Z)*(e/m_p)^2 = {theory_ratio_pp:.1e}")
    print(f"(Z'/Z)*(e²/(m_p*m_e)) = {theory_ratio_pe:.1e}")
    
    # 验证理论预测与实际计算的一致性
    print(f"\n理论预测与实际计算的比较:")
    print(f"电子力比 - 实际: {F_ratio_ee:.1e}, 理论: {theory_ratio_ee:.1e}, 误差: {abs(F_ratio_ee - theory_ratio_ee)/F_ratio_ee:.1e}")
    print(f"质子力比 - 实际: {F_ratio_pp:.1e}, 理论: {theory_ratio_pp:.1e}, 误差: {abs(F_ratio_pp - theory_ratio_pp)/F_ratio_pp:.1e}")
    print(f"质子-电子力比 - 实际: {F_ratio_pe:.1e}, 理论: {theory_ratio_pe:.1e}, 误差: {abs(F_ratio_pe - theory_ratio_pe)/F_ratio_pe:.1e}")
    
    return F_ratio_ee, F_ratio_pp, F_ratio_pe

def validate_vacuum_constants(Z_prime):
    """验证真空常数关系"""
    print("\n=== 验证真空常数关系 ===")
    
    # 真空介电常数与Z'的关系
    epsilon_0_calc = c / (8 * pi * Z_prime)
    print(f"ε₀ (计算值) = {epsilon_0_calc:.10e}")
    print(f"ε₀ (标准值) = {epsilon_0:.10e}")
    print(f"相对误差: {abs(epsilon_0_calc - epsilon_0)/epsilon_0:.10e}")
    
    # 真空磁导率与Z'的关系
    mu_0 = 1 / (epsilon_0 * c**2)
    print(f"μ₀ = 1/(ε₀c²) = {mu_0:.10e}")
    
    # 真空阻抗
    Z_0 = np.sqrt(mu_0 / epsilon_0)
    print(f"真空阻抗 Z₀ = √(μ₀/ε₀) = {Z_0:.10e}")
    
    return epsilon_0_calc

def validate_fine_structure_constant(Z_prime):
    """验证精细结构常数关系"""
    print("\n=== 验证精细结构常数关系 ===")
    
    # 从Z'推导精细结构常数
    alpha_calc = 2 * e**2 * Z_prime / (hbar * c**2)
    print(f"α (计算值) = {alpha_calc:.10e}")
    print(f"α (标准值) = {alpha:.10e}")
    print(f"相对误差: {abs(alpha_calc - alpha)/alpha:.10e}")
    
    if abs(alpha_calc - alpha) < 1e-10:
        print("✅ 精细结构常数关系验证通过！")
    else:
        print("❌ 精细结构常数关系验证失败！")
    
    return alpha_calc

def validate_geometry_factors():
    """验证几何因子"""
    print("\n=== 验证几何因子 ===")
    
    # 经典电磁学的几何因子
    k_e = 1 / (4 * pi * epsilon_0)
    print(f"经典电磁学几何因子: 4π")
    print(f"库仑常数 k_e = 1/(4πε₀) = {k_e:.10e}")
    
    # 张祥前理论的几何因子
    Z_prime_4pi = c / (4 * pi * epsilon_0)
    Z_prime_8pi = calculate_Z_prime()
    print(f"Z' (4π因子) = {Z_prime_4pi:.10e}")
    print(f"Z' (8π因子) = {Z_prime_8pi:.10e}")
    print(f"4π/8π 因子比 = {Z_prime_4pi/Z_prime_8pi:.1f}")
    
    return k_e

def plot_force_ratios():
    """绘制力的强度比图表"""
    print("\n=== 绘制力的强度比图表 ===")
    
    Z = calculate_Z()
    Z_prime = calculate_Z_prime()
    Z_ratio = Z_prime / Z
    
    # 计算不同粒子组合的力比
    particles = ['电子-电子', '质子-电子', '质子-质子']
    mass_ratios = [m_e*m_e, m_p*m_e, m_p*m_p]
    force_ratios = []
    theory_ratios = []
    
    for mass_ratio in mass_ratios:
        # 实际力比
        F_ratio = (e**2/(4*pi*epsilon_0)) / (G*mass_ratio)
        force_ratios.append(F_ratio)
        
        # 理论力比
        theory_ratio = Z_ratio * (e**2/mass_ratio)
        theory_ratios.append(theory_ratio)
    
    # 绘制对数坐标图
    plt.figure(figsize=(10, 6))
    plt.bar(particles, np.log10(force_ratios), alpha=0.6, label='实际力比 (log10)')
    plt.bar(particles, np.log10(theory_ratios), alpha=0.6, label='理论力比 (log10)')
    plt.xlabel('粒子组合')
    plt.ylabel('力强比 (log10)')
    plt.title('不同粒子组合的电磁力/引力强度比')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('force_ratios_comparison.png', dpi=300)
    print("力的强度比图表已保存为 'force_ratios_comparison.png'")
    
    return force_ratios, theory_ratios

def plot_constant_relationships():
    """绘制常数关系图表"""
    print("\n=== 绘制常数关系图表 ===")
    
    Z = calculate_Z()
    Z_prime = calculate_Z_prime()
    
    # 常数对比
    constants = ['Z (引力耦合常数)', 'Z\' (电磁光速几何耦合常数)']
    values = [Z, Z_prime]
    
    # 绘制对数坐标图
    plt.figure(figsize=(10, 6))
    plt.bar(constants, np.log10(values), alpha=0.6, color=['blue', 'red'])
    plt.ylabel('常数数值 (log10)')
    plt.title('引力耦合常数与电磁光速几何耦合常数对比')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('constants_comparison.png', dpi=300)
    print("常数对比图表已保存为 'constants_comparison.png'")
    
    return values

def run_all_validations():
    """运行所有验证"""
    print("\n" + "="*60)
    print("🧪 电磁光速几何耦合常数 Z' 全面验证")
    print("="*60)
    
    Z_prime_def1, Z_prime_def2 = validate_Z_prime_formulas()
    Z = validate_Z_formula()
    F_ratio_ee, F_ratio_pp, F_ratio_pe = validate_force_ratios(Z, Z_prime_def1)
    epsilon_0_calc = validate_vacuum_constants(Z_prime_def1)
    alpha_calc = validate_fine_structure_constant(Z_prime_def1)
    k_e = validate_geometry_factors()
    
    # 绘制图表
    force_ratios, theory_ratios = plot_force_ratios()
    constant_values = plot_constant_relationships()
    
    print("\n" + "="*60)
    print("📋 验证总结")
    print("="*60)
    
    # 检查所有验证是否通过
    all_passed = True
    
    # 使用相对误差进行比较，更合理
    if abs(Z_prime_def1 - Z_prime_def2)/Z_prime_def1 >= 1e-8:
        all_passed = False
    
    if abs(alpha_calc - alpha)/alpha >= 1e-8:
        all_passed = False
    
    if abs(epsilon_0_calc - epsilon_0)/epsilon_0 >= 1e-8:
        all_passed = False
    
    if all_passed:
        print("✅ 所有验证通过！Z' 理论在数学和数值上自洽。")
        print("\n⚠️  注意：虽然理论内部自洽，但与主流物理学框架存在差异，")
        print("特别是关于 G 与 c 的物理依赖关系的解释需要谨慎对待。")
    else:
        print("❌ 部分验证失败！理论存在内部不一致性。")
    
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    run_all_validations()