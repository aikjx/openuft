# -*- coding: utf-8 -*-
"""_ma_v60_t07l4_note.py — 主册追加 T07 线四审计背书注记（append-only，锚文件尾）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('\n> **★★ MainAgent T07 线四审计背书（2026-09-25，append-only）**：`tuft_t07_line4_vortex_spiral.py` 全文已读、.venv 复跑**逐位一致**。\n'
        '> **子任务 1 · 4 力口径裁定**：u_ν∂_μT^{μν} 字面收缩=静止系功率（反对称 F × 对称 uu，在壳恒 0）——**严格定理**；空间 4 力=h 投影=qF^{μν}u_ν，口径差异显式标注（caliber=projector，非矛盾）。'
        '演化方程三通道：Lorentz（严格）+ 自旋-挠率 S^{μν}∂_ν(τ̂)（TUFT 公设，OPEN）+ OAM 传递 l·(σ_abs/ω_L)·束流（OPEN）。E18 γv=c 与螺旋世界线自洽（严格）。\n'
        '> **子任务 2 · 非傍轴 LG**：Lax 一阶修正 E_z^(1)=−(i/k_L)div_⊥E_⊥；R_old~1/(k_Lw₀) 标度常数 1.4142（严格）；**傍轴失效阈值 w₀/λ≈2.251**（R_old=10% 判据）；w₀/λ≥5 傍轴定量可用（R_old<4.5%）。\n'
        '> **子任务 3 · 共振相空间**：共振条件 l·w_s=k_L(γ−sinθ)、sinθ=τ/w_s（Lorentz Doppler，严格）；解析轨迹 κ_res、τ_res；l=1..6 峰值扫描复现；共振壳半宽~Γ/l，高 l 通道更窄；共振=轴向 OAM 力峰（条件定理），稳定/不稳定定性（Floquet OPEN）。\n'
        '> **子任务 4 · 对照仿真**：章节定位合规——主册无 §13、§16 仅门/讨论锚，按规则新建结构（§13=傍轴紧聚焦失效构型、§16 讨论）。旧方案 w₀/λ=0.5：R_old=0.4501（~45% 散度残差）+ 缺 E_z 致轴向力 f³ O(1) 误估；新方案 R_new=0.1433（**3.1× 压散度**）；f·u=0 为 Lorentz 恒等式两方案皆成立（诚实标注非失效通道）。新标签 **D31–D34**。\n'
        '> **E 号冻结**：E1–E498 不变，T07-4 仅 D31–D34 标签；无伪闭合。\n'
        '> **裁决：T07 线四 ENDORSED。** 台账见 main_agent_v60_t07_line4_rerun。\n')

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t + note)
os.replace(tmp, p)
print('master T07 line4 note appended; total chars:', len(t) + len(note))
