# ROOT V134｜核心方程与严格边界（一页审计）

## 统一时空规范：仅 `c=1`

保留 `ℏ,G,ε₀,g_i,m_i`，并严格区分各场强的归一化。

## 1. 可验证的核心几何方程

对 Hermitian 非阿贝尔规范联络：

\[
\boxed{D_\mu=\partial_\mu-i\mathcal A_\mu,\quad
\mathcal F_{\mu\nu}=i[D_\mu,D_\nu]=
\partial_\mu\mathcal A_\nu-\partial_\nu\mathcal A_\mu-i[\mathcal A_\mu,\mathcal A_\nu]}
\]

这已是 Yang–Mills 理论基本定义，不是 ROOT 新定律。

## 2. 两个审计极限

**纯转动标架：** `𝒜=-i(dU)U† ⇒ 𝓕=0`（局部光滑定义）。  
**非零规范曲率：** `𝒜_x=aσ₁/2, 𝒜_y=bσ₂/2 ⇒ 𝓕_xy=abσ₃/2 ≠0`（a,b≠0）。

前者证明几何旋转不等于非零力场，后者展示真正的非阿贝尔自相互作用结构。

## 3. 内部态的动力学闭环

\[
\boxed{S_\text{probe}=-m\int ds+i\hbar\int ds\,z^\dagger(\partial_s-i\mathcal A_\mu u^\mu)z}
\]

在恰当规范固定、归一化与变分条件下，`D_s z=0` 并得到

\[
\boxed{\frac{dQ^a}{ds}+f^a{}_{bc}\mathcal A_s^b Q^c=0,\quad Q^a=z^\dagger T^az}
\]

这是已知 Wong 规范荷输运机制，内部 `SU(2)`/`SU(3)` 表示是**额外加入**的。

## 4. 量子一致性

\[
\boxed{\mathcal A_{SU(3)^3}=\mathcal A_{SU(3)^2Y}=\mathcal A_{SU(2)^2Y}=\mathcal A_{Y^3}=\mathcal A_{\mathrm{grav}^2Y}=0}
\]

并需满足 Witten `SU(2)` 全局异常条件。给定标准模型一代输入，其左手弱双重态为 4 个，满足偶数条件。

## 5. 引力与规范的低能共同作用量骨架

\[
\boxed{S_{\rm EFT}=\frac1{16\pi G}\int\sqrt{-g}\,R\,d^4x
-\sum_i\frac{\hbar}{2g_i^2}\int\sqrt{-g}\,\mathrm{Tr}(\mathcal F_i^{\mu\nu}\mathcal F_{i\mu\nu})\,d^4x
+S_{\rm matter}+S_{\rm Higgs}}
\]

它是已知相对论和标准模型有效场论的组合骨架，**不是完整的量子大统一**。

## 6. 五项无法跳过的 OPEN

1. 从 ROOT 原始公设而不是手工指定，导出非阿贝尔内部规范群。
2. 从几何谱独立导出恰当的手征费米子表示与三代质量。
3. 预测 `g_i, α, ℏ, G` 的来源或至少新的无参数比例。
4. 推导可量子化且与实验相容的引力场动力学。
5. 对至少一项未被拟合的新预言开展独立观测检验。

**审计裁定：已有代数验证通过；没有宣称完成四力统一。**
