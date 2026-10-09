# -*- coding: utf-8 -*-
# 第9层：P3路线 —— 胀子物理与等效原理精密检验
import math

print('='*74)
print('第9层 P3：胀子物理与等效原理精密检验（定量）')
print('='*74)

print()
print('【1】问题：KK/额外维必然产生胀子(模场)，破坏等效原理')
print('-'*74)
print('  KK紧致化的模场(radion/dilaton φ)是额外维尺度的标度场')
print('  若φ无质量且以引力强度耦合物质 -> 破坏弱等效原理(WEP)')
print('  WEP破坏参数: η = (a1-a2)/((a1+a2)/2) ~ 2α_d²·Δ(q/m)')
print('  其中 α_d = 胀子-物质耦合(相对引力), Δ(q/m)=材料电荷差')

print()
print('【2】MICROSCOPE卫星对胀子耦合的约束')
print('-'*74)
eta_MICROSCOPE = 1.2e-14  # Ti/Pt 实测上限
alpha_d = math.sqrt(eta_MICROSCOPE/2)  # 若 Δ(q/m)~1
print(f'  MICROSCOPE实测 η < {eta_MICROSCOPE:.1e} (Ti/Pt, 2017-2022)')
print(f'  => 胀子-物质耦合 α_d < √(η/2) = {alpha_d:.2e} (相对引力)')
print(f'  => 任何引力强度标量场(胀子)耦合被约束到 <1e-7 相对引力')
print(f'  => 无质量胀子与实验矛盾，必须被质量化/屏蔽')

print()
print('【3】Eöt-Wash扭秤对Yukawa型第五力的约束')
print('-'*74)
print('  V(r) = -(Gm1m2/r)(1 + α·e^(-r/λ))   [α=耦合强度, λ=力程]')
bounds = [
    (1e-5, 1e-2, '10 µm-1 cm 短程'),
    (1e-3, 1e-9, '1 mm 中等程'),
    (1e-2, 1e-12, '1 cm 中长程'),
]
for lam, alpha_max, name in bounds:
    print(f'  λ={lam*1e3:.3g} mm: α < {alpha_max:.0e}  [{name}]')
print('  => 额外维度/胀子若产生Yukawa力，短程扭秤给出最严格约束')

print()
print('【4】胀子质量化(屏蔽)机制：需要多重的胀子？')
print('-'*74)
hbar = 1.054571817e-34
c = 2.99792458e8
# 若力程 < λ_c, 则屏蔽。Eöt-Wash敏感范围 ~30µm 起
lam_min = 30e-6
m_dilaton = hbar/(lam_min*c)
m_dilaton_eV = m_dilaton*c**2/1.602176634e-19
print(f'  若要求胀子力程 < 30 µm (扭秤敏感下限):')
print(f'  胀子质量 m_φ > ℏ/(λc) = {m_dilaton_eV:.2e} eV = 6.6 meV')
print(f'  => 只需 m_φ > 6.6 meV (约电子质量的 {m_dilaton_eV/5.11e5:.1e} 倍)')
print(f'     即可把胀子力程压到扭秤盲区以下')

print()
print('【5】结论：P3路线的实验边界')
print('-'*74)
print('  · MICROSCOPE: α_d < 1e-7 相对引力(无质量胀子已排除)')
print('  · Eöt-Wash: Yukawa第五力 α < 1e-9~1e-12 (依力程)')
print('  · 胀子若存在: 必须 m_φ > ~6.6 meV (被扭秤屏蔽) 或极弱耦合')
print('  · 未来: 下一代扭秤/原子干涉可再提升1-2个量级')
print('  => 胀子方向可检验性明确, 但需精密实验持续收紧')
