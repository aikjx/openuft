# ROOT V116 · 量子诱导引力 × 精密太阳系检验（396 项 OPEN 跟踪）

## 结论
从协变单标量作用量严格导出 BD 参数、长程标量引力 PPN γ、实验牛顿常数校准及有裸 Einstein–Hilbert 项时 QCD 尺度引力份额上界。证明**指定的**单 QCD 尺度轻标量诱导引力模型不能同时恢复观测引力强度和 Cassini 测试。**没有证明四力统一。**

## 一键复算

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -v
python tests/browser_smoke.py # 可选：需要 playwright 与 Chromium
```

依赖 `numpy`、`matplotlib`、`sympy`、`mpmath`。运行后输出 JSON 及四张独立图。页面 `web/index.html` 可直接在普通浏览器离线打开。

## 归档清单

- `research/01_完整科研总论.md`：完整模型和统计假设
- `research/02_严格定理_修复与失败条件.md`：6项证明与不适用条件
- `research/03_396项OPEN_验收与下一步.md`：开放任务决策矩阵
- `src/core.py`：纯函数计算核心、75位精算
- `tests/test_core.py`：44项测试，其中11项符号证明
- `ledger/V116_ALL_396_PRESERVED.csv`：历史396行字节原样保留
- `archive/ROOT_V115_original.zip`：原始 V115 完整科研包
- `results/V116_SUMMARY.json`：精算可复查结果
- `web/index.html`：离线计算和模型对照

所有场论单位默认 ℏ=c=1。输入的 G、α_s、M_Z 均为实验/基准，非第一性预测。使用 Cassini 原始 γ 的简单 2σ 阈值仅用于**长程无质量标量**，不可套成任意标量质量限制。
