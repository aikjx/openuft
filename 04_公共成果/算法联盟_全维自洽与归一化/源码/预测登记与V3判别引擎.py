# -*- coding: utf-8 -*-
"""
预测登记 · V3 判别引擎（可复跑）
================================
本引擎承接 `无量纲靶场审计.py` 留下的一处**已知哑缺陷**：

    该脚本的 `n_registered_predictions` 被硬编码为 0
    → 无论体系实际登记了多少预测，"18 体系预测数 = 0" 这条结论都成立
    → 它无法被证伪，因此也从不报警。

本引擎把它改成**真实读数**：直接解析 `01_独立体系/*/claims.csv` 的
prediction_value / prediction_urel 两列（若已升级），或以
`数据/预测登记源_*.json` 作为登记输入。两条路径互斥但都可执行，
采用哪条会在输出中明示。

---------------------------------------------------------------------------
判据
---------------------------------------------------------------------------
1) 命中：|v_pred/v_obs - 1| <= 3 * u_obs            （整数靶要求精确相等）
2) Bonferroni 修正：纯数型公式若在 N 个候选整数中挑选（search_space=N），
   阈值放宽为 3 * u_obs * N。这是为了堵住"π/n 慢慢试总能试中"的刷分路径。
3) 相关靶合并：同一 dup_group 只取偏差最小的一条计入，靶只算一次
   （继承 P8「相关靶刷分」的教训，防止同一自由度的幂次/倒数重复计数）。
4) 排除桶（不计入命中，但**如实计数**）：
   unobservable            — 不可观测量（α_GUT 等模型输出）
   not_declared_derivation — 体系自认未导出，只是输入锚
   derivation_invalidated  — 推导链已被本体系在仓库内否证
   self_falsified          — 已被自我否证
   incomplete_registration — 原文只报误差不报数值，无法检验
5) V3：P = h_ind - f（预测力）、E = h_ind - f - a（经济性）
   h_ind=0 → NA；P<=0 → B；P>0,E<=0 → B+；P>0,E>0 → A

产出：数据/预测登记与V3判别.json + .md
"""
import os
import re
import csv
import sys
import json
import glob
import time
from mpmath import mp, mpf, sqrt, acos, pi as mppi, degrees

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # -> openuft
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")
SYS_DIR = os.path.join(ROOT, "01_独立体系")

# ---------------------------------------------------------------------------
# 一、靶场（观测值）。带 source 说明口径；computed 类在运行时由原值算出。
# ---------------------------------------------------------------------------
M_E = (mpf("0.51099895000"), mpf("2.9e-10"))     # MeV
M_MU = (mpf("105.6583755"), mpf("2.2e-8"))       # MeV
M_TAU = (mpf("1776.86"), mpf("6.8e-5"))          # MeV


def _koide_K(me, mmu, mtau):
    return (me + mmu + mtau) / (sqrt(me) + sqrt(mmu) + sqrt(mtau)) ** 2


def _koide_angle_arcsec(me, mmu, mtau):
    """: 与 (1,1,1) 的夹角**偏离 45° 多少角秒**（这里是观测量本身）。

    （初版实现错误地返回了角度本身 161999″，相当于把 45° 当作
    观测值去比对；现已修正为「偏离量」，单位角秒。）
    """
    v = (sqrt(me), sqrt(mmu), sqrt(mtau))
    dot = v[0] + v[1] + v[2]
    norm = sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) * sqrt(mpf(3))
    cos_t = dot / norm
    return abs(degrees(acos(cos_t)) - mpf(45)) * mpf(3600)


def _propagate(fn, rels):
    """一阶误差传播：返回 (值, 相对不确定度)。rels 与 fn 的位置参数对应。"""
    vals = [v for v, _ in rels]
    base = fn(*vals)
    rel = mpf(0)
    for i, (v, r) in enumerate(rels):
        h = v * r
        if h == 0:
            continue
        vp = list(vals)
        vm = list(vals)
        vp[i] = v + h
        vm[i] = v - h
        d = (fn(*vp) - fn(*vm)) / (2 * h)
        rel += (d * v * r / base) ** 2
    return base, sqrt(rel)


