# 任务 3 · 用量纲分析推出光速 $c$ 的来源

> 目标：只用量纲、不借助微分方程，证明由 $\varepsilon_0,\mu_0$ 组合成速度的形式**唯一**是 $1/\sqrt{\mu_0\varepsilon_0}$。

---

## 3.1 两个真空电磁常数的量纲

$$
[\varepsilon_0]=\mathrm{M^{-1}\,L^{-3}\,T^{4}\,I^{2}},\qquad
[\mu_0]=\mathrm{M\,L\,T^{-2}\,I^{-2}}
$$

## 3.2 相乘与化简

$$
[\mu_0\varepsilon_0]=[\mu_0][\varepsilon_0]
=\mathrm{M\,L\,T^{-2}\,I^{-2}}\cdot\mathrm{M^{-1}\,L^{-3}\,T^{4}\,I^{2}}
=\mathrm{L^{-2}\,T^{2}}
$$

取倒数：

$$
\left[\frac{1}{\mu_0\varepsilon_0}\right]=\mathrm{L^{2}\,T^{-2}}
$$

开方：

$$
\left[\frac{1}{\sqrt{\mu_0\varepsilon_0}}\right]=\mathrm{L\,T^{-1}}
$$

$\mathrm{L\,T^{-1}}$ 正是**速度量纲**，故猜测

$$
\boxed{\,c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}\,}
$$

---

## 3.3 唯一性证明（量纲代数的线性方程组）

仅凭「量纲对得上」不足以声称这是唯一组合。设候选组合 $\varepsilon_0^{a}\mu_0^{b}$，要求其量纲为速度 $\mathrm{L\,T^{-1}}$，逐基本量纲列方程：

$$
\begin{array}{rcl}
\mathrm{M}: & -a+b & = 0\\
\mathrm{L}: & -3a+b & = 1\\
\mathrm{T}: & 4a-2b & = -1\\
\mathrm{I}: & 2a-2b & = 0
\end{array}
$$

由 $\mathrm{M}$ 与 $\mathrm{I}$ 式均得 $a=b$；代入 $\mathrm{L}$ 式：$-2a=1\Rightarrow a=-\tfrac12$；代入 $\mathrm{T}$ 式校验：$4(-\tfrac12)-2(-\tfrac12)=-2+1=-1$ ✔ 相容。

$$
\boxed{a=b=-\tfrac12\ \Longrightarrow\ \varepsilon_0^{-1/2}\mu_0^{-1/2}=\frac{1}{\sqrt{\mu_0\varepsilon_0}}\ \text{是唯一解}}
$$

> 4 个方程、2 个未知量且相容 ⇒ 解唯一。这是量纲分析（Buckingham $\Pi$ 定理的特例）能给出的**最强结论**：形式唯一，数值不给。

---

## 3.4 数值（CODATA / SI 定义值）

| 量 | 值 | 状态 |
|---|---|---|
| $c$ | $299\,792\,458\ \mathrm{m/s}$ | **SI 定义值**（精确，无不确定度） |
| $\mu_0$ | $1.256\,637\,062\,12(19)\times10^{-6}\ \mathrm{H/m}$ | 测量导出值（2019 起不再是定义常数） |
| $\varepsilon_0$ | $8.854\,187\,8128(13)\times10^{-12}\ \mathrm{F/m}$ | 由 $\varepsilon_0=1/(\mu_0c^2)$ 导出 |

代入校验：$1/\sqrt{\mu_0\varepsilon_0}=2.99792458\times10^{8}\ \mathrm{m/s}=c$ ✔

> **A7 物理边界（重要）**：2019 年 SI 修订后，$c$ 与 $e$（基本电荷）、$h$（普朗克常数）成为**定义常数**，$\mu_0$ 不再精确等于 $4\pi\times10^{-7}$。因此现代口径下因果方向是**反转**的：不是「由实验测得的 $\mu_0,\varepsilon_0$ 算出光速」，而是「$c$ 为定义值，$\mu_0$ 由精细结构常数 $\alpha$ 测得，$\varepsilon_0=1/(\mu_0c^2)$ 随之导出」。
> 量纲分析本身不受影响——它给出的仍是 $\varepsilon_0,\mu_0,c$ 三者之间的**恒等约束** $\varepsilon_0\mu_0c^2=1$，该约束在任何 SI 版本下都成立；但**不能**据此宣称「量纲分析预言了光速的数值」。数值来自测量，量纲只给形式。

---

## 3.5 波动方程对照（独立交叉验证）

由麦克斯韦方程组在无源真空中消去磁场：

$$
\nabla^{2}\boldsymbol{E}=\mu_0\varepsilon_0\frac{\partial^{2}\boldsymbol{E}}{\partial t^{2}}
$$

与标准波动方程 $\nabla^{2}\psi=\dfrac{1}{v^{2}}\partial_t^{2}\psi$ 对照，直接读出

$$
v=\frac{1}{\sqrt{\mu_0\varepsilon_0}}=c
$$

量纲核验：$[\mu_0\varepsilon_0]=\mathrm{L^{-2}T^{2}}=[\partial_t^{2}/\nabla^{2}]$ ✔

这是与量纲分析**独立**的第二条路径（动力学导出 vs 量纲约束），二者一致构成交叉印证。

---

## 3.6 三层分离小结

| 层 | 结论 |
|---|---|
| **数学定义** | $\varepsilon_0\mu_0c^2=1$（SI 恒等式） |
| **量纲分析** | 由 $[\varepsilon_0],[\mu_0]$ 构造速度量纲的组合**唯一**为 $(\mu_0\varepsilon_0)^{-1/2}$；**不给数值** |
| **本体论解释** | 真空电磁相互作用的传播速度由真空电磁常数决定 ⇒ 光是电磁波（Maxwell 1865 的历史洞见）；但该结论的**物理内容**来自麦克斯韦方程组的动力学结构，量纲分析只是相容性约束，不能单独承担「光即电磁波」这一物理主张 |
