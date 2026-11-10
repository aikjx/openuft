# P11 · Strongly Coupled Matter: the KSS Viscosity Bound and the QCD Running Coupling

**中文题名：强耦合物质——KSS 粘滞下界与 QCD 跑动耦合的求导与精算**

**Authors:** Guozi Mo (莫国子)^1,\*

**Affiliation:** ^1 墨行科技（江门 / 佛山），中国；\* Corresponding author.

**Date:** 2026-11-09 · **Series:** Unified-Field Breaching Papers, P11 of 13

---

## Abstract

Two numbers define the modern picture of strongly coupled matter: the shear-viscosity-to-entropy ratio bound $\eta/s\ge\hbar/(4\pi k_B)$, and the one-loop QCD beta function that makes the strong coupling fall with energy. We derive both from their generating structures — the holographic shear-mode absorption cross-section for the first, the renormalization-group equation for the second — and evaluate them in 60-digit arithmetic. The KSS bound is $6.078312\times10^{-13}$ K s, with the experimentally inferred QGP value sitting at 1–2 times this floor. The QCD coefficients are exact rationals: $b_0=11-2N_f/3$ gives $7$ at $N_f=6$ and $23/3$ at $N_f=5$; $b_1=102-38N_f/3$ gives $26$ at $N_f=6$. A one-loop estimate with $\Lambda_{\overline{\rm MS}}=200$ MeV yields $\alpha_s(M_Z)=0.1466$, quoted explicitly as an order-of-magnitude check rather than a prediction, because the two-loop value used in P1 is $0.1161$ after GUT-boundary back-running. The distinction between "exact rational coefficient" and "scheme-dependent estimate" is stated, not blurred.

**摘要：** 两个数字定义了强耦合物质的现代图像：剪切粘滞-熵比下界 $\eta/s\ge\hbar/(4\pi k_B)$，以及使强耦合随能标下降的单圈 QCD β 函数。本文分别从其生成结构求导——全息剪切模吸收截面与重整化群方程——并以 60 位算术取值。KSS 下界为 $6.078312\times10^{-13}$ K·s，实验反推的 QGP 值落在此下限的 1–2 倍。QCD 系数为精确有理数：$b_0=11-2N_f/3$ 在 $N_f=6$ 时给 $7$、$N_f=5$ 时给 $23/3$；$b_1=102-38N_f/3$ 在 $N_f=6$ 时给 $26$。取 $\Lambda_{\overline{\rm MS}}=200$ MeV 的单圈估计给出 $\alpha_s(M_Z)=0.1466$，本文明确将其标为“量级检查”而非预言——P1 中经 GUT 边界回推的两圈值为 $0.1161$。本文把“精确有理系数”与“方案依赖估计”分开陈述，不混为一谈。

---

## 1. Introduction

量子色动力学（QCD）有两个极端：高能区耦合小、可用微扰；低能区耦合大、只能靠格点或全息。前者给出 β 函数的精确有理系数，后者给出 $\eta/s$ 的近普适下界。把这两个极端放在同一篇文章里，是因为它们共享同一个逻辑：**系数的来源是可写的，数值的大小是口径依赖的**。本文的结构就是把“可写死的部分”和“口径依赖的部分”分栏列出。

## 2. Results

### 2.1 求导链 I：KSS 下界的来源

**Step 1（全息设定）.** 在 $AdS_{d+1}$ 黑洞背景中，边界场论的剪切粘滞由引力子横向极化模的吸收截面决定。

**Step 2（截面）.** 对 $AdS_4$（对偶 $2+1$ 维场论），$\sigma_{\rm abs}=\hbar/k_B$ 的极化平均给出

$$
\frac{\eta}{s}=\frac{\hbar}{4\pi k_B}.
$$

**Step 3（数值）.** $\hbar=1.0545718176\times10^{-34}$ J s、$k_B=1.380649\times10^{-23}$ J K⁻¹：

$$
\frac{\eta}{s}=\frac{1.0545718176\times10^{-34}}{4\pi\times1.380649\times10^{-23}}=6.078312\times10^{-13}\ \mathrm{K\,s}.
$$

**Step 4（实验对照）.** RHIC/LHC 的流体力学反演给 QGP 的 $\eta/s$ 为 $1$–$2$ 倍 KSS 值（legacy C0282，守卫 3/3）。

**Step 5（性质）.** 该下界是**普适**的：不依赖耦合强度、不依赖 $N_c$，只依赖全息对偶的几何。这正是它成为“近完美流体”判据的原因。

### 2.2 求导链 II：QCD β 函数

**Step 1（定义）.**

$$
\beta(g)=-\frac{g^3}{16\pi^2}b_0-\frac{g^5}{(16\pi^2)^2}b_1-\cdots
$$

**Step 2（单圈系数）.** 对 $SU(N_c)$ 带 $N_f$ 味：

$$
b_0=\frac{11}{3}N_c-\frac{2}{3}N_f\ \xrightarrow{N_c=3}\ 11-\frac{2N_f}{3}.
$$

**Step 3（两圈系数）.**

$$
b_1=34-\frac{13N_f}{3}\ \text{(scheme-dependent form)}\ \Rightarrow\ 102-\frac{38N_f}{3}\ \text{(standard normalization)}.
$$

**Step 4（读数）.** $N_f=6$：$b_0=7$、$b_1=26$；$N_f=5$：$b_0=23/3\approx7.667$（E11.2–E11.4）。全部为精确有理数，无近似。

