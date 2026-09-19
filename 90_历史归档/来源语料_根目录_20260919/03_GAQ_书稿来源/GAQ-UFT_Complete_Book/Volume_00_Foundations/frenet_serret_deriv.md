# 第0卷 基础数学与公理地基

# 第1章 空间曲线微分几何：Frenet–Serret 方程组

> 本章目标：为 GAQ‑UFT 建立唯一的微分几何语言。我们从弧长参数化出发，严格推导活动标架 $\{T,N,B\}$ 与曲率 $\kappa$、挠率 $\tau$，给出 Frenet–Serret 微分方程组，并完整求解常数 $\kappa,\tau$ 情形——圆柱螺旋。本章全部推导均可在 `Supplemental_Code/frenet_high_prec.py` 中以 200 位精度数值复现。

---

## 1.1 正则空间曲线与弧长参数化

设一条空间曲线由向量值函数给出

$$
\gamma : I \subset \mathbb{R} \longrightarrow \mathbb{R}^3,\qquad \gamma(t)=\bigl(x(t),y(t),z(t)\bigr).
$$

**定义 1.1.1（正则性）.** 若 $\gamma$ 连续可微且对任意 $t\in I$ 有 $\gamma'(t)\neq 0$，则称 $\gamma$ 为**正则曲线**。正则性保证切向量处处非零，从而可以定义单位切向。

**定义 1.1.2（弧长参数）.** 取定点 $t_0\in I$，定义弧长函数

$$
s(t)=\int_{t_0}^{t}\bigl\|\gamma'(u)\bigr\|\,du,
$$

其中 $\|\cdot\|$ 为欧氏范数。由此得到反函数 $t=t(s)$，把曲线改写为弧长参数形式 $\mathbf{r}(s)=\gamma(t(s))$。弧长参数的核心性质是

$$
\Bigl\|\frac{d\mathbf{r}}{ds}\Bigr\|=1,
$$

即弧长参数化下速度恒为单位长度。本章以下若无特别说明，曲线一律记作 $\mathbf{r}(s)$，并以 $s$ 为自变量。

---

## 1.2 活动标架 $\{T,N,B\}$ 的严格构造

**定义 1.2.1（单位切向量）。**

$$
\mathbf{T}(s)=\frac{d\mathbf{r}}{ds},\qquad \|\mathbf{T}\|=1.
$$

因为 $\mathbf{T}\cdot\mathbf{T}=1$ 恒成立，对 $s$ 求导得

$$
2\,\mathbf{T}\cdot\frac{d\mathbf{T}}{ds}=0\quad\Longrightarrow\quad \mathbf{T}\perp \frac{d\mathbf{T}}{ds}.
$$

**定义 1.2.2（曲率与单位法向量）。** 当 $\frac{d\mathbf{T}}{ds}\neq 0$ 时，定义

$$
\kappa(s)=\Bigl\|\frac{d\mathbf{T}}{ds}\Bigr\|>0,\qquad
\mathbf{N}(s)=\frac{1}{\kappa(s)}\frac{d\mathbf{T}}{ds},\qquad \|\mathbf{N}\|=1.
$$

$\kappa$ 度量切向旋转的速率（曲线偏离直线的程度），$\mathbf{N}$ 指向曲率中心。

**定义 1.2.3（副法向量）。**

$$
\mathbf{B}(s)=\mathbf{T}(s)\times\mathbf{N}(s).
$$

由 $\mathbf{T},\mathbf{N}$ 正交单位，$\mathbf{B}$ 自动单位且与二者构成右手正交标架：

$$
\mathbf{T}\times\mathbf{N}=\mathbf{B},\quad \mathbf{N}\times\mathbf{B}=\mathbf{T},\quad \mathbf{B}\times\mathbf{T}=\mathbf{N}.
$$

**引理 1.2.1（标架正交性）。** 对任意 $s$（在 $\kappa>0$ 处），$\{\mathbf{T},\mathbf{N},\mathbf{B}\}$ 是 $\mathbb{R}^3$ 的一组标准正交基。数值校验见代码：计算 $\mathbf{T}\cdot\mathbf{N},\mathbf{N}\cdot\mathbf{B},\mathbf{B}\cdot\mathbf{T}$ 应精确到 $10^{-190}$ 量级。

