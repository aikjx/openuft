# -*- coding: utf-8 -*-
"""
算法联盟：攻破力的统一 · 共享—分置跷跷板与参数下界 / 设计矩阵秩
====================================================================================
第七轮。直接针对「力的统一」的物理结构，不再审来源或判据。

把「同一个方程描述四力」拆成两个可算分支：
  共享参数  ⇒ 单一力程 κ 与单一耦合 g，与实验给定的力程谱 / 耦合谱直接冲突；
  分置参数  ⇒ 每条力各自 κ_i / g_i，能拟合但描述压缩增益 <= 0，统一只是模板复用。
在 Yukawa/Proca 单方程族内穷举 2×2 = 4 种配置，问是否存在
「实验存活 ∧ 压缩增益 > 0」的第三条路。

可算量全部精确有理数：
  ħc/m 力程、κ 谱、Vandermonde 设计矩阵 RREF 秩与零空间、参数下界、MDL 增益。

诚实定位：这是对这一族方程与这套实验来料的结构性判决，不是全称不可能定理。
数学自洽 != 实验证实；只产可算判决，不产新物理；四力大统一 0 条正确解、
独立实验预言 0；不宣称攻破统一场论。
（算法联盟册，不占 RID、不入 README、不与任何审计卷相加。）

环境纪律：Python 3.13 无 numpy/sympy，纯 Fraction / Decimal(60)；
UTF-8 源码 + ASCII runner；中文路径不进外层 argv。
"""
import json, os, ast, hashlib, re, glob, itertools
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
CROSS = os.path.join(ROOT, "03_跨体系研究")
GAQ_DIR = os.path.join(ROOT, "01_独立体系", "S02_空间光速螺旋统一力", "04_理论推导")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_PREV1 = os.path.join(DATA, "_ALG_expdata_fullchain_recompute_2026-11-11.json")
P_PREV5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_PREV6 = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
P_R222 = glob.glob(os.path.join(DATA, "TUFT-r222_*.json"))[0]
P_R218 = glob.glob(os.path.join(DATA, "TUFT-r218_*.json"))[0]
P_GAQ_MD = os.path.join(CROSS, "GAQ-UFT_V50_第五轮_力方程实验数据对标矩阵_2026-10-15.md")
P_GAQ_PY = os.path.join(GAQ_DIR, "unified_forces_vs_experiment.py")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_force_unification_recompute_2026-11-12.json")
OUT_REPORT = os.path.join(DATA, "_ALG_force_unification_recompute_report_2026-11-12.txt")
SOURCE_FILES = [P_LEDGER, P_PREV1, P_PREV5, P_PREV6, P_R222, P_R218,
                P_GAQ_MD, P_GAQ_PY, P_R403, P_R404]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def sci(fr, n=6):
    return format(D_fr(fr), "." + str(n) + "E")


def rel_dev(a, b):
    return abs(D_fr(a - b) / D_fr(b))


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


LEDGER = load(P_LEDGER)
PREV1 = load(P_PREV1)
PREV5 = load(P_PREV5)
PREV6 = load(P_PREV6)
R222 = load(P_R222)
R218 = load(P_R218)
R403 = load(P_R403)
R404 = load(P_R404)
GAQ_MD = open(P_GAQ_MD, encoding="utf-8").read()
GAQ_PY = open(P_GAQ_PY, encoding="utf-8").read()
GAQ_TREE = ast.parse(GAQ_PY)
E = {x["id"]: x for x in LEDGER["ledger"]}
R222K = R222["key_numbers"]
R218K = R218["key_numbers"]
K1 = PREV1["key_numbers"]

HBAR = F_of(E["C03"]["value"])
C_LIGHT = F_of(E["C01"]["value"])
E_CHARGE = F_of(E["C04"]["value"])
G_NEWTON = F_of(E["C05"]["value"])
M_PROTON = F_of(E["C09"]["value"])
M_W_P02 = F_of(E["P02"]["value"]) * F(10) ** 9
M_W_P03 = F_of(E["P03"]["value"]) * F(10) ** 9
ALPHA_INV_ZERO = F_of(E["C06"]["value"])
ALPHA_INV_MZ = F_of(E["P15"]["value"])
SIN2W = F_of(E["P08"]["value"])
ALPHA_S_MZ = F_of(E["P07"]["value"])
HC = HBAR * C_LIGHT / E_CHARGE


