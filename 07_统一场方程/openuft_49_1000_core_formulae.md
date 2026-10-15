# openuft#49｜1000核心理论体系公式集（EC挠率几何统一场框架）

> 文件路径：`openuft/07_统一场方程/openuft_49_1000_core_formulae.md`
> 元数据：继承 openuft#48 勘误，旧 A1/A2/A3/A4 永久作废；全部公式内嵌**量纲审计标记**；7 大模块；公式 1~1000；LaTeX 格式；关键公式附大白话释义；候选假设公式标记 `OPEN`；严格区分 7 类别；禁止数字命理，所有公式可审计。
> 译名注：用户原文"爱因斯坦-嘉唐挠率引力"按标准译名统一为**爱因斯坦-嘉当（Einstein-Cartan, EC）挠率引力**（Élie Cartan）。
> 本版归档区间：公式 601–800（模块5）。建立日期：2026-10-15。量纲侧机器裁定完成日期：2026-10-15（见 §三）。

## 〇、归档状态登记

| 区间 | 模块 | 状态 |
|---|---|---|
| 1–150 | 模块1 微分几何 & 张量基础 | 待补：源文在会话上下文中压缩丢失（已全盘检索工作区无副本） |
| 151–300 | 模块2 EC 引力核心方程 | 待补（同上） |
| 301–450 | 模块3 Clifford 代数 & 旋量表示 | 待补：仅收到截断样条 301–306 |
| 451–600 | 模块4 UFT 动力学、拉格朗日乘子与约束系统 | 待补：未提供 |
| 601–800 | 模块5 参数约化、普朗克尺度内蕴推导、数字筛查 + UFT 现象学预言 | **本版已归档** |
| 801–1000 | 模块6 自洽性审计、悖论消解、量子几何边界、总结公理体系 + 开放猜想清单 | 待补：源文已发出但随上下文压缩丢失（全库检索零副本），**待用户重新提供** |

**红线声明**：数学自洽 ≠ 实验证实；本册不粉饰、不编造读数；所有数值锚点均为 CODATA/PDG/实验公布值或定义式常数，**无数字命理**；OPEN = UFT 候选假设方程，其量纲登记项不得读作已裁定结论。

## 一、全局约定

- 时空号差 $(-,+,+,+)$；克利福德代数 $\mathrm{Cl}(1,3)$；
- 自然单位 $\hbar=c=1$（SI 形式在定义式处并列给出）；
- 指标 $a,b,c,d\in\{0,1,2,3\}$；$g_{ab}$ 时空度规；$\nabla_a$ 带挠率度量兼容联络；$T^a_{bc}$ 挠率张量；$R^a_{bcd}$ 曲率张量；
- $\ell_P$ 普朗克长度；$m_P$ 普朗克质量；$\omega$ 局域几何角频率标量场；$c$ 真空光速；$\hbar$ 约化普朗克常数；$G$ 牛顿引力常数；
- 量纲记号：**L** 长度、**T** 时间、**M** 质量；自然单位下 $[L]=[T]=[M]^{-1}$、$[G]=M^{-2}$、$[\ell_P]=[t_P]=M^{-1}$、$[m_P]=[E_P]=M$；
- 量纲审计标记约定：每条公式后嵌【量纲】行——`✓` = 两侧齐次（教科书级）；`登记` = 发现口径/量纲疑点，按 openuft 纪律留待机器裁定（Decimal 60 位 + Fraction 四元组 (M,L,T,Q) 机器兜底）；
- 七类别标签：【数学恒等式】【经典引力】【爱因斯坦-嘉当挠率引力】【旋量/克利福德代数】【统一场动力学】【标准模型嵌入】【宇宙学与观测约束】。

## 二、模块5：参数约化、普朗克尺度内蕴推导、数字筛查 + UFT现象学预言（601–800）

### 5.1 普朗克尺度内蕴推导（601–610）

**601.** $\ell_P=\sqrt{G}$（自然单位）；SI：$\ell_P=\sqrt{\hbar G/c^3}$
【数学恒等式】【量纲】✓ $[\ell_P]=L$；$[G]=M^{-2}\Rightarrow[\sqrt G]=M^{-1}=L$，两侧齐次
【大白话】普朗克长度就是把牛顿常数开方——引力常数的"自然尺寸"。SI 中补上 $\hbar/c^3$ 才凑出长度。

**602.** $m_P=1/\sqrt{G}$；SI：$m_P=\sqrt{\hbar c/G}$
【数学恒等式】【量纲】✓ $[m_P]=M$；$[G^{-1/2}]=M$

**603.** $t_P=\sqrt{G}$；SI：$t_P=\sqrt{\hbar G/c^5}$
【数学恒等式】【量纲】✓ $[t_P]=T=M^{-1}$；$[\sqrt G]=M^{-1}=T$

**604.** $E_P=1/\sqrt{G}$；SI：$E_P=\sqrt{\hbar c^5/G}$
【数学恒等式】【量纲】✓ $[E_P]=M$

**605.** $\kappa_G=8\pi G$（爱因斯坦常数/引力耦合）
【经典引力】【量纲】✓ $[\kappa_G]=[G]=M^{-2}$；$8\pi$ 无量纲

**606.** $\Lambda_P=\ell_P^{-2}$（普朗克曲率标量量级）
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\Lambda_P]=L^{-2}=M^2$（曲率标量量纲）

**607.** $\tau_P=\ell_P^{-1}$（普朗克挠率特征幅值）
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\tau_P]=L^{-1}=M$（挠率张量分量量纲）

**608.** $\omega_P=\ell_P^{-1}$，满足 $\kappa_P^2+\tau_P^2=\omega_P^2$　【OPEN】
【统一场动力学】【量纲】✓ $[\omega_P]=T^{-1}=M$；$\kappa^2+\tau^2$ 与 $\omega^2$ 均为 $M^2$（自然单位；SI 形式为 $\kappa^2+\tau^2=\omega^2/c^2$，即公式 183，模块2 待补）
【大白话】把曲率、挠率、频率放进同一个"几何毕达哥拉斯定理"：曲率的平方加挠率的平方等于频率的平方。这是整个 UFT 的脊梁骨（SI 中要除以 $c^2$ 补齐量纲）。

**609.** 普朗克尺度约束饱和：$\kappa_P^2+\tau_P^2=\omega_P^2$，UFT 核心约束在 Planck 标度紧束　【OPEN】
【统一场动力学】【量纲】✓ 同 608（各项 $M^2$）
【大白话】在普朗克标度这个约束被"顶满"——三个几何量同数量级，UFT 的自由度在那里被锁死。

**610.** 低能展开：$\kappa=\omega-\dfrac{\tau^2}{2\omega}+\mathcal O\!\left(\dfrac{\tau^4}{\omega^3}\right)$，$\tau\ll\omega$　【OPEN】
【统一场动力学】【量纲】✓ $[\kappa]=[\omega]=M$；$[\tau^2/\omega]=M$；余项 $\tau^4/\omega^3=M$

### 5.2 参数约化与重整化群（611–632）

**611.** 耦合层级假设：$G,\alpha,\alpha_s,y_e,y_u,y_d,\sin\theta_W,\theta_\text{QCD}$ 全部由 UFT 几何约束 $\kappa^2+\tau^2=\omega^2/c^2$ 在红外定点自动导出　【OPEN】
【统一场动力学】【量纲】登记：约束方程齐次（同 608 SI 形式）；但被导出对象混合量纲——$G$ 为 $M^{-2}$、其余无量纲，"自动导出"须逐项配平，待机器裁定
【大白话】最大胆的一条：标准模型里那些"手动输入"的常数（精细结构常数、夸克汤川耦合、混合角……）全都是同一条几何约束在不同能标投影出来的。这是"参数约化"的总宣言，也是本节所有 $f_\alpha,f_\theta,\dots$ 的目标。

**612.** 参数向量 $\boldsymbol\theta=\{\alpha,\alpha_s(M_Z),\sin\theta_W,m_e,m_u,m_d,m_\tau,m_t,\tau_0,\omega_0,\alpha\}$
【标准模型嵌入】【量纲】登记：混合量纲向量——无量纲：$\alpha,\alpha_s,\sin\theta_W$；质量量纲 $M$：$m_e,m_u,m_d,m_\tau,m_t,\tau_0,\omega_0$；末项 $\alpha$ 与首项重复（疑笔误，按原文存档并登记）

