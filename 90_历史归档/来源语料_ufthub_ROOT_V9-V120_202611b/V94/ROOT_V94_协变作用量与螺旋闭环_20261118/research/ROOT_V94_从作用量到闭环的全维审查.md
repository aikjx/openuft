# ROOT V94｜从作用量到环面螺旋闭环：存在性、逆动力学、Maxwell 场源、稳定性与证伪

**研究日期：2026-11-18**  
**性质：数学定理、条件构造、数值验证、理论反例与开放问题盘点。全部数值为 THEORY／SIMULATED；无自主物理实验。**

## 摘要与科学裁定

ROOT V93 的给定参数化曲线，已实现从内向外、由外向内的空间周期运动。V94 首次把问题严格分成两个方向：**正问题**（给出自然作用量和实际场源，是否产生闭环）与**逆问题**（预先指定闭环，需要什么外场）。在标准相对论和 Maxwell–Lorentz 框架内，已严格得到：

- 无外力的自由粒子在 Minkowski 惯性系里不可能沿非平凡闭合空间螺旋运行。
- 只给定空间均匀、时间不变的磁场，粒子运行轨迹是圆或圆柱螺旋，不可能是非平凡环面结。
- 对任意足够光滑、速率恒定且低于光速的实验室轨迹，可**逆向构造**时间变化的外部电磁场，使它成为测试粒子的精确轨道。这是存在性构造，不是新力定律或自发形成轨迹的证明。
- 本构造的电磁势严格满足齐次 Maxwell 方程；定义外部电流可满足完整的非齐次 Maxwell 方程。但所用全空间均匀磁场、非局域电流导致无限场能量，不是有限尺寸可制造装置。
- 对 V93 三叶结基准解，数值线性化的单周期最大 Floquet 乘子模约 3.54087（β=0.8），存在受扰动放大的方向。**精确轨道存在不推出稳定性**。
- 空间闭合不是 Lorentz 不变量；闭环后相隔 T 的两个事件没有在时空中重合，不能据此构造闭合类时曲线。

本轮**没有**从曲率/挠率/频率独立导出 G、电荷、SU(3)×SU(2)×U(1) 或量子引力。V94 是一个在数学与物理边界上更加严格的进展，而非四力统一的终点。

## 1. 承接 V93 的几何基准

令主半径 R、环面截面半径 a，R>a>0，参数 u 无量纲：

\[
\boldsymbol r(u)=\bigl((R+a\cos nu)\cos mu,\;(R+a\cos nu)\sin mu,\;a\sin nu\bigr),
\quad m,n\in\mathbb N.
\]

\[
\sigma(u)=\left|\frac{d\boldsymbol r}{du}\right|=\sqrt{a^2n^2+m^2(R+a\cos nu)^2};
\quad \frac{dt}{du}=\frac{\sigma(u)}{v_0},\;v_0=\beta c,\;0<\beta<1.
\]

在 gcd(m,n)=1 时原始空间周期为 u∈[0,2π]。对于 m=2,n=3，其轨迹是三叶结。此曲线只有在所选实验室惯性系中规定了时间参数化后，才具有速度、加速度、受力等物理量。

## 2. 从协变作用量到受力方程 [现有物理 E]

在 Minkowski 平直背景中，带电质量粒子的作用量写为：

\[
S_p=\int\left[-mc^2\sqrt{1-v^2/c^2}+q\boldsymbol A(\boldsymbol x,t)\cdot\boldsymbol v-q\phi(\boldsymbol x,t)\right]dt.
\]

把场和外部电流加入总作用量：

\[
S=S_p+\int dt\,d^3x\left[\frac{\epsilon_0}{2}|\boldsymbol E|^2-\frac{1}{2\mu_0}|\boldsymbol B|^2
+\boldsymbol J_{\rm ext}\cdot\boldsymbol A-\rho_{\rm ext}\phi\right].
\]

注意：为避免计数重复，S_p 中测试粒子电流在完整耦合场方程中同样是源；本轮只把测试粒子在指定外场里的**试验粒子极限**用于精确轨迹反演，不能把背景场与它的自场视为完整自洽解。

Euler–Lagrange 方程产生：

\[
\frac{d(\gamma m\boldsymbol v)}{dt}=q\bigl(\boldsymbol E+\boldsymbol v\times\boldsymbol B\bigr),
\qquad\gamma=(1-v^2/c^2)^{-1/2}.
\]

由 \(\boldsymbol E=-\partial_t\boldsymbol A-\nabla\phi\)、\(\boldsymbol B=\nabla\times\boldsymbol A\) 可重建分量变分。这是已知的相对论电磁动力学，不是新统一力公式。

