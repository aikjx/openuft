# 判定：TUFT V3.5 增补 · 外部评审整理与逐点裁决

- **来料**：TUFT V3.5 增补（Part B：复相位 $\Rightarrow$ 宇称破缺 $\Rightarrow$ 手征不对称；Part C：协方差传播 / 数值误差 / 95% 区间 / 证伪阈值；Part D：MCMC 采样）
- **定位**：对增补的**核心推导闭合性**与**统计自洽性**逐点裁决（判定册）；保留骨架，不推倒重来
- **日期**：2026-10-04
- **红线**：数学自洽 ≠ 物理真实。本册只裁决「推导是否闭合 / 数值是否由公式导出 / 声称是否过强」，不物理判决。

---

## 〇、一句话结论

**这份 V3.5 增补还不能判定为「数学证明正确」。** 两块核心各有硬伤：

- **Part B**：「复相位 $\Rightarrow$ 宇称破缺 $\Rightarrow$ 手征不对称」链**不成立**——决定性代数结果是 $\mathcal A_{\rm chiral}\equiv 0$，复相位只能给 $g_R=g_L^*$ 而非 $|g_R|\neq|g_L|$；
- **Part C**：协方差传播框架**正确**，但 $\sigma_{\lambda/\lambda}$、$\sigma_{\Delta a_e}=0.65\times10^{-13}$、UHECR 的 $\sigma=0.21\times10^{19}\ {\rm eV}$、95% 区间与证伪阈值**均未从现有公式实际推导出来**。

保留项：$\theta=\operatorname{atan2}(\tau,\kappa a)$、$\Omega_R=\lambda\cos3\theta$、三倍角坐标化、量纲结构、协方差传播框架、「必须给出可证伪观测量」的路线。但核心链须重构为：

$$\boxed{\text{明确 }L/R\ \text{Lorentz 算符}\ \Rightarrow\ C_L\neq C_R\ \Rightarrow\ P\ \text{破缺}\ \Rightarrow\ \beta\ \text{衰变角相关}}$$

而复相位 $\phi_0$ 另行负责干涉 / CP 型相位效应。

---

## 一、总审计裁决表

| 模块 | 判定 | 核心原因 |
|---|---|---|
| $\theta=\operatorname{atan2}(\tau,\kappa a)$，$\tau\to-\tau\Rightarrow\theta\to-\theta$ | 🟢 局部正确 | 除 $\operatorname{atan2}$ 支割线外成立 |
| $\cos3\theta$ 转回 $(\kappa a,\tau)$ | 🟢 正确 | 三倍角公式完全成立 |
| 量纲分析 | 🟢 基本正确 | — |
| 若 $\lambda$ 无量纲线性、$\phi(\theta)$ 满足 $\phi(-\theta)=-\phi(\theta)$ | 🔴 一般错误 | 只有特殊条件才成立 |
| 弱域边界「相位光滑」 | 🔴 错误 | 当前分段定义一般甚至不连续 |
| $\Omega(-\theta)=\Omega^*(\theta)\Rightarrow P$ 破缺 | 🔴 不成立 | 这是变换关系，不等于对称性破缺 |
| $P_L,P_R$ 定义 | 🟢 正确 | — |
| $g_L=e^{i\phi},\ g_R=e^{-i\phi}\Rightarrow$ 手征不对称 | 🔴 明确错误 | $\mathcal A_{\rm chiral}\equiv0$ |
| 协方差一阶传播公式 | 🟢 正确 | $\sigma_y^2=J_y\Sigma_pJ_y^T$ |
| $\sigma_\lambda/\lambda\simeq0.0076$ | 🟡 算术可成立 | 只有 $\lambda\propto\alpha_s$ 时才能这样传递 |
| $\sigma_{\Delta a_e}=0.65\times10^{-13}$ | 🔴 尚无推导 | 未由 Jacobian 与协方差算出 |
| UHECR $\sigma=0.21\times10^{19}\ {\rm eV}$ | 🔴 尚无推导 | 同上 |
| 「超出 95% 区间即证伪」 | 🟠 表述过强 | 应为在给定假设下的统计排斥 |
| 三组观测「独立」 | 🔴 当前不正确 | $\Delta a_e$ 与 UHECR 至少共享 $\lambda$ |
| emcee「嵌套采样」 | 🔴 技术术语错误 | emcee 是 ensemble MCMC，不是 nested sampling |

