# -*- coding: utf-8 -*-
"""_ma_v59_master_note.py — 主册追加 v49 复跑背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent v49 独立复跑背书（2026-09-24，append-only）**：`tuft_v49_deturbed_teukolsky_jansen.py`+`_out.txt` '
        '**真实落盘且自包含**（numpy/scipy only、无 qnm import、门靶常量仅作判定对照、求解路径无硬编码）。'
        'MainAgent 先 Read 源码再 .venv 原样复跑，**全部数字逐位复现**：GR 门 A PASS（N=40/50/60 最佳 '
        '|err|=1.757e-13，12.8 位）；GR 门 B **FAIL**（adjoint Rayleigh 一阶微扰：splitR/a=0.265681 vs 靶 '
        '0.2515323，实部 5.6%；splitI/a=1.6017 vs 0.0080，**200×**）；TUFT 频裂保持 OPEN。'
        '**这是组织者首个真实落盘的旋转攻坚，诚实 FAIL 背书采纳**。诊断：其 (iii) 项 '
        '`i·am·2(r−1)/r³·g·D` 是 Teukolsky 交叉项 4i(r−1)K/Δ 的**近似光滑核**，虚部结构不完备——'
        'Jansen 微扰嵌入路径在 O(a) 虚部交叉项上已被证明不足。**对照（关键）**：MainAgent 第二独立实现'
        '（完整 deturbed Teukolsky + Cook–Zalutskiy Leaver，`_ma_kerr_leaver_full.py`）GR 门 A 14.8 位/'
        '门 B 7.7 位**双 PASS**——完整径向方程**精确包含全部交叉项**（无需微扰展开）。'
        '⇒ **Jansen 微扰路径被完整 Leaver 取代**，作为 TUFT 反射壁扩展的基座。'
        'TUFT 旋转 m 频裂仍 **OPEN**（反射壁 BC 进完整 Leaver 是下一仗）。台账见 main_agent_v59_v49_rerun。\n')

# 插到 v5.9 门 PASS 注记之后（第一个注记块之后）
anchor = '台账见 main_agent_v59_t01_gate_pass。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
