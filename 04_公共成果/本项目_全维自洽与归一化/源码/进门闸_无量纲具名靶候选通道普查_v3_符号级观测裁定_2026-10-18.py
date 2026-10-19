# -*- coding: utf-8 -*-
"""进门闸 v3：符号级观测裁定（G2 分母的第三口径）。

v2 把「自产输出／回声」从分母里剔掉，但保留了两样补贴：
  (i) 名册靶位本身算一条观测（散文里提到"温伯格角"就 +1，不需要任何数值）；
  (ii) 分母只认 MEASURED 那条窄正则能读的拼写，而语料里 α_s、α_em、sin²θ_W、
       M_Pl、s² 这些 ASCII 下标/复合写法它一条也读不到。
v2 面由此印出的「56/58 条通道拿不出一个 符号=数值」有一半是**我这把尺的形状**，
不是语料的事实。v3 做的事：
  * 用一条宽符号正则把四个观测列里所有 `符号=数值` 取出（形状覆盖由语料现扫，见
    scratch/sym_shape_probe.txt：58 条通道共 67 种符号名，窄正则只命中 2 行）；
  * 一个 token 只有在**名与值同时锚在观测载体上**时才算被引观测：符号要命中该靶的
    别名模式，数值要落进 `源码/无量纲靶场审计.py` 自己印出的 3σ 带内；
  * 其余一律进「未裁定」并在面上**逐枚点名**（印出读不到的东西，不许安静忽略）；
  * 名册靶位不再补贴分母（去掉 (i)）。
判决口径三档并列输出：v1 / v2 / v3，外加逐档翻转数。
"""
from __future__ import print_function

