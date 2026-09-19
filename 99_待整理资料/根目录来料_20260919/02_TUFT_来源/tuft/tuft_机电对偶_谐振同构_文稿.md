# 力学–电磁对偶（机电类比）全维精算与求导整理

> 本册对应脚本：`tuft_机电对偶_谐振同构_全维精算.py`
> 精算报告：`tuft_机电对偶_report.txt`
> 结果：**PASS = 39 · FAIL = 0 · BOUNDARY = 9 · INFO = 1**
>
> 红线：数学自洽 ≠ 物理证实。凡属已知结果、欠定、或不可证伪的表述，一律标 BOUNDARY/FAIL，不粉饰为理论成就。

---

## 一、两套系统的方程与求导（完整版）

### 1.1 机械：弹簧–质量简谐振子

运动方程与能量：

$$m\ddot x + kx = 0, \qquad E_{\rm mech} = \tfrac12 m\dot x^2 + \tfrac12 k x^2$$

对能量求导：

$$\frac{dE}{dt} = m\dot x\ddot x + kx\dot x = \dot x\,(m\ddot x + kx)$$

代入运动方程即 $\dot E = 0$。**精算 A1**：sympy 符号求导后代入 $m\ddot x = -kx$，`simplify` 结果恒为 `0`（机器零）。

### 1.2 电磁：串联 LC 回路

$$L\ddot q + \frac1C q = 0, \qquad E_{\rm em} = \tfrac12 L\dot q^2 + \frac{1}{2C}q^2$$

$$\frac{dE}{dt} = L\dot q\ddot q + \frac1C q\dot q = \dot q\left(L\ddot q + \frac1C q\right) = 0$$

**精算 A2**：符号求导+代入后 `simplify = 0`。

### 1.3 解析解与角频率

取 $x = A_0\cos(\omega t+\phi)$ 代入：

- 机械残差 $= A_0(k - m\omega^2)\cos(\omega t+\phi)$ ⟹ $\omega = \sqrt{k/m}$
- 电磁残差 $= A_0(1 - CL\omega^2)\cos(\omega t+\phi)/C$ ⟹ $\omega = 1/\sqrt{LC}$

**精算 A4**：RK4 积分 100 个周期（两套系统、各两组参数），能量相对漂移均 $\sim 2.7\times10^{-12}$，守恒成立。
**精算 A5/A6**：相空间作用量 $J=\oint p\,dx = 2\pi E/\omega$（数值/解析相对残差 $1.4\times10^{-16}$）；Virial 时间均分 $\langle T\rangle=\langle V\rangle=E/2$（相对差 $3.0\times10^{-15}$）。

---

## 二、对偶映射：不是一张表，而是两套约定（重要补强）

| | 机械 | **阻抗型类比**（力↔电压） | **导纳型类比**（力↔电流） |
|---|---|---|---|
| 广义坐标 | 位移 $x$ | 电荷 $q$（串联 LC） | 磁通链 $\lambda=\int V dt$（并联 LC） |
| 广义速度 | $v=\dot x$ | 电流 $I=\dot q$ | 电压 $V$ |
| 广义力 | $F$ | 电压 $V$ | 电流 $i$ |
| 惯性项 | $m$ | $L$ | $C$ |
| 刚度项 | $k$ | $1/C$ | $1/L$ |
| $\omega^2$ | $k/m$ | $(1/C)/L = 1/(LC)$ | $(1/L)/C = 1/(LC)$ |

**精算 B3/B4**：导纳型下并联方程 $C\ddot V + V/L = 0$ 与机械方程归一化后逐项同形（差 `simplify = 0`）；两条路径给出的 $\omega^2$ 代数恒等 $=1/(LC)$。

> **BOUNDARY B5（对偶映射是约定，不是物理断言）**
> 同一个质量 $m$：在阻抗型类比里映到 $L$（惯性），在导纳型类比里映到 $C$（惯性）；
> 同一个电感 $L$：在阻抗型里是惯性，在导纳型里是柔度 $1/k$。
> 换一套约定，映射就翻转——它不是可被实验判定的命题。用户原表中「$m$ 对应 $L$」只在阻抗型约定内成立。

> **INFO B6**：串联 LC 与并联 LC 互为对偶（$L\leftrightarrow C$、$q\leftrightarrow\lambda$、$1/C\leftrightarrow 1/L$），这是电路层面的电–磁对偶，与场论 $E\leftrightarrow B$ 对偶同构，属已知结构。

---

## 三、量纲审计：形式同构 ≠ 量纲同一（本册最硬的一条）

以量纲向量 $[M,L,T,I]$ 审计（精算 C1–C4）：

