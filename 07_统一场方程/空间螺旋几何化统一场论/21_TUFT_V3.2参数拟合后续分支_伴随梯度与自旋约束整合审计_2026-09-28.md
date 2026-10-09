# TUFT V3.2 参数拟合后续分支（分支A 伴随梯度 / 分支B N=ℏ 自旋-挠率约束）· 来稿整合审计

2026-09-27 至 09-28 日界轮。来稿为「本项目最高权限｜TUFT V3.2 参数拟合后续分支完整推导与精算框架」，
含分支 A（伴随解析梯度替换有限差分）、分支 B（自旋-挠率约束 $N=\hbar$ 打破简并）、三阶段执行规划与
末尾「选定。」二问。本轮**不重复实现**已在库内落地的部分，而是把该稿 12 项主张逐条并入既有证据链
（07 系列 15A/16/17/18 稿、S14 系统的同名分析与审计），并用 sympy 精确符号推导给每条主张一个可复现裁定。

[来稿原文](来稿_TUFT_V3.2参数拟合后续分支_伴随梯度与自旋约束_2026-09-27.txt)（UTF-8/LF，9,934 字节、183 行（按换行计））
SHA-256：`19CFB6BD308DE7A11C6A13C393515FDBF560698A2C8A15AF8B57146F8FFF782D`。
[符号核验脚本](验证脚本/V32_参数拟合后续分支_2026-09-27/branch_ab_symbolic_audit.py) ·
[核验读数](V3_8_paramfit_branch_checks.json)（sympy 1.13.3，run_time 见 JSON `meta`）。
既有相关轮次：[S14 同名分析](../../01_独立体系/S14_挠率统一场论TUFT/04_理论推导/tuft_v32_参数拟合_伴随梯度与自旋约束_分析.md)、
[18 稿·伴随审查复核](18_伴随审查复核与约束梯度融合_2026-09-27.md)、
[15A 稿·路线2 符号自洽审计](15A_路线2数值校验_符号自洽与局域性审计_2026-09-27.md)、
[17 稿·固定荷敏感度](17_固定荷敏感度求导与能量交叉验证_2026-09-27.md)。

---

## 0. 结论先行

**本稿整体判定：已在库内处理过的框架稿的"补全推导版"，其中 12 项主张 1 项成立、3 项订正后成立、
7 项不成立、1 项待补。** 三条独立结论：

1. **分支 A 的"伴随"三点误一处、一处多余**：A1 的原方程 $\mathcal F$ 与其自身 $E_0$ 的 EL 方程
   **符号不一致**（差 $2\mathcal P$，$\mathcal P:=\mathcal V_1\psi^3-\mathcal V_2\psi^5$）；
   A1 的伴随算子 $\mathcal F^*$ 把一阶项写成 $+2/r$，在 $4\pi r^2dr$ 加权下正确算子是**自伴**的
   $-\partial_r^2-(2/r)\partial_r+\mathcal V$；而该 $+2/r$ 版连**完备无权伴随**都不是（缺 $-2\psi_a/r^2$）；
   A2 用伴随处理 $E_0$ 是多余的（包络定理，见 T3）。
2. **分支 B 的目标与手段错位（秩证明）**：$\nabla(\mathcal N-\hbar)$ 在 $(q_0,\omega_0)$ 分量为 0，
   而简并方向 $t=(0,0,q_0,-\omega_0)$ 在 $(\mathcal V_1,\mathcal V_2)$ 分量为 0，故
   $\nabla G\cdot t\equiv0$；把 $G$ 加进目标雅可比后秩仍为 **3**、零度仍为 **1** ⇒ $N=\hbar$ **不切断简并**。
   它作用在剖面上，使 2 未知的剖面变成 3 方程**过定**。
