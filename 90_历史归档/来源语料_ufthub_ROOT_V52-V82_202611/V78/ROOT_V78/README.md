# ROOT V78｜引力常数本源、变化电磁场与微观机制联合审计科研包

**版本时间：2026-11-17｜科学状态：现有理论复算 + 候选物理检验设计，不是四力大统一证明。**

## 这次实际新做了什么

1. 对 V77 `G=2Z/c` 和微观空间螺旋方案实施完整参数可辨识性、量纲与单位制度审查。
2. 系统验证 Maxwell 的总能量、能流、应力与两个电磁不变量——「不变量=0」不等于「能量=0」。
3. 新设计理想平行 `E//B` 反转实验：常规电磁能动张量保持偶对称，而 `E·B` 翻转符号。导出 **零伪标量背景时，平方曲率耦合不会产生磁场反转奇引力信号** 的选择规则。
4. 独立研究封闭装置能量守恒、交变磁场诱导电场、有限球 Yukawa 力和合成统计参数退化。
5. 修复了光子系统不变质量的浮点消差，以及大 `R/λ` 场景下球形 Yukawa 因子的数值上溢。
6. 交付了 22 章中文研究正文、55 条有证明状态的核心方程、36 条研究审查路线、73 项 Python 自动单元测试、13 项 SymPy 符号核验及 12 项 Chromium 页面交互检查。

## 文件树

- `book/ROOT_V78_统一场论攻坚_数值验收与微观机制审计总集.md` — 22 章、原始推导与反例。
- `data/equation_catalog.csv` — 55 条核心方程，E / C / H / R 等证据等级。
- `data/method_matrix.csv` — 36 条研究路线、失败机制、下一步检验。
- `data/*scan.csv` — 三类原始数值扫描。
- `src/core.py` — Python 标准库为主的物理公式与稳定算法。
- `src/cli.py` — 命令行科研计算界面。
- `tests/test_physics.py` — 73 项单元测试。
- `scripts/symbolic_checks.py` — 13 项符号校核（安装 SymPy 时实际运行）。
- `scripts/generate_results.py` — 数值 CSV、JSON 和绘图。
- `scripts/browser_smoke.py` — Chromium/Playwright 页面交互测试（可选依赖）。
- `web/index.html` — 完全离线的四模块交互实验室，原生 HTML、JS、Canvas2D，无外部 CDN。
- `results/` — 数值结果、图表、Chromium 截图、验收日志。
- `history/` — V77 历史科研版本的真实 ZIP 拷贝。
- `SHA256_MANIFEST.csv` — 全包文件的 SHA-256 哈希清单，避免将文件误认为数字签名。
- `PROOF_STATUS.md` — 每个核心命题的科研状态。
- `RELEASE_NOTES.md` — 版本变更与修复记录。
- `SOURCES.md` — 可检查的权威公开资料。

## 一键使用

在解压后的 `ROOT_V78` 根目录执行：

```bash
python run_all.py
```

独立运行：

```bash
python -m src.cli --B 10 --volume 1 --distance 10 --f 50
python -m unittest discover -s tests -v
python -m scripts.generate_results
python -m scripts.symbolic_checks
```

离线网页：双击 `web/index.html`。它不需要网络、第三方帐号或部署服务器。

可选绘图与符号依赖安装：

```bash
pip install -r requirements-optional.txt
python -m scripts.browser_smoke
```

脚本 `run_all.py` 使用 Python 标准库即可完成 73 项单元测试与 JSON/CSV 计算；SymPy 若缺失会明确标为跳过，Matplotlib 若缺失会只生成数值文件。**不要把跳过的检查报告为通过。** 可选浏览器测试需要 Playwright 和本地 Chromium。

## 验收判定与限制

- 单元测试只验证科学公式实现与指定条件的数值性质。
- 符号检查只验证代数、变分背景和一定范围内的极限关系。
- 浏览器测试在本环境被禁止直接使用 `file://`，因此将相同 HTML 字节装载进 Chromium 后测试 JS 与 UI；没有验证实际客户机的 GPU、文件权限和部署配置。Canvas2D 图表不等于真正的 WebGL 地球数字孪生。
- 理想均匀磁场体积只用于能量当量示例，并非完整自洽的真实线圈装置。
- 人工合成回归里的 `G` 是 **CODATA 2022 数值注入**，绝不是无输入新预测。
- 「四力统一」「G 单由 c 或变化电磁场决定」都**尚未证明**。

## 正式宣告条件

若要转为真实新理论：必须给出独立冻结的微观作用量，明确 UV 完成、粒子谱与量子一致性；在不回填实测 G 的前提下导出普适引力耦合，提出与现有理论不同的可观测量，并经独立实验重复确认。没有证据则不得宣告成功。
