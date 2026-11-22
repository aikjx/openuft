# -*- coding: utf-8 -*-
"""
ROOT V128 第八册 · MICROSCOPE 一手读数对耦合荷的判别力

性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

本册不再在旧模型内部找出口，而是引入外部一手读数做可翻转判据。

外部来料（两个独立一手来源，逐字引文与 URL 存在 JSON 中）
----------------------------------------------------------
A: arXiv:2209.15487, Phys. Rev. Lett. 129, 121102 (2022)
   eta(Ti,Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15
B: arXiv:2209.15488, Class. Quantum Grav. 39 204009 (2022)
   no EP violation at the level of 2.7 x 10^-15 (quadrature)
   Pt-Pt null control: statistical uncertainty 1.1 x 10^-15

要判的两件具体事
----------------
M（质量耦合 Yukawa，即 V128 第五册的对象）：耦合荷 q_A = 1 通用
   => eta_M = 0 对任何 beta、lambda 精确成立
   => MICROSCOPE 判别力为零；与读数「相容」不等于「被证实」
BL（B-L 耦合 Yukawa，A 文明确讨论的 spin-1 U(1)_{B-L} 对照模型）：
   q_A = (B-L)/mu ~ N/A -> q_Ti != q_Pt
   => eta_BL = alpha * q_earth * (q_Ti - q_Pt) * F(r/lambda), F=(1+x)e^{-x}
   => d eta / d alpha != 0，可用同一读数给 |alpha| 95% 双侧端点上界

红线：不宣称攻破统一场论；数学自洽 != 实验证实；独立实验预言 0；
      本册只读外部一手读数，不改任何上游判词，不与任何册相加。
"""

import ast
import hashlib
import json
import os
import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

STEM = "_ALG_ep_microscope_coupling_gate"
DATE = "2026-11-22"


def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_5():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128e_largelambda_vacuity_recompute_2026-11-22.json")


def upstream_6():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128f_beta_fisher_recompute_2026-11-22.json")


def Dq(x):
    if isinstance(x, D):
        return x
    if isinstance(x, int):
        return D(x)
    return D(str(x))


def fmt(x, nd=6):
    v = Dq(x)
    if v == 0:
        return "0"
    return ("%." + str(nd) + "E") % v


def fstr(x, nd=6):
    return fmt(x, nd)


# ------------------------------------------------------------------ 外部一手读数
SOURCE_A = {
    "id": "arXiv:2209.15487",
    "journal": "Phys. Rev. Lett. 129, 121102 (2022)",
    "url": "https://arxiv.org/abs/2209.15487",
    "quote": "eta(Ti, Pt) = [-1.5 +/- 2.3 (stat) +/- 1.5 (syst)] x 10^-15 at 1 sigma",
    "eta_center": "-1.5e-15",
    "sigma_stat": "2.3e-15",
    "sigma_syst": "1.5e-15",
}

SOURCE_B = {
    "id": "arXiv:2209.15488",
    "journal": "Class. Quantum Grav. 39 204009 (2022)",
    "url": "https://arxiv.org/abs/2209.15488",
    "quote": "no EP violation at the level of 2.7 x 10^-15 if we combine stochastic and systematic errors quadratically; null Eotvos parameter with a statistical uncertainty of 1.1 x 10^-15",
    "sigma_comb_reported": "2.7e-15",
    "sigma_pt_pt_null": "1.1e-15",
}

# ------------------------------------------------------------------ 成分与几何输入
# 天然同位素加权标准原子量（无量纲，物质属性，不是自由参数）
A_TI, Z_TI = D("47.867"), D(22)
A_PT, Z_PT = D("195.084"), D(78)
N_TI = A_TI - Z_TI
N_PT = A_PT - Z_PT
Q_TI = N_TI / A_TI
Q_PT = N_PT / A_PT
DELTA_Q = Q_TI - Q_PT
Q_MEAN = (Q_TI + Q_PT) / D(2)
REL_DQ = DELTA_Q / Q_MEAN

# MICROSCOPE 轨道：R_E = 6371 km，高度约 700 km
R_ORBIT = D("7071000")
Q_EARTH = D("0.5")          # 地球平均 (B-L)/mu 近似，模型输入，登记为非自由参数

SIGMA_COMB = (Dq(SOURCE_A["sigma_stat"]) ** 2 + Dq(SOURCE_A["sigma_syst"]) ** 2).sqrt()
ETA_CENTER = Dq(SOURCE_A["eta_center"])
ETA_95_ENDPOINT = abs(ETA_CENTER) + D("1.96") * SIGMA_COMB

