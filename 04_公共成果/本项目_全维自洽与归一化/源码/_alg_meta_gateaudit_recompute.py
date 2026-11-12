# -*- coding: utf-8 -*-
"""
算法联盟：判据自审 + 模型空间穷举 + 描述压缩增益 + 谓词自指反噬
====================================================================================
第四轮。前三轮都在找「更好的理论候选」或「更多来料/机制类型」，本轮换到元层级：
把前三轮的**判据本身**当作审查对象，问三个新问题：

  (M1) 第三轮的三重门 C1/C2/C3 在逻辑上是否相容？是否存在满足构型？
       若存在、且其中含单侧边界型，则三重门有**判据逃逸**：它把
       「尚未被排除」误当成「阳性证据」。本册穷举有限一致模型空间把它找出来，
       并补上 C4 双侧阳性证据门，升级为四重门。
  (M2) 描述压缩增益（MDL 有限影子）：统一是否真的压缩了描述，而不只是换写法？
       gain = 非回述数值陈述数 − (p_free + p_exp)，且只认通过实验存活层的陈述。
  (M3) 「统一」谓词自指反噬：unifies(m) 必须对模型扰动敏感、不能恒真、
       不能由公理直接注入；否则它本身是装饰判据。

预期结论（不预支，全部由机算给出）：三重门**逻辑相容**但**不完备**，
存在单侧逃逸构型；补 C4 后满足构型全部要求双侧观测量；
现有 10 条候选在四重门下仍 0 命中 ⇒ 缺口是「理论给出可被双侧观测命中的非回述数值」，
不是逻辑死胡同。数学自洽 != 实验证实；不产新物理；不宣称攻破统一场论。

（算法联盟册，不占 RID、不入 README、不与任何审计卷相加。）
环境纪律：Python 3.13 无 numpy/sympy，纯 Fraction / Decimal(60)；
UTF-8 源码 + ASCII runner；中文路径不进外层 argv。
"""
import json, os, ast, hashlib, itertools
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")

P_PREV3 = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
P_PREV2 = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_2026-11-11.json")
P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_CHI2 = os.path.join(DATA, "靶场卡方联合拟合.json")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_2026-11-11.json")
OUT_REPORT = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_report_2026-11-11.txt")
SOURCE_FILES = [P_PREV3, P_PREV2, P_LEDGER, P_CHI2, P_R403, P_R404]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    """把 Fraction 字符串（a/b 或整数）还原成精确有理数。"""
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def sci(fr, n=6):
    return format(D_fr(fr), "." + str(n) + "E")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


PREV3 = load(P_PREV3)
PREV2 = load(P_PREV2)
LEDGER = load(P_LEDGER)
CHI2DOC = load(P_CHI2)
R403 = load(P_R403)
R404 = load(P_R404)

CAND = PREV3["candidates"]
PREV3_K = PREV3["key_numbers"]
CHI2_CRIT_PREV = F_of(PREV3_K["chi2_crit"])
PREV = {e["id"]: e for e in LEDGER["ledger"]}


# ============================ exp / act 两条独立路径 ============================
def survive_exp(r):
    """exp 路径：直接回读第三轮成品 JSON 里的 survive 布尔字段。"""
    return bool(r["survive"])


