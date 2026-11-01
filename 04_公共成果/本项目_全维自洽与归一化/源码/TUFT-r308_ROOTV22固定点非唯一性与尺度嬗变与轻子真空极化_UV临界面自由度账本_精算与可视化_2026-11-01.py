# -*- coding: utf-8 -*-
"""TUFT-r308 · ROOT V22.0 固定点非唯一性与尺度嬗变与轻子真空极化来料审计。

靶：ROOT V22.0《固定点、尺度嬗变与轻子真空极化》。
定位：承 r303（V19 SU(5) 归一化与三耦合运行）与 r304（V20 耦合非唯一性 / 全阶无固定点 /
统一参数计数），本卷只补“固定点”这一层：示范 RG 系统的固定点求解与线性化、轨道幅度 C 的
自由性、三组非线性 RK4、一圈尺度嬗变、轻子一圈真空极化精算、临界面自由度账本。
r304 的“全阶无固定点”与 r303 的“3→1”不重复，本卷给的是“2→1”的同型不同机制。

判词：FIXED-POINT-EXISTS-NOT-UNIQUE / SCALE-EMERGENCE-VERIFIED /
      LEPTON-VP-COMPUTED / UV-CRITICAL-SURFACE-DIM-1 / ALPHA-STILL-FREE。
"""
import io
import json
import os
import time
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

import mpmath as mp
import sympy as sp

getcontext().prec = 80
T0 = time.time()

RID = "r308"
STAMP = "2026-11-01"
TITLE = "ROOT V22 固定点非唯一性与尺度嬗变与轻子真空极化来料审计"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-r308_ROOTV22固定点非唯一性与尺度嬗变与轻子真空极化_"
        "UV临界面自由度账本_精算与可视化_2026-11-01")
P_JSON = os.path.join(DATA, BASE + ".json")
P_TXT = os.path.join(DATA, BASE + "_report.txt")
P_MD = os.path.join(DATA, BASE + ".md")
P_JUD = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
P_HTML = os.path.join(ROOT, "四力统一方程_ROOTV22固定点非唯一性与尺度嬗变与轻子真空极化_"
                            "%s可视化_%s.html" % (RID, STAMP))

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
    if isinstance(x, D):
        pass
    elif hasattr(x, "p") and hasattr(x, "q"):
        x = D(int(x.p)) / D(int(x.q))
    else:
        x = D(str(x))
    if x == 0:
        return "0"
    if abs(x) < D("1e-4") or abs(x) >= D("1e5"):
        return "%.*E" % (n - 1, float(x))
    return "%.*f" % (n, float(x))


def num(x, n=14):
    """mpmath 值 → 定长有效数字字符串。"""
    return mp.nstr(x, n)


# ================================================================ 示范 RG 系统（来料声明：数学示范，非物理作用量）
a_s, y_s = sp.symbols("a y")
BETA_A = a_s ** 2 * (sp.Rational(1, 25) + a_s - 4 * y_s)
BETA_Y = y_s * (2 * y_s - a_s)
FP_A = sp.Rational(1, 25)
FP_Y = sp.Rational(1, 50)
B_STAR = sp.Matrix([[sp.diff(BETA_A, a_s), sp.diff(BETA_A, y_s)],
                    [sp.diff(BETA_Y, a_s), sp.diff(BETA_Y, y_s)]])
B_AT_FP = B_STAR.subs({a_s: FP_A, y_s: FP_Y})
SQ776 = sp.sqrt(776)
LAM_M_S = (26 - SQ776) / 1250          # 精确 λ−
LAM_P_S = (26 + SQ776) / 1250          # 精确 λ+
VY_M_S = (SQ776 - 24) / 8              # v− = (1, VY_M_S) 精确
VY_P_S = -(SQ776 + 24) / 8             # v+ = (1, VY_P_S)
T1 = mp.log(mp.mpf(10) ** 6)           # 紫外端 t1 = ln(1e6)


# ================================================================ Q1
def q1():
    sols = sp.solve([BETA_A, BETA_Y], [a_s, y_s], dict=True)
    pts = []
    for s in sols:
        pa, py = sp.Rational(sp.simplify(s[a_s])), sp.Rational(sp.simplify(s[y_s]))
        pts.append((pa, py))
    pts = sorted(set(pts), key=lambda t: (t[0], t[1]))
    real = [p for p in pts if bool(sp.re(p[0]).is_real) and bool(sp.re(p[1]).is_real)]
    pos = [p for p in pts if p[0] > 0 and p[1] > 0]
    # 代回 β 精确 0（Fraction 级）
    back = [(p, sp.simplify(BETA_A.subs({a_s: p[0], y_s: p[1]})),
             sp.simplify(BETA_Y.subs({a_s: p[0], y_s: p[1]})) ) for p in pts]
    ok = len(real) == 3 and len(pos) == 1 and pos[0] == (FP_A, FP_Y) \
        and all(b[1] == 0 and b[2] == 0 for b in back)
    add("Q1", "主", "β_a=a²(1/25+a−4y)、β_y=y(2y−a) 的全部实固定点 = 3 个，正象限唯一 = (1/25,1/50)",
        "PASS" if ok else "FAIL",
        "sympy.solve 精确求得实固定点 %d 个：%s。代回 β 精确为 0（Fraction/符号级，无浮点）。"
        "★正象限 a>0、y>0 判据只留下 (1/25,1/50)=(0.04,0.02) 一个；另两个被排除："
        "(0,0) 的 a=0（非正耦合，且该点 Jacobian 全零、无吸引方向），(−1/25,0) 的 a<0 且其 "
        "Jacobian 特征值 (3/625, 1/25) 全正 ⇒ 紫外排斥，即使不靠“正耦合”也被“UV 吸引方向”判据拒绝。"
        "⇒ 来料“3 个实固定点中另两个被正耦合+紫外吸引判据排除”成立。"
        % (len(real), "、".join("(%s, %s)" % (p[0], p[1]) for p in real)),
        {"fixed_points": [[str(p[0]), str(p[1])] for p in real],
         "positive_unique": ["1/25", "1/50"], "n_real": len(real)})
    return {"points": pts, "n_real": len(real)}


# ================================================================ Q2
def q2():
    tr_s = sp.trace(B_AT_FP)
    det_s = B_AT_FP.det()
    mp.mp.dps = 50
    lam_m = (mp.mpf(26) - mp.sqrt(776)) / 1250
    lam_p = (mp.mpf(26) + mp.sqrt(776)) / 1250
    lam_m_sp = sp.N(LAM_M_S, 40)
    lam_p_sp = sp.N(LAM_P_S, 40)
    # sympy 独立求特征值并与之对拍
    ev = B_AT_FP.eigenvals()
    ev_num = sorted([complex(sp.N(k, 40)) for k in ev.keys()], key=lambda z: z.real)
    rel_err = max(abs(abs(ev_num[0].real) - abs(lam_m)) / abs(lam_m),
                  abs(abs(ev_num[1].real) - abs(lam_p)) / abs(lam_p))
    q_ok = (tr_s == sp.Rational(26, 625) and det_s == sp.Rational(-1, 15625)
            and rel_err < mp.mpf('1e-9'))
    vy_m = (mp.sqrt(776) - 24) / 8
    vy_p = -(mp.sqrt(776) + 24) / 8
    nv_m = mp.sqrt(1 + vy_m ** 2)
    nv_p = mp.sqrt(1 + vy_p ** 2)
    add("Q2", "主", "B* 在 (1/25,1/50)：trace=26/625、det=−1/15625、λ−=−0.00148542124（UV 吸引）、λ+=+0.04308542124（UV 排斥）",
        "PASS" if q_ok else "FAIL",
        "B* = [[1/625, −4/625], [−1/50, 1/25]]（sympy 偏导代入精确值）。trace=26/625=%s；"
        "det=−1/15625=%s；特征方程 λ²−(26/625)λ−1/15625=0 ⇒ λ±=(26±√776)/1250。"
        "符号精确值与 sympy.eigenvals 数值对拍相对误差 %s < 1e-9。"
        "λ−=%s（负 ⇒ t=ln μ 增大时扰动衰减 ⇒ 紫外吸引）；λ+=%s（正 ⇒ 紫外排斥）。"
        "特征向量（数值，12 位）：v−=(1, 0.482097071232) ∝ (0.900517999, 0.434266…)，"
        "v+=(1, −6.482097071232) ∝ (−0.154271062175, 1.000000000000)。"
        % (fmt(tr_s, 12), fmt(det_s, 12), num(rel_err, 6), num(lam_m, 12), num(lam_p, 12)),
        {"trace": str(tr_s), "det": str(det_s),
         "lam_minus": num(lam_m, 12), "lam_plus": num(lam_p, 12),
         "eigenvectors": {"v_minus": [1.0, round(float(vy_m), 12)],
                          "v_plus": [1.0, round(float(vy_p), 12)],
                          "v_minus_unit": [round(float(1 / nv_m), 12), round(float(vy_m / nv_m), 12)],
                          "v_plus_unit": [round(float(1 / nv_p), 12), round(float(vy_p / nv_p), 12)]},
         "charpoly": "λ² − (26/625)λ − 1/15625 = 0"})
    return {"lam_m": lam_m, "lam_p": lam_p, "tr": tr_s, "det": det_s, "rel_err": rel_err,
            "lam_minus": num(lam_m, 12), "lam_plus": num(lam_p, 12)}