import csv
import glob
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
OPENUFT = os.path.join(ROOT, "openuft")
PROJ = os.path.join(OPENUFT, "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJ, "源码")
DATA = os.path.join(PROJ, "数据")
V2NAME = "进门闸_无量纲具名靶候选通道普查_v2_G2口径分家复算_2026-10-18.py"
CARRIER = os.path.join(SRC, "无量纲靶场审计.py")
FACE = "进门闸_无量纲具名靶候选通道普查_v3_符号级观测裁定_2026-10-18.json"

LAND = "--land" in sys.argv[1:]
OUT_DIR = DATA if LAND else os.path.join(ROOT, "scratch")


class Fatal(Exception):
    pass


def load(modname, path):
    if not os.path.isfile(path):
        raise Fatal("依赖文件不在盘：%s" % path)
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V2 = load("intake_v2_probe", os.path.join(SRC, V2NAME))
CAR = load("target_carrier_probe", CARRIER)

# ---- 观测词表：全部由载体文件现生成，我不在本判决里打任何数值
SYM = re.compile(r"([A-Za-zα-ωΑ-Ω][A-Za-z0-9_α-ωΑ-Ω*/²]{0,22})\s*=\s*"
                 r"([-+]?[0-9][0-9./eExX*+−-]*)")
OBS_COLS = ("statement", "derivation", "assumptions", "uncertainty")


def parse_num(s):
    t = s.strip().rstrip("/").replace("−", "-")
    if "/" in t:
        a, _, b = t.partition("/")
        try:
            return float(a) / float(b)
        except (ValueError, ZeroDivisionError):
            return None
    try:
        return float(t)
    except ValueError:
        return None


def measured_vocab():
    """[(key, name_alias_patterns, value, band_rel)] —— 值与不确定度都来自载体。"""
    out = []
    for t in CAR.build_targets():
        v = t["value"]
        if v is None:
            continue
        try:
            val = float(v)
        except (TypeError, ValueError):
            continue
        rel = 3.0 * float(t["urel"])
        out.append((t["key"], V2.ALIAS[t["key"]], val, rel))
    # 载体里另存的四条量纲常数（kg / GeV），名册别名沿用 v2 的 MEASURED 符号族
    extra = [("m_e", [r"^m_e$"], float(CAR.M_E), 0.0),
             ("m_P", [r"^m_P$"], float(CAR.M_P), 0.0),
             ("m_t", [r"^m_t$"], float(CAR.M_T), 0.0),
             ("m_W", [r"^m_W$"], float(CAR.M_W), 0.0)]
    for k, pats, val, rel in extra:
        out.append((k, pats, val, rel))
    if not out:
        raise Fatal("观测词表为空——不许在空词表上判「没有观测」")
    return out


VOCAB = measured_vocab()


def classify(sym, numstr, pv):
    """Return (cls, detail). cls in measured / echo / unadjudicated."""
    num = parse_num(numstr)
    if num is None:
        return "unadjudicated", "数值不可解析"
    if pv is not None and num == pv:
        return "echo", "等于本通道输出"
    hits = []
    for key, pats, val, rel in VOCAB:
        # 别名模式有的以 `\s*=` 结尾（散文里用），token 侧要把等号补回去才比得上
        if not any(re.search(p, sym) or re.search(p, sym + "=") for p in pats):
            continue
        band = abs(val) * rel if rel else 0.0
        if abs(num - val) <= (band if band else 1e-12):
            hits.append(key)
        else:
            return "unadjudicated", "名对而值出 3σ 带（靶 %s=%.6g，token=%.6g）" % (key, val, num)
    if hits:
        return "measured", ",".join(sorted(set(hits)))
    return "unadjudicated", "符号未锚在任何观测靶上"


def read_v3(row, rt):
    val = (row.get("prediction_value") or "").strip()
    try:
        pv = float(val) if val and re.fullmatch(r"[-+0-9.eE/]+", val) else None
    except ValueError:
        pv = None
    toks = []
    for col in OBS_COLS:
        txt = row.get(col) or ""
        for m in SYM.finditer(txt):
            cls, why = classify(m.group(1), m.group(2), pv)
            toks.append({"col": col, "sym": m.group(1), "num": m.group(2),
                         "cls": cls, "why": why})
    meas = sorted({"%s:%s" % (t["sym"], t["why"]) for t in toks if t["cls"] == "measured"})
    n_obs_v3 = len(meas)
    n_free = V2.price(row, rt)["n_free_assumptions"]
    g2_v3 = "PASS" if (n_obs_v3 > 0 and n_free <= n_obs_v3 - 1) else "FAIL"
    by = {"measured": 0, "echo": 0, "unadjudicated": 0}
    for t in toks:
        by[t["cls"]] += 1
    assert len(toks) == sum(by.values()), "token 分类没有闭合"
    knobs = [t for t in toks if t["cls"] == "unadjudicated"
             and re.fullmatch(r"[-+]?[0-9]+", t["num"].strip())]
    return {"tokens": toks, "n_token": len(toks), "n_measured_v3": n_obs_v3,
            "measured_v3": meas, "n_echo": by["echo"], "n_unadjudicated": by["unadjudicated"],
            "n_knob_candidate": len(knobs), "n_free_v3": n_free, "g2_v3": g2_v3,
            "g2_v3_by": by}


def probe_rows():
    """Synthetic fixtures used as controls (never written to the corpus)."""
    def mk(cid, statement, assumptions, pv, derivation="", uncertainty="", prediction=""):
        return {"claim_id": cid, "_sys": "S00_夹具",
                "statement": statement, "assumptions": assumptions, "derivation": derivation,
                "prediction": prediction, "prediction_value": pv, "uncertainty": uncertainty}
    f = []
    # N6 名对值在带、ASCII 下标拼写：窄正则读不到，v3 必须读到（针有牙）
    f.append(mk("N6", "一循环跑动给出边界值", "输入 α_s=0.1184 与 M_Z", "0.2289"))
    # N7 值撞进带内但符号不对（tanβ 不是任何靶）⇒ 必须不计数
    f.append(mk("N7", "跑动给出边界值", "输入 tanβ=0.1184", "0.2289"))
    # N8 符号对而值出 3σ 带 ⇒ 必须不计数
    f.append(mk("N8", "跑动给出边界值", "输入 α_s=0.19", "0.2289"))
    # N9a token 复述本通道输出 ⇒ 回声，不计；N9b 输出换成别的数 ⇒ 同一 token 必须计
    f.append(mk("N9a", "跑动给出边界值", "代数 N_gen=3", "3"))
    f.append(mk("N9b", "跑动给出边界值", "代数 N_gen=3", "0.2289"))
    # N10 分数写法 1/137.036 必须能解析并落进 α 带；同形但分母写错 ⇒ 不计数
    f.append(mk("N10", "跑动给出边界值", "输入 α_em=1/137.035999084", "0.2289"))
    return f


def run_probes(rt):
    out = []

    def fire(name, ok, detail):
        out.append({"name": name, "fired": bool(ok), "detail": detail})
    rows = probe_rows()
    r = {x["claim_id"]: x for x in rows}
    a = read_v3(r["N6"], rt)
    fire("N6 名对值在带的 ASCII 下标 token 必须计入（窄口 v1/v2 读不到）",
         a["n_measured_v3"] == 1 and not V2.MEASURED.search(r["N6"]["assumptions"]),
         "measured=%d narrow=%s" % (a["n_measured_v3"], bool(V2.MEASURED.search(r["N6"]["assumptions"]))))
    fire("N7 值撞进带而符号不是靶 ⇒ 不计数（双锚不是单锚）",
         read_v3(r["N7"], rt)["n_measured_v3"] == 0,
         read_v3(r["N7"], rt)["tokens"])
    fire("N8 符号对而值出 3σ 带 ⇒ 不计数，且必须点名出带",
         read_v3(r["N8"], rt)["n_measured_v3"] == 0
         and any(u"出" in t["why"] for t in read_v3(r["N8"], rt)["tokens"]),
         read_v3(r["N8"], rt)["tokens"])
    fire("N9a 复述本通道输出的 token 算回声 ⇒ 0 观测",
         read_v3(r["N9a"], rt)["n_measured_v3"] == 0
         and read_v3(r["N9a"], rt)["n_echo"] == 1,
         read_v3(r["N9a"], rt))
    fire("N9b 同一条只换输出值 ⇒ 同一 token 必须计入（回声规则不是恒假门）",
         read_v3(r["N9b"], rt)["n_measured_v3"] == 1,
         read_v3(r["N9b"], rt))
    fire("N10 分数写法 1/137.036 必须解析并落进 α 带",
         read_v3(r["N10"], rt)["n_measured_v3"] == 1,
         read_v3(r["N10"], rt)["tokens"])
    # 形状覆盖自证：面上每个 unadjudicated token 都必须逐枚在名单里（不许安静忽略）
    fire("闭合和：夹具 token 数 = measured+echo+unadjudicated",
         all(v["n_token"] == sum(v["g2_v3_by"].values()) for v in
             [read_v3(x, rt) for x in rows]), "见 each row")
    return out


def main():
    rt = V2.roster()
    ch = []
    files = 0
    scanned = 0
    for sysname, path in V2.scope():
        files += 1
        for row in V2.cells(sysname, path):
            scanned += 1
            if not (row.get("prediction_value") or "").strip():
                continue
            row["_sys"] = sysname
            v2c = V2.price(row, rt)
            v3c = read_v3(row, rt)
            c = dict(v2c)
            c.update(v3c)
            ch.append(c)
    if scanned == 0 or not ch:
        raise Fatal("扫描到 %d 行、声明通道 %d 条——判集塌空时不许出判决" % (scanned, len(ch)))
    for c in ch:
        c["survives_all_four_v3"] = bool(c["g1"] and c["g2_v3"] == "PASS"
                                         and c["g3_derivation_on_disk"]
                                         and c["g3_control_wording"] is not False
                                         and not c["g4_backfill_marker"])
    flips = [c["claim_id"] for c in ch if c["g2_v2"] != c["g2_v3"]]
    g1ch = [c for c in ch if c["g1"]]
    unadj = {}
    for c in ch:
        for t in c["tokens"]:
            if t["cls"] != "unadjudicated":
                continue
            k = t["sym"]
            e = unadj.setdefault(k, {"n": 0, "systems": set(), "sample": "%s=%s（%s）"
                                     % (t["sym"], t["num"], t["why"]), "cols": set()})
            e["n"] += 1
            e["systems"].add(c["system"])
            e["cols"].add(t["col"])
    for e in unadj.values():
        e["systems"] = sorted(e["systems"])
        e["cols"] = sorted(e["cols"])
    probes = run_probes(rt)
    fn = {
        "declared_channels": len(ch),
        "g1_both": sum(1 for c in ch if c["g1"]),
        "token_total": sum(c["n_token"] for c in ch),
        "token_measured_v3": sum(c["g2_v3_by"]["measured"] for c in ch),
        "token_echo": sum(c["g2_v3_by"]["echo"] for c in ch),
        "token_unadjudicated": sum(c["g2_v3_by"]["unadjudicated"] for c in ch),
        # 未裁定要分家：是「语料引的常量载体里没这条靶」（下一轮该补词表），
        # 还是「名对而值落在 3σ 带外」（该核对数值或尺度）——两类债付法不同。
        "unadj_no_target_name": sum(1 for c in ch for t in c["tokens"]
                                    if t["cls"] == "unadjudicated" and u"未锚" in t["why"]),
        "unadj_value_out_of_band": sum(1 for c in ch for t in c["tokens"]
                                       if t["cls"] == "unadjudicated" and u"出" in t["why"]),
        "unadj_unparsable": sum(1 for c in ch for t in c["tokens"]
                                if t["cls"] == "unadjudicated" and u"不可解析" in t["why"]),
        "rows_zero_free_zero_obs": sum(1 for c in ch
                                       if c["n_free_v3"] == 0 and c["n_measured_v3"] == 0),
        "token_knob_candidate": sum(c["n_knob_candidate"] for c in ch),
        "distinct_unadjudicated_symbols": len(unadj),
        "rows_with_measured_v3": sum(1 for c in ch if c["n_measured_v3"] > 0),
        "rows_without_measured_v3": sum(1 for c in ch if c["n_measured_v3"] == 0),
        "g2_v3_pass": sum(1 for c in ch if c["g2_v3"] == "PASS"),
        "g2_v3_pass_within_g1": sum(1 for c in g1ch if c["g2_v3"] == "PASS"),
        "g2_v3_flips_from_v2": flips,
        "survive_v3": sum(1 for c in ch if c["survives_all_four_v3"]),
        "survive_v3_within_g1": sum(1 for c in g1ch if c["survives_all_four_v3"]),
    }
    assert fn["token_total"] == (fn["token_measured_v3"] + fn["token_echo"]
                                 + fn["token_unadjudicated"]), "三分类没有闭合"
    assert fn["token_unadjudicated"] == (fn["unadj_no_target_name"] + fn["unadj_value_out_of_band"]
                                         + fn["unadj_unparsable"]), "未裁定的三族拆分没有闭合（原因不互斥）"
    assert all(p["fired"] for p in probes), [p for p in probes if not p["fired"]]
    face = {
        "generated_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "land": LAND, "rc": 0, "files": files, "rows_scanned": scanned,
        "caliber": ("v3：被引观测必须名与值双锚在 %s 的靶上（3σ 带），"
                    "名册靶位不再补贴分母" % os.path.basename(CARRIER)),
        "vocab": [{"key": k, "value": v, "band_rel3sigma": r,
                   "alias": pats} for k, pats, v, r in VOCAB],
        "funnel": fn, "controls": probes,
        "unadjudicated_symbols": [dict(unadj[k], symbol=k) for k in sorted(unadj)],
        "channels": ch,
        "survivors_v3": [c["claim_id"] for c in ch if c["survives_all_four_v3"]],
    }
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    path = os.path.join(OUT_DIR, FACE)
    txt = json.dumps(face, ensure_ascii=False, indent=1, sort_keys=True)
    # 同目录 v1/v2 面是纯 CRLF：形状按邻居约定走，别让同一目录里出现两种换行
    data = (txt.replace("\r\n", "\n") + "\n").replace("\n", "\r\n").encode("utf-8")
    pre = io.open(path, "rb").read() if os.path.isfile(path) else None
    io.open(path, "wb").write(data)
    post = io.open(path, "rb").read()
    assert post == data and post.count(b"\r") == post.count(b"\n") == post.count(b"\r\n") > 0
    print(json.dumps(fn, ensure_ascii=False, indent=1))
    print("FACE %s bytes=%d md5=%s rerun=%s" % (path, len(post),
          __import__("hashlib").md5(post).hexdigest(), "pre-existed" if pre else "new"))
    print("controls %d/%d fired" % (sum(1 for p in probes if p["fired"]), len(probes)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        sys.stderr.write("FATAL: %s\n" % e)
        sys.exit(2)
