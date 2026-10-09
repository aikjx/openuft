# -*- coding: utf-8 -*-
"""C₂ 方案依赖裁决: 引力对标量自耦合 β 的修正
来稿 β_α=C₁α²+C₂Gα+C₃G² (33 号: C₁=3/16π² 闭合, C₂/C₃ 开放)
本轮锚点:
 - dim-reg/MS-bar (33 号 C₁ 同框架): C₂=0 (Toms 2007/Pietrykowski/Ebert 共识, 0807.0331)
 - 功能RG/asymptotic safety: C₂=55/18π (arXiv 2306.17718 式8), β_m² 引力项 53/18π
验证数值 + 引力修正量级 (普朗克能标才显著)。
"""
import numpy as np
G_N=6.67430e-11; hbar=1.054571817e-34; c=299792458.0
Mpl=np.sqrt(hbar*c/G_N)  # ~2.18e-8 kg
Mpl_gev=Mpl*c**2/(1.602176634e-10)  # ~1.22e19 GeV (1GeV=1.602e-10 J)

print("== C₁ 复核 (33号) ==")
C1=3/(16*np.pi**2)
print(f" C₁=3/16π²={C1:.7f} ✓ (与33号一致)")

print("\n== C₂ 锚点 (两个框架) ==")
print(" dim-reg/MS-bar (与C₁同框架): C₂=0")
print("  依据: Toms (Vilkovisky-DeWitt, 2007), Pietrykowski, Ebert —")
print("  cut-off 与 dim-reg 下引力对物质β均无修正 (0807.0331)")
C2_fRG=55/(18*np.pi)
print(f" 功能RG/asymptotic safety: C₂=55/18π={C2_fRG:.6f}")
print(f"  依据: arXiv 2306.17718 式(8) β_λ4=...+55/18π·Gλ₄ (引力修正项)")
C2_m2=53/(18*np.pi)
print(f"  β_m² 引力项: 53/18π={C2_m2:.6f} (同文献式(6))")

print("\n== 引力修正的量级 (普朗克能标才显著) ==")
print(" 无量纲引力耦合 G(k)=(k/M_Pl)², M_Pl=1.22e19 GeV")
print("  k(GeV)      G=(k/M_Pl)²      C₂Gα项量级(C₂=0.973, α=0.1)")
for k in [1e1,1e3,1e6,1e9,1e12,1e16,1.22e19]:
    G=(k/Mpl_gev)**2
    print(f"  {k:6.1e}   {G:8.1e}   {C2_fRG*G*0.1:8.1e}")
print(" ⇒ G=1 在 k=M_Pl=1.22e19 GeV; 低能(k<<M_Pl) C₂Gα≪C₁α² 可忽略")
print(f" 例: k=1TeV → G={(1e3/Mpl_gev)**2:.1e}, C₂Gα={C2_fRG*(1e3/Mpl_gev)**2*0.1:.1e} ≪ C₁α²={C1*0.1:.3e}")

print("\n== 诚实结论 ==")
print(" ① C₂ 是正规化方案依赖: dim-reg=0 (与C₁同框架), 功能RG=55/18π")
print(" ② 来稿 β_α 若与 C₁=3/16π² 同框架(dim-reg)自洽 → C₂=0")
print(" ③ 即使取非零 C₂, 引力修正只在普朗克能标显著(低能可忽略)")
print(" ④ C₃(G²项): dim-reg 无 G² 对数项; 功能RG 方案依赖更强, 不构造数值")