**613.** 无量纲 UFT 基础参数：$\hat\kappa=\kappa\ell_P,\ \hat\tau=\tau\ell_P,\ \hat\omega=\omega\ell_P$　【OPEN】
【统一场动力学】【量纲】✓ 三者均无量纲（$[\kappa\ell_P]=M\cdot M^{-1}=1$）

**614.** 无量纲约束：$\hat\kappa^2+\hat\tau^2=\hat\omega^2$；普朗克标度下 $\hat\kappa,\hat\tau,\hat\omega\sim\mathcal O(1)$　【OPEN】
【统一场动力学】【量纲】✓ 无量纲齐次

**615.** RG 流：$\mu\dfrac{d}{d\mu}\begin{pmatrix}\hat\kappa\\ \hat\tau\\ \hat\omega\end{pmatrix}=\boldsymbol\beta(\hat\kappa,\hat\tau,\hat\omega)$　【OPEN】
【统一场动力学】【量纲】✓ $\mu\,d/d\mu$ 无量纲 $\Rightarrow\boldsymbol\beta$ 各分量无量纲

**616.** UV 不动点条件：$\boldsymbol\beta(\hat\kappa_*,\hat\tau_*,\hat\omega_*)=0$；$\hat\kappa_*^2+\hat\tau_*^2=\hat\omega_*^2$　【OPEN】
【统一场动力学】【量纲】✓ 无量纲

**617.** 不动点稳定性矩阵：$\mathbf M_{ij}=\dfrac{\partial\beta_i}{\partial\theta_j}\bigg|_{*}$；$\mathrm{Re}(\lambda_i)<0$ 对应吸引 UV 不动点　【OPEN】
【统一场动力学】【量纲】✓ $\mathbf M$ 无量纲（$\beta$ 与 $\theta$ 均无量纲），本征值无量纲

**618.** 跑动几何耦合：$\hat\tau(\mu)$ 挠率耦合随能标跑动　【OPEN】
【统一场动力学】【量纲】✓ 无量纲

**619.** 低能有效理论投影：$\mathcal L_\text{eff}(\mu<\mu_*)=\mathcal L_\text{SM}+\mathcal L_\text{EC}+\Delta\mathcal L_\text{tors}(\hat\tau(\mu))$　【OPEN】
【统一场动力学】【量纲】✓ 各项均为拉氏量密度 $M^4$（4 维时空）

**620.** 有效截断尺度 $\Lambda_\text{UFT}$，高于此尺度 SM 失效，UFT 几何自由度激活
【统一场动力学】【量纲】✓ $[\Lambda_\text{UFT}]=M$

**621.** 维度正则化：$\int d^dp\to\mu^{4-d}\int d^dp$；$d=4-\epsilon$
【数学恒等式】【量纲】✓ 两侧均为 $M^d$（$\mu^{4-d}$ 为 $M^{4-d}$）

**622.** 极点分离：$\dfrac{1}{\epsilon}-\gamma_E+\ln 4\pi$，$\gamma_E$ 欧拉常数
【数学恒等式】【量纲】✓ 无量纲组合

**623.** 圈修正的几何重求和：$\sum_{n=0}^{\infty}\mathcal L_n(\hat\tau^n)$，$n$ 为圈阶　【OPEN】
【统一场动力学】【量纲】✓ 每阶 $\mathcal L_n$ 为 $M^4$；$\hat\tau$ 无量纲

