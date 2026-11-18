# ROOT V74｜全链路科研审计与可证伪模型

## 科学状态

**未证明四力统一，未独立预测 G，未发现新相互作用。** 本项目完成的是企业级研究工程与审计：推导、独立计算、反例、模型边界、实验约束及可复现交付。

## 交付结构

- `book/ROOT_V74_统一场论第一性原理_严格证明审计与新突破路线.md`：完整研究报告。
- `rootv74/physics.py`：螺旋曲率、Schwarzschild 曲率不变量、Yukawa 均匀/分层球、SM 规范异常、耦合运行、量纲嬗变等。
- `tests/test_physics.py`：实际运行的 55 个自动测试，包括独立数值积分。
- `run_experiments.py`：独立生成 6 个 CSV、4 张图、`results/numerical_summary.json`。
- `web/index.html`：零外部依赖的离线交互实验室，支持三维螺旋、星体参考模型、有限球新力形状及理论状态。
- `data/ROOT_V74_方程索引.csv`、`data/ROOT_V74_方法审计矩阵.csv`：核心公式与条件、方法与失败标准。
- `results/verification_report.json` 和 `SHA256_MANIFEST.csv`：验收信息和哈希。
- `SOURCES.md`, `PROOF_STATUS.md`：来源和证明责任。

## 开箱使用

Python >=3.10。完整单元测试含一个 SciPy 独立积分交叉核验，需先安装 SciPy：

```bash
python run_tests.py
```

图表和批量数据还需要 `numpy` + `matplotlib`：

```bash
python -m pip install numpy matplotlib scipy
python run_experiments.py
python run_tests.py
```

> 提示：当前自动测试集的独立积分测试依赖 SciPy；未安装 SciPy 时请先安装，不能把缺失依赖声称为测试通过。

网页使用浏览器打开 `web/index.html`。没有网络请求和第三方 JS CDN。

## 必须注意

- 重力常数 `G_EXP` 来自 CODATA 2022，是外部实验输入，绝不是 ROOT 预测。
- 天体参考值采用球形/非旋转近似；白矮星和中子星数据是**假设代表参数**。
- 新力计算 α=1 仅为几何对照；与真实观测兼容性另需限制。
- `Z/A` 只是人为代理源荷；MICROSCOPE 的约束演示不能冒充特定新力的正式排除图。
- 任何理论性结论都必须先看 `PROOF_STATUS.md`。
