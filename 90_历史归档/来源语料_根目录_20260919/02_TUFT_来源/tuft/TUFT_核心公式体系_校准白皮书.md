# TUFT 核心公式体系 —— 校准白皮书（v1.0）

> **依据**：openuft TUFT 语料链 R1–R28、OPEN-5 / OPEN-6 / OPEN-7、$\sigma_\text{abs}=0$ ringdown v2 / v3 / v4、
> 以及本白皮书专门的校准册 **R29**（口径校准 + 结构判定）与 **R30**（求导符号验真 + 三个新判定 + 全维度总结）
> **日期**：2026-09-30　**实跑环境**：Python 3.8.8 + sympy 1.13.3 + numpy 1.24.3 + mpmath 1.3.0
> **红线**：数学自洽 ≠ 实验证实。本白皮书不作 TUFT 框架整体的证伪宣告；所有结论均标注实算出处，可独立复算。

---

## 0. 前置约定

| 符号 | 定义 | 量纲 |
|---|---|---|
| $\kappa$ | 时空标曲率（螺旋世界线 Frenet 第一曲率） | $L^{-1}$ |
| $\tau$ | 挠率标量（螺旋 Frenet 第二曲率 / 挠率） | $L^{-1}$ |
| $\omega$ | 场螺旋本征角频率 | $T^{-1}$ |
| $\rho_C$ | 康普顿半径 $\hbar/(mc)$ | $L$ |
| $\alpha$ | 精细结构常数（**外部测量锚**，非 TUFT 导出） | 无量纲 |

**几何实现**：圆柱螺旋 $r(t)=(a\cos t,\,a\sin t,\,bt)$；场载体为挠率流形 ≅ 爱因斯坦–嘉当（EC）联络。

**诚实分层**（全书通用）：[A] 严格证明 / [B] 框架映射（借用外部输入）/ [C] 无依据假设 / TAUT 定义回代。

---

## 1. 校准后的核心公式体系（唯一版本）

### 1.1 公理 A 及其几何实现 ★（本白皮书唯一的正向收获）

$$\boxed{\kappa^2+\tau^2=\frac{\omega^2}{c^2}}\tag{公理 A}$$

代入 S12 严格几何确立的电子螺旋 $a=\alpha\rho_C,\; b=\rho_C\sqrt{1-\alpha^2}$ 与 Frenet 闭式 $\kappa=\frac{a}{a^2+b^2},\tau=\frac{b}{a^2+b^2}$，得**显式闭式**（R30 §3，sympy 精确 0）：

$$\boxed{\kappa=\frac{\alpha}{\rho_C}=\frac{\alpha\,m_ec}{\hbar},\qquad \tau=\frac{\sqrt{1-\alpha^2}}{\rho_C}=\frac{\sqrt{1-\alpha^2}\,m_ec}{\hbar}}$$

并自动闭合到康普顿频率：

$$\kappa^2+\tau^2=\frac{1}{\rho_C^2}\ \Longrightarrow\ \omega=\frac{c}{\rho_C}=\frac{m_ec^2}{\hbar}=7.7634\times10^{20}\ \mathrm{rad/s}$$

**电子数值**（可独立复算）：

| 量 | 值 |
|---|---|
| $\rho_C=\hbar/m_ec$ | $3.861593\times10^{-13}$ m |
| $\kappa_e$ | $1.889726\times10^{10}\ \mathrm{m^{-1}}$ |
| $\tau_e$ | $2.589536\times10^{12}\ \mathrm{m^{-1}}$ |
| $\kappa_e/\tau_e$ vs $\tan\theta$ | $7.2975468740\times10^{-3}$ **恒等** |
| $\sqrt{\kappa_e^2+\tau_e^2}\cdot\rho_C$ | $1.000000000000000$ |

⚠️ **方向地雷（R29 §1）**：严格几何给 $\dfrac{\kappa}{\tau}=\tan\theta=\dfrac{\alpha}{\sqrt{1-\alpha^2}}$，即 $\dfrac{\tau}{\kappa}=\dfrac{\sqrt{1-\alpha^2}}{\alpha}=137.0324\approx 1/\alpha$。
白皮书系的「$\alpha=\tau/\kappa$」方向写反，**相差 $(1/\alpha)^2=1.878\times10^{4}$ 倍**。凡以 $\tau/\kappa$ 代入 $\alpha$ 处的公式，数值全错。

