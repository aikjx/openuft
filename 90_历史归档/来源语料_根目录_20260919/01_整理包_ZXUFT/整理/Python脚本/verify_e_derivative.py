import math
import numpy as np
import matplotlib.pyplot as plt

# 1. 验证极限定理: (1 + 1/n)^n → e 当n→∞时
def verify_limit_e():
    print("=== 验证极限定理: (1 + 1/n)^n → e ===")
    # 计算不同n值的(1 + 1/n)^n
    n_values = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 10000]
    exact_e = math.e
    
    print(f"精确e值: {exact_e:.10f}")
    print("n值\t\t(1 + 1/n)^n\t\t误差\t\t相对误差")
    print("-" * 80)
    
    for n in n_values:
        approx_e = (1 + 1/n)**n
        error = abs(approx_e - exact_e)
        rel_error = error / exact_e * 100
        print(f"{n}\t\t{approx_e:.10f}\t\t{error:.6f}\t\t{rel_error:.4f}%")
    
    # 验证误差收敛速度 O(1/n)
    print("\n=== 验证误差收敛速度 O(1/n) ===")
    for n in [10, 100, 1000, 10000]:
        approx_e = (1 + 1/n)**n
        error = abs(approx_e - exact_e)
        theoretical_error = math.e / (2 * n)  # 理论误差 O(1/n)
        print(f"n={n}: 实际误差={error:.6f}, 理论误差≈{theoretical_error:.6f}, 比值={error/theoretical_error:.2f}")

# 2. 验证导数性质: d/dx(e^x) = e^x
def verify_derivative_e():
    print("\n=== 验证导数性质: d/dx(e^x) = e^x ===")
    
    # 使用数值微分近似导数
    def numerical_derivative(f, x, h=1e-8):
        return (f(x + h) - f(x)) / h
    
    # 测试点
    test_points = [0, 1, 2, 3, 5]
    
    print("x值\t\te^x\t\t数值导数\t\t误差")
    print("-" * 80)
    
    for x in test_points:
        exact_value = math.exp(x)
        numerical_deriv = numerical_derivative(math.exp, x)
        error = abs(numerical_deriv - exact_value)
        print(f"{x}\t\t{exact_value:.6f}\t\t{numerical_deriv:.6f}\t\t{error:.10f}")

# 3. 验证离散差分到连续导数的过渡
def verify_discrete_to_continuous():
    print("\n=== 验证离散差分到连续导数的过渡 ===")
    
    # 离散模型: r(t) = (1 + 1/n)^(n*t)
    def discrete_model(t, n):
        return (1 + 1/n)**(n * t)
    
    # 连续模型: r(t) = e^t
    def continuous_model(t):
        return math.exp(t)
    
    # 测试时间点
    t = 1.0
    
    print(f"在t={t}处的比较:")
    print("n值\t\t离散模型值\t\t连续模型值\t\t误差")
    print("-" * 80)
    
    n_values = [10, 100, 1000, 10000]
    for n in n_values:
        discrete_value = discrete_model(t, n)
        continuous_value = continuous_model(t)
        error = abs(discrete_value - continuous_value)
        print(f"{n}\t\t{discrete_value:.6f}\t\t{continuous_value:.6f}\t\t{error:.6f}")
    
    # 验证离散差分等于当前值
    print("\n验证离散差分等于当前值:")
    print("n值\t\t离散值r(t)\t\t离散差分Δr/Δt")
    print("-" * 80)
    
    for n in n_values:
        delta_t = 1/n
        r_t = discrete_model(t, n)
        r_t_plus = discrete_model(t + delta_t, n)
        delta_r = r_t_plus - r_t
        discrete_deriv = delta_r / delta_t
        print(f"{n}\t\t{r_t:.6f}\t\t{discrete_deriv:.6f}")

# 4. 可视化收敛过程
def visualize_convergence():
    print("\n=== 可视化收敛过程 ===")
    
    # 生成n值
    n_values = np.logspace(0, 5, 100, dtype=int)
    approx_e_values = []
    exact_e = math.e
    
    for n in n_values:
        approx_e = (1 + 1/n)**n
        approx_e_values.append(approx_e)
    
    # 绘制收敛曲线
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, approx_e_values, 'b-', label='(1 + 1/n)^n')
    plt.axhline(y=exact_e, color='g', linestyle='--', label=f'exact e = {exact_e:.6f}')
    plt.xscale('log')
    plt.xlabel('n')
    plt.ylabel('(1 + 1/n)^n')
    plt.title('Convergence of (1 + 1/n)^n to e')
    plt.legend()
    plt.grid(True)
    plt.savefig('convergence_plot.png')
    print("收敛曲线已保存为 convergence_plot.png")

# 5. 验证复合函数导数: d/dx(e^λx) = λe^λx
def verify_compound_derivative():
    print("\n=== 验证复合函数导数: d/dx(e^λx) = λe^λx ===")
    
    λ = 2.0  # 任意常数
    
    def compound_function(x):
        return math.exp(λ * x)
    
    def analytical_derivative(x):
        return λ * math.exp(λ * x)
    
    def numerical_derivative(f, x, h=1e-8):
        return (f(x + h) - f(x)) / h
    
    test_points = [0, 1, 2, 3]
    print(f"λ = {λ}")
    print("x值\t\te^λx\t\t解析导数\t\t数值导数\t\t误差")
    print("-" * 80)
    
    for x in test_points:
        f_x = compound_function(x)
        analytical_deriv = analytical_derivative(x)
        numerical_deriv = numerical_derivative(compound_function, x)
        error = abs(numerical_deriv - analytical_deriv)
        print(f"{x}\t\t{f_x:.6f}\t\t{analytical_deriv:.6f}\t\t{numerical_deriv:.6f}\t\t{error:.10f}")

if __name__ == "__main__":
    verify_limit_e()
    verify_derivative_e()
    verify_discrete_to_continuous()
    visualize_convergence()
    verify_compound_derivative()
    print("\n=== 验证完成 ===")
