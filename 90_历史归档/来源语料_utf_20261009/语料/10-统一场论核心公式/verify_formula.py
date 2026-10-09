import math

# 物理常数精确值
c = 299792458  # 光速 (m/s)
G_known = 6.67430e-11  # 万有引力常数 (N·m²/kg²)
epsilon0_known = 8.8541878128e-12  # 真空介电常数 (F/m)

# 计算Z和Z'的原始值（从已知G和epsilon0）
Z_original = G_known * c / 2
Z_prime_original = c / (8 * math.pi * epsilon0_known)

print("=== 原始值计算 ===")
print(f"Z (原始) = Gc/2 = {Z_original:.6e} m⁴/(kg·s³)")
print(f"Z' (原始) = c/(8πε0) = {Z_prime_original:.6e} m⁴·kg/(s⁵·A²)")
print()

# 使用修改后的公式计算G和epsilon0
G_calculated = 2 * Z_original / c
epsilon0_calculated = c / (8 * math.pi * Z_prime_original)

print("=== 修改后公式验证 ===")
print(f"G (计算) = 2Z/c = {G_calculated:.6e} N·m²/kg²")
print(f"G (已知) = {G_known:.6e} N·m²/kg²")
print(f"G 误差: {abs(G_calculated - G_known)/G_known * 100:.10f}%")
print()
print(f"ε0 (计算) = c/(8πZ') = {epsilon0_calculated:.6e} F/m")
print(f"ε0 (已知) = {epsilon0_known:.6e} F/m")
print(f"ε0 误差: {abs(epsilon0_calculated - epsilon0_known)/epsilon0_known * 100:.10f}%")
print()

# 验证公式等价性
print("=== 公式等价性验证 ===")
print("原始公式: Z = Gc/2")
print(f"修改公式: G = 2Z/c")
print(f"验证: 2Z/c = 2*(Gc/2)/c = G ✓")
print()
print("原始公式: Z' = c/(8πε0)")
print(f"修改公式: ε0 = c/(8πZ')")
print(f"验证: c/(8πZ') = c/(8π*(c/(8πε0))) = ε0 ✓")
print()

# 验证数值一致性
print("=== 数值一致性验证 ===")
print(f"Z值验证: {Z_original:.10e}")
print(f"Z'值验证: {Z_prime_original:.10e}")
print()
print(f"G值验证: {G_calculated:.10e} (应等于 {G_known:.10e})")
print(f"ε0值验证: {epsilon0_calculated:.10e} (应等于 {epsilon0_known:.10e})")
print()

# 结论
if abs(G_calculated - G_known) < 1e-20 and abs(epsilon0_calculated - epsilon0_known) < 1e-20:
    print("✅ 验证通过: 修改后的公式与原始公式完全等价，数值计算一致！")
else:
    print("❌ 验证失败: 修改后的公式与原始公式存在差异！")

print()
print("=== 总结 ===")
print("1. G = 2Z/c 是 Z = Gc/2 的等价变形")
print("2. ε0 = c/(8πZ') 是 Z' = c/(8πε0) 的等价变形")
print("3. 数值计算验证显示修改后的公式与原始公式完全一致")
print("4. 修改后的公式形式更直观地展示了物理常数的几何起源")