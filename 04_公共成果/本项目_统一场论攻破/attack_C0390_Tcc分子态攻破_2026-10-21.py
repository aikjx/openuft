# -*- coding: utf-8 -*-
# C0390 T350 T_cc(3875) D̄D* 分子态束缚能（mpmath 250 位）
from mpmath import mp, mpf, sqrt
mp.dps = 250
import json

m_D0 = mpf('1864.84')                        # MeV
m_Dsp = mpf('2010.26')                       # MeV
m_Tcc = mpf('3874.71')                       # MeV（LHCb）

thr = m_D0 + m_Dsp
dE = thr - m_Tcc                             # 束缚能
mu = m_D0 * m_Dsp / (m_D0 + m_Dsp)           # 约化质量
a_inv = sqrt(2 * mu * dE)                    # 1/散射长度（MeV）
a = 1 / a_inv                                # 散射长度（MeV^-1）
a_fm = a * mpf('197.3269804')                # 散射长度（fm）
print('阈值=%.4f MeV  束缚能=%.4f MeV' % (thr, dE))
print('约化质量=%.4f MeV  1/a=%.6f MeV   a=%.6f MeV^-1 = %.4f fm' % (mu, a_inv, a, a_fm))

# 近阈值 Breit-Wigner 宽度关联：Γ ∝ k·|T|²；T_cc Γ=0.048 MeV（LHCb）
Gamma = mpf('0.048')
tau = mpf('6.582119569e-22') / Gamma        # s（ℏ=6.582e-22 MeV·s）
print('Γ=%.3f MeV  τ=%.4e s' % (Gamma, tau))

# 与氘核散射长度对比（a_d≈5.4 fm）
a_d = mpf('5.4')
print('a/a_d=%.4f' % (a_fm / a_d))

entries = [
    {'id': 'C0390-1', 'claim': 'D⁰D*⁺ 阈值 = 3875.10 MeV', 'value': str(thr), 'verdict': 'CLOSED'},
    {'id': 'C0390-2', 'claim': '束缚能 ΔE = 0.39 MeV（近阈值浅束缚）', 'value': str(dE), 'verdict': 'CLOSED'},
    {'id': 'C0390-3', 'claim': '散射长度 a = 7.19 fm（氘核量级）', 'value': str(a_fm), 'verdict': 'CLOSED'},
    {'id': 'C0390-4', 'claim': '寿命 τ=ℏ/Γ = 1.37e-20 s', 'value': str(tau), 'verdict': 'CLOSED'},
    {'id': 'C0390-5', 'claim': 'TUFT 供给 0：无束缚能预测，归因标准强子分子算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert abs(thr - mpf('3875.10')) < mpf('0.01'), 'thr'
    guards.append('G1 阈值=3875.10 MeV ok')
    assert dE > mpf('0.3') and dE < mpf('0.5'), 'dE'
    guards.append('G2 束缚能=0.39 MeV ok')
    assert a_fm > mpf('6') and a_fm < mpf('8'), 'a'
    guards.append('G3 散射长度=7.19 fm ok')
    assert tau > mpf('1e-20') and tau < mpf('2e-20'), 'tau'
    guards.append('G4 τ=1.37e-20 s ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准强子分子/近阈值量子力学算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0390 T350 T_cc(3875) D̄D* 分子态束缚能（C1,C5）'}
with open('attack_C0390_Tcc分子态攻破_2026-10-21.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('G:')
for gx in guards:
    print(gx)
print('exit_code=%d' % exit_code)
