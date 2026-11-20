# ROOT V85｜G 与星球组成、四力统一、双不变量联合检验

**核心结论**：研究给出两个明确前提下的数学模型筛选量——径向形状 Q=-r g'/(2g) 与跨源/跨材料差分矩阵 D 的 rank≤1；未独立预测 G、未发现新力，未证明四力统一。软件数字是合成数据，不是实测。

## 一键复算

- Python >=3.10，并安装 `pip install -r requirements.txt`（numpy、matplotlib、sympy）。
- `python run_all.py`：重算数据、SymPy 审核、测试和基本文件检查。
- Windows：双击 `RUN_WINDOWS.bat`；Linux/macOS：运行 `bash run_linux_macos.sh`。
- 离线实验界面：浏览器直接打开 `web/index.html`，不需要联网。
- 研究总论：`book/ROOT_V85_G来源_星球组成依赖_四力统一_双不变量攻坚总论.md`。

## 文件与数据

- `src/physics.py`：严格模型的公式与参数域校验。
- `src/simulation.py`：单/双媒介跨源矩阵和固定种子的**合成**噪声模拟。
- `data/equation_catalog.csv`：证明状态与严格限制。
- `data/method_matrix.csv`：研究路线及证伪边界。
- `data/celestial_GM_benchmarks.csv`：基于 JPL GM 的体表 g、紧致度与外部 Schwarzschild 曲率示意。
- `data/*SYNTHETIC*`：假设新力数据，不允许作为实测发表。
- `spec/experiment_protocol_v85.json`：未执行的实验计划协议，不控制硬件。
- `results/`：纯计算图、数值与代码复测结果。
- `history/`：之前若干版本的归档，仅作为历史工作关联，不作为外部证据。

## 研究局限

木星 GM 使用 JPL Jupiter *system*，与木星本体半径仅作近似对比。白矮星和中子星是人为示意。理想 Yukawa 电荷并非从具体粒子理论独立计算。Q 必须处理已知非球形、转动及 GR 修正；D rank-one 需要多个源和多个材料的可比真实测量及严密系统误差控制。MICROSCOPE 只限制特定源—材料组合的相关耦合乘积，不是普适“G 不变”定理。
