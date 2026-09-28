#!/usr/bin/env python3
"""
简单验证耦合系数f的量纲推导
"""

print("耦合系数f的量纲验证")
print("=" * 60)

# 使用字典表示量纲，键为基本量，值为指数
# 例如：{"L": 1, "M": 0, "T": -1, "I": 0} 表示 LT⁻¹

def format_dim(dim):
    """格式化量纲输出"""
    parts = []
    for key, val in dim.items():
        if val != 0:
            parts.append(f"{key}^{val}")
    return "·".join(parts) if parts else "1"

def multiply_dim(dim1, dim2):
    """量纲乘法"""
    result = dim1.copy()
    for key, val in dim2.items():
        result[key] = result.get(key, 0) + val
    return result

def divide_dim(dim1, dim2):
    """量纲除法"""
    result = dim1.copy()
    for key, val in dim2.items():
        result[key] = result.get(key, 0) - val
    return result

# 基本量纲模板
base_dim = {"L": 0, "M": 0, "T": 0, "I": 0}

# 固定物理量量纲（经典电磁学定义）
E = {"L": 1, "M": 1, "T": -3, "I": -1}  # 电场强度 [E] = MLT⁻³I⁻¹
B = {"L": 0, "M": 1, "T": -2, "I": -1}  # 磁感应强度 [B] = MT⁻²I⁻¹
V = {"L": 1, "M": 0, "T": -1, "I": 0}  # 速度 [V] = LT⁻¹
c = V.copy()                               # 光速 [c] = LT⁻¹
nabla = {"L": -1, "M": 0, "T": 0, "I": 0}  # 空间算子 [∇] = L⁻¹
partial_t = {"L": 0, "M": 0, "T": -1, "I": 0}  # 时间微分算子 [∂/∂t] = T⁻¹

# 定义1：A为磁矢势 ([A] = MLT⁻²I⁻¹)
print("\n=== 定义1：A为磁矢势 ([A] = MLT⁻²I⁻¹) ===")

A_def1 = {"L": 1, "M": 1, "T": -2, "I": -1}  # 磁矢势量纲

# 验证方程1：∇×A = B/f
print("\n1. 验证方程：∇×A = B/f")
left = multiply_dim(nabla, A_def1)  # ∇×A的量纲
print(f"   左侧量纲：∇×A = {format_dim(left)}")
print(f"   右侧量纲：B/f = {format_dim(B)} / [f]")
print(f"   等式成立条件：{format_dim(left)} = {format_dim(B)} / [f]")

# 解f的量纲
# [f] = B / (∇×A)
f_dim1 = divide_dim(B, left)
print(f"   解得[f] = {format_dim(B)} / {format_dim(left)} = {format_dim(f_dim1)}")

if all(val == 0 for val in f_dim1.values()):
    print("   ✅ 正确：f为无量纲量 [f] = 1")
else:
    print("   ❌ 错误：f的量纲推导有误")

# 验证方程2：E = -f dA/dt
print("\n2. 验证方程：E = -f dA/dt")
dA_dt = multiply_dim(partial_t, A_def1)  # dA/dt的量纲
right = multiply_dim(f_dim1, dA_dt)  # f dA/dt的量纲
print(f"   左侧量纲：E = {format_dim(E)}")
print(f"   右侧量纲：f dA/dt = {format_dim(right)}")

if E == right:
    print("   ✅ 正确：方程量纲一致")
else:
    print("   ❌ 错误：方程量纲不一致")

# 验证方程3：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)
print("\n3. 验证方程：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)")
# 左侧：∂²A/∂t² = ∂/∂t · ∂/∂t · A
partial_t_sq = multiply_dim(partial_t, partial_t)  # ∂²/∂t²的量纲
left_eq3 = multiply_dim(partial_t_sq, A_def1)  # ∂²A/∂t²的量纲

# 右侧第一项：(V/f)(∇·E) = V · ∇ · E / f
nabla_dot_E = multiply_dim(nabla, E)  # ∇·E的量纲
v_nabla_E = multiply_dim(V, nabla_dot_E)  # V·∇·E的量纲
term1 = divide_dim(v_nabla_E, f_dim1)  # V·∇·E / f的量纲

