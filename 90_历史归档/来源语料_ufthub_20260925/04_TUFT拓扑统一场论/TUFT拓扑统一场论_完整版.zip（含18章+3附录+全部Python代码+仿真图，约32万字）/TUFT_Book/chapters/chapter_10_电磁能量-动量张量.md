# 第10章 电磁能量-动量张量

## 10.1 能量-动量张量的物理意义

能量-动量张量（应力-能量张量）$T^{\mu\nu}$ 是相对论物理学中描述物质和场的能量、动量分布及应力状态的核心物理量。它是广义相对论爱因斯坦方程的源项，决定了时空的曲率。

对于电磁场，能量-动量张量描述了电磁场的能量密度、能流密度（坡印廷矢量）、动量密度和麦克斯韦应力张量。

在TUFT中，电磁场完全由矢量挠率场 $\boldsymbol{\tau}$ 描述，因此电磁能量-动量张量也必须用挠率场表达。本章将建立TUFT框架下的电磁能量-动量张量。

## 10.2 标准电磁能量-动量张量回顾

### 10.2.1 电磁场张量

标准电磁学中，电磁场张量 $F_{\mu\nu}$ 定义为：

$$
F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu
$$

其中 $A_\mu = (\phi/c, -\boldsymbol{A})$ 是四维势。

电磁场张量的分量为：

$$
F^{0i} = -\frac{E_i}{c}, \quad F^{ij} = -\epsilon^{ijk} B_k
$$

矩阵形式：

$$
F^{\mu\nu} =
\begin{pmatrix}
0 & -E_x/c & -E_y/c & -E_z/c \\
E_x/c & 0 & -B_z & B_y \\
E_y/c & B_z & 0 & -B_x \\
E_z/c & -B_y & B_x & 0
\end{pmatrix}
$$

### 10.2.2 电磁能量-动量张量

标准电磁能量-动量张量为：

$$
T^{\mu\nu}_\mathrm{EM} = \epsilon_0\left(F^{\mu\alpha}F^{\nu}_{~\alpha} - \frac{1}{4}\eta^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\right)
$$

其中 $\eta^{\mu\nu} = \mathrm{diag}(1, -1, -1, -1)$ 是闵氏度规。

### 10.2.3 三维分量分解

**能量密度（$T^{00}$）：**

$$
u = T^{00} = \frac{1}{2}\left(\epsilon_0 |\boldsymbol{E}|^2 + \frac{1}{\mu_0}|\boldsymbol{B}|^2\right)
$$

**能流密度/坡印廷矢量（$T^{0i} = T^{i0}$）：**

$$
\boldsymbol{S} = c T^{0i} = \frac{1}{\mu_0}\boldsymbol{E} \times \boldsymbol{B}
$$

**动量密度：**

$$
\boldsymbol{g} = \frac{\boldsymbol{S}}{c^2} = \epsilon_0 \boldsymbol{E} \times \boldsymbol{B}
$$

**麦克斯韦应力张量（$T^{ij}$）：**

$$
\sigma_{ij} = \epsilon_0 E_i E_j + \frac{1}{\mu_0}B_i B_j - \frac{1}{2}\delta_{ij}\left(\epsilon_0 |\boldsymbol{E}|^2 + \frac{1}{\mu_0}|\boldsymbol{B}|^2\right)
$$

### 10.2.4 能量守恒定律

电磁能量-动量张量的散度为零（无源区域）：

$$
\partial_\mu T^{\mu\nu} = 0
$$

这对应能量守恒和动量守恒。$\nu = 0$ 分量为：

$$
\frac{\partial u}{\partial t} + \nabla \cdot \boldsymbol{S} = -\boldsymbol{J} \cdot \boldsymbol{E}
$$

即坡印廷定理：电磁场能量的变化率等于能流的散度加上场对电荷做的功。

## 10.3 TUFT中电磁场张量的挠率表达

### 10.3.1 四维势的挠率表达

由第8章，TUFT中电磁四维势完全由挠率场构造：

$$
A^\mu = k(\tau_t, \boldsymbol{\tau})
$$

其中 $\tau_t$ 是挠率场的时间分量（标量部分），$\boldsymbol{\tau}$ 是矢量挠率场，$k$ 是拓扑-电磁耦合常数。

协变分量：

$$
A_\mu = k(\tau_t, -\boldsymbol{\tau})
$$

（度规约定 $\eta_{\mu\nu} = \mathrm{diag}(1, -1, -1, -1)$。）

### 10.3.2 电磁场张量

由 $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$，代入挠率势：

$$
F_{0i} = \partial_0 A_i - \partial_i A_0 = \frac{1}{c}\frac{\partial}{\partial t}(-k\tau_i) - \frac{\partial}{\partial x^i}(k\tau_t)
$$

