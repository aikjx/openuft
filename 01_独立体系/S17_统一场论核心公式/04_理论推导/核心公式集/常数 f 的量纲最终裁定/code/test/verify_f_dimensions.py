#!/usr/bin/env python3
"""
验证耦合系数f在两种矢量A定义下的量纲推导
1. 定义1：A为磁矢势 ([A] = MLT⁻²I⁻¹)
2. 定义2：A为引力场强度 ([A] = LT⁻²)
"""

class Dimension:
    """物理量纲类，用于表示和计算物理量的量纲"""
    def __init__(self, L=0, M=0, T=0, I=0):
        self.L = L  # 长度
        self.M = M  # 质量
        self.T = T  # 时间
        self.I = I  # 电流
    
    def __str__(self):
        """将量纲转换为字符串表示"""
        parts = []
        if self.L != 0:
            parts.append(f"L^{self.L}")
        if self.M != 0:
            parts.append(f"M^{self.M}")
        if self.T != 0:
            parts.append(f"T^{self.T}")
        if self.I != 0:
            parts.append(f"I^{self.I}")
        return "·".join(parts) if parts else "1"  # 无量纲用1表示
    
    def __mul__(self, other):
        """量纲乘法"""
        return Dimension(
            self.L + other.L,
            self.M + other.M,
            self.T + other.T,
            self.I + other.I
        )
    
    def __truediv__(self, other):
        """量纲除法"""
        return Dimension(
            self.L - other.L,
            self.M - other.M,
            self.T - other.T,
            self.I - other.I
        )
    
    def __eq__(self, other):
        """量纲相等性比较"""
        return (
            self.L == other.L and
            self.M == other.M and
            self.T == other.T and
            self.I == other.I
        )

# 基本物理量量纲定义
L = Dimension(L=1)  # 长度
M = Dimension(M=1)  # 质量
T = Dimension(T=1)  # 时间
I = Dimension(I=1)  # 电流

# 固定物理量量纲（经典电磁学定义）
E = Dimension(L=1, M=1, T=-3, I=-1)  # 电场强度 [E] = MLT⁻³I⁻¹
B = Dimension(M=1, T=-2, I=-1)        # 磁感应强度 [B] = MT⁻²I⁻¹
V = L / T                              # 速度 [V] = LT⁻¹
c = V                                  # 光速 [c] = LT⁻¹
nabla = Dimension() / L                # 空间算子 [∇] = L⁻¹
partial_t = Dimension() / T            # 时间微分算子 [∂/∂t] = T⁻¹

# 定义1：A为磁矢势 ([A] = MLT⁻²I⁻¹)
def verify_definition_1():
    print("=== 定义1：A为磁矢势 ([A] = MLT⁻²I⁻¹) ===")
    
    A = Dimension(L=1, M=1, T=-2, I=-1)  # 磁矢势量纲
    
    # 验证方程1：∇×A = B/f
    print("\n1. 验证方程：∇×A = B/f")
    left = nabla * A  # ∇×A的量纲
    print(f"   左侧量纲：∇×A = ∇·A = {left}")
    print(f"   右侧量纲：B/f = {B} / [f]")
    print(f"   等式成立条件：{left} = {B} / [f]")
    
    # 解f的量纲
    # [f] = B / (∇×A)
    f_dim = B / left
    print(f"   解得[f] = {B} / {left} = {f_dim}")
    
    if f_dim == Dimension():  # 无量纲量
        print("   ✅ 正确：f为无量纲量 [f] = 1")
    else:
        print("   ❌ 错误：f的量纲推导有误")
    
    # 验证方程2：E = -f dA/dt
    print("\n2. 验证方程：E = -f dA/dt")
    dA_dt = partial_t * A  # dA/dt的量纲
    right = f_dim * dA_dt  # f dA/dt的量纲
    print(f"   左侧量纲：E = {E}")
    print(f"   右侧量纲：f dA/dt = [f]·∂A/∂t = {right}")
    
    if E == right:
        print("   ✅ 正确：方程量纲一致")
    else:
        print("   ❌ 错误：方程量纲不一致")
    
    # 验证方程3：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)
    print("\n3. 验证方程：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)")
    left = partial_t * partial_t * A  # ∂²A/∂t²的量纲
    term1 = (V / f_dim) * (nabla * E)  # 第一项量纲
    term2 = (c * c / f_dim) * (nabla * B)  # 第二项量纲
    print(f"   左侧量纲：∂²A/∂t² = {left}")
    print(f"   右侧第一项量纲：(V/f)(∇·E) = {term1}")
    print(f"   右侧第二项量纲：(c²/f)(∇×B) = {term2}")
    
    if left == term1 and left == term2:
        print("   ✅ 正确：方程量纲一致")
    else:
        print("   ❌ 错误：方程量纲不一致")
    
    return f_dim

