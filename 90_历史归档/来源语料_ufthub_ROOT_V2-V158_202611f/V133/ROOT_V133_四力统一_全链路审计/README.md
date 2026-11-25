# ROOT V133 可复算工程与历史整合包

- 版本：2026-11-24
- 科学状态：研究审计，**不是**四力统一证明。
- 单位：**只采用 c=1；ℏ、G 保留各自有量纲。**
- 环境：Python 3.9+，`verify_v133.py` 不需要第三方库；可在 Windows/Linux 使用 UTF-8 终端。

## 一键操作

Windows PowerShell：
```powershell
py -3 verify_v133.py
```
Linux：
```bash
python3 verify_v133.py
```

会重新生成 `data/` 里的 CSV/JSON 并输出 `PASS: ... checks`，每个检查的日志另存 `data/check_log.json`。

## 文件结构

- `研究报告.md`：严格推导、数值、限制、文献、状态。
- `verify_v133.py`：可复现检查脚本，纯 Python 标准库。
- `data/*.csv`：螺旋条件性筛选、Berry 相位收敛、RGE 曲线与输入扰动、异常精确扫描。
- `data/*.json`：检查摘要、参数、全部断言日志。
- `plots/*.png`：**可视化基准**，用于理解已知理论，不是测得的 ROOT 新发现。
- `下一步研究与判伪清单.md`：物理/统计审查门禁。
- `prior_versions/`：V2/V130/V131/V132 历史原始包（若可访问）。其科学结论不因归档而自动获验证。
- `ARCHIVE_MANIFEST.json`：实际归档的源文件、字节数和 SHA-256。
- `SHA256SUMS.txt`：不包含自身的 SHA256 文件列表。

## 分别理解检查层级

**Level A:** 数学恒等式与条件性证明通过；**Level B:** 合成数据程序能复现；**Level C:** 与权威观测数值对照（本包仅采用参考输入，非全面精密拟合）；**Level D:** 新理论的无调参预言经独立实验检验（**未达到**）。

不要将“137项PASS”解释为“ROOT 统一场论已被证实”。
