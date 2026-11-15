# -*- coding: utf-8 -*-
"""算法联盟第二十四轮：统一场论方程的代数可解性（精确消元与相容条件）。
只产可算判决，不产新物理；数学自洽不等于实验证实；不宣称攻破统一场论。
"""
import os, glob, json, re, ast, hashlib, itertools, sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 70
DATE = "2026-11-15"

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
_anchor_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_anchor_hits) == 1, "ANCHOR-HITS=%d" % len(_anchor_hits)
MAIN = os.path.dirname(os.path.dirname(_anchor_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
JUDGE = os.path.join(MAIN, "判定")
README = os.path.join(MAIN, "README.md")

OUT_JSON = os.path.join(DATA, "_ALG_r24_elimination_recompute_2026-11-15.json")
OUT_REPORT = os.path.join(DATA, "_ALG_r24_elimination_recompute_report_2026-11-15.txt")

OWN_TOKENS = ("r24_elimination", "第二十四轮", "消元与相容条件")


def is_own(p):
    """自指盘点：本册全部产物必须排除，否则首次与复跑读数漂移。"""
    return any(t in os.path.basename(p) for t in OWN_TOKENS)


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(DATA, stem)


def md5_of(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def rel_dev(x, y):
    """判相同用偏离 + 容差，禁字符串相等；零分母单独处理。"""
    if y == 0:
        return F(0) if x == 0 else F(1)
    return abs(x - y) / abs(y)


def dstr(x, nd=12):
    """只用于展示；精确值一律以 Fraction 参与判据。"""
    return ("%." + str(nd) + "f") % float(x)


def sci(x, nd=3):
    """相对偏离展示：禁把 1e-70 舍成 0.000000（会被误读成零偏离）。"""
    return ("%." + str(nd) + "e") % float(x)


# ---------------- 来料 ----------------

SRC_FILES = {
    "r20": "_ALG_gut_meet_recompute_2026-11-14.json",
    "r20_report": "_ALG_gut_meet_recompute_report_2026-11-14.txt",
    "r22": "_ALG_r22_equation_deriv_recompute_2026-11-15.json",
    "r22_report": "_ALG_r22_equation_deriv_recompute_report_2026-11-15.txt",
    "r99": "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18.json",
    "r99_report": "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18_report.txt",
    "ledger": "_ALG_expdata_fullchain_来料总表_2026-11-11.json",
    "beta": "_ALG_UFT_eq_derive_recompute_2026-11-09.json",
}


def load_json(key):
    return json.load(open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8"))


def load_text(key):
    return open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8",
                errors="replace").read()


# ---------------- act：结构化 JSON 路径 ----------------

def act_coupling():
    k = load_json("r20")["key_numbers"]
    a = [F(str(k["a1_inv_MZ"])), F(str(k["a2_inv_MZ"])), F(str(k["a3_inv_MZ"]))]
    c = [F(str(k["c1_slope"])), F(str(k["c2_slope"])), F(str(k["c3_slope"]))]
    s = [F(str(k["sigma_a1"])), F(str(k["sigma_a2"])), F(str(k["sigma_a3"]))]
    return dict(a=a, c=c, sigma=s,
                u_obs=F(str(k["alpha_s_MZ"])),
                sigma_alpha_s=F(str(k["sigma_alpha_s"])),
                chi2_min=F(str(k["chi2_min"])),
                alpha_s_new=F(str(k["alpha_s_new"])),
                delta3=F(str(k["delta3"])),
                dalpha_s_over_sigma=F(str(k["dalpha_s_over_sigma"])),
                mssm_chi2=F(str(k["mssm_chi2"])),
                b_sm=[F(str(x)) for x in k["b_sm"]],
                b_mssm=[F(str(x)) for x in k["mssm_beta"]])


def act_r99_scaling():
    kn = load_json("r99")["key_numbers"]
    eq15 = " ".join(str(e["eq"]) for e in load_json("r99")["formula_verdicts"]
                    if "n=-5" in str(e["eq"]))
    return dict(p_r99=F(-5), eq15_present=bool("n=-5" in eq15),
                three_plus_p_reg=F(str(kn["k02_apsidal_3_plus_p"])),
                mars_pred_d=F(str(kn["k01_mars_pred_d"])),
                mars_rel_err=F(str(kn["k01_mars_rel_err"])),
                newton_rel_err=F(str(kn["k01_newton_rel_err"])),
                d2veff_p5=F(str(kn["k02_d2veff_p_minus5"])),
                d2veff_p2=F(str(kn["k02_d2veff_p_minus2"])),
                formula_count=len(load_json("r99")["formula_verdicts"]))


def act_ledger_counts():
    rows = load_json("ledger")["ledger"]
    two = [r for r in rows if str(r.get("sigma", "0")) not in ("0", "0.0", "")]
    return dict(total=len(rows), two_sided=len(two))


def act_r22_object_count():
    return len(load_json("r22")["equation_objects"])


def act_beta():
    k = load_json("beta")["key_numbers"]
    return [F(str(k[x])) for x in ("b1", "b2", "b3")]


# ---------------- exp：纯文本正则抽列，与 act 不同函数族 ----------------

def exp_r20_field(key):
    txt = load_text("r20_report")
    m = re.search(r"^%s\s*=\s*(\S+)" % re.escape(key), txt, re.M)
    return F(str(m.group(1))) if m else None


def exp_r99_mars_obs():
    txt = load_text("r99_report")
    m = re.search(r"观测\s*([\d.]+E[+-]?\d+)\s*d", txt)
    return F(str(Decimal(str(m.group(1))))) if m else None


def exp_r99_three_plus_p():
    txt = load_text("r99_report")
    m = re.search(r"3\+p=\s*([-\d.]+E[+-]?\d+)", txt)
    return F(str(Decimal(str(m.group(1))))) if m else None


def exp_r99_mars_pred():
    txt = load_text("r99_report")
    m = re.search(r"火星周期预言\s*([\d.]+E[+-]?\d+)\s*d", txt)
    return F(str(Decimal(str(m.group(1))))) if m else None


def exp_r22_new_equations():
    txt = load_text("r22_report")
    m = re.search(r"^new_equation_count\s*=\s*(\d+)", txt, re.M)
    return int(m.group(1)) if m else -1


def readme_snapshot():
    """README 实时读数：并行会话可能改动，禁时序型 MD5 判据。"""
    rb = open(README, "rb").read()
    rids = [int(m) for m in re.findall(rb"TUFT-r(\d+)_", rb)]
    tree = []
    for d in (DATA, SRC, JUDGE):
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            mm = re.search(r"r(\d+)_", os.path.basename(p))
            if mm:
                tree.append(int(mm.group(1)))
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1,
                tree_max_rid=max(tree) if tree else -1)


# ---------------- 守卫累加器 ----------------

GUARDS = []


def add(name, ok, note="", tag=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, kind="PASS" if ok else "FAIL",
                       note=str(note), tag=str(tag)))
    return ok


def add_identity(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="IDENTITY", note=str(note), tag="identity"))


