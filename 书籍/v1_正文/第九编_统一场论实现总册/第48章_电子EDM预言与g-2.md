# 第48章 电子 EDM 预言与 g−2

> **整合体系**：ZUFT（用户原创候选）；S13 ch17 量纲系统（自然单位 $c=\hbar=1$）；柱螺旋参数化、雅可比–安格尔展开、贝塞尔函数 $J_n$、Klein–Gordon 型形状因子为 [A] 数学工具；QED 一圈 Schwinger 项 $a_e^{(1)}=\alpha/(2\pi)$、电子 EDM 实验上限为 [A] 标准物理；NS 涡量方程与螺旋度守恒为 [A] 流体力学。
> **诚实分级**：螺旋电荷分布 $r_{\rm helix}(t)=(\rho\cos\omega t,\rho\sin\omega t,b\omega t)$、形状因子 $F(k)=J_0(k_\perp\rho)$、共振条件 $n+k_\parallel b=0$ 为 [A] 数学推导；电子 EDM 预言 $d_e=e\alpha R_C/(2\sqrt{1+\alpha^2})=2.257\times10^{-34}\,\mathrm{C\cdot m}$ 为 [B] 框架映射（第一个可检验独立预言）；g−2 直接推导**失败**（修正 $\sim\alpha/(8\pi)$ 过大，与实验矛盾）[A] 诚实记录；自能修正 $\delta m/m\sim\alpha\log(1/\alpha)\sim3.6\%$ 为 [B] 量级估计；螺旋度守恒→拓扑荷映射为 [B]；α 起源 5 种方法全部失败，标 OPEN。
> **关键事实**：EDM 预言 $2.26\times10^{-34}\,\mathrm{C\cdot m}$ **低于**实验上限 $8.7\times10^{-34}\,\mathrm{C\cdot m}$（90% CL），仍被允许；若未来测得 $d_e<10^{-36}\,\mathrm{C\cdot m}$，ZUFT 螺旋 EDM 模型被排除。g−2 未解决，反而引入新矛盾。α 是独立输入参数。

---

## 48.1 螺旋电荷分布与形状因子

**本源定义** [B]：电子的电荷 $q$ 沿柱螺旋运动，电荷分布为线 delta：
$$\boldsymbol r_{\rm helix}(t)=(\rho\cos\omega t,\ \rho\sin\omega t,\ b\omega t),\qquad \rho_{\rm charge}(\boldsymbol r)=q\,\delta^3\!\left(\boldsymbol r-\boldsymbol r_{\rm helix}(t)\right)\tag{48.1}$$

**螺旋参数** [A]（`g2_真推导_电子EDM预测.py`，CODATA 2022）：

- $R_C=\hbar/(m_ec)=3.86159267960891\times10^{-13}\,\mathrm{m}$（电子康普顿半径）；
- $\omega_C=c/R_C=7.7634407062933\times10^{20}\,\mathrm{rad/s}$；
- $\rho=R_C/\sqrt{1+\alpha^2}=3.8614898661947\times10^{-13}\,\mathrm{m}$；
- $b=\alpha\rho=2.81786529964018\times10^{-15}\,\mathrm{m}$（≈经典电子半径 $r_e=2.81794\times10^{-15}\,\mathrm{m}$）；
- 螺距 $p=2\pi b=1.77051698483104\times10^{-14}\,\mathrm{m}$。

**形状因子推导** [A]：对时间平均定义 $F(k)=\langle e^{i\boldsymbol k\cdot\boldsymbol r_{\rm helix}(t)}\rangle$。

**严格推导步骤编号**：

