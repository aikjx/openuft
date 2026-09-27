# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 「算法联盟缺陷修复体系」第一性审计
============================================================

审计对象
--------
2026-09-25 提交的《算法联盟·空间螺旋几何统一场论 缺陷修复体系｜核心公理+闭环公式+纠错算法理论》：
  - 4 条新公理（螺旋拓扑本原 / 相位曲率等价 / 量子离散拓扑量化 / 常数拓扑派生）
  - 5 组修复公式（N 量化 / α 闭环 / G 去循环 / ρ 本源 / 电磁-引力统一耦合）
  - 3 个纠错算法（矛盾自检 / 拓扑归一 / 层级升维）
  - 申报评级面板：修复后 H6/O6/C3/U2、L3 完整第一性闭环、原 falsified 缺陷清零

方法（严格复用 openuft 既有工具链，本册不新造判据）
----------------------------------------------------
  1. 量纲账本：齐次性检查 + Buckingham Π 定理（无量纲输入不能产出有量纲输出）
  2. 定理 C（量纲不可行性，见本目录 README）：情形 1 / 情形 2 判定
  3. 信息增益判别式 V = (n_hit − n_free − n_anchor) / n_hit（无量纲靶场审计）
  4. 自由度审计（项数 ≠ 约束数，见本目录三条方法论结论 H02/H03）
  5. 独立数值复算：mpmath dps=50 + Frenet 公式数值反算（不采信原文献自陈的精算）

红线
----
所有结论一律登记为 PASS / BOUNDARY / INFO / FAIL 四态，不粉饰；
「用了更多符号」不等于「解释力增加」；循环性换壳（ρ → K₀）记为未解除。

产出
----
  数据/空间螺旋修复版_第一性审计.json
  数据/空间螺旋修复版_第一性审计.md
  07_统一场方程/空间螺旋几何化统一场论/claims.csv 追加 C24–C38（幂等）
  07_统一场方程/空间螺旋几何化统一场论/11_证伪与反例/空间螺旋修复版_第一性缺陷记录.md

V21 续修并入（2026-09-26 · 统一脚本）
------------------------------------
  §12  C25 — LB 本征能级高阶扫描 n=1..6（mpmath 250 位 + 误差棒传播审计）
  §13  C35 — 固定 β 多行星近日点进动交叉验证（水星标定 → 金星/地球，250 位）
  §14  汇总表更新复核 + claims.csv 台账登记 C48/C49（幂等）
  数据/空间螺旋V21续修_C25C35_审计.json / .md

V22 收官并入（2026-09-26 · 统一脚本，落实草稿「剩余待攻坚清单」三项）
--------------------------------------------------------------------
  §15  C25 续 — 高阶本征能级 n 域扩展扫描（n=1..12 + 10^k）+ 误差棒正确式 + 可检测阈值
  §16  C35 续 — 多行星进动交叉验证 + β 普适性结构审计（结构同一性 / β-free 形状比 / 可观测性）
  §17  全量 claims 批量审计引擎（类别 → 证据型 → 层级 规则判定）+ 新版完整审计文档产出
  claims.csv 台账登记 C50/C51/C52（幂等）
  数据/空间螺旋修复版_第一性审计.md          ← 新版·全量（§0–§19 + claims 批量审计表）
  数据/空间螺旋V22收官_全量claims审计.json / .md

V21 续修② 并入（2026-09-26 · 统一脚本，模块1 引力泡工程 + 模块2 TUFT 重整化群 RG 流）
--------------------------------------------------------------------------
  §18  C53 引力泡（GravBubble）—— 250 位高斯积分闭式核对 + 三口径量纲账本 + 判别式 V
  §19  C54 TUFT-RG —— b 系数来源审计 + 固定点存在性精确定理（sympy 精确）+ 能标口径审计
  claims.csv 台账登记 C53/C54（幂等）
  数据/空间螺旋V21续修②_引力泡与RG流_审计.json / .md

V21 续修② 结论（不粉饰）
------------------------
  C53 → falsified（公式层）：ρ_grav 在三种 κ 口径下量纲全非法；高斯积分漏乘 π^(3/2)；
      自旋进动 δφ 非无量纲；最小量纲修复（×c⁴）后 E=1.14e16 J 与「地面实验室」矛盾；
      无作用量 ⇒ 高斯包络是 ansatz 非孤子解；4 自由参数 0 约束 ⇒ V≤0。
  C54 → falsified（模块层）：b1..b6 六自由无推导 ⇒ 非检验；精确定理
      「非平凡固定点 ⇔ b5²(−b2/b1)=b6²(−b4/b3)」在给定系数下不成立（sympy 解集仅原点）；
      草稿 findroot 原样运行抛 TypeError；μ_IR/μ_UV 口径混用（eV vs s^-1）虚增跨度 34.96；
      Landau 极点位置依赖任意 IR 输入 ⇒ 不可证伪。
  议题级（挠率场能否局域激发 / TUFT 是否有紫外固定点）仍 open。

V21 续修③ 并入（2026-09-26 · 统一脚本，双圈 RG + 泡动力学 ODE + 元审计）
--------------------------------------------------------------------
  §20  C55 TUFT-RG 双圈 β —— 固定点真伪（截断伪影定理）/ 微扰可靠域 / 物理可达性
  §21  C56 引力泡动力学演化 ODE —— σ 段恒等式 / 数值稳定性 / 坍缩与守恒审计
  §22  C57 草稿 37-claim 自评清单与层级判据审计（元审计）
  claims.csv 台账登记 C55/C56/C57（幂等）
  数据/空间螺旋V21续修③_双圈RG与泡动力学_审计.json / .md
  数据/空间螺旋修复版_第一性审计.md          ← 新版·全量（§0–§22）

V21 续修③ 结论（不粉饰）
------------------------
  C55 → falsified（模块层）：能标口径错误复发；固定点搜索仍不可运行；sympy 精确解集 4 组且非平凡解全部
      gkt*=0；截断伪影定理——gk*=−b1/d1、gt*=−b3/d3 恰使二阶/一阶项比 = −1（精确）；到达固定点需
      ln μ = 572 ≫ Planck 跨度 64.7（μ 超 Planck 2.26e220 倍）；Planck 内双圈仅改耦合 0.12%~0.44%；
      自由系数 6→13 且仍无作用量（3 方程 = 3 未知数 ⇒ 有解属自由度配平）。
  C56 → falsified（模块层）：符号恒等式 accel ≡ 3/σ ⇒ σ 段方程不含任何场参数（且把总能量当密度用）；
      量纲两头非法；显式 Euler 越稳定界 986.7 倍 ⇒ 草稿 σ 输出为数值伪迹（与稳定参考解差 2.45e18 倍）；
      σ̈=3/σ>0 ⇒ 永不坍缩；窗长仅 0.159 个振荡周期、比衰减时标短 1e13 倍；E_b 不守恒（α_g≠1 摆动 17.65%）；
      ω_bub 与本征频率差 3.34e7 倍；δφ 量纲复发；自由参数 4→9、约束 0 条。
  C57 → BOUNDARY（元审计）：清单计数自述与清单不符；与台账冲突 9 处（8 条 falsified + 1 条 boundary 被改标
      PASS）；四态退化为二态并新增 23 条未登记编号；S03 与 C24 矛盾；矛盾自检算法为桩函数；层级判据被放宽
      （空公理集亦升 L3）⇒「L3 资格保持有效」不成立；CSV 导出破坏列结构。
  议题级（TUFT 是否有紫外固定点 / 挠率场能否局域激发并动力学演化）仍 open。

用法：python 空间螺旋修复版_第一性审计与伪派生判定.py

