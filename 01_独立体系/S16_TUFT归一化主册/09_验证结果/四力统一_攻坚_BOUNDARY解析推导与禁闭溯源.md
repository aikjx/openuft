# 四力统一_攻坚 —— BOUNDARY 解析推导与禁闭缺陷溯源

> 所属独立体系：[TUFT 归一化主册](../README.md)
> 关联：[09_验证结果/四力大统一_验证摘要_结构化整理](./四力大统一_验证摘要_结构化整理.md) · [11_证伪与反例/四力统一验证_FAIL与BOUNDARY攻破台账](../11_证伪与反例/四力统一验证_FAIL与BOUNDARY攻破台账.md)
> 定位：对 BOUNDARY 项（B1：$\nabla\kappa\perp\nabla\tau$）做解析推导，对 FAIL 项（F1：禁闭线性势非 Proca 齐次解）做修复路线溯源。**本文件为整理登记与解析记录，不构成物理结论背书。**
> 登记状态：`registered`（解析攻坚记录）

---

## 一、BOUNDARY B1 攻坚：$\boldsymbol{\nabla}\kappa \perp \boldsymbol{\nabla}\tau$ 解析推导

**命题**：检验 $\boldsymbol{\nabla}\kappa \cdot \boldsymbol{\nabla}\tau = 0$。

**前置已知（圆柱螺旋单粒子几何，L1 已验证）**：
$$ \kappa=\frac{\rho}{\rho^2+b^2},\qquad \tau=\frac{b}{\rho^2+b^2} $$
其中 $\rho,b$ 为螺旋几何参数；在原始单世界线版本中 $\rho,b$ 为常数（固定螺旋）。

### 1.1 固定参数情形（单粒子螺旋，$\rho=\mathrm{const},\ b=\mathrm{const}$）

$\rho,b$ 是常数 → $\kappa,\tau$ 都是常数：
$$ \boldsymbol{\nabla}\kappa=\boldsymbol{0},\qquad \boldsymbol{\nabla}\tau=\boldsymbol{0} $$
零向量点积 $0\cdot0=0$，形式上满足正交。

**👉 但平凡成立，无物理意义：常数场没有梯度。**
这正是文档 BOUNDARY 的根源：单粒子螺旋的 $(\kappa,\tau)$ 是常数，梯度正交是平凡的；一旦推广到空间场分布，$\rho(\boldsymbol r),b(\boldsymbol r)$ 变成空间位置的场函数，命题不再自动成立。

### 1.2 推广到场论版本：$\rho=\rho(\boldsymbol r),\ b=b(\boldsymbol r)$

$$ \kappa(\boldsymbol r)=\frac{\rho}{\rho^2+b^2},\qquad \tau(\boldsymbol r)=\frac{b}{\rho^2+b^2} $$
记分母 $D=\rho^2+b^2$，则 $\kappa=\rho/D,\ \tau=b/D$。求梯度：
$$ \boldsymbol{\nabla}\kappa =\frac{\boldsymbol{\nabla}\rho}{D}-\frac{\rho}{D^2}\big(2\rho\boldsymbol{\nabla}\rho+2b\boldsymbol{\nabla}b\big) =\frac{1}{D^2}\Big[\big(D-2\rho^2\big)\boldsymbol{\nabla}\rho-2\rho b\,\boldsymbol{\nabla}b\Big] $$
$$ \boldsymbol{\nabla}\tau =\frac{\boldsymbol{\nabla}b}{D}-\frac{b}{D^2}\big(2\rho\boldsymbol{\nabla}\rho+2b\boldsymbol{\nabla}b\big) =\frac{1}{D^2}\Big[-2\rho b\,\boldsymbol{\nabla}\rho+\big(D-2b^2\big)\boldsymbol{\nabla}b\Big] $$

### 1.3 点积化简与最终紧凑形式

做点积：
$$ \boldsymbol{\nabla}\kappa\cdot\boldsymbol{\nabla}\tau =\frac{1}{D^4}\Big[ \big(D-2\rho^2\big)(-2\rho b)|\boldsymbol{\nabla}\rho|^2 +\big(D-2\rho^2\big)\big(D-2b^2\big)\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b +(-2\rho b)(-2\rho b)\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b +(-2\rho b)\big(D-2b^2\big)|\boldsymbol{\nabla}b|^2 \Big] $$

代入 $D=\rho^2+b^2$，化简系数：
$$ D-2\rho^2=b^2-\rho^2,\qquad D-2b^2=\rho^2-b^2 $$
$$ \begin{aligned}
\boldsymbol{\nabla}\kappa\cdot\boldsymbol{\nabla}\tau =\frac{1}{D^4}\Big[&-2\rho b(b^2-\rho^2)|\boldsymbol{\nabla}\rho|^2\\
&+\big(b^2-\rho^2\big)\big(\rho^2-b^2\big)\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b\\
&+4\rho^2b^2\,\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b\\
&-2\rho b\big(\rho^2-b^2\big)|\boldsymbol{\nabla}b|^2\Big]
\end{aligned} $$

合并交叉项 $\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b$ 的系数：
$$ -(b^2-\rho^2)^2+4\rho^2b^2=-(\rho^4-2\rho^2b^2+b^4)+4\rho^2b^2=-\rho^4+6\rho^2b^2-b^4 $$