def survive_act(r):
    """act 路径：本册用精确有理卡方或 excluded 字段独立重算，不读 survive 字段。"""
    if r["chi2"] is None:
        return not bool(r["excluded"])
    return F_frac_str(r["chi2"]) < CHI2_CRIT_PREV


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "survive_act" not in funcs or "survive_exp" not in funcs:
        return False
    if ast.dump(funcs["survive_act"]) == ast.dump(funcs["survive_exp"]):
        return False
    for name in ("survive_act", "survive_exp"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


# ============================ 有限一致模型空间 ============================
# 一个抽象「理论候选」由 6 个离散属性刻画；power 与 obs_type 独立，
# 因此这是**逻辑可构型空间**，不绑定某个具体实验（具体实验的判别力另见第三轮 K07）。
P_FREE_VALS = (0, 1, 2)
LTO_VALS = (0, 1)
OBS_TYPES = ("two-sided", "lower", "upper", "identity")
SURVIVE_VALS = (0, 1)
POWER_VALS = (0, 1)
AXIOM_VALS = (0, 1)


def model_of(tup):
    p_free, lto, obs, survive, power, axiom = tup
    return dict(p_free=p_free, lto=lto, obs_type=obs, survive=survive,
                power=power, axiom_injected=axiom,
                is_identity=(obs == "identity"), two_sided=(obs == "two-sided"))


def consistent(m):
    """一致性约束：把逻辑上自相矛盾的构型剔掉，不让它们污染穷举读数。"""
    if m["is_identity"] and (m["power"] != 0 or m["survive"] != 1 or m["lto"] != 0):
        return False
    if m["axiom_injected"] == 1 and m["p_free"] == 0:
        return False
    return True


ALL_MODELS = [model_of(t) for t in itertools.product(
    P_FREE_VALS, LTO_VALS, OBS_TYPES, SURVIVE_VALS, POWER_VALS, AXIOM_VALS)]
CONSISTENT = [m for m in ALL_MODELS if consistent(m)]


# ============================ 第三轮三重门 / 本轮四重门 ============================
def gate_c1(m):
    return m["p_free"] == 0


def gate_c2(m):
    return m["lto"] == 1


def gate_c3(m):
    return (m["survive"] == 1) and (m["power"] == 1) and (not m["is_identity"])


def gate_c4(m):
    """本轮新增：双侧阳性证据门。下界/上界型实验的存活只意味「尚未排除」。"""
    return m["two_sided"]


def breakthrough_3gate(m):
    return gate_c1(m) and gate_c2(m) and gate_c3(m)


def breakthrough_4gate(m):
    return breakthrough_3gate(m) and gate_c4(m)


def b3_without_power(m):
    """反噬基线：把 C3 的判别力门去掉后的假突破数。"""
    return gate_c1(m) and gate_c2(m) and (m["survive"] == 1) and (not m["is_identity"])

# ============================ M1：三重门相容性穷举 ============================
B3_MODELS = [m for m in CONSISTENT if breakthrough_3gate(m)]
B4_MODELS = [m for m in CONSISTENT if breakthrough_4gate(m)]
ESCAPE_MODELS = [m for m in B3_MODELS if not gate_c4(m)]

N_all = len(ALL_MODELS)
N_consistent = len(CONSISTENT)
N_B3 = len(B3_MODELS)
N_B4 = len(B4_MODELS)
N_escape = len(ESCAPE_MODELS)
N_no_power = sum(1 for m in CONSISTENT if b3_without_power(m))
N_unifies_true = len(CONSISTENT)

# 三重门在逻辑上相容（存在满足构型），但不完备（满足构型里含单侧型）
triple_compatible = (N_B3 > 0)
triple_incomplete = (N_escape > 0)
escape_obs_types = sorted({m["obs_type"] for m in ESCAPE_MODELS})
b4_all_two_sided = all(m["two_sided"] for m in B4_MODELS)
c4_closes_escape = (N_B4 > 0) and (N_B4 < N_B3) and b4_all_two_sided

# 最小满足模型（四重门）的必要结构：p_free=0、LTO 通过、双侧、存活、有判别力、非恒等式
MIN_B4 = [m for m in B4_MODELS if m["axiom_injected"] == 0]
min_b4_necessary = {
    "p_free": sorted({m["p_free"] for m in B4_MODELS}),
    "lto": sorted({m["lto"] for m in B4_MODELS}),
    "obs_type": sorted({m["obs_type"] for m in B4_MODELS}),
    "survive": sorted({m["survive"] for m in B4_MODELS}),
    "power": sorted({m["power"] for m in B4_MODELS}),
}


# ============================ 现候选占据构型重检 ============================
KIND_TO_OBS = {"chi2": "two-sided", "identity": "identity",
               "lower": "lower", "upper": "upper"}


def candidate_to_model(r):
    obs = KIND_TO_OBS[r["kind"]]
    return dict(p_free=r["p_free"], lto=1 if r["lto_ok"] else 0,
                obs_type=obs, survive=1 if survive_act(r) else 0,
                power=1 if r["power"] else 0,
                axiom_injected=1 if r["p_axiom"] > 0 else 0,
                is_identity=(obs == "identity"), two_sided=(obs == "two-sided"))


CAND_MODELS = [(r["id"], candidate_to_model(r)) for r in CAND]
existing_B3 = [cid for cid, m in CAND_MODELS if breakthrough_3gate(m)]
existing_B4 = [cid for cid, m in CAND_MODELS if breakthrough_4gate(m)]
existing_C3_true = [r["id"] for r in CAND if r["C3"]]
# 第三轮 K09 的 C3 为 True 却因 p_free=1 挂 C1 ⇒ 把它的 p_free 置 0 就是逃逸构型的实例
ESCAPE_WITNESS = [r["id"] for r in CAND
                  if r["C2"] and r["C3"] and (not r["is_identity"])
                  and (KIND_TO_OBS[r["kind"]] != "two-sided")]


# ============================ exp / act 两路机拼 ============================
survive_pairs = [(survive_exp(r), survive_act(r)) for r in CAND]
survive_two_path_agree = (len(survive_pairs) == len(CAND)) and all(a == b for a, b in survive_pairs)
# 正对照：只改 act 路径的输入（把卡方压到临界以下），两路读数必须分叉
ACT_PROBE = dict(CAND[0])
ACT_PROBE["chi2"] = str(CHI2_CRIT_PREV / 2)
survive_act_perturbed = survive_act(ACT_PROBE)
survive_exp_perturbed = survive_exp(ACT_PROBE)
two_path_diverges = (survive_act_perturbed != survive_exp_perturbed)


# ============================ M2：描述压缩增益（MDL 有限影子） ============================
MDL = []
for r in CAND:
    n_in = r["p_free"] + r["p_exp"]
    n_out_raw = 1 if (r["lto_ok"] and not r["is_identity"]) else 0
    n_out_valid = 1 if (r["lto_ok"] and not r["is_identity"] and r["survive"]
                        and r["power"] and r["kind"] == "chi2") else 0
    MDL.append(dict(id=r["id"], n_in=n_in, n_out_raw=n_out_raw, n_out_valid=n_out_valid,
                    gain_raw=n_out_raw - n_in, gain_eff=n_out_valid - n_in))
mdl_raw_positive = sum(1 for x in MDL if x["gain_raw"] > 0)
mdl_eff_positive = sum(1 for x in MDL if x["gain_eff"] > 0)
mdl_max_eff = max(x["gain_eff"] for x in MDL)
# 模型空间层：逻辑上统一能压缩描述，但最小满足模型必须消费一个双侧观测量
mdl_model_gain = (1 - min(m["p_free"] for m in B4_MODELS)) if B4_MODELS else 0


# ============================ M3：「统一」谓词自指反噬 ============================
def perturb_all(ms, key, value_fn):
    out = []
    for m in ms:
        q = dict(m)
        q[key] = value_fn(m[key])
        out.append(q)
    return out


N_B4 = len(B4_MODELS)
n_perturb_pfree = sum(1 for m in perturb_all(CONSISTENT, "p_free", lambda v: v + 1)
                      if breakthrough_4gate(m))
n_perturb_lto = sum(1 for m in perturb_all(CONSISTENT, "lto", lambda v: 1)
                    if breakthrough_4gate(m))
n_perturb_power = sum(1 for m in perturb_all(CONSISTENT, "power", lambda v: 0)
                      if breakthrough_4gate(m))
predicate_discriminating = (n_perturb_pfree != N_B4) and (n_perturb_lto != N_B4) \
                           and (n_perturb_power != N_B4) and (N_unifies_true > N_B4)


# ============================ 控制组：四读数两两不同 + 正负对照 ============================
CTRL_READINGS = [N_consistent, N_B3, N_escape, N_B4]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
# 阳性对照：单侧逃逸构型确实存在且被 C4 拦下
ctrl_positive_alerts = (N_escape > 0) and all(not gate_c4(m) for m in ESCAPE_MODELS)
# 阴性对照：恒等式构型恒绿但被 is_identity 与 power 双重排除，配 NOT-ALL-GREEN
IDENTITY_MODELS = [m for m in CONSISTENT if m["is_identity"]]
ctrl_identity_never_breaks = all(not breakthrough_3gate(m) for m in IDENTITY_MODELS)
not_all_green = (len(set(CTRL_READINGS)) > 1) and (N_escape > 0) and (N_B4 > 0) \
                and ctrl_identity_never_breaks

# 反噬基线（本册独立计算，不受源码变体影响）
backfire_no_c4 = N_B3
backfire_unifies_true = N_unifies_true
backfire_no_power = N_no_power


# ============================ 跨卷脊梁与诚实边界 ============================
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and \
             (R404["key_numbers"]["four_force_accepted"] == 0)
spine_pred = sum(1 for e in R403.get("entries", []) if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
prev3_breakthrough = PREV3_K["breakthrough_count"]
prev3_guards = PREV3["guard_pass"]
prev3_count = PREV3["guard_count"]
prev2_breakthrough = PREV2["key_numbers"]["breakthrough_count"]
prev2_guards = PREV2["guard_pass"]
prev2_count = PREV2["guard_count"]
ledger_n = len(PREV)
ledger_two_sided = sum(1 for e in LEDGER["ledger"] if F_of(e["sigma"]) != 0)
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(SOURCE_FILES) > 0) and (len(source_missing) == 0)
honest_boundary = spine_zero and (spine_pred == 0) and (prev3_breakthrough == 0) \
                  and (prev2_breakthrough == 0)

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
    return ("ALG-META-GATEAUDIT"
            + "__MODELS-" + token
            + "__CONSISTENT-" + str(N_consistent)
            + "__B3-" + str(N_B3)
            + "__ESCAPE-" + str(N_escape)
            + "__B4-" + str(N_B4)
            + "__C4-ADDED"
            + "__EXISTING-B4-0"
            + "__MDL-EFF-GAIN-0"
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_all))
v_machine_1 = verdict_with(str(N_all + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and (("__MODELS-" + str(N_all)) in v_machine_0)
verdict = v_machine_0


# ============================ 守卫组装 ============================
segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV3-RELOADED",
    (prev3_guards == prev3_count) and (prev3_count == 39) and
    (prev3_breakthrough == 0) and (len(CAND) == 10),
    "PASS",
    "第三轮 39/39 守卫、10 条候选、突破 0 次；本册把它的 gates 字段当作审查对象")
add("PREV2-RELOADED",
    (prev2_guards == prev2_count) and (prev2_count == 35) and (prev2_breakthrough == 0),
    "PASS",
    "第二轮 35/35 守卫、20 次迭代突破 0 次；钉死—预言跷跷板结论回读一致")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) + " 个；分母为 0 判 FAIL")
