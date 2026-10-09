import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

print("===== 几何因子2推导的积分验证 =====")
print("积分公式：⟨μ⟩ = (1/(4π)) ∫₀²π ∫₀^π |cosθ| sinθ dθ dφ")

# 1. 解析计算
print("\n1. 解析计算：")
phi_integral = 2 * np.pi  # ∫₀²π dφ = 2π

# 计算 ∫₀^π |cosθ| sinθ dθ
theta_integral = 1  # 可以通过变量替换证明

avg_mu_analytical = (phi_integral * theta_integral) / (4 * np.pi)
eta_analytical = 1 / avg_mu_analytical

print(f"  ∫₀²π dφ = {phi_integral}")
print(f"  ∫₀^π |cosθ| sinθ dθ = {theta_integral}")
print(f"  ⟨μ⟩ = ({phi_integral} * {theta_integral}) / (4π) = {avg_mu_analytical}")
print(f"  η = 1/⟨μ⟩ = {eta_analytical}")

# 2. 数值积分验证
print("\n2. 数值积分验证：")

# 定义被积函数
def integrand_theta(theta):
    return np.abs(np.cos(theta)) * np.sin(theta)

def integrand(theta, phi):
    return np.abs(np.cos(theta)) * np.sin(theta)

# 数值计算θ积分
theta_integral_numerical, theta_error = integrate.quad(integrand_theta, 0, np.pi)

# 数值计算双重积分
double_integral_numerical, double_error = integrate.nquad(integrand, [[0, np.pi], [0, 2*np.pi]])

avg_mu_numerical = double_integral_numerical / (4 * np.pi)
eta_numerical = 1 / avg_mu_numerical

print(f"  数值计算∫₀^π |cosθ| sinθ dθ = {theta_integral_numerical:.8f} (误差: {theta_error:.8f})")
print(f"  数值计算∫₀²π ∫₀^π |cosθ| sinθ dθ dφ = {double_integral_numerical:.8f} (误差: {double_error:.8f})")
print(f"  数值计算⟨μ⟩ = {double_integral_numerical:.8f} / (4π) = {avg_mu_numerical:.8f}")
print(f"  数值计算η = 1/⟨μ⟩ = {eta_numerical:.8f}")

print("\n结论：方法一、二、四、五的积分计算正确，确实得出平均投影效率1/2，几何因子η=2。")

# =============================================================================
# 方法三：方向组合积分法
# =============================================================================
print("\n\n===== 方法三：方向组合积分法 =====")
print("积分公式：I_total = ∫₀²π ∫₀^π ∫₀²π ∫₀^π sinθ₁ sinθ₂ cos²(φ₁-φ₂) dθ₁ dφ₁ dθ₂ dφ₂")

# 1. 解析计算（按正确方式）
print("\n1. 正确的解析计算：")

# 方位角部分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = 2π²
phi_integral_part = 2 * np.pi**2
print(f"  方位角积分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = {phi_integral_part}")

# 极角部分：∫₀^π sinθ dθ = 2（单个极角积分）
single_theta_integral = 2
print(f"  单个极角积分：∫₀^π sinθ dθ = {single_theta_integral}")

# 两个极角积分的乘积
theta_integral_product = single_theta_integral**2
print(f"  极角积分乘积：(∫₀^π sinθ dθ)² = {theta_integral_product}")

# 总积分
I_total_correct = theta_integral_product * phi_integral_part / (2 * np.pi)**2
print(f"  正确的I_total = ({theta_integral_product} * {phi_integral_part}) / (2π)² = {I_total_correct}")

# 文档中的错误计算
print("\n2. 文档中的错误计算：")
print("   文档中错误地将极角积分写成4π，导致后续归一化出现问题")

# 3. 数值积分验证
print("\n3. 数值积分验证：")

# 定义被积函数
def integrand_phi(phi1, phi2):
    return np.cos(phi1 - phi2)**2

def integrand_theta3(theta):
    return np.sin(theta)

def integrand_3d(theta1, phi1, theta2, phi2):
    return np.sin(theta1) * np.sin(theta2) * np.cos(phi1 - phi2)**2

# 数值计算方位角部分积分
phi_integral_numerical, phi_error = integrate.nquad(integrand_phi, [[0, 2*np.pi], [0, 2*np.pi]])

# 数值计算单个极角积分
theta_integral_numerical3, theta_error3 = integrate.quad(integrand_theta3, 0, np.pi)

# 数值计算四维积分
four_d_integral_numerical, four_d_error = integrate.nquad(integrand_3d, [[0, np.pi], [0, 2*np.pi], [0, np.pi], [0, 2*np.pi]])

print(f"  数值计算方位角积分：∫₀²π∫₀²π cos²(φ₁-φ₂) dφ₁ dφ₂ = {phi_integral_numerical:.8f} (误差: {phi_error:.8f})")
print(f"  数值计算单个极角积分：∫₀^π sinθ dθ = {theta_integral_numerical3:.8f} (误差: {theta_error3:.8f})")
print(f"  数值计算四维积分：I_total = {four_d_integral_numerical:.8f} (误差: {four_d_error:.8f})")

print("\n结论：方法三在极角积分处理上存在错误，正确计算显示其结果并不直接给出1/2的平均投影效率。")
print("      这表明需要重新审视该方法的物理归一化方式，或者该方法本身的推导逻辑存在问题。")

# =============================================================================
# 可视化不同角度下的投影效率
# =============================================================================
print("\n\n===== 投影效率可视化 =====")

# 生成θ角度序列
theta = np.linspace(0, np.pi, 1000)
projection_efficiency = np.abs(np.cos(theta)) * np.sin(theta)

# 绘制投影效率随角度的变化
plt.figure(figsize=(10, 6))
plt.plot(np.rad2deg(theta), projection_efficiency, 'b-', linewidth=2)
plt.axhline(y=avg_mu_analytical, color='r', linestyle='--', label=f'平均投影效率 = {avg_mu_analytical}')
plt.title('投影效率随极角θ的变化')
plt.xlabel('极角θ (度)')
plt.ylabel('投影效率 μ(θ) = |cosθ|·sinθ')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('d:\\a10\\aikjx\\code\\my_lib\\投影效率可视化.png', dpi=300, bbox_inches='tight')
print("  投影效率可视化图已保存：投影效率可视化.png")

# =============================================================================
# 总体结论
# =============================================================================
print("\n\n===== 总体结论 =====")
print("1. 方法一、二、四、五的积分计算是正确的，确实得出平均投影效率1/2，几何因子η=2。")
print("2. 方法三在极角积分时存在错误，导致其结论可靠性存疑。")
print("3. 几何因子2确实是三维各向同性场在二维平面上投影的固有统计属性。")