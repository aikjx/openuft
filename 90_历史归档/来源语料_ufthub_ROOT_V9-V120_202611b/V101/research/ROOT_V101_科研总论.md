# ROOT V101｜曲率—结拓扑—辐射能量下界与场逆问题不可辨识性

**日期：2026-11-19｜证据等级：严格的条件定理 + 已知物理的推论 + V100 历史理论数据的独立数值复核。**

> 本文没有解决完整统一场论，未独立计算 G，未证明 V100 连续 Maxwell 场精确存在结轨道，未执行真实实验。所有图表和数值数据均是 THEORY。所谓“突破”指在明确假设下新增的数学限制、反例及复算结果，不主张对应自然定律世界首次发现。

## 1. 研究对象和假设

延续 V100 有限截面双线圈中外源 Maxwell–Lorentz 测试粒子轨道的理论模型。物体为电荷 q 的经典点粒子；参考速率恒定、0 < v < c，β=v/c，γ=(1−β²)^−1/2；轨道为长度 L 的光滑闭合空间曲线，曲率 κ(s) 连续。忽略自场对指定轨迹的改变时，用 Liénard 公式估算辐射。结拓扑下界**仅**用于严格无自交、非平凡的空间结；此前 V100 对物理轨道的结证据仍为有限采样算法结论，不是验证式积分证书。

## 2. 结果一：辐射能量的拓扑下界 [CONDITIONAL PROOF]

恒速曲线中 a⊥=v²κ。经典 Liénard 发射功率为

\[
P=\frac{q^2\gamma^4 a_\perp^2}{6\pi\varepsilon_0c^3}
 =\frac{q^2\gamma^4v^4\kappa^2}{6\pi\varepsilon_0c^3}.
\]

使用 dt=ds/v，得到

\[
E_{\rm rad}=C\oint \kappa^2 ds,\qquad
C=\frac{q^2\gamma^4v^3}{6\pi\varepsilon_0 c^3}.
\]

Cauchy–Schwarz 给出 `∮κ²ds ≥ (∮κds)²/L`。对一般光滑简单闭曲线，Fenchel 定理 `∮κds ≥ 2π`；对非平凡结，Fáry–Milnor 定理 `∮κds ≥ 4π`，所以

\[
\boxed{E_{\rm rad}\geq E_{\rm knot}:=\frac{8\pi q^2\gamma^4 v^3}{3\varepsilon_0 c^3L}.}
\]

相比普通闭合曲线下界 `E_general=C(2π)²/L`，这个非平凡结**下界**恰好四倍。这里比较的是两条数学不等式的下界，而不是声称任意非平凡结的实际辐射都恰好是平凡结的四倍。两种最优下界的可达性不由此定理保证。

量纲：`[q²/ε0]=ML³T⁻²`，`[v³/c³]=1`，`[1/L]=L⁻¹`，故 `[E]=ML²T⁻²`。完整 SI 检查见 `src/symbolic_checks.py`。

## 3. 结果二：给定总曲率的更强下界 [PROOF + NUMERICAL]

不使用任何结分类信息，也有：

\[
\boxed{E_{\rm rad}\geq C\frac{K^2}{L},\quad K:=\oint\kappa ds.}
\]

从 V100 已保存的 `V100_ORBIT_21Q_THEORY.csv` **独立**建立闭合多边形，以边切向转角近似 K、以两侧边长平均值定义离散曲率，得到：

|量|独立复核|
|---|---|
|闭合多边形长度|0.1618828928 m|
|多边形总曲率|31.41592113|
|多边形 `∮κ² ds` 近似|6096.8067 m⁻¹|
|非平凡结下界|1.53080304×10⁻²⁸ J|
|给定 K 的 Cauchy 下界|9.56751572×10⁻²⁸ J|
|由多边形计算辐射|9.56759915×10⁻²⁸ J|
|V100 原理论辐射估计|9.56732637×10⁻²⁸ J|
|两种辐射估计相对差|2.85×10⁻⁵|
|离散曲率计算 / 离散 K 下界|1.00000872|

**解释**：该曲线非常接近五圈圆形运动，因此 K≈10π，曲率相当均匀，接近“已给定总曲率”下界；但它对非平凡结的 4π 普遍下界并不接近（约高 6.25 倍）。这里是多边形离散复核，边数与采样插值误差有作用，不能误称无限精度曲线定理或实验结果。

## 4. 结果三：真空磁场逆问题的严格不可辨识反例 [PROOF]

在圆柱环域 `0<r_min<r<r_max` 内定义两套静态真空磁场：

\[
\mathbf B^{(1)}=B_0\mathbf e_z,\qquad
\mathbf B^{(2)}=B_0\mathbf e_z+\frac{C_B}{r}\mathbf e_\phi.
\]

