# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R14  结激发能否提供大统一所需的规范量子数？—— 决定性检验
================================================================================
R12 的结论：单一最简表示无法实现大统一（质子衰变排除），必须成套引入新态；
R12 同时指出：**TUFT 通往 L3（可检验预言）的唯一已识别路径**
= TUFT 必须给出其结激发的 **T(R)（Dynkin 指数）与 Y²** 的具体有理数，
  才能进入 R12 的反解方程，反解出 M_new / M_GUT。

本册正面攻击这条路径。问题精确化：
    TUFT 的结拓扑不变量（Lk、自链、缠绕数 W、交叉数、亏格）能否**确定**
    规范群的表示 (R₃, R₂) 与超荷 Y？

答案（可算，且是决定性的）：**不能**。核心证据是一个简单的反例族——
    **所有 SM 费米子的自旋都是 1/2 ⇒ Lk 全等于 1，但它们的 (R₃,R₂,Y) 全不同。**
    ⇒ Lk 对 SM 费米子的**区分力为零** ⇒ 无法给出 Y、色表示、弱表示
    ⇒ 无法计算 T(R) 与 Y² ⇒ **R12 指出的唯一 L3 路径被关闭**。

本册结构：
  §1 需求回顾：R12 的反解究竟需要什么（可精确列出）
  §2 TUFT 可用的拓扑不变量清单（可算项逐项列出）
  §3 【决定性·反例 1】Lk → Y 不成立（Lk=1 对应 6 个不同超荷）
  §4 【决定性·反例 2】Lk → 色表示 / 弱表示不成立
  §5 规范玻色子与 Higgs 层（Lk=2 / 0）同样不成立
  §6 信息论量化：Lk 的区分力 vs 所需信息量（可算的自由度计数）
  §7 反解可行性：TUFT 无法进入 R12 的方程（不可计算，而非计算失败）
  §8 「注入 holonomy」路径的预测力审计（R9 4b 的后果）
  §9 【建设性】可能的补救：结群表示论 π₁(S³∖K) → G（初步可行性）
  §10 结论与开放项

红线：
  · 本册为**决定性否定**，但否定的是「TUFT 现有结构足以导出规范量子数」，
    不否定 TUFT 的其他部分（自旋/统计/拓扑量子化仍然成立）；
  · §9 提出的补救方向是**可能的路径**，本册只做初步可行性分析，不宣称已实现。
