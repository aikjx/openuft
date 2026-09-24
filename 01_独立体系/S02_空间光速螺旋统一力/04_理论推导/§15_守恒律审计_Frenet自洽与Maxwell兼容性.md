# §15 守恒律审计：Frenet 自洽性 + Maxwell 兼容性

> 算法联盟最高权限 · S02 空间光速螺旋统一力 · 场标架分支
>
> **本节性质变更（重要）**：原计划 Part E-① 是「守恒律完整证明 + Noether 对应」。但在动笔前做前提审计时发现，**§13 的场拟设并非真空 Maxwell 解**，守恒律因此无从成立。本节改为**审计报告**，如实给出两个已坐实的缺陷与一个 no-go 定理。
>
> **红线守约**：以下全部为数值事实（脚本 `conservation_maxwell_audit.py` 实跑输出）。**不粉饰为 PASS，不把 FAIL 写成「部分闭合」以规避结论**。两个缺陷是 §13 的结构性问题，不是舍入误差。

---

## 15.0 为什么必须先做 Maxwell 审计

守恒律（能量 / 动量 / 角动量）是 Maxwell 方程组的**推论**，不是独立假设。Poynting 定理 $\partial_t u+\nabla\!\cdot\!\boldsymbol S=0$ 与动量守恒 $\partial_t \boldsymbol g-\nabla\!\cdot\!\overleftrightarrow T=0$ 的成立，严格依赖场满足真空 Maxwell 方程（$\rho=0,\boldsymbol J=0$）。若场构型本身不是真空解，则：

- 连续性方程出现源项（$\nabla\!\cdot\!\boldsymbol S=-\boldsymbol J\!\cdot\!\boldsymbol E$ 等）；
- Noether 守恒流因对称性被背景结构破坏而不再守恒。

故必须先审计 §13 拟设的 Maxwell 兼容性，再谈守恒律。

---

## 15.1 缺陷一：§13 显式标架不满足其自身声明的 Frenet 方程

§13 文档 Part B 与 `momentum_darboux.py` 中的显式标架为（$\phi=Ks$）：

$$
\boldsymbol e_1=(\cos\phi,\ \sin\phi,\ 0),\quad
\boldsymbol e_2=(-\sin\phi\cos\theta,\ \cos\phi\cos\theta,\ \sin\theta),\quad
\boldsymbol e_3=(-\sin\phi\sin\theta,\ \cos\phi\sin\theta,\ -\cos\theta)
$$

代入 §13 自己声明的 Frenet 方程 $\boldsymbol e_1'=\kappa\boldsymbol e_2,\ \boldsymbol e_2'=-\kappa\boldsymbol e_1+\tau\boldsymbol e_3,\ \boldsymbol e_3'=-\tau\boldsymbol e_2$（$\kappa=K\cos\theta,\ \tau=K\sin\theta$），数值残差（已用 $1/K$ 无量纲化）：

| $\theta$ | $0^\circ$ | $15^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $75^\circ$ | $89^\circ$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| §13 原版残差 | $0$ | $3.66\!\times\!10^{-1}$ | $7.07\!\times\!10^{-1}$ | $1.000$ | $1.225$ | $1.366$ | $1.414$ |

**残差是 $O(1)$ 量级**（$\theta=89^\circ$ 时达 $1.41$），不是数值误差。该标架**仅在 $\theta=0$ 时**是 Frenet 标架。

### 判据性诊断（更简洁的判据）

$\kappa,\tau$ 为常数时，圆柱螺旋的 **Darboux 矢量在实验室系必须是常矢量**（螺旋轴固定，$\boldsymbol\omega_D=K\hat z$）。检查 $|\mathrm d\boldsymbol\omega_D/\mathrm ds|/K^2$：

| $\theta$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $75^\circ$ |
| --- | --- | --- | --- | --- |
| §13 原版 | $0.661$ | $0.866$ | $0.968$ | $0.998$ |
| 修正版 | $0$ | $0$ | $0$ | $3\!\times\!10^{-17}$ |

> §13 原版的 $\boldsymbol\omega_D$ 随 $s$ 明显变化 → **直接证否其 Frenet 标架身份**，无需逐项核对。

### 影响范围（重要：有限）

