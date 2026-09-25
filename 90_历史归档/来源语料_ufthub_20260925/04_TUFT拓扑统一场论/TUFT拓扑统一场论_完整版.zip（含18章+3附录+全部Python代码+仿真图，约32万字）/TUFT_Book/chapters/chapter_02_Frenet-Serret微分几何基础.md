# 第2章 Frenet-Serret微分几何基础

## 2.1 曲线论的基本概念

微分几何中，曲线是最基本的研究对象。一条空间曲线可以用参数方程表示：

$$
\boldsymbol{r}(t) = \big(x(t),\ y(t),\ z(t)\big)
$$

其中 $t$ 是参数。如果参数 $t$ 是弧长 $s$（即从曲线某一点起算的曲线长度），则称为**自然参数化**或**弧长参数化**。弧长参数化的优越性在于：切向量的模恒等于1。

### 2.1.1 弧长参数化

对于任意参数化曲线 $\boldsymbol{r}(t)$，弧长元为：

$$
ds = \left|\frac{d\boldsymbol{r}}{dt}\right| dt = \sqrt{\dot{x}^2 + \dot{y}^2 + \dot{z}^2} \, dt
$$

从起点 $t_0$ 到 $t$ 的弧长为：

$$
s(t) = \int_{t_0}^{t} \left|\frac{d\boldsymbol{r}}{dt'}\right| dt'
$$

如果 $s(t)$ 单调递增，可以反解出 $t = t(s)$，从而得到弧长参数化曲线 $\boldsymbol{r}(s) = \boldsymbol{r}(t(s))$。

弧长参数化的关键性质：

$$
\left|\frac{d\boldsymbol{r}}{ds}\right| = 1
$$

即切向量是单位向量。

### 2.1.2 TUFT中的弧长参数化

在TUFT中，公理Ⅰ规定时空元世界线的总切向速率模恒等于 $c$。因此，世界线的弧长元为：

$$
ds = |\boldsymbol{v}_\mathrm{total}| \, dt = c \, dt
$$

这意味着TUFT中的世界线天然以弧长参数化，且弧长与时间的关系极其简单：$s = ct$（从 $t=0$ 起算）。

这一性质极大简化了后续推导：所有对时间的导数都可以直接转换为对弧长的导数：

$$
\frac{d}{dt} = c \frac{d}{ds}, \qquad \frac{d^2}{dt^2} = c^2 \frac{d^2}{ds^2}
$$

## 2.2 Frenet标架

对于一条弧长参数化的光滑曲线 $\boldsymbol{r}(s)$，可以在每一点建立一个正交标架——**Frenet标架**，由三个互相垂直的单位向量组成：

### 2.2.1 切向量 $\boldsymbol{T}$

切向量是曲线的一阶导数：

$$
\boldsymbol{T}(s) = \frac{d\boldsymbol{r}}{ds}
$$

由于弧长参数化，$|\boldsymbol{T}| = 1$。切向量指向曲线的前进方向。

在TUFT中，切向量 $\boldsymbol{T}$ 对应世界线的运动方向，即动量方向。三维动量可以表示为：

$$
\boldsymbol{p} = mc \boldsymbol{T}
$$

其中 $m$ 是拓扑质量（将在第5章导出），$c$ 是光速。

### 2.2.2 主法向量 $\boldsymbol{N}$ 与曲率 $\kappa$

对切向量求导：

$$
\frac{d\boldsymbol{T}}{ds} = \frac{d^2\boldsymbol{r}}{ds^2}
$$

由于 $\boldsymbol{T} \cdot \boldsymbol{T} = 1$，对 $s$ 求导得：

$$
2 \boldsymbol{T} \cdot \frac{d\boldsymbol{T}}{ds} = 0 \implies \boldsymbol{T} \cdot \frac{d\boldsymbol{T}}{ds} = 0
$$

即 $d\boldsymbol{T}/ds$ 与 $\boldsymbol{T}$ 垂直。定义**曲率** $\kappa(s)$ 为 $d\boldsymbol{T}/ds$ 的模：

$$
\kappa(s) = \left|\frac{d\boldsymbol{T}}{ds}\right| = \left|\frac{d^2\boldsymbol{r}}{ds^2}\right|
$$

定义**主法向量** $\boldsymbol{N}(s)$ 为 $d\boldsymbol{T}/ds$ 方向上的单位向量：

$$
\boldsymbol{N}(s) = \frac{1}{\kappa(s)} \frac{d\boldsymbol{T}}{ds}
$$

因此有Frenet第一公式：

$$
\frac{d\boldsymbol{T}}{ds} = \kappa \boldsymbol{N}
$$

**曲率的物理意义：** 曲率描述曲线偏离直线的程度。$\kappa = 0$ 对应直线，$\kappa$ 越大曲线弯曲越厉害。曲率的倒数 $\rho = 1/\kappa$ 称为**曲率半径**，对应曲线在该点的密切圆半径。

在TUFT中，曲率 $\kappa$ 是引力的几何本源。主法向量 $\boldsymbol{N}$ 指向曲线弯曲的方向，即引力加速度的方向。引力加速度为：

$$
\boldsymbol{g} = -c^2 \kappa \boldsymbol{N}
$$

这将在第6章详细推导。

### 2.2.3 副法向量 $\boldsymbol{B}$ 与挠率 $\tau$

定义**副法向量**为切向量与主法向量的叉积：

$$
\boldsymbol{B}(s) = \boldsymbol{T}(s) \times \boldsymbol{N}(s)
$$

由于 $\boldsymbol{T}$ 和 $\boldsymbol{N}$ 都是单位向量且互相垂直，$\boldsymbol{B}$ 也是单位向量，且与 $\boldsymbol{T}$、$\boldsymbol{N}$ 都垂直。$\{\boldsymbol{T}, \boldsymbol{N}, \boldsymbol{B}\}$ 构成右手正交标架。

对副法向量求导：

$$
\frac{d\boldsymbol{B}}{ds} = \frac{d\boldsymbol{T}}{ds} \times \boldsymbol{N} + \boldsymbol{T} \times \frac{d\boldsymbol{N}}{ds}
$$

第一项：$\dfrac{d\boldsymbol{T}}{ds} \times \boldsymbol{N} = \kappa \boldsymbol{N} \times \boldsymbol{N} = 0$。

因此：

$$
\frac{d\boldsymbol{B}}{ds} = \boldsymbol{T} \times \frac{d\boldsymbol{N}}{ds}
$$

这说明 $d\boldsymbol{B}/ds$ 与 $\boldsymbol{T}$ 垂直。又因为 $\boldsymbol{B} \cdot \boldsymbol{B} = 1$，所以 $d\boldsymbol{B}/ds$ 也与 $\boldsymbol{B}$ 垂直。因此 $d\boldsymbol{B}/ds$ 只能沿 $\boldsymbol{N}$ 方向。

定义**挠率** $\tau(s)$ 为：

$$
\frac{d\boldsymbol{B}}{ds} = -\tau \boldsymbol{N}
$$

负号是历史约定，使得右手螺旋的挠率为正。

**挠率的物理意义：** 挠率描述曲线偏离平面的程度，即曲线的扭曲程度。$\tau = 0$ 对应平面曲线（曲线完全在一个平面内），$\tau \neq 0$ 表示曲线离开平面发生扭曲。挠率的符号表示扭曲的手性（左旋或右旋）。

在TUFT中，挠率 $\tau$ 是电磁力的几何本源。副法向量 $\boldsymbol{B}$ 对应电磁力的方向，挠率的符号天然对应电荷的正负（手性）。这将在第8章详细推导。

### 2.2.4 Frenet第二公式

对主法向量 $\boldsymbol{N} = \boldsymbol{B} \times \boldsymbol{T}$ 求导：

$$
\frac{d\boldsymbol{N}}{ds} = \frac{d\boldsymbol{B}}{ds} \times \boldsymbol{T} + \boldsymbol{B} \times \frac{d\boldsymbol{T}}{ds}
$$

代入Frenet第一和第三公式：

$$
\frac{d\boldsymbol{N}}{ds} = (-\tau \boldsymbol{N}) \times \boldsymbol{T} + \boldsymbol{B} \times (\kappa \boldsymbol{N})
$$

利用叉积性质：$\boldsymbol{N} \times \boldsymbol{T} = -\boldsymbol{B}$，$\boldsymbol{B} \times \boldsymbol{N} = -\boldsymbol{T}$：

$$
\frac{d\boldsymbol{N}}{ds} = \tau \boldsymbol{B} - \kappa \boldsymbol{T} = -\kappa \boldsymbol{T} + \tau \boldsymbol{B}
$$

这就是Frenet第二公式。

## 2.3 Frenet-Serret公式汇总

完整的Frenet-Serret公式为：

$$
\begin{cases}
\dfrac{d\boldsymbol{T}}{ds} = \kappa \boldsymbol{N} \\[6pt]
\dfrac{d\boldsymbol{N}}{ds} = -\kappa \boldsymbol{T} + \tau \boldsymbol{B} \\[6pt]
\dfrac{d\boldsymbol{B}}{ds} = -\tau \boldsymbol{N}
\end{cases}
$$

可以写成矩阵形式：

$$
\frac{d}{ds}
\begin{pmatrix}
\boldsymbol{T} \\
\boldsymbol{N} \\
\boldsymbol{B}
\end{pmatrix}
=
\begin{pmatrix}
0 & \kappa & 0 \\
-\kappa & 0 & \tau \\
0 & -\tau & 0
\end{pmatrix}
\begin{pmatrix}
\boldsymbol{T} \\
\boldsymbol{N} \\
\boldsymbol{B}
\end{pmatrix}
$$

注意这个矩阵是反对称矩阵，这保证了Frenet标架的正交性在沿曲线移动时保持不变。

## 2.4 曲线论基本定理

**曲线论基本定理（存在唯一性定理）：**

给定区间 $I$ 上的连续函数 $\kappa(s) > 0$ 和 $\tau(s)$，则存在一条弧长参数化曲线 $\boldsymbol{r}(s)$，其曲率为 $\kappa(s)$，挠率为 $\tau(s)$。且这条曲线在刚体运动（平移+旋转）下唯一确定。

这条定理的意义在于：**曲率和挠率完全刻画了一条曲线的全部几何性质**（只差一个刚体运动）。换句话说，知道了 $\kappa(s)$ 和 $\tau(s)$，就知道了曲线的一切。

在TUFT中，公理Ⅱ将这条数学定理提升为物理公理：时空世界线的全部物理信息都编码在 $\kappa(s)$ 和 $\tau(s)$ 中。这是TUFT能够用曲率和挠率统一描述全部物理现象的数学基础。

## 2.5 圆柱螺旋线的Frenet-Serret分析

圆柱螺旋线是TUFT中最重要的曲线，因为它是曲率和挠率均为常数的唯一曲线（稳态解）。下面详细推导其Frenet-Serret性质。

### 2.5.1 参数方程

圆柱螺旋线的参数方程为：

$$
\boldsymbol{r}(t) = \big(R\cos\omega t,\ R\sin\omega t,\ h\,t\big)
$$

其中：
- $R$ 是螺旋半径（圆柱半径）；
- $\omega$ 是角频率（旋转角速度）；
- $h$ 是轴向速率（沿z轴的匀速运动速度）。

### 2.5.2 速度与弧长

对 $t$ 求导得到速度：

$$
\dot{\boldsymbol{r}}(t) = \big(-R\omega\sin\omega t,\ R\omega\cos\omega t,\ h\big)
$$

速度的模为：

$$
|\dot{\boldsymbol{r}}| = \sqrt{R^2\omega^2 + h^2}
$$

在TUFT中，公理Ⅰ要求总速率模等于 $c$：

$$
\sqrt{R^2\omega^2 + h^2} = c \implies (R\omega)^2 + h^2 = c^2
$$

其中 $v_\perp = R\omega$ 是切向旋转速率。因此：

$$
v_\perp^2 + h^2 = c^2
$$

弧长元：

$$
ds = |\dot{\boldsymbol{r}}| dt = c \, dt
$$

### 2.5.3 切向量

切向量为：

$$
\boldsymbol{T} = \frac{d\boldsymbol{r}}{ds} = \frac{\dot{\boldsymbol{r}}}{c} = \left(-\frac{R\omega}{c}\sin\omega t,\ \frac{R\omega}{c}\cos\omega t,\ \frac{h}{c}\right)
$$

验证 $|\boldsymbol{T}| = 1$：

$$
|\boldsymbol{T}|^2 = \frac{R^2\omega^2}{c^2} + \frac{h^2}{c^2} = \frac{R^2\omega^2 + h^2}{c^2} = \frac{c^2}{c^2} = 1
$$

### 2.5.4 曲率与主法向量

对切向量关于 $s$ 求导：

$$
\frac{d\boldsymbol{T}}{ds} = \frac{1}{c}\frac{d\boldsymbol{T}}{dt} = \frac{1}{c}\left(-\frac{R\omega^2}{c}\cos\omega t,\ -\frac{R\omega^2}{c}\sin\omega t,\ 0\right)
$$

曲率为其模：

$$
\kappa = \left|\frac{d\boldsymbol{T}}{ds}\right| = \frac{R\omega^2}{c^2}
$$

主法向量为：

$$
\boldsymbol{N} = \frac{1}{\kappa}\frac{d\boldsymbol{T}}{ds} = (-\cos\omega t,\ -\sin\omega t,\ 0)
$$

主法向量指向圆柱轴线方向（径向向内），这正是向心加速度的方向。

### 2.5.5 副法向量与挠率

副法向量：

$$
\boldsymbol{B} = \boldsymbol{T} \times \boldsymbol{N}
$$

计算叉积：

$$
\boldsymbol{B} = \begin{vmatrix}
\boldsymbol{i} & \boldsymbol{j} & \boldsymbol{k} \\
-\frac{R\omega}{c}\sin\omega t & \frac{R\omega}{c}\cos\omega t & \frac{h}{c} \\
-\cos\omega t & -\sin\omega t & 0
\end{vmatrix}
$$

$$
= \left(\frac{h}{c}\sin\omega t,\ -\frac{h}{c}\cos\omega t,\ \frac{R\omega}{c}\right)
$$

对副法向量关于 $s$ 求导：

$$
\frac{d\boldsymbol{B}}{ds} = \frac{1}{c}\frac{d\boldsymbol{B}}{dt} = \frac{1}{c}\left(\frac{h\omega}{c}\cos\omega t,\ \frac{h\omega}{c}\sin\omega t,\ 0\right)
$$

根据Frenet第三公式 $d\boldsymbol{B}/ds = -\tau \boldsymbol{N}$，而 $\boldsymbol{N} = (-\cos\omega t, -\sin\omega t, 0)$，所以：

$$
-\tau \boldsymbol{N} = (\tau\cos\omega t,\ \tau\sin\omega t,\ 0)
$$

对比得：

$$
\tau = \frac{h\omega}{c^2}
$$

### 2.5.6 圆柱螺旋的几何性质汇总

圆柱螺旋线的全部Frenet-Serret性质：

| 物理量 | 表达式 |
|--------|--------|
| 参数方程 | $\boldsymbol{r}(t) = (R\cos\omega t, R\sin\omega t, ht)$ |
| 切向速率 | $v_\perp = R\omega$ |
| 速率守恒 | $v_\perp^2 + h^2 = c^2$ |
| 切向量 | $\boldsymbol{T} = (-\frac{v_\perp}{c}\sin\omega t, \frac{v_\perp}{c}\cos\omega t, \frac{h}{c})$ |
| 主法向量 | $\boldsymbol{N} = (-\cos\omega t, -\sin\omega t, 0)$ |
| 副法向量 | $\boldsymbol{B} = (\frac{h}{c}\sin\omega t, -\frac{h}{c}\cos\omega t, \frac{v_\perp}{c})$ |
| 曲率 | $\kappa = \frac{R\omega^2}{c^2} = \frac{v_\perp \omega}{c^2}$ |
| 挠率 | $\tau = \frac{h\omega}{c^2}$ |
| 曲率/挠率比 | $\frac{\kappa}{\tau} = \frac{v_\perp}{h}$ |

这些结果是TUFT后续所有推导的基础。第3章将在此基础上，结合公理Ⅰ，导出稳态圆柱螺旋的全部恒等式。

## 2.6 本章小结

本章详细回顾了Frenet-Serret微分几何的数学基础：

1. 弧长参数化：$ds = c\,dt$，切向量模为1；
2. Frenet标架：$\{\boldsymbol{T}, \boldsymbol{N}, \boldsymbol{B}\}$ 构成右手正交标架；
3. Frenet-Serret公式：$d\boldsymbol{T}/ds = \kappa\boldsymbol{N}$，$d\boldsymbol{N}/ds = -\kappa\boldsymbol{T} + \tau\boldsymbol{B}$，$d\boldsymbol{B}/ds = -\tau\boldsymbol{N}$；
4. 曲线论基本定理：曲率和挠率完全刻画曲线；
5. 圆柱螺旋线的完整Frenet-Serret分析：$\kappa = R\omega^2/c^2$，$\tau = h\omega/c^2$。

TUFT的物理诠释：
- 切向量 $\boldsymbol{T}$ → 动量方向；
- 主法向量 $\boldsymbol{N}$ + 曲率 $\kappa$ → 引力；
- 副法向量 $\boldsymbol{B}$ + 挠率 $\tau$ → 电磁力（手性对应电荷正负）。

**下一章预告：** 第3章将从公理Ⅰ和公理Ⅱ严格导出稳态圆柱螺旋的全部几何恒等式，包括核心公式 $\omega = c\sqrt{\kappa^2+\tau^2}$ 和 $\tan\theta = \kappa/\tau$。
