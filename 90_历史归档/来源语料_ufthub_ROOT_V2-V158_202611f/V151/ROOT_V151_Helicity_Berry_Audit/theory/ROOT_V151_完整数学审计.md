# ROOT V151｜光速螺旋、三正交标架与光子螺旋度的几何审计

**科学定位**：研究性数学复算与反例审计，不是四力统一证明，也不是光速螺旋粒子假说的实验确认。**理论仅采用 `c=1`；从未令 `ħ=1` 或 `G=1`。**

## 1. 研究问题、定义与假设

- **H1（ROOT 待证明）**：基础场的内部旋转/螺旋几何具有动力学意义，可能联系基本相互作用。
- **E1（已建立物理）**：真空自由电磁波是洛伦兹协变、质量为零、螺旋度为 ±1 的规范场激发；每个动量方向具有两个横向偏振态。
- **E2（已建立数学）**：空间传播方向 `n` 与其切空间 `e_theta,e_phi` 构成局部正交标架，能够产生带规范变换的 Berry 联络。
- **待解问题**：是否能在不预先假设 Maxwell/Yang–Mills/Einstein 方程的情况下，从 H1 得到四种相互作用及其耦合。现阶段答案：**没有证明**。

此处区分 **光子传播方向在动量空间转动** 和 **光子在真实空间沿螺旋世界线运动**；二者不是同一件事。

## 2. 三方向正交（可严格证明）

取传播方向球坐标：

\[
\mathbf n=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta),
\quad \mathbf e_\theta=(\cos\theta\cos\phi,\cos\theta\sin\phi,-\sin\theta),
\quad \mathbf e_\phi=(-\sin\phi,\cos\phi,0).
\]

直接点积得 `n·e_theta=n·e_phi=e_theta·e_phi=0`，长度均为 1，并且 `n×e_theta=e_phi`。

圆偏振基底：

\[
\mathbf e_\sigma=(\mathbf e_\theta+i\sigma\mathbf e_\phi)/\sqrt2,
\quad \sigma=\pm1.
\]

\(\mathbf n\cdot \mathbf e_\sigma=0\)，归一化 \(\mathbf e_\sigma^\dagger\mathbf e_\sigma=1\)。取算符 \(\mathsf H=i\mathbf n\times\)，则
\[
\mathsf H\mathbf e_\sigma=\sigma\mathbf e_\sigma.
\]

这里的 ±1 是 **spin-1 横向偏振基底的螺旋度标签**；真实单光子的角动量投影为 \(\sigma\hbar\)，不设 \(\hbar=1\)。

## 3. 从正交标架推导 Berry 联络和曲率（可严格证明）

定义动量传播方向球 `S²` 上的一形式
\[
\mathcal A_\sigma=-i\mathbf e_\sigma^\dagger d\mathbf e_\sigma.
\]

由于 `e_theta·∂_phi e_phi=-cos(theta)` 与其余关系：
\[
\mathcal A_\sigma=-\sigma\cos\theta\,d\phi,\qquad
\mathcal F_\sigma=d\mathcal A_\sigma
=\sigma\sin\theta\,d\theta\wedge d\phi.
\]

沿两个局部图分别取 `A_N=σ(1−cosθ)dφ`、`A_S=−σ(1+cosθ)dφ`，则 `A_N−A_S=2σ dφ`。这是带非平凡跃迁的局部规范联络；不存在全局处处光滑的单个偏振基底。

对球面积分：
\[
\boxed{C_\sigma=\frac1{2\pi}\int_{S^2}\mathcal F_\sigma
=2\sigma.}
\]

传播动量非零时，动量空间 Berry 曲率向量：
\[
\boldsymbol\Omega_\sigma(\mathbf k)
=\sigma\frac{\mathbf k}{|\mathbf k|^3},\quad \mathbf k\ne0.
\]

**关键物理归属**：\(\mathcal F_\sigma\) 属于 **动量空间**，不是时空张量 \(F_{\mu\nu}^{EM}\)。`C=±2` 是光子横向偏振束的已知拓扑性质，而非 ROOT 新导出的基本力常数。出处参阅参考文献。

## 4. 局部垂直旋转只产生规范变化，不必产生真实场强

在任意局部区间作基底变换
\[
\mathbf e_\sigma\mapsto e^{i\chi(\mathbf k)}\mathbf e_\sigma,
\qquad
\mathcal A\mapsto\mathcal A+d\chi,
\qquad \mathcal F\mapsto\mathcal F.
\]

对传播方向固定的单纯相位 \(\psi(x)\)，若构造时空势 \(A_\mu=\partial_\mu\psi\)，则
\[
F_{\mu\nu}=\partial_\mu\partial_\nu\psi-\partial_\nu\partial_\mu\psi=0.
\]

当标架方向 `n(k)` 改变时，动量空间 Berry 曲率可以非零，但不能因此断言时空 Maxwell 场强非零。**ROOT 必须额外给出哪些自由度有独立传播，且为什么具有可测耦合。**

## 5. 圆偏振光场：旋转矢量与直线传播（可严格验证）