def add_boundary(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="BOUNDARY", note=str(note), tag="boundary"))


def add_info(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="INFO", note=str(note), tag="info"))


def guard_stats():
    n = len(GUARDS)
    npass = sum(1 for g in GUARDS if g["kind"] == "PASS")
    nfail = sum(1 for g in GUARDS if g["kind"] == "FAIL")
    counts = {}
    for g in GUARDS:
        counts[g["kind"]] = counts.get(g["kind"], 0) + 1
    return dict(count=n, pas=npass, fail=nfail, kinds=counts)


# ---------------- 层 E：规范耦合三线联立的精确消元 ----------------

# 算术容差（机器精度），不是物理门限；物理判据一律走精确有理数符号判定
TOL = F(1, 10 ** 50)


def orthocomplement(c):
    """加权正交补方向 u=(c2-c3, c3-c1, c1-c2)：sum(u)=sum(u*c)=0 按定义恒真。"""
    return [c[1] - c[2], c[2] - c[0], c[0] - c[1]]


def delta_of(u, a):
    """三线共点的代数相容条件 Delta = sum(u_i a_i)；Delta=0 才有公共零点。"""
    return sum(u[i] * a[i] for i in range(3))


def eliminate_x(a, c):
    """路径一：由前两式解出 (A,x)，再问第三式要求 a3 等于多少。"""
    x = (a[0] - a[1]) / (c[0] - c[1])
    A = a[0] - c[0] * x
    a3_req = A + c[2] * x
    return dict(x=x, A=A, a3_required=a3_req, u_star=1 / a3_req)


def u_star_closed(u, a):
    """路径二：令 Delta(u)=0 直接解出自由参数，与路径一互不引用。"""
    return -u[2] / (u[0] * a[0] + u[1] * a[1])


def S_of(u, sigma):
    """Delta 到 chi2 的换算分母 S = sum(u_i^2 sigma_i^2)。"""
    return sum(u[i] ** 2 * sigma[i] ** 2 for i in range(3))


