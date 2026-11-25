# ROOT V145 — 闭环拓扑、粒子手征性与量子异常研究包

**研究性质：已知数学机制的严格复算 + ROOT 候选假设的否证/约束审计。不是四力统一已完成的声明。**

## 一键运行

- Windows：双击 `scripts/运行_Windows.bat`（需安装 Python 3.10+）
- Linux：`bash scripts/run_linux.sh`
- 通用命令：`python run_all.py`
- 无需联网；核心程序仅依赖 Python 标准库。

## V145 最重要的结果

1. 在 `M4 × S²` 的单位电荷单极子背景中，磁通数 `n ∈ Z`，第一 Chern 数 `n`。
2. 扭曲 Dirac 指标 `index = q n`。取 `n=3,q=1` 有三个同一内部手征性的零模，但 **n=3 是人为选择，不是对自然界三代的独立预测**。
3. 完整 6D Dirac 与单个 6D Weyl 不同；前者一般给出 4D 左右配对而非净手征粒子。
4. 单一超荷磁通时，不同标准模型表示的零模指标不一致：`(+3,-12,+6,-9,+18)`。因此不能不加额外机制就推出三代完整粒子谱。
5. 一个电荷为 +1 的三重左手模态若直接作为 4D U(1) 规范理论的唯一费米子谱，具有非零三角异常。工程用 exact Fraction 验证已有标准模型一代的异常抵消。
6. 模型的第一非零质量尺度 `m = ℏ sqrt(|qn|+1)/R`；示意 R=10^-18m、n=3,q=1 => E≈394.65396 GeV。不是实测结果或独立质量预测。

## 目录

- `theory/V145_完整数学推导.md`：中文推导、严格限制、量纲和未来检验。
- `theory/ROOT_V145.tex`：LaTeX 可复用公式。
- `src/root_v145`：数学计算源代码（flux、扭曲 Dirac 谱、异常、单位转换）。
- `tests`：47 项自动化测试。
- `results/flux_scan.csv`：磁通、指标、谱间隙扫描。
- `results/spectrum_scan.csv`：非零 Dirac 谱及简并度。
- `results/zero_mode_norms.csv`：正手征零模范数交叉校验。
- `results/anomaly_checks.json`：异常校验与单超荷磁通反例。
- `results/results.json`：全量模型元数据。
- `figures`：SVG 数学可视化。
- `history/ROOT_V144_Geometric_Gauge_Audit_Complete.zip`：上一版完整归档，独立于 V145 程序运行。
- `MANIFEST.sha256`：除自身外的每个文件 SHA-256 摘要。

## 精度和边界

- 磁通数值积分使用 4096 段复合 Simpson。
- 47 项为数学与软件一致性测试，并非 47 个物理实验。
- 没有调用真实加速器或天体实验数据进行参数拟合。
- 没有解 6D Einstein–Maxwell 背景的动力学方程，也没有稳定化 R；这是必要前置问题。
- 尚未推导出四种基本相互作用共同微观起源、G、耦合常数或三代粒子的唯一性。

## 单位

严格采用 `c = 1`。`ℏ` 和 `G` 不设为 1。用于输出 GeV 的代码显式恢复 `c_SI`，这只是单位换算。
