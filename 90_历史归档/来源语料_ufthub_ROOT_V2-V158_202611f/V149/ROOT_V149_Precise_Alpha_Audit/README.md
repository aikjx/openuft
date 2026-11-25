# ROOT V149 — 精细结构常数与协变螺旋精算

**研究工程，不是四力统一的证明。**

本轮是对 V148 的精细化审计：仅设置 `c=1`，严格保留 `ħ` 与 `G` 独立有量纲。

## 可复核结论

- 光速螺旋的三维曲率/挠率比值不是 Lorentz 标量。同一曲线在一组参考系有比值 0.0072973525643，但合法 boost 后为 1，因而不能直接等同普适精细结构常数。
- 任意目标数 `0<α*<1` 都能用于**反向选择**螺旋参数；这不是预测。
- 如果假设光速激发的瞬时能量动量沿螺旋切线运动，几何角频率与能量的 boost 因子相反，不能简单把 `E=ħω_helix` 当普适关系。
- 对真正圆偏振 Maxwell 波，矢量旋转、能流直线前进，符合真空方程；两个主要电磁场 Lorentz 标量为零，不能独立决定 α。
- 在 c=1 体系中，电子引力耦合 `Gm_e²/ħ≈1.7518094e-45`；用 SI 参考常数数值比较时须在换算式中恢复 `c_SI`。

详细解释：`theory/ROOT_V149_精细求导.md`；原公式源码：`theory/ROOT_V149_equations.tex`。

## 完整运行

Python 3.10+：

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_manifest.py
```

Windows：双击 `scripts/运行_Windows.bat`；Linux：运行 `bash scripts/run_linux.sh`。

## 文件

- `src/root_v149/`：光速螺旋、轴向 Lorentz boost、频率、Maxwell 波和单位/常数；
- `tests/`：自动化物理-数学一致性单元测试；
- `symbolic_audit.py`：独立符号恒等式核验；
- `results/`：CODATA 比较、55 位十进制审计、各参考系扫描、测试记录（非实测数据）；
- `figures/boost_frame_dependence.svg`：变换后几何比例变化的矢量图；
- `history/ROOT_V148_Lorentz_Helix_Covariance_Complete.zip`：上个完整研究包，作为历史快照；
- `MANIFEST.sha256`、`verify_manifest.py`：可验证的文件摘要。

## 完成状态

程序审计：66 项自动化测试、12 项独立 SymPy 校验均通过；详见 `TEST_REPORT.md`。


已完成：模型求导、Lorentz 反例、精细结构常数对照、Maxwell 例子、Python/SymPy 验证、代码/数据归档。

未完成：从单一螺旋动力学独立预测 α、ħ、G；完整强弱规范群及粒子谱；独立实验支持；四力统一最终证明。

所有“测试通过”仅指自动化数学/软件校验通过，绝不表示自然界实验验证通过。
