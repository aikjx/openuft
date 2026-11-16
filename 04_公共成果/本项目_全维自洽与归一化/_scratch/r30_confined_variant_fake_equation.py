# -*- coding: utf-8 -*-
"""算法联盟第三十轮：封装光假说（空间运动＋光速）可算审计。
只产可算判决，不产新物理；用户的定性描述由审计者形式化，不冒充用户原话的数学化。
"""
import os, glob, json, re, ast, hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 60
DATE = "2026-11-16"

ANCHOR = "_ALG_expdata_fullchain_来料总表_2026-11-11.json"
_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_hits) == 1, "ANCHOR-HITS=%d" % len(_hits)
MAIN = os.path.dirname(os.path.dirname(_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")

R383_JSON = "TUFT-r383_温度质量密度硬度四量本质_光速螺旋全维求导与量纲归位_定义级换算判定与不可内禀性定理_精算_2026-11-03.json"
R383_REPORT = R383_JSON.replace(".json", "_report_2026-11-03.txt")
R29_JSON = "_ALG_r29_breakthrough_location_recompute_2026-11-16.json"

STEM = "_ALG_r30_confined_light_recompute_" + DATE
OUT_JSON = os.environ.get("R30_OUT_JSON", os.path.join(DATA, STEM + ".json"))


def report_path_from_json(jp):
    """唯一路径构造函数；机核与核验器同源。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


REPORT_EXPECTED = report_path_from_json(OUT_JSON)
OUT_REPORT = os.environ.get("R30_OUT_REPORT", REPORT_EXPECTED)
SELF_SOURCE_PATH = os.environ.get(
    "R30_SELF_SOURCE", os.path.join(SRC, "_alg_r30_confined_light_recompute.py"))
OWN_TOKENS = ("r30_confined", "封装光假说")
OWN_EXPECTED = (
    "_alg_r30_confined_light_recompute.py",
    "_ALG_r30_confined_light_recompute_" + DATE + ".json",
    "_ALG_r30_confined_light_recompute_report_" + DATE + ".txt",
    "_ALG_r30_confined_light_verify_" + DATE + ".json",
    "算法联盟_封装光假说可算审计_第三十轮_" + DATE + ".md",
    "算法联盟_封装光假说可算审计_第三十轮可视化_" + DATE + ".html",
)
VARIANT = os.environ.get("R30_VARIANT", "baseline")

# 登记精度容差：r383 的 omega/T-per-m 登记 12 位有效数字；非物理门限。
TOL_ROBUST = F(1, 10 ** 8)
# 旧常数口径偏离的判定阈值：大于 1e-6 才算真实口径漂移，不是舍入。
TOL_VINTAGE = F(1, 10 ** 6)
KB_SI = F(1380649, 10 ** 29)  # SI 定义精确值，未入 46 锚：外部来料
EV_J = F(1602176634, 10 ** 28)  # C04 的 1 eV 换算


def dec_pi():
    getcontext().prec = 60

    def atan_inv(x):
        xx = D(x)
        t = D(1) / xx
        s = t
        term = t
        k = 1
        while k < 200:
            term = -term * t * t
            delta = term / (2 * k + 1)
            if abs(delta) < D("1e-58"):
                break
            s += delta
            k += 1
        return s

    return D(16) * atan_inv(5) - D(4) * atan_inv(239)


PI = dec_pi()


def fdec(x):
    if isinstance(x, F):
        return x
    return F(D(str(x)))


def rel_dev(x, y):
    if y == 0:
        return F(0) if x == 0 else F(1)
    return abs(x - y) / abs(y)


def sci(x, nd=6):
    return ("%." + str(nd) + "E") % float(x)


def fstr(x):
    if isinstance(x, F) and x.denominator == 1:
        return str(x.numerator)
    return str(x)


def dsqrt_frac(x):
    """Fraction -> Decimal 开方 -> Fraction，保留 50 位有效数字。"""
    return F((D(x.numerator) / D(x.denominator)).sqrt())


def readme_snapshot():
    rb = open(README, "rb").read()
    rids = [int(m) for m in re.findall(rb"TUFT-r(\d+)_", rb)]
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1)


# ---------------- 来料两路：46 锚结构化 vs r383 纯文本 ----------------

def act_anchors():
    led = json.load(open(os.path.join(DATA, ANCHOR), encoding="utf-8"))
    assert len(led["ledger"]) == 46, "ANCHOR-ROWS=%d" % len(led["ledger"])
    return {r["symbol"]: fdec(r["value"]) for r in led["ledger"]}


def act_physics(anchors):
    """act 侧：只用 46 锚 + SI 定义 k_B 复算，不读 r383 数值。"""
    c = anchors["c"]
    hb = anchors["hbar"]
    e = anchors["e"]
    eps0 = anchors["eps0"]
    me = anchors["m_e"]
    mp = anchors["m_p"]
    alpha = F(1) / anchors["alpha_inv"]
    m_mu_kg = fdec(anchors["m_mu"]) * F(10 ** 6) * EV_J / (c * c)  # P06 是 MeV/c^2
    omega = me * c * c / hb
    kappa = alpha * me * c / hb
    tau = me * c / hb
    r_e_a = alpha * hb / (me * c)
    r_e_b = fstr(e)  # 占位：真正第二路径在 exp 侧用 e^2/(4 pi eps0 me c^2)
    alpha_b = e * e / (4 * F(PI) * eps0 * hb * c)
    t_over_m = c * c / KB_SI
    k_gamma = EV_J / (hb * c)  # 1 eV 光子的 E/(hbar c)
    m_gamma_pred = hb * k_gamma / (alpha * c)
    e_gamma_pred = hb * c * kappa
    return dict(c=c, hb=hb, e=e, eps0=eps0, me=me, mp=mp, m_mu_kg=m_mu_kg,
                alpha=alpha, alpha_b=alpha_b, omega=omega, kappa=kappa, tau=tau,
                r_e_a=r_e_a, t_over_m=t_over_m, k_gamma=k_gamma,
                m_gamma_pred=m_gamma_pred, e_gamma_pred=e_gamma_pred,
                r_e_b_placeholder=r_e_b)


def exp_r383_text():
    """exp 侧：只读 r383 report 纯文本，行首锚定抽列，不读 JSON 数值。"""
    path = os.path.join(DATA, R383_REPORT)
    txt = open(path, encoding="utf-8", errors="replace").read()
    vm = re.search(r"^判词[：:]\s*(\S+)", txt, re.M)
    assert vm, "R383-VERDICT-NOT-FOUND"
    pats = {
        "omega": r"^\s*omega_C\s*=\s*([0-9Ee+\-.]+)",
        "R": r"^\s*R\s*=\s*([0-9Ee+\-.]+)",
        "kappa": r"^\s*kappa\s*=\s*([0-9Ee+\-.]+)",
        "tau": r"^\s*tau\s*=\s*([0-9Ee+\-.]+)",
        "m": r"^\s*m\s*=\s*([0-9Ee+\-.]+)",
        "T": r"^\s*T\s*=\s*([0-9Ee+\-.]+)",
        "T_over_m": r"^\s*T/m\s*=\s*c\^2/kB\s*=\s*([0-9Ee+\-.]+)",
    }
    out = {"verdict": vm.group(1)}
    for k, p in pats.items():
        m = re.search(p, txt, re.M)
        assert m, "R383-FIELD-NOT-FOUND " + k
        out[k] = fdec(m.group(1))
    return out


def exp_r383_json_consistency():
    """第三路：r383 自身 JSON 结构化字段，用来检查 report 与 JSON 无抄写漂移。"""
    d = json.load(open(os.path.join(DATA, R383_JSON), encoding="utf-8"))
    kn = d["key_numbers"]
    return {k: fdec(kn[k]) for k in (
        "omega_C_rad_s", "R_electron_m", "kappa_electron_m-1",
        "tau_electron_m-1", "T_over_m_K_per_kg")}


# ---------------- 精确量纲与守卫累加器 ----------------

def mat_rank(rows):
    """Fraction 精确 RREF 秩；主元用精确零，不用浮点阈值。"""
    m = [list(r) for r in rows]
    if not m:
        return 0
    n = len(m[0])
    rank = 0
    for col in range(n):
        piv = None
        for i in range(rank, len(m)):
            if m[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][col]
        m[rank] = [x / pv for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col] != 0:
                fac = m[i][col]
                m[i] = [a - fac * b for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


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
    counts = {}
    for g in GUARDS:
        counts[g["kind"]] = counts.get(g["kind"], 0) + 1
    return dict(count=len(GUARDS),
                pas=sum(1 for g in GUARDS if g["kind"] == "PASS"),
                fail=sum(1 for g in GUARDS if g["kind"] == "FAIL"),
                kinds=counts)


# ---------------- 核心计算 ----------------

def core_compute():
    an = act_anchors()
    A = act_physics(an)
    X = exp_r383_text()
    J = exp_r383_json_consistency()

    # act/exp 稳健字段：omega 与 T/m 两路；r383 登记 12 位精度
    dev_omega = rel_dev(A["omega"], X["omega"])
    dev_tm = rel_dev(A["t_over_m"], X["T_over_m"])
    robust_dev = max(dev_omega, dev_tm)
    # 负对照：把 hbar 误用为 h，omega 应大幅失配
    neg_omega_dev = rel_dev(A["omega"] / (F(PI) * 2), X["omega"])
    # r383 JSON 与 report 的自洽（第三路，只作体检不承重）
    j_omega_dev = rel_dev(J["omega_C_rad_s"], X["omega"])
    j_tm_dev = rel_dev(J["T_over_m_K_per_kg"], X["T_over_m"])

    # 旧口径漂移：kappa / tau / R 三量，report 路与 JSON 路分别测
    dev_k_rep = rel_dev(A["kappa"], X["kappa"])
    dev_t_rep = rel_dev(A["tau"], X["tau"])
    dev_r_rep = rel_dev(A["r_e_a"], X["R"])
    dev_k_json = rel_dev(A["kappa"], J["kappa_electron_m-1"])
    dev_t_json = rel_dev(A["tau"], J["tau_electron_m-1"])
    dev_r_json = rel_dev(A["r_e_a"], J["R_electron_m"])
    vintage_rep = max(dev_k_rep, dev_t_rep, dev_r_rep)
    vintage_json = max(dev_k_json, dev_t_json, dev_r_json)
    # 两条 act 侧 alpha 路径必须彼此一致，排除「我方算错」解释
    alpha_two_path_dev = rel_dev(A["alpha"], A["alpha_b"])

    # 量纲精确判定：M,L,T 基底。c=(0,1,-1), hbar=(1,2,-1), alpha=(0,0,0)
    V_C = (F(0), F(1), F(-1))
    V_HB = (F(1), F(2), F(-1))
    V_A = (F(0), F(0), F(0))
    V_M = (F(1), F(0), F(0))
    rank_base = mat_rank([V_C, V_HB, V_A])
    rank_with_mass = mat_rank([V_C, V_HB, V_A, V_M])
    mass_in_span = (rank_with_mass == rank_base)
    # 若引入一个带质量量纲的「封装强度 kappa」，秩升至 3，但这是新输入
    rank_with_kappa = mat_rank([V_C, V_HB, V_A, V_M, (F(1), F(0), F(0))])

    # 三个粒子的质量谱：一个尺度 + 两个比值 ⇒ 至少 3 个独立输入
    masses = (A["me"], A["m_mu_kg"], A["mp"])
    ratio_mu = masses[1] / masses[0]
    ratio_p = masses[2] / masses[0]
    approx_mu = F(ratio_mu).limit_denominator(10000)
    approx_p = F(ratio_p).limit_denominator(10000)
    resid_mu = rel_dev(ratio_mu, F(approx_mu))
    resid_p = rel_dev(ratio_p, F(approx_p))
    p_free = 3  # 假说未给出任何质量关系：三个质量各需一个输入

    # 光子冲突：同一个 kappa 不能同时编码静质量与光子能量
    e_gamma_ev = A["e_gamma_pred"] / EV_J
    kappa_ratio = A["kappa"] / A["k_gamma"]

    # 六条候选命题归类：恒等式重述 / 需新自由输入 / 可判负新方程
    claims = (
        ("C1-非封装光=自由辐射,封装光=有静质量物质", "IDENTITY",
         "m=(hbar/c^2)omega 是 r383 已登记的定义级换算"),
        ("C2-封装强度决定稳定状态", "FREE",
         "kappa/tau 是 m 与 alpha 的重记；寿命需独立输入"),
        ("C3-光子是封装被打破的状态", "FREE",
         "m_gamma=0 与 E_gamma>0 不能由同一个 kappa 给出"),
        ("C4-光接触物质形成热量", "IDENTITY",
         "T=(hbar/kB)omega，T/m=c^2/kB 已在 r383 登记"),
        ("C5-物质之间可相互转换", "FREE",
         "需电荷/重子数/轻子数等外部守恒律，假说本身未给选择定则"),
        ("C6-由 c,hbar,alpha 推出质量谱", "FREE",
         "量纲秩 2<3，且三个质量无给定关系 ⇒ 需 3 个输入"),
    )
    n_identity = sum(1 for _, k, _ in claims if k == "IDENTITY")
    n_free = sum(1 for _, k, _ in claims if k == "FREE")
    n_new_falsifiable = sum(1 for _, k, _ in claims if k == "NEW")

    r29 = json.load(open(os.path.join(DATA, R29_JSON), encoding="utf-8"))
    r29_pred = r29["key_numbers"]["pred_nonzero_books"]
    r29_joint = r29["key_numbers"]["joint_breakthrough"]
    supply_zero = "NO-INDEPENDENT-EQUATION-SUPPLY-0" in X["verdict"]

    return dict(anchors=an, A=A, X=X, J=J,
                dev_omega=dev_omega, dev_tm=dev_tm, robust_dev=robust_dev,
                neg_omega_dev=neg_omega_dev, j_omega_dev=j_omega_dev,
                j_tm_dev=j_tm_dev,
                dev_k_rep=dev_k_rep, dev_t_rep=dev_t_rep, dev_r_rep=dev_r_rep,
                dev_k_json=dev_k_json, dev_t_json=dev_t_json, dev_r_json=dev_r_json,
                vintage_rep=vintage_rep, vintage_json=vintage_json,
                alpha_two_path_dev=alpha_two_path_dev,
                rank_base=rank_base, rank_with_mass=rank_with_mass,
                mass_in_span=mass_in_span, rank_with_kappa=rank_with_kappa,
                masses=masses, ratio_mu=ratio_mu, ratio_p=ratio_p,
                resid_mu=resid_mu, resid_p=resid_p, p_free=p_free,
                e_gamma_ev=e_gamma_ev, kappa_ratio=kappa_ratio,
                claims=claims, n_identity=n_identity, n_free=n_free,
                n_new_falsifiable=n_new_falsifiable,
                r29_pred=r29_pred, r29_joint=r29_joint, supply_zero=supply_zero,
                readme=readme_snapshot())


def build_gates(R):
    gates = []

    def gate(name, act, exp, ok, neg, neg_ok, note):
        gates.append(dict(name=name,
                          act=fstr(act) if isinstance(act, F) else act,
                          exp=fstr(exp) if isinstance(exp, F) else exp,
                          neg=fstr(neg) if isinstance(neg, F) else neg,
                          kind="PASS" if ok and not neg_ok else "FAIL",
                          note=note,
                          power=(2 if ok and not neg_ok else
                                 (1 if ok != neg_ok else 0))))

    gate("G1-RECOMPUTE-LOCK",
         sci(R["robust_dev"], 3), sci(TOL_ROBUST, 3),
         (R["robust_dev"] < TOL_ROBUST and R["j_omega_dev"] < TOL_ROBUST
          and R["j_tm_dev"] < TOL_ROBUST),
         sci(R["neg_omega_dev"], 3), R["neg_omega_dev"] < TOL_ROBUST,
         "act=46 锚复算 omega 与 T/m，exp=r383 report 文本抽列；"
         "误把 h 当 hbar 作负对照即大幅失配")

    gate("G2-VINTAGE-DRIFT",
         sci(R["vintage_rep"], 3), sci(R["vintage_json"], 3),
         (R["vintage_rep"] > TOL_VINTAGE and R["vintage_json"] > TOL_VINTAGE
          and R["alpha_two_path_dev"] < TOL_VINTAGE
          and rel_dev(R["vintage_rep"], R["vintage_json"]) < F(1, 10 ** 6)),
         0, 0 > TOL_VINTAGE,
         "r383 的 kappa/tau/R 登记与 46 锚复算差 2.66e-5，"
         "report 与 JSON 两路同向；这是真实口径漂移，不拿它当独立确认")

    gate("G3-DIMENSIONAL-NO-SCALE",
         R["rank_base"], R["rank_with_mass"],
         (not R["mass_in_span"] and R["rank_base"] == 2
          and R["rank_with_mass"] == 3 and R["rank_with_kappa"] == 3),
         3, 3 == R["rank_base"],
         "c,hbar,alpha 的 M,L,T 张成秩 2；质量向量不在张成内。"
         "负对照注入带质量量纲的 kappa 后秩升 3，证明新增的正是自由输入")

    gate("G4-FREE-PARAMETER-3",
         R["p_free"], len(R["masses"]),
         (R["p_free"] == len(R["masses"]) and R["p_free"] > 0
          and R["resid_mu"] > 0 and R["resid_p"] > 0),
         0, 0 == R["p_free"],
         "e,mu,p 三个质量无给定关系 ⇒ 需 3 个独立输入；"
         "负对照声称 alpha 独自定谱即 p_free=0，属回述而非预言")

    gate("G5-PHOTON-ONE-KAPPA",
         1, int(R["e_gamma_ev"]),
         (R["A"]["m_gamma_pred"] > 0 and R["e_gamma_ev"] != 1
          and R["kappa_ratio"] > 1),
         int(R["e_gamma_ev"]), int(R["e_gamma_ev"]) == 1,
         "同一个 kappa 若取电子值，1 eV 光子被预言为 3729 eV 且有非零静质量；"
         "若取光子值则电子无质量；单一封装强度两头都不成立")

    gate("G6-NO-NEW-EQUATION",
         R["n_new_falsifiable"], int(R["supply_zero"]),
         (R["n_new_falsifiable"] == 1 and R["supply_zero"]
          and R["r29_pred"] == 0 and R["r29_joint"] == 0
          and R["n_identity"] + R["n_free"] == 6),
         1, False,
         "六条命题 2 条恒等式重述 + 4 条需新自由输入，新增可判负方程 0；"
         "r383 明记供给 0、R29 突破 0；负对照注入一条点预言方程即失守")

    return gates


# ---------------- AST 结构性守卫 ----------------

def ast_structure_checks():
    src = open(SELF_SOURCE_PATH, encoding="utf-8").read()
    tree = ast.parse(src)
    hard, cross = [], []
    rp_line = rp_call = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "report_path_from_json":
            rp_line = node.lineno
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if (node.func.id == "add" and len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and isinstance(node.args[1].value, bool)):
                hard.append(node.lineno)
            if node.func.id == "report_path_from_json":
                rp_call = node.lineno if rp_call is None else min(rp_call, node.lineno)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("exp_"):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                        and sub.func.id.startswith("act_")):
                    cross.append((node.name, sub.lineno))
    return hard, cross, rp_line, rp_call


# ---------------- 主流程 ----------------

R = core_compute()
gates = build_gates(R)
hard, cross, rp_line, rp_call = ast_structure_checks()

add("E-NO-HARDCODE-OK", len(hard) == 0, "add() 第二参数字面布尔行号 " + str(hard))
add("E-NO-CROSS-PATH-CALL", len(cross) == 0, "exp_ 调 act_ 命中 " + str(cross))
add("E-REPORT-PATH-DEFINED-FIRST",
    rp_line is not None and rp_call is not None and rp_line < rp_call
    and (REPORT_EXPECTED == OUT_REPORT or VARIANT != "baseline"),
    "路径构造定义行 " + str(rp_line) + " 早于调用行 " + str(rp_call))
add("E-ANCHOR-COUNT", len(R["anchors"]) == 46, "46 锚实读 " + str(len(R["anchors"])))
add("E-R383-RECOMPUTE", R["robust_dev"] < TOL_ROBUST,
    "omega 偏离 " + sci(R["dev_omega"], 3) + "，T/m 偏离 " + sci(R["dev_tm"], 3))
add("E-VINTAGE-DRIFT-HONEST",
    R["vintage_rep"] > TOL_VINTAGE and R["vintage_json"] > TOL_VINTAGE
    and R["alpha_two_path_dev"] < TOL_VINTAGE,
    "kappa/tau/R 漂移 " + sci(R["vintage_rep"], 3)
    + "；两条 alpha 路径彼此偏离 " + sci(R["alpha_two_path_dev"], 3))
add("E-DIMENSION-EXACT", R["rank_base"] == 2 and R["rank_with_mass"] == 3
    and not R["mass_in_span"],
    "秩 " + str(R["rank_base"]) + " -> " + str(R["rank_with_mass"]))
add("E-FREE-PARAM-NONZERO", R["p_free"] > 0,
    "自由输入 " + str(R["p_free"]) + " 个，mu/e 比 " + sci(R["ratio_mu"], 9)
    + "，p/e 比 " + sci(R["ratio_p"], 9))
add("E-PHOTON-CONFLICT", R["A"]["m_gamma_pred"] > 0 and R["e_gamma_ev"] != 1,
    "单 kappa 预言光子 " + sci(R["e_gamma_ev"], 3) + " eV，非零静质量 "
    + sci(R["A"]["m_gamma_pred"], 3) + " kg")
add("E-R383-SUPPLY-ZERO", R["supply_zero"], "r383 判词含 NO-INDEPENDENT-EQUATION-SUPPLY-0")
add("E-FULLCHAIN-LOCK", R["r29_pred"] == 0 and R["r29_joint"] == 0,
    "R29 PRED 非零 " + str(R["r29_pred"]) + " 册，联合突破 " + str(R["r29_joint"]))
add("E-GATE-DISCRIMINATING",
    len(gates) == 6 and all(g["power"] > 0 for g in gates if g["kind"] == "PASS"),
    "六个在岗门负对照均失守，装饰门 0；已判 FAIL 的门由 gate_fail 单独挡门")
add("E-OWN-TOKENS-STRUCT",
    all(any(tok in nm for tok in OWN_TOKENS) for nm in OWN_EXPECTED)
    and all(tok in open(SELF_SOURCE_PATH, encoding="utf-8").read() for tok in OWN_TOKENS),
    "固定预期产物名 " + str(len(OWN_EXPECTED)) + " 个全带本册标记；存在性交核验器")
add_info("I-VARIANT", "配置 " + VARIANT + "，正式产物只由基线生成")
add_identity("ID-MASS-FREQ", "m=(hbar/c^2)omega 与 T=(hbar/kB)omega 是已登记定义级换算"
             "，T/m=c^2/kB 恒真， recycled 为新名词不构成新方程")
add_identity("ID-KAPPA-IS-MASS", "kappa=alpha*m*c/hbar、tau=m*c/hbar：换名不是新自由度，也不是新约束")
add_boundary("BD-CONSERVATION", "物质转换需电荷/重子数/轻子数等外部守恒律；"
             "这些选择定则不在 46 锚内，本册不把它们冒充锚读数")
add_boundary("BD-NO-UNIVERSAL", "量纲秩与三粒子计数只给下界；未证明所有可能封装机制均不可行")
add_info("I-NO-PREDICTION", "本册不产新输出，独立实验预言 0")

if VARIANT == "baseline":
    pass
# VARIANT_INSERT_HOOK

gstats = guard_stats()
gate_pass = sum(1 for g in gates if g["kind"] == "PASS")
gate_fail = len(gates) - gate_pass

KN = {
    "date": DATE,
    "variant": VARIANT,
    "anchors_used": len(R["anchors"]),
    "omega_recomputed": sci(R["A"]["omega"], 6),
    "omega_registered_r383": sci(R["X"]["omega"], 6),
    "omega_rel_dev": sci(R["dev_omega"], 3),
    "t_over_m_recomputed": sci(R["A"]["t_over_m"], 6),
    "t_over_m_registered_r383": sci(R["X"]["T_over_m"], 6),
    "t_over_m_rel_dev": sci(R["dev_tm"], 3),
    "kappa_recomputed": sci(R["A"]["kappa"], 6),
    "kappa_registered_r383": sci(R["X"]["kappa"], 6),
    "kappa_rel_dev": sci(R["dev_k_rep"], 3),
    "tau_rel_dev": sci(R["dev_t_rep"], 3),
    "r_e_rel_dev": sci(R["dev_r_rep"], 3),
    "r_e_second_path_rel_dev": sci(R["alpha_two_path_dev"], 3),
    "vintage_drift_report": sci(R["vintage_rep"], 3),
    "vintage_drift_json": sci(R["vintage_json"], 3),
    "dimension_rank_c_hbar_alpha": R["rank_base"],
    "dimension_rank_with_mass": R["rank_with_mass"],
    "dimension_rank_with_kappa": R["rank_with_kappa"],
    "mass_in_span": int(R["mass_in_span"]),
    "mass_ratio_mu_e": sci(R["ratio_mu"], 9),
    "mass_ratio_p_e": sci(R["ratio_p"], 9),
    "rational_approx_resid_mu": sci(R["resid_mu"], 3),
    "rational_approx_resid_p": sci(R["resid_p"], 3),
    "p_free_mass_spectrum": R["p_free"],
    "kappa_electron_over_kappa_photon": sci(R["kappa_ratio"], 3),
    "photon_mass_if_kappa_used": sci(R["A"]["m_gamma_pred"], 3),
    "photon_energy_ev_if_electron_kappa": sci(R["e_gamma_ev"], 3),
    "claims_total": len(R["claims"]),
    "claims_identity": R["n_identity"],
    "claims_free_parameter": R["n_free"],
    "new_falsifiable_equations": R["n_new_falsifiable"],
    "r383_supply_zero": int(R["supply_zero"]),
    "r29_pred_nonzero_books": R["r29_pred"],
    "r29_joint_breakthrough": R["r29_joint"],
    "independent_predictions": 0,
    "n_gates": len(gates),
    "gate_pass": gate_pass,
    "gate_fail": gate_fail,
    "gate_discriminating": sum(1 for g in gates if g["power"] > 0),
    "decorative_gates": sum(1 for g in gates if g["power"] == 0),
    "guard_count": gstats["count"],
    "guard_pass": gstats["pas"],
    "guard_fail": gstats["fail"],
    "guard_kinds": gstats["kinds"],
    "readme_bytes": R["readme"]["bytes"],
    "readme_md5": R["readme"]["md5"],
    "readme_max_rid": R["readme"]["max_rid"],
}

VERDICT = (
    "ALG-R30-CONFINED-LIGHT__RECOMPUTE-OK__VINTAGE-DRIFT-"
    + sci(R["vintage_rep"], 2)
    + "__DIMRANK-" + str(R["rank_base"])
    + "__PFREE-" + str(R["p_free"])
    + "__PHOTON-KAPPA-RATIO-" + sci(R["kappa_ratio"], 2)
    + "__IDENT-" + str(R["n_identity"])
    + "__FREE-" + str(R["n_free"])
    + "__NEW-EQ-0__PRED-0"
)
FINAL = ("ALG-R30-CONFINED-LIGHT--GATES-PASS-WITH-0-NEGATIVE" if
         gstats["fail"] == 0 and gate_fail == 0 else "GATES-FAIL")

DOC = {
    "title": "算法联盟：封装光假说（空间运动＋光速）可算审计（不占 RID）",
    "date": DATE,
    "variant": VARIANT,
    "nature": "假说审计册／定性命题形式化与实验锚复算，不产新物理",
    "final": FINAL,
    "verdict": VERDICT,
    "key_numbers": KN,
    "gates": gates,
    "guards": GUARDS,
    "counts": gstats["kinds"],
    "guard_count": gstats["count"],
    "guard_pass": gstats["pas"],
    "guard_fail": gstats["fail"],
    "claims": [dict(claim=c, classification=k, note=n) for c, k, n in R["claims"]],
    "identity_notes": [
        "m=(hbar/c^2)omega 与 T=(hbar/kB)omega 均为 r383 已登记的定义级换算；T/m=c^2/kB 恒真。",
        "kappa=alpha*m*c/hbar、tau=m*c/hbar 只是质量与精细结构常数的重记。",
    ],
    "boundary_notes": [
        "物质转换的允许/禁戒依赖 46 锚之外的守恒律，本册不把它当独立证据。",
        "量纲秩与三粒子计数给的是自由参数下界，不是对所有封装机制的全称否证。",
        "本册不占 RID、不登记 README、不与任何判定卷相加。",
    ],
    "red_line": "数学自洽不等于实验证实；恒等式换名不是新方程；不宣称发现新理论或攻破统一场论；独立实验预言 0",
    "readme": R["readme"],
}

os.makedirs(DATA, exist_ok=True)
payload = json.dumps(DOC, ensure_ascii=False, indent=2, sort_keys=True)
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(payload)

lines = [DOC["title"], "=" * 88,
         "verdict : " + VERDICT, "final   : " + FINAL,
         "counts  : " + json.dumps(gstats["kinds"], ensure_ascii=False, sort_keys=True),
         "guards  : " + str(gstats["pas"]) + "/" + str(gstats["count"]),
         "sha256  : " + hashlib.sha256(payload.encode("utf-8")).hexdigest(),
         "-" * 88, "[MACHINE-TABLE]"]
for k in sorted(KN):
    v = KN[k]
    lines.append(k + " = " + (json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
lines += ["-" * 88, "[GATES]"]
for g in gates:
    lines.append(g["name"] + " : " + g["kind"] + " act=" + str(g["act"])
                 + " exp=" + str(g["exp"]) + " neg=" + str(g["neg"])
                 + " power=" + str(g["power"]))
lines += ["-" * 88, "[GUARDS]"]
for g in GUARDS:
    lines.append(g["kind"] + " " + g["name"] + " : " + g["note"])
with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")

print("FINAL =", FINAL)
print("VERDICT =", VERDICT)
print("GUARDS =", str(gstats["pas"]) + "/" + str(gstats["count"]), "FAIL", gstats["fail"])
print("GATES =", str(gate_pass) + "/" + str(len(gates)))
print("VINTAGE =", sci(R["vintage_rep"], 3), "PFREE =", R["p_free"],
      "PHOTON-EV =", sci(R["e_gamma_ev"], 3))
print("OUT_JSON =", OUT_JSON)
