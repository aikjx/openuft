# 延伸方向 B｜最小耦合原理：\(\partial_\mu\to D_\mu\) 的求导证明与本体论

> 全程严格区分 **数学定义 / 量纲分析 / 本体论解释**；SI 单位制；签名 \((+,-,-,-)\)。
> 本文全部结论由 `verify_extension_derivation.py` 的 **B 组**符号求导复算（见文末 B.9）。

---

## B.0 问题：为什么偏导数"不够用"

设物质场 \(\psi(x)\)（复标量场或旋量场），考虑**全局** \(U(1)\) 变换（SI 下相位带 \(\hbar\)）：

\[
\psi(x)\;\longrightarrow\;e^{i q\alpha/\hbar}\,\psi(x),\qquad \alpha=\text{常数}
\]

对 \(x^\mu\) 求导：

\[
\partial_\mu\big(e^{iq\alpha/\hbar}\psi\big)=e^{iq\alpha/\hbar}\,\partial_\mu\psi
\]

**偏导数与变换对易 ⇒ 协变**，含 \(|\partial_\mu\psi|^2\) 的动能项（如 \(\hbar^2\partial_\mu\psi^\ast\partial^\mu\psi\)）不变。

但若把对称性**局域化**，\(\alpha\to\alpha(x)\)：

\[
\partial_\mu\big(e^{iq\alpha(x)/\hbar}\psi\big)
=e^{iq\alpha/\hbar}\Big[\partial_\mu\psi+\frac{iq}{\hbar}\big(\partial_\mu\alpha\big)\psi\Big]
\]

**多出 \(\frac{iq}{\hbar}(\partial_\mu\alpha)\psi\) 项 ⇒ 偏导数不再协变**，动能项不再不变。

**这是本专题任务 1 中"基矢随位置变化 ⇒ 需要联络"的完全同构**：
- GR：基矢随位置变 ⇒ 引入 \(\Gamma\)（时空联络）；
- 规范理论：内部相位随位置变 ⇒ 引入 \(A_\mu\)（内部联络）。

两者的**数学结构一致**，但**本体论不同**（见 B.7）。

---

## B.1 规范协变导数的定义

**定义（数学层，SI 制）**：

\[
\boxed{D_\mu\equiv\partial_\mu-\frac{i q}{\hbar}A_\mu}
\]

其中 \(q\) 为粒子的电荷（含符号），\(A_\mu\) 为 4 势。

**规范变换（约定 B-1）**：

\[
A_\mu\;\longrightarrow\;A_\mu-\partial_\mu\lambda,\qquad
\psi\;\longrightarrow\;e^{-iq\lambda/\hbar}\,\psi
\]

**量纲核验（必要前提）**：

\[
[D_\mu]=[\partial_\mu]=\mathrm{L}^{-1},\qquad
\Big[\frac{q}{\hbar}A_\mu\Big]
=\frac{\mathrm{I}\,\mathrm{T}}{\mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-1}}\cdot
\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-2}\mathrm{I}^{-1}
=\mathrm{L}^{-1}\;\checkmark
\]

\[
\Big[\frac{q\lambda}{\hbar}\Big]
=\frac{\mathrm{I}\,\mathrm{T}\cdot\mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-2}\mathrm{I}^{-1}}
{\mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-1}}=1\;\checkmark\quad(\text{相位无量纲})
\]

（脚本 B5、B7。）

---

## B.2 规范协变性的求导证明

**目标**：证明 \(D'_\mu\psi'=e^{-iq\lambda/\hbar}\,D_\mu\psi\)（协变 = 与变换对易）。

**左端展开**（\(\theta\equiv q\lambda/\hbar\)）：