3. **「$S=(s/2)\mathcal N$」的 $1/2$ 无来源**：对 $\psi=f(r)e^{is\phi}$ 直接算 Noether 轨道角动量得
   $\mathcal L_z/\mathcal N=s$（无 $1/2$）；$1/2$ 只能来自旋量表示，而标量场 $\Sigma^{\mu\nu\alpha}=0$。
   所以「$N=\hbar$」这一约束的**数值目标本身不唯一**（同一 ansatz 下也可读作 $N=\hbar/2$）。

---

## 1. 主张逐项裁定表

| # | 来稿主张 | 裁定 | 依据（读数所挂文件） | 级别 |
|---|---|---|---|---|
| M1 | A1：$\mathcal F=-\psi''-\frac2r\psi'-\mathcal V_1\psi^3+\mathcal V_2\psi^5$ 是所写 $E_0$ 的驻点方程 | ❌ 不成立（非线性块符号相反，$\delta E_0/\delta\psi-\mathcal F=2\mathcal P$） | `V3_8_paramfit_branch_checks.json` → `checks.T1_el_sign.resid_ed_minus_F_doc`；18 稿 §1 | mathematical_result |
| M2 | A1：该方程存在满足 $\psi'(0)=0,\psi(\infty)=0$ 的有限范数非零孤子 | ❌ 不成立（$-\Delta f+\mathcal V_1f^3-\mathcal V_2f^5=0$ 经积分+Pohozaev 只有零解；来稿符号版连 EL 都不满足） | 18 稿 §1；15A 稿；S14 §7.1（补质量项后趋向平台 $\psi\approx0.488$） | mathematical_result |
| M3 | A1：伴随方程 $-\psi_a''+\frac2r\psi_a'+\mathcal V\psi_a=$ 源 | ⚠️ 订正后成立（加权下自伴；$+2/r$ 版非完备无权伴随，缺 $-2\psi_a/r^2$） | `T2_adjoint.resid_weighted_minus_boundary_total_derivative=0`、`resid_来稿伴随_minus_完备无权伴随=-2v/r^2`；S14 报告 `3.840e-14` vs `4.701e-01` | mathematical_result |
| M4 | A3：$\mathcal N,\mathcal I_\mu,\mathcal C$ 三个源项公式 | ✅ 成立（加权约定下为 $2f$、$rf$ 的等价写法） | `tuft_v32_参数拟合_伴随梯度与自旋约束_分析.md` §A3；18 稿 §2 | mathematical_result |
| M5 | A3：$\delta E_0/\delta\psi=4\pi r^2\mathcal P$ | ❌ 不成立（$E_{\text{code}}$ 背景上正确值为 $0$；$F_{\text{doc}}$ 背景上是 $2\cdot4\pi r^2\mathcal P$，两个背景都不是来稿值） | `T3_envelope`：`on_F_code=0`、`on_F_doc=2*(V1-V2*psi^2)*psi^3` | mathematical_result |
| M6 | A2：$E_0$ 需伴随 ODE | ⚠️ 订正（$E_0$ 是被最小化泛函，走包络定理 $\frac{dE_0}{d\mathcal V_1}=\frac14\!\int\!\psi^4 4\pi r^2dr$、$\frac{dE_0}{d\mathcal V_2}=-\frac16\!\int\!\psi^6 4\pi r^2dr$） | 同 M5；S14 §A4 | mathematical_result |
| M7 | A2：$\partial\chi^2/\partial q_0,\partial\chi^2/\partial\omega_0$ 纯解析、无需伴随 | ✅ 成立（在本稿模型内）；⚠️ 但这正是简并的人为来源，且该前提在**带相位动能的修复模型**中失效（$M$ 依赖 $\omega_0$） | `T4_degeneracy`；S14 §B4-1；17 稿（修复模型里背景随 $\omega$ 重新求解） | mathematical_result |
| M8 | B1：简并根源是 $4-3=1$ 的一般流形 | ❌ 不成立（$Q_0,\mu$ 只依赖 $\Pi=q_0\omega_0$：解析核 $t=(0,0,q_0,-\omega_0)$，秩 3、零度 1；有效独立量本就是 3） | `T4_degeneracy.J_times_t=[[0],[0],[0]]`；S14 报告 V2（$\Pi=2$ 的四组 $(q_0,\omega_0)$ 给出同一 $Q_0=1.348937e{+}02$、$\mu=2.252569e{+}02$）；18 稿 §5 | mathematical_result |
| M9 | B2/B4：$N=\hbar$ 把约束数 3→4、自由度 $4-3-1=0$、消除简并 | ❌ 不成立（增广雅可比秩 $3\to3$、零度仍 1；且剖面 3 方程/2 未知过定） | `T4_degeneracy.rank_stacked_with_N_hbar=3`、`T5_count.over_determined=True` | mathematical_result |
| M10 | B2：$S^{\mu\nu\alpha}=\frac i2(\psi^*\Sigma^{\mu\nu\alpha}\psi)$，标量孤子携带自旋 $\hbar/2$ | ❌ 不闭合（复标量 $e^{is\phi}$ 给的是轨道角动量，$\mathcal L_z/\mathcal N=s$；旋量 $\Sigma$ 对标量表示为 0） | `T6_orbital_spin.ratio_Lz_to_N=s`、`resid_ratio_minus_s=0`；16 稿（轨道/内禀自旋分离） | mathematical_result（物理身份层面 conjecture） |
| M11 | B4 步骤 3：$\mu=\mathcal Q_e\mathcal I_\mu/\hbar$ 可当电子磁矩拟合目标 | ❌ 不成立（球对称静电背景空间电流为 0 ⇒ $\mu=0$，相对误差目标至少为 1） | 15 稿三方向审订；`V3_2_孤子多极矩复算.py`（除总电荷外全电磁多极矩为 0） | mathematical_result |
| M12 | B5：约束给出唯一 $\mathcal C$、$\mu$、挠率分布 $T(r)$ 与自旋进动预言 | ⚠️ 待补（$\mathcal C$ 的归一化与单位/4π 未钉扎；进动需旋量结构；本库 $\kappa=8\pi G/c^4$ 侧尚无自洽 ECSK 自旋源解） | S14 §B3-3；`02_TUFT_来源` 的 R13/R18/R19 挠率审计；本页 §2 数字纪律 | conjecture |

