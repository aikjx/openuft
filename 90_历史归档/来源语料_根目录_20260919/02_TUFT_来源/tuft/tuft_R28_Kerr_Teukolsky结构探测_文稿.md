# TUFT · R28 —— Kerr/Teukolsky 推广：第一性结构探测 v2

> 一句话：向**旋转 Kerr 黑洞**推广 R25 的 QNM 工具。v1 曾"自检失败"，**v2 已定位并修复根因**，machinery 现通过自检。
> 结论：**Teukolsky 径向方程（s=−2）在标准 Leaver ansatz 下是 4 项递推，不是 3 项** ⇒ R25 的单连分式**不能直接移植**到 Kerr；需 Nollert 广义（矩阵）连分式，或先变换到 3 项形式。
> 本册**仍不产出 Kerr QNM 数值**（未实现广义连分式），只给结构结论。

评级 **C / L2**。结果：**PASS=2 / FAIL=0 / BOUNDARY=7 / INFO=14**。

---

## 零、承接

| 册 | 内容 | 精度 |
|---|---|---|
| R21/R22 | 时域演化 | 0.3~0.6% |
| R23 | Chebyshev 谱配点**失败**（QNM 两端指数增长 ⇒ 退化为箱模） | — |
| R24 | 矩阵束 Prony | 1.2e-3 |
| **R25** | **Schwarzschild Leaver 连分式** | **≤1e-6（特征值级）** |
| R26 | R25 全维验证 + 结构诊断（RW=3 项，Zerilli=5 项） | — |
| R27 | SUSY(Darboux) 证明 **RW↔Zerilli 等谱**（闭合 R26 缺口） | — |
| **R28** | **向 Kerr（Teukolsky）推广 → 4 项递推，Kerr 需广义连分式** | 结构结论 |

---

## 一、V1：Teukolsky 径向方程正确建立（**PASS**）

$$\Delta R''+(s+1)\Delta'R'+\Big[\tfrac{K^2}{\Delta}-\tfrac{2is(r-M)K}{\Delta}+4is\omega r-\lambda\Big]R=0$$

$$\Delta=r^2-2Mr+a^2,\quad K=(r^2+a^2)\omega-ma,\quad \lambda=A+a^2\omega^2-2am\omega,\quad s=-2$$

**核对**（a→0, s=0 的标量极限）：化为 ΔR''+Δ'R'+[K²/Δ−λ]R=0，Δ=r²−2Mr ⇒ K²/Δ=ω²r²/f、Δ'=2r−2M；与独立推导的 Schwarzschild 无质量标量方程

$$r^2fR''+(2r-2M)R'+\big[\tfrac{r^2\omega^2}{f}-l(l+1)\big]R=0$$

sympy 相减**恰为 0** ⇒ 方程本身无误（此前怀疑 −2is(r−M)K/Δ、4isωr 项有误，此核对排除该怀疑）。

---

## 二、V2：定位并修复 machinery（**PASS**）

### v1 的 BUG
v1 把 ODE 化为标准形时**先除以 A**：`R_yy + (q_y/q + B/(Aq)) R_y + (C/(Aq²)) R = 0`。
但对 RW，`A=f²` 且 **`f=y`**（因 r=2M/(1−y)），故 A→0 于 y=0，**人为引入 1/y² 极点**，把结构抬高。

### v2 的修复
1. **不除以 A**：直接对 `A R_yy + B̄ R_y + C̄ R = 0` 处理，其中
   `B̄ = A·q_y/q + B/q`、`C̄ = C/q²`（由 `R'=qR_y`、`R''=qq_yR_y+q²R_yy` 得）。
2. **自动判定 p**（A 在 y=0 的零点阶），并按正规奇点结构归一：
   `Aₜ=A/yᵖ`、`Bₜ=(S'系数)/y^(p−1)`、`Cₜ=(S系数)/y^(p−2)`；
   **递推阶数 = max(deg Aₜ, deg Bₜ, deg Cₜ) + 1**（3 项 ⇔ 该最大值 = 2）。

