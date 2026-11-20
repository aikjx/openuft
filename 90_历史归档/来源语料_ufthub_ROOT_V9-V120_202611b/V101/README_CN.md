# ROOT V101 · 曲率辐射拓扑与统一场论反例科研包

**版本**：2026-11-19，承接 ROOT V100，类型为数学推导/理论数值/科研程序；**不是新物理实验，也不是四力统一成功**。

## 这一版实际完成的事

- 证明指定经典恒速点电荷非平凡空间结的辐射能量下界 `E_rad ≥ 8π q² γ⁴ v³/(3 ε₀ c³ L)`。
- 从 Maxwell 真空场构造一个“相同圆形参考轨道、不同磁场和不同扰动动力学”的严格反例。
- 通过完整周期能量守恒指出：严格静态外部场无法为持续辐射的精确周期轨道提供净补偿功。
- 独立使用 V100 保存的 1201 点轨道，重新算出曲率与辐射，和原基准误差约 0.00285%。
- 保留 V100 原始 ZIP；合并 337 条历史任务和 12 条新任务，349 条任务可追踪。

## 运行

在解压目录运行（推荐 Python 3.11+）：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

随后打开 `web/index.html` 可使用离线公式实验室。程序会重建 `results/V101_NUMERICAL_SUMMARY_THEORY.json`、`results/BETA_LENGTH_SCAN_THEORY.csv` 和三张图表，并运行新增的 Python 与 SymPy 测试。

历史原始包位于 `archive/ROOT_V100_original.zip`，原版测试需在原包解压目录运行 `python -m pytest -q tests/test_v100.py`（不与 V101 的测试数量混淆）。所有文件校验清单见 `CHECKSUMS.sha256`。

## 资料目录

- `research/ROOT_V101_科研总论.md`：完整数学推导、局域 Maxwell 反例、物理边界及文献。
- `research/严格定理_量纲与反例.md`：T1–T5 定理与条件。
- `research/后续攻坚_正向动力学路线.md`：仍开放的真正统一场论工作。
- `src/v101_core.py`：公式、场不可辨识与独立多边形积分。
- `src/symbolic_checks.py`：符号 Maxwell/量纲检查。
- `tests/test_v101.py`：新增可重复测试。
- `figures/`：理论计算图。
- `ledger/ALL_349_ISSUES.csv`：349 项问题总账。

## 证据等级与限制

PROVEN = 明确数学假设下成立；NUMERIC = 有限精度模拟或数值近似；OPEN = 未验证的基础问题或实验问题。V100 连续场轨道的存在性、真实结拓扑、辐射反作用下的长期稳定及四力统一均为 OPEN。尽管本研究跨越几何、Maxwell 和辐射，它们仍是已知基本物理的约束组合，而不是量子引力的实验发现。
