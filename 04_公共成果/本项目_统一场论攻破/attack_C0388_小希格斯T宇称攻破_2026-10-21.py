# -*- coding: utf-8 -*-
# C0388 T326 小希格斯（little Higgs）T 宇称：集体压制闭式（mpmath 250 位）
from mpmath import mp, mpf, sqrt, power, pi
mp.dps = 250
import json

g = mpf('0.6529')                            # SU(2)_L 规范耦合
gp = mpf('0.3570')                           # U(1)_Y 耦合
f = mpf('1000')                              # little Higgs 破缺标度（GeV）
Lambda = 4 * pi * f                          # 强耦合截断 Λ ~ 4πf

# 集体对称性圈压制：δm_H² ~ (3g²/8π²)Λ²（两标量三重态，T 宇称下 1 圈主压制）
r_loop = 3 * g * g / (8 * pi * pi)           # δm_H²/Λ² 压制比
mH2 = r_loop * Lambda * Lambda
mH = sqrt(mH2)
print('压制比 r=%.10e' % r_loop)
print('Λ=%.6e GeV  m_H=%.6e GeV  (%.3f TeV)' % (Lambda, mH, mH / 1000))

# T 宇称：Z₂ 对称性——重光子 A_H 为 LKP 暗物质候选
mA_H = gp * f
print('重光子 A_H = g\' f = %.6e GeV (%.3f TeV)' % (mA_H, mA_H / 1000))

# 集体对称性判据：交换 g₁↔g₂ 保持 m_H² 不动（leading 对数抵消）
# 抵消比 = (g²/16π²)·(Λ²/f²) 相对裸 Λ² 项
cancel_ratio = (g * g / (16 * pi * pi)) * (Lambda * Lambda / (f * f))
print('圈抵消比（裸项相对）=%.10f' % cancel_ratio)

entries = [
    {'id': 'C0388-1', 'claim': '集体对称性压制比 δm_H²/Λ² = 3g²/8π²', 'value': str(r_loop), 'verdict': 'CLOSED'},
    {'id': 'C0388-2', 'claim': 'm_H ~ 1.6 TeV（Λ=4πf=12.6 TeV）', 'value': str(mH), 'verdict': 'CLOSED'},
    {'id': 'C0388-3', 'claim': 'T 宇称重光子 A_H = g\' f = 357 GeV（LKP）', 'value': str(mA_H), 'verdict': 'CLOSED'},
    {'id': 'C0388-4', 'claim': '圈抵消比 (g²/16π²)(Λ²/f²)', 'value': str(cancel_ratio), 'verdict': 'CLOSED'},
    {'id': 'C0388-5', 'claim': 'TUFT 供给 0：无 f/g 预测，归因标准 little Higgs 算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert abs(r_loop - mpf('1.6197e-2')) < mpf('0.01e-2'), 'r'
    guards.append('G1 压制比=1.62e-2 ok')
    assert mH > mpf('1500') and mH < mpf('1700'), 'mH'
    guards.append('G2 m_H=1.61 TeV ok')
    assert mA_H > mpf('350') and mA_H < mpf('365'), 'A_H'
    guards.append('G3 A_H=357 GeV ok')
    assert cancel_ratio > mpf('0.40') and cancel_ratio < mpf('0.45'), 'cr'
    guards.append('G4 抵消比=0.426 ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 little Higgs 集体对称性算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0388 T326 小希格斯 T 宇称（C1,C2）'}
with open('attack_C0388_小希格斯T宇称攻破_2026-10-21.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('G:')
for gx in guards:
    print(gx)
print('exit_code=%d' % exit_code)
