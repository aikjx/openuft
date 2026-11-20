# ROOT V103｜研究代码与复现包

**未证明完整统一场论。** 本包为经典电磁力、空间结几何、辐射补偿的条件数学推论与历史模拟复算。所有图片、数据为 THEORY，不是观测结果。

## 内容

- `src/v103_core.py`: 数值核心；包括非平凡结辐射下界、供能下界、洛伦兹 boost 的挠率反例、离散轨迹曲率积分。
- `src/symbolic.py`: 9 项 SymPy 代数和 SI 量纲审计。
- `src/generate.py`: 使用 V100 原轨迹（存自 V102）计算 CSV/JSON 和两张图。
- `tests/test_v103.py`: 28 项 pytest 测试。
- `data/`: V100 轨迹（非观察数据）；`results/`、`figures/`: 合成计算结果。
- `research/`: 中文严谨推导、假设及不足。
- `ledger/`: 原 V102 的 357 项与 12 项新问题，共 369 项。
- `archive/ROOT_V102_original.zip`: 上一版原始归档，供独立历史检查。
- `web/index.html`: 完全离线的参数化互动页面，无外部依赖。
- `CHECKSUMS.sha256`: SHA-256 完整性清单；`MANIFEST.json`: 文件元数据。

## 运行

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q tests
```

历史 V102 复测可解压 `archive/ROOT_V102_original.zip` 后在其根目录运行 `python -m pytest -q tests`。不要求浏览器联网。

**验收边界**：单元/符号测试只保证代码对指定模型的正确性；严格的连续线圈场周期轨道存在性、三维结拓扑证明、反作用自洽、四力统一仍 OPEN。
