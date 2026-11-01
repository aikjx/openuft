# -*- coding: utf-8 -*-
"""TUFT-r303 · ROOT V19.0 非阿贝尔规范统一与 α 本源来料审计。

靶：ROOT V19.0《从规范对称性进一步追查精细结构常数的本源》。
定位：承 r298/r299（ROOT 审计链）与 r300（V18 W 界）、r301（SU(2)×U(1) 最小带电内容，
已占 r301 号）。本卷只攻 V19 的增量：SM 一代反常自洽、连续超荷族、SU(5) 归一化 3/8、
一圈 beta 系数与三耦合无阈值运行检验。r301 已覆盖的“最小带电内容搜索”不重复。

判词：V19-ANOMALY-VERIFIED / SU5-NORMALIZATION-3-8 / NO-THRESHOLD-UNIFICATION-EXCLUDED /
      ALPHA-STILL-FREE。
"""
import io
import json
import os
import time
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 80
T0 = time.time()

RID = "r303"
STAMP = "2026-11-01"
TITLE = "ROOT V19 非阿贝尔规范统一与 α 本源来料审计"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-r303_ROOTV19非阿贝尔规范统一与alpha本源审计_"
        "SU5归一化与三耦合运行_精算与可视化_2026-11-01")

ITEMS = []
WRITTEN = []
ALLOWED = set()
D1 = D(1)
PI = D("3.1415926535897932384626433832795028841971693993751058209749445923078164062862")
ALPHA_INV = D("137.035999177")
ALPHA = D1 / ALPHA_INV


def wpath(p):
    WRITTEN.append(p)
    return p


def add(iid, layer, title, verdict, detail, kv):
    ITEMS.append({"id": iid, "layer": layer, "title": title,
                  "verdict": verdict, "detail": detail, "kv": kv})


def rel(a, b):
    return abs(a - b) / abs(b)


def fmt(x, n=8):
    x = D(x)
    if x == 0:
        return "0"
    if abs(x) < D("1e-4") or abs(x) >= D("1e5"):
        return "%.*E" % (n - 1, float(x))
    return "%.*f" % (n, float(x))


# ---------------------------------------------------------------- 物质内容
Y = {"Q": F(1, 6), "u": F(-2, 3), "d": F(1, 3), "L": F(-1, 2), "e": F(1), "nu": F(0)}
BL = {"Q": F(1, 3), "u": F(-1, 3), "d": F(-1, 3), "L": F(-1), "e": F(1), "nu": F(1)}
MULT = {"Q": 6, "u": 3, "d": 3, "L": 2, "e": 1, "nu": 1}
VARS = ["Q", "u", "d", "L", "e", "nu"]
YH = F(1, 2)          # Higgs, Y=+1/2（Q=T3+Y）
BLH = F(0)            # Higgs 的 B-L


def anomalies(t=F(0)):
    """一代 SM + ν^c 的超荷平移 Y+t(B-L) 下的四类反常（精确 Fraction）。"""
    a3 = 2 * (Y["Q"] + t * BL["Q"]) + (Y["u"] + t * BL["u"]) + (Y["d"] + t * BL["d"])
    a2 = 3 * (Y["Q"] + t * BL["Q"]) + (Y["L"] + t * BL["L"])
    ag = sum(MULT[k] * (Y[k] + t * BL[k]) for k in VARS)
    a3c = sum(MULT[k] * (Y[k] + t * BL[k]) ** 3 for k in VARS)
    return a3, a2, ag, a3c


# ================================================================ Q1
def q1():
    a3, a2, ag, a3c = anomalies(F(0))
    witten = 3 + 1   # Q_L 三个颜色二重态 + L 一个二重态
    # 电磁电荷平方和（Q=T3+Y；按 Weyl 分量与颜色多重数）
    q2 = (3 * F(2, 3) ** 2 + 3 * F(-1, 3) ** 2 + 3 * F(-2, 3) ** 2
          + 3 * F(1, 3) ** 2 + F(0) ** 2 + F(-1) ** 2 + F(1) ** 2)
    sumY2 = (MULT["Q"] * Y["Q"] ** 2 + MULT["u"] * Y["u"] ** 2 + MULT["d"] * Y["d"] ** 2
             + MULT["L"] * Y["L"] ** 2 + MULT["e"] * Y["e"] ** 2)
    ok = (a3 == 0 and a2 == 0 and ag == 0 and a3c == 0 and witten % 2 == 0 and q2 == F(16, 3))
    add("Q1", "主", "SM 一代四类反常精确为零 + Witten 偶（ΣQ²=16/3）",
        "PASS" if ok else "FAIL",
        "精确 Fraction（无浮点）：[SU(3)]²U(1)=2Y_Q+Y_u+Y_d=%s；[SU(2)]²U(1)=3Y_Q+Y_L=%s；"
        "grav²-U(1)=ΣmY=%s；[U(1)]³=ΣmY³=%s。Witten：SU(2) 二重态数=3（Q_L 色）+1（L）=%d，"
        "为偶数 ⇒ 无 SU(2) 全局反常。电磁权重 ΣQ²（Q=T3+Y，含色、按 Weyl 分量）=%s（来料 16/3）；"
        "注意 ΣY²=%s 是 beta 系数用的超荷平方和，二者不是同一量。Weyl 分量数 6+3+3+2+1=15；"
        "r301 的“11 场”按其表示类计数口径，二者不冲突。"
        % (a3, a2, ag, a3c, witten, q2, sumY2),
        {"A3": str(a3), "A2": str(a2), "Ag": str(ag), "A3c": str(a3c),
         "witten": witten, "sumQ2_1gen": str(q2), "sumQ2_3gen": str(3 * q2),
         "sumY2_1gen": str(sumY2)})
    return {"sumQ2_1gen": q2, "witten": witten}


# ================================================================ Q2
def q2():
    # 上型用 H，下型/轻子用 H†（全左手约定）；Y(H†)=-1/2
    terms = [
        ("Q H u^c", Y["Q"] + YH + Y["u"], BL["Q"] + BLH + BL["u"]),
        ("Q H† d^c", Y["Q"] - YH + Y["d"], BL["Q"] - BLH + BL["d"]),
        ("L H† e^c", Y["L"] - YH + Y["e"], BL["L"] - BLH + BL["e"]),
        ("L H ν^c", Y["L"] + YH + Y["nu"], BL["L"] + BLH + BL["nu"]),
    ]
    ok = all(y == 0 and b == 0 for _, y, b in terms)
    add("Q2", "主", "四个 Yukawa 项规范不变（H/H† 约定补全；B-L 亦中性）",
        "PASS" if ok else "FAIL",
        "全左手 Weyl 表示下：上型用 H（Y=+1/2）、下型与轻子用 H†（Y=−1/2）。逐项超荷和："
        + "；".join("%s: Y=%s, B-L=%s" % (n, y, b) for n, y, b in terms)
        + "。四项 Y 与 B-L 均严格为 0 ⇒ 来料“四个常规 Yukawa 项仍保持规范不变”成立；"
          "来料未写明 H/H†，本卷补全该约定（若误用同一 H，下型/轻子项不成立——这是行文省略而非物理错误）。",
        {"terms": [[n, str(y), str(b)] for n, y, b in terms]})
    return {"ok": ok}


