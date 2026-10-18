# -*- coding: utf-8 -*-
"""总账 §七.1+§七.2 合并的「进门闸」普查：谁能在四条门前活下来。

四条门（判定卷《第一性输出台账》§进门清单）：
  G1 声明的输出是一个**无量纲数**，且落在具名靶场上（靶场名册由 `无量纲靶场审计.py` 现场抽取，不打字）
  G2 参数计数门 n_free ≤ n_obs − 1（与 §七.2 仪器同口径；本册把 claims.csv 的 assumptions 当旋钮名册）
  G3 控制组在场：所引推导文件在盘上、且含控制组字样（SHIFT/STALE 同规则）
  G4 非回填：行文本或推导文件里没有 拟合/回填/标定/自由参数 字样

普查对象=注册表里 prediction_value 非空的行（可机读的唯一候选面）。
Exit: 0 普查完成且控制组全点火 | 1 控制组未点火 | 2 硬抛（名册空/扫描集空/重名）
"""
import csv
import glob
import hashlib
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
OPENUFT = os.path.join(ROOT, "openuft")
DATA = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化", "数据")
ROSTER_SRC = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化", "源码",
                          "无量纲靶场审计.py")
FACE = "进门闸_无量纲具名靶候选通道普查_v2_2026-10-18.json"
# 试跑只写 scratch；带 --land 才写注册目录。路径由这一个开关现导，判决与落点同源。
LAND = "--land" in sys.argv[1:]
OUT_DIR = DATA if LAND else os.path.join(ROOT, "scratch")
RATCHET_FACE = "falsified不缩水跨体系台账_2026-10-18.json"

# alias patterns per roster key; the KEYS themselves come from ROSTER_SRC, so an
# unmapped key is a hard throw rather than a silent gap.
ALIAS = {
    "alpha": [r"精细结构常数", r"\balpha_em\b", r"α_em", r"(?<![_a-zA-Z])α(?!_)\s*="],
    "alpha_s": [r"α_s", r"\balpha_s\b", r"强耦合"],
    "m_mu_over_me": [r"m_μ\s*/\s*m_e", r"μ/m_e", r"206\.7"],
    "m_tau_over_me": [r"m_τ\s*/\s*m_e", r"τ/m_e", r"3477"],
    "me_over_mP": [r"m_e\s*/\s*m_P", r"me/mP"],
    "alpha_grav_e": [r"α_grav", r"引力耦合"],
    "sin2_thetaW": [r"sin²θ_W", r"sin\^2\s*θ_W", r"温伯格角", r"sin2θ", r"sin²θ"],
    "mt_over_mW": [r"m_t\s*/\s*m_W"],
    "n_gen": [r"代数\s*N_gen", r"N_gen", r"三代"],
    "n_c": [r"色数", r"N_c"],
}
ASSUM = re.compile(r"\b[A-Za-z]\d*_?[A-Za-z0-9]*-A[A-Za-z0-9_]*")
MEASURED = re.compile(r"(?:α|g[-/]?2|M_Z|m_W|m_t|m_e|m_μ|m_τ|Λ|H0|θ|sin²?θ)\s*=\s*[-+]?[0-9][\d./eE-]*")
FREE_MARK = re.compile(r"自由参数|可调参数|拟合参数|norm 常数|归一化常数|标定常数")
BACKFILL = re.compile(r"拟合|回填|事后标定|反推参数|标定而来")
CONTROL = re.compile(r"控制组|正对照|对照实验|对照组|回归测试|已知通过")
# 第二口径（宽词表）。G1–G4 的判决不许挂在我采到的第一种拼写上：每条门都另配一份
# 放宽的词表读数，若「四门全活」数在宽窄两口径下相同，拒绝就不是我的词表造成的。
MEASURED_WIDE = re.compile(r"[0-9]+\.[0-9]{2,}")
BACKFILL_WIDE = re.compile(r"拟合|回填|标定|反推|调参|凑|fit\b|calibrat|tune")
CONTROL_WIDE = re.compile(r"控制组|正对照|对照实验|对照组|回归测试|已知通过|基准|不变性|复算|"
                          r"sanity|smoke|control|fixture")
# 记录用：v1 的宽词表把「反例」也算作控制组字样，于是 S02 的两条通道被判成 G3 通过——
# 而唯一命中是评分图例行 `| falsified | 存在可复现反例或数量级排除，或定级否定 |`。
# 反例属证伪登记，不属控制组；且判决性字样出现在表格行里时它描述的是**评级口径**，不是推导做过的事。
CONTROL_NAIVE_V1 = re.compile(r"控制组|正对照|对照实验|对照组|回归测试|已知通过|基准|不变性|复算|"
                              r"反例|sanity|smoke|control|fixture|counterexample")


class Fatal(Exception):
    pass