\[
\begin{aligned}
D'_\mu\psi'
&=\Big(\partial_\mu-\frac{iq}{\hbar}(A_\mu-\partial_\mu\lambda)\Big)\big(e^{-i\theta}\psi\big)\\[4pt]
&=e^{-i\theta}\Big[-\frac{iq}{\hbar}(\partial_\mu\lambda)\psi+\partial_\mu\psi\Big]
-\frac{iq}{\hbar}A_\mu e^{-i\theta}\psi+\frac{iq}{\hbar}(\partial_\mu\lambda)e^{-i\theta}\psi\\[4pt]
&=e^{-i\theta}\Big[\partial_\mu\psi-\frac{iq}{\hbar}A_\mu\psi\Big]\\[4pt]
&=e^{-iq\lambda/\hbar}\,D_\mu\psi
\end{aligned}
\]

**关键点**：由 \(\partial_\mu\) 作用到相位上产生的项 \(-\frac{iq}{\hbar}(\partial_\mu\lambda)\psi\)，
与由 \(A_\mu\to A_\mu-\partial_\mu\lambda\) 产生的项 \(+\frac{iq}{\hbar}(\partial_\mu\lambda)\psi\) **精确相消**。
这就是"联络按非齐次方式变换"的全部作用。

脚本 B1 对 \(\mu=0,1,2,3\) 四个分量符号展开验证恒等（PASS）。

---

## B.3 两套约定及其配对规则（重要）

文献中存在两套等效约定，**符号与相位因子必须成对使用**：

| 约定 | 协变导数 | 规范场变换 | 物质场变换 |
|---|---|---|---|
| **B-1（本文）** | \(D_\mu=\partial_\mu-\dfrac{iq}{\hbar}A_\mu\) | \(A_\mu\to A_\mu-\partial_\mu\lambda\) | \(\psi\to e^{-iq\lambda/\hbar}\psi\) |
| **B-2（Peskin 型）** | \(D_\mu=\partial_\mu+\dfrac{iq}{\hbar}A_\mu\) | \(A_\mu\to A_\mu-\partial_\mu\lambda\) | \(\psi\to e^{+iq\lambda/\hbar}\psi\) |

两套均由脚本符号验证（B1、B2 均 PASS）。二者关系为 \(q\to-q\)（或等价地 \(A_\mu\to-A_\mu\)）。

> **审计项 A9（登记于 `../量纲审计与修正清单.md`）**：专题任务 4 给出 \(\boldsymbol{A}\to\boldsymbol{A}+\nabla\lambda,\ \phi\to\phi-\partial_t\lambda\)
> （等价于 \(A_\mu\to A_\mu-\partial_\mu\lambda\)），但未给出物质场 \(\psi\) 的相位因子；
> 任务 5 给出 \(D_\mu=\partial_\mu-i\frac{q}{\hbar}A_\mu\)。
> 两者**单独都正确，但合起来不构成完整约定对**——必须补上 \(\psi\to e^{-iq\lambda/\hbar}\psi\)（本文 B-1）才是自洽的一套。
> 这属于"表述不完整"，不是量纲错误，与 A1–A8 的实质缺陷分级不同。

---

## B.4 对易子即场强：\([D_\mu,D_\nu]=-\dfrac{iq}{\hbar}F_{\mu\nu}\)

直接对 \(\psi\) 作用（脚本 B3 抽样 3 组 PASS）：

\[
\begin{aligned}
D_\mu D_\nu\psi
&=\Big(\partial_\mu-\frac{iq}{\hbar}A_\mu\Big)\Big(\partial_\nu\psi-\frac{iq}{\hbar}A_\nu\psi\Big)\\[4pt]
&=\partial_\mu\partial_\nu\psi-\frac{iq}{\hbar}\big[(\partial_\mu A_\nu)\psi+A_\nu\partial_\mu\psi+A_\mu\partial_\nu\psi\big]
+\Big(\frac{iq}{\hbar}\Big)^2A_\mu A_\nu\psi
\end{aligned}
\]

交换 \(\mu\leftrightarrow\nu\) 相减：一阶导项与 \(A_\mu A_\nu\) 项（对称）全部相消，只剩

