# 延伸方向 E｜黎曼张量的代数对称性、Bianchi 恒等式与独立分量数

> 全程严格区分 **数学定义 / 代数恒等式证明 / 本体论解释**；签名 \((+,-,-,-)\)。
> 本文全部恒等式由 `verify_extension_derivation.py` 的 **E 组**在**具体度规上精确复算**（2 维球面、3 维共形平直、4 维 Schwarzschild），见文末 E.9。
> **红线**：本文核验的是**数学恒等式**（由定义推出），**不是**新的物理预言。

---

## E.0 约定

与专题任务 1 一致：

\[
R^\rho_{\ \sigma\mu\nu}
=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}
\]

\[
R_{\rho\sigma\mu\nu}=g_{\rho\lambda}R^\lambda_{\ \sigma\mu\nu},\qquad
R_{\mu\nu}=R^\sigma_{\ \mu\sigma\nu},\qquad
R=g^{\mu\nu}R_{\mu\nu}
\]

（脚本 E2、E18 明确核验了缩并约定与专题 T1 一致：2 维球面上给出 \(\mathrm{Ric}=Kg\)，即 \(n-1=1\) 倍。）

---

## E.1 四条代数对称性

对**任意**度规（无挠 + 度规相容），全下指标黎曼张量满足：

\[
\boxed{
\begin{aligned}
&\text{(S1)}\quad R_{\rho\sigma\mu\nu}=-R_{\sigma\rho\mu\nu}\qquad &&\text{前对反对称}\\
&\text{(S2)}\quad R_{\rho\sigma\mu\nu}=-R_{\rho\sigma\nu\mu}\qquad &&\text{后对反对称}\\
&\text{(S3)}\quad R_{\rho\sigma\mu\nu}=+R_{\mu\nu\rho\sigma}\qquad &&\text{块交换对称}\\
&\text{(S4)}\quad R_{\rho\sigma\mu\nu}+R_{\rho\mu\nu\sigma}+R_{\rho\nu\sigma\mu}=0\qquad &&\text{第一（代数）Bianchi}
\end{aligned}}
\]

### 证明思路（局部惯性系法）

在任意一点 \(p\) 可取**局部惯性系**：\(\Gamma^\rho_{\mu\nu}(p)=0\)，但 \(\partial\Gamma(p)\neq0\)（曲率不可"变换掉"）。
此时 \(\Gamma\Gamma\) 项为零，且由 \(\Gamma\) 的显式公式与 \(\partial_\alpha g_{\mu\nu}(p)=0\) 得：

\[
R_{\rho\sigma\mu\nu}(p)=\frac12\Big(
\partial_\mu\partial_\sigma g_{\nu\rho}
-\partial_\mu\partial_\rho g_{\nu\sigma}
-\partial_\nu\partial_\sigma g_{\mu\rho}
+\partial_\nu\partial_\rho g_{\mu\sigma}\Big)
\]

由该式**逐项读出**四条对称性：

- **S1**：\(\rho\leftrightarrow\sigma\) 时四项整体变号 ✔
- **S2**：\(\mu\leftrightarrow\nu\) 时四项整体变号 ✔
- **S3**：\((\rho\sigma)\leftrightarrow(\mu\nu)\) 时式子回到自身 ✔
- **S4**：轮换 \((\sigma,\mu,\nu)\) 三项相加，每个二阶导数出现两次且符号相反 ⇒ 相消 ✔

由于两边都是**张量**，在局部惯性系成立的等式在任意坐标系成立 ⇒ 全局成立。

**脚本核验**：E4（2 维球面，全 16 分量三条对称性）、E9/E10（Schwarzschild 抽样）、E11（Schwarzschild 第一 Bianchi）均 PASS。

---

## E.2 独立分量数

**计数方法（三种等价）**：

1. **双矢量空间法**：由 S1、S2，黎曼张量可看作定义在 \(\wedge^2 T_p^\ast\)（维数 \(N=\binom{n}{2}=\frac{n(n-1)}{2}\)）上的**对称**双线性型（由 S3）⇒ 候选数 \(\frac{N(N+1)}{2}\)；
2. 再减去 S4 的独立约束数 \(\binom{n}{4}\)（每个 4 元指标组给 1 个约束）；
3. 结果：

\[
\boxed{C_n=\frac{N(N+1)}{2}-\binom{n}{4}=\frac{n^2(n^2-1)}{12}}
\]

| 维数 \(n\) | \(N\) | \(\frac{N(N+1)}{2}\) | \(\binom{n}{4}\) | \(C_n\) |
|---|---|---|---|---|
| 2 | 1 | 1 | 0 | **1** |
| 3 | 3 | 6 | 0 | **6** |
| 4 | 6 | 21 | 1 | **20** |

**脚本核验**：E12 对 \(n=2,3\) 用**线性约束矩阵的秩**实测（把 \(n^4\) 个分量作变量、把 S1–S4 写成齐次线性方程，独立分量数 = 变量数 \(-\) 约束秩），实测 1 与 6，与公式一致（PASS）；E13 对 \(n=4\) 用公式给出 20（PASS）。

