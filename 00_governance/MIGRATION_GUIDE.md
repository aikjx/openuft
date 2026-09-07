# 2026-09-07 全生命周期重布局

原始文件全部纳入快照和逐文件 SHA-256 清单；已有暂存与未暂存修改均按迁移开始时磁盘内容保留，未执行 git reset、提交或暂存。

| 原目录 | 新目录 |
|---|---|
| 00_index | 00_governance/catalog |
| 01_hypotheses | 01_models |
| 02_comparison | 03_comparative/comparison |
| 03_research_protocol | 02_shared/protocols |
| 04_synthesis | 03_comparative/synthesis |
| 50_physics_domains | 03_comparative/physics_domains |
| 60_application | 03_comparative/applications |
| 70_source_code | 02_shared/computation |
| 80_visualization | 04_publications/visualizations |
| 90_paper_论文 | 04_publications/legacy_reports |
| 95_history_archive | 90_archive/legacy |
| 99_inbox_future | 99_inbox |
| docs | 02_shared/references |

原 00–08 阶段按语义迁入新阶段；空的 D/P/V/A 遗留目录移除。旧 verify.py 与 reorganize_structure.py 存入 legacy_tools，当前 verify.py 采用新结构。修复三处复算入口对共享源码的路径查找。历史综合论文与 GAQ 系列保留整体归档，归属未审定时不强行划入单一假设路线。

[迁移清单](../90_archive/migrations/20260907_full_layout/manifest.json) · [完整快照](../90_archive/migrations/20260907_full_layout/before.zip)

校验命令：`python verify.py`。快照只作恢复依据；历史文本中的旧路径与历史工具不代表当前运行约定。
