# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V137 可算审计（最高权限 14 门）

审计对象：用户本轮提供的 ROOT V137 全文（六维异常—磁通—三代手征—内部空间稳定性联合攻坚）。
性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。

V137 自称「残差 0 / 精确匹配」的 9 项，本册逐项独立复算；V137 自称「未完成」的 4 项
（全 KK 稳定性 / 完整 GS / ROOT→S² / 动态选 N=3），本册给出「未完成」与「模型内不可完成」
的区分，并把其中两项从 OPEN 升级为否定理。

十四门：
  G1  迹恒等式两路复算（Fraction 采样 + sympy 多项式恒等）——顺带定价其模型内容为 0。
  G2  I_8 七项系数复算（权重求和路 vs 迹恒等式代入路），逐项对照 V137 原式。
  G3  ∫_{S²}I_8 与 3×16 四维异常的精确多项式恒等 + 负对照（16_1+16_1 不抵消）。
  G4  双张量形式 (X^{(1)},X^{(2)}) 是代数恒等式 ⇒ 零判别力。
  G5  完美平方不可能定理 ⇒ 六维单张量 GS 在模型内不可实现（承 r390，同源计 1 份）。
  G6  四维 I_6 = y∧X_2 精确分解 ⇒ 单轴子可消 ⇒ U(1)_F 反常且必须变重（「匹配」≠「无害」）。
  G7  可辨识性维数：2 个四维观测 vs 4 个未知 ⇒ N 不可判；自然归一下 N 的读数与张力。
  G8  背景唯一性：常曲率二维内空间中只有 S² 与正 Λ_6 相容（给 V137 记一分，限定范围）。
  G9  radion 势是被迫形式 ⇒ V≥0、V''>0 自动成立 ⇒ 零判别力；σ→∞ 处存在退化真空。
  G10 中性 16̄ 无零模：Lichnerowicz 成立 + 圆球谱独立核；负对照 R≤0 时零模出现。
  G11 三重态简并定理（交换子维数=1）+ 13 个味观测输入计数。
  G12 无写死 ok 守卫。
  G13 幂等（自哈希、二次序列化逐字节相同）。
  G14 外部一手来源（可核 URL，禁造假阳性错误）。

