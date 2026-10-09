import math
import numpy as np
from scipy import integrate

# 设置高精度计算
np.set_printoptions(precision=10)

print("===== 几何因子2推导的积分验证 =====")
print("积分公式：⟨μ⟩ = (1/(4π)) ∫₀²π ∫₀^π |cosθ| sinθ dθ dφ ")
print()

# 1. 解析计算
dphi_result = 2 * math.pi
integral_theta = 1.0
avg_mu_analytic = (dphi_result * integral_theta) / (4 * math.pi)
geometric_factor_analytic = 1.0 / avg_mu_analytic

print("1. 解析计算：")
print(f"  ∫₀²π dφ = {dphi_result}")
print(f"  ∫₀^π |cosθ| sinθ dθ = {integral_theta}")
print(f"  ⟨μ⟩ = ({dphi_result} * {integral_theta}) / (4π) = {avg_mu_analytic}")
print(f"  η = 1/⟨μ⟩ = {geometric_factor_analytic}")
print()

# 2. 数值积分验证
# 定义被积函数
def integrand_theta(theta):
    return abs(math.cos(theta)) * math.sin(theta)

# 数值计算∫₀^π |cosθ| sinθ dθ
numerical_theta, error_theta = integrate.quad(integrand_theta, 0, math.pi)

# 数值计算∫₀²π ∫₀^π |cosθ| sinθ dθ dφ
numerical_double = dphi_result * numerical_theta

# 数值计算平均投影效率
avg_mu_numerical = numerical_double / (4 * math.pi)

# 数值计算几何因子
geometric_factor_numerical = 1.0 / avg_mu_numerical

print("2. 数值积分验证：")
print(f"  数值计算∫₀^π |cosθ| sinθ dθ = {numerical_theta:.8f} (误差: {error_theta:.8f})")
print(f"  数值计算∫₀²π ∫₀^π |cosθ| sinθ dθ dφ = {numerical_double:.8f} (误差: {error_theta * dphi_result:.8f})")
print(f"  数值计算⟨μ⟩ = {numerical_double:.8f} / (4π) = {avg_mu_numerical:.8f}")
print(f"  数值计算η = 1/⟨μ⟩ = {geometric_factor_numerical:.8f}")
print()

print("结论：方法一、二、四、五的积分计算正确，确实得出平均投影效率1/2，几何因子η=2。")
print()
print()

print("===== 方法三：方向组合积分法 =====")
print("积分公式：I_total = ∫₀²π ∫₀^π ∫₀²π ∫₀^π sinθ₁ sinθ₂ cos²(φ₁-φ₂) dθ₁ dφ₁ dθ₂ dφ₂")
print()

# 1. 正确的解析计算
phi_integral_exact = 2 * math.pi * math.pi  # ∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = 2π²
single_theta_integral_exact = 2.0  # ∫₀^π sinθ dθ = 2
theta_integral_product_exact = single_theta_integral_exact ** 2  # (∫₀^π sinθ dθ)² = 4
correct_I_total_exact = (theta_integral_product_exact * phi_integral_exact) / (2 * math.pi) ** 2

print("1. 正确的解析计算：")
print(f"  方位角积分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = {phi_integral_exact}")
print(f"  单个极角积分：∫₀^π sinθ dθ = {single_theta_integral_exact}")
print(f"  极角积分乘积：(∫₀^π sinθ dθ)² = {theta_integral_product_exact}")
print(f"  正确的I_total = ({theta_integral_product_exact} * {phi_integral_exact}) / (2π)² = {correct_I_total_exact}")
print()

# 2. 文档中的错误计算
print("2. 文档中的错误计算：")
print("   文档中错误地将极角积分写成4π，导致后续归一化出现问题")
print()

# 3. 数值积分验证
# 定义方位角积分的被积函数
def integrand_phi(phi1, phi2):
    return math.cos(phi1 - phi2) ** 2

# 数值计算方位角积分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂
numerical_phi, error_phi = integrate.dblquad(
    integrand_phi, 0, 2*math.pi, lambda x: 0, lambda x: 2*math.pi
)

# 数值计算单个极角积分：∫₀^π sinθ dθ
single_theta_numerical, error_single_theta = integrate.quad(math.sin, 0, math.pi)

# 数值计算四维积分：I_total
four_dim_integral = single_theta_numerical ** 2 * numerical_phi

print("3. 数值积分验证：")
print(f"  数值计算方位角积分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = {numerical_phi:.8f} (误差: {error_phi:.8f})")
print(f"  数值计算单个极角积分：∫₀^π sinθ dθ = {single_theta_numerical:.8f} (误差: {error_single_theta:.8f})")
print(f"  数值计算四维积分：I_total = {four_dim_integral:.8f} (误差: {error_single_theta**2 * error_phi:.8f})")
print()

print("结论：方法三在极角积分处理上存在错误，正确计算显示其结果并不直接给出1/2的平均投影效率。")
print("      这表明需要重新审视该方法的物理归一化方式，或者该方法本身的推导逻辑存在问题。")

# 额外添加方法三的详细分析
def analyze_method3():
    print("\n\n===== 方法三错误详细分析 =====")
    print("文档中方法三存在的问题：")
    print("1. 极角积分的错误处理：")
    print("   文档中错误地计算极角积分 I_theta = 4π")
    print("   正确的极角积分应为单个角度积分：∫₀^π sinθ dθ = 2")
    print()
    print("2. 总相互作用因子的错误计算：")
    print("   文档中计算：I_total = (4π)^2 * (2π²) / (2π)^2 = 8π²")
    print("   正确的计算应为：I_total = (2)^2 * (2π²) / (2π)^2 = 2")
    print()
    print("3. 归一化过程的错误：")
    print("   文档中使用 (4π)^2 = 16π² 作为归一化因子是错误的")
    print("   正确的归一化应基于实际的积分物理意义")
    print()
    print("建议修复方案：")
    print("1. 重新推导方法三，正确处理极角积分和归一化步骤")
    print("2. 确保积分结果与其他方法的结论一致，即几何因子η=2")
    print("3. 明确解释方法三的物理意义，确保与统一场论的基本假设一致")

analyze_method3()