---

## 1.3 Frenet–Serret 微分方程组的完整求导

对 $\mathbf{B}=\mathbf{T}\times\mathbf{N}$ 求导，利用 $\mathbf{T}\perp\mathbf{N}$ 与前面定义：

$$
\frac{d\mathbf{B}}{ds}=\frac{d\mathbf{T}}{ds}\times\mathbf{N}+\mathbf{T}\times\frac{d\mathbf{N}}{ds}
=\kappa\mathbf{N}\times\mathbf{N}+\mathbf{T}\times\frac{d\mathbf{N}}{ds}
=\mathbf{T}\times\frac{d\mathbf{N}}{ds}.
$$

由于 $\{\mathbf{T},\mathbf{N},\mathbf{B}\}$ 张成全空间，$\frac{d\mathbf{N}}{ds}$ 可展开为

$$
\frac{d\mathbf{N}}{ds}=a\,\mathbf{T}+b\,\mathbf{N}+c\,\mathbf{B}.
$$

- 由 $\mathbf{N}\cdot\mathbf{N}=1$ 得 $2\mathbf{N}\cdot\frac{d\mathbf{N}}{ds}=0\Rightarrow b=0$。
- $\mathbf{N}\cdot\mathbf{T}=0$ 求导：$\frac{d\mathbf{N}}{ds}\cdot\mathbf{T}+\mathbf{N}\cdot\frac{d\mathbf{T}}{ds}=0\Rightarrow a+\kappa=0\Rightarrow a=-\kappa$。
- 代入 $\frac{d\mathbf{B}}{ds}$：注意 $\mathbf{T}\times\mathbf{N}=\mathbf{B}$，故 $\mathbf{T}\times\frac{d\mathbf{N}}{ds}=\mathbf{T}\times(c\mathbf{B})=c(\mathbf{T}\times\mathbf{B})=-c\mathbf{N}$。于是 $\frac{d\mathbf{B}}{ds}=-c\mathbf{N}$。

**定义 1.3.1（挠率）。** 令 $c=\tau$，即

$$
\frac{d\mathbf{B}}{ds}=-\tau\,\mathbf{N}.
$$

代回得 $\frac{d\mathbf{N}}{ds}=-\kappa\mathbf{T}+\tau\mathbf{B}$。

最终得到 **Frenet–Serret 方程组**：

$$
\boxed{
\begin{aligned}
\frac{d\mathbf{T}}{ds}&=\kappa\,\mathbf{N},\\[2mm]
\frac{d\mathbf{N}}{ds}&=-\kappa\,\mathbf{T}+\tau\,\mathbf{B},\\[2mm]
\frac{d\mathbf{B}}{ds}&=-\tau\,\mathbf{N}.
\end{aligned}}
$$

$\tau$ 度量标架绕切向扭转的速率（曲线偏离平面的程度）。当 $\tau\equiv0$ 曲线落在平面内；当 $\kappa\equiv0$ 曲线退化为直线。

---

## 1.4 常数曲率–常数挠率：圆柱螺旋解析解

设 $\kappa(s)\equiv\kappa_0>0,\ \tau(s)\equiv\tau_0$（常数）。记 $\Omega=\sqrt{\kappa_0^2+\tau_0^2}$。由 1.3 的线性系统对 $\mathbf{T}$ 求三阶导：

$$
\mathbf{T}''=\kappa_0\frac{d\mathbf{N}}{ds}=\kappa_0(-\kappa_0\mathbf{T}+\tau_0\mathbf{B}),
$$
$$
\mathbf{T}'''=-\kappa_0^2\mathbf{T}'+\kappa_0\tau_0\mathbf{B}'
=-\kappa_0^2(\kappa_0\mathbf{N})+\kappa_0\tau_0(-\tau_0\mathbf{N})
=-\kappa_0(\kappa_0^2+\tau_0^2)\mathbf{N}=-\kappa_0\Omega^2\mathbf{N}.
$$

故 $\mathbf{N}=-\mathbf{T}'''/(\kappa_0\Omega^2)$，代入 $\mathbf{T}''$ 得纯 $\mathbf{T}$ 的三阶常系数线性方程：

