# openuft 全维守卫工具链 —— 统一入口

> 全维分形知识自动演化引擎的「企业级多域守卫」：硬校验 + 扩展域软检查 + 写入门禁 + 隔离自测 + 列语义审计。
> 红线：所有工具纯校验编排，不篡改任何 CURATED 真源；裁定项须由所属方批准后另行执行。

## 一、工具清单与职责

| 工具 | 职责 | 调用 |
|---|---|---|
| **`guard_all.py`** | 多域守卫。复用 verify.py 硬校验（决定退出码）+ 扩展域软检查：域A claims 结构、域B claims 语义（evidence 词表 / 单字母分级 / 长文本 / 裸 VERIFIED / status 串列 / **status 非法词**）、域C system 身份（必填 / A1 schema）、域D 夸大词 | `python guard_all.py`<br>`python guard_all.py --json` |
| **`guard_install.py`** | 写入门禁安装器。追加式 pre-commit、MARK 幂等、备份、逃生门 | `--status` `--install` `--uninstall` `--test` |
| **`guard_selftest.py`** | 隔离自测。tempfile 夹具，负向检出 + 正向无误报 + 逃生门 + JSON | `python guard_selftest.py` |
| **`claims_columns_audit.py`** | 列语义对账审计。全 01_独立体系 claims.csv 逐列形态对账 + **表头归一化对账**，识别列语义串列（evidence/status/reviewer/uncertainty） | `python claims_columns_audit.py`<br>`--json` |
| **`apply_remap.py`** | 列重映射执行器（OPEN-B8/B9/B10）。dry-run 默认预览，`--apply` 改写真源（S14 右移还原） | `python apply_remap.py [--apply]` |

## 二、门禁工作流

```
编辑治理资产(claims.csv/system.json/layout/verify.py/维护工具/审计记录/迁移记录)
  → git commit
  → pre-commit [openuft 全维守卫段]
  → guard_all.py：verify 硬校验(PASS?)+扩展域软检查
  → PASS → 提交放行；FAIL → 阻断(exit 1)
```

触发正则（只触发核心治理资产，体系内容不触发）：
`claims.csv|system.json|layout.json|system_registry.json|module_types.json|chapter_provenance.json|^verify.py|00_项目治理/维护工具/|00_项目治理/审计记录/|90_历史归档/迁移记录/`

## 三、逃生门

- `git commit --no-verify`（绕过 pre-commit）
- `OPENUFT_GUARD_SKIP=1`（guard_all 内部跳过）
- `OPENUFT_GUARD_FORCE=1`（强制，忽略 SKIP）
- TUFT 卷系门禁段保留共存，`TUFT_HOOK_FORCE=1` 兼容

## 四、已登记 OPEN / 待裁定（不擅自改真源）

| 项 | 内容 | 状态 |
|---|---|---|
| OPEN-B8（S15） | **无行级错位**；evidence_level 列被单字母分级值（H）污染（值语义） | 画像已精确化，待 S15 所属方裁定 |
| OPEN-B9（S14） | **真错位 10 行**（整体右移 1 列，尾缀多余列）+ evidence_level/status 值污染 + 85 空行 | 画像已精确化，待裁定 |
| OPEN-B10（S17） | **无行级错位**；evidence_level 列单字母分级（40 行）（值语义） | 画像已精确化，待裁定 |
| 空行清理 | S14 85 / S15 31 / S17 41 个 CSV 空行（格式问题，非列错位） | 保留与否待所属方定 |
| **列重映射方案** | 见 `审计记录/列重映射裁定方案.md`（S14 精确改法 + S15/S17 待核 + 空行选项） | **方案就绪，批准即执行** |
| **status 自定义词** | `unreproduced`(P03×2/S12×3/S15×6)、`repaired`(S05×2/S06×3)、`structural_failure`(S09×1) ∉ 标准 STATUS_WORDS | 域B 新增非法词检测已检出，待裁定：纳入词表 or 数据规范化 |
| A1 schema | 23 体系缺 ontology/freedom_degrees/degrees_of_freedom/scale；owner 空缺 | 模板已补强，真实体系待回填 |
| 12 体系长文本 | **已修正为误判**：evidence_level 长文本多为合法组合词超阈值（域B 已加 `and not ok`），仅 S14 右移污染为真 | 已闭环（S14 并入列重映射） |

## 五、验证基线

- verify 硬校验：22 体系 / 17 阶段 / 12837 链接，FAIL 0
- guard_all：PASS（3 WARN / 548 INFO，待裁定项豁免）
- guard_selftest：14/14 PASS
- 端到端门禁：commit 触发守卫 PASS，可安全回滚验证
- 备份：`openuft/.git/hooks/pre-commit.bak.*`
- **表头归一化（架构层实证）**：23/23 体系 claims.csv 权威表头 14 列 schema 完全一致——claims 架构归一化达成；**错位问题全部在数据行值层**（S14 行级 15 列右移 / S15·S17 值落错列），表头层无差异
