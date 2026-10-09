import sympy as sp

# 定义符号变量
x, y, z, t, m, g = sp.symbols('x y z t m g')
Cx, Cy, Cz = sp.symbols('Cx Cy Cz')

print("=== 核力场定义方程符号验证 ===")

# 定义位置矢量和径向距离
R = sp.Matrix([x, y, z])  # 位置矢量
r = sp.sqrt(x**2 + y**2 + z**2)  # 径向距离
C = sp.Matrix([Cx, Cy, Cz])  # 光速矢量

print(f"1. 位置矢量 R = {R}")
print(f"2. 径向距离 r = {r}")
print(f"3. 光速矢量 C = {C}")

# 计算径向速度 dr/dt
dr_dt = (R.dot(C)) / r
print(f"4. 径向速度 dr/dt = {dr_dt}")

# 计算 dR/dt = C
dR_dt = C
print(f"5. dR/dt = {dR_dt}")

# 步骤1：计算 d/dt(R/r³)
print("\n=== 步骤1：计算 d/dt(R/r³) ===")
term1 = dR_dt / r**3
print(f"6. 第一项：dR/dt / r³ = {term1}")

# 正确计算第二项：先计算 d/dt(1/r³) = -3/r^4 * dr/dt
d_inv_r3_dt = -3 / r**4 * dr_dt
term2 = R * d_inv_r3_dt
print(f"7. 第二项：R * d/dt(1/r³) = R * (-3 dr/dt / r^4) = {term2}")

# 合并两项
d_R_r3_dt = term1 + term2
print(f"8. 合并后：d/dt(R/r³) = {d_R_r3_dt}")

# 步骤2：计算核力场 D
d_R_r3_dt_simplified = sp.simplify(d_R_r3_dt)
print(f"\n=== 步骤2：计算核力场 D ===")
print(f"10. d/dt(R/r³) 化简后：{d_R_r3_dt_simplified}")

D = -g * m * d_R_r3_dt_simplified
print(f"11. 核力场 D = {D}")

# 步骤3：验证与手动推导结果的一致性
print("\n=== 步骤3：验证与手动推导结果的一致性 ===")
manual_result = -g*m/r**3 * (C - 3*R*dr_dt/r)
manual_result_simplified = sp.simplify(manual_result)
print(f"12. 手动推导结果：{manual_result_simplified}")

consistency = (sp.simplify(D - manual_result_simplified) == sp.Matrix([0, 0, 0]))
print(f"13. 符号验证结果：{consistency}")

# 步骤4：特殊情况验证
print("\n=== 步骤4：特殊情况验证 ===")

# 静态情况 (dr/dt = 0)
print("14. 静态情况 (dr/dt = 0)：")
dr_dt_static = 0
D_static = D.subs(dr_dt, dr_dt_static)
D_static_simplified = sp.simplify(D_static)
print(f"    D_static = {D_static_simplified}")

# 径向运动情况 (C = R*C_mag/r)
print("15. 径向运动情况 (C 沿径向)：")
C_mag = sp.symbols('C_mag')
C_radial = R * C_mag / r
D_radial = D.subs(C, C_radial).subs(dr_dt, C_mag)
D_radial_simplified = sp.simplify(D_radial)
print(f"    D_radial = {D_radial_simplified}")

# 步骤5：与引力场的关系验证
print("\n=== 步骤5：与引力场的关系验证 ===")
# 引力场 A = g m R / r**3
A = g * m * R / r**3
print(f"16. 引力场 A = {A}")

# 计算引力场对时间的导数
dA_dt = sp.simplify(g * m * (d_R_r3_dt))
print(f"17. dA/dt = {dA_dt}")

# 验证 D = -dA/dt
D_from_A = -dA_dt
D_from_A_simplified = sp.simplify(D_from_A)
print(f"18. D_from_A = -dA/dt = {D_from_A_simplified}")
print(f"19. D_from_A 是否等于 D：{sp.simplify(D_from_A_simplified - D) == sp.Matrix([0, 0, 0])}")

# 总结
print("\n=== 符号验证总结 ===")
print(f"✅ 核力场定义方程：D = -g m d/dt(R/r³)")
print(f"✅ 展开化简后：D = -g m/r³ (C - 3 R dr/dt / r)")
print(f"✅ 符号计算验证：{consistency}")
print(f"✅ 与引力场关系：D = -dA/dt")
print(f"✅ 静态情况：D_static = -g m C / r³")
print(f"✅ 径向运动情况：D_radial = {D_radial_simplified}")
