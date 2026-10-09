# TUFT V3.5修复版 · 验收引擎自指涉盲区回修（机器产物）

- 生成时间：2026-10-07 10:07:45
- 条目 8 ｜ PASS 4 ｜ FAIL 1 ｜ BOUNDARY 3 ｜ INFO 0 ｜ 自检 4 / 4
- V-07 交叉相似度（实际field vs 均匀场）：1.0000 ｜ V-08 自相似度：1.0000

## 条目

| ID | 节 | 条目 | 判定 | 摘要 |
|---|---|---|---|---|
| A-01 | 盲区确认 | 验收册引擎自建硬编码 sut_field | PASS | 验收册引擎含硬编码 sut_field（径向 −(1/r²)(x,y)），是自建复刻非实际 SUT 实现 |
| A-02 | 盲区确认 | AST 守卫只查函数名不查实现 | PASS | load_sut() 的 sut_has_verified_symbols 只核对函数名存在，不校验硬编码复刻与实际 SUT field() 实现一致 ⇒ 自指涉盲区确认 |
| B-01 | SUT 实抽 | AST 抽取 field/omega/region | PASS | 从实际 SUT 源码 AST 抽取并 exec：field=True, omega=True, region=True |
| C-01 | 重跑 V-07/V-08 | V-07 交叉比对（实际field vs 参考均匀场） | PASS | 实际 SUT 抽取 field() 与参考均匀场 −(1,1)/√2 余弦相似度 **1.0000** ⇒ （验收册硬编码径向 sut_field 得 0.1173 FAIL；实际实现为均匀场 ⇒ V-07 从 FAIL 转 PASS） |
| C-02 | 重跑 V-07/V-08 | V-08 自相似度判据 | FAIL | 自比 cos(field,field)=**1.0000** 恒 1 ⇒ **零信息判据仍失效**，必须替换为对参考场的交叉比对（本册 C-01 即其替代） |
| D-01 | 回修判定 | 盲区回修成立 | BOUNDARY | 验收册引擎的 sut_field 应改为**从实际 SUT AST 抽取 field() 并 exec**（本册 B/C 段即回修范式），重跑 V-07 得 1.0000（非硬编码 0.1173）；V-08 自比恒 1 判据须废弃、由交叉比对替代 |
| D-02 | 回修判定 | 修复建议（登记给验收册引擎） | BOUNDARY | ① load_sut() 增加按符号名的 AST 抽取 exec（替代 sut_field/sut_omega/sut_region 硬编码复刻）② V-08 自相似度判据删除，改为 V-07 交叉比对 ③ 抽取函数体须在独立命名空间 exec，避免整文件副作用 |
| D-03 | 回修判定 | 不修改 SUT / 验收册引擎 | BOUNDARY | 本册只验证回修范式可行，不改 SUT 也不改验收册引擎源码（并行编辑冲突规避）；修复建议待并入验收册引擎下一版 |

## 自检

| 基线 | 结果 | 取证 |
|---|---|---|
| blindspot_confirmed | PASS | 验收册引擎自指涉盲区成立（硬编码复刻 + AST 只查名） |
| sut_extracted | PASS | 实际 SUT 的 field/omega/region 均已 AST 抽取 |
| v07_cross_pass | PASS | 实际 field 是均匀场（V-07 交叉比对通过） |
| v08_invalid | PASS | V-08 自比恒 1，失效判据（须交叉比对替代） |
