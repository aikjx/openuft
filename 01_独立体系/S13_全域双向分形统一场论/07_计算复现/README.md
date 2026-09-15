# 07_计算复现

所属独立体系：[全域双向分形统一场论](../README.md)。

验证脚本与复现方法；代码存在不等于物理成立，运行结果以 09_验证结果 与 claims.csv 的登记为准。

[身份与基础前提](../system.json) · [来源](../sources.md) · [证据登记](../claims.csv)

## 源码（14 个脚本，可原样重跑）

| 脚本 | 覆盖 | 命令 |
|---|---|---|
| [verify_unified_theory.py](源码/verify_unified_theory.py) | 第12/14章 实验一–八（流守恒、β、分形、度规、曲率、畴） | python verify_unified_theory.py |
| [diagnose_winding.py](源码/diagnose_winding.py) | 第15章 实验九诊断（绕数崩溃、∫J⁰、λ=0 对照） | python diagnose_winding.py |
| [hopf_verify.py](源码/hopf_verify.py) | 第7/14章 实验十/十一（霍普夫荷收敛、整数谱、形变保护） | python hopf_verify.py |
| [hopf_control.py](源码/hopf_control.py) | 第7/15章 实验十二对照（平方映射高分辨率、自由场 3D 不保护） | python hopf_control.py |
| [higgs_verify.py](源码/higgs_verify.py) | 第8/14章 实验十三–十五（对偶帧酉性、模式谱、未破缺 U(1)） | python higgs_verify.py |
| [dimension_unify_verify.py](源码/dimension_unify_verify.py) | 第17/19/20章 验证A–E（量纲谱、参数自洽、常数比例、依赖图、归一化） | python dimension_unify_verify.py |

### V1.3–V1.8 追加脚本

| 脚本 | 覆盖 | 命令 |
|---|---|---|
| [yang_mills_verify.py](源码/yang_mills_verify.py) | V1.3 拼图一（联络 u(2)、几何曲率、格点规范不变性、希格斯–金哈质量谱） | python yang_mills_verify.py |
| [consistency_verify.py](源码/consistency_verify.py) | V1.3.1 口径闭合（弱混合角、质量比、四观测四未知） | python consistency_verify.py |
| [fermion_family_verify.py](源码/fermion_family_verify.py) | V1.4 拼图二（$\mathbb{Z}_{4}$ 三实表示、每代六反常消去、第四代禁戒） | python fermion_family_verify.py |
| [color_su3_verify.py](源码/color_su3_verify.py) | V1.5 拼图三（$\mathfrak{su}(3)$ 李代数、$\mathbb{CP}^{2}$ 等距与稳定子、色单态判据） | python color_su3_verify.py |
| [quantum_brst_verify.py](源码/quantum_brst_verify.py) | V1.6 量子化层（BRST 幂零、单圈 $\beta$ 系数、渐近自由窗口） | python quantum_brst_verify.py |
| [constant_unify_verify.py](源码/constant_unify_verify.py) | V1.6 常数统一（参数对接、电荷量子化、$\sin^{2}\theta_{W}$ 候选、$\Lambda$ 边界） | python constant_unify_verify.py |
| [running_unify_verify.py](源码/running_unify_verify.py) | V1.7 统一跑动（三耦合、SM 单圈不统一、CP² 候选负面、MSSM 对照） | python running_unify_verify.py |
| [全域统一场论_全维精算_mp.py](源码/全域统一场论_全维精算_mp.py) | V1.8 50 位精算（P1–P10 共 25 项闭式核查，全 PASS / 机器零） | python 全域统一场论_全维精算_mp.py |

## 运行记录

- [run_template.json](运行记录/run_template.json)：全套复现命令与环境（Python 3.14.7 + numpy 2.5.2，谱方法/保守晶格原生实现，无第三方求解器依赖）。
- 主脚本已于 2026-09-12 实跑：五项实验全部完成，输出与 [验证精算报告](../09_验证结果/验证精算报告_V1.2.md) 一致（实验九拓扑荷漂移 0.9985 为预期证伪信号）。
- 实验九（Q: 1→0）、实验十二（+0.875→-0.162）为**预期的反证输出**，出现即说明代码正确复现了理论升级动机，不是故障。
- [run-20260915-mp.json](运行记录/run-20260915-mp.json)：V1.8 精算复现（Python 3.8.10 + mpmath 1.3.0，dps=50），25 项核查全 PASS，输出见 [验证精算报告 V1.8](../09_验证结果/验证精算报告_V1.8.md)。
- **精度设置警示**：mpmath 1.3.0 下 `import mpmath as mp; mp.dps = 50` 会静默失效（实际 15 位），必须写成 `from mpmath import mp; mp.dps = 50`（设在上下文对象上）；V1.8 脚本已按此实现。
