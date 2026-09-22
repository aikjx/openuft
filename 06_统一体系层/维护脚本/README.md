# 维护脚本

[统一体系层](../README.md)

- `build_layer_core.py`：生成本层核心文档、实现方式总表、体系坐标表。
- `build_impl_dossiers.py`：生成实现方式档案与关系图谱、关系图 HTML。

脚本只写入 `06_统一体系层`，不修改 `01_独立体系` 的身份文件。运行方式：

```bash
python -B 06_统一体系层/维护脚本/build_layer_core.py
python -B 06_统一体系层/维护脚本/build_impl_dossiers.py
```