\[
\boxed{[D_\mu,D_\nu]\psi=-\frac{iq}{\hbar}\big(\partial_\mu A_\nu-\partial_\nu A_\mu\big)\psi
=-\frac{iq}{\hbar}F_{\mu\nu}\psi}
\]

**数学意义**：规范场强 \(F_{\mu\nu}\) 就是**规范协变导数的曲率**（与任务 1 中 \([\nabla_\mu,\nabla_\nu]V^\rho=R^\rho_{\ \sigma\mu\nu}V^\sigma\) 逐字同构）。

**量纲核验**：\([[D_\mu,D_\nu]]=\mathrm{L}^{-2}\)；右端 \(\frac{q}{\hbar}F_{\mu\nu}\)：
\(\frac{\mathrm{I}\,\mathrm{T}}{\mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-1}}\cdot\mathrm{M}\,\mathrm{T}^{-2}\mathrm{I}^{-1}=\mathrm{L}^{-2}\) ✔

---

## B.5 最小耦合 = 动量平移 \(p_\mu\to p_\mu-qA_\mu\)

把 \(D_\mu\) 乘以 \(-i\hbar\)（即把"导数语言"翻成"算符语言"）：

\[
-i\hbar D_\mu
=-i\hbar\Big(\partial_\mu-\frac{iq}{\hbar}A_\mu\Big)
=-i\hbar\partial_\mu\;-\;qA_\mu
\]

（其中 \((-i\hbar)\cdot\left(-i\frac{q}{\hbar}A_\mu\right)=(-i)(-i)\,\frac{\hbar q}{\hbar}A_\mu=i^2\,qA_\mu=-qA_\mu\)；脚本 B4 四分量符号验证 PASS。）

\[
\boxed{p_\mu\equiv-i\hbar\partial_\mu\;\longrightarrow\;p_\mu-qA_\mu}
\]

**这是"最小耦合替换 \(\partial_\mu\to D_\mu\)"的物理内容**：带电粒子的正则动量被规范势平移。

**量纲核验（关键）**：

\[
[\hbar\partial_\mu]=\mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-1}\cdot\mathrm{L}^{-1}=\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-1}
\]

\[
[qA_\mu]=\mathrm{I}\,\mathrm{T}\cdot\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-2}\mathrm{I}^{-1}=\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-1}\;\checkmark
\]

两侧量纲严格一致（脚本 B6）。**注意**：\(D_\mu\) 中出现 \(\frac{1}{\hbar}\) 是为了让 \(D_\mu\) 与 \(\partial_\mu\) 同量纲；乘上外层的 \(\hbar\) 后，\(\hbar\) 完全消去，因此"最小耦合"**不需要任何额外的 \(\hbar\) 因子**——这也侧面印证了专题任务 5 中 \(D_\mu=\partial_\mu-i\frac{q}{\hbar}A_\mu\) 的形式（而非漏写 \(\hbar\) 的 \(\partial_\mu-iqA_\mu\)）是正确的。

---

## B.6 规范不变的作用量（一步到位的构造）

自由复标量场（Klein–Gordon）拉氏量密度：

\[
\mathcal{L}_0=\hbar^2(\partial_\mu\psi)^\ast(\partial^\mu\psi)-m^2c^2|\psi|^2
\]

**最小耦合替换** \(\partial_\mu\to D_\mu\)：

\[
\boxed{\mathcal{L}=\hbar^2(D_\mu\psi)^\ast(D^\mu\psi)-m^2c^2|\psi|^2}
\]

由于 \(D_\mu\psi\) 与 \(\psi\) 按**同一相位**变换（B.2），\(|(D_\mu\psi)|^2\) 严格不变 ⇒ 作用量局域 \(U(1)\) 不变。

展开后自动出现相互作用项（含 \(A_\mu\) 与 \(A_\mu A^\mu\) 项）——**"力"从"对称性要求"中涌现**，这是规范原理的核心。

---

## B.7 本体论定位

