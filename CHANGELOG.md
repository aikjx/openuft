# CHANGELOG.md · openuft 全维统一场论研究进展追踪

> **跟踪原则**：每次有实质进展（理论突破 / 实验对标 / 代码升级 / 论文版本）必追加一条
> **时间戳**：GMT+8
> **当前版本**：v4.0
> **格式**：遵循 [Keep a Changelog](https://keepachangelog.com/) + [Semantic Versioning](https://semver.org/)

---

## [Unreleased]

### Added（计划中 · v4.x）
- `P11_弯曲时空_R12/`：Schwarzschild 度规下三重奏精确证明（R12 / TS13）
- `P12_FRW_R13/`：宇宙学三重奏（R13 / TS14）
- `docs/OPEN_PROBLEMS.md`：扩展开放问题清单（与 A4 同步）
- `triad_uft` 子模块集成至 `70_source_code/`（ADR-008）

### Changed
- 无

### Fixed
- 无

---

## [4.0.2] - 2026-09-06 23:57 — 目录小写化

### Changed（核心变更）
- **目录名**：`openUFT/` → **`openuft/`**（小写，对齐 GitHub URL `github.com/aikjx/openuft.git`）
- **批量替换**：所有 `.md` / `.py` / `.cff` / `LICENSE` 文件中的 `openUFT` 字面改为 `openuft`（71 处）
- **URL 同步**：`github.com/aikjx/openUFT` → `github.com/aikjx/openuft`（所有文件）
- **Python 缓存清理**：删除全部 `__pycache__/`（防 .pyc 文件残留旧名）

### Constraint Note
- 旧目录 `openUFT/` 因 Windows 进程锁定（`WinError 5` Permission Denied）**无法自动删除**
- **用户需手动删除**（详见 `openuft_小写化报告.md` 操作步骤）
- 旧目录 `openUFT_改名与全维整理优化报告.md` 等历史报告文件保留（工作记录）

### Fixed
- verify.py 重跑保持 36/36 通过
- 0 处 `openUFT` 字面残留
- 0 处旧 URL 残留

### 验收
- ✅ `python verify.py` 36/36 通过
- ✅ Markdown: 79 篇
- ✅ Python: 11 个
- ✅ 总文件: 93 · 1.3 MB

---

## [4.0.1] - 2026-09-06 22:34 — 全维整理优化 v2（求导·证明·验证·精算）

### Changed（核心变更）
- **作者统一切换**：`莫国子 / Guozi Mo / 算法联盟 ROOT` → **AI 科技星（AI Tech Star）**
  - 60+ 文件批量替换
  - LICENSE / CITATION.cff / README.md / docs 全部更新
  - 组织名保留「AI 科技星实验室（Algorithm Alliance）」作为方法论传承
- **`00_index/全维分析报告.md`** 新建（10 节 · 整合 D/P/V/A 四主轴一张总表）

### Added
- **`00_index/全维分析报告.md`** ★ 全项目一表总览（10 节）
- **`docs/DESIGN_DECISIONS.md` ADR-009**：作者署名切换决策记录
- **`verify.py`** 白名单扩展（识别「全维分析报告.md」的历史叙述提及）

### Fixed
- README 顶部：`项目代号` → `作者：AI 科技星`
- README 末尾：补充「八、关于作者」独立小节

### 验证状态
- ✅ verify.py：36/36 通过
- ✅ Markdown：74 篇
- ✅ AI 科技星署名：72 处
- ✅ 历史叙述提及：4 处（合法）

---

## [4.0.0] - 2026-09-06 ★ 当前首发版

### Added（首次完整发布）
- **项目改名**：`alg_uft_unified/` → `openuft/` （ADR-001）
- **顶层入口文档（11 件）**：
  - `README.md` · 项目入口
  - `INDEX.md` · 文件索引
  - `CHANGELOG.md` · 本文件
  - `MIGRATION_GUIDE.md` · 迁移指南
  - `WORKFLOW.md` · 工作流
  - **`ROADMAP.md`** · 18 个月路线图
  - **`FAQ.md`** · 50 个常见问题
  - **`QUICKSTART.md`** · 5 分钟上手
  - **`CONTRIBUTING.md`** · 贡献指南（5 步流程）
  - **`LICENSE`** · MIT
  - **`.gitignore`** · Python / Node / OS / Editor
  - **`CITATION.cff`** · 学术引用规范
- **二级目录索引（17 件）**：
  - `00_index/定理谱系总表.md` · TS1-TS12 总览
  - `40_A_精算_audit/A4_诚实声明OpenProblems/开放问题清单_L0-L2.md` · O-1 ~ O-12 详细描述
  - `P3_归纳闭合_R9/README.md` · R9 ★ 重点
  - `P4_绝热三重奏_R10/README.md` · R10 ★ 重点
  - `P5_梯度磁场精确性_R11/README.md` · R11 ★ 重点
  - `99_inbox_future/README.md` · 无限扩展机制
  - `12 个一级目录 README` · 每个主轴的子说明
- **docs/ 文档库（8 件）**：
  - `docs/README.md` · docs 子目录总览
  - `docs/GLOSSARY.md` · 术语表
  - `docs/THEOREMS.md` · 12 定理详细展开
  - `docs/EXPERIMENTAL_CROSS_VALIDATION.md` · 48 项验证矩阵
  - `docs/OPEN_PROBLEMS.md` · 与 A4 同步
  - `docs/MATHEMATICS.md` · 数学结构
  - `docs/NUMERICAL_METHODS.md` · 数值方法
  - `docs/BIBLIOGRAPHY.md` · 完整参考文献
  - `docs/DESIGN_DECISIONS.md` · 8 项架构决策 (ADR-001 ~ ADR-008)
- **GitHub 模板（4 件）**：
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `.github/ISSUE_TEMPLATE/question.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`
- **验证脚本**：`verify.py`（一键检查 36 项可验证项）
- **55 篇历史文档**完整迁移

### Changed（结构改造）
- **目录架构**：12 一级目录 + 66 二级目录 + 80+ 三级文件
- **4 方法主轴**清晰：求导 D + 证明 P + 验证 V + 精算 A

### Deprecated
- `alg_uft_unified/` 命名（已废弃，全文替换为 openuft）

### Removed
- 无

### Fixed
- 无（首次发布无需 fix 历史）

### Security
- 无已知安全问题

---

## [4.0-pre] - 2026-09-06 21:48 — 方法分层骨架完成

### Added（内部骨架）
- `openuft/` 项目根目录建立（原 `alg_uft_unified/`）
- **12 个一级目录**（按"求导·证明·验证·精算"四方法主轴 + 物理领域 + 应用 + 代码 + 可视化 + 论文 + 历史 + 未来扩展）
- **50+ 个二级目录**（每个一级目录下展开）
- **顶层核心文档（初始）**：README.md / INDEX.md / CHANGELOG.md / MIGRATION_GUIDE.md / WORKFLOW.md

---

## [3.x] - 历史档案（详见 `95_history_archive/`）

### [3.6.0] - 2026-07-31 — 质量谱几何化
- GAQ-UFT v6：三代费米子 Cl(4,4) 分类

### [3.5.0] - 2026-07-31 — cħ 几何化
- GAQ-UFT v5：c 与 ħ 的几何化

### [3.4.0] - 2026-07-30 — 全维统一
- GAQ-UFT v4：全维统一顶尖论文

### [3.3.0] - 2026-07-29 — 三大新体系
- GAQ-UFT v3：三大新体系（连续积分、Clifford 几何、分形-类分形）

### [3.0.0] - 2026-07-29 — 三大新体系完整

### [2.0.0] - 2026-06-15 — 前端 README（已退役）

---

## 版本对照表

| 版本 | 日期 | 代号 | 主要变化 |
|---|---|---|---|
| 4.0.0 | 2026-09-06 | **正式首发版** | 项目改名 + 全维整理优化 |
| 4.0-pre | 2026-09-06 | 方法分层骨架 | 内部骨架阶段 |
| 3.6.0 | 2026-07-31 | 质量谱 | Cl(4,4) 分类 |
| 3.5.0 | 2026-07-31 | cħ 几何化 | c 与 ħ 几何化 |
| 3.4.0 | 2026-07-30 | 全维统一 | 顶尖论文 |
| 3.3.0 | 2026-07-29 | 三大新体系 | 完整版 |
| 3.0.0 | 2026-07-29 | 三大新体系 | 初版 |
| 2.0.0 | 2026-06-15 | 前端 README | 已退役 |
| 1.x | 2026-06 前 | 内部研发 | 个人探索 |

— AI 科技星 · 2026-09-06
