# TUFT / H-TUFT 卷系归一化总览（自动生成）

> 由 `tuft_卷系_归一化总览.py` 生成（可复跑）。覆盖**卷系**（卷十九~卷三十 + 补充卷A/B/C/D/E/F/G/H/I）：
> R 系 `*_report.txt` 的归一化见 `tuft_跨册缺陷族检查.py` / `tuft_判据门禁.py`（本工具不重复）。
> 红线：数学自洽 != 实验证实。本表只做归一化与完整性审计，不改动真源。

## 一、CURATED 索引（CUR-01 ~ CUR-21）

| entry | 卷 | 名称 | script_ref | 落盘/哈希 | 状态(grade) | 层级 |
|---|---|---|---|---|---|---|
| CUR-01 | 19 | TUFT 电子 EDM 挠率诱导 | `tuft_EDM_实验对接_OPEN6.py` | MATCH | ❌ 已排除 (C) | L3 |
| CUR-02 | 19 | TUFT 电子反常磁矩 g-2 | `tuft_g2_电子反常磁矩_OPEN5.py` | MATCH | ❌ 已排除 (C) | L3 |
| CUR-03 | 19 | Ringdown 挠率可检验性 | `tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py` | MATCH | ❌ 窗口已关闭（临界） (C) | L3 |
| CUR-04 | 19 | β-running 缺口定理实例化 | `tuft_beta_running_缺口_定理N实例化.py` | MATCH | ✅ 自洽（[B] 级，非实验证实） (O) | L1 |
| CUR-05 | 21 | TUFT 挠率诱导费米子代际与味混合（提案） | `tuft_flavor_ckm_pmns_OPEN_v1.py` | MATCH | ⏳ 待检验（假设） (O) | L2 |
| CUR-06 | 22 | TUFT 挠率驱动暴胀与 CMB 原初扰动（提案） | `tuft_cmb_inflation_bmode_OPEN_v1.py` | MATCH | ⏳ 待检验（假设） (O) | L2 |
| CUR-07 | 23 | TUFT 全局 MCMC 贝叶斯联合推断（主线，19 维参数，8 通道） | `tuft_global_mcmc_nested_OPEN_v1.py` | MATCH | ❌ 已触发（8 通道联合 Z=0 严格 ⇒ 主线 TUFT 被微观窗口排除；CMB-on (C) | L2 |
| CUR-08 | 24 | TUFT 挠率正则黑洞与普朗克核心、黑洞信息守恒（假设/解读） | `tuft_blackhole_torsion_core_OPEN_v1.py` | MATCH | ⏳ 待检验（假设，经验支柱已关闭） (O) | L2 |
| CUR-09 | 25 | 螺旋挠率丛统一场论 H-TUFT | `tuft_helical_bundle_H_v1.py` | MATCH | ⏳ 待检验（框架升维，低能投影继承已关窗口） (O) | L1 |
| CUR-10 | 26 | H-TUFT 丛路径积分与螺旋孤子拓扑散射 S 矩阵 | `tuft_htuft_scatter_amplitude_v1.py` | MATCH | ⏳ 待检验（脚手架已落盘；参数未锚定） (O) | L1 |
| CUR-11 | 27 | H-TUFT 螺旋宇宙弦与原初拓扑孤子、SGWB 与 CMB 手征非高斯 | `tuft_htuft_cosmic_string_v1.py` | MATCH | ⏳ 待检验（结构性待检验；预言未锚定、手征机制缺失） (O) | L2 |
| CUR-12 | 28 | H-TUFT 螺旋拓扑孤子：标准模型粒子谱系、三代味、CKM/PMNS 拓扑起源 | `tuft_htuft_particle_spectrum_v1.py` | MATCH | ⏳ 待检验（结构性风险最高；定量预言实跑失败） (O) | L2 |
| CUR-13 | 30 | H-TUFT 全局 MCMC 与嵌套采样跨尺度联合贝叶斯推断（复用型扩展） | `tuft_htuft_global_mcmc_v1.py` | MATCH | ❌ 已触发（正式排除；扩展通道 UNVALIDATED） (C) | L2 |
| CUR-14 | 补充卷A | H-TUFT 高螺旋拓扑荷孤子暗物质：遗迹丰度与直接探测截面 | `tuft_htuft_darkmatter_soliton_v1.py` | MATCH | ❌ 核心宣称失败（Omega_DM 实跑差 ~25 量级、量纲反）；DM 通道本身未排除 (C) | L2 |
| CUR-15 | 补充卷B | H-TUFT 真空拓扑能与宇宙学常数（从丛欧拉示性数推导 Lambda） | `tuft_htuft_vacuum_topology_lambda_v1.py` | MATCH | ❌ 核心宣称失败（Omega_Lambda 实跑 3.62e101 != 0.6889， (C) | L2 |
| CUR-16 | 补充卷D | H-TUFT 黑洞『拓扑毛发』Q_hel 与黑洞拓扑荷守恒（真增量条目；黑洞主体结构不重复登记） | `tuft_htuft_blackhole_topology_v1.py` | MATCH | ⏳ 待检验（**无可证伪力**：全局荷外部不可读 + α/Q_hel 双自由；草稿引擎已 (O) | L2 |
| CUR-17 | 补充卷E | H-TUFT 量子拓扑涨落：多扇区路径积分求和、拓扑隧穿、量子孤子 WKB 与 chi2_quantum（真增量条目；量子化框架不重复登记） | `tuft_htuft_quantum_bundle_pathint_v1.py` | MATCH | ❌ 核心宣称失败（多扇区求和未定义/自我取消；ħ 阶修正比 (m_e/M_Pl)² 大  (C) | L1 |
| CUR-18 | 补充卷F | H-TUFT 味物理：CKM 矩阵与三代费米子拓扑起源（隧穿深化） | `tuft_htuft_flavor_ckm_topology_v1.py` | MATCH | ❌ 核心宣称失败（CP 破坏未生成 J=0；|V_ub| 差 26.25×；质量层级失败 (C) | L2 |
| CUR-19 | 补充卷G | H-TUFT 拓扑相变原初引力波与手征极化、CMB B 模印记（相变源深化；手征引力波主结构不重复登记，见 CUR-11） | `tuft_htuft_primordial_gw_topophase_v1.py` | MATCH | ⏳ 待检验（结构性待检验；手征机制缺失 + σ_wall 量纲差 1 能量量纲 + 输出 (O) | L2 |
| CUR-20 | 补充卷H | H-TUFT 规范相互作用的拓扑生成（丛局部缠绕 → SU(3)xSU(2)xU(1)；划界专卷） | `tuft_htuft_gauge_topology_v1.py` | MATCH | ❌ 核心宣称失败（结构性：「自然导出 SM 规范群」不成立——同伦签名非唯一选出 ≥3~ (C) | L2 |
| CUR-21 | 补充卷I | H-TUFT 拓扑缺陷的 BBN 约束（首次实算；畴壁张力量化上限） | `tuft_htuft_bbn_topology_v1.py` | MATCH | ❌ 核心宣称失败（『BBN 自动满足』未证；畴壁分支下 sigma_wall 需 ≲(8 (C) | L2 |

## 二、完整性审计

- 条目总数：**21**；编号范围 CUR-01 ~ CUR-21
- **缺号**：无 ✅
- **重号**：无 ✅
- **哈希漂移**：无 ✅
- **脚本未落盘**：无 ✅
- **反回退守卫**：全部 ❌ 条目保持 ❌ ✅

## 三、归一化评级（H 可信地基 / O 欠定诚实边界 / C 缺陷冲突 / U 未展开）

| 等级 | 条目数 |
|---|---|
| H | 0 |
| O | 10 |
| C | 11 |
| U | 0 |

层级分布：L0=0 · L1=4 · L2=14 · L3=3

> **归一化结论**：`H=0`——卷系**无一条达到可信地基**；`C=11`（已排除/已关闭/核心失败）；
> `O=10`（待检验/自洽无预言）；`U=0`（缺号未固化）。

## 四、问题清单

无不一致项 ✅