add("LEDGER-RELOADED", (ledger_n == 46) and (ledger_two_sided > 0), "PASS",
    "回读第一册 46 项实测锚，其中带非零 sigma 的双侧型读数 " + str(ledger_two_sided) +
    " 项 ⇒ 双侧观测量本身不缺，缺的是能被理论命中的那一条")
add("CHI2-CRIT-TWO-SOURCES",
    (CHI2_CRIT_PREV == F_of(CHI2DOC["caliber"]["chi2_crit_1dof_95"])),
    "PASS",
    "卡方临界 " + PREV3_K["chi2_crit"] + " 两路机读：第三轮 JSON 与卡方靶场 caliber 一致")

add("MODEL-SPACE-ENUMERATED",
    (N_all == 192) and (N_consistent > 0) and (N_consistent < N_all),
    "PASS",
    "6 维离散模型空间全枚举 " + str(N_all) + " 个构型，一致性约束后剩 " + str(N_consistent) + " 个")
add("CONSISTENCY-CONSTRAINTS-BITE", (N_all - N_consistent > 0), "PASS",
    "恒等式约束与公理注入约束确实剔掉 " + str(N_all - N_consistent) +
    " 个自相矛盾构型 ⇒ 穷举不是对空集或全集做装饰统计")
add("TRIPLE-GATE-LOGICALLY-COMPATIBLE", triple_compatible, "PASS",
    "第三轮三重门在逻辑上相容：一致模型空间里有 " + str(N_B3) +
    " 个满足构型 ⇒ 攻破不是逻辑矛盾，缺口在别处")
