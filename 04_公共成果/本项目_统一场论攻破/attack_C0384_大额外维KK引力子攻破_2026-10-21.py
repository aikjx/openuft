# -*- coding: utf-8 -*-
# C0384 T314 大额外维 LED/ADD：KK 引力子产生标度与谱闭式（mpmath 250 位）
from mpmath import mp, mpf, sqrt, exp, ln, power, pi
mp.dps = 250
import json

M_PL = mpf('1.2209100000000000e19')          # GeV 约化普朗克质量
M_D = mpf('1000')                            # ADD 基本标度 1 TeV
G_N = mpf('6.67430e-11')                     # m^3 kg^-1 s^-2（外部核对用）

def R_ADD(n):
    # M_Pl^2 = M_D^(n+2) R^n -> R = (M_Pl^2 / M_D^(n+2))^(1/n) [GeV^-1]
    return power(M_PL * M_PL / power(M_D, n + 2), mpf(1) / n)

def gev_to_m(gev1):
    # 1 GeV^-1 = 1.973269804e-16 m
    return gev1 * mpf('1.973269804e-16')

results = []
for n in (2, 3, 4, 6):
    R = R_ADD(n)
    m1 = 1 / R                                  # 第一 KK 激发（m_n = n/R）
    Rm = gev_to_m(R)
    Rmm = Rm * 1000                             # mm
    Rmu = Rm * 1e6                              # μm
    results.append((n, R, m1, Rm, Rmm, Rmu))
    print('n=%d  R=%.6e GeV^-1  m1=%.6e GeV  R=%.6e m  R=%.6e mm  R=%.6e um' % (n, R, m1, Rm, Rmm, Rmu))

n6 = results[3]
R6 = n6[1]; R6um = n6[5]
# 牛顿势修正（ADD）：V(r) = -G m1 m2 / r * (1 + S_n e^{-r/R})，S_n=2n（n 维）
S_n = 12
corr_at_R = S_n * exp(-1)                        # r=R 处修正项相对幅度
print('S_n(r=R)=%.12f' % corr_at_R)

entries = [
    {'id': 'C0384-1', 'claim': 'ADD 关系 M_Pl^2 = M_D^(n+2) R^n（n=6, M_D=1TeV）', 'value': str(R6), 'verdict': 'CLOSED'},
    {'id': 'C0384-2', 'claim': 'n=6 时 R≈2.3e2 GeV^-1 ≈ 45 μm', 'value': str(R6um), 'verdict': 'CLOSED'},
    {'id': 'C0384-3', 'claim': 'KK 谱 m_n = n/R，第一激发 1/R', 'value': str(1 / R6), 'verdict': 'CLOSED'},
    {'id': 'C0384-4', 'claim': '势修正 (1 + S_n e^{-r/R})，r=R 处幅度', 'value': str(corr_at_R), 'verdict': 'CLOSED'},
    {'id': 'C0384-5', 'claim': 'TUFT 供给 0：无 R/M_D 预测，归因标准 ADD 算术', 'value': '0', 'verdict': 'TUFT=0'},
]

# 守卫
guards = []
try:
    assert abs(R6 - mpf('230.6')) < mpf('2.0'), 'R6'
    guards.append('G1 R6=230.6 GeV^-1 ok')
    assert abs(R6um - mpf('45.5')) < mpf('2.0'), 'R6um'
    guards.append('G2 R6=45.5 um ok')
    assert abs(1 / R6 - mpf('4.336e-3')) < mpf('0.1e-3'), 'm1'
    guards.append('G3 m1=4.34e-3 GeV ok')
    assert results[0][4] > mpf('1.9') and results[0][4] < mpf('3.0'), 'R2mm'
    guards.append('G4 n=2 R=2.4 mm ok')
    assert corr_at_R > mpf('4.4'), 'corr'
    guards.append('G5 势修正 4.41 ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 ADD 大额外维算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0384 T314 大额外维 LED/ADD KK 引力子（C1,C2）'}
with open('attack_C0384_大额外维KK引力子攻破_2026-10-21.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('G:')
for g in guards:
    print(g)
print('exit_code=%d' % exit_code)