**最终紧凑形式**：
$$ \boldsymbol{\nabla}\kappa\cdot\boldsymbol{\nabla}\tau =\frac{1}{(\rho^2+b^2)^4}\Big[ 2\rho b(\rho^2-b^2)\big(|\boldsymbol{\nabla}b|^2-|\boldsymbol{\nabla}\rho|^2\big)+\big(-\rho^4+6\rho^2b^2-b^4\big)\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b \Big] $$

### 1.4 关键结论

**$\boldsymbol{\nabla}\kappa\cdot\boldsymbol{\nabla}\tau=0$ 不是恒等式！** 只有在附加约束条件下才等于 0：
$$ \boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b=0,\qquad |\boldsymbol{\nabla}\rho|=|\boldsymbol{\nabla}b| $$

**本质判定**：场层面的垂直原理 $\nabla\kappa\perp\nabla\tau$ 是**额外强加的约束方程**，不是螺旋几何自带的推论。这是 BOUNDARY 项的本质：
- 单粒子固定螺旋：平凡成立（常数场，无梯度）；
- 一般场分布 $\rho(\boldsymbol r),b(\boldsymbol r)$：**不自动成立**，必须额外假设 $\rho$ 场与 $b$ 场梯度正交且模相等。

> 含义：垂直原理从"单粒子曲线标架"推广到"连续场分布"的成立，需要把 $\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b=0$ 且 $|\boldsymbol{\nabla}\rho|=|\boldsymbol{\nabla}b|$ 作为**场方程层面的附加约束/构造条件**嵌入 TUFT，而非可由 Proca 型方程自动导出。

---

## 二、L3 FAIL F1 攻坚：禁闭线性势 $\sigma r$ 的修复路线溯源

**问题复述**：原 Proca 齐次方程 $(\nabla^2-\mu^2)\kappa=0$ 代入禁闭势 $\Phi=\sigma r$：
$$ \nabla^2(\sigma r)=\sigma\,\frac{2}{r},\qquad (\nabla^2-\mu^2)(\sigma r)=\sigma\Big(\frac{2}{r}-\mu^2 r\Big)\neq 0 $$
齐次 Proca 无法容纳线性项。

### 2.1 路线 1：非齐次 Proca（源项携带禁闭）

$$ (\nabla^2-\mu^2)\kappa = S(\boldsymbol r) $$
令源 $S(\boldsymbol r)$ 不是 δ 函数，而是能生成线性势的空间分布源。由 $\nabla^2(\sigma r)=2\sigma/r$：
$$ S(\boldsymbol r)=\frac{2\sigma}{r}-\mu^2\sigma r $$

- ✅ **数学可行**：方程有解 $\kappa=\sigma r$。
- ❌ **代价**：源项 $S(\boldsymbol r)$ 是**新引入的场**，不是从 $(\kappa,\tau)$ 几何自动生成，属外部输入。需物理上解释这个源是什么，几何上必须绑定到螺旋曲率挠率。

### 2.2 路线 2：非线性场方程（内生禁闭）

Proca 是线性二阶；QCD 禁闭来自非线性自耦合（胶子自相互作用）。候选修改：
$$ \nabla^2\kappa-\mu^2\kappa+\lambda\kappa^3=0 $$
非线性自耦合项，可同时容纳短程汤川解 + 线性增长解（类似标量场孤子/弦解）。

- ✅ **内生性**：禁闭由场自耦合产生，不引入外部源。
- ❌ **代价**：破坏原统一势的**线性叠加原理**——原理论最大优势是四力可直接线性叠加；引入非线性后叠加性消失，四力简单叠加不再成立。

### 2.3 路线取舍台账

| 路线 | 场方程结构 | 禁闭来源 | 优势 | 代价 |
|---|---|---|---|---|
| 路线 1 | 线性非齐次 Proca | 外部源 $S(\boldsymbol r)$ | 形式简单，保留线性 | 源项外部输入，需物理解释 |
| 路线 2 | 非线性 Proca（$\lambda\kappa^3$） | 场自耦合内生 | 禁闭内生，无需外部源 | 丢掉线性叠加，四力叠加结构失效 |

---

## 三、攻坚小结

1. **BOUNDARY B1**：已由解析推导确定其本质——$\nabla\kappa\perp\nabla\tau$ 非恒等式，需附加约束 $\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b=0$ 且 $|\boldsymbol{\nabla}\rho|=|\boldsymbol{\nabla}b|$ 方成立。该项从"未验证（O）"推进为"已解析刻画（约束条件明确，嵌入与否待定）"。
2. **FAIL F1**：两条修复路线均已刻画利弊；路线 1 数学直接可行但源项外部输入（与 L5 的常数输入短板同类），路线 2 内生但破坏叠加。

---

## 四、待选攻坚路线（下一步）

- **A**：继续解析推导约束方程 $\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b=0,\ |\boldsymbol{\nabla}\rho|=|\boldsymbol{\nabla}b|$，把垂直原理场版写成完整几何约束，嵌入 TUFT 场方程。
- **B**：路线 1 完整展开——构造非齐次 Proca 源项，推导带禁闭势的完整场解。
- **C**：路线 2 完整展开——求解非线性 Proca 孤子型禁闭解，评估叠加性破坏的连锁影响。
- **D**：转向 L5 FAIL，尝试从几何约束构造能锁定 $\alpha$ 的方程，解决精细结构常数输入问题。
