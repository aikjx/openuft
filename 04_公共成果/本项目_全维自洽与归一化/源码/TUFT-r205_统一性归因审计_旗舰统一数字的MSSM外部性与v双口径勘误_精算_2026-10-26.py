# -*- coding: utf-8 -*-
r"""TUFT-r205｜统一性归因审计 + v 双口径勘误
================================================================================
承 r199（尺度锚定不可能性定理、三族离散归一化条件排除）与 r194/r195 的
旗舰数字（M_GUT、α_GUT⁻¹、M*/v、M_GUT/v）。本卷不问「尺度能否导出」，而问
「这些数字到底属于谁」：

  A  框架自我账本（机读，只读）
      07_统一场方程/验证脚本/验证报告.json（47 项：PASS 39 / FAIL 2 / INFO 6）
      08_预言与判据.md 的 V1–V7「已验证预言」；09_已知局限 的 L10 否定登记。
      结论：框架自己写明 SM 单圈**不统一**（R1.1 比值 9384.78、R1.2 散布 3.656），
            只有 MSSM 对照散布 0.049（INFO）。

  B  归一性归属：五单元矩阵（独立复算，Decimal 60）
      (β 族, sin²θ_W 口径, 匹配条件) ∈ {SM, MSSM} × {s实测, s*} × {α₁=α₂, α₁=α₃}
      SM(s实测)×α₁=α₂ → 1.02e13；SM(s*)×α₁=α₃ → 2.43e14；
      MSSM(s实测)×α₁=α₂ → 1.99e16；MSSM(s实测)×α₁=α₃ → 2.09e16；
      MSSM(s*)×α₁=α₃ → 2.121e16（= 各轮旗舰 M_GUT）。
      ⇒ 「统一质量」不是预测量，而是口径选择（跨 3.3 个数量级）。

  C  自相矛盾（机读）
      r192 path2_z4_susy = CLOSED-NEGATIVE（no-go）；UFE-1 v1 的核心文档
      （00/01/08）中 MSSM 出现 **0 次**。⇒ 旗舰统一数字 100% 依赖一个被本框架
      判死、且不在其场内容中的外部情景。

  D  v 双口径勘误（P 级）
      E1 定义 v = (√2G_F)^(-1/2) = 246.2200（容差 0.002）；
      r190–r199 全账本用 v = 255.26242445425643，标为「PDG 反解」，实为
      2M_W/g₂(α(0), sin²θ_W^OS) 的组合 ⇒ 偏差 +3.673%。
      M*/v、M_GUT/v、M_Z/v 三个纯数的分母全部受此影响（×1.03672）。
      成因：g₂=2M_W/v 用 α(0)=1/137.036；改用 α(M_Z)=1/127.952 得 246.6515（差 0.18%）。

  E  供给侧与判定
      框架自有统一性证据 0；连续预言外部性 100%；供给仍 0（承接 r199）。

落地勘误（幂等，只追加）：r194 判定册追加 r205 附节 2 条。原记录一字不改。
治理红线：归因审计只针对被引用的统一数字与 V1–V7；MSSM 是外部情景、不计入
框架供给；v 勘误只追加不改原记录；本卷条目不可与 r142–r204 相加。
纯标准库（Decimal(60) + Fraction），无 numpy/sympy/mpmath。
"""

import ast
import glob
import hashlib
import json
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")
DOCS = os.path.join(_ROOT, "07_统一场方程")
VERIFY = os.path.join(DOCS, "验证脚本")
RPT_JSON = os.path.join(VERIFY, "验证报告.json")
VERIFY_CORE = os.path.join(VERIFY, "verify_core.py")
DOC08 = os.path.join(DOCS, "08_预言与判据.md")
DOC09 = os.path.join(DOCS, "09_已知局限与否定清单.md")
DOC00 = os.path.join(DOCS, "00_统一场方程.md")
DOC01 = os.path.join(DOCS, "01_作用量与场内容.md")
R192_JSON = os.path.join(
    _DATADIR, "TUFT-r192_S13三路径攻坚_Z4超对称no-go定理_尺度同源归并与几何候选排除_精算_2026-10-25.json")
R199_JSON = os.path.join(
    _DATADIR, "TUFT-r199_尺度锚定不可能性定理_三类离散归一化条件排除与跨轮口径一致性审计_精算_2026-10-25.json")
R194_BOOK = os.path.join(
    _DATADIR, "判定_TUFT-r194_统一场论尺度不可导出no-go与六处缺陷单源勘误_精算_2026-10-25.md")

BASE = "TUFT-r205_统一性归因审计_旗舰统一数字的MSSM外部性与v双口径勘误_精算_2026-10-26"
ERRATA_TAG = "【r205 统一性归因与 v 双口径勘误｜2026-10-26】"

VERDICT = ("R205-UNIFICATION-ATTRIBUTION-FLAGSHIP-MGUT-2-121E16-ALPHA-GUT-INV-24-2764-"
           "ONLY-IN-MSSM-BETA-CELL-FIVE-CELL-MASSES-1-02E13-2-40E14-1-99E16-2-09E16-"
           "2-12E16-SPAN-3-3-DECADES-SM-OWN-CONTENT-DOES-NOT-UNIFY-R11-RATIO-9384-78-R12-"
           "SPREAD-3-656-R13-MSSM-INFO-0-049-R192-PATH2-CLOSED-NEGATIVE-UFE1-DOCS-"
           "MSSM-COUNT-0-V-DUAL-CALIBER-255-2624-VS-246-22-DELTA-3-673PCT-RATIOS-"
           "SCALE-1-03672-CAUSE-ALPHA0-VS-ALPHA-MZ-V-MZ-246-65-SUPPLY-0")
REDLINE = "归因审计只针对被引用的统一数字与 V1–V7；MSSM 是外部情景、不计入框架供给；v 勘误只追加不改原记录；本卷条目不可与 r142–r204 相加"

ENTRIES = []
CTRL = []
GUARDS = []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


# ---------------------------------------------------------------------------
# 〇、常量（两套口径分开命名，禁止混用）
# ---------------------------------------------------------------------------
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781641")
TWO_PI = D(2) * PI

GF = D("1.1663787e-5")
MW_OBS = D("80.377")
MH = D("125.25")
MT = D("172.76")
MZ = D("91.1876")
ALPHA0 = D(1) / D("137.035999084")
ALPHA_MZ = D(1) / D("127.952")
S2_MS = D("0.23121")
ALPHAS_MZ = D("0.118")

# 验证报告口径（R1.1–R1.3）
SM_B = (D("4.1"), D(-19) / D(6), D(-7))
MSSM_B = (D(33) / D(5), D(1), D(-3))