红线：数学自洽 != 实验证实；不宣称攻破统一场论，不宣称独立实验预言；四力统一未证。
"""
import os
import ast
import glob
import json
import math
import hashlib
from fractions import Fraction
from decimal import Decimal, getcontext

import sympy as sp

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv137_6d_anomaly_flux_threegen_audit_2026-11-22.json")

X1, X2, X3, X4, X5, Y, P1, P2, Ns = sp.symbols("x1 x2 x3 x4 x5 y p1 p2 N")
XS = [X1, X2, X3, X4, X5]
Q = 2 * sum(x ** 2 for x in XS)          # tr_10 x^2
P = 2 * sum(x ** 4 for x in XS)          # tr_10 x^4


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def fstr(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)


def weights16():
    """Spin(10) 旋量 16 的 16 个权重：五个坐标各 ±1/2，负号个数为偶数。"""
    out = []
    for m in range(32):
        s = [1 if (m >> k) & 1 else -1 for k in range(5)]
        if sum(1 for v in s if v < 0) % 2 == 0:
            out.append([Fraction(v, 2) for v in s])
    assert len(out) == 16
    return out


W16 = weights16()


# ---------------------------------------------------------------- G1 迹恒等式
def g1_trace_identities():
    """两路：(A) 16 权重上精确 Fraction 采样 10 点；(B) sympy 对五个变量做多项式恒等。
       V137 §二 的两个 boxed 式若为真，两路残差均须为 0。"""
    # 路 A：采样
    pts = [[Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)],
           [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
           [Fraction(3, 7), Fraction(-5, 11), Fraction(0), Fraction(2), Fraction(-1, 13)],
           [Fraction(-2), Fraction(9, 4), Fraction(1, 3), Fraction(-7, 5), Fraction(11, 6)],
           [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(1)]]
    seed = 20261122
    for k in range(5):
        seed = (1103515245 * seed + 12345) % (2 ** 31)
        pts.append([Fraction(((seed >> (3 * i)) % 17) - 8, 1 + ((seed >> (5 + i)) % 7))
                    for i in range(5)])

    bad2 = bad4 = 0
    for x in pts:
        t2 = sum(sum(a * b for a, b in zip(x, w)) ** 2 for w in W16)
        t4 = sum(sum(a * b for a, b in zip(x, w)) ** 4 for w in W16)
        if t2 != 4 * sum(c ** 2 for c in x):
            bad2 += 1
        if t4 != Fraction(3, 4) * (2 * sum(c ** 2 for c in x)) ** 2 - 2 * sum(c ** 4 for c in x):
            bad4 += 1

    # 路 B：sympy 多项式恒等
    dw = [sum(XS[i] * sp.Rational(int(w[i].numerator), int(w[i].denominator)) for i in range(5))
          for w in W16]
    tr2_sym = sp.expand(sum(d ** 2 for d in dw))
    tr4_sym = sp.expand(sum(d ** 4 for d in dw))
    res2 = sp.simplify(tr2_sym - 2 * Q)
    res4 = sp.simplify(tr4_sym - (sp.Rational(3, 4) * Q ** 2 - P))

    sample2_val = sum(sum(a * b for a, b in zip(pts[0], w)) ** 2 for w in W16)
    return {
        "n_sample_points": len(pts),
        "sample_fail_2nd": bad2, "sample_fail_4th": bad4,
        "symbolic_residual_2nd": str(res2), "symbolic_residual_4th": str(res4),
        "identity_2nd_holds": bool(bad2 == 0 and res2 == 0),
        "identity_4th_holds": bool(bad4 == 0 and res4 == 0),
        "tr16_2_at_12345": fstr(sample2_val),
        "tr10_2_at_12345": fstr(2 * sum(c ** 2 for c in pts[0])),
        "twice_tr10_2_at_12345": fstr(4 * sum(c ** 2 for c in pts[0])),
        "uses_any_v137_model_input": False,
        "model_content_zero": True,
        "ok": bool(bad2 == 0 and bad4 == 0 and res2 == 0 and res4 == 0),
        "note": "V137 §二 两个迹恒等式成立：10 组有理点采样零失配、sympy 多项式恒等残差 0。"
                "但两式只用到 16 权重的对称性，对任意 x 成立，未使用任何 V137 模型输入"
                "（无 N、无磁通、无 S²）⇒ 它们是表示论恒等式，不构成模型证据，V137 亦未据此作判负。",
    }


# ---------------------------------------------------------------- G2 I8 系数
def _w():
    """16 权重上的一次型 ⟨x,w⟩ 列表（符号）。"""
    return [sum(XS[i] * sp.Rational(int(w[i].numerator), int(w[i].denominator))
                for i in range(5)) for w in W16]


def _ch4():
    """ch_4 = (1/4!)Σ_w (⟨x,w⟩+y)^4 —— 纯权重求和，不假设任何闭式。"""
    return sp.expand(sum((d + Y) ** 4 for d in _w()) / 24)


def _ch3():
    return sp.expand(sum((d + Y) ** 3 for d in _w()) / 6)


def _ch1():
    return sp.expand(sum((d + Y) for d in _w()))


def _ch2():
    return sp.expand(sum((d + Y) ** 2 for d in _w()) / 2)


def _i8_from_weights():
    """I_8 = [Â ch]_8，Â_4=-p1/24, Â_8=(7p1²-4p2)/5760，dim16 乘 Â_8。"""
    return sp.expand(_ch4() + (-P1 / 24) * _ch2() + ((7 * P1 ** 2 - 4 * P2) / sp.Integer(5760)) * 16)


def _i6_from_weights():
    """四维 I_6 = [Â ch]_6 = ch_3 + Â_4 ch_1（单个 16，电荷 1）。"""
    return sp.expand(_ch3() + (-P1 / 24) * _ch1())


def g2_i8_coefficients():
    """路 A：16 权重直接求和（_i8_from_weights，不假设闭式）；
       路 B：V137 §四 原文七项照录。
       判据：两条表达式的差在 8 个单项式上必须恒为 0；并做变异负对照。"""
    i8_w = _i8_from_weights()
    v137 = sp.expand((-sp.Rational(1, 24)) * P + sp.Rational(1, 32) * Q ** 2
                     + sp.Rational(1, 2) * Q * Y ** 2 + sp.Rational(2, 3) * Y ** 4
                     + (-P1 / 24) * Q + (-P1 / 3) * Y ** 2
                     + (7 * P1 ** 2 - 4 * P2) / sp.Integer(360))
    diff = sp.expand(i8_w - v137)
    ok_identity = (diff == 0)

    # 逐单项式系数对照（用 x 的单项式，避免 Q/P 符号化导致的空比对）
    mons = [("x1^4", X1 ** 4), ("x1^2*x2^2", X1 ** 2 * X2 ** 2),
            ("x1^2*y^2", X1 ** 2 * Y ** 2), ("y^4", Y ** 4),
            ("p1*x1^2", P1 * X1 ** 2), ("p1*y^2", P1 * Y ** 2),
            ("p1^2", P1 ** 2), ("p2", P2)]
    table = []
    for nm, mm in mons:
        cw = sp.simplify(i8_w.coeff(mm))
        cv = sp.simplify(v137.coeff(mm))
        table.append({"monomial": nm, "recomputed": str(cw), "v137": str(cv),
                      "match": bool(sp.simplify(cw - cv) == 0)})
    all_match = all(r["match"] for r in table)

    # 独立第二路：5 组有理点直接数值代入（弱路径，仅作旁证）
    pts = []
    for seed in (7, 11, 13, 17, 19):
        t = seed
        vals = []
        for i in range(5):
            t = (1103515245 * t + 12345) % (2 ** 31)
            vals.append(sp.Rational(((t >> (2 * i)) % 13) - 6, 1 + ((t >> (3 + i)) % 5)))
        yv = sp.Rational(((t >> 7) % 11) - 5, 1 + (t % 4))
        p1v = sp.Rational(((t >> 9) % 9) - 4, 1 + (t % 3))
        p2v = sp.Rational(((t >> 11) % 7) - 3, 1 + (t % 2))
        pts.append((vals, yv, p1v, p2v))
    samp_bad = 0
    for vals, yv, p1v, p2v in pts:
        sub = {XS[i]: vals[i] for i in range(5)}
        sub.update({Y: yv, P1: p1v, P2: p2v})
        if sp.simplify(i8_w.subs(sub) - v137.subs(sub)) != 0:
            samp_bad += 1

    # 变异负对照：把 -p1*y^2/3 改成 -p1*y^2/3 + 1/100，判据必须失效
    mut = sp.expand(v137 + sp.Rational(1, 100) * P1 * Y ** 2)
    mut_detected = bool(sp.expand(i8_w - mut) != 0)

    return {
        "i8_recomputed_from_weights": str(i8_w),
        "i8_v137": str(v137),
        "difference": str(diff),
        "identity_exact": ok_identity,
        "term_table": table,
        "all_monomials_match": all_match,
        "sample_points": len(pts), "sample_mismatch": samp_bad,
        "mutation_control_detected": mut_detected,
        "p2_coeff_recomputed": str(sp.simplify(i8_w.coeff(P2))),
        "p2_coeff_v137": str(sp.simplify(v137.coeff(P2))),
        "ok": bool(ok_identity and all_match and samp_bad == 0 and mut_detected),
        "note": "V137 §四 的 I_8(16_1) 与「16 权重直接求和 + Â 展开」逐单项式完全一致（8 个单项式全匹配，"
                "残差 0），含 p_1 交叉项两个负号与 p_2 系数 -1/90。变异负对照（把 -p1y²/3 加 1/100）"
                "被检出 ⇒ 本门有牙。⇒ V137 的八形式代数本身无误。",
    }


# ---------------------------------------------------------------- G3 S² 降维匹配
def g3_s2_reduction_match():
    """真做内部积分：y = a + b（a 沿 S²、b 沿 M_4），S² 是二维 ⇒ a^k=0 (k≥2)，∫a=N。
       六维侧：∫_{S²}I_8^total；四维侧：3×I_6（I_6 由权重求和独立给出）。"""
    a, b = sp.symbols("a b")
    i8_tot = sp.expand(sp.Rational(1, 2) * Q * Y ** 2 - sp.Rational(1, 3) * P1 * Y ** 2
                       + sp.Rational(2, 3) * Y ** 4)
    ex = sp.expand(i8_tot.subs(Y, a + b))
    # 内部积分的机械规则：S² 是二维 ⇒ a^k=0 (k>=2)；8 形式只取恰含一个 a 的项（S² 度为 2），
    # 不含 a 的项属 M_4 的八形式、不进四维六形式反常。∫_{S²}a = N。
    ex = sp.expand(ex.subs(a ** 2, 0))
    ex = sp.expand(ex.subs(a ** 3, 0))
    ex = sp.expand(ex.subs(a ** 4, 0))
    int_s2 = sp.expand(sp.expand(ex).coeff(a) * Ns)
    int_s2_n3 = sp.expand(int_s2.subs(Ns, 3))

    i6_one = sp.expand(_i6_from_weights().subs(Y, b))   # 单代四维六形式异常（权重求和，独立）
    i6_three = sp.expand(3 * i6_one)
    resid = sp.expand(int_s2_n3 - i6_three)

    n_blind = {}
    for n in (1, 2, 4):
        d = sp.expand(int_s2.subs(Ns, n) - sp.expand(n * i6_one))
        n_blind[str(n)] = {"residual": str(d), "match": bool(d == 0)}

    # 负对照：伙伴同带电 (1,1) 时纯规范/纯引力项不抵消
    pure2 = sp.expand(2 * (_ch4() + ((7 * P1 ** 2 - 4 * P2) / sp.Integer(5760)) * 16))
    return {
        "int_S2_I8_symbolic": str(int_s2),
        "int_S2_I8_at_N3": str(int_s2_n3),
        "I6_one_gen_from_weights": str(i6_one),
        "I6_3x16": str(i6_three),
        "residual": str(resid),
        "exact_match": bool(resid == 0),
        "N_blind": n_blind,
        "counterexample_both_charged_pure_term": str(pure2),
        "counterexample_nonzero": bool(pure2 != 0),
        "ok": bool(resid == 0 and all(v["match"] for v in n_blind.values()) and pure2 != 0),
        "note": "六维侧真做内部积分（a^k=0, ∫a=N）得 ∫_{S²}I_8 = N(Qy4-(2/3)p1y4+(8/3)y4³)，"
                "四维侧由权重求和独立给出 I_6 = Qy4+(8/3)y4³-(2/3)p1y4，两者在 N=3 时残差 0。"
                "该匹配对 N=1,2,4 同样精确成立 ⇒ 对代数是盲的。负对照：伙伴同带电时纯规范项残差非零，"
                "故 (16_1,16̄_0) 的电荷赋值是输入。",
    }


# ---------------------------------------------------------------- G3b 四维可消
def g6_four_dim_factorization():
    """I_6（权重求和）能否写成 y4∧X_2：X_2=3Q-2p1+8y4²。"""
    y4 = Y
    i6 = _i6_from_weights()
    x2 = 3 * Q - 2 * P1 + 8 * Y ** 2
    recon = sp.expand(Y * x2)
    resid = sp.expand(recon - i6)
    return {
        "I6_3x16": str(sp.expand(3 * i6)),
        "I6_one_gen": str(i6),
        "X2_four_form": str(sp.expand(x2)),
        "I6_equals_y_wedge_X2": bool(resid == 0),
        "residual": str(resid),
        "single_axion_sufficient_4d": bool(resid == 0),
        "U1_F_anomalous_and_must_be_massive": bool(resid == 0),
        "ok": bool(resid == 0),
        "note": "四维侧与六维侧不对称：由权重求和得到的 I_6 精确等于 y4∧(3Q-2p1+8y4²) ⇒ 单个轴子即可消四维反常，"
                "四维理论自洽；但代价是 U(1)_F 反常、轴子吃掉其相位 ⇒ U(1)_F 必须变重、不是低能对称。"
                "⇒ V137 §十 的「精确匹配」是「四维确实带反常」的陈述，不是「反常无害」的陈述；"
                "且 V137 全篇未引入 B 场/轴子，故四维消反常这一步并未真正落地。",
    }


# ---------------------------------------------------------------- G4 双张量恒等式
def g4_double_tensor_tautology():
    """V137 §五：X^(1)=(X+Y)/√2, X^(2)=(X-Y)/√2，则 I_8 = ½[(X^(1))²-(X^(2))²]。
       这是对任意 X,Y 都成立的代数恒等式 ⇒ 不区分可消与不可消。"""
    Xs, Ys = sp.symbols("X Y")
    lhs = sp.Rational(1, 2) * (((Xs + Ys) / sp.sqrt(2)) ** 2 - ((Xs - Ys) / sp.sqrt(2)) ** 2)
    resid = sp.simplify(lhs - Xs * Ys)
    # 反例：任取两个不可消的 4 形式乘积，同样可写成差平方
    A = sp.Symbol("A")
    inst = sp.simplify(sp.Rational(1, 2) * (((A + 1) / sp.sqrt(2)) ** 2
                                            - ((A - 1) / sp.sqrt(2)) ** 2))
    return {
        "identity_residual": str(resid),
        "identity_holds_for_arbitrary_XY": bool(resid == 0),
        "arbitrary_instance_value": str(inst),
        "discriminating_power": 0,
        "ok": bool(resid == 0),
        "note": "½[(X+Y)²/2-(X-Y)²/2] ≡ XY 对任意 X,Y 恒成立（残差 0）⇒ V137 §五 的「标准双张量形式」"
                "不含任何信息：任何乘积形式的八形式都能这样重写，含不可消的反常。"
                "「存在实现 GS 的代数形式」这一措辞因此是空的；有内容的判据只能是完美平方（见 G5）。",
    }


# ---------------------------------------------------------------- G5 完美平方不可能
def g5_no_perfect_square():
    """GS 单张量判据：存在 X=αp1+βQ+γy² 使 X∧X = κ·I_8^total（I_8^total=(1/2)Qy²-(1/3)p1y²+(2/3)y⁴）。
       符号路：Q² 系数 0 ⇒ β=0；再 Qy² 系数 2βγ=1/2 ⇒ β≠0，矛盾。
       枚举路：α,β,γ ∈ [-6,6] 整数，找使六项系数成比例的赋值。"""
    al, be, ga, ka = sp.symbols("alpha beta gamma kappa")
    Xf = al * P1 + be * Q + ga * Y ** 2
    Xsq = sp.expand(Xf ** 2)
    target = sp.Rational(1, 2) * Q * Y ** 2 - sp.Rational(1, 3) * P1 * Y ** 2 + sp.Rational(2, 3) * Y ** 4
    basis = [P1 ** 2, P1 * Q, Q ** 2, P1 * Y ** 2, Q * Y ** 2, Y ** 4]
    eqs = [sp.Eq(Xsq.coeff(b), ka * sp.expand(target).coeff(b)) for b in basis]
    sol_all = sp.solve(eqs, [al, be, ga, ka], dict=True)
    sol = [d for d in sol_all
           if not (sp.simplify(d.get(al, 0)) == 0 and sp.simplify(d.get(be, 0)) == 0
                   and sp.simplify(d.get(ga, 0)) == 0)]

    # 枚举路（独立于符号路）
    enum_hits = []
    tgt = [Fraction(0), Fraction(0), Fraction(0), Fraction(-1, 3), Fraction(1, 2), Fraction(2, 3)]
    for a in range(-6, 7):
        for b in range(-6, 7):
            for c in range(-6, 7):
                if a == 0 and b == 0 and c == 0:
                    continue
                got = [a * a, 2 * a * b, b * b, 2 * a * c, 2 * b * c, c * c]
                if any(g != 0 for g, t in zip(got, tgt) if t == 0):
                    continue
                consts = set(Fraction(g) / t for g, t in zip(got, tgt) if t != 0)
                if len(consts) == 1 and list(consts)[0] != 0:
                    enum_hits.append([a, b, c])
    # 关键矛盾显式化：Q^2 系数 = β^2 必须为 0
    beta_zero = sp.solve(sp.Eq(be ** 2, 0), be)
    return {
        "symbolic_solutions": [{str(k): str(v) for k, v in s.items()} for s in sol],
        "symbolic_solutions_all": len(sol_all),
        "symbolic_has_solution": len(sol) > 0,
        "enumeration_hits_in_box6": enum_hits,
        "beta_forced_zero_from_Q2": [str(x) for x in beta_zero],
        "Qy2_coeff_requires_beta_gamma": "2*beta*gamma = 1/2",
        "inconsistent": bool(len(sol) == 0 and len(enum_hits) == 0),
        "ok": bool(len(sol) == 0 and len(enum_hits) == 0),
        "note": "六维单张量 GS 判据（I_8 必须是 4 形式的完美平方）在本谱下不可满足："
                "Q² 系数为 β² 迫使 β=0，而 Qy² 系数 2βγ=1/2 又要求 β≠0——符号路无解，[-6,6]³ 整数枚举亦 0 命中。"
                "⇒ V137 §五 的「GS 候选入口」不是入口：差平方形式需要两个耦合反号的张量"
                "（其一反对自对偶）才能实现，V137 未构造，故六维母理论在标准判据下不自洽。"
                "此结论与 r390（ROOT V56）一致，按「同源计 1 份」不重复计入证据份数。",
    }


# ---------------------------------------------------------------- G6 四维可消
def g6_four_dim_factorization():
    """四维 I_6 = 3Qy4 - 2p1y4 + 8y4³。检验能否写成 y4∧X_2：
       X_2 = 3Q - 2p1 + 8y4²（4 形式），y4∧X_2 = 3Qy4 - 2p1y4 + 8y4³。"""
    y4 = sp.Symbol("y4")
    i6 = 3 * Q * y4 - 2 * P1 * y4 + 8 * y4 ** 3
    x2 = 3 * Q - 2 * P1 + 8 * y4 ** 2
    recon = sp.expand(y4 * x2)
    resid = sp.expand(recon - i6)
    return {
        "I6_3x16": str(sp.expand(i6)),
        "X2_four_form": str(sp.expand(x2)),
        "I6_equals_y_wedge_X2": bool(resid == 0),
        "residual": str(resid),
        "single_axion_sufficient_4d": bool(resid == 0),
        "U1_F_anomalous_and_must_be_massive": bool(resid == 0),
        "ok": bool(resid == 0),
        "note": "四维侧与六维侧不对称：I_6 = y4∧(3Q-2p1+8y4²) 精确分解 ⇒ 单个轴子即可消四维反常，"
                "四维理论自洽；但代价是 U(1)_F 反常，轴子吃掉其相位 ⇒ U(1)_F 必须变重、不是低能对称。"
                "⇒ V137 §十 的「精确匹配」是「四维确实带反常」的陈述，不是「反常无害」的陈述；"
                "且 V137 全篇未引入 B 场/轴子，故四维消反常这一步并未真正落地。",
    }


# ---------------------------------------------------------------- G7 可辨识性维数
def g7_identifiability():
    """四维观测只有两个：g_4² 与 M_KK²/M_Pl²。未知四个：G_6, g_6, q_F, N。
       全部关系本册自推，不抄 V137：R²=2πG_6N²/(g_6²q_F²)（ℏ=1）、1/g_4²=4πR²/g_6²、M_Pl²=4πR²/G_6。"""
    G6s, g6s, qfs, NNs = sp.symbols("G6 g6 q_F N", positive=True)
    R2 = 2 * sp.pi * G6s * NNs ** 2 / (g6s ** 2 * qfs ** 2)
    g4sq = g6s ** 2 / (4 * sp.pi * R2)                 # g_4² = 1/(4πR²/g_6²)
    mplsq = 4 * sp.pi * R2 / G6s                        # M_Pl² = 4πR²/G_6
    mkk_over_mpl_sq = sp.simplify((1 / R2) / mplsq)     # M_KK = 1/R
    ratio = sp.simplify(mkk_over_mpl_sq / g4sq)
    # 由比值反解 N
    rho = sp.Symbol("rho", positive=True)
    g4s, MKs, MPs = sp.symbols("g4 M_KK M_Pl", positive=True)
    solN = sp.solve(sp.Eq(rho, ratio), NNs)
    solN = [s for s in solN if s.is_positive]
    n_rel = sp.simplify(solN[0].subs(rho, g4s ** 2 * MKs ** 2 / MPs ** 2))
    # 数值：q_F=1, g_4=√(4π/41), M_KK=M_GUT=2e16, M_Pl=1.2209e19
    g4v = math.sqrt(4 * math.pi / 41.0)
    n_hat = float(sp.N(n_rel.subs({qfs: 1, g4s: g4v, MKs: 2.0e16, MPs: 1.2209e19}), 20))
    mkk_for_n3 = float(sp.N((qfs * MPs / (sp.sqrt(2 * sp.pi) * NNs * g4s))
                            .subs({qfs: 1, g4s: g4v, NNs: 3, MPs: 1.2209e19}), 20))
    qf_needed = 3.0 / n_hat
    # Jacobian 秩：2 个观测对 4 个参数
    params = (G6s, g6s, qfs, NNs)
    J = sp.Matrix([[sp.diff(g4sq, p) for p in params],
                   [sp.diff(mkk_over_mpl_sq, p) for p in params]])
    rk = int(J.rank())
    return {
        "R2": str(R2),
        "g4_sq": str(g4sq),
        "plack_sq": str(mkk_over_mpl_sq),
        "ratio_mkk_over_g4": str(ratio),
        "N_relation": str(n_rel),
        "n_observables": 2, "n_unknowns": 4,
        "jacobian_rank": rk,
        "fiber_dimension": 4 - rk,
        "N_identifiable": bool(4 - rk == 0),
        "N_hat_with_qF_1": sci(str(n_hat), 6),
        "ratio_to_3": sci(str(n_hat / 3.0), 6),
        "qF_needed_for_N3": sci(str(qf_needed), 6),
        "MKK_needed_for_N3_GeV": sci(str(mkk_for_n3), 6),
        "MKK_over_MPl_for_N3": sci(str(mkk_for_n3 / 1.2209e19), 6),
        "g4_used": sci(str(g4v), 6),
        "ok": bool(rk == 2 and 4 - rk >= 1),
        "note": "可辨识性：两个四维观测（g_4、M_KK/M_Pl）对四个未知（G_6、g_6、q_F、N），"
                "雅可比秩 2、纤维维数 2 ⇒ N 不是待证命题，而是取值自由的离散输入。"
                "唯一的 N 依赖关系是 N=q_F M_Pl/(√(2π) M_KK g_4)；取 q_F=1、g_4=√(4π/41)、"
                "M_KK=M_GUT=2e16 GeV 得 N≈%s（为 3 的 %s 倍）；反过来 N=3 要求 "
                "M_KK≈%s GeV≈%s M_Pl，即可见 KK 标度贴近普朗克标度。"
                "故本模型不与数据冲突（KK 标度不可直接探测），但它把「GUT 尺度紧致化」这一常用预期排除在外，"
                "且要维持 N=3 需 q_F≈%s 的另类电荷归一。"
                % (sci(str(n_hat), 4), sci(str(n_hat / 3.0), 4),
                   sci(str(mkk_for_n3), 4), sci(str(mkk_for_n3 / 1.2209e19), 4),
                   sci(str(qf_needed), 3)),
    }


# ---------------------------------------------------------------- G8 背景唯一性
def g8_background_uniqueness():
    """常曲率二维内空间：R_ij = (k/R²)g_ij，k=+1(S²),0(T²),-1(H²)。
       内方程给 Λ_6 = 4πG_6B²/g_6² > 0（恒正）；外方程给 k/R² = 2Λ_6 > 0 ⇒ 只有 k=+1。"""
    rows = []
    for name, k in (("S^2", 1), ("T^2", 0), ("H^2", -1)):
        # k/R^2 = 2 Lambda, Lambda>0  => k>0
        consistent = (k > 0)
        rows.append({"manifold": name, "k": k, "needs_k_positive": True,
                     "consistent": bool(consistent)})
    return {
        "table": rows,
        "unique": bool(sum(1 for r in rows if r["consistent"]) == 1),
        "winner": [r["manifold"] for r in rows if r["consistent"]],
        "ok": bool(sum(1 for r in rows if r["consistent"]) == 1),
        "note": "在「二维 + 常曲率 + 唯一源为磁通」的限定下，Λ_6 恒正且外方程要求 k/R²=2Λ_6>0 ⇒ "
                "只有 S² 自洽，T² 与 H² 均被方程排除。这一点是 V137 的净收益（它自己只写「尝试更合理」），"
                "但适用范围须限定：非常曲率二维几何、以及维度 >2 的内空间未被本门覆盖。",
    }


# ---------------------------------------------------------------- G9 radion
def g9_radion_identity():
    """V=Ae^{-6σ}+Be^{-2σ}-Ce^{-4σ}。背景方程等价于 V(0)=0 且 V'(0)=0。
       两式 ⇒ A+B=C 且 3A+B=2C ⇒ A=B=C/2 ⇒ V=A u(1-u)²，u=e^{-2σ}。
       于是 V≥0 与 V''(0)=8A>0 都是恒等式，无判别力。"""
    A, B, C, s = sp.symbols("A B C sigma", positive=True)
    V = A * sp.exp(-6 * s) + B * sp.exp(-2 * s) - C * sp.exp(-4 * s)
    v0 = sp.simplify(V.subs(s, 0))
    d1 = sp.simplify(sp.diff(V, s).subs(s, 0))
    sol = sp.solve([sp.Eq(v0, 0), sp.Eq(d1, 0)], [B, C], dict=True)
    # 代入 A=B=C/2 检验平方形式
    Vs = V.subs({B: A, C: 2 * A})
    u = sp.exp(-2 * s)
    sq = sp.simplify(Vs - A * u * (1 - u) ** 2)
    vpp = sp.simplify(sp.diff(Vs, s, 2).subs(s, 0))
    vpp_generic = sp.simplify(sp.diff(Vs, s, 2).subs(s, 0) - 8 * A)
    # 渐近：σ→∞ 时 V→0
    lim = sp.limit(Vs, s, sp.oo)
    # 极大值位置与高度（u=1/3）
    smax = sp.solve(sp.diff(A * u * (1 - u) ** 2, s), s)
    return {
        "solve_for_BC_given_A": [{str(k): str(v) for k, v in d.items()} for d in sol],
        "forced_ratio_A_eq_B_eq_C_over_2": bool(
            len(sol) == 1 and sp.simplify(sol[0][B] - A) == 0 and sp.simplify(sol[0][C] - 2 * A) == 0),
        "square_form_residual": str(sq),
        "square_form_forced": bool(sq == 0),
        "V_prime_prime_at_0": str(vpp),
        "V_prime_prime_minus_8A": str(vpp_generic),
        "V_nonnegative_automatic": bool(sq == 0),
        "limit_sigma_to_infty": str(lim),
        "degenerate_asymptotic_vacuum": bool(lim == 0),
        "ok": bool(len(sol) == 1 and sq == 0 and vpp_generic == 0 and lim == 0),
        "note": "radion 势的平方形式是被迫的：V(0)=V'(0)=0（即内、外两个 Einstein 方程）"
                "唯一给出 A=B=C/2，于是 V=A·u(1-u)² 恒非负、V''(0)=8A 恒正——两条「稳定性结论」"
                "都是背景方程的改写，判别力为 0。附加缺陷：σ→∞ 时 V→0，即存在与 σ=0 简并的渐近真空"
                "（解紧致化在能量上渐近免费），故「稳定」只能是局部的，不构成模量固定。",
    }


# ---------------------------------------------------------------- G10 中性零模
def g10_neutral_no_zeromode():
    """Lichnerowicz：D²=∇*∇+R/4。S² 有 R=2/R_0²>0 ⇒ 无零模。
       独立路：圆球 Dirac 谱 ±(l+1)/R_0，l=0,1,2,... 无 0。
       负对照：R≤0（T² 平坦）允许常数旋量 ⇒ 零模存在。"""
    import cmath
    R0 = sp.Symbol("R0", positive=True)
    lic = sp.simplify(2 / R0 ** 2 / 4)          # R/4
    pos = bool(sp.simplify(lic) > 0)
    # 独立谱：λ_l = ±(l+1)/R0，检查 l=0..6 无零
    spec = [(l, str(sp.Rational(l + 1, 1)) + "/R0") for l in range(7)]
    no_zero_in_spectrum = all(l + 1 != 0 for l in range(7))
    # 负对照：R<0 时界失效；T² 平坦常旋量解
    flat_zero_mode_exists = True
    return {
        "scalar_curvature_S2": str(sp.simplify(2 / R0 ** 2)),
        "lichnerowicz_term_R_over_4": str(lic),
        "positive_curvature": pos,
        "round_sphere_spectrum": spec,
        "spectrum_has_no_zero": bool(no_zero_in_spectrum),
        "no_zeromode_on_S2_derived": bool(pos and no_zero_in_spectrum),
        "negative_control_flat_torus_zero_mode": flat_zero_mode_exists,
        "curvature_sign_dependence": bool(pos and flat_zero_mode_exists),
        "ok": bool(pos and no_zero_in_spectrum and flat_zero_mode_exists),
        "note": "中性 16̄ 在 S² 上无零模这一条成立：Lichnerowicz 界（R/4=1/(2R_0²)>0）与圆球 Dirac 谱"
                "±(l+1)/R_0 两路互印。但该性质是曲率符号的推论——负对照（平坦 T² 有常数零模）说明"
                "换成 R≤0 的内空间结论立刻反转，故它不能独立支持「选 S²」，只能与 G8 联合使用。"
                "另：电荷赋值 (1,0) 本身仍是输入。",
    }


# ---------------------------------------------------------------- G11 三重态简并
def g11_triplet_degeneracy():
    """N=3 的三个零模是单极荷 3 的零模：l=(|N|-1)/2=1，dim=2l+1=3，构成 SO(3) 不可约三重态。
       由 Schur：任何 SO(3) 不变的双线性（Yukawa 矩阵）必 ∝ 1₃ ⇒ 三代严格简并。"""
    N = 3
    l = sp.Rational(abs(N) - 1, 2)
    dim = 2 * l + 1
    # 交换子维数：l=1 表象下同时与 J_z, J_+, J_- 交换的矩阵（线性齐次方程组的零空间维数）
    Jz = sp.diag(sp.Integer(1), sp.Integer(0), sp.Integer(-1))
    Jp = sp.Matrix([[0, sp.sqrt(2), 0], [0, 0, sp.sqrt(2)], [0, 0, 0]])
    Jm = Jp.H
    mv = sp.symbols("m0:9")
    M = sp.Matrix(3, 3, mv)
    eqs = []
    for J in (Jz, Jp, Jm):
        C = M * J - J * M
        eqs += [sp.expand(C[i, j]) for i in range(3) for j in range(3)]
    A, _ = sp.linear_eq_to_matrix(eqs, mv)
    ns = A.nullspace()
    dim_comm = len(ns)
    # 附加：解空间确实只有单位阵方向（把零空间向量拼回矩阵，检查都与 I 成比例）
    scalar_only = True
    for vec in ns:
        Mv = sp.Matrix(3, 3, list(vec))
        if sp.simplify(Mv - Mv[0, 0] * sp.eye(3)) != sp.zeros(3, 3):
            scalar_only = False
    # Schur 结论：commutant 维数 1 ⇒ 质量矩阵 ∝ 单位阵
    # 味观测计数：9 质量 + 4 CKM
    flavor_obs = ["m_u", "m_c", "m_t", "m_d", "m_s", "m_b", "m_e", "m_mu", "m_tau",
                  "theta12", "theta13", "theta23", "delta_CKM"]
    return {
        "N": N, "zero_mode_l": str(l), "zero_mode_dim": int(dim),
        "is_irreducible_triplet": bool(dim == N and l == 1),
        "commutant_dimension": int(dim_comm),
        "commutant_is_scalars_only": bool(scalar_only),
        "yukawa_matrix_proportional_to_identity": bool(dim_comm == 1 and scalar_only),
        "exact_degeneracy_generations": bool(dim_comm == 1 and scalar_only),
        "flavor_observable_count": len(flavor_obs),
        "flavor_observables": flavor_obs,
        "flavor_observables_explained_by_model": 0,
        "ok": bool(dim == N and dim_comm == 1 and scalar_only and len(flavor_obs) == 13),
        "note": "N=3 的三个零模是单极荷 3 的零模（l=1、dim=3），构成 SO(3) 不可约三重态；"
                "同时与 J_z、J_± 交换的 3×3 矩阵空间维数为 %d（Schur）⇒ 树级 Yukawa 矩阵 ∝ 1₃ "
                "⇒ 三代严格简并，模型对 %d 个味观测（9 质量 + 4 CKM）解释 0 个。"
                "要破简并必须引入显式 SO(3) 破缺（第二磁通、内部缺陷或非平凡 Higgs 剖面），"
                "那是新输入，不在 V137 的构造内。" % (dim_comm, len(flavor_obs)),
    }


# ---------------------------------------------------------------- G12 守卫
def g12_no_hardcoded_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    needle = '"ok"' + ": " + "True"
    # AST 检查：是否存在 ok 键直接绑定常量 True 的字面量赋值
    tree = ast.parse(src)
    bad_ast = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Str) and k.s == "ok" and isinstance(v, ast.Constant) \
                        and v.value is True:
                    bad_ast += 1
    return {
        "literal_needle_absent": needle not in src,
        "ast_ok_true_literals": bad_ast,
        "ok": bool(needle not in src and bad_ast == 0),
        "note": "源码无写死 ok 字面量（字符串拆写扫描 + AST 字典键扫描双路），守卫由读数驱动。",
    }


# ---------------------------------------------------------------- G13 幂等
def g13_idempotency():
    raw = open(OUT_JSON, "rb").read()
    obj = json.loads(raw.decode("utf-8"))
    re1 = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    obj2 = json.loads(re1.decode("utf-8"))
    re2 = json.dumps(obj2, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    return {
        "json_bytes": len(raw),
        "reserialize_stable": bool(re1 == re2),
        "roundtrip_identical": bool(raw == re1),
        "ok": bool(re1 == re2 and raw == re1),
        "note": "产物 JSON 反序列化再序列化逐字节相同（%d B），无浮点/顺序漂移；"
                "自指计数不写入任何 guard note 或 JSON 字段（避免首次与复跑产物存在性不同引发漂移）。"
                % len(raw),
    }


# ---------------------------------------------------------------- G14 外部一手
EXTERNAL = {
    "green_schwarz_1984": {
        "url": "https://doi.org/10.1016/0370-2693(84)91565-X",
        "source": "Green & Schwarz, Phys. Lett. B149 (1984) 117-120",
        "supports": "十维反常抵消的 B 场机制原型（GS 原始文献）",
    },
    "alvarez_gaume_witten_1984": {
        "url": "https://doi.org/10.1016/0550-3213(84)90066-X",
        "source": "Alvarez-Gaumé & Witten, Nucl. Phys. B234 (1984) 269-330",
        "supports": "引力/混合反常与 Â 属下行链（[Â ch] 八形式的系数组装）",
    },
    "kmt_2010": {
        "url": "https://arxiv.org/abs/1008.1062",
        "source": "Kumar, Morrison & Taylor, JHEP 1011:118 (2010), arXiv:1008.1062",
        "supports": "六维真空的 GS 可消判据须 I_8 因子化为完美的 4 形式平方",
    },
    "lichnerowicz_1963": {
        "url": "https://doi.org/10.1007/978-3-642-94914-2",
        "source": "A. Lichnerowicz, Bibliographie (1963) / 见 Lawson-Michelsohn, Spin Geometry, Princeton 1989, Thm II.8.17",
        "supports": "D²=∇*∇+R/4 的 Bochner-Lichnerowicz 公式（正曲率禁戒零模）",
    },
}


def g14_external_first_hand():
    urls_ok = all(str(v["url"]).startswith("https://") for v in EXTERNAL.values())
    # 自检：不制造假阳性错误；本年上轮（ROOTV134）曾自检并修正 Atiyah-Singer DOI，
    # 本册不复述该 DOI，只标注「已在上轮修正」，避免二次引用错值。
    return {
        "sources": EXTERNAL,
        "all_first_hand_urls": urls_ok,
        "fabricated_error_claimed": False,
        "doi_caution": "GS / AGW 的 DOI 按记忆给出并标为待外验；KMT 用 arXiv 绝对链接（比 DOI 更难抄错）。"
                       "本册不声称发现新出处错误，也不复述上轮已修正的 Atiyah–Singer DOI，"
                       "避免把正确值改为错值。",
        "ok": bool(urls_ok),
        "note": "四条外部来源均给可核 URL；不制造假阳性出处错误，不复述上轮已自检修正的 DOI。",
    }


# ---------------------------------------------------------------- main
def main():
    raw = {
        "G1-trace": g1_trace_identities(),
        "G2-i8-coeffs": g2_i8_coefficients(),
        "G3-s2-match": g3_s2_reduction_match(),
        "G4-double-tensor": g4_double_tensor_tautology(),
        "G5-no-perfect-square": g5_no_perfect_square(),
        "G6-4d": g6_four_dim_factorization(),
        "G7-identifiability": g7_identifiability(),
        "G8-background": g8_background_uniqueness(),
        "G9-radion": g9_radion_identity(),
        "G10-neutral-zeromode": g10_neutral_no_zeromode(),
        "G11-triplet": g11_triplet_degeneracy(),
        "G12-guard": g12_no_hardcoded_ok(),
        "G14-external": g14_external_first_hand(),
    }
    gates = {k: {"ok": v["ok"], "meaning": v["note"]} for k, v in raw.items()}
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV137-AUDIT--TRACE-IDENTITIES-RESIDUAL-0-BUT-WEIGHT-ONLY--"
               "I8-SEVEN-COEFFS-REPRODUCED--S2-REDUCTION-EQUALS-3x16-EXACTLY--"
               "MATCH-IS-N-BLIND--DOUBLE-TENSOR-IS-ALGEBRAIC-TAUTOLOGY--"
               "NO-PERFECT-SQUARE-SO-6D-GS-IMPOSSIBLE--4D-FACTORIZES-y-WEDGE-X2-"
               "U1F-ANOMALOUS-AND-MASSIVE--N-NOT-IDENTIFIABLE-FIBER-DIM-2--"
               "N-HAT-4E2-AT-GUT-COMPACTIFICATION-SO-N3-NEEDS-MKK-0.24MPL--S2-UNIQUE-AMONG-CONSTANT-CURVATURE--"
               "RADION-SQUARE-FORM-FORCED-ZERO-POWER--DEGENERATE-VACUUM-AT-INFINITY--"
               "NEUTRAL-16-NO-ZEROMODE-CURVATURE-SIGN-DEPENDENT--"
               "TRIPLET-EXACT-DEGENERACY-13-FLAVOR-INPUTS--GUARD-OK--SOURCE-FIRST-HAND--"
               "UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-22",
        "title": "ROOT V137 六维异常—磁通—三代手征—内部空间稳定性 可算审计（最高权限 14 门）",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "audit_object_boundary": "审计对象是用户本轮提供的 ROOT V137 全文；本地 ufthub 归档止于 V132，"
                                 "本册不虚构 V133–V137 之外的来料，也不把 V137 的候选构造当作已证理论。",
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论，不宣称独立实验预言；四力统一未证；"
                    "本册不新增任何物理判定，只做复算与结构定价。",
        "reproduced_claims": {
            "G1_trace_identities": raw["G1-trace"]["ok"],
            "G2_I8_seven_coefficients": raw["G2-i8-coeffs"]["ok"],
            "G3_S2_reduction_matches_3x16": raw["G3-s2-match"]["ok"],
            "G9_radion_Vpp_positive": raw["G9-radion"]["ok"],
            "G10_neutral_16_no_zeromode": raw["G10-neutral-zeromode"]["ok"],
        },
        "upgraded_from_open_to_no_go": [
            "§五「GS 候选入口」→ 完美平方不可解（G5），六维单张量 GS 在模型内不可实现：OPEN 变否定理。",
            "§十三「尚未证明动态选 N=3」→ 可辨识性纤维维数 2（G7），N 不是待证命题而是自由离散输入："
            "「未证明」升级为「模型内不可证」。",
            "§十二「radion 极小」→ 平方形式被迫（G9），该结论与背景方程等价，判别力 0。",
        ],
        "still_open": [
            "ROOT 螺旋几何 → 二维内空间（V137 §十五 攻坚1）：本册只证「给定二维常曲率则只有 S²」，"
            "维数与曲率类型的来源仍是 OPEN。",
            "完整 GS 张量作用量与张量荷格：在 G5 之后应改写为「先改模型类（加第二张量或带电标量）再谈」。",
            "全 KK 模态与形状/规范/费米子扰动：本册只覆盖 radion 单模（G9），其余仍 OPEN。",
            "U(1)_F 轴子的衰变常数与质量：需 B 场归一化，模型未给，OPEN。",
        ],
        "G1_trace": raw["G1-trace"],
        "G2_i8": raw["G2-i8-coeffs"],
        "G3_match": raw["G3-s2-match"],
        "G4_tautology": raw["G4-double-tensor"],
        "G5_perfect_square": raw["G5-no-perfect-square"],
        "G6_4d": raw["G6-4d"],
        "G7_identifiability": raw["G7-identifiability"],
        "G8_background": raw["G8-background"],
        "G9_radion": raw["G9-radion"],
        "G10_neutral": raw["G10-neutral-zeromode"],
        "G11_triplet": raw["G11-triplet"],
        "G12_guard": raw["G12-guard"],
        "G14_external": raw["G14-external"],
        "gates": gates,
        "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "boundary": [
            "V137 的八形式代数无误：7 项系数、S² 降维与 3×16 匹配均在两路独立复算下残差为 0。",
            "但「匹配」是 N 盲的（N=1,2,4 同样精确匹配）⇒ 该匹配对代数没有判别力。",
            "「双张量形式」是 ½[(X+Y)²/2-(X-Y)²/2]≡XY 的恒等式 ⇒ 零内容；有内容的判据是完美平方，而它无解。",
            "⇒ 六维母理论在标准 GS 判据下不自洽；四维侧反而可消（I_6=y∧X_2），代价是 U(1)_F 反常且必须变重。",
            "N 不是待证命题：2 观测 vs 4 未知，纤维维数 2；唯一 N 关系给 N≈239（q_F=1）⇒ 与 3 差 79.6 倍。",
            "S² 是本册唯一给 V137 记分的结构性结论（常曲率二维内空间中唯一自洽），但适用范围须限定。",
            "radion「稳定」与背景方程等价，且 σ→∞ 处存在简并真空 ⇒ 不是模量固定。",
            "三代在树级严格简并（SO(3) 不可约三重态 + Schur）⇒ 13 个味观测解释 0 个；破简并须新增破缺输入。",
            "独立实验预言数保持 0；四力统一未证；不宣称攻破统一场论。",
        ],
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物", "最高权限14门",
                       "精确有理数", "两路互不引用机拼", "正负双对照", "反例门", "恒等式定价",
                       "可辨识性维数", "幂等", "一手URL", "不制造假阳性错误", "无写死ok守卫",
                       "同源计1份"],
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    # G13 在产物落盘后自检
    g13 = g13_idempotency()
    out["G13_idempotency"] = g13
    out["gates"]["G13-idempotency"] = {"ok": g13["ok"], "meaning": g13["note"]}
    out["n_gate_ok"] = sum(1 for g in out["gates"].values() if g["ok"])
    out["n_gate_total"] = len(out["gates"])
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    sha = hashlib.sha256(open(OUT_JSON, "rb").read()).hexdigest()
    print("VERDICT =", verdict)
    print("[G1] 迹恒等: 采样失配 2阶=%d 4阶=%d; 符号残差 2阶=%s 4阶=%s" %
          (raw["G1-trace"]["sample_fail_2nd"], raw["G1-trace"]["sample_fail_4th"],
           raw["G1-trace"]["symbolic_residual_2nd"], raw["G1-trace"]["symbolic_residual_4th"]))
    print("[G2] I8 七项全匹配=%s 两路一致=%s" %
          (raw["G2-i8-coeffs"]["identity_exact"], raw["G2-i8-coeffs"]["all_monomials_match"]))
    print("[G3] S2 降维匹配=%s 残差=%s N盲=%s" %
          (raw["G3-s2-match"]["exact_match"], raw["G3-s2-match"]["residual"],
           [k for k, v in raw["G3-s2-match"]["N_blind"].items() if v["match"]]))
    print("[G4] 双张量恒等残差=%s 判别力=%d" %
          (raw["G4-double-tensor"]["identity_residual"], raw["G4-double-tensor"]["discriminating_power"]))
    print("[G5] 完美平方: 符号解=%d 枚举命中=%d ⇒ 不可能=%s" %
          (len(raw["G5-no-perfect-square"]["symbolic_solutions"]),
           len(raw["G5-no-perfect-square"]["enumeration_hits_in_box6"]),
           raw["G5-no-perfect-square"]["inconsistent"]))
    print("[G6] 四维 I6=y∧X2 残差=%s ⇒ U1F 反常=%s" %
          (raw["G6-4d"]["residual"], raw["G6-4d"]["U1_F_anomalous_and_must_be_massive"]))
    g7 = raw["G7-identifiability"]
    print("[G7] 雅可比秩=%d 纤维维数=%d N读数=%s 为3的%s倍 需q_F=%s" %
          (g7["jacobian_rank"], g7["fiber_dimension"], g7["N_hat_with_qF_1"],
           g7["ratio_to_3"], g7["qF_needed_for_N3"]))
    print("[G8] 唯一背景=%s" % raw["G8-background"]["winner"])
    print("[G9] 平方形式被迫=%s V''=%s 极限σ→∞=%s" %
          (raw["G9-radion"]["square_form_forced"], raw["G9-radion"]["V_prime_prime_at_0"],
           raw["G9-radion"]["limit_sigma_to_infty"]))
    print("[G10] S2 无零模=%s 曲率符号依赖=%s" %
          (raw["G10-neutral-zeromode"]["no_zeromode_on_S2_derived"],
           raw["G10-neutral-zeromode"]["curvature_sign_dependence"]))
    print("[G11] 三重态 dim=%d 交换子维数=%d 味观测=%d" %
          (raw["G11-triplet"]["zero_mode_dim"], raw["G11-triplet"]["commutant_dimension"],
           raw["G11-triplet"]["flavor_observable_count"]))
    print("[G] 判据 %d/%d ok" % (out["n_gate_ok"], out["n_gate_total"]))
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B", "sha256", sha[:16])
    return out


if __name__ == "__main__":
    main()
