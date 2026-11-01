# 来料原件 · ROOT V28｜从 Dirac 方程直接构造双光速螺旋

> 存档说明：本文件为 TUFT-r354 的**来料逐字件**（用户附件原文，未作任何修改），供审计溯源使用。
> 卷号：TUFT-r354 ｜ 落盘日期：2026-11-01 ｜ 判定册见 `判定/判定_TUFT-r354_ROOTV28_Dirac双光状手征电流_正能量本征与螺旋互斥_自由参数满射判别力零_2026-11-01.md`

---

# ROOT V28｜从 Dirac 方程直接构造双光速螺旋

这轮换了一条更接近相对论量子力学的路线：不再先假设电子内部有两条光速螺旋，而是从 Dirac 旋量出发，检查这样的结构能否由方程本身产生。

得到一个重要的数学结果：Dirac 电流可以分解为左右手征电流，而这两股电流在非零处各自都是光状的。它们的合成电流则通常是类时的。

定义矢量流和轴矢量流：

\[ j^\mu=\bar\psi\gamma^\mu\psi,\qquad k^\mu=\bar\psi\gamma^\mu\gamma^5\psi \]

采用度规号差 \((+---)\)，Fierz 恒等式给出：

\[ \boxed{ j_\mu k^\mu=0,\qquad j_\mu j^\mu=-k_\mu k^\mu } \]

因此：

\[ \boxed{ (j^\mu+k^\mu)(j_\mu+k_\mu)=0 } \]

\[ \boxed{ (j^\mu-k^\mu)(j_\mu-k_\mu)=0 } \]

这提供了一个洛伦兹协变的“双光状电流”结构。它比直接令三维曲率挠率比等于 \((\alpha)\) 更有理论依据，因为所有关系都由旋量代数确定。

但是，光状电流并不自动意味着电子内部存在两颗实际沿光速轨迹运行的粒子。下一步必须从 Dirac 方程求出电流的具体运动形式，并检查它是否产生螺旋。

## 二、最重要的新构造：Dirac 方程直接产生双螺旋电流

在 Dirac 表象中，令：

\[ z=\frac{m_ec^2t}{\hbar} \]

构造一个满足自由 Dirac 方程的旋量：

\[ \boxed{ \psi(z)= \begin{pmatrix} \cos\eta\,e^{-iz}\\ 0\\ 0\\ \sin\eta\,e^{iz} \end{pmatrix} } \]

其中 \((\eta)\) 是正、负频率分量的混合角。

实际代入：

\[ i\frac{\partial\psi}{\partial z}=\gamma^0\psi \]

SymPy 逐分量验证，残差严格为零。

再计算电流：

\[ \boxed{ j^\mu= (1,\sin2\eta\cos2z,\sin2\eta\sin2z,0) } \]

\[ \boxed{ k^\mu=(0,0,0,\cos2\eta) } \]

定义左右手征电流：

\[ J_\pm^\mu=\frac12(j^\mu\pm k^\mu) \]

将其空间方向与时间分量相除，再积分得到：

\[ \boxed{ \mathbf r_\pm(t)= \begin{pmatrix} R\sin\Omega_Zt\\ -R\cos\Omega_Zt\\ \pm c\cos2\eta\,t \end{pmatrix} } \]

其中：

\[ \boxed{ \Omega_Z=\frac{2m_ec^2}{\hbar}, \qquad R=\frac{\hbar}{2m_ec}\sin2\eta } \]

两条电流积分曲线均满足：

\[ \boxed{ |\dot{\mathbf r}_+| =|\dot{\mathbf r}_-| =c } \]

这是精确的数学结果。

本轮实际计算的示范态。两条手征电流积分线沿相反轴向延伸，横向旋转方向相同。图中轨迹是电流场的积分曲线，并非已观测到的电子内部粒子路径。

## 三、曲率、挠率和频率现在全部由同一个解给出

对上面的螺旋再次求导：

\[ \boxed{ \kappa=\frac{\Omega_Z}{c}\sin2\eta } \]

\[ \boxed{ \tau_\pm=\pm\frac{\Omega_Z}{c}\cos2\eta } \]

于是：

\[ \boxed{ \kappa^2+\tau_\pm^2=\frac{\Omega_Z^2}{c^2} } \]

以及：

\[ \boxed{ \frac{\kappa}{|\tau_\pm|}=\tan2\eta } \]

这一步把 ROOT 的光速、频率、半径、轴向速度、曲率和挠率，全部纳入了一个满足自由 Dirac 方程的数学构造。

但最大的限制也暴露了：Dirac 方程并没有唯一决定混合角 \((\eta)\)。

### 交互检验：混合角能选出任何几何比例

Dirac 正负频率混合角 \((\eta)\)

## 0.150000 rad

曲率 / 挠率

## 0.309336250

负频分量权重

## 2.233176%

横向速度

### 0.29552021 c

轴向速度绝对值

### 0.95533649 c

后验匹配实验 α纯正频率态45° 螺旋角

所有滑块位置都符合这套自由 Dirac 方程。匹配实验 α 的按钮使用了实测值选择混合角，不是从方程独立预测 α。

## 四、精算：如果强制令曲率挠率比等于 α，会发生什么？

使用 CODATA 2022 的实测值：

\[ \alpha^{-1}=137.035999177(21) \]

