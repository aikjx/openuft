# §13 动量密度推导 + Darboux–动量映射 + 模型对比与实验判据

> 算法联盟最高权限 · S02 空间光速螺旋统一力
> 延续「光速螺旋**场标架**」公理体系（注意：此处是**场正交标架**模型，与 §一–§七 的质点空间轨迹螺旋模型是两个并行的几何描述分支；本 §13 全部结论属于场标架分支，不继承 S02-A4 关于轴向速度 $u<c$ 的互斥定理，因为本分支不假设质点沿真实空间曲线运动）。
>
> **边界红线（本 §13）**：以下为场标架微分几何 + 经典电磁动量密度（Minkowski 形式）的体系内自洽推导。所有「预言」在实验判决前仅是模型独有几何结构，不替代 QED；本模型把标准圆偏振平面波作为 $\tau=0$ 子空间特例包含在内。

> ## ⚠️ 勘误（2026-09-24，依据 §15 审计）
>
> 本节存在**两处结构性缺陷**，已在 §15 坐实，阅读本节前必读：
>
> 1. **Part B 的显式标架不满足其自身声明的 Frenet 方程**（$\theta\neq0$ 时残差达 $O(1)$，$\theta=89^\circ$ 时 $1.414$；且 $\boldsymbol\omega_D$ 随 $s$ 变化，违反「常 $\kappa,\tau$ 下 Darboux 矢量必恒定」）。仅在 $\theta=0$ 成立。**已修正**，见 Part B 修正版公式；`momentum_darboux.py` 已同步更新。
> 2. **本节的场拟设不是真空 Maxwell 解**（更严重）：$\theta\neq0$ 时存在纵向分量（$\theta=45^\circ$ 时 $\lvert E_z\rvert/\lvert E\rvert=50\%$），$\nabla\!\cdot\!\boldsymbol E\neq0$ 需非零电荷密度；$\theta=0$ 原写法中标架转动与传播相位同速抵消，$k_{\text{eff}}=0$，场根本不传播。**故 Part C2/C3 的实验判据不具备真空自由光子层面的理论基础**，Part C4-1「兼容麦克斯韦方程组」仅在 $\theta=0$ 且做相位补偿时成立。
>
> **不受影响的部分**：Part A 的耦合恒等式 $\boldsymbol p_\gamma\!\cdot\!\boldsymbol\omega_D=K^2S_z$（推导只用到正交归一性，已验至 $10^{-16}$），以及 §14 全部误差传播结论（只依赖 $S_z=\hbar\cos\theta$ 等标量关系）。

---

## 公理前置（场标架分支）

场正交 Frenet 三元组 $\{\boldsymbol e_1,\boldsymbol e_2,\boldsymbol e_3\}$，弧长参数 $s=z$（取沿实验室 $z$ 轴），且 $z=ct$：

$$
\partial_s\begin{pmatrix}\boldsymbol e_1\\\boldsymbol e_2\\\boldsymbol e_3\end{pmatrix}
=
\begin{pmatrix}
0 & \kappa & 0 \\
-\kappa & 0 & \tau \\
0 & -\tau & 0
\end{pmatrix}
\begin{pmatrix}\boldsymbol e_1\\\boldsymbol e_2\\\boldsymbol e_3\end{pmatrix},
\qquad
\kappa=K\cos\theta,\;\tau=K\sin\theta,\;K=\frac{2\pi}{\lambda},
\qquad \kappa^2+\tau^2=K^2
$$

场：
$$
\boldsymbol E=E_0(\boldsymbol e_1+i\boldsymbol e_2)e^{i(Ks-\omega t)},\qquad \omega=cK
$$
$$
\boldsymbol B=\frac{1}{c}\boldsymbol e_3\times\boldsymbol E
$$

局域能流速度恒为 $c$（横波、无纵向分量）。

---

## Part A：动量密度（电磁动量，Minkowski 形式）推导

电磁动量密度（Minkowski 动量密度，真空与 Abraham 动量密度等价）：

$$
\boldsymbol g = \varepsilon_0 \boldsymbol E\times\boldsymbol B
$$

代入真空横波关系 $\boldsymbol B=\tfrac1c\boldsymbol e_3\times\boldsymbol E$：