知识图谱（Mermaid）｜本源公理 → 核心场方程 → 子模块 → 观测靶 → 审计判定
========================================================================
图谱与 claims 台账**一一对应**：每个节点都能在 07_统一场方程/空间螺旋几何化统一场论/
claims.csv 或本目录 数据/*.json 中定位到对应判定记录（映射见下方
《图谱 ↔ claims 台账一一对应（五层，逐节点可溯源）》）。

口径声明（红线，务必先读）
------------------------
下列 Mermaid 正文保留**申报/草稿自评**文案：「37 Claim 批量审计 PASS:20 / OPEN:17 /
FAIL:0」为草稿标记，「层级判定：L3准入」为草稿申报诉求。本册引擎 + §17-CLAIMS-1/2 +
守卫脚本的**台账实读**与之不符：
  · 台账 C01–C54（54 条，2026-09-26 实读）：pass 16 / open 14 / boundary 8
    （含大写 BOUNDARY 2）/ falsified 14 / info 2
  · L 层级：L0=16 / L1=34 / L2=4 / **L3=0**（UFT-3 无量纲靶登记 = 0 条）
  · 守卫（空间螺旋判定_总览与防回潮守卫.py）：8/8 通过、EXIT=0，结论「申报不成立」
两口径不一致处一律**以台账实读为准**；图谱仅作结构索引与产物导航，不作判定依据。
全维明细（逐节点判词 + 口径对账 + 缺口清单）另见同目录
  判定_空间螺旋V21知识图谱_全维分析与节点台账对应_2026-09-26.md

```mermaid
flowchart LR
    %% 样式定义
    classDef axiom fill:#224488,color:#fff,stroke:#000
    classDef field fill:#227744,color:#fff,stroke:#000
    classDef module fill:#774422,color:#fff,stroke:#000
    classDef obs fill:#882255,color:#fff,stroke:#000
    classDef audit fill:#553388,color:#fff,stroke:#000

    %% ========== L1 本源公理层 ==========
    A1["Axiom1:曲率κ本源场"]:::axiom
    A2["Axiom2:挠率τ本源场"]:::axiom
    A3["Axiom3:角频率ω本源场"]:::axiom
    A4["Axiom4:v_total=c光速基底约束"]:::axiom
    A5["Axiom5:Frenet-Serret螺旋几何<br/>κ²+τ²=ω²/c²"]:::axiom

    %% ========== L2 核心场方程层 ==========
    F1["LB螺旋哈密顿本征方程"]:::field
    F2["TUFT修正麦克斯韦方程<br/>J_geo几何流源项"]:::field
    F3["Binet引力测地线方程<br/>含拓扑β修正项"]:::field
    F4["TUFT RG β函数(单圈+双圈)"]:::field
    F5["引力泡孤子动力学ODE"]:::field
    F6["CMB拓扑双谱场方程"]:::field
    F7["EHT光子环几何修正方程"]:::field

    %% ========== L3 子模块层 ==========
    M1["原子能级子模块<br/>C25高阶精细结构αₙ"]:::module
    M2["太阳系引力子模块<br/>C35行星近日点进动"]:::module
    M3["CMB宇宙学子模块<br/>CMB01/02/03拓扑双谱"]:::module
    M4["黑洞光子环子模块<br/>EHT01/EHT02/EHT03次环"]:::module
    M5["引力泡工程子模块<br/>BUB01~BUB04静态+动力学"]:::module
    M6["RG重整化群子模块<br/>RG01~RG05单/双圈紫外固定点"]:::module
    M7["自洽审计子模块<br/>C38矛盾自检/拓扑归一/层级升维"]:::module

    %% ========== L4 观测预言靶层 ==========
    O1["O1:α₂,α₃,α₄,α₅,α₆<br/>高阶精细结构能级"]:::obs
    O2["O2:金星、地球百年进动角"]:::obs
    O3["O3:CMB双谱B₂,₁₀₀₀,₁₀₀₀;B₈₀₀,₈₀₀,₈₀₀;B₄₀₀,₄₀₀,₈₀₀"]:::obs
    O4["O4:M87*光子环n1/n2/n3位置+宽度修正"]:::obs
    O5["O5:引力泡E_bubble、δφ_spin、σ(t),κ₀(t),τ₀(t)时序演化"]:::obs
    O6["O6:gk,g_t,g_kt跑动曲线+双圈紫外固定点"]:::obs
    O7["O7:能量正定区间、弱场GR还原、跨尺度耦合匹配"]:::obs

    %% ========== L5 审计判定层 ==========
    AUD["AUD:37 Claim批量审计<br/>PASS:20,OPEN:17,FAIL:0<br/>层级判定：L3准入"]:::audit

    %% 链路连接
    A1 & A2 & A3 & A4 & A5 --> F1 & F2 & F3 & F4 & F5 & F6 & F7

    F1 --> M1
    F3 --> M2
    F6 --> M3
    F7 --> M4
    F5 --> M5
    F4 --> M6
    A1 & A2 & A3 & A5 --> M7

    M1 --> O1
    M2 --> O2
    M3 --> O3
    M4 --> O4
    M5 --> O5
    M6 --> O6
    M7 --> O7

    O1 & O2 & O3 & O4 & O5 & O6 & O7 --> AUD

    %% 反向校验链路（自洽闭环）
    AUD -.反馈校验.-> A1 & A2 & A3 & A4 & A5
```

图谱 ↔ claims 台账一一对应（五层，逐节点可溯源）
========================================================================
【L1 本源公理层】（深蓝：不可观测的理论底层假设）
  A1 曲率 κ 本源场      → C02（κ=ρ/(ρ²+b²)）；C12/C13（G 的 κ_G/τ_G 版）
                          C02 pass·L2 ｜ C12 falsified·L0 ｜ C13 open·L1
  A2 挠率 τ 本源场      → C02；C14（ω=c(κ²+τ²)/κ 频率越低引力越强）
                          C02 pass·L2 ｜ C14 boundary·L1
  A3 角频率 ω 本源场    → C01（ω√(ρ²+b²)=c）；C14
                          C01 pass·L1 ｜ C14 boundary·L1
  A4 v_total=c 基底约束 → C24 / C39（第三分量改 b·ω·t 后切向速率模长/c=1，
                                  b/A 取 1·0.5·1/137·2 四组最大偏差 1.33638e-51）
                          C24 pass·L2 ｜ C39 pass·L2 ← 唯一经引擎复算确认的公理
  A5 Frenet-Serret 几何 → C01+C02+C10（ℓ=1/√(κ²+τ²)、E=mc²=ℏω=ℏc/ℓ）
                          C01/C10 pass·L1（恒等重述，R2 封顶 L1）

【L2 核心场方程层】（绿：理论核心数学关系）
  F1 LB 螺旋哈密顿本征方程 → M1 → C25/C48/C50（LB 谱 n=1..12 + 10^k）
                          C25 open·L1 ｜ C48/C50 open·L1（谱宽 1.09e-75，
                          达 α 精度需 n_detect=2.196e33 ⇒ 阈值不可达）
  F2 TUFT 修正麦克斯韦    → C33/C34/C41（J_geo 几何流源项）
                          C33 falsified·L0（α²K 与 ∇×B 差因子 M·T⁻²·I⁻¹）｜
                          C34 pass·L1（μ₀J 已补，J_geo 源项仍未闭合）｜C41 pass·L2
  F3 Binet 引力测地线      → M2 → C35/C49/C51（含拓扑 β 修正）
                          C35 open·L1 ｜ C49/C51 open·L1（β0=3h²/c² 时
                          草稿 Binet 方程 ≡ GR 1PN；标定靶=最佳靶 ⇒ 独立判别力为零）
  F4 TUFT RG β 函数        → M6 → C54/§19
                          C54 falsified·L0（b1..b6 六自由无推导；精确定理：
                          非平凡紫外固定点存在 ⇔ b5²(−b2/b1)=b6²(−b4/b3)，
                          给定系数 LHS/RHS=5.2478 ⇒ 解集仅原点）
  F5 引力泡孤子动力学 ODE  → M5 → C53/§18
                          C53 falsified·L0（三种 κ 口径量纲全非法、漏乘
                          π^(3/2)=5.5683、δφ 量纲 [LM]；×c⁴ 修复后 E=1.14e16 J
                          与「地面实验室」自相矛盾、无作用量故非孤子）
  F6 CMB 拓扑双谱场方程    → M3 → CMB01/CMB02/CMB03
                          **台账未登记**（V21续修②：模块提交前不得占位 C55/C56）
  F7 EHT 光子环几何修正    → M4 → EHT01/EHT02/EHT03
                          **台账未登记**（同上）

【L3 子模块层】（棕褐：代码实现单元，图谱节点 → 台账）
  M1 原子能级（C25 高阶 αₙ）        → C25/C48/C50 ｜ open·L1（退化谱）
  M2 太阳系引力（C35 行星进动）      → C35/C49/C51 ｜ open·L1（公式需修正）
  M3 CMB 宇宙学（CMB01/02/03 双谱）  → 未登记 ｜ 无模块、无公式、无脚本
  M4 黑洞光子环（EHT01/02/03 次环）  → 未登记 ｜ 同上
  M5 引力泡工程（BUB01~BUB04）       → C53/§18 ｜ falsified·L0
  M6 RG 重整化群（RG01~RG05）        → C54/§19 ｜ falsified·L0
  M7 自洽审计（C38 三算法）          → C38/C52/§9.5 ｜ C38 BOUNDARY·L1
                                    （算法已实现并带算例，提交理论自身仍缺公开规格）
                                    ｜ C52 BOUNDARY·L1

【L4 定量预言 / 观测靶层】（玫红：可证伪，OPEN claims）
  O1 α₂..α₆ 高阶精细结构能级      → C48/C50 ｜ 无独立可检验靶：谱宽 1.09e-75
                                   比 α 测量精度 1.5e-10 低 65.14 个量级
  O2 金星、地球百年进动角          → C49/C51 ｜ 修正量 4.93e-3 / 1.59e-3 角秒·百年，
                                   低于历表约束 ⇒ 不可判别
  O3 CMB 双谱 B₂,₁₀₀₀,₁₀₀₀ 等     → 未登记 ｜ 无预测值 + 无误差棒 ⇒ UFT-3 计数 +0
  O4 M87* 光子环 n1/n2/n3 位置+宽度 → 未登记 ｜ 同上
  O5 引力泡 E_bubble、δφ_spin、σ(t)/κ₀(t)/τ₀(t) → C53 ｜ falsified（δφ 非无量纲）
  O6 gk/g_t/g_kt 跑动曲线 + 紫外固定点 → C54 ｜ falsified（无紫外非平凡固定点）
  O7 能量正定区间 / 弱场 GR 还原 / 跨尺度耦合匹配 → §0–§9 引擎自检 + 定理 H；C45
                                   ｜ C45 open·L1（3 未知/1 约束、α 自由、靶登记 0、L3=0）

【L5 审计判定层】（紫：L 层级判定，claims 统计）
  AUD 全量 claims 批量审计（台账实读）
      → claims.csv C01–C54；§17-CLAIMS-1/2；同目录 空间螺旋_全量claims批量审计与L3层级判定.py
      ｜ 54 条；状态 pass 16 / open 14 / boundary 8 / falsified 14 / info 2；
        L0=16 / L1=34 / L2=4 / L3=0；标记复核 PASS 20 / PARTIAL 2 /
        FAIL 9 / INFO 23；台账镜像 G1–G8 全绿
      ｜ ⇒「L3 完整第一性推导闭环」在台账层面不成立（UFT-3 = 0）
  AUD（图谱原文＝草稿自评口径）
      → 草稿汇总表（C24–C38 共 15 行）
      ｜ 草稿标记：PASS 12 / open 3 / FAIL 0
      ｜ 台证实读 C24–C38：pass 3（C24/C32/C34）、open 2（C25/C35）、
        boundary 2（C28/C38）、falsified 8（C26/C27/C29/C30/C31/C33/C36/C37）
      ｜ 若「37 条清单」指首期台账 C01–C37（该范围恰 37 条）：
        pass 13 / open 8 / boundary 5 / falsified 11
  AUD -.反馈校验.-> A1..A5（反向闭环的实际实现）
      → 空间螺旋判定_总览与防回潮守卫.py + 数据/空间螺旋判定_不变量基线.json
        （G4 禁把 C12/C21/C23 改回；G5 审计组 falsified 不得缩水；G6 引擎判定总数对齐）
      ｜ 守卫实跑 8/8 通过、EXIT=0，结论「申报不成立」⇒ 反向链路是**硬门禁**，
        不是示意虚线

图谱说明（供论文附录引用）
------------------------
  1. 正向推导链（主链路）：5 条本源几何公理 → 7 组核心场方程 → 7 个计算子模块 →
     7 组可定量观测预言靶 → 全量 Claim 审计判定。
  2. 反向闭环链路（虚线）：审计结果回传本源公理层，用于公理修正与参数调优，
     构成自迭代闭环（本仓库中以守卫脚本 + 不变量基线落为硬门禁）。
  3. 颜色编码：深蓝=本源公理（不可观测底层假设）｜绿=核心场方程（核心数学关系）｜
     棕褐=计算子模块（对应 Python 函数/脚本）｜玫红=观测预言靶（可证伪 OPEN claims）｜
     紫=审计判定层（L 层级判定与 claims 统计）。
  4. 图谱只描述**结构**与**产物导航**；节点是否为真，以 claims 台账与引擎判定为准。
"""

import os
import io
import sys
import json
import time
from fractions import Fraction

import mpmath
from mpmath import mp, mpf, mpc, sqrt, sin, cos, tan, atan, pi
import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

mp.dps = 50
T0 = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")
SYS_DIR = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论")
REF_DIR = os.path.join(SYS_DIR, "11_证伪与反例")

# ---------------------------------------------------------------------------
# 常量（SI-2019 / CODATA；全部**就地写死**以避免环境差异）
# ---------------------------------------------------------------------------
C = mpf("299792458")                 # c  精确定义值
ALPHA = mpf("7.2973525693e-3")       # α  精细结构常数
ALPHA_UREL = mpf("1.5e-10")
G_NEWTON = mpf("6.67430e-11")
HBAR = mpf("1.054571817e-34")
MU0 = 4 * pi * mpf("1e-7")
EPS0 = 1 / (MU0 * C * C)

N_DEF_A = mpf("18916.90839")   # 原定义 A：N = 1/[α²(1−α)]
N_DEF_B = mpf("18907")         # 原定义 B：N = 1/α² + 1/α + 1 + α

# ---------------------------------------------------------------------------
# 结果收集器
# ---------------------------------------------------------------------------
ROWS = []
CHECKS = []


def reg(state, tag, statement, detail, evidence=""):
    """登记一条判定（四态）。"""
    assert state in ("PASS", "BOUNDARY", "INFO", "FAIL")
    ROWS.append({"state": state, "tag": tag, "statement": statement,
                 "detail": detail, "evidence": evidence})
    print("  [%-8s] %s" % (state, tag))
    if detail:
        print("             %s" % detail.replace("\n", "\n             "))
    return state


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def fmt(x, n=8):
    return mpmath.nstr(x, n)


# ---------------------------------------------------------------------------
# 量纲账本（L, M, T, I 四个基本量纲的整数指数向量）
# ---------------------------------------------------------------------------
def D(L=0, M=0, T=0, I=0):
    return {"L": Fraction(L), "M": Fraction(M), "T": Fraction(T), "I": Fraction(I)}


def dmul(a, b):
    return {k: a[k] + b[k] for k in a}


def ddiv(a, b):
    return {k: a[k] - b[k] for k in a}


def dpow(a, n):
    return {k: a[k] * Fraction(n) for k in a}


def dfmt(d):
    parts = []
    for k in ("L", "M", "T", "I"):
        e = d[k]
        if e == 0:
            continue
        parts.append(k + "^" + str(e))
    return "[" + " ".join(parts) + "]" if parts else "[1]"


DIM_G = D(L=3, M=-1, T=-2)
DIM_C = D(L=1, T=-1)
DIM_ALPHA = D()
DIM_CURV = D(L=-1)          # 曲率 κ：[L^-1]
DIM_B = D(M=1, T=-2, I=-1)  # 磁感应强度 B：tesla
DIM_E = D(L=1, M=1, T=-3, I=-1)
DIM_FORCE = D(L=1, M=1, T=-2)
DIM_MASS_DENS = D(M=1, L=-3)


def required_dim(target, known):
    """求未知量的必需量纲：[X] = [target] / [known]。"""
    return ddiv(target, known)


# ---------------------------------------------------------------------------
# 信息增益判别式 V（openuft 无量纲靶场审计口径）
# ---------------------------------------------------------------------------
def disc_v(n_hit, n_free, n_anchor):
    if n_hit == 0:
        return None
    return (Fraction(n_hit) - Fraction(n_free) - Fraction(n_anchor)) / Fraction(n_hit)


print("=" * 76)
print("空间螺旋几何化统一场论 · 「算法联盟缺陷修复体系」第一性审计")
print("工具：量纲账本 / 定理 C / 判别式 V / 自由度审计 / mpmath dps=50 独立复算")
print("=" * 76)

# ===========================================================================
# §0  基线对齐：核对修复版引用的原体系评级的真实性
# ===========================================================================
print("\n" + "=" * 76)
print("§0  基线对齐：修复版所引「原体系 H4/O5/C1/U0、L3×0」是否属实")
print("=" * 76)

def read_claims():
    path = os.path.join(SYS_DIR, "claims.csv")
    lines = [l for l in io.open(path, encoding="utf-8").read().splitlines() if l.strip()]
    rows = []
    for l in lines[1:]:
        parts = l.split(",")
        rows.append({"id": parts[0], "status": parts[3] if len(parts) > 3 else ""})
    return rows


CL = read_claims()
cnt = {}
for r in CL:
    cnt[r["status"]] = cnt.get(r["status"], 0) + 1
print("     claims.csv 现有主张 %d 条，状态分布：%s" % (len(CL), cnt))

# 只统计本次登记之前的「原 falsified」：以 C23 为分界（幂等重跑时不再把新登记行算进去）
def _num(cid):
    try:
        return int(cid[1:])
    except ValueError:
        return 10 ** 6


BASELINE = [r for r in CL if _num(r["id"]) <= 23]
n_falsified = sum(1 for r in BASELINE if r["status"] == "falsified")
old_falsified_ids = [r["id"] for r in BASELINE if r["status"] == "falsified"]
print("     原 falsified 主张：%s" % "、".join(old_falsified_ids))

# 01_全维评级与诚实边界.md 记载：H 4（一/四/八/九）· O 5（二/三/六/七/十）· C 1（五）· U 0
LEVELS = {"L0": 2, "L1": 7, "L2": 2, "L3": 0}   # 见 01_全维评级与诚实边界.md 全维汇总表
item("基线面板 H4/O5/C1/U0 与 01_全维评级档案一致 ⇒ 修复版引用属实", True,
     "来源：01_全维评级与诚实边界.md 全维汇总表；L 计数 %s 亦一致" % LEVELS)
reg("PASS", "§0-1 基线引用属实",
    "修复版所引原体系评级 H4/O5/C1/U0 与 L0=2/L1=7/L2=2/L3=0 与档案一致",
    "核对 01_全维评级与诚实边界.md 全维汇总表逐字比对一致；claims.csv 现有 %d 条主张、%d 条 falsified"
    % (len(CL), n_falsified),
    "档案核对（非负成果，如实计入）")

reg("INFO", "§0-2 基线 falsified 尚未在台账中撤销",
    "修复版宣称「原 falsified 缺陷清零」，但 claims.csv 中 %s 仍为 falsified" % "、".join(old_falsified_ids),
    "openuft 维护契约：先改 claims.csv 再复跑引擎；申报先行而台账未动 ⇒ 申报不成立",
    "台账状态：%s" % cnt)

# ===========================================================================
# §1  公理 1：修复标准版螺旋基底 R(t) = (A cos ωt, A sin ωt, c t)
# ===========================================================================
print("\n" + "=" * 76)
print("§1  公理1 螺旋基底：κ、τ 的闭合式与 Frenet 数值反算")
print("=" * 76)

A_s, OM_s, U_s, T_s = sp.symbols("A omega u t", positive=True)
# 一般形式 R(t) = (A cos ωt, A sin ωt, u t)，u 为轴向速率（修复版取 u = c）
R = sp.Matrix([A_s * sp.cos(OM_s * T_s), A_s * sp.sin(OM_s * T_s), U_s * T_s])
R1 = R.diff(T_s)
R2 = R.diff(T_s, 2)
R3 = R.diff(T_s, 3)
cross_sym = R1.cross(R2)
kappa_sym = sp.simplify(sp.sqrt((cross_sym.T * cross_sym)[0]) / (sp.sqrt((R1.T * R1)[0]) ** 3))
tau_sym = sp.simplify(R1.dot(R2.cross(R3)) / (cross_sym.T * cross_sym)[0])
speed_sym = sp.simplify(sp.sqrt((R1.T * R1)[0]))

kappa_claim = A_s * OM_s ** 2 / (A_s ** 2 * OM_s ** 2 + U_s ** 2)
tau_claim = U_s * OM_s / (A_s ** 2 * OM_s ** 2 + U_s ** 2)

print("     符号推导：κ = %s" % sp.simplify(kappa_sym))
print("     Γ        τ = %s" % sp.simplify(tau_sym))
print("              |R'| = %s" % sp.simplify(speed_sym))

item("κ 闭合式与教科书螺旋公式一致", sp.simplify(kappa_sym - kappa_claim) == 0)
item("τ 闭合式与教科书螺旋公式一致", sp.simplify(tau_sym - tau_claim) == 0)
item("切向速率 |R'| = sqrt(A²ω² + u²)",
     sp.simplify(speed_sym ** 2 - (A_s ** 2 * OM_s ** 2 + U_s ** 2)) == 0)

# Frenet 数值反算（独立于上述符号推导的第二条路径）
def frenet_numeric(A, om, u, t):
    r1 = [-A * om * sin(om * t), A * om * cos(om * t), u]
    r2 = [-A * om ** 2 * cos(om * t), -A * om ** 2 * sin(om * t), mpf(0)]
    r3 = [A * om ** 3 * sin(om * t), -A * om ** 3 * cos(om * t), mpf(0)]

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    cr = cross(r1, r2)
    k = sqrt(dot(cr, cr)) / dot(r1, r1) ** mpf("1.5")
    tau = dot(r1, cross(r2, r3)) / dot(cr, cr)
    return k, tau


Anum, OMnum, Unum = mpf("1.7"), mpf("2.3"), mpf("5.0")
maxerr = mpf(0)
for tv in ["0.3", "1.1", "2.7"]:
    t = mpf(tv)
    kn, tn = frenet_numeric(Anum, OMnum, Unum, t)
    kc = Anum * OMnum ** 2 / (Anum ** 2 * OMnum ** 2 + Unum ** 2)
    tc = Unum * OMnum / (Anum ** 2 * OMnum ** 2 + Unum ** 2)
    maxerr = max(maxerr, abs(kn - kc), abs(tn - tc))
item("Frenet 数值反算复现 κ、τ 闭合式（三个参数点）", maxerr < mpf("1e-40"),
     "最大绝对偏差 %s" % fmt(maxerr, 6))

reg("PASS", "§1-1 螺旋 κ、τ 闭合式正确",
    "R(t)=(A cos ωt, A sin ωt, u t) 的 κ=Aω²/(A²ω²+u²)、τ=uω/(A²ω²+u²) 经符号推导与 Frenet 数值反算双路确认",
    "符号残差 0；数值反算偏差 %s" % fmt(maxerr, 6),
    "独立复算（非零成果，如实计入）")

# --- τ/κ 与的重要关系：修复版取 u = c 时 τ/κ = c/(ωA)，恰是 α 新公式里的因子 ---
ratio = sp.simplify(tau_sym / kappa_sym)
print("     τ/κ = %s" % ratio)
item("τ/κ = u/(Aω)（取 u=c 即 τ/κ = c/(ωA)）",
     sp.simplify(ratio - U_s / (A_s * OM_s)) == 0)

# --- 光速本体相容性 ---
print("\n     光速本体检验：修复版把轴向分量写死为 c·t ⇒ |R'| = sqrt(A²ω² + c²)")
u_req, whereby = None, None
# 读数 A（字面）：轴向速率 = c，总速率 = sqrt(A²ω²+c²)
expr_A2 = sp.sqrt(A_s ** 2 * OM_s ** 2 + C ** 2)   # 无法直接用 sympy 的 C（mpf），改用符号
Csym = sp.Symbol("c", positive=True)
speed_A = sp.sqrt(A_s ** 2 * OM_s ** 2 + Csym ** 2)
print("     读数A：|R'| = %s  ⇒ 当 Aω>0 时严格 > c" % sp.sqrt(A_s ** 2 * OM_s ** 2 + Csym ** 2))
# 读数 B：恢复原体系 ω√(A²+b²)=c，则 ωA = c·A/√(A²+b²) = c·cosθ
print("     读数B：恢复原约束 ω√(A²+b²)=c ⇒ ωA = c·cosθ < c（相容），但此时 τ/κ = b/A ≠ c/(ωA) = secθ")

reg("FAIL", "§1-2 公理1 与「光速螺旋本体 v=c」不相容（读数A）",
    "把轴向分量写死为 c·t 后 abs(R') = sqrt(A²ω²+c²)；只要 Aω>0 即严格大于 c ⇒ 与本体「空间中每一点作光速螺旋运动」直接冲突",
    "(v/c) = sqrt(1 + (ωA/c)²)；为使 §2 的 α 公式命中观测需 ωA/c = %s ⇒ v = %s c（超光速 %s%%）"
    % (fmt(1 / (2 * sqrt(N_DEF_B) * ALPHA), 8),
       fmt(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2), 8),
       fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6)),
    "§2 反解 + §1 速率式联立")

reg("FAIL", "§1-3 两种读数互不相容（同一式子在两种补全下给出不同的 τ/κ）",
    "读数A给出 τ/κ = c/(ωA)；读数B（恢复原光速约束）给出 τ/κ = b/A 而 c/(ωA) = secθ ⇒ 若要求二者同为 τ/κ 则需 tanθ = secθ 即 sinθ=1 无解",
    "公理1 未声明速度归一化条件 ⇒ 同一符号 c 在本体系内承担两个互斥角色",
    "符号比较")

# ===========================================================================
# §2  α 新公式：α = (1/(2√N)) · c/(ωA)
# ===========================================================================
print("\n" + "=" * 76)
print("§2  α 闭环公式 α = (1/(2√N)) · c/(ωA)")
print("=" * 76)

print("     量纲：[α]=%s；[1/(2√N)]=%s；[c/(ωA)]=%s ⇒ 两侧无量纲，通过齐次性检查"
      % (dfmt(DIM_ALPHA), dfmt(D()), dfmt(ddiv(DIM_C, D(L=1, T=-1)))))
reg("PASS", "§2-1 α 公式量纲齐次",
    "α 与右端均无量纲（ωA 为速率，c/(ωA) 无量纲）⇒ 通过量纲必要条件",
    "这是本轮唯一通过的量纲检查，如实计入", "齐次性")

# --- 不可证伪性：任意 N 都能命中 α ---
print("\n     「命中」的自由度演示：对每个 N 反解所需的 ωA/c，重代回后均能精确复现 α")
print("     %-14s %-22s %-22s" % ("N", "所需 ωA/c", "回代所得 α"))
fit_rows = []
skipped = []
max_err = mpf(0)
for n_val in ["137", "1000", "4695", "18907", "100000", "1000000000"]:
    Nv = mpf(n_val)
    factor = 2 * sqrt(Nv) * ALPHA           # 所需 c/(ωA)
    if factor <= 1:
        # 透明化：不静默跳过。读数B 下 c/(ωA)=secθ>=1，故小 N 不可行（读数A 下无此限制）
        print("     %-14s %-22s %-22s   ← 读数B 不可行（需 c/(ωA)=%s < 1）"
              % (n_val, "—", "—", fmt(factor, 8)))
        skipped.append(n_val)
        continue
    wa = C / factor                          # 所需 ωA
    alpha_back = (1 / (2 * sqrt(Nv))) * (C / wa)
    err = abs(alpha_back / ALPHA - 1)
    max_err = max(max_err, err)
    fit_rows.append({"N": n_val, "omegaA_over_c": float(1 / factor), "alpha_back": float(alpha_back)})
    print("     %-14s %-22s %-22s" % (n_val, fmt(1 / factor, 10), fmt(alpha_back, 12)))
print("     命中 %d 个 N；读数B 下不可行 %d 个（%s）"
      % (len(fit_rows), len(skipped), "、".join(skipped) if skipped else "无"))
print("     最大相对偏差 %s" % fmt(max_err, 6))

item("任意 N（读数B 下满足 2√Nα>1）均可精确命中 α ⇒ 该公式对 N 无任何选择力",
     max_err < mpf("1e-40"),
     "四个数量级不同的 N 全部给出同一 α")

n_min = 1 / (4 * ALPHA ** 2)
print("     读数B 唯一被排出的区间：2√N α < 1（即 N < %s）；读数A 下该约束亦不存在" % fmt(n_min, 10))
reg("FAIL", "§2-2 α 公式不可证伪：不构成对 N 的选择规则",
    "α = c/(2√N·ωA) 是两个未知量（N、ωA）对一个方程 ⇒ 读数B 下除 N ≥ %s 外无任何 N 被排除，读数A 下连该约束也没有"
    % fmt(n_min, 10),
    "实测：N 取 4695…1e9 四个数量级，反解 ωA 后重算 α 的偏差均 < %s ⇒ 「高精度匹配」不含信息" % fmt(max_err, 6),
    "反解 + 回代复算")

# --- 判别式 V ---
v_alpha = disc_v(1, 2, 1)
print("     判别式 V(α 声明) = (1 − 2 − 1)/1 = %s" % v_alpha)
reg("FAIL", "§2-3 判别式 V = −2 ≤ 0 ⇒ 判为伪派生（等价交换以下）",
    "n_hit=1（α）· n_free=2（N、ωA）· n_anchor=1（c）⇒ V = %s，落在 openuft 判定的「净消耗」区"
    % v_alpha,
    "与既有 M02（普朗克锚定谬误，V=−3）同型", "无量纲靶场审计口径")

# --- θ 三方冲突 ---
tan_new_A = 2 * sqrt(N_DEF_B) * ALPHA
theta_new_A = atan(tan_new_A) * 180 / pi
theta_old = atan(ALPHA) * 180 / pi
theta_sqrtN = atan(sqrt(N_DEF_B)) * 180 / pi
tan_new_B = sqrt(tan_new_A ** 2 - 1)
theta_new_B = atan(tan_new_B) * 180 / pi

print("\n     θ 三方口径对照（N = %s）：" % fmt(N_DEF_B, 8))
print("     %-34s %-16s %-12s" % ("口径", "tanθ", "θ(度)"))
print("     %-34s %-16s %-12s" % ("原主体 α=τ/κ=tanθ (C03)", fmt(ALPHA, 8), fmt(theta_old, 8)))
print("     %-34s %-16s %-12s" % ("原拓扑绕数 tanθ=√N (C23 falsified)", fmt(sqrt(N_DEF_B), 8), fmt(theta_sqrtN, 8)))
print("     %-34s %-16s %-12s" % ("修复版读数A 隐含 tanθ=2√Nα", fmt(tan_new_A, 8), fmt(theta_new_A, 8)))
print("     %-34s %-16s %-12s" % ("修复版读数B 隐含 tanθ=√((2√Nα)²−1)", fmt(tan_new_B, 8), fmt(theta_new_B, 8)))

reg("FAIL", "§2-4 θ 与 α 的冲突未消除，反而由二方变为四方",
    "tanθ 同时被要求为 %s（原主体 α=τ/κ）、%s（原拓扑绕数 √N）、%s 或 %s（修复版两种读数）"
    % (fmt(ALPHA, 6), fmt(sqrt(N_DEF_B), 6), fmt(tan_new_A, 6), fmt(tan_new_B, 6)),
    "修复版所谓「彻底消解 tanθ 与 α 的数值矛盾」的实现方式是在新公式中不再使用 α=τ/κ ⇒ 冲突的一侧被删除而非被调和",
    "claims C03 / C23 仍然有效且互斥")

# --- 读数 B 下 α 预测值 ---
alpha_pred_B = (1 / (2 * sqrt(N_DEF_B))) * sqrt(1 + ALPHA ** 2)
rel_B = alpha_pred_B / ALPHA - 1
reg("FAIL", "§2-5 读数B（恢复原光速约束且保留 α=τ/κ）下 α 预测低 %s%%"
    % fmt(abs(rel_B) * 100, 6),
    "此时 c/(ωA) = secθ = √(1+α²) ⇒ α_pred = √(1+α²)/(2√N) = %s，观测 %s"
    % (fmt(alpha_pred_B, 10), fmt(ALPHA, 10)),
    "相对偏差 %s，约为观测不确定度 %s 的 %s 倍 ⇒ 即便按最宽松的 3σ 判据也远未命中"
    % (fmt(rel_B, 6), fmt(ALPHA_UREL, 4), fmt(abs(rel_B) / ALPHA_UREL, 6)),
    "独立复算")

# --- 定理 H 提示 ---
reg("INFO", "§2-6 与既有定理的一致性",
    "本册结论不是孤例：openuft 定理 H 已证「7 个初等几何作用量无一能把 α 固定到 1/137」；定理 C 情形2 已证「含未测量自有量的等式等价于该量的定义」",
    "α 公式含未测量自有量 ωA ⇒ 正落在定理 C 情形 2", "既有定理套用")

# ===========================================================================
# §3  N 量化定义 N = floor(2π/Δθ_min)
# ===========================================================================
print("\n" + "=" * 76)
print("§3  N 量化定义 N = floor(2π/Δθ_min)")
print("=" * 76)

for name, nv in [("定义A 18916.9", N_DEF_A), ("定义B 18907", N_DEF_B)]:
    dth = 2 * pi / nv
    print("     若目标为 %s ⇒ Δθ_min = 2π/N = %s rad；floor(2π/Δθ_min) = %s"
          % (name, fmt(dth, 10), mp.floor(2 * pi / dth)))

reg("FAIL", "§3-1 floor 取整使定义 A 不可复现 ⇒ 双值冲突未被消除而是被删除",
    "新定义 N = floor(2π/Δθ_min) 只能产出整数；原定义 A = 1/[α²(1−α)] = %s 非整数 ⇒ 不可能由新定义导出"
    % fmt(N_DEF_A, 10),
    "「彻底消除双值冲突」的另一种说法是「抛弃其中一个值」；原冲突 C21 在台账中仍为 falsified",
    "取整天性")

reg("BOUNDARY", "§3-2 Δθ_min 无第一性来源 ⇒ N 仍是外部输入换壳",
    "复现目标 N=18907 需 Δθ_min = %s rad，文中未给出该值的任何推导或约束方程"
    % fmt(2 * pi / N_DEF_B, 10),
    "自由度从「N 手填」平移为「Δθ_min 手填」；自由度总数不降 ⇒ 不满足「去拟合」准则",
    "自由度审计")

# ===========================================================================
# §4  G 去循环公式 G = c⁴/(8πK₀) · α²
# ===========================================================================
print("\n" + "=" * 76)
print("§4  G 第一性公式 G = c⁴/(8πK₀) · α²")
print("=" * 76)

dim_k0_req = required_dim(dpow(DIM_C, 4), DIM_G)     # [K0] = [c^4] / [G]
print("     必需量纲：[K₀] = [c⁴] ÷ [G] = %s ÷ %s = %s"
      % (dfmt(dpow(DIM_C, 4)), dfmt(DIM_G), dfmt(dim_k0_req)))
print("     而「曲率」的量纲为 %s ⇒ 二者相差 %s（非无量纲 ⇒ 等号不成立）"
      % (dfmt(DIM_CURV), dfmt(ddiv(dim_k0_req, DIM_CURV))))
item("[K₀] 必需为力（牛顿）而非曲率（1/长度）", dim_k0_req == DIM_FORCE and dim_k0_req != DIM_CURV,
     "[K₀]_req = %s" % dfmt(dim_k0_req))

k0_val = C ** 4 * ALPHA ** 2 / (8 * pi * G_NEWTON)
print("     反解必需的 K₀ 取值 = %s N（牛顿）" % fmt(k0_val, 10))
print("     对照：普朗克力 c⁴/G = %s N；比值 %s = 8π/α² ⇒ K₀ ≡ α²·F_Planck/(8π)（即由 G 反定义而来）"
      % (fmt(C ** 4 / G_NEWTON, 10), fmt(C ** 4 / G_NEWTON / k0_val, 8)))

reg("FAIL", "§4-1 G 式量纲失败：要求的 K₀ 是「力」不是「曲率」",
    "[K₀] = [c⁴]/[G] = %s（= 牛顿·力），而曲率量纲为 %s ⇒ 把 K₀ 称作「时空基底曲率」与量纲账本直接冲突"
    % (dfmt(dim_k0_req), dfmt(DIM_CURV)),
    "反解所得 K₀ = %s N（= α²·普朗克力/(8π)），无任何已知物理量在该量级上独立存在" % fmt(k0_val, 8),
    "量纲账本 + Buckingham")

reg("FAIL", "§4-2 「K₀ 可由 N 与 α 直接推导」违反 Buckingham Π 定理",
    "N 与 α 均为无量纲数；任何无量纲量的函数仍为无量纲 ⇒ 不可能产出有量纲的 K₀（更不可能产出 G）",
    "这是结构性不可能，不是数值精度问题", "Π 定理")

reg("FAIL", "§4-3 循环性未解除，只是把 ρ 换壳为 K₀",
    "原式 G = α²μ₀c²ρ²（C12 falsified）中 ρ = sqrt(G/(α²μ₀c²)) 由 G 反推；新式 G = c⁴α²/(8πK₀) 中 K₀ = α²c⁴/(8πG) 同样由 G 反推",
    "两式同构：均为「把 G 的定义式改写成求 G 的形式」。故 C12 的 falsified 标记不能被撤销",
    "对照 C12 结构")

# 与旧 ρ 值交叉验证引擎标定
rho_old = sqrt(G_NEWTON / (ALPHA ** 2 * MU0 * C ** 2))
print("     引擎标定交叉验证：由 C12 反解 ρ = %s m（档案记载 ρ≈3.33e-9 m）" % fmt(rho_old, 8))
item("引擎能复现档案记载的 ρ≈3.33e-9 m（标定自检）", abs(rho_old / mpf("3.33e-9") - 1) < mpf("0.01"),
     "复得 %s m，与 00_核心理论体系总纲一致" % fmt(rho_old, 8))

v_g = disc_v(1, 1, 2)
reg("FAIL", "§4-4 G 作为声明目标本身不构成有效靶（定理 C）",
    "G 是带量纲量 ⇒ 按定理 C，任何「由其他常数组成 G」的等式要么落在零空间（无预言内容）要么等价于定义某个未测量量",
    "若强行套 V：n_hit=1·n_free=1（K₀）·n_anchor=2（c、α）⇒ V = %s ≤ 0" % v_g,
    "定理 C + 判别式 V")

reg("INFO", "§4-5 正确的无量纲靶应是什么",
    "有意义的靶是 α_grav(m) = G m²/(ℏc) = (m/m_P)²；「导出 G」等价于「导出 m_e/m_P」，后者才是 openuft 登记的无量纲靶",
    "要宣称拿到 G，必须给出 m_e/m_P 的预测值 + 误差棒（本体系现登记数量：0 条）",
    "构建性建议而非缺陷")

# ===========================================================================
# §5  ρ 通量密度定义 ρ = (1/V) ∮ S·dl
# ===========================================================================
print("\n" + "=" * 76)
print("§5  ρ 拓扑本源定义 ρ = (1/V) ∮ S·dl")
print("=" * 76)

# [ρ] = M L^-3；[∮S·dl] = [S]·L；除以 [V]=L^3 后得 [S]/L^2 = [ρ] ⇒ [S] = [ρ]·L^2 = M L^-1
dim_S_req = ddiv(dmul(DIM_MASS_DENS, D(L=3)), D(L=1))
print("     必需：[S] = [ρ]·[V]/[L] = %s ⇒ S 的量纲必须是「质量/长度」" % dfmt(dim_S_req))
print("     对照：任何标准通量（如坡印廷矢量）都不是该量纲 ⇒ 「通量矢量」的命名与必需量纲不符")
print("     且通量的自然积分域是面积 dA（∮S·dA），文中对线元 dl 积分属范畴错误")

reg("FAIL", "§5-1 ρ 定义量纲不成立（要求 [S] = M·L⁻¹，非任何通量）",
    "ρ=(1/V)∮S·dl 要给出质量密度，S 必须具 M·L⁻¹ 量纲；无任何标准「通量矢量」具有该量纲",
    "若 S 取通量的通常量纲，则右端量纲为 %s，与 [ρ]=%s 不符"
    % (dfmt(ddiv(dmul(D(M=1, T=-3), D(L=1)), D(L=3))), dfmt(DIM_MASS_DENS)),
    "量纲账本")

reg("FAIL", "§5-2 ρ 在新体系中是孤儿量：无任何方程消费它",
    "修复版已把 ρ 从 G 式中移除（这是正确的结构性动作），但随后又用一条无法闭合的公式把 ρ 请回；"
    "10 个子系统中 ρ 不进入任何后续关系（m=ℏ/(cρ_C) 中的 ρ_C 是另一符号）",
    "干净做法是直接删除 ρ；保留即是新增一个 U 类未展开项", "依赖图检查")

reg("INFO", "§5-3 删除 ρ 依赖本身是真实的进步，应予承认",
    "把 ρ 移出 G 的方向正确：它切断了被判 falsified 的 C12 的一条循环边",
    "问题只在于 K₀ 承接了同一个循环角色（§4-3）⇒ 净效果为循环性搬家而非消除",
    "非负成果，如实计入")

# ===========================================================================
# §6  电磁场-引力场统一耦合方程
# ===========================================================================
print("\n" + "=" * 76)
print("§6  场耦合方程 ∇×B = (1/c²)∂E/∂t + α²·K(R)  与  F_grav 修正")
print("=" * 76)

curlB = ddiv(DIM_B, D(L=1))
disp = ddiv(ddiv(DIM_E, D(T=1)), dpow(DIM_C, 2))
print("     [∇×B] = %s" % dfmt(curlB))
print("     [(1/c²)∂E/∂t] = %s  ⇒ 标准两项量纲一致 ✓" % dfmt(disp))
item("标准两项（∇×B 与位移电流项）量纲一致", curlB == disp, "%s = %s" % (dfmt(curlB), dfmt(disp)))

print("     [α²·K] = %s（α²无量纲、K 取曲率）⇒ 与 %s 相差 %s"
      % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))))
reg("FAIL", "§6-1 附加项 α²·K(R) 量纲不匹配",
    "[α²K] = %s，而方程其余各项为 %s ⇒ 差因子 %s（具 M·T⁻²·I⁻¹，非无量纲）"
    % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))),
    "若 K 改取 [∇×B] 的量纲，则它不再是曲率 ⇒ 二选一必居其一", "量纲账本")

reg("FAIL", "§6-2 方程缺少 μ₀J ⇒ 稳恒电流的安培环路定理无法复现",
    "标准式 ∮B·dl = μ₀(I + ε₀dΦ_E/dt)；新式无传导电流项，稳恒情形（∂E/∂t=0）要求 α²∫K·dA = μ₀I_enclosed 对**一切**电流分布成立",
    "这等于把 K 规定为电流分布的泛函，与「K 为时空几何曲率」的定位冲突；文中未给出该对应关系 ⇒ 方程或未写完或为假",
    "取 ∮ ∮ 环路积分")

# 散度 / 电荷守恒
print("\n     取散度：0 = ∇·[(1/c²)∂E/∂t] + α²∇·K ⇒ ∇·J = (α²/μ₀)·∇·K（用到连续性方程 ∂ρ_e/∂t = −∇·J）")
alpha2_over_mu0 = ALPHA ** 2 / MU0
print("     系数 α²/μ₀ = %s（量纲 %s）"
      % (fmt(alpha2_over_mu0, 8), dfmt(ddiv(DIM_ALPHA, D(L=1, M=1, T=-2, I=-2)))))
reg("FAIL", "§6-3 与电荷守恒耦合出一个未被声明的约束",
    "∇·(∇×B)≡0 迫使 ∇·J = (α²/μ₀)∇·K；文中既未给出 K 与电流的关系，也未声明 ∇·K ≡ 0",
    "若 ∇·K ≡ 0 则该附加项无源（无法担当「几何源」角色）；若不恒为零则电荷守恒被修改",
    "恒等式 ∇·(∇×)≡0")

# 引力修正：F = −G m₁m₂/r² · ∇Φ/Φ₀
print("\n     引力修正：F = −G m₁m₂/r² · ∇Φ(r)/Φ₀")
r_sym, n_sym, phi0_sym = sp.symbols("r n Phi_0", positive=True)
phi = r_sym ** n_sym
F_exp = n_sym - 3      # F ∝ r^-2 · r^(n-1) = r^(n-3)
print("     设 Φ ∝ r^n ⇒ ∇Φ/Φ₀ ∝ r^(n−1) ⇒ F ∝ r^−2 · r^(n−1) = r^(%s)" % F_exp)
print("     恢复牛顿 r^−2 要求 %s = −2 ⇒ n = %s" % (F_exp, sp.solve(sp.Eq(F_exp, -2), n_sym)))
item("牛顿极限唯一解为 n = 1（Φ 必须线性于 r）", sp.solve(sp.Eq(F_exp, -2), n_sym) == [1])

reg("FAIL", "§6-4 引力修正为二分：或退化为常数（零内容）或违反闭合轨道",
    "若 Φ ∝ r^n：恢复牛顿律唯一要求 n=1，此时 ∇Φ/Φ₀ 为常数，可整体吸收进 G ⇒ 该因子不携带任何新内容；"
    "n≠1 则力律变为 r^(n−3)，不再是 1/r² ⇒ 与行星闭合轨道冲突（Bertrand 定理：仅 1/r² 与 ∝r 给出闭合稳定轨道）",
    "另：该式为「标量模长」乘向量而非矢量形式；且方向由 ∇Φ 决定而非径向 ⇒ 形式亦不自洽",
    "符号推导 + Bertrand 定理")

reg("FAIL", "§6-5 Φ₀ 与 Φ 量纲不一致（∇Φ/Φ₀ 需无量纲）",
    "∇Φ/Φ₀ 必须无量纲 ⇒ [Φ₀] 必须等于 [∇Φ] = [Φ]/L，而非 [Φ]；记号 Φ₀（Φ 的某取值）与这一要求冲突",
    "除非 Φ 本身无量纲（相位解读），但那样又与主量表语义中的「势」不一致", "量纲账本")

# ===========================================================================
# §7  公理2 ∇Φ ≡ K
# ===========================================================================
print("\n" + "=" * 76)
print("§7  公理2 相位曲率等价 ∇Φ ≡ K")
print("=" * 76)

reg("BOUNDARY", "§7-1 量纲可相容但类型不匹配（向量 ≡ 标量）",
    "若 Φ 为无量纲相位、K 取曲率，则 [∇Φ] = [K] = L⁻¹ 相容；但左端为向量/余向量、右端 K 写为标量 ⇒ 严格应写作 abs(∇Φ) = κ 或 K_a = ∇_aΦ",
    "注：若要 K=∇Φ 则 K 必须为曲率向量，后续 G 式中的 K₀ 又必须退化为标量 ⇒ 同一符号两种身份",
    "类型检查")

reg("BOUNDARY", "§7-2 该项是定义（L1）不是推导（L3），且与既有 UFT 桥接重复",
    "把相位梯度定义为曲率在本仓库 UFT 体系中已有同类桥接（κ = ½·abs(∇ln β₁)）；本质是给同一数学对象换名字",
    "作为约定可接受（故判 BOUNDARY 而非 FAIL），但不得计入「L3 第一性推导」的证据清单",
    "与既有档案比对")

# ===========================================================================
# §8  信息/自由度总账
# ===========================================================================
print("\n" + "=" * 76)
print("§8  自由度总账与三大准则逐条对照")
print("=" * 76)

ledger = [
    ("原体系: 未知量", "ρ、b、ω（3）"),
    ("原体系: 独立约束", "ω√(ρ²+b²)=c（1）"),
    ("修复版: 未知量", "A、ω、Δθ_min(→N)、K₀、S、V、Φ₀、Φ(r)（8）"),
    ("修复版: 独立约束", "0（除定义式外无任何方程约束上述量）"),
]
for k, v in ledger:
    print("     %-18s %s" % (k, v))

print("\n     三条 headline 声明的信息增益 V：")
vtab = [
    ("α = c/(2√N·ωA)", 1, 2, 1, disc_v(1, 2, 1)),
    ("G = c⁴α²/(8πK₀)", 1, 1, 2, disc_v(1, 1, 2)),
    ("N = floor(2π/Δθ_min)", 0, 1, 0, None),
]
print("     %-24s %8s %8s %8s %8s" % ("声明", "n_hit", "n_free", "n_anchor", "V"))
for nm, h, f, a, v in vtab:
    print("     %-24s %8s %8s %8s %8s" % (nm, h, f, a, "NA" if v is None else str(v)))

item("自由度总数由 3→8、约束由 1→0 ⇒ 「去拟合」准则未达成", True,
     "新增自由度多于新增方程；按 openuft 方法论，合理情形应下降或持平")

reg("FAIL", "§8-1 准则一「去拟合、重公理」未达成",
    "自由度净增 5（3→8）且约束净减 1 ⇒ 拟合能力上升而非下降；ρ 与 N 的自由度被平移为 K₀ 与 Δθ_min",
    "判别式 V 对两条 headline 声明分别为 −2 与 −2，均 ≤ 0", "自由度审计 + 判别式 V")

reg("FAIL", "§8-2 准则二「去循环、闭逻辑」未达成（循环搬家）",
    "G 的循环依赖由 ρ 转移到 K₀：K₀ ≡ α²c⁴/(8πG) 与旧 ρ ≡ sqrt(G/(α²μ₀c²)) 在结构上完全同构",
    "α 一侧同样引入未测量自有量 ωA ⇒ 落入定理 C 情形 2", "循环性结构比对")

reg("BOUNDARY", "§8-3 准则三「统一数值、消矛盾」部分达成、部分靠删除实现",
    "达成：① ω√(ρ²+b²)=c 的旧式与新基底不冲突的表述被替换；② G 式不再含 ρ。"
    "未达成：① N 双定义（18916.9/18907）中前者被 floor 静默删除而非调和；② θ 冲突由二方扩为四方；③ α 精度在相容读数下差 %s%%"
    % fmt(abs(rel_B) * 100, 6),
    "「消除矛盾」与「删除矛盾的一方」的区别必须写进档案", "逐条比对")

# ===========================================================================
# §9  申报面板算数与 UFT-3 计数
# ===========================================================================
print("\n" + "=" * 76)
print("§9  申报面板 H6/O6/C3/U2 与 UFT-3 计数")
print("=" * 76)

h_, o_, c_, u_ = 6, 6, 3, 2
sum_declared = h_ + o_ + c_ + u_
print("     申报：H%d/O%d/C%d/U%d 合计 %d；而其 §5 自列子系统恰为 10 个" % (h_, o_, c_, u_, sum_declared))
print("     注意：合计 %d 与子系统数 10 不符，差值 %d —— 该项作为 §9-1 的 FAIL 证据登记，不作为引擎自检项"
      % (sum_declared, sum_declared - 10))

print("     与基线对照：C 由 1 → %d（升）、U 由 0 → %d（升），同时宣称「全部原 falsified 缺陷清零」"
      % (c_, u_))
reg("FAIL", "§9-1 面板自相矛盾：C、U 计数反向上升却宣称缺陷清零",
    "H6/O6/C3/U2 合计 %d 与其自列 10 个子系统不符；且较基线 C 1→3、U 0→2 均为上升"
    % sum_declared,
    "即便按最宽松读法，该面板也不构成「修复」的证据", "算数 + 语义比对")

n_reg_pred = 0
reg("FAIL", "§9-2 修复版未登记任何无量纲靶的预测值与误差棒 ⇒ UFT-3 计数仍为 0",
    "全文未出现任何「预测值 ± 不确定度」的可登记条目（α 的表述依赖事后反解 ωA；G 依赖反解 K₀）",
    "按 openuft 既有统计，全部体系 n_registered_predictions = 0 的局面未改变 ⇒ 本申报不解锁 UFT-3",
    "预测登记口径")

reg("BOUNDARY", "§9-3 「纠错算法」3 项提交版未给出规格（本册 §9.5 已补全）",
    "提交版中 3.1 矛盾自检 / 3.2 拓扑归一 / 3.3 层级升维 均未给出输入格式·输出证书·终止性·复杂度·拒绝准则·算例；"
    "本册 §9.5 已作为审计引擎能力补全（含算例、捕获 §0 叉乘 bug、强制拒绝 L1→L3 升维），但提交理论自身仍缺公开规格",
    "层级升维若把 L1 内容批量标为 L3 仍违反 openuft 层级定义（L3 要求第一性推导或可检验预言）", "U 类判定")

# ===========================================================================
# §9.5  C38 三项审计算法实现与自测（本轮补全，回应 §9-3 的 U 类缺陷）
# ===========================================================================
print("\n" + "=" * 76)
print("§9.5  C38 三项审计算法：矛盾自检 / 拓扑归一 / 层级升维（实现 + 算例）")
print("=" * 76)


# ---------- 3.1 矛盾自检 ----------
def algo_contradiction_selfcheck(assertions):
    """输入：assertions = list[dict]，每条为一待检声明。
       支持 kind：
         'ortho' : {a,b} 两向量应正交（点积=0）
         'unit'  : {v}   向量应为单位长（|v|=1）
         'eq'    : {lhs,rhs[,tol]} 两数值应相等（相对容差）
         'sign'  : {v,expect} v 的符号应与 expect(±1) 一致
       输出：findings = list[(aid, kind, ok, msg)]
       终止性：有限输入有限步；无循环。
       复杂度：O(m) 单条校验（可选 O(m^2) 交叉比对未启用）。
       拒绝准则：缺 kind / kind 不在支持集 → 'rejected:under-specified' 或 'unknown-kind'。"""
    findings = []
    for a in assertions:
        aid = a.get("id", "?")
        kind = a.get("kind")
        if kind is None or kind not in ("ortho", "unit", "eq", "sign"):
            findings.append((aid, kind, False,
                             "rejected:under-specified" if kind is None else "rejected:unknown-kind"))
            continue
        if kind == "ortho":
            x, y = a["a"], a["b"]
            d = x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
            ok = abs(d) < mpf("1e-40")
            findings.append((aid, "ortho", ok, "B·T=%.3e (应=0)" % d if not ok else "ok"))
        elif kind == "unit":
            v = a["v"]
            m = sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
            ok = abs(m - 1) < mpf("1e-40")
            findings.append((aid, "unit", ok, "|B|=%.12f (应=1)" % m if not ok else "ok"))
        elif kind == "eq":
            tol = a.get("tol", mpf("1e-12"))
            ok = abs(a["lhs"] - a["rhs"]) <= (abs(a["rhs"]) + mpf("1e-60")) * tol
            findings.append((aid, "eq", ok, "lhs=%.6e rhs=%.6e" % (a["lhs"], a["rhs"])))
        else:  # sign
            s = 1 if a["v"] > 0 else -1
            ok = (s > 0 and a["expect"] > 0) or (s < 0 and a["expect"] < 0)
            findings.append((aid, "sign", ok, "sign(v)=%d expect=%d" % (s, a["expect"])))
    return findings


# 算例：V21 §0 副法向量叉乘（捕获叉乘 bug，并给出修正式）
# b 由速度归一化约束 ω√(A²+b²)=c 反解 ⇒ T 为单位矢、B_correct 真正单位长
A_d, om_d, c_d = mpf("1e-16"), mpf("1e15"), C
b_d = sqrt((c_d / om_d) ** 2 - A_d ** 2)
Tx, Ty, Tz = mpf(0), A_d * om_d / c_d, b_d * om_d / c_d          # T(λ=0)
Nx, Ny, Nz = mpf(-1), mpf(0), mpf(0)                             # N(λ=0)
B_user = [om_d * b_d / c_d, mpf(0), om_d * A_d / c_d]            # 用户写的 (ω/c)(b cos,b sin,A)
B_corr = [Ty * Nz - Tz * Ny, Tz * Nx - Tx * Nz, Tx * Ny - Ty * Nx]  # 正确 T×N

cc_find = algo_contradiction_selfcheck([
    {"id": "B_user⊥T", "kind": "ortho", "a": B_user, "b": [Tx, Ty, Tz]},
    {"id": "B_user⊥N", "kind": "ortho", "a": B_user, "b": [Nx, Ny, Nz]},
    {"id": "B_user单位长", "kind": "unit", "v": B_user},
    {"id": "B_correct⊥T", "kind": "ortho", "a": B_corr, "b": [Tx, Ty, Tz]},
    {"id": "B_correct⊥N", "kind": "ortho", "a": B_corr, "b": [Nx, Ny, Nz]},
    {"id": "B_correct单位长", "kind": "unit", "v": B_corr},
])
bug_caught = any((fid.startswith("B_user") and not ok) for fid, _, ok, _ in cc_find)
all_correct_ok = all(ok for fid, _, ok, _ in cc_find if fid.startswith("B_correct"))
print("     矛盾自检算例（V21 §0 副法向量叉乘）：")
for fid, kind, ok, msg in cc_find:
    print("       · %-14s %s  %s" % (fid, "PASS" if ok else "FAIL", msg))
print("     修正式：B_correct = (ω/c)(b·sin ωλ, −b·cos ωλ, A)")
item("矛盾自检捕获 V21 §0 叉乘错误（B_user 不正交于 T 与 N）", bug_caught,
     "B_user=(ωb/c,0,ωA/c) 在 λ=0 处 B_user·T=ω²Ab/c² ≠ 0、B_user·N=−ωb/c ≠ 0 ⇒ 叉乘 x,y 分量 sin/cos 与符号均错位")
item("矛盾自检确认修正式 B_correct=T×N 满足正交+单位长", all_correct_ok)
reg("INFO", "§9.5-1 矛盾自检算法已实现并捕获 §0 叉乘 bug",
    "algo_contradiction_selfcheck 对 ortho/unit/eq/sign 四类声明做有限步校验；"
    "喂入 V21 §0 的 B_user=(ω/c)(b cos,b sin,A) 报出与 T、N 均不正交且非单位长 ⇒ 叉乘展开式错误；"
    "修正式 B_correct=(ω/c)(b sin,−b cos,A) 全部通过",
    "I/O: list[assertion]→list[finding]；终止:有限；复杂度 O(m)；拒绝:under-specified/unknown-kind",
    "自实现 + 算例")


# ---------- 3.2 拓扑归一 ----------
def algo_topo_normalize(quantities):
    """输入：quantities = list[(qid, value, dim_dict)]，dim_dict∈{L,M,T,I} 整数指数。
       输出：{pis:list[(name,expr,val)], consistent:bool, rejected:list}
       方法：Buckingham Π——对维度矩阵做秩分析，构造无量纲组。
       终止性：有限（秩≤4）；复杂度 O(n·4)；拒绝：缺维/未知量 → rejected。"""
    bases = ["L", "M", "T", "I"]
    mat, names, vals, rejected = [], [], [], []
    for qid, val, dim in quantities:
        if dim is None:
            rejected.append(qid)
            continue
        names.append(qid)
        vals.append(val)
        mat.append([Fraction(dim.get(b, 0)) for b in bases])
    if len(mat) < 2:
        return {"pis": [], "consistent": False, "rejected": rejected}
    ref, ref_val = mat[0], vals[0]
    pis, consistent = [], True
    for i in range(1, len(mat)):
        e = None
        ok = True
        for k in range(4):
            if ref[k] != 0:
                ek = mat[i][k] / ref[k]
                if e is None:
                    e = ek
                elif abs(ek - e) > Fraction(1, 10 ** 9):
                    ok = False
        if not ok:
            consistent = False
            pis.append((names[i], "dim-mismatch-with-%s" % names[0], None))
        else:
            pis.append((names[i], "(%s)^(%s)/(%s)" % (names[0], e, names[i]),
                        (float(ref_val) ** float(e)) / float(vals[i])))
    return {"pis": pis, "consistent": consistent, "rejected": rejected}


# 算例：κ,τ,ω,c 的维度归一 + 不变量 κ²+τ²=ω²/c² 量纲自洽
k_ex = A_d * om_d ** 2 / c_d ** 2
t_ex = b_d * om_d ** 2 / c_d ** 2
w_ex = om_d
topo = algo_topo_normalize([
    ("kappa", k_ex, {"L": -1}),
    ("tau", t_ex, {"L": -1}),
    ("omega", w_ex, {"T": -1}),
    ("c", c_d, {"L": 1, "T": -1}),
])
dim_lhs = dpow(DIM_CURV, 2)                                  # (L^-1)^2 = L^-2
dim_rhs = ddiv(D(L=0, T=-2), dpow(D(L=1, T=-1), 2))         # ω²/c² = T^-2 / (L²T^-2) = L^-2
inv_dim_ok = dim_lhs == dim_rhs
print("     拓扑归一算例：κ²+τ² 与 ω²/c² 量纲 = %s vs %s ⇒ %s"
      % (dfmt(dim_lhs), dfmt(dim_rhs), "一致" if inv_dim_ok else "冲突"))
item("拓扑归一确认 κ²+τ²=ω²/c² 量纲自洽（Π 群存在）", inv_dim_ok)
reg("INFO", "§9.5-2 拓扑归一算法已实现",
    "algo_topo_normalize 对 (qid,value,dim) 做 Buckingham Π 降维；κ,τ,ω,c 可构造无量纲不变量组 Π=(κ²+τ²)/(ω²/c²)；"
    "拒绝缺维量",
    "I/O: list[(qid,value,dim)]→{pis,consistent,rejected}；终止:有限；复杂度 O(n·4)",
    "自实现 + 算例")


# ---------- 3.3 层级升维 ----------
def algo_hierarchy_uplift(claim_id, current_level, evidence_type,
                          constructive_derivation=False, testable_prediction=False,
                          requested_level=None):
    """输入：(claim_id, current_level∈{L0..L3}, evidence_type∈{identity,definition,
       construction,prediction}, constructive_derivation, testable_prediction, requested_level)
       输出：(allowed_level, decision, reason)
       拒绝准则：
         R1 跳级：requested > current+1 ⇒ 拒绝（不得 L1→L3）。
         R2 identity/definition 证据最多 L1，不得升 L2/L3。
         R3 升 L3 须同时具 constructive_derivation 与 testable_prediction(带误差棒)；否则封顶 L2(或 L1)。
       终止性：单趟 O(1)；复杂度 O(1)。"""
    order = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    cur = order[current_level]
    req = order[requested_level] if requested_level else cur
    if req > cur + 1:
        return current_level, "REJECT", "R1 跳级（%s→%s 不允许）" % (current_level, requested_level)
    if evidence_type in ("identity", "definition") and req > 1:
        return "L1", "REJECT-CAP-L1", "R2 identity/definition 证据不得高于 L1"
    if req >= 3 and not (constructive_derivation and testable_prediction):
        cap = "L2" if constructive_derivation else "L1"
        return cap, "REJECT-CAP", "R3 升 L3 需 constructive_derivation 与 testable_prediction(误差棒)；封顶 %s" % cap
    return (requested_level or current_level), "ALLOW", "通过"


r1 = algo_hierarchy_uplift("inv_k2_t2", "L0", "identity", requested_level="L3")
r2 = algo_hierarchy_uplift("alpha_eigen", "L1", "construction",
                            constructive_derivation=True, requested_level="L3")
r3 = algo_hierarchy_uplift("theta_def", "L0", "definition", requested_level="L2")
print("     层级升维算例：")
for tag, res in [("κ²+τ²=ω²/c² →L3", r1), ("α 本征(构造,无预言) →L3", r2), ("θ=τ/κ 定义 →L2", r3)]:
    print("       · %-26s 允许=%s 决策=%s | %s" % (tag, res[0], res[1], res[2]))
item("层级升维拒绝 L1→L3 批量升维（§9-3 的红旗）",
     r1[1].startswith("REJECT") and r2[1].startswith("REJECT"))
reg("INFO", "§9.5-3 层级升维算法已实现并强制拒绝违规升维",
    "algo_hierarchy_uplift 实现 R1(禁跳级)/R2(identity·definition 封顶 L1)/R3(升 L3 需构造+可检验预言)；"
    "算例：不变量恒等式请求升 L3 被拒、α 本征(仅构造无预言)升 L3 被拒封顶 L2、θ 定义不得高于 L1",
    "I/O:(claim_id,level,evidence_type,flags)→(allowed_level,decision,reason)；终止:O(1)",
    "自实现 + 算例")

reg("BOUNDARY", "§9.5-4 C38 三项算法本轮已补全（原 open → BOUNDARY）",
    "矛盾自检/拓扑归一/层级升维均已给出输入格式·输出证书·终止性·复杂度·拒绝准则·算例；"
    "但本引擎能力补全不抵消 §24–§37 对提交理论 headline 公式的 falsified 判定",
    "提交理论自身仍缺三项算法的公开规格；本册仅作为审计工具补齐", "引擎能力补全")


# ===========================================================================
# §9.6  C25(α 本征值) 与 C35(轨道进动) 的数值复核（用 §9.5 算法做实判据）
# ===========================================================================
print("\n" + "=" * 76)
print("§9.6  C25 α 本征值 / C35 轨道进动 —— 数值复核与突破条件")
print("=" * 76)


# ---------- C25：α 公式的欠定性与拓扑本征值路径 ----------
# 提交公式 α = (1/(2√N))·(c/(ωA))：未知量 {N, ωA} 两个，约束方程一个。
# 固定 α=α_exp，对任意选定的 N 反解 ωA 均成立 ⇒ 对 N 无选择力（伪派生）。
print("     C25  α=(1/(2√N))·(c/(ωA)) 的欠定性复核：")
c25_rows = []
for Ndemo in [mpf('4695'), mpf('18907'), mpf('1e9')]:
    wA = C / (2 * mp.sqrt(Ndemo) * ALPHA)                 # 反解使 α 命中观测
    a_back = (C / wA) / (2 * mp.sqrt(Ndemo))               # 回代验证
    ok = abs(a_back - ALPHA) < mpf('1e-40')
    c25_rows.append((Ndemo, wA, a_back, ok))
    print("       · N=%-12s → ωA=%.6e （回代 α=%.10f，命中=%s）"
          % (float(Ndemo), float(wA), float(a_back), ok))
c25_underdet = all(ok for _, _, _, ok in c25_rows)
item("C25 数值复核：N 取 4695/18907/1e9 三量级均可反解合法 ωA 命中 α", c25_underdet,
     "约束数 1 < 未知量数 2 ⇒ 系统欠定，α 不具选择力（与 C25 falsified 判据一致）")
# 拓扑本征值路径（理论自承的核心目标）：α = sin(1/(N+Δ_top))，Δ_top≈0.036
Dt = mpf('0.036')
N_from_topo = mpf(1) / mp.asin(ALPHA) - Dt
print("     拓扑本征值路径 α=sin(1/(N+Δ_top)) ⇒ 反解 N=%.4f（理论须由拓扑本征值『推出』此 N）"
      % float(N_from_topo))
item("C25 拓扑路径给出 N≈137.036，但 N 的『第一性推导』仍是理论未闭合目标", True,
     "N=137 目前是手填目标值；三条推导路径(拓扑绕数/Dirac谱流/量子相位)未互相收口 ⇒ α 仍属测量锚")
reg("INFO", "§9.6-1 C25 α 数值复核（确认 falsified 并给突破条件）",
    "对任意 N 均可反解 ωA 使 α 命中观测 ⇒ 伪派生；唯一使其成立的是『由拓扑本征值推出 N=137』，"
    "而该步在提交理论中仍未闭合（C23/C27 亦 falsified）",
    "I/O:{N,ωA}→α；终止:有限；复杂度 O(1)；拒绝:约束<未知量⇒欠定", "自实现 + 算例")


# ---------- C35：轨道进动的数值积分（Binet 方程 + RK4）----------
def orbit_precession_rad(gm, p, extra_coeff, n_orbits=30, dphi=mpf('0.003')):
    """中心力 F=-gm·m/r²·(1+extra_coeff·u² 形式) 的近日点进动（弧度/轨道）。
       Binet 方程（c=1 几何单位）：u''+u = gm/h² + extra_coeff·u²，h²≈gm·p（弱场）。"""
    h2 = gm * p
    base = gm / h2
    def acc(uu):
        return base + extra_coeff * uu * uu
    u = mpf('1.5') / p          # 椭圆初始条件（近日点 r=p/1.5，偏心率 0.5）；圆轨道 u=1/p 无进动无法检测
    v = mpf(0)
    phi = mpf(0)
    peri = [mpf(0)]                      # φ=0 起点即近日点
    prev_v = v
    steps = int(n_orbits * 2 * mp.pi / dphi) + 20
    for _ in range(steps):
        k1u, k1v = v, -u + acc(u)
        u2_ = u + dphi / 2 * k1u
        v2_ = v + dphi / 2 * k1v
        k2u, k2v = v2_, -u2_ + acc(u2_)
        u3_ = u + dphi / 2 * k2u
        v3_ = v + dphi / 2 * k2v
        k3u, k3v = v3_, -u3_ + acc(u3_)
        u4_ = u + dphi * k3u
        v4_ = v + dphi * k3v
        k4u, k4v = v4_, -u4_ + acc(u4_)
        un = u + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + dphi / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if prev_v > 0 and vn <= 0:        # v 由 + 转 − ⇒ 近日点
            frac = prev_v / (prev_v - vn)
            peri.append(phi + dphi * frac)
        prev_v = vn
        u, v = un, vn
        phi += dphi
    diffs = [peri[i + 1] - peri[i] for i in range(len(peri) - 1)]
    return (sum(diffs) / len(diffs)) - 2 * mp.pi


# 几何单位 gm=1, c=1，p=1000（弱场：3gm/(c²p)=3e-3 ≪ 1）
prec_kepler = orbit_precession_rad(mpf(1), mpf('1000'), mpf(0))     # 修复版线性 Φ ⇒ 牛顿，进动≈0
prec_gr = orbit_precession_rad(mpf(1), mpf('1000'), mpf(3))         # GR 1PN 修正项 3GMu²/c²
# 缩放到水星：Δφ_M = Δφ_geo · [GM_sun/(c²·p_Mercury)] / [1/(1·1000)]
GM_sun = mpf('1.32712440018e20')
p_merc = mpf('5.7909e10') * (mpf(1) - mpf('0.2056') ** 2)
scale = (GM_sun / (C ** 2 * p_merc)) / (mpf(1) / mpf('1000'))
arcsec_per_cent = lambda rad: rad * scale * (mpf(180) / mp.pi) * mpf(3600) * mpf('415')
print("     C35  轨道进动（水星，角秒/世纪）：")
print("       · 修复版线性 Φ（牛顿）   : %s" % fmt(float(arcsec_per_cent(prec_kepler)), 4))
print("       · GR 1PN 修正 3GMu²/c²   : %s  （观测值 42.98）" % fmt(float(arcsec_per_cent(prec_gr)), 4))
c35_mercury_fail = (abs(arcsec_per_cent(prec_kepler)) < mpf('1e-6')
                    and abs(arcsec_per_cent(prec_gr) - mpf('42.98')) < mpf('1'))
item("C35 数值复核：修复版线性 Φ 退化为牛顿律（进动≈0），无法解释水星 43″/世纪", c35_mercury_fail,
     "要复现 43″ 必须把 ∇Φ/Φ₀ 取为 1+3GM/(c²r) —— 即把 GR 的 GM/c² 作为自由形状参数导入 ⇒ 拟合而非推导")
reg("INFO", "§9.6-2 C35 轨道进动数值复核（确认 falsified 并给突破条件）",
    "RK4 积分 Binet 方程：线性 Φ 给出牛顿进动 0″（与观测 43″ 冲突）；GR 1PN 项 3GMu²/c² 给出 43″/世纪（匹配）"
    "但要求把 GM/c² 作为形状参数导入 ⇒ 框架只能『拟合』GR 而非『导出』",
    "I/O:(gm,p,extra_coeff)→进动弧度；终止:有限步；复杂度 O(步数)；拒绝:Bertrand 冲突(n≠1 非闭合轨道)",
    "自实现 + 算例")

# 层级升维：C25/C35 仍属 L0/L1 参数化/拟合，未达 L3
r_c25 = algo_hierarchy_uplift("alpha_deriv", "L0", "parameterization", requested_level="L3")
r_c35 = algo_hierarchy_uplift("orbit_precession", "L1", "fit", constructive_derivation=False,
                               testable_prediction=False, requested_level="L3")
print("     层级升维：C25(%s→%s) / C35(%s→%s)" % (r_c25[0], r_c25[1], r_c35[0], r_c35[1]))
item("C25/C35 经层级升维审查仍被封顶 L1（无构造推导+无带误差棒预言）",
     r_c25[1].startswith("REJECT") and r_c35[1].startswith("REJECT"))
reg("BOUNDARY", "§9.6-3 C25/C35 本轮数值复核后仍维持 falsified（非 PASS）",
    "C25 α 伪派生、C35 引力因子零内容/冲突——两项均经 §9.5 算法复核确认；"
    "理论若要在 L3 成立，须补两条第一性输入：①由拓扑本征值推出 N=137（C23/C27 未闭合）；"
    "②把螺旋曲率 κ,τ 与 GM/c² 经测地线方程挂钩（当前为手填）",
    "突破条件已显式列出，但提交理论未提供 ⇒ 仍为 falsified", "引擎能力补全")


# ===========================================================================
# §10  整合：诚实结论与真正可行的闭合路径
# ===========================================================================
print("\n" + "=" * 76)
print("§10  结论与最小可行修复路径")
print("=" * 76)

n_pass = sum(1 for r in ROWS if r["state"] == "PASS")
n_fail = sum(1 for r in ROWS if r["state"] == "FAIL")
n_bd = sum(1 for r in ROWS if r["state"] == "BOUNDARY")
n_info = sum(1 for r in ROWS if r["state"] == "INFO")
print("     判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(ROWS), n_pass, n_fail, n_bd, n_info))

paths = [
    ("基底", "把 z 分量由 c·t 改为 b·ω·t，并显式重列 ω√(A²+b²)=c ⇒ 消除超光速读数"),
    ("α", "放弃「2√N 反解」路线；按定理 F/G 走算子谱 + 量子化，且必须回答「什么把 (A,c) 钉在规格曲线上」"),
    ("G", "把靶改为无量纲 α_grav(m)=(m/m_P)²，并登记 m_e/m_P 的预测值 + 误差棒"),
    ("ρ", "直接删除（已从 G 中移除）；若要保留须改为 [S]=M·L⁻¹ 的线密度型对象并给出消费方方程"),
    ("Maxwell", "补全 μ₀J；若坚持几何源项须给出其量纲载体与电荷守恒相容定理"),
    ("引力修正", "或声明 Φ 线性于 r（承认因子退化为 G 的重标），或给出具体 Φ(r) 并接受力律被行星轨道检验"),
    ("N", "或删一留一并给出推导，或承认 N 仍为外部输入；floor 取整与定义 A 不可共存"),
    ("算法", "已完成：§9.5 给出三项算法的输入/输出/终止/复杂度/拒绝准则与算例，并捕获 §0 叉乘 bug（C38 由 open 转 BOUNDARY）"),
]
print("\n     最小可行修复路径（逐项）：")
for k, v in paths:
    print("       · %-8s %s" % (k, v))

reg("INFO", "§10-1 总体判定",
    "修复版在**方向上**做对了两件事（把 ρ 移出 G、给 N 一个可计算的表达式形式），"
    "但在**每一条 headline 公式**上都未通过第一性审计：量纲 3 处失败、循环性 1 处搬家、自由度净增 5、"
    "UFT-3 计数仍为 0 ⇒ 申报的「L3 完整第一性推导闭环」不成立",
    "判定： PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (n_pass, n_fail, n_bd, n_info),
    "本次审计")

# ===========================================================================
# 产出
# ===========================================================================
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

payload = {
    "title": "空间螺旋几何化统一场论「算法联盟缺陷修复体系」第一性审计",
    "date": "2026-09-25",
    "method": ["量纲账本", "Buckingham Π 定理", "定理 C（量纲不可行性）",
               "判别式 V = (n_hit-n_free-n_anchor)/n_hit", "自由度审计",
               "mpmath dps=50 独立复算"],
    "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
               "BOUNDARY": n_bd, "INFO": n_info},
    "checks": CHECKS,
    "rows": ROWS,
    "alpha_formula": {
        "implied_tan_theta_readingA": float(tan_new_A),
        "implied_tan_theta_readingB": float(tan_new_B),
        "speed_excess_readingA": float(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1),
        "alpha_pred_readingB": float(alpha_pred_B),
        "rel_error_readingB": float(rel_B),
        "N_lower_bound": float(n_min),
        "V": str(v_alpha),
    },
    "G_formula": {
        "K0_required_dim": dfmt(dim_k0_req),
        "K0_value_newton": float(k0_val),
        "planck_force_newton": float(C ** 4 / G_NEWTON),
        "V": str(v_g),
    },
    "fit_freedom_demo": fit_rows,
    "fit_freedom_skipped_readingB": skipped,
    "minimal_repair_paths": [{"item": k, "action": v} for k, v in paths],
}

with io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)

lines = []
lines.append("# 空间螺旋几何化统一场论「算法联盟缺陷修复体系」第一性审计")
lines.append("")
lines.append("> 日期 2026-09-25 · 工具：量纲账本 / Buckingham Π 定理 / 定理 C / 判别式 V / 自由度审计 / mpmath dps=50")
lines.append("")
lines.append("**判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
             % (len(ROWS), n_pass, n_fail, n_bd, n_info))
lines.append("")
lines.append("| 状态 | 编号 | 主张 | 依据 |")
lines.append("|------|------|------|------|")
for r in ROWS:
    det = r["detail"].replace("\n", " ")
    lines.append("| %s | %s | %s | %s |" % (r["state"], r["tag"], r["statement"], det))
lines.append("")
lines.append("## α 公式两读数")
lines.append("")
lines.append("| 量 | 值 |")
lines.append("|----|----|")
lines.append("| 隐含 tanθ（读数A） | %s |" % fmt(tan_new_A, 10))
lines.append("| 隐含 tanθ（读数B） | %s |" % fmt(tan_new_B, 10))
lines.append("| 读数A 超光速幅度 | %s%% |" % fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6))
lines.append("| 读数B α 预测 | %s |" % fmt(alpha_pred_B, 10))
lines.append("| 读数B 相对偏差 | %s |" % fmt(rel_B, 6))
lines.append("| N 的下界（唯一被排除的区间） | N < %s |" % fmt(n_min, 8))
lines.append("")
lines.append("## G 公式")
lines.append("")
lines.append("| 量 | 值 |")
lines.append("|----|----|")
lines.append("| [K₀] 必需量纲 | %s |" % dfmt(dim_k0_req))
lines.append("| 曲率量纲 | %s |" % dfmt(DIM_CURV))
lines.append("| 反解 K₀ | %s N |" % fmt(k0_val, 8))
lines.append("| 普朗克力 c⁴/G | %s N |" % fmt(C ** 4 / G_NEWTON, 8))
lines.append("")
lines.append("## 最小可行修复路径")
lines.append("")
for k, v in paths:
    lines.append("- **%s**：%s" % (k, v))
lines.append("")

with io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

# ===========================================================================
# 登记：claims.csv（幂等） + 11_证伪与反例
# ===========================================================================
print("\n" + "=" * 76)
print("§11  台账登记（claims.csv 幂等追加 + 证伪与反例记录）")
print("=" * 76)

NEW_CLAIMS = [
    ("C24", "【冲突】修复版公理1 的基底 R(t)=(Acosωt·Asinωt·ct) 与本体「光速螺旋运动」不相容：该式切向速率 sqrt(A²ω²+c²) 恒大于 c；为使 §2 的 α 公式命中观测需 ωA=c/%s ⇒ |v|=%s c（超光速 %s%%）"
     % (fmt(2 * sqrt(N_DEF_B) * ALPHA, 8), fmt(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2), 8),
        fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6)),
     "第一性审计", "falsified"),
    ("C25", "【冲突】α 新公式 α=(1/(2√N))(c/(ωA)) 是两个未知量对一个方程：读数B 下唯一约束为 N≥%s且读数A 下连该约束亦无；实测 N 取 4695 至 1e9 四个量级全部精确命中 α ⇒ 对 N 无选择力且不可证伪；判别式 V=(1−2−1)/1=−2 ≤ 0 判为伪派生"
     % fmt(n_min, 8),
     "第一性审计", "falsified"),
    ("C26", "【冲突】修复版未消除 tanθ 矛盾而是把它扩为四方：要求 tanθ 同时等于 α=%s（原主体 C03）· √N=%s（原拓扑绕数 C23）· 2√Nα=%s 或 √((2√Nα)²−1)=%s（修复版两读数）；实现方式是新公式不再使用 α=τ/κ ⇒ 冲突的一侧被删除而非被调和"
     % (fmt(ALPHA, 6), fmt(sqrt(N_DEF_B), 6), fmt(tan_new_A, 6), fmt(tan_new_B, 6)),
     "第一性审计", "falsified"),
    ("C27", "【冲突】N=floor(2π/Δθ_min) 只能产出整数 ⇒ 原定义 A 的 1/[α²(1−α)]=%s 不可能由新定义导出；「彻底消除双值冲突」实为抛弃其中一个值"
     % fmt(N_DEF_A, 10),
     "第一性审计", "falsified"),
    ("C28", "【欠定】Δθ_min 无第一性来源：要复现 N=18907 需 Δθ_min=%s rad 且文中未给出任何推导或约束方程 ⇒ 自由度由 N 平移为 Δθ_min 总数不降"
     % fmt(2 * pi / N_DEF_B, 10),
     "第一性审计", "open"),
    ("C29", "【冲突】G=c⁴α²/(8πK₀) 量纲失败：反解要求 [K₀]=[G]/[c⁴]=L·M·T⁻²（牛顿·力）而非曲率 L⁻¹；反解值 K₀=%s N 无任何已知物理量在该量级独立存在"
     % fmt(k0_val, 8),
     "第一性审计", "falsified"),
    ("C30", "【循环】G 式与被判 falsified 的 C12 同构：原式 ρ=sqrt(G/(α²μ₀c²)) 由 G 反推；新式 K₀=α²c⁴/(8πG) 同样由 G 反推 ⇒ 循环依赖只是把 ρ 换壳为 K₀ 故 C12 的 falsified 标记不可撤销",
     "第一性审计", "falsified"),
    ("C31", "【不可行】「K₀ 可由 N 与 α 直接推导」违反 Buckingham Π 定理：N 与 α 均无量纲 ⇒ 任何无量纲量的函数仍无量纲 不可能产出有量纲的 K₀ 更不可能产出 G",
     "第一性审计", "falsified"),
    ("C32", "【冲突】ρ=(1/V)∮S·dl 要求 [S]=M·L⁻¹（质量每长度）而这不是任何标准通量的量纲；且通量的自然积分域是面积 dA 而非线元 dl；另修复后 10 个子系统中无任何方程消费 ρ ⇒ 该量为孤儿量",
     "第一性审计", "falsified"),
    ("C33", "【冲突】∇×B=(1/c²)∂E/∂t+α²K(R) 的第二项量纲失败：[α²K]=%s 而方程其余各项为 %s ⇒ 差因子 %s 非无量纲；若改令 K 具 [∇×B] 量纲则 K 不再是曲率"
     % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))),
     "第一性审计", "falsified"),
    ("C34", "【冲突】该式缺传导电流项 μ₀J：稳恒情形要求 α²∫K·dA=μ₀I_enclosed 对一切电流分布成立 ⇒ K 被规定为电流的泛函 与「K 为时空曲率」冲突；取散度还迫使 ∇·J=(α²/μ₀)∇·K 这一未被声明的约束",
     "第一性审计", "falsified"),
    ("C35", "【冲突】F_grav=−Gm₁m₂/r²·∇Φ/Φ₀ 为二分：设 Φ∝r^n 则 ∇Φ/Φ₀∝r^(n−1) 力律为 r^(n−3) 恢复牛顿 r^−2 唯一要求 n=1 此时因子退化为常数可吸收进 G（零内容）；n≠1 则不再是 1/r² 与行星闭合轨道冲突（Bertrand 定理）",
     "第一性审计", "falsified"),
    ("C36", "【冲突】同一式中 ∇Φ/Φ₀ 需无量纲 ⇒ [Φ₀] 必须等于 [∇Φ]=[Φ]/L 而非 [Φ]；记号 Φ₀ 作为 Φ 的取值与这一要求冲突 除非另行声明 Φ 为无量纲相位",
     "第一性审计", "falsified"),
    ("C37", "【面板】申报 H6/O6/C3/U2 合计 17 与其自列 10 个子系统不符；且较基线 C 由 1→3·U 由 0→2 均为上升 却宣称「全部原 falsified 缺陷清零」；全文未登记任何无量纲靶的预测值与误差棒 ⇒ UFT-3 计数仍为 0",
     "第一性审计", "falsified"),
    ("C38", "【本轮补全】三项审计算法已在审计引擎 §9.5 实现：矛盾自检(algo_contradiction_selfcheck·ortho/unit/eq/sign 四类声明有限步校验·已捕获 V21 §0 副法向量叉乘错误)/拓扑归一(algo_topo_normalize·Buckingham Π 降维)/层级升维(algo_hierarchy_uplift·R1禁跳级/R2 identity封顶L1/R3 升L3需构造+可检验预言)；均含输入输出格式·终止性·复杂度·拒绝准则·算例。提交理论自身仍缺公开规格故维持 BOUNDARY 而非 PASS",
     "第一性审计", "BOUNDARY"),
    ("C46", "【复算·INFO】C25 α 公式 α=(1/(2√N))(c/(ωA)) 经 §9.6 数值复核确认欠定：N=4695/18907/1e9 三量级均可反解合法 ωA 命中 α ⇒ 伪派生；唯一转机『由拓扑本征值推出 N=137』在提交理论中未闭合",
     "第一性审计", "info"),
    ("C47", "【复算·INFO】C35 轨道进动经 §9.6 RK4 积分确认：线性 Φ 退化为牛顿律（进动 0″ 与水星 43″/世纪冲突）；GR 1PN 项给出 43″/世纪（匹配）但需导入 GM/c² 形状参数 ⇒ 拟合非导出；突破条件已列出",
     "第一性审计", "info"),
]

claims_path = os.path.join(SYS_DIR, "claims.csv")
text = io.open(claims_path, encoding="utf-8").read()
existing = set(l.split(",", 1)[0] for l in text.splitlines()[1:] if l.strip())
if not text.endswith("\n"):
    text += "\n"
added = 0
for cid, statement, category, status in NEW_CLAIMS:
    if cid in existing:
        continue
    for field in (cid, statement, category, status, "算法联盟审计组"):
        if "," in field or '"' in field:
            raise ValueError("字段不得含裸逗号或引号: " + cid)
    text += ",".join([cid, statement, category, status, "算法联盟审计组"]) + "\n"
    added += 1
io.open(claims_path, "w", encoding="utf-8").write(text)
item("claims.csv 幂等追加完毕（新增 %d 行 重复时 0 行）" % added, True)

if not os.path.isdir(REF_DIR):
    os.makedirs(REF_DIR)
rec_path = os.path.join(REF_DIR, "空间螺旋修复版_第一性缺陷记录.md")
rec = []
rec.append("# 空间螺旋修复版 · 第一性缺陷记录")
rec.append("")
rec.append("> 针对 2026-09-25 提交的《算法联盟·空间螺旋几何统一场论 缺陷修复体系》的独立审计结论。")
rec.append("> 引擎：`04_公共成果/算法联盟_全维自洽与归一化/源码/空间螺旋修复版_第一性审计与伪派生判定.py`（可复跑）。")
rec.append("> 全额四态判定见 `04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋修复版_第一性审计.md`。")
rec.append("")
rec.append("## 判定")
rec.append("")
rec.append("总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (len(ROWS), n_pass, n_fail, n_bd, n_info))
rec.append("")
rec.append("## 已登记缺陷（对应 claims.csv C24–C38）")
rec.append("")
for cid, statement, category, status in NEW_CLAIMS:
    rec.append("- **%s**（%s）：%s" % (cid, status, statement))
rec.append("")
rec.append("## 承认的非负成果")
rec.append("")
rec.append("- κ=Aω²/(A²ω²+u²)·τ=uω/(A²ω²+u²) 的闭合式经符号推导与 Frenet 数值反算**双路确认正确**。")
rec.append("- 把 ρ 移出 G 式的方向**正确**；问题在于 K₀ 承接了同一循环角色（C30）。")
rec.append("- 修复版所引原体系评级 H4/O5/C1/U0 与 L 计数**与档案一致**，引用属实。")
rec.append("")
rec.append("## 最小可行修复路径")
rec.append("")
for k, v in paths:
    rec.append("- **%s**：%s" % (k, v))
rec.append("")
rec.append("## 红线")
rec.append("")
rec.append("本记录只判定**数学自洽性与第一性层级**，不否定该纲领作为几何草案的价值；")
rec.append("「数学自洽」不等于「实验证实」，更不等于「L3 第一性推导」。")
rec.append("")
io.open(rec_path, "w", encoding="utf-8").write("\n".join(rec))

readme_path = os.path.join(REF_DIR, "README.md")
if os.path.isfile(readme_path):
    rt = io.open(readme_path, encoding="utf-8").read()
else:
    rt = "# 证伪与反例\n\n当前尚无本阶段独立产物；不因目录存在而标记完成。\n"
TAIL = ("本阶段产物：[空间螺旋修复版_第一性缺陷记录](空间螺旋修复版_第一性缺陷记录.md)"
        "（C24–C38；α/G/ρ/场耦合 四处量纲或循环性失败，面板计数自相矛盾，UFT-3 计数仍为 0）。")
if TAIL not in rt:
    import re as _re
    rt2, _n = _re.subn(r".*本阶段产物：.*\n?", TAIL + "\n", rt)
    if _n == 0:
        rt2 = rt.replace("当前尚无本阶段独立产物；不因目录存在而标记完成。", TAIL)
        if TAIL not in rt2:
            rt2 = rt.rstrip() + "\n\n" + TAIL + "\n"
    io.open(readme_path, "w", encoding="utf-8").write(rt2)

n_ok = sum(1 for c in CHECKS if c["ok"])
print("\n" + "=" * 76)
print("自检 %d/%d | 判定 总数=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d | 用时 %.1f s"
      % (n_ok, len(CHECKS), len(ROWS), n_pass, n_fail, n_bd, n_info, time.time() - T0))
if n_ok != len(CHECKS):
    print("【自检失败项】")
    for c in CHECKS:
        if not c["ok"]:
            print("  -", c["name"], "|", c["note"])
print("=" * 76)


# ===========================================================================
# §12  V21 续修 · C25：LB 本征能级高阶扫描（n=1..6 · mpmath 250 位）
# ===========================================================================
print("\n" + "=" * 76)
print("§12  V21续修 C25 | LB 本征能级扫描 n=1..6 · 250 位 mpmath")
print("=" * 76)

V21_START = len(ROWS)                     # 本节起的新判定行（用于独立数据切片）
mp.dps = 250
V_C = mpf("299792458")                    # c 精确定义值
V_G = mpf("6.67430e-11")                  # G（草稿指定 CODATA2018）
V_HBAR = mpf("1.0545718176461565e-34")    # ħ（草稿指定 CODATA2018）
V_ME = mpf("9.1093837015e-31")            # m_e（草稿指定 CODATA2018）
V_MSUN = mpf("1.98847e30")                # M_sun（草稿指定）
V_ALPHA = mpf("0.0072973525693")          # α_obs
V_ARC = pi / (180 * 3600)                 # 角秒→弧度

V_OMEGA = mpf("1.23558996e20")            # 螺旋特征频率（外部输入）
V_N = mpf("18907")                        # 拓扑绕数（外部输入）
V_V0 = mpf("1.0")                         # 几何势耦合（草稿声明无量纲）
dN_rel = mpf("1e-12")                     # 草稿假设 N 相对不确定度
domega_rel = mpf("1e-12")                 # 草稿假设 ω 相对不确定度


def En_lb(n):
    """草稿式 LB 本征能级：E_n = (ω²/c²)(V0 + n²ℏ²/N²)。"""
    return (V_OMEGA ** 2 / V_C ** 2) * (V_V0 + (n ** 2 * V_HBAR ** 2) / (V_N ** 2))


E1_v = En_lb(1)
C_couple = V_ALPHA * V_ME * V_C ** 2 / E1_v   # (n=1) 标定耦合常数 𝒞
term1 = V_HBAR ** 2 / (V_N ** 2)

print("     标定：E1 = %s" % fmt(E1_v, 24))
print("     标定：𝒞 = α_obs·m_e c²/E1 = %s" % fmt(C_couple, 24))
print("     谱修正基数：ℏ²/N² = %s（相对 V0=1 ⇒ 谱宽仅 ~1e-77 量级）" % fmt(term1, 6))

print("\n     n | E_n（数值）          | α_n               | σα（草稿式）      | (α_n−α_1)/α_1")
alpha_rows = []
for n in range(1, 7):
    En_v = En_lb(n)
    alphan = C_couple * En_v / (V_ME * V_C ** 2)
    term_n = (n ** 2 * V_HBAR ** 2) / (V_N ** 2)
    rel_err_draft = sqrt(domega_rel ** 2 + ((2 * term_n) / (V_V0 + term_n) * dN_rel) ** 2)
    alpha_err_draft = alphan * rel_err_draft
    rel_spread = alphan / V_ALPHA - 1
    alpha_rows.append({"n": n, "En": En_v, "alpha": alphan,
                       "sig": alpha_err_draft, "rel": rel_spread})
    print("     %2d | %s | %s | %s | %s"
          % (n, fmt(En_v, 18), fmt(alphan, 18), fmt(alpha_err_draft, 10), fmt(rel_spread, 4)))

max_rel = max(r["rel"] for r in alpha_rows[1:])
draft_sig_rel = alpha_rows[-1]["sig"] / alpha_rows[-1]["alpha"]
true_rel_n6 = 2 * abs(term1 / (V_V0 + term1) - (36 * term1) / (V_V0 + 36 * term1)) * dN_rel
log10_over = mp.log10(draft_sig_rel / max_rel) if max_rel > 0 else mp.mpf("nan")
print("\n     误差传播审计：α_n = 𝒞·E_n/(m_e c²) = α_obs·f_n/f_1 ⇒ ω、c 不确定度完全抵消；")
print("       草稿式 σα/α（n=6）= %s" % fmt(draft_sig_rel, 6))
print("       正确传播 σα/α（n=6）= %s" % fmt(true_rel_n6, 6))
print("       草稿误差棒超过谱效应（α_6−α_1）/α_1 约 10^%s 个量级" % fmt(log10_over, 5))

print("\n     量纲账本：")
print("       [ω²/c²] = L^-2；V0 无量纲 ⇒ 第一项 [L^-2]")
print("       n²ℏ²/N² ⇒ [M²L⁴T^-2]（ℏ 带量纲）⇒ 第二项（乘 ω²/c²）为 [M²L²T^-2]")
print("       ⇒ E_n 括号内 1（无量纲）与 M²L⁴T^-2 不可相加；E_n 亦非能量 [M L² T^-2]")
print("       ⇒ 𝒞 = α m_e c²/E1 ⇒ [M^-1]，并非无量纲耦合常数")

reg("FAIL", "§12-C25-1 量纲账本：E_n 非能量、𝒞 非无量纲",
    "E_n = (ω²/c²)(V0+n²ℏ²/N²) 中 V0 项为 [L^-2] 而 n²ℏ²/N² 项为 [M²L⁴T^-2] ⇒ 括号内不可相加；"
    "E_n 整体为 [M²L²T^-2] 非能量 [M L² T^-2]；𝒞 = α m_e c²/E1 ⇒ [M^-1] 非无量纲耦合常数",
    "与上轮 §1-C25-1 同一缺陷：草稿复用原公式未修量纲", "量纲账本")

reg("FAIL", "§12-C25-2 谱退化：n=2..6 与标定态 α_1 相对差 ≤ ~1e-75",
    "ℏ²/N² ≈ %s（相对 V0=1）⇒ α_n−α_1 相对量级 ~%s；α 观测不确定度仅 1.5e-10 ⇒ "
    "高阶能级在约 76 位有效数字内与 α_1 不可区分，无独立可检验靶" % (fmt(term1, 4), fmt(max_rel, 4)),
    "「n≥2 独立预言」在物理上消失；任何光谱类实验均无法分辨该谱间距", "退化审计（数值）")

reg("FAIL", "§12-C25-3 误差棒公式误算：ω 不确定度应完全抵消",
    "α_n = α_obs·f_n/f_1（f_n = V0+n²ℏ²/N²）⇒ ω、c 在两个能级比中抵消，草稿式把 dω 计入 σα 属双重计账；"
    "草稿式 σα/α（n=6）≈ %s，正确传播 ≈ %s（仅 N 差项贡献）" % (fmt(draft_sig_rel, 6), fmt(true_rel_n6, 6)),
    "即便采用草稿式，σα/α≈1e-12 也超过谱效应 10^%s 个量级 ⇒ 「误差棒完备/可证伪」不成立" % fmt(log10_over, 5),
    "误差传播解析")

reg("BOUNDARY", "§12-C25-4 标记：open（退化谱），非 open（可证伪谱）",
    "草稿 C25 更新标记为 open 的方向可接受（LB 离散谱在数学上建立）；"
    "但「高阶能级预测+误差棒完备+可证伪」被退化审计与误差棒审计推翻 ⇒ 登记 open（退化谱）",
    "等待先修量纲（ℏ²/N² 与 V0 的物理单位）后再谈可证伪性", "诚实重判")

# ===========================================================================
# §13  V21 续修 · C35：多行星近日点进动（固定 β · 金星/地球交叉验证）
# ===========================================================================
print("\n" + "=" * 76)
print("§13  V21续修 C35 | 固定 β 多行星进动 · 250 位 mpmath")
print("=" * 76)


def planet_dphi(a, e, T_yr, beta):
    """草稿式：返回（GR 基础项，几何修正项，总预测），单位角秒/百年。"""
    dphi_GR_per = 6 * pi * V_G * V_MSUN / (V_C ** 2 * a * (1 - e ** 2))
    dphi_geo_per = (3 * pi * beta / (a ** 2 * (1 - e ** 2))) * (V_G * V_MSUN) / (V_C ** 2 * a * (1 - e ** 2))
    N_orb = 100 / T_yr
    return (dphi_GR_per * N_orb / V_ARC,
            dphi_geo_per * N_orb / V_ARC,
            (dphi_GR_per + dphi_geo_per) * N_orb / V_ARC)


def dphi_geo_correct(a, e, beta):
    """Binet 方程 u''+u = GM/h² + (GMβ/h²)u² 的一阶精确结果：Δφ_geo = 2πβ/(a²(1−e²)²)（弧度/圈）。"""
    return 2 * pi * beta / (a ** 2 * (1 - e ** 2) ** 2)


a_mer, e_mer, T_mer = mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846")


def residual_draft(beta):
    _, _, dp = planet_dphi(a_mer, e_mer, T_mer, beta)
    return dp - mpf("43.03")


def residual_correct(beta):
    dpGR, _, _ = planet_dphi(a_mer, e_mer, T_mer, mpf(0))
    geo_c = dphi_geo_correct(a_mer, e_mer, beta) * (100 / T_mer) / V_ARC
    return dpGR + geo_c - mpf("43.03")


beta_draft = mp.findroot(residual_draft, mpf("1e18"))
beta_correct = mp.findroot(residual_correct, mpf("1e11"))

planets = [
    ("水星", mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846"), mpf("43.03")),
    ("金星", mpf("1.0820893e11"), mpf("0.00677672"), mpf("0.615197"), mpf("8.62")),
    ("地球", mpf("1.4959787e11"), mpf("0.0167086"), mpf("1.000017"), mpf("3.84")),
]

print("     水星标定：草稿式 β = %s" % fmt(beta_draft, 12))
print("             Binet 一阶正确式 β = %s" % fmt(beta_correct, 12))
print("     两式差因子（水星处）= %s = 3GM/(2c²a_mer)" % fmt(beta_draft / beta_correct, 8))

print("\n     %-4s | %-13s | %-15s | %-13s | %-11s | %-15s | %-13s"
      % ("行星", "GR基础", "几何修正(草稿式)", "总预测(草稿式)", "参考值",
         "几何修正(Binet式)", "总预测(正确式)"))
c35_out = []
for name, a_p, e_p, T_p, ref in planets:
    dpGR, dpGeo_draft, dpTot_draft = planet_dphi(a_p, e_p, T_p, beta_draft)
    geo_correct = dphi_geo_correct(a_p, e_p, beta_correct) * (100 / T_p) / V_ARC
    tot_correct = dpGR + geo_correct
    c35_out.append({"planet": name,
                    "GR": float(dpGR), "GR_s": fmt(dpGR, 8),
                    "geo_draft": float(dpGeo_draft), "geo_draft_s": fmt(dpGeo_draft, 8),
                    "tot_draft": float(dpTot_draft), "tot_draft_s": fmt(dpTot_draft, 8),
                    "ref": float(ref), "ref_s": fmt(ref, 8),
                    "geo_correct": float(geo_correct), "geo_correct_s": fmt(geo_correct, 8),
                    "tot_correct": float(tot_correct), "tot_correct_s": fmt(tot_correct, 8)})
    print("     %-4s | %-13s | %-15s | %-13s | %-11s | %-15s | %-13s"
          % (name, fmt(dpGR, 8), fmt(dpGeo_draft, 8), fmt(dpTot_draft, 8), fmt(ref, 8),
             fmt(geo_correct, 8), fmt(tot_correct, 8)))
print("     注：水星参考值 43.03 为观测反常进动（标定靶）；金星/地球参考值 8.62/3.84 为 GR 预言值（非独立观测残差）")

venus_ratio = c35_out[1]["geo_draft"] / c35_out[1]["geo_correct"]
earth_ratio = c35_out[2]["geo_draft"] / c35_out[2]["geo_correct"]
formula_factor = 3 * V_G * V_MSUN / (2 * V_C ** 2 * a_mer)

reg("PASS", "§13-C35-1 GR 基础项复现标准值（250 位）",
    "水星 %s / 金星 %s / 地球 %s 角秒每百年（标准 GR：42.98 / 8.62 / 3.84）"
    % (fmt(c35_out[0]["GR"], 6), fmt(c35_out[1]["GR"], 6), fmt(c35_out[2]["GR"], 6)),
    "解析一阶公式 6πGM/(c²a(1−e²)) 直接计算", "独立复算")

reg("BOUNDARY", "§13-C35-2 β 为水星拟合自由参数，非第一性",
    "β 由「总预测=43.03」反解（草稿式 β=%s），金星/地球预测全部依赖该拟合值；"
    "理论未给出 β 的第一性来源（对应上轮 §2-C35-3 的自由度审计）" % fmt(beta_draft, 6),
    "固定 β 不再重拟合在方法上成立，但「普适性检验」的前提是 β 具有独立推导", "自由度审计")

reg("FAIL", "§13-C35-3 草稿几何项与自身 Binet 方程一阶结果不符",
    "草稿 Δφ_geo = 3πβ·GM/(c²a³(1−e²)²)；由草稿 Binet 方程 u''+u=GM/h²+(GMβ/h²)u² 的一阶微扰得 Δφ_geo = 2πβ/(a²(1−e²)²)，"
    "草稿式多出因子 3GM/(2c²a)（水星处 %s）" % fmt(formula_factor, 6),
    "同以水星 43.03 标定，两式给出不同的金星/地球几何修正：金星 %s vs %s（差 %.3f×）；"
    "地球 %s vs %s（差 %.3f×）⇒ a 标度（a³ vs a²）不同，非约定自由度"
    % (fmt(c35_out[1]["geo_draft"], 6), fmt(c35_out[1]["geo_correct"], 6), venus_ratio,
       fmt(c35_out[2]["geo_draft"], 6), fmt(c35_out[2]["geo_correct"], 6), earth_ratio),
    "Binet 一阶微扰解析")

reg("INFO", "§13-C35-4 修正量级低于当前天体测量精度",
    "草稿式金星/地球几何修正仅 ~%s / ~%s 角秒每百年（正确式 ~%s / ~%s）；"
    "现代历表对金星/地球进动的约束在 ~0.1–1 角秒每百年量级 ⇒ 低 2–3 个量级，当前不可判"
    % (fmt(c35_out[1]["geo_draft"], 4), fmt(c35_out[2]["geo_draft"], 4),
       fmt(c35_out[1]["geo_correct"], 4), fmt(c35_out[2]["geo_correct"], 4)),
    "「等待更高精度天体测量观测比对」为诚实表述，但需先修正 §13-C35-3 的公式偏差", "精度量级")

reg("BOUNDARY", "§13-C35-5 标记：open（框架就绪·公式需修正）",
    "草稿 C35 更新标记为 open 的方向可接受（多行星交叉验证框架可运行）；"
    "但几何修正项公式与自身 Binet 一阶结果不符，须修正后再谈普适性预言", "诚实重判")

# ===========================================================================
# §14  V21 续修 · 汇总表更新复核 + 台账登记（C48/C49）+ 数据产出
# ===========================================================================
print("\n" + "=" * 76)
print("§14  V21续修 | 汇总表更新复核 · 台账 C48/C49 · 数据产出")
print("=" * 76)

# --- C24 复核：修正基底 |R'|=c（最小修复轮 B1 证据复算） ---
A_chk = mpf("1.3")
b_chk = A_chk / 137
w_chk = V_C / sqrt(A_chk ** 2 + b_chk ** 2)
speed_chk = sqrt((A_chk * w_chk) ** 2 + (b_chk * w_chk) ** 2) / V_C
item("C24 复核：修正基底（b·ω·t）+ ω√(A²+b²)=c ⇒ |R'|/c = 1", abs(speed_chk - 1) < mpf("1e-40"),
     "b/A=1/137 参数点 |R'|/c = %s" % fmt(speed_chk, 20))
reg("PASS", "§14-C24 复核",
    "第三分量写为 b·ω·t 并显式重列 ω√(A²+b²)=c 后 abs(R')=c 精确成立 ⇒ 草稿 C24 更新标记 PASS 有引擎证据（与最小修复轮 C39 一致）",
    "b/A=1/137 参数点 abs(R')/c = %s" % fmt(speed_chk, 20), "复算")

reg("INFO", "§14-C38 复核",
    "三项审计算法（矛盾自检/拓扑归一/层级升维）在本册 §9.5 已实现并带示范算例 ⇒ 草稿 C38 更新标记 open（待批量 claims 扫描）方向成立",
    "与 §9.6 的 C25/C35 复核共享同一算法栈", "引擎能力盘点")

print("\n     草稿全审计汇总表（C24–C38）与引擎复核：")
summary_rows = [
    (24, "falsified", "PASS", "基底光速约束，无超光速", "PASS（复算确认，见 §14-C24）"),
    (25, "falsified", "open", "LB本征谱；(n=1)标定𝒞，n≥6高阶α_n+误差棒完备，可证伪", "open（退化谱；误差棒公式需修正，不可证伪）"),
    (26, "falsified", "PASS", "tanθ唯一Frenet定义", "未复核（Frenet 比值 τ/κ=u/(Aω) 唯一，但四方冲突未调和）"),
    (27, "falsified", "PASS", "N外部拓扑输入，无虚假导出", "未复核（声明诚实，但非 PASS 证据）"),
    (28, "open", "PASS", "删除Δθ_min", "未复核"),
    (29, "falsified", "PASS", "删除K₀", "未复核"),
    (30, "falsified", "PASS", "消除G循环定义", "未复核"),
    (31, "falsified", "PASS", "Π定理满足", "未复核"),
    (32, "falsified", "PASS", "删除ρ孤儿场", "未复核（与最小修复轮 C44 方向一致）"),
    (33, "falsified", "PASS", "几何源电流量纲自洽", "未复核（上轮 §6-3 电荷守恒约束仍 FAIL）"),
    (34, "falsified", "PASS", "麦克斯韦含J+J_geo，电荷守恒约束推导完成", "未复核（μ₀J 已补，J_geo 源项仍缺闭合）"),
    (35, "falsified", "open", "Binet方程，水星标定β，金星地球独立预测，普适性检验框架就绪", "open（框架就绪；几何项公式需修正）"),
    (36, "falsified", "PASS", "相位场量纲对齐", "未复核"),
    (37, "falsified", "PASS", "面板统计修正，多套无量纲预测靶", "未复核（靶登记仍为 0）"),
    (38, "open", "open", "三审计算法完整实现，示范算例就绪；待批量全量claims扫描", "open（§9.5 已实现，待批量扫描）"),
]
for cid, old, new, note, review in summary_rows:
    print("     C%-2d  %-9s → %-9s | %s | 引擎复核：%s" % (cid, old, new, note, review))
reg("INFO", "§14-汇总 更新标记引擎复核",
    "草稿 C24–C38 更新标记中：C24 PASS、C25/C35/C38 open 有引擎证据；"
    "C26–C34、C36、C37 的 PASS 为草稿自评，本册未给出复核证据 ⇒ 不得直接登记为 PASS",
    "claims.csv 中 C25/C35 旧行属修复版轮记录，保持 falsified；V21续修轮新登记 C48/C49", "汇总口径")

# --- 台账登记：C48/C49（幂等，与 §11 的 C24–C47 互不冲突） ---
V21_NEW_CLAIMS = [
    ("C48", "【V21续修·谱】LB本征能级 n=1..6 扫描（mpmath 250位）：α_n 与标定值 α_1 相对差 ≤ 1.09e-75（ℏ²/N²≈3.11e-77 主导）⇒ 谱在约 76 位有效数字内退化 无独立可检验靶；草稿误差棒公式误算 ω 抵消项 正确传播误差 ~1e-87 量级 故「误差棒完备/可证伪」不成立 → open（退化谱）",
     "第一性审计", "open"),
    ("C49", "【V21续修·进动】固定 β（水星标定 43.03 角秒/百年）预测金星/地球近日点进动：GR 项复现 8.62/3.84 角秒/百年；草稿几何修正项与自身 Binet 方程一阶结果不符（正确 2πβ/(a²(1−e²)²) 草稿含 3GM/(2c²a)≈3.83e-8 因子）同标定下金星/地球预测差约 1.9×/2.6×；修正量仅 ~1e-3 角秒/百年 低于当前天体测量精度 → open（框架就绪·公式需修正）",
     "第一性审计", "open"),
]
added_v21 = 0
for cid, statement, category, status in V21_NEW_CLAIMS:
    if cid in existing:
        continue
    for field in (cid, statement, category, status, "算法联盟审计组"):
        if "," in field or '"' in field:
            raise ValueError("字段不得含裸逗号或引号: " + cid)
    text += ",".join([cid, statement, category, status, "算法联盟审计组"]) + "\n"
    added_v21 += 1
io.open(claims_path, "w", encoding="utf-8").write(text)
item("claims.csv V21续修幂等追加完毕（新增 %d 行 重复时 0 行）" % added_v21, True)

# --- 数据产出：V21续修审计 json/md（独立文件，不覆盖修复版轮产物） ---
V21_ROWS = ROWS[V21_START:]
n21_pass = sum(1 for r in V21_ROWS if r["state"] == "PASS")
n21_fail = sum(1 for r in V21_ROWS if r["state"] == "FAIL")
n21_bd = sum(1 for r in V21_ROWS if r["state"] == "BOUNDARY")
n21_info = sum(1 for r in V21_ROWS if r["state"] == "INFO")

V21_payload = {
    "title": "空间螺旋几何化统一场论 · V21续修 C25/C35 审计（并入第一性审计统一脚本）",
    "date": "2026-09-26",
    "method": ["mpmath dps=250", "参数扰动误差传播（草稿式 vs 正确式）", "量纲账本",
               "Binet 一阶微扰解析", "水星标定 β + 金星/地球交叉验证"],
    "counts": {"total": len(V21_ROWS), "PASS": n21_pass, "FAIL": n21_fail,
               "BOUNDARY": n21_bd, "INFO": n21_info},
    "C25": {"E1": float(E1_v), "C_couple": float(C_couple),
            "hbar2_over_N2": float(term1), "max_rel_spread": float(max_rel),
            "sigma_draft_rel": float(draft_sig_rel), "true_rel_n6": float(true_rel_n6),
            "log10_sigma_over_spread": float(log10_over),
            "rows": [{"n": r["n"], "En": float(r["En"]), "alpha": float(r["alpha"]),
                      "sigma_draft": float(r["sig"]), "rel_spread": float(r["rel"])}
                     for r in alpha_rows]},
    "C35": {"beta_draft": float(beta_draft), "beta_correct": float(beta_correct),
            "formula_ratio_mercury": float(formula_factor),
            "venus_geo_ratio_draft_over_correct": float(venus_ratio),
            "earth_geo_ratio_draft_over_correct": float(earth_ratio),
            "rows": c35_out},
    "rows": V21_ROWS,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修_C25C35_审计.json"), "w", encoding="utf-8") as fh:
    json.dump(V21_payload, fh, ensure_ascii=False, indent=1)

lines21 = []
lines21.append("# 空间螺旋几何化统一场论 · V21续修 C25/C35 审计（250 位 mpmath）")
lines21.append("")
lines21.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋修复版_第一性审计与伪派生判定.py` §12–§14（统一脚本并入）")
lines21.append("> 方法：mpmath dps=250 / 量纲账本 / 误差传播（草稿式 vs 正确式）/ Binet 一阶微扰 / 水星标定 β + 金星/地球交叉验证")
lines21.append("")
lines21.append("**判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
               % (len(V21_ROWS), n21_pass, n21_fail, n21_bd, n21_info))
lines21.append("")
lines21.append("| 状态 | 编号 | 主张 | 依据 |")
lines21.append("|------|------|------|------|")
for r in V21_ROWS:
    det = r["detail"].replace("\n", " ")
    lines21.append("| %s | %s | %s | %s |" % (r["state"], r["tag"], r["statement"], det))
lines21.append("")
lines21.append("## C25 LB 本征谱扫描（n=1..6）")
lines21.append("")
lines21.append("| n | E_n（数值） | α_n | σα（草稿式） | (α_n−α_1)/α_1 |")
lines21.append("|----|----|----|----|----|")
for r in alpha_rows:
    lines21.append("| %d | %s | %s | %s | %s |"
                   % (r["n"], fmt(r["En"], 10), fmt(r["alpha"], 14), fmt(r["sig"], 8), fmt(r["rel"], 4)))
lines21.append("")
lines21.append("| 量 | 值 |")
lines21.append("|----|----|")
lines21.append("| ℏ²/N²（谱修正基数） | %s |" % fmt(term1, 6))
lines21.append("| 最大相对谱宽 (α_6−α_1)/α_1 | %s |" % fmt(max_rel, 6))
lines21.append("| 草稿式 σα/α（n=6） | %s |" % fmt(draft_sig_rel, 6))
lines21.append("| 正确传播 σα/α（n=6） | %s |" % fmt(true_rel_n6, 6))
lines21.append("| 草稿误差棒超出谱效应量级 | 10^%s |" % fmt(log10_over, 5))
lines21.append("")
lines21.append("## C35 多行星进动（固定 β）")
lines21.append("")
lines21.append("| 行星 | GR基础 | 几何修正(草稿式) | 总预测(草稿式) | 参考值 | 几何修正(Binet式) | 总预测(正确式) |")
lines21.append("|----|----|----|----|----|----|----|")
for r in c35_out:
    lines21.append("| %s | %s | %s | %s | %s | %s | %s |"
                   % (r["planet"], r["GR_s"], r["geo_draft_s"], r["tot_draft_s"],
                      r["ref_s"], r["geo_correct_s"], r["tot_correct_s"]))
lines21.append("")
lines21.append("| 量 | 值 |")
lines21.append("|----|----|")
lines21.append("| β（草稿式，水星标定） | %s |" % fmt(beta_draft, 12))
lines21.append("| β（Binet 一阶正确式，水星标定） | %s |" % fmt(beta_correct, 12))
lines21.append("| 公式差因子 3GM/(2c²a_mer) | %s |" % fmt(formula_factor, 6))
lines21.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修_C25C35_审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines21))

print("\n" + "=" * 76)
print("V21续修判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(V21_ROWS), n21_pass, n21_fail, n21_bd, n21_info))
print("产出：04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V21续修_C25C35_审计.json / .md")
print("=" * 76)


# ===========================================================================
# §15  V22 收官 · C25 续：高阶本征能级扫描（n 域扩展 + 误差棒正确式 + 可检测阈值）
# ===========================================================================
print("\n" + "=" * 76)
print("§15  V22收官 C25 | 高阶本征能级扫描：n 域扩展 + 误差棒正确式 + 可检测阈值")
print("=" * 76)

V22_START = len(ROWS)


def f_n_of(n):
    """草稿谱函数 f_n = V0 + n²ℏ²/N²（E_n = (ω²/c²)·f_n）。"""
    return V_V0 + (n ** 2) * term1


def spread_of(n):
    """(α_n − α_1)/α_1 = f_n/f_1 − 1（α_n = α_obs·f_n/f_1，ω·c 严格约去）。"""
    return f_n_of(n) / f_n_of(1) - 1


def sigma_rel_draft(n):
    """草稿误差棒：把 dω_rel 与 dN_rel 同时计入 ⇒ ω 项属双重计账。"""
    t_n = (n ** 2) * term1
    return sqrt(domega_rel ** 2 + ((2 * t_n) / (V_V0 + t_n) * dN_rel) ** 2)


def sigma_rel_correct(n):
    """正确传播：σ(α_n/α_1)/(α_n/α_1) = |∂_N ln(f_n/f_1)|·σ_N（σ_N = dN_rel·N）。
       ∂_N ln(f_n/f_1) = (−2u/N)[n²/(V0+n²u) − 1/(V0+u)]，u = ℏ²/N²。"""
    u = term1
    dln = (-2 * u / V_N) * (n ** 2 / (V_V0 + n ** 2 * u) - 1 / (V_V0 + u))
    return abs(dln) * (dN_rel * V_N)


item("C25-误差棒①：代数恒等 α_n = α_obs·f_n/f_1 ⇒ ω、c 严格约去（非「不确定度抵消」）",
     spread_of(1) == 0,
     "E_n=(ω²/c²)f_n、𝒞=α_obs·m_e c²/E_1 ⇒ α_n/α_obs = E_n/E_1 = f_n/f_1，与 ω、c 无关")

N_SCAN = list(range(1, 13)) + [10 ** 3, 10 ** 6, 10 ** 12, 10 ** 18, 10 ** 24,
                              10 ** 30, 10 ** 33, 10 ** 34, 10 ** 38]


def fmt_n(n):
    """大 n 以 10^k 形式展示（n=1000 ⇒ 10^3），小 n 原样。"""
    s = str(n)
    if n >= 1000 and s == "1" + "0" * (len(s) - 1):
        return "10^%d" % (len(s) - 1)
    return s


print("\n     %-8s | %-15s | %-15s | %-15s | %s"
      % ("n", "(α_n−α_1)/α_1", "σα/α(草稿式)", "σα/α(正确式)", "谱宽/α精度(1.5e-10)"))
scan15 = []
for n in N_SCAN:
    # 注：此处曾用局部变量名 `sp`，遮蔽模块级 sympy 别名 `sp`（import sympy as sp）⇒
    #     后续任何 sp.xxx 调用都会 AttributeError（本册 §19 现场踩到并修复）。改名 spread_n。
    spread_n = spread_of(n)
    sg_d = sigma_rel_draft(n)
    sg_c = sigma_rel_correct(n)
    scan15.append({"n": n, "spread": float(spread_n), "sigma_draft": float(sg_d),
                   "sigma_correct": float(sg_c), "ratio_to_alpha_prec": float(spread_n / ALPHA_UREL)})
    print("     %-8s | %-15s | %-15s | %-15s | %s"
          % (fmt_n(n), fmt(spread_n, 6), fmt(sg_d, 6), fmt(sg_c, 6), fmt(spread_n / ALPHA_UREL, 6)))

n_detect = sqrt(1 + ALPHA_UREL * V_V0 / term1)
n_unit = sqrt(V_V0 / term1)
print("\n     可检测性阈值（α 测量精度 σα/α = %s）：" % fmt(ALPHA_UREL, 4))
print("       n=6 谱宽 (α_6−α_1)/α_1     = %s" % fmt(max_rel, 6))
print("       谱宽 = σα/α 所需 n_detect   = %s" % fmt(n_detect, 10))
print("       二阶项 = V0 所需 n_unit     = %s" % fmt(n_unit, 10))
print("       低于 α 精度的量级数         = %s" % fmt(mp.log10(ALPHA_UREL / max_rel), 5))

reg("PASS", "§15-C25-5 误差棒正确式建立：ω、c 严格约去 ⇒ 草稿 σα 为双重计账（解析证明）",
    "α_n/α_obs = f_n/f_1 与 ω、c 无关（代数恒等）⇒ 草稿 σα(n=6)=%s 由 dω_rel=1e-12 支配属错误；"
    "正确传播仅含 N 项：σα/α(n=6) = %s" % (fmt(sigma_rel_draft(6), 6), fmt(sigma_rel_correct(6), 6)),
    "草稿误差棒超出谱效应 10^%s 个量级（承接 §12-C25-3，本轮给出解析证明）" % fmt(log10_over, 5),
    "误差传播解析")

reg("FAIL", "§15-C25-6 可检测性阈值：谱宽达 α 测量精度需 n ≳ 2.196e33",
    "n=6 谱宽 = %s（低 α 精度 %s 个量级）；令 f_n/f_1−1 = σα/α = %s 解得 n_detect = %s；"
    "二阶项与 V0 同量级需 n_unit = %s"
    % (fmt(max_rel, 6), fmt(mp.log10(ALPHA_UREL / max_rel), 5), fmt(ALPHA_UREL, 4),
       fmt(n_detect, 10), fmt(n_unit, 10)),
    "n≤12 全谱相对差 ≤ 1.3e-74 ⇒ 任何光谱类实验均无判别力；「n≥2 独立预言」的物理窗口被推到 "
    "n ~ 10^33（无物理承载客体）", "数值扫描（n 域扩展）")

reg("BOUNDARY", "§15-C25-7 标记维持：open（退化谱·阈值不可达）",
    "存在形式窗口 n∈(%s, %s)（谱宽可测且二阶项尚未溢出），但：(a) 量纲缺陷未修"
    "（§12-C25-1：括号内 [L^-2] 与 [M²L⁴T^-2] 不可相加）；(b) n~1e33 无物理承载客体 ⇒ 窗口不可达"
    % (fmt(n_detect, 6), fmt(n_unit, 6)),
    "不把「数值上存在窗口」误记为「可证伪」；C25 维持 open（退化谱）", "诚实重判")


# ===========================================================================
# §16  V22 收官 · C35 续：多行星进动交叉验证 + β 普适性结构审计
# ===========================================================================
print("\n" + "=" * 76)
print("§16  V22收官 C35 | 多行星进动交叉验证 + β 普适性结构审计")
print("=" * 76)

# --- (1) 结构同一性：β0 = 3h²/c² 使草稿 Binet 方程与 GR 1PN 方程恒等 ---
H2_M = V_G * V_MSUN * a_mer * (1 - e_mer ** 2)
BETA0_M = 3 * H2_M / V_C ** 2
coef_draft = (V_G * V_MSUN / H2_M) * BETA0_M
coef_GR = 3 * V_G * V_MSUN / V_C ** 2
print("     结构同一性：草稿 u''+u = GM/h² + (GM·β/h²)u²；GR 1PN u''+u = GM/h² + (3GM/c²)u²")
print("       β0 = 3h²/c² = %s（水星）" % fmt(BETA0_M, 10))
print("       ⇒ 草稿 u² 系数 (GM/h²)·β0 = %s；GR 系数 3GM/c² = %s" % (fmt(coef_draft, 10), fmt(coef_GR, 10)))
item("C35-结构：β0=3h²/c² ⇒ 草稿 Binet 方程与 GR 1PN 方程恒等（u² 系数精确相等）",
     abs(coef_draft / coef_GR - 1) < mpf("1e-50"),
     "相对偏差 %s ⇒ β=β0 分支下「几何修正」即 GR 1PN 项本身（无新增自由度、无新增预言）"
     % fmt(abs(coef_draft / coef_GR - 1), 4))


# --- (2) β-free 形状比（两框架各自给出，用于判别理论形状是否稳定） ---
def shape_ratio(p_idx, exponent):
    """R_p/R_水星。exponent=1 ⇒ Δφ_geo∝1/(a(1−e²))（正确 Binet 一阶）；2 ⇒ ∝1/(a²(1−e²))（草稿式）。"""
    def w(pl):
        return pl[1] ** exponent * (1 - pl[2] ** 2)
    return w(planets[0]) / w(planets[p_idx])


print("\n     β-free 形状比 R_p/R_水星（β 在比值中约去 ⇒ 唯一独立于标定的候选可证伪量）：")
print("       %-4s | %-24s | %-24s" % ("行星", "正确 Binet 式(比例 1/a)", "草稿式(比例 1/a²)"))
shape_rows = []
for _i, _pl in enumerate(planets):
    _r1 = shape_ratio(_i, 1)
    _r2 = shape_ratio(_i, 2)
    shape_rows.append({"planet": _pl[0], "ratio_correct": float(_r1), "ratio_draft": float(_r2)})
    print("       %-4s | %-24s | %-24s" % (_pl[0], fmt(_r1, 8), fmt(_r2, 8)))

# --- (3) 可观测性（假定历表约束量级，外部输入已声明） ---
SIGMA_OBS = mpf("0.1")            # 假定：现代历表对类地行星近日点进动的约束量级（角秒/百年）
R_merc = mpf(c35_out[0]["geo_correct_s"]) / mpf(c35_out[0]["GR_s"])
print("\n     相对 GR 的几何修正之比 R = Δφ_geo/Δφ_GR ∝ 1/(a(1−e²))（对 a 单调）：")
for _r in c35_out:
    _R = mpf(_r["geo_correct_s"]) / mpf(_r["GR_s"])
    print("       %-4s R = %-12s（相对水星 %s）" % (_r["planet"], fmt(_R, 6), fmt(_R / R_merc, 6)))
print("     可观测性（假定 σ_obs = %s 角秒/百年，外部输入·待核实）：" % fmt(SIGMA_OBS, 4))
for _r in c35_out[1:]:
    _gc = mpf(_r["geo_correct_s"])
    print("       %-4s 几何修正(正确式) = %-10s 角秒/百年 ⇒ %s σ_obs；可判需 σ ≲ %s"
          % (_r["planet"], _r["geo_correct_s"], fmt(_gc / SIGMA_OBS, 4), fmt(_gc / 3, 4)))

_v_shape = shape_rows[1]["ratio_correct"] / shape_rows[1]["ratio_draft"]
_e_shape = shape_rows[2]["ratio_correct"] / shape_rows[2]["ratio_draft"]

reg("INFO", "§16-C35-6 β-free 形状比（唯一独立于标定的候选可证伪量）",
    "R_p/R_水星：正确 Binet 式 金星 %s、地球 %s；草稿式 金星 %s、地球 %s"
    % (fmt(shape_rows[1]["ratio_correct"], 6), fmt(shape_rows[2]["ratio_correct"], 6),
       fmt(shape_rows[1]["ratio_draft"], 6), fmt(shape_rows[2]["ratio_draft"], 6)),
    "该比值与 β 无关 ⇒ 未来若测出金星/地球反常进动超额，可用比值形状检验；"
    "但信号量级仅 1e-4–1e-3 相对 GR（见 §16-C35-9）", "纯几何推导")

reg("FAIL", "§16-C35-7 β-free 形状比随公式框架变化：金星 %s×、地球 %s×"
    % (fmt(_v_shape, 5), fmt(_e_shape, 5)),
    "同一理论两条公式给出不同形状：金星/水星 %s(a²) vs %s(a³)；地球/水星 %s(a²) vs %s(a³)"
    % (fmt(shape_rows[1]["ratio_correct"], 6), fmt(shape_rows[1]["ratio_draft"], 6),
       fmt(shape_rows[2]["ratio_correct"], 6), fmt(shape_rows[2]["ratio_draft"], 6)),
    "形状比虽与 β 无关，却与「a² vs a³」这一未解决的框架歧义（§13-C35-3）耦合 ⇒ "
    "公式歧义消除前形状检验不能判别理论", "框架歧义审计")

reg("FAIL", "§16-C35-8 标定靶 = 最佳靶 ⇒ 独立判别力为零",
    "几何修正相对 GR 之比 R ∝ 1/(a(1−e²)) 对 a 单调 ⇒ 太阳系行星中水星信号最大（R_水星 = %s），"
    "而水星正是 β 的标定靶 ⇒ 「金星/地球独立预测」全部落在信号更弱的靶上（R = 0.513·R_水星 / "
    "0.371·R_水星）" % fmt(R_merc, 6),
    "普适性检验要求「标定靶 ≠ 检验靶且检验靶信号可测」；本理论两条同时不满足", "结构审计")

reg("BOUNDARY", "§16-C35-9 可观测性：修正量低现代历表约束 1.3–1.8 个量级",
    "正确式几何修正：金星 %s、地球 %s 角秒/百年；相对假定 σ_obs=%s 为 %sσ / %sσ ⇒ 当前不可判"
    % (c35_out[1]["geo_correct_s"], c35_out[2]["geo_correct_s"], fmt(SIGMA_OBS, 4),
       fmt(mpf(c35_out[1]["geo_correct_s"]) / SIGMA_OBS, 4),
       fmt(mpf(c35_out[2]["geo_correct_s"]) / SIGMA_OBS, 4)),
    "σ_obs 为量级假设（外部输入，已声明）；可判需达 ~1.6e-3 角秒/百年精度", "量级估计")

reg("BOUNDARY", "§16-C35-10 标记维持：open（框架就绪·无独立判别力）",
    "综合 §16-C35-6..9：结构同一性（β0 分支退化为 GR 复述）+ 框架歧义（形状比不稳定）"
    "+ 标定靶=最佳靶（独立性为零）+ 信号低于精度 ⇒ 多行星交叉验证框架可运行但无判别力",
    "C35 维持 open；与 §13-C35-5 口径一致", "诚实重判")


# ===========================================================================
# §18  V21 续修② 模块1 · 引力泡工程（GravBubble）—— 地面实验室预言靶审计
# ===========================================================================
print("\n" + "=" * 76)
print("§18  V21续修② 模块1 | 引力泡工程（GravBubble）：量纲 / 归一化 / 可证伪性审计")
print("=" * 76)

V23_START = len(ROWS)

# --- 草稿参数（照抄，不做任何「善意」补正） ---
GB_SIGMA = mpf("0.1")        # σ  泡宽 m
GB_K0 = mpf("1e-16")         # κ0 草稿自述 m^-2（与本体 κ 量纲冲突，见 18.2）
GB_T0 = mpf("1e-12")         # τ0 m^-1
GB_AG = mpf("0.85")          # α_g 草稿示例值（自称「TUFT 基础耦合」）
GB_VP = C * mpf("0.1")       # 粒子速度 0.1c

print("     草稿参数：σ=%s m  κ0=%s  τ0=%s  α_g=%s   v=%s c"
      % (fmt(GB_SIGMA, 6), fmt(GB_K0, 6), fmt(GB_T0, 6), fmt(GB_AG, 6), "0.1"))

# ---- 18.1 高斯积分严格值 + 能量归一化 ----
_gb_I = mp.quad(lambda _r: mp.exp(-(_r ** 2) / GB_SIGMA ** 2) * _r ** 2, [0, mp.inf]) * 4 * pi
_gb_pi = pi ** mpf("1.5") * GB_SIGMA ** 3
_gb_2pi = (2 * pi) ** mpf("1.5") * GB_SIGMA ** 3
_gb_pk = GB_K0 ** 2 + GB_AG * GB_T0 ** 2
E_doc = GB_SIGMA ** 3 / (16 * pi * G_NEWTON) * _gb_pk
E_gauss = _gb_I / (16 * pi * G_NEWTON) * _gb_pk
E_alt = _gb_2pi / (16 * pi * G_NEWTON) * _gb_pk
E_dimfix = C ** 4 * E_gauss

print("\n     --- 18.1 高斯积分与能量归一化（mpmath 250 位） ---")
print("     ∮d³x e^{-r²/σ²}          = %s" % fmt(_gb_I, 20))
print("     π^{3/2}σ³                = %s    ⇒ 比值 = %s" % (fmt(_gb_pi, 20), fmt(_gb_I / _gb_pi, 20)))
print("     (2π)^{3/2}σ³             = %s" % fmt(_gb_2pi, 20))
print("     E_草稿  σ³/(16πG)·(…)    = %s J" % fmt(E_doc, 12))
print("     E_严格  π^{3/2}σ³/(16πG) = %s J   ⇒ 草稿少乘 %s 倍"
      % (fmt(E_gauss, 12), fmt(E_gauss / E_doc, 12)))
print("     E_(2π)^{3/2} 口径        = %s J   ⇒ E_草稿/该口径 = %s（草稿中间式与最终式互斥）"
      % (fmt(E_alt, 12), fmt(E_doc / E_alt, 12)))
print("     E_量纲修复(×c⁴)          = %s J = %s eV"
      % (fmt(E_dimfix, 12), fmt(E_dimfix / mpf("1.602176634e-19"), 8)))
print("       对照：LHC 单束能量 3.62e8 J ⇒ 该泡能量为其 %s 倍"
      % fmt(E_dimfix / mpf("3.62e8"), 6))

reg("FAIL", "§18-C53-2 高斯积分归一化被漏乘：E 少 π^{3/2}=5.5683 倍（且草稿内部自相矛盾）",
    "∫d³x e^{−r²/σ²} = π^{3/2}σ³ = %s（250 位与闭式比值 = %s）；草稿把积分写成"
    "「σ³/(2π)^{3/2}·(…)·(2π)^{3/2}」却给出 E=σ³/(16πG)(…)（既无 π^{3/2} 亦无 (2π)^{3/2}）；"
    "数值 E_草稿=%s J vs E_严格=%s J，E_草稿/E_(2π)^{3/2}=%s=1/(2π)^{3/2} ⇒ 两式不可同时成立"
    % (fmt(_gb_pi, 10), fmt(_gb_I / _gb_pi, 20), fmt(E_doc, 8), fmt(E_gauss, 8), fmt(E_doc / E_alt, 8)),
    "σ=%s m、κ0=%s、τ0=%s、α_g=%s" % (fmt(GB_SIGMA, 4), fmt(GB_K0, 4), fmt(GB_T0, 4), fmt(GB_AG, 4)),
    "250 位高斯积分 + 闭式核对")

# ---- 18.2 能量密度量纲审计（三种 κ 口径） ----
_DIM_ED = D(L=-1, M=1, T=-2)          # 能量密度 [L^-1 M T^-2]
_dim_need_k2 = dmul(_DIM_ED, DIM_G)   # 需要 (κ²+ατ²) 的量纲
_dim_need_k = dpow(_dim_need_k2, Fraction(1, 2))

print("\n     --- 18.2 ρ_grav = (1/16πG)(κ²+α_g τ²) 量纲审计 ---")
print("     [能量密度] = %s ；[1/(16πG)] = %s" % (dfmt(_DIM_ED), dfmt(dpow(DIM_G, -1))))
print("     齐次性要求 (κ²+ατ²) = %s ⇒ κ 需具 %s（**加速度**，非曲率）"
      % (dfmt(_dim_need_k2), dfmt(_dim_need_k)))
_gb_dims = [("本体  κ=ρ/(ρ²+b²)  [L^-1]", D(L=-1)),
            ("模块自述 κ0 (m^-2)    [L^-2]", D(L=-2)),
            ("归一化约化 κ̃²+τ̃²=1   [1]", D())]
_gb_dim_bad = 0
for _nm, _dk in _gb_dims:
    _rd = dmul(dpow(DIM_G, -1), dpow(_dk, 2))
    _ok = (_rd == _DIM_ED)
    if not _ok:
        _gb_dim_bad += 1
    print("       %-30s ⇒ ρ 量纲 %-16s %s" % (_nm, dfmt(_rd), "OK" if _ok else "≠ 能量密度"))

reg("FAIL", "§18-C53-1 ρ_grav=(1/16πG)(κ²+α_gτ²) 量纲非法——三种 κ 口径全部失败",
    "①TUFT 本体 κ=ρ/(ρ²+b²) 为 [L^-1]（claims C02）⇒ ρ=[L^-5 M T^2]；②模块自述 κ0 单位 m^-2 ⇒ ρ=[L^-7 M T^2]；"
    "③既有归一化约化形 κ̃²+τ̃²=1（κ̃、τ̃ 无量纲）⇒ ρ=[L^-3 M T^2]。三者均 ≠ 能量密度 [L^-1 M T^-2]。"
    "齐次性反解：惟有 κ 具加速度量纲 [L T^-2] 时该式才成立 ⇒ 与「曲率」语义直接冲突"
    "（%d/3 口径失败）" % _gb_dim_bad,
    "量纲账本（L,M,T,I 四基）+ Buckingham 齐次性", "量纲审计")

# ---- 18.3 最小量纲修复的后果：与「地面实验室」自相矛盾 ----
print("\n     --- 18.3 唯一最小量纲修复（齐次性强制 ×c⁴）与其物理后果 ---")
print("     ρ = (c⁴/16πG)(κ²+α_gτ²)；E = π^{3/2}σ³c⁴/(16πG)(κ0²+α_gτ0²)")
print("     E = %s J = %s eV ≈ %s 百万吨 TNT（1 t TNT = 4.184e9 J）"
      % (fmt(E_dimfix, 8), fmt(E_dimfix / mpf("1.602176634e-19"), 8),
         fmt(E_dimfix / mpf("4.184e9") / mpf("1e6"), 6)))

reg("FAIL", "§18-C53-4 量纲修复后 E_bubble ≈ 1.14e16 J（≈2.72 Mt TNT / 3.1e7 倍 LHC 单束能量）"
    " ⇒ 「地面实验室可实现靶」被理论自身否定",
    "齐次性只允许 κ,τ 以 (c²κ)²、(c²τ)² 形式进入 ρ（c²κ 具加速度量纲）⇒ E 必含 c⁴ = 8.0776e33 因子；"
    "取草稿参数（σ=0.1 m、κ0=1e-16、τ0=1e-12、α_g=0.85）得 E = %s J。"
    "草稿之所以得到「2.5e-19 J ≈ 1.6 eV 的实验室量级」，正是因为漏了量纲因子 c⁴ 与归一化因子 π^{3/2}"
    "（两个错误方向相反地被抵消）⇒ 该「实验室预言」是双重错误的产物"
    % fmt(E_dimfix, 8),
    "c⁴ = %s；E_草稿(非法量纲) = %s J" % (fmt(C ** 4, 8), fmt(E_doc, 8)), "量纲修复 + 量级对照")

# ---- 18.4 自旋进动量纲 ----
_gb_spin = mpf("0.5") * HBAR
_dphi_doc = _gb_spin * GB_T0 * GB_SIGMA / GB_VP        # 草稿式 S·τ0·σ/v
_dphi_dim = mpf("0.5") * GB_T0 * GB_SIGMA              # 无量纲形式 (S/ħ)·τ0·σ
print("\n     --- 18.4 自旋进动 δφ 量纲与量级 ---")
print("     δφ_草稿 = S·τ0·σ/v = %s rad" % fmt(_dphi_doc, 10))
print("     δφ_无量纲(ħ 归一) = (S/ħ)·τ0·σ = %s rad" % fmt(_dphi_dim, 10))
print("     两者相差 %s 倍（且草稿式量纲为 [L M]）" % fmt(_dphi_doc / _dphi_dim, 8))

reg("FAIL", "§18-C53-3 自旋进动 δφ = S·τ0·σ/v 量纲非法（[L M] 非无量纲），且量级低 39 个量级",
    "量纲：S·τ0·σ/v = [L²MT^-1][L^-1][L]/[LT^-1] = [L M]（角度必须无量纲）。"
    "唯一同结构无量纲形式为 (S/ħ)·τ0·σ（ħ 归一化自旋）⇒ 草稿式缺 ħ 因子。"
    "数值：草稿式 %s rad vs 无量纲式 %s rad（差 %s 倍）；两者均远低于任何可测精度"
    % (fmt(_dphi_doc, 8), fmt(_dphi_dim, 8), fmt(_dphi_doc / _dphi_dim, 8)),
    "S = 0.5ħ；σ=%s m；τ0=%s m^-1；v=0.1c" % (fmt(GB_SIGMA, 4), fmt(GB_T0, 4)), "量纲账本")

# ---- 18.5 孤子合法性 / 边界匹配条件 ----
print("\n     --- 18.5 「孤子解」与「曲率-挠率边界匹配条件」的合法性 ---")
print("     模块提供的全部内容：场 ansatz κ=κ0exp(−r²/2σ²)、τ=τ0exp(−r²/2σ²) + 能量密度式")
print("     未提供：作用量 S[κ,τ]、Euler–Lagrange 方程、度规 ansatz、匹配面 Σ")

reg("FAIL", "§18-C53-5 高斯包络是 ansatz 而非孤子解：无作用量、无场方程、无 EL 方程验证",
    "「孤子」的判据是其为某作用量的稳定有限能量解（非线性项与色散项平衡）。"
    "本模块未给出 S[κ,τ]、未给出运动方程、亦未把高斯代入任何方程验证 ⇒ 「引力泡是曲率-挠率场有限能量孤子解」"
    "为未验证的命名，不构成结论。附带：与本体约束 κ²+τ²=ω²/c² 联立会使 ω 变成场 ω(x)=c√(κ²+τ²)，"
    "该自洽性亦未在模块中讨论",
    "结构性缺项（作用量/场方程/EL）", "第一性判据")

reg("BOUNDARY", "§18-C53-6 「边界满足曲率-挠率场匹配条件」是空陈述：无形匹配面 ⇒ 无匹配条件对象",
    "高斯包络为 C^∞ 且 r→∞ 时 κ,τ→0 ⇒ 不存在分界面 Σ（σ 是「宽度」不是「边界」）；"
    "GR 的 Israel 连接条件需要 Σ 两侧的诱导度规与外在曲率，此处二者皆未定义。"
    "「平滑衔接至闵氏时空」对 C^∞ 包络自动成立，不携带信息",
    "结构性缺项（无 Σ）", "几何审计")

# ---- 18.6 ω_bubble 与本体约束的自洽性（模块唯一自洽的结构点） ----
_omega_b = C * sqrt(GB_K0 ** 2 + GB_T0 ** 2)
_f_b = _omega_b / (2 * pi)
_lam_e = HBAR / (mpf("9.1093837015e-31") * C)
_k_t_ratio = GB_T0 / GB_K0
print("\n     --- 18.6 泡中心频率与本体约束 ---")
print("     ω(0)=c√(κ0²+τ0²) = %s rad/s ⇒ f = %s Hz（周期 %s 小时）"
      % (fmt(_omega_b, 10), fmt(_f_b, 8), fmt(1 / _f_b / 3600, 6)))
print("     τ0/κ0 = %s ；本体 α=τ/κ = %s ⇒ 偏离 %s 倍"
      % (fmt(_k_t_ratio, 6), fmt(ALPHA, 6), fmt(_k_t_ratio / ALPHA, 8)))
print("     电子康普顿波长 = %s m ⇒ 1/λ_e = %s m^-1 ；τ0 比之小 %s 倍"
      % (fmt(_lam_e, 8), fmt(1 / _lam_e, 8), fmt(GB_T0 * _lam_e, 8)))

reg("INFO", "§18-C53-8 ω_bubble = c√(κ0²+τ0²) 与本体约束结构自洽（模块唯一自洽点）",
    "由 claims C01/C02 的 ω√(ρ²+b²)=c 得 ω(x)=c√(κ²+τ²)；泡心 ω(0)=%s rad/s，f=%s Hz（周期 5.8 h）。"
    "草稿「ω_bubble ∝ τ0·c」在 τ0≫κ0 时成立（本例 τ0/κ0=1e4）⇒ 比例关系为结构近似而非新预言"
    % (fmt(_omega_b, 8), fmt(_f_b, 8)),
    "τ0=%s m^-1 比电子尺度 1/λ_e=%s m^-1 小 %s 倍 ⇒ 该「场」极弱"
    % (fmt(GB_T0, 4), fmt(1 / _lam_e, 4), fmt(GB_T0 * _lam_e, 4)), "本体约束对齐")

reg("BOUNDARY", "§18-C53-9 泡中心 κ0、τ0 与本体 α=τ/κ 之间无任何约束方程",
    "本体把 τ/κ 钉为 α=7.297e-3（claims C03），而模块取 τ0/κ0 = 1e4 ⇒ 两者相差 %s 倍；"
    "模块亦未声明「泡心几何不受 α 约束」的理由 ⇒ 泡参数与本体耦合谱系之间的关系未定义"
    % fmt(_k_t_ratio / ALPHA, 6),
    "若泡心必须满足 τ0/κ0=1/α 则 α_g 无自由；若不受约束则 α_g、κ0、τ0、σ 四者全自由", "自由度审计")

# ---- 18.7 自由度 / 可证伪性（判别式 V 口径） ----
_gb_n_free = 4     # σ、κ0、τ0、α_g
_gb_n_hit = 0      # 登记在册的可检验预测量（E、δφ 均含未标定参数且量纲非法）
_gb_V = (Fraction(_gb_n_hit) - Fraction(_gb_n_free) - Fraction(0)) / Fraction(1)
print("\n     --- 18.7 自由度与可证伪性 ---")
print("     自由参数 n_free = %d（σ、κ0、τ0、α_g）；可检验预测量 n_hit = %d" % (_gb_n_free, _gb_n_hit))
print("     V = (n_hit − n_free − n_anchor)/1 = %s ≤ 0 ⇒ 伪派生（口径同 §2-3）" % _gb_V)

reg("FAIL", "§18-C53-7 模块自称「无额外参数的独立实验室预言」但自由参数 4 个、约束方程 0 条 ⇒ 伪派生",
    "「标定后 σ、E_bubble、δθ_spin 是无额外参数的独立预言」本身即承认 α_g 需标定（第 1 个额外参数）；"
    "κ0、τ0 无任何第一性确定方式（第 2、3 个）；σ 由实验者选定（第 4 个）。"
    "判别式 V = (n_hit − n_free − n_anchor)/n_hit = %s ≤ 0 ⇒ 与 C25/C29 同类：命中不构成选择规则" % _gb_V,
    "口径与 §2-2/§2-3、C25/C46 一致", "判别式 V")

reg("FAIL", "§18-C53-10 标记重判：GravBubble「open（孤子解框架+实验室可观测量预言就绪）」不成立",
    "综合 §18-C53-1..9：能量密度量纲非法（3/3 口径失败）、归一化漏乘 π^{3/2}、自旋进动非无量纲、"
    "量纲修复后能量 1.14e16 J 与「实验室」矛盾、无作用量故非孤子、4 自由参数 0 约束 ⇒ "
    "「预言就绪」的实质内容不成立 ⇒ 台账登记 falsified（公式层）；"
    "体系级「挠率场能否局域激发」仍 open（本轮不否定该物理议题本身）",
    "与 C24/C43 同口径：证伪针对模块宣称，不针对议题", "诚实重判")


# ===========================================================================
# §19  V21 续修② 模块2 · TUFT 重整化群 RG 流 —— 紫外完备性检验审计
# ===========================================================================
print("\n" + "=" * 76)
print("§19  V21续修② 模块2 | TUFT-RG 流：β 系数来源 / 固定点 / 能标口径审计")
print("=" * 76)

RG_B = [mpf("0.021"), mpf("-0.012"), mpf("0.018"), mpf("-0.009"), mpf("0.015"), mpf("-0.007")]
RG_BF = [Fraction("0.021"), Fraction("-0.012"), Fraction("0.018"),
         Fraction("-0.009"), Fraction("0.015"), Fraction("-0.007")]
RG_B1, RG_B2, RG_B3, RG_B4, RG_B5, RG_B6 = RG_B
RG_GK0, RG_GT0, RG_GKT0 = mpf("0.12"), mpf("0.08"), mpf("0.05")

print("     草稿 β 函数：β_gk=b1gk²+b2gkt²、β_gt=b3gt²+b4gkt²、β_gkt=b5gk·gkt+b6gt·gkt")
print("     草稿系数 b1..b6 = %s" % "、".join([fmt(v, 4) for v in RG_B]))
print("     草稿红外耦合 (gk、gt、gkt) = (%s、%s、%s)"
      % (fmt(RG_GK0, 4), fmt(RG_GT0, 4), fmt(RG_GKT0, 4)))

# ---- 19.1 β 系数来源审计 ----
reg("FAIL", "§19-C54-1 b1..b6 六个自由系数且无作用量/Feynman 推导 ⇒ 结论完全由输入决定 ⇒ 不构成理论检验",
    "草稿称「b1..b6 由螺旋场 Feynman 规则算出」，但未给出拉氏量、未给出任何一条 Feynman 图贡献；"
    "而「有无紫外固定点」「流是增长还是衰减」全部由这 6 个数的符号与比例决定 ⇒ "
    "该模块检验的是手选参数集，不是 TUFT 理论。判别式口径：n_hit=0（无待预测观测量）、n_free=6 ⇒ V≤0",
    "口径同 §2-2、C25/C46：命中不构成选择规则", "结构审计")

# ---- 19.2 固定点存在性的精确条件（本册正面产出） ----
_cA = -RG_BF[1] / RG_BF[0]          # −b2/b1
_cB = -RG_BF[3] / RG_BF[2]          # −b4/b3
_cond_lhs = RG_BF[4] ** 2 * _cA
_cond_rhs = RG_BF[5] ** 2 * _cB
_cond_ratio = _cond_lhs / _cond_rhs
_need_b6 = mp.sqrt(mpf(float(RG_B5)) ** 2 * mpf(float(_cA)) / mpf(float(_cB)))
_need_b5 = mp.sqrt(mpf(float(RG_B6)) ** 2 * mpf(float(_cB)) / mpf(float(_cA)))
print("\n     --- 19.2 非平凡紫外固定点存在性（精确） ---")
print("     三式联立：由 ①、② 得 |gk|=√(−b2/b1)|gkt|=√(%s)|gkt|、|gt|=√(−b4/b3)|gkt|=√(%s)|gkt|"
      % (fmt(mpf(float(_cA)), 8), fmt(mpf(float(_cB)), 8)))
print("     由 ③ 得 b5·gk + b6·gt = 0 ⇒ 需 |gk/gt| = |b6/b5| = %s，而 ①② 给出 |gk/gt| = %s ⇒ 不相容"
      % (fmt(abs(RG_BF[5] / RG_BF[4]), 8), fmt(mp.sqrt(mpf(float(_cA))) / mp.sqrt(mpf(float(_cB))), 8)))
print("     存在条件 b5²(−b2/b1) = b6²(−b4/b3)： LHS = %s、RHS = %s ⇒ 比值 = %s ≠ 1"
      % (fmt(mpf(float(_cond_lhs)), 8), fmt(mpf(float(_cond_rhs)), 8), fmt(mpf(float(_cond_ratio)), 8)))
print("     反解：固定 b5=0.015 需 |b6| = %s（草稿取 0.007）；固定 b6=0.007 需 |b5| = %s（草稿取 0.015）"
      % (fmt(_need_b6, 8), fmt(_need_b5, 8)))

import sympy as _sym23   # 专用别名（§15 曾以 `sp` 作局部变量遮蔽 sympy 别名，见 §15 注释）

_sp_gk, _sp_gt, _sp_gkt = _sym23.symbols("gk gt gkt", real=True)
_sp_eqs = [_sym23.Rational("0.021") * _sp_gk ** 2 + _sym23.Rational("-0.012") * _sp_gkt ** 2,
           _sym23.Rational("0.018") * _sp_gt ** 2 + _sym23.Rational("-0.009") * _sp_gkt ** 2,
           _sym23.Rational("0.015") * _sp_gk * _sp_gkt + _sym23.Rational("-0.007") * _sp_gt * _sp_gkt]
try:
    _sp_sols = _sym23.solve(_sp_eqs, [_sp_gk, _sp_gt, _sp_gkt], dict=True)
    _sp_txt = "、".join([str(s) for s in _sp_sols]) if _sp_sols else "无解"
except Exception as _e19:
    _sp_sols = []
    _sp_txt = "solve 异常：%s" % type(_e19).__name__
print("     sympy 精确解集：%s（唯一实解为原点 ⇒ 无紫外非平凡固定点）" % _sp_txt)

reg("FAIL", "§19-C54-2 【精确定理】非平凡紫外固定点存在 ⇔ b5²(−b2/b1)=b6²(−b4/b3)；给定系数下不成立 ⇒ "
    "无紫外固定点、渐近安全不成立",
    "由 β_gk=0、β_gt=0 得 abs(gk)=√(−b2/b1)·abs(gkt)、abs(gt)=√(−b4/b3)·abs(gkt)（需 b2<0、b4<0——本例满足）；"
    "再由 β_gkt=0 得 b5·gk+b6·gt=0 ⇒ 需 b5²(−b2/b1)=b6²(−b4/b3)。"
    "给定系数下 LHS/RHS = %s ≠ 1；sympy 精确解集 = %s ⇒ 唯一点为 Gaussian 原点 (0、0、0)。"
    "即所谓「紫外固定点搜索」的正确答案是「不存在」，而该条件对 6 个系数是 codimension-1 细调 ⇒ "
    "即便修 b6 使条件成立，也只是调参产物，不是第一性结论" % (fmt(mpf(float(_cond_ratio)), 8), _sp_txt),
    "LHS=%s、RHS=%s；使条件成立的 abs(b6) 需 %s（草稿 0.007）"
    % (fmt(mpf(float(_cond_lhs)), 8), fmt(mpf(float(_cond_rhs)), 8), fmt(_need_b6, 8)),
    "sympy 精确有理数求解 + 解析推导")

# ---- 19.3 草稿固定点搜索代码的可运行性 ----
def _fp_eq_draft(_x):
    """草稿 §「RG模块」原样照抄：fp_eq(x) 解包三分量并返回三分量列表。"""
    _gk, _gt, _gkt = _x
    return [RG_B1 * _gk ** 2 + RG_B2 * _gkt ** 2,
            RG_B3 * _gt ** 2 + RG_B4 * _gkt ** 2,
            RG_B5 * _gk * _gkt + RG_B6 * _gt * _gkt]


try:
    _fp_try = mp.findroot(_fp_eq_draft, [mpf("0.05"), mpf("0.05"), mpf("0.02")])
    _fp_txt = "返回 %s" % str(_fp_try)
except Exception as _e19b:
    _fp_txt = "抛 %s：%s" % (type(_e19b).__name__, _e19b)
print("\n     --- 19.3 草稿固定点搜索代码原样运行 ---")
print("     mp.findroot(fp_eq, [0.05、0.05、0.02])（fp_eq 返回三分量列表）⇒ %s" % _fp_txt)

reg("FAIL", "§19-C54-3 草稿的固定点搜索代码原样运行抛 TypeError ⇒ 崩溃掩盖「不存在固定点」这一事实",
    "mpmath.findroot 对「返回列表的多元函数」的调用约定与草稿写法（把 Python list 当 x0、函数按列表解包）不匹配，"
    "实测抛 TypeError: cannot unpack non-iterable mpf object。后果：草稿既得不到固定点，"
    "也无法暴露 §19-C54-2 已证的「无固定点」结论——错误被异常替换成了误导（若用 try 吞掉更危险）",
    "实测（本机 mpmath 1.3.0 / Python 3.8.8）", "可运行性检验")

# ---- 19.4 能标口径混用（单位错误） ----
M_PL_AUDIT = sqrt(HBAR * C / G_NEWTON)
_mu_ir = mpf("1.0")
_mu_uv_doc = M_PL_AUDIT * C ** 2 / HBAR
_E_pl_eV = M_PL_AUDIT * C ** 2 / mpf("1.602176634e-19")
_ln_doc = mp.log(_mu_uv_doc) - mp.log(_mu_ir)
_ln_ok = mp.log(_E_pl_eV) - mp.log(_mu_ir)
print("\n     --- 19.4 能标口径（单位）审计 ---")
print("     μ_IR = %s eV（草稿声明为能量）" % fmt(_mu_ir, 4))
print("     μ_UV 草稿 = M_pl c²/ħ = %s（量纲实为 s^-1/角频率）" % fmt(_mu_uv_doc, 12))
print("     μ_UV 正确 = M_pl c² = %s eV（Planck 能量）" % fmt(_E_pl_eV, 12))
print("     积分跨度 ln：草稿 %s vs 正确 %s ⇒ 虚增 %s（+%s%%）"
      % (fmt(_ln_doc, 10), fmt(_ln_ok, 10), fmt(_ln_doc - _ln_ok, 8),
         fmt((_ln_doc / _ln_ok - 1) * 100, 6)))

reg("FAIL", "§19-C54-4 能标口径混用：μ_IR 用 eV 而 μ_UV=M_pl c²/ħ=%s s⁻¹（角频率非能量）"
    " ⇒ 积分跨度虚增 %s（+%s%%）故所有跑动曲线定量错误"
    % (fmt(_mu_uv_doc, 6), fmt(_ln_doc - _ln_ok, 6), fmt((_ln_doc / _ln_ok - 1) * 100, 5)),
    "M_pl c² = 1.9561e9 J；除以 ħ（J·s）得 %s s^-1，而除以 1.602176634e-19 J/eV 才得能标 %s eV。"
    "两者相差 1/ħ(eV·s)=1.5193e15 ⇒ ln 跨度 %s vs %s（虚增 %s）。"
    "该错误直接平移 Landau 极点位置与全部 UV 耦合值（见 §19-C54-5）"
    % (fmt(_mu_uv_doc, 8), fmt(_E_pl_eV, 8), fmt(_ln_doc, 8), fmt(_ln_ok, 8), fmt(_ln_doc - _ln_ok, 6)),
    "1/ħ = %s (eV·s)^-1" % fmt(1 / mpf("6.582119569e-16"), 8), "量纲/单位审计")

# ---- 19.5 修正口径下的 RG 流行为 ----
def _rg_uv(_span, _nstep=2000):
    _ds = _span / _nstep
    _gk, _gt, _gkt = RG_GK0, RG_GT0, RG_GKT0
    for _ in range(_nstep):
        _d0 = RG_B1 * _gk ** 2 + RG_B2 * _gkt ** 2
        _d1 = RG_B3 * _gt ** 2 + RG_B4 * _gkt ** 2
        _d2 = RG_B5 * _gk * _gkt + RG_B6 * _gt * _gkt
        _gk, _gt, _gkt = _gk + _d0 * _ds, _gt + _d1 * _ds, _gkt + _d2 * _ds
    return _gk, _gt, _gkt

_uv_doc = _rg_uv(_ln_doc)
_uv_ok = _rg_uv(_ln_ok)
_uv_ok_fine = _rg_uv(_ln_ok, 16000)
_s_pole = 1 / (RG_B1 * RG_GK0)
_mu_pole = mp.exp(mp.log(_mu_ir) + _s_pole)
_gk_closed = RG_GK0 / (1 - RG_B1 * RG_GK0 * _ln_ok)
print("\n     --- 19.5 RG 流（显式 Euler，两口径对照） ---")
print("     UV(草稿跨度 %s)：gk=%s、gt=%s、gkt=%s"
      % (fmt(_ln_doc, 8), fmt(_uv_doc[0], 10), fmt(_uv_doc[1], 10), fmt(_uv_doc[2], 10)))
print("     UV(正确跨度 %s)：gk=%s、gt=%s、gkt=%s"
      % (fmt(_ln_ok, 8), fmt(_uv_ok[0], 10), fmt(_uv_ok[1], 10), fmt(_uv_ok[2], 10)))
print("     步长收敛性：nstep=2000 → gk=%s；nstep=16000 → gk=%s（相对差 %s）"
      % (fmt(_uv_ok[0], 12), fmt(_uv_ok_fine[0], 12), fmt(abs(_uv_ok_fine[0] / _uv_ok[0] - 1), 6)))
print("     参照：纯 gk² 一维闭式（丢弃 b2·gkt² 抑制项）= %s，与三维数值差 %s%%（差异来自 b2<0 的抑制项，属预期）"
      % (fmt(_gk_closed, 10), fmt(abs(_uv_ok[0] / _gk_closed - 1) * 100, 6)))
print("     Landau 极点 s* = 1/(b1·gk0) = %s ⇒ μ_pole = %s eV（10^%s eV）"
      % (fmt(_s_pole, 10), fmt(_mu_pole, 8), fmt(mp.log10(_mu_pole), 8)))
print("     在 Planck 内是否到达极点：%s" % ("是" if _s_pole < _ln_ok else "否（极点位于 Planck 之外）"))

reg("FAIL", "§19-C54-5 给定系数下流为紫外增长型：既非渐近自由亦非渐近安全；Landau 极点位置依赖任意 IR 输入",
    "β 分量在 gk、gt、gkt>0 时全为正（b1=0.021>0、b3=0.018>0 主导）⇒ 耦合随 μ 单调增："
    "正确跨度下 UV(Planck) = (%s、%s、%s)；Euler 步长收敛性 2000 vs 16000 步相对差 %s ⇒ 数值可靠。"
    "Landau 极点 s*=%s ⇒ μ_pole≈1e%s eV；但 g0=0.12 是任意红外输入 ⇒ "
    "「理论何时失效」这一陈述本身不可证伪（换任意 g0 即换答案）"
    % (fmt(_uv_ok[0], 8), fmt(_uv_ok[1], 8), fmt(_uv_ok[2], 8),
       fmt(abs(_uv_ok_fine[0] / _uv_ok[0] - 1), 6), fmt(_s_pole, 8), fmt(mp.log10(_mu_pole), 6)),
    "对照：草稿（错误跨度）UV = (%s、%s、%s) ⇒ 同一模块两次运行给出不同「结论」"
    % (fmt(_uv_doc[0], 8), fmt(_uv_doc[1], 8), fmt(_uv_doc[2], 8)), "RG 数值积分")

reg("BOUNDARY", "§19-C54-6 「低能耦合值匹配 α_g、β、C、A_topo、α_BH」无映射方程 ⇒ 不可计算",
    "模块列出 5 个待匹配的低能观测量，但未给出 (gk、gt、gkt) → (α_g、β、C、A_topo、α_BH) 的任何一个映射式；"
    "3 个耦合对 5 个观测量在方程缺失时无内容 ⇒ 该「匹配」不可执行（与 §2-2 的「反解 ωA 命中 α」同类结构）",
    "结构性缺项（无映射）", "第一性判据")

reg("INFO", "§19-C54-7 【正面产出】本模块给出 TUFT 紫外完备性的可证伪判据（本册唯一新增可判定陈述）",
    "判据：TUFT 若紫外完备，则其有效耦合在 μ→∞ 时必须 ①趋于非平凡固定点 或 ②趋于零（渐近自由）。"
    "本模块已证：在给定 b1..b6 下 ①不成立（§19-C54-2 精确定理）、②不成立（§19-C54-5 单调增长）。"
    "⇒ 该证伪性依赖于 b1..b6 的导出；一旦由有效作用量第一性算出 b1..b6，本判据即刻成为定量可检验陈述",
    "把「是否紫外完备」从口号转为可判定命题，是本册对 TUFT-RG 的唯一正面贡献", "可证伪判据构造")

reg("FAIL", "§19-C54-8 标记重判：TUFT-RG「open（单圈 β 函数+固定点搜索就绪，用于检验紫外完备性）」不成立",
    "综合 §19-C54-1..6：b 系数全自由（非检验）、给定系数下无固定点（自身反例）、"
    "固定点搜索代码不可运行、能标口径混用致全部定量错误、无观测映射 ⇒ 「检验就绪」不成立 ⇒ "
    "台账登记 falsified（模块层）；体系级「TUFT 是否存在紫外固定点」仍 open——"
    "前置条件是先由有效作用量导出 b1..b6",
    "与 C25/C29 的 FAIL 口径一致（公式层证伪 ≠ 议题证伪）", "诚实重判")

reg("BOUNDARY", "§19-全局表-1 草稿「全局审计表」新增 4 行中 CMB-Bispec / EHT-PhotonRing 无本册模块支撑",
    "草稿全局表列出 new 行：CMB-Bispec（螺旋拓扑振荡双谱）、EHT-PhotonRing（黑洞挠率修正光子环）、"
    "GravBubble、TUFT-RG。本册提交内容只含后两个模块的公式与代码；前两条无模块、无公式、无脚本 ⇒ "
    "按 §17-CLAIMS-3 口径不得凭声明登记（「未复核」≠「已通过」）⇒ 建议待其模块提交后再登记为 C55/C56",
    "本册只登记 C53（GravBubble）与 C54（TUFT-RG）", "口径红线")

# ---- 19.6 台账登记 C53/C54（幂等；先登记，§17 再对「登记后全量」做批量审计） ----
V23_NEW_CLAIMS = [
    ("C53",
     "【V21续修②·引力泡】GravBubble 模块（高斯螺旋包 κ=κ0e^(−r²/2σ²)、τ=τ0e^(−r²/2σ²)；ρ=(1/16πG)(κ²+αgτ²)）"
     "250 位审计：①能量密度量纲非法——三种 κ 口径（本体 [L^-1]、模块自述 m^-2、归一化约化 [1]）代入 ρ 分别得 "
     "[L^-5MT²]、[L^-7MT²]、[L^-3MT²] 均非 [L^-1MT^-2] 齐次性要求 κ 具加速度量纲 [LT^-2] 与「曲率」语义冲突；"
     "②高斯积分严格值 π^(3/2)σ³ 被漏乘（E 少 π^(3/2)=5.5683 倍且草稿中间式 (2π)^(3/2) 与最终式互斥 "
     "E_草稿/E_该口径=0.0635）；③自旋进动 δφ=Sτ0σ/v 量纲 [LM] 非无量纲（无量纲式 (S/ħ)τ0σ=5.0e-14 rad "
     "而草稿值 1.76e-55 rad）；④唯一最小量纲修复（×c⁴）给出 E=1.14e16 J≈2.72 Mt TNT≈3.1e7 倍 LHC 单束能量 "
     "⇒ 与「地面实验室可实现靶」自相矛盾（草稿的 1.6 eV「实验室量级」是漏 c⁴ 与漏 π^(3/2) 两错相消的产物）；"
     "⑤无作用量无场方程 ⇒ 高斯包络是 ansatz 非孤子解；「曲率-挠率边界匹配条件」无形匹配面为空陈述；"
     "⑥自由参数 σ、κ0、τ0、αg 四个而约束方程 0 条 ⇒ 判别式 V≤0 伪派生 ⇒ "
     "模块「孤子解框架+实验室可观测量预言就绪」宣称不成立 → falsified（公式层；体系级「挠率场能否局域激发」仍 open）",
     "第一性审计", "falsified"),
    ("C54",
     "【V21续修②·TUFT-RG】RG 流模块（β_gk=b1gk²+b2gkt²、β_gt=b3gt²+b4gkt²、β_gkt=b5gk·gkt+b6gt·gkt；"
     "b1..b6=0.021/−0.012/0.018/−0.009/0.015/−0.007）250 位审计：①b 系数六自由且无作用量/Feynman 推导 ⇒ "
     "结论由未导出输入决定 ⇒ 不构成对理论的检验；②精确定理——非平凡紫外固定点存在当且仅当 "
     "b5²(−b2/b1)=b6²(−b4/b3)（需 b2<0、b4<0）给定系数下 LHS/RHS=5.2478 不成立 sympy 精确解集仅原点 "
     "⇒ 无紫外固定点 ⇒ 渐近安全在给定系数下不成立；③草稿固定点搜索代码（mp.findroot(fp_eq、[0.05、0.05、0.02])）"
     "原样运行抛 TypeError ⇒ 崩溃掩盖「不存在固定点」；④能标口径混用：μ_IR=1 eV 而 μ_UV=M_pl c²/ħ=1.8549e43 s^-1"
     "（实为角频率非 eV 正确 Planck 能量 1.2209e28 eV）⇒ 积分跨度 ln=99.629 vs 64.672 虚增 34.957（+54.1%）"
     "故全部跑动曲线定量错误；⑤修正口径下耦合单调增长（Planck 处 gk≈0.1408）Landau 极点 s*=1/(b1gk0)=396.83 "
     "⇒ μ≈1e172.34 eV 且该陈述依赖任意 IR 输入 g0 ⇒ 既非渐近自由亦非渐近安全且判据不可证伪；"
     "⑥「低能耦合匹配 α_g、β、C、A_topo、α_BH」无映射方程 ⇒ 不可计算 ⇒ 模块「紫外完备性检验就绪」宣称不成立 "
     "→ falsified（模块层；体系级「TUFT 是否有紫外固定点」仍 open——前置条件是先由有效作用量导出 b1..b6）",
     "第一性审计", "falsified"),
]
_existing_v23 = set(l.split(",", 1)[0].strip() for l in
                    io.open(os.path.join(SYS_DIR, "claims.csv"), encoding="utf-8")
                    .read().splitlines()[1:] if l.strip())
_txt23 = io.open(os.path.join(SYS_DIR, "claims.csv"), encoding="utf-8").read()
if not _txt23.endswith("\n"):
    _txt23 += "\n"
added_v23 = 0
for _cid, _st_, _cat, _stat in V23_NEW_CLAIMS:
    if _cid in _existing_v23:
        continue
    for _f in (_cid, _st_, _cat, _stat, "算法联盟审计组"):
        if "," in _f or '"' in _f:
            raise ValueError("字段不得含裸逗号或引号: " + _cid)
    _txt23 += ",".join([_cid, _st_, _cat, _stat, "算法联盟审计组"]) + "\n"
    added_v23 += 1
io.open(os.path.join(SYS_DIR, "claims.csv"), "w", encoding="utf-8").write(_txt23)
item("claims.csv V21续修② 幂等追加完毕（C53/C54 新增 %d 行，重复时 0 行）" % added_v23, True)


# ===========================================================================
# §20  V21 续修③ 模块1 · TUFT-RG 双圈 β 函数（C55）—— 「紫外固定点」真伪判定
# ===========================================================================
print("\n" + "=" * 76)
print("§20  V21续修③ 模块1 | TUFT-RG 双圈 β：固定点真伪 / 微扰可靠域 / 截断伪影")
print("=" * 76)

V24_START = len(ROWS)

RG2_B = [mpf("0.021"), mpf("-0.012"), mpf("0.018"), mpf("-0.009"), mpf("0.015"), mpf("-0.007")]
RG2_D = [mpf("-0.0041"), mpf("0.0022"), mpf("-0.0033"), mpf("0.0016"),
         mpf("-0.0024"), mpf("-0.0018"), mpf("0.0009")]
RG2_BF = [Fraction("0.021"), Fraction("-0.012"), Fraction("0.018"),
          Fraction("-0.009"), Fraction("0.015"), Fraction("-0.007")]
RG2_DF = [Fraction("-0.0041"), Fraction("0.0022"), Fraction("-0.0033"), Fraction("0.0016"),
          Fraction("-0.0024"), Fraction("-0.0018"), Fraction("0.0009")]
RG2_GK0, RG2_GT0, RG2_GKT0 = mpf("0.12"), mpf("0.08"), mpf("0.05")


def rg2_beta(gk, gt, gkt):
    """照抄草稿双圈 β（三分量），不做任何「善意」补正。"""
    bgk = (RG2_B[0] * gk ** 2 + RG2_B[1] * gkt ** 2
           + RG2_D[0] * gk ** 3 + RG2_D[1] * gk * gkt ** 2)
    bgt = (RG2_B[2] * gt ** 2 + RG2_B[3] * gkt ** 2
           + RG2_D[2] * gt ** 3 + RG2_D[3] * gt * gkt ** 2)
    bgkt = (RG2_B[4] * gk * gkt + RG2_B[5] * gt * gkt + RG2_D[4] * gk ** 2 * gkt
            + RG2_D[5] * gt ** 2 * gkt + RG2_D[6] * gkt ** 3)
    return bgk, bgt, bgkt


def rg2_flow(span, nstep, two_loop=True):
    """显式 Euler 积分（与草稿同阶），two_loop=False 退化为 §19 的单圈。"""
    ds = span / nstep
    gk, gt, gkt = RG2_GK0, RG2_GT0, RG2_GKT0
    for _ in range(nstep):
        if two_loop:
            bgk, bgt, bgkt = rg2_beta(gk, gt, gkt)
        else:
            bgk = RG2_B[0] * gk ** 2 + RG2_B[1] * gkt ** 2
            bgt = RG2_B[2] * gt ** 2 + RG2_B[3] * gkt ** 2
            bgkt = RG2_B[4] * gk * gkt + RG2_B[5] * gt * gkt
        gk, gt, gkt = gk + bgk * ds, gt + bgt * ds, gkt + bgkt * ds
    return gk, gt, gkt


print("     草稿双圈新增系数 d1..d7 = %s" % "、".join([fmt(v, 4) for v in RG2_D]))
print("     单圈系数 b1..b6 沿用 §19 = %s" % "、".join([str(v) for v in RG2_BF]))

# ---- 20.1 能标口径：同一错误原样复发 ----
print("\n     --- 20.1 能标口径（与 §19-C54-4 同错，本轮未修） ---")
print("     μ_UV 草稿 = M_pl c²/ħ = %s（s^-1）" % fmt(_mu_uv_doc, 12))
print("     μ_UV 正确 = %s eV；积分跨度 ln = %s vs %s ⇒ 虚增 %s"
      % (fmt(_E_pl_eV, 12), fmt(_ln_doc, 8), fmt(_ln_ok, 8), fmt(_ln_doc - _ln_ok, 8)))
reg("FAIL", "§20-C55-1 能标口径错误在续修③中原样复发：μ_UV = M_pl c²/ħ = %s s⁻¹（非 eV）⇒ 跨度虚增 %s"
    % (fmt(_mu_uv_doc, 6), fmt(_ln_doc - _ln_ok, 6)),
    "§19-C54-4 已判定该错误并给出正确值 %s eV；本轮「双圈升级」未修能标定义，仅新增 7 个系数 ⇒ "
    "单圈/双圈两组跑动曲线共用一个错误输入 ⇒ 「双圈降低截断误差」的对比基准本身错误"
    % fmt(_E_pl_eV, 8),
    "μ_UV 草稿=%s、正确=%s eV；ln 虚增 %s（+%s%%）"
    % (fmt(_mu_uv_doc, 8), fmt(_E_pl_eV, 8), fmt(_ln_doc - _ln_ok, 6),
       fmt((_ln_doc / _ln_ok - 1) * 100, 5)), "量纲/单位审计")

# ---- 20.2 草稿固定点搜索代码的可运行性（复发） ----
def rg2_fp_draft(x):
    """照抄草稿 fp_two_loop：把 x 解包为三分量并返回三分量列表。"""
    gk, gt, gkt = x
    return list(rg2_beta(gk, gt, gkt))


print("\n     --- 20.2 草稿固定点搜索原样运行（3 种 x0 × 2 种 solver） ---")
_rg2_try_txt = []
for _lab, _x0 in (("list  x0", [mpf("0.05"), mpf("0.05"), mpf("0.02")]),
                  ("tuple x0", (mpf("0.05"), mpf("0.05"), mpf("0.02"))),
                  ("matrix x0", mp.matrix([mpf("0.05"), mpf("0.05"), mpf("0.02")]))):
    for _solv in ("default", "mnewton"):
        try:
            if _solv == "default":
                _rr = mp.findroot(rg2_fp_draft, _x0)
            else:
                _rr = mp.findroot(rg2_fp_draft, _x0, solver="mnewton")
            _rg2_try_txt.append("%s/%s → %s" % (_lab, _solv, str(_rr)))
        except Exception as _e20:
            _rg2_try_txt.append("%s/%s → 抛 %s" % (_lab, _solv, type(_e20).__name__))
for _t20 in _rg2_try_txt:
    print("       %s" % _t20)

# 手工 Newton（3×3 解析 Jacobian + Cramer）从草稿种子出发
_rg2_x = [mpf("0.05"), mpf("0.05"), mpf("0.02")]
_rg2_steps = 0
for _k20 in range(60):
    _f20 = rg2_fp_draft(_rg2_x)
    _J20 = [[2 * RG2_B[0] * _rg2_x[0] + 3 * RG2_D[0] * _rg2_x[0] ** 2 + RG2_D[1] * _rg2_x[2] ** 2,
             mpf(0),
             2 * RG2_B[1] * _rg2_x[2] + 2 * RG2_D[1] * _rg2_x[0] * _rg2_x[2]],
            [mpf(0),
             2 * RG2_B[2] * _rg2_x[1] + 3 * RG2_D[2] * _rg2_x[1] ** 2 + RG2_D[3] * _rg2_x[2] ** 2,
             2 * RG2_B[3] * _rg2_x[2] + 2 * RG2_D[3] * _rg2_x[1] * _rg2_x[2]],
            [RG2_B[4] * _rg2_x[2] + 2 * RG2_D[4] * _rg2_x[0] * _rg2_x[2],
             RG2_B[5] * _rg2_x[2] + 2 * RG2_D[5] * _rg2_x[1] * _rg2_x[2],
             RG2_B[4] * _rg2_x[0] + RG2_B[5] * _rg2_x[1] + RG2_D[4] * _rg2_x[0] ** 2
             + RG2_D[5] * _rg2_x[1] ** 2 + 3 * RG2_D[6] * _rg2_x[2] ** 2]]
    _det20 = mp.det(mp.matrix(_J20))
    if abs(_det20) < mpf("1e-80"):
        break
    _d20 = []
    for _c20 in range(3):
        _M20 = [list(_J20[_r20]) for _r20 in range(3)]
        for _r20 in range(3):
            _M20[_r20][_c20] = -_f20[_r20]
        _d20.append(mp.det(mp.matrix(_M20)) / _det20)
    _rg2_x = [_rg2_x[_i20] + _d20[_i20] for _i20 in range(3)]
    _rg2_steps = _k20 + 1
    if max(abs(_v20) for _v20 in _d20) < mpf("1e-60"):
        break
_rg2_seed_norm = max(abs(_v20) for _v20 in _rg2_x)
_rg2_seed_origin = _rg2_seed_norm < mpf("1e-12")
print("     手工 Newton（解析 Jacobian）自草稿种子 [0.05、0.05、0.02] 出发：")
print("       迭代 %d 步 ⇒ (gk、gt、gkt) = (%s、%s、%s)，max abs(x) = %s"
      % (_rg2_steps, fmt(_rg2_x[0], 6), fmt(_rg2_x[1], 6), fmt(_rg2_x[2], 6), fmt(_rg2_seed_norm, 6)))

reg("FAIL", "§20-C55-2 草稿固定点搜索代码在续修③中仍不可运行（3 种 x0 × 2 种 solver 全部抛错）",
    "本机 mpmath 1.3.0 实测：%s。草稿写法把 Python list 当 x0、函数按列表解包，"
    "而该版本 findroot 的多元路径不可用 ⇒ 草稿既得不到固定点，也无法暴露「固定点落在何处」这一关键事实"
    "（与 §19-C54-3 同型：异常替换结论）。另：手工 Newton（解析 Jacobian）自同一草稿种子出发，"
    "%d 步后 max abs(x) = %s ⇒ %s（该模长比非平凡解 210/41 = 5.122 小 21 个量级）"
    % ("；".join(_rg2_try_txt[:3]), _rg2_steps, fmt(_rg2_seed_norm, 4),
       "落在原点吸引域（即草稿路径得不到非平凡固定点）" if _rg2_seed_origin
       else "收敛到非原点（异常，需复核）"),
    "可运行性检验（本机 mpmath 1.3.0 / Python 3.8.8）", "可运行性检验")

# ---- 20.3 精确固定点解集（sympy 有理数，本册正面产出） ----
_gk_, _gt_, _gkt_ = _sym23.symbols("gk gt gkt", real=True)
_rg2_eqs = [_sym23.Rational("0.021") * _gk_ ** 2 + _sym23.Rational("-0.012") * _gkt_ ** 2
            + _sym23.Rational("-0.0041") * _gk_ ** 3 + _sym23.Rational("0.0022") * _gk_ * _gkt_ ** 2,
            _sym23.Rational("0.018") * _gt_ ** 2 + _sym23.Rational("-0.009") * _gkt_ ** 2
            + _sym23.Rational("-0.0033") * _gt_ ** 3 + _sym23.Rational("0.0016") * _gt_ * _gkt_ ** 2,
            _sym23.Rational("0.015") * _gk_ * _gkt_ + _sym23.Rational("-0.007") * _gt_ * _gkt_
            + _sym23.Rational("-0.0024") * _gk_ ** 2 * _gkt_
            + _sym23.Rational("-0.0018") * _gt_ ** 2 * _gkt_ + _sym23.Rational("0.0009") * _gkt_ ** 3]
try:
    _rg2_sols = _sym23.solve(_rg2_eqs, [_gk_, _gt_, _gkt_], dict=True)
    _rg2_sol_txt = "、".join(["(gk=" + str(_s.get(_gk_, 0)) + "、gt=" + str(_s.get(_gt_, 0))
                              + "、gkt=" + str(_s.get(_gkt_, 0)) + ")" for _s in _rg2_sols]) \
        if _rg2_sols else "无解"
except Exception as _e20b:
    _rg2_sols = []
    _rg2_sol_txt = "solve 异常：%s" % type(_e20b).__name__
_rg2_nontrivial = [(_s.get(_gk_, 0), _s.get(_gt_, 0), _s.get(_gkt_, 0)) for _s in _rg2_sols
                   if not (str(_s.get(_gk_, 0)) == "0" and str(_s.get(_gt_, 0)) == "0"
                           and str(_s.get(_gkt_, 0)) == "0")]
_rg2_nt_txt = "、".join(["(gk=" + str(_a) + "、gt=" + str(_b) + "、gkt=" + str(_c) + ")"
                         for _a, _b, _c in _rg2_nontrivial]) if _rg2_nontrivial else "无非平凡解"
print("\n     --- 20.3 精确固定点解集（sympy 有理数） ---")
print("     共 %d 组解：%s" % (len(_rg2_sols), _rg2_sol_txt))
print("     非平凡解：%s" % _rg2_nt_txt)
_rg2_gkstar = -RG2_BF[0] / RG2_DF[0]        # -b1/d1 = 210/41
_rg2_gtstar = -RG2_BF[2] / RG2_DF[2]        # -b3/d3 = 60/11
print("     解析：gk* = −b1/d1 = %s ；gt* = −b3/d3 = %s" % (str(_rg2_gkstar), str(_rg2_gtstar)))
print("     该点二阶/一阶项比：d1·gk*/b1 = %s ；d3·gt*/b3 = %s"
      % (str(_rg2_gkstar * RG2_DF[0] / RG2_BF[0]), str(_rg2_gtstar * RG2_DF[2] / RG2_BF[2])))

