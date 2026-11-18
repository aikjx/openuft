# ROOT V67｜正式统一场论研究总集与可复现科研工程

**2026-11-17 · 科学状态：没有证明四力大统一，也没有从 ROOT 螺旋公设独立预测 G。** 本版提供的是完整的 *审计、条件证明、数值测试、可视化及失败原因修复* 研究工程。不要把软件可运行或数学恒等式理解为发现新自然定律。

## 一、立即使用

1. **读新研究总书：** `book/ROOT_V67_统一场论_正式研究总集.md`，22 章新正文，实际字数见 `book/manuscript_statistics.json`。历史 V66 完整研究材料在 `archive/`。
2. **体验交互模拟：** 用 Chrome、Edge、Firefox 双击打开 `web/index.html`，完全离线。五个页签：空间螺旋 3D 透视、球形地球与理想磁偶极、标准模型一圈规范耦合运行、诱导引力 G 反向标定、第五力等效原理示意。
3. **跑数学回归：** Python 3.10+，在本目录运行 `python run_all.py`；纯标准库运行多数测试，若安装 SciPy 则进行独立比较。报告写入 `results/verification_report.json` 和 `results/test_log.txt`。
4. **重算所有曲线/数据：** 安装 `pip install -r requirements-optional.txt`，执行 `python experiments/generate.py`。还可运行 `python experiments/derive_variational.py` 验证有限自由度变分和 U(1) 规范不变性。
5. **浏览器复测：** `python experiments/browser_smoke.py` 需要 `playwright` 与本地 Chromium；测试容器阻止 `file://` 导航，使用 `page.set_content` 加载**同一份 HTML 源码**并点击页签与滑块，因此未完成实际文件系统导航的自动化复验。
6. **检查交付完整性：** `python VERIFY_PACKAGE.py` 对源码文件 SHA-256 核验。另可使用 ZIP 工具“测试压缩包”。

Windows：双击 `RUN_ALL.bat`；Linux/macOS：`sh RUN_ALL.sh`。如果未安装可选科学计算库，独立实验脚本会报出缺少依赖；这是环境依赖，不是物理理论失败。

## 二、新增核心数学进展

- **[MATH] 运动学：** Frenet 曲率与挠率准确求导、含退化条件的反演。速度 `v=c` 仅作数学运动假设，不可直接解释有质量粒子实际速度。
- **[COND] 量子场：** 有螺旋相位的 KG 圆柱本征模，给定边界与场归一化后解析能量积分和独立积分吻合。
- **[EST/COND] 引力源：** 给定 GR 时，可以计算微观场的应力能量对宏观引力源的贡献，但 Einstein–Hilbert 项中已预先包含 G。
- **[COND/FIT] 诱导引力：** 在明确 UV 固有时间截止下计算阈值函数 `F(μ)`，展示 `N, ξ, μ, ℓ, G_bare` 的不可辨识性，**不是 G 的独立预测**。
- **[COND] 规范论：** 复算标准模型一圈 SU(5) 归一化规范耦合三交点不相同；精确有理数核对一代规范异常抵消。结果不否认其他高能完成。
- **[COND] 高维几何：** 5D 圆形纤维的一形式在 KK 坐标变换下保持不变，条件性得到 4D Abelian 规范变换。无法仅此得到 SU(2)、SU(3)、量子引力和 G。
- **[CANDIDATE] 新场：** 给出带螺旋相位可能性的伪标量 χ 与 `χ F Ftilde` 耦合候选作用量，明确变分方程、可证伪思路及未满足的理论义务。

## 三、本版真实结果（验证文件为准）

- 新研究正文 22 章，准确字符数用 `book/manuscript_statistics.json`。
- 60 条失败根因矩阵：其中 `CORRECTED` 仅是已修复的陈述/数学处理，`OPEN` 是仍未证明的物理问题。文件 `data/ROOT_V67_逐项失败原因与修复矩阵.csv`。
- 自动测试 `run_all.py`，测试数与通过数以实际生成的 JSON 为准。
- 五张可重算数值图、五个 HTML 交互模块。
- 版本基于 2026-11-17 已核对的 NIST/PDG/MICROSCOPE/Cassini/GW170817 公共文献。

## 四、为什么不能宣布成功

统一要求从**独立的微观公设**导出正确的引力低能极限、SU(3)×SU(2)×U(1) 规范理论、手征费米子与粒子谱、全部独立耦合和可检验新预测。ROOT 的螺旋几何、拟合 G 或把 GR+SM 写在同一作用量中，并未满足这一要求。因此本版保持 `OPEN` 科学状态。最重要的待解题为：独立给出微观长度或质量尺度与 G；推导完整的手征规范结构和异常抵消；证明量子一致性及新物理观测差异。

## 五、目录

`book/` 正文、分章、统计；`src/` 纯标准库内核；`tests/` 自动测试；`experiments/` 数值生成、符号变分、浏览器烟测、错误矩阵构建；`data/` CSV；`results/` JSON、PNG、烟测截图与测试记录；`sources/` 原始出处；`web/` 离线 HTML；`archive/` V66 完整历史包（内含再早版本），不保证历史所有科学断言正确。
