# ROOT V84｜多距离引力调制、有限尺寸第五力与可辨识性科研包

**本工程是严谨的科研仿真和理论审计，不是实际的引力控制仪器。未测量新的引力，也未证明四力统一。**

## 运行

需要 Python 3.10+，核心程序仅依赖标准库。

```bash
python run_all.py
```

该命令重建全部三个**合成**测量数据集、理论曲线、统计拟合与 58 项单元测试。自动测试不会向硬件发送指令。

独立执行：

```bash
python -m unittest discover -s tests -v
python tools/build_catalog.py
```

图表可用已安装 matplotlib 的环境执行 `python tools/plots.py` 生成。离线仪表台用浏览器打开 `web/index.html`，无外网依赖。

## 三个具有不同科学含义的合成情景

- `NULL`：只有牛顿引力+执行器伪差和随机噪声，没有第五力；检验假阳性。
- `INJECTED`：人为设定 `alpha=0.08` 和 `lambda=0.25m`，检验程序能否在合成数据中恢复注入参数。
- `CONFOUNDED`：没有任何新力，只是有源臂比假动作臂多一个与 Yukawa 模型完全同形的伪差；此时拟合仍会显著，故**软件显著性不能等于新物理发现**。

三个情景的 CSV `provenance` 均为 `SYNTHETIC_NOT_REAL_DATA`。其显著性仅针对设定噪声的算法演示。

## 核心研究问题

1. **物理奇偶性**：位置反转时共模奇、梯度偶。
2. **漂移**：ABBA/BAAB 精确抵消块内线性漂移，不保证消除二次漂移。
3. **有限尺寸**：Newton 外场不依赖均匀球半径；假设性有限程 Yukawa 修正取决于 `a/lambda`。
4. **物理可辨识**：`lambda→∞` 时新力和 Newton 项的距率相同，`alpha` 与 `G` 整体幅度不可分。
5. **系统误差**：同形执行伪差可完全假冒第五力，须独立实验排除。

## 文件

- `src/physics.py`：SI 量纲、均匀球、Newton、有限球 Yukawa、误差微分和 EM 能量。
- `src/analysis.py`：ABBA 奇信号、假动作扣除、加权最小二乘与参数不可辨识检查。
- `src/simulate.py`：种子固定的全部合成观测和 `results/numerical_summary.json`。
- `tests/test_v84.py`：独立单元/极限/反例验证。
- `book/*`：完整中文专著，含推导、反例及硬件实验必要前提。
- `data/*SYNTHETIC*`：不是真实实验观测数据。
- `data/equation_catalog.csv`：50 条有状态、有适用条件的方程。
- `data/method_matrix.csv`：30 条实验审查路线。
- `spec/*.json`：ROOT-GCL/1.2 机器可读实验要求，不含运动机构控制指令。
- `web/index.html`：离线交互与实验可辨识性说明。
- `results/*`：统计复算、数值曲线、浏览器测试和最终校验。

## 现场试验安全边界

100 kg 源质量只用于理论建模。实际移动这类重物存在挤压、坠落、结构振动与其他风险；本工程**不提供运动控制软件或安装方法**。任何现实操作都应由合格实验室负责机械防护、载荷及地面振动、传感器保护和电磁合规。