# 定义2：A为引力场强度 ([A] = LT⁻²)
def verify_definition_2():
    print("\n=== 定义2：A为引力场强度 ([A] = LT⁻²) ===")
    
    A = Dimension(L=1, T=-2)  # 引力场强度量纲
    
    # 验证方程1：∇×A = B/f
    print("\n1. 验证方程：∇×A = B/f")
    left = nabla * A  # ∇×A的量纲
    print(f"   左侧量纲：∇×A = ∇·A = {left}")
    print(f"   右侧量纲：B/f = {B} / [f]")
    print(f"   等式成立条件：{left} = {B} / [f]")
    
    # 解f的量纲
    # [f] = B / (∇×A)
    f_dim = B / left
    print(f"   解得[f] = {B} / {left} = {f_dim}")
    print(f"   对应的SI单位：kg/A (因为 {f_dim} 对应 M·I⁻¹)")
    
    if f_dim == Dimension(M=1, I=-1):
        print("   ✅ 正确：f的量纲为 [f] = MI⁻¹ (kg/A)")
    else:
        print("   ❌ 错误：f的量纲推导有误")
    
    # 验证方程2：E = -f dA/dt
    print("\n2. 验证方程：E = -f dA/dt")
    dA_dt = partial_t * A  # dA/dt的量纲
    right = f_dim * dA_dt  # f dA/dt的量纲
    print(f"   左侧量纲：E = {E}")
    print(f"   右侧量纲：f dA/dt = [f]·∂A/∂t = {right}")
    
    if E == right:
        print("   ✅ 正确：方程量纲一致")
    else:
        print("   ❌ 错误：方程量纲不一致")
    
    # 验证方程3：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)
    print("\n3. 验证方程：∂²A/∂t² = (V/f)(∇·E) - (c²/f)(∇×B)")
    left = partial_t * partial_t * A  # ∂²A/∂t²的量纲
    term1 = (V / f_dim) * (nabla * E)  # 第一项量纲
    term2 = (c * c / f_dim) * (nabla * B)  # 第二项量纲
    print(f"   左侧量纲：∂²A/∂t² = {left}")
    print(f"   右侧第一项量纲：(V/f)(∇·E) = {term1}")
    print(f"   右侧第二项量纲：(c²/f)(∇×B) = {term2}")
    
    if left == term1 and left == term2:
        print("   ✅ 正确：方程量纲一致")
    else:
        print("   ❌ 错误：方程量纲不一致")
    
    return f_dim

# 主函数
def main():
    print("耦合系数f的量纲验证")
    print("=" * 60)
    
    # 验证两种定义
    f_dim_1 = verify_definition_1()
    f_dim_2 = verify_definition_2()
    
    # 总结
    print("\n" + "=" * 60)
    print("=== 总结 ===")
    print(f"定义1（A为磁矢势）：f的量纲 = {f_dim_1}，无量纲量")
    print(f"定义2（A为引力场强度）：f的量纲 = {f_dim_2}，单位 kg/A")
    print("\n结论：")
    print("1. 当A为磁矢势时，f为无量纲量，适配经典电磁学框架")
    print("2. 当A为引力场强度时，f为跨场耦合系数，量纲为MI⁻¹，是连接引力场与电磁场的关键媒介")

if __name__ == "__main__":
    main()