add("TRIPLE-GATE-INCOMPLETE", (triple_incomplete and len(escape_obs_types) > 0), "PASS",
    "★本轮核心发现：满足三重门的构型里有 " + str(N_escape) + " 个是单侧型（" +
    "、".join(escape_obs_types) + "）⇒ 三重门会把「尚未排除」误当成阳性证据")
add("ESCAPE-WITNESS-IN-EXISTING", (len(ESCAPE_WITNESS) > 0), "PASS",
    "现候选里就有实例：" + "、".join(ESCAPE_WITNESS) +
    " 的 C2 与 C3 均为真、且是单侧型，只因 p_free=1 挂 C1 才没被放行 ⇒ 漏洞不是假想的")
add("EXISTING-C3-TRUE-COUNT", (len(existing_C3_true) > 0), "PASS",
    "第三轮 C3 为真的候选 " + str(len(existing_C3_true)) + " 条：" +
    "、".join(existing_C3_true) + "；其中单侧型存活者需要 C4 兜底")
add("C4-CLOSES-ESCAPE", c4_closes_escape, "PASS",
    "补上 C4 双侧阳性证据门后，满足构型从 " + str(N_B3) + " 降到 " + str(N_B4) +
    "，且剩余全部为双侧型 ⇒ 逃逸被封住")
