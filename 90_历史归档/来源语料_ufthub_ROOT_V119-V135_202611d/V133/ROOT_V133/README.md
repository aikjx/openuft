# ROOT V133｜全维统一场论攻坚：量子内禀相位与规范联络

科研结论：**获得规范／Lorentz 协变的内部转子候选作用量，并证明电荷量子化、洛伦兹力和几何相位的条件关系；未完成四力大统一。**

## 文件导航

- `book/ROOT_V133_统一场论研究专著_第二卷.md`：完整研究专著（本轮新增）；
- `research/核心方程与审计边界.md`：一页核心方程和条件；
- `research/可证伪模型对照.md`：反例与开放问题；
- `research/参考文献与数据源.md`：可追踪的实验与理论来源；
- `src/root_v133.py`：主要模型与数值轨道积分；
- `src/make_figures.py`：四张合成计算图与数据 CSV；
- `src/property_audit.py`：固定随机种子 10,000 次随机数值性质检查（不是 10,000 项独立物理实验）；
- `tests/test_root_v133.py`：可重复单元测试；
- `results/`：运行日志、计算结果、合成数据；
- `plots/`：图表（全部注明是模拟而非观察）；
- `previous/ROOT_V132_原始归档.zip`：上一轮 ZIP 原件；
- `manifest.sha256`：文件哈希清单。

## 一键复现

在 ZIP 解压目录的 `ROOT_V133` 下执行：

```bash
python -m pip install numpy scipy sympy matplotlib
python src/root_v133.py
python src/make_figures.py
python src/property_audit.py
python -m unittest discover -s tests -v
sha256sum -c manifest.sha256
```

仅采用 **c=1**，不设 ℏ=1、G=1。图表中的质量、时间、磁场选择仅供数值检验，不视为粒子实验测量。NIST CODATA 的 ℏ 和 ε₀ SI 数值只用作合成数值计算的参考（不可将原 SI 数值不经单位换算用于实际 c=1 物理预测）；`m0`、`I` 数值通过任意选定的 `t0=1 s` 构造，没有作为真实粒子参数。

## 科研透明度

- 条件性解析推导和数值测试通过 ≠ 四力已统一；
- 由 `α` 反求 `λ` 是校准，不是从几何预测 `α`；
- 复合 SO(2) 联络是一个需要独立物理定义内部二维平面的候选结构；
- 本轮未做真实量子散射、轨道观测或实验联合拟合。