$$
= -\frac{k}{c}\frac{\partial \tau_i}{\partial t} - k \frac{\partial \tau_t}{\partial x^i}
$$

而标准电磁学中 $F_{0i} = E_i/c$（注意符号约定），因此：

$$
\frac{E_i}{c} = -\frac{k}{c}\frac{\partial \tau_i}{\partial t} - k \frac{\partial \tau_t}{\partial x^i}
$$

$$
E_i = -k\left(\frac{\partial \tau_i}{\partial t} + c \frac{\partial \tau_t}{\partial x^i}\right)
$$

这与第8章的结果 $\boldsymbol{E} = -k(c\nabla\tau_t + \partial_t\boldsymbol{\tau})$ 完全一致。✓

空间分量：

$$
F_{ij} = \partial_i A_j - \partial_j A_i = \frac{\partial}{\partial x^i}(-k\tau_j) - \frac{\partial}{\partial x^j}(-k\tau_i) = k\left(\frac{\partial \tau_i}{\partial x^j} - \frac{\partial \tau_j}{\partial x^i}\right)
$$

而 $F_{ij} = -\epsilon_{ijk} B_k$，因此：

$$
-\epsilon_{ijk} B_k = k\left(\partial_j \tau_i - \partial_i \tau_j\right) = -k \epsilon_{ijk} (\nabla \times \boldsymbol{\tau})_k
$$

$$
B_k = k (\nabla \times \boldsymbol{\tau})_k
$$

即 $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$，与第8章一致。✓

### 10.3.3 电磁场张量的挠率表达

完整的电磁场张量用挠率场表达为：

$$
F_{\mu\nu}(\boldsymbol{\tau}) = k(\partial_\mu \tau_\nu - \partial_\nu \tau_\mu)
$$

其中 $\tau_\mu = (\tau_t, -\boldsymbol{\tau})$ 是挠率四维矢量。

这是一个非常简洁的结果：**电磁场张量就是挠率四维矢量的旋度**。

## 10.4 TUFT电磁能量-动量张量

### 10.4.1 张量形式

将 $F_{\mu\nu}(\boldsymbol{\tau})$ 代入标准电磁能量-动量张量公式，得到TUFT电磁能量-动量张量：

$$
\boldsymbol{T^{\mu\nu}_\tau = \mathcal{E}_\tau\left(F^{\mu\alpha}(\boldsymbol{\tau})F^{\nu}_{~\alpha}(\boldsymbol{\tau}) - \frac{1}{4}\eta^{\mu\nu}F_{\alpha\beta}(\boldsymbol{\tau})F^{\alpha\beta}(\boldsymbol{\tau})\right)}
$$

其中 $\mathcal{E}_\tau$ 是TUFT拓扑等效介电常数，对应标准电磁学中的 $\epsilon_0$。

拓扑等效磁导率 $\mathcal{M}_\tau$ 满足：

$$
c^2 = \frac{1}{\mathcal{E}_\tau \mathcal{M}_\tau}
$$

与标准电磁学 $c^2 = 1/(\epsilon_0\mu_0)$ 完全同构。

### 10.4.2 三维分量分解

**能量密度：**

$$
u_\tau = T^{00}_\tau = \frac{1}{2}\left(\mathcal{E}_\tau |\boldsymbol{E}|^2 + \frac{1}{\mathcal{M}_\tau}|\boldsymbol{B}|^2\right)
$$

代入 $\boldsymbol{E} = -k(c\nabla\tau_t + \partial_t\boldsymbol{\tau})$ 和 $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$：

$$
u_\tau = \frac{k^2}{2}\left[\mathcal{E}_\tau |c\nabla\tau_t + \partial_t\boldsymbol{\tau}|^2 + \frac{1}{\mathcal{M}_\tau}|\nabla\times\boldsymbol{\tau}|^2\right]
$$

**坡印廷矢量：**

$$
\boldsymbol{S}_\tau = \frac{1}{\mathcal{M}_\tau}\boldsymbol{E} \times \boldsymbol{B} = -\frac{k^2}{\mathcal{M}_\tau}(c\nabla\tau_t + \partial_t\boldsymbol{\tau}) \times (\nabla\times\boldsymbol{\tau})
$$

**动量密度：**

$$
\boldsymbol{g}_\tau = \frac{\boldsymbol{S}_\tau}{c^2} = \mathcal{E}_\tau \boldsymbol{E} \times \boldsymbol{B}
$$

**麦克斯韦应力张量：**

$$
\sigma_{ij}^{(\tau)} = \mathcal{E}_\tau E_i E_j + \frac{1}{\mathcal{M}_\tau}B_i B_j - \frac{1}{2}\delta_{ij}\left(\mathcal{E}_\tau |\boldsymbol{E}|^2 + \frac{1}{\mathcal{M}_\tau}|\boldsymbol{B}|^2\right)
$$

