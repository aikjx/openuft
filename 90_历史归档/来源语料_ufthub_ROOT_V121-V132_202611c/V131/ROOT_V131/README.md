# ROOT V131 — 规范阈值可行域与大统一反例审计

**项目性质：可复现的理论模型审计，不是四力统一证明。**

## 本轮核心结论

- 一枚 `SU(2)` 实三重态 Weyl 费米子 `(1,3,0)` 可在一圈近似下产生形式规范耦合汇合：`MU = 2.43264314534e14 GeV`，`Mtriplet = 8.050978055e6 GeV`。
- 增加一枚 `(8,1,0)` 八重态 Weyl 费米子，并要求所有新粒子质量处于 `[MZ,MU]`，严格得到条件性可行域 `2.4326431e14 ≤ MU ≤ 3.1442676e15 GeV`。
- 一圈形式汇合不意味着通过质子衰变限制、量子引力、第五力观测或现实规范统一。

## 复现步骤

Python >=3.9：

```bash
cd ROOT_V131
python -m unittest discover -s tests -v
python theory/v131.py
python theory/generate.py
```

`theory/v131.py` 仅使用标准库；`generate.py` 用标准库生成 JSON/CSV，安装 `matplotlib` 时额外生成 PNG。

### 历史版本

本包 `history/ROOT_V130_original.zip` 是保留原始 V130 归档的嵌套 ZIP。本轮另行重新执行 V130 的 54 项测试，但未对更早历史版本逐层执行。

## 目录说明

- `theory/v131.py`：阈值差分公式、解析反演、适用范围及条件性的质子寿命尺度。
- `theory/generate.py`：生成结构化结果与研究图。
- `tests/test_v131.py`：60 项新增数学/程序测试。
- `data/`：CSV、JSON 结果。
- `figures/`：三张解释性示意图。
- `reports/`：完整科研报告（含假设、证明、反例与文献链接）。
- `evidence/`：新增测试、V130 回归测试、环境与 SHA-256 清单。
- `history/`：原始 V130 压缩包。

## 验收与状态

新测试 60/60；V130 历史 54/54 本轮独立执行；没有声称真实实验物理验收完成。`SHA256SUMS.txt` 是本压缩包内容校验清单，不含清单自身。