---

## 2. 本轮新增的符号核验（T1–T6，逐条带反对照）

脚本：`验证脚本/V32_参数拟合后续分支_2026-09-27/branch_ab_symbolic_audit.py`（sympy 1.13.3；
每条判据同时打印一枚**必须非零**的对照组，避免"全绿自证"）。

| 项 | 结果（JSON 字段） | 反对照 |
|---|---|---|
| T1 EL 符号 | $\delta E_0/\delta\psi/(4\pi r^2)=-\psi''-\frac2r\psi'+\mathcal V_1\psi^3-\mathcal V_2\psi^5$；$\mathrm{resid}-\mathcal F_{\rm doc}=2(\mathcal V_1-\mathcal V_2\psi^2)\psi^3$，$\mathrm{resid}-\mathcal F_{\rm code}=0$ | 「$ed-\mathcal F_{\rm doc}$ 必须恰为 $2\mathcal P$ 且非零」= `True` |
| T2 伴随 | 加权 $4\pi r^2dr$ 下 $\langle u,\mathcal Lv\rangle-\langle v,\mathcal Lu\rangle$ 精确等于边界全导数 $4\pi[r^2(vu'-uv')]$（残差 `0`）；完备无权伴随 $=-v''+\frac2r v'+\mathcal A v-\frac{2v}{r^2}$ | 来稿伴随与完备无权伴随之差 $=-2v/r^2\neq0$ = `True` |
| T3 包络 | $\mathcal F_{\rm code}=0$ 上 $\delta E_0/\delta\psi=0$；$\mathcal F_{\rm doc}=0$ 上 $=2\mathcal P$ | 来稿源项 $4\pi r^2\mathcal P$ 在**两个**背景上的残差分别为 $-4\pi r^2\mathcal P$、$+4\pi r^2\mathcal P$，均非零 = `True` |
| T4 秩 | $\mathcal J\,t=0$、$\nabla G\,t=0$、$\mathrm{rank}\,\mathcal J=\mathrm{rank}\,[\mathcal J;\nabla G]=3$、零度 $1$ | 数值零空间基（$\mathcal V_1{=}1.7,\mathcal V_2{=}2.3,q_0{=}0.9,\omega_0{=}1.1$）= `[1.60626626139562e-14, 0.0, -0.8181818181818181, 1.0]`，与解析 $t\propto(0,0,q_0,-\omega_0)$ 一致（$0.9/1.1=0.81818\ldots$）；若误取 $(0,0,\omega_0,-q_0)$ 则 $\mathcal Jt\neq0$（脚本首版即因此反照红出，已改） |
| T5 计数 | 剖面：未知 2、加 $\mathcal N=\hbar$ 后方程 3 ⇒ 过定；有效独立参数 3（$\mathcal V_1,\mathcal V_2,\Pi$）对 3 目标 | 来稿「$4-3-1=0$」在 JSON 里显式记为 `False` |
| T6 自旋 | $\mathcal L_z$ 密度 $=f_0^2 s$，$\mathcal L_z/\mathcal N=s$ | `resid_ratio_minus_s=0`，同时打印 $\mathcal S=\frac s2\mathcal N$ 记为 `False`（即 $\frac12$ 因子无轨道来源） |