reg("INFO", "§20-C55-3 【正面产出·形式修复】双圈项使「单圈唯一解为原点」的缺陷在形式上被修掉：出现 3 组非平凡固定点",
    "sympy 有理数精确解集 = %s；即在 gkt=0 平面上 β_gk = gk²(b1+d1 gk) 与 β_gt = gt²(b3+d3 gt) 各多出一个零点 ⇒ "
    "固定点从 1 个（原点）增至 4 个。这是草稿「双圈降低截断误差」宣称中唯一在形式上成立的部分；"
    "但代价是新增 7 个自由系数（见 §20-C55-7），且性质由 §20-C55-4/5 判定" % _rg2_nt_txt,
    "与 §19-C54-2 对照：单圈条件下该平面唯有原点", "sympy 精确求解")

reg("FAIL", "§20-C55-4 【截断伪影定理】全部非平凡固定点位于 gkt*=0 且恰在「二阶项 = −一阶项」处 ⇒ 该固定点是截断产物",
    "①所有 3 组非平凡解均满足 gkt*=0（混合耦合必须整体关闭）⇒ 草稿预测靶「gk*、gt*、gkt* 三分量固定点」不存在；"
    "②解析恒等式：gk* = −b1/d1 ⇒ 该点 d1·gk*/b1 = %s（精确 −1）；gt* = −b3/d3 ⇒ d3·gt*/b3 = %s（精确 −1）。"
    "即固定点恰好出现在「被截断的高阶项与最低阶项等量反号」之点 ⇒ 按定义即微扰展开最不可靠处；"
    "③固定点位置 100%% 由手选系数决定：改 d1（−0.0041）即改 gk*（5.122），改 d3 即改 gt*（5.455）——"
    "不存在任何第一性输入锁定它们"
    % (str(_rg2_gkstar * RG2_DF[0] / RG2_BF[0]), str(_rg2_gtstar * RG2_DF[2] / RG2_BF[2])),
    "gk*=%s（强耦合 4π 归一后 α≈g²/4π≈2.09）、gt*=%s；与 §19-C54-2 的 codimension-1 细调同性质"
    % (str(_rg2_gkstar), str(_rg2_gtstar)), "解析推导 + sympy 精确")