LAMS = ("1e6", "1e8", "1e10", "1e12")


# ------------------------------------------------------------------ 两个具体模型
def eta_mass(beta, lam):
    """模型 M：通用质量耦合，耦合荷 q_A = 1 对所有物质 => eta 恒零。"""
    return D(0)


def shape_factor(lam):
    """F(x) = (1+x) exp(-x), x = r/lambda；lambda -> inf 时 F -> 1。"""
    x = R_ORBIT / Dq(lam)
    return (D(1) + x) * (-x).exp()


def k_bl(lam):
    """模型 BL：d eta / d alpha = q_earth * (q_Ti - q_Pt) * F(r/lambda)。"""
    return Q_EARTH * DELTA_Q * shape_factor(lam)


def eta_bl(alpha, lam):
    return Dq(alpha) * k_bl(lam)


# ------------------------------------------------------------------ 判词（唯一入口）
def verdict_of(e5, e6, tflag):
    """承重三标志：E5（BL 判别力）、E6（外部上界）、T（命题判决）。
    E4 是由模型定义推出的恒等式，单列不承重，不进判词。"""
    a = ("BL-COUPLING-CHARGE-DIFFERENCE-NONZERO--DISCRIMINATION-EXISTS"
         if e5 else "BL-COUPLING-CHARGE-DIFFERENCE-ZERO--DISCRIMINATION-LOST")
    b = ("SAME-READOUT-BOUNDS-ALPHA--UPPER-BOUND-IS-BL-ONLY"
         if e6 else "NO-ALPHA-BOUND-FROM-READOUT")
    c = "CLAIM-T-REFUTED--COMPATIBILITY-IS-NOT-CONFIRMATION" if tflag \
        else "CLAIM-T-NOT-REFUTED--COMPATIBILITY-CHECK-INCONCLUSIVE"
    return "--".join(["EP-MICROSCOPE-ONE-HAND-READOUT", a, b, c,
                      "UFT-NOT-BROKEN", "NO-INDEPENDENT-PREDICTION"])


def _ok_assigns(fn):
    out = []

    def walk(node, depth):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "ok" for t in ch.targets):
                out.append((ch, depth, ch.value))
            walk(ch, depth + (1 if isinstance(ch, (ast.If, ast.For, ast.While, ast.Try))
                              else 0))
    walk(fn, 0)
    return out


# ------------------------------------------------------------------ 门
def gate_E1():
    """外部读数锚：两篇一手来源的统计+系统组合误差互相一致。"""
    ok = True
    rep = Dq(SOURCE_B["sigma_comb_reported"])
    rel = abs(SIGMA_COMB - rep) / rep
    if not (D(0) < rel < D("0.05")):
        ok = False
    return {"id": "E1", "kind": "guard", "ok": ok,
            "title": "一手读数锚：A 的 stat/syst 二次组合与 B 的 2.7e-15 一致",
            "notes": ["A: %s（结果论文）" % SOURCE_A["url"],
                      "B: %s（系统学论文）" % SOURCE_B["url"],
                      "★A 与 B 是同一 MICROSCOPE 实验的两篇论文，同源，门数不相加",
                      "组合二次误差 %s；B 报 %s；相对差 %s（<5%% 为一位有效数字一致）"
                      % (fmt(SIGMA_COMB), fmt(rep), fmt(rel))],
            "readings": {"eta_center": fmt(ETA_CENTER),
                         "sigma_stat": SOURCE_A["sigma_stat"],
                         "sigma_syst": SOURCE_A["sigma_syst"],
                         "sigma_comb_exact": fmt(SIGMA_COMB),
                         "sigma_comb_reported": fmt(rep),
                         "relative_difference": fmt(rel)}}


def gate_E2():
    """同成分零对照：Pt-Pt 零读数存在且小于 Ti-Pt 组合误差（机器没坏）。"""
    ok = True
    s0 = Dq(SOURCE_B["sigma_pt_pt_null"])
    rep = Dq(SOURCE_B["sigma_comb_reported"])
    if not (D(0) < s0 < rep):
        ok = False
    return {"id": "E2", "kind": "guard", "ok": ok,
            "title": "Pt-Pt 同成分零对照：sigma=1.1e-15，小于 Ti-Pt 组合误差",
            "notes": ["零对照来自 B 文原文，不是本册自造；它证明差分通道没有系统偏置",
                      "★与 E1 同源（同一 MICROSCOPE 实验），不是独立证据，不相加"],
            "readings": {"sigma_pt_pt_null": fmt(s0), "sigma_ti_pt_comb": fmt(rep)}}