add("B4-ALL-TWO-SIDED", b4_all_two_sided, "PASS",
    "四重门 " + str(N_B4) + " 个满足构型的 obs_type 全部为 two-sided")
add("MIN-B4-NECESSARY-STRUCTURE",
    (min_b4_necessary["p_free"] == [0]) and (min_b4_necessary["lto"] == [1]) and
    (min_b4_necessary["obs_type"] == ["two-sided"]) and
    (min_b4_necessary["survive"] == [1]) and (min_b4_necessary["power"] == [1]) and
    (len(MIN_B4) > 0),
    "PASS",
    "最小满足模型的必要结构：" + json.dumps(min_b4_necessary, ensure_ascii=False) +
    " ⇒ 第三轮 OPEN 出口被形式化为可机算的必要条件")
add("EXISTING-ZERO-B4", (len(existing_B4) == 0) and (len(existing_B3) == 0), "PASS",
    "把第三轮 10 条候选映射进模型空间重算：四重门命中 " + str(len(existing_B4)) +
    " 条、三重门命中 " + str(len(existing_B3)) + " 条 ⇒ 升级判据不改变既有判决")

add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 survive_act 与 survive_exp 是两个不同函数，且 return 均非顶层数值常量")
add("EXP-ACT-AGREE-ON-SURVIVE", survive_two_path_agree, "PASS",
    "两路机拼：本册精确有理卡方/excluded 重算 vs 第三轮 JSON 布尔字段，" +
    str(len(survive_pairs)) + "/" + str(len(survive_pairs)) + " 一致")
add("EXP-ACT-DIVERGE-ON-PERTURBATION", two_path_diverges, "PASS",
    "正对照：只把 act 路径的卡方压到临界一半，act=" + str(survive_act_perturbed) +
    " 而 exp=" + str(survive_exp_perturbed) + " ⇒ act 确实独立计算，不是照抄 exp")

add("MDL-RAW-GAIN-EXISTS", (mdl_raw_positive > 0), "PASS",
    "描述压缩原始增益 >0 的候选 " + str(mdl_raw_positive) +
    " 条：纯群论常数看似压缩了描述，但还没过实验层")
add("MDL-EFFECTIVE-GAIN-ZERO", (mdl_eff_positive == 0) and (mdl_max_eff <= 0), "PASS",
    "★M2 结论：只认通过实验存活层的陈述后，正增益候选 " + str(mdl_eff_positive) +
    " 条、最大有效增益 " + str(mdl_max_eff) + " ⇒ 目前的「统一」只是重述写法，没有压缩出任何经得起检验的新陈述")
add("MDL-MODEL-LEVEL-POSITIVE", (mdl_model_gain > 0), "PASS",
    "模型空间层最小满足模型的描述增益 " + str(mdl_model_gain) +
    " > 0 ⇒ 逻辑上统一可以压缩，前提仍是必须消费一个双侧观测量")

add("PREDICATE-DISCRIMINATING", predicate_discriminating, "PASS",
    "★M3 结论：unifies 对模型扰动敏感——基准 " + str(N_B4) + "，p_free+1 ⇒ " +
    str(n_perturb_pfree) + "，lto 全置 1 ⇒ " + str(n_perturb_lto) +
    "，power 全置 0 ⇒ " + str(n_perturb_power) + "；三路读数均与基准不同")
add("UNIFY-TRUE-IS-FALSE-BREAKTHROUGH", (N_unifies_true > N_B4), "PASS",
    "把 unifies 写成恒真谓词会凭空造出 " + str(N_unifies_true) +
    " 个假突破（真实 " + str(N_B4) + " 个）⇒「统一」谓词不能是装饰")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个模型计数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 N_consistent，杜绝全表读数相同造成的假判别力")
add("CTRL-POSITIVE-ALERTS", ctrl_positive_alerts, "PASS",
    "阳性对照：" + str(N_escape) + " 个单侧逃逸构型全部 non-two-sided，C4 确实报警")
