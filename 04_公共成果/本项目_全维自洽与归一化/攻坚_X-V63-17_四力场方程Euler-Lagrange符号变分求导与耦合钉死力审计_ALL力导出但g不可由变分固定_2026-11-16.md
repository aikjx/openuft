# 攻坚册 X-V63-17 · 四力场方程的 Euler–Lagrange 符号变分求导与耦合钉死力审计

## 第 1 节 · 一句话结论

对标准模型规范群 U(1)×SU(2)×SU(3) 的完整 Yang–Mills 拉格朗日逐场做 Euler–Lagrange 符号变分，三种规范力的场方程均可精确导出（场方程项数 24 / 432 / 4920，符号偏导对中心差分 Richardson 两路相对误差 `2.175e-12`）；但三个规范耦合 \(g_1,g_2,g_3\) **无一能被变分本身固定为唯一值**（钉死数 0/3）。判词：`GATES-PASS-WITH-1-NEGATIVE`「所有力的场方程求导得出来，但没有一个力的耦合强度能由这场方程的求导本身定下来」。

## 第 2 节 · 与既有册的分工

- **R22（求导层）**：做单变量有理函数商法则、一圈 β、WLS 单方程族，结论是「真实新方程 0」，参数不灭落在**求导层**。
- **本册 X-V63-17**：把求导对象从单变量有理函数升级为**完整规范场强的泛函变分**——含 \(g f^{abc}A^b_\mu A^c_\nu\) 自相互作用全项，逐场求 Euler–Lagrange。问的是「所有力的场方程能否求导出来」与「求导能否固定耦合」，是 R22 之后求导层的一个新切面，不与 R22 相加。
- **X-V63-14/15/16（三个 OPEN）**：分别处理 6D 反常多项式、引力反常配平、G₄ 通量量子化，结论一致——CS 级 k 未被内部机制钉死。本册处理的是**规范耦合 g**，与 k 是不同对象（k 是 CS 级，g 是耦合常数），三册结论互印但不相加。
- **r403 GUT 裁决**：含引力四力大统一正确者 0 条，唯一真 C3 统一为电弱（仅 2 力）。本册为其补一个「场方程求导」侧的支撑读数，不改变其判词。

## 第 3 节 · 核心定理（可算命题）

**命题**：设 \(F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+g f^{abc}A^b_\mu A^c_\nu\)，\(\mathcal{L}=-\tfrac12 F^a_{\mu\nu}F^{a\mu\nu}\)（欧氏记号）。则：

1. Euler–Lagrange 变分 \(\partial_\nu\big(\partial\mathcal{L}/\partial(\partial_\nu A^a_\rho)\big)-\partial\mathcal{L}/\partial A^a_\rho=D_\mu F^{a\mu\rho}\) 是**恒等式**（场方程可由变分导出，残差按定义为零）；
2. 耦合 \(g\) 在 \(g^0,g^1,g^2\) 三个幂次上都出现在场方程中，但 \(\partial\mathcal{L}/\partial g\) 的「纯 \(g\) 分量」为空——不存在与背景场无关、可解出唯一 \(g\) 的变分方程。

第 1 条是 IDENTITY（不承重）；第 2 条是本册承重的可算判决。

## 第 4 节 · 机制

- **多项式引擎**：变量为场 \(A^a_\mu\) 与导数 \(\partial_\nu A^a_\mu\)，单项式为排序变量元组，系数 \(F\) 的单项式求导满足 \(g^2\mapsto 2g\)（此处曾暴露一处「求导把整幂变量删除」的对象错位错误，已修正）。
- **三群**：U(1) 取 \(f=0\)（阿贝尔，\(g\) 不进场强）；SU(2) 取 \(\varepsilon^{abc}\)（实表示）；SU(3) 取 Gell-Mann 结构常数，含 \(\sqrt3/2\)，用 `Decimal(60)` 精确处理。
- **变分提升算子**：\(\partial_\nu(\partial\mathcal{L}/\partial(\partial_\nu A))\) 把 \(A\to\partial A\)、\(\partial A\to\partial^2 A\)，再减 \(\partial\mathcal{L}/\partial A\)，得到 \(D_\mu F^{a\mu\rho}\) 的展开式。
- **耦合钉死判据**：把 \(g\) 当作动力学变量求 \(\partial\mathcal{L}/\partial g\)，取其中**不含任何场变量**的纯 \(g\) 分量；若有唯一根则钉死，否则不钉死。

