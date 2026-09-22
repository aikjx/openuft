# 结构审计与执行记录

[返回治理](../README.md) · [验证说明](../VALIDATION.md)

- [当前目录审计](DIRECTORY_AUDIT.md) 与 [机器数据](directory_audit.json)：由 audit_directories.py 生成。
- [体系拆分执行记录](independent_systems_execution.json)：历史命令与输出。
- [本次目录迁移记录](layout_reorganization_20260909.json)：路径映射及迁移前后摘要。

审计文件描述检查范围和执行结果，不认证物理理论。目录结构变动后，从项目根运行 `python -B 00_项目治理/维护工具/audit_directories.py`。
