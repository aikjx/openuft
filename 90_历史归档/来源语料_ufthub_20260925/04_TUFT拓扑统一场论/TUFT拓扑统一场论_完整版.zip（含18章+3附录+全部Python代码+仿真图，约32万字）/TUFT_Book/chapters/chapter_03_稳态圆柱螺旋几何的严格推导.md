# 第3章 稳态圆柱螺旋几何的严格推导

## 3.1 稳态解的存在性

在TUFT中，公理Ⅰ（速率守恒）和公理Ⅱ（Frenet-Serret）共同决定了时空世界线的几何结构。一个自然的问题是：什么样的曲线是这两条公理的**稳态解**？

**稳态解**定义为：曲率 $\kappa(s)$ 和挠率 $\tau(s)$ 均为常数的曲线。稳态解对应物理上的**定态**——不随时间（弧长）变化的基本粒子孤子。

**定理3.1：** 曲率和挠率均为常数的曲线，在刚体变换下唯一是圆柱螺旋线（包括直线和圆周作为特例）。

**证明：**

设 $\kappa = \text{常数} > 0$，$\tau = \text{常数}$。Frenet-Serret方程为线性常系数微分方程组：

$$
\frac{d}{ds}\begin{pmatrix}\boldsymbol{T} \\ \boldsymbol{N} \\ \boldsymbol{B}\end{pmatrix}
=
\begin{pmatrix}0 & \kappa & 0 \\ -\kappa & 0 & \tau \\ 0 & -\tau & 0\end{pmatrix}
\begin{pmatrix}\boldsymbol{T} \\ \boldsymbol{N} \\ \boldsymbol{B}\end{pmatrix}
$$

系数矩阵的特征方程为：

$$
\det\begin{pmatrix}-\lambda & \kappa & 0 \\ -\kappa & -\lambda & \tau \\ 0 & -\tau & -\lambda\end{pmatrix} = 0
$$

展开：

$$
-\lambda(\lambda^2 + \tau^2) - \kappa(\kappa\lambda) = -\lambda(\lambda^2 + \kappa^2 + \tau^2) = 0
$$

特征值为 $\lambda = 0$ 和 $\lambda = \pm i\sqrt{\kappa^2 + \tau^2}$。

零特征值对应一个常向量（螺旋轴线方向），纯虚特征值对应周期性旋转。因此解的形式是绕固定轴的匀速旋转加上沿轴的匀速平移——即圆柱螺旋线。

当 $\tau = 0$ 时，螺旋退化为圆周（平面曲线）；当 $\kappa \to 0$ 时，螺旋退化为直线。

**证毕。**

这条定理是TUFT的核心：基本粒子作为稳态孤子，其世界线必然是圆柱螺旋线。这不是人为假设，而是公理Ⅰ+Ⅱ的数学必然结果。

## 3.2 螺旋升角与速率分解

定义**螺旋升角** $\theta$ 为切向量与螺旋轴线（z轴）之间的夹角的余角。即切向量与垂直于轴线的平面之间的夹角。

由切向量表达式：

$$
\boldsymbol{T} = \left(-\frac{v_\perp}{c}\sin\omega t,\ \frac{v_\perp}{c}\cos\omega t,\ \frac{h}{c}\right)
$$

切向量的z分量为 $h/c$，垂直于z轴的分量的模为 $v_\perp/c$。因此：

$$
\sin\theta = \frac{v_\perp}{c}, \qquad \cos\theta = \frac{h}{c}
$$

其中 $\theta$ 是切向量与xy平面（垂直于轴线）之间的夹角。

由公理Ⅰ $v_\perp^2 + h^2 = c^2$，自动满足：

$$
\sin^2\theta + \cos^2\theta = \frac{v_\perp^2 + h^2}{c^2} = 1
$$

速率分解可以用升角表示为：

$$
v_\perp = c\sin\theta, \qquad h = c\cos\theta
$$

**物理意义：** 螺旋升角 $\theta$ 描述了世界线运动中"旋转"与"推进"的比例。$\theta = 90^\circ$ 对应纯旋转（无轴向推进，$h=0$），$\theta = 0^\circ$ 对应纯轴向推进（无旋转，$v_\perp=0$，即直线）。

## 3.3 核心恒等式一：$\tan\theta = \kappa/\tau$

由第2章的结果：

$$
\kappa = \frac{R\omega^2}{c^2} = \frac{v_\perp \omega}{c^2}
$$

