# ROOT V105｜规范闭环、螺旋相位与四力统一必要条件研究包

**性质：数学检验与候选理论分析，全部数据为 THEORY/MODEL。未发现新物理、未统一四力、未自主求出 G。**

继承：`archive/ROOT_V104_original.zip` 为 V104 原始完整科研包（保持字节原样）。`ledger/ALL_369_AUDITED_BASELINE.csv` 为 V104 369 项唯一追踪 ID 台账，不修改历史状态。

## 文件

- `research/01_ROOT_V105_科研总论.md`：主论文，解释轨迹几何、规范联络、标准模型以及新方向。
- `research/02_严格证明_规范群交换子.md`：U1 SU2 SU3 精确等式、单位/变分和适用条件。
- `research/03_协变候选作用量与量纲.md`：EH+SM+周期相位 EFT 的严格条件。
- `research/04_候选实验与证伪路线.md`：实验可行性前置条件与停止准则。
- `ledger/V105_关键问题_证据更新.csv`：对原有任务的重点交叉审查，不把开放问题改为已解决。
- `src/holonomy.py`：非阿贝尔 Wilson 群交换子的 numpy 模型。
- `src/eft.py`：无量纲紧致相位的 EFT 健康性、质量与量纲审计。
- `src/symbolic.py`：SymPy 精确恒等式。
- `src/generate.py`：生成理论 JSON、CSV 和图形。
- `tests/`：57 项实际 Python unittest。
- `web/index.html`：离线交互教学演示。
- `web/browser_smoke.py`：Chromium 实际浏览器检查。
- `VALIDATION_REPORT.md`：实际复运行结果。

## 环境与命令

```bash
python -m pip install -r requirements.txt
python run_all.py
python web/browser_smoke.py  # 可选：需 playwright+本地 Chromium
python verify_integrity.py  # 打包后的文件哈希审计
```

浏览器页面可直接作为 HTML 文件打开。如自动浏览器环境拦截 `file://`，测试程序会使用加载同一 HTML 内容的方法，不影响离线网页本身的算法实现。

**工程验收 ≠ 统一场论证明。**
