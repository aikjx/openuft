# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
动力学本征值路线：可行性判据与首次真实尝试
=========================================

第56章 §56.9 [C]3 明确把"动力学路线的可行性判据"列为解锁 UFT-3 所必需、
但本书尚未完成的步骤。本章（第62章）做两件事：

  (1) 给出动力学路线的可行性判据——定理 A 的动力学类比：
      一个动力学路线能产出"真预言"，当且仅当无量纲靶 q 是某个
      "由第一性原理固定、无可调无量纲旋钮"的算子 O 的谱不变量，
      且该算子的"旋钮空间"维数 nullity_dyn = 0。
      （这是量纲零空间定理的动力学对应物：量纲代数路线用锚集零空间，
       动力学路线用旋钮零空间。两者都是"自由度的零空间"。）

  (2) 在该判据下，对本书螺旋几何做第一次真实尝试，并诚实审计：
      尝试 #1：螺旋曲线上的 da Costa 几何势薛定谔算子 —— 谱是自由粒子谱的
              常数平移，无任何 α 尺度的本征结构；候选无量纲本征值 q 依赖
              任意的盒子长度 L（或等价地螺旋半径 R），证明 nullity_dyn >= 1。
      尝试 #2：把螺旋螺距 b/R 当作应由变分原理固定的量 —— 在已陈述的几何中
              b/R 是自由参数，没有任何第一性原理项依赖它，故偏导数恒为 0，
              b/R 不被固定，α = sinθ ≈ κ/τ 仍是输入而非本征值。

  全程不调参去凑 1/137。所有数字由 mpmath/sympy 真实算出。