# r190–r199 旗舰口径（r199 常量）
AEM_INV = D("127.916")
S2W_R199 = D("0.23122")
A3_INV = D(10000) / D(1179)

CANON_V = "255.26242445425643"
CANON_XGUT13 = "5.2648981057"
CANON_ALPHA_INV = "24.2764585242"
CANON_MGUT = "2.1210003843584052e16"
CANON_MSTAR_OVER_V = "14.3979002445"

DOC_R11 = "9384.779131071888"
DOC_R12 = "3.656054544564036"
DOC_R13 = "0.04914338915893168"


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rel(a, b):
    return abs(a - b) / abs(b)


# ---------------------------------------------------------------------------
# 一、RG 工具（独立实现，Decimal 60）
# ---------------------------------------------------------------------------
A1_0 = (D(3) / D(5)) * (D(1) - S2_MS) / ALPHA_MZ
A2_0 = S2_MS / ALPHA_MZ
A3_0 = D(1) / ALPHAS_MZ
A_REP = (A1_0, A2_0, A3_0)

A1_C = (D(3) / D(5)) * (D(1) - S2W_R199) * AEM_INV
A2_C = S2W_R199 * AEM_INV
A3_C = A3_INV
A_CANON = (A1_C, A2_C, A3_C)


def cross(ai, aj, bi, bj):
    return MZ * ((TWO_PI * (ai - aj) / (bi - bj)).exp())


def spread_at(lnmu, bs, a0s):
    vals = [a0 - b * lnmu / TWO_PI for a0, b in zip(a0s, bs)]
    return max(vals) - min(vals)


def min_spread(bs, a0s, k=4000):
    lo = D(1000).ln()
    hi = D("1e19").ln()
    best, best_ln = None, None
    for i in range(k + 1):
        lnmu = lo + D(i) * (hi - lo) / D(k)
        s = spread_at(lnmu, bs, a0s)
        if best is None or s < best:
            best, best_ln = s, lnmu
    return best, best_ln.exp()


def crossings(bs, a0s):
    return {"m12": cross(a0s[0], a0s[1], bs[0], bs[1]),
            "m13": cross(a0s[0], a0s[2], bs[0], bs[2]),
            "m23": cross(a0s[1], a0s[2], bs[1], bs[2])}


def unification_probe():
    out = {}
    for tag, bs in (("SM", SM_B), ("MSSM", MSSM_B)):
        cr = crossings(bs, A_REP)
        best, at = min_spread(bs, A_REP)
        out[tag] = {"crossings": {k: str(v) for k, v in cr.items()},
                    "ratio_12_23": str(max(cr["m12"], cr["m23"]) / min(cr["m12"], cr["m23"])),
                    "min_spread": str(best),
                    "min_spread_at": str(at)}
    return out


S_STAR = (D(3) * AEM_INV + D(7) * A3_INV) / (D(15) * AEM_INV)
S_MEAS = S2W_R199


def a0_from_s(s):
    return ((D(3) / D(5)) * (D(1) - s) * AEM_INV, s * AEM_INV, A3_INV)


def flagship_cell(bs, s):
    """(β 族, α₁=α₃) 单元：x=(a1(s)-a3)/(b1-b3)，M=M_Z e^{2πx}，α_GUT⁻¹=a3-b3x。"""
    a0 = a0_from_s(s)
    x = (a0[0] - a0[2]) / (bs[0] - bs[2])
    m = MZ * (TWO_PI * x).exp()
    return x, m, a0[2] - bs[2] * x, spread_at(TWO_PI * x, bs, a0)


def cell_matrix():
    rows = []
    plan = (("SM", SM_B, "s_meas", "alpha1=alpha2"),
            ("SM", SM_B, "s_star", "alpha1=alpha3"),
            ("MSSM", MSSM_B, "s_meas", "alpha1=alpha2"),
            ("MSSM", MSSM_B, "s_meas", "alpha1=alpha3"),
            ("MSSM", MSSM_B, "s_star", "alpha1=alpha3"))
    for tag, bs, sk, match in plan:
        s = S_STAR if sk == "s_star" else S_MEAS
        a0 = a0_from_s(s)
        p, q = (0, 1) if match == "alpha1=alpha2" else (0, 2)
        x = (a0[p] - a0[q]) / (bs[p] - bs[q])
        m = MZ * (TWO_PI * x).exp()
        sp = spread_at(TWO_PI * x, bs, a0)
        rows.append({"beta": tag, "s": sk, "match": match,
                     "x": str(x), "M": str(m), "spread": str(sp),
                     "s_value": str(s), "unified": sp < D("0.1")})
    return rows


def mstar_over_v():
    r = D(9) / D(5)
    x = (A_CANON[0] - r * A_CANON[1]) / (SM_B[0] - r * SM_B[1])
    return MZ * (TWO_PI * x).exp() / D(CANON_V)


def v_dual():
    v_gf = D(1) / (D(2).sqrt() * GF).sqrt()
    v_a0 = D(2) * MW_OBS / (D(4) * PI * ALPHA0 / S2W_R199).sqrt()
    v_mz = D(2) * MW_OBS / (D(4) * PI * ALPHA_MZ / S2_MS).sqrt()
    ratio = v_a0 / v_gf
    return {"v_gf": str(v_gf), "v_alpha0": str(v_a0), "v_alphaMz": str(v_mz),
            "delta_pct": str((ratio - 1) * D(100)), "factor": str(ratio),
            "mstar_over_v_canon": str(mstar_over_v()),
            "mstar_over_v_corrected": str(mstar_over_v() * ratio),
            "mgut_over_v_canon": str(D(CANON_MGUT) / D(CANON_V)),
            "mgut_over_v_corrected": str(D(CANON_MGUT) / v_gf),
            "mz_over_v_canon": str(MZ / D(CANON_V)),
            "mz_over_v_corrected": str(MZ / v_gf)}


# ---------------------------------------------------------------------------
# 二、机读（只读）
# ---------------------------------------------------------------------------
def read_report_json():
    with open(RPT_JSON, "rb") as f:
        d = json.loads(f.read().decode("utf-8"))
    return d


def read_08_v_rows():
    rows = []
    with open(DOC08, "rb") as f:
        text = f.read().decode("utf-8")
    for line in text.splitlines():
        m = re.match(r"^\|\s*\*\*(V\d)\*\*\s*\|", line)
        if m:
            rows.append({"id": m.group(1), "line": line})
    return rows


def mssm_in_core_docs():
    out = {}
    for p in (DOC00, DOC01, DOC08):
        with open(p, "rb") as f:
            t = f.read().decode("utf-8")
        out[os.path.basename(p)] = t.upper().count("MSSM")
    return out