---

## 二、Part B · 宇称 / 手征推导闭合性（复相位 ≠ 手征性）

### B-01 可直接算出的代数错误：$\phi(-\theta)\neq-\phi(\theta)$

原定义 $\phi(\theta)=\phi_0\frac{\theta-\theta_{W,c}}{\Delta\theta_W}$，则

$$\phi(-\theta)=\phi_0\frac{-\theta-\theta_{W,c}}{\Delta\theta_W},\qquad -\phi(\theta)=\phi_0\frac{-\theta+\theta_{W,c}}{\Delta\theta_W}$$

两者之差：

$$\boxed{\phi(-\theta)+\phi(\theta)=-\frac{2\phi_0\theta_{W,c}}{\Delta\theta_W}}$$

一般情形 $\phi(-\theta)\neq-\phi(\theta)$。只有 $\theta_{W,c}=0$ 或满足特殊模 $2\pi$ 条件时才有 $e^{i\phi(-\theta)}=e^{-i\phi(\theta)}$。原文「$\lambda\cos3\theta\,e^{i\phi(-\theta)}=\lambda\cos3\theta\,e^{-i\phi(\theta)}$」直接跳了一步**不存在的等式**。

### B-02 弱域必须关于 $0$ 对称

宇称反演后仍在同一弱域，需满足

$$\boxed{\theta\in\mathcal D_W \ \Longleftrightarrow\ -\theta\in\mathcal D_W}$$

若弱域中心 $\theta_{W,c}\neq0$，宇称会把它映到中心为 $-\theta_{W,c}$ 的另一个扇区。要么把弱域设计为关于 $0$ 对称，要么设置一对 $\mathcal D_W^{(+)}\leftrightarrow\mathcal D_W^{(-)}$。

### B-03 更根本：$\Omega^*\neq\Omega$ 不能证明宇称破缺

普通 QFT 中，宇称 $P$ 是幺正空间反演变换；对一般复标量场，宇称**并不**必须做复共轭——复共轭通常与电荷共轭 $C$ 更直接相关。故 $P:\Omega\to\Omega^*$ 不能仅因 $\Omega$ 是复数就自动成立。

可严格化重构：令

$$\boxed{\Omega=S+iP_s}$$

其中 $S$ 为普通标量、$P_s$ 为赝标量，规定 $S(-\theta)=S(\theta)$，$P_s(-\theta)=-P_s(\theta)$，则自然有 $\Omega(-\theta)=S(\theta)-iP_s(\theta)=\Omega^*(\theta)$。此构造数学上漂亮——但 $\Omega(-\theta)=\Omega^*(\theta)$ 此时恰是**良好的宇称变换律**，本身不意味着宇称已破缺。

判定宇称是否破缺必须检查整个作用量：$\mathcal L[\text{fields}]\xrightarrow{P}\mathcal L_P$ 是否满足 $\mathcal L_P=\mathcal L$。只有 $\mathcal L_P\neq\mathcal L$ 才是显式破缺；或真空满足 $P|0\rangle\neq|0\rangle$ 才是自发破缺。原逻辑「$\phi\neq0\Rightarrow\Omega^*\neq\Omega\Rightarrow P$ 不守恒」不成立。

> 标准模型带电弱流违反宇称，是因为 $V-A$（即 $1-\gamma^5$）的手征结构、$W$ 只耦合左手费米子结构，而非存在一个普通复相位。PDG 电弱综述明确写出这种 $1-\gamma^5$ 结构。

### B-04 决定性代数结果：$\mathcal A_{\rm chiral}\equiv 0$

设 $g_L=|\Omega|e^{+i\phi}$，$g_R=|\Omega|e^{-i\phi}$，则 $|g_L|^2=|g_R|^2=|\Omega|^2$，故

$$\boxed{\mathcal A_{\rm chiral}=\frac{|g_L|^2-|g_R|^2}{|g_L|^2+|g_R|^2}\equiv 0}$$

不是近似为零，而是**恒等于零**。因此「复相位导致左手、右手耦合强度不等」不成立；复相位只导致 $g_R=g_L^*$。这是整个 Part B 当前**最大漏洞**。

