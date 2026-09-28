# -*- coding: utf-8 -*-
"""MainAgent: append T10 three-line audit to master ledger (append-only)."""
import os, shutil

p = 'TUFT_归一化主册_v1.0.md'
shutil.copy(p, 'TUFT_归一化主册_v1.0.md.bak_t10')
note = '''

---

## T10 三线 · 锚点升级 + Gate A 新锚重判 + validated peel 应用泛音 + 外向 WKB/Leaver 打靶 MainAgent 审计（2026-09-27）

<!-- ma-audit-t10-lines123 -->

**本机复跑审计**（`_ma_t10_audit.py`，import 官方模块最小子集）：线一 N=180 |dw|=4.285e-13、线二 N=300 |dw|=9.616e-14、线三 n=0 |dw|=2.605e-13——**三线数值全部逐位复现**。

### 线一 · 锚点升级（VERIFIED + 外推代数独立复核）

- 外推数学手算复核：w_inf = w360 + d3/(1−r_b) = 0.434445176207−0.056449764437i ✓；err_bar=√(1.040e-10²+1.913e-10²)=2.177e-10 ✓；r_a=0.3509、r_b=0.4369（近实正、|r|<1=真几何收敛）
- **新锚正式冻结：w_TUFT(n=0) = 0.434445176207 − 0.056449764436i，置信半径 2.178e-10**
- Gate A 新锚重判：(i) N 互合 4.419e-10 PASS (ii) |w−新锚| 7.849e-10 PASS → **PASS**
- 旧锚偏置揭示 4.785e-9（旧 0.434445178−0.056449760i = 旧 psi 平台）；升级史 T08→T09→T10 记录在案；仍为 (B) 条件定理（数值钉定非解析闭式）

### 线二 · validated peel 应用泛音（数值 VERIFIED；n=1 跨管线不一致——审计新增发现）

- Gate A 复现 PASS（ic=4.420e-10、|err|=3.292e-12 @N=360）
- n=1：frob 铅笔单管线几何收敛（3.30e-8→6.30e-9→3.18e-9，pole-switch=False），best ic=3.18e-9 未达 1e-9
- **MA-AUDIT 跨管线发现**：T10 frob n=1 (N=300) = 0.569956890813−0.287671183832i vs **T09 管线 n=1 = 0.569957939619−0.287655030300i**，|dw|~1.6e-2——单管线自洽不足以钉定 n=1，**两个竞争候选并存，n=1 未定位**（组织者汇总未显式报告此差异，本审计补记）
- n=2：staged ic=1.056e-03（极点跨 N 跳变）；SVD rescue N=240/300/360 各 rank=1 单极但位置漂移（0.4666/0.4799/0.5059−0.42i），tol=0.015 无稳定链 → **NOT LOCALIZED**
- **Gate B n=1,2 维持 OPEN**；残余=pole-doublet/泄漏极限，非 peel 本身（peel 在 n=0 上 Gate-A 已证）

### 线三 · 外向 WKB/Leaver 打靶（数值 VERIFIED + 方法推导正确；实轮廓 FAIL——结构性）

- 方法推导复核闭合：剥离 F''+2iwF'−V F=0 → F=exp(−iws)G → tortoise Schrödinger；壁端正则支 λ₊=(1+√(1+4C))/2；Smatch 纯出射 BC；外向方向稳定（反向测试被拒）——推导正确
- n=0 自检 FAIL：打靶根 0.411848556867+0.039242326370i **虚部为正（增长模）**，|vs 锚点|=9.832e-02，Smatch40/60 互合 2.737e-02
- n=1 Newton 发散至 3.37+4.27i（25 步 |R|=1.6e-3）；n=2 发散至 0.62+4.58i
- 归因（结构性，非实现 bug）：谱极点活在复轮廓 b=3.5+1.5i 上，实轴 IVP 采样的是另一 BVP；解析轮廓不变性在出射/增长通道切换的 Stokes 线处失效——与 T09 n=1 pole-switch、n=2 SVD 漂移同源
- 修复需在同一复轮廓上做复 ρ 积分，超出本双精度线范围；Gate B 维持 OPEN

### T10 判别增量

| 项 | 状态 |
|---|---|
| 新锚冻结 0.434445176207−0.056449764436i（conf 2.2e-10） | 严格定理（数值）+ 条件定理（物理） |
| Gate A 新锚重判 PASS | 严格定理 |
| n=1 单管线几何收敛 ic=3.18e-9（跨管线不一致 ~1e-2） | 条件定理/开放 |
| n=2 SVD 未定位 | 开放命题 |
| 实轮廓 BVP vs 复轮廓谱极点（Stokes 线） | 开放命题（结构性） |

台账 main_agent_v60_t10_line1/2/3_rerun。latest_round=v6.0_T10_anchor_upgraded_gateB_open_stokes_line。E1-E498 冻结不变。
'''
with open(p, 'a', encoding='utf-8') as f:
    f.write(note)
print('appended; new size', os.path.getsize(p))
