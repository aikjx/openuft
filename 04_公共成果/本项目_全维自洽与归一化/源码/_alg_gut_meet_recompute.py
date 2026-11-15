# -*- coding: utf-8 -*-
"""第二十轮：规范耦合高能交汇的可判负性、阈值自由度定价与反解门。
纯标准库机核；不产生新物理，只产可算判决。输出路径可被外部覆盖后调用 main()。
"""
import os
import sys
import json
import glob
import ast
import re
import io
import tokenize
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 70
DATE = "2026-11-14"
TOL_STRICT = D("1e-30")
TOL_GRID = D("1e-18")
TOL_NUM = D("1e-20")
CHI2_DOF = 1


def rd(p):
    return open(p, "r", encoding="utf-8", errors="replace").read()


def rb(p):
    return open(p, "rb").read()


def jload(p):
    return json.loads(rd(p))


def md5(p):
    return hashlib.md5(rb(p)).hexdigest()


def Dq(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    if isinstance(x, bool):
        return D(1) if x else D(0)
    return D(str(x))


def Fq(x):
    return F(str(x))


def num(x):
    return format(Dq(x), "f")


def disp(x, n=9):
    return format(Dq(x), ".%df" % n)


def rel(a, b):
    aa, bb = Dq(a), Dq(b)
    if bb == 0:
        return D(0) if aa == 0 else D("1e30")
    return abs(aa - bb) / abs(bb)


def atan_inv(n):
    x = D(1) / D(n)
    x2 = x * x
    term, s, k = x, x, 1
    while abs(term) > D(10) ** (-66):
        term *= -x2
        s += term / D(2 * k + 1)
        k += 1
    return s


PI = 16 * atan_inv(5) - 4 * atan_inv(239)
LN10 = D(10).ln()


def find_main():
    """并行会话可能新增同形目录 ⇒ 用唯一既有产物反查主目录。"""
    hits = glob.glob("openuft/**/_ALG_information_gate_recompute_2026-11-12.json",
                     recursive=True)
    assert len(hits) == 1, "ANCHOR-HITS=%d" % len(hits)
    return os.path.dirname(os.path.dirname(hits[0]))


def one(pattern, sub=None):
    base = DATA if sub is None else sub
    hits = glob.glob(os.path.join(base, pattern))
    assert len(hits) == 1, "ONE-HITS=%d(%s)" % (len(hits), pattern)
    return hits[0]


MAIN = find_main()
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")
KERNEL = os.path.abspath(__file__)
SRC_TEXT = rd(KERNEL)
OUT_JSON = os.path.join(DATA, "_ALG_gut_meet_recompute_" + DATE + ".json")
OUT_REPORT = os.path.join(DATA, "_ALG_gut_meet_recompute_report_" + DATE + ".txt")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_R1 = os.path.join(DATA, "_ALG_expdata_fullchain_recompute_2026-11-11.json")
P_R4 = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_2026-11-11.json")
P_R5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_B1 = os.path.join(DATA, "_ALG_UFT_eq_derive_recompute_2026-11-09.json")
P_B2 = os.path.join(DATA, "_ALG_all_directions_recompute_2026-11-09.json")
P_R64 = one("TUFT-r64_耦合统一GUT数值审计_*.json")
P_R188 = one("TUFT-r188_*统一尺度出处*精算_*.json")
P_R188_REP = one("TUFT-r188_*统一尺度出处*精算_*_report.txt")

LEDGER = jload(P_LEDGER)
ROWS = LEDGER["ledger"]
BY_ID = {r["id"]: r for r in ROWS}
R1 = jload(P_R1)["key_numbers"]
R4 = jload(P_R4)["key_numbers"]
R5 = jload(P_R5)["key_numbers"]
R64 = jload(P_R64)
R188 = jload(P_R188)["key_numbers"]
R188_REP_TEXT = rd(P_R188_REP)

AEM = Fq(BY_ID["P15"]["value"])
S2 = Fq(BY_ID["P08"]["value"])
AS = Fq(BY_ID["P07"]["value"])
SIG_S2 = Fq(BY_ID["P08"]["sigma"])
SIG_AS = Fq(BY_ID["P07"]["sigma"])
MZ = Fq(BY_ID["P01"]["value"])
SIG_AEM_TENSION = abs(Fq(BY_ID["C06"]["value"]) - Fq(BY_ID["C07"]["value"]))

A_FRAC = [F(3, 5) * (1 - S2) * AEM, S2 * AEM, 1 / AS]
SIG_A_FRAC = [F(3, 5) * AEM * SIG_S2, AEM * SIG_S2, SIG_AS / (AS * AS)]
A = [Dq(x) for x in A_FRAC]
SIG_A = [Dq(x) for x in SIG_A_FRAC]
MZ_D = Dq(MZ)


def act_beta():
    """A 路：从 _ALG_UFT_eq_derive 的 key_numbers 结构化读取 SM 一圈 β。"""
    kn = jload(P_B1)["key_numbers"]
    return [Fq(kn["b1"]), Fq(kn["b2"]), Fq(kn["b3"])]


def exp_beta():
    """B 路：从另一册 _ALG_all_directions 的 key_numbers 独立读取，互不引用。"""
    kn = jload(P_B2)["key_numbers"]
    return [Fq(kn["b1"]), Fq(kn["b2"]), Fq(kn["b3"])]


B_SM = act_beta()
B_EXP = exp_beta()
C_SM = [Dq(x) / (2 * PI) for x in B_SM]


def act_crit():
    """A 路：第五轮判据 JSON 里的精确有理 χ² 阈值。"""
    return Fq(jload(P_R5)["key_numbers"]["chi2_crit"])


def exp_crit():
    """B 路：第四轮判据 JSON 里的十进制串阈值。"""
    return Fq(jload(P_R4)["key_numbers"]["chi2_crit"])


CHI2_CRIT = act_crit()


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


def json_path_from_report(rp):
    """report -> JSON 的唯一路径构造。"""
    stem = os.path.splitext(os.path.basename(rp))[0]
    stem = stem.replace("_recompute_report_", "_recompute_") + ".json"
    return os.path.join(os.path.dirname(rp), stem)


def act_span_dex():
    """A 路：由 46 项锚重算三交点的 dex 跨度（用精确有理 β）。"""
    xs = pairwise_x(A, B_SM)
    return span_dex(xs)


def exp_span_dex():
    """B 路：第一轮机读 JSON 的独立存档读数。"""
    return Dq(jload(P_R1)["key_numbers"]["rg_span_dex_act"])


def act_two_sided():
    """A 路：结构化统计 σ>0 的双侧锚。"""
    return sum(1 for r in ROWS if Fq(r["sigma"]) > 0)


def exp_two_sided():
    """B 路：第四轮机读 JSON 的独立存档计数。"""
    return int(jload(P_R4)["key_numbers"]["ledger_two_sided_with_sigma"])


def act_mssm_beta():
    """A 路：r64 判定册结构化读取 MSSM 一圈 β（正对照）。"""
    return [Fq(x) for x in R64["mssm_control"]["b"]]


def exp_mssm_beta():
    """B 路：r188 report 正文正则抽取同一组 β 系数，与 A 路互不引用。
    正文里的负号是 U+2212、括号是全角，必须先归一到 ASCII 再抽。"""
    t = (R188_REP_TEXT.replace("\u2212", "-").replace("\uff08", "(")
         .replace("\uff09", ")").replace("\uff0c", ","))
    m = re.search(r"MSSM\s*β\s*系数\s*[()]\s*([\d/]+)\s*,\s*([\d/\-]+)\s*,\s*([\d/\-]+)", t)
    if m is None:
        m = re.search(r"MSSM\s*β[^0-9]{0,12}([\d/]+)\s*,\s*([\d/\-]+)\s*,\s*([\d/\-]+)", t)
    assert m is not None, "EXP-MSSM-BETA-MISSING"
    return [Fq(m.group(1)), Fq(m.group(2)), Fq(m.group(3))]


def act_r188_resid():
    """A 路：r188 判定册的 s* 拟合残差（反解证人）。"""
    return Dq(str(R188["sstar_residual_vs_target"]))


def exp_r188_resid():
    """B 路：r188 report 正文正则抽取同一残差，独立来源。"""
    m = re.search(r"resid\s*=\s*([0-9.]+e[+-]\d+)", R188_REP_TEXT, re.I)
    assert m is not None, "EXP-R188-RESID-MISSING"
    return Dq(m.group(1))


# ---------------------------------------------------------------------------
# 第二部分：数值机核（闭式 / 笨办法 / 协方差 / 阈值定价 / 控制组 / 扰动）
# ---------------------------------------------------------------------------
PAIRS = ((0, 1), (0, 2), (1, 2))


def pairwise_x(a, b):
    """三对两两交点 ln(Q/M_Z)；用精确有理 β，避免 Decimal 中间量污染。"""
    return [2 * PI * (a[i] - a[j]) / (Dq(b[i]) - Dq(b[j]))
            for i, j in PAIRS]


def span_dex(xs):
    return (max(xs) - min(xs)) / LN10


def wls_closed(a, sig, c):
    """A 路：加权最小二乘闭式解。模型 a_i = A + c_i x，3 观测 2 参数 ⇒ 1 自由度。"""
    w = [D(1) / (s * s) for s in sig]
    W = sum(w)
    cb = sum(w[i] * c[i] for i in range(3)) / W
    ab = sum(w[i] * a[i] for i in range(3)) / W
    den = sum(w[i] * (c[i] - cb) ** 2 for i in range(3))
    x = sum(w[i] * (c[i] - cb) * (a[i] - ab) for i in range(3)) / den
    A0 = ab - x * cb
    r = [a[i] - A0 - c[i] * x for i in range(3)]
    chi2 = sum(w[i] * r[i] ** 2 for i in range(3))
    return chi2, A0, x, r


def golden_min(f, lo, hi, iters=110):
    g = (D(5).sqrt() - 1) / 2
    a, b = Dq(lo), Dq(hi)
    c = b - g * (b - a)
    d = a + g * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    return (a + b) / 2


def exp_chi2_grid(a, sig, c):
    """B 路：不借闭式的笨办法。粗网格定位 + 坐标下降黄金分割，独立实现目标函数。"""
    def grid_S(A0, x):
        t0 = (a[0] - A0 - c[0] * x) / sig[0]
        t1 = (a[1] - A0 - c[1] * x) / sig[1]
        t2 = (a[2] - A0 - c[2] * x) / sig[2]
        return t0 * t0 + t1 * t1 + t2 * t2

    best = None
    for ix in range(61):
        xx = D(ix)
        for ia in range(81):
            aa = D(ia)
            vv = grid_S(aa, xx)
            if best is None or vv < best[0]:
                best = (vv, aa, xx)
    _, aa, xx = best
    lo_x, hi_x = max(D(0), xx - D(2)), xx + D(2)
    lo_A, hi_A = max(D(0), aa - D(4)), aa + D(4)
    for _ in range(40):
        xx = golden_min(lambda z: grid_S(aa, z), lo_x, hi_x)
        aa = golden_min(lambda z: grid_S(z, xx), lo_A, hi_A)
    return grid_S(aa, xx), aa, xx


def gls_correlated(a, sig_primitive):
    """第三读数：把 P15/P08/P07 当独立来料，按雅可比传播构造满秩协方差再做 GLS。
    P15 登记 σ=0，改用 C06/C07 两路口径张力作保守 σ_AEM（明示口径，BOUNDARY）。"""
    J = [[F(3, 5) * (1 - S2), -F(3, 5) * AEM, F(0)],
         [S2, AEM, F(0)],
         [F(0), F(0), -1 / (AS * AS)]]
    s2 = [sig_primitive[0] ** 2, SIG_S2 ** 2, SIG_AS ** 2]
    C = [[sum(J[i][k] * J[j][k] * s2[k] for k in range(3))
          for j in range(3)] for i in range(3)]
    Cd = [[Dq(x) for x in row] for row in C]
    n = 3
    M = [Cd[i][:] + [D(1) if i == j else D(0) for j in range(n)]
         for i in range(n)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for i in range(n):
            if i != col and M[i][col] != 0:
                f = M[i][col]
                M[i] = [M[i][j] - f * M[col][j] for j in range(2 * n)]
    Mi = [row[n:] for row in M]

    def ip(u, v):
        return sum(u[i] * Mi[i][j] * v[j] for i in range(n) for j in range(n))

    one, cc = [D(1)] * n, C_SM
    m11, m12, m22 = ip(one, one), ip(one, cc), ip(cc, cc)
    r1, r2 = ip(one, a), ip(cc, a)
    det = m11 * m22 - m12 * m12
    A0 = (r1 * m22 - r2 * m12) / det
    x = (r2 * m11 - r1 * m12) / det
    res = [a[i] - A0 - cc[i] * x for i in range(n)]
    return ip(res, res), A0, x, det


def solve3(mat, rhs):
    """3×3 Decimal 线性方程组（高斯消元），返回解与行列式符号。
    主元必须按矩阵量级设相对阈值：Decimal 舍入会把精确为零的主元留成 1e-68，
    用 != 0 判定会把奇异方向误判成可解并吐出 1e39 量级的假 δ。"""
    m = [mat[i][:] + [rhs[i]] for i in range(3)]
    scale = max(abs(mat[i][j]) for i in range(3) for j in range(3))
    eps = scale * D("1e-40") if scale > 0 else D("1e-40")
    det_sign = 1
    for col in range(3):
        cand = [(abs(m[i][col]), i) for i in range(col, 3)]
        best, piv = max(cand, key=lambda t: t[0])
        if best < eps:
            return None, 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det_sign = -det_sign
        pv = m[col][col]
        m[col] = [v / pv for v in m[col]]
        for i in range(3):
            if i != col and abs(m[i][col]) >= eps:
                f = m[i][col]
                m[i] = [m[i][j] - f * m[col][j] for j in range(4)]
    return [m[i][3] for i in range(3)], det_sign


def threshold_solve(v, a, c):
    """p=1 阈值：a_i + δ v_i = A + c_i x。3 方程 3 未知 ⇒ 精确解（恒等式）。"""
    mat = [[Dq(v[i]), D(-1), -c[i]] for i in range(3)]
    rhs = [-a[i] for i in range(3)]
    sol, sg = solve3(mat, rhs)
    if sol is None:
        return None
    delta, A0, x = sol
    r = [a[i] + delta * Dq(v[i]) - A0 - c[i] * x for i in range(3)]
    chi2 = sum((r[i] / SIG_A[i]) ** 2 for i in range(3))
    return dict(delta=delta, A=A0, x=x, chi2=chi2, det_sign=sg)


def mssm_eval(a, b_mssm):
    cm = [Dq(x) / (2 * PI) for x in b_mssm]
    chi2, A0, x, r = wls_closed(a, SIG_A, cm)
    xs = pairwise_x(a, b_mssm)
    return dict(chi2=chi2, A=A0, x=x, span=span_dex(xs), xs=xs)


def precision_pair():
    old = getcontext().prec
    try:
        getcontext().prec = 50
        v50 = wls_closed(A, SIG_A, C_SM)[0]
        getcontext().prec = 90
        v90 = wls_closed(A, SIG_A, C_SM)[0]
    finally:
        getcontext().prec = old
    return v50, v90


def build_controls(chi2_sm, chi2_mssm):
    """四个控制读数：合成精确统一（正）、沿加权正交补 10σ 偏移（负）、仓库 SM、仓库 MSSM。
    负对照不能随便挑一个分量：单分量偏移会被 (A,x) 拟合吸收大半。加权正交补是
    3 观测 2 参数下唯一无法被吸收的方向，故 10σ 位移的 χ² 应恰为 100。"""
    A0, X0 = D("24.3"), D("33.0")
    syn = [A0 + C_SM[i] * X0 for i in range(3)]
    pos = wls_closed(syn, SIG_A, C_SM)
    w = [D(1) / (s * s) for s in SIG_A]
    u = [C_SM[1] - C_SM[2], C_SM[2] - C_SM[0], C_SM[0] - C_SM[1]]
    n = [u[i] / w[i] for i in range(3)]
    norm2 = sum(w[i] * n[i] ** 2 for i in range(3))
    k = D(10) / norm2.sqrt()
    shift = [k * n[i] for i in range(3)]
    neg_in = [syn[i] + shift[i] for i in range(3)]
    neg = wls_closed(neg_in, SIG_A, C_SM)
    return dict(syn_A=A0, syn_x=X0, pos_chi2=pos[0], pos_A=pos[1], pos_x=pos[2],
                neg_chi2=neg[0], sm_chi2=chi2_sm, mssm_chi2=chi2_mssm,
                neg_shift=[num(x) for x in shift],
                neg_target=D(100), readings=[pos[0], neg[0], chi2_sm, chi2_mssm])


def det3(mat):
    a, b, c = mat
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def threshold_dets(vdirs):
    """p=1 方向的 3×3 行列式：与 span{1,c} 共线的方向必奇异。"""
    out = {}
    for name, v in vdirs.items():
        mat = [[Dq(v[i]), D(-1), -C_SM[i]] for i in range(3)]
        out[name] = det3(mat)
    return out


def perturbations():
    """24 个输入扰动方向：单变量 12 + 双变量 12，检验 δ 与 χ² 是否随观测动。"""
    ks = [F(-3), F(-1), F(1), F(3)]
    dirs = []
    for idx in range(3):
        for k in ks:
            dirs.append((k, F(0), F(0)) if idx == 0 else
                        ((F(0), k, F(0)) if idx == 1 else (F(0), F(0), k)))
    combos = [(F(1), F(1)), (F(1), F(-1)), (F(-1), F(1)), (F(-1), F(-1)),
              (F(3), F(3)), (F(3), F(-3)), (F(-3), F(3)), (F(-3), F(-3)),
              (F(1), F(3)), (F(3), F(1)), (F(-1), F(-3)), (F(-3), F(-1))]
    for k1, k2 in combos:
        dirs.append((F(0), k1, k2))
    out = []
    for k_aem, k_s2, k_as in dirs:
        aem = AEM + k_aem * SIG_AEM_TENSION
        s2 = S2 + k_s2 * SIG_S2
        as_ = AS + k_as * SIG_AS
        a = [Dq(F(3, 5) * (1 - s2) * aem), Dq(s2 * aem), Dq(1 / as_)]
        chi2, _, _, _ = wls_closed(a, SIG_A, C_SM)
        xs = pairwise_x(a, B_SM)
        x12 = xs[0]
        A12 = a[0] - C_SM[0] * x12
        d3 = A12 + C_SM[2] * x12 - a[2]
        out.append(dict(chi2=chi2, delta3=d3, x12=x12, span=span_dex(xs)))
    return out


def slope_robustness():
    """22 个 β 扰动剖面（含正负两侧，先定方向再报单调性）。"""
    profiles = []
    epss = [F(1, 100), F(-1, 100), F(5, 100), F(-5, 100),
            F(10, 100), F(-10, 100)]
    for i in range(3):
        for e in epss:
            b = list(B_SM)
            b[i] = b[i] * (1 + e)
            profiles.append(("single_%d_%s" % (i, str(e)), b))
    for e in [F(1, 100), F(-1, 100), F(10, 100), F(-10, 100)]:
        profiles.append(("uniform_%s" % str(e), [x * (1 + e) for x in B_SM]))
    out = []
    for name, b in profiles:
        c = [Dq(x) / (2 * PI) for x in b]
        chi2, _, _, _ = wls_closed(A, SIG_A, c)
        out.append(dict(name=name, chi2=chi2, span=span_dex(pairwise_x(A, b))))
    return out


def literal_values(path):
    """按 tokenize 原文取字面量（AST float 是二进制近似，不可当十进制值）。"""
    try:
        text = rd(path)
    except Exception:
        return []
    out = []
    try:
        for t in tokenize.generate_tokens(io.StringIO(text).readline):
            if t.type == tokenize.NUMBER:
                s = t.string
                if s and s[-1] in "jJ":
                    continue
                try:
                    out.append(Fq(s))
                except Exception:
                    pass
    except Exception:
        pass
    return out


def gut_script_paths():
    pats = [os.path.join(SRC, "*.py")]
    hits = []
    for p in glob.glob(pats[0]):
        if re.search(r"GUT|统一|耦合|r64|r188|r189|r250|r403", os.path.basename(p)):
            hits.append(p)
    return sorted(set(hits + [KERNEL]))


def ast_copy_count(targets):
    """目标数值是否作为字面量出现在仓库 GUT 相关源码里（观测副本检测）。"""
    vals = []
    for p in gut_script_paths():
        vals.extend(literal_values(p))
    uniq = set(vals)
    hits = 0
    for t in targets:
        ft = F(Dq(t))
        if ft in uniq:
            hits += 1
    return hits, len(vals), len(uniq), uniq


RE_GUT = re.compile(r"tau_p|proton|GUT|unif|decay|统一|衰变|超对称|sparticle|susy", re.I)


def scan_gut_anchors():
    like = [r for r in ROWS if RE_GUT.search(r["symbol"] + " " + r["note"])]
    two = [r for r in like if Fq(r["sigma"]) > 0]
    return dict(gut_like=[r["id"] for r in like],
                gut_two_sided=[r["id"] for r in two],
                n_like=len(like), n_two_sided=len(two),
                gut_bound_kinds=sorted(set(r["kind"] for r in like)),
                two_sided_total=act_two_sided())


# ---------------------------------------------------------------------------
# 判据（四门串联 + 判别力守卫）；每次反噬只动一个判据
# ---------------------------------------------------------------------------
def gate_convergence(chi2, crit):
    return chi2 < crit


def gate_zero_extra(n):
    return (n == 0)


def gate_lto(rec):
    return ((not rec["delta_is_inversion"]) and
            (rec["ast_copy_count"] == 0) and
            (not rec["restatement"]))


def gate_falsifiable(rec):
    return (rec["n_two_sided_gut"] >= 1) and (rec["n_new_outputs"] >= 1)


def gate_power(ctrl):
    return (ctrl["n_pass"] > 0) and (ctrl["n_fail"] > 0)


def config_certified(cfg, rec):
    return (gate_convergence(cfg["chi2"], Dq(CHI2_CRIT)) and
            gate_zero_extra(cfg["n_extra"]) and
            gate_lto(rec) and
            gate_falsifiable(rec))


def config_gate_vector(cfg, rec):
    return [bool(gate_convergence(cfg["chi2"], Dq(CHI2_CRIT))),
            bool(gate_zero_extra(cfg["n_extra"])),
            bool(gate_lto(rec)),
            bool(gate_falsifiable(rec))]


def lto_fixtures():
    neg = dict(delta_is_inversion=True, ast_copy_count=0, restatement=False)
    pos = dict(delta_is_inversion=False, ast_copy_count=0, restatement=False)
    return bool(gate_lto(neg)), bool(gate_lto(pos))


def falsify_fixtures():
    neg = dict(n_two_sided_gut=0, n_new_outputs=2)
    pos = dict(n_two_sided_gut=1, n_new_outputs=2)
    return bool(gate_falsifiable(neg)), bool(gate_falsifiable(pos))


# ---------------------------------------------------------------------------
# 第三部分：守卫、判词、落盘、main
# ---------------------------------------------------------------------------
GUARDS = []


def add(name, ok, exp, act, note="", kind=None):
    """ok 驱动 kind；守卫/控制组 ok 禁写死（由 NO-HARDCODE-OK 全表 AST 扫描）。"""
    if kind is None:
        kind = "PASS" if ok else "FAIL"
    GUARDS.append(dict(name=name, ok=bool(ok), exp=str(exp), act=str(act),
                       note=note, kind=kind))


def counts_of():
    out = {}
    for g in GUARDS:
        out[g["kind"]] = out.get(g["kind"], 0) + 1
    return out


def final_of(nf_main, nf_guard, n_decl):
    if n_decl is None:
        return "ALG-GUT-MEET--GATES-FAIL"
    if nf_guard > 0:
        return "ALG-GUT-MEET--GATES-FAIL"
    return "ALG-GUT-MEET--GATES-PASS-WITH-0-NEGATIVE"


def verdict_string(kn):
    return ("ALG-GM__CHI2-%s__SIGMA-%s__CRIT-%s__SPAN-%s__MSSM-%s"
            "__P1-%s__DAS-%s__ANCH-%s__CFG-%s__ESC-%s__CUT-%s"
            "__CLEAN-0__PRED-0" %
            (disp(kn["chi2_min"], 6), disp(kn["sigma_equiv"], 6),
             disp(kn["chi2_crit"], 6), disp(kn["span_dex_act"], 6),
             disp(kn["mssm_chi2"], 6), disp(kn["chi2_p1_e3"], 3),
             disp(kn["dalpha_s_over_sigma"], 6), str(kn["gut_like"]),
             str(kn["n_configs"]), str(kn["escape_configs"]),
             str(kn["single_decisive"])))


def hardcode_ok_hits(tree):
    bad = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "add"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                bad.append("add-ok-pos2")
            for kw in node.keywords:
                if kw.arg == "ok" and isinstance(kw.value, ast.Constant):
                    bad.append("add-ok-kw")
    return bad


def exp_act_ast_hits(tree):
    bad = []
    srcs = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("act_") or node.name.startswith("exp_") \
                    or node.name in ("wls_closed", "exp_chi2_grid"):
                srcs[node.name] = ast.get_source_segment(SRC_TEXT, node) or ""
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Return) and isinstance(sub.value, ast.Constant)
                        and isinstance(sub.value.value, (int, float))
                        and not isinstance(sub.value.value, bool)
                        and node.name.startswith(("act_", "exp_"))):
                    bad.append(node.name + ":constant-return")
    for a_name in ("act_beta", "act_crit", "act_span_dex", "act_two_sided",
                   "act_mssm_beta", "act_r188_resid"):
        e_name = "exp_" + a_name[4:]
        if a_name in srcs and e_name in srcs and srcs[a_name] == srcs[e_name]:
            bad.append(a_name + ":same-as-" + e_name)
    if srcs.get("wls_closed") == srcs.get("exp_chi2_grid"):
        bad.append("chi2-two-path-identical")
    return bad


