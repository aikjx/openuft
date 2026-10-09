# TUFT V3.5 · 新体系 PGT 谱分析与观测兼容性评估（机器产物）

- 生成时间：2026-10-07
- 条目 14 ｜ PASS 3 ｜ FAIL 4 ｜ BOUNDARY 7 ｜ 自检 7 / 7
- **结论：谱稳定性非自动**——须选 ghost-free 参数区；EC 传播挠率模式被观测排除；谱兼容与预言可测两难（与 β 两难同构）
- **E2 修正：无 Ostrogradsky ≠ 无 ghost/tachyon**

## PGT 谱分析文献结论

| 来源 | 结论 | 判定 |
|---|---|---|
| arXiv 0905.1068 | 2⁻ 分量无 tachyon 需 γ>0、无 ghost 需 γ<0 ⇒ 必然含其一，除非 γ=0 | FAIL |
| arXiv 1910.07506 | quadratic PGT 轴向扇区 ghostly；ghost-free 一般⇒挠率非动力学 | FAIL |
| arXiv 1812.02675 | 系统性方法找到 ghost/tachyon-free 参数区（4 例） | PASS |
| arXiv 1411.5613 | pole=mass 须正(tachyon)、residue 符号(ghost) 判据 | 判据 |

## 观测兼容性

- **EC 传播挠率模式被观测排除**（cdnsciencepub 2025，Ψ2/Ψ3/Ψ4 null test，Bayes>10^20~10^26）；
- m_τ 分层：低 m_τ 被 EC 排除；高 m_τ(>TeV) 安全但预言被 1/m_τ² 压到不可测；
- **谱兼容(高 m_τ 安全)与预言可测(低 m_τ)两难**——与 β 通道两难同构。

## 条目

| ID | 节 | 条目 | 判定 | 摘要 |
|---|---|---|---|---|
| A-01 | 谱分析 | 挠率自由度分解 | BOUNDARY | 传播挠率 T 按 parity 分解为 2⁻(张量)/1⁻(矢量)/0⁻(标量) 分量；传播子 pole=mass、residue 符号决定 ghost（回链 1411.5613 判据） |
| A-02 | 谱分析 | 特定 2⁻ 分量模型 ghost/tachyon 两难 | FAIL | arXiv 0905.1068：2⁻ 分量无 tachyon 需 γ>0、无 ghost 需 γ<0 ⇒ 同分量无法同时避免，除非 γ=0——模型必然含 ghost 或 tachyon 其一 |
| A-03 | 谱分析 | quadratic PGT 轴向扇区 ghostly | FAIL | arXiv 1910.07506：轴向扇区与引力子扇区 ghostly 耦合致不稳定；ghost-free 一般 ⇒ 挠率非动力学 |
| A-04 | 谱分析 | 存在 ghost/tachyon-free 参数区 | PASS | arXiv 1812.02675：系统性方法确定无 ghost/tachyon 的参数区（含临界额外规范不变），找到 4 例——存在性成立 |
| A-05 | 谱分析 | 谱稳定性判定 | BOUNDARY | 谱稳定性**非自动**：须严格选择 ghost-free 参数区（1812.02675 存在性，但 0905.1068/1910.07506 表明大量模型必然有 ghost/tachyon）；ESCAPE-AUDIT E2「无 Ostrogradsky」远不足以排 ghost/tachyon |
| B-01 | 观测兼容 | EC 传播挠率模式被观测排除 | FAIL | cdnsciencepub 2025(USMEG-EFT)：EC 传播挠率模式被引力波形/偏振观测排除（Ψ2,Ψ3,Ψ4 null test，Bayes 因子 >10^20~10^26） |
| B-02 | 观测兼容 | m_τ 能标分层 | BOUNDARY | 低 m_τ（可测能标）→ 传播挠率模式被 EC 观测排除（B-01）；高 m_τ（>TeV）→ 传播模式低能不可见、不冲突 |
| B-03 | 观测兼容 | 与可证伪预言草案衔接 | BOUNDARY | 草案预测低能四费米子修正依赖 m_τ：高 m_τ(>TeV) 安全但修正被 1/m_τ² 压到不可测；低 m_τ 可测但被 EC 观测排除——**谱兼容与预言可测呈两难**（与 β 通道两难同构） |
| C-01 | 综合 | 谱稳定性需参数区选择 | BOUNDARY | 新体系须在立项时选 ghost-free 参数区（1812.02675 存在性作为可行依据）；否则重蹈 0905.1068/1910.07506 的 ghost/tachyon |
| C-02 | 综合 | 观测兼容 vs 预言可测两难 | FAIL | 传播挠率的低能可测窗口被 EC 观测排除，高能安全窗口则预言不可测——与 β 通道两难同构，新体系传播挠率预言面临同构困境 |
| C-03 | 综合 | 新体系可行性再评估 | BOUNDARY | 谱分析给新体系双重压力（ghost 需参数区 + EC 观测排除/不可测张力）；但**不终结**新体系——选高 m_τ ghost-free 参数区仍构成可行窗口（代价：预言不可测，回到解释性模型） |
| D-01 | 诚实 | E2 修正 | PASS | 无 Ostrogradsky（一阶导数，E2）≠ 无 ghost/tachyon（动能项规范结构层面）；ESCAPE-AUDIT 已诚实标注 NOT-ASSESSED，本册补判为「非自动、需参数区选择」 |
| D-02 | 诚实 | 新体系立项纳入谱前置 | BOUNDARY | 新体系立项前置清单③结论：须 ①选 ghost-free 参数区 ②权衡 m_τ 能标（低被 EC 排除/高不可测）——谱分析是立项的硬前置，非可选项 |
| D-03 | 诚实 | 本册定位 | PASS | 本册为前置③谱分析评估，不终结新体系（高 m_τ ghost-free 参数区仍可行）；但显著收窄可行窗口，并揭示与 β 两难同构的传播挠率困境 |

## 自检

| 基线 | 结果 | 取证 |
|---|---|---|
| ghost_tachyon_dilemma | PASS | 2⁻ 分量 ghost/tachyon 两难已登记（回链 0905.1068） |
| ghostfree_exists | PASS | ghost-free 参数区存在性已登记（回链 1812.02675） |
| ec_excluded | PASS | EC 传播挠率模式观测排除已登记（回链 cdnsciencepub 2025） |
| not_automatic | PASS | 谱稳定性非自动已判定 |
| e2_corrected | PASS | E2 修正（无Ostrogradsky≠无ghost/tachyon）已登记 |
| analogous_dilemma | PASS | 传播挠率谱兼容vs预言可测两难已登记 |
| window_remains | PASS | 高 m_τ ghost-free 参数区仍可行已登记 |

## 诚实边界与衔接

1. 谱分析结论基于公开 PGT 文献（0905.1068/1910.07506/1812.02675/1411.5613）；不同 PGT 模型谱不同，本册给出文献级的条件判据而非逐个模型计算；
2. EC 传播挠率观测排除（cdnsciencepub 2025）为低能引力波形/偏振 null test；高 m_τ 时传播模式低能不可见，不冲突；
3. **E2 修正**：无 Ostrogradsky（一阶导数）≠ 无 ghost/tachyon（动能项规范结构）；ESCAPE-AUDIT NOT-ASSESSED 诚实标注保留，本册补判；
4. 新体系**不终结**但窗口显著收窄：高 m_τ ghost-free 参数区仍可行，代价是预言不可测（回到解释性模型，F-02 不满足）；
5. 红线：数学自洽 ≠ 物理真实；评级 C/L1 维持。