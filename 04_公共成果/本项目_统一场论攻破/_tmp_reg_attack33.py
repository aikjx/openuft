# -*- coding: utf-8 -*-
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
P = r'd:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破\README.md'
L = io.open(P, encoding='utf-8').read().split('\n')
idx = [i for i, l in enumerate(L) if l.startswith('- **attack32')]
assert len(idx) == 1, idx
LINE = (
    '- **attack33 2-loop M_SUSY 跨册差异机器定位（2026-10-31）**：'
    '`判定_attack33_2loopMSUSY跨册差异机器定位_2026-10-31.md` + 引擎 '
    '`attack33_2loopMSUSY跨册差异机器定位_2026-10-31.py` / 数据 .json / 记录 _report.txt'
    '（10 条目、FAIL 1 / CORRECTED 3 / BOUNDARY 2 / PASS 1 / INFO 3、退出码 0）。'
    '**裁定 1（域截断）**：attack30 的 2-loop `M_SUSY=193.04415 GeV` 恰等于其 L1 搜索域上界 '
    '`M_Z*exp(0.75)`（相对偏差 3.70e-09；源码注释声称上界 3.0 而 `range(46)` 实为 0.75，差 4 倍/9.49 倍 M_SUSY）'
    '⇒ 该数是域边界不是解，原域内最优点 residual `7.512e-01` 未收敛；扩展域+精修后 residual 降到 `7.461e-14`（13.00 个数量级，粗扫仅贡献 1.02）'
    '⇒ 跨册 12.01 倍差异的真实归因是「搜索域截断 + 未精修 + 未报 residual」。'
    '**裁定 2（撤回 F5c 归因）**：两册真实 b_ij 只在 b33 符号上不同（+14 vs -14），不存在「一方只有对角项」；'
    'F5c 的 V1（183.60 GeV）落在 193 附近属数值巧合 ⇒ 「非对角项」归因作废，其「b_ij 约定有影响」的结论仍成立并被量化为 **7.7312 倍**'
    '（2317.71643 vs 17918.76520，两值分别逐位复现 attack32 的 V0 与 V3）。'
    '**裁定 3（本册 v1 自纠）**：v1 的 `flow` 用单一矩阵跑 SM 段与 MSSM 段，解的不是 attack32 的方程组'
    '（v1 得 1780.00 / 24053.22，attack32 得 2317.72）；改分段矩阵后逐位复现，'
    '⇒ **v1 的 13.51 倍 b33 敏感度作废**，引用纪律由四项扩为五项（新增「分段动力学矩阵」）。'
    '红线：不判 attack30/attack32 作者算错，不宣称 MSSM 被否证，只判「报出的量是不是解」与「是否同一方程组」。'
)
L.insert(idx[0] + 1, LINE)
io.open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('inserted at line', idx[0] + 2)
print('total lines', len(L))
