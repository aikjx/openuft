# -*- coding: utf-8 -*-
# 第7层延伸：核尺度自旋相关力实验方案与灵敏度分析
# EC挠率诱导自旋-自旋力，设计实验探针并定量评估灵敏度差距
import math

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
mn = 1.67492749804e-27   # 中子质量
mu_n = -9.6623651e-27    # 中子磁矩 J/T
me = 9.1093837015e-31

print('='*74)
print('第7层延伸：核尺度自旋相关力实验方案与灵敏度分析')
print('='*74)

print()
print('【A】物理信号：挠率诱导自旋-自旋力')
print('-'*74)
print('  EC消去挠率后产生自旋-自旋接触势(四费米相互作用):')
print('  V_ss(r) = (G/c²)·(S₁·S₂/r³)   [非长程力, 接触相互作用]')
print('  对中子等效"赝磁场": B_eff = V_ss/μ_n')
print()

# 微观尺度(1fm): 由第7层核子对能移换算
V_ss_1fm = 1.3e-38*1e6*1.602176634e-19  # MeV -> J
B_micro = V_ss_1fm/abs(mu_n)
print(f'  微观(核子对@1fm): V_ss = 1.3e-38 MeV')
print(f'    等效赝磁场 B_eff = V_ss/μ_n = {B_micro:.2e} T')
print(f'    对比磁屏蔽噪声(~1e-11 T): 低 {1e-11/B_micro:.0e} 个量级')
print()
# 宏观尺度(1mm): 1/r^3 衰减, 距离比 1fm->1mm = 1e12, 衰减 1e-36
r_ratio = (1e-3/1e-15)**3
B_macro = B_micro/r_ratio
print(f'  宏观(极化源@1mm): 距离放大 1e12 倍, 1/r³ 衰减 {r_ratio:.0e} 倍')
print(f'    等效赝磁场 B_eff ~ {B_macro:.2e} T')
print(f'    对比磁屏蔽噪声(~1e-11 T): 低 {1e-11/B_macro:.0e} 个量级')
print(f'  => 无论微观还是宏观, EC自旋-自旋赝磁场都远低于可探测水平')

print()
print('【B】经典实验灵敏度（中子/原子精密测量）')
print('-'*74)
# 中子EDM实验: 可探测能移 ~1e-26 eV 量级
E_EDM = 1e-26  # eV 可探测能移
# EC自旋-自旋能移: 核子对@1fm = 1.3e-38 MeV = 1.3e-32 eV
E_ss_nucleon = 1.3e-38*1e6  # MeV -> eV = 1.3e-32 eV
print(f'  中子EDM实验可探测能移: ~1e-26 eV')
print(f'  EC核子对自旋-自旋能移: ~1.3e-32 eV (@1fm)')
print(f'  差距: 灵敏度比EC预言大 {1e-26/1.3e-32:.0e} 倍')
print()

# 短程自旋相关力(类轴子力)搜索
print('  短程自旋相关力搜索(轴子类 monopole-dipole):')
print('  当前最好约束: 耦合 ~1e-22~1e-20 (相对核力, 依力程)')
g_nuclear = 1.0
g_bound = 1e-20
g_EC = 1.3e-38
print(f'  核力耦合: {g_nuclear:.0e}')
print(f'  当前实验对自旋相关力耦合上限: ~{g_bound:.0e} (最优)')
print(f'  EC预言的自旋-自旋耦合: ~{g_EC:.0e}')
print(f'  差距: 当前灵敏度比EC预言高 {g_bound/g_EC:.0e} 倍')
print(f'  => 需要灵敏度提升 ~{g_bound/g_EC:.0e} 倍才能触及EC预言')

print()
print('【C】实验方案设计（探测EC预言需的灵敏度目标）')
print('-'*74)
print('  方案1: 超冷中子自旋进动(类似nEDM)')
print('    - 极化固态氦/极化核自旋源作靶')
print('    - 测量中子自旋进动频率的源开关差')
print('    - 需要: 磁屏蔽+自旋极化为磁噪声的10^20倍抑制')
print('    - 现实: 无法达到, 但可设新物理上限')
print()
print('  方案2: 原子干涉/磁强计阵列')
print('    - 极化源周围放高灵敏原子磁强计')
print('    - 探测赝磁场 B_eff~1e-61 T @1mm (全极化源, 1/r³衰减)')
print('    - 需要: 灵敏度比现有磁强计(1e-15 T)高46个量级')
print('    - 现实: 无法达到')
print()
print('  方案3: 宇宙学/天体物理间接约束')
print('    - 中子星内部自旋极化可能放大挠率效应')
print('    - 可约束EC的量子修正(如果有)')
print('    - 现实: 仅设上限, 不触及预言')

print()
print('【D】结论：可观测性判定')
print('-'*74)
print('  EC预言的核尺度自旋相关力(耦合~1e-38核力)比当前最优实验')
print('  灵敏度(~1e-20核力)低 18 个数量级。')
print('  => 任何当前/近未来实验都无法直接探测EC挠率效应，')
print('     只能用于约束"比EC更强的"新自旋相关力(新物理)。')
print('  => EC的可检验性边界: 理论预言明确、但实验灵敏度差18个量级。')
print('     这是EC"正确但难验证"的根本原因，也是其"零参数无脆弱性"的来源。')
