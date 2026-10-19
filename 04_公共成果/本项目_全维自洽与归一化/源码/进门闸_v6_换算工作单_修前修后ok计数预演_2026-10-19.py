# -*- coding: utf-8 -*-
"""进门闸 v6：登记列的**换算工作单**＋修前/修后 `ok` 计数预演（写入侧，2026-10-19）。

来龙去脉
  v4 判的是判决侧（同一行喂两种货币，命中会不会翻面），v5 判的是写入侧分型
  （107 条非空登记行按欠账类型闭合分桶，并测了「照门禁建议删列」的后果）。
  本轮把 v5 的**货币型**真的换算成声明的相对货币，在**内存视图**里（不落他人台账）
  让写入侧门禁自己的 `classify` 复算修前/修后 `ok` 计数——回答「这一列修到底能出多少可判决的登记」。

单一真源
  判定/分型借 `靶场登记列校验_写入侧门禁.py`（G）与 `进门闸_v5_…py`（V5，census/debt_of），
  命中判决借 `无量纲靶场审计.py`（CAR.hit_test），带宽换算与 v4 面逐枚交叉核对。
  本册**不写任何他人 claims.csv**：修后计数是「建议新串喂回门禁」的预演，不是落盘。

产出
  数据/进门闸_v6_换算工作单_修前修后ok计数预演_2026-10-19.json  （面）
  数据/进门闸_v6_逐行换算工作单_2026-10-19.csv                    （107 行工作单）
"""
import collections
import csv
import hashlib
import io
import json
import os
import sys
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
PROJP = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
GATE_SRC = os.path.join(SRC, "靶场登记列校验_写入侧门禁.py")
V5_SRC = os.path.join(SRC, "进门闸_v5_登记列欠账分型与破坏性建议针_2026-10-18.py")
V4_FACE = os.path.join(DATA, "进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.json")
CARRIER = os.path.join(SRC, "无量纲靶场审计.py")

FACE_NAME = "进门闸_v6_换算工作单_修前修后ok计数预演_2026-10-19.json"
ORDER_NAME = "进门闸_v6_逐行换算工作单_2026-10-19.csv"
LAND = "--land" in sys.argv[1:]
QUIET = "--quiet" in sys.argv[1:]
OUT_DIR = DATA if LAND else os.path.join(ROOT, "scratch")

FMT = "%.12g"        # 建议新串的印刷格式（C4 给这档精度定价）
TOL_FMT = 1e-11      # 与 v4 面 urel_B 的最大允许相对偏差
COARSE = "%.3g"      # 变异体：把印刷精度砍到 3 位

# 换算规则**照抄上一轮已发表的面**：v4 的 price() 里 B 档只把 percent÷100、
# pm_abs/ineq_abs÷|pv|，其余（含 ineq_bare）按「已是声明货币」原样吃。
# v5 把 ineq_bare 也塞进了 ÷|pv| 族（CUR_SHAPES），本轮把它当**跨轮规则不一致**逐枚点名（C11）。
CONV_PCT = ("percent",)
CONV_ABS = ("pm_abs", "ineq_abs")
AS_WRITTEN = ("ineq_bare",)          # 只需去掉不等式标记，数值不改
RULE = dict([(s, u"÷100（百分数→相对）") for s in CONV_PCT] +
            [(s, u"÷声明值绝对值（绝对写法→相对）") for s in CONV_ABS] +
            [(s, u"原样（去掉不等式标记即声明货币）") for s in AS_WRITTEN])

ACTION = {
    "urel_other_currency": "把带按声明货币换算成相对数（规则见 v4 price()：百分数÷100；pm_abs/ineq_abs÷声明值绝对值；ineq_bare 去标记原样）",
    "pointer_in_urel": "把路径移到推导/证据列，本列另填真实相对不确定度（本腿不产 ok）",
    "urel_prose_band": "把散文带改写成数值上界，或连同推导一起移到证据列（本腿不产 ok）",
    "value_unparseable": "先修 prediction_value：文字描述应放 prediction 列（本腿不产 ok）",
    "urel_absent": "补 prediction_urel（整数靶填 0）或一并清空两列（清空＝不登记，不是修好）",
    "urel_zero_exact_noninteger": "urel=0 是精确声明：非整数靶须给真实相对不确定度（不许换算）",
    "negative_urel": "相对不确定度不得为负",
    "value_absent": "补 prediction_value",
    "clean_numeric": "无需动作",
    "other": "词表外——先补词表",
}


class Fatal(Exception):
    pass


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G = load("intake_v6_gate", GATE_SRC)
V5 = load("intake_v6_v5", V5_SRC)
CAR = load("intake_v6_carrier", CARRIER)


