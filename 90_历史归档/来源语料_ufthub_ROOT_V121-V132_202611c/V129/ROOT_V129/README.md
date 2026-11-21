# ROOT V129 — 量子规范反常、超荷、五维质量—电荷统一审计

## 交付是什么

本包对接 V128，独立验证了三类核心结论：

1. 单代标准模型超荷与手征规范反常的精确代数，包含右手中微子存在与不存在的两种情形；
2. 无裸质量、同圆周动量同时产生电荷与质量的最小 KK 模型不能同时解释电子与 μ 子；
3. 固定 radion、标准归一化、纯引力 KK 光子模型的圆半径若按电子质量确定，电磁规范耦合会相差约 `1.0205e21` 倍；
4. 经 Lorentz 变换的自由场相位是标量，但此处的质量与 hbar 仍为输入。

**不是**量子本源、G 的本源或四力大统一的完成证明。

## 一键复现

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_v129.py
```

第一个脚本在 `results/tests_v129.log` 记录本轮已运行测试结果（60 tests）；第二个生成 `results/v129_exact_and_numeric.json`、`results/mass_charge_spectrum_SYNTHETIC.csv` 以及 `figures/*.png`。

## 文件结构

- `reports/ROOT_V129_量子反常_质量电荷几何统一审计.md`：论证、限定条件、成果、未解决问题。
- `scripts/v129_core.py`：精确异常多项式、超荷族、KK 质量、耦合与 Lorentz 相位计算。
- `scripts/run_v129.py`：结果数据和图表生成。
- `tests/test_v129.py`：60 个单元测试，含多个逐参数子测试。
- `results/`：此次真实运行结果。
- `figures/`：**SYNTHETIC** 图，不是实测。
- `references/sources.md`：文献来源与归一化约定。
- `prior_v128/ROOT_V128_original.zip`：历史原包，非本轮测试成功的证明。
- `MANIFEST.sha256`：归档清单，校验当前版本文件。

## 约束与研究伦理

所有新数据图是数学合成图。未使用真实卫星轨道或实际电子/μ 子源实验数据进行模型拟合。新包只对 60 项 V129 测试负责；虽携带 V128 的历史 ZIP，但不冒充对 V128 全部测试进行回归验收。
