# ROOT V135｜四种相互作用、空间螺旋和地月精算：数学推导与审计

版本：2026-11-23。**研究构想，不是已证实的四力统一理论**。

## 0. 单位与符号（严格）

**理论推导只取 \(c=1\)，绝不同时取 \(\hbar=1\) 或 \(G=1\)。**

令长度 \(L\)、质量 \(M\)、时间维度 \(T=L\)。于是：

- \([G]=L/M\)；\([\hbar]=ML\)；\([\mathcal R]=L^{-2}\)。
- \([S]=ML=[\hbar]\)；\([d^4x]=L^4\)。
- \([\kappa]=[\tau]=[\omega]=L^{-1}\)，\([\lambda]=L\)。
- \([\rho]=M/L^3\)，\([\Phi_{\rm Newton}]=1\)，\([\mathbf g]=L^{-1}\)。

**计算程序使用卫星测地资料原有的 SI 单位（米、秒、千克）输入、输出。** 这只是测量数字的单位接口，不意味着在理论中恢复 \(c\neq1\)。

## 1. 什么才是“统一的方程”

一个可被变分、具有明确对称性和自由度的总作用量，才能涵盖各场。

\[
\boxed{\delta S[\Phi]=0},\quad
S=S_{\rm EH}+S_{\rm SM}+S_{\rm extra}.
\]

其中已建立的广义相对论部分：

\[
S_{\rm EH}=\frac1{16\pi G}\int d^4x\sqrt{-g}\,\mathcal R.
\]

\(S_{\rm SM}[g,A,\psi,H;\hbar,g_1,g_2,g_3]\) 为具有规范群
\(SU(3)_C\times SU(2)_L\times U(1)_Y\) 的已知标准模型作用量。它描述的基本相互作用是电弱和强相互作用，电磁相互作用来自电弱对称性破缺后的剩余 \(U(1)_{\rm em}\)。

对这些场分别变分，可在合适极限恢复：

\[
G_{\mu\nu}=8\pi G\,T_{\mu\nu},\qquad
D_\mu F^{A\mu\nu}=J^{A\nu},\qquad
(i\hbar\gamma^\mu D_\mu-m)\psi=0.
\]

最后一式是简化的有质量 Dirac 场表达；完整标准模型包含自发对称性破缺、Yukawa 相互作用、规范作用和适当的手征表象。规范场强、源和耦合采用同一套归一化才使第二式成立。

**重要：直接写出 \(S_{\rm EH}+S_{\rm SM}\) 不是从单一原理推导出四力，只是把两个已知理论并列。**

## 2. 可推导的实验候选：一个额外的有质量标量

作为明确的 *现象学竞争模型*，定义：

\[
\begin{aligned}
S_{\rm cand}={}&\frac1{16\pi G}\int d^4x\sqrt{-g}\,\mathcal R\\
&+\int d^4x\sqrt{-g}\left[-\frac12(\nabla\varphi)^2-\frac{\varphi^2}{2\lambda^2}\right]\\
&+S_{\rm SM}[\widetilde g,\psi,A,H;\hbar],\\
\widetilde g_{\mu\nu}={}&e^{2\beta\sqrt{4\pi G}\,\varphi}g_{\mu\nu}.
\end{aligned}
\]

其中 \(\varphi\) 为新的假设性场，\([\varphi]=\sqrt{M/L}\)；指数的指数 \(\beta\sqrt{4\pi G}\varphi\) 无量纲，因此 \(\beta\) 无量纲。此模型一般不需要先假定空间挠率存在。

在线性、静态、弱场和普适物质耦合近似下，一个点质量之间的相互作用势为：

\[
V(r)=-\frac{Gm_1m_2}{r}\left[1+\alpha e^{-r/\lambda}\right],\qquad \alpha=\beta^2.
\]

为检查 ROOT 以前的假设可取 \(\alpha=1/3\)、\(\lambda=124.6\,\mathrm{km}\)，这**不是**从螺旋原理推导出的数值。这个标量模型也是已知的理论工具，不是 ROOT 的新发现。

## 3. 空间光速螺旋：能够严格证明什么？

选定惯性系中的曲线：

\[
\mathbf x(t)=\big(a\cos\omega t,\ a\sin\omega t,\ ut\big),
\quad \dot{\mathbf x}^2=a^2\omega^2+u^2.
\]

ROOT 假设某种基础激发的空间轨迹为类光运动，取 \(\dot{\mathbf x}^2=1\)。于是：

\[
a^2\omega^2+u^2=1,\quad
\kappa=\frac{a\omega^2}{a^2\omega^2+u^2}=a\omega^2,
\quad \tau=\frac{u\omega}{a^2\omega^2+u^2}=u\omega.
\]

得到：

\[
\boxed{\kappa^2+\tau^2=\omega^2},
\qquad \mathbf v\cdot\mathbf a=0.
\]