- **PASS**：两套方程各自量纲自洽（$m\ddot x$ 与 $kx$ 同为力；$L\ddot q$ 与 $q/C$ 同为电压）；$\omega^2=K/A$ 同为 $T^{-2}$。
- **BOUNDARY C3**：$[m]/[L] = M^0L^{-2}T^{2}I^{2}\neq 1$，$[k]/[1/C] = M^0L^{-2}T^{2}I^{2}\neq 1$。
- **PASS C4**：阻抗型类比必须引入两个带量纲的标定常数
  $F=\alpha V \Rightarrow [\alpha]=L^{-1}TI$；$v=\beta I \Rightarrow [\beta]=LT^{-1}I^{-1}$；
  机械阻抗 $[F/v]=MT^{-1}$ 与电阻抗 $[V/I]=ML^{2}T^{-3}I^{-2}$ 相差 $[\alpha/\beta]=L^{-2}T^{2}I^{2}$。

**结论**：可以写「在选定标定常数后，$m$ 与 $L$ 在方程中占据同一个结构槽位」，**不能**写「$m$ 就是 $L$」——后者在量纲上不成立。

---

## 四、相对论修正：修正成立，但**对偶在此断裂**

### 4.1 推导（精算 D1–D3）

$$\frac{d}{dt}(\gamma v) = \gamma^3 a \quad\Rightarrow\quad m\gamma^3\ddot x + kx = 0$$

能量 $E=(\gamma-1)mc^2+\tfrac12kx^2$，代入 EOM 后 $\dot E=0$（符号验证 `simplify = 0`）。

弱相对论展开 $\gamma^3 \approx 1+\tfrac32 v^2/c^2$ 给出
$\ddot x + \omega_0^2 x\left(1-\tfrac32 \dot x^2/c^2\right)=0$。
Lindstedt 谐波平衡（取 $x=A\cos\omega t$，令 $\cos\theta$ 系数为零）：

$$A(\omega_0^2-\omega^2) = \tfrac38\,\frac{\omega_0^2\omega^2A^3}{c^2}
\;\Longrightarrow\;
\omega^2 = \frac{8c^2\omega_0^2}{3A^2\omega_0^2+8c^2}
\;\Longrightarrow\;
\omega \simeq \omega_0\left[1-\frac{3}{16}\left(\frac{v_0}{c}\right)^2\right]$$

**精算 D4**：RK4 实测周期，对 $A=0.01\ldots0.08$ 的 $\delta\equiv(T/T_0-1)/(v_0/c)^2$ 作 $(v/c)^2$ 线性外推，**截距 $=0.18749966$**，与 $3/16=0.1875$ 差 $3.4\times10^{-7}$。周期随振幅增大而变长（非线性特征）。

### 4.2 负结论（BOUNDARY D5，本册最重要的边界）

- 机械侧：存在速度上限 $c$，EOM 变非线性，频率依赖振幅。
- 电磁侧：集总 LC 是**准静态近似**，电荷无速度上限，不存在「相对论 LC 方程」；一旦回路尺度接近 $c/\omega$，必须改用分布参数传输线
  $\partial^2 V/\partial x^2 = LC\,\partial^2 V/\partial t^2$——**方程从 ODE 变成 PDE，自由度无限**，与单自由度振子不再同构。

**机电对偶的严格作用域：非相对论 + 集总（波长 ≫ 回路尺度）。**「同一个振荡结构贯穿力学与电磁」在相对论/高频 regime 不成立。

---

## 五、量子化：形式逐字平行，实验极不对称

### 5.1 两套正则量子化（精算 E1–E5）

$$[x,p]=i\hbar,\; H=\frac{p^2}{2m}+\tfrac12 m\omega^2x^2 \qquad
[\phi,q]=i\hbar,\; H=\frac{q^2}{2C}+\frac{\phi^2}{2L}$$

| 项 | 机械 | LC 回路 | 精算结果 |
|---|---|---|---|
| 对易关系 | $[x,p]=i\hbar$ | $[\phi,q]=i\hbar$ | 误差 $1.2\times10^{-14}$ |
| 能谱 | $\hbar\omega(n+\tfrac12)$ | $\hbar\omega(n+\tfrac12)$ | 前 20 级相对残差 $<7\times10^{-16}$ |
| 基态 Virial | $\langle T\rangle=\langle V\rangle=\hbar\omega/4$ | 同 | 机器零 |
| 零点涨落 | — | $\phi_{\rm zpf}=\sqrt{\hbar Z/2},\; q_{\rm zpf}=\sqrt{\hbar/2Z},\;Z=\sqrt{L/C}$ | 与 $\tfrac12\hbar\omega$ 自洽 |

