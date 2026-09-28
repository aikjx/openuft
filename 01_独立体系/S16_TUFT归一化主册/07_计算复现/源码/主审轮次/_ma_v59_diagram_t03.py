# -*- coding: utf-8 -*-
"""_ma_v59_diagram_t03.py — 架构图追加 T03 节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t03-baryogenesis">
<h3>★ T03 重子生成三条件定理级审计（2026-09-24，MainAgent .venv 复跑三线全部复现）</h3>
<div class="node">
<b>线一（B 破坏）</b>：E329 为 T=0 微扰定理，不覆盖高温；sphaleron 窗口 160 GeV<T<6.84e8 GeV、E_sph(0)=7.36 TeV、需 Y_{B−L}(in)=2.455e-10；<b>Q=B 或 B−L 身份未登记（定义级缺口）</b>；B 破坏取决于 P_T 公设<br>
<b>线二（CP 破坏）</b>：J=3.1503e-5；无味同时满足非平衡+CKM 相位；缺口 <b>10^9.94</b>；TUFT 内部全实无复相位 → <b>CP 内部不可用</b>，需 η_new~O(0.1)<br>
<b>线三（非平衡）</b>：四条严格定理封死 EW 出口（细致平衡/de Sitter 稀释 1.49e78/K>>1/E273 静态壁）；高 T 非平衡窗口 T>1.58e14 GeV 但 TUFT 无 T_rh 预言；V(n,T) 缺失 → <b>Sakharov-3 不满足</b>，NE 公设<br>
<b>破解矩阵 #5 转换</b>：未触及 → <b>结构封闭（不可约输入：P_T+η_new+NE）</b>；不可约输入集 5→7；非伪闭合（O1-O4 开放）<br>
<i>脚本 tuft_t03_line{1,2,3}_*.py 已背书。重子生成三条件缺二定理级确认：B 破坏依赖公设、CP 破坏内部不可用（10^9.94 缺口）、非平衡 V(n,T) 缺失。</i>
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
