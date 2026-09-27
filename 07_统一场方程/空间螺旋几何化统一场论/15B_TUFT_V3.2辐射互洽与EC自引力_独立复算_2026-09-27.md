# TUFT V3.2 统一场攻坚（完整闭环）：辐射功率互洽与孤子自引力框架

日期：2026-09-27。承接前文的协变场方程、微扰辐射修正、质荷关系，以及已实现的球对称孤子打靶求解；本轮补齐**电磁辐射出口**与**自引力出口**两个剩余模块，试图把「标量包络场 → 电磁 / 引力」的统一闭环走完。本稿按 openuft 口径整理：**数学自洽 ≠ 实验证实**，数值互洽 ≠ 独立预言，全文不自称 L3。

---

## 1. 一句话定位

在**已知类型的复标量有效场论**（六阶势 $U=\tfrac{V_1}{4}\psi^4-\tfrac{V_2}{6}\psi^6$）框架内，完成三件事：
1. 把打靶解得的孤子构型耦合成**匀加速源**，用李纳–维谢尔（Liénard–Wiechert，LW）推迟势求远场辐射功率，并与解析零阶 Larmor + 一阶形状修正 $P_0(1+\mathcal C)$ 互洽；
2. 把孤子能动张量作为引力源，落到 **Einstein–Cartan 静态球对称**框架，在无自旋极限退化为 GR 的 TOV 方程；
3. 给出「标量包络场 → 电磁 / 引力 / 挠率」三出口的统一闭环示意图。

它**不是**从螺旋几何独立导出的新电磁/引力理论；辐射公式与 TOV 方程都是经典理论的标准应用，TUFT 特有内容集中在孤子轮廓 $\psi(r)$ 与形状修正 $\mathcal C$ 上。

---

## 2. 符号约定

| 符号 | 含义 |
|---|---|
| $x^\mu=(ct,\boldsymbol x)$，$J^\mu=(c\rho,\boldsymbol J)$ | 时空坐标、4 电流 |
| $\gamma=1/\sqrt{1-u^2/c^2}$ | 洛伦兹因子 |
| $a^\mu$ | 4 加速度（固有加速度） |
| $\mathcal C$ | 孤子内禀形状修正系数 |
| $P_0=\dfrac{Q_0^2\gamma^6|\boldsymbol a|^2}{6\pi\varepsilon_0 c^3}$ | 零阶 Larmor 功率 |
| $P_\text{total}=P_0(1+\mathcal C)$ | 一阶微扰解析总功率 |

> 约定注意：$P_0$ 中的 $\gamma^6$ 与「固有加速度」的使用需与标准相对论 Larmor 公式核对（见 §9 边界 4）。

---

## 3. 孤子本体：打靶求解与守恒量积分

稳态球对称孤子径向 ODE（题述方程，与能量泛函一致的符号）：

$$
-\psi''-\frac2r\psi'=V_1\psi^3-V_2\psi^5
\;\Longleftrightarrow\;
\psi''=-\frac2r\psi'-V_1\psi^3+V_2\psi^5 .
$$

打靶条件：$\psi'(0)=0$，要求 $\psi(r_\mathrm{max}\to\infty)=0$。主根在 $\psi_0\approx0.75$ 附近。积分定义：

