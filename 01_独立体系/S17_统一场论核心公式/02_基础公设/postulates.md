# 基础公设

本体系以张祥前统一场论的「空间光速螺旋运动」为本源公设，由此导出 20 个核心公式及若干扩展公式。以下公设为来源文本主张的归属摘要；本仓库不沿用来源自封的「算法联盟 ROOT 最高权限 ✅ 全部通过」认证，按 H/O/C/U 诚实评级独立登记（见 `../README.md` 与 `../claims.csv`）。

## 公理 A1：空间光速螺旋运动公设（S17-A1）

> 宇宙中任一相对于观察者静止的物体，其周围空间以该物体为中心、以矢量光速 $\vec{C}$ 作圆柱状螺旋式发散运动。

- 螺旋由圆周运动与沿轴的直线运动合成；速度大小恒为光速 c。
- 数学形式：$\vec{r}(t)=r\cos\omega t\cdot\vec{i}+r\sin\omega t\cdot\vec{j}+ht\cdot\vec{k}$，且 $|\mathrm{d}\vec{r}/\mathrm{d}t|=c$。
- 来源：13_论文与成果/统一场论核心公式全面验证与理论分析_高标准论文.md §2.2、§3.2。

## 公理 A2：时空同一化（S17-A2）

> 空间位置矢量等于光速矢量乘以时间，即时间是空间光速运动的累积表现。

- 公式：$\vec{r}(t)=\vec{C}t=x\vec{i}+y\vec{j}+z\vec{k}$。
- 来源：同上 §3.1。

## 公理 A3：质量 / 电荷 / 能量几何起源（S17-A3）

> 质量、电荷、能量、引力场与电磁场，均为空间光速螺旋运动的几何后果，可由螺旋参数与光速 c 推导。

- 具体推导见 `../04_理论推导/核心公式集/` 各章节。
- 来源：同上 §3.3–§3.20。

## 20 个核心公式（源自论文 §3）

| 编号 | 名称 | 公式 |
|---|---|---|
| 3.1 | 时空同一化方程 | $\vec{r}(t)=\vec{C}t$ |
| 3.2 | 三维螺旋时空方程 | $\vec{r}(t)=r\cos\omega t\,\vec{i}+r\sin\omega t\,\vec{j}+ht\,\vec{k}$ |
| 3.3 | 质量定义方程 | $m=k\,\frac{dn}{d\Omega}$，$k=4\pi m_p$ |
| 3.4 | 引力场定义方程 | $\vec{A}=-Gk\frac{dn}{d\Omega}\frac{\vec{r}}{r^3}$ |
| 3.5 | 静止动量方程 | $\vec{p}_0=m_0\vec{C}_0$ |
| 3.6 | 运动动量方程 | $\vec{P}=m(\vec{C}-\vec{V})$ |
| 3.7 | 宇宙大统一方程（力方程） | $\vec{F}=\frac{d\vec{P}}{dt}=(\vec{C}-\vec{V})\frac{dm}{dt}-m\frac{d\vec{V}}{dt}$ |
| 3.8 | 空间波动方程 | $\nabla^2 L=\frac{1}{c^2}\frac{\partial^2 L}{\partial t^2}$ |
| 3.9 | 电荷定义方程 | $q=k'k\frac{1}{\Omega^2}\frac{d\Omega}{dt}$ |
| 3.10 | 电场定义方程 | $\vec{E}=-\frac{kk'}{4\pi\epsilon_0\Omega^2}\frac{d\Omega}{dt}\frac{\vec{r}}{r^3}$ |
| 3.11 | 磁场定义方程 | $\vec{B}=\frac{\mu_0\gamma kk'}{4\pi\Omega^2}\frac{d\Omega}{dt}\frac{[(x-vt)\vec{i}+y\vec{j}+z\vec{k}]}{[\gamma^2(x-vt)^2+y^2+z^2]^{3/2}}$ |
| 3.12 | 变化的引力场产生电磁场 | $\frac{\partial^2\vec{A}}{\partial t^2}=\frac{\vec{V}}{f}(\vec{\nabla}\cdot\vec{E})-\frac{C^2}{f}(\vec{\nabla}\times\vec{B})$ |
| 3.13 | 磁矢势方程 | $\vec{\nabla}\times\vec{A}=\frac{\vec{B}}{f}$ |
| 3.14 | 变化的引力场产生电场 | $\vec{E}=-f\frac{d\vec{A}}{dt}$ |
| 3.15 | 变化的磁场产生引力场和电场 | $\frac{d\vec{B}}{dt}=-\frac{\vec{A}\times\vec{E}}{c^2}-\frac{\vec{V}}{c^2}\times\frac{d\vec{E}}{dt}$ |
| 3.16 | 统一场论能量方程 | $e=m_0c^2=\frac{mc^2}{\sqrt{1-v^2/c^2}}$ |
| 3.17 | 光速飞行器动力学方程 | $\vec{F}=(\vec{C}-\vec{V})\frac{dm}{dt}-m\frac{d\vec{V}}{dt}$ |
| 3.18 | 核力场定义方程 | $\mathbf{D}=-Gm\frac{\mathbf{C}-3\frac{\mathbf{R}}{r}\dot{r}}{r^3}$ |
| 3.19 | 引力光速统一方程 | $Z=\frac{Gc}{2}$ |
| 3.20 | 电磁光速几何耦合常数 | $Z'=\frac{c}{8\pi\epsilon_0}$ |

## 扩展公式章节（超出原 20 个）

位于 `../04_理论推导/核心公式集/`：24-时空与物理常数归一化方程、常数 f 的量纲最终裁定、常数 k' 的量纲最终裁定、加速运动正电荷产生加速度反向相反的引力场方程、圆周运动正电荷产生的引力场方程。
