# -*- coding: utf-8 -*-
"""
P03 规范对称统一候选 · 第一次公设建模（内部群 GUT 路线）精算
纯标准库。用法: python p03_gut_first_formulation.py

依据：Georgi–Glashow SU(5)(1974)、SO(10)(Fritzsch-Minkowski/Georgi 1974)、
      1 圈规范耦合跑动、Coleman–Mandula 直积（第79/82章 定理Q）。
不继承 S07/S08/S09/S10 几何化谱系；统一只在内部因子进行。

复算内容:
  1. SU(5) 单代表示填充 5̄⊕10：维度、Σdim·Y、Σdim·Y³（Fraction 精确为0）、SU(5) 三角反常指数
  2. SO(10) 16 = 5̄⊕10⊕1（含右手中微子 ν^c）
  3. 耦合常数 1 圈跑动：SM 与 MSSM 两组 b，三耦合在高能的汇聚残差与 M_GUT
  4. SU(5) 树级 sin²θW=3/8 vs 实测 MZ
  5. 质子衰变：最小非SUSY SU(5) p→e⁺π⁰ vs Super-K 下限
  6. 几何本体输入计数（定理Q执行）：κ/τ/ω 在选群判据中出现次数
"""
from fractions import Fraction as Fr
import math

def L(k,v): print(f"{k:50s} = {v}")

print("="*84)
print(" 1. SU(5) 单代费米子表示填充（左手 Weyl）：5̄ ⊕ 10")
print("="*84)
# (名称, SU3表示维数贡献, SU2表示维数贡献, 超荷Y, SU5所属不可约, 多重数=dim3*dim2)
comp=[
 ("d^c  反下夸克", 3,1, Fr(1,3), "5bar"),
 ("L    轻子二重态", 1,2, Fr(-1,2),"5bar"),
 ("Q    夸克二重态", 3,2, Fr(1,6), "10"),
 ("u^c  反上夸克", 3,1, Fr(-2,3),"10"),
 ("e^c  反带电轻子",1,1, Fr(1),   "10"),
]
sumdim=0; sumY=Fr(0); sumY3=Fr(0); dim_by_rep={"5bar":0,"10":0}
print(f"{'分量':<22}{'rep':<6}{'dim3×dim2':<12}{'Y':<8}{'dim·Y':<10}{'dim·Y³(分数)'}")
for n,d3,d2,Y,rep in comp:
    dim=d3*d2; sumdim+=dim; sumY+=dim*Y; sumY3+=dim*Y**3; dim_by_rep[rep]+=dim
    print(f"{n:<20}{rep:<7}{d3}×{d2}={dim:<5d}{str(Y):<8}{str(dim*Y):<10}{dim}·({str(Y)})³")
L("5̄ 维度", dim_by_rep["5bar"]); L("10 维度", dim_by_rep["10"])
L("单代左手 Weyl 总数 5̄+10", f"{sumdim}（与第76章 S06 审计单代15一致）")
L("Σ dim·Y（电荷中性必要条件）", f"{sumY}")
L("Σ dim·Y³（U(1) 三角反常抵消）", f"{sumY3}  → 精确为 0：{sumY3==0}")
# SU(5) 不可约表示的三角反常指数 A(R)（基础 5 的 A=1）
A={"5":1,"5bar":-1,"10":1,"1":0}
anom=A["5bar"]+A["10"]
L("SU(5) 三角反常指数 A(5̄)+A(10)", f"{A['5bar']}+{A['10']} = {anom}  → 无反常：{anom==0}")

print()
print("="*84)
print(" 2. SO(10)：单代 16 = 5̄ ⊕ 10 ⊕ 1")
print("="*84)
L("16 维度", "5+10+1 = 16")
L("多出的单态 1", "ν^c 右手中微子（SM 单代15态之外），自然给出轻中微子（see-saw 素材）")
L("SO(10) 单群装一代", "是（16 一个不可约表示即装一代全部费米子，含 ν^c）")
L("SU(5) vs SO(10)", "SU(5) 需 5̄⊕10 两个表示；SO(10) 单表示 16，结构更紧")

print()
print("="*84)
print(" 3. 规范耦合 1 圈跑动：SM vs MSSM（输入取 MZ 实测）")
print("="*84)
MZ=91.1876
aEM_inv=127.951
s2=0.23122
c2=1-s2
alpha_s=0.1179
a1_inv=(Fr(3,5))*aEM_inv*c2          # SU(5) 归一化 g1=√(5/3)g'
a2_inv=aEM_inv*s2
a3_inv=1.0/alpha_s
L("α_EM^{-1}(MZ)", f"{aEM_inv}")
L("sin²θW(MZ)", f"{s2}")
L("α1^{-1}(MZ)=(3/5)αEM^{-1}cos²", f"{float(a1_inv):.3f}")
L("α2^{-1}(MZ)=αEM^{-1}sin²", f"{float(a2_inv):.3f}")
L("α3^{-1}(MZ)=1/αs", f"{a3_inv:.3f}")
two_pi=2*math.pi
def run(ainv0,b,mu):
    return ainv0-(b/two_pi)*math.log(mu/MZ)
