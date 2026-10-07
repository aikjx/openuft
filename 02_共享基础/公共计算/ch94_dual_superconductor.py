# -*- coding: utf-8 -*-
"""
第94章 配套复算脚本 ch94_dual_superconductor.py（纯标准库，exit 0）
双超导（对偶 Meissner）禁闭机制的可复核数值骨架：
 1) Meissner 指数屏蔽 B(x)=B0·e^{-x/λ_L}（λ_L=50 nm，铝典型值）
 2) 对偶 Meissner：色电场 E(r)~e^{-μr} 屏蔽（μ~1 GeV，与第92章 Debye 质量同构）
 3) 通量管能量/长度：E=σL（σ=0.1936 GeV²，√σ=0.44 GeV，1 fm=5.068 GeV⁻¹）
 4) 't Hooft–Mandelstam 对偶字典（打印）
 5) Abelian dominance 数值（Kronfeld–Laursen–Schierholz–Wiese 1987：~92%；后续 perfect dominance）
全部公式来自已引文献/格点口径，本书只做数值复算，不声称新推导。
"""
import math

HBC = 0.197327          # GeV·fm
FM_INV = 1.0/HBC        # 1 fm = 5.068 GeV^{-1}
SQRT_SIGMA = 0.44       # GeV
SIGMA = SQRT_SIGMA**2   # GeV²

print("="*78)
print("1) Meissner 效应：B(x) = B0·e^{-x/λ_L}（λ_L=50 nm，铝典型值）")
print("="*78)
lam = 50e-9  # m
print(f"   λ_L = {lam*1e9:.0f} nm = {lam*1e6:.2f} μm；B(2λ)={math.exp(-2):.3f}·B0, B(5λ)={math.exp(-5):.4f}·B0")
for xl in (0,1,2,3,5,10):
    print(f"   x/λ_L={xl:>3}: B/B0 = e^-{xl} = {math.exp(-xl):.5f}")

print()
print("="*78)
print("2) 对偶 Meissner：色电场屏蔽 E(r) ~ e^{-μr}（μ~1 GeV，与 Debye m_D 同构）")
print("="*78)
mu = 1.0  # GeV
print(f"   μ={mu} GeV；μ^{-1} = {1/mu:.3f} GeV⁻¹ = {1/(mu*FM_INV):.3f} fm（屏蔽长度）")
for r_fm in (0.1, 0.2, 0.5, 1.0, 2.0):
    r = r_fm*FM_INV
    E = math.exp(-mu*r)
    print(f"   r={r_fm:.2f} fm: E/E0 = e^-{mu*r:.3f} = {E:.5f}")

print()
print("="*78)
print("3) 通量管能量/长度：E = σ·L（线性势，禁闭签名）")
print("="*78)
print(f"   √σ=0.44 GeV → σ={SIGMA:.4f} GeV²")
print(f"   {'L (fm)':>7} {'L (GeV⁻¹)':>10} {'E=σL (GeV)':>12} {'E (MeV)':>9}")
for L_fm in (0.5, 1.0, 2.0, 3.0):
    L = L_fm*FM_INV
    E = SIGMA*L
    print(f"   {L_fm:>7.1f} {L:>10.4f} {E:>12.4f} {E*1000:>9.1f}")
print("   → 1 fm 通量管 ≈ 0.98 GeV：静夸克对分离 r 时势能 V(r)≈σr 线性上升（格点确认）")

print()
print("="*78)
print("4) 't Hooft–Mandelstam 对偶字典（机制类比，非推导）")
print("="*78)
dict_rows = [
 ("超导（电超导）", "QCD 对偶超导（磁超导）"),
 ("Cooper 对凝聚", "磁单极凝聚"),
 ("Meissner 排斥磁场", "对偶 Meissner 排斥色电场"),
 ("Abrikosov 磁涡旋线", "Nielsen–Olesen 色电通量管"),
 ("磁通量子 Φ0", "色电通量量子（中心荷）"),
 ("第二类超导 κ>1/√2", "QCD 型（κ 参数类比）"),
 ("穿透深度 λ", "通量管半径 ~0.3–0.5 fm（格点）"),
 ("BCS 能隙 Δ", "质量间隙 m（克雷问题！）"),
]
for a,b in dict_rows:
    print(f"   {a:<22} ↔  {b}")

print()
print("="*78)
print("5) Abelian dominance（Maximal Abelian Gauge 格点证据）")
print("="*78)
print("   Kronfeld–Laursen–Schierholz–Wiese 1987 (PLB198,516)：Abelian 弦张力 ≈ 92%")
print("   EPJ 2016：'perfect Abelian dominance' σ^Abel ≈ σ（QQ/3Q 体系）")
print("   hep-th/9805153：Abelian monopole dominance 证明框架")
print("   INSPIRE 2902125：Gribov copy 影响 ~86–90%（模拟退火固定规范）")
print("   → 数值证据 [A]：弦张力绝大部分由 Abelian 磁单极贡献；")
print("     但 4D 解析证明缺失：κ、λ、单极凝聚序参量均无第一性计算（[C]）")

print()
print("红线：对偶超导=机制设想（'t Hooft/Mandelstam/Nambu 1970s）；格点数值=[A] 证据级；")
print("4D 数学证明（克雷）仍缺失；双超导与中心涡旋（第93章）为互补但均未证机制；UFT 2/6。")
print("EXIT 0")
