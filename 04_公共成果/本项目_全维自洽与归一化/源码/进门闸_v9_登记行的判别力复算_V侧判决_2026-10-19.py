# -*- coding: utf-8 -*-
"""进门闸 v9：登记行的**判别力**复算（V 侧判决）。

问题由载体提出，不是我发明的：
- `判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08.md` §5 D2／§8.3：要求对已登记的严格预测
  逐条核「是否非测量锚 + 判别式 V₂」，并把 UFT-3 的 PASS 挂成 **BOUNDARY（V₂>0 未判）**；
- `判定_本项目_统一场论_D2质量侧核查_2026-10-09.md` 执行了它，但核的是**当时**的严 4（S18/S15 四枚）；
- v7∪v8 证明门禁口径下**可登记行的上界只有 5 枚**，而这 5 枚从未被问过 V。本册只问这一件事。

货币全部取自载体，不自立口径：
- 登记列语义：`源码/靶场登记列校验_写入侧门禁.py`（`band_form`/`to_relative`/`parse_number`/`scan_registry`）；
- 靶表、判别式、命中尺：`源码/无量纲靶场审计.py`（`build_targets`/`verdict_v`/`hit_test`/`worked_examples`）；
- 锚的语义（「对测量输入有非零依赖者计锚」）：`数据/靶场卡方联合拟合.json` 的 `caliber.reused_discriminant`。

本册对语料**只读**；写出只有自己的面、卷与（`--land` 时）落库的仪器副本。不碰他人文件。
用法：`python 进门闸_v9_….py`＝预跑（产物落 scratch/）；`--land`＝落库；
`--mutant=m1|m2|m4`＝只断仪器自己的一条推理，指定的控制必须红（红不了即该控制是橡皮章，本册直接 FATAL），产物加 `.mut-<名>` 后缀、不落库。
"""
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import types

try:
    from mpmath import mpf
except Exception:
    raise SystemExit("FATAL: 需要 mpmath（门禁与审计册都用它，本册不降级为 float）")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
if not os.path.isdir(os.path.join(ROOT, "openuft")):
    _up = HERE
    while _up and not os.path.isdir(os.path.join(_up, "openuft")):
        _n = os.path.dirname(_up)
        if _n == _up:
            break
        _up = _n
    if not os.path.isdir(os.path.join(_up, "openuft")):
        raise SystemExit("FATAL: 找不到 openuft 的仓根（本册须放在 源码/ 或 scratch/）")
    ROOT = _up
PROJP = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
SCRATCH = os.path.join(ROOT, "scratch")

GATE_SRC = os.path.join(SRC, "靶场登记列校验_写入侧门禁.py")
AUD_SRC = os.path.join(SRC, "无量纲靶场审计.py")
POOL_JSON = os.path.join(DATA, "靶场卡方联合拟合.json")
V8_FACE = os.path.join(DATA, "进门闸_v8_值列货币裁定_剥尾注通道定价_2026-10-19.json")
D2_DOC = os.path.join(PROJP, "判定_本项目_统一场论_D2质量侧核查_2026-10-09.md")

STEM = "进门闸_v9_登记行的判别力复算_V侧判决_2026-10-19"
INSTR_NAME = STEM + ".py"
FACE_NAME = STEM + ".json"
VOL_NAME = u"判定_" + STEM + ".md"
SELF_PATH = os.path.abspath(__file__)
LAND = "--land" in sys.argv[1:]
OUT_DIR = DATA if LAND else SCRATCH

# 变异体：把仪器自己的三条推理各断一处，指定的控制必须红——否则那条控制是橡皮章。
# 只动内存里的判断，绝不写语料；产物另名，不覆盖好面。
MUT = None
for _a in sys.argv[1:]:
    if _a.startswith("--mutant="):
        MUT = _a.split("=", 1)[1]
        LAND = False
        OUT_DIR = SCRATCH
EXPECTED_RED = {u"m1": u"X3",    # 关掉 10 靶门：C0093 被当成 sin²θ_W
                u"m2": u"X10",   # 锚计数归零：撤锚的反事实不再改变 V
                u"m4": u"X8"}    # 污染输入图像：只读复量应当报出「移动 1 份」
MUT_NAMES = {u"m1": u"10 靶门被关掉", u"m2": u"锚计数被抹平",
             u"m4": u"输入图像在判决后移动"}

PUBLISHED_GATE_MD5 = "e997593cd676213654fbd19d61615c76"   # v7 发表图（v7 卷与本卡共同钉住）
FMT = "%.12g"


class Fatal(Exception):
    pass


def md5(b):
    return hashlib.md5(b).hexdigest()


def rb(p):
    with open(p, "rb") as fh:
        return fh.read()


def load(tag, path):
    src = rb(path).decode("utf-8")
    mod = types.ModuleType(tag)
    mod.__file__ = os.path.abspath(path)
    sys.modules[tag] = mod
    exec(compile(src, os.path.abspath(path), "exec"), mod.__dict__)
    return mod


def sanitize(s):
    return (s or u"").replace(u"|", u"∣").replace(u"\r", u" ").replace(u"\n", u" ")


CONTROLS = []


def ctl(code, title, fired, payload=None):
    # 题面必须写完：残留的 %s/%d 会被原样印进控制表（读数看不见，题面却已发表）。
    leftover = re.findall(u"%[sdfg]", title or u"")
    if leftover:
        raise Fatal(u"控制 %s 的题面有未插值的占位符 %s：%s" % (code, leftover, title))
    CONTROLS.append({"code": code, "title": title, "fired": bool(fired), "payload": payload or {}})
    print(u"%s %s｜%s" % (u"[RED]" if not fired else u"[ok]", code, title))
    if not fired:
        print(u"      payload: %s" % json.dumps(payload or {}, ensure_ascii=False, default=str)[:700])