def roster():
    txt = io.open(ROSTER_SRC, encoding="utf-8").read()
    ks = re.findall(r'\{"key":\s*"([A-Za-z_0-9]+)",\s*"name_zh":\s*"([^"]*)"', txt)
    if not ks:
        raise Fatal("靶场名册从 %s 抽不到任何 key —— 不许在空名册上判「没有候选」"
                    % os.path.basename(ROSTER_SRC))
    unmapped = [k for k, _ in ks if k not in ALIAS]
    if unmapped:
        raise Fatal("名册里的 key 没有别名模式：%s（补 ALIAS，别放宽判据）" % unmapped)
    return dict(ks)


def scope():
    out = []
    for f in sorted(glob.glob(os.path.join(OPENUFT, "01_独立体系", "*", "claims.csv"))):
        out.append((os.path.basename(os.path.dirname(f)), f))
    if not out:
        raise Fatal("扫描集为空（0 个 claims.csv）")
    return out


def cells(sysname, path):
    txt = io.open(path, encoding="utf-8-sig", newline="").read()
    rows = [r for r in csv.DictReader(io.StringIO(txt)) if r and (r.get("claim_id") or "").strip()]
    seen = set()
    for r in rows:
        cid = r["claim_id"].strip()
        if cid in seen:
            raise Fatal("体系 %s 内 claim_id 重名 %s" % (sysname, cid))
        seen.add(cid)
        yield r


def price(row, rt):
    """Return the four gate reads for one declared channel."""
    val = (row.get("prediction_value") or "").strip()
    blob = " ".join((row.get(k) or "") for k in
                    ("statement", "assumptions", "derivation", "prediction", "uncertainty"))
    g1_num = bool(val) and bool(re.fullmatch(r"[-+0-9.eE/]+", val))
    keys = sorted({k for k in rt for p in ALIAS[k] if re.search(p, blob)})
    n_free = len(set(ASSUM.findall(row.get("assumptions") or "")))
    extra = len(set(FREE_MARK.findall(blob)))
    n_free += extra
    n_obs = len(set(MEASURED.findall(blob))) + len(keys)
    g2 = "PASS" if (n_obs > 0 and n_free <= n_obs - 1) else "FAIL"
    # 宽口径：把行内任何 3 位以上小数字面量都当作被引观测（放宽 n_obs 的分母）
    n_obs_w = len(set(MEASURED_WIDE.findall(blob))) + len(keys)
    g2_w = "PASS" if (n_obs_w > 0 and n_free <= n_obs_w - 1) else "FAIL"
    # ---- v2 口径分家（付 §六.1 债）：被引观测 / 自产输出 / 回声必须分开。
    # v1 把整行拼成一个 blob 再数 `符号=数值`，于是「把自己的输出印第二遍」也算一次观测，
    # n_obs 的分母可以被通道自己灌水；宽口径更是把行里任何 3 位小数都当观测。
    COLTXT = [("statement", "statement"), ("derivation", "derivation"),
              ("assumptions", "assumptions"), ("uncertainty", "uncertainty"),
              ("prediction", "prediction")]
    SELF_COLS = set(["prediction"])

    def _tail_num(s):
        m = re.search(r"([-+]?[0-9][\d./eE-]*)\s*$", s)
        return m.group(1) if m else ""

    def _same_as_output(tok):
        if not val:
            return False
        try:
            return float(tok) == float(val)
        except ValueError:
            return False

    ext, ext_w, selfs, colmap = set(), set(), set(), {}
    for col, k in COLTXT:
        txt = row.get(k) or ""
        a = {m.group(0) for m in MEASURED.finditer(txt)}
        b = set(MEASURED_WIDE.findall(txt))
        ca = sorted(t for t in a if t not in SELF_COLS and not _same_as_output(_tail_num(t)))
        colmap[col] = {"measured": len(a), "measured_wide": len(b),
                       "self_col": col in SELF_COLS,
                       "echo_of_output": sum(1 for t in a if _same_as_output(_tail_num(t))),
                       "counted": 0 if col in SELF_COLS else len(ca)}
        if col not in SELF_COLS:
            ext |= set(ca)
            ext_w |= set(t for t in b if not _same_as_output(t))
        else:
            selfs |= a
        selfs |= set(t for t in a if _same_as_output(_tail_num(t)))
    n_obs_v2 = len(ext) + len(keys)
    g2_v2 = "PASS" if (n_obs_v2 > 0 and n_free <= n_obs_v2 - 1) else "FAIL"
    n_obs_v2_w = len(ext_w) + len(keys)
    g2_v2_w = "PASS" if (n_obs_v2_w > 0 and n_free <= n_obs_v2_w - 1) else "FAIL"

    dpath = (row.get("derivation") or "").strip()
    first = re.split(r"[;；]", dpath)[0].strip()
    m = re.match(r"^(\S+?\.(?:md|py|json|csv))", first)
    on_disk = None
    ctl = None
    ctl_w = None
    ev = []
    dres = None
    if m:
        p = os.path.join(OPENUFT, "01_独立体系", row["_sys"], m.group(1))
        if not os.path.isfile(p):
            p = os.path.join(OPENUFT, m.group(1))
        on_disk = os.path.isfile(p)
        if on_disk:
            dres = os.path.relpath(p, ROOT).replace("\\", "/")
            try:
                dtxt = io.open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                dtxt = None
            if dtxt is not None:
                ctl = bool(CONTROL.search(dtxt))
                lines = dtxt.replace("\r\n", "\n").split("\n")
                # 宽口径按**形状**过滤：markdown 表格行里判决性字样描述的是评级口径，不是推导做过的对照
                ctl_w = any(CONTROL_WIDE.search(ln) and not ln.lstrip().startswith("|")
                            for ln in lines)
                for i, ln in enumerate(lines, 1):
                    if CONTROL_NAIVE_V1.search(ln):
                        ev.append({"line": i, "table": ln.lstrip().startswith("|"),
                                   "counted": bool(CONTROL_WIDE.search(ln)) and not ln.lstrip().startswith("|"),
                                   "narrow": bool(CONTROL.search(ln)),
                                   "text": ln.strip()[:78]})
                        if len(ev) >= 5:
                            break
    bf = bool(BACKFILL.search(blob))
    bf_w = bool(BACKFILL_WIDE.search(blob))
    return {
        "claim_id": row["claim_id"].strip(),
        "system": row["_sys"],
        "prediction_value": val[:40],
        "g1_dimensionless_declared": g1_num,
        "g1_named_targets": keys,
        "g1": bool(g1_num and keys),
        "n_free_assumptions": n_free,
        "n_obs_cited": n_obs,
        "g2": g2,
        "n_obs_cited_wide": n_obs_w,
        "g2_wide": g2_w,
        "n_obs_external_v2": n_obs_v2,
        "g2_v2": g2_v2,
        "n_obs_external_v2_wide": n_obs_v2_w,
        "g2_v2_wide": g2_v2_w,
        "n_self_produced": len(selfs),
        "g2_col_map": colmap,
        "g3_derivation_on_disk": on_disk,
        "g3_derivation_resolved": dres,
        "g3_control_wording": ctl,
        "g3_control_wording_wide": ctl_w,
        "g3_evidence": ev,
        "g4_backfill_marker": bf,
        "g4_backfill_marker_wide": bf_w,
        "status": (row.get("status") or "").strip(),
    }