**读数一致性**：T2/T4 与 S14 的数值版核验同源——
`tuft_v32_adjoint_degeneracy_report.txt` 给出随机测试函数 200 组
$\max|\langle\mathcal Lf,g\rangle-\langle f,\mathcal Lg\rangle|/\mathrm{ref}=3.840e{-}14$（自伴）
与 $\max|\langle\mathcal Lf,g\rangle-\langle f,\mathcal L_{\rm flip}g\rangle|/\mathrm{ref}=4.701e{-}01$（来稿翻转版不是伴随），
本轮把同一结论从"数值 200 组"升级为"符号恒等式 + 边界项闭式"。

---

## 3. 与库内既有落地的关系（本稿已完成 / 不应重复执行）

| 来稿阶段 | 库内状态 | 读数出处 |
|---|---|---|
| A3「解析雅可比替换有限差分」 | **已实现并验证**：物理 ansatz 上 $\chi^2$ 梯度全解析，解析 vs 有限差分最大相对误差 `5.491e-08`（4 测试点）；解析 jac 的 SLSQP/L-BFGS-B 收敛到 `χ²=2.353486e-17`（`success=True`、`iter=57`、`nfev=88`），`E_tot/电子静能=1.000000`、`N=1.000000` | `../../01_独立体系/S14_挠率统一场论TUFT/09_验证结果/原始运行记录/tuft_v32_adjoint_slsqp_report.txt`（脚本 `tuft_v32_adjoint_slsqp.py`） |
| A 阶段的"约束/伴随"正确形态 | **已重做**：固定荷约束下的伴随需带秩一项 $\mathcal K=\mathcal L_++\frac{4\omega^2}{\mathcal I}|f\rangle\langle f|$；直接解、伴随解、背景重解三方交叉到 `1.94e-12 / 6.92e-12 / 3.62e-11`（三档网格），漏掉秩一项给出 `-737.920785710305`（数量级与符号同时错） | 18 稿 §3–§4、`V3_5_adjoint_crosschecks.json` |
| 无约束"简并流形扫描"（阶段一第 3 步） | **口径需改**：可扫描的是 $\Pi=q_0\omega_0$ 固定下的 $q_0/\omega_0$ 比值（对该比值全部可观测量不变 ⇒ 扫描必然给常数），以及 $(\mathcal V_1,\mathcal V_2)$ 上的真实剖面流形；来稿把两者混为一谈 | 本表 M7/M8 |
| 分支 B「SLSQP 增加等式约束 $\mathcal N=\hbar$」（阶段二） | **不应执行**：见 M9（不切断简并、剖面过定）；且单位制/4π 未钉扎前 $\mathcal N=\hbar$ 无唯一数值目标（M12） | 18 稿 §5「$N=\hbar$」「简并流形」两行、S14 §B2–B3 |
| 阶段三校验闭环 | **前置关口未到**：18 稿 §6 与 20 稿把下一实质关口定在**带电约束二次型与扰动谱**（中性分支已完成 $\ell=0,1,2$ 稠密全谱，`linear_stable_candidate`）；带电规范零模仍缺 ⇒ 在缺口上跑电子拟合会产出不可解释的"验证" | 20 稿、18 稿 §6 |

