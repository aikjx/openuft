# -*- coding: utf-8 -*-
"""_ma_v59_v54_note.py — 主册追加 v54 最终背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★★ MainAgent v54 最终背书——T01 头号 P0 完成（2026-09-24，append-only）**：'
        '`tuft_v54_tuft_spin_final.py` 全文已读、.venv 复跑**全部数字逐位复现**：三重门 PASS'
        '（GR A 14.8 位 / GR B 7.7 位 / TUFT 静态 7.9 位 + N 互合 8.36e-10，新标准 ≥6 位 & ≤1e-9）；'
        '**TUFT 频裂 splitR/a=1.635427**（Rayleigh E475 场）、非微扰延拓 a=0.05 1.632148（互证 0.2%）、'
        'm=±2 频裂绝对值 @a=0.10=0.162136115；裸核三极限带 置零 0.0 / GR 2R⁻³ 4.662482 / E475 1.635427，'
        '**E475/GR=0.3508**。\n'
        '**★ MainAgent N 扫描核查（`_ma_v59_v54_grband_conv.py`）**：GR band N=60/90/120 = '
        '4.662484/4.662482/4.662482 **完全收敛**；E475 band 1.635428/1.635428/1.635427 收敛；'
        'E475/GR=0.3508 与 N 无关。**⇒ v54 的 4.662 正确且收敛；v50 的 2.337 是漂移基错误**'
        '（v50 在漂移极点 0.434442828 提取特征向量 + N=60/b=4+0.5i/Frobenius 级数，基不可靠）。'
        '**v50 频裂 0.5805 彻底作废**（漂移基 + 手动 barrier 场 + GR band 错误三重缺陷）。\n'
        '**物理结论**：TUFT 反射壁腔对 E475 第一性原理 frame-dragging 场的频裂斜率 '
        'splitR/a≈1.635，为 GR LT 裸核（4.662）的 **35%**（近壁 E475/GR≈0.30–0.45，远尾渐入 GR）。\n'
        '**T01 状态**：从 v48（Beyn 旋转 FAIL）到 v54 完整闭环——独立 Leaver 基座（GR 双门 PASS）'
        '→ TUFT 静态收敛（8.4 位）→ E475 第一性原理场（无手动参数）→ 三重门 PASS → 频裂 1.635427。'
        '台账见 main_agent_v59_v54_rerun。\n')

anchor = '台账见 main_agent_v59_v53_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