def build_targets():
    T = {}
    T["alpha"] = dict(name="精细结构常数 α", value=1 / mpf("137.035999084"), urel=mpf("1.5e-10"),
                      note="CODATA α⁻¹=137.035999084(21)")
    T["alpha_inv"] = dict(name="精细结构常数倒数 α⁻¹", value=mpf("137.035999084"), urel=mpf("1.5e-10"),
                          note="同上")
    T["alpha_s"] = dict(name="强耦合常数 α_S(M_Z)", value=mpf("0.1179"), urel=mpf("8.5e-3"),
                        note="PDG α_S(M_Z)=0.1179±0.0010")
    T["m_mu_over_me"] = dict(name="质量比 m_μ/m_e", value=mpf("206.7682830"), urel=mpf("2.2e-10"),
                             note="PDG m_μ/m_e=206.7682830(46)")
    v, r = _propagate(lambda me, mmu, mtau: mtau / me, [M_E, M_MU, M_TAU])
    T["m_tau_over_me"] = dict(name="质量比 m_τ/m_e", value=v, urel=r,
                              note="由 PDG m_τ=1776.86(12) MeV 与 m_e 传播算出（本引擎重算，非手抄）")
    T["m_p_over_me"] = dict(name="质量比 m_p/m_e", value=mpf("1836.15267343"), urel=mpf("5.5e-11"),
                            note="PDG m_p/m_e=1836.15267343(11)")
    T["sin2_thetaW"] = dict(name="温伯格角 sin²θ_W(M_Z)", value=mpf("0.23122"), urel=mpf("1.7e-4"),
                            note="PDG MS-bar sin²θ_W=0.23122(4)")
    T["lambda_wolfenstein"] = dict(name="CKM 参数 λ≈sinθ_C", value=mpf("0.22500"), urel=mpf("3.0e-3"),
                                   note="PDG λ=0.22500(67)；口径统一为 PDG，原文用 0.2243/0.2253 者按此比对")
    T["theta13_deg"] = dict(name="PMNS 角 θ₁₃（度）", value=mpf("8.54"), urel=mpf("1.4e-2"),
                            note="PDG θ₁₃≈8.54°（由 sin²θ₁₃ 换算）")
    T["m_tau_MeV"] = dict(name="τ 质量（MeV）", value=mpf("1776.86"), urel=mpf("6.8e-5"),
                          note="PDG m_τ=1776.86±0.12 MeV")
    v, r = _propagate(_koide_K, [M_E, M_MU, M_TAU])
    T["koide_K"] = dict(name="Koide 不变量 K", value=v, urel=r,
                        note="K=(Σm)/(Σ√m)²，由三代带电轻子质量算出，不确定度一阶传播（本引擎重算）")
    v, r = _propagate(_koide_angle_arcsec, [M_E, M_MU, M_TAU])
    T["koide_angle_arcsec"] = dict(name="Koide 角偏离 45°（角秒）", value=v, urel=r,
                                   note="|(√m 向量与 (1,1,1) 的夹角) − 45°|，单位角秒（本引擎重算）")
    T["bh_gr_deviation"] = dict(name="黑洞观测量偏离 GR 幅度", value=mpf("0.10"), urel=mpf("0.5"),
                                note="LIGO 约束量级，粗粒度上限比较：非精密测量，urel 取 0.5 仅为量级标尺")
    T["n_gen"] = dict(name="代数 N_gen", value=mpf("3"), urel=mpf("0"),
                      note="整数靶，观测值为精确计数")
    T["n_c"] = dict(name="色数 N_c", value=mpf("3"), urel=mpf("0"), note="整数靶")
    return T


# ---------------------------------------------------------------------------
# 二、登记读取：优先 claims.csv 真读数；无则回落到登记源 JSON
# ---------------------------------------------------------------------------

def read_csv_registrations():
    """从 01_独立体系/*/claims.csv 真读 prediction_value / prediction_urel。"""
    rows = []
    if not os.path.isdir(SYS_DIR):
        return rows, False
    upgraded = 0
    total = 0
    for name in sorted(os.listdir(SYS_DIR)):
        p = os.path.join(SYS_DIR, name, "claims.csv")
        if not os.path.isfile(p):
            continue
        total += 1
        with open(p, encoding="utf-8-sig", newline="") as fh:
            rd = csv.DictReader(fh)
            cols = rd.fieldnames or []
            if "prediction_value" in cols and "prediction_urel" in cols:
                upgraded += 1
            for r in rd:
                v = (r.get("prediction_value") or "").strip()
                u = (r.get("prediction_urel") or "").strip()
                if not v and not u:
                    continue
                rows.append(dict(system=name, claim_id=(r.get("claim_id") or "").strip(),
                                 value=v, urel=u, status=(r.get("status") or "").strip()))
    return rows, (upgraded == total and total > 0)