def family_e(C, mode="baseline"):
    a, c, sig = C["a"], C["c"], C["sigma"]
    u = orthocomplement(c)
    delta = delta_of(u, a)
    el = eliminate_x(a, c)
    us_closed = u_star_closed(u, a)
    S = S_of(u, sig)
    chi2_from_delta = delta ** 2 / S
    disp = []
    for i in range(3):
        d = -delta / u[i]
        disp.append(dict(eq=i + 1, delta=d, sigma_units=d / sig[i]))

    cfg = dict(u=u, delta=delta, x=el["x"], A=el["A"],
               a3_required=el["a3_required"], u_star=el["u_star"],
               u_star_closed=us_closed,
               u_star_path_rel=rel_dev(el["u_star"], us_closed),
               S=S, chi2_from_delta=chi2_from_delta,
               chi2_ref=C["chi2_min"],
               chi2_rel=rel_dev(chi2_from_delta, C["chi2_min"]),
               displacements=disp,
               overdetermined=3 - 2,
               free_parameters_needed=1,
               delta_nonzero=bool(delta != 0),
               sum_u=sum(u), sum_uc=sum(u[i] * c[i] for i in range(3)))

    if mode == "positive":
        # 释放 alpha_s 为自由参数并取相容值：Delta 精确为 0，系统恰定
        a3_pos = 1 / el["u_star"]
        delta_pos = delta_of(u, [a[0], a[1], a3_pos])
        cfg.update(delta=delta_pos, chi2_from_delta=delta_pos ** 2 / S,
                   chi2_rel=rel_dev(delta_pos ** 2 / S, C["chi2_min"]),
                   overdetermined=3 - 3, free_parameters_needed=0,
                   delta_nonzero=bool(delta_pos != 0),
                   u_released=el["u_star"])
    if mode == "negative":
        # 跨册口径位移：MSSM 一圈 beta 重算斜率（不碰观测与误差）
        c_neg = [c[i] * C["b_mssm"][i] / C["b_sm"][i] for i in range(3)]
        u_neg = orthocomplement(c_neg)
        d_neg = delta_of(u_neg, a)
        S_neg = S_of(u_neg, sig)
        cfg.update(c_negative=c_neg, u_negative=u_neg,
                   delta=d_neg, S=S_neg,
                   chi2_from_delta=d_neg ** 2 / S_neg,
                   chi2_rel=rel_dev(d_neg ** 2 / S_neg, C["chi2_min"]),
                   delta_nonzero=bool(d_neg != 0),
                   chi2_negative_ref=C["mssm_chi2"],
                   chi2_negative_rel=rel_dev(d_neg ** 2 / S_neg, C["mssm_chi2"]))
    return cfg


# ---------------- 层 S：距离标度方程与闭合轨道条件的精确矛盾 ----------------

def family_s(R, mode="baseline"):
    p = R["p_r99"]
    three_plus_p = p + 3
    orbit_ok = bool(three_plus_p > 0)
    T_exp = (1 - p) / 2
    mars_obs = R["mars_pred_d"] / (1 + R["mars_rel_err"])
    cfg = dict(p=p, three_plus_p=three_plus_p, orbit_ok=orbit_ok,
               T_exponent=T_exp, mars_obs_d=mars_obs,
               d2veff=R["d2veff_p5"], veff_stable=bool(R["d2veff_p5"] > 0),
               mars_rel=R["mars_rel_err"], newton_rel=R["newton_rel_err"],
               mars_mismatch=bool(R["mars_rel_err"] > 3 * R["newton_rel_err"]),
               registered_3plus=R["three_plus_p_reg"],
               free_parameters_needed=1,
               superdetermined=2 - 1)
    if mode == "positive":
        p2 = F(-2)
        cfg.update(p=p2, three_plus_p=p2 + 3, orbit_ok=bool(p2 + 3 > 0),
                   T_exponent=(1 - p2) / 2,
                   d2veff=R["d2veff_p2"], veff_stable=bool(R["d2veff_p2"] > 0),
                   mars_rel=R["newton_rel_err"],
                   mars_mismatch=bool(R["newton_rel_err"] > 3 * R["newton_rel_err"]),
                   free_parameters_needed=0, superdetermined=2 - 2)
    if mode == "negative":
        p3 = F(-3)
        # 只位移一个判据驱动量：p=-3 使 3+p 落在边界 0
        cfg.update(p=p3, three_plus_p=p3 + 3, orbit_ok=bool(p3 + 3 > 0),
                   T_exponent=(1 - p3) / 2,
                   d2veff=F(0), veff_stable=False)
    return cfg


# ---------------- 门判别力 ----------------

def gate_vector(E, S):
    return {
        "E-DELTA-NONZERO": bool(E["delta_nonzero"]),
        "E-FREE-PARAM-PRICE": bool(E["overdetermined"] > 0),
        "E-CHI2-CONSISTENT": bool(E["chi2_rel"] < TOL),
        "S-ORBIT-CONDITION-FAIL": bool(not S["orbit_ok"]),
        "S-VEFF-UNSTABLE": bool(not S["veff_stable"]),
        "S-MARS-MISMATCH": bool(S["mars_mismatch"]),
    }


def gate_power(configs):
    names = sorted(configs[0][1].keys())
    rates = {}
    for nm in names:
        vals = [bool(cfg[1][nm]) for cfg in configs]
        rates[nm] = dict(values=vals, pass_rate=sum(1 for v in vals if v) / len(vals))
    decisive = [nm for nm in names if 0 < rates[nm]["pass_rate"] < 1]
    decorative = [nm for nm in names if rates[nm]["pass_rate"] in (0.0, 1.0)]
    return dict(rates=rates, decisive=decisive, decorative=decorative,
                decisive_count=len(decisive), decorative_count=len(decorative))


# ---------------- 两路机拼（逐字类 + 偏离类分开） ----------------