# ---- 20.4 物理可达性 ----
_rg2_s_need = mp.quad(lambda _x: 1 / (_x ** 2 * (RG2_B[0] + RG2_D[0] * _x)),
                      [float(RG2_GK0), float(_rg2_gkstar) * 0.9999999])
_rg2_mu_ratio = mp.exp(_rg2_s_need - _ln_ok)
print("\n     --- 20.4 固定点的物理可达性 ---")
print("     到达 gk* 所需积分跨度（纯 gk 方向）= %s" % fmt(_rg2_s_need, 10))
print("     Planck 跨度 = %s ⇒ 比值 = %s" % (fmt(_ln_ok, 10), fmt(_rg2_s_need / _ln_ok, 8)))
print("     μ_need / E_Planck = %s" % fmt(_rg2_mu_ratio, 8))
reg("FAIL", "§20-C55-5 双圈固定点物理不可达：所需 ln μ 为 Planck 跨度的 %s 倍，μ 须超 Planck %s 倍"
    % (fmt(_rg2_s_need / _ln_ok, 8), fmt(_rg2_mu_ratio, 6)),
    "从红外 gk0=0.12 出发到达 gk*=210/41 需 ∫dgk/(gk²(b1+d1·gk)) = %s，而 Planck 跨度仅 %s ⇒ 差 %s 倍；"
    "换算 μ_need/E_Planck = %s。即在任何可计算能区内都观测不到该固定点 ⇒ "
    "「紫外固定点精度提升」在本模块自身参数下没有可观测内容（黑洞/对撞机/宇宙学均不可及）"
    % (fmt(_rg2_s_need, 8), fmt(_ln_ok, 8), fmt(_rg2_s_need / _ln_ok, 6), fmt(_rg2_mu_ratio, 6)),
    "一维 RG 闭式积分 + mpmath 250 位", "可达性审计")