**624.** 精细结构常数几何 ansatz：$\alpha=f_\alpha(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$　【OPEN】
【标准模型嵌入】【量纲】✓ $\alpha$ 无量纲；$f_\alpha$ 为无量纲函数（形式未定）
【大白话】"$\alpha=1/137$"不再是输入，而是某个几何函数在红外定点的值。函数长什么样，UFT 还没给出——这是 OPEN 的核心困难。

**625.** 弱混合角几何关系：$\sin^2\theta_W=f_\theta(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲

**626.** 汤川耦合几何表达式：$y_f=f_f(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲

**627.** 费米子质量：$m_f=\dfrac{y_fv}{\sqrt2}=\dfrac{v}{\sqrt2}f_f(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$　【OPEN】
【标准模型嵌入】【量纲】✓ $[m_f]=M$；$y_f$ 无量纲、$[v]=M$

**628.** 真空期望值几何来源：$v=f_v(\hat\kappa_0,\hat\tau_0,\hat\omega_0)\,m_P$　【OPEN】
【标准模型嵌入】【量纲】✓ $[v]=M$

**629.** 强耦合 $\alpha_s(M_Z)=f_s(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲

**630.** 强 CP 角 $\theta_\text{QCD}=f_\theta(\hat\kappa_0,\hat\tau_0,\hat\omega_0)$，UFT 预测 $\theta_\text{QCD}\approx0$　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲（角度）
【大白话】强 CP 问题：QCD 允许一个破坏 CP 的角，实验上它小得惊人（$<10^{-10}$）。UFT 声称几何约束天然把它压到 0——这是它相对 SM 的"预言"，但函数形式未定，暂列 OPEN。

**631.** 中微子跷跷板标度 $M_R=f_R(\hat\kappa_0,\hat\tau_0,\hat\omega_0)\,m_P$　【OPEN】
【标准模型嵌入】【量纲】✓ $[M_R]=M$

**632.** 中微子有效质量 $m_\nu=m_D^2/M_R$；$m_D=y_\nu v/\sqrt2$
【标准模型嵌入】【量纲】✓ $[m_\nu]=M^2/M=M$；$[m_D]=M$

### 5.3 数字筛查与贝叶斯推断（633–650）

**633.** 数字筛查目标函数：
$$\chi^2_\text{tot}=\chi^2_\text{SM-particle}+\chi^2_\text{CMB}+\chi^2_{a_e}+\chi^2_{d_e}+\chi^2_\text{grav-wave}$$　【OPEN】
【数学恒等式】【量纲】✓ 各分量无量纲
【大白话】给理论打分的"总罚分"：把 UFT 预言与五类实验数据（粒子谱、CMB、电子 g-2、电子 EDM、引力波）的偏差平方加起来。分越低越像真的。

**634.** $\chi^2_\text{SM-particle}$：电弱、QCD、费米子质量、CKM/PMNS 残差
【标准模型嵌入】【量纲】✓ 无量纲

**635.** $\chi^2_\text{CMB}$：Planck CMB 角功率谱残差
【宇宙学与观测约束】【量纲】✓ 无量纲

**636.** $\chi^2_{a_e}$：电子反常磁矩 $a_e$ 实验残差
【标准模型嵌入】【量纲】✓ 无量纲（$a_e$ 本身无量纲）

**637.** $\chi^2_{d_e}$：电子电偶极矩上限约束残差
【标准模型嵌入】【量纲】✓ 无量纲

**638.** $\chi^2_\text{grav-wave}$：LIGO/Virgo 引力波波形残差
【宇宙学与观测约束】【量纲】✓ 无量纲

**639.** 似然函数：$\mathcal L(\boldsymbol\theta)\propto\exp\left(-\dfrac12\chi^2_\text{tot}(\boldsymbol\theta)\right)$
【数学恒等式】【量纲】✓ 无量纲（正比关系）

**640.** 先验分布 $\pi(\boldsymbol\theta)$：几何参数在 $[0,1]$ 均匀先验（无量纲 Planck 单位）
【数学恒等式】【量纲】✓ 参数无量纲 ⇒ 先验为 $[\theta^{-1}]$ 型概率密度

**641.** 嵌套采样证据：$\mathcal Z=\int\mathcal L(\boldsymbol\theta)\pi(\boldsymbol\theta)\,d^N\theta$
【数学恒等式】【量纲】✓ 无量纲（$d^N\theta$ 无量纲）

**642.** 贝叶斯信息准则 $\mathrm{BIC}=\chi^2+k\ln N_\text{data}$；$k$ 参数数目，$N_\text{data}$ 数据点数
【数学恒等式】【量纲】✓ 无量纲

**643.** AIC 信息准则：$\mathrm{AIC}=\chi^2+2k$
【数学恒等式】【量纲】✓ 无量纲

**644.** 模型比较因子：$\mathcal B_{12}=\mathcal Z_1/\mathcal Z_2$（贝叶斯因子）；$\ln\mathcal B>5$ 强证据支持模型1
【数学恒等式】【量纲】✓ 无量纲

**645.** 参数后验分布 $P(\boldsymbol\theta|D)=\mathcal L(\boldsymbol\theta)\pi(\boldsymbol\theta)/\mathcal Z$
【数学恒等式】【量纲】登记：后验为概率密度，量纲 $[\theta^{-N}]$，依赖参数化

**646.** 后验均值：$\langle\theta_i\rangle=\int\theta_iP(\boldsymbol\theta|D)\,d^N\theta$
【数学恒等式】【量纲】✓ 与 $\theta_i$ 同量纲

**647.** 后验协方差矩阵：$\Sigma_{ij}=\langle\theta_i\theta_j\rangle-\langle\theta_i\rangle\langle\theta_j\rangle$
【数学恒等式】【量纲】✓ $[\theta_i\theta_j]$

**648.** 边际化：$P(\theta_i|D)=\int P(\boldsymbol\theta|D)\prod_{j\neq i}d\theta_j$
【数学恒等式】【量纲】✓ $[\theta_i^{-1}]$

**649.** 轮廓似然：$\chi^2_\text{profile}(\theta_i)=\min_{\theta_{j\neq i}}\chi^2_\text{tot}(\boldsymbol\theta)$
【数学恒等式】【量纲】✓ 无量纲

**650.** 置信区间：$1\sigma:\ \Delta\chi^2\le1$；$2\sigma:\ \Delta\chi^2\le4$
【数学恒等式】【量纲】✓ 无量纲

### 5.4 UFT现象学：精密检验与引力波（651–662）

**651.** 挠率贡献至 $a_e$ 一圈项：$\Delta a_e^{(1)}=C_a\,\dfrac{\tau^2}{m_e^2}$　【OPEN】
【标准模型嵌入】【量纲】✓ $[\tau^2/m_e^2]=M^2/M^2=1$，$a_e$ 无量纲
【大白话】电子在真空里"打转"时会感受到一点时空挠率，让它的反常磁矩多出一份与挠率平方成正比的修正。

**652.** $C_a$ 无量纲几何圈系数，由旋量-挠率耦合(335)导出　【OPEN】
【旋量/克利福德代数】【量纲】✓ 无量纲（若导出则须保持无量纲；被引公式 335 属模块3，待补）

**653.** 两圈挠率修正：$\Delta a_e^{(2)}\propto\tau^4/m_e^4$　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲

**654.** UFT 总反常磁矩：$a_e^\text{UFT}=a_e^\text{QED}+a_e^\text{had}+a_e^\text{weak}+\Delta a_e^{(1)}+\Delta a_e^{(2)}+\dots$　【OPEN】
【标准模型嵌入】【量纲】✓ 各项无量纲

**655.** 电子 EDM：$d_e=C_d\,\dfrac{\tau}{m_e^2}\,\bar\psi\gamma^5\sigma_{ab}\psi$　【OPEN】
【标准模型嵌入】【量纲】登记：$[d_e]=M^{-1}$（自然单位）；$[\tau/m_e^2]=M^{-1}$ 主体相容；完整算符若含场强插入则为 5 维算符（见 728 注），$C_d$ 量纲随口径而变，待机器裁定
【大白话】电偶极矩是 CP 破坏的"探雷器"。挠率是赝张量，天然能生出这项——但实验上限极紧（下条），UFT 的参数空间会被它切掉一大块。

**656.** 实验上限 $|d_e|<1.1\times10^{-29}\ e\cdot\text{cm}$，UFT 参数空间裁剪边界
【宇宙学与观测约束】【量纲】✓ 实验公布值（ACME 2018，非命理数）

**657.** 质子 EDM：$d_p\propto\tau\,\langle\bar q\gamma^5\sigma_{ab}q\rangle$　【OPEN】
【标准模型嵌入】【量纲】登记：$[d_p]=M^{-1}$；强子矩阵元量纲非平凡，比例系数量纲待机器裁定

**658.** 中子 EDM：$d_n\propto\tau\,\langle\bar q\gamma^5\sigma_{ab}q\rangle$，强 CP + 挠率联合贡献　【OPEN】
【标准模型嵌入】【量纲】登记：同 657

**659.** 引力波相位修正（UFT）：$\Delta\Phi_\text{UFT}=\Phi_\text{GR}+\Delta\Phi_\tau(\tau_0,M,z)$　【OPEN】
【宇宙学与观测约束】【量纲】✓ 相位无量纲
【大白话】双黑洞并合放出的引力波，波形相位里会掺进挠率修正项——LIGO/Virgo 测相位灵敏到能当"挠率探测器"用。

**660.** 双星合并引力波相位 $\Phi(f)=\Phi_\text{Newt}(f)+\Phi_{1PN}+\Phi_{2PN}+\dots+\Delta\Phi_\tau$
【经典引力】【量纲】✓ 各阶无量纲

**661.** PN 展开参数 $v/c$，$v$ 双星轨道速度
【经典引力】【量纲】✓ 无量纲

**662.** 挠率引入的后牛顿修正项 $\Delta\Phi_\tau\propto\tau_0M^{n}$　【OPEN】
【宇宙学与观测约束】【量纲】登记：$\Delta\Phi_\tau$ 须无量纲；$[\tau_0M^n]=M^{1+n}$ ⇒ $n$ 与 $\tau_0$ 幂次须配平（或另有隐标度），待机器裁定

### 5.5 UFT现象学：宇宙学与CMB（663–683）

**663.** CMB 标量谱指数 UFT 修正：$n_s^\text{UFT}=n_s^\text{GR}+\Delta n_s(\tau_0,\omega_0)$　【OPEN】
【宇宙学与观测约束】【量纲】✓ $n_s$ 无量纲

**664.** 张量标量比 $r^\text{UFT}=r^\text{GR}+\Delta r(\tau_0,\omega_0)$　【OPEN】
【宇宙学与观测约束】【量纲】✓ 无量纲

**665.** 原初 B 模偏振 $\Delta B_\text{UFT}$ 挠率贡献　【OPEN】
【宇宙学与观测约束】【量纲】✓ B 模功率无量纲

**666.** 宇宙学挠率流体状态方程：$w_\tau=p_\tau/\rho_\tau$
【宇宙学与观测约束】【量纲】✓ 无量纲（$p,\rho$ 均为 $M^4$）

**667.** 动态暗能量：$w_\tau(a)=w_0+w_a(1-a)$；UFT 给出 $w_0,w_a$ 几何表达　【OPEN】
【宇宙学与观测约束】【量纲】✓ $w_0,w_a$ 无量纲

**668.** 弗里德曼方程 UFT：
$$H^2=\frac{8\pi G}{3}\left(\rho_m+\rho_r+\rho_\Lambda+\rho_\tau(\kappa,\tau,\omega)\right)$$　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[H^2]=M^2$；$[G\rho]=M^{-2}\cdot M^4=M^2$
【大白话】宇宙膨胀速率由四样东西决定：物质、辐射、暗能量，外加一份"挠率能量密度"——把时空的扭曲本身当成一种流体喂进弗里德曼方程。

**669.** $\rho_\tau$ 挠率等效能量密度，由 $\mathcal L_\text{UFT}$ 变分导出
【宇宙学与观测约束】【量纲】✓ $[\rho_\tau]=M^4$

**670.** 压强 $p_\tau=\dfrac{\partial\mathcal L_\tau}{\partial\dot\omega}\dot\omega-\mathcal L_\tau$
【宇宙学与观测约束】【量纲】✓ $[p_\tau]=M^4$（标准勒让德变换形式）

**671.** 能量守恒：$\dot\rho_\tau+3H(\rho_\tau+p_\tau)=S_\tau$；$S_\tau$ 挠率能量交换源项　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[\dot\rho]=M^5$；$[H(\rho+p)]=M\cdot M^4=M^5$ ⇒ $[S_\tau]=M^5$

**672.** 宇宙曲率约束：$\Omega_k=-\dfrac{kc^2}{a^2H^2}$；UFT 修正 $\Omega_k^\text{UFT}$　【OPEN】
【宇宙学与观测约束】【量纲】✓ 无量纲

**673.** 密度涨落 $\delta_m=\delta\rho_m/\bar\rho_m$
【宇宙学与观测约束】【量纲】✓ 无量纲

**674.** 线性演化方程：$\ddot\delta_m+2H\dot\delta_m-4\pi G\bar\rho_m\delta_m=\mathcal S_\tau(\delta,\tau)$　【OPEN】
【宇宙学与观测约束】【量纲】✓ 各项 $M^2$；⇒ $[\mathcal S_\tau]=M^2$

**675.** $\mathcal S_\tau$ 挠率诱导涨落源项　【OPEN】
【宇宙学与观测约束】【量纲】✓ 须为 $M^2$（同 674 配平）

**676.** 物质功率谱 $P_m(k,z)=\langle|\delta_m(k,z)|^2\rangle$；UFT 修正 $P_m^\text{UFT}(k,z)$　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[P_m]=M^{-3}$（动量空间功率谱标准量纲）

**677.** 重子声学振荡 BAO 特征尺度 $r_s=\int_0^{z_d}\dfrac{c_s}{H(z)}\,dz$；$c_s$ 声速
【宇宙学与观测约束】【量纲】✓ $[c_s]=M^0$、$[H]=M$ ⇒ $[r_s]=M^{-1}=L$

**678.** $c_s^2=\partial p/\partial\rho$ 流体声速；挠率介质修正 $c_{s,\tau}$　【OPEN】
【宇宙学与观测约束】【量纲】✓ $c_s^2$ 无量纲

**679.** 视界穿越 $k=aH$；$k_*$ 支点尺度
【宇宙学与观测约束】【量纲】✓ $[k]=[aH]=M$

**680.** 原初曲率扰动 $\mathcal R$；功率谱 $P_\mathcal R(k)=A_s(k_*/k)^{n_s-1}$
【宇宙学与观测约束】【量纲】✓ $[P_\mathcal R]=M^{-3}$；$A_s,n_s$ 无量纲

**681.** 非高斯性 $f_\text{NL}$；UFT 几何耦合诱导局部型 $f_\text{NL}$　【OPEN】
【宇宙学与观测约束】【量纲】✓ 无量纲

**682.** 三点关联函数 $\langle\mathcal R(\mathbf k_1)\mathcal R(\mathbf k_2)\mathcal R(\mathbf k_3)\rangle$
【宇宙学与观测约束】【量纲】登记：与 $(2\pi)^3\delta^{(3)}(\mathbf k_1+\mathbf k_2+\mathbf k_3)$ 相配的双谱 $B_\mathcal R$ 量纲 $M^{-6}$，全关联函数另含 $\delta^{(3)}$ 的 $M^{-3}$；待机器裁定

**683.** 局域非高斯：$\mathcal R=\mathcal R_g+\dfrac35f_\text{NL}\left(\mathcal R_g^2-\langle\mathcal R_g^2\rangle\right)$
【宇宙学与观测约束】【量纲】✓ $\mathcal R$ 无量纲，$f_\text{NL}$ 无量纲

### 5.6 黑洞、奇点与反弹（684–692）

**684.** 黑洞熵 UFT 修正：$S_\text{BH}^\text{UFT}=\dfrac{A}{4G}+\Delta S_\tau(\tau|_\text{horizon})$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[A/G]=M^{-2}/M^{-2}=1$ 无量纲；$\Delta S_\tau$ 须无量纲

**685.** 视界处挠率边界条件 $\tau|_{r_h}$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\tau|_{r_h}]=M$

**686.** 霍金温度修正 $T_H^\text{UFT}=T_H^\text{GR}+\Delta T_\tau$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[T_H]=M$

**687.** 黑洞第一定律 UFT：$dM=\dfrac{\kappa_\text{sg}}{8\pi G}dA+\Omega\,dJ+\Phi\,dQ+\Xi\,d\tau_h$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[dM]=M$；$\kappa_\text{sg}/(8\pi G)\cdot dA=M/M^{-2}\cdot M^{-2}=M$；$\Omega\,dJ$ 与 $\Phi\,dQ$ 均为 $M$ ⇒ $[\Xi\,d\tau_h]=M$
【大白话】黑洞力学第一定律本来只有"面积+角动量+电荷"三项；UFT 把"视界挠率"也当成一个热力学变量加了进来——就像给黑洞多记一本"挠率账"。

**688.** $\Xi$ 挠率共轭势；$\tau_h$ 视界挠率强度　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】登记：由 687 配平，若 $[\tau_h]=M$ 则 $[\Xi]=M^0$

**689.** 雷乔杜里 UFT：
$$\dot\theta+\frac13\theta^2+\sigma^2-\omega^2=-u^au^b\mathcal R_{ab}+u^au^bT^c_{ad}T^d_{cb}$$
【爱因斯坦-嘉当挠率引力】【量纲】✓ 各项 $M^2$：$[\dot\theta]=M^2$、$[\mathcal R_{ab}]=M^2$、$[T^c_{ad}T^d_{cb}]=M^2$
【大白话】膨胀与剪切让光线聚焦的方程（奇点定理的引擎）。右边第二项是挠率的"反聚焦"贡献——两个挠率相乘、正号，能把聚焦抵消掉，奇点定理从此不再自动成立。
【符号登记】本条 $\omega$ 为涡率（vorticity），与 UFT 几何角频率标量场同形异义，跨册引用须声明。

**690.** 奇点定理修正：UFT 挠率项可抵消聚焦，允许无奇点宇宙　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】—（定性陈述；机制见 689）

**691.** 反弹宇宙解：$\mathcal H=0,\ \dot H>0$ 在最小尺度因子 $a_\text{min}$；由 $\kappa^2+\tau^2=\omega^2$ 支持　【OPEN】
【宇宙学与观测约束】【量纲】✓ 符号条件；$[\dot H]=M^2$

**692.** 反弹条件：$\rho_\text{tot}+p_\text{tot}<0$ 有效负压强由挠率提供　【OPEN】
【宇宙学与观测约束】【量纲】✓ 符号条件；$[\rho+p]=M^4$
【大白话】大爆炸不是"从零炸开"，而是宇宙先收缩到最小体积、再弹回来——挠率在最小尺度处提供负压强当"弹簧"。

### 5.7 球对称解与太阳系检验（693–698）

**693.** 静态球对称 UFT 度规 $ds^2=-e^{2\nu(r)}dt^2+e^{2\mu(r)}dr^2+r^2d\Omega^2$
【经典引力】【量纲】✓ $[ds^2]=M^{-2}$；$[dt]=[dr]=[r]=M^{-1}$，指数因子无量纲

**694.** 径向约束 $\kappa(r)^2+\tau(r)^2=\omega(r)^2$，径向常微分方程组　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ 各项 $M^2$（自然单位）

**695.** 弱场极限 $e^{2\nu}\approx1-2M/r+\delta\nu_\tau(r)$；$\delta\nu_\tau$ 挠率修正势　【OPEN】
【经典引力】【量纲】✓ $M/r$ 无量纲；$\delta\nu_\tau$ 无量纲
【大白话】离大质量物体很远的地方，UFT 必须退回牛顿引力。多出来的 $\delta\nu_\tau$ 就是挠率在太阳系里留下的"指纹"——水星进动、光线偏折都能卡它。

**696.** 光线偏折角 $\delta\phi^\text{UFT}=\delta\phi_\text{GR}+\Delta\phi_\tau(M,r_0)$　【OPEN】
【经典引力】【量纲】✓ 角度无量纲

**697.** 夏皮罗时间延迟 $\Delta t^\text{UFT}=\Delta t_\text{GR}+\Delta t_\tau$　【OPEN】
【经典引力】【量纲】✓ $[\Delta t]=M^{-1}$

**698.** 行星进动 $\Delta\phi_\text{peri}^\text{UFT}=\Delta\phi_\text{GR}+\Delta\phi_\tau$；水星进动约束　【OPEN】
【经典引力】【量纲】✓ 无量纲

### 5.8 测地线、Lorentz/宇称/CPT与拓扑项（699–714）

**699.** 类光测地线：$\dfrac{d^2x^a}{d\lambda^2}+\Gamma^a_{bc}\dfrac{dx^b}{d\lambda}\dfrac{dx^c}{d\lambda}=0$，$\lambda$ 仿射参数
【经典引力】【量纲】✓ 取 $[\lambda]=M^{-1}$：$[d^2x^a/d\lambda^2]=M$、$[\Gamma]=M$，两侧齐次

**700.** 零条件 $g_{ab}\dfrac{dx^a}{d\lambda}\dfrac{dx^b}{d\lambda}=0$
【经典引力】【量纲】✓ 与 $[ds^2]$ 同型 $M^{-2}$

**701.** 旋量-挠率散射振幅 $\mathcal M(\psi\to\psi)$，单挠率交换　【OPEN】
【标准模型嵌入】【量纲】登记：2→2 振幅标准归一化下 $[\mathcal M]=M^0$；挠率交换振幅的具体量纲随归一化声明，待机器裁定

**702.** 费曼规则：挠率顶点 $\propto T_{abc}\bar\psi\gamma^{[a}\gamma^b\gamma^{c]}\psi$（来自 335）
【旋量/克利福德代数】【量纲】✓ $[T_{abc}]=M$、$[\bar\psi\gamma\gamma\gamma\psi]=M^3$ ⇒ 顶点算子 $M^4$，耦合系数可无量纲（被引公式 335 属模块3，待补）

**703.** 挠率传播子 $D_T(p)$　【OPEN】
【标准模型嵌入】【量纲】登记：若挠率场带动能项 $(\partial T)^2$（$[T]=M$），则 $[D_T]=M^{-2}$；归一化声明待机器裁定

**704.** 挠率介导的中微子散射 $\nu+e\to\nu+e$，UFT 新贡献　【OPEN】
【宇宙学与观测约束】【量纲】✓ 截面 $M^{-2}$（随振幅归一化）

**705.** 宇宙射线高能截断修正：UFT 色散 $v_g(k)$ 改变 GZK 阈值　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[v_g]=M^0$

**706.** GZK 阈值 $E_\text{GZK}\approx5\times10^{19}\,\text{eV}$；UFT 修正 $\Delta E_\text{GZK}$　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[E]=M$（$5\times10^{19}$ eV 为实验观测锚，非命理数）

**707.** 洛伦兹破缺检验：UFT 在低能保持洛伦兹不变；挠率是几何，不是 Lorentz-violating 背景
【统一场动力学】【量纲】—（结构性陈述）

**708.** 局域洛伦兹不变：$\Lambda\in\mathrm{SO}(1,3)$，$\psi\mapsto U(\Lambda)\psi$；$\omega,\kappa,\tau$ 为洛伦兹标量
【旋量/克利福德代数】【量纲】—（结构性陈述）

**709.** 宇称检验：挠率张量 $T^a_{bc}$ 是赝张量，自然引入 P 破坏；CPT 保持不变
【统一场动力学】【量纲】—（结构性陈述）

**710.** CP 破坏源：$T\wedge\mathcal R$ 拓扑项 + 挠率-旋量赝标耦合（EDM 来源）
【统一场动力学】【量纲】登记：见 712 注（$T\wedge\mathcal R$ 为 $M^3$ 型 4-形式）

**711.** 拓扑不变量 Pontryagin 密度：$\mathcal P=\dfrac12\mathrm{tr}(\mathcal R\wedge\mathcal R)$
【数学恒等式】【量纲】✓ $[\mathcal P]=M^4$（4-形式；其积分无量纲）

**712.** UFT 拓扑项：$\mathcal L_\text{top}=\zeta\mathcal P+\xi\,T\wedge\mathcal R$　【OPEN】
【统一场动力学】【量纲】登记：$[\mathcal P]=M^4$ 而 $[T\wedge\mathcal R]=M^3$（$[T]=M$、$[\mathcal R]=M^2$）⇒ 两项相差一个质量量纲；若 $\zeta,\xi$ 均无量纲（见 713）则不可加，须 $\xi$ 携带 $M$ 或补 $1/\Lambda_\text{UFT}$ 型标度；待机器裁定

**713.** $\zeta,\xi$ 无量纲拓扑耦合系数，由基础几何约束导出　【OPEN】
【统一场动力学】【量纲】登记：若坚持无量纲声明，则与 712 的量纲配平冲突（差 $M^1$）；待机器裁定

**714.** 路径积分拓扑求和：$\sum_{M,\ \text{spin structures}}e^{iS_\text{UFT}+i\int\mathcal L_\text{top}}$
【统一场动力学】【量纲】✓ 指数无量纲（作用量无量纲）

### 5.9 瞬子、磁单极与拓扑缺陷（715–726）

**715.** 瞬子解 $\mathcal R\wedge\mathcal R\neq0$；挠率瞬子 $T\neq0$　【OPEN】
【统一场动力学】【量纲】—（解的存在性陈述）

**716.** 瞬子作用量 $S_\text{inst}\propto m_P^2\ell_P^2\sim\mathcal O(1)$（自然单位）
【统一场动力学】【量纲】✓ $[m_P^2\ell_P^2]=M^2\cdot M^{-2}=1$

**717.** 手征对称性瞬子破缺；UFT 挠率瞬子附加手征源　【OPEN】
【标准模型嵌入】【量纲】—（机制陈述）

**718.** 杨-米尔斯瞬子：$\mathcal F\wedge\mathcal F$，QCD $\theta$ 项来源
【标准模型嵌入】【量纲】✓ $[\mathcal F]=M^2$ ⇒ 4-形式 $M^4$

**719.** 磁单极拓扑荷 $q_m=\dfrac{1}{4\pi}\int_SF$
【数学恒等式】【量纲】✓ 无量纲（$[F]=M^2$、面积 $M^{-2}$）

**720.** 狄拉克量子化 $q_eq_m=n/2,\ n\in\mathbb Z$
【数学恒等式】【量纲】✓ 无量纲

**721.** UFT 磁单极解带挠率背景：$T(r)\neq0$，球对称拓扑孤子　【OPEN】
【统一场动力学】【量纲】✓ $[T(r)]=M$

**722.** 孤子能量 $E_\text{soliton}=\int T_{00}\sqrt g\,d^3x$
【统一场动力学】【量纲】✓ $[T_{00}]=M^4$、$d^3x=M^{-3}$ ⇒ $[E]=M$

**723.** 孤子质量 $M_\text{sol}\propto m_P/\alpha$，大质量普朗克尺度孤子　【OPEN】
【统一场动力学】【量纲】✓ $[M_\text{sol}]=M$

**724.** 拓扑缺陷：宇宙弦 $\mu_\text{string}\propto m_P^2$；UFT 挠率修正张力　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[\mu]=M^2$（张力）

**725.** 畴壁面密度 $\sigma_\text{wall}\propto m_P^3$
【宇宙学与观测约束】【量纲】✓ $[\sigma]=M^3$

**726.** 单极子丰度约束：$\Omega_\text{monopole}<10^{-5}$，宇宙学上限
【宇宙学与观测约束】【量纲】✓ 无量纲

### 5.10 有效场论、幺正性与渐近安全（727–750）

**727.** 有效场论幂次计数：算子维数 $[O]=d$；高维算子 $\propto\Lambda_\text{UFT}^{4-d}$
【数学恒等式】【量纲】✓ 标准计数：$[\Lambda_\text{UFT}^{4-d}O]=M^{4-d}\cdot M^d=M^4$

**728.** 6 维算子例子：$\bar\psi\sigma_{ab}\psi\,\mathcal R^{ab}$，$\bar\psi\gamma_5\sigma_{ab}\psi\,T^{ab}$（EDM 算子）
【标准模型嵌入】【量纲】登记：按标准质量量纲计数 $[\bar\psi\psi]=M^3$、$[\mathcal R^{ab}]=M^2$、$[T^{ab}]=M$、$[\sigma_{ab}]=M^0$ ⇒ 两项分别为 5 维与 4 维算符；条目所标"6 维"若按指标数（6/6）计，则与 727 的质量量纲计数口径不同，待机器裁定

**729.** 8 维算子：$T_{abc}T^{abc}\mathcal R$，高阶几何修正　【OPEN】
【标准模型嵌入】【量纲】登记：标准计数 $[T^2\mathcal R]=M\cdot M\cdot M^2=M^4$（4 维算符）；"8 维"疑为指标数口径（3+3+2），同 728 注，待机器裁定

**730.** 有效作用量按 $1/\Lambda_\text{UFT}$ 展开：$\Gamma_\text{eff}=\Gamma_0+\dfrac{1}{\Lambda_\text{UFT}^2}\Gamma_2+\dfrac{1}{\Lambda_\text{UFT}^4}\Gamma_4+\dots$
【数学恒等式】【量纲】✓ $\Gamma_\text{eff}$ 无量纲（作用量）；$[\Gamma_2]=M^2$、$[\Gamma_4]=M^4$

**731.** 正则化尺度 $\Lambda_\text{UFT}$：UFT 新自由度开始激发的能标
【统一场动力学】【量纲】✓ $[\Lambda_\text{UFT}]=M$

**732.** 低能定理：所有低能可观测量可以展开为 $\tau/\Lambda_\text{UFT}$ 幂级数
【统一场动力学】【量纲】✓ 无量纲小参数

**733.** 散射截面高能极限：$\sigma(E)\sim1/E^2$；UFT 修正 $\Delta\sigma(\tau,E)$　【OPEN】
【数学恒等式】【量纲】✓ $[\sigma]=M^{-2}$

**734.** 幺正性边界：$|\mathcal M|^2<16\pi s$；UFT 必须满足幺正性在所有能标
【数学恒等式】【量纲】登记：标准 2→2 归一化下 $[\mathcal M]=M^0$、$[s]=M^2$，两侧相差 $M^2$；须声明振幅归一化口径（或改为无量纲形式 $|\mathcal M|^2\lesssim16\pi$），待机器裁定

**735.** $s=(p_1+p_2)^2$ 曼德尔斯坦不变量
【数学恒等式】【量纲】✓ $[s]=M^2$

**736.** 幺正截断能标 $\Lambda_\text{unit}$，高于此微扰论失效
【统一场动力学】【量纲】✓ $[\Lambda_\text{unit}]=M$

**737.** 色散关系：$\mathrm{Re}\mathcal M(s)=\dfrac{1}{\pi}\mathcal P\int_{s_0}^{\infty}\dfrac{\mathrm{Im}\mathcal M(s')}{s'-s}ds'$
【数学恒等式】【量纲】✓ 若 $\mathcal M$ 无量纲则两侧无量纲（$ds'/(s'-s)$ 无量纲）

**738.** 光学定理：$\sigma_\text{tot}=\dfrac{1}{s}\mathrm{Im}\mathcal M(s,t=0)$
【数学恒等式】【量纲】✓ $[\sigma_\text{tot}]=M^{-2}$

**739.** 因果性：$\mathcal M(t)$ 无极点在非物理区域，UFT 因果性核验
【数学恒等式】【量纲】—（结构性陈述）

**740.** 解析性 + 幺正性 + 交叉对称约束 S 矩阵
【数学恒等式】【量纲】—（结构性陈述）

**741.** S 矩阵元 $S_{fi}=\delta_{fi}+i(2\pi)^4\delta^{(4)}(\textstyle\sum p)\mathcal M_{fi}$
【数学恒等式】【量纲】✓ $\delta^{(4)}$ 为 $M^{-4}$；$\mathcal M$ 无量纲 ⇒ 全式无量纲

**742.** 交叉对称：$\mathcal M(s,t,u)=\mathcal M(u,t,s)$，替换入射/出射粒子
【数学恒等式】【量纲】✓ 不变量均为 $M^2$

**743.** 重整化可核查：UFT 计数 $\mathcal L_\text{UFT}$ 表面发散度 $D=4-\sum d_\text{op}$　【OPEN】
【统一场动力学】【量纲】✓ $D$ 无量纲

**744.** 表面发散度 $D$；$D\ge0$ 紫外发散；$D<0$ 收敛
【数学恒等式】【量纲】✓ 无量纲判据

**745.** 引力本身是非重整化，UFT 依靠 UV 不动点渐近安全方案
【统一场动力学】【量纲】—（方案性陈述）

**746.** Wetterich 流：$\partial_k\Gamma_k=\dfrac12\mathrm{Tr}\left[(\Gamma_k^{(2)}+\mathcal R_k)^{-1}\partial_k\mathcal R_k\right]$
【统一场动力学】【量纲】✓ 标准精确流方程；$\Gamma_k$ 为无量纲有效作用量，$\mathcal R_k$ 为以截断 $k$（$M$）标度的调节器

**747.** 安全不动点：$\partial_k\Gamma_k|_*=0$，所有 β 函数归零
【统一场动力学】【量纲】—（不动点条件）

**748.** 临界指数 $\theta_i=-\mathrm{eigenval}(\mathbf M_{ij}|_*)$；正 $\theta_i$ 为相关算子
【统一场动力学】【量纲】✓ 无量纲

**749.** 相关算子数目 = 独立低能参数数目
【统一场动力学】【量纲】—（计数陈述）

**750.** UFT 猜想：仅 3 个基础几何相关算子（$\hat\kappa,\hat\tau,\hat\omega$），其余 SM 参数全部派生　【OPEN】
【统一场动力学】【量纲】✓ 三者无量纲
【大白话】整个 #49 的"终极大单"：如果成立，标准模型二十多个"手动拧"的常数其实只是 3 个无量纲几何数在红外定点的投影。参数约化从此从"愿景"变成"可证伪命题"——反过来说，只要有一个 SM 参数证伪了这 3 数投影，猜想即倒。

### 5.11 质量层级、真空稳定性与欧氏/热场论（751–768）

**751.** 相空间体积：$\Omega(\boldsymbol\theta)=\int d^N\theta$ 参数空间体积
【数学恒等式】【量纲】登记：量纲依赖参数化（无量纲参数下为 $M^0$）

**752.** 奥卡姆因子：$\mathcal O=\dfrac{\mathcal Z_\text{UFT}}{\mathcal Z_\text{SM}}\dfrac{\Omega_\text{SM}}{\Omega_\text{UFT}}$，衡量参数精简度
【数学恒等式】【量纲】✓ 无量纲

**753.** 预测能力判据：$\dfrac{\text{Number of predictions}}{\text{Number of input parameters}}$；UFT 目标 $\gg1$
【数学恒等式】【量纲】✓ 无量纲比值

**754.** 普朗克单位无量纲可观测量：$\hat m=m/m_P,\ \hat\alpha=\alpha$
【数学恒等式】【量纲】✓ 无量纲

**755.** 无量纲关系：$\hat m_e=F_e(\hat\kappa_*,\hat\tau_*,\hat\omega_*)$，无额外输入　【OPEN】
【统一场动力学】【量纲】✓ 无量纲

**756.** 质量层级问题：UFT 方案——希格斯质量由几何约束保护，无二次发散精细调节　【OPEN】
【标准模型嵌入】【量纲】—（机制性陈述）

**757.** 希格斯质量 $m_h=125\,\text{GeV}$；UFT 几何预测 $m_h=F_h(\hat\kappa_*,\hat\tau_*,\hat\omega_*)$　【OPEN】
【标准模型嵌入】【量纲】✓ $[m_h]=M$（125 GeV 为实验锚）

**758.** 希格斯自耦合 $\lambda=m_h^2/(2v^2)$，几何导出　【OPEN】
【标准模型嵌入】【量纲】✓ 无量纲

**759.** 电弱真空稳定性：有效势 $V_\text{eff}(\phi,\mu)$；UFT 修正稳定性边界　【OPEN】
【标准模型嵌入】【量纲】✓ $[V_\text{eff}]=M^4$

**760.** 亚稳态真空寿命 $\tau_\text{vac}\propto e^B$，$B$ 隧穿作用量；挠率修正 $B$　【OPEN】
【标准模型嵌入】【量纲】✓ $[\tau_\text{vac}]=M^{-1}$；$B$ 无量纲

**761.** 隧穿解：欧氏引力瞬子，带挠率背景 $\tau_E\neq0$　【OPEN】
【统一场动力学】【量纲】✓ $[\tau_E]=M$

**762.** 欧氏作用量 $S_E=-\int\mathcal L_\text{UFT}\sqrt g\,d^4x$
【数学恒等式】【量纲】✓ 无量纲

**763.** 欧氏约束：$\kappa_E^2+\tau_E^2=\omega_E^2$，欧氏几何版本　【OPEN】
【统一场动力学】【量纲】✓ 各项 $M^2$

**764.** 欧氏自旋联络 $\omega_{ab}^E$；欧氏克利福德代数 $\mathrm{Cl}(4)$
【旋量/克利福德代数】【量纲】✓ $[\omega_{ab}^E]=M$

**765.** 欧氏狄拉克算子 $\not\nabla_E=\gamma_E^a\nabla_a^E$
【旋量/克利福德代数】【量纲】✓ $[\not\nabla_E]=M$

**766.** 热场论：$t\to-i\beta$，$\beta=1/T$ 逆温度
【数学恒等式】【量纲】✓ $[\beta]=M^{-1}$

**767.** 配分函数热场：$\mathcal Z(\beta)=\mathrm{Tr}\,e^{-\beta\hat H}$
【数学恒等式】【量纲】✓ 无量纲

**768.** 自由能 $F=-T\ln\mathcal Z$；熵 $S=-\partial F/\partial T$；内能 $U=F+TS$
【数学恒等式】【量纲】✓ $[F]=[U]=M$；$[S]=M^0$

### 5.12 QGP、格点与数值方法（769–781）

**769.** 高温极限 $T\gg\Lambda_\text{QCD}$ 夸克胶子等离子体；UFT 几何修正物态方程　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[T]=M$

**770.** 格点 QCD+UFT：$\langle\bar qq\rangle_\tau$ 挠率修正手征凝聚　【OPEN】
【标准模型嵌入】【量纲】✓ $[\langle\bar qq\rangle]=M^3$

**771.** 格点离散联络 $\Gamma^a_{bc,\text{latt}}$；离散挠率 $T^a_{bc,\text{latt}}$
【数学恒等式】【量纲】✓ 同连续对应物（$M$）

**772.** Regge calculus UFT 离散作用量：$S_R^\text{UFT}=S_R+\sum_\text{simplex}f(\kappa,\tau,\omega)V_\text{simplex}$　【OPEN】
【数学恒等式】【量纲】登记：$S_R$ 无量纲；须使单项无量纲（亏角无量纲、4-单纯形体积 $M^{-4}$），$f(\kappa,\tau,\omega)$ 的具体量纲待机器裁定

**773.** $V_\text{simplex}$ 单纯形体积；亏角 $\delta_h$ 铰链曲率
【数学恒等式】【量纲】✓ $[V_\text{simplex}]=M^{-4}$；$\delta_h$ 无量纲

**774.** 数值仿真误差估计：$\epsilon_\text{num}=\epsilon_\text{trunc}+\epsilon_\text{round}+\epsilon_\text{grid}$
【数学恒等式】【量纲】✓ 相对误差无量纲

**775.** 收敛判据：$\chi^2_{n+1}-\chi^2_n<\epsilon_\text{tol}$，$\epsilon_\text{tol}$ 容差
【数学恒等式】【量纲】✓ 无量纲

**776.** RK4 稳定性条件：$\Delta t<C\Delta x$（CFL 条件；$C$ 库朗数）
【数学恒等式】【量纲】✓ $[\Delta t]=[\Delta x]=M^{-1}$

**777.** FDTD Yee 网格稳定性：$c\Delta t<\dfrac{1}{\sqrt{(1/\Delta x)^2+(1/\Delta y)^2+(1/\Delta z)^2}}$
【数学恒等式】【量纲】✓ 两侧均为 $M^{-1}$

**778.** ADM-BSSN 约束监视：$\mathcal H(t),\mathcal M_i(t)$；约束违反范数 $\|\mathcal H\|=\int|\mathcal H|\sqrt h\,d^3x$
【爱因斯坦-嘉当挠率引力】【量纲】✓ 哈密顿约束 $M^2$；范数积分 $M^2\cdot M^{-3}=M^{-1}$（归一化约定）

**779.** 约束阻尼项：$\partial_t\mathcal H=-\eta\mathcal H$，抑制数值约束漂移
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\eta]=M$

**780.** 引力波提取：纽曼-彭罗斯标量 $\Psi_4$；$\Psi_4\propto\ddot h_+$
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\Psi_4]=M^2$

**781.** NP 旋系数 $\Psi_0,\Psi_1,\Psi_2,\Psi_3,\Psi_4$；UFT 带挠率修正 NP 方程组　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ 各 $\Psi_i$ 为 Weyl 分量型曲率标量 $M^2$

### 5.13 纽曼-彭罗斯形式与初值问题（782–791）

**782.** 类光基 $\{l,n,m,\bar m\}$；$l\cdot n=-1,\ m\cdot\bar m=1$
【旋量/克利福德代数】【量纲】✓ 标量积无量纲

**783.** 纽曼彭罗斯曲率分量 $\mathcal R_{abcd}$ 投影到类光四元组
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\mathcal R_{abcd}]=M^2$

**784.** 旋系数 $\gamma_{ijk}$，带挠率修正　【OPEN】
【旋量/克利福德代数】【量纲】✓ 连接型旋系数为 $M$

**785.** 特征初值问题：柯西数据 $\{h_{ab},K_{ab},T^a_{bc},\omega\}$ 在 $\Sigma_t$
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[h_{ab}]=M^0$（3-度规无量纲）、$[K_{ab}]=M$、$[T^a_{bc}]=M$、$[\omega]=M$

**786.** 初值约束：哈密顿约束 $\mathcal H=0$；动量约束 $\mathcal M_a=0$；挠率约束 $\kappa^2+\tau^2=\omega^2$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ 约束分别为 $M^2$ / $M^2$ / $M^2$ 型

**787.** 初值求解方案：共形薄夹层方法，UFT 扩展版本　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】—（方法性陈述）

**788.** 共形因子 $\psi$；$h_{ab}=\psi^4\bar h_{ab}$
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\psi]=M^0$（3-度规无量纲口径）