### B-05 干涉相位产生 β 不对称：还缺一层

相位可经干涉产生可测量效应，但必须有至少两个真正独立的振幅 $\mathcal M=\mathcal M_1+\mathcal M_2$：

$$|\mathcal M|^2=|\mathcal M_1|^2+|\mathcal M_2|^2+2\operatorname{Re}(\mathcal M_1^*\mathcal M_2)$$

若 $\mathcal M_2=|\mathcal M_2|e^{i\phi}$，干涉项才可能含 $\cos\phi,\sin\phi$。但这还不能证明它修改的是**宇称不对称系数**——必须知道 $\mathcal O_{\rm TUFT}$ 究竟是 $V,A,S,P,T$ 中的哪一种 Lorentz 结构。

若 TUFT 振幅仅是标准模型振幅乘整体相位 $\mathcal M_{\rm TUFT}=c e^{i\phi}\mathcal M_{\rm SM}$，则 $\mathcal M_{\rm tot}=(1+ce^{i\phi})\mathcal M_{\rm SM}$：可改变总衰变率，却**可能完全不改变归一化后的角不对称度**。故 $\delta\mathcal A_{\rm TUFT}(\phi_0)$ 目前尚未被定义出来。

### B-06 能闭合宇称推导的正确形式

最低阶严谨写法：

$$\boxed{\mathcal L_{\rm TUFT}=C_L(\theta)\mathcal O_L+C_R(\theta)\mathcal O_R+\text{h.c.}},\qquad \mathcal O_L=\bar\psi_L\Gamma\psi_L,\ \mathcal O_R=\bar\psi_R\Gamma\psi_R$$

宇称下 $P_L\leftrightarrow P_R$，故 $\mathcal O_L\xleftrightarrow{P}\mathcal O_R$。宇称守恒要求形如 $C_L(\theta)=C_R(-\theta)$ 的关系。定义真正的宇称/手征不对称量：

$$\boxed{\Delta_P(\theta)=\frac{|C_L(\theta)|^2-|C_R(-\theta)|^2}{|C_L(\theta)|^2+|C_R(-\theta)|^2}}$$

$\Delta_P\neq0$ 才真正有手征耦合强度不对称。这与标准电弱理论中左右手耦合本就不对称的结构一致（PDG 将低能弱相互作用直接写成带 $1-\gamma^5$、$1+\gamma^5$ 的不同手征流）。

> **核心判语：复相位 ≠ 手征性。** 复相位往往更自然地与 CP / T 相位联系；纯 $P$ 破缺首先来自左右手 Lorentz 结构的不等价。PDG 对弱相互作用明确区分 $P$ 破缺与 CP 破缺。

### B-07 弱域边界不自动光滑：bump function 构造

当前分段 $\Omega=\begin{cases}A(\theta),&\theta\notin\mathcal D_W\\A(\theta)e^{i\phi(\theta)},&\theta\in\mathcal D_W\end{cases}$，在弱域边界 $\theta_b$ 连续至少要求 $e^{i\phi(\theta_b)}=1$ 或 $A(\theta_b)=0$，当前线性相位无保证；即使 $\phi(\theta_b)=0$，导数仍跳变（外部 $\phi'=0$，内部 $\phi'=\phi_0/\Delta\theta_W$），故「幅值连续、相位连续 ✔️」一般不正确，连 $C^1$ 都不一定成立。

若要求光滑复场，应换 bump function（弱域取 $|\theta|<\Delta$）：

$$w(\theta)=\begin{cases}\exp\left[-\dfrac{1}{1-(\theta/\Delta)^2}\right],&|\theta|<\Delta\\0,&|\theta|\ge\Delta\end{cases},\qquad \boxed{\phi(\theta)=\phi_0\frac{\theta}{\Delta}\frac{w(\theta)}{w(0)}}$$

$w$ 为偶函数 ⇒ $\phi(-\theta)=-\phi(\theta)$，且边界所有阶导数消失 $\phi^{(n)}(\pm\Delta)=0$，得到 $C^\infty$ 的弱域相位窗口。

### B-08 三倍角正确 + 原点必须删去