### 1.2 场方程（修正版）

$$R_{\mu\nu}-\tfrac12 R g_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\,T_{\mu\nu}[\kappa,\tau,\omega]$$

修正点：$\Lambda$ 与右侧 $\propto g_{\mu\nu}$ 的项**不可分离**（见 1.3）；因此上式应理解为含组合 $\Lambda_\text{eff}$ 的有效方程，不得声称"$\Lambda$ 由几何导出"。

### 1.3 能动张量（修正版 · 带不可辨识警告）

$$T_{\mu\nu}=\alpha(\kappa,\omega)\,\kappa\,g_{\mu\nu}+\beta(\tau,\omega)\,\tau\,S_{\mu\nu}$$

**新增警告（必须保留）**：第一项与 $\Lambda g_{\mu\nu}$ 同型，合并后只有

$$\Lambda_\text{eff}=\Lambda-8\pi G\,\alpha\kappa$$

可观测 ⇒ **故声称「$\Lambda$ 由孤子几何导出」属定义回代（TAUT）**。因 $S^{\mu\nu}$ 反对称、$g^{\mu\nu}$ 对称，二者在张量空间正交，$\beta\tau$ 项不参与该简并。

### 1.4 守恒律（修正版 · 这是本白皮书最重要的修正）

联络差闭式（$K=\Gamma^{(\mathrm{EC})}-\Gamma^{(\mathrm{LC})}$ 为 contortion 张量）：

$$\boxed{\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}=\nabla^{(\mathrm{LC})}_\mu T^{\mu\nu}+\underbrace{K^\mu{}_{\mu\lambda}T^{\lambda\nu}+K^\nu{}_{\mu\lambda}T^{\mu\lambda}}_{=:F^\nu}}$$

**判定（R29 §2，实算）**：映射 $K\mapsto F^\nu$ 在 24 维 / 64 维 $K$ 空间上 **rank 恒为 4**（三种 $T^{\mu\nu}$ 形态一致）⇒ $F^\nu=0$ 是余维 4 的零测度约束面；**2000 组随机 contortion 100.0% 给出 $\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}\neq0$**。

> ❌ 原稿陈述「由场方程 + 公理 A 可推出 $\nabla^\mu T_{\mu\nu}=0$」**不成立**。
> ✅ 正确陈述：守恒成立需**附加 4 个 contortion 代数约束**；唯一自动成立的分支是 $K\equiv0$（挠率为零）且 $\alpha\kappa$ 时空常数（回归 GR）。

---

## 2. 求导证明与验真（R30 §1，sympy 符号级）

| 编号 | 求导链 | 实算结果 | 判定 |
|---|---|---|---|
| **D1** | $\nabla_\mu(\kappa^2+\tau^2)=\nabla_\mu(\omega^2/c^2)\Rightarrow\kappa\nabla_\mu\kappa+\tau\nabla_\mu\tau=\frac{\omega}{c^2}\nabla_\mu\omega$ | 4 个 $\nu$ 分量残差全为 0；代入 $\omega=c\sqrt{\kappa^2+\tau^2}$ 后自动化简为 0 | **PASS（信息量为零）** |
| **D2** | 稳态 $\nabla_\mu\omega=0\Rightarrow\partial_\mu(\kappa^2+\tau^2)=0\Rightarrow\omega=cR$ 常数 | $\kappa=R\cos\varphi,\tau=R\sin\varphi$ 对任意 $\varphi$ 恒等 | **PASS** |
| **D3** | $-\frac{g}{4}=-\frac12(1+\tau/\kappa)\Rightarrow g-2=2\tau/\kappa$ | sympy 解得 $g=2(1+\tau/\kappa)$ | **代数 PASS / 物理 FAIL** |
| **D4** | $\partial^2\Im[\omega_\text{QNM}]/\partial\tau^2$ 稳定判据 | 无可用映射 | **FAIL 不可验真** |

**D1 的诚实判读**：该式是**约束自身的链式法则推论**——任何 $f^2+g^2=h^2$ 型关系都自动满足。它可以写成一个"证明"，但**不含超出公理 A 的物理信息**，不得当作理论成立的证据。