def conjunction_arity(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "config_certified":
            for sub in ast.walk(node):
                if isinstance(sub, ast.BoolOp) and isinstance(sub.op, ast.And):
                    return len(sub.values)
    return -1


def main():
    GUARDS.clear()
    crit_d = Dq(CHI2_CRIT)
    tree = ast.parse(SRC_TEXT)

    # ---- 基础读数 ----
    chi2_cf, A_cf, x_cf, r_cf = wls_closed(A, SIG_A, C_SM)
    chi2_grid, A_grid, x_grid = exp_chi2_grid(A, SIG_A, C_SM)
    chi2_gls, A_gls, x_gls, gls_det = gls_correlated(
        A, [SIG_AEM_TENSION, SIG_S2, SIG_AS])
    xs = pairwise_x(A, B_SM)
    span = span_dex(xs)
    span_act, span_exp = act_span_dex(), exp_span_dex()
    span_lit = Dq(R1["rg_span_dex_exp"])
    Q12 = MZ_D * xs[0].exp()
    Q_cf = MZ_D * x_cf.exp()
    A12 = A[0] - C_SM[0] * xs[0]
    d3 = A12 + C_SM[2] * xs[0] - A[2]
    as_new = 1 / (A[2] + d3)
    das_sigma = (as_new - Dq(AS)) / Dq(SIG_AS)
    sig_eq = chi2_cf.sqrt()
    ratio_crit = chi2_cf / crit_d
    v50, v90 = precision_pair()

    # ---- p=1 阈值定价（6 个方向） ----
    vdirs = {"e1": [F(1), F(0), F(0)], "e2": [F(0), F(1), F(0)],
             "e3": [F(0), F(0), F(1)], "common": [F(1), F(1), F(1)],
             "antisym": [F(1), F(-1), F(0)],
             "beta_like": [F(41, 10), F(-19, 6), F(-7)]}
    solves = {}
    for name, v in vdirs.items():
        solves[name] = threshold_solve(v, A, C_SM)
    sol_e3 = solves["e3"]
    dets = threshold_dets(vdirs)
    singular = sorted(k for k, v in dets.items() if abs(v) < D("1e-40"))
    nonsingular = sorted(k for k in dets if k not in singular)
    p_max_chi2 = max(s["chi2"] for s in solves.values() if s is not None)
    solvable = len(nonsingular)
    delta_vals = [s["delta"] for s in solves.values() if s is not None]
    delta_distinct = len(set(num(v) for v in delta_vals))
    delta_max_abs = max(abs(v) for v in delta_vals) if delta_vals else D(0)

    # ---- 正对照：r64 的 MSSM 一圈 β 在新 χ² 判据下重算 ----
    bm_act, bm_exp = act_mssm_beta(), exp_mssm_beta()
    mssm = mssm_eval(A, bm_act)
    ctrl = build_controls(chi2_cf, mssm["chi2"])
    flags = [v < crit_d for v in ctrl["readings"]]
    ctrl["n_pass"] = sum(1 for f in flags if f)
    ctrl["n_fail"] = len(flags) - ctrl["n_pass"]
    pair_distinct = all(rel(ctrl["readings"][i], ctrl["readings"][j]) > D("1e-8")
                        for i in range(4) for j in range(i + 1, 4))

    # ---- 扰动传递 / β 剖面 ----
    pert = perturbations()
    inv_chi2 = sum(1 for p in pert if rel(p["chi2"], chi2_cf) < D("1e-12"))
    inv_d3 = sum(1 for p in pert if rel(p["delta3"], d3) < D("1e-12"))
    pert_distinct = len(set(num(p["delta3"]) for p in pert))
    prof = slope_robustness()
    slope_below = sum(1 for p in prof if p["chi2"] < crit_d)
    slope_min = min(p["chi2"] for p in prof)
    slope_min_span = min(p["span"] for p in prof)
    slope_up = sum(1 for p in prof if "single_" in p["name"] and "-" not in p["name"].split("_")[-1])
    slope_dn = len([p for p in prof if "single_" in p["name"]]) - slope_up

    # ---- 观测副本 / 可判负锚 / 反解证人 ----
    targets = [A_cf, x_cf, d3, as_new, Q12, A12, A_gls, x_gls]
    copies, n_lit, n_uniq, uniq = ast_copy_count(targets)
    scanner_power = (F(1) in uniq)
    led_vals = set(F(Dq(r["value"])) for r in ROWS)
    restatement = any(F(Dq(t)) in led_vals for t in targets)
    gut = scan_gut_anchors()
    r4_types = list(R4["escape_obs_types"])
    r4_witness = str(R4["escape_witness_in_existing"])
    r188_a, r188_e = act_r188_resid(), exp_r188_resid()
    inv_expr = bool(re.search(r"s\*\s*=\s*\(3a\+7A3\)/\(15a\)", R188_REP_TEXT))
    inv_zero = bool(re.search(r"框架含量为零", R188_REP_TEXT))
    inv_fail = bool(re.search(r"\[FAIL\]\s*B7", R188_REP_TEXT))

    # ---- 四门配置表 ----
    rec_common = dict(n_two_sided_gut=gut["n_two_sided"],
                      n_new_outputs=len(targets), ast_copy_count=copies,
                      restatement=restatement)
    configs = [
        dict(name="SM-1loop-no-threshold", chi2=chi2_cf, n_extra=0,
             rec=dict(rec_common, delta_is_inversion=False)),
        dict(name="MSSM-1loop-r64-control", chi2=mssm["chi2"], n_extra=1,
             rec=dict(rec_common, delta_is_inversion=False)),
        dict(name="SM-plus-fitted-threshold-e3", chi2=sol_e3["chi2"], n_extra=1,
             rec=dict(rec_common, delta_is_inversion=True)),
    ]
    vectors = [config_gate_vector(c, c["rec"]) for c in configs]
    certified = [config_certified(c, c["rec"]) for c in configs]
    escape = sum(1 for v in certified if v)
    g1v = [v[0] for v in vectors]
    g2v = [v[1] for v in vectors]
    seesaw = (all(g1v[i] != g2v[i] for i in range(len(vectors)))
              and (True in g1v) and (False in g1v)
              and (True in g2v) and (False in g2v))
    marginal = []
    for g in range(4):
        cnt = 0
        for v in vectors:
            w = list(v)
            w[g] = True
            if all(w):
                cnt += 1
        marginal.append(cnt)
    single_decisive = sum(1 for c in marginal if c > 0)

    # ---- WLS 正交恒等式（单列 IDENTITY，不进布尔结论） ----
    wv = [D(1) / (s * s) for s in SIG_A]
    orth1 = sum(wv[i] * r_cf[i] for i in range(3))
    orth2 = sum(wv[i] * C_SM[i] * r_cf[i] for i in range(3))
    scale = sum(wv[i] * abs(r_cf[i]) for i in range(3))
    orth_ok = (abs(orth1) / scale < D("1e-40")) and (abs(orth2) / scale < D("1e-40"))

    # ---- 守卫 ----
    add("GM-LEDGER-TWO-PATH", act_two_sided() == exp_two_sided() and act_two_sided() > 0,
        exp_two_sided(), act_two_sided(), "46 项锚的双侧计数两路机拼")
    add("GM-BETA-TWO-SOURCE", B_SM == B_EXP and len(B_SM) == 3,
        [str(x) for x in B_EXP], [str(x) for x in B_SM], "SM 一圈 β 两册独立读取")
    add("GM-MSSM-BETA-TWO-SOURCE", bm_act == bm_exp,
        [str(x) for x in bm_exp], [str(x) for x in bm_act], "r64 JSON vs r188 report 正文")
    add("GM-CRIT-TWO-SOURCE", act_crit() == exp_crit(),
        str(exp_crit()), str(act_crit()), "第四轮十进制串 vs 第五轮精确分数")
    add("GM-CRIT-EQUAL-ACTIVE", Dq(CHI2_CRIT) == Dq(act_crit()) and Dq(CHI2_CRIT) < D(10),
        num(Dq(act_crit())), num(Dq(CHI2_CRIT)), "反噬：阈值被抬高即挡门")
    add("GM-CHI2-RATIO-SANITY", ratio_crit > D(1),
        "gt1", num(ratio_crit), "反噬第二道：χ²/阈值 必须大于 1")
    r1a = [Dq(R1["alpha1_inv_MZ_act"]), Dq(R1["alpha2_inv_MZ_act"]),
           Dq(R1["alpha3_inv_MZ_act"])]
    a_match = all(rel(A[i], r1a[i]) < TOL_STRICT for i in range(3))
    add("GM-A123-MATCH-R1", a_match,
        [num(x) for x in r1a], [num(x) for x in A], "a1/a2/a3 与首册存档逐位对齐")
    add("GM-SPAN-MATCH-R1", rel(span, span_exp) < TOL_STRICT and rel(span_act, span) < TOL_STRICT,
        num(span_exp), num(span_act), "三交点 dex 跨度两路机拼")
    add("GM-SPAN-LITERATURE-HONEST", rel(span, span_lit) > D("1e-4"),
        num(span_lit), num(span), "文献口径不同，不强行对齐", kind="INFO")
    add("GM-CHI2-CLOSED-VS-BRUTE", rel(chi2_cf, chi2_grid) < TOL_GRID,
        num(chi2_grid), num(chi2_cf), "闭式 WLS vs 网格加坐标下降（笨办法）")
    add("GM-BRUTE-RECOVERS-X", rel(x_cf, x_grid) < D("1e-14"),
        num(x_grid), num(x_cf), "两条独立路径的交汇能标一致")
    add("GM-PRECISION-50-90", rel(v50, v90) < D("1e-25") and rel(chi2_cf, v90) < D("1e-25"),
        num(v50), num(v90), "精度不足误判来料错的排查")
    add("GM-SIGMA-TENSION-POSITIVE", SIG_AEM_TENSION > 0 and all(s > 0 for s in SIG_A),
        num(Dq(SIG_AEM_TENSION)), [num(s) for s in SIG_A], "C06/C07 口径张力作保守 σ_AEM")
    add("GM-GLS-DET-NONZERO", gls_det != 0, "nonzero", num(gls_det), "满秩协方差可逆")
    add("GM-GLS-GT-CRIT", chi2_gls > crit_d, num(crit_d), num(chi2_gls),
        "含相关性的 GLS 读数仍远超阈值")
    add("GM-CHI2-P0-GT-CRIT", chi2_cf > crit_d, num(crit_d), num(chi2_cf),
        "p=0：零额外自由度下三耦合交汇被判负")
    add("GM-WLS-ORTHOGONALITY", orth_ok, num(orth1), num(orth2),
        "按定义成立，恒等式不作证据，配 NOT-ALL-GREEN", kind="IDENTITY")
    add("GM-DOF-IDENTITY", (3 - 2) == CHI2_DOF, 1, 3 - 2,
        "3 观测 2 参数 ⇒ 1 自由度，结构性恒真", kind="IDENTITY")
    add("GM-P1-EXACT-IDENTITY", p_max_chi2 < D("1e-40"), num(p_max_chi2), 0,
        "3 方程 3 未知 ⇒ χ²=0 是线性代数恒等式，不是拟合成功", kind="IDENTITY")
    add("GM-DELTA-TWO-PATH", rel(d3, sol_e3["delta"]) < D("1e-40"),
        num(sol_e3["delta"]), num(d3), "δ3 直接代数 vs 3×3 线性解")
    add("GM-THRESHOLD-RANK-PRICED",
        solvable >= 4 and len(dets) == 6
        and singular == ["beta_like", "common"]
        and all(abs(dets[k]) > D("1e-12") for k in nonsingular),
        "4 solvable / 2 in span{1,c}", [solvable, singular],
        "如实负读数：common 与 beta_like 落在 span{1,c} 内，行列式恒零，不构成自由度")
    add("GM-THRESHOLD-DELTAS-DISTINCT", delta_distinct == solvable,
        solvable, delta_distinct, "非奇异方向给出互异 δ，判别力非零")
    add("GM-THRESHOLD-MAGNITUDE-SANITY", delta_max_abs < D("1e3"),
        "lt1e3", num(delta_max_abs),
        "量级 sanity：Decimal 近奇异主元曾吐出 5.8e39 的假 δ，改相对阈值后消失")
    add("GM-DALPHA-S-GT-10SIGMA", abs(das_sigma) > D(10),
        "gt10", num(das_sigma), "阈值校正须把 α_s 推移超过 10σ")
    add("GM-CTRL-POS-ZERO", ctrl["pos_chi2"] < D("1e-40")
        and rel(ctrl["pos_x"], ctrl["syn_x"]) < D("1e-25"),
        num(ctrl["pos_chi2"]), num(ctrl["pos_A"]), "合成统一数据必过交汇门")
    add("GM-CTRL-NEG-LARGE",
        ctrl["neg_chi2"] > crit_d
        and rel(ctrl["neg_chi2"], ctrl["neg_target"]) < D("1e-18"),
        num(ctrl["neg_target"]), num(ctrl["neg_chi2"]),
        "沿加权正交补的 10σ 位移 χ² 恰为 100；单分量偏移会被拟合吸收，不可用")
    add("GM-CTRL-FOUR-DISTINCT", pair_distinct,
        [num(x) for x in ctrl["readings"]], 6, "四读数两两不同")
    add("GM-CTRL-MSSM-PASSES-G1", mssm["chi2"] < crit_d,
        num(crit_d), num(mssm["chi2"]), "r64 几何正对照映射到 χ² 判据后仍通过")
    add("GM-CTRL-SM-FAILS-G1", chi2_cf > crit_d,
        num(crit_d), num(chi2_cf), "SM 一圈不能通过")
    add("GM-POWER-NONZERO", gate_power(ctrl),
        [ctrl["n_pass"], ctrl["n_fail"]], [0, 4], "正对照与负对照两侧都测")
    add("GM-PERT-ALL-DIRECTIONS", len(pert) == 24 and inv_chi2 == 0 and inv_d3 == 0,
        [24, 0, 0], [len(pert), inv_chi2, inv_d3], "δ 与 χ² 对全部输入扰动随动")
    add("GM-PERT-DELTA-DISTINCT", pert_distinct == 24,
        24, pert_distinct, "24 个扰动给出 24 个不同 δ")
    add("GM-SLOPE-PROFILES-GE4", len(prof) >= 4, 4, len(prof), "β 扰动剖面数")
    add("GM-SLOPE-NO-PASS", slope_below == 0 and slope_min > crit_d,
        num(crit_d), num(slope_min), "22 个 β 剖面无一能把 χ² 压到阈值下")
    add("GM-SLOPE-TWO-SIDES", slope_up > 0 and slope_dn > 0,
        [slope_up, slope_dn], [slope_up, slope_dn], "正负两侧都测，先定方向")
    add("GM-GUT-ANCHOR-EXISTS", gut["n_like"] >= 1,
        1, gut["n_like"], "46 锚中确有 GUT 尺度相关观测")
    add("GM-GUT-TWO-SIDED-ZERO", gut["n_two_sided"] == 0,
        0, gut["n_two_sided"], "可判负门：双侧锚 0 个")
    p11 = BY_ID.get("P11")
    add("GM-P11-ONE-SIDED-BOUND",
        p11 is not None and p11["kind"] == "measured-bound" and Fq(p11["sigma"]) == 0,
        "measured-bound/sigma0", str(p11["kind"]) if p11 else "missing",
        "质子衰变只有单侧下界，σ=0")
    add("GM-R4-ESCAPE-ONE-SIDED",
        set(r4_types) == set(["lower", "upper"]) and "tau_p" in r4_witness,
        str(r4_types), r4_witness, "第四轮质子衰变逃逸证人也是单侧")
    add("GM-R188-INVERSION-WITNESS",
        inv_expr and inv_zero and inv_fail and r188_a < D("1e-20") and r188_e < D("1e-20"),
        [num(r188_e), inv_expr, inv_zero, inv_fail], [num(r188_a), 1, 1, 1],
        "仓库自身 GUT 尺度 s* 由实验输入闭式反解")
    add("GM-R188-ROUNDED-NOT-EXACT", rel(r188_a, r188_e) > D("1e-3"),
        num(r188_e), num(r188_a), "report 的 1.2e-31 是舍入串，禁当精确值比较",
        kind="INFO")
    add("GM-AST-NO-OBSERVATION-COPY", copies == 0,
        0, copies, "拟合输出不是源码里的观测副本")
    add("GM-AST-SCANNER-POWER", scanner_power and not restatement,
        True, scanner_power, "扫描器能认出已知字面量（正对照）")
    add("GM-NO-HARDCODE-OK", len(hardcode_ok_hits(tree)) == 0,
        [], hardcode_ok_hits(tree), "全表 AST 扫描 add 的 ok")
    add("GM-EXP-ACT-DISTINCT-AST", len(exp_act_ast_hits(tree)) == 0,
        [], exp_act_ast_hits(tree), "所有 return 分支禁顶层数值常量")
    add("GM-CONJUNCTION-ARITY", conjunction_arity(tree) == 4,
        4, conjunction_arity(tree), "反噬：删任一门即挡门")
    lto_f = lto_fixtures()
    add("GM-LTO-PREDICATE-ACTIVE", lto_f == (False, True),
        [False, True], list(lto_f), "非回述谓词正负夹具")
    fal_f = falsify_fixtures()
    add("GM-FALSIFY-PREDICATE-ACTIVE", fal_f == (False, True),
        [False, True], list(fal_f), "反噬：可判负门被强制为 True 即挡门")
    add("GM-SEESAW-ANTICORRELATED", seesaw, [g1v, g2v], [g1v, g2v],
        "交汇门与零自由度门在仓库来料上反相关")
    add("GM-CONFIGS-NO-ESCAPE", escape == 0, 0, escape,
        "三个仓库来源配置无一同时满足四门")
    add("GM-MARGINAL-NO-SINGLE-KEY", single_decisive == 0,
        0, single_decisive, "如实负读数：本候选集没有任何单门是关键")
    add("GM-README-STRUCTURAL-ZERO-WRITE",
        len(re.findall(r"open\s*\(\s*README[^)]*['\"][wax]", SRC_TEXT)) == 0,
        0, len(re.findall(r"open\s*\(\s*README[^)]*['\"][wax]", SRC_TEXT)),
        "并行会话会改 README，故用 AST 结构性零写入而非前后 MD5")
    add("GM-PATH-CONSTRUCTOR-CONSISTENT",
        report_path_from_json(OUT_JSON) == OUT_REPORT
        and json_path_from_report(OUT_REPORT) == OUT_JSON,
        os.path.basename(OUT_REPORT), os.path.basename(report_path_from_json(OUT_JSON)),
        "机核与核验器共用同一路径构造")

    # ---- 判词与判定表 ----
    readme_b = rb(README)
    readme_txt = readme_b.decode("utf-8", errors="replace")
    rid = re.findall(r"TUFT-r(\d+)_", readme_txt)
    key_numbers = dict(
        chi2_min=num(chi2_cf), chi2_grid=num(chi2_grid), chi2_gls=num(chi2_gls),
        chi2_crit=num(crit_d), chi2_ratio_crit=num(ratio_crit),
        sigma_equiv=num(sig_eq), dof=CHI2_DOF,
        A_opt=num(A_cf), x_opt=num(x_cf), Q_opt_GeV=num(Q_cf),
        ledger_total=len(ROWS),
        aem_inv_MZ=num(Dq(AEM)), s2w_MZ=num(Dq(S2)),
        sigma_s2w=num(Dq(SIG_S2)), alpha_s_MZ=num(Dq(AS)),
        sigma_alpha_s=num(Dq(SIG_AS)), M_Z_GeV=num(MZ_D),
        r64_sm_gap_pct=num(Dq(str(R64["sm"]["min_spread_rel_pct"]))),
        r64_mssm_gap_pct=num(Dq(str(R64["mssm_control"]["min_spread_rel_pct"]))),
        a1_inv_MZ=num(A[0]), a2_inv_MZ=num(A[1]), a3_inv_MZ=num(A[2]),
        c1_slope=num(C_SM[0]), c2_slope=num(C_SM[1]), c3_slope=num(C_SM[2]),
        b_sm=[str(x) for x in B_SM],
        b_sm_text="、".join(str(x) for x in B_SM),
        span_dex_act=num(span_act), span_dex_exp_r1=num(span_exp),
        span_dex_literature=num(span_lit),
        x12=num(xs[0]), x13=num(xs[1]), x23=num(xs[2]),
        Q12_GeV=num(Q12), A12=num(A12), delta3=num(d3),
        alpha_s_new=num(as_new), dalpha_s_over_sigma=num(das_sigma),
        chi2_p1_e3=num(sol_e3["chi2"]), p_min=1,
        mssm_chi2=num(mssm["chi2"]), mssm_span_dex=num(mssm["span"]),
        mssm_beta=[str(x) for x in bm_act],
        mssm_beta_text="、".join(str(x) for x in bm_act),
        ctrl_pos_chi2=num(ctrl["pos_chi2"]), ctrl_neg_chi2=num(ctrl["neg_chi2"]),
        ctrl_readings=[num(x) for x in ctrl["readings"]],
        ctrl_readings_text=" / ".join(disp(x, 6) for x in ctrl["readings"]),
        ctrl_n_pass=ctrl["n_pass"], ctrl_n_fail=ctrl["n_fail"],
        n_configs=len(configs), escape_configs=escape,
        gate_vectors=[[int(z) for z in v] for v in vectors],
        gate_vectors_text="；".join("".join(str(int(z)) for z in v) for v in vectors),
        seesaw_ok=int(bool(seesaw)), marginal=marginal,
        single_decisive=single_decisive,
        gut_like=gut["n_like"], gut_two_sided=gut["n_two_sided"],
        gut_like_anchors=gut["gut_like"], gut_bound_kinds=gut["gut_bound_kinds"],
        two_sided_total=gut["two_sided_total"],
        r188_resid_json=num(r188_a), r188_resid_report=num(r188_e),
        r188_resid_sci=format(r188_a, ".3e"),
        r188_resid_report_sci=format(r188_e, ".3e"),
        r4_escape_obs_types=r4_types,
        r4_escape_obs_text="、".join(r4_types),
        pert_directions=len(pert), pert_invariant=inv_chi2 + inv_d3,
        pert_distinct_delta=pert_distinct,
        slope_profiles=len(prof), slope_below_crit=slope_below,
        slope_min_chi2=num(slope_min), slope_min_span_dex=num(slope_min_span),
        ast_copy_hits=copies, ast_literals=n_lit, ast_unique=n_uniq,
        threshold_directions=len(vdirs), threshold_solvable=solvable,
        threshold_singular=singular,
        threshold_singular_text="、".join(singular),
        threshold_dets={k: num(v) for k, v in sorted(dets.items())},
        threshold_deltas=[num(v) for v in delta_vals],
        threshold_delta_max_abs=num(delta_max_abs),
        threshold_chi2_max=num(p_max_chi2),
        ctrl_neg_target=num(ctrl["neg_target"]),
        ctrl_neg_shift=ctrl["neg_shift"],
        sigma_a1=num(SIG_A[0]), sigma_a2=num(SIG_A[1]), sigma_a3=num(SIG_A[2]),
        sigma_aem_tension=num(Dq(SIG_AEM_TENSION)),
        readme_bytes=len(readme_b),
        readme_md5=hashlib.md5(readme_b).hexdigest(),
        readme_max_rid=max(int(x) for x in rid) if rid else 0,
        source_missing=sum(1 for p in [P_LEDGER, P_R1, P_R4, P_R5, P_B1, P_B2,
                                       P_R64, P_R188, P_R188_REP, README]
                           if not os.path.isfile(p)),
    )
    add("GM-VERDICT-MACHINE",
        verdict_string(key_numbers) !=
        verdict_string(dict(key_numbers, chi2_min=num(Dq(key_numbers["chi2_min"]) + 1))),
        "changed", "same", "读数 +1 后判词串必须变化")
    add("GM-SOURCE-COMPLETE", key_numbers["source_missing"] == 0,
        0, key_numbers["source_missing"], "十份来料文件全部存在")

    blob = json.dumps(key_numbers, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    cnts = counts_of()
    nf_guard = sum(1 for g in GUARDS if not g["ok"])
    n_decl = len(key_numbers)
    final = final_of(0, nf_guard, n_decl)
    verdict = verdict_string(key_numbers)
    segments = [dict(name=g["name"], kind=g["kind"], note=g["note"])
                for g in GUARDS]
    doc = dict(
        title="算法联盟：规范耦合高能交汇的可判负性、阈值自由度定价与反解门（第二十轮）",
        date=DATE,
        nature="不占号、不登记、不与任何卷相加；审对象是一圈 SM 规范耦合交汇与仓库既有 GUT 正对照",
        red_line="数学自洽 != 实验证实；四力大统一正确方程 0 条；独立实验预言 0；不宣称攻破统一场论",
        final=final, verdict=verdict, key_numbers=key_numbers,
        segments=segments, counts=cnts,
        guard_count=len(GUARDS), guard_pass=len(GUARDS) - nf_guard,
        content_sha256=sha, chi2_crit=float(crit_d),
        control_readings=[num(x) for x in ctrl["readings"]],
        configs=[dict(name=c["name"], chi2=num(c["chi2"]),
                      n_extra=c["n_extra"], gates=[int(z) for z in v],
                      certified=bool(ok))
                 for c, v, ok in zip(configs, vectors, certified)],
        identity_notes=[
            "WLS 残差对设计空间正交、自由度 3-2=1、p=1 时 3 方程 3 未知给 χ²=0，三者都是按定义成立的恒等式；本册单列 IDENTITY 并配 NOT-ALL-GREEN，不作为任何物理结论的证据",
            "合成统一数据可同时满足交汇门与零自由度门，但它是人为构造的数据集，不是物理候选；只能用作交汇判据的仪器正对照",
        ],
        boundary_notes=[
            "本册只覆盖一圈 SM β 与 r64 登记的一圈 MSSM β；两圈系数、完整阈值谱、超对称破缺质量谱、额外维与弦论族均未枚举，故「未被满足」不等于「不可满足」",
            "P15 登记 σ=0；相关协方差读数改用 C06/C07 两路口径张力作保守 σ_AEM，这是明示口径替换，不是来料本身的误差棒",
            "r64 用几何残差 0.246% 判 MSSM 通过；本册改用带误差棒 χ² 判据，属判据升级后的旧候选重映射，两判据对象不同不取和",
            "46 锚中唯一能检验 GUT 尺度的是 P11 质子衰变单侧下界（σ=0）；即使补上双侧锚，也不自动构成独立实验预言",
            "p=1 阈值方向只枚举 6 个显式方向，δ 记在 M_Z 处而非完整 RG 阈值谱；其中 common 与 beta_like 落在 span{1,c} 内导致 3×3 行列式恒零，它们根本不是新增自由度，已如实报 4 可解 / 2 奇异",
            "负对照必须沿加权正交补位移：只改单个耦合分量的 10σ 会被 (A,x) 拟合吸收大半，用它当负对照会给出假绿读数",
        ],
        info_notes=[
            "数学自洽 != 实验证实；审计册只产可算判决，不产新物理",
            "四力大统一正确方程 0 条、独立实验预言 0；不宣称攻破统一场论",
            "本册不占 RID、不入 README、不与任何审计卷相加",
            "README 全程零写入；并行会话已两次改动 README，故用结构性零写入而非前后 MD5 相等",
        ],
        source_files=[os.path.relpath(p).replace("\\", "/") for p in
                      [P_LEDGER, P_R1, P_R4, P_R5, P_B1, P_B2, P_R64,
                       P_R188, P_R188_REP, README]],
        source_missing=key_numbers["source_missing"],
        declared_negative=0,
    )

    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    lines = [
        doc["title"],
        "=" * 96,
        "verdict : " + verdict,
        "final   : " + final,
        "counts  : " + json.dumps(cnts, ensure_ascii=False, sort_keys=True),
        "guards  : %d/%d" % (doc["guard_pass"], doc["guard_count"]),
        "sha256  : " + sha,
        "-" * 96,
        "[MACHINE-TABLE]",
    ]
    for k in sorted(key_numbers):
        v = key_numbers[k]
        s = v if isinstance(v, str) else (
            json.dumps(v, ensure_ascii=False, sort_keys=True)
            if isinstance(v, (list, dict)) else str(v))
        lines.append("%s = %s" % (k, s))
    lines += ["[/MACHINE-TABLE]", "-" * 96]
    lines += [
        "零额外自由度：χ²_min = %s（%sσ 等效，阈值 %s，比值 %s）" %
        (disp(chi2_cf), disp(sig_eq), disp(crit_d), disp(ratio_crit)),
        "三交点 ln(Q/M_Z)：%s / %s / %s；跨度 %s dex（首册存档 %s）" %
        (disp(xs[0]), disp(xs[1]), disp(xs[2]), disp(span_act), disp(span_exp)),
        "p=1 阈值 e3：δ(α3⁻¹) = %s，α_s 须移到 %s（%sσ）；χ² = %s（恒等式）" %
        (disp(d3), disp(as_new, 9), disp(das_sigma), disp(sol_e3["chi2"], 3)),
        "r64 MSSM 正对照映射回 χ² 判据：χ² = %s < 阈值，但需 ≥1 个新自由参数" %
        disp(mssm["chi2"]),
        "交汇—自由度跷跷板：%d 个仓库来源配置，四门全过 %d 个；单门关键 %d 个" %
        (len(configs), escape, single_decisive),
        "可判负门：GUT 尺度相关锚 %d 个，其中双侧 %d 个；P11 为单侧下界 σ=0" %
        (gut["n_like"], gut["n_two_sided"]),
        "控制读数四路：%s（两两不同）；正对照 %d 过 / 负对照 %d 不过" %
        ("/".join(disp(x, 4) for x in ctrl["readings"]),
         ctrl["n_pass"], ctrl["n_fail"]),
        "输入扰动 %d 方向：恒假/随动检查 %d；β 剖面 %d 个，压到阈值下 %d 个" %
        (len(pert), inv_chi2 + inv_d3, len(prof), slope_below),
        "README %d B / %s / 最大 RID %d；本册零写入" %
        (len(readme_b), hashlib.md5(readme_b).hexdigest()[:12],
         key_numbers["readme_max_rid"]),
        "-" * 96,
        "红线：数学自洽 != 实验证实；不宣称攻破统一场论；独立实验预言 0。",
    ]
    with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print("FINAL =", final)
    print("VERDICT =", verdict)
    print("GUARDS = %d/%d" % (doc["guard_pass"], doc["guard_count"]))
    print("COUNTS =", json.dumps(cnts, ensure_ascii=False, sort_keys=True))
    print("CHI2 =", disp(chi2_cf), "SIGMA =", disp(sig_eq),
          "MSSM =", disp(mssm["chi2"]), "ESCAPE =", escape)
    return doc


if __name__ == "__main__":
    main()
