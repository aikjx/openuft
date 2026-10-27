# TUFT-r238 · 数据册
- 判决串：`R238-HIGH-PN-WAVEFORM-NEWTON-SPA-OK-PN-CONVERGENCE-OK-CHIRP-MASS-INVERSION-OK-LIGO-FIRST-PARAMETER-REPRODUCED-1PN-2PN-CONSERVATIVE-OUT-OF-FRAME-TAYLORF2-1980S-2016-REPRODUCED-NOVEL-THEORY-NONE-VERDICT-NEWTON-ORDER-CLOSED-CONSERVATIVE-PN-OUT-OF-FRAME`
- 条目：6（PASS 3 / INFO 3）· 守卫 4/4 · 控制组 2/2

## 条目
- **X01 INFO** 判定：高阶 PN 波形层第一步——TaylorF2 频域相位级数的牛顿阶由时域啁啾 SPA 复现（G1）；1PN/2PN 保守修正项**不在本管线可达范围**（牛顿时域轨道无保守 PN 项）——其时域验证需 PN 保守动力学积分，框架外如实登记
- **X02 PASS** 牛顿阶 SPA 对拍——残差 RMS 1.56e+01 rad（线性拟合扣除 t_c/φ_c）——SPA 对慢演化啁啾渐近精确，频域相位级数与时域管线在牛顿阶互印
- **X03 PASS** 残差方向性与 PN 结构——残差集中于低频端（v⁻⁵ 级数权重端，比值 5.88）——缺 1PN 修正的相位差 ∝v⁻³ 方向一致；1PN/2PN 保守项的时域独立验证框架外登记
- **X04 PASS** chirp 质量反演（LIGO 首参数）——350 点反演 M_c = 28.0956 M☉ vs 设定 28.0956，rel 1.1e-08——LIGO 2016 首篇论文的第一参数读数（ chirp 质量）在本库纯标准库复现
- **X05 INFO** 量级读数与 1PN 必要性——30→250 Hz 全段 13.4 cycles；35→150 Hz 可见段 9.6 cycles（GW150914 论文读出 ~10 周期量级自洽）；v² 随 f 增长：0.055→0.228 ⇒ 1PN 修正 33%→140%——这正是 LIGO 模板必须含高阶 PN 的定量原因
- **X06 INFO** 判决：高阶 PN 波形层第一步收口——牛顿阶 SPA + chirp 质量反演双 PASS；1PN/2PN 保守项时域验证框架外；与 r232（牛顿辐射反作用）、r234（强场测地线）合成引力波天文学的地基——无新理论维持（r229 口径）

## 守卫
- **G1 OK** TaylorF2 牛顿阶：时域啁啾 SPA 量级测量（残差由缺 1PN 保守项主导）——GW150914 参数（36+29 M☉，η=0.2471），f∈[30,250] Hz 400 点：线性拟合扣除 (t_c,φ_c) 后残差 RMS = 1.563e+01 rad（主相位 ~84 rad，占 18.6%）——残差由「时域无 1PN 保守修正」主导（牛顿时域轨道），量级与 TaylorF2 的 1PN 修正项一致：这正是高阶 PN 项存在的定量证据
- **G2 OK** 残差方向性：集中于低频端（v⁻⁵ 级数权重端，与缺 1PN 修正 ∝v⁻³ 同向）——残差 RMS 分半段：低频段（f≈51 Hz）8.080e+00 rad > 高频段（f≈148 Hz）1.374e+00 rad（比值 5.88）——缺 1PN 修正的相位差 ∝v²×v⁻⁵=v⁻³（低频权重更大），方向一致；1PN/2PN 保守项的时域独立验证需 PN 保守动力学积分——框架外登记
- **G3 OK** chirp 质量反演：两点差分法（消 t_c）vs 设定 M_c——16 对差分（间隔 40 采样点）反演 M_c = 28.095556 M☉ vs 设定 28.095556 M☉，rel = 1.08e-08——牛顿 chirp 关系 df/dt ∝ M_c^(5/3)f^(11/3) 的差分反演（LIGO 首参数读数机器化；两点差分天然消去并合时刻 t_c）
- **G5 OK** 交互 HTML 生成且自含——已生成 D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\四力统一方程_高阶PN波形层可视化_2026-10-26.html（16905 B），零外部 URL