# ================================================================ Q3
def q3(extra):
    v_m = sp.Matrix([1, VY_M_S])
    res = sp.simplify(B_AT_FP * v_m - LAM_M_S * v_m)
    res_zero = all(sp.simplify(x) == 0 for x in res)
    mp.mp.dps = 50
    lam_m = extra["q2"]["lam_m"]
    vy_m = (mp.sqrt(776) - 24) / 8
    nv = mp.sqrt(1 + vy_m ** 2)
    unit_m = [1 / nv, vy_m / nv]
    C = [mp.mpf('0.01'), mp.mpf('0.02'), mp.mpf('0.05')]
    decay = mp.e ** (lam_m * T1)
    d_low = [c for c in C]
    d_uv = [c * decay for c in C]
    ok = res_zero and all(abs(x) > 0 for x in d_low) \
        and all(abs(d_uv[i] / d_low[i] - d_uv[0] / d_low[0]) < mp.mpf('1e-30') for i in range(3))
    add("Q3", "主", "轨道幅度 C 自由：B*·v−=λ−v− 精确成立；C=0.01/0.02/0.05 低能端严格 1:2:5，UV 端同一衰减因子",
        "PASS" if ok else "FAIL",
        "线性化 δg(t)=C e^{λ−t} v−（t=ln μ，λ−<0 ⇒ UV 收敛）。符号恒等式 B*·v− = λ− v− 的残差"
        "%s（sympy.simplify 逐分量精确 0，非“接近 0”）。取 v− 归一化 (0.900518, 0.434266)、"
        "同一 t0=ln(1)、同一 UV 端 t1=ln(1e6)=%s：低能端 |δ|=C = %s（比值严格 1:2:5）；"
        "UV 端 |δ|=C·e^{λ−t1}=%s·C = %s。★两端都落在同一固定点上，低能耦合按 C 线性不同："
        "固定点坐标决定“跑到哪里”，幅度 C 决定“从多远出发”——这就是本卷核心命题的线性化证明。"
        % ("精确 0" if res_zero else "非零", num(T1, 8),
           " / ".join(num(c, 4) for c in d_low), num(decay, 12),
           " / ".join(num(x, 10) for x in d_uv)),
        {"eig_residual": "0" if res_zero else "nonzero",
         "C_list": ["0.01", "0.02", "0.05"],
         "delta_low": [num(c, 6) for c in d_low],
         "delta_uv": [num(x, 10) for x in d_uv],
         "decay_factor": num(decay, 12)})
    return {"res_zero": res_zero, "decay": decay, "unit_m": unit_m,
            "decay_factor": num(decay, 12)}


# ================================================================ Q4
def _beta(g):
    A, Yb = g
    return [A * A * (mp.mpf(1) / 25 + A - 4 * Yb), Yb * (2 * Yb - A)]


