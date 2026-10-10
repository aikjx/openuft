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
$$ \boldsymbol{\nabla}\kappa\cdot\boldsymbol{\nabla}\tau =\frac{1}{(\rho^2+b^2)^4}\Big[ 2\rho b(\rho^2-b^2)\big(|\boldsymbol{\nabla}\rho|^2-|\boldsymbol{\nabla}b|^2\big)+\big(-\rho^4+6\rho^2b^2-b^4\big)\boldsymbol{\nabla}\rho\cdot\boldsymbol{\nabla}b \Big] $$

> **⚠ 勘误（2026-10-10，独立复算逮获）**：上式第一项原整理稿写为 $(|\boldsymbol{\nabla}b|^2-|\boldsymbol{\nabla}\rho|^2)$，**整体符号反了**，正确为 $(|\boldsymbol{\nabla}\rho|^2-|\boldsymbol{\nabla}b|^2)$。精确分数定点（$\rho=1,b=4,\nabla\rho=(1,0),\nabla b=(0,4)$）真值 $+0.021551$，原式给 $-0.021551$，修正式给 $+0.021551$；随机光滑场修正残差 $6.9\times10^{-17}$、原式残差 $0.039$。交叉项系数 $-\rho^4+6\rho^2b^2-b^4$ 正确。**关键：正交零条件不变**（仍要求两项各自为零 ⟹ $|\nabla\rho|=|\nabla b|$ 与 $\nabla\rho\cdot\nabla b=0$），故路线 A 的柯西-黎曼闭合及全部后续结论不受影响。凭证：[母本紧凑式_独立复算核验.py](./母本紧凑式_独立复算核验.py)。

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

---

## 五、四选项推进结果回填（攻坚链闭环，2026-10-10）

本母本提出的 A/B/C/D 已在后续算法联盟/openuft 攻坚中逐一处置：

| 选项 | 处置 | 结果 | 文档 |
|---|---|---|---|
| **A** | 已完成 | B1 闭合：约束 ⟺ 位形复场 $W=\rho+ib$ 全纯（柯西-黎曼），解析+数值双证，$\Xi=1/W^{*}$ 与 L1-7 对偶反演闭环 | [垂直原理场版闭合_柯西黎曼嵌入](./四力统一_攻坚_垂直原理场版闭合_柯西黎曼嵌入.md) |
| **B** | 已完成（深化） | 非齐次源 $S=2\sigma/r-\mu^2\sigma r$ 残差 0；但朴素塞入破坏 CR，兼容修复为禁闭由解析函数**模** $|\Xi|=\sigma r$ 承载 | [F1禁闭势修复_非齐次Proca与解析性兼容](./四力统一_攻坚_F1禁闭势修复_非齐次Proca与解析性兼容.md) |
| **C** | 未单独展开（被更优路径覆盖） | 非线性 $\lambda\kappa^3$ 破坏线性叠加的代价仍登记在案；其"内生禁闭"诉求由全纯模/通量管路线（E2/E2-a）更优回应，无需另起非线性 Proca | 见三难闸门 §4 与 E2/E2-a |
| **D** | 已完成（证否型） | 全 $\alpha\in[10^{-3},137]$ 扫描恒等式残差 ~1e-16，纯几何严格不能锁定 $\alpha$；F2/F3/F4 应作 EFT 外部输入登记 | [L5_alpha第一性导出_否定结论](./四力统一_攻坚_L5_alpha第一性导出_否定结论.md) |

**由 B 继续深入产生的禁闭链**（母本未列、后续新增）：
1. [全局有质量解析解族_两尺度统一](./四力统一_攻坚_全局有质量解析解族_两尺度统一.md)——$\Phi=qe^{-\mu r}/r+\sigma r$ 两尺度共存。
2. [算法联盟_全局全纯禁闭构造_三难禁阻闸门](./算法联盟_全局全纯禁闭构造_三难禁阻闸门.md)——证明「全纯+径向各向同性+线性」三难不相容（$\nabla^2r=1/r$）。
3. [算法联盟_E2各向异性通量管全纯解_G4有条件逃生](./算法联盟_E2各向异性通量管全纯解_G4有条件逃生.md)——$f=ze^{az}$ 保 CR，沿轴线性、横向受限。
4. [算法联盟_E2a_通量管轴自发方向_G4正式过闸](./算法联盟_E2a_通量管轴自发方向_G4正式过闸.md)——旋转不变母泛函 $E=\sigma L$ 变分自发选轴，G4 运动学层面通过；螺旋作用量→NG 能量动力学桥仍开放。

收口总览：[12_研究结论/四力统一验证_结论与评级汇总](../12_研究结论/四力统一验证_结论与评级汇总.md) · 论文 [Discussion_局限与展望](../13_论文与成果/总结/TUFT四力统一_Discussion_局限与展望.md)。
