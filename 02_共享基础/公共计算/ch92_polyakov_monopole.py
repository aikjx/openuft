# -*- coding: utf-8 -*-
"""
第92章 配套复算脚本 ch92_polyakov_monopole.py（纯标准库，exit 0）
磁单极凝聚机制的可复核数值骨架：
 1) Dirac–Schwinger 磁荷量子化 eg = 2πn（严格）
 2) 't Hooft–Polyakov BPS 单极质量 M = 4π m_W / e²（SU(2) Georgi-Glashow）
 3) 3D 紧致 U(1) 单极（瞬子）作用量 S0 = 2π²β（Villain 参数 β），密度 z ∝ e^{-S0}
 4) Debye 光子质量（Polyakov）：M² = 8π²z/e²（cond-mat/0501022）；SU(2) 板块形式 m²=16π²β e^{-2π²β}G0(M)（arXiv:1106.0293）
全部公式来自已引文献，本书只做数值复算与指数行为演示，不声称新推导。
"""
import math

print("="*78)
print("1) Dirac–Schwinger 量子化：eg = 2πn  (n ∈ Z)")
print("="*78)
for n in range(1,5):
    # 取 e = 1 单位制下磁荷 g_n = 2πn / e；此处列 g·e 积
    print(f"  n={n}:  eg = 2π×{n} = {2*math.pi*n:.6f}  (无量纲积，单位制无关)")
print("  注：Gaussian 单位下点磁单极磁荷 Q_m = 4π/e（arXiv:hep-th/9908095 提及）")

print()
print("="*78)
print("2) 't Hooft–Polyakov BPS 单极质量（4D, SU(2)→U(1)）")
print("   M = 4π m_W / e²   （Bogomolny 1976 / Prasad–Sommerfield，SU(2) 精确）")
print("="*78)
mW = 80.379  # GeV, PDG
alpha = 1/137.035999084
s2w  = 0.23122
alpha2 = alpha/s2w          # α₂(MZ) = α/sin²θW
g2_1 = math.sqrt(4*math.pi*alpha2)          # 由 α₂ 导出
g2_2 = 0.653                # 常用 g₂(MZ) 数值（PDG 口径）
for tag, g2 in (("g2=sqrt(4πα₂)", g2_1), ("g2=0.653(PDG常用)", g2_2)):
    M = 4*math.pi*mW/(g2*g2)
    print(f"  {tag}: e²={g2*g2:.6f} → M_BPS = 4π×{mW}/({g2:.4f})² = {M:.1f} GeV ≈ {M/1000:.3f} TeV")
print(f"  α₂(MZ)={alpha2:.6f}（由 α={alpha:.6f}, sin²θW={s2w} 导出）")

print()
print("="*78)
print("3) 3D 紧致 U(1)：单极（瞬子）作用量与气体密度")
print("   S0 = 2π²β（Villain 参数 β），密度 z ∝ e^{-S0}（Polyakov 1977；arXiv:2112.02483）")
print("="*78)
print(f"  {'β':>4} {'S0=2π²β':>10} {'z=e^-S0':>16} {'log10 z':>10}")
for beta in (1,2,3,4,5,6):
    S0 = 2*math.pi*math.pi*beta
    z  = math.exp(-S0)
    print(f"  {beta:>4} {S0:>10.4f} {z:>16.3e} {math.log10(z):>10.3f}")

print()
print("="*78)
print("4) Debye 光子质量（Polyakov 德拜屏蔽）")
print("   连续/格点形式 M² = 8π²z/e²（cond-mat/0501022）；")
print("   SU(2) 板块形式 m² = 16π²β e^{-2π²β} G0(M)，G0(M)~O(1)（arXiv:1106.0293）")
print("="*78)
print("   a) M² = 8π²z/e² 的指数行为（z=e^{-S0}，比例关系演示，绝对标度依赖正则化）:")
for beta in (1,2,3,4):
    S0 = 2*math.pi*math.pi*beta
    z  = math.exp(-S0)
    M2 = 8*math.pi*math.pi*z   # e² 归一到 1 的比例关系
    print(f"      β={beta}: S0={S0:.3f}, z={z:.3e}, M²(∝8π²z)={M2:.3e}")
print("   b) SU(2) 板块 Debye 质量 m² = 16π²β e^{-2π²β} G0，G0=0.25（示意，O(1)）:")
G0 = 0.25
for beta in (1,2,3,4):
    m2 = 16*math.pi*math.pi*beta*math.exp(-2*math.pi*math.pi*beta)*G0
    print(f"      β={beta}: m²={m2:.3e}  (m={math.sqrt(m2):.3e})")
print("   → 结论：m_D 指数式抑制（e^{-2π²β}），但恒>0；这就是'真空被单极气体无序化'")
print("     带来的德拜屏蔽：光子获得质量 → 面积律 → 禁闭（Göpfert–Mack 1981 严格化）")

print()
print("="*78)
print("5) 弦张力数量级（3D 紧致 U(1)，面积律指数）")
print("   σ ∝ z（单极密度）；以下给出与 e^{-S0} 同阶的相对值（绝对标度依赖格距）")
print("="*78)
for beta in (1,2,3):
    S0=2*math.pi*math.pi*beta; z=math.exp(-S0)
    print(f"  β={beta}: z={z:.3e}, log10 σ(∝z)={math.log10(z):.3f}")
print()
print("红线提示：上述数值为文献公式的复算/指数行为演示；")
print("4D 非阿贝尔质量间隙仍为克雷未解（第91章），3D 结果不可外推（维度谱标注）。")
print("EXIT 0")
