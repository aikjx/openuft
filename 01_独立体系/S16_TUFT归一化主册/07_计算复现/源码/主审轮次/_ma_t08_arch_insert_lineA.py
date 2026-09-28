# -*- coding: utf-8 -*-
"""MainAgent: insert T08 lineA audit section into architecture HTML."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t08la')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t08-lineA-audit" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7fbf7;">
<h3 style="margin:0 0 8px 0;">T08 线 A · 泛音定量闭合 MainAgent 审计复跑（2026-09-27）</h3>
<div style="font-size:14px;line-height:1.65;">
<b>7/7 数值点逐位一致（|dw| &lt; 3.4e-13）</b>：审计变体 import 官方模块函数逐字复用，本机 .venv 最小集（n=0 三点 + n=1/2 N=180/240），wall 477.8s<br>
n=0：err 3.885e-09/4.720e-09/4.808e-09（管线复现）｜n=1：N=180 0.569959376313−0.287683421561i、N=240 0.569958559840−0.287657668455i（逐位一致）｜n=2：N=180 0.499906955875−0.406567819775i、N=240 0.496288359607−0.396115697374i（逐位一致）<br>
<b>UNREACHABLE 确认为数值事实</b>：n=1 单调分支 drift 9.6e-06..1.8e-05 ≫ 1e-9（N=300→360 pole-switch 3.0e-5 需 N≥300，OOM 历史）；n=2 未定位 1.7e-02（需 N≥480+SVD）；WKB peel 已拒；<b>Gate B n=1,2 维持 OPEN</b>，定量 1e-9 背书本机 N≤240 不可达。四态：A 严格/B 条件（n=0 gate PASS 复现）/C 定义/D 开放。无伪闭合。<br>
<i>台账 main_agent_v60_t08_lineA_rerun。E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