# 右侧第二项：(c²/f)(∇×B) = c · c · ∇ · B / f
c_sq = multiply_dim(c, c)  # c²的量纲
nabla_cross_B = multiply_dim(nabla, B)  # ∇×B的量纲
c2_nabla_B = multiply_dim(c_sq, nabla_cross_B)  # c²·∇·B的量纲
term2 = divide_dim(c2_nabla_B, f_dim1)  # c²·∇·B / f的量纲

print(f"   左侧量纲：∂²A/∂t² = {format_dim(left_eq3)}")
print(f"   右侧第一项量纲：(V/f)(∇·E) = {format_dim(term1)}")
print(f"   右侧第二项量纲：(c²/f)(∇×B) = {format_dim(term2)}")

if left_eq3 == term1 and left_eq3 == term2:
    print("   ✅ 正确：方程量纲一致")
else:
    print("   ❌ 错误：方程量纲不一致")

# 定义2：A为引力场强度 ([A] = LT⁻²)
print("\n" + "=" * 60)
print("=== 定义2：A为引力场强度 ([A] = LT⁻²) ===")

A_def2 = {"L": 1, "M": 0, "T": -2, "I": 0}  # 引力场强度量纲

# 验证方程1：∇×A = B/f
print("\n1. 验证方程：∇×A = B/f")
left = multiply_dim(nabla, A_def2)  # ∇×A的量纲
print(f"   左侧量纲：∇×A = {format_dim(left)}")
print(f"   右侧量纲：B/f = {format_dim(B)} / [f]")
print(f"   等式成立条件：{format_dim(left)} = {format_dim(B)} / [f]")

# 解f的量纲
# [f] = B / (∇×A)
f_dim2 = divide_dim(B, left)
print(f"   解得[f] = {format_dim(B)} / {format_dim(left)} = {format_dim(f_dim2)}")
print(f"   对应的SI单位：kg/A (因为 {format_dim(f_dim2)} 对应 M·I⁻¹)")

if f_dim2 == {"L": 0, "M": 1, "T": 0, "I": -1}:
    print("   ✅ 正确：f的量纲为 [f] = MI⁻¹ (kg/A)")
else:
    print("   ❌ 错误：f的量纲推导有误")

# 验证方程2：E = -f dA/dt
print("\n2. 验证方程：E = -f dA/dt")
dA_dt = multiply_dim(partial_t, A_def2)  # dA/dt的量纲
right = multiply_dim(f_dim2, dA_dt)  # f dA/dt的量纲
print(f"   左侧量纲：E = {format_dim(E)}")
print(f"   右侧量纲：f dA/dt = {format_dim(right)}")

if E == right:
    print("   ✅ 正确：方程量纲一致")
else:
    print("   ❌ 错误：方程量纲不一致")

# 验证方程3：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)
print("\n3. 验证方程：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)")
# 左侧：∂²A/∂t² = ∂/∂t · ∂/∂t · A
left_eq3 = multiply_dim(partial_t_sq, A_def2)  # ∂²A/∂t²的量纲

# 右侧第一项：(V/f)(∇·E) = V · ∇ · E / f
term1 = divide_dim(v_nabla_E, f_dim2)  # V·∇·E / f的量纲

# 右侧第二项：(c²/f)(∇×B) = c · c · ∇ · B / f
term2 = divide_dim(c2_nabla_B, f_dim2)  # c²·∇·B / f的量纲

print(f"   左侧量纲：∂²A/∂t² = {format_dim(left_eq3)}")
print(f"   右侧第一项量纲：(V/f)(∇·E) = {format_dim(term1)}")
print(f"   右侧第二项量纲：(c²/f)(∇×B) = {format_dim(term2)}")

if left_eq3 == term1 and left_eq3 == term2:
    print("   ✅ 正确：方程量纲一致")
else:
    print("   ❌ 错误：方程量纲不一致")

# 总结
print("\n" + "=" * 60)
print("=== 总结 ===")
print(f"定义1（A为磁矢势）：f的量纲 = {format_dim(f_dim1)}，无量纲量")
print(f"定义2（A为引力场强度）：f的量纲 = {format_dim(f_dim2)}，单位 kg/A")
print("\n结论：")
print("1. 当A为磁矢势时，f为无量纲量，适配经典电磁学框架")
print("2. 当A为引力场强度时，f为跨场耦合系数，量纲为MI⁻¹，是连接引力场与电磁场的关键媒介")
