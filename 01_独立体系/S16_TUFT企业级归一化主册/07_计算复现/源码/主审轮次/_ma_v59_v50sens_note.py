# -*- coding: utf-8 -*-
"""_ma_v59_v50sens_note.py — 主册追加 v50 敏感度降级注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent v50 敏感度核查——TUFT 频裂降级 OPEN（2026-09-24，append-only，最重要审计结论）**：'
        '① **静态 pole 不收敛**：N=60→90→120 的 TUFT 静态极点 0.434442828→0.434509369→0.434846785，'
        '**随 N 增大远离 Grade-A 锚**（偏差 2.36e-6→7.6e-5→4.1e-4）——谱方法系统误差/伪根污染特征；'
        'N=60 的 2.35e-6 一致是**巧合**非收敛。② **barrier 手动参数敏感**：split/a 在 amp=0/0.04/0.10 下 '
        '为 0.5636/0.5805/0.6058（~3%）。③ GR 2R⁻³ band 2.337008 精确复现。'
        '**裁决：TUFT split/a=0.5805 由"条件定理声称"降级 OPEN**——Rayleigh 与非微扰延拓的 0.2% 互证是'
        '**同一未收敛基上的内部一致性**（共用 (u,v,w0)，系统误差一致传导，不能互证正确性）；'
        '叠加"TUFT 侧无门禁 + 静态基不收敛 + E475 场含手动参数"三因素，精确值 0.5805 **不可背书**。'
        'lapse 压制机制（real/GR≈0.25 量级）仍具物理动机，作为**量级候选**保留。'
        '**修复路径**：先解决 TUFT 静态求解器收敛（b_t 复龟坐标、U 拟合窗口、Frobenius 截断、'
        'N 收敛到 Grade-A ≥11.6 位），再从 TUFT 慢转展开**第一性原理导出 E475 frame-dragging 场**'
        '（禁手动 barrier）。台账见 main_agent_v59_v50_sens。\n')

anchor = '台账见 main_agent_v59_v50_rerun / main_agent_v59_v51_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