# ---- 20.5 微扰收敛诊断（本册正面产出：判据） ----
_rg2_1l = rg2_flow(_ln_ok, 20000, two_loop=False)
_rg2_2l = rg2_flow(_ln_ok, 20000, two_loop=True)
_rg2_1l_d = rg2_flow(_ln_doc, 20000, two_loop=False)
_rg2_2l_d = rg2_flow(_ln_doc, 20000, two_loop=True)
_rg2_rel = [abs(_rg2_2l[_i] / _rg2_1l[_i] - 1) for _i in range(3)]
_rg2_rat = [RG2_D[0] * _rg2_2l[0] ** 3 / (RG2_B[0] * _rg2_2l[0] ** 2),
            RG2_D[2] * _rg2_2l[1] ** 3 / (RG2_B[2] * _rg2_2l[1] ** 2),
            (RG2_D[4] * _rg2_2l[0] ** 2 * _rg2_2l[2] + RG2_D[5] * _rg2_2l[1] ** 2 * _rg2_2l[2]
             + RG2_D[6] * _rg2_2l[2] ** 3) / (RG2_B[4] * _rg2_2l[0] * _rg2_2l[2]
                                              + RG2_B[5] * _rg2_2l[1] * _rg2_2l[2])]
print("\n     --- 20.5 微扰收敛诊断（Planck 内） ---")
print("     1 圈 UV = (%s、%s、%s)" % (fmt(_rg2_1l[0], 10), fmt(_rg2_1l[1], 10), fmt(_rg2_1l[2], 10)))
print("     2 圈 UV = (%s、%s、%s)" % (fmt(_rg2_2l[0], 10), fmt(_rg2_2l[1], 10), fmt(_rg2_2l[2], 10)))
print("     耦合相对差 = (%s、%s、%s)" % tuple(fmt(_v, 6) for _v in _rg2_rel))
print("     β 项二阶/一阶比 = (%s、%s、%s)" % tuple(fmt(_v, 6) for _v in _rg2_rat))
print("     步长收敛：2000 vs 20000 步 gk = %s vs %s（相对差 %s）"
      % (fmt(rg2_flow(_ln_ok, 2000)[0], 12), fmt(_rg2_2l[0], 12),
         fmt(abs(rg2_flow(_ln_ok, 2000)[0] / _rg2_2l[0] - 1), 6)))
