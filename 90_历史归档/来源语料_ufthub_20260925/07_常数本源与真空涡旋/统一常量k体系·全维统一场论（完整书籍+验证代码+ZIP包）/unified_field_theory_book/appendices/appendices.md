# 附录A · 数学公式速查表

## A.1 k体系核心定义

| 符号 | 定义 | 量纲 | 数值 |
|---|---|---|---|
| \(k\) | \(4\pi G\) | \(L^3M^{-1}T^{-2}\) | \(8.387 \times 10^{-10}\) m³kg⁻¹s⁻² |
| \(k'\) | \(1/\varepsilon_0\) | \(ML^3T^{-4}I^{-2}\) | \(1.129 \times 10^{11}\) m/F |
| \(\eta\) | \(Q/M\) | \(M^{-1}IT\) | 粒子依赖 |
| \(\xi\) | 色荷/M | 依赖定义 | 粒子依赖 |

## A.2 场方程

**爱因斯坦场方程**：
\[
G_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu} = \frac{2k}{c^4}T_{\mu\nu}
\]

**希尔伯特作用量**：
\[
S_H = \frac{c^4}{16\pi G}\int R\sqrt{-g}\,d^4x = \frac{c^4}{4k}\int R\sqrt{-g}\,d^4x
\]

**麦克斯韦方程**：
\[
\nabla\cdot\mathbf{E} = \frac{\rho_e}{\varepsilon_0} = k'\rho_e
\]

## A.3 力定律

**牛顿引力**：
\[
F = G\frac{Mm}{r^2} = \frac{k}{4\pi}\frac{Mm}{r^2}
\]

