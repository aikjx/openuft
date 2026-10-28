# -*- coding: utf-8 -*-
# C0385 T315 卷曲额外维 RS1：层级 ω=e^{kπr_c} 与 KK 引力子谱（mpmath 250 位）
from mpmath import mp, mpf, sqrt, exp, ln, power, pi
mp.dps = 250
import json

M_PL = mpf('1.2209100000000000e19')          # GeV
omega = mpf('1e15')                           # SM 层级 M_Pl/M_5D
k_over_M5 = mpf('0.1')                        # 曲率/5D 普朗克标度比
x1 = mpf('3.8317059702075123156')             # J_1 第一零点

kprc = ln(omega)                              # k π r_c = ln(omega)
M5 = M_PL / omega                             # 5D 普朗克标度
k = k_over_M5 * M5                            # 若 k 由 M5 决定
# 经典 RS1：k ~ 0.1 M_Pl（M_Pl 即 4D 约化普朗克质量），层级独立给出
k_classic = mpf('0.1') * M_PL
m1 = x1 * k_classic * exp(-kprc)              # 第一 KK 引力子质量（TeV 标度）
print('kπr_c=%.10f' % kprc)
print('M_5D=%.6e GeV' % M5)
print('k=%.6e GeV' % k_classic)
print('m1=%.6e GeV = %.4f TeV' % (m1, m1 / 1000))

# KK 塔：m_n = x_n k e^{-kπr_c}，x_n: J_1 零点（n=1..3）
x2 = mpf('7.0155866698156187')
x3 = mpf('10.1734681350627220')
m2 = x2 * k_classic * exp(-kprc)
m3 = x3 * k_classic * exp(-kprc)
print('m2=%.4f TeV  m3=%.4f TeV' % (m2 / 1000, m3 / 1000))

# 层级质量比闭式
ratio_21 = m2 / m1
print('m2/m1=%.8f' % ratio_21)

entries = [
    {'id': 'C0385-1', 'claim': '层级 kπr_c = ln(10^15) = 34.5388', 'value': str(kprc), 'verdict': 'CLOSED'},
    {'id': 'C0385-2', 'claim': '第一 KK 引力子 m1 = x1 k e^{-kπr_c} ≈ 4.67 TeV', 'value': str(m1), 'verdict': 'CLOSED'},
    {'id': 'C0385-3', 'claim': 'KK 塔 x_n 零点（3.8317/7.0156/10.1735）', 'value': str(ratio_21), 'verdict': 'CLOSED'},
    {'id': 'C0385-4', 'claim': '5D 标度 M_5D = M_Pl/10^15 = 1.22e4 GeV', 'value': str(M5), 'verdict': 'CLOSED'},
    {'id': 'C0385-5', 'claim': 'TUFT 供给 0：无 k/M_5D 预测，归因标准 RS1 算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert abs(kprc - mpf('34.538776394910684')) < mpf('1e-9'), 'kprc'
    guards.append('G1 kprc=34.5388 ok')
    assert m1 / 1000 > mpf('4.5') and m1 / 1000 < mpf('5.0'), 'm1'
    guards.append('G2 m1=4.67 TeV ok')
    assert abs(ratio_21 - mpf('1.8319')) < mpf('0.01'), 'r21'
    guards.append('G3 m2/m1=1.832 ok')
    assert M5 > mpf('1.2e4') and M5 < mpf('1.24e4'), 'M5'
    guards.append('G4 M5D=1.22e4 GeV ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 RS1 卷曲额外维算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0385 T315 卷曲额外维 RS1 与 Higgs 局域化（C1,C2）'}
with open('attack_C0385_RS1卷曲额外维攻破_2026-10-21.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('G:')
for g in guards:
    print(g)
print('exit_code=%d' % exit_code)