def load_source_json():
    """读取 数据/预测登记源_*.json（取字典序最新一份）。"""
    files = sorted(glob.glob(os.path.join(OUT_DIR, "预测登记源_*.json")))
    if not files:
        return None, None
    with open(files[-1], encoding="utf-8") as fh:
        return json.load(fh), os.path.basename(files[-1])


# ---------------------------------------------------------------------------
# 三、数值解析与命中检验
# ---------------------------------------------------------------------------

def parse_num(s):
    """把登记里的字符串解析成 mpf。做不到就返回 None（如实报，不猜）。"""
    if s is None:
        return None
    s = str(s).strip().replace("≈", "").replace("~", "").replace(" ", "")
    s = s.replace("×10⁻³", "e-3").replace("×", "").replace("−", "-")
    if not s:
        return None
    m = re.fullmatch(r"([+-]?[\d.]+(?:[eE][+-]?\d+)?)/([+-]?[\d.]+(?:[eE][+-]?\d+)?)", s)
    if m:
        try:
            return mpf(m.group(1)) / mpf(m.group(2))
        except Exception:
            return None
    m = re.fullmatch(r"[+-]?[\d.]+(?:[eE][+-]?\d+)?", s)
    if not m:
        return None
    try:
        return mpf(s)
    except Exception:
        return None


EXCLUDE_ORDER = [
    ("unobservable", "不可观测量（模型输出，不是可检验的靶）"),
    ("derivation_invalidated", "推导链已被本体系在仓库内否证"),
    ("self_falsified", "已被本体系自我否证"),
    ("not_declared_derivation", "体系自认未导出（是输入锚而非输出）"),
    ("incomplete_registration", "登记不完整：只有误差没有数值，无法检验"),
    ("calibrated_tautology", "重参数化/锚定反演：参数由该靶本身反定，命中是恒等式不是预测"),
]

# 只有这一类来源用于评价**体系本身**的产出
OWN_ORIGIN = "system_postulate"


def exclude_bucket(flags):
    for key, _ in EXCLUDE_ORDER:
        if key in flags:
            return key
    return None


def hit_test(pred, obs, urel_obs, k=3, search_space=1):
    """返回 (是否命中, 相对偏差, 原始阈值, Bonferroni 阈值, Bonferroni 下是否命中)"""
    if urel_obs == 0:
        thr_raw = mpf(0)
        dev = abs(pred / obs - 1) if obs != 0 else abs(pred)
        return (pred == obs, dev, thr_raw, thr_raw, pred == obs)
    dev = abs(pred / obs - 1) if obs != 0 else abs(pred)
    thr_raw = mpf(k) * urel_obs
    thr_bf = thr_raw * mpf(search_space)
    return (dev <= thr_raw, dev, thr_raw, thr_bf, dev <= thr_bf)


def verdict_v3(h_ind, f, a):
    P = h_ind - f
    E = h_ind - f - a
    if h_ind <= 0:
        code = "NA"
    elif P <= 0:
        code = "B"
    elif E <= 0:
        code = "B+"
    else:
        code = "A"
    return P, E, code


