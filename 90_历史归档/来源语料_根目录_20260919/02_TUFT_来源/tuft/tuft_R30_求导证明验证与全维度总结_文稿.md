# TUFT-R30 文稿：求导证明验证 · 三个新判定 · 全维度总结

> 评级建议：**O / L2**（PASS=7 / FAIL=4 / BOUNDARY=1 / INFO=2；4 项 FAIL 全为「公式/判据不可成立或不可验真」的实判定）
> 脚本：`tuft_r30_求导证明验证与全维度总结.py`　报告：`tuft_r30_report.txt`
> 依赖实跑：sympy 1.13.3 / numpy 1.24.3 / mpmath 1.3.0

---

## 0. 本册做了什么

承接 R29 的口径校准，正面完成**求导 symbol 验证**，并得出三个此前 TUFT 体系内从未处理过的新判定，
最后收敛为一张全维度坐标表。

红线：**数学自洽 ≠ 实验证实**。本册不构成对 TUFT 框架整体的证伪宣告。

---

## 1. 求导链的符号验真（必读：哪些"证明"其实不含信息）

### D1｜公理 A 的协变微分 —— **PASS，但信息量为零**

sympy 逐分量（4 个 $\nu$）验证：

$$\frac{\partial}{\partial x^\nu}\!\left(\kappa^2+\tau^2-\frac{\omega^2}{c^2}\right)-2\Big[\kappa\partial_\nu\kappa+\tau\partial_\nu\tau-\tfrac{\omega}{c^2}\partial_\nu\omega\Big]=0$$

残差 **全为 0**。进一步把约束解出 $\omega=c\sqrt{\kappa^2+\tau^2}$ 代入，表达式**自动化简为 0**。

> **必须诚实指出**：这正是**链式法则的直接结果**，是这个约束关系自身的微分推论，
> **不含任何超出公理 A 的物理信息**。它可以被写成"第一条证明"，但不能被当作"理论成立的证据"——
> 任何形如 $f^2+g^2=h^2$ 的关系都自动满足该式。

### D2｜稳态条件 —— **PASS**

取参数化 $\kappa=R\cos\varphi(x),\ \tau=R\sin\varphi(x)$（$R$ 常数，$\varphi$ 任意时空函数）：

$$\kappa^2+\tau^2=R^2,\qquad \partial_\nu(\kappa^2+\tau^2)=0\ \ (\forall\nu)$$

⇒ $\nabla_\mu\omega=0\Rightarrow\omega=cR=$ 常数。**稳态条件与公理 A 相容**，且与 §3 的康普顿频率闭合一致。

### D3｜g−2 联立消去 —— **代数 PASS / 物理 FAIL（分项）**

sympy 解 $-\frac{g}{4}=-\frac12(1+\tau/\kappa)$ 得 $g=2(1+\tau/\kappa)$，即 $g-2=2\tau/\kappa$ —— **代数无误**。

但前提式 $\mu_e=-\frac{e\hbar}{2m}(1+\tau/\kappa)$ 在 openuft 全仓**无来源**，且 $\tau/\kappa$ 存在
$1.878\times10^4$ 倍的方向歧义（R29 模块 C）。⇒ **代数自洽 ≠ 物理可用**，不得引用其数值结果。

### D4｜ringdown 二阶判据 —— **FAIL：不可验真（概念错位）**

整理稿写作 $\omega_\text{QNM}(\kappa,\tau)$ 并对 $\tau$ 求一/二阶导数。但 **R20–R22 的 $\omega_\text{QNM}$ 是
GR Regge–Wheeler/Zerilli 势 + 人为反射壁 $r_s$ 的谱，自变量是 $(r_s,M)$，不是 $(\kappa,\tau)$**。
TUFT 从未给出任何 $\omega_\text{QNM}(\kappa,\tau)$ 闭式，且 OPEN_v4 已证 $r_s=2.05M$ 不可由 TUFT 导出
⇒ 该映射**不可构造**，二阶导数判据无从求导。

---

## 2. 新判定①：稳态 + 螺旋约束 ⇒ **第二次得到 $\beta\equiv0$**

联立两条常数条件

$$\text{(i) }\kappa^2+\tau^2=\text{const}\quad(\text{D2})\qquad \text{(ii) }\frac{\kappa}{\tau}=\tan\theta=\text{const}\quad(\text{R29 §1})$$

