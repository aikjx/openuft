# ROOT V114｜科研审计与独立复验报告

**日期：2026-11-20**  
**状态：实际源码计算、数学单元测试、历史回归、浏览器控件验收完成。**

| 验收项 | 已执行结果 | 证据 |
|---|---|---|
| V114 数值+数学测试 | 90 项通过 | `python -m pytest tests/test_v114.py -q` |
| 其中精确符号检查 | 8 项通过（属于前述 90 项） | `test_sympy_*` |
| V113 历史回归 | 109 项通过 | 从 V113 原始 ZIP 解压后 `python -m pytest tests/test_v113.py -q` |
| Chromium E2E | 11 项通过 | `python tests/browser_smoke.py --capture` |
| V113 问题台账 | 396 行、396 个唯一 canonical ID、逐字节一致 | `ledger/V114_ALL_396_PRESERVED.csv` |
| 合成参数逆求 | 独立两种反演路径都恢复 a=1/3,λ=1 AU | `results/V114_RESULTS.json` |
| 离线计算 | 已生成 250 行扫描、5 幅理论曲线和 1 张实际浏览器截图 | `results/`、`figures/` |
| 独立清单核验 | `verify_release.py` 对 SHA、历史包和台账核验 | `MANIFEST.json`、`CHECKSUMS.sha256` |

## 测试过程中发现并修复的问题

1. 浏览器异步控件测试对 `all()` 传入了异步生成器，触发运行时错误；改为异步列表推导。
2. Playwright 的 range 控件拒绝 `.5` 这种填入格式；改为 `0.5`。
3. HTML 滑块的 `step=0.001` 使初始 `0.333333` 被 Chromium 舍入，导致精算测试产生误差；改为 `step=0.000001` 后 11/11 通过。
4. V113 以单半径模拟 γ 解释 Cassini 测量容易产生错误外推，V114 明确区分局部度规比、动力学势导数和完整光路拟合。

## 数值精算摘要

- 基准：`a=1/3, lambda=1 AU, r=1 AU`。
- γ_loc=0.781536454854；G_force/G*=1.24525296078；本地归一 toy γ_fit=0.606099373372。
- 0.5 AU 和 2 AU 测力超额比 Y2/Y1=0.446260320297；无损反演 a=1/3、lambda=1 AU。
- 1 AU 标量 Compton 质量能量 m_phi c²=1.319049391646e-18 eV，自由传播阈值 f*=3.189447240733e-4 Hz。
- 单点双观测雅可比行列式在 r=1 AU 为 0.07158948083668465；它不是任何实验的统计显著性。
- 1000 组合成高斯噪声、σgamma=σforce=0.001，λ/AU 的 5%、50%、95% 分位数约 0.979256、0.999959、1.022155；**不是实测置信区间**。

## 科学边界

- **没有证明四力统一、从第一性原理导出 G、自然生成粒子谱、UV 量子完备或独有实验新信号。**
- 模型只适用于线性静态、共形标量普遍耦合、无筛选点质量源等明确条件。
- 本次没有获取或重新拟合 Cassini、MICROSCOPE、LVK 的原始事件/测量数据；没有报告任何新实验参数排除限。
- 浏览器截图仅是前端交互功能证据，重新截图后像素/哈希不保证完全一致；源码和 JSON 对照作为确定性科研数据验收依据。
- 历史任务 396 项保留原始状态，不将此轮数学子任务错误地标成完成原始科学难题。

## 独立复验命令

```bash
python verify_release.py --quick
python verify_release.py --browser
```

执行 `verify_release.py` 应在解压出的项目根目录运行；需要 `pytest`、`scipy`、`sympy`、`numpy`、`matplotlib`，浏览器额外需要 Playwright 和 Chromium。
