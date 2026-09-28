# -*- coding: utf-8 -*-
"""_ma_v59_t02_note.py — 主册追加 T02 审计背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent T02 审计背书（2026-09-24，append-only）**：`tuft_t02_line{1,2,3}_*.py` 全文已读、.venv 复跑三线**全部数字复现**。\n'
        '> **线一（E145 几何上界精确化）**：G=α·Q·τ 三因子分解，基态扫描 G∈[2,60]（10^1.78）；缺口 Y_span/G_max=5.69e3=10^3.755。'
        '**纯几何原理性差 ~10^3.5 阶——量级论断稳健接受**；但"严格定理"标签偏强（G 拆法为定义选择、α≤5 为经验扫描），'
        '**降级为条件定理**（精确常数 G_max 解析值开放）。\n'
        '> **线二（seesaw×FN 桥接）**：seesaw light eigen −5.99e-10 GeV≈0.6 eV 复现；FN 反解最佳 dQ=6、ε_req=0.2579 vs β−1=0.2638、rel-dist=2.28e-2 复现。'
        '**★ 口径纠正**：线二以 G_geom=1e2 作分母，但线一本尊扫描 G_max=60——若用 60，ε_req(dQ=6)=0.2366、rel-dist=0.115，'
        '"0.023 巧合"质量下降 5 倍。**判定：dQ=6/β−1 为口径敏感的弱巧合，不作理论证据**。算术桥接闭合（1e2×3.4e3=3.4e5，条件定理级）；'
        '内部来源被 E479 + N_R Hopf 身份开放项封锁（开放命题，诚实不闭合）。\n'
        '> **线三（G3 三代不可约输入公设）**：每代反常消消数值演示复现（SU(3)²U(1)=0、SU(2)²U(1)=0、U(1)³=1.9e-16、grav²U(1)=0）→ '
        '反常条件对任意 N_g 恒成立，不能选定 3；Weyl 总数 45；**不可约输入集=5**（α⁻¹、m_Pl/m_e、y_t/y_e、N_g、θ_QCD）+ 量纲 G。'
        '公设诚实：明确不推导、不伪闭合，逃逸口 O1/O2 开放。口径注：y_t 取 m_t/v=0.70（pole）与线一/二 0.99（M_Z）跨度同为 3.4e5 量级。\n'
        '> **T02 裁决**：三代起源从"部分覆盖"**正式定性收口为不可约输入 G3**（破解矩阵 #2 结构封闭，非伪闭合）；'
        '汤川跨度保持部分覆盖（算术桥接闭、来源开放）。E145 从"最多 10²"强化为扫描 G_max=60+Derrick 保护的原理性缺口。'
        '台账见 main_agent_v59_t02_rerun。\n')

anchor = '台账见 main_agent_v59_v54_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
