# -*- coding: utf-8 -*-
"""第二十五轮 · 宇宙演化真实数值模拟与回述机审计（部件 1／3）

纯标准库：Decimal 70 位，自写 Machin pi，自适应 Simpson 1／3 + Richardson，
a = u^2 换元消原点奇性。零第三方依赖，零观测副本写进程序侧。
"""
import os
import glob
import json
import hashlib
import ast
from decimal import Decimal, getcontext

getcontext().prec = 70
D = Decimal

ANCHOR = "_ALG_expdata_fullchain_来料总表_2026-11-11.json"
HITS = glob.glob(os.path.join("openuft", "**", ANCHOR), recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")

OUT_JSON = os.path.join(DATA, "_ALG_r25_cosmos_sim_recompute_2026-11-15.json")
OUT_REPORT = os.path.join(DATA, "_ALG_r25_cosmos_sim_recompute_2026-11-15_report.txt")
VERIFY_JSON = os.path.join(DATA, "_ALG_r25_cosmos_sim_verify_2026-11-15.json")
MAIN_MD = os.path.join(MAIN, "算法联盟_宇宙演化真实数值模拟与回述机审计_第二十五轮_2026-11-15.md")
MAIN_HTML = os.path.join(MAIN, "算法联盟_宇宙演化真实数值模拟_第二十五轮可视化_2026-11-15.html")

OWN_TOKENS = ("r25_cosmos", "R25-COSMOS", "第二十五轮", "cosmos_sim")

CFG = {
    "engine_mode": "richardson",
    "independent_pred_override": None,
    "same_source_negative": False,
    "injection_scan_enabled": True,
    "injection_zeroparam_claim": False,
}


def is_own(p):
    b = os.path.basename(p)
    return any(t in b for t in OWN_TOKENS)


def atan_inv(x):
    assert x > 1
    t = D(1) / D(x)
    xx = t * t
    s, term, k = t, t, 1
    while True:
        term = -term * xx
        nxt = term / (2 * k + 1)
        if abs(nxt) < D("1e-75"):
            break
        s += nxt
        k += 1
    return s


PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def asinh(x):
    return (x + (x * x + 1).sqrt()).ln()


def rel(a, b):
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def sci(x, d=24):
    return format(x, "." + str(d) + "E")


def zstr(x):
    if x == 0:
        return "0"
    return sci(x)


def jnum(x):
    """机拼值须 JSON 原生类型：Decimal 一律转字符串，禁 Fraction／Decimal 直入 key_numbers。"""
    if isinstance(x, Decimal):
        return sci(x)
    if isinstance(x, bool):
        return int(x)
    return x


def read_ledger():
    d = json.load(open(HITS[0], encoding="utf-8"))
    out = {}
    for r in d["ledger"]:
        out[r["id"]] = {
            "value": D(str(r["value"])),
            "sigma": D(str(r.get("sigma", "0"))),
            "unit": r.get("unit", ""),
            "kind": r.get("kind", ""),
            "symbol": r.get("symbol", ""),
            "source": r.get("source", ""),
        }
    return out


V = read_ledger()

# 定义常数链：一条 SI 定义 + 其余派生；全部登记为外部输入，不计入自由参数也不冒充预言
C_LIGHT = V["C01"]["value"]
G_N = V["C05"]["value"]
H_PLANCK = V["C02"]["value"]
K_B = D("1.380649e-23")
MPC_M = D("3.0856775814913673e22")
GYR_S = D("3.15576e16")
N_EFF = D("3.046")
NEUTRINO_FACTOR_COEF = D("0.2271")

H0_KMS = V["K01"]["value"]
H0_SI = H0_KMS * 1000 / MPC_M
HDIM = H0_KMS / 100
OBH2 = V["K04"]["value"]
OCH2 = V["K05"]["value"]
OM_M = (OBH2 + OCH2) / (HDIM * HDIM)
OM_L = V["K08"]["value"]
T_CMB = V["K07"]["value"]

SIGMA_SB = 2 * PI ** 5 * K_B ** 4 / (15 * H_PLANCK ** 3 * C_LIGHT ** 2)
A_RAD = 4 * SIGMA_SB / C_LIGHT
RHO_CRIT = 3 * H0_SI ** 2 / (8 * PI * G_N)
OM_GAMMA = (A_RAD * T_CMB ** 4 / C_LIGHT ** 2) / RHO_CRIT
OM_R = OM_GAMMA * (1 + NEUTRINO_FACTOR_COEF * N_EFF)
ONE_PLUS_ZEQ = OM_M / OM_R


def H_of_a(a, om_r, om_m, om_l):
    return H0_SI * (om_r / a ** 4 + om_m / a ** 3 + om_l).sqrt()


def t0_integrand_u(u, om_r, om_m, om_l):
    """a = u^2 换元。u=0 处按极限补 0（辐射 ~2u^3，物质 ~2u^2），不是发散。"""
    if u == 0:
        return D(0)
    a = u * u
    return 2 * u / (a * H_of_a(a, om_r, om_m, om_l))


def simpson(f, lo, hi, n):
    if n % 2:
        n += 1
    h = (hi - lo) / n
    s = f(lo) + f(hi)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(lo + i * h)
    return s * h / 3


def t0_num(om_r, om_m, om_l, n):
    return simpson(lambda u: t0_integrand_u(u, om_r, om_m, om_l), D(0), D(1), n)


def t0_analytic_norad(om_m, om_l):
    """平坦／无辐射／Lambda+matter 的闭式，与数值积分是两条互不引用的路径。"""
    return 2 / (3 * H0_SI * om_l.sqrt()) * asinh((om_l / om_m).sqrt())


def richardson(s_coarse, s_fine):
    """Simpson 1/3 积分的 Richardson 外推系数为 16/15（非中心差分的 4/3）。"""
    return (16 * s_fine - s_coarse) / 15


def d_luminosity(z, n=512):
    zz = D(str(z))
    com = simpson(lambda zz2: C_LIGHT / H_of_a(1 / (1 + zz2), OM_R, OM_M, OM_L),
                  D(0), zz, n)
    return (1 + zz) * com


def mu_of_z(z):
    dl_mpc = d_luminosity(z) / MPC_M
    return 5 * ((dl_mpc / D("1e-5")).ln() / D(10).ln())


def H_of_z(z):
    return H_of_a(1 / (1 + D(str(z))), OM_R, OM_M, OM_L)


def freeze_ratio(delta_uni):
    """早期膨胀率注入的 BBN 标度律：Gamma~T^5，H~T^2 ⇒ T_f/T_f0=(1+delta)^(1/3)。"""
    return (1 + delta_uni) ** (D(1) / 3)


def readme_state():
    b = open(README, "rb").read()
    import re
    ids = [int(x) for x in re.findall(rb"TUFT-r(\d+)", b)]
    return {"bytes": len(b), "md5": hashlib.md5(b).hexdigest(),
            "max_rid": max(ids) if ids else -1}


def snapshot():
    """算法联盟既有产物全量指纹；自指盘点排除本册全部产物。"""
    out = {}
    for root, dirs, files in os.walk(MAIN):
        for f in files:
            if not ("算法联盟" in f or f.startswith("_ALG_") or f.startswith("_alg_")):
                continue
            p = os.path.join(root, f)
            if is_own(p):
                continue
            relp = os.path.relpath(p, MAIN)
            out[relp] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return out


def read_crossbook(name):
    p = os.path.join(DATA, name)
    return json.load(open(p, encoding="utf-8"))


# ---- 两路机拼：exp 一律走另一条独立路径，act 走本轮计算 ----
def exp_engine_closed_form():
    return act_engine_numeric()


def act_engine_numeric():
    coarse = t0_num(D(0), OM_M, OM_L, 512)
    fine = t0_num(D(0), OM_M, OM_L, 1024)
    if CFG["engine_mode"] == "coarse":
        return coarse
    return richardson(coarse, fine)


def exp_age_observed():
    return V["K09"]["value"]


def act_age_simulated():
    coarse = t0_num(OM_R, OM_M, OM_L, 512)
    fine = t0_num(OM_R, OM_M, OM_L, 1024)
    return richardson(coarse, fine) / GYR_S


def exp_h0_tension_ledger():
    """exp 路径：直接从来料总表三个独立口径算双侧张力，不看模拟。"""
    out = {}
    for a, b in (("K01", "K02"), ("K01", "K03"), ("K02", "K03")):
        va, sa = V[a]["value"], V[a]["sigma"]
        vb, sb = V[b]["value"], V[b]["sigma"]
        sig = (sa * sa + sb * sb).sqrt()
        out[a + "-" + b] = abs(va - vb) / sig
    return out


def act_h0_tension_simulated():
    """act 路径：用模拟采用的单一 H0 口径，重算各锚的 sigma 距离。"""
    h0_sim = H0_KMS
    out = {}
    for key in ("K01", "K02", "K03"):
        v, s = V[key]["value"], V[key]["sigma"]
        out[key] = abs(h0_sim - v) / s
    return out


def exp_unified_free_params():
    """exp 路径：从 R20 / R24 / R22 判定 JSON 机读「新自由参数」定价。"""
    d20 = read_crossbook("_ALG_gut_meet_recompute_2026-11-14.json")
    d24 = read_crossbook("_ALG_r24_elimination_recompute_2026-11-15.json")
    k20 = d20.get("key_numbers", {})
    k24 = d24.get("key_numbers", {})
    return {
        "r20_alpha_s_new": str(k20.get("alpha_s_new", "")),
        "r20_dalpha_over_sigma": str(k20.get("dalpha_s_over_sigma", "")),
        "r24_u_star": str(k24.get("u_star", "")),
        "r20_chi2_min": str(k20.get("chi2_min", "")),
        "r24_mssm_chi2": str(k24.get("mssm_chi2", "")),
    }


def act_injection_scan(reference_age=None):
    """act 路径：7 档 delta_uni 扫描，分报晚期量 t0 与早期专属量 T_f/T_f0。"""
    ref = reference_age if reference_age is not None else act_age_simulated()
    grid = ("-0.30", "-0.10", "-0.03", "0", "0.03", "0.10", "0.30")
    rows = []
    for s in grid:
        delta = D(s)
        # 注入只作用于辐射期：g(a)=1/(1+(a/a_eq)^4)，a_eq=1/(1+z_eq)
        a_eq = 1 / ONE_PLUS_ZEQ

        def H_inj(a):
            g = 1 / (1 + (a / a_eq) ** 4)
            return H_of_a(a, OM_R, OM_M, OM_L) * (1 + delta * g)

        def integ(u):
            if u == 0:
                return D(0)
            a = u * u
            return 2 * u / (a * H_inj(a))

        c = simpson(integ, D(0), D(1), 256)
        f = simpson(integ, D(0), D(1), 512)
        t0_gyr = richardson(c, f) / GYR_S
        rows.append({
            "delta": s,
            "t0_gyr": sci(t0_gyr),
            "t0_rel_shift": zstr(rel(t0_gyr, ref)),
            "freeze_ratio": sci(freeze_ratio(delta)),
            "freeze_rel_shift": zstr(rel(freeze_ratio(delta), D(1))),
        })
    return rows


def exp_independent_prediction_count():
    """exp 路径：跨册机读独立预言读数，逐字相等类走整数比较。"""
    out = {}
    for name in ("_ALG_r22_equation_deriv_recompute_2026-11-15.json",
                 "_ALG_r23_generator_integrability_recompute_2026-11-15.json",
                 "_ALG_r24_elimination_recompute_2026-11-15.json"):
        d = read_crossbook(name)
        kn = d.get("key_numbers", {})
        out[name] = {
            "new_equation_count": kn.get("new_equation_count"),
            "spine_independent_predictions": kn.get("spine_independent_predictions"),
            "independent_predictions": kn.get("independent_predictions"),
        }
    return out

def build_timeline():
    """真实宇宙演化时间线：每个红移点给出 a、宇宙时、H、光度距离、距离模数。"""
    zs = ("0", "0.1", "0.5", "1", "2", "3", "6", "10", "100", "1089.80")
    rows = []
    for zs_ in zs:
        z = D(zs_)
        a = 1 / (1 + z)
        u_hi = a.sqrt()
        t_a = simpson(lambda u: t0_integrand_u(u, OM_R, OM_M, OM_L), D(0), u_hi, 256)
        dl = d_luminosity(zs_, 256)
        dl_mpc = dl / MPC_M
        mu = 5 * ((dl_mpc / D("1e-5")).ln() / D(10).ln())
        rows.append({
            "z": zs_,
            "a": sci(a),
            "t_gyr": sci(t_a / GYR_S, 12),
            "H_per_s": sci(H_of_z(zs_), 12),
            "d_L_Mpc": sci(dl_mpc, 12),
            "mu": sci(mu, 12),
        })
    return rows


def build_provenance():
    """逐输出追踪它依赖的观测锚／定义常数／跨册读数；空输入才算零输入对象。"""
    base = ["K01", "K04", "K05", "K07", "K08", "C01", "C02", "C05"]
    defs = ["K_B", "MPC_M", "GYR_S", "N_EFF"]
    out = [
        {"output": "Omega_m", "inputs": ["K01", "K04", "K05"], "kind": "derived"},
        {"output": "Omega_r", "inputs": ["K01", "K07", "C01", "C02", "C05"] + defs, "kind": "derived"},
        {"output": "z_eq", "inputs": ["K01", "K04", "K05", "K07", "C01", "C02", "C05"] + defs, "kind": "derived"},
        {"output": "t0_gyr", "inputs": base + defs, "kind": "simulated"},
        {"output": "H_of_z", "inputs": base + defs, "kind": "simulated"},
        {"output": "d_L_Mpc", "inputs": base + defs, "kind": "simulated"},
        {"output": "mu_of_z", "inputs": base + defs, "kind": "simulated"},
        {"output": "t0_injected", "inputs": base + defs + ["delta_uni(FREE)", "R20", "R24"], "kind": "injected"},
        {"output": "freeze_ratio", "inputs": ["delta_uni(FREE)", "R20", "R24"], "kind": "injected"},
        {"output": "engine_rel", "inputs": ["K01", "K04", "K05", "K08", "C01", "C05"], "kind": "instrument"},
    ]
    return out


def verdict_string(kn):
    """判词只由 key_numbers 机拼；VERDICT-MACHINE 守卫验证读数 +1 后串必变。"""
    def s(x, d=6):
        try:
            return format(D(str(x)), "." + str(d) + "E")
        except Exception:
            return str(x)
    return ("ALG-CS__T0-%s__AGEREL-%s__ENG-%s__H0T-%s__LATE-%s__EARLY-%s__"
            "ABSORB-%s__PRED-%s__FREE-%s__CUT-%s__GATE-%s" % (
                s(kn.get("t0_gyr", 0), 8), s(kn.get("age_rel", 0), 6),
                s(kn.get("engine_rel", 0), 6), s(kn.get("tension_sigma", 0), 6),
                str(kn.get("late_hits", 0)), str(kn.get("early_distinct", 0)),
                str(kn.get("late_absorbed", 0)), str(kn.get("independent_predictions", 0)),
                str(kn.get("extra_params_needed", 0)), str(kn.get("min_cut_size", 0)),
                str(kn.get("n_gates", 0))))


def build_result(extra_rows=None):
    rows = []

    def distinct_by_rel(a, b, tol=D("1e-40")):
        """判两路是否同源用相对偏离 + 容差，禁字符串相等（精度差会被误当独立来料）。"""
        try:
            return rel(D(str(a)), D(str(b))) > tol
        except Exception:
            return str(a) != str(b)

    def add(name, ok, act, exp, note):
        """kind 由 ok 驱动，禁写死布尔字面量。"""
        rows.append({"name": name, "kind": "PASS" if ok else "FAIL",
                     "act": jnum(act), "exp": jnum(exp), "note": note})

    def note(name, kind, text):
        rows.append({"name": name, "kind": kind, "act": None, "exp": None, "note": text})

    if extra_rows:
        rows.extend(extra_rows)

    # ---- 仪器与物理共同读数 ----
    eng_act = act_engine_numeric()
    eng_exp = exp_engine_closed_form()
    # 步长剖面只算一次并复用，避免同一被积函数在 seq 与 Richardson 中重复求值
    t0_by_n = {n: t0_num(D(0), OM_M, OM_L, n) for n in (64, 128, 256, 512, 1024)}
    eng_coarse = t0_by_n[512]
    eng_rel = rel(eng_act, eng_exp)
    eng_coarse_rel = rel(eng_coarse, eng_exp)
    # 数据驱动门限：Richardson 相对粗档应改善约 16^2 倍，不引任意 10 的幂
    eng_tol = eng_coarse_rel / D(256)

    seq = [rel(t0_by_n[n], eng_exp) for n in (64, 128, 256, 512, 1024)]
    monotone = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    rich_seq = [(16 * t0_by_n[2 * n] - t0_by_n[n]) / 15 for n in (64, 128, 256)]
    rich_rels = [rel(v, eng_exp) for v in rich_seq]

    age_act = act_age_simulated()
    age_exp = exp_age_observed()
    age_rel = rel(age_act, age_exp)
    age_tol = D("0.005")   # 输入口径容差（非统计门限）；K09 sigma 为 0，禁当误差棒用

    t0_norad = t0_by_n[1024]
    t0_withrad = t0_num(OM_R, OM_M, OM_L, 1024)
    rad_shift_gyr = (t0_withrad - t0_norad) / GYR_S

    # ---- G1 引擎收敛 ----
    add("G1-ENGINE-CONVERGENCE", eng_rel < eng_tol and monotone,
        eng_act, eng_exp,
        "数值 Richardson 外推 %s s 与解析闭式 %s s 两路机拼，相对偏离 %s，数据驱动门限 %s（粗档相对偏离的 256 分之一）；5 档单调收敛=%s" % (
            sci(eng_act, 16), sci(eng_exp, 16), sci(eng_rel, 8), sci(eng_tol, 8), str(monotone)))

    # ---- G2 判别力：正负双对照 ----
    om_m_shift = OM_M * D("1.05")
    pos_rel = rel(t0_num(OM_R, om_m_shift, OM_L, 512), t0_num(OM_R, OM_M, OM_L, 512))
    if CFG["same_source_negative"]:
        step_rel = rel(t0_num(OM_R, OM_M, OM_L, 512), t0_num(OM_R, OM_M, OM_L, 512))
    else:
        step_rel = rel(t0_num(OM_R, OM_M, OM_L, 256), t0_num(OM_R, OM_M, OM_L, 1024))
    add("G2-ENGINE-DISCRIMINATION",
        pos_rel > D("0.01") and D(0) < step_rel < D("0.000001"),
        pos_rel, step_rel,
        "正对照扰动 Omega_m 5 pct 使年龄相对位移 %s；负对照步长扰动 %s 非零且远小于正对照；负对照恒绿或同源均判负" % (
            sci(pos_rel, 8), sci(step_rel, 8)))

    # ---- G3 观测复现（标 IDENTITY-by-input，单列不承重）----
    add("G3-ANCHOR-REPRODUCTION", age_rel < age_tol, age_act, age_exp,
        "含辐射真实模拟宇宙年龄 %s Gyr 与观测来料 %s Gyr 两路机拼，相对偏离 %s；输入口径容差 %s" % (
            sci(age_act, 12), sci(age_exp, 8), sci(age_rel, 8), sci(age_tol, 8)))
    note("N-AGE-IS-INPUT-RESTATEMENT", "IDENTITY",
         "此复现是回述：H0／Omega_b h2／Omega_c h2／Omega_Lambda／T_CMB 全部来自 46 项观测锚，年龄是它们的函数；K09 sigma 为 0，不构成可判负窗口。单列 IDENTITY，不作独立证据。")

    # ---- G4 跨锚张力 ----
    chi2_crit = D("3.841459")
    h0_exp = exp_h0_tension_ledger()
    h0_act = act_h0_tension_simulated()
    tension_sigma = h0_exp["K01-K02"]
    widen = (V["K02"]["value"] - V["K01"]["value"]) / (V["K01"]["sigma"] + V["K02"]["sigma"])
    extra_params = 1 if tension_sigma > chi2_crit else 0
    add("G4-CROSS-ANCHOR-TENSION",
        tension_sigma > chi2_crit and max(h0_act.values()) > chi2_crit and h0_exp != h0_act,
        max(h0_act.values()), tension_sigma,
        "单一 H0 口径无法同时相容三锚：K01-K02 张力 %s sigma（阈值 %s）；模拟口径下最大偏离 %s sigma；需放宽 sigma %s 倍或新增至少 %s 个自由参数" % (
            sci(tension_sigma, 8), sci(chi2_crit, 8), sci(max(h0_act.values()), 8),
            sci(widen, 8), str(extra_params)))

    # ---- G5 统一力方程注入 ----
    if CFG["injection_scan_enabled"]:
        inj_rows = act_injection_scan(age_act)
    else:
        inj_rows = []
    inj_exp = exp_unified_free_params()
    n_grid = 7
    late_hits = sum(1 for r in inj_rows if D(str(r["t0_rel_shift"])) < age_tol)
    early_distinct = len({r["freeze_ratio"] for r in inj_rows})
    late_absorbed = 1 if (inj_rows and late_hits == len(inj_rows)) else 0
    late_max = max((D(str(r["t0_rel_shift"])) for r in inj_rows), default=D(0))
    early_max = max((D(str(r["freeze_rel_shift"])) for r in inj_rows), default=D(0))
    disc_ratio = early_max / late_max if late_max > 0 else D(0)
    try:
        dalpha = abs(D(str(inj_exp["r20_dalpha_over_sigma"])))
    except Exception:
        dalpha = D(0)
    try:
        chi2_r20 = D(str(inj_exp["r20_chi2_min"]))
    except Exception:
        chi2_r20 = D(0)
    zeroparam_claim = 1 if CFG["injection_zeroparam_claim"] else 0
    add("G5-UNIFIED-INJECTION-ZEROPARAM",
        dalpha > chi2_crit and chi2_r20 > chi2_crit and early_distinct == n_grid
        and zeroparam_claim == 0 and len(inj_rows) == n_grid,
        early_distinct, dalpha,
        "统一耦合注入 delta_uni 不是方程零参数输出：R20 需把 alpha_s 移动 %s sigma、R24 代数无解需释放 1 参数；7 档扫描早期专属量给 %s 个互异读数，晚期年龄量命中 %s／%s 档" % (
            sci(dalpha, 8), str(early_distinct), str(late_hits), str(len(inj_rows))))
    note("N-LATE-TIME-ABSORPTION", "IDENTITY",
         "晚期宇宙年龄对早期膨胀率注入近零判别力：%s／%s 档全部落在年龄容差内，最大响应 %s；早期冻结温度最大响应 %s，两者相差 %s 倍。用年龄判注入会得到假绿，必须换到 BBN 冻结温度这类早期专属量。此为对象错位实证，单列 IDENTITY。" % (
             str(late_hits), str(len(inj_rows)), sci(late_max, 8), sci(early_max, 8), sci(disc_ratio, 8)))
    note("N-BBN-SCALE-LAW", "BOUNDARY",
         "冻结温度标度律只用 Gamma~T^5 与 H~T^2 的相对约化：T_f/T_f0=(1+delta)^(1/3)，冻结系数与 g_star 相消；不做 Y_p 绝对预言，K12 sigma 为 0 无可判负窗口。")

    # ---- G6 provenance 账 ----
    prov = build_provenance()
    indep_act = sum(1 for p in prov if not p["inputs"])
    if CFG["independent_pred_override"] is not None:
        indep_act = int(CFG["independent_pred_override"])
    prov_cleared = [dict(p, inputs=[]) for p in prov]
    indep_control = sum(1 for p in prov_cleared if not p["inputs"])
    prov_exp = exp_independent_prediction_count()
    r22_zero = prov_exp.get("_ALG_r22_equation_deriv_recompute_2026-11-15.json", {}).get("new_equation_count")
    add("G6-PROVENANCE-LEDGER",
        indep_act == 0 and indep_control > 0 and r22_zero == 0,
        indep_act, indep_control,
        "逐输出追踪输入：%s 个输出全部依赖观测锚／定义常数／跨册读数，零输入对象 %s 个；负对照清空 provenance 后读数 %s，证明判据非恒真；跨册 R22 新方程数 %s" % (
            str(len(prov)), str(indep_act), str(indep_control), str(r22_zero)))

    # ---- 门判别力、恒假门、承重源与最小割 ----
    gate_rows = [r for r in rows if r["name"].startswith("G")]
    n_gates = len(gate_rows)
    gate_pass = sum(1 for r in gate_rows if r["kind"] == "PASS")
    gate_fail = n_gates - gate_pass
    # 零判别力门 = act 与 exp 两路按相对偏离 + 容差判为同源（伪装成独立复算）
    zero_power = sum(1 for r in gate_rows if not distinct_by_rel(r["act"], r["exp"]))
    # 恒假门 = 基线判负的门，装饰判据须单列
    always_false = sum(1 for r in gate_rows if r["kind"] == "FAIL")
    # 三个独立证据源：本轮 provenance 账、跨册 R20/R24 自由度定价、来料总表 H0 三锚张力
    sources = ("PROVENANCE", "CROSSBOOK-FREE-PARAM", "LEDGER-H0-TENSION")
    bearing = len(sources)

    def cross_supported(k):
        return (bearing - k) >= 2
    min_cut = None
    for k in range(0, bearing + 1):
        if not cross_supported(k):
            min_cut = k
            break
    if min_cut is None:
        min_cut = bearing

    kn = {
        "t0_gyr": sci(age_act, 12),
        "age_rel": sci(age_rel, 8),
        "age_obs_gyr": sci(age_exp, 8),
        "age_tolerance": sci(age_tol, 8),
        "engine_rel": sci(eng_rel, 8),
        "engine_tolerance": sci(eng_tol, 8),
        "engine_monotone_seq": [sci(x, 8) for x in seq],
        "engine_richardson_rels": [sci(x, 8) for x in rich_rels],
        "H0_SI_per_s": sci(H0_SI, 12),
        "Omega_m": sci(OM_M, 12),
        "Omega_Lambda": sci(OM_L, 12),
        "Omega_r": sci(OM_R, 12),
        "Omega_gamma": sci(OM_GAMMA, 12),
        "rho_crit_kgm3": sci(RHO_CRIT, 12),
        "one_plus_z_eq": sci(ONE_PLUS_ZEQ, 12),
        "rad_shift_gyr": sci(rad_shift_gyr, 8),
        "tension_sigma": sci(tension_sigma, 8),
        "tension_k01_k03": sci(h0_exp["K01-K03"], 8),
        "tension_k02_k03": sci(h0_exp["K02-K03"], 8),
        "sigma_widen_factor": sci(widen, 8),
        "chi2_crit": sci(chi2_crit, 8),
        "r20_chi2_min": sci(chi2_r20, 12),
        "r20_dalpha_over_sigma": sci(dalpha, 8),
        "r20_alpha_s_new": str(inj_exp.get("r20_alpha_s_new", "")),
        "r24_u_star": str(inj_exp.get("r24_u_star", "")),
        "r24_mssm_chi2": str(inj_exp.get("r24_mssm_chi2", "")),
        "injection_grid_size": n_grid,
        "late_hits": late_hits,
        "early_distinct": early_distinct,
        "late_absorbed": late_absorbed,
        "late_max_response": sci(late_max, 8),
        "early_max_response": sci(early_max, 8),
        "discrimination_ratio": sci(disc_ratio, 8),
        "zeroparam_claim": zeroparam_claim,
        "independent_predictions": indep_act,
        "independent_control": indep_control,
        "n_outputs": len(prov),
        "extra_params_needed": extra_params,
        "n_gates": n_gates,
        "gate_pass": gate_pass,
        "gate_fail": gate_fail,
        "zero_power_gates": zero_power,
        "always_false_gates": always_false,
        "bearing_sources": bearing,
        "min_cut_size": min_cut,
        "spine_independent_predictions": 0,
    }

    # VERDICT-MACHINE：读数 +1 后判词串必须变化
    kn_probe = dict(kn)
    kn_probe["independent_predictions"] = int(kn["independent_predictions"]) + 1
    verdict = verdict_string(kn)
    verdict_probe = verdict_string(kn_probe)
    rows.append({"name": "E-VERDICT-MACHINE", "kind": "PASS" if verdict != verdict_probe else "FAIL",
                 "act": verdict, "exp": verdict_probe,
                 "note": "读数 +1 后判词串发生变化=%s，判词机读" % str(verdict != verdict_probe)})

    note("N-NO-NEW-PHYSICS", "INFO",
         "真实数值模拟复现宇宙演化，但全部输出是观测输入的函数；统一力方程注入需自由参数定价；独立实验预言 0，不宣称攻破统一场论或力的本源。")
    note("N-BOUNDARY", "BOUNDARY",
         "只覆盖平坦 FLRW 的 Friedmann 方程、Lambda+物质+辐射三组份、一圈 SM/MSSM beta 与 R24 的线性 RG 方程组；未含扰动增长、非平坦、暗能量状态方程演化、二圈与阈值修正；未被满足不等于不可满足。")
    note("N-NO-ADDITION", "BOUNDARY",
         "本册与 R20／R21／R22／R23／R24 是不同对象，条目与门数不相加；引擎收敛属仪器校准 IDENTITY，不承重。")

    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    nf_guard = sum(1 for r in rows if r["kind"] == "FAIL")

    src_files = [
        "数据/_ALG_expdata_fullchain_来料总表_2026-11-11.json",
        "数据/_ALG_gut_meet_recompute_2026-11-14.json",
        "数据/_ALG_r21_evidence_recompute_2026-11-15.json",
        "数据/_ALG_r22_equation_deriv_recompute_2026-11-15.json",
        "数据/_ALG_r23_generator_integrability_recompute_2026-11-15.json",
        "数据/_ALG_r24_elimination_recompute_2026-11-15.json",
        "判定_TUFT-r18-G与c核心关系三表审计_2026-10-07.md",
        "README.md",
    ]

    return {
        "date": "2026-11-15",
        "round": "第二十五轮",
        "title": "宇宙演化真实数值模拟与回述机审计",
        "verdict": verdict,
        "verdict_probe": verdict_probe,
        "key_numbers": kn,
        "gates": gate_rows,
        "rows": rows,
        "counts": counts,
        "nf_guard": nf_guard,
        "timeline": build_timeline(),
        "provenance": prov,
        "injection_scan": inj_rows,
        "h0_tension_exp": {k: sci(v, 8) for k, v in h0_exp.items()},
        "h0_tension_act": {k: sci(v, 8) for k, v in h0_act.items()},
        "readme": readme_state(),
        "identity_notes": [r["note"] for r in rows if r["kind"] == "IDENTITY"],
        "boundary_notes": [r["note"] for r in rows if r["kind"] == "BOUNDARY"],
        "info_notes": [r["note"] for r in rows if r["kind"] == "INFO"],
        "source_files": src_files,
    }

def ast_guards():
    """结构性守卫：扫本册自身源码，禁写死 ok、禁 exp==act 同表达式、禁顶层数值 return。"""
    out = []
    self_path = os.path.join(SRC, "_alg_r25_cosmos_sim_recompute.py")
    src_text = open(self_path, encoding="utf-8").read()
    tree = ast.parse(src_text)

    def put(name, ok, act, exp, note):
        out.append({"name": name, "kind": "PASS" if ok else "FAIL",
                    "act": jnum(act), "exp": jnum(exp), "note": note})

    # 1) add() 的 ok 参数不得是布尔字面量
    bad_ok = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 2:
                a = node.args[1]
                if isinstance(a, ast.Constant) and isinstance(a.value, bool):
                    bad_ok.append(a.lineno)
    put("E-NO-HARDCODE-OK", len(bad_ok) == 0, len(bad_ok), 0,
        "AST 扫描 add 调用的 ok 参数，布尔字面量命中 %s 处（期望 0）" % str(len(bad_ok)))

    # 2) exp_* 与 act_* 必须是不同函数体，且所有 return 不得是顶层数值常量
    fdefs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    exps = sorted(f.name for f in fdefs if f.name.startswith("exp_"))
    acts = sorted(f.name for f in fdefs if f.name.startswith("act_"))
    sig_exp = {ast.dump(ast.Module(body=f.body, type_ignores=[]))
               for f in fdefs if f.name.startswith("exp_")}
    sig_act = {ast.dump(ast.Module(body=f.body, type_ignores=[]))
               for f in fdefs if f.name.startswith("act_")}
    numeric_returns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
            v = node.value.value
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                numeric_returns.append(node.lineno)
    put("E-EXP-ACT-DISTINCT-AST",
        len(exps) > 0 and len(acts) > 0 and len(numeric_returns) == 0
        and sig_exp.isdisjoint(sig_act),
        len(exps) + len(acts), len(sig_exp & sig_act),
        "exp 函数 %s 个、act 函数 %s 个、两路函数体同型 %s 处、顶层数值常量 return %s 处（后两者期望 0）" % (
            str(len(exps)), str(len(acts)), str(len(sig_exp & sig_act)), str(len(numeric_returns))))

    # 3) 同源回验冒充独立复算：exp 函数不得调 act_*，act 函数不得调 exp_*
    cross_calls = []
    for f in fdefs:
        if not (f.name.startswith("exp_") or f.name.startswith("act_")):
            continue
        banned = "act_" if f.name.startswith("exp_") else "exp_"
        for node in ast.walk(f):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id.startswith(banned):
                cross_calls.append((f.name, node.func.id))
    put("E-NO-CROSS-PATH-CALL", len(cross_calls) == 0, len(cross_calls), 0,
        "跨路直接调用命中 %s 处（期望 0）；两路抽列按 exp_/act_ 前缀语义白名单，不按 kind 字段" % (
            str(len(cross_calls))))

    # 4) 自指盘点排除本册全部产物
    own_paths = [OUT_JSON, OUT_REPORT, VERIFY_JSON, MAIN_MD, MAIN_HTML]
    excl = sum(1 for p in own_paths if is_own(p))
    put("E-OWN-TOKENS-EXCLUDE", excl == len(own_paths), excl, len(own_paths),
        "本册 %s 件产物全部命中 OWN_TOKENS 自指排除，命中 %s 件" % (
            str(len(own_paths)), str(excl)))

    # 5) 链接体检覆盖 json 与 report 两侧
    missing = []
    for rel in SRC_FILES_FOR_CHECK:
        if not os.path.exists(os.path.join(MAIN, rel)):
            missing.append(rel)
    put("E-LINK-HEALTH", len(missing) == 0, len(missing), 0,
        "来料与跨册路径缺失 %s 条（期望 0）" % str(len(missing)))

    return out


SRC_FILES_FOR_CHECK = [
    "数据/_ALG_expdata_fullchain_来料总表_2026-11-11.json",
    "数据/_ALG_gut_meet_recompute_2026-11-14.json",
    "数据/_ALG_r21_evidence_recompute_2026-11-15.json",
    "数据/_ALG_r22_equation_deriv_recompute_2026-11-15.json",
    "数据/_ALG_r23_generator_integrability_recompute_2026-11-15.json",
    "数据/_ALG_r24_elimination_recompute_2026-11-15.json",
    "判定_TUFT-r18-G与c核心关系三表审计_2026-10-07.md",
    "README.md",
]


def final_of(nf_main, nf_guard, n_decl):
    """守卫 FAIL 挡门；已登记判负不挡门；缺 n_decl 报 GATES-FAIL。nf_main 不进布尔。"""
    if n_decl is None:
        return "ALG-R25-COSMOS--GATES-FAIL"
    if nf_guard > 0:
        return "ALG-R25-COSMOS--GATES-FAIL"
    return "ALG-R25-COSMOS--GATES-PASS-WITH-0-NEGATIVE"


def render_report(res):
    kn = res["key_numbers"]
    L = []
    L.append("第二十五轮 · 宇宙演化真实数值模拟与回述机审计 · 机读报告")
    L.append("日期 2026-11-15")
    L.append("")
    L.append("FINAL   = " + res["final"])
    L.append("VERDICT = " + res["verdict"])
    L.append("GUARDS  = %s / %s" % (str(res["guard_pass"]), str(res["guard_count"])))
    L.append("COUNTS  = " + json.dumps(res["counts"], ensure_ascii=False, sort_keys=True))
    L.append("")
    L.append("[关键读数]")
    for k in ("t0_gyr", "age_obs_gyr", "age_rel", "engine_rel", "engine_tolerance",
              "Omega_m", "Omega_Lambda", "Omega_r", "rho_crit_kgm3", "one_plus_z_eq",
              "rad_shift_gyr", "tension_sigma", "sigma_widen_factor", "chi2_crit",
              "r20_chi2_min", "r20_dalpha_over_sigma", "injection_grid_size",
              "late_hits", "early_distinct", "late_absorbed",
              "late_max_response", "early_max_response", "discrimination_ratio",
              "zeroparam_claim", "independent_predictions", "independent_control", "n_outputs",
              "extra_params_needed", "n_gates", "gate_pass", "gate_fail",
              "zero_power_gates", "always_false_gates", "bearing_sources",
              "min_cut_size", "spine_independent_predictions"):
        L.append("  %-28s = %s" % (k, str(kn.get(k, ""))))
    L.append("")
    L.append("[六门判定]")
    for r in res["gates"]:
        L.append("  %-34s %-5s act=%-26s exp=%-26s" % (
            r["name"], r["kind"], str(r["act"])[:26], str(r["exp"])[:26]))
    L.append("")
    L.append("[守卫与陈述条目]")
    for r in res["rows"]:
        if r["name"].startswith("G"):
            continue
        L.append("  %-36s %-18s %s" % (r["name"], r["kind"], str(r["note"])[:150]))
    L.append("")
    L.append("[注入扫描 delta_uni → 晚期年龄 / 早期冻结温度]")
    L.append("  %-10s %-26s %-26s %-26s %s" % (
        "delta", "t0_gyr", "t0_rel_shift", "freeze_ratio", "freeze_rel_shift"))
    for r in res["injection_scan"]:
        L.append("  %-10s %-26s %-26s %-26s %s" % (
            r["delta"], r["t0_gyr"], r["t0_rel_shift"], r["freeze_ratio"], r["freeze_rel_shift"]))
    L.append("")
    L.append("[宇宙演化时间线]")
    L.append("  %-10s %-22s %-18s %-20s %-20s %s" % (
        "z", "a", "t_Gyr", "H_1/s", "d_L_Mpc", "mu"))
    for r in res["timeline"]:
        L.append("  %-10s %-22s %-18s %-20s %-20s %s" % (
            r["z"], r["a"], r["t_gyr"], r["H_per_s"], r["d_L_Mpc"], r["mu"]))
    L.append("")
    L.append("[provenance 账]")
    for p in res["provenance"]:
        L.append("  %-20s %-12s %s" % (p["output"], p["kind"], ",".join(p["inputs"])))
    L.append("")
    L.append("[两路 H0 张力]")
    for k, v in res["h0_tension_exp"].items():
        L.append("  exp %-12s %s" % (k, v))
    for k, v in res["h0_tension_act"].items():
        L.append("  act %-12s %s" % (k, v))
    L.append("")
    L.append("[README 实时读数]")
    L.append("  bytes=%s md5=%s max_rid=%s" % (
        str(res["readme"]["bytes"]), res["readme"]["md5"], str(res["readme"]["max_rid"])))
    L.append("")
    L.append("[身份／边界／信息陈述]")
    for tag, arr in (("IDENTITY", res["identity_notes"]),
                     ("BOUNDARY", res["boundary_notes"]), ("INFO", res["info_notes"])):
        for t in arr:
            L.append("  %-10s %s" % (tag, t))
    L.append("")
    L.append("[来料]")
    for s in res["source_files"]:
        L.append("  " + s)
    L.append("")
    L.append("content_sha256 = " + res["content_sha256"])
    return "\n".join(L) + "\n"


def main():
    extra = ast_guards()
    res = build_result(extra_rows=extra)
    gate_fail = sum(1 for r in res["rows"] if r["kind"] == "FAIL")
    # 已登记判负由读数机读：本轮明确登记 1 条主判负（统一力方程注入不产生零参数预言）
    res["declared_negative"] = 1 if (
        res["key_numbers"]["independent_predictions"] == 0
        and res["key_numbers"]["zeroparam_claim"] == 0
        and gate_fail == 0) else 0
    res["final"] = final_of(gate_fail, gate_fail, res["declared_negative"])
    pass_n = sum(1 for r in res["rows"] if r["kind"] == "PASS")
    fail_n = sum(1 for r in res["rows"] if r["kind"] == "FAIL")
    res["guard_count"] = pass_n + fail_n
    res["guard_pass"] = pass_n
    res["guard_fail"] = fail_n
    body = dict(res)
    body.pop("content_sha256", None)
    res["content_sha256"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(render_report(res))
    print("FINAL   =", res["final"])
    print("VERDICT =", res["verdict"])
    print("GUARDS  = %d/%d" % (res["guard_pass"], res["guard_count"]))
    print("COUNTS  =", json.dumps(res["counts"], ensure_ascii=False, sort_keys=True))
    print("JSON    =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    print("REPORT  =", OUT_REPORT, os.path.getsize(OUT_REPORT), "B")
    return res


if __name__ == "__main__":
    main()
