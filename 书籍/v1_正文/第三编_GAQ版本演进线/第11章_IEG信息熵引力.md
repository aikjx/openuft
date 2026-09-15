# 第 11 章 IEG 信息熵引力（S04 v3）

> **整合体系**：S04_IEG 信息熵引力（Information-Entropy Gravity，几何信息场、信息熵与引力动力学联系）
> **诚实分级**：部分统一（语言重述成立）/ 待建模（信息场 $\rho_{\mathrm{info}}$ 的非均匀动力学缺失）
> **关键事实**：核心命题"Einstein 方程 ⟺ 信息流守恒"是 Bianchi 恒等式与能量守恒的**同义反复**；信息场 $\rho_{\mathrm{info}}$ 除归一化条件外无独立演化方程；I5–I7 为诠释性命题，无 GR 检验之外的新定量预言。

---

## 11.1 三公理

IEG 体系以三条公设起步，把"引力"重新表述为"几何信息场的流"。

**A1（Einstein ⟺ 信息流）**：引力场方程 $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T_{\mu\nu}$ 等价于几何信息流的守恒律。这一公设是整个体系的支点，但如 11.2 节所析，它在数学上退化为 Bianchi 恒等式的重述。

**A2（几何信息场归一化）**：在时空 4D 流形 $M$ 上定义标量场 $\rho_{\mathrm{info}}$（几何信息密度），满足

$$
\int_M \rho_{\mathrm{info}}\sqrt{-g}\,d^4x = 1 .
$$

这是一条归一化约束，而非动力学方程。它只固定 $\rho_{\mathrm{info}}$ 的"总信息量"为 1，但不约束其时空分布如何演化。

**A3（弱场信息过剩源）**：物质分布以"信息过剩"的方式作为引力源进入弱场方程。原文形式为 $\rho_{\mathrm{info}}^{\mathrm{excess}}=(M/M_p)\,\rho_{\mathrm{info}}^{\mathrm{vac}}$，其中 $\rho_{\mathrm{info}}^{\mathrm{vac}}$ 是真空信息密度（未给出闭式）。

---

## 11.2 核心定理与恒等本质

### 11.2.1 定理 I1（信息-引力等价）

原文给出的核心定理为：

$$
\boxed{G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T_{\mu\nu}\iff\nabla^\mu J_{\mu\nu}^{\mathrm{info}}=0},
\qquad
J_{\mu\nu}^{\mathrm{info}}\equiv -\frac{1}{8\pi G}G_{\mu\nu}+\frac{1}{2}T_{\mu\nu} .
$$

**诚实审查**：$J_{\mu\nu}^{\mathrm{info}}$ 是把场方程两端按固定系数做线性组合而定义出来的张量。对其求散度：

$$
\nabla^\mu J_{\mu\nu}^{\mathrm{info}}=-\frac{1}{8\pi G}\underbrace{\nabla^\mu G_{\mu\nu}}_{=0\;(\text{Bianchi})}+\frac{1}{2}\underbrace{\nabla^\mu T_{\mu\nu}}_{=0\;(\text{能量守恒})}\equiv 0 .
$$

两步代入即得。这并不是"从信息论导出了 Einstein 方程"，而是把 Einstein 方程两端（它们的散度本来就都为零）重新打包命名为"信息流"。等价方向 $\Leftarrow$ 也只说明：若散度为零，则场方程成立——但前提仍是先有 $G_{\mu\nu}$ 与 $T_{\mu\nu}$ 这两个场量。**结论：I1 是 Bianchi 恒等式 + 能量守恒的同义反复，不包含 GR 之外的新物理。**

### 11.2.2 定理 I2（最大信息熵作用量）

IEG 构造的总作用量为

$$
S_{\mathrm{IEG}}=S_{\mathrm{EH}}-\frac{1}{2}\int_M \nabla_\mu\rho_{\mathrm{info}}\,\nabla^\mu\rho_{\mathrm{info}}\sqrt{-g}\,d^4x ,
$$

即在 Einstein-Hilbert 作用量上叠加一个梯度惩罚项。对度规变分给出：

$$
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T_{\mu\nu}+\nabla_\mu\rho_{\mathrm{info}}\nabla_\nu\rho_{\mathrm{info}}-\frac{1}{2}g_{\mu\nu}(\nabla\rho_{\mathrm{info}})^2 .
$$

