# TUFT-r236_warp线外部核实闭环_Fuchs2024_时序保护_Krasnikov_2026-10-26

- 日期：2026-10-26
- 承接：r64 F01 / F02 / F03 三条 BOUNDARY（离线不可核实项）
- 方法：外部检索（arXiv / DOI / 期刊卷页三源核对）

## 汇总

条目 10（PASS=1 / CORRECTED=4 / MISMATCH=1 / BOUNDARY=1 / INFO=3）

守卫 10 / 10

评级：外部核实轮：来稿引用 2 真 1 误（Krasnikov 归属错）；四册结论零更正、净立场加强

## 守卫清单

| 守卫 | 结果 | 说明 |
|---|---|---|
| G0-1 | PASS | [c^2 v_s^2 (f')^2 / G] = 能量密度（r64 A03 唯一化族） |
| G0-2 | PASS | 能量密度 = 能量 / 体积 |
| G1-fuchs-bibcode-3way | PASS | Fuchs 2024 的 bibcode（2024CQGra..41i5013F）/ 期刊（CQG 41,095013）/ arXiv（2405.02709 = 2024-05）三源年份卷页一致 |
| G2-arxiv-ym | PASS | 全部 arXiv 号的 YYMM 与论文年份一致（新旧格式都过） |
| G3-krasnikov-polarity-ctr | PASS | 阳性对照：Krasnikov 原文标题含 do not forbid（许可向）、Finazzi 标题含 unstable（限制向）⇒ 极性检测器有判别力 |
| G4-ctc-threshold | PASS | CTC 判据 u > 2v/(1+v^2)：v=1 处阈值恰为 1（边界，阳性对照），v>1 全部 < 1 ⇒ 两个超光速泡只需亚光速相对速度即可生成 CTC |
| G5-fuel-mono | PASS | 燃料界 exp(-3L) 严格递减且 L=1 处已跌到 5% 以下（阳性对照：L=0 时为 1） |
| G6-refs-have-ids | PASS | 全部 11 条文献至少带 arXiv 号或 DOI（无 ID 不进判定） |
| G7-popular-not-cited | PASS | 流行科学数字（72%）标记为未核实，不作文献读数使用 |
| G8-g0-dims | PASS | 量纲工具自检（用于 V03a 互证读数） |

## 条目

### V01 · PASS · Fuchs 2024 引用确证：文献真实、六作者、CQG 41,095013、亚光速 + 全能量条件

外部检索确证来稿钥匙 2 所引文献真实存在且描述准确：Jared Fuchs/Christopher Helmerich 等 等 6 位作者《Constant Velocity Physical Warp Drive Solution》，arXiv:2405.02709，Class. Quantum Grav. 41, 095013 (2024)，DOI 10.1088/1361-6382/ad26aa。摘要原文关键句逐条与来稿对照：(1)「constant-velocity SUBLUMINAL warp drive」= 来稿「v_s<c」✓；(2)「satisfies ALL of the energy conditions」= 来稿「满足能量条件」✓；(3)「stable matter shell with a shift vector distribution」⇒ **正能量解不是 Alcubierre 型泡**，而是「物质壳 + 位移矢量」构造 ✓（与 r64 D02 的机器预测一致：r64 D02 已证明 §四 的 rho 式恒负、不可能给出正能量泡，故钥匙 2 必属不同度规族）；(4)「positive ADM mass」⇒ 正能量属性确认；(5)「shift vector cannot be reduced to a coordinate transformation」⇒ 该解不是坐标戏法（作者自设的反规避条款）。⇒ **r64 F01 从 BOUNDARY 升级为 PASS**：来稿引用为真，钥匙 2 的「纸上存在」成立。但注意：这只确认「存在亚光速正能量解」，不确认「已攻破超光速」——见 V07。

- 机器读数：`bibcode=2024CQGra..41i5013F | arxiv=2405.02709 (2024-05) | journal=Class. Quantum Grav. 41, 095013 (2024) | doi=10.1088/1361-6382/ad26aa`

### V02 · CORRECTED · 「2026 正能量解」确证存在（An T. Le 三篇），但净方向是收紧而非确认

来稿写「Fuchs 2024 及 2026 正能量解」。外部检索确证 2026 年确有同一路线的新文献，且全部出自单一作者 An T. Le 的三篇预印本：(a) arXiv:2602.18023《Observer-robust energy condition verification for warp drive spacetimes》（46 页）——把能量条件检验从「单一 Euler 观测者」升级为「全部观测者」的 4x4 线性矩阵不等式（S-lemma）判据，并实现为 Warpax 工具包；(b) arXiv:2605.25417《On the boundary cost of source-consistent warp shells》——对**八个经典正能量壳层构造**做完整能量条件测试，结论是违背**集中在源-真空过渡边界**而不在体内部（即正能量宣称在边界处失效）；(c) arXiv:2606.22531《Radiative steering of warp shells (v4; earlier title: Steering a warp drive without exotic matter)》（39 页）——在严格曲面主导能量条件下构造亚光速转向，但代价是 m_f/m_i = exp(-3L) 的指数燃料界。⇒ **2026 文献的净方向是收紧而非确认**：它们没有给出新的超光速正能量解，而是（i）证明 Euler 分析会漏检违背、（ii）八个构造的边界处仍违背、（iii）转向代价指数爆炸。⇒ 来稿把 2026 文献当作钥匙 2 的加强证据，属**引用方向误读**。

- 机器读数：`le2026=2602.18023,2605.25417,2606.22531`

### V03 · CORRECTED · r64 D01 的 Euler 观测者口径缺陷被 Le 2026 独立确证并形式化

r64 D01 曾判 BOUNDARY：来稿「对 Euler 观测者取 u = n 即违反 WEC」需限定 n 的类时性，且泡内 f=1 处 n 是零法向量。外部检索发现该边界裁定已被 2026 年文献**独立形式化并加强**：Le 2602.18023 摘要原文——「Whether a warp drive metric requires exotic matter is decided by energy conditions quantified over ALL observers, not only the Eulerian」，并把 NEC/WEC/SEC 表为 4x4 线性矩阵不等式（经典 S-lemma），DEC 需两项此类检验；进一步给出动量约束：单位时间膨胀切片上 Euler 动量与位移矢量涡量相联系，动量恒为零当且仅当位移矢量 = 梯度场 + 刚体转动。⇒ **r64 D01 从 BOUNDARY 升级为「已被外部文献独立支持」**，且这是本册与 r64 之间最强的一条跨册互证：r64 凭量纲与逻辑指出的口径缺陷，在文献侧有对应的严格化工具（warpax）。附带互证：r64 A03 用两条物理判据（恒等退化 + 线性 GR 极限）从 5 个量纲族中唯一选出 rho ~ v_s^2；Le 2602.18023 在「单位引力时间膨胀因子平直切片」上证明 Euler 负能积分严格按 v^2 缩放。两条独立路径同一指数 ⇒ 互证。⇒ 来稿 §四 的 WEC 论证（取 Euler 法向）按 2026 标准属**不完整检验**，虽然其「rho<0 ⇒ 违反 WEC」的结论方向仍成立（负能密度对任何观测者都违反 WEC），但论证方式已过时。

- 机器读数：`LE2602=arXiv:2602.18023 | r64 D01 联动 | rho~v_s^2 双路互证`

### V04 · CORRECTED · F02 降级确证：时序保护已有构型级双向结果（Everett-Roman / Sajeendran-Ralph 等）

r64 F02 曾判 BOUNDARY：「Hawking 时序保护猜想完全未攻破」是过度陈述，逻辑上「存在部分构型级结果」即足以否证「完全未攻破」。外部检索确证该降级：(1) Everett & Roman, Phys. Rev. D 56, 2100 (1997)（1997）——两个超光速泡在相对速度 u > 2v/(1+v^2) 时生成闭类时曲线（曲速版时序问题的经典构型级结果，早于 Hawking 1992 之后的全部讨论）；(2) Sajeendran & Ralph, arXiv:2407.18993（2024）——在受控旋转 Alcubierre 时空中构造自由落体观测者回到过去的显式机制；(3) Bunyaratavej 等, Eur. Phys. J. C 85, 270 (2025)（2025）——在具体黑洞时空中重新检验时序保护猜想。⇒ 措辞应改为「**未完全证明，且已有构型级双向结果**」（既有构造 CTC 的，也有检验保护机制的）。r64 F02 的降级建议成立。机器扫描 CTC 判据阈值（v = 泡速/c）：v=1.0000E+00 -> u_thr=1.00000000E+00（<1: False）；v=1.5000E+00 -> u_thr=9.23076923E-01（<1: True）；v=2.0000E+00 -> u_thr=8.00000000E-01（<1: True）；v=5.0000E+00 -> u_thr=3.84615385E-01（<1: True）；v=1.0000E+01 -> u_thr=1.98019802E-01（<1: True）；v=2.0000E+02 -> u_thr=9.99975001E-03（<1: True）。注意 v=1 处阈值恰为 1（阳性对照），v>1 时阈值全部 < 1：**两个超光速泡只需亚光速的相对速度即可互相生成 CTC**，这把「时序风险」从边缘情形变成结构性质。

- 机器读数：`ctc_thresholds=1.000000E+00,9.230769E-01,8.000000E-01,3.846154E-01,1.980198E-01,9.999750E-03`

### V05 · CORRECTED · ★承重：来稿「Krasnikov 不稳定」归属错误——Krasnikov 原文是许可向（QI 不禁止）

**本册最重要的单项发现：来稿对 Krasnikov 的归属是错误的。**来稿钥匙 4 写「Krasnikov：负能壳半经典不稳定」。外部检索定位到 Krasnikov 关于曲速的原始论文：S. Krasnikov《The quantum inequalities do not forbid spacetime shortcuts》，Phys. Rev. D 67, 104013 (2003)，arXiv:gr-qc/0207057（提交 2002-07）。该文标题直译即「量子不等式**不禁止**时空捷径」，其摘要明确把 Alcubierre 泡、Krasnikov 管与虫洞归为一类，并论证**量子不等式不禁止它们**——这是**许可向**结果，与来稿所述的「不稳定」方向相反。半经典不稳定性的正确归属是 S. Finazzi、S. Liberati、C. Barcelo：Superluminal warp drives are semiclassically unstable（J. Phys. Conf. Ser. 222, 012046 (2010)，DOI 10.1088/1742-6596/222/1/012046）与 Semiclassical instability of warp drives（J. Phys. Conf. Ser. 229, 012018 (2010)，DOI 10.1088/1742-6596/229/1/012018），以及综述向的 On the Impossibility of Superluminal Travel: The Warp Drive Lesson（arXiv:1001.4960）。⇒ 三条裁定：(a) 来稿钥匙 4 的**引用必须更正**（Krasnikov 2003 不支持「不稳定」 claim）；(b) 钥匙 4 的**结论方向仍成立**——曲速泡的半经典不稳定性有真实文献支持，只是作者是 Finazzi/Liberati/Barcelo 而非 Krasnikov；(c) 更微妙的一层：Krasnikov 的许可向论文与 Finazzi 的限制向论文并存，说明「量子不等式」与「半经典稳定性」是**两道彼此独立的关卡**——QI 不禁止（Krasnikov）不等于半经典稳定（Finazzi）。来稿把两者混为一条「钥匙 4」，属于本库「不同机制并账」缺陷族的又一实例。极性机检（G3）：Krasnikov 标题含 "do not forbid" = 许可向；Finazzi 标题含 "unstable" = 限制向 ⇒ 检测器有判别力。

- 机器读数：`krasnikov=%s PRD 67,104013 (do not forbid) | instability=Finazzi/Liberati/Barcelo 2010`

### V06 · INFO · Le 2026 燃料界 exp(-3L)：正能量壳层转向的指数代价（机器扫描）

Le 2606.22531（v4）给出正能量曲速壳层的转向代价：静止球面上逐次点火给m_f/m_i = exp(-3L)（L = 速度空间路径长度）。机器扫描：L=1.00E-01 -> m_f/m_i=7.40818221E-01；L=5.00E-01 -> m_f/m_i=2.23130160E-01；L=1.00E+00 -> m_f/m_i=4.97870684E-02；L=2.00E+00 -> m_f/m_i=2.47875218E-03；L=3.00E+00 -> m_f/m_i=1.23409804E-04；L=5.00E+00 -> m_f/m_i=3.05902321E-07。L=1 时只剩 4.978707E-02（约 4.9787E+00%）。⇒ 即使满足曲面主导能量条件（正能量壳层），**改变速度的代价是指数级的**，且自相似壳层需要各向异性应力并带有增长的法向模态（稳定性隐患）。这为 r64/r65 的「不可行」结论补上外部文献的工程侧证据：正能量路线的障碍不是「不可能转向」，而是「转向按 exp(-3L) 燃烧质量」。该文同时自留开放项：转弯后的自引力沉降未解决。

- 机器读数：`fuel=1.00E-01:7.40818221E-01,5.00E-01:2.23130160E-01,1.00E+00:4.97870684E-02,2.00E+00:2.47875218E-03,3.00E+00:1.23409804E-04,5.00E+00:3.05902321E-07`

### V07 · MISMATCH · 来稿「钥匙 2 纸上已攻破」推论过度：亚光速限定 + 边界违背 + 指数操控代价

综合 V01–V06，来稿把钥匙 2 列为「✅ 纸上已攻破」的推论过度，三处：(1) **范围**：Fuchs 2024 与 Le 2026 的全部正能量结果都限于**亚光速**；没有任何正能量解达到 v_s >= c。来稿表格把钥匙 2 与超光速需求并列，易被读成「正能量已解决一半」。(2) **边界违背**：Le 2605.25417 对八个经典构造的完整测试显示能量条件违背集中在源-真空过渡边界——「正能量壳层」在边界处并不正能量。(3) **可控性**：Le 2606.22531 显示满足 DEC 的转向受 exp(-3L) 燃料界，且 Bobrick-Martire 早已指出曲速泡「没有任何自然方式改变速度」。⇒ 正确记账：钥匙 2 = 「**亚光速正能量解确实存在（Fuchs 2024）**」+「**其完整能量条件自洽性在 2026 年被发现在边界处失效（Le 2605）**」+「**可控性代价指数级（Le 2606）**」——是「部分存在、边界存疑、操控昂贵」的三段式，不是「已攻破」。本项不推翻 r64/r65/r66/r67 的任何结论，只修正来稿钥匙 2 的状态词。

- 机器读数：`subluminal_only=true | boundary_violation=LE2605 | fuel=exp(-3L)`

### V08 · INFO · F01/F02/F03 三条 BOUNDARY 全部闭环；流行数字 72% 单独登记为 BOUNDARY

r64 登记的三条外部核实遗留项本册全部闭环：F01（Fuchs 2024）→ **PASS**（V01）；F02（时序保护措辞）→ **CORRECTED 且确证**（V04）；F03（Krasnikov）→ **CORRECTED 且归属纠错**（V05）。另登记一条不可用作文献读数的流行科学数字：「Euler 分析漏检约 72% 泡壁 WEC 违反（Rodal 几何）」出自 freeastroscience.com 的转述而非论文摘要，本册标 **BOUNDARY**：方向与 Le 2602.18023 的定理一致（Euler 分析不完整），但 72% 这个具体数字需查论文正文才能引用。按 r66 立下的纪律（比值/倍数读数必须先证量纲与来源），本册不把它用于任何判定。⇒ warp-drive 线（r64/r65/r66/r67 + 本册 r200）至此**无未闭环的外部核实项**。

- 机器读数：`F01=PASS(V01) | F02=CORRECTED(V04) | F03=CORRECTED(V05) | 72%=BOUNDARY`

### V09 · BOUNDARY · 流行转述数字「72% 漏检」不作文献读数（需论文正文核实）

Eulerian analysis missed about 72 percent of wall weak-energy violations in the tested Rodal geometry。来源：freeastroscience.com popular summary (not the paper abstract)。方向与 Le 2602.18023 定理（Euler 分析不完整）一致，但具体数值未核实。若后续要引用，须查 arXiv:2602.18023 正文中 Rodal 几何的逐点检验表。

- 机器读数：`unverified=72 | paper=LE2602`

### V10 · INFO · 净立场：外部核实加强 r64–r67 结论；唯一实质更正是来稿的 Krasnikov 归属

外部核实对 r64–r67 四册净立场的影响：**加强，不是削弱**。(1) r64 C01/C04 的「v_s>c 泡内固有时为虚」是数学事实，文献无争议；(2) r64 D02 的机器预测（正能量泡必非 Alcubierre 型）被 Fuchs 2024 的构造（物质壳 + 位移矢量，且自证非坐标变换）直接确证；(3) r64 D01 的 Euler 口径缺陷被 Le 2026 形式化（全部观测者 LMI 判据）；(4) r64 E03b 的撤回（r66 I03）不受影响——那是量纲问题，与文献无关；(5) r67 的「五族全关」针对的是 QEI 量纲闭合族，与外部文献两条线（正能量存在性 / 半经典稳定性）**互不重叠**，仍独立成立。⇒ 可引用的最终立场（更新版）：「超光速曲率引擎在 GR 内部结构性不可行：v_s>c 使泡内运动学失去实定义；唯一定义域内的 v_s→c⁻ 上，QEI 量纲闭合五族中四族被直接排除，仅存族要求壳厚锁死在 10 ℓ_P 内、宏观泡负能量跳到 10⁶ 倍可观测宇宙质量；正能量路线（Fuchs 2024 / Le 2026）仅限亚光速，且 2026 年发现其能量条件违背集中在源-真空边界、转向代价按 exp(-3L) 指数燃烧；半经典不稳定性的正确文献归属是 Finazzi-Liberati-Barcelo 2010（非 Krasnikov）。」⇒ 本册对外部文献的唯一实质更正是来稿的 Krasnikov 归属（V05），对四册结论零更正。

- 机器读数：`corrections_to_r64-r67=0 | corrections_to_incoming=1 (V05)`

## 文献登记表

| key | 文献 | arXiv | 期刊 | DOI |
|---|---|---|---|---|
| FUCHS2024 | Constant Velocity Physical Warp Drive Solution | 2405.02709 | Class. Quantum Grav. 41, 095013 (2024) | 10.1088/1361-6382/ad26aa |
| LE2602 | Observer-robust energy condition verification for warp drive spacetimes | 2602.18023 | arXiv preprint (46 pages, v5) | 10.48550/arXiv.2602.18023 |
| LE2605 | On the boundary cost of source-consistent warp shells | 2605.25417 | arXiv preprint | 10.48550/arXiv.2605.25417 |
| LE2606 | Radiative steering of warp shells (v4; earlier title: Steering a warp drive without exotic matter) | 2606.22531 | arXiv preprint (39 pages, v4) | 10.48550/arXiv.2606.22531 |
| FINAZZI2010 | Superluminal warp drives are semiclassically unstable | - | J. Phys. Conf. Ser. 222, 012046 (2010) | 10.1088/1742-6596/222/1/012046 |
| FINAZZI2010B | Semiclassical instability of warp drives | - | J. Phys. Conf. Ser. 229, 012018 (2010) | 10.1088/1742-6596/229/1/012018 |
| BARcELO2010 | On the Impossibility of Superluminal Travel: The Warp Drive Lesson | 1001.4960 | arXiv preprint (9 pages) | 10.48550/arXiv.1001.4960 |
| KRASNIKOV2003 | The quantum inequalities do not forbid spacetime shortcuts | gr-qc/0207057 | Phys. Rev. D 67, 104013 (2003) | 10.1103/PhysRevD.67.104013 |
| EVERETT1997 | Superluminal subway: The Krasnikov tube | - | Phys. Rev. D 56, 2100 (1997) | 10.1103/PhysRevD.56.2100 |
| SAJEENDRAN2025 | Looping back to the past through free fall in a controlled warp drive spacetime | 2407.18993 | arXiv preprint (v2, Mar 2025) | 10.48550/arXiv.2407.18993 |
| KERRSEN2025 | Revisiting chronology protection conjecture in the Dyonic Kerr-Sen black hole spacetime | 2408.06023 | Eur. Phys. J. C 85, 270 (2025) | 10.1140/epjc/s10052-025-13935-2 |