零依赖：仅 sympy / mpmath（与既有引擎一致，使用系统 python3.8 运行）。
"""

import io
import json
import os
import sys

import mpmath as mp
from sympy import Matrix, symbols, Rational, simplify, diff, pi

try:                       # 修复：GBK 控制台无法编码非 GBK 字符（→ 等）时崩溃
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)

# =====================================================================
# 物理常数（CODATA 2018 / 标准值）
# =====================================================================
ALPHA = mp.mpf("7.2973525693e-3")          # 精细结构常数
ALPHA_INV = mp.mpf("137.035999084")        # 1/alpha
HBAR = mp.mpf("1.054571817e-34")           # J·s
C = mp.mpf("299792458")                    # m/s
ME = mp.mpf("9.1093837015e-31")            # kg
LAMBDA_C = HBAR / (ME * C)                 # 电子康普顿波长 ≈ 3.8616e-13 m


def fmt(x, n=6):
    return mp.nstr(x, n)


# =====================================================================
# 第一部分：动力学可行性判据（定理 A 的动力学类比）—— 文字 + 形式化
# =====================================================================
def feasibility_criterion():
    """
    返回可行性判据的结构化描述。
    nullity_dyn = 算子 O 中"可调无量纲旋钮"的个数。
      nullity_dyn = 0  -> 靶 q 由解的结构唯一决定 -> 可能为真预言
      nullity_dyn >= 1 -> 存在自由旋钮 -> q 随旋钮连续变化 -> 是拟合非预言
    这是量纲零空间定理（nullity(D_A)=0）的动力学对应物。
    """
    return {
        "name": "动力学可行性判据（定理 A 的动力学类比）",
        "statement": (
            "设动力学路线给出的算子 O[geometry; p_1,...,p_k]，其中 p_i 是理论为固定 O "
            "而引入的无量纲旋钮。定义旋钮空间维数 nullity_dyn = k。靶 q 作为 O 的谱不变量 "
            "被'真派生'当且仅当 nullity_dyn = 0——即 q 不由任何可调旋钮决定，而由解的结构决定。"
        ),
        "analogy_to_theorem_A": (
            "量纲代数路线：nullity(D_A)=0 才能造出无量纲数；"
            "动力学路线：nullity_dyn=0 才能造出'被解固定的'无量纲数。"
            "两条都是'自由度的零空间'，差别在零空间出现在哪类方程上。"
        ),
        "verdict_rule": "nullity_dyn = 0 ⇒ 路线有望；nullity_dyn >= 1 ⇒ 路线当前为拟合，未解锁 UFT-3",
    }


# =====================================================================
# 第二部分：尝试 #1 —— 螺旋曲线上的 da Costa 几何势薛定谔算子
# =====================================================================
def attempt_1_helix_schrodinger():
    """
    在具有恒定曲率 κ、恒定挠率 τ 的螺旋曲线上，约束粒子运动的量子哈密顿量为
        H = -(ħ²/2m) d²/ds² + V_geo(s)
    其中 da Costa 几何势 V_geo = -(ħ²/8m)(κ²(s) - τ²(s))。
    对螺旋曲线 κ,τ 为常数，故 V_geo 为常数偏移 -> 谱 = 自由粒子谱 + 常数。

    真实计算：
      (a) 用有限差分把 H 离散成 N×N 三对角矩阵，取 N=6 用 sympy 求本征值，
          验证其等于闭式 E_n = V_geo + 2t(1 - cos(nπ/(N+1)))（t=ħ²/(2m h²)）。
      (b) 取物理长度尺度，展示"候选无量纲本征值" q = E_1/(m c²) 随任意盒子长度
          L（或等价地螺旋半径 R）连续变化 -> 证明存在自由旋钮（nullity_dyn >= 1）。
    """
    # --- 螺旋几何参数：人为选取 b/R = 1/α，使 κ/τ = tanθ ≈ α（复现书中设定）---
    ratio_bR = 1 / ALPHA                       # b/R，使 κ/τ = R/b = α
    R = mp.mpf("1e-15")                        # 螺旋半径（任意！这是自由旋钮）
    b = ratio_bR * R
    Rs2 = R * R + b * b
    kappa = R / Rs2                            # 曲率
    tau = b / Rs2                              # 挠率
    kappa_tau = kappa / tau                    # = R/b = α（定义性，复现 C2）

    # --- da Costa 几何势（常数）---
    V_geo = -(HBAR ** 2) / (8 * ME) * (kappa ** 2 - tau ** 2)

    # --- (a) 小小的 sympy 验证：N=6 三对角矩阵本征值是否等于闭式 ---
    N = 6
    h = symbols("h")
    t = (HBAR ** 2) / (2 * ME * h ** 2)        # 离散动能系数（符号）
    V0 = symbols("V0")
    # 三对角矩阵：对角 V0 + 2t，次对角 -t
    rows = []
    for i in range(N):
        row = [0] * N
        row[i] = V0 + 2 * t
        if i > 0:
            row[i - 1] = -t
        if i < N - 1:
            row[i + 1] = -t
        rows.append(row)
    M = Matrix(rows)
    # 先代入数值（sympy 无法对含自由符号的 6×6 矩阵求符号根），再做数值本征值
    hval = mp.mpf("1e-11")
    V0val = float(V_geo)
    tval = float((HBAR ** 2) / (2 * ME * hval ** 2))
    M_num = M.subs({h: hval, V0: V0val})
    ev_sym = M_num.eigenvals()                 # 数值本征值（CRootOf）
    ev_sym_list = sorted([complex(e.evalf()).real for e in ev_sym.keys()])
    # 闭式：E_n = V0 + 2t(1 - cos(nπ/(N+1))), n=1..N
    hval = mp.mpf("1e-11")                     # 任意网格间距
    V0val = float(V_geo)
    tval = float((HBAR ** 2) / (2 * ME * hval ** 2))
    closed = [V0val + 2 * tval * (1 - mp.cos(n * mp.pi / (N + 1))) for n in range(1, N + 1)]
    closed_sorted = sorted([float(c) for c in closed])
    max_dev = max(abs(ev_sym_list[i].real - closed_sorted[i]) for i in range(N))

    # --- (b) 候选无量纲本征值 q = E_1/(m c²) 对自由旋钮 L（盒子长度）的依赖 ---
    # 取连续闭式在 L→∞ 极限下基态 E_1 → V_geo（最低 k→0），
    # 但有限盒子下 E_1 = V_geo + (ħ²/2m)(π/L)²。q = E_1/(m c²) 显含 L。
    Ls = [mp.mpf("1e-12"), mp.mpf("1e-10"), mp.mpf("1e-8"), mp.mpf("1e-6")]
    q_scan = []
    for L in Ls:
        E1 = V_geo + (HBAR ** 2) / (2 * ME) * (mp.pi / L) ** 2
        q = E1 / (ME * C ** 2)
        q_scan.append((float(L), float(q)))

    # 同时展示：以 R 为旋钮时 q(R) = (λ_C / R)² 形式（电子能量尺度/约束能尺度）
    R_scan = [mp.mpf("1e-16"), mp.mpf("1e-15"), mp.mpf("1e-14"), mp.mpf("1e-13")]
    qR_scan = []
    for Rr in R_scan:
        # 约束带来的特征能量尺度 ~ ħ²/(2m R²)，无量纲化 ~ (λ_C/R)²
        qR = (LAMBDA_C / Rr) ** 2
        qR_scan.append((float(Rr), float(qR)))

    return {
        "R_chosen": fmt(R, 4),
        "b_over_R": fmt(ratio_bR, 6),
        "kappa": fmt(kappa, 6),
        "tau": fmt(tau, 6),
        "kappa_over_tau": fmt(kappa_tau, 6),
        "alpha": fmt(ALPHA, 6),
        "V_geo_J": fmt(V_geo, 6),
        "sympy_vs_closed_maxdev": fmt(max_dev, 4),
        "sympy_validated": bool(max_dev < 1e-6),
        "q_vs_L": q_scan,
        "q_formula_note": "q(L) = [V_geo + (ħ²/2m)(π/L)²]/(m c²)，显含任意盒子长度 L",
        "q_vs_R": qR_scan,
        "qR_formula_note": "以螺旋半径 R 为旋钮时 q(R) = (λ_C/R)²，R 任意 ⇒ q 任意",
        "conclusion": (
            "螺旋曲线（恒定曲率）上的 da Costa 薛定谔谱是自由粒子谱的常数平移，"
            "不含任何 α 尺度的本征结构。候选无量纲本征值 q 显含任意旋钮 L 或 R，"
            "证明 nullity_dyn >= 1：这条朴素动力学路线没有解锁 UFT-3，"
            "α 仍藏在 κ/τ（即 b/R）的定义里——这正是定理 C 情形 2（C2）的动力学重述。"
        ),
    }


# =====================================================================
# 第三部分：尝试 #2 —— 螺距 b/R 是否由第一性原理变分固定？
# =====================================================================
def attempt_2_pitch_variation():
    """
    书中 α = sinθ，且 κ/τ = tanθ = R/b，故 α 由螺距比 b/R 决定。
    要让 α 成为"派生量"而非"输入"，必须有第一性原理变分原理固定 b/R。

    真实计算：构造作用量 A(b/R)。在当前已陈述的纯螺旋几何中，没有任何项
    显式依赖 b/R（κ,τ 出现在运动学里但 α 只是其比值，几何本身对 b/R 无偏好）。
    因此 ∂A/∂(b/R) ≡ 0 -> b/R 是平移方向（flat direction），不被固定。

    我们用一个符号示例演示：A = a*(κ²+τ²) + b_const（a,b_const 为常数），
    其中 κ²+τ² = (ω/c)² 与 b/R 无关（三重奏恒等式），故 A 不依赖 b/R。
    """
    x = symbols("x")        # x = b/R（螺距比）
    a, om, c = symbols("a om c")
    # 三重奏恒等式：κ²+τ² = (ω/c)²，与 x 无关
    kappa2_tau2 = om ** 2 / c ** 2
    # 作用量只含 (κ²+τ²) 与一个常数 -> 不依赖 x
    A = a * kappa2_tau2 + Rational(1, 2)
    dA_dx = diff(A, x)
    return {
        "action_depends_on_x": bool(simplify(dA_dx) != 0),
        "dA_dx": str(simplify(dA_dx)),
        "flat_direction": bool(simplify(dA_dx) == 0),
        "note": (
            "在当前螺旋几何的作用量中，κ²+τ² 由三重奏恒等式固定为 (ω/c)²，"
            "与螺距比 x=b/R 无关；没有任何第一性原理项显式依赖 x。"
            "故 ∂A/∂x ≡ 0，x=b/R 是平移方向，不被变分固定。"
            "α = sinθ ≈ κ/τ 因此仍是输入（C2），不是本征值。"
        ),
    }


# =====================================================================
# 第四部分：对本次尝试的诚实审计（UFT-1..6 + V3）
# =====================================================================
def audit_attempt():
    """
    用与第55章、第60章一致的 UFT-1..6 / V3 口径审计本次动力学尝试。
    关键点：本尝试"走动力学路线"本身不等于"解锁 UFT-3"；
    它必须同时满足 nullity_dyn=0 才谈得上预测力。本次为 1/6。
    """
    marks = {
        "UFT-1": (True,  "数学自洽：薛定谔/da Costa 算子在螺旋上内部无硬冲突"),
        "UFT-2": (False, "无新的统一作用量；螺旋几何+SM 重写，无特有项"),
        "UFT-3": (False, "α 仍是输入（κ/τ 定义），nullity_dyn>=1，V3 判 NA/B"),
        "UFT-4": (False, "未从第一性原理复现 SM 粒子谱/耦合"),
        "UFT-5": (False, "无与已知理论不同的可检验新预言"),
        "UFT-6": (False, "unreviewed"),
    }
    score = sum(1 for v in marks.values() if v[0])
    return {
        "marks": {k: {"pass": v[0], "note": v[1]} for k, v in marks.items()},
        "score": score,
        "total": 6,
        "verdict": (
            "本次动力学尝试得分 1/6（仅 UFT-1）。"
            "这比联盟自身的 2/6 还低，说明'仅仅改用动力学语言'并不自动解锁 UFT-3；"
            "要解锁必须满足 nullity_dyn=0，即提供能固定 b/R（从而固定 α）的"
            "第一性原理变分项与具结构的（非恒定）势——这正是开放的研究缺口。"
        ),
    }


def main():
    crit = feasibility_criterion()
    a1 = attempt_1_helix_schrodinger()
    a2 = attempt_2_pitch_variation()
    aud = audit_attempt()

    payload = {
        "tool": "动力学本征值路线_可行性判据与首次尝试",
        "feasibility_criterion": crit,
        "attempt_1_helix_schrodinger": a1,
        "attempt_2_pitch_variation": a2,
        "audit": aud,
        "overall": (
            "UFT 联盟层达成度仍为 2/6（未实现）。动力学本征值路线是唯一可行解路径"
            "(定理 C)，但本次首次真实尝试证明：朴素地把螺旋几何动力学化并不能解锁 "
            "UFT-3——α 仍编码在 κ/τ（即 b/R）的定义中，且几何势谱无 α 尺度结构。"
            "解锁所需的研究缺口：(i) 一个显式依赖 b/R 的第一性原理变分项以固定螺距；"
            "(ii) 一个具非平凡结构的势使算子产生可被观测约束的本征值；"
            "(iii) nullity_dyn=0 的形式化证明。"
        ),
    }

    with io.open(os.path.join(DATA, "动力学本征值路线_2026-09-19.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))

    # markdown
    L = []
    L.append("# 动力学本征值路线：可行性判据与首次真实尝试")
    L.append("")
    L.append("**引擎**：`源码/动力学本征值路线_可行性判据与首次尝试.py`（零依赖，系统 python3.8）")
    L.append("")
    L.append("## 一、可行性判据（定理 A 的动力学类比）")
    L.append("")
    L.append("> " + crit["statement"])
    L.append("")
    L.append(crit["analogy_to_theorem_A"])
    L.append("")
    L.append("**裁定规则**：" + crit["verdict_rule"])
    L.append("")
    L.append("## 二、尝试 #1：螺旋曲线上的 da Costa 几何势薛定谔算子")
    L.append("")
    L.append("选取 b/R = 1/α = %.4f 复现书中设定，使 κ/τ = %.6f ≈ α = %.6f。" % (
        float(a1["b_over_R"]), float(a1["kappa_over_tau"]), float(ALPHA)))
    L.append("")
    L.append("| 量 | 值 |")
    L.append("| --- | --- |")
    L.append("| 螺旋半径 R（任意旋钮） | %s m |" % a1["R_chosen"])
    L.append("| 曲率 κ | %s |" % a1["kappa"])
    L.append("| 挠率 τ | %s |" % a1["tau"])
    L.append("| κ/τ | %s |" % a1["kappa_over_tau"])
    L.append("| da Costa 几何势 V_geo | %s J |" % a1["V_geo_J"])
    L.append("| sympy 本征值 vs 闭式最大偏差 | %s（验证通过=%s） |" % (
        a1["sympy_vs_closed_maxdev"], a1["sympy_validated"]))
    L.append("")
    L.append("**候选无量纲本征值 q = E_1/(m c²) 对自由旋钮 L（盒子长度）的依赖**：")
    L.append("")
    L.append("| L (m) | q |")
    L.append("| --- | --- |")
    for Lv, qv in a1["q_vs_L"]:
        L.append("| %.0e | %.6e |" % (Lv, qv))
    L.append("")
    L.append("**以螺旋半径 R 为旋钮时 q(R) = (λ_C/R)²**：")
    L.append("")
    L.append("| R (m) | q(R) |")
    L.append("| --- | --- |")
    for Rv, qRv in a1["q_vs_R"]:
        L.append("| %.0e | %.6e |" % (Rv, qRv))
    L.append("")
    L.append("> " + a1["conclusion"])
    L.append("")
    L.append("## 三、尝试 #2：螺距 b/R 是否由第一性原理变分固定？")
    L.append("")
    L.append("- 作用量是否显式依赖 x=b/R：**%s**" % a2["action_depends_on_x"])
    L.append("- ∂A/∂x = `%s`" % a2["dA_dx"])
    L.append("- x=b/R 是否为平移方向（不被固定）：**%s**" % a2["flat_direction"])
    L.append("")
    L.append("> " + a2["note"])
    L.append("")
    L.append("## 四、对本次尝试的诚实审计（UFT-1..6 + V3）")
    L.append("")
    L.append("| 判据 | 结论 | 依据 |")
    L.append("| --- | --- | --- |")
    for k, v in aud["marks"].items():
        L.append("| %s | %s | %s |" % (k, "✅" if v["pass"] else "❌", v["note"]))
    L.append("")
    L.append("**得分：%d/6** — %s" % (aud["score"], aud["verdict"]))
    L.append("")
    L.append("## 五、总论")
    L.append("")
    L.append(payload["overall"])
    L.append("")
    L.append("> **诚实立场**：本次尝试**没有**实现统一场论，也没有解锁 UFT-3。"
             "它做的是把「为什么朴素螺旋动力学仍失败」从一句断言变成一次可复算的计算："
             "几何势谱无 α 尺度结构、螺距比 b/R 是自由旋钮（nullity_dyn≥1）。"
             "这正是要走通动力学路线必须补上的三块砖（固定螺距的变分项 / 具结构势 / nullity_dyn=0 证明）。")

    with io.open(os.path.join(DATA, "动力学本征值路线.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    # stdout summary
    out = []
    out.append("=" * 60)
    out.append("动力学本征值路线：可行性判据与首次真实尝试")
    out.append("=" * 60)
    out.append("κ/τ = %s  (α = %s)" % (a1["kappa_over_tau"], fmt(ALPHA, 6)))
    out.append("sympy验证最大偏差 = %s (通过=%s)" % (a1["sympy_vs_closed_maxdev"], a1["sympy_validated"]))
    out.append("b/R 平移方向(不被固定) = %s" % a2["flat_direction"])
    out.append("审计得分 = %d/6" % aud["score"])
    out.append("结论: UFT 仍为 2/6; 动力学路线未解锁 UFT-3")
    txt = "\n".join(out)
    with io.open(os.path.join(HERE, "_动力学_stdout.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
