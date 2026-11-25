# ROOT V153｜从螺旋运动到规范场动力学的必要条件

## 0. 约定与研究边界

采用平直背景 `eta = diag(-1,1,1,1)`，**仅**令 `c=1`。保留有量纲 `hbar` 和 `G`：

- `[x]=[t]=L`, `[omega]=[k]=L^-1`, `[hbar]=M L`, `[G]=L/M`。
- 相位 `theta` 无量纲。若 `A_mu` 是无量纲规范群的联络，则 `[A_mu]=L^-1`, `[F_munu]=L^-2`。
- Einstein–Hilbert 密度 `R/(16 pi G)` 的量纲 `M/L^3`。
- `hbar F^2/(4 g^2)` 的量纲也是 `M/L^3`，其中 `g` 为无量纲规范耦合。积分 `d^4x` 得作用量量纲 `M L`，与 `hbar` 同量纲。
- 度规扰动 `h_munu` 是无量纲；其线性化曲率量纲 `L^-2`。
- 实际把长度倒数换成 SI 角频率需要恢复 `c_SI`，而不是在理论里令 `hbar` 或 `G` 为 1。

## 1. 螺旋运动是运动学条件，而非场方程

`r(t)=(a cos(omega t), a sin(omega t), u t)` 给出

`a^2 omega^2+u^2=1`（光速条件），

`kappa=a omega^2`, `tau=u omega`, `omega^2=kappa^2+tau^2`。

这些关系严格成立，但 `kappa`、`tau` 属于观察者依赖的三维空间曲率和挠率，不是洛伦兹标量。运动学不决定真实传播自由度或力的耦合系数。

## 2. 单标量相位生成场：一个可严格否定的最小模型

若 `theta` 为单值、足够光滑的时空标量，尝试定义：

`A_mu = partial_mu theta`，则

`F_munu=partial_mu partial_nu theta-partial_nu partial_mu theta=0`。

再取 `h_munu=partial_mu partial_nu theta`，令 `xi_mu=(1/2)partial_mu theta`，则

`h_munu = partial_mu xi_nu + partial_nu xi_mu`。

线性引力的 `R^(1)_munurhosigma` 在这种变换下不变，因此这个构造的线性化曲率为零。

**适用范围：**光滑局部标量、上述特定的局部场映射，以及 Minkowski 背景附近的线性引力。若使用两个方向场及其外积 `dphi wedge dchi`、非平凡拓扑、非零背景或独立张量场，需要全新分析。标量 `theta` 的应力—能量本身也可以使时空弯曲；本结论不排除该效应。

## 3. 真正的横向矢量波

取 `s=t-z`，`A_0=A_z=0`, `A_x=cos(s)`, `A_y=sin(s)`。

则 `F_0x = -sin(s)`, `F_0y = cos(s)`，非零；在度规 `diag(-,+,+,+)` 下直接求导验证 `partial^mu F_munu=0`，`dF=0`。

平面波 Fourier 模式的条件为：

`k^2=0`, `k^mu eps_mu=0`, `eps_mu ~ eps_mu + lambda k_mu`。

对 `k^mu=(omega,0,0,omega)`，横向约束与规范商去掉冗余分量，只剩 `eps_x,eps_y` 两个传播自由度。其旋转本征态是 `eps_±=(ex±i ey)/sqrt(2)`，螺旋度为 `±1`（符号依旋转约定）。

## 4. 真实的横向无迹引力波

记 `g_munu=eta_munu+h_munu`，取 `h_xx=H cos(s)`、`h_yy=-H cos(s)`，其他分量为 0。根据

`R^(1)_munurhosigma = 1/2 (partial_rho partial_nu h_mu sigma + partial_sigma partial_mu h_nu rho - partial_rho partial_mu h_nu sigma - partial_sigma partial_nu h_mu rho)`，

有 `R^(1)_0x0x=(H/2)cos(s)`（单位倒长度波数）。

对任意波数 `k`，这个振幅变为 `k^2 H/2`。物理偏振由 `h_+=h_xx=-h_yy` 和 `h_cross=h_xy=h_yx` 两个独立参数构成，双圆偏振张量 `eps_± tensor eps_±` 绕传播轴旋转获得 `e^(∓2 i phi)` 因子。

线性化 Fierz–Pauli 规范变换 `delta h_munu=partial_mu xi_nu+partial_nu xi_mu`；曲率在此下不变。真空场方程 `G^(1)_munu=0`，其线性 Bianchi 恒等式 `partial^mu G^(1)_munu=0`。

注意：这是**已知的线性广义相对论**，不是从螺旋假设新推导的 Einstein 方程。

## 5. 为什么自旋 1 和自旋 2 的偏振几何仍不构成统一

同一对横向正交矢量可以构造 `eps_±`（自旋 1）、`eps_± tensor eps_±`（自旋 2），甚至更高秩张量。旋转表示只固定变换律，**没有固定作用量及其独立耦合**。例如

`S = ∫ d^4x sqrt(-g) [R/(16 pi G) - hbar F_munu F^munu/(4g_F^2)]`

在无源真空中，常数 `G>0`、`g_F>0` 的不同选择均保留相同的自由平面波传播与偏振。这是一个明确的参数不唯一性反例。此作用量是已有引力+电磁的拼接，不是统一微观起源。

## 6. 守恒与规范对称性的必要关系

给源耦合 `S_int^(1) = -∫ d^4x A_mu J^mu`，规范变化 `A_mu→A_mu+partial_mu lambda`，积分分部并忽略边界：

`delta S_int^(1) = ∫ d^4x lambda partial_mu J^mu`。

对任意 `lambda` 不变要求 `partial_mu J^mu=0`。

给线性引力 `S_int^(2)=(1/2)∫ d^4x h_munu T^munu`，对称张量 `T` 和线性坐标变换给出

`delta S_int^(2) = - ∫ d^4x xi_nu partial_mu T^munu`。

对任意 `xi` 不变要求 `partial_mu T^munu=0`。全非线性及耦合场中，应使用协变守恒及总能量动量张量。

## 7. 数值交叉验证与新理论的终点判据

- 256 组随机相对论 Boost：直接计算变换后 `F`、`R^(1)`，并与按张量律变换的结果比较。
- 38 项单元测试检查零模、非零物理场强、规范不变性、线性 Bianchi、旋转螺旋度等。
- 独立 SymPy：256 个线性化曲率分量和 16 个 Maxwell 分量对光滑标量构造全部严格为零。
- 数据仅为**理论生成与程序校验**；未导入真实地球、月球或粒子散射观测。

### 真正的新理论必须再完成：

(a) 从明确的基础自由度得到非平凡且洛伦兹协变的场；(b) 动力学自然获得正确无鬼模的两种传播偏振；(c) 独立导出粒子谱、标准模型内部规范群及相互作用耦合；(d) 与广义相对论、标准模型和已知实验相容；(e) 给出无反向调参的新预测。ROOT 当前没有达到这五个要求。
