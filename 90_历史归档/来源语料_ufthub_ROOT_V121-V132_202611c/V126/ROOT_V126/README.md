# ROOT V126 — 三大根波的数学验证与物理审计

本研究包采用 c=1，保留 G 与 ħ。S/V/T 是候选的标量、矢量、张量模式，不是已证实的三种宇宙基本波。

## 内容
- `docs/theory.md`: 推导、适用条件、失败模式与四力统一的未解问题
- `src/verify.py`: NumPy 本征值、色散与人工引力基准计算
- `tests/test_verify.py`: 八项可复现测试
- `results/calculations.json`: 数值结果
- `results/test_log.txt`: 测试记录

运行：`python src/verify.py` 和 `python -m unittest discover -s tests -v`。依赖 Python 3 和 NumPy。

结论：计算仅验证指定线性玩具模型的数学性质，不构成四力统一、三大根波本源或人工引力新机制的证明。