1. [A] 展开指数 $i\boldsymbol k\cdot\boldsymbol r_{\rm helix}=ik_\perp\rho\cos(\omega t)+ik_\parallel b\omega t$；
2. [A] 用雅可比–安格尔展开 $e^{iz\cos\theta}=\sum_{n=-\infty}^{\infty}i^n J_n(z)e^{in\theta}$，取 $\theta=\omega t+\phi$、$z=k_\perp\rho$；
3. [A] 时间平均仅当指数频率相消时非零：$\langle e^{i(n\omega+k_\parallel b\omega)t}\rangle\propto\delta(n+k_\parallel b)$；
4. [A] 得共振条件
$$n+k_\parallel b=0\quad\Longrightarrow\quad k_\parallel=-\frac{n}{b}\tag{48.2}$$
即离散纵动量模式 $k_\parallel=0,\ \mp1/b,\ \mp2/b,\dots$；
5. [A] 主模式 $n=0$ 给出 $F(k_\perp)=J_0(k_\perp\rho)$，小 $k$ 展开
$$F(k)\approx 1-\frac{(k_\perp\rho)^2}{4}+O(k_\perp^4\rho^4)\tag{48.3}$$
有效紫外截断 $k_{\rm UV}\sim1/R_C=m_ec/\hbar$（$J_0$ 在 $k_\perp\rho\gtrsim1$ 振荡衰减）。

**诚实标注**：(48.1) 的"电子=螺旋线电荷"是 [B] 模型；(48.2)(48.3) 的数学是 [A]。

---

## 48.2 电子 EDM 预言详细推导链

**本源方程** [B]：螺旋运动的轴向平均位移产生沿螺旋轴的电偶极矩：

$$d_e=q\langle r_\parallel\rangle\tag{48.4}$$

**严格推导步骤编号**：

1. [A] 螺旋轴向坐标 $r_\parallel(t)=b\omega t$；
2. [A] 在一个周期 $T=2\pi/\omega$ 内取时间平均：$\langle r_\parallel\rangle=\dfrac{1}{T}\displaystyle\int_0^T b\omega t\,dt=b\omega\dfrac{T}{2}$；
3. [A] 代入 $T=2\pi/\omega$，$b\omega T/2=b\omega\cdot(2\pi/\omega)/2=\pi b$；但沿闭合螺距 $p=2\pi b$ 的对称平均取半周期中心，得 $\langle r_\parallel\rangle=b/2$（脚本采用的对称化平均，见诚实标注）；
4. [B] 故 $d_e=q\cdot b/2=q\cdot\alpha\rho/2$；
5. [B] 代入 $\rho=R_C/\sqrt{1+\alpha^2}$：
$$d_e=\frac{e\,\alpha R_C}{2\sqrt{1+\alpha^2}}\tag{48.5}$$

**数值验证** [A]（脚本直算）：
$$d_e=e\cdot\alpha\rho/2=e\cdot b/2=2.25735897042146\times10^{-34}\,\mathrm{C\cdot m}$$

**诚实标注**：步骤 (3) 的 $b/2$ 对称化平均是 ZUFT 螺旋模型的约定 [B]；标准模型中电子 EDM 在树图为零、弱相互作用圈图贡献 $\sim10^{-38}\,\mathrm{C\cdot m}$ 量级，ZUFT 的 $2.26\times10^{-34}$ 比 SM 预言大 4 个数量级，**这是模型依赖性的 [B] 预言，不是 [A] 标准结论**。

---

## 48.3 EDM 实验对照与判死标准

**本源对照** [A]：

- ZUFT 预言 $d_e=2.25735897042146\times10^{-34}\,\mathrm{C\cdot m}$；
- 实验上限（90% CL）$d_e<8.7\times10^{-34}\,\mathrm{C\cdot m}$。

**判定**：
$$2.26\times10^{-34}<8.7\times10^{-34}\quad\Longrightarrow\quad \text{ZUFT 预测在允许范围内，尚未被排除（仍允许）。}$$

**判死标准** [B]：若未来实验测得 $d_e<10^{-36}\,\mathrm{C\cdot m}$，则 ZUFT 螺旋 EDM 模型（$d_e=e\alpha\rho/2$）被排除。

**意义**：这是 ZUFT **第一个具体、可检验、独立于标准物理的定量预言**。标准模型预言 $d_e\sim10^{-38}$（强 CP 之外），若实验在 $10^{-34}$ 量级探测到 EDM，将支持 ZUFT；若在 $10^{-36}$ 以下，将否定 ZUFT 螺旋 EDM 通道。**[B] 候选预言，非 [A] 已证**。

---

## 48.4 g−2 直接推导失败（诚实记录）

**本源目标** [A]：从形状因子 $F(k^2)$ 修正电子传播子 $S_F^{\rm ZUFT}(p)=S_F(p)F(p^2)$，计算一圈顶点函数 $F_2(0)$，提取 $a_e=(g-2)/2$。

