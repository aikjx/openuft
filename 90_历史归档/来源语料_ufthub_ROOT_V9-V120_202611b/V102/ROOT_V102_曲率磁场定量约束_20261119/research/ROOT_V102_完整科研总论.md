# ROOT V102｜从曲率与挠率到磁场强度：闭合结的可计算约束

**日期：2026-11-19｜证据：已知经典理论的严格条件推论 + 合成/历史轨迹数据的数值交叉验证。**

> 重要声明：本文未证明统一场论，未推出基本常数 G，未实现自维持带电粒子结轨道，未验证 V100 连续磁场周期轨道的严格存在性。数值数据全部是历史 THEORY/SYNTHETIC 数据；不是自然观测，也没有发现新基本相互作用。所谓“证明”均明确受到假设限制。

## 1. 为什么要从反推磁场开始

ROOT V90—V101 累计了光速螺旋、环面闭环、外源线圈 Maxwell–Lorentz、三维数值周期候选、结自交反例和 Liénard 辐射下界等方法。在 V101 已得到 \(E_{\rm rad}=C\oint\kappa^2ds\) 之后，本轮专攻“是否能够从轨迹几何求出维持轨迹所需的外部磁场”。

**明确的命题边界：** 若指定恒定速率、非零电荷、无电场、经典点质量与相对论 Lorentz 力，则可以**局部**反推出磁场的横向分量；并不能单凭轨道确定磁场沿切线的分量，也不能自动给出全空间满足 Maxwell 方程和有限电流边界条件的场。

## 2. 定理 1｜Frenet–Lorentz 局部磁场重构 [STRICT UNDER ASSUMPTIONS]

设光滑空间轨迹 \(\mathbf x(s)\)，\(s\) 为弧长，\(\mathbf T,\mathbf N,\mathbf b=\mathbf T\times\mathbf N\) 为 Frenet–Serret 标架。\(\kappa=|d\mathbf T/ds|>0\)，\(0<v<c\)，\(\gamma=(1-v^2/c^2)^{-1/2}\)。要求带电粒子仅受磁力且速度恒定：

\[
\mathbf v=v\mathbf T,\quad \mathbf a=v^2\kappa\mathbf N,\quad
q\mathbf v\times\mathbf B=\gamma m_0\mathbf a.
\]

将任意候选磁场分解成 \(B_T\mathbf T+B_N\mathbf N+B_b\mathbf b\)，利用 \(\mathbf T\times\mathbf N=\mathbf b\)、\(\mathbf T\times\mathbf b=-\mathbf N\) ，得到 \(B_N=0\)，且 \(-qvB_b=\gamma m_0 v^2\kappa\)。因此

\[
\boxed{\mathbf B(\mathbf x(s))=-\frac{\gamma m_0 v}{q}\kappa(s)\,\mathbf b(s)+B_\parallel(s)\mathbf T(s).}
\]

也可不经 Frenet 标架，直接写

\[
\boxed{\mathbf B_\perp=\frac{\gamma m_0}{qv^2}(\mathbf a\times\mathbf v).}
\]

第二个式子对局部 \(\kappa=0\) 处同样适用。沿切线磁场 \(B_\parallel\) 是未确定的函数。**这是局部代数逆问题而非全局 Maxwell 方程的存在性定理**；实际源和边界条件可能限制或排除给定 \(B_\parallel\)。

速度具有固定模时，粒子实际空间速度依然严格小于 \(c\)。四速度不变量 \(U^\mu U_\mu=-c^2\) 并不等价于实际三维速度恒为 \(c\)。

## 3. 定理 2｜磁场的结拓扑下界 [CONDITIONAL]

局部横向磁场满足：

\[
B_\perp(s)=\frac{\gamma m_0v}{|q|}\kappa(s),\qquad
\overline{B}_\perp=\frac1L\oint B_\perp ds=\frac{\gamma m_0v}{|q|L}K,
\quad K:=\oint\kappa ds.
\]

一般光滑嵌入的闭合曲线，Fenchel 定理 \(K\ge2\pi\)；若是 **无自交的非平凡空间结**，Fáry–Milnor 定理 \(K\ge4\pi\)。因此

\[
\boxed{\overline{B}_\perp\ge \frac{4\pi\gamma m_0v}{|q|L}},\quad
\boxed{B_{\perp,\mathrm{rms}}\ge\overline B_\perp\ge \frac{4\pi\gamma m_0v}{|q|L}}.
\]

**警告：** V100 保存的三维近闭合数值多边形尚没有连续精确 Maxwell ODE 解的区间验证证书。V100 能计算 \(K\) 和 \(B_\perp\)，但将 4π 下界用于其“真实连续结轨道”的行为仍是以确认为嵌入非平凡结为前提的条件判断。

## 4. 定理 3｜辐射能量和横向磁场平方积分等价 [CONDITIONAL]

对恒速规定轨迹，Liénard 远区辐射公式为

\[
E_{\rm rad}=\frac{q^2\gamma^4v^3}{6\pi\varepsilon_0c^3}\oint\kappa^2ds.
\]

由定理 1 代入 \(\kappa=|q|B_\perp/(\gamma m_0v)\)，严格化为

\[
\boxed{E_{\rm rad}=\frac{q^4\gamma^2v}{6\pi\varepsilon_0m_0^2c^3}\oint B_\perp^2 ds.}
\]

