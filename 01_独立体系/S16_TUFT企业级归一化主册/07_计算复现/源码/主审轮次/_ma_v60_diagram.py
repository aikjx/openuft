# -*- coding: utf-8 -*-
import io
p='TUFT_企业级归一化全维架构图_E1-E336.html'
s=io.open(p,encoding='utf-8-sig').read()
old='''<tr><td style="border:1px solid #30363d;padding:6px">v5.7 (E497)</td><td style="border:1px solid #30363d;padding:6px">A4 SNR 精算（真实 PSD loudness、D_max 表）</td><td style="border:1px solid #30363d;padding:6px">无（台账 v47 键亦缺失）</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · 台账版本头已并发改 v5.7 但 v47 键缺失</td></tr>'''
new='''<tr><td style="border:1px solid #30363d;padding:6px">v5.7 (E497)</td><td style="border:1px solid #30363d;padding:6px">A4 SNR 精算（真实 PSD loudness、D_max 表）</td><td style="border:1px solid #30363d;padding:6px">无（台账 v47 键亦缺失）</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · 台账版本头已并发改 v5.7 但 v47 键缺失</td></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.8 (E498)</td><td style="border:1px solid #30363d;padding:6px">v48 旋转 QNM Beyn 扩展：GR 门 A PASS（12 位）/门 B FAIL、TUFT 旋转极点 UNTRUSTED</td><td style="border:1px solid #30363d;padding:6px"><b>有（脚本+out 真实落盘）</b></td><td style="border:1px solid #30363d;padding:6px"><b>MainAgent .venv 复跑逐位复现 · 诚实 FAIL 采纳 · TUFT 频裂 OPEN · 反驳 v44 无证声称</b></td></tr>'''
assert old in s
s=s.replace(old,new,1)
io.open(p,'w',encoding='utf-8').write(s)
print('diagram v48 row added, sections', s.count('<section'), s.count('</section>'))