**789.** 椭圆方程求解：$\Delta\psi=\dots$；挠率作为源项　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\Delta\psi]=M^2$

**790.** 自适应网格细化 AMR：细化判据 $\nabla\Psi_4>\epsilon_\text{AMR}$，引力波梯度
【数学恒等式】【量纲】✓ $[\nabla\Psi_4]=M^3$；$\epsilon_\text{AMR}$ 为阈值（约定归一化）

**791.** 多物理场耦合：度规、挠率、$\omega$ 标量、旋量场同步演化
【爱因斯坦-嘉当挠率引力】【量纲】—（方案性陈述）

### 5.14 共振、QNM、黑洞影子与联合观测约束（792–799）

**792.** 波包散射：几何 $\omega$ 波包与引力曲率散射，共振态 $\omega_\text{res}$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\omega_\text{res}]=M$

**793.** 共振截面 $\sigma_\text{res}\propto\dfrac{\Gamma^2}{(E-E_\text{res})^2+\Gamma^2/4}$；$\Gamma$ 宽度
【数学恒等式】【量纲】登记：条目省略标准 Breit-Wigner 的 $1/k^2$ 前置因子（否则两侧差 $M^{-2}$）；$[\Gamma]=[E]=M$，待机器裁定

**794.** 准正常模 QNM：黑洞扰动 $\Psi\sim e^{-i\omega t-\Gamma t}$；UFT 修正 QNM 频率　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\omega]=[\Gamma]=M$

