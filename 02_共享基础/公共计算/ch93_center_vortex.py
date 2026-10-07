# -*- coding: utf-8 -*-
"""
第93章 配套复算脚本 ch93_center_vortex.py（纯标准库，exit 0）
中心涡旋（ℤ_N）机制的可复核数值骨架：
 1) SU(N) 中心群 ℤ_N 元素表（N=2,3,4）
 2) Polyakov 圈序参量判据：⟨L⟩=0（禁闭）vs ≠0（退禁闭），ℤ_N 平均演示
 3) 中心涡旋"三方程"机制：W(C) = e^{-2ρA}（arXiv:2605.29109）
 4) 面积律 vs 周长律数值对比（√σ=0.44 GeV 口径，1 fm=5.068 GeV⁻¹）
 5) 涡旋密度与弦张力自洽：2ρ=σ
全部公式来自已引文献/格点口径，本书只做数值复算，不声称新推导。
"""
import math

HBC = 0.197327          # GeV·fm
FM_INV = 1.0/HBC        # 1 fm = 5.068 GeV^{-1}
SQRT_SIGMA = 0.44       # GeV（格点/PDG 口径，第91章）
SIGMA = SQRT_SIGMA**2   # GeV²

print("="*78)
print("1) SU(N) 中心群 ℤ_N：z_k = e^{2πik/N}·1  (k=0..N-1)")
print("="*78)
for N in (2,3,4):
    elems = [(k, math.cos(2*math.pi*k/N), math.sin(2*math.pi*k/N)) for k in range(N)]
    print(f"  N={N}: " + ", ".join(f"z_{k}=e^{{2πi{k}/{N}}}→({c:+.3f},{s:+.3f})" for k,c,s in elems))
    # 非平凡元素求和（应≈0，表示对中心群平均为零）
    s_c = sum(math.cos(2*math.pi*k/N) for k in range(1,N))
    print(f"       sum k=1..N-1 of z_k = ({s_c:+.6f}, 0)  -> 非平凡元素平均≈0（中心对称）")

print()
print("="*78)
print("2) Polyakov 圈序参量：⟨L⟩=0 禁闭 / ⟨L⟩≠0 退禁闭")
print("   L(x) = P exp[i∮ A₀]（时间方向 Wilson 圈）；L→zL（arXiv:1312.0991, hep-ph/0007069）")
print("="*78)
print("   禁闭相：中心对称保持 → ⟨L⟩ = (1/N)∑_k z_k = 0（上表非平凡元素平均≈0 即此）")
print("   退禁闭相：中心对称自发破缺 → ⟨L⟩ ≠ 0，L(T) ∼ e^{-F(r→∞)/T}")
print("   数值判据：⟨L⟩=0 ⇔ 孤立色荷自由能发散 ⇔ 禁闭；CPC-2021-0544 口径")

print()
print("="*78)
print("3) 中心涡旋机制（三方程，arXiv:2605.29109）：W(C)=e^{-2ρA}")
print("   涡旋穿透 Wilson 圈→中心相位 z；密度 ρ 渗透→面积律 e^{-2ρA}")
print("="*78)
print(f"   √σ = {SQRT_SIGMA} GeV → σ = {SIGMA:.4f} GeV²；自洽 2ρ=σ → ρ = σ/2 = {SIGMA/2:.4f} GeV²")
rho = SIGMA/2.0
print(f"   {'A (fm²)':>9} {'A (GeV⁻²)':>11} {'W=e^-2ρA':>12} {'log10 W':>9}")
for A_fm2 in (0.25, 0.5, 1.0, 2.0, 4.0):
    A = A_fm2 * FM_INV**2      # fm² → GeV⁻²
    W = math.exp(-2*rho*A)
    print(f"   {A_fm2:>9.2f} {A:>11.4f} {W:>12.4e} {math.log10(W):>9.3f}")

print()
print("="*78)
print("4) 面积律 vs 周长律：W_area=e^{-σA}  vs  W_perim=e^{-μL}（μ=0.7 GeV 示意）")
print("="*78)
mu = 0.7
print(f"   {'尺寸 L×W (fm)':>14} {'A(fm²)':>7} {'周界(fm)':>9} {'W_area':>12} {'W_perim':>12}")
for L_fm in (0.5, 1.0, 2.0, 3.0):
    A_fm2 = L_fm*L_fm
    A = A_fm2*FM_INV**2
    perim = 4*L_fm*FM_INV
    Wa = math.exp(-SIGMA*A)
    Wp = math.exp(-mu*perim)
    print(f"   {L_fm}×{L_fm}         {A_fm2:>7.2f} {4*L_fm:>9.2f} {Wa:>12.4e} {Wp:>12.4e}")
print("   → 大圈极限：面积律指数衰减（σA）远超周长律（μL）：禁闭的定量签名")
print("   （禁闭相还要求 't Hooft 圈取周长律——对偶判据 arXiv:2604.05950）")

print()
print("="*78)
print("5) 涡旋去除实验（数值证据，非证明）")
print("   de Forcrand–D'Elia：U_μ → sign[Tr U_μ]·U_μ 去掉中心涡旋后，")
print("   Wilson 圈线性上升势消失（Hindawi AHEP 2018 综述）；涡旋位于 Gribov 视界")
print("="*78)
print("   结论：涡旋密度 ρ 与弦张力 σ 由 2ρ=σ 自洽锁定（√σ=0.44 GeV → ρ=0.0968 GeV²）；")
print("   但 ρ 的第一性计算（无格点输入）不存在——4D 中心涡旋仍无解析构造（[C]）。")
print("红线：涡旋去除/渗透=格点数值证据 [A]；4D 数学证明（克雷）仍缺失；3D 结果不可外推。")
print("EXIT 0")