**库仑力**：
\[
F = \frac{1}{4\pi\varepsilon_0}\frac{Qq}{r^2} = \frac{k'}{4\pi}\frac{Qq}{r^2}
\]

## A.4 普朗克量

| 量 | 传统形式 | k形式 | 数值 |
|---|---|---|---|
| 质量 | \(\sqrt{\hbar c/G}\) | \(\sqrt{4\pi\hbar c/k}\) | \(2.176\times10^{-8}\) kg |
| 长度 | \(\sqrt{G\hbar/c^3}\) | \(\sqrt{k\hbar/(4\pi c^3)}\) | \(1.616\times10^{-35}\) m |
| 时间 | \(\sqrt{G\hbar/c^5}\) | \(\sqrt{k\hbar/(4\pi c^5)}\) | \(5.391\times10^{-44}\) s |
| 能量 | \(\sqrt{\hbar c^5/G}\) | \(\sqrt{4\pi\hbar c^5/k}\) | \(1.956\times10^9\) J |

## A.5 宇宙学

**弗里德曼方程**：
\[
H^2 = \frac{8\pi G}{3}\rho - \frac{Kc^2}{a^2} + \frac{\Lambda c^2}{3} = \frac{2k}{3}\rho - \frac{Kc^2}{a^2} + \frac{\Lambda c^2}{3}
\]

**加速度方程**：
\[
\frac{\ddot{a}}{a} = -\frac{4\pi G}{3}\left(\rho+\frac{3p}{c^2}\right)+\frac{\Lambda c^2}{3} = -\frac{k}{6}\left(\rho+\frac{3p}{c^2}\right)+\frac{\Lambda c^2}{3}
\]

**临界密度**：
\[
\rho_c = \frac{3H^2}{8\pi G} = \frac{3H^2}{2k}
\]

## A.6 黑洞热力学

**史瓦西半径**：
\[
r_s = \frac{2GM}{c^2} = \frac{kM}{2\pi c^2}
\]

**霍金温度**：
\[
T_H = \frac{\hbar c^3}{8\pi GMk_B} = \frac{\hbar c^3}{2kMk_B}
\]

**贝肯斯坦-霍金熵**：
\[
S_{BH} = \frac{4\pi Gk_BM^2}{\hbar c} = \frac{kk_BM^2}{\hbar c}
\]

**蒸发寿命**：
\[
\tau \approx \frac{5120\pi G^2M^3}{\hbar c^4} = \frac{320k^2M^3}{\pi\hbar c^4}
\]

## A.7 天体物理

**钱德拉塞卡极限**：
\[
M_{Ch} = \frac{5.83}{\mu_e^2}\left(\frac{\hbar c}{G}\right)^{3/2}\frac{1}{m_H^2} = \frac{5.83}{\mu_e^2}\left(\frac{4\pi\hbar c}{k}\right)^{3/2}\frac{1}{m_H^2}
\]

**TOV方程**：
\[
\frac{dP}{dr} = -\frac{kM\rho}{4\pi r^2}\left(1+\frac{P}{\rho c^2}\right)\left(1+\frac{kr^3P}{Mc^2}\right)\left(1-\frac{kM}{2\pi c^2r}\right)^{-1}
\]

**光线偏折**：
\[
\alpha = \frac{4GM}{c^2b} = \frac{kM}{\pi c^2b}
\]

**引力波四极辐射**：
\[
P = \frac{G}{5c^5}\langle\dddot{Q}_{ij}\dddot{Q}_{ij}\rangle = \frac{k}{20\pi c^5}\langle\dddot{Q}_{ij}\dddot{Q}_{ij}\rangle
\]

## A.8 量纲相容条件

\[
[k'\eta^2] = [k] = L^3M^{-1}T^{-2}
\]
\[
[k_s\xi^2] = [k] = L^3M^{-1}T^{-2}
\]

---

# 附录B · 物理常数表（CODATA 2022）

## B.1 基本常数

| 常数 | 符号 | 数值 | 单位 |
|---|---|---|---|
| 光速 | \(c\) | 299792458 | m/s（精确） |
| 普朗克常数 | \(h\) | 6.62607015×10⁻³⁴ | J·s（精确） |
| 约化普朗克常数 | \(\hbar\) | 1.054571817×10⁻³⁴ | J·s |
| 万有引力常数 | \(G\) | 6.67430(15)×10⁻¹¹ | m³kg⁻¹s⁻² |
| 统一常量k | \(k=4\pi G\) | 8.38717×10⁻¹⁰ | m³kg⁻¹s⁻² |
| 基本电荷 | \(e\) | 1.602176634×10⁻¹⁹ | C（精确） |
| 真空磁导率 | \(\mu_0\) | 1.25663706212×10⁻⁶ | H/m |
| 真空介电常数 | \(\varepsilon_0\) | 8.8541878128×10⁻¹² | F/m |
| 电磁耦合k' | \(k'=1/\varepsilon_0\) | 1.12941×10¹¹ | m/F |
| 玻尔兹曼常数 | \(k_B\) | 1.380649×10⁻²³ | J/K（精确） |
| 阿伏伽德罗常数 | \(N_A\) | 6.02214076×10²³ | mol⁻¹（精确） |

## B.2 粒子质量

| 粒子 | 符号 | 质量 (kg) | 质量 (MeV/c²) |
|---|---|---|---|
| 电子 | \(e^-\) | 9.1093837015×10⁻³¹ | 0.51099895 |
| 质子 | \(p\) | 1.67262192369×10⁻²⁷ | 938.272088 |
| 中子 | \(n\) | 1.67492749804×10⁻²⁷ | 939.565420 |
| μ子 | \(\mu^-\) | 1.883531627×10⁻²⁸ | 105.658375 |
| τ子 | \(\tau^-\) | 3.16754×10⁻²⁷ | 1776.86 |
| 上夸克 | \(u\) | — | 2.2±0.5 |
| 下夸克 | \(d\) | — | 4.7±0.5 |
| 粲夸克 | \(c\) | — | 1270±20 |
| 奇异夸克 | \(s\) | — | 95±5 |
| 顶夸克 | \(t\) | — | 173000±400 |
| 底夸克 | \(b\) | — | 4180±30 |
| 希格斯玻色子 | \(H\) | — | 125100±140 |
| W玻色子 | \(W^\pm\) | — | 80379±12 |
| Z玻色子 | \(Z^0\) | — | 91187.6±2.1 |

## B.3 天体物理常数

| 常数 | 数值 |
|---|---|
| 太阳质量 \(M_\odot\) | 1.98847×10³⁰ kg |
| 太阳半径 \(R_\odot\) | 6.957×10⁸ m |
| 太阳光度 \(L_\odot\) | 3.828×10²⁶ W |
| 地球质量 \(M_\oplus\) | 5.9722×10²⁴ kg |
| 地球半径 \(R_\oplus\) | 6.371×10⁶ m |
| 天文单位 AU | 1.495978707×10¹¹ m |
| 光年 ly | 9.4607304725808×10¹⁵ m |
| 秒差距 pc | 3.0856775814913673×10¹⁶ m |

## B.4 宇宙学参数（普朗克2018）

| 参数 | 数值 | 不确定度 |
|---|---|---|
| \(H_0\) (km/s/Mpc) | 67.4 | ±0.5 |
| \(\Omega_m h^2\) | 0.1430 | ±0.0011 |
| \(\Omega_b h^2\) | 0.02240 | ±0.00014 |
| \(\Omega_c h^2\) | 0.1200 | ±0.0012 |
| \(\Omega_\Lambda\) | 0.6889 | ±0.0056 |
| \(\Omega_m\) | 0.3111 | ±0.0056 |
| \(\Omega_K\) | 0.0007 | ±0.0019 |
| \(n_s\) | 0.9650 | ±0.0041 |
| \(r\) | <0.06 | 95% CL |
| \(w\) | -1.03 | ±0.03 |
| 宇宙年龄 (Gyr) | 13.800 | ±0.024 |

---

# 附录C · 参考文献

## C.1 经典著作

1. Newton, I. (1687). *Philosophiæ Naturalis Principia Mathematica*.
2. Einstein, A. (1915). "Die Feldgleichungen der Gravitation". *Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin*.
3. Hilbert, D. (1915). "Die Grundlagen der Physik". *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen*.
4. Planck, M. (1899). "Über irreversible Strahlungsvorgänge". *Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin*.
5. Dirac, P. A. M. (1928). "The Quantum Theory of the Electron". *Proceedings of the Royal Society A*.
6. Heisenberg, W. (1925). "Über quantentheoretische Umdeutung kinematischer und mechanischer Beziehungen". *Zeitschrift für Physik*.
7. Schrödinger, E. (1926). "Quantisierung als Eigenwertproblem". *Annalen der Physik*.

## C.2 广义相对论与宇宙学

8. Schwarzschild, K. (1916). "Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie". *Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften*.
9. Reissner, H. (1916). "Über die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie". *Annalen der Physik*.
10. Nordström, G. (1918). "On the Energy of the Gravitational Field in Einstein's Theory". *Verhandlingen van de Koninklijke Nederlandse Akademie van Wetenschappen te Amsterdam*.
11. Kerr, R. P. (1963). "Gravitational Field of a Spinning Mass as an Example of Algebraically Special Metrics". *Physical Review Letters*.
12. Newman, E. T., et al. (1965). "Metric of a Rotating, Charged Mass". *Journal of Mathematical Physics*.
13. Friedman, A. (1922). "Über die Krümmung des Raumes". *Zeitschrift für Physik*.
14. Lemaître, G. (1927). "Un univers homogène de masse constante et de rayon croissant rendant compte de la vitesse radiale des nébuleuses extra-galactiques". *Annales de la Société Scientifique de Bruxelles*.
15. Robertson, H. P. (1935). "Kinematics and World-Structure". *The Astrophysical Journal*.
16. Walker, A. G. (1937). "On Milne's Theory of World-Structure". *Proceedings of the London Mathematical Society*.
17. Hawking, S. W. (1974). "Black hole explosions?". *Nature*.
18. Bekenstein, J. D. (1973). "Black holes and entropy". *Physical Review D*.
19. Penrose, R. (1969). "Gravitational collapse: The role of general relativity". *Rivista del Nuovo Cimento*.
20. Oppenheimer, J. R., & Volkoff, G. M. (1939). "On Massive Neutron Cores". *Physical Review*.
21. Tolman, R. C. (1939). "Static Solutions of Einstein's Field Equations for Spheres of Fluid". *Physical Review*.
22. Chandrasekhar, S. (1931). "The Maximum Mass of Ideal White Dwarfs". *The Astrophysical Journal*.

## C.3 量子场论与标准模型

23. Yang, C. N., & Mills, R. L. (1954). "Conservation of Isotopic Spin and Isotopic Gauge Invariance". *Physical Review*.
24. Glashow, S. L. (1961). "Partial Symmetries of Weak Interactions". *Nuclear Physics*.
25. Salam, A. (1968). "Weak and Electromagnetic Interactions". *Elementary Particle Physics*.
26. Weinberg, S. (1967). "A Model of Leptons". *Physical Review Letters*.
27. Higgs, P. W. (1964). "Broken Symmetries and the Masses of Gauge Bosons". *Physical Review Letters*.
28. Englert, F., & Brout, R. (1964). "Broken Symmetry and the Mass of Gauge Vector Mesons". *Physical Review Letters*.
29. Gross, D. J., & Wilczek, F. (1973). "Ultraviolet Behavior of Non-Abelian Gauge Theories". *Physical Review Letters*.
30. Politzer, H. D. (1973). "Reliable Perturbative Results for Strong Interactions?". *Physical Review Letters*.
31. 't Hooft, G., & Veltman, M. (1972). "Regularization and renormalization of gauge fields". *Nuclear Physics B*.
32. Kobayashi, M., & Maskawa, T. (1973). "CP-Violation in the Renormalizable Theory of Weak Interaction". *Progress of Theoretical Physics*.
33. Cabibbo, N. (1963). "Unitary Symmetry and Leptonic Decays". *Physical Review Letters*.

## C.4 宇宙学与暗能量

34. Riess, A. G., et al. (1998). "Observational Evidence from Supernovae for an Accelerating Universe and a Cosmological Constant". *The Astronomical Journal*.
35. Perlmutter, S., et al. (1999). "Measurements of Ω and Λ from 42 High-Redshift Supernovae". *The Astrophysical Journal*.
36. Guth, A. H. (1981). "Inflationary universe: A possible solution to the horizon and flatness problems". *Physical Review D*.
37. Linde, A. D. (1982). "A new inflationary universe scenario: A possible solution of the horizon, flatness, homogeneity, isotropy and primordial monopole problems". *Physics Letters B*.
38. Albrecht, A., & Steinhardt, P. J. (1982). "Cosmology for Grand Unified Theories with Radiatively Induced Symmetry Breaking". *Physical Review Letters*.
39. Peebles, P. J. E., & Ratra, B. (2003). "The cosmological constant and dark energy". *Reviews of Modern Physics*.
40. Zwicky, F. (1933). "Die Rotverschiebung von extragalaktischen Nebeln". *Helvetica Physica Acta*.
41. Rubin, V. C., & Ford, W. K. (1970). "Rotation of the Andromeda Nebula from a Spectroscopic Survey of Emission Regions". *The Astrophysical Journal*.
42. Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters". *Astronomy & Astrophysics*.

## C.5 引力波与实验

43. Abbott, B. P., et al. (LIGO Scientific Collaboration) (2016). "Observation of Gravitational Waves from a Binary Black Hole Merger". *Physical Review Letters*.
44. Abbott, B. P., et al. (2017). "GW170817: Observation of Gravitational Waves from a Binary Neutron Star Inspiral". *Physical Review Letters*.
45. Hulse, R. A., & Taylor, J. H. (1975). "Discovery of a pulsar in a binary system". *The Astrophysical Journal*.
46. Taylor, J. H., & Weisberg, J. M. (1982). "A new test of general relativity - Gravitational radiation and the binary pulsar PSR 1913+16". *The Astrophysical Journal*.
47. Dyson, F. W., Eddington, A. S., & Davidson, C. (1920). "A Determination of the Deflection of Light by the Sun's Gravitational Field, from Observations Made at the Total Eclipse of May 29, 1919". *Philosophical Transactions of the Royal Society*.
48. Pound, R. V., & Rebka, G. A. (1959). "Apparent Weight of Photons". *Physical Review Letters*.
49. Eöt-Wash Collaboration (2008). "Torsion balance experiments: A low-energy frontier of particle physics". *Progress in Particle and Nuclear Physics*.
50. MICROSCOPE Collaboration (2022). "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle". *Classical and Quantum Gravity*.

## C.6 量子引力与统一理论

51. Weinberg, S. (1979). "Ultraviolet divergences in quantum theories of gravitation". *General Relativity: An Einstein Centenary Survey*.
52. Reuter, M. (1998). "Nonperturbative evolution equation for quantum gravity". *Physical Review D*.
53. Green, M. B., Schwarz, J. H., & Witten, E. (1987). *Superstring Theory*. Cambridge University Press.
54. Polchinski, J. (1998). *String Theory*. Cambridge University Press.
55. Rovelli, C. (2004). *Quantum Gravity*. Cambridge University Press.
56. Ashtekar, A. (1986). "New Variables for Classical and Quantum Gravity". *Physical Review Letters*.
57. 't Hooft, G. (1993). "Dimensional reduction in quantum gravity". *Salamfest*.
58. Susskind, L. (1995). "The world as a hologram". *Journal of Mathematical Physics*.
59. Maldacena, J. (1999). "The Large N limit of superconformal field theories and supergravity". *International Journal of Theoretical Physics*.
60. Verlinde, E. P. (2011). "On the Origin of Gravity and the Laws of Newton". *Journal of High Energy Physics*.

## C.7 数学与方法

61. Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). *Gravitation*. W. H. Freeman.
62. Wald, R. M. (1984). *General Relativity*. University of Chicago Press.
63. Carroll, S. M. (2004). *Spacetime and Geometry: An Introduction to General Relativity*. Addison-Wesley.
64. Peskin, M. E., & Schroeder, D. V. (1995). *An Introduction to Quantum Field Theory*. Westview Press.
65. Weinberg, S. (1995). *The Quantum Theory of Fields* (Vols. 1-3). Cambridge University Press.
66. Griffiths, D. J. (2008). *Introduction to Elementary Particles*. Wiley-VCH.
67. Kolb, E. W., & Turner, M. S. (1990). *The Early Universe*. Addison-Wesley.
68. Dodelson, S. (2003). *Modern Cosmology*. Academic Press.
69. Buckingham, E. (1914). "On physically similar systems; illustrations of the use of dimensional equations". *Physical Review*.
70. Barenblatt, G. I. (1996). *Scaling, Self-Similarity, and Intermediate Asymptotics*. Cambridge University Press.

