# -*- coding: utf-8 -*-
"""_ma_v59_diagram_t02.py — 架构图追加 T02 节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t02-yukawa-generations">
<h3>★ T02 汤川跨度 + 三代拓扑联合攻坚（2026-09-24，MainAgent .venv 复跑三线全部复现）</h3>
<div class="node">
<b>线一（E145 几何上界精确化）</b>：G=α·Q·τ；基态扫描 G∈[2,60]=10^1.78；缺口 Y_span/G_max=5.69e3=10^3.755。<b>纯几何原理性差 ~10^3.5 阶</b>（量级稳健；"严格定理"标签降为条件定理）<br>
<b>线二（seesaw×FN 桥接）</b>：seesaw light≈0.6 eV 复现；FN 最佳 dQ=6（ε_req=0.2579 vs β−1=0.2638，rel=0.023）——<b>口径纠正：用线一实测 G_max=60 时 rel 变 0.115，弱巧合不作证据</b>；算术桥接闭合、内部来源封锁（E479+N_R 开放）<br>
<b>线三（G3 三代不可约输入公设）</b>：每代反常消消（SU3 0/SU2 0/U1³ 1.9e-16/grav 0）→ 反常不选 N_g；Weyl 45；<b>不可约输入集=5</b>（α⁻¹、m_Pl/m_e、y_t/y_e、N_g、θ_QCD）+量纲 G；公设诚实不伪闭合<br>
<b>T02 裁决</b>：三代起源正式定性收口为<b>不可约输入 G3</b>（破解矩阵 #2 结构封闭）；汤川跨度保持部分覆盖（算术闭、来源开）<br>
<i>脚本 tuft_t02_line{1,2,3}_*.py 已背书。E145 强化：10² 上限→扫描 G_max=60+Derrick 保护的原理性缺口。</i>
</div>
</section>
'''

old_footer = '''</footer>
</body>
</html>'''
assert old_footer in t, 'footer anchor not found'
t2 = t.replace(old_footer, section + '\n' + old_footer, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('diagram updated; total chars:', len(t2))
