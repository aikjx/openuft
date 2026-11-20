# ROOT V89 · 量子引力相位、经典媒介与 EFT 独立证伪科研包

**目的**：对 ROOT V50—V88 的引力源、双体相位、量子关联和量子引力文献做严格交叉审计。不是完整四力统一证明；没有实物量子引力测量。

## 目录

- `book/`：22 章中文研究总论。
- `src/quantum_gravity_audit.py`：可复用 SI 量纲与双系统物理计算。
- `tests/`：单元测试、符号检查和独立积分。
- `scripts/generate_results.py`：确定性合成数据、5 张曲线和高精度滤波审计。
- `web/index.html`：离线可操作实验室，不依赖远程网络。
- `protocols/`：实验控制、零实验与经典媒介模型检验的机器可读 JSON。
- `data/`：核心方程目录、方法审查、5 个带 `SYNTHETIC` 后缀的数据集。
- `results/`：报告、验收与浏览器截图。
- `archive/ROOT_V88.zip`：直接历史研究包。

## 运行

```bash
python -m pip install -r requirements.txt
python run_all.py
```

如果系统已安装 Playwright 和 Chromium，可以执行：

```bash
python web/browser_smoke.py
```

请在 Python 3.11+ 运行；Windows 可运行 `RUN_WINDOWS.bat`，Linux/macOS 可运行 `RUN_LINUX.sh`。运行会覆盖 `results/` 内同名**计算生成文件**，不会修改历史 V88 包。

## 模型状态

演示质量 1e-14 kg、双分支间距 200 μm、距离 450 μm、作用时间 1 s；Newton 非局部相位 `-0.06923945973538509` rad。低能 EFT 势展开是用来估计量级的**约定性模型项**，不是一台可见装置的完整规范不变可观量。90 位十进制算法演示了如何排除浮点伪信号。

**所有数据均为数学预测或合成模拟，绝不能当作真实科学发现。**