**物理意义**：4 维时空的"自由度"是 20 个曲率分量；其中 Ricci 张量（10 个）由场方程与物质耦合确定，剩下 10 个由 **Weyl 张量**承载——那是**真空中的引力自由度**（引力波、潮汐形变），即"物质之外的时空弯曲"。

---

## E.3 第二（微分）Bianchi 恒等式

\[
\boxed{\nabla_\lambda R^\rho_{\ \sigma\mu\nu}
+\nabla_\mu R^\rho_{\ \sigma\nu\lambda}
+\nabla_\nu R^\rho_{\ \sigma\lambda\mu}=0}
\]

（等价写法 \(\nabla_{[\lambda}R^\rho_{\ \sigma|\mu\nu|}=0\)，轮换 \((\lambda,\mu,\nu)\)。）

### 证明（局部惯性系）

在 \(p\) 点取局部惯性系（\(\Gamma(p)=0\)），协变导数退化为偏导，且 \(R^\rho_{\ \sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}\)：

\[
\begin{aligned}
&\partial_\lambda(\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma})
+\partial_\mu(\partial_\nu\Gamma^\rho_{\lambda\sigma}-\partial_\lambda\Gamma^\rho_{\nu\sigma})
+\partial_\nu(\partial_\lambda\Gamma^\rho_{\mu\sigma}-\partial_\mu\Gamma^\rho_{\lambda\sigma})\\
=&\ \big(\partial_\lambda\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\mu\partial_\lambda\Gamma^\rho_{\nu\sigma}\big)
 +\big(\partial_\mu\partial_\nu\Gamma^\rho_{\lambda\sigma}-\partial_\nu\partial_\mu\Gamma^\rho_{\lambda\sigma}\big)
 +\big(\partial_\nu\partial_\lambda\Gamma^\rho_{\mu\sigma}-\partial_\lambda\partial_\nu\Gamma^\rho_{\mu\sigma}\big)=0
\end{aligned}
\]

每一对由**偏导数对易**相消。由于结果是张量方程且在每点可取局部惯性系 ⇒ 全局成立。

**脚本核验**：
- E16：3 维共形平直度规 \(g_{\mu\nu}=e^{2\sigma(u_1)}\cdot\mathrm{diag}(1,-1,-1)\)，曲率非零（E15 先行确认非平凡），符号精确验证，抽样 3 组 PASS；
- E17：4 维 Schwarzschild 真空解，在 \(r=4M,\ \theta=\pi/3\) 数值代入（30 位），抽样 2 组，**最大残差 \(0.000\times10^{0}\)**，PASS。

---

## E.4 最重要的推论：\(\nabla^\mu G_{\mu\nu}=0\)

对微分 Bianchi 缩并两次（先 \(\rho\) 与 \(\mu\)，再与 \(\nu\)）：

\[
\nabla^\mu\Big(R_{\mu\nu}-\frac12g_{\mu\nu}R\Big)=0
\;\Longrightarrow\;
\boxed{\nabla^\mu G_{\mu\nu}=0}
\]

**这是爱因斯坦选择 \(G_{\mu\nu}\) 作为场方程几何侧的"唯一理由"**（在 ≤2 阶导数、由度规构造的张量中，满足恒等守恒的对称张量只有 \(G_{\mu\nu}+\Lambda g_{\mu\nu}\)——Lovelock 定理在 4 维的特例）。

**物理意义（本体论层）**：

> 物质侧的能量动量守恒 \(\nabla^\mu T_{\mu\nu}=0\) 与几何侧的 \(\nabla^\mu G_{\mu\nu}=0\) **不是两条独立定律**——
> 几何侧是恒等式（自动成立），物质侧是场方程的**相容性条件**。
> 广义相对论"自动"保证能量动量守恒，这正是 Bianchi 恒等式的物理分量。

---

## E.5 精算基准 I：2 维球面（常曲率）

\[
ds^2=r_0^2\big(d\theta^2+\sin^2\theta\,d\phi^2\big)
\]

常曲率空间满足：

\[
R_{\rho\sigma\mu\nu}=K\big(g_{\rho\mu}g_{\sigma\nu}-g_{\rho\nu}g_{\sigma\mu}\big),\qquad K=\frac{1}{r_0^2}
\]

**脚本核验（E1，PASS）**：16 个分量符号恒等。

推论（与缩并约定自洽）：

\[
R_{\mu\nu}=K\,g_{\mu\nu}\ \ \text{(E2, PASS)},\qquad
R=n(n-1)K=\frac{2}{r_0^2}\ \ \text{(E3, PASS)}
\]

> **注意**：\(R_{\mu\nu}=(n-1)Kg_{\mu\nu}\) 中的 \((n-1)\) 直接依赖缩并约定 \(R_{\mu\nu}=R^\sigma_{\ \mu\sigma\nu}\)。
> 若采用相反的缩并约定（部分文献），\(\mathrm{Ric}\) 与 \(R\) 会整体变号。本文与专题任务 1 的约定一致（脚本 E18，INFO）。