**795.** QNM 本征值 $\omega_\text{QNM}=\omega_\text{QNM}^\text{GR}+\Delta\omega_\tau(M,a,\tau_h)$　【OPEN】
【爱因斯坦-嘉当挠率引力】【量纲】✓ $[\omega_\text{QNM}]=M$

**796.** 黑洞影子：$r_\text{shadow}$；UFT 修正 $r_\text{shadow}^\text{UFT}$，EHT 观测约束　【OPEN】
【宇宙学与观测约束】【量纲】✓ $[r_\text{shadow}]=M^{-1}$

**797.** EHT 残差 $\chi^2_\text{EHT}$，黑洞影像轮廓约束挠率参数
【宇宙学与观测约束】【量纲】✓ 无量纲

**798.** 参数退化：$\tau_0\leftrightarrow M$；MCMC 后验轮廓识别退化方向
【数学恒等式】【量纲】—（结构性陈述：退化方向识别）

**799.** 组合观测断简并：CMB+引力波+EHT+EDM 联合似然
【宇宙学与观测约束】【量纲】—（方案性陈述）

### 5.15 模块小结（800）

**800.** 模块小结恒等式：UFT 底层几何公理 $\boldsymbol{\kappa^2+\tau^2=\omega^2}$，在 UV 不动点生成全部 SM 参数与引力动力学　【OPEN】
【统一场动力学】【量纲】✓ 自然单位齐次（SI：$\kappa^2+\tau^2=\omega^2/c^2$，即公式 183）
【大白话】把 601–800 压成一句话：时空几何有个"毕达哥拉斯约束"，它在普朗克标度被顶满、在红外定点"投影"出我们看见的所有常数和力。这句话是 UFT 的脊梁，也是它最大的赌注——整模块的 OPEN 标记，押的都是它。

