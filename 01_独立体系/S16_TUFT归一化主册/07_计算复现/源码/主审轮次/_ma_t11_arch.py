# -*- coding: utf-8 -*-
"""MainAgent T11: errata #43 fix + T11 section insert in arch HTML (before footer)."""
import io

path = r'D:\a10\aikjx\code\my_lib\TUFT_企业级归一化全维架构图_E1-E336.html'
with io.open(path, 'r', encoding='utf-8') as f:
    h = f.read()

# ---- errata #43 fix ----
old = "<b>跨管线不一致 ~1.6e-2</b>（T10 frob 0.5699569−0.2876712i vs T09 0.5699579−0.2876550i，两候选并存未定位）"
new = "<b>跨管线不一致 1.619e-5</b>（勘误 #43；T10 frob 0.5699569−0.2876712i vs T09 0.5699579−0.2876550i，数值微扰级接近、非双根签名，两候选并存未定位）"
if old in h:
    h = h.replace(old, new); print('arch errata applied')
else:
    print('WARN arch errata target NOT FOUND')

t11 = """
<section class="arch-section" id="t11-shooting-scoped-out">
<div class="arch-block">
<b>T11 复轮廓 shooting 攻坚 · 锚点 N=480 强化（2026-09-27，MainAgent 审计收口）</b>
<br><b>审计复核</b>：三线本机 .venv 复跑逐位一致——线一 n=0 shooting 0.430352451005−0.100230156674i（|dw|=3.6e-13）；线二 n=1 shooting t=20 0.513402121318−0.285869774501i（|dw|=1.4e-13）；线三 F-pencil N=480 0.434445176596−0.056449764639i（|dw|=1.8e-13）
<br><b>核心结论 1 · n=0 锚点独立强化（严格定理级数值交叉）</b>：谱线阶梯 N=300→360→480 收敛，|w480−外推锚|=4.387e-10 ≤1e-9——<b>T10 冻结锚 0.434445176207−0.056449764436i 的权威数值证据链完整</b>（T08 Gate A → T10 冻结 → T11 N=480 强化）
<br><b>核心结论 2 · shooting 方法学划界（负结论有价值）</b>：锚附近 |R| 景观平坦无根——V~3/ρ² 长程尾使 T09 f1/f2 peel 失效，锚残差为 ~1/Smatch² 尾部漂移非 BVP 根；方向证据 |D(anchor,|s|)| 单调趋零（0.86→3.1e-4）确认新锚为复轮廓 BVP 极点，但外向 IVP 在强增长轮廓上（泄漏指数压制、窄盆地）不能钉到 1e-9
<br><b>核心结论 3 · n=1 三候选 STANDOFF</b>：复射线 shooting 根随 t_match 漂移 1.557e-1（0.513402−0.285870i → 0.661274−0.334668i），vs T09（0.5699579−0.2876550i）/T10（0.5699569−0.2876712i）均差 ~1.03e-1 未命中；有限 t 零为 1/|s|² 漂移偶然相消
<br><b>勘误 #43</b>：n=1 跨管线差异 1.619e-5（非 1.6e-2）——T09/T10 为数值微扰级接近、非双根/泄漏对签名
<br><b>权威方法学裁决</b>：TUFT 径向方程极点唯一权威路线 = 谱离散（Chebyshev/Frobenius 铅笔）+ Beyn 围道；有限匹配 IVP shooting（实轴/复轮廓）均不能独立钉定极点。Gate B n=1,2 维持 OPEN（n=2 因 n=0 自检未过不背书）
<br><i>台账 main_agent_v60_t11_line1/2/3_rerun + errata_43；latest_round=v6.0_T11_anchor_N480_reinforced_shooting_scoped_out_gateB_open；E1–E498 冻结不变。</i>
</div>
</section>

"""

anchor = "</footer>"
idx = h.rfind(anchor)
if idx < 0:
    print('ERROR footer anchor not found')
else:
    h = h[:idx] + t11 + h[idx:]
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(h)
    print('arch chars now:', len(h))
