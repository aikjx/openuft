# 20261018 ufthub_md_202609 选择性入库（审定迁移）

把 `ufthub/md/202609` 的 28 件审定件写入 `03_跨体系研究/语料审定_ufthub_md_202609/`：
其中 20 件自 `90_历史归档/来源语料_ufthub_20260925/` 待归属分箱**迁出**（移动），8 件自 `ufthub/md/202609/` **复制**（分箱建立后新增的件）。

| 项 | 值 |
|---|---|
| 迁出（move） | 20 件 |
| 新采（copy） | 8 件 |
| 体积 | 490.52 KB |
| 校验 | 每件落位后 md5 与 ufthub 原件逐件断言相等 |
| 逐件账 | [manifest.json](manifest.json)（md5+sha256+新旧路径） |
| 驱动 | `my_lib/_tmp_tools/r60_promote.py`（预演/落位两级） |

## 失效登记

以下旧路径自本轮起不存在，引用它们的既有文本一律以 manifest.json 的新路径为准：

- `90_历史归档/来源语料_ufthub_20260925/` 内 20 件（箱内 `来料清单.csv` 对应行、箱 README 分箱计数为迁移前当下读数，不再逐处改写）；
- `00_项目治理/资料索引/material_catalog.md` 与 `structure_manifest.json` 中上述 19 条旧条目本轮已删并补入新条目。

## 未动之物

- `my_lib/ufthub/md/202609/` 全部原件：未移动、未删除（含 v1 台账与隔离禁词件）。
- 留档 3 件（claims.csv、momentum_darboux.py、oam_tuft_couple_audit.py）仍在 90 分箱原处——它们与现行 S02 版本已分叉，只登记不合并，见处置台账 §四。