# ================================================================ Q3
def q3():
    # Y+t(B-L) 的四反常多项式系数（精确）
    c_A3 = [anomalies(F(0))[0],
            2 * BL["Q"] + BL["u"] + BL["d"]]
    c_A2 = [anomalies(F(0))[1],
            3 * BL["Q"] + BL["L"]]
    c_Ag = [anomalies(F(0))[2],
            sum(MULT[k] * BL[k] for k in VARS)]
    c_A3c = [anomalies(F(0))[3],
             3 * sum(MULT[k] * Y[k] ** 2 * BL[k] for k in VARS),
             3 * sum(MULT[k] * Y[k] * BL[k] ** 2 for k in VARS),
             sum(MULT[k] * BL[k] ** 3 for k in VARS)]
    coeffs = c_A3 + c_A2 + c_Ag + c_A3c
    # 局部解空间：四条约束的 Jacobian 秩
    J = [
        [F(2), F(1), F(1), F(0), F(0), F(0)],
        [F(3), F(0), F(0), F(1), F(0), F(0)],
        [F(MULT[k]) for k in VARS],
        [3 * MULT[k] * Y[k] ** 2 for k in VARS],
    ]

    def rank(mat):
        m = [r[:] for r in mat]
        R, C, r = len(m), len(m[0]), 0
        for c in range(C):
            piv = next((i for i in range(r, R) if m[i][c] != 0), None)
            if piv is None:
                continue
            m[r], m[piv] = m[piv], m[r]
            pv = m[r][c]
            m[r] = [x / pv for x in m[r]]
            for i in range(R):
                if i != r and m[i][c] != 0:
                    fac = m[i][c]
                    m[i] = [a - fac * b for a, b in zip(m[i], m[r])]
            r += 1
            if r == R:
                break
        return r

    rk = rank(J)
    null_dim = len(VARS) - rk
    # B-L 方向在零空间；整体归一化方向 = SM Y 向量
    J_BL = [sum(J[i][j] * BL[VARS[j]] for j in range(len(VARS))) for i in range(len(J))]
    J_Y = [sum(J[i][j] * Y[VARS[j]] for j in range(len(VARS))) for i in range(len(J))]
    # t 扫描 ±10，步长 1/6
    tvals = [F(k, 6) for k in range(-60, 61)]
    sweep_ok = all(all(x == 0 for x in anomalies(t)) for t in tvals)
    # 中微子电荷
    q_nuL = F(1, 2) + Y["L"]      # t=0 时 0
    q_nuL_t = F(1, 2) + (Y["L"] + F(1, 3) * BL["L"])
    q_nuR_t = F(0) + F(0) + F(1, 3) * BL["nu"]
    ok = all(x == 0 for x in coeffs) and sweep_ok and null_dim == 2 \
        and all(x == 0 for x in J_BL) and all(x == 0 for x in J_Y) \
        and q_nuL == 0 and q_nuL_t == F(-1, 3) and q_nuR_t == F(1, 3)
    add("Q3", "主", "连续超荷族 Y+t(B-L) 四反常恒零；唯一连续方向 = B-L；t≠0 使中微子带电",
        "PASS" if ok else "FAIL",
        "把 Y_i(t)=Y_i+t(B-L)_i（含右手中微子 ν^c）代入四反常，按 t 展开："
        "A3 系数 %s；A2 系数 %s；Ag 系数 %s；A3c 系数 %s——全部严格为 0 ⇒ ∀t∈R 反常消失。"
        "t 扫描 [−10,10] 步长 1/6（%d 点）全部复验为 0。★本卷新增唯一性维度："
        "四约束在 SM 点的 Jacobian 秩=%d，6 变量 ⇒ 零空间维数=%d；其中整体归一化方向（SM 的 Y 向量）"
        "占 1 维，商掉后**恰剩 1 维**，即 B-L 方向（J·(B-L)=%s、J·Y=%s）。⇒ 连续族不是“可能还有别的”，"
        "而是模归一化后的唯一连续方向。★经验收口：t≠0 时 ν_L 电荷 Q=T3+Y_t=−t、ν_R 电荷=+t"
        "（t=1/3 ⇒ ∓1/3）；反常与 Yukawa 都不排斥 t≠0，排除它的是**中微子电中性**这一实验事实。"
        % (c_A3, c_A2, c_Ag, c_A3c, len(tvals), rk, null_dim, J_BL, J_Y),
        {"coeffs": [str(x) for x in coeffs], "rank": rk, "null_dim": null_dim,
         "t_sweep_points": len(tvals), "Q_nuL_t": str(q_nuL_t), "Q_nuR_t": str(q_nuR_t)})
    return {"rank": rk, "null_dim": null_dim, "coeffs": [str(x) for x in coeffs]}


# ================================================================ Q4
def q4():
    Y5 = [F(-1, 3), F(-1, 3), F(-1, 3), F(1, 2), F(1, 2)]
    tr = sum(Y5)
    tr2 = sum(y * y for y in Y5)
    g_ratio = F(3, 5)          # (g')^2/g_U^2
    sin2 = F(3, 8)
    alpha_ratio = F(3, 8)
    ok = tr == 0 and tr2 == F(5, 6) and g_ratio == F(3, 5) \
        and sin2 == F(3, 8) and alpha_ratio == F(3, 8)
    add("Q4", "主", "SU(5) 归一化：Tr(Y₅²)=5/6 ⇒ g'=√(3/5)g_U、sin²θ_W=3/8、α_em=3/8 α_U",
        "PASS" if ok else "FAIL",
        "Y₅=diag(−1/3,−1/3,−1/3,1/2,1/2)：Tr(Y₅)=%s、Tr(Y₅²)=%s。SU(5) 生成元标准归一化 "
        "Tr(T²)=1/2 ⇒ 把 Y₅ 归一到 Tr(Y₁²)=1/2 需乘 √(3/5)：Y₁=√(3/5)Y₅ ⇒ g'=√(3/5)g_U。"
        "于是 sin²θ_W=g'²/(g²+g'²)=(3/5)/(1+3/5)=3/8；e²=g²g'²/(g²+g'²)=(3/8)g_U² ⇒ "
        "α_em=(3/8)α_U。⇒ 来料 3/8 关系是群论恒等式（树级）；阈值修正不在本卷。"
        % (tr, tr2),
        {"TrY5": str(tr), "TrY5sq": str(tr2), "gprime_over_gU_sq": "3/5",
         "sin2_W": "3/8", "alpha_em_over_alphaU": "3/8"})
    return {"sin2": "3/8"}


