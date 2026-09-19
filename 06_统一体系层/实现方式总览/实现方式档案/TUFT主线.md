# 实现方式档案：TUFT 主线 v2–v18

[实现方式总览](../README.md) · 归属体系：[s14 挠率统一场论 TUFT](../../../01_独立体系/S14_挠率统一场论TUFT/README.md)

- **形态**：M1 符号推导 · M2 数值精算 · M3 谱方法与打靶 · M6 书稿
- **位置**：仓库根 `tuft_v*.py`、`tuft_v*_out.txt`、`TUFT_*.md`、`_ma_v*_*.py`
- **状态**：active，主线在研

## 主线做了什么

以 `v_total=c` 为唯一公设，把曲率 K 与挠率 T 作为几何两分量，主张挠率内禀代数承载 U(1)×SU(2)×SU(3)。版本线 v2（2026-09-16）至 v18（2026-09-18，在研），每期配 `_out.txt` 运行报告与独立审计裁决文档。

工作流编号说明：`line1/line2/line3` 是**每期内部重排**的编号，不是固定的三条推论链。真正连续的主轴是 line1（强场与 QNM）。

## 关键转折

- v6 用 WKB 估谱 → v7 首试 Leaver 连续分数法
- v9–v12 转向"先证明引擎能复现已知答案"：GR Schwarzschild QNM 标量/引力双通道达 13–15 位（`tuft_v12_line1_rw_out.txt`，GATE: PASS）
- v13/v14 双向打靶找 TUFT 壁谱，**两次均被证明在 GR 上就不收敛**
- v15 范式转换：放弃复极点，改走实频散射相位
- v16 发现 |R_TUFT|²≡1，所谓"0.90 反射峰"不存在
- v17 坐标纠错：odd 势必须用面积半径 R=ρ√B，结论翻转为"外垒与 GR 几乎相同，差异只在内边界"

## 诚实评级

**算过且站得住**：GR QNM 双通道 13–15 位复现；`|R_TUFT|²−1 ≤ 4.4e−16` 全频；无高 Q 壁腔窄谱；几何壁垒 r_h=0.6099/0.7071M、ISCO 4.9491M、b_crit 5.1928M。

**已推翻或勘误（23 条）**：C_k 三代、"Leaver PASS"（实为查表冒充）、2L 几何回波、v13 六个壁频、v14 两个外推根、0.90 Lorentzian 反射率峰、E399/E400 隧穿率（坐标错）、Hz 换算漏 2π。

**仍 OPEN**：TUFT 反射壁渐近复谱（连续五期未闭合）、回波模板 SNR、C18 可观测性——v17 后已从"TUFT 独有"降级为 ECO 通用判据。

**常数预言：没有。** α 在 v2 规格中为外部标定输入，主册明写"几何给不了 1/137"。三代质量与 mass hierarchy 双否决。

## 与体系的关系

本档案是 s14 的**主力实现**。s14 的 `claims.csv` 已登记多项 falsified，与本档案一致。两者不可互提证据等级。

## 建议保留的核心文件

`TUFT_企业级归一化主册_v1.0.md`（SSOT）、`TUFT_归一化台账_v1.0.json`、`TUFT_v2.0_企业级规格.md`、`tuft_v2_verify.py`、`tuft_v4_line2_geodesic.py`、`tuft_v7_line2_c_deriv.py`、`tuft_v9_line1_leaver.py`、`tuft_v10_line1_scalar.py`、`tuft_v12_line1_rw.py`、`tuft_v13/v14_tuft_wall.py`（负面结果存档）、`tuft_v16_gr_reflection.py`、`tuft_v17_odd_potential.py`、`_ma_v13/v14/v16/v17_*`（审计代码）。

调试产物（`_diag_*.py`、`_probe_v14*.py`、`_proto_*.py`、`_ricc*.py` 等）建议归档，其数字禁止引用。
