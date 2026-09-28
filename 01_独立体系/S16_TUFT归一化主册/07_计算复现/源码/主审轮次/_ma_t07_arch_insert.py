# -*- coding: utf-8 -*-
"""MainAgent: insert T07 lines13 audit section into architecture HTML (append-only style)."""
import io, shutil, os

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t07l13')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t07-lines13-audit" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#fbfbf9;">
<h3 style="margin:0 0 8px 0;">T07 线一/线三 MainAgent 独立审计背书 + 线二部分审计（2026-09-26）</h3>
<div style="font-size:14px;line-height:1.65;">
<b>线一 · Q_N 唯一性锁定（ENDORSED）</b>：复跑逐位一致（差 [written] 尾行）。Q_N=1 <b>唯一存活</b>（M_R=1.00e14 GeV，GUT 窗下缘，热地板 323.26x PASS）；Q_N=2（6.33e12，低 15.8x）与 Q_N=3（3.23e11，低 309x + 热地板 0.67x MARG）EXCLUDE；K_N=[5.38,31.31] 洗掉；<b>I3 桥 CONDITIONAL</b>（14.3% 残差，GUT 窗=唯象输入，中间 seesaw 下 Q1,Q2 皆存活 OPEN）；mu→eγ 9.62e-31 与 |m_bb|=[0.0033,0.0084] eV 均不区分 Q_N<br>
<b>线三 · 微观-宏观联合（ENDORSED）</b>：复跑字节一致。残差 RMS=0.353 dex（OOM 拟合）；Q_b=11 m_s=3.4641 GeV n_s≈0.365 m⁻³；a0_TUFT=1.0468e-10（H0=67.7）；BTFR +1.90σ；mu0=2.175030e-04；Λ_n/m_n=0.5385；<b>mu0↔a0 DECOUPLED（D30 OPEN）</b>；P11 α_s=1 vs Skyrme √2 张力复现（E483/E484 未闭合）；新标签 D28/D29/D30<br>
<b>线二 · 泛音谱（PARTIAL-AUDIT，完整背书延期）</b>：本机三次复跑失败（文件锁 / N>240 OOM exit -1 / 系统卡死）。已逐位复现：[1] Leaver 参考值、[2] <b>WKB Gaussian peel 构建→测试→拒绝</b>（n=0 错位 1e-3，改用 plain s^β）、[3] n=1 N=180/240；未复现 N>=300 及 n=2（本机内存不足）。<b>维持官方 OPEN</b>：n=1 drift 2.7e-6→3.0e-5（pole-switch）、n=2 1e-2..4e-2；Gate B n=1,2=OPEN；无伪闭合。完整背书待低内存策略（N<=240 分阶段 / validated Frobenius peel）<br>
<i>E1–E498 冻结不变。台账 main_agent_v60_t07_line{1,3}_rerun + line2_rerun_partial。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