---

## 4. 「选定。」的执行裁定

来稿末尾只写「选定。」而选项 1/选项 2 并列，未指明选中其一（与 15 稿「延续」轮的同一遗留一致）。
按本轮证据裁定为：**两个选项都不按原样执行**。

- 不执行选项 1 的**重复部分**：分支 A 的实用内涵（解析梯度替换有限差分）已在库内落地
  （§3 第一行），再跑一次"高精度无约束优化"只会在错误的简并口径上刷精度。
  仍要做的**是订正**：把 M1/M3/M5 三处符号错误写进任何后续实现的前置修正清单。
- 不执行选项 2：$N=\hbar$ 不切断简并（M9）、$\mathcal L_z/\mathcal N=s$ 与 $1/2$ 无来源（M10）、
  $\mu$ 在球对称静电背景为 0（M11）。
- 实际下一关口（继承 18 稿 §6 / 20 稿）：**带电分支的约束二次型与扰动谱**，即把 $\omega_0$ 按
  M7 的反面处理——让相位动能进入 $M$，使 $\mathcal V_1,\mathcal V_2,\omega_0$ 由三个观测量分立锁定，
  再由 $\Pi$ 定 $q_0$；这既是"打破简并"的正确手段，也不需要引入未定义的自旋挠率源。

---

## 5. 数字纪律、红线与登记

- 本文件所有读数均点名印出它的文件；`V3_8_paramfit_branch_checks.json` 是本轮脚本的原始输出，
  未手改；符号结论以 sympy `simplify` 恒等式为准，数值对照组同时打印。
- 首跑曾因输出路径少推导一层而把同一份读数写到 `验证脚本/` 下（该副本 `meta` 无 `run_time`、
  `meta.script` 缺 `验证脚本/` 前缀，可与有效面区分）。该副本已删除，`material_catalog.md` 与
  `structure_manifest.json` 中对应条目同步移除；唯一有效读出面为系列根目录的该 JSON。
- 只核验算子代数、变分符号与自由度计数：**未**重解孤子背景、**未**做电子拟合、**不**构成对
  TUFT 物理真实性的判定；不升级 L3 计数，也不改变 UFT 完成度（2/6、L3=0、UFT-3=0 不变）。
- 新增 claim（`claims.csv`）：C80（M1＋M3＋M5 与 $E_0$ 源项的符号裁定）、C81（M8＋M9 的秩裁定，并含 M10 的
  $\mathcal L_z/\mathcal N=s$ 与 $\frac12$ 因子无来源）、C82（分支 A 的工程内涵已在 S14 复现、电子身份关口仍开放）。
  编号按登记时台账末行顺延（该目录存在并发写入者，故不写死前驱编号）。
- 遗留开放：$\mathcal C$ 与 $\mathcal N$ 的单位制/4π 钉扎、旋量自旋的合法构造、
  带电流稳定性与完整约束二次型扰动谱（三者登记在 C82 与 18/20 稿中，均未闭合）。

## 6. 复现

```bash
cd openuft/07_统一场方程/空间螺旋几何化统一场论/验证脚本/V32_参数拟合后续分支_2026-09-27
python branch_ab_symbolic_audit.py      # 重写 ../../V3_8_paramfit_branch_checks.json
```
