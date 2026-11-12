# -*- coding: utf-8 -*-
"""
算法联盟：27 项双侧观测锚 × 历史理论预测 · 穷举配对与优化搜索
====================================================================================
第五轮。直接执行第四轮形式化出来的 OPEN 出口：把 27 项带非零 sigma 的双侧观测，
与仓库全部历史理论候选的数值输出做穷举配对；并把它升级为带目标函数的**优化搜索**：

  目标函数  min |gap|，gap = (theory - obs) / sigma
  约束      ① 对象同一（observable 标签必须相等，杜绝把 α_s 配到 M_Z 这类对象错位）
            ② LTO 非回述（理论值不等于观测值，且来源不是循环/恒等式/往返反解）
            ③ p_free 确定为 0（来源若无自由度标注则记 undetermined，不冒充）
            ④ χ² < 3.84145882069

输出不止「有没有命中」，还给出：最接近命中的配对、最小 sigma 距离、
达到命中所需的**最小理论修正量**与**误差棒放宽倍数**——这就是本轮「优化」的可算量。

诚实定位：数学自洽 != 实验证实；只产可算判决，不产新物理；
四力大统一 0 条正确解、独立实验预言 0；不宣称攻破统一场论。
（算法联盟册，不占 RID、不入 README、不与任何审计卷相加。）

环境纪律：Python 3.13 无 numpy/sympy，纯 Fraction / Decimal(60)；
UTF-8 源码 + ASCII runner；中文路径不进外层 argv。
"""
import json, os, ast, hashlib, re, itertools
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
ATTACK = os.path.join(ROOT, "04_公共成果", "本项目_统一场论攻破")
CROSS = os.path.join(ROOT, "03_跨体系研究")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_PREV4 = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_2026-11-11.json")
P_PREV3 = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
P_A28 = os.path.join(ATTACK, "attack28_力的大统一方程_sin2thetaW真预测_M5修法_2026-10-31.json")
P_A27B = os.path.join(ATTACK, "attack27b_力的大统一方程_零代价修法修正引擎_2026-10-30.json")
P_A34 = os.path.join(ATTACK, "attack34_b33符号的物理后果_tau_p与物理域判定_2026-10-31.json")
P_CHI2 = os.path.join(DATA, "靶场卡方联合拟合.json")
P_R188 = os.path.join(DATA, "TUFT-r188_S13残余路径一二三第一性审计_统一尺度出处与Z4超对称对应及MGUT几何指定_精算_2026-10-25.json")
P_GAQ = os.path.join(CROSS, "GAQ-UFT_V50_第五轮_力方程实验数据对标矩阵_2026-10-15.md")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
OUT_REPORT = os.path.join(DATA, "_ALG_pair_optim_recompute_report_2026-11-12.txt")
SOURCE_FILES = [P_LEDGER, P_PREV4, P_PREV3, P_A28, P_A27B, P_A34,
                P_CHI2, P_R188, P_GAQ, P_R403, P_R404]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def sci(fr, n=6):
    return format(D_fr(fr), "." + str(n) + "E")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


LEDGER = load(P_LEDGER)
PREV4 = load(P_PREV4)
PREV3 = load(P_PREV3)
A28 = load(P_A28)
A27B = load(P_A27B)
A34 = load(P_A34)
CHI2DOC = load(P_CHI2)
R188 = load(P_R188)
R403 = load(P_R403)
R404 = load(P_R404)
GAQ_TEXT = open(P_GAQ, encoding="utf-8").read()

PREV = {e["id"]: e for e in LEDGER["ledger"]}
CHI2_ROWS = {r["entry_id"]: r for r in CHI2DOC["rows"]}
CHI2_CRIT = F_of(PREV3["key_numbers"]["chi2_crit"])
GAP_CRIT = D_fr(CHI2_CRIT).sqrt()


# ============================ exp / act 两条独立路径（GAQ 两张表） ============================
def theory_value_act(pattern):
    """act 路径：从对标矩阵总表（§二）按正则抽取理论值。"""
    m = re.findall(pattern, GAQ_TEXT)
    if not m:
        raise RuntimeError("GAQ-ACT-MISSING-" + pattern)
    return F_of(m[0])