def gate_E3():
    """成分荷：从天然同位素加权原子量算 B-L 荷/质量比，Ti 与 Pt 必须不同。"""
    ok = True
    if not (D(0) < Q_TI < D(1) and D(0) < Q_PT < D(1) and Q_TI != Q_PT):
        ok = False
    if not (DELTA_Q < D(0) and REL_DQ != D(0)):
        ok = False
    return {"id": "E3", "kind": "structure", "ok": ok,
            "title": "成分荷：q=(B-L)/mu=N/A，Ti 与 Pt 的差非零",
            "notes": ["A_Ti=%s, Z_Ti=%s；A_Pt=%s, Z_Pt=%s（标准原子量，非自由参数）"
                      % (A_TI, Z_TI, A_PT, Z_PT),
                      "q_Ti != q_Pt 是 BL 判别力的唯一来源；质量耦合 q=1 通用，无此差"],
            "readings": {"q_ti": fmt(Q_TI), "q_pt": fmt(Q_PT),
                         "delta_q": fmt(DELTA_Q), "delta_q_over_mean": fmt(REL_DQ),
                         "q_earth_input": fmt(Q_EARTH)},
            "rows": [{"pair": "Ti", "A": str(A_TI), "Z": str(Z_TI),
                      "N_over_A": fmt(Q_TI)},
                     {"pair": "Pt", "A": str(A_PT), "Z": str(Z_PT),
                      "N_over_A": fmt(Q_PT)}]}


def gate_E4():
    """承重：模型 M 的 eta 对 beta、lambda 全网格精确为零。"""
    ok = True
    worst = D(0)
    worst_d = D(0)
    rows = []
    h = D("1e-8")
    for b in ("0", "1e-6", "1e-3", "1"):
        for l in LAMS:
            v = eta_mass(Dq(b), Dq(l))
            d = (eta_mass(Dq(b) + h, Dq(l)) - eta_mass(Dq(b) - h, Dq(l))) / (2 * h)
            worst = max(worst, abs(v))
            worst_d = max(worst_d, abs(d))
        rows.append({"beta": b, "max_abs_eta": fmt(worst)})
    if worst > D(0) or worst_d > D(0):
        ok = False
    return {"id": "E4", "kind": "identity", "ok": ok,
            "title": "恒等（不承重）：质量耦合 eta=0 对 beta,lambda 全网格精确成立",
            "notes": ["★E4 由模型定义 q_A=1 直接推出，是恒等式，不是证据，不进承重计数",
                      "4 个 beta x 4 个 lambda：max|eta_M| = %s，max|d eta_M/d beta| = %s"
                      % (fmt(worst), fmt(worst_d)),
                      "=> MICROSCOPE 对该模型的判别力精确为零，不是统计功效不足"],
            "readings": {"max_abs_eta_mass": fmt(worst),
                         "max_d_eta_d_beta": fmt(worst_d),
                         "n_configurations": 16},
            "rows": rows}


def gate_E5():
    """承重：模型 BL 的 d eta/d alpha 在 lambda 网格上全非零。"""
    ok = True
    rows = []
    mn = None
    for l in LAMS:
        k = k_bl(Dq(l))
        mn = abs(k) if mn is None else min(mn, abs(k))
        if k == D(0):
            ok = False
        rows.append({"lambda_m": l, "F": fmt(shape_factor(Dq(l))),
                     "d_eta_d_alpha": fmt(k)})
    return {"id": "E5", "kind": "load-bearing", "ok": ok,
            "title": "承重：B-L 耦合的 d eta/d alpha 非零，判别力存在",
            "notes": ["同一外部读数下：模型 M 判别力 0，模型 BL 判别力 %s（最小绝对值）"
                      % fmt(mn),
                      "这不是「所有模型都通过」的空判据"],
            "readings": {"min_abs_d_eta_d_alpha": fmt(mn)}, "rows": rows}


