# -*- coding: utf-8 -*-
"""MainAgent: append T08 lineB endorsement to master ledger (append-only)."""
import os, shutil

p = 'TUFT_归一化主册_v1.0.md'
shutil.copy(p, 'TUFT_归一化主册_v1.0.md.bak_t08lb')
note = '''

---

## T08 线 B · QCD 弦张力与夸克禁闭 MainAgent 独立审计背书（2026-09-27）

<!-- ma-audit-t08-lineB-endorsed -->

**背书（ENDORSED）**：Read 脚本全文（纯代数、无随机、双精度、四态分级显式）→ .venv 复跑 exit=0 → 脚本自写 out 与官方 **191/191 行逐行一致**（早期 diff 的 BOM 与尾空行差异系 PowerShell `*>` 重定向编码人工产物，非脚本输出差异，已排除）。

关键数值（官方=复跑一致）：
- sigma_QCD = 0.180 GeV^2；sigma_fund = M_pl^2 = 1.4906e38 GeV^2；**gap = 8.28e38（log10=38.92）**
- **Z(pi_3(S^2)) 与 Z_3(center SU(3)) 不同构 → 裸同伦映射不存在（A 级严格定理）**
- gap = (M_pl/Lambda_eff)^2 = RG 跑动距离 **44.8 e-folds**（B 级条件定理：本质为层级非缺陷，强行几何补偿即伪闭合）
- Abel 投影 + 对偶 Meissner 条件桥：闭 Hopf 环 ↔ 闭禁闭磁通环，两外源切断为 QCD 开弦（B 级）
- 禁闭对应：Hopfion 有限能边界迫使磁通管闭合 ≡ 色 Gauss 定律；**L_break = 0.60 fm**（与强子半径 ~1 fm 一致）
- 开放（D 级，不伪闭合）：同一 Lagrangian 同出 Hopfion 与 QCD 磁通管、从 M_pl 预言 Lambda_QCD（需完整 SU(3) beta 函数 + UV 边界）、Z<->Z_3 严格映射、端点约束定量匹配

判别预言增量：gap=(M_pl/Lambda_QCD)^2 严格、Z!=Z_3 严格、Abel 投影条件桥（B）、n=1,2 泛音谱仍开放（见线 A）。

台账键：main_agent_v60_t08_lineB_rerun。E1-E498 冻结不变；T08 线 B 不新增 E 号。
'''
with open(p, 'a', encoding='utf-8') as f:
    f.write(note)
print('appended; new size', os.path.getsize(p))
