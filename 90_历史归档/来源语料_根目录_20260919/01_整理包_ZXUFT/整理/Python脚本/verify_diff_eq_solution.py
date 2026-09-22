import sympy as sp

# 定义符号变量
t = sp.Symbol('t')
r = sp.Function('r')(t)
l = sp.Symbol('lambda')

# 1. 演化微分方程
diff_eq = sp.Eq(sp.diff(r, t), l * r)
print("=== 演化微分方程 ===")
print(f"微分方程: {diff_eq}")
print()

# 2. 分离变量法
print("=== 分离变量法 ===")
# 移项
term1 = sp.Eq(1/r * sp.diff(r, t), l)
print(f"分离变量后: {term1}")
print()

# 3. 两边积分
print("=== 两边积分 ===")
left_integral = sp.Integral(1/r, r)
right_integral = sp.Integral(l, t)
print(f"左边积分: {left_integral}")
print(f"右边积分: {right_integral}")
print()

# 计算积分结果
left_result = left_integral.doit()
right_result = right_integral.doit()
print(f"左边积分结果: {left_result}")
print(f"右边积分结果: {right_result}")
print()

# 合并积分结果，添加常数项
C = sp.Symbol('C')
integrated_eq = sp.Eq(left_result, right_result + C)
print(f"积分后的方程: {integrated_eq}")
print()

# 4. 指数化求解
print("=== 指数化求解 ===")
# 两边取指数
exp_eq = sp.Eq(sp.exp(left_result), sp.exp(right_result + C))
print(f"指数化后: {exp_eq}")
print()

# 化简
simplified_eq = sp.Eq(r, sp.exp(C) * sp.exp(l * t))
print(f"化简后: {simplified_eq}")
print()

# 定义初始条件
print("=== 应用初始条件 ===")
t0 = sp.Symbol('t0')
r0 = sp.Symbol('r0')
# 初始条件 r(t0) = r0
initial_condition = simplified_eq.subs(t, t0).subs(r, r0)
print(f"初始条件方程: {initial_condition}")
print()

# 解出常数项
exp_C = sp.solve(initial_condition, sp.exp(C))[0]
print(f"exp(C) = {exp_C}")
print()

# 代入通解
final_solution = simplified_eq.subs(sp.exp(C), exp_C)
print(f"最终解: {final_solution}")
print()

# 特殊情况：t0 = 0
print("=== 特殊情况 t0 = 0 ===")
solution_t0_0 = final_solution.subs(t0, 0)
print(f"t0=0 时的解: {solution_t0_0}")
print()

# 5. 验证解的正确性
print("=== 验证解的正确性 ===")
# 代入微分方程验证
r_sol = solution_t0_0.rhs
derivative_r_sol = sp.diff(r_sol, t)
substituted_eq = sp.Eq(derivative_r_sol, l * r_sol)
simplified_substituted_eq = sp.simplify(substituted_eq)
print(f"代入微分方程: {substituted_eq}")
print(f"化简后: {simplified_substituted_eq}")
print(f"验证结果: {'正确' if simplified_substituted_eq else '错误'}")
print()

# 6. 总结
print("=== 总结 ===")
print("演化微分方程的求解过程验证成功：")
print("1. 分离变量法: 1/r dr = lambda dt")
print("2. 两边积分: ln(r) = lambda t + C")
print("3. 指数化: r = exp(C) * exp(lambda t)")
print("4. 应用初始条件: r(t0) = r0")
print("5. 最终解: r(t) = r0 * exp(lambda (t - t0))")
print("6. 当 t0 = 0 时: r(t) = r0 * exp(lambda t)")