对 `C_B` 任意常数，环域内 `∇·B=0` 且 `∇×B=0`，因为 `∂(rBφ)/∂r=0`。附加场可由穿过环域中心孔、位于测试区域外的轴向电流产生；在环域内确实无电流源。

对于切向速度 `v eφ` 的圆轨道，额外项与速度平行，故 `q v×(B²−B¹)=0`。取负电荷 q=−e，`B0=γm_ev/(e r0)`，两场产生**完全相同**的圆形参考轨道及κ、τ、ω。可是对小径向扰动 vr：

\[
\boxed{\Delta a_z=\frac{qv_r C_B}{\gamma m_er_0}.}
\]

两场的径向—轴向扰动线性动力学不同，且磁场的能量密度不同。给定 `r0=5mm, β=0.1, C_B=10⁻⁴ T·m`，有 `Bφ(r0)=0.02T`，对应轴向电流约 500 A。这个反例否定了“单凭轨道几何必定能唯一恢复物理磁场”的命题。并不否定在加上足够多独立探针、场边界数据和完整源条件后可以重构场。

## 5. 结果四：静态场与辐射周期闭环不能无限共存 [CONDITIONAL NO-GO]

对一个假设完整周期 T 的真实辐射点电荷，当机械能、束缚近场能量（包括 Abraham–Lorentz–Dirac 形式下的 Schott 能量）及状态都在周期末恢复，周期能量收支为

\[
\int_0^T q\mathbf E(\mathbf x(t),t)\cdot\mathbf v(t)\,dt
= E_{\rm rad}>0.
\]

磁场永不做机械功。对全局单值静电势 `E=−∇Φ(x)`，固定静态场中闭合路径 `∮E·dx=0`。因此不可能在**仅有固定静态外源电磁场、无外部注能**的条件下，产生严格周期、持续加速且持续辐射的自持点电荷轨道。

必要的外部输入每周期至少为 E_rad。若所有补偿经粒子上的电功提供，有

\[
\boxed{\max_{t\in[0,T]}|E_{\parallel}(t)|
\ge E_{\rm rad}/(|q|L).}
\]

`E_parallel` 指轨道切线方向的时间依赖电场分量，上式不是任何真实装置都可直接达到的充分条件。来自 V100 的估算：每五圈 `E_rad≈9.5673e−28 J`，相当于每电子 `≈5.9715e−9 V` 电压积分，平均切线电场幅值的必要下界约 `3.689×10⁻⁸ V/m`。这显著小于电磁线圈实际可能的耗散与噪声，并不是可制造性的证明。

辐射反作用的瞬时机械功有 Schott 项，不应写成 `dK/dt=−P_rad` 的无条件逐时刻等式；这里的不可持续性结论只使用完整周期的能量收支及周期性边界条件。

## 6. 结果五：为何仍未完成四种基本相互作用统一

本轮通过的结论都使用已知 Liénard 辐射、Cauchy–Schwarz、Fáry–Milnor、Lorentz 力和 Maxwell 方程。它们为“自然螺旋一统四力”提出额外的反例与约束，但并未建立新的统一作用量，也没有独立导出 G、粒子质量谱、SU(3)×SU(2)×U(1) 的规范群或引力场量子自由度。特别是 ROOT `v_total=c` 不适用于有质量粒子的实际三维运动：本轮电子基准为 v=0.1c。

真正可推进的正面路线：定义 Lorentz/GR 协变的独立内部自由度及无异常局域作用量；从变分恢复全部已验证场方程；预测一个不靠事后参数拟合的可实验量；再进行噪声、探针、源和守恒量的可辨识检验。

## 7. 复现范围和不具备的证据

`python run_all.py` 独立生成 V101 数据、图表，运行新增单元测试与符号检查。`archive/ROOT_V100_original.zip` 保留历史基线。V100 历史 41 项测试可以从原始源码独立复跑，但网页运行、测试通过都不等于真实测量。没有执行区间算术的 ODE 周期存在证明，也没有完成结类型的严格证书。

## 8. 参考依据

1. UCSB 微分几何讲义，Fáry–Milnor 定理： https://web.math.ucsb.edu/~yer/teach/147Atext.pdf
2. Mathematical Annalen, elastic knot / Hölder lower bound： https://link.springer.com/article/10.1007/s00208-021-02346-9
3. Physics LibreTexts（Likharev）Liénard 辐射： https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Essential_Graduate_Physics_-_Classical_Electrodynamics_(Likharev)/10%3A_Radiation_by_Relativistic_Charges/10.02%3A_Radiation_Power
4. Radiation reaction and Schott energy review： https://www.mdpi.com/2073-8994/13/4/658
5. Maxwell–Lorentz 环形轨道与能量、正则动量背景： https://galileoandeinstein.phys.virginia.edu/Elec_Mag/2022_Lectures/EM_72_Particle_in_Field.html