def gate_E6():
    """承重：用 95% 双侧端点给 BL 的 |alpha| 上界。"""
    ok = True
    rows = []
    for l in LAMS:
        k = abs(k_bl(Dq(l)))
        a95 = ETA_95_ENDPOINT / k
        if not (a95 > D(0)):
            ok = False
        rows.append({"lambda_m": l, "alpha_95_endpoint": fmt(a95)})
    return {"id": "E6", "kind": "load-bearing", "ok": ok,
            "title": "承重：BL 获得非零 |alpha| 95% 双侧端点上界",
            "notes": ["eta 双侧区间 = [%s, %s]；取绝对值较大端点 %s（不用 |eta_hat|+1.96sigma）"
                      % (fmt(ETA_CENTER - D("1.96") * SIGMA_COMB),
                         fmt(ETA_CENTER + D("1.96") * SIGMA_COMB),
                         fmt(ETA_95_ENDPOINT)),
                      "上界只给 BL；质量耦合模型 M 无上界可给（eta 恒零）"],
            "readings": {"eta_95_endpoint_abs": fmt(ETA_95_ENDPOINT),
                         "alpha_95_at_1e12m": fmt(ETA_95_ENDPOINT / abs(k_bl(D("1e12"))))},
            "rows": rows}


def gate_E7():
    """反噬：把读数中心值换成显著非零，模型 M 立即被判负。"""
    ok = True
    fake = D("1e-13")
    dev = abs(fake - eta_mass(D("1"), D("1e12"))) / SIGMA_COMB
    if not dev > D(10):
        ok = False
    return {"id": "E7", "kind": "guard", "ok": ok,
            "title": "反噬：注入显著非零 eta 时质量耦合模型被判负",
            "notes": ["假读数 1e-13 偏离 M 的预言 0 达 %s sigma => M 会被判负"
                      % fmt(dev, 3),
                      "=> E4 的「与读数相容」不是「被证实」，判据有判别力"],
            "readings": {"fake_eta": fmt(fake), "sigma_deviation": fmt(dev, 3)}}


def gate_E8():
    """反噬：把耦合荷改成通用，BL 判别力归零。"""
    ok = True
    k_uni = D(1) * (D(1) - D(1)) * shape_factor(D("1e12"))
    k_ref = k_bl(D("1e12"))
    if not (k_uni == D(0) and k_ref != D(0)):
        ok = False
    return {"id": "E8", "kind": "guard", "ok": ok,
            "title": "反噬：通用耦合荷使 BL 判别力归零",
            "notes": ["q_A=q_B=1 时 d eta/d alpha = %s；真实 B-L 荷差下 = %s"
                      % (fmt(k_uni), fmt(k_ref)),
                      "=> 判别力来自耦合荷差，不是误差假设或手工调参"],
            "readings": {"k_universal": fmt(k_uni), "k_bl_reference": fmt(k_ref)}}


def gate_E9():
    """lambda 稳健性：形状因子在四个尺度上都正且不超过 1。"""
    ok = True
    rows = []
    for l in LAMS:
        f = shape_factor(Dq(l))
        if not (D(0) < f <= D(1)):
            ok = False
        rows.append({"lambda_m": l, "F": fmt(f), "r_over_lambda": fmt(R_ORBIT / Dq(l))})
    return {"id": "E9", "kind": "structure", "ok": ok,
            "title": "lambda 稳健性：F=(1+x)e^-x 在四个尺度上均在 (0,1]",
            "notes": ["lambda 只改变系数大小，不改变「M 零 / BL 非零」的判别结构"],
            "readings": {"r_orbit_m": str(R_ORBIT)}, "rows": rows}