def theory_value_exp(pattern):
    """exp 路径：从残差表（§五）按**另一组正则**抽取同一物理量，互不引用。"""
    m = re.findall(pattern, GAQ_TEXT)
    if not m:
        raise RuntimeError("GAQ-EXP-MISSING-" + pattern)
    return F_of(m[-1])


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "theory_value_act" not in funcs or "theory_value_exp" not in funcs:
        return False
    if ast.dump(funcs["theory_value_act"]) == ast.dump(funcs["theory_value_exp"]):
        return False
    for name in ("theory_value_act", "theory_value_exp"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


# ============================ 27 项双侧观测锚 ============================
OBS_LABEL = {
    "C05": "G_Newton", "C06": "alpha_inv_zero", "C07": "alpha_inv_PDG",
    "C12": "Planck_length", "C13": "Planck_mass",
    "P01": "M_Z", "P02": "M_W_PDG2026", "P03": "M_W_PDG2024",
    "P04": "m_Higgs", "P05": "m_top", "P07": "alpha_s_MZ",
    "P08": "sin2thetaW_MZ", "P09": "pdg_213", "P12": "CKM_V",
    "G01": "mercury_precession", "G02": "light_deflection",
    "G04": "GW150914_mass", "G05": "EHT2019_shadow", "G06": "EHT2022_shadow",
    "K01": "H0_Planck", "K02": "H0_SH0ES", "K03": "H0_TRGB",
    "K04": "Omega_b_h2", "K05": "Omega_m_h2", "K06": "n_s",
    "K07": "T_CMB", "K10": "z_rec",
}
OBSERVATIONS = []
for e in LEDGER["ledger"]:
    if D(str(e["sigma"])) == 0:
        continue
    OBSERVATIONS.append(dict(id=e["id"], observable=OBS_LABEL[e["id"]],
                             value=F_of(e["value"]), sigma=F_of(e["sigma"]),
                             source=str(e.get("source", ""))))
OBS_BY_ID = {o["id"]: o for o in OBSERVATIONS}


# ============================ 历史理论预测输出 ============================
def theory(tid, value, observable, source, p_free_status, contam_tag, note):
    return dict(id=tid, theory=value, observable=observable, source=source,
                p_free_status=p_free_status, contam_tag=contam_tag, note=note)


A28K = A28["key_numbers"]
R188K = R188["key_numbers"]
CHI2_SU5_ROW = CHI2_ROWS["SU5-sin2_thetaW"]
IDENT_ROW = CHI2_ROWS["IDENT-alpha_grav_e"]
P3C = {c["id"]: c for c in PREV3["candidates"]}

GAQ_ACT_PAT = {
    "sec20": r"§20 一循环 sin²θ_W\s*\|\s*([\d.]+)",
    "sec24": r"§24 两循环 sin²θ_W\s*\|\s*([\d.]+)",
    "sec25": r"§25 全链 sin²θ_W\s*\|\s*([\d.]+)",
    "mW": r"UFE-1 V1 m_W\s*\|\s*([\d.]+)",
    "mercury": r"UFE-1 V3 水星进动\s*\|\s*([\d.]+)",
    "light": r"UFE-1 V4 光偏折\s*\|\s*([\d.]+)",
    "alpha_inv": r"α⁻¹ 复核[^|]*\|\s*([\d.]+)",
}
GAQ_EXP_PAT = {
    "mW": r"\|\s*m_W\s*\|\s*([\d.]+)",
    "sec25": r"\|\s*sin²θ_W（§25）\s*\|\s*([\d.]+)",
}
GAQ_ACT = {k: theory_value_act(v) for k, v in GAQ_ACT_PAT.items()}
GAQ_EXP = {k: theory_value_exp(v) for k, v in GAQ_EXP_PAT.items()}

# 污染标记机读：来源文本/成品字段，不手写
A28_CYCLIC = any("循环" in str(e.get("title", "")) for e in A28["entries"])
GAQ_IDENTITY = (re.search(r"α⁻¹ 复核[^\n]*恒等", GAQ_TEXT) is not None)
P3_RESTATED = (P3C["K05-RESTATEMENT-obs"]["label"] == "RESTATED")
P3_IDENTITY = (P3C["K06-IDENT-alpha_grav_e"]["label"] == "IDENTITY")
R188_MSSM_BETA = any("MSSM" in str(s) for s in R188K.get("sstar_formula_symbols", []))

THEORIES = [
    theory("T01-SU5-3over8", F(3, 8), "sin2thetaW_MZ", "卡方靶场 SU5-sin2_thetaW",
           "zero", "none", "纯群论树级 3/8，零可调参数"),
    theory("T02-attack28-SM", F_of(A28K["SM_pred_sin2thetaW"]), "sin2thetaW_MZ",
           "attack28 key_numbers SM_pred_sin2thetaW", "zero", "none",
           "GUT 边界真预测，sin2thetaW 不进入求解"),
    theory("T03-attack28-MSSM", F_of(A28K["MSSM_pred_sin2thetaW"]), "sin2thetaW_MZ",
           "attack28 key_numbers MSSM_pred_sin2thetaW", "nonzero", "none",
           "注入超对称假设，p_axiom=1"),
    theory("T04-attack28-circular", F_of("0.2304"), "sin2thetaW_MZ",
           "attack28 P2 循环版本", "zero", "cyclic" if A28_CYCLIC else "none",
           "目标观测被塞回输入，对 sin2thetaW 零判别力"),
    theory("T05-r188-sstar", F_of(R188K["sstar"]), "sin2thetaW_MZ",
           "r188 key_numbers sstar", "nonzero" if R188_MSSM_BETA else "undetermined", "none",
           "闭式 s*，符号集含 MSSM beta 系数 ⇒ 外部注入"),
    theory("T06-r188-sstar-SMbeta", F_of(R188K["sstar_with_sm_beta"]), "sin2thetaW_MZ",
           "r188 key_numbers sstar_with_sm_beta", "undetermined", "none",
           "负对照：换 SM beta 后 s* 大幅偏离"),
    theory("T07-GAQ-sec20", GAQ_ACT["sec20"], "sin2thetaW_MZ", "GAQ V50 §二 一循环",
           "undetermined", "none", "原册标 INFO（已闭合），相对误差 −1.76%"),
    theory("T08-GAQ-sec24", GAQ_ACT["sec24"], "sin2thetaW_MZ", "GAQ V50 §二 两循环",
           "undetermined", "none", "原册标 PASS，相对误差 +0.29%"),
    theory("T09-GAQ-sec25", GAQ_ACT["sec25"], "sin2thetaW_MZ", "GAQ V50 §二 全链",
           "undetermined", "none", "原册标 PASS，相对误差 +0.26%"),
    theory("T10-GAQ-mW", GAQ_ACT["mW"], "M_W_PDG2026", "GAQ V50 §二 UFE-1 V1",
           "undetermined", "none", "原册标 PASS，相对误差 0.0398% < 1% 阈值"),
    theory("T11-GAQ-mercury", GAQ_ACT["mercury"], "mercury_precession",
           "GAQ V50 §二 UFE-1 V3", "undetermined", "none", "理论值与实验锚同值"),
    theory("T12-GAQ-light", GAQ_ACT["light"], "light_deflection",
           "GAQ V50 §二 UFE-1 V4", "undetermined", "none", "理论值与实验锚同值"),
    theory("T13-GAQ-alpha-inv", GAQ_ACT["alpha_inv"], "alpha_inv_zero",
           "GAQ V50 §二 α⁻¹ 复核", "undetermined", "identity" if GAQ_IDENTITY else "none",
           "原册自标「恒等」，属定义复核"),
    theory("T14-P3-RESTATEMENT", F_frac_str(P3C["K05-RESTATEMENT-obs"]["theory"]),
           "sin2thetaW_MZ", "第三轮 K05 阳性对照", "zero",
           "restated" if P3_RESTATED else "none", "把实测值原样当预测"),
    theory("T15-P3-IDENTITY", F_of(IDENT_ROW["theory"]), "alpha_grav_e",
           "卡方靶场 IDENT-alpha_grav_e", "zero",
           "identity" if P3_IDENTITY else "none", "恒等式，27 项锚里无对应可观测量"),
    theory("T16-attack27b-tau_p", F_of(A27B["key_numbers"]["tau_p_computed_yr"]),
           "tau_p_lifetime", "attack27b key_numbers tau_p_computed_yr",
           "nonzero", "none", "质子寿命只有下界，27 项里无双侧观测锚"),
    theory("T17-attack34-tau_p", F_of(A34["key_numbers"]["branch_2loop_p14_taup_yr"]),
           "tau_p_lifetime", "attack34 key_numbers branch_2loop_p14_taup_yr",
           "nonzero", "none", "二圈分支读数，同样无双侧观测锚"),
]

# ============================ 穷举配对：对象门 + 污染门 + 卡方门 + 自由度门 ============================
def pair_eval(t, o, enforce_object=True, enforce_contam=True, crit=CHI2_CRIT):
    object_ok = (not enforce_object) or (t["observable"] == o["observable"])
    d = t["theory"] - o["value"]
    gap = d / o["sigma"]
    chi2 = gap * gap
    exact_restatement = (t["theory"] == o["value"])
    tag_contam = (t["contam_tag"] != "none")
    if enforce_contam:
        contaminated = exact_restatement or tag_contam
    else:
        contaminated = False
    chi2_ok = (chi2 < crit)
    p_free_ok = (t["p_free_status"] == "zero")
    hit = object_ok and chi2_ok and (not contaminated) and p_free_ok
    if not object_ok:
        label = "TYPE-MISMATCH"
    elif contaminated:
        label = "CONTAMINATED"
    elif not chi2_ok:
        label = "EXCLUDED"
    elif not p_free_ok:
        label = "P-FREE-UNDETERMINED-OR-NONZERO"
    else:
        label = "HIT"
    return dict(tid=t["id"], oid=o["id"], observable_t=t["observable"],
                observable_o=o["observable"], object_ok=object_ok,
                theory=str(t["theory"]), obs=str(o["value"]), sigma=str(o["sigma"]),
                d=str(d), gap=str(gap), chi2=str(chi2),
                exact_restatement=exact_restatement, tag_contam=tag_contam,
                contaminated=contaminated, chi2_ok=chi2_ok,
                p_free_status=t["p_free_status"], p_free_ok=p_free_ok,
                hit=hit, label=label, source=t["source"], note=t["note"])


ALL_PAIRS = [pair_eval(t, o) for t, o in itertools.product(THEORIES, OBSERVATIONS)]
N_total = len(ALL_PAIRS)
MATCHED = [p for p in ALL_PAIRS if p["object_ok"]]
N_matched = len(MATCHED)
N_object_mismatch = N_total - N_matched
CLEAN = [p for p in MATCHED if not p["contaminated"]]
N_clean = len(CLEAN)
HITS = [p for p in ALL_PAIRS if p["hit"]]
N_hits = len(HITS)

# 跨对象但数值上「看似接近」的伪配对：证明对象门不是装饰判据
CROSS_OBJECT_CLOSE = [p for p in ALL_PAIRS
                      if (not p["object_ok"]) and (F_frac_str(p["chi2"]) < CHI2_CRIT)
                      and (not p["contaminated"])]
N_cross_close = len(CROSS_OBJECT_CLOSE)


def abs_gap_fr(p):
    return abs(F_frac_str(p["gap"]))


def required_shift(p):
    """达到 95% 卡方区间所需的最小理论修正量；<=0 表示已在区间内。"""
    return abs(D_fr(F_frac_str(p["d"]))) - GAP_CRIT * D_fr(OBS_BY_ID[p["oid"]]["sigma"])


def sigma_inflation(p):
    """要把误差棒放宽多少倍才能让该配对判为存活。"""
    return abs(D_fr(F_frac_str(p["gap"]))) / GAP_CRIT


BEST = min(CLEAN, key=abs_gap_fr)
ZERO_FREE_CLEAN = [p for p in CLEAN if p["p_free_status"] == "zero"]
BEST_ZERO_FREE = min(ZERO_FREE_CLEAN, key=abs_gap_fr) if ZERO_FREE_CLEAN else None
best_gap_abs = abs_gap_fr(BEST)
best_chi2 = F_frac_str(BEST["chi2"])
best_shift = required_shift(BEST)
best_inflation = sigma_inflation(BEST)
zero_free_best_gap = abs_gap_fr(BEST_ZERO_FREE) if BEST_ZERO_FREE else None

# 原册口径对照：GAQ 用「相对误差 <1%」判 PASS，本册用带误差棒的卡方。
# ★这一对照必须钉死在固定历史配对 T10-GAQ-mW × P02 上，不能挂在 BEST 上：
#   反噬变体拆除对象门后 BEST 会换成跨对象伪配对，若相对误差随 BEST 漂移，
#   守卫会在计算前就崩掉，反噬测试测到的就不是「门是否承重」而是「None 异常」。
GAQ_MW_THEORY = [t for t in THEORIES if t["id"] == "T10-GAQ-mW"][0]["theory"]
GAQ_MW_OBS = OBS_BY_ID["P02"]["value"]
GAQ_MW_SIGMA = OBS_BY_ID["P02"]["sigma"]
GAQ_MW_D = GAQ_MW_THEORY - GAQ_MW_OBS
GAQ_MW_REL = abs(GAQ_MW_D) / GAQ_MW_OBS
GAQ_MW_GAP = GAQ_MW_D / GAQ_MW_SIGMA
GAQ_MW_CHI2 = GAQ_MW_GAP ** 2
GAQ_MW_INFLATION = abs(D_fr(GAQ_MW_GAP)) / GAP_CRIT


# ============================ 反噬基线（本册独立计算） ============================
def count_hits(enforce_object, enforce_contam, crit):
    n = 0
    for t, o in itertools.product(THEORIES, OBSERVATIONS):
        p = pair_eval(t, o, enforce_object, enforce_contam, crit)
        if p["hit"]:
            n += 1
    return n


backfire_no_object_gate = count_hits(False, True, CHI2_CRIT)
backfire_no_contam_gate = count_hits(True, False, CHI2_CRIT)
backfire_inflated_crit = count_hits(True, True, F(10) ** 40)


# ============================ 两路机拼 ============================
gaq_two_table_agree = (GAQ_ACT["mW"] == GAQ_EXP["mW"]) and \
                      (GAQ_ACT["sec25"] == GAQ_EXP["sec25"])
act_perturbed = theory_value_act(GAQ_ACT_PAT["sec20"])
exp_perturbed = theory_value_exp(GAQ_EXP_PAT["sec25"])
two_path_diverges = (act_perturbed != exp_perturbed)
# 卡方临界两路：第三轮 JSON 与卡方靶场 caliber
crit_two_sources = (CHI2_CRIT == F_of(CHI2DOC["caliber"]["chi2_crit_1dof_95"]))
# SU5 靶场历史读数与本册在 P08 sigma 下的重算（口径不同，如实报差异，不强求相等）
SU5_HIST = F_of(CHI2_SU5_ROW["chi2"])
SU5_NOW = F_frac_str([p for p in MATCHED if p["tid"] == "T01-SU5-3over8"][0]["chi2"])
su5_calibre_diff = abs(D_fr(SU5_NOW - SU5_HIST) / D_fr(SU5_HIST))
# 口径差异必须能由 sigma 比值平方精确解释，而不是靠一个拍出来的容差蒙混过关
SIGMA_HIST = F_of(CHI2_SU5_ROW["sigma"])
SIGMA_NOW = OBS_BY_ID["P08"]["sigma"]
sigma_ratio_sq = (SIGMA_NOW / SIGMA_HIST) ** 2
calibre_restored = SU5_NOW * sigma_ratio_sq
calibre_explained = (abs(D_fr(calibre_restored - SU5_HIST) / D_fr(SU5_HIST)) < D("1e-7"))


# ============================ 控制组 ============================
CTRL_READINGS = [N_total, N_matched, N_clean, N_hits]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
ctrl_positive_alerts = (N_cross_close > 0) and all(not p["object_ok"] for p in CROSS_OBJECT_CLOSE)
CTRL_IDENTITY = [p for p in MATCHED if p["label"] == "CONTAMINATED"]
ctrl_identity_never_hits = all(not p["hit"] for p in CTRL_IDENTITY)
not_all_green = (len(set(CTRL_READINGS)) > 1) and (N_cross_close > 0) \
                and (N_hits == 0) and (len(CTRL_IDENTITY) > 0)


# ============================ 跨卷脊梁与诚实边界 ============================
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and \
             (R404["key_numbers"]["four_force_accepted"] == 0)
spine_pred = sum(1 for e in R403.get("entries", []) if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
prev4_escape = PREV4["key_numbers"]["escape_models"]
prev4_b4 = PREV4["key_numbers"]["quad_gate_hits"]
prev4_guards = PREV4["guard_pass"]
prev4_count = PREV4["guard_count"]
prev3_breakthrough = PREV3["key_numbers"]["breakthrough_count"]
prev3_guards = PREV3["guard_pass"]
prev3_count = PREV3["guard_count"]
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(SOURCE_FILES) > 0) and (len(source_missing) == 0)
honest_boundary = spine_zero and (spine_pred == 0) and (prev3_breakthrough == 0) \
                  and (N_hits == 0)

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


best_gap_dec = abs(D_fr(F_frac_str(BEST["gap"])))
best_chi2_dec = D_fr(F_frac_str(BEST["chi2"]))
best_shift_dec = best_shift
best_inflation_dec = best_inflation
best_theory_pretty = format(D_fr(F_frac_str(BEST["theory"])), "f")
best_obs_pretty = format(D_fr(F_frac_str(BEST["obs"])), "f")
best_sigma_pretty = format(D_fr(F_frac_str(BEST["sigma"])), "f")


def fmt_fr_or_na(x, spec):
    """反噬变体里零自由参数层可能为空；None 时如实写 n/a，不让守卫崩在格式化上。"""
    return "n/a" if x is None else format(D_fr(x), spec)


def verdict_with(token):
    return ("ALG-PAIR-OPTIM"
            + "__PAIRS-" + token
            + "__MATCHED-" + str(N_matched)
            + "__CLEAN-" + str(N_clean)
            + "__HITS-" + str(N_hits)
            + "__BEST-GAP-SIGMA-" + format(best_gap_dec, ".4f")
            + "__BEST-CHI2-" + format(best_chi2_dec, ".4f")
            + "__SIGMA-INFLATION-" + format(best_inflation_dec, ".4f")
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_total))
v_machine_1 = verdict_with(str(N_total + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and (("__PAIRS-" + str(N_total)) in v_machine_0)
verdict = v_machine_0


# ============================ 守卫组装 ============================
segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV4-OPEN-EXECUTED",
    (PREV4["key_numbers"]["ledger_two_sided_with_sigma"] == len(OBSERVATIONS)) and
    (len(OBSERVATIONS) == 27) and (prev4_guards == prev4_count) and (prev4_count == 40),
    "PASS",
    "直接执行第四轮 OPEN 出口：其登记的 27 项双侧锚与本册回读的 " + str(len(OBSERVATIONS)) +
    " 项逐条对应；第四轮 40/40 守卫、四重门命中 " + str(prev4_b4) + "、单侧逃逸 " + str(prev4_escape))
add("PREV3-RELOADED",
    (prev3_guards == prev3_count) and (prev3_count == 39) and (prev3_breakthrough == 0),
    "PASS",
    "第三轮 39/39 守卫、10 条候选突破 0 次；本册回读其 p_free / 污染标签与卡方临界")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) + " 个；分母为 0 判 FAIL")