def crosscheck(C, E, Eneg, S, R):
    rows = []
    rows.append(dict(key="r99_3plus_p", act=str(S["three_plus_p"]),
                     exp=str(exp_r99_three_plus_p()),
                     match=bool(S["three_plus_p"] == exp_r99_three_plus_p())))
    rows.append(dict(key="r22_new_equations", act=str(load_json("r22")["key_numbers"]["new_equation_count"]),
                     exp=str(exp_r22_new_equations()),
                     match=bool(str(load_json("r22")["key_numbers"]["new_equation_count"])
                                == str(exp_r22_new_equations()))))
    b = act_beta()
    rows.append(dict(key="beta_cross_book", act="、".join(str(x) for x in b),
                     exp=exp_beta_text(),
                     match=bool("、".join(str(x) for x in b) == exp_beta_text())))
    rows.append(dict(key="r99_mars_pred_report", act=dstr(R["mars_pred_d"], 3),
                     exp=dstr(exp_r99_mars_pred(), 3),
                     match=bool(dstr(R["mars_pred_d"], 3) == dstr(exp_r99_mars_pred(), 3))))

    rel_rows = []

    def rel(key, x, y, tol=TOL):
        d = rel_dev(x, y)
        rel_rows.append(dict(key=key, act=dstr(x, 12), exp=dstr(y, 12),
                             rel_dev=sci(d), ok=bool(d < tol)))

    rel("u_star_vs_r20_json", E["u_star"], C["alpha_s_new"])
    rel("u_star_vs_r20_report", E["u_star"], exp_r20_field("alpha_s_new"))
    rel("chi2_from_delta_vs_r20_json", E["chi2_from_delta"], C["chi2_min"])
    rel("chi2_from_delta_vs_r20_report", E["chi2_from_delta"], exp_r20_field("chi2_min"))
    rel("delta_a3_inv_vs_r20_json", E["displacements"][2]["delta"], C["delta3"])
    rel("delta_a3_inv_vs_r20_report", E["displacements"][2]["delta"], exp_r20_field("delta3"))
    rel("mssm_chi2_vs_r20", Eneg["chi2_from_delta"], C["mssm_chi2"])
    rel("mars_obs_derived_vs_report", S["mars_obs_d"], exp_r99_mars_obs(), F(1, 10 ** 6))
    return dict(rows=rows, rel_rows=rel_rows,
                exact_match=sum(1 for r in rows if r["match"]), exact_total=len(rows),
                rel_match=sum(1 for r in rel_rows if r["ok"]), rel_total=len(rel_rows))


def exp_beta_text():
    """独立册口径：R20 report 的 b_sm_text 文本登记。"""
    txt = load_text("r20_report")
    m = re.search(r"^b_sm_text\s*=\s*(\S+)", txt, re.M)
    return m.group(1).strip() if m else ""


# ---------------- 判词 ----------------

def verdict_of(K):
    return ("ALG-EL__EQ-3__UNK-2__OVER-%d__DELTA-%s__USTAR-%s__CHI2-%s__MSSM-%s"
            "__P-%s__3P-%s__MARS-%s__GATE-%d__CLEAN-%d__PRED-%d" %
            (K["overdetermined"], K["delta_str"], K["u_star_str"], K["chi2_str"],
             K["mssm_chi2_str"], K["p_str"], K["three_plus_p_str"], K["mars_pred_str"],
             K["decisive_gates"], K["clean_zero_count"], K["independent_predictions"]))


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-R24-ELIMINATION--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-R24-ELIMINATION--GATES-FAIL"
    return "ALG-R24-ELIMINATION--GATES-PASS-WITH-0-NEGATIVE"


# ---------------- AST 结构性守卫 ----------------

def kernel_source():
    return open(os.path.join(SRC, "_alg_r24_elimination_recompute.py"),
                encoding="utf-8").read()


def ast_no_hardcode_ok():
    tree = ast.parse(kernel_source())
    bad = []
    scanned = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "add"):
            continue
        scanned += 1
        arg = node.args[1] if len(node.args) >= 2 else None
        for kw in node.keywords:
            if kw.arg == "ok":
                arg = kw.value
        if arg is None or isinstance(arg, ast.Constant):
            bad.append(getattr(node, "lineno", -1))
    return dict(bad=bad, ok=bool(len(bad) == 0), scanned=scanned)


def ast_exp_act_distinct():
    tree = ast.parse(kernel_source())
    groups = {"act": set(), "exp": set()}
    bad_return = []
    calls = {"act": set(), "exp": set()}
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        for pref in groups:
            if not fn.name.startswith(pref + "_"):
                continue
            groups[pref].add(fn.name)
            for node in ast.walk(fn):
                if isinstance(node, ast.Return) and node.value is not None:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                        bad_return.append(fn.name)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    calls[pref].add(node.func.id)
    return dict(act_funcs=sorted(groups["act"]), exp_funcs=sorted(groups["exp"]),
                disjoint=bool(not (groups["act"] & groups["exp"])),
                bad_return=sorted(set(bad_return)),
                ok=bool(len(groups["act"]) > 0 and len(groups["exp"]) > 0
                        and not (groups["act"] & groups["exp"])
                        and len(bad_return) == 0
                        and "load_json" in calls["act"]
                        and "load_text" in calls["exp"]))


