# -*- coding: utf-8 -*-
"""_ma_v59_v53_note.py — 主册追加 v53 复跑审计注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent v53 复跑审计（2026-09-24，append-only）**：`tuft_v53_dual_domain_spectral.py` 全文已读、'
        '.venv 复跑逐位复现（自包含、无 qnm/_ma_ import、门靶仅判定）。GR 门 A 14.8 位/B 7.7 位双 PASS 复现；'
        '**TUFT 静态 4.4 位（0.4344631137−0.0564889878i，|err|=4.31e-5）——比 v52 的 8.4 位退步**；'
        '三重门 FAIL → TUFT 频裂 OPEN（诚实守铁律）。'
        '**★ 实现缺陷发现**：`outer_logder(N,w)` 的 N 参数**未参与计算**（Lobatto 网格参数是空操作，匹配残差'
        '与 N 无关）——N=60/90/120 是同一 shooting 重复三次，报告的 2.02e-9"互合"是浮点路径噪声而非收敛证据。'
        '实际精度受 shooting rtol + Frobenius r_in 拟合（c_j lstsq logspace 2e-3..0.45）限制。'
        '**E475 推导链**：Ω_F 数值逐位复现（ρ=1 ratio 0.3234）；推导链补入但 **(ii) 中间式 ρ² 与最终 ρ⁴ 不一致**'
        '（GR LT 应为 ρ⁴ω\'=const→2/ρ³）——最终公式数值/极限已验证（大 ρ→2/ρ³、近壁发散），接受为条件定理，'
        '推导链 (ii) 待澄清。**裁决**：v53 双域 shooting 退步（4.4 < 8.4），诚实 FAIL 采纳；'
        '**v52 的 8.4 位收敛解（N 互合 8.4e-10）仍是当前最佳 TUFT 静态锚**。台账见 main_agent_v59_v53_rerun。\n')

anchor = '台账见 main_agent_v59_v52_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
