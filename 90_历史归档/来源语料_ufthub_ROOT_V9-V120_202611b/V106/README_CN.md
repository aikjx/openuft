# ROOT V106｜复现与研究说明

本包基于 ROOT V105 原始文件，新增 69 项 Python 自动测试与 19 项符号检查，以及单相位规范曲率 no-go、两相位 SU2 例子、标准模型一代异常抵消、SU5 正规化和最简 SM 单圈非统一数值审计，并增加 G 量纲 no-go。

**本包不宣称四力已经统一；代码测试不是现实实验。**

## 运行环境

Python 3.10+。在解压目录中执行：

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_integrity.py
```

`run_all.py` 可以从任意工作目录执行，自动生成 `results/numerical_summary_THEORY.json`、`results/gauge_running_ONE_LOOP_THEORY.csv` 和 `figures/` 两张理论图。

网页 `web/index.html` 无 CDN、无后端，可直接在浏览器中打开，调节 sin²θW 与 αs，实时查看三耦合交点。对于 Chromium 安全沙箱，`web/browser_smoke.py` 用 HTML 内容加载同一页面进行检查。

历史原包位于 `archive/ROOT_V105_original.zip`，与新版源码相互独立。`python legacy_regression.py` 在临时目录运行其原生 `run_all.py`；独立环境必须安装历史版本依赖。

## 交付文件

- `research/01_ROOT_V106_完整科研总论.md`：严格证明、异常抵消和单圈 RG 数值。
- `research/02_严格证明与反例_单相位_异常_耦合.md`：五项证明及反例边界。
- `research/03_未来突破任务与证伪路线.md`：15 项新专项任务、明确开放问题。
- `ledger/ALL_369_AUDITED_BASELINE.csv`：完整历史台账保留。
- `ledger/V106_15_tasks.csv`：本轮重点新任务。
- `src/`、`tests/`：程序及自动化检查。
- `results/`、`figures/`：理论/模型数据，绝非观测。
- `VALIDATION_REPORT.md`：实际测试状态和已知限制。

## 核心数值输入

仅为演示的 MSbar 附近基准：MZ=91.1876 GeV，1/αem(MZ)=127.930，sin²θW=.23122，αs(MZ)=.1180。最简 SM 一圈 b=(41/10,−19/6,−7)；**不存在单圈三条耦合的精确共同交点**，不等同于排除全部高能统一理论。

浏览器真实界面自动化需要额外安装 `playwright` 及兼容的 Chromium；科研核心计算不依赖浏览器。
