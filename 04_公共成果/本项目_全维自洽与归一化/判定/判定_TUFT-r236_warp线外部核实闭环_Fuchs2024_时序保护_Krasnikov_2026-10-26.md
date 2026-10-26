# 判定_TUFT-r236 · warp-drive 线（r64–r67）外部核实闭环：Fuchs 2024 / 时序保护 / Krasnikov

- 日期：2026-10-26
- 引擎：`源码/TUFT-r236_warp线外部核实闭环_Fuchs2024_时序保护_Krasnikov_2026-10-26.py`
- 产物：`数据/TUFT-r236_warp线外部核实闭环_Fuchs2024_时序保护_Krasnikov_2026-10-26.{json,md,_report.txt}`
- 承接：r64 判定册 §零之二 之后登记的 **F01 / F02 / F03 三条 BOUNDARY**（离线不可核实项）
- ★改号：原稿号 **r200 已被并行会话《三维螺旋时空方程》（2026-10-25 落盘）占用** ⇒ 按「先占位者为权威 / 后到者整体改号」纪律整体改 **r236**（实测 r235 已由并行链双占、r24x 全空）
- 条目 **10**（PASS 1 / CORRECTED 4 / MISMATCH 1 / BOUNDARY 1 / INFO 3）；守卫 **10/10**；退出码 **0**；纯标准库

---

## 〇 · 一页纸结论（承重裁定）

1. **F01（Fuchs 2024）确证为真** —— Jared Fuchs 等 6 人《Constant Velocity Physical Warp Drive Solution》，arXiv:2405.02709，Class. Quantum Grav. **41, 095013 (2024)**，DOI 10.1088/1361-6382/ad26aa。摘要原文确为「constant-velocity **subluminal** warp drive that **satisfies all of the energy conditions**」，构造 = **稳定物质壳 + 位移矢量分布**（并自证「shift vector 不能退化为坐标变换」）。⇒ 来稿钥匙 2 的引用为真，r64 F01 从 BOUNDARY 升级 **PASS**。
2. **★承重：F03 是归属错误，不是结论错误** —— 来稿写「Krasnikov：负能壳半经典不稳定」。但 Krasnikov 关于曲速的原始论文是《The quantum inequalities **do not forbid** spacetime shortcuts》（Phys. Rev. D **67, 104013 (2003)**，arXiv:gr-qc/0207057）——它是**许可向**的（QI 不禁止 Alcubierre 泡 / Krasnikov 管 / 虫洞）。半经典不稳定性的正确归属是 **Finazzi–Liberati–Barceló**（J. Phys. Conf. Ser. **222, 012046 (2010)**；229, 012018 (2010)）。⇒ 来稿钥匙 4 的结论方向仍成立，但**引用必须更正**。
3. **「2026 正能量解」确证存在，但方向是收紧** —— An T. Le 三篇（arXiv:**2602.18023** 观测者鲁棒能量条件验证 / **2605.25417** 源一致壳层边界代价 / **2606.22531** 辐射转向）的净结论是：Euler 单观测者分析**不完整**（WEC 须对全部观测者检验，S-lemma 化为 4×4 LMI）；**八个经典正能量构造的违背集中在源-真空过渡边界**；满足曲面 DEC 的转向受 **m_f/m_i = exp(−3L)** 指数燃料界。⇒ 来稿把 2026 文献当作钥匙 2 的加强证据，属**引用方向误读**。
4. **r64 D01 被外部文献独立确证** —— r64 曾判 BOUNDARY 的「取 Euler 法向 u=n 即违反 WEC 需限定类时性」这一口径缺陷，在 Le 2602.18023 中被严格形式化（全部观测者 LMI 判据 + 动量-涡量约束定理）。⇒ r64 D01 从 BOUNDARY 升级为「已被外部文献独立支持」。
5. **F02 措辞降级确证** —— 时序保护已有**构型级双向结果**：Everett & Roman（Phys. Rev. D 56, 2100 (1997)）双超光速泡 CTC 判据 u > 2v/(1+v²)；Sajeendran & Ralph（arXiv:2407.18993）受控旋转 Alcubierre 时空 CTC 构造；Kerr–Sen 类时空 CPC 再检验（EPJC 85, 270 (2025)）。「完全未攻破」确属过度陈述。

**净立场**：外部核实**加强而非削弱** r64–r67 四册结论；对四册**零更正**，对来稿**一处实质更正**（V05 Krasnikov 归属）。warp-drive 线至此无未闭环的外部核实项。

---

## 一 · 方法、纪律与文献登记表

**方法**：外部检索（arXiv / DOI / 期刊卷页三源核对），逐条引用必须带可复核 ID；流行科学转述数字（「72% 漏检」）单独登记 BOUNDARY，不作文献读数。

