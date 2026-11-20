# ROOT V110｜Floquet 参数共振与有限能量闭环研究包

**属性**：理论数学、受控模型的数值仿真、符号校验、反例构造；**不是实验观测，更不是四力统一证明**。

## 快速运行

```bash
python -m pip install -r requirements.txt
python src/symbolic_audit.py
python -m pytest -q tests/test_v110.py
python src/generate.py
python verify_integrity.py
```

通过 `web/index.html` 可以离线调整参数并运行浏览器内的单周期矩阵仿真（浏览器图仅做理论演示）。

程序不需要网络、密码或外部服务。离线页面使用原生 JS Canvas。

## 包内目录

- `src/v110.py`：外源 Floquet 单周期基本矩阵、扫描及双光模反作用积分
- `src/symbolic_audit.py`：SymPy 解析恒等式检查
- `src/generate.py`：理论 JSON、CSV 和图表重新生成
- `tests/test_v110.py`：数值和物理一致性自动测试
- `research/`：完整中文科研总论、证明、OPEN 验收矩阵
- `results/`：独立理论数据，均包含 THE0RY 标记或 meta 声明
- `figures/`：理论模型计算图
- `ledger/V110_ALL_396_PRESERVED.csv`：396 项历史原始状态，不擅自关闭 OPEN
- `archive/ROOT_V109_original.zip`：完整 V109 历史研究归档
- `web/index.html`：离线可交互实验室

## 符号与计算定义

自然单位 \(c=\hbar=1\)，数值时间和频率经任意参考标度无量纲化；数值不能直接当作秒、电子伏特或实验设备读数。

主要结果：完整周期后 \(\Delta\theta=0\) 时仍可能 Floquet 放大；双圆偏振 Floquet 谱相同；闭合 Lagrangian 的能量在自洽模型内严格守恒。三项均不为 ROOT 特有定律。

## 验收约定

- 测试通过只说明对应模型和软件的指定性质满足条件。
- `run_all.py` 分成快速、数值、历史三部分，其中历史原始归档并不默认全部重新执行，以避免环境依赖；独立核验范围在 `VALIDATION_REPORT.md` 中记录。
- 原始 396 项研究问题并非全部科学意义上被解决；本轮专项工作记录与历史台账分开管理。