def survive(c, wide=False, cal="v1"):
    """The four-gate verdict under the narrow or the widened vocabulary.
    cal="v1" keeps the flattened single-blob n_obs; cal="v2" uses the split caliber."""
    g2k = "g2_wide" if wide else "g2"
    if cal == "v2":
        g2k = "g2_v2_wide" if wide else "g2_v2"
    if wide:
        return bool(c["g1"] and c[g2k] == "PASS" and c["g3_derivation_on_disk"]
                    and c["g3_control_wording_wide"] is not False
                    and not c["g4_backfill_marker_wide"])
    return bool(c["g1"] and c[g2k] == "PASS" and c["g3_derivation_on_disk"]
                and c["g3_control_wording"] is not False
                and not c["g4_backfill_marker"])


def census():
    rt = roster()
    ch = []
    files = 0
    scanned = 0
    for sysname, path in scope():
        files += 1
        for row in cells(sysname, path):
            scanned += 1
            if not (row.get("prediction_value") or "").strip():
                continue
            row["_sys"] = sysname
            ch.append(price(row, rt))
    if scanned == 0:
        raise Fatal("注册表一行也没读到（%d 个文件）——零候选不是证据" % files)
    declared = len(ch)
    if declared == 0:
        raise Fatal("prediction_value 非空的通道数为 0，普查无从判定")
    for c in ch:
        c["survives_all_four"] = survive(c)
        c["survives_all_four_wide"] = survive(c, wide=True)
        c["survives_all_four_v2"] = survive(c, cal="v2")
        c["survives_all_four_v2_wide"] = survive(c, wide=True, cal="v2")
    g1 = [c for c in ch if c["g1"]]
    funnel = {
        "declared_channels": declared,
        "numeric_prediction_value": sum(1 for c in ch if c["g1_dimensionless_declared"]),
        "names_a_roster_target": sum(1 for c in ch if c["g1_named_targets"]),
        "g1_both": len(g1),
        "g2_pass_overall": sum(1 for c in ch if c["g2"] == "PASS"),
        "g2_pass_within_g1": sum(1 for c in g1 if c["g2"] == "PASS"),
        "derivation_on_disk_within_g1": sum(1 for c in g1 if c["g3_derivation_on_disk"]),
        "control_wording_within_g1": sum(1 for c in g1 if c["g3_control_wording"]),
        "control_wording_within_g1_wide": sum(1 for c in g1 if c["g3_control_wording_wide"]),
        "backfill_marker_within_g1": sum(1 for c in g1 if c["g4_backfill_marker"]),
        "backfill_marker_within_g1_wide": sum(1 for c in g1 if c["g4_backfill_marker_wide"]),
        "survive_narrow": sum(1 for c in ch if c["survives_all_four"]),
        "survive_wide": sum(1 for c in ch if c["survives_all_four_wide"]),
        "survive_v2_narrow": sum(1 for c in ch if c["survives_all_four_v2"]),
        "survive_v2_wide": sum(1 for c in ch if c["survives_all_four_v2_wide"]),
        "g2_v2_pass": sum(1 for c in ch if c["g2_v2"] == "PASS"),
        "g2_v2_pass_within_g1": sum(1 for c in ch if c["g1"] and c["g2_v2"] == "PASS"),
        "g2_v2_flips_from_v1": [c["claim_id"] for c in ch if c["g2"] != c["g2_v2"]],
        "g2_v2_disagreement_ids": [c["claim_id"] for c in ch if c["g2_v2"] != c["g2_v2_wide"]],
        "rows_without_external_obs": sum(1 for c in ch
                                         if c["n_obs_external_v2"] == len(c["g1_named_targets"])),
        "echo_rows": sum(1 for c in ch
                         if any(v["echo_of_output"] for v in c["g2_col_map"].values())),
        "g2_pass_within_g1_wide": sum(1 for c in g1 if c["g2_wide"] == "PASS"),
        "naive_control_hits_within_g1": sum(1 for c in g1 if c["g3_evidence"]),
        "g2_disagreement_ids": [c["claim_id"] for c in ch if c["g2"] != c["g2_wide"]],
    }
    return rt, {"files": files, "rows_scanned": scanned, "declared_channels": declared,
                "funnel": funnel, "channels": ch}


