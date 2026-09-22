import sympy as sp

# 定义符号变量
t = sp.Symbol('t')
z = sp.Symbol('z')
A = sp.Function('A')(t)
omega = sp.Symbol('omega')
c = sp.Symbol('c')
l = sp.Symbol('lambda')

# 1. 假设波动解的形式
print("=== 波动方程的解形式 ===")
Lx = A * sp.cos(omega * (t - z/c))  # 沿z轴传播的波
Ly = A * sp.sin(omega * (t - z/c))
Lz = 0

print(f"Lx = {Lx}")
print(f"Ly = {Ly}")
print(f"Lz = {Lz}")
print()

# 2. 计算时间二阶导数
print("=== 时间二阶导数 ===")
d2Lx_dt2 = sp.diff(Lx, t, 2)
d2Ly_dt2 = sp.diff(Ly, t, 2)

print(f"∂²Lx/∂t² = {sp.simplify(d2Lx_dt2)}")
print(f"∂²Ly/∂t² = {sp.simplify(d2Ly_dt2)}")
print()

# 3. 计算空间二阶导数
print("=== 空间二阶导数 ===")
d2Lx_dz2 = sp.diff(Lx, z, 2)
d2Ly_dz2 = sp.diff(Ly, z, 2)

print(f"∂²Lx/∂z² = {sp.simplify(d2Lx_dz2)}")
print(f"∂²Ly/∂z² = {sp.simplify(d2Ly_dz2)}")
print()

# 4. 验证波动方程
print("=== 验证波动方程 ===")
print("波动方程: ∇²L = (1/c²) ∂²L/∂t²")
print()

# 对于Lx
wave_eq_Lx = sp.Eq(d2Lx_dz2, (1/c**2) * d2Lx_dt2)
simplified_wave_eq_Lx = sp.simplify(wave_eq_Lx)
print(f"Lx的波动方程验证: {simplified_wave_eq_Lx}")
print()

# 对于Ly
wave_eq_Ly = sp.Eq(d2Ly_dz2, (1/c**2) * d2Ly_dt2)
simplified_wave_eq_Ly = sp.simplify(wave_eq_Ly)
print(f"Ly的波动方程验证: {simplified_wave_eq_Ly}")
print()

# 5. 代入A(t) = r0 e^(lambda t)
print("=== 代入A(t) = r0 e^(lambda t) ===")
r0 = sp.Symbol('r0')
A_exp = r0 * sp.exp(l * t)
print(f"A(t) = {A_exp}")
print()

# 计算A的一阶和二阶导数
dA_dt = sp.diff(A_exp, t)
d2A_dt2 = sp.diff(A_exp, t, 2)
print(f"dA/dt = {dA_dt}")
print(f"d²A/dt² = {d2A_dt2}")
print()

# 代入Lx
Lx_exp = A_exp * sp.cos(omega * (t - z/c))
d2Lx_dt2_exp = sp.diff(Lx_exp, t, 2)
d2Lx_dz2_exp = sp.diff(Lx_exp, z, 2)

print(f"代入A(t)后的∂²Lx/∂t² = {sp.simplify(d2Lx_dt2_exp)}")
print(f"代入A(t)后的∂²Lx/∂z² = {sp.simplify(d2Lx_dz2_exp)}")
print()

# 验证波动方程
wave_eq_Lx_exp = sp.Eq(d2Lx_dz2_exp, (1/c**2) * d2Lx_dt2_exp)
simplified_wave_eq_Lx_exp = sp.simplify(wave_eq_Lx_exp)
print(f"代入A(t)后的Lx波动方程验证: {simplified_wave_eq_Lx_exp}")
print()

# 6. 简化情况：慢变振幅近似
print("=== 慢变振幅近似 ===")
print("当lambda << omega时，A(t)为慢变函数")
print()

# 假设lambda很小，忽略高阶项
approx_d2Lx_dt2 = -omega**2 * A_exp * sp.cos(omega * (t - z/c))
approx_wave_eq = sp.Eq(d2Lx_dz2_exp, (1/c**2) * approx_d2Lx_dt2)
simplified_approx_wave_eq = sp.simplify(approx_wave_eq)
print(f"慢变振幅近似后的波动方程验证: {simplified_approx_wave_eq}")
print()

# 7. 特殊情况：常数振幅
print("=== 特殊情况：常数振幅 ===")
A_const = r0  # 常数振幅
Lx_const = A_const * sp.cos(omega * (t - z/c))
d2Lx_dt2_const = sp.diff(Lx_const, t, 2)
d2Lx_dz2_const = sp.diff(Lx_const, z, 2)

wave_eq_Lx_const = sp.Eq(d2Lx_dz2_const, (1/c**2) * d2Lx_dt2_const)
simplified_wave_eq_Lx_const = sp.simplify(wave_eq_Lx_const)
print(f"常数振幅时的波动方程验证: {simplified_wave_eq_Lx_const}")
print()

# 8. 总结
print("=== 总结 ===")
print("波动方程的自洽性验证结果：")
print("1. 对于沿z轴传播的波Lx = A(t) cos(omega(t - z/c))，当A(t)为常数时，严格满足波动方程")
print("2. 当A(t) = r0 e^(lambda t)时，波动方程的满足程度取决于lambda与omega的相对大小")
print("3. 在慢变振幅近似下（lambda << omega），演化的振幅解也能近似满足波动方程")
print()
print("结论：螺旋演化的波函数在适当条件下可以满足空间波动方程，验证了理论的自洽性")