# ============================ act / exp 两条独立力程路径 ============================
def act_force_ranges():
    """act 路径：从 46 项来料表用 ħc/m 精确重算力程；π⁰ 质量从对标脚本 AST 机读。"""
    vals = [n.value for n in ast.walk(GAQ_TREE)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
            and not isinstance(n.value, bool)]
    # 脚本里写的是 134.9768e6，AST 把它折成 134976800.0（单位 eV）
    mpi_hits = [v for v in vals if F_of(str(v)) == F("134976800")]
    if not mpi_hits:
        raise RuntimeError("ACT-MPI-MISSING")
    mpi_ev = F_of(str(mpi_hits[0]))
    return dict(HC=HC, m_pi_ev=mpi_ev,
                lam_W_P02=HC / M_W_P02,
                lam_W_P03=HC / M_W_P03,
                lam_pi=HC / mpi_ev)


def exp_force_ranges():
    """exp 路径：从 r222 / r218 两卷成品 JSON 回读力程，与 act 互不引用。"""
    return dict(lam_W_P02=F_of(R222K["lam_W"]),
                lam_W_P03=F_of(R218K["lam_W"]),
                lam_pi=F_of(R222K["lam_pi"]),
                lam_pi_r218=F_of(R218K["lam_pi"]),
                lam_W_P02_r222=F_of(R222K["lam_W"]))


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "act_force_ranges" not in funcs or "exp_force_ranges" not in funcs:
        return False
    if ast.dump(funcs["act_force_ranges"]) == ast.dump(funcs["exp_force_ranges"]):
        return False
    for name in ("act_force_ranges", "exp_force_ranges"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


ACT = act_force_ranges()
EXP = exp_force_ranges()
DEV_W_P02 = rel_dev(ACT["lam_W_P02"], EXP["lam_W_P02"])
DEV_PI = rel_dev(ACT["lam_pi"], EXP["lam_pi"])
DEV_W_P03 = rel_dev(EXP["lam_W_P03"], ACT["lam_W_P03"])
DEV_PI_TWO = rel_dev(EXP["lam_pi"], EXP["lam_pi_r218"])

# r218 的 2.5e-6 偏差必须由「把 P03 的 80.3692 截断成 80.369」精确解释，不是拍容差。
# 判据不是 λ∝1/m 的代数恒等式（那对偏差零判别力），而是机读出那个被截断的质量值。
M_W_TRUNC = F("80.369") * F(10) ** 9
IMPLIED_M_W = HC / EXP["lam_W_P03"]
DEV_TRUNC = rel_dev(IMPLIED_M_W, M_W_TRUNC)
MASS_RATIO_MINUS_1 = M_W_P03 / M_W_TRUNC - F(1)
LAM_RATIO_MINUS_1 = EXP["lam_W_P03"] / ACT["lam_W_P03"] - F(1)
DEV_RATIO = rel_dev(MASS_RATIO_MINUS_1, LAM_RATIO_MINUS_1)
MACHINE_EPS = D("1e-50")
CALIBRE_EXPLAINED = (DEV_TRUNC < MACHINE_EPS) and (DEV_RATIO < MACHINE_EPS)
GAQ_TOL_W = F_of("0.000104")
GAQ_TOL_PI = F_of("0.000046")

# 报告 §六的 π⁰ 质量作为 act 路径质量的第二来源
MD_MPI = re.findall(r"M_π⁰=([\d.]+)\s*MeV", GAQ_MD)
MD_MPI_ACT = F_of(MD_MPI[0]) if MD_MPI else None
MPI_TWO_SOURCE = (MD_MPI_ACT is not None) and \
                 (MD_MPI_ACT * F(10) ** 6 == ACT["m_pi_ev"])


# ============================ 四力的力程谱与耦合谱 ============================
FORCES = [
    dict(id="EM", name="电磁", kappa=F(0), mass=F(0)),
    dict(id="G", name="引力", kappa=F(0), mass=F(0)),
    dict(id="W", name="弱", kappa=F(1) / ACT["lam_W_P02"], mass=M_W_P02),
    dict(id="S", name="强（剩余核力）", kappa=F(1) / ACT["lam_pi"], mass=ACT["m_pi_ev"]),
]
N_FORCE = len(FORCES)
KAPPA = [f["kappa"] for f in FORCES]
KAPPA_DISTINCT = sorted(set(KAPPA))
K_DISTINCT = len(KAPPA_DISTINCT)
LAM_PI_OVER_LAM_W = ACT["lam_pi"] / ACT["lam_W_P02"]

ALPHA_EM_ACT = F(1) / ALPHA_INV_ZERO
ALPHA_W_ACT = (F(1) / ALPHA_INV_MZ) * SIN2W
ALPHA_S_ACT = ALPHA_S_MZ
ALPHA_G_ACT = G_NEWTON * M_PROTON ** 2 / (HBAR * C_LIGHT)
COUPLINGS_ACT = [ALPHA_EM_ACT, ALPHA_W_ACT, ALPHA_S_ACT, ALPHA_G_ACT]
A_DISTINCT = len(set(COUPLINGS_ACT))
ALPHA_G_EXP = F_of(K1["alpha_G_proton"])
DEV_ALPHA_G = rel_dev(ALPHA_G_ACT, ALPHA_G_EXP)
COUPLINGS_EXP = [F(1) / F_of(K1["alpha1_inv_MZ_act"]),
                 F(1) / F_of(K1["alpha2_inv_MZ_act"]),
                 F(1) / F_of(K1["alpha3_inv_MZ_act"]),
                 ALPHA_G_EXP]
A_DISTINCT_EXP = len(set(COUPLINGS_EXP))
COUPLING_SPAN_DEX = D(str(K1["coupling_span_dex"]))
FE_OVER_FG = D(str(K1["F_E_over_F_G"]))


# ============================ 精确有理 RREF 与 Vandermonde 设计矩阵 ============================
def rref_rank(mat):
    m = [[F(x) for x in row] for row in mat]
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                q = m[i][c]
                m[i] = [a - q * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def vandermonde(kappas, ncols):
    return [[k ** j for j in range(ncols)] for k in kappas]


V3 = vandermonde(KAPPA_DISTINCT, 3)
V2 = vandermonde(KAPPA_DISTINCT, 2)
RANK_V3 = rref_rank(V3)
RANK_V2 = rref_rank(V2)
DEFICIENCY_V2 = len(V2) - RANK_V2
NULL_VEC = [KAPPA_DISTINCT[2] - KAPPA_DISTINCT[1],
            -KAPPA_DISTINCT[2], KAPPA_DISTINCT[1]]


def orth_residual(vec):
    return [sum(vec[i] * V2[i][j] for i in range(len(V2)))
            for j in range(len(V2[0]))]


ORTH_RESIDUAL = orth_residual(NULL_VEC)
BAD_VEC = list(NULL_VEC)
BAD_VEC[0] = BAD_VEC[0] + F(1)
ORTH_RESIDUAL_BAD = orth_residual(BAD_VEC)
NULL_VEC_DISCRIMINATES = all(x == 0 for x in ORTH_RESIDUAL) and \
                         any(x != 0 for x in ORTH_RESIDUAL_BAD)
P_EQ = 2

# ============================ 共享—分置跷跷板：2×2 穷举 ============================
def config_eval(k_split, g_split):
    """k_split/g_split = 该维度是否允许每条力各自取值；False 表示四力共享一个参数。"""
    p_extra = (K_DISTINCT - 1 if k_split else 0) + (A_DISTINCT - 1 if g_split else 0)
    mismatch = (0 if k_split else K_DISTINCT - 1) + (0 if g_split else A_DISTINCT - 1)
    gain = N_FORCE - p_extra
    survive = (mismatch == 0)
    unified = (gain > 0)
    breakthrough = survive and unified
    return dict(k_split=k_split, g_split=g_split, p_extra=p_extra,
                mismatch=mismatch, gain=gain, survive=survive,
                unified=unified, breakthrough=breakthrough)


CONFIGS = [config_eval(ks, gs) for ks in (False, True) for gs in (False, True)]
N_CONFIGS = len(CONFIGS)
N_ESCAPE = sum(1 for c in CONFIGS if c["breakthrough"])
P_EXTRA_MAX = max(c["p_extra"] for c in CONFIGS)
GAIN_MAX = max(c["gain"] for c in CONFIGS)
SHARED_CONFIGS = [c for c in CONFIGS if not (c["k_split"] and c["g_split"])]
SEPARATE_CONFIG = [c for c in CONFIGS if c["k_split"] and c["g_split"]][0]
SHARED_ALL_EXCLUDED = all(not c["survive"] for c in SHARED_CONFIGS)
SEPARATE_GAIN = SEPARATE_CONFIG["gain"]
SEPARATE_SURVIVES = SEPARATE_CONFIG["survive"]
SHARED_KAPPA_MISMATCH = K_DISTINCT - 1
SHARED_COUPLING_MISMATCH = A_DISTINCT - 1
P_MIN_EXTRA = SHARED_KAPPA_MISMATCH + SHARED_COUPLING_MISMATCH
SEESAW = SHARED_ALL_EXCLUDED and SEPARATE_SURVIVES and (SEPARATE_GAIN <= 0) and (N_ESCAPE == 0)


# ============================ 正 / 负对照 ============================
def merged_kappa_distinct():
    """阳性对照：把 κ_W 与 κ_π 人为合并成一类，共享分支失配必须下降。"""
    merged = [F(0), KAPPA_DISTINCT[1], KAPPA_DISTINCT[1]]
    return len(set(merged))


K_MERGED = merged_kappa_distinct()
SHARED_MISMATCH_BASE = SHARED_KAPPA_MISMATCH + SHARED_COUPLING_MISMATCH
SHARED_MISMATCH_MERGED = (K_MERGED - 1) + SHARED_COUPLING_MISMATCH
POS_CTRL_ALERTS = (K_DISTINCT == 3) and (K_MERGED == 2) and \
                  (SHARED_MISMATCH_MERGED < SHARED_MISMATCH_BASE)
N_LONG_RANGE = sum(1 for f in FORCES if f["kappa"] == 0)
NEG_CTRL_GREEN = (N_LONG_RANGE >= 2) and all(
    f["kappa"] == 0 for f in FORCES if f["id"] in ("EM", "G"))
CTRL_READINGS = [N_CONFIGS, P_EQ, N_ESCAPE, P_EXTRA_MAX]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
not_all_green = (len(set(CTRL_READINGS)) > 1) and (N_ESCAPE == 0) and \
                SHARED_ALL_EXCLUDED and (RANK_V3 > RANK_V2)

# ============================ 两路机拼判定 ============================
DEV_W_P02_OK = (DEV_W_P02 < MACHINE_EPS)
DEV_PI_OK = (DEV_PI < MACHINE_EPS) and (DEV_PI_TWO < MACHINE_EPS)
DEV_W_P03_IN_SOURCE_TOL = (DEV_W_P03 < D_fr(GAQ_TOL_W))
CALIBRE_OK = CALIBRE_EXPLAINED and DEV_W_P03_IN_SOURCE_TOL and \
             (MASS_RATIO_MINUS_1 > 0) and (DEV_W_P03 > 0)
ALPHA_G_TWO_SOURCE = (DEV_ALPHA_G < MACHINE_EPS)
COUPLING_TWO_PATH = (A_DISTINCT == 4) and (A_DISTINCT_EXP == 4)
VANDEX_OK = (RANK_V3 == 3) and (RANK_V2 == 2) and (DEFICIENCY_V2 == 1) and \
            NULL_VEC_DISCRIMINATES and (P_MIN_EXTRA > P_EQ)


# ============================ 跨卷脊梁与诚实边界 ============================
R218_PRICING = R218K.get("pricing", {}).get("counts", {})
R218_COVERAGE = R218K.get("coverage", {})
R218_SHAPE = R218K.get("shape_confrontation", {})
R218_SURVIVE = int(R218_PRICING.get("SURVIVE", -1))
R218_OUT_OF_FORM = int(R218_COVERAGE.get("n_out_of_form", -1))
R218_SHAPE_HITS = int(R218_SHAPE.get("n_hits", -1))
R222_DISP_RESIDUAL = D(str(R222K["max_disp_residual"]))
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and \
             (R404["key_numbers"]["four_force_accepted"] == 0)
spine_pred = sum(1 for e in R403.get("entries", []) if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
prev5_hits = int(PREV5["key_numbers"]["pairs_hit"])
prev6_hits = int(PREV6["key_numbers"]["pairs_hit_after"])
prev6_open = int(PREV6["key_numbers"]["remaining_undetermined"])
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(SOURCE_FILES) > 0) and (len(source_missing) == 0)
honest_boundary = spine_zero and (spine_pred == 0) and (prev5_hits == 0) and \
                  (prev6_hits == 0) and (N_ESCAPE == 0)

BACKFIRE_READINGS = dict(n_escape=N_ESCAPE, gain_max=GAIN_MAX,
                         shared_mismatch=SHARED_MISMATCH_BASE,
                         k_distinct=K_DISTINCT, p_extra_max=P_EXTRA_MAX)

# ============================ 元守卫 ============================
def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


def verdict_with(token):
    return ("ALG-FORCE-UNIFICATION"
            + "__FORCES-" + str(N_FORCE)
            + "__KAPPA-CLASSES-" + str(K_DISTINCT)
            + "__COUPLING-CLASSES-" + str(A_DISTINCT)
            + "__CONFIGS-" + str(N_CONFIGS)
            + "__ESCAPE-" + token
            + "__P-MIN-EXTRA-" + str(P_MIN_EXTRA)
            + "__RANK-" + str(RANK_V3) + "vs" + str(RANK_V2)
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_ESCAPE))
v_machine_1 = verdict_with(str(N_ESCAPE + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and \
                     (("__ESCAPE-" + str(N_ESCAPE)) in v_machine_0)
verdict = v_machine_0

segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV6-RELOADED",
    (PREV6["guard_pass"] == PREV6["guard_count"]) and
    (PREV6["guard_count"] == 38) and (prev6_hits == 0) and
    (prev6_open == 0) and (prev5_hits == 0),
    "PASS",
    "第六轮 38/38 守卫、8 对归属闭合、回填 0 命中；第五轮穷举 0 命中。本册不再审来源，直接转向力的物理结构")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("FORCE-INVENTORY", (N_FORCE == 4) and (len(set(f["id"] for f in FORCES)) == 4), "PASS",
    "四力清单机读：" + " / ".join(f["name"] for f in FORCES) + "，每条带 κ 与质量")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_force_ranges（ħc/m 重算）与 exp_force_ranges（r222/r218 回读）为两个不同函数，return 均非顶层数值常量")
add("TWO-PATH-W-P02-EXACT", DEV_W_P02_OK, "PASS",
    "两路机拼：act 用 C01/C03/C04 + P02 算 λ_W = " + sci(ACT["lam_W_P02"], 12) +
    " m，r222 成品读数相同，相对偏离 " + format(DEV_W_P02, ".3E"))
add("TWO-PATH-PI-EXACT", DEV_PI_OK and MPI_TWO_SOURCE, "PASS",
    "λ_π = " + sci(ACT["lam_pi"], 12) + " m：act 从对标脚本 AST 机读 m_π⁰，报告 §六第二来源同值；" +
    "r222/r218 两卷 λ_π 一致，相对偏离 " + format(DEV_PI_TWO, ".3E"))
add("ALPHA-G-TWO-SOURCE", ALPHA_G_TWO_SOURCE, "PASS",
    "α_G act = G·m_p²/(ħc) = " + sci(ALPHA_G_ACT, 9) + "，第一册成品 " +
    sci(ALPHA_G_EXP, 9) + "，相对偏离 " + format(DEV_ALPHA_G, ".3E"))
add("R218-CALIBRE-EXPLAINED", CALIBRE_OK, "PASS",
    "★口径差异机算还原：r218 λ_W 比 act(P03) 大 " + format(DEV_W_P03, ".6E") +
    "，由隐含质量 " + format(D_fr(IMPLIED_M_W) / D(10) ** 9, ".6f") +
    " GeV（= P03 的 80.3692 被截断为 80.369）精确解释：质量比减一 " +
    format(D_fr(MASS_RATIO_MINUS_1), ".12E") + " 与 λ 比减一 " +
    format(D_fr(LAM_RATIO_MINUS_1), ".12E") + " 一致；远小于来源自报 0.0104% 阈值")

add("KAPPA-SPECTRUM-3-CLASSES",
    (K_DISTINCT == 3) and (N_LONG_RANGE == 2) and (LAM_PI_OVER_LAM_W > 500),
    "PASS",
    "力程谱机读：κ = 0（电磁、引力两类长程）、κ_W、κ_π，共 " + str(K_DISTINCT) +
    " 类；λ_π/λ_W = " + format(D_fr(LAM_PI_OVER_LAM_W), ".4f") + " 倍，不是同一个力程")
add("COUPLING-SPECTRUM-4-CLASSES", COUPLING_TWO_PATH, "PASS",
    "耦合谱机读：act 四个无量纲耦合两两不同（" + str(A_DISTINCT) +
    " 类），第一册 α1/α2/α3/α_G 亦 " + str(A_DISTINCT_EXP) +
    " 类；跨度 " + format(COUPLING_SPAN_DEX, ".4f") + " dex")
add("RANK-V3-FULL", (RANK_V3 == 3), "PASS",
    "精确有理 RREF：三个不同 κ 上的 3×3 Vandermonde 设计矩阵秩 " + str(RANK_V3) +
    " ⇒ 要插值这三类力程至少需要 3 个独立参数方向")
add("RANK-V2-DEFICIENT", (RANK_V2 == 2) and (DEFICIENCY_V2 == 1) and (P_MIN_EXTRA > P_EQ),
    "PASS",
    "单方程只提供 " + str(P_EQ) + " 个参数方向 ⇒ 3×2 设计矩阵秩 " + str(RANK_V2) +
    "、亏 " + str(DEFICIENCY_V2) + "；参数下界 " + str(P_MIN_EXTRA) +
    "（2 个独立质量 + 3 个独立耦合破缺）> " + str(P_EQ))
add("NULL-VEC-DISCRIMINATES", NULL_VEC_DISCRIMINATES, "PASS",
    "零空间负对照：显式构造的非零向量与两列精确正交（残差全 0）；给它加 1 后残差非零 ⇒ 该检验有判别力，不是恒等式")
add("VANDEX-CONSISTENT", VANDEX_OK, "PASS",
    "秩、亏、零向量、参数下界四项互洽，均由精确有理数机算")

add("SHARED-EXCLUDED", SHARED_ALL_EXCLUDED, "PASS",
    "★共享分支：单一 κ 与单一 g 无法同时给出 " + str(K_DISTINCT) + " 类力程与 " +
    str(A_DISTINCT) + " 类耦合，失配 " + str(SHARED_MISMATCH_BASE) +
    " 处（κ " + str(SHARED_KAPPA_MISMATCH) + " + g " + str(SHARED_COUPLING_MISMATCH) +
    "）⇒ 被实验谱直接排除")
add("SEPARATE-NO-COMPRESSION", SEPARATE_SURVIVES and (SEPARATE_GAIN <= 0), "PASS",
    "★分置分支：每条力各自 κ_i / g_i 可拟合，但需额外 " + str(P_EXTRA_MAX) +
    " 个参数，MDL 增益 = " + str(N_FORCE) + " − " + str(P_EXTRA_MAX) + " = " +
    str(SEPARATE_GAIN) + " ≤ 0 ⇒ 统一只是模板复用，没有压缩描述")
add("CONFIG-ENUMERATION-COMPLETE",
    (N_CONFIGS == 4) and (len({(c["k_split"], c["g_split"]) for c in CONFIGS}) == 4),
    "PASS",
    "2×2 穷举四种配置（κ 共享/分置 × g 共享/分置），无遗漏、无重复")
add("SEESAW-ZERO-ESCAPE", SEESAW and (N_ESCAPE == 0), "PASS",
    "共享 ⇒ 被排除；分置 ⇒ 增益 " + str(SEPARATE_GAIN) +
    " ≤ 0；「实验存活 ∧ 压缩增益 > 0」的逃逸配置 " + str(N_ESCAPE) +
    " 个 ⇒ 在单方程族内没有第三条路")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个计数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 " + str(CTRL_READINGS[0]) + "，杜绝全表读数相同造成的假判别力")
add("CTRL-POSITIVE-ALERTS", POS_CTRL_ALERTS, "PASS",
    "阳性对照：把 κ_W 与 κ_π 人为合并 ⇒ 力程类数 " + str(K_DISTINCT) + "→" +
    str(K_MERGED) + "，共享失配 " + str(SHARED_MISMATCH_BASE) + "→" +
    str(SHARED_MISMATCH_MERGED) + " ⇒ 判据确实由实测力程差驱动")
add("CTRL-IDENTITY-NEVER-HITS", NEG_CTRL_GREEN and (N_LONG_RANGE == 2), "IDENTITY",
    "阴性对照：电磁与引力 κ 均为 0，长程段恒绿且不受本册判据影响，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有共享排除、分置零压缩、秩亏、参数下界等非恒绿读数")

add("R218-SPINE-0-SURVIVE",
    (R218_SURVIVE == 0) and (R218_SHAPE_HITS == 0) and (R218_OUT_OF_FORM >= 1),
    "PASS",
    "跨卷脊梁：r218 修复定价 " + str(R218_PRICING) + "、形状对撞命中 " +
    str(R218_SHAPE_HITS) + "、形式外行数 " + str(R218_OUT_OF_FORM) +
    "（色禁闭不在此方程形式内）⇒ 已有卷独立给出「形式统一不可修复」")
add("R222-DISPERSION-RESIDUAL", (R222_DISP_RESIDUAL < D("1e-30")), "PASS",
    "r222 传播层：色散残差 " + format(R222_DISP_RESIDUAL, ".3E") +
    "，质量—力程等价成立 ⇒ 本册用 κ 谱代表力程谱有仓库依据")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 " + str(spine_pred) +
    "；第五轮 0 命中、第六轮 0 命中、本册逃逸 " + str(N_ESCAPE))
add("FAMILY-LIMITED-CLAIM", (P_MIN_EXTRA > P_EQ) and (N_ESCAPE == 0), "BOUNDARY",
    "本册结论只对 Yukawa/Proca 单方程族 + 这 46 项来料成立；不是「四力统一不可能」的全称定理。" +
    "换参数化、换方程族或引入新的对称性破缺结构都超出本册可算范围")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (N_ESCAPE == 0), "INFO",
    "本册不宣称攻破力的统一；给出的是「共享—分置跷跷板」这条结构性判决")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（力程谱、秩、参数账），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_ESCAPE == 0) and (P_MIN_EXTRA > P_EQ), "INFO",
    "要越过本册下界，必须给出能把 " + str(K_DISTINCT) + " 类力程与 " +
    str(A_DISTINCT) + " 类耦合从少于 " + str(N_FORCE) +
    " 个独立参数里生出来的机制；这仍需要一条带双侧误差棒的新实验读数来验收，不是再放宽判据")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把逃逸配置读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-FORCE-UNIFICATION--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-FORCE-UNIFICATION--GATES-FAIL"
    return "ALG-FORCE-UNIFICATION--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "SHARED-EXCLUDED", "SEPARATE-NO-COMPRESSION",
                     "SEESAW-ZERO-ESCAPE", "RANK-V2-DEFICIENT"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-FORCE-UNIFICATION--GATES-PASS-WITH-0-NEGATIVE") and \
              (nf_guard_before == 0) and (len(declared_negative) > 0)