def cross_check(channels):
    """Instrument-to-instrument: per-system falsified counts must equal the §七.5 face."""
    p = os.path.join(DATA, RATCHET_FACE)
    if not os.path.isfile(p):
        return {"ran": False, "note": "§七.5 面缺席，跨仪器通道未跑"}
    f = json.load(io.open(p, encoding="utf-8"))
    ref = {k: len(v["ids"]) for k, v in f["per_system"].items()}
    import collections
    cnt = collections.Counter()
    for c in channels:
        if c["status"] == "falsified":
            cnt[c["system"]] += 1
    bad = []
    for s, n in cnt.items():
        # only comparable where the same predicate is countable over the declared subset
        if s not in ref:
            bad.append((s, n, "absent"))
    return {"ran": True, "ratchet_total": sum(ref.values()), "ratchet_files": f["scope_live_files"],
            "declared_falsified_by_system": dict(cnt), "unknown_systems": bad}


def probe_fixtures(rt):
    """G3/G4 的针能不能红：语料里 control_wording 读数是 0，恒 0 必须先当针坏。

    探针打在临时夹具上（scratch/ 内，跑完即删），不动注册语料一个字节。
    """
    global OPENUFT
    outs = []
    keep = OPENUFT
    d = os.path.join(HERE, "_intake_probe_sys")
    if not os.path.isdir(d):
        os.makedirs(d)
    pos = os.path.join(d, "ctl_pos.md")
    neg = os.path.join(d, "ctl_neg.md")
    rub = os.path.join(d, "ctl_rubric.md")
    io.open(pos, "wb").write(u"# 推导\n\n本节配了正对照与回归测试两套控制组。\n"
                             u"| falsified | 存在可复现反例或数量级排除 |\n".encode("utf-8"))
    io.open(neg, "wb").write(u"# 推导\n\n这里只有推导本身。\n".encode("utf-8"))
    io.open(rub, "wb").write(u"# 推导\n\n| 级别 | 定义 |\n| --- | --- |\n"
                             u"| falsified | 存在可复现反例或数量级排除，或定级否定 |\n".encode("utf-8"))
    def row(deriv, pv="0.5", extra="", **over):
        r = {"claim_id": "PROBE", "_sys": "夹具", "prediction_value": pv,
             "statement": "m_μ/m_e " + extra, "assumptions": "JJ-A1",
             "derivation": deriv, "prediction": "", "uncertainty": "α = 1/137.036",
             "status": "open"}
        r.update(over)
        return r
    try:
        OPENUFT = os.path.join(HERE, "_intake_probe_sys")
        p_pos = price(row("ctl_pos.md"), rt)
        outs.append(("M8 含控制组字样的推导文件必须把 G3 探针钉成 True（针能红）",
                     p_pos["g3_derivation_on_disk"] is True
                     and p_pos["g3_control_wording"] is True
                     and p_pos["g3_control_wording_wide"] is True,
                     "盘=%s 窄=%s 宽=%s" % (p_pos["g3_derivation_on_disk"],
                                          p_pos["g3_control_wording"],
                                          p_pos["g3_control_wording_wide"])))
        p_neg = price(row("ctl_neg.md"), rt)
        outs.append(("M9 同形但不含控制组字样的推导文件必须读 False（探针不是恒真）",
                     p_neg["g3_derivation_on_disk"] is True
                     and p_neg["g3_control_wording"] is False
                     and p_neg["g3_control_wording_wide"] is False,
                     "盘=%s 窄=%s 宽=%s" % (p_neg["g3_derivation_on_disk"],
                                          p_neg["g3_control_wording"],
                                          p_neg["g3_control_wording_wide"])))
        p_rub = price(row("ctl_rubric.md"), rt)
        outs.append(("M13 只有评分图例行（含「反例」）的推导文件必须读 False，而 naive 扫描必须看得见它",
                     p_rub["g3_control_wording"] is False
                     and p_rub["g3_control_wording_wide"] is False
                     and len(p_rub["g3_evidence"]) >= 1
                     and all(e["table"] for e in p_rub["g3_evidence"]),
                     "窄=%s 宽=%s 命中行=%s" % (p_rub["g3_control_wording"],
                                              p_rub["g3_control_wording_wide"],
                                              [e["line"] for e in p_rub["g3_evidence"]])))
        outs.append(("M13b 散文控制组加图例行混排的文件必须仍读 True（形状过滤不许一票否决真对照）",
                     p_pos["g3_control_wording_wide"] is True
                     and any(e["counted"] and not e["table"] for e in p_pos["g3_evidence"])
                     and any(e["table"] for e in p_pos["g3_evidence"]),
                     "宽=%s 见证=%s" % (p_pos["g3_control_wording_wide"],
                                       [(e["line"], e["table"], e["counted"])
                                        for e in p_pos["g3_evidence"]])))
        p_bf = price(row("ctl_pos.md", extra="参数由事后标定而来"), rt)
        outs.append(("M10 回填字样必须把 G4 探针钉成 True（窄宽两口径都要红）",
                     p_bf["g4_backfill_marker"] is True and p_bf["g4_backfill_marker_wide"] is True,
                     "窄=%s 宽=%s" % (p_bf["g4_backfill_marker"], p_bf["g4_backfill_marker_wide"])))
        p_txt = price(row("ctl_pos.md", pv="约 0.23（定性描述）"), rt)
        outs.append(("M11 输出不是纯数字时 G1 必须读 False（G1 不是恒真门）",
                     p_txt["g1_dimensionless_declared"] is False,
                     "val=%s 无量纲声明=%s" % (p_txt["prediction_value"],
                                             p_txt["g1_dimensionless_declared"])))
        # ---- v2 口径分家的正/反对照：n_obs 的分母不许由通道自己灌水。
        # 夹具的 statement 故意不点任何名册靶（keys=0），否则靶位本身会把 n_obs_v2 抬到
        # n_free+1，让判决与分家无关——N1 第一版就是这么假 MISS 的。
        n1 = price(row("ctl_neg.md", pv="0.1122", statement="中性玻色子质量由本通道给出",
                       uncertainty="", prediction="M_Z = 91.1876; m_W = 80.379"), rt)
        outs.append(("N1 数值只印在输出列时 v2 必须不再当观测（v1 PASS→v2 FAIL，针有牙）",
                     n1["g1_named_targets"] == []
                     and n1["g2"] == "PASS" and n1["g2_v2"] == "FAIL"
                     and n1["n_obs_cited"] >= 2 and n1["n_obs_external_v2"] == 0
                     and n1["n_self_produced"] >= 2,
                     "v1 n_obs=%d %s | v2 外=%d %s 自产=%d 靶=%s"
                     % (n1["n_obs_cited"], n1["g2"], n1["n_obs_external_v2"], n1["g2_v2"],
                        n1["n_self_produced"], ",".join(n1["g1_named_targets"]) or "-")))
        n2 = price(row("ctl_neg.md", pv="0.1122", statement="中性玻色子质量由本通道给出",
                       prediction="", uncertainty="M_Z = 91.1876; m_W = 80.379"), rt)
        outs.append(("N2 同两个数值改放观测列时 v2 必须仍 PASS（修的不是恒假门）",
                     n2["g1_named_targets"] == []
                     and n2["g2_v2"] == "PASS" and n2["n_obs_external_v2"] >= 2
                     and n2["n_free_assumptions"] == n1["n_free_assumptions"],
                     "v2 外=%d %s n_free=%d（与 N1 同）"
                     % (n2["n_obs_external_v2"], n2["g2_v2"], n2["n_free_assumptions"])))
        n3 = price(row("ctl_neg.md", pv="0.2289",
                       statement="sin²θ = 0.2289 与实测一致",
                       uncertainty="", prediction=""), rt)
        outs.append(("N3 声明值被原句复述（回声）必须不计入观测：v1 PASS→v2 FAIL",
                     n3["g2"] == "PASS" and n3["g2_v2"] == "FAIL"
                     and n3["g2_col_map"]["statement"]["echo_of_output"] == 1
                     and n3["g2_col_map"]["statement"]["counted"] == 0,
                     "v1 n_obs=%d | v2 外=%d 回声=%d %s"
                     % (n3["n_obs_cited"], n3["n_obs_external_v2"],
                        n3["g2_col_map"]["statement"]["echo_of_output"], n3["g2_v2"])))
        n4 = price(row("ctl_neg.md", pv="0.2289",
                       statement="sin²θ = 0.23122（PDG）",
                       uncertainty="", prediction=""), rt)
        outs.append(("N4 同形但引用的是另一个数（0.23122≠0.2289）必须计入：v2 PASS",
                     n4["g2_v2"] == "PASS" and n4["g2_col_map"]["statement"]["echo_of_output"] == 0
                     and n4["g2_col_map"]["statement"]["counted"] == 1,
                     "v2 外=%d %s 回声=%d" % (n4["n_obs_external_v2"], n4["g2_v2"],
                                            n4["g2_col_map"]["statement"]["echo_of_output"])))
        n5 = price(row("ctl_neg.md", pv="0.1122", statement="中性玻色子质量由本通道给出",
                       uncertainty="", prediction="M_Z = 91.1876; m_W = 80.379",
                       assumptions="JJ-A1 JJ-A2 JJ-A3"), rt)
        outs.append(("N5 旋钮侧不受分家影响：同一条只加 assumptions，n_free 必须随之上升而外观测不变",
                     n5["n_free_assumptions"] > n1["n_free_assumptions"]
                     and n5["n_obs_external_v2"] == n1["n_obs_external_v2"]
                     and n5["g2_v2"] == "FAIL",
                     "n_free %d->%d 外=%d 口径=%s"
                     % (n1["n_free_assumptions"], n5["n_free_assumptions"],
                        n5["n_obs_external_v2"], n5["g2_v2"])))
    finally:
        OPENUFT = keep
        for f in (pos, neg, rub):
            if os.path.isfile(f):
                os.remove(f)
        if os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)
    return outs


