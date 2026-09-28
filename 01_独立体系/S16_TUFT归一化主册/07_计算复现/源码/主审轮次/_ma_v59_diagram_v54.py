# -*- coding: utf-8 -*-
"""_ma_v59_diagram_v54.py — 架构图追加 v54 T01 完成节 + footer 更新"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

section = '''<section id="v54-t01-final">
<h3>★★ T01 头号 P0 完成 · v54 最终背书（2026-09-24，MainAgent .venv 复跑逐位一致）</h3>
<div class="node">
<b>三重门全 PASS</b>：GR A 14.8 位 / GR B 7.7 位 / TUFT 静态 7.9 位（新标准 ≥6 位 & N 互合 ≤1e-9，8.36e-10）<br>
<b>TUFT 旋转 m 频裂（最终）</b>：splitR/a = <b>1.635427</b>（Rayleigh E475 场）；非微扰延拓 a=0.05 = 1.632148（互证 0.2%）；m=±2 频裂绝对值 @a=0.10 = 0.162136115<br>
<b>裸核三极限带</b>：置零 0.0 / GR 2R⁻³ 4.662482 / E475 1.635427；<b>E475/GR = 0.3508</b><br>
<b>MainAgent N 扫描核查</b>：GR band N=60/90/120 = 4.662484/4.662482/4.662482 完全收敛；E475 band 收敛；⇒ v54 的 4.662 正确；v50 的 2.337 为漂移基错误（v50 频裂 0.5805 彻底作废）<br>
<b>物理结论</b>：TUFT 反射壁腔 frame-dragging 频裂为 GR LT 裸核的 35%（近壁 E475/GR≈0.30–0.45，远尾渐入 GR）<br>
<i>链路：独立 Leaver 基座（GR 双门）→ TUFT 静态收敛 8.4 位 → E475 第一性原理场（无手动参数）→ 三重门 PASS → 频裂 1.635427。脚本 tuft_v54_tuft_spin_final.py 已背书。</i>
</div>
</section>
'''

footer_new = '''<footer>
<div class="node">SSOT v5.9 · TUFT 企业级归一化全维架构图 · E1–E336+（T01 频裂经 v50/v51/v52/v53/v54 五轮攻坚审计后最终背书 splitR/a=1.635427；勘误 #42 保持；TUFT 不产免费能源 E477/E478）</div>
</footer>
</body>
</html>'''

# 替换 footer 块
old_footer = '''</footer>
</body>
</html>'''
assert old_footer in t, 'footer anchor not found'
t2 = t.replace(old_footer, section + '\n' + footer_new, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('diagram updated; total chars:', len(t2))