取 \(\varphi=\omega(t-z)\)、\(c=1\)，任意 \(\sigma=\pm1\)：
\[
\begin{aligned}
\mathbf E&=E_0(\cos\varphi,\sigma\sin\varphi,0),\\
\mathbf B&=E_0(-\sigma\sin\varphi,\cos\varphi,0).
\end{aligned}
\]

显式求导得
\[
\nabla\cdot\mathbf E=\nabla\cdot\mathbf B=0,
\quad \partial_t\mathbf E=\nabla\times\mathbf B,
\quad\partial_t\mathbf B=-\nabla\times\mathbf E.
\]

此时 \(\mathbf E\cdot\mathbf B=0\)，\(E^2=B^2=E_0^2\)，\(\mathbf E\times\mathbf B=E_0^2\hat z\)。场矢量的端点可以沿空间形成螺旋图样，**能流仍沿直线 +z 方向**，不能把图上的螺旋线当作自由光子的轨迹。

沿 +z 以速度 β 作洛伦兹变换，令 \(D=\sqrt{(1-\beta)/(1+\beta)}\)：
\[
\omega'=D\omega,\quad E'_0=D E_0,\quad \sigma'=\sigma,
\quad E'_\gamma=\hbar\omega'=D E_\gamma.
\]

**与 V149 的区别**：真空光的相位频率 \(\omega\) 和能量一起变换；非自由点状激发的空间螺旋角频率不必等同于光子的量子频率。

## 6. 明确的不可行证明（限定前提）

**(a) 纯相位无法产生自由光子**：只用 `A=dψ` 则 `F=d²ψ=0`，没有非零 Maxwell 动力学。这个结论只针对光滑局部纯梯度构造；有奇点或全局不平凡拓扑时需单独讨论 holonomy。

**(b) 一对 Euler 标量不能描述一般电磁场**：若 `F=dq∧dp`，则 `F∧F=0`，等价于四维 4×4 反对称矩阵的 Pfaffian 为 0。一般场可有 \(\mathbf E\cdot\mathbf B\ne0\)，因此不被覆盖。

**(c) 单纯几何数值 `C=±2` 不能决定精细结构常数**：在 Maxwell/Yang–Mills 型作用量中，`(1/4g²)F²` 的系数是仍可连续选取的动力学耦合参数。几何绕数整数并不给出 `g`，也没有量纲机制决定 \(G,\hbar\)。

**(d) 偏振自由度检验**：四维无质量规范四矢量具有 8 个相空间变量、2 个一类约束，故物理传播模式数 `(8−2×2)/2=2`。标量相位的一种纵向模式不能以纯局部基底变换代替这两个 spin-1 横向模式。模型若生成额外纵向模，需要同实验检验。

**(e) 三维空间螺旋不是 Lorentz 标量**：对零间隔的\(\mathbf r=(a\cos\omega t,a\sin\omega t,ut)\)，速度约束\(a²\omega²+u²=1\)，其\(\kappa=a\omega²\)，\(\tau=u\omega\)。沿轴以 \(\beta=u\) boost 后，\(\tau'=0\)，故 \(\kappa²/(\kappa²+\tau²)\) 不能普遍解释精细结构常数。

## 7. 量纲审计（c=1，保留 ħ/G）

| 变量 | 量纲 | 备注 |
|---|---|---|
| `κ, τ, ω` | `L⁻¹` | 因为时间与长度同量纲，采用 `c=1` |
| `ħ` | `能量×长度` | 不设为 1；单光子能量 \(E=\hbar\omega\) |
| `G` | `L/M`（等价的物理维度按质量单位约定） | 独立有量纲，未从模型推出 |
| `A_φ`, `F_θφ`, `C` | 无量纲角变量对应几何量 | 来自动量方向球的角坐标 |
| `Ω_k` | `k⁻²` | 指动量/波数空间的 Berry 曲率，非时空 Maxwell 场强 |
| `α` | 无量纲 | 观测参考值来自 CODATA，未被理论预测 |

**注意**：引力常数在 `c=1`、`M` 按普通质量单位记时为 `G` 的量纲 `L/M`；将 `M` 表示为能量也可记 `L²`，不能将不同计量习惯混为一谈。

## 8. 对四力统一的判据与下一步任务

在给定基本变量和有限个耦合参数的条件下，必须满足：

1. 变分得到独立无质量 spin-1 的两种传播模式，而不只得到纯规范相位；
2. 具有可计算的 Lorentz 协变场方程、正定适当能量条件以及一致约束结构；
3. 不直接预装目标规范群，而能解释出现 \(U(1)\times SU(2)\times SU(3)\) 的原因；
4. 在明确的量子化方案下异常抵消、预测耦合运行，说明 \(\alpha(0)\) 的边界值从何而来；
5. 引力部分从作用量恢复 Einstein 极限，并产生至少一个可与地月或粒子实验独立比较的新预测。

本版已证明的是已知数学和物理中的几个必要关系及特定最小构造的反例，不是完成这些五个要求。

## 9. 复现限制

全部测试为**符号恒等式、合成参数或解析模型**，没有新粒子散射数据、地月卫星实际残差，也没有独立实验验证新力。程序会生成自动化数据和示意图；不同库版本的 PNG 文件字节可能不同，不影响数值精算验证。