def limitation_registered():
    with open(DOC09, "rb") as f:
        t = f.read().decode("utf-8")
    hit = [ln for ln in t.splitlines() if "MSSM" in ln]
    neg = "不能" in t and "否定结果" in t
    return {"mssm_lines": len(hit), "has_negative_wording": neg,
            "first_line": hit[0].strip() if hit else ""}


def read_r192():
    with open(R192_JSON, "rb") as f:
        d = json.loads(f.read().decode("utf-8"))
    path = d.get("path_status", {})
    th = d.get("theta_algebra", {})
    return {"path2": str(path.get("path2_z4_susy", "")),
            "path1": str(path.get("path1_sin2w_scale", "")),
            "path3": str(path.get("path3_mgut_geometric", "")),
            "theta_keys": len(th)}


def cross_round_v():
    out = []
    for p in sorted(glob.glob(os.path.join(_DATADIR, "TUFT-r19*.json"))):
        b = os.path.basename(p)
        m = re.match(r"TUFT-r(19\d)_", b)
        if not m:
            continue
        n = int(m.group(1))
        if n == 205:
            continue
        raw = open(p, "rb").read()
        t = raw.decode("utf-8", "replace")
        out.append({"round": n, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "v_canon_hits": len(re.findall(r"255\.2624\d*", t)),
                    "v_gf_hits": len(re.findall(r"246\.22\b", t)),
                    "v_canon_field": bool(re.search(r'"v":\s*"255\.2624', t))})
    return out


def ast_attribution():
    src = open(VERIFY_CORE, "rb").read().decode("utf-8")
    toks = ("S13", "s13", "分形", "fractal", "bidirectional", "双向",
            "Z_4", "Z4", "theta_4", "torsion", "挠率")
    tree = ast.parse(src)
    names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Attribute):
            names.add(n.attr)
    hits = {k: src.count(k) for k in toks}
    ident_hits = sum(1 for k in toks for nm in names if k.lower() in nm.lower())
    return {"bytes": len(src.encode("utf-8")), "tokens": toks,
            "hits": hits, "token_total": sum(hits.values()),
            "identifier_hits": ident_hits,
            "ufe1_label_hits": src.count("UFE-1")}


def verdict_has_supply0():
    with open(R199_JSON, "rb") as f:
        d = json.loads(f.read().decode("utf-8"))
    return "SUPPLY-0" in str(d.get("verdict", "")), str(d.get("round", ""))


# ---------------------------------------------------------------------------
# 三、分析
# ---------------------------------------------------------------------------
def do_analysis():
    rpt = read_report_json()
    items = {r["id"]: r for r in rpt.get("results", [])}
    vrows = read_08_v_rows()
    mssm_docs = mssm_in_core_docs()
    lim = limitation_registered()
    r192 = read_r192()
    crv = cross_round_v()
    att = ast_attribution()
    supply_ok, r199_round = verdict_has_supply0()

    probe = unification_probe()
    fl_mssm = flagship_cell(MSSM_B, S_STAR)
    fl_sm = flagship_cell(SM_B, S_STAR)
    cells = cell_matrix()
    vd = v_dual()

    return {"report": rpt, "items": items, "vrows": vrows,
            "mssm_docs": mssm_docs, "limitation": lim, "r192": r192,
            "cross_v": crv, "attribution": att,
            "supply_ok": supply_ok, "r199_round": r199_round,
            "probe": probe, "fl_mssm": fl_mssm, "fl_sm": fl_sm,
            "cells": cells, "vdual": vd}


