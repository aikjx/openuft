# -*- coding: utf-8 -*-
"""
第75章 四力强度阶梯与统一的真实门槛——耦合跑动/GUT/Planck/统一判据 精算复现
纯标准库。1 圈重整化群，GUT 归一化初始值取 PDG MSbar(MZ)。用法: python unification_ladder.py
"""
import math

MZ=91.1876
# GUT 归一化逆耦合 at MZ（MSbar，标准教科书值）
A1_0,A2_0,A3_0=59.0,29.6,8.5
# 1 圈 beta 系数：d(alpha_i^-1)/d ln mu = -b_i/(2pi)
b_SM ={"b1":41/10,"b2":-19/6,"b3":-7}
b_SUSY={"b1":33/5,"b2":1.0,"b3":-3.0}

def inv_alphas(L, b):
    a1=A1_0-(b["b1"]/(2*math.pi))*L
    a2=A2_0-(b["b2"]/(2*math.pi))*L
    a3=A3_0-(b["b3"])/(2*math.pi)*L
    return a1,a2,a3

def L(k,v): print(f"{k:46s} = {v}")

print("==== 1. 低能相对强度（在质子标度 m_p≈0.938 GeV）====")
a_em=1/137.036
a_s=1.0                       # 低能 O(1)
GF=1.1663787e-5; mp=0.938272
a_w=GF*mp**2/math.sqrt(2)     # 弱作用无量纲有效耦合 ~ G_F m_p^2
Ggev=6.708830e-39             # 牛顿常数 in GeV^-2 (=(hbar c)^? ; G=6.708e-39 GeV^-2)
a_g=Ggev*mp**2                # 两质子引力无量纲耦合
L("强 alpha_s (低能)", f"{a_s:g}")
L("电磁 alpha", f"{a_em:.2e}")
L("弱 G_F m_p^2/√2", f"{a_w:.2e}")
L("引力 G m_p^2/hbar c", f"{a_g:.2e}")
L("强/引力 跨度(数量级)", f"{math.log10(a_s/a_g):.0f} 个数量级")

print("\n==== 2. 关键质量/能标（GeV）====")
mP=1/math.sqrt(Ggev)
L("普朗克质量 m_P=1/sqrt(G)", f"{mP:.3e} GeV  (~1.22e19)")
L("约化普朗克质量 m_P/sqrt(8pi)", f"{mP/math.sqrt(8*math.pi):.3e} GeV (~2.4e18)")
L("Higgs vev v", "246.22 GeV")
L("Lambda_QCD", "~0.2 GeV（强作用标度）")

print("\n==== 3. 耦合常数随能标跑动（GUT 归一化 alpha^-1）====")
def table(b,name):
    print(f"--- {name} ---")
    print(f"{'log10 mu':>9} | {'alpha1^-1':>9} {'alpha2^-1':>9} {'alpha3^-1':>9}  (mu GeV)")
    for lg in [2,4,6,8,10,13,16,19]:
        mu=10**lg
        Lg=math.log(mu/MZ)
        a1,a2,a3=inv_alphas(Lg,b)
        print(f"{lg:>9} | {a1:9.2f} {a2:9.2f} {a3:9.2f}  ({mu:.1e})")
table(b_SM,"标准模型 SM（1圈）")
table(b_SUSY,"最小超对称 MSSM（1圈，超粒子未发现=[C]）")

print("\n==== 4. 两两交汇尺度（数值求根）====")
def crossing(b,i,j,namei,namej):
    def f(Lg):
        a=inv_alphas(Lg,b)
        return a[i]-a[j]
    lo,hi=0.0,60.0
    flo=f(lo)
    for _ in range(200):
        mid=(lo+hi)/2; fm=f(mid)
        if flo*fm<=0: hi=mid
        else: lo=mid;flo=fm
    Lx=(lo+hi)/2
    mu=MZ*math.exp(Lx)
    return mu
for b,nm in [(b_SM,"SM"),(b_SUSY,"MSSM")]:
    m12=crossing(b,0,1,"a1","a2")
    m23=crossing(b,1,2,"a2","a3")
    m13=crossing(b,0,2,"a1","a3")
    L(f"{nm}  alpha1=alpha2 交汇", f"{m12:.2e} GeV")
    L(f"{nm}  alpha2=alpha3 交汇", f"{m23:.2e} GeV")
    L(f"{nm}  alpha1=alpha3 交汇", f"{m13:.2e} GeV")
    spread=abs(math.log10(max(m12,m23,m13)/min(m12,m23,m13)))
    L(f"{nm}  三交点离散度(数量级)", f"{spread:.1f}  ({'近一点=GUT 证据' if spread<0.7 else '不成一点（三角形缺口）'})")

print("\n==== 5. GUT 可检验义务（[A] 实验限 / [C] 理论预言）====")
L("最小 SU(5) 质子寿命预言 p->e+pi0", "~10^31 年（[C]）")
L("Super-Kamiokande 下限(2020)", ">2.4e34 年（[A]）-> 排除最小非SUSY SU(5)")
L("Hyper-K 目标", "~10^35 年")
L("GUT 磁单极质量 ~m_P/alpha_GUT", "~10^17–10^18 GeV/c^2（MACMO 等未发现 [A 零结果]）")

print("\n==== 6. “直积群不是统一”的计数（S14 U6.1 教训）====")
# 直积群独立规范玻色子/耦合计数
L("SM 直积 SU(3)xSU(2)xU(1) 规范玻色子", "8+3+1 = 12，3 个独立耦合 g3,g2,g1")
L("真正单群 SU(5)/SO(10)", "1 个规范耦合（破缺后分化），含跨力规范玻色子 X,Y（致质子衰变）")
L("判据", "不产生跨力关系、不减少独立常数数 = 只是并排抄写，不是统一")

print("\n精算完成。")
