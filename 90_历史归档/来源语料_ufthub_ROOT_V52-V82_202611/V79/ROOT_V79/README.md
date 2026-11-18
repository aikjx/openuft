# ROOT V79｜变化电磁场的谐波、手性与引力源：严格科研审计包

**日期：2026-11-17｜工程状态：离线可复算；科学状态：没有发现新引力，没有预测 G，没有实现四力统一。**

## 为什么做 V79

V78 已证明在既定作用量里 E·B 的奇宇称不能直接等价为引力源。V79 进一步检验三条机制：

1. **时域频率：** B(t) 以 f 变化，但 B² 所给能量在 0 和 2f；感应 E 场能量也必须计入。
2. **候选手性：** E·B 可以在 f 上驱动一个 *假设的* 伪标量；a² 曲率耦合在 a0=0 时只带 0 和 2f，而 a0≠0 时允许 f。
3. **系统守恒：** 总装置的磁场增能若由电池供能，封闭系统总质量不能因内部能量转换凭空增加；四极时变不等于单极质量变化。

## 文件结构

- `book/ROOT_V79_时变电磁引力与手性场全链路研究专著.md` — 20章，推导、适用范围、模型反例和实验设计。
- `data/equation_catalog.csv` — 66条可搜索的公式与科学状态。
- `data/method_matrix.csv` — 28条检查/实验路线。
- `data/` 其余5个 CSV — 磁场扫描、频率适用性、时间账本、B反转、候选轴子谐波。
- `src/core.py` — SI 场能、Tμν、Lorentz提升、法拉第积分、守恒、多极量级、候选谐波的程序实现。
- `tests/test_core.py` — unittest 自动数学与数值检查。
- `tools/symbolic_check.py` — SymPy 独立公式/积分校核。
- `tools/build_data.py` — CSV、JSON、PNG数值复算。
- `tools/browser_check.py` — Chromium 页面实际点击与滑块检查。
- `tools/verify.py` — 文件SHA-256核验。
- `web/index.html` — 单文件离线交互实验室。使用 Canvas2D，不是 WebGL 引力数字孪生。
- `results/` — 实际运行数据、绘图、浏览器截图与测试报告。
- `history/ROOT_V78_历史归档.zip` — 上版历史研究文件原样归档。

## 一键执行

解压 ZIP 后在 `ROOT_V79` 根目录执行：

```bash
python run_all.py
```

只用 Python 标准库：

```bash
python -m unittest discover -s tests -v
python -m src.cli --B 10 --f 50 --radius 1 --distance 10
```

可选外部依赖（若未安装，项目会明确报告跳过，而非伪称通过）：

```bash
pip install -r requirements-optional.txt
python -m tools.symbolic_check
python -m tools.build_data
python -m tools.browser_check
python -m tools.verify
```

Chromium 脚本默认使用 `/usr/bin/chromium`，需修改为机器实际路径。可直接用浏览器打开 `web/index.html`，完全不依赖网络，也无需帐号。

## 科学与数值风险说明

- **G=6.67430e-11 是外部输入。** 任何数值结果都不是从 c 独立预测 G。
- B=B0 cosωt 的均匀磁场是**有限观测区域准静态近似**，需要实际源电流和边界实现，不能被当作完整的 Maxwell 精确装置解。
- `ωa/c` 明显小于1是使用该准静态式的必要条件之一。网页以0.1作为示意标识阈值，不是严格误差上界。
- `monopole_g` 只适用于**真实净输入能量**。不可将场从电源转移出的能量反复加到封闭系统质量。
- `quadrupole_strain_scale` 是**未定义完整四极源的数量级表达式**，不等于理论预测；其远场公式对距装置10m、f=50Hz无效。
- 轴子响应是任意参数的玩具振子，不是已发现轴子，也不是 G 的新理论。
- 实验结果要求独立盲测、屏蔽、负对照和参考文献中的零结果约束。
- 自动测试证明所选公式/实现一致；不是验证自然界存在新增相互作用。

## 本轮关键方程

\[
T^{00}=u,\quad T^{0i}=S_i/c,\quad T^{ij}=u\delta_{ij}-\epsilon_0E_iE_j-B_iB_j/\mu_0.
\]

\[
\frac{\langle U_E\rangle}{\langle U_B\rangle}=\frac{1}{10}(\omega a/c)^2.
\]

\[
\mathcal L_{a\gamma}=-(g_{a\gamma}/4)\,aF\widetilde F,
\qquad F(a)=F_0+\xi a^2.
\]

当 \(a(t)=a_0+A\cos\omega t\)，\(F(a)\)的一次谐波系数为\(2\xi a_0A\)，二次谐波系数为\(\xi A^2/2\)；零背景\(a_0=0\)时一次谐波消失。这是**特定候选耦合**的数学结论，非实验证明。

## 可核对文献

参考 `SOURCES.md`。NIST/CODATA 2022常数、2024稳态电磁—引力实验零结果、经典EM能动张量与轴子电动力学都是已有公开研究。2026 CODATA调整尚未发布，不能虚构成最新G。