## 10.5 静态场的能量-动量张量

### 10.5.1 静电场

在静电场中（$\partial_t = 0$, $\boldsymbol{B} = 0$）：

$$
\boldsymbol{E} = -kc\nabla\tau_t
$$

能量密度：

$$
u_\tau = \frac{1}{2}\mathcal{E}_\tau |\boldsymbol{E}|^2 = \frac{k^2 c^2 \mathcal{E}_\tau}{2} |\nabla\tau_t|^2
$$

坡印廷矢量：$\boldsymbol{S}_\tau = 0$（无磁场，无能流）。

应力张量：

$$
\sigma_{ij}^{(\tau)} = \mathcal{E}_\tau E_i E_j - \frac{1}{2}\delta_{ij}\mathcal{E}_\tau |\boldsymbol{E}|^2
$$

### 10.5.2 静磁场

在静磁场中（$\partial_t = 0$, $\boldsymbol{E} = 0$）：

$$
\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}
$$

能量密度：

$$
u_\tau = \frac{1}{2\mathcal{M}_\tau}|\boldsymbol{B}|^2 = \frac{k^2}{2\mathcal{M}_\tau}|\nabla\times\boldsymbol{\tau}|^2
$$

应力张量：

$$
\sigma_{ij}^{(\tau)} = \frac{1}{\mathcal{M}_\tau}B_i B_j - \frac{1}{2}\delta_{ij}\frac{|\boldsymbol{B}|^2}{\mathcal{M}_\tau}
$$

### 10.5.3 点电荷的静电能

对于点电荷 $q$，电场 $E = q/(4\pi\mathcal{E}_\tau r^2)$。

总静电能：

$$
U = \int u_\tau dV = \int \frac{1}{2}\mathcal{E}_\tau E^2 \cdot 4\pi r^2 dr = \frac{q^2}{8\pi\mathcal{E}_\tau} \int \frac{dr}{r^2}
$$

这个积分在 $r \to 0$ 时发散，这就是经典电动力学中的电子自能发散问题。

在TUFT中，这个发散可能被孤子的有限核心尺寸截断。孤子核心有最小尺寸（约为康普顿波长或普朗克长度），积分下限不为零，因此自能有限。这是TUFT对经典发散问题的可能解决方案，但需要进一步研究。

## 10.6 电磁波的能量-动量张量

### 10.6.1 平面电磁波

对于平面电磁波，$\boldsymbol{E} \perp \boldsymbol{B} \perp \boldsymbol{k}$，且 $|\boldsymbol{E}| = c|\boldsymbol{B}|$。

能量密度：

$$
u_\tau = \frac{1}{2}\left(\mathcal{E}_\tau |\boldsymbol{E}|^2 + \frac{1}{\mathcal{M}_\tau}|\boldsymbol{B}|^2\right) = \mathcal{E}_\tau |\boldsymbol{E}|^2 = \frac{|\boldsymbol{B}|^2}{\mathcal{M}_\tau}
$$

（电场和磁场能量各占一半。）

坡印廷矢量：

$$
\boldsymbol{S}_\tau = \frac{1}{\mathcal{M}_\tau}\boldsymbol{E} \times \boldsymbol{B}
$$

大小：

$$
|\boldsymbol{S}_\tau| = \frac{|\boldsymbol{E}||\boldsymbol{B}|}{\mathcal{M}_\tau} = \frac{|\boldsymbol{E}|^2}{c\mathcal{M}_\tau} = c\mathcal{E}_\tau |\boldsymbol{E}|^2 = c u_\tau
$$

即能流密度等于能量密度乘以光速，这与电磁波以光速传播能量一致。✓

动量密度：

$$
|\boldsymbol{g}_\tau| = \frac{u_\tau}{c}
$$

这与光子的能量-动量关系 $E = pc$ 一致。✓

### 10.6.2 辐射压力

电磁波对完全吸收体的辐射压力为：

$$
P = |\boldsymbol{g}_\tau| c = u_\tau
$$

对完全反射体的辐射压力为 $P = 2u_\tau$。

这与标准电磁学结果一致。✓

## 10.7 能量守恒的挠率表达

电磁能量守恒定律（坡印廷定理）：

$$
\frac{\partial u_\tau}{\partial t} + \nabla \cdot \boldsymbol{S}_\tau = -\boldsymbol{J}_e \cdot \boldsymbol{E}
$$

用挠率场表达：

左边第一项：

$$
\frac{\partial u_\tau}{\partial t} = k^2\left[\mathcal{E}_\tau (c\nabla\tau_t + \partial_t\boldsymbol{\tau}) \cdot (c\nabla\partial_t\tau_t + \partial_t^2\boldsymbol{\tau}) + \frac{1}{\mathcal{M}_\tau}(\nabla\times\boldsymbol{\tau}) \cdot (\nabla\times\partial_t\boldsymbol{\tau})\right]
$$

