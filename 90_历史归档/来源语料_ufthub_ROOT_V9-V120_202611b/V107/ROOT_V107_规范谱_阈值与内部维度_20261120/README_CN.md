# ROOT V107｜规范谱与阈值统一的条件性攻坚科研包

版本日期：2026-11-20。项目承接 ROOT V106 完整科研包（`archive/ROOT_V106_original.zip`）。**不会宣称完整四力统一已攻破。**

## 实际完成

- 不引入右手中微子的最小一代标准模型超荷，依赖给定谱、Yukawa 与异常抵消，可以推得**相对比例**；引入 Dirac 右手中微子后存在 B−L 一参数歧义。
- Dirac 矢量样 SU5 的完整 5+5̄ 多重态在质量简并下对三个 beta 函数具有相同贡献，不能修复固定一圈失配。
- 在具体阶跃阈值 toy 中，一组分裂多重态需要 MT/MD≈7.266×10^18，超出 MZ—Planck 约束；两组可以数学上产生一圈交点，但尚未通过质子衰变和两圈检查。
- 若联络完全由 k 个光滑内部相位拉回，k≤3 时局部 Tr(F∧F)=0；k=4 可以有非零局部例子，但没有证实非零全局二陈数。
- 保留 V106 的全部 384 项研究任务，并新增 12 项：共 396 个唯一 ID。所有仍未解决的四力统一问题保持开放。

## 环境与复现

Python 3.10+，SymPy、mpmath、numpy、matplotlib、pytest（各版本使用 `requirements.txt`）。从本目录运行：

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_integrity.py
python legacy_regression.py
```

可选 Chromium 页面检查（需系统安装 Chromium 和 Python Playwright）：

```bash
python web/browser_smoke.py
```

程序不需要联网；`web/index.html` 没有外部 CDN 或后端，可离线直接打开。旧版完整科研 ZIP 位于 `archive/`，历史回归程序会先在临时目录解压，不改动原档。

## 文件说明

- `research/01_ROOT_V107_完整科研总论.md`：理论、推导、限制及来源。
- `research/02_严格证明与失败条件.md`：五个条件定理及反例、量纲审计。
- `research/03_下一阶段必须解决的开放问题.md`：延续科研目标。
- `src/theory.py`：异常约束、SU5 多重态 beta、阈值模型、维度 4-form 的数学引擎。
- `src/symbolic_audit.py`：精确 SymPy 恒等式核验。
- `src/generate.py`：80 位精算、CSV 及科学图。
- `tests/test_theory.py`：自动化单元与反例测试。
- `ledger/ALL_396_UNIQUE_ISSUES.csv`：369+15+12 的可追溯问题总账。
- `results/*THEORY*`、`figures/*THEORY*`：全部是模型数据，不是实验数据。
- `web/index.html`：可操作的理论交互演示。
- `VALIDATION_REPORT.md`：真实运行与未实现项。

## 证据标签

数学定理 [M] 仅在已声明前提下成立；模型数值 [N] 并不构成自然界的实验发现；外部文献 [L] 用于背景验证；开放问题 [O] 不得假定关闭。

**ROOT V107 未独立计算 G，未观测引力子的量子态，未得到标准模型与引力的 UV 完备统一，也未证明螺旋是四力共同本源。**
