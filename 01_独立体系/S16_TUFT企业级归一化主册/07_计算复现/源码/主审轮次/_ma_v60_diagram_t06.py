# -*- coding: utf-8 -*-
"""_ma_v60_diagram_t06.py — 架构图追加 T06 攻坚背书节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t06">
<h3>★ T06 攻坚 · N_R Hopf 身份 + QNM 门 B（2026-09-24，MainAgent 复跑背书）</h3>
<div class="node">
<b>线一 · N_R Hopf 身份</b>：γ=2/ρ_h=<b>3.279215613</b>（几何预言非拟合）｜锚 Q_R=1→M_R=<b>1.00e14 GeV</b>（Q=2: 6.33e12、Q=3: 3.23e11）｜Q 格点 top/electron/nu=<b>10/14/19</b>｜格点 span=3.8635e5 vs 观测 3.3808e5（rel=14.3%）→ 过覆盖 G_res 达 <b>114.3x</b>（条件定理·FIT，非严格）｜K_N=<b>23.36</b>>1 洗掉→需共振轻子生成<br>
<b>线二 · QNM 门 B</b>：GR n=0 |err|=1.59e-15（14.8 位）｜GR splitR/a=<b>0.25153232</b>（7.7 位 PASS）｜<b>TUFT n=0 基模门 B PASS</b>（N 互合 8.359e-10 ≤1e-9，8.3 位）｜TUFT n=1,2 泛音 <b>OPEN</b>（2.940e-05>1e-9）｜O(a) 嵌入 vs 完整 Leaver 差异 ~O(a²)（6.1e-3/6.1e-3/1.3e-2）<br>
<b>四态</b>：严格=seesaw 代数/N_R 零反常/E142 否决仍立/GR 14.8 位/O(a²) 定量；条件=Q_N=1 锚定/I3 格点桥接(TUFT n=0 门 B)；定义=Q_N 最低 Hopf sector/O(a) 一阶微扰；开放=Q_N 唯一性/整数指派精度/K_N/I6/I7/泛音谱<br>
<i>E1–E498 冻结不变（T06 待分配 E 号）；v50 作废值未复活；无伪闭合。台账 main_agent_v60_t06_rerun。</i>
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
print('diagram t06 section added; total chars:', len(t2))
