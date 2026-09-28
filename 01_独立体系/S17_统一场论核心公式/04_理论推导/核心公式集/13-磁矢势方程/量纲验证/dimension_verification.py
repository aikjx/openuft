# 量纲验证文件中的Python实现
# 验证统一场论中f的量纲推导

from dataclasses import dataclass

@dataclass
class Dimension:
    """
    量纲类，用于表示物理量的量纲，支持基本的乘除运算
    对应量纲：M(质量), L(长度), T(时间), Q(电荷)
    """
    M: int = 0  # 质量 [M] 指数
    L: int = 0  # 长度 [L] 指数
    T: int = 0  # 时间 [T] 指数
    Q: int = 0  # 电荷 [Q] 指数
    
    def __mul__(self, other: "Dimension") -> "Dimension":
        """量纲乘法：对应指数相加"""
        if not isinstance(other, Dimension):
            raise TypeError("仅支持两个Dimension对象相乘")
        return Dimension(
            M=self.M + other.M,
            L=self.L + other.L,
            T=self.T + other.T,
            Q=self.Q + other.Q
        )
    
    def __truediv__(self, other: "Dimension") -> "Dimension":
        """量纲除法：对应指数相减"""
        if not isinstance(other, Dimension):
            raise TypeError("仅支持两个Dimension对象相除")
        return Dimension(
            M=self.M - other.M,
            L=self.L - other.L,
            T=self.T - other.T,
            Q=self.Q - other.Q
        )
    
    def __repr__(self) -> str:
        """格式化输出量纲结果"""
        dim_parts = []
        if self.M != 0:
            dim_parts.append(f"M^{self.M}")
        if self.L != 0:
            dim_parts.append(f"L^{self.L}")
        if self.T != 0:
            dim_parts.append(f"T^{self.T}")
        if self.Q != 0:
            dim_parts.append(f"Q^{self.Q}")
        return "[" + " ".join(dim_parts) + "]" if dim_parts else "[无量纲]"

# 步骤1：定义题目中给定的已知量纲
# 电场强度 E
E_dim = Dimension(M=1, L=1, T=-3, Q=-1)
# 磁矢势 A
A_dim = Dimension(M=1, L=1, T=-1, Q=-1)
# 时间 t（导数运算需要）
T_dim = Dimension(T=1)
# 磁感应强度 B（用于交叉验证）
B_dim = Dimension(M=1, T=-1, Q=-1)
# 梯度/旋度中的空间导数 L^-1（用于交叉验证）
nabla_dim = Dimension(L=-1)

# 步骤2：计算 dA/dt 的量纲（对A求时间一阶导）
dA_dt_dim = A_dim / T_dim
print(f"dA/dt 的量纲：{dA_dt_dim}")

# 步骤3：根据方程14推导 f 的量纲（E = -f * dA/dt → f = E / (dA/dt)）
f_dim = E_dim / dA_dt_dim
print(f"通过方程14推导得到 f 的量纲：{f_dim}")

# 步骤4：交叉验证（方程13：∇×A = B/f → f = B / (∇×A)）
nabla_cross_A_dim = nabla_dim * A_dim  # 旋度的量纲（∇×A 等价于 ∇·A 的量纲运算）
f_dim_cross_verify = B_dim / nabla_cross_A_dim
print(f"通过方程13交叉验证得到 f 的量纲：{f_dim_cross_verify}")

# 步骤5：量纲结果总结
print("\n=== 量纲推导总结 ===")
print(f"最终 f 的量纲：{f_dim}")
print(f"量纲说明：T^-1 对应【时间倒数】（频率量纲，等价于 Hz）")

# 额外：验证主论文中的量纲定义
print("\n=== 主论文量纲验证 ===")
# 主论文中的量纲定义
E_dim_paper = Dimension(M=1, L=1, T=-3, Q=-1)  # [MLT^-3 Q^-1] 或 [MLT^-3 I^-1]
B_dim_paper = Dimension(M=1, T=-2, Q=-1)  # [MT^-2 Q^-1] 或 [MT^-2 I^-1]
A_dim_paper = Dimension(L=1, T=-2)  # 引力场，[LT^-2]

# 验证方程 ∇×A = B/f 中 f 的量纲
nabla_cross_A_dim_paper = nabla_dim * A_dim_paper
f_dim_paper = B_dim_paper / nabla_cross_A_dim_paper
print(f"主论文中通过方程 ∇×A = B/f 推导得到 f 的量纲：{f_dim_paper}")