$$
\boldsymbol g=\varepsilon_0 \boldsymbol E\times\left(\frac{1}{c}\boldsymbol e_3\times\boldsymbol E\right)
=\frac{\varepsilon_0}{c}\Big[(\boldsymbol E\cdot\boldsymbol E)\boldsymbol e_3 - (\boldsymbol E\cdot\boldsymbol e_3)\boldsymbol E\Big]
$$

横波条件 $\boldsymbol E\cdot\boldsymbol e_3=0$，电场严格落在局部横向平面 $\text{span}\{\boldsymbol e_1,\boldsymbol e_2\}$：

$$
\boldsymbol g = \frac{\varepsilon_0|\boldsymbol E|^2}{c}\boldsymbol e_3
$$

时间平均动量密度：

$$
\langle \boldsymbol g\rangle = \frac{\varepsilon_0 |E_0|^2}{c}\boldsymbol e_3
$$

时间平均能量密度 $\langle u\rangle=\tfrac12\varepsilon_0 |E_0|^2$，因此：

$$
\langle\boldsymbol g\rangle = \frac{\langle u\rangle}{c}\boldsymbol e_3
$$

这是真空电磁波标准关系：**动量密度 = 能量密度 / c，沿局域传播基矢 $\boldsymbol e_3$**。

### 动量与 Darboux 向量映射

Darboux 向量：
$$
\boldsymbol\omega_D=\tau\boldsymbol e_1+\kappa\boldsymbol e_3,\qquad |\boldsymbol\omega_D|=K
$$

局域动量沿 $\boldsymbol e_3$，因此动量密度投影到 Darboux：

$$
\langle\boldsymbol g\rangle\cdot\boldsymbol\omega_D
= \frac{\langle u\rangle}{c}\boldsymbol e_3\cdot(\tau\boldsymbol e_1+\kappa\boldsymbol e_3)
= \frac{\langle u\rangle}{c}\kappa
$$

代入 $\kappa=K\cos\theta,\;K=\omega/c$：

$$
\langle\boldsymbol g\rangle\cdot\boldsymbol\omega_D=\langle u\rangle\frac{\omega}{c^2}\cos\theta
$$

单光子层面映射：单光子能量 $E_\gamma=\hbar\omega$，单光子动量期望值（沿局域 $\boldsymbol e_3$）：

$$
\boldsymbol p_\gamma=\frac{E_\gamma}{c}\boldsymbol e_3=\hbar K \boldsymbol e_3
$$

> 单光子动量：$\boldsymbol p_\gamma=\hbar K \boldsymbol e_3$。

点乘 Darboux 向量：

$$
\boldsymbol p_\gamma\cdot\boldsymbol\omega_D=\hbar K \boldsymbol e_3\cdot(\tau\boldsymbol e_1+\kappa\boldsymbol e_3)=\hbar K\kappa=\hbar K^2\cos\theta
$$

联立自旋投影关系 $S_z=\hbar\cos\theta$，得到**动量–自旋–Darboux 耦合恒等式（体系内新方程）**：

$$
\boldsymbol p_\gamma\cdot\boldsymbol\omega_D = \hbar K^2 \frac{S_z}{\hbar}=K^2 S_z
$$

$$
\boxed{\boldsymbol{p_\gamma\cdot\boldsymbol\omega_D = K^2 S_z}}
$$

> 物理解读：光子动量与场标架 Darboux 转动矢量的内积，正比于轴向自旋投影。
> 这是光速螺旋场标架模型独有的几何耦合关系，标准平面波无此结构。

极限校验：

1. $\tau=0,\theta=0,\kappa=K,\;S_z=\hbar$：$\boldsymbol p_\gamma\cdot\boldsymbol\omega_D=K^2\hbar$；普通圆偏振光子特例。
2. $\tau=K,\theta=\pi/2,\kappa=0,\;S_z=0$：$\boldsymbol p_\gamma\cdot\boldsymbol\omega_D=0$；纯扭转标架，自旋投影归零。

---

## Part B：动量密度随弧长 $s$ 演化

全局实验室坐标系下，局域基矢 $\boldsymbol e_3(s)$ 随弧长 $s$ 缓慢偏转（来自 Frenet 标架弯曲 + 扭转）。