# ---------------------------------------------------------------------------
# 词表：把行内文本里的输入分成 锚／旋钮／理论输入／派生量／未分类赋值
# ---------------------------------------------------------------------------
LETTERS = u"0-9A-Za-z_α-ωΑ-Ω⁻¹²³"
ANCHOR_VOCAB = [
    (u"α_em", re.compile(u"α_?em|alpha_?em|1\\s*/\\s*127\\.9", re.I)),
    (u"α_s", re.compile(u"α_?s\\b|alpha_?s\\b|0\\.1184|0\\.1179", re.I)),
    (u"M_Z", re.compile(u"M_?Z\\b|m_?Z\\b|Z 玻色子质量", re.I)),
    (u"G（牛顿常数）", re.compile(u"(?<![" + LETTERS + u"])G(?![" + LETTERS + u"])|牛顿常数", re.I)),
    (u"m_e", re.compile(u"(?<![" + LETTERS + u"])m_?e(?![" + LETTERS + u"])|电子质量", re.I)),
    (u"m_P", re.compile(u"(?<![" + LETTERS + u"])m_?P(?![" + LETTERS + u"])|普朗克质量", re.I)),
    (u"m_t", re.compile(u"(?<![" + LETTERS + u"])m_?t(?![" + LETTERS + u"])|顶夸克质量", re.I)),
    (u"M_W", re.compile(u"M_?W\\b|W 玻色子质量", re.I)),
]
KNOB_VOCAB = [
    (u"M_SUSY／M_S（假设阈值）", re.compile(u"M_?SUSY|M_?S\\b|超对称阈值", re.I)),
    (u"tanβ（选择值）", re.compile(u"tan\\s*β|tanbeta", re.I)),
    (u"未纳入项（阈值／Yukawa 匹配）", re.compile(u"阈值项|未纳入|Yukawa", re.I)),
]
THEORY_VOCAB = [
    (u"b 系数（群论／物质含量）", re.compile(u"Δb|T[123]|\\bb\\b|b_ij|SM/MSSM", re.I)),
    (u"RGE 结构", re.compile(u"RGE|跑动|β 函数", re.I)),
    (u"重整化方案", re.compile(u"DR|MSbar|\\bMS\\b|matching|匹配", re.I)),
]
DERIVED_VOCAB = [
    (u"M_GUT／α_G／sin²θ_W（被解出的输出）", re.compile(u"M_?GUT|统一条件|α_?G|α1=α2|θ_?W|sin²θ|sin2θ", re.I)),
]
INHERIT = re.compile(u"同上输入|同上|同前")
ASSIGN = re.compile(u"([" + u"A-Za-zα-ωΑ-Ω_" + u"][A-Za-z0-9α-ωΑ-Ω_]{0,14})\\s*=\\s*[（(]?\\s*"
                    u"(-?\\d+(?:\\.\\d+)?(?:[eE][-+]?\\d+)?|1\\s*/\\s*\\d+(?:\\.\\d+)?)")
KNOWN_RX = re.compile(u"|".join([r.pattern for _, r in
                                 ANCHOR_VOCAB + KNOB_VOCAB + THEORY_VOCAB + DERIVED_VOCAB]), re.I)


def classify_tokens(txt):
    hit = lambda vocab: [n for n, rx in vocab if rx.search(txt)]
    an, kn, th, dv = hit(ANCHOR_VOCAB), hit(KNOB_VOCAB), hit(THEORY_VOCAB), hit(DERIVED_VOCAB)
    inherited = bool(INHERIT.search(txt))
    stray = []
    for m in ASSIGN.finditer(txt):
        sym = m.group(1)
        if not KNOWN_RX.search(sym):
            stray.append(sym + u"=" + m.group(2))
    collide = sorted((set(an) & set(kn)) | (set(an) & set(th)) | (set(an) & set(dv)) |
                     (set(kn) & set(th)) | (set(kn) & set(dv)) | (set(th) & set(dv)))
    return an, kn, th, dv, inherited, sorted(set(stray)), collide


ALIASES = [
    (u"alpha", [u"精细结构常数", u"α（", u"alpha_em 的预言"]),
    (u"alpha_grav_e", [u"α_grav", u"引力耦合"]),
    (u"m_mu_over_me", [u"m_μ/m_e", u"μ 子与电子质量比"]),
    (u"m_tau_over_me", [u"m_τ/m_e"]),
    (u"me_over_mP", [u"m_e/m_P"]),
    (u"mt_over_mW", [u"m_t/m_W"]),
    (u"sin2_thetaW", [u"sin²θ_W", u"sin2θ_W", u"sin^2θ_W", u"温伯格角", u"Weinberg"]),
    (u"n_gen", [u"代数 N", u"N_gen", u"世代数"]),
    (u"n_c", [u"色数", u"N_c"]),
    (u"alpha_s", [u"强耦合常数 α_S 的预言", u"α_S 预言"]),
]


def resolve_target(pred_text):
    t = (pred_text or u"").replace(u" ", u"")
    for key, alist in ALIASES:
        for a in alist:
            if a.replace(u" ", u"") in t:
                return key, a
    if MUT == u"m1" and t:
        return u"sin2_thetaW", u"(m1：绕过 10 靶门强塞)"
    return None, None


