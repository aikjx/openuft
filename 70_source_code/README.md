# 70_source_code/ · Python 源码

> Python 包 `triad_uft` 的源码、测试、示例、验证脚本。

## 当前状态

**等待 triad_uft 包迁移**（详见 [docs/DESIGN_DECISIONS.md ADR-008](../docs/DESIGN_DECISIONS.md)）。

## 计划结构

```
70_source_code/
├── triad_uft/          # 工业级 Python 包（20 模块，72 测试）
│   ├── __init__.py
│   ├── core.py          # 核心数据类
│   ├── proof.py         # TS1-TS12 严格证明实现
│   ├── verify.py        # sympy/mpmath 验证
│   ├── physics.py       # 物理常数、PDG 数据
│   └── ...
├── tests/
│   └── test_*.py        # 单元测试（72+）
├── examples/
│   └── demo_*.py        # 应用示例
└── verify/
    └── verify_*.py      # 验证脚本
```

## 集成计划（v4.x → v5.0）

- v4.1.0：通过 git submodule 引入 triad_uft
- v5.0.0：完全整合到本仓库

## 临时占位（直到正式迁移）

如果你是贡献者，请暂时把代码放 `99_inbox_future/` 或者本地 work-in-progress，**不要**直接创建 `70_source_code/triad_uft/` 文件（避免破坏未来的模块化整合）。

— AI 科技星
