# 简单测试计算
c = 299792458
G = 6.67430e-11

# 计算Z = Gc/2
Z_theory = (G * c) / 2
print(f"Z理论值: {Z_theory} (≈ {Z_theory:.2e})")

# 从Z解出G
G_from_Z = (2 * Z_theory) / c
print(f"从Z解出的G: {G_from_Z}")

# 验证文档中的公式 G = k1 * c² / Z
k1 = (G * Z_theory) / (c ** 2)
print(f"比例系数k1: {k1}")

# 测试文档中的公式
G_doc = k1 * (c ** 2) / Z_theory
print(f"文档公式计算的G: {G_doc}")