def ast_readme_zero_write():
    tree = ast.parse(kernel_source())
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id != "open" or not node.args:
            continue
        a0 = node.args[0]
        text = a0.id if isinstance(a0, ast.Name) else (a0.attr if isinstance(a0, ast.Attribute) else "")
        if text != "README":
            continue
        for arg in node.args[1:]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and "w" in arg.value:
                bad.append(getattr(node, "lineno", -1))
    return dict(bad=bad, ok=bool(len(bad) == 0))


def self_exclusion_check():
    """固定预期产物名校验 OWN_TOKENS 覆盖，不实时枚举磁盘 ⇒ 首次/复跑不漂移。"""
    expected = [
        os.path.basename(OUT_JSON), os.path.basename(OUT_REPORT),
        "_alg_r24_elimination_recompute.py",
        "_ALG_r24_elimination_verify_2026-11-15.json",
        "算法联盟_统一场论方程的代数可解性与消元判负_第二十四轮_2026-11-15.md",
        "算法联盟_方程消元与相容条件_第二十四轮可视化_2026-11-15.html",
    ]
    missed = [n for n in expected if not is_own(n)]
    false_positive = bool(is_own("_ALG_r23_generator_integrability_recompute_2026-11-15.json") or
                          is_own("README.md"))
    return dict(expected=len(expected), missed=missed,
                false_positive=false_positive,
                ok=bool(len(missed) == 0 and not false_positive))


def source_manifest():
    rows = []
    for key, name in sorted(SRC_FILES.items()):
        p = os.path.join(DATA, name)
        rows.append(dict(key=key, path=os.path.relpath(p, MAIN).replace("\\", "/"),
                         bytes=os.path.getsize(p), md5=md5_of(p)))
    return rows


def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                     default=str).encode("utf-8")).hexdigest()


# ---------------- 主流程 ----------------

