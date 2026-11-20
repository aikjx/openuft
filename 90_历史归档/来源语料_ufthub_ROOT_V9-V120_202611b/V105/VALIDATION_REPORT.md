# ROOT V105｜实际执行验收报告

**证据标签：MODEL/THEORY。任何软件验收均不等于统一场论物理证明或真实实验。**

| 检验项目 | 验收结果 |
|---|---|
| V105 Python unittest | 57 项通过 |
| V105 SymPy 精确代数 | 12 项通过 |
| SI/自然单位质量维度自洽审计 | 12 项通过（包括拒绝不相容等式） |
| Chromium 离线页面运行 | 8 项通过，脚本错误 0 |
| V104 原始 ZIP 独立解压 Python pytest | 76 项通过 |
| V104 原始 ZIP SymPy 回归 | 9 项通过 |
| V104 基线问题台账 | 原样继承 369 行，369 个不同 canonical_id |
| SU2 闭环 | 精确公式与独立 numpy 矩阵一致 |
| SU3 嵌入闭环 | 精确公式与独立 numpy 矩阵一致 |
| U1 相位群交换子 | 恒为 1 |
| 新场 EFT | 形式量纲、周期势及小振幅质量通过 |
| 非阿贝尔矩阵幺正性/共轭迹不变性 | 通过 |
| 物理统一与 G 的推导 | **未完成** |
| 实际观测 | **无** |

说明：运行中修复了一个 `source_GeV4` 名称调用错误；浏览器因环境限制拦截 file URL，改用向 Chromium 加载同一 HTML 内容；滑块使用 step=any 避免端点被舍入。上述改动均已写入正式交付内容。

存档的 `archive/ROOT_V104_original.zip` 由原 ZIP 原样复制，不修改其历史记录。V105 的三项规范迹结果没有任何物理耦合的数值反推，不能声称完成四力。

**最终独立验收：通过。** 已将首次发布 ZIP 解压到全新目录 `/mnt/data/v105_independent_8P7e`，分别执行 `python verify_integrity.py`、`python run_all.py`、`python web/browser_smoke.py`，随后再次运行哈希校验。结果为 57/57 Python 测试、12/12 SymPy、8/8 浏览器，以及 30/30 个源文件 SHA-256 校验通过。该结果验证的是软件包可复现性，**没有**验证新的物理统一理论。