**关键点**：右端多出的项 $(\nabla\rho\otimes\nabla\rho-\tfrac12 g(\nabla\rho)^2)$ 正比于 $(\nabla\rho)^2$。当且仅当 $\rho_{\mathrm{info}}=\mathrm{const}$（均匀信息场）时，附加项恒为零，理论才退回标准 Einstein 方程。一旦 $\rho_{\mathrm{info}}$ 在空间中起伏，就必须额外提供 $\rho_{\mathrm{info}}$ 的演化方程——而 A2 只给了归一化，**未给动力学**。因此 I2 在非均匀情形下是"欠定"的：多了一个场 $\rho$ 却没有约束它的方程，无新解可言。

### 11.2.4 与 Verlinde/Jacobson 路线的区分

读者可能会问：IEG 与近年来的"熵引力"路线（Verlinde 2010 的熵力引力、Jacobson 1995 的热力学推导 Einstein 方程）有何不同？必须指出：Jacobson 是从 Rindler 视界的热力学第一定律出发，在局部双曲面 $\dot a=0$ 假设下导出 Einstein 方程，这是一个**带额外几何假设**的推导；Verlinde 是从全息屏上的熵变 $\Delta S=2\pi k_B \Delta x/\lambda$ 导出 Newton 引力。IEG 的 I1 **比这两者都弱**——它连 Rindler 视界、全息屏、熵变梯度都未引入，只把场方程两端打包命名为"信息流"。因此 IEG 在"引力是否由信息论导出"这一问题上的立场，比 Verlinde/Jacobson 还要弱一档：它甚至没有尝试从信息熵的微观自由度出发，只在宏观场方程层做了词汇替换。这一区分必须诚实写出，以免读者误以为 IEG 完成了 Verlinde 路线尚未完成的工作。

### 11.2.5 定理 I3（弱场信息梯度）

弱场近似 $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}$，取 $h_{\mu\nu}\propto-\nabla_\mu\nabla_\nu\phi$，原文给出

$$
\nabla^2\phi=4\pi G\rho_M-\rho_{\mathrm{info}}^{\mathrm{excess}} .
$$

右端第二项"信息过剩源"在原文中按 I4 被赋值为 $(M/M_p)\rho_{\mathrm{info}}^{\mathrm{vac}}$，但 $\rho_{\mathrm{info}}^{\mathrm{vac}}$ 未给定标。**诚实标注**：在 $\rho_{\mathrm{info}}^{\mathrm{excess}}=0$ 时上式就是标准 Poisson 方程；修正项无独立数值，因此 I3 不构成对牛顿引力的可检验修正。

---

## 11.3 元数据表（五字段）

| 符号 | 定义 | 来源方程 | 量纲（自然单位 $\hbar=c=1$） | 数值/闭式 | 验证状态 + 出处 |
|---|---|---|---|---|---|
| $\rho_{\mathrm{info}}$ | 几何信息密度标量场 | A2 | $\ell^{-4}$ | 满足 $\int\rho\sqrt{-g}\,d^4x=1$，时空分布未定 | **待建模**：无独立演化方程；source_chapter §1.2 |
| $J_{\mu\nu}^{\mathrm{info}}$ | 信息流张量 | I1 | $\ell^{-2}$ | $-G_{\mu\nu}/(8\pi G)+T_{\mu\nu}/2$ | 结构已证（定义恒等），Bianchi+能量守恒，source_chapter §1.3 |
| $\rho_{\mathrm{info}}^{\mathrm{excess}}$ | 信息过剩源 | A3/I3 | $\ell^{-2}$ | $(M/M_p)\rho_{\mathrm{info}}^{\mathrm{vac}}$，$\rho_{\mathrm{info}}^{\mathrm{vac}}$ 未定义 | **待建模**：无定标；source_chapter §1.4 |
| $S_{\mathrm{IEG}}$ | IEG 总作用量 | I2 | $\ell^0$ | $S_{\mathrm{EH}}-\tfrac12\int(\nabla\rho)^2\sqrt{-g}\,d^4x$ | 形式已写；非均匀动力学缺失 |
| $\mathcal S_{\mathrm{geo}}$ | 几何信息熵密度 | 定义 1 | $\ell^{-2}$ | $-\tfrac12 g^{\mu\nu}\nabla_\mu\rho\nabla_\nu\rho+R/(8\pi G)$ | 形式定义；未用于独立预言 |

---

## 11.4 诠释性命题 I5–I7

原文在 §1.5 列出三条"预言"：

- **I5**：引力波是"信息熵的振荡模式"，波形写成 $h_{\mu\nu}=A_{\mu\nu}e^{iS_{\mathrm{info}}/\hbar}$。
- **I6**：引力坍缩是"信息熵坍缩"，黑洞是信息饱和态。
- **I7**：宇宙加速膨胀是"信息熵梯度反转"，$\Lambda$ 是"信息反转能"。