## 三、量纲审计与机器裁定（601–800，已跑机）

本版审计方式为**内嵌标记**：凡标 `✓` 者为教科书级齐次性（定义式、无量纲比值、拉氏量密度 $M^4$ 等）；凡标 `登记` 者为发现口径或量纲疑点，按 openuft 纪律留待机器裁定。

**机器裁定已执行**（2026-10-15）：脚本 `_p49_dim601800_calc.py` → `_p49_dim601800_data.json` / `_p49_dim601800_out.txt`（同目录；纯标准库，Fraction 四元组 $(M,L,T,Q)$，自然单位质量维 $\mathrm{mdim}=M-L-T$）。自检守卫 **12/12 通过**（$[G]=M^{-2}$、$[\ell_P]=M^{-1}$、$[m_P]=M$、$[t_P]=M^{-1}$、$[E_P]=M$、拉氏密度 $M^4$、$\kappa^2+\tau^2$ 与 $\omega^2$ 同为 $M^2$、曲率 $M^2$、挠率 $M$、旋量 $3/2$、规范场 $M$、$\delta^{(3)}(k)=M^{-3}$）。裁定计数：**PASS 2 / FAIL 4 / CORRECTED 1 / MISMATCH 1 / BOUNDARY 4**（12 条，覆盖原登记 11 类）。原登记项与机器读数对照：

