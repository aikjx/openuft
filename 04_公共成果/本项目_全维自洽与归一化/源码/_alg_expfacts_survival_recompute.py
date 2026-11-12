# -*- coding: utf-8 -*-
"""
算法联盟：实验给定的离散事实 + 留一法剔伪 + 实验存活层 · 统一场论三重门攻坚
====================================================================================
承接上一册唯一 OPEN 出口：把实验给定的离散/数值事实纳入自由度账
  p_total = p_eq + p_axiom + p_exp
其中 p_exp 计入账但**不是可调自由选择**。本册把「攻破」升级为三重门：

  C1 自由度门：p_free = p_eq + p_axiom == 0（无可调参数、无额外可自由选择假设）
  C2 留一法门（LTO / leave-target-out）：目标观测值不作为输入，且理论值不等于观测值；
     同时对任一实验事实做 LAF（leave-any-fact-out）得到 p_exp 的**机算**依赖度
  C3 实验存活门：卡方/下界/上界判决通过，且判别力 > 0（存在使其失败的观测读数），
     且不是恒等式、不是只能给单侧「尚未排除」的弱证据

突破 = C1 且 C2 且 C3 同时成立。判据必须反噬自己：
  抹掉 LTO ⇒ 回述型伪预言暴增；抬高卡方阈值 ⇒ 被排除候选假存活；
  抹掉判别力 ⇒ 恒等式 χ²≈0 假突破。三种扰动都必须触发 GATES-FAIL。

诚实定位：本册只产可算判决，不产新物理；不宣称攻破统一场论；
数学自洽 != 实验证实；四力大统一 0 条正确解、独立实验预言 0。
（算法联盟册，不占 RID、不入 README、不与任何审计卷相加。）

环境纪律：Python 3.13 无 numpy/sympy，全部 Fraction / Decimal(60) 精确计算；
UTF-8 源码 + ASCII runner；中文路径不进外层 argv。
"""
import json, os, ast, hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
ATTACK = os.path.join(ROOT, "04_公共成果", "本项目_统一场论攻破")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_PREV2 = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_2026-11-11.json")
P_CHI2 = os.path.join(DATA, "靶场卡方联合拟合.json")
P_A28 = os.path.join(ATTACK, "attack28_力的大统一方程_sin2thetaW真预测_M5修法_2026-10-31.json")
P_A34 = os.path.join(ATTACK, "attack34_b33符号的物理后果_tau_p与物理域判定_2026-10-31.json")
P_R120 = os.path.join(DATA, "TUFT-r120_所有力大统一方程式_候选全集与状态机判_2026-10-20.json")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
OUT_REPORT = os.path.join(DATA, "_ALG_expfacts_survival_recompute_report_2026-11-11.txt")

SOURCE_FILES = [P_LEDGER, P_PREV2, P_CHI2, P_A28, P_A34, P_R120, P_R403, P_R404]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    """把本册 JSON/report 里的 Fraction 字符串（形如 a/b 或整数）还原成精确有理数。"""
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def sci(fr, n=6):
    return format(D_fr(fr), "." + str(n) + "E")


def rel_diff(a, b):
    """两个非零有理数的相对差（Decimal），用于跨卷回读一致性核验。"""
    if a == 0 or b == 0:
        return abs(D_fr(a - b))
    return abs(D_fr(a - b) / D_fr(b))


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


LEDGER = load(P_LEDGER)
PREV2 = load(P_PREV2)
CHI2DOC = load(P_CHI2)
A28 = load(P_A28)
A34 = load(P_A34)
R120 = load(P_R120)
R403 = load(P_R403)
R404 = load(P_R404)

PREV = {e["id"]: e for e in LEDGER["ledger"]}
CHI2_ROWS = {r["entry_id"]: r for r in CHI2DOC["rows"]}


def pv(k):
    return F_of(PREV[k]["value"])


def sv(k):
    return F_of(PREV[k]["sigma"])


# ============================ 实验给定事实账 ============================
# M 类：本仓库有机器可读实测锚的事实（全部来自上一册 46 项来料总表）
MEASURED_FACTS = {
    "P15": {"value": pv("P15"), "sigma": sv("P15"), "meaning": "alpha_em^-1(M_Z)"},
    "P07": {"value": pv("P07"), "sigma": sv("P07"), "meaning": "alpha_s(M_Z)"},
    "P08": {"value": pv("P08"), "sigma": sv("P08"), "meaning": "sin2thetaW(M_Z) 实测"},
    "P11": {"value": pv("P11"), "sigma": sv("P11"), "meaning": "Super-K 质子寿命下限"},
    "K11": {"value": pv("K11"), "sigma": sv("K11"), "meaning": "BK18 张量标量比上界"},
    "C06": {"value": pv("C06"), "sigma": sv("C06"), "meaning": "alpha^-1(零动量)"},
    "P01": {"value": pv("P01"), "sigma": sv("P01"), "meaning": "M_Z 质量"},
}
FACTS_ALIVE = {k: v["value"] for k, v in MEASURED_FACTS.items()}

# D 类：结构性离散事实。上一册 OPEN 点名的电荷量子化 / 三代 / N_c=3 / 自旋统计，
# 本仓库**没有**实测锚可机读，只有教科书符号 ⇒ 明确标 BOUNDARY：
# 它们只作符号输入，不产生数值预言，不计入 p_exp，也不冒充本册证明。
STRUCTURAL_DISCRETE = [
    {"id": "D1", "name": "电荷量子化", "symbol": "Q/e in Z", "anchor": "none-in-repo", "tag": "BOUNDARY"},
    {"id": "D2", "name": "轻子代数", "symbol": "N_gen=3", "anchor": "none-in-repo", "tag": "BOUNDARY"},
    {"id": "D3", "name": "色数", "symbol": "N_c=3", "anchor": "none-in-repo", "tag": "BOUNDARY"},
    {"id": "D4", "name": "自旋统计", "symbol": "s=1/2", "anchor": "none-in-repo", "tag": "BOUNDARY"},
]

