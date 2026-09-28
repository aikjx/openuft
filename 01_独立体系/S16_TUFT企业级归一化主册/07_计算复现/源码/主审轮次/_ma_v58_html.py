# -*- coding: utf-8 -*-
import io,os,time,shutil
p='TUFT_企业级归一化全维架构图_E1-E336.html'
ts=time.strftime('%Y%m%d_%H%M%S')
shutil.copy2(p, f'{p}.ma_v58pre_{ts}.bak')
s=io.open(p,encoding='utf-8-sig').read()
orig=len(s)
# 1) title
s=s.replace('<title>TUFT 全维架构图 v4.4 · E479 输入计数元定理＋开放分诊 P0/P1/P2/P3 · E1–E479</title>',
            '<title>TUFT 全维架构图 v5.7 · E497 慢转证据审计＋A6 2PN＋A4 SNR · E1–E497</title>')
# 2) h1 line (keep details history block untouched; replace only the version prefix through the closing </h1>)
old_h1='<h1>TUFT 企业级归一化全维架构图 · <span style="color:#7ee787;">v4.4</span>（当前权威口径：E1–E479 · 勘误 #41 · 四态 严格35/条件61/定义18/开放27 · E479 输入计数元定理＋开放分诊 · 2026-09-20）</h1>'
new_h1='<h1>TUFT 企业级归一化全维架构图 · <span style="color:#7ee787;">v5.7</span>（当前权威口径：E1–E497 · 勘误 #42 · 四态 严格35/条件61/定义18/开放27 · E492–E497 登记不进四态 · 2026-09-24）</h1>'
assert old_h1 in s, 'h1 not found'
s=s.replace(old_h1,new_h1)
# 3) sub line
old_sub='<div class="sub">本源拓扑统一场论｜Frenet–Serret + Călugăreanu–White｜算法联盟攻坚 + MainAgent 归一化与独立复核（唯一独立审计方）｜<b style="color:#7ee787;">当前 v4.4 · E1–E479 · 勘误 #41 · 2026-09-20</b>｜<b>本图为唯一权威口径（single source of truth；文件名沿用 E1-E336）</b></div>'
new_sub='<div class="sub">本源拓扑统一场论｜Frenet–Serret + Călugăreanu–White｜算法联盟攻坚 + MainAgent 归一化与独立复核（唯一独立审计方）｜<b style="color:#7ee787;">当前 v5.7 · E1–E497 · 勘误 #42 · 2026-09-24</b>｜<b>本图为唯一权威口径（single source of truth；文件名沿用 E1-E336）</b></div>'
assert old_sub in s, 'sub not found'
s=s.replace(old_sub,new_sub)
# 4) stats E-range
old_stats='<div class="stat"><div class="n" style="color:var(--novel)">E1–E462</div>'
new_stats='<div class="stat"><div class="n" style="color:var(--novel)">E1–E497</div>'
assert old_stats in s, 'stats not found'
s=s.replace(old_stats,new_stats)
# 5) insert v5.3-v5.7 evidence-audit section before <footer>
audit_section='''<section id="v53-v57-evidence-audit" style="box-sizing:border-box;width:100%;padding:18px 20px;border-top:3px solid #ff7b72;background:#161b22;color:#e6edf3;font-family:'Microsoft YaHei',Arial,sans-serif;">
<h2 style="font-size:16px;color:#ff7b72;margin:0 0 10px 0;">★★ v5.3–v5.7 证据审计（MainAgent，2026-09-24）——口头升版，无落盘证据，不背书</h2>
<div class="note bad" style="border-color:#ff7b72;color:#ff7b72"><b>磁盘实查（os.path.exists 逐一 False）</b>：organizer 声称引用的 <code>_audit_v43_slow_rotation(_out).py/.txt</code>、<code>_audit_v44_mirror_slowrot(_out).py/.txt</code>、<code>_audit_v45_multiseg_frobenius(_out).py/.txt</code>、<code>_audit_v46_2pn_coupling(_out).py/.txt</code> <b>全部不存在</b>。按铁律，E492–E497 的数值（GR 门 A/B PASS 12.6/7.2 位、TUFT m 频裂 0.09832、Hartle 外推 0.06288、A6 2PN 重解、v47 SNR 精算）<b>无脚本无输出、未经 MainAgent .venv 独立复跑，一律标 UNVERIFIED，不进 SSOT 权威</b>；TUFT m 频裂保持 <b>OPEN</b>。勘误 #42（门常数 0.25153，MainAgent 第三实现＋门常加固双确认）不受影响。架构图于 09-22 10:10 被批量写盘覆盖回退 v4.4 混合体（h1=E479/stats=E462/footer=v3.8 内部不一致），MainAgent 本轮重建至 v5.7/E497 一致；v5.2 十九节版与 _bak_rec_* 备份已丢失。</div>
<table style="border-collapse:collapse;width:100%;font-size:13px;margin-top:6px"><tr style="background:#0d1117"><th style="border:1px solid #30363d;padding:6px;text-align:left">轮次</th><th style="border:1px solid #30363d;padding:6px;text-align:left">声称</th><th style="border:1px solid #30363d;padding:6px;text-align:left">落盘证据</th><th style="border:1px solid #30363d;padding:6px;text-align:left">MainAgent 状态</th></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.3 (E492/E493)</td><td style="border:1px solid #30363d;padding:6px">异常根因表 11 条；慢转第二独立实现 GR 门 A/B PASS（12.6/7.2 位）</td><td style="border:1px solid #30363d;padding:6px">无</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · 门常数 0.25153 本身由 #42 独立背书</td></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.4 (E494)</td><td style="border:1px solid #30363d;padding:6px">TUFT 镜壁 m 频裂 0.09832、Hartle 0.06288、dQ/da≈+0.11973</td><td style="border:1px solid #30363d;padding:6px">无</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · 频裂 OPEN</td></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.5 (E495)</td><td style="border:1px solid #30363d;padding:6px">A9 多段 Frobenius GR 门 FAIL（0.6 位）</td><td style="border:1px solid #30363d;padding:6px">无</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED（方向与历史死路一致，可参考）</td></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.6 (E496)</td><td style="border:1px solid #30363d;padding:6px">A6 U_ph×2PN：GR 极限 10.6 位 PASS、c_m 调制 −0.2116 μas NEGATIVE</td><td style="border:1px solid #30363d;padding:6px">无</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · A6 维持 OPEN</td></tr>
<tr><td style="border:1px solid #30363d;padding:6px">v5.7 (E497)</td><td style="border:1px solid #30363d;padding:6px">A4 SNR 精算（真实 PSD loudness、D_max 表）</td><td style="border:1px solid #30363d;padding:6px">无（台账 v47 键亦缺失）</td><td style="border:1px solid #30363d;padding:6px">UNVERIFIED · 台账版本头已并发改 v5.7 但 v47 键缺失</td></tr>
</table>
<div class="note" style="border-color:#d29922;color:#d29922"><b>要求（硬）</b>：organizer 补交冻结 v43–v47 脚本＋out（禁 import qnm、禁硬编码 0.0628831/0.2515323、禁循环标定）；MainAgent 逐项 .venv 独立复跑后按铁律过 GR 门才许入 SSOT。TUFT m 频裂未过门保持 OPEN。</div>
</section>
'''
s=s.replace('</footer>', audit_section+'</footer>')
# 6) footer version bump
s=s.replace('<b style="color:#7ee787">★ TUFT 企业级归一化 v3.8（当前权威；MainAgent 独立 .venv 复算，勘误 #36，E1–E462',
            '<b style="color:#7ee787">★ TUFT 企业级归一化 v5.7（当前权威口径；E1–E497 · 勘误 #42；v5.3–v5.7 数值层 UNVERIFIED 待补证；历史权威层见下）')
s=s.replace('（文件名沿用 E1-E336，内容已更新至 v4.3 / E1–E478 / 勘误 #41（+ v4.3 能源/工程审计 E477 能层χ≈.96 / E478 Penrose+BZ 双关闭·无免费能源）：v30/v31 独立散射信息论收口，D18 物理阻尼物理闭合；&lt;1e-6 实频互证撤销＝谱复平面专属；E459 并行 v28 保留、E460/E461/E462 新增，物理四态 35/61/18/27 冻结）</footer>',
            '（文件名沿用 E1-E336，内容已更新至 v5.7 / E1–E497 / 勘误 #42：v3.8 起 D18 物理阻尼物理闭合；E477 能层χ≈.96 / E478 Penrose+BZ 双关闭·无免费能源；物理四态 35/61/18/27 冻结；v5.3–v5.7 数值层 UNVERIFIED）</footer>')
io.open(p,'w',encoding='utf-8').write(s)
print('html upgraded', orig, '->', len(s))
print('tags balanced sections:', s.count('<section'), s.count('</section>'))
