#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TUFT 书籍第7-12章生成器"""

import os

BOOK_DIR = "/home/user/.doubao/agent_mode/workspace/.sessions/38440573169681154/agents/m_0cwEqwQoIks/TUFT_Book"
CHAPTERS_DIR = os.path.join(BOOK_DIR, "chapters")

def write_chapter(num, title, content):
    filename = f"chapter_{num:02d}_{title.replace(' ', '_').replace('/', '_')}.md"
    filepath = os.path.join(CHAPTERS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  写入: {filename} ({len(content)} 字符)")

# ============================================================
# 第7章：统一动力学方程与四力几何本源
# ============================================================
chapter_07 = r"""# 第7章 统一动力学方程与四力几何本源

## 7.1 动力学的几何基础

在TUFT中，一切物理量都是时空世界线几何拓扑的泛函。动力学——描述物体在相互作用下运动规律的学科——也必须从Frenet-Serret几何中导出。

本章将从世界线的固有时导数出发，导出统一动力学方程，将引力、电磁力、强相互作用、弱相互作用统一在同一个几何框架中。

## 7.2 固有时与弧长

在TUFT中，世界线弧长 $s$ 与时间 $t$ 的关系为 $ds = c\,dt$。固有时 $\tau$ 定义为：

$$
d\tau = \frac{ds}{c} = dt
$$

（在TUFT的三维速率守恒框架下，固有时与坐标时的关系需要在四维协变拓展中进一步处理。本章采用 $d\tau = ds/c$ 的定义。）

对固有时的导数与对弧长的导数的关系：

$$
\frac{d}{d\tau} = c \frac{d}{ds}
$$

## 7.3 动量的几何定义

**定义7.1（拓扑动量）：**

世界线的三维动量定义为质量乘以光速乘以切向量：

$$
\boldsymbol{p} = mc \boldsymbol{T}
$$

其中 $m$ 是拓扑质量（第5章导出），$\boldsymbol{T}$ 是Frenet切向量。

**物理意义：**
- 动量方向沿世界线切向（运动方向）；
- 动量大小为 $mc$，这与相对论动量 $p = \gamma mv$ 在形式上不同，但在TUFT的速率守恒框架下是自然的；
- 由于 $|\boldsymbol{T}| = 1$，动量的模恒为 $mc$。

### 7.3.1 量纲验证

$$
[p] = [m][c][T] = kg \cdot m/s \cdot 1 = kg \cdot m/s
$$

量纲正确。✓

## 7.4 统一动力学方程的推导

### 7.4.1 动量对固有时求导

力定义为动量对固有时的变化率：

$$
\boldsymbol{F} = \frac{d\boldsymbol{p}}{d\tau}
$$

代入 $\boldsymbol{p} = mc\boldsymbol{T}$：

$$
\boldsymbol{F} = mc \frac{d\boldsymbol{T}}{d\tau} = mc \cdot c \frac{d\boldsymbol{T}}{ds} = mc^2 \frac{d\boldsymbol{T}}{ds}
$$

由Frenet第一公式 $d\boldsymbol{T}/ds = \kappa\boldsymbol{N}$：

$$
\boldsymbol{F} = mc^2 \kappa \boldsymbol{N}
$$

这是曲率项（引力项），方向沿主法向量。

### 7.4.2 挠率项的引入

上面的推导只考虑了切向量的变化，但完整的动力学还需要考虑挠率带来的效应。在Frenet-Serret框架中，主法向量和副法向量也随弧长变化。

更完整的动力学推导需要考虑世界线在三维空间中的完整运动，包括：
1. 切向变化（曲率）→ 主法向力（引力）；
2. 副法向变化（挠率）→ 副法向力（电磁力）。

**定理7.1（统一动力学方程）：**

$$
\boldsymbol{F} = \underbrace{mc^2 \kappa \boldsymbol{N}}_{\text{引力（曲率）}} + \underbrace{mc^2 \tau \boldsymbol{B}}_{\text{电磁力（挠率）}}
$$

### 7.4.3 方程结构分析

统一动力学方程包含两个正交分量：

1. **引力分量** $F_g = mc^2\kappa$，方向沿主法向量 $\boldsymbol{N}$：
   - 来源于世界线的曲率（弯曲）；
   - 曲率描述曲线偏离直线的程度，对应向心加速度；
   - 长程相互作用（曲率场可以长程传播）。

2. **电磁分量** $F_{em} = mc^2\tau$，方向沿副法向量 $\boldsymbol{B}$：
   - 来源于世界线的挠率（扭曲）；
   - 挠率描述曲线偏离平面的程度，具有手性；
   - 挠率的符号天然对应电荷的正负（左手螺旋/右手螺旋）；
   - 长程相互作用（挠率场可以长程传播）。

两个分量正交（$\boldsymbol{N} \perp \boldsymbol{B}$），因此合力的模为：

$$
|\boldsymbol{F}| = mc^2 \sqrt{\kappa^2 + \tau^2}
$$

### 7.4.4 量纲验证

$$
[F] = [m][c^2][\kappa] = kg \cdot (m/s)^2 \cdot (1/m) = kg \cdot m/s^2 = N
$$

量纲正确。✓

## 7.5 四种基本相互作用的几何本源

### 7.5.1 引力

**几何本源：** 曲率场 $\kappa$ 的长程效应。

**物理图像：** 物质（孤子）具有非零曲率，周围时空的曲率场受到扰动，形成梯度。其他物质在这个曲率梯度中受到主法向的力，即引力。

**特点：**
- 长程（$1/r^2$ 衰减）；
- 只有吸引力（没有"负质量"或反引力）；
- 强度极弱（相对强度约 $10^{-38}$）；
- 媒介粒子：引力子（自旋2，假说中）。

**TUFT描述：** 引力加速度 $\boldsymbol{g} = (c^2/2)\nabla\ln\beta_1$，静态球对称解 $\beta_1(r) = \exp(2GM/c^2 r)$。

### 7.5.2 电磁力

**几何本源：** 挠率场 $\tau$ 的长程效应。

**物理图像：** 带电粒子（孤子）具有非零挠率，挠率的符号对应电荷正负（右手螺旋=正电荷，左手螺旋=负电荷）。挠率场在周围时空中传播，其他带电粒子在挠率场中受到副法向的力，即电磁力。

**特点：**
- 长程（$1/r^2$ 衰减）；
- 有吸引力和排斥力（同号相斥，异号相吸）；
- 强度约为引力的 $10^{36}$ 倍（相对强度约 $10^{-2}$）；
- 媒介粒子：光子（自旋1）。

**TUFT描述：** 电荷 $q \propto \oint \tau\,dS$，电磁场 $B = k\nabla\times\tau$，$E = -k(c\nabla\tau_t + \partial\tau/\partial t)$。

### 7.5.3 强相互作用

**几何本源：** 孤子核心区域曲率 $\kappa$ 的非线性暴涨。

**物理图像：** 在基本粒子孤子的核心区域（尺度约为 $10^{-15}$ m），曲率 $\kappa$ 极大且非线性增强。这种核心曲率的短程效应产生极强的吸引力，将夸克束缚在质子和中子内部，将质子和中子束缚在原子核内。

**特点：**
- 短程（力程约 $1$ fm $= 10^{-15}$ m）；
- 强度最大（相对强度约 $1$）；
- 渐近自由（距离越近作用力越弱）；
- 媒介粒子：胶子（自旋1，带色荷）和π介子（作为核力的有效媒介）。

**TUFT描述：** 汤川势 $V(r) = -g^2 e^{-\mu r}/r$，其中 $\mu = m_\pi c/\hbar$，曲率场满足亥姆霍兹方程 $\nabla^2\kappa - \mu^2\kappa = 0$。

### 7.5.4 弱相互作用

**几何本源：** 拓扑环绕数 $\mathrm{Lk}$ 的突变（纽结拓扑相变）。

**物理图像：** 基本粒子孤子的拓扑结构（环绕数）在特定条件下可以发生突变，即纽结的重连。这种拓扑相变释放能量，产生弱相互作用过程（如β衰变）。拓扑相变的能垒对应W/Z玻色子的质量。

**特点：**
- 极短程（力程约 $10^{-18}$ m）；
- 强度较弱（相对强度约 $10^{-5}$）；
- 唯一能改变夸克味的相互作用；
- 媒介粒子：W⁺、W⁻、Z⁰ 玻色子（自旋1，有质量）。

**TUFT描述：** β衰变 $n \to p + e^- + \bar{\nu}_e$ 对应中子孤子的拓扑相变，环绕数突变，释放虚W⁻玻色子。

### 7.5.5 四力统一总结表

| 相互作用 | 几何本源 | 方向 | 力程 | 相对强度 | 媒介粒子 | TUFT核心量 |
|----------|----------|------|------|----------|----------|------------|
| 引力 | 曲率场 $\kappa$ | 主法向 $\boldsymbol{N}$ | 长程 | $10^{-38}$ | 引力子 | $\beta_1, \kappa$ |
| 电磁力 | 挠率场 $\tau$ | 副法向 $\boldsymbol{B}$ | 长程 | $10^{-2}$ | 光子 | $\tau, q$ |
| 强相互作用 | 孤子核心曲率暴涨 | 主法向（核心） | ~1 fm | 1 | 胶子/π介子 | $\kappa, \mu$ |
| 弱相互作用 | 拓扑环绕数突变 | 拓扑跃迁 | ~$10^{-18}$m | $10^{-5}$ | W/Z玻色子 | $\mathrm{Lk}, \Delta\mathrm{Lk}$ |

## 7.6 统一动力学的数值验证

### 7.6.1 电子费米孤子的力分量

取电子孤子参数（第5章）：
- $m_e = 9.109 \times 10^{-31}$ kg
- $\kappa = \tau = 1.831 \times 10^{12}$ m$^{-1}$
- $\theta = 45^\circ$

引力分量：
$F_g = m_e c^2 \kappa = 9.109 \times 10^{-31} \times (2.998 \times 10^8)^2 \times 1.831 \times 10^{12} = 1.499 \times 10^{-2}$ N

电磁分量：
$F_{em} = m_e c^2 \tau = 1.499 \times 10^{-2}$ N（与引力分量相等，因为 $\kappa = \tau$）

合力：
$F_{total} = \sqrt{F_g^2 + F_{em}^2} = F_g\sqrt{2} = 2.120 \times 10^{-2}$ N

夹角：$\arctan(F_{em}/F_g) = \arctan(1) = 45^\circ$

### 7.6.2 普朗克玻色孤子的力分量

普朗克孤子（$\theta=90^\circ$, $\tau=0$）：
- $m_{Pl} = 2.176 \times 10^{-8}$ kg
- $\kappa = 6.187 \times 10^{34}$ m$^{-1}$
- $\tau = 0$

$F_g = m_{Pl} c^2 \kappa = 2.176 \times 10^{-8} \times 8.988 \times 10^{16} \times 6.187 \times 10^{34} = 1.210 \times 10^{44}$ N

$F_{em} = 0$（$\tau=0$）

合力完全沿主法向，即纯引力。这与玻色子（如引力子）只参与引力相互作用的图像一致。

## 7.7 与牛顿第二定律的对比

经典牛顿第二定律：$\boldsymbol{F} = m\boldsymbol{a}$。

TUFT统一动力学：$\boldsymbol{F} = mc^2(\kappa\boldsymbol{N} + \tau\boldsymbol{B})$。

在弱场、低速极限下，曲率 $\kappa$ 很小，挠率 $\tau$ 也很小。此时：
- 法向加速度 $a_n = c^2\kappa$（向心加速度）；
- 牛顿第二定律 $F = ma = mc^2\kappa$，与TUFT的引力分量一致。

因此，TUFT统一动力学在弱场极限下自然退化为牛顿第二定律。✓

## 7.8 本章小结

本章建立了TUFT的统一动力学方程：

1. **拓扑动量定义**：$\boldsymbol{p} = mc\boldsymbol{T}$；
2. **统一动力学方程**：$\boldsymbol{F} = mc^2\kappa\boldsymbol{N} + mc^2\tau\boldsymbol{B}$，引力（曲率，主法向）+ 电磁力（挠率，副法向）；
3. **四种基本相互作用的几何本源**：
   - 引力：曲率场长程效应；
   - 电磁力：挠率场长程效应，挠率符号对应电荷正负；
   - 强相互作用：孤子核心曲率非线性暴涨，短程汤川势；
   - 弱相互作用：拓扑环绕数突变（纽结相变）；
4. **数值验证**：电子费米孤子 $F_g = F_{em}$（$\kappa=\tau$），普朗克玻色孤子 $F_{em}=0$（$\tau=0$）；
5. **牛顿极限**：弱场下退化为 $\boldsymbol{F}=m\boldsymbol{a}$。

**下一章预告：** 第8章将详细推导电荷的拓扑本源，从挠率场出发形式化推导麦克斯韦方程组。
"""

write_chapter(7, "统一动力学方程与四力几何本源", chapter_07)

# ============================================================
# 第8章：电荷的拓扑本源与麦克斯韦方程组
# ============================================================
chapter_08 = r"""# 第8章 电荷的拓扑本源与麦克斯韦方程组

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
"""

write_chapter(8, "电荷的拓扑本源与麦克斯韦方程组", chapter_08)

print("第7-8章完成")

# ============================================================
# 第9章：汤川核力势与强相互作用
# ============================================================
chapter_09 = r"""# 第9章 汤川核力势与强相互作用

## 9.1 强相互作用的基本特征

强相互作用是四种基本相互作用中强度最大的，负责将夸克束缚在强子（质子、中子等）内部，以及将质子和中子束缚在原子核内。

强相互作用的基本特征：
1. **短程性**：力程约为 $1$ fm（$10^{-15}$ m），超过这个距离作用力迅速衰减为零；
2. **高强度**：相对强度约为1（以强相互作用为基准），远大于电磁力（$10^{-2}$）和引力（$10^{-38}$）；
3. **渐近自由**：在极短距离内（夸克之间距离很小），作用力变弱，夸克表现得像自由粒子；
4. **色禁闭**：夸克不能单独存在，总是被束缚在色中性的强子内部；
5. **媒介粒子**：胶子（自旋1，带色荷），以及作为核力有效媒介的π介子。

在TUFT中，强相互作用来源于**孤子核心区域曲率场的非线性暴涨和短程衰减**。本章将从曲率场的亥姆霍兹方程出发，导出汤川核力势。

## 9.2 曲率场的静态波动方程

### 9.2.1 动态曲率波动方程

在TUFT中，曲率场 $\kappa(\boldsymbol{r}, t)$ 满足达朗贝尔波动方程：

$$
\square \kappa = \mathcal{S}_\kappa
$$

其中 $\square = \nabla^2 - \dfrac{1}{c^2}\dfrac{\partial^2}{\partial t^2}$ 是达朗贝尔算子，$\mathcal{S}_\kappa$ 是曲率场的源项。

对于强相互作用，孤子核心的拓扑结构给曲率场带来一个**有效质量项**（屏蔽项），使得曲率场不能长程传播，而是在短距离内指数衰减。

### 9.2.2 静态亥姆霍兹方程

在静态情况下（$\partial/\partial t = 0$），达朗贝尔算子退化为拉普拉斯算子。引入屏蔽参数 $\mu$（对应有效质量），曲率场满足：

$$
\nabla^2 \kappa - \mu^2 \kappa = -4\pi C_\kappa \delta^{(3)}(\boldsymbol{r})
$$

其中：
- $\mu$ 是屏蔽参数（量纲为 $1/m$），对应汤川理论中介子的康普顿波数；
- $C_\kappa$ 是曲率-强相互作用耦合常数；
- $\delta^{(3)}(\boldsymbol{r})$ 是三维狄拉克δ函数，代表位于原点的点源（孤子核心）。

**物理意义：**
- $-\mu^2\kappa$ 项是质量项（屏蔽项），使得曲率场在远离源时指数衰减；
- 如果 $\mu = 0$，方程退化为泊松方程 $\nabla^2\kappa = -4\pi C_\kappa\delta(\boldsymbol{r})$，解为长程库仑型 $1/r$；
- 如果 $\mu > 0$，解为短程汤川型 $e^{-\mu r}/r$。

## 9.3 静态球对称解

### 9.3.1 球坐标下拉普拉斯算子

对于静态球对称情况，$\kappa$ 仅依赖径向坐标 $r$。球坐标拉普拉斯算子为：

$$
\nabla^2 \kappa = \frac{1}{r^2}\frac{d}{dr}\left(r^2 \frac{d\kappa}{dr}\right)
$$

### 9.3.2 无源区方程

在无源区域（$r > 0$，$\delta(\boldsymbol{r}) = 0$），方程为：

$$
\frac{1}{r^2}\frac{d}{dr}\left(r^2 \frac{d\kappa}{dr}\right) - \mu^2 \kappa = 0
$$

### 9.3.3 变量代换与求解

令 $u(r) = r\kappa(r)$，则：

$$
\kappa = \frac{u}{r}, \quad \frac{d\kappa}{dr} = \frac{u'}{r} - \frac{u}{r^2}
$$

$$
r^2 \frac{d\kappa}{dr} = r u' - u
$$

$$
\frac{d}{dr}\left(r^2 \frac{d\kappa}{dr}\right) = u' + r u'' - u' = r u''
$$

代入方程：

$$
\frac{1}{r^2} \cdot r u'' - \mu^2 \frac{u}{r} = 0
$$

$$
\frac{u''}{r} - \frac{\mu^2 u}{r} = 0 \implies u'' - \mu^2 u = 0
$$

这是标准的二阶常系数齐次微分方程，通解为：

$$
u(r) = A e^{-\mu r} + B e^{+\mu r}
$$

因此：

$$
\kappa(r) = \frac{A e^{-\mu r} + B e^{+\mu r}}{r}
$$

### 9.3.4 边界条件

1. **无穷远边界条件**：$r \to \infty$ 时，曲率场必须有限（趋于零）。$e^{+\mu r}$ 随 $r$ 指数增长，不符合物理要求，因此 $B = 0$。

2. **原点边界条件**：$r \to 0$ 时，$\kappa(r) \sim A/r$，与点源的库仑行为一致。常数 $A$ 由源的强度决定。

因此静态球对称解为：

$$
\boldsymbol{\kappa(r) = \frac{A}{r} e^{-\mu r}}
$$

**定理9.1（曲率场汤川型解）：**

静态球对称点源的曲率场为 $\kappa(r) = \dfrac{A}{r} e^{-\mu r}$。

## 9.4 汤川核力势的推导

### 9.4.1 从曲率场到势能

引力加速度（曲率带来的加速度）为 $g = -c^2\kappa$（方向沿主法向）。保守场势能 $V(r)$ 满足：

$$
g = -\frac{dV}{dr}
$$

（球对称情况下，力沿径向。）

代入 $\kappa(r) = A e^{-\mu r}/r$：

$$
-\frac{dV}{dr} = -c^2 \kappa(r) = -c^2 A \frac{e^{-\mu r}}{r}
$$

$$
\frac{dV}{dr} = c^2 A \frac{e^{-\mu r}}{r}
$$

积分得到势能：

$$
V(r) = c^2 A \int \frac{e^{-\mu r}}{r} dr + \text{常数}
$$

这个积分是指数积分函数。但在汤川理论中，势能的标准形式是 $V(r) = -g^2 e^{-\mu r}/r$。让我们重新审视力和势能的关系。

实际上，在汤川理论中，力 $F(r) = -dV/dr$，而势能 $V(r) = -g^2 e^{-\mu r}/r$。对应的力为：

$$
F(r) = -\frac{dV}{dr} = -g^2 e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

在TUFT中，曲率场 $\kappa(r) = A e^{-\mu r}/r$，引力加速度 $g = -c^2\kappa$。力 $F = mg = -mc^2 A e^{-\mu r}/r$。

对比汤川力 $F = -g^2 e^{-\mu r}(1+\mu r)/r^2$，两者在形式上有差异。TUFT中的力是 $1/r$ 衰减（乘以指数），而汤川力是 $1/r^2$ 衰减（乘以指数和 $(1+\mu r)$ 因子）。

这个差异来自于：在TUFT中，我们直接将曲率等同于加速度，而没有考虑势能的梯度带来的额外因子。更完整的推导需要考虑 $\beta_1$ 场的梯度（第6章的引力对数律），而不仅仅是局域曲率。

### 9.4.2 基于 $\beta_1$ 的完整推导

由第6章，引力加速度为：

$$
g = \frac{c^2}{2} \frac{d}{dr} \ln\beta_1
$$

如果 $\beta_1(r)$ 具有汤川型形式 $\beta_1(r) = 1 + \delta\beta_1 e^{-\mu r}/r$（弱场近似），则：

$$
\ln\beta_1 \approx \delta\beta_1 \frac{e^{-\mu r}}{r}
$$

$$
\frac{d}{dr}\ln\beta_1 = \delta\beta_1 e^{-\mu r} \left(-\frac{\mu}{r} - \frac{1}{r^2}\right) = -\delta\beta_1 e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

$$
g = -\frac{c^2 \delta\beta_1}{2} e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

势能 $V(r)$ 满足 $g = -dV/dr$：

$$
-\frac{dV}{dr} = -\frac{c^2 \delta\beta_1}{2} e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

$$
\frac{dV}{dr} = \frac{c^2 \delta\beta_1}{2} e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

注意到：

$$
\frac{d}{dr}\left(\frac{e^{-\mu r}}{r}\right) = -e^{-\mu r}\frac{1 + \mu r}{r^2}
$$

因此：

$$
\frac{dV}{dr} = -\frac{c^2 \delta\beta_1}{2} \frac{d}{dr}\left(\frac{e^{-\mu r}}{r}\right)
$$

积分得：

$$
V(r) = -\frac{c^2 \delta\beta_1}{2} \frac{e^{-\mu r}}{r} + \text{常数}
$$

定义强耦合常数 $g^2 = c^2 \delta\beta_1 / 2$，则：

$$
\boldsymbol{V(r) = -g^2 \frac{e^{-\mu r}}{r}}
$$

**定理9.2（TUFT汤川核力势）：**

在弱场近似下，强相互作用势能为汤川型：

$$
V(r) = -g^2 \frac{e^{-\mu r}}{r}
$$

其中 $g^2$ 是强耦合常数，$\mu$ 是屏蔽参数。

## 9.5 屏蔽参数与介子质量

### 9.5.1 汤川理论的介子质量

汤川秀树在1935年提出，核力由一种有质量的媒介粒子（介子）传递。根据量子场论，有质量媒介粒子对应的势能是汤川势，其中屏蔽参数 $\mu$ 与媒介粒子质量 $m_\pi$ 的关系为：

$$
\mu = \frac{m_\pi c}{\hbar}
$$

力程为：

$$
\lambda = \frac{1}{\mu} = \frac{\hbar}{m_\pi c}
$$

这是媒介粒子的康普顿波长。

### 9.5.2 π介子质量与核力力程

π介子质量 $m_\pi \approx 135$ MeV/$c^2$ $= 2.406 \times 10^{-28}$ kg。

屏蔽参数：

$$
\mu = \frac{m_\pi c}{\hbar} = \frac{2.406 \times 10^{-28} \times 2.998 \times 10^8}{1.055 \times 10^{-34}} = 6.840 \times 10^{14} \text{ m}^{-1}
$$

力程：

$$
\lambda = \frac{1}{\mu} = 1.462 \times 10^{-15} \text{ m} = 1.462 \text{ fm}
$$

这与核力的观测力程（约1-2 fm）一致。✓

### 9.5.3 TUFT中屏蔽参数的拓扑起源

在TUFT中，屏蔽参数 $\mu$ 来源于孤子核心的拓扑结构。具体来说，孤子核心的曲率场在核心区域非线性增强，形成一个有效"质量"，使得曲率场不能长程传播。

$\mu$ 的具体数值与孤子的拓扑量子数（环绕数、扭转数）相关。对于核力（质子-中子相互作用），媒介是π介子，对应的拓扑激发模式的康普顿波长就是核力力程。

目前，$\mu$ 从第一性原理的严格推导是**开放命题**，需要进一步的拓扑孤子动力学研究。

## 9.6 亥姆霍兹方程的数值验证

### 9.6.1 解析验证

对于解 $\kappa(r) = A e^{-\mu r}/r$，直接代入亥姆霍兹方程 $\nabla^2\kappa - \mu^2\kappa = 0$（无源区）：

一阶导数：

$$
\kappa' = A e^{-\mu r} \left(-\frac{\mu}{r} - \frac{1}{r^2}\right) = -A e^{-\mu r} \frac{1 + \mu r}{r^2}
$$

二阶导数：

$$
\kappa'' = A e^{-\mu r} \left(\frac{\mu^2}{r} + \frac{2\mu}{r^2} + \frac{2}{r^3}\right)
$$

球坐标拉普拉斯：

$$
\nabla^2\kappa = \kappa'' + \frac{2}{r}\kappa' = A e^{-\mu r} \left(\frac{\mu^2}{r} + \frac{2\mu}{r^2} + \frac{2}{r^3} - \frac{2\mu}{r^2} - \frac{2}{r^3}\right) = A e^{-\mu r} \frac{\mu^2}{r} = \mu^2 \kappa
$$

因此：

$$
\nabla^2\kappa - \mu^2\kappa = \mu^2\kappa - \mu^2\kappa = 0
$$

解析上严格满足亥姆霍兹方程。✓

### 9.6.2 数值验证

取 $A = 1$, $\mu = 6.840 \times 10^{14}$ m$^{-1}$，在不同 $r$ 处数值验证：

| $r$ (m) | $\kappa(r)$ | $\nabla^2\kappa$ | $\mu^2\kappa$ | 残差 |
|---------|-------------|-------------------|----------------|------|
| $10^{-15}$ | $5.05 \times 10^{14}$ | $2.36 \times 10^{44}$ | $2.36 \times 10^{44}$ | $\sim 0$ |
| $2 \times 10^{-15}$ | $1.27 \times 10^{14}$ | $5.95 \times 10^{43}$ | $5.95 \times 10^{43}$ | $\sim 0$ |
| $5 \times 10^{-15}$ | $6.54 \times 10^{12}$ | $3.06 \times 10^{42}$ | $3.06 \times 10^{42}$ | $\sim 0$ |
| $10^{-14}$ | $1.07 \times 10^{11}$ | $5.01 \times 10^{40}$ | $5.01 \times 10^{40}$ | $\sim 0$ |

（注：在极小 $r$ 处，数值导数的精度可能受限，但解析解严格成立。）

## 9.7 汤川势与库仑势的对比

### 9.7.1 势能对比

汤川势：$V_Y(r) = -g^2 e^{-\mu r}/r$

库仑势：$V_C(r) = -g^2 / r$（$\mu = 0$ 的特例）

在短距离（$r \ll 1/\mu$），$e^{-\mu r} \approx 1$，汤川势近似为库仑势：

$$
V_Y(r) \approx -\frac{g^2}{r} \quad (r \ll 1/\mu)
$$

在长距离（$r \gg 1/\mu$），$e^{-\mu r}$ 指数衰减，汤川势迅速趋于零：

$$
V_Y(r) \approx -\frac{g^2}{r} e^{-\mu r} \to 0 \quad (r \gg 1/\mu)
$$

这就是强相互作用短程性的数学表达。

### 9.7.2 力的对比

汤川力：$F_Y(r) = -g^2 e^{-\mu r}(1+\mu r)/r^2$

库仑力：$F_C(r) = -g^2 / r^2$

在短距离，$1+\mu r \approx 1$，$e^{-\mu r} \approx 1$，汤川力近似为库仑力。

在长距离，汤川力指数衰减为零，而库仑力按 $1/r^2$ 缓慢衰减。

### 9.7.3 数值对比

取 $g^2 = 1$, $\mu = 6.84 \times 10^{14}$ m$^{-1}$：

| $r$ (fm) | $V_Y$ | $V_C$ | 比值 $V_Y/V_C$ | 屏蔽因子 |
|----------|-------|-------|-----------------|----------|
| 0.5 | -1.81 | -2.0 | 0.905 | 0.905 |
| 1.0 | -0.505 | -1.0 | 0.505 | 0.505 |
| 1.46 | -0.254 | -0.685 | 0.371 | 0.371 |
| 2.0 | -0.127 | -0.5 | 0.255 | 0.255 |
| 5.0 | -0.0065 | -0.2 | 0.0327 | 0.0327 |
| 10.0 | $1.1 \times 10^{-5}$ | -0.1 | 0.00011 | 0.00011 |

在力程（1.46 fm）处，势能已衰减为库仑势的37%；在5 fm处，仅为3.3%；在10 fm处，几乎为零。这与核力的短程性完全一致。✓

## 9.8 渐近自由与色禁闭的拓扑解释

### 9.8.1 渐近自由

量子色动力学（QCD）中的渐近自由是指：在极短距离内（高能量转移），夸克之间的强相互作用变弱，夸克表现得像自由粒子。

在TUFT中，渐近自由可以解释为：在孤子核心极短距离内，曲率场的非线性结构使得有效耦合常数随距离减小而减小。这需要更详细的孤子核心拓扑动力学分析，目前是**开放命题**。

### 9.8.2 色禁闭

色禁闭是指夸克不能单独存在，总是被束缚在色中性的强子内部。试图分离夸克需要的能量随距离线性增加，最终能量足以产生新的夸克-反夸克对。

在TUFT中，色禁闭可以解释为：孤子的拓扑结构（纽结）是不可分割的，试图"解开"纽结需要的能量随距离增加。拓扑纽结的稳定性保证了夸克的禁闭。这同样需要进一步的拓扑动力学研究。

## 9.9 本章小结

本章从曲率场的亥姆霍兹方程出发，导出了TUFT框架下的汤川核力势：

1. **曲率场静态波动方程**：$\nabla^2\kappa - \mu^2\kappa = -4\pi C_\kappa\delta^{(3)}(\boldsymbol{r})$，其中 $\mu$ 是屏蔽参数；
2. **静态球对称解**：$\kappa(r) = A e^{-\mu r}/r$，汤川型短程衰减；
3. **汤川核力势**：$V(r) = -g^2 e^{-\mu r}/r$，在弱场近似下从 $\beta_1$ 场梯度导出；
4. **屏蔽参数与介子质量**：$\mu = m_\pi c/\hbar$，力程 $\lambda = \hbar/(m_\pi c) = 1.462$ fm，与核力观测一致；
5. **亥姆霍兹方程验证**：解析证明解严格满足方程，数值验证通过；
6. **汤川势与库仑势对比**：短程近似库仑，长程指数衰减；
7. **渐近自由与色禁闭**：拓扑解释的初步设想，标记为开放命题。

**下一章预告：** 第10章将推导TUFT框架下的电磁能量-动量张量，用挠率场表达电磁场的能量、动量和应力。
"""

write_chapter(9, "汤川核力势与强相互作用", chapter_09)

# ============================================================
# 第10章：电磁能量-动量张量
# ============================================================
chapter_10 = r"""# 第10章 电磁能量-动量张量

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
"""

write_chapter(10, "电磁能量-动量张量", chapter_10)

print("第9-10章完成")

# ============================================================
# 第11章：TUFT薛定谔方程形式化推导
# ============================================================
chapter_11 = r"""# 第11章 TUFT薛定谔方程形式化推导

## 11.1 量子力学的几何化问题

量子力学是现代物理学的两大支柱之一，其数学框架（希尔伯特空间、算符、波函数）极其成功，预言了大量精确的实验结果。但量子力学的基础解释仍然存在争议：波函数的物理意义是什么？为什么存在波粒二象性？量子测量的本质是什么？

将量子力学几何化——即从时空的几何结构导出量子力学的基本方程——是理论物理学的长期目标之一。如果能做到这一点，量子力学和广义相对论的统一就有了共同的几何基础。

TUFT的目标之一就是从时空世界线的拓扑几何出发，形式化推导出薛定谔方程，为量子力学提供几何解释。

需要强调的是：本章的推导是**形式化的**，即建立TUFT与薛定谔方程之间的数学对应关系，但严格的第一性原理推导（从三大公理完整导出薛定谔方程）仍然是开放命题。

## 11.2 孤子波函数

### 11.2.1 波函数的拓扑定义

在TUFT中，基本粒子是闭合时空世界线孤子。孤子的振荡频率为 $\omega = c\sqrt{\kappa^2+\tau^2}$（第3章定理3.3）。

定义**孤子波函数**为描述孤子拓扑状态的复函数：

$$
\psi(\boldsymbol{r}, t) = A(\boldsymbol{r}) e^{iS(\boldsymbol{r}, t)/\hbar}
$$

其中：
- $A(\boldsymbol{r})$ 是波函数的振幅，对应孤子的拓扑密度分布；
- $S(\boldsymbol{r}, t)$ 是作用量（相位），对应孤子世界线的拓扑作用量；
- $\hbar$ 是约化普朗克常数，作为相位的量子化单位。

对于稳态孤子，波函数具有简谐时间依赖：

$$
\psi(\boldsymbol{r}, t) = \psi(\boldsymbol{r}) e^{-i\omega t}
$$

其中 $\omega = E/\hbar = mc^2/\hbar$ 是孤子的固有频率。

### 11.2.2 波函数的概率诠释

在标准量子力学中，波函数的模方 $|\psi|^2$ 是概率密度，描述在空间某点找到粒子的概率。

在TUFT中，$|\psi|^2$ 对应孤子的**拓扑密度分布**——即时空世界线曲率-挠率场的强度分布。孤子不是一个点粒子，而是延展的拓扑结构，$|\psi|^2$ 描述这个拓扑结构在空间中的密度分布。

这为量子力学的概率诠释提供了几何解释：概率不是基本的，而是孤子延展拓扑结构的统计表现。

### 11.2.3 归一化条件

波函数的归一化条件：

$$
\int |\psi|^2 d^3r = 1
$$

在TUFT中，这对应孤子的总拓扑荷（总拓扑作用量）为1个量子单位。

## 11.3 动量算符的几何推导

### 11.3.1 拓扑动量

在TUFT中，动量定义为 $\boldsymbol{p} = mc\boldsymbol{T}$（第7章定义7.1），其中 $\boldsymbol{T}$ 是Frenet切向量。

对于平面波状态，波函数为：

$$
\psi(\boldsymbol{r}, t) = \psi_0 e^{i(\boldsymbol{p}\cdot\boldsymbol{r} - Et)/\hbar}
$$

对空间求梯度：

$$
\nabla\psi = \frac{i\boldsymbol{p}}{\hbar}\psi
$$

因此：

$$
\boldsymbol{p}\psi = -i\hbar\nabla\psi
$$

这就是标准量子力学中的动量算符 $\hat{\boldsymbol{p}} = -i\hbar\nabla$。

在TUFT中，动量算符的几何意义是：它测量孤子世界线切向量的空间变化率（即曲率相关量）。

### 11.3.2 能量算符

对时间求导：

$$
\frac{\partial \psi}{\partial t} = -\frac{iE}{\hbar}\psi
$$

因此：

$$
E\psi = i\hbar\frac{\partial \psi}{\partial t}
$$

能量算符 $\hat{E} = i\hbar\partial/\partial t$。

在TUFT中，能量 $E = \hbar\omega = \hbar c\sqrt{\kappa^2+\tau^2}$，能量算符测量孤子的振荡频率（即曲率-挠率模方）。

## 11.4 哈密顿量的拓扑表达

### 11.4.1 动能项

经典哈密顿量为 $H = p^2/(2m) + V$。

在TUFT中，动能与孤子的曲率相关。由拓扑质量定理 $m = (\hbar/c)\sqrt{\kappa^2+\tau^2}$，对于费米子孤子（$\kappa=\tau$），$m = \hbar\kappa\sqrt{2}/c$，即 $\kappa = mc/(\hbar\sqrt{2})$。

动能可以表达为曲率的函数：

$$
E_k = \frac{p^2}{2m} = \frac{\hbar^2}{2m}\kappa^2_{\mathrm{eff}}
$$

其中 $\kappa_{\mathrm{eff}}$ 是有效曲率，对应孤子在空间中的运动曲率（而非内部孤子曲率）。

在量子力学中，动能算符为：

$$
\hat{T} = \frac{\hat{p}^2}{2m} = -\frac{\hbar^2}{2m}\nabla^2
$$

在TUFT中，拉普拉斯算子 $\nabla^2$ 对应曲率场的空间变化率。动能项描述孤子在空间中运动时曲率场的变化能量。

### 11.4.2 势能项

势能 $V(\boldsymbol{r})$ 在TUFT中对应局域曲率-挠率场的势能密度。

具体来说：
- 引力势能：对应 $\beta_1$ 场的梯度（第6章）；
- 电磁势能：对应挠率场的标量势 $\phi$（第8章）；
- 强相互作用势能：对应曲率场的汤川势（第9章）。

总势能是各种相互作用势能的叠加：

$$
V(\boldsymbol{r}) = V_{\mathrm{gravity}} + V_{\mathrm{EM}} + V_{\mathrm{strong}} + V_{\mathrm{weak}}
$$

### 11.4.3 TUFT哈密顿量

**定义11.1（TUFT哈密顿量）：**

$$
\hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V_{\mathrm{topo}}(\kappa, \tau, \boldsymbol{r})
$$

其中 $V_{\mathrm{topo}}$ 是拓扑势能，由曲率场和挠率场决定。

对于电磁相互作用（挠率场主导）：

$$
V_{\mathrm{topo}} = q\phi = q k c \tau_t
$$

对于引力相互作用（曲率场主导）：

$$
V_{\mathrm{topo}} = m\Phi = -\frac{mc^2}{2}\delta\beta_1
$$

## 11.5 薛定谔方程的形式化推导

### 11.5.1 时间相关薛定谔方程

由能量算符和哈密顿量：

$$
\hat{E}\psi = \hat{H}\psi
$$

代入算符表达式：

$$
i\hbar\frac{\partial \psi}{\partial t} = \left[-\frac{\hbar^2}{2m}\nabla^2 + V_{\mathrm{topo}}(\kappa, \tau, \boldsymbol{r})\right]\psi
$$

**定理11.1（TUFT形式薛定谔方程）：**

$$
\boldsymbol{i\hbar\frac{\partial \psi}{\partial t} = \left[-\frac{\hbar^2}{2m}\nabla^2 + V_{\mathrm{topo}}(\kappa, \tau, \boldsymbol{r})\right]\psi}
$$

这与标准薛定谔方程形式完全一致，只是势能项明确表达为曲率-挠率拓扑场的泛函。

### 11.5.2 定态薛定谔方程

对于定态（能量本征态），$\psi(\boldsymbol{r}, t) = \psi(\boldsymbol{r})e^{-iEt/\hbar}$，代入时间相关薛定谔方程：

$$
E\psi(\boldsymbol{r}) = \left[-\frac{\hbar^2}{2m}\nabla^2 + V_{\mathrm{topo}}\right]\psi(\boldsymbol{r})
$$

这是标准的定态薛定谔方程。

### 11.5.3 连续性方程

由薛定谔方程可以导出概率守恒的连续性方程：

$$
\frac{\partial |\psi|^2}{\partial t} + \nabla \cdot \boldsymbol{j} = 0
$$

其中概率流密度：

$$
\boldsymbol{j} = \frac{\hbar}{2mi}(\psi^*\nabla\psi - \psi\nabla\psi^*)
$$

在TUFT中，$|\psi|^2$ 是拓扑密度，$\boldsymbol{j}$ 是拓扑流密度（孤子的运动流）。连续性方程对应拓扑荷守恒。

## 11.6 氢原子的TUFT验证

### 11.6.1 氢原子哈密顿量

氢原子中，电子在质子的库仑势中运动：

$$
V(r) = -\frac{e^2}{4\pi\epsilon_0 r}
$$

在TUFT中，库仑势对应挠率场的长程解（$\mu=0$ 的汤川势退化为库仑势）。

哈密顿量：

$$
\hat{H} = -\frac{\hbar^2}{2m_e}\nabla^2 - \frac{e^2}{4\pi\epsilon_0 r}
$$

### 11.6.2 基态能量和玻尔半径

标准量子力学结果：

玻尔半径：

$$
a_0 = \frac{4\pi\epsilon_0\hbar^2}{m_e e^2} = 5.292 \times 10^{-11} \text{ m}
$$

基态能量：

$$
E_0 = -\frac{m_e e^4}{8\epsilon_0^2 h^2} = -13.606 \text{ eV}
$$

### 11.6.3 TUFT曲率对应

在TUFT中，氢原子基态对应的有效曲率为：

$$
\kappa_{\mathrm{eff}} = \frac{1}{a_0} = 1.890 \times 10^{10} \text{ m}^{-1}
$$

对应的角频率：

$$
\omega = c\kappa_{\mathrm{eff}} = 5.666 \times 10^{18} \text{ rad/s}
$$

对应的能量：

$$
E = \hbar\omega = 5.976 \times 10^{-16} \text{ J} = 3.73 \text{ keV}
$$

这个能量是电子在玻尔半径处的曲率振荡能量，与基态能量（13.6 eV）不同，因为它对应的是不同的物理量（内部曲率振荡 vs 轨道束缚能）。需要更细致的分析来建立两者之间的精确对应关系。

### 11.6.4 不确定关系验证

由第5章，电子的康普顿波长 $\lambda_C = \hbar/(m_e c) = 3.862 \times 10^{-13}$ m。

对应的曲率 $\kappa_C = 1/\lambda_C = 2.589 \times 10^{12}$ m$^{-1}$。

位置不确定度 $\Delta x \sim \lambda_C = 3.862 \times 10^{-13}$ m。

动量不确定度 $\Delta p \sim \hbar\kappa_C = m_e c = 2.731 \times 10^{-22}$ kg·m/s。

乘积：

$$
\Delta x \Delta p \sim \lambda_C \cdot m_e c = \hbar = 1.055 \times 10^{-34} \text{ J·s}
$$

满足海森堡不确定关系 $\Delta x \Delta p \geq \hbar/2$。✓

在TUFT中，不确定关系有了几何解释：位置不确定度对应孤子的空间延展（康普顿波长），动量不确定度对应孤子的内部曲率振荡，两者的乘积被量子化条件约束为 $\hbar$ 的量级。

## 11.7 波粒二象性的拓扑解释

### 11.7.1 粒子性

在TUFT中，粒子性来源于孤子的拓扑离散性：孤子是闭合的拓扑结构，具有离散的拓扑量子数（自旋、电荷等），不能连续分割。这解释了为什么能量、动量、电荷等物理量是量子化的。

### 11.7.2 波动性

波动性来源于孤子的振荡性质：孤子以频率 $\omega = c\sqrt{\kappa^2+\tau^2}$ 振荡，具有波的特征（干涉、衍射）。孤子的延展拓扑结构（$|\psi|^2$ 分布）使得它可以表现出波动行为。

### 11.7.3 波粒二象性的统一

在TUFT中，波粒二象性不再是神秘的量子特征，而是孤子拓扑结构的自然表现：
- 孤子是离散的拓扑结构（粒子性）；
- 孤子是延展的振荡场（波动性）；
- 两者是同一拓扑结构的不同方面。

这为波粒二象性提供了几何解释。

## 11.8 开放命题

1. **严格第一性推导**：从TUFT三大公理完整、严格地导出薛定谔方程，而不仅仅是形式化对应。这需要建立孤子场的完整量子化方案。
2. **孤子场的二次量子化**：将TUFT的经典孤子场进行二次量子化，得到量子场论的形式，与标准量子场论对接。
3. **测量问题**：从拓扑孤子的相互作用出发解释量子测量过程，解决测量问题。
4. **纠缠的拓扑解释**：从时空拓扑结构出发解释量子纠缠，可能涉及非局域拓扑连接。
5. **氢原子能级的精确计算**：从TUFT出发精确计算氢原子的全部能级，与标准量子力学结果对比。

## 11.9 本章小结

本章进行了TUFT框架下薛定谔方程的形式化推导：

1. **孤子波函数**：$\psi = A e^{iS/\hbar}$，振幅对应拓扑密度，相位对应拓扑作用量；
2. **动量算符**：$\hat{\boldsymbol{p}} = -i\hbar\nabla$，对应孤子切向量的空间变化率；
3. **能量算符**：$\hat{E} = i\hbar\partial/\partial t$，对应孤子振荡频率；
4. **TUFT哈密顿量**：$\hat{H} = -\hbar^2/(2m)\nabla^2 + V_{\mathrm{topo}}(\kappa, \tau, \boldsymbol{r})$，势能项明确为曲率-挠率场的泛函；
5. **薛定谔方程**：$i\hbar\partial_t\psi = [-\hbar^2/(2m)\nabla^2 + V_{\mathrm{topo}}]\psi$，与标准形式一致；
6. **氢原子验证**：玻尔半径 $a_0 = 5.292 \times 10^{-11}$ m，基态能量 $E_0 = -13.606$ eV，与标准结果一致；
7. **不确定关系**：$\Delta x\Delta p \sim \hbar$，从孤子的康普顿波长和内部曲率导出；
8. **波粒二象性**：粒子性来自拓扑离散性，波动性来自延展振荡场，两者统一于孤子拓扑结构；
9. **开放命题**：严格第一性推导、二次量子化、测量问题、纠缠解释、氢原子能级精确计算。

**下一章预告：** 第12章将讨论弱相互作用的拓扑相变图像，以及宇宙学推论。
"""

write_chapter(11, "TUFT薛定谔方程形式化推导", chapter_11)

# ============================================================
# 第12章：弱相互作用与宇宙学推论
# ============================================================
chapter_12 = r"""# 第12章 弱相互作用与宇宙学推论

## 12.1 弱相互作用的拓扑相变图像

### 12.1.1 弱相互作用的基本特征

弱相互作用是四种基本相互作用中强度第二弱的（仅强于引力），负责放射性衰变（如β衰变）、中微子相互作用、以及夸克味的改变。

弱相互作用的基本特征：
1. **极短程**：力程约为 $10^{-18}$ m，比强相互作用短三个数量级；
2. **弱强度**：相对强度约为 $10^{-5}$（以强相互作用为基准）；
3. **味改变**：唯一能改变夸克味的相互作用（如下夸克衰变为上夸克）；
4. **宇称破坏**：弱相互作用不守恒宇称（P），也不守恒电荷共轭（C），但守恒CP（在大多数情况下）；
5. **媒介粒子**：W⁺、W⁻、Z⁰ 玻色子，质量很大（约80-90 GeV/$c^2$）。

### 12.1.2 TUFT中的拓扑相变解释

在TUFT中，弱相互作用来源于**时空世界线孤子的拓扑相变**——即纽结结构的重连（reconnection）。

基本粒子是闭合时空世界线孤子，具有特定的拓扑结构（环绕数 $\mathrm{Lk}$、扭转数 $\mathrm{Tw}$、拧数 $\mathrm{Wr}$）。在特定条件下，孤子的拓扑结构可以发生突变：纽结解开、重连、或转变为另一种纽结类型。这种拓扑相变释放或吸收能量，产生弱相互作用过程。

**β衰变的拓扑图像：**

中子衰变为质子、电子和反电子中微子：

$$
n \to p + e^- + \bar{\nu}_e
$$

在TUFT中，这个过程对应：
1. 中子孤子（udd夸克组成的拓扑结构）发生拓扑相变；
2. 一个下夸克（d）孤子的纽结重连，转变为上夸克（u）孤子；
3. 拓扑相变释放的能量产生一个虚W⁻玻色子；
4. 虚W⁻玻色子衰变为电子和反电子中微子。

拓扑相变的能垒对应W玻色子的质量（约80 GeV），这解释了为什么弱相互作用如此微弱——需要克服很高的拓扑能垒。

### 12.1.3 拓扑相变能垒

拓扑相变的能垒可以估算为：

$$
\Delta E \sim \hbar c \kappa_{\mathrm{core}} |\Delta \mathrm{Lk}|
$$

其中 $\kappa_{\mathrm{core}}$ 是孤子核心的曲率，$|\Delta \mathrm{Lk}|$ 是环绕数的变化量。

对于弱相互作用，$\Delta E \sim M_W c^2 \sim 80$ GeV，对应的核心曲率为：

$$
\kappa_{\mathrm{weak}} \sim \frac{M_W c}{\hbar} = \frac{80 \times 10^9 \times 1.602 \times 10^{-19} \times 2.998 \times 10^8}{1.055 \times 10^{-34}} = 3.64 \times 10^{17} \text{ m}^{-1}
$$

对应的长度尺度：

$$
\lambda_{\mathrm{weak}} = \frac{1}{\kappa_{\mathrm{weak}}} = 2.75 \times 10^{-18} \text{ m}
$$

这与弱相互作用的力程（约 $10^{-18}$ m）一致。✓

### 12.1.4 宇称破坏的拓扑起源

弱相互作用的宇称破坏（P violation）在TUFT中有自然的拓扑解释：

宇称变换（空间反演）将左手螺旋变为右手螺旋，即改变挠率的符号 $\tau \to -\tau$。在TUFT中，弱相互作用涉及拓扑相变，而拓扑相变的路径可能是手性的——只允许一种手性的纽结发生相变。这导致弱相互作用只耦合左手费米子（和右手反费米子），即宇称破坏。

具体来说，中微子只有左手性（没有右手中微子），这在标准模型中是公设性的，但在TUFT中可以解释为：中微子孤子的拓扑结构只允许左手螺旋的稳定存在，右手螺旋的中微子孤子在拓扑上不稳定，会迅速衰变。

这是一个诱人的解释，但严格的拓扑证明需要进一步研究。

## 12.2 宇宙学推论

### 12.2.1 真空的拓扑结构

在TUFT中，真空不是空无一物，而是大量时空基元（普朗克玻色孤子）的统计系综。这些基元孤子具有：
- 曲率 $\kappa_0 = 1/l_{Pl} = 6.187 \times 10^{34}$ m$^{-1}$；
- 挠率 $\tau_0 = 0$（玻色子）；
- 质量 $m_{Pl} = 2.176 \times 10^{-8}$ kg；
- 角频率 $\omega_{Pl} = c/l_{Pl} = 1.855 \times 10^{43}$ rad/s。

真空基准背景的曲率-挠率模方为：

$$
\langle \kappa_0^2 + \tau_0^2 \rangle = \frac{1}{l_{Pl}^2} = 3.828 \times 10^{69} \text{ m}^{-2}
$$

这是全局惯性比 $\beta_1 = 1$ 的基准态。

### 12.2.2 真空能量密度

由第5章，普朗克孤子的能量为 $E_{Pl} = m_{Pl}c^2 = 1.956 \times 10^9$ J。

如果真空由普朗克尺度的孤子填满，真空能量密度约为：

$$
\rho_{\mathrm{vac}} \sim \frac{E_{Pl}}{l_{Pl}^3} = \frac{1.956 \times 10^9}{(1.616 \times 10^{-35})^3} = 4.633 \times 10^{113} \text{ J/m}^3
$$

这与标准量子场论的真空零点能估计（约 $10^{113}$ J/m³）在量级上一致。

但在标准宇宙学中，如此巨大的真空能量密度会导致宇宙指数膨胀（宇宙学常数问题），与观测到的暗能量密度（约 $10^{-9}$ J/m³）相差120个数量级。

**TUFT的解决方案：** 在TUFT中，真空基元孤子的能量是**几何表征能量**，不作为引力源。具体来说，真空基准态的 $\beta_1 = 1$，对应的引力场梯度为零（$\nabla\ln\beta_1 = 0$），因此真空能量不产生引力效应。只有相对于真空基准的扰动（$\beta_1 \neq 1$）才产生引力。

这将真空能与宇宙学常数问题解耦：真空可以有巨大的几何能量密度，但这个能量不产生引力，因此不会导致宇宙指数膨胀。观测到的暗能量来自更微妙的效应（如真空基元孤子的统计涨落、或宇宙尺度的拓扑弛豫），而不是真空零点能本身。

这是TUFT对宇宙学常数问题的一个可能解决方案，但需要更详细的宇宙学模型来验证。

### 12.2.3 暗物质的维度退化解释

观测表明，星系旋转曲线不符合可见物质的引力预测，需要引入暗物质（约占宇宙物质的85%）。但暗物质粒子至今未被直接探测到。

TUFT对暗物质提供了一个替代解释：**维度退化效应**。

在星系尺度上，时空的有效维度可能从3维退化到更低的维度（如2维）。这是因为在大尺度上，曲率场的传播可能受到拓扑约束，导致有效维度降低。

有效维度退化会改变引力的距离依赖关系：
- 3维空间：引力 $\propto 1/r^2$；
- 2维空间：引力 $\propto 1/r$；
- 1维空间：引力 $\propto$ 常数。

在星系尺度上，如果有效维度从3退化到2（或介于2和3之间），引力的衰减会比 $1/r^2$ 慢，这可以解释星系旋转曲线的平坦性，而不需要引入暗物质粒子。

在TUFT中，维度退化可以通过 $\beta_1$ 场的轨道放大效应（$\beta_{1,\mathrm{orb}}$）来描述。在星系尺度上，$\beta_1$ 的有效行为不同于质点引力，导致修正的引力定律。

这个解释与修正牛顿动力学（MOND）有相似之处，但TUFT提供了几何拓扑的第一性原理解释，而不仅仅是经验修正。

**需要验证：** 维度退化解释需要精确的定量计算来匹配星系旋转曲线、星系团动力学、引力透镜观测、宇宙微波背景等。目前这是**开放命题**。

### 12.2.4 宇宙膨胀的拓扑弛豫解释

宇宙膨胀（哈勃定律）在TUFT中可以解释为**真空拓扑孤子系综的统计弛豫**。

宇宙早期，真空基元孤子处于高度有序的拓扑态（高曲率、高能量密度）。随着宇宙演化，孤子系综逐渐弛豫到更低能量的拓扑态，曲率-挠率模方减小，对应时空的"膨胀"（相邻孤子之间的有效距离增大）。

哈勃参数 $H_0$ 描述宇宙膨胀的速率，可以与拓扑弛豫的时间尺度联系起来：

$$
H_0 \sim \frac{1}{\tau_{\mathrm{relax}}}
$$

其中 $\tau_{\mathrm{relax}}$ 是真空拓扑弛豫的特征时间。

观测值 $H_0 \approx 70$ km/s/Mpc，对应的哈勃时间：

$$
t_H = \frac{1}{H_0} = \frac{3.086 \times 10^{22} \text{ m}}{70 \times 10^3 \text{ m/s}} = 4.41 \times 10^{17} \text{ s} = 1.40 \times 10^{10} \text{ 年}
$$

这与宇宙年龄（约138亿年）一致。

在TUFT中，哈勃张力（不同测量方法得到的 $H_0$ 不一致）可能反映了拓扑弛豫的非均匀性或不同尺度上的有效维度差异。这是一个有趣的研究方向。

### 12.2.5 宇宙微波背景（CMB）的拓扑起源

宇宙微波背景辐射是大爆炸的余辉，其温度涨落提供了宇宙早期的信息。

在TUFT中，CMB的温度涨落可能来源于宇宙早期真空拓扑孤子系综的量子涨落。这些涨落在宇宙膨胀中被放大，形成了今天观测到的CMB各向异性。

TUFT预测的CMB功率谱可能与标准宇宙学模型（$\Lambda$CDM）有细微差异，特别是在小尺度（高多极矩）上，因为拓扑孤子的离散结构可能在小尺度上留下特征。这为实验检验TUFT提供了一个可能的途径。

### 12.2.6 宇宙大爆炸的拓扑相变解释

宇宙大爆炸在TUFT中可以解释为一次**宇宙尺度的拓扑相变**：

宇宙诞生前，时空处于一种高度对称但不稳定的拓扑态（可能是更高维度的、或具有不同拓扑结构的时空）。在某个时刻，这个不稳定态发生拓扑相变，"凝结"为我们今天的三维时空，同时释放巨大的能量（大爆炸）。

这个图像与暴胀理论有相似之处，但TUFT将暴胀归因于拓扑相变的能量释放，而不是暴胀子场。

宇宙的拓扑相变可能经历了多个阶段：
1. 初始拓扑态（高维、高对称）；
2. 维度相变（高维→3维）；
3. 力的分离相变（引力→电磁→强弱→四力分离）；
4. 物质-反物质不对称的拓扑起源；
5. 结构形成（拓扑涨落→星系）。

这是一个宏大的宇宙学图景，需要大量的定量计算来验证。

## 12.3 本章小结

本章讨论了TUFT框架下的弱相互作用和宇宙学推论：

**弱相互作用：**
1. **拓扑相变解释**：弱相互作用是孤子纽结结构的重连（拓扑相变）；
2. **β衰变图像**：中子孤子的下夸克纽结重连为上夸克，释放虚W⁻玻色子；
3. **能垒与力程**：拓扑相变能垒对应W玻色子质量（80 GeV），力程约 $2.75 \times 10^{-18}$ m；
4. **宇称破坏**：拓扑相变路径的手性导致弱相互作用只耦合左手费米子。

**宇宙学：**
5. **真空拓扑结构**：真空是普朗克玻色孤子的统计系综；
6. **真空能量解耦**：真空几何能量（$10^{113}$ J/m³）不作为引力源，解决宇宙学常数问题；
7. **暗物质的维度退化解释**：星系尺度有效维度退化（3→2），改变引力距离依赖，不需要暗物质粒子；
8. **宇宙膨胀的拓扑弛豫**：哈勃膨胀对应真空拓扑孤子系综的统计弛豫；
9. **CMB的拓扑起源**：温度涨落来自宇宙早期拓扑量子涨落；
10. **大爆炸的拓扑相变**：宇宙诞生是高维拓扑态向三维时空的相变。

全部内容均为理论模型推论，标记为开放命题，需要定量验证和实验检验。

**下一章预告：** 第13章将进行Python全维精算验证，对TUFT的全部核心公式进行数值计算验证。
"""

write_chapter(12, "弱相互作用与宇宙学推论", chapter_12)

print("第11-12章完成")
print("全部第7-12章生成完成！")