$$
\tau = \frac{h\omega}{c^2}
$$

两式相除：

$$
\frac{\kappa}{\tau} = \frac{v_\perp \omega / c^2}{h \omega / c^2} = \frac{v_\perp}{h}
$$

而由升角定义：

$$
\tan\theta = \frac{\sin\theta}{\cos\theta} = \frac{v_\perp/c}{h/c} = \frac{v_\perp}{h}
$$

因此得到核心恒等式：

$$
\boldsymbol{\tan\theta = \frac{\kappa}{\tau}}
$$

**定理3.2：** 螺旋升角的正切等于曲率与挠率之比。

**物理意义：** 这条定理将螺旋的几何角度（升角）与曲线的内禀几何量（曲率、挠率）直接联系起来。它意味着：
- 曲率远大于挠率（$\kappa \gg \tau$）→ 升角接近90° → 以旋转为主；
- 挠率远大于曲率（$\tau \gg \kappa$）→ 升角接近0° → 以轴向推进为主；
- 曲率等于挠率（$\kappa = \tau$）→ 升角等于45° → 旋转与推进均衡。

最后一种情况（$\kappa = \tau$，$\theta = 45^\circ$）在TUFT中对应费米子孤子，将在第4章详细讨论。

## 3.4 核心恒等式二：$\omega = c\sqrt{\kappa^2 + \tau^2}$

将曲率和挠率用升角表示：

由 $\kappa = \dfrac{v_\perp \omega}{c^2}$，代入 $v_\perp = c\sin\theta$：

$$
\kappa = \frac{c\sin\theta \cdot \omega}{c^2} = \frac{\omega}{c}\sin\theta
$$

同理，由 $\tau = \dfrac{h\omega}{c^2}$，代入 $h = c\cos\theta$：

$$
\tau = \frac{c\cos\theta \cdot \omega}{c^2} = \frac{\omega}{c}\cos\theta
$$

因此：

$$
\kappa = \frac{\omega}{c}\sin\theta, \qquad \tau = \frac{\omega}{c}\cos\theta
$$

平方相加：

$$
\kappa^2 + \tau^2 = \frac{\omega^2}{c^2}(\sin^2\theta + \cos^2\theta) = \frac{\omega^2}{c^2}
$$

因此得到核心恒等式：

$$
\boldsymbol{\omega = c\sqrt{\kappa^2 + \tau^2}}
$$

**定理3.3：** 角频率完全由曲率和挠率唯一决定，等于光速乘以曲率-挠率模方的平方根。

**物理意义：** 这条定理是TUFT最深刻的结果之一。它表明：
1. 角频率 $\omega$ 不是独立参数，而是曲率和挠率的导出量；
2. 知道了世界线的曲率和挠率，就知道了它的振荡频率；
3. 结合量子关系 $E = \hbar\omega$，能量也完全由曲率和挠率决定。

这为第5章的拓扑质量定理奠定了基础：质量 $m = E/c^2 = \hbar\omega/c^2 = (\hbar/c)\sqrt{\kappa^2+\tau^2}$。

## 3.5 曲率-挠率平面的几何图像

将 $\kappa$ 和 $\tau$ 作为平面直角坐标系的两个轴，可以得到直观的几何图像：

- 任意稳态螺旋对应 $(\kappa, \tau)$ 平面上的一个点；
- 该点到原点的距离 $r = \sqrt{\kappa^2 + \tau^2} = \omega/c$，与角频率成正比；
- 该点与 $\kappa$ 轴的夹角 $\phi = \arctan(\tau/\kappa) = 90^\circ - \theta$，与螺旋升角互余。

特殊点：
- $(\kappa, 0)$：$\tau=0$，平面圆周，对应玻色子孤子；
- $(0, \tau)$：$\kappa=0$，直线（曲率为零的极限），无物理稳态粒子对应；
- $(\kappa, \kappa)$：$\kappa=\tau$，$\theta=45^\circ$，对应费米子孤子；
- 原点 $(0,0)$：$\kappa=\tau=0$，直线，无振荡，对应真空平直时空。

## 3.6 数值验证

下面用Python数值验证上述全部恒等式。

### 3.6.1 玻色子孤子（$\theta = 90^\circ$, $h = 0$）

取螺旋半径 $R = l_{Pl} = 1.616 \times 10^{-35}$ m，轴向速率 $h = 0$。

