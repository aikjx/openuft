# -*- coding: utf-8 -*-
"""
第73章 强相互作用的本源（SU(3)_c 色规范·渐近自由·禁闭·质量起源）——精算复现脚本
纯标准库。常数取 PDG/CODATA。用法: python strong_source_ladder.py
"""
import math

hbar = 1.054571817e-34      # J s
c    = 2.99792458e8
e    = 1.602176634e-19
GeV  = 1.602176634e-10      # 1 GeV in J
fm   = 1e-15                # m
hcbar_GeVfm = hbar*c/GeV/fm # ħc in GeV·fm  ≈ 0.1973

def L(k,v): print(f"{k:46s} = {v}")

print("==== 0. 换算常数 ====")
L("hbar c (GeV·fm)", f"{hcbar_GeVfm:.5f}  (~0.197327)")

print("\n==== 1. SU(3)_c 的群结构（[A]）====")
Nc = 3
n_g = Nc*Nc-1
L("色数 Nc", Nc)
L("胶子数 Nc^2-1", f"{n_g}（8 个，全部带色，非阿贝尔）")
L("生成元 Tr(Ta Tb)=delta/2 个数", f"{n_g}")
# β 函数一圈系数 b0 = (11 Nc - 2 nf)/3  (约定 alpha_s 跑动用 b0/(2pi))
for nf in (3,5,6):
    b0=(11*Nc-2*nf)/3
    L(f"b0=(33-2 nf)/3, nf={nf}", f"{b0:.3f}  (>0 => 渐近自由)")

print("\n==== 2. 渐近自由：alpha_s 随能标跑动（单圈，仅微扰区有效）====")
# 1/alpha_s(Q) = 1/alpha_s(MZ) + b0/(2pi) ln(Q^2/MZ^2)；单圈仅在 alpha_s<~0.5（Q 明显高于 Lambda）可信
a_MZ = 0.1179; MZ = 91.1876
def alpha_s(Q, nf=5, Q0=MZ, a0=a_MZ):
    b=(33-2*nf)/3
    inv=1.0/a0 + b/(2*math.pi)*math.log(Q*Q/(Q0*Q0))
    return 1.0/inv
L("alpha_s(MZ) 输入", a_MZ)
for Q,nfl in [(91.1876,5),(200.0,5),(1000.0,6)]:
    L(f"alpha_s(Q={Q:>8.1f} GeV, nf={nfl})（高能，单圈定性可靠）", f"{alpha_s(Q,nfl):.4f}")
print("  → Q 越高 alpha_s 越小 = 渐近自由（夸克在短程/高能近自由）。")
print("  低能方向（Q ↓）alpha_s 增大，到 Q ≲ 2–3 GeV 单圈越过 Landau 极点，微扰论失效；")
print("  PDG 高阶/实验值：alpha_s(m_b=4.18)≈0.22、alpha_s(m_J/psi=3.10)≈0.25、")
print("  alpha_s(m_tau=1.78)≈0.30；Q~质子(~0.94 GeV) alpha_s~O(1)：禁闭/手征破缺区，须格点 QCD（[A]）。")

print("\n==== 3. QCD 标度 Lambda_QCD（反解单圈 + PDG 对照）====")
b0=(33-2*5)/3
Lam1 = MZ*math.exp(-2*math.pi/(b0*a_MZ))
L("Lambda_QCD 单圈(nf=5) (GeV)", f"{Lam1:.4f}")
L("PDG 高阶 MSbar Lambda (~nf=5) (GeV)", "≈0.21（单圈偏低，量级一致：百 MeV）")
L("对应长度 hbar c/0.21GeV (fm)", f"{hcbar_GeVfm/0.21:.3f}  (~1 fm 强子尺度)")

print("\n==== 4. 禁闭：线性势与弦张力（[A] 格点/夸克偶素）====")
sigma = 1.0   # GeV/fm  弦张力
sigma_N = sigma*GeV/fm
L("弦张力 sigma", "≈1 GeV/fm")
L("  = N/m", f"{sigma_N:.4e} N/m")
L("  ≈ 吨力(每fm夸克分离)", f"{sigma_N/9.8/1000:.1f} 吨力")
E_1fm = sigma*1.0
L("拉开 1 fm 储能", f"{E_1fm:.1f} GeV")
L("产生一对轻夸克约需", "~2×(0.3 GeV 组分)≈0.6 GeV → 弦在 ~1 fm 断裂生新夸克，无自由夸克")
# Cornell 势在 J/psi r=0.5 fm，用物理 alpha_s≈0.25
aJ=0.25; r=0.5
V_coul=-4*aJ/(3*r); V_lin=sigma*r
L("J/psi r=0.5fm: 库仑项 -4 a_s/(3r) (GeV)", f"{V_coul:+.3f}  (a_s≈0.25)")
L("                  线性项 +sigma r (GeV)", f"{V_lin:+.3f}")

print("\n==== 5. 质量起源：质子的 99% 来自 QCD（脚本复算）====")
mp=0.938272; mu_md=0.0022+0.0047
L("质子质量 (GeV)", mp)
L("u+d 流夸克质量 (GeV)", f"{mu_md:.4f}")
L("Higgs 流质量占比", f"{mu_md/mp*100:.3f} %")
L("QCD 能量占比", f"{(1-mu_md/mp)*100:.3f} %")
# 组分夸克~300 MeV ×3
L("组分夸克质量(手征破缺后)×3 (GeV)", f"{3*0.300:.2f}  ≈ 质子质量")

print("\n==== 6. 核力=残余强作用：pi 介子 Yukawa 程（[A]）====")
mpi=0.1396  # GeV charged pion
R_pi=hcbar_GeVfm/mpi
L("pi 介子质量 (GeV)", mpi)
L("Yukawa 程 hbar/(m_pi c) (fm)", f"{R_pi:.3f}  (~1.4 fm，与核力程吻合)")
L("核子结合能/核子(铁, MeV)", "≈8.79（对比 QCD 标度 ~200 MeV 小两个量级）")

print("\n==== 7. 强作用 vs 电磁 vs 引力（低能强度，相对量级）====")
aem=1/137.036
L("高能 alpha_s(MZ)", f"{a_MZ:.4f}（与 alpha_em 同量级，微扰可用）")
L("低能 Q~质子 alpha_s", "≈O(1)（微扰论失效，格点 QCD 处理）")
L("alpha_em", f"{aem:.5f}")
L("低能 强/电 耦合比", f"~{1.0/aem:.0f} 倍以上（低能强作用远强于电磁）")
L("两质子核内(r=1fm) 库仑势能 (MeV)", f"{aem*hcbar_GeVfm/1.0*1000:.2f} (~1.44 MeV，远小于核束缚 ~8 MeV)")

print("\n精算完成。")