设 $x=\kappa a,\ y=\tau,\ r=\sqrt{x^2+y^2}$，则 $\cos\theta=x/r$、$\sin\theta=y/r$，三倍角公式 $\cos3\theta=\cos^3\theta-3\cos\theta\sin^2\theta$ 给出

$$\boxed{\cos3\theta=\frac{x^3-3xy^2}{(x^2+y^2)^{3/2}}=\frac{(\kappa a)^3-3(\kappa a)\tau^2}{[(\kappa a)^2+\tau^2]^{3/2}}}$$

**完全正确**。但遗漏：$(\kappa a,\tau)=(0,0)$ 处 $\theta$ 不存在、分母为零，必须**显式从流形中删去原点**或给出正则化。

---

## 三、Part C · 协方差 / 误差 / 区间（框架对，来源未建立）

### C-01 误差传播公式正确，但 $\Sigma_p$ 未得到

一阶 delta method：$\sigma_y^2=J_y\Sigma_pJ_y^T$；多预测量：$\Sigma_y=J\Sigma_pJ^T$。数学框架没问题——**问题在于目前还没有真正得到 $\Sigma_p$**。

### C-02 六参数四输入 ⇒ 严重可识别性问题

参数 $\mathbf p=(\lambda,\phi_0,B_1,B_2,B_3,B_4)$ 共 **6** 个；本节约定的拟合观测量 $\alpha_G,\alpha,\alpha_s,\alpha_W$ 仅 **4** 个。若 $\mathbf q=F(\mathbf p)$，Jacobian $H_{ki}=\partial q_k/\partial p_i$ 最多 $4\times6$，故

$$\operatorname{rank}H\le4\ \Rightarrow\ \boxed{\operatorname{rank}F_p\le4<6},\qquad F_p=H^T\Sigma_q^{-1}H$$

$F_p^{-1}$ 一般不存在 ⇒ **仅凭这四个耦合常数，不可能唯一得到六参数协方差矩阵**。除非前置文档另给至少两个独立方程 / 先验约束。尤其 $\phi_0$ 不由 $\alpha_G,\alpha,\alpha_s,\alpha_W$ 确定，而由 β 衰变确定 ⇒ 目前 $\sigma_{\phi_0}$ 没有来源。

### C-03 $\sigma_\lambda/\lambda\simeq0.0076$：算术对、逻辑未建立

$\frac{0.0009}{0.1179}\simeq0.00763$ 算术成立；但只有给出明确 $\lambda=f(\alpha_s,\alpha_W,\alpha,\alpha_G)$ 及 $\lambda\propto\alpha_s$，$\sigma_\lambda/\lambda\simeq\sigma_{\alpha_s}/\alpha_s\simeq0.0076$ 才成立。目前「由 $\alpha_s$ 主导」是假设，不是误差传播结果。

> PDG 版本冻结：2025 PDG QCD 世界平均 $\alpha_s(M_Z)=0.1180\pm0.0009$，与所用 $0.1179\pm0.0009$ 接近；但文档日期已是 2026、PDG 2026 已发布，最终稿须统一注明冻结 PDG 2022 还是当前版本。

> 尺度口径：$\alpha=7.2973525693\times10^{-3}$ 是低能 $\alpha(0)\approx1/137.036$，不能笼统写成「所有输入均在 $\mu=M_Z$」。PDG 明确区分 $\alpha(0)$ 与运行到 $M_Z$ 的 $\alpha(M_Z^2)$。

### C-04 电子 $g-2$ 的 95% 区间：算术对、来源未建立

接受 $\Delta a_e^{\rm center}=2.4\times10^{-13}$ 与 $\sigma=0.65\times10^{-13}$，则 $2\sigma=1.30\times10^{-13}$，得 $[1.1,3.7]\times10^{-13}$；严格 95% 高斯用 $1.96\sigma$ 得约 $[1.126,3.674]\times10^{-13}$。**算术无问题**。

但 $0.65\times10^{-13}$ **没有从 Jacobian 和协方差矩阵计算出来**：基本相对误差为 0.76% 与 2%，输出误差却是 $0.65/2.4\simeq27\%$。这在敏感/近奇异模型并非不可能，但必须展示 $\partial\Delta a_e/\partial B_i$ 具有如此大的条件数——当前没有。

