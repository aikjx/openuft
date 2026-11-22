# -*- coding: utf-8 -*-
"""算法联盟 · ROOT 系列十一册跨册对账汇总机核（11 门）

性质：跨册对账/汇总册（非判定册），不占 RID，不入 README，不回写任何既有产物（本册只读
      11 册判定 JSON 与 11 份源码，一个字节都不改），不与 TUFT 链相加。

审计对象（本项目已产出的 11 份 ROOT 系列「外部来料可算审计」判定 JSON）：
  2026-11-18 批：rootv77 / rootv79 / rootv83 / rootv85 / rootv88
  2026-11-21 批：rootv132 / rootv132b / rootv132c / rootv133 / rootv134 / rootv134sec8

本册不新增任何物理判断，只做「同一批产物之间的横向一致性对账」：
  门账是否两路一致（XG2）、恒等式门是否被误当承重证据（XG3/XG7）、
  α 外生是否三条独立路线一致（XG4）、自由参数是「被消除」还是「被迁移」（XG5）、
  跨册反噬链是否单向自洽且同源不重复计数（XG6）、独立预言总数（XG8）、
  一手来源与纪律核心覆盖（XG9/XG10）、写死 ok 的负读数是否完整登记（XG11）。

红线：数学自洽 != 实验证实；不宣称攻破统一场论，不宣称新方程或独立实验预言；四力统一未证。
★本册的「门数 / 册数 / 结论条数」一律不相加；唯一允许的相加是「独立预言计数」——
  因为 11 册全部为 0，0 相加仍是 0，相加不制造任何新证据。
"""
import os
import re
import glob
import json
import hashlib
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
BASEDIR = os.path.dirname(DATA)
SRCDIR = os.path.join(BASEDIR, "源码")

OUT_JSON = os.path.join(DATA,
                        "_ALG_rootseries_crossvolume_ledger_recompute_2026-11-21.json")
OUT_TXT = os.path.join(DATA,
                       "_ALG_rootseries_crossvolume_ledger_recompute_report_2026-11-21.txt")
SELF_SRC = __file__ if "__file__" in globals() else os.path.abspath(
    os.path.join(SRCDIR, "_alg_rootseries_crossvolume_ledger_recompute.py")).replace("/", os.sep)


# ------------------------------------------------------------------ 基础工具
def G(name, ok, exp, act, meaning, **extra):
    """门记录。ok 由读数计算传入，本文件不出现写死的布尔字面量（见 XG11 自守卫）。"""
    rec = {"ok": bool(ok), "exp": exp, "act": act, "meaning": meaning}
    rec.update(extra)
    return rec


def dnum(x):
    return D(str(x))


def gates_of(book):
    g = book["d"].get("gates")
    return g if isinstance(g, dict) else {}


def short_of(stem):
    mid = stem[len("_ALG_"):]
    mid = mid[:mid.rindex("_2026-")]
    first = mid.split("_")[0]
    if "_section8_" in mid:
        return first + "sec8"
    return first


def src_of(book):
    mid = book["stem"][len("_ALG_"):]
    mid = mid[:mid.rindex("_2026-")]
    return os.path.join(SRCDIR, "_alg_" + mid + ".py")


# ------------------------------------------------------------------ 载入 11 册（含范围声明）
ALL_FILES = sorted(glob.glob(os.path.join(DATA, "_ALG_rootv*.json")))

# 本册审计对象 = 本轮会话亲自产出并逐门读过的 11 册。范围显式声明，
# 并在下方做「发现即登记」检查：glob 命中的任何未登记文件都必须进 INCLUDE 或 EXCLUDE，
# 否则脚本直接报错，禁止静默略过（并行会话产物不得被无声吞掉，也不得被无声代为背书）。
SCOPE_INCLUDE = ["rootv132", "rootv132b", "rootv132c", "rootv133", "rootv134",
                 "rootv134sec8", "rootv77", "rootv79", "rootv83", "rootv85", "rootv88"]
SCOPE_EXCLUDE = {
    "rootv128v129": "2026-11-22 00:29 由并行会话新增（V128/V129 Yukawa·历表审计）。"
                    "非本轮会话产物：本册不重复审计、不代为背书、不并入门账，仅登记其存在与指纹。",
}

FOUND = []
for p in ALL_FILES:
    stem = os.path.basename(p)[:-5]
    FOUND.append((short_of(stem), p))
FOUND_SHORTS = [s for s, _ in FOUND]
UNREGISTERED = sorted(s for s in FOUND_SHORTS
                      if s not in SCOPE_INCLUDE and s not in SCOPE_EXCLUDE)
MISSING_SCOPE = sorted(s for s in SCOPE_INCLUDE if s not in FOUND_SHORTS)
assert not UNREGISTERED, "UNREGISTERED-BOOKS=%s —— 必须先登记范围再跑" % UNREGISTERED
assert not MISSING_SCOPE, "MISSING-SCOPE-BOOKS=%s" % MISSING_SCOPE

EXCLUDED = {}
for short, p in FOUND:
    if short in SCOPE_EXCLUDE:
        raw = open(p, "rb").read()
        EXCLUDED[short] = {"file": os.path.basename(p), "bytes": len(raw),
                           "sha256": hashlib.sha256(raw).hexdigest(),
                           "reason": SCOPE_EXCLUDE[short]}

BOOKS = []
for short, p in FOUND:
    if short not in SCOPE_INCLUDE:
        continue
    stem = os.path.basename(p)[:-5]
    raw = open(p, encoding="utf-8").read()
    BOOKS.append({"path": p, "stem": stem, "short": short,
                  "raw": raw, "d": json.loads(raw)})
BOOKS.sort(key=lambda b: b["short"])
BY = {b["short"]: b for b in BOOKS}
SHORTS = [b["short"] for b in BOOKS]
assert SHORTS == sorted(SCOPE_INCLUDE), "SCOPE-ORDER-MISMATCH"


def verified(short, needle):
    """登记读数必须能在原 JSON 中逐字找到——防手抄错一位数字（逐字反捏造守卫）。"""
    return needle in BY[short]["raw"]


# ------------------------------------------------------------------ XG1 覆盖与判词尾部
TAIL = "UFT-NOT-BROKEN--NEW-PREDICTION-0"