def main():
    t0 = time.time()
    G = load("v9_gate", GATE_SRC)
    A = load("v9_aud", AUD_SRC)
    for nm in ("band_form", "to_relative", "classify", "scan_registry", "parse_number"):
        if not hasattr(G, nm):
            raise Fatal(u"门禁缺函数 %s（单一真源漂移）" % nm)
    for nm in ("build_targets", "verdict_v", "hit_test", "worked_examples"):
        if not hasattr(A, nm):
            raise Fatal(u"审计册缺函数 %s（货币来源漂移）" % nm)

    gate_raw = rb(GATE_SRC)
    gate_md5 = md5(gate_raw)
    own_src = rb(SELF_PATH)
    own_lf = own_src.replace(b"\r\n", b"\n")
    landed_image = own_lf.replace(b"\n", b"\r\n")
    instr_image = landed_image if LAND else own_lf
    instr_bytes, instr_md5 = len(instr_image), md5(instr_image)

    rows, _paths = G.scan_registry()
    if not rows:
        raise Fatal(u"门禁扫到 0 行——判据集塌缩，不许发布")
    rows_total, files_total = len(rows), len(set([r["file"] for r in rows]))

    # 只读声明的可执行化：把本册判据的全部输入（claims 台账 + 两把源刀）先存一张图像，
    # 判决算完后、落盘前再量一次——语料若在判决之后移动，这张面立即作废而不是加注。
    corpus_paths = sorted(set([r["file"] for r in rows]) | {GATE_SRC, AUD_SRC})
    corpus_before = dict([(p, md5(rb(p))) for p in corpus_paths])
    if MUT == u"m4" and corpus_paths:
        corpus_before[corpus_paths[0]] = u"0" * 32   # 伪造「判决后语料移动」

    def sweep(tag):
        now = dict([(p, md5(rb(p))) for p in corpus_paths])
        moved = sorted([os.path.relpath(p, ROOT).replace("\\", "/")
                        for p in corpus_paths if now.get(p) != corpus_before.get(p)])
        return {"tag": tag, "inputs": len(corpus_paths), "moved": moved}

    v8 = json.loads(rb(V8_FACE).decode("utf-8"))
    v7_ids = sorted(set(v8.get("v7_ok_ids") or []))
    strip_ids = sorted(set(v8.get("strip_ok_ids") or []))
    ceiling = sorted(set(v7_ids) | set(strip_ids))
    ctl(u"X1", u"上界集现读：v7 ok %d 枚 ⊕ v8 剥尾注 %d 枚＝并 %d 枚、交 %d 枚（应为 5 与 0）"
        % (len(v7_ids), len(strip_ids), len(ceiling), len(set(v7_ids) & set(strip_ids))),
        len(ceiling) == 5 and not (set(v7_ids) & set(strip_ids)),
        {"v7_ids": v7_ids, "strip_ids": strip_ids, "ceiling": ceiling})

    by_id = {}
    for r in rows:
        by_id.setdefault(r["claim_id"], r)
    missing = [c for c in ceiling if c not in by_id]
    if missing:
        raise Fatal(u"上界集有 %d 枚已不在门禁扫描集：%s（语料在两轮之间移动，须先复核）" % (len(missing), missing))

    # 全部 claims.csv 的字段现读（可判面要扫全体，不能只读那 5 枚所在文件）
    fields = {}
    order_by_file = {}
    for path in sorted(set([r["file"] for r in rows])):
        order = []
        with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
            for rec in csv.DictReader(fh):
                cid = (rec.get("claim_id") or u"").strip()
                if not cid:
                    continue
                order.append(cid)
                fields[(path, cid)] = {k: (v or u"").strip() for k, v in rec.items() if k}
        order_by_file[path] = order
        for i, cid in enumerate(order):
            txt = fields[(path, cid)].get("assumptions", u"")
            if INHERIT.search(txt):
                src_cid = u""
                for j in range(i - 1, -1, -1):
                    prev = fields[(path, order[j])].get("assumptions", u"")
                    if ASSIGN.search(prev) and not INHERIT.search(prev):
                        src_cid = order[j]
                        break
                fields[(path, cid)]["_inherit_from"] = src_cid

    tg = {t["key"]: t for t in A.build_targets()}
    per = []
    cover_flags = []
    for cid in ceiling:
        r = by_id[cid]
        path, f = r["file"], fields[(r["file"], cid)]
        key, alias = resolve_target(f.get("prediction", u""))
        shape, num = G.band_form(r["prediction_urel"])
        rel, blocked = G.to_relative(shape, num, r["prediction_value"])
        pv = G.parse_number(r["prediction_value"])
        inh_from = f.get("_inherit_from", u"")
        txt = f.get("assumptions", u"") + u"；" + f.get("statement", u"")
        if inh_from:
            par = fields[(path, inh_from)].get("assumptions", u"")
            txt += u"；" + par
        an, kn, th, dv, inh_mark, stray, collide = classify_tokens(txt)
        cover_flags.append((cid, collide, len(stray)))
        rec = {
            "claim_id": cid,
            "file": os.path.relpath(path, ROOT).replace("\\", "/"),
            "prediction_text": f.get("prediction", u""),
            "target_key": key, "target_alias_hit": alias,
            "target_name_zh": (tg[key]["name_zh"] if key else None),
            "obs": (tg[key]["value"] if key else None), "obs_urel": (tg[key]["urel"] if key else None),
            "gate_flag": r["flag"], "band_shape": shape,
            "band_relative": (None if rel is None else FMT % rel), "band_blocked_reason": blocked,
            "prediction_value": r["prediction_value"],
            "status": f.get("status", u""), "evidence_level": f.get("evidence_level", u""),
            "run_id": f.get("run_id", u""), "uncertainty_field": f.get("uncertainty", u""),
            "assumptions": f.get("assumptions", u""),
            "inherited_from": inh_from, "inherit_marker": inh_mark,
            "anchors": an, "knobs": kn, "theory_inputs": th, "derived": dv,
            "unclassified_assignments": stray,
        }
        if key and pv is not None and rec["obs"]:
            rec["is_measurement_anchor_copy"] = (mpf(r["prediction_value"]) == mpf(rec["obs"]))
            rec["hit"] = (bool(A.hit_test(pv, mpf(rec["obs"]), mpf(rec["band_relative"]), 3))
                          if rec["band_relative"] is not None else None)
        else:
            rec["is_measurement_anchor_copy"] = None
            rec["hit"] = None
        if key:
            n_hit = 1 if (rec["hit"] and not rec["is_measurement_anchor_copy"]) else 0
            n_free, n_anchor = len(set(kn)), (0 if MUT == u"m2" else len(set(an)))
            V, code, why = A.verdict_v(n_hit, n_free, n_anchor)
            if n_hit == 0:
                why = (u"该靶 3σ 外（预测 %s vs 观测 %s，带 %s）⇒ n_hit=0，"
                       u"审计册 verdict_v 在 n_hit=0 时返回 N（分母为零，不可判）"
                       % (r["prediction_value"], rec["obs"], rec["band_relative"]))
        else:
            n_hit = n_free = n_anchor = None
            V, code = None, u"N"
            why = u"预言对象不在 10 靶 ⇒ 不进 V 的分子（登记合格≠对世界有预言）"
        rec.update({"n_hit": n_hit, "n_free": n_free, "n_anchor": n_anchor,
                    "V": (None if V is None else float(V)), "V_code": code, "V_why": why})
        if key and stray:
            for tag, da, df in (("as_anchor", len(stray), 0), ("as_knob", 0, len(stray))):
                V2, c2, _ = A.verdict_v(n_hit, n_free + df, n_anchor + da)
                rec["sens_" + tag] = {"V": (None if V2 is None else float(V2)), "code": c2}
            rec["sens_flip"] = rec["sens_as_anchor"]["code"] != rec["sens_as_knob"]["code"]
        if key and n_hit == 1:
            V0, c0, _ = A.verdict_v(n_hit, n_free, 0)
            rec["V_if_no_anchor"] = {"V": float(V0), "code": c0}
            V00, c00, _ = A.verdict_v(n_hit, 0, 0)
            rec["V_if_neither"] = {"V": float(V00), "code": c00}
            if cid == u"S02-C0058":
                Vh, ch, _ = A.verdict_v(n_hit, n_free, n_anchor + 2)
                rec["V_if_anchor_inherited"] = {"V": float(Vh), "code": ch,
                                                "note": u"按物理实际补两个锚（α_em、α_s；文本未点名）"}
        per.append(rec)

    codes = {}
    for x in per:
        codes[x["V_code"]] = codes.get(x["V_code"], 0) + 1
    n_a = codes.get("A", 0)
    n_absent = sum(1 for x in per if x["target_key"] is None)
    n_copy = sum(1 for x in per if x["is_measurement_anchor_copy"])
    absent_ids = sorted([x["claim_id"] for x in per if x["target_key"] is None])
    stray_rows = [(x["claim_id"], x["unclassified_assignments"]) for x in per if x["unclassified_assignments"]]
    flips = [(x["claim_id"], x.get("sens_as_anchor", {}).get("code"), x.get("sens_as_knob", {}).get("code"))
             for x in per if x.get("sens_flip")]
    pop, pop_ids = 0, []
    for r in rows:
        if G.parse_number(r["prediction_value"]) is None:
            continue
        k, _ = resolve_target(fields.get((r["file"], r["claim_id"]), {}).get("prediction", u""))
        shape, num = G.band_form(r["prediction_urel"])
        rel, why = G.to_relative(shape, num, r["prediction_value"])
        if k and rel is not None:
            pop += 1
            pop_ids.append(r["claim_id"])

    ex1 = A.worked_examples()[0]
    ctl(u"X2", u"货币同源：审计册自己的算例例 1 必须给 V=-3、码 C（证明本册用的是它的尺）",
        abs(ex1["V"] + 3.0) < 1e-12 and ex1["verdict"] == u"C",
        {"name": ex1["name"], "n_hit": ex1["n_hit"], "n_free": ex1["n_free"],
         "n_anchor": ex1["n_anchor"], "V": ex1["V"], "verdict": ex1["verdict"]})

    ctl(u"X3", u"靶解析：不在 10 靶者逐枚点名，实测 %d 枚 %s（应恰 C0093＝「完整表示 Δb」群论恒等式）"
        % (n_absent, absent_ids), absent_ids == [u"S02-C0093"], {"absent": absent_ids})

    ctl(u"X4", u"非测量锚这一半：5 枚里预测值与靶观测值逐字相等者 %d 枚（应为 0；出现即不许计 n_hit）"
        % n_copy, n_copy == 0, {"copies": [x["claim_id"] for x in per if x["is_measurement_anchor_copy"]]})

    h_good = A.hit_test(mpf(u"0.23122"), mpf(tg["sin2_thetaW"]["value"]), mpf(tg["sin2_thetaW"]["urel"]), 3)
    h_bad = A.hit_test(mpf(u"0.375"), mpf(tg["sin2_thetaW"]["value"]), mpf(tg["sin2_thetaW"]["urel"]), 3)
    ctl(u"X5", u"命中尺有牙：pred＝观测 ⇒ HIT、SU(5) 树级 3/8 ⇒ MISS（实测 %s／%s）" % (h_good, h_bad),
        h_good is True and h_bad is False, {"hit_obs": h_good, "hit_tree_3_8": h_bad})

    inh_rows = [(x["claim_id"], x["inherited_from"]) for x in per if x["inherit_marker"]]
    ctl(u"X6", u"继承不许静默：带「同上输入」者必须解析到同册一枚具体行（%d 枚：%s）"
        % (len(inh_rows), inh_rows), bool(inh_rows) and all(a and b for a, b in inh_rows),
        {"inherit": inh_rows})

    collisions = [(c, col) for c, col, _ in cover_flags if col]
    ctl(u"X7", u"词表闭合：每个赋值符号都落进锚/旋钮/理论输入/派生四桶之一（未分类 %d 枚），且四桶名册互不重合（重合 %d 处）"
        % (sum(len(s) for _, s in stray_rows), len(collisions)),
        not stray_rows and not collisions,
        {"stray": stray_rows, "collisions": collisions})

    sweep_mid = sweep("判决计算后、落盘前")
    ctl(u"X8", u"中立性：门禁仍是 v7 发表图（现读 md5 %s）；语料只读——本册 %d 份输入（台账＋两把源刀）在判决计算后逐份复量，移动 0 份"
        % (gate_md5, sweep_mid["inputs"]),
        gate_md5 == PUBLISHED_GATE_MD5 and not sweep_mid["moved"],
        {"gate_md5": gate_md5, "gate_bytes": len(gate_raw), "expect": PUBLISHED_GATE_MD5,
         "sweep": sweep_mid})

    ctl(u"X9", u"码分布闭合：各码之和＝被评判行数 %d，A 码（V>0）＝%d" % (len(per), n_a),
        sum(codes.values()) == len(per) and len(per) == len(ceiling), {"codes": codes})

    load_bearing = [x["claim_id"] for x in per
                    if x.get("V_if_no_anchor") and x["V"] is not None
                    and x["V_if_no_anchor"]["V"] > x["V"]]
    best_after_strip_anchor = sorted(set(x["V_if_no_anchor"]["code"] for x in per if x.get("V_if_no_anchor")))
    ctl(u"X10", u"锚计数承重：撤掉锚（n_anchor→0）后 V 必须严格变大，实测 %d 枚 %s；只撤锚所能达到的最好码＝%s"
        % (len(load_bearing), load_bearing, u"、".join(best_after_strip_anchor) or u"—"),
        len(load_bearing) >= 1, {"load_bearing": load_bearing, "codes_after": best_after_strip_anchor})

    both_empty = [x["claim_id"] for x in per
                  if x.get("V_if_neither") and x["V_if_neither"]["code"] == u"A"]
    ctl(u"X13", u"正对照（尺子不是恒判 C）：把锚与旋钮**同时**撤掉（宣称既不吃测量也不吃旋钮）必须翻到 A，实测 %d 枚 %s"
        % (len(both_empty), both_empty), len(both_empty) >= 1, {"flipped_to_A": both_empty})

    inh58 = [x for x in per if x.get("V_if_anchor_inherited")]
    ctl(u"X14", u"锚名册是**下界**（少计只会让 V 偏乐观）：给 C0058 按物理实际补两个锚（α_em、α_s）后 V 必须更差——实测 %s"
        % (u"%s→%s（码 %s→%s）" % (FMT % inh58[0]["V"], FMT % inh58[0]["V_if_anchor_inherited"]["V"],
                                   inh58[0]["V_code"], inh58[0]["V_if_anchor_inherited"]["code"]) if inh58 else u"无"),
        bool(inh58) and inh58[0]["V_if_anchor_inherited"]["V"] < inh58[0]["V"],
        {"c58": (inh58[0] if inh58 else None)})

    files_with_rows = len(set([r["file"] for r in rows]))
    ctl(u"X11", u"分母现读：门禁现场返回 %d 行／台账 %d 份（其中贡献行的 %d 份）；"
                u"与 v8 面自报 files=%s／rows_total=%s 交叉一致"
        % (rows_total, len(_paths), files_with_rows, v8.get("files"), v8.get("rows_total")),
        rows_total == 462 and len(_paths) == (v8.get("files") or -1)
        and rows_total == v8.get("rows_total") and 0 < files_with_rows <= len(_paths),
        {"rows_total": rows_total, "paths": len(_paths), "files_with_rows": files_with_rows,
         "v8_files": v8.get("files"), "v8_rows": v8.get("rows_total")})

    ctl(u"X12", u"可判面（靶∈10靶 ∧ 值可解析 ∧ 带可换算）＝全仓 %d 枚；上界里除靶外者 %d 枚外必须全在可判面内"
        % (pop, n_absent), set(ceiling) - set(pop_ids) == set(absent_ids),
        {"population": pop, "ids": pop_ids, "ceiling_minus_pop": sorted(set(ceiling) - set(pop_ids))})

    pool = json.loads(rb(POOL_JSON).decode("utf-8"))
    d2_ids = sorted(set(re.findall(r"[A-Z]\d{2}-C\d{4}", rb(D2_DOC).decode("utf-8", "replace"))))
    drift = {"d2_2026_10_09_ids": d2_ids,
             "overlap_with_ceiling": sorted(set(d2_ids) & set(ceiling)),
             "pool_entry_count_2026_09_27": pool.get("entry_count"),
             "pool_rows_named_sin2_thetaW": sum(1 for e in pool.get("rows", []) if e.get("target") == u"sin2_thetaW"),
             "v8_files_scanned": v8.get("files"), "v8_rows_total": v8.get("rows_total")}

    face = {
        "instrument": INSTR_NAME,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rc": 0 if all(c["fired"] for c in CONTROLS) else 1,
        "mode": ("mutant:" + MUT) if MUT else ("land" if LAND else "dry"),
        "currency_sources": {
            "gate": {"path": os.path.relpath(GATE_SRC, ROOT).replace("\\", "/"),
                     "bytes": len(gate_raw), "md5": gate_md5},
            "auditor": {"path": os.path.relpath(AUD_SRC, ROOT).replace("\\", "/"),
                        "bytes": len(rb(AUD_SRC)), "md5": md5(rb(AUD_SRC))},
            "pool_caliber": pool.get("caliber"),
        },
        "denominator": {"rows_total": rows_total, "claims_files": files_total,
                        "ceiling": ceiling, "judgeable_population": pop},
        "rows": per,
        "aggregate": {"V_codes": codes, "V_gt_0_count": n_a, "target_absent": n_absent,
                      "measurement_anchor_copy": n_copy,
                      "band_is_implementation_scatter": sum(1 for x in per if re.search(
                          u"实现|两实现|交叉|=§", x["uncertainty_field"] or u""))},
        "drift_vs_d2_2026_10_09": drift,
        "read_only_sweep": sweep_mid,
        "controls": CONTROLS,
        "controls_total": len(CONTROLS),
        "controls_fired": sum(1 for c in CONTROLS if c["fired"]),
        "controls_red": [c["code"] for c in CONTROLS if not c["fired"]],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    face_json = json.dumps(face, ensure_ascii=False, indent=1)
    face_bytes = face_json.encode("utf-8")
    suffix = (u".mut-" + MUT + u"") if MUT else u""
    face_path = os.path.join(OUT_DIR, FACE_NAME.replace(".json", suffix + ".json"))

    if not all(c["fired"] for c in CONTROLS):
        print(u"控制未全点火：%s ⇒ 不落库（只把预跑面与卷写进 scratch）" % face["controls_red"])
        rc = 1
    else:
        rc = 0

    if MUT:
        want = EXPECTED_RED[MUT]
        if want not in face["controls_red"]:
            raise Fatal(u"变异体 %s（%s）没有打破它点名的控制 %s ⇒ 该控制是橡皮章，本册不许自证有效"
                        % (MUT, MUT_NAMES[MUT], want))
        others = [c for c in face["controls_red"] if c != want]
        print(u"MUT=%s（%s）：指定控制 %s 已红；连带红＝%s；rc=1" % (MUT, MUT_NAMES[MUT], want, others))

    # 全部判决计算完成后、任何写出之前，再量一次输入图像：移动即作废本轮（不是加注）。
    sweep_last = sweep("判决计算后、写出前")
    if sweep_last["moved"] and not MUT:
        raise Fatal(u"语料在判决计算后移动（%d 份：%s）⇒ 本面/本卷作废，须重跑"
                    % (len(sweep_last["moved"]), sweep_last["moved"]))

    L = []
    P = L.append
    P(u"# 判定 · 进门闸 v9 · 登记行的**判别力**复算（V 侧判决）· 2026-10-19")
    P(u"")
    P(u"| 项 | 值 |")
    P(u"|---|---|")
    P(u"| 仪器 | `%s` |" % INSTR_NAME)
    P(u"| 面 | `%s` |" % FACE_NAME)
    P(u"| 判据来源 | 登记列语义＝门禁单一真源；靶表／V／命中尺＝`源码/无量纲靶场审计.py`；锚语义＝`数据/靶场卡方联合拟合.json` 的 `caliber` |")
    P(u"| 分母 | 门禁现场返回 %d 行／%d 份 claims.csv（X11）；可判面（靶＋值＋带三件齐）＝%d 枚（X12）|" % (rows_total, files_total, pop))
    P(u"| 一句话 | **登记面最好的 5 枚里，V>0 的有 %d 枚** |" % n_a)
    P(u"| 红线 | 本册不改任何 claims.csv、不动门禁、不提升任何体系证据等级；只把 2026-10-08 册挂在 UFT-3 上的 BOUNDARY（「V₂>0 未判」）对**当前**存活集判掉 |")
    P(u"")
    P(u"## §1 为什么是这 5 枚")
    P(u"")
    P(u"《达成度重算与最小闭合清单》（2026-10-08）§5 把 D2 的通过标准写成「数量已够，但判别式 V₂>0 未判、且须逐条核对是否属非测量锚」，§8.3 又称之为「本册定位出的真实卡点」。")
    P(u"次日《D2 质量侧核查》（2026-10-09）用四重过滤执行了它，名册是 `%s`（其中 2 枚已 falsified、2 枚无误差棒）。" % u"、".join(d2_ids))
    P(u"十天里语料移动了：本册现读 %d 行／%d 份台账，而 v7（建议档换算）∪ v8（剥尾注）给出的**登记上界**是另一组 `%s`，与上列名册交集 **%d 枚**——"
      % (rows_total, files_total, u"、".join(ceiling), len(drift["overlap_with_ceiling"])))
    P(u"对这一组，D2 的四重过滤（非重定义／有误差棒／未判伪／带数值）**全部通过**（面内逐枚带 `status`、`evidence_level`），所以卡点确实前移到本册问的这一件事：**锚与旋钮的记账**。")
    P(u"")
    P(u"## §2 逐枚账目（值、名册、计数全部现读）")
    P(u"")
    P(u"| claim | 靶 | 预测值 | 观测值 | 带：形状→相对 | 3σ | 锚名册 | 旋钮名册 | n(h/f/a) | V | 码 |")
    P(u"|---|---|---|---|---|---|---|---|---|---|---|")
    for x in per:
        P(u"| %s | %s | %s | %s | %s→%s | %s | %s | %s | %s/%s/%s | %s | %s |" % (
            x["claim_id"],
            sanitize(x["target_name_zh"] or u"不在 10 靶（预言＝`%s`）" % x["prediction_text"]),
            sanitize(x["prediction_value"]), sanitize(x["obs"] or u"—"),
            sanitize(x["band_shape"] or u"—"),
            sanitize(x["band_relative"] or u"挡住：%s" % x["band_blocked_reason"]),
            (u"HIT" if x["hit"] else (u"MISS" if x["hit"] is False else u"—")),
            sanitize(u"、".join(x["anchors"]) or u"（无）"), sanitize(u"、".join(x["knobs"]) or u"（无）"),
            x["n_hit"], x["n_free"], x["n_anchor"],
            (u"—" if x["V"] is None else FMT % x["V"]), x["V_code"]))
    P(u"")
    P(u"码义逐字取自审计册 `verdict_v`：A＝有信息增益（输出多于输入，真正的派生候选）；B＝等价交换；C＝净消耗（测量值的重新包装＝伪派生）；N＝不可判。")
    P(u"分布：%s ⇒ **A（V>0）%d 枚**。" % (u"、".join(u"%s＝%d" % (k, v) for k, v in sorted(codes.items())), n_a))
    P(u"")
    P(u"## §3 判决的承重件")
    P(u"")
    for x in per:
        if x["target_key"] and x["n_hit"] == 1:
            V0 = x["V_if_no_anchor"]
            P(u"- **%s**：现账 V＝%s（码 %s，锚 %d／旋钮 %d）。**若**宣称纯第一性（n_anchor→0）则 V＝%s（码 %s）——差距全部来自锚名册 %s。" % (
                x["claim_id"], FMT % x["V"], x["V_code"], x["n_anchor"], x["n_free"], FMT % V0["V"], V0["code"],
                sanitize(u"、".join(x["anchors"]))))
    P(u"- X10（承重）：撤掉锚之后 V 严格变大的有 %d 枚 %s；但**只撤锚**所能达到的最好码是 %s——即「把测量输入拿掉」还不足以翻成 A。"
      % (len(load_bearing), load_bearing, u"、".join(best_after_strip_anchor) or u"—"))
    P(u"- X13（正对照）：把锚**与旋钮同时**撤掉（等于宣称既不吃测量、也不吃假设阈值）时，%d 枚翻到 A %s ⇒ 判别式本身能给 A，"
      % (len(both_empty), both_empty))
    P(u"  本册的负判不是尺子恒红，而是这些行的输入账确实占着分子。")
    P(u"- X14（方向）：文本没点名的锚只能少计，少计只会让 V 偏乐观——按物理实际给 C0058 补 α_em、α_s 两锚，V 从 %s 变到 %s。"
      % (FMT % [x for x in per if x["claim_id"] == u"S02-C0058"][0]["V"],
         FMT % [x for x in per if x["claim_id"] == u"S02-C0058"][0]["V_if_anchor_inherited"]["V"]))
    P(u"- X5：命中尺在两端都有牙——pred＝观测判 HIT，SU(5) 树级 3/8 判 MISS（与池面 `SU5-sin2_thetaW` 反证行同向）。")
    P(u"- X4：**非测量锚这一半过了**（%d 枚复写），没过的是**增益**那一半。这一句要说细：预言值 0.2289／0.2319／0.2318 都不等于观测 0.23122，所以它们不是把测量抄回来；" % n_copy)
    P(u"  但它们的**输入**是测量常数（α_em、α_s、M_Z），产出 1 个数要消耗 2–3 个锚 ⇒ V≤0。这正是审计册例 1（α_grav＝(m_e/m_P)²，V＝−3）的同型，只是程度轻。")
    P(u"- X3：`S02-C0093` 的预言是「完整表示 Δb＝0（精确）」——群论恒等式，不在 10 靶内。它进得了登记上界（`urel=0` 对精确靶合法），**但不进 V 的分子**；")
    P(u"  若把它当成一条无量纲预言计入，池里就会多出一枚零判别力的格（与 2026-09-27 池面 `axis_b: zero_power` 同一诊断）。")
    P(u"- 误差棒的**来源**（面内 `uncertainty_field` 逐枚印出，本册不替作者改写）：5 枚里 %d 枚的带写明是实现间离散／交叉核对（「两实现离散」「实现级」「=§24 数值」）。" % face["aggregate"]["band_is_implementation_scatter"])
    P(u"  门禁的 `ok` 只保证「有数有带、带可解析」，不保证那条带是**理论**不确定度——这是债 C 的精确形状，记为债 **F**。")
    P(u"")
    P(u"## §4 中立性与跨轮漂移")
    P(u"")
    P(u"门禁 md5 `%s`＝v7 发表图（X8 现读）；只读不是声明而是复量：本册 %d 份输入（台账＋两把源刀）在判决计算后与写出前各量一次，移动 %d／%d 份"
      u"（写出前若移动即 FATAL，本面作废）。跨轮对照：2026-09-27 池面 `entry_count=%s`、点名 `sin2_thetaW` 的行 %d 枚；"
      % (gate_md5, sweep_mid["inputs"], len(sweep_mid["moved"]), len(sweep_last["moved"]),
         drift["pool_entry_count_2026_09_27"], drift["pool_rows_named_sin2_thetaW"]))
    P(u"v8 面自报 files=%s／rows_total=%s，与本册 X11 的 %d／%d 同值。登记行与进池行是**两套账**：v8 已证池只吃无量纲靶，本册再证即便进池也要过 V——"
      % (drift["v8_files_scanned"], drift["v8_rows_total"], rows_total, files_total))
    P(u"「门禁放行」既不等于「可登记」，更不等于「有贡献」。")
    P(u"")
    P(u"## §5 裁定与债")
    P(u"")
    P(u"1. **净读数**：在登记面最好的 5 枚上 V>0 者 **%d 枚**。故 2026-10-08 册挂在 UFT-3 的 BOUNDARY 对这一组判**不通过**：" % n_a)
    P(u"   UFT-3 的 PASS 只到「有数有带」为止，不到「派生」；`完成统一场论` 在这一层仍无支撑。")
    P(u"2. 债 **F（本册新增）**：误差棒来源须分档（实现间离散／理论截断／测量不确定度三种货币在门禁里同形）。本册逐枚印出但不改写。")
    P(u"3. 债 **C** 形状被钉死：450 行没数没带；**有数有带的这几行也还没有增益** ⇒ 要的是把测量锚换成第一性输入的推导工作，不是登记口径的放宽。")
    P(u"4. 债 **B/D/E** 原样挂着（`ineq_bare` 档裁定、基线欠登记 106 条、有量纲值进池的量纲折算口径）。")
    P(u"")
    P(u"## §6 自检控制（%d/%d 点火）" % (sum(1 for c in CONTROLS if c["fired"]), len(CONTROLS)))
    P(u"")
    P(u"| 码 | 题面 | 点火 |")
    P(u"|---|---|---|")
    for c in CONTROLS:
        P(u"| %s | %s | %s |" % (c["code"], sanitize(c["title"]), u"是" if c["fired"] else u"**否**"))
    P(u"")
    P(u"上表绿只证明控制**在真数据上不报警**。三枚变异体（`--mutant=m1｜m2｜m4`：绕过 10 靶门／抹平锚计数／伪造判决后语料移动）")
    P(u"各点名打破一条控制（m1→X3、m2→X10、m4→X8），跑在本面之外、产物另存为 `scratch/…json.mut-m1` 一类的名字，不覆盖上面这张面；")
    P(u"若指定控制不红，仪器自己 FATAL——「全绿」不算证据这一条写在代码里，不写在 prose 里。")
    P(u"")
    P(u"## §7 产物钉")
    P(u"")
    P(u"（本卷不钉自己；下面这一行钉面与仪器，`--land` 分支在落盘后从**盘上的卷**找回这两个数并量盘像，不符即 FATAL。）")
    P(u"")
    P(u"面 `%s` %d B／md5 `%s`；仪器 `%s` %d B／md5 `%s`" % (FACE_NAME, len(face_bytes), md5(face_bytes),
                                                              INSTR_NAME, instr_bytes, instr_md5))
    P(u"")
    vol_text = u"\r\n".join(L) + u"\r\n"
    residue = re.findall(u"%[sdfg]", vol_text)
    if residue:
        raise Fatal(u"卷面有 %d 处未插值占位符 %s ⇒ 不落盘" % (len(residue), sorted(set(residue))))
    vol_bytes = vol_text.encode("utf-8")
    vol_path = os.path.join(PROJP if LAND else SCRATCH,
                            VOL_NAME.replace(u".md", suffix + u".md") if MUT else VOL_NAME)

    open(face_path, "wb").write(face_bytes)
    if LAND:
        open(os.path.join(SRC, INSTR_NAME), "wb").write(landed_image)
    open(vol_path, "wb").write(vol_bytes)
    if LAND:
        # 分箱不是习惯而是断言：面进 数据/、卷与 v7／v8 同目录、仪器进 源码/。
        if os.path.dirname(face_path) != DATA:
            raise Fatal(u"面分箱走偏：%s" % face_path)
        preced = sorted([f for f in os.listdir(PROJP) if f.startswith(u"判定_进门闸_v")])
        if VOL_NAME not in preced or len(preced) < 3:
            raise Fatal(u"卷未与 v7／v8 同目录并列（PROJP 下判定_进门闸_v*＝%s）" % preced)
        landed_instr = rb(os.path.join(SRC, INSTR_NAME))
        scratch_src = rb(SELF_PATH) if SELF_PATH != os.path.join(SRC, INSTR_NAME) else landed_instr
        if scratch_src.replace(b"\r\n", b"\n") != landed_instr.replace(b"\r\n", b"\n"):
            raise Fatal(u"W1 落盘的刀≠手里的刀")
        on_vol = open(vol_path, "rb").read().decode("utf-8")
        on_face = rb(face_path)
        m = re.search(u"面 `%s` (\\d+) B／md5 `([0-9a-f]{32})`；仪器 `%s` (\\d+) B／md5 `([0-9a-f]{32})`"
                      % (re.escape(FACE_NAME), re.escape(INSTR_NAME)), on_vol)
        if not m:
            raise Fatal(u"卷里找不到它自己印的产物钉行——本次产物不得引用")
        bad_f = (int(m.group(1)), m.group(2)) != (len(on_face), md5(on_face))
        bad_i = (int(m.group(3)), m.group(4)) != (len(landed_instr), md5(landed_instr))
        if bad_f or bad_i:
            raise Fatal(u"卷印的钉与盘上图像不符（面 %s／仪器 %s）——本次产物不得引用"
                        % (u"异" if bad_f else u"同", u"异" if bad_i else u"同"))
        print(u"W1＋钉行盘上复核通过：仪器 %d B（scratch 源 %d B，EOL 归一后逐字同）" % (len(landed_instr), len(scratch_src)))

    print(u"控制 %d/%d 点火，rc=%d｜面 %s %d B md5 %s｜卷 %s %d B md5 %s｜耗时 %.1fs" % (
        face["controls_fired"], face["controls_total"], rc,
        os.path.relpath(face_path, ROOT).replace("\\", "/"), len(face_bytes), md5(face_bytes),
        os.path.relpath(vol_path, ROOT).replace("\\", "/"), len(vol_bytes), md5(vol_bytes), time.time() - t0))
    print(u"V 码分布 %s｜V>0 %d 枚｜靶外 %d 枚｜锚复写 %d 枚｜可判面 %d 枚" % (codes, n_a, n_absent, n_copy, pop))
    for x in per:
        print(u"   %-11s target=%-13s hit=%-5s n(h,f,a)=%s/%s/%s V=%-8s code=%s 锚=%s 旋钮=%s 未分类=%s" % (
            x["claim_id"], x["target_key"], x["hit"], x["n_hit"], x["n_free"], x["n_anchor"],
            x["V"], x["V_code"], x["anchors"], x["knobs"], x["unclassified_assignments"]))
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        print(u"FATAL: %s" % e)
        sys.exit(2)
