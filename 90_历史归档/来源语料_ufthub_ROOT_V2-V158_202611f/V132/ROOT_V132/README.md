# ROOT V132 研究包

## 运行

需要 Python 3.10 或以上，**不需要安装任何第三方依赖**：

```bash
python verify_v132.py
```

执行后控制台打印 `ROOT V132 PASS`，并更新 `results.json` 和 `anomaly_scenarios.csv`。

## 文件

- `研究报告.md`：全部推导、概念区分、证据状态、参考资料。
- `verify_v132.py`：精确有理数反常抵消和规范变换反例验证。
- `results.json`：精确多项式系数与测试结论。
- `anomaly_scenarios.csv`：选定超荷下有/无右手中微子的反常结果。
- `判伪清单.csv`：下一轮理论与实验准入要求。
- `SHA256SUMS.txt`：压缩前各文件哈希。

## 科学边界

这是数学一致性审查，**不是四力统一已获证明，也不是实验发现**。全程只取 `c=1`，`ℏ,G` 保留独立量纲。
