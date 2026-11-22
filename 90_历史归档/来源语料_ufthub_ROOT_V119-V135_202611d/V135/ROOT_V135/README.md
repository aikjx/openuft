# ROOT V135｜拓扑零模、三代粒子与量子反常攻坚

这是承接 V134 的独立数学研究、数值验证与可复现 ZIP。**仅 c=1；没有将 ℏ、G 或 ε₀ 设置为 1。**

## 内容

- `reports/ROOT_V135_统一场论拓扑手征与量子反常_科研总报告.md`：含证明、明确假设、反例、工程结果、参考文献的主报告。
- `reports/最核心方程_证明与反例.md`：核心公式与未解决问题。
- `src/topology.py`：二维 U(1) 通量与 overlap/Wilson–Dirac 指数、零模计算。
- `src/run_experiment.py`：输出量子通量、晶格指标、随机变形、超荷异常数据。
- `src/make_figures.py`：生成三张分析图。
- `tests/test_topology.py`：25 项自动化测试。
- `results/`：CSV、JSON、V134 回归日志、本轮测试日志。
- `figures/`：三张 PNG 数学模型图。
- `previous/`：V134 原始研究 ZIP，延续历史研究材料。
- `manifest.sha256`：除自身外的内容文件 SHA-256 清单。

## 最少复现命令

进入 `ROOT_V135` 目录后：

```bash
python -m pip install numpy matplotlib
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 python src/run_experiment.py
python src/make_figures.py
```

Windows PowerShell：

```powershell
$env:OPENBLAS_NUM_THREADS = "1"
py -m unittest discover -s tests -v
py src/run_experiment.py
py src/make_figures.py
```

运行 `bash run_verification.sh` 或 `./run_verification.ps1` 可核验本轮测试和 SHA-256。

## 严格结论

1. 已有的 Atiyah–Singer 指数定理可将二维内部通量与净手征零模联系起来；数值 Wilson–Dirac/overlap 模型复现了该关系。
2. 全局光滑纯相位无法产生非零 Chern 数。
3. **同一 6D 手征性、单一共通量**的最简模型对带电场产生不可自动抵消的 U(1) 反常，不能当作已完成的物理模型。
4. 2026 年迄今没有通过本包证明 ROOT 螺旋公设能解释 α、ℏ、G、三代质量或完成四种相互作用统一。所有输出都是模型验证，不是实验发现。

## 运行记录口径

新增 25 项测试通过；V134 历史 45 项在本轮实际重新执行通过，共 **70 项分段测试**。额外 600 组合成扰动**并非全部满足一致性条件**：对于强噪声故意保留了拓扑失配记录，以展示数值适用范围。该扰动试验没有计作 600 项全部通过的单元测试。