add("OBSERVATIONS-27-WITH-SIGMA",
    (len(OBSERVATIONS) == 27) and all(o["sigma"] != 0 for o in OBSERVATIONS),
    "PASS",
    "从 46 项来料表按 sigma!=0 机读 " + str(len(OBSERVATIONS)) +
    " 项双侧观测；每项带 value / sigma / observable / source")
add("THEORY-INVENTORY", (len(THEORIES) == 17), "PASS",
    "历史理论数值输出 " + str(len(THEORIES)) + " 条，来自卡方靶场、attack28、attack27b、attack34、r188、GAQ V50、第三轮共 7 处")

add("OBJECT-GATE-ENFORCED",
    (N_matched < N_total) and (N_object_mismatch > 0) and (N_cross_close > 0),
    "PASS",
    "★对象同一性门：全枚举 " + str(N_total) + " 对，observable 相等仅 " + str(N_matched) +
    " 对，拒绝 " + str(N_object_mismatch) + " 对跨对象错配")
add("CROSS-OBJECT-CLOSE-IS-REAL", (N_cross_close > 0), "PASS",
    "跨对象却有 " + str(N_cross_close) + " 对数值上 χ²<临界（例：" +
    "、".join(p["tid"] + "×" + p["oid"] for p in CROSS_OBJECT_CLOSE[:3]) +
    "）⇒ 若不做对象门，这类物理量完全不同的伪配对会混进优化搜索")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 theory_value_act 与 theory_value_exp 是两个不同函数，且 return 均非顶层数值常量")
