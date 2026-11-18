# ROOT V73 文献与实验来源 / 来源状态

以下数据来源用于核验**已知理论与观测**。网址在研究时检索过；本 ZIP 不将外部网页内容复制为本研究原创成果。网页可能变化，使用时应以发布机构最新版本为准。

1. **PDG 2026 — Grand Unified Theories**，https://ccwww.kek.jp/pdg/2026/reviews/rpp2026-rev-guts.pdf 。该综述说明标准模型规范群、三代粒子谱的已知条件、GUT 中的规范嵌入及实验约束。此处引用的内容是已有物理学，并非 ROOT 新定理。
2. **NIST / CODATA 2022 物理常数**，https://physics.nist.gov/cuu/pdf/all.pdf 。`G=6.67430(15)×10^-11 m^3 kg^-1 s^-2`；代码仅用作外部实验参考。
3. **MICROSCOPE Final Results, 2022**，https://doi.org/10.1103/PhysRevLett.129.121102 。Ti/Pt 实测 `η=[−1.5±2.3stat±1.5syst]×10^-15`；本项目只对人为代理源荷模型计算示意条件界限，不能替代原论文的完整似然与系统分析。
4. **Weinberg, Witten (1980), Limits on massless particles**，https://doi.org/10.1016/0370-2693(80)90212-9 。用于检查平直时空局域理论复合无质量自旋 2 的条件限制；不等同对所有涌现引力机制的一般否定。
5. **QCD 讲义：Dimensionful scale from RG**，https://cds.cern.ch/record/836684/files/cern-2010-001p97.pdf 。量纲嬗变属于已有 QFT；本项目做数值敏感性分析而非声称原创发现 RG。

## 数据与软件证据标签

- `observational_published`：来源明确的公开实验报告或常数，代码不得改写为理论预测。
- `derived_conditionally`：在明确数学公设与近似下证明的公式；不能不经检查外推到自然界。
- `synthetic`：本项目人为设置参数及噪声得到的数值，没有任何实际实验测量。
- `hypothetical`：未获实测支持的候选场、耦合和新作用。

**禁止把 synthetic 或 hypothetical 重新标注为 observational_published。**
