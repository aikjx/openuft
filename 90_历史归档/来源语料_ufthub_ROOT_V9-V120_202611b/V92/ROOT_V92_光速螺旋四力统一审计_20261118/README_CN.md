# ROOT V92｜空间光速螺旋与四力统一全维审计（2026-11-18）

本科研包承接 V91 已存在的 115 项问题，新增 32 项专门针对总速 c、曲率 κ、挠率 τ、频率 ω 与四种基本相互作用的严谨检验问题，共 147 项**研究任务台账**（不是 147 条已经完成的证明）。

> **科学裁定：完整四力统一尚未攻破。** 这轮正式完成了常速螺旋严格几何关系、三个决定性反例、相对论磁场轨道交叉计算、量纲碰撞和全部旧问题的状态映射。没有发现新的第五力、没有证明有质量粒子以实际三速度 c 运动、没有从 c 和螺旋几何独立求出 G。

## 重要数学结果

`r(t)=(R cosωt,R sinωt,p t)`，`v=sqrt((Rω)²+p²)`：

- `κ=Rω²/v²`，`τ=pω/v²`，`|ω|=v sqrt(κ²+τ²)`。
- 若**附加** `v=c`，则 `|ω|=c sqrt(κ²+τ²)`；并非由等式自发推出 `v=c`。
- 在 SR 中对轴向 boost `u=p`，原空间螺旋的挠率变成零；三维 τ 不是 Lorentz 标量。
- 沿直线电场加速的粒子有 `F=qE≠0`，但曲率为零，反驳仅由 `(κ,τ,ω)` 唯一确定所有力的简单路线。
- `G` 的质量维度为 `M^-1`，而 `c, κ, τ, ω` 全部不含质量维度。不能只用它们构造 G。加入 ħ 和独立曲率只能得到带未知尺度与耦合的量纲式，非原理预测。

## 已运行验证

- 16 项独立 SymPy 代数断言；
- 16 个 Python 单测**测试组**，内部覆盖 500 个随机螺旋、数百组磁场与速度情形；
- 15 组磁场电子运动扫描（B=0.3/0.5/0.7 T, v/c=0.2/0.5/0.8/0.95/0.99）；
- 单个独立 RK4 完整轨道验证（12,000 步）；
- 33 个增强量纲向量，528 对交叉维度碰撞，22 个候选方程，其中 6 个维度不匹配；
- V91 的 115 项原始台账逐项映射、新增 32 项螺旋问题；
- 所有数值为 THEORY / MODEL / COUNTEREXAMPLE，非实物观测。

## 包内目录

| 文件 | 用途 |
|---|---|
| `research/ROOT_V92_全维科研总论.md` | 主要理论体系、严格区分/未解决点、外部出处 |
| `research/严格推导与反例_证明本.md` | 10 个定理、反例、条件判据 |
| `research/四力路线矩阵_下一步攻坚.md` | 多理论路径、失败条件、最短研究顺序 |
| `ledger/V91_115逐项螺旋关联审计.csv` | 旧 115 项原状态 + V92 专项判据 |
| `ledger/V92_新增32项专门任务.csv` | 32 项新任务和解决情况 |
| `ledger/FULL_TRACKER_147.json` | 全 147 项机器可读原始数据和新判断 |
| `results/DIMENSION_VECTOR_CATALOG.csv` | 33 个 SI 维度向量 |
| `results/DIMENSION_CROSS_ALL_PAIRS.csv` | 528 条两两维度检查 |
| `results/CANDIDATE_EQUATION_DIMENSION_AUDIT.csv` | 22 条候选等式的可能性判定 |
| `results/magnetic_helix_CODATA2022_THEORY.csv` | 15 点电子螺旋数值 |
| `results/electric_straight_COUNTEREXAMPLE.csv` | 直线电场反例 |
| `results/NUMERICAL_SUMMARY_THEORY.json` | 可复算数值基准和独立 ODE 积分误差 |
| `figures/*.png` | 三张理论图，非实验数据 |
| `web/index.html` | 无网络依赖的离线交互模型 |
| `src/*.py`, `tests/*.py` | 完整计算源代码及自动测试 |
| `archive/ROOT_V91_原始归档.zip` | 未修改的 V91 原始归档 |
| `CHECKSUMS.sha256`, `MANIFEST.json` | 文件哈希和包验证 |

## 解压与复算

Python 3.10+；运行前将终端定位在解压后的 ROOT_V92 目录。

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_checksums.py
```

Windows 可双击 `RUN_WINDOWS.bat`，Linux/macOS 可运行 `sh RUN_LINUX_MAC.sh`。**注意首次安装依赖可能需要联网**，但数据和离线可视化页面无需在线连接。操作中的任何通过状态都只属于软件/理论级验收，不属于统一场论物理证明。
