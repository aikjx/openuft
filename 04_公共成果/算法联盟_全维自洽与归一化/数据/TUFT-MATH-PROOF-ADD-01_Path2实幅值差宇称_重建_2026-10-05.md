# TUFT-MATH-PROOF-ADD-01 实幅值差宇称通道（Path 2）数值重建【修正版】报告（分支 3c）

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_Path2实幅值差宇称_重建_2026-10-05.py
- 日期：2026-10-05
- 读数：7 guard —— PASS 7 / FAIL 0（退出码 0）

| PASS | delta_lambda_formula | delta_lambda(0.05)=0.01312（≈0.2625·eps） |
| PASS | deltaA_scaling | deltaA(0.01)=0.00102 ⇒ 系数 0.102·eps |
| PASS | survival_epsilon_threshold | eps_crit = 0.0098（约 1% 右旋污染为存活上限） |
| PASS | natural_epsilon_from_omega | eps_nat(g2)=0.026, eps_nat(sqrt)=0.130（均超存活上限 ~0.01） |
| PASS | deltaA_natural_vs_precision | deltaA_nat(g2)=0.0026（3×ΔA），deltaA_nat(sqrt)=0.0120（12×ΔA） |
| PASS | live_testable_boundary | eps=0.01 ⇒ |deltaA|=0.0010 ≈ ΔA=0.001（可探边界） |
| PASS | honest_epsilon_status | deltaA=0.10·eps 为干净线性预言（物理基线下无归一化歧义）；但 eps 由模型未定；天然 eps=|Omega|/g_SM~0.03-0.13 超存活上限，须把右旋污染压到 ~1% 方存活 |

### 结论

1. **修正模型**：在物理基线 lambda_SM=-1.2756 上叠加右旋污染 eps（幅值比），
   delta_lambda = -eps(1+lambda_SM)/(1+eps) ~ +0.2756·eps，**只依赖 eps，不依赖 g_SM 归一化**
   （消除分支 3 的归一化歧义）。
2. **deltaA 显式**：**deltaA = 0.10·eps**（物理基线下干净线性）。
3. **存活阈值**：|deltaA|<DeltaA=0.001 需 **eps < ~0.01（约 1% 右旋污染）**。
4. **TUFT 天然值**：若右旋幅值=|Omega|（继承 B.3），eps=|Omega|/g_SM=0.026(g2)/0.130(sqrt)
   ⇒ deltaA=0.0027(g2)/0.013(sqrt)，**超 ΔA 约 3-13 倍** ⇒ 天然假设下仍被排除，须把
   右旋污染压到 ~1%。
5. **边界可测**：eps=0.01 时 deltaA~0.001，恰在当前 β 精度 ~ΔA ⇒ 现有/近未来测量可探
   （对比相位通道 T-odd 已被 EDM 排除 ~3e11 倍，Path 2 是唯一活通道）。
6. **诚实**：eps 由模型未定；deltaA=0.10·eps 是干净可证伪预言，但需模型解释为何
   eps~1% 而非天然 3-13%。