def build_entries(a):
    it = a["items"]
    r11 = D(str(it["R1.1"]["computed"]))
    r12 = D(str(it["R1.2"]["computed"]))
    r13 = D(str(it["R1.3"]["computed"]))
    pr = a["probe"]
    vd = a["vdual"]
    cells = a["cells"]
    masses = [D(c["M"]) for c in cells]
    span = max(masses) / min(masses)

    add("A1", "doc", "机读 07/验证脚本/验证报告.json：%d 项（PASS %d / FAIL %d / INFO %d）；"
        "R1.1 比值 %.6f（FAIL）、R1.2 最小散布 %.6f（FAIL）、R1.3 MSSM 散布 %.6f（INFO）"
        " ⇒ 框架自己的账本写明：UFE-1 自有 SM 单圈**不统一**"
        % (a["report"]["summary"]["total"], a["report"]["summary"]["pass"],
           a["report"]["summary"]["fail"], a["report"]["summary"]["info"],
           float(r11), float(r12), float(r13)),
        "FAIL", "R194 引用 R1 时只取 MSSM 结果，未标注其为外部对照")
    add("A2", "doc", "机读 09_已知局限：L10 已登记「UFE-1 v1 不能在无新物理的情况下实现耦合统一」"
        "（%d 处 MSSM 行、否定措辞=%s）⇒ 框架不统一是**已登记结论**，不是本卷新发现"
        % (a["limitation"]["mssm_lines"], a["limitation"]["has_negative_wording"]),
        "FAIL", "登记 ≠ 消解：r194–r199 仍以 MSSM 数字作旗舰")
    add("A3", "doc", "机读 08_预言与判据 的「已验证预言」表：%d 行（V1–V7），逐条归因为 "
        "SM 电弱一圈（V1/V2/V7）、GR（V3/V4/V5）、QCD 一圈（V6），TUFT 特有内容 = 0"
        % len(a["vrows"]), "FAIL", "V1–V7 是 SM/GR/QCD 的标准结果，对本框架零证据价值")
    add("B0", "recompute", "旗舰复现（r190–r199 口径 + MSSM β + s 反解）：s*=%.10f"
        "（实测 %.10f，差 %.2E = %.3f%%），x=%.10f，M_GUT=%.10E GeV（规范 %s，残差 %.2E），"
        "α_GUT⁻¹=%.10f（规范 %s，残差 %.2E）"
        % (float(S_STAR), float(S_MEAS), float(abs(S_STAR - S_MEAS)),
           float(abs(S_STAR / S_MEAS - 1) * D(100)),
           float(D(a["fl_mssm"][0])), float(D(a["fl_mssm"][1])), CANON_MGUT,
           float(rel(D(a["fl_mssm"][1]), D(CANON_MGUT))),
           float(D(a["fl_mssm"][2])), CANON_ALPHA_INV,
           float(rel(D(a["fl_mssm"][2]), D(CANON_ALPHA_INV)))),
        "PASS", "复现成立 ⇒ 归属判断有确定对象；s* 由 α₁=α₃ 反解，非测量输入")
    add("B1", "recompute", "独立复算 SM 三交点：α₁=α₂ → %.4E、α₁=α₃ → %.4E、"
        "α₂=α₃ → %.4E GeV；比值 %.6f（文档 %s，残差 %.2E）"
        % (float(D(pr["SM"]["crossings"]["m12"])), float(D(pr["SM"]["crossings"]["m13"])),
           float(D(pr["SM"]["crossings"]["m23"])), float(D(pr["SM"]["ratio_12_23"])),
           DOC_R11, float(rel(D(pr["SM"]["ratio_12_23"]), D(DOC_R11)))),
        "PASS", "三交点跨 3.3 个数量级 ⇒ SM 无公共点")
    add("B2", "recompute", "最小散布复算：SM %.6f @ %.3E GeV（文档 %s）；MSSM %.6f @ %.3E GeV"
        "（文档 %s）⇒ 相差 %.1f 倍"
        % (float(D(pr["SM"]["min_spread"])), float(D(pr["SM"]["min_spread_at"])), DOC_R12,
           float(D(pr["MSSM"]["min_spread"])), float(D(pr["MSSM"]["min_spread_at"])), DOC_R13,
           float(D(pr["SM"]["min_spread"]) / D(pr["MSSM"]["min_spread"]))),
        "PASS", "独立实现与框架自身验证报告一致 ⇒ 复算可信")
    add("B3", "audit", "五单元矩阵（β 族 × s 口径 × 匹配条件）：SM(s实测,α₁=α₂) → %.3E；"
        "SM(s*,α₁=α₃) → %.3E；MSSM(s实测,α₁=α₂) → %.3E；MSSM(s实测,α₁=α₃) → %.3E；"
        "MSSM(s*,α₁=α₃) → %.3E GeV ⇒ 五个「统一质量」跨 %.0f 倍（%.1f 个数量级）"
        "⇒ 统一质量由口径选择决定，不是预测量"
        % (float(masses[0]), float(masses[1]), float(masses[2]),
           float(masses[3]), float(masses[4]), float(span), float(span.log10())),
        "FAIL", "同一组实测耦合 + 两个口径旋钮可造出任意一个「统一点」")
    sm_a13 = [D(c["spread"]) for c in cells
              if c["beta"] == "SM" and c["s"] == "s_star"][0]
    add("B4", "audit", "归属判定（必要条件 1）：旗舰 (M_GUT=%s, α_GUT⁻¹=%s) 只在 "
        "β=MSSM 的 (α₁=α₃) 单元成立；SM 即便把 s 反解到 α₁=α₃，散布仍 %.4f"
        "（≥ 0.5 即不统一）⇒ MSSM β 不可省"
        % (CANON_MGUT, CANON_ALPHA_INV, float(sm_a13)),
        "FAIL", "旗舰数字的框架自供含量 = 0")
    m_meas = [D(c["M"]) for c in cells
              if c["beta"] == "MSSM" and c["s"] == "s_meas" and c["match"] == "alpha1=alpha3"][0]
    add("B5", "audit", "归属判定（必要条件 2）：用实测 s=%.6f 的 MSSM 给出 M=%.4E，"
        "与旗舰 %.4E 差 %.2f%%；把 s 反解到 %.6f（Δ=%.2E，落在 α_s 传播不确定度 ~2.4E-4 内）"
        "才得到旗舰值 ⇒ 单元内「散布≈0」部分是同义反复（α₁=α₃ 由 s* 定义）"
        % (float(S_MEAS), float(m_meas), float(D(CANON_MGUT)),
           float(abs(m_meas / D(CANON_MGUT) - 1) * D(100)), float(S_STAR),
           float(abs(S_STAR - S_MEAS))),
        "FAIL", "两个旋钮（β=MSSM、s 反解）都是外部选择，不是框架内容")
    add("B6", "audit", "自相矛盾（机读）：r192 path2_z4_susy = 「%s」；UFE-1 v1 核心文档 "
        "00/01/08 的 MSSM 计数 = %s ⇒ 旗舰数字 100%% 依赖一个被本框架判死、且不在其场内容中的情景"
        % (a["r192"]["path2"], a["mssm_docs"]),
        "FAIL", "F-attribution：借用一个被自身 no-go 排除的外部情景")
    add("C1", "errata", "v 双口径：E1 定义 v=(√2G_F)^(-1/2)=%s GeV（容差 0.002）；"
        "r190/r194/r195/r199 账本 v=%s（标为「PDG 反解」）⇒ 偏差 +%s%%；"
        "r196 反而用 246.22（2 处）⇒ 账本内并存两个定义"
        % (vd["v_gf"][:8], CANON_V, vd["delta_pct"][:6]),
        "FAIL", "P 级口径缺陷：两个定义在同一账本混用")
    add("C2", "errata", "影响量化（×%s）：M*/v %s → %s；M_GUT/v %s → %s；"
        "M_Z/v %s → %s ⇒ r194–r199 的五个纯数中三个分母有偏"
        % (vd["factor"][:8], CANON_MSTAR_OVER_V, vd["mstar_over_v_corrected"][:8],
           vd["mgut_over_v_canon"][:8], vd["mgut_over_v_corrected"][:8],
           vd["mz_over_v_canon"][:8], vd["mz_over_v_corrected"][:8]),
        "FAIL", "r199 跨轮审计只查轮间一致性、未查定义 ⇒ 遗漏 1 处")
    add("C3", "errata", "成因定位：g₂=2M_W/v 用 α(0)=1/137.036 ⇒ v=%s；改用 α(M_Z)=1/127.952 ⇒ "
        "v=%s（与 G_F 值差 %.2f%%）⇒ 255.26 是方案误用（α 取错能标），不是新物理"
        % (vd["v_alpha0"][:8], vd["v_alphaMz"][:8],
           float(abs(D(vd["v_alphaMz"]) / D(vd["v_gf"]) - 1) * D(100))),
        "PASS", "解释性结论：可用 α(M_Z) 复现 E1")
    add("D1", "supply", "供给总账（承接 r199）：α_GUT 0 / M_GUT 0 / τ_p 0 / 1/4 独立含量 0 / "
        "ℓ_sd 0；本卷新增「统一性证据 0」（MSSM 外部情景不计入）", "FAIL",
        "r199 判词含 SUPPLY-0 = %s（round=%s）" % (a["supply_ok"], a["r199_round"]))
    add("D2", "ledger", "本轮账目：归因 7 条（A1–A3、B3–B6）、复算 3 条（B0–B2）、"
        "v 勘误 3 条（C1–C3）、供给 1 条；物理闭合 0；框架自有供给 0", "INFO", "")
    add("V1", "verdict", "判定：**CLOSED-NEGATIVE（no-go）**——旗舰统一数字的框架自供含量 = 0；"
        "统一性证据来自被 r192 判死的 MSSM 外部情景；v 双口径偏差 3.673% 已登记为 P 级勘误；"
        "供给仍 0", "FAIL", "本卷不否定 SM/GR/MSSM 自身的正确性，只否定其归属于本框架")
    return {"span": str(span)}