相空间环面积 $J=2\pi E/\omega$ 配合 Bohr–Sommerfeld $J=2\pi\hbar(n+\tfrac12)$ 直接给出同一能谱（精算 G2）。

### 5.2 可达性审计（精算 E6/E7）

| 系统 | 频率 | $\hbar\omega/k_B$ |
|---|---|---|
| 超导 LC（1 nH / 100 fF） | 15.9 GHz | **0.764 K** |
| transmon 典型 | 5 GHz | 0.240 K |
| 纳米机械 | 1 GHz | 0.048 K |
| MEMS | 10 MHz | $4.8\times10^{-4}$ K |
| 宏观弹簧（1 g / 100 N/m） | 50.3 Hz | **$2.4\times10^{-9}$ K** |

> **BOUNDARY E7**：数学上两套量子化逐字平行；实验上相差 **8.5 个数量级**（比值 $3.2\times10^8$）。
> 只有超导/纳米体系能进入 $\hbar\omega\gg k_BT$ 的量子区；宏观机械振子的对偶量子态原则上存在、实践上不可达。
> **形式同构不能推出「两者在实验中是同一个东西」。**

---

## 六、把同构变成可测量：耦合劈裂（唯一有实验内容的部分）

引入机电耦合能 $U_{\rm int}=g\,x\,q$（压电/电容式换能、腔光力学的线性化极限）：

$$m\ddot x + kx + gq = 0,\qquad L\ddot q + \tfrac1C q + gx = 0$$

特征方程 $(k-m\omega^2)(1/C-L\omega^2)=g^2$。在简并 $\omega_0^2=k/m=1/(LC)$ 时：

$$\omega_\pm^2 = \omega_0^2 \pm \frac{g}{\sqrt{mL}},\qquad
\bar E_{\rm mech}(t) \simeq E_0\cos^2\!\left(\frac{\Delta\omega}{2}t\right),\quad T_{\rm beat}=\frac{2\pi}{\Delta\omega}$$

| 精算项 | 结果 |
|---|---|
| F1 劈裂闭式 vs 数值本征值 | 一致（机器零） |
| F2 非简并四阶特征方程 vs 数值 | 一致 |
| F3 避免交叉 $\Delta\omega_{\rm coupled} > \lvert\omega_a-\omega_b\rvert_{\rm bare}$ | $0.1052 > 0.0483$ ✔ |
| F4 总能量守恒 | 漂移 $3.0\times10^{-14}$ |
| F5 拍频节点 $t^\*=\pi/\Delta\omega$ 处能量包络归零 | $\bar E(t^\*)/E_0 = 2.7\times10^{-3}$ ✔ |

**诚实细节（非 bug）**：瞬时 $E_{\rm mech}$ 在包络节点并不精确为零——$x=0$ 但 $\dot x=-\delta\cos(\bar\omega t)\sin(\delta t)\neq0$，残余动能 $\sim\tfrac12\delta^2$（实测 $4.6\times10^{-4}$，理论 $6.3\times10^{-4}$）。故用**对快振荡的滑动平均包络**判定转移，而非瞬时值。

> **BOUNDARY F7**：该劈裂是腔光力学/压电的标准 avoided crossing，实验早已观测，**不是新预言**。它的意义在于：这才是「两个系统真实耦合」的判据——**若无 $g$ 项，两个 $\omega$ 恰好相等也只是数值巧合**；形式同构推不出任何物理联系。

---

## 七、涡旋与拓扑

- **G1** 相空间 $(x,\,v/\omega)$ 轨道闭合，绕数 $W=1$（一周期后回到起点，偏差 $2\times10^{-17}$）。
- **G2** 环面积 $J=2\pi E/\omega=2\pi\hbar(n+\tfrac12)$，与 §E 对角化能谱同一。
- **G3/G4** 2D 振子：频率比 $1{:}1$、$2{:}1$、$1{:}2$ 轨道闭合（偏差 $<3\times10^{-14}$）；无理比 $1{:}\varphi$ 不闭合（偏差 $0.42$，对照组证明判据非恒真）。
- **G5** 两条 Hopf 纤维的 Gauss 链环积分 $Lk=-1.0000000000$（$|Lk|=1$，中点法 $1200\times1200$）。

> **BOUNDARY G6**：TUFT 中 $Lk$ 的角色（$Lk$ 宇称 ⟹ 自旋–统计）来自 Chern–Simons Wilson 环期望值 $\langle W_1W_2\rangle=e^{-2\pi i Lk/k}$（Witten 1989）。本册只是把同一数学对象搬到相空间 $S^1$ 纤维上；相空间纤维绕数恒为 1，**不携带**粒子量子数。二者等同需要额外输入，本册不给（沿用 R10 的 O-LCS-NORM：不同归一化层禁止断言等价）。

