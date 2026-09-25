# 第8章 电荷的拓扑本源与麦克斯韦方程组

## 8.1 电荷的本质

电荷是电磁相互作用的源，是物理学中最基本的量子数之一。但电荷的本质是什么？为什么电荷是量子化的？为什么存在正负两种电荷？

标准模型中，电荷是U(1)规范对称性的守恒量（诺特定理），电荷的量子化来自规范群的紧致性。但这只是形式化的描述，没有解释电荷的物理本体。

TUFT对电荷的理解更加几何化：**电荷是时空世界线挠率的拓扑通量**。挠率的手性（左旋/右旋）天然对应电荷的正负。

## 8.2 矢量挠率场

### 8.2.1 从标量挠率到矢量挠率场

前几章中，挠率 $\tau$ 是标量，描述单根世界线的扭曲程度。但在描述电磁场时，需要将挠率推广为**矢量场** $\boldsymbol{\tau}(\boldsymbol{r}, t)$。

**定义8.1（矢量挠率场）：**

矢量挠率场 $\boldsymbol{\tau}(\boldsymbol{r}, t)$ 是定义在三维空间中的矢量场，其方向沿Frenet副法向量 $\boldsymbol{B}$，其模为标量挠率 $\tau$。

$$
\boldsymbol{\tau} = \tau \boldsymbol{B}
$$

**物理意义：**
- 矢量挠率场描述时空的扭曲分布；
- 场的方向是扭曲的轴向（副法向）；
- 场的大小是扭曲的强度；
- 场的散度对应电荷密度，场的旋度对应磁场。

### 8.2.2 挠率场的手性

挠率 $\tau$ 可以取正值或负值，对应右手螺旋或左手螺旋。矢量挠率场的方向也因此有两种手性。

在TUFT中：
- **正电荷**：右手螺旋挠率场（$\tau > 0$）；
- **负电荷**：左手螺旋挠率场（$\tau < 0$）。

这为电荷的正负提供了自然的几何解释，不需要额外的假设。

## 8.3 电荷的拓扑定义

### 8.3.1 电荷作为挠率通量

**定义8.2（拓扑电荷）：**

闭合曲面 $S$ 内的电荷等于矢量挠率场通过该曲面的通量乘以拓扑-电磁耦合常数 $k_q$：

$$
\boldsymbol{q = k_q \oiint_S \boldsymbol{\tau} \cdot d\boldsymbol{S}}
$$

由高斯散度定理：

$$
q = k_q \iiint_V (\nabla \cdot \boldsymbol{\tau}) \, dV
$$

因此电荷密度为：

$$
\rho_e = k_q \nabla \cdot \boldsymbol{\tau}
$$

### 8.3.2 量纲验证

$$
[\rho_e] = [k_q] \cdot [\nabla \cdot \boldsymbol{\tau}] = [k_q] \cdot (1/m) \cdot (1/m) = [k_q] / m^2
$$

如果 $[k_q] = C \cdot m$，则 $[\rho_e] = C/m^3$，量纲正确。

（$k_q$ 的具体量纲和数值需要通过拓扑孤子散射确定，目前是开放命题。）

### 8.3.3 电荷量子化的拓扑起源

电荷的量子化（所有电荷都是基本电荷 $e$ 的整数倍）在TUFT中有自然的拓扑解释：

电荷是挠率通量，而挠率通量对于闭合孤子是拓扑量子化的。环绕数 $\mathrm{Lk}$ 是整数（或半整数），挠率通量与环绕数相关，因此电荷自然量子化。

具体来说，对于基本费米孤子（$\theta=45^\circ$），挠率通量对应一个基本单位，电子的电荷为 $-e$，质子的电荷为 $+e$。

## 8.4 电磁势的挠率表达

### 8.4.1 矢量势

标准电磁学中，矢量势 $\boldsymbol{A}$ 定义为：

$$
\boldsymbol{B} = \nabla \times \boldsymbol{A}
$$

在TUFT中，矢量势直接对应矢量挠率场：

$$
\boldsymbol{A} = k_A \boldsymbol{\tau}
$$

其中 $k_A$ 是拓扑-电磁耦合常数。

### 8.4.2 标量势

标量势 $\phi$ 对应挠率场的时间分量（或时间导数）：

$$
\phi = k_\phi c \, \tau_t
$$

其中 $\tau_t$ 是挠率场的时间分量（标量部分），$k_\phi$ 是耦合常数。

### 8.4.3 四维势