**纪律**（承接 r64/r66）：
1. 量纲工具自身先过 guard 再用于判定；
2. 「恒为负」类裁定必须配阳性对照；
3. 引用必须可复核（arXiv 号 / DOI / 期刊卷页），不可复核的标 BOUNDARY；
4. 流行转述数字不算文献读数；
5. 外部核实可确认、收紧或推翻来稿——三者都记账，不预设方向。

**文献登记表**（全部 11 条，含机器校验）：

| key | 文献 | arXiv | 期刊 | DOI |
|---|---|---|---|---|
| FUCHS2024 | Constant Velocity Physical Warp Drive Solution（Fuchs 等 6 人） | 2405.02709 | CQG 41, 095013 (2024) | 10.1088/1361-6382/ad26aa |
| LE2602 | Observer-robust energy condition verification for warp drive spacetimes（An T. Le） | 2602.18023 | preprint 46p | 10.48550/arXiv.2602.18023 |
| LE2605 | On the boundary cost of source-consistent warp shells（An T. Le） | 2605.25417 | preprint | 10.48550/arXiv.2605.25417 |
| LE2606 | Radiative steering of warp shells（An T. Le） | 2606.22531 | preprint 39p | 10.48550/arXiv.2606.22531 |
| FINAZZI2010 | Superluminal warp drives are semiclassically unstable（Finazzi/Liberati/Barceló） | — | JPCS 222, 012046 (2010) | 10.1088/1742-6596/222/1/012046 |
| FINAZZI2010B | Semiclassical instability of warp drives（同作者） | — | JPCS 229, 012018 (2010) | 10.1088/1742-6596/229/1/012018 |
| BARcELO2010 | On the Impossibility of Superluminal Travel: The Warp Drive Lesson | 1001.4960 | preprint 9p | 10.48550/arXiv.1001.4960 |
| KRASNIKOV2003 | The quantum inequalities **do not forbid** spacetime shortcuts | gr-qc/0207057 | PRD 67, 104013 (2003) | 10.1103/PhysRevD.67.104013 |
| EVERETT1997 | Superluminal subway: The Krasnikov tube（Everett & Roman） | — | PRD 56, 2100 (1997) | 10.1103/PhysRevD.56.2100 |
| SAJEENDRAN2025 | Looping back to the past through free fall in a controlled warp drive spacetime | 2407.18993 | preprint v2 | 10.48550/arXiv.2407.18993 |
| KERRSEN2025 | Revisiting chronology protection conjecture in the Dyonic Kerr–Sen black hole spacetime | 2408.06023 | EPJC 85, 270 (2025) | 10.1140/epjc/s10052-025-13935-2 |

---

## 二 · V 组逐条裁定

### V01 · PASS —— Fuchs 2024 引用确证

来稿钥匙 2 所引文献真实存在且描述准确：摘要原文逐条对照——
(1)「constant-velocity **subluminal** warp drive」= 来稿「v_s<c」✓；
(2)「satisfies **all of the energy conditions**」= 来稿「满足能量条件」✓；
(3)「stable matter shell + shift vector distribution」⇒ **正能量解不是 Alcubierre 型泡**，与 **r64 D02 的机器预测一致**（r64 D02 已证 §四 的 ρ 式恒负、不可能给出正能量泡，故钥匙 2 必属不同度规族）；
(4)「positive ADM mass」⇒ 正能量属性确认；
(5)「shift vector cannot be reduced to a coordinate transformation」⇒ 作者自设的反规避条款。
⇒ r64 F01 升级 PASS。**但这只确认「存在亚光速正能量解」，不确认「已攻破超光速」**（见 V07）。

### V02 · CORRECTED —— 「2026 正能量解」方向误读

来稿写「Fuchs 2024 **及 2026 正能量解**」。2026 年文献确有三篇（An T. Le），但净方向是**收紧**：(i) Le 2602.18023 证明 Euler 单观测者分析不完整（能量条件须对全部观测者，S-lemma 4×4 LMI；动量约束：动量恒为零 ⇔ 位移矢量 = 梯度场 + 刚体转动）；(ii) Le 2605.25417 对**八个经典构造**的完整测试显示违背**集中在源-真空过渡边界**（正能量宣称在边界处失效）；(iii) Le 2606.22531 的转向燃料界 exp(−3L)。⇒ 来稿把 2026 文献当作钥匙 2 的加强证据，属引用方向误读。

### V03 · CORRECTED —— r64 D01 被独立确证