### 自检结果

| 对象 | A | p | 最小清分母 | 约化次数 | **递推阶数** |
|---|---|---|---|---|---|
| **RW**（R25 已知 3 项） | `f² = y²`（双零点） | 2 | **(1−y)²** | **(2,2,2)** | **3** ✅ |
| Teukolsky(a=0,s=−2) | `Δ ∝ y/(1−y)²`（单零点） | 1 | **(1−y)⁵** | **(3,3,3)** | **4** |

RW 阶数 3 与 **R25 的 3 项递推一致** ⇒ **v2 通过自检**，v1 偏差根因确认为"先除以 A 引入人为极点"。

（v1 曾误用 `(deg S'',deg S',deg S)=(2,1,0)` 作判据——那是对 p=2 情形的另一种归一，未除 y 幂，故不适用。）

---

## 三、V3：Teukolsky 是 **4 项**递推（**BOUNDARY**）

修复后的 machinery：Teukolsky(a=0, s=−2)，Leaver ansatz `u=−s−iσ₊=−s−2iMω`、`v=−1+s`，得递推阶数 **4**。

**结构原因**：RW 的 `A=f²` 在 y=0 为**双零点**(p=2)，且 `V_RW→0` 于无穷；而 Teukolsky 的 `A=Δ` 为**单零点**(p=1)，且 `K²/Δ ∝ r²` **在 r→∞ 不衰减**，故 y=1 处奇性更重（需 (1−y)⁵ 才能清净）。

⇒ **R25 的单连分式不能直接移植到 Kerr**。后续两条路：
- **Nollert 广义（矩阵）连分式**（这与 R26 发现 Zerilli 为 5 项后的处置是同一工具家族）；
- 或先经 **Sasaki-Nakamura / Teukolsky→RW 型变换**化到 3 项形式。

---

## 四、后续清单

1. 实现 **Nollert 广义连分式**（可同时服务 R26 的 Zerilli-5 项与 R28 的 Kerr-4 项——**一举两得**）。
2. 或实现 Sasaki-Nakamura 变换，化 Kerr 为 3 项。
3. Kerr 还需**角向自旋权椭球调和本征值 A(aω)** 与径向**联动求解**（比 Schwarzschild 多一维）。
4. V3 目前只做 a=0；Kerr(a≠0) 时 ma≠0、r₋≠0，奇性结构可能变化，需复测。

---

## 五、诚实边界

| # | 边界 |
|---|---|
| ① | **本册不含任何 Kerr QNM 数值**，未实现广义连分式/角向本征值联动。 |
| ② | V1 仅核对 a=0, s=0 标量极限；s=±2 的 −2is(r−M)K/Δ、4isωr 项**未被独立验证**。 |
| ③ | V3 只做 a=0；Kerr(a≠0) 时奇性结构可能变化，未测。 |
| ④ | 仅非磁化、无宇宙学常数 Kerr；极值 a→M 未处理；拖曳效应与 Teukolsky-Starobinsky 恒等式未实现。 |
| ⑤ | **红线**：数学自洽 ≠ 实验证实；宁记边界，不产出未闭合的数值。 |

---

## 六、结论

1. **Teukolsky 径向方程成立**（标量极限符号恒等）。
2. **machinery 已修复并通过 RW 自检**——v1 的 FAIL 已消除，根因是"先除以 A"。
3. **Teukolsky 为 4 项递推** ⇒ Kerr 需 Nollert 广义连分式；这与 R26 的 Zerilli-5 项**共用同一工具**，可作为统一的下一步。

---

*TUFT R28 · Kerr/Teukolsky 结构探测 v2 · 算法联盟 · 脚本 `tuft_r28_kerr_teukolsky_probe.py` · 报告 `tuft_r28_report.txt`*