该标架**仍是正交归一的**（正交性残差 $0$），而 §13 的耦合恒等式 $\boldsymbol p_\gamma\!\cdot\!\boldsymbol\omega_D=K^2S_z$ 的推导**只用到正交性**（$\boldsymbol e_3\!\cdot\!\boldsymbol e_1=0,\ \boldsymbol e_3\!\cdot\!\boldsymbol e_3=1$），未用到 Frenet 方程。故：

- ✅ **§13 Part A 耦合恒等式不受影响**（数值已验至 $5\times10^{-16}$）；
- ✅ **§14 全部误差传播结论不受影响**（只依赖 $S_z=\hbar\cos\theta$ 等标量关系）；
- ❌ **§13 Part B 的动量演化曲线**用的是错误 $\boldsymbol e_3$，定性结论（横向振荡、均值归零、净沿 $z$）幸存，但具体分量式需改用修正标架重算。

---

## 15.2 修正标架（绕固定 Darboux 轴匀角速转动）

常 $\kappa,\tau$ 螺旋的正确标架：以 $\boldsymbol\omega_D=K\hat z$ 为轴、以角速率 $K$ 匀角速转动。取 $\phi=Ks$：

$$
\boxed{
\begin{aligned}
\boldsymbol e_1&=(\cos\theta\cos\phi,\ \cos\theta\sin\phi,\ \sin\theta)\\
\boldsymbol e_2&=(-\sin\phi,\ \cos\phi,\ 0)\\
\boldsymbol e_3&=(-\sin\theta\cos\phi,\ -\sin\theta\sin\phi,\ \cos\theta)
\end{aligned}}
$$

校验（数值，全角度）：

- Frenet 三式残差 $\le1.5\times10^{-16}$（机器精度）；
- 正交归一残差 $0$；
- $\boldsymbol\omega_D=\tau\boldsymbol e_1+\kappa\boldsymbol e_3=K\hat z$ **严格恒定**（$\sin\theta\!\cdot\!\sin\theta+\cos\theta\!\cdot\!\cos\theta=1$，横向项逐项抵消）。

---

## 15.3 缺陷二（更严重）：§13 场拟设不是真空 Maxwell 解

取相量 $\tilde{\boldsymbol E}=E_0(\boldsymbol e_1+i\boldsymbol e_2)e^{ikz}$、$\tilde{\boldsymbol B}=\tfrac1c\boldsymbol e_3\times\tilde{\boldsymbol E}$，时间因子 $e^{-i\omega t}$；标架绕 $z$ 转动速率 $q$，指数波数 $k$。§13 原拟设取 $q=K,\ k=K$。

真空 Maxwell 残差（归一化）：$R_1=\nabla\!\cdot\!\tilde{\boldsymbol E}$、$R_2=\nabla\!\cdot\!\tilde{\boldsymbol B}$、$R_3=\nabla\times\tilde{\boldsymbol E}-i\omega\tilde{\boldsymbol B}$、$R_4=\nabla\times\tilde{\boldsymbol B}+i\frac{\omega}{c^2}\tilde{\boldsymbol E}$：

| 构型 | $R_1=\nabla\!\cdot\!E$ | $R_2$ | $R_3$ (Faraday) | $R_4$ (Ampère) | $\lvert E_z\rvert/\lvert E\rvert$ |
| --- | --- | --- | --- | --- | --- |
| §13 原版 $\theta=0^\circ$, $q{=}K,k{=}K$ | $0$ | $0$ | **$1.000$** | $3\!\times\!10^{-9}$ | $0$ |
| §13 原版 $\theta=45^\circ$, $q{=}K,k{=}K$ | **$0.500$** | $2\!\times\!10^{-9}$ | **$1.000$** | $3\!\times\!10^{-9}$ | **$0.500$** |
| 修正 $\theta=0^\circ$, $q{=}K,k{=}K$ | $0$ | $0$ | **$1.000$** | $3\!\times\!10^{-9}$ | $0$ |
| 修正 $\theta=45^\circ$, $q{=}K,k{=}K$ | **$0.500$** | $2\!\times\!10^{-9}$ | **$1.082$** | $4\!\times\!10^{-9}$ | **$0.500$** |
| 修正 $\theta=0^\circ$, $q{=}K,k{=}K{+}q$ | $0$ | $0$ | $0$ | $0$ | $0$ |
| 修正 $\theta=45^\circ$, $q{=}K,k{=}K{+}q$ | **$0.721$** | $2\!\times\!10^{-9}$ | **$0.556$** | $2\!\times\!10^{-9}$ | **$0.500$** |