$$
\mathbf{T}'''-\Omega^2\mathbf{T}'=0.
$$

其特征根为 $0,\ \pm\Omega$，通解

$$
\mathbf{T}(s)=\mathbf{C}_0+\mathbf{C}_1\cos(\Omega s)+\mathbf{C}_2\sin(\Omega s),
$$

其中 $\mathbf{C}_i$ 为常向量，且由 $\|\mathbf{T}\|=1$ 与 $\mathbf{T}\cdot\mathbf{T}'=0$ 确定。积分 $\mathbf{r}(s)=\mathbf{r}_0+\int_0^s\mathbf{T}(u)\,du$ 得到圆柱螺旋的标准形式：

$$
\boxed{
\mathbf{r}(s)=\mathbf{r}_0+
\frac{1}{\Omega^2}
\begin{pmatrix}
\kappa_0\sin(\Omega s)\\
\kappa_0\bigl(1-\cos(\Omega s)\bigr)\\
\tau_0\,\Omega s
\end{pmatrix}
\quad(\text{经适当正交旋转与平移})
}
$$

等价地，以角度 $\theta$ 参数化：令 $\tan\theta=\tau_0/\kappa_0$，则螺旋半径 $R=\kappa_0/(\kappa_0^2+\tau_0^2)$，螺距因子 $c=\tau_0/(\kappa_0^2+\tau_0^2)$，经典写法

$$
\mathbf{r}(\varphi)=\bigl(R\cos\varphi,\ R\sin\varphi,\ c\,\varphi\bigr).
$$

**结论 1.4.1.** 在弧长参数下，常数曲率与常数挠率是**圆柱螺旋的充分必要条件**（除去整体刚体运动）——这正是 GAQ‑UFT 工作分支（分支3）的几何身份。

---

## 1.5 变曲率变挠率曲线的解空间

当 $\kappa(s),\tau(s)$ 为任意光滑正函数时，Frenet–Serret 方程组仍是线性 ODE 系统，由初值 $\{\mathbf{T},\mathbf{N},\mathbf{B}\}(0)$（标准正交）唯一确定一族曲线。由基本定理（do Carmo, 1976）：

**定理 1.5.1（曲线基本定理）。** 给定任意光滑函数 $\kappa(s)>0,\ \tau(s)$ 与一组标准正交初值标架，存在唯一（差一个欧氏运动）正则空间曲线以之为曲率与挠率。

因此“变 $\kappa,\tau$ 曲线”构成一个**无穷维函数空间** $(\kappa,\tau)\in C^\infty(\mathbb{R}_{>0})\times C^\infty(\mathbb{R})$。这是本章最关键的认知之一：**数学本身并不偏爱常数曲率挠率**——常数情形只是该无穷维空间中的一个单参数子族（由比值 $\tau/\kappa$ 决定）。把 $\kappa,\tau$ 强制为常数，是后续 A3 物理公设的任务，绝非数学必然。

---

## 1.6 mpmath 高精度数值微分与标架正交性校验

解析推导之外，我们以中心差分在 200 位精度下独立校验上述公式。`frenet_high_prec.py` 的核心：

- `diff_central` 用步长 $h=10^{-120}$ 的中心差分估计各阶导数；
- `frenet_decompose` 由 $(\mathbf{r}',\mathbf{r}'',\mathbf{r}''')$ 直接计算 $\kappa,\tau$ 与标架；
- 对参考圆柱螺旋 `helix_const` 应得到常数 $\kappa,\tau$；
- 对反例 `gamma_var`（半径随 $t$ 缓变）应得到随 $s$ 变化的 $\kappa,\tau$，演示分支2。

**校验清单：**
1. $\mathbf{T}\cdot\mathbf{N},\ \mathbf{N}\cdot\mathbf{B},\ \mathbf{B}\cdot\mathbf{T}<10^{-190}$；
2. 圆柱螺旋的 $\kappa,\tau$ 在采样点数值恒定；
3. 反例曲线 $\tau/\kappa$ 随采样点变化，证明非恒定。

> 这一“解析 + 数值双轨验证”方法论贯穿全书，是 GAQ‑UFT 可计算、可复现承诺的基石。

---

*（本章完。下一章进入广义 Kakeya 集，给出“覆盖所有方向”的拓扑约束。）*