电磁四维势 $A^\mu = (\phi/c, \boldsymbol{A})$ 在TUFT中完全由挠率场构造：

$$
A^\mu = (k_\phi \tau_t,\ k_A \boldsymbol{\tau})
$$

如果 $k_A = k_\phi = k$（耦合常数统一），则：

$$
A^\mu = k(\tau_t, \boldsymbol{\tau})
$$

## 8.5 电场和磁场的挠率表达

### 8.5.1 磁场

由 $\boldsymbol{B} = \nabla \times \boldsymbol{A}$ 和 $\boldsymbol{A} = k\boldsymbol{\tau}$：

$$
\boldsymbol{B} = k \nabla \times \boldsymbol{\tau}
$$

**定理8.1（磁场的挠率表达）：**

$$
\boldsymbol{B} = k \nabla \times \boldsymbol{\tau}
$$

磁场是矢量挠率场的旋度。

### 8.5.2 电场

标准电磁学中，电场由势导出：

$$
\boldsymbol{E} = -\nabla\phi - \frac{\partial \boldsymbol{A}}{\partial t}
$$

代入 $\phi = kc\tau_t$ 和 $\boldsymbol{A} = k\boldsymbol{\tau}$：

$$
\boldsymbol{E} = -k c \nabla\tau_t - k \frac{\partial \boldsymbol{\tau}}{\partial t} = -k\left(c\nabla\tau_t + \frac{\partial \boldsymbol{\tau}}{\partial t}\right)
$$

**定理8.2（电场的挠率表达）：**

$$
\boldsymbol{E} = -k\left(c\nabla\tau_t + \frac{\partial \boldsymbol{\tau}}{\partial t}\right)
$$

电场由挠率场的空间梯度和时间变化共同决定。

### 8.5.3 静电场特例

在静电场中（$\partial/\partial t = 0$）：

$$
\boldsymbol{E} = -kc\nabla\tau_t
$$

电场是标量挠率时间分量的负梯度，与标准静电学 $\boldsymbol{E} = -\nabla\phi$ 完全对应。

## 8.6 齐次麦克斯韦方程组的推导

### 8.6.1 高斯磁定律

**定理8.3（高斯磁定律）：**

$$
\nabla \cdot \boldsymbol{B} = 0
$$

**证明：**

代入 $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$：

$$
\nabla \cdot \boldsymbol{B} = k \nabla \cdot (\nabla \times \boldsymbol{\tau})
$$

由矢量恒等式：任意矢量场的旋度的散度恒为零，

$$
\nabla \cdot (\nabla \times \boldsymbol{X}) \equiv 0
$$

因此：

$$
\nabla \cdot \boldsymbol{B} = 0
$$

**证毕。**

这条定律是纯数学恒等式的结果，不需要额外的物理假设。它表明不存在磁单极子（至少在TUFT的基本框架中）。

### 8.6.2 法拉第电磁感应定律

**定理8.4（法拉第电磁感应定律）：**

$$
\nabla \times \boldsymbol{E} = -\frac{\partial \boldsymbol{B}}{\partial t}
$$

**证明：**

代入电场和磁场的挠率表达：

左边：

$$
\nabla \times \boldsymbol{E} = \nabla \times \left[-k\left(c\nabla\tau_t + \frac{\partial \boldsymbol{\tau}}{\partial t}\right)\right]
$$

$$
= -kc \nabla \times (\nabla\tau_t) - k \nabla \times \frac{\partial \boldsymbol{\tau}}{\partial t}
$$

由矢量恒等式：任意标量场的梯度的旋度恒为零，

$$
\nabla \times (\nabla f) \equiv 0
$$

第一项为零。交换旋度和时间导数的顺序：

$$
\nabla \times \boldsymbol{E} = -k \frac{\partial}{\partial t}(\nabla \times \boldsymbol{\tau})
$$

右边：

$$
-\frac{\partial \boldsymbol{B}}{\partial t} = -\frac{\partial}{\partial t}(k\nabla\times\boldsymbol{\tau}) = -k \frac{\partial}{\partial t}(\nabla \times \boldsymbol{\tau})
$$

左边等于右边。

**证毕。**

法拉第定律在 $k_e = k_m = k$（电场和磁场的耦合常数相等）的条件下严格成立。这个条件是自然的，因为电场和磁场都来自同一个挠率场。

### 8.6.3 齐次方程组总结

TUFT中，齐次麦克斯韦方程组

$$
\begin{cases}
\nabla \cdot \boldsymbol{B} = 0 \\
\nabla \times \boldsymbol{E} = -\dfrac{\partial \boldsymbol{B}}{\partial t}
\end{cases}
$$