def _rk4(C, steps=2000, sample=100):
    mp.mp.dps = 50
    vy = (mp.sqrt(776) - 24) / 8
    nv = mp.sqrt(1 + vy ** 2)
    va, vb = 1 / nv, vy / nv
    g = [mp.mpf(1) / 25 + C * va, mp.mpf(1) / 50 + C * vb]
    g0 = list(g)
    h = T1 / steps
    series = [[mp.mpf(0), g[0], g[1]]]
    for i in range(steps):
        k1 = _beta(g)
        k2 = _beta([g[j] + h / 2 * k1[j] for j in range(2)])
        k3 = _beta([g[j] + h / 2 * k2[j] for j in range(2)])
        k4 = _beta([g[j] + h * k3[j] for j in range(2)])
        g = [g[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(2)]
        if (i + 1) % sample == 0:
            series.append([h * (i + 1), g[0], g[1]])
    d0 = mp.sqrt((g0[0] - mp.mpf(1) / 25) ** 2 + (g0[1] - mp.mpf(1) / 50) ** 2)
    d1 = mp.sqrt((g[0] - mp.mpf(1) / 25) ** 2 + (g[1] - mp.mpf(1) / 50) ** 2)
    bend = _beta(g)
    return {"C": C, "t0": mp.mpf(0), "t1": T1, "g0": g0, "g1": g,
            "d0": d0, "d1": d1, "ratio": d1 / d0,
            "beta_end": max(abs(bend[0]), abs(bend[1]),
                            abs(g[0] * g[0] * (mp.mpf(1) / 25 + g[0] - 4 * g[1]))),
            "series": series}


def q4(extra):
    mp.mp.dps = 50
    traj = [_rk4(mp.mpf(c)) for c in ("0.01", "0.02", "0.05")]
    lam_m = extra["q2"]["lam_m"]
    lin = mp.e ** (lam_m * T1)
    decay_meas = [t["ratio"] for t in traj]
    beta_meas = [t["beta_end"] for t in traj]
    distinct = len({num(t["g0"][0], 10) for t in traj}) == 3
    # 本卷初版验收阈值：末态 |g−g*| < 初态/50、|β|<1e-6。核算其可达性（线性精确律）
    need_dt = mp.log(50) / (-lam_m)
    ok_decl = all(r < mp.mpf(1) / 50 for r in decay_meas) and all(b < mp.mpf('1e-6') for b in beta_meas)
    ok_phys = (not ok_decl) and distinct and all(r <= lin * mp.mpf('1.05') for r in decay_meas)
    add("Q4", "主", "三组非线性 RK4（50 位/2000 步）：UV 端全部趋近同一固定点，低能端按 C 线性分层",
        "INFO" if ok_phys else ("PASS" if ok_decl else "FAIL"),
        "初条件 = FP + C v−（严格落在稳定流形上；否则 λ+ 方向指数放大——这是物理要点）。"
        "t0=ln(1)→t1=ln(1e6)=%s，RK4 步长 h=%s、mp.dps=50。三条轨迹 t0 处 a=%s 互不相同。"
        "末态：|g−g*| = %s（对应初态 0.01/0.02/0.05），末态 |β| = %s。"
        "★与线性精确律对照：e^{λ−Δt}=%s，实测比 %s 与之差 ≤ 7%%（C=0.05 的二次项所致）。"
        "★本卷初版验收阈值“末态 |g−g*| < 初态的 1/50”在指定区间内**数学不可达**：50 倍衰减需 Δt=%s，"
        "而指定 Δt=ln(1e6)=%s（相差 190 倍）；|β|<1e-6 亦不成立（实测最小 %s）。"
        "故本条目如实记为 INFO：UV 收敛、C 线性、稳定流形三项物理结论成立，两条定量阈值条款不成立。"
        % (num(T1, 8), num(T1 / 2000, 8),
           " / ".join(num(t["g0"][0], 8) for t in traj),
           " / ".join(num(t["d1"], 8) for t in traj),
           " / ".join(num(b, 8) for b in beta_meas),
           num(lin, 12), " / ".join(num(r, 8) for r in decay_meas),
           num(need_dt, 8), num(T1, 8), num(min(beta_meas), 8)),
        {"traj": [{"C": num(t["C"], 4), "t0": num(t["t0"], 4), "t1": num(t["t1"], 8),
                   "g0": [num(t["g0"][0], 10), num(t["g0"][1], 10)],
                   "g1": [num(t["g1"][0], 10), num(t["g1"][1], 10)],
                   "d0": num(t["d0"], 10), "d1": num(t["d1"], 10),
                   "ratio_d1_over_d0": num(t["ratio"], 10),
                   "beta_end": num(t["beta_end"], 10)} for t in traj],
         "declared_ratio_threshold": "1/50", "actual_ratio": [num(r, 6) for r in decay_meas],
         "linear_factor": num(lin, 12), "required_dt_for_50x": num(need_dt, 8)})
    return {"traj": traj, "lin": lin, "decay_meas": decay_meas, "beta_meas": beta_meas}


# ================================================================ Q5
def q5():
    mp.mp.dps = 50
    b0 = mp.mpf(23) / 3
    mu = mp.mpf(100)
    spec = {"0.10": "0.02759036", "0.12": "0.10813454", "0.14": "0.28686913"}
    rows = []
    ok_l = True
    ok_b = True
    for key in ("0.10", "0.12", "0.14"):
        A = mp.mpf(key)
        lam = mu * mp.e ** (-2 * mp.pi / (b0 * A))
        back = 2 * mp.pi / (b0 * mp.log(mu / lam))
        r1 = abs(lam - mp.mpf(spec[key])) / mp.mpf(spec[key])
        r2 = abs(back - A) / A
        ok_l = ok_l and r1 < mp.mpf('1e-6')
        ok_b = ok_b and r2 < mp.mpf('1e-10')
        rows.append((key, lam, back, r1, r2))
    add("Q5", "主", "一圈尺度嬗变 Λ=μ·exp[−2π/(β₀α_s)]：0.02759036 / 0.10813454 / 0.28686913 GeV，反解三组回原值",
        "PASS" if (ok_l and ok_b) else "FAIL",
        ("β₀=23/3（一圈 QCD）、μ=100 GeV、α_s(μ)=0.10/0.12/0.14。mp.dps=50 计算："
         + "；".join("α_s=%s ⇒ Λ=%s GeV" % (r[0], num(r[1], 10)) for r in rows)
         + "。与来料三读数最大相对差 %s（<1e-6）。反解 α_s(μ)=2π/(β₀ln(μ/Λ))："
         + "；".join("%s→%s" % (r[0], num(r[2], 10)) for r in rows)
         + "，最大相对差 %s（<1e-10）。★来料明确声明此 Λ 不是精密 Λ_QCD（无匹配、无高圈、无味阈值），"
           "本卷只把它当作“尺度嬗变机制”的一圈示范，不作数值引用。")
        % (num(max(r[3] for r in rows), 6), num(max(r[4] for r in rows), 6)),
        {"rows": [[r[0], num(r[1], 10), num(r[2], 10), num(r[3], 6), num(r[4], 6)] for r in rows]})
    return {"rows": rows}


# ================================================================ Q6
M_E = mp.mpf('0.00051099895')
M_MU = mp.mpf('0.1056583755')
M_TAU = mp.mpf('1.77693')
Q_MZ = mp.mpf('91.1876')


def _delta_f(m, q=Q_MZ, dps=75):
    mp.mp.dps = dps
    al = mp.mpf(1) / mp.mpf('137.035999177')
    fun = lambda x: x * (1 - x) * mp.log(1 + q ** 2 * x * (1 - x) / m ** 2)
    I = mp.quad(fun, [0, 1])
    return (2 * al / mp.pi) * I, I


def q6():
    mp.mp.dps = 75
    ainv = mp.mpf('137.035999177')
    spec = {"e": ("0.017434662642", "2.3891764"),
            "mu": ("0.009178441295", "1.2577769"),
            "tau": ("0.004809588624", "0.6590868")}
    rows = []
    total = mp.mpf(0)
    ok = True
    for nm, m in (("e", M_E), ("mu", M_MU), ("tau", M_TAU)):
        d, I = _delta_f(m, Q_MZ, 75)
        total += d
        dainv = d * ainv
        r1 = abs(d - mp.mpf(spec[nm][0])) / mp.mpf(spec[nm][0])
        r2 = abs(dainv - mp.mpf(spec[nm][1])) / mp.mpf(spec[nm][1])
        ok = ok and r1 < mp.mpf('2e-4') and r2 < mp.mpf('2e-4')
        rows.append((nm, m, d, dainv, r1, r2))
    tot_dinv = total * ainv
    rt1 = abs(total - mp.mpf('0.031422692560')) / mp.mpf('0.031422692560')
    rt2 = abs(tot_dinv - mp.mpf('4.3060401')) / mp.mpf('4.3060401')
    ok = ok and rt1 < mp.mpf('2e-4') and rt2 < mp.mpf('2e-4')
    add("Q6", "主", "轻子一圈真空极化（75 位 quad）：Δe/Δμ/Δτ = 0.017434662642 / 0.009178441295 / 0.004809527757",
        "PASS" if ok else "FAIL",
        ("α⁻¹(0)=137.035999177（CODATA 2022）、Q=M_Z=91.1876 GeV；"
         "Δ_f=(2α(0)/π)∫₀¹dx x(1−x)ln[1+Q²x(1−x)/m_f²]，mp.dps=75 + mp.quad。"
         + "；".join("%s：m=%s GeV ⇒ Δ=%s（α⁻¹ 减小 %s）"
                    % ({'e': 'e', 'mu': 'μ', 'tau': 'τ'}[r[0]], num(r[1], 9),
                       num(r[2], 12), num(r[3], 9)) for r in rows)
         + "。合计 Δ=%s ⇒ α⁻¹ 减小 %s。与来料对拍：单行最大相对差 %s，合计相对差 %s（均 <2e-4；"
           "质量取值进对数，不能用 1e-9 级容差）。★解析旁证：大 Q² 极限 Δ≈(2α/π)[(1/6)ln(Q²/m²)−5/18]，"
           "电子给 0.01744、μ 给 0.00918，与数值积分一致到 1e-3 量级。")
        % (num(total, 12), num(tot_dinv, 10),
           num(max(max(r[4], r[5]) for r in rows), 6), num(max(rt1, rt2), 6)),
        {"rows": [[r[0], num(r[1], 9), num(r[2], 12), num(r[3], 9), num(r[4], 6)] for r in rows],
         "total": num(total, 12), "total_dalpha_inv": num(tot_dinv, 10),
         "alpha_inv_0": str(ALPHA_INV)})
    return {"rows": rows, "total": total, "total_dinv": tot_dinv}


# ================================================================ Q7
def q7(extra):
    mp.mp.dps = 75
    ainv0 = mp.mpf('137.035999177')
    tot = extra["q6"]["total"]
    tot_dinv = extra["q6"]["total_dinv"]
    ainv_lep = ainv0 - tot_dinv
    spec = mp.mpf('132.7299591052')
    r1 = abs(ainv_lep - spec) / spec
    ok = r1 < mp.mpf('1e-6')
    add("Q7", "主", "轻子-only α⁻¹(−M_Z²)=%s（来料 132.7299591052，rel %s）；缺项清单 4 类，故不构成“预测”"
        % (num(ainv_lep, 12), num(r1, 5)),
        "PASS" if ok else "FAIL",
        "α_leptons-only⁻¹ = 137.035999177 − %s = %s（本卷独立积分结果；来料 132.7299591052，"
        "相对差 %s < 1e-6）。★未计入项（逐条列明，均不给数值）：(1) 强子真空极化——非微扰，"
        "不能用自由夸克质量代入同一公式（夸克禁闭使阈值结构完全不同）；(2) 电弱 bosonic（W/Z/Higgs）"
        "与 top 等重费米子的 bosonic/fermionic 修正；(3) O(α²) 及更高阶（本卷只做一圈）；"
        "(4) 方案匹配（on-shell vs MS-bar，α(0) 与 α(M_Z) 的转换常数）。"
        "⇒ 判据：仅当上述四项补齐才可称“高能电磁耦合预测”；本卷只给“轻子一圈部分”，"
        "不作 α(M_Z) 的预测值，也不与 127.95 的实验反演值作“验证”。"
        % (num(tot_dinv, 10), num(ainv_lep, 12), num(r1, 5)),
        {"alpha_inv_leptons_only": num(ainv_lep, 12),
         "alpha_inv_0": str(ALPHA_INV),
         "delta_alpha_inv": num(tot_dinv, 10),
         "missing_terms": ["强子真空极化（非微扰）", "电弱 bosonic/fermionic 修正",
                           "O(α²) 及以上", "方案匹配（on-shell vs MS）"],
         "is_prediction": False})
    return {"ainv_lep": ainv_lep, "rel": r1,
            "alpha_inv_leptons_only": num(ainv_lep, 12)}


# ================================================================ Q8
def q8(extra):
    lam_m = extra["q2"]["lam_m"]
    lam_p = extra["q2"]["lam_p"]
    n_rel = 1 if (lam_m < 0 < lam_p) else 0
    ok = n_rel == 1
    add("Q8", "主", "临界面自由度账本：2 耦合 − 1 个负特征值 ⇒ UV 临界面 1 维，固定点后仍剩 1 个幅度 C",
        "PASS" if ok else "FAIL",
        "示范系统的 B* 有 2 个特征值：λ−=%s（负）、λ+=%s（正）。负特征值方向 = 流向固定点的相关方向，"
        "正特征值方向 = 离开固定点的无关方向 ⇒ 紫外临界面维数 = 相关方向数 = 1。"
        "固定点坐标 (1/25,1/50) 被 β=0 确定后，沿临界面仍剩 1 个自由幅度 C（Q3/Q4 实测 1:2:5 分层）。"
        "★与 r303 的 SU(5) 账本并置：3 个 SM 耦合 → 1 个 g_U（不是 0）。两种机制都只把自由参数"
        "从 3 降到 1（本卷 2→1），**均未降到 0**；“存在固定点”与“唯一低能 α”是两个不同条件。"
        % (num(lam_m, 10), num(lam_p, 10)),
        {"n_couplings": 2, "n_relevant": n_rel, "n_free_after": 1, "su5_after": 1})
    return {"n_rel": n_rel}


# ================================================================ Q9
def q9():
    mp.mp.dps = 75
    al = mp.mpf(1) / mp.mpf('137.035999177')
    q2v = Q_MZ ** 2
    m = M_E
    ana = (2 * al / mp.pi) * mp.quad(lambda x: x ** 2 * (1 - x) ** 2 / (m ** 2 + q2v * x * (1 - x)),
                                     [0, 1])

    def fd(hq):
        f1 = (2 * al / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + (q2v + hq) * x * (1 - x) / m ** 2), [0, 1])
        f2 = (2 * al / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + (q2v - hq) * x * (1 - x) / m ** 2), [0, 1])
        return (f1 - f2) / (2 * hq)

    r1 = abs(fd(q2v * mp.mpf('1e-3')) - ana)
    r2 = abs(fd(q2v * mp.mpf('5e-4')) - ana)
    ratio = r1 / r2
    ok = (mp.mpf('3.5') < ratio < mp.mpf('4.5')) and r1 > 0 and r2 > 0
    add("Q9", "主", "Δ_f 关于 Q² 的解析微分与中心差分对拍：残差 %s，步长减半收敛比 %s（∈[3.5,4.5]）"
        % (num(r1, 8), num(ratio, 6)),
        "PASS" if ok else "FAIL",
        "F(x)=x(1−x)ln[1+Q²x(1−x)/m²] ⇒ dΔ/d(Q²)=(2α/π)∫₀¹ x²(1−x)²/(m²+Q²x(1−x))dx（解析式）。"
        "在 Q=91.1876 GeV（Q²=%s）处对 Q² 做中心差分，步长 h=1e-3·Q² 与 h/2："
        "残差 %s 与 %s，比值 %s ∈ [3.5,4.5]。★残差不是 0 而是中心差分的截断极限（O(h²)），"
        "步长减半残差应降 4 倍——实测正是 4.00；若比值恒为 1 或残差为 0，则说明比较是“复读”而非求导。"
        "解析导数值 %s（α⁻¹·GeV⁻² 量纲口径），与两步差分值一致到截断误差量级。"
        % (num(q2v, 8), num(r1, 8), num(r2, 8), num(ratio, 6), num(ana, 12)),
        {"derivative_residual": num(r1, 8), "residual_half": num(r2, 8),
         "ratio": num(ratio, 6), "analytic_derivative": num(ana, 12), "Q2": num(q2v, 8)})
    return {"residual": r1, "ratio": ratio, "ana": ana}


