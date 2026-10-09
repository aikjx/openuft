#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论常量量纲验证
算法联盟 - 量纲一致性检查
日期：2026-02-05
"""

class Dimension:
    """量纲类，用于表示和计算物理量的量纲"""
    def __init__(self, L=0, M=0, T=0, I=0, Q=0):
        self.L = L  # 长度
        self.M = M  # 质量
        self.T = T  # 时间
        self.I = I  # 电流
        self.Q = Q  # 电荷
    
    def __mul__(self, other):
        """量纲乘法"""
        return Dimension(
            self.L + other.L,
            self.M + other.M,
            self.T + other.T,
            self.I + other.I,
            self.Q + other.Q
        )
    
    def __truediv__(self, other):
        """量纲除法"""
        return Dimension(
            self.L - other.L,
            self.M - other.M,
            self.T - other.T,
            self.I - other.I,
            self.Q - other.Q
        )
    
    def __repr__(self):
        """量纲的字符串表示"""
        parts = []
        if self.L != 0:
            parts.append(f"L^{self.L}")
        if self.M != 0:
            parts.append(f"M^{self.M}")
        if self.T != 0:
            parts.append(f"T^{self.T}")
        if self.I != 0:
            parts.append(f"I^{self.I}")
        if self.Q != 0:
            parts.append(f"Q^{self.Q}")
        if not parts:
            return "无量纲"
        return " ".join(parts)
    
    def to_si(self):
        """转换为SI制（用I表示，Q=I*T）"""
        # Q = I*T，所以 Q的量纲可以转换为I和T
        return Dimension(
            self.L,
            self.M,
            self.T + self.Q,  # Q的T部分
            self.I + self.Q,  # Q的I部分
            0  # 转换后Q=0
        )
    
    def __eq__(self, other):
        """比较两个量纲对象是否相等"""
        if not isinstance(other, Dimension):
            return False
        return (
            self.L == other.L and
            self.M == other.M and
            self.T == other.T and
            self.I == other.I and
            self.Q == other.Q
        )

# 基本量纲
L = Dimension(L=1)
M = Dimension(M=1)
T = Dimension(T=1)
I = Dimension(I=1)
Q = Dimension(Q=1)

# 导出量纲
C = Q  # 库仑
A = I  # 安培
V = M*L*L/(T*T*Q)  # 伏特 = J/C = kg·m²/(s²·C)
F = Q/V  # 法拉 = C/V
H = V*T/I  # 亨利 = V·s/A
N = M*L/(T*T)  # 牛顿
J = N*L  # 焦耳
W = J/T  # 瓦特

# 基本常数的量纲
c = L/T  # 光速
G = L*L*L/(M*T*T)  # 万有引力常数

epsilon_0 = Q/V/L  # 真空介电常数 = C/(V·m)
mu_0 = V*T/(I*L)  # 真空磁导率 = H/m

# 验证epsilon_0的量纲
print("epsilon_0量纲:", epsilon_0)
print("epsilon_0 (SI):", epsilon_0.to_si())

# 验证mu_0的量纲
print("mu_0量纲:", mu_0)
print("mu_0 (SI):", mu_0.to_si())

# 计算Z和Z'的量纲
# 创建无量纲对象表示纯数值系数
numeric = Dimension()
Z = G * c / numeric  # Z = Gc/2 (系数不影响量纲)
Z_prime = c / (numeric * epsilon_0)  # Z' = c/(8πε₀) (系数不影响量纲)

print("\nZ量纲:", Z)
print("Z (SI):", Z.to_si())

print("\nZ'量纲:", Z_prime)
print("Z' (SI):", Z_prime.to_si())

# 其他常量的量纲
k = M  # 空间-质量耦合常数
k_prime = Q*T/M  # 空间-电荷耦合常数 = C·s/kg
f = M/I  # 场转化耦合常数 = kg/A

Lambda = numeric/(L*L)  # 宇宙学常数 = 1/m²
omega = numeric/T  # 角频率 = 1/s
h_pitch = L  # 螺距 = m/rad (rad是无量纲的)
dot_r = L/T  # 径向速度 = m/s
gamma = Dimension()  # 洛伦兹因子（无量纲）
H0 = numeric/T  # 哈勃常数 = 1/s
m0 = M  # 基本质量量子
n = Dimension()  # 空间几何参数（无量纲）
Omega = Dimension()  # 立体角（无量纲）

# 打印所有常量的量纲
print("\n" + "="*80)
print("张祥前统一场论常量量纲验证")
print("="*80)

constants = {
    "c": ("光速", c),
    "G": ("万有引力常数", G),
    "epsilon_0": ("真空介电常数", epsilon_0),
    "mu_0": ("真空磁导率", mu_0),
    "hbar": ("约化普朗克常数", M*L*L/T),
    "k": ("空间-质量耦合常数", k),
    "k'": ("空间-电荷耦合常数", k_prime),
    "f": ("场转化耦合常数", f),
    "Z": ("引力光速统一常数", Z),
    "Z'": ("电磁光速几何耦合常数", Z_prime),
    "Lambda": ("宇宙学常数", Lambda),
    "omega": ("角频率", omega),
    "h": ("螺距", h_pitch),
    "dot_r": ("径向速度", dot_r),
    "gamma": ("洛伦兹因子", gamma),
    "H0": ("哈勃常数", H0),
    "m0": ("基本质量量子", m0),
    "n": ("空间几何参数", n),
    "Omega": ("立体角", Omega)
}

print("\n常量量纲表（原始表示）:")
print("-"*80)
print(f"{'常量':<15} {'物理意义':<25} {'量纲':<30}")
print("-"*80)
for const, (desc, dim) in constants.items():
    print(f"{const:<15} {desc:<25} {dim!r:<30}")

print("\n常量量纲表（SI制，Q转换为I·T）:")
print("-"*80)
print(f"{'常量':<15} {'物理意义':<25} {'SI量纲':<30}")
print("-"*80)
for const, (desc, dim) in constants.items():
    si_dim = dim.to_si()
    print(f"{const:<15} {desc:<25} {si_dim!r:<30}")

print("\n" + "="*80)
print("量纲验证结果")
print("="*80)

# 验证Z'的量纲计算
print("\nZ' = c/(8πε₀) 的量纲计算:")
print(f"c 的量纲: {c!r}")
print(f"epsilon_0 的量纲: {epsilon_0!r}")
print(f"1/epsilon_0 的量纲: {Dimension()/epsilon_0!r}")
print(f"Z' 的量纲: {Z_prime!r}")
print(f"Z' (SI): {Z_prime.to_si()!r}")

# 验证文档中的量纲
print("\n文档中Z'的量纲验证:")
doc_Z_prime = M*L*L*L*L/(T*T*T*Q*Q)  # [M L⁴ T⁻³ Q⁻²]
print(f"文档中Z'量纲: {doc_Z_prime!r}")
print(f"转换为SI制: {doc_Z_prime.to_si()!r}")
print(f"与计算结果是否一致: {doc_Z_prime.to_si() == Z_prime.to_si()}")

print("\n" + "="*80)
print("结论")
print("="*80)
print("Z'的正确SI量纲为:", Z_prime.to_si())
print("之前的错误量纲:", "L⁴ M T⁻³ I⁻²")
print("正确量纲:", Z_prime.to_si())
print("\n量纲不一致的原因: 之前计算时错误地处理了时间维度")
