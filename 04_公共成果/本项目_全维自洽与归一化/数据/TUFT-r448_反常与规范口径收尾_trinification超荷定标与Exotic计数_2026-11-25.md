# TUFT-r448_反常与规范口径收尾_trinification超荷定标与Exotic计数_2026-11-25

- 判词：`TRINIFICATION-HYPERCHARGE-CALIBRATED--ANOMALIES-DO-NOT-CONSTRAIN-MIXING--SM-MATCHING-FIXES-A-B--27-CONTAINS-EXOTICS--PASS-NOT-FIRST-PRINCIPLE`
- 条目：14；PASS=9 / FAIL=0 / BOUNDARY=1 / INFO=3 / CORRECTED=1
- 守卫：23/23

## 定标结果

- `Y = a·T8_L + b·T8_R`，SM 匹配给出 `a=-1/2`、`b=1`。
- 四条反常对任意 `(a,b)` 恒为零（约束秩 0）。

## 关键读数

| 项 | 读数 |
|---|---|
| sum_tL | 0 |
| sum_tR | 0 |
| sum_tL3 | 0 |
| sum_tR3 | 0 |
| sum_tL2tR | 0 |
| sum_tLtR2 | 0 |
| a33_a | 0 |
| a33_b | 0 |
| a22_a | 0 |
| a22_b | 0 |
| max_sampled_anomaly | 0 |
| a_calibrated | -1/2 |
| b_calibrated | 1 |
| ratio_minus_a_over_b | 1/2 |
| sm15_total | 15 |
| extra_sm_states | 5 |
| pure_exotic_states | 7 |
| n_Q | 6 |
| n_L | 4 |
| n_dc | 6 |
| n_nuc | 2 |
| n_g | 3 |
| n_exotic_doublet | 2 |

## 27 的 SM 谱

| 类别 | i | j | Y | 标签 |
|---|---|---|---|---|
| A | 0 | 0 | 1/6 | Q(3,2) |
| A | 0 | 1 | 1/6 | Q(3,2) |
| A | 0 | 2 | -1/3 | g(3,1) leptoquark |
| A | 1 | 0 | 1/6 | Q(3,2) |
| A | 1 | 1 | 1/6 | Q(3,2) |
| A | 1 | 2 | -1/3 | g(3,1) leptoquark |
| A | 2 | 0 | 1/6 | Q(3,2) |
| A | 2 | 1 | 1/6 | Q(3,2) |
| A | 2 | 2 | -1/3 | g(3,1) leptoquark |
| B | 0 | 0 | -1/2 | L(1,2) |
| B | 0 | 1 | -1/2 | L(1,2) |
| B | 0 | 2 | 1/2 | exotic(1,2) |
| B | 1 | 0 | -1/2 | L(1,2) |
| B | 1 | 1 | -1/2 | L(1,2) |
| B | 1 | 2 | 1/2 | exotic(1,2) |
| B | 2 | 0 | 0 | nu^c(1,1) |
| B | 2 | 1 | 0 | nu^c(1,1) |
| B | 2 | 2 | 1 | e^c(1,1) |
| C | 0 | 0 | 1/3 | d^c(3bar,1) |
| C | 0 | 1 | 1/3 | d^c(3bar,1) |
| C | 0 | 2 | -2/3 | u^c(3bar,1) |
| C | 1 | 0 | 1/3 | d^c(3bar,1) |
| C | 1 | 1 | 1/3 | d^c(3bar,1) |
| C | 1 | 2 | -2/3 | u^c(3bar,1) |
| C | 2 | 0 | 1/3 | d^c(3bar,1) |
| C | 2 | 1 | 1/3 | d^c(3bar,1) |
| C | 2 | 2 | -2/3 | u^c(3bar,1) |

## 条目

- **I01 [INFO]** [C] 约定登记：T8=diag(1/3,1/3,-2/3)；27=(3,3b,1)+(1,3,3b)+(3b,1,3)；L 分量 0,1 为双态；Y=a·T8_L+b·T8_R
- **I02 [PASS]** grav-U1 对任意 (a,b) 恒为零：ΣtL=ΣtR=0，符号项无约束
- **I03 [PASS]** U1³ 对任意 (a,b) 恒为零：ΣtL³=ΣtR³=ΣtL²tR=ΣtLtR²=0
- **I04 [PASS]** [SU3_C]²U1 对任意 (a,b) 恒为零：ΣT3C²·tL=ΣT3C²·tR=0
- **I05 [PASS]** [SU2_L]²U1 对任意 (a,b) 恒为零：ΣT3L²·tL=ΣT3L²·tR=0（破缺基）
- **I06 [PASS]** 四条反常约束秩为 0：6 组 (a,b) 采样最大反常 0；判据由阳性对照 A3 保证有牙
- **I07 [PASS]** 阳性对照证明判据有牙：全 Y=1 给 grav=27；非迹零位移被检测
- **I08 [PASS]** SM 超荷匹配唯一确定 (a,b)：a=-1/2、b=1，比例 -a/b=1/2
- **I09 [PASS]** 27 的 SM 谱自洽：Q=1/6、g=-1/3、L=-1/2、e^c=1、ν^c=0、u^c=-2/3、d^c=1/3 逐项匹配
- **I10 [PASS]** exotic 计数：SM 15 + 额外 SM 5 + 纯 exotic 7 = 27
- **I11 [CORRECTED]** r443/r446「Y 不代选」精确化：反常恒零 ⇒ 反常不约束 (a,b)；SM 匹配可唯一确定，BOUNDARY 降级为约定依赖
- **I12 [BOUNDARY]** 27 含 exotic 需额外机制：g(3,1)_{-1/3}、额外 d^c/L 副本、Y=1/2 双态与 ν^c 需质量/破缺机制，不属 TUFT 导出
- **I13 [INFO]** 与 r446 门禁对照：r446 的 grav-U1 门禁对 trinification 判 N/A，本册给出恒零证明，门禁可补记
- **I14 [INFO]** 全局记分板不变：0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3 不升 L4
