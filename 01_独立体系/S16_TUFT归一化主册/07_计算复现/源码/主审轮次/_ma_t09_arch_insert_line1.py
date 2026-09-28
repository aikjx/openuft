# -*- coding: utf-8 -*-
"""MainAgent: insert T09 line1 Gate-A-FAIL section into architecture HTML."""
import io, shutil

p = 'TUFT_企业级归一化全维架构图_E1-E336.html'
shutil.copy(p, 'TUFT_企业级归一化全维架构图_E1-E336.html.bak_t09l1')
t = io.open(p, encoding='utf-8').read()

anchor = '</footer>\n</body>\n</html>'
sec = '''
<section id="t09-line1-gateA-fail" style="border:1px solid #999;border-radius:10px;padding:14px 18px;margin:18px 0;background:#f7f7fb;">
<h3 style="margin:0 0 8px 0;">T09 线一 · validated 高阶 Frobenius peel（2026-09-27）— Gate A FAIL，瓶颈精确定位</h3>
<div style="font-size:14px;line-height:1.65;">
<b>推导验算闭合</b>：psi=s^{−β}F 离心项精确抵消、jw 交叉项抵消 → F''+2jwF'−VF=0；f1=3j/w、f2=−3/w²−15j/(2w)；端点 Robin 比 −3j/(2wb) 自洽；收敛论证（psi~(1−z)^{1.2638} 代数收敛 = T08 平台理论根源；F 解析 → 几何）<br>
<b>Gate A 实测</b>：F-pencil err N=60 1.421e-07 → 90 4.191e-08 → 120 1.830e-08 → 180 7.339e-09 → 240 5.475e-09；best interconsistency 2.882e-09、best anchor 5.475e-09 &gt; 1e-9 → <b>FAIL → STOP、Gate B n=1,2 维持 OPEN、无伪闭合</b><br>
<b>瓶颈定位（预判修正）</b>：F-pencil <b>几何收敛</b>（视界端弱奇异未成主导），但 N=180→240 骤降 1.34× 撞 <b>~5e-9 数值噪声地板</b>（与 psi 平台同一地板）→ 瓶颈是 <b>rho ODE rtol=1e-13 + Beyn 噪声</b>，非 peel 解析化程度。修复优先级：ODE 提精度（rtol=1e-14/atol=1e-17）+ nc 增密<br>
<i>台账 main_agent_v60_t09_line1_rerun；诊断 TUFT_T09_中间诊断_线一Fpeel收敛异常_2026-09-27.md；E1–E498 冻结不变。</i>
</div>
</section>
'''
assert anchor in t, 'anchor not found'
t = t.replace(anchor, sec + '\n' + anchor)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('inserted; new len', len(t))
