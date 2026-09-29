# TUFT-R29 文稿：核心公式体系的口径校准与两个内生结构问题

> 评级建议：**C / L2**（含 8 项 FAIL，均为「公式不成立或口径不一致」的实判定，非 TUFT 框架证伪宣告）
> 脚本：`tuft_r29_核心公式口径校准与结构可行性.py`　报告：`tuft_r29_report.txt`
> 汇总：**PASS=4 / FAIL=8 / BOUNDARY=1 / INFO=3**

---

## 0. 本册定位

本册**不做新的实验拟合**，只处理一件事：把一份整理稿中的公式体系，用 openuft 现存的源脚本逐条校准，
并对其中两个从未被处理过的**内生结构问题**给出可算判定。

红线：**数学自洽 ≠ 实验证实**。本册所有结论均为「公式是否成立 / 是否需要额外假设」的判定，
**不构成对 TUFT 框架整体的证伪宣告**，也不否定 R1–R28 的模型内数值自洽性。

---

## 1. 模块 C（前置）：τ/κ 的方向地雷

### 1.1 严格 Frenet 给出的是 κ/τ，不是 τ/κ

圆柱螺旋 $r(t)=(a\cos t,\,a\sin t,\,bt)$ 的严格不变量：

$$\kappa=\frac{a}{a^2+b^2},\qquad \tau=\frac{b}{a^2+b^2},\qquad \kappa^2+\tau^2=\frac{1}{a^2+b^2}$$

代入 S12 裁决确立的电子螺旋几何 $a=R=\alpha\rho_C,\; b=\rho_C\sqrt{1-\alpha^2}$（由 $\sin\theta=\alpha$ 导出）：

$$\frac{\kappa}{\tau}=\frac{a}{b}=\frac{\alpha}{\sqrt{1-\alpha^2}}=\tan\theta$$

数值回算残差 **0.00e+00（机器零）**，与 S12 裁决完全一致。

### 1.2 地雷：白皮书系的 $\alpha=\tau/\kappa$ 方向写反

| 项 | 值 |
|---|---|
| 严格 $\tau/\kappa$ | $137.032350$ |
| $1/\alpha$ | $137.035999$ |
| 白皮书主张的 $\alpha$ | $7.2974\times10^{-3}$ |
| **二者相差** | $\mathbf{1.8778\times10^{4}\;\approx\;(1/\alpha)^2}$ |

⇒ **任何把 $\tau/\kappa$ 当作 $\alpha$ 使用的公式，数值错 $1.88\times10^4$ 倍**。凡要在 g−2、耦合常数处使用 $\tau/\kappa$，必须先做此裁决。

### 1.3 附带闭合（本册唯一正向收获）

公理 A 在该几何下自动闭合：

$$\kappa^2+\tau^2=\frac{1}{\rho_C^2}\;\Longrightarrow\;\frac{\omega}{c}=\frac{1}{\rho_C}\;\Longrightarrow\;\omega=\frac{m_ec^2}{\hbar}=7.7634\times10^{20}\ \mathrm{rad/s}$$

即**公理 A 在螺旋几何下等价于「频率 = 康普顿角频率」**，无自由参数。这是本链条上第一处把约束式与可观测量真正对接上的节点，建议后续对外陈述以此为准。

---

## 2. 模块 A：$\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}=0$ 不是场方程推论

### 2.1 联络差闭式

令 $K=\Gamma^{(\mathrm{EC})}-\Gamma^{(\mathrm{LC})}$ 为 contortion 张量（差是张量，故可直接写）：

$$\boxed{\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}=\nabla^{(\mathrm{LC})}_\mu T^{\mu\nu}+\underbrace{K^\mu{}_{\mu\lambda}T^{\lambda\nu}+K^\nu{}_{\mu\lambda}T^{\mu\lambda}}_{=:F^\nu}}$$

$F^\nu$ 对 $K$ **线性** ⇒ 把 $K\mapsto F^\nu$ 看作线性映射，$F^\nu\equiv0$ 的解空间维数由秩决定。

### 2.2 实算：秩 = 4 ⇒ 需 4 个额外约束

在一点的局部惯性系（$g=\eta$）计算；因 $T,K$ 为张量、$F$ 为矢量，该映射的秩在可逆坐标变换下不变，结论坐标无关。

| $T^{\mu\nu}$ 形态 | $K$ 空间 | dim | **rank** | nullity |
|---|---|---|---|---|
| $\alpha\kappa\,g$ 主导 | 一般 $K$ | 64 | **4** | 60 |
| $\alpha\kappa\,g$ 主导 | 后两指标反对称 | 24 | **4** | 20 |
| $\beta\tau\,S$ 主导 | 一般 $K$ | 64 | **4** | 60 |
| $\beta\tau\,S$ 主导 | 后两指标反对称 | 24 | **4** | 20 |
| 混合典型 | 反对称 | 24 | **4** | 20 |

**满秩 4** ⇒ $F^\nu=0$ 是余维 4 的代数约束面（在 24 维 $K$ 空间中为零测度）。
$2000$ 组随机 contortion 采样：**100.0% 给出 $\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}\neq0$**（$\|F\|$ 中位 $4.44$）。

### 2.3 结论与唯一自动成立的分支

- **FALSE**：「由场方程 + 公理 A 可推出 $\nabla^\mu T_{\mu\nu}=0$」——不是恒等式，须附加 4 个独立代数约束。
- **TRUE**：$K\equiv0$（挠率为零）且 $\alpha\kappa$ 时空常数时自动守恒（回归 GR）。

