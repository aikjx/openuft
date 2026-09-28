# -*- coding: utf-8 -*-
"""MainAgent: append T09 line1 Gate-A-FAIL result to master ledger (append-only)."""
import os, shutil

p = 'TUFT_企业级归一化主册_v1.0.md'
shutil.copy(p, 'TUFT_企业级归一化主册_v1.0.md.bak_t09l1')
note = '''

---

## T09 线一 · validated 高阶 Frobenius peel MainAgent 审计（2026-09-27）

<!-- ma-audit-t09-line1 -->

**独立推导验算闭合**（Read 全文 → 重推）：
- 代入 psi=s^{-BETA}F 后离心项 BETA(BETA+1)-2BETA²+BETA(BETA-1)=0 精确抵消、jw 交叉项 ±2jwBETA/s 抵消 → F''+2jwF'-VF=0
- Frobenius 系数：f1=3j/w（O(s^-2)）、f2=-3/w²-15j/(2w)（O(s^-3)，V=6/ρ²-30/ρ³ 含 e^{-4/ρ} 因子）
- 端点 Robin 比 F'_z/F=3/(2jwb)=-3j/(2wb) 与 f1/(2b) 自洽
- 收敛论证：psi~(1-z)^{1.2638} 分数幂 → 代数收敛 N^{-β}（T08 平台 3.89/4.72/4.81e-9 理论根源）；F 在 z=1 解析 → 几何收敛

**Gate A 实测（组织者 out）**：F-pencil |err| N=60 1.421e-07 → N=90 4.191e-08 → N=120 1.830e-08 → N=180 7.339e-09 → N=240 5.475e-09；best interconsistency 2.882e-09、best anchor 5.475e-09，均 >1e-9 → **GATE A FAIL** → 按硬顺序 STOP、Gate B n=1,2 维持 OPEN、无伪闭合。

**瓶颈精确定位（预判修正）**：F-pencil **几何收敛**（每 N 改善 2.3-3.4×，视界端 (1+z)^{-2/3} 弱奇异未成主导——Cheb-Gauss 无端点网格容忍强于 Boyd 保守估计）；但 N=180→240 骤降至 1.34×，撞 **~5e-9 数值噪声地板**——与 psi-pencil 平台同一地板 → 瓶颈是 **rho ODE 积分（rtol=1e-13）+ Beyn LU/快照噪声**，非 peel 解析化程度。修复优先级：**提高 ODE 精度（rtol=1e-14/atol=1e-17）+ nc 增密**，双边 peel 退居次席。

四态：A 严格（GR Leaver 参考）/ B 条件（n=0 停在 ~5e-9 平台，Gate A 未过）/ C 定义（Beyn 隔离极点有理近似）/ D 开放（泛音谱，硬顺序未达）。

中间诊断：`TUFT_T09_中间诊断_线一Fpeel收敛异常_2026-09-27.md`（含预判修正）。台账 main_agent_v60_t09_line1_rerun。E1-E498 冻结不变。
'''
with open(p, 'a', encoding='utf-8') as f:
    f.write(note)
print('appended; new size', os.path.getsize(p))
