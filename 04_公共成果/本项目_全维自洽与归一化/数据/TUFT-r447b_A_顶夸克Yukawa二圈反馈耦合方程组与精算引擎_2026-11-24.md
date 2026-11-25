# TUFT-r447b_A_顶夸克Yukawa二圈反馈耦合方程组与精算引擎_2026-11-24

- 判词：`TOP-YUKAWA-TWO-LOOP-FEEDBACK-PRICED--INPUT-COEFFICIENTS-CORRECTED--STANDARD-SIGN-AND-COLUMN-LOCKED--RK4-CONVERGED--PASS-NOT-FIRST-PRINCIPLE`
- 条目：14；PASS=5 / FAIL=0 / BOUNDARY=1 / INFO=5 / CORRECTED=3
- 守卫：22/22

## 关键读数

| 项 | 读数 |
|---|---|
| beta_chain_max_rel_err_std | 3.7196170846605928025124680E-19 |
| beta_chain_max_rel_err_input | 3.5984278500951195177014479E-19 |
| b2_matrix_sensitivity | 4.0356200137977403557139119E-5 |
| yt_coeff_sensitivity | 4.3097515837686864488135802E-2 |
| formal_noY_MG_GeV | 1.1247473212631995094549825E+16 |
| formal_noY_r447_rel_diff | 1.0455543921032936736870544E-14 |
| formal_std_MG_GeV | 1.1030289063619143453645251E+16 |
| formal_std_alphaG12 | 3.8824720501304635638097948E-2 |
| formal_std_yt_at_G | 7.5643548204642482348099102E-1 |
| formal_std_dL | 3.9552059413485094312056464E-1 |
| formal_MG_rel_offset_std | -1.9309594689137195322558970E-2 |
| formal_alphaG_rel_offset_std | -5.1259629744517569994909950E-3 |
| formal_MG_rel_offset_input_column | -7.4193731531583678613793151E-2 |
| formal_step_rel_MG | 1.2856033687897306749370660E-10 |
| benchmark_noY_MG23_GeV | 5.2529541334316153889165096E+15 |
| benchmark_std_MG23_GeV | 5.5344056833824559120368913E+15 |
| benchmark_input_MG23_GeV | 5.1469157756979639362517049E+15 |
| benchmark_input_t23 | 3.1664255128757780705910102E+1 |
| benchmark_input_delta_inv_2_3 | 1.5671639958854060050759392E-7 |
| benchmark_input_delta_inv_1_2 | 1.3682589036099405650718438E+0 |
| benchmark_input_rel_offset | -5.4239359557509963513246427E-1 |
| benchmark_std_invAlphaG_at_23 | 2.4191295228092036817579128E+1 |
| benchmark_std_yt_at_23 | 5.0712443041484363238081568E-1 |
| benchmark_MG_rel_offset_std | 5.3579670182076328618254582E-2 |
| benchmark_invAlphaG_claim_rel_error | 6.5973157216523674996944856E-2 |
| input_report_t_rel_diff | 1.3333424051241177684495134E-12 |
| input_report_MG_rel_diff | 5.8682923306552877585374792E-11 |
| input_report_shift_rel_diff | 7.4562937710385353770058101E-7 |

## 条目

- **I01 [INFO]** [C] 外部输入登记：MSSM 规范群、GUT 归一、yt(MZ)=0.95、tan beta=10、mt=163 GeV 均为外部输入；不是 TUFT 导出
- **I02 [PASS]** 顶 Yukawa 一圈 beta 系数核验：yt_c=(-13/15,-3,-16/3)，d=6，规范项为负、自作用为正；守卫 G0-4 与 G0-10 通过
- **I03 [CORRECTED]** 来料二圈 Yukawa 列修正：来料 C_U=(14/5,6,16/3)；标准顶列 c_it=(26/5,6,4)，来料列不作为标准结论
- **I04 [CORRECTED]** 来料二圈 Yukawa 符号修正：标准 g 形式括号为 sum B_ij g_j^2 - c_it yt^2；来料正号只作 benchmark 对照
- **I05 [PASS]** 规范-beta 链式求导核验：标准负号与来料正号两套 alpha^-1 导数有限差分误差均小于 1e-12
- **I06 [PASS]** 四耦合 RK4 分段引擎收敛：formal 与 benchmark 的 h=0.02/0.01 相对差均小于 1e-6
- **I07 [PASS]** 顶 Yukawa 偏移完成量化：formal M_G 相对无 Yukawa 偏移 -1.9309594689137195322558970E-2，alpha_G 偏移 -5.1259629744517569994909950E-3
- **I08 [BOUNDARY]** tan beta 与顶质量初始值为外部输入：yt(MZ)=0.95 依赖 mt=163 GeV 与 tan beta=10；误差不构成本框架内部矛盾
- **I09 [INFO]** 阶数边界：规范二圈含 Yukawa 诱导项，Yukawa 只取一圈；Yukawa 二圈自修正登记为 r447b-2
- **I10 [INFO]** 基准与正式口径分离：来料全程 MSSM 代码只作 benchmark；正式口径保持 r447 的 SM 一圈至 1 TeV + MSSM 二圈分段
- **I11 [INFO]** 全局记分板不变：0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4
- **I12 [PASS]** 来料代码读数复现：t_G=3.1664255128757780705910102E+1，M_G=5.1469157756979639362517049E+15 GeV，inv2-inv3=1.5671639958854060050759392E-7
- **I13 [CORRECTED]** 来料模块5报告数字修正：报告写 M_G≈1.21e16 GeV 与 +7.5%；同一代码口径实跑为约 5.15e15 GeV 与 -54.24%，以代码实跑为准
- **I14 [INFO]** 严格三线交汇未成立：来料 benchmark 在 inv2=inv3 处 inv1-inv2=1.3682589036099405650718438E+0，不是三线同点