⇒ **「TUFT 协变闭环」应改述为「TUFT 附加守恒假设」**。若坚持原陈述，必须显式列出使 $F^\nu\equiv0$ 的那 4 个约束，
并检查它们是否与 Cartan 方程（$\text{扭率}\propto\text{自旋源}$）相容。

---

## 3. 模块 B：$\alpha\kappa\,g_{\mu\nu}$ 与 $\Lambda g_{\mu\nu}$ 的结构不可辨识

场方程合并同型项：

$$G_{\mu\nu}+\bigl[\Lambda-8\pi G\,\alpha\kappa\bigr]g_{\mu\nu}=8\pi G\,\beta\tau\,S_{\mu\nu}$$

因 $S^{\mu\nu}$ 反对称、$g^{\mu\nu}$ 对称，二者在张量空间**正交**，$\beta\tau$ 项不参与简并；退化只发生在 $\Lambda$ 与 $\alpha\kappa$ 之间。

以 $s=\Lambda-8\pi G\alpha\kappa$ 为可观测量，对 $\theta=(\Lambda,\alpha)$ 求雅可比：

| 情形 | 雅可比 | rank | 判定 |
|---|---|---|---|
| 单值 $\kappa$ | $[1,\,-8\pi G\kappa]$ | **1** | **不可辨识**（仅 1 个可测组合，1 个退化方向） |
| 多值 $\kappa=[1,2.5,7]$ | 三行 | **2** | 可辨识（充要条件：$\kappa_i$ 已知且互异） |

⇒ 声称「$\Lambda$ 由孤子几何导出」在单 $\kappa$ 下是**定义回代（TAUT）**。
破简并的充要条件是「≥2 个不同 $\kappa$ 的同型观测 + $\kappa_i$ 数值已知」，而 TUFT 现无第一性 $\kappa(\mu)$ 剖面
（**O-SCALE 锚定定理 / D3 $K_\text{sat}$ 审计 / 定理 N M2** 三处同源结论）⇒ **简并不能被真正打破**。

⇒ 本模块把「TUFT 无第一性尺度」从 RG 层（$\beta\equiv0$）**推广到宇宙学常数层**。

---

## 4. 四条实验窗口的口径校准表

| 窗口 | 源脚本口径 | 外稿口径 | 处置 |
|---|---|---|---|
| g−2 | $a_\text{TUFT}=\alpha/(8\pi)=2.904\times10^{-4}$ ⇒ $g-2=5.807\times10^{-4}$（**−74.96%**） | $\mu_e=-\frac{e\hbar}{2m}(1+\tau/\kappa)$ ⇒ $g-2=2\tau/\kappa=0.00404$ | **无源**，且与三条候选路径全部不符：$2\alpha\to1.459\times10^{-2}$(+529%)、$2/\alpha\to2.741\times10^{2}$(+1.18e7%)。唯一有源口径为 $\alpha/(8\pi)$ |
| EDM | $d_e=\dfrac{e\alpha R_C}{2\sqrt{1+\alpha^2}}=1.409\times10^{-13}$ e·cm，超 ACME $1.28\times10^{16}$ 倍 | $\gamma\kappa\tau\frac{e\hbar}{m_ec}$（$\gamma$「由公理A固定」无源） | **公式无源**；且第52章判该式依赖 $\langle z\rangle=b/2$ 属 [C] 类假设、螺旋对称性严格给 $d_e=0$ ⇒ 比「偏大」更彻底 |
| β 跑动 | $g=\kappa/\tau$ 无量纲常数 ⇒ $\partial g/\partial\mu=0$ ⇒ **$\beta\equiv0$** | $\beta=b_0g^3+b_1g^5+\delta_\text{TUFT}$，缺口 $\Delta\beta\neq0$ | **方向相反**：源结论是「无跑动」，不是「跑动有缺口」；M1/M2/M3=0/0/1 |
| ringdown | v2 两难 → **v3** $\chi^2=33.00(\mathrm{df}=2),\,p=6.83\times10^{-8},\,5.74\sigma$，MCMC n=19200 → **v4** 三尺度锚差 26~78 量级 | 「缺 $\chi^2$ metric，L3 ⚠OPEN」 | **已过时两代**：$\chi^2$ 已完成且 $>5\sigma$ 排除；v4 从可导出性上关闭窗口（$\sigma_\text{abs}=0$ 非 TUFT 可导出结构） |

附带勘误：白皮书引用的「ACME $8.7\times10^{-34}$ C·m」$=5.430\times10^{-13}$ e·cm，**比真实上限宽松 $4.94\times10^{16}$ 倍**；
凡以该数字判「未排除」的结论全部作废。

---

## 5. 对上层陈述的建议措辞（诚实版）

1. **公理 A** $\kappa^2+\tau^2=\omega^2/c^2$：可保留，且在第 1.3 节的几何下与康普顿频率闭合 ✅
2. **守恒律**：改写为「在附加 4 个 contortion 约束（或挠率为零）时成立」，不可写成场方程推论
3. **$\Lambda$**：不可写成由几何导出，只能写成 $\Lambda_\text{eff}=\Lambda-8\pi G\alpha\kappa$ 的一个反问题
4. **$\tau/\kappa$**：禁止单独使用，使用前必须标注采用的是 $\kappa/\tau=\tan\theta$ 口径
5. **四条窗口**：三条已无 OPEN 状态（g−2、EDM 被实验否决；ringdown 被定量关闭），β 为边界判定

---

> **红线声明**：数学自洽 ≠ 实验证实。本册判定的是公式成立条件与口径一致性，
> TUFT 仍可作为一个「给定 $m_e$ 后把质量/自旋/统计编码为几何」的有效框架存在；
> 本册未对其作整体证伪宣告。
