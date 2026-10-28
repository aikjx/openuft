# -*- coding: utf-8 -*-
# C0389 T335 L_μ−L_τ 规范玻色子与缪子 g−2：反常相消+Δa_μ 闭式（mpmath 250 位）
from mpmath import mp, mpf, pi, power, log, quad
mp.dps = 250
import json

# U(1)_{Lμ−Lτ} 荷：μ/ν_μ=+1、τ/ν_τ=−1、e/ν_e=0
# 反常相消（逐代）：A = Σ_f Q_f³；重力反常 B = Σ_f Q_f
Qs = [mpf('1'), mpf('-1'), mpf('0')]
A = sum(q ** 3 for q in Qs)
B = sum(Qs)
print('A=ΣQ³=%.6f  B=ΣQ=%.6f' % (A, B))

# Δa_μ^(Z')：矢量耦合闭式积分
# Δa_μ = (g'²/4π²)∫₀¹ dx x²(1−x)/(x² + (1−x)·(m_Z'/m_μ)²)
gprime = mpf('4e-4')                          # KLOE-2 尺度约束
m_mu = mpf('105.6583755e-3')                  # GeV
m_Zp = mpf('0.2')                             # GeV
t = (m_Zp / m_mu) ** 2

def integrand(x):
    return x * x * (1 - x) / (x * x + (1 - x) * t)

I = quad(integrand, [0, 1])
d_a_mu = (gprime * gprime / (4 * pi * pi)) * I
print('t=%.6f  I=%.10e  Δa_μ=%.10e' % (t, I, d_a_mu))

# 大质量极限闭式核对：Δa_μ ≈ g'²m_μ²/(12π²m_Z'²)（leading，m_Z'≫m_μ 时 I≈m_μ²/(6m_Z'²)）
I_lead = 1 / (6 * t)
d_lead = (gprime * gprime / (4 * pi * pi)) * I_lead
print('leading I=%.10e  Δa_μ_lead=%.10e' % (I_lead, d_lead))

# 实验偏离（Fermilab/BNL 联合）：Δa_μ_exp = 2.49e-9
exp = mpf('2.49e-9')
print('实验 Δa_μ=%.6e  比值=%s' % (exp, mp.nstr(d_a_mu / exp, 5)))

entries = [
    {'id': 'C0389-1', 'claim': '反常相消 ΣQ³=0（μ:+1, τ:−1, e:0 逐代精确）', 'value': str(A), 'verdict': 'CLOSED'},
    {'id': 'C0389-2', 'claim': '重力反常 ΣQ=0', 'value': str(B), 'verdict': 'CLOSED'},
    {'id': 'C0389-3', 'claim': 'Δa_μ^(Z\') 闭式积分（g\'=4e-4, m_Z\'=0.2 GeV）', 'value': str(d_a_mu), 'verdict': 'CLOSED'},
    {'id': 'C0389-4', 'claim': 'leading 极限 Δa_μ≈g\'²m_μ²/(12π²m_Z\'²)', 'value': str(d_lead), 'verdict': 'CLOSED'},
    {'id': 'C0389-5', 'claim': 'TUFT 供给 0：无 g\'/m_Z\' 预测，归因标准 U(1) 反常算术', 'value': '0', 'verdict': 'TUFT=0'},
]

guards = []
try:
    assert A == 0 and B == 0, 'anom'
    guards.append('G1 反常相消 ΣQ³=ΣQ=0 精确 ok')
    assert abs(d_a_mu - mpf('1.974e-10')) < mpf('0.5e-10'), 'dmu'
    guards.append('G2 Δa_μ=1.97e-10 量级 ok')
    assert d_a_mu > d_lead, 'lead'
    guards.append('G3 精确积分>leading 近似（t=3.58 有限） ok')
    assert d_a_mu / exp > mpf('0.05') and d_a_mu / exp < mpf('0.5'), 'ratio'
    guards.append('G4 比值 0.079 部分偏离解释 ok')
    exit_code = 0
except AssertionError as e:
    guards.append('FAIL ' + str(e))
    exit_code = 1

red_line = ('0/22 保持；UFT-3=0 保持；不宣称实现统一场论；'
            '攻破=对 TUFT/几何框架结构性负面闭合（数学自洽≠实验证实；'
            '归因写「标准 U(1)_{Lμ−Lτ} 反常/圈算术，未写成 TUFT 预测」）')
out = {'entries': entries, 'guards': guards, 'exit_code': exit_code,
       'red_line': red_line, 'precision': 250,
       'claim': 'C0389 T335 L_μ−L_τ 规范玻色子与缪子 g−2（C1,C2）'}
with open('attack_C0389_LμLτ规范玻色子攻破_2026-10-21.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('G:')
for gx in guards:
    print(gx)
print('exit_code=%d' % exit_code)