| 层次 | GR 协变导数 \(\nabla_\mu\) | 规范协变导数 \(D_\mu\) |
|---|---|---|
| 联络 | \(\Gamma^\rho_{\mu\nu}\)（由度规 \(g_{\mu\nu}\) 决定） | \(A_\mu\)（独立动力学场，不由度规决定） |
| 平行移动的对象 | 时空切空间中的矢量 | 内部 \(U(1)\) 纤维上的相位 |
| 曲率 | \(R^\rho_{\ \sigma\mu\nu}\) = **时空弯曲** = 引力 | \(F_{\mu\nu}\) = **内部空间曲率** = 电磁力 |
| 本体论 | 外部时空的几何性质 | 抽象内部自由度空间的几何性质 |
| 是否改变时空 | 是（引力即几何） | **否**（电磁不改变时空几何本身） |

> **一句话**：\(\nabla_\mu\) 描述"在弯曲时空中如何比较不同点的矢量"；\(D_\mu\) 描述"在不同点如何比较内部相位"。
> 二者数学同构（联络 + 不对易 ⇒ 曲率），但**曲率承载的物理完全不同**——这是本专题任务 5 结论的深化。

**可检验差别**：引力是"universal"（所有物体同加速度，与 \(q\) 无关的等效原理）；电磁力正比于 \(q\)，不同电荷加速度不同。这一条把"几何"与"内部规范"彻底区分开。

---

## B.8 物理边界（严格标注）

1. **本文只做阿贝尔 \(U(1)\)**。非阿贝尔推广（\(SU(N)\)）：\(D_\mu=\partial_\mu-i\frac{g}{\hbar}A^a_\mu T^a\)，场强
   \(F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+\frac{g}{\hbar}f^{abc}A^b_\mu A^c_\nu\) **多出自相互作用项**（结构常数项）——这是 Yang–Mills 与电磁的本质区别（规范玻色子自相互作用）。本文不含此项。
2. **"最小耦合"不是唯一可能的耦合**：Pauli 项 \(\propto\bar\psi\sigma^{\mu\nu}\psi F_{\mu\nu}\) 等非最小耦合原则上允许，受实验约束（如反常磁矩）。最小耦合是"最低阶、重整化最简"的选择，**不是纯逻辑必然**。
3. **引力中的类比有限**：把 \(\partial\to\nabla\) 叫"引力最小耦合"，但引力耦合常数是 \(G\)（有量纲，导致不可重整），与规范耦合 \(q\)（无量纲化的 \(\sqrt{\alpha}\)）性质不同。
4. **规范势 \(A_\mu\) 的可观测性**：在量子层面 \(A_\mu\) 本身有可观测效应（Aharonov–Bohm 效应），因此不能简单说"势只是数学工具"——但经典层面只有 \(F_{\mu\nu}\) 可观测量（规范不变量）。

---

## B.9 精算结论（脚本 B 组，符号求导复算）

| 条目 | 核验内容 | 结论 |
|---|---|---|
| B1 | 约定 B-1 规范协变（4 个分量符号展开） | PASS |
| B2 | 约定 B-2 规范协变（4 个分量符号展开） | PASS |
| B3 | \([D_\mu,D_\nu]\psi=-\frac{iq}{\hbar}F_{\mu\nu}\psi\)（抽样 3 组） | PASS |
| B4 | \(-i\hbar D_\mu=-i\hbar\partial_\mu-qA_\mu\)（4 个分量） | PASS |
| B5 | \([q\lambda/\hbar]=1\) | PASS |
| B6 | \([\hbar\partial_\mu]=[qA_\mu]=\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-1}\) | PASS |
| B7 | \([\frac{q}{\hbar}A_\mu]=\mathrm{L}^{-1}=[\partial_\mu]\) | PASS |
| B8 | 约定配对边界（登记审计项 A9） | BOUNDARY |

**复跑方式**：

```
cd 02_共享基础/推导与量纲专题/延伸方向
python -B verify_extension_derivation.py
```
