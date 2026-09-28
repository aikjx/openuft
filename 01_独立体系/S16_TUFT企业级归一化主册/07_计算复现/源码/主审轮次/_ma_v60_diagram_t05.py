# -*- coding: utf-8 -*-
"""_ma_v60_diagram_t05.py — 架构图追加 v6.0 终版冻结节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t05-v60-freeze">
<h3>★ v6.0 终版冻结 · T05 收官总盘点（2026-09-24，MainAgent 复跑背书）</h3>
<div class="node">
<b>破解矩阵终态（冻结）</b>：完全闭合 <b>0</b>（禁止凑数）｜结构封闭(输入层) <b>3</b>（#2 G3 / #5 P_T+η_new+NE / #9 M2-EXT）｜条件性闭合 <b>1</b>（#13 P17）｜部分覆盖 <b>10</b>｜未触及 <b>0</b><br>
<b>不可约输入集 9 项（权威登记）</b>：I1 α⁻¹=137.036(P9)｜I2 m_Pl/m_e(P6)｜I3 y_t/y_e（G_res~3.38e3，E479 封锁）｜I4 N_g=3(G3)｜I5 θ_QCD≈0｜I6 η_new｜I7 NE(V(n,T))｜I8 M2-EXT｜I9 Q=B−L(E329)；+量纲 G；P18 最小性降级、P19 不入集<br>
<b>E329 Q=B−L 登记（定义识别）</b>：SM 约化下 sphaleron 守恒 B−L、与 τ_p=∞ 共存（条件定理）；Q=B 备选须 P_T 冻结 N_CS（未选，开放）<br>
<b>开放项冻结</b>：O-M1..M4 测量逃逸口｜N_R Hopf 身份｜c_m 区间[−0.369,−0.218]/点值 OPEN｜QNM 空腔谱（Grade A 0.434445178−0.056449760i，阻尼/泛音/门B OPEN）｜l_A CMB ~12%｜汤川 E479 BLOCKED｜Page/D25｜重子温窗<br>
<b>不变量</b>：勘误 #42 held｜四态 35/61/18/27 冻结｜D18 v31 不回退｜联盟层 2/6｜E1–E498 不变（本轮零新 E-number）<br>
<i>TUFT v6.0 终版冻结通过，归一化闭环正式收口。脚本 tuft_t05_finalize_v6.py 已背书；主册 §21 + freeze 标记；台账 main_agent_v59_t05_finalize + main_agent_v60_t05_rerun。</i>
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