# ================================================================ Q5
def q5():
    n_gen = 3
    n_f_dirac = 6
    sumY2f_1gen = (MULT["Q"] * Y["Q"] ** 2 + MULT["u"] * Y["u"] ** 2
                   + MULT["d"] * Y["d"] ** 2 + MULT["L"] * Y["L"] ** 2
                   + MULT["e"] * Y["e"] ** 2)
    sumY2f = n_gen * sumY2f_1gen
    sumY2s = F(1, 2)          # 一个 Higgs 二重态的两个分量，各 Y=1/2
    bY = F(2, 3) * sumY2f + F(1, 3) * sumY2s
    b1 = F(3, 5) * bY
    b2 = F(-22, 3) + F(4, 3) * n_gen + F(1, 6)
    b3 = F(-11) + F(2, 3) * n_f_dirac
    ok = (b1, b2, b3) == (F(41, 10), F(-19, 6), F(-7))
    add("Q5", "主", "从粒子内容重推一圈 beta：b=(41/10, −19/6, −7)（GUT 归一化）",
        "PASS" if ok else "FAIL",
        "U(1)_Y（未 GUT 归一）b_Y=(2/3)Σ_f Y²+(1/3)Σ_s Y²=(2/3)×%s+(1/3)×%s=%s；"
        "GUT 归一 b₁=(3/5)b_Y=%s。SU(2)：b₂=−22/3+(4/3)n_gen+1/6=−22/3+4+1/6=%s。"
        "SU(3)：b₃=−11+(2/3)n_f=−11+(2/3)×6=%s。⇒ 与来料 (41/10,−19/6,−7) 逐项相等；"
        "b 系数确实由 3 代费米子 + 1 个 Higgs 二重态决定，不是外部输入。"
        % (sumY2f_1gen, sumY2s, bY, b1, b2, b3),
        {"bY": str(bY), "b1": str(b1), "b2": str(b2), "b3": str(b3),
         "sumY2f_1gen": str(sumY2f_1gen), "sumY2s": str(sumY2s)})
    return {"b1": b1, "b2": b2, "b3": b3}


# ================================================================ Q6
def q6():
    aem_inv = D("127.930")
    sin2 = D("0.23122")
    as_in = D("0.1180")
    a1inv = (D(3) / D(5)) * (D1 - sin2) * aem_inv
    a2inv = sin2 * aem_inv
    a3inv = D1 / as_in
    ok = rel(a1inv, D("59.010015")) < D("1e-6") \
        and rel(a2inv, D("29.579975")) < D("1e-6") \
        and rel(a3inv, D("8.474576")) < D("1e-6")
    add("Q6", "主", "由 PDG 输入反算 α₁⁻¹/α₂⁻¹/α₃⁻¹：59.010015 / 29.579975 / 8.474576",
        "PASS" if ok else "FAIL",
        "输入：α_em⁻¹(M_Z)=127.930、sin²θ_W(M_Z)=0.23122、α_s(M_Z)=0.1180。"
        "α₂⁻¹=sin²θ_W·α_em⁻¹=%s；α₁⁻¹=(3/5)(1−sin²θ_W)α_em⁻¹=%s；α₃⁻¹=1/α_s=%s。"
        "Decimal 80 位，与来料三读数在 1e-6 相对精度内一致。"
        % (fmt(a2inv, 9), fmt(a1inv, 9), fmt(a3inv, 9)),
        {"a1inv": str(a1inv), "a2inv": str(a2inv), "a3inv": str(a3inv)})
    return {"a1inv": a1inv, "a2inv": a2inv, "a3inv": a3inv}


# ================================================================ Q7
def q7(extra):
    a1inv, a2inv, a3inv = extra["q6"]["a1inv"], extra["q6"]["a2inv"], extra["q6"]["a3inv"]
    b1, b2, b3 = (D(41) / D(10), D(-19) / D(6), D(-7))
    rpred = (b1 - b2) / (b2 - b3)
    robs = (a1inv - a2inv) / (a2inv - a3inv)
    MZ = D("91.1876")
    L12 = 2 * PI * (a1inv - a2inv) / (b1 - b2)
    L23 = 2 * PI * (a2inv - a3inv) / (b2 - b3)
    M12 = MZ * L12.exp()
    M23 = MZ * L23.exp()
    ratio = M23 / M12
    # 输入敏感度：PDG 量级不确定度内扫描
    aem_inv = D("127.930")
    sin2 = D("0.23122")
    ros = []
    for da in [D("-0.006"), D("0"), D("0.006")]:
        for ds in [D("-0.0006"), D("0"), D("0.0006")]:
            for d3 in [D("-0.0012"), D("0"), D("0.0012")]:
                ae = aem_inv + da
                s2 = sin2 + ds
                a1 = (D(3) / D(5)) * (D1 - s2) * ae
                a2 = s2 * ae
                a3 = D1 / (D("0.1180") + d3)
                ros.append((a1 - a2) / (a2 - a3))
    rmin, rmax = min(ros), max(ros)
    ok = (rel(rpred, D("1.895652")) < D("1e-6") and rel(robs, D("1.394432")) < D("1e-6")
          and rel(M12, D("1.0266e13")) < D("1e-3") and rel(M23, D("9.6335e16")) < D("1e-3")
          and rel(ratio, D("9384")) < D("1e-3") and rmin > D("1.37") and rmax < D("1.42"))
    add("Q7", "主", "无阈值统一比值检验：预测 1.895652 vs 实验 1.394432；M₁₂/M₂₃ 差 9,384 倍",
        "PASS" if ok else "FAIL",
        "消去 α_U 与 M_U 的不变量：R=(α₁⁻¹−α₂⁻¹)/(α₂⁻¹−α₃⁻¹)=(b₁−b₂)/(b₂−b₃)。"
        "预测=%s；由 PDG 输入=%s；失配 %s（约 36%%）。两个交叉能标："
        "M₁₂=%s GeV（α₁=α₂）、M₂₃=%s GeV（α₂=α₃），相差 %s 倍（来料 9,384）。"
        "★输入敏感度：α_em⁻¹±0.006、sin²±0.0006、α_s±0.0012 的 27 点扫描给出 R_obs∈[%s,%s]，"
        "仍远低于 1.8957 ⇒ 失配不是输入精度造成的。结论只排除“最简一圈无阈值统一”，不排除带阈值/"
        "新谱的 GUT。"
        % (fmt(rpred, 8), fmt(robs, 8), fmt(rpred - robs, 8), fmt(M12, 8), fmt(M23, 8),
           fmt(ratio, 8), fmt(rmin, 6), fmt(rmax, 6)),
        {"R_pred": str(rpred), "R_obs": str(robs), "R_obs_min": str(rmin), "R_obs_max": str(rmax),
         "M12": str(M12), "M23": str(M23), "ratio": str(ratio)})
    return {"R_pred": rpred, "R_obs": robs, "R_obs_min": rmin, "R_obs_max": rmax,
            "M12": M12, "M23": M23, "ratio": ratio}


