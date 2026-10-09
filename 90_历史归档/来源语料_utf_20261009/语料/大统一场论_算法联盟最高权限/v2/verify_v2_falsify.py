# -*- coding: utf-8 -*-
"""
verify_v2_falsify.py
卷十二《质量量子化的诚实证伪检验》
对卷九/卷十预言 "m = N·m₀, N∈ℤ⁺（m₀ 普适 = m_e）" 做严格检验。
0 模糊：结果如实报告，含可能的证伪。
"""
from mpmath import mp, mpf
mp.dps = 60

SEP = "=" * 66
SUB = "-" * 66

# ---------- CODATA 2022 粒子质量 ----------
m_e = mpf('9.1093837015e-31')
m_mu = mpf('1.883531627e-28')
m_tau = mpf('3.16754e-27')
m_p = mpf('1.67262192369e-27')
m_n = mpf('1.67492749804e-27')

def report(name, result, detail=""):
    mark = "✓" if result else "✗ 证伪"
    print(f"  [{mark}] {name} {detail}")
    return result

print(SEP)
print("  卷十二 · 质量量子化的诚实证伪检验")
print("  预言：m = N·m₀, N∈ℤ⁺，m₀ 普适 = m_e（卷九/卷十）")
print("  检验：对所有已知粒子，N = m/m₀ 是否整数？")
print(SEP)

# 若 m₀ 普适 = m_e，则各粒子条数 N_i = m_i/m_e
particles = [("电子 e", m_e), ("μ子", m_mu), ("τ子", m_tau),
             ("质子 p", m_p), ("中子 n", m_n)]

print("\n[检验 1] N = m/m₀（m₀=m_e 普适）是否整数？")
print(SUB)
for name, m in particles:
    N = m / m_e
    near_int = mpf(round(float(N)))           # 最近整数
    dist = abs(N - near_int)                   # 到最近整数的距离
    is_int = dist < mpf('1e-6')                # 整数判定阈值（1e-6 相对/绝对）
    print(f"  {name:<8} N = {mp.nstr(N, 8)}  距最近整数 {mp.nstr(dist, 3)}")
    report(f"{name} 条数 N 为整数", is_int, "")

# 统计
integer_count = sum(1 for name, m in particles if
                    abs((m/m_e) - mpf(round(float(m/m_e)))) < mpf('1e-6'))

print(SUB)
print(f"\n  整数条数粒子数: {integer_count} / {len(particles)}（唯一整数为电子 N=1，属定义）")

# ============ 诚实结论判定 ============
print("\n[结论判定]")
print(SUB)
prediction_falsified = integer_count <= 1
report("普适 m₀=m_e 的整数条数量子化预言", not prediction_falsified,
       "（若证伪则：预言不成立）")

# 关键诚实结论（不计入通过率，仅陈述）
print("\n[诚实科学定位]")
print("  ✗ 若 m₀ 普适 = m_e，则 μ(N=206.77)、τ(N=3477.15)、p(N=1836.15)、")
print("    n(N=1838.68) 均为非整数 → 整数条数量子化预言被证伪。")
print("  ⇒ '质量是所有粒子共享同一普适量 m₀ 的整数倍' 不成立。")
print("  ⇒ N 只能作为逐粒子的'等效计数'（每粒子自身 m₀=N=1），无独立预言力。")
print("  ⇒ 与标准模型一致：质量谱并非普适量子的整数倍（QCD 中亦然）。")
print()
print("  ✓ 科学价值：本检验诚实地排除了'普适质量量子化'这一可证伪假说，")
print("    使框架定位更准确（质量谱未导出，与 QCD 诚实地位一致）。")
print(SEP)