| 编号 | 原登记项 | 机器裁定 | 机器读数 | 最小修法（**不代选**） |
|---|---|---|---|---|
| F1 | **612** 参数向量 | BOUNDARY | 11 项、去重后 10 个互异名（$\alpha$ 重复 1 次）；4 项无量纲 + 7 项质量维 1 | 向量非方程，无齐次性要求；$\alpha$ 重复是否为笔误由作者裁定 |
| F2 | **662** $\Delta\Phi_\tau\propto\tau_0M^n$ | **FAIL（原文写法）** | $\mathrm{mdim}(\tau_0)=1$、$\mathrm{mdim}(M)=1$ ⇒ $1+n=0$ ⇒ **$n=-1$** | ① $\Delta\Phi_\tau\propto\tau_0/M$；② 显式引入标度 $\tau_0M^n/\Lambda^{n+1}$ |
| F3 | **680/682** 三点函数 | PASS（内部自洽） | $\mathrm{mdim}(\mathcal R(k))=-3$，$\langle\mathcal R\mathcal R\mathcal R\rangle=-9$，$\delta^{(3)}=-3$ ⇒ $B_\mathcal R=M^{-6}$、$P_\mathcal R=M^{-3}$ | 登记解除条件：显式声明 Fourier 约定 $\mathcal R(k)=\int d^3x\,e^{-ikx}\mathcal R(x)$ |
| F4 | **645/751** 后验密度 / 参数空间体积 | BOUNDARY | 无量纲参数下均为 $M^0$；含质量维 $d_i$ 参数时 $P$ 为 $M^{-\sum d_i}$ | 无参数化声明不可裁定；常规约定，备查 |
| F5 | **701/703** 振幅 / 挠率传播子 | BOUNDARY | 标准 2→2 口径 $[\mathcal M]=M^0$；挠率正则动能 $(\partial T)^2$ ⇒ $[D_T]=M^{-2}$ | 登记解除条件：作者声明振幅归一化 |
| F6 | **710/712/713** $\mathcal L_\text{top}=\zeta\mathcal P+\xi\,T\wedge\mathcal R$ | **FAIL（$\xi$ 无量纲版本）** | $[\mathcal P]=M^4$、$[T\wedge\mathcal R]=M^3$、需求 $M^4$ ⇒ $[\zeta]=0$、**$[\xi]=M$** | ① $\xi\to\hat\xi\,m_P$；② 改 Nieh–Yan 型 $T^a\wedge T_a-\mathcal R_{ab}\wedge e^a\wedge e^b$（$M^2$，系数 $M^2$）；③ 保留 $T\wedge\mathcal R$ 并声明 $\xi$ 带质量维 |
| F6b | **713** $\zeta,\xi$ 均无量纲 | FAIL（条件性：仅当 712 保留 $T\wedge\mathcal R$ 时） | 与 F6 差一个质量幂次 | 同上三选一 |
| F7 | **728/729** "6 维 / 8 维" | **MISMATCH（口径冲突）** | $[\bar\psi\psi]=3$ ⇒ 算子一 $=3+2=5$、算子二 $=3+1=4$；"6/8" 是指标数（3+3 / 3+3+2） | 同一节内不得混用「指标数」与「质量量纲」两套计数；按 727 口径应记 5 维与 4 维 |
| F8 | **734** $|\mathcal M|^2<16\pi s$ | **FAIL（原文写法）** | 标准口径下 LHS $=M^0$，RHS $=M^2$，**差 $M^2$** | 改无量纲分波形式 $|a_l|\le1$（或分波归一后的 $|\mathcal M|^2\le16\pi$） |
| F9 | **772/773** Regge 作用量 | PASS（条件性） | $[V_\text{simplex}]=M^{-4}$、$S_R$ 无量纲 ⇒ **$[f]=M^4$** | $f=\omega^4$ 或 $f=(\kappa^2+\tau^2)^2$ 自洽；$f=\kappa^2+\tau^2$（$M^2$）不自洽 |
| F10 | **793** Breit–Wigner | **CORRECTED** | $[\sigma]=M^{-2}$，原文 RHS 为 $M^0$，缺口 $M^{-2}$ ⇒ 由 $1/k^2$ 补齐 | $\sigma_\text{res}\propto\dfrac{1}{k^2}\dfrac{\Gamma^2}{(E-E_\text{res})^2+\Gamma^2/4}$ |
| F11 | **689** 涡率 $\omega$ | BOUNDARY（符号台账） | 涡率与几何角频率同为 $\mathrm{mdim}=1$；$\sigma^2,\omega^2$ 同为 $M^2$（雷乔杜里项齐次） | 无量纲缺陷；跨册引用须声明是哪一个 $\omega$ |