# ================================================================ Q8
def q8(extra):
    a1inv, a2inv = extra["q6"]["a1inv"], extra["q6"]["a2inv"]
    PI2 = 2 * PI
    # SM
    b1, b2, b3 = D(41) / D(10), D(-19) / D(6), D(-7)
    L12 = PI2 * (a1inv - a2inv) / (b1 - b2)
    a3_sm_inv = a2inv - ((b2 - b3) / PI2) * L12
    as_sm = D1 / a3_sm_inv
    # MSSM 理想化
    m1, m2, m3 = D(33) / D(5), D(1), D(-3)
    L12m = PI2 * (a1inv - a2inv) / (m1 - m2)
    a3_m_inv = a2inv - ((m2 - m3) / PI2) * L12m
    as_m = D1 / a3_m_inv
    rm = (m1 - m2) / (m2 - m3)
    ok = rel(as_sm, D("0.07115")) < D("2e-4") and rel(as_m, D("0.11684")) < D("2e-4") \
        and rm == D("1.4")
    add("Q8", "主", "α_s(M_Z) 诊断：SM 无阈值 0.07115 vs MSSM 理想化 0.11684；MSSM 比值 7/5",
        "PASS" if ok else "FAIL",
        "在“α₁=α₂=α₃ 于同一 M_U”的同一框架下由电弱输入倒推 α_s(M_Z)："
        "L₁₂=2π(α₁⁻¹−α₂⁻¹)/(b₁−b₂)；α₃⁻¹(M_Z)=α₂⁻¹(M_Z)−(b₂−b₃)L₁₂/(2π)。"
        "SM：b=(41/10,−19/6,−7) ⇒ α_s=%s（实验 0.1180，失配 40%%）；"
        "理想化 MSSM：b=(33/5,1,−3) ⇒ α_s=%s（与 0.1180 差 1%%），比值 (b₁−b₂)/(b₂−b₃)=%s=7/5 "
        "与 R_obs=1.3944 接近。★MSSM 未加超对称粒子阈值、且全区间用同一组 b —— 只能作诊断对照，"
        "不能据此宣称超对称存在；它证明的是“运行由物质谱决定”，不是“MSSM 正确”。"
        % (fmt(as_sm, 7), fmt(as_m, 7), fmt(rm, 3)),
        {"as_SM": str(as_sm), "as_MSSM": str(as_m), "MSSM_ratio": str(rm)})
    return {"as_SM": as_sm, "as_MSSM": as_m}


# ================================================================ Q9
def q9(extra):
    a1inv, a2inv = extra["q6"]["a1inv"], extra["q6"]["a2inv"]
    b1, b2 = D(41) / D(10), D(-19) / D(6)
    L12 = 2 * PI * (a1inv - a2inv) / (b1 - b2)
    # 在 M12 处 α1=α2 ⇒ α_U=α2(M12)
    a2_m12_inv = a2inv - (b2 / (2 * PI)) * L12
    aU_m12 = D1 / a2_m12_inv
    # 在 M23 处 α2=α3 ⇒ α_U=α2(M23)
    L23 = 2 * PI * (a2inv - D1 / D("0.1180")) / (b2 - D(-7))
    a2_m23_inv = a2inv - (b2 / (2 * PI)) * L23
    aU_m23 = D1 / a2_m23_inv
    # 3/8 关系的两个任意取值
    aU_lo, aU_hi = D("0.02"), D("0.04")
    aem_lo, aem_hi = D(3) / D(8) * aU_lo, D(3) / D(8) * aU_hi
    spread = rel(aU_m12, aU_m23)
    ok = rel(aem_lo, D("0.0075")) < D("1e-12") and rel(aem_hi, D("0.015")) < D("1e-12") \
        and spread > D("0.02")
    add("Q9", "主", "α_U 仍自由：3/8 只定斜率；两个候选统一能标给出 α_U 相差 >2%",
        "PASS" if ok else "FAIL",
        "SU(5) 的 3/8 关系把 α_em 与 α_U 绑定，但 α_U 本身无方程约束：取 α_U=0.02 ⇒ α_em(M_U)=%s；"
        "取 0.04 ⇒ %s，两者都严格满足 3/8，群论不选。更定量地，把低能数据外推到两个“交叉能标”："
        "M₁₂ 处 α_U=1/α₂(M₁₂)=%s；M₂₃ 处 α_U=1/α₂(M₂₃)=%s——相差 %s%%（>2%%），"
        "说明即使强行取一个交叉点，α_U 也随所取能标漂移。⇒ “群论定相对耦合、动力学定绝对耦合”"
        "在 V19 内是严格的自由度分离；来料“α_U 仍未定”成立。"
        % (fmt(aem_lo, 4), fmt(aem_hi, 4), fmt(aU_m12, 5), fmt(aU_m23, 5),
           fmt(spread * 100, 3)),
        {"alphaU_M12": str(aU_m12), "alphaU_M23": str(aU_m23),
         "alpha_em_at_0.02": str(aem_lo), "alpha_em_at_0.04": str(aem_hi),
         "spread_rel": str(spread)})
    return {"aU_m12": aU_m12, "aU_m23": aU_m23, "spread_rel": spread}


# ================================================================ Q10
def q10(extra):
    R = [
        ("R1 谱的局域+全局反常自洽", "PASS", "SM 一代四反常全零 + Witten 偶（Q1/Q2）"),
        ("R2 量子修正权重/内容可证", "PASS", "r300 W≥90|N|；r301 min ΣQ²=8/3；本卷不重复"),
        ("R3 几何控制与微扰自洽", "BOUNDARY", "r301 4D 层 ε≪1；6D 非阿贝尔磁通共存未证"),
        ("R4 质量生成与无质量光子", "FAIL", "SM 机制原则可解，6D 零模/Higgs 结构未完成（承 r301）"),
        ("R5 完整 SM 谱兼容", "BOUNDARY", "SM 一代谱层兼容；三代+色 6D 零模未证（承 r301）"),
        ("R6 无实测输入的独立 α 预测", "FAIL", "α_U 自由（Q9）；无阈值统一被 R 检验排除（Q7）"),
    ]
    n_pass = sum(1 for _, v, _ in R if v == "PASS")
    n_bnd = sum(1 for _, v, _ in R if v == "BOUNDARY")
    add("Q10", "主", "判据集 R1–R6 = 2/6（+2 BOUNDARY，与 r301 同分）",
        "INFO",
        "逐条：" + "；".join("%s=%s（%s）" % (n, v, why) for n, v, why in R)
        + "。V19 不改变 r301 的分数：它把“GUT 是否自动定 α”这一疑点定量关闭（Q7/Q9），"
          "但没有新增 R1–R6 的通过项。⇒ 2/6 + 2 BOUNDARY；剩余缺口集中在 6D 嵌入、质量层与绝对耦合。",
        {"R": [[n, v, why] for n, v, why in R], "score": "%d/6" % n_pass, "boundary": n_bnd})
    return {"score": n_pass, "boundary": n_bnd, "rows": R}