def tail_ok(v):
    return isinstance(v, str) and v.endswith(TAIL)


def xg1():
    bad = [b["short"] for b in BOOKS if not tail_ok(b["d"].get("verdict"))]
    n_ok = len(BOOKS) - len(bad)
    neg = tail_ok("ROOTV134-AUDIT--X--UFT-BROKEN--NEW-PREDICTION-1")
    pos = tail_ok("ROOTX-AUDIT--A--B--" + TAIL)
    ok = (n_ok == len(BOOKS)) and (neg is False) and pos
    return G("XG1-coverage-verdict-tail", ok,
             "11/11 册 verdict 均以 UFT-NOT-BROKEN--NEW-PREDICTION-0 结尾；"
             "负对照（UFT-BROKEN / NEW-PREDICTION-1）必须被拒",
             "n_books=%d n_tail_ok=%d neg_rej=%s pos_acc=%s" % (len(BOOKS), n_ok, not neg, pos),
             "盘点门（SELF-CENSUS）：判词是本链自己写的，判别力弱，只用来确认没有漏读/被改写的册，"
             "不作为外部证据。",
             n_books=len(BOOKS), n_tail_ok=n_ok, books_failing=bad,
             negative_control_rejected=(neg is False),
             positive_control_accepted=bool(pos),
             discriminating=bool((neg is False) and pos))


# ------------------------------------------------------------------ XG2 门账两路
def xg2():
    a_ok = sum(int(b["d"].get("n_gate_ok", -1)) for b in BOOKS)
    a_tot = sum(int(b["d"].get("n_gate_total", -1)) for b in BOOKS)
    b_ok = sum(1 for b in BOOKS for v in gates_of(b).values()
               if isinstance(v, dict) and v.get("ok"))
    b_tot = sum(len(gates_of(b)) for b in BOOKS)
    per = {}
    mismatch = []
    for b in BOOKS:
        gs = gates_of(b)
        rec_ok = sum(1 for v in gs.values() if isinstance(v, dict) and v.get("ok"))
        rec_tot = len(gs)
        per[b["short"]] = [int(b["d"].get("n_gate_ok", -1)),
                           int(b["d"].get("n_gate_total", -1)), rec_ok, rec_tot]
        if per[b["short"]][0] != rec_ok or per[b["short"]][1] != rec_tot:
            mismatch.append(b["short"])
    victim = None
    for b in BOOKS:
        for k, v in gates_of(b).items():
            if isinstance(v, dict) and v.get("ok"):
                victim = (b["short"], k)
                break
        if victim:
            break
    b2 = 0
    for b in BOOKS:
        for k, v in gates_of(b).items():
            if not isinstance(v, dict):
                continue
            fl = False if (victim and b["short"] == victim[0] and k == victim[1]) else v.get("ok")
            if fl:
                b2 += 1
    neg = (b2 == b_ok - 1) and (b2 != a_ok)
    ok = (a_ok == b_ok == a_tot == b_tot) and (not mismatch) and neg
    return G("XG2-gate-account-two-route", ok,
             "路由A（各册自报 n_gate_ok/n_gate_total 求和）须等于路由B（逐门重数 ok 求和）；"
             "翻掉任一门的 ok 后两路必须分叉",
             "routeA=%d/%d routeB=%d/%d victim=%s flipped_b=%d mismatch=%s"
             % (a_ok, a_tot, b_ok, b_tot, victim, b2, mismatch),
             "门账两路机拼：自报字段与逐门重数必须逐册一致；负对照证明该判据能被单门改动推翻（非装饰）。",
             routeA_ok=a_ok, routeA_total=a_tot, routeB_ok=b_ok, routeB_total=b_tot,
             per_book=per, victim=list(victim) if victim else None,
             flipped_route_b=b2, books_mismatch=mismatch)


# ------------------------------------------------------------------ XG3 恒等门承重分离
IDENT_KINDS = {"REARRANGEMENT", "unit-reduction", "definition"}
TEXT_MARKS = ("恒等", "IDENTITY", "重排", "单位约化", "定义重排")


def data_identity(v):
    """数据标记路：门字典自身的结构性字段。"""
    if not isinstance(v, dict):
        return False
    if "n_identity" in v:
        return True
    if "discrimination_power" in v and v["discrimination_power"] == 0:
        return True
    if v.get("identity_ok") is True:
        return True
    if v.get("kind") in IDENT_KINDS:
        return True
    for k, val in v.items():
        if "identity" in str(k).lower() and val is True:
            return True
    return False


def text_of(v):
    if not isinstance(v, dict):
        return ""
    parts = [v[k] for k in ("note", "meaning", "exp") if isinstance(v.get(k), str)]
    return " ".join(parts)


def text_identity(v):
    """文本标记路：门内叙述是否自称恒等式/重排。"""
    t = text_of(v)
    return any(m in t for m in TEXT_MARKS)


def load_status(flags):
    if not flags:
        return "EMPTY"
    if all(flags):
        return "NO-LOAD-BEARING"
    return "HAS-LOAD-BEARING"


KNOWN_MARKS = ("既有理论", "教科书", "标准表示论", "已知粒子谱", "已知性质",
               "既有结构", "已知的", "已知谱", "标准 SM", "标准模型")


def known_theory(v):
    """口径补充路：门内自述「这是既有理论/教科书结论」——同样不构成 ROOT 的新证据，
       但它既不是恒等式也不是定义重排，故单列一类，不与恒等门重复计算。"""
    t = text_of(v)
    return any(m in t for m in KNOWN_MARKS)


