# TUFT · R28 —— Kerr/Teukolsky 推广：第一性结构探测（**自检失败，NO Kerr numbers**）

> 一句话：向**旋转 Kerr 黑洞**推广 R25 的 QNM 工具时，先做了一次**自检**，结果是**中止**——
> Teukolsky 径向方程本身**已验证正确**（a→0, s=0 的标量极限与 Schwarzschild 无质量标量方程**符号恒等**）；
> 但重建的 y-变量约化 machinery **未通过自检**（对已知应该给出 3 项递推的 RW，复算得 (3,2,1) 而非 (2,1,0)）。
> **因此 R28 不产出任何 Kerr QNM 频率**——宁记失败，不编数值。

评级 **C / L2**。结果：**PASS=1 / FAIL=1 / BOUNDARY=10 / INFO=13**。

---

## 零、承接

| 册 | 内容 | 精度 |
|---|---|---|
| R20 | WKB σ_abs⁰（含 R19 修正） | — |
| R21/R22 | 时域演化 | 0.3~0.6% |
| R23 | Chebyshev 谱配点**失败**（QNM 两端指数增长 ⇒ 退化为箱模） | — |
| R24 | 矩阵束 Prony | 1.2e-3 |
| **R25** | **Schwarzschild Leaver 连分式** | **≤1e-6（特征值级）** |
| R26 | R25 全维验证 + 结构诊断（RW=3 项，Zerilli=5 项） | — |
| R27 | SUSY(Darboux) 证明 **RW↔Zerilli 等谱**（闭合 R26 缺口） | — |
| **R28** | **向 Kerr（Teukolsky）推广 → 自检失败，中止** | — |

---

## 一、V1：Teukolsky 径向方程正确建立（**PASS**）

Teukolsky 径向方程（s=−2）：

$$\Delta R''+(s+1)\Delta'R'+\Big[\tfrac{K^2}{\Delta}-\tfrac{2is(r-M)K}{\Delta}+4is\omega r-\lambda\Big]R=0$$

$$\Delta=r^2-2Mr+a^2,\quad K=(r^2+a^2)\omega-ma,\quad \lambda=A+a^2\omega^2-2am\omega$$

**核对**：取 a→0、s=0（标量极限），方程化为 ΔR''+Δ'R'+[K²/Δ−λ]R=0，其中 Δ=r²−2Mr ⇒ K²/Δ=ω²r²/f、Δ'=2r−2M。

独立推导的 Schwarzschild 无质量标量径向方程（`□Φ=0`，Φ=R(r)Y e^{−iωt}）：

$$r^2fR''+(2r-2M)R'+\big[\tfrac{r^2\omega^2}{f}-l(l+1)\big]R=0$$

sympy 逐**符号恒等**相减结果为 **0** ⇒ **Teukolsky 方程本身无误**（至少在该极限下）。

> 此前我一度怀疑 −2is(r−M)K/Δ、4isωr 等项有误；这个核对证明担忧不成立。

---

## 二、V2：machinery **自检未通过**（**FAIL**）

对 Kerr 推广，我重建了一套统一的 y-变量约化 machinery

$$y=\frac{r-r_+}{r-r_-},\qquad q=\frac{dy}{dr}=\frac{(1-y)^2}{D},\qquad R=e^{i\omega r}(r-r_+)^u(r-r_-)^v S(y)$$

核心判据：清分母并约去公共因子后，(deg S″, deg S′, deg S) **必须 = (2,1,0)**，才对应 3 项递推（Leaver 连分式的必要条件；由 (2,1,0) 时 y^k 系数只含 d_k, d_{k+1}, d_{k+2} 得出）。

**先在 RW（a=0，R25 已知 3 项）上自检**：

| 检验对象 | 最小清分母倍数 | (deg S″, deg S′, deg S) | 期望 | 结论 |
|---|---|---|---|---|
| **RW**（ansatz u=−2iMω, v=4iMω） | y(1−y)² | **(3, 2, 1)** | (2,1,0) | ❌ **未通过** |

⇒ machinery 与 R25 的推导存在**未定位的偏差**。已排查并**排除**的可能性：
- ansatz 指数 (u,v) 取值——不影响次数（次数只由极点结构决定，与 u,v 具体值无关）；
- A,B,C 的公共因子——已做 gcd 约分，次数不降（仍 (3,2,1)）。

**最可疑点**（列入修复清单①）：machinery 先除以 A=f² 清分母；而 f=y，使 A→0 于 y=0，**人为引入 1/y² 极点**，可能把本应 (2,1,0) 的结构抬高。

---

## 三、V3：Teukolsky 约化结果（**不可信，不作数**）

同一 machinery 对 Teukolsky(a=0, s=−2)（Leaver ansatz：u=−s−2iMω, v=−1+s）：

| 对象 | 最小倍数 | 次数 |
|---|---|---|
| Teukolsky a=0, s=−2 | y(1−y)³ | (4, 3, 2) |

**但因 V2 自检未过，此结果不可信** ⇒ **R28 不产出任何 Kerr QNM 频率**。

---

## 四、修复清单（下一步）

1. **先对齐 RW**（最重要）：不要重建 machinery，直接复用 **R25 已通的推导路径**，与之逐项对齐；重点排查"先除以 A=f²"是否引入人为极点。
2. 对齐后再处理 Kerr 的 ma≠0、r₋≠0 分支；并与 **Leaver (1985) 原文**核对 ansatz 指数与 σ± 归一：
   σ±=(ω(r±²+a²)−ma)/(r₊−r₋)。
3. 即便 3 项成立，Kerr 还需**角向自旋权椭球调和本征值 A(aω)** 与径向**联动求解**（双连分式/迭代）——这是比 Schwarzschild 多出的一维。
4. 若高阶递推为真，则需 **Nollert 广义（矩阵）连分式**，而非 Leaver 单连分式。

---

## 五、诚实边界

| # | 边界 |
|---|---|
| ① | **本册不含任何 Kerr QNM 数值**，也不含 Teukolsky-Starobinsky 数值结果。 |
| ② | V1 仅核对 a=0, s=0 标量极限；s=±2 独有的 −2is(r−M)K/Δ、4isωr 项**未被独立验证**。 |
| ③ | V2 的"应为 (2,1,0)"是从 R25 的 3 项结论**反推**的判据；若 R25 的 3 项来自另一等价形式，则可能是**判据**而非 machinery 出错——已如实标注为"未定位"。 |
| ④ | 仅非磁化、无宇宙学常数的 Kerr；极值 a→M 未处理；拖曳效应未在本册实现。 |
| ⑤ | **红线**：宁记失败，不产出未经自检的数值。 |

---

## 六、结论

1. **Teukolsky 径向方程成立**（标量极限符号恒等）——这是可以放心使用的正结果。
2. **向 Kerr 的 QNM 推广在本册中止**：machinery 未过 RW 自检，**这是本册最重要的方法论输出**——它拦住了一批本会错误的 Kerr 数值。
3. 下一步必须先完成修复清单①（对齐 RW），否则后续 Kerr 结果都不可信。

---

*TUFT R28 · Kerr/Teukolsky 结构探测 · 算法联盟 · 脚本 `tuft_r28_kerr_teukolsky_probe.py` · 报告 `tuft_r28_report.txt`*