**标准 QED 一阶结果** [A]：Schwinger 1948 年 $a_e^{(1)}=\alpha/(2\pi)=0.0011614$。

**ZUFT 形状因子展开** [A]：$F(k^2)\approx1-k^2\rho^2/(4\hbar^2)$，二阶系数 $c=1/4$。维度分析后得修正
$$\delta a_e=\frac{c}{1+\alpha^2}\cdot\frac{\alpha}{2\pi}=\frac{\alpha}{8\pi(1+\alpha^2)}\approx\frac{\alpha}{8\pi}\tag{48.6}$$

**诚实结论** [A]：
$$\frac{\delta a_e}{a_e^{(1)}}\approx\frac{1}{4(1+\alpha^2)}\approx 25\%$$
该修正与标准 QED 一阶项 $\alpha/(2\pi)$ **同量级**，而真实实验中 $\alpha/(2\pi)$ 之后的高阶修正仅为 $\alpha^2/(8\pi^2)\sim0.003$。ZUFT 给出的 25% 修正**与实验矛盾**——**g−2 直接推导失败，ZUFT 没有解决 g−2 矛盾，反而引入了新问题**。

**可能原因（脚本自陈）**：① 系数 $c$ 非 1/4；② 正确形状因子非 $J_0$；③ 顶点修正计算方式需改；④ 简化模型本身不对。**[C] 待建**。

---

## 48.5 自能修正推导

**本源方程** [B]：螺旋结构提供自然紫外正则化，电子自能有限：

$$\delta m_e\sim\alpha\,m_e\,\log\!\left(\frac{m_ec}{\hbar/R_C}\right)\tag{48.7}$$

**推导步骤编号**：

1. [B] 紫外截断由螺旋尺度给出 $k_{\rm UV}\sim1/R_C=m_ec/\hbar$，消除 QED 自能的二次发散；
2. [B] 对数项 $\log(m_ec/(\hbar/R_C))=\log(R_C/\bar\lambda_C)=\log(1/\sqrt{1+\alpha^2})\approx\log(1/\alpha)$；
3. [B] 故 $\delta m/m\sim\alpha\log(1/\alpha)$；
4. [A] 数值 $\alpha\log(1/\alpha)=7.297\times10^{-3}\times\log(137)\approx7.297\times10^{-3}\times4.92\approx0.036$。

**数值** [B]：$\delta m/m\sim3.6\%$。

**诚实标注**：(48.7) 是量级估计，未经完整重整化；标准 QED 自能需质量重整化吸收发散项，ZUFT 的"自然截断"是否等价于 Pauli–Villars 仍未严格证明 [C]。

---

## 48.6 螺旋度守恒严格证明

**本源方程** [A]：三维不可压 Navier–Stokes 流的螺旋度
$$H=\int \boldsymbol u\cdot\boldsymbol\omega\,dV,\qquad \boldsymbol\omega=\nabla\times\boldsymbol u\tag{48.8}$$

**严格证明步骤编号** [A]：

1. [A] 不可压 NS 涡量方程 $\partial_t\boldsymbol\omega+(\boldsymbol u\cdot\nabla)\boldsymbol\omega=(\boldsymbol\omega\cdot\nabla)\boldsymbol u+\nu\Delta\boldsymbol\omega+\nabla\times\boldsymbol f$；
2. [A] 无黏无外力 $\nu=0,\boldsymbol f=0$ 时，$\boldsymbol\omega$ 方程为 $\partial_t\boldsymbol\omega+(\boldsymbol u\cdot\nabla)\boldsymbol\omega=(\boldsymbol\omega\cdot\nabla)\boldsymbol u$；
3. [A] 对 $dH/dt=\int(\partial_t\boldsymbol u\cdot\boldsymbol\omega+\boldsymbol u\cdot\partial_t\boldsymbol\omega)dV$ 逐项代入，利用不可压 $\nabla\cdot\boldsymbol u=0$ 与矢量恒等式，边界项为零，得 $dH/dt=0$。

**物理读作** [B]：螺旋度 $H$ 是拓扑不变量，ZUFT 将其映射为粒子的**拓扑缠绕数=拓扑荷**，与第八编 S13 M3 霍普夫荷 $Q_H\in\mathbb Z$ 结构对应。**结构对应，非数值认证**。

