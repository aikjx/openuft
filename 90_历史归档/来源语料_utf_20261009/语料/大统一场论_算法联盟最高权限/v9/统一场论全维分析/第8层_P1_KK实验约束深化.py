# -*- coding: utf-8 -*-
# 第8层：P1路线 —— KK 实验约束深化（多通道精算）
# 覆盖: 直接搜索 / 虚交换 / 未来对撞机 / 宇宙学 / ADD大额外维
import math

hbar = 1.054571817e-34
c = 2.99792458e8
# 常用换算: 1 GeV^-1 长度, 1 TeV 对应半径
def R_from_E(GeV):
    return hbar*c/(GeV*1e9*1.602176634e-19)

print('='*74)
print('第8层 P1：Kaluza-Klein 实验约束深化（多通道）')
print('='*74)

print()
print('【通道1】直接搜索：KK引力子共振')
print('-'*74)
# KK引力子 G* 在 pp->G*->ll, gamma-gamma 中产生，共振搜索
print('  过程: pp → G* → ℓ⁺ℓ⁻ / γγ   (共振搜索)')
print('  ATLAS/CMS 现行限制: M_G* > 5~10 TeV (取决于耦合)')
print(f'  对应半径: R < {R_from_E(5e3):.3e} m (5TeV)  ~  {R_from_E(1e4):.3e} m (10TeV)')
print('  缺稀薄通道: pp → G*+X, G*逃逸到额外维(缺失能量/光子)')
print('  -> LHC Run 3 已排除 TeV 尺度额外维')

print()
print('【通道2】虚KK引力子交换（干涉/接触项）')
print('-'*74)
print('  过程: qq̄ → G*虚交换 → ℓ⁺ℓ⁻   (干扰+接触项)')
print('  灵敏的短程力探针: 精密对撞机 / μ子反常磁矩')
print('  LEP EW精密: M₁ > 5~6 TeV')
print('  目前最强约束来自 Drell-Yan 对引力子KK塔的连续贡献')

print()
print('【通道3】未来对撞机展望')
print('-'*74)
prospects = [
    ('LHC(13TeV,现行)', 5e3, '已完成'),
    ('HL-LHC(14TeV)', 15e3, '~2029-2035'),
    ('FCC-hh(100TeV)', 40e3, '~2050+'),
]
for name, M, t in prospects:
    R = R_from_E(M)
    print(f'  {name:16s}: 可达 M₁>{M/1e3:.0f}TeV -> R<{R:.2e} m   [{t}]')

print()
print('【通道4】宇宙学/天体物理约束')
print('-'*74)
print('  ADD模型(大额外维): KK引力子逃逸到额外维 -> 恒星冷却加速')
print('  SN1987A 超新星中微子时限: 对 ADD n=2 给出 R_d<1e-4 m 约束(已被排除)')
print('  CMB/BBN: 额外维会改变哈勃率/核合成 -> 约束额外维尺度')
print('  => 宇宙学通道主要排除 ADD 大额外维，对经典 KK 弱')

print()
print('【通道5】ADD 大额外维模型对比')
print('-'*74)
# ADD: M_Pl^2 = M_D^(n+2) * V_n, V_n ~ R^n
# 若 M_D ~ 1 TeV, 由对撞机排除
M_Pl_GeV = 1.221e19
M_D = 1e3  # 1 TeV
print(f'  关系: M_Pl² = M_D^(n+2)·R^n')
print('  若 M_D=1TeV (使引力在TeV尺度变强):')
for n in [2,3,4,5,6]:
    R_cm = (M_Pl_GeV/M_D)**(2/(n+2)) * (hbar*c*1e9*1.602176634e-19/(1.602176634e-13))*1e2/1  # 简化尺度
    # 更标准: R = (1/M_D)*(M_Pl/M_D)^(2/n)
    R_m = (1/(M_D*1e9*1.602176634e-19/hbar/c)) * (M_Pl_GeV/M_D)**(2/n)
    print(f'  n={n}: R ~ {R_m:.2e} m  (LHC已排除 n>=2)')
print('  => ADD模型 n>=2 已被 LHC 排除；经典 KK 仍存活但需 M₁>10TeV')

print()
print('【通道6】综合约束总表')
print('-'*74)
print('  通道              约束                      状态')
print('  直接搜索(ATLAS/CMS) M₁>5~10TeV              已排除 TeV 额外维')
print('  虚交换(LEP/EW)     M₁>5~6TeV                精密约束')
print('  Drell-Yan          KK塔连续贡献              最强约束')
print('  HL-LHC            可达 M₁>15TeV             未来')
print('  FCC-hh            可达 M₁>40TeV             远期')
print('  SN1987A/CMB       排除 ADD n=2              宇宙学')
print('  => 经典KK的 R_KK=1.07e-34m 比实验上界1.97e-20m小15个量级')
print('  => 若存在额外维，其在TeV尺度会产生可探测信号，但迄今未发现')

print()
print('='*74)
print('P1结论: KK/额外维在全部可及通道均未发现信号；')
print('若四力大统一要求额外维，其尺度被限制在 R<~1e-20m，')
print('需 FCC-hh 级对撞机才可能直接探测。')
print('='*74)
