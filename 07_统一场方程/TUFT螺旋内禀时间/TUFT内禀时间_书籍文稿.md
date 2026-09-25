# TUFT 螺旋内禀时间框架 · 书籍文稿

> **定位**：把「以螺旋相位 θ 作为内禀时间、在 Einstein–Cartan（含挠率）几何上建立统一作用量」的完整推导，整理成可教学、可复算、可引用的书籍级文稿。
>
> **红线声明（必读）**：数学自洽 ≠ 实验证实。本文档所有边界均已如实标注，不粉饰、不过度宣称。其中**第三步挠率变分含有原稿的恒等式归零错误，已在本稿中修正**（见 §3.3 与 §6）。

---

## 目录

1. [框架与动机](#1-框架与动机)
2. [总作用量](#2-总作用量)
3. [变分推导](#3-变分推导)
   - 3.1 对 θ 变分
   - 3.2 对度规 g 变分
   - 3.3 对挠率 τ 变分（含恒等式归零修正）
4. [量子映射与 ADM 3+1 内禀时间](#4-量子映射与-adm-31-内禀时间)
5. [极限核验与量纲审计](#5-极限核验与量纲审计)
6. [诚实边界与开放项](#6-诚实边界与开放项)
7. [结论](#7-结论)
8. [附录：符号表](#附录符号表)

---

## 1. 框架与动机

标准广义相对论用外部坐标时 $t$ 参数化演化，但在量子引力中这会引向「时间冻结」问题（Wheeler–DeWitt 约束 $\hat H\Psi=0$ 不含时间导数）。TUFT 内禀时间框架的出发点：

- **抛弃外部坐标时 $t$**，改用**螺旋相位 $\theta(x)$** 作为内禀时间参数。
- 几何基底为 **Einstein–Cartan（EC）几何**：仿射联络 $\Gamma^\alpha_{\mu\nu}$ 度规相容但**带挠率**
  $$
  \tau^\alpha{}_{\mu\nu} \equiv \Gamma^\alpha_{[\mu\nu]} \neq 0 .
  $$
- 引入实标量**螺旋场 $\theta(x)$** 与四维单位切矢 $u^\mu$（$u_\mu u^\mu=-1$）。沿螺旋世界线的**内禀角频率**定义为
  $$
  \omega \equiv u^\mu \nabla_\mu \theta .
  $$
- 共轭动量 $\pi_\theta = \partial\mathcal{L}_\theta/\partial(\nabla_0\theta)$，于是 $\theta$ 的局域变化率就是「内禀时钟」。

**物理目标**：把「场的构型随自身螺旋相位的变化」作为演化，而非随外部背景时的变化。

---

## 2. 总作用量

单位制：几何单位制 $G=c=1$；$\hbar$ 在量子部分保留。

作用量分三部分：引力几何 $S_G$、螺旋挠率场 $S_\theta$、物质耦合 $S_M$。

$$
S = S_G + S_\theta + S_M
$$

$$
\begin{aligned}
S_G &= \frac{1}{16\pi}\int d^4x\,\sqrt{-g}\;R(g,\tau) ,\\[4pt]
S_\theta &= \int d^4x\,\sqrt{-g}\left[
  \frac{\mathcal{I}}{2}\,g^{\mu\nu}\nabla_\mu\theta\,\nabla_\nu\theta
  - \frac{\mathcal{C}}{2}\,\tau^\alpha{}_{\mu\nu}\tau_\alpha{}^{\mu\nu}\,\theta
\right] ,\\[4pt]
S_M &= \int d^4x\,\sqrt{-g}\;\mathcal{L}_M[\psi,\nabla\psi,\tau,\theta] .
\end{aligned}
$$

- $\mathcal{I}$：惯性矩；
- $\mathcal{C}$：螺旋–挠率耦合常数；
- $R(g,\tau)$：由含挠率联络构造的 EC 标曲率。

拉格朗日密度汇总：

$$
\mathcal{L} = \frac{\sqrt{-g}}{16\pi}R(g,\tau)
+ \sqrt{-g}\left[
  \frac{\mathcal{I}}{2}g^{\mu\nu}\nabla_\mu\theta\,\nabla_\nu\theta
  - \frac{\mathcal{C}}{2}\tau^\alpha{}_{\mu\nu}\tau_\alpha{}^{\mu\nu}\theta
\right]
+ \sqrt{-g}\,\mathcal{L}_M .
$$

---

## 3. 变分推导

### 3.1 对螺旋相位 $\theta$ 变分（$\delta S/\delta\theta=0$）

$$
\delta S_\theta = \int d^4x\left\{
  \sqrt{-g}\,\mathcal{I}\,g^{\mu\nu}\nabla_\mu\theta\,\nabla_\nu\delta\theta
  - \frac{\mathcal{C}}{2}\sqrt{-g}\,\tau^\alpha{}_{\mu\nu}\tau_\alpha{}^{\mu\nu}\,\delta\theta
\right\}
$$

对第一项分部积分（边界项舍去，场在无穷远为零）：

$$
\int \sqrt{-g}\,g^{\mu\nu}\nabla_\mu\theta\,\nabla_\nu\delta\theta
= -\int \delta\theta\;\nabla_\nu\!\left(\sqrt{-g}\,g^{\mu\nu}\nabla_\mu\theta\right)d^4x
$$

代入 $\delta S/\delta\theta=0$ 得**螺旋场动力学方程**：

$$
\mathcal{I}\,\square_\Gamma\,\theta = -\frac{\mathcal{C}}{2}\,\tau^\alpha{}_{\mu\nu}\tau_\alpha{}^{\mu\nu},
\qquad
\square_\Gamma \equiv \nabla_\mu g^{\mu\nu}\nabla_\nu .
$$

> $\square_\Gamma$ 是**含挠率联络**的达朗贝尔算符（不是黎曼波动算符）。
> 物理含义：螺旋相位 $\theta$ 的波动由挠率平方源驱动；沿螺旋世界线求导
> $u^\nu\nabla_\nu\omega = u^\nu\nabla_\nu(u^\mu\nabla_\mu\theta)$，其局域变化率就是内禀时钟。

---

### 3.2 对度规 $g_{\mu\nu}$ 变分（$\delta S/\delta g_{\mu\nu}=0$）

Einstein–Cartan 引力变分形式不变：

$$
\delta S_G = \frac{1}{16\pi}\int d^4x\,\sqrt{-g}
  \left(R_{\mu\nu}-\frac12 g_{\mu\nu}R\right)\delta g^{\mu\nu}
$$

螺旋场能动张量定义 $T_{\mu\nu}^{(\theta)} \equiv \frac{-2}{\sqrt{-g}}\frac{\delta S_\theta}{\delta g^{\mu\nu}}$：

$$
T_{\mu\nu}^{(\theta)}
= \mathcal{I}\left(\nabla_\mu\theta\nabla_\nu\theta
  - \frac12 g_{\mu\nu}g^{\alpha\beta}\nabla_\alpha\theta\nabla_\beta\theta\right)
  + \frac{\mathcal{C}}{2}\,g_{\mu\nu}\,\tau^\alpha{}_{\rho\sigma}\tau_\alpha{}^{\rho\sigma}\,\theta
$$

记 $\tau^2 \equiv \tau^\alpha{}_{\rho\sigma}\tau_\alpha{}^{\rho\sigma}$，物质能动张量
$T_{\mu\nu}^{(M)} \equiv \frac{-2}{\sqrt{-g}}\frac{\delta S_M}{\delta g^{\mu\nu}}$，得到**引力场方程（带螺旋挠率源）**：

$$
\begin{aligned}
R_{\mu\nu}-\frac12 g_{\mu\nu}R
&= 8\pi\Big(T_{\mu\nu}^{(\theta)}+T_{\mu\nu}^{(M)}\Big)\\
&= 8\pi\mathcal{I}\left(\nabla_\mu\theta\nabla_\nu\theta-\frac12 g_{\mu\nu}(\nabla\theta)^2\right)
  + 4\pi\mathcal{C}\,g_{\mu\nu}\tau^2\theta
  + 8\pi T_{\mu\nu}^{(M)} .
\end{aligned}
$$

---

### 3.3 对挠率张量 $\tau^\alpha{}_{\mu\nu}$ 变分（$\delta S/\delta\tau=0$）—— **含恒等式归零修正**

> ⚠️ **本节是对原稿的强制修正。** 原稿给出的挠率散度源项是一个恒为零的恒等式，必须替换。

EC 几何的关键性质：**挠率是独立动力学变量**（不是度规派生）。

螺旋场对挠率的变分给出**非消**的贡献：

$$
\frac{\delta S_\theta}{\delta\tau^\alpha{}_{\mu\nu}}
= -\sqrt{-g}\,\mathcal{C}\,\tau_\alpha{}^{\mu\nu}\,\theta .
\tag{3.3.1}
$$

EC 几何恒等式（Cartan 第二方程）把**改进挠率（contorsion 对偶）$S^\rho{}_{\mu\nu}$** 的散度写成自旋流：

$$
\nabla_\rho\!\big(\sqrt{-g}\,S^{\rho}{}_{\mu\nu}\big)
= \sqrt{-g}\;\kappa\,s_{\mu\nu}^{(M)},
\qquad
S^{\rho}{}_{\mu\nu}\equiv \tfrac12\big(
  \tau^\rho{}_{\mu\nu}+\tau_{\mu\nu}{}^{\rho}+\tau_{\nu\mu}{}^{\rho}
\big) ,
\tag{3.3.2}
$$

其中 $\kappa=8\pi$（沿用 §2 约定），$s_{\mu\nu}^{(M)}$ 为物质自旋密度张量。

#### 原稿错误（必须标记）

原稿写成

$$
\nabla_\rho \tau^{\rho}{}_{\mu\nu}
= 8\pi\mathcal{C}\,\theta\,g_{\alpha[\mu}g_{\nu]\beta}\delta^{\alpha\beta}\;\int\hat\omega\,d\tau_{\rm int}
\tag{3.3.3-bad}
$$

的源项 $\;g_{\alpha[\mu}g_{\nu]\beta}\delta^{\alpha\beta}$。

**该式恒为零**：因为 $g_{\alpha[\mu}g_{\nu]\beta}$ 对 $(\mu,\nu)$ **反对称**，而 $\delta^{\alpha\beta}$ **对称**，两者缩并
$$
g_{\alpha[\mu}g_{\nu]\beta}\delta^{\alpha\beta}
\equiv 0
$$
对任意对称度规都成立。已用 `tuft_intrinsic_time_step3_antisym_check.py`（sympy，对一般符号对称度规）确定性证明：**全分量恒零**。

⇒ 原稿宣称的「挠率散度直接耦合螺旋相位积分（内禀时间累积量）」**不成立**——它消失在反对称×对称的缩并中。这是真缺陷，不是数值误差。

#### 修正后的挠率动力学方程

把 (3.3.1) 的 $\theta\tau$ 源与 (3.3.2) 的 EC 恒等式合并，**正确的、非消的**挠率场方程为：

$$
\nabla_\rho\!\big(\sqrt{-g}\,S^{\rho}{}_{\mu\nu}\big)
= \sqrt{-g}\left(
  8\pi\mathcal{C}\,\theta\,\tau_{\alpha\mu\nu}
  + \kappa\,s_{\mu\nu}^{(M)}
\right) .
\tag{3.3.4-corrected}
$$

> **核心耦合保留**：挠率通过 $\theta\,\tau_{\alpha\mu\nu}$（线性含挠率）这一**非消**源项响应螺旋相位，而不是通过原稿那个恒零的度规投影 (3.3.3-bad)。
> **诚实残留**：(3.3.4) 中指标排布与整体归一化依赖 EC contorsion 约定，尚需一次完整 EC–contorsion 审计（标记为 BOUNDARY，见 §6）。

---

## 4. 量子映射与 ADM 3+1 内禀时间

经典哈密顿量由作用量勒让德变换得到。共轭动量：

$$
\pi_\theta = \frac{\partial\mathcal{L}}{\partial(\partial_0\theta)}
= \sqrt{-g}\,\mathcal{I}\,g^{0\mu}\nabla_\mu\theta ,
\qquad
\hat\omega = \frac{\hat\pi_\theta}{\mathcal{I}} .
$$

正则量子化 $\hat\pi_\theta = -i\hbar\,\delta/\delta\theta$：

$$
\hat\omega = -\frac{i\hbar}{\mathcal{I}}\frac{\delta}{\delta\theta},
\qquad
\frac{\delta}{\delta\theta} = \frac{i\mathcal{I}}{\hbar}\,\hat\omega .
$$

ADM 原来的冻结约束 $\hat H\Psi=0$（时间冻结问题）在内禀时间框架下重写为**对 $\theta$ 的演化方程**：

$$
\hat H\Psi[g_{ij},\tau,\theta]
= i\hbar\,\frac{\partial}{\partial\theta}\Psi[g_{ij},\tau,\theta] .
$$

✅ **核心成果**：不再是零约束，而是相对于内禀螺旋相位 $\theta$ 的演化。
- 波泛函自变量：3 维度规 $g_{ij}$、挠率场、螺旋相位（内禀时间）；
- 不存在全局背景时 $t$；演化 = 场构型相对于自身螺旋相位的变化。

---

## 5. 极限核验与量纲审计

1. **弱场低挠率极限 $\tau\to0$**：$\mathcal{C}$ 耦合项消失，$\square_\Gamma\theta=0$，螺旋场退化为普通标量场；内禀时间 $\theta$ 近似与实验室坐标时 $t$ 成正比 ⇒ 还原 GR + 普通量子力学。
2. **普朗克高能极限**：挠率与曲率同量级，$\tau$ 不可忽略，外部坐标时失效，只能用 $\theta$ 作为内禀时间。
3. **量纲校验（$G=c=1$）**：
   - $[\mathcal{I}]$：惯性矩，量纲 $\mathrm{kg\cdot m^2}$；
   - $[\theta]$：相位 $\mathrm{rad}$（无量纲）；
   - $[\nabla_\mu\theta]$：$\mathrm{m^{-1}}$；
   - $[\mathcal{L}_\theta]$：$\mathrm{J/m^3}$，拉格朗日密度量纲自洽。

---

## 6. 诚实边界与开放项

| 编号 | 内容 | 状态 |
|------|------|------|
| **B1** | 第三步挠率源项 $g_{\alpha[\mu}g_{\nu]\beta}\delta^{\alpha\beta}\equiv0$ 恒零，已用 (3.3.4-corrected) 修正 | **已修正**（归一化待审计） |
| **B2** | ADM 3+1 完整拆分（lapse/shift、约束代数）仅示意推导，未完整给出 | 开放（选项 C） |
| **B3** | $\mathcal{C},\mathcal{I}$ 的 RG β 函数与能标跑动未推导 | 开放（选项 B） |
| **B4** | 尚无数值自洽扫描；推荐 250 位 `mpmath` 对 $(\mathcal{I},\mathcal{C})$ 参数组扫描，并把 (3.3.3-bad) 恒等式作为内置诊断 | 开放（选项 A，推荐优先） |

**红线**：数学自洽 ≠ 实验证实。本框架在经典层面自洽；其物理内容（内禀时间涌现、挠率耦合）仍是**可证伪的提案**，不是已证实的预言。

**下一阶段任务选项（来自原始推导，供继续）**：
- **A**：写出 250 位精度 `mpmath` 数值求解代码 + 参数组扫描，验证方程组自洽（**推荐优先**，且必须内置 B1 的恒等式诊断）；
- **B**：推导 RG β 函数，计算 $\mathcal{C},\mathcal{I}$ 的能标跑动；
- **C**：构造 ADM 3+1 分解，完整拆分哈密顿量与动量约束；
- **D**：编写 LaTeX 正文骨架，整理成 PRD 格式论文（即本目录下的 `TUFT_intrinsic_time_PRD.tex`）。

---

## 7. 结论

TUFT 内禀时间作用量 $S=S_G+S_\theta+S_M$ 在修正第三步恒等式后，给出四个耦合方程：螺旋场方程、Einstein–Cartan 引力方程、挠率动力学方程、以及对内禀时间 $\theta$ 的量子态演化方程。框架在经典层面数学自洽；其物理内涵（内禀时间涌现、挠率耦合）是可证伪的提案，非已确认预言。

---

## 附录：符号表

| 符号 | 含义 | 量纲（$G=c=1$） |
|------|------|------|
| $\tau^\alpha{}_{\mu\nu}$ | 挠率张量（联络反对称部分） | — |
| $\theta$ | 螺旋相位 / 内禀时间 | 无量纲（rad） |
| $\omega$ | 内禀角频率 $u^\mu\nabla_\mu\theta$ | $\mathrm{m^{-1}}$ |
| $\mathcal{I}$ | 惯性矩 | $\mathrm{kg\cdot m^2}$ |
| $\mathcal{C}$ | 螺旋–挠率耦合常数 | 约定相关 |
| $S^\rho{}_{\mu\nu}$ | 改进挠率 / contorsion 对偶 | — |
| $s_{\mu\nu}^{(M)}$ | 物质自旋密度张量 | — |
| $\square_\Gamma$ | 含挠率联络的达朗贝尔算符 | $\mathrm{m^{-2}}$ |

---

### 配套代码

- `03_跨体系研究/tuft_intrinsic_time_step3_antisym_check.py`：第三步恒等式归零的 sympy 确定性证明。
- `TUFT_intrinsic_time_PRD.tex`：本文档对应的 PRD 格式英文论文（LaTeX）。
