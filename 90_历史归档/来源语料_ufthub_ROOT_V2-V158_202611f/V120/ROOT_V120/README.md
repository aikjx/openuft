# ROOT V120 — 螺旋几何谱论、引力本源与人工引力可行性研究

日期：2026-11-21。研究性质：探索性数学模型与已知物理的对照；**没有证明四力统一或实现可控人工引力**。

## 内容
- `docs/theory.md`：公式、推导、已知/假设/待证的逐项区分
- `docs/engineering.md`：人工引力、旋转栖居地、磁场能量、星际工程与可证伪实验
- `docs/audit.md`：主要漏洞、失败条件与下一步研究计划
- `src/compute.py`：可复现的 SI 数值计算；`data/results.json`：计算结果
- `tests/test_compute.py`：自动化测试

## 运行
```bash
python src/compute.py
python -m unittest discover -s tests -v
```
依赖：Python 3 标准库。几何模型采用 c=1；工程计算将 c 恢复为 SI 常数。

## 核心结论
螺旋曲率挠率恒等式可证明，但不自动给出引力场方程；谱算子是候选结构，未推导标准模型。电磁能量产生引力在 GR 中已成立，但数量级极弱。最现实的可控类重力方案是旋转产生的惯性加速度，而非制造新的引力源。