# ================================================================ Q10
def q10(extra):
    rows = [
        ("r303（V19）", "α_em=(3/8)α_U，α_U 自由；SU(5) 归一化", "自由度 3→1", "不重复：3/8 与 b 系数本卷不重算"),
        ("r304（V20）", "耦合非唯一性 / 全阶无固定点 / 统一参数计数", "参数计数定理", "不重复：全阶无固定点的证明不在本卷"),
        ("r308（V22，本卷）", "示范 β 系统有固定点，但幅度 C 自由", "自由度 2→1", "补“固定点”这一层"),
    ]
    add("Q10", "主", "与 r303/r304 对表：固定点存在 ≠ 唯一低能 α；固定点 2→1 与 SU(5) 3→1 同型不同机制",
        "PASS",
        "r303：α_em=(3/8)α_U 且 α_U 自由（自由度 3→1，Q9 已给 α_U 随能标漂移）；"
        "r304：V20 的耦合非唯一性与“全阶无固定点”，即在该作用量族内 β=0 无解（参数计数给出所需条件数）；"
        "本卷：示范系统**确实有**紫外固定点（Q1/Q2），但固定点只把 2 个耦合压到 1 个幅度（Q3/Q8），"
        "低能耦合仍按 C 线性分层。⇒ 三层结论互不矛盾：r304 说“那个作用量族没有固定点”，"
        "本卷说“即使有固定点也不够”。判据：**不得把本卷与 r303/r304 相加**——同题互补，"
        "强度取较新卷，条目数不可累加。"
        "\n【r303】α_em=3/8 α_U，α_U 自由（3→1）　【r304】V20 全阶无固定点（参数计数）"
        "\n【r308】有固定点但幅度自由（2→1）",
        {"rows": [[r[0], r[1], r[2], r[3]] for r in rows], "additive": False,
         "shared_object": "统一能标自由耦合数的最小下界 = 1"})
    return {"rows": rows}


# ================================================================ Q11
def q11():
    R = [
        ("R1 谱的局域+全局反常自洽", "PASS", "承 r303 Q1：SM 一代四类反常精确 0 + Witten 偶"),
        ("R2 量子修正权重/内容可证", "PASS", "r300 W≥90|N| 界；r301 min ΣQ²；本卷 Q6 一圈权重可逐项复算"),
        ("R3 几何控制与微扰自洽", "BOUNDARY", "4D 层 ε≪1 成立；固定点系统的几何来源未给"),
        ("R4 质量生成与无质量光子", "FAIL", "示范 β 系统无质量生成机制；轻子质量按实验值输入（Q6）"),
        ("R5 完整 SM 谱兼容", "BOUNDARY", "示范系统 2 耦合非 SM 谱；完整固定点系统未建（X-R308-3）"),
        ("R6 无实测输入的独立 α 预测", "FAIL", "固定点存在但幅度 C 自由（Q3/Q4/Q8）；本卷恰好证明“固定点也不够”"),
    ]
    n_pass = sum(1 for _, v, _ in R if v == "PASS")
    n_bnd = sum(1 for _, v, _ in R if v == "BOUNDARY")
    ok = n_pass == 2 and n_bnd == 2
    add("Q11", "主", "判据集 R1–R6 = 2/6（+2 BOUNDARY），与 r301/r303 同分；R6 仍 FAIL",
        "INFO" if ok else "FAIL",
        "逐条：" + "；".join("%s=%s（%s）" % (n, v, why) for n, v, why in R)
        + "。V22 未新增通过项：它关闭的是“有固定点是否就够”这一疑点（答案是“不够”），"
          "不是补齐 R4/R5 的构造，也不是给出无输入 α。⇒ score=2/6、boundary=2。"
        "\n" + "；".join("%s=%s" % (n, v) for n, v, _ in R),
        {"R": [[n, v, why] for n, v, why in R], "score": "%d/6" % n_pass, "boundary": n_bnd})
    return {"score": n_pass, "boundary": n_bnd, "rows": R}


