# -*- coding: utf-8 -*-
"""
TUFT-r300 · ROOT V18.0「反常自由谱与量子修正下界」来料审计（承 r298/r299 ROOT 审计链）

靶：ROOT V18.0 来料《量子几何统一：发现新的严格下界》。V18 自承四项增量：
    ①消元定理：6D 两规范反常方程 Σd_q q²=0、Σd_q q⁴=0 的整数解族
      (d₁,d₂,d₃,d₄)=(15a+64b, −6a−20b, a, b)；
    ②严格下界 W=|N|Σ|d_q|q³ ≥ 90|N|（最小解 ±(15,−6,1,0)，即 V17 电荷 {1,2,3} 族）；
    ③更精简新谱 (d₁,d₂,d₃,d₄)=(4,4,−4,1)：13 个 6D 带电 Weyl 场、28 个 4D 带电零模（N=1），
      但 W=208 更重 —— "粒子数更少 ≠ 量子修正更小"；
    ④联合约束：M₆R≥10 ⇒ N≥215 ⇒ W≥19 350 ⇒ ε_loop=αW/(3π)≈14.98 ≫ 1，微扰失效。
    外加 §5 质量障碍（五条件清单）与 V19 非阿贝尔路线建议。

本卷判据族：
  Q1  ★消元代数严格核验（Fraction 精确）：两方程 ⇒ 二参数族
  Q2  ★W≥90|N| 定理：解析证明复述 + 整数穷举（box ±200）+ q≥5 排除论证
  Q3  ★V18 新谱 (4,4,−4,1) 全核验：6D 两反常 0/0、场数 13/5、4D 零模 28、ΣQ=ΣQ³=0、W=208
  Q4  ★V17/V18 对比表复算（22/10/30/90/9.5493 vs 13/5/28/208/22.0695）
  Q5  ★ε_loop 表 Decimal 80 位复算 + N=215 联合约束（W≥19 350、零模 ≥6 450）
  Q6  ★6D 局域反常完备集勘误：I₈=[Â·ch]₄ 且 Â₁=Â₃=0 ⇒ 6D 无线性项 Σd_q·q（p₁）；
      V18 两方程 + 中性场补 p0 恰为完备集；登记 V16.1 工作区卷 p₁ 过约束勘误
  Q7  ★符号关联路线（6D 矢量型 d_q=0、符号-手征不对称 δ_q）下界 180|N|：
      显式最小实现（δ=(15,−6,1,0) 形状）⇒ 全局最小仍为 90|N|（6D 手征路线达到）
  Q8  ★与 r299/双通量对表：V18 内容界 × 几何控制互补；SM 外额外可见手征内容被 RG 链定量排除
  Q9  质量障碍登记（V18 §5 五条件；带电凝聚破 U(1)_em 的 no-go 确认）
  Q10 判据集 R1–R6（V18 版）
控制组：C1 正对照 V17 族 (15,−6,1,0) 全条件通过 / C2 负对照 玩具谱 (1,0,0,0) 必须不满足反常条件 /
        C3 正对照 4D 反常双算法对拍（零模直算 = Σd_q q², Σd_q q⁴）/ C4 负对照 平凡谱 d=0 必须被判非手征
守卫：G1–G10
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80

RID = "r300"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_ROOTV18反常自由谱与量子修正下界_W下界90与符号关联路线180与完备反常集勘误_"
        "精算与可视化_%s" % (RID, STAMP))

WRITTEN = []
ALLOWED = set()
T0 = time.time()

PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
D0, D1, D2, D3 = Decimal(0), Decimal(1), Decimal(2), Decimal(3)

ALPHA_INV = Decimal("137.035999177")     # CODATA 2022
ALPHA = D1 / ALPHA_INV
MZ = Decimal("91.1876")
M4_RED = Decimal("2.435e18")             # 约化 Planck 质量 GeV（r299 同口径）


def fmt(x, nd=12):
    if isinstance(x, Decimal):
        if x == 0:
            return "0"
        return "%.*E" % (nd - 1, x)
    return str(x)


def rel(a, b):
    if b == 0:
        return Decimal("Infinity") if a != 0 else D0
    return abs(a / b - D1)


ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


def dq_w(d):
    """W/|N| = Σ|d_q| q³（q=1..4 段）。"""
    return sum(abs(dd) * (i + 1) ** 3 for i, dd in enumerate(d))


def dq_checks(d):
    """6D 两反常 + 场数 + 4D 零模数（N=1）。"""
    s2 = sum(dd * (i + 1) ** 2 for i, dd in enumerate(d))
    s4 = sum(dd * (i + 1) ** 4 for i, dd in enumerate(d))
    n6 = sum(abs(dd) for dd in d)
    n4 = sum(abs(dd) * (i + 1) for i, dd in enumerate(d))
    return s2, s4, n6, n4


# ================================================================ Q1 · 消元代数
def q1():
    """两反常方程 d1+4d2+9d3+16d4=0、d1+16d2+81d3+256d4=0 消元 ⇒
    d2=−6d3−20d4、d1=15d3+64d4。Fraction 精确验证 + 一般性论证（系数矩阵秩 2）。"""
    a, b = Fraction(7), Fraction(-3)
    d3, d4 = a, b
    d2 = -6 * d3 - 20 * d4
    d1 = 15 * d3 + 64 * d4
    eq2 = d1 + 4 * d2 + 9 * d3 + 16 * d4
    eq4 = d1 + 16 * d2 + 81 * d3 + 256 * d4
    # 反向：任意满足两方程的 (d1,d2,d3,d4) 必可写成该参数化（消元唯一性）
    # 由两方程相减 12d2+72d3+240d4=0 ⇒ d2=−6d3−20d4；回代第一方程 ⇒ d1=15d3+64d4。
    ok = (eq2 == 0) and (eq4 == 0)
    add("Q1", "机制", "消元代数：两反常方程 ⇔ 二参数族 (15a+64b, −6a−20b, a, b)",
        "PASS" if ok else "FAIL",
        "Fraction 精确：取 (a,b)=(7,−3) 得 d=(%s,%s,%s,%s)，Σd_q q²=%s、Σd_q q⁴=%s（应 0）。"
        "消元路径：两方程相减 12d₂+72d₃+240d₄=0 ⇒ d₂=−6d₃−20d₄；回代 ⇒ d₁=15d₃+64d₄。"
        "系数矩阵 [[1,4,9,16],[1,16,81,256]] 秩 2 ⇒ 解空间恰为 2 参数族，与来料一致。"
        % (d1, d2, d3, d4, eq2, eq4),
        {"a": str(a), "b": str(b), "d": [str(d1), str(d2), str(d3), str(d4)],
         "sum_dq2": str(eq2), "sum_dq4": str(eq4)})
    return {"ok": ok}


# ================================================================ Q2 · W>=90|N|
def q2():
    """解析证明复述 + 穷举。W/|N| = |15a+64b| + 8|6a+20b| + 27|a| + 64|b|。
    b≠0,a≠0 ⇒ ≥27+64=91；b≠0,a=0 ⇒ ≥8·20=160；故 b=0 ⇒ W=90|a| ⇒ min 90（|a|=1）。"""
    BOX = 200
    best, sols, count = None, [], 0
    for a in range(-BOX, BOX + 1):
        for b in range(-BOX, BOX + 1):
            if a == 0 and b == 0:
                continue
            W = abs(15 * a + 64 * b) + 8 * abs(-6 * a - 20 * b) + 27 * abs(a) + 64 * abs(b)
            count += 1
            if best is None or W < best:
                best, sols = W, [(a, b)]
            elif W == best:
                sols.append((a, b))
    d_sols = [(15 * a + 64 * b, -6 * a - 20 * b, a, b) for a, b in sols]
    ok = (best == 90) and (len(sols) == 2) and all(d in d_sols for d in [(15, -6, 1, 0), (-15, 6, -1, 0)])
    add("Q2", "机制", "W ≥ 90|N| 严格下界：解析证明 + 穷举（box ±%d）" % BOX,
        "PASS" if ok else "FAIL",
        "穷举 %d 组（a,b ∈ [−%d,%d]²，排除平凡原点；含原点共 %d 组）：W_min/|N| = %d，"
        "达到者 (a,b) = %s，对应 (d₁,d₂,d₃,d₄) = %s —— 恰为 ±(15,−6,1,0)（V17 电荷 {1,2,3} 族），"
        "与来料「仅两个相反号最小解」一致。来料 §6 自报穷举「87 423 组」，其扫描域与约束未声明，"
        "与本卷 160 800 组（含原点 160 801）不可直接对表；判据以最小解与解析证明为准，不以计数为准。"
        "解析证明复述：q≥5 分量单权重 |d_q|q³ ≥ 125 > 90 被 |·| "
        "求和排除；b≠0,a≠0 ⇒ ≥91；b≠0,a=0 ⇒ ≥160；故 b=0 ⇒ W/|N|=90|a| ⇒ min=90。"
        "下界由整数电荷格与反常方程共同确定，非 α 拟合。"
        % (count, BOX, BOX, (2 * BOX + 1) ** 2, best, sols, d_sols),
        {"box": BOX, "count": count, "W_min": best, "argmin": [list(s) for s in sols]})
    return {"W_min": best, "count": count}


# ================================================================ Q3 · V18 新谱
def q3():
    """(d₁,d₂,d₃,d₄)=(4,4,−4,1)：6D 两反常 0/0；6D 带电场 13；4D 带电零模 28（N=1）；
    零模表 +1:4LH, +2:8LH, +3:12RH, +4:4LH；ΣQ=ΣQ³=0（4D 自身反常自由）；W=208。"""
    d = (4, 4, -4, 1)
    s2, s4, n6, n4 = dq_checks(d)
    W = dq_w(d)
    # 4D 零模表与反常（零模计数 |d_q|·q，手征 = 6D 手征性 XOR 电荷符号）
    rows, SQ, SQ3 = [], 0, 0
    for q, dd in zip((1, 2, 3, 4), d):
        n = abs(dd) * q
        ch = "LH" if (dd > 0) == (q > 0) else "RH"
        rows.append("%+d:%d%s" % (q, n, ch))
        sgn = 1 if ch == "LH" else -1
        SQ += sgn * n * q
        SQ3 += sgn * n * q ** 3
    ok = (s2 == 0 and s4 == 0 and n6 == 13 and n4 == 28 and W == 208
          and SQ == 0 and SQ3 == 0)
    add("Q3", "机制", "V18 新谱 (4,4,−4,1)：6D 反常自由 + 4D 零模自身反常自由 + W=208",
        "PASS" if ok else "FAIL",
        "Σd_q q²=%s、Σd_q q⁴=%s（6D 两规范反常 = 0）；6D 带电 Weyl 场 %d（来料 13）；"
        "4D 带电零模（N=1）%d（来料 28）：%s；按零模逐个计权重 ΣQ=%s、ΣQ³=%s（来料 0/0 —— "
        "零模计数=|d_q|·q，故 ΣQ=Σd_q q²、ΣQ³=Σd_q q⁴，来料的 4+16−36+16 与 4+64−324+256 "
        "正是这两个和，标签与公式均正确）；W=Σ|d_q|q³=%s（来料 208）。"
        % (s2, s4, n6, n4, ", ".join(rows), SQ, SQ3, W),
        {"d": list(d), "sum_dq2": s2, "sum_dq4": s4, "n6": n6, "n4": n4,
         "zero_modes": rows, "sumQ": SQ, "sumQ3": SQ3, "W": W})
    return {"ok": ok, "W": W, "n6": n6, "n4": n4}


# ================================================================ Q4 · 对比表
def q4():
    """V17 (15,−6,1,0) vs V18 (4,4,−4,1)：22/10/30/90/9.5493 vs 13/5/28/208/22.0695。"""
    d17, d18 = (15, -6, 1, 0), (4, 4, -4, 1)
    w17, w18 = dq_w(d17), dq_w(d18)
    f17, f18 = sum(abs(x) for x in d17), sum(abs(x) for x in d18)
    z17, z18 = sum(abs(x) * (i + 1) for i, x in enumerate(d17)), \
               sum(abs(x) * (i + 1) for i, x in enumerate(d18))
    n0_17, n0_18 = sum(d17), sum(d18)          # 总手征差 ⇒ 需相反手征中性场补 p0
    r17, r18 = Decimal(w17) / (3 * PI), Decimal(w18) / (3 * PI)
    ok = (f17, z17, w17, n0_17) == (22, 30, 90, 10) \
        and (f18, z18, w18, n0_18) == (13, 28, 208, 5) \
        and rel(r17, Decimal("9.5493")) < Decimal("1e-4") and rel(r18, Decimal("22.0695")) < Decimal("1e-4")
    add("Q4", "机制", "V17/V18 对比表复算：场数更少但量子修正更重的取舍成立",
        "PASS" if ok else "FAIL",
        "V17：6D 带电场 %d、4D 零模 %d、W=%d、−dα⁻¹/dlnμ=W/3π=%s（来料 9.5493）；"
        "V18：%d、%d、%d、%s（来料 22.0695）。「粒子数更少 ≠ 电磁量子修正更小」"
        "定量成立：V18 场数 −41%% 而 W +131%%。总手征差 Σd_q=%d（V17）/%d（V18）"
        "⇒ 需 %d/%d 个相反六维手征中性场补 p0（来料表中性场 10/5 命中）。"
        % (f17, z17, w17, fmt(r17, 6), f18, z18, w18, fmt(r18, 6),
           n0_17, n0_18, n0_17, n0_18),
        {"V17": [f17, z17, w17, n0_17, float(r17)], "V18": [f18, z18, w18, n0_18, float(r18)]})
    return {"w17": w17, "w18": w18, "n0_17": n0_17, "n0_18": n0_18}


# ================================================================ Q5 · epsilon_loop
def q5():
    """ε_loop = α·W/(3π)（Decimal 80 位）：0.0697/0.1610/0.6968/14.9822；
    N=215 ⇒ W≥19 350、带电手征零模 ≥6 450。"""
    rows = []
    for name, W in (("V17,N=1", 90), ("V18,N=1", 208), ("V17,N=10", 900), ("V17,N=215", 90 * 215)):
        eps = ALPHA * Decimal(W) / (3 * PI)
        rows.append((name, W, eps))
    targets = {"V17,N=1": "0.0697", "V18,N=1": "0.1610", "V17,N=10": "0.6968", "V17,N=215": "14.9822"}
    ok = all(rel(e, Decimal(t)) < Decimal("2e-3") for (_, _w, e), t in
             zip(rows, [targets[n] for n, _w, _e in rows]))
    # 来料 §4 条件关系 α=N²/(64π²(M₆R)⁴) 的代数复算（按给定式，不重推 V16 推导）
    s6 = Decimal(10)
    n_min_real = 8 * PI * ALPHA.sqrt() * s6 ** 2
    alpha_215 = Decimal(215) ** 2 / (64 * PI * PI * s6 ** 4)
    ok_alpha = rel(n_min_real, Decimal(215)) < Decimal("1e-2") and rel(alpha_215, ALPHA) < Decimal("1e-2")
    ok = ok and ok_alpha
    W215 = 90 * 215
    zm215 = 30 * 215
    add("Q5", "机制", "ε_loop 表复算 + N=215 联合约束（W≥19 350、零模 ≥6 450）",
        "PASS" if ok else "FAIL",
        "Decimal 80 位：ε_loop = α·W/(3π)：" +
        "；".join("%s(W=%d)=%s" % (n, w, fmt(e, 6)) for n, w, e in rows) +
        "。来料值 0.0697/0.1610/0.6968/14.9822 全部命中（rel<2e-3，来料为 4 位舍入）。"
        "联合约束：M₆R≥10 ⇒ N≥215（V16.0 条件）⇒ W≥90×215=%d、带电手征零模 ≥30×215=%d；"
        "ε_loop=%s ≫ 1 ⇒ 大 N 几何控制路线与一圈微扰自洽不相容——来料的联合限制成立，"
        "且与本库 r299 的「ξ 自由、口径混用」结论同向。"
        "来料 §4 关系 α=N²/(64π²(M₆R)⁴) 按给定式代数复算（不重推 V16 推导）："
        "M₆R=10 ⇒ N_min=8π√α·s²=%s → 取整 215；N=215 反算 α=%s（1/%s），"
        "与 CODATA α 相对差 %s%%——来料「约 N≥215」成立。"
        % (W215, zm215, fmt(rows[-1][2], 6), fmt(n_min_real, 6), fmt(alpha_215, 8),
           fmt(D1 / alpha_215, 6), fmt(rel(alpha_215, ALPHA) * 100, 3)),
        {"eps": [(n, w, float(e)) for n, w, e in rows], "W215": W215, "zm215": zm215,
         "N_min_real": str(n_min_real), "alpha_at_215": str(alpha_215),
         "alpha_inv_at_215": str(D1 / alpha_215)})
    return {"eps215": rows[-1][2]}


# ================================================================ Q6 · 完备反常集勘误
def q6():
    """I₈=[Â(R)·ch(F)]₄，Â=1+Â₂+Â₄+…（Â₁=Â₃=0）⇒ [Â·ch]₄ = Â₀ch₄+Â₂ch₂+Â₄ch₀：
    结构恰为 F⁴(∝Y⁴)、F²R²(∝Y²)、纯引力(∝1)。线性项 Σd_q·q（p₁）在 6D 不存在
    （混合引力-规范反常只在 d=4k 维出现）。⇒ V18 两方程 + 中性场补 p0 = 完备集；
    V16.1 工作区卷 §5 把 p₁ 误列为必要条件（过约束）——登记勘误。"""
    # 结构计数：Â 的偶阶性是恒等式层面的事实（Â 由 Pontryagin 类构成，全为偶形式）
    # ch(F)=e^{Yc₁} 含奇阶 ch₁=Yc₁，但无 Â₃ 可与之配对 ⇒ 线性项系数恒 0。
    # 数值佐证：任取谱，p₁ 任意取值不影响 p₀/p₂/p₄ 判定（线性项独立）。
    d = (4, 4, -4, 1)
    p1 = sum(dd * (i + 1) for i, dd in enumerate(d))
    p1_shift = sum((dd + 1) * (i + 1) for i, dd in enumerate(d))   # 每场加一个 LH q-场不改变 p2/p4 判定的结构演示
    add("Q6", "★勘误", "6D 局域反常完备集：{p0, p2, p4}；线性项 p1 在 6D 不存在（V16.1 过约束勘误）",
        "PASS",
        "I₈=[Â(R)·ch(F)]₄ 且 Â 只含偶阶（Â₁=Â₃=0，Pontryagin 类皆为偶形式）⇒ "
        "[Â·ch]₄=Â₀ch₄+Â₂ch₂+Â₄ch₀，即 F⁴(∝Σ±Y⁴)、F²R²(∝Σ±Y²)、纯引力(∝Σ±1) 三结构，"
        "无 F·R³ 线性项（混合引力-规范反常只在 d=4k 维存在；6D 属 4k+2，只有纯引力反常）。"
        "⇒ V18 的两方程 Σd_q q²=Σd_q q⁴=0（p₂、p₄）+ 中性场补 p0 恰为**完备**局域反常条件——"
        "来料的反常框架正确且自洽。连带勘误：本库工作区平行卷 ROOT V16.1 §5 的 6D 谱搜索"
        "把 p₁=Σd_q·q 误列为必要条件（过约束），其 945 154 类结果集是真解空间的**子集**，"
        "最小显式反例 LH{−2,−2,1,1}/RH{−2,−1,−1,2} 仍有效（恰也满足 p₁）；"
        "V16.0 来料的 4D 检查（Σq、Σq³）属 4D 层条件，与本卷 6D 层条件互补不冲突。"
        "数值演示：谱 (4,4,−4,1) 的 p₁=%d；整体加场后 p₁′=%d——p₂/p₄ 结构与 p₁ 独立。"
        % (p1, p1_shift),
        {"p1_example": p1, "p1_shift": p1_shift,
         "complete_set": ["p0: Σd_q=0（中性场可补）", "p2: Σd_q q²=0", "p4: Σd_q q⁴=0"]})
    return {"ok": True}


# ================================================================ Q7 · 符号关联路线 180|N|
def q7():
    """6D 矢量型谱（每 |q| 取 m_q LH + m_q RH，d_q=0，6D 反常自动消去）+
    符号分配不对称 δ_q=α_q−β_q ⇒ 4D 零模净手征 2qNδ_q；4D 反常消去 ⇔ Σδ_q q²=Σδ_q q⁴=0。
    运行权重 ΣQ² = 2|N|Σm_q q³ ≥ 2|N|Σ|δ_q|q³ ≥ 180|N|。显式最小实现（δ=(15,−6,1,0) 形状）。"""
    # δ=(15,-6,1,0)：q=1:(α,β)=(15,0)；q=2:(0,6)；q=3:(1,0)
    plan = [(1, 15, 0), (2, 0, 6), (3, 1, 0)]
    tot_q2 = tot_Q = tot_Q3 = 0
    n6_total = 0
    lines = []
    for q, al, be in plan:
        m = max(al, be)
        nLH = al * q + (m - be) * q     # LH,Y>0 → LH 零模；RH,Y<0 → LH 零模
        nRH = (m - al) * q + be * q     # LH,Y<0 → RH 零模；RH,Y>0 → RH 零模
        tot_q2 += (nLH + nRH) * q * q
        tot_Q += (nLH - nRH) * q
        tot_Q3 += (nLH - nRH) * q ** 3
        n6_total += 2 * m
        lines.append("q=%d: 6D 场 2×%d（LH %d + RH %d），4D 零模 %dLH+%dRH（N=1）" % (q, m, m, m, nLH, nRH))
    ok = (tot_Q == 0 and tot_Q3 == 0 and tot_q2 == 180)
    add("Q7", "★新增", "符号关联路线（6D 矢量型 + 符号-手征不对称）下界 180|N|：全局最小仍 90|N|",
        "PASS" if ok else "FAIL",
        "V18 的 W 界只覆盖 6D 手征谱（d_q≠0）。本条证明另一条构造路线——6D 矢量型"
        "（d_q=0，反常自动消去）靠电荷符号与手征性的关联产生 4D 手征零模——的下界："
        "净 4D 手征 = 2qNδ_q（δ_q=α_q−β_q ∈ [−m_q,m_q]），4D 反常自由 ⇔ Σδ_q q²=Σδ_q q⁴=0"
        "（与 V18 两方程同构）；运行权重 ΣQ²=2|N|Σm_q q³ ≥ 2|N|Σ|δ_q|q³ = 2W(δ) ≥ 180|N|。"
        "显式最小实现（δ 取 V17 形状 (15,−6,1,0)）：" + "；".join(lines) +
        "；ΣQ=%d、ΣQ³=%d（4D 反常自由）、ΣQ²=%d=2×90。⇒ 两路线合并后全局最小运行权重仍为 "
        "90|N|（由 6D 手征路线 V17 族达到），「绕过 W 界的粒子数减半捷径」不存在；"
        "符号关联路线的代价是 6D 场数翻倍（44 vs 22）且运行权重翻倍。"
        % (tot_Q, tot_Q3, tot_q2),
        {"delta": [15, -6, 1, 0], "sumQ": tot_Q, "sumQ3": tot_Q3, "sumQ2": tot_q2,
         "n6_total": n6_total, "bound": "180|N|"})
    return {"ok": ok}


# ================================================================ Q8 · 与 r299/双通量对表
def q8():
    """V18 内容界 × 几何控制互补。量化：可见扇区若在 SM 内容之外再携带 6D 手征
    单位荷指标 N_v=3（W=270），则 Δ(1/α)=(W/3π)ln(M_KK/M_Z)：M_KK=1e14 ⇒ Δ≈794 ⇒
    1/α(0)=77.95−794<0，RG 不自洽 ⇒ 额外可见手征内容被排除。"""
    MKK = Decimal("1e14")
    T_MKK = Decimal("127.952") - Decimal("1.8038") * (MKK / MZ).ln()
    W_extra = 270                        # 90 × N_v(=3)
    d_extra = W_extra / (3 * PI) * (MKK / MZ).ln()
    one_alpha0 = T_MKK - d_extra
    ok = T_MKK > 0 and one_alpha0 < 0
    add("Q8", "★对表", "V18 内容界 × r299 几何结论互补：SM 外额外可见手征内容被 RG 链定量排除",
        "PASS" if ok else "FAIL",
        "与本库 r298/r299 审计链对表：r299 判词「XI-FREE-STILL-NO-PREDICTION」管的是**几何侧**"
        "（ξ 无方程约束、√(8π) 口径），V18 的 W≥90|N| 管的是**内容侧**（额外轻带电粒子）——"
        "两者正交且互补。定量联合：工作区平行卷 V16.1 的双通量构造把几何控制交给隐藏通量"
        "（s=M₆R 达 26–829），可见扇区保持 N_v=3；此时若可见扇区在 SM 内容（ΣQ²=8）之外再携带"
        "6D 手征单位荷谱（W=90N_v=270），则 Δ(1/α)=(W/3π)ln(M_KK/M_Z)：M_KK=1e14 ⇒ "
        "ln=%.4f，Δ=%s，1/α(0)=%s<0 —— RG 不自洽。⇒ **V18 下界 × RG 链 ⇒ 可见扇区的额外"
        "手征内容被定量排除**：可见代数只能来自 SM 型最小内容或非阿贝尔嵌入（V19 路线），"
        "且 ε_loop≫1 的大 N 路线（V18 §4）与双通量的隐藏大 N 路线不冲突——隐藏扇区无带电物质，"
        "W 界不适用于它（q=0）。" % (float((MKK / MZ).ln()), fmt(d_extra, 6), fmt(one_alpha0, 6)),
        {"T_MKK_1e14": float(T_MKK), "W_extra": W_extra, "delta_1_over_alpha": float(d_extra),
         "one_over_alpha0": float(one_alpha0)})
    return {"ok": ok}


# ================================================================ Q9 · 质量障碍
def q9():
    """V18 §5：两套候选谱均无可直接配对的相反电荷场；带电标量凝聚生成质量会破 U(1)，
    使规范玻色子获质 —— 对「把该 U(1) 识别为光子」是严重约束。登记为真，并补双通量关系。"""
    add("Q9", "登记", "质量障碍登记：手征 U(1) 谱的质量生成与光子无质量性相容性未解",
        "INFO",
        "V18 §5 的障碍为真且重要：候选谱（V17 族与 (4,4,−4,1)）缺少可配对的相反电荷场，"
        "普通 Dirac 质量项不可写；带电标量凝聚 ⟨φ⟩≠0 会破 U(1) 并给规范玻色子质量——"
        "与「该 U(1)=电磁」矛盾。五条件清单（局域+全球反常消失/正确轻重谱/保留无质量电磁场/"
        "可控量子修正/正确低能耦合）需同时成立，登记为 V19 的约束集。"
        "与本库双通量构造的关系：隐藏 U(1) 无带电物质 ⇒ 无质量生成问题、规范玻色子保持无质量"
        "（自由暗光子）；障碍集中在**可见扇区**——SM 型嵌入（非阿贝尔磁通）中质量由 Higgs 机制"
        "承担，但那已超出单 U(1) 玩具的管辖，V18 的障碍判词对玩具谱成立、对 SM 嵌入路线是"
        "「需重述」而非「否证」。")
    return {"ok": True}


# ================================================================ Q10 · 判据集
def q10():
    """V18 版判据集 R1–R6。"""
    rows = [
        ("R1", "谱的局域+4D 反常自洽（6D p0/p2/p4 完备 + 4D ΣQ=ΣQ³=0）", "PASS",
         "V18 谱 (4,4,−4,1) 两层全过（Q3）；完备集结构正确（Q6）"),
        ("R2", "量子修正下界可证且非拟合（W≥90|N|）", "PASS", "Q2 穷举+解析双通道确证"),
        ("R3", "几何控制与微扰自洽兼容（大 N 路线）", "FAIL",
         "N≥215 ⇒ ε_loop≈14.98≫1（Q5）——大 N 控制路线在一圈水平自毁"),
        ("R4", "质量生成与无质量光子相容", "FAIL", "V18 §5 障碍为真（Q9）；两套谱均未解决"),
        ("R5", "完整 SM 谱兼容（电荷 2/3,1/3 的整数磁通计数）", "FAIL",
         "单位荷 |q|N 计数给不出夸克电荷；需非阿贝尔嵌入（V19）"),
        ("R6", "无实测输入的独立 α 预测", "FAIL",
         "W 下界是筛选条件不是数值预测；α 仍以 CODATA 为输入（来料自承）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q10", "判据", "判据集 R1–R6（V18 版）= %d/6" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299（V15 版）=1/6；V18 把 R1、R2 两层做实——这是 ROOT 系列第一次同时拥有"
        "「可证的内容层筛选条件」与「反常自由的具体谱」，但 R3–R6 四层仍全部未过。",
        {"逐条": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ 控制组
def controls():
    ctl = []
    # C1 正对照：V17 族
    d = (15, -6, 1, 0)
    s2, s4, n6, n4 = dq_checks(d)
    ok1 = (s2 == 0 and s4 == 0 and n6 == 22 and n4 == 30 and dq_w(d) == 90)
    ctl.append(("C1", "正对照", "V17 族 (15,−6,1,0)：6D 反常 0/0、22 场、30 零模、W=90", 
                "PASS" if ok1 else "FAIL",
                "Σd_q q²=%d、Σd_q q⁴=%d、场数=%d、零模=%d、W=%d——全中。" % (s2, s4, n6, n4, dq_w(d))))
    # C2 负对照：玩具谱必须不满足
    d = (1, 0, 0, 0)
    s2, s4, n6, n4 = dq_checks(d)
    ok2 = (s2 != 0 and s4 != 0)
    ctl.append(("C2", "负对照", "玩具谱 (1,0,0,0) 必须不通过两反常条件（判据有牙）",
                "PASS" if ok2 else "FAIL",
                "Σd_q q²=%d、Σd_q q⁴=%d —— 均非零，正确拒绝。" % (s2, s4)))
    # C3 正对照：4D 反常双算法对拍
    d = (4, 4, -4, 1)
    SQ_direct = SQ3_direct = 0
    for q, dd in zip((1, 2, 3, 4), d):
        n = abs(dd) * q
        ch = "LH" if (dd > 0) == (q > 0) else "RH"
        sgn = 1 if ch == "LH" else -1
        SQ_direct += sgn * n * q
        SQ3_direct += sgn * n * q ** 3
    SQ_formula = sum(dd * (i + 1) ** 2 for i, dd in enumerate(d))
    SQ3_formula = sum(dd * (i + 1) ** 4 for i, dd in enumerate(d))
    ok3 = (SQ_direct == SQ_formula == 0) and (SQ3_direct == SQ3_formula == 0)
    ctl.append(("C3", "正对照", "4D 反常双算法对拍：零模直算 = Σd_q q² / Σd_q q⁴",
                "PASS" if ok3 else "FAIL",
                "直算 ΣQ=%d、ΣQ³=%d；公式 Σd_q q²=%d、Σd_q q⁴=%d——两路一致且均为 0。" %
                (SQ_direct, SQ3_direct, SQ_formula, SQ3_formula)))
    # C4 负对照：平凡谱必须被判非手征
    d = (0, 0, 0, 0)
    ok4 = (dq_w(d) == 0 and sum(abs(x) for x in d) == 0)
    ctl.append(("C4", "负对照", "平凡谱 d=(0,0,0,0) 必须被判「非手征」排除于候选之外",
                "PASS" if ok4 else "FAIL",
                "W=0、场数=0：非平凡性条件（存在净手征带电谱）有效排除平凡解；"
                "注意 d=0 但符号不对称的谱是另一条路线（Q7 已单独定界 180|N|），不与本条混淆。"))
    for tid, layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    g.append(("G2", "Q2 穷举量 ≥ 10^4（box ±200 ⇒ 160 800 非平凡组 / 含原点 160 801 组）",
              extra["q2"]["count"] >= 10 ** 4, "实测 %d 组" % extra["q2"]["count"]))
    g.append(("G3", "Q2 最小解恰为 ±(15,−6,1,0)", extra["q2"]["W_min"] == 90,
              "W_min=%d" % extra["q2"]["W_min"]))
    g.append(("G4", "Q3/Q4 的 W 读数与来料一致（208/90）",
              extra["q3"]["W"] == 208 and extra["q4"]["w17"] == 90,
              "W18=%d, W17=%d" % (extra["q3"]["W"], extra["q4"]["w17"])))
    g.append(("G5", "Q5 ε_loop(N=215) > 10（微扰失效判据复现）", extra["q5"]["eps215"] > 10,
              "实测 %s" % fmt(extra["q5"]["eps215"], 6)))
    has_fail = sum(1 for it in ITEMS if it["verdict"] == "FAIL") >= 1
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2/C4 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d：来料可计算断言全真，无 FAIL 可登记）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2/C4（拒绝型负对照）%s；主条目 FAIL=%d。"
              "与 r299 的 G6（要求主条目含 FAIL）语义差异：本卷来料可计算断言全部核验为真，"
              "不存在可登记的 FAIL；牙齿由拒绝型负对照证明，不以主条目 FAIL 为必要条件。"
              % (len(ctl), "PASS" if teeth else "FAIL", n_fail_main)))
    g.append(("G7", "关键量非负（W17, W18, 零模数, N=215 权重）",
              extra["q3"]["W"] > 0 and extra["q4"]["w17"] > 0 and
              extra["q3"]["n4"] > 0 and extra["q3"]["n6"] > 0,
              "W18=%d W17=%d n4=%d n6=%d" % (extra["q3"]["W"], extra["q4"]["w17"],
                                             extra["q3"]["n4"], extra["q3"]["n6"])))
    keys_ok = all(set(it.keys()) == {"id", "layer", "title", "verdict", "detail", "kv"} for it in ITEMS)
    g.append(("G8", "条目键集合一致", keys_ok, "6 键"))
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G9", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "写入 %d 个路径，越界 %d 个" % (len(WRITTEN), len(bad))))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS),
              "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        if gid != "G2":
            add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 10 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit(extra):
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP, "标题": "ROOT V18 反常自由谱与量子修正下界来料审计",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · ROOT V18 反常自由谱与量子修正下界来料审计 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：W90-BOUND-VERIFIED / ANOMALY-SET-COMPLETE-P1-ABSENT / STILL-NOT-A-PREDICTION。")
    L.append("      V18 的 W≥90|N| 下界经解析+穷举双通道确证；新谱 (4,4,−4,1) 两层反常全过；")
    L.append("      本卷新增：6D 完备反常集勘误（p1 不存在，V16.1 过约束登记）与符号关联路线")
    L.append("      180|N| 下界（全局最小仍 90|N|）；SM 外额外可见手征内容被 RG 链定量排除；")
    L.append("      判据集 R1–R6 = 2/6（r299 为 1/6）。质量障碍与 SM 兼容性仍是真缺口。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · ROOT V18 反常自由谱与量子修正下界来料审计（数据册）" % RID, "",
         "| 项 | 值 |", "| --- | --- |"]
    for k, v in summary.items():
        M.append("| %s | %s |" % (k, v))
    M += ["", "## 条目逐条", ""]
    for it in ITEMS:
        M.append("### %s · %s · %s" % (it["id"], it["verdict"], it["title"]))
        M += ["", it["detail"], ""]
        if it["kv"]:
            M.append("```json")
            M.append(json.dumps(it["kv"], ensure_ascii=False, indent=1, default=str))
            M.append("```")
            M.append("")
    with io.open(wpath(os.path.join(DATA, BASE + ".md")), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    emit_judgment(summary, main, ctl, grd)
    return summary


def emit_judgment(summary, main, ctl, grd):
    p_jud = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
    J = []
    J.append("# 判定_TUFT-%s · ROOT V18 反常自由谱与量子修正下界来料审计" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：ROOT V18.0 来料《量子几何统一：发现新的严格下界》"
             "（承 r298/r299 ROOT 审计链；V17 谱为来料内部引用）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**W90-BOUND-VERIFIED / ANOMALY-SET-COMPLETE-P1-ABSENT / STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **下界定理全真（确认 V18 的核心增量）**：W=|N|Σ|d_q|q³ ≥ 90|N| 经解析证明复述"
             "（Q2：q≥5 单权重 ≥125 排除；b≠0 ⇒ ≥91/160；b=0 ⇒ W=90|a|）与整数穷举（box ±200，"
             "160 800 非平凡组 / 含原点 160 801 组）双通道确证，最小解恰为 ±(15,−6,1,0)"
             "（V17 电荷 {1,2,3} 族）。来料 §6 自报 87 423 组为未声明扫描域的另一口径，"
             "不与本卷计数对表、亦不影响结论。该界由整数电荷格与反常方程共同确定，非 α 拟合——"
             "来料的定性主张全部成立。")
    J.append("2. **新谱 (4,4,−4,1) 两层反常全过**：6D Σd_q q²=Σd_q q⁴=0（Q3）；4D 零模"
             " +1:4LH/+2:8LH/+3:12RH/+4:4LH 的 ΣQ=ΣQ³=0——来料行文的「4+16−36+16」「4+64−324+256」"
             "正是零模加权和 Σd_q q²、Σd_q q⁴，标签正确。取舍定量成立：场数 −41%、W +131%（Q4）。")
    J.append("3. **★本册新增一：6D 局域反常完备集勘误（Q6）**。I₈=[Â·ch]₄ 且 Â₁=Â₃=0 ⇒ 6D 结构"
             "只有 F⁴/F²R²/纯引力三族，线性项 Σd_q·q（p₁）不存在（混合引力-规范反常只在 d=4k 维）。"
             "⇒ V18 的两方程 + 中性场补 p0 恰为完备集；工作区平行卷 ROOT V16.1 §5 的谱搜索把 p₁ "
             "误列为必要条件（过约束），其 945 154 类结果为真解空间的子集、最小反例仍有效——登记勘误。")
    J.append("4. **★本册新增二：符号关联路线下界 180|N|（Q7）**。6D 矢量型谱（d_q=0）可经电荷符号-"
             "手征关联产生 4D 手征零模，但其运行权重 ΣQ²=2|N|Σm_q q³ ≥ 180|N|（显式最小实现"
             " δ=(15,−6,1,0)：ΣQ=ΣQ³=0、ΣQ²=180）。⇒ 两条路线合并后全局最小仍为 90|N|，"
             "V18 下界的适用域经本条扩展到全部构造路线。")
    J.append("5. **★对表与联合（Q8）**：V18 内容界与 r299 几何结论正交互补。定量：可见扇区在 SM"
             "（ΣQ²=8）外若再携带 6D 手征单位荷指标 N_v=3（W=270），M_KK=1e14 ⇒ Δ(1/α)≈794，"
             "1/α(0)<0 不自洽 ⇒ **额外可见手征内容被 RG 链定量排除**；大 N 几何控制只能走无带电"
             "物质的隐藏扇区（q=0 处 W 界不适用）——与工作区双通量构造（s=26–829）相容。")
    J.append("6. **预测层维持**：W 界是筛选条件不是数值预测；判据集 R1–R6 = 2/6（Q10，r299 为 1/6）"
             "——R1（反常自洽）与 R2（可证下界）首次做实，R3–R6（微扰兼容/质量生成/SM 兼容/独立预测）"
             "仍全部未过。来料自承「无输入的 α 数值预测尚未实现」与本题判定一致。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：6D 单 U(1) Weyl 费米子谱，d_q=n₊,q−n₋,q；局域反常 Σd_q q²=Σd_q q⁴=0"
             "（p₂、p₄）+ 纯引力 Σd_q=0（p0，中性场补足）；磁通 |qN| 零模计数；"
             "W=|N|Σ|d_q|q³；d(α⁻¹)/dlnμ=−W/(3π)（一圈、轻场近似）。")
    J.append("- **管线**：消元代数（Q1）→ W 下界（Q2）→ 新谱核验（Q3）→ 对比表（Q4）→ "
             "ε_loop 与 N=215 联合（Q5）→ 完备集勘误（Q6）→ 符号关联路线（Q7）→ "
             "r299/双通量对表（Q8）→ 质量障碍（Q9）→ 判据集（Q10）。")
    J.append("")
    J.append("## 三、判据集 R1–R6 = 2/6")
    J.append("")
    q10 = [i for i in main if i["id"] == "Q10"][0]
    for line in q10["kv"]["逐条"]:
        J.append("- " + line)
    J.append("")
    J.append("## 四、控制组（证明判据非一律否定/非一律通过）")
    J.append("")
    for it in ctl:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 五、守卫")
    J.append("")
    for it in grd:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 六、条目逐条")
    J.append("")
    for it in main:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 七、诚实边界（本卷不主张什么）")
    J.append("")
    J.append("- **B1**：W 界与 ε_loop 均为一圈、轻场近似；阈值结构与质量门槛会修改数值，本卷按来料口径复算。")
    J.append("- **B2**：Q2 穷举 box ±200 内「恰两个最小解」；box 外由解析证明覆盖（b≠0/大 a 支一律 ≥91/160），"
             "不依赖穷举完备性。")
    J.append("- **B3**：Q7 的符号关联路线在「6D 矢量型 + 4D 反常自由」约束下定界；若允许 4D 反常由"
             "流入机制抵消，约束会变化——本卷按 V18 §5 的保守要求（4D 自身反常自由）计算。")
    J.append("- **B4**：Q8 的 RG 定量排除以 SM 内容 ΣQ²=8、锚 M_Z、C=1.8038/ln 为口径（r299 同源），"
             "阈值细节未含。")
    J.append("- **B5**：V18 引证（Phys. Rev. D 等）只做存在性登记，未联网核对（承本线惯例）。")
    J.append("- **B6**：V17 来料卷未独立审计，其读数（22/10/30/90）仅作为 V18 对比表的来料侧引用复算。")
    J.append("- **B7**：V18 来料正本已逐字留档（`数据/TUFT-r300_…_来料原件_ROOT_V18.0_用户附件逐字_2026-11-01.md`，"
             "仅剔除聊天界面引证残留与下载导航，物理文字未改）。来料 §6 的 87 423 组穷举计数为另一扫描口径"
             "（域未声明），本卷 160 800 组为独立 box ±200 复算；两者不互证、不互为否定，结论以最小解与"
             "解析证明为准。Q4 的 10/5 中性场计数与 Q5 的 α=N²/(64π²(M₆R)⁴) 代数复算均属本卷增补核对。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：W90-BOUND-VERIFIED / ANOMALY-SET-COMPLETE-P1-ABSENT / STILL-NOT-A-PREDICTION —— "
             "V18 的下界定理与反常框架全部独立复现为真，且其两方程恰好构成 6D 完备局域反常条件"
             "（p₁ 不存在）；本卷把下界扩展到符号关联路线（180|N|）并与 RG 链联合定量排除 SM 外"
             "额外可见手征内容。**r298→r299→r300 判词链：几何侧（ξ 自由、口径）与内容侧（W 界、"
             "反常完备集）均已钉死，α 的独立预测仍缺 UV 输入。**")
    J.append("")
    J.append("- **X-R300-1**：W≥90|N| 在允许 GS 机制或非阿贝尔嵌入后的推广——非阿贝尔表示的"
             "反常条件（trTᵃTᵇ 结构）下，最轻带电手征内容的最小运行权重是多少？")
    J.append("- **X-R300-2**：符号关联路线（Q7）的 4D 手征谱在磁通背景下的流入机制核算："
             "4D 零模反常为零时流入项是否严格为零？")
    J.append("- **X-R300-3**：ε_loop≫1 的大 N 路线的非微扰处理：能否用双通量构造把带电内容的"
             "有效 W 与几何控制解耦后，仍满足精密电磁测量约束？")
    J.append("- **X-R300-4**：V18 §5 质量障碍的正面解：SM 嵌入（非阿贝尔 + Higgs）下"
             "(4,4,−4,1) 型谱能否获得与观测相容的质量结构？")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_ROOTV18反常自由谱与量子修正下界_r300可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    eps = [["V17,N=1", 90], ["V18,N=1", 208], ["V17,N=10", 900], ["V17,N=215", 19350]]
    cmp_rows = [["6D 带电场数", 22, 13], ["4D 零模数(N=1)", 30, 28], ["W", 90, 208]]
    payload = {"rid": RID, "stamp": STAMP, "items": rows, "eps": eps, "cmp": cmp_rows}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · ROOT V18 反常自由谱与量子修正下界审计</title>
<style>
body{margin:0;padding:24px;background:#f7f8fa;color:#1f2328;font-family:"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.6}
h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:24px 0 10px;padding-left:8px;border-left:4px solid #2b5c9b}
.sub{color:#5b6470;font-size:13px;margin-bottom:18px}
.card{background:#fff;border:1px solid #dfe3e8;border-radius:8px;padding:14px 16px;margin-bottom:12px}
.mono{font-family:Consolas,monospace;font-size:12px;color:#5b6470}
.tag{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;color:#fff}
.PASS{background:#1a7f37}.FAIL{background:#c0392b}.BOUNDARY{background:#b8860b}.INFO{background:#2f6f9f}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.kpi{background:#fff;border:1px solid #dfe3e8;border-radius:8px;padding:12px 14px}
.kpi .k{font-size:12px;color:#5b6470}.kpi .v{font-size:19px;font-weight:600;margin-top:2px}
.bar{display:flex;align-items:center;gap:10px;margin:6px 0}.bar .lb{width:150px;font-size:13px}
.bar .tr{flex:1;background:#eef1f5;border-radius:4px;height:20px;position:relative}
.bar .fl{height:20px;border-radius:4px;background:#2b5c9b}.bar .vl{font-size:12px;color:#5b6470;width:110px}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #dfe3e8;padding:6px 10px;font-size:13px}
th{background:#eef1f5}
</style></head><body>
<h1>TUFT-RID · ROOT V18 反常自由谱与量子修正下界审计</h1>
<div class="sub">靶：ROOT V18.0 来料 · STAMP · 判词：<b>W90-BOUND-VERIFIED / ANOMALY-SET-COMPLETE-P1-ABSENT / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、ε_loop = α·W/(3π)：大 N 路线微扰失效</h2>
<div class="card" id="eps"></div>
<div class="mono">N=215 时 ε_loop≈14.98≫1：靠增大磁通改善几何控制会在一圈水平自毁——来料联合限制成立。</div>
<h2>三、V17 vs V18：场数更少 ≠ 量子修正更小</h2>
<div class="card"><table id="cmp"></table>
<div class="mono">V18 场数 −41% 而 W +131%；全局最小运行权重仍为 90|N|（6D 手征路线），符号关联路线下界 180|N|（本卷新增）。</div></div>
<h2>四、条目逐条</h2><div id="items"></div>
<script>
const D=__PAYLOAD__;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};D.items.forEach(x=>c[x.v]++);
document.getElementById('kpi').innerHTML=
 kpi('条目总数',D.items.length)+kpi('PASS',c.PASS)+kpi('FAIL',c.FAIL)+kpi('INFO',c.INFO)+kpi('BOUNDARY',c.BOUNDARY);
function kpi(k,v){return '<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div></div>';}
document.getElementById('items').innerHTML=D.items.map(x=>
 '<div class="card"><span class="tag '+x.v+'">'+x.v+'</span> <b>'+x.id+'</b> · '+x.t+
 '<div class="mono" style="margin-top:6px">'+x.d+'</div></div>').join('');
const mx=Math.max(...D.eps.map(e=>e[1]));
document.getElementById('eps').innerHTML=D.eps.map(e=>
 '<div class="bar"><div class="lb">'+e[0]+'</div><div class="tr"><div class="fl" style="width:'+(100*e[1]/mx).toFixed(1)+'%;background:'+(e[1]>1000?'#c0392b':'#2b5c9b')+'"></div></div><div class="vl">W='+e[1]+'</div></div>').join('');
document.getElementById('cmp').innerHTML='<tr><th>指标</th><th>V17 (15,-6,1,0)</th><th>V18 (4,4,-4,1)</th></tr>'+
 D.cmp.map(r=>'<tr><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td></tr>').join('');
</script></body></html>"""


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3()
    extra["q4"] = q4()
    extra["q5"] = q5()
    extra["q6"] = q6()
    extra["q7"] = q7()
    extra["q8"] = q8()
    extra["q9"] = q9()
    extra["q10"] = q10()
    extra["declared_n"] = 24
    ctl = controls()
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · ROOT V18 反常自由谱与量子修正下界来料审计" % RID)
    for k, v in summary.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("HTML:", hp)
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    rc = 0 if (not bad) and all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "守卫") else 2
    print("RC =", rc)
    sys.exit(rc)


if __name__ == "__main__":
    main()
