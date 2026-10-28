# -*- coding: utf-8 -*-
# C0387 T398 α 吸引子暴胀（α-attractor E/T 模型）：慢滚闭式 r/n_s/V0（mpmath 250 位）
from mpmath import mp, mpf, sqrt, exp, ln, power, pi
mp.dps = 250
import json

A_s = mpf('2.105e-9')                        # 标量振幅原初功率谱
N = mpf('55')                                # e-fold 数

def attractor(alpha):
    # T 模型：V = V0 (1 - exp(-sqrt(2/(3α)) φ))^2
    # N≫1 闭式：n_s = 1 - 2/N；r = 12α/N^2；φ_N = sqrt(3α/2) ln(4N/(3α))
    ns = 1 - 2 / N
    r = 12 * alpha / (N * N)
    V0 = (mpf('3') * pi * pi / 2) * r * A_s     # 振幅归一化
    phi_N = sqrt(mpf('3') * alpha / 2) * ln(4 * N / (3 * alpha))
    eps = r / 16                                # 慢滚第一参数（闭式）
    return ns, r, V0, phi_N, eps

ns1, r1, V01, phi1, eps1 = attractor(mpf('1'))
ns79, r79, V079, phi79, eps79 = attractor(mpf('7') / 9)
print('alpha=1    : n_s=%.10f  r=%.10f  V0=%.6e M_Pl^4  phi_N=%.6f M_Pl  eps=%.6e' % (ns1, r1, V01, phi1, eps1))
print('alpha=7/9  : n_s=%.10f  r=%.10f  V0=%.6e M_Pl^4  phi_N=%.6f M_Pl  eps=%.6e' % (ns79, r79, V079, phi79, eps79))

# E 模型（n=1 双曲正切）：r = 12α/N^2 同（渐近相同）；V = V0 tanh^2(φ/sqrt(6α))
# 与 C0310/C0316 希格斯暴胀同源衔接：r_Higgs = 4/N^2（α=1/3 特例）
r_higgs = 4 / (N * N)
print('r(alpha=1/3 Higgs 特例)=%.10f' % r_higgs)

entries = [
    {'id': 'C0387-1', 'claim': 'α 吸引子闭式 n_s = 1 - 2/N（N=55）', 'value': str(ns1), 'verdict': 'CLOSED'},
    {'id': 'C0387-2', 'claim': 'r = 12α/N^2（α=1）', 'value': str(r1), 'verdict': 'CLOSED'},
    {'id': 'C0387-3', 'claim': 'V0 = (3π^2/2) r A_s', 'value': str(V01), 'verdict': 'CLOSED'},
    {'id': 'C0387-4', 'claim': '场值 φ_N = sqrt(3α/2) ln(4N/(3α))', 'value': str(phi1), 'verdict': 'CLOSED'},
    {'id': 'C0387-5', 'claim': 'α=1/3 特例 r=4/N^2 衔接希格斯暴胀 C0310/C0316', 'value': str(r_higgs), 'verdict': 'CLOSED'},
    {'id': 'C0387-6', 'claim': 'TUFT 供给 0：无 α 预测，归因标准慢滚/双曲几何算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert abs(ns1 - mpf('0.9636363636363636')) < mpf('1e-12'), 'ns'
    guards.append('G1 n_s=0.9636 ok')
    assert r1 > mpf('0.0038') and r1 < mpf('0.0041'), 'r'
    guards.append('G2 r=3.97e-3 ok')
    assert V01 > mpf('1.1e-10') and V01 < mpf('1.4e-10'), 'V0'
    guards.append('G3 V0=1.24e-10 ok')
    assert phi1 > mpf('5.2') and phi1 < mpf('5.4'), 'phi'
    guards.append('G4 phi_N=5.26 M_Pl ok')
    assert abs(r_higgs - mpf('0.0013223140495867769')) < mpf('1e-12'), 'rh'
    guards.append('G5 r_Higgs=1.32e-3 衔接 ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 α 吸引子慢滚算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0387 T398 α 吸引子暴胀 E/T 模型（C1,C7）'}
with open('attack_C0387_α吸引子暴胀攻破_2026-10-21.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('G:')
for g in guards:
    print(g)
print('exit_code=%d' % exit_code)
