# ROOT V130 · 可复现统一场论科研包

本包延续 ROOT V129 的量子反常和质量–电荷研究。**研究结论不是“完成大统一”，而是获得了可审计的规范统一必要条件以及对无阈值简单模型的精确反例。**

## 文件结构

- `reports/ROOT_V130_科研总报告.md`：完整数学证明、数值结果、检验边界与科研裁定。
- `theory/root_v130.py`：标准库精确有理数 SU(5) 算法及一圈耦合 RG。
- `theory/generate_results.py`：生成 JSON、CSV、两张图。
- `tests/test_v130.py`：正式 unittest 反例与回归测试。
- `data/v130_results.json`：可机读的数值结果。
- `data/running.csv`：标准模型与 MSSM 理论演化曲线（示例）。
- `figures/`：演化图。
- `evidence/test_results.log`：实际执行的 unittest 日志。
- `evidence/sources.md`：可追溯文献与输入来源。
- `history/`：V129 历史 ZIP 原始拷贝，供核查；未重复执行其历史测试。
- `SHA256SUMS.txt`：归档文件 SHA-256 清单。

## Linux、macOS、Windows 的一键复现

```bash
python -m unittest discover -s tests -v
python theory/generate_results.py
python verify.py
```

前两条命令依次运行核心测试、生成数据与图；需要绘图时安装 `matplotlib`，没有它时仍能生成数值文件。`verify.py` 检查 SHA-256 清单并执行核心测试。

## 实验边界

- 所有数值是输入条件下的一圈微扰数学计算，**不含超对称质量阈值、不含二圈修正、不含实验协方差拟合**。
- 高能 GUT 一圈交叉的精确数值对输入和规范约定敏感，不能单独用来宣称某新物理理论成立。
- 不推导 G、hbar、质量矩阵、三代世代数或引力量子化。
- 包内历史压缩包是供复核的归档资料，不作为 V130 新增测试计数。

研究日期 2026-11-21。