> 电子磁矩实验精度极高（2023 年约 0.13 ppt），但用于找新物理受限于两个高精度独立 $\alpha$ 测量彼此约 $5.5\sigma$ 不一致。TUFT 若要定义 $10^{-13}$ 量级 $\Delta a_e$，必须明确采用哪个独立 $\alpha$ 输入及其协方差。

### C-05 UHECR：算术对、证伪阈值不成立

$0.68\pm0.21$（$10^{19}$ eV）⇒ 0.68±2(0.21) 得 $[0.26,1.10]\times10^{19}\ {\rm eV}$。基准 GZK 取 $5.00\times10^{19}\ {\rm eV}$、定义 $E_{\rm TUFT}=E_0-\Delta E$，则 $5.00-1.10=3.90$、$5.00-0.26=4.74$，即 $E_{\rm TUFT}=[3.90,4.74]\times10^{19}\ {\rm eV}$——**算术正确**。

但存在内部逻辑冲突：先称 95% 区间**剥离宇宙传播系统误差**，又称观测截断 $\ge5.0\times10^{19}\ {\rm eV}$ 即证伪。与观测比较必须使用

$$\boxed{\Sigma_{\rm total}=\Sigma_{\rm TUFT}+\Sigma_{\rm propagation}+\Sigma_{\rm source}+\Sigma_{\rm composition}+\Sigma_{\rm detector}}$$

更准确做法是把这些量作为 nuisance parameters 在完整似然中**边缘化**。现代 Auger 数据本身显示 UHECR 能谱具多个结构，解释依赖质量组成、源最大刚度、源分布与星系际磁场，并非模型无关的「唯一 GZK 截断数字」；Auger 当前分析联合考虑能谱与质量组成及源模型。因此「$E_{\rm cutoff}\ge5.0\times10^{19}\ {\rm eV}$」**不能作为严格 TUFT 单点证伪条件**，应改为完整统计检验（如 $-2\ln(L_{\rm TUFT,max}/L_{\rm reference,max})$，或 posterior predictive $p$-value / Bayes factor）。

### C-06 「三组观测独立」不正确

$\Delta a_e=\Delta a_e(\lambda,B_i,\ldots)$ 与 $\Delta E_{\rm GZK}=\Delta E_{\rm GZK}(\lambda,B_i,\ldots)$ **至少共享 $\lambda$**，故理论预测协方差

$$\operatorname{Cov}(\Delta a_e,\Delta E_{\rm GZK})=J_e\Sigma_pJ_{\rm GZK}^T$$

一般不自动为零。正确表述：β 衰变、电子 $g-2$、UHECR 是三组**数据来源不同**的观测通道；在给定参数下其实验似然可近似独立，但 TUFT 预测经共享参数产生**理论相关性**，必须做**联合参数拟合**。这比「三重完全独立交叉检验」严谨得多。

---

## 四、Part D · MCMC 技术修正

### D-01 emcee ≠ nested sampling

「MCMC 嵌套采样，基于 emcee」混用了两个不同方法：emcee 是 **ensemble Markov-chain Monte Carlo**（后验采样）；nested sampling 通常用 dynesty / UltraNest（evidence / 证据计算）。应选择其一：

$$\boxed{\text{emcee：MCMC 后验采样}}\quad\text{或}\quad\boxed{\text{dynesty：nested sampling + evidence}}$$

不能称「基于 emcee 的嵌套采样」。

### D-02 双重计数风险

若 $\Sigma$ 是用同一批耦合常数数据拟合出的后验协方差，再把它作为 MCMC 的 Gaussian prior 并**再次使用同一批数据**，会造成**数据双重计数**。只有由**独立数据**获得的协方差才能合理充当先验。

---

## 五、核心链重构建议

**废弃**：

$$\text{复相位}\ \Rightarrow\ \text{宇称破缺}\ \Rightarrow\ \text{手征不对称}$$

**采纳**：

$$\boxed{\text{明确 }L/R\ \text{Lorentz 算符}\ \Rightarrow\ C_L\neq C_R\ \Rightarrow\ P\ \text{破缺}\ \Rightarrow\ \beta\ \text{衰变角相关}}$$

复相位 $\phi_0$ 另行负责**干涉 / CP 型相位效应**。

---

## 六、状态更新表