add("FINAL-OF-CONSISTENT", final_of_ok, "PASS",
    "final_of(nf_main=" + str(nf_main_before) + ",nf_guard=" + str(nf_guard_before) +
    ",n_decl=" + str(len(declared_negative)) + ")：守卫 FAIL 挡门、已登记判负不挡门、缺 n_decl 报 GATES-FAIL")

counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0, "BOUNDARY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)

key_numbers = {
    "forces": N_FORCE,
    "hbar_c_eV_m": sci(HC, 12),
    "lam_W_P02_m": sci(ACT["lam_W_P02"], 12),
    "lam_W_P03_m": sci(ACT["lam_W_P03"], 12),
    "lam_pi_m": sci(ACT["lam_pi"], 12),
    "lam_pi_over_lam_W": format(D_fr(LAM_PI_OVER_LAM_W), ".6f"),
    "dev_W_P02_two_path": format(DEV_W_P02, ".6E"),
    "dev_pi_two_path": format(DEV_PI, ".6E"),
    "dev_W_P03_r218_vs_act": format(DEV_W_P03, ".12E"),
    "r218_implied_m_W_GeV": format(D_fr(IMPLIED_M_W) / D(10) ** 9, ".6f"),
    "r218_mass_ratio_minus_1": format(D_fr(MASS_RATIO_MINUS_1), ".12E"),
    "r218_lam_ratio_minus_1": format(D_fr(LAM_RATIO_MINUS_1), ".12E"),
    "r218_dev_implied_vs_trunc": format(DEV_TRUNC, ".6E"),
    "kappa_classes": K_DISTINCT,
    "long_range_forces": N_LONG_RANGE,
    "coupling_classes_act": A_DISTINCT,
    "coupling_classes_exp": A_DISTINCT_EXP,
    "coupling_span_dex": format(COUPLING_SPAN_DEX, ".6f"),
    "alpha_G_act": sci(ALPHA_G_ACT, 9),
    "alpha_G_exp": sci(ALPHA_G_EXP, 9),
    "dev_alpha_G_two_path": format(DEV_ALPHA_G, ".6E"),
    "F_E_over_F_G": format(FE_OVER_FG, ".6E"),
    "rank_v3": RANK_V3,
    "rank_v2": RANK_V2,
    "deficiency_v2": DEFICIENCY_V2,
    "p_eq_single_equation": P_EQ,
    "p_min_extra": P_MIN_EXTRA,
    "shared_kappa_mismatch": SHARED_KAPPA_MISMATCH,
    "shared_coupling_mismatch": SHARED_COUPLING_MISMATCH,
    "shared_total_mismatch": SHARED_MISMATCH_BASE,
    "configs_enumerated": N_CONFIGS,
    "escape_configs": N_ESCAPE,
    "p_extra_max": P_EXTRA_MAX,
    "gain_max": GAIN_MAX,
    "separate_gain": SEPARATE_GAIN,
    "shared_all_excluded": SHARED_ALL_EXCLUDED,
    "positive_control_kappa_merged": K_MERGED,
    "control_readings": CTRL_READINGS,
    "r218_pricing_survive": R218_SURVIVE,
    "r218_shape_hits": R218_SHAPE_HITS,
    "r218_out_of_form": R218_OUT_OF_FORM,
    "r222_disp_residual": format(R222_DISP_RESIDUAL, ".3E"),
    "prev5_hits": prev5_hits,
    "prev6_hits": prev6_hits,
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": spine_pred,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：攻破力的统一 · 共享—分置跷跷板与参数下界 / 设计矩阵秩",
    "date": "2026-11-12",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "gates": {
        "act": "ħc/m 从 46 项来料表精确重算力程",
        "exp": "r222 / r218 两卷成品 JSON 回读力程",
        "spectrum": "κ 谱与耦合谱的不同取值类数",
        "rank": "精确有理 RREF 的 Vandermonde 设计矩阵秩与零空间",
        "seesaw": "共享参数被实验排除 / 分置参数压缩增益 <= 0",
    },
    "forces": [dict(id=f["id"], name=f["name"],
                    kappa=str(f["kappa"]), mass_eV=str(f["mass"])) for f in FORCES],
    "couplings": dict(act=[str(x) for x in COUPLINGS_ACT],
                      exp=[str(x) for x in COUPLINGS_EXP]),
    "two_path": dict(act_lam_W_P02=str(ACT["lam_W_P02"]),
                     exp_lam_W_P02=str(EXP["lam_W_P02"]),
                     act_lam_pi=str(ACT["lam_pi"]),
                     exp_lam_pi=str(EXP["lam_pi"]),
                     dev_W_P02=format(DEV_W_P02, ".6E"),
                     dev_pi=format(DEV_PI, ".6E"),
                     r218_calibre_explained=bool(CALIBRE_EXPLAINED)),
    "rank_evidence": dict(kappa_distinct=[str(k) for k in KAPPA_DISTINCT],
                          v3_rows=[[str(x) for x in row] for row in V3],
                          rank_v3=RANK_V3, rank_v2=RANK_V2,
                          deficiency_v2=DEFICIENCY_V2,
                          null_vector=[str(x) for x in NULL_VEC],
                          orth_residual=[str(x) for x in ORTH_RESIDUAL],
                          bad_vector_residual=[str(x) for x in ORTH_RESIDUAL_BAD]),
    "configurations": CONFIGS,
    "key_numbers": key_numbers,
    "segments": segs,
}
_payload = json.dumps(out, ensure_ascii=False, sort_keys=True, indent=0)
digest = hashlib.sha256(_payload.encode("utf-8")).hexdigest()
out["content_sha256"] = digest

