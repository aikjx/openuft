import numpy as np
import matplotlib.pyplot as plt

# 1. 计算不同n值下的(1+1/n)^n
print("=== 验证e的极限定义 ===")
print("e = lim(n→∞) (1 + 1/n)^n")
print()

# 定义n值列表
n_values = [1, 10, 100, 1000, 10000, 100000, 1000000]
# 实际e值
e_actual = np.e
print(f"实际e值: {e_actual}")
print()

# 计算并比较
results = []
print("=== 离散逼近的收敛 ===")
print("n		(1 + 1/n)^n		误差")
print("-" * 60)

for n in n_values:
    approximation = (1 + 1/n)**n
    error = abs(approximation - e_actual)
    results.append((n, approximation, error))
    print(f"{n}		{approximation:.10f}		{error:.10f}")

print()

# 2. 验证离散演化模型
print("=== 离散演化模型验证 ===")
print("r_{k+1} = r_k(1 + lambda*dt)")
print()

# 设定参数
lambda_val = 1.0  # 演化常数
T = 1.0  # 总时间
r0 = 1.0  # 初始半径

# 计算不同n值下的演化结果
print("n		离散结果		连续结果		相对误差")
print("-" * 80)

for n in n_values:
    dt = T / n
    r_discrete = r0
    for k in range(n):
        r_discrete *= (1 + lambda_val * dt)
    r_continuous = r0 * np.exp(lambda_val * T)
    relative_error = abs(r_discrete - r_continuous) / r_continuous
    print(f"{n}		{r_discrete:.10f}		{r_continuous:.10f}		{relative_error:.10f}")

print()

# 3. 验证一般时刻t的离散演化
print("=== 一般时刻t的离散演化验证 ===")
print("lim(n→∞) r0*(1 + 1/n)^(nt/T) = r0*e^(t/T)")
print()

# 设定参数
t_val = 0.5  # 验证时刻

print("n		离散结果		连续结果		相对误差")
print("-" * 80)

for n in n_values:
    k = int(n * t_val / T)
    r_discrete = r0 * (1 + 1/n)**k
    r_continuous = r0 * np.exp(t_val / T)
    relative_error = abs(r_discrete - r_continuous) / r_continuous
    print(f"{n}		{r_discrete:.10f}		{r_continuous:.10f}		{relative_error:.10f}")

print()

# 4. 二项式定理展开验证
print("=== 二项式定理展开验证 ===")
def binomial_expansion(n):
    """使用二项式定理计算(1 + 1/n)^n"""
    result = 0
    for k in range(n+1):
        # 计算组合数 C(n, k)
        comb = 1
        for i in range(1, k+1):
            comb *= (n - i + 1) / i
        term = comb * (1/n)**k
        result += term
    return result

print("n		二项式展开		直接计算		误差")
print("-" * 80)

for n in [1, 10, 100, 1000]:  # 限制n值以避免计算时间过长
    binomial_result = binomial_expansion(n)
    direct_result = (1 + 1/n)**n
    error = abs(binomial_result - direct_result)
    print(f"{n}		{binomial_result:.10f}		{direct_result:.10f}		{error:.10f}")

print()

# 5. 级数展开验证
print("=== 级数展开验证 ===")
print("e = sum(k=0→∞) 1/k!")
print()

def series_expansion(terms):
    """使用级数展开计算e"""
    result = 0
    factorial = 1
    for k in range(terms):
        if k > 0:
            factorial *= k
        result += 1 / factorial
    return result

print("项数		级数结果		误差")
print("-" * 50)

for terms in [1, 5, 10, 20, 30]:
    series_result = series_expansion(terms)
    error = abs(series_result - e_actual)
    print(f"{terms}		{series_result:.10f}		{error:.10f}")

print()

# 6. 总结
print("=== 总结 ===")
print("e的极限定义验证成功：")
print("1. 当n→∞时，(1 + 1/n)^n → e")
print("2. 离散演化模型r_{k+1} = r_k(1 + lambda*dt)在dt→0时收敛到连续解r(t) = r0*e^(lambda*t)")
print("3. 二项式定理展开和级数展开都验证了e的数学定义")
print()
print(f"最终验证：e ≈ {e_actual:.10f}")
