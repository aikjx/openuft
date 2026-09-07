# 迁移说明（MIGRATION_GUIDE）

本次布局调整把「按方法分目录」改为「按假设体系分目录 + 每条体系自带全链路」。

## 变更前

- 顶层 `10_D_求导_derivation/`、`20_P_证明_proof/`、`30_V_验证_verification/`、`40_A_精算_audit/` 按**方法**横切，与 `01_hypotheses/` 的八阶段脚手架**重复、割裂**，真实研究产出散落于方法目录，假设体系内几乎为空。

## 变更后

- 主分类轴 = `01_hypotheses/` 的 6 条体系（h01–h06），每条体系自成九阶段全链路 `00_假设 → … → 08_结论`（新增 `06_audit` 精算阶段，原 `06_falsification`/`07_conclusions` 顺延为 `07`/`08`）。
- 原方法目录的**真实内容**已并入对应体系：
  - `D5_大统一力方程` → `h01_space_motion/02_derivations/`（空间运行产生力）
  - `D0_作用量变分求导` → `h04_geometry_action/02_derivations/`（几何作用量）
  - `P1/P3/P4/P5/P6` 螺旋三重奏与谱理论证明 → `h01_space_motion/03_proofs/`
  - `V2_mpmath高精度` → `h01_space_motion/05_verification/`
  - `A1/A4/A5/A6` 精算方法论 → `03_research_protocol/audit_methodology/`
  - 方法总览 README → `03_research_protocol/method_D_求导.md`、`method_P_证明.md`、`method_V_验证.md`
- 顶层 `10_D/20_P/30_V/40_A` 已移除（内容已并入上述位置）。
- 跨体系公共层保留：`00_index`、`02_comparison`、`03_research_protocol`、`04_synthesis`、`50_physics_domains`、`60_application`、`70_source_code`、`80_visualization`、`90_paper_论文`、`95_history_archive`、`99_inbox_future`、`docs`。

## 待办（如未自动清理）

若工作区仍残留空的 `10_D_求导_derivation/`、`20_P_证明_proof/`、`30_V_验证_verification/`、`40_A_精算_audit/` 目录，直接删除即可（内容已迁出，目录为空）。