> **BOUNDARY G7（禁止等同）**：TUFT 的 $\Omega=\sqrt{\kappa^2+\tau^2}$（世界线螺旋的 Frenet 角频率）与 SHO 的 $\omega$（动力学振荡频率）量纲同为 $T^{-1}$ 但语义不同。若强行令 $\omega=\Omega$，由 $m=\hbar\Omega/c^2$ 与 $E=\hbar\omega$ 得 $E=mc^2$——这只是普朗克–爱因斯坦关系与质能等价的**复合重述**，不是 TUFT 独有的导出；且 $\Omega$ 的绝对标度需外部锚定（O-SCALE / D3：$K_{\rm sat}$ 无第一性推导，Planck 值与电子尺度差 $5.7\times10^{44}$）。

---

## 八、对「通用本源方程」的审查

$$A\ddot\phi + K\phi = 0,\qquad E=\tfrac12 A\dot\phi^2+\tfrac12 K\phi^2$$

- **H1 自由度审计**：$(A,K)$ 两个参数，可测量只有比值 $K/A$ 一个——整体缩放 $(A,K)\to(\lambda A,\lambda K)$ 下轨迹**逐点相同**（数值验证到 $10^{-12}$）。所以整个「本源方程」能给出的数只有 $\omega$。
- **H2 双锚点检验失败**：由 $(m,k)$ 推不出 $(L,C)$（只能给 $LC$ 之积）；反之亦然。跨系统**零定量预测力**。

> **BOUNDARY C5/H3**：「宇宙底层是同一个振荡结构」等价于「存在无阻尼二阶线性方程」，其全部可测后果只有一个 $\omega$。按第一性判据，属 **L0/L1 重述层**，不是可证伪的物理断言。
> 机电类比的正确定位是**计算工具**（用电路模拟机械、反之亦然，有真实工程价值）；把它上升为「宇宙本源结构」超出其可证伪范围。

---

## 九、本册三条主结论

1. **经典层（§A/§B）**：用户给出的推导链**全部正确**——两套系统的能量求导、守恒、振荡解、$\omega$ 闭式、作用量、Virial 均通过，机器零级。补强两点：对偶有**两套约定**（阻抗型 $m\leftrightarrow L$ / 导纳型 $m\leftrightarrow C$），且需**两个带量纲标定常数**；因此「$m$ 就是 $L$」是约定不是物理命题。
2. **修正层（§D/§E）**：相对论修正（$\delta=+3/16$，外推截距 $0.18749966$）与量子化（同一 $E_n$、同一零点涨落）在两套系统中**形式上平行**；但相对论 regime 下对偶**断裂**（ODE→PDE），量子化实验可达性相差 **8.5 个数量级**。
3. **本体论层（§C/§H）**：$A\ddot\phi+K\phi=0$ 只有一个可测量 $\omega$，跨系统零定量预测力。它是优秀的**计算模板**，不是可证伪的宇宙本源命题。唯一把同构变成可测量的途径是引入真实耦合项 $g\,x\,q$（§F），而该劈裂是已知物理，非新预言。

---

## 十、边界与开放项清单

| 编号 | 内容 | 级别 |
|---|---|---|
| B5 | 对偶映射是约定（两套类比并存） | BOUNDARY（不可证伪） |
| C3/C4 | 类比需量纲标定常数，「$m=L$」量纲不成立 | BOUNDARY |
| C5/H3 | 「同一振荡结构」无跨系统定量预测力 | BOUNDARY（L0/L1） |
| D5 | 相对论/高频 regime 对偶断裂（ODE→PDE） | BOUNDARY（负结论） |
| E7 | 量子层形式平行、实验差 8.5 量级 | BOUNDARY |
| F7 | 劈裂为已知物理（腔光力学/压电） | BOUNDARY（L2，非新预言） |
| G6 | Hopf 链环与 TUFT $Lk$ 是数学借用 | BOUNDARY |
| G7 | $\Omega$ 与 $\omega$ 禁止等同（需尺度锚定） | BOUNDARY（O-SCALE/D3 遗留） |
| B6 | 集总版电–磁对偶为已知结构 | INFO |

**未闭合、本册不冒充已闭合**：$\Omega$ 的绝对标度（O-SCALE）、$K_{\rm sat}$ 无第一性推导（D3）、代质量层级（需外部 Yukawa 输入）。红线：以上均为诚实边界，非证伪宣告，也非 TUFT 的新成就。