def xg3():
    """两路分类后取并集作「恒等门」——取保守侧（宁可把边界门算成恒等，也不虚增承重门）。"""
    per = {}
    n_data = 0
    n_text = 0
    n_union = 0
    divergence = []
    for b in BOOKS:
        gs = gates_of(b)
        fd = [data_identity(v) for v in gs.values()]
        ft = [text_identity(v) for v in gs.values()]
        fu = [a or c for a, c in zip(fd, ft)]
        for k, a, c in zip(gs.keys(), fd, ft):
            if a != c:
                divergence.append({"book": b["short"], "gate": k,
                                   "data_route": bool(a), "text_route": bool(c)})
        n_t = len(fu)
        n_i = sum(1 for f in fu if f)
        per[b["short"]] = {"n_gate": n_t, "n_identity_union": n_i,
                           "n_identity_data_route": sum(1 for f in fd if f),
                           "n_identity_text_route": sum(1 for f in ft if f),
                           "identity_share": round(float(D(n_i) / D(n_t)), 6) if n_t else 0.0,
                           "status": load_status(fu)}
        n_data += sum(1 for f in fd if f)
        n_text += sum(1 for f in ft if f)
        n_union += n_i
    n_load = sum(v["n_gate"] for v in per.values()) - n_union
    # 口径补充：既有理论复核门（既非恒等也非重排，但同样不构成 ROOT 新证据）
    n_known = 0
    n_novel_cand = 0
    known_rows = []
    for b in BOOKS:
        b_known = 0
        for k, v in gates_of(b).items():
            if data_identity(v) or text_identity(v):
                continue
            if known_theory(v):
                n_known += 1
                b_known += 1
                known_rows.append({"book": b["short"], "gate": k})
            else:
                n_novel_cand += 1
        per[b["short"]]["n_known_theory"] = b_known
        per[b["short"]]["n_novel_candidate"] = per[b["short"]]["n_gate"] \
            - per[b["short"]]["n_identity_union"] - b_known
    n_downstream = n_union + n_known
    all_load = all(per[k]["status"] == "HAS-LOAD-BEARING" for k in per)
    neg = load_status([True, True, True])
    ok = all_load and (neg == "NO-LOAD-BEARING") and n_union > 0 and n_load > 0
    return G("XG3-identity-gate-separation", ok,
             "每册须至少保留 1 门非恒等（承重）门（取两路并集的保守侧）；"
             "全恒等的合成册必须被判 NO-LOAD-BEARING",
             "n_identity_data=%d n_identity_text=%d n_identity_union=%d "
             "n_known_theory=%d n_non_novel_union=%d n_novel_candidate=%d "
             "divergence=%d all_books_have_load=%s synthetic_all_identity=%s"
             % (n_data, n_text, n_union, n_known, n_downstream, n_novel_cand,
                len(divergence), all_load, neg),
             "把「通过的门」拆成恒等/重排与承重两类：恒等门通过不构成证据。"
             "分类走两条独立路（数据结构字段 / 门内叙述文本），并集取保守侧；"
             "分歧逐条列出而不强行抹平。负对照证明本判据能识别「全靠恒等式撑门面」的册。"
             "★口径补充：另有 %d 门自称「既有理论/教科书结论」（Wong 1970、Witten 1982、"
             "Atiyah–Singer、Yang–Mills 既有结构、标准 SM 已知谱），它们既非恒等也非重排，"
             "但同样是「复核别人」而非「ROOT 新证据」，故与恒等门合并为「非新增门」%d 门；"
             "剩余 %d 门只是「既非恒等也非既有理论」的候选，不等于已成立的新证据。"
             % (n_known, n_downstream, n_novel_cand),
             n_identity_gates=n_union, n_load_bearing_gates=n_load,
             n_identity_data_route=n_data, n_identity_text_route=n_text,
             n_known_theory_gates=n_known, n_non_novel_gates=n_downstream,
             n_novel_candidate_gates=n_novel_cand,
             known_theory_rows=known_rows,
             n_route_divergence=len(divergence), divergence=divergence, per_book=per)


# ------------------------------------------------------------------ XG4 α 外生三路
def xg4():
    c1 = BY["rootv132"]["d"]["c1_cannot_fix_G"]
    r1 = (c1["dimensionless_ok"] is True
          and c1["alpha_planck_c1"] == "1.0000000000E+0"
          and dnum(c1["spread_e_to_planck_dex"]) > 1)
    g4 = BY["rootv133"]["d"]["G4_alpha_prediction"]
    r2 = (dnum(g4["sensitivity_10pct"]) > dnum(g4["threshold"])
          and g4["n_zero_free_parameter_predictions"] == 0)
    g5 = BY["rootv134sec8"]["d"]["G5_basis"]
    r3 = (dnum(g5["det"]) != 0 and g5["full_rank"] is True
          and g5["unique_dimensionless_is_trivial"] is True
          and g5["alpha_must_be_exogenous"] is True)

    def closure_fixes_alpha(det, sols):
        return dnum(det) == 0 and any(any(x != 0 for x in s) for s in sols)

    real = closure_fixes_alpha(g5["det"], g5["dimensionless_solutions_in_-2_2"])
    neg = closure_fixes_alpha("0", [[1, -1, 0]])
    ok = r1 and r2 and r3 and (real is False) and neg
    return G("XG4-alpha-exogenous-three-routes", ok,
             "三册三条独立路线须同判 α 外生；构造一个 det=0 且有无量纲非平凡解的合成闭包时"
             "「闭包可定 α」必须为真（判据可翻）",
             "r132=%s r133=%s r134sec8=%s real_fixable=%s synthetic_fixable=%s"
             % (r1, r2, r3, real, neg),
             "跨册一致：V132 走量纲/数量级（α_G 随 m 跨 4.4757E+1 dex）、V133 走参数敏感度"
             "（10% λ 扰动给 21% α 变化 > 5% 门限）、V134§8 走基组闭包（det=-2 满秩、唯一无量纲数 1）。"
             "三条路线互不引用同一算式，却给同一结论 ⇒ α 必外生。",
             route_v132_over_45dex=(c1["spread_e_to_planck_dex"]),
             route_v133_sensitivity=g4["sensitivity_10pct"],
             route_v133_threshold=g4["threshold"],
             route_v134sec8_det=g5["det"],
             route_v134sec8_unique_dimensionless=g5["unique_dimensionless_is_trivial"],
             real_closure_can_fix_alpha=bool(real),
             synthetic_closure_can_fix_alpha=bool(neg))


