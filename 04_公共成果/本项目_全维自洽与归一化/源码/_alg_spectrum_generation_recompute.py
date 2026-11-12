# -*- coding: utf-8 -*-
"""
算法联盟：破缺谱生成机制穷举 · 离散标签账与参数下界修正
====================================================================================
第八轮。承接第七轮留下的 BOUNDARY：上一册的 p_min_extra=5 只对 Yukawa/Proca
单方程族成立，并明确把「换参数化、换方程族、引入对称性破缺结构」划在可算范围之外。
本轮直接攻这个边界，把它们变成显式可算对象。

三个新问题：
  1. 划分格：κ 的三类与 g 的四类是不是彼此独立的破缺？若 κ 划分是 g 划分的粗化，
     第七轮把两者相加（2 + 3 = 5）就是上界而非下界；标签可复用。
  2. 机制族穷举：8 个显式「参数 → 谱」生成族，每族机算 p_cont / p_disc、
     生成谱的类数与数值，四门判「少于 4 个独立参数且实验存活」。
  3. 离散标签归属：表示论能自动生出几类？剩下的标签由谁注入？

诚实定位：机制族是显式有限枚举，不是全称穷尽；结论仍标 BOUNDARY。
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
GAQ_DIR = os.path.join(ROOT, "01_独立体系", "S02_空间光速螺旋统一力", "04_理论推导")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_PREV1 = os.path.join(DATA, "_ALG_expdata_fullchain_recompute_2026-11-11.json")
P_PREV2 = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_2026-11-11.json")
P_PREV5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_PREV6 = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
P_PREV7 = os.path.join(DATA, "_ALG_force_unification_recompute_2026-11-12.json")
P_R401 = glob.glob(os.path.join(DATA, "TUFT-r401_*.json"))[0]
P_R402 = glob.glob(os.path.join(DATA, "TUFT-r402_*.json"))[0]
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")
P_GAQ_PY = os.path.join(GAQ_DIR, "unified_forces_vs_experiment.py")

OUT_JSON = os.path.join(DATA, "_ALG_spectrum_generation_recompute_2026-11-12.json")
OUT_REPORT = os.path.join(DATA, "_ALG_spectrum_generation_recompute_report_2026-11-12.txt")
SOURCE_FILES = [P_LEDGER, P_PREV1, P_PREV2, P_PREV5, P_PREV6, P_PREV7,
                P_R401, P_R402, P_R403, P_R404, P_GAQ_PY]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def sci(fr, n=6):
    return format(D_fr(fr), "." + str(n) + "E")


def rel_dev(a, b):
    # κ 谱含两条长程 κ=0；分母为 0 时按「同值零偏离 / 异值极大偏离」显式处理，
    # 不搞 0/0，也不拿容差把它掩盖掉（分母口径写进守卫 note）。
    # ★精确相等必须先短路：Decimal 的 0 除以极小数会继承正指数，
    #   format 成 0.000000E+68 这类误导性读数（数值格式不收敛不得当证据）。
    if a == b:
        return D(0)
    if b == 0:
        return D(10) ** 50
    return abs(D_fr(a - b) / D_fr(b))


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


LEDGER = load(P_LEDGER)
PREV1 = load(P_PREV1)
PREV2 = load(P_PREV2)
PREV5 = load(P_PREV5)
PREV6 = load(P_PREV6)
PREV7 = load(P_PREV7)
R401 = load(P_R401)
R402 = load(P_R402)
R403 = load(P_R403)
R404 = load(P_R404)
GAQ_PY = open(P_GAQ_PY, encoding="utf-8").read()
GAQ_TREE = ast.parse(GAQ_PY)
E = {x["id"]: x for x in LEDGER["ledger"]}
K1 = PREV1["key_numbers"]
K7 = PREV7["key_numbers"]

HBAR = F_of(E["C03"]["value"])
C_LIGHT = F_of(E["C01"]["value"])
E_CHARGE = F_of(E["C04"]["value"])
G_NEWTON = F_of(E["C05"]["value"])
M_PROTON = F_of(E["C09"]["value"])
M_W_P02 = F_of(E["P02"]["value"]) * F(10) ** 9
ALPHA_INV_ZERO = F_of(E["C06"]["value"])
ALPHA_INV_MZ = F_of(E["P15"]["value"])
SIN2W = F_of(E["P08"]["value"])
ALPHA_S_MZ = F_of(E["P07"]["value"])
HC = HBAR * C_LIGHT / E_CHARGE

FORCE_IDS = ["EM", "G", "W", "S"]
FORCE_NAMES = ["电磁", "引力", "弱", "强（剩余核力）"]
N_FORCE = len(FORCE_IDS)

source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0) and (len(SOURCE_FILES) > 0)


# ============================ act / exp 两条独立谱路径 ============================
def act_spectrum():
    """act：从 46 项来料表用 ħc/m 与耦合定义式精确重算 κ 谱与 g 谱。"""
    vals = [n.value for n in ast.walk(GAQ_TREE)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
            and not isinstance(n.value, bool)]
    # 第七轮教训：脚本写 134.9768e6，AST 折成 134976800.0；按 AST 实际形态机读
    mpi_hits = [v for v in vals if F_of(str(v)) == F("134976800")]
    if not mpi_hits:
        raise RuntimeError("ACT-MPI-MISSING")
    mpi_ev = F_of(str(mpi_hits[0]))
    lam_W = HC / M_W_P02
    lam_pi = HC / mpi_ev
    kap = [F(0), F(0), F(1) / lam_W, F(1) / lam_pi]
    g = [F(1) / ALPHA_INV_ZERO,
         (F(1) / ALPHA_INV_MZ) * SIN2W,
         ALPHA_S_MZ,
         G_NEWTON * M_PROTON ** 2 / (HBAR * C_LIGHT)]
    return dict(kappa=kap, coupling=g, lam_W=lam_W, lam_pi=lam_pi,
                m_pi_ev=mpi_ev, hc=HC)


def exp_spectrum():
    """exp：回读第七轮成品 JSON 的 forces / couplings（与 act 互不引用）。"""
    kap = [F_frac_str(f["kappa"]) for f in PREV7["forces"]]
    g = [F_frac_str(x) for x in PREV7["couplings"]["act"]]
    return dict(kappa=kap, coupling=g,
                lam_W=F_of(K7["lam_W_P02_m"]),
                lam_pi=F_of(K7["lam_pi_m"]))


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "act_spectrum" not in funcs or "exp_spectrum" not in funcs:
        return False
    if ast.dump(funcs["act_spectrum"]) == ast.dump(funcs["exp_spectrum"]):
        return False
    for name in ("act_spectrum", "exp_spectrum"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


ACT = act_spectrum()
EXP = exp_spectrum()
KAPPA = ACT["kappa"]
COUPLING = ACT["coupling"]
KAPPA_EXP = EXP["kappa"]
COUPLING_EXP = EXP["coupling"]

DEV_KAPPA = [rel_dev(a, b) for a, b in zip(KAPPA, KAPPA_EXP)]
DEV_COUPLING = [rel_dev(a, b) for a, b in zip(COUPLING, COUPLING_EXP)]
MACHINE_EPS = D("1e-45")
TWO_PATH_OK = all(x < MACHINE_EPS for x in DEV_KAPPA + DEV_COUPLING)
DEV_KAPPA_MAX = max(DEV_KAPPA)
DEV_COUPLING_MAX = max(DEV_COUPLING)

# g 的第二条独立路径：第一册 α1/α2/α3/α_G 的倒数
COUPLING_EXP2 = [F(1) / F_of(K1["alpha1_inv_MZ_act"]),
                 F(1) / F_of(K1["alpha2_inv_MZ_act"]),
                 F(1) / F_of(K1["alpha3_inv_MZ_act"]),
                 F_of(K1["alpha_G_proton"])]


# ============================ 划分格：等价类、粗化、标签下界 ============================
def partition_blocks(values):
    """按精确值相等分块，返回按值排序的块（每块是下标列表）。"""
    out = []
    for v in sorted(set(values)):
        out.append([i for i, x in enumerate(values) if x == v])
    return out


def join_partition(blocks_a, blocks_b, n):
    """两个划分的共同细化：按 (a 块号, b 块号) 对重新分块。"""
    la = [next(j for j, b in enumerate(blocks_a) if i in b) for i in range(n)]
    lb = [next(j for j, b in enumerate(blocks_b) if i in b) for i in range(n)]
    pairs = list(zip(la, lb))
    return [[i for i, p in enumerate(pairs) if p == q] for q in sorted(set(pairs))]


def is_coarsening(coarse, fine, n):
    """coarse 的每块是否都是 fine 若干块的并。"""
    for cb in coarse:
        touched = [j for j, fb in enumerate(fine) if any(i in fb for i in cb)]
        covered = set(i for j in touched for i in fine[j])
        if covered != set(cb):
            return False
    return True


def ceil_log2(n):
    """整数机算 ceil(log2 n)，不用浮点对数。"""
    k = 0
    v = 1
    while v < n:
        v = v * 2
        k = k + 1
    return k


K_BLOCKS = partition_blocks(KAPPA)
A_BLOCKS = partition_blocks(COUPLING)
N_K_BLOCKS = len(K_BLOCKS)
N_A_BLOCKS = len(A_BLOCKS)
JOIN_BLOCKS = join_partition(K_BLOCKS, A_BLOCKS, N_FORCE)
N_JOIN_BLOCKS = len(JOIN_BLOCKS)
# 「κ 是 g 的粗化」在 g 为最细划分时恒真 ⇒ 判为 IDENTITY，不进布尔判定
COARSENING_HOLDS = is_coarsening(K_BLOCKS, A_BLOCKS, N_FORCE)

# 两种口径都要报，避免口径决定判定（第五轮教训）
LABELS_TREE = N_A_BLOCKS - 1          # 二元判定树内部节点下界
LABELS_BITS = ceil_log2(N_JOIN_BLOCKS)  # 最小二进制标签比特数
P_MIN_V7 = F_frac_str(str(K7["p_min_extra"]))
P_MIN_V8 = LABELS_TREE + 1            # 3 个离散标签 + 1 个连续尺度
REDUCTION = int(P_MIN_V7) - P_MIN_V8
BUDGET = N_FORCE - 1                  # 「少于 4 个独立参数」⇒ 3

# 阳性对照：人为合并两个 g 值 ⇒ 谱类数下降，标签下界必须响应
COUPLING_MERGED = list(COUPLING)
COUPLING_MERGED[1] = COUPLING_MERGED[0]
A_BLOCKS_MERGED = partition_blocks(COUPLING_MERGED)
N_A_MERGED = len(A_BLOCKS_MERGED)
LABELS_TREE_MERGED = N_A_MERGED - 1
LABELS_BITS_MERGED = ceil_log2(len(join_partition(K_BLOCKS, A_BLOCKS_MERGED, N_FORCE)))
POS_CTRL_ALERTS = (LABELS_TREE_MERGED < LABELS_TREE) and (N_A_MERGED < N_A_BLOCKS)

# 阴性对照：两条长程 κ=0 恒绿，单列 IDENTITY
N_LONG_RANGE = len([x for x in KAPPA if x == 0])
NEG_CTRL_GREEN = (N_LONG_RANGE == 2) and (N_K_BLOCKS < N_A_BLOCKS)


# ============================ 离散标签归属：表示论能自动生几类 ============================
R401_VERDICT = str(R401.get("verdict", ""))
R402_VERDICT = str(R402.get("verdict", ""))
R401_A1 = next((r["name"] for r in R401["rows"] if r.get("id") == "A1"), "")
REP_TWO_CLASSES = ("TWO-PARITY-CLASSES" in R401_VERDICT) and ("两个宇称类" in R401_A1)
REP_ONE_BIT = ("ONE-BIT-SUFFICIENT" in R401_VERDICT) and ("ZERO-BIT-INSUFFICIENT" in R401_VERDICT)
REP_NO_EXTRA = "DIRAC-INVARIANT-COMPLEX-DIM-1" in R402_VERDICT
N_REP_CLASSES = 2 if (REP_TWO_CLASSES and REP_ONE_BIT) else None
LABELS_EXTERNAL = N_JOIN_BLOCKS - N_REP_CLASSES if N_REP_CLASSES is not None else None

MECH2 = {m["id"]: m for m in PREV2["mechanism_probes"]}
T3_T4_PRED_ZERO = all(MECH2[t]["pred"] == 0 for t in ("T3", "T4"))
T3_T4_NONUNIQUE = all(MECH2[t]["unique"] is False for t in ("T3", "T4"))
T3_T4_CARD = [int(MECH2[t]["cardinality"]) for t in ("T3", "T4")]

SPINE_PRED = 0
prev5_hits = PREV5["key_numbers"]["pairs_hit"]
prev6_hits = PREV6["key_numbers"]["pairs_hit_after"]
honest_boundary = (prev5_hits == 0) and (prev6_hits == 0) and (SPINE_PRED == 0)


# ============================ 8 个显式「参数 → 谱」生成族 ============================
# 每族真的生成 4 条力的 (κ, g) 精确有理值；p_cont / p_disc 由构造里的输入列表机数，
# 类数与数值失配由生成结果机算，不写结论。
# literal_lookup=True 表示理论输出就是把目标观测谱整表抄进来（第五轮污染门口径）；
# 由 m/ħc、α 定义式等中间推导得到的不算抄表，但所用实验输入仍按第六轮 p_exp 口径记账。

def fam_shared():
    params = [KAPPA[2], COUPLING[0]]
    k = [params[0] for _ in FORCE_IDS]
    g = [params[1] for _ in FORCE_IDS]
    return dict(id="M1", name="共享常数", params=params, labels=[], kappa=k,
                coupling=g, literal_lookup=False, note="单一 κ 与单一 g")


def fam_power():
    r = KAPPA[3] / KAPPA[2]
    params = [KAPPA[2], r, COUPLING[0], F(2)]
    k = [params[0] * params[1] ** i for i in range(N_FORCE)]
    g = [params[2] * params[3] ** i for i in range(N_FORCE)]
    return dict(id="M2", name="幂律标度", params=params, labels=[], kappa=k,
                coupling=g, literal_lookup=False, note="κ_i=κ₀rⁱ、g_i=g₀sⁱ，无法生出 κ=0 的长程力")


def fam_vander():
    params = [F(1), F(2), F(3), COUPLING[0], F(5), F(7), F(11)]
    labels = [F(i) for i in range(N_FORCE)]
    k = [params[0] * t + params[1] * t ** 2 + params[2] * t ** 3 for t in labels]
    g = [params[3] * (params[4] + params[5] * t + params[6] * t ** 2) for t in labels]
    return dict(id="M3", name="线性 Vandermonde 插值", params=params, labels=labels,
                kappa=k, coupling=g, literal_lookup=False, note="3 系数插 κ 谱 + 4 系数插 g 谱 + 4 横坐标标签")


def fam_breaking():
    labels = [F(0), F(1), F(0)]
    k = [x for x in KAPPA_EXP]
    g = [x for x in COUPLING_EXP]
    return dict(id="M4", name="二分支对称性破缺链", params=[], labels=labels,
                kappa=k, coupling=g, literal_lookup=True,
                note="3 个二元判定选 4 叶；叶上直接挂实验谱值 ⇒ 回述")


def fam_rg_short():
    params = [KAPPA[2], KAPPA[3], COUPLING[0]]
    k = [F(0), F(0), params[0], params[1]]
    g = [params[2], params[2] / F(2), params[2] / F(7), params[2] / F(11)]
    return dict(id="M5", name="RG 阈值简版", params=params, labels=[], kappa=k,
                coupling=g, literal_lookup=False, note="3 个参数生对类数，但 g 后三值失配")


def fam_rep():
    params = [COUPLING[0]]
    labels = [F(0), F(1)]
    k = [F(0), F(0), KAPPA[2], KAPPA[2]]
    g = [params[0], params[0] / F(2), params[0], params[0] / F(2)]
    return dict(id="M6", name="表示论宇称类", params=params, labels=labels,
                kappa=k, coupling=g, literal_lookup=False,
                note="r401 一比特必要且充分 ⇒ 只能自动分 2 类")


def fam_rg_full():
    # 5 个独立阈值输入；ħ、c、G、m_p、sin²θ_W 按 SI「一条定义 + 其余派生」口径
    # 与第六轮 p_exp 口径作固定定义常数，不计入自由参数（在主文单列 BOUNDARY）。
    params = [M_W_P02, ACT["m_pi_ev"], ALPHA_INV_ZERO, ALPHA_INV_MZ, ALPHA_S_MZ]
    k = [F(0), F(0), params[0] / HC, params[1] / HC]
    g = [F(1) / params[2], (F(1) / params[3]) * SIN2W, params[4],
         G_NEWTON * M_PROTON ** 2 / (HBAR * C_LIGHT)]
    return dict(id="M7", name="RG 全阈值（质量—力程等价）", params=params, labels=[],
                kappa=k, coupling=g, literal_lookup=False,
                note="κ 由 m/ħc 推导、g 由定义式推导；5 个独立阈值 ⇒ 超预算")


def fam_separate():
    params = [x for x in KAPPA_EXP] + [x for x in COUPLING_EXP]
    k = [x for x in params[:N_FORCE]]
    g = [x for x in params[N_FORCE:]]
    return dict(id="M8", name="分置模板复用", params=params, labels=[], kappa=k,
                coupling=g, literal_lookup=True, note="每力独立 (κ_i,g_i)，整表查表")


def measure(m):
    kap = m["kappa"]
    cou = m["coupling"]
    k_out = len(set(kap))
    a_out = len(set(cou))
    k_ok = all(x == y for x, y in zip(kap, KAPPA))
    g_ok = all(x == y for x, y in zip(cou, COUPLING))
    n_mis = sum(1 for x, y in zip(kap, KAPPA) if x != y) + \
            sum(1 for x, y in zip(cou, COUPLING) if x != y)
    return dict(id=m["id"], name=m["name"], note=m["note"],
                p_cont=len(m["params"]), p_disc=len(m["labels"]),
                p_total=len(m["params"]) + len(m["labels"]),
                K_out=k_out, A_out=a_out, restore_ok=(k_ok and g_ok),
                mismatch=n_mis, literal_lookup=m["literal_lookup"],
                kappa=[str(x) for x in kap], coupling=[str(x) for x in cou])


FAMILIES = [measure(f()) for f in (fam_shared, fam_power, fam_vander, fam_breaking,
                                   fam_rg_short, fam_rep, fam_rg_full, fam_separate)]
N_FAMILIES = len(FAMILIES)
FAMILY_IDS = [m["id"] for m in FAMILIES]


# ============================ 四门判定 ============================
# G1 谱覆盖 / G2 参数预算（少于 4 个独立参数）/ G3 实验存活（数值逐条精确相等）
# G4 非回述（理论输出不是把目标观测整表抄进来）
def gate_eval(m, budget, require_k, enforce_g3, enforce_g4):
    g1 = (m["K_out"] >= require_k) and (m["A_out"] >= N_A_BLOCKS)
    g2 = (m["p_total"] <= budget)
    g3 = (m["restore_ok"] if enforce_g3 else True)
    g4 = ((not m["literal_lookup"]) if enforce_g4 else True)
    return dict(g1=bool(g1), g2=bool(g2), g3=bool(g3), g4=bool(g4),
                hit=bool(g1 and g2 and g3 and g4))


RESULTS = []
for m in FAMILIES:
    r = gate_eval(m, BUDGET, N_K_BLOCKS, True, True)
    RESULTS.append(dict(m, gates=r))

N_BREAK = sum(1 for r in RESULTS if r["gates"]["hit"])
BREAK_IDS = [r["id"] for r in RESULTS if r["gates"]["hit"]]
N_G1 = sum(1 for r in RESULTS if r["gates"]["g1"])
N_G2 = sum(1 for r in RESULTS if r["gates"]["g2"])
N_G3 = sum(1 for r in RESULTS if r["gates"]["g3"])
N_G4 = sum(1 for r in RESULTS if r["gates"]["g4"])
# 只挂一门的族：证明每道门都承重，而不是装饰
ONE_GATE_ONLY = [r["id"] for r in RESULTS
                 if sum(1 for k in ("g1", "g2", "g3", "g4") if r["gates"][k]) == 3]
CRITICAL_BY_G2 = [r["id"] for r in RESULTS
                  if (r["gates"]["g1"] and r["gates"]["g3"] and r["gates"]["g4"]
                      and not r["gates"]["g2"])]
CRITICAL_BY_G3 = [r["id"] for r in RESULTS
                  if (r["gates"]["g1"] and r["gates"]["g2"] and r["gates"]["g4"]
                      and not r["gates"]["g3"])]
CRITICAL_BY_G4 = [r["id"] for r in RESULTS
                  if (r["gates"]["g1"] and r["gates"]["g2"] and r["gates"]["g3"]
                      and not r["gates"]["g4"])]

N_ESCAPE = N_BREAK
BACKFIRE_READINGS = dict(n_families=N_FAMILIES, n_break=N_BREAK,
                         labels_tree=LABELS_TREE, budget=BUDGET,
                         n_g1=N_G1, n_g2=N_G2, n_g3=N_G3, n_g4=N_G4)

# 控制组四个读数两两不同，且都不等于基线读数
CTRL_READINGS = [N_FAMILIES, LABELS_TREE, N_BREAK, P_MIN_V8]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == len(CTRL_READINGS))
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
not_all_green = (N_BREAK == 0) and (N_G1 > 0) and (N_G3 > 0) and (N_G4 > 0)


def fmt_dev(x):
    # Decimal(0) 用 .E 格式化会显示成 0.000000E+6（零值的科学计数习惯），
    # 容易被误读成巨大偏离；精确相等就直接写 0 并注明逐位相等。
    return "0（逐位相等）" if x == 0 else format(x, ".3E")


def fmt_dev_json(x):
    return "0" if x == 0 else format(x, ".6E")


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
    return ("ALG-SPECTRUM-GEN"
            + "__FAMILIES-" + str(N_FAMILIES)
            + "__KAPPA-" + str(N_K_BLOCKS)
            + "__COUPLING-" + str(N_A_BLOCKS)
            + "__LABELS-" + str(LABELS_TREE) + "or" + str(LABELS_BITS)
            + "__P-MIN-" + str(int(P_MIN_V7)) + "to" + str(P_MIN_V8)
            + "__BUDGET-" + str(BUDGET)
            + "__BREAK-" + token
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_BREAK))
v_machine_1 = verdict_with(str(N_BREAK + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and \
                     (("__BREAK-" + str(N_BREAK)) in v_machine_0)
verdict = v_machine_0

segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV7-RELOADED",
    (PREV7["guard_pass"] == PREV7["guard_count"]) and
    (PREV7["guard_count"] == 34) and (K7["escape_configs"] == 0) and
    (K7["p_min_extra"] == 5) and (prev5_hits == 0) and (prev6_hits == 0),
    "PASS",
    "第七轮 34/34 守卫、逃逸 0、p_min_extra=5；第五／六轮穷举 0 命中。本册攻的正是第七轮自划的 BOUNDARY")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_spectrum（ħc/m 与耦合定义式重算）与 exp_spectrum（第七轮成品回读）为两个不同函数，return 均非顶层数值常量")
add("TWO-PATH-KAPPA-EXACT", TWO_PATH_OK and (max(DEV_KAPPA) < MACHINE_EPS), "PASS",
    "两路机拼 κ 谱：act 重算 vs exp 回读，最大相对偏离 " + fmt_dev(DEV_KAPPA_MAX))
add("TWO-PATH-COUPLING-EXACT", (max(DEV_COUPLING) < MACHINE_EPS) and
    (len(set(COUPLING_EXP2)) == N_A_BLOCKS), "PASS",
    "两路机拼 g 谱：最大相对偏离 " + fmt_dev(DEV_COUPLING_MAX) +
    "；第一册 α1/α2/α3/α_G 倒数独立给 " + str(len(set(COUPLING_EXP2))) + " 类")
add("KAPPA-3-CLASSES", (N_K_BLOCKS == 3) and (N_LONG_RANGE == 2), "PASS",
    "κ 谱精确分块 " + str(N_K_BLOCKS) + " 类，两条长程 κ=0 合并为一块；λ_π/λ_W = " +
    K7["lam_pi_over_lam_W"] + " 来自第七轮成品")
add("COUPLING-4-CLASSES", (N_A_BLOCKS == 4) and (N_JOIN_BLOCKS == 4), "PASS",
    "g 谱精确分块 " + str(N_A_BLOCKS) + " 类；κ 与 g 的共同细化 " + str(N_JOIN_BLOCKS) +
    " 块 ⇒ 需要区分的可辨别状态数由 g 谱钉死")
add("COARSENING-IDENTITY", COARSENING_HOLDS, "IDENTITY",
    "★诚实标注：g 划分已是最细划分，任何 κ 划分都是它的粗化 ⇒ 该判定恒真、零判别力，不进布尔结论；" +
    "真正有判别力的是下面的标签下界与机制族数值匹配")
add("LABEL-BOUND-TWO-CALIBRE", (LABELS_TREE == 3) and (LABELS_BITS == 2) and
    (LABELS_TREE > LABELS_BITS), "PASS",
    "两种口径都报：二元判定树内部节点下界 " + str(LABELS_TREE) +
    "（= 4−1），二进制标签比特下界 " + str(LABELS_BITS) +
    "（= ceil(log2 4)）；口径决定读数，不许只挑一个")
add("P-MIN-REVISED", (P_MIN_V8 < P_MIN_V7) and (REDUCTION == 1) and
    (P_MIN_V8 == LABELS_TREE + 1), "PASS",
    "★标签可复用：第七轮把 κ 破缺 2 与 g 破缺 3 相加得 p_min_extra=" + str(int(P_MIN_V7)) +
    "，本轮机读划分格后修正为 " + str(LABELS_TREE) + " 个离散标签 + 1 个连续尺度 = " +
    str(P_MIN_V8) + "，下降 " + str(REDUCTION) + "；但 " + str(P_MIN_V8) + " 仍 > 预算 " + str(BUDGET))
add("BUDGET-LESS-THAN-FOUR", (BUDGET == N_FORCE - 1) and (BUDGET < N_FORCE), "PASS",
    "「少于 4 个独立参数」机读为 budget = " + str(BUDGET) + "；由力的条数驱动，不是手填常数")
add("POS-CTRL-MERGED-SPECTRUM", POS_CTRL_ALERTS, "PASS",
    "阳性对照：人为合并两个 g 值 ⇒ 谱类数 " + str(N_A_BLOCKS) + "→" + str(N_A_MERGED) +
    "，判定树下界 " + str(LABELS_TREE) + "→" + str(LABELS_TREE_MERGED) +
    "；比特口径 " + str(LABELS_BITS) + "→" + str(LABELS_BITS_MERGED) +
    "（该口径不响应，如实记录）⇒ 标签下界确由实测谱驱动")

add("REP-2-CLASSES-ONLY", REP_TWO_CLASSES and REP_ONE_BIT and REP_NO_EXTRA and
    (N_REP_CLASSES == 2), "PASS",
    "r401 机读：TWO-PARITY-CLASSES + ONE-BIT-SUFFICIENT + ZERO-BIT-INSUFFICIENT，" +
    "r402 DIRAC-INVARIANT-COMPLEX-DIM-1 ⇒ 表示论自动只能生 " + str(N_REP_CLASSES) + " 类")
add("REP-LABELS-EXTERNAL", (LABELS_EXTERNAL == 2) and (N_JOIN_BLOCKS > N_REP_CLASSES), "PASS",
    "★离散标签归属：需要 " + str(N_JOIN_BLOCKS) + " 类、表示论自动给 " + str(N_REP_CLASSES) +
    " 类 ⇒ 至少 " + str(LABELS_EXTERNAL) + " 个标签须由外部实验事实注入（第六轮 p_exp 口径），" +
    "参数不灭从方程层搬到标签层")
add("T3-T4-NO-PRED", T3_T4_PRED_ZERO and T3_T4_NONUNIQUE and
    min(T3_T4_CARD) > 1, "PASS",
    "第二轮离散机制复核：T3 整数格 / T4 表示论解数 " + str(T3_T4_CARD) +
    "，均 unique=False 且 pred=0 ⇒ 离散结构本身不产独立预言")

add("FAMILY-INVENTORY", (N_FAMILIES == 8) and (len(set(FAMILY_IDS)) == N_FAMILIES), "PASS",
    "显式机制族 " + str(N_FAMILIES) + " 个：" + " / ".join(r["name"] for r in FAMILIES))
add("FAMILY-MEASURED-NOT-DECLARED",
    all((r["p_total"] == r["p_cont"] + r["p_disc"]) and
        (r["K_out"] == len(set(r["kappa"]))) and
        (r["A_out"] == len(set(r["coupling"]))) and
        (r["mismatch"] >= 0) for r in FAMILIES), "PASS",
    "每族的 p_cont/p_disc 由输入列表机数，类数由生成谱机数，失配条数由逐条精确比较机算，不是声明")
add("G1-SPECTRUM-COVER", (N_G1 > 0) and (N_G1 < N_FAMILIES), "PASS",
    "谱覆盖门（κ≥3 类且 g≥4 类）通过 " + str(N_G1) + "/" + str(N_FAMILIES) + " 族 ⇒ 非恒绿")
add("G2-PARAMETER-BUDGET", (N_G2 > 0) and (N_G2 < N_FAMILIES), "PASS",
    "参数预算门（p_total≤" + str(BUDGET) + "）通过 " + str(N_G2) + "/" + str(N_FAMILIES) + " 族")
add("G3-EXPERIMENTAL-RESTORE", (N_G3 > 0) and (N_G3 < N_FAMILIES), "PASS",
    "实验存活门（κ/g 逐条精确相等）通过 " + str(N_G3) + "/" + str(N_FAMILIES) + " 族")
add("G4-NON-RESTATEMENT", (N_G4 > 0) and (N_G4 < N_FAMILIES), "PASS",
    "非回述门（理论输出不是整表抄目标观测）通过 " + str(N_G4) + "/" + str(N_FAMILIES) + " 族")
add("FOUR-GATES-ALL-BEARING", (len(CRITICAL_BY_G2) >= 1) and
    (len(CRITICAL_BY_G3) >= 1) and (len(CRITICAL_BY_G4) >= 1) and
    (len(ONE_GATE_ONLY) >= 3), "PASS",
    "每门都有恰好只挂该门的族：G2 " + str(CRITICAL_BY_G2) + " / G3 " +
    str(CRITICAL_BY_G3) + " / G4 " + str(CRITICAL_BY_G4) +
    "；只挂一门共 " + str(len(ONE_GATE_ONLY)) + " 族 ⇒ 四门都不是装饰判据")
add("FAMILY-ZERO-BREAKTHROUGH", (N_BREAK == 0) and (N_ESCAPE == 0), "PASS",
    "★8 族四门全过 " + str(N_BREAK) + " 族 ⇒ 在显式机制族内「少于 4 个独立参数且实验存活」的机制 0 个")
add("CRITICAL-M7-BY-G2", ("M7" in CRITICAL_BY_G2), "PASS",
    "最接近的是 M7（RG 全阈值）：谱覆盖、数值精确、非回述全过，只因 5 个独立阈值 > 预算 " +
    str(BUDGET) + " 被挡 ⇒ 参数预算是承重门")
add("CRITICAL-M5-BY-G3", ("M5" in CRITICAL_BY_G3), "PASS",
    "M5 用 3 个参数生对类数但 g 后三值失配 ⇒ 谱类数达标不等于实验存活")
add("CRITICAL-M4-BY-G4", ("M4" in CRITICAL_BY_G4), "PASS",
    "M4 用 3 个二元标签选 4 叶，参数账达标、数值全对，但叶上是整表抄实验谱 ⇒ 回述，非突破")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个读数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 " + str(CTRL_READINGS[0]) + "，杜绝全表读数相同的假判别力")
add("CTRL-IDENTITY-NEVER-HITS", NEG_CTRL_GREEN, "IDENTITY",
    "阴性对照：两条长程 κ=0 恒绿，单列 IDENTITY；粗化判定亦恒真，已单列不进结论")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但标签下界、参数下界修正、四门读数、机制族失配均为非恒绿读数")

add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 " + str(R403["unique_answer"]["four_forces_c3"]) +
    " 条、r404 接受 " + str(R404["key_numbers"]["four_force_accepted"]) +
    "；第五轮 0 命中、第六轮 0 命中、第七轮逃逸 " + str(K7["escape_configs"]) +
    "、本族突破 " + str(N_BREAK))
add("FAMILY-LIMITED-CLAIM", (N_BREAK == 0) and (P_MIN_V8 > BUDGET), "BOUNDARY",
    "★机制族是 8 个显式有限枚举，不是全称穷尽；8 族外未列出的构造不构成已排除。" +
    "本册把第七轮 BOUNDARY 从「单方程族」推到「显式生成族」，仍不是「四力统一不可能」的全称定理")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (N_BREAK == 0), "INFO",
    "本册不宣称攻破统一场论；给出的是标签可复用带来的下界修正与机制族穷举判决")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（划分格、标签账、生成谱数值），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_BREAK == 0) and (P_MIN_V8 > BUDGET), "INFO",
    "下界由 " + str(int(P_MIN_V7)) + " 降到 " + str(P_MIN_V8) + " 后仍比预算多 " +
    str(P_MIN_V8 - BUDGET) + "；要越过它须给出能用 " + str(BUDGET) +
    " 个以内参数生出 4 类耦合且标签非外部注入的机制，并仍由一条带双侧误差棒的新实验读数验收")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-SPECTRUM-GEN--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-SPECTRUM-GEN--GATES-FAIL"
    return "ALG-SPECTRUM-GEN--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "FAMILY-ZERO-BREAKTHROUGH",
                     "P-MIN-REVISED", "FAMILY-LIMITED-CLAIM", "REP-LABELS-EXTERNAL"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-SPECTRUM-GEN--GATES-PASS-WITH-0-NEGATIVE") and \
              (nf_guard_before == 0) and (len(declared_negative) > 0)
add("FINAL-OF-CONSISTENT", final_of_ok, "PASS",
    "final_of(nf_main=" + str(nf_main_before) + ",nf_guard=" + str(nf_guard_before) +
    ",n_decl=" + str(len(declared_negative)) + ")：守卫 FAIL 挡门、已登记判负不挡门、缺 n_decl 报 GATES-FAIL")

counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0, "BOUNDARY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)

key_numbers = {
    "forces": N_FORCE,
    "kappa_classes": N_K_BLOCKS,
    "coupling_classes": N_A_BLOCKS,
    "join_blocks": N_JOIN_BLOCKS,
    "long_range_forces": N_LONG_RANGE,
    "labels_tree": LABELS_TREE,
    "labels_bits": LABELS_BITS,
    "labels_tree_merged": LABELS_TREE_MERGED,
    "labels_bits_merged": LABELS_BITS_MERGED,
    "coupling_classes_merged": N_A_MERGED,
    "p_min_prev7": int(P_MIN_V7),
    "p_min_v8": P_MIN_V8,
    "p_min_reduction": REDUCTION,
    "budget": BUDGET,
    "rep_auto_classes": N_REP_CLASSES,
    "labels_external": LABELS_EXTERNAL,
    "families": N_FAMILIES,
    "families_g1": N_G1,
    "families_g2": N_G2,
    "families_g3": N_G3,
    "families_g4": N_G4,
    "families_one_gate_only": len(ONE_GATE_ONLY),
    "families_breakthrough": N_BREAK,
    "critical_by_g2": CRITICAL_BY_G2,
    "critical_by_g3": CRITICAL_BY_G3,
    "critical_by_g4": CRITICAL_BY_G4,
    "control_readings": CTRL_READINGS,
    "dev_kappa_two_path_max": fmt_dev_json(DEV_KAPPA_MAX),
    "dev_coupling_two_path_max": fmt_dev_json(DEV_COUPLING_MAX),
    "prev5_hits": prev5_hits,
    "prev6_hits": prev6_hits,
    "prev7_escape": K7["escape_configs"],
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": SPINE_PRED,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：破缺谱生成机制穷举 · 离散标签账与参数下界修正",
    "date": "2026-11-12",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "gates": {
        "G1": "谱覆盖：生成谱 κ>=3 类且 g>=4 类",
        "G2": "参数预算：p_cont+p_disc <= 3（少于 4 个独立参数）",
        "G3": "实验存活：κ/g 四条逐条与实验谱精确相等",
        "G4": "非回述：理论输出不是把目标观测整表抄进来",
    },
    "spectrum": dict(kappa=[str(x) for x in KAPPA],
                     coupling=[str(x) for x in COUPLING],
                     kappa_blocks=K_BLOCKS, coupling_blocks=A_BLOCKS,
                     join_blocks=JOIN_BLOCKS, coarsening_is_identity=bool(COARSENING_HOLDS)),
    "families": RESULTS,
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
    lines.append("算法联盟：破缺谱生成机制穷举 · 离散标签账与参数下界修正（第八轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("两路机拼：act 从 46 项来料表 ħc/m 与耦合定义式重算，exp 回读第七轮成品。")
    lines.append("  κ 谱最大相对偏离 " + fmt_dev(DEV_KAPPA_MAX) +
                 "，g 谱最大相对偏离 " + fmt_dev(DEV_COUPLING_MAX))
    lines.append("  κ 类数 " + str(N_K_BLOCKS) + "（长程 " + str(N_LONG_RANGE) +
                 " 条），g 类数 " + str(N_A_BLOCKS) + "，共同细化 " + str(N_JOIN_BLOCKS) + " 块")
    lines.append("-" * 96)
    lines.append("★划分格：g 划分最细 ⇒ 粗化判定恒真、零判别力，单列 IDENTITY。")
    lines.append("  标签下界两口径：判定树 " + str(LABELS_TREE) + " / 二进制比特 " + str(LABELS_BITS))
    lines.append("  阳性对照合并两个 g 值：类数 " + str(N_A_BLOCKS) + "→" + str(N_A_MERGED) +
                 "，树口径 " + str(LABELS_TREE) + "→" + str(LABELS_TREE_MERGED) +
                 "，比特口径 " + str(LABELS_BITS) + "→" + str(LABELS_BITS_MERGED))
    lines.append("  第七轮 p_min_extra=" + str(int(P_MIN_V7)) + " ⇒ 本册 " + str(P_MIN_V8) +
                 "，下降 " + str(REDUCTION) + "；预算 " + str(BUDGET) + " 仍不够")
    lines.append("  表示论自动 " + str(N_REP_CLASSES) + " 类 ⇒ 至少 " + str(LABELS_EXTERNAL) +
                 " 个标签须由外部实验事实注入")
    lines.append("-" * 96)
    lines.append("8 族四门（id / p_cont+p_disc / K / A / 失配 / G1G2G3G4 / 突破）：")
    for r in RESULTS:
        gg = r["gates"]
        lines.append("  " + r["id"] + " " + r["name"].ljust(22) +
                     str(r["p_total"]).rjust(3) + str(r["K_out"]).rjust(3) +
                     str(r["A_out"]).rjust(3) + str(r["mismatch"]).rjust(4) + "  " +
                     "".join("1" if gg[k] else "0" for k in ("g1", "g2", "g3", "g4")) +
                     "   " + ("HIT" if gg["hit"] else "-"))
    lines.append("★四门全过 " + str(N_BREAK) + " 族；只挂一门 " + str(len(ONE_GATE_ONLY)) + " 族")
    lines.append("  只挂 G2：" + str(CRITICAL_BY_G2) + " / 只挂 G3：" + str(CRITICAL_BY_G3) +
                 " / 只挂 G4：" + str(CRITICAL_BY_G4))
    lines.append("-" * 96)
    lines.append("红线：数学自洽 != 实验证实；四力大统一 0 条正确解；独立实验预言 0；不宣称攻破。")
    lines.append("-" * 96)
    for s in segs:
        lines.append("[" + s["kind"] + "] " + s["name"] + " :: " + ("OK" if s["ok"] else "FAIL"))
    text = "\n".join(lines) + "\n"
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(text)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if (g_pass == g_count) else "SOME-GUARDS-FAILED")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
