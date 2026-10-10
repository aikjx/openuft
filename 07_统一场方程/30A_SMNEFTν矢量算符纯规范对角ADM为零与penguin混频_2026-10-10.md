# 30A · SMNEFT $(\bar n\gamma n)(\bar X\gamma X)$ 矢量算符纯规范对角 ADM 为零 + penguin 混频

> 日期：2026-10-10  
> 状态：承接 [29A](29A_SMNEFT四费米算符纯规范ADM复现_2026-10-10.md) 的算符级 ADM 方法，直接作用于 **25A 的 6 个 ν 类算符**。按 arXiv:2010.12109 约定（$a_\psi=-C_2$、$a_\psi^1=-y^2$，29A 钉死）+ 主公式 $\gamma_{ij}=-2g_m^2\big[\sum_\psi\tfrac12a_\psi^m\delta_{ij}+b_{ij}^m\big]$，自含复现 $O_{nd}$ 对角 ADM=0（A.21），并证明**全部 $(\bar n\gamma n)(\bar X\gamma X)$ 矢量算符的纯规范对角 ADM 为零**（n 是规范单态，X 流-流 $b=C_2/y^2$ 恰抵消 X 场强 $\sum\tfrac12a_\psi$）；核验 penguin 混频非零。由零依赖验证器 [war_smneft_nu_adm.py](验证脚本/war_smneft_nu_adm.py) 固化，**8/8 PASS**。

[29A · SMNEFT四费米纯规范ADM复现](29A_SMNEFT四费米算符纯规范ADM复现_2026-10-10.md) · [25A · 含νR扩展系数表](25A_含νR的J5平方扩展算符完整系数表_2026-10-10.md) · [28A · 场强重整化系数](28A_SM费米子场强重整化系数与ADM场强分量_2026-10-10.md)

---

## 1. 本卷回答什么

25A 的 6 个 ν 类矢量算符（$Q_{\nu\nu},Q_{\nu e},Q_{\nu u},Q_{\nu d},Q_{\nu l},Q_{\nu q}$，即 SMNEFT 的 $O_{nn},O_{ne},O_{nd},O_{nu},O_{\ell n},O_{nq}$）的一圈 RG：它们的**纯规范对角 ADM 是否为零？** 答案：**是**——因 n 是全规范单态，且 X 流内单规范玻色子交换的流-流 $b_X=C_2(R_X)$（或 $y_X^2$）恰与 X 的场强贡献 $-\sum\tfrac12a_\psi$ 抵消。

## 2. 方法与机制

主公式：$\gamma=-2g_m^2[\sum_\psi\tfrac12a_\psi^m\delta_{ij}+b_{ij}^m]$。对 $(X\gamma X)(n\gamma n)$（场序 $n,n,X,X$）：场强分量 $\sum\tfrac12a_\psi=\tfrac12(2a_X)=\tfrac12(-2C_2)=-C_2$（g₁ 为 $-y_X^2$）；流-流 $b_X=C_2(R_X)$（g₁ 为 $y_X^2$）。二者相加为零 → $\gamma=0$。

## 3. 结果（8/8 PASS）

| 检查 | 内容 | 结果 |
|---|---|---|
| V1 | $O_{nn}$：n 全规范单态，对角 $\gamma=0$（主文 $\dot{\mathcal C}_{nn}=0$） | PASS |
| V2 | $O_{nd}$：场强 $g_1{=}{-}y_d^2/b^1{=}y_d^2$、$g_3{=}{-}\tfrac43/b^3{=}\tfrac43$ 相消 → $\gamma_1{=}\gamma_3{=}0$（复现 A.21） | PASS |
| V3 | $O_{ne}$：$g_1$ 场强 $-y_e^2$/流-流 $y_e^2$ 相消 → 0 | PASS |
| V4 | $O_{nu}$：$g_1/g_3$ 均相消 → 0 | PASS |
| V5 | $O_{\ell n}$：$g_2$ 场强 $-\tfrac34$/流-流 $\tfrac34$、$g_1$ 相消 → 0 | PASS |
| V6 | $O_{nq}$：$g_1/g_2/g_3$ 全相消 → 0 | PASS |
| V7 | penguin 混频 $O_{nd}\to O_{nu}$：$\gamma_1=\tfrac43 y_d y_u N_c=-\tfrac89 g_1^2\ne0$（A.22） | PASS |
| V8 | 25A 映射：6 个 ν 类矢量算符对角纯规范 ADM 全零；跑动经 penguin 混频 | PASS |

**机制**：$(X\gamma X)$ 流在规范群下的单玻色子交换 $b_X$ 恰等于 $X$ 的场强贡献（$C_2$ 或 $y^2$），符号相反，故对角相消。这是 n 为规范单态的结构性后果。

## 4. 对统一场论主线的意义

对 25A 的 ν 类算符给出确定的一圈 RG 结构：**纯规范对角 ADM 全零**（$Q_{\nu\nu}$ 总单态、其余因相消），跑动来自 penguin 混频（$O_{nd}\to O_{nu}$、$O_{X n}\to O_{\phi n}$ 等）。这修正了"ν 类算符需逐类取 ADM"的预期——其对角部分自动为零，只需处理 penguin 混频。

## 5. 诚实边界与下一步

| 关口 | 本卷所得 | 仍未做 |
|---|---|---|
| 6 个 ν 类矢量算符纯规范对角 ADM=0 | 8/8 PASS（复现 A.21 + 机制推广） | — |
| penguin 混频非零（$O_{nd}\to O_{nu}$） | 已核验（A.22） | — |
| 25A 标准 15 类算符（无 ν）的 ADM | 未做 | 需完整 SMEFT ψ⁴ 矩阵（$O_{qq},O_{ll},O_{uu}$…） |
| 完整混频 $O_{X n}\to O_{\phi n}$、Yukawa 贡献、$J_5^2$ 一圈跑动 | 未做 | 需外部矩阵 + 组装 |
| 完整量子引力、四力统一、暗物质 | 未涉及 | 研究前沿 / 需外部数据 |

**下一步**：a) 对 25A 的**标准 15 类**（$Q_{qq}^{(1)},Q_{ll},Q_{uu},Q_{ee},Q_{lq},Q_{qu},...$）取纯规范对角 ADM——这些无 n 单态抵消，ADM 非零，需完整 SMEFT ψ⁴ 矩阵；b) 组装 $J_5^2$ 一圈跑动。

## 6. 本轮结论

1. **证明**所有 $(\bar n\gamma n)(\bar X\gamma X)$ 矢量算符的纯规范对角 ADM 为零（n 规范单态 + 流-流/场强相消），8/8 PASS。
2. 复现权威 $O_{nd}$ 结果（A.21 $\gamma_1=\gamma_3=0$），并推广到全部 6 个 ν 类算符。
3. 跑动来自 penguin 混频（非零），25A 的 ν 类算符一圈 RG 结构确立。
4. 25A 标准 15 类算符 ADM 与完整组装仍为明示边界。

## 参考资料

- arXiv:2010.12109：A.19–A.21（$O_{nd}$ 对角）、A.17/A.22（penguin 混频）、主文 $\dot{\mathcal C}_{nn}=0$；约定见 29A。
- 25A 卷：6 个 ν 类算符的完整 Wilson 系数表。
