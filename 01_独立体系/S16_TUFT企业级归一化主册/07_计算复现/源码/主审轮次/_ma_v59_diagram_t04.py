# -*- coding: utf-8 -*-
"""_ma_v59_diagram_t04.py — 架构图追加 T04 节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t04-measurement-boundary">
<h3>★ T04 量子测量边界声明收口（2026-09-24，MainAgent .venv 复跑三线全部复现）</h3>
<div class="node">
<b>M1 确定结果=PARTIAL</b>：经典天然确定严格成立（无叠加+Cauchy 唯一）；取消叠加≠解释坍缩；Born 反解 μ 手放（微调非推导，f(+) 误差 1e-16）<br>
<b>M2 玻恩规则=结构性不可导出[严格定理 S5]</b>：四条阻塞（实辛流形≠复 Hilbert、对角测度无相干、无 H_S⊗H_E 张量分解、确定性阻断随机映射）；rho_Q[0,1]=0.4869≠0 vs rho_C[0,1]=0；f0=P0 巧合标注为维度事故；边界公设 <b>M2-EXT</b>（泛波函数+幺正演化+玻恩）<br>
<b>M3 线性→非线性=PARTIAL（错型）</b>：Skyrme L4 为 Derrick 稳定项（R*=1.0、E2=E4=E*/2），正则量子化后退化为幺正顶点非坍缩项<br>
<b>破解矩阵 #9 转换</b>：未触及 → <b>结构封闭（不可约边界：M2-EXT+P-B1/P-B2/P-B3）</b>；不可约输入集 7→9；非伪闭合（O1-O4 开放）<br>
<i>脚本 tuft_t04_line{1,2,3}_*.py 已背书。量子测量=TUFT 结构性边界：经典场论可给确定结果（M1 字面），但玻恩概率与坍缩机制是定理级不可导出、须外挂量子基底。</i>
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
