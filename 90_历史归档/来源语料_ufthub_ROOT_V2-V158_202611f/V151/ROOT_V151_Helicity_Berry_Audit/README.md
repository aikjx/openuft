# ROOT V151 — 三力垂直、光子螺旋度、Berry 曲率和场论的独立精算审计

**本工程不是四力统一证明。** 它严格检验一个与 ROOT 原始设想有关的结构：三维正交标架能在动量空间生成光子的 Berry 曲率，其两个偏振分支具有相反的、量子化的 Chern 数 ±2；但不能直接把这类几何曲率当作时空电磁力或拿来推导精细结构常数。

## 单位规则

只采用 **`c=1`**；保留 `ħ`、`G` 的独立量纲，不采用 `ħ=1`、`G=1`。计算中的波频率按参考长度归一化；实验的 α 只作为对照值，不参与拟合。

## 一键复算（Python 3.10+）

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_manifest.py
```

- Windows：双击 `scripts/run_windows.bat`。
- Linux：`bash scripts/run_linux.sh`。
- 所有核心计算可离线复算。绘图依赖 matplotlib，符号审计依赖 SymPy。

## 文件

- `theory/ROOT_V151_完整数学审计.md`：核心推导、可证伪条件、已有/假设的边界。
- `theory/ROOT_V151_equations.tex`：英文 LaTeX 公式与审计概要。
- `src/root_v151/core.py`：纯 Python + NumPy 计算核心。
- `tests/`：自动化测试（偏振几何、Berry 积分、光子传播、标量反例）。
- `symbolic_audit.py`：SymPy 符号推导核验。
- `generate_results.py`：重新生成数值 JSON、CSV 与示意图。
- `figures/`：场矢量旋转与直线传播、Berry 连接、Chern 通量。
- `results/`：精算 JSON、参考系扫描及符号验证结果。
- `history/ROOT_V150_Precision_Alpha_Covariant_Complete.zip`：V150 研究原包，保留历史连续性。
- `TEST_REPORT.md`：本轮测试边界及再现情况。

## 五个结论

1. 三方向正交是严谨的几何关系，但不能直接指定三种力。
2. 光子动量方向的 Berry 曲率有 `C=±2`；这是已知光子偏振拓扑性质，并非新发现。
3. `A=dψ` 的纯相位旋转局部 `F=0`，不具独立 Maxwell 传播自由度。
4. 真空圆偏振电磁波满足 Maxwell 方程；旋转的是电磁场矢量，其自由能流沿传播轴前进。
5. `α≈1/137` 不是由整数拓扑不变量或三维螺旋的曲率/挠率推导得到；统一引力和强弱规范群仍未完成。

## 研究状态

**已完成：** 指定模型数学推导、符号和程序测试、确定性参数扫描与 ZIP 完整性检查。

**未完成：** 独立推导 `G、ħ、α`、标准模型规范群与粒子谱、量子一致性和真实实验新预测，因此不得宣称“100% 攻破四力统一”。