---

# 附录D · 索引

## D.1 概念索引

- **渐近自由** — 第三卷第15章
- **暗能量** — 第六卷第29章
- **暗物质** — 第六卷第29章
- **奥本海默-沃尔科夫极限** — 第七卷第35章
- **暴胀** — 第六卷第31章
- **贝肯斯坦-霍金熵** — 第二卷第9章
- **比安基恒等式** — 第二卷第8章
- **标准模型** — 第三卷
- **测地线方程** — 第二卷第7章
- **钱德拉塞卡极限** — 第七卷第34章
- **大统一理论** — 第三卷第16章、第八卷第40章
- **等效原理** — 第二卷第7章
- **狄拉克大数假说** — 第八卷第42章
- **弗里德曼方程** — 第六卷第28章
- **高斯定律** — 第一卷第2章
- **广义协变性** — 第二卷第7章
- **哈勃常数** — 第六卷第28章
- **哈勃张力** — 第六卷第30章
- **黑洞热力学** — 第二卷第9章
- **霍金辐射** — 第二卷第9章
- **精细结构常数** — 第三卷第16章
- **克尔解** — 第二卷第9章
- **可证伪性** — 第九卷第45章
- **量纲分析** — 第一卷第3章、第八卷第39章
- **量纲相容条件** — 第五卷第24章
- **量子色动力学** — 第三卷第15章
- **量子引力** — 第四卷第20章
- **雷斯纳-诺德斯特洛姆解** — 第二卷第9章
- **人择原理** — 第八卷第43章
- **时空泡沫** — 第四卷第18章
- **时空张力** — 第六卷第30章
- **史瓦西半径** — 第二卷第9章
- **史瓦西解** — 第二卷第9章
- **四维逻辑架构** — 第一卷第4章
- **宇宙学常数** — 第二卷第8章、第六卷
- **宇宙学常数问题** — 第八卷第40章
- **宇宙微波背景** — 第六卷第31章
- **无循环论证** — 第一卷第1章、第4章
- **希格斯机制** — 第三卷第14章
- **弦理论** — 第四卷第20章、第九卷第49章
- **圈量子引力** — 第四卷第20章、第九卷第49章
- **杨-米尔斯理论** — 第三卷第14章
- **引力波** — 第二卷第10章、第七卷第36章
- **渐近安全** — 第四卷第20章