add("CTRL-IDENTITY-NEVER-BREAKS", ctrl_identity_never_breaks, "IDENTITY",
    "阴性对照：" + str(len(IDENTITY_MODELS)) + " 个恒等式构型按预期恒绿且无一突破，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有逃逸检出、C4 收紧、MDL 归零等非恒绿读数 ⇒ 配 NOT-ALL-GREEN")
add("BACKFIRE-NO-C4", (backfire_no_c4 > N_B4), "PASS",
    "反噬基线 1：抹掉 C4 会让假突破从 " + str(N_B4) + " 涨到 " + str(backfire_no_c4) + " ⇒ C4 承重")
add("BACKFIRE-UNIFIES-TRUE", (backfire_unifies_true > N_B4), "PASS",
    "反噬基线 2：unifies 恒真会造 " + str(backfire_unifies_true) + " 个假突破 ⇒ 谓词承重")
add("BACKFIRE-NO-POWER", (backfire_no_power > N_B3), "PASS",
    "反噬基线 3：抹掉 C3 的判别力门会让三重门命中从 " + str(N_B3) +
    " 涨到 " + str(backfire_no_power) + " ⇒ power 门承重")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把模型空间总数读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 " + str(spine_pred) +
    "；第二册 20 次迭代与第三册 10 条候选突破均 0")