def meet12(ainv0,b):
    # (a1-a2)=(b1-b2)/2π L
    Lln=two_pi*(ainv0[0]-ainv0[1])/(b[0]-b[1])
    return MZ*math.exp(Lln),Lln
for label,b in [("SM",(41/10,-19/6,-7)),("MSSM",(33/5,1.0,-3.0))]:
    mu,Lln=meet12((a1_inv,a2_inv),b)
    vals=[run(a1_inv,b[0],mu),run(a2_inv,b[1],mu),run(a3_inv,b[2],mu)]
    spread=max(vals)-min(vals)
    print(f"\n[{label}] b=(b1,b2,b3)=({b[0]},{b[1]:.4f},{b[2]})")
    L("  α1=α2 交汇能标 M12", f"{mu:.3e} GeV  (ln μ/MZ={Lln:.2f})")
    L("  该处 α1^{-1},α2^{-1},α3^{-1}", f"{vals[0]:.2f}, {vals[1]:.2f}, {vals[2]:.2f}")
    L("  三耦合最大散布 spread", f"{spread:.3f}  → {'汇聚良好(<0.2)' if spread<0.2 else '不汇聚(>1)：最小模型失败'}")
print("\n  读法：1 圈 SM 三耦合在 1-2 交汇点与 α3 相差约 5.6（不严格汇聚）；")
print("  MSSM 三耦合在 ~2×10^16 GeV 汇聚（散布<0.1），但需整套超对称（LHC 零超粒子）。")

print()
print("="*84)
print(" 4. SU(5) 树级弱角 vs 实测")
print("="*84)
L("SU(5) 树级 sin²θW(M_GUT)", f"{3/8:.4f}（g1=g2 ⇒ 3/8）")
L("实测 sin²θW(MZ)", f"{s2}")
L("差距", f"跑动后由 MSSM 修正到~0.231 吻合；最小非SUSY SU5 1圈预测偏低(~0.20-0.21)")

print()
print("="*84)
print(" 5. 质子衰变：最小非 SUSY SU(5) 已被实验排除")
print("="*84)
MX_minSU5=1.0e15
tau_pred=(1.0e29,1.0e31)
SK_limit=1.6e34
L("最小非SUSY SU(5) X/Y 玻色子质量 M_X", f"~{MX_minSU5:.0e} GeV")
L("预言 τ(p→e⁺π⁰)", f"~10^{int(math.log10(tau_pred[0]))}–10^{int(math.log10(tau_pred[1]))} 年")
L("Super-K 下限(2020)", f">{SK_limit:.1e} 年")
L("最小非 SUSY SU(5)", f"被排除（预言比下限短约 {SK_limit/1e31:.0f}–{SK_limit/1e29:.0f} 倍）")
L("MSSM SU(5)/SO(10)", "M_GUT~2e16；经 dimension-5 算符 p→K⁺ν̄，τ~1e34–1e35，部分参数空间被挤压")

print()
print("="*84)
print(" 6. 几何本体输入计数（定理 Q 的执行）：螺旋量是否参与选群？")
print("="*84)
criteria=[
 ("单代费米子可装入最少表示","内部表示论（5̄⊕10 / 16）","否"),
 ("三角反常 Σdim·Y³=0、A(R)=0","内部群表示论","否"),
 ("三耦合在某能标汇聚","规范 β 函数（内部力 RG）","否"),
 ("sin²θW 与质子衰变对标","电弱测量/强子实验","否"),
 ("破缺链 G→SM 与 Higgs 表示","内部群分支律","否"),
]
geo=0
print(f"{'选群判据':<34}{'依据领域':<24}{'是否用κ/τ/ω/螺旋'}")
for c,dep,used in criteria:
    print(f"{c:<32}{dep:<26}{used}")
    if used=="是": geo+=1
L("几何本体输入计数", f"{geo}/5  → openuft 螺旋/频率本体对 G 的选择贡献 0 个非平凡输入")
print(""" 判决（定理Q直接推论）：G=SU(5)/SO(10)/E6 的选择、表示填充、破缺与汇聚尺度全部由
 内部表示论+规范RG+实验决定，曲率κ/挠率τ/涡量ω/螺旋频率不出现在任何一项。P03 是健康的
 内部群研究纲领，但不是 openuft 螺旋本体的产物，也不借 GUT 统一引力或第一性给出 α。""")

print()
print("="*84)
print(" P03 建模结论（诚实分级）")
print("="*84)
print(" 状态提升：unformulated_direction/unformulated → candidate_framework/unreviewed")
print(" [A] 标准数学/物理事实：5̄⊕10 装15态、ΣY³=0、反常指数0、SO10 16、SM 不汇聚、MSSM ~2e16 汇聚、3/8、质子排除。")
print(" [B] 本库建模：6 条公设（A1直积边界…A6几何零贡献）＋破缺链＋对标量；候选身份。")
print(" [C] 开放：SU5/SO10/E6 选谁、破缺势参数、Yukawa(≥SM自由参数)；MSSM 需无证据的超对称。")
print(" UFT：GUT 不统一引力(UFT-2 仍❌)、耦合统一不给 α 绝对值(UFT-3 仍❌)、无外部验证(UFT-6❌) ⇒ 维持 2/6。")
print(" 脚本纯标准库（fractions 精确反常计数）exit 0。")
