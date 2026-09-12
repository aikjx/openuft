# 07_计算复现

所属独立体系：[全域双向分形统一场论](../README.md)。

验证脚本与复现方法；代码存在不等于物理成立，运行结果以 09_验证结果 与 claims.csv 的登记为准。

[身份与基础前提](../system.json) · [来源](../sources.md) · [证据登记](../claims.csv)

## 源码（6 个脚本，可原样重跑）

| 脚本 | 覆盖 | 命令 |
|---|---|---|
| [verify_unified_theory.py](源码/verify_unified_theory.py) | 第12/14章 实验一–八（流守恒、β、分形、度规、曲率、畴） | python verify_unified_theory.py |
| [diagnose_winding.py](源码/diagnose_winding.py) | 第15章 实验九诊断（绕数崩溃、∫J⁰、λ=0 对照） | python diagnose_winding.py |
| [hopf_verify.py](源码/hopf_verify.py) | 第7/14章 实验十/十一（霍普夫荷收敛、整数谱、形变保护） | python hopf_verify.py |
| [hopf_control.py](源码/hopf_control.py) | 第7/15章 实验十二对照（平方映射高分辨率、自由场 3D 不保护） | python hopf_control.py |
| [higgs_verify.py](源码/higgs_verify.py) | 第8/14章 实验十三–十五（对偶帧酉性、模式谱、未破缺 U(1)） | python higgs_verify.py |
| [dimension_unify_verify.py](源码/dimension_unify_verify.py) | 第17/19/20章 验证A–E（量纲谱、参数自洽、常数比例、依赖图、归一化） | python dimension_unify_verify.py |

## 运行记录

- [run_template.json](运行记录/run_template.json)：全套复现命令与环境（Python 3.14.7 + numpy 2.5.2，谱方法/保守晶格原生实现，无第三方求解器依赖）。
- 主脚本已于 2026-09-12 实跑：五项实验全部完成，输出与 [验证精算报告](../09_验证结果/验证精算报告_V1.2.md) 一致（实验九拓扑荷漂移 0.9985 为预期证伪信号）。
- 实验九（Q: 1→0）、实验十二（+0.875→-0.162）为**预期的反证输出**，出现即说明代码正确复现了理论升级动机，不是故障。
