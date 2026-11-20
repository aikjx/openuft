# ROOT V86｜G 的来源、星体差异与四力统一：漏洞修复、数值计算与可证伪实验包

**完整科研专著：** `book/ROOT_V86_G来源_星球差异_四力统一_漏洞修复与独立证伪总论.md`。

**状态：** 当前科学问题中的 `G` 独立预测、跨星球基本常数变化及四力完整统一均为**开放问题**。本包完成了明确前提下的数值推导、模型审计、反例和软件复现；**没有真实引力仪器或原始实测新力数据**。

## 一键运行

- Windows：双击 `RUN_WINDOWS.bat`。要求可用的 Python 3.10+；依赖按需安装。执行公式和程序测试、生成合成数据，完成后打开本地 HTML。
- Linux/macOS：在终端 `bash run_linux_macos.sh`。
- 已安装依赖：直接 `python run_all.py`；跳过 Chromium 可使用 `python run_all.py --skip-browser`。
- 浏览器完整性检查需另行准备 Playwright 和 Chromium，然后运行 `python tools/browser_check.py`。普通离线页面无需任何服务器或 CDN。

## 内容

| 位置 | 说明 |
|---|---|
| `src/physics.py` | Newton/J2/有限球 Yukawa 及精确 Eötvös 前向公式 |
| `src/geometry.py` | 分层球、两球及独立体积分 |
| `src/inference.py` | GLS、相关噪声、自助 rank-1、λ 参数扫描 |
| `tests/` | 自动回归测试和反例 |
| `tools/symbolic_audit.py` | 19 项 SymPy 解析公式审查 |
| `data/` | 52 条公式、40 项路线及全部带 SYNTHETIC 的合成 CSV |
| `spec/` | ROOT-GCL/2.0 四份机读实验方案（不是仪器驱动） |
| `results/` | 四张数值曲线、摘要、统计报告、实际 Chromium 截图 |
| `web/index.html` | 本地离线交互可视化：J2、Yukawa、Q、D vs eta、实验语言 |
| `history/` | V85 完整归档的历史入口，便于回溯旧研究 |

## V86 核心修复

1. 既有的径向形状量 `Q=1` 只适用于球对称牛顿外场，地球 `J2` 就会构造出看似新力的 `Q≠1`。
2. 单一可分离媒介的 **D 差分矩阵**可严格秩一，但**精确 Eötvös 比值矩阵**一般不严格秩一，不能混用判据。
3. 有限程效应依赖源内**新荷密度分布**和测试体自身有限尺寸，不能只用一颗星球的总质量和平均密度。
4. 相关噪声下的奇异值不是直接证据；补充 GLS、bootstrap、参数退化及已知非球形效应反例。

## 实验标记

- 文件名含 `SYNTHETIC` 的 CSV、所有 p 值、注入 α 和 λ、模型扫描均属于计算机生成的演示数据。
- `data/reference_constraints` / `results/reference_constraints.json` 复制并说明公开文献摘要数值，没有重新处理原始天文观测。
- 源质量、电磁开关与设备联锁协议都是实验**设计草案**，不会驱动真实高压、强磁场或重物机械设备。
- 软件测试通过不能认证真实科研结果或现场仪器安全。

## 独立计量、统计和科学开放性

轨道只约束 `GM`；用同一 G 倒算星体质量再声称发现 G 规律会循环论证。若要追求真正突破，需从可变分的底层作用量独立给出引力尺度、满足 GR/Maxwell/标准模型低能极限，并通过多距离、跨材料、跨源和独立仪器盲测约束。