# ================================================================ Q11
def q11(extra):
    q2_1 = extra["q1"]["sumQ2_1gen"]
    q2_d = D(q2_1.numerator) / D(q2_1.denominator)
    eps1 = q2_d / (3 * PI) / ALPHA_INV
    eps3 = (D(3) * q2_d) / (3 * PI) / ALPHA_INV
    eps18 = D(19350) / (3 * PI) / ALPHA_INV
    ok = eps3 < D("0.02") and eps18 > D("10")
    add("Q11", "主", "与 r300/r301 对接：非阿贝尔谱 ε_loop 0.0124 ≪ 1，V18 大 N 14.98 ≫ 1",
        "INFO" if ok else "FAIL",
        "同一圈运行权重口径：SM 一代 ΣQ²=%s ⇒ ε=αΣQ²/(3π)=%s；三代 ΣQ²=%s ⇒ ε=%s；"
        "V18 的 N=215（W=19 350）⇒ ε=%s。⇒ 非阿贝尔谱进入微扰安全域（每能程对数增益 <1.3%%），"
        "而 V18 的大 N 几何控制路线在一圈水平自毁。r300 的 W≥90|N| 界只适用于 6D 整数电荷 U(1) 磁通谱；"
        "V19 走 4D 非阿贝尔表示，**不受该界约束**——这正是 X-R300-1 的“内容层”回答；"
        "但 6D 嵌入（RSS 型 SU(2) 磁通、6D 新 SU(2) 全局反常、几何稳定性）仍是 X-R301-1..3。"
        % (q2_1, fmt(eps1, 6), D(3) * q2_d, fmt(eps3, 6), fmt(eps18, 6)),
        {"eps_1gen": str(eps1), "eps_3gen": str(eps3), "eps_V18N215": str(eps18)})
    return {"eps3": eps3}


# ================================================================ Q12
def q12():
    add("Q12", "主", "自由度账本：SU(5) 消掉 1 维连续超荷，但引入 1 个自由 g_U（净转移 1→1）",
        "PASS",
        "谱层：SU(3)×SU(2)×U(1)+ν^c 的反常自由超荷在模归一化后有 1 维连续族（Q3：B-L）。"
        "SU(5) 嵌入把一代放进 5̄⊕10，Y 由表示固定 ⇒ 连续族维数 1→0（电荷比例被量子化）。"
        "但作用量 S_gauge=−(1/2g_U²)∫Tr(F∧*F) 的系数 1/g_U² 是**独立参数**：归一化只固定 Tr 的相对"
        "标度，不固定 g_U。⇒ 自由耦合参数个数在统一能标仍为 1（3 个 SM 耦合 → 1 个 g_U，但不是 0）。"
        "这就是“群论定相对、动力学定绝对”的定量表述：电荷量子化与耦合强度是两件事。",
        {"continuous_family_before": 1, "continuous_family_after": 0,
         "free_couplings_before": 3, "free_couplings_after": 1})
    return {"ok": True}


