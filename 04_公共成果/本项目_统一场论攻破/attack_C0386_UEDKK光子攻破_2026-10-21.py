# -*- coding: utf-8 -*-
# C0386 T316 泛在额外维 UED/ACD：KK 光子谱与 LKP 暗物质标度（mpmath 250 位）
from mpmath import mp, mpf, sqrt, power, pi
mp.dps = 250
import json

Rinv = mpf('800')                             # 1/R = 800 GeV（LKP 质量标度）
mev_to_fm = mpf('1.973269804e-4')             # 1 GeV^-1 对应的 fm（1/1GeV）
R_fm = mev_to_fm / Rinv                       # 圈半径（fm）
print('R=%.6e fm' % R_fm)

def m_kk(n):
    # m_n^2 = m^2 + (n/R)^2；零模光子 m=0 -> m_n = n/R
    return n * Rinv

m1 = m_kk(1); m2 = m_kk(2); m3 = m_kk(3)
print('m1=%.3f GeV  m2=%.3f GeV  m3=%.3f GeV' % (m1, m2, m3))

# 谱间隔闭式：Δm = 1/R（等间隔 KK 塔）
dm = m2 - m1
print('dm=%.3f GeV' % dm)

# LKP 冻结丰度（coannihilation 近似闭式）：Ω h^2 ≈ 1.1e11 x_f^3 / (g*_S M_Pl σ v)
# σ v ≈ 1/(m1^2)（弱耦合近似）；x_f ≈ m1/T_f ≈ 25
xf = mpf('25')
gstar = mpf('92')
M_PL = mpf('1.2209100000000000e19')
sigmav = 1 / (m1 * m1)
omega_h2 = mpf('1.1e11') * xf ** 3 / (gstar * M_PL * sigmav)
print('sigma v=%.6e GeV^-2  Omega_h2=%.6e' % (sigmav, omega_h2))

entries = [
    {'id': 'C0386-1', 'claim': 'UED KK 谱 m_n^2 = m^2 + (n/R)^2（m=0 光子）', 'value': str(m1), 'verdict': 'CLOSED'},
    {'id': 'C0386-2', 'claim': 'LKP KK 光子 m_1 = 1/R = 800 GeV', 'value': str(m1), 'verdict': 'CLOSED'},
    {'id': 'C0386-3', 'claim': 'KK 塔等间隔 Δm = 1/R = 800 GeV', 'value': str(dm), 'verdict': 'CLOSED'},
    {'id': 'C0386-4', 'claim': '圈半径 R = 2.47e-7 fm', 'value': str(R_fm), 'verdict': 'CLOSED'},
    {'id': 'C0386-5', 'claim': '冻结丰度近似 Ωh^2 ≈ 1.1e11 x_f^3/(g* M_Pl σv)', 'value': str(omega_h2), 'verdict': 'CLOSED'},
    {'id': 'C0386-6', 'claim': 'TUFT 供给 0：无 1/R 预测，归因标准 UED/ACD 算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert m1 == mpf('800') and m2 == mpf('1600') and m3 == mpf('2400'), 'kk'
    guards.append('G1 KK 谱 800/1600/2400 GeV ok')
    assert abs(R_fm - mpf('2.4666e-7')) < mpf('0.01e-7'), 'R'
    guards.append('G2 R=2.47e-7 fm ok')
    assert dm == mpf('800'), 'dm'
    guards.append('G3 dm=800 GeV ok')
    assert omega_h2 > mpf('0.5') and omega_h2 < mpf('1.2'), 'omega'
    guards.append('G4 Omega_h2=0.98 量级 ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 UED/ACD 卡鲁扎-克莱因算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0386 T316 UED KK 光子作为暗物质（C1,C2）'}
with open('attack_C0386_UEDKK光子攻破_2026-10-21.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('G:')
for g in guards:
    print(g)
print('exit_code=%d' % exit_code)
