# ROOT V104｜369 项全量台账修复与螺旋动力学逆问题验证

> **重要：没有证明完整统一场论。** 这是一个可复现的数学/物理诊断包，重点解决历史 369 行任务台账的重复 ID 与缺少验收条件问题，并证明电磁反问题的秩条件、几何曲率和时空曲率的区分、空间结曲率判据的逆命题错误。全部样本数据均为 THEORY 或 SYNTHETIC，不是实验观测。

## 完成范围

- 审计原 V103 的 369 行历史研究任务；发现旧 ID 仅有 345 个唯一值（24 个 H01—H24 编号重复）。
- 在 `ledger/ALL_369_AUDITED.csv` 中生成 **369 个唯一 `canonical_id`**，保留 `id` 原值及 `source_version`。
- 为原始 32 条缺失验收条件补充 `supplemental_acceptance_if_missing`，完全保留原始缺失字段以保证来源诚实。
- 把“旧数学公式诊断闭合”和“物理本源被证明”拆开，不再用 `CLOSED_MATH` 当成四力统一成功。
- 严格证明单个速度探针局部 EM 反问题秩 3、两个不同速度一般秩 5、三组非共线速度差秩 6。
- 精算局部场反演的病态条件数随速度夹角的变化；合成数据恢复电场和磁场。
- 证明一条平面、无自交、无结闭曲线也可有总曲率大于 4π，因此不能靠曲率阈值反推结类型。
- 继续保留相对论 Frenet 动力学、Lorentz boost 和经典辐射的历史理论基准。
- 独立检查 V103 28 项旧测试，历史 V103 ZIP 在 `archive/ROOT_V103_original.zip`。

## 目录

| 路径 | 用途 |
|---|---|
| `research/01_统一场论全量审计与科学裁定.md` | 科研总论、公式、限制与下一步 |
| `research/02_严格证明_反问题秩和拓扑反例.md` | 定理与反例完整证明 |
| `research/03_可证伪实验与误差管理.md` | 多速度反演实验设计、统计条件 |
| `research/04_369项逐行验收表.md` | 完整 369 行的可浏览逐行任务 |
| `ledger/LEGACY_369_ORIGINAL.csv` | V103 原始 369 行，未修改 |
| `ledger/ALL_369_AUDITED.csv` | 唯一 ID、来源状态、补充验收准则 |
| `ledger/EVIDENCE_STATUS_COUNTS.json` | 研究证据分级计数 |
| `src/v104_core.py` | 物理/几何/逆问题计算引擎 |
| `src/dimensions.py` | SI 量纲一致性审计 |
| `src/audit.py` | 历史研究台账一致性审计 |
| `src/symbolic.py` | SymPy 符号检查 |
| `src/generate.py` | 图表、表格及数值报告重算 |
| `tests/test_v104.py` | pytest 自动数学测试 |
| `web/index.html` | 无联网依赖的互动场反演实验室 |
| `web/browser_smoke.py` | Chromium 实测（可选，需要 Playwright + Chromium） |
| `archive/ROOT_V103_original.zip` | 历史版本压缩包，用于独立验收 |
| `data/V100_ORBIT_21Q_INPUT_THEORY.csv` | 历史模拟轨道，绝非真实观测 |
| `results/` `figures/` | 可复算模型输出和科研图 |
| `CHECKSUMS.sha256` `MANIFEST.json` | 发布时文件校验 |
| `verify_integrity.py` | 校验发布原始文件 SHA-256 |

## 运行方式

Python 3.10+：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

如果浏览器可用：

```bash
python -m pip install playwright
python web/browser_smoke.py
```

历史回归：先解压 `archive/ROOT_V103_original.zip` 到单独目录，再从其项目目录执行 `python -m pytest -q tests`，不能依赖本次主包的 76 项测试替代历史测试。

**第一次发布校验：**

```bash
python verify_integrity.py
```

请先校验哈希再重新生成图表；不同系统的 Matplotlib 图片元数据/字体可能导致重新生成后的 SHA-256 不同，不能因此认定发布 ZIP 被篡改。

## 可以称为完成的事情与不能称为完成的事情

- ✅ 原项目文件、369 行台账全部逐行读取并生成可审查状态；重复 ID 与 32 条无验收准则均已修复（新增 ID 不覆盖原 ID）。
- ✅ 本轮严格数学定理、数值逆问题、单位检查和离线实验室完成；执行记录见 `VALIDATION_REPORT.md`。
- ✅ 完整科研包和历史数据可独立解压复运行。
- ❌ **不能**宣称 369 个科学问题全部解决；不能声称 4 力统一、量子引力、高能 UV 完备或不含输入 G 的新 G 公式已得到证明。
- ❌ V100 数值轨道的连续存在性、真实结拓扑和无限时间稳定性仍未由严格误差界认证。
- ❌ 没有搭建或运行真实电磁/引力装置，全部结果是数学与合成模拟。

## 证据规则

所有条目用真实科学判据分级，不用单元测试数量替代科学正确性。若任务需要真实数据、实验许可或独立第三方审查，保留为未完成；不制造不存在的实验报告。
