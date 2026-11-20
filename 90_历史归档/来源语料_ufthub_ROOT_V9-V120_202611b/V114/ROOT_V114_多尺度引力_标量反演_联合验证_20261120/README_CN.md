# ROOT V114｜多尺度引力、标量反演、光传播联合审计科研包

**研究日期**：2026-11-20  
**科学状态**：条件性数学与程序验证通过；四力统一、\(G\) 本源、量子引力等根本目标 OPEN。

## 一键运行

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest tests/test_v114.py -q
python tests/browser_smoke.py
python verify_release.py --browser
```

上面的浏览器命令需要另外安装 Chromium 和 Playwright；物理计算、单元测试、图表不依赖浏览器。

## 研究文件

- `research/01_ROOT_V114_完整科研总论.md`：全部模型假设、严格定理、数值精算、现实物理适用边界
- `research/02_五项严格定理与失效条件.md`：五个定理的代数证明和反例
- `research/03_396项_OPEN_关键攻坚矩阵.md`：五大基础 OPEN 的闭合条件
- `src/v114.py`：Yukawa 力、局部空间曲率、双通道/双尺度反演、引力波色散
- `run_all.py`：从源码重新生成 JSON、250 组模型表、5 张计算曲线
- `tests/test_v114.py`：自动测试与 SymPy 符号验证
- `tests/browser_smoke.py`：真正的 Chromium 浏览器端到端控件验收
- `web/index.html`：无联网、可直接打开的交互引力反演实验室
- `ledger/V114_ALL_396_PRESERVED.csv`：前 396 项历史台账（保留原始字节）
- `archive/ROOT_V113_original.zip`：V113 完整历史科研包
- `VALIDATION_REPORT.md`：真实验收日志；`MANIFEST.json` 与 `CHECKSUMS.sha256` 用于独立校验

## 一项核心限制

\(\gamma_{\rm loc}(r)=\Psi/U\) 不是一个可直接从 Cassini 2003 的常数 PPN \(\gamma\) 结果逐点读取的真实数据。`results/` 的全部参数反演结果由**我们自己的合成输入**生成，未使用 Cassini 或 MICROSCOPE 原始观测数据，不得宣传为发现新引力或得到了真实质量排除限。

本版本关闭的是“指定模型内的数学和代码子任务”，**没有关闭完整四力统一的任何根本 OPEN**。