左边第二项：

$$
\nabla \cdot \boldsymbol{S}_\tau = -\frac{k^2}{\mathcal{M}_\tau}\nabla \cdot \left[(c\nabla\tau_t + \partial_t\boldsymbol{\tau}) \times (\nabla\times\boldsymbol{\tau})\right]
$$

右边：

$$
-\boldsymbol{J}_e \cdot \boldsymbol{E} = k_J k \frac{\partial \boldsymbol{\tau}}{\partial t} \cdot (c\nabla\tau_t + \partial_t\boldsymbol{\tau})
$$

在挠率场满足波动方程 $\square\boldsymbol{\tau} = \mathcal{S}_\tau$ 的条件下，这个守恒定律可以从波动方程直接导出。这是能量守恒的拓扑表达。

## 10.8 数值验证

### 10.8.1 正交场验证

取 $\boldsymbol{E} = (1, 0, 0)$ V/m，$\boldsymbol{B} = (0, 1, 0)$ T（正交场）。

能量密度：

$u = 0.5 \times (\epsilon_0 \times 1^2 + 1^2/\mu_0) = 0.5 \times (8.854 \times 10^{-12} + 7.958 \times 10^5) = 3.979 \times 10^5$ J/m³

坡印廷矢量：

$\boldsymbol{S} = (1/\mu_0) \boldsymbol{E} \times \boldsymbol{B} = (1/\mu_0)(0, 0, 1) = (0, 0, 7.958 \times 10^5)$ W/m²

动量密度：

$\boldsymbol{g} = \epsilon_0 \boldsymbol{E} \times \boldsymbol{B} = (0, 0, 8.854 \times 10^{-12})$ kg/(m²·s)

验证 $\boldsymbol{g} = \boldsymbol{S}/c^2$：

$S/c^2 = 7.958 \times 10^5 / (2.998 \times 10^8)^2 = 8.854 \times 10^{-12}$ ✓

### 10.8.2 平面电磁波验证

取平面波 $E_0 = 1$ V/m，$B_0 = E_0/c = 3.336 \times 10^{-9}$ T。

能量密度：

$u = \epsilon_0 E_0^2 = 8.854 \times 10^{-12}$ J/m³

坡印廷矢量大小：

$S = E_0 B_0 / \mu_0 = 1 \times 3.336 \times 10^{-9} / (1.257 \times 10^{-6}) = 2.654 \times 10^{-3}$ W/m²

验证 $S = cu$：

$cu = 2.998 \times 10^8 \times 8.854 \times 10^{-12} = 2.654 \times 10^{-3}$ ✓

## 10.9 与广义相对论的衔接

在广义相对论中，能量-动量张量是爱因斯坦方程的源项：

$$
G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}
$$

其中 $G_{\mu\nu}$ 是爱因斯坦张量。

在TUFT中，总能量-动量张量应包含：
1. 电磁能量-动量张量 $T^{\mu\nu}_\tau$（挠率场）；
2. 引力/曲率场的能量-动量张量；
3. 物质（孤子）的能量-动量张量。

目前，TUFT中完整的总能量-动量张量及其与爱因斯坦方程的对应关系是**开放命题**，需要进一步的四维协变理论构建。

## 10.10 本章小结

本章建立了TUFT框架下的电磁能量-动量张量：

1. **电磁场张量的挠率表达**：$F_{\mu\nu} = k(\partial_\mu\tau_\nu - \partial_\nu\tau_\mu)$，电磁场张量是挠率四维矢量的旋度；
2. **TUFT电磁能量-动量张量**：$T^{\mu\nu}_\tau = \mathcal{E}_\tau[F^{\mu\alpha}F^\nu_\alpha - \frac{1}{4}\eta^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}]$，用挠率场完全表达；
3. **三维分量分解**：能量密度、坡印廷矢量、动量密度、麦克斯韦应力张量，全部用挠率场的梯度和旋度表达；
4. **静态场**：静电场和静磁场的能量-动量张量简化形式；
5. **电磁波**：平面电磁波的能量密度 $u = \epsilon_0 E^2$，能流 $S = cu$，动量密度 $g = u/c$，与标准结果一致；
6. **能量守恒**：坡印廷定理的挠率表达，从挠率波动方程导出；
7. **数值验证**：正交场和平面波的能量、动量关系验证通过；
8. **开放命题**：完整的总能量-动量张量与广义相对论爱因斯坦方程的衔接。

**下一章预告：** 第11章将进行TUFT薛定谔方程的形式化推导，从拓扑孤子的波动性质出发建立量子力学的几何基础。
