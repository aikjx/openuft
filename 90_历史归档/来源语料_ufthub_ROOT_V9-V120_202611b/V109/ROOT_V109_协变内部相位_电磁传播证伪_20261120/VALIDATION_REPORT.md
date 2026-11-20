# ROOT V109｜科学与工程验收记录

验收日期：2026-11-20。**本报告仅认证程序和限定模型计算，不认证新物理。**

## 已实际运行的测试

- V109 Python：`python run_all.py` -> **89 项 pytest 全部通过**。
- V109 符号/自然单位量纲：`src/symbolic_audit.py` -> **10/10 为真**。
- 两种独立数值积分器：SciPy DOP853 复数 ODE 与不依赖 SciPy ODE 的实分量 RK4，10 项交叉/控制测试包含于 89 项中，全部通过。
- Chromium：`python web/browser_smoke.py` -> **11 项页面实际检查通过**，并生成 `figures/05_CHROMIUM_ACTUAL_SCREENSHOT.png`。
- V108 原始科研 ZIP：独立解压至外部临时目录后 `python -m pytest -q tests/test_v108.py`，**124 项通过**。这是历史软件回归，不等于 V108 的 396 项科学目标被完成。
- 历史台账：396 行且 canonical_id 396 个唯一；新项目保留原始每项 acceptance 和 prior_status，另放 12 条新任务。

## 核心数值核对

- benchmark θ=.4 sin(.7t)、λ=.08、T=5：WKB 旋转角约 -0.005612531643 rad。
- 在 k=20：直接 A 模式相位轴约 -0.005614176952 rad；E 模式相位轴约 -0.005610888 rad。
- 在 k=80：A 模式相位轴约 -0.005612640323 rad，逐步逼近 WKB。
- 非绝热案例 k=.8、λ=.35、θ=sin t、T=2.5：完整 A 相位轴约 +0.236577 rad；WKB 约 +0.104733 rad，体现近似适用边界。
- θ 完整周期返回：WKB 端点差 0，有限 k=1 时模式相位代理非零（不是实验偏振读数）。
- 单测量 λ 与 Δθ 的线性雅可比：秩 1，存在精确零方向。
- 已做同一 HTML 的实际浏览器点击/滑块测试；其 JS RK4 与 Python 的 DOP853 非相同实现。

## 必须谨慎的独立性层次

- 物理公式：采用公开成熟的 axion-like electrodynamics，非 ROOT 新定律。
- 数学证明：在明确假设的作用量和模型内成立，非标准模型与引力的最终统一。
- 数值结果：仅用于模型计算；没有新实验样本。
- 来源引用：文献结论须附带假设，不能把 g_{aγ} 的 GeV⁻¹ 界直接用于无量纲 λ。

## 归档与独立验收

最终 ZIP 的文件计数、SHA-256 校验、独立解压、重新计算与完整回归以 `CHECKSUMS.sha256`、`MANIFEST.json` 和最终终端运行记录为准。`python verify_integrity.py` 不读取任何外部服务。