是矢量微积分恒等式的直接结果，不需要额外物理假设。这是TUFT的一个优美性质：电磁学的基本方程从时空几何的拓扑结构中自然涌现。

## 8.7 非齐次麦克斯韦方程组

### 8.7.1 高斯电场定律

**定理8.5（高斯电场定律）：**

$$
\nabla \cdot \boldsymbol{E} = \frac{\rho_e}{\varepsilon_0}
$$

在静电极限下（$\partial/\partial t = 0$），代入 $\boldsymbol{E} = -kc\nabla\tau_t$：

$$
\nabla \cdot \boldsymbol{E} = -kc \nabla^2 \tau_t
$$

电荷密度 $\rho_e = k_q \nabla \cdot \boldsymbol{\tau}$。在静电场中，挠率场的空间分布满足泊松型方程，通过适当的耦合常数匹配，可以得到高斯电场定律。

完整的动态情况需要挠率场的波动方程（见下节），这里标记为**条件性定理**：在静电极限下成立，动态情况依赖挠率场波动方程的源项。

### 8.7.2 安培-麦克斯韦定律

**定理8.6（安培-麦克斯韦全电流定律）：**

$$
\nabla \times \boldsymbol{B} = \mu_0 \boldsymbol{J}_e + \mu_0\varepsilon_0 \frac{\partial \boldsymbol{E}}{\partial t}
$$

代入 $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$：

$$
\nabla \times \boldsymbol{B} = k \nabla \times (\nabla \times \boldsymbol{\tau})
$$

由矢量恒等式：

$$
\nabla \times (\nabla \times \boldsymbol{X}) = \nabla(\nabla \cdot \boldsymbol{X}) - \nabla^2 \boldsymbol{X}
$$

$$
\nabla \times \boldsymbol{B} = k\left[\nabla(\nabla \cdot \boldsymbol{\tau}) - \nabla^2 \boldsymbol{\tau}\right]
$$

引入达朗贝尔算子 $\square = \nabla^2 - \dfrac{1}{c^2}\dfrac{\partial^2}{\partial t^2}$：

$$
-\nabla^2 \boldsymbol{\tau} = -\square\boldsymbol{\tau} - \frac{1}{c^2}\frac{\partial^2 \boldsymbol{\tau}}{\partial t^2}
$$

因此：

$$
\nabla \times \boldsymbol{B} = k\left[\nabla(\nabla \cdot \boldsymbol{\tau}) - \square\boldsymbol{\tau} - \frac{1}{c^2}\frac{\partial^2 \boldsymbol{\tau}}{\partial t^2}\right]
$$

右边的安培-麦克斯韦项包含电流密度 $\boldsymbol{J}_e$ 和位移电流 $\partial\boldsymbol{E}/\partial t$。电流密度对应挠率场的时间变化：

$$
\boldsymbol{J}_e = k_J \frac{\partial \boldsymbol{\tau}}{\partial t}
$$

当挠率场满足波动方程 $\square\boldsymbol{\tau} = \mathcal{S}_\tau(\rho_e, \boldsymbol{J}_e)$（源项由电荷和电流决定）时，可以实现与安培-麦克斯韦定律的完全匹配。

这标记为**条件性定理**：依赖挠率场波动方程的源项 $\mathcal{S}_\tau$ 的具体形式，目前是开放命题。

## 8.8 挠率场的波动方程

**假设8.1（挠率场波动方程）：**

矢量挠率场满足达朗贝尔波动方程：

$$
\square \boldsymbol{\tau} = \mathcal{S}_\tau(\rho_e, \boldsymbol{J}_e)
$$

其中源项 $\mathcal{S}_\tau$ 由电荷密度和电流密度决定，具体形式需要进一步推导。

在无源区域（$\rho_e = 0, \boldsymbol{J}_e = 0$）：

$$
\square \boldsymbol{\tau} = 0
$$

这是标准的波动方程，描述挠率波（即电磁波）以光速传播。

### 8.8.1 电磁波的传播

无源波动方程的平面波解为：

$$
\boldsymbol{\tau}(\boldsymbol{r}, t) = \boldsymbol{\tau}_0 e^{i(\boldsymbol{k}\cdot\boldsymbol{r} - \omega t)}
$$

色散关系：$\omega = c|\boldsymbol{k}|$，即波以光速传播。这与电磁波的传播速度一致。✓

对应的电场和磁场：