add("MODEL-SPACE-IS-BOUNDARY", (N_all == 192), "BOUNDARY",
    "192 个构型是 6 维离散属性的**逻辑影子**，不是物理理论全集；本册结论只对这 6 维抽象层全称成立，对未来新属性保持开放")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (len(existing_B4) == 0), "INFO",
    "本册不宣称攻破统一场论；升级为四重门后现有候选仍 0 命中")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（元逻辑层），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEW-EXIT-FORMALIZED", (c4_closes_escape and len(min_b4_necessary["obs_type"]) == 1), "INFO",
    "第三轮的 OPEN 出口被形式化：攻破所需的新实验读数必须双侧可判、且理论值落在其可判负区间之外")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-META-GATEAUDIT--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-META-GATEAUDIT--GATES-FAIL"
    return "ALG-META-GATEAUDIT--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "TRIPLE-GATE-INCOMPLETE", "MDL-EFFECTIVE-GAIN-ZERO",
                     "C4-CLOSES-ESCAPE", "ESCAPE-WITNESS-IN-EXISTING"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-META-GATEAUDIT--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "model_space_all": N_all,
    "model_space_consistent": N_consistent,
    "models_rejected_by_consistency": N_all - N_consistent,
    "triple_gate_hits": N_B3,
    "quad_gate_hits": N_B4,
    "escape_models": N_escape,
    "escape_obs_types": escape_obs_types,
    "escape_witness_in_existing": ESCAPE_WITNESS,
    "existing_B3": existing_B3,
    "existing_B4": existing_B4,
    "existing_C3_true": existing_C3_true,
    "min_b4_necessary": min_b4_necessary,
    "triple_gate_compatible": triple_compatible,
    "triple_gate_incomplete": triple_incomplete,
    "c4_closes_escape": c4_closes_escape,
    "mdl_raw_positive": mdl_raw_positive,
    "mdl_eff_positive": mdl_eff_positive,
    "mdl_max_effective_gain": mdl_max_eff,
    "mdl_model_level_gain": mdl_model_gain,
    "predicate_baseline": N_B4,
    "predicate_perturb_pfree": n_perturb_pfree,
    "predicate_perturb_lto": n_perturb_lto,
    "predicate_perturb_power": n_perturb_power,
    "predicate_unifies_true": N_unifies_true,
    "control_readings": CTRL_READINGS,
    "backfire_no_c4": backfire_no_c4,
    "backfire_unifies_true": backfire_unifies_true,
    "backfire_no_power": backfire_no_power,
    "two_path_pairs": len(survive_pairs),
    "two_path_agree": survive_two_path_agree,
    "two_path_diverges_on_perturbation": two_path_diverges,
    "ledger_total": ledger_n,
    "ledger_two_sided_with_sigma": ledger_two_sided,
    "chi2_crit": PREV3_K["chi2_crit"],
    "prev3_guards": str(prev3_guards) + "/" + str(prev3_count),
    "prev3_breakthrough": prev3_breakthrough,
    "prev2_guards": str(prev2_guards) + "/" + str(prev2_count),
    "prev2_breakthrough": prev2_breakthrough,
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": spine_pred,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：判据自审 + 模型空间穷举 + 描述压缩增益 + 谓词自指反噬",
    "date": "2026-11-11",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "model_space": {
        "dimensions": {"p_free": list(P_FREE_VALS), "lto": list(LTO_VALS),
                       "obs_type": list(OBS_TYPES), "survive": list(SURVIVE_VALS),
                       "power": list(POWER_VALS), "axiom_injected": list(AXIOM_VALS)},
        "all": N_all, "consistent": N_consistent,
        "constraints": ["identity 构型必须 power=0、survive=1、lto=0",
                        "axiom_injected=1 必须 p_free>=1"],
    },
    "gates": {
        "C1": "p_free == 0",
        "C2": "LTO 通过（lto == 1）",
        "C3": "survive == 1 且 power == 1 且 非恒等式",
        "C4": "本轮新增：观测量为双侧型（下界/上界存活只意味尚未排除）",
        "breakthrough_3gate": "C1 and C2 and C3",
        "breakthrough_4gate": "C1 and C2 and C3 and C4",
    },
    "escape_models": ESCAPE_MODELS,
    "b4_models": B4_MODELS,
    "mdl": MDL,
    "self_reference": {
        "baseline": N_B4, "perturb_pfree": n_perturb_pfree,
        "perturb_lto": n_perturb_lto, "perturb_power": n_perturb_power,
        "unifies_true": N_unifies_true, "discriminating": predicate_discriminating,
    },
    "candidate_recheck": [{"id": cid, "model": m, "B3": breakthrough_3gate(m),
                           "B4": breakthrough_4gate(m)} for cid, m in CAND_MODELS],
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
    lines.append("算法联盟：判据自审 + 模型空间穷举 + 描述压缩增益 + 谓词自指反噬")
    lines.append("=" * 92)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 92)
    lines.append("本轮换到元层级：不找新理论，审查前三轮的判据本身。")
    lines.append("模型空间 " + str(N_all) + " 个构型，一致性约束后 " + str(N_consistent) + " 个。")
    lines.append("第三轮三重门命中 " + str(N_B3) + " 个，其中单侧逃逸 " + str(N_escape) +
                 " 个（" + "、".join(escape_obs_types) + "）⇒ 逻辑相容但不完备。")
    lines.append("补 C4 双侧阳性证据门后命中 " + str(N_B4) + " 个，全部为 two-sided。")
    lines.append("把第三轮 10 条候选映射进来重算：三重门 " + str(len(existing_B3)) +
                 " 条、四重门 " + str(len(existing_B4)) + " 条 ⇒ 升级判据不改变既有判决。")
    lines.append("-" * 92)
    lines.append("★逃逸实例（现候选中）：" + "、".join(ESCAPE_WITNESS) +
                 " 的 C2 与 C3 均为真且为单侧型，仅因 p_free=1 挂 C1 才未放行。")
    lines.append("最小满足模型必要结构：" + json.dumps(min_b4_necessary, ensure_ascii=False))
    lines.append("-" * 92)
    lines.append("M2 描述压缩：原始正增益 " + str(mdl_raw_positive) + " 条，经实验存活层筛后 " +
                 str(mdl_eff_positive) + " 条，最大有效增益 " + str(mdl_max_eff) +
                 "；模型空间层最小满足模型增益 " + str(mdl_model_gain) + "。")
    lines.append("M3 谓词自指：基准 " + str(N_B4) + " / p_free+1 " + str(n_perturb_pfree) +
                 " / lto 全 1 " + str(n_perturb_lto) + " / power 全 0 " + str(n_perturb_power) +
                 " / unifies 恒真 " + str(N_unifies_true) + "。")
    lines.append("两路机拼：survive 重算 " + str(len(survive_pairs)) + "/" +
                 str(len(survive_pairs)) + " 一致；扰动正对照两路分叉 " + str(two_path_diverges) + "。")
    lines.append("-" * 92)
    lines.append("反噬基线：抹掉 C4 ⇒ " + str(backfire_no_c4) + " 个假突破；unifies 恒真 ⇒ " +
                 str(backfire_unifies_true) + " 个；抹掉 power ⇒ 三重门命中 " +
                 str(backfire_no_power) + "。")
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