## 3. 两项 no-go：为什么不能靠几何直接得到自然闭环？ [严格]

### 3.1 自由粒子

若 \(q=0\)、无其它作用，粒子作用量 \(-mc^2\int d\tau\) 导出 \(dU^\mu/d\tau=0\)，空间轨迹为 \(\boldsymbol x=\boldsymbol x_0+\boldsymbol vt\)。除静止粒子这一退化情形外，不能形成非平凡有界闭环。对光速无质量粒子也不能使用上面的质量粒子固有时作用量，需要独立的无质量粒子或光场动力学。

### 3.2 空间均匀、时间恒定的磁场

取 E=0、B=B\(\hat z\)，则速度大小、平行 B 速度固定，横向速度以频率 \(\omega=qB/(\gamma m)\) 匀速旋转：

\[
x(t)=\frac{v_\perp\sin\omega t}{\omega},\quad
 y(t)=\frac{v_\perp(\cos\omega t-1)}{\omega},\quad
 z(t)=v_\parallel t.
\]

如 \(v_\parallel\ne0\)，z 单调且空间轨迹不闭合；如 \(v_\parallel=0\)，只能得到平面圆。不同于环面结的变曲率和变挠率。于是**均匀静磁场不产生非平凡环面结粒子轨迹**。

## 4. 一个严格的逆设计定理 [条件数学结论]

**前提：** 给定足够光滑的曲线 \(\boldsymbol r(t)\)，其速率 \(v_0\in(0,c)\) 为常数，\(\boldsymbol v=\dot{\boldsymbol r}\)、\(\boldsymbol a=\dot{\boldsymbol v}\)、\(\boldsymbol j=\dot{\boldsymbol a}\)，且 \(q\ne0,m>0\)。由于 \(\boldsymbol v\cdot\boldsymbol a=0\)，构造：

\[
\boxed{\boldsymbol B(t)=\frac{\gamma m}{qv_0^2}\bigl(\boldsymbol a(t)\times\boldsymbol v(t)\bigr).}
\]

应用三重叉积公式：

\[
\boldsymbol v\times(\boldsymbol a\times\boldsymbol v)
= v_0^2\boldsymbol a-(\boldsymbol v\cdot\boldsymbol a)\boldsymbol v=v_0^2\boldsymbol a,
\]

因此 \(q\boldsymbol v\times\boldsymbol B=\gamma m\boldsymbol a\)。由于可以任意添加平行速度方向的 \(B_\parallel(t)\boldsymbol v\)，这不是唯一反演。本式得到的是在 E=0（轨道上）且 B·v=0 条件下的**最小范数磁场**。

进一步令 \(\boldsymbol X=\boldsymbol x-\boldsymbol r(t)\)，构造规范势

\[
\boxed{
\boldsymbol A(\boldsymbol x,t)=\tfrac12\boldsymbol B(t)\times\boldsymbol X,
\qquad
\phi(\boldsymbol x,t)=\tfrac12[\boldsymbol B(t)\times\boldsymbol v(t)]\cdot\boldsymbol X.
}
\]

直接计算得：

\[
\boxed{
\boldsymbol B(\boldsymbol x,t)=\boldsymbol B(t),\quad
\boldsymbol E(\boldsymbol x,t)=-\tfrac12\dot{\boldsymbol B}(t)\times[\boldsymbol x-\boldsymbol r(t)].
}
\]

沿指定曲线 \(\boldsymbol x=\boldsymbol r(t)\)：\(\boldsymbol E=0\)。此外

\[
\nabla\cdot\boldsymbol B=0,\quad
\nabla\times\boldsymbol E=-\dot{\boldsymbol B},\quad
\nabla\cdot\boldsymbol E=0.
\]

为了同时满足 \(\nabla\times\boldsymbol B=\mu_0\boldsymbol J_{\rm ext}+\mu_0\epsilon_0\partial_t\boldsymbol E\)，取

\[
\boxed{\rho_{\rm ext}=0,\qquad
\boldsymbol J_{\rm ext}=\frac{\epsilon_0}{2}\left[
\ddot{\boldsymbol B}\times(\boldsymbol x-\boldsymbol r)
-\dot{\boldsymbol B}\times\boldsymbol v\right].}
\]

