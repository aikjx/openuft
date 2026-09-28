# -*- coding: utf-8 -*-
"""MainAgent: insert T10 three-line section into architecture HTML."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t10')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t10-lines123-audit" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7fbf7;">
<h3 style="margin:0 0 8px 0;">T10 三线 · 锚点升级 + 泛音 peel + WKB/Leaver 打靶 MainAgent 审计（2026-09-27）</h3>
<div style="font-size:14px;line-height:1.65;">
<b>本机复跑</b>：线一 N=180 |dw|=4.3e-13、线二 N=300 |dw|=9.6e-14、线三 n=0 |dw|=2.6e-13 —— 三线数值全部逐位复现<br>
<b>线一 · 新锚正式冻结</b>：w_TUFT(n=0)=<b>0.434445176207−0.056449764436i</b>（置信半径 2.178e-10；外推代数手算复核闭合）；Gate A 新锚重判 (i) 互合 4.419e-10 (ii) |w−新锚| 7.849e-10 → <b>PASS</b>；旧锚偏置 4.785e-9 揭示（旧值 = 旧 psi 平台）<br>
<b>线二 · 泛音</b>：Gate A PASS（|err|=3.292e-12）；n=1 单管线几何收敛 ic=3.18e-9 但 <b>跨管线不一致 ~1.6e-2</b>（T10 frob 0.5699569−0.2876712i vs T09 0.5699579−0.2876550i，两候选并存未定位）；n=2 SVD 各 N rank=1 但漂移无稳定链 → <b>NOT LOCALIZED</b>；Gate B n=1,2 维持 OPEN<br>
<b>线三 · WKB/Leaver 打靶</b>：方法推导正确（tortoise Schrödinger、正则支、纯出射 BC、外向稳定方向）；但 n=0 根 Im&gt;0（增长模，|vs 锚|=9.8e-2），n=1/2 发散——<b>实轮廓 IVP vs 复轮廓谱极点是 Stokes 线结构性失配</b>，修复需复 ρ 积分（超双精度范围）<br>
<i>台账 main_agent_v60_t10_line1/2/3_rerun；latest_round=v6.0_T10_anchor_upgraded_gateB_open_stokes_line；E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
