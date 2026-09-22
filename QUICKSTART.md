# 快速开始

[English](05_全球研究/03_多语种协作/英语/项目介绍.md) · [日本語](05_全球研究/03_多语种协作/日语/项目介绍.md) · [参考文献](02_共享基础/参考资料/BIBLIOGRAPHY.md)


1. 阅读 [全球研究路线](05_全球研究/02_全球路线/README.md)，了解外部理论与本地体系的边界。
2. 在 [体系分类](01_独立体系/TYPE_INDEX.md) 选择中文体系目录，核对 system.json、公设与来源。
3. 新命题登记到所属体系 claims.csv；未知资料进入“99_待整理资料”。
4. 在项目根运行 `python -B verify.py`。
5. 三重奏复算：进入 `01_独立体系/S01_螺旋三重奏与谱几何/07_计算复现/源码`，执行 `python -B -m 三重奏统一场.verify`。
6. 跨体系对照：阅读 [统一架构总纲](06_统一体系层/统一架构/统一架构总纲.md)，再看 [体系关系图](06_统一体系层/关系体系图/体系关系图.html)。

修改登记或目录后，依次运行：

```sh
python -B 00_项目治理/维护工具/module_catalog.py refresh
python -B 00_项目治理/维护工具/global_catalog.py refresh
python -B 00_项目治理/维护工具/audit_directories.py
python -B 00_项目治理/维护工具/refresh_catalog.py
python -B verify.py
```
