# -*- coding: utf-8 -*-
# C0391 T340 四夸克态 X(6900) 双粲隐形态（mpmath 250 位）
from mpmath import mp, mpf, sqrt
mp.dps = 250
import json

m_Jpsi = mpf('3096.900')                     # MeV
m_X = mpf('6900')                            # MeV（LHCb J/ψJ/ψ 共振）
thr_2J = 2 * m_Jpsi
delta = m_X - thr_2J
Gamma_X = mpf('122')                         # MeV（LHCb 宽度）
tau = mpf('6.582119569e-22') / Gamma_X       # s
print('2J/ψ 阈值=%.4f MeV  X(6900) 偏移 Δ=%.4f MeV' % (thr_2J, delta))
print('Γ=%.1f MeV  τ=%.4e s' % (Gamma_X, tau))

# 紧四夸克（diquark-antidiquark）闭式：M ≈ 2m_c + E_dd；色-自旋分裂
# 双粲 diquark 质量估计：m_cc = 2m_c + 绑定（m_c=1270 质壳）；紧四夸克 vs 分子态判据
m_c = mpf('1270')                            # 粲夸克 MSbar 质量（MeV）
m_dd = 2 * m_c - mpf('50')                   # cc diquark 绑定（MeV 量级）
m_X_pred = 2 * m_dd + mpf('60')              # 双 diquark + 色-自旋（粗）
print('cc diquark=%.0f MeV  X 预测=%.0f MeV（粗估）' % (m_dd, m_X_pred))

# 判据：Δ/M 相对宽度——分子态要求 ΔE 小（vs T_cc 0.39 MeV）；X(6900) Δ=706 MeV ≫ Γ=122 MeV
# 判定：紧四夸克主导（非近阈值分子态）
ratio = delta / Gamma_X
print('Δ/Γ=%.4f（>1 ⟹ 紧四夸克）' % ratio)

entries = [
    {'id': 'C0391-1', 'claim': '2J/ψ 阈值 = 6193.8 MeV', 'value': str(thr_2J), 'verdict': 'CLOSED'},
    {'id': 'C0391-2', 'claim': 'X(6900) 相对阈值偏移 Δ = 706.2 MeV', 'value': str(delta), 'verdict': 'CLOSED'},
    {'id': 'C0391-3', 'claim': 'Δ/Γ = 5.79 ⟹ 紧四夸克主导（非浅分子态）', 'value': str(ratio), 'verdict': 'CLOSED'},
    {'id': 'C0391-4', 'claim': '寿命 τ=ℏ/Γ = 5.4e-24 s', 'value': str(tau), 'verdict': 'CLOSED'},
    {'id': 'C0391-5', 'claim': 'TUFT 供给 0：无 X(6900) 质量预测，归因标准色-自旋/四夸克算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert abs(thr_2J - mpf('6193.8')) < mpf('0.1'), 'thr'
    guards.append('G1 阈值=6193.8 MeV ok')
    assert delta > mpf('700') and delta < mpf('715'), 'delta'
    guards.append('G2 Δ=706.2 MeV ok')
    assert ratio > mpf('5') and ratio < mpf('6'), 'ratio'
    guards.append('G3 Δ/Γ=5.79 ok')
    assert tau > mpf('5e-24') and tau < mpf('6e-24'), 'tau'
    guards.append('G4 τ=5.4e-24 s ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 QCD 色-自旋/四夸克算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0391 T340 四夸克态 X(6900) 双粲隐形态（C1,C5）'}
with open('attack_C0391_X6900四夸克攻破_2026-10-21.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('G:')
for gx in guards:
    print(gx)
print('exit_code=%d' % exit_code)
