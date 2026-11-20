# ROOT V83 · 双传感器引力调制、零实验与 ROOT-GCL/1.1

**本包是可复现的物理计算和安全实验设计工具，不是引力控制硬件。**

## 立即运行

Python 3.10+，不需要安装第三方模块：

```bash
python run_all.py
```

它执行单元测试并生成固定随机种子的**人工合成** CSV 与 `results/numeric_summary.json`。亦可单独执行 `python -m unittest discover -s tests -v`。

```bash
PYTHONPATH=. python tools/validate_protocols.py
```

在浏览器中离线打开 `web/index.html`，控制 M、d、传感器间距和理想 B 参数。页面仅用 JavaScript 在本地计算，不连接硬件或网络。

## 文件与用途

- `src/gravitylab.py`：受控源质量、双传感器共模/梯度、理想磁储能、ABBA、模拟噪声与误差预算。
- `tests/test_physics.py`：物理极限、镜像奇偶性、有限差分、随机区组、模拟复现、场能和异常处理。
- `spec/*.json`：ROOT-GCL/1.1 实验方案与机器可读协议。
- `data/*SYNTHETIC.csv`：明示为模拟的传感器时间序列。
- `results/*`：测试、数值、图表和工程验证报告。
- `book/ROOT_V83_双传感器引力控制与实验语言研究总集.md`：逐章推导、误差和证伪逻辑。
- `SOURCES.md`：科学来源；`PROOF_STATUS.md`：成功与失败边界。

## 不得误解

1. 代码模拟 100kg 质量源的引力信号，不代表仪器已实际达到需要的灵敏度。
2. 该装置只能通过移动质量改变**局部引力场**，没有改变 G。
3. 电磁场储能可以贡献引力，但内部能量转移不等于系统总质量净增加。
4. 所有 CSV、PNG、JSON 中的仿真数值均非观测，不构成新力或四力统一证据。
5. 不提供与真实电源、磁体、马达或重物执行机构的接口，真实实验需要合格实验室安全批准。
