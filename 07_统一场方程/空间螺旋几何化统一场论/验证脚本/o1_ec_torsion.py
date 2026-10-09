# -*- coding: utf-8 -*-
"""引力扇区 EC 分支厘清：完全反对称挠率的 A3 代数验证
A3 挠率方程: T^α_μν - δ^α_μ T^ρ_ρν + δ^α_ν T^ρ_ρμ = κ S^α_μν
若自旋 S 完全反对称(S^α_μν=s·ε^α_μν)，验证：
  (1) T^α_μν=c·ε^α_μν（完全反对称）使迹 T^ρ_ρν=0
  (2) A3 退化为 T=κS（c=κs）
分支1(原始 EC, 挠率代数无动力学): 宏观=Einstein+四费米子, 物质单独守恒
分支2(V09, 挠率动力学 g_τ, 32号): 物质不守恒 ∇^μT^m_μν=(3g_τ/4)R∇_ντ
"""
import numpy as np
# 构造 4 维全反对称 Levi-Civita 张量 ε^α_μν（固定 α, μν 反对称）
eps_alpha_munu = np.zeros((4,4,4), dtype=int)
# ε^α_μν 对 μν 全反对称：ε^0_12=+1 等（取 ε^α_μν = 完全反对称符号）
for a in range(4):
    for m in range(4):
        for n in range(4):
            # 用 3 指标 Levi-Civita 在剩余 3 维 (去掉 a)
            idx=[i for i in range(4) if i!=a]
            # 位置映射
            def lc3(i,j,k):
                # 三指标完全反对称
                if len({i,j,k})<3: return 0
                import itertools
                sgn=1
                if (i,j,k) in [(idx[0],idx[1],idx[2]),(idx[2],idx[0],idx[1]),(idx[1],idx[2],idx[0])]: sgn=1
                elif (i,j,k) in [(idx[1],idx[0],idx[2]),(idx[2],idx[1],idx[0]),(idx[0],idx[2],idx[1])]: sgn=-1
                else: sgn=0
                return sgn
            if m in idx and n in idx:
                eps_alpha_munu[a,m,n]=lc3(m,n,idx[(idx.index(m)+1)%3] if False else 1) if False else lc3(m,n, idx[2] if False else None)
# 改用更干净的方法：ε^α_μν = ε_{αμν}（完全反对称，用 np 直接定义）
def levi(a,m,n):
    """4 维完全反对称 ε_{aμν}（固定第一个指标 a）"""
    # 用 3x3 全反对称在排除 a 的 3 维
    rem=[i for i in range(4) if i!=a]
    # ε_{rem[0] rem[1] rem[2]}=+1
    table={(rem[0],rem[1],rem[2]):1,(rem[2],rem[0],rem[1]):1,(rem[1],rem[2],rem[0]):1,
           (rem[1],rem[0],rem[2]):-1,(rem[0],rem[2],rem[1]):-1,(rem[2],rem[1],rem[0]):-1}
    if m not in rem or n not in rem or m==n: return 0
    return table.get((m,n),0)

kappa=2.0; s=1.5
# S^α_μν = s·ε^α_μν（完全反对称）
S=np.zeros((4,4,4))
for a in range(4):
    for m in range(4):
        for n in range(4):
            S[a,m,n]=s*levi(a,m,n)

# 解 A3: T^α_μν - δ^α_μ T^ρ_ρν + δ^α_ν T^ρ_ρμ = κ S^α_μν
# 设 T=c·ε（完全反对称），验证 T^ρ_ρν=0 且方程退化为 T=κS
# 先构造 T=c·ε 并算迹
def trace(T_):
    tr=np.zeros(4)  # T^ρ_ρν（一维：收缩 α=ρ, μ=ρ）
    for n in range(4):
        for p in range(4):
            tr[n]+=T_[p,p,n]  # T^ρ_ρν (收缩 α=ρ, μ=ρ)
    return tr

# 验证完全反对称 T 迹零
eps=np.zeros((4,4,4))
for a in range(4):
    for m in range(4):
        for n in range(4):
            eps[a,m,n]=levi(a,m,n)
c=kappa*s
T=c*eps
trT=trace(T)
print("== 完全反对称挠率 T=c·ε 的迹 T^ρ_ρν ==")
print(f"  max|trace|={np.max(np.abs(trT)):.1e} → {'迹零 ✓' if np.max(np.abs(trT))<1e-12 else '迹非零'}")

# 验证 A3 残差: T - δ^α_μ T^ρ_ρν + δ^α_ν T^ρ_ρμ vs κS
resid=np.zeros((4,4,4))
for a in range(4):
    for m in range(4):
        for n in range(4):
            # δ^α_μ T^ρ_ρν
            d1 = float(T[a,m,n].item()) - (1.0 if a==m else 0.0)*float(trT[n].item()) + (1.0 if a==n else 0.0)*float(trT[m].item())
            resid[a,m,n]=d1 - float(kappa*S[a,m,n].item())
print(f"  A3 残差 max|resid|={np.max(np.abs(resid)):.1e} → {'A3 精确满足 (T=κS) ✓' if np.max(np.abs(resid))<1e-12 else '不满足'}")
print(f"  T 相对 S: T/κS 比值 = {T[0,1,2]/(kappa*S[0,1,2]):.4f} (应=1)")

print("\n== EC 分支厘清 ==")
print(" 分支1(原始 EC, 挠率代数无动力学):")
print("   T=κS 代数求解(无传播自由度) → 代入 Einstein: R_μν-½Rg_μν=κ(T^m_μν+T^spin_μν)")
print("   T^spin = 四费米子项(自旋-自旋接触) → 宏观=标准 Einstein GR")
print("   挠率无动力学 → 物质能量动量单独守恒 ∇^μT^m_μν=0")
print(" 分支2(V09, 挠率动力学 g_τ, 32号):")
print("   挠率 τ 成为传播场(含 g_τ 动力学项) → 物质不单独守恒")
print("   ∇^μT^m_μν=(3g_τ/4)R∇_ντ (32 号闭合)")
print("   → TUFT 特有修正(依赖 g_τ 参数)")
print("\n== 引力扇区闭合状态(诚实) ==")
print(" 曲率线(能量动量→曲率): 分支1 闭合=标准 GR 复述(无 TUFT 新预言); 分支2 V09 闭合(有修正, g_τ 开放)")
print(" 来稿 A=引力场线: X-01/X-02/X-05/X-06 量纲 FAIL, 身份已撤(X-15)")
print(" ⇒ 引力扇区现状: 标准 GR 线闭合(无新意) + V09 挠率修正线闭合(参数开放) + 来稿引力场线 FAIL")
