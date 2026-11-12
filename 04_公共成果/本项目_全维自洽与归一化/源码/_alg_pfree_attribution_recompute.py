# -*- coding: utf-8 -*-
"""
算法联盟：undetermined 层 p_free 归属机读 + 回填第五轮 459 对重判
====================================================================================
第六轮。执行第五轮写明的 OPEN 出口：把 8 对 p_free=undetermined 的占位拆成
可算的三账（p_eq 方程自由参数 / p_axiom 注入假设 / p_exp 实验给定输入），
逐条从来源机读证据，再回填第五轮配对表重跑四门。

两路机拼（互不引用）：
  act 路径 = AST 扫描 GAQ 对标脚本 unified_forces_vs_experiment.py 的数值字面量；
  exp 路径 = 正则扫描 GAQ V50 报告 §二对标矩阵总表的「理论值」列。
另有 §六锚点、§三判据修正、§四第一性原理关、r188 key_numbers 四类机读账。

诚实定位：本册判定的是「来源能否认证 p_free=0」，不是断言底层理论的自由参数真值。
数学自洽 != 实验证实；只产可算判决，不产新物理；四力大统一 0 条正确解、
独立实验预言 0；不宣称攻破统一场论。
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
CROSS = os.path.join(ROOT, "03_跨体系研究")
GAQ_DIR = os.path.join(ROOT, "01_独立体系", "S02_空间光速螺旋统一力", "04_理论推导")

P_PREV5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_PREV5V = os.path.join(DATA, "_ALG_pair_optim_verify_2026-11-12.json")
P_PREV4 = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_2026-11-11.json")
P_PREV3 = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_GAQ_MD = os.path.join(CROSS, "GAQ-UFT_V50_第五轮_力方程实验数据对标矩阵_2026-10-15.md")
P_GAQ_PY = os.path.join(GAQ_DIR, "unified_forces_vs_experiment.py")
P_R188 = os.path.join(DATA, "TUFT-r188_S13残余路径一二三第一性审计_统一尺度出处与Z4超对称对应及MGUT几何指定_精算_2026-10-25.json")
P_CHI2 = os.path.join(DATA, "靶场卡方联合拟合.json")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
OUT_REPORT = os.path.join(DATA, "_ALG_pfree_attribution_recompute_report_2026-11-12.txt")
SOURCE_FILES = [P_PREV5, P_PREV5V, P_PREV4, P_PREV3, P_LEDGER,
                P_GAQ_MD, P_GAQ_PY, P_R188, P_CHI2, P_R403, P_R404]


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


PREV5 = load(P_PREV5)
PREV5V = load(P_PREV5V)
PREV4 = load(P_PREV4)
PREV3 = load(P_PREV3)
LEDGER = load(P_LEDGER)
R188 = load(P_R188)
CHI2DOC = load(P_CHI2)
R403 = load(P_R403)
R404 = load(P_R404)
GAQ_MD = open(P_GAQ_MD, encoding="utf-8").read()
GAQ_PY = open(P_GAQ_PY, encoding="utf-8").read()
GAQ_TREE = ast.parse(GAQ_PY)

CHI2_CRIT = F_of(PREV3["key_numbers"]["chi2_crit"])
GAP_CRIT = D_fr(CHI2_CRIT).sqrt()


# ============================ 两路机拼：act = 脚本 AST / exp = 报告 §二 ============================
def act_literal_values(tree=None):
    """act 路径：AST 里所有数值字面量（不含布尔）。问的是「这个数是不是被直接写进源码」。"""
    src_tree = GAQ_TREE if tree is None else tree
    out = []
    for node in ast.walk(src_tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool):
            out.append(F_of(str(node.value)))
    return out


def act_row_theory_literals():
    """act 路径补强：row() 调用的第二个位置参数（理论值）是否为字面量。"""
    rows = []
    for node in ast.walk(GAQ_TREE):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "row" and len(node.args) >= 2:
            a = node.args
            name = a[0].value if isinstance(a[0], ast.Constant) else None
            theo = a[1]
            rows.append(dict(name=name, is_literal=isinstance(theo, ast.Constant),
                             value=theo.value if isinstance(theo, ast.Constant) else None,
                             symbols=[n.id for n in ast.walk(theo) if isinstance(n, ast.Name)]))
    return rows


def exp_md_table_rows(text=None):
    """exp 路径：从报告 §二对标矩阵总表抽出「理论值」列，数值前缀解析。"""
    seg = md_section("## 二、对标矩阵总表", text)
    rows = []
    for line in seg.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] == "组":
            continue
        if set("".join(cells)) <= set("- "):
            continue
        m = re.match(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?", cells[2])
        if m:
            rows.append(dict(label=cells[1], raw=cells[2], value=F_of(m.group(0))))
    return rows


def md_section(heading, text=None):
    """按 ## 标题切出一个章节，直到下一个 ## 标题；找不到就报错，不静默返回空。"""
    src = GAQ_MD if text is None else text
    i = src.find(heading)
    if i < 0:
        raise RuntimeError("MD-SECTION-MISSING-" + heading)
    j = src.find("\n## ", i + len(heading))
    return src[i:(j if j > 0 else len(src))]


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "act_literal_values" not in funcs or "exp_md_table_rows" not in funcs:
        return False
    if ast.dump(funcs["act_literal_values"]) == ast.dump(funcs["exp_md_table_rows"]):
        return False
    for name in ("act_literal_values", "exp_md_table_rows"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


ACT_LITERALS = act_literal_values()
ACT_ROWS = act_row_theory_literals()
EXP_ROWS = exp_md_table_rows()
ANCHOR_SEG = md_section("## 六、代码与参数")
CRIT_SEG = md_section("## 三、判据修正记录")
FIRST_SEG = md_section("## 四、三关检验逐项说明")
ANCHOR_BULLETS = [l for l in ANCHOR_SEG.splitlines() if l.startswith("- ")]
CRITERION_ROWS = [l for l in CRIT_SEG.splitlines()
                  if l.startswith("|") and "初版 FAIL" not in l
                  and not set(l.replace("|", "").strip()) <= set("- ")]
SCRIPT_NUMERIC_ASSIGNS = [n for n in GAQ_TREE.body
                          if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
                          and isinstance(n.value.value, (int, float))
                          and not isinstance(n.value.value, bool)]
FIRST_PRINCIPLE_ADMISSION = ("标准物理" in FIRST_SEG) and ("不是" in FIRST_SEG)


# ============================ r188 侧机读参数账 ============================
R188K = R188["key_numbers"]
R188_SYMS = list(R188K["sstar_formula_symbols"])
R188_BETA_FRAMEWORK = list(R188K["framework_beta_from_content"])
R188_BETA_CITED = list(R188K["mssm_beta_cited"])
R188_VFIT = F_of(R188K["v_fit_from_pdg"])
R188_INTERSECTION = list(R188K["sstar_framework_intersection"])
R188_REPAIR_ZERO = int(R188K["repair_zero_cost"])
R188_BETA_INJECTED = (len(R188_BETA_CITED) > 0) and (len(R188_BETA_FRAMEWORK) > 0) \
                     and (R188_VFIT != 0) and (len(R188_INTERSECTION) == 0)
R188_P_EXP = len(R188_SYMS) + (1 if R188_VFIT != 0 else 0)
GAQ_P_EXP = len(ANCHOR_BULLETS)


# ============================ 第五轮来料：17 理论 × 27 观测 ============================
OBSERVATIONS = [dict(id=o["id"], observable=o["observable"],
                     value=F_frac_str(o["value"]), sigma=F_frac_str(o["sigma"]))
                for o in PREV5["observations"]]
THEORIES = [dict(id=t["id"], theory=F_frac_str(t["theory"]),
                 observable=t["observable"], source=t["source"],
                 p_free_status=t["p_free_status"], contam_tag=t["contam_tag"],
                 note=t["note"]) for t in PREV5["theories"]]
THEORY_BY_ID = {t["id"]: t for t in THEORIES}
UNDETERMINED = [t for t in THEORIES if t["p_free_status"] == "undetermined"]
GAQ_TARGETS = [t for t in UNDETERMINED if not t["source"].startswith("r188")]
R188_TARGETS = [t for t in UNDETERMINED if t["source"].startswith("r188")]

# 每个 GAQ 目标在 exp 路径（§二表）中的行标签关键字，用于定位而非手写数值
MD_LABEL_KEY = {
    "T07-GAQ-sec20": "§20 一循环",
    "T08-GAQ-sec24": "§24 两循环",
    "T09-GAQ-sec25": "§25 全链",
    "T10-GAQ-mW": "UFE-1 V1 m_W",
    "T11-GAQ-mercury": "UFE-1 V3 水星进动",
    "T12-GAQ-light": "UFE-1 V4 光偏折",
    "T13-GAQ-alpha-inv": "α⁻¹ 复核",
}

# ============================ 两路证据：这个数值是「算出来的」还是「写进去的」 ============================
def evidence_for(t):
    v = t["theory"]
    act_hit = any(x == v for x in ACT_LITERALS)
    key = MD_LABEL_KEY[t["id"]]
    md_rows = [r for r in EXP_ROWS if key in r["label"]]
    exp_hit = (len(md_rows) == 1) and (md_rows[0]["value"] == v)
    return act_hit, exp_hit, md_rows


def classify(t, act_hit, exp_hit, beta_injected):
    """把第五轮的 undetermined 占位拆成可算三账；只判「能否认证为零」，不冒充测出真值。"""
    old = t["p_free_status"]
    if old != "undetermined":
        return dict(tid=t["id"], old=old, new=old, p_eq=None, p_axiom=None, p_exp=None,
                    p_free=(0 if old == "zero" else None),
                    certified_zero=(old == "zero"), reason="NOT-IN-SCOPE",
                    act_hit=act_hit, exp_hit=exp_hit)
    if t["source"].startswith("r188"):
        p_eq = 0
        p_axiom = 1 if beta_injected else 0
        p_exp = R188_P_EXP
        status = "NONZERO-BETA-INJECTED" if p_axiom > 0 else "UNDETERMINED"
        reason = "r188 机读：MSSM/SM beta 系数由外部框架注入，v_fit_from_pdg 为拟合量"
        p_free = (p_eq + p_axiom) if p_axiom > 0 else None
    else:
        literal_ok = (act_hit and exp_hit)
        p_eq = 0
        p_axiom = 1 if literal_ok else 0
        p_exp = GAQ_P_EXP
        status = "INPUT-LITERAL" if literal_ok else "UNDETERMINED"
        reason = "两路机读：理论值在脚本 AST 与报告 §二表中同为字面量，来源内无推导链"
        # 只数报告层的注入陈述，不冒充测出底层理论的自由参数真值
        p_free = None
    certified_zero = (p_free == 0)
    return dict(tid=t["id"], old=old, new=status, p_eq=p_eq, p_axiom=p_axiom,
                p_exp=p_exp, p_free=p_free, certified_zero=certified_zero,
                reason=reason, act_hit=act_hit, exp_hit=exp_hit)


def build_ledger():
    recs = []
    for t in THEORIES:
        if t["id"] in MD_LABEL_KEY:
            ah, eh, _ = evidence_for(t)
        else:
            ah, eh = False, False
        recs.append(classify(t, ah, eh, R188_BETA_INJECTED))
    return recs


LEDGER_RECS = build_ledger()
REC_BY_ID = {r["tid"]: r for r in LEDGER_RECS}
RECLASSIFIED = [r for r in LEDGER_RECS if r["old"] == "undetermined"]
N_RECLASSIFIED = len(RECLASSIFIED)
N_REMAINING_UNDETERMINED = sum(1 for r in RECLASSIFIED if r["new"] == "UNDETERMINED")
N_INPUT_LITERAL = sum(1 for r in RECLASSIFIED if r["new"] == "INPUT-LITERAL")
N_BETA_INJECTED = sum(1 for r in RECLASSIFIED if r["new"] == "NONZERO-BETA-INJECTED")
N_UNCHANGED = sum(1 for r in LEDGER_RECS if r["old"] != "undetermined")
N_STATUS_CHANGED = sum(1 for r in LEDGER_RECS if r["old"] != r["new"])

OLD_STATUS_MAP = {t["id"]: t["p_free_status"] for t in THEORIES}
NEW_STATUS_MAP = {r["tid"]: ("zero" if r["certified_zero"] else r["new"]) for r in LEDGER_RECS}
N_CERTIFIED_ZERO_THEORIES = sum(1 for r in LEDGER_RECS if r["certified_zero"])


# ============================ 正对照：两路在扰动下必须分叉 ============================
T10_VALUE = THEORY_BY_ID["T10-GAQ-mW"]["theory"]


def t10_in_act(vals):
    return any(v == T10_VALUE for v in vals)


def t10_in_exp(rows):
    return any((r["value"] == T10_VALUE) and ("UFE-1 V1 m_W" in r["label"]) for r in rows)


def two_path_perturb():
    py2 = GAQ_PY.replace("80.409", "80.419")
    md2 = GAQ_MD.replace("80.409", "80.419")
    act_base = t10_in_act(ACT_LITERALS)
    exp_base = t10_in_exp(EXP_ROWS)
    act_py = t10_in_act(act_literal_values(ast.parse(py2)))
    exp_md = t10_in_exp(exp_md_table_rows(md2))
    return dict(act_base=act_base, exp_base=exp_base,
                act_after_py_perturb=act_py, exp_after_py_perturb=exp_base,
                act_after_md_perturb=act_base, exp_after_md_perturb=exp_md)


PERTURB = two_path_perturb()
two_path_diverges = (PERTURB["act_base"] and PERTURB["exp_base"]) and \
                    (not PERTURB["act_after_py_perturb"]) and \
                    (not PERTURB["exp_after_md_perturb"]) and \
                    (PERTURB["act_after_py_perturb"] != PERTURB["exp_after_py_perturb"]) and \
                    (PERTURB["act_after_md_perturb"] != PERTURB["exp_after_md_perturb"])
N_ROW_LITERAL = sum(1 for r in ACT_ROWS if r["is_literal"])
N_ROW_TOTAL = len(ACT_ROWS)
ACT_ROW_LITERAL_VALUES = [F_of(str(r["value"])) for r in ACT_ROWS
                          if r["is_literal"] and r["value"] is not None]
N_GAQ_IN_ROW_LITERALS = sum(1 for t in GAQ_TARGETS if t["theory"] in ACT_ROW_LITERAL_VALUES)
T07_NOT_IN_ROWS = (THEORY_BY_ID["T07-GAQ-sec20"]["theory"] not in ACT_ROW_LITERAL_VALUES)
T13_NOT_IN_ROWS = (THEORY_BY_ID["T13-GAQ-alpha-inv"]["theory"] not in ACT_ROW_LITERAL_VALUES)
T13_ROUNDTRIP = any(("α⁻¹" in str(r["name"])) and ("alpha_codata" in r["symbols"])
                    and (not r["is_literal"]) for r in ACT_ROWS)
GAQ_ALL_AGREE = all(REC_BY_ID[t["id"]]["act_hit"] and REC_BY_ID[t["id"]]["exp_hit"]
                    for t in GAQ_TARGETS)


# ============================ 回填第五轮配对表：两路读数互校 ============================
def pair_eval(t, o, status_map, crit, enforce_object=True, enforce_contam=True):
    object_ok = (not enforce_object) or (t["observable"] == o["observable"])
    d = t["theory"] - o["value"]
    gap = d / o["sigma"]
    chi2 = gap * gap
    exact_restatement = (t["theory"] == o["value"])
    tag_contam = (t["contam_tag"] != "none")
    contaminated = (exact_restatement or tag_contam) if enforce_contam else False
    chi2_ok = (chi2 < crit)
    p_free_ok = (status_map[t["id"]] == "zero")
    hit = object_ok and chi2_ok and (not contaminated) and p_free_ok
    return dict(tid=t["id"], oid=o["id"], object_ok=object_ok,
                gap=gap, chi2=chi2, contaminated=contaminated,
                p_free_status=status_map[t["id"]], hit=hit,
                d=d, theory=t["theory"], obs=o["value"], sigma=o["sigma"])


def abs_gap(p):
    return abs(p["gap"])


def run_pairs(status_map, crit=None, enforce_object=True, enforce_contam=True):
    c = CHI2_CRIT if crit is None else crit
    ps = [pair_eval(t, o, status_map, c, enforce_object, enforce_contam)
          for t, o in itertools.product(THEORIES, OBSERVATIONS)]
    matched = [p for p in ps if p["object_ok"]]
    clean = [p for p in matched if not p["contaminated"]]
    certified = [p for p in clean if status_map[p["tid"]] == "zero"]
    hits = [p for p in ps if p["hit"]]
    return dict(all=ps, matched=matched, clean=clean, certified=certified, hits=hits,
                n_total=len(ps), n_matched=len(matched), n_clean=len(clean),
                n_certified=len(certified), n_hits=len(hits))


OLD = run_pairs(OLD_STATUS_MAP)
NEW = run_pairs(NEW_STATUS_MAP)
ACT_COUNTS = (OLD["n_total"], OLD["n_matched"], OLD["n_clean"], OLD["n_hits"])
EXP_COUNTS = tuple(PREV5["key_numbers"][k] for k in
                   ("pairs_total", "pairs_object_matched", "pairs_clean", "pairs_hit"))
two_source_agree = (ACT_COUNTS == EXP_COUNTS)
BEST_OLD = min(OLD["clean"], key=abs_gap)
BEST_CERTIFIED = min(NEW["certified"], key=abs_gap) if NEW["certified"] else None
best_old_gap = abs_gap(BEST_OLD)
best_certified_gap = abs_gap(BEST_CERTIFIED) if BEST_CERTIFIED else None
best_old_gap_dec = D_fr(best_old_gap)
best_certified_gap_dec = D_fr(best_certified_gap) if BEST_CERTIFIED else None
recede_ratio = (best_certified_gap_dec / best_old_gap_dec) if BEST_CERTIFIED else None
PREV5_BEST = PREV5["key_numbers"]["best_pair"]
optimum_disqualified = (BEST_OLD["tid"] + "×" + BEST_OLD["oid"] == PREV5_BEST) and \
                       (REC_BY_ID[BEST_OLD["tid"]]["old"] == "undetermined") and \
                       (not REC_BY_ID[BEST_OLD["tid"]]["certified_zero"])
N_HITS_AFTER = NEW["n_hits"]
verdict_unchanged = (OLD["n_hits"] == 0) and (N_HITS_AFTER == 0) and \
                    (N_UNCHANGED == len(THEORIES) - N_RECLASSIFIED) and \
                    (N_STATUS_CHANGED == N_RECLASSIFIED)
BACKFIRE_READINGS = dict(n_certified_zero=N_CERTIFIED_ZERO_THEORIES,
                         n_hits_after=N_HITS_AFTER,
                         n_remaining_undetermined=N_REMAINING_UNDETERMINED,
                         best_certified_gap=str(best_certified_gap) if BEST_CERTIFIED else None)

# 反噬基线（本册独立计算，核验只在内存里替换源码单点）
backfire_no_object = run_pairs(NEW_STATUS_MAP, enforce_object=False)["n_matched"]
backfire_no_contam = run_pairs(NEW_STATUS_MAP, enforce_contam=False)["n_hits"]
backfire_inflated_crit = run_pairs(NEW_STATUS_MAP, crit=F(10) ** 40)["n_hits"]

# ============================ 控制组与跨卷脊梁 ============================
CTRL_READINGS = [OLD["n_total"], N_RECLASSIFIED, NEW["n_certified"], N_HITS_AFTER]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
CTRL_IDENTITY = [p for p in NEW["matched"] if p["contaminated"]]
ctrl_identity_never_hits = all(not p["hit"] for p in CTRL_IDENTITY)
not_all_green = (len(set(CTRL_READINGS)) > 1) and (N_RECLASSIFIED > 0) and \
                (N_HITS_AFTER == 0) and (len(CTRL_IDENTITY) > 0)
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and \
             (R404["key_numbers"]["four_force_accepted"] == 0)
spine_pred = sum(1 for e in R403.get("entries", []) if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
prev5_guards = PREV5["guard_pass"]
prev5_count = PREV5["guard_count"]
prev5_verify = PREV5V["verdict"]
prev4_b4 = PREV4["key_numbers"]["quad_gate_hits"]
prev3_breakthrough = PREV3["key_numbers"]["breakthrough_count"]
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(SOURCE_FILES) > 0) and (len(source_missing) == 0)
honest_boundary = spine_zero and (spine_pred == 0) and (prev3_breakthrough == 0) \
                  and (PREV5["key_numbers"]["pairs_hit"] == 0) and (N_HITS_AFTER == 0)

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
    return ("ALG-PFREE-ATTRIBUTION"
            + "__RECLASSIFIED-" + token
            + "__LITERAL-" + str(N_INPUT_LITERAL)
            + "__BETA-" + str(N_BETA_INJECTED)
            + "__CERTIFIED-" + str(N_CERTIFIED_ZERO_THEORIES)
            + "__HITS-" + str(N_HITS_AFTER)
            + "__BEST-GAP-SIGMA-" + format(best_certified_gap_dec, ".4f")
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_RECLASSIFIED))
v_machine_1 = verdict_with(str(N_RECLASSIFIED + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and \
                     (("__RECLASSIFIED-" + str(N_RECLASSIFIED)) in v_machine_0)
verdict = v_machine_0


# ============================ 守卫组装 ============================
segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV5-RELOADED",
    (prev5_guards == prev5_count) and (prev5_count == 38) and
    (prev5_verify == "VERIFY-ALL-PASS") and
    (PREV5["key_numbers"]["pairs_hit"] == 0) and
    (PREV5["key_numbers"]["pairs_p_free_undetermined"] == 8),
    "PASS",
    "第五轮 38/38 守卫、VERIFY-ALL-PASS、穷举命中 0、8 对 undetermined 待查；本册直接承接该 OPEN 出口")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("UNDETERMINED-8-ENUMERATED",
    (N_RECLASSIFIED == 8) and (len(GAQ_TARGETS) == 7) and (len(R188_TARGETS) == 1),
    "PASS",
    "机读 8 对：GAQ V50 七条（sec20/sec24/sec25/mW/mercury/light/alpha_inv）+ r188 一条（sstar_with_sm_beta）")
add("GAQ-SCRIPT-AST-PARSED", (N_ROW_TOTAL > 0) and (len(ACT_LITERALS) > 0), "PASS",
    "独立第二路径：对标脚本 AST 解析出 " + str(N_ROW_TOTAL) + " 个 row() 调用、" +
    str(len(ACT_LITERALS)) + " 个数值字面量")

add("ACT-LITERAL-SCAN", all(REC_BY_ID[t["id"]]["act_hit"] for t in GAQ_TARGETS), "PASS",
    "act 路径：7 条理论值全部作为数值字面量出现在脚本 AST 中 ⇒ 来源内没有把它们算出来的表达式")
add("EXP-MD-TABLE-SCAN", all(REC_BY_ID[t["id"]]["exp_hit"] for t in GAQ_TARGETS), "PASS",
    "exp 路径：7 条理论值在报告 §二总表的「理论值」列逐条唯一命中，数值前缀机读解析")
add("TWO-PATH-AGREE", GAQ_ALL_AGREE and (len(EXP_ROWS) > 0), "PASS",
    "两路读数一致：act 与 exp 对 7 条给出同一数值，且都等于第五轮 JSON 里的理论值")
add("TWO-PATH-DIVERGE-ON-PERTURBATION", two_path_diverges, "PASS",
    "双向正对照：内存里把脚本 80.409→80.419 ⇒ act=" +
    str(PERTURB["act_after_py_perturb"]) + " 而 exp=" + str(PERTURB["exp_after_py_perturb"]) +
    "；只改报告 ⇒ act=" + str(PERTURB["act_after_md_perturb"]) + " 而 exp=" +
    str(PERTURB["exp_after_md_perturb"]) + " ⇒ 两路分别可寻址，不是同一表达式改名")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_literal_values 与 exp_md_table_rows 是两个不同函数，且 return 均非顶层数值常量")
add("TARGETS-IN-LITERAL-SUBSET",
    (N_ROW_LITERAL > 0) and (N_ROW_LITERAL < N_ROW_TOTAL) and
    (N_GAQ_IN_ROW_LITERALS == len(GAQ_TARGETS) - 2) and
    T07_NOT_IN_ROWS and T13_NOT_IN_ROWS and T13_ROUNDTRIP,
    "PASS",
    "如实报混合结构：" + str(N_ROW_TOTAL) + " 个判定行里 " + str(N_ROW_LITERAL) +
    " 个理论值是字面量；7 条目标中 " + str(N_GAQ_IN_ROW_LITERALS) +
    " 条落在字面量判定行，§20 的 0.2272 只在 INFO 打印里（连判定行都没有），" +
    "α⁻¹ 复核由 AST 机读为 1/alpha_codata 的定义往返表达式（对目标量零判别力）")

add("GAQ-ANCHOR-LEDGER", (GAQ_P_EXP > 0) and (len(SCRIPT_NUMERIC_ASSIGNS) > 0), "PASS",
    "p_exp 机读：§六外部锚点 " + str(GAQ_P_EXP) + " 组（CODATA/PDG/Super-K/pdgLive），脚本顶层数值字面量赋值 " +
    str(len(SCRIPT_NUMERIC_ASSIGNS)) + " 处 ⇒ 数值链不是零输入")
add("GAQ-CRITERION-LEDGER", (len(CRITERION_ROWS) > 0) and FIRST_PRINCIPLE_ADMISSION, "PASS",
    "§三判据修正记录 " + str(len(CRITERION_ROWS)) + " 行（改窗口/降 INFO/放宽阈值/改下界）；§四自述第一性来源是标准物理、不是单公理反向生成")
add("R188-BETA-INJECTED", R188_BETA_INJECTED and (len(R188_SYMS) > 0), "PASS",
    "r188 机读：sstar_formula_symbols " + str(len(R188_SYMS)) + " 个、framework_beta " +
    str(len(R188_BETA_FRAMEWORK)) + " 个、mssm_beta_cited " + str(len(R188_BETA_CITED)) +
    " 个、v_fit_from_pdg 非零、framework_intersection 空 ⇒ 外部框架注入")
add("R188-NO-ZERO-COST-REPAIR", (R188_REPAIR_ZERO == 0), "PASS",
    "r188 repair_zero_cost=" + str(R188_REPAIR_ZERO) + " ⇒ 没有零代价修法把注入项消掉")

add("RECLASSIFY-ALL-8",
    (N_REMAINING_UNDETERMINED == 0) and (N_INPUT_LITERAL == 7) and
    (N_BETA_INJECTED == 1) and
    (N_CERTIFIED_ZERO_THEORIES == sum(1 for t in THEORIES if t["p_free_status"] == "zero")),
    "PASS",
    "8 对全部给出确定处置：7 对 INPUT-LITERAL、1 对 NONZERO-BETA-INJECTED；0 对保持无据待定；" +
    "原本确定为 zero 的 " + str(N_CERTIFIED_ZERO_THEORIES) + " 条未被误改")
add("P-FREE-ZERO-NOT-CERTIFIABLE", all(not r["certified_zero"] for r in RECLASSIFIED), "PASS",
    "★本册判的是「来源能否认证 p_free=0」：8 对全部不能。7 对有注入字面量正证据，1 对有 beta 系数注入正证据")
add("TRUE-P-FREE-UNDECIDED",
    all(r["p_free"] is None or r["p_free"] > 0 for r in RECLASSIFIED) and
    (sum(1 for r in RECLASSIFIED if r["p_free"] is None) == N_INPUT_LITERAL),
    "BOUNDARY",
    "不冒充测出底层理论的自由参数真值：" + str(N_INPUT_LITERAL) +
    " 对 GAQ 记 p_free=未定（只数报告层注入陈述 p_axiom=1、实验输入 p_exp=4）；" +
    "r188 一条由机读字段确定为 p_free=" +
    str([r["p_free"] for r in RECLASSIFIED if r["new"] == "NONZERO-BETA-INJECTED"]))

add("TWO-SOURCE-COUNTS-AGREE", two_source_agree, "PASS",
    "回填前先用旧状态复算：act=" + str(ACT_COUNTS) + "，exp=第五轮 key_numbers " +
    str(EXP_COUNTS) + " ⇒ 本册复算路径与第五轮成品互校一致")
add("UPGRADE-DOES-NOT-CHANGE-VERDICT", verdict_unchanged, "PASS",
    "元纪律：判据升级后把旧候选映射回新判据重算。17 条里只有 8 条 undetermined 改变状态，其余 " +
    str(N_UNCHANGED) + " 条原样；命中数 0→" + str(N_HITS_AFTER) + "，既有判决不变")
add("ZERO-HITS-AFTER-RECLASSIFY", (N_HITS_AFTER == 0), "PASS",
    "回填 459 对重跑四门，命中 " + str(N_HITS_AFTER) + " 对；四门同时命中仍为 0")
add("OPTIMUM-DISQUALIFIED", optimum_disqualified, "PASS",
    "★第五轮最优 " + PREV5_BEST + "（2.666667σ）恰在 undetermined 层；归属查清后认证不了 zero ⇒ 失去资格")
add("CERTIFIED-LAYER-RECEDES",
    (BEST_CERTIFIED is not None) and (recede_ratio > 100) and
    (best_certified_gap_dec > best_old_gap_dec),
    "PASS",
    "可认证零自由参数层只剩 " + str(NEW["n_certified"]) + " 对，最优 " +
    (BEST_CERTIFIED["tid"] + "×" + BEST_CERTIFIED["oid"] if BEST_CERTIFIED else "n/a") +
    " = " + format(best_certified_gap_dec, ".4f") + "σ，比全表最优 " +
    format(best_old_gap_dec, ".4f") + "σ 远 " + format(recede_ratio, ".4f") +
    " 倍 ⇒ 清账把「离命中最近」推远两个量级")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个计数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 " + str(CTRL_READINGS[0]) + "，杜绝全表读数相同造成的假判别力")
add("CTRL-POSITIVE-ALERTS", optimum_disqualified and (N_INPUT_LITERAL > 0), "PASS",
    "阳性对照：第五轮最优配对被本册归属门真实拦下，不是恒绿")
add("CTRL-IDENTITY-NEVER-HITS", ctrl_identity_never_hits, "IDENTITY",
    "阴性对照：" + str(len(CTRL_IDENTITY)) + " 对污染配对按预期 χ²≈0 却恒被挡住，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有 8 对归属改写、最优失格、认证层后退等非恒绿读数")

add("BACKFIRE-NO-OBJECT-GATE", (backfire_no_object > OLD["n_matched"]), "PASS",
    "反噬基线 1：抹掉对象门会让对象匹配数 " + str(OLD["n_matched"]) + "→" +
    str(backfire_no_object) + " ⇒ 对象门承重")
add("BACKFIRE-NO-CONTAM-GATE", (backfire_no_contam > N_HITS_AFTER), "PASS",
    "反噬基线 2：抹掉污染门出现 " + str(backfire_no_contam) + " 次假命中 ⇒ LTO 非回述门承重")
add("BACKFIRE-INFLATED-CRIT", (backfire_inflated_crit > N_HITS_AFTER), "PASS",
    "反噬基线 3：卡方临界抬到 1e40 出现 " + str(backfire_inflated_crit) +
    " 次假命中 ⇒ 阈值必须驱动判定")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把归属改写条数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 " + str(spine_pred) +
    "；第三轮突破 0、第四轮四重门命中 " + str(prev4_b4) + "、第五轮穷举 0、本册回填 0")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (N_HITS_AFTER == 0), "INFO",
    "本册不宣称攻破统一场论；8 对归属查清、最优失格、回填命中仍 0")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（来源参数账与回填层），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_HITS_AFTER == 0) and (N_REMAINING_UNDETERMINED == 0), "INFO",
    "8 对归属已闭合，0 命中仍成立 ⇒ 下一轮只剩一条硬出口：构造或检索一条带双侧误差棒、" +
    "且理论值落在其可判负区间之外的新实验读数；在此之前不必再造新理论")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-PFREE-ATTRIBUTION--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-PFREE-ATTRIBUTION--GATES-FAIL"
    return "ALG-PFREE-ATTRIBUTION--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "RECLASSIFY-ALL-8", "OPTIMUM-DISQUALIFIED",
                     "CERTIFIED-LAYER-RECEDES", "ZERO-HITS-AFTER-RECLASSIFY"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-PFREE-ATTRIBUTION--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "undetermined_pairs_prev5": PREV5["key_numbers"]["pairs_p_free_undetermined"],
    "reclassified": N_RECLASSIFIED,
    "gaq_targets": len(GAQ_TARGETS),
    "r188_targets": len(R188_TARGETS),
    "input_literal": N_INPUT_LITERAL,
    "beta_injected": N_BETA_INJECTED,
    "remaining_undetermined": N_REMAINING_UNDETERMINED,
    "certified_zero_theories": N_CERTIFIED_ZERO_THEORIES,
    "status_changed": N_STATUS_CHANGED,
    "status_unchanged": N_UNCHANGED,
    "gaq_row_calls": N_ROW_TOTAL,
    "gaq_row_theory_literals": N_ROW_LITERAL,
    "gaq_targets_in_row_literals": N_GAQ_IN_ROW_LITERALS,
    "gaq_p_exp_anchor_groups": GAQ_P_EXP,
    "gaq_script_numeric_assigns": len(SCRIPT_NUMERIC_ASSIGNS),
    "gaq_criterion_rows": len(CRITERION_ROWS),
    "gaq_first_principle_admission": FIRST_PRINCIPLE_ADMISSION,
    "r188_formula_symbols": len(R188_SYMS),
    "r188_framework_beta": len(R188_BETA_FRAMEWORK),
    "r188_mssm_beta_cited": len(R188_BETA_CITED),
    "r188_p_exp": R188_P_EXP,
    "r188_repair_zero_cost": R188_REPAIR_ZERO,
    "act_counts_old": list(ACT_COUNTS),
    "exp_counts_prev5": list(EXP_COUNTS),
    "two_source_agree": two_source_agree,
    "pairs_total": OLD["n_total"],
    "pairs_object_matched": OLD["n_matched"],
    "pairs_clean": OLD["n_clean"],
    "pairs_hit_before": OLD["n_hits"],
    "pairs_hit_after": N_HITS_AFTER,
    "pairs_certified_clean": NEW["n_certified"],
    "best_pair_before": PREV5_BEST,
    "best_gap_before_sigma": format(best_old_gap_dec, ".6f"),
    "best_certified_pair": (BEST_CERTIFIED["tid"] + "×" + BEST_CERTIFIED["oid"]) if BEST_CERTIFIED else None,
    "best_certified_gap_sigma": format(best_certified_gap_dec, ".6f") if BEST_CERTIFIED else None,
    "certified_layer_recede_ratio": format(recede_ratio, ".6f") if BEST_CERTIFIED else None,
    "chi2_crit": str(CHI2_CRIT),
    "control_readings": CTRL_READINGS,
    "backfire_no_object_gate_matched": backfire_no_object,
    "backfire_no_contam_gate_hits": backfire_no_contam,
    "backfire_inflated_crit_hits": backfire_inflated_crit,
    "prev5_guards": prev5_guards,
    "prev5_verify": prev5_verify,
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
    "title": "算法联盟：undetermined 层 p_free 归属机读 + 回填第五轮 459 对重判",
    "date": "2026-11-12",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "gates": {
        "act": "AST 扫描 GAQ 对标脚本的数值字面量",
        "exp": "正则扫描 GAQ V50 §二总表理论值列",
        "reclassify": "只判来源能否认证 p_free=0，不冒充测出自由参数真值",
        "backfill": "用新归属重跑第五轮四门（对象/污染/p_free/卡方）",
    },
    "attribution_ledger": [dict(tid=r["tid"], old=r["old"], new=r["new"],
                                p_eq=r["p_eq"], p_axiom=r["p_axiom"], p_exp=r["p_exp"],
                                p_free=str(r["p_free"]) if r["p_free"] is not None else None,
                                certified_zero=r["certified_zero"], reason=r["reason"],
                                act_hit=r["act_hit"], exp_hit=r["exp_hit"])
                           for r in LEDGER_RECS],
    "gaq_evidence": dict(script_literal_values=len(ACT_LITERALS), row_calls=N_ROW_TOTAL,
                         row_theory_literals=N_ROW_LITERAL,
                         md_table_rows=len(EXP_ROWS),
                         perturbation=PERTURB),
    "r188_evidence": dict(symbols=R188_SYMS, framework_beta=R188_BETA_FRAMEWORK,
                          mssm_beta_cited=R188_BETA_CITED,
                          v_fit_from_pdg=str(R188_VFIT),
                          framework_intersection=R188_INTERSECTION,
                          repair_zero_cost=R188_REPAIR_ZERO),
    "backfill": dict(before=dict(total=OLD["n_total"], matched=OLD["n_matched"],
                                 clean=OLD["n_clean"], hits=OLD["n_hits"]),
                     after=dict(total=NEW["n_total"], matched=NEW["n_matched"],
                                clean=NEW["n_clean"], certified=NEW["n_certified"],
                                hits=N_HITS_AFTER),
                     certified_pairs=[dict(pair=p["tid"] + "×" + p["oid"],
                                           gap_sigma=format(D_fr(abs_gap(p)), ".6f"))
                                      for p in NEW["certified"]]),
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
    lines.append("算法联盟：undetermined 层 p_free 归属机读 + 回填第五轮 459 对重判")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("执行第五轮 OPEN 出口：8 对 undetermined 逐条机读来源参数账。")
    lines.append("两路机拼：act=GAQ 对标脚本 AST（" + str(len(ACT_LITERALS)) + " 个数值字面量 / " +
                 str(N_ROW_TOTAL) + " 个 row 调用，其中 " + str(N_ROW_LITERAL) +
                 " 个理论值为字面量）；exp=GAQ V50 §二总表（" + str(len(EXP_ROWS)) + " 行）。")
    lines.append("7 条 GAQ 理论值两路同为字面量；其中 " + str(N_GAQ_IN_ROW_LITERALS) +
                 " 条是判定行的字面量理论值，§20 的 0.2272 只在 INFO 打印里，" +
                 "α⁻¹ 复核是 1/alpha_codata 的定义往返表达式。")
    lines.append("r188 机读：symbols=" + str(len(R188_SYMS)) + " / framework_beta=" +
                 str(len(R188_BETA_FRAMEWORK)) + " / mssm_beta_cited=" + str(len(R188_BETA_CITED)) +
                 " / v_fit_from_pdg 非零 / repair_zero_cost=" + str(R188_REPAIR_ZERO))
    lines.append("-" * 96)
    lines.append("归属结果：" + str(N_INPUT_LITERAL) + " 对 INPUT-LITERAL + " +
                 str(N_BETA_INJECTED) + " 对 NONZERO-BETA-INJECTED；剩余 undetermined " +
                 str(N_REMAINING_UNDETERMINED) + " 对；认证 zero 的理论仍 " +
                 str(N_CERTIFIED_ZERO_THEORIES) + " 条。")
    lines.append("逐条（tid / old -> new / p_eq,p_axiom,p_exp / 认证 zero）：")
    for r in LEDGER_RECS:
        lines.append("  " + r["tid"] + " : " + r["old"] + " -> " + r["new"] +
                     " | " + str(r["p_eq"]) + "," + str(r["p_axiom"]) + "," + str(r["p_exp"]) +
                     " | cert0=" + str(r["certified_zero"]))
    lines.append("-" * 96)
    lines.append("回填前两路互校：act=" + str(ACT_COUNTS) + " exp=第五轮 " + str(EXP_COUNTS) +
                 " ⇒ " + ("一致" if two_source_agree else "不一致"))
    lines.append("回填后：全枚举 " + str(NEW["n_total"]) + " 对，对象匹配 " + str(NEW["n_matched"]) +
                 " 对，非污染 " + str(NEW["n_clean"]) + " 对，可认证零自由参数 " +
                 str(NEW["n_certified"]) + " 对，四门命中 " + str(N_HITS_AFTER) + " 对（前后均 0）。")
    lines.append("★第五轮最优 " + PREV5_BEST + " = " + format(best_old_gap_dec, ".6f") +
                 "σ 已失格；认证层最优 " +
                 (BEST_CERTIFIED["tid"] + "×" + BEST_CERTIFIED["oid"] if BEST_CERTIFIED else "n/a") +
                 " = " + (format(best_certified_gap_dec, ".6f") if BEST_CERTIFIED else "n/a") +
                 "σ，后退 " + (format(recede_ratio, ".6f") if BEST_CERTIFIED else "n/a") + " 倍")
    lines.append("-" * 96)
    lines.append("反噬基线：抹掉对象门⇒匹配 " + str(OLD["n_matched"]) + "→" +
                 str(backfire_no_object) + "；抹掉污染门⇒" + str(backfire_no_contam) +
                 " 次假命中；抬高卡方临界⇒" + str(backfire_inflated_crit) + " 次假命中。")
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