~~原（错误）式：$\boldsymbol e_3(s)=-\sin(Ks)\sin\theta\,\hat x+\cos(Ks)\sin\theta\,\hat y-\cos\theta\,\hat z$~~

**修正版（§15.2）**——绕固定 Darboux 轴 $\boldsymbol\omega_D=K\hat z$ 以角速率 $K$ 匀角速转动，记 $\phi=Ks$：

$$
\boxed{
\begin{aligned}
\boldsymbol e_1&=(\cos\theta\cos\phi,\ \cos\theta\sin\phi,\ \sin\theta)\\
\boldsymbol e_2&=(-\sin\phi,\ \cos\phi,\ 0)\\
\boldsymbol e_3&=(-\sin\theta\cos\phi,\ -\sin\theta\sin\phi,\ \cos\theta)
\end{aligned}}
\qquad \boldsymbol\omega_D=\tau\boldsymbol e_1+\kappa\boldsymbol e_3=K\hat z\ \text{（严格恒定）}
$$

代入单光子动量：

$$
\boldsymbol p_\gamma(s)=\hbar K\Big[-\sin\theta\cos(Ks)\,\hat x-\sin\theta\sin(Ks)\,\hat y+\cos\theta\,\hat z\Big]
$$

动量矢量随 $s$ 出现**横向振荡分量**，来自标架的空间扭转。

- 横向动量分量：周期性振荡，时间平均 $\langle p_x\rangle=\langle p_y\rangle=0$；
- 轴向动量分量恒定：$p_z=+\hbar K\cos\theta$（修正标架下为正；原错误标架给出 $-\hbar K\cos\theta$，符号差异已随标架修正确定）。数值复核：`momentum_darboux.py` 输出 $\langle p_z\rangle=+9.371\times10^{-28}$ kg·m/s（$\lambda=500$ nm, $\theta=\pi/4$）。

> 关键结论：**单光子动量全局存在横向微扰振荡，但横向动量平均值为零；净动量沿实验室 $z$ 轴**。
> 这保证了整体动量守恒，不破坏自由空间传播。

---

## Part C：§13 光速螺旋场标架模型 vs 标准麦克斯韦 / QED，可观测实验判据

### C1：标准理论基准

1. 经典麦克斯韦：自由空间单色横波，电场/磁场在固定横向平面；**标架无空间扭转 $\tau=0$**；只有圆偏振带来的相位旋转，不是场标架本身沿传播方向的空间扭转。
2. QED 自由光子：螺旋度严格 $\pm\hbar$；自旋投影只能取这两个离散本征值，不存在连续 $S_z$。

### C2：光速螺旋模型（本模型）独有预言

1. 场标架允许非零挠率 $\tau\in[0,K]$；$\tau\neq0$ 对应**场局部正交三元组沿传播方向同时弯曲 + 扭转**，不是单纯电场相位旋转。
2. 自旋投影 $S_z=\hbar\sqrt{1-(\tau/K)^2}$，**连续取值区间 $0\le|S_z|\le\hbar$**；自由光子不再被强制只能取 $\pm\hbar$。
3. 动量存在局域横向振荡分量（时间平均归零）；可在近场 / 局域探测中寻找局域横向动量密度的空间调制。
4. 三重不变量 $\kappa^2+\tau^2=K^2$；波长固定时，弯曲与挠率可以相互分配。

### C3 实验判决性观测方案（可落地）

#### 判据 1：自旋投影连续谱探测（核心区分实验）

标准 QED：光子自旋投影只能观测到 $\pm\hbar$ 两个峰。
本模型：若存在 $\tau\neq0$ 场标架态，自旋投影测量会出现**连续分布**，在 $0\sim\hbar$ 区间出现信号。

> 难点：需要制备纯 $\tau\neq0$ 光速螺旋场；普通圆偏振光源只能激发 $\tau=0$ 分支。

#### 判据 2：局域横向动量密度成像（纳米光压 / 原子探针）

普通圆偏振光：局域动量严格沿传播轴向，无局域横向动量密度。
光速螺旋场：局域动量密度存在空间周期性横向分量，可通过纳米粒子光力显微，探测周期性横向光压调制。