**诚实标注**：这三条都是**诠释性命题**，把已知现象（引力波、坍缩、$\Lambda$CDM 加速）换一套词汇重说一遍。它们不给出任何新的频率、振幅、红移关系，也不给出 $\Lambda$ 的数值。原文 §1.4 精算表中"I1：$S_{\mathrm{BH}}=S_{\mathrm{info}}^{\max}$，预测 ✓ 实验 ✓ 误差 0"一行，**实为引用 Bekenstein-Hawking 熵公式 $S_{\mathrm{BH}}=k_BA/(4L_p^2)$，并非 IEG 自己的预言**——Bekenstein 1973、Hawking 1975 已先于此体系。

进一步说，I5 把引力波写成 $h_{\mu\nu}=A_{\mu\nu}e^{iS_{\mathrm{info}}/\hbar}$，这只是把 GR 平面波解中的相位 $\omega t-kx$ 替换为 $S_{\mathrm{info}}/\hbar$；若 $S_{\mathrm{info}}=\hbar(\omega t-kx)$，则上式与 GR 平面波完全相同，无新内容。I7 把宇宙学常数 $\Lambda$ 称为"信息反转能"，但未给出 $\Lambda\sim 10^{-52}\ \mathrm{m}^{-2}$ 这一数值的任何估算路径。I6 的"黑洞是信息饱和态"是对 Bekenstein-Hawking 熵极限的语言重述，未涉及黑洞信息悖论（page curve、Hawking 辐射纠缠）的任何新解。

---

## 11.5 与 S03（v1）的关系

S03 母本的 A5（$M=M_p N$）把"信息"操作化为离散元胞计数 $N$。S04 本应在此之上展开"信息如何驱动引力"，但实际上 I1 的证明只用到 Bianchi 恒等式与能量守恒，**完全没有用到 $N$ 或离散性**。这意味着 S04 与 S03 的母本关系在定理层是悬空的：S03 提供的"元胞计数"入口在 S04 中并未真正参与推导。S07（第 14 章）后来把 S04 的 IEG 拼接到 v4 组合候选中，但拼接点仅为"$G_{\mu\nu}=$ 信息流"这一恒等式识别（V4），上游结论不自动转移。

---

## 11.6 诚实边界与待研究问题

**必须明确写出的边界**：

1. **不可写成"引力已由信息论导出"**。I1 的等价方向 $\nabla^\mu J_{\mu\nu}^{\mathrm{info}}=0$ 是 Bianchi 恒等式的同义反复，不是第一性推导。
2. **$\rho_{\mathrm{info}}$ 没有动力学**。A2 只是归一化积分，不构成场方程；I2 多出的梯度项在非均匀情形下无新解。
3. **黑洞信息饱和态引用 Bekenstein-Hawking 属引用而非新预言**。
4. **claims.csv 空、无验证脚本入库**：本体系 `07_计算复现/` 与 `claims.csv` 仅有表头，原文 §1.4 精算表中的"误差 0"无脚本可复核。
5. **I5–I7 无定量新预言**：引力波=信息熵振荡、坍缩=信息熵坍缩、加速=信息梯度反转，全部为诠释性命题。

**待研究问题**：

- $\rho_{\mathrm{info}}$ 是否能被赋予一个真正的运动方程（例如与 Ricci scalar 的耦合 $R=8\pi G\,\rho_{\mathrm{info}}$）？若不能，IEG 仅为语言重述。
- 非均匀 $\rho_{\mathrm{info}}$ 情形下，附加项 $(\nabla\rho\otimes\nabla\rho-\tfrac12 g(\nabla\rho)^2)$ 是否会给出可观测的弱场修正（例如偏离 GR 的后牛顿参数 $\gamma,\beta$）？
- $\rho_{\mathrm{info}}^{\mathrm{vac}}$ 的真空信息密度是否可由宇宙学常数 $\Lambda$ 反定标，还是反过来？
- IEG 与 Verlinde 熵引力、Jacobson 热力学引力的关系需另行审查——本体系目前未与这些已有路线做严格对照。

---

## 11.7 本章小结

IEG 用"信息"这一词汇重新包装了 Einstein 方程与 Bianchi 恒等式。它的公设清晰、数学推导正确，但推导步数几乎为零——核心定理 I1 是定义性打包，I2 在 $\rho=\mathrm{const}$ 时退回 GR，I3 的修正项无定标。作为 GAQ 版本线 v3 的三子系统之一，它在 v4 中被拼接为"$G_{\mu\nu}=$ 信息流"的口号，但这一拼接不带来 GR 之外的新预言。读者应把本章读作"一个用信息论语言重述 GR 的候选框架"，而非"引力已被信息论导出"的成果章。
