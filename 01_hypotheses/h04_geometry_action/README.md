# H04_GEOMETRY_ACTION · 几何与作用量

研究问题：给定几何结构与作用量，能否一致导出动力学和已知极限？

状态：进行中（已迁入 `D0_作用量变分求导`）。下列结论需在 `06_audit` 完成误差预算后方可称「已验证」。

## 全链路导航

- [0：假设与边界](00_assumptions/README.md)
- [1：数学定义与量纲](01_definitions/README.md)
- [2：方程推导（求导 D）](02_derivations/README.md) — 含 `D0_作用量变分求导/`
- [3：数学证明与一致性（证明 P）](03_proofs/README.md)
- [4：可区分预测](04_predictions/README.md)
- [5：复现与实验对照（验证 V）](05_verification/README.md)
- [6：误差预算与诚实分层（精算 A）](06_audit/README.md)
- [7：反例与证伪](07_falsification/README.md)
- [8：结论与未解问题](08_conclusions/README.md)

[候选资料索引](sources.md) · [跨体系比较](../../02_comparison/README.md) · [研究记录模板](../../03_research_protocol/claim_template.md)

## 关键结论（待审计）

- 统一场论是「单一变分原理的求导」：Einstein 场方程、Yang-Mills 方程、Higgs 质量矩阵、大统一力方程都是某作用量的 Euler-Lagrange 方程。
- `δS/δg` 偏差已达机器精度级（≈ 9.85e-13）。