#### 判据 3：$\kappa,\tau$ 参数的色散 / 波长扫描校验

固定激发构型，改变波长 $\lambda$：

- 本模型：$\kappa^2+\tau^2=(2\pi/\lambda)^2$，随波长平方反比变化；
- 普通偏振光：始终 $\tau=0$。

### C4：模型适用边界与红线

1. $\tau=0$ 子空间完全退化为标准圆偏振电磁波；**本模型包含标准平面波作为特例，数学上兼容麦克斯韦方程组**。
2. $\tau\neq0$ 构型属于**广义正交场标架解**，不是常规平面波解；需要特殊光学结构（涡旋、结构光）来尝试激发。
3. 本模型是场几何微分几何模型，**不替代 QED，是一套几何等效描述框架；所有预言必须由实验判决**。

---

## Part D：Python 复现模块（动量密度演化 + Darboux 耦合）

代码落地于 `04_理论推导/momentum_darboux.py`：

- `frenet_frame_lightspeed(s, K, theta)`：返回 $\boldsymbol e_1,\boldsymbol e_2,\boldsymbol e_3,\kappa,\tau,\boldsymbol\omega_D$；
- `momentum_density(E0, e3)`：返回时间平均动量密度 $\langle\boldsymbol g\rangle=\varepsilon_0|E_0|^2/c\,\boldsymbol e_3$（注意修正了纯标量版漏写 $1/c$ 的量纲问题）；
- `photon_momentum(K, e3)`：$\boldsymbol p_\gamma=\hbar K\boldsymbol e_3$；
- `darboux_coupling(K, theta)`：返回 $\boldsymbol p_\gamma\cdot\boldsymbol\omega_D$ 与 $K^2 S_z$ 的对照；
- 绘图：`plot_momentum_evolution`（Part B 横向 / 轴向动量随 $s$ 振荡）、`plot_darboux_coupling`（Part A 耦合恒等式随 $\theta$ 连续谱校验），输出 `momentum_evolution.svg` 与 `darboux_coupling.svg`。

核心片段（Part A 数值对照）：

```python
lam = 500e-9
K = 2*math.pi/lam
theta = math.pi/4
s_list = np.linspace(0, 2*lam, 10)
E0 = 1.0
hbar = 1.054571817e-34

print("=== Light Speed Helix: Momentum & Darboux Inner Product ===")
for s in s_list:
    e1,e2,e3,kappa,tau,omegaD = frenet_frame_lightspeed(s,K,theta)
    g_avg = momentum_density(E0,e3)
    p_gamma = photon_momentum(K, e3)
    p_dot_omegaD = np.dot(p_gamma, omegaD)
    Sz = hbar * np.sqrt(1 - (tau/K)**2)
    K2Sz = K**2 * Sz
    print(f"s={s:.2e}, tau={tau:.2e}, p.wD={p_dot_omegaD:.2e}, K2*Sz={K2Sz:.2e}, Sz/hbar={Sz/hbar:.3f}")
```

输出应出现 `p·ωD` 与 `K²·Sz` 每步严格相等（机器精度），验证耦合恒等式；`Sz/ħ` 随 `theta` 连续变化于 $[0,1]$。

---

## Part E：可选下一阶段任务（4 条分支）

1. **守恒律完整证明**：能量守恒、动量守恒、角动量守恒，写出守恒流密度与 Noether 对应；
2. **非单色波包**：高斯波包光速螺旋，研究标架在波包前沿 / 后沿的畸变，色散效应；
3. **角动量流张量**：分离自旋流与轨道角动量流，和涡旋光（OAM）做对比；
4. **§14：误差传播迁移**：误差传播迁移到自旋投影与动量测量，计算 $\sigma_{S_z}$ 如何由 $\sigma_\lambda,\sigma_\theta$ 误差传导。

> 待选定方向后继续推进。本 §13 的诚实边界：耦合恒等式 $\boldsymbol p_\gamma\cdot\boldsymbol\omega_D=K^2S_z$ 是场标架几何内的数学关系，其物理可观测性依赖能否制备 $\tau\neq0$ 场标架态（判据 1 难点），在实验未证实前仅作模型结构标识。
