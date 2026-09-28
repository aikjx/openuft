# -*- coding: utf-8 -*-
"""_ma_v60_diagram_t07l4.py — 架构图追加 T07 线四背书节"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="t07-line4">
<h3>★ T07 线四 · 涡旋光-螺旋世界线粒子耦合动力学（2026-09-25，MainAgent 复跑背书）</h3>
<div class="node">
<b>4 力口径裁定</b>：u_ν∂_μT^{μν}=0（反对称×对称，静止系功率，严格）→ 空间 4 力 = h 投影 = qF^{μν}u_ν；演化方程三通道：Lorentz（严格）+ 自旋-挠率 S^{μν}∂_ν(τ̂)（TUFT 公设，OPEN）+ OAM 传递 l·(σ_abs/ω_L)·束流（OPEN）；E18 γv=c 锁定螺旋（严格）<br>
<b>非傍轴 LG</b>：Lax E_z^(1)=−(i/k_L)div_⊥E_⊥；R_old~1/(k_Lw₀)（常数 1.4142，严格）｜<b>失效阈值 w₀/λ≈2.25</b>；≥5 傍轴可用（<4.5%）<br>
<b>共振相空间</b>：<b>l·w_s=k_L(γ−sinθ)</b>，sinθ=τ/w_s（Lorentz Doppler，严格）；l=1..6 峰值扫描复现；共振壳半宽~Γ/l；共振=轴向 OAM 力峰；Floquet 稳定性 OPEN<br>
<b>对照仿真</b>：主册无 §13（grep 确认）、§16 仅锚 → 按规则新结构（§13=傍轴紧聚焦失效、§16 讨论）｜旧 w₀/λ=0.5：R_old=<b>0.4501</b>（45% 散度）+缺 E_z→f³ O(1) 误估；新 R_new=<b>0.1433</b>（<b>3.1×</b> 压散度）；f·u=0 两方案皆成立（非失效通道，诚实）<br>
<b>新标签</b>：D31（4 力 caliber）｜D32（阈值 2.25）｜D33（共振轨迹）｜D34（新旧对照）<br>
<i>E1–E498 冻结不变；无伪闭合。台账 main_agent_v60_t07_line4_rerun。</i>
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
print('diagram t07-line4 section added; total chars:', len(t2))
