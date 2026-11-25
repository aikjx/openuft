# ROOT V141｜螺旋内部相位—规范动力学修复研究

**状态：研究模型与自动化验证已完成；四力统一的证明尚未完成。**

## 核心发现

1. V140 的两对内部变量组成的曲率 `Ω=Σdq∧dp` 是局部恰当形式。如果只通过 `H=dA+ηΩ` 进入动力学，`H=d(A+ηΣqdp)`，可完全吸收，不能因此宣称新力。
2. 单纯内部变量在常量背景附近缺少普通的二次传播项；独立的 U(1) 场 `A` 可恢复无质量 Maxwell 模式。
3. 采用 **已知的类轴子电动力学** 耦合，让内部相位 θ 具有独立的动力学，变分后得到双向耦合场方程。这个模型**没有**从螺旋几何独立推出 U(1)。
4. 使用一维空间螺旋 Beltrami 模式，解析证明守恒量，进行数值精算和步长收敛测试。
5. 只采用 `c=1`；`ℏ`、`G` **保留**，具体量纲见 `docs/DERIVATION_zh.md`。

## 使用

Python 3.10+，需要 `sympy>=1.12`，其他运行库使用 Python 标准库。可选图形 `matplotlib>=3.7`。

```bash
python -m pip install 'sympy>=1.12'
python run_all.py
```

- Windows：双击 `run_windows.bat`。
- Linux：`./run_linux.sh`。
- 生成 CSV：`results/coupled_helical_mode.csv`。
- 生成数值诊断：`results/summary.json`。
- 完整中文推导：`docs/DERIVATION_zh.md`。
- LaTeX 形式：`docs/ROOT_V141.tex`。
- 对比旧工程：`legacy/ROOT_V140_Composition_Dynamics_Complete.zip`。

## 必须区别

- **已证明**：在列出的假设下的场重定义、规范不变性、Euler–Lagrange 方程、Noether 型守恒式。
- **已测试**：符号与有限初值模型的程序数值结果。
- **未完成**：从空间光速螺旋运动导出引力、强弱规范群、自由参数数值与实际新物理；没有真实实验数据约束。

## 审计与复现

运行 `python run_all.py` 重新计算并生成日志。日志显示实际通过的测试数。
数值误差是截断与浮点误差，不代表实验置信区间。
参考文献与物理边界条件在 `docs/DERIVATION_zh.md`。
