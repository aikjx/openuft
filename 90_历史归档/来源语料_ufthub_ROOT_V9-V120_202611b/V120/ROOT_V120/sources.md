# 公开文献与资料索引（2026-11-20 核对）

## 1. 地球 Yukawa 形状因子：使用了文章的明确公式

Pierre Fayet, “Hyperbolic form factors for Yukawa interactions, and applications to the Earth,” *European Physical Journal C* **86**, 1125 (2026). DOI: 10.1140/epjc/s10052-026-15933-4

https://link.springer.com/article/10.1140/epjc/s10052-026-15933-4

- 本包使用该文 Eq.(16) 的解析地球模型 `Phi'(x)`；文章称它对五层球模型的近似在 x≤64 时误差至多约 0.7%。
- 文献主要涉及具有不同源/探针耦合的有限范围新力、MICROSCOPE 约束。**不能**把文中对 B、B-L 等物质荷耦合的限制简单当作普适纯引力标量的 alpha=1/3 上界。

## 2. f(R) 线性势：现成的 alpha=1/3 与 lambda=sqrt(6a)

“Screened scalar hair and the weak-lensing separation of black holes from neutron stars in quadratic f(R) gravity,” *European Physical Journal C* (2026).

https://link.springer.com/article/10.1140/epjc/s10052-026-16565-4

- 参照文章的弱场势 Eq.(4)：`Phi=-GM/r*(1+exp(-r/lambda)/3)`, `Psi=-GM/r*(1-exp(-r/lambda)/3)`，以及 `lambda=sqrt(6 alpha)`（文中 alpha 是曲率系数，不应与本包 alpha_Y 混淆）。
- 该文指出领先阶透镜势标量修正抵消；不能把轨道加速度异常照搬为光偏折增强。

## 3. GOCE、GRACE/GRACE-FO 任务背景

ESA GOCE instruments: https://www.esa.int/Applications/Observing_the_Earth/FutureEO/GOCE/Instruments

GOCE gravity gradients versus global gravity field models, *Geophysical Journal International* 189 (2012): https://academic.oup.com/gji/article/189/2/846/2088935

NASA JPL GRACE-FO Mission Overview: https://www.jpl.nasa.gov/news/press_kits/grace-fo/mission/

Ghobadi-Far et al., “GRACE Follow-On Laser Ranging Interferometer Measurements Uniquely Distinguish Short-Wavelength Gravitational Perturbations,” *Geophysical Research Letters* (2020), https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL089445

- 这些来源用来确认可用的卫星测量通道、轨道高度、误差处理的复杂性；**未作为本包的原始观测数据**。

## 4. Yukawa 约束与普适耦合的区分

“The local dark sector” (2021), Earth-satellite fifth-force constraints survey: https://doi.org/10.1007/s10686-021-09734-8

Pierre Fayet, “The Yukawa potential of a non-homogeneous sphere, with new limits on an ultralight boson” (2025): https://arxiv.org/abs/2507.02723

- MICROSCOPE 的组分差分 WEP 约束通常不能原封不动应用于完全普适的 f(R) 标量耦合，必须区分理论和荷的定义。

## 5. 原创性边界

指数多项式、Prony、重根广义指数以及 Hankel 子式的这些恒等式属于经典数值代数和信号重建框架。本包的五点专用消元公式与 ROOT 场模型检查属于应用层面的推导，不主张对 Prony 数学的优先权。
