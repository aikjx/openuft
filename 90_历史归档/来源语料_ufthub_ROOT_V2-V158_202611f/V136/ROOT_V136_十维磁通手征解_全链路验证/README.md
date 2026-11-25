# ROOT V136｜可复算研究包

**目标**：给一个十维 Einstein–Maxwell–Λ 磁通紧化的明确、可复算的条件性数学解，并审计 Spinᶜ 指标、SU(3) 表示、规范反常及半径稳定性的范围。

## 操作（Windows / Linux，Python ≥ 3.10）

```shell
python src/verify_v136.py
```

无第三方依赖；结果保存到 `data/`。绘图使用 matplotlib（可选）：

```shell
python src/plot_v136.py
```

研究依据和所有定义在 `研究报告.md`。`核心公式.tex` 便于 LaTeX 引用。`docs/模型准入判伪表.csv` 是面向下一轮的真实关口。

**特别说明**：只采用 c=1，ℏ 和 G 始终有量纲。自带数值系数 H=1 是将长度以 `sqrt(H)` 表示，不是把 G 或 ℏ 设为 1。所有断言是特定模型的数理检查，不能代替实验验证。当前候选未完成四力统一、10D 反常、完整 4D 粒子谱或 KK 稳定性。

`history/` 只包含本工作区实际存在的历史研究包；历史内容不因归档自动通过本轮审计。`MANIFEST_SHA256.txt` 存放 ZIP 内所有其他文件的哈希，`verify_archive.py` 可检查内容完整性。
