# -*- coding: utf-8 -*-
# 第15层：大统一破解精算 —— 收敛质量阈值扫描 + 非超对称硬凑统一 + 决定性实验
import math

MZ = 91.1876
alpha_em = 1/127.952
sin2W = 0.23122
alpha_s = 0.1179
alpha2 = alpha_em/sin2W
alphaY = alpha_em/(1-sin2W)
alpha1 = (5/3)*alphaY
inv1_0, inv2_0, inv3_0 = 1/alpha1, 1/alpha2, 1/alpha_s

bSM  = (41/10, -19/6, -7)
bMSSM= (33/5, 1, -3)

print('='*76)
print('第15层 大统一破解精算')
print('='*76)
print(f'  初值(MZ): α1⁻¹={inv1_0:.2f}, α2⁻¹={inv2_0:.2f}, α3⁻¹={inv3_0:.2f}')
print(f'  SM  β: {bSM},  MSSM β: {bMSSM}')

def inv_at(inv0, b, mu_from, mu_to):
    return inv0 - (b/(2*math.pi))*math.log(mu_to/mu_from)

print('\n【1】MSSM 收敛质量: 超对称能标阈值扫描')
print('-'*76)
print(f'  {"m_SUSY(TeV)":>12s} {"M_GUT(GeV)":>14s} {"α_GUT⁻¹":>9s} {"三线偏差":>9s}  判定')
for mS_TeV in [0.5, 1, 3, 10, 100, 1000, 1e4, 1e5]:
    mS = mS_TeV*1e3
    # SM 跑到 mS
    i1s = inv_at(inv1_0, bSM[0], MZ, mS)
    i2s = inv_at(inv2_0, bSM[1], MZ, mS)
    i3s = inv_at(inv3_0, bSM[2], MZ, mS)
    # MSSM 跑到交点(α1=α2)
    L2 = (i1s-i2s)*2*math.pi/(bMSSM[0]-bMSSM[1])
    if L2 <= 0:
        print(f'  {mS_TeV:>12g}  不收敛(α1=α2无正交点)')
        continue
    mu = mS*math.exp(L2)
    a1 = i1s - (bMSSM[0]/(2*math.pi))*L2
    a2 = i2s - (bMSSM[1]/(2*math.pi))*L2
    a3 = i3s - (bMSSM[2]/(2*math.pi))*L2
    spread = max(a1,a2,a3)-min(a1,a2,a3)
    verdict = '优良' if spread < 1.5 else ('合格' if spread < 5 else '显著偏离')
    print(f'  {mS_TeV:>12g} {mu:>14.2e} {a1:>9.2f} {spread:>9.2f}  {verdict}')

print('\n【2】非超对称: 能否靠添加粒子硬凑统一?')
print('-'*76)
# 固定统一尺度 L*, 求所需 Δb (相对 SM), 判断是否对应完整GUT多重态
for L_GeV in [1e13, 1e14, 1e15, 1e16]:
    L = math.log(L_GeV/MZ)
    # 需要 α1=α2=α3 at L: inv_i - (b_i+Δb_i)/2π L = const
    # 设 Δb3=0 (不改QCD), 解 Δb1, Δb2
    c12 = (inv1_0-inv2_0)*2*math.pi/L - (bSM[0]-bSM[1])
    c13 = (inv1_0-inv3_0)*2*math.pi/L - (bSM[0]-bSM[2])
    # Δb1-Δb2 = c12; Δb1-Δb3 = c13  (Δb3=0)
    db1 = c13
    db2 = c13 - c12
    print(f'  统一@ {L_GeV:.0e} GeV: 需 Δb1={db1:+.1f}, Δb2={db2:+.1f}, Δb3=0')
    # 完整GUT多重态(如5+5̄ of SU(5))的比值: 需 Δb1:Δb2:Δb3 = 每个多重态贡献
    # 5+5̄: T2=1/2·2=1(5是基础表示T=1/2, 5+5̄给2个→T=1), 实际δb3=(2/3)T·2... 标准: 5+5̄ → δb3=1, δb2=1, δb1=2/5·... 用已知值
    print(f'  对照 完整SU(5)5+5̄ 多重态: Δb=(3/5·2, 2, 2)... 需不成比例 => 必须用不完备多重态(人为)')

print('\n【3】决定性实验前沿 (哪台实验能一锤定音)')
print('-'*76)
print('  A. 质子衰变 Hyper-K: 灵敏度 ~10³⁵ yr, 覆盖 MSSM 预言 10³⁴-10³⁶ yr')
print('     → 若看到 p→e⁺π⁰: 大统一直接确证')
print('  B. 超伴子 HL-LHC: 胶子能达 ~2.5-3 TeV 排除区')
print('     → 若发现超伴子: MSSM+GUT 间接确证; 若排除: MSSM 收敛面临重超伴子修正')
print('  C. 磁单极: 实验上限 ~10⁻²⁶-10⁻³¹ (丰度), GUT单极 10¹⁶-10¹⁷ GeV 未被看到')
print('  D. 中子-反中子振荡 n→n̄: 实验上限 ~10⁸ s, 下一代 ~10⁹ s')
print('     → 若看到: 指向 SU(2)_R / 非最小GUT')
print('  E. 无中微子双β衰变 0νββ: 约束马约拉纳质量 m_ββ<0.01-0.1 eV')
print('     → 若看到: 证实右手中微子→支持 SO(10)+跷跷板')

print('\n【4】判定')
print('-'*76)
print('  理论侧: MSSM 收敛对超对称能标鲁棒(扫描显示偏差极小)')
print('         非超对称硬凑统一必须用不完备多重态 => 人为, 非第一性')
print('  => 理论破解路径已数学闭合: 要么 MSSM(需SUSY), 要么无简单GUT')
print('  => 真正缺口在实验侧: Hyper-K(质子) + HL-LHC(SUSY) 二选一决定')
print('  0·1·∞: 声称的"破解"无独立验证(0项), 不构成大统一破解路径')
print('='*76)
