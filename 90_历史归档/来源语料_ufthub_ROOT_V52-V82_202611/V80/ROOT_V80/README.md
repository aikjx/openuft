# ROOT V80 · 星际—微观统一场论研究包

本版围绕 **G 与 c 的联系、变化电磁场对引力源的贡献、强磁场量子电动力学、星际紧致度与曲率、不同星体的场环境和观测证伪**。目标是建立可审计的跨尺度统一测试基准，**没有证明四力大统一，也没有无实验输入预测 G**。

## 一键运行

Python 3.10+。打开项目根目录执行：

```bash
python run_all.py
```

会重新生成数值 CSV/PNG、运行标准库 unittest 与可选 SymPy 符号检验；需要 `matplotlib` 才能绘图。浏览器直接打开 `web/index.html` 查看**完全离线**可交互的天体/磁场模拟（静态 Canvas2D 透视示意，不是 WebGL 或天体真实数字孪生）。

依赖安装：`python -m pip install -r requirements.txt`。离线网页不需要 Python 服务。

## 文件索引

- `book/ROOT_V80_星际微观统一场论研究总集.md`：15 章理论、完整假设/反例/引用。
- `src/cosmos.py`：13 组天体近似量及合成参数、G/c、场能、Schwarzschild 曲率、轨道与核验函数。
- `data/astro_reference.csv`：跨星体对照，含模拟/参考来源标签。
- `data/hypothesis_scan.csv`：**假说** ΔG/G=βBχB，不是物理发现。
- `data/equation_catalog.csv`：50 条分级公式，E/C/H/R/O 状态。
- `data/method_matrix.csv`：25 类独立观察/反例路径。
- `data/observational_constraints.csv`：MICROSCOPE、Cassini、双脉冲星、GW、EHT、磁星的公开约束与适用前提。
- `results/summary.json`：数值摘要；`results/browser_report.json`：交互检查；`results/verification.json`：测试报告。
- `charts/*.png`：3 张参考图；`results/browser_smoke.png`：真实 Chromium 页面测试截图。
- `SOURCES.md`、`PROOF_STATUS.md`、`SHA256_MANIFEST.csv`：来源、证明边界、文件完整性。
- `historical/`：V77 与 V79 的先前研究压缩包（如打包前校验存在）。

## 方法界限

1. 太阳系：NASA/JPL **近似**天体半径/质量；忽略椭球形变、自转、各层密度与精准天体星历。
2. 白矮星/中子星/磁星：**合成演示**质量、半径、代表磁场；未拟合 X 射线、脉冲星时序、EHT 或 GW 原始数据。
3. `K`：纯 Schwarzschild 外部几何参考，不能当作磁星自洽 Einstein–Maxwell 解。
4. B²/(2μ0ρmean c²)：**局域代表 B 与全星均密度的量纲比**，并非真实全星磁能比例。
5. B 接近/超过 BQ≈4.414×10⁹ T 时必须考虑强场 QED 非线性与磁化介质。
6. `G=2Z/c` 当 Z 定义为 Gc/2 时仅为恒等式。四力统一、ROOT 空间光速螺旋的自然实在性和微观无参数决定 G 均为未证明。
7. 自动测试和模拟验证的是模型/程序一致性，不是新的独立实验数据；绝不混淆。

**复现检查**：`python tools/browser_smoke.py` 用本机 Chromium 可选复测交互界面；如果没有 Chromium/Playwright，HTML 仍能离线打开。`python tools/package_release.py` 生成/校验 ZIP 文件。
