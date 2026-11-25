# ROOT V153｜光速螺旋与协变规范动力学：严格可证伪性审计

**状态：已完成数学与数值的有限模型审计；没有解决四力统一。** 这份独立研究工程延续 V152，重点排除“旋转相位本身就能产生电磁力与引力波”的错误推理。

## 一键运行

Python 3.10+：

```bash
python -m pip install -r requirements.txt
python run_all.py
python generate_results.py
python verify_manifest.py
```

Windows：`scripts/run_windows.bat`；Linux：`bash scripts/run_linux.sh`。默认测试与符号计算使用 NumPy、SymPy。图表额外使用可选 Matplotlib。

## 本版可重复结论

1. 对任意光滑标量 `theta`，若 **特别选择** `A_mu = partial_mu theta`，则 Maxwell 场强严格为零。
2. 若 **特别选择** `h_munu=partial_mu partial_nu theta`，则线性黎曼曲率严格为零；该扰动等于线性坐标规范变换。
3. 取横向向量 `A_x=cos(t-z), A_y=sin(t-z)`，计算出非零的电磁场强，且满足真空麦克斯韦方程。
4. 取横向无迹张量 `h_xx=cos(t-z), h_yy=-cos(t-z)`，得到 `R^(1)_0x0x=cos(t-z)/2`（单位频率和单位应变示例），且线性化 Einstein 方程为零。
5. 同一正交基可构造螺旋度 ±1 和 ±2，但这种**表示论事实不能决定动力学系数**。正的任意规范耦合仍给出相同真空自由波方程。
6. 正确的规范耦合还要求电荷流守恒、应力张量守恒；这是规范变换与积分分部得到的必要条件。

## 当前最新验证

- `38/38` 项 `unittest` 测试通过。
- `256` 个标量构造线性化黎曼分量经 SymPy 直接求导全部为零；另有 `16` 个 Maxwell 场强矩阵分量为零。
- `256` 组固定随机种子的洛伦兹 Boost、矢量场强、秩四曲率交叉检验完成。
- Maxwell 和 Fierz–Pauli 的规范不变性、Bianchi 恒等式、独立物理偏振检验通过。
- **这些数字代表程序和数学公式的一致性，不代表 256 次物理实验。**

## 从三维光速螺旋通向可检验统一理论的缺口

`光速螺旋轨迹 → 有协变性约束的微观变量 → 非平凡场强 → 正确二次作用量 → 正确约束和源耦合 → 规范群/粒子谱/耦合常数 → 真实实验预测`

现在只完成其中一部分必要条件审计。尚未从螺旋曲率、挠率独立导出规范场、标准模型规范群、粒子谱、G、hbar 或 α。

## 重要限制

本版反例只针对**单个光滑标量相位的特定局部构造** `A=dtheta`、`h=Hessian(theta)`；它不声称所有标量介质或所有复合场理论都不能产生有效矢量场，也不否认标量场的应力—能量张量能够产生引力。全程只设 `c=1`，不设 `hbar=1` 或 `G=1`。

## 包内容

- `src/physics.py`：独立 Fourier 场强、线性化曲率、洛伦兹变换和偏振算法
- `symbolic_audit.py`：符号求导检查
- `stress_audit.py`：256 组参考系数值校验
- `tests/test_physics.py`：物理一致性单元测试
- `theory/V153_derivation.md`：完整公式、推导及必要假设
- `theory/V153_derivation.tex`：LaTeX 公式复核文件
- `results/`：JSON/CSV 数据
- `figures/`：曲线图
- `history/ROOT_V152_Helicity_Spin2_Complete.zip`：上一完整历史包
- `manifest.json` + `verify_manifest.py`：静态源文件 SHA-256 校验

## 科学参考

见 `REFERENCES.md`，优先为 Cambridge David Tong 线性化引力讲义及原始同行评审的 Fierz–Pauli 文献。
