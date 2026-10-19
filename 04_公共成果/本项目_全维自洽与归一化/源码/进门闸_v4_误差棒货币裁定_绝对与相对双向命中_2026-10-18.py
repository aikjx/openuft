# -*- coding: utf-8 -*-
"""进门闸 v4：误差棒的**货币**裁定（绝对 vs 相对），命中判定用观测载体自己的 hit_test。

治理侧把 `prediction_urel` 声明为「无量纲靶的预测值 + **相对**不确定度」
（见 `源码/靶场登记列校验_写入侧门禁.py`、`源码/claims_登记列语义修复.py`），
下游 `无量纲靶场审计.py` 的 `hit_test(pred, obs, urel)` 也确实按相对用：
`|pred/obs - 1| <= 3*urel`。
但语料这一列实际写的是：`±0.002（两实现离散）`（绝对）、`±20%（文献跨度）`（百分数）、
`实现级 <±0.0005`（不等式）、空。同一串数字在两种货币下差 |pv| 倍（pv≈0.23 时差约 26 倍），
所以「落不落在自己的带里」这个判决会随货币翻面。

本仪器不自己发明判据：命中一律交给载体的 `hit_test`，我只是把同一行喂两次
（A＝按声明的相对货币原样吃数字；B＝按拼写的绝对/百分数货币换算成相对），
再逐枚点名判决翻面的行。判决不许猜形状：形状分类器按语料实际拼写建，
残差（无法归一化的写法）逐枚点名并要求闭合求和。
"""
from __future__ import print_function

import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
PROJP = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
V3NAME = "进门闸_无量纲具名靶候选通道普查_v3_符号级观测裁定_2026-10-18.py"
CARRIER = os.path.join(SRC, "无量纲靶场审计.py")
FACE = "进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.json"
LAND = "--land" in sys.argv[1:]
OUT_DIR = DATA if LAND else os.path.join(ROOT, "scratch")


class Fatal(Exception):
    pass


def load(name, path):
    if not os.path.isfile(path):
        raise Fatal("依赖文件不在盘：%s" % path)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V3 = load("intake_v4_v3", os.path.join(SRC, V3NAME))
CAR = load("intake_v4_carrier", CARRIER)

NUM = re.compile(r"[-+]?[0-9][0-9.eE-]*")
VOCAB_SHAPES = set(["empty", "percent", "pm_abs", "ineq_abs", "ineq_bare",
                    "bare_number", "prose_only"])


def read_band(u):
    """Return (shape, numeral or None). 形状按语料实际拼写枚举，不放宽成「有个数就行」。"""
    s = (u or "").strip()
    if not s:
        return "empty", None
    has_pct = "%" in s
    pm = u"±" in s or "+/-" in s or u"正负" in s
    ineq = bool(re.search(r"[<>≤≥]", s))
    m = NUM.search(s.replace(",", ""))
    if not m:
        return "prose_only", None
    try:
        val = float(m.group(0))
    except ValueError:
        return "prose_only", None
    if has_pct:
        return "percent", val
    if ineq and pm:
        return "ineq_abs", val
    if pm:
        return "pm_abs", val
    if ineq:
        return "ineq_bare", val
    return "bare_number", val


def targets_of(c):
    """该行点名且有实测值的名册靶（值与不确定度都从载体取）。"""
    out = []
    for key in c["g1_named_targets"]:
        v = TG.get(key)
        if v is not None:
            out.append(key)
    return out


TG = {}
for t in CAR.build_targets():
    if t["value"] is not None:
        try:
            TG[t["key"]] = (float(t["value"]), float(t["urel"]))
        except (TypeError, ValueError):
            pass
if not TG:
    raise Fatal("观测载体一条带值的靶也没给出——空词表上不许判命中")