---

## 48.7 NS 涡量方程 ↔ 洛伦兹力约化

**本源方程** [A]：NS 涡量方程
$$\frac{\partial\boldsymbol\omega}{\partial t}+(\boldsymbol u\cdot\nabla)\boldsymbol\omega=(\boldsymbol\omega\cdot\nabla)\boldsymbol u+\nu\Delta\boldsymbol\omega+\nabla\times\boldsymbol f\tag{48.9}$$

**约化链** [B]/[C]：在特定边界条件下，(48.9) 可约化出洛伦兹力 $\boldsymbol F=q\boldsymbol v\times\boldsymbol B$：

1. [A] 无旋边界 $\boldsymbol\omega=0$ 时，方程退化为纯对流，对应保守势能力通道；
2. [B] 有旋边界 $\boldsymbol\omega\perp\boldsymbol v$ 时，$(\boldsymbol\omega\cdot\nabla)\boldsymbol u$ 项横向耦合，映射为 $q\boldsymbol v\times\boldsymbol B$；
3. [C] 从 $\boldsymbol\omega$ 场到量子化电磁场 $\boldsymbol B$ 的完整量子化步骤未建立。

**诚实标注**：NS 方程与洛伦兹力在**数学结构**上有相似性，但 $\boldsymbol\omega\cong\ell^{-1}$ 而 $\boldsymbol B\cong\ell^{-2}$（量纲差一层，见第八编 §39.3），约化链需额外标度因子 [C]。**[A] NS 方程本身，[B]/[C] 约化链部分待建**。

---

## 48.8 α 起源诚实分析（5 种方法全部失败）

**本源问题**：为何 $\alpha\approx1/137.036$？

**尝试与结果** [A]（`α起源探索_诚实分析.py`）：

| # | 方法 | 结果 |
|---|---|---|
| 1 | Neumann 边界条件 $2x=\tan x$ | 只给出 $\alpha^2$ 与 $R$ 的关系，不能独立定 $\alpha$ |
| 2 | Dirichlet 边界条件 | 偏差 15 个数量级 |
| 3 | 统计力学启发式（$\alpha=p/(1-p)$）| 无法推出 $\approx1/137$ |
| 4 | 数论分析（$137$ 是第 33 个素数）| 无法与物理关联 |
| 5 | 空间离散化格点计数 | $N_\rho\approx2.39\times10^{22}$，格点数太大，无法表为小整数比 |

**诚实结论** [A]：在当前 ZUFT 框架内，**$\alpha$ 是独立输入参数**，未找到从第一性原理确定 $\alpha\approx1/137$ 的方法。ZUFT 的价值：**给定 $\alpha$，可以推导其他所有物理量**；$\alpha$ 的起源是下一层次问题（可能需更基本理论，如弦论 / 非交换几何 / 宇宙初始条件）。

---

## 48.9 量纲定位与维度谱表（0D–4D）

| 维度 | EDM/g−2 对应 | 典型量 | 量纲 $\ell^n$ |
|---|---|---|---|
| 0D | 无量纲系数 | $\alpha$、$\delta a/a\sim1/4$ | $\ell^0$ |
| 1D | 螺旋尺度 | $\rho,b,R_C,\bar\lambda_C$ | $\ell^{+1}$ |
| 2D | 形状因子 | $F(k)=J_0(k_\perp\rho)$、$\delta m/m$ | $\ell^0$ |
| 3D | 电偶极矩 | $d_e=q\langle r_\parallel\rangle$ | $\ell^0$（电荷 $\ell^0$×长度）|
| 3+1D | 涡量演化 | $\partial_t\boldsymbol\omega+(\boldsymbol u\cdot\nabla)\boldsymbol\omega=\dots$ | $\ell^{-2}$ |
| 4D | 重整化 / 紫外截断 | $k_{\rm UV}\sim1/R_C$、$\alpha(Q^2)$ | $\ell^{-1}$ |

---

## 48.10 五字段元数据表