**D4 的概念错位**：R20–R22 的 $\omega_\text{QNM}$ 是 **GR Regge–Wheeler/Zerilli 势 + 人为反射壁 $r_s$** 的谱，自变量为 $(r_s,M)$，**不是** $(\kappa,\tau)$；TUFT 从未给出 $\omega_\text{QNM}(\kappa,\tau)$ 闭式，且 OPEN_v4 已证 $r_s=2.05M$ 不可导出 ⇒ 该映射**不可构造**，二阶导数无从求导。

---

## 3. 四个实验 / 可检验窗口的最终状态

| 窗口 | 源口径（唯一有源） | 精算结果 | 最终判定 |
|---|---|---|---|
| **g−2** | OPEN-5：$a_\text{TUFT}=\alpha/(8\pi)$ | $2.904\times10^{-4}$ ⇒ $g-2=5.807\times10^{-4}$（**−74.96%** vs $a_e^\text{exp}=1.1597\times10^{-3}$） | **被实验否决** |
| **EDM** | OPEN-6：$d_e=\dfrac{e\alpha R_C}{2\sqrt{1+\alpha^2}}$ | $2.257\times10^{-34}$ C·m $=1.409\times10^{-13}$ e·cm，超 **ACME 2018**（$1.1\times10^{-29}$ e·cm）$\mathbf{1.28\times10^{16}}$ 倍 | **被实验否决** |
| **β 跑动** | OPEN-7：固定螺旋 $g=\kappa/\tau$ | **$\beta\equiv0$**（无 RG 流） | 边界判定 |
| **ringdown** | v2 两难 → v3 → v4 | v3 $\chi^2=33.00(\mathrm{df}=2),\,p=6.83\times10^{-8},\,5.74\sigma$，MCMC n=19200；v4 三尺度锚与所需 $r_s=2.05M$ 差 **26~78 量级** | **窗口关闭** |

**EDM 的二层否决（比"偏大"更彻底）**：书籍第52章判定该式的推导依赖 $\langle z\rangle=b/2$ 固定偏移，属 **[C] 类无依据假设**；而螺旋对称性的严格论证给出 $d_e=0$（40 万点采样旁证）。⇒ 该"预言"本身**不应存在**。

**附带勘误**：白皮书引用的「ACME $8.7\times10^{-34}$ C·m」$=5.430\times10^{-13}$ e·cm，**比真实上限宽松 $4.94\times10^{16}$ 倍**；凡以该数字判"未排除"的结论一律作废。（此条同时作废了一条历史 memory 中的旧判断。）

**$\beta\equiv0$ 的三路交叉闭环**（R30 §2–§3，这是本轮的方法论收获）：

1. OPEN-7：$g=\kappa/\tau$ 为无量纲常数 ⇒ $\beta\equiv0$
2. R30 §2：稳态 + 螺旋约束 ⇒ $\kappa,\tau$ 各自常数 ⇒ $\beta\equiv0$
3. R30 §3：$\kappa=\alpha m c/\hbar,\ \tau=\sqrt{1-\alpha^2}mc/\hbar$ 显式闭式 ⇒ 无残余 $\mu$ 自由度 ⇒ $\beta\equiv0$

⇒ 说明 TUFT 的 $\beta\equiv0$ **不是漏加了 RG**，而是几何量已被 $(m,\alpha)$ 完全定死的必然后果。

---

## 4. 三个结构缺口 + 四条同源边界

### 4.1 三个结构缺口

| 编号 | 内容 | 实算支撑 |
|---|---|---|
| **EC-CONSERVE** | $\nabla^{(\mathrm{EC})}\cdot T=0$ 需附加 4 个 contortion 约束 | rank=4；随机 $K$ 100% 不成立 |
| **EC-CONSERVE-TUNE** | Cartan（挠率↔自旋）与守恒律相容需 fine-tuning | 最一般假设 $K=W\cdot S$：300 组随机 $W$ **100% 不相容**；允许的 $K$-系数构成 $\mathbb{R}^{24}$ 中 **20 维（余维 4）子空间**，非零测度不可达 |
| **Λ-NONIDENT** | $\Lambda$ 与 $\alpha\kappa$ 结构不可辨识 | 单锚 $\mathrm{rank}(J)=1$ |