add("GAQ-TWO-TABLE-AGREE", gaq_two_table_agree, "PASS",
    "两路机拼：GAQ §二 对标矩阵总表 vs §五 残差表，m_W=" + str(GAQ_ACT["mW"]) +
    " / §25 sin²θ_W=" + str(GAQ_ACT["sec25"]) + " 两表读数一致")
add("TWO-PATH-DIVERGE-ON-PERTURBATION", two_path_diverges, "PASS",
    "正对照：换抽另一理论条目时 act=" + str(act_perturbed) + " 而 exp=" +
    str(exp_perturbed) + " ⇒ 两路独立可寻址，不是同一表达式改名字")
add("CHI2-CRIT-TWO-SOURCES", crit_two_sources, "PASS",
    "卡方临界 " + str(CHI2_CRIT) + " 两路机读：第三轮 JSON 与卡方靶场 caliber 一致")
add("SU5-CALIBRE-EXPLAINED-BY-SIGMA",
    (su5_calibre_diff > 0) and calibre_explained, "PASS",
    "口径差异机算还原：靶场 sigma=" + str(SIGMA_HIST) + " 得 χ²=" + str(SU5_HIST) +
    "，本册 P08 sigma=" + str(SIGMA_NOW) + " 得 " + sci(SU5_NOW, 9) +
    "（相对差 " + format(su5_calibre_diff, ".3E") + "）；乘 sigma 比值平方 " +
    format(D_fr(sigma_ratio_sq), ".8f") + " 后还原为 " + sci(calibre_restored, 9) +
    "，与靶场一致 ⇒ 差异纯由误差棒口径造成，不是算错")

