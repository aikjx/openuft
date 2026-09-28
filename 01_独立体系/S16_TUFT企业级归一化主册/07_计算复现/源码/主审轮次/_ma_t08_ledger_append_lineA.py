# -*- coding: utf-8 -*-
"""MainAgent: append T08 lineA audit result to master ledger (append-only)."""
import os, shutil

p = 'TUFT_企业级归一化主册_v1.0.md'
shutil.copy(p, 'TUFT_企业级归一化主册_v1.0.md.bak_t08la')
note = '''

---

## T08 线 A · 线二泛音定量闭合 MainAgent 独立审计复跑（2026-09-27）

<!-- ma-audit-t08-lineA-rerun -->

**复跑验证：7/7 数值点逐位一致（|dw| < 3.4e-13）**。审计变体 import 官方模块函数逐字复用（无 main 副作用），本机 .venv 跑最小集：n=0 N=90/120/180 + n=1 N=180/240 + n=2 N=180/240，wall 477.8s。

- n=0：err 3.885e-09 / 4.720e-09 / 4.808e-09 vs TUFT_ANCHOR —— 与官方完全一致（管线复现）
- n=1：N=180 0.569959376313−0.287683421561i、N=240 0.569958559840−0.287657668455i —— 逐位一致
- n=2：N=180 0.499906955875−0.406567819775i、N=240 0.496288359607−0.396115697374i —— 逐位一致

**裁决确认**：UNREACHABLE 为数值事实（非环境产物）——
- n=1 单调分支 interconsistency 9.6e-06..1.8e-05 ≫ 1e-9；T07 已证 N=300→360 pole-switch 3.0e-5（真泛音+泄漏增长解双根切换），需 N≥300 而该区段本机 OOM 两次/卡死一次
- n=2 未定位（1.7e-02），需 N≥480 + SVD de-clustering
- WKB Gaussian peel 已在 T07 构建→测试→拒绝（n=0 错位 1e-3）；修正高阶 Frobenius peel 须先过 n=0 1e-9 门
- **Gate B n=1,2 维持 OPEN**（定量 1e-9 背书在本机硬件 N≤240 不可达），不伪闭合

四态：A 严格（GR Leaver 参考）/ B 条件（n=0 gate PASS 复现）/ C 定义（Beyn 隔离极点有理近似）/ D 开放（泛音谱）。

台账键：main_agent_v60_t08_lineA_rerun。latest_round=v6.0_T08_audited_lineB_endorsed_lineA_open_confirmed。
'''
with open(p, 'a', encoding='utf-8') as f:
    f.write(note)
print('appended; new size', os.path.getsize(p))