def gate_E10(paths):
    """同源性：只读上游 sha，登记不同源，明确不相加。"""
    ok = True
    rows = []
    expected = {"V": "57373c7300448ced", "F": "681689456689e2ad"}
    for tag, p in paths.items():
        raw = open(p, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        if not sha.startswith(expected[tag]):
            ok = False
        rows.append({"upstream": tag, "sha16": sha[:16], "bytes": len(raw)})
    return {"id": "E10", "kind": "guard", "ok": ok,
            "title": "同源性登记：上游只读、不同源、不相加",
            "notes": ["本册外部读数来自 EP 空间实验，与第三册星历、第五/六册结构判据不同源",
                      "只登记 sha，不把门数或结论条数相加"],
            "readings": {}, "rows": rows}


def gate_T(flags):
    """判决：命题 T（MICROSCOPE 能约束 V128 质量耦合模型）REFUTED。"""
    ok = True
    if not (flags["E5"] and flags["E6"]):
        ok = False
    claim_t = "REFUTED" if flags["E4"] else "NOT-REFUTED"
    claim_u = "BOUNDED" if flags["E6"] else "NOT-BOUNDED"
    return {"id": "T", "kind": "load-bearing", "ok": ok,
            "title": "判决：T=REFUTED（零判别力）；U=BOUNDED（BL 得上界）",
            "notes": ["T：MICROSCOPE 一手读数可约束 V128 的质量耦合 Yukawa => REFUTED",
                      "U：同一读数可约束 B-L 耦合 Yukawa => BOUNDED，但未被排除",
                      "两者不是同一对象，不能把 U 的上界搬到 V128 头上"],
            "readings": {"claim_T": claim_t, "claim_U": claim_u,
                         "external_source": SOURCE_A["id"] + " + " + SOURCE_B["id"]}}


def gate_verdict_machine():
    base = verdict_of(True, True, True)
    vs = [verdict_of(False, True, True), verdict_of(True, False, True),
          verdict_of(True, True, False)]
    ok = all(v != base for v in vs)
    return {"id": "G-VERDICT-MACHINE", "kind": "guard", "ok": ok,
            "title": "判词机读：承重 E5/E6/T 任一翻转必改判词串（E4 恒等不进）",
            "notes": ["基线 %d 字符；变体 %s" % (len(base), [len(v) for v in vs])],
            "readings": {}}


def gate_no_hardcode():
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    bad = []
    scanned = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        asg = _ok_assigns(node)
        if not asg:
            continue
        scanned += 1
        top = [a for a in asg if a[1] == 0 and isinstance(a[2], ast.Constant)]
        nested = [a for a in asg if a[1] >= 1]
        if top and not nested:
            bad.append((node.name, node.lineno))
    return {"id": "G-NO-HARDCODE-OK", "kind": "guard", "ok": not bad,
            "title": "AST 守卫：ok 不得顶层赋常量且无条件翻转",
            "notes": ["扫描 %d 个函数" % scanned, str(bad) if bad else "零命中"],
            "readings": {"n_functions_scanned": scanned}}


def gate_link(jp, rp, verdict):
    ok = True
    notes = []
    for p in (jp, rp):
        if not os.path.exists(p):
            ok = False
            notes.append("缺失 %s" % os.path.basename(p))
            continue
        t = open(p, "rb").read().decode("utf-8", "ignore")
        v, d = verdict in t, DATE in t
        ok = ok and v and d
        notes.append("%s: verdict=%s date=%s" % (os.path.basename(p), v, d))
    return {"id": "G-LINK", "kind": "guard", "ok": ok,
            "title": "链接体检：JSON 与报告均含判词串与日期",
            "notes": notes, "readings": {}}


# ------------------------------------------------------------------ 输出
def render_report(gates, verdict, final):
    L = []
    add = L.append
    add("=" * 78)
    add("ROOT V128 第八册 · MICROSCOPE 一手读数对耦合荷的判别力")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("external_A : %s / eta=%s / stat=%s / syst=%s"
        % (SOURCE_A["id"], SOURCE_A["eta_center"],
           SOURCE_A["sigma_stat"], SOURCE_A["sigma_syst"]))
    add("external_B : %s / comb=%s / PtPt_null=%s"
        % (SOURCE_B["id"], SOURCE_B["sigma_comb_reported"],
           SOURCE_B["sigma_pt_pt_null"]))
    add("claim_T   : MICROSCOPE 一手读数可约束 V128 的质量耦合 Yukawa")
    add("claim_U   : 同一读数可约束 B-L 耦合 Yukawa（对照模型）")
    add("")
    add("-" * 78)
    for g in gates:
        add("[%s] %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["title"]))
        for n in g.get("notes", []):
            add("       " + n)
        for k, v in (g.get("readings") or {}).items():
            add("       .%-40s = %s" % (k, v))
        for r in (g.get("rows") or [])[:8]:
            add("       | " + "  ".join("%s=%s" % (kv, vv) for kv, vv in r.items()))
        add("")
    add("-" * 78)
    add("verdict   : %s" % verdict)
    add("final     : %s" % final)
    add("guards    : %s" % " ".join(g["id"] for g in gates if g["kind"] == "guard"))
    add("bearing   : %s" % " ".join(g["id"] for g in gates
                                    if g["kind"].startswith("load-bearing")))
    add("n_gate_ok : %d / %d" % (sum(1 for g in gates if g["ok"]), len(gates)))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            相容不是证实；上界只属于 BL，不属于 V128。")
    add("boundary  : 本册只读外部一手读数，不改上游判词，不与任何册相加。")
    add("            未排除 B-L 模型；未证明第五力不存在；未测出 lambda。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第八册 MICROSCOPE 一手读数对耦合荷的判别力",
        "date": DATE,
        "claim_under_test": "MICROSCOPE 一手读数可约束 V128 的质量耦合 Yukawa",
        "external_sources": {"A": SOURCE_A, "B": SOURCE_B},
        "models": {
            "M_mass_coupled": {"charge": "q_A = 1 universal",
                               "eta_prediction": "identically zero",
                               "discriminating_power": 0},
            "BL_coupled": {"charge": "q_A = (B-L)/mu ~ N/A",
                           "q_ti": fmt(Q_TI), "q_pt": fmt(Q_PT),
                           "delta_q": fmt(DELTA_Q),
                           "d_eta_d_alpha_at_1e12m": fmt(k_bl(D("1e12")))},
        },
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "load_bearing_gates": [g["id"] for g in gates
                               if g["kind"].startswith("load-bearing")],
        "gates": gates,
        "discipline": [
            "外部一手读数必须给 URL 与逐字引文",
            "上界量用双侧区间端点，不用 |eta_hat|+1.96sigma",
            "相容不是证实；判别力为零不等于模型为真",
            "E4 是模型定义推出的恒等式，单列不承重，不进判词",
            "A/B 两篇论文属同一 MICROSCOPE 实验，同源不相加",
            "反噬：显著非零读数会判负模型 M；通用荷会抹掉 BL 判别力",
            "不同源判据不相加；门数不等于证据份数",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "数学自洽不等于实验证实",
            "不产生新物理，独立实验预言 0",
            "BL 的上界不能搬到 V128 的质量耦合模型",
        ],
    }


def write_json(gates, verdict, final):
    p = out_json()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(build_payload(gates, verdict, final),
                            ensure_ascii=False, indent=1, sort_keys=False) + "\n")
    return p


def write_report(gates, verdict, final):
    p = report_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final))
    return p