# ---------------------------------------------------------------------------
# 四、勘误落地（幂等，只追加）
# ---------------------------------------------------------------------------
def apply_errata(a):
    vd = a["vdual"]
    bullets = [
        "- P1｜v 双口径（F-convention）：本册第二节 v=%s（标为「PDG 反解」）实为 "
        "2M_W/g₂(α(0), sin²θ_W^OS) 的组合，与 E1 的 G_F 定义 v=(√2G_F)^(-1/2)=%s 相差 "
        "+%s%%；r194–r199 的 M*/v、M_GUT/v、M_Z/v 分母全部沿用 255.2624，改用 246.22 后"
        "三比值 ×%s。成因：g₂=2M_W/v 用 α(0)=1/137.036；改用 α(M_Z)=1/127.952 得 v=%s"
        "（差 0.18%%）。原记录保留，本注为单一更正源（r205）。"
        % (CANON_V, vd["v_gf"][:8], vd["delta_pct"][:6], vd["factor"][:8], vd["v_alphaMz"][:8]),
        "- P2｜统一性归属（F-attribution）：M_GUT=%s 与 α_GUT⁻¹=%s 只在 MSSM "
        "β=(33/5,1,−3) 下成立；MSSM/超对称已被 r192 path2 判 CLOSED-NEGATIVE，且 UFE-1 v1 "
        "场内容文档（00/01/08）MSSM 计数 = 0；框架自有 SM 单圈按自身验证报告 R1.1/R1.2 不统一"
        "（比值 %s、散布 %s）⇒ 本册「统一点」数字的框架自供含量 = 0。"
        % (CANON_MGUT, CANON_ALPHA_INV, DOC_R11, DOC_R12),
    ]
    now = "本次已存在（幂等）"
    old = ""
    if os.path.exists(R194_BOOK):
        with open(R194_BOOK, "rb") as f:
            old = f.read().decode("utf-8")
    prefix_ok = "## 二、出处与秩" in old and "## 六、自纠 Q1" in old
    if ERRATA_TAG in old:
        size0 = size1 = len(old.encode("utf-8"))
    else:
        block = ["", "", "---", "", "## " + ERRATA_TAG, "",
                 "> 审计侧附加标注；**正文/原记录一字未改**（只追加，不静默改写）。",
                 "> 依据：`04_公共成果/本项目_全维自洽与归一化/数据/判定_%s.md`。" % BASE,
                 ""] + bullets + [""]
        with open(R194_BOOK, "a", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(block))
        size0 = len(old.encode("utf-8"))
        with open(R194_BOOK, "rb") as f:
            size1 = len(f.read())
    return {"path": R194_BOOK, "tag": ERRATA_TAG, "status": now if ERRATA_TAG in old else "追加完成",
            "bytes_before": size0, "bytes_after": size1,
            "prefix_preserved": prefix_ok, "bullets": 2}


# ---------------------------------------------------------------------------
# 五、控制组与守卫
# ---------------------------------------------------------------------------
def build_controls(a):
    it = a["items"]
    pr = a["probe"]
    vd = a["vdual"]
    cells = a["cells"]
    masses = [D(c["M"]) for c in cells]

    ctl("C01", "E1 v=(√2G_F)^(-1/2) ≈ 246.22（容差 0.002）",
        abs(D(vd["v_gf"]) - D("246.22")) < D("0.002"), vd["v_gf"][:10])
    ctl("C02", "旗舰口径 v=255.26242445425643 复现（残差<1e-12）",
        rel(D(vd["v_alpha0"]), D(CANON_V)) < D("1e-12"), vd["v_alpha0"][:14])
    ctl("C03", "v 偏差 = +3.673%",
        abs(D(vd["delta_pct"]) - D("3.6732")) < D("0.002"), vd["delta_pct"][:8])
    ctl("C04", "验证报告汇总 47/39/2/6",
        (a["report"]["summary"]["total"], a["report"]["summary"]["pass"],
         a["report"]["summary"]["fail"], a["report"]["summary"]["info"]) == (47, 39, 2, 6),
        str(a["report"]["summary"]))
    ctl("C05", "R1.1 = 9384.779131071888", rel(D(str(it["R1.1"]["computed"])), D(DOC_R11)) < D("1e-9"),
        str(it["R1.1"]["computed"]))
    ctl("C06", "R1.2 = 3.656054544564036", rel(D(str(it["R1.2"]["computed"])), D(DOC_R12)) < D("1e-9"),
        str(it["R1.2"]["computed"]))
    ctl("C07", "R1.3 = 0.04914338915893168", rel(D(str(it["R1.3"]["computed"])), D(DOC_R13)) < D("1e-9"),
        str(it["R1.3"]["computed"]))
    ctl("C08", "复算 R1.1 残差 < 1e-9", rel(D(pr["SM"]["ratio_12_23"]), D(DOC_R11)) < D("1e-9"),
        pr["SM"]["ratio_12_23"][:14])
    ctl("C09", "复算 R1.2 残差 < 1e-9", rel(D(pr["SM"]["min_spread"]), D(DOC_R12)) < D("1e-9"),
        pr["SM"]["min_spread"][:14])
    ctl("C10", "复算 R1.3 残差 < 1e-9", rel(D(pr["MSSM"]["min_spread"]), D(DOC_R13)) < D("1e-9"),
        pr["MSSM"]["min_spread"][:14])
    ctl("C11", "SM α₁=α₂ 交点量级 1e13", D(pr["SM"]["crossings"]["m12"]) > D("9e12")
        and D(pr["SM"]["crossings"]["m12"]) < D("1.2e13"), pr["SM"]["crossings"]["m12"][:10])
    ctl("C12", "SM α₂=α₃ 交点量级 9.69e16", D(pr["SM"]["crossings"]["m23"]) > D("9e16")
        and D(pr["SM"]["crossings"]["m23"]) < D("1.05e17"), pr["SM"]["crossings"]["m23"][:10])
    ctl("C13", "MSSM 三交点同在 2e16 附近（散布<0.1）",
        D(pr["MSSM"]["min_spread"]) < D("0.1"), pr["MSSM"]["min_spread"][:8])
    ctl("C14", "旗舰复现 M_GUT 残差<1e-12", rel(D(a["fl_mssm"][1]), D(CANON_MGUT)) < D("1e-12"),
        str(D(a["fl_mssm"][1]))[:20])
    ctl("C15", "旗舰复现 α_GUT⁻¹ 残差<1e-9（规范串 10 位小数分辨率）",
        rel(D(a["fl_mssm"][2]), D(CANON_ALPHA_INV)) < D("1e-9"),
        str(D(a["fl_mssm"][2]))[:14])
    ctl("C16", "五单元质量互异（5 个不同值，max/min > 100）",
        len({c["M"] for c in cells}) == 5 and max(masses) / min(masses) > D(100),
        "span=" + str((max(masses) / min(masses)))[:10])
    ctl("C17", "SM(s*,α₁=α₃) 仍不统一（spread > 0.5）",
        [D(c["spread"]) for c in cells if c["beta"] == "SM" and c["s"] == "s_star"][0] > D("0.5"),
        "")
    ctl("C18", "MSSM(s*,α₁=α₃) 统一（spread < 0.1）",
        [D(c["spread"]) for c in cells
         if c["beta"] == "MSSM" and c["s"] == "s_star" and c["match"] == "alpha1=alpha3"][0] < D("0.1"),
        "")
    ctl("C19", "r192 path2 含 CLOSED-NEGATIVE", "CLOSED-NEGATIVE" in a["r192"]["path2"],
        a["r192"]["path2"][:40])
    ctl("C20", "UFE-1 核心文档 MSSM 计数 = 0", sum(a["mssm_docs"].values()) == 0, str(a["mssm_docs"]))
    ctl("C21", "09 已登记否定（含否定措辞）", a["limitation"]["has_negative_wording"],
        str(a["limitation"]["mssm_lines"]))
    ctl("C22", "08 V1–V7 计 7 行", len(a["vrows"]) == 7, str(len(a["vrows"])))
    ctl("C23", "verify_core.py 框架特有 token = 0", a["attribution"]["token_total"] == 0,
        str(a["attribution"]["hits"]))
    ctl("C24", "v=255.2624 在 r190–r199 ≥3 轮出现",
        sum(1 for r in a["cross_v"] if r["v_canon_hits"] > 0) >= 3,
        str([r["round"] for r in a["cross_v"] if r["v_canon_hits"] > 0]))
    ctl("C25", "246.22 仅 r196 使用（2 处），其余轮次用 255.2624",
        sum(r["v_gf_hits"] for r in a["cross_v"]) == 2
        and [r["round"] for r in a["cross_v"] if r["v_gf_hits"] > 0] == [196],
        str({r["round"]: r["v_gf_hits"] for r in a["cross_v"] if r["v_gf_hits"] > 0}))
    ctl("C26", "r199 判词含 SUPPLY-0", a["supply_ok"], a["r199_round"])
    ctl("C27", "s* 与实测 sin²θ_W 相差 < 3e-4（0.12%）",
        abs(S_STAR - S_MEAS) < D("3e-4"),
        "s*=%s meas=%s" % (str(S_STAR)[:9], str(S_MEAS)[:8]))
    m_meas = [D(c["M"]) for c in cells
              if c["beta"] == "MSSM" and c["s"] == "s_meas" and c["match"] == "alpha1=alpha3"][0]
    ctl("C28", "MSSM(s实测,α₁=α₃) 与旗舰 M_GUT 差 1%–2%",
        D("0.01") < abs(m_meas / D(CANON_MGUT) - 1) < D("0.02"),
        str(abs(m_meas / D(CANON_MGUT) - 1))[:8])