| 审计项 | 当前更准确状态 |
|---|---|
| D-02 弱力方向不可证伪 | 🟡 **部分推进**：已确定 β 衰变作为可观测通道，但尚未给出明确 TUFT Lorentz 算符，$\delta A$ 尚不可计算 |
| D-03 宇称不守恒概念错配 | 🔴 **尚未修复**：$\Omega\to\Omega^*$ 不等价于 $P$ 破缺；当前 $g_L,g_R$ 给出 $\mathcal A_{\rm chiral}=0$ |
| F-02 可证伪预言数量 = 0 | 🟡 已有 3 个候选可检验量，但 $g-2$、UHECR、β 不对称的数值区间**尚未从完整模型推导出来**，暂不能标记为三个定量预言 |

---

## 七、路线建议（4 → 3 → 1）

在四个后续分支中，当前最应先做的是 **4【自洽性校验】→ 3【β 衰变数值计算】→ 1【MCMC】**。

> 现在直接 MCMC 会把尚未定义好的模型函数和人为指定的误差「高精度地采样」，得到漂亮图形但无统计意义。先把 $C_L,C_R$、Hermiticity、宇称变换和 $\delta\mathcal A$ 推导闭合，才是让 V3.5 从「结构性假说」进入「可计算场论模型」的关键一步。

---

## 八、保留项 vs 废弃项

**保留（骨架正确）**：$\theta=\operatorname{atan2}(\tau,\kappa a)$、$\Omega_R=\lambda\cos3\theta$、三倍角坐标化、量纲结构、协方差传播框架、「必须给出可证伪观测量」的路线。

**废弃/重构**：复相位 $\Rightarrow$ 宇称破缺链；$g_L=e^{i\phi},g_R=e^{-i\phi}$ 手征不对称声称（$\mathcal A_{\rm chiral}\equiv0$）；未导出的误差/区间/证伪阈值；「emcee 嵌套采样」；「三重完全独立」。

---

## 九、红线

1. **不推倒重来**：V3.5 保留的骨架与路线继续有效；
2. **不物理判决**：本册只裁决推导闭合性、数值来源与声称强度；
3. **来源即权威**：数值误差、区间、阈值必须在 $C_L,C_R$ 闭合后由 Jacobian / 协方差实际导出，否则视为未建立；
4. **PDG 版本冻结**：最终稿须统一注明采用 PDG 2022 / 2025 / 2026 哪一版，不得混用；
5. 有效域：增补 Part B/C/D 来料文本；公式链修订后须重跑引擎再判。

---

## 十、关联与互证（回链）

本册结论与仓内既有判定册**交叉印证、不宣称新发现**：

- **「复相位 ≠ 手征性」「Ω→Ω* 非 P 破缺」「ℛ_chiral≡0」** 与元审计 [判定_TUFT_V3.5修复方案_全维审计与重整](判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04.md) 的 **B-08**（公理集对 Ω 符号无约束力 ⇒ D-01 不可由公理消除）同向互证——复相位既不能给手征不对称，也不能由公理锁定符号；
- **「g-2 / UHECR 数值区间未由公式导出」** 与求导证明攻破 [判定_TUFT_V3.5修复方案_求导证明验证精算攻破](判定_TUFT_V3.5修复方案_求导证明验证精算攻破_2026-10-04.md) 的「两条预言均不可得」（g−2 已否决 8.06 量级、宇宙线 $\xi<5.11\times10^{-23}$ 或无约束）同向——候选预言在完整模型闭合前既不可算、也已被仓内判定关窗；
- **「Ω 候选自由度受限」** 与 Ω 公理构造不可行性册 [判定_TUFT_V3.5_Ω公理构造_不可行性判定与最小增广](判定_TUFT_V3.5_Ω公理构造_不可行性判定与最小增广_2026-10-04.md)（Π 定理 ⇒ $\Omega=\Phi(\tau/\kappa)$ 1 维）互证——复相位若作独立自由度，须先回答可识别性（见本册 §三 C-02）。

分工：本册**独有增量**在 Part C 统计自洽性（六参数/四输入可识别性、双重计数、证伪须全协方差边缘化）与 Part B 的 $C_L=C_R(-θ)$ 正确手征量重构；仓内各册负责公式层/公理层定价。

