# ROOT V122 来源审计（截至 2026-11-21）

以下为公开资料及其适用范围。未从任何文献抓取或拟合原始卫星观测时序；不把模型图表、示例值或仪器精度冒充独立观测上界。

1. Bergé 等，*Interpretation of geodesy experiments in non-Newtonian theories of gravity* (2018): https://arxiv.org/abs/1808.00340 。正文讨论地球密度/形状误差与第五力参数的混合估计，示例 λ=1.2×10⁵ m、α=2×10⁻⁸（其示例不能不经论证地解释为正式统一上限）；第五力和大地测量联合建模是必要的。
2. *Constraining f(R) gravity with a space-borne superconducting gradiometer via precision measurement of the planetary gravitomagnetic field*, Chinese Physics C, 2026：https://cpc.ihep.ac.cn/article/doi/10.1088/1674-1137/ae8ce5 。正文有 f(R) 的作用量、迹方程及 m_s²=1/(6α)；注意文献以 α 表示二次曲率系数，别与本文 α_Y 混淆。
3. Chen 等，*Determination of Earth's Static Gravity Field Using Quantum Gravity Satellites at Very Low Earth Orbit*, Earth and Space Science (2026-09-29): https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026EA005368 。关于 GOCE/GRACE、低轨梯度仪和光钟的研究，包含理想化仿真，**不能直接作为 ROOT 的排除统计**。
4. Scholarpedia，*F(R) theories of gravitation*: https://www.scholarpedia.org/article/F%28R%29_theories_of_gravitation 。f(R) 理论、标量模与弱场背景。
5. Berry & Gair, *Linearized f(R) Gravity: Gravitational Radiation & Solar System Tests* (2011), https://arxiv.org/abs/1104.0819 。关于线性引力与光学限制的文献；注意不同光源结构和 PPN 定义有条件限制。
6. MICROSCOPE composition-dependent fifth-force references: https://arxiv.org/abs/1712.00483 。主要针对组成荷量相关耦合；不能直接把该界限当作普适 $f(R)$ 的 α_Y 的上界。
7. LAGEOS laser-ranging discussion：https://link.springer.com/article/10.1007/s12210-025-01395-5 。主要针对地球半径量级与更长作用程，不能简单替代短 124.6 km 的低轨检验。

**出处限定**：本版本的地球形状系数和相关数值例子来自随包包含的 V120/V121 代码与预定义假设，不代表它们已在本轮独立复核外部文献每个积分公式。仅在球外和线性近似下使用相应表达式。
