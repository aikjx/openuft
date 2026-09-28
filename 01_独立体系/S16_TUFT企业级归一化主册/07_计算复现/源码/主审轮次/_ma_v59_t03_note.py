# -*- coding: utf-8 -*-
"""_ma_v59_t03_note.py — 主册追加 T03 审计背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent T03 审计背书（2026-09-24，append-only）**：`tuft_t03_line{1,2,3}_*.py` 全文已读、.venv 复跑三线**全部数字复现**。\n'
        '> **线一（B 破坏）**：E329 为 T=0 微扰定理，**字面上不覆盖高温早期宇宙**（三层缺口：零温/有限温、微扰/非微扰、Q=B 或 B−L 未登记）；'
        'sphaleron SM 基准：T_eq=6.839e8 GeV（窗口 160 GeV<T<6.84e8 GeV）、E_sph(0)=7362 GeV=7.36 TeV、Δ(B+L)=6、washout 28/79、'
        '需 Y_{B−L}(in)=2.455e-10 全部复现。**Q 的物理身份登记缺口为真实定义级空洞**（E329 未登记 Q=B 或 B−L）。\n'
        '> **线二（CP 破坏）**：Jarlskog J=3.1503e-5（J/J_G3=0.9845）复现；kappa 表——u/d/s/c/b 冻结但被规范平衡擦掉相干、t 平衡（κ_t=6.93）→ '
        '**无味同时满足"非平衡+携带 CKM 相位"**；缺口 8.7e-11/1e-20=**10^9.94**；TUFT 内部几何全实（cm_t,d_t）→ 无内禀复相位。'
        '**CP 资源内部不可用**，需 η_new~O(0.1)（比 J 强 10⁹）公设。\n'
        '> **线三（非平衡）**：四条严格定理（细致平衡→Y_B=0、de Sitter 稀释 exp(3×60)=1.4894e78、K(T_EW)=9.86e11>>1、E273 静态壁）；'
        '高 T K=1 断点在 T_K1=1.58e14 GeV（alpha_w=1/30）——**reheating 窗口在此之上天然非平衡（无需 V(n,T)），但 TUFT 对 T_rh 无预言**'
        '（P17 只定 H_inf）；轻子生成通道可行（K_N=3.88e-4<1 @ m_N=1e13 GeV）；中微子退耦 1.445 MeV 复现。**Sakharov-3 内部不满足**，V(n,T) 缺失，NE 公设登记。\n'
        '> **破解矩阵 #5（重子生成）状态转换**：未触及 → **结构封闭（不可约输入）**：P_T（B 破坏冻结或承认 sphaleron，Q 身份未登记）'
        '+ η_new（新 CP 相位）+ NE（V(n,T) 外部）。**不可约输入集 5 → 7**。非伪闭合：O1-O4 逃逸口与线一 A/B 判定全部显式开放。'
        '台账见 main_agent_v59_t03_rerun。\n')

anchor = '台账见 main_agent_v59_t02_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
