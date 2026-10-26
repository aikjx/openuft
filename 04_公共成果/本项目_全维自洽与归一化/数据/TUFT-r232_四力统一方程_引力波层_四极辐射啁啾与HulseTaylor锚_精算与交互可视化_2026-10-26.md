# TUFT-r232 · 数据册（引擎自动生成）
- 判决串：`R232-GW-LAYER-QUADRUPOLE-NUMERICAL-OK-HULSE-TAYLOR-ANCHOR-OK-CHIRP-INTEGRATION-OK-LIGO-STRAIN-SCALE-OK-UPCHIRP-SIGNATURE-OK-EINSTEIN-1918-REPRODUCED-NOVEL-THEORY-NONE-VERDICT-CLASSICAL-GRAVITY-THREE-LAYERS-CLOSED-ESSENCE-OPEN`
- 条目：6（PASS 3 / FAIL 0 / BOUNDARY 0 / INFO 3）· 守卫 5/5 · 控制组 2/2

## 条目
- **W01 INFO** 判定：引力波层 = 几何化的动力学验证——四极公式（Einstein 1918）+ Ṗb（Taylor–Weisberg 1982）+ 啁啾闭式全部为教科书内容；本卷三条独立管线互印（数值差分/公式对观测锚/ODE 对闭式）——复现层，无新理论（承 r229/r230）
- **W02 PASS** 四极功率恒等——圆双星 Q_ij(t) 数值三阶差分 ⟨Q̈⃛²⟩ → P_num vs 解析 P_ana：rel 1e−6 级——四极辐射的微分内核被数值端独立复现
- **W03 PASS** Hulse–Taylor 锚（Nobel 1993）——Ṗb 计算 -2.403e-12 vs 观测 -2.418e-12 s/s，rel 0.65%——差额即银河系加速度修正（修正后 0.13%）；Peters da/dt = -3.53 m/yr 与文献 3.5 一致；Kepler 关系互拍 rel 1.3e-14
- **W04 PASS** 啁啾积分与 LIGO 应变量级——36+29 M☉：41.3→116.9 Hz 扫频耗时 0.11 s（GW150914 同频段 ~0.2 s 自洽；t_merge rel 2.2e-11）；末端应变 h = 1.80e-21 ≈ GW150914 峰值量级——波形的时间-频率-振幅三要素在纯标准库内自洽
- **W05 INFO** 升频标志与判别力——chirp 单调升频（C2 阴性守卫）；F(e) 椭圆修正因子 3 倍级变化被解析对拍（C1）——管线对波形形态与偏心率有判别力
- **W06 INFO** 判决：引力波层收口——经典引力三层（牛顿 1/r² → 1PN 几何化唯象 → 四极辐射/啁啾）全部机器复现；「本质」之问维持 r230 判定：场方程/量子化/等级起源在框架外或人类边界——引力波层不改变「无新理论」判定，但把几何化的动力学证据补齐

## 守卫
- **G1 OK** 四极功率恒等：数值三阶差分 ⟨Q̈⃛²⟩ vs Einstein 解析 (32/5)G⁴μ²M³/(c⁵a⁵)——圆双星（等质量 1 M☉，a=3e6 m，2 周期 8192 点，中心 5 点三阶差分）：P_num = 1.341989e+37 W vs P_ana = 1.341995e+37 W，rel = 4.707e-06——四极公式（Einstein 1918）的微分内核被数值端独立复现（非解析代入）
- **G2 OK** Hulse–Taylor 锚：Ṗb 公式 vs 观测（Nobel 1993 间接验证机器复现）——Ṗb（M_c=1.2309 M☉ 以 M☉ 计配套 T☉——kg 代入差 50 量级为本轮自抓教训）：计算 -2.4027e-12 s/s vs 观测 -2.4184e-12，rel = 0.65%（差额=著名银河系加速度修正，修正后 0.13%）；Peters da/dt 完整式 = -1.1188e-07 m/s = -3.531 m/yr（文献 3.5），与 Ṗ 的 Kepler 互拍 rel = 1.26e-14
- **G3 OK** 啁啾积分：da/dt RK4（Richardson 外推） vs 闭式，中途 a(t) 逐点对拍——GW150914 参数（36+29 M☉）：a₀=8e5 m（f=41.32 Hz）积分到 a_min=4e5 m，双步长 Richardson 外推 + 末步穿越插值：t_merge 数值 = 0.114487208 s vs 闭式 0.114487208 s，rel = 2.23e-11；中途逐点 a(t) 对拍闭式 (a₀⁴−t/COEF_T)^{1/4}：max rel = 4.52e-12（400 点）——啁啾演化（LIGO 波形的时间-频率骨架）数值与闭式互印
- **G4 OK** LIGO 应变量级：h(M_c=28.1 M☉, D=410 Mpc, f_end) ≈ 1e−21——啁啾末端应变 h = 1.799e-21（M_c = 28.1 M☉，D = 410 Mpc）——GW150914 峰值应变 ~1e−21 量级锚（LIGO 2016 首次直接探测读数）：波形振幅公式的量级自洽
- **G5 OK** 交互 HTML 生成且自含——已生成 D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\四力统一方程_引力波层可视化_2026-10-26.html（26036 B），零外部 URL、JSON 已铸入

## 控制组
- **C1 OK** 判别力：F(e) 修正因子对偏心率敏感——F(0.617)/F(0.1) = 11.109（数值）vs 解析 11.109——椭圆修正因子 3 倍级变化被机器解析对拍：Ṗb 管线对偏心率有判别力
- **C2 OK** 阴性对照：升频标志（chirp 必升频，降频波形必被判红）——f 从 41.32 Hz 单调升到 116.86 Hz——引力波升频是 LIGO 波形的标志特征；若数值管线给出降频（如符号约定错），C2 立刻失败
