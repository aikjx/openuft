# 原始数值来源与数据边界

下面链接用于审计常数和寻找后续真实数据。程序在离线环境复算；**没有下载或假装下载 EGM2008、GOCE、GRACE-FO 或 GRAIL 的原始测量数据**。

1. **JPL / NASA, Astrodynamic Parameters (DE440)**：地球 \(GM=398600.435507\) km³/s²；月球 \(GM=4902.800118\) km³/s²。 https://ssd.jpl.nasa.gov/astro_par.html
2. **NIST / CODATA 2022**：\(G=6.67430(15)\times10^{-11}\) SI，\(\hbar\) 保留有量纲。 https://physics.nist.gov/cuu/pdf/wall_2022.pdf ； https://physics.nist.gov/cuu/Constants/
3. **NASA Earth Fact Sheet**：赤道与极地半径、平均半径、赤道 9.780 m/s²、极地 9.832 m/s²（表中数值有舍入）。 https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
4. **NASA Moon Fact Sheet**：月球半径 1737.4 km、宏观重力参数与 \(J_2\)。 https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
5. **NGA EGM2008**：全球地球重力场后续真实数据入口。 https://earth-info.nga.mil/index.php?action=wgs84&dir=wgs84
6. **ICGEM**：球谐系数、重力场模型、各模型准确度文档。 https://icgem.gfz.de/faq
7. **PREM (Dziewonski & Anderson, 1981)**：地球平均径向密度参考模型；本包五层密度不是 PREM。 https://authors.library.caltech.edu/records/rjkzg-1a346
8. **NASA GRAIL**：月球重力分布和 mascon 的观测使命。 https://science.nasa.gov/mission/grail/
9. **NASA Open Data, GRAIL derived products**：球谐模型与部分协方差归档入口。 https://data.nasa.gov/dataset/grail-moon-lgrs-derived-gravity-science-data-products-v1-0-b0393

**重要的数据谱系说明**：

- JPL 的 \(GM\) 是以既定动力学模型与轨道测量求得的引力参数；用它再计算标准引力并非独立发现地球/月球质量。
- 地球五层密度继承自 V132 的**演示性**剖分，不能叫作 PREM 测量；月球四层密度同样是演示性假设，不可叫作 GRAIL 密度反演。
- 地表额外加速度的任何具体数字是由 \(\alpha=1/3,\lambda=124.6\,\mathrm{km}\) **先验假设**产生的，不是卫星观测到的残差。
- 目前只做了轴对称 \(J_2\) 截断，未完成 EGM2008 高阶地球模型或 GRAIL 高阶月球模型的原始数据拟合。