## D.2 符号索引

- \(k \equiv 4\pi G\) — 统一常量，第一卷第2章
- \(k' = 1/\varepsilon_0\) — 电磁耦合系数，第五卷第23章
- \(k_s\) — 强相互作用耦合常数，第五卷第25章
- \(\eta = Q/M\) — 电荷-质量比，第五卷第24章
- \(\xi = \text{色荷}/M\) — 色荷-质量比，第五卷第25章
- \(G_{\mu\nu}\) — 爱因斯坦张量，第二卷第8章
- \(T_{\mu\nu}\) — 能量动量张量，第二卷第8章
- \(R_{\mu\nu}\) — 里奇张量，第一卷第5章
- \(R\) — 里奇标量，第一卷第5章
- \(\Gamma^\lambda_{\mu\nu}\) — 克里斯托费尔符号，第一卷第5章
- \(H = \dot{a}/a\) — 哈勃参数，第六卷第28章
- \(a(t)\) — 尺度因子，第六卷第28章
- \(\Omega_i\) — 密度参数，第六卷第28章
- \(\rho_c\) — 临界密度，第六卷第28章
- \(r_s = 2GM/c^2\) — 史瓦西半径，第二卷第9章
- \(T_H\) — 霍金温度，第二卷第9章
- \(S_{BH}\) — 贝肯斯坦-霍金熵，第二卷第9章
- \(m_p, l_p, t_p, E_p, T_p\) — 普朗克量，第四卷第18章
- \(\alpha\) — 精细结构常数，第三卷第16章
- \(\alpha_s\) — 强耦合常数，第三卷第15章
- \(\Lambda\) — 宇宙学常数，第二卷第8章
- \(w\) — 暗能量状态方程参数，第六卷第30章
- \(M_{Ch}\) — 钱德拉塞卡极限，第七卷第34章
- \(M_{OV}\) — 奥本海默-沃尔科夫极限，第七卷第35章

## D.3 人名索引

- 爱因斯坦（Einstein）— 第二卷
- 牛顿（Newton）— 第一卷
- 普朗克（Planck）— 第四卷
- 史瓦西（Schwarzschild）— 第二卷第9章
- 克尔（Kerr）— 第二卷第9章
- 霍金（Hawking）— 第二卷第9章
- 贝肯斯坦（Bekenstein）— 第二卷第9章
- 钱德拉塞卡（Chandrasekhar）— 第七卷第34章
- 奥本海默（Oppenheimer）— 第七卷第35章
- 弗里德曼（Friedmann）— 第六卷第28章
- 勒梅特（Lemaître）— 第六卷第28章
- 罗伯逊（Robertson）— 第六卷第28章
- 沃尔克（Walker）— 第六卷第28章
- 狄拉克（Dirac）— 第三卷、第八卷第42章
- 杨（Yang）— 第三卷第14章
- 米尔斯（Mills）— 第三卷第14章
- 格拉肖（Glashow）— 第三卷第14章
- 萨拉姆（Salam）— 第三卷第14章
- 温伯格（Weinberg）— 第三卷第14章、第四卷第20章
- 希格斯（Higgs）— 第三卷第14章
- 格罗斯（Gross）— 第三卷第15章
- 维尔切克（Wilczek）— 第三卷第15章
- 波利策（Politzer）— 第三卷第15章
- 波普尔（Popper）— 第九卷第45章
- 古斯（Guth）— 第六卷第31章
- 林德（Linde）— 第六卷第31章
- 彭罗斯（Penrose）— 第二卷第9章
- 泰勒（Taylor）— 第七卷第36章
- 赫尔斯（Hulse）— 第七卷第36章

---

**全书附录 · 完**
