# ROOT V113｜五维标量 × 精密引力 × 四力统一可证伪攻坚包

**状态：数学/数值模型审计完成；真正四力统一仍然 OPEN。**

## 本轮科研结果

- 最简 5D KK 无质量 radion 的标准 4D Jordan 普遍物质耦合极限：Brans–Dicke ω=0 ⇒ PPN γ=0.5；与 Cassini 公开测量强烈冲突，排除这一**带条件的低能模型**，不排除所有高维统一理论。
- 标准无质量 Brans–Dicke ω≥0 的 Cassini 简化 2σ 比较给出 ω≥39998；并非重新拟合原始实验数据。
- 含质量标量的局部 toy γ(r) 可被 Yukawa 抑制；1AU 示例 mφ≈1.3443×10⁻¹⁷ eV **不能冒充真实 Cassini 对标量质量的实验下限**。
- MICROSCOPE 测试材料耦合差，Cassini 检查 PPN γ；普遍标量耦合可令 η_AB=0 而 γ≠1，这两个判据必须联合使用。
- 两尺度局部标量测量给出非零雅可比行列式，数学上解除单尺度两参数退化，但不保证现实可测；同时解释了为什么仅有一组关联关系不能独立推出 G。
- 代数 Einstein–Cartan 轴向挠率消去只得到局域四费米接触项，不自动生成新长程基本力。

## 一键运行（项目根目录）

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest tests/test_v113.py -q
```

实际浏览器测试（可选；需另行安装 Playwright 和 Chromium）：

```bash
python tests/browser_smoke.py
```

离线实验室直接打开 `web/index.html`；支持调节 ω、标量质量、作用尺度、物质耦合差和第二观测距离，显示曲线与对比。

## 交付目录

- `research/01_ROOT_V113_完整科研总论.md`：完整四力统一研究总论、场方程与实验边界。
- `research/02_八项严格定理与反例.md`：八项有明确假设的定理、严格反例。
- `research/03_四力统一五大OPEN_决策矩阵.md`：核心理论 OPEN 与关闭条件。
- `src/v113.py`：所有数字来源、单位与模型计算。
- `tests/test_v113.py`：109 项 Python 测试（含精确 SymPy 代数验证）。
- `tests/browser_smoke.py`：11 项可运行的 Chromium 浏览器检查。
- `run_all.py`：生成数据、CSV 和四幅理论图。
- `results/`：基准参数、真实文献输入和数值结果。
- `figures/`：4 幅理论图 + 1 幅实际 Chromium 截图。
- `ledger/V113_ALL_396_PRESERVED.csv`：从 V112 直接复制的全部 396 项历史台账，不篡改 OPEN。
- `archive/ROOT_V112_original.zip`：上一代完整科研包。
- `VALIDATION_REPORT.md`、`CHECKSUMS.sha256`、`MANIFEST.json`：测试、文件哈希、交付溯源。

## 本轮没有完成的工作

完整的量子引力 UV 完备性、强弱作用粒子谱的独立推导、无循环求出 G、独立于现有 GR+SM+KK+ALP 的新预言、前瞻实验验证，仍不能宣布解决。

## 文件日期

2026-11-20。
