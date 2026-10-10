# -*- coding: utf-8 -*-
"""attack20_唯一化原理候选测试.py (v2 修正)
修正：完整规范群 = SU(m+1)×SU(n+1)×U(1)，秩 = m+n+1（含 U(1)）。
时空维=4 → m+n=3 → 候选 {(1,2),(3,0)}。测试后续判据能否唯一选出 (1,2)。
纯标准库。
"""
# 候选 (m,n), 0..4, 完整群 SU(m+1)×SU(n+1)×U(1)
pools = [(m,n) for m in range(0,5) for n in range(0,5) if m>=n]

def rank_full(g):
    m,n = g
    return m+n+1  # 含 U(1)

def factors(g):
    m,n = g
    return {m,n}  # 简单因子秩集合 {rank(SU(m+1))=m, rank(SU(n+1))=n}

print("="*70)
print("attack20 v2_唯一化原理候选测试 · 独立复算（修正 U(1)）")
print("="*70)

# ---- C1: 完整群秩 = 时空维 4 ----
st = 4
c1 = [g for g in pools if rank_full(g)==st]
print(f"\n[C1] 完整群秩=时空维(4): m+n+1=4 -> m+n=3")
for g in c1:
    m,n = g
    print(f"     CP^{m}×CP^{n} -> SU({m+1})×SU({n+1})×U(1), 秩={rank_full(g)}")
print(f"     候选: {c1}")

# ---- C2: 需含秩1(SU2弱)和秩2(SU3色)两个不同秩简单因子 ----
c2 = [g for g in c1 if {1,2} <= factors(g)]
print(f"[C2] 需含秩1(SU2)+秩2(SU3)简单因子: {c2}")
print("     注: (1,2) 有 SU(2)(秩1)+SU(3)(秩2); (3,0) 只有 SU(4)(秩3), 排除")

# ---- C3: 弱结构含双态⊕单态(0-1对偶二分, 稳定子 U(2)→2⊕1, 需 n=2 或 m=2) ----
c3 = [g for g in c1 if 2 in factors(g)]
print(f"[C3] 弱双态⊕单态(某 CP^2 稳定子 U(2)→2⊕1, 需秩2因子): {c3}")
print("     -> (3,0) 无秩2因子(SU(4) 秩3), 排除; 保留 (1,2)")

# ---- C4: 拓扑荷载体 ----
print(f"[C4] 拓扑荷: CP^1 有霍普夫荷(pi_3=Z); CP^2 无(pi_3(CP^2)=0)")
c4_has_hopf = [g for g in c1 if 1 in factors(g)]
print(f"     需至少一因子承载霍普夫荷(含 CP^1): {c4_has_hopf}")
print(f"     -> (3,0) 无 CP^1(SU(4), 秩3) 无霍普夫荷, 排除; 保留 (1,2)")

print("\n"+"="*70)
print("唯一化判据逐层结果(v2 修正 U(1)):")
print(f"  候选池(0..4): {len(pools)} 个")
print(f"  [C1]完整群秩=时空维4: {c1}")
print(f"  [C2]含秩1+秩2: {c2}  (注:若作纯几何判据需'需两不同秩因子'独立论证)")
print(f"  [C3]弱双态⊕单态: {c3}")
print(f"  [C4]含霍普夫荷载体: {c4_has_hopf}")
print()
print("结论(v2):")
print("  C1(秩=时空维) 把候选缩到 {(1,2),(3,0)}；")
print("  C3(弱双态⊕单态,0-1对偶) 排除 (3,0)；C4(拓扑荷) 同样排除 (3,0)；")
print("  -> 若无循环输入'需弱+色', 则需独立判据同时要求: 秩=时空维 + 弱双态对偶,")
print("     可唯一选出 (1,2)。用户'全维度秩-时空对偶' + '0-1阴阳对偶二分'")
print("     构成部分唯一化判据(排除到 (1,2))，但仍需把'为何需弱双态⊕单态'公理化。")