sympy 解得 $\kappa=\dfrac{\sqrt{S}\,r}{\sqrt{1+r^2}},\ \tau=\dfrac{\sqrt{S}}{\sqrt{1+r^2}}$（$S=\kappa^2+\tau^2,\ r=\kappa/\tau$）
⇒ $\kappa,\tau$ **各自**为常数 ⇒ $\partial\kappa/\partial\mu=\partial\tau/\partial\mu=0\Rightarrow\beta\equiv0$。

这与 OPEN-7 的路径（$g=\kappa/\tau$ 为无量纲常数 ⇒ $\beta\equiv0$）**独立同源**，相互印证。

---

## 3. 新判定②：$\kappa,\tau$ 的**显式闭式** —— 第三次 $\beta\equiv0$，且给出可引用数值

由 S12 严格几何 $a=\alpha\rho_C,\ b=\rho_C\sqrt{1-\alpha^2}$ 代入 Frenet 闭式：

$$\boxed{\kappa=\frac{\alpha}{\rho_C}=\frac{\alpha\,m_ec}{\hbar},\qquad \tau=\frac{\sqrt{1-\alpha^2}}{\rho_C}=\frac{\sqrt{1-\alpha^2}\,m_ec}{\hbar}}$$

sympy 检验 $\sqrt{\kappa^2+\tau^2}-1/\rho_C=0$（**精确 0**，因 $\alpha^2+1-\alpha^2=1$），与公理 A 自动相容。

**电子数值**（这是目前 TUFT 体系内唯一一组"有明确闭式 + 有数值 + 与标准量吻合"的几何量）：

| 量 | 值 |
|---|---|
| $\rho_C=\hbar/m_ec$ | $3.861593\times10^{-13}$ m |
| $\kappa_e=\alpha/\rho_C$ | $\mathbf{1.889726\times10^{10}\ m^{-1}}$ |
| $\tau_e=\sqrt{1-\alpha^2}/\rho_C$ | $\mathbf{2.589536\times10^{12}\ m^{-1}}$ |
| $\kappa_e/\tau_e$ vs $\tan\theta$ | $7.2975468740\times10^{-3}$ **（恒等）** |
| $\sqrt{\kappa_e^2+\tau_e^2}\cdot\rho_C$ | $1.000000000000000$ |

⇒ **$\kappa,\tau$ 被 $(m,\alpha)$ 唯一锁定，无残余 $\mu$ 自由度** ⇒ $\beta\equiv0$（第三次，且是闭式层面的证明）。

> 这条同时**解释了 OPEN-7 的 $\beta\equiv0$ 为何不是偶然**：不是"忘了加 RG"，而是"几何量已被完全定死"。

---

## 4. 新判定③（模块 A2）：Cartan 方程与守恒律的 **fine-tuning 矛盾**

R29 已证 $F^\nu:=K^\mu{}_{\mu\lambda}T^{\lambda\nu}+K^\nu{}_{\mu\lambda}T^{\mu\lambda}$ 的映射 $K\mapsto F^\nu$ 满秩 4。
但 EC 中 $K$ 并不自由：Cartan 方程把挠率（⇒contortion）与自旋源代数绑定。

取所有 EC 版本的共同点作为**最一般假设**：$K$ 与轴张量 $S$ 之间存在线性对应 $K=W\cdot S$
（$S$ 有 6 个独立分量，$K$ 有 24 个 ⇒ $W$ 为 $24\times6$ 矩阵）。随机扫描：

| 检验 | 结果 |
|---|---|
| 300 组随机 $W$ 下 $F^\nu\neq0$ 比例 | **100.0%**（$\\|F\\|$ 中位 $4.794$） |
| 使 $F\equiv0$ 的 $K$-系数子空间 | $\mathbb{R}^{24}$ 中 **20 维**（余维 4），非空 |

⇒ $W\cdot S$ 需命中 $\mathbb{R}^{24}$ 中一个**余维 4 的子空间**，在随机 $W$ 下为**零测度事件**。

**结论（新登记开放项 `EC-CONSERVE-TUNE`）**：TUFT 若要同时主张「挠率来自物质」与「$\nabla^{(\mathrm{EC})}_\mu T^{\mu\nu}=0$」，
必须额外给出这份精细调节机制；当前未提供 ⇒ 这是继「Λ 不可辨识」之后的**第三个结构性缺口**。

---

## 5. 新判定④（模块 B2）：Λ–ακ 破简并 —— **不可能 vs 可借用**（第四同源边界）

由 §3 闭式 $\kappa_i=\alpha\,m_ic/\hbar$ ⇒ 不同的 $\kappa_i$ ⇔ 不同的**质量锚** $m_i$。必须诚实分两情形：

