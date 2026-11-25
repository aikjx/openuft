# ROOT V143｜从光速螺旋到几何规范场：完整可复算数学审计

> 科学状态：已有 Kaluza–Klein (KK) 理论的**明确候选扩展路线与限制审计**，不是 ROOT 四力统一的证明。文中的新结果指本研究工作流中新完成的复算及反例检查，不声称首创 KK 机制。
>
> 单位：**只采用 c=1；绝不再令 ℏ=1 或 G=1。** 以长度 L 与质量 M 为基本量：`[ℏ]=M·L`、`[G4]=L/M`、`[G5]=L²/M`。

## 1. 研究问题和前提

V142 已证明光滑的 `SO(3)` 纯旋转标架 `Ω=R^-1dR` 满足 `dΩ+Ω∧Ω=0`，因此单独旋转不自动产生真实规范场。V143 转而检查：**把闭环方向解释为独立内部坐标，能否通过几何动态产生 U(1) 规范场的二次传播作用量？**

必须强调：假设多出一个内部圆 `S¹` 是新增的物理假设，而非从三方向正交自动推导出的事实。五维的零间隔条件不是说已经发现了五维光子；也不证明四维光会沿螺旋空间路径运动。

## 2. 五维光速运动与四维螺旋的严格关系

取五维平直圆纤维几何（无连接时）：

\[
 ds_5^2=-dt^2+dx^2+dy^2+dz^2+R^2 d\phi^2,
 \qquad \phi\sim\phi+2\pi.
\]

定义轨迹：

\[
(x,y,z,\phi)=(a\cos\omega t,a\sin\omega t,ut,\Omega t).
\]

若 `ds5²=0`，则：

\[
 \boxed{a^2\omega^2+u^2+R^2\Omega^2=1.}
\]

对四维投影求导，得到 `v₃²=a²ω²+u²`。Frenet–Serret 曲率、挠率（`v₃>0`）为：

\[
 \kappa=\frac{a\omega^2}{v_3^2},\quad
 \tau=\frac{u\omega}{v_3^2},\quad
 \boxed{v_3^2(\kappa^2+\tau^2)=\omega^2.}
\]

这修正了先前依赖 `v3=1` 的等式；当 `RΩ≠0` 时，不能同时强行要求 `a²ω²+u²=1`。例子：`a=0.3 L`，`ω=1/L`，`u=0.8`，`R=2L`，`Ω=√0.27/(2L)`；`v3=√0.73=0.854400...`，`κ=0.3/0.73=0.4109589/L`，`τ=0.8/0.73=1.0958904/L`。

这里的 `κ,τ` 是三维**轨迹**的几何量，仍然不是时空联络挠率。

## 3. 从内部闭环导出 U(1) 规范连接（已有的 KK 构造）

假设五维度规

\[
 \boxed{ds_5^2=g_{\mu\nu}(x)dx^\mu dx^\nu+R^2\left(d\phi+kA_\mu(x)dx^\mu\right)^2}.\tag{1}
\]

其中 `R` 是常量背景内部半径，`k` 是无量纲规范化常数，`[Aμ]=L^-1`。定义一形式 `η=dφ+kA`。在纤维坐标变换

\[
\phi'=\phi-k\chi(x),\qquad A'_\mu=A_\mu+\partial_\mu\chi
\]

下 `η'=η`，即四维 U(1) 规范变换来自内部坐标变换。由于 `A` 是**独立的度规分量**，不是 `R(x)^-1 ∂R(x)` 的纯旋转联络，它允许非零场强：

\[
F=dA,\quad F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu.
\]

这说明**几何本身可以携带 U(1) 规范场**，但它不是从三维曲率/挠率被唯一推出的，也不是将四力全部统一。

## 4. 五维引力作用量如何产生四维 Maxwell 动力学

令 

\[
 S_5=\frac{1}{16\pi G_5}\int d^4x\,d\phi\,R\sqrt{-g_4}\,\mathcal R_5,
\quad G_4=\frac{G_5}{2\pi R}.
\]

在常量 R、无纤维依赖、忽略边界项的**受限几何**下，标准 KK 恒等式为：

\[
\mathcal R_5=\mathcal R_4-\frac{k^2R^2}{4}F_{\mu\nu}F^{\mu\nu}.
\]

