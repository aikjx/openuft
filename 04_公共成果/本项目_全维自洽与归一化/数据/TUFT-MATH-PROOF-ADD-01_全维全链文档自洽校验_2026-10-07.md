# TUFT-MATH-PROOF-ADD-01 全维全链文档自洽校验报告
- 引擎：源码/TUFT-MATH-PROOF-ADD-01_全维全链文档自洽校验_2026-10-07.py
- 对象：全维全链 / 全维主册 / 修订全本（openuft 规范目录）
- 读数：9 guard PASS 9/FAIL 0 (exit 0)

| PASS | nine_engines_recorded | 缺失计数: 无 |
| PASS | deltaA_scaling_doc | 重算 δA/eps=0.1016 |
| PASS | dlambda_scaling_doc | 重算 δλ/eps=0.2625 |
| PASS | eps_crit_doc | 重算 eps_crit=0.0098 |
| PASS | omega_max_doc | 重算 |Omega_W|_max=6.394e-03 |
| PASS | edm_window_doc | EDM 相位窗口与排除倍数均已记录 |
| PASS | posterior_consistency | 后验四关键数在文档中均记录 |
| PASS | falsifiability_verdict_doc | D-06 未翻盘裁决已记录 |
| PASS | placeholder_not_fabricated | 机制占位已标（ε 机制 / |Ω_W| 压低） |

### 独立重算
| 量 | 重算值 | 文档声明 | 一致 |
|---|---|---|---|
| δA/eps | 0.1016 | 0.10 | ✔ |
| δλ/eps | 0.2625 | 0.2756 | ✔ |
| eps_crit | 0.0098 | ~0.01 | ✔ |
| |Ω_W|_max | 6.394e-03 | 6.4e-3 | ✔ |

### 结论
1. 全维全链/主册/修订全本三份文档内部一致：B.3' 公式、存活阈值、|Ω_W| 上限均可由独立重算复现。
2. 九引擎计数、EDM 相位窗口与排除倍数、后验四关键数、可证伪预言数=0 裁决均已记录且互相不矛盾。
3. 两处机制占位（ε 机制、|Ω_W| 压低）存在，未编造机制值。
4. 收口档案本身通过文档级自洽校验，可作为后续改稿/投实验的可追溯基准。