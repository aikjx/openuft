# -*- coding: utf-8 -*-
"""_ma_v59_diagram.py — 架构图追加 v5.9 T01 门 PASS 节 + 更新 footer 版本头"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

new_section = ('<section id="v59-t01-gate-pass" style="box-sizing:border-box;width:100%;padding:18px 20px;'
               'border-top:3px solid #3fb950;background:#161b22;color:#e6edf3;'
               "font-family:'Microsoft YaHei',Arial,sans-serif;\">\n"
               '<h2 style="font-size:16px;color:#3fb950;margin:0 0 10px 0;">★★ v5.9 T01 门双 PASS（'
               'MainAgent 第二独立 Kerr QNM 求解器，2026-09-24）——完整 deturbed Teukolsky + Cook-Zalutskiy Leaver，零写公式</h2>\n'
               '<div class="note ok" style="border-color:#3fb950;color:#3fb950"><b>实现</b>：'
               '角向 Cook–Zalutskiy 2014 谱方法（五对角矩阵，CG 与 sympy 逐位核对）+ 径向 Leaver 连分数'
               '（完整 V(r) 含交叉项 <code>4i(r−1)K/Δ</code>——v48 缺失项）+ Nollert u1..u3 + 同步牛顿；'
               '不 import qnm、求解器无硬编码门靶。<b>GR 门 A PASS（14.8 位）</b>：a=0 l=2 m=2 n=0 '
               '从偏离初值 0.3700−0.0900i 独立收敛 0.373671684418042−0.088962315688936i'
               '（|err|=1.646e-15，≥11.6）；残留 |Cf|=9.9e-16。<b>GR 门 B PASS（7.7 位）</b>：'
               'splitR/a Richardson a² 线性 0.25153218（6.9 位）/a⁴ 四截断 0.25153232（7.7 位）vs 靶 0.2515323'
               '（≥4 位）；per-m slope 0.12576616 与 qnm c_rot=0.0628831（split=4k）自洽。<b>意义</b>：'
               'v48 门 B FAIL 根因（缺 O(a) 虚部交叉项）被完整方程直接解决；组织者 v5.3 无证声称方向获实质'
               '独立支撑（其数字仍 UNVERIFIED）；<b>TUFT 旋转 m 频裂仍 OPEN</b>——反射壁 BC（r_wall、'
               'Neumann/有界支）进方程是下一步。脚本 <code>_ma_kerr_leaver_full.py</code>/'
               '<code>_ma_t01_gate_verify.py</code>/<code>_ma_kerr_gateB2.py</code>（+out）全部落盘可复跑。</div>\n'
               '</section>\n')

anchor = '</section>\n</footer>'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, new_section + anchor, 1)

old_ver = ('<b style="color:#7ee787">★ TUFT 企业级归一化 v5.7（当前权威口径；E1–E497 · 勘误 #42；'
           'v5.3–v5.7 数值层 UNVERIFIED 待补证；历史权威层见下），物理四态 35/61/18/27，'
           'D18 物理阻尼物理闭合 g=.056±.001/Q≈3.85）：</b>')
new_ver = ('<b style="color:#7ee787">★ TUFT 企业级归一化 v5.9（当前权威口径；E1–E498 · 勘误 #42；'
           'MainAgent 第二独立 Kerr QNM 求解器 GR 门 A 14.8 位/门 B 7.7 位双 PASS；'
           'v5.3–v5.7 数值层仍 UNVERIFIED 待补证；物理四态 35/61/18/27，'
           'D18 物理阻尼物理闭合 g=.056±.001/Q≈3.85）：</b>')
if old_ver in t2:
    t2 = t2.replace(old_ver, new_ver, 1)
    ver_note = True
else:
    ver_note = False

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('diagram updated; version head replaced:', ver_note, '; total chars:', len(t2))
