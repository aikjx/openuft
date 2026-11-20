# ROOT V98｜三维非线性内外周期轨道科研包

> 版本 2026-11-18。研究性质：数学推导、现有 Maxwell–Lorentz 物理模型下的数值计算和软件回归测试。**不宣称四种基本力已统一、光速内禀螺旋已证实或新物理实验已完成。**

## 最重要的新内容

从 V97 的“平面非圆形周期轨道”推进到**真正具有非零轴向位移的三维数值周期轨道候选**。

- 来源：轴对称、静态、有限截面连续电流的双线圈 Biot–Savart 磁场。
- 电子速度：`0.1c`；径向初始偏移：`60 μm`；轴向初始高度：约 `8.84 μm`。
- 21 阶源求积：参考圆半径 `5.152776021 mm`，完整周期 `5.39998604 ns`。
- 完整 6 维返回位置误差约 `1.65e-14 m`（仅指定离散场与数值积分条件）。
- 独立定时积分、Boris 时间步收敛、源阶数收敛、Maxwell 真空残差、正则角动量及速度守恒交叉审计均已执行。
- 仍开放：真实制造、辐射反作用、非线性长期稳定、严格存在性、结拓扑、`G` 来源、强弱相互作用和量子引力。

## 包内文件

| 路径 | 内容 |
|---|---|
| `research/ROOT_V98_三维非线性闭环科研总论.md` | 模型、作用量、推导、完整精算、误差与失败条件 |
| `research/严格定理与反例.md` | 已证明内容和未证明内容逐项区分 |
| `src/coil_model.py`, `src/v97_core.py` | V97 的有限截面线圈磁场和历史物理代码 |
| `src/v98_core.py` | 三维周期射击、独立积分、守恒量和辐射核算 |
| `src/generate_v98.py` | 全量数值重新生成、CSV、图像及离线实验室 |
| `src/symbolic_audit.py` | 20 项精确代数 / SI 量纲检查 |
| `tests/test_v98.py` | 35 项 Python 模型与回归测试 |
| `results/NUMERICAL_SUMMARY_THEORY.json` | 标准数值结果与明确局限性 |
| `results/3D_PERIODIC_TRAJECTORY_THEORY.csv` | 逐点三维轨道理论数据 |
| `results/SOURCE_CONVERGENCE_THEORY.csv` | 截面求积阶数误差 |
| `results/BORIS_CROSSCHECK_THEORY.csv` | 独立积分器收敛 |
| `plots/` | 三维轨道、双向振荡、收敛及实测浏览器截图 |
| `web/index.html` | 完全离线、无网络依赖的交互三维可视化（轴向尺寸标注已统一） |
| `web/browser_smoke.py` | 可选 Chromium/Playwright 验收脚本 |
| `ledger/ALL_297_ISSUES.csv` | V97 277 项加 V98 20 项，保留历史状态 |
| `archive/ROOT_V97_original.zip` | V97 原始完整科研 ZIP，供独立历史复测 |
| `CHECKSUMS.sha256` | 包内文件 SHA-256 固定快照 |

## Windows / Linux / macOS 快速运行

建议 Python 3.10+，联网环境下安装依赖：

```bash
python -m pip install -r requirements.txt
python verify_checksums.py
python run_all.py
```

从源码重新计算所有理论数据、图像与 HTML（计算量较大）：

```bash
python run_all.py --regenerate
```

并运行解压出的 V97 历史测试：

```bash
python run_all.py --historical
```

可选安装 Playwright 并确保 Chromium `/usr/bin/chromium` 在 Linux 上可用，再执行：

```bash
python web/browser_smoke.py
```

**重要**：执行 `--regenerate` 后生成文件的字节会变化；因此原始固定快照的 SHA-256 可能不再匹配，这是正常的。应在重新生成之前执行一次校验。

**科研裁定**：可复现数值周期候选不等于数学严证，不等于实验，不等于四力统一。严格证明、实验与新物理都需要另设验收标准。