这是**纯几何恒等式**，不能据此推出基本力或粒子质量。若把这条弯曲类光轨迹作为自由粒子的质心世界线，那么在平直时空中它并不是自由的惯性测地线；必须给出导引机制或外力，并核算其能量、动量守恒。内部波动相位绕螺旋变化并不等于质心也绕螺旋运动。

Frenet–Serret 三正交标架：

\[
\mathbf t\cdot\mathbf n=\mathbf n\cdot\mathbf b=\mathbf b\cdot\mathbf t=0,
\quad \mathbf b=\mathbf t\times\mathbf n.
\]

恒速圆柱螺旋的加速度纯法向；**切向和副法向不必存在独立非零作用力**。几何三方向与内部规范群的生成元（\(1+3+8\) 个）不是同一个概念。

普适 \(\mathbf g\perp\mathbf E\perp\mathbf B\) 也不成立。沿一个理想、轴向对齐的磁偶极子极轴，\(\mathbf B\parallel\mathbf g\)（或反向），与普适正交假设矛盾；普通静态电磁场也无需 \(\mathbf E\perp\mathbf B\)。真空电磁平面波有特殊的正交关系，但不能泛化。

## 4. 不把地球当成点质量：有限球体的 Yukawa 积分

密度 \(\rho(s)\) 为球对称，球体半径 \(R\)，观察点 \(r\ge R\)。点元的 Yukawa 核为 \(e^{-d/\lambda}/d\)。精确角积分为

\[
\int d\Omega\frac{e^{-\lvert\mathbf r-\mathbf s\rvert/\lambda}}{\lvert\mathbf r-\mathbf s\rvert}
=\frac{4\pi e^{-r/\lambda}}{r}
\frac{\sinh(s/\lambda)}{s/\lambda}.
\]

定义

\[
M=4\pi\int_0^R ds\,\rho(s)s^2,\quad
Q=4\pi\int_0^R ds\,\rho(s)s^2\frac{\sinh(s/\lambda)}{s/\lambda},\quad
C=e^{-R/\lambda}Q.
\]

于是**球外候选势、加速度大小及相对牛顿比率**为

\[
\boxed{\Phi_Y(r)=-\frac{G\alpha C}{r}e^{-(r-R)/\lambda}},
\]

\[
\boxed{|\mathbf g_Y(r)|=\frac{G\alpha C}{r^2}\left(1+\frac r\lambda\right)e^{-(r-R)/\lambda}},
\]

\[
\boxed{\epsilon(r)=\frac{|\mathbf g_Y|}{|\mathbf g_N|}=
\alpha\frac{C}{M}\left(1+\frac r\lambda\right)e^{-(r-R)/\lambda}}.
\]

若密度为常数的层段 \(s\in[a,b]\)，其对 \(C\) 的精确贡献为

\[
C_{ab}=2\pi\rho\lambda^2\left[
(s-\lambda)e^{-(R-s)/\lambda}+(s+\lambda)e^{-(R+s)/\lambda}
\right]_{a}^{b}.
\]

程序采用此闭式解，又使用独立的辛普森求积交叉验证，还用势函数有限差分对加速度求导。

对于均匀球，\(x=R/\lambda\)，再得到一个不依赖数值积分的检查：

\[
\epsilon(R)=\alpha\frac{3(x\cosh x-\sinh x)}{x^3}(1+x)e^{-x}.
\]

**这一步的数学正确性可以复核，实际存在第五力则没有因此得到证明。**

## 5. 地球与月球：固定同一参数的可证伪预测

JPL DE440 引力参数为

\[
\mu_E=3.98600435507\times10^{14}\,{\rm m^3/s^2},\qquad
\mu_M=4.902800118\times10^{12}\,{\rm m^3/s^2}.
\]

用 CODATA \(G=6.67430(15)\times10^{-11}\,\mathrm{m^3kg^{-1}s^{-2}}\) 才能把 \(\mu\) 转成以 kg 表示的天体质量。这种换算 **不是从微观几何独立推导出了质量或 G**。只用引力轨道资料通常首先得到 \(GM\)，不是可分离的 \(G\) 和 \(M\)。

继续沿用 V132 的地球五层**示意密度**，并为月球建立四层**示意密度**（不是 PREM 或 GRAIL 反演）：

| 来源 | 地表候选额外比例 \(\epsilon(R)\) | 额外加速度（m/s²）|
|---|---:|---:|
| 地球（五层） | 0.00628038673 | 0.06167496988 |
| 月球（四层） | 0.03294588251 | 0.05351132428 |

在地球平均球半径之上 400 km：\(\delta g\approx0.00233866234\,\mathrm{m/s^2}\)。注意，这个数值与旧 V132 结果一致，但原因是继承了相同的示意层分布和参数。

### 为什么跨天体很重要？