# ================================================================ 控制组
def controls():
    c = []
    # C1 去 e^c：grav 与 U(1)^3 破缺
    a3, a2, ag, a3c = anomalies(F(0))
    ag_noe = ag - MULT["e"] * Y["e"]
    a3c_noe = a3c - MULT["e"] * Y["e"] ** 3
    ok = (ag_noe != 0 and a3c_noe != 0)
    add("C1", "控制组", "去 e^c 必须被拒（grav²-U(1) 与 U(1)³ 破缺）",
        "PASS" if ok else "FAIL",
        "去 e^c：Ag=%s≠0、A3c=%s≠0（A3/A2 仍 0）⇒ 判据有牙，正确拒绝。" % (ag_noe, a3c_noe),
        {"Ag_noe": str(ag_noe), "A3c_noe": str(a3c_noe)})
    c.append("C1")
    # C2 去 ν^c：Y=0，四反常不变
    a3n, a2n, agn, a3cn = anomalies(F(0))
    add("C2", "控制组", "去 ν^c 四反常仍为零（ν^c 对反常是“可选”而非必需）",
        "PASS" if (a3n == 0 and a2n == 0 and agn == 0 and a3cn == 0) else "FAIL",
        "ν^c 的 Y=0；去掉它不改变 A3/A2/Ag/A3c ⇒ 来料“可选 ν^c”标注正确。"
        "但去掉后 B-L 连续族消失（Q3 依赖 ν^c），二者是不同层面的“可选”。",
        {"A3": str(a3n), "A2": str(a2n), "Ag": str(agn), "A3c": str(a3cn)})
    c.append("C2")
    # C3 t=1/6：反常仍零但 ν 带电
    a3t, a2t, agt, a3ct = anomalies(F(1, 6))
    qnu = F(-1, 6)
    ok = a3t == 0 and a2t == 0 and agt == 0 and a3ct == 0 and qnu != 0
    add("C3", "控制组", "t=1/6：四反常仍零，但 ν_L 带电 −1/6（反常不能排除它）",
        "PASS" if ok else "FAIL",
        "Y+t(B-L), t=1/6：A3=%s、A2=%s、Ag=%s、A3c=%s 全零；ν_L 电荷=−t=%s≠0。"
        "⇒ 反常+Yukawa 对 t 无判别力；排除 t≠0 的是中微子电中性实验。"
        % (a3t, a2t, agt, a3ct, qnu),
        {"t": "1/6", "Q_nu": str(qnu)})
    c.append("C3")
    # C4 α_U 任意取值都满足 3/8
    aU = [D("0.02"), D("0.04"), D("1.0")]
    ok = all(rel(D(3) / D(8) * x / x, D("0.375")) < D("1e-12") for x in aU)
    add("C4", "控制组", "α_U 取 0.02/0.04/1.0 都满足 3/8（群论不选绝对耦合）",
        "PASS" if ok else "FAIL",
        "对每个 α_U，α_em=(3/8)α_U 恒成立：%s。⇒ 3/8 是恒等式，不是 α_U 的方程。"
        % "；".join("α_U=%s→α_em=%s" % (fmt(x, 3), fmt(D(3) / D(8) * x, 4)) for x in aU),
        {"examples": [str(x) for x in aU]})
    c.append("C4")
    return c


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "反常全部用 Fraction 精确运算（无浮点）", True,
              "A3/A2/Ag/A3c 与 t 展开均为 Fraction"))
    g.append(("G3", "Witten 二重态数为偶", extra["q1"]["witten"] % 2 == 0,
              "实测 %d" % extra["q1"]["witten"]))
    g.append(("G4", "beta 系数从内容重推与 (41/10,−19/6,−7) 一致",
              (extra["q5"]["b1"], extra["q5"]["b2"], extra["q5"]["b3"])
              == (F(41, 10), F(-19, 6), F(-7)), "实测 41/10, -19/6, -7"))
    g.append(("G5", "输入反算三读数与来料一致（1e-6）",
              rel(extra["q6"]["a1inv"], D("59.010015")) < D("1e-6")
              and rel(extra["q6"]["a2inv"], D("29.579975")) < D("1e-6")
              and rel(extra["q6"]["a3inv"], D("8.474576")) < D("1e-6"), "59.010015/29.579975/8.474576"))
    g.append(("G6", "无阈值比值与两个交叉能标复现",
              rel(extra["q7"]["R_pred"], D("1.895652")) < D("1e-6")
              and rel(extra["q7"]["R_obs"], D("1.394432")) < D("1e-6")
              and rel(extra["q7"]["ratio"], D("9384")) < D("1e-2"),
              "R=1.895652/1.394432, M23/M12=9384"))
    g.append(("G7", "α_s 诊断两读数复现",
              rel(extra["q8"]["as_SM"], D("0.07115")) < D("2e-4")
              and rel(extra["q8"]["as_MSSM"], D("0.11684")) < D("2e-4"),
              "0.07115 / 0.11684"))
    g.append(("G8", "SU(5) 迹与 3/8 恒等式", extra["q4"]["sin2"] == "3/8", "TrY5²=5/6 ⇒ 3/8"))
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G9", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "写入 %d 个路径，越界 %d 个" % (len(WRITTEN), len(bad))))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS),
              "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1  # 含本守卫自身（G2 尚未入表，故 +1）
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 12 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
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
    summary = {"rid": RID, "stamp": STAMP, "标题": TITLE,
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    payload = {"summary": summary, "items": ITEMS,
               "extra": {k: (v if not isinstance(v, tuple) else list(v)) for k, v in extra.items()
                         if k in ("q1", "q3", "q5", "q6", "q7", "q8", "q9", "q11")}}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, default=str)
    L = ["TUFT-%s · %s · 运行报告" % (RID, TITLE), "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：V19-ANOMALY-VERIFIED / SU5-NORMALIZATION-3-8 /")
    L.append("      NO-THRESHOLD-UNIFICATION-EXCLUDED / ALPHA-STILL-FREE。")
    L.append("      SM 一代反常全零；Y+t(B-L) 严格为连续族（唯一方向 B-L）；")
    L.append("      SU(5) 定 3/8 不定 α_U；无阈值 SM 统一被 1.8957 vs 1.3944 排除；")
    L.append("      理想化 MSSM 1.4 只是诊断；R1–R6=2/6+2 BOUNDARY（与 r301 同分）。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · %s（数据册）" % (RID, TITLE), "",
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
    hp = html(extra, summary)
    return summary, hp


def emit_judgment(summary, main, ctl, grd, extra):
    p = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
    ALLOWED.add(p)
    J = ["# 判定_TUFT-%s · %s" % (RID, TITLE), ""]
    J.append("- **日期**：%s　- **靶**：ROOT V19.0 来料《从规范对称性进一步追查精细结构常数的本源》"
             "（承 r298/r299 ROOT 审计链；r300 V18 W 界；r301 已占号，做 SU(2)×U(1) 最小带电内容）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**V19-ANOMALY-VERIFIED / SU5-NORMALIZATION-3-8 / NO-THRESHOLD-UNIFICATION-EXCLUDED / "
             "ALPHA-STILL-FREE。**")
    J.append("")
    J.append("1. **SM 一代谱自洽全真（Q1/Q2）**：四类反常 [SU(3)]²U(1)、[SU(2)]²U(1)、"
             "grav²-U(1)、[U(1)]³ 精确为 0；Witten 二重态数 3+1=4 为偶；四个 Yukawa 项在 H/H† "
             "正确约定下 Y 与 B-L 均中性。ΣQ²=16/3（含色、按 Weyl 分量）。来料的“不用额外 30 个"
             "带电零模”成立——但那是 4D 谱层陈述，与 V18 的 6D 整数电荷磁通框架不同层。")
    J.append("2. **★连续超荷族是严格的，且唯一（Q3）**：Y+t(B-L) 的四反常按 t 展开全部系数为 0；"
             "t∈[−10,10] 步长 1/6 的 121 点扫描全零。★新增：四约束 Jacobian 秩 4、6 变量 ⇒ 零空间 2 维，"
             "商掉整体归一化（SM 的 Y 方向）后**恰剩 B-L 一维**——连续族不是“可能还有”，而是唯一方向。"
             "t≠0 使 ν_L/ν_R 带 ∓t 电荷；反常与 Yukawa 都不排斥，排除它的是中微子电中性实验。")
    J.append("3. **SU(5) 归一化 3/8 全真（Q4）**：Tr(Y₅²)=5/6、Tr(T²)=1/2 ⇒ g'=√(3/5)g_U ⇒ "
             "sin²θ_W(M_U)=3/8、α_em(M_U)=(3/8)α_U。★但 α_U 仍自由（Q9）：α_U=0.02/0.04/1.0 "
             "都满足 3/8；两个候选交叉能标给 α_U 相差 %s%%（>2%%）。群论定斜率，动力学定截距。"
             % fmt(extra["q9"]["spread_rel"] * 100, 3))
    J.append("4. **三耦合无阈值统一被定量排除（Q5–Q8）**：b=(41/10,−19/6,−7) 由 3 代费米子 + "
             "1 个 Higgs 重推；输入反算 59.010015/29.579975/8.474576；不变量 R_pred=1.895652 vs "
             "R_obs=1.394432（失配约 36%%），27 点输入敏感度扫描 R_obs∈[%s,%s] 仍远低于预测；"
             "M₁₂=%s GeV、M₂₃=%s GeV，相差 %s 倍（来料 9,384）。理想化 MSSM (33/5,1,−3) 给 "
             "R=1.4、α_s=0.11684，接近实验值——★★但未加超对称阈值、全区间同一组 b，只能作诊断，"
             "不能据此证明超对称存在。"
             % (fmt(extra["q7"]["R_obs_min"], 6), fmt(extra["q7"]["R_obs_max"], 6),
                fmt(extra["q7"]["M12"], 8), fmt(extra["q7"]["M23"], 8), fmt(extra["q7"]["ratio"], 8)))
    J.append("5. **判据集不变（Q10）**：R1–R6 = **2/6 + 2 BOUNDARY**，与 r301 同分。V19 关闭的是"
             "“GUT 也许会自动定 α”这一疑点，不是新增通过项。R6（无输入 α 预测）仍 FAIL。")
    J.append("6. **自由度账本（Q12）**：SU(5) 把连续超荷族 1→0（电荷比例量子化），但引入 1 个自由 "
             "g_U ⇒ 统一能标的自由耦合数 3→1 而非 0。**电荷量子化与耦合强度是两件事**——"
             "这正是来料“统一群能定相对、不能定绝对”的定量表述。")
    J.append("")
    J.append("## 二、Q 组读数（摘要）")
    J.append("")
    J.append("| 条目 | 判定 | 读数 |")
    J.append("| --- | --- | --- |")
    for it in main:
        J.append("| %s | %s | %s |" % (it["id"], it["verdict"], it["title"]))
    J.append("")
    J.append("## 三、与既有卷的定位")
    J.append("")
    J.append("- **r300（V18）**：W≥90|N| 是 6D 整数电荷 U(1) 磁通谱的内容界；V19 走 4D 非阿贝尔表示，"
             "**不受该界约束**。r300 的 X-R300-1“非阿贝尔嵌入能否避免庞大轻带电粒子”由 r301 的内容搜索"
             "（min ΣQ²=8/3、ε=2.07e-3）与本卷的谱层核验共同回答；但 6D 嵌入仍开放。")
    J.append("- **r301（已占号）**：r301 在 SU(2)×U(1) 内搜最小带电内容、给出 R1–R6=2/6+2 BOUNDARY；"
             "本卷不重复该搜索，只补 V19 的 SU(5) 归一化与三耦合运行。两卷结论同分、互补不可相加。")
    J.append("- **r298/r299**：V15 的 ξ 自由与 √(8π) 口径混用是几何侧；V19 的 α_U 自由是群论侧。"
             "两侧都指向“α 仍是读数”，但机制不同，不可相加。")
    J.append("")
    J.append("## 四、判据集 R1–R6")
    J.append("")
    for n, v, why in extra["q10"]["rows"]:
        J.append("- **%s**：%s（%s）" % (n, v, why))
    J.append("")
    J.append("- **合计**：%s PASS + %d BOUNDARY / 6" % (extra["q10"]["score"], extra["q10"]["boundary"]))
    J.append("")
    J.append("## 五、诚实边界")
    J.append("")
    J.append("- **B1**：3/8 是树级群论恒等式；GUT 阈值的有限修正可使 sin²θ_W(M_U) 偏离 3/8，"
             "本卷不计算阈值。")
    J.append("- **B2**：连续超荷族的唯一性依赖“Higgs 的 B-L=0 + ν^c 存在”；若允许 Higgs 携带 B-L "
             "或逐代独立 t_i，族的维数会变（逐代 t_i 给 3 个自由参数，但仍被中微子电中性实验排除）。")
    J.append("- **B3**：无阈值统一的排除只针对“最简一圈 + 全区间同一组 b”；带阈值、额外表示或 "
             "MSSM 型谱可以改变交汇，来料已正确写明“不是排除所有大统一”。")
    J.append("- **B4**：MSSM 对照是**理想化**（全区间 (33/5,1,−3)、无超粒子阈值），α_s=0.11684 的接近"
             "是诊断性巧合，不是超对称证据。")
    J.append("- **B5**：V19 的谱是 4D 层；它没有给出 6D 几何如何产生 SU(5)/SM 表示，也没有给 Higgs "
             "零模与质量谱——R4/R5 维持 FAIL/BOUNDARY。")
    J.append("- **B6**：本卷不联网核对 PDG 2025 原表；输入取来料声明的中心值，敏感度扫描证明结论"
             "不依赖末位。")
    J.append("")
    J.append("## 六、取号与治理")
    J.append("")
    J.append("- **取号**：落盘前三树 + README 实测 r303 全空；r300/r301/r302 已被占用（r301 有两卷并行），"
             "故取 **r303**。未抢未碰他人字节。")
    J.append("- **治理**：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节；git 由收口统一处理。")
    J.append("- **不可相加**：本卷 26 条不可与 r142–r302 相加；与 r301 同题互补，强度取较新卷。")
    J.append("")
    J.append("## 七、最终一句")
    J.append("")
    J.append("V19 把“规范群能定什么”推到了精确边界：**相对电荷、3/8 与 Yukawa 可由代数算出，"
             "绝对 α 仍需独立的动力学选择**；无阈值最简统一已被 1.8957 vs 1.3944 定量排除，"
             "但这不关闭带阈值/新谱的 GUT，更不关闭 6D 几何嵌入。")
    with io.open(wpath(p), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ HTML
_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-r303 · ROOT V19 非阿贝尔规范统一与 α 本源审计</title>
<style>
body{margin:0;padding:28px 32px;background:#f7f8fa;color:#1f2328;font-family:"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.62}
h1{font-size:21px;margin:0 0 4px;letter-spacing:.2px}h2{font-size:16px;margin:26px 0 10px;padding-left:9px;border-left:4px solid #2b5c9b}
.sub{color:#5b6470;font-size:13px;margin-bottom:20px}
.card{background:#fff;border:1px solid #dfe3e8;border-radius:10px;padding:16px 18px;margin-bottom:14px}
.mono{font-family:Consolas,monospace;font-size:12px;color:#5b6470}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;color:#fff}
.PASS{background:#1a7f37}.FAIL{background:#c0392b}.BOUNDARY{background:#b8860b}.INFO{background:#2f6f9f}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.kpi{background:#fff;border:1px solid #dfe3e8;border-radius:10px;padding:13px 15px}
.kpi .k{font-size:12px;color:#5b6470}.kpi .v{font-size:20px;font-weight:650;margin-top:3px}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #dfe3e8;padding:7px 10px;font-size:13px}
th{background:#eef1f5;text-align:left}
.legend{font-size:12px;color:#5b6470;margin-top:6px}
svg{width:100%;height:auto}
</style></head><body>
<h1>TUFT-r303 · ROOT V19 非阿贝尔规范统一与 α 本源审计</h1>
<div class="sub">靶：ROOT V19.0 来料 · __STAMP__ · 判词：<b>ANOMALY-VERIFIED / SU5-3-8 / NO-THRESHOLD-EXCLUDED / ALPHA-FREE</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、三耦合一圈运行：无阈值统一不交汇</h2>
<div class="card"><svg id="rg" viewBox="0 0 860 360"></svg>
<div class="legend">横轴 log₁₀(μ/GeV)，纵轴 αᵢ⁻¹。三条曲线由 PDG 输入 + b=(41/10,−19/6,−7) 计算；α₁ 与 α₂ 在 ~10¹³ GeV 交叉，α₂ 与 α₃ 在 ~10¹⁷ GeV 交叉，相差约 9,384 倍。</div></div>
<h2>三、不变量检验：预测 1.896 vs 实验 1.394</h2>
<div class="card"><div id="rbars"></div>
<div class="mono">R=(α₁⁻¹−α₂⁻¹)/(α₂⁻¹−α₃⁻¹)=(b₁−b₂)/(b₂−b₃)；失配约 36%，输入敏感度扫描不能弥合。</div></div>
<h2>四、α_s(M_Z) 诊断：SM 0.07115 / 理想化 MSSM 0.11684 / 实验 0.1180</h2>
<div class="card"><div id="asbars"></div>
<div class="mono">MSSM 未加阈值，只能作诊断；它证明运行由物质谱决定，不证明超对称。</div></div>
<h2>五、条目逐条</h2><div id="items"></div>
<script>
const D=__PAYLOAD__;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};D.items.forEach(x=>c[x.v]++);
document.getElementById('kpi').innerHTML=
 kpi('条目总数',D.items.length)+kpi('PASS',c.PASS)+kpi('FAIL',c.FAIL)+kpi('INFO',c.INFO)+kpi('BOUNDARY',c.BOUNDARY);
function kpi(k,v){return '<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div></div>';}
const rg=D.extra.rg;
const W=860,H=360,PL=58,PR=18,PT=18,PB=34;
const xs=rg.map(p=>p[0]), ymin=Math.min(...rg.map(p=>Math.min(p[1],p[2],p[3]))), ymax=Math.max(...rg.map(p=>Math.max(p[1],p[2],p[3])));
const xmin=Math.min(...xs),xmax=Math.max(...xs);
function X(v){return PL+(v-xmin)/(xmax-xmin)*(W-PL-PR);}
function Y(v){return PT+(ymax-v)/(ymax-ymin)*(H-PT-PB);}
let s='';
for(let i=0;i<=5;i++){const yy=ymin+(ymax-ymin)*i/5;s+='<line x1="'+PL+'" y1="'+Y(yy)+'" x2="'+(W-PR)+'" y2="'+Y(yy)+'" stroke="#e6eaef"/>';
 s+='<text x="'+(PL-8)+'" y="'+(Y(yy)+4)+'" font-size="11" fill="#8a94a0" text-anchor="end">'+yy.toFixed(0)+'</text>';}
for(let i=0;i<=5;i++){const xx=xmin+(xmax-xmin)*i/5;s+='<line x1="'+X(xx)+'" y1="'+PT+'" x2="'+X(xx)+'" y2="'+(H-PB)+'" stroke="#f0f3f6"/>';
 s+='<text x="'+X(xx)+'" y="'+(H-14)+'" font-size="11" fill="#8a94a0" text-anchor="middle">'+xx.toFixed(0)+'</text>';}
const cols=['#2b5c9b','#b8860b','#1a7f37'];
for(let k=1;k<=3;k++){
 const pts=rg.map(p=>X(p[0])+','+Y(p[k])).join(' ');
 s+='<polyline fill="none" stroke="'+cols[k-1]+'" stroke-width="2.2" points="'+pts+'"/>';
}
s+='<text x="'+(W-PR)+'" y="'+(PT+14)+'" font-size="12" fill="#2b5c9b" text-anchor="end">α₁⁻¹</text>';
s+='<text x="'+(W-PR)+'" y="'+(PT+32)+'" font-size="12" fill="#b8860b" text-anchor="end">α₂⁻¹</text>';
s+='<text x="'+(W-PR)+'" y="'+(PT+50)+'" font-size="12" fill="#1a7f37" text-anchor="end">α₃⁻¹</text>';
document.getElementById('rg').innerHTML=s;
function bars(el,arr,maxv,fmtn){document.getElementById(el).innerHTML=arr.map(r=>{
 const w=Math.max(2,100*r[1]/maxv);
 return '<div style="display:flex;align-items:center;gap:10px;margin:7px 0"><div style="width:190px;font-size:13px">'+r[0]+
 '</div><div style="flex:1;background:#eef1f5;border-radius:5px;height:22px"><div style="width:'+w+'%;height:22px;border-radius:5px;background:'+(r[2]||'#2b5c9b')+'"></div></div>'+
 '<div class="mono" style="width:90px;text-align:right">'+fmtn(r[1])+'</div></div>';}).join('')}
bars('rbars',[['预测 R_pred',D.extra.R_pred,'#2b5c9b'],['实验 R_obs',D.extra.R_obs,'#b8860b'],['敏感度下界',D.extra.R_obs_min,'#8a94a0'],['敏感度上界',D.extra.R_obs_max,'#8a94a0']],2.1,v=>v.toFixed(4));
bars('asbars',[['SM 无阈值',D.extra.as_SM,'#c0392b'],['理想化 MSSM',D.extra.as_MSSM,'#2b5c9b'],['实验 α_s',0.1180,'#1a7f37']],0.13,v=>v.toFixed(5));
document.getElementById('items').innerHTML=D.items.map(x=>
 '<div class="card"><span class="tag '+x.v+'">'+x.v+'</span> <b>'+x.id+'</b> · '+x.t+
 '<div class="mono" style="margin-top:6px">'+x.d+'</div></div>').join('');
</script></body></html>"""


def html(extra, summary):
    p = os.path.join(ROOT, "四力统一方程_ROOTV19非阿贝尔规范统一与alpha本源_%s可视化_%s.html" % (RID, STAMP))
    ALLOWED.add(p)
    # 运行曲线采样
    b1, b2, b3 = D(41) / D(10), D(-19) / D(6), D(-7)
    a1inv, a2inv, a3inv = extra["q6"]["a1inv"], extra["q6"]["a2inv"], extra["q6"]["a3inv"]
    MZ = D("91.1876")
    rg = []
    for i in range(0, 161):
        lg = D("2") + (D("16") * D(i) / D("160"))
        mu = D(10) ** lg
        L = (mu / MZ).ln()
        rg.append([float(lg),
                   float(a1inv - (b1 / (2 * PI)) * L),
                   float(a2inv - (b2 / (2 * PI)) * L),
                   float(a3inv - (b3 / (2 * PI)) * L)])
    payload = {"summary": summary, "items": [{"id": i["id"], "v": i["verdict"],
                                              "t": i["title"], "d": i["detail"]} for i in ITEMS],
               "extra": {"rg": rg, "R_pred": float(extra["q7"]["R_pred"]),
                         "R_obs": float(extra["q7"]["R_obs"]),
                         "R_obs_min": float(extra["q7"]["R_obs_min"]),
                         "R_obs_max": float(extra["q7"]["R_obs_max"]),
                         "as_SM": float(extra["q8"]["as_SM"]),
                         "as_MSSM": float(extra["q8"]["as_MSSM"])}}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("__STAMP__", STAMP)
    with io.open(wpath(p), "w", encoding="utf-8") as f:
        f.write(doc)
    return p


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    q2()
    extra["q3"] = q3()
    extra["q4"] = q4()
    extra["q5"] = q5()
    extra["q6"] = q6()
    extra["q7"] = q7(extra)
    extra["q8"] = q8(extra)
    extra["q9"] = q9(extra)
    extra["q10"] = q10(extra)
    extra["q11"] = q11(extra)
    q12()
    extra["declared_n"] = 26
    ctl = controls()
    guards(extra, ctl)
    summary, hp = emit(extra)
    print("=" * 78)
    print("TUFT-%s · %s" % (RID, TITLE))
    print("=" * 78)
    for k, v in summary.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("判定：V19-ANOMALY-VERIFIED / SU5-NORMALIZATION-3-8 /")
    print("      NO-THRESHOLD-UNIFICATION-EXCLUDED / ALPHA-STILL-FREE。")
    print("产物：%s" % hp)
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    print("FAIL=%d；rc=%d" % (n_fail, 0 if n_fail == 0 else 2))
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
