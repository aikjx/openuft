# ROOT V94｜从协变作用量到内外螺旋闭环：数学、逆动力学和稳定性科研包

**研究日期 2026-11-18。研究类型：严格数学证明、已知 Maxwell–Lorentz 动力学的逆向设计、数字积分及边界条件审查。没有真实实物实验，未证明四力统一。**

## 这次真正完成的进展

1. **严格否定两条过度推论：** 自由粒子不会在平直时空自发形成非平凡闭环；空间均匀的静磁场只能产生圆周/圆柱螺旋，不能维持环面三叶结轨道。
2. **条件存在性定理：** 对固定实验室坐标中足够光滑的恒速轨迹，可以构造所需的 B(t) 以及 Maxwell 相容的势、E(x,t) 和外部源 J(x,t)。轨迹是测试粒子运动方程的解。
3. **反例和工程边界：** 所构造的全空间 B 场不是有限能量分布；还缺少物理线圈、完整 Maxwell–测试粒子自场耦合和经典辐射反作用。
4. **实际动力学检验：** 使用 DOP853 对 relativistic Lorentz ODE 进行前向积分；用 6×6 单周期返回映射评估局部线性稳定性，基准 β=0.8 谱半径约 3.54。
5. **独立核验：** SymPy 符号恒等式、85 位 mpmath 独立解析求导、自动测试与 90 组随机参数案例；54 量纲、1431 对碰、33 公式审计；实际 Chromium 界面测试。
6. **科研任务闭环：** V93 的 177 项问题照原记录保留，V94 新增 28 项，总计 205 项，附逐项验收标准及明确状态。

## 主要文件

- `research/ROOT_V94_从作用量到闭环的全维审查.md`：完整中文研究正文、公式、参考来源、适用范围与开放问题。
- `research/严格证明与反例_定理目录.md`：10 条独立可审查的命题与限制。
- `src/inverse_maxwell.py`：轨迹速度、加速度、jerk、逆磁场、Maxwell 势与源、实际 relativistic ODE、Floquet 近似。
- `src/generate_results.py`：独立 85 位核验、参数扫描、5 张理论图及 JSON/CSV 数值输出。
- `src/dimension_and_ledger.py`：SI 量纲对碰及历史台账汇总。
- `src/symbolic_audit.py`：精确符号恒等式检查。
- `tests/test_inverse_maxwell.py`：39 项 Python 自动化测试（含 90 随机几何场例）。
- `results/NUMERICAL_SUMMARY_THEORY.json`：场、轨道、扰动、Lorentz boost、辐射基准的数值总览。
- `results/STABILITY_BY_BETA_THEORY.csv`：不同 β 的单圈乘子模。
- `results/V94_EQUATION_DIMENSIONS.csv`：明确列出量纲不合法的旧式与示例。
- `ledger/ALL_205_ISSUES.csv`：205 项任务和验收标准。
- `web/index.html`：无外部依赖的离线内外闭环实验室；不用于证明新物理。
- `archive/ROOT_V93_original.zip`：完整、未修改的 V93 原始历史科研包。

## 一键复现

系统要求 Python 3.10+。Windows 双击 `RUN_WINDOWS.bat`；Linux/macOS 执行 `sh RUN_LINUX_MAC.sh`。

```bash
python -m pip install -r requirements.txt
python verify_checksums.py  # 仅原始交付包运行；计算重生成后输出文件哈希会不同
python run_all.py           # V94 新测试、符号、量纲、数值和 V93 独立解压回归
# 已安装 Playwright 与 Chromium，并确认脚本中浏览器路径时，可附加：
python run_all.py --browser
```

如果重算结果，软件新生成的数据可能引起包内原始 SHA-256 与当前内容不同；验证原始包请先运行 `verify_checksums.py`，再运行计算程序。具体测试日志记录在 `results/VALIDATION_REPORT.json`。

## 核心结果与科学限制

在 R=10mm、a=2mm、m=2、n=3、β=0.8 的电子测试粒子模型中：逆磁场范围 0.108964–0.255744 T；独立 85 位比对最大相对差 7.33×10^-16；非线性 ODE 归一化误差约 1.63×10^-10；单周期线性扰动谱半径约 3.54087。**这些数值不是装置测得的真实数据。**

一个物体可以回到相同空间位置，但该事件与先前事件的时空坐标不相同。给定场可产生目标轨迹，不表示场由目标曲率“自然产生”，更不能直接推出万有引力常数、量子引力或 SU(3)×SU(2)×U(1) 的规范结构。所有新增候选问题仍接受反例和独立审查。