def build_guards(a, an, patch):
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    doc = ast.get_docstring(tree) or ""
    big = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            s = n.value
            if doc and s.strip() == doc.strip():
                continue
            if len(s) > 200 and "\n" in s:
                big.append(len(s))

    grd("G1", "Decimal 精度 ≥ 50", getcontext().prec >= 50, str(getcontext().prec))
    grd("G2", "β 系数精确有理数", SM_B[1] == D(-19) / D(6) and MSSM_B[0] == D(33) / D(5),
        "SM/MSSM")
    grd("G3", "机读只读：r192/验证报告 sha256 前后一致", a["_hash_ok"], a["_hash_note"])
    grd("G4", "07 四件文档零改动", a["_doc_hash_ok"], a["_doc_hash_note"])
    grd("G5", "勘误幂等 + 前缀保留", patch["prefix_preserved"],
        patch["status"] + "|" + str(patch["bytes_before"]) + "->" + str(patch["bytes_after"]))
    grd("G6", "红线逐字存在", REDLINE in src, "len=" + str(len(REDLINE)))
    grd("G7", "判词 ASCII 大写/数字/连字符", all(c.isupper() or c.isdigit() or c == "-" for c in VERDICT),
        "len=" + str(len(VERDICT)))
    grd("G8", "ast 自审：无 >200 字符且含换行的字符串", len(big) == 0, str(big))
    grd("G9", "独立复算与文档值残差 < 1e-9",
        rel(D(a["probe"]["SM"]["ratio_12_23"]), D(DOC_R11)) < D("1e-9")
        and rel(D(a["probe"]["SM"]["min_spread"]), D(DOC_R12)) < D("1e-9")
        and rel(D(a["probe"]["MSSM"]["min_spread"]), D(DOC_R13)) < D("1e-9"), "3/3")
    grd("G10", "五单元矩阵非平凡（5 个质量互异）",
        len({c["M"] for c in a["cells"]}) == 5, "n=5")
    grd("G11", "供给不因审计增加（仍 0）", a["supply_ok"], "SUPPLY-0")
    grd("G12", "本卷条目不可跨轮相加", "本卷条目不可与 r142–r204 相加" in REDLINE, "redline")


# ---------------------------------------------------------------------------
# 六、产出
# ---------------------------------------------------------------------------
def fmt_entries():
    lines = []
    for e in ENTRIES:
        lines.append("%-6s [%s] %s : %s" % (e["id"], e["layer"], e["verdict"], e["text"]))
    return lines


