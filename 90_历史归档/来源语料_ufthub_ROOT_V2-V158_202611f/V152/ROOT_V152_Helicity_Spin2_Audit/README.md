# ROOT V152 — 光速螺旋 / 三方向正交 / 自旋1与自旋2 的严格场论审计

**状态：可运行数学与数值研究包；不是四力统一证明。**

本轮重新设计了 ROOT 的数学关口：与其把三方向分别命名为三种力，不如检验同一横向正交标架怎样构造出不同螺旋度（自旋1、2、3 等），以及这些表示怎样接受 Lorentz 协变、规范不变性、场方程和实验可测量的严格要求。

## 精简结论

1. `e_±=(e₁±i e₂)/√2` 在绕轴旋转时获得相位 `exp(∓iφ)`；`e_±⊗e_±` 获得 `exp(∓2iφ)`。这对应自旋1、自旋2 的**偏振几何**；它同样允许构造自旋3、4 等，因此**不能只凭正交几何选出四力**。
2. Maxwell 的真实两个自由传播模必须来自规范约束和正确的二次作用量；线性引力也必须遵从微分同胚规范对称性。它们都不是简单的螺旋运动学恒等式。
3. 数值与符号计算分别检验了 Maxwell 场强、线性 Riemann 张量、线性 Einstein 方程及其在洛伦兹 Boost 下的协变性。
4. 对 `f=100 Hz, h=10⁻²¹, L=4 km` 的示例，引力波单臂扰动为 `2×10⁻¹⁸ m`，双臂差分扰动为 `4×10⁻¹⁸ m`，仅是已知公式的演示计算。
5. 一个决定性反例：自由场的同一偏振几何，在 `g_A=0.1` 与 `g_A=0.3` 下仍然成立；因此**没有从光速螺旋推出 α、G、ħ**。

## 单位

严格只设 `c=1`；**保留有量纲的** `ħ` 和 `G`。量纲详见 `theory/ROOT_V152_精细全维研究报告.md`。

## 运行环境

Python 3.10+；仅使用 NumPy、SymPy 与 Matplotlib，支持 Windows 和 Linux。

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_manifest.py
```

Windows 双击 `scripts/run_windows.bat`，Linux 执行 `bash scripts/run_linux.sh`。

## 文件清单

- `src/root_v152/core.py`：三维正交标架、螺旋度变换、横向无迹投影、Maxwell / 线性引力场计算、洛伦兹 Boost 与量纲检查。
- `tests/`：82 项数值数学测试与反例（偏振、规范变换、张量曲率、协变、量纲）。
- `symbolic_audit.py`：24 项 SymPy 符号恒等式核验。
- `stress_audit.py`：固定随机种子的 256 组参考系、方向和规范不变性检验。
- `generate_results.py`：401 角度扫描、JSON、原理示意图。
- `results/`：401 角度扫描、数值测试日志和演示性、可重复的计算结果，不包含任何声称来自探测器的实测数据。
- `theory/`：完整中文推导及 LaTeX 文稿。
- `REFERENCES.md`：可检查的外部参考文献和链接。
- `STATUS_MATRIX.csv`：已完成与未完成的科学问题。
- `history/ROOT_V151_Helicity_Berry_Theory_Audit_Complete.zip`：上一完整版本归档。
- `manifest.json` + `verify_manifest.py`：交付源码/静态文件完整性检查；运行生成的文件未纳入静态哈希范围。

**科学状态**：这次只证明在明确假设下的数学一致性，仍没有从单一微观螺旋出发独立推导自旋1、2 的动力学，更没有统一强、弱相互作用、生成粒子谱或预测物理常数。不能将“测试通过”表述成“理论已被实验证实”。