def convert_band(shape, num, pv_txt):
    """照 v4 price() 的 B 档规则换算成声明的相对货币。返回 (rel 或 None, 挡住的原因)。"""
    if num is None:
        return None, "no_numeral"
    if shape in CONV_PCT:
        return abs(float(num)) / 100.0, None
    if shape in CONV_ABS:
        pv = G.parse_number(pv_txt)
        if pv is None:
            return None, "value_side_blocks"
        v = abs(float(pv))
        if not v:
            return None, "pv_zero"
        return abs(float(num)) / v, None
    if shape in AS_WRITTEN:
        return abs(float(num)), None
    raise Fatal("换算规则表里没有形状 %s——先对齐 v4 的 price()，别自定第三档" % shape)


def build_props(nonempty, cmap):
    out = []
    for r in nonempty:
        typ, c = cmap[(r["owner"], r["claim_id"])]
        rel = rule = blocked = None
        prop = None
        if typ == "urel_other_currency":
            rel, blocked = convert_band(c.get("shape"), c.get("numeral"), r["prediction_value"])
            rule = RULE.get(c.get("shape"))
            if rel is not None:
                prop = FMT % rel
        flag_after = r["flag"]
        if prop is not None:
            flag_after = G.classify(r["prediction_value"], prop)[0]
        out.append({"owner": r["owner"], "claim_id": r["claim_id"], "type": typ,
                    "flag_before": r["flag"], "pv": r["prediction_value"],
                    "urel": r["prediction_urel"], "proposed": prop, "rule": rule,
                    "blocked_reason": blocked, "flag_after": flag_after, "action": ACTION[typ],
                    "rel": rel, "rel_v5": c.get("rel_converted"), "shape": c.get("shape")})
    return out


def ok_after_of(rows, props):
    after = dict(((p["owner"], p["claim_id"]), p["flag_after"]) for p in props)
    return sum(1 for r in rows if after.get((r["owner"], r["claim_id"]), r["flag"]) == "ok")


def cross_check_v4(props):
    """建议新串 vs v4 面自己的 urel_B（第二把尺），逐枚点名偏差。"""
    v4f = json.load(io.open(V4_FACE, encoding="utf-8", errors="ignore"))
    chan = dict((c["claim_id"], c) for c in v4f["channels"])
    diffs, miss = [], []
    for p in props:
        if p["proposed"] is None:
            continue
        ch = chan.get(p["claim_id"])
        if not ch or not ch["priced"]["targets"]:
            miss.append(p["claim_id"])
            continue
        ub = ch["priced"]["targets"][0]["urel_B"]
        v = float(G.parse_number(p["proposed"]))
        diffs.append({"claim_id": p["claim_id"], "proposed": v, "v4_urel_B": ub,
                      "rel_diff": abs(v - ub) / max(abs(ub), 1e-300),
                      "coarse_rel_diff": abs(float(COARSE % p["rel"]) - ub) / max(abs(ub), 1e-300),
                      "verdict": ch["priced"]["verdict"]})
    return chan, diffs, miss


def hit_replay(chan, props):
    """把建议新串喂回观测载体自己的 hit_test，与 v4 面 B 档判决对照（判决不自定）。"""
    byid = dict((p["claim_id"], p) for p in props if p["proposed"] is not None)
    out = []
    for cid, ch in chan.items():
        p = byid.get(cid)
        if not p or ch["priced"]["verdict"] != "FLIP":
            continue
        for t in ch["priced"]["targets"]:
            if t["A"] == "MISS" and t["B"] == "HIT":
                pred = float(G.parse_number(ch["pv"]))
                new = G.parse_number(p["proposed"])
                out.append({"claim_id": cid, "target": t["key"], "obs": t["obs"],
                            "urel_A": t["urel_A"], "proposed": float(new),
                            "hit_A": bool(CAR.hit_test(pred, t["obs"], t["urel_A"], 3)),
                            "hit_new": bool(CAR.hit_test(pred, t["obs"], float(new), 3)),
                            "v4_B": t["B"]})
    return out