## 第 5 节 · 机器守卫

| 守卫 | 内容 | 结果 |
|---|---|---|
| NO-HARDCODE-OK | AST 扫描判据行 `add()` 的 `ok` 参数无布尔字面量（登记行白名单） | PASS |
| KEY-TABLE-TWO-PATH | 路径 A 符号 \(\partial\mathcal{L}/\partial g\) 与路径 B 数值背景敏感性，三群一致 | PASS |
| ZERO-READOUT-DENOMINATOR | 钉死数 0 时写明分母 3（三个规范因子） | INFO |
| FIXER-PREDICATE-SENSITIVE | 加 \(\lambda(g-c)^2\) 后 \(pin=1, root=7/5\)；未加时 \(pin=0\) | PASS |
| EL-TWO-PATH | 符号偏导 vs 中心差分 Richardson 相对误差 `2.175e-12` < `1e-8` | PASS |
| VERDICT-MACHINE | 关键读数 +1 后判词串变化 | PASS |
| CONTROL-4-DISTINCT | 控制组 4 条读数两两不同 | PASS |
| GAUGE-GROUP-SPECTRUM | U1 的 \(g\) 幂次 `[0]`、SU2/SU3 为 `[0,1,2]` | PASS |

守卫合计 4/4（GUARD 类），判据 PASS 7 条、INFO 2 条、FAIL 1 条。

## 第 6 节 · 逐层判决

| 判据键 | 类型 | 读数 |
|---|---|---|
| EL-DERIVED-U1 | PASS | 24 |
| EL-DERIVED-SU2 | PASS | 432 |
| EL-DERIVED-SU3 | PASS | 4920 |
| EL-TWO-PATH | PASS | 2.175e-12 |
| KEY-TABLE-TWO-PATH | PASS | [0,0,0] |
| FIXER-PREDICATE-SENSITIVE | PASS | pos=7/5, base=0 |
| FROZEN-PARAM-TRAP | INFO | 单档 g=1 残差恒 0（假绿），全档幂次 [0,1,2] |
| ZERO-READOUT-DENOMINATOR | INFO | 0/3 |
| COUPLING-NOT-PINNED | FAIL（已登记，不挡门） | 0 |
| CROSS-VOLUME-READBACK | PASS | 3 |
| NO-HARDCODE-OK / VERDICT-MACHINE / CONTROL-4-DISTINCT / GAUGE-GROUP-SPECTRUM | GUARD | 全 PASS |

冻结参数陷阱如实报告：若只在单档 \(g=1\) 看，场方程残差恒为 0，会误判为「已固定」；全符号扫描显示 \(g\) 跨越 0/1/2 三个幂次，判别力真实存在。

## 第 7 节 · 控制组

| 控制组 | 生成元数 | \(g\) 幂次 | 场方程项数 | 钉死数 |
|---|---|---|---|---|
| U(1) 阿贝尔 | 1 | [0] | 24 | 0 |
| SU(2) 实表示 | 3 | [0,1,2] | 432 | 0 |
| SU(3) 复表示 | 8 | [0,1,2] | 4920 | 0 |
| 正对照 \(\lambda(g-c)^2\) | 1 | [0] | 1 | 1 |

4 条读数两两不同。正对照证明判据有判别力：人为加入一个把 \(g\) 固定到 \(c=7/5\) 的项后，钉死数从 0 变 1，根精确为 `7/5`。

