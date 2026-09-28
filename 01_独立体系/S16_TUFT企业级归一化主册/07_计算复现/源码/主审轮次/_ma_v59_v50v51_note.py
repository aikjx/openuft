# -*- coding: utf-8 -*-
"""_ma_v59_v50v51_note.py — 主册追加 v50/v51 复跑审计注记（append-only）"""
import io, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_企业级归一化主册_v1.0.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()

note = ('> **★★ MainAgent v50/v51 复跑审计（2026-09-24，append-only）**：'
        '**v50（TUFT 旋转频裂，线六）**源码全文已读——自包含独立 Cook–Zalutskiy Leaver 实现'
        '（无 qnm/无 _ma_ import、门靶仅作判定）；.venv 复跑**全部数字逐位复现**：GR 门 A 14.8 位'
        '（独立解尾数 -936 vs 参考 -93410，证明真实独立实现非抄数）、门 B 7.7 位（a⁴ 四截断 '
        '0.25153232）。TUFT 侧：静态 pole 0.434442828−0.056449578i、频裂 **split/a=0.580493**'
        '（真实 E475 场）、裸核三极限带 置零 0.0 / GR 2R⁻³ 2.337008 / 真实 0.580493、real/GR=0.2484；'
        'Rayleigh 0.580493 vs 非微扰延拓@a=0.05 0.579552（互证差 0.16%）。**条件背书**，两个开放问题：'
        '① **静态锚偏差**——TUFT pole 与 Grade-A ref（0.434445178−0.056449760i）差 **2.35e-6（5.6 位）**，'
        'TUFT 侧无门禁，谱方法收敛精度须核查；② **E475 场含手动参数**——`OmF_real=(2/ρ³)e^{−2/ρ}'
        '(1+0.04·barrier)`，0.04·barrier 高斯项**无第一性原理来源**（TUFT 慢转展开未导出），'
        '频裂量级对其鲁棒（~4% 修正）但"真实 E475"标签夸大，须从 TUFT 度规慢转第一性原理确认。'
        '**v5.4 声称 0.09832（无脚本，UNVERIFIED）与 v50 0.5805 方向/量级相反，以 v50 为当前候选数，'
        '差异须解释。**\n'
        '**v51（完整 V 进 Jansen，线七）**复跑逐位一致：门 A 12.9 位 PASS、门 B **1.3 位 FAIL**'
        '（splitR/a=0.2011 vs 0.2515323）；根因=peel alpha 为 Schwarzschild 视界 r=2 构造，Kerr 需 '
        'σ₊=(2ωr₊−ma)/(r₊−r₋) O(a) 归一化——与 MainAgent 谱方法诊断同源；**诚实 FAIL 采纳**，'
        'TUFT 数未报（守铁律）。台账见 main_agent_v59_v50_rerun / main_agent_v59_v51_rerun。\n')

anchor = '台账见 main_agent_v59_v49_rerun。\n'
assert anchor in t, 'anchor not found'
t2 = t.replace(anchor, anchor + note, 1)

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(t2)
os.replace(tmp, p)
print('master note appended; total chars:', len(t2))