r64 D01 的边界裁定（Euler 法向的类时性限定）在 Le 2602.18023 中被**独立形式化并加强**：「Whether a warp drive metric requires exotic matter is decided by energy conditions quantified over **all observers**, not only the Eulerian」。⇒ r64 D01 从 BOUNDARY 升级为「已被外部文献独立支持」——r64 凭量纲与逻辑指出的口径缺陷，在文献侧有对应的严格化工具（Warpax）。附带互证：r64 A03 用物理判据唯一选出 ρ ~ v_s²，Le 2602.18023 证明 Euler 负能积分 ∝ v²，**两条独立路径同一指数**。来稿 §四 的 WEC 论证按 2026 标准属**不完整检验**（结论方向仍成立：负能密度对任何观测者都违反 WEC）。

### V04 · CORRECTED —— F02 措辞降级确证

构型级双向结果全部确证（Everett-Roman CTC 判据 / Sajeendran-Ralph CTC 构造 / Kerr–Sen CPC 再检验）。机器扫描 CTC 判据 u > 2v/(1+v²)：**v=1 处阈值恰为 1（阳性对照）；v>1 时阈值全部 < 1** ⇒ 两个超光速泡只需**亚光速**的相对速度即可互相生成 CTC——这把「时序风险」从边缘情形变成结构性质。措辞应改为「未完全证明，且已有构型级双向结果」。

### V05 · CORRECTED（本册承重）—— Krasnikov 归属错误

见 §〇 第 2 条。极性机检（G3）：Krasnikov 标题含 "do not forbid"（许可向），Finazzi 标题含 "unstable"（限制向）⇒ 检测器有判别力。更微妙的一层：**「量子不等式」与「半经典稳定性」是两道彼此独立的关卡**——QI 不禁止（Krasnikov）不等于半经典稳定（Finazzi）；来稿把两者混为一条「钥匙 4」，属本库「不同机制并账」缺陷族的又一实例。

### V06 · INFO —— 燃料界机器扫描

m_f/m_i = exp(−3L)：L=0.1 → 0.741；0.5 → 0.223；**1 → 0.0498**；2 → 0.00248；3 → 1.23e−4；5 → 2.86e−7。⇒ 即使满足曲面 DEC，改变速度的代价是指数级的；自相似壳层还需各向异性应力且带增长的法向模态（稳定性隐患）。该文自留开放项：转弯后的自引力沉降未解决。

### V07 · MISMATCH —— 来稿「钥匙 2 纸上已攻破」推论过度

三处：(1) **范围**——Fuchs 2024 与 Le 2026 全部正能量结果都限于**亚光速**，无任何正能量解达到 v_s ≥ c；(2) **边界违背**——Le 2605.25417 显示八个构造的违背集中在源-真空边界，「正能量壳层」在边界处并不正能量；(3) **可控性**——exp(−3L) 燃料界 + Bobrick-Martire 早已指出曲速泡「没有任何自然方式改变速度」。正确记账：钥匙 2 = 「亚光速正能量解确实存在」+「完整 EC 自洽性在 2026 年被发现在边界处失效」+「操控代价指数级」——三段式，不是「已攻破」。

### V08 · INFO —— 遗留项清零

r64 三条外部核实遗留项全部闭环：F01 → PASS（V01）；F02 → CORRECTED 且确证（V04）；F03 → CORRECTED 且归属纠错（V05）。

### V09 · BOUNDARY —— 流行数字「72%」不作文献读数

「Euler 分析漏检约 72% 泡壁 WEC 违反（Rodal 几何）」出自 freeastroscience.com 转述而非论文摘要。方向与 Le 2602.18023 定理一致，但具体数值需查论文正文。按 r66 纪律（比值/倍数读数必须先证来源），不用于任何判定。

### V10 · INFO —— 净立场（更新版，可引用）

> 超光速曲率引擎在 GR 内部结构性不可行：v_s>c 使泡内运动学失去实定义（r64 C01/C04）；唯一定义域内的 v_s→c⁻ 上，QEI 量纲闭合五族中四族被直接排除，仅存族要求壳厚锁死在 10 ℓ_P 内、宏观泡负能量跳到 10⁶ 倍可观测宇宙质量（r66/r67）；正能量路线（Fuchs 2024 / Le 2026）仅限亚光速，且 2026 年发现其能量条件违背集中在源-真空边界、转向代价按 exp(−3L) 指数燃烧；半经典不稳定性的正确文献归属是 Finazzi-Liberati-Barceló 2010（**非 Krasnikov**）。

---

## 三 · 机器读数与守卫清单

