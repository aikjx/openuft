# ROOT V128｜核心统一曲率方程、Lorentz 反例与可复现验证

## 核心结论

- **数学成立（既有理论）**：统一协变导数的对易子同时包含时空自旋曲率和三个规范场的曲率。
- **数学反例（本轮严格推导）**：三维光速螺旋频率 \(\omega\) 是坐标量，`m_try=ħω/c²` 在 Lorentz boost 下不恒定，不能作为通常的粒子不变静质量。
- **条件性替代**：五维 null 运动允许四维 timelike 投影和 KK 离散谱，但需要新增维度/尺度且尚未预测标准模型。
- **科学状态**：未发现新物理，未完成量子本源或四力大统一。

## 一键复算

在 `ROOT_V128` 根目录运行：

```bash
python -m pip install -r requirements.txt
python scripts/run_v128.py
python -m pytest -q tests
python verify_manifest.py
```

`results/audit_results.json`：关键数值；`results/lorentz_boost_SYNTHETIC.csv`：不同 boost 下错误“质量”比例；`figures/lorentz_noninvariance_SYNTHETIC.png`：合成曲线；`reports/ROOT_V128_最核心统一曲率方程_数学审计.md`：完整推导。

## 数据和测试的含义

70 项为单元/数值测试，不代表真实高能实验、第五力实验或大统一模型验收。根目录包含 V127 原始 ZIP 作为可追溯历史附件，但没有在 V128 默认脚本中重新执行所有历史长链路测试，避免混淆累计数与本轮真实跑通的测试。