### 4.2 四条同源边界（同一事实的四个来源）

$$\text{O-SCALE}\;=\;\text{D3}(K_\text{sat})\;=\;\text{定理 N M2}\;=\;\text{O-SCALE-BREAK}$$

⇒ **TUFT 没有第一性尺度**，并由此伴生「无 RG 流」与「Λ 不可分离」。

`O-SCALE-BREAK` 的精确表述（诚实二分）：
- **情形 A 单锚 $m_e$**：$\kappa$ 唯一 ⇒ $\mathrm{rank}=1$ ⇒ **数学上不可能破简并**
- **情形 B 借用多锚 $(m_e,m_p,m_\mu)$**：$\mathrm{rank}=2$ ⇒ 可破简并，但**代价是输入多个外部粒子质量**（与 OPEN-7「借用标准 RGE 才升 [A]」同构）

---

## 5. 全维度总结表

| 条目 | 精算结果 | 判定 | 备注 |
|---|---|---|---|
| 窗口1 g−2 | $5.807\times10^{-4}$（−74.96%） | **被实验否决** | 整理稿 $\mu_e$ 式全仓无源 |
| 窗口2 EDM | 超 ACME $1.28\times10^{16}$ | **被实验否决** | [C] 类假设；对称性给 $d_e=0$ |
| 窗口3 β 跑动 | $\beta\equiv0$ | 边界判定 | 三路独立推导同结果 |
| 窗口4 ringdown | $5.74\sigma$；差 26~78 量级 | **窗口关闭** | 非 TUFT 可导出 |
| 结构 D1 | 残差 0 | PASS（无新信息） | 链式法则推论 |
| 结构 D2 | $\omega=$ 常数 | PASS | 与康普顿频率闭合 |
| 结构 D4 | 无闭式 | **不可验真** | 概念错位 |
| EC-CONSERVE | 需 4 约束 | **FAIL** | 随机 $K$ 100% 不成立 |
| EC-CONSERVE-TUNE | 100% 不相容 | **FAIL** | 需 fine-tuning |
| Λ-NONIDENT | rank=1 | **FAIL** | 破简并不可能 / 须借用 |
| **收获** | $\kappa,\tau,\omega$ 干净闭式 | **PASS** | **唯一可正向引用** |

---

## 6. 对外陈述建议（可说 / 不可说）

**可说（有实算支撑）**
- 给定 $(m,\alpha)$ 后，$\kappa,\tau,\omega$ 有一组自洽闭式，并与康普顿频率闭合
- $\beta\equiv0$ 有三路独立推导，是 TUFT 内稳健结论
- $\kappa/\tau=\tan\theta$ 与 $\sin\theta=\alpha$ 严格自洽（机器零）

**不可说（已被实算或实验关闭）**
- ❌ "由场方程可推出 $\nabla^\mu T_{\mu\nu}=0$"（需 4 个额外约束）
- ❌ "$\Lambda$ 由孤子几何导出"（TAUT / 不可辨识）
- ❌ 直接用 $\tau/\kappa$ 代入 $\alpha$（差 $1.878\times10^4$ 倍）
- ❌ "g−2 / EDM 待检验"（两者已被实验否决）
- ❌ "ringdown 是唯一开放窗口"（已被 v3+v4 定量关闭）
- ❌ 把 D1 的链式法则恒等式当作"理论成立的证明"

**准确定位**：$\text{[B] 级有效编码} + \text{已关闭的实验窗口}$ ⇒ **不得作为已完成的第一性理论对外陈述**。

---

## 附录 A · 订正对照表（整理稿 → 校准后）

