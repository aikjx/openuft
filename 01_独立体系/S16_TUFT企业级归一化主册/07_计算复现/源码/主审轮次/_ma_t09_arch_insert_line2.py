# -*- coding: utf-8 -*-
"""MainAgent: insert T09 line2 + anchor-bias section into architecture HTML."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t09l2')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t09-line2-audit" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7fbf7;">
<h3 style="margin:0 0 8px 0;">T09 线二 · 低内存 N≥300-480 Beyn + SVD de-clustering MainAgent 审计（2026-09-27）</h3>
<div style="font-size:14px;line-height:1.65;">
<b>复现证据</b>：n=0 三点本机逐位一致（3.885/4.720/4.808e-9）；本机完整 N=300 复跑被外部终止（exit -1，系统健康）；<b>官方内部交叉验证：T09 N=300 vs T07 = 5.422e-10、N=360 vs T07 = 1.906e-09</b>（独立运行、nc 阶梯不同）<br>
<b>关键数值</b>：n=1 N=300 0.569957939619−0.287655030300i、N=360 0.569974871843−0.287680404348i（pole-switch 3.05e-05 跨管线确认）；n=2 跨 N 漂移 ~2.5e-2 未定位（N=480 有效秩 1→2，次模刚冒头 4.5e-6）；<b>N=480 干净运行无 OOM——瓶颈非 RAM，是孤立极 Beyn vs 非孤立双根/泄漏对</b><br>
<b>Gate B n=1,2 维持 OPEN</b>（n=1 best 2.71e-6、n=2 未定位 ≫ 1e-9）；剩余路径：外向 WKB/Leaver 打靶（泛音相位起点）或 n=0 先验证到 1e-9 的 peel<br>
<b>锚点偏置（T09 最大发现）</b>：旧 psi 笔 0.434445176377−0.056449764526i vs 新 F 笔 0.434445176903−0.056449764800i 互合 ~6e-10；冻结锚点偏离 ~4.9e-9（实 1.1e-9/虚 4.8e-9）= 旧 peel 平台偏置 → <b>锚点升级候选 0.4344451769−0.0564497648i</b>，Gate A 新锚重判后可推进泛音<br>
<i>台账 main_agent_v60_t09_line2_rerun；E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