**守卫 10/10 全过**：G0-1/G0-2 量纲自检（[c²v_s²(f′)²/G] = 能量密度）· G1 Fuchs bibcode/期刊/arXiv 三源一致（2024CQGra..41i5013F ↔ CQG 41,095013 ↔ 2405.02709）· G2 全部 arXiv 号 YYMM 与论文年份一致（新旧格式）· G3 Krasnikov/Finazzi 极性检测器阳性对照 · G4 CTC 阈值（v=1 处 =1，v>1 全 <1）· G5 燃料界单调递减 · G6 全部文献带可复核 ID · G7 流行数字不 cited · G8 量纲守卫。

**关键机器读数**：
- Fuchs bibcode 解析：(2024, 'CQGra', '41', '5013') ↔ 期刊串 (2024, 41, '095013') ↔ arXiv (2024, 5) 三源一致；
- CTC 阈值：v=1 → 1.0；v=1.5 → 0.923；v=2 → 0.8；v=5 → 0.385；v=10 → 0.198；v=200 → 0.00998；
- 燃料界：L=1 → 4.978e−02；L=3 → 1.234e−04；
- 极性：Krasnikov permissive=True / Finazzi restrictive=True。

**自抓 5 处（已修）**：①V04 字符串格式化 `%` 优先级错误（只绑最后字面量组）——两轮修复后改显式分段；②bibcode 解析正则畸形字符类——重写；③Krasnikov 旧格式 arXiv 号 `gr-qc/0207057` 尾段 3 位数字，正则写严——放宽；④CTC 守卫把 v=1 边界行误纳入「全部 <1」——拆出边界阳性对照；⑤bibcode 卷页间小写限定字母 'i' 切断数字子串——先去小写再查。**其中 ①②③④⑤ 全部由守卫先行抓出（首跑 8/10、二跑 9/10、三跑 10/10）**，未带病落盘判定。

---

## 四 · 与 r64–r67 的接口

| r64 条目 | 原判定 | r236 外部核实后 |
|---|---|---|
| F01 Fuchs 2024 引用 | BOUNDARY | **升级 PASS**（V01） |
| D01 Euler 观测者口径 | BOUNDARY | **升级：被 Le 2602.18023 独立确证**（V03） |
| F02 时序保护措辞 | BOUNDARY（建议降级） | **降级确证**（V04） |
| F03 Krasnikov 归属 | BOUNDARY | **CORRECTED：归属错误，改为 Finazzi-Liberati-Barceló**（V05） |
| D02 正能量泡必非 Alcubierre 型 | FAIL（篇内互斥） | **被 Fuchs 构造独立确证**（V01 第 3 条） |
| A03 ρ ~ v_s² 唯一族 | CORRECTED | **与 Le 2602.18023 的 v² 缩放定理互证**（V03a） |
| C01/C04、C05/C05b、E07 | FAIL/FAIL/CORRECTED | 文献无争议，**继续有效** |

对 r65/r66/r67：零更正（r66 I03 对 r64 E03b 的撤回是量纲问题，与外部文献无关；r67 的五族全关针对 QEI 族，与外部两条文献线互不重叠）。

---

## 五 · 对来稿的更正清单（唯一实质更正）

1. **钥匙 4 引用**：「Krasnikov：负能壳半经典不稳定」⇒ 改为「**Finazzi–Liberati–Barceló 2010：超光速曲速泡半经典不稳定**（RSET 分析）」；如确要引 Krasnikov，则须按其原文写「**Krasnikov 2003：量子不等式不禁止时空捷径**（许可向）」。
2. **钥匙 2 状态词**：「✅ 纸上已攻破」⇒ 改为「**亚光速正能量解存在（Fuchs 2024）；完整能量条件自洽性在源-真空边界处失效（Le 2026）；操控代价指数级**」。
3. **钥匙 3 状态词**：「❌ 未攻破」⇒ 改为「**未完全证明，已有构型级双向结果**」（Everett-Roman / Sajeendran-Ralph / Kerr-Sen）。

---

## 六 · 遗留与待办

- [ ] V09：Le 2602.18023 正文中 Rodal 几何的逐点检验表（核实「72%」具体数值后才可引用）
- [ ] LE2606 的「转弯后自引力沉降」开放项（该文自留），若后续闭合可更新 V06 的燃料界解读
- [ ] LE2605 的「source-first shell ansatz」若给出通过全部五项测试的构造，则 V07 第 (2) 条须复审（当前为八构造全败）

---

## 七 · 复算方式

```
python -X utf8 源码\TUFT-r236_warp线外部核实闭环_Fuchs2024_时序保护_Krasnikov_2026-10-26.py
```

退出码 0；条目 10；守卫 10/10。纯标准库（re / json / decimal / fractions），无外部依赖。文献 ID 可逐条在 arXiv / DOI 解析核对。