| 条目 | 整理稿 | 校准后（本白皮书） |
|---|---|---|
| g−2 | $\mu_e=-\frac{e\hbar}{2m}(1+\tau/\kappa)\Rightarrow g-2=2\tau/\kappa=0.00404$ | $a=\alpha/(8\pi)\Rightarrow g-2=5.807\times10^{-4}$（−74.96%）；$\mu_e$ 式全仓无源 |
| EDM | $d_e=\gamma\kappa\tau\frac{e\hbar}{m_ec}$ | $d_e=\frac{e\alpha R_C}{2\sqrt{1+\alpha^2}}$，且该式属 [C] 类、对称性给 $0$ |
| β | $\beta=b_0g^3+b_1g^5+\delta_\text{TUFT}$，缺口 $\Delta\beta\neq0$ | **$\beta\equiv0$**（无跑动），方向相反 |
| ringdown | 缺 $\chi^2$ metric，L3 OPEN | v3 $\chi^2=33.00/5.74\sigma$、v4 尺度冲突 ⇒ **已关闭** |
| 守恒律 | $\nabla^\mu T_{\mu\nu}=0$ | $\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}=\nabla^{(\mathrm{LC})}_\mu T^{\mu\nu}+F^\nu$，需 4 个附加约束 |

## 附录 B · 数值常数（CODATA 近似）

$\alpha=1/137.035999084$　$\hbar=1.054571817\times10^{-34}$ J·s　$m_e=9.1093837015\times10^{-31}$ kg　$c=299792458$ m/s
$a_e^\text{exp}=1.15965218073\times10^{-3}$　ACME 2018 $\lvert d_e\rvert<1.1\times10^{-29}$ e·cm　$1\ \mathrm{e\cdot cm}=1.602176634\times10^{-21}$ C·m

## 附录 C · 产物索引

| 产物 | 路径（均在 openuft/90_历史归档/来源语料_根目录_20260919/02_TUFT_来源/tuft/） |
|---|---|
| R29 脚本 / 报告 / 文稿 | `tuft_r29_核心公式口径校准与结构可行性.py` / `tuft_r29_report.txt` / `tuft_R29_核心公式口径校准与结构可行性_文稿.md` |
| R30 脚本 / 报告 / 文稿 | `tuft_r30_求导证明验证与全维度总结.py` / `tuft_r30_report.txt` / `tuft_R30_求导证明验证与全维度总结_文稿.md` |
| 上游链路 | `tuft_g2_电子反常磁矩_OPEN5.py`、`tuft_EDM_实验对接_OPEN6.py`、`tuft_beta_running_缺口_定理N实例化.py`、`tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py`、`tuft_sigma_abs0_ringdown_定量metric_OPEN_v3.py`、`tuft_sigma_abs0_尺度锚定冲突_OPEN_v4_report.txt` |
| R31 脚本 / 报告 / 文稿 | `tuft_r31_两条主线可行性与缺陷审计.py` / `tuft_r31_report.txt` / `tuft_R31_两条主线审计与修正方案_文稿.md`（CMB 嵌套采样 + QNM FDTD/PML 两条主线的审计，C/L2） |
| 索引 / 归一化 | `tuft_总索引.md`、`tuft_第一性归一化总览.md`（r29=C/L2，r30=O/L2，r31=C/L2） |

**R31 对本白皮书的两点补强**：
1. **「TUFT 无 CMB 双谱」已有量化凭证**：`tuft_暴胀CMB_report.txt` 评级 **C / L1，计数 5/35/8/10（35 项 FAIL）** ⇒ f_NL 类原初谱计算在 TUFT 内无可用第一性结果。
2. **「无 RG 流」再次被独立印证**：R31 审计的 CMB 嵌套采样方案以「拓扑跃迁能标 $t_c=\ln(\mu_c/M_\text{Pl})$」为核心采样参数，而本白皮书 §3 已证 $\beta\equiv0$ ⇒ 该参数在 TUFT 内**无定义**（R31 判为致命理论冲突）。

复跑方式：`python tuft_r29_核心公式口径校准与结构可行性.py` 与 `python tuft_r30_求导证明验证与全维度总结.py`（随后跑 `tuft_总索引.py` 刷新索引）。

---

> **红线声明**：数学自洽 ≠ 实验证实。本白皮书所有负结论均为「公式不成立 / 口径不一致 / 已被实验或数据排除」的实判定，
> **不构成对 TUFT 框架整体的证伪宣告**；1.1 节的 $\kappa,\tau,\omega$ 闭式与 $\beta\equiv0$ 三路闭环是真实的正收获，但其正确性与"该理论描述自然"是两件不同的事。