本式是 V101 辐射公式在同一恒速纯磁力轨道上的另一种表达，而非新的辐射物理。要从模型轨迹持续实现闭环，仍必须考虑辐射反作用、外源能量补给和场的时间依赖。

## 5. 定理 4｜辐射超额与曲率/磁场不均匀度的严格等式 [CONDITIONAL]

记 \(K_2=\oint\kappa^2ds\)，\(\overline\kappa=K/L\)，曲率沿弧长的变异系数 \(\mathrm{CV}_\kappa^2=K_2L/K^2-1\)。那么

\[
\boxed{\frac{E_{\rm rad}}{C K^2/L}=1+\mathrm{CV}_\kappa^2=1+\mathrm{CV}_{B_\perp}^2},
\qquad C=\frac{q^2\gamma^4v^3}{6\pi\varepsilon_0c^3}.
\]

这解释了 V101 的数值现象：若沿路径曲率近乎均匀，辐射值会接近“给定总曲率 K”的 Cauchy 下界；若曲率变化很强，辐射能量必定高于那个下界。**它不声称一条结轨道实际能达到给定拓扑种类下的理论全局最小能量。**

## 6. V100 历史理论轨迹的独立计算 [NUMERICAL]

使用 V100 原始保存的 1201 个三维轨道点（\(\beta=0.1\)），不用旧 V101 的辐射代码，由闭合多边形边长及转角独立重建曲率。数据文件为 `data/V100_ORBIT_21Q_INPUT_THEORY.csv`。计算如下：

| 项目 | V102 复算 |
|---|---:|
| 闭合多边形长度 | 0.1618828928 m |
| 总曲率 \(K\) | 31.41592113 |
| 曲率均值 | 194.065726 m⁻¹ |
| 曲率均方根 | 194.066572 m⁻¹ |
| 所需磁场 \(\overline{B}_\perp\) | 0.03324532245 T |
| 所需磁场 \(B_{\perp,\mathrm{rms}}\) | 0.03324546740 T |
| 磁场沿轨道的标准差 | 0.00009817113 T |
| 磁场变异系数 | 0.0029529307（约 0.295%）|
| 非平凡结条件下的通用磁场下界 | 0.01329813127 T |
| \(K_2L/K^2\) | 1.00000871980 |
| 从曲率计算的经典辐射能量 | 9.56759915 × 10⁻²⁸ J |
| 从磁场平方积分计算的经典辐射能量 | 9.56759915 × 10⁻²⁸ J |
| 两种表达式的浮点相对差 | 约 1.87 × 10⁻¹⁶ |
| 与 V100 保存辐射数据的相对差 | 约 2.85 × 10⁻⁵ |
| 给定 K 的 Cauchy 下界超额 | 约 8.3427 × 10⁻³³ J |

这些数值说明的是**一个指定的历史理论轨道在经典电磁力框架内的运动学与辐射一致性**，不等于直接测量到磁场，更不证明四力统一。

按 \(T=L/v\) 粗略估计，该周期约为 5.3998 ns，平均辐射功率约 1.772 × 10⁻¹⁹ W；如连续光滑轨道经证书证实为非平凡结，对应的普适结下界功率约为 2.835 × 10⁻²⁰ W。

## 7. 为什么这还不是四力统一 [OPEN]

1. 仅由轨迹几何无法唯一确定 \(B_\parallel\) 或 Maxwell 场的全局源，V101 已有具有相同参考轨道但扰动不同的真空 Maxwell 反例。
2. 磁场约束限于经典带电粒子、纯磁力、恒定空间速率，不能推广到不带电物体、强弱规范场或量子引力。
3. 有限轨道样本不是连续精确周期轨道的区间算术证明；即使数值结行列式一致，也不自动产生可接受的连续结型证书。
4. 磁场沿轨道的必要强度不等于产生这个场所需的总磁能；总磁能、电流密度、源体到轨道距离、辐射损失必须单独优化。
5. 四力统一至少要求局域协变作用量、规范群结构、手征性、异常抵消、GR/SM 极限、可辨识新预测及独立实验；本轮没有完成这些。

## 8. 下一轮值得严格证明的命题

- **ODE 存在性证书：** 对连续有限截面线圈的周期映射建立带定向误差界的区间 Newton / Krawczyk 证明。
- **连续轨道嵌入证书：** 对所有非相邻弧段求正的间隔下界，用正规结投影和可审核的 Reidemeister 规约或可验证不变量确定结型。
- **场源可行性：** 结合源体间距和电流密度上限，建立磁场沿轨道下界对总材料成本、储能和发热的可实现边界。
- **完整能量闭环：** 联立带辐射反作用的运动方程、有限源与外部电源；验证周期返回时机械、近场与远区能量的闭环账本。

## 9. 外部文献与归属

上述结果使用或推演了既有 Lorentz 力、Frenet–Serret 公式、Liénard 功率及 Fáry–Milnor 定理。不能称为世界首次发现。参考：

- Liénard 相对论辐射公式，Likharev/LibreTexts：https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Essential_Graduate_Physics_-_Classical_Electrodynamics_(Likharev)/10%3A_Radiation_by_Relativistic_Charges/10.02%3A_Radiation_Power
- 粒子与打结电磁场的公开研究：https://doi.org/10.1088/1751-8121/ac7c49
- Fáry–Milnor 总曲率综述：https://web.math.ucsb.edu/~yer/teach/147Atext.pdf
- ROOT V101 附带的历史基准与进一步详细参考见 `archive/ROOT_V101_original.zip`。