## 第 8 节 · 诚实边界

- Einstein–Hilbert 场方程的变分不在本多项式引擎内（需度规行列式与曲率平方）；引力配平见 X-V63-15，结论是不给 k 新约束。
- 模型为 SM 规范群的纯 Yang–Mills 拉格朗日（欧氏记号，无度规符号），物质表示固定为给定维数；非全称定理。
- 单圈树级变分，未含量子反常与重整化群修正；耦合跑动见 R27。
- 钉死判据只问 \(\partial\mathcal{L}/\partial g\) 能否给出与背景无关的唯一根；不排除额外动力学或新物理机制。
- **数学自洽 ≠ 实验证实**；本册不产新物理。

## 第 9 节 · 跨册回代（磁盘实读）

| 回代册 | 命中 token | 文件 |
|---|---|---|
| X-V63-14 | `UNIQUE-U01-电弱统一-L-EW-唯一-仅覆盖-2-力` | `_XV6314_recompute_2026-11-08.json` |
| X-V63-15 | `NO-EXTRA-K-CONSTRAINT` | `_XV6315_recompute_2026-11-09.json` |
| X-V63-16 | `K-PINNED-0` | `_XV6316_recompute_2026-11-09.json` |

三处均从磁盘实读 JSON 并逐字命中，非手填；回代文件按精确前缀定位并排除 `_整理` 汇总册。

## 第 10 节 · 红线

- 数学自洽 ≠ 实验证实；只产可算判决，不产新物理。
- 独立实验预言当前 = 0；含引力四力大统一正确者 = 0 条；唯一真 C3 统一为电弱（仅 2 力）。
- 绝不写「统一场论已被攻破／实现」；本册结论是「所有力的场方程可求导导出，但耦合不可由变分固定」，是一个判负读数，不是突破。

## 第 11 节 · 复现与产物

```
python _assemble_xv6317.py       # 三部件 → 源码/_xv6317_recompute.py
python _run_xv6317.py            # 两次连跑，MD5 一致 773447c6…
python _xv6317_final_check.py    # 18/18，打印 ALL-CHECKS-PASS
```

产物：源码 `_xv6317_recompute.py`（21055 B）、数据 `_XV6317_recompute_2026-11-16.json`、`_XV6317_recompute_report_2026-11-16.txt`、本主文。

## 第 12 节 · 下一轮 OPEN

1. 把引力 Einstein–Hilbert 变分纳入符号引擎（度规行列式 + Ricci 标量），检验 \(G_{\mu\nu}=\kappa T_{\mu\nu}\) 中 \(\kappa\) 是否同样不可由变分固定。
2. 对含物质表示（费米子 Yukawa、Higgs）的完整 \(L_{SM}\) 做变分，问 Yukawa 耦合与 CKM 相能否被变分固定。
3. 在量子层（一圈有效作用量）重做耦合钉死判据，与 R20/R27 的跑动/交汇结论对接。

三项均为**新增外部对象**，非本审计线内可凭空构造；无新来料则本线维持暂停。

## 第 13 节 · 不占 RID 声明

本册为攻坚册 X-V63-17，不占新 RID、不进 README、不与任何审计卷或算法联盟册相加。README 实时字节数 939057 B（仅作快照，非判据）。

## 第 14 节 · 结论

四力（规范三力 U(1)/SU(2)/SU(3) + 引力作为边界）中，规范三力的场方程全部可由 Euler–Lagrange 变分精确导出，两路误差 `2.175e-12`；但三个规范耦合无一能被变分本身固定（0/3），正对照证明判据有判别力。这是参数不灭在**泛函变分求导层**的一个新实例：求导能给出力的方程形式，却定不下力的强度。「最正确的统一方程」在本口径下仍不可内部判定——四力统一正确者 0 条，独立实验预言 0。**不宣称攻破统一场论。**
