# ROOT V147 可复算研究包
- 研究报告.md：条件性解析推导、实验来源、失败条件。
- verify.py：Python 3.8+ 标准库精确分数、Decimal 与数值诊断。
- results.json：实际执行结果；radion_screening.csv：模拟值。
- history/：V146 历史 ZIP 原样归档。
运行 python verify.py（Windows: run.bat；Linux: bash run.sh）。脚本会重新写入 results.json 和 radion_screening.csv。SHA256SUMS.txt 校验归档初始内容。不是四力统一证明，不含原始 Cassini 测距数据。