================================================================================
"""
import os
import sys
import math

import sympy as sp
from mpmath import mp, mpf, pi, cos, sin, sqrt

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "tuft_r14_report.txt")

OUT = []


def sec(t):
    OUT.append("\n" + "=" * 78)
    OUT.append("  " + t)
    OUT.append("=" * 78)


def put(s=""):
    OUT.append(s)


def bnd(name, detail):
    OUT.append("  [BOUNDARY] %s  |  %s" % (name, detail))


def info(name, detail):
    OUT.append("  [INFO] %s  |  %s" % (name, detail))


def main():
    sec("TUFT-R14  结激发能否提供大统一所需的规范量子数？—— 决定性检验")
    put("  R12 指出：TUFT 通往 L3 的唯一路径 = 给出结激发的 T(R) 与 Y²。")
    put("  本册检验：TUFT 的结拓扑不变量能否确定规范群的表示与超荷？")

    n_pass = 0
    n_fail = 0
    n_bnd = 0
    n_info = 0

    def P(name, detail):
        nonlocal n_pass
        n_pass += 1
        OUT.append("  [PASS] %s  |  %s" % (name, detail))

    def F(name, detail):
        nonlocal n_fail
        n_fail += 1
        OUT.append("  [FAIL] %s  |  %s" % (name, detail))

    def B(name, detail):
        nonlocal n_bnd
        n_bnd += 1
        bnd(name, detail)

    def I(name, detail):
        nonlocal n_info
        n_info += 1
        info(name, detail)

    # ═════════ §1 需求回顾 ═════════
    sec("1. 需求回顾：R12 的反解究竟需要什么")
    put("  R12 反解方程：L_ij = 2π(D_i − D_j)/((b_i+Δb_i) − (b_j+Δb_j))，ΔL = max − min")
    put("  其中 Δb 由新态的规范量子数**唯一确定**（R12 §1 已验证的公式）：")
    put("      Δb₃ = c·d(R₂)·T(R₃)")
    put("      Δb₂ = c·d(R₃)·T(R₂)")
    put("      Δb₁ = c·(3/5)·d(R₃)·d(R₂)·Y²        c = 2/3（Weyl）或 1/3（复标量）")
    put("")
    put("  ⇒ 要计算 Δb，必须**先知道三个量**：")
    put("     ① SU(3) 表示 R₃（决定 d(R₃) 与 T(R₃)）")
    put("     ② SU(2) 表示 R₂（决定 d(R₂) 与 T(R₂)）")
    put("     ③ 超荷 Y（决定 Y²）")
    P("1a: 需求已精确化（可检验的三项输入）",
      "Δb 的闭式已由 R12 验证；缺口被精确归约为「TUFT 能否给出 (R₃, R₂, Y)」，不再含糊")

    # ═════════ §2 TUFT 可用不变量 ═════════
    sec("2. TUFT 可用的拓扑不变量清单")
    invs = [
        ("链环数 Lk", "整数 ℤ", "Gauss 积分，R2/R9 已数值验证（Hopf |Lk|=1）"),
        ("自链数 SL", "半整数", "闭合曲线的自缠绕（Călugăreanu–White）"),
        ("缠绕数 W", "整数", "两条世界线的互缠（Q-TUFT 曾用，后被证非整）"),
        ("曲率 κ、挠率 τ", "连续 ℝ⁺", "Frenet 不变量，κ²+τ²=(ω/c)²"),
        ("交叉数 c(K)", "整数", "结图的最小交叉数（拓扑不变）"),
        ("亏格 g(K)", "整数", "结的 Seifert 亏格"),
        ("结群 π₁(S³∖K)", "群", "结补的基本群（非 Abel，信息量最大）"),
    ]
    put("  %-18s %-10s %s" % ("不变量", "取值", "说明"))
    put("  " + "-" * 84)
    for nm, rng, note in invs:
        put("  %-18s %-10s %s" % (nm, rng, note))
    I("2a", "TUFT 文献中**实际被使用**的只有 Lk、κ、τ 三个（R1–R10）；"
            "W 已被 Q-TUFT 证伪为「非整数」（拓扑荷 W 非整，见归一化坐标）；"
            "结群 π₁ 虽信息量最大，但 TUFT 从未使用过（见 §9）")

    # ═════════ §3 决定性反例 1：Lk → Y ═════════
    sec("3. 【决定性·反例 1】Lk 不能确定超荷 Y")
    put("  TUFT 的自旋公式（R2/R9，已验证）：S = Lk·ℏ/2  ⇒  Lk = 2S")
    put("  SM 全部费米子自旋 S = 1/2 ⇒ **Lk 全等于 1**。")
    put("  列出 Lk=1 的 SM 费米子场及其超荷（约定 a：Q = T3 + Y）：")
    put("")
    put("    %-8s %-14s %-10s %-12s %s" % ("场", "SU(3)×SU(2)", "Y", "Lk", "自旋"))
    put("    " + "-" * 62)
    sm_fermions = [
        ("Q_L", "3 × 2", sp.Rational(1, 6)),
        ("u_R", "3 × 1", sp.Rational(2, 3)),
        ("d_R", "3 × 1", sp.Rational(-1, 3)),
        ("L", "1 × 2", sp.Rational(-1, 2)),
        ("e_R", "1 × 1", sp.Integer(-1)),
        ("ν_R", "1 × 1", sp.Integer(0)),
    ]
    for nm, rep, Y in sm_fermions:
        put("    %-8s %-14s %-10s %-12s %s" % (nm, rep, str(Y), "1", "1/2"))
    Ys = [Y for _, _, Y in sm_fermions]
    n_distinct = len(set(Ys))
    put("")
    put("  同一 Lk (=1) 下，超荷 Y 取 %d 个互不相同的值：%s"
        % (n_distinct, ", ".join(str(y) for y in sorted(set(Ys), key=lambda z: float(z)))))
    F("3a: 【决定性】Y 不是 Lk 的函数（反例族）",
      "Lk=1 对应 %d 个不同超荷（1/6, −1/3, −1/2, 0, 2/3, −1）⇒ 数学上 Y 不可能由 Lk 决定。"
      "这是一个**反例证明**，不是推测：单值函数不能把一个输入映到 %d 个不同输出" % (n_distinct, n_distinct))
    P("3b: 反例有效性的形式检验",
      "函数性要求：Lk 相同 ⇒ Y 相同。实测 6 个场 Lk 同为 1 而 Y 有 %d 个值 ⇒ 函数性被**证伪**（sympy 有理数精确比较）"
      % n_distinct)

    # ═════════ §4 决定性反例 2：Lk → 表示 ═════════
    sec("4. 【决定性·反例 2】Lk 不能确定色表示与弱表示")
    su3reps = set()
    su2reps = set()
    for nm, rep, _ in sm_fermions:
        r3, r2 = rep.split(" × ")
        su3reps.add(r3)
        su2reps.add(r2)
    put("  Lk=1 的 6 个费米子场中：")
    put("    SU(3) 表示出现：%s   （色三重态与色单态**并存**）" % ", ".join(sorted(su3reps)))
    put("    SU(2) 表示出现：%s   （弱双重态与弱单态**并存**）" % ", ".join(sorted(su2reps)))
    F("4a: 【决定性】色表示不是 Lk 的函数",
      "同为 Lk=1：Q_L/u_R/d_R 是色三重态 3，而 L/e_R/ν_R 是色单态 1 ⇒ "
      "Lk 无法区分带色与不带色 ⇒ 无法给出 d(R₃) 与 T(R₃)")
    F("4b: 【决定性】弱表示不是 Lk 的函数",
      "同为 Lk=1：Q_L/L 是弱双重态 2，而 u_R/d_R/e_R/ν_R 是弱单态 1 ⇒ "
      "Lk 无法给出 d(R₂) 与 T(R₂)")

    # ═════════ §5 其他自旋层 ═════════
    sec("5. 规范玻色子层（Lk=2）与 Higgs 层（Lk=0）同样失败")
    put("    %-10s %-16s %-10s %-8s %s" % ("场", "SU(3)×SU(2)", "Y", "Lk", "自旋"))
    put("    " + "-" * 60)
    bosons = [
        ("gluon", "8 × 1", sp.Integer(0), 2),
        ("W", "1 × 3", sp.Integer(0), 2),
        ("B", "1 × 1", sp.Integer(0), 2),
        ("Higgs", "1 × 2", sp.Rational(1, 2), 0),
    ]
    for nm, rep, Y, lk in bosons:
        put("    %-10s %-16s %-10s %-8d %s" % (nm, rep, str(Y), lk, "1" if lk == 2 else "0"))
    put("")
    F("5a: Lk=2 的三个规范玻色子表示互不相同（8 / 3 / 1）",
      "gluon=(8,1)、W=(1,3)、B=(1,1) 同为 Lk=2 但 SU(3)/SU(2) 表示完全不同 ⇒ "
      "即便在玻色子层，Lk 仍**零区分力**")
    I("5b", "Higgs 是唯一 Lk=0 的 SM 场 ⇒ Lk 只能**区分自旋层级**（0 / 1/2 / 1），"
            "不能区分同一自旋层内的不同规范表示")

    # ═════════ §6 信息论量化 ═════════
    sec("6. 信息论量化：Lk 的区分力 vs 所需信息量")
    lk_vals = sorted({lk for _, _, _, lk in bosons} | {1})
    n_fields = len(sm_fermions) + len(bosons)
    put("  SM 场总数（本册计入）：%d 个" % n_fields)
    put("  Lk 在 SM 中的取值集合：%s ⇒ 只能分成 %d 个自旋层" % (lk_vals, len(lk_vals)))
    need_bits = math.log(n_fields, 2)
    have_bits = math.log(len(lk_vals), 2)
    put("")
    put("  区分 %d 个场所需信息量  = log₂(%d) = %.3f bits" % (n_fields, n_fields, need_bits))
    put("  Lk 实际提供的信息量    = log₂(%d) = %.3f bits" % (len(lk_vals), have_bits))
    put("  信息缺口              = %.3f bits" % (need_bits - have_bits))
    F("6a: 【决定性】Lk 的信息量**不足以**区分 SM 场",
      "需 %.2f bits，仅有 %.2f bits（缺口 %.2f bits）⇒ Lk 最多区分自旋层，"
      "而 SM 的规范量子数信息**完全不在** Lk 中" % (need_bits, have_bits, need_bits - have_bits))
    put("")
    put("  更精确的结构性论证：")
    put("    规范量子数 (R₃, R₂, Y) 是 **群表示论** 的对象；")
    put("    Lk、W、交叉数、亏格 是 **曲线/结拓扑** 的不变量。")
    put("    二者属于**不同的数学范畴**，且不存在自然函子把后者映到前者。")
    B("6b: 范畴差异是根因（不是「还没找到映射」，而是**不存在**自然映射）",
      "结拓扑不变量刻画的是 S³ 中曲线的嵌入方式；规范表示刻画的是主丛的纤维变换。"
      "从结到规范表示需要一个**额外结构**（如结群表示、或额外维度等距群），"
      "TUFT 未引入任何此类结构 ⇒ 缺的不是计算，是**定義**")

    # ═════════ §7 反解可行性 ═════════
    sec("7. 反解可行性：TUFT 无法进入 R12 的方程")
    put("  R12 反解要求输入 Δb_i = f(T(R₃), T(R₂), Y²)。")
    put("  TUFT 能提供的：Lk（⇒ 仅自旋）、κ、τ（⇒ 仅频率/质量标度，且标度须外部锚定 O-SCALE）。")
    put("  TUFT 不能提供的：R₃、R₂、Y ⇒ **T(R) 与 Y² 均不可计算**。")
    F("7a: 【决定性】R12 指出的唯一 L3 路径**被关闭**",
      "TUFT 无法计算 Δb ⇒ 无法进入 R12 的反解方程 ⇒ 无法反解 M_new / M_GUT ⇒ "
      "**无法产生可检验的新态质量预言**。注意这是『不可计算』（缺定义），不是『计算失败』")
    I("7b", "这个否定的精确边界：它否定的是「用 TUFT **现有**结构（Lk,κ,τ）导出规范量子数」，"
            "**不否定** TUFT 已成立的部分——自旋量子化、自旋-统计、LCS 链环-CS 对接仍然有效。"
            "TUFT 是一个**自旋/统计拓扑编码框架**，不是规范量子数导出框架")

    # ═════════ §8 注入路径的预测力审计 ═════════
    sec("8. 「注入 holonomy」路径的预测力审计（R9 4b 的后果）")
    put("  R9 §4b 已诚实标注：结构群 U(1)×SU(2)×SU(3) 是**假定**注入，非从底层导出。")
    put("  若接受这条注入路径，则 TUFT 可做：把 SM 场抄一遍，贴上 holonomy 标签。")
    put("  但这条路径的**预测力为零**：")
    put("    · 不能预言新粒子（清单 = SM 清单，R9 §4c 已承认）")
    put("    · 不能给出 Δb（因为 Y 是抄来的，不是导出的 ⇒ 与「导出」无区别）")
    put("    · 不能进入 R12 反解（反解需要**新态**的量子数，抄 SM 无新态）")
    F("8a: 【诚实】注入路径**不能**恢复 L3 前景",
      "注入 = 把答案抄进假设 ⇒ 不产生任何新预言。R9 §4c 已承认「未减少自由参数、未预言新粒子」；"
      "本册补充：它也**不能**提供 R12 所需的新态 Δb（因为注入的是 SM 现有场，不是新态）")

    # ═════════ §9 建设性：结群表示论 ═════════
    sec("9. 【建设性】可能的补救：结群表示论 π₁(S³∖K) → G")
    put("  这是**唯一**可能从结结构产生规范量子数的已知数学机制：")
    put("     结 K 的补空间 S³∖K 的基本群 G_K = π₁(S³∖K)（结群）")
    put("     结群到规范群 G 的表示 ρ: G_K → G  ⇔  平坦 G-联络")
    put("     （这正是 Chern–Simons 与 Jones 多项式的数学基础，与 R10 的 LCS 同构）")
    put("")
    put("  初步可行性（本册只做存在性检查，不宣称已实现）：")
    put("    · 三叶结 T(2,3) 的结群：⟨a, b | aba = bab⟩（辫群 B₃ 的表示）")
    put("    · B₃ 到 SU(2) 的表示由 R10 的 modular 数据给出（SU(2)_k，量子维数 d_i）")
    put("    · 量子维数闭式（R10 §9 已验证，i 对应自旋 j=i/2）：")
    put("         d_i = sin((i+1)θ)/sin θ,   θ = π/(k+2)")
    put("      注意：d₁ = sin(2θ)/sin θ = 2cos θ ；（**不可**推广为 2cos((i+1)θ)）")
    put("")
    put("    %-4s %-14s %-14s %-14s %s" % ("k", "d₀ (j=0)", "d₁ (j=1/2)", "d₂ (j=1)", "说明"))
    for k in (2, 3, 4, 5, 6):
        th = pi / (k + 2)
        d0 = sin(th) / sin(th)
        d1 = sin(2 * th) / sin(th)
        d2 = sin(3 * th) / sin(th)
        note = ""
        if k == 2:
            note = "d₁ = √2（openuft v29）"
        if k == 3:
            note = "d₁ = φ = 1.618（openuft v29）"
        if k == 4:
            note = "d₁ = √3"
        put("    %-4d %-14.9f %-14.9f %-14.9f %s" % (k, d0, d1, d2, note))
    P("9a: 结群表示论在数学上**存在**且可算（初步可行性成立）",
      "B₃ 的 SU(2)_k 表示给出量子维数谱 d_i = sin((i+1)θ)/sin θ（k=2: d₁=√2；k=3: d₁=φ），数值精确；"
      "⇒ 从结的辫群表示**确实可以**产生一组离散量子数（这是可能的补救方向）")
    B("9b: 【诚实】存在 ≠ 可用：三道未跨越的鸿沟",
      "① SU(2)_k 的量子维数 d_j 是**任意子/融合范畴**的量子数，**不是** SM 的规范表示 (R₃,R₂,Y)；"
      "② 需要把 d_j 翻译为 T(R₃)、T(R₂)、Y² —— 该翻译映射**不存在已知构造**；"
      "③ 即便存在，还须解释为何是 SU(3)×SU(2)×U(1) 而非其他群。"
      "⇒ 本册只指出**方向**，不宣称可行；列为开放项 O-KNOTREP")
    I("9c", "历史对照：这条路径与 Kaluza–Klein（额外维度等距群 → 规范群）、"
            "以及弦论（弦振动模 → 表示）属同一类型——都需要**额外结构**把拓扑变成规范。"
            "TUFT 迄今未引入任何此类结构，这正是 §6b 所指的「缺的是定義」")

    # ═════════ §10 结论 ═════════
    sec("10. 结论与开放项")
    put("  【决定性结论】")
    put("   ① 所有 SM 费米子 Lk 全等于 1，却有 6 个不同超荷 ⇒ Y 不是 Lk 的函数（反例证明）")
    put("   ② 同为 Lk=1，色三重态与色单态并存 ⇒ SU(3) 表示不是 Lk 的函数")
    put("   ③ 同为 Lk=2，gluon(8) / W(3) / B(1) 并存 ⇒ SU(2)、SU(3) 表示同样不是 Lk 的函数")
    put("   ④ 信息论：需 %.2f bits vs 仅有 %.2f bits ⇒ Lk 零区分力" % (need_bits, have_bits))
    put("   ⑤ ⇒ TUFT 无法计算 T(R) 与 Y² ⇒ **R12 指出的唯一 L3 路径被关闭**")
    put("   ⑥ 注入 holonomy 路径预测力为零，不能恢复 L3 前景")
    put("")
    put("  【建设性建议】唯一可能的补救 = 引入结群表示论 π₁(S³∖K) → G（§9），")
    put("     但须跨越三道鸿沟（翻译映射未知、任意子≠规范表示、群选择未解释）。")
    put("")
    put("  【本册不否定的部分】TUFT 的自旋量子化、自旋-统计、LCS 链环–CS 对接仍然成立；")
    put("     TUFT 的准确定位 = **自旋/统计的拓扑编码框架**。")
    for oid, txt in (
        ("O-KNOTREP", "结群表示 π₁(S³∖K)→G 是唯一可能的规范量子数来源；但 d_j→(T(R₃),T(R₂),Y²) "
                      "的翻译映射未知，且任意子量子数 ≠ SM 规范表示"),
        ("O-GAUGE-ORIGIN", "规范群 U(1)×SU(2)×SU(3) 无推导（R9 4b）；本册证明 Lk 不足以给出它"),
        ("O-L3-CLOSED", "R12 指出的 TUFT 通往 L3 的唯一路径已被本册关闭（不可计算）"),
    ):
        put("  · %-16s %s" % (oid, txt))
    put("")
    put("红线：本册否定的是「TUFT 现有结构足以导出规范量子数」，非 TUFT 全部；")
    put("      §9 的补救方向只做存在性检查，不宣称可行。")

    put("")
    put("汇总：PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
        % (n_pass, n_fail, n_bnd, n_info))

    txt = "\n".join(OUT) + "\n"
    print(txt)
    try:
        with open(REPORT, "w", encoding="utf-8") as fh:
            fh.write(txt)
        print("[报告已写入] " + REPORT)
    except Exception as exc:
        print("[warn] " + str(exc))


if __name__ == "__main__":
    main()
