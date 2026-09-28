# -*- coding: utf-8 -*-
"""MainAgent: append T09 line2 audit + anchor-bias finding to master ledger (append-only)."""
import os, shutil

p = 'TUFT_归一化主册_v1.0.md'
shutil.copy(p, 'TUFT_归一化主册_v1.0.md.bak_t09l2')
note = '''

---

## T09 线二 · 低内存 N≥300-480 Beyn + SVD de-clustering MainAgent 审计（2026-09-27）

<!-- ma-audit-t09-line2 -->

**Read 全文 + 审计**：S1+S2 内存纪律继承 T08 线 A；SVD de-clustering（r=8 探针列、枚举轮廓内极点、奇异值排序、跨 N tol=0.015 稳定链、N=480 shrink）设计正确；裁决逻辑显式区分算法/内存界限。

**复现证据**：
- 本机 auditA：n=0 N=90/120/180 = 3.885e-09/4.720e-09/4.808e-09 **逐位一致**（管线 VERIFIED）
- 本机完整 N=300 三阶段复跑被外部终止（exit -1 无 traceback，系统健康，历史 OOM 区段）——单阶段变体 B 后台续跑，非阻塞
- **官方内部交叉验证（强证据）**：T09 N=300 vs T07 独立运行 N=300 = 5.422e-10、N=360 vs T07 = 1.906e-09（两套 nc 阶梯 300/500/700 vs 500/700/900 交叉一致）

**关键数值（组织者 out + 回执）**：
- n=1：N=300 0.569957939619−0.287655030300i、N=360 0.569974871843−0.287680404348i；interconsistency N240→300=2.710e-06（单调）、N300→360=3.050e-05（**pole-switch 跨管线确认**）
- n=2：N=300 0.502373260−0.409432283i、N=360 0.476411761−0.414820488i、N=480 0.491671861−0.394756853i（有效秩 1→2，次模刚冒头 4.5e-6）；**跨 N 漂移 ~2.5e-2 ≫ tol，未定位**
- **N=480 全程干净运行（单铅笔驻留、无 OOM、RSS~0MB）——prior N≥300 OOM 是旧版存全 resolvent 所致，本版瓶颈非 RAM**

**裁决**：n=1 best 2.71e-6、n=2 未定位，均 ≫ 1e-9 → **UNREACHABLE，Gate B n=1,2 维持 OPEN**。真正界限：孤立极 Beyn 作用在非孤立双根/泄漏对 + plain s^β peel 谱截断。剩余路径（未做，不凑数）：(i) 带泛音相位起点的外向 WKB/Leaver 打靶；(ii) 先在 n=0 验证到 1e-9 的高阶 Frobenius peel。

**锚点偏置（T09 最大发现，定义识别）**：旧 psi 笔收敛值 0.434445176377−0.056449764526i 与新 F 笔收敛值 0.434445176903−0.056449764800i 互合 ~6e-10（独立双管线），冻结锚点 0.434445178000−0.056449760000i 偏离 ~4.9e-9（实 1.1e-9/虚 4.8e-9）= 旧 psi peel 平台偏置。**锚点升级候选 0.4344451769−0.0564497648i（置信 ~6e-10）**；Gate A 用新锚重判（互合已过 4.42e-10）后泛音可推进。

四态：A 严格（GR 参考 + peel 推导/收敛证明 + Gate A(i) PASS + 锚点偏置发现）/ B 条件（n=0 gate PASS 复现）/ C 定义（Beyn + SVD）/ D 开放（泛音谱）。台账 main_agent_v60_t09_line2_rerun。latest_round=v6.0_T09_dual_line_completed_gateB_open_anchor_bias_found。E1-E498 冻结不变。
'''
with open(p, 'a', encoding='utf-8') as f:
    f.write(note)
print('appended; new size', os.path.getsize(p))