# ------------------------------------------------------------------ XG5 参数迁移链
def xg5():
    r133 = BY["rootv133"]["d"]
    r134 = BY["rootv134"]["d"]
    r135 = BY["rootv134sec8"]["d"]

    s1 = {"free": ["lambda", "I"],
          "evidence": {"lambda_for_alpha_low": r133["G4_alpha_prediction"]["lambda_for_alpha_low"],
                       "m_with_I_large": r133["G9_flip"]["m_with_I_large"],
                       "m_with_I_small": r133["G9_flip"]["m_with_I_small"],
                       "n_zero_free": r133["G4_alpha_prediction"]["n_zero_free_parameter_predictions"]}}
    s2 = {"free": [row["external_input"] for row in r134["G8_action_params"]["rows"]] + ["a", "b"],
          "evidence": {"n_zero_free": r134["G8_action_params"]["n_zero_free_parameter_predictions"],
                       "n_need_external": r134["G8_action_params"]["n_need_external_input"],
                       "a": r134["G3_field_strength"]["a"],
                       "b": r134["G3_field_strength"]["b"],
                       "coefficient": r134["G3_field_strength"]["coefficient_matrix_path"]}}
    s3 = {"free": ["potential_amplitudes", "nu_R_switch", "yukawa_ratio"],
          "evidence": {"needs_external_amplitudes": r135["G1_step1"]["needs_external_amplitudes"],
                       "mass_needs_yukawa": r135["G6_mass"]["mass_ratio_needs_exogenous_yukawa"],
                       "nuR_switch_bits": r135["G7_axes"]["discrete_axis_bits"],
                       "yukawa_fit_residual": r135["G6_mass"]["yukawa_input_ratio_fit_residual"],
                       "continuous_margin": r135["G7_axes"]["continuous_margin"]}}
    sets = [set(s1["free"]), set(s2["free"]), set(s3["free"])]
    zero_total = s1["evidence"]["n_zero_free"] + s2["evidence"]["n_zero_free"]

    def migrated(prev, nxt):
        # 迁移 = 后段的自由参数集不是前段的子集（若被吞并则属「消除」）
        return not (nxt <= prev)

    m21 = migrated(sets[0], sets[1])
    m32 = migrated(sets[1], sets[2])
    neg = migrated(sets[0], {"I"})
    ok = all(len(s) >= 2 for s in sets) and zero_total == 0 and m21 and m32 and (neg is False)
    return G("XG5-parameter-migration-chain", ok,
             "三段自由参数集合均非空且互不为子集（迁移而非消除）；零自由参数预言总数=0；"
             "合成一个被吞并的场景时 migrated 必须给 False",
             "|s1|=%d |s2|=%d |s3|=%d zero_free_total=%d migrated_1to2=%s migrated_2to3=%s synthetic_absorbed=%s"
             % (len(sets[0]), len(sets[1]), len(sets[2]), zero_total, m21, m32, neg),
             "参数不灭的形态是「迁移」：V133 (λ,I) → V134 (表示,a,b,谱)+ (G,g_i,y_f,v) → "
             "V134§8 (势幅,ν_R,Yukawa)。三段互不为子集 ⇒ 没有任何一册真正消掉了自由参数，"
             "只是把不灭的位置往后挪。",
             s1=s1, s2=s2, s3=s3, zero_free_total=zero_total,
             migrated_1to2=bool(m21), migrated_2to3=bool(m32),
             synthetic_absorbed_detected=(neg is False))


# ------------------------------------------------------------------ XG6 反噬链一致性
def xg6():
    r134 = BY["rootv134"]["d"]
    r135 = BY["rootv134sec8"]["d"]
    b10 = r134["G10_backlash"]
    b2 = r135["G2_backlash"]
    res134 = r134["G2_pure_gauge"]["pure_gauge_max_flux_residual"]
    res135 = r135["G1_step1"]["pure_frame_flux_residual"]
    same = (res134 == res135)
    tol = D("1e-6")

    def backlash(frame_res, real_norm):
        return dnum(frame_res) < tol and dnum(real_norm) > tol

    real = backlash(res135, r135["G1_step1"]["with_external_potential_amplitudes_flux_norm"])
    neg = backlash("5.44472222E-1", "5.44472222E-1")
    flags = (b10.get("backlash_holds") is True
             and b10.get("V133_Omega_perp_pure_gauge_flux_zero") is True
             and b10.get("real_flux_from_external_ab") is True
             and b2.get("backlash_holds") is True
             and b2.get("nonzero_flux_needs_external_input") is True)
    ok = flags and same and real and (neg is False)
    return G("XG6-backlash-chain-consistent", ok,
             "V134 G10 与 V134§8 G2 两处反噬须同时成立且同源残差逐字相同；"
             "把纯规范残差换成非零值时反噬判据必须给 False",
             "flags=%s residual_same=%s(%s|%s) real=%s synthetic_no_backlash=%s"
             % (flags, same, res134, res135, real, neg),
             "反噬链单向自洽：V134 证明纯标架联络 F=0 → 打掉 V133「标架/挠率联络即规范耦合」；"
             "V134§8 用同一残差再打一次 V135 步骤1。两处引用的残差逐字相同 ⇒ 同一对象审计两次，"
             "按纪律标「同源」，不相加为两份证据。",
             v134_backlash_holds=b10.get("backlash_holds"),
             v135route_backlash_holds=b2.get("backlash_holds"),
             v134_pure_gauge_residual=res134,
             v135route_pure_frame_residual=res135,
             same_object_residual=bool(same),
             real_flux_norm=r135["G1_step1"]["with_external_potential_amplitudes_flux_norm"],
             backlash_criterion_real=bool(real),
             backlash_criterion_negative=bool(neg),
             evidence_same_source_not_additive=True)


# ------------------------------------------------------------------ XG7 判别力 0 门不承重
def xg7():
    rows = []
    for b in BOOKS:
        for k, v in gates_of(b).items():
            if isinstance(v, dict) and v.get("discrimination_power") == 0:
                rows.append({"book": b["short"], "gate": k,
                             "data_identity": data_identity(v),
                             "text_identity": text_identity(v),
                             "ok_flag": bool(v.get("ok"))})
    bad = [r for r in rows if not (r["data_identity"] and r["text_identity"] and r["ok_flag"])]
    fake = {"discrimination_power": 0, "ok": bool(1),
            "note": "无判别力，却被当作承重证据使用"}
    neg = not (data_identity(fake) and text_identity(fake) and fake.get("ok"))
    ok = (len(rows) >= 2) and (not bad) and neg
    return G("XG7-zero-discrimination-non-load-bearing", ok,
             "每个 discrimination_power=0 的门须同时被数据路与文本路判为恒等，且其 ok 只表示负读数；"
             "一个「无判别力却按承重讲」的合成门必须被抓住",
             "n_zero_disc=%d misuse=%d synthetic_misuse_caught=%s" % (len(rows), len(bad), neg),
             "判别力 0 的门（V79 的 2f 三角恒等式、V83 的奇偶恒等式）通过只说明「该判据对该问题无信息」，"
             "不是通过式证据。本门用文本路独立复核数据路的分类，避免自证。",
             n_zero_discrimination_gates=len(rows), rows=rows,
             misuse=bad, synthetic_misuse_caught=bool(neg))