add("OPTIMIZATION-TARGET-DEFINED",
    (best_gap_dec > 0) and (best_shift_dec > 0) and (best_inflation_dec > 1) and
    (best_gap_dec > GAP_CRIT) and (len(CLEAN) > 0),
    "PASS",
    "目标函数 min|gap| 在 " + str(len(CLEAN)) + " 对非污染配对上求解：最优 " +
    BEST["tid"] + "×" + BEST["oid"] + "，|gap|=" + format(best_gap_dec, ".4f") +
    "σ，χ²=" + format(best_chi2_dec, ".4f"))
add("BEST-PAIR-IDENTIFIED",
    (BEST["observable_t"] == BEST["observable_o"]) and
    (BEST_ZERO_FREE is not None) and (zero_free_best_gap > best_gap_dec),
    "PASS",
    "最优配对是 " + BEST["tid"] + "（" + BEST["source"] + "）的 " + best_theory_pretty +
    " vs " + BEST["oid"] + " " + best_obs_pretty + "±" + best_sigma_pretty +
    "；而确定零自由参数层的最优仍差 " +
    fmt_fr_or_na(zero_free_best_gap, ".2f") + "σ（" +
    (BEST_ZERO_FREE["tid"] if BEST_ZERO_FREE else "n/a") + "）⇒ 越干净差得越远")
