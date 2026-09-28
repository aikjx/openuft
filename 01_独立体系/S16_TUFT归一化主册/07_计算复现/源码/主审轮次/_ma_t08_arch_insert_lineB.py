# -*- coding: utf-8 -*-
"""MainAgent: insert T08 lineB endorsement section into architecture HTML."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t08lb')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t08-lineB-endorsed" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7fbf7;">
<h3 style="margin:0 0 8px 0;">T08 线 B · QCD 弦张力与夸克禁闭 MainAgent 审计背书（2026-09-27）</h3>
<div style="font-size:14px;line-height:1.65;">
<b>ENDORSED</b>：Read 全文 → .venv 复跑 exit=0 → 脚本自写 out 与官方 <b>191/191 行逐行一致</b>（BOM/尾空行差异为 PowerShell 重定向人工产物，已排除）<br>
<b>关键数值</b>：σ_QCD=0.180 GeV² vs σ_fund=M_pl²=1.4906e38 GeV² → <b>gap=8.28e38（log₁₀=38.92）</b>；<b>Z(π₃(S²))≠Z₃(center SU(3)) 不同构 → 裸同伦映射不存在（A 级）</b>；gap=(M_pl/Λ_eff)² = RG 跑动距离 <b>44.8 e-folds</b>（B 级，层级非缺陷，强补偿即伪闭合）；Abel 投影+对偶 Meissner 条件桥（B 级）；L_break=<b>0.60 fm</b>（≈强子半径）<br>
<b>开放（D 级）</b>：同一 Lagrangian 双出、从 M_pl 预言 Λ_QCD（需完整 SU(3) β 函数+UV 边界）、Z↔Z₃ 严格映射、端点匹配<br>
<i>台账 main_agent_v60_t08_lineB_rerun。E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