def run_controls(nonempty, props, ok_after, rows, cd, hits):
    CT = []

    def fire(pin, cond, detail):
        CT.append({"name": pin, "fired": bool(cond), "detail": detail})

    conv = [p for p in props if p["type"] == "urel_other_currency" and p["proposed"] is not None]
    blocked = [p for p in props if p["type"] == "urel_other_currency" and p["proposed"] is None]
    ptr = [p for p in props if p["type"] == "pointer_in_urel"]
    exact = [p for p in props if p["type"] == "urel_zero_exact_noninteger"]

    blank_ok = sum(1 for p in conv if G.classify("", "")[0] == "ok")
    fire(u"C1 删除支（照 v5 门禁建议「一并清空两列」）产出 0 条 ok，而换算支产出 %d 条 ⇒ 换算是唯一出登记的支"
         % len([p for p in conv if p["flag_after"] == "ok"]),
         blank_ok == 0 and len([p for p in conv if p["flag_after"] == "ok"]) > 0,
         [blank_ok, len([p for p in conv if p["flag_after"] == "ok"]),
          [G.classify("", "")[0] for _ in conv[:1]]])

    bad = [p["claim_id"] for p in blocked if p["flag_after"] == "ok"]
    not_prose = [p["claim_id"] for p in blocked if G.parse_number(p["pv"]) is not None]
    fire(u"C2 被值侧挡住的 %d 条一行都不许变 ok，且挡住的原因必须是值侧不是带侧" % len(blocked),
         bool(blocked) and not bad and not not_prose,
         [len(blocked), bad, not_prose, [p["claim_id"] for p in blocked][:9]])

    unparsed = [p["claim_id"] for p in conv if G.parse_number(p["proposed"]) is None]
    mutant = [(p["claim_id"], G.classify(p["pv"], p["proposed"] + u"（换算）")[0]) for p in conv[:4]]
    fire(u"C3 建议新串必须自己能被门禁解析；加一句注释即被门禁判成 non_numeric ⇒ 带注释的建议自己造新债",
         not unparsed and all(f == "non_numeric" for _, f in mutant),
         [unparsed, mutant])

    maxd = max([d["rel_diff"] for d in cd["diffs"]] or [0.0])
    maxc = max([d["coarse_rel_diff"] for d in cd["diffs"]] or [0.0])
    fire(u"C4 换算值必须复现 v4 面自己的 urel_B（最大相对偏差 %.3g ≤ %.3g），而粗到 %s 精度会把它推歪"
         % (maxd, TOL_FMT, COARSE),
         cd["diffs"] and maxd <= TOL_FMT and maxc > 1e-3,
         {"n_diff": len(cd["diffs"]), "max_rel_diff": maxd, "max_coarse_rel_diff": maxc,
          "worst": sorted(cd["diffs"], key=lambda d: -d["rel_diff"])[:3]})

    washtest = [(p["claim_id"], G.classify(p["pv"], "0.0")[0]) for p in exact]
    fire(u"C5 urel=0 的精确声明（%d 条）不许被「换算」洗成 ok——填 0 仍停在 WARN" % len(exact),
         exact and all(f == "urel_zero_noninteger" for _, f in washtest), washtest)

    moved = [(p["claim_id"], G.classify(p["pv"], "")[0]) for p in ptr[:8]]
    fire(u"C6 指针搬家之后本列只剩 partial/empty，永远不产出 ok ⇒「搬家」≠「登记」",
         ptr and all(f in ("partial", "empty") for _, f in moved),
         {"n_pointer": len(ptr), "sample": moved})

    sums = collections.Counter(p["type"] for p in props)
    after = ok_after_of(rows, props)
    conv_ok = len([p for p in conv if p["flag_after"] == "ok"])
    fire(u"C7 闭合：各型之和 = 非空行 %d，且修后 ok 全仓数（门禁现读）= 换算支产出的 ok 数"
         % len(nonempty),
         sum(sums.values()) == len(nonempty) and after == conv_ok and sums["other"] == 0,
         {"sums": dict(sums), "ok_after": after, "conv_ok": conv_ok})

    fire(u"C8 分母由扫描现取（%d 行 / %d 个文件），修后读数一律写成「ok/该分母」"
         % (len(rows), len(G.scan_registry()[1])),
         len(rows) > 0 and ok_after <= len(rows),
         {"rows": len(rows), "ok_before": int(sum(1 for r in rows if r["flag"] == "ok")),
          "ok_after": ok_after, "files": len(G.scan_registry()[1])})

    fire(u"C9 换算后的带喂回观测载体自己的 hit_test：必须与 v4 面 B 档同为 HIT，且原样当相对吃必须 MISS",
         hits and all(h["hit_new"] == (h["v4_B"] == "HIT") and not h["hit_A"] for h in hits),
         hits)

    fire(u"C10 工作单必须逐行覆盖非空登记行，且每行的建议新串要么可解析要么为 None",
         len(props) == len(nonempty) and
         all(p["proposed"] is None or G.parse_number(p["proposed"]) is not None for p in props),
         {"order_rows": len(props), "nonempty": len(nonempty),
          "with_proposal": len(conv), "blocked": len(blocked)})

    dis = [p for p in props if p["type"] == "urel_other_currency"
           and p["rel"] is not None and p["rel_v5"] is not None
           and abs(p["rel"] - p["rel_v5"]) > 1e-15]
    fix_shape, fix_num = V5.read_band(u"实现级 <1e-4")
    fix_pv = u"0.2289"
    rel_v6_fx = convert_band(fix_shape, fix_num, fix_pv)[0]
    rel_v5_fx = V5.rel_band(fix_shape, fix_num, G.parse_number(fix_pv))
    fire(u"C11 换算规则以 v4 面自己的 price() 为准：夹具 `实现级 <1e-4` 在 v6 规则下原样吃（%s），"
         u"在 v5 规则下除以声明值绝对值（%s）——两档必须分叉，且语料里分歧的每一枚都只能是 ineq_bare 型"
         % (FMT % rel_v6_fx, FMT % rel_v5_fx),
         fix_shape == "ineq_bare" and abs(rel_v6_fx - rel_v5_fx) > 0.5 * rel_v6_fx
         and bool(dis) and all(p["shape"] in AS_WRITTEN for p in dis),
         {"fixture": [fix_shape, fix_num, fix_pv, rel_v6_fx, rel_v5_fx],
          "corpus_disagreements": [p["claim_id"] for p in dis],
          "shapes": sorted({p["shape"] for p in dis})})

    dist = sorted(p["rel"] for p in conv if p["rel"] is not None)
    if not dist:
        raise Fatal("换算支为空——本轮的核心发现无输入，不许出预演")
    over = [p["claim_id"] for p in conv if p["rel"] is not None and p["rel"] >= 1]
    return CT, {"converted_rel_min": dist[0], "converted_rel_max": dist[-1],
                 "rel_ge_one": over, "cross_checked": len(cd["diffs"]),
                 "not_in_v4_admission": cd["miss"], "hits_replayed": len(hits),
                 "v5_rule_disagreement": [{"claim_id": p["claim_id"], "shape": p["shape"],
                                           "urel": p["urel"], "pv": p["pv"],
                                           "rel_v6": p["rel"], "rel_v5": p["rel_v5"],
                                           "factor": p["rel_v5"] / p["rel"]} for p in dis],
                 "fixture_rel_v6_vs_v5": [rel_v6_fx, rel_v5_fx]}