$$
\boldsymbol{E} = -k\frac{\partial \boldsymbol{\tau}}{\partial t} = ik\omega \boldsymbol{\tau}_0 e^{i(\boldsymbol{k}\cdot\boldsymbol{r}-\omega t)}
$$

$$
\boldsymbol{B} = k\nabla\times\boldsymbol{\tau} = ik\boldsymbol{k}\times\boldsymbol{\tau}_0 e^{i(\boldsymbol{k}\cdot\boldsymbol{r}-\omega t)}
$$

$\boldsymbol{E} \perp \boldsymbol{B} \perp \boldsymbol{k}$，且 $|\boldsymbol{E}|/|\boldsymbol{B}| = c$，与标准电磁波完全一致。✓

## 8.9 与传统电磁学的映射总结

| 标准电磁学 | TUFT拓扑统一场论 | 关系 |
|------------|------------------|------|
| 矢量势 $\boldsymbol{A}$ | 矢量挠率场 $\boldsymbol{\tau}$ | $\boldsymbol{A} = k\boldsymbol{\tau}$ |
| 标量势 $\phi$ | 挠率时间分量 $\tau_t$ | $\phi = kc\tau_t$ |
| 磁场 $\boldsymbol{B}$ | 挠率场旋度 | $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$ |
| 电场 $\boldsymbol{E}$ | 挠率场梯度+时间导数 | $\boldsymbol{E} = -k(c\nabla\tau_t + \partial_t\boldsymbol{\tau})$ |
| 电荷密度 $\rho_e$ | 挠率场散度 | $\rho_e = k_q\nabla\cdot\boldsymbol{\tau}$ |
| 电流密度 $\boldsymbol{J}_e$ | 挠率场时间导数 | $\boldsymbol{J}_e = k_J\partial_t\boldsymbol{\tau}$ |
| 高斯磁定律 | 旋度散度恒等式 | 自动满足 |
| 法拉第定律 | 梯度旋度恒等式 | 条件 $k_e=k_m$ 下满足 |
| 高斯电场定律 | 挠率泊松方程 | 静电极限下成立 |
| 安培-麦克斯韦定律 | 挠率波动方程 | 依赖源项 $\mathcal{S}_\tau$ |
| 电磁波 | 挠率波 | 光速传播，横波 |

## 8.10 开放命题

1. **拓扑-电磁耦合常数 $k, k_q, k_J$**：这些常数的具体数值需要通过拓扑孤子散射求解，目前不能从第一性原理算出。它们对应现实中的 $\varepsilon_0, \mu_0, e$。
2. **挠率场波动方程源项 $\mathcal{S}_\tau$**：非齐次麦克斯韦方程组的完备推导依赖源项的具体形式，目前尚未从TUFT公理严格导出。
3. **四维协变形式**：当前推导主要在三维空间中进行，完整的四维协变形式需要进一步建立。
4. **磁单极子问题**：TUFT中 $\nabla\cdot\boldsymbol{B}=0$ 是恒等式，不允许磁单极子。但如果引入挠率场的拓扑缺陷（如纽结奇点），可能存在有效磁单极子，需要进一步研究。

## 8.11 本章小结

本章建立了TUFT的电磁理论：

1. **矢量挠率场**：$\boldsymbol{\tau} = \tau\boldsymbol{B}$，方向沿副法向，模为标量挠率；
2. **电荷的拓扑定义**：$q = k_q \oiint_S \boldsymbol{\tau}\cdot d\boldsymbol{S}$，电荷是挠率通量，挠率手性对应电荷正负；
3. **电磁势的挠率表达**：$\boldsymbol{A} = k\boldsymbol{\tau}$，$\phi = kc\tau_t$；
4. **电场和磁场**：$\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$，$\boldsymbol{E} = -k(c\nabla\tau_t + \partial_t\boldsymbol{\tau})$；
5. **齐次麦克斯韦方程组**：$\nabla\cdot\boldsymbol{B}=0$ 和 $\nabla\times\boldsymbol{E}=-\partial_t\boldsymbol{B}$ 是矢量微积分恒等式的直接结果，严格成立；
6. **非齐次麦克斯韦方程组**：高斯电场定律和安培-麦克斯韦定律在静电极限和挠率波动方程下成立，标记为条件性定理；
7. **电磁波**：挠率波以光速传播，横波，与标准电磁波完全一致；
8. **开放命题**：耦合常数、波动方程源项、四维协变形式。

**下一章预告：** 第9章将推导汤川核力势，从曲率场的短程衰减出发描述强相互作用。