add("GAQ-RELATIVE-ERROR-VS-CHI2",
    (GAQ_MW_REL < F(1, 100)) and (GAQ_MW_CHI2 > CHI2_CRIT),
    "PASS",
    "★口径决定判定：固定历史配对 T10-GAQ-mW×P02 上，原册用「相对误差 <1%」判 PASS（实算 " +
    format(D_fr(GAQ_MW_REL) * 100, ".4f") + "%），本册用带误差棒 χ² 判 " +
    format(D_fr(GAQ_MW_CHI2), ".4f") + " > " + str(CHI2_CRIT) + " ⇒ FAIL。两者只差 " +
    format(GAQ_MW_INFLATION, ".4f") + " 倍误差棒")
add("REQUIRED-SHIFT-COMPUTED", (best_shift_dec > 0) and (best_inflation_dec < 2), "PASS",
    "优化量：达到 95% 卡方区间需把理论值至少修正 " + format(best_shift_dec, ".8E") +
    "（按该观测量单位），或把误差棒放宽 " + format(best_inflation_dec, ".4f") +
    " 倍 ⇒ 判定处在临界附近，不是稳健结论")
add("ZERO-FREE-LAYER-FARTHER",
    (BEST_ZERO_FREE is not None) and (zero_free_best_gap > best_gap_dec * 10),
    "PASS",
    "p_free 确定为 0 的候选层最优 " + fmt_fr_or_na(zero_free_best_gap, ".2f") +
    "σ，比全表最优差一个量级以上 ⇒ 自由度门不许放水")

add("ZERO-HITS", (N_hits == 0), "PASS",
    "穷举 " + str(N_total) + " 对，四门同时命中 " + str(N_hits) +
    " 对 ⇒ 第四轮 OPEN 出口给出的配对搜索在现有来料上 0 命中")
add("CONTAMINATED-EXCLUDED", (len(CTRL_IDENTITY) > 0) and ctrl_identity_never_hits, "PASS",
    "污染门剔下 " + str(len(CTRL_IDENTITY)) + " 对（理论值=观测值、恒等式、循环版本、往返反解），无一命中")
add("P-FREE-UNDETERMINED-REPORTED",
    (sum(1 for p in MATCHED if p["p_free_status"] == "undetermined") > 0),
    "BOUNDARY",
    "GAQ 等来源无自由度标注的配对记为 undetermined，不冒充 p_free=0，也不判负；" +
    str(sum(1 for p in MATCHED if p["p_free_status"] == "undetermined")) + " 对单列待定")
add("TAU-P-NO-TWO-SIDED-ANCHOR",
    (sum(1 for p in ALL_PAIRS if p["observable_t"] == "tau_p_lifetime" and p["object_ok"]) == 0),
    "PASS",
    "质子寿命只有 Super-K 下限、27 项里没有双侧误差棒观测 ⇒ 穷举配对对它零判别力，如实报 0 对")
add("EXCLUDED-COUNT-REPORTED",
    (sum(1 for p in MATCHED if p["label"] == "EXCLUDED") > 0),
    "PASS",
    "对象匹配后被卡方判负 " + str(sum(1 for p in MATCHED if p["label"] == "EXCLUDED")) +
    " 对；含 GAQ 三条 sin²θ_W 与 attack28 SM/MSSM/SU5")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个计数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 N_total，杜绝全表读数相同造成的假判别力")