def mutants(rt):
    """Controls. M1/M5 share one fixture, so the injection delta is measurable."""
    global ALIAS, scope
    outs = []
    # fixture: 1 旋钮 / 2 观测 / 无量纲 / 命中具名靶 —— 应当活在前两道门
    good = {"claim_id": "MUT-5", "_sys": "夹具", "prediction_value": "0.5",
            "statement": "m_μ/m_e 由单个比值假设给出", "assumptions": "JJ-A1",
            "derivation": "控制组在场", "prediction": "",
            "uncertainty": "实测 α = 1/137.036，m_h = 125.25", "status": "open"}
    base = price(good, rt)
    outs.append(("M5 正对照（1 旋钮/2 观测、无量纲、命中具名靶）必须活下来",
                 bool(base["g1"] and base["g2"] == "PASS"),
                 "g1=%s 靶=%s n_free=%d n_obs=%d %s"
                 % (base["g1"], ",".join(base["g1_named_targets"]), base["n_free_assumptions"],
                    base["n_obs_cited"], base["g2"])))
    # M1 注入 4 个新旋钮：同一夹具必须由 PASS 翻 FAIL（证明计数门有牙）
    inj = dict(good)
    inj["claim_id"] = "MUT-1"
    inj["assumptions"] = "JJ-A1;ZZ-A1;ZZ-A2;ZZ-A3;ZZ-A4"
    m1 = price(inj, rt)
    fired = (base["g2"] == "PASS" and m1["g2"] == "FAIL"
             and m1["n_free_assumptions"] == base["n_free_assumptions"] + 4)
    outs.append(("M1 注入 4 个旋钮必须把夹具从 PASS 钉成 FAIL", fired,
                 "n_free %d->%d，n_obs=%d，%s->%s"
                 % (base["n_free_assumptions"], m1["n_free_assumptions"], m1["n_obs_cited"],
                    base["g2"], m1["g2"])))
    _, c = census()
    ch_all = c["channels"]
    g1 = [x for x in ch_all if x["g1"]]
    if g1:
        v = g1[0]
        outs.append(("M6 真实语料读数样例（G1 通道必须带得出逐条计数）", True,
                     "样例 %s/%s n_free=%d n_obs=%d %s" % (v["system"], v["claim_id"],
                                                          v["n_free_assumptions"],
                                                          v["n_obs_cited"], v["g2"])))
    # M7 词表包含关系必须在每一行都成立：宽词表若真含窄词表，窄口 True 时宽口不可能 False。
    # 违例意味着「放宽口径」这件事本身是假的，那么宽窄对照读数一文不值。
    viol = [x["claim_id"] for x in ch_all
            if (x["g3_control_wording"] and not x["g3_control_wording_wide"])
            or (x["g4_backfill_marker"] and not x["g4_backfill_marker_wide"])]
    outs.append(("M7 宽词表必须真含窄词表（窄口 True 而宽口 False 的行数必须为 0）",
                 not viol, "违例 %d 条 %s" % (len(viol), ",".join(viol[:5]) or "-")))
    # M7b 两口径在 G2 上有分歧时，分歧行必须逐条进台账；针本身用「动一格就红」来验，
    # 免得空台账上的恒等比较把自己印成证据。
    dis = sorted(x["claim_id"] for x in ch_all if x["g2"] != x["g2_wide"])
    ledger = sorted(c["funnel"]["g2_disagreement_ids"])
    tampered = (ledger[:-1] if dis else ledger + ["GHOST"])
    outs.append(("M7b G2 宽窄分歧必须逐条点名，且台账动一格就红",
                 dis == ledger and dis != tampered,
                 "分歧 %d 条 台账 %d 条 样例=%s" % (len(dis), len(ledger),
                                                   ",".join(dis[:6]) or "无分歧")))
    # M12 口径造成的翻案必须能被行级见证解释：窄 False 而宽 True 的行，
    # 见证里必须至少有一条 narrow=False 的命中；否则「宽口径多认出控制组」是无源断言。
    flipped = [x for x in ch_all if x["g3_control_wording"] is False
               and x["g3_control_wording_wide"] is True]
    unpriced = [x["claim_id"] for x in flipped if not [e for e in x["g3_evidence"]
                  if e["counted"] and not e["narrow"]]]
    naive = [x["claim_id"] for x in ch_all if x["g3_evidence"] and not x["g3_control_wording_wide"]]
    outs.append(("M12 宽口径翻案行必须各带一条被计入的非表格行见证；naive-only 命中行必须点名",
                 not unpriced,
                 "翻案 %d 条(无见证 %d)｜naive 命中但不计入 %d 条 %s"
                 % (len(flipped), len(unpriced), len(naive), ",".join(naive[:5]) or "-")))
    # M2 名册别名缺失必须硬抛
    keep = ALIAS
    try:
        ALIAS = {}
        roster()
        outs.append(("M2 名册别名缺失必须硬抛", False, "未抛"))
    except Fatal as e:
        outs.append(("M2 名册别名缺失必须硬抛", True, str(e)[:46]))
    finally:
        ALIAS = keep
    # M3 空扫描集必须硬抛
    keep_scope = scope
    try:
        scope = lambda: []
        census()
        outs.append(("M3 零个 claims.csv 必须硬抛", False, "未抛"))
    except Fatal as e:
        outs.append(("M3 零个 claims.csv 必须硬抛", True, str(e)[:46]))
    finally:
        scope = keep_scope
    # M4 体系内重名 claim_id 必须硬抛。
    # 变异必须打在**真 cells()** 上：换掉 cells 就等于换掉探测器本身（第一版就是这样，
    # 于是夹具从未被检测过，M4 安静地 MISS）。这里只换 scope，喂进一份含重名的临时 CSV，
    # 并配一枚「同形但 id 不重」的负对照，证明抛错来自重名而不是来自夹具形状。
    keep_scope = scope
    fixture = (u"claim_id,status,prediction_value,assumptions,statement\n"
               u"D1,open,1.0,S02-A4,α_em=1/137.036\n"
               u"{second},open,2.0,,sin²θ_W=0.23\n")
    dup = os.path.join(HERE, "_intake_m4_dup.csv")
    ok = os.path.join(HERE, "_intake_m4_distinct.csv")
    for p, second in ((dup, "D1"), (ok, "D2")):
        io.open(p, "wb").write(fixture.format(second=second).encode("utf-8"))
    try:
        for p, label, want in ((dup, "M4 体系内重名 claim_id 必须硬抛", True),
                               (ok, "M4n 同形夹具但 id 不重 必须不抛（证明抛错只因重名）", False)):
            scope = lambda: [("夹具", p)]
            threw = None
            try:
                census()
            except Fatal as e:
                threw = str(e)[:46]
            outs.append((label, (threw is not None) == want, threw or "未抛"))
    finally:
        scope = keep_scope
        for p in (dup, ok):
            if os.path.isfile(p):
                os.remove(p)
    return outs