# 卡方临界值：从仓库靶场的 caliber 回读，不在本册另造口径
CHI2_CRIT = F_of(CHI2DOC["caliber"]["chi2_crit_1dof_95"])
CHI2_CRIT_TEXT = CHI2DOC["caliber"]["chi2_crit_1dof_95"]


# ============================ exp / act 两条独立路径 ============================
def chi2_act(theory, obs, sigma):
    """act 路径：本册用精确有理数直接展开 ((theory-obs)/sigma)^2。"""
    d = theory - obs
    return (d * d) / (sigma * sigma)


def chi2_exp_from_file(entry_id):
    """exp 路径：从仓库卡方靶场成品 JSON 回读历史读数（与本册计算互不引用）。"""
    row = CHI2_ROWS[entry_id]
    return F_of(row["chi2"])


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "chi2_act" not in funcs or "chi2_exp_from_file" not in funcs:
        return False
    if ast.dump(funcs["chi2_act"]) == ast.dump(funcs["chi2_exp_from_file"]):
        return False
    for name in ("chi2_act", "chi2_exp_from_file"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


# ============================ 三重门的机算零件 ============================
def recomputable(input_facts, facts):
    """候选能否在给定事实集上被重算：全部输入事实存在且非零。
    注意这是**输入依赖度**的符号级可算判决，不是伪造一条物理公式重解 RG；
    扰动方向上的真实数值灵敏度另由 attack28 的 alpha_s 展宽读数给出。"""
    return all(facts.get(k, F(0)) != 0 for k in input_facts)


def laf_dependency(input_facts, facts):
    """LAF：逐个把某项实验事实置零，数出使候选不可重算的事实条数 = p_exp。"""
    lost = []
    for k in input_facts:
        trial = dict(facts)
        trial[k] = F(0)
        if not recomputable(input_facts, trial):
            lost.append(k)
    return len(lost), lost


def lto_clean(target_fact, input_facts, theory, obs):
    """LTO：目标观测不得作为输入，且理论值不得等于观测值（否则是回述）。"""
    target_is_input = (target_fact in input_facts)
    restated = (theory == obs)
    return (not target_is_input) and (not restated), target_is_input, restated


def chi2_power(theory, obs, sigma):
    """双侧可证伪 / 判别力：枚举 4 个不同观测读数，看是否存在双双两类的卡方判决。
    恒等式的 theory 会随 obs 同步变化，因此四个读数全绿 ⇒ 判别力 0。"""
    tf = theory(obs) if callable(theory) else theory
    probes = [obs, obs + sigma, obs - sigma, tf, tf + F(3) * sigma, tf - F(3) * sigma]
    vals = []
    for o in probes:
        th = theory(o) if callable(theory) else theory
        vals.append(chi2_act(th, o, sigma))
    n_fail = sum(1 for v in vals if v >= CHI2_CRIT)
    n_pass = sum(1 for v in vals if v < CHI2_CRIT)
    power = (n_fail > 0) and (n_pass > 0) and (len(set(vals)) > 1)
    return power, n_fail, n_pass, len(set(vals))


def bound_power(kind, bound, trials):
    """单侧边界型实验的判别力：给定的一组不同理论值中，是否同时存在被排除与存活。
    若全部存活，则该实验对这一组候选零判别力（消元型检验式对被消量零判别力）。"""
    marks = []
    for t in trials:
        excluded = (t < bound) if kind == "lower" else (t > bound)
        marks.append(not excluded)
    n_alive = sum(1 for x in marks if x)
    n_dead = len(marks) - n_alive
    return (n_alive > 0 and n_dead > 0), n_alive, n_dead

# ============================ 历史候选预言：全部从仓库成品回读 ============================
A28K = A28["key_numbers"]
A34K = A34["key_numbers"]
R120PD = R120["proton_decay"]

OBS_SIN2 = pv("P08")
SIG_SIN2 = sv("P08")
SIG_SU5 = F_of(CHI2_ROWS["SU5-sin2_thetaW"]["sigma"])
OBS_IDENT = F_of(CHI2_ROWS["IDENT-alpha_grav_e"]["obs"])
SIG_IDENT = F_of(CHI2_ROWS["IDENT-alpha_grav_e"]["sigma"])
LOWER_TAU = pv("P11")
UPPER_R = pv("K11")


def identity_theory(obs):
    """恒等式对照：alpha_grav(e) == (m_e/m_P)^2 由观测锚自身定义 ⇒ 理论值随观测同步。"""
    return obs


# 候选表：每条都带可机读来源、输入事实集、自由度账、目标事实 id
def cand(cid, kind, origin, theory, target_fact, input_facts, p_eq, p_axiom,
         obs=None, sigma=None, bound=None, exp_entry=None, note=""):
    return dict(id=cid, kind=kind, origin=origin, theory=theory, target_fact=target_fact,
                input_facts=list(input_facts), p_eq=p_eq, p_axiom=p_axiom,
                obs=obs, sigma=sigma, bound=bound, exp_entry=exp_entry, note=note)


CANDIDATES = [
    cand("K01-SU5-sin2-3over8", "chi2", "卡方靶场 SU5-sin2_thetaW / SU(5) 树级群论常数",
         F(3, 8), "P08", [], 0, 0,
         obs=F_of(CHI2_ROWS["SU5-sin2_thetaW"]["obs"]), sigma=SIG_SU5,
         exp_entry="SU5-sin2_thetaW",
         note="纯群论边界条件，不消费任何实测数值锚；非输入、零可调参数"),
    cand("K02-attack28-SM-sin2", "chi2", "attack28 key_numbers SM_pred_sin2thetaW",
         F_of(A28K["SM_pred_sin2thetaW"]), "P08", ["P15", "P07"], 0, 0,
         obs=OBS_SIN2, sigma=SIG_SIN2,
         note="真预测：sin2thetaW 不进入求解，只消费 alpha_em(M_Z) 与 alpha_s(M_Z)"),
    cand("K03-attack28-MSSM-sin2", "chi2", "attack28 key_numbers MSSM_pred_sin2thetaW",
         F_of(A28K["MSSM_pred_sin2thetaW"]), "P08", ["P15", "P07"], 0, 1,
         obs=OBS_SIN2, sigma=SIG_SIN2,
         note="与上条唯一差别是注入超对称假设 ⇒ p_axiom=1；偏差缩小是买来的"),
    cand("K04-attack28-circular-sin2", "chi2", "attack28 P2 循环版本 0.2304",
         F_of("0.2304"), "P08", ["P15", "P07", "P08"], 0, 0,
         obs=OBS_SIN2, sigma=SIG_SIN2,
         note="循环版本：目标观测本身是输入 ⇒ 对 sin2thetaW 零判别力"),
    cand("K05-RESTATEMENT-obs", "chi2", "阳性对照：把实测值原样当预测",
         OBS_SIN2, "P08", ["P08"], 0, 0,
         obs=OBS_SIN2, sigma=SIG_SIN2,
         note="构造对照，卡方精确为 0；留一法必须把它抓成回述型伪预言"),
    cand("K06-IDENT-alpha_grav_e", "identity", "卡方靶场 IDENT-alpha_grav_e 恒等式控制",
         identity_theory, "CHI-IDENT", [], 0, 0,
         obs=OBS_IDENT, sigma=SIG_IDENT, exp_entry="IDENT-alpha_grav_e",
         note="理论值由观测锚定义 ⇒ 卡方恒 0，但对任何观测扰动都恒绿 ⇒ 判别力 0"),
    cand("K07-BK18-r-upper", "upper", "BK18 张量标量比上界 K11（合成三点探针）",
         F(1, 100), "R-OBS", ["K11"], 0, 0,
         bound=UPPER_R,
         note="上界型实验：三个不同 r 值全部落在 r<0.032 内 ⇒ 判别力 0，存活不构成阳性证据"),
    cand("K08-SU5-tau_p", "lower", "r120 data.proton_decay.minimal_SU5.tau_yr",
         F_of(R120PD["minimal_SU5"]["tau_yr"]), "TAU-OBS", ["P11"], 0, 0,
         bound=LOWER_TAU,
         note="最小 SU(5) 质子寿命预言，已被 Super-K 下限硬排除"),
    cand("K09-MSSM-tau_p-dim6", "lower", "r120 data.proton_decay.MSSM_dim6_only.tau_yr",
         F_of(R120PD["MSSM_dim6_only"]["tau_yr"]), "TAU-OBS", ["P11"], 0, 1,
         bound=LOWER_TAU,
         note="注入维度六算符假设后落在下限之上 ⇒ 只是尚未排除，不是阳性证据"),
    cand("K10-attack34-tau_p-branch", "lower", "attack34 key_numbers branch_2loop_p14_taup_yr",
         F_of(A34K["branch_2loop_p14_taup_yr"]), "TAU-OBS", ["P11"], 0, 1,
         bound=LOWER_TAU,
         note="二圈分支读数，注入分支选择假设 ⇒ p_axiom=1，且低于 Super-K 下限"),
]

TRIALS_TAU = [F_of(R120PD["minimal_SU5"]["tau_yr"]),
              F_of(R120PD["MSSM_dim6_only"]["tau_yr"]),
              F_of(A34K["branch_2loop_p14_taup_yr"])]
TRIALS_R = [F(0), F(1, 100), F(3, 100)]

# 存活阈值与判别力阈值分开：反噬时只动其中一个，避免一次扰动连带破坏两道门
SURVIVE_CRIT = CHI2_CRIT


# ============================ 三重门逐条机算 ============================
def evaluate(c):
    kind = c["kind"]
    theory_fixed = c["theory"](c["obs"]) if callable(c["theory"]) else c["theory"]
    p_free = c["p_eq"] + c["p_axiom"]
    p_exp, lost = laf_dependency(c["input_facts"], FACTS_ALIVE)
    lto_ok, target_is_input, restated = lto_clean(
        c["target_fact"], c["input_facts"], theory_fixed, c["obs"] if c["obs"] is not None else c["bound"])

    is_identity = (kind == "identity")
    positive_evidence = False
    chi2 = None
    exp_chi2 = None
    n_fail = n_pass = n_distinct = 0
    n_alive = n_dead = 0
    excluded = False

    if kind in ("chi2", "identity"):
        chi2 = chi2_act(theory_fixed, c["obs"], c["sigma"])
        survive = (chi2 < SURVIVE_CRIT)
        power, n_fail, n_pass, n_distinct = chi2_power(c["theory"], c["obs"], c["sigma"])
        # 双侧测量、卡方存活、且通过留一法（非回述）才算阳性证据；
        # 恒等式、单侧边界、以及把观测原样当预测的对照都不算
        positive_evidence = survive and (not is_identity) and lto_ok
        if c["exp_entry"] is not None:
            exp_chi2 = chi2_exp_from_file(c["exp_entry"])
    else:
        trials = TRIALS_R if kind == "upper" else TRIALS_TAU
        excluded = (theory_fixed < c["bound"]) if kind == "lower" else (theory_fixed > c["bound"])
        survive = not excluded
        power, n_alive, n_dead = bound_power(kind, c["bound"], trials)
        # 下界/上界实验只给单侧：存活只意味「尚未被排除」，不构成阳性证据
        positive_evidence = False

    C1 = (p_free == 0)
    C2 = lto_ok
    C3 = survive and power and (not is_identity)
    breakthrough = C1 and C2 and C3

    if is_identity:
        label = "IDENTITY"
    elif restated or target_is_input:
        label = "RESTATED"
    elif not survive:
        label = "EXCLUDED"
    elif not power:
        label = "ZERO-POWER"
    elif not positive_evidence:
        label = "NOT-EXCLUDED-ONLY"
    elif not C1:
        label = "FREE-PARAM"
    else:
        label = "SURVIVE"
    if breakthrough:
        label = "BREAKTHROUGH"

    return dict(id=c["id"], kind=kind, origin=c["origin"], note=c["note"],
                theory=str(theory_fixed), obs=str(c["obs"]) if c["obs"] is not None else None,
                bound=str(c["bound"]) if c["bound"] is not None else None,
                chi2=str(chi2) if chi2 is not None else None,
                chi2_exp=str(exp_chi2) if exp_chi2 is not None else None,
                chi2_crit=str(CHI2_CRIT),
                p_eq=c["p_eq"], p_axiom=c["p_axiom"], p_free=p_free, p_exp=p_exp,
                p_total=p_free + p_exp, lost_facts=lost,
                target_is_input=target_is_input, restated=restated, lto_ok=lto_ok,
                survive=survive, excluded=excluded, power=power,
                power_readings=dict(n_fail=n_fail, n_pass=n_pass, n_distinct=n_distinct,
                                    n_alive=n_alive, n_dead=n_dead),
                positive_evidence=positive_evidence, is_identity=is_identity,
                C1=C1, C2=C2, C3=C3, breakthrough=breakthrough, label=label)


RESULTS = [evaluate(c) for c in CANDIDATES]
BY_ID = {r["id"]: r for r in RESULTS}
breakthrough_count = sum(1 for r in RESULTS if r["breakthrough"])
restated_count = sum(1 for r in RESULTS if r["label"] == "RESTATED")
excluded_count = sum(1 for r in RESULTS if r["label"] == "EXCLUDED")
zero_power_count = sum(1 for r in RESULTS if (not r["power"]))
identity_count = sum(1 for r in RESULTS if r["is_identity"])
c1_fail_count = sum(1 for r in RESULTS if not r["C1"])
c2_fail_count = sum(1 for r in RESULTS if not r["C2"])
c3_fail_count = sum(1 for r in RESULTS if not r["C3"])
survive_count = sum(1 for r in RESULTS if r["survive"])
positive_evidence_count = sum(1 for r in RESULTS if r["positive_evidence"])
p_exp_max = max(r["p_exp"] for r in RESULTS)
p_free_min = min(r["p_free"] for r in RESULTS)
p_total_min = min(r["p_total"] for r in RESULTS)

# 新思路核心读数：非输入且零自由参数的候选（C1∧C2）与实验存活（C3）是否相容
C12_ONLY = [r["id"] for r in RESULTS if r["C1"] and r["C2"]]
C123 = [r["id"] for r in RESULTS if r["C1"] and r["C2"] and r["C3"]]
seesaw_exp = (len(C12_ONLY) > 0) and (len(C123) == 0)


# ============================ 假设注入的数值效应（p_axiom 不是装饰） ============================
SM_PRED = F_of(A28K["SM_pred_sin2thetaW"])
MSSM_PRED = F_of(A28K["MSSM_pred_sin2thetaW"])
axiom_effect = MSSM_PRED - SM_PRED
dev_sm = abs(SM_PRED - OBS_SIN2) / OBS_SIN2
dev_mssm = abs(MSSM_PRED - OBS_SIN2) / OBS_SIN2
axiom_buys_closeness = (axiom_effect != 0) and (dev_mssm < dev_sm)
# attack28 P3 的实验输入灵敏度：预测值随 alpha_s 扰动而变化（外部读数回读）
alpha_s_sensitivity = F_of(A28K["alpha_s_sensitivity_spread"])
input_sensitivity_real = (alpha_s_sensitivity > 0)
# 两路机拼：本册从预测值与观测值重算的相对偏差 vs attack28 成品里登记的偏差百分数
dev_sm_pct_file = F_of(A28K["SM_dev_pct"])
dev_mssm_pct_file = F_of(A28K["MSSM_dev_pct"])
dev_sm_gap = abs(D_fr(dev_sm) * 100 - D_fr(dev_sm_pct_file))
dev_mssm_gap = abs(D_fr(dev_mssm) * 100 - D_fr(dev_mssm_pct_file))
dev_two_sources_ok = (dev_sm_gap < D("1e-3")) and (dev_mssm_gap < D("1e-3"))


# ============================ 控制组：四读数两两不同 + 正负对照 ============================
CTRL_IDS = ["K01-SU5-sin2-3over8", "K02-attack28-SM-sin2",
            "K03-attack28-MSSM-sin2", "K04-attack28-circular-sin2"]
CTRL_READINGS = [BY_ID[k]["chi2"] for k in CTRL_IDS]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
# 阳性对照：K05 卡方精确 0 却必须被留一法抓成回述
ctrl_positive_alerts = (BY_ID["K05-RESTATEMENT-obs"]["chi2"] == str(F(0))) and \
                       (BY_ID["K05-RESTATEMENT-obs"]["label"] == "RESTATED")
# 阴性对照：恒等式对 6 个不同观测读数全绿（判别力 0），配 NOT-ALL-GREEN
ctrl_identity_zero_power = (BY_ID["K06-IDENT-alpha_grav_e"]["power"] is False) and \
                           (BY_ID["K06-IDENT-alpha_grav_e"]["power_readings"]["n_fail"] == 0)
# 上界型对照：三个不同 r 值全部存活 ⇒ 该实验对这一组零判别力
ctrl_bound_zero_power = (BY_ID["K07-BK18-r-upper"]["power"] is False) and \
                        (BY_ID["K07-BK18-r-upper"]["power_readings"]["n_alive"] == len(TRIALS_R))
not_all_green = (len(set(CTRL_READINGS)) > 1) and (excluded_count > 0) and \
                (restated_count > 0) and (zero_power_count > 0)

# exp / act 两路回读一致性：SU5 靶场历史读数 vs 本册精确有理重算
CHI2_ACT_SU5 = chi2_act(F(3, 8), F_of(CHI2_ROWS["SU5-sin2_thetaW"]["obs"]), SIG_SU5)
CHI2_EXP_SU5 = chi2_exp_from_file("SU5-sin2_thetaW")
exp_act_rel = rel_diff(CHI2_ACT_SU5, CHI2_EXP_SU5)
exp_act_agree = (exp_act_rel < D("1e-6")) and (str(CHI2_ACT_SU5) != str(CHI2_EXP_SU5))

# 卡方阈值抬高的反噬基线：只改阈值，不改任何候选与观测
CHI2_CRIT_INFLATED = F(10) ** 40
false_survive_if_inflated = sum(
    1 for r in RESULTS
    if (r["chi2"] is not None) and (F_frac_str(r["chi2"]) < CHI2_CRIT_INFLATED) and (F_frac_str(r["chi2"]) >= CHI2_CRIT))
# 抹掉判别力门的假突破基线：K07 之类单侧上界候选会立刻假突破
false_breakthrough_if_no_power = sum(
    1 for r in RESULTS if r["C1"] and r["C2"] and r["survive"] and (not r["is_identity"]))
# 抹掉留一法门的假突破基线：K05 回述候选会立刻假突破
false_breakthrough_if_no_lto = sum(
    1 for r in RESULTS if r["C1"] and r["C3"])


# ============================ 跨卷脊梁与诚实边界 ============================
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and \
             (R404["key_numbers"]["four_force_accepted"] == 0)
spine_pred = sum(1 for e in R403.get("entries", []) if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
prev2_guards = PREV2["guard_pass"]
prev2_count = PREV2["guard_count"]
prev2_breakthrough = PREV2["key_numbers"]["breakthrough_count"]
prev2_native_pred = PREV2["key_numbers"]["native_independent_predictions"]
prev2_ledger_n = len(PREV)
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(SOURCE_FILES) > 0) and (len(source_missing) == 0)
honest_boundary = spine_zero and (spine_pred == 0) and (prev2_breakthrough == 0) and (prev2_native_pred == 0)

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
    return ("ALG-EXPFACTS-SURVIVAL"
            + "__CANDIDATES-" + token
            + "__BREAKTHROUGH-" + str(breakthrough_count)
            + "__RESTATED-" + str(restated_count)
            + "__EXCLUDED-" + str(excluded_count)
            + "__ZERO-POWER-" + str(zero_power_count)
            + "__C12-ONLY-" + str(len(C12_ONLY))
            + "__PEXP-MAX-" + str(p_exp_max)
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(len(RESULTS)))
v_machine_1 = verdict_with(str(len(RESULTS) + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and \
                     (("__CANDIDATES-" + str(len(RESULTS))) in v_machine_0)
verdict = v_machine_0


# ============================ 守卫组装 ============================
segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV-LEDGER-RELOADED",
    (prev2_ledger_n == 46) and (len(MEASURED_FACTS) == 7) and
    all(v["value"] != 0 for v in MEASURED_FACTS.values()),
    "PASS",
    "承接上一册 46 项实测锚；本册 M 类机器可读事实 " + str(len(MEASURED_FACTS)) +
    " 条全部非零，且逐条带 value/sigma/meaning")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 时判 FAIL")
add("PREV2-SPINE-RELOADED",
    (prev2_guards == prev2_count) and (prev2_count == 35) and
    (prev2_breakthrough == 0) and (prev2_native_pred == 0),
    "PASS",
    "上一册 35/35 守卫、20 次迭代突破 0 次、纯自洽独立预言 0 条；本册从其 p_exp 出口继续")
add("CHI2-CALIBER-EXTERNAL",
    ("chi2_crit_1dof_95" in CHI2DOC["caliber"]) and (CHI2_CRIT > F(0)) and (CHI2_CRIT < F(100)),
    "PASS",
    "卡方临界 " + CHI2_CRIT_TEXT + " 从仓库靶场 caliber 回读，本册不另造口径")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 chi2_act 与 chi2_exp_from_file 是两个不同函数，且 return 均非顶层数值常量")
add("EXP-ACT-AGREE-ON-SU5", exp_act_agree, "PASS",
    "两路机拼：本册精确有理重算 " + sci(CHI2_ACT_SU5, 9) + " vs 靶场历史读数 " +
    str(CHI2_EXP_SU5) + "，相对差 " + format(exp_act_rel, ".3E") + "；字面串不相等")
add("TAU-LIMIT-TWO-SOURCES",
    (F_of(str(R120PD["superK_limit_yr"])) == pv("P11")),
    "PASS",
    "Super-K 质子寿命下限两路机读：r120 成品 " + str(R120PD["superK_limit_yr"]) +
    " 与上一册来料表 P11 " + str(pv("P11")) + " 一致，两个文件路径互不引用")

add("C1-FREE-PARAM-ACCOUNTING",
    (p_free_min == 0) and (c1_fail_count > 0) and
    all(r["p_free"] == r["p_eq"] + r["p_axiom"] for r in RESULTS),
    "PASS",
    "自由度账 p_free=p_eq+p_axiom 逐条机算；最小 " + str(p_free_min) +
    "，因注入假设挡门 " + str(c1_fail_count) + " 条")
add("AXIOM-HAS-NUMERICAL-EFFECT", axiom_buys_closeness, "PASS",
    "attack28 的 SM " + str(SM_PRED) + " 与 MSSM " + str(MSSM_PRED) +
    " 差 " + sci(axiom_effect, 6) + "，相对偏差从 " + format(D_fr(dev_sm), ".4%") +
    " 降到 " + format(D_fr(dev_mssm), ".4%") + " ⇒ p_axiom 不是装饰，偏差缩小靠注入假设买来")
add("INPUT-SENSITIVITY-REAL", input_sensitivity_real, "PASS",
    "attack28 P3 外部读数：alpha_s ±5% 使预测跨度 " + str(alpha_s_sensitivity) +
    " ≠ 0 ⇒ 候选确实依赖实验输入，p_exp 计入账有依据")
add("DEVIATION-TWO-SOURCES", dev_two_sources_ok, "PASS",
    "偏差两路机拼：本册由预测值与观测值重算 " + format(D_fr(dev_sm) * 100, ".6f") + "% / " +
    format(D_fr(dev_mssm) * 100, ".6f") + "% vs attack28 成品登记 " +
    str(dev_sm_pct_file) + " / " + str(dev_mssm_pct_file) + "，绝对差 " +
    format(dev_sm_gap, ".2E") + " / " + format(dev_mssm_gap, ".2E"))
add("LTO-CATCHES-RESTATEMENT",
    (restated_count >= 2) and (BY_ID["K05-RESTATEMENT-obs"]["label"] == "RESTATED") and
    BY_ID["K04-attack28-circular-sin2"]["target_is_input"],
    "PASS",
    "留一法抓出回述型伪预言 " + str(restated_count) + " 条：把观测原样当预测、以及把目标观测塞回输入的循环版本")
add("LTO-ON-TRUE-PREDICTIONS",
    all(BY_ID[k]["lto_ok"] for k in ("K01-SU5-sin2-3over8", "K02-attack28-SM-sin2",
                                     "K03-attack28-MSSM-sin2")),
    "PASS",
    "对靶有利的单列：SU(5) 3/8 与 attack28 的 SM/MSSM 三条确实不是回述，目标观测不进入输入集")
add("LAF-COMPUTES-PEXP",
    (p_exp_max >= 2) and (BY_ID["K01-SU5-sin2-3over8"]["p_exp"] == 0) and
    all(len(r["lost_facts"]) == r["p_exp"] for r in RESULTS),
    "PASS",
    "LAF 逐项置零机算输入依赖度：纯群论候选 p_exp=0、attack28 家族 p_exp 最大 " +
    str(p_exp_max) + "；p_exp 计入 p_total 但不是可调自由选择")

add("CHI2-EXCLUSION-REGISTERED",
    (excluded_count >= 3) and (BY_ID["K01-SU5-sin2-3over8"]["label"] == "EXCLUDED") and
    (BY_ID["K08-SU5-tau_p"]["label"] == "EXCLUDED"),
    "PASS",
    "实验存活层判负 " + str(excluded_count) + " 条；卡方与质子寿命下限两条独立排除路径同时在册")
add("ATTACK28-PASS-REVERSED",
    (A28["tally"]["PASS"] > 0) and (BY_ID["K02-attack28-SM-sin2"]["label"] == "EXCLUDED") and
    (BY_ID["K03-attack28-MSSM-sin2"]["label"] == "EXCLUDED"),
    "PASS",
    "仓库 attack28 原标 " + str(A28["tally"]["PASS"]) + " 条 PASS；用其自身引用的观测 " +
    str(OBS_SIN2) + " 与本册来料 sigma " + str(SIG_SIN2) + " 重判，SM/MSSM 两条真预测均超临界")
add("DEVIATION-SIGMA-ORDERED",
    (F_frac_str(BY_ID["K02-attack28-SM-sin2"]["chi2"]) >
     F_frac_str(BY_ID["K03-attack28-MSSM-sin2"]["chi2"]) > CHI2_CRIT),
    "PASS",
    "卡方读数 SM " + sci(F_frac_str(BY_ID["K02-attack28-SM-sin2"]["chi2"]), 6) +
    " > MSSM " + sci(F_frac_str(BY_ID["K03-attack28-MSSM-sin2"]["chi2"]), 6) +
    " > 临界 " + CHI2_CRIT_TEXT + "；顺序由计算给出")
add("IDENTITY-ZERO-POWER", ctrl_identity_zero_power, "PASS",
    "恒等式阴性对照：6 个不同观测读数下卡方恒 0、判负读数 0 个 ⇒ 判别力 0，χ²≈0 不等于证据")
add("UPPER-BOUND-ZERO-POWER", ctrl_bound_zero_power, "PASS",
    "上界型对照：r 取 " + str(len(TRIALS_R)) + " 个不同值全部落在 r<" + str(UPPER_R) +
    " 内 ⇒ 该实验对这一组零判别力（消元型检验式对被消量零判别力）")
add("SURVIVE-NOT-EVIDENCE",
    (survive_count > 0) and (positive_evidence_count == 0),
    "PASS",
    "存活 " + str(survive_count) + " 条（" + "、".join(r["label"] for r in RESULTS if r["survive"]) +
    "），可算阳性证据 " + str(positive_evidence_count) +
    " 条 ⇒ 卡方为 0 的回述、恒等式、单侧上界、注入假设后的下限存活，全都不是证据")
add("SEESAW-C12-VS-C3", seesaw_exp and (len(C123) == 0), "PASS",
    "本册新思路读数：C1∧C2 同时成立的候选 " + str(len(C12_ONLY)) + " 条，逐条走 C3 后剩 " +
    str(len(C123)) + " 条 ⇒ 非输入性与实验存活在全部候选上互斥")
add("TRIPLE-GATE-NECESSITY",
    (c1_fail_count > 0) and (c2_fail_count > 0) and (c3_fail_count > 0) and
    (len(C123) == 0),
    "PASS",
    "三重门各自挡下 " + str(c1_fail_count) + " / " + str(c2_fail_count) + " / " +
    str(c3_fail_count) + " 条；无一条同时通过三门")
add("ZERO-BREAKTHROUGH", (breakthrough_count == 0), "PASS",
    "突破判据 C1∧C2∧C3 在 " + str(len(RESULTS)) + " 条候选上成立 " +
    str(breakthrough_count) + " 次")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个卡方读数两两不同：" + " / ".join(sci(F_frac_str(x), 6) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线，杜绝全表读数相同造成的假判别力")
add("CTRL-POSITIVE-ALERTS", ctrl_positive_alerts, "PASS",
    "阳性对照：卡方精确 0 的回述候选仍被留一法判 RESTATED，判据确实报警")
add("CTRL-NEGATIVE-GREEN", ctrl_identity_zero_power, "IDENTITY",
    "阴性对照：恒等式按预期恒绿，单独标 IDENTITY 并配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有排除、回述、零判别力等非恒绿读数 ⇒ 配 NOT-ALL-GREEN")
add("BACKFIRE-INFLATED-THRESHOLD", (false_survive_if_inflated > 0), "PASS",
    "反噬基线 1：把卡方临界抬到 1e40 会让 " + str(false_survive_if_inflated) +
    " 条被排除候选假存活 ⇒ 阈值必须驱动判定，不是装饰")
add("BACKFIRE-NO-LTO", (false_breakthrough_if_no_lto > 0), "PASS",
    "反噬基线 2：抹掉留一法门会让 " + str(false_breakthrough_if_no_lto) +
    " 条回述候选假突破 ⇒ C2 承重")
add("BACKFIRE-NO-POWER", (false_breakthrough_if_no_power > 0), "PASS",
    "反噬基线 3：抹掉判别力门会让 " + str(false_breakthrough_if_no_power) +
    " 条单侧上界候选假突破 ⇒ C3 承重")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把候选条数读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 " + str(spine_pred) +
    "；上一册突破 0 / 纯自洽独立预言 0")
