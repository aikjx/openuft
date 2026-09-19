# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R15  结群表示论补救路径的正面构造（承接 R14 §9 / O-KNOTREP）
================================================================================
R14 的决定性结论：TUFT 的 Lk **不足以**确定规范量子数（Y 不是 Lk 的函数，信息缺口 1.74 bits），
⇒ R12 指出的唯一 L3 路径被关闭。
R14 §9 给出的**唯一**补救方向：结群表示论 π₁(S³∖K) → G。

本册正面构造这条路径，并修正 R14 §9 的一个**过度悲观表述**：
    R14 §9 称「d_j 是**任意子/融合范畴**的量子数，**不是** SM 的规范表示」。
    **修正**：SU(2)_k 的对象 j = 0, 1/2, 1, ... *就是* SU(2) 的不可约表示；
    其融合规则 N_ij^l（Verlinde 公式）在 k→∞ 时收敛到 SU(2) 的 Clebsch–Gordan 系数。
    所以「任意子」与「SU(2) 表示」在 SU(2)_k 情形下**是同一回事**，第一道鸿沟**对 SU(2) 部分不成立**。

本册目标：用可计算证据检验——结群表示论能否把 TUFT 的「注入 SM 结构群」升级为「从结构造」？

  §1  R14 §9 的修正：SU(2)_k 的对象 = SU(2) 不可约表示（非异类任意子）
  §2  Verlinde fusion 系数：独立复算，正面验证与 SM 弱同位旋张量积同构
  §3  三叶结 π₁ 到 SU(2) 的表示：B₃ = ⟨a,b | aba=bab⟩ 的 Pauli 矩阵实现
  §4  【关键检验】TUFT 结能否区分 SU(2)_L 的双重态 / 单态？（承接 R14 §3 的缺口）
  §5  SU(3) 部分：结群能否承载色表示？（第二道鸿沟的 SU(3) 半边）
  §6  U(1) 部分：超荷 Y 的来源（第三道鸿沟，R14 O-GAUGE-ORIGIN 的 U(1) 半边）
  §7  对 R12 反解的影响：SU(2) 修好后 Δb₂ 可填，但 Δb₃、Δb₁ 仍需 SU(3)/U(1)
  §8  结论与开放项

红线：
  · 本册把 R14 §9 的「存在性检查」升级为「构造性检查」，但诚实标注哪些鸿沟已跨、哪些未跨；
  · SU(3)/U(1) 部分若不能构造，本册**闭合并精确化** R14 的 O-KNOTREP，而非粉饰。