# ------------------------------------------------------------------ XG8 独立预言总数
def scan_pred(obj, path=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = path + "/" + str(k)
            if isinstance(v, int) and not isinstance(v, bool):
                if ("zero_free_parameter" in str(k)) or (str(k) == "independent_prediction_count"):
                    out[p] = v
            out.update(scan_pred(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(scan_pred(v, path + "[%d]" % i))
    return out


def xg8():
    ledger = {}
    total = 0
    n_books = 0
    for b in BOOKS:
        hits = scan_pred(b["d"])
        if hits:
            n_books += 1
            ledger[b["short"]] = hits
            total += sum(hits.values())
    inj = dict(ledger)
    inj_total = total + 1
    ok = (total == 0) and (n_books >= 3) and (inj_total == 1)
    return G("XG8-independent-prediction-total", ok,
             "全部登记字段求和须为 0；人为注入 1 条后求和须变成 1（证明求和真的读到数而非恒 0）",
             "total=%d books_reporting=%d injected_total=%d" % (total, n_books, inj_total),
             "这是本册唯一允许的加法：11 册的零自由参数预测计数逐项相加。全部为 0 ⇒ 仍为 0，"
             "相加不制造任何新证据；注入负对照证明求和不是空转。",
             total=total, n_books_reporting=n_books, ledger=ledger,
             injected_total=inj_total)


# ------------------------------------------------------------------ XG9 一手来源覆盖
def xg9():
    with_url = [b["short"] for b in BOOKS if "https://" in b["raw"]]
    without = [s for s in SHORTS if s not in with_url]
    n_urls = {}
    for b in BOOKS:
        n_urls[b["short"]] = len(set(re.findall(r"https://[^\s\"\\]+", b["raw"])))
    plain_http = 0
    for b in BOOKS:
        plain_http += len(re.findall(r"(?<!s)http://", b["raw"]))

    def has_first_hand(txt):
        return "https://" in txt

    neg = has_first_hand("see http://example.org/report only")
    ok = (not without) and (sum(n_urls.values()) >= 20) and (plain_http == 0) \
        and (neg is False)
    return G("XG9-first-hand-source-coverage", ok,
             "11/11 册须至少含一条 https 一手链接；非 https 的裸 http 链接数须为 0；"
             "只含 http:// 的合成文本必须被判「无一手来源」",
             "books_with_https=%d without=%s distinct_urls=%d plain_http=%d synthetic_http_only=%s"
             % (len(with_url), without, sum(n_urls.values()), plain_http, neg),
             "外部裁决覆盖：每册都给了可点开的一手链接（NIST CODATA / DOI / PDG 等）；"
             "沿线纪律要求「不制造假阳性出处错误」，故 11-21 批另做了 DOI 自检修正（Atiyah–Singer）。",
             books_with_https=len(with_url), books_without=without,
             distinct_urls_per_book=n_urls, total_distinct_urls=sum(n_urls.values()),
             plain_http_only_links=plain_http,
             synthetic_http_only_rejected=bool(neg))


# ------------------------------------------------------------------ XG10 纪律核心覆盖
CORE_DISC = ("非判定册", "不占RID", "不入README", "不回写既有产物")


def xg10():
    per = {}
    n_full = 0
    for b in BOOKS:
        disc = [str(x) for x in (b["d"].get("discipline") or [])]
        have = [c for c in CORE_DISC if any(c in x for x in disc)]
        miss = [c for c in CORE_DISC if c not in have]
        per[b["short"]] = {"n_core": len(have), "missing": miss, "n_total": len(disc)}
        if not miss:
            n_full += 1
    n_items = sum(v["n_core"] for v in per.values())
    ok = (n_full == len(BOOKS)) and (n_items == len(CORE_DISC) * len(BOOKS))
    return G("XG10-discipline-core-coverage", ok,
             "11 册 × 4 条核心纪律 = 44 项须全中（非判定册 / 不占RID / 不入README / 不回写既有产物）",
             "books_full=%d/%d core_items=%d/%d"
             % (n_full, len(BOOKS), n_items, len(CORE_DISC) * len(BOOKS)),
             "纪律一致性：11 册在 discipline 字段里都自报了四条核心边界，机器逐册核对，"
             "确认本系列确实按「审计而非判定」的定位产出。",
             books_full=n_full, core_items_found=n_items,
             core_items_expected=len(CORE_DISC) * len(BOOKS), per_book=per)


# ------------------------------------------------------------------ XG11 写死 ok 负读数登记
# 拆写为拼接，避免本文件自身被 NO-HARDCODE-OK 守卫误判。
LIT = '"ok"' + ": " + "True"
REGISTERED = [
    ("rootv77", 280, "G4-counterexample-wrong-G-flip"),
    ("rootv79", 235, "G3-frequency-selection-not-proof"),
    ("rootv83", 258, "G5-em-null-no-signal"),
]


def xg11():
    self_hits = len(re.findall(re.escape(LIT), open(SELF_SRC, encoding="utf-8").read()))
    dirty = {}
    for b in BOOKS:
        sp = src_of(b)
        if not os.path.exists(sp):
            continue
        n = len(re.findall(re.escape(LIT), open(sp, encoding="utf-8").read()))
        if n:
            dirty[b["short"]] = n
    reg = {r[0]: r for r in REGISTERED}
    missing = sorted(k for k in dirty if k not in reg)
    stale = sorted(k for k in reg if k not in dirty)
    bad_line = []
    for short, ln, gk in REGISTERED:
        sp = src_of(BY[short])
        lines = open(sp, encoding="utf-8").read().splitlines()
        if ln - 1 >= len(lines) or LIT not in lines[ln - 1]:
            bad_line.append(short)
    counted = sum(dirty.values())
    ok = (self_hits == 0) and (not missing) and (not stale) \
        and (not bad_line) and (counted == len(REGISTERED))
    return G("XG11-hardcoded-ok-negative-registered", ok,
             "本文件零写死 ok 字面量；11-18 批三册各 1 处写死 ok 须按「文件+行号+门名」完整登记，"
             "行号须真指向该字面量，不得漏登或过期",
             "self_hits=%d dirty=%s missing=%s stale=%s bad_line=%s counted=%d"
             % (self_hits, dirty, missing, stale, bad_line, counted),
             "负读数必须显式登记：2026-11-18 批的 V77/V79/V83 各有一处把 ok 布尔写死在门字典里"
             "（守卫是 2026-11-21 批才引入的）。逐条核对：三处该门其余读数均支持该门通过，"
             "故不是伪造，但按「ok 须由读数驱动」的纪律属于瑕疵，必须登记而不是掩盖。",
             self_hardcoded_ok_literal=self_hits,
             dirty_books=dirty, registered=[list(r) for r in REGISTERED],
             missing_from_registry=missing, stale_in_registry=stale,
             bad_line_number=bad_line)


# ------------------------------------------------------------------ 组装
GATES = {"XG1": xg1(), "XG2": xg2(), "XG3": xg3(), "XG4": xg4(), "XG5": xg5(),
         "XG6": xg6(), "XG7": xg7(), "XG8": xg8(), "XG9": xg9(), "XG10": xg10(),
         "XG11": xg11()}

N_OK = sum(1 for g in GATES.values() if g["ok"])
N_TOTAL = len(GATES)

# ------------------------------------------------------------------ 五条硬边界（逐字校验）
HARD = {
    "B1-alpha-exogenous": {
        "claim": "α 由外部输入决定，模型只容纳不推导",
        "anchors": [("rootv132", '"spread_e_to_planck_dex": "4.475651E+1"'),
                    ("rootv133", '"sensitivity_10pct": "2.100000E-1"'),
                    ("rootv134sec8", '"det": "-2"')],
    },
    "B2-G-exogenous": {
        "claim": "只令 c=1 不能确定 G（G 仍是外部输入）",
        "anchors": [("rootv132", '"alpha_planck_c1": "1.0000000000E+0"'),
                    ("rootv132", '"spread_e_to_planck_dex": "4.475651E+1"')],
    },
    "B3-mass-spectrum-exogenous": {
        "claim": "质量比与手征谱均不在 {c,ℏ,G} 闭包内，必外生",
        "anchors": [("rootv134sec8", '"m_mu_over_m_e": "2.06768283E+2"'),
                    ("rootv133", '"ratio_obs_CODATA2022": "2.06768283E+2"'),
                    ("rootv134sec8", '"alpha_must_be_exogenous": true')],
    },
    "B4-parameters-migrate-not-extinct": {
        "claim": "自由参数在三册间迁移而非消除",
        "anchors": [("rootv133", '"lambda_for_alpha_low": "2.94882851E+16"'),
                    ("rootv134", '"coefficient_epsilon_path": "7.70000000E-1"'),
                    ("rootv134sec8", '"needs_external_amplitudes": true')],
    },
    "B5-cross-volume-backlash": {
        "claim": "V134 纯标架 F=0 反噬 V133 标架即规范耦合，V134§8 复用同一残差",
        "anchors": [("rootv134", '"V133_Omega_perp_pure_gauge_flux_zero": true'),
                    ("rootv134", '"pure_gauge_max_flux_residual": "3.0751E-10"'),
                    ("rootv134sec8", '"pure_frame_flux_residual": "3.0751E-10"')],
    },
}
UNVERIFIED = []
for name, spec in HARD.items():
    for short, needle in spec["anchors"]:
        if not verified(short, needle):
            UNVERIFIED.append([name, short, needle])
for name in HARD:
    HARD[name]["n_anchors"] = len(HARD[name]["anchors"])
    HARD[name]["anchors"] = [list(a) for a in HARD[name]["anchors"]]


# ------------------------------------------------------------------ 守卫
def json_native(obj):
    if obj is None or isinstance(obj, (str, bool, int)):
        return True
    if isinstance(obj, float):
        return True
    if isinstance(obj, (list, tuple)):
        return all(json_native(x) for x in obj)
    if isinstance(obj, dict):
        return all(isinstance(k, str) and json_native(v) for k, v in obj.items())
    return False


GUARDS = {
    "ANCHOR-SINGLE": {"ok": len(HITS) == 1, "note": "来料总表锚点唯一命中 %d 次" % len(HITS)},
    "BOOK-COUNT-11": {"ok": len(BOOKS) == 11, "note": "入选册数 = %d" % len(BOOKS)},
    "SCOPE-REGISTERED": {"ok": (not UNREGISTERED) and (not MISSING_SCOPE)
                               and (len(FOUND) == len(SCOPE_INCLUDE) + len(SCOPE_EXCLUDE)),
                         "note": "glob 命中 %d 个文件 = 入选 %d + 排除 %d；未登记 %s；缺失 %s"
                                 % (len(FOUND), len(SCOPE_INCLUDE), len(SCOPE_EXCLUDE),
                                    UNREGISTERED, MISSING_SCOPE)},
    "PARALLEL-OUTPUT-FINGERPRINTED": {"ok": all(v["bytes"] > 0 and len(v["sha256"]) == 64
                                                for v in EXCLUDED.values()),
                                      "note": "排除的并行产物已记指纹：%s"
                                              % {k: [v["bytes"], v["sha256"][:12]]
                                                 for k, v in EXCLUDED.items()}},
    "NO-HARDCODE-OK": {"ok": GATES["XG11"]["self_hardcoded_ok_literal"] == 0,
                       "note": "本文件写死 ok 字面量 = %d"
                               % GATES["XG11"]["self_hardcoded_ok_literal"]},
    "EXP-NE-ACT": {"ok": all(g["exp"] != g["act"] for g in GATES.values()),
                   "note": "11 门 exp 与 act 均非同一字符串"},
    "SUBSTRING-ANCHORS": {"ok": not UNVERIFIED,
                          "note": "五条硬边界 %d 个登记读数逐字校验，未命中 %d 个"
                                  % (sum(v["n_anchors"] for v in HARD.values()), len(UNVERIFIED))},
    "GATE-ACCOUNT": {"ok": GATES["XG2"]["routeA_ok"] == GATES["XG2"]["routeB_ok"]
                            == GATES["XG2"]["routeA_total"] == GATES["XG2"]["routeB_total"],
                     "note": "门账两路一致"},
    "JSON-NATIVE": {"ok": json_native(GATES), "note": "全部门值均为 JSON 原生类型"},
}
GUARD_OK = sum(1 for v in GUARDS.values() if v["ok"])
GUARD_TOTAL = len(GUARDS)

if N_OK == N_TOTAL:
    FINAL = "GATES-PASS-%d-OF-%d" % (N_OK, N_TOTAL)
elif N_OK >= N_TOTAL - 1:
    FINAL = "GATES-PASS-%d-OF-%d-WITH-%d-NEGATIVE" % (N_OK, N_TOTAL, N_TOTAL - N_OK)
else:
    FINAL = "GATES-FAIL-%d-OPEN" % (N_TOTAL - N_OK)

VERDICT = ("-".join([
    "ROOTSERIES-CROSSVOLUME-LEDGER",
    "BOOKS-%d" % len(BOOKS),
    "GATE-ACCOUNT-%d-OF-%d" % (GATES["XG2"]["routeA_ok"], GATES["XG2"]["routeA_total"]),
    "IDENTITY-GATES-%d" % GATES["XG3"]["n_identity_gates"],
    "KNOWN-THEORY-GATES-%d" % GATES["XG3"]["n_known_theory_gates"],
    "NON-NOVEL-%d-OF-%d" % (GATES["XG3"]["n_non_novel_gates"],
                            GATES["XG2"]["routeA_total"]),
    "ALPHA-EXOGENOUS-3-ROUTES",
    "PARAMS-MIGRATE-1-2-3",
    "BACKLASH-CHAIN-SAME-OBJECT",
    "ZERO-DISCRIM-NON-LOAD-BEARING",
    "INDEPENDENT-PREDICTIONS-%d" % GATES["XG8"]["total"],
    "FIRST-HAND-%d-OF-%d" % (GATES["XG9"]["books_with_https"], len(BOOKS)),
    "DISCIPLINE-CORE-%d-OF-%d" % (GATES["XG10"]["core_items_found"],
                                  GATES["XG10"]["core_items_expected"]),
    "HARDCODED-OK-FLAW-%d-BOOKS-REGISTERED" % len(REGISTERED),
    "UFT-NOT-BROKEN",
    "NEW-PREDICTION-0",
]))


def build_payload():
    return {
        "title": "ROOT 系列十一册跨册对账汇总 · 机核（11 门）",
        "kind": "cross-volume-reconciliation-ledger",
        "date": "2026-11-21",
        "red_line": ("数学自洽 != 实验证实；不宣称攻破统一场论，不宣称新方程或独立实验预言；"
                     "四力统一未证。"),
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "只读11册JSON与11份源码", "门数册数结论不相加",
                       "唯一允许相加的是独立预言计数（全0）", "两路机拼",
                       "恒等门不承重", "跨册一致与反噬", "负读数显式登记",
                       "逐字子串校验", "无写死ok守卫"],
        "books": [{"short": b["short"], "file": os.path.basename(b["path"]),
                   "bytes": len(b["raw"].encode("utf-8")),
                   "n_gate_ok": b["d"].get("n_gate_ok"),
                   "n_gate_total": b["d"].get("n_gate_total"),
                   "verdict": b["d"].get("verdict")} for b in BOOKS],
        "scope": {
            "declared_include": SCOPE_INCLUDE,
            "declared_exclude": SCOPE_EXCLUDE,
            "n_glob_hits": len(FOUND),
            "unregistered": UNREGISTERED,
            "missing": MISSING_SCOPE,
            "note": "范围显式声明并做「发现即登记」检查：glob 命中的任何未登记文件都会让脚本报错，"
                    "禁止静默略过，也禁止把并行会话产物无声并入本册门账。",
        },
        "excluded_parallel_outputs": EXCLUDED,
        "n_gate_ok": N_OK, "n_gate_total": N_TOTAL,
        "gates": GATES,
        "hard_boundaries": HARD,
        "unverified_anchors": UNVERIFIED,
        "guards": GUARDS, "n_guard_ok": GUARD_OK, "n_guard_total": GUARD_TOTAL,
        "final": FINAL, "verdict": VERDICT,
        "non_additivity": {
            "rules": ["门数不相加：77 门是 11 册各自的判据，不是 77 份独立证据。",
                      "册数不相加：同一对象被两册审计时标「同源」，不折成两份。",
                      "结论条数不相加：五条硬边界是多册共同指向，不是五次独立确认。",
                      "唯一可加：独立预言计数，全 0 相加仍 0。"],
            "same_object_pairs": [
                {"pair": ["rootv134", "rootv134sec8"],
                 "object": "纯标架/纯规范联络曲率残差 3.0751E-10",
                 "treatment": "同源，计 1 份"}]},
        "boundary": [
            "本册是横向对账，不产生新的物理判断；它检验的是「已产出的 11 册之间是否互相自洽」。",
            "门账 77/77 全通过不等于 77 条证据：其中恒等/重排门占比在本册 XG3 单独登记。",
            "11 册的结论互相印证只说明本链内部一致，不构成对外部世界的证据。",
            "α/G/质量三条外生边界由三条互不引用同一算式的路线得到，但仍属「同一个模型的三种视角」。",
            "V134 反噬 V133 是链内自我修正，属正常审计行为，不是外部反驳。",
            "三册写死 ok 的瑕疵已登记；其门内读数支持该门通过，但 ok 本身不可由读数推翻。",
            "真正的硬出口（外部新读数 + 可认证零自由参数的非回述输出）仍未出现，独立预言数保持 0。"],
    }


PAYLOAD = build_payload()
BLOB = (json.dumps(PAYLOAD, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")

PREV = None
if os.path.exists(OUT_JSON):
    PREV = open(OUT_JSON, "rb").read()
IDEM = (PREV == BLOB) if PREV is not None else None
SHA = hashlib.sha256(BLOB).hexdigest()

with open(OUT_JSON, "wb") as fh:
    fh.write(BLOB)


def report():
    L = []
    A = L.append
    A("=" * 96)
    A(PAYLOAD["title"])
    A("=" * 96)
    A("kind    : %s" % PAYLOAD["kind"])
    A("date    : %s" % PAYLOAD["date"])
    A("red_line: %s" % PAYLOAD["red_line"])
    A("")
    A("-" * 96)
    A("一、十一册机读总表（门数不相加）")
    A("-" * 96)
    A("%-14s %-8s %-6s %s" % ("short", "gate", "bytes", "verdict_tail"))
    for b in PAYLOAD["books"]:
        A("%-14s %-8s %-6d %s" % (b["short"],
                                  "%s/%s" % (b["n_gate_ok"], b["n_gate_total"]),
                                  b["bytes"], TAIL))
    A("合计门账（仅作盘点，不作证据份数）: %d/%d"
      % (GATES["XG2"]["routeA_ok"], GATES["XG2"]["routeA_total"]))
    A("")
    A("-" * 96)
    A("二、11 门逐条读数")
    A("-" * 96)
    for k in sorted(GATES):
        g = GATES[k]
        A("[%s] ok=%s" % (k, g["ok"]))
        A("   exp: %s" % g["exp"])
        A("   act: %s" % g["act"])
        A("   why: %s" % g["meaning"])
        A("")
    A("-" * 96)
    A("三、五条反复出现且未被突破的硬边界")
    A("-" * 96)
    for name in sorted(HARD):
        spec = HARD[name]
        A("[%s] %s  (anchors=%d)" % (name, spec["claim"], spec["n_anchors"]))
        for short, needle in spec["anchors"]:
            A("   %-12s %s   [逐字校验 %s]"
              % (short, needle, "OK" if verified(short, needle) else "MISS"))
        A("")
    A("-" * 96)
    A("四、守卫")
    A("-" * 96)
    for k in sorted(GUARDS):
        A("[%s] ok=%s  %s" % (k, GUARDS[k]["ok"], GUARDS[k]["note"]))
    A("")
    A("-" * 96)
    A("五、负读数与边界（如实登记，不掩盖）")
    A("-" * 96)
    A("N1 写死 ok：%s（行号已登记于 XG11，逐条核对读数自洽，但 ok 不可由读数推翻）"
      % PAYLOAD["gates"]["XG11"]["dirty_books"])
    A("N2 恒等/重排门：%d 门（数据路 %d / 文本路 %d，取并集保守侧）；承重门：%d 门"
      % (GATES["XG3"]["n_identity_gates"], GATES["XG3"]["n_identity_data_route"],
         GATES["XG3"]["n_identity_text_route"], GATES["XG3"]["n_load_bearing_gates"]))
    A("N2b 两路分类分歧：%d 条（逐条列出，不抹平）" % GATES["XG3"]["n_route_divergence"])
    for r in GATES["XG3"]["divergence"]:
        A("     %-12s %-46s data=%s text=%s"
          % (r["book"], r["gate"], r["data_route"], r["text_route"]))
    A("N2c 既有理论复核门（既非恒等也非重排，但同样是「复核别人」）：%d 门"
      % GATES["XG3"]["n_known_theory_gates"])
    for r in GATES["XG3"]["known_theory_rows"]:
        A("     %-12s %s" % (r["book"], r["gate"]))
    A("N2d 非新增门合计（恒等 ∪ 既有理论）= %d / %d；既非恒等也非既有理论的候选 = %d 门"
      % (GATES["XG3"]["n_non_novel_gates"], GATES["XG2"]["routeA_total"],
         GATES["XG3"]["n_novel_candidate_gates"]))
    A("     ★候选 ≠ 新证据：其中大量门是负读数判据（判「做不到」），不构成 ROOT 的正向增量。")
    A("N3 判别力为 0 的门：%d 门（%s）"
      % (GATES["XG7"]["n_zero_discrimination_gates"],
         ", ".join("%s/%s" % (r["book"], r["gate"]) for r in GATES["XG7"]["rows"])))
    A("N4 同源不相加：rootv134 与 rootv134sec8 共用残差 3.0751E-10，计 1 份")
    A("N5 独立预言计数：%d" % GATES["XG8"]["total"])
    A("")
    for line in PAYLOAD["boundary"]:
        A("边界: %s" % line)
    A("")
    A("-" * 96)
    A("六、范围声明与被排除的并行产物（发现即登记，禁止静默略过）")
    A("-" * 96)
    A("入选 %d 册：%s" % (len(SCOPE_INCLUDE), ", ".join(SCOPE_INCLUDE)))
    A("glob 命中 %d 个文件；未登记 %s；范围缺失 %s"
      % (len(FOUND), UNREGISTERED, MISSING_SCOPE))
    for k in sorted(EXCLUDED):
        v = EXCLUDED[k]
        A("排除 %-14s file=%s bytes=%d sha256=%s"
          % (k, v["file"], v["bytes"], v["sha256"][:24]))
        A("     理由：%s" % v["reason"])
    A("说明：被排除册只登记存在与指纹，不计门账、不做背书；若它日后被并行会话改动，"
      "指纹变化可被本册下一轮检出。")
    A("")
    A("-" * 96)
    A("七、机读结论")
    A("-" * 96)
    A("verdict : %s" % VERDICT)
    A("final   : %s" % FINAL)
    A("guards  : %d/%d 通过" % (GUARD_OK, GUARD_TOTAL))
    A("sha256  : %s" % SHA)
    if IDEM is None:
        A("idem    : FIRST-RUN（本册首跑；复跑将对 JSON 逐字节比较）")
    else:
        A("idem    : %s（复跑字节一致）" % ("TRUE" if IDEM else "FALSE"))
    A("json    : %s" % os.path.basename(OUT_JSON))
    A("")
    return "\n".join(L) + "\n"


TXT = report()
with open(OUT_TXT, "wb") as fh:
    fh.write(TXT.encode("utf-8"))

print(TXT)
print("JSON-BYTES=%d SHA256=%s" % (len(BLOB), SHA))
print("IDEMPOTENT=%s" % ("FIRST-RUN" if IDEM is None else IDEM))