---

## E.6 精算基准 II：Schwarzschild（真空解）

\[
ds^2=\Big(1-\frac{2M}{r}\Big)dt^2-\Big(1-\frac{2M}{r}\Big)^{-1}dr^2
-r^2\big(d\theta^2+\sin^2\theta\,d\phi^2\big)
\]

（取 \(G=c=1\)，签名 \((+,-,-,-)\)。）

**脚本核验**：

- E6：\(\mathrm{Ric}_{\mu\nu}=0\)（16 个分量全部符号化简为零）— PASS
- E7：\(R=0\) — PASS
- E8：\(G_{\mu\nu}=0\) — PASS

**注意（诚实边界）**：Schwarzschild 是**真空解** ⇒ \(R_{\mu\nu}=0\) 但 \(R^\rho_{\ \sigma\mu\nu}\neq0\)。
真空中"曲率不为零而 Ricci 为零"正是 Weyl 张量承载自由度的体现（与 E.2 呼应）：
潮汐力 / 引力波存在于真空，而 Ricci 只由局域物质决定。

---

## E.7 数学层 vs 物理层的严格分工

| 层次 | 内容 | 是否含物理假设 |
|---|---|---|
| 数学定义 | \(R^\rho_{\ \sigma\mu\nu}\) 由联络定义 | 否 |
| 代数对称性 S1–S4 | 由定义（无挠 + 度规相容）推出 | 否（但"无挠"是假设：有挠理论如 Einstein–Cartan 会破坏 S3/S4） |
| 微分 Bianchi | 由定义推出（偏导对易） | 否 |
| \(\nabla^\mu G_{\mu\nu}=0\) | 恒等式 | 否 |
| 场方程 \(G_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}\) | **物理定律** | **是**（非由几何推出） |
| Schwarzschild 度规 | 场方程的一个解 | 是（对称性 + 边界条件的物理选择） |

> **关键区分**：本文 E 组全部是**数学恒等式**的复算，不含任何物理假设（除"无挠 + 度规相容"这一列维-奇维塔联络的定义前提）。
> 场方程本身是物理输入，不能从 Bianchi 恒等式推出——Bianchi 只限制它的**形式**（必须是 \(G_{\mu\nu}+\Lambda g_{\mu\nu}\)）。

---

## E.8 物理边界（严格标注）

1. **"无挠"是假设**：Einstein–Cartan 理论等含挠引力理论中，S3/S4 会被挠率项修正；本文结论限于列维-奇维塔联络。
2. **缩并约定依赖文献**：不同文献对 \(R_{\mu\nu}\) 的缩并指标顺序不同（导致整体符号差异）。本文固定专题任务 1 的约定，并在 E2 用已知度规（2 维球面）做了自洽性交叉验证。
3. **不宣称新结果**：E 组是标准结果的**可复算核验**，其价值在于：为后续任何引用黎曼张量性质的推导提供"已验证的地基"，而非提出新物理。
4. **数值验证的局限**：E17 是**单点数值代入**（\(r=4M,\theta=\pi/3\)），配合 E16 的符号精确验证；严格性由"符号恒等式 + 具体度规复算"双重保证，不等于对所有时空的穷举证明（数学证明由 E.3 的局部惯性系论证完成）。

---

## E.9 精算结论（脚本 E 组）

| 条目 | 核验内容 | 结论 |
|---|---|---|
| E1 | 2 维球面常曲率关系（16 分量） | PASS |
| E2 | \(\mathrm{Ric}=K g\)（缩并约定自洽） | PASS |
| E3 | \(R=n(n-1)K=2/r_0^2\) | PASS |
| E4 | 代数对称性 S1/S2/S3（2 维球面全分量） | PASS |
| E5 | Ricci 张量对称 | PASS |
| E6 | Schwarzschild \(R_{\mu\nu}=0\)（16 分量） | PASS |
| E7/E8 | Schwarzschild \(R=0,\ G_{\mu\nu}=0\) | PASS |
| E9/E10 | Schwarzschild 抽样对称性 | PASS |
| E11 | Schwarzschild 抽样第一 Bianchi | PASS |
| E12 | \(n=2,3\) 独立分量数实测 \(1,6\)（线性约束秩） | PASS |
| E13 | \(n=4\) 独立分量数 \(20\)（公式） | PASS |
| E14 | 计数方法说明 | INFO |
| E15 | 3 维共形平直度规曲率非零（非平凡性） | PASS |
| E16 | 微分 Bianchi（3 维，符号精确，抽样 3 组） | PASS |
| E17 | 微分 Bianchi（Schwarzschild，\(r=4M\) 数值，残差 \(0\)） | PASS |
| E18 | 缩并约定说明 | INFO |

**复跑方式**：

```
cd 02_共享基础/推导与量纲专题/延伸方向
python -B verify_extension_derivation.py
```