def price(c):
    pv_raw = (c["prediction_value"] or "").strip()
    try:
        pv = float(pv_raw) if re.fullmatch(r"[-+0-9.eE/]+", pv_raw) else None
        if pv is None and "/" in pv_raw:
            a, b = pv_raw.split("/", 1)
            pv = float(a) / float(b)
    except (ValueError, ZeroDivisionError):
        pv = None
    shape, num = read_band(c.get("prediction_urel"))
    rows = []
    if pv is None:
        return {"shape": shape, "band_numeral": num, "targets": [], "pv": None,
                "verdict": "NO_NUMERIC_OUTPUT"}
    for key in targets_of(c):
        obs, ourel = TG[key]
        # A 货币：按治理声明「相对不确定度」原样吃这串数字
        ua = num if num is not None else None
        # B 货币：按拼写把它换回相对
        if num is None:
            ub = None
        elif shape == "percent":
            ub = num / 100.0
        elif shape in ("pm_abs", "ineq_abs"):
            ub = abs(num) / abs(pv) if pv else None
        else:
            ub = num
        va = "NO_BAND" if ua is None else ("HIT" if CAR.hit_test(pv, obs, ua) else "MISS")
        vb = "NO_BAND" if ub is None else ("HIT" if CAR.hit_test(pv, obs, ub) else "MISS")
        rows.append({"key": key, "obs": obs, "obs_urel": ourel,
                     "urel_A": ua, "urel_B": ub, "A": va, "B": vb,
                     "dev_rel": abs(pv / obs - 1.0) if obs else None,
                     "bandwidths_A": (abs(pv / obs - 1.0) / (3.0 * ua)) if (ua and obs) else None,
                     "bandwidths_B": (abs(pv / obs - 1.0) / (3.0 * ub)) if (ub and obs) else None})
    flips = [r for r in rows if r["A"] != r["B"]]
    return {"shape": shape, "band_numeral": num, "pv": pv, "targets": rows,
            "n_flip": len(flips),
            "verdict": ("FLIP" if flips else
                        (rows[0]["A"] if rows else "NO_NAMED_TARGET_WITH_VALUE"))}


def fixtures():
    def mk(cid, targets, pv, urel):
        return {"claim_id": cid, "prediction_value": pv, "prediction_urel": urel,
                "g1_named_targets": targets}
    f = [mk("B1", ["sin2_thetaW"], "0.2289", u"±0.002（两实现离散）"),
         mk("B2", ["sin2_thetaW"], "0.2289", "0.002"),
         mk("B3", ["alpha"], "0.0218920577279", u"±20%（文献跨度）"),
         mk("B4", ["n_gen"], "3", ""),
         mk("B5", ["alpha_s"], "0.11795", u"实现级 <±0.0001"),
         mk("B6", ["n_gen"], "4", "0")]
    return f


def run_probes():
    out = []

    def fire(name, ok, detail):
        out.append({"name": name, "fired": bool(ok), "detail": detail})
    fx = dict((x["claim_id"], price(x)) for x in fixtures())
    t0 = dict((k, fx[k]["targets"][0]) for k in fx)
    fire("B1 同一行喂两种货币判决必须相反（相对 0.002 判 MISS、绝对 0.002 换算后判 HIT）",
         t0["B1"]["A"] == "MISS" and t0["B1"]["B"] == "HIT", fx["B1"]["targets"])
    fire("B2 只改拼写（去掉 ±）必须落回声明货币、与 B1 的 A 同判（证明分叉来自形状不是数值）",
         fx["B2"]["verdict"] == t0["B1"]["A"], (fx["B2"]["targets"], t0["B1"]["A"]))
    fire("B3 `±20%` 按相对原样吃是 20（=6000% 带，错三倍也判 HIT），换算后 0.20 必须判 MISS",
         fx["B3"]["targets"][0]["A"] == "HIT" and fx["B3"]["targets"][0]["B"] == "MISS"
         and abs(fx["B3"]["targets"][0]["urel_B"] - 0.20) < 1e-12,
         fx["B3"]["targets"])
    fire("B4 带为空必须 NO_BAND（拒绝判决），不许自动当命中",
         fx["B4"]["verdict"] == "NO_BAND", fx["B4"]["targets"])
    fire("B5 不等式绝对写法必须识别为 ineq_abs 并按绝对换算（A 判 MISS、B 判 HIT）",
         fx["B5"]["shape"] == "ineq_abs" and fx["B5"]["n_flip"] == 1
         and fx["B5"]["targets"][0]["A"] == "MISS" and fx["B5"]["targets"][0]["B"] == "HIT",
         (fx["B5"]["shape"], fx["B5"]["targets"]))
    fire("B6 整数靶精确声明 urel=0：错值必须 MISS 且两种货币同判（不是形状游戏）",
         t0["B6"]["A"] == "MISS" and fx["B6"]["n_flip"] == 0, fx["B6"]["targets"])
    fire("B7 夹具必须各用一种形状（pm_abs/bare_number/percent/ineq_abs/empty 五档互不相同）",
         len(set([fx["B1"]["shape"], fx["B2"]["shape"], fx["B3"]["shape"],
                  fx["B5"]["shape"], fx["B6"]["shape"], fx["B4"]["shape"]])) == 5
         and fx["B4"]["shape"] == "empty",
         dict((k, fx[k]["shape"]) for k in sorted(fx)))
    return out


