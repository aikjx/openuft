# ROOT V95｜有限能量 Maxwell 场、螺旋闭环与能源—稳定性审计

承接 V94（205 项）并追加 V95（24 项），共 **229 项研究问题**。本包只证明条件模型内的新数学结果，**没有解决四力统一，也没有进行实物实验**。

## 首次实现与关键约束

- 用光滑紧支撑矢势为任意给定光滑嵌入闭合轨道构造有限磁能的理想 Maxwell 静场。
- 证明给定轨道上的洛伦兹力精确相容、`divB=0`、`divJ=0`；静态且完全无源时这种紧支撑非零 B 不可能存在。
- 特定截止函数下导出 `U_B=(π ε²/(4μ0))(γm v/q)² ∮κ²ds+O(ε⁴)`，并以独立网格和高精度参数审计核对。
- 基准三叶结：30 万分之一米宽度级别的磁管、约 0.109–0.256 T 轨道磁场和 3.8960×10⁻⁴ J 理想静磁能；闭合轨道虽然存在，对一类小扰动却明显不稳定。
- 经典带电加速辐射导致非零能耗；静磁场不做功，不能无条件自维持。

## 文件清单

- `research/ROOT_V95_有限磁能闭环_完整科研总论.md`：完整定理、推导、适用域、数量级、限制与参考资料。
- `research/定理与反例_独立审计.md`：10 条独立证明与反例。
- `src/finite_tube.py`：几何、紧支撑矢势/磁场、体能量、Lorentz 轨道积分。
- `src/asymptotic.py`：磁能领先系数独立计算。
- `src/symbolic_audit.py`：圆形轨道的独立符号 Maxwell 检查。
- `src/dimension_audit.py`：24 条 SI 量纲方程审计。
- `src/generate_results.py`：高精度、参数扫描、独立网格、图表与 JSON/CSV 数据。
- `tests/test_finite_tube.py`：真实 Python 自动化单元测试。
- `results/`：全部生成的 THEORY 数值和验收数据。
- `ledger/ALL_229_ISSUES.csv`：保留 V94 原始 205 项并添加 V95 24 项。
- `web/index.html`：离线交互可视化，仅展示指定理论模型。
- `archive/ROOT_V94_original.zip`：原始、未修改的 V94 科研包。

## 复现步骤

Python 3.10+；依赖 `numpy scipy sympy mpmath matplotlib pytest`。

```bash
python -m pip install -r requirements.txt
python verify_checksums.py     # 在任何数据重生成之前核验原始交付状态
python run_all.py             # 测试 + 符号 + 量纲 + 结果与台账复算
# 可选，已安装 Playwright + Chromium 的系统中：
python web/browser_smoke.py
```

Windows 可运行 `RUN_WINDOWS.bat`；Linux/macOS 运行 `sh RUN_LINUX_MAC.sh`。

运行 `run_all.py` 后生成图像或 JSON 的元数据可能变化，原始交付哈希不应在重新生成之后解释为被篡改。验证请先进行。

**科研诚实声明：** 数学定理不是新物理发现；模拟轨道不是已观测轨道；有限场能量不代表有限制造成本；`v=c` 不是有静质量粒子的物理速度；该研究尚未提出并实验确认四力共同本源。