def write_outputs(face, props):
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    fp = os.path.join(OUT_DIR, FACE_NAME)
    with io.open(fp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(face, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write(u"\n")
    op = os.path.join(OUT_DIR, ORDER_NAME)
    with io.open(op, "w", encoding="utf-8-sig", newline="\r\n") as fh:
        w = csv.writer(fh)
        w.writerow([u"owner", u"claim_id", u"分型", u"修前flag", u"修后flag", u"prediction_value",
                    u"prediction_urel_现串", u"形状", u"换算规则", u"换算后相对带", u"建议新串",
                    u"挡住原因", u"v5规则换算值_仅备查", u"建议动作"])
        for p in props:
            w.writerow([p["owner"], p["claim_id"], p["type"], p["flag_before"], p["flag_after"],
                        p["pv"], p["urel"], p.get("shape") or "", p.get("rule") or "",
                        ("" if p["rel"] is None else FMT % p["rel"]),
                        p["proposed"] or "", p.get("blocked_reason") or "",
                        ("" if p.get("rel_v5") is None else FMT % p["rel_v5"]), p["action"]])
    return fp, op


def main():
    rows, paths = G.scan_registry()
    if not paths or not rows:
        raise Fatal("扫描集为空（%d 文件 / %d 行）——不许在空台账上出预演" % (len(paths), len(rows)))
    nonempty = [r for r in rows if r["flag"] != "empty"]
    classes, grid = V5.census(nonempty)
    if classes["other"]:
        raise Fatal("有 %d 行归不进词表（%s）——先修词表"
                    % (len(classes["other"]), [c["claim_id"] for c in classes["other"]][:6]))
    if sum(len(v) for v in classes.values()) != len(nonempty):
        raise Fatal("分型不闭合：%d ≠ 非空行 %d" % (sum(len(v) for v in classes.values()), len(nonempty)))

    cmap = {}
    for k in V5.VOCAB:
        for c in classes[k]:
            kk = (c["owner"], c["claim_id"])
            if kk in cmap:
                raise Fatal("同一 (体系, claim_id) 出现两次：%s——工作单会串行" % (kk,))
            cmap[kk] = (k, c)
    if len(cmap) != len(nonempty):
        raise Fatal("映射不闭合：%d ≠ %d" % (len(cmap), len(nonempty)))

    props = build_props(nonempty, cmap)
    ok_after = ok_after_of(rows, props)
    chan, diffs, miss = cross_check_v4(props)
    hits = hit_replay(chan, props)
    CT, dist = run_controls(nonempty, props, ok_after, rows, {"diffs": diffs, "miss": miss}, hits)

    face = {
        "instrument": os.path.relpath(os.path.abspath(__file__), ROOT).replace("\\", "/"),
        "generated_utc": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "single_sources": {
            "classification": "源码/靶场登记列校验_写入侧门禁.py（classify/parse_number/scan_registry）",
            "taxonomy": "源码/进门闸_v5_登记列欠账分型与破坏性建议针_2026-10-18.py（census/debt_of/VOCAB）",
            "hit_verdict": "源码/无量纲靶场审计.py（hit_test，3σ）",
            "band_conversion_cross_check": "数据/进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.json（urel_B/verdict）",
        },
        "totals": {"files": len(paths), "rows": len(rows),
                   "nonempty_rows": len(nonempty),
                   "ok_rows_before": int(sum(1 for r in rows if r["flag"] == "ok")),
                   "ok_rows_after_preview": ok_after,
                   "ok_rows_after_denominator_note": "分母 = rows（本册现取），修后=建议串喂回门禁的预演，未落他人台账"},
        "type_counts": dict(collections.Counter(p["type"] for p in props)),
        "converted": {"n": len([p for p in props if p["proposed"] is not None]),
                      "yield_ok": len([p for p in props if p["flag_after"] == "ok"]),
                      "not_ok_after_convert": [p["claim_id"] for p in props
                                               if p["proposed"] is not None and p["flag_after"] != "ok"]},
        "blocked": {"n": len([p for p in props if p["type"] == "urel_other_currency" and p["proposed"] is None]),
                    "reasons": dict(collections.Counter(
                        p["blocked_reason"] for p in props
                        if p["type"] == "urel_other_currency" and p["proposed"] is None)),
                    "claim_ids": [p["claim_id"] for p in props
                                  if p["type"] == "urel_other_currency" and p["proposed"] is None]},
        "caliber": {
            "authority": "换算规则取自已发表并钉住 md5 的 v4 面自己的 price()（源码/进门闸_v4_….py:127-132）",
            "divide_by_100": list(CONV_PCT), "divide_by_abs_pv": list(CONV_ABS),
            "as_written_relative": list(AS_WRITTEN),
            "v5_conflict": "v5 把 ineq_bare 也归入 ÷|pv| 族（V5.CUR_SHAPES），与 v4 的 B 档规则冲突——"
                           "v5 面已钉 md5 不可改，本册以 v6 工作单为准并在判定卷里点名",
            "v5_rule_disagreement": dist["v5_rule_disagreement"],
            "fixture_rel_v6_vs_v5": dist["fixture_rel_v6_vs_v5"],
        },
        "v4_cross_check": {"diffs": diffs, "not_in_v4_admission": miss, "tol_fmt": TOL_FMT,
                           "fmt": FMT, "coarse_fmt": COARSE},
        "hits_replayed": hits,
        "distribution": dist,
        "work_order": {"file": os.path.relpath(os.path.join(OUT_DIR, ORDER_NAME), ROOT).replace("\\", "/"),
                       "rows": len(props),
                       "by_owner": dict(collections.Counter(p["owner"] for p in props))},
        "controls": CT,
        "controls_fired": "%d/%d" % (sum(1 for c in CT if c["fired"]), len(CT)),
    }

    face["rc"] = 0 if all(c["fired"] for c in CT) else 1
    fp, op = write_outputs(face, props)

    if not QUIET:
        print("v6 预演：修前 ok = %d/%d，修后 ok = %d/%d（换算支产出 %d）" % (
            face["totals"]["ok_rows_before"], len(rows), ok_after, len(rows),
            face["converted"]["yield_ok"]))
        print("控制 %s 点火；面 %s（%d B）；工作单 %s（%d 行）" % (
            face["controls_fired"], fp, os.path.getsize(fp), op, len(props)))
        for c in CT:
            if not c["fired"]:
                print("  未点火：%s | %s" % (c["name"], json.dumps(c["detail"], ensure_ascii=False)[:200]))
    fired = sum(1 for c in CT if c["fired"])
    if fired != len(CT):
        raise Fatal("控制 %d/%d 点火——面已落盘（rc=1），红在哪一条看上面" % (fired, len(CT)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        sys.stderr.write("FATAL: %s\n" % e)
        sys.exit(2)