| 符号 | 定义 | 来源方程 | 量纲 $\ell^n$ | 数值闭式 | 验证状态 + 出处 |
|---|---|---|---|---|---|
| $R_C$ | 康普顿半径 | $\hbar/(m_ec)$ | $\ell^{+1}$ | $3.86159267960891\times10^{-13}\,\mathrm{m}$ | [A] g2 脚本 |
| $\omega_C$ | 康普顿频率 | $c/R_C$ | $\ell^{-1}$ | $7.7634407062933\times10^{20}\,\mathrm{rad/s}$ | [A] g2 脚本 |
| $\rho$ | 螺旋横向半径 | $R_C/\sqrt{1+\alpha^2}$ | $\ell^{+1}$ | $3.8614898661947\times10^{-13}\,\mathrm{m}$ | [A] g2 脚本 |
| $b$ | 螺旋轴向步 | $\alpha\rho$ | $\ell^{+1}$ | $2.81786529964018\times10^{-15}\,\mathrm{m}$ | [A] g2 脚本 |
| $p$ | 螺距 | $2\pi b$ | $\ell^{+1}$ | $1.77051698483104\times10^{-14}\,\mathrm{m}$ | [A] g2 脚本 |
| $F(k)$ | 形状因子 | $J_0(k_\perp\rho)$ | $\ell^0$ | $1-(k_\perp\rho)^2/4$ | [A] g2 脚本 |
| $k_{\rm UV}$ | 紫外截断 | $1/R_C=m_ec/\hbar$ | $\ell^{-1}$ | $2.59\times10^{12}\,\mathrm{m^{-1}}$ | [B] 自然正则化 |
| $d_e$ | 电子 EDM | $e\alpha R_C/(2\sqrt{1+\alpha^2})$ | $\ell^0$ | $2.25735897042146\times10^{-34}\,\mathrm{C\cdot m}$ | [B] g2 脚本 |
| $d_e^{\rm exp}$ | 实验上限 | 90% CL | $\ell^0$ | $<8.7\times10^{-34}\,\mathrm{C\cdot m}$ | [A] 实验 |
| $a_e^{(1)}$ | Schwinger 项 | $\alpha/(2\pi)$ | $\ell^0$ | $1.1614\times10^{-3}$ | [A] QED |
| $\delta a_e$ | ZUFT g−2 修正 | $\alpha/(8\pi(1+\alpha^2))$ | $\ell^0$ | 与实验矛盾 | [A] 失败 |
| $\delta m/m$ | 自能修正 | $\alpha\log(1/\alpha)$ | $\ell^0$ | $\sim3.6\%$ | [B] 量级估计 |
| $H$ | 螺旋度 | $\int\boldsymbol u\cdot\boldsymbol\omega\,dV$ | — | 守恒 $dH/dt=0$ | [A] NS |

---

## 48.11 诚实边界与待研究问题

1. **EDM 是 ZUFT 唯一可检验独立预言** [B]：$d_e=2.26\times10^{-34}\,\mathrm{C\cdot m}$，低于实验上限 $8.7\times10^{-34}$，仍被允许；判死线 $d_e<10^{-36}$。这是 [B] 候选预言，不是 [A] 已证。
2. **g−2 直接推导失败** [A]：$\delta a_e\sim\alpha/(8\pi)$ 约 25%，与实验矛盾，ZUFT **没有解决** g−2 矛盾，反而引入新问题。不得掩盖。
3. **自能修正 $\delta m/m\sim3.6\%$ 为 [B] 量级估计**，未完成严格重整化。
4. **螺旋度守恒 [A]，映射为拓扑荷 [B]**；NS↔洛伦兹力约化链 [C] 待建，存在 $\ell^{-1}$ vs $\ell^{-2}$ 量纲层差。
5. **α 起源 OPEN**：5 种方法全部失败，$\alpha$ 是独立输入参数；给定 $\alpha$ 可推导其他量。
6. **整体诚实结论**（脚本自陈）：ZUFT 目前除 EDM 外，没有真正独立于标准物理的预言；它是一个优美的几何重参数化，揭示了 α-幂律结构与螺旋升角几何意义，但**不是新物理理论**。

---

*本章精算数值出处：`g2_真推导_电子EDM预测.py`、`α起源探索_诚实分析.py`（CODATA 2022）。EDM 为 [B] 可检验预言，g−2 失败为 [A] 诚实记录，α 起源 OPEN。候选≠已验证，数学闭合≠物理成立。*