**Step 5（跑动）.** 单圈解

$$
\alpha_s(\mu)=\frac{4\pi}{b_0\ln(\mu^2/\Lambda^2)} .
$$

取 $\Lambda=200$ MeV、$\mu=M_Z$ 得 $\alpha_s=0.1466$（E11.5）——仅为量级检查；两圈回推值见 P1（$0.1161$，与实测 $0.1184$ 差 $2.0\%$）。

### 2.3 精算读数表

| 量 | 闭式 | 读数 | 来源 | 性质 |
|---|---|---|---|---|
| $\eta/s_{\min}$ | $\hbar/(4\pi k_B)$ | **$6.078312\times10^{-13}$ K s** | E11.1 | 普适下界 |
| QGP $\eta/s$ | 实验反演 | **$(1\text{–}2)\times$KSS** | E11.6 | 近完美流体 |
| $b_0(N_f=6)$ | $11-2N_f/3$ | **7**（精确） | E11.2 | 精确有理 |
| $b_0(N_f=5)$ | 同上 | **$23/3$** | E11.3 | 精确有理 |
| $b_1(N_f=6)$ | $102-38N_f/3$ | **26** | E11.4 | 精确有理 |
| $\alpha_s(M_Z)$ 单圈 | $4\pi/b_0\ln(\mu^2/\Lambda^2)$ | **0.1466** | E11.5 | 量级检查，非预言 |
| $\alpha_s(M_Z)$ 两圈+回推 | P1 引擎 | **0.1161** | CUNI-v2 | 与实测 0.1184 差 2.0% |

## 3. Discussion

**两个“精确”与一个“估计”.** $b_0$、$b_1$ 是精确有理数，可以写死；$\eta/s_{\min}$ 是普适常数，也可以写死；而 $\alpha_s(M_Z)$ 的具体数值依赖 $\Lambda$ 与圈数，属于估计。把三者放在同一张表里，是为了让读者一眼看出“哪一栏可以拿去检验理论、哪一栏只能拿去对口径”。

**与 P1 的衔接.** P1 的 GUT 回推给出 $\alpha_s(M_Z)=0.1161$（实测 $0.1184$，差 $2.0\%$），这是本系列中唯一把强耦合当作“可预言量”的地方。本模块的单圈值 $0.1466$ 与它相差 $26\%$，正是“圈数不足”的代价——这也解释了为什么 P1 必须走两圈+阈值匹配，而不能停在单圈。

**与 TUFT 的关系.** TUFT 未给出任何 QCD β 系数或 $\eta/s$ 闭式（18 条必要条件供给 0），故本项为结构性负面闭合的一部分。

## 4. Methods

常数：$\hbar$、$k_B$ 取 CODATA 2018；$N_c=3$；$\Lambda_{\overline{\rm MS}}=200$ MeV 为示例输入（非拟合）。mpmath 60 位；有理数用 Fraction 校验；容差逐条列于 JSON。

## 5. Figure legends

**Fig. 11 | Strong-coupling diagnostics.** (a) 单圈 $\alpha_s^{-1}(\mu)$ 两条路径：虚线为纯 SM（$b_0=23/3$）从 $M_Z$ 外推至 $1.69\times10^{16}$ GeV，得到 $\alpha_s^{-1}=48.3$，不汇聚；实线为 MSSM 三段有效斜率，恰好落在金点 $\alpha_{\rm GUT}^{-1}=25.827$。两条路径的分离即为「为何需要超对称」的图面证据。(b) 单圈 β 系数对照：SM（$N_f=3,4,5,6$ 对应 $b_0=9,\,25/3,\,23/3,\,7$，均大于零）与 MSSM（$b_1=33/5,\ b_2=1,\ b_3=-3$，$\alpha_3$ 的系数转负）。全部图内文字为英文（DejaVu Sans + mathtext），无 CJK 字形依赖，故无缺字形（乱码）风险。

## 6. Data & Code Availability

- 精算锚点：`verify_papers_P6_P13_精算验证_2026-11-09.py`（E11.1–E11.6）
- 既有判定册：`判定_C0282_QGP粘滞熵比攻破_2026-10-21.md`
- P1 两圈回推：`attack_力的大统一方程_CUNI-v2_GUT边界回推验证_2026-10-30.json`
- 图：`figures/Fig11_QCD_running_EN.png`

## 7. Author Contributions

G.M. 完成两条求导链、口径分栏与全文。

## 8. Competing Interests

作者声明无竞争性利益。

## References

1. Kovtun, P. K., Son, D. T. & Starinets, A. O. Viscosity in strongly interacting quantum field theories from black hole physics. *Phys. Rev. Lett.* **94**, 111601 (2005).
2. Policastro, G., Son, D. T. & Starinets, A. O. The shear viscosity of strongly coupled N=4 supersymmetric Yang–Mills plasma. *Phys. Rev. Lett.* **87**, 081601 (2001).
3. Gross, D. J. & Wilczek, F. Ultraviolet behavior of non-Abelian gauge theories. *Phys. Rev. Lett.* **30**, 1343–1346 (1973).
4. Politzer, H. D. Reliable perturbative results for strong interactions? *Phys. Rev. Lett.* **30**, 1346–1349 (1973).
5. Adams, A., Chesler, P. M. & Liu, H. Holographic vortex liquids and superfluid turbulence. *Phys. Rev. Lett.* **112**, 151602 (2014).