于是

\[
\boxed{S_{4,\mathrm{restricted}}=\int d^4x\sqrt{-g_4}
\left[\frac{\mathcal R_4}{16\pi G_4}-\frac{k^2R^2}{64\pi G_4}F_{\mu\nu}F^{\mu\nu}\right].}\tag{2}
\]

这一次 Maxwell 的**二次传播项真实存在**，修复了 V140–V142 的复合二形式模型在常量场附近缺乏二次项的问题。但代价是引入了一个新的五维度规自由度 `Aμ`，不算从螺旋独立推导的结果。

我们用**独立的五维 Christoffel–Ricci 符号计算**验证一个非平凡特例：四维平直背景，`A_y=Bx`，其余 `A=0`。有 `F_xy=B`、`F²=2B²`，计算全五维 Ricci 标量得到：

\[
 \boxed{\mathcal R_5=-\frac12 R^2k^2B^2}
\]

与 (2) 的预测完全一致，符号差为严格的零。这是对特例的独立符号交叉验证，不是对任意背景全部公式的计算机形式化证明。

### 规范耦合与量纲

将四维规范场写为 `S_A=-ℏ/(4g²) ∫√−g F²`，对比 (2)：

\[
 \boxed{g^2=\frac{16\pi G_4\hbar}{R^2k^2}}.\tag{3}
\]

量纲：`G4ℏ~L²`、`R²~L²`，`g` 无量纲。\(\hbar\) 和 \(G_4\) 始终保持独立量纲，绝不设置为 1。

### 两个光子偏振

规范场 `Aμ` 具有 Maxwell 约束和规范冗余，在线性真空中只含两个横向物理偏振。程序对一般 `Ax=a cos[ω(t−z)]`、`Ay=b sin[ω(t−z)]` 逐项验证 `∂μ F^{μν}=0` 和 Bianchi 恒等式。在这一例子中两种振幅 `a,b` 独立，验证的是 Maxwell 理论的已知解，不是从微观螺旋得到的额外预测。

## 5. 新的致命一致性检查：半径标量不能随意冻结

真正的 KK 降维包含圆半径 \(\rho(x)\) 这一额外标量（radion/dilaton）。在 Jordan frame 忽略边界项，五维 Einstein–Hilbert 作用量的相关部分为：

\[
 S\propto\int d^4x\sqrt{-g}\left[\rho\mathcal R_4-\frac{k^2\rho^3}{4}F^2\right].
\]

对 \(\rho\) 变分：

\[
 \boxed{\mathcal R_4-\frac{3k^2\rho^2}{4}F^2=0.}\tag{4}
\]

而在**没有其他物质、宇宙常数或额外稳定化势**且设 \(\rho\) 为常数时，四维度规方程的迹给出 `R4=0`（Maxwell 能量动量张量无迹）。故 (4) 强制

\[
\boxed{F_{\mu\nu}F^{\mu\nu}=0.}\tag{5}
\]

所以在这一极简的五维真空模型中，随意将 `R` 固定，再声称获得任意真空 Maxwell 场，是**不一致的截断**；通常静态纯磁场 `F²>0` 并不满足 (5)。要避免这一限制，需要引入合适的半径动力学与稳定化/其他源，并独立验证它们的方程。

本轮符号程序直接验证了半径变分公式 (4)，没有把稳定化问题假装成已解决。

## 6. 内部闭环产生质量和电荷，随后暴露重大数值矛盾

对无质量五维自由标量模态（为了明确推导，不是电子自旋场）：

\[
\Phi(x,\phi)=\sum_n\psi_n(x)e^{in\phi},\qquad n\in\mathbb Z.
\]

四维协变导数和无质量五维标量的 KK 质量塔：

\[
 D_\mu\psi_n=(\partial_\mu-i n kA_\mu)\psi_n,
 \qquad m_n=\frac{|n|\hbar}{R}.
\]

定义规范规范化 `A_can=A/g`，则相应的无量纲规范电荷为 `e_n=nkg`，以 Heaviside–Lorentz 约定 `α_n=e_n²/(4π)`。结合 (3)：

\[
 \boxed{\alpha_n=\frac{4n^2G_4\hbar}{R^2}}
 \quad\Rightarrow\quad
 \boxed{\alpha_n=\frac{4G_4m_n^2}{\hbar}.}\tag{6}
\]

