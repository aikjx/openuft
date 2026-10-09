# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 核束缚溯源：挠率凝聚（挠率平方负压）审计（C0111）
======================================================================
C0093 假设核 = Poincaré 应力（conjecture），C0108 给出核平衡负压 P_airy=-U_es/(4πR*³)
=-6.45e-93 M_P/l_P³（内拉）。本审计把核束缚溯源到挠率凝聚：
  P1 挠率场 T^0_{φr}=4πψ_s²（C0110，唯一非零分量）
  P2 挠率平方缩并 T^{μνλ}T_{μνλ} = 2(T^0_{φr})²（两个反对称分量 φr/rφ）
  P3 爱因斯坦-嘉当有效能动张量：挠率平方项在作用量 (1/16πG)R 中 R=R̃-(3/4)T² 给出
     负压 P_torsion(r) = -(3/4)·(1/16πG)·T^{μνλ}T_{μνλ}(r) < 0（内拉）
  P4 对照 C0108 核负压 P_airy：比较量级与符号
  ⟹ 核束缚（内拉负压）可由挠率凝聚（挠率平方项）提供，符号一致；
     给 C0093 '核=Poincaré 应力' 一个模型层面构造性溯源（爱因斯坦-嘉当标准结果）。

红线：模型层面构造性核验，非物理主张；挠率平方项系数 -(3/4)(1/16πG) 为爱因斯坦-嘉当
标准规范（TUFT 作用量细节 open，α 扩展扇区）；G=c=ℏ=1(Pl)；ψ_s 为 Airy 基态（C0096/C0109）；
T 场来自 C0110。
"""
import numpy as np, io, math
from scipy.special import airy
OUT="tuft_v32_torsion_condensate_audit_report.txt"
buf=[]; log=buf.append
M_nat=4.1855e-23; lamC=1.0/M_nat; R=0.5*lamC
Q=0.473401; a1=2.338107410459767
G=1.0  # Planck

s_=np.linspace(1e-5,40,400000); r=s_*R
u=airy(Q**(1/3.0)*s_-a1)[0]; Iu=np.trapezoid(u**2,s_)
A2=1/(4*np.pi*R*Iu); A=math.sqrt(A2)
psi=A*u/(R*s_)
Tv=4*np.pi*psi**2                 # T^0_{φr}
T2=2*Tv**2                        # T^{μνλ}T_{μνλ}=2(T^0_{φr})² (φr/rφ)
I_T2=np.trapezoid(T2*4*np.pi*r**2, r)   # ∫T²缩并 d³x
Ptors=-(3.0/4.0)*(1.0/(16.0*np.pi*G))*T2  # 挠率负压 P_torsion(r)
P_tors_peak=Ptors.min()           # 最负（核中心）
# 加权平均压强（以 T² 密度加权）
Pavg=np.trapezoid(Ptors*T2*4*np.pi*r**2, r)/np.trapezoid(T2*4*np.pi*r**2, r)
# C0108 核负压
Ues=0.0033*M_nat
P_airy=-Ues/(4*np.pi*R**3)

log("TUFT V3.2 攻破阶段 · 核束缚溯源：挠率凝聚（挠率平方负压）审计（C0111）")
log("运行时间: 2026-10-10")
log("R=0.5λ_C=%.4e l_P; G=1(Pl); T^0_{φr}=4πψ_s² (C0110)" % R)
log("")
log("=== P1/P2 挠率平方密度 ===")
log("  T^{μνλ}T_{μνλ}=2(T^0_{φr})²（φr/rφ 两分量）")
log("  ∫T²缩并 d³x = %.4e 1/l_P³" % I_T2)
log("  挠率平方密度集中于核中心（ψ∝1/r ⟹ T²∝1/r⁴）")
log("")
log("=== P3 爱因斯坦-嘉当挠率负压 ===")
log("  R=R̃-(3/4)T² ⟹ P_torsion(r)=-(3/4)(1/16πG)T²<0（内拉）")
log("  峰值（核中心）P_tors,peak = %.4e M_P/l_P³ (<0 内拉 ✓)" % P_tors_peak)
log("  T²加权平均压强 P_tors,avg = %.4e M_P/l_P³ (<0 ✓)" % Pavg)
log("")
log("=== P4 对照 C0108 核负压 ===")
log("  C0108 平衡负压 P_airy = -U_es/(4πR*³) = %.4e M_P/l_P³"%P_airy)
log("  符号：两者均 <0（内拉）⟹ 挠率平方负压与核束缚同号 ✓")
log("  量级比 |P_tors,avg|/|P_airy| = %.2e（差约 43 个数量级 ✗）"% abs(Pavg/P_airy))
log("")
log("=== 结论（负面结果）===")
log("  **核束缚 ≠ 挠率平方凝聚**：爱因斯坦-嘉当挠率平方项 -(3/4)(1/16πG)T² 的负压")
log("  P_tors,avg=-7.46e-136 比核平衡负压 P_airy=-6.45e-93 小约 10⁴³ 个数量级，完全不足以")
log("  平衡 EM 自斥。符号虽同号（均内拉），但量级严重不匹配 ⟹ 排除'核=挠率平方凝聚'机制。")
log("  ⟹ C0093 '核=Poincaré 应力' 保持 conjecture（结构对应），其动力学来源不是挠率平方项；")
log("  核束缚的能动张量来源仍需 TUFT 作用量（α 扩展扇区，open）。")
log("  本负面结果为模型层面构造性排除：自旋孤子的挠率平方远弱于核束缚所需。")
log("")
log("红线声明：模型层面构造性核验，非物理主张；α=e²/4π(HL)；挠率平方系数 -(3/4)(1/16πG)")
log("为爱因斯坦-嘉当标准规范（TUFT 作用量细节 open，其他挠率高阶项/耦合可能贡献）；")
log("G=c=ℏ=1(Pl)；ψ_s 为 Airy 基态（C0096/C0109）；T 场来自 C0110。")
with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
