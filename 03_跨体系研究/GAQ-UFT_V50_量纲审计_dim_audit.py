# -*- coding: utf-8 -*-
"""
第一轮·家族七·量纲闭合审计（A1-A4 + Gε0 恒等式）
量纲空间: (L, T, M, Q) 四维幂次向量
规则: 两式相加(同量纲)合法; 乘积=幂次相加; 方程两侧幂次向量必须相等。
"""
def add(a, b): return [a[i]+b[i] for i in range(4)]
def sub(a, b): return [a[i]-b[i] for i in range(4)]
def mul(a, k): return [x*k for x in a]
def dim_str(v):
    parts = []
    names = ["L", "T", "M", "Q"]
    for i, x in enumerate(v):
        if x != 0:
            parts.append(f"{names[i]}^{x}")
    return "*".join(parts) if parts else "无量纲"

# 基本物理量量纲
kappa = [-1, 0, 0, 0]   # 曲率: 1/L
tau   = [-1, 0, 0, 0]   # 挠率: 1/L
omega = [0, -1, 0, 0]   # 角频率: 1/T
lP    = [1, 0, 0, 0]    # 普朗克长度: L
c     = [1, -1, 0, 0]   # 光速: L/T
G     = [3, -2, -1, 0]  # 引力常数: M^-1 L^3 T^-2
eps0  = [-3, 4, -1, 2]  # 真空介电常数: M^-1 L^-3 T^4 Q^2
hbar  = [2, -1, 1, 0]   # 约化普朗克常数: M L^2 T^-1

# 同量纲两项相加: 量纲不变 (κ² 与 τ² 同量纲)
kappa2 = mul(kappa, 2)   # κ² 量纲
tau2   = mul(tau, 2)     # τ² 量纲
assert kappa2 == tau2, "κ² 与 τ² 必须同量纲才能相加"
lhs = kappa2              # κ²+τ² 量纲 = κ² 量纲 (同量纲加法不变)

print("="*78)
print("量纲审计 1: 公理 A2  κ²+τ² = (ω·ℓP/c)²")
print(f"  κ² 量纲        = {dim_str(kappa2)}  (曲率²)")
print(f"  τ² 量纲        = {dim_str(tau2)}  (挠率²)")
print(f"  κ²+τ²         量纲 = {dim_str(lhs)}  (同量纲相加不变)")
inner = sub(add(omega, lP), c)                  # ω·ℓP/c
rhs = mul(inner, 2)
print(f"  ω·ℓP/c        量纲 = {dim_str(inner)}")
print(f"  (ω·ℓP/c)²     量纲 = {dim_str(rhs)}")
print(f"  判定: {'闭合 ✓' if lhs == rhs else '不闭合 ✗ (左=L^-2 右=无量纲)'}")

print()
print("量纲审计 1b: 修正版 A2'  κ²+τ² = (ω/c)²  （去掉 ℓP）")
inner2 = sub(omega, c)                          # ω/c = 波数, 量纲 1/L
rhs2 = mul(inner2, 2)
print(f"  (ω/c)²        量纲 = {dim_str(rhs2)}")
print(f"  判定: {'闭合 ✓' if lhs == rhs2 else '不闭合 ✗'}")
print("  注: 修正版中 ℓP 消失 → A2 退化为纯运动学恒等式（Darboux 频率=光波数），无量子/普朗克内容")

print()
print("量纲审计 1c: 无量纲化版 A2'' (κℓP)²+(τℓP)² = (ωℓP/c)²")
k_lP = add(kappa, lP)   # κℓP: 幂次相加 = 无量纲
t_lP = add(tau, lP)
lhs3 = mul(k_lP, 2)     # (κℓP)² 量纲; (τℓP)² 同量纲, 相加不变
assert mul(t_lP,2) == lhs3
rhs3 = mul(inner, 2)
print(f"  (κℓP)²+(τℓP)² 量纲 = {dim_str(lhs3)}")
print(f"  判定: {'闭合 ✓' if lhs3 == rhs3 else '不闭合 ✗'}")
print("  注: 此版所有项无量纲，数学自洽；但 ℓP 只是公共标度因子（代数上恒等约去），"
      "并不赋予 A2 量子内容——'普朗克长度决定频率'的说法是过度诠释")

print()
print("="*78)
print("量纲审计 2: 'G·ε0 恒等式'")
ge = add(G, eps0)
print(f"  G       量纲 = {dim_str(G)}")
print(f"  ε0      量纲 = {dim_str(eps0)}")
print(f"  G·ε0    量纲 = {dim_str(ge)}")
print(f"  判定: 无量纲? {'是' if ge == [0,0,0,0] else '否 ✗ (G·ε0 不是无量纲纯数)'}")

print()
print("量纲审计 2b: 正确的电磁-引力耦合比较（应有参照质量）")
ge_hc = sub(add(G, eps0), add(hbar, c))          # Gε0/(ħc)
print(f"  G·ε0/(ħc)   量纲 = {dim_str(ge_hc)}")
print(f"  判定: 无量纲? {'是' if ge_hc == [0,0,0,0] else '否 ✗'}")
print("  正确形式: α = e²/(4π·ε0·ħc) 无量纲 ✓;  Gm_P²/(ħc) = 1 是 m_P 的*定义*，非预言")

print()
print("="*78)
print("量纲审计 3: 32 维 Dirac 旋量维数（A3 '房间' 论断检查）")
for d in [4, 10, 11, 32]:
    n = 2 ** (d // 2)
    print(f"  时空维数 d={d}: Dirac 旋量分量数 2^(⌊d/2⌋) = {n}")
print("  判定: d=32 旋量空间 = 65536 复分量，'正好装下'的说法不成立——")
print("  高维旋量产生的是海量额外态（超出 SM 48 费米子 3 个数量级），"
      "且没有任何已知机制消除；32 维无超对称/反常/最大维数动机")

print()
print("量纲审计 4: 公理 A1 'v ≡ c' 表述检查")
print("  字面版 (v≡c 恒成立): 被已知物理证伪 —— 物质速度 v<c 的过程普遍存在")
print("  上限版 (v≤c): 洛伦兹不变性/无质量色散关系的推论，非独立公理，亦不'解释'光速数值")
print("  判定: 需澄清表述；字面版不可作为公理")

print()
print("="*78)
print("汇总: A2(带ℓP版) ✗不闭合 | G·ε0 ✗非无量纲 | 32维旋量论断 ✗不成立 | A1 表述需澄清")