此源还满足连续性方程 \(\partial_t\rho+\nabla\cdot\boldsymbol J=0\)。任意延伸到全空间的场有非零均匀 B，因此 \(\int B^2/(2\mu_0)d^3x\) 发散；当 \(\dot B\ne0\)，E 的模还随距离线性增大。本定理只说明“具有人工外部源的 Maxwell 背景可以反演”，**不是有限场能、有限设备、自由发生的解**。实际设备的边界、场源能量和自作用未解决。

### 4.1 显式四维协变性与参考系问题

粒子与 Maxwell 场的作用量可以用四维张量写为 Lorentz 协变式。上述 E、B 的表达是在一个被指定的实验室参考系中的逆向设计；作 Lorentz 变换时需要同时变换 F^{μν}、外部电流 J^μ 和实验室所选择的场源系统。不能把实验室轨迹的三维曲率/挠率直接当成 Lorentz 标量。

## 5. 新发现：闭合空间轨道并不等于时空闭合 [严格反例]

若实验室两次遇到同一位置，事件间隔为 \(\Delta x^\mu=(cT,0,0,0)\)，对沿 x 方向以 \(V_b=\beta_b c\) 运动的参考系：

\[
\Delta t'=\gamma_b T,\qquad\boxed{\Delta x'=-\gamma_b\beta_b cT}.
\]

