# -*- coding: utf-8 -*-
"""_ma_v59_cheb_interim.py — 记录谱方法中间结果到主册（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **MainAgent 谱方法中间试验（2026-09-24，append-only，IN-PROGRESS 诚实记录）**：'
        '为修复 v49 门 B FAIL（Jansen 微扰的 O(a) 虚部交叉项近似不足），MainAgent 尝试把**完整 '
        'Teukolsky V(r)**（含 4i(r−1)K/Δ 精确项）直接离散进 Jansen 紧化 Chebyshev 谱方法（'
        '`_ma_kerr_teukolsky_cheb.py`，不 import qnm、无硬编码、A2/A1/A0 三矩阵按 w 幂组装）。'
        '**门 A 结果 FAIL（0.6 位）**：直接离散内部点未显式提出视界入波/无穷远出射的 Frobenius 指数，'
        '谱被伪根污染——这确认"完整 V 进 Jansen"需要组织者 v24 已验证的边界工程框架（入波线性化+'
        '出射外推），非简单替换。**状态：OPEN/IN-PROGRESS**，不消耗 E 号、不进四态。\n')

anchor = '台账见 main_agent_v59_v49_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master interim note appended; total chars:', len(t2))
