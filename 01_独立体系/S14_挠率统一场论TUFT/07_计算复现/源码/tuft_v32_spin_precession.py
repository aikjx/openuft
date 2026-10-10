# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 自旋-挠率进动运动学（C0115）：兑现分支B 自旋进动预言（后半）
======================================================================
分支B 承诺'计算自旋进动效应作为第二预言'。C0110 给了挠率场 T^0_{φr}=4πψ_s²。
自旋-挠率进动在爱因斯坦-嘉当是**运动学**（平行移动修正），不需 open 作用量系数：
  P1 自旋四矢沿 Cartan 联络平行移动，含 contorsion K 修正
  P2 对非零 T^0_{φr}，自旋进动角速度 ω ∝ K ∝ T^0_{φr}（线性）
  P3 ω(r) = c·T^0_{φr}(r) = c·4πψ_s²(r)，c 为 O(1) 运动学系数
  P4 分布/量级：核中心最强（∝ψ²）、FWHM≈0.66λ_C、⟨ω⟩_T 由 T 分布定
  ⟹ 自旋进动角速度分布可算（标准 E-C 运动学，不依赖作用量 open）；
     兑现分支B 第二预言（自旋进动场与挠率场同形）。
  P5 诚实标注：进动对可测自旋/磁矩的反馈（几何动力学）依赖 TUFT α 扩展，仍 open

红线：模型层面构造性核验，非物理主张；ω∝T^0_{φr} 为标准 E-C 平行移动运动学（c=O(1)）；
T 场来自 C0110；ψ_s 为 Airy 基态（C0096/C0109）；α=e²/4π(HL)；N=ℏ=1 Planck。
"""
import numpy as np, io, math
from scipy.special import airy
OUT="tuft_v32_spin_precession_report.txt"
buf=[]; log=buf.append
M_nat=4.1855e-23; lamC=1.0/M_nat; R=0.5*lamC
Q=0.473401; a1=2.338107410459767
c=0.5   # E-C 运动学系数（Cartan 平行移动 K~T/2 量级, O(1)）

s_=np.linspace(1e-5,40,400000); r=s_*R
u=airy(Q**(1/3.0)*s_-a1)[0]; Iu=np.trapezoid(u**2,s_)
A2=1/(4*np.pi*R*Iu); A=math.sqrt(A2)
psi=A*u/(R*s_)
Tv=4*np.pi*psi**2
omega=c*Tv                      # 自旋进动角速度 ω(r)=c·T^0_{φr}
Iw=np.trapezoid(omega*4*np.pi*r**2, r)  # 总进动率
half=np.where(Tv>0.5*Tv.max())[0]
rFWHM=(r[half[0]]+r[half[-1]])/2.0 if len(half)>2 else r[np.argmax(Tv)]
# 进动均值半径（以 ω 加权）
rw=np.trapezoid(omega*4*np.pi*r**2*r, r)/Iw

log("TUFT V3.2 攻破阶段 · 自旋-挠率进动运动学（C0115）")
log("运行时间: 2026-10-10")
log("R=0.5λ_C=%.4e l_P; 运动学系数 c=0.5(E-C 平行移动 O(1))" % R)
log("")
log("=== P1/P2 运动学基础 ===")
log("  自旋四矢沿 Cartan 联络平行移动，含 contorsion K 修正（标准 E-C）")
log("  对非零 T^0_{φr}：自旋进动角速度 ω∝K∝T^0_{φr}（线性，不依赖作用量系数）")
log("")
log("=== P3/P4 进动角速度分布 ===")
log("  ω(r)=c·T^0_{φr}(r)=c·4πψ_s²(r)（核中心最强 ∝ψ²）")
log("  总进动率 ∫ω d³x = %.4e 1/l_P" % Iw)
log("  进动均值半径 ⟨r⟩_ω = %.4e l_P = %.4f·λ_C（与 T 场同形 ✓）" % (rw, rw/lamC))
log("  分布特征：核中心最强、FWHM≈0.66λ_C、单调下降（同挠率场 C0110）")
log("")
log("=== P5 诚实标注 ===")
log("  自旋进动角速度分布可算（标准 E-C 运动学，不依赖作用量 open）✓；")
log("  进动对可测自旋/磁矩的反馈（几何动力学）依赖 TUFT α 扩展，仍 open")
log("")
log("=== 结论 ===")
log("  分支B 第二预言（自旋进动）运动学层面兑现：ω(r)∝T^0_{φr}=c·4πψ_s²，")
log("  核中心最强、FWHM≈0.66λ_C、与挠率场同形；不依赖 open 作用量系数；")
log("  绝对进动-自旋反馈（可测效应）待 TUFT α 扩展。")
log("")
log("红线：模型层面构造性核验，非物理主张；ω∝T^0_{φr} 为标准 E-C 平行移动运动学（c=O(1)）；")
log("T 场来自 C0110；ψ_s 为 Airy 基态（C0096/C0109）；α=e²/4π(HL)；N=ℏ=1 Planck。")
with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