### 两条物理根因

**(a) $\theta=0$ 时传播被标架转动完全抵消（$k_{\text{eff}}=k-q=0$）**

$\theta=0$ 时 $\boldsymbol e_1+i\boldsymbol e_2=e^{-iqz}(1,i,0)$，故

$$
\tilde{\boldsymbol E}=E_0(1,i,0)e^{i(k-q)z}
$$

有效波数 $k_{\text{eff}}=k-q$。§13 取 $k=q=K\ \Rightarrow\ k_{\text{eff}}=0$：**场在空间上完全均匀**，仅为原地旋转的时间振荡 $\boldsymbol E=E_0(1,i,0)e^{-i\omega t}$，**根本不传播**。此时 $\nabla\times\boldsymbol E=0$ 而 $\partial_t\boldsymbol B\neq0$，Faraday 定律被彻底违反（$R_3=1.000$ 归一化残差）。

> 只有补上相位（$k=K+q$，使 $k_{\text{eff}}=K=\omega/c$）才得到合法真空解——而这**就是普通的圆偏振平面波**。

**(b) $\theta\neq0$ 时出现纵向分量，需要非零电荷密度**

修正标架下 $\boldsymbol e_1$ 有 $z$ 分量 $\sin\theta$，故 $E_z=E_0\sin\theta\,e^{ikz}\neq0$，$\theta=45^\circ$ 时 $\lvert E_z\rvert/\lvert E\rvert=50\%$。因场仅依赖 $z$：

$$
\nabla\!\cdot\!\boldsymbol E=\frac{\partial E_z}{\partial z}=ikE_0\sin\theta\,e^{ikz}\neq0
\quad\Longrightarrow\quad
\rho=\varepsilon_0\nabla\!\cdot\!\boldsymbol E\neq0
$$

即 $\tau\neq0$ 构型是**带纵向分量的有源模（等离子体型振荡）**，不是横向自由辐射场。

### no-go 定理（核心结论）

真空单色解要求**每个** Fourier 分量的波数满足色散 $\lvert k\rvert=\omega/c$。标架以速率 $q$ 绕轴旋转，会在场中同时引入 $k+q$ 与 $k-q$ 两个分量（$\theta\neq0$ 时二者系数均非零）：

$$
\lvert k+q\rvert=\lvert k-q\rvert=\frac{\omega}{c}\ \Longrightarrow\ q=0
$$

> **结论**：真空中**不存在**「偏振基矢沿传播方向以非零速率旋转」的单色横向解。纯 $z$ 依赖的标架旋转在真空中必然退化为普通平面波。

---

## 15.4 守恒律核验结果

对时均流 $\langle\boldsymbol S\rangle=\tfrac{1}{2\mu_0}\mathrm{Re}[\tilde{\boldsymbol E}\times\tilde{\boldsymbol B}^*]$ 与 Maxwell 应力张量 $\langle\overleftrightarrow T\rangle$：

| 构型 | $\nabla\!\cdot\!\langle\boldsymbol S\rangle/K\lvert\boldsymbol S\rvert$ | $\nabla\!\cdot\!\langle\overleftrightarrow T\rangle/K\lVert T\rVert$ |
| --- | --- | --- |
| §13 原版 $\theta=45^\circ$, $q{=}K,k{=}K$ | $0$ | **$1.000$** |
| 修正 $\theta=0^\circ$, $q{=}K,k{=}K{+}q$（合法真空解） | $0$ | **$0$** |
| 修正 $\theta=45^\circ$, $q{=}K,k{=}K{+}q$ | $0$ | **$1.000$** |

- **只有合法真空解同时满足能量与动量守恒**（两项残差均为 $0$）；
- 所有 $\theta\neq0$ 构型的**动量守恒以 $O(1)$ 相对破坏**（残差 $=1.000$）；
- $\nabla\!\cdot\!\langle\boldsymbol S\rangle=0$ 在所有行均为 $0$，但这只是「一维平面波结构导致 $S_z$ 为常数」的平凡结果，**不代表**构型合法。

---

## 15.5 Noether 对应的失效根源

自由电磁场作用量 $S=-\tfrac14\int F_{\mu\nu}F^{\mu\nu}$ 具 Poincaré 对称性，Noether 给出三条守恒流：

