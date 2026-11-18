# ROOT V71 文献与数值来源追溯

本研究主要参考以下可公开访问的权威资料；凡新力都按**假设性有效相互作用**处理。

1. **Particle Data Group, Review of Particle Physics 2026**，https://pdg.lbl.gov/ 和 https://pdg.lbl.gov/2026/reviews/searches-and-hypothetical-particles.html ，正式刊载 Int. J. Mod. Phys. A 41, 2630011 (2026)。用于核查规范群、粒子表象和新物理约束；并不提供 ROOT 理论的证明。
2. **NIST CODATA 2022 fundamental constants**，https://physics.nist.gov/cuu/Constants/ 。其中 G 的推荐值为 `6.67430(15)×10⁻¹¹ m³ kg⁻¹ s⁻²`；本包取中心值为**已知输入**。
3. **Touboul et al., MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle**, Phys. Rev. Lett. 129, 121102 (2022)，https://doi.org/10.1103/PhysRevLett.129.121102 。Ti/Pt 零结果的 Eötvös 参数与系统误差说明是外部约束，不能简单当作所有新力参数的统一阈值。
4. **Pierre Fayet, Hyperbolic form factors for Yukawa interactions, and applications to the Earth**, European Physical Journal C 86 (2026), https://doi.org/10.1140/epjc/s10052-026-15933-4 ，发表 2026-09-28；开放文章 https://link.springer.com/article/10.1140/epjc/s10052-026-15933-4 。提供球形非点源 Yukawa 形状因子；**本包没有原创发现该因子**，只是补齐自身先前简化模型并数值验证。
5. **Schlamminger & Rothleitner, Measurements of the Newtonian Constant of Gravitation G**, https://www.nist.gov/publications/measurements-newtonian-constant-gravitation-g ，Review of Scientific Instruments (2017)。不同实验测 G 的系统误差与测量手段。
6. **Eöt-Wash Group, What is a Torsion Balance?**，https://www.npl.washington.edu/eotwash/torsion-balances 。基于不同物质组分的扭秤实验背景。
7. **Kostelecký and Vargas, Lorentz and CPT tests with clock-comparison experiments**, PRD 98, 036003 (2018)，https://doi.org/10.1103/PhysRevD.98.036003 。用钟比较约束可能的 Lorentz 优选方向场及恒星日、周年信号。
8. **LIGO/Virgo GW170817 factsheet**，https://dcc.ligo.org/public/0146/G1702000/006/GW170817_Factsheet.pdf 。只用于标明双信使传播速率是一项关键约束；本轮未独立分析该 PDF 的页图或事件原始数据。
9. **前版 ROOT V70**，本地 `archive/ROOT_V70_前版研究包.zip`，用于模型连续性；其中全部合成源荷/材料荷仍非实测。

## 来源与可复现说明

- `rootv71/physics.py` 的行星 GM、半径取前版较圆整数值；不是实时高阶重力球谐或高精星历。
- `data/` 中的曲线均由本地公式生成，没有任何被伪装成真实测量值的外部观测记录。
- 公式中的 `α=1` 仅用于演示“在相同假设强度下有限球与点源的几何差别”，不意味着该值符合当前实验上限。
- 2026 Fayet 形状因子对应线性、各向同性、无屏蔽的 Yukawa 型相互作用；不能自动推广到所有屏蔽标量/张量理论或任意自旋相关力。
- 若要给出新力强度置信区间，应使用真正实验源体的有限几何、材质层、响应卷积和噪声协方差，并预先固定统计检验方法。