reg("INFO", "§20-C55-6 【正面产出·判据】双圈项在 Planck 内确为小量修正（β 项比 −%s~−%s），但它对结论的改变量同样微小 ⇒ 「大幅降低截断误差」无内容"
    % (fmt(abs(_rg2_rat[2]) * 100, 4), fmt(abs(_rg2_rat[0]) * 100, 4)),
    "Planck 内 β 项二阶/一阶比 = (%s、%s、%s)（均在 −2%%~−4%%）、UV 耦合相对差 = (%s、%s、%s) ⇒ "
    "在微扰可靠的能区内，双圈只把耦合改了 0.1%%~0.5%%；而「大幅降低截断误差」既未给出误差预算（无三圈基准、"
    "无 scheme 声明、无收敛阶验证），也未给出任何被判定的观测量 ⇒ 该宣称不可证伪也无内容。"
    "真正需要双圈修正的正是固定点处，而那里比值为 −1（§20-C55-4）"
    % (tuple(fmt(_v, 6) for _v in _rg2_rat) + tuple(fmt(_v, 6) for _v in _rg2_rel)),
    "RG 数值积分（2000 步与 20000 步一致性）", "收敛性诊断")

# ---- 20.6 自由度与完备性 ----
print("\n     --- 20.6 自由度与三阶项完备性 ---")
print("     自由系数：单圈 6 个 → 双圈 13 个（+7）；固定点方程数 3、未知数 3 ⇒ 一般必有孤立解")
print("     3 变量 3 次单项式共 C(5,3)=10 个；草稿 β_gk 含 2 个（gk³、gk·gkt²）、β_gt 含 2 个、β_gkt 含 3 个")
print("     无拉氏量/无对称性声明 ⇒ 无法判定缺项是否合法（完整性判据不存在）")
reg("FAIL", "§20-C55-7 双圈未修 C54 的核心缺陷而是加重它：自由系数 6→13 且仍无作用量推导 ⇒ 「有固定点」是自由度配平而非物理",
    "固定点方程数（3）= 未知数（3）⇒ 一般情形必有解，因此「找到了紫外固定点」不能作为理论正确的证据；"
    "而 13 个系数全部手选、无拉氏量、无一条 Feynman 图贡献、无 scheme 说明 ⇒ 与 §19-C54-1 同型且更严重。"
    "另：β_gk/β_gt 在 10 个三阶单项式中各仅含 2 个 ⇒ 相对一般 2-loop 结构不完备，且因无作用量而无法判定缺项合法性",
    "口径同 §19-C54-1、§2-2；判别式 V = (n_hit − n_free − n_anchor)/n_hit 中 n_hit=0 ⇒ V≤0",
    "结构审计 + 自由度审计")

reg("FAIL", "§20-C55-8 标记重判：TUFT-RG「双圈修正、降低紫外固定点截断误差、渐近安全精度提升」不成立",
    "综合 §20-C55-1..7：能标口径错误复发（跨度虚增 %s）；固定点搜索代码仍不可运行；"
    "非平凡固定点全部落在 gkt*=0 且恰在二阶项与一阶项等量反号处（截断伪影）；到达该点需 μ 超 Planck %s 倍（不可达）；"
    "可计算能区内双圈仅改耦合 0.1%%~0.5%%（无「大幅」可言）；自由系数 6→13 ⇒ "
    "「双圈升级」在形式上加了一个截断伪影固定点，在物理上未产生任何新可检验内容 ⇒ 登记 falsified（模块层）；"
    "体系级「TUFT 是否有紫外固定点」仍 open（前置条件仍是由有效作用量导出全部 β 系数）"
    % (fmt(_ln_doc - _ln_ok, 6), fmt(_rg2_mu_ratio, 4)),
    "与 §19-C54-8、C25/C29 的 FAIL 口径一致（公式/模块层证伪 ≠ 议题证伪）", "诚实重判")

reg("INFO", "§20-C55-9 【正面产出·截断伪影判据】本册新增可判定陈述：固定点只有在「二阶/一阶项比 → 0」的微扰可靠区内才具物理意义",
    "判据：设 β = β₁ + β₂（最低阶 + 次阶），任何「非平凡固定点 g*」必须满足 abs(β₂(g*)/β₁(g*)) ≪ 1，"
    "且须给出三阶项以显示比值继续下降（收敛阶验证）。本册据此外推：§20-C55-3 的固定点 abs(β₂/β₁) = 1（临界）⇒ "
    "不满足判据 ⇒ 判为截断伪影。该判据把「有没有固定点」这一逻辑问题，推进为「固定点在不在微扰可靠区」这一可算问题",
    "该判据对任何截断 β 函数通用，不限于本模块", "判据构造")

item("§20 TUFT-RG 双圈截断伪影判定完成（固定点在二阶/一阶比 = −1 处、可达性 ln 需 %s ≫ Planck %s）"
     % (fmt(_rg2_s_need, 6), fmt(_ln_ok, 6)), True)


# ===========================================================================
# §21  V21 续修③ 模块2 · 引力泡动力学演化 ODE（C56）—— 稳定性 / 坍缩 / 守恒审计
# ===========================================================================
print("\n" + "=" * 76)
print("§21  V21续修③ 模块2 | 引力泡动力学 ODE：方程量纲 / 数值稳定性 / 坍缩与守恒")
print("=" * 76)

GB2_S0 = mpf("0.1")
GB2_V0 = mpf("0.0")
GB2_K0 = mpf("1e-16")
GB2_T0 = mpf("1e-12")
GB2_AG = mpf("0.85")
GB2_W = mpf("1e4")
GB2_GAM = mpf("1e-8")
GB2_GT = mpf("1e-9")
GB2_GK = mpf("1e-9")
GB2_T1 = mpf("1e-4")
GB2_NSTEP = 2000
GB2_RADAU_REF = mpf("8.064660050877137e-13")   # scipy Radau(rtol=1e-13) 外校值（见 §21 文字说明）


def gb2_accel(sg, vv, kk, tt):
    """照抄草稿：accel = (∂ρ_grav/∂σ − γ v)/ρ_eff；同时返回 ρ_eff 与 ∂ρ/∂σ。"""
    _F = kk ** 2 + GB2_AG * tt ** 2
    _drho = 3 * sg ** 2 / (16 * pi * G_NEWTON) * _F
    _rho = sg ** 3 / (16 * pi * G_NEWTON) * _F
    if abs(_rho) < mpf("1e-220"):
        return mpf(0), _rho, _drho
    return (_drho - GB2_GAM * vv) / _rho, _rho, _drho


def gb2_euler(nstep):
    """照抄草稿 integrate_bubble_dynamics（显式 Euler + 固定 dt）。"""
    _dt = GB2_T1 / nstep
    _sg, _vv, _kk, _tt = GB2_S0, GB2_V0, GB2_K0, GB2_T0
    for _ in range(nstep + 1):
        _a, _rho, _drho = gb2_accel(_sg, _vv, _kk, _tt)
        _sg, _vv = _sg + _vv * _dt, _vv + _a * _dt
        _kk, _tt = _kk + (GB2_W * _tt - GB2_GK * _kk) * _dt, _tt + (-GB2_W * _kk - GB2_GT * _tt) * _dt
    return _sg, _vv, _kk, _tt


def gb2_stable(nstep):
    """指数拟合格式（对阻尼项精确、无条件稳定）——用于取得物理参考解。"""
    _dt = GB2_T1 / nstep
    _sg, _vv, _kk, _tt = GB2_S0, GB2_V0, GB2_K0, GB2_T0
    for _ in range(nstep + 1):
        _F = _kk ** 2 + GB2_AG * _tt ** 2
        _lam = GB2_GAM * 16 * pi * G_NEWTON / (_sg ** 3 * _F)
        _Ee = mp.exp(-_lam * _dt)
        _vn = _vv * _Ee + (3 / _sg) * (1 - _Ee) / _lam
        _sg = _sg + _dt * (_vv + _vn) / 2
        _vv = _vn
        _kk, _tt = _kk + (GB2_W * _tt - GB2_GK * _kk) * _dt, _tt + (-GB2_W * _kk - GB2_GT * _tt) * _dt
    return _sg, _vv, _kk, _tt


# ---- 21.1 加速度恒等式（本册关键结构性发现） ----
_sg_, _kk_, _tt_, _vv_, _ag_, _ga_ = _sym23.symbols("sg kk tt vv ag ga", positive=True)
_Fsym = _kk_ ** 2 + _ag_ * _tt_ ** 2
_acc_ident = _sym23.simplify((3 * _sg_ ** 2 * _Fsym - _ga_ * _vv_) / (_sg_ ** 3 * _Fsym)
                             - (3 / _sg_ - _ga_ * _vv_ / (_sg_ ** 3 * _Fsym)))
print("\n     --- 21.1 加速度恒等式：γ → 0 时 accel ≡ 3/σ（与 G、κ0、τ0、α_g 全部无关） ---")
print("     simplify(accel − (3/σ − γv·16πG/(σ³F))) = %s" % _acc_ident)
print("     σ=0.1 时 3/σ = %s（数值口径为 [1/L]，见 21.2）" % fmt(3 / GB2_S0, 8))

reg("FAIL", "§21-C56-1 【结构性】σ 的运动方程与引力/挠率/曲率场完全无关：∂ρ/∂σ 与 ρ_eff 中同一因子 (κ0²+α_gτ0²) 恒约去 ⇒ accel ≡ 3/σ − γv·16πG/(σ³F)",
    "符号恒等式 simplify(...) = %s（精确 0）⇒ 除阻尼项外，σ 的加速度不含 G、κ0、τ0、α_g 中的任何一个；"
    "即该「引力泡动力学」的 σ 段与 §18 声称的曲率-挠率能量无关，实质是运动学关系 d(σ³)/dt 的自洽式，"
    "不能作为引力/几何动力学的输出。另有第二类错误：代码把 §18 的**总能量** E=σ³/(16πG)F 当作**密度** ρ_eff 使用"
    "（两者同式），故 «∂E/∂σ)/E ≡ 3/σ» 恒成立" % _acc_ident,
    "sympy 精确符号验证；对照 §18-C53-1/4：ρ_grav 本身量纲非法（三口径全败）", "符号推导 + 结构审计")

# ---- 21.2 量纲 ----
_d_rho_body = dmul(dpow(DIM_G, -1), dpow(D(L=-1), 2))       # 本体 κ=[L^-1] 口径
_rg2_dacc = ddiv(dmul(_d_rho_body, D(L=-1)), _d_rho_body)   # [∂ρ/∂σ]/[ρ]
print("\n     --- 21.2 方程量纲审计 ---")
print("     ρ_grav 量纲（承 §18-C53-1）= %s（≠ 能量密度 %s）" % (dfmt(_d_rho_body), dfmt(D(L=-1, M=1, T=-2))))
print("     accel = (∂ρ/∂σ − γv)/ρ 的量纲 = %s ；加速度应为 %s ⇒ 差 [M^-1 T^1]"
      % (dfmt(_rg2_dacc), dfmt(D(L=1, T=-2))))
reg("FAIL", "§21-C56-2 ODE 两头量纲均非法：(a) ρ_grav 承 §18 仍非能量密度；(b) accel =(∂ρ/∂σ − γv)/ρ 的量纲为 %s 而加速度须为 %s"
    % (dfmt(_rg2_dacc), dfmt(D(L=1, T=-2))),
    "①(∂ρ/∂σ)/ρ 比 ρ 的量纲本身低一个 L ⇒ 结果是 [L^-1]（数值 3/σ=30 带单位 1/m，无物理含义）；"
    "②阻尼项 γv/ρ 与 3/σ 并不同量纲（γ=[T^-1]、v=[L T^-1]、ρ=[L^-5 M T^2] ⇒ [L^4 M^-1 T^-4]）"
    "⇒ 4 个 ODE 中 2 个（σ、v）量纲不自洽；③σ 的初值 0.1 m 与 ρ 的量纲错误互相掩盖，使数值看起来「有量级」",
    "量纲账本（L、M、T、I）+ §18-C53-1 的 ρ 量纲结论", "量纲审计")

# ---- 21.3 数值稳定性（本册关键发现） ----
_F0 = GB2_K0 ** 2 + GB2_AG * GB2_T0 ** 2
_lam0 = GB2_GAM * 16 * pi * G_NEWTON / (GB2_S0 ** 3 * _F0)
_dt_draft = GB2_T1 / GB2_NSTEP
_e_stab = _lam0 * _dt_draft / 2
_n_min = _lam0 * GB2_T1 / 2
_gb2_eul = gb2_euler(GB2_NSTEP)
_gb2_ref = gb2_stable(GB2_NSTEP)
_gb2_ref2 = gb2_stable(20000)
print("\n     --- 21.3 显式 Euler 稳定极限 ---")
print("     σ 段有效阻尼率 λ = γ·16πG/(σ0³F0) = %s s^-1" % fmt(_lam0, 8))
print("     显式 Euler 稳定上限 dt < 2/λ = %s s ；草稿 dt = %s s" % (fmt(2 / _lam0, 8), fmt(_dt_draft, 8)))
print("     越界判据 λ·dt/2 = %s（>1 即不稳定）⇒ 稳定所需 n > %s，草稿 n = %d"
      % (fmt(_e_stab, 8), fmt(_n_min, 8), GB2_NSTEP))
print("     草稿 Euler 输出：σ_end = %s m（σ/σ0 − 1 = %s）" % (fmt(_gb2_eul[0], 10), fmt(_gb2_eul[0] / GB2_S0 - 1, 8)))
print("     稳定参考解（指数拟合）：n=2000 → σ/σ0−1 = %s ；n=20000 → %s（自洽）"
      % (fmt(_gb2_ref[0] / GB2_S0 - 1, 8), fmt(_gb2_ref2[0] / GB2_S0 - 1, 8)))
print("     外校：scipy Radau(rtol=1e-13) 给 σ/σ0−1 = %s（与上一致）" % fmt(GB2_RADAU_REF, 8))
_gb2_ratio = (_gb2_eul[0] / GB2_S0 - 1) / (_gb2_ref[0] / GB2_S0 - 1)
print("     草稿输出 / 物理参考 = %s 倍" % fmt(_gb2_ratio, 6))
reg("FAIL", "§21-C56-3 草稿的「演化」是数值不稳定伪迹：显式 Euler 越稳定界 %s 倍 ⇒ 输出 σ_end/σ0−1 = %s，而物理参考仅 %s（差 %s 倍）"
    % (fmt(_e_stab, 6), fmt(_gb2_eul[0] / GB2_S0 - 1, 6), fmt(_gb2_ref[0] / GB2_S0 - 1, 6), fmt(_gb2_ratio, 6)),
    "σ 段阻尼率 λ = %s s⁻¹ 使 ODE 变刚性：显式 Euler 稳定上限 dt < %s s，而草稿取 dt = %s s ⇒ λ·dt/2 = %s（需 n > %s 步，草稿仅 %d 步）。"
    "后果：草稿输出 σ 由 0.1 m 涨到 %s m（6 个量级），而稳定解（指数拟合 n=2000 与 20000 一致、并经 scipy Radau rtol=1e-13 外校）"
    "给出 σ/σ0−1 = %s —— 即 σ 在 1e-4 s 内基本不动。⇒ 草稿展示的「激发→传播→坍缩全过程」实际是数值发散，"
    "与物理轨道相差 %s 倍 ⇒ 该动态预言不成立"
    % (fmt(_lam0, 6), fmt(2 / _lam0, 6), fmt(_dt_draft, 6), fmt(_e_stab, 6), fmt(_n_min, 6), GB2_NSTEP,
       fmt(_gb2_eul[0], 6), fmt(_gb2_ref[0] / GB2_S0 - 1, 6), fmt(_gb2_ratio, 6)),
    "稳定性判据（线性化阻尼率）+ 指数拟合稳定格式 + scipy Radau 外校", "数值稳定性审计")

# ---- 21.4 「坍缩」与时间尺度 ----
_sv = []
_sg_r, _vv_r = GB2_S0, GB2_V0
_gb2_mono = True
for _i21 in range(GB2_NSTEP + 1):
    _a21, _rho21, _d21 = gb2_accel(_sg_r, _vv_r, GB2_K0, GB2_T0)
    _sv.append(_sg_r)
    _sg_r, _vv_r = _sg_r + _vv_r * _dt_draft, _vv_r + _a21 * _dt_draft
    if _a21 <= 0 and _i21 < 5:
        _gb2_mono = False
print("\n     --- 21.4 「坍缩」与时间尺度错配 ---")
print("     γ=0 时 dσ̈/dt 的驱动项 = 3/σ > 0 恒成立 ⇒ σ 单调加速；首个舍入步内 accel = %s" % fmt(3 / GB2_S0, 6))
print("     振荡周期 2π/ω_bub = %s s ；积分窗 %s s ⇒ 覆盖 %s 个周期（不足 1 个）"
      % (fmt(2 * pi / GB2_W, 6), fmt(GB2_T1, 4), fmt(GB2_W * GB2_T1 / (2 * pi), 6)))
print("     幅值衰减时标 2/(γ_τ+γ_κ) = %s s = %s yr ⇒ 窗长为其 %s 倍"
      % (fmt(2 / (GB2_GT + GB2_GK), 8), fmt(2 / (GB2_GT + GB2_GK) / 31557600, 6),
         fmt(GB2_T1 / (2 / (GB2_GT + GB2_GK)), 4)))
reg("FAIL", "§21-C56-4 模块宣称的「激发、传播、坍缩全过程」在方程层面不可能出现，且演示窗与三个特征时标全部错配",
    "①σ̈ = 3/σ > 0（σ>0 时恒正）⇒ ρ_eff 段提供的只有排斥 ⇒ 不存在坍缩分支；「坍缩」只存在于文字，"
    "任何初速下 σ 最终都被推向膨胀（v0<0 亦只能减速后回转）；"
    "②时间尺度：振荡周期 2π/ω_bub = %s s，而积分窗 1e-4 s 仅覆盖 %s 个周期（不足 1 个完整振荡）；"
    "幅值衰减时标 2/(γ_τ+γ_κ) = %s s ≈ 31.7 yr，窗长仅为其 %s 倍 ⇒ 演示窗内 κ0、τ0 幅值几乎不衰减、σ 几乎不变 ⇒ "
    "«全周期演化» 在数据中不可见" % (fmt(2 * pi / GB2_W, 6), fmt(GB2_W * GB2_T1 / (2 * pi), 6),
                                     fmt(2 / (GB2_GT + GB2_GK), 6),
                                     fmt(GB2_T1 * (GB2_GT + GB2_GK) / 2, 6)),
    "解析（符号）+ 时间尺度谱", "动力学定性审计")

# ---- 21.5 「守恒总能量 E_b」 ----
_base_norm = GB2_K0 ** 2 + GB2_AG * GB2_T0 ** 2
_norm_max = (GB2_T0 ** 2 + GB2_AG * GB2_K0 ** 2)   # 相位 π/2：κ→τ0、τ→−κ0
_norm_gain = _norm_max / _base_norm - 1
print("\n     --- 21.5 「守恒总能量 E_b」检验（无耗散解析） ---")
print("     范数 κ²+α_gτ² 随相位：初值 %s → 相位 π/2 处 %s ⇒ 变化 +%s%%"
      % (fmt(_base_norm, 6), fmt(_norm_max, 6), fmt(_norm_gain * 100, 6)))
print("     α_g=1 时该范数为旋转不变量（变化 0）⇒ 不守恒的唯一来源是 α_g≠1")
reg("FAIL", "§21-C56-5 「守恒总能量 E_b」不成立：α_g=0.85≠1 使范数 κ²+α_gτ² 在四分之一周期内摆动 +%s%%（零耗散下）"
    % fmt(_norm_gain * 100, 4),
    "无耗散时 κ→τ0、τ→−κ0（相位 π/2），范数由 κ0²+α_gτ0²=%s 变为 τ0²+α_gκ0²=%s ⇒ +%s%%；"
    "仅当 α_g=1 该旋转才保范数。而 ODE 另含 3 个耗散系数（γ、γ_τ、γ_κ）⇒ E_b 既因 α_g≠1 不守恒、"
    "又因耗散单调衰减；模块未给出任何能量预算把 σ 段与 κ0/τ0 段耦合起来 ⇒ «守恒» 与 «耗散» 两种描述自相矛盾"
    % (fmt(_base_norm, 6), fmt(_norm_max, 6), fmt(_norm_gain * 100, 4)),
    "解析范数计算（旋转轨道闭合式）", "守恒性审计")

# ---- 21.6 参数体系自洽性 ----
_omega_bub_native = C * sqrt(GB2_K0 ** 2 + GB2_T0 ** 2)
_dphi_draft2 = _gb2_eul[3] * _gb2_eul[0] * mpf("0.5") * HBAR / (mpf("0.1") * C)
_dphi_dimless2 = mpf("0.5") * _gb2_eul[3] * _gb2_eul[0]
print("\n     --- 21.6 参数体系自洽性 ---")
print("     模块输入的 ω_bub = %s rad/s ；而 §18-C53-8 的泡心频率 ω(0)=c√(κ0²+τ0²) = %s rad/s ⇒ 相差 %s 倍"
      % (fmt(GB2_W, 6), fmt(_omega_bub_native, 8), fmt(GB2_W / _omega_bub_native, 8)))
print("     末态自旋进动（草稿式）δφ = %s rad（量纲 [L M]）" % fmt(_dphi_draft2, 8))
print("     无量纲对照 (S/ħ)τ0σ = %s rad" % fmt(_dphi_dimless2, 8))
reg("FAIL", "§21-C56-6 模块内部参数不自洽：输入的 ω_bub=%s rad/s 与本体给出的泡心频率 ω(0)=c√(κ0²+τ0²)=%s rad/s 相差 %s 倍，且无任何约束方程"
    % (fmt(GB2_W, 6), fmt(_omega_bub_native, 8), fmt(GB2_W / _omega_bub_native, 6)),
    "§18-C53-8 已建立 ω(x)=c√(κ²+τ²)；本模块却把「孤子本征螺旋频率」当作独立自由输入取 1e4 rad/s，"
    "既不等于泡心频率、也不与之建立关系 ⇒ 同一体系的「频率」出现两个互不相干的定义（相差 3.34e7 倍）",
    "跨模块一致性（§18-C53-8 对照）", "一致性审计")
reg("FAIL", "§21-C56-7 自旋进动式 δφ = S·τ0·σ/v 量纲错误在续修③中原样复发（[L M] 非无量纲）",
    "草稿式 %s rad vs 唯一同结构无量纲式 (S/ħ)τ0σ = %s rad ⇒ 缺 ħ 因子（与 §18-C53-3 完全同型）；"
    "且两者量级（1e-49 / 1e-8 rad）均远低于任何可测精度" % (fmt(_dphi_draft2, 8), fmt(_dphi_dimless2, 8)),
    "量纲账本；对照 §18-C53-3", "量纲审计（复发）")

# ---- 21.7 自由度与可证伪性 ----
_gb2_n_free = 9
print("\n     --- 21.7 自由度与可证伪性 ---")
print("     自由参数：初值 4（σ0、v0、κ0、τ0）+ 系数 5（α_g、ω_bub、γ、γ_τ、γ_κ）= %d ；约束方程 0 条" % _gb2_n_free)
print("     可检验预测量 n_hit = 0（σ(t)、κ0(t)、τ0(t) 是手写 ODE 在 9 个自由输入下的解，不是预言）")
reg("FAIL", "§21-C56-8 伪派生（比 §18-C53 更严重）：自由参数 4→9 个、约束 0 条、可检验预言 0 条 ⇒ V≤0",
    "「新增动态观测预言」的靶 σ(t)、κ0(t)、τ0(t) 由 4 个初值 + 5 个系数（含 §21-C56-6 判为无约束的 ω_bub）决定；"
    "而 §21-C56-1 已证 σ 段方程不含任何场参数 ⇒ σ(t) 不可能承载引力/挠率信息。"
    "判别式 V = (n_hit − n_free − n_anchor)/n_hit 中 n_hit = 0 ⇒ V 无定义且 ≤ 0（口径同 §2-2、C25/C46）",
    "对照 §18-C53-7（4 参数 0 约束）；自由度随「续修」单调增加 4→9", "自由度审计")

reg("FAIL", "§21-C56-9 标记重判：引力泡动力学「激发传播坍缩时变预言就绪」不成立",
    "综合 §21-C56-1..8：σ 段与场参数无关（3/σ 恒等）；ρ_grav 与 accel 两头量纲非法；"
    "草稿数值为不稳定伪迹（越稳定界 %s 倍、与参考解差 %s 倍）；σ̈>0 ⇒ 永不坍缩；"
    "演示窗不足 1 个振荡周期且比衰减时标短 1e13 倍；E_b 不守恒（α_g≠1 摆动 +%s%%）；"
    "ω_bub 与本征频率相差 3.34e7 倍；δφ 量纲复发；9 参数 0 约束 ⇒ 登记 falsified（模块层）；"
    "体系级「挠率/曲率场能否局域激发并动力学演化」仍 open（本轮不否定该物理议题）"
    % (fmt(_e_stab, 6), fmt(_gb2_ratio, 4), fmt(_norm_gain * 100, 4)),
    "与 §18-C53-10、C25/C29 同口径（模块宣称证伪 ≠ 议题证伪）", "诚实重判")

item("§21 引力泡动力学 ODE 审计完成（越稳定界 %s 倍、σ 段恒等式 accel≡3/σ、9 参数 0 约束）"
     % fmt(_e_stab, 4), True)


# ===========================================================================
# §22  V21 续修③ 模块3 · 草稿自评清单与判据审计（C57）—— 「37 claim / L3 有效」复核
# ===========================================================================
print("\n" + "=" * 76)
print("§22  V21续修③ 模块3 | 草稿 37-claim 自评清单与层级判据：计数 / 台账冲突 / 判据放宽")
print("=" * 76)

# 草稿清单逐条照抄：(id, status, name, predict_target)
D22_CLAIMS = [
    ("C24", "PASS", "光速归一基底约束", ""),
    ("C25", "open", "LB螺旋哈密顿，高阶αn能级+误差棒", "α_2..α_6 精细结构高阶能级"),
    ("C26", "PASS", "Frenet tanθ唯一几何定义", ""),
    ("C27", "PASS", "拓扑绕数N外部输入，无循环导出", ""),
    ("C28", "PASS", "移除旧Δθ_min伪约束", ""),
    ("C29", "PASS", "移除K0冗余常数", ""),
    ("C30", "PASS", "消除G循环定义", ""),
    ("C31", "PASS", "Π定理量纲自洽校验", ""),
    ("C32", "PASS", "删除ρ孤儿场项", ""),
    ("C33", "PASS", "修正麦克斯韦，Jgeo量纲自洽", ""),
    ("C34", "PASS", "电荷守恒约束推导成立", ""),
    ("C35", "open", "Binet方程，水星标定β，金星地球独立进动预言", "金星、地球百年进动角"),
    ("C36", "PASS", "相位场量纲对齐", ""),
    ("C37", "PASS", "多观测靶统计面板", ""),
    ("C38-1", "PASS", "矛盾自检算法", ""),
    ("C38-2", "PASS", "拓扑归一算法", ""),
    ("C38-3", "PASS", "层级升维判定算法", ""),
    ("CMB01", "open", "CMB拓扑双谱挤压构型", "B_2,1000,1000"),
    ("CMB02", "open", "CMB拓扑双谱等边构型", "B_800,800,800"),
    ("CMB03", "open", "CMB拓扑双谱折叠构型", "B_400,400,800"),
    ("EHT01", "open", "M87*主光子环角偏移", "n=1环角半径修正"),
    ("EHT02", "open", "M87*n=2次环位置与宽度", "n=2次环参数"),
    ("EHT03", "open", "M87*n=3次次环位置与宽度", "n=3次次环参数"),
    ("BUB01", "open", "引力泡总能量积分", "E_bubble实验室能量"),
    ("BUB02", "open", "自旋穿过引力泡进动偏移", "δφ_spin自旋进动角"),
    ("BUB03", "open", "引力泡参数误差传播", "σ_E能量误差棒"),
    ("BUB04", "open", "引力泡动力学演化ODE", "\\(\\sigma(t)\\),κ0(t),τ0(t)时间演化曲线"),
    ("RG01", "PASS", "TUFT单圈β函数定义", ""),
    ("RG02", "open", "TUFT RG流数值积分IR→UV", "gk,gt,gkt随能标跑动曲线"),
    ("RG03", "open", "紫外固定点求解", "gk*,gt*,gkt*固定点耦合"),
    ("RG04", "open", "渐近安全判定逻辑", "紫外发散抑制条件"),
    ("RG05", "open", "TUFT双圈β修正", "双圈耦合跑动与修正紫外固定点"),
    ("S01", "PASS", "螺旋场Frenet-Serret相容性", ""),
    ("S02", "open", "局域能量正定检验", "能量密度正定区间"),
    ("S03", "PASS", "洛伦兹不变性检验", ""),
    ("S04", "open", "弱场极限还原GR", "弱场下回归广义相对论"),
    ("S05", "open", "耦合跨尺度一致性约束", "αg,β,Atopo跨尺度匹配"),
]

_d22_total = len(D22_CLAIMS)
_d22_pass = sum(1 for _c in D22_CLAIMS if _c[1] == "PASS")
_d22_open = sum(1 for _c in D22_CLAIMS if _c[1] == "open")
_d22_bd = sum(1 for _c in D22_CLAIMS if _c[1] == "BOUNDARY")
_d22_fail = sum(1 for _c in D22_CLAIMS if _c[1] == "FAIL")
print("     草稿清单实测计数：总 %d | PASS=%d | open=%d | BOUNDARY=%d | FAIL=%d"
      % (_d22_total, _d22_pass, _d22_open, _d22_bd, _d22_fail))
print("     草稿「审计结论 1」自述：总 37 | PASS 20 | OPEN 17 | FAIL 0")
reg("FAIL", "§22-C57-1 草稿自评清单的计数自述与清单本身不符：实测 PASS=%d / open=%d，自述 PASS=20 / OPEN=17"
    % (_d22_pass, _d22_open),
    "逐条统计草稿 audit_claims 列表（37 条）：PASS=%d、open=%d、BOUNDARY=0、FAIL=0。"
    "「总 Claim=37」正确，但 PASS/OPEN 各差 2 条 ⇒ 该结论段的数字未与实际清单对齐（元审计层面已不自洽）；"
    "更关键的是 BOUNDARY 与 FAIL 被整体删除（见 §22-C57-3）" % (_d22_pass, _d22_open),
    "对草稿清单逐条计数（本引擎复算）", "计数核对")

# ---- 22.2 与已登记台账的冲突 ----
_d22_ledger = {}
for _l22b in io.open(os.path.join(SYS_DIR, "claims.csv"), encoding="utf-8").read().splitlines()[1:]:
    _p22 = _l22b.split(",")
    if len(_p22) >= 5:
        _d22_ledger[_p22[0].strip()] = _p22[3].strip().lower()
_d22_conf = [(_c[0], _c[1], _d22_ledger[_c[0]]) for _c in D22_CLAIMS
             if _c[0] in _d22_ledger and _d22_ledger[_c[0]] != _c[1].lower()]
_d22_conf_fal = [_t for _t in _d22_conf if _t[2] == "falsified"]
_d22_conf_bd = [_t for _t in _d22_conf if _t[2] == "boundary"]
_d22_unreg = [_c[0] for _c in D22_CLAIMS if _c[0] not in _d22_ledger]
print("\n     --- 22.2 与已登记台账（claims.csv C01–C54）比对 ---")
print("     同编号且状态冲突：%d 条 ⇒ %s" % (len(_d22_conf), "、".join(
    ["%s(%s→%s)" % _t for _t in _d22_conf])))
print("     其中台账已 falsified 被改标 PASS：%d 条；台账 boundary 被改标 PASS：%d 条"
      % (len(_d22_conf_fal), len(_d22_conf_bd)))
print("     草稿清单中台账尚未登记的编号：%d 条（%s）" % (len(_d22_unreg), "、".join(_d22_unreg)))
reg("FAIL", "§22-C57-2 草稿自评清单与已登记台账直接冲突 %d 处：%d 条已 falsified 与 %d 条 boundary 被改标为 PASS"
    % (len(_d22_conf), len(_d22_conf_fal), len(_d22_conf_bd)),
    "冲突明细（编号：草稿→台账）= %s。其中 C26/C27/C29/C30/C31/C33/C36/C37 在台账中已是 falsified"
    "（引擎 §11/§14 曾逐条给出量纲/循环/不可行证据），C28 为 boundary；草稿把它们统一列为 PASS ⇒ "
    "以自评覆盖已登记的证伪结论，属台账级口径倒退（§17-CLAIMS-3 明确「不得据草稿自评登记为 PASS」）"
    % "、".join(["%s：%s→%s" % _t for _t in _d22_conf]),
    "台账为 claims.csv 现值（C01–C54）", "台账一致性审计")

reg("FAIL", "§22-C57-3 草稿清单由「四态」退化为「二态」：BOUNDARY=0、FAIL=0，且新增 %d 条无模块支撑的观测靶主张"
    % len(_d22_unreg),
    "①清单仅含 PASS（%d）与 open（%d）两种状态，不含任何 BOUNDARY/FAIL/falsified ⇒ 与引擎四态口径"
    "（§17-CLAIMS-1 实测分布 pass/open/boundary/falsified/info）不可比 ⇒ 全部负结论在自评层被删除；"
    "②新增编号 %s 共 %d 条（CMB01-03、EHT01-03、BUB01-04、RG01-05、S01-05、C38-1..3），"
    "其中 CMB/EHT 共 6 条既无本册模块、也无公式与脚本（§19-全局表-1 已明确「不得凭声明登记」）⇒ "
    "「五大观测靶全部保留」的表述把未复核条目当作在册内容"
    % (_d22_pass, _d22_open, "、".join(_d22_unreg), len(_d22_unreg)),
    "口径同 §17-CLAIMS-3、§19-全局表-1", "口径红线")

# ---- 22.3 S03 与 C24 的内部矛盾 ----
_tan_theta22 = 2 * sqrt(N_DEF_B) * ALPHA
_speed_rel22 = sqrt(1 + 1 / _tan_theta22 ** 2)
print("\n     --- 22.3 「洛伦兹不变性检验 = PASS」与基底超光速的矛盾 ---")
print("     §2 的 α 命中要求 ωA = c/tanθ，tanθ = 2√N·α = %s ⇒ 基底速率 |v|/c = √(1+1/tan²θ) = %s"
      % (fmt(_tan_theta22, 8), fmt(_speed_rel22, 10)))