| 情形 | 雅可比 | rank | 判定 |
|---|---|---|---|
| **A · 单一锚 $m_e$** | $[1,\ -8\pi G\kappa_e]$ | **1** | **数学上不可能破简并**：$\Lambda_\text{eff}=\Lambda-8\pi G\alpha\kappa$ 永远不可分离 |
| **B · 借用多个外部质量锚**（$m_e,m_p,m_\mu$） | 三行 | **2** | 可破简并，但**代价是输入多个外部粒子质量** |

⇒ 情形 B 与 OPEN-7 §4「借用标准 RGE 才升 [A]」**同构**：破简并必须以外部锚为输入，
因此 Λ 与 $\alpha\kappa$ 的分离不是 TUFT 第一性导出，而是**借用**。

**登记第四同源边界：`O-SCALE-BREAK`**（破简并须外部多锚）。

---

## 6. 四条同源边界正式收敛

$$\text{O-SCALE（尺度秩=1 须外部锚）}\;=\;\text{D3（}K_\text{sat}=1/\ell_P^2\text{ 手写普朗克锚）}\;=\;\text{定理 N M2（尺度生成缺第一性）}\;=\;\text{O-SCALE-BREAK}$$

四处独立来源指向**同一个结构性事实**：**TUFT 没有第一性尺度，也没有与之伴生的 RG 流与 Λ 分离能力**。

---

## 7. 全维度总结表

| 条目 | 精算结果 | 判定 | 备注 |
|---|---|---|---|
| 窗口1 g−2 | $\alpha/(8\pi)\Rightarrow g-2=5.807\times10^{-4}$（−74.96%） | **被实验否决** | 整理稿的 $\mu_e$ 式全仓无源 |
| 窗口2 EDM | $d_e=1.409\times10^{-13}$ e·cm，超 ACME $1.28\times10^{16}$ 倍 | **被实验否决** | [C] 类假设；对称性严格给 $d_e=0$ |
| 窗口3 β 跑动 | $\kappa,\tau$ 由 $(m,\alpha)$ 锁定 ⇒ $\beta\equiv0$ | 边界判定 | **三次独立推导同结果** |
| 窗口4 ringdown | v3 $\chi^2=33.00$、$5.74\sigma$；v4 差 26~78 量级 | **窗口关闭** | $\sigma_\text{abs}=0$ 非 TUFT 可导出 |
| 结构 D1 公理A微分 | 链式法则恒等，残差 0 | PASS（无新信息） | 属约束的微分推论 |
| 结构 D2 稳态 | $\kappa^2+\tau^2=$ const ⇒ $\omega=$ const | PASS | 与康普顿频率闭合 |
| 结构 D4 ringdown 二阶 | $\omega_\text{QNM}(\kappa,\tau)$ 无闭式 | **不可验真** | 整理稿概念错位 |
| 结构 A 守恒律 | 需 4 个 contortion 约束 | **FAIL** | 随机 $K$ 100% 不成立 |
| 结构 A2 Cartan 相容 | 随机线性对应 100% 不相容 | **FAIL** | `EC-CONSERVE-TUNE` |
| 结构 B Λ 不可辨识 | rank=1（单锚） | **FAIL** | 破简并不可能 / 须借用 |
| **收获 · 公理A闭合** | $\omega=m_ec^2/\hbar=7.763\times10^{20}$ rad/s | **PASS** | **唯一可正向引用的结论** |

---

## 8. TUFT 准确定位（R29 + R30 联合收口）

- **可用**：给定 $m$ 与 $\alpha$ 后，把自旋/统计/频率编码为几何——一个自洽的**编码框架**；
  且 $\kappa=\alpha m c/\hbar,\ \tau=\sqrt{1-\alpha^2}\,mc/\hbar$ 与 $\omega=m_ec^2/\hbar$ 组成一组干净闭式。
- **不可用**：作为产生低能预言的理论——没有 RG 流、没有第一性尺度、Λ 不可分离、
  四条实验/可检验窗口三条已被否决、一条被定量关闭。
- **全局定位**：$\text{[B] 级有效编码} + \text{已关闭的实验窗口}$ ⇒ **不得作为已完成的第一性理论对外陈述**。

> **红线声明**：数学自洽 ≠ 实验证实。本册加固边界而非推翻，不改变 R1–R29 的模型内数值自洽性。
>
> 数学结果的正确性（例如 $\beta\equiv0$ 的三路交叉闭环、$\kappa/\tau=\tan\theta$ 的机器零）是**真实的收获**；
> 它与"该理论描述自然"是两件不同的事。