候选参数 \(\alpha,\lambda\) 若称为基本的、普适的相互作用参数，就应当**在地球、月球、太阳之间共同固定**。相同参数对不同半径和密度结构的天体预测不同，但不能对每个天体随意重设 \(\alpha\)。

### 与地球赤道参考重力的初步冲突

使用 \(J_2\) 和自转模型，计算赤道有效重力 \(9.780281495\,\mathrm{m/s^2}\)，与 NASA 的**四舍五入后** \(9.780\,\mathrm{m/s^2}\) 相符。

在同一模型加上额外假设引力 \(0.058175122\,\mathrm{m/s^2}\)，得到 \(9.838456617\,\mathrm{m/s^2}\)。相比 NASA 赤道参考值高出 \(0.058456617\,\mathrm{m/s^2}\)。

**这是强烈的数值一致性警告，不是对新引力的发现，更不能替代严谨的多仪器原始观测和误差协方差排除分析。** 高阶地球重力场、地形、潮汐、系统误差以及 \(GM\) 与新参数的关联必须正确建模；是否已经被数据正式排除还需独立检验。

## 6. 可辨识性：为什么只测一个高度不够

在 \(\lambda\) 固定并线性化的条件下，定义 \(H_i=\epsilon(r_i)|_{\alpha=1}\)。局部相对测量残差可以写成

\[
y_i=\beta_0+\alpha H_i+\eta_i,
\]

\(\beta_0\) 表示待标定的统一尺度偏差（例如近似的 \(\delta GM/GM\)），\(\eta_i\) 是残差。单一高度无法区分 \(\beta_0\) 与 \(\alpha\)：设计矩阵两列在该采样下共线。多高度、不同密度天体、独立质量约束可提高可辨识性。

程序包含一次**完全合成数据**的注入/恢复试验（\(\beta_0=2\times10^{-4},\alpha=0.05\)），并验证零信号的恢复。它只是算法单元测试，并不构成新的物理实验。

## 7. 地球三维力方向、内部密度和自转

在球外取轴对称 \(J_2\) 势（地球赤道半径 \(R_e\)、\(\theta\) 为余纬）：

\[
\Phi=-\frac{\mu_E}{r}\bigg[1-J_2\bigg(\frac{R_e}{r}\bigg)^2P_2(\cos\theta)\bigg],
\qquad \mathbf g=-\nabla\Phi.
\]

计算了赤道、北极、中纬度和非子午线点的矢量，以及地固旋转参考系中的离心项。对于自由飞行的卫星，应使用合适惯性系的运动方程，不应把旋转坐标项作为新的引力。

对于球对称地球/月球内部，牛顿基准为 \(g(r)=GM(<r)/r^2\)，球心处 \(g(0)=0\)。该公式不能外推为整个非球形真实地球的精密场。`results/interior_profiles.csv` 给出分层示意结果。

## 8. 近圆轨道进动：另一项尖锐的反证检验

在仅含球对称牛顿场与该 Yukawa 候选项的理想模型中，令

\[s(r)=\alpha\frac{C}{M}e^{-(r-R)/\lambda},\quad
\epsilon(r)=s(r)(1+r/\lambda).\]

绕中心作近圆运动的角频率与小径向振荡频率：

\[
\Omega^2=\frac{\mu}{r^3}[1+\epsilon(r)],\qquad
\kappa_r^2=\frac{\mu}{r^3}\left[1+\epsilon(r)-s(r)\left(\frac{r}{\lambda}\right)^2\right].
\]

若两者正定，近圆轨道每圈拱点进动近似为

\[
\boxed{\Delta\varpi=2\pi\left(\frac{\Omega}{\kappa_r}-1\right)}.
\]

在地球平均半径之上 400 km，本轮示意候选参数预测 **0.0455710 rad/圈（约 2.611°/圈）**。该值来自球对称数学模型，不包含真实地球 \(J_2\)、多极矩、潮汐、相对论或其他卫星扰动；它**不代表真实观测到的卫星进动**，但为理论提出了更强的验证压力。完整结果参见 `results/candidate_near_circular_precession.csv`。

## 9. 真正的四力统一需要满足哪些更严格的门槛？

1. **单一明确的基础动力学**：不能预先把想得到的规范群写在作用量中，再宣称已经推导。
2. **准确的微观谱**：要独立生成标准模型费米子手征表示、规范群、质量机制和耦合。
3. **守恒、协变、量子一致性**：局域洛伦兹对称、能动量守恒、规范异常消除、可重整化或可控制的有效场论截断。
4. **正确恢复引力与已知实验**：弱场、光偏折、引力红移、轨道进动、地月轨道、强等效原理约束。
5. **独立、盲测、可证伪的预测**：给出不重新拟合参数就能同时解释地球、月球及粒子实验的数据。

截止 V135，**没有得到四力的共同微观起源、没有推导出 \(G\)、\(\hbar\) 或规范耦合常数，也没有真正独立的第四力统一证明。** 本轮取得的是数学模型和数值审计上的实质进展。
