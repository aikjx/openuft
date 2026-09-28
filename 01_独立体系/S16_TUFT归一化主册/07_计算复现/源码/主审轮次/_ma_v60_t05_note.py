# -*- coding: utf-8 -*-
"""_ma_v60_t05_note.py — 主册追加 T05 收官审计背书注记（append-only，锚 freeze 标记）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('\n> **★★ MainAgent T05 收官审计背书（2026-09-24，append-only）**：`tuft_t05_finalize_v6.py` 全文已读、.venv 复跑**全部数字复现**，§21 与台账已验证。\n'
        '> **复跑校验**：α⁻¹=137.035999、m_Pl/m_e=2.389222e+22、y_t/y_e=3.380829e+05（G_res=3.380829e+03，log10=3.529 dex）、washout=28/79=0.354430、'
        'Y_B−L(in)=2.454643e-10、三角反常三通道 0/0/2.22e-16 全部一致。\n'
        '> **矩阵终态冻结背书**：完全闭合=0（禁止凑数）、结构封闭(输入层)=3（#2 G3 / #5 P_T+η_new+NE / #9 M2-EXT）、条件性闭合=1（#13 P17）、'
        '部分覆盖=10、未触及=0；"结构封闭"≠"完全闭合"诚实标注，O 系列逃逸口显式保留。\n'
        '> **不可约输入集 9 项权威登记背书**：I1–I9（含 E329 Q=B−L 定义识别，A/B 路径未选定、P_T 备选开放）；P18 最小性主张降级（E483/E484 自解锁锚失败）'
        '与 P19 不入 9 项——处理正确。\n'
        '> **E329 Q=B−L 登记完成确认**（T03 遗留项闭环）：定义识别 + SM 约化条件定理 + Q=B 冲突开放。\n'
        '> **开放项冻结**：O-M1..O-M4、N_R Hopf、c_m 区间/点值、QNM 空腔谱、l_A CMB ~12%、汤川 E479 BLOCKED、Page/D25、重子温窗——状态与下一步全部显式。\n'
        '> **不变量**：勘误 #42 held、四态 35/61/18/27 冻结、完全闭合=0 冻结、D18 v31 不回退、联盟层 2/6、E1–E498 不变（本轮零新 E-number）。\n'
        '> **裁决：TUFT v6.0 终版冻结通过，归一化闭环正式收口。** 台账见 main_agent_v60_t05_rerun。\n')

marker = '<!-- ma-t05-v60-freeze -->'
assert marker in t, 'freeze marker not found'
t2 = t.replace(marker, marker + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master endorsement appended; total chars:', len(t2))
