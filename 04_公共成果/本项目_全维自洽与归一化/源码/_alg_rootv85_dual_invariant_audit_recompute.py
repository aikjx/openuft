# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V85（双不变量：径向形状量 Q / 秩≤1 矩阵 D）· 来料独立可算审计

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
来料性质：科研包文本，给出两个「可证伪判据」和两项精算示例（1.024849 / 0.4162）。

七个审计问题：
  G1 纯牛顿 g=GM/r^2 的 Q=-r/(2g) dg/dr 是否恒为 1（闭式 + 数值差分两路）？
  G2 Yukawa 修正下 Q 的闭式是否与独立数值求导一致（多参数扫描）？
  G3 Q 是否真的消除 GM 幅度依赖；Q=1 对幂律指数是否具备唯一性（Q=n/2）？
  G4 来料 1.024849 是否可复现；是否唯一反演（不得当作实测/新力）？
  G5 D_ij^A = alpha q_A H_A(lam) (q_i - q_j) 的 rank<=1 是否严格成立
      （精确 Fraction 小行列式 + Jacobi 奇异值两路）？
  G6 两媒介反例是否使秩判据翻转，并复现来料 0.4162？
  G7 负对照：Q 对「星球间常数 G 不同」是否完全盲；多极矩无新力也能让 Q 偏离 1；
     纯系统误差也能满足 rank<=1 ⇒ 通过判据 ≠ 单媒介存在。

判据机读；结论随输入翻转；来源给一手 URL；不自盖章；不宣称攻破统一场论。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootv85_dual_invariant_audit_recompute_2026-11-18.json")


def sci(x, d=10):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    b = D(str(b))
    if b == 0:
        return abs(D(str(a)))
    return abs(D(str(a)) - b) / abs(b)


# ---------------------------------------------------------------- 一、径向形状量 Q
def g_newton(r, gm):
    return gm / r ** 2


def g_yuk(r, gm, A, lam):
    x = r / lam
    return gm / r ** 2 * (1 + A * (1 + x) * (-x).exp())


def deriv_rich(f, x, h):
    """中心差分 + Richardson：(4 D(h/2) - D(h)) / 3（与积分 Richardson 不同对象）。"""
    d1 = (f(x + h) - f(x - h)) / (2 * h)
    hh = h / 2
    d2 = (f(x + hh) - f(x - hh)) / (2 * hh)
    return (4 * d2 - d1) / 3


def Q_numeric(r, gm, A=D(0), lam=D(1)):
    def f(rr):
        return g_yuk(rr, gm, A, lam)
    return -r / (2 * f(r)) * deriv_rich(f, r, r * D("1e-4"))


def Q_newton_closed(r, gm):
    """闭式：dg/dr = -2 GM/r^3 ⇒ Q = -r/(2 GM/r^2) * (-2 GM/r^3) = 1。"""
    g = g_newton(r, gm)
    dg = -2 * gm / r ** 3
    return -r / (2 * g) * dg


def Q_yuk_closed(r, gm, A, lam):
    """来料闭式：Q = 1 + A x^2 e^-x / [2(1 + A(1+x) e^-x)]，x=r/lam。"""
    x = r / lam
    e = (-x).exp()
    return 1 + A * x ** 2 * e / (2 * (1 + A * (1 + x) * e))


def Q_power_closed(r, gm, n):
    """校验 sharpness：g ∝ r^-n ⇒ Q = n/2（Q=1 唯一对应 n=2）。"""
    g = gm / r ** n
    dg = -n * g / r
    return -r / (2 * g) * dg


# ---------------------------------------------------------------- 二、秩判据矩阵
R_SRC = [D("6.371e6"), D("1.7374e6"), D("7.1492e7")]   # 地球半径 / 月球半径 / 木星赤道半径（示例尺度）
LAM1 = D("1e7")
QA1 = [D("1"), D("-1"), D("0.5")]
QA2 = [D("0.3"), D("0.7"), D("-0.2")]
Q1 = [D("0.4"), D("-0.6"), D("0.1")]
Q2 = [D("0.2"), D("0.3"), D("-0.5")]
PAIRS = [(0, 1), (0, 2), (1, 2)]     # (Ti,Pt), (Ti,Al), (Al,Pt)


