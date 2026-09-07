# 共享计算工具

现有源码位于 [src/triad_uft](src/triad_uft/)。H01 与 H04 的既有复算脚本依赖此库，因此保留一个共享实现。库中的理论假设与证据标签继承历史版本，未在目录迁移中科学审定。

从本目录的 src 执行 `python -m triad_uft.verify`。各模型专属代码放在各自 07_computation/src。环境与依赖以实际运行记录为准。
