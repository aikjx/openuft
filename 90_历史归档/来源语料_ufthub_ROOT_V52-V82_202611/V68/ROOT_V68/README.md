# ROOT V68｜引力常数、规范结构与量子一致性攻坚科研包

**科学状态：未证明四力大统一。** 本交付包含对三大缺口的严密反例、条件推导、真实数值执行及科研可审计材料。新作用量不是从螺旋运动学推出的全部标准模型，不得据此对外宣称取得四力统一的完整物理证明。

## 一、直接运行

1. 阅读：`book/ROOT_V68_三大证明缺口_正式研究专著.md`（18 章；已将“已证明 / 已知 / 玩具 / 反拟合 / 开放问题”分开）。
2. 交互界面：浏览器打开 `web/index.html`，完全离线。五个页面：螺旋、G 参数退化、一圈规范耦合、组成依赖第五力、科研裁定。使用 Canvas2D 三维透视，**不使用 WebGL GPU、无在线实验数据**。
3. 运行单元测试：在 ZIP 解压后的 `ROOT_V68` 文件夹运行 `python run_all.py`（Python 3.10+，标准库即可）。
4. 生成数值：先 `pip install -r requirements-optional.txt`，再运行 `python experiments/run_numerics.py`。
5. 符号交叉检查：安装 SymPy 后运行 `python experiments/symbolic_checks.py`。
6. 浏览器自动化烟测：安装 Playwright 与 Chromium 后 `python experiments/browser_smoke.py`；本版在 Chromium 通过 `page.set_content(网页实际字节)` 测试，**不宣称测试了 file:// 操作系统权限或 WebGL**。
7. 完整性：`python VERIFY_PACKAGE.py` 验证压缩包文件哈希清单。

**运行条件**：Windows：`RUN_ALL.bat`；Linux/macOS：`sh RUN_ALL.sh`。基础测试零第三方依赖。可选脚本需要 SciPy、NumPy、Matplotlib、SymPy、Playwright，版本范围见 `requirements-optional.txt`。

## 二、本版关键可复算结论

- [THEOREM] 只含 c、ħ、无量纲螺旋角不能构造 G 的量纲；必须产生一个独立尺度或等价动力学。
- [THEOREM] 圆柱螺旋曲率、挠率及反演公式在明确非退化域内成立。
- [COND] 指定一圈热核截止表达式能够诱导有效曲率项，但系数依赖 N、ξ、m、ℓ、G_bare；拟合 G 不唯一。
- [KNOWN/VERIFIED] 一代标准模型费米子的异常抵消可用精确有理数求和验证；这并未推导出该粒子谱。
- [KNOWN/TOY] 采用固定标准模型一圈 β 系数和所列演示输入，三规范耦合不在同一能标精确交会。
- [COND] 五维圆纤维一形式可出现四维 U(1) 规范变换，但不能自动得到完整 SU3×SU2 结构。
- [OPEN] 从 ROOT 无外部校准计算 G；从单一原理生成手征谱；完整量子 UV 幺正和独立新物理实验检测。

## 三、目录

- `src/root_v68.py` — 可运行的纯标准库科学计算核心。
- `tests/test_core.py` — 显式单元测试（真实运行数量记录在 `results/`）。
- `experiments/run_numerics.py` — 独立数值扫描、CSV、PNG 图表。
- `experiments/symbolic_checks.py` — 独立 SymPy 微分、变分与规范不变性检查。
- `experiments/browser_smoke.py` — Chromium 实际页面交互核对。
- `book/` — 完整中文正文和研究限制。
- `data/` — 原始数据及逐项证明缺口矩阵。
- `results/` — 实际运行日志、JSON、图像与测试结果。
- `sources/` — 公共来源链接与观测/假设分类。
- `web/index.html` — 可离线交互的科学演示实验台。
- `archive/ROOT_V67_历史完整科研包.zip` — 上一版完整科研档案（历史论断应重新审核）。

## 四、禁止误读

**计算正确 ≠ 理论物理正确 ≠ 独立观测发现 ≠ 四力统一成功。** 本版数值精度衡量的是实现误差，不是对新自然律的实验检验；后续需要同行评审及独立实测。