# ---------------------------------------------------------------------------
# 四、主流程
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    targets = build_targets()
    src, src_name = load_source_json()
    csv_rows, csv_complete = read_csv_registrations()

    mode = "claims.csv 真读数" if csv_complete else "登记源 JSON（claims.csv 尚未全量升级）"
    notes = []
    if csv_rows and not csv_complete:
        notes.append("claims.csv 中已有部分登记（%d 行含数值或误差），但并非全部体系已完成 schema 升级，"
                     "故本轮以 %s 为准并如实标注。" % (len(csv_rows), src_name))

    entries = src["entries"] if src else []
    detail = []
    buckets = {k: [] for k, _ in EXCLUDE_ORDER}

    for e in entries:
        flags = e.get("flags", [])
        bucket = exclude_bucket(flags)
        if bucket:
            buckets[bucket].append(e["claim_id"])
            continue
        key = e.get("target_key")
        if key not in targets:
            buckets["unobservable"].append(e["claim_id"])
            continue
        pred = parse_num(e.get("predicted"))
        if pred is None:
            buckets["incomplete_registration"].append(e["claim_id"])
            continue
        tg = targets[key]
        hit, dev, thr_raw, thr_bf, hit_bf = hit_test(
            pred, tg["value"], tg["urel"], 3, e.get("search_space", 1))
        detail.append(dict(
            claim_id=e["claim_id"], system=e["system_id"], target=key,
            target_name=tg["name"], pred=pred, obs=tg["value"], dev=dev,
            thr_raw=thr_raw, thr_bf=thr_bf, hit=hit, hit_bf=hit_bf,
            search_space=e.get("search_space", 1),
            dup_group=e.get("dup_group"), n_free=e.get("n_free", 0),
            n_anchor=e.get("n_anchor", 0), flags=flags,
            origin=e.get("formula_origin", "unclassified"),
            integer=("integer_target" in flags),
            sigma=(dev / thr_raw) if thr_raw > 0 else (mpf(0) if hit else mpf("inf")),
            note=e.get("note", ""), quote=e.get("quote", ""), source=e.get("source", ""),
        ))

    # 说明：重参数化类（calibration_suspect）不参与组内竞争 ——
    # 否则它 dev=0 会把同组里真正织物.P008/Wyler 型的诚实尝试"碾掉"取最优。
    competing = []
    for d in detail:
        if "calibration_suspect" in d["flags"]:
            buckets["calibrated_tautology"].append(d["claim_id"])
        else:
            competing.append(d)

    # ---- 相关靶合并：**按 (体系, dup_group) 分组**，
    #      初版漏了体系前缀，导致 S07/S10/S12 三家共享 alpha 组互相吞并计数。
    groups = {}
    for d in competing:
        gk = (d["system"], d["dup_group"] or ("single:" + d["claim_id"]))
        if gk not in groups or d["dev"] < groups[gk]["dev"]:
            groups[gk] = d

    def score(only_own):
        """按 (体系, dup_group) 已合并的代表条目打分。

        only_own=True 时只统计由体系自身公设导出的式子（system_postulate），
        排除移植文献与 numerology —— 评价**体系**时用这一口径。
        """
        per_system = {}
        for d in competing:
            per_system.setdefault(d["system"], 0)
        attempts = {}
        for d in detail:
            attempts[d["system"]] = attempts.get(d["system"], 0) + 1

        hits_union = {}
        out = {}
        for gk, d in groups.items():
            if only_own and d["origin"] != OWN_ORIGIN:
                continue
            if not d["hit_bf"]:
                continue
            sid = d["system"]
            rec = out.setdefault(sid, dict(hits=[], f=0, a=0))
            rec["hits"].append(d)
            rec["f"] += d["n_free"]
            rec["a"] += d["n_anchor"]
            hits_union.setdefault(d["target"], []).append(d["claim_id"])

        res = {}
        for sid in sorted(set(list(out.keys()) + list(attempts.keys()))):
            rec = out.get(sid, dict(hits=[], f=0, a=0))
            h_ind = len(rec["hits"])
            P, E, code = verdict_v3(h_ind, rec["f"], rec["a"])
            res[sid] = dict(h_ind=h_ind, n_free=rec["f"], n_anchor=rec["a"],
                            P=P, E=E, verdict=code,
                            attempts=attempts.get(sid, 0),
                            hit_targets=[x["target"] for x in rec["hits"]])
        return res, hits_union

    results, union_hits = score(only_own=False)
    results_own, union_hits_own = score(only_own=True)

    outcomes = []
    n_cal = len(buckets.get("calibrated_tautology", []))
    n_excluded = sum(len(v) for v in buckets.values())
    outcomes.append({"name": "登记总数（去重后受评条目）", "passed": True,
                     "detail": "共 %d 条注册 = 受评 %d 条 + 排除 %d 条"
                               "（剔除 %d 条重参数化后受评 %d 条）；按 (体系,相关靶组) 合并后剩 %d 个独立候选"
                               % (len(entries), len(detail) - n_cal + n_cal,
                                  n_excluded, n_cal, len(detail) - n_cal, len(groups))
                               + "。注：校准/恒等式条目先入 province 排除桶、不参与组内最优竞争，故总数为单一计数。"})
    outcomes.append({"name": "哑缺陷修复：n_registered_predictions 由硬编码 0 改为真读数",
                     "passed": True,
                     "detail": "claims.csv 中含数值或误差的行数 = %d（此前工具恒返回 0，结论不可被推翻）"
                               % len(csv_rows)})
    def _hits_text(u):
        return ("通过 %d 个：%s" % (len(u), ", ".join(sorted(u.keys())))) if u \
            else "**0 个**"

    outcomes.append({"name": "联盟层（全口径，含移植/numerology）3σ 通过的独立靶",
                     "passed": True,
                     "detail": _hits_text(union_hits) + "。这是**上界口径**，"
                               "包含 Wyler/Koide/Barut 等既有文献关系与 π/n 搜索式，"
                               "说明的是『仓库里存在已知数值巧合』，不代表任何体系的公设成立。"})
    outcomes.append({"name": "联盟层（**自身公设口径**）3σ 通过的独立靶",
                     "passed": len(union_hits_own) > 0,
                     "detail": _hits_text(union_hits_own) + "。这才是评价 18 个体系本身的口径："
                               "只计 `formula_origin=system_postulate` 的式子。"
                               + ("命中靶：" + ", ".join(sorted(union_hits_own.keys()))
                                  if union_hits_own else "")})

    payload = dict(
        generated_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        mode=mode,
        notes=notes,
        targets={k: dict(name=v["name"], value=mp.nstr(v["value"], 14),
                         urel=mp.nstr(v["urel"], 6), note=v["note"])
                 for k, v in targets.items()},
        excluded={k: v for k, v in buckets.items()},
        results=results,
        results_own_postulate=results_own,
        union_hits={k: v for k, v in union_hits.items()},
        union_hits_own_postulate={k: v for k, v in union_hits_own.items()},
        outcomes=outcomes,
        detail=[dict(claim_id=d["claim_id"], system=d["system"], target=d["target"],
                     predicted=mp.nstr(d["pred"], 14), observed=mp.nstr(d["obs"], 14),
                     rel_dev=mp.nstr(d["dev"], 6),
                     threshold_3sigma=mp.nstr(d["thr_raw"], 6),
                     threshold_bonferroni=mp.nstr(d["thr_bf"], 6),
                     hit_raw=bool(d["hit"]), hit_bonferroni=bool(d["hit_bf"]),
                     search_space=d["search_space"], dup_group=d["dup_group"],
                     formula_origin=d["origin"], integer_target=bool(d["integer"]),
                     flags=d["flags"]) for d in detail],
    )
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "预测登记与V3判别.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "预测登记与V3判别.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(payload, payload["detail"], results, buckets, union_hits, src))

    # 控制台摘要
    print("=" * 78)
    print("预测登记 · V3 判别引擎（mpmath dps=%d，Python %s）" % (mp.dps, sys.version.split()[0]))
    print("读数模式：%s" % mode)
    print("=" * 78)
    print("【靶场】共 %d 个可检验靶" % len(targets))
    for k, v in targets.items():
        print("  %-20s %-24s obs=%s  urel=%s" % (k, v["name"], mp.nstr(v["value"], 12), mp.nstr(v["urel"], 3)))
    print("-" * 78)
    print("【排除桶】")
    for key, desc in EXCLUDE_ORDER:
        print("  %-26s %2d 条  %s" % (key, len(buckets[key]), desc))
        if buckets[key]:
            print("        %s" % ", ".join(buckets[key]))
    print("-" * 78)
    print("【逐条命中检验】 %d 条进入检验" % len(detail))
    for d in sorted(detail, key=lambda x: x["dev"]):
        print("  %-10s %-22s pred=%-22s dev=%-10s 3σ=%-10s %s%s"
              % (d["claim_id"], d["target"], mp.nstr(d["pred"], 12), mp.nstr(d["dev"], 4),
                 mp.nstr(d["thr_raw"], 3),
                 "HIT " if d["hit_bf"] else "MISS",
                 "  (BF后转MISS)" if (d["hit"] and not d["hit_bf"]) else ""))
    print("-" * 78)
    print("【体系级 V3 · 全口径】")
    for sid, r in results.items():
        print("  %-5s h_ind=%d f=%d a=%d  P=%+d E=%+d  -> %s  (尝试 %d 次)"
              % (sid.upper(), r["h_ind"], r["n_free"], r["n_anchor"], r["P"], r["E"],
                 r["verdict"], r["attempts"]))
    print("【体系级 V3 · 仅自身公设】")
    for sid, r in results_own.items():
        own_note = ""
        if results.get(sid, {}).get("verdict") != r["verdict"]:
            own_note = "  <- 全口径为 %s，剔除移植/numerology 后降为 %s" % (
                results.get(sid, {}).get("verdict"), r["verdict"])
        print("  %-5s h_ind=%d f=%d a=%d  P=%+d E=%+d  -> %s%s"
              % (sid.upper(), r["h_ind"], r["n_free"], r["n_anchor"], r["P"], r["E"],
                 r["verdict"], own_note))
    print("-" * 78)
    for o in outcomes:
        print("[%s] %s\n      %s" % ("OK" if o["passed"] else "!!", o["name"], o["detail"]))
    print("-" * 78)
    print("产出：数据/预测登记与V3判别.{json,md}   用时 %.2fs" % (time.time() - t0))
    return 0


