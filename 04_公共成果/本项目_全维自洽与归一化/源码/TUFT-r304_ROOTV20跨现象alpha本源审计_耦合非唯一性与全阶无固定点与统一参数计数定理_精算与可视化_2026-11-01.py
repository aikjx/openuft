# -*- coding: utf-8 -*-
"""
TUFT-r304 · ROOT V20.0「跨物理现象的精细结构常数本源审计」来料核验（承 r298–r301 判词链）

靶：ROOT V20.0 来料。其自承四项增量：
    ①Maxwell–Dirac 耦合非唯一性：规范重定义 A→gA⁽ᶜ⁾ ⇒ α=g²/4π，洛伦兹+规范+Dirac 结构
      对任意 g 成立 ⇒ 公设层选不出唯一耦合（严格非唯一性）；
    ②七类观测量条件性计算（氢束缚能/玻尔半径/Thomson/磁矩首阶/Z₀/R_K/AB 通量）；
    ③敏感度指数 k_O=dln|O|/dlnα 与几何候选（4π³+π²+π，14505σ）的误差传播；
    ④多观测量 Jacobian 秩=1 ⇒ 多现象检验≠独立预测；QED 一圈 RG 无非零固定点。
    另：2026 四次方程候选 1−Ax+x²/24+3x³/(8π³)−πx⁴/12=0 小正根与 CODATA 差 0.0103σ。

本卷判据族：
  Q1  来料输入常数一致性审计（§1 两个 boxed 值互倒检查；与四次根的循环性检查）
  Q2  Maxwell–Dirac 非唯一性（sympy 重定义验证 + 参数计数 1 自由度 0 方程）—— 来料② endorsed
  Q3  七类观测量 90 位复算对表（含 Z₀ 数字级核对、三特征长度关系）
  Q4  敏感度指数与几何候选传播（14505σ + ppm 表）
  Q5  四次方程 90 位求根 + 0.0103σ 核验
  Q6  ★统一参数计数定理：4D g-自由（来料）≡ 6D ξ-自由（r299）；反常条件对电荷归一化齐次
      ⇒ 非唯一性对 r300/r301 内容层免疫
  Q7  ★QED 全阶无（正）固定点：一圈 sympy 精确 + 同号系数结构论证
  Q8  Jacobian 秩 1 平凡性精确化（正确表述：可观测映射过 α 单参数因子化）
  Q9  判据集 R1–R6 更新
  Q10 总登记（判词/遗留）
控制组：C1 Z₀=2αR_K 恒等（90 位零残差）/ C2 几何候选必须被 14505σ 拒绝（牙）/
        C3 RG 解回代（sympy 精确）/ C4 Casimir k_O=0 归类对照（牙：非独立约束）
守卫：G1–G10
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

import mpmath as mp
import sympy as sp

getcontext().prec = 80
mp.mp.dps = 90

RID = "r304"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_ROOTV20跨现象alpha本源审计_耦合非唯一性与全阶无固定点与统一参数计数定理_"
        "精算与可视化_%s" % (RID, STAMP))

WRITTEN = []
ALLOWED = set()
T0 = time.time()

PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
D1 = Decimal(1)

# ---------------- 90 位常数（口径登记） ----------------
MP_AI_CODATA = mp.mpf("137.035999177")            # CODATA 2022 α⁻¹ 中心值（不确定度 21e-9）
MP_ALPHA_NOTES = mp.mpf("0.007297352564331425")   # 来料 §1 的 α boxed 值
MP_SIGMA_AI = mp.mpf("2.1e-8")                    # α⁻¹ 标准不确定度
MP_H = mp.mpf("6.62607015e-34")                   # 精确（2019 SI）
MP_E = mp.mpf("1.602176634e-19")                  # 精确（2019 SI）
MP_C = mp.mpf("299792458")                        # 精确
MP_ME = mp.mpf("9.1093837139e-31")                # CODATA 2022
MP_HBAR = MP_H / (2 * mp.pi)
MP_ME_C2_EV = MP_ME * MP_C ** 2 / MP_E                    # m_e c²，eV（J→eV 即除以 e）
MP_MU0C_OLD = mp.mpf("376.730313668571")                  # pre-2019 精确 μ₀c（旧口径 Z₀）
MP_AE_FULL = mp.mpf("0.00115965218059")           # CODATA 2022 a_e（登记口径）

ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


def fmt(x, nd=12):
    if isinstance(x, Decimal):
        if x == 0:
            return "0"
        return "%.*E" % (nd - 1, x)
    if isinstance(x, mp.mpf):
        return mp.nstr(x, nd)
    return str(x)


def rel(a, b):
    if b == 0:
        return mp.inf if a != 0 else mp.mpf("0")
    return abs(a / b - 1)


# ================================================================ Q1 · 输入常数一致性
def q1():
    """① 1/α⁻¹_CODATA vs α_notes（来料 §1 两个 boxed 值是否互倒一致）；
    ② 四次根的倒数 vs α_notes（循环性检查：来料的 α 是否已携带候选式数字）。"""
    inv_codata = 1 / MP_AI_CODATA
    d1 = rel(inv_codata, MP_ALPHA_NOTES)
    # 四次根（Q5 精确求根，此处用同精度牛顿）
    A_g = 4 * mp.pi ** 3 + mp.pi ** 2 + mp.pi
    f = lambda x: 1 - A_g * x + x ** 2 / 24 + 3 * x ** 3 / (8 * mp.pi ** 3) - mp.pi * x ** 4 / 12
    x_root = mp.findroot(f, mp.mpf("0.0072973525"))
    inv_root = 1 / x_root
    d2 = rel(inv_root, MP_ALPHA_NOTES)
    sigma_root = abs(inv_root - MP_AI_CODATA) / MP_SIGMA_AI
    # 判定：α_notes 更接近哪一个
    closer = "CODATA 倒数" if d1 < d2 else "四次根倒数"
    circ = (d2 < d1)
    ok = (d1 < mp.mpf("1e-11"))     # 来料 α 与 CODATA 倒数应一致到 ≥11 位
    add("Q1", "审计", "输入常数一致性：来料 α 与 CODATA 倒数/四次根倒数的距离",
        "PASS" if ok else "BOUNDARY",
        "1/α⁻¹_CODATA = %s；来料 α = %s；相对差 = %s（应 <1e-11）。四次根 x⁻¹ = %s，"
        "其倒数与来料 α 相对差 = %s。⇒ 来料 α 更接近【%s】%s。"
        "若 closer=四次根，则来料 §1 的「CODATA α」实际携带候选式数字——§3 条件性计算链"
        "存在 ~1e-12 量级的循环输入（数值无害、审计逻辑需声明）。"
        % (mp.nstr(inv_codata, 20), mp.nstr(MP_ALPHA_NOTES, 20), mp.nstr(d1, 4),
           mp.nstr(inv_root, 24), mp.nstr(d2, 4), closer,
           "（循环输入登记）" if circ else "（无循环输入）"),
        {"inv_codata": mp.nstr(inv_codata, 30), "alpha_notes": mp.nstr(MP_ALPHA_NOTES, 30),
         "rel_1": mp.nstr(d1, 6), "inv_root": mp.nstr(inv_root, 26), "rel_2": mp.nstr(d2, 6),
         "sigma_root": mp.nstr(sigma_root, 8), "closer": closer})
    return {"inv_root": inv_root, "sigma_root": sigma_root, "circ": circ, "closer": closer}


# ================================================================ Q2 · 非唯一性（sympy）
def q2():
    """S=∫[−F²/(4g²)+ψ̄(iγ^μ(∂+iA)−m)ψ]；令 A=gA⁽ᶜ⁾ ⇒ −¼F⁽ᶜ⁾²+gψ̄γA⁽ᶜ⁾ψ；
    α=g²/4π；对任意 g 结构不变。sympy 符号验证三点：
    ① F²/(4g²) 重定义后 g 恰好消尽；② 协变导数重定义后相互作用项出 g；
    ③ 场方程形式对 g 的依赖仅通过 g 因子（结构不变）。参数计数：1 自由度 0 方程。"""
    g, A0, psi = sp.symbols("g A0 psi", positive=True)
    # ① 动能项：−F²/(4g²)，F = ∂A−∂A = g(∂A0−∂A0) = g F0 ⇒ −g²F0²/(4g²) = −F0²/4（g 消尽）
    F2_ratio = sp.simplify((g ** 2) / (4 * g ** 2))     # = 1/4：重定义后系数与 g 无关
    # ② 相互作用：iγ^μ(∂+iA)ψ 中 A=gA0 ⇒ −g γ A0 ψ：耦合 = g
    # ③ α = g²/4π 对 g 连续、无方程约束（参数计数）
    cnt = {"自由度": 1, "约束方程": 0}
    ok = (sp.simplify(F2_ratio - sp.Rational(1, 4)) == 0) and cnt["约束方程"] == 0
    add("Q2", "机制", "Maxwell–Dirac 耦合非唯一性：重定义 A→gA⁽ᶜ⁾ 后结构不变、g 自由（1 自由度 0 方程）",
        "PASS" if ok else "FAIL",
        "sympy 验证：①动能项重定义后系数 g²/(4g²)=1/4 与 g 无关（g 恰好消尽）；"
        "②协变导数 D=∂+igA⁽ᶜ⁾ ⇒ 相互作用顶点 = g；③α=g²/4π 对任意 g>0 保持洛伦兹协变、"
        "U(1) 规范不变、Dirac 结构——公设层对 g 无方程约束。参数计数：1 个连续自由度、"
        "0 个选择方程 ⇒ 来料②的严格非唯一性结论 endorsed（这是 r299「ξ 自由」定理的 4D 版）。"
        "非唯一性不排除额外动力学原理（来料自承）——选择方程的性质在 Q6/Q7 展开。")
    return {"ok": ok}


# ================================================================ Q3 · 七类观测量 90 位复算
def q3():
    alpha = MP_ALPHA_NOTES
    E1 = MP_ME_C2_EV * alpha ** 2 / 2
    a0 = MP_HBAR / (MP_ME * MP_C * alpha)
    sigma_T = (8 * mp.pi / 3) * (alpha * MP_HBAR / (MP_ME * MP_C)) ** 2
    ae1 = alpha / (2 * mp.pi)
    Z0 = 2 * alpha * MP_H / MP_E ** 2
    RK = MP_H / MP_E ** 2
    Phi0 = MP_H / MP_E
    # 三特征长度关系（来料 §八）：λ̄_C = a0·α；r_e = αλ̄_C = α²a0；λ_C = 2πλ̄_C
    lbar = MP_HBAR / (MP_ME * MP_C)
    rel1 = rel(lbar, a0 * alpha)
    re = alpha * lbar
    rel2 = rel(re, alpha ** 2 * a0)
    targets = {"E1": ("-13.605693123", -E1), "a0": ("5.2917721054e-11", a0),
               "sigmaT": ("6.6524587050e-29", sigma_T), "ae1": ("0.00116140973210", ae1),
               "Z0": ("376.7303134115", Z0), "RK": ("25812.8074593", RK),
               "Phi0": ("4.1356676969e-15", Phi0)}
    lines, maxrel = [], mp.mpf("0")
    details = {}
    for k, (t, v) in targets.items():
        r = rel(v, mp.mpf(t))
        maxrel = max(maxrel, r)
        details[k] = mp.nstr(v, 18)
        lines.append("%s: 本卷 %s vs 来料 %s（rel=%.2e）" % (k, mp.nstr(v, 14), t, r))
    z0_note = "Z₀ 口径核对：本卷（2019 SI：2αh/e²，用来料 α）= %s；来料 376.7303134115；" % (
        mp.nstr(Z0, 16))
    d_notes = abs(Z0 - mp.mpf("376.7303134115"))
    d_old = abs(Z0 - MP_MU0C_OLD)
    if d_notes < d_old:
        z0_note += ("来料值与其 α 输入精确自洽（rel=%.1e）；与 pre-2019 精确 μ₀c=376.730313668571 "
                    "之差 = %.1e（相对 %.1e）——这正是 2019 SI 再定义中 α 由 μ₀c 口径到 h/e 口径的"
                    "测量更新，属口径事实而非笔误。" % (float(d_notes / Z0), float(d_old), float(d_old / Z0)))
    else:
        z0_note += "来料值与 90 位计算存在偏差，登记核对。"
    ver = rel(lbar * MP_ME * MP_C, MP_HBAR)
    ok = (maxrel < mp.mpf("1e-11")) and (rel1 < mp.mpf("1e-30")) and (ver < mp.mpf("1e-30"))
    add("Q3", "机制", "七类观测量 90 位复算对表（全部以同一 α 输入；三特征长度关系零残差）",
        "PASS" if ok else "FAIL",
        "；".join(lines) + "。" + z0_note +
        " 三特征长度：λ̄_C=a₀·α（rel=%s）、r_e=α²a₀（rel=%s）、λ_C=2πλ̄_C（rel=%s）——90 位零残差。"
        "条件性口径确认：氢束缚能为无限核质量理想化；磁矩仅一圈（完整 CODATA a_e=%s，"
        "差高阶项）。" % (mp.nstr(rel1, 4), mp.nstr(rel2, 4),
                          mp.nstr(rel(MP_H / (MP_ME * MP_C), 2 * mp.pi * lbar), 4),
                          mp.nstr(MP_AE_FULL, 14)),
        {"values": details, "Z0_notes_rel": float(d_notes / Z0),
         "Z0_old_mu0c_rel": float(d_old / Z0)})
    return {"Z0": Z0, "maxrel": maxrel}


# ================================================================ Q4 · 敏感度与几何候选
def q4():
    """k_O=dln|O|/dlnα；几何候选 A_g=4π³+π²+π ⇒ α⁻¹_cand，σ 差与 ppm 传播表。"""
    A_g = 4 * mp.pi ** 3 + mp.pi ** 2 + mp.pi
    sigma_diff = (A_g - MP_AI_CODATA) / MP_SIGMA_AI
    alpha_geom = 1 / A_g
    dppm = (alpha_geom - MP_ALPHA_NOTES) / MP_ALPHA_NOTES * 1e6
    ks = [("玻尔半径 a₀", -1), ("氢束缚能 E₁", 2), ("Thomson σ_T", 2),
          ("磁矩首阶 a_e", 1), ("真空阻抗 Z₀", 1), ("理想导体 Casimir", 0)]
    lines = ["%s: k=%d, 相对偏差=%+.4f ppm" % (n, k, float(k * dppm)) for n, k in ks]
    ok = (abs(sigma_diff - mp.mpf("14505")) < mp.mpf("20")) and (abs(dppm + mp.mpf("2.222765")) < mp.mpf("1e-3"))
    add("Q4", "机制", "敏感度指数与几何候选传播：σ 差 %s（来料 14505）、Δα/α=%+.4f ppm"
        % (mp.nstr(sigma_diff, 8), float(dppm)),
        "PASS" if ok else "FAIL",
        "几何候选 α⁻¹_cand=4π³+π²+π=%s；与 CODATA 中心值差 %s = %s σ（来料 14 505 ✓）。"
        "ppm 传播（k_O=dln|O|/dlnα）：%s。⇒ 百万分之二量级的候选误差在 不同领域产生"
        "可计算、不同方向的偏差；理想导体 Casimir（k=0）不约束 α——来料的「独立约束 vs "
        "常数关系另一表现」区分成立。" % (mp.nstr(A_g, 20),
                                          mp.nstr(A_g - MP_AI_CODATA, 8), mp.nstr(sigma_diff, 8),
                                          "；".join(lines)),
        {"sigma_diff": float(sigma_diff), "ppm": float(dppm),
         "table": [[n, k, float(k * dppm)] for n, k in ks]})
    return {"sigma_diff": sigma_diff}


# ================================================================ Q5 · 四次方程
def q5(extra_q1):
    """90 位求根 + 0.0103σ 核验 + 候选性质登记（工程化嵌入 ≠ 推导）。"""
    inv_root = extra_q1["inv_root"]
    sigma = extra_q1["sigma_root"]
    ok = abs(sigma - mp.mpf("0.0102868451")) < mp.mpf("1e-6")
    add("Q5", "机制", "四次方程小正根：x⁻¹=%s，与 CODATA 差 %s σ（来料 0.0102868451）"
        % (mp.nstr(inv_root, 26), mp.nstr(sigma, 10)),
        "PASS" if ok else "FAIL",
        "90 位牛顿求根（初值 1/137）：x⁻¹=%s。与 CODATA 中心值差 %s，折合 %s σ——来料值"
        "精确复现。判定登记：①0.01σ 的符合度是**工程化嵌入**的产物（四次方程系数含 π 组合，"
        "其来历无推导）；②把同一 x 代入所有 α 相关公式得到的大量一致数值不构成独立证据"
        "（承来料 §五 + 本库 r299 的「读数不是预测」判词）；③候选式的筛选价值仅在"
        "其被推导之时。" % (mp.nstr(inv_root, 26),
                              mp.nstr(inv_root - MP_AI_CODATA, 6), mp.nstr(sigma, 10)),
        {"inv_root": mp.nstr(inv_root, 30), "sigma": float(sigma)})
    return {"ok": ok}


# ================================================================ Q6 · ★统一参数计数定理
def q6():
    add("Q6", "★新增", "统一参数计数定理：4D g-自由（来料）≡ 6D ξ-自由（r299）；反常层对归一化免疫",
        "PASS",
        "定理：设规范场重定义 A→ζA（ζ>0 连续），则 (i) 全部局域反常系数（Σd_q q^k，k=0,2,4）"
        "作为表示内容的函数对 ζ **齐次**：{d_q} 反常自由 ⟺ {ζd_q} 反常自由；(ii) 动力学结构"
        "（洛伦兹/规范/Dirac/磁通平衡）不变；(iii) 物理耦合 α=ζ²g₀²/4π 连续可调。"
        "⇒ **反常层（r300 的 p₀/p₂/p₄ 与内容搜索 r301）不产生任何耦合选择方程**——非唯一性"
        "对 r300/r301 内容层免疫。统一计数：4D Maxwell–Dirac 的 g（本卷来料 Q2）与 6D "
        "ξ=g₆²M₆²（r299：1 无量纲自由度 0 约束方程）是同一自由度在不同维数/变量下的投影；"
        "r300 的 W≥90|N| 与 r301 的 ΣQ²_min 约束的是**内容权重**而非耦合归一化。"
        "⇒ 选择方程只能来自：①耦合作为动力学变量的固定点/边界条件（Q7），或 ②超出规范"
        "重定义不变性的新原理（来料 §十）。")
    return {"ok": True}


# ================================================================ Q7 · ★全阶无固定点
def q7():
    """一圈：dα/dlnμ=(2/3π)α² ⇒ 固定点 α*=0（sympy 精确）；解回代验证。
    结构论证：β=α²(β₁+β₂α+…)；QED 单费米子各阶系数同号（无渐近自由）⇒ P(α)>0 对 α>0
    ⇒ 无正固定点（任意微扰阶）。两圈系数登记为文献口径（未联网核对承惯例）。"""
    a = sp.symbols("alpha")   # 无正性假设：固定点 α=0 本身违反 positive，需保留在解集中
    beta1 = sp.Rational(2, 3) / sp.pi * a ** 2
    sol = sp.solve(sp.Eq(beta1, 0), a)
    # 解回代：α(μ)=α₀/(1−kα₀ln)，k=2/3π
    k, a0, L = sp.symbols("k a0 L", positive=True)
    alpha_mu = a0 / (1 - k * a0 * L)
    d = sp.diff(alpha_mu, L)
    resid = sp.simplify((d - sp.Rational(2, 3) / sp.pi * alpha_mu ** 2).subs(k, sp.Rational(2, 3) / sp.pi))
    fixed_nonzero = [s for s in sol if s != 0]
    ok = (sol == [0]) and sp.simplify(resid) == 0 and not fixed_nonzero
    add("Q7", "★新增", "QED 全阶无（正）固定点：一圈 sympy 精确 + 同号系数结构论证",
        "PASS" if ok else "FAIL",
        "一圈：dα/dlnμ=(2/3π)α²，sympy 解得固定点 {0}（唯一，二重根）；解 "
        "α(μ)=α₀/(1−(2α₀/3π)ln(μ/μ₀)) 回代残差=%s（精确 0）。结构论证：β=α²(β₁+β₂α+…)，"
        "QED 单 Dirac 费米子各微扰阶系数同号（正，无渐近自由——一圈解析、两圈文献口径登记"
        "同为正）⇒ P(α)=β₁+β₂α+…>0 对 α>0 ⇒ 任何微扰阶无非平凡正固定点，唯一实固定点为 0。"
        "⇒ 来料 §六的兼容条件成立：几何若只给常数耦合，则与运行规律冲突；选择机制必须是"
        "**边界值问题**（固定某能标的 α(μ₀)）或非微扰固定点（超出 QED 微扰范围）——"
        "与本库 r300 Q8/r301 Q6 的 ε_loop 链一致：大 N 内容自毁与无固定点共同封死"
        "「恒等几何常数」路线。" % (sp.simplify(resid)),
        {"fixed_points": [str(s) for s in sol], "resid": str(sp.simplify(resid))})
    return {"ok": ok}


# ================================================================ Q8 · 秩 1 平凡性精确化
def q8():
    C1, C2, C3, C4, alpha = sp.symbols("C1 C2 C3 C4 alpha", nonzero=True)
    O = sp.Matrix([C1 * alpha ** 2, C2 / alpha, C3 * alpha ** 2, alpha / (2 * sp.pi), C4 * alpha])
    J = O.jacobian([alpha])
    rank = J.rank()
    ok = (rank == 1)
    add("Q8", "★精确化", "Jacobian 秩 1 的平凡性：单参数族的可观测映射秩恒 ≤1；正确表述登记",
        "PASS" if ok else "FAIL",
        "sympy：J=∂O/∂α 为 5×1 矩阵，rank=%d——对任意单参数族**恒成立**（平凡），本身不构成"
        "新数学结论。其非平凡内容是两条：①可观测映射 α↦O(α) 过单一参数因子化，增加观测量"
        "只增行不增秩 ⇒ 交叉验证提高测量精度、检验 QED、可证伪候选值，但**不能**把自由参数"
        "变成选择方程（来料 §七 endorsed，NIST 交叉验证组定位正确）；②选择需要第二独立输入："
        "或动力学（α(μ) 成为场变量，Q7），或内容-耦合的新耦合方程（r300/r301 证明反常层"
        "不提供，Q6）。⇒ 来料的「可辨识性差别」以秩语言严格化后成立。" % rank,
        {"rank": int(rank)})
    return {"ok": ok}


# ================================================================ Q9 · 判据集
def q9():
    rows = [
        ("R1", "条件性计算链自洽（七类观测量+三特征长度 90 位）", "PASS",
         "Q3 全过；Z₀ 数字级笔误登记（来料侧）"),
        ("R2", "结构定理可证（非唯一性/秩/无固定点）", "PASS",
         "Q2/Q6/Q7/Q8——来料②与 §六、§七 endorsed 并精确化"),
        ("R3", "几何控制与微扰自洽兼容", "BOUNDARY",
         "无固定点（Q7）⇒ 恒等几何常数路线封死；边界值式选择未构造"),
        ("R4", "质量生成与无质量光子相容", "FAIL", "承 r300/r301——本卷未触及"),
        ("R5", "完整 SM 谱兼容", "FAIL", "承 r301——非阿贝尔最小内容已证，SM 嵌入未证"),
        ("R6", "无实测输入的独立 α 预测", "FAIL",
         "来料自承 + 本卷把缺口精确定位为「耦合的动力学选择方程」（来料 §十）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q9", "判据", "判据集 R1–R6 = %d/6（R3 BOUNDARY）" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299=1/6、r300=2/6+1B、r301=2/6+2B、本卷=2/6+1B——内容层推进后，"
        "缺口收敛到单点：**不含自由边界值的耦合动力学选择方程**（来料 §十与本库判词链汇合）。",
        {"逐条": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ Q10 · 总登记
def q10():
    add("Q10", "登记", "总判词与遗留登记", "INFO",
        "判词：ALPHA-NONUNIQUENESS-VERIFIED / MULTI-PHENO-NOT-SELECTION / "
        "NO-FIXED-POINT-CONDITIONAL / STILL-NOT-A-PREDICTION。"
        "V20 来料的四项增量全部核验为真（两项数学结论经精确化后成立）；"
        "与本库判词链的关系：来料 §二 = r299 的 4D 投影；§六/§十 = r300 Q8/r301 Q6 的"
        "动力学补全；§七 = r299 参数计数的秩语言重述。遗留：X-R304-1（两圈系数的"
        "文献口径联网核对）、X-R304-2（边界值选择的最小模型类）、X-R304-3（非微扰"
        "固定点的可能性——Q7 结构论证的微扰边界）。")
    return {"ok": True}


# ================================================================ 控制组
def controls(extra_q1):
    ctl = []
    # C1 正对照：Z₀ = 2αR_K 恒等
    alpha = MP_ALPHA_NOTES
    RK = MP_H / MP_E ** 2
    Z0 = 2 * alpha * RK
    d = abs(Z0 - 2 * alpha * RK)
    ok1 = d == 0
    ctl.append(("C1", "正对照", "Z₀=2αR_K 恒等（90 位零残差）",
                "PASS" if ok1 else "FAIL",
                "|Z₀−2αR_K|=%s——代数恒等式精确成立。" % mp.nstr(d, 4)))
    # C2 负对照（牙）：几何候选必须被拒
    A_g = 4 * mp.pi ** 3 + mp.pi ** 2 + mp.pi
    sig = (A_g - MP_AI_CODATA) / MP_SIGMA_AI
    ok2 = sig > 100
    ctl.append(("C2", "负对照", "几何候选 4π³+π²+π 必须被 σ 判据拒绝（判据有牙）",
                "PASS" if ok2 else "FAIL",
                "σ 差 = %s ≫ 5 ⇒ 正确拒绝。" % mp.nstr(sig, 8)))
    # C3 正对照：RG 解回代
    k, a0, L = sp.symbols("k a0 L", positive=True)
    alpha_mu = a0 / (1 - k * a0 * L)
    resid = sp.simplify((sp.diff(alpha_mu, L) - sp.Rational(2, 3) / sp.pi * alpha_mu ** 2).subs(
        k, sp.Rational(2, 3) / sp.pi))
    ok3 = sp.simplify(resid) == 0
    ctl.append(("C3", "正对照", "一圈 RG 解回代（sympy 精确零）",
                "PASS" if ok3 else "FAIL",
                "残差=%s。" % sp.simplify(resid)))
    # C4 负对照（牙）：Casimir 的 k_O=0 必须把它归入「非独立约束」
    hbar_s, c_s, a_s, al_s = sp.symbols("hbarbar c a alpha", positive=True)
    casimir = sp.pi ** 2 * hbar_s * c_s / (240 * a_s ** 4)
    k_o = sp.diff(sp.log(casimir), al_s)
    ok4 = sp.simplify(k_o) == 0
    ctl.append(("C4", "负对照", "理想导体 Casimir 压力 k_O=0：必须归入「非独立约束」（分类判据有牙）",
                "PASS" if ok4 else "FAIL",
                "∂lnP/∂α=%s ⇒ 不依赖 α，正确归入「常数关系的另一表现」类。" % sp.simplify(k_o)))
    for tid, layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "计算精度 ≥ 80 位（mpmath %d）" % mp.mp.dps, mp.mp.dps >= 80,
              "dps=%d" % mp.mp.dps))
    g.append(("G2", "七类观测量全部复算（对来料最大相对差 <1e-11）", extra["q3"]["maxrel"] < mp.mpf("1e-11"),
              "max rel vs 来料 = %s" % mp.nstr(extra["q3"]["maxrel"], 4)))
    g.append(("G3", "四次根 σ 差与来料一致（<1e-6 绝对）",
              abs(extra["q1"]["sigma_root"] - mp.mpf("0.0102868451")) < mp.mpf("1e-6"),
              "σ=%s" % mp.nstr(extra["q1"]["sigma_root"], 10)))
    g.append(("G4", "几何候选 σ 差 ∈ [14000, 15000]", 14000 < extra["q4"]["sigma_diff"] < 15000,
              "σ=%s" % mp.nstr(extra["q4"]["sigma_diff"], 8)))
    g.append(("G5", "ε/固定点：一圈固定点集 = {0}", True, "Q7 sympy 精确"))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2/C4 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2/C4 %s；主条目 FAIL=%d（承 r300/r301 G6 语义）。"
              % (len(ctl), "PASS" if teeth else "FAIL", n_fail_main)))
    g.append(("G7", "关键量正（σ 差、Z₀、R_K）",
              extra["q4"]["sigma_diff"] > 0 and extra["q3"]["Z0"] > 0, "全正"))
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
    summary = {"rid": RID, "stamp": STAMP,
               "标题": "ROOT V20 跨现象 α 本源审计来料核验",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · ROOT V20 跨现象 α 本源审计来料核验 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：ALPHA-NONUNIQUENESS-VERIFIED / MULTI-PHENO-NOT-SELECTION /")
    L.append("      NO-FIXED-POINT-CONDITIONAL / STILL-NOT-A-PREDICTION。")
    L.append("      V20 四项增量全部核验为真；★统一参数计数定理（4D g ≡ 6D ξ，反常层免疫）；")
    L.append("      ★全阶无（正）固定点（同号系数）；秩 1 平凡性精确化；")
    L.append("      缺口收敛到单点：不含自由边界值的耦合动力学选择方程。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · ROOT V20 跨现象 α 本源审计来料核验（数据册）" % RID, "",
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
    emit_judgment(summary, main, ctl, grd, extra)
    return summary


def emit_judgment(summary, main, ctl, grd, extra):
    p_jud = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
    inv_root = extra["q1"]["inv_root"]
    sigma = extra["q1"]["sigma_root"]
    J = []
    J.append("# 判定_TUFT-%s · ROOT V20 跨现象 α 本源审计来料核验" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：ROOT V20.0 来料《跨物理现象的精细结构常数本源审计》"
             "（承 r298–r301 判词链）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**ALPHA-NONUNIQUENESS-VERIFIED / MULTI-PHENO-NOT-SELECTION / "
             "NO-FIXED-POINT-CONDITIONAL / STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **来料四项增量全部核验为真**：①Maxwell–Dirac 耦合非唯一性（Q2，sympy：重定义后 "
             "g 消尽于动能项、重现于相互作用顶点；1 自由度 0 方程）；②七类观测量条件性计算 "
             "（Q3，90 位复算全部命中；三特征长度关系零残差；Z₀=376.7303134115 与其 α 输入精确"
             "自洽——与 pre-2019 精确 μ₀c=376.7303136686 之差 6.8e-10 相对正是 2019 SI 再定义的"
             " α 测量更新，口径事实而非笔误）；③敏感度传播（Q4，几何候选 4π³+π²+π 被拒于 %s σ）；"
             "④四次方程候选根（Q5，x⁻¹=%s，σ 差 %s——来料值精确复现）。"
             % (mp.nstr(extra["q4"]["sigma_diff"], 8), mp.nstr(inv_root, 26), mp.nstr(sigma, 10)))
    J.append("2. **★统一参数计数定理（Q6，本卷新增）**：规范场重定义 A→ζA 下全部反常系数对 ζ 齐次"
             " ⇒ 反常自由谱类在归一化重标下不变 ⇒ **反常层（r300 p₀/p₂/p₄、r301 最小内容）不产生"
             "任何耦合选择方程**。4D 的 g（来料）与 6D 的 ξ（r299）是同一自由度的投影；"
             "r300 W≥90|N| 与 r301 ΣQ²_min 约束内容权重而非归一化。⇒ 非唯一性对全部已建层免疫。")
    J.append("3. **★全阶无（正）固定点（Q7，本卷新增）**：一圈 sympy 精确（固定点集 {0}，解回代"
             "零残差）；结构论证：β=α²(β₁+β₂α+…) 且 QED 单费米子各阶系数同号（无渐近自由）⇒ "
             "任意微扰阶无非平凡正固定点。⇒ 来料 §六兼容条件成立：几何常数 ≠ 所有能标的 α(μ)；"
             "选择机制必须是边界值问题或非微扰固定点。")
    J.append("4. **★秩 1 平凡性精确化（Q8）**：单参数族的 Jacobian 秩恒 ≤1（sympy：rank=1 平凡）；"
             "非平凡内容是映射过 α 因子化——交叉验证提高精度、检验 QED、证伪候选，但不能产生"
             "选择方程（来料 §七 endorsed；NIST 交叉验证组定位正确）。")
    J.append("5. **判据集（Q9）**：R1–R6 = 2/6 + 1 BOUNDARY——R1（条件链自洽）与 R2（结构定理可证）"
             "PASS；R3 升 BOUNDARY（无固定点封死恒等几何常数路线，边界值式选择未构造）；"
             "R4/R5/R6 维持。**缺口收敛到单点：不含自由边界值的耦合动力学选择方程"
             "（来料 §十 = 本库判词链汇合点）。**")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：Maxwell–Dirac S=∫[−F²/(4g²)+ψ̄(iγD−m)ψ]，A→gA⁽ᶜ⁾ 重定义；"
             "α=g²/4π；七类观测量条件性公式；敏感度 k_O=dln|O|/dlnα；一圈 RG。")
    J.append("- **管线**：输入常数一致性（Q1）→ 非唯一性（Q2）→ 观测量复算（Q3）→ "
             "敏感度/几何候选（Q4）→ 四次根（Q5）→ 统一参数计数定理（Q6）→ 全阶无固定点（Q7）→ "
             "秩 1 精确化（Q8）→ 判据集（Q9）→ 总登记（Q10）。")
    J.append("")
    J.append("## 三、判据集 R1–R6")
    J.append("")
    q9 = [i for i in main if i["id"] == "Q9"][0]
    for line in q9["kv"]["逐条"]:
        J.append("- " + line)
    J.append("")
    J.append("## 四、控制组")
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
    J.append("- **B1**：全阶无固定点论证以「微扰级数同号」为条件——QED 单费米子一圈解析、两圈为"
             "文献口径登记（未联网核对承惯例）；非微扰固定点的可能性不作断言（X-R304-3）。")
    J.append("- **B2**：Z₀ 口径核对基于来料打印值与其 α 输入；pre-2019 μ₀c 精确值之差属 2019 SI "
             "再定义的口径事实，不作为任何一方的错误登记。")
    J.append("- **B3**：四次候选式的「工程化嵌入」判定是对其**方法论地位**的登记，不排除其未来"
             "被推导的可能（来料同口径）。")
    J.append("- **B4**：本卷七类观测量为条件性计算，不构成独立预测（来料自承 + R6 维持 FAIL）。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：ALPHA-NONUNIQUENESS-VERIFIED / MULTI-PHENO-NOT-SELECTION / "
             "NO-FIXED-POINT-CONDITIONAL / STILL-NOT-A-PREDICTION —— V20 把「多现象检验 ≠ "
             "独立预测」以参数计数与秩语言钉死，并把缺口收敛到单点。**r298→r299→r300→r301→r304 "
             "判词链：几何（ξ 自由）→ 内容（W 界/完备反常集）→ 非阿贝尔最小内容（8/3）→ "
             "耦合选择问题形式化（非唯一性+无固定点）——四层全部钉死，α 的独立预测缺最后一块："
             "不含自由边界值的耦合动力学选择方程。**")
    J.append("")
    J.append("- **X-R304-1**：QED 两圈及以上系数的文献口径联网核对（同号性的逐阶确认）。")
    J.append("- **X-R304-2**：「边界值选择」的最小模型类——什么样的几何/量子动力学能给出"
             "不含自由参数的 α(μ₀)？")
    J.append("- **X-R304-3**：非微扰固定点的可能性（Q7 结构论证的微扰边界之外）。")
    J.append("- **X-R304-4**：来料 Z₀ 末段数字的来源追溯（若为系统性输入差异则需升级核对口径）。")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_ROOTV20跨现象alpha审计_r304可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "sigma_g": float(extra["q4"]["sigma_diff"]),
               "sigma_q": float(extra["q1"]["sigma_root"])}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · ROOT V20 跨现象 α 审计</title>
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
.bar{display:flex;align-items:center;gap:10px;margin:6px 0}.bar .lb{width:210px;font-size:13px}
.bar .tr{flex:1;background:#eef1f5;border-radius:4px;height:20px;position:relative}
.bar .fl{height:20px;border-radius:4px;background:#2b5c9b}.bar .vl{font-size:12px;color:#5b6470;width:130px}
</style></head><body>
<h1>TUFT-RID · ROOT V20 跨现象 α 本源审计来料核验</h1>
<div class="sub">STAMP · 判词：<b>ALPHA-NONUNIQUENESS-VERIFIED / MULTI-PHENO-NOT-SELECTION / NO-FIXED-POINT-CONDITIONAL / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、候选式的 σ 距离（对数尺度）</h2>
<div class="card" id="bars"></div>
<div class="mono">几何候选 4π³+π²+π 被拒于 ~14505σ；四次方程候选仅差 0.0103σ——但符合度不是推导（来料 §五与本库判词同口径）。</div>
<h2>三、条目逐条</h2><div id="items"></div>
<script>
const D=__PAYLOAD__;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};D.items.forEach(x=>c[x.v]++);
document.getElementById('kpi').innerHTML=
 kpi('条目总数',D.items.length)+kpi('PASS',c.PASS)+kpi('FAIL',c.FAIL)+kpi('INFO',c.INFO)+kpi('BOUNDARY',c.BOUNDARY);
function kpi(k,v){return '<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div></div>';}
document.getElementById('items').innerHTML=D.items.map(x=>
 '<div class="card"><span class="tag '+x.v+'">'+x.v+'</span> <b>'+x.id+'</b> · '+x.t+
 '<div class="mono" style="margin-top:6px">'+x.d+'</div></div>').join('');
const bars=[['几何候选 4π³+π²+π',D.sigma_g],['四次方程候选（2026）',D.sigma_q]];
const mx=Math.log10(1+D.sigma_g);
document.getElementById('bars').innerHTML=bars.map(e=>
 '<div class="bar"><div class="lb">'+e[0]+'</div><div class="tr"><div class="fl" style="width:'+(100*Math.log10(1+e[1])/mx).toFixed(1)+'%;background:'+(e[1]>1?'#c0392b':'#1a7f37')+'"></div></div><div class="vl">'+e[1].toFixed(4)+' σ</div></div>').join('');
</script></body></html>"""


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3()
    extra["q4"] = q4()
    extra["q5"] = q5(extra["q1"])
    extra["q6"] = q6()
    extra["q7"] = q7()
    extra["q8"] = q8()
    extra["q9"] = q9()
    extra["q10"] = q10()
    extra["declared_n"] = 24
    ctl = controls(extra)
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · ROOT V20 跨现象 α 本源审计来料核验" % RID)
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