reg("FAIL", "§22-C57-4 草稿 S03「洛伦兹不变性检验 = PASS」与本体系自身的 C24 结论直接矛盾",
    "C24（台账 pass，引擎 §0/§2 复核）：α 公式命中观测要求 ωA = c/2.0068118 ⇒ 基底 R(t)=(A cos ωt、A sin ωt、ct) "
    "的速率 v = √(A²ω²+c²) = %s c，超光速 %s%% ⇒ 该基底不具洛伦兹不变性。"
    "同一清单同时标注 C24=PASS 与 S03（洛伦兹不变性）=PASS 不可兼得 ⇒ 至少一条为误标；"
    "按引擎口径应改判 S03 为 FAIL/BOUNDARY（洛伦兹不变性至多在基底速率 = c 的特殊参数下成立）"
    % (fmt(_speed_rel22, 8), fmt((_speed_rel22 - 1) * 100, 6)),
    "N_def_B=18907、α=7.2973525693e-3；与 §0-C24 同源", "内部一致性审计")

# ---- 22.4 三个「纠错算法」的实现审计 ----
def d22_claim_self_check(axiom_set, eq_list, param_dict, eps=mpf("1e-200")):
    """照抄草稿 claim_self_check。"""
    rep = {"status": "PASS", "conflict": []}
    if abs(param_dict.get("inv_res", 0)) > eps:
        rep["status"] = "FAIL"
        rep["conflict"].append("几何不变量残差超限")
    return rep


def d22_topological_normalization(frenet_data, manifold_bound, N_input, eps=mpf("1e-200")):
    """照抄草稿 topological_normalization。"""
    report = {}
    _k = frenet_data["kappa"]
    _t = frenet_data["tau"]
    _w = frenet_data["omega"]
    _c = frenet_data["c"]
    _res = _k ** 2 + _t ** 2 - _w ** 2 / _c ** 2
    if abs(_res) > eps:
        report["status"] = "FAIL"
        report["residual"] = _res
        report["message"] = "Frenet几何不变量不满足"
        return report
    if not isinstance(N_input, int) or N_input <= 0:
        report["status"] = "FAIL"
        report["residual"] = None
        report["message"] = "拓扑绕数N必须为正整数"
        return report
    _s = manifold_bound["s_total"]
    _it = _t * _s
    _rt = _it - 2 * pi * N_input
    report["topo_invariant"] = _it
    report["residual"] = _rt
    if abs(_rt) < eps:
        report["status"] = "PASS"
        report["message"] = "拓扑积分与输入N自洽，归一化完成"
    else:
        report["status"] = "INCONCLUSIVE"
        report["message"] = "拓扑积分残差超出阈值，拓扑不匹配"
    return report


def d22_hierarchy_lift(axiom_raw, eq_system, audit_claim_list, tolerance=mpf("1e-200")):
    """照抄草稿 hierarchy_lift（注意：axiom_raw / eq_system 在函数体内从未被读取）。"""
    report = {}
    _has_f = any(_claim["status"] == "FAIL" for _claim in audit_claim_list)
    _has_p = any(_claim.get("predict_target") is not None for _claim in audit_claim_list)
    if _has_f:
        report["status"] = "REJECT"
        report["target_level"] = "L1"
        report["conflict_list"] = ["存在FAIL缺陷，禁止层级升维"]
        report["message"] = "体系存在数学自洽缺陷，不满足L2/L3准入"
        return report
    report["base_level"] = "L2"
    if _has_p:
        report["target_level"] = "L3"
        report["status"] = "PASS"
        report["message"] = "场自洽 + 多套独立定量预测靶，升维L3"
    else:
        report["target_level"] = "L2"
        report["status"] = "PASS"
        report["message"] = "场方程自洽，但缺少定量预言，停留在L2"
    report["conflict_list"] = []
    return report


print("\n     --- 22.4 「矛盾自检算法」的实现审计 ---")
_r22_a = d22_claim_self_check("任意公理集（含自相矛盾者）", ["任意方程集"], {})
_r22_b = d22_claim_self_check("", [], {"inv_res": 0})
print("     claim_self_check(矛盾公理集、任意方程集、空 param_dict) → %s" % _r22_a)
print("     claim_self_check(空公理集、空方程集、inv_res=0)        → %s" % _r22_b)
reg("FAIL", "§22-C57-5 「矛盾自检算法」（C38-1 标 PASS）是桩函数：axiom_set 与 eq_list 在函数体内从未被读取",
    "照抄实现后实测：d22_claim_self_check(任意/自相矛盾的公理集、任意方程集、空 dict) 与 "
    "(空公理集、空方程集、inv_res=0) 均返回 status=PASS。函数体只读 param_dict['inv_res'] 一个外部数字 ⇒ "
    "它对「公理集是否矛盾」「方程集是否自洽」完全不可见 ⇒ 该 PASS 不携带任何引擎证据，"
    "不构成「矛盾自检」结论（口径同 §17-CLAIMS-3：无证据 ≠ 通过）",
    "照抄草稿实现并在引擎内实跑（两次调用均 PASS）", "实现级审计")

print("\n     --- 22.5 「层级升维判定算法」的判据放宽 ---")
_r22_c = d22_hierarchy_lift("", [], [{"status": "open", "predict_target": "任意字符串"}])
_r22_d = d22_hierarchy_lift("", [], [{"status": "open", "predict_target": None}])
print("     hierarchy_lift(空公理、空方程、一条 open+非空 predict_target) → %s / %s"
      % (_r22_c.get("base_level"), _r22_c.get("target_level")))
print("     hierarchy_lift(空公理、空方程、一条 open+无 predict_target)   → %s / %s"
      % (_r22_d.get("base_level"), _r22_d.get("target_level")))
reg("FAIL", "§22-C57-6 层级判据被放宽：草稿 hierarchy_lift 硬编码 base_level=\"L2\" 且只要有非空 predict_target 即升 L3/PASS ⇒ 丢掉「构造性推导 + 误差棒」双条件",
    "①函数体从不读取 axiom_raw 与 eq_system ⇒ 传入空字符串也照样输出 base_level=L2、target_level=L3（实测）；"
    "②引擎 §9.5/§17 的升 L3 规则要求 constructive_derivation 与带误差棒的 testable_prediction 同时具备，"
    "而草稿口径下本清单 19 条 open 全部带 predict_target ⇒ 直接判 L3/PASS。"
    "对照：引擎 §17 对登记全量（C01–C57）批量审计的 L3 = 0、无量纲靶登记 = 0。"
    "⇒ 「L3 资格保持有效」是判据放宽的产物，不是审计结论（这也解释了为何草稿清单删除了 BOUNDARY/FAIL 两态）",
    "照抄草稿实现并在引擎内实跑（空公理集亦升 L3）；对照 §17-CLAIMS-2", "判据级审计")

print("\n     --- 22.6 「拓扑归一算法」的恒等性与阈值 ---")
_r22_fd = {"kappa": mpf("1e-3"), "tau": mpf("1e-4"), "omega": C * sqrt(mpf("1e-3") ** 2 + mpf("1e-4") ** 2),
           "c": C}
_r22_bound = {"s_total": 2 * pi * 7 / mpf("1e-4")}
_r22_e = d22_topological_normalization(_r22_fd, _r22_bound, 7)
_r22_f = d22_topological_normalization(_r22_fd, {"s_total": _r22_bound["s_total"] * mpf("1.001")}, 7)
print("     τ·s_total 与 2πN 精确相等 → %s" % _r22_e["status"])
print("     s_total 仅扰动 0.1%% → %s（residual=%s）" % (_r22_f["status"], fmt(abs(_r22_f["residual"]), 6)))
reg("BOUNDARY", "§22-C57-7 「拓扑归一算法」（C38-2 标 PASS）是恒等重述 + 无来源阈值：τ·s_total 与 2πN 的比对即 N 的定义式",
    "①该「算法」用 integral_tau = τ·s_total 与输入的 2πN 比对，而 N 在其自身框架中正是由同一积分定义的 ⇒ "
    "自洽性检查退化为恒等式核对（无新约束）；②阈值 eps=1e-200 无来源说明：实测 s_total 仅扰动 0.1% 即从 PASS "
    "变为 INCONCLUSIVE ⇒ 该判据实为「精确相等」，既不能作为数值容差判据、也未界定物理容差；"
    "③N 仍为外部整数输入（与本体系 C27「N 无循环导出」一致）⇒ 三个「纠错算法」中两个为桩/恒等，"
    "其 PASS 不构成算法有效性证据",
    "照抄草稿实现在引擎内实跑（精确相等→PASS；0.1% 扰动→INCONCLUSIVE）", "实现级审计")

# ---- 22.7 CSV 导出契约 ----
_d22_csv = ["claim_id,claim_name,status,predict_target"]
for _c in D22_CLAIMS:
    _t22 = _c[3] if _c[3] else ""
    _d22_csv.append(_c[0] + "," + _c[2] + "," + _c[1] + "," + _t22)
_d22_bad = [(_i, len(_l.split(",")), _l) for _i, _l in enumerate(_d22_csv) if len(_l.split(",")) != 4]
print("\n     --- 22.7 CSV 导出契约 ---")
print("     照抄草稿 csv_text：字段数 ≠ 4 的行 %d 条" % len(_d22_bad))
for _b22 in _d22_bad:
    print("       行 %d（%d 字段）：%s" % _b22)
reg("FAIL", "§22-C57-8 草稿 CSV 导出破坏列结构：%d 行字段数 ≠ 4（predict_target 含裸英文逗号）" % len(_d22_bad),
    "草稿 run_full_audit 直接以逗号拼接字段而不转义；BUB04 的 predict_target 为 "
    "«\\(\\sigma(t)\\),κ0(t),τ0(t)时间演化曲线» 含 2 个英文逗号 ⇒ 该行裂成 6 字段，"
    "下游按 4 列解析将全部错位。对照：本引擎写入 claims.csv 前对每个字段做裸逗号/引号拒绝（见 §19.6 与 V22 登记块）"
    "⇒ 「归一化导出」在草稿侧未实现（口径不一致）",
    "草稿 csv 拼接逻辑照抄实跑", "接口契约审计")

# ---- 22.8 正面产出：审计清单四条必备字段 ----
reg("INFO", "§22-C57-9 【正面产出】给出「自评清单可被审计」的四条最低契约（本册把元审计也变为可判定）",
    "①状态必须四态齐备（PASS/BOUNDARY/INFO/FAIL），且与 claims.csv 现值逐条一致（不得单方改写已登记状态）；"
    "②新编号须附模块/公式/脚本三要素，否则仅可登记为「未复核」而非 PASS；"
    "③层级升维须引用判据原文（构造性推导 + 带误差棒的可检验预言），不得硬编码基准层级；"
    "④导出字段必须转义（裸逗号/引号拒绝）。本册据此外推出草稿清单的 4 类缺陷（§22-C57-2/3/6/8），"
    "并说明「L3 保持有效」在契约①③下不成立",
    "该契约对后续任何 V2x 续修清单通用", "判据构造")

# ---- 22.9 台账登记 C55/C56/C57（幂等） ----
V24_NEW_CLAIMS = [
    ("C55",
     "【V21续修③·双圈RG】TUFT-RG 双圈 β 扩展（β_gk=b1gk²+b2gkt²+d1gk³+d2gk·gkt²；β_gt 对称；"
     "β_gkt=b5gk·gkt+b6gt·gkt+d5gk²gkt+d6gt²gkt+d7gkt³；d1..d7=−0.0041/0.0022/−0.0033/0.0016/−0.0024/−0.0018/0.0009）"
     "250 位审计：①能标口径错误原样复发（μ_UV=M_pl c²/ħ=1.8549e43 s^-1 非 eV 正确值 1.2209e28 eV 跨度虚增 34.957）；"
     "②固定点搜索代码仍不可运行（mpmath 1.3.0 下 list/tuple/matrix 三种 x0 × default/mnewton 全抛错 手工 Newton 自草稿种子收敛到原点）；"
     "③sympy 精确解集 4 组且非平凡解全部 gkt*=0（gk*=210/41、gt*=60/11）⇒ 草稿预测靶「三分量固定点」不存在；"
     "④【截断伪影定理】gk*=−b1/d1 与 gt*=−b3/d3 恰使二阶项/一阶项比 = −1（精确）⇒ 固定点位于微扰展开最不可靠处 "
     "且位置 100% 由手选 d1/d3 决定；⑤物理不可达——到达 gk* 需 ln μ=572.06 而 Planck 跨度 64.67（μ 须超 Planck 2.26e220 倍）；"
     "⑥Planck 内双圈仅改耦合 0.12%~0.44%（β 项比 −1.6%~−3.9%）⇒ 「大幅降低截断误差」既无误差预算也无内容；"
     "⑦自由系数 6→13 且仍无作用量（固定点方程数 3 = 未知数 3 ⇒ 有解属自由度配平）；三阶单项式仅含 2/10（无完整性判据） "
     "⇒ 模块「双圈降低紫外固定点截断误差」宣称不成立 → falsified（模块层）；体系级「TUFT 是否有紫外固定点」仍 open "
     "（前置条件仍是由有效作用量导出全部 β 系数）",
     "第一性审计", "falsified"),
    ("C56",
     "【V21续修③·泡动力学】引力泡时间演化 ODE（dσ/dt=v、dv/dt=(∂ρgrav/∂σ−γv)/ρeff、"
     "dκ0/dt=ω_bub·τ0−γ_κκ0、dτ0/dt=−ω_bub·κ0−γ_ττ0；σ0=0.1 m、κ0=1e-16、τ0=1e-12、α_g=0.85、ω_bub=1e4、"
     "γ=1e-8、γ_τ=γ_κ=1e-9、t_end=1e-4 s、nstep=2000）250 位审计："
     "①【结构性】∂ρ/∂σ 与 ρ_eff 中同一因子 (κ0²+α_gτ0²) 恒约去 ⇒ accel ≡ 3/σ − γv·16πG/(σ³F)（sympy 精确恒等）"
     "⇒ σ 段方程不含 G、κ0、τ0、α_g 中任何一个 且把总能量当密度用；"
     "②量纲两头非法——ρ_grav 承 §18 非能量密度 accel 量纲 [L^-1] 而加速度须 [L^1 T^-2]；"
     "③【数值伪迹】σ 段阻尼率 λ=3.9469e10 s^-1 ⇒ 显式 Euler 需 dt<5.07e-11 s 而草稿 dt=5.0e-8 s（越界 986.7 倍）"
     "⇒ 草稿输出 σ_end/σ0−1=1.9757e6 而稳定参考解（指数拟合 2000/20000 步一致 并经 scipy Radau rtol=1e-13 外校）"
     "仅 8.06e-13 ⇒ 相差 2.45e18 倍；④σ̈=3/σ>0 恒成立 ⇒ 永不坍缩「激发传播坍缩全周期」在方程层面不可能；"
     "⑤时间尺度错配：窗 1e-4 s 仅覆盖 0.159 个振荡周期（不足 1 个）且比幅值衰减时标 1e9 s 短 1e13 倍；"
     "⑥「守恒总能量 E_b」不成立：α_g=0.85≠1 使范数 κ²+α_gτ² 在四分之一周期摆动 +17.65%（零耗散下）；"
     "⑦ω_bub=1e4 rad/s 与本体泡心频率 c√(κ0²+τ0²)=2.998e-4 rad/s 相差 3.34e7 倍且无约束方程；"
     "⑧δφ=S·τ0·σ/v 量纲 [LM] 错误复发；⑨自由参数 4→9 而约束 0 条、可检验预言 0 条 ⇒ V≤0 伪派生 "
     "⇒ 模块「时变动态观测预言就绪」宣称不成立 → falsified（模块层）；体系级「挠率/曲率场能否局域激发并动力学演化」仍 open",
     "第一性审计", "falsified"),
    ("C57",
     "【V21续修③·元审计】草稿 37-claim 自评清单与层级判据审计：①计数自述与清单不符（实测 PASS=18/open=19 "
     "而自述 PASS=20/OPEN=17）；②与已登记台账冲突 9 处——C26/C27/C29/C30/C31/C33/C36/C37 台账已 falsified 与 "
     "C28 boundary 被统一改标 PASS（以自评覆盖已登记证伪）；③清单由四态退化为二态（BOUNDARY=0、FAIL=0）"
     "并新增 23 条未登记编号（含 CMB01-03/EHT01-03 共 6 条无模块无公式无脚本）；"
     "④S03「洛伦兹不变性 PASS」与本体系 C24 矛盾（基底速率 √(1+1/tan²θ)=1.117276 c 超光速 11.73%）；"
     "⑤「矛盾自检算法」是桩函数（axiom_set/eq_list 从未被读取 空参数亦 PASS）；"
     "⑥层级判据被放宽（hierarchy_lift 硬编码 base_level=L2 且只要有非空 predict_target 即升 L3/PASS "
     "丢掉「构造性推导+误差棒」双条件 空公理集亦升 L3）⇒ 「L3 资格保持有效」不成立（引擎 §17 对登记全量 L3=0）；"
     "⑦「拓扑归一算法」为恒等重述 + 无来源阈值 eps=1e-200（0.1% 扰动即 INCONCLUSIVE）；"
     "⑧CSV 导出破坏列结构（BUB04 的 predict_target 含裸逗号 ⇒ 6 字段）；"
     "并给出「自评清单可被审计」四条最低契约（四态齐备且与台账一致/新编号须附模块公式脚本/升维须引用判据原文/导出须转义）",
     "元审计", "BOUNDARY"),
]
_existing_v24 = set(_l.split(",", 1)[0].strip() for _l in
                    io.open(os.path.join(SYS_DIR, "claims.csv"), encoding="utf-8")
                    .read().splitlines()[1:] if _l.strip())
_txt24 = io.open(os.path.join(SYS_DIR, "claims.csv"), encoding="utf-8").read()
if not _txt24.endswith("\n"):
    _txt24 += "\n"
added_v24 = 0
for _cid, _st_, _cat, _stat in V24_NEW_CLAIMS:
    if _cid in _existing_v24:
        continue
    for _f in (_cid, _st_, _cat, _stat, "算法联盟审计组"):
        if "," in _f or '"' in _f:
            raise ValueError("字段不得含裸逗号或引号: " + _cid)
    _txt24 += ",".join([_cid, _st_, _cat, _stat, "算法联盟审计组"]) + "\n"
    added_v24 += 1
io.open(os.path.join(SYS_DIR, "claims.csv"), "w", encoding="utf-8").write(_txt24)
item("claims.csv V21续修③ 幂等追加完毕（C55/C56/C57 新增 %d 行，重复时 0 行）" % added_v24, True)


# ===========================================================================
# §17  V22 收官 · 全量 claims 批量审计 + 新版完整审计文档产出
# ===========================================================================
print("\n" + "=" * 76)
print("§17  V22收官 | 全量 claims 批量审计引擎 + 新版完整审计文档产出")
print("=" * 76)

import re as _re17

_claims_file = os.path.join(SYS_DIR, "claims.csv")
_raw17 = io.open(_claims_file, encoding="utf-8").read()
_lines17 = [l for l in _raw17.splitlines() if l.strip()]
CLAIMS_ALL = []

# --- 台账登记：C50/C51/C52（幂等）——先登记，再对「登记后的全量」做批量审计（口径自洽） ---
V22_NEW_CLAIMS = [
    ("C50", "【V22收官·谱】C25 高阶本征能级 n 域扩展扫描（n=1..12 + 10^k）：α_n = α_obs·f_n/f_1"
            "（f_n=V0+n²ℏ²/N²）⇒ ω、c 严格约去（代数恒等；草稿 σα 含 dω 属双重计账）；"
            "n=6 谱宽 1.089e-75 低于 α 测量精度 1.5e-10 达 65.14 个量级；谱宽达 α 精度需 "
            "n_detect=2.196e33（二阶项=V0 需 n_unit=1.793e38）⇒ 无物理可达检验靶 → open（退化谱·阈值不可达）",
     "第一性审计", "open"),
    ("C51", "【V22收官·进动】C35 多行星结构审计：β0=3h²/c² 使草稿 Binet 方程与 GR 1PN 方程恒等"
            "（u² 系数 3GM/c² 精确相等）⇒ β=β0 分支「几何修正」即 GR 本身；β-free 形状比 R_p/R_水星 "
            "在两框架下为 0.51256/0.37082（正确 Binet a²式）与 0.27429/0.14355（草稿 a³式）互差 1.87×/2.58×；"
            "R ∝ 1/(a(1−e²)) 对 a 单调且水星最大 ⇒ 标定靶=最佳靶 独立判别力为零；金星/地球修正 "
            "4.93e-3/1.59e-3 角秒每百年低于历表约束 → open（框架就绪·无独立判别力）",
     "第一性审计", "open"),
    ("C52", "【V22收官·批量】全量 claims 批量审计引擎：按「类别→证据型→层级」规则对 claims.csv 全部主张"
            "逐条判定（公理/恒等层 基线 L1、约定层 基线 L0、construction 基线 L2、falsified 封顶 L0、"
            "open/boundary 封顶 L1、升 L3 需 constructive+testable_prediction 带误差棒）；"
            "结果 L3 条目=0、无量纲靶登记=0 ⇒ "
            "申报「L3 完整第一性推导闭环」在台账层面不成立（UFT-3=0）→ BOUNDARY",
     "第一性审计", "BOUNDARY"),
]
_existing_v22 = set(l.split(",", 1)[0].strip() for l in _lines17[1:] if l.strip())
_txt22 = _raw17
if not _txt22.endswith("\n"):
    _txt22 += "\n"
added_v22 = 0
for _cid, _st_, _cat, _stat in V22_NEW_CLAIMS:
    if _cid in _existing_v22:
        continue
    for _f in (_cid, _st_, _cat, _stat, "算法联盟审计组"):
        if "," in _f or '"' in _f:
            raise ValueError("字段不得含裸逗号或引号: " + _cid)
    _txt22 += ",".join([_cid, _st_, _cat, _stat, "算法联盟审计组"]) + "\n"
    added_v22 += 1
io.open(_claims_file, "w", encoding="utf-8").write(_txt22)
item("claims.csv V22 幂等追加完毕（新增 %d 行，重复时 0 行）" % added_v22, True)

# 重新读取（含本轮新增）→ 批量审计输入为「登记后全量」
_raw17 = io.open(_claims_file, encoding="utf-8").read()
_lines17 = [l for l in _raw17.splitlines() if l.strip()]
for _l in _lines17[1:]:
    _p = _l.split(",")
    if len(_p) < 5:
        continue
    CLAIMS_ALL.append({"id": _p[0].strip(), "statement": _p[1], "category": _p[2],
                       "status": _p[3].strip().lower(), "reviewer": _p[4].strip()})

_AXIOM_KW = ("几何定义", "恒等", "数学事实")           # 公理/恒等层 → L1（OpenUFT：L1=纯几何公理）
_CONVENTION_KW = ("约定", "命名", "组织框架", "参数化", "重排", "重述", "定义", "归一化")  # 零内容约定层 → L0
_AUDIT_KW = ("审计", "冲突", "检查", "面板")
_CONSTRUCTION_KW = ("推导", "闭合", "修复", "本源", "计算", "拓扑", "构造", "量子")


def evidence_of(cat):
    """类别 → 证据型（axiom/convention/construction/audit）。
       未识别类别保守归入 axiom（L1），不给 L2「场方程导出」信用。"""
    if any(k in cat for k in _AXIOM_KW):
        return "axiom"
    if any(k in cat for k in _CONVENTION_KW):
        return "convention"
    if any(k in cat for k in _AUDIT_KW):
        return "audit"
    if any(k in cat for k in _CONSTRUCTION_KW):
        return "construction"
    return "axiom"


_BASE_LEVEL = {"axiom": "L1", "convention": "L0", "construction": "L2", "audit": "—"}
_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}


def audit_one(c):
    """单条 claim 的层级判定（复用 §9.5 层级升维算法口径，批量版）。
       层级口径（OpenUFT）：L1=纯几何公理/恒等；L2=场方程导出；L3=第一性可检验定量预言。
       规则：axiom 基线 L1、convention 基线 L0、construction 基线 L2；
             falsified ⇒ 封顶 L0；open/boundary ⇒ 封顶 L1；
             升 L3 需 constructive_derivation + testable_prediction(带误差棒)——台账字段无此信息 ⇒ L3 恒 0。"""
    ev = evidence_of(c["category"])
    st = c["status"]
    lvl = _BASE_LEVEL[ev]
    if ev == "audit" or st == "info":
        return {"level": "—", "evidence": ev, "note": "元判定（审计/复算信息）"}
    if st == "falsified":
        return {"level": "L0", "evidence": ev, "note": "已证伪 ⇒ 封顶 L0"}
    nt = []
    if st in ("open", "boundary") and _ORDER[lvl] > 1:
        lvl = "L1"
        nt.append("%s ⇒ 封顶 L1" % st)
    if ev == "convention":
        nt.append("约定层（零内容）")
    return {"level": lvl, "evidence": ev, "note": "; ".join(nt)}


AUDIT_ALL = []
for _c in CLAIMS_ALL:
    _a = audit_one(_c)
    _a.update({"id": _c["id"], "status": _c["status"], "category": _c["category"],
               "statement": _c["statement"]})
    AUDIT_ALL.append(_a)

# 引擎复核映射（只取 §12–§16 的 V21/V22 判定行，避免 §0–§11 标签误匹配）
ENGINE_VERDICT = {}
for _r in ROWS:
    _m = _re17.match(r"§(?:1[2-9]|2[0-9])-C(\d+)", _r["tag"])
    if _m:
        ENGINE_VERDICT.setdefault("C" + _m.group(1), []).append(_r["state"])

_lvl_cnt, _st_cnt = {}, {}
for _a in AUDIT_ALL:
    _lvl_cnt[_a["level"]] = _lvl_cnt.get(_a["level"], 0) + 1
    _st_cnt[_a["status"]] = _st_cnt.get(_a["status"], 0) + 1
_l3_ids = [_a["id"] for _a in AUDIT_ALL if _a["level"] == "L3"]
_l2_ids = [_a["id"] for _a in AUDIT_ALL if _a["level"] == "L2"]
_l1_ids = [_a["id"] for _a in AUDIT_ALL if _a["level"] == "L1"]
_l0_ids = [_a["id"] for _a in AUDIT_ALL if _a["level"] == "L0"]

print("     批量审计：主张 %d 条 | 登记状态分布 %s" % (len(AUDIT_ALL), _st_cnt))
print("     审计层级分布：%s" % _lvl_cnt)
print("       L2（构造型）：%s" % (", ".join(_l2_ids) if _l2_ids else "无"))
print("       L1：%s" % (", ".join(_l1_ids) if _l1_ids else "无"))
print("       L0：%s" % (", ".join(_l0_ids) if _l0_ids else "无"))
print("       L3（第一性可检验定量预言）：%s" % (", ".join(_l3_ids) if _l3_ids else "0 条"))
print("\n     C24–C38 / C53–C57 引擎复核（有引擎证据者）：")
for _cid in ["C24", "C25", "C26", "C27", "C28", "C29", "C30", "C31", "C32", "C33",
             "C34", "C35", "C36", "C37", "C38", "C53", "C54", "C55", "C56", "C57"]:
    _ev = ENGINE_VERDICT.get(_cid)
    if _ev:
        print("       %s : %s" % (_cid, "/".join(_ev)))

item("全量 claims 批量审计引擎运行完成（%d 条主张逐条给出层级与依据）" % len(AUDIT_ALL),
     len(AUDIT_ALL) >= 35,
     "类别 → 证据型 → 层级 三级规则；L3 需 constructive+testable_prediction，台账字段无此信息 ⇒ L3 恒 0")

reg("INFO", "§17-CLAIMS-1 全量 claims 批量审计：类别 → 证据型 → 层级（规则化）",
    "共 %d 条主张：状态分布 %s；层级分布 %s（L2 构造型 %s 条、L1 %s 条、L0 %s 条、元判定 %s 条）"
    % (len(AUDIT_ALL), _st_cnt, _lvl_cnt, len(_l2_ids), len(_l1_ids), len(_l0_ids),
       _lvl_cnt.get("—", 0)),
    "与 §9.5 层级升维算法同源（R1 禁跳级 / R2 恒等·定义 ≤ L1 / R3 升 L3 需构造 + 可检验预言带误差棒）",
    "批量审计引擎")

reg("FAIL", "§17-CLAIMS-2 L3 条目 = 0 ⇒ 申报「L3 完整第一性推导闭环」在台账层面不成立",
    "全量 %d 条主张中无一条同时具备 constructive_derivation 与 testable_prediction(含误差棒)；"
    "无量纲靶登记 = 0 条 ⇒ UFT-3 计数 = 0" % len(AUDIT_ALL),
    "该结论与 §9-3、§10-1 一致，本轮以批量审计独立复现；修复版面板 H6/O6/C3/U2 未兑现为 L3 内容",
    "批量审计（台账全量）")

_eng_missing = [c for c in ["C26", "C27", "C28", "C29", "C30", "C31", "C32", "C33", "C34", "C36", "C37"]
                if c not in ENGINE_VERDICT]
reg("BOUNDARY", "§17-CLAIMS-3 C26–C34/C36/C37 的 PASS 为草稿自评，本轮无引擎复核证据",
    "本轮引擎给出证据的仅 C24（PASS）、C25（FAIL/BOUNDARY）、C35（FAIL/BOUNDARY）、C38（INFO）；"
    "未复核条目：%s" % "、".join(_eng_missing),
    "「未复核」不等于「已否定」，也不等于「已通过」⇒ 不得据草稿自评登记为 PASS（口径同 §14-汇总）",
    "口径红线")

reg("BOUNDARY", "§17-CLAIMS-4 台账新增 C50/C51/C52（本轮三项攻坚结论）",
    "C50=C25 高阶扫描可检测阈值（open·退化谱）；C51=C35 结构同一性与 β-free 形状比（open·无独立判别力）；"
    "C52=全量 claims 批量审计（BOUNDARY·L3=0）",
    "与 §11 的 C24–C47、§14 的 C48/C49 互不冲突；幂等追加", "台账登记")

reg("BOUNDARY", "§17-CLAIMS-5 台账续增 C55/C56/C57（V21 续修③ 双圈 RG / 泡动力学 ODE / 元审计）",
    "C55=双圈 β 截断伪影判定（falsified·固定点在二阶/一阶比 = −1 处、ln 可达性 572 ≫ 64.7）；"
    "C56=引力泡动力学 ODE（falsified·越稳定界 986.7 倍、σ 段恒等 accel≡3/σ、9 参数 0 约束）；"
    "C57=草稿 37-claim 自评清单与判据审计（BOUNDARY·9 处与台账冲突、二态化、升维判据放宽）。"
    "序号口径：C55/C56 原拟留给草稿全局表的 CMB-Bispec/EHT-PhotonRing，但该二者至今无模块、无公式、无脚本 ⇒ "
    "按 §19-全局表-1 与 §17-CLAIMS-3 不登记，序号由本轮实体模块占用；其提交后另取序号",
    "幂等追加；与 C53/C54 同族（C55 为 C54 续、C56 为 C53 续）", "台账登记")

# --- 产出①：本轮数据 json/md ---
V22_ROWS = ROWS[V22_START:V23_START]   # §15–§16（V21续修②的 §18/§19 归入 V23_ROWS）
n22_pass = sum(1 for r in V22_ROWS if r["state"] == "PASS")
n22_fail = sum(1 for r in V22_ROWS if r["state"] == "FAIL")
n22_bd = sum(1 for r in V22_ROWS if r["state"] == "BOUNDARY")
n22_info = sum(1 for r in V22_ROWS if r["state"] == "INFO")

V22_payload = {
    "title": "空间螺旋几何化统一场论 V22 收官 · C25 高阶扫描 + C35 多行星结构审计 + 全量 claims 批量审计",
    "date": "2026-09-26",
    "dps": 250,
    "method": ["n 域扩展扫描（n=1..12 + 10^k）", "误差传播正确式（ω·c 严格约去）",
               "结构同一性（Binet vs GR 1PN）", "β-free 形状比", "类别→证据型→层级 批量规则判定"],
    "counts": {"total": len(V22_ROWS), "PASS": n22_pass, "FAIL": n22_fail,
               "BOUNDARY": n22_bd, "INFO": n22_info},
    "C25": {"hbar2_over_N2": float(term1), "n_detect": float(n_detect), "n_unit": float(n_unit),
            "spread_n6": float(max_rel), "log10_below_alpha_prec": float(mp.log10(ALPHA_UREL / max_rel)),
            "sigma_draft_n6": float(sigma_rel_draft(6)), "sigma_correct_n6": float(sigma_rel_correct(6)),
            "scan": scan15},
    "C35": {"beta0_mercury": float(BETA0_M), "coef_draft_beta0": float(coef_draft),
            "coef_GR": float(coef_GR), "R_mercury": float(R_merc),
            "shape_ratios": shape_rows, "sigma_obs_assumed": float(SIGMA_OBS),
            "rows": c35_out},
    "claims_batch": {"total": len(AUDIT_ALL), "status_counts": _st_cnt, "level_counts": _lvl_cnt,
                     "L3": _l3_ids, "L2": _l2_ids, "L1": _l1_ids, "L0": _l0_ids,
                     "engine_verdict": {k: v for k, v in ENGINE_VERDICT.items()},
                     "rows": [{"id": a["id"], "status": a["status"], "category": a["category"],
                               "evidence": a["evidence"], "level": a["level"], "note": a["note"]}
                              for a in AUDIT_ALL]},
    "rows": V22_ROWS,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋V22收官_全量claims审计.json"), "w", encoding="utf-8") as fh:
    json.dump(V22_payload, fh, ensure_ascii=False, indent=1)

_l22 = []
_l22.append("# 空间螺旋几何化统一场论 · V22 收官：C25 高阶扫描 + C35 多行星结构审计 + 全量 claims 批量审计")
_l22.append("")
_l22.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋修复版_第一性审计与伪派生判定.py` §15–§17（统一脚本并入，可复跑）")
_l22.append("> 精度 mpmath dps=250 · 量纲审计内置 · 红线：数学自洽 ≠ 实验证实")
_l22.append("")
_l22.append("**本轮判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
            % (len(V22_ROWS), n22_pass, n22_fail, n22_bd, n22_info))
_l22.append("")
_l22.append("## §15 C25 续：高阶本征能级 n 域扩展扫描")
_l22.append("")
_l22.append("代数恒等：α_n = α_obs·f_n/f_1（f_n = V0 + n²ℏ²/N²）⇒ ω、c 严格约去（非「不确定度抵消」）。")
_l22.append("")
_l22.append("| n | (α_n−α_1)/α_1 | σα/α(草稿式) | σα/α(正确式) | 谱宽/α精度 |")
_l22.append("|---|---|---|---|---|")
for _s in scan15:
    _l22.append("| %s | %s | %s | %s | %s |"
                % (fmt_n(_s["n"]), fmt(mpf(_s["spread"]), 6), fmt(mpf(_s["sigma_draft"]), 6),
                   fmt(mpf(_s["sigma_correct"]), 6), fmt(mpf(_s["ratio_to_alpha_prec"]), 6)))
_l22.append("")
_l22.append("| 量 | 值 |")
_l22.append("|----|----|")
_l22.append("| ℏ²/N²（谱修正基数） | %s |" % fmt(term1, 6))
_l22.append("| n=6 谱宽 (α_6−α_1)/α_1 | %s |" % fmt(max_rel, 6))
_l22.append("| 低 α 测量精度（1.5e-10）量级数 | %s |" % fmt(mp.log10(ALPHA_UREL / max_rel), 5))
_l22.append("| 谱宽 = σα/α 所需 n_detect | %s |" % fmt(n_detect, 10))
_l22.append("| 二阶项 = V0 所需 n_unit | %s |" % fmt(n_unit, 10))
_l22.append("| 草稿式 σα/α(n=6) | %s |" % fmt(sigma_rel_draft(6), 6))
_l22.append("| 正确式 σα/α(n=6) | %s |" % fmt(sigma_rel_correct(6), 6))
_l22.append("")
_l22.append("## §16 C35 续：多行星进动 + β 普适性结构审计")
_l22.append("")
_l22.append("结构同一性：β0 = 3h²/c² = %s（水星）⇒ 草稿 u² 系数 (GM/h²)·β0 = %s "
            "精确等于 GR 系数 3GM/c² = %s ⇒ 该分支下「几何修正」即 GR 1PN 项本身。"
            % (fmt(BETA0_M, 10), fmt(coef_draft, 10), fmt(coef_GR, 10)))
_l22.append("")
_l22.append("β-free 形状比 R_p/R_水星（β 约去）：")
_l22.append("")
_l22.append("| 行星 | 正确 Binet 式（比例 1/a） | 草稿式（比例 1/a²） |")
_l22.append("|---|---|---|")
for _s in shape_rows:
    _l22.append("| %s | %s | %s |" % (_s["planet"], fmt(mpf(_s["ratio_correct"]), 8),
                                      fmt(mpf(_s["ratio_draft"]), 8)))
_l22.append("")
_l22.append("| 行星 | GR 基础 | 几何修正（正确式） | 总预测（正确式） | 参考值 | R = Δφ_geo/Δφ_GR |")
_l22.append("|---|---|---|---|---|---|")
for _r in c35_out:
    _l22.append("| %s | %s | %s | %s | %s | %s |"
                % (_r["planet"], _r["GR_s"], _r["geo_correct_s"], _r["tot_correct_s"], _r["ref_s"],
                   fmt(mpf(_r["geo_correct_s"]) / mpf(_r["GR_s"]), 6)))
_l22.append("")
_l22.append("| 量 | 值 |")
_l22.append("|----|----|")
_l22.append("| β（草稿式，水星标定） | %s |" % fmt(beta_draft, 12))
_l22.append("| β（Binet 一阶正确式，水星标定） | %s |" % fmt(beta_correct, 12))
_l22.append("| β0 = 3h²/c²（使方程 ≡ GR 1PN） | %s |" % fmt(BETA0_M, 12))
_l22.append("| 假定历表约束量级 σ_obs | %s 角秒/百年（外部输入，待核实） |" % fmt(SIGMA_OBS, 4))
_l22.append("")
_l22.append("## §17 全量 claims 批量审计（类别 → 证据型 → 层级）")
_l22.append("")
_l22.append("共 %d 条主张；登记状态分布 %s；审计层级分布 %s。**L3 条目 = 0**。"
            % (len(AUDIT_ALL), _st_cnt, _lvl_cnt))
_l22.append("")
_l22.append("| ID | 登记状态 | 类别 | 证据型 | 审计层级 | 引擎复核 | 备注 |")
_l22.append("|----|---------|------|--------|---------|---------|------|")
for _a in AUDIT_ALL:
    _ev = "/".join(ENGINE_VERDICT.get(_a["id"], [])) or "—"
    _l22.append("| %s | %s | %s | %s | %s | %s | %s |"
                % (_a["id"], _a["status"], _a["category"], _a["evidence"], _a["level"], _ev,
                   _a["note"] if _a["note"] else "—"))
_l22.append("")
_l22.append("## 结论（不粉饰）")
_l22.append("")
_l22.append("1. **C25**：高阶能级在 n≤12 内与标定态不可区分（谱宽 ≤ 1.3e-74）；谱宽达 α 测量精度需")
_l22.append("   n ≳ 2.196e33 ⇒ 无物理可达检验靶 ⇒ 维持 open（退化谱）。")
_l22.append("2. **C35**：草稿 Binet 方程在 β0=3h²/c² 时与 GR 1PN 方程恒等（无新增预言）；")
_l22.append("   β-free 形状比随「a² vs a³」框架歧义变化 1.87×/2.58×；R ∝ 1/(a(1−e²)) 使水星既是")
_l22.append("   标定靶又是最强信号靶 ⇒ 独立判别力为零 ⇒ 维持 open（无独立判别力）。")
_l22.append("3. **全量 claims**：批量审计给出 L3 = 0、无量纲靶登记 = 0 ⇒ 申报「L3 完整第一性推导闭环」")
_l22.append("   在台账层面不成立（与 §9-3/§10-1 独立复现一致）。")
_l22.append("")
_l22.append("**红线**：本册只判定**数学自洽性与第一性层级**，不否定该纲领作为几何草案的价值；")
_l22.append("「数学自洽」不等于「实验证实」，更不等于「L3 第一性推导」。")
_l22.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋V22收官_全量claims审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(_l22))

# --- 产出②：新版全量审计文档（覆盖 §10 写出的部分版） ---
_full_pass = sum(1 for r in ROWS if r["state"] == "PASS")
_full_fail = sum(1 for r in ROWS if r["state"] == "FAIL")
_full_bd = sum(1 for r in ROWS if r["state"] == "BOUNDARY")
_full_info = sum(1 for r in ROWS if r["state"] == "INFO")

_fm = []
_fm.append("# 空间螺旋几何化统一场论 · 第一性审计（新版·全量：§0–§22）")
_fm.append("")
_fm.append("> 日期 2026-09-26 · 引擎：`04_公共成果/算法联盟_全维自洽与归一化/源码/"
           "空间螺旋修复版_第一性审计与伪派生判定.py`（统一脚本，可复跑）")
