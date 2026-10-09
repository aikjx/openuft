# TUFT V3.5 分支①修复版 · 独立再验收（机器产物）

- 生成时间：2026-10-05 00:59:28
- 条目 5 ｜ PASS 4 ｜ FAIL 0 ｜ BOUNDARY 1 ｜ INFO 0 ｜ 自检 7 / 7
- F-03：实际 field() vs 理论 F=−∇(κ+τ) 交叉相似度 1.0000（≥0.95 ⇒ V-07 已修）
- 判据信息量：旧径向场被拒 0.2357（<0.95）
- F-04：判据已改交叉比对（自比弃用）⇒ V-08 已修
- 方法论：验收册引擎用硬编码旧版 sut_field（自指涉），直接重跑不能验证修复

## 条目

| ID | 节 | 条目 | 判定 | 摘要 |
|---|---|---|---|---|
| A-01 | 实际SUT读取 | 从实际 SUT 抽取 field() | PASS | exec 实际源码中的 field 定义；抽取成功，样本点实际调用 field()（非复刻） |
| B-01 | F-03 交叉比对 | 实际 field() vs 理论目标 | PASS | 交叉相似度（6 点）1.0000 ≥ 0.95 ⇒ 实际代码与其声称的 E∝(κ+τ) 一致（F-03 修复确认） |
| B-02 | F-03 交叉比对 | 旧缺陷径向场被拒 | PASS | 同判据对旧场：0.2357 < 0.95 ⇒ 判据非零信息（能区分正确场与旧缺陷场） |
| C-01 | F-04 判据核验 | V-08 判据改为交叉比对 | PASS | 读取实际 SUT 源码：E-02 判据=交叉相似度；旧 ok_render=sim_self 判据行已移除 ⇒ V-08 已修 |
| D-01 | 方法论盲区 | 验收册引擎自指涉盲区 | BOUNDARY | 复刻旧版 sut_field：验收册用自己的硬编码 sut_field(径向) 做 V-07/V-08 计算（确认为硬编码旧版），AST 只查函数名 ⇒ 直接重跑它无法确认 F-03/F-04 是否已修，必须改读实际 SUT（本册即此做法） |

## 自检

| 基线 | 结果 | 取证 |
|---|---|---|
| sut_has_field | PASS | SUT 含 1 个 field 定义（1） |
| F03_fixed_uniform | PASS | 实际 field() 输出单一方向 [(-0.707107, -0.707107)]（均匀场） |
| F03_cross_matches_theory | PASS | 实际 field() 与理论 F=−∇(κ+τ) 交叉余弦相似度 = 1.0000 ≥ 0.95 ⇒ V-07 已修 |
| F03_rejects_old | PASS | 旧缺陷径向场交叉相似度 = 0.2357 < 0.95 ⇒ 判据有信息量（能区分） |
| F04_uses_cross | PASS | SUT E-02 判据使用交叉比对（sim_cross / target_field） |
| F04_no_self_criterion | PASS | SUT 不再用 ok_render=sim_self 当判据（自比已弃用） |
| audit_engine_self_referential | PASS | 验收册引擎含硬编码旧版 sut_field ⇒ 自指涉，重跑不能验证修复 |