对 V93 基准（β=0.8）与参考系 boost=0.3c，\(\Delta x'\approx-0.0516144\) m。事件间固有时 \(\Delta\tau=T/\gamma_{\rm particle}>0\)（对常速测试粒子），所以不存在闭合时空世界线或由此产生的时间旅行问题。

## 6. V93 三叶结的反演精算和稳定性

计算基准：R=10 mm、a=2 mm、m=2、n=3、β=0.8，电子 m_e=9.1093837139×10^-31 kg（本研究所用 CODATA 2022 标称），q=−1.602176634×10^-19 C，c=299792458 m/s。

| 计算量 | V94 实际结果（理论模拟） |
|---|---:|
| 空间闭合曲线弧长 | 0.1312986594444883 m |
| 单圈周期 | 约 5.47456×10^-10 s |
| 逆磁场强度区间 | 0.108964–0.255744 T |
| 独立高精度磁场向量核对 | 85 位，最大相对差 7.33×10^-16 |
| 非线性 Lorentz ODE 前向积分最大归一化误差 | 1.633×10^-10 |
| β=0.8，单周期最大 Floquet 乘子模 | 3.54087 |
| monodromy 矩阵行列式 | 约 1，数值量级精度内 |
| 0.3c boost 后空间返回事件位移 | −0.0516144 m |

在给定的逆向场里，局部 Floquet 乘子模超过 1 表明至少一个线性扰动方向的单周期振幅增长。它属于固定驱动周期的测试粒子有限维线性稳定性审计；并未证明真实工程装置的长期不稳定性，也没有计算出真正的控制策略。

**小心：** 这种场在轨道处 E=0，所以点粒子在理想化的 Lorentz 方程中保持能量；但真实加速电荷会辐射，辐射反作用和补偿能量未包含。不能把这一模型当永动机，亦不能把测试粒子闭环误写成全 Maxwell–粒子自洽闭环。

## 7. 为什么磁力线打结不等于粒子本身沿磁力线打结？

真实 Maxwell 场能够具有打结、闭合、链接的电磁场线，这已是独立研究主题。**磁力线是一种空间场积分曲线，而带电粒子的轨迹由 Lorentz 微分方程决定**。若粒子速度局部恰好与磁场平行，则 \(q\boldsymbol v\times\boldsymbol B=0\)，该磁场不会提供将轨迹立即弯成场线的法向力。若要约束粒子沿曲线，就需考虑引导中心近似、磁梯度、反射、边界等明确机制。场线结的拓扑不自动转化为单粒子轨迹结，更不自动推导四力统一。

相关已发表文献指出 Maxwell 真空场确实允许非平凡的打结电磁场线（见第 12 节）；不能把这些既有结果描述为 ROOT 自主发现。

## 8. 维度对碰与循环定义审计

以 kg,m,s,A 四种 SI 基本量作为维度基；本轮新审计 54 类物理量、1431 对两两组合、33 条候选方程，其中 7 条刻意加入的不合法示例被识别为量纲不符。

\([\boldsymbol B]=M T^{-2}I^{-1}\)、\([\dot {\boldsymbol B}]=M T^{-3}I^{-1}\)、\([\boldsymbol E]=MLT^{-3}I^{-1}\)、\([\boldsymbol A]=MLT^{-2}I^{-1}\)、\([\rho_e]=ITL^{-3}\)、\([\boldsymbol J]=IL^{-2}\)。

注意：[G]=M^-1 L^3 T^-2。即使通过 \(\kappa_*\) 构造量纲正确的 \(G=\xi c^3/(\hbar\kappa_*^2)\)，若 \(\kappa_*\) 来源于已知 G 的普朗克长度，此式仍循环。量纲一致从不是物理等价的充分条件。

## 9. “从内到外，从外到内”能否导出四力？

**不能从这一环面曲线单独导出：**

- 曲率给出常速轨迹的法向加速度 \(a=v^2\kappa\)，但不指定产生它的电荷、质量或具体场。
- 挠率是参考系依赖的三维几何量；强、弱相互作用还要求内禀量子数、规范群表示、手征性和非阿贝尔场强。
- 电磁逆向场已通过已知 Lorentz 力构造，不能从中倒推“磁力由曲率发明”。
- 引力需通过完整应力—能量张量及 Einstein 方程耦合，还缺少独立推导 G 与量子时空自由度。
- 将磁场线的拓扑链接数、磁螺度和粒子自旋直接等同为相同的“统一频率”，尚无数学或实验根据。

## 10. 假设性的协变内部螺旋动力学：最简检验入口

可以研究具有固有加速度曲率 \(\kappa_4=\sqrt{a^\mu a_\mu}/c^2\) 的非平凡世界线泛函：

\[
S_{\rm trial}=-mc^2\int d\tau + \frac{K}{2}\int \kappa_4^2\,d\tau,
\quad [K]={\rm J\,m^2}.
\]

**这只是候选高阶导数理论的形式，不是验证过的新基本作用量。** 要证明它产生自发稳定的内外闭环，需要列出完整高阶 Euler–Lagrange 方程、施加边界条件、检查物理自由度与幽灵/Ostrogradsky 风险，验证实验限制和有效场论适用范围。甚至即使产生闭环，也没有自动产生 QCD 和弱相互作用。此处没有宣称已求解上述条件。

## 11. 接下来需要逐项关闭的具体缺口

1. 有限区域、具有物理线圈与电流分布的 Maxwell 源能否近似实现逆向场？
2. 源的磁体与线圈受到的力如何反作用？完整装置总能动张量能否守恒？
3. 电子相对论辐射反馈如何改变闭合轨道？是否能通过受控 E·v 补偿？
4. 能否找到无需预先“编程”轨迹、由守恒量和对称性自然产生环面闭环的作用量？
5. 哪些候选轨道在完整扰动和噪声下存在吸引域或稳定岛？
6. 内部自由度怎样作为 Lorentz 表示或协变局域场出现？
7. 是否能够不输入已知 q、m、G 而导出这些常数及粒子谱？
8. 如何建立量子态与时空几何共同的规范不变可观测量？
9. 有无现有标准模型＋GR 不同且仪器可检的独立预测？

全部旧研究任务连同 V94 新增 28 项，记录在 `ledger/ALL_205_ISSUES.csv`。`NO_GO_PROVEN` 代表**排除原候选机制**，不代表“统一场论已解决”。

## 12. 资料对照（已知文献，非本项目原创）

- Feynman Lectures, Vol. II, Ch. 13, Lorentz Force: https://www.feynmanlectures.caltech.edu/II_13.html
- UW Lecture notes: Relativistic Particle with Electric Charge, action and field coupling: https://faculty.washington.edu/seattle/physics544/2011-lectures/zwiebach.pdf
- Kedia et al., *Tying Knots in Light Fields*, knotted null electromagnetic field constructions: https://irvinelab.uchicago.edu/papers/LA14160.pdf
- *Stable Knots and Links in Electromagnetic Fields*, Commun. Math. Phys. (2022): https://link.springer.com/article/10.1007/s00220-021-04219-3
- *Knots in Electromagnetism*, Physics Reports review: https://www.sciencedirect.com/science/article/pii/S0370157316303908

阅读提示：已知 Maxwell 场线的结结构、带电粒子轨迹和 ROOT 内部运动假设是不同层级的对象；文献只支持相应的已发表结论，不支持未经证明的四力统一宣称。

## 附录：复现与证据等级

`python run_all.py` 运行数学测试、SymPy 恒等式、维度检查、逆场独立计算、相对论 ODE、扰动线性化与扫描图。数据、图表文件名标识 `THEORY`、`NUMERICAL` 或 `SIMULATED`。不包含真实观测数据、粒子实验或任何“已检测到新力”的证据。完整源码为 `src/*.py`，浏览器交互示范为 `web/index.html`，独立历史基线位于 `archive/ROOT_V93_original.zip`。
