# ROOT V123 文献与数据源审计（截至 2026-11-21）

本文只引用公开资源背景和可复现的公开数据入口，不声称已经下载或处理这些卫星观测。

1. **Pierre Fayet (2026-09-28)**, *Hyperbolic form factors for Yukawa interactions, and applications to the Earth*, EPJC 86, 1125, DOI:10.1140/epjc/s10052-026-15933-4, https://link.springer.com/article/10.1140/epjc/s10052-026-15933-4 。支持球对称源的双曲形状因子和近似地球密度模型。注意文中 B、B-L 耦合的 MICROSCOPE 限制是成分相关情形，不能无条件套到普适耦合的 f(R) 标量。
2. **Bergé, Brax, Pernot-Borràs & Uzan (2018)**, *Interpretation of geodesy experiments in non-Newtonian theories of gravity*, https://arxiv.org/abs/1808.00340 。强烈提示非球形引力场、多极系数、测地反演与修改引力间的退化。
3. **2026 EPJC**, *Post-Newtonian N-body dynamics in Extended Theories of Gravity*, https://link.springer.com/article/10.1140/epjc/s10052-026-16139-4 。用于核对标量弱场和 PPN 背景，不把其中关于有屏蔽机制的模型自动赋给固定二次 R² 模型。
4. **GFZ/ICGEM**, *GOCO06s satellite-only global gravity field model*, https://dataservices.gfz-potsdam.de/icgem/showshort.php?id=escidoc%3A4081892 ，及 https://icgem.gfz.de/tom 。用于背景地球重力场数据模型、模型元数据和版本。
5. **ESA GOCE**, https://www.esa.int/Applications/Observing_the_Earth/FutureEO/GOCE/Introducing_GOCE 。用于低轨重力梯度科学任务背景。
6. **NASA/JPL GRACE-FO**, https://www.jpl.nasa.gov/missions/gravity-recovery-and-climate-experiment-follow-on-grace-fo/ ；**NASA GRACE-FO Level-1B** https://data.nasa.gov/dataset/grace-fo-level-1b-release-version-4-0-from-jpl-in-ascii-5f885 ；NASA Level-1 文档 https://podaac.jpl.nasa.gov/gravity/gracefo-documentation 。供后续真实数据处理。
7. **CERN 5D fermions / chirality background**, https://e-publishing.cern.ch/index.php/CYR/article/download/187/131/509 。说明 5D 单一几何的手征零模需要独立边界/投影设计，不能由五维零动量壳直接得到标准模型手征谱。

## 外部证据边界

- 以上链接标记为“已检索公开文献/资源”，**不是**“已用卫星真实测距数据拟合”。
- 数值报告全部标记 `SYNTHETIC`。即便 GOCO06s 引用一个 `GM`，它也是反演模型内参考值，不能充当独立的未建模 Yukawa 第五力证据。
- 不对 α=1/3、λ=124.6 km 宣称某个未经真正联合似然计算的经验置信上界。
- 数学公式大部分为已知标量—度规和指数核理论，ROOT 的命名不构成原创性证据。