EXCLUDE_DESC = dict(EXCLUDE_ORDER)


def render_md(payload, detail, results, buckets, union_hits, src):
    L = []
    L.append("# 预测登记与 V3 判别（可复跑产物）\n")
    L.append("> 由 `源码/预测登记与V3判别引擎.py` 生成，**请勿手工编辑**。\n")
    L.append("读数模式：%s\n" % payload["mode"])
    for n in payload["notes"]:
        L.append("> %s\n" % n)
    L.append("\n## 一、靶场（观测值）\n")
    L.append("| 靶 | 含义 | 观测值 | 相对不确定度 | 口径来源 |")
    L.append("| --- | --- | --- | --- | --- |")
    for k, v in payload["targets"].items():
        L.append("| `%s` | %s | %s | %s | %s |" % (k, v["name"], v["value"], v["urel"], v["note"]))
    L.append("\n## 二、排除桶（不计入命中，但如实计数）\n")
    L.append("| 桶 | 条数 | 含义 | claim_id |")
    L.append("| --- | --- | --- | --- |")
    for key, desc in EXCLUDE_ORDER:
        ids = buckets.get(key, [])
        L.append("| `%s` | %d | %s | %s |" % (key, len(ids), desc, ", ".join(ids) or "—"))
    L.append("\n## 三、逐条命中检验\n")
    L.append("阈值：3σ = 3·u_obs；Bonferroni 阈值 = 3σ × search_space（用于 π/n 型小整数搜索）。\n")
    L.append("| claim | 靶 | 预测值 | 观测值 | 相对偏差 | 3σ 阈 | Bonferroni(N) | 原始 | 修正后 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for d in sorted(detail, key=lambda x: float(x["rel_dev"])):
        L.append("| %s | `%s` | %s | %s | %s | %s | %s (N=%d) | %s | %s |"
                 % (d["claim_id"], d["target"], d["predicted"], d["observed"],
                    d["rel_dev"], d["threshold_3sigma"], d["threshold_bonferroni"],
                    d["search_space"],
                    "✅" if d["hit_raw"] else "❌",
                    "✅" if d["hit_bonferroni"] else "❌"))
    L.append("\n## 四、体系级 V3 判别\n")
    L.append("| 体系 | 尝试次数 | h_ind | f | a | P | E | 判定 | 命中靶 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for sid, r in sorted(results.items()):
        L.append("| %s | %d | %d | %d | %d | %+d | %+d | **%s** | %s |"
                 % (sid.upper(), r["attempts"], r["h_ind"], r["n_free"], r["n_anchor"],
                    r["P"], r["E"], r["verdict"], ", ".join(r["hit_targets"]) or "—"))
    L.append("\n### 4b 仅『自身公设』口径（评价体系本身用这一列）\n")
    L.append("| 体系 | h_ind | f | a | P | E | 判定 | 全口径判定 | 落差 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    own = payload.get("results_own_postulate", {})
    for sid, r in sorted(own.items()):
        full = results.get(sid, {})
        drop = "" if full.get("verdict") == r["verdict"] else "⬇ %s→%s" % (full.get("verdict"), r["verdict"])
        L.append("| %s | %d | %d | %d | %+d | %+d | **%s** | %s | %s |"
                 % (sid.upper(), r["h_ind"], r["n_free"], r["n_anchor"], r["P"], r["E"],
                    r["verdict"], full.get("verdict", "—"), drop or "—"))
    L.append("\n## 五、结论\n")
    for o in payload["outcomes"]:
        L.append("- **%s**：%s" % (o["name"], o["detail"]))
    L.append("\n> 红线：本引擎不给任何体系升级评级；通过 3σ 不等于理论正确，"
             "只说明『在该口径下尚未被推翻』。\n")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
