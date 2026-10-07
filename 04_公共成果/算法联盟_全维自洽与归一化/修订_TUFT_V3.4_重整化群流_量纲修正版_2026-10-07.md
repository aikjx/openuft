# 修订 · TUFT V3.4 重整化群流（β_G, β_c）与能标跑动 · 量纲修正版

> 本文是《TUFT V3.4：重整化群流与能标跑动》的整理+修正版。相对来料：
> - **D1** ω 代数修正（补 $c^2$）；
> - **D2** ω 量纲更正（是力不是角频率）；
> - **D3** κ+τc 量纲三重不匹配，标注待 X-EXT-5 修复（同源第十九轮 O-V34-C）；
> - **D4** β_τ 三项量纲不齐，标注待补量纲；
> - **D5** β_G 链式法则保留但附注分母非法。
> 机器核验见 `源码/TUFT_V34_RG_ω与β_量纲审计与修正_2026-10-07.py`（自检 4/4）。

---

## 1. 基本设定（保留）
重整化群：耦合常数随能标 $\mu$ 跑动，$\beta_g=\mu\,dg/d\mu$。
TUFT 核心假设：$G$ 是局域场，随截断能标演化；$c$ 在高能存在微小跑动。

耦合关系：
$$
G(\mu)=\frac{c(\mu)^4}{8\pi\big(\kappa(\mu)+\tau(\mu)c(\mu)\big)}
$$
取对数对 $\ln\mu$ 求导得（**形式正确，D5**）：
$$
\boxed{\;\beta_G=G\left(\frac{4\beta_c}{c}-\frac{\beta_{\kappa\tau}}{\kappa+\tau c}\right)\;},\qquad
\beta_c=\mu\frac{dc}{d\mu},\ \beta_{\kappa\tau}=\mu\frac{d(\kappa+\tau c)}{d\mu}
$$
> ⚠️ **D3**：分母 $\kappa+\tau c$ 在来料内三套量纲（弧长倒数 / 力 / 频率）互相矛盾、不可相加。本式在 D3 修复前仅是形式记号，不能数值化。建议走 X-EXT-5（R1 零成本改写 / R2 定值场 / R3 ECSK）后再用。

### 弱场低能极限（保留）
$\tau\to0$，$\beta_{\kappa\tau}\approx\mu\,d\kappa/d\mu$；不动点 $\beta_G\to0,\beta_c\to0$，$(G,c)$ 近似常数。

### 普朗克高能区（保留叙述，删「显著偏离零」的定量断言）
$\kappa\sim\tau c$ 时 $\beta_{\kappa\tau}$ 不可忽略。⚠️ 因 D3，$\beta_G$ 当前无合法数值，不能宣称「引力耦合开始跑动」的定量结论。

---

## 2. 挠率场 β 函数（D4 修正）
$$
\boxed{\;\beta_\tau=\mu\frac{d\tau}{d\mu}=-\eta\tau+\alpha\tau^2+\frac{\hbar}{c^2}\mu^2\;}
$$
> ⚠️ **D4**：三项量纲不齐（机器断言：$-\eta\tau\sim L^{-1}T^{-1}$，$\alpha\tau^2\sim L^{-2}$，$\hbar\mu^2/c^2\sim M^3T^{+1}$）。在显式声明 $[\eta],[\alpha],[\mu]$ 之前，这不是齐次 RG 方程。物理图像（低能耗散、近 Planck 挠率被真空涨落激发）**叙述保留**，但量级比较需补量纲。

---

## 3. 球对称静态孤子 ODE 边值问题（D1/D2 修正）
边界条件、径向关系（保留）：
$$
\tau(r)=\frac{\omega\ell_P^2}{c r^2},\qquad \kappa(r)=\Lambda_0-\frac{\omega\ell_P^2}{r^2}
$$
视界条件 $\kappa(r_s)=0$ 给出 $\omega=\Lambda_0\,r_s^2/\ell_P^2$。代入 $r_s=2GM/c^2$、$\Lambda_0=c^4/(8\pi G)$、$\ell_P^2=\hbar G/c^3$：

**修正后的代数结果（D1，来料少 $c^2$）**：
$$
\boxed{\;\omega_{\text{alg}}=\frac{c^3M^2}{2\pi\hbar}\;}
$$
$G$ 在代数上消去 ⇒ 「ω 不含 G」**这句本身为真**。

**但（D2，关键）**：量纲 $[\omega_{\text{alg}}]=M\,L\,T^{-2}$（力），**不是角频率**（$T^{-1}$）。来料式 $[cM^2/\hbar]=M\,L^{-1}$ 同样不是频率。
⇒ 「TUFT 静态球对称孤子**本征角频率**」「质量越大周期越短」的解读**不成立**。

> 诚实备选：若要坚持「角频率」，唯一与 TUFT 结构相容的自然频率是光穿越频率 $\omega_{\text{lc}}=c/r_s=c^3/(2GM)$，量纲 $T^{-1}$ 但**含 $G$** —— 直接否定「ω 不含 G」。⇒ 「不含 G」与「是角频率」**不可兼得**，须二选一。

对应「周期」$T=2\pi/\omega$ 同样不是时间，删除原推论。

---

## 4. 引力波微扰方程（保留结构，删未证伪断言）
在背景上加扰动，TT 规范下：
$$
\square h_{\mu\nu}=\frac{2}{\bar\kappa+\bar\tau c}\big(\delta T_{\mu\nu}+\delta\kappa\,g_{\mu\nu}+c\,\delta\tau\,g_{\mu\nu}\big)
$$
- 远场退化为 $\square h_{\mu\nu}=16\pi G/c^4\,\delta T_{\mu\nu}$（与 GR/LIGO 一致）；
- 近核心 $\delta\tau$ 贡献额外分量（「挠率极化模」仍是 TUFT 独有预言的方向，但其幅度依赖 β_τ、ω 二者，当前均受 D2/D4 影响，定量待修）。

相位修正 $\Delta\Phi\propto\int\delta\tau\,dr$ 叙述保留，量级待 β_τ 量纲修复。

---

## 5. CMB 双谱与原初非高斯性（保留）
总扰动 $\zeta_{\text{total}}=\zeta+\zeta_\tau$，双谱 $B_{\text{total}}=B_{\text{GR}}+B_\tau$，正交型形状保留。
> 注：用 Planck 对 $f_{\text{NL}}$ 的限制约束挠率自耦合 $\alpha$ 的链路**成立的前提**是 β_τ（第 2 节）量纲合法；在 D4 修复前，$f_{\text{NL}}^\tau$ 与 $\alpha$ 的定量关系暂不闭合。

---

## 6. 下一阶段路径（门禁，非来料）
四条路径（能量动量守恒 / 拉氏量 / LIGO 波形 / 量子 TUFT）**全部依赖第 3、4 节的 ω 与 β**，在 D2/D3/D4 未修前**阻塞**。前置顺序：
1. 修 D3（选 X-EXT-5 路线使 κ+τc 量纲合法）；
2. 修 D4（声明 β_τ 各项量纲）；
3. 重做 ω（「不含 G 的形式量」或「含 G 的真实频率」二选一）；
4. 闭环后回路径，优先路径 3（最可证伪）。

---

*红线：数学自洽 ≠ 实验证实。本修订只修正量纲与代数错误，不宣称任何新物理预言。*