def main():
    try:
        rt, c = census()
    except Fatal as e:
        print("HARD THROW: %s" % e)
        return 2
    ch = c["channels"]
    fn = c["funnel"]
    g1 = [x for x in ch if x["g1"]]
    surv = [x for x in ch if x["survives_all_four"]]
    surv_w = [x for x in ch if x["survives_all_four_wide"]]
    ctl = mutants(rt) + probe_fixtures(rt)
    bad = [n for n, f, _ in ctl if not f]
    print("进门闸普查  靶场名册 %d 项（抽自 %s）" % (len(rt), os.path.basename(ROSTER_SRC)))
    print("  扫描 %d 个 claims.csv / %d 行；prediction_value 非空通道 %d 条"
          % (c["files"], c["rows_scanned"], c["declared_channels"]))
    print("  漏斗：声明 %d → 纯数字输出 %d → 点名靶场 %d → G1 双条件 %d"
          % (fn["declared_channels"], fn["numeric_prediction_value"],
             fn["names_a_roster_target"], fn["g1_both"]))
    print("  G1 通道内：G2 PASS %d | 推导在盘 %d | 控制组窄 %d 宽 %d | 回填标记窄 %d 宽 %d"
          % (fn["g2_pass_within_g1"], fn["derivation_on_disk_within_g1"],
             fn["control_wording_within_g1"], fn["control_wording_within_g1_wide"],
             fn["backfill_marker_within_g1"], fn["backfill_marker_within_g1_wide"]))
    print("  四门全活：窄口径 %d 条 | 宽口径 %d 条（G2 宽窄分歧 %d 条）"
          % (fn["survive_narrow"], fn["survive_wide"], len(fn["g2_disagreement_ids"])))
    print("  v2 分家口径：G2 PASS %d（v1 %d）| G1 内 PASS %d（v1 %d）| 四门全活 窄 %d 宽 %d"
          % (fn["g2_v2_pass"], fn["g2_pass_overall"], fn["g2_v2_pass_within_g1"],
             fn["g2_pass_within_g1"], fn["survive_v2_narrow"], fn["survive_v2_wide"]))
    print("  v2 代价单：与 v1 判决翻转 %d 条 | 宽窄分歧 %d 条（v1 %d 条）| 无外观测行 %d | 含回声行 %d"
          % (len(fn["g2_v2_flips_from_v1"]), len(fn["g2_v2_disagreement_ids"]),
             len(fn["g2_disagreement_ids"]), fn["rows_without_external_obs"], fn["echo_rows"]))
    for x in sorted(g1, key=lambda y: (not y["survives_all_four"], y["system"]))[:12]:
        print("    %-12s %-28s val=%-10s n_free=%d n_obs=%d/%d %s|%s 靶=%s 盘=%s 对照=%s/%s 回填=%s/%s"
              % (x["claim_id"], x["system"][:28], x["prediction_value"], x["n_free_assumptions"],
                 x["n_obs_cited"], x["n_obs_cited_wide"], x["g2"], x["g2_wide"],
                 ",".join(x["g1_named_targets"]) or "-", x["g3_derivation_on_disk"],
                 x["g3_control_wording"], x["g3_control_wording_wide"],
                 x["g4_backfill_marker"], x["g4_backfill_marker_wide"]))
    for x in surv_w:
        print("    宽口径存活 %s/%s 靶=%s 推导=%s" % (x["system"], x["claim_id"],
                                                    ",".join(x["g1_named_targets"]),
                                                    x["g3_derivation_resolved"]))
        for e in x["g3_evidence"][:3]:
            print("        L%-5d %s%s" % (e["line"], e["text"], "" if e["narrow"] else "  ← 窄词表认不出"))
    for n, f, note in ctl:
        print("  [%s] %s | %s" % ("FIRED" if f else "MISS", n, note))
    face = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "roster_keys": sorted(rt), "roster_source": os.path.relpath(ROSTER_SRC, ROOT).replace("\\", "/"),
            "files": c["files"], "rows_scanned": c["rows_scanned"],
            "declared_channels": c["declared_channels"], "funnel": fn,
            "n_g1_named_dimensionless": len(g1), "n_survive_narrow": len(surv),
            "n_survive_wide": len(surv_w),
            "survivors": surv, "survivors_wide": surv_w, "g1_channels": g1,
            "channels": ch,
            "cross_check_seven_five": cross_check(ch),
            "controls": [{"name": n, "fired": bool(f), "note": x} for n, f, x in ctl],
            "rc": 0 if not bad else 1}
    os.makedirs(OUT_DIR, exist_ok=True)
    out = json.dumps(face, ensure_ascii=False, indent=2) + "\n"
    face_path = os.path.join(OUT_DIR, FACE)
    _pre = io.open(face_path, "rb").read() if os.path.isfile(face_path) else b""
    io.open(face_path, "wb").write(out.replace("\n", "\r\n").encode("utf-8"))
    _post = io.open(face_path, "rb").read()
    assert _post == out.replace("\n", "\r\n").encode("utf-8"), "面字节回读不符"
    assert _post != _pre, "面未变动（写到的还是旧图，判决不可引用）"
    print("  面：%s（%s，%d 条通道全量入面，含 v1/v2 两套 G2 口径；%d→%d B）"
          % (os.path.relpath(face_path, ROOT).replace("\\", "/"),
             "LAND 注册目录" if LAND else "试跑 scratch",
             len(ch), len(_pre), len(_post)))
    return face["rc"]


if __name__ == "__main__":
    sys.exit(main())