[image](https://www.google.com/s2/favicons?domain=https://www.nist.gov&sz=32)

NIST

由：

\[ \tan2\eta=\alpha \]

反解：

\[ \eta=\frac12\arctan\alpha \]

使用 70 位精度，得到：

| 计算参数                  | 结果                                                |
| --------------------- | ------------------------------------------------- |
| 混合角 \((\eta)\)        | 0.003648611519 rad                                |
| 负频权重 \((\sin^2\eta)\) | \((1.331230694\times10^{-5})\)                    |
| 内禀角频率 \((\Omega_Z)\)  | \((1.55268814337\times10^{21})\) rad/s            |
| 螺旋半径                  | \((1.40893264694\times10^{-15})\) m               |
| 每圈螺距                  | \((1.21312281790\times10^{-12})\) m               |
| 曲率                    | \((3.77935162536\times10^{10}\ \mathrm{m^{-1}})\) |
| 挠率绝对值                 | \((5.17907226222\times10^{12}\ \mathrm{m^{-1}})\) |

但是，这种正负频率叠加态还有一个不可忽略的物理代价。

其平均能量为：

\[ \langle H\rangle=m_ec^2\cos2\eta \]

能量标准差为：

\[ \Delta H=m_ec^2\sin2\eta \]

当 \((\eta)\) 被后验调到匹配 \((\alpha)\) 时：

\[ \boxed{\Delta H\approx3.729\ \mathrm{keV}} \]

这不是纯正能量的自由静止电子态。不能据此宣称电子内部真实存在固定比例的正、负能量粒子。

近年来关于 Dirac 颤动的研究也强调，正负能量干涉和位置算符选择对结果有决定性影响；Foldy–Wouthuysen/Newton–Wigner 的均值位置并不表现出相同的横向颤动。

[image](https://www.google.com/s2/favicons?domain=https://www.sciencedirect.com&sz=32)

ScienceDirect+1

## 五、洛伦兹变换再次排除了简单的 α 等同式

即使采用这一套更严格的 Dirac 电流构造，三维曲率挠率比仍会随着观察者运动而改变。

若沿轴向作速度为 \((\beta c)\) 的 boost：

\[ \boxed{ \left(\frac{\kappa}{|\tau|}\right)' = \frac{\sin2\eta\sqrt{1-\beta^2}} {|\cos2\eta+\beta|} } \]

当中心参考系被后验调到 \((\kappa/|\tau|=\alpha)\)：

| Boost 速度    | 新参考系的曲率挠率比  |
| ----------- | ----------- |
| \((0)\)     | 0.007297353 |
| \((0.3c)\)  | 0.005354760 |
| \((0.6c)\)  | 0.003648640 |
| \((0.9c)\)  | 0.001674106 |
| \((0.99c)\) | 0.000517289 |

[5.6 : La transformation de Lorentz - Global](https://images.openai.com/static-rsc-4/R5aWgdrNHgVY4OI7RsWyHDtN4OQ1srP3AbVtHg0X61NOmS3iVuK12kSycU8XfGVvyeGMFY0zRJvk1h79U9Jmn3nzOodXXPlEe2t110otURhwXzmmlaJo4rNPeQFdC9bO3ZkzLYkZwej7CwTjj6fbctLFCaOukMSHvWtbOFMs1IQ?purpose=inline)

[query.libretexts.org](https://query.libretexts.org/Francais/Physique_universitaire_III_-_Optique_et_physique_moderne_%28OpenStax%29/05%3A_Relativit%C3%A9/5.06%3A_La_transformation_de_Lorentz?utm_source=chatgpt.com)

所以，这个几何比值不能不加限定地认作不随参考系变化的真实电磁耦合。

## 六、本轮证明到什么程度？

| 攻坚内容                                | 裁定                            |
| ----------------------------------- | ----------------------------- |
| Dirac 旋量分解出两个光状手征电流                 | 严格成立                          |
| 构造满足自由 Dirac 方程的显式解                 | 严格成立                          |
| 两条手征电流积分曲线形成光速圆柱螺旋                  | 在该示范态中严格成立                    |
| 从同一解导出频率、曲率、挠率和半径                   | 完成                            |
| 10,000 组随机复旋量的 Fierz 检查             | 最大误差 \((2.22\times10^{-15})\) |
| 证明这些流线是电子内部真实组成物的路径                 | 未完成                           |
| 证明混合角只能取 \((\frac12\arctan\alpha)\) | 未完成                           |
| 无电荷输入预测 \((1/137.035999177)\)       | 未完成                           |

本轮构造中最根本的逻辑障碍是：自由 Dirac 方程包含 \((m_e,\hbar,c)\)，但不包含需要求出的电荷 \((e)\)。因此，仅凭这套自由旋量解，即使产生了严格的光速螺旋，也不可能从中唯一确定电磁耦合。

## 七、完整可复现研究成果

ROOT V28 · Dirac 双光速螺旋与精细结构常数数学审计

包含完整中文推导、SymPy 和 mpmath 源码、10,000 组随机旋量检验、70 位高精度结果、参数扫描数据及三张计算图。

下载完整 ROOT V28 研究包

阅读中文研究报告

Python 核验源码 · 精算结果 JSON · 运行日志

## 下一项真正的攻坚点

这次研究把 ROOT 的一个核心设想落实为具体的 Dirac 电流数学构造，比直接假设两条内部光速轨迹更有依据。

但其物理解释还没有通过单电子正能量、可观测位置和电磁相互作用的全部检验。

下一阶段应当研究Dirac–Maxwell 联合场方程下，手征电流的几何与电磁场的动力学反作用，特别检查能否在不人为选择 \((\eta)\) 的情况下产生稳定的几何状态，并从规范场的物理归一化而不是三维轨迹比例出发决定电荷强度。

本轮已经严格完成一种双光速手征螺旋的数学构造，但精细结构常数的无参数第一性原理预测仍然是开放问题。