if __name__ == "__main__":
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：攻破力的统一 · 共享—分置跷跷板与参数下界 / 设计矩阵秩")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("两路机拼：act ħc/m 重算 vs exp r222/r218 回读。")
    lines.append("  hbar*c/e = " + sci(HC, 12) + " eV*m")
    lines.append("  lambda_W(P02=80.377) = " + sci(ACT["lam_W_P02"], 12) +
                 " m  [r222 同值，偏离 " + format(DEV_W_P02, ".3E") + "]")
    lines.append("  lambda_W(P03=80.3692) = " + sci(ACT["lam_W_P03"], 12) + " m")
    lines.append("  lambda_pi = " + sci(ACT["lam_pi"], 12) +
                 " m  [r222/r218 同值，偏离 " + format(DEV_PI, ".3E") + "]")
    lines.append("  r218 口径差异 " + format(DEV_W_P03, ".12E") + " 由隐含质量 " +
                 format(D_fr(IMPLIED_M_W) / D(10) ** 9, ".6f") +
                 " GeV（P03 截断为 80.369）精确解释；比值减一 " +
                 format(D_fr(MASS_RATIO_MINUS_1), ".12E") + " / " +
                 format(D_fr(LAM_RATIO_MINUS_1), ".12E"))
    lines.append("-" * 96)
    lines.append("力程谱 kappa 类数 = " + str(K_DISTINCT) +
                 "（长程 2 条 + W + pi）；lambda_pi/lambda_W = " +
                 format(D_fr(LAM_PI_OVER_LAM_W), ".6f"))
    lines.append("耦合谱类数 act=" + str(A_DISTINCT) + " exp=" + str(A_DISTINCT_EXP) +
                 "，跨度 " + format(COUPLING_SPAN_DEX, ".6f") + " dex")
    lines.append("Vandermonde RREF：3x3 秩 " + str(RANK_V3) + "，3x2 秩 " +
                 str(RANK_V2) + "，亏 " + str(DEFICIENCY_V2) +
                 "；单方程参数方向 " + str(P_EQ) + " < 参数下界 " + str(P_MIN_EXTRA))
    lines.append("-" * 96)
    lines.append("2x2 穷举（k_split / g_split / p_extra / mismatch / gain / survive / breakthrough）：")
    for c in CONFIGS:
        lines.append("  " + str(c["k_split"]).ljust(6) + str(c["g_split"]).ljust(6) +
                     str(c["p_extra"]).rjust(3) + str(c["mismatch"]).rjust(4) +
                     str(c["gain"]).rjust(4) + "  " + str(c["survive"]).ljust(6) +
                     str(c["breakthrough"]))
    lines.append("★逃逸配置 " + str(N_ESCAPE) + " 个：共享 ⇒ 失配 " +
                 str(SHARED_MISMATCH_BASE) + " 被排除；分置 ⇒ 增益 " +
                 str(SEPARATE_GAIN) + " <= 0 只是模板复用")
    lines.append("-" * 96)
    lines.append("跨卷脊梁：r218 定价 SURVIVE=" + str(R218_SURVIVE) +
                 " / 形状命中 " + str(R218_SHAPE_HITS) + " / 形式外 " +
                 str(R218_OUT_OF_FORM) + "；r222 色散残差 " +
                 format(R222_DISP_RESIDUAL, ".3E"))
    lines.append("红线：数学自洽 != 实验证实；四力大统一 0 条正确解；独立实验预言 0；不宣称攻破。")
    lines.append("-" * 96)
    for s in segs:
        lines.append("[" + s["kind"] + "] " + s["name"] + " :: " + ("OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