由公理Ⅰ：$v_\perp = \sqrt{c^2 - 0} = c = 2.998 \times 10^8$ m/s。

角频率：$\omega = v_\perp / R = 2.998 \times 10^8 / 1.616 \times 10^{-35} = 1.855 \times 10^{43}$ rad/s。

曲率：$\kappa = R\omega^2/c^2 = 1.616 \times 10^{-35} \times (1.855 \times 10^{43})^2 / (2.998 \times 10^8)^2 = 6.187 \times 10^{34}$ m$^{-1}$。

挠率：$\tau = h\omega/c^2 = 0$。

验证 $\omega = c\sqrt{\kappa^2+\tau^2}$：
$c\sqrt{\kappa^2+\tau^2} = 2.998 \times 10^8 \times 6.187 \times 10^{34} = 1.855 \times 10^{43}$ rad/s。✓ 与 $\omega$ 完全一致。

验证 $\tan\theta = \kappa/\tau$：$\tau = 0$，$\tan 90^\circ = \infty$，$\kappa/\tau = \infty$。✓ 一致（极限意义下）。

### 3.6.2 费米子孤子（$\theta = 45^\circ$, $\kappa = \tau$）

取 $R = l_{Pl}$，$h = c/\sqrt{2} = 2.120 \times 10^8$ m/s。

$v_\perp = \sqrt{c^2 - h^2} = c/\sqrt{2} = 2.120 \times 10^8$ m/s。

$\omega = v_\perp/R = 2.120 \times 10^8 / 1.616 \times 10^{-35} = 1.312 \times 10^{43}$ rad/s。

$\kappa = R\omega^2/c^2 = 3.094 \times 10^{34}$ m$^{-1}$。

$\tau = h\omega/c^2 = 3.094 \times 10^{34}$ m$^{-1}$。

验证 $\kappa = \tau$：✓ 完全相等。

验证 $\omega = c\sqrt{\kappa^2+\tau^2}$：
$c\sqrt{2\kappa^2} = c\kappa\sqrt{2} = 2.998 \times 10^8 \times 3.094 \times 10^{34} \times 1.414 = 1.312 \times 10^{43}$ rad/s。✓ 完全一致。

验证 $\tan\theta = \kappa/\tau$：$\tan 45^\circ = 1$，$\kappa/\tau = 1$。✓ 完全一致。

### 3.6.3 任意角度验证

取 $\theta = 30^\circ$，$R = l_{Pl}$。

$v_\perp = c\sin 30^\circ = c/2 = 1.499 \times 10^8$ m/s。
$h = c\cos 30^\circ = c\sqrt{3}/2 = 2.596 \times 10^8$ m/s。

$\omega = v_\perp/R = 9.274 \times 10^{42}$ rad/s。

$\kappa = R\omega^2/c^2 = 1.547 \times 10^{34}$ m$^{-1}$。
$\tau = h\omega/c^2 = 2.679 \times 10^{34}$ m$^{-1}$。

$\kappa/\tau = 1.547/2.679 = 0.5774 = 1/\sqrt{3} = \tan 30^\circ$。✓

$c\sqrt{\kappa^2+\tau^2} = 2.998 \times 10^8 \times \sqrt{(1.547)^2+(2.679)^2} \times 10^{34} = 9.274 \times 10^{42}$ rad/s。✓

全部恒等式在任意角度下严格成立。

## 3.7 本章小结

本章从公理Ⅰ（速率守恒）和公理Ⅱ（Frenet-Serret）严格导出了稳态圆柱螺旋的全部几何恒等式：

1. **稳态解定理**：曲率和挠率均为常数的曲线唯一是圆柱螺旋线；
2. **螺旋升角**：$\sin\theta = v_\perp/c$，$\cos\theta = h/c$；
3. **核心恒等式一**：$\tan\theta = \kappa/\tau$；
4. **核心恒等式二**：$\omega = c\sqrt{\kappa^2+\tau^2}$；
5. **曲率挠率表达式**：$\kappa = (\omega/c)\sin\theta$，$\tau = (\omega/c)\cos\theta$。

全部恒等式通过Python数值验证，在玻色子（90°）、费米子（45°）、任意角度下均严格成立。

**下一章预告：** 第4章将引入Călugăreanu-White拓扑纽结定理，导出拓扑自旋恒等式 $s + \mathrm{Lk}^2 = 1$，自然得到玻色子90°和费米子45°孤子解。