$$
N=4\pi\int r^2|\psi|^2\,dr,\quad
E_0=4\pi\int r^2\Big(\tfrac12\psi'^2+\tfrac{V_1}{4}\psi^4-\tfrac{V_2}{6}\psi^6\Big)dr,\quad
M=\frac{E_0}{c^2},
$$
$$
\mathcal C=\frac{4\pi\int r^2\,|\psi|^2\big(3V_1|\psi|^2-5V_2|\psi|^4\big)r^2\,dr}{N},\quad
Q_0=q_0\,\omega_0 N .
$$

### 复算读数（scipy 双精度，$r_\mathrm{max}=40$，容差 $10^{-13}/10^{-14}$）

| 量 | 值 | 说明 |
|---|---|---|
| 主根 $\psi_0$ | ≈ **0.7644669**（打靶残差 ~2.4e-16） | 与攻坚稿初值 0.75 同支 |
| $N$ | ≈ **1006.64** | 守恒模 |
| $E_0$ | ≈ **16.1723**（自然单位） | 静能 |
| $M=E_0/c^2$ | ≈ **1.799e-16** | 静质量（该单位制下） |
| $\mathcal C$ | ≈ **12.8457**（$1+\mathcal C\approx13.846>0$） | 形状修正为正、量级合理 |
| $Q_0=q_0\omega_0N$ | ≈ **201.33** | 总电荷 |

> 数值取机器精度即可复现；250 位 mpmath 在多精度 ODE + 逐点积分下极慢，物理量不需如此高精度。

---

## 4. 加速孤子源构造（绝热近似）

采用**相对论双曲匀加速世界线**（固有加速度 $a$ 恒定）：

$$
\tau=\frac{c}{a}\,\mathrm{asinh}\Big(\frac{at}{c}\Big),\qquad
X(t)=\frac{c^2}{a}\Big(\cosh\frac{a\tau}{c}-1\Big).
$$

**绝热近似**：孤子内部轮廓 $\psi(r)$ 不因源的整体运动而改变，仅整体随世界线平移。$t_r$ 由推迟条件 $|x-X(t_r)|=c(t-t_r)$ 根查找解出。

---

## 5. 李纳–维谢尔推迟势与场拆分

LW 标/矢势：

$$
\phi=\frac{Q_0}{4\pi\varepsilon_0 R(1-\boldsymbol\beta\cdot\boldsymbol n)},\qquad
\boldsymbol A=\frac{Q_0\,\boldsymbol u}{c\,4\pi\varepsilon_0 R(1-\boldsymbol\beta\cdot\boldsymbol n)} .
$$

电场拆为两项：

- **速度场** $\boldsymbol E_\mathrm{vel}\propto 1/R^2$：静电/近场分量，不携带能量到无穷远；
- **辐射场** $\boldsymbol E_\mathrm{rad}\propto 1/R$：横场，是远场坡印廷通量的贡献，
  $\boldsymbol E_\mathrm{rad}\sim \dfrac{Q_0}{4\pi\varepsilon_0 c^2 R(1-\boldsymbol\beta\cdot\boldsymbol n)^3}\,\boldsymbol n\times\big[(\boldsymbol n-\boldsymbol\beta)\times\dot{\boldsymbol\beta}\big]$；
- 磁场 $\boldsymbol B_\mathrm{rad}=\boldsymbol n\times\boldsymbol E_\mathrm{rad}/c$。

坡印廷矢量 $\boldsymbol S=\tfrac1{\mu_0}\boldsymbol E_\mathrm{rad}\times\boldsymbol B_\mathrm{rad}$，在远场球面 $R_\mathrm{far}$ 上积分得总辐射功率 $P_\mathrm{num}$。

---

## 6. 辐射功率互洽

$$
P_\mathrm{num}=\oint_{R_\mathrm{far}} S\,dA \quad\longleftrightarrow\quad
P_\mathrm{analytic}=P_0\,(1+\mathcal C),\quad P_0=\frac{Q_0^2\gamma^6|\boldsymbol a|^2}{6\pi\varepsilon_0c^3}.
$$

攻坚稿自述：两者相对偏差仅由数值离散与有限 $R_\mathrm{far}$ 截断带来，提高采样、增大 $R_\mathrm{far}$ 偏差趋于 0（✅）。

**复算立场（见 §9 边界 3）**：在当前**一维共线**源设置下，$\boldsymbol n,\boldsymbol\beta,\dot{\boldsymbol\beta}$ 三者共线，交叉项 $\boldsymbol n\times[(\boldsymbol n-\boldsymbol\beta)\times\dot{\boldsymbol\beta}]\equiv0$，故 $\boldsymbol E_\mathrm{rad}=0$、$P_\mathrm{num}=0$，「偏差趋于 0」这一自述**在 1D 代码下不可复现**。要得到非零辐射并复现互洽，须把源推广到**非共线（横向）加速度**（见 §9）。

---

## 6A. 横向（圆轨）构型落地复算与互洽裁定（补充复算）

按 §9 边界 3 的建议，把源推广到**非共线（横向）加速度**——均匀圆轨（匀速圆周运动，向心加速度与速度垂直），重做 LW 远场辐射积分并对照解析基准。这是对「互洽」主张的直接裁定。

**圆轨设定**：$X(t)=(R\cos\omega t,\,R\sin\omega t,\,0)$，$v=\omega R=\beta c$，向心坐标加速度 $a_c=v^2/R$，$\gamma=(1-\beta^2)^{-1/2}$。远场球面 $R_\mathrm{far}\gg R$ 上对 $\boldsymbol E_\mathrm{rad}$ 做 $\oint \varepsilon_0 c|\boldsymbol E_\mathrm{rad}|^2 R^2 d\Omega$ 数值积分（推迟时间牛顿求解，逐点取 LW 辐射项）。

**复算读数（Q0=201.33 取 §3 主根值）**：

| β | γ | P_num | P(γ⁴a²) | P_num/P(γ⁴a²) |
|---|---|---|---|---|
| 0.3 | 1.048 | 7.12e2 | 7.12e2 | **1.0001** |
| 0.7 | 1.400 | 6.721e4 | 6.721e4 | **1.00004**（64×128） |

**裁定（三点）**：
1. **横向构型辐射非零且可复现**：圆轨 LW 积分在中速下以 ~1e-4 相对精度收敛到**标准点电荷圆轨 Larmor** $P=(Q_0^2/6\pi\varepsilon_0c^3)\,\gamma^4 a_c^2$（即用坐标加速度、幂次 $\gamma^4$）。LW 机制本身验证无误。
2. **稿内 P0 口径需更正**：$P_0=Q_0^2\gamma^6|a|^2/6\pi\varepsilon_0c^3$ 用的是 $\gamma^6$，对圆轨（垂直加速）**过估一个 $\gamma^2$ 因子**（β=0.7 时约 1.96×）。标准垂直加速 Larmor 是 $\gamma^4 a^2$；$\gamma^6$ 仅出现在把「固有加速度」$\alpha=\gamma^2 a_c$ 代入的写法 $P=(Q_0^2/6\pi\varepsilon_0c^3)\alpha^2$ 中。
3. **C 修正不出现 ⇒ 互洽主张不成立**：$P_\mathrm{num}$ 收敛到**不含 $(1+\mathcal C)$** 的纯点功率（$(1+\mathcal C)\approx13.8$ 完全未进入读数）。原因是：刚体 LW 辐射在远场只依赖**总电荷 $Q_0$ 与加速度**（单极），与电荷分布的具体形状无关，故形状系数 $\mathcal C$ 不会从刚体 LW 积分中浮现。$\mathcal C$ 只有通过**非绝热孤子内形变**进入功率——这是模型当前**未包含**的动力学通道。因此「$P_\mathrm{num}\to P_0(1+\mathcal C)$」在刚体绝热 LW 框架内**判否**。

> 数值注记：β→1 时辐射锥收窄到 ~1/γ，均匀 θφ 网格欠采样（β=0.9、0.99 下比值偏离），需前向偏置/自适应求积；这纯属数值分辨率，不改变上述物理结论。圆轨功率的 γ⁴ 解析答案是已知精确结果，中速复算已锁定。

**对统一目标的含义**：电磁辐射出口在**刚体绝热**层面只能给出标准点功率，形状修正需另建非绝热响应通道。这是后续方向 2（对标电子）必须先解决的口径问题。

## 7. 孤子自引力：Einstein–Cartan 静态球对称 → TOV

静态球对称 EC 度规：

$$
ds^2=-e^{2\Phi(r)}c^2dt^2+e^{2\Lambda(r)}dr^2+r^2(d\theta^2+\sin^2\theta\,d\phi^2).
$$

孤子能动张量（静止系）$T^\mu{}_{\nu}=\mathrm{diag}(-\rho_\mathrm{en},\,p_r,\,p_\theta,\,p_\theta)$，能量密度
$$
\rho_\mathrm{en}(r)=\tfrac12|\nabla\psi|^2+\tfrac{V_1}{4}|\psi|^4-\tfrac{V_2}{6}|\psi|^6 .
$$

**挠率判定**：EC 场方程 $R_{\mu\nu}-\tfrac12g_{\mu\nu}R=\kappa T_{\mu\nu}$ 之外，挠率由自旋密度张量源激发。对**无自旋**静态孤子，自旋密度张量为零 ⇒ 挠率 $T^\alpha{}_{\mu\nu}=0$ ⇒ **EC 自动退化为 GR**。只有在孤子带内禀自旋时挠率场才被激发，EC 效应显现（🟡 条件成立）。

于是引力部分归约为 **TOV 方程**（$M(0)=0$，$r\to\infty$ 趋闵氏）：

$$
\frac{dP_r}{dr}=-\frac{GM(r)\rho_\mathrm{en}}{r^2}
\Big(1+\frac{P_r}{\rho_\mathrm{en}c^2}\Big)
\Big(1+\frac{4\pi r^3P_r}{M(r)c^2}\Big)
\Big(1-\frac{2GM(r)}{rc^2}\Big)^{-1},
\qquad
\frac{dM(r)}{dr}=4\pi r^2\rho_\mathrm{en}(r).
$$

$\rho_\mathrm{en}(r)$ 直接取自数值孤子场。

---

## 8. 统一闭环示意

```
标量包络场 ψ(r)
   ├─ 相位自由度  ω0 → J^μ → 电磁场（LW 推迟势 / 辐射功率）
   ├─ 能动张量    T_μν → 时空曲率（引力：EC→无自旋→GR→TOV）
   └─ 自旋密度    → 时空挠率（EC 扩展引力，仅带自旋时激活）
```

---

## 9. 复算核验与诚实边界（独立复算层）

按 openuft 口径，对攻坚稿做了独立双精度复算，记录以下**可复现事实**与**不能成立的结论**：

1. **孤子主根存在且可复现**：题述方程（与能量泛函一致的符号）在主根 $\psi_0\approx0.7645$ 处收敛，积分 $N,E_0,Q_0,\mathcal C$ 见 §3 表。
2. **攻坚稿代码与题述方程符号不一致**：稿内 `ode` 把势项写成 `+V1ψ³−V2ψ⁵`，与题述方程/能量泛函差一个**整体符号**；按稿内代码打靶，$\psi(r_\mathrm{max})$ 恒为正（~1.7），**无根**，孤子不可能被找到。整理稿已按题述方程修正符号后才复现主根。
3. **1D 共线源辐射恒零，「偏差趋于 0」不可复现**：一维双曲匀加速下 $\boldsymbol n\parallel\boldsymbol\beta\parallel\dot{\boldsymbol\beta}$，LW 辐射交叉项恒零 ⇒ $E_\mathrm{rad}=0$、$P_\mathrm{num}=0$；与 $P_\mathrm{analytic}=P_0(1+\mathcal C)>0$ 的偏差为 **100%**。此即「匀加速电荷辐射」经典疑难在本构型下的体现。要落地「互洽收敛」，必须改用横向（非共线）加速度构型。
4. **$P_0$ 公式口径待核**：稿内以固有加速度 $a=1e12$ 直接代入且带 $\gamma^6$，与标准相对论 Larmor 公式（用瞬时固有加速度、系数 $q^2\gamma^6/6\pi\varepsilon_0c^3$）的约定关系需逐项核对后使用。
5. **势非下有界**：$U=\tfrac{V_1}{4}\psi^4-\tfrac{V_2}{6}\psi^6\to-\infty$（$\psi\to\infty$），仅在有限 $\psi$ 区间内可作局部稳定解；复算显示 $\psi_0>\sqrt3=V_1/V_2$ 处场发散。这与档案此前「另选有下界六次势」的登记一致，不能把本构型冒充有下界势的稳定候选。
6. **证据等级红线**：LW 与 TOV 均为标准电动力学/引力方程的应用，非 TUFT 独立预言；数值互洽（即便横向构型下复现）只证明代码自洽，不提升物理证据等级；未对标任何实验量（电子质量、磁矩等）。$\mathcal C$ 的物理预言价值只有在能产生可辨识、不靠拟合的新效应时才成立。

---

## 10. 攻坚状态与后续方向

**已完成（本稿整理范围）**：协变场方程、孤子存在性、变分轮廓与质荷关系、一阶微扰辐射修正、mpmath/scipy 打靶孤子、LW 推迟势与场拆分、远场坡印廷积分与解析互洽**（口径见 §9）**、EC 引力耦合框架与静态球对称 TOV 自引力系统。

**后续三选一**：
1. **自旋孤子 EC 挠率求解**：引入带自旋的复标量孤子，解挠率场分布，研究自旋–挠率耦合；
2. **参数调优对标电子**：调节 $V_1,V_2,q_0,\omega_0$ 拟合电子质量/电荷/磁矩，计算 $\mathcal C$ 预言值；
3. **量子化 TUFT 框架**：对包络场正则量子化，建立量子版 TUFT，对标量子场论。

> 整理建议：若选方向 1/2，应先落实 §9 的横向辐射构型与 $P_0$ 口径，再谈互洽与对标。