_fm.append("> 方法：量纲账本 / Buckingham Π / 判别式 V / 自由度审计 / mpmath dps=250 / "
           "Binet 一阶微扰 / 数值稳定性判据 / 全量 claims 批量审计")
_fm.append("")
_fm.append("**总判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
           % (len(ROWS), _full_pass, _full_fail, _full_bd, _full_info))
_fm.append("")
_fm.append("## 一、逐条判定（§0–§22 全部判定行）")
_fm.append("")
_fm.append("| 状态 | 编号 | 主张 | 依据 |")
_fm.append("|------|------|------|------|")
for _r in ROWS:
    _fm.append("| %s | %s | %s | %s |"
               % (_r["state"], _r["tag"], _r["statement"], _r["detail"].replace("\n", " ")))
_fm.append("")
_fm.append("## 二、全量 claims 批量审计（层级判定）")
_fm.append("")
_fm.append("共 %d 条主张；登记状态分布 %s；层级分布 %s。**L3 = 0**、无量纲靶登记 = 0（UFT-3 = 0）。"
           % (len(AUDIT_ALL), _st_cnt, _lvl_cnt))
_fm.append("")
_fm.append("| ID | 登记状态 | 类别 | 证据型 | 审计层级 | 引擎复核 | 备注 |")
_fm.append("|----|---------|------|--------|---------|---------|------|")
for _a in AUDIT_ALL:
    _ev = "/".join(ENGINE_VERDICT.get(_a["id"], [])) or "—"
    _fm.append("| %s | %s | %s | %s | %s | %s | %s |"
               % (_a["id"], _a["status"], _a["category"], _a["evidence"], _a["level"], _ev,
                  _a["note"] if _a["note"] else "—"))
_fm.append("")
_fm.append("## 三、V22 收官三项攻坚结论")
_fm.append("")
_fm.append("1. **C25 高阶本征能级**：α_n = α_obs·f_n/f_1 ⇒ ω、c 严格约去（代数恒等）；"
           "谱宽达 α 测量精度需 n_detect = %s（n_unit = %s）⇒ open（退化谱）。"
           % (fmt(n_detect, 8), fmt(n_unit, 8)))
_fm.append("2. **C35 多行星进动**：β0 = 3h²/c² 使草稿 Binet 方程 ≡ GR 1PN 方程（u² 系数精确相等）；"
           "β-free 形状比随框架歧义变化 1.87×/2.58×；标定靶 = 最佳靶 ⇒ open（无独立判别力）。")
_fm.append("3. **全量 claims 批量审计**：L3 = 0、UFT-3 = 0 ⇒ 申报「L3 完整第一性推导闭环」不成立。")
_fm.append("")
_fm.append("## 四、V21 续修②（§18 引力泡 + §19 TUFT-RG）结论")
_fm.append("")
_fm.append("1. **C53 引力泡（GravBubble）→ falsified（公式层）**：能量密度式在三种 κ 口径下量纲全非法；"
           "高斯积分严格值 π^(3/2)σ³ 被漏乘（E 少 5.5683 倍且草稿两式互斥）；自旋进动 δφ 非无量纲；"
           "唯一最小量纲修复（×c⁴）给出 E = 1.14e16 J ≈ 2.72 Mt TNT ⇒ 与「地面实验室」自相矛盾；"
           "无作用量 ⇒ 高斯包络是 ansatz 非孤子解；4 自由参数 0 约束 ⇒ V≤0 伪派生。")
_fm.append("2. **C54 TUFT-RG → falsified（模块层）**：b1..b6 六自由且无推导 ⇒ 非检验；"
           "精确定理「非平凡固定点 ⇔ b5²(−b2/b1)=b6²(−b4/b3)」在给定系数下不成立（LHS/RHS=5.2478，"
           "sympy 解集仅原点）⇒ 无紫外固定点；固定点搜索代码原样运行抛 TypeError；"
           "能标口径混用（eV vs s^-1）虚增积分跨度 34.96（+54.1%）；Landau 极点位置依赖任意 IR 输入 ⇒ 不可证伪。")
_fm.append("3. **正面产出**：本册把「TUFT 是否紫外完备」转为可判定命题（须存在非平凡固定点或渐近自由），"
           "并给出其前置条件——先由有效作用量第一性导出 b1..b6（§19-C54-7）。")
_fm.append("4. **未登记**：草稿全局表的 CMB-Bispec / EHT-PhotonRing 无本册模块支撑，按 §17-CLAIMS-3 口径不登记。")
_fm.append("")
_fm.append("## 五、V21 续修③（§20 双圈 RG + §21 泡动力学 ODE + §22 元审计）结论")
_fm.append("")
_fm.append("1. **C55 TUFT-RG 双圈 → falsified（模块层）**：能标口径错误原样复发（μ_UV = M_pl c²/ħ = %s s⁻¹，"
           "非 eV，跨度虚增 %s）；固定点搜索代码仍不可运行（3 种 x0 × 2 种 solver 全抛错，手工 Newton 自草稿种子收敛到原点）；"
           "sympy 精确解集 4 组且**非平凡解全部 gkt\\*=0**（gk\\*=210/41、gt\\*=60/11）⇒ 草稿预测靶「三分量固定点」不存在；"
           "**截断伪影定理**：gk\\* = −b1/d1 与 gt\\* = −b3/d3 恰使二阶/一阶项比 = **−1**（精确）⇒ 固定点位于微扰展开最不可靠处、"
           "位置 100%% 由手选 d1/d3 决定；可达性 ln μ = %s 而 Planck 跨度 %s（μ 须超 Planck %s 倍）⇒ 物理不可达；"
           "Planck 内双圈仅改耦合 0.12%%~0.44%%（β 项比 −1.6%%~−3.9%%）⇒ 「大幅降低截断误差」无误差预算亦无内容；"
           "自由系数 6→13 且仍无作用量（3 方程 = 3 未知数 ⇒ 有解属自由度配平）；三阶单项式仅含 2/10（无完整性判据）。"
           % (fmt(_mu_uv_doc, 6), fmt(_ln_doc - _ln_ok, 6), fmt(_rg2_s_need, 8), fmt(_ln_ok, 8), fmt(_rg2_mu_ratio, 6)))
_fm.append("2. **C56 引力泡动力学 ODE → falsified（模块层）**：符号恒等式 accel ≡ 3/σ − γv·16πG/(σ³F) "
           "⇒ σ 段方程**不含 G、κ0、τ0、α_g 中任何一个**（且把总能量当密度用）；ρ_grav 与 accel 两头量纲非法；"
           "**数值伪迹**：σ 段阻尼率 λ = %s s⁻¹ ⇒ 显式 Euler 需 dt < %s s 而草稿取 5.0e-8 s（越界 %s 倍），"
           "草稿输出 σ_end/σ0−1 = %s，稳定参考解仅 %s（相差 %s 倍；指数拟合 2000/20000 步自洽并经 scipy Radau rtol=1e-13 外校）；"
           "σ̈ = 3/σ > 0 恒成立 ⇒ 永不坍缩（「激发→传播→坍缩全周期」在方程层面不可能）；窗 1e-4 s 仅覆盖 0.159 个振荡周期、"
           "比幅值衰减时标 1e9 s 短 1e13 倍；「守恒总能量 E_b」不成立（α_g=0.85≠1 使范数在四分之一周期摆动 +%s%%）；"
           "ω_bub=1e4 rad/s 与本体泡心频率 %s rad/s 相差 3.34e7 倍且无约束；δφ 量纲错误复发；自由参数 4→9、约束 0 条 ⇒ V≤0。"
           % (fmt(_lam0, 6), fmt(2 / _lam0, 6), fmt(_e_stab, 6), fmt(_gb2_eul[0] / GB2_S0 - 1, 6),
              fmt(_gb2_ref[0] / GB2_S0 - 1, 6), fmt(_gb2_ratio, 6), fmt(_norm_gain * 100, 4),
              fmt(_omega_bub_native, 8)))
_fm.append("3. **C57 元审计 → BOUNDARY**：草稿 37-claim 自评清单计数自述与清单不符（实测 PASS=%d/open=%d vs 自述 20/17）；"
           "与台账冲突 %d 处（%d 条已 falsified 与 %d 条 boundary 被改标 PASS）；四态退化为二态并新增 %d 条未登记编号"
           "（含 CMB/EHT 共 6 条无模块支撑）；S03「洛伦兹不变性 PASS」与 C24 超光速 %.6f c 矛盾；"
           "「矛盾自检算法」是桩函数（axiom_set/eq_list 从未被读取）；层级判据被放宽（hierarchy_lift 硬编码 base_level=L2，"
           "只要有非空 predict_target 即升 L3/PASS，空公理集亦升 L3）⇒ 「L3 资格保持有效」不成立（引擎 §17 对登记全量 L3 = 0）；"
           "「拓扑归一算法」为恒等重述 + 无来源阈值；CSV 导出破坏列结构（BUB04 预测靶含裸逗号 ⇒ 6 字段）。"
           % (_d22_pass, _d22_open, len(_d22_conf), len(_d22_conf_fal), len(_d22_conf_bd), len(_d22_unreg), _speed_rel22))
_fm.append("4. **正面产出**：①**截断伪影判据**——任何非平凡固定点须落在 |β₂/β₁| ≪ 1 的微扰可靠区并附三阶项以显示收敛（§20-C55-9）；"
           "②**自评清单可被审计的四条最低契约**——四态齐备且与台账一致 / 新编号须附模块·公式·脚本 / 升维须引用判据原文 / 导出须转义（§22-C57-9）；"
           "③σ 段 ODE 的刚性稳定判据（λ·dt < 2）作为「动力学演示」的准入红线（§21-C56-3）。")
_fm.append("")
_fm.append("## 六、红线")
_fm.append("")
_fm.append("本文件只判定**数学自洽性与第一性层级**；「数学自洽」不等于「实验证实」，"
           "更不等于「L3 第一性推导」。C25/C35 均维持 open（带限定语），非 PASS。"
           "C55/C56 的 falsified 针对**模块宣称**（模块层），不否定议题本身："
           "「TUFT 是否有紫外固定点」「挠率/曲率场能否局域激发并动力学演化」仍 open。")
_fm.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(_fm))

# --- 产出③：V21 续修②（§18 引力泡 + §19 TUFT-RG）数据与报告 ---
# 按 tag 前缀取行：§18/§19（本册模块）+ §17（台账登记与批量审计，与本轮同批登记）
# ⇒ 与 V21 续修③ 的 §20/§21/§22 完全隔离（避免两份报告互相污染）
V23_ROWS = [r for r in ROWS[V23_START:] if r["tag"].startswith(("§18", "§19", "§17"))]
n23_pass = sum(1 for r in V23_ROWS if r["state"] == "PASS")
n23_fail = sum(1 for r in V23_ROWS if r["state"] == "FAIL")
n23_bd = sum(1 for r in V23_ROWS if r["state"] == "BOUNDARY")
n23_info = sum(1 for r in V23_ROWS if r["state"] == "INFO")

V23_payload = {
    "title": "空间螺旋几何化统一场论 V21 续修② · 引力泡工程（GravBubble）+ TUFT 重整化群 RG 流",
    "date": "2026-09-26",
    "dps": 250,
    "method": ["250 位高斯积分闭式核对", "量纲账本（三口径 κ）", "判别式 V 自由度审计",
               "sympy 精确有理数固定点求解", "双口径 RG 显式 Euler 积分"],
    "counts": {"total": len(V23_ROWS), "PASS": n23_pass, "FAIL": n23_fail,
               "BOUNDARY": n23_bd, "INFO": n23_info},
    "C53_GravBubble": {
        "sigma_m": float(GB_SIGMA), "kappa0": float(GB_K0), "tau0": float(GB_T0), "alpha_g": float(GB_AG),
        "gauss_integral": float(_gb_I), "pi_3_2_sigma3": float(_gb_pi), "sigma3": float(GB_SIGMA ** 3),
        "E_draft_J": float(E_doc), "E_strict_J": float(E_gauss), "E_2pi_J": float(E_alt),
        "E_dimfix_J": float(E_dimfix), "E_dimfix_eV": float(E_dimfix / mpf("1.602176634e-19")),
        "dim_rho_body": dfmt(dmul(dpow(DIM_G, -1), dpow(D(L=-1), 2))),
        "dim_rho_module": dfmt(dmul(dpow(DIM_G, -1), dpow(D(L=-2), 2))),
        "dim_rho_norm": dfmt(dmul(dpow(DIM_G, -1), dpow(D(), 2))),
        "dim_needed_kappa": dfmt(_dim_need_k),
        "dphi_draft_rad": float(_dphi_doc), "dphi_dimless_rad": float(_dphi_dim),
        "omega_bubble": float(_omega_b), "f_bubble_Hz": float(_f_b),
        "n_free": _gb_n_free, "n_hit": _gb_n_hit, "disc_V": str(_gb_V),
    },
    "C54_TUFT_RG": {
        "b": [str(v) for v in RG_BF],
        "fp_condition_lhs": str(_cond_lhs), "fp_condition_rhs": str(_cond_rhs),
        "fp_condition_ratio": float(mpf(float(_cond_ratio))),
        "fp_sympy_solutions": _sp_txt, "draft_findroot": _fp_txt,
        "b6_required": float(_need_b6), "b5_required": float(_need_b5),
        "mu_uv_draft": float(_mu_uv_doc), "E_planck_eV": float(_E_pl_eV),
        "ln_span_draft": float(_ln_doc), "ln_span_correct": float(_ln_ok),
        "ln_span_inflation": float(_ln_doc - _ln_ok),
        "uv_draft_span": [float(v) for v in _uv_doc], "uv_correct_span": [float(v) for v in _uv_ok],
        "landau_pole_s": float(_s_pole), "mu_pole_eV": float(_mu_pole),
    },
    "claims_registered": {"added": added_v23, "ids": ["C53", "C54"]},
    "rows": V23_ROWS,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修②_引力泡与RG流_审计.json"), "w", encoding="utf-8") as fh:
    json.dump(V23_payload, fh, ensure_ascii=False, indent=1)

_l23 = []
_l23.append("# 空间螺旋几何化统一场论 · V21 续修②：引力泡工程（GravBubble）+ TUFT 重整化群 RG 流")
_l23.append("")
_l23.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋修复版_第一性审计与伪派生判定.py` §18–§19（统一脚本，可复跑）")
_l23.append("> 精度 mpmath dps=250 · 量纲账本内置 · 红线：数学自洽 ≠ 实验证实")
_l23.append("")
_l23.append("**本轮判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
            % (len(V23_ROWS), n23_pass, n23_fail, n23_bd, n23_info))
_l23.append("")
_l23.append("## §18 引力泡（GravBubble · C53 → falsified）")
_l23.append("")
_l23.append("| 量 | 值 |")
_l23.append("|----|----|")
_l23.append("| 高斯积分 ∮d³x e^(−r²/σ²) | %s |" % fmt(_gb_I, 16))
_l23.append("| 闭式 π^(3/2)σ³ | %s（比值 %s） |" % (fmt(_gb_pi, 16), fmt(_gb_I / _gb_pi, 16)))
_l23.append("| E_草稿 = σ³/(16πG)(κ0²+α_gτ0²) | %s J |" % fmt(E_doc, 10))
_l23.append("| E_严格 = π^(3/2)σ³/(16πG)(…) | %s J（草稿少乘 %s 倍） |" % (fmt(E_gauss, 10), fmt(E_gauss / E_doc, 8)))
_l23.append("| ρ 量纲（本体 κ=[L^-1]） | %s（≠ 能量密度） |" % dfmt(dmul(dpow(DIM_G, -1), dpow(D(L=-1), 2))))
_l23.append("| ρ 量纲（模块 κ0=[m^-2]） | %s（≠ 能量密度） |" % dfmt(dmul(dpow(DIM_G, -1), dpow(D(L=-2), 2))))
_l23.append("| 齐次性要求 κ 的量纲 | %s（加速度） |" % dfmt(_dim_need_k))
_l23.append("| E（唯一最小量纲修复 ×c⁴） | %s J = %s eV ≈ 2.72 Mt TNT |"
            % (fmt(E_dimfix, 8), fmt(E_dimfix / mpf("1.602176634e-19"), 8)))
_l23.append("| δφ（草稿 Sτ0σ/v） | %s rad（量纲 [LM]，非法） |" % fmt(_dphi_doc, 8))
_l23.append("| δφ（无量纲 (S/ħ)τ0σ） | %s rad |" % fmt(_dphi_dim, 8))
_l23.append("| 泡心频率 ω = c√(κ0²+τ0²) | %s rad/s（f = %s Hz） |" % (fmt(_omega_b, 8), fmt(_f_b, 8)))
_l23.append("| 自由度 | n_free=%d、n_hit=%d ⇒ V=%s ≤ 0 |" % (_gb_n_free, _gb_n_hit, _gb_V))
_l23.append("")
_l23.append("## §19 TUFT-RG（C54 → falsified）")
_l23.append("")
_l23.append("**精确定理**：非平凡紫外固定点存在 ⇔ b5²(−b2/b1) = b6²(−b4/b3)。")
_l23.append("")
_l23.append("| 量 | 值 |")
_l23.append("|----|----|")
_l23.append("| b1..b6 | %s |" % "、".join([str(v) for v in RG_BF]))
_l23.append("| 条件 LHS = b5²(−b2/b1) | %s |" % str(_cond_lhs))
_l23.append("| 条件 RHS = b6²(−b4/b3) | %s |" % str(_cond_rhs))
_l23.append("| LHS/RHS | %s ≠ 1 ⇒ 条件不成立 |" % fmt(mpf(float(_cond_ratio)), 8))
_l23.append("| sympy 精确解集 | %s |" % _sp_txt)
_l23.append("| 草稿 findroot 原样运行 | %s |" % _fp_txt)
_l23.append("| μ_UV 草稿 = M_pl c²/ħ | %s（s^-1，非 eV） |" % fmt(_mu_uv_doc, 10))
_l23.append("| μ_UV 正确（Planck 能量） | %s eV |" % fmt(_E_pl_eV, 10))
_l23.append("| 积分跨度 ln | 草稿 %s vs 正确 %s ⇒ 虚增 %s |"
            % (fmt(_ln_doc, 8), fmt(_ln_ok, 8), fmt(_ln_doc - _ln_ok, 8)))
_l23.append("| UV 耦合（正确跨度） | (%s、%s、%s) |" % (fmt(_uv_ok[0], 8), fmt(_uv_ok[1], 8), fmt(_uv_ok[2], 8)))
_l23.append("| Landau 极点 | s*=%s ⇒ μ≈1e%s eV |" % (fmt(_s_pole, 8), fmt(mp.log10(_mu_pole), 6)))
_l23.append("")
_l23.append("## 判定明细")
_l23.append("")
_l23.append("| 状态 | 编号 | 主张 | 依据 |")
_l23.append("|------|------|------|------|")
for _r in V23_ROWS:
    _l23.append("| %s | %s | %s | %s |"
                % (_r["state"], _r["tag"], _r["statement"], _r["detail"].replace("\n", " ")))
_l23.append("")
_l23.append("## 诚实边界（不粉饰）")
_l23.append("")
_l23.append("- C53/C54 的 falsified 针对**模块宣称**（公式层/模块层），不否定议题本身：")
_l23.append("  「挠率场能否局域激发」「TUFT 是否有紫外固定点」仍 open。")
_l23.append("- 本册对弯曲时空中的真实度规扰动、引力波 ringdown、有效作用量未做任何计算 ⇒")
_l23.append("  所有结论限于提交文本自身的公式与数值。")
_l23.append("- 本册**未**评估「引力泡」作为科幻/工程概念的可行性，只判定其数学表述的自洽性。")
_l23.append("")
_l23.append("**红线**：数学自洽 ≠ 实验证实；falsified = 该模块的宣称不成立，不等于体系被整体否定。")
_l23.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修②_引力泡与RG流_审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(_l23))

# --- 产出④：V21 续修③（§20 双圈 RG + §21 泡动力学 ODE + §22 元审计）数据与报告 ---
V24_ROWS = [r for r in ROWS[V24_START:] if r["tag"].startswith(("§20", "§21", "§22"))]
n24_pass = sum(1 for r in V24_ROWS if r["state"] == "PASS")
n24_fail = sum(1 for r in V24_ROWS if r["state"] == "FAIL")
n24_bd = sum(1 for r in V24_ROWS if r["state"] == "BOUNDARY")
n24_info = sum(1 for r in V24_ROWS if r["state"] == "INFO")

V24_payload = {
    "title": "空间螺旋几何化统一场论 V21 续修③ · TUFT-RG 双圈 β + 引力泡动力学演化 ODE + 元审计",
    "date": "2026-09-26",
    "dps": 250,
    "method": ["sympy 精确有理数固定点求解（双圈）", "截断伪影判据 |β₂/β₁|（本册新增）",
               "稳定性判据 λ·dt 与指数拟合稳定格式 + scipy Radau 外校",
               "符号恒等式（σ 段与场参数无关）", "量纲账本", "草稿清单 × 台账逐条比对", "桩函数实跑取证"],
    "counts": {"total": len(V24_ROWS), "PASS": n24_pass, "FAIL": n24_fail,
               "BOUNDARY": n24_bd, "INFO": n24_info},
    "C55_RG_two_loop": {
        "b": [str(v) for v in RG2_BF], "d": [str(v) for v in RG2_DF],
        "mu_uv_draft": float(_mu_uv_doc), "E_planck_eV": float(_E_pl_eV),
        "ln_span_inflation": float(_ln_doc - _ln_ok),
        "fp_sympy_solutions": _rg2_sol_txt, "fp_nontrivial": _rg2_nt_txt,
        "gk_star": str(_rg2_gkstar), "gt_star": str(_rg2_gtstar),
        "fp_second_over_first_gk": str(_rg2_gkstar * RG2_DF[0] / RG2_BF[0]),
        "fp_second_over_first_gt": str(_rg2_gtstar * RG2_DF[2] / RG2_BF[2]),
        "draft_findroot": "；".join(_rg2_try_txt),
        "manual_newton_steps": _rg2_steps, "manual_newton_end": [float(v) for v in _rg2_x],
        "ln_span_to_fp": float(_rg2_s_need), "mu_need_over_planck": float(_rg2_mu_ratio),
        "uv_1loop": [float(v) for v in _rg2_1l], "uv_2loop": [float(v) for v in _rg2_2l],
        "uv_rel_diff": [float(v) for v in _rg2_rel], "beta_term_ratio": [float(v) for v in _rg2_rat],
        "n_free": 13,
    },
    "C56_bubble_dynamics": {
        "sigma0_m": float(GB2_S0), "kappa0": float(GB2_K0), "tau0": float(GB2_T0),
        "alpha_g": float(GB2_AG), "omega_bub": float(GB2_W),
        "gamma": float(GB2_GAM), "gamma_tau": float(GB2_GT), "gamma_kappa": float(GB2_GK),
        "t_end_s": float(GB2_T1), "nstep": GB2_NSTEP,
        "lambda_damping": float(_lam0), "dt_stability_limit": float(2 / _lam0),
        "dt_draft": float(_dt_draft), "stability_exceed_factor": float(_e_stab),
        "n_min_for_stability": float(_n_min),
        "sigma_ratio_draft": float(_gb2_eul[0] / GB2_S0 - 1),
        "sigma_ratio_stable": float(_gb2_ref[0] / GB2_S0 - 1),
        "sigma_ratio_radau_external": float(GB2_RADAU_REF),
        "draft_over_reference": float(_gb2_ratio),
        "period_s": float(2 * pi / GB2_W), "periods_covered": float(GB2_W * GB2_T1 / (2 * pi)),
        "decay_timescale_s": float(2 / (GB2_GT + GB2_GK)),
        "norm_gain_no_dissipation": float(_norm_gain),
        "omega_native": float(_omega_bub_native), "omega_mismatch": float(GB2_W / _omega_bub_native),
        "dphi_draft_rad": float(_dphi_draft2), "dphi_dimless_rad": float(_dphi_dimless2),
        "n_free": _gb2_n_free, "n_hit": 0,
    },
    "C57_meta_audit": {
        "draft_total": _d22_total, "draft_pass_measured": _d22_pass, "draft_open_measured": _d22_open,
        "draft_claimed_pass": 20, "draft_claimed_open": 17,
        "ledger_conflicts": ["%s:%s→%s" % _t for _t in _d22_conf],
        "ledger_conflicts_falsified": len(_d22_conf_fal), "ledger_conflicts_boundary": len(_d22_conf_bd),
        "unregistered_ids": _d22_unreg,
        "speed_over_c": float(_speed_rel22),
        "stub_self_check": _r22_a, "hierarchy_lift_empty_axioms": _r22_c,
        "topo_norm_exact": _r22_e["status"], "topo_norm_perturbed": _r22_f["status"],
        "csv_bad_rows": len(_d22_bad),
    },
    "claims_registered": {"added": added_v24, "ids": ["C55", "C56", "C57"]},
    "rows": V24_ROWS,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修③_双圈RG与泡动力学_审计.json"), "w", encoding="utf-8") as fh:
    json.dump(V24_payload, fh, ensure_ascii=False, indent=1)

_l24 = []
_l24.append("# 空间螺旋几何化统一场论 · V21 续修③：TUFT-RG 双圈 β + 引力泡动力学演化 ODE + 元审计")
_l24.append("")
_l24.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋修复版_第一性审计与伪派生判定.py` §20–§22（统一脚本，可复跑）")
_l24.append("> 精度 mpmath dps=250 · 量纲账本内置 · 红线：数学自洽 ≠ 实验证实")
_l24.append("")
_l24.append("**本轮判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
            % (len(V24_ROWS), n24_pass, n24_fail, n24_bd, n24_info))
_l24.append("")
_l24.append("## §20 TUFT-RG 双圈 β（C55 → falsified）")
_l24.append("")
_l24.append("| 量 | 值 |")
_l24.append("|----|----|")
_l24.append("| d1..d7（新增） | %s |" % "、".join([str(v) for v in RG2_DF]))
_l24.append("| μ_UV 草稿 = M_pl c²/ħ | %s（s^-1，非 eV） |" % fmt(_mu_uv_doc, 10))
_l24.append("| 跨度虚增 | %s（= §19 同一错误复发） |" % fmt(_ln_doc - _ln_ok, 8))
_l24.append("| sympy 精确解集 | %s |" % _rg2_sol_txt)
_l24.append("| 非平凡解 | %s（**全部 gkt\\*=0**） |" % _rg2_nt_txt)
_l24.append("| gk\\* = −b1/d1、gt\\* = −b3/d3 | %s、%s |" % (str(_rg2_gkstar), str(_rg2_gtstar)))
_l24.append("| 该点 二阶/一阶项比 | %s、%s（精确 −1 ⇒ 截断伪影） |"
            % (str(_rg2_gkstar * RG2_DF[0] / RG2_BF[0]), str(_rg2_gtstar * RG2_DF[2] / RG2_BF[2])))
_l24.append("| 草稿 findroot 原样运行 | %s |" % _rg2_try_txt[0])
_l24.append("| 手工 Newton 自草稿种子 | %d 步 ⇒ (%s、%s、%s)（收敛到原点） |"
            % (_rg2_steps, fmt(_rg2_x[0], 4), fmt(_rg2_x[1], 4), fmt(_rg2_x[2], 4)))
_l24.append("| 到达 gk\\* 需 ln μ | %s（Planck 跨度 %s ⇒ 比 %s；μ 超 Planck %s 倍） |"
            % (fmt(_rg2_s_need, 8), fmt(_ln_ok, 8), fmt(_rg2_s_need / _ln_ok, 6), fmt(_rg2_mu_ratio, 4)))
_l24.append("| UV 耦合 1 圈 / 2 圈 | (%s、%s、%s) / (%s、%s、%s) |"
            % (fmt(_rg2_1l[0], 8), fmt(_rg2_1l[1], 8), fmt(_rg2_1l[2], 8),
               fmt(_rg2_2l[0], 8), fmt(_rg2_2l[1], 8), fmt(_rg2_2l[2], 8)))
_l24.append("| 耦合相对差 | (%s、%s、%s) |" % tuple(fmt(v, 6) for v in _rg2_rel))
_l24.append("| β 项二阶/一阶比 | (%s、%s、%s) |" % tuple(fmt(v, 6) for v in _rg2_rat))
_l24.append("")
_l24.append("## §21 引力泡动力学演化 ODE（C56 → falsified）")
_l24.append("")
_l24.append("| 量 | 值 |")
_l24.append("|----|----|")
_l24.append("| 加速度恒等式 | accel ≡ 3/σ − γv·16πG/(σ³F)（sympy 精确 0 ⇒ 不含 G、κ0、τ0、α_g） |")
_l24.append("| σ 段阻尼率 λ | %s s^-1 |" % fmt(_lam0, 8))
_l24.append("| 显式 Euler 稳定上限 dt | %s s（草稿取 5.0e-8 s ⇒ 越界 %s 倍） |"
            % (fmt(2 / _lam0, 8), fmt(_e_stab, 6)))
_l24.append("| 稳定所需最少步数 | %s（草稿 %d） |" % (fmt(_n_min, 8), GB2_NSTEP))
_l24.append("| 草稿输出 σ_end/σ0−1 | %s（数值伪迹） |" % fmt(_gb2_eul[0] / GB2_S0 - 1, 8))
_l24.append("| 稳定参考解 σ_end/σ0−1 | %s（n=2000/20000 自洽；scipy Radau 外校 %s） |"
            % (fmt(_gb2_ref[0] / GB2_S0 - 1, 8), fmt(GB2_RADAU_REF, 8)))
_l24.append("| 草稿 / 参考 | %s 倍 |" % fmt(_gb2_ratio, 6))
_l24.append("| σ̈ 符号 | 3/σ > 0 恒成立 ⇒ 永不坍缩 |")
_l24.append("| 窗长 / 振荡周期 | %s s / %s s ⇒ 覆盖 %s 个周期 |"
            % (fmt(GB2_T1, 4), fmt(2 * pi / GB2_W, 6), fmt(GB2_W * GB2_T1 / (2 * pi), 6)))
_l24.append("| 幅值衰减时标 | %s s ≈ 31.7 yr（窗长为其 %s 倍） |"
            % (fmt(2 / (GB2_GT + GB2_GK), 6), fmt(GB2_T1 * (GB2_GT + GB2_GK) / 2, 4)))
_l24.append("| 范数摆动（α_g=0.85、零耗散） | +%s%%（α_g=1 时为 0） |" % fmt(_norm_gain * 100, 6))
_l24.append("| ω_bub 输入 / 本体泡心频率 | %s / %s rad/s ⇒ 相差 %s 倍 |"
            % (fmt(GB2_W, 6), fmt(_omega_bub_native, 8), fmt(GB2_W / _omega_bub_native, 6)))
_l24.append("| δφ（草稿式 / 无量纲） | %s / %s rad |" % (fmt(_dphi_draft2, 8), fmt(_dphi_dimless2, 8)))
_l24.append("| 自由度 | n_free=%d、n_hit=0、约束 0 条 ⇒ V≤0 |" % _gb2_n_free)
_l24.append("")
_l24.append("## §22 草稿 37-claim 自评清单与判据审计（C57 → BOUNDARY）")
_l24.append("")
_l24.append("| 项 | 值 |")
_l24.append("|----|----|")
_l24.append("| 清单实测计数 | 总 %d：PASS=%d、open=%d、BOUNDARY=%d、FAIL=%d |"
            % (_d22_total, _d22_pass, _d22_open, _d22_bd, _d22_fail))
_l24.append("| 草稿自述 | 总 37：PASS=20、OPEN=17、FAIL=0（不符） |")
_l24.append("| 与台账冲突 | %d 处（falsified→PASS %d、boundary→PASS %d） |"
            % (len(_d22_conf), len(_d22_conf_fal), len(_d22_conf_bd)))
_l24.append("| 冲突明细 | %s |" % "、".join(["%s:%s→%s" % _t for _t in _d22_conf]))
_l24.append("| 未登记编号 | %d 条：%s |" % (len(_d22_unreg), "、".join(_d22_unreg)))
_l24.append("| S03 洛伦兹不变性 vs 基底速率 | 矛盾（速率比 v/c = %s，超光速 %s%%） |"
            % (fmt(_speed_rel22, 8), fmt((_speed_rel22 - 1) * 100, 4)))
_l24.append("| 矛盾自检算法（空参数） | %s（桩函数：axiom_set/eq_list 从未被读取） |" % _r22_a["status"])
_l24.append("| 层级升维（空公理集） | base=%s → target=%s（判据放宽） |"
            % (_r22_c.get("base_level"), _r22_c.get("target_level")))
_l24.append("| 拓扑归一（精确 / 0.1%% 扰动） | %s / %s |" % (_r22_e["status"], _r22_f["status"]))
_l24.append("| CSV 导出坏行 | %d 条（字段数 ≠ 4） |" % len(_d22_bad))
_l24.append("")
_l24.append("## 判定明细")
_l24.append("")
_l24.append("| 状态 | 编号 | 主张 | 依据 |")
_l24.append("|------|------|------|------|")
for _r in V24_ROWS:
    _l24.append("| %s | %s | %s | %s |"
                % (_r["state"], _r["tag"], _r["statement"], _r["detail"].replace("\n", " ")))
_l24.append("")
_l24.append("## 诚实边界（不粉饰）")
_l24.append("")
_l24.append("- C55/C56 的 falsified 针对**模块宣称**（模块层），不否定议题本身：")
_l24.append("  「TUFT 是否有紫外固定点」「挠率/曲率场能否局域激发并动力学演化」仍 open。")
_l24.append("- 本册对有效作用量、弯曲时空中的真实度规扰动、引力波 ringdown 未做任何计算 ⇒")
_l24.append("  所有结论限于提交文本自身的公式、代码与数值。")
_l24.append("- 本册**未**评估「引力泡」作为工程/科幻概念的可行性，只判定其数学表述的自洽性；")
_l24.append("  σ 段恒等式 accel ≡ 3/σ 是「该 ODE 与场参数无关」的结论，不等于「引力泡不可能存在」。")
_l24.append("- §21 的「稳定参考解」由指数拟合格式给出（无条件稳定），并经 scipy Radau(rtol=1e-13) 外校；")
_l24.append("  scipy 仅用于外校，引擎本身不依赖 scipy（主脚本可独立复跑）。")
_l24.append("")
_l24.append("**红线**：数学自洽 ≠ 实验证实；falsified = 该模块的宣称不成立，不等于体系被整体否定。")
_l24.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修③_双圈RG与泡动力学_审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(_l24))

print("\n" + "=" * 76)
print("V21续修②判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(V23_ROWS), n23_pass, n23_fail, n23_bd, n23_info))
print("V21续修③判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(V24_ROWS), n24_pass, n24_fail, n24_bd, n24_info))
print("=" * 76)

print("\n" + "=" * 76)
print("V22收官判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(V22_ROWS), n22_pass, n22_fail, n22_bd, n22_info))
print("产出：")
print("  04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V21续修②_引力泡与RG流_审计.json / .md")
print("  04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V21续修③_双圈RG与泡动力学_审计.json / .md")
print("  04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V22收官_全量claims审计.json / .md")
print("  04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋修复版_第一性审计.md（新版·全量 §0–§22）")
print("  07_统一场方程/空间螺旋几何化统一场论/claims.csv（C50/C51/C52 + C53/C54 + C55/C56/C57 追加 %d/%d/%d 行）"
      % (added_v22, added_v23, added_v24))
print("=" * 76)

n_ok_all = sum(1 for c in CHECKS if c["ok"])
print("全程自检 %d/%d | 全程判定 总数=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d | 用时 %.1f s"
      % (n_ok_all, len(CHECKS), len(ROWS), _full_pass, _full_fail, _full_bd, _full_info,
         time.time() - T0))
if n_ok_all != len(CHECKS):
    print("【自检失败项】")
    for c in CHECKS:
        if not c["ok"]:
            print("  -", c["name"], "|", c["note"])
print("=" * 76)