| 对称性 | 守恒量 | 流 |
| --- | --- | --- |
| 时间平移 | 能量 | 应力-能量张量 $T^{\mu\nu}$ |
| 空间平移 | 动量 | $T^{\mu\nu}$ 的空间分量 |
| 洛伦兹转动 | 角动量 | $M^{\lambda\mu\nu}=x^\mu T^{\lambda\nu}-x^\nu T^{\lambda\mu}$ |

**本模型的问题**：把 $\kappa,\tau$（随 $z$ 转动的标架）当作**外加背景几何结构**引入，就等于在作用量中植入了一个依赖 $z$ 的背景场，这**显式破坏了沿 $z$ 的平移对称性与绕轴转动对称性**。Noether 定理的前提不再满足，守恒律失效——这正是 15.4 中 $\nabla\!\cdot\!\langle\overleftrightarrow T\rangle\neq0$ 的根源，与数值结果完全自洽。

> 换言之：不是「守恒律推导有误」，而是**该构型本就不具备产生守恒律所需的对称性**。

---

## 15.6 诚实结论（对 §13 的降级判定）

| §13 条目 | 判定 | 说明 |
| --- | --- | --- |
| Part A 耦合恒等式 $\boldsymbol p_\gamma\!\cdot\!\boldsymbol\omega_D=K^2S_z$ | ✅ 体系内成立 | 仅用正交性；已验至 $5\times10^{-16}$。但**物理诠释降级**为纯几何关系 |
| Part B 动量横向振荡 | ⚠️ 需修正 | 结论定性幸存，须改用 15.2 修正标架重算 |
| Part C2 连续自旋投影 $S_z\in[0,\hbar]$ | ❌ 失去真空基础 | 对应构型非真空解（需非零电荷密度） |
| Part C3 判据 1（连续谱） | ❌ 理论基础不成立 | 非真空自由光子态 |
| Part C3 判据 2（横向动量密度成像） | ❌ 同上 | 同上 |
| Part C4-1「兼容麦克斯韦方程组」 | ⚠️ 仅 $\theta=0$ 且相位补偿后成立 | 即退化为标准圆偏振平面波；$\tau\neq0$ **不兼容** |

**一句话**：§13 唯一自洽的真空极限就是标准圆偏振平面波；$\tau\neq0$ 分支在真空中不成立（是有源纵向模），§13 的三条实验判据因此**不具备真空自由光子层面的理论基础**。

---

## 15.7 若要挽救 $\tau\neq0$：可能出路（诚实列出，**均未实现**）

1. **介质 / 波导 / 结构光近场**：在有源或有界系统中 $\nabla\!\cdot\!\boldsymbol E\neq0$ 由束缚电荷承担，守恒律改写为「场 + 介质/源」的整体守恒（Minkowski–Abraham 争议范畴）。此时 $\theta\neq0$ 可作为**介质内**的有效描述，但不再是自由光子。
2. **涡旋光（OAM）**：真正的 OAM 光束（Laguerre–Gaussian / Bessel）确具空间变化的偏振与横向结构，且**满足**真空 Maxwell —— 但其变化依赖**横向坐标** $(x,y)$（$e^{i\ell\varphi}$ 方位角依赖），**不是**纯 $z$ 依赖的标架旋转。若改用横向结构建模，则 §13 的「沿传播方向的标架扭转」图景需整体重构。
3. **放弃单色性**：15.3 的 no-go 只约束**单色**解。允许波包（多 $k$ 叠加）后，不同分量可有不同有效波数；但这已落入 Part E-②（非单色波包）范畴，且波包在真空中仍受 $\lvert k\rvert=\omega/c$ 逐分量约束，前景不明。

**建议**：在明确选定上述出路之一前，不建议继续推进 §13 的实验判据方向；Part E-①（守恒律）在真空自由场层面已由本节给出**否定性闭合**。

---

## 15.8 附：需同步修正的既有文件

- `momentum_darboux.py`：`frenet_frame_lightspeed` 须改用 15.2 修正标架（耦合恒等式结论不变，Part B 曲线需重算）；
- §13 文档 Part B 的 $\boldsymbol e_3(s)$ 显式式须替换；
- §13 Part C4-1 与 Part C3 判据须加注 15.6 的降级判定。