def main():
    GUARDS.clear()
    C = act_coupling()
    R = act_r99_scaling()
    E = family_e(C)
    Epos = family_e(C, "positive")
    Eneg = family_e(C, "negative")
    Sb = family_s(R)
    Spos = family_s(R, "positive")
    Sneg = family_s(R, "negative")

    configs = [("baseline", gate_vector(E, Sb)),
               ("ctrl_pos", gate_vector(Epos, Spos)),
               ("ctrl_neg", gate_vector(Eneg, Sneg))]
    power = gate_power(configs)
    baseline_gates = configs[0][1]
    decisive_pass = sum(1 for nm in power["decisive"] if baseline_gates[nm])
    decisive_total = len(power["decisive"])

    cc = crosscheck(C, E, Eneg, Sb, R)
    n_hc = ast_no_hardcode_ok()
    n_ea = ast_exp_act_distinct()
    n_rw = ast_readme_zero_write()
    n_se = self_exclusion_check()
    rdm = readme_snapshot()
    manifest = source_manifest()
    led = act_ledger_counts()

    # 口径错位：delta 在 alpha_s^{-1} 与 alpha_s 两种参数化下的 sigma 单位
    delta_a3_inv = E["displacements"][2]["delta"]
    sig_units_a3 = E["displacements"][2]["sigma_units"]
    delta_alpha_s = E["u_star"] - C["u_obs"]
    sig_units_alpha_s = delta_alpha_s / C["sigma_alpha_s"]

    K = dict(
        equations=3, unknowns=2, overdetermined=E["overdetermined"],
        delta=dstr(E["delta"], 12), delta_str=dstr(E["delta"], 6),
        u_obs=dstr(C["u_obs"], 6), u_star=dstr(E["u_star"], 15),
        u_star_str=dstr(E["u_star"], 6),
        u_star_closed=dstr(E["u_star_closed"], 15),
        u_star_path_rel=sci(E["u_star_path_rel"]),
        u_star_vs_r20_rel=sci(rel_dev(E["u_star"], C["alpha_s_new"])),
        x_from_f12=dstr(E["x"], 12), A_from_f12=dstr(E["A"], 12),
        a3_required=dstr(E["a3_required"], 12),
        S=dstr(E["S"], 12),
        chi2_from_delta=dstr(E["chi2_from_delta"], 12),
        chi2_str=dstr(E["chi2_from_delta"], 6),
        chi2_rel=sci(E["chi2_rel"]),
        chi2_r20=dstr(C["chi2_min"], 12),
        sum_u=str(E["sum_u"]), sum_uc=dstr(E["sum_uc"], 6),
        displacement_sigma_units=[dstr(d["sigma_units"], 6) for d in E["displacements"]],
        delta_a3_inv=dstr(delta_a3_inv, 12),
        sigma_units_a3_inv=dstr(sig_units_a3, 6),
        delta_alpha_s=dstr(delta_alpha_s, 12),
        sigma_units_alpha_s=dstr(sig_units_alpha_s, 6),
        ctrl_pos_delta=dstr(Epos["delta"], 6),
        ctrl_pos_overdetermined=Epos["overdetermined"],
        ctrl_neg_delta=dstr(Eneg["delta"], 12),
        ctrl_neg_chi2=dstr(Eneg["chi2_from_delta"], 12),
        mssm_chi2=dstr(Eneg["chi2_from_delta"], 12),
        mssm_chi2_str=dstr(Eneg["chi2_from_delta"], 6),
        mssm_chi2_rel=sci(Eneg["chi2_negative_rel"]),
        mssm_chi2_r20=dstr(C["mssm_chi2"], 12),
        beta_text="、".join(str(x) for x in C["b_sm"]),
        beta_cross_book="、".join(str(x) for x in act_beta()),
        p_r99=str(Sb["p"]), p_str=str(Sb["p"]),
        three_plus_p=str(Sb["three_plus_p"]),
        three_plus_p_str=str(Sb["three_plus_p"]),
        three_plus_p_registered=str(Sb["registered_3plus"]),
        orbit_condition_ok=Sb["orbit_ok"],
        T_exponent=str(Sb["T_exponent"]),
        T_exponent_control=str(Spos["T_exponent"]),
        d2veff_p5=sci(Sb["d2veff"]), d2veff_p2=sci(Spos["d2veff"]),
        mars_pred_d=dstr(R["mars_pred_d"], 6),
        mars_pred_str=dstr(R["mars_pred_d"], 6),
        mars_obs_d=dstr(Sb["mars_obs_d"], 6),
        mars_rel=dstr(Sb["mars_rel"], 9),
        newton_rel=dstr(Sb["newton_rel"], 9),
        ctrl_pos_3plus=str(Spos["three_plus_p"]),
        ctrl_neg_3plus=str(Sneg["three_plus_p"]),
        r99_formula_count=R["formula_count"],
        r22_objects=act_r22_object_count(),
        r22_new_equations=load_json("r22")["key_numbers"]["new_equation_count"],
        ledger_total=led["total"], ledger_two_sided=led["two_sided"],
        decisive_gates=power["decisive_count"],
        decorative_gates=power["decorative_count"],
        decisive_pass=decisive_pass, decisive_total=decisive_total,
        crosscheck_exact_match=cc["exact_match"],
        crosscheck_exact_total=cc["exact_total"],
        crosscheck_rel_match=cc["rel_match"],
        crosscheck_rel_total=cc["rel_total"],
        guards_add_scanned=n_hc["scanned"],
        act_func_count=len(n_ea["act_funcs"]),
        exp_func_count=len(n_ea["exp_funcs"]),
        own_expected=n_se["expected"], own_missed=len(n_se["missed"]),
        readme_bytes=rdm["bytes"], readme_max_rid=rdm["max_rid"],
        tree_max_rid=rdm["tree_max_rid"],
        clean_zero_count=0, independent_predictions=0,
    )
    verdict = verdict_of(K)
    K["verdict"] = verdict
    K["verdict_machine_shift"] = verdict_of(dict(K, overdetermined=K["overdetermined"] + 1))

    # ---------------- 守卫注册 ----------------
    add("ANCHOR-UNIQUE", len(_anchor_hits) == 1, "唯一锚点定位主目录")
    add("SRC-FILES-PRESENT", all(os.path.isfile(os.path.join(DATA, n)) for n in SRC_FILES.values()),
        "来料文件齐全")
    add("README-SNAPSHOT-VALID", rdm["bytes"] > 0 and rdm["max_rid"] > 0, "README 实时读数")
    add("README-ZERO-WRITE-AST", n_rw["ok"], "AST 结构性零写入", "structural")
    add("E-ORTHOCOMPLEMENT-IDENTITY", E["sum_u"] == 0 and E["sum_uc"] == 0,
        "sum(u)=sum(u*c)=0 按定义恒真", "identity")
    add("E-DELTA-NONZERO", E["delta_nonzero"], "Delta(u_obs) 非零 ⇒ 代数无解")
    add("E-TWO-PATHS-CONSISTENT", E["u_star_path_rel"] < TOL,
        "两条互不引用的消元路径一致")
    add("E-USTAR-VS-R20", rel_dev(E["u_star"], C["alpha_s_new"]) < TOL,
        "独立消元复算 R20 反解值")
    add("E-CHI2-FROM-DELTA", E["chi2_rel"] < TOL,
        "纯代数 Delta^2/S 复算 R20 卡方")
    add("E-DISPLACEMENT-THIRD-MATCHES-R20", rel_dev(delta_a3_inv, C["delta3"]) < TOL,
        "第三条方程位移复算 R20 delta3")
    add("E-SIGMA-UNITS-THREE-DISTINCT",
        len(set(K["displacement_sigma_units"])) == 3,
        "三条方程的单点位移读数两两不同")
    add("E-CALIBER-DISTINCT", sig_units_a3 != sig_units_alpha_s and
        sig_units_a3 != 0 and sig_units_alpha_s != 0,
        "alpha_s^-1 口径与 alpha_s 口径数值不同，禁混用")
    add("E-ALPHAS-SIGMA-VS-R20", rel_dev(sig_units_alpha_s, C["dalpha_s_over_sigma"]) < TOL,
        "alpha_s 口径复算 R20 的 -46.762383 sigma")
    add("E-BETA-CONSISTENT", act_beta() == C["b_sm"], "独立册 beta 与 R20 登记一致")
    add("E-MSSM-DELTA-DIFFERS", Eneg["delta"] != E["delta"],
        "跨册 MSSM 位移改变相容条件")
    add("E-MSSM-CHI2-CONSISTENT", Eneg["chi2_negative_rel"] < TOL,
        "MSSM 负对照独立复算 R20 mssm_chi2")
    add("E-POS-DELTA-ZERO", Epos["delta"] == 0, "正对照释放自由参数后精确相容")
    add("E-POS-OVERDETERMINED-ZERO", Epos["overdetermined"] == 0,
        "正对照系统恰定")
    add("E-CTRL-READINGS-DISTINCT",
        len({E["delta"], Epos["delta"], Eneg["delta"]}) == 3,
        "层 E 三配置读数两两不同")
    add("S-EQ15-PRESENT", R["eq15_present"], "r99 式(15) n=-5 机读存在")
    add("S-3PLUS-SELF-COMPUTED", Sb["three_plus_p"] == Sb["registered_3plus"],
        "自算 3+p 与 r99 登记一致")
    add("S-ORBIT-CONDITION-FAIL", not Sb["orbit_ok"], "闭合轨道条件 3+p>0 被违反")
    add("S-VEFF-UNSTABLE", Sb["d2veff"] < 0, "有效势二阶导为负（极大，不稳定）")
    add("S-VEFF-CONTROL-STABLE", Spos["d2veff"] > 0, "p=-2 正对照二阶导为正")
    add("S-MARS-MISMATCH", Sb["mars_mismatch"], "火星周期预言与观测不符")
    add("S-MARS-OBS-DERIVED", rel_dev(Sb["mars_obs_d"], exp_r99_mars_obs()) < F(1, 10 ** 6),
        "由相对误差反推的观测与文本登记一致")
    add("S-T-EXPONENT-DIFFERS", Sb["T_exponent"] != Spos["T_exponent"],
        "p=-5 与 p=-2 的周期标度指数不同")
    add("S-POS-ORBIT-OK", Spos["orbit_ok"], "p=-2 正对照满足闭合轨道条件")
    add("S-NEG-BOUNDARY-ZERO", Sneg["three_plus_p"] == 0,
        "p=-3 负对照落在条件边界")
    add("S-FREE-PARAM-PRICE", Sb["superdetermined"] > 0,
        "标度族两约束一未知，超定度大于零")
    add("LEDGER-46-27", led["total"] == 46 and led["two_sided"] == 27,
        "46 锚中 27 项带双侧误差棒（规模读数）")
    add("R22-NEW-EQUATIONS-ZERO", load_json("r22")["key_numbers"]["new_equation_count"] == 0,
        "R22 全链新方程计数为零")
    add("GATE-DECISIVE-ALL-PASS", decisive_pass == decisive_total and decisive_total > 0,
        "全部有判别力门在基线判负方向成立")
    add("GATE-DECORATIVE-REPORTED", power["decorative_count"] == len(power["decorative"]),
        "装饰门如实报数并剔除出布尔值")
    add("VERDICT-MACHINE", K["verdict_machine_shift"] != K["verdict"],
        "读数加一后判词串变化")
    add("CROSSCHECK-EXACT-ALL-MATCH", cc["exact_match"] == cc["exact_total"],
        "逐字类两路机拼全一致")
    add("CROSSCHECK-REL-ALL-MATCH", cc["rel_match"] == cc["rel_total"],
        "偏离类两路机拼全一致")
    add("CROSSCHECK-BETA-CROSS-BOOK",
        any(r["key"] == "beta_cross_book" and r["match"] for r in cc["rows"]) and
        SRC_FILES["beta"] != SRC_FILES["r20_report"], "跨册独立 beta 口径一致")
    add("NO-HARDCODE-OK", n_hc["ok"], "守卫 ok 非字面量")
    add("EXP-ACT-DISTINCT-AST", n_ea["ok"], "两路函数族不同且非常量返回")
    add("SELF-EXCLUSION", n_se["ok"], "本册产物全部排除")
    add("SOURCE-MANIFEST-NONEMPTY", len(manifest) == len(SRC_FILES), "来料清单完整")

    add_identity("E-ORTHOCOMPLEMENT", "sum(u)=0 与 sum(u*c)=0 来自差分构造，按定义恒真")
    add_identity("E-CHI2-DELTA-IDENTITY", "chi2_min = Delta^2 / sum(u_i^2 sigma_i^2) 是加权最小二乘的代数恒等式，单列只作归因")
    add_identity("E-DELTA-AT-USTAR", "Delta(u_star)=0 由令相容条件为零定义，不作独立证据")
    add_identity("CROSSCHECK-REL-SAME-BOOK", "同册两路机拼的恒真部分只抓回填错，不冒充独立复算")
    add_boundary("BOUNDARY-ONE-LOOP-LINEAR", "族 1 只覆盖一圈 SM/MSSM beta 与三条线性 RG 直线，未含二圈与阈值修正")
    add_boundary("BOUNDARY-REGISTERED-PRECISION", "斜率与截距取 R20 的 60 位登记值，算术容差 1e-50 是机器精度而非物理门限")
    add_boundary("BOUNDARY-SCALING-FAMILY", "族 2 只覆盖 r99 的 p=-5 / p=-2 两个标度与 r99 机器读数")
    add_boundary("BOUNDARY-ALGEBRAIC-ONLY", "代数无解只对该有限方程组成立；未被满足不等于不可满足")
    add_info("RED-LINE-NO-CLAIM", "数学自洽不等于实验证实；四力统一未证；独立实验预言 0；不宣称攻破统一场论")
    add_info("NON-ADDITIVITY", "层 E 与层 S 是不同方程族，读数不相加；与 R20 卡方、R23 生成元层亦不相加")

    declared_negative = [
        "族 1 代数判负：3 方程 2 未知，精确相容条件 Delta=%s 非零 ⇒ 该方程组无公共零点" % K["delta"],
        "自由参数定价：释放 alpha_s 后系统恰定，需注入 1 个新自由参数，精确值 %s" % K["u_star"],
        "族 2 代数判负：p=-5 与闭合轨道条件 3+p>0 联立得 3+p=%s，矛盾" % K["three_plus_p"],
        "族 2 双路径：有效势二阶导 %s 为负（无稳定圆轨道），火星周期预言 %s d 与观测 %s d 不符" %
        (K["d2veff_p5"], K["mars_pred_d"], K["mars_obs_d"]),
    ]
    st = guard_stats()
    final = final_of(decisive_total - decisive_pass, st["fail"], len(declared_negative))

    doc = dict(
        title="算法联盟第二十四轮：统一场论方程的代数可解性（精确消元与相容条件）",
        date=DATE, nature="可算判决（代数层），不产新物理",
        final=final, verdict=verdict, guard_count=st["count"],
        guard_pass=st["pas"], guards=GUARDS, counts=st["kinds"],
        key_numbers=K,
        family_e=dict(baseline={k: str(v) for k, v in E.items()},
                      positive={k: str(v) for k, v in Epos.items()},
                      negative={k: str(v) for k, v in Eneg.items()}),
        family_s=dict(baseline={k: str(v) for k, v in Sb.items()},
                      positive={k: str(v) for k, v in Spos.items()},
                      negative={k: str(v) for k, v in Sneg.items()}),
        gate_power=power, gate_baseline=baseline_gates,
        crosscheck=cc,
        identity_notes=[g["note"] for g in GUARDS if g["kind"] == "IDENTITY"],
        boundary_notes=[g["note"] for g in GUARDS if g["kind"] == "BOUNDARY"],
        info_notes=[g["note"] for g in GUARDS if g["kind"] == "INFO"],
        declared_negative=declared_negative,
        red_line="数学自洽不等于实验证实；四力统一未证；独立实验预言 0；不宣称攻破统一场论",
        readme=rdm, source_files=manifest,
    )
    doc["content_sha256"] = canonical_sha(doc)
    open(OUT_JSON, "w", encoding="utf-8").write(
        json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True, default=str))

    lines = [
        "算法联盟：统一场论方程的代数可解性（精确消元与相容条件）· 第二十四轮",
        "=" * 96,
        "verdict : " + verdict,
        "final   : " + final,
        "counts  : " + json.dumps(st["kinds"], ensure_ascii=False, sort_keys=True),
        "guards  : %d/%d" % (st["pas"], st["count"]),
        "sha256  : " + doc["content_sha256"],
        "-" * 96,
        "[MACHINE-TABLE]",
    ]
    for kk in sorted(K.keys()):
        lines.append("%s = %s" % (kk, json.dumps(K[kk], ensure_ascii=False, sort_keys=True)))
    lines += ["-" * 96, "[DECLARED-NEGATIVE]"] + ["- " + x for x in declared_negative]
    lines += ["-" * 96, "[BOUNDARY]"] + ["- " + x for x in doc["boundary_notes"]]
    lines += ["-" * 96, "[RED-LINE]", doc["red_line"]]
    open(OUT_REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return doc


if __name__ == "__main__":
    d = main()
    print("FINAL =", d["final"])
    print("VERDICT =", d["verdict"])
    print("GUARDS = %d/%d" % (d["guard_pass"], d["guard_count"]))
    print("COUNTS =", json.dumps(d["counts"], ensure_ascii=False, sort_keys=True))
    print("DELTA =", d["key_numbers"]["delta"], "USTAR =", d["key_numbers"]["u_star"],
          "CHI2 =", d["key_numbers"]["chi2_str"])