机器裁定只覆盖**量纲与口径**维度，不判定物理真伪；凡给出多条最小修法者**一律不代选**，按 openuft 纪律留给作者裁决。

## 四、待补区间与后续

- 公式 1–306：源文在会话上下文中压缩丢失（已全盘检索工作区无副本），需重新提供后补录；
- 公式 307–600：未提供；
- 公式 **801–1000（模块6：UFT 自洽性审计、悖论消解、量子几何边界、总结公理体系 + 开放猜想清单）**：用户已发出，**但该段源文随上下文压缩丢失，磁盘与工作区均无副本**（已检索 `07_统一场方程` 全目录与全库关键词，零命中）。按本册"不编造"红线，**不据目录大纲反推公式**，待用户重新粘贴后按同款体例（LaTeX 清洗 → 类别标签 → 内嵌量纲审计 → OPEN 标记 → 大白话 → 机器裁定）补录；
- 本区间（601–800）OPEN 公式共 **92 条**；量纲侧已跑机（见 §三），物理/可证伪侧裁定仍待脚本接线后逐条给出 PASS/FAIL/BOUNDARY/CORRECTED。

**红线**：数学自洽 ≠ 实验证实；本册所有 OPEN 公式均为候选假设；登记项不得读作已裁定结论；无数字命理。