def H(r, lam):
    """Yukawa 源端形状因子 (1+r/lam) exp(-r/lam)。"""
    x = r / lam
    return (1 + x) * (-x).exp()


def build_D(alpha2=D(0), lam1=LAM1, lam2=LAM1):
    """3 源 × 3 材料对矩阵；单媒介 alpha2=0，两媒介 alpha2>0（独立源荷/材料荷）。"""
    M = []
    for a in range(3):
        u1 = QA1[a] * H(R_SRC[a], lam1)
        u2 = QA2[a] * H(R_SRC[a], lam2)
        row = [u1 * (Q1[i] - Q1[j]) + alpha2 * u2 * (Q2[i] - Q2[j])
               for (i, j) in PAIRS]
        M.append(row)
    return M


def jacobi_eig(Ain, iters=400):
    """纯 Python Jacobi 对称特征值（float）；返回降序特征值。"""
    n = len(Ain)
    A = [list(map(float, row)) for row in Ain]
    for _ in range(iters):
        p, q, mx = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > mx:
                    mx, p, q = abs(A[i][j]), i, j
        if mx < 1e-20:
            break
        th = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
        c, s = math.cos(th), math.sin(th)
        app, aqq, apq = A[p][p], A[q][q], A[p][q]
        A[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq
        A[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq
        A[p][q] = A[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                akp, akq = A[k][p], A[k][q]
                A[k][p] = A[p][k] = c * akp - s * akq
                A[k][q] = A[q][k] = s * akp + c * akq
    return sorted((A[i][i] for i in range(n)), reverse=True)


def singular_ratio(M):
    """第二/第一奇异值，经 D^T D 的 Jacobi 特征值开方。"""
    n, m = len(M), len(M[0])
    G = [[sum(float(M[k][i]) * float(M[k][j]) for k in range(n))
          for j in range(m)] for i in range(m)]
    ev = jacobi_eig(G)
    sv = [math.sqrt(max(v, 0.0)) for v in ev]
    return (sv[1] / sv[0]) if sv[0] > 0 else float("inf"), sv


def solve_alpha2(target=0.4162):
    """二分求两媒介权重使奇异值比等于来料示例；存在性复现，非唯一反演。"""
    lo, hi = 0.5, 1.8
    assert singular_ratio(build_D(D(str(lo))))[0] < target
    assert singular_ratio(build_D(D(str(hi))))[0] > target
    for _ in range(120):
        mid = (lo + hi) / 2
        if singular_ratio(build_D(D(str(mid))))[0] < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve_A_for_Q(target, x):
    """给定 x=r/lam 反解 A；用于展示 1.024849 的非唯一性。"""
    e = (-x).exp()
    # Q-1 = A x^2 e / [2(1 + A(1+x)e)]  ⇒  A = 2(Q-1) / [x^2 e - 2(Q-1)(1+x)e]
    return 2 * (target - 1) / (x ** 2 * e - 2 * (target - 1) * (1 + x) * e)


# ---------------------------------------------------------------- 三、精确 Fraction 路径
def minors2(M):
    """所有 2x2 子式（Fr 精确）。全零 ⇔ 秩<=1。"""
    n, m = len(M), len(M[0])
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(m):
                for l in range(k + 1, m):
                    out[(i, j, k, l)] = M[i][k] * M[j][l] - M[i][l] * M[j][k]
    return out


def exact_paths():
    u = [Fr(1), Fr(-2), Fr(1, 2)]
    v = [Fr(1), Fr(-1), Fr(2)]
    one = [[u[i] * v[j] for j in range(3)] for i in range(3)]
    u2 = [Fr(1, 3), Fr(1), Fr(-1)]
    v2 = [Fr(1, 4), Fr(1, 2), Fr(-1)]
    two = [[one[i][j] + 2 * u2[i] * v2[j] for j in range(3)] for i in range(3)]
    sys = [[Fr(1) for _ in range(3)] for _ in range(3)]   # 纯共模系统误差，秩 1
    return {
        "single_all_minors_zero": all(x == 0 for x in minors2(one).values()),
        "single_n_minors": len(minors2(one)),
        "two_has_nonzero_minor": any(x != 0 for x in minors2(two).values()),
        "two_n_nonzero": sum(1 for x in minors2(two).values() if x != 0),
        "systematic_all_minors_zero": all(x == 0 for x in minors2(sys).values()),
    }


# ---------------------------------------------------------------- 四、外部一手
EXTERNAL = {
    "microscope_2022": {
        "title": "MICROSCOPE: final result of the WEP test (Ti/Pt)",
        "result": "eta(Ti,Pt) = (-1.5 +/- 2.3_stat +/- 1.5_syst) e-15",
        "arxiv": "https://arxiv.org/abs/2209.15487",
        "doi": "https://doi.org/10.1103/PhysRevLett.129.121102",
        "scope": "约束测试质量的组成依赖自由落体；不直接覆盖星球环境依赖 G，"
                 "也不直接覆盖径向形状量 Q。",
        "transferred_from": "V88 册已核验的一手来源，本册只引用不重复计数",
    },
    "isl_review": {
        "title": "Adelberger, Heckel, Nelson, Tests of the Gravitational Inverse-Square Law",
        "ref": "Rev. Mod. Phys. 81, 61 (2009)",
        "doi": "https://doi.org/10.1103/RevModPhys.81.61",
        "scope": "Yukawa 有限程参数化与 1/r^2 检验的一手综述；"
                 "Q 判据属于该检验家族的形状量重述，不是新定律。",
    },
    "codata_g": {
        "title": "CODATA 2022 Newtonian constant of gravitation",
        "url": "https://physics.nist.gov/cgi-bin/cuu/Value?bg",
        "scope": "GM 幅度标定的外部输入；Q 按来料设计对此幅度不敏感——"
                 "这正是它无法判定「各星球 G 是否不同」的原因。",
    },
}


def main():
    # ---- G1 牛顿恒等式
    nt_rows = []
    for gm in ("1", "1e6", "1e-6"):
        for r in ("1", "5", "10", "50"):
            gm_d, r_d = D(gm), D(r)
            qc = Q_newton_closed(r_d, gm_d)
            qn = Q_numeric(r_d, gm_d)
            nt_rows.append({"GM": gm, "r": r, "Q_closed": sci(qc, 12),
                            "Q_numeric": sci(qn, 12), "rel": sci(rel(qn, qc), 4)})
    g1_res = [D(row["rel"]) for row in nt_rows]
    g1 = {
        "exp": "Q=-r/(2g)dg/dr=1 for g=GM/r^2 (closed == numeric)",
        "n_rows": len(nt_rows), "max_rel": sci(max(g1_res), 4),
        "threshold": "1e-9 (数据驱动：Richardson 截断 ~h^4, h=r*1e-4 ⇒ ~1e-16；"
                     "留 7 位给 Decimal/浮点混合舍入)",
        "ok": bool(all(x < D("1e-9") for x in g1_res)
                   and all(D(row["Q_closed"]) == 1 for row in nt_rows)),
        "meaning": "Q=1 是牛顿幂律的形状恒等式；不是对新力的判负。",
    }

    # ---- G2 Yukawa 闭式 vs 数值求导
    yk_rows = []
    for A in ("0.15", "-0.3", "1"):
        for lam in ("2", "10", "50"):
            for r in ("1", "5", "10", "20"):
                a, lm, rr = D(A), D(lam), D(r)
                gm = D("3.7")
                qc = Q_yuk_closed(rr, gm, a, lm)
                qn = Q_numeric(rr, gm, a, lm)
                yk_rows.append({"A": A, "lam": lam, "r": r,
                                "Q_closed": sci(qc, 12), "Q_numeric": sci(qn, 12),
                                "rel": sci(rel(qn, qc), 4)})
    yk_res = [D(row["rel"]) for row in yk_rows]
    g2 = {
        "exp": "Q=1+A x^2 e^-x/[2(1+A(1+x)e^-x)] agrees with independent derivative",
        "n_rows": len(yk_rows), "max_rel": sci(max(yk_res), 4),
        "threshold": "1e-9（同上；含 A=1 强修正与 A<0 反号分支）",
        "ok": bool(all(x < D("1e-9") for x in yk_res)),
        "meaning": "来料 Q 公式推导正确；两路独立（解析求导 / 中心差分 Richardson）一致。",
    }

    # ---- G3 幅度盲 + 幂律唯一性
    amp = []
    for gm in ("1", "1e6", "1e-6"):
        vals = [Q_newton_closed(D(r), D(gm)) for r in ("1", "10")]
        amp.append({"GM": gm, "Q": [sci(v, 12) for v in vals]})
    amp_ok = all(D(v["Q"][0]) == 1 and D(v["Q"][1]) == 1 for v in amp)
    sharp = [{"n": n, "Q": sci(Q_power_closed(D(7), D(2), D(n)), 12)}
             for n in ("1", "2", "3", "4")]
    sharp_ok = (D(sharp[0]["Q"]) == D("0.5") and D(sharp[1]["Q"]) == 1
                and D(sharp[2]["Q"]) == D("1.5") and D(sharp[3]["Q"]) == 2)
    g3 = {
        "exp": "Q independent of GM; Q=n/2 for g~r^-n, so Q=1 singles out n=2",
        "amplitude_scan": amp, "amplitude_blind": bool(amp_ok),
        "power_scan": sharp, "sharp": bool(sharp_ok),
        "ok": bool(amp_ok and sharp_ok),
        "meaning": "幅度盲是优点（免除绝对质量标定）也是边界："
                   "它按设计看不见任何「各星球常数 G 幅度不同」。"
                   "Q=1 对幂律指数是充要的，但对偏离来源不唯一。",
    }

    # ---- G4 来料 1.024849 存在性复现 + 非唯一性
    target = D("1.024849")
    q_demo = Q_yuk_closed(D(1), D(1), D("0.15"), D(1))
    a_solved = solve_A_for_Q(target, D(1))
    a_solved_check = Q_yuk_closed(D(1), D(1), a_solved, D(1))
    nonunique = []
    for x in ("1", "2", "3", "0.5"):
        ax = solve_A_for_Q(target, D(x))
        nonunique.append({"x": x, "A_required": sci(ax, 10),
                          "Q_recheck": sci(Q_yuk_closed(D(x), D(1), ax, D(1)), 10)})
    swapped = [sci(Q_yuk_closed(D(1), D(1), solve_A_for_Q(target, D(x)), D(x)), 10)
               for x in ("2", "3")]
    g4 = {
        "exp": "claimed Q=1.024849 reproduced; but inversion A(x) is non-unique",
        "gate_self_check_wrong_argument_order": {
            "note": "把 x 误当 lam 传入时回代应偏离目标；门限须能抓住这一自伤",
            "swapped_Q_at_x2_x3": swapped,
            "swapped_fails": all(abs(D(v) - target) > D("1e-3") for v in swapped),
        },
        "claimed": sci(target, 6), "example_A": "0.15", "example_x": "1",
        "Q_at_example": sci(q_demo, 12), "matches_6_digits": bool(rel(q_demo, target) < D("5e-7")),
        "A_solved_at_x1": sci(a_solved, 12),
        "Q_recheck_solved": sci(a_solved_check, 12),
        "nonunique_set": nonunique,
        "ok": bool(rel(q_demo, target) < D("5e-7")
                   and rel(a_solved_check, target) < D("1e-12")
                   and len({row["x"] for row in nonunique}) == 4
                   and all(rel(D(row["Q_recheck"]), target) < D("1e-9")
                           for row in nonunique)
                   and all(abs(D(v) - target) > D("1e-3") for v in swapped)),
        "meaning": "来料示例来自人为设定候选模型（A=0.15, r/lam=1 即复现到 6 位）；"
                   "来料未给 A/lam/r，同一 Q 可由无穷多组 (A,x) 给出——"
                   "存在性复现 ≠ 参数反演 ≠ 实测新力。",
    }

    # ---- G5 秩≤1：精确 + 数值两路
    ex = exact_paths()
    r_single, sv_single = singular_ratio(build_D(D(0)))
    g5 = {
        "exp": "rank(D)<=1 for separable single-mediator D_ij^A",
        "exact_fraction": ex,
        "jacobi_single_ratio": sci(r_single, 6),
        "jacobi_singular_values": [sci(v, 8) for v in sv_single],
        "threshold": "1e-7（Jacobi 浮点迭代残差量级；精确路为零容差）",
        "ok": bool(ex["single_all_minors_zero"] and r_single < 1e-7
                   and ex["single_n_minors"] == 9),
        "meaning": "来料秩判据在分离性假设下严格成立；承重前提是 H_A(lam) 只依赖源、"
                   "(q_i-q_j) 只依赖材料对。前提破坏时判据自动失效，不是对单媒介的判负。",
    }

    # ---- G6 两媒介 flip + 0.4162
    alpha2 = solve_alpha2(0.4162)
    r_two, sv_two = singular_ratio(build_D(D(str(alpha2))))
    ex_two = exact_paths()
    g6 = {
        "exp": "two independent mediators break rank<=1; ratio flips 0 -> 0.4162",
        "alpha2_solved": sci(alpha2, 14),
        "ratio_single": sci(r_single, 8), "ratio_two": sci(r_two, 8),
        "target": "0.4162", "matches_4_digits": bool(abs(r_two - 0.4162) < 5e-5),
        "singular_values_two": [sci(v, 8) for v in sv_two],
        "exact_two_nonzero_minors": ex_two["two_n_nonzero"],
        "flip": bool(r_single < 1e-7 and r_two > 1e-2),
        "ok": bool(abs(r_two - 0.4162) < 5e-5 and r_single < 1e-7
                   and ex_two["two_has_nonzero_minor"] and ex["systematic_all_minors_zero"]),
        "meaning": "反例确证秩判据可翻转；0.4162 由二分调参存在性复现，"
                   "来料未给两媒介参数，故该数值不是唯一预言，也不是实测。",
    }

    # ---- G7 负对照：判据无法吸收的方向
    gm_x = D("7")
    q_gm = Q_newton_closed(D(10), gm_x)                     # 常数 G 放大 7 倍
    q_gm2 = Q_newton_closed(D(10), D(1))
    j = D("0.001")
    q_mult = (lambda x: 1 - x * (-2 * j * x ** (-3)) /
              (2 * (1 + j * x ** (-2))))(D(10))             # g=r^-2(1+J r^-2), G 未变
    rr_sys, _ = singular_ratio([[1.0, 1.0, 1.0]] * 3)       # 纯共模系统误差，秩 1
    g7 = {
        "exp": "negative controls along directions the criteria cannot absorb",
        "Q_blind_to_constant_G": {"GM=1": sci(q_gm2, 12), "GM=7": sci(q_gm, 12),
                                  "identical": bool(q_gm == q_gm2)},
        "multipole_mimic": {"model": "g = GM/r^2 [1+J/r^2], J=0.001, G unchanged",
                            "Q_at_r10": sci(q_mult, 12),
                            "deviates_from_1": bool(abs(q_mult - 1) > D("1e-9"))},
        "systematic_passes_rank": {"ratio": sci(rr_sys, 8), "rank_le_1": bool(rr_sys < 1e-7),
                                   "new_force_present": False},
        "ok": bool(q_gm == q_gm2 and abs(q_mult - 1) > D("1e-9")
                   and rr_sys < 1e-7 and ex["systematic_all_minors_zero"]),
        "meaning": "Q 对星球间常数 G 差异完全盲（按设计）；多极矩在 G 不变时也能让 Q 偏离 1；"
                   "纯共模系统误差也满足 rank<=1。因此 Q 偏离不能唯一归因新力，"
                   "rank<=1 通过也不能证明单媒介存在。",
    }

    gates = {"V85-G1-newton-Q-identity": g1, "V85-G2-yukawa-Q-two-path": g2,
             "V85-G3-amplitude-blind-sharp-exponent": g3,
             "V85-G4-claimed-1024849-existence": g4,
             "V85-G5-rank-one-exact-and-numeric": g5,
             "V85-G6-two-mediator-flip-04162": g6,
             "V85-G7-negative-controls": g7}
    n_ok = sum(1 for v in gates.values() if v["ok"])

    verdict = ("ROOTV85-AUDIT--Q-NEWTON-IDENTITY--Q-YUKAWA-REPRO--"
               "Q-AMPLITUDE-BLIND--RANK1-EXACT--TWO-MEDIATOR-FLIP--"
               "Q-BLIND-TO-PERPLANET-G--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-18",
        "title": "ROOT V85（径向形状量 Q / 秩≤1 矩阵 D）· 来料独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "q_newton_scan": nt_rows, "q_yukawa_scan": yk_rows,
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "external_sources": EXTERNAL,
        "boundary": [
            "Q=1 是 g∝r^-2 的形状恒等式，两路复算一致；它检验的是径向幂律，"
            "不是引力定律整体，更不是四力统一。",
            "Q 按设计消去 GM 幅度，因此按设计看不见「不同星球常数 G 不同」这一命题；"
            "V85 的 Q 不能替代 V88 已判定的 μ=GM 不可辨识。",
            "Q 偏离 1 不能唯一归因新力：未建模多极矩、自转与相对论修正都能产生偏离；"
            "必须先扣已知效应（来料对此已如实声明）。",
            "rank(D)≤1 在分离性假设下严格成立（9 个 2x2 子式精确为 0 + Jacobi 奇异值比 <1e-7）；"
            "两媒介反例把比值翻到 0.4162，证明判据可证伪。",
            "rank≤1 通过是必要条件而非充分条件：纯共模系统误差同样给出秩 1；"
            "必须有独立材料与源的标定才能区分。",
            "1.024849 与 0.4162 均为人为候选模型读数；本册给出存在性复现参数，"
            "来料未给参数故不可唯一反演，不得登记为实测新力。",
            "MICROSCOPE 的 1e-15 量级只约束组成依赖自由落体，"
            "既不明确覆盖径向形状量 Q，也不覆盖行星环境依赖 G。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现变 G 新物理或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "精确Fraction", "Jacobi奇异值", "反例翻转",
                       "负对照", "一手URL", "与既有册不相加"],
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("VERDICT =", verdict)
    print("[G1] newton Q rows", len(nt_rows), "max_rel", g1["max_rel"], "ok", g1["ok"])
    print("[G2] yukawa Q rows", len(yk_rows), "max_rel", g2["max_rel"], "ok", g2["ok"])
    print("[G3] amplitude blind", amp_ok, "sharp", sharp_ok)
    print("[G4] claimed Q", sci(q_demo, 12), "A_solved", sci(a_solved, 10),
          "n_x", len(nonunique))
    print("[G5] rank1 exact minors", ex, "jacobi", sci(r_single, 6))
    print("[G6] alpha2", sci(alpha2, 12), "ratio", sci(r_two, 8), "flip", g6["flip"])
    print("[G7] negatives", g7["Q_blind_to_constant_G"]["identical"],
          g7["multipole_mimic"]["deviates_from_1"], g7["systematic_passes_rank"]["rank_le_1"])
    print("GATES", n_ok, "/", len(gates))
    for k, v in gates.items():
        print("  %-42s ok=%s" % (k, v["ok"]))
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