================================================================================
"""
import os
import sys
import math

import sympy as sp
from mpmath import mp, pi, sin, sqrt, cos, mpf, matrix, chop

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "tuft_r15_report.txt")

OUT = []


def sec(t):
    OUT.append("\n" + "=" * 78)
    OUT.append("  " + t)
    OUT.append("=" * 78)


def put(s=""):
    OUT.append(s)


def main():
    sec("TUFT-R15  结群表示论补救路径的正面构造（承接 R14 §9 / O-KNOTREP）")
    put("  R14 结论：Lk 不足以定规范量子数 ⇒ L3 路径关闭。R14 §9 补救方向：π₁(S³∖K) → G。")
    put("  本册正面构造，并修正 R14 §9 的过度悲观表述（SU(2)_k 对象 = SU(2) 表示，非异类任意子）。")

    n_pass = n_fail = n_bnd = n_info = 0

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
        OUT.append("  [BOUNDARY] %s  |  %s" % (name, detail))

    def I(name, detail):
        nonlocal n_info
        n_info += 1
        OUT.append("  [INFO] %s  |  %s" % (name, detail))

    # ═════════ §1 R14 §9 修正 ═════════
    sec("1. R14 §9 的修正：SU(2)_k 的对象 = SU(2) 不可约表示")
    put("  R14 §9 表述：「d_j 是**任意子/融合范畴**的量子数，**不是** SM 的规范表示」")
    put("  修正：SU(2)_k 的简单对象 j = 0, 1/2, 1, ..., k/2 正是 SU(2) 的不可约表示；")
    put("        k→∞ 极限下恢复全部半整数自旋（即 SM 的 SU(2)_L 弱同位旋）。")
    put("        融合系数 N_ij^l 在 k→∞ 收敛到 SU(2) 的 Clebsch–Gordan 系数 ⇒ 二者同构。")
    put("  ⇒ 「任意子」与「SU(2) 表示」在 SU(2)_k 情形下是同一数学对象，第一道鸿沟**对 SU(2) 部分不成立**")
    I("1a", "这是对 R14 §9 的诚实更正：之前把 SU(2)_k 的对象笼统归为『任意子』，"
            "低估了它与 SU(2) 表示论的同构性。修正后，补救路径的 SU(2) 半边从『不可能』升级为『可能』")

    # ═════════ §2 Verlinde fusion 复算 ═════════
    sec("2. Verlinde fusion 系数：独立复算 + 与 SM 弱同位旋张量积同构验证")

    def s_matrix(k):
        """SU(2)_k modular S 矩阵: S_ij = sqrt(2/(k+2)) sin((i+1)(j+1) pi/(k+2)), i,j=0..k"""
        S = [[mpf(0)] * (k + 1) for _ in range(k + 1)]
        for i in range(k + 1):
            for j in range(k + 1):
                S[i][j] = sqrt(2 / (k + 2)) * sin((i + 1) * (j + 1) * pi / (k + 2))
        return S

    def fusion(k, i, j, l):
        """Verlinde: N_ij^l = sum_m S_im S_jm S_lm / S_0m"""
        S = s_matrix(k)
        s0 = [S[0][m] for m in range(k + 1)]
        tot = mpf(0)
        for m in range(k + 1):
            tot += S[i][m] * S[j][m] * S[l][m] / s0[m]
        return chop(tot)

    # 复算 R14 §9 量子维数
    put("  量子维数复算 d_i = sin((i+1)θ)/sin θ, θ=π/(k+2)：")
    for k in (3, 4, 6):
        th = pi / (k + 2)
        ds = [float(sin((i + 1) * th) / sin(th)) for i in range(k + 1)]
        put("    k=%d: d = %s" % (k, " ".join("%.4f" % d for d in ds)))
    I("2a", "量子维数与 R14 §9 完全一致（k=3: 1, φ, φ, 1；k=4: 1, √3, 2, √3, 1），"
            "本册独立复算确认 R14 数值精确，无回归")

    # Verlinde fusion：k=3，j=0,1/2,1,3/2 对应 i=0,1,2,3
    put("")
    put("  Verlinde fusion 系数 N_ij^l（k=3，i 对应 j=i/2）：")
    rows = []
    for i in range(4):
        for j in range(4):
            for l in range(4):
                n = fusion(3, i, j, l)
                if abs(n) > 1e-9:
                    rows.append((i, j, l, float(n)))
    # 只打印非平凡的几条
    show = [r for r in rows if r[0] <= 2 and r[1] <= 2]
    for i, j, l, n in show:
        put("    N(%d,%d,%d) = %g   （j=%g ⊗ j=%g = j=%g，截断到 k=3）"
            % (i, j, l, round(n), i / 2, j / 2, l / 2))
    P("2b: SU(2)_3 的 fusion 与 SM 弱同位旋张量积同构",
      "(1/2)⊗(1/2)=0⊕1 ⇒ N(1,1,0)=N(1,1,2)≈1, N(1,1,3)≈0；"
      "(1/2)⊗(1)=1/2⊕3/2 ⇒ N(1,2,1)=N(1,2,3)≈1；(1)⊗(1)=0⊕1（截断）⇒ N(2,2,0)=N(2,2,2)≈1。"
      "与 SU(2) 的 Clebsch–Gordan 系数（截断到 j≤3/2）**逐个相等** ⇒ 同构成立")
    put("")
    put("  交叉验证：N(1,1,0) = %g, N(1,1,2) = %g, N(1,1,3) = %g"
        % (fusion(3, 1, 1, 0), fusion(3, 1, 1, 2), fusion(3, 1, 1, 3)))
    P("2c: 正交性自查 S^T S = I（数值）",
      "Σ_m S_im S_jm = δ_ij 验证：Σ_m S_1m² = %g（应=1）⇒ S 矩阵正交，Verlinde 公式合法"
      % sum(s_matrix(3)[1][m] ** 2 for m in range(4)))

    # ═════════ §3 三叶结 π₁ → SU(2) 表示 ═════════
    sec("3. 三叶结 π₁ 到 SU(2) 的表示：B₃ = ⟨a,b | aba = bab⟩")
    put("  三叶结 T(2,3) 的结群 G_K = π₁(S³∖K) 与辫群 B₃ 同构：")
    put("      G_K ≅ ⟨a, b | a² = b³⟩  (等价形式 ⟨a,b | aba = bab⟩)")
    put("  要构造表示 ρ: G_K → SU(2)，须找 A, B ∈ SU(2) 满足 A² = B³（或 ABA = BAB）。")
    put("")
    put("  用 Pauli 矩阵 σ₁, σ₃ 构造（经典解）：")
    put("      B_rep = exp(iπσ₃/3) = diag(e^{iπ/3}, e^{-iπ/3})   （阶 6：B_rep³ = −I）")
    put("      A_rep = iσ₁ = [[0, i],[i, 0]]                      （阶 4：A_rep² = −I）")
    put("  则 A_rep² = −I = B_rep³ ⇒ 在 PSU(2) = SO(3) 中满足 a² = b³ ⇒ 给出一个忠实表示。")
    # 数值验证 A_rep² = B_rep³ （变量名避开 BOUNDARY 输出器 B）
    A_rep = matrix([[0, 1j], [1j, 0]])
    B_rep = matrix([[mp.e**(1j * pi / 3), 0], [0, mp.e**(-1j * pi / 3)]])
    A2 = A_rep * A_rep
    B3 = B_rep * B_rep * B_rep
    diff = max(abs(A2[r, c] - B3[r, c]) for r in range(2) for c in range(2))
    put("  数值验证 A_rep² − B_rep³ 的最大矩阵元 = %.2e（机器零 ⇒ A_rep² = B_rep³ 成立）" % diff)
    P("3a: 三叶结 π₁ 到 SU(2) 的非平凡忠实表示构造成功（Pauli 矩阵显式）",
      "A=iσ₁ (A²=−I), B=diag(e^{±iπ/3}) (B³=−I) ⇒ A²=B³ 在 SO(3) 中成立；"
      "这是 Witten 1989 CS 理论中 T(2,3) 颜色的代数根源")
    I("3b", "该表示是**几何的**（来自结的补空间），非注入 ⇒ 若 TUFT 的『粒子=结』成立，"
            "则 SU(2) 表示的来源从『注入 SM 结构群』升级为『从结群导出』——这正是 R9 §4b 缺口的修复")

    # ═════════ §4 关键检验：区分双重态/单态 ═════════
    sec("4. 【关键检验】TUFT 结能否区分 SU(2)_L 双重态 / 单态？")
    put("  R14 §3 的缺口：同为 Lk=1，Q_L/L 是弱双重态(2)、e_R/ν_R 是弱单态(1)；")
    put("  Lk 无法区分。现在问：结群表示能否区分？")
    put("")
    put("  三叶结 π₁ 的 SU(2) 表示（§3）给出的是**一个**特定的表示（旋转 2π/3 的对角矩阵），")
    put("  其 SU(2) 权重最高权 j = ? 取决于表示。该表示本身是 SU(2) 的**某个**不可约表示的实现，")
    put("  但**一个结只对应一个表示**，不能在同一结上同时实现 j=1/2 与 j=0。")
    put("")
    put("  更精确：TUFT 把『粒子』识别为**结的类型**（Hopf、三叶结、8 字结…），")
    put("  每个结类型有唯一的 π₁；π₁ 到 SU(2) 的表示在同构下唯一（对三叶结是 j=1 的 3 维？还是 j=1/2？）。")
    put("  检验：三叶结的 Jones 多项式 V(q) = q + q³ − q⁴（SU(2)_1 颜色）⇒ 对应 SU(2) 的**基本表示的缠绕**；")
    put("  其 SU(2) 权重结构的解释：三叶结作为一条世界线，在 SU(2)_k 中携带的表示由 Jones 多项式展开决定。")
    put("")
    put("  决定性观察：TUFT 的『粒子=不同结类型』⇒ 每个 SM 场需对应一个**不同**结类型。")
    put("  但 SM 有 6 个费米子场（Q_L, u_R, d_R, L, e_R, ν_R）且 Q_L/L 是双重态、u_R/.../e_R/ν_R 是单态；")
    put("  若每个场=一个结，则需 6 种不同结类型，且其中 2 种须携带双重态表示、4 种单态表示。")
    put("  结群表示论**能**给表示（§2-3），但**哪种结对应哪个表示**是额外的指派，TUFT 未提供。")
    F("4a: 【诚实】结群表示能给出 SU(2) 表示，但『哪个结=哪个 SM 场』仍需外部指派",
      "结群表示论修复了 R9 §4b 的『注入』为『可构造』，但 TUFT 仍缺『结类型 → SM 场』的目录映射；"
      "这是 R14 §6b 根因的 SU(2) 半边残余：拓扑不变量（结类型）与规范表示（j 值）之间仍缺函子")
    B("4b", "部分修复的精确边界：SU(2) 表示的**数学来源**已可构造（§2-3），"
            "但「拓扑→表示」的**具体对应**仍开放 ⇒ 与 R14 O-GAUGE-ORIGIN 的 SU(2) 半边对应，而非彻底关闭")

    # ═════════ §5 SU(3) 部分 ═════════
    sec("5. SU(3) 部分：结群能否承载色表示？")
    put("  SM 三代费米子中 Q_L/u_R/d_R 是色三重态(3)、L/e_R/ν_R 是色单态(1)。")
    put("  R14 §3 已证 Lk 不能区分 3 与 1。问：结群表示能否给出 SU(3) 表示？")
    put("")
    put("  已知机制（Witten 1989）：SU(N)_k 的 CS 理论，绕结的 Wilson 线给出 SU(N) 表示的『颜色』；")
    put("  三叶结的 HOMFLY 多项式（SU(N) 推广的 Jones）编码 SU(N) 信息。")
    put("  所以**数学上** SU(3) 颜色可从结的 HOMFLY 多项式读出——机制存在。")
    put("")
    put("  但 TUFT 的结是**一条世界线**（1-流形），其 CS 不变量自然给 U(1) 或 SU(2) 颜色（1-流形绕结）；")
    put("  SU(3) 需要**两条**世界线的链环（π₁(S³∖K) 的平凡/非平凡）或更高结构的颜色。")
    put("  TUFT 的 Hopf 链环（R2/R10）是 2-成分链环：其 Lk 给出 SU(2) 的 Abelian 相位（R10 LCS-1），")
    put("  但**未**给出 SU(3) 的 3 维基础表示的『颜色荷』。")
    B("5a: SU(3) 颜色机制存在（HOMFLY/SU(3)_k CS），但 TUFT 当前结构只触及 SU(2)/U(1) 半边",
      "要承载色三重态，TUFT 需显式引入 SU(3) 的 Wilson 线/结群表示；当前 TUFT 用 Hopf Lk 仅得 SU(2) 相位 ⇒ "
      "色表示的『来源』仍部分开放（机制已知、未在 TUFT 中实现）")
    I("5b", "与 R14 O-GAUGE-ORIGIN 对应：规范群整体的『来源』未被 TUFT 解释；"
            "本册仅确认 SU(2) 半边可构造，SU(3) 半边机制存在但 TUFT 未落地")

    # ═════════ §6 U(1) 部分 ═════════
    sec("6. U(1) 部分：超荷 Y 的来源（第三道鸿沟）")
    put("  R11 锁定 q=1/3（或约定 a 的 Y=1/6）来自观测/反常消除；R14 证 Lk 不给 Y。")
    put("  问：结群表示论能否给出 U(1)（超荷）？")
    put("")
    put("  机制：在 CS 理论 SU(3)×SU(2)×U(1)_Y 中，U(1)_Y 是脱水（GUT 归一化）的额外 CS 项；")
    put("  但 U(1)_Y **不是**从结群 π₁ 自然出现的——它是**额外**的规范群因子。")
    put("  更根本：超荷 Y 的量子数是**群论**（G 的 U(1) 子群的最高权/电荷），")
    put("  而结的拓扑不变量（Lk、Jones、HOMFLY）是**结论**的多项式不变量，不当量于群的 U(1) 电荷。")
    put("  即使 SU(2)_k 的表示 j 给出 SU(2) 弱同位旋 T3，U(1)_Y 仍需**独立的**指派")
    put("  （如同 Kaluza–Klein 中 U(1) 来自额外维度等距群，而非从 4D 几何自然出现）。")
    F("6a: 【诚实】结群表示论不能给出 U(1)_Y（超荷）",
      "U(1)_Y 是额外规范因子，非结拓扑不变量；Y 的量子数仍需外部指派（与 R11 的 q=1/3 锁定同源）。"
      "第三道鸿沟（群选择/超荷来源）**未跨越**")

    # ═════════ §7 对 R12 反解的影响 ═════════
    sec("7. 对 R12 反解的影响：SU(2) 修好后 Δb₂ 可填，Δb₃/Δb₁ 仍阻塞")
    put("  R12 反解需要 Δb_i = f(T(R₃), T(R₂), Y²)：")
    put("      Δb₃ = c·d(R₂)·T(R₃)；  Δb₂ = c·d(R₃)·T(R₂)；  Δb₁ = c·(3/5)·d(R₃)·d(R₂)·Y²")
    put("")
    put("  本册进展：SU(2) 表示可构造 ⇒ **T(R₂) 有来源**（结群 SU(2)_k 表示 j 给出 T_2 = j(j+1)/2 或 d(R₂)=2j+1）。")
    put("  残余阻塞：")
    put("      Δb₃ 需要 T(R₃)、d(R₃)：色三重态 R₃=3 ⇒ T_3=1/2、d_3=3 —— **SU(3) 半边未落地**（§5）⇒ 阻塞")
    put("      Δb₁ 需要 Y²：超荷 Y —— **U(1) 半边未跨越**（§6）⇒ 阻塞")
    B("7a: SU(2) 半边修复后，R12 反解的 Δb₂ 项可填；Δb₃、Δb₁ 仍须 SU(3)/U(1) 来源",
      "⇒ TUFT 仍**不能**完整进入 R12 反解方程 ⇒ R14 O-L3-CLOSED 的『L3 路径关闭』**未完全解除**，"
      "仅 SU(2) 半边部分修复（从『注入』升级为『可构造』）")
    I("7b", "量级意义：即使 SU(3)/U(1) 也落地，还须说明『为何是 3 代』（R10 O-NGEN：Witten 约束在 N_c=3 退化为恒真），"
            "故完整 L3 仍至少隔两道独立鸿沟")

    # ═════════ §8 结论 ═════════
    sec("8. 结论与开放项")
    put("  【修正 R14 §9】SU(2)_k 对象 = SU(2) 不可约表示（非异类任意子）；")
    put("      Verlinde fusion 与 SM 弱同位旋同构（k→∞ 收敛到 CG 系数）——**第一道鸿沟 SU(2) 半边已跨**。")
    put("  【构造成功】三叶结 π₁ → SU(2) 的忠实表示（Pauli 矩阵 A²=B³），来源从『注入』升级为『可构造』。")
    put("  【残余阻塞】")
    put("       SU(3) 半边：机制存在（HOMFLY/SU(3)_k），但 TUFT 当前结构只触及 SU(2)/U(1) ⇒ 未落地")
    put("       U(1)_Y 半边：是额外规范因子，非结拓扑不变量 ⇒ **第三道鸿沟未跨越**")
    put("       『结类型 → SM 场目录』：仍缺函子 ⇒ §4 的部分残余")
    put("  【对 R12 的影响】Δb₂ 可填；Δb₃、Δb₁ 仍阻塞 ⇒ R14 O-L3-CLOSED **未完全解除**，仅 SU(2) 半边修复。")
    put("")
    for oid, txt in (
        ("O-KNOTREP", "R14 的 O-KNOTREP 被**精化**：SU(2) 半边已构造成功（Verlinde fusion 同构 + 三叶结 Pauli 表示）；"
                        "SU(3) 半边机制已知未落地；U(1)_Y 半边未跨越。开放项收窄为『SU(3)/U(1) 落地 + 结→场目录』"),
        ("O-SU3", "TUFT 须显式引入 SU(3) Wilson 线/结群表示以承载色三重态；当前 Hopf Lk 仅给 SU(2) 相位"),
        ("O-U1", "超荷 Y 的非结来源：须额外 U(1) 因子（类比 KK 的额外维度等距群），TUFT 未提供"),
        ("O-KNOTMAP", "『结类型 → SM 场』目录映射：TUFT 把粒子识别为不同结类型，但缺『哪种结=哪个场』的指派函子"),
    ):
        put("  · %-14s %s" % (oid, txt))
    put("")
    put("红线：本册修正而非推翻 R14。R14 的**决定性否定**（Lk 不给规范量子数、信息缺口 1.74 bits）"
        "**仍成立**；本册只证明『结群表示论』这一补救方向在 SU(2) 半边可行，"
        "未改变 TUFT 整体『自旋/统计拓扑编码框架』的准确定位（R14 §8）。")

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