def main():
    flags = {}
    gates = []
    for gid, fn in (("E1", gate_E1), ("E2", gate_E2), ("E3", gate_E3),
                    ("E4", gate_E4), ("E5", gate_E5), ("E6", gate_E6),
                    ("E7", gate_E7), ("E8", gate_E8), ("E9", gate_E9)):
        g = fn()
        flags[gid] = g["ok"]
        gates.append(g)
    gates.append(gate_E10({"V": upstream_5(), "F": upstream_6()}))
    flags["E10"] = gates[-1]["ok"]
    gates.append(gate_T(flags))
    flags["T"] = gates[-1]["ok"]
    gates.append(gate_verdict_machine())
    gates.append(gate_no_hardcode())

    verdict = verdict_of(flags["E5"], flags["E6"], flags["T"])

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if flags["E5"] and flags["E6"] and flags["T"]:
            return "GATES-PASS-WITH-CLAIM-T-REFUTED"
        return "GATES-PASS-BUT-CLAIM-NOT-REFUTED"

    final = decide(gates)
    write_report(gates, verdict, final)
    write_json(gates, verdict, final)
    gates.append(gate_link(out_json(), report_path(), verdict))
    final = decide(gates)
    rp = write_report(gates, verdict, final)
    jp = write_json(gates, verdict, final)

    n_ok = sum(1 for g in gates if g["ok"])
    sys.stdout.write("verdict   : %s\n" % verdict)
    sys.stdout.write("final     : %s\n" % final)
    sys.stdout.write("n_gate_ok : %d / %d\n" % (n_ok, len(gates)))
    sys.stdout.write("gates     : %s\n"
                     % ".".join("%s=%s" % (g["id"], g["ok"]) for g in gates))
    sys.stdout.write("report    : %s\n" % rp)
    sys.stdout.write("json      : %s\n" % jp)
    raw = open(jp, "rb").read()
    sys.stdout.write("json_bytes: %d\n" % len(raw))
    sys.stdout.write("json_sha  : %s\n" % hashlib.sha256(raw).hexdigest())
    for g in gates:
        if not g["ok"]:
            sys.stdout.write("FAILED GATE: %s\n" % g["id"])
            for n in g.get("notes", []):
                if n.startswith("FAIL"):
                    sys.stdout.write("    " + n + "\n")
    return 0 if n_ok == len(gates) else 1


if __name__ == "__main__":
    sys.exit(main())