这条关系是**极简圈纤维+质量纯源于环向动量**模型的特定推论，不能普遍施加给带有其他质量机制的所有粒子。

NIST CODATA 2022 输入（用于物理量数量级对照，采用常规 SI 提供的 Planck 量与电子质量，仅使用 `c=1` 的公式求比值）：

- \(\alpha_{obs}=7.2973525643\times10^{-3}\)
- \(m_e=9.1093837139\times10^{-31}\,\mathrm{kg}\)
- \(m_P=2.176434\times10^{-8}\,\mathrm{kg}\)
- \(\ell_P=1.616255\times10^{-35}\,\mathrm m\)

在 `m_n=m_e` 的最简识别下：

\[
 \alpha_{KK}=4\left(\frac{m_e}{m_P}\right)^2\approx
 7.00724\times10^{-45},\quad
 \frac{\alpha_{obs}}{\alpha_{KK}}\approx1.0414\times10^{42}.
\]

反过来强迫模型的带电 KK 模态具有观测到的 \(\alpha_{obs}\)，得到

\[
 m_{KK}=\frac{\sqrt{\alpha_{obs}}}{2}m_P \approx
 9.296\times10^{-10}\,\mathrm{kg}
\]

约为电子质量的 `1.02×10²¹` 倍，`n=1` 时圆半径约 `3.784×10^-34 m`。这是该极简模型最直接的**定量不相容问题**，不能用“数值计算成功”来掩盖。它不排除更复杂的规范/质量机制，也不能直接作为所有 KK 理论的无条件否证。

## 7. 四力、对称性与下一步的可检验路线

当前只演示：`五维 Einstein 几何 → 四维 Einstein + U(1) + radion`，还没有导出标准模型的 `SU(2)` 和 `SU(3)`，没有导出手征费米子、质量谱和 \(G\) 的独立数值。扩展到非交换内部空间会引入更多自由参数和一致性约束，不能凭空宣称它就是强弱作用。

后续严谨路线：

1. 构造**没有无依据冻结自由度**的完整协变作用量；找出背景真空与稳定性。
2. 计算二次涨落并做 Hamilton 约束，确认两光子偏振以及额外标量的质量与耦合。
3. 从微观螺旋及其对称性**不预置规范群**地推出允许的内部结构。
4. 验证规范场的非平庸曲率并检验 Noether 守恒、洛伦兹协变和量子正定性。
5. 设计可与实验对照的**无自由补偿参数**预测；若电子电荷/质量关系仍为 (6)，则极简模型已经失败。
6. 对引力新项使用地球/月球独立测量，仅报告真正使用观测数据拟合后的残差；此版本并未进行此项工作。

## 8. 计算交付说明

- `src/physics.py` 计算光速条件、曲率/挠率、规范耦合及质量-电荷关系。
- `src/symbolic_checks.py` 独立地用五维 Christoffel–Ricci 表达式验证特殊磁背景，并检查麦克斯韦平面波与半径标量变分。
- `tests/test_v143.py` 使用 unittest 做数学一致性和边界回归测试；运行 `python run_all.py`。
- `results/*.json`, `results/*.csv`, `results/tests.log` 是**真实生成的数据**；所有物理数据对照都标记为 CODATA 参考值，而非用户的实验数据。
- `legacy/ROOT_V142_Helix_Polarization_Complete.zip` 包含前版完整历史包，提供可追踪性，不代表本轮重新实测了旧版所有实验。

## 9. 参考资料

1. B. Church, *Kaluza–Klein Theory*, Stanford slides: https://web.stanford.edu/~bvchurch/assets/files/talks/Kaluza-Klein.pdf
2. *Kaluza–Klein Reduction of Einstein Gravity*: https://blackhole.org/gr-formulations/kaluza-klein-reduction-einstein-gravity/
3. *Dynamics of Matter in a Compactified Kaluza-Klein Model*: https://arxiv.org/abs/0902.1718
4. NIST, CODATA 2022: https://physics.nist.gov/cuu/pdf/all.pdf
5. *Kaluza–Klein Reduction*: https://blackhole.org/beyond-general-relativity/kaluza-klein-reduction/