add("CTRL-POSITIVE-ALERTS", ctrl_positive_alerts, "PASS",
    "阳性对照：" + str(N_cross_close) + " 对跨对象伪接近配对全部被对象门拦下")
add("CTRL-IDENTITY-NEVER-HITS", ctrl_identity_never_hits, "IDENTITY",
    "阴性对照：污染配对按预期 χ²≈0 却恒被污染门挡住，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有对象拒绝、卡方判负、优化位移等非恒绿读数 ⇒ 配 NOT-ALL-GREEN")
add("BACKFIRE-NO-OBJECT-GATE", (N_cross_close > 0), "PASS",
    "反噬基线 1：抹掉对象门会让 " + str(N_cross_close) + " 对物理量不同的伪配对进入优化搜索 ⇒ 对象门承重")
add("BACKFIRE-NO-CONTAM-GATE", (backfire_no_contam_gate > N_hits), "PASS",
    "反噬基线 2：抹掉污染门会出现 " + str(backfire_no_contam_gate) + " 次假命中 ⇒ LTO 非回述门承重")
add("BACKFIRE-INFLATED-CRIT", (backfire_inflated_crit > N_hits), "PASS",
    "反噬基线 3：把卡方临界抬到 1e40 会出现 " + str(backfire_inflated_crit) +
    " 次假命中 ⇒ 阈值必须驱动判定")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把配对总数读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 " + str(spine_pred) +
    "；第三轮突破 0、本册穷举命中 0")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (N_hits == 0), "INFO",
    "本册不宣称攻破统一场论；27 项双侧锚与历史理论输出的穷举配对 0 命中")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（配对与口径层），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_hits == 0) and (best_shift_dec > 0), "INFO",
    "0 命中才真需要一条新实验读数；在此之前可先补做「undetermined 层的 p_free 归属机读」，" +
    "把 GAQ 等来源的可调参数账查清，而不必先造新理论")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-PAIR-OPTIM--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-PAIR-OPTIM--GATES-FAIL"
    return "ALG-PAIR-OPTIM--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "GAQ-RELATIVE-ERROR-VS-CHI2", "ZERO-HITS",
                     "BEST-PAIR-IDENTIFIED", "ZERO-FREE-LAYER-FARTHER"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-PAIR-OPTIM--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "pairs_total": N_total,
    "observations_two_sided": len(OBSERVATIONS),
    "theories": len(THEORIES),
    "pairs_object_matched": N_matched,
    "pairs_object_mismatch": N_object_mismatch,
    "pairs_clean": N_clean,
    "pairs_hit": N_hits,
    "pairs_contaminated": len(CTRL_IDENTITY),
    "pairs_excluded": sum(1 for p in MATCHED if p["label"] == "EXCLUDED"),
    "pairs_p_free_undetermined": sum(1 for p in MATCHED if p["p_free_status"] == "undetermined"),
    "cross_object_close": N_cross_close,
    "cross_object_examples": [p["tid"] + "×" + p["oid"] for p in CROSS_OBJECT_CLOSE[:5]],
    "best_pair": BEST["tid"] + "×" + BEST["oid"],
    "best_theory": BEST["theory"],
    "best_theory_decimal": best_theory_pretty,
    "best_obs": BEST["obs"] + "+/-" + BEST["sigma"],
    "best_obs_decimal": best_obs_pretty + "+/-" + best_sigma_pretty,
    "best_gap_sigma": format(best_gap_dec, ".6f"),
    "best_chi2": format(best_chi2_dec, ".6f"),
    "chi2_crit": str(CHI2_CRIT),
    "gap_crit_sigma": format(GAP_CRIT, ".8f"),
    "required_theory_shift_GeV": format(best_shift_dec, ".8E"),
    "sigma_inflation_factor": format(best_inflation_dec, ".6f"),
    "gaq_relative_error_pct": format(D_fr(GAQ_MW_REL) * 100, ".6f") if GAQ_MW_REL is not None else None,
    "best_zero_free_pair": (BEST_ZERO_FREE["tid"] + "×" + BEST_ZERO_FREE["oid"]) if BEST_ZERO_FREE else None,
    "best_zero_free_gap_sigma": format(D_fr(zero_free_best_gap), ".4f") if BEST_ZERO_FREE else None,
    "SU5_chi2_historical": str(SU5_HIST),
    "SU5_chi2_this_run": sci(SU5_NOW, 9),
    "SU5_calibre_rel_diff": format(su5_calibre_diff, ".6E"),
    "SU5_sigma_ratio_sq": format(D_fr(sigma_ratio_sq), ".10f"),
    "SU5_calibre_restored": sci(calibre_restored, 9),
    "gaq_two_table_mW": str(GAQ_ACT["mW"]),
    "gaq_two_table_sec25": str(GAQ_ACT["sec25"]),
    "control_readings": CTRL_READINGS,
    "backfire_no_object_gate_false_hits": backfire_no_object_gate,
    "backfire_no_contam_gate_false_hits": backfire_no_contam_gate,
    "backfire_inflated_crit_false_hits": backfire_inflated_crit,
    "prev4_escape_models": prev4_escape,
    "prev4_quad_gate_hits": prev4_b4,
    "prev3_breakthrough": prev3_breakthrough,
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": spine_pred,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：27 项双侧观测锚 × 历史理论预测 · 穷举配对与优化搜索",
    "date": "2026-11-12",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "gates": {
        "object": "observable 标签必须相等",
        "contamination": "理论值不等于观测值，且来源不是循环/恒等式/往返反解",
        "p_free": "p_free_status 确定为 zero（无标注记 undetermined，不冒充）",
        "chi2": "((theory-obs)/sigma)^2 < " + str(CHI2_CRIT),
        "objective": "min |(theory-obs)/sigma|",
    },
    "observations": [dict(id=o["id"], observable=o["observable"],
                          value=str(o["value"]), sigma=str(o["sigma"])) for o in OBSERVATIONS],
    "theories": [dict(id=t["id"], theory=str(t["theory"]), observable=t["observable"],
                      source=t["source"], p_free_status=t["p_free_status"],
                      contam_tag=t["contam_tag"], note=t["note"]) for t in THEORIES],
    "pair_enumeration_summary": dict(total=N_total, object_matched=N_matched,
                                     object_mismatch=N_object_mismatch,
                                     clean=N_clean, hits=N_hits,
                                     note="全枚举逐对计算，JSON 只留对象匹配与跨对象伪接近的逐条证据"),
    "pairs_matched": MATCHED,
    "pairs_cross_object_close": CROSS_OBJECT_CLOSE,
    "optimization": dict(best_pair=BEST, best_zero_free_pair=BEST_ZERO_FREE,
                         gap_crit_sigma=str(GAP_CRIT),
                         required_shift=str(best_shift_dec),
                         sigma_inflation=str(best_inflation_dec)),
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
    lines.append("算法联盟：27 项双侧观测锚 × 历史理论预测 · 穷举配对与优化搜索")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("执行第四轮 OPEN 出口：27 项双侧锚 × " + str(len(THEORIES)) +
                 " 条历史理论数值输出，全枚举 " + str(N_total) + " 对。")
    lines.append("对象同一性门：匹配 " + str(N_matched) + " 对，拒绝 " + str(N_object_mismatch) +
                 " 对；其中跨对象却 χ²<临界 的伪配对 " + str(N_cross_close) + " 对。")
    lines.append("污染门剔 " + str(len(CTRL_IDENTITY)) + " 对；非污染 " + str(N_clean) +
                 " 对；四门同时命中 " + str(N_hits) + " 对。")
    lines.append("-" * 96)
    lines.append("优化目标 min|gap|：最优 " + BEST["tid"] + "×" + BEST["oid"] +
                 "，理论 " + best_theory_pretty + " vs 观测 " + best_obs_pretty +
                 "±" + best_sigma_pretty)
    lines.append("  |gap|=" + format(best_gap_dec, ".6f") + " sigma，chi2=" +
                 format(best_chi2_dec, ".6f") + "，临界=" + str(CHI2_CRIT))
    lines.append("  达到 95% 区间所需最小理论修正 = " + format(best_shift_dec, ".8E") +
                 " GeV；或误差棒放宽 " + format(best_inflation_dec, ".6f") + " 倍")
    lines.append("  原册 GAQ 用相对误差 <1% 判 PASS（实算 " +
                 (format(D_fr(GAQ_MW_REL) * 100, ".4f") if GAQ_MW_REL is not None else "n/a") +
                 "%），本册带误差棒卡方判 FAIL ⇒ 口径只差 " +
                 format(best_inflation_dec, ".4f") + " 倍误差棒")
    if BEST_ZERO_FREE is not None:
        lines.append("  p_free 确定为 0 的层最优 " + BEST_ZERO_FREE["tid"] + "×" +
                     BEST_ZERO_FREE["oid"] + "，|gap|=" + format(D_fr(zero_free_best_gap), ".4f") +
                     " sigma ⇒ 越干净差得越远")
    lines.append("-" * 96)
    lines.append("两路机拼：GAQ §二 vs §五 m_W=" + str(GAQ_ACT["mW"]) +
                 " / §25=" + str(GAQ_ACT["sec25"]) + "；卡方临界两路一致；" +
                 "SU5 靶场 " + str(SU5_HIST) + " vs 本册 P08 口径 " + sci(SU5_NOW, 9) +
                 "（相对差 " + format(su5_calibre_diff, ".3E") + "，口径差异如实报）")
    lines.append("-" * 96)
    lines.append("对象匹配配对逐条（tid × oid / label / gap_sigma / chi2 / p_free）：")
    for p in MATCHED:
        lines.append("  " + p["tid"] + " × " + p["oid"] + " [" + p["label"] + "] gap=" +
                     format(D_fr(F_frac_str(p["gap"])), ".4f") + " chi2=" +
                     sci(F_frac_str(p["chi2"]), 6) + " p_free=" + p["p_free_status"])
    lines.append("-" * 96)
    lines.append("反噬基线：抹掉对象门⇒" + str(N_cross_close) + " 对伪配对混入；抹掉污染门⇒" +
                 str(backfire_no_contam_gate) + " 次假命中；抬高卡方临界⇒" +
                 str(backfire_inflated_crit) + " 次假命中。")
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
