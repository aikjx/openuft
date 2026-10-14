# 清理操作记录 2026-09-27

> 范围：全仓垃圾文件扫描与门禁断链修复；不认证物理理论，仅记录仓库卫生动作。
> 前置门禁：`python -B verify.py`（exit 0 = PASS）。

## 1. 扫描方法

从仓库根递归遍历，排除 `.git`、`90_历史归档`、`__pycache__`、`.pytest_cache`；按文件名模式
`*.bak / *.old / *.tmp / Thumbs.db / ~$* / _tmp* / *_out.txt` 粗筛后，逐文件用 `git ls-files --error-unmatch`
与 `git status --porcelain` 区分「已跟踪证据」与「未跟踪临时产物」，再决定去留。

## 2. 处置结果

| 路径 | 性质 | 处置 |
|---|---|---|
| `04_公共成果/本项目_全维自洽与归一化/源码/_tmp_check.pyc` | 未跟踪编译缓存（35 KB），由 `_tmp_probe_ym.py` 运行生成 | **删除** |
| `00_项目治理/资料索引/material_catalog.md` 第 2308 行 | 指向已删 pyc 的目录条目，门禁报断链 | **摘除该条目**（保留 BOM，diff 仅 1 行删除） |
| `01_独立体系/S02_空间光速螺旋统一力/04_理论推导/*_out.txt`（4 个） | 已跟踪且干净，S02 provenance 引用的数值复跑日志 | **保留**（粗筛误报，非临时产物） |
| `04_公共成果/.../源码/_tmp_probe_ym.py` | 已被并行会话提交入库 | **保留** |
| `书籍/v1_正文/第十二编.../*.bak`（45 个） | 写书会话的版本回滚备份（`pre_vNN` / `YYYYMMDD_vNNpre` 命名约定） | **不动**（属该会话工作流） |
| `01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/claims.csv` | 复核：现 14 列表头、0 数据行；此前普查发现的 30 行 × 16 列漂移已被并行会话修复 | **无需动作** |

## 3. 提交

- `ec97d7c` — chore(资料索引): 摘除已删除编译缓存 `_tmp_check.pyc` 的目录条目，修复门禁断链；无内容变更。
  - 提交前执行 `git reset HEAD -- .` 清空 index，再单独 `git add` 本文件，避免卷入并行会话暂存改动。

## 4. 复跑门禁

删除 pyc 后首次复跑报 1 条断链（即 catalog 条目）；摘除条目后复跑：

```
Systems/directions: 19; lifecycle stages: 17; local links: 9914; snapshot originals: [193, 393]
PASS
```

## 5. 未处理项（归属并行会话，不代做）

- 工作树大量未提交改动：P01–P04 立项文件与脚本、`02_TUFT_复算/`、`04_公共成果` 批量新报告与数值 json/py、`07_统一场方程` 多文件、`书籍/v1_文书` 多篇文章。由各会话按自己的提交节奏入库。
- S05 claims.csv 两条 `status='repaired'`（己方公式 H2/H3 自纠错记录）：语义不可机械映射为 verified/falsified，待 S05 负责人判定。
- 跨体系审计报告见 `03_跨体系研究/跨体系_claims体例合规审计_20260926.md`（提交 `8ad26da`）。


---

# 追加段：2026-10-14 门禁断链清零（130 → 0）

> 前置门禁：`python -B verify.py`（exit 0 = PASS）。并行会话 9-27 大推进后门禁 FAIL(130)，本轮修复至 PASS。

## 1. 处置结果

| 断链类别 | 数量 | 处置 |
|---|---|---|
| material_catalog 引用 .git 内部对象 | 120 | 上轮已摘除 .git 段(188 行) |
| catalog 索引 _shots/*.jpg（审计收官报告 2 + 攻破总报告 4） | 6 | **摘除过期索引**（jpg 不存在，仅 html/md 存在） |
| 62_文档引用 第十五编 README（未建） | 2 | 链接改纯文本 + 标注 README 待建（不代建） |
| 本项目_统一场论攻破/README.md 引用 scratch/A22_readme_register.txt | 1 | 去链接语法，保留反引号文本 |
| TUFT-r63 `[L²](废式)` | 1 | 改全角括号断开 `](` 结构（反引号转义对 verify 正则无效） |

> 全部为纯机械转义/摘除，不改物理语义；并行会话在途引用仅断链处理、不代建文件。

## 2. 提交

- `31d80726` — fix(openuft): 门禁 verify.py 断链清零（4 文件 +4/−198）；提交前 reset index 仅 add 本 4 文件。

## 3. 复跑门禁

```
Systems/directions: 22; lifecycle stages: 17; local links: 18370; snapshot originals: [193, 393]
PASS
```

## 4. 未处理项

- 第十五编 README.md 待并行会话创建（建成后 62 文档可恢复链接）。
- 工作树仍存并行会话未提交改动（S02 §28–30、S15 V9.x、TUFT-r65、07 层 38/39/40 等），由各会话自提。
