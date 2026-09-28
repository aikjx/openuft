# -*- coding: utf-8 -*-
"""_ma_v59_v52_note.py — 主册追加 v52 复跑背书注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent v52 复跑背书（2026-09-24，append-only）**：`tuft_v52_tuft_static_converge.py` 全文已读'
        '（自包含、无 qnm/_ma_ import、门靶仅判定；Beyn 围道中心=Grade-A 锚属先验输入，但结果偏离锚 '
        '1e-8 量级证明是真实求解非投影）。.venv 复跑**全部数字逐位复现**：GR 门 A 14.8 位、门 B 7.7 位'
        '（0.25153232）双 PASS。**v50 漂移真修复**：TUFT 静态极点 N=60/90/120 = '
        '0.434445185→0.434445177→0.434445176（偏差 1.34e-8→3.89e-9→4.72e-9），N=90 vs 120 互合 8.4e-10，'
        '**从 v50 的 1e-4 漂移修复 5 个量级**；但仅 **8.4 位，未达 11.6 位门禁 → TUFT 静态门 FAIL**。'
        '**E475 frame-dragging 第一性原理导出接受**（条件定理）：Ω_F(ρ)/a=6∫_ρ^∞ dr\'/(r\'⁴e^{2/r\'}h^{3/2})，'
        '无手动 barrier；复现数值 ratio@ρ=1=0.323、@ρ=10=0.864，大 ρ→2/ρ³ 匹配 GR LT，近壁 (ρ−ρ_h)^{−1/2} 发散。'
        '**交叉对照**：v52 第一性原理 E475（ρ=1 ratio≈0.323）与 v50 手动 barrier 版（≈0.27）差 ~20%——'
        '进一步坐实 v50 频裂 0.5805 不可靠。**三重门禁 FAIL（GR A PASS/GR B PASS/TUFT 静态 FAIL）→ '
        'TUFT 频裂保持 OPEN**（诚实守铁律）。下一步：8.4→11.6 位需双域谱法（近壁 Frobenius 域+外谱域匹配）'
        '或新紧化映射。台账见 main_agent_v59_v52_rerun。\n')

anchor = '台账见 main_agent_v59_v50_sens。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