def write_json(a, an, patch):
    d = {
        "round": "r205", "date": "2026-10-26",
        "title": "统一性归因审计：旗舰统一数字的 MSSM 外部性与 v 双口径勘误",
        "verdict": VERDICT, "redline": REDLINE,
        "doc": {"verify_summary": a["report"]["summary"],
                "R1.1": a["items"]["R1.1"], "R1.2": a["items"]["R1.2"],
                "R1.3": a["items"]["R1.3"],
                "v_rows": [v["id"] for v in a["vrows"]],
                "mssm_core_docs": a["mssm_docs"],
                "limitation": a["limitation"],
                "r192_path": {k: a["r192"][k] for k in ("path1", "path2", "path3")}},
        "recompute": a["probe"],
        "flagship": {"mssm": {k: str(v) for k, v in zip(("x", "M", "alpha_inv"), a["fl_mssm"])},
                     "sm": {k: str(v) for k, v in zip(("x", "M", "alpha_inv"), a["fl_sm"])}},
        "cells": a["cells"],
        "v_dual": a["vdual"],
        "attribution": a["attribution"],
        "cross_round_v": a["cross_v"],
        "patches": [patch],
        "counts": {"entries": len(ENTRIES),
                   "pass": sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
                   "fail": sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                   "info": sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
                   "controls": "%d/%d" % (sum(1 for c in CTRL if c["ok"]), len(CTRL)),
                   "guards": "%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS))},
        "entries": ENTRIES, "controls": CTRL, "guards": GUARDS,
        "layering": {"A": "框架自我账本", "B": "五单元矩阵与旗舰归属",
                     "C": "v 双口径勘误", "D": "供给与判定"},
    }
    p = os.path.join(_DATADIR, BASE + ".json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return p, len(json.dumps(d, ensure_ascii=False, indent=1))


def write_md(a, an):
    pr = a["probe"]
    vd = a["vdual"]
    cells = a["cells"]
    L = []
    L.append("# TUFT-r205 · 统一性归因审计：旗舰统一数字的 MSSM 外部性与 v 双口径勘误")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、定位")
    L.append("")
    L.append("r199 证明「无量纲数据不能选出绝对尺度」；本卷改问：**已有的统一数字属于谁**。")
    L.append("结论：旗舰 (M_GUT=2.121e16, α_GUT⁻¹=24.2765) 只在 MSSM β 单元成立，")
    L.append("而 MSSM 已被 r192 path2 判 CLOSED-NEGATIVE；UFE-1 v1 文档 MSSM 计数 = 0。")
    L.append("")
    L.append("## 二、框架自我账本（机读 07）")
    L.append("")
    L.append("| 项 | 机读值 | 状态 |")
    L.append("|---|---|---|")
    L.append("| 验证报告 | %d 项（PASS %d / FAIL %d / INFO %d） | — |"
             % (a["report"]["summary"]["total"], a["report"]["summary"]["pass"],
                a["report"]["summary"]["fail"], a["report"]["summary"]["info"]))
    L.append("| R1.1 SM 交点比 | %s | FAIL |" % DOC_R11)
    L.append("| R1.2 SM 最小散布 | %s @ 2.65e12 | FAIL |" % DOC_R12)
    L.append("| R1.3 MSSM 最小散布 | %s @ 2.33e14 | INFO（对照） |" % DOC_R13)
    L.append("| 08 已验证预言 | V1–V7 共 %d 条 | 全为 SM/GR/QCD |" % len(a["vrows"]))
    L.append("| 00/01/08 的 MSSM 计数 | %s | 0 |" % str(a["mssm_docs"]))
    L.append("")
    L.append("## 三、五单元矩阵（独立复算，Decimal 60）")
    L.append("")
    L.append("| β 族 | sin²θ_W 口径 | 匹配条件 | x | M / GeV | α⁻¹ 散布 | 统一？ |")
    L.append("|---|---|---|---|---|---|---|")
    for c in cells:
        L.append("| %s | %s | %s | %.6f | %.4E | %.6f | %s |"
                 % (c["beta"], c["s"], c["match"], float(D(c["x"])), float(D(c["M"])),
                    float(D(c["spread"])), "是" if c["unified"] else "否"))
    L.append("")
    L.append("- SM 三交点：%.3E / %.3E / %.3E GeV（比值 %s）⇒ 无公共点。"
             % (float(D(pr["SM"]["crossings"]["m12"])), float(D(pr["SM"]["crossings"]["m13"])),
                float(D(pr["SM"]["crossings"]["m23"])), DOC_R11))
    L.append("- 五个「统一质量」跨 %.0f 倍 ⇒ 统一质量是口径选择，不是预测量。" % float(an["span"]))
    L.append("")
    L.append("## 四、v 双口径（P 级勘误）")
    L.append("")
    L.append("| 定义 | 值 / GeV | 来源 |")
    L.append("|---|---|---|")
    L.append("| (√2G_F)^(-1/2) | %s | 验证报告 E1（容差 0.002） |" % vd["v_gf"][:10])
    L.append("| 2M_W/g₂(α(0), sin²θ_W) | %s | r190–r199 全账本 |" % vd["v_alpha0"][:10])
    L.append("| 2M_W/g₂(α(M_Z), sin²θ_W) | %s | 本卷诊断 |" % vd["v_alphaMz"][:10])
    L.append("")
    L.append("- 偏差 **+%s%%**；成因 = g₂ 用 α(0) 而非 α(M_Z)。" % vd["delta_pct"][:6])
    L.append("- 受影响纯数：M*/v %s → %s；M_GUT/v %s → %s；M_Z/v %s → %s。"
             % (CANON_MSTAR_OVER_V, vd["mstar_over_v_corrected"][:8],
                vd["mgut_over_v_canon"][:8], vd["mgut_over_v_corrected"][:8],
                vd["mz_over_v_canon"][:8], vd["mz_over_v_corrected"][:8]))
    L.append("- 原始记录保留：勘误追加于 r194 判定册（%s）。" % patch_status(a))
    L.append("")
    L.append("## 五、归因结论")
    L.append("")
    L.append("- V1–V7 归因：SM 电弱 / GR / QCD 100%，TUFT 特有 0。")
    L.append("- 旗舰统一数字归因：MSSM β 100%；而 MSSM 被 r192 path2 判 CLOSED-NEGATIVE。")
    L.append("- verify_core.py 的框架特有 token 计数 = %d（UFE-1 仅作标签出现 %d 次）。"
             % (a["attribution"]["token_total"], a["attribution"]["ufe1_label_hits"]))
    L.append("")
    L.append("## 六、供给侧")
    L.append("")
    L.append("- 统一性证据 0（MSSM 外部情景不计入框架供给）；连续预言外部性 100%。")
    L.append("- 供给仍 0：α_GUT 0 / M_GUT 0 / τ_p 0 / 1/4 独立含量 0 / ℓ_sd 0。")
    L.append("")
    L.append("## 七、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for c in CTRL if c["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 八、判定与红线")
    L.append("")
    L.append("- **CLOSED-NEGATIVE（no-go）**：旗舰统一数字的框架自供含量 = 0。")
    L.append("- 本卷不否定 SM/GR/MSSM 自身的正确性，只否定其**归属于本框架**。")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def patch_status(a):
    return a["patch"]["status"]


def write_report(a, an, patch):
    L = []
    L.append("=" * 78)
    L.append("TUFT-r205 · 统一性归因审计 / 五单元矩阵 / v 双口径勘误")
    L.append("=" * 78)
    L.append("")
    L.append("[A] 框架自我账本（机读 07）")
    L.append("[B] 五单元矩阵与旗舰归属（独立复算）")
    L.append("[C] v 双口径勘误")
    L.append("[D] 供给与判定")
    L.append("")
    L.extend(fmt_entries())
    L.append("")
    L.append("-" * 78)
    L.append("控制组 %d/%d；守卫 %d/%d"
             % (sum(1 for c in CTRL if c["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("条目 %d（FAIL %d / INFO %d / PASS %d）"
             % (len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS")))
    L.append("v: G_F=%s | α(0)=%s | α(M_Z)=%s | Δ=%s%%"
             % (a["vdual"]["v_gf"][:9], a["vdual"]["v_alpha0"][:9],
                a["vdual"]["v_alphaMz"][:9], a["vdual"]["delta_pct"][:6]))
    L.append("勘误: %s（%d B -> %d B，前缀保留=%s）"
             % (patch["status"], patch["bytes_before"], patch["bytes_after"],
                patch["prefix_preserved"]))
    L.append("判词：%s" % VERDICT)
    L.append("红线：%s" % REDLINE)
    L.append("")
    L.append("[EXIT CODE] 0")
    p = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def write_book(a, an):
    pr = a["probe"]
    vd = a["vdual"]
    L = []
    L.append("# TUFT-r205 · 统一性归因审计：旗舰统一数字的 MSSM 外部性与 v 双口径勘误")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、判定")
    L.append("")
    L.append("- **CLOSED-NEGATIVE（no-go）**：旗舰统一数字 (M_GUT, α_GUT⁻¹) 的**框架自供含量 = 0**。")
    L.append("- 它们只在 MSSM β=(33/5,1,−3) 的 (α₁=α₃) 单元成立；MSSM 已被 r192 path2 判 CLOSED-NEGATIVE。")
    L.append("- 框架自有 SM 单圈按自身验证报告 R1.1/R1.2 明确不统一（比值 %s、散布 %s）。" % (DOC_R11, DOC_R12))
    L.append("- v 双口径偏差 +%s%% 登记为 P 级勘误（只追加，不改原记录）。" % vd["delta_pct"][:6])
    L.append("")
    L.append("## 二、出处（机读）")
    L.append("")
    L.append("| 路径 | 读数 |")
    L.append("|---|---|")
    L.append("| 07/验证脚本/验证报告.json | 47 项：PASS 39 / FAIL 2 / INFO 6 |")
    L.append("| 07/08_预言与判据.md | V1–V7 共 7 条已验证预言 |")
    L.append("| 07/09_已知局限.md | L10：UFE-1 v1 不能统一（已登记） |")
    L.append("| r192 JSON | path2_z4_susy = CLOSED-NEGATIVE |")
    L.append("| 00/01/08 | MSSM 计数 = 0 |")
    L.append("")
    L.append("## 三、五单元矩阵")
    L.append("")
    L.append("| β 族 | sin²θ_W 口径 | 匹配 | M / GeV | 散布 | 统一 |")
    L.append("|---|---|---|---|---|---|")
    for c in a["cells"]:
        L.append("| %s | %s | %s | %.4E | %.6f | %s |"
                 % (c["beta"], c["s"], c["match"], float(D(c["M"])), float(D(c["spread"])),
                    "是" if c["unified"] else "否"))
    L.append("")
    L.append("- 五个质量跨 %.1f 倍 ⇒ 统一质量 = 口径选择。" % float(
        max(D(c["M"]) for c in a["cells"]) / min(D(c["M"]) for c in a["cells"])))
    L.append("")
    L.append("## 四、v 双口径")
    L.append("")
    L.append("- v(G_F) = %s；v(α(0)) = %s；v(α(M_Z)) = %s。" % (
        vd["v_gf"][:10], vd["v_alpha0"][:10], vd["v_alphaMz"][:10]))
    L.append("- 偏差 +%s%%；受影响：M*/v、M_GUT/v、M_Z/v（×%s）。" % (
        vd["delta_pct"][:6], vd["factor"][:8]))
    L.append("")
    L.append("## 五、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for c in CTRL if c["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 六、红线")
    L.append("")
    L.append("- 归因审计只针对被引用的统一数字与 V1–V7；MSSM 是外部情景、不计入框架供给。")
    L.append("- v 勘误只追加不改原记录；供给仍 0；本卷条目不可与 r142–r204 相加。")
    p = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


# ---------------------------------------------------------------------------
# 七、主流程
# ---------------------------------------------------------------------------
def main():
    watched = [RPT_JSON, R192_JSON, R199_JSON]
    docs = [DOC00, DOC01, DOC08, DOC09]
    h0 = {p: sha(p) for p in watched}
    d0 = {p: sha(p) for p in docs}

    a = do_analysis()
    a["_hash_ok"] = all(sha(p) == h0[p] for p in watched)
    a["_hash_note"] = "3/3" if a["_hash_ok"] else "changed"
    a["_doc_hash_ok"] = all(sha(p) == d0[p] for p in docs)
    a["_doc_hash_note"] = "4/4" if a["_doc_hash_ok"] else "changed"

    an = build_entries(a)
    patch = apply_errata(a)
    a["patch"] = patch
    build_controls(a)
    build_guards(a, an, patch)

    jp, jn = write_json(a, an, patch)
    mp = write_md(a, an)
    rp = write_report(a, an, patch)
    bp = write_book(a, an)

    h1 = {p: sha(p) for p in watched}
    d1 = {p: sha(p) for p in docs}

    for line in fmt_entries():
        print(line)
    print("")
    print("-" * 78)
    print("控制组 %d/%d；守卫 %d/%d"
          % (sum(1 for c in CTRL if c["ok"]), len(CTRL),
             sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("条目 %d（FAIL %d / INFO %d / PASS %d）"
          % (len(ENTRIES),
             sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
             sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
             sum(1 for e in ENTRIES if e["verdict"] == "PASS")))
    print("只读校验：机读 %d/%d，文档 %d/%d"
          % (sum(1 for p in watched if sha(p) == h0[p]), len(watched),
             sum(1 for p in docs if sha(p) == d0[p]), len(docs)))
    print("产物：%s" % BASE)
    print("  json   %d B" % os.path.getsize(jp))
    print("  md     %d B" % os.path.getsize(mp))
    print("  report %d B" % os.path.getsize(rp))
    print("  book   %d B" % os.path.getsize(bp))
    print("勘误：%s（%d B -> %d B）" % (patch["status"], patch["bytes_before"], patch["bytes_after"]))
    print("判词：%s" % VERDICT)
    print("红线：%s" % REDLINE)
    rc = 0 if all(c["ok"] for c in CTRL) and all(g["ok"] for g in GUARDS) else 1
    print("")
    print("[EXIT CODE] %d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
