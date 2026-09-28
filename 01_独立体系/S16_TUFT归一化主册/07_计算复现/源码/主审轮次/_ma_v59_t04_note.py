# -*- coding: utf-8 -*-
"""_ma_v59_t04_note.py — 主册追加 T04 审计背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent T04 审计背书（2026-09-24，append-only）**：`tuft_t04_line{1,2,3}_*.py` 全文已读、.venv 复跑三线**全部数字复现**。\n'
        '> **线一（M1 确定结果）**：PARTIAL 维持 v8。经典天然确定=严格定理（非线性 PDE 无叠加原理 + Cauchy 唯一演化）；'
        '取消叠加≠解释坍缩=严格定理。数值演示 dφ/dt=φ−φ³ 双稳：t*=ln(2.0647/ε) 解析；'
        'Born 反解 μ 手放（p=0.9→μ=1.2816，f(+) 误差 1e-16）——**μ 是微调非推导**。\n'
        '> **线二（M2 玻恩规则）——本轮最强定理级成果**：**结构性不可导出[严格定理 S5]**：四条阻塞'
        '（态空间错配：实辛流形≠复 Hilbert；经典测度对角无相干；无 H_S⊗H_E 张量分解无退相干对象；确定性阻断本体论随机映射）。'
        '数值复现：rho_Q[0,1]=0.4869≠0 vs rho_C[0,1]=0；f0=P0=0.386399 数值巧合**明确标注为维度事故非推导**；'
        'E_norm=1 需除物理能量。边界公设 **M2-EXT**（泛波函数 Ψ[φ]+Hilbert 内积+幺正泛函薛定谔+玻恩概率密度）登记。\n'
        '> **线三（M3 线性→非线性）**：PARTIAL（错型非线性）。Skyrme L4 使 EOM 非线性[严格]但为 Derrick 稳定项：'
        'R*=√(B/A)/(f_πe)=1.0、E*=2√(AB)f_π/e=2.0、维力 E2=E4=E*/2 全部复现；正则量子化后 L4 退化为幺正顶点非坍缩项。\n'
        '> **破解矩阵 #9（量子测量）状态转换**：未触及 → **结构封闭（不可约边界：M2-EXT+P-B1/P-B2/P-B3）**；'
        'M1/M3 维持 PARTIAL；**不可约输入集 7 → 9**。非伪闭合：O1-O4 逃逸口全部显式开放。'
        '台账见 main_agent_v59_t04_rerun。\n')

anchor = '台账见 main_agent_v59_t03_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