def main():
    rt = V3.V2.roster()
    ch = []
    files = 0
    scanned = 0
    for sysname, path in V3.V2.scope():
        files += 1
        for row in V3.V2.cells(sysname, path):
            scanned += 1
            if not (row.get("prediction_value") or "").strip():
                continue
            row["_sys"] = sysname
            c = dict(V3.V2.price(row, rt))
            c["system"] = sysname
            c["claim_id"] = row["claim_id"].strip()
            c["prediction_urel"] = (row.get("prediction_urel") or "").strip()
            c["status"] = (row.get("status") or "").strip()
            c["priced"] = price(c)
            ch.append(c)
    if not ch:
        raise Fatal("声明通道为 0（扫描 %d 行）——判集塌空时不许出判决" % scanned)
    shapes = {}
    for c in ch:
        shapes.setdefault(c["priced"]["shape"], []).append(c["claim_id"])
    allflips = []
    for c in ch:
        for r in c["priced"]["targets"]:
            if r["A"] != r["B"]:
                allflips.append({"claim_id": c["claim_id"], "system": c["system"],
                                 "key": r["key"], "urel_spelling": c["prediction_urel"][:34],
                                 "shape": c["priced"]["shape"], "pv": r and c["priced"]["pv"],
                                 "obs": r["obs"], "A": r["A"], "B": r["B"],
                                 "dev_rel": r["dev_rel"], "bw_A": r["bandwidths_A"],
                                 "bw_B": r["bandwidths_B"]})
    verdicts = {}
    for c in ch:
        verdicts.setdefault(c["priced"]["verdict"], []).append(c["claim_id"])
    probes = run_probes()
    n_target_rows = sum(len(c["priced"]["targets"]) for c in ch)
    fn = {"declared_channels": len(ch),
          "rows_scanned": scanned,
          "channels_with_named_target_value": len(verdicts.get("HIT", []))
                                            + len(verdicts.get("MISS", []))
                                            + len(verdicts.get("FLIP", [])),
          "channel_target_pairs": n_target_rows,
          "pairs_flip_by_currency": len(allflips),
          "pairs_A_HIT_B_MISS": sum(1 for f in allflips
                                   if f["A"] == "HIT" and f["B"] == "MISS"),
          "pairs_A_MISS_B_HIT": sum(1 for f in allflips
                                    if f["A"] == "MISS" and f["B"] == "HIT"),
          "verdict_counts": dict((k, len(v)) for k, v in verdicts.items()),
          "shape_counts": dict((k, len(v)) for k, v in shapes.items()),
          "shapes_absent_from_corpus": sorted(VOCAB_SHAPES - set(shapes)),
          "verified_rows_flip": [f["claim_id"] for f in allflips
                                 if [c for c in ch if c["claim_id"] == f["claim_id"]][0]
                                 ["status"].lower().startswith("verif")]}
    assert sum(fn["shape_counts"].values()) == len(ch), "形状分类没有闭合"
    assert set(shapes) <= VOCAB_SHAPES, sorted(set(shapes) - VOCAB_SHAPES)
    assert fn["pairs_A_HIT_B_MISS"] + fn["pairs_A_MISS_B_HIT"] == fn["pairs_flip_by_currency"]
    assert fn["channels_with_named_target_value"] + len(verdicts.get("NO_NAMED_TARGET_WITH_VALUE", [])) \
        + len(verdicts.get("NO_NUMERIC_OUTPUT", [])) == len(ch), "通道级判决没有闭合"
    assert fn["pairs_flip_by_currency"] == len(allflips)
    assert all(p["fired"] for p in probes), [p for p in probes if not p["fired"]]
    face = {"generated_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "land": LAND, "rc": 0, "files": files, "rows_scanned": scanned,
            "carrier": os.path.relpath(CARRIER, ROOT).replace("\\", "/"),
            "currency_A": "按治理声明把 prediction_urel 当**相对**不确定度原样吃",
            "currency_B": "按该行拼写（±x 绝对、x%% 百分数、<±x 不等式）换算成相对",
            "funnel": fn, "controls": probes,
            "flips": allflips,
            "channels": [{"claim_id": c["claim_id"], "system": c["system"],
                          "status": c["status"], "pv": c["prediction_value"],
                          "urel": c["prediction_urel"], "priced": c["priced"]}
                         for c in ch]}
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    path = os.path.join(OUT_DIR, FACE)
    txt = json.dumps(face, ensure_ascii=False, indent=1, sort_keys=True)
    data = (txt.replace("\r\n", "\n") + "\n").replace("\n", "\r\n").encode("utf-8")
    io.open(path, "wb").write(data)
    post = io.open(path, "rb").read()
    assert post == data and post.count(b"\r") == post.count(b"\n") == post.count(b"\r\n") > 0
    print(json.dumps(fn, ensure_ascii=False, indent=1))
    print("FACE %s bytes=%d md5=%s" % (path, len(post),
          __import__("hashlib").md5(post).hexdigest()))
    print("controls %d/%d fired" % (sum(1 for p in probes if p["fired"]), len(probes)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        sys.stderr.write("FATAL: %s\n" % e)
        sys.exit(2)
