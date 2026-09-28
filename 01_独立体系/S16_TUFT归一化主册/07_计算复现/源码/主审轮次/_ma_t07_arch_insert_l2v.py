# -*- coding: utf-8 -*-
"""MainAgent: insert line2 OPEN-verdict note into architecture HTML (append-only style)."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t07l2v')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t07-line2-open-verdict" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7fbf7;">
<h3 style="margin:0 0 8px 0;">T07 线二 OPEN 判定·组织者裁决确认（2026-09-26）</h3>
<div style="font-size:14px;line-height:1.65;">
裁决：<b>线二 OPEN 判定已足够作为证据</b>（定性结论不依赖 N=360 精确值；已复现段[1][2] + n=1 N180/240 漂移足以支撑；N>=300 只影响漂移尺度精度；OOM 为本机环境限制非方法缺陷）<br>
MainAgent 接受：<b>Gate B n=1,2 = OPEN-CONFIRMED</b>（作为证据）；完整数值背书延期待低内存策略复跑补充（N<=240 分阶段 / validated Frobenius peel）。无伪闭合。<br>
<b>T07 四线终态</b>：线一 ENDORSED / 线三 ENDORSED / 线四 ENDORSED / 线二 OPEN-CONFIRMED（定量背书延期）<br>
<i>台账 main_agent_v60_t07_line2_open_verdict。E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