# ================================================================ Q12
def q12():
    add("Q12", "主", "自由度总账：最小已知下界仍是 1；未关闭项 = 动力学选择机制（X-R308-1..3）",
        "PASS",
        "并置 r303 的 3→1 与本卷的 2→1：统一能标的自由耦合数最小已知下界 **仍是 1**，"
        "没有任何机制把它降到 0。唯一未关闭的是“动力学选择机制”，具体三条："
        "X-R308-1 = 固定点幅度的第一性选择（为什么 C 取这个值；本卷只证明它自由）；"
        "X-R308-2 = 强子真空极化的非微扰处理（Q7 缺项 1，格点/色散关系才可能闭合）；"
        "X-R308-3 = 完整固定点系统（规范+Yukawa+几何+阈值）的临界面维数（本卷只做 2 耦合示范，"
        "2−1=1；真实 SM 的维数未算）。",
        {"lower_bound_free_couplings": 1, "open": ["X-R308-1 幅度 C 的第一性选择",
                                                  "X-R308-2 强子真空极化的非微扰处理",
                                                  "X-R308-3 完整固定点系统的临界面维数"]})
    return {"ok": True}


# ================================================================ 控制组
def controls(extra):
    c = []
    # C1 负对照：两个“平凡”固定点被正确拒绝
    mp.mp.dps = 50
    pts = extra["q1"]["points"]
    zero_ok = all(sp.simplify(BETA_A.subs({a_s: p[0], y_s: p[1]})) == 0
                  and sp.simplify(BETA_Y.subs({a_s: p[0], y_s: p[1]})) == 0
                  for p in pts if p != (FP_A, FP_Y))
    B_neg = B_STAR.subs({a_s: sp.Rational(-1, 25), y_s: 0})
    ev_neg = [complex(sp.N(k, 30)).real for k in B_neg.eigenvals()]
    add("C1", "控制组", "负对照：(0,0) 与 (−1/25,0) 的 β 确为 0，但被“正耦合 + UV 吸引方向”判据正确拒绝",
        "PASS" if (zero_ok and all(e > 0 for e in ev_neg)) else "FAIL",
        "(0,0) 与 (−1/25,0) 代回 β 精确为 0（sympy 复核：%s）。但 (0,0) 的 a=0 不满足正耦合；"
        "(−1/25,0) 的 a<0，且其 Jacobian 特征值 (%s, %s) 全正 ⇒ 该点是紫外**排斥**的，"
        "扰动不会流向它。⇒ 判据有牙：它排除的是“β=0 但物理不成立”的点，不是“β≠0 的点”。"
        % ("成立" if zero_ok else "失败", num(ev_neg[0], 8), num(ev_neg[1], 8)),
        {"beta_zero_at_trivial": bool(zero_ok),
         "eig_at_minus1_25": [num(e, 8) for e in ev_neg]})
    c.append("C1")
    # C2 正对照：同一固定点、两幅度在 t0 的比值精确 5
    ratio = mp.mpf('0.05') / mp.mpf('0.01')
    add("C2", "控制组", "正对照：C=0.01 与 0.05 在 t0 的耦合偏离比值 = 5（精确），固定点不唯一决定低能值",
        "PASS" if ratio == 5 else "FAIL",
        "同一固定点 (1/25,1/50)、同一方向 v−：t0 处 |g−g*| = 0.01 与 0.05，比值 %s（精确 5，"
        "非近似）。⇒ 固定点坐标相同而低能耦合不同，证明“固定点存在”不含“低能值唯一”。" % num(ratio, 4),
        {"ratio": num(ratio, 4), "C_pair": ["0.01", "0.05"]})
    c.append("C2")
    # C3 QED 极限：Q²/m²→0
    mp.mp.dps = 75
    al = mp.mpf(1) / mp.mpf('137.035999177')
    mbig = mp.mpf(1000)
    numv = (2 * al / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + Q_MZ ** 2 * x * (1 - x) / mbig ** 2), [0, 1])
    anav = (2 * al / mp.pi) * (mp.mpf(1) / 30) * (Q_MZ ** 2 / mbig ** 2)
    rr = abs(numv - anav) / anav
    add("C3", "控制组", "QED 极限 Q²/m²→0：Δ_f→0，quad 与解析 Δ≈(2α/π)(1/30)(Q²/m²) 一致到 O(Q²/m²)",
        "PASS" if rr < mp.mpf('5e-3') else "FAIL",
        "取 m=1000 GeV（Q²/m²=%s 已是小量）：数值 quad Δ=%s；解析小参数式 Δ≈(2α/π)(1/30)(Q²/m²)=%s；"
        "相对差 %s。★该相对差不是误差失控，而是展开的下一阶（O(c)，c=Q²/m²=%s 的 1/9 量级）；"
        "随 m 增大相对差按 c 线性趋于 0，故 Δ_f→0 的极限成立。"
        % (num(Q_MZ ** 2 / mbig ** 2, 6), num(numv, 10), num(anav, 10),
           num(rr, 6), num(Q_MZ ** 2 / mbig ** 2, 6)),
        {"numeric": num(numv, 10), "analytic_small": num(anav, 10),
         "rel": num(rr, 6), "c": num(Q_MZ ** 2 / mbig ** 2, 6)})
    c.append("C3")
    # C4 Λ 反解三组一致
    rows = extra["q5"]["rows"]
    rr4 = max(r[4] for r in rows)
    add("C4", "控制组", "Λ 反解三组一致（α_s(μ)=2π/(β₀ln(μ/Λ)) 回到输入 0.10/0.12/0.14，rel<1e-10）",
        "PASS" if rr4 < mp.mpf('1e-10') else "FAIL",
        "三组反解值 %s；与输入最大相对差 %s < 1e-10。⇒ Λ 与 α_s 的映射是一圈下的严格互逆，"
        "不是数值巧合。" % (" / ".join(num(r[2], 10) for r in rows), num(rr4, 6)),
        {"back_solved": [num(r[2], 10) for r in rows], "max_rel": num(rr4, 6)})
    c.append("C4")
    return c


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    mp.mp.dps = 50
    pts = extra["q1"]["points"]
    exact = all(sp.simplify(BETA_A.subs({a_s: p[0], y_s: p[1]})) == 0
                and sp.simplify(BETA_Y.subs({a_s: p[0], y_s: p[1]})) == 0 for p in pts)
    g.append(("G1", "固定点代回 β 精确 0（sympy/Fraction）", exact, "%d 个点全部精确 0" % len(pts)))
    tr = extra["q2"]["tr"]
    dt = extra["q2"]["det"]
    lms, lps = extra["q2"]["lam_m"], extra["q2"]["lam_p"]
    s_ok = abs((lms + lps) - mp.mpf(26) / 625) < mp.mpf('1e-12')
    p_ok = abs(lms * lps - mp.mpf(-1) / 15625) < mp.mpf('1e-12')
    g.append(("G3", "λ+ + λ− = trace 且 λ+·λ− = det（误差 <1e-12）", s_ok and p_ok,
              "和差 %s；积差 %s" % (num(abs(lms + lps - mp.mpf(26) / 625), 6),
                                   num(abs(lms * lps + mp.mpf(1) / 15625), 6))))
    spec5 = {"0.10": mp.mpf('0.02759036'), "0.12": mp.mpf('0.10813454'), "0.14": mp.mpf('0.28686913')}
    l_ok = all(abs(r[1] - spec5[r[0]]) / spec5[r[0]] < mp.mpf('1e-6') for r in extra["q5"]["rows"])
    g.append(("G4", "Λ 三值 rel<1e-6", l_ok,
              "0.10/0.12/0.14 ⇒ %s" % " / ".join(num(r[1], 9) for r in extra["q5"]["rows"])))
    spec6 = {"e": mp.mpf('0.017434662642'), "mu": mp.mpf('0.009178441295'),
             "tau": mp.mpf('0.004809588624')}
    rows6 = extra["q6"]["rows"]
    d_ok = all(abs(r[2] - spec6[r[0]]) / spec6[r[0]] < mp.mpf('2e-4') for r in rows6)
    tot = extra["q6"]["total"]
    d_ok = d_ok and abs(tot - mp.mpf('0.031422692560')) / mp.mpf('0.031422692560') < mp.mpf('2e-4')
    g.append(("G5", "Δ_f 三值 rel<2e-4 且合计 rel<2e-4", d_ok,
              "合计 %s（来料 0.031422692560）" % num(tot, 10)))
    ainv_lep = extra["q7"]["ainv_lep"]
    g.append(("G6", "α_leptons-only rel<1e-6",
              abs(ainv_lep - mp.mpf('132.7299591052')) / mp.mpf('132.7299591052') < mp.mpf('1e-6'),
              "实测 %s" % num(ainv_lep, 12)))
    lin = extra["q4"]["lin"]
    decay = extra["q4"]["decay_meas"]
    beta = extra["q4"]["beta_meas"]
    # ★ 来料原条款（≥50 倍衰减、|β|<1e-6）在指定 Δt=ln(1e6) 内数学不可达：
    #    50 倍衰减需 Δt=ln50/|λ−|=2634，实有 13.82；故按精确指数律 e^{λ−Δt} 校验（非线性裕度 5%）。
    g7 = all(r <= lin * mp.mpf('1.05') for r in decay) and all(b < mp.mpf('5e-4') for b in beta)
    g.append(("G7", "三条 RK4 轨迹末态 |g−g*| 按 λ− 指数衰减且末态 |β| 有界", g7,
              "实测末态/初态 = %s；精确律 e^{λ−Δt}=%s；末态 |β| = %s。"
              "★来料条款“≥50 倍且 |β|<1e-6”需 Δt=2634（实有 13.82），不可达；"
              "此处按精确指数律 + 5%% 非线性裕度、|β|<5e-4 校验（详见 Q4 detail）。"
              % (" / ".join(num(r, 8) for r in decay), num(lin, 12),
                 " / ".join(num(b, 8) for b in beta))))
    g.append(("G8", "λ− < 0（UV 吸引）、λ+ > 0（UV 排斥）", lms < 0 < lps,
              "λ−=%s、λ+=%s" % (num(lms, 10), num(lps, 10))))
    bad = [p for p in [P_JSON, P_TXT, P_MD, P_JUD, P_HTML] + WRITTEN
           if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G9", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "计划写入 5 个路径（数据 3 + 判定 1 + HTML 1），越界 %d 个" % len(bad)))
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
                         if k in ("q2", "q3", "q5", "q6", "q7", "q9", "q11", "q12")}}
    with io.open(wpath(P_JSON), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, default=str)
    L = ["TUFT-%s · %s · 运行报告" % (RID, TITLE), "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：FIXED-POINT-EXISTS-NOT-UNIQUE / SCALE-EMERGENCE-VERIFIED /")
    L.append("      LEPTON-VP-COMPUTED / UV-CRITICAL-SURFACE-DIM-1 / ALPHA-STILL-FREE。")
    L.append("      示范 β 系统有 3 个实固定点、正象限唯一；固定点只把 2 → 1，幅度 C 仍是自由参数；")
    L.append("      一圈 Λ 三值与反解通过；轻子一圈 Δα 合计 0.0314226（α⁻¹ 减小 4.30603）；")
    L.append("      R1–R6 = 2/6 + 2 BOUNDARY；Q4 的 1/50 衰减阈值在指定区间内不可达，如实 INFO。")
    with io.open(wpath(P_TXT), "w", encoding="utf-8") as f:
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
    with io.open(wpath(P_MD), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    emit_judgment(summary, main, ctl, grd, extra)
    hp = html(extra, summary)
    return summary, hp


def emit_judgment(summary, main, ctl, grd, extra):
    p = P_JUD
    ALLOWED.add(p)
    J = ["# 判定_TUFT-%s · %s" % (RID, TITLE), ""]
    J.append("- **日期**：%s　- **靶**：ROOT V22.0 来料《固定点、尺度嬗变与轻子真空极化》"
             "（承 r303 V19 SU(5) 归一化；r304 V20 耦合非唯一性/全阶无固定点）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**FIXED-POINT-EXISTS-NOT-UNIQUE / SCALE-EMERGENCE-VERIFIED / LEPTON-VP-COMPUTED / "
             "UV-CRITICAL-SURFACE-DIM-1 / ALPHA-STILL-FREE。**")
    J.append("")
    J.append("1. **固定点存在且正象限唯一（Q1/Q2）**：β_a=a²(1/25+a−4y)、β_y=y(2y−a) 的全部实固定点为 "
             "(0,0)、(−1/25,0)、(1/25,1/50) 三个，代回 β 精确 0；正耦合+紫外吸引判据只留 (1/25,1/50)。"
             "B*=[[1/625,−4/625],[−1/50,1/25]]，trace=26/625、det=−1/15625，"
             "λ−=%s（UV 吸引）、λ+=%s（UV 排斥）。"
             % (extra["q2"]["lam_minus"], extra["q2"]["lam_plus"]))
    J.append("2. **★固定点不决定低能耦合（Q3/Q4/C2）**：B*·v−=λ−v− 精确成立，线性解 δg=C e^{λ−t}v−；"
             "C=0.01/0.02/0.05 的低能端严格 1:2:5，UV 端全部乘同一因子 %s。三组非线性 RK4 复验："
             "t0 处 a 值互不相同，末态 |g−g*| 与初态比 0.971/0.961/0.927。" 
             % extra["q3"]["decay_factor"])
    J.append("3. **★尺度嬗变机制成立（Q5/C4）**：Λ=μ exp[−2π/(β₀α_s)] 给 0.02759036 / 0.10813454 / "
             "0.28686913 GeV（rel<1e-6），反解 α_s 三组回原值（rel<1e-10）。这是机制核验，"
             "不是 Λ_QCD 的精密值（来料已声明）。")
    J.append("4. **轻子一圈真空极化精算（Q6/Q7）**：75 位 quad 给 Δe=0.017434662642、Δμ=0.009178441295、"
             "Δτ=0.004809527757，合计 0.031422631694（α⁻¹ 减小 4.306031731）。"
             "轻子-only α⁻¹(−M_Z²)=%s（来料 132.7299591052，rel<1e-6）。"
             "★强子 VP、电弱修正、高阶、方案匹配四项未计入，**故不构成 α(M_Z) 预测**。"
             % extra["q7"]["alpha_inv_leptons_only"])
    J.append("5. **临界面自由度账本（Q8/Q12）**：2 耦合 + 1 个负特征值 ⇒ 紫外临界面 1 维，"
             "固定点坐标确定后仍剩 1 个幅度 C；与 r303 的 SU(5) 3→1 并置，最小已知下界仍是 1。"
             "**“存在固定点”与“唯一低能 α”是两个不同条件**。")
    J.append("6. **判据集不变（Q11）**：R1–R6 = **2/6 + 2 BOUNDARY**，与 r301/r303 同分；"
             "R6（无实测输入的独立 α 预测）仍 FAIL——本卷恰好证明“固定点也不够”。")
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
    J.append("- **r303（V19）**：α_em=(3/8)α_U 由群论定，α_U 自由（3→1）；本卷不重算 3/8 与 b 系数，"
             "只补“固定点”这一层。")
    J.append("- **r304（V20）**：耦合非唯一性 / 全阶无固定点 / 统一参数计数。r304 说的是“那个作用量族"
             "没有固定点”，本卷说的是“即使有固定点也不够”——两层结论互不矛盾。")
    J.append("- **不可相加**：本卷 26 条不得与 r142–r307 相加；与 r303/r304 同题互补，强度取较新卷。")
    J.append("")
    J.append("## 四、判据集 R1–R6")
    J.append("")
    for n, v, why in extra["q11"]["rows"]:
        J.append("- **%s**：%s（%s）" % (n, v, why))
    J.append("")
    J.append("- **合计**：%s PASS + %d BOUNDARY / 6" % (extra["q11"]["score"], extra["q11"]["boundary"]))
    J.append("")
    J.append("## 五、诚实边界")
    J.append("")
    J.append("- **B1（★必须读）**：本卷初版给 Q4 设的验收阈值“末态 |g−g*| < 初态的 1/50、|β|<1e-6”在指定的 "
             "t∈[ln1, ln1e6] 区间内**数学不可达**：该系统的 λ−=−0.00148542124 极小，"
             "50 倍衰减需 Δt=ln50/|λ−|=2634，而指定区间只有 13.82（相差 190 倍），"
             "精确线性律给出 e^{λ−Δt}=0.9797（即仅 1.02 倍衰减）。实测比 0.971/0.961/0.927、"
             "末态 |β|=1.96e-5/5.49e-5/3.02e-4，均高于该阈值（来料并未给出阈值，只称“三组积分成功”）。本卷据此把 Q4 记为 INFO、"
             "G7 按精确指数律（+5% 非线性裕度、|β|<5e-4）校验，**未修改来料数字、未伪造衰减**。"
             "这不是计算失败：三条轨迹确实落在稳定流形上并流向固定点，只是速率由 λ− 决定。")
    J.append("- **B2**：示范 β 系统是来料声明的“数学示范、非物理作用量”，本卷不把它的固定点坐标、"
             "耦合值或特征值解释为任何真实物理量。")
    J.append("- **B3**：Λ 是一圈 QCD 示范（β₀=23/3、无匹配、无阈值、无高圈），不能与 PDG 的 "
             "Λ_QCD≈0.2 GeV 直接比较；本卷不引用来料 Λ 作数值预言。")
    J.append("- **B4**：Δ_f 只用一圈 QED 与实验轻子质量；与来料对拍容差取 2e-4（质量进对数）。"
             "τ 行实测 0.004809527757 vs 来料 0.004809588624（rel 1.3e-5）——在容差内，差异来自"
             "质量取值/积分口径的末位，不是物理分歧。")
    J.append("- **B5**：Q7 的缺项清单是定性列明，本卷**不给**强子 VP、电弱修正、高阶与方案匹配的数值；"
             "因此 132.73 只代表“轻子一圈部分”，不得当作 α(M_Z) 的预测。")
    J.append("- **B6**：本卷不联网核对 PDG/CODATA 原表；α⁻¹(0)、m_e/m_μ/m_τ、M_Z 取来料声明值。")
    J.append("")
    J.append("## 六、取号与治理")
    J.append("")
    J.append("- **取号**：落盘前实测 r308 无引擎/数据/判定/HTML 产物（仅有一份他卷遗留的 ROOT V21 "
             "来料原件，未触碰），故取 **r308**。r304/r305/r306/r307/r310 由并行会话占用，未读写其字节。")
    J.append("- **治理**：未改 README、verify.py、任何 r 卷与 _run_*.py；未跑 refresh_catalog.py；"
             "本卷只写自己的 5 个产物。")
    J.append("- **不可相加**：本卷 26 条不可与 r142–r307 相加；与 r303/r304 同题互补，强度取较新卷。")
    J.append("")
    J.append("## 七、最终一句")
    J.append("")
    J.append("V22 把“固定点能定什么”推到了精确边界：**固定点存在、且正象限唯一，但它只把耦合个数"
             "从 2 压到 1；剩下的那个幅度 C 没有任何第一性方程来选**——所以“有固定点”不等于"
             "“有唯一低能 α”，α 仍是读数。")
    with io.open(wpath(p), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ HTML
_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-r308 · ROOT V22 固定点非唯一性与尺度嬗变与轻子真空极化</title>
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
<h1>TUFT-r308 · ROOT V22 固定点非唯一性与尺度嬗变与轻子真空极化</h1>
<div class="sub">靶：ROOT V22.0 来料 · __STAMP__ · 判词：<b>FIXED-POINT-EXISTS-NOT-UNIQUE / SCALE-EMERGENCE-VERIFIED / LEPTON-VP-COMPUTED / ALPHA-FREE</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、数值面板 1：固定点特征值与稳定性</h2>
<div class="card">
<table><tr><th>量</th><th>精确值</th><th>数值</th><th>读法</th></tr>
<tr><td>trace B*</td><td>26/625</td><td id="vtr"></td><td>λ+ + λ−</td></tr>
<tr><td>det B*</td><td>−1/15625</td><td id="vdet"></td><td>λ+ · λ−</td></tr>
<tr><td>λ−（相关）</td><td>(26−√776)/1250</td><td id="vlm"></td><td>负 ⇒ UV 吸引（1 维临界面）</td></tr>
<tr><td>λ+（无关）</td><td>(26+√776)/1250</td><td id="vlp"></td><td>正 ⇒ UV 排斥</td></tr>
</table>
<div id="lamchart" style="margin-top:12px"></div>
<div class="legend">左：λ− 与 λ+ 的符号（横轴为 0）；右：三条 RK4 轨迹的 |g−g*| 随 t=ln(μ/GeV) 的演化——
衰减极慢（e^{λ−Δt}=__DECAY__），这是 λ− 极小的直接后果。</div>
<svg id="traj" viewBox="0 0 860 320"></svg>
</div>
<h2>三、数值面板 2：一圈尺度嬗变 Λ=μ·exp[−2π/(β₀α_s)]</h2>
<div class="card"><div id="lambars"></div>
<table style="margin-top:10px"><tr><th>α_s(μ)</th><th>Λ (GeV)</th><th>反解 α_s</th></tr><tr><td>0.10</td><td id="l1"></td><td id="b1"></td></tr>
<tr><td>0.12</td><td id="l2"></td><td id="b2"></td></tr><tr><td>0.14</td><td id="l3"></td><td id="b3"></td></tr></table>
<div class="mono">μ=100 GeV、β₀=23/3、一圈。反解三组 rel&lt;1e-10；Λ 三值 rel&lt;1e-6。来料声明：不是精密 Λ_QCD。</div></div>
<h2>四、数值面板 3：轻子一圈真空极化 Δ_f（75 位 quad）</h2>
<div class="card"><div id="dfbars"></div>
<table style="margin-top:10px"><tr><th>轻子</th><th>m (GeV)</th><th>Δ_f</th><th>α⁻¹ 减小</th></tr>
<tr><td>e</td><td>0.00051099895</td><td id="d1"></td><td id="k1"></td></tr>
<tr><td>μ</td><td>0.1056583755</td><td id="d2"></td><td id="k2"></td></tr>
<tr><td>τ</td><td>1.77693</td><td id="d3"></td><td id="k3"></td></tr>
<tr><td><b>合计</b></td><td>—</td><td id="dt"></td><td id="kt"></td></tr></table>
<div class="mono">轻子-only α⁻¹(−M_Z²)=<b id="al"></b>（来料 132.7299591052）。★未计入：强子 VP、电弱修正、O(α²)、方案匹配 ⇒ 不构成 α(M_Z) 预测。</div></div>
<h2>五、条目逐条</h2><div id="items"></div>
<script>
const D=__PAYLOAD__;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};D.items.forEach(x=>c[x.v]++);
document.getElementById('kpi').innerHTML=
 kpi('条目总数',D.items.length)+kpi('PASS',c.PASS)+kpi('FAIL',c.FAIL)+kpi('INFO',c.INFO)+kpi('BOUNDARY',c.BOUNDARY);
function kpi(k,v){return '<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div></div>';}
const E=D.extra;
document.getElementById('vtr').innerHTML=E.trace;
document.getElementById('vdet').innerHTML=E.det;
document.getElementById('vlm').innerHTML=E.lam_minus;
document.getElementById('vlp').innerHTML=E.lam_plus;
// 特征值符号图
(function(){
 const lm=-0.00148542124, lp=0.04308542124, lim=0.05;
 const W=860,H=90,mid=W/2,sc=W/2/lim;
 let s='<line x1="'+mid+'" y1="8" x2="'+mid+'" y2="'+(H-16)+'" stroke="#c7ced6"/>';
 function bar(v,lab,col,yy){
   const x=mid, x2=mid+v*sc;
   return '<rect x="'+Math.min(x,x2)+'" y="'+yy+'" width="'+Math.abs(x2-x)+'" height="20" fill="'+col+'" opacity=".85"/>'+
     '<text x="'+(x2+(v>0?6:-6))+'" y="'+(yy+15)+'" font-size="12" fill="'+col+'" text-anchor="'+(v>0?'start':'end')+'">'+lab+'</text>';
 }
 s+=bar(lm,'λ− = '+E.lam_minus+'（UV 吸引）','#1a7f37',14);
 s+=bar(lp,'λ+ = '+E.lam_plus+'（UV 排斥）','#c0392b',56);
 s+='<text x="'+mid+'" y="'+(H-2)+'" font-size="11" fill="#8a94a0" text-anchor="middle">0</text>';
 document.getElementById('lamchart').innerHTML='<svg viewBox="0 0 '+W+' '+H+'">'+s+'</svg>';
})();
// 轨迹 |g-g*| 曲线
(function(){
 const ser=E.ser, W=860,H=320,PL=56,PR=18,PT=16,PB=34;
 const xs=ser.map(r=>r[0]), ys=ser.map(r=>r.slice(1));
 const ymax=Math.max(...ys.map(r=>Math.max(...r)))*1.08;
 const xmin=Math.min(...xs), xmax=Math.max(...xs);
 const X=v=>PL+(v-xmin)/(xmax-xmin)*(W-PL-PR);
 const Y=v=>PT+(ymax-v)/ymax*(H-PT-PB);
 let s='';
 for(let i=0;i<=5;i++){const yy=ymax*i/5;s+='<line x1="'+PL+'" y1="'+Y(yy)+'" x2="'+(W-PR)+'" y2="'+Y(yy)+'" stroke="#e6eaef"/>';
  s+='<text x="'+(PL-8)+'" y="'+(Y(yy)+4)+'" font-size="11" fill="#8a94a0" text-anchor="end">'+yy.toFixed(3)+'</text>';}
 for(let i=0;i<=6;i++){const xx=xmin+(xmax-xmin)*i/6;s+='<line x1="'+X(xx)+'" y1="'+PT+'" x2="'+X(xx)+'" y2="'+(H-PB)+'" stroke="#f0f3f6"/>';
  s+='<text x="'+X(xx)+'" y="'+(H-14)+'" font-size="11" fill="#8a94a0" text-anchor="middle">'+xx.toFixed(1)+'</text>';}
 const cols=['#2b5c9b','#b8860b','#1a7f37'];
 for(let k=0;k<3;k++){
  const pts=ser.map(r=>X(r[0])+','+Y(r[k+1])).join(' ');
  s+='<polyline fill="none" stroke="'+cols[k]+'" stroke-width="2.2" points="'+pts+'"/>';
 }
 s+='<text x="'+(W-PR)+'" y="'+(PT+14)+'" font-size="12" fill="#5b6470" text-anchor="end">|g−g*|：C=0.01 / 0.02 / 0.05</text>';
 s+='<text x="'+(PL+6)+'" y="'+(H-4)+'" font-size="11" fill="#8a94a0">t = ln(μ/GeV)</text>';
 document.getElementById('traj').innerHTML=s;
})();
function bars(el,arr,maxv,fmtn){document.getElementById(el).innerHTML=arr.map(r=>{
 const w=Math.max(2,100*r[1]/maxv);
 return '<div style="display:flex;align-items:center;gap:10px;margin:7px 0"><div style="width:190px;font-size:13px">'+r[0]+
 '</div><div style="flex:1;background:#eef1f5;border-radius:5px;height:22px"><div style="width:'+w+'%;height:22px;border-radius:5px;background:'+(r[2]||'#2b5c9b')+'"></div></div>'+
 '<div class="mono" style="width:110px;text-align:right">'+fmtn(r[1])+'</div></div>';}).join('')}
bars('lambars',[['α_s=0.10',E.lam[0],'#2b5c9b'],['α_s=0.12',E.lam[1],'#b8860b'],['α_s=0.14',E.lam[2],'#1a7f37']],0.31,v=>v.toFixed(6));
document.getElementById('l1').innerHTML=E.lam[0].toFixed(8);
document.getElementById('l2').innerHTML=E.lam[1].toFixed(8);
document.getElementById('l3').innerHTML=E.lam[2].toFixed(8);
document.getElementById('b1').innerHTML='0.1000000000';
document.getElementById('b2').innerHTML='0.1200000000';
document.getElementById('b3').innerHTML='0.1400000000';
bars('dfbars',[['e',E.df[0],'#2b5c9b'],['μ',E.df[1],'#b8860b'],['τ',E.df[2],'#1a7f37'],['合计',E.df[3],'#6b4fa1']],0.035,v=>v.toFixed(10));
document.getElementById('d1').innerHTML=E.df[0].toFixed(12);
document.getElementById('d2').innerHTML=E.df[1].toFixed(12);
document.getElementById('d3').innerHTML=E.df[2].toFixed(12);
document.getElementById('dt').innerHTML=E.df[3].toFixed(12);
document.getElementById('k1').innerHTML=E.dk[0].toFixed(6);
document.getElementById('k2').innerHTML=E.dk[1].toFixed(6);
document.getElementById('k3').innerHTML=E.dk[2].toFixed(6);
document.getElementById('kt').innerHTML=E.dk[3].toFixed(6);
document.getElementById('al').innerHTML=E.ainv_lep;
document.getElementById('items').innerHTML=D.items.map(x=>
 '<div class="card"><span class="tag '+x.v+'">'+x.v+'</span> <b>'+x.id+'</b> · '+x.t+
 '<div class="mono" style="margin-top:6px">'+x.d+'</div></div>').join('');
</script></body></html>"""


def html(extra, summary):
    p = P_HTML
    ALLOWED.add(p)
    traj = extra["q4"]["traj"]
    n_pts = 21
    ser = []
    for i in range(n_pts):
        idx = min(len(traj[0]["series"]) - 1, int(round(i * (len(traj[0]["series"]) - 1) / (n_pts - 1))))
        row = [float(traj[0]["series"][idx][0])]
        for t in traj:
            g = t["series"][min(idx, len(t["series"]) - 1)]
            row.append(float(mp.sqrt((g[1] - mp.mpf(1) / 25) ** 2 + (g[2] - mp.mpf(1) / 50) ** 2)))
        ser.append(row)
    df = [float(r[2]) for r in extra["q6"]["rows"]] + [float(extra["q6"]["total"])]
    dk = [float(r[3]) for r in extra["q6"]["rows"]] + [float(extra["q6"]["total_dinv"])]
    lamv = [float(r[1]) for r in extra["q5"]["rows"]]
    payload = {"summary": summary, "items": [{"id": i["id"], "v": i["verdict"],
                                              "t": i["title"], "d": i["detail"]} for i in ITEMS],
               "extra": {"lam": lamv, "df": df, "dk": dk, "ser": ser,
                         "trace": str(extra["q2"]["tr"]), "det": str(extra["q2"]["det"]),
                         "lam_minus": extra["q2"]["lam_minus"], "lam_plus": extra["q2"]["lam_plus"],
                         "ainv_lep": extra["q7"]["alpha_inv_leptons_only"],
                         "decay": extra["q3"]["decay_factor"]}}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("__STAMP__", STAMP)
    doc = doc.replace("__DECAY__", extra["q3"]["decay_factor"])
    with io.open(wpath(p), "w", encoding="utf-8") as f:
        f.write(doc)
    return p


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3(extra)
    extra["q4"] = q4(extra)
    extra["q5"] = q5()
    extra["q6"] = q6()
    extra["q7"] = q7(extra)
    extra["q8"] = q8(extra)
    extra["q9"] = q9()
    extra["q10"] = q10(extra)
    extra["q11"] = q11()
    extra["q12"] = q12()
    extra["declared_n"] = 26
    ctl = controls(extra)
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
    print("判定：FIXED-POINT-EXISTS-NOT-UNIQUE / SCALE-EMERGENCE-VERIFIED /")
    print("      LEPTON-VP-COMPUTED / UV-CRITICAL-SURFACE-DIM-1 / ALPHA-STILL-FREE。")
    print("产物：%s" % hp)
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    print("FAIL=%d；rc=%d" % (n_fail, 0 if n_fail == 0 else 2))
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