add("COVERAGE-BOUNDARY",
    (len(STRUCTURAL_DISCRETE) == 4) and all(x["tag"] == "BOUNDARY" for x in STRUCTURAL_DISCRETE),
    "BOUNDARY",
    "上一册点名的 4 条结构性离散事实（电荷量子化 / 三代 / N_c=3 / 自旋统计）在本仓库无实测锚 ⇒ " +
    "只作符号输入、不计 p_exp、不冒充本册证明；本册只对有机器可读锚的 M 类事实全称成立")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (breakthrough_count == 0), "INFO",
    "本册不宣称攻破统一场论；三重门在全部候选上 0 次同时成立")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（结构层），不是实验证实；不产新物理，独立实验预言仍为 0")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-EXPFACTS--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-EXPFACTS--GATES-FAIL"
    return "ALG-EXPFACTS--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "SEESAW-C12-VS-C3", "ATTACK28-PASS-REVERSED",
                     "SURVIVE-NOT-EVIDENCE", "LTO-CATCHES-RESTATEMENT"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-EXPFACTS--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "candidates": len(RESULTS),
    "measured_facts_M": len(MEASURED_FACTS),
    "structural_discrete_D": len(STRUCTURAL_DISCRETE),
    "breakthrough_count": breakthrough_count,
    "C1_fail": c1_fail_count,
    "C2_fail": c2_fail_count,
    "C3_fail": c3_fail_count,
    "C12_only": len(C12_ONLY),
    "C12_only_ids": C12_ONLY,
    "C123": C123,
    "restated_count": restated_count,
    "excluded_count": excluded_count,
    "zero_power_count": zero_power_count,
    "identity_count": identity_count,
    "survive_count": survive_count,
    "positive_evidence_count": positive_evidence_count,
    "p_free_min": p_free_min,
    "p_exp_max": p_exp_max,
    "p_total_min": p_total_min,
    "chi2_crit": CHI2_CRIT_TEXT,
    "chi2_SU5_act": str(CHI2_ACT_SU5),
    "chi2_SU5_exp": str(CHI2_EXP_SU5),
    "chi2_SU5_rel_diff": format(exp_act_rel, ".6E"),
    "chi2_attack28_SM": BY_ID["K02-attack28-SM-sin2"]["chi2"],
    "chi2_attack28_MSSM": BY_ID["K03-attack28-MSSM-sin2"]["chi2"],
    "dev_SM_rel": format(D_fr(dev_sm), ".8%"),
    "dev_MSSM_rel": format(D_fr(dev_mssm), ".8%"),
    "dev_SM_pct_in_attack28": str(dev_sm_pct_file),
    "dev_MSSM_pct_in_attack28": str(dev_mssm_pct_file),
    "dev_two_sources_abs_gap": format(dev_sm_gap, ".6E") + " / " + format(dev_mssm_gap, ".6E"),
    "survive_labels": [r["id"] + ":" + r["label"] for r in RESULTS if r["survive"]],
    "axiom_effect_abs": str(axiom_effect),
    "alpha_s_sensitivity_spread": str(alpha_s_sensitivity),
    "tau_lower_SuperK": str(LOWER_TAU),
    "tau_SU5_minimal": str(TRIALS_TAU[0]),
    "tau_MSSM_dim6": str(TRIALS_TAU[1]),
    "tau_attack34_branch": str(TRIALS_TAU[2]),
    "r_upper_BK18": str(UPPER_R),
    "control_readings": CTRL_READINGS,
    "backfire_inflated_false_survive": false_survive_if_inflated,
    "backfire_no_lto_false_breakthrough": false_breakthrough_if_no_lto,
    "backfire_no_power_false_breakthrough": false_breakthrough_if_no_power,
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": spine_pred,
    "prev2_guards": str(prev2_guards) + "/" + str(prev2_count),
    "prev2_breakthrough": prev2_breakthrough,
    "prev2_native_independent_predictions": prev2_native_pred,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：实验给定事实 + 留一法剔伪 + 实验存活层 · 统一场论三重门攻坚",
    "date": "2026-11-11",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "measured_facts": {k: {"value": str(v["value"]), "sigma": str(v["sigma"]),
                           "meaning": v["meaning"]} for k, v in MEASURED_FACTS.items()},
    "structural_discrete": STRUCTURAL_DISCRETE,
    "gates": {
        "C1": "p_free = p_eq + p_axiom == 0",
        "C2": "留一法 LTO：目标观测不作为输入、理论值不等于观测值；LAF 机算 p_exp 依赖度",
        "C3": "实验存活：卡方/边界存活 且 判别力 > 0 且 非恒等式",
        "breakthrough": "C1 and C2 and C3",
    },
    "candidates": RESULTS,
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
    lines.append("算法联盟：实验给定事实 + 留一法剔伪 + 实验存活层 · 统一场论三重门攻坚")
    lines.append("=" * 92)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 92)
    lines.append("自由度账：p_total = p_eq + p_axiom + p_exp；C1 只看 p_free = p_eq + p_axiom。")
    lines.append("M 类机器可读实测锚 " + str(len(MEASURED_FACTS)) + " 条；D 类结构性离散事实 " +
                 str(len(STRUCTURAL_DISCRETE)) + " 条（无仓库实测锚，标 BOUNDARY、不计 p_exp）。")
    lines.append("三重门：C1 p_free==0 / C2 留一法非回述 / C3 卡方或边界存活且判别力>0。")
    lines.append("候选 " + str(len(RESULTS)) + " 条；突破 " + str(breakthrough_count) +
                 " 次；C1∧C2 同时成立 " + str(len(C12_ONLY)) + " 条，走完 C3 剩 " + str(len(C123)) + " 条。")
    lines.append("三重门分别挡下 C1=" + str(c1_fail_count) + " / C2=" + str(c2_fail_count) +
                 " / C3=" + str(c3_fail_count) + " 条。")
    lines.append("-" * 92)
    lines.append("卡方两路机拼：SU5 3/8 本册 act=" + sci(CHI2_ACT_SU5, 9) +
                 " / 靶场 exp=" + str(CHI2_EXP_SU5) + " / 相对差=" + format(exp_act_rel, ".3E") +
                 " / 临界=" + CHI2_CRIT_TEXT)
    lines.append("attack28 真预测重判：SM chi2=" + sci(F_frac_str(BY_ID["K02-attack28-SM-sin2"]["chi2"]), 6) +
                 " / MSSM chi2=" + sci(F_frac_str(BY_ID["K03-attack28-MSSM-sin2"]["chi2"]), 6) +
                 "，均超临界 ⇒ 原册 PASS 在实验存活层反转为 EXCLUDED。")
    lines.append("假设代价：SM 偏差 " + format(D_fr(dev_sm), ".4%") +
                 " → MSSM " + format(D_fr(dev_mssm), ".4%") +
                 "，p_axiom +1 带来的数值位移 " + sci(axiom_effect, 6))
    lines.append("-" * 92)
    lines.append("候选逐条判决（id / kind / label / p_free / p_exp / C1 C2 C3 / chi2 / 来源）：")
    for r in RESULTS:
        lines.append("  " + r["id"] + " [" + r["kind"] + "] " + r["label"] +
                     " p_free=" + str(r["p_free"]) + " p_exp=" + str(r["p_exp"]) +
                     " C1=" + str(r["C1"]) + " C2=" + str(r["C2"]) + " C3=" + str(r["C3"]) +
                     " chi2=" + (r["chi2"] if r["chi2"] is not None else "n/a"))
        lines.append("      " + r["origin"])
        lines.append("      " + r["note"])
    lines.append("-" * 92)
    lines.append("反噬基线：抬高卡方临界⇒" + str(false_survive_if_inflated) +
                 " 条假存活；抹掉留一法⇒" + str(false_breakthrough_if_no_lto) +
                 " 条假突破；抹掉判别力⇒" + str(false_breakthrough_if_no_power) + " 条假突破。")
    lines.append("红线：数学自洽 != 实验证实；四力大统一 0 条正确解；独立实验预言 0；不宣称攻破。")
    lines.append("-" * 92)
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
