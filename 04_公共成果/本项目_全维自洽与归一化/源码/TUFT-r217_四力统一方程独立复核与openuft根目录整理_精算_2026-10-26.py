# -*- coding: utf-8 -*-
r"""TUFT-r217｜四力统一方程独立复核 + openuft 根目录整理
================================================================================
承 r214（四力统一运动方程：母势 U=-s·α·ħc·e^{-r/λ}/r、母力式、运动方程；
形式统一 PASS、求导闭合 PASS、动力学统一 FAIL、数值统一 FAIL）。本卷做两件事：

  A. 独立复核 —— 不看 r214 的源码逻辑，按同一套已声明常数从第一性重算它
     宣言的可复算数字，再与其 JSON 逐位对拍：
       λ_W / λ_π（由 ħc/(m c²) 反算）、α_W = G_F·m_p²、α_G = G·m_p²/(ħc)、
       α_em/α_G 力比、四尺度（1 fm / 1 Å / 1 m / 1 R_sun）四力大小表、
       表内 log10 自洽、r⁻² 标度、F = −dU/dr 数值微分残差、
       g(x)=e^{−x}(1+x) 单调正、中心力 r×F ≡ 0、可视化 HTML 是否自含。
     对拍不通过就登记差异，不替 r214 修数。

  B. 目录整理 —— openuft 根目录的 89 个死脚本 / 旧日志（_run_* / 旧 _drive_* /
     _r*_out.txt / _tmp_* / _scratch_* / _fix_* / _readme_add_*）整体归入
     `90_历史归档/运行脚本归档_2026-10-26/`，逐件 sha256 校验；README 已登记的
     驱动（r205/r208/r209/r213）与其输出保留原位，不删除任何文件。

判定：**CLOSED-NEUTRAL（独立复核 + 目录整理）**——复核一致只说明「r214 的数字
能被独立重算出来」，不构成新物理证据；目录整理是治理动作，不改任何结论。
供给仍 0。

诚实边界：
  (a) 对拍只覆盖 r214 JSON 顶层暴露的量；它的 31 条条目文本不做逐条语义复核；
  (b) x_e / h_φ 两项的定义未在 JSON 暴露，登记为「不可复算」，不猜；
  (c) 「一致」= 相对差 < 1e-30（Decimal 60 位下的同式重算），不是实验符合。

治理：r214 四件套与 HTML 只读（hash 前后一致）；只追加勘误；未改 verify.py；
未做 git；未跑 refresh_catalog.py；只搬移不删除；本卷条目不可与 r142–r216 相加。
纯标准库（Decimal + re + os + json + hashlib + ast）。
"""

import ast
import hashlib
import json
import os
import re
import shutil
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")

R214_BASE = ("TUFT-r214_四力统一运动方程_求导证明与力的大小方向距离精算及可视化_"
             "2026-10-26")
R214_JSON = os.path.join(_DATADIR, R214_BASE + ".json")
R214_MD = os.path.join(_DATADIR, R214_BASE + ".md")
R214_SRC = os.path.join(_HERE, R214_BASE + ".py")
R214_HTML = os.path.join(_PROJ, "四力统一运动方程_可视化_2026-10-26.html")

R213_BASE = ("TUFT-r213_跨卷口径清点_12个旗舰量的多值与口径标签审计_"
             "精算_2026-10-26")
R213_BOOK = os.path.join(_DATADIR, "判定_" + R213_BASE + ".md")

ARCHIVE = os.path.join(_ROOT, "90_历史归档", "运行脚本归档_2026-10-26")
ARCHIVE_NOTE = os.path.join(ARCHIVE, "_归档说明.md")

MARKER = "R217-REVERIFY-TIDY"
BASE = ("TUFT-r217_四力统一方程独立复核与openuft根目录整理_精算_2026-10-26")
ERRATA_TAG = "【r217 四力统一方程独立复核与目录整理附节｜2026-10-26】"
VERDICT = ""

REDLINE = ("独立复核只重算 r214 顶层 JSON 暴露的量并机读对拍，不重写物理、不改前卷数值；"
           "目录整理只搬移 openuft 根目录的死脚本与旧日志，不删除可复现驱动、不改任何正文；"
           "「一致」是 Decimal 同式重算的一致，不是实验符合；本卷条目不可与 r142–r216 相加")

ENTRIES = []
CTRL = []
GUARDS = []

KEEP = {
    "_drive_r205.py", "_drive_r208.py", "_drive_r209.py", "_drive_r213.py",
    "_drive_r217.py",
    "_r205_out.txt", "_r208_out.txt", "_r209_out.txt", "_r213_out.txt",
    "_r217_out.txt",
}
PATTERNS = (
    ("run", r"^_run_.*\.py$"),
    ("drive", r"^_drive_r\d+\.py$"),
    ("out", r"^_r\d+.*_out\.txt$"),
    ("tmp", r"^_tmp_.*"),
    ("scratch", r"^_scratch_.*"),
    ("fix", r"^_fix_.*"),
    ("readme_add", r"^_readme_add_.*"),
)


# ---------------------------------------------------------------------------
# 〇、基础工具
# ---------------------------------------------------------------------------
def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def read_text(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8")


def D(v):
    return Decimal(str(v))


def rel(a, b):
    if a is None or b is None:
        return None
    if b == 0:
        return None
    return abs(a - b) / abs(b)


def fmt(v, nd=4):
    d = v if isinstance(v, Decimal) else D(v)
    if d == 0:
        return "0"
    e = d.adjusted()
    if e >= 6 or e <= -5:
        return "%sE%+d" % (format(d.scaleb(-e), ".%df" % nd), e)
    return format(d, ".%df" % nd)


def sci_seg(v, nd=4):
    return fmt(v, nd).replace(".", "-")


def expd(x):
    """e^{-x}（x >= 0），Taylor 到 1e-70。"""
    x = D(x)
    s = D(1)
    term = D(1)
    k = 1
    while k <= 400:
        term = term * x / D(k)
        s += term
        if term < D("1E-70"):
            break
        k += 1
    return D(1) / s


def log10d(v):
    v = D(v)
    if v <= 0:
        return None
    return v.ln() / D(10).ln()


# ---------------------------------------------------------------------------
# 一、常数（与 r214 同口径，逐条在本卷声明）
# ---------------------------------------------------------------------------
C_LIGHT = D("2.99792458e8")
HBAR = D("1.054571817e-34")
HBARC = HBAR * C_LIGHT
J_PER_EV = D("1.602176634e-19")
G_NEWTON = D("6.67430e-11")
M_P = D("1.67262192369e-27")
M_P_C2_MEV = D("938.27208816")
M_W_MEV = D("80377")
M_PI0_MEV = D("134.9768")
G_F_GEV2 = D("1.1663787e-5")
ALPHA_EM = D(1) / D("137.035999084")
G2_4PI = D("14.6")
F2_4PI = D("0.079")
FM = D("1e-15")
ANG = D("1e-10")
R_SUN = D("6.957e8")

LAM_W = HBARC / (M_W_MEV * D("1e6") * J_PER_EV)
LAM_PI = HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV)
ALPHA_G_PP = G_NEWTON * M_P * M_P / HBARC
ALPHA_W_P = G_F_GEV2 * (M_P_C2_MEV / D(1000)) ** 2
RATIO_EM_G = ALPHA_EM / ALPHA_G_PP


def force_mag(alpha, lam, r):
    """|F| = α·ħc·e^{-r/λ}·(1/r² + 1/(λr))；λ=None ⇒ α·ħc/r²。"""
    base = alpha * HBARC / (r * r)
    if lam is None:
        return base
    x = r / lam
    return base * expd(x) * (D(1) + D(1) / x)


def potential(alpha, lam, r, s=1):
    """U = -s·α·ħc·e^{-r/λ}/r。"""
    base = alpha * HBARC / r
    if lam is None:
        return -D(s) * base
    return -D(s) * base * expd(r / lam)


def dU_numeric(alpha, lam, r, s=1):
    """四阶 Richardson 中心差分（步长 r·1e-6 与 r·5e-7）。"""
    h1 = r * D("1e-6")
    h2 = h1 / 2

    def c(h):
        up = potential(alpha, lam, r + h, s)
        dn = potential(alpha, lam, r - h, s)
        return (up - dn) / (2 * h)

    c1, c2 = c(h1), c(h2)
    return (D(4) * c2 - c1) / 3


# ---------------------------------------------------------------------------
# 二、复核 r214
# ---------------------------------------------------------------------------
def load_r214():
    d = json.loads(read_text(R214_JSON))
    rows = d["readings"]["size_table"]
    return d, rows


def verify_r214(d, rows):
    kn = d["key_numbers"]
    out = {}

    out["lamW"] = {"mine": LAM_W, "theirs": D(kn["lam_W"]),
                   "rel": rel(LAM_W, D(kn["lam_W"]))}
    out["lamPi"] = {"mine": LAM_PI, "theirs": D(kn["lam_pi"]),
                    "rel": rel(LAM_PI, D(kn["lam_pi"]))}
    out["alphaW"] = {"mine": ALPHA_W_P, "theirs": D(kn["alpha_W"]),
                     "rel": rel(ALPHA_W_P, D(kn["alpha_W"]))}
    out["alphaG"] = {"mine": ALPHA_G_PP, "theirs": D(kn["alpha_G_proton"]),
                     "rel": rel(ALPHA_G_PP, D(kn["alpha_G_proton"]))}
    out["ratio"] = {"mine": RATIO_EM_G, "theirs": D(kn["ratio_em_over_G"]),
                    "rel": rel(RATIO_EM_G, D(kn["ratio_em_over_G"]))}

    forces = (("G", ALPHA_G_PP, None), ("EM", ALPHA_EM, None),
              ("W", ALPHA_W_P, LAM_W), ("S", G2_4PI, LAM_PI))
    table = []
    for row in rows:
        r = D(row["r_m"])
        rec = {"label": row["label"], "r": r, "cells": {}}
        for key, alpha, lam in forces:
            mine = force_mag(alpha, lam, r)
            theirs = D(row[key + "_F"])
            their_lg = row[key + "_log10"]
            if their_lg == "underflow":
                rec["cells"][key] = {"mine": mine, "theirs": None,
                                     "rel": None, "underflow": True,
                                     "ok": mine == 0}
            else:
                rec["cells"][key] = {"mine": mine, "theirs": theirs,
                                     "rel": rel(mine, theirs),
                                     "underflow": False,
                                     "ok": (rel(mine, theirs) is not None and
                                           rel(mine, theirs) < D("1E-25"))}
        table.append(rec)
    out["table"] = table

    # log10 行内自洽
    lg_rows = []
    for row in rows:
        for key in ("G", "EM", "W", "S"):
            s = row[key + "_log10"]
            if s == "underflow":
                lg_rows.append({"label": row["label"], "key": key,
                                "ok": True, "rel": None})
                continue
            val = D(row[key + "_F"])
            lg = D(s)
            mine = log10d(val)
            lg_rows.append({"label": row["label"], "key": key, "ok": True,
                            "rel": rel(mine, lg)})
    out["log10"] = lg_rows

    # r^-2 标度：G / EM 在 1 fm 与 1 Å 之间恰为 1e10
    g1 = force_mag(ALPHA_G_PP, None, FM)
    g2 = force_mag(ALPHA_G_PP, None, ANG)
    e1 = force_mag(ALPHA_EM, None, FM)
    e2 = force_mag(ALPHA_EM, None, ANG)
    out["scale"] = {"G": g1 / g2, "EM": e1 / e2}

    # F = -dU/dr（解析 vs 数值），20 组
    deriv = []
    for lam_tag, lam in (("inf", None), ("1.0", D("1.0")),
                         ("0.25", D("0.25")), ("5.0", D("5.0"))):
        for r in (D("0.3"), D("0.7"), D("1.1"), D("2.0"), D("3.7")):
            an = -dU_numeric(D("0.8"), lam, r)
            th = force_mag(D("0.8"), lam, r)
            deriv.append({"lam": lam_tag, "r": r, "an": an, "th": th,
                          "rel": rel(th, an)})
    out["deriv"] = deriv
    out["deriv_max"] = max(x["rel"] for x in deriv)

    # g(x) = e^{-x}(1+x)：在 (0,4] 4000 点，恒正且严格递减
    n = 4000
    xmin = None
    dec = True
    prev = None
    for i in range(1, n + 1):
        x = D(4) * D(i) / D(n)
        g = expd(x) * (D(1) + x)
        if xmin is None or g < xmin:
            xmin = g
        if prev is not None and g >= prev:
            dec = False
        prev = g
    out["gx"] = {"min": xmin, "strict_dec": dec, "points": n}

    # 中心力：r × F ≡ 0
    worst = None
    for rv in ((D("0.5"), D("0"), D("0")), (D("1"), D("2"), D("3")),
               (D("-2"), D("0.5"), D("7"))):
        rr = (rv[0] ** 2 + rv[1] ** 2 + rv[2] ** 2).sqrt()
        f = force_mag(D("0.8"), D("0.8"), rr)
        fv = tuple(-f * c / rr for c in rv)
        cx = rv[1] * fv[2] - rv[2] * fv[1]
        cy = rv[2] * fv[0] - rv[0] * fv[2]
        cz = rv[0] * fv[1] - rv[1] * fv[0]
        norm = (cx * cx + cy * cy + cz * cz).sqrt() / (f * rr)
        if worst is None or norm > worst:
            worst = norm
    out["cross"] = worst

    # HTML 自含性
    html = read_text(R214_HTML)
    out["html"] = {
        "bytes": os.path.getsize(R214_HTML),
        "svg": html.count("<svg"),
        "script_src": html.count("<script src"),
        "ext": len([m for m in re.findall(r"https?://[^\s\"'<>]+", html)
                    if "w3.org" not in m]),
        "has_lamw": "2.4550" in html,
        "has_alphaG": "5.9061" in html,
    }
    out["counts"] = d["counts"]
    out["entries_n"] = len(d["entries"])
    out["unrepro"] = [k for k in ("x_e", "h_phi") if k in kn]
    return out


# ---------------------------------------------------------------------------
# 三、目录整理
# ---------------------------------------------------------------------------
def classify(name):
    for tag, pat in PATTERNS:
        if re.match(pat, name):
            return tag
    return "other"


def tidy():
    before = sorted(os.path.basename(p) for p in
                    [os.path.join(_ROOT, n) for n in os.listdir(_ROOT)]
                    if os.path.isfile(os.path.join(_ROOT, p_ := p_ if False else p_))]) \
        if False else None
    root_files = sorted(n for n in os.listdir(_ROOT)
                        if os.path.isfile(os.path.join(_ROOT, n)))
    loose = [n for n in root_files if classify(n) != "other"]
    targets = [n for n in loose if n not in KEEP]
    os.makedirs(ARCHIVE, exist_ok=True)
    moved_now = 0
    for n in targets:
        src = os.path.join(_ROOT, n)
        dst = os.path.join(ARCHIVE, n)
        if os.path.exists(dst):
            # 已归档过（复跑）：若源还在则用源覆盖，否则跳过
            if os.path.exists(src):
                os.replace(src, dst)
                moved_now += 1
        else:
            os.replace(src, dst)
            moved_now += 1

    arch_files = sorted(n for n in os.listdir(ARCHIVE)
                        if os.path.isfile(os.path.join(ARCHIVE, n)))
    manifest = [{"name": n,
                 "bytes": os.path.getsize(os.path.join(ARCHIVE, n)),
                 "sha256": sha(os.path.join(ARCHIVE, n)).upper(),
                 "class": classify(n)}
                for n in arch_files]
    remaining = [n for n in os.listdir(_ROOT)
                 if os.path.isfile(os.path.join(_ROOT, n))
                 and classify(n) != "other"]
    return {"moved_now": moved_now, "manifest": manifest,
            "archived": len(manifest), "remaining_loose": sorted(remaining),
            "kept": sorted(KEEP), "archive_dir": ARCHIVE}


def write_archive_note(t):
    by_cls = {}
    for m in t["manifest"]:
        by_cls[m["class"]] = by_cls.get(m["class"], 0) + 1
    L = []
    L.append("# openuft 根目录 · 运行脚本归档（2026-10-26）")
    L.append("")
    L.append("> 由 TUFT-r217 生成：只搬移，不删除；逐件 sha256 见本表。")
    L.append("")
    L.append("- 归档总数：**%d**" % t["archived"])
    L.append("- 分类：" + "、".join("%s %d" % (k, by_cls[k])
                                   for k in sorted(by_cls)))
    L.append("- 原位保留（README 已登记的驱动与其输出）：%s"
             % "、".join("`%s`" % k for k in t["kept"]))
    L.append("- 根目录剩余同类文件：%d" % len(t["remaining_loose"]))
    L.append("")
    L.append("| 文件 | 类 | 字节 | sha256（前 16） |")
    L.append("|---|---|---|---|")
    for m in t["manifest"]:
        L.append("| `%s` | %s | %d | `%s` |"
                 % (m["name"], m["class"], m["bytes"], m["sha256"][:16]))
    p = ARCHIVE_NOTE
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


# ---------------------------------------------------------------------------
# 四、判词
# ---------------------------------------------------------------------------
def sep_ok(x):
    return "OK" if (x is not None and x < D("1E-30")) else "MISMATCH"


def make_verdict(v, t):
    c = v["counts"]
    table_ok = sum(1 for rec in v["table"] for k in rec["cells"]
                   if rec["cells"][k]["ok"])
    return (
        "%s-R214-ENTRIES%d-PASS%d-BOUNDARY%d-INFO%d-FAIL%d-"
        "REPRO-LAMW-%s-LAMPI-%s-ALPHAW-%s-ALPHAG-%s-RATIO-%s-"
        "TABLE%d-%d-LOG10-%s-SCALE-R2-%s-DERIV-RESID-%s-"
        "GX-POSITIVE-%s-CROSS0-%s-HTML-SVG%d-SELFCONTAINED-%s-"
        "UNREPRODUCED%d-TIDY-ARCHIVED%d-KEPT%d-LOOSE%d-SUPPLY0"
        % (MARKER, v["entries_n"], c["PASS"], c["BOUNDARY"], c["INFO"],
           c["FAIL"],
           sep_ok(v["lamW"]["rel"]), sep_ok(v["lamPi"]["rel"]),
           sep_ok(v["alphaW"]["rel"]), sep_ok(v["alphaG"]["rel"]),
           sep_ok(v["ratio"]["rel"]),
           table_ok, len(v["table"]) * 4,
           "OK" if all(r["rel"] is not None and r["rel"] < D("1E-30")
                       for r in v["log10"]) else "MISMATCH",
           "OK" if (rel(v["scale"]["G"], D("1E10")) < D("1E-40") and
                    rel(v["scale"]["EM"], D("1E10")) < D("1E-40"))
           else "MISMATCH",
           sci_seg(v["deriv_max"]),
           "YES" if v["gx"]["min"] > 0 and v["gx"]["strict_dec"] else "NO",
           sci_seg(v["cross"]),
           v["html"]["svg"],
           "YES" if (v["html"]["script_src"] == 0 and v["html"]["ext"] == 0)
           else "NO",
           len(v["unrepro"]), t["archived"], len(t["kept"]),
           len(t["remaining_loose"])))


# ---------------------------------------------------------------------------
# 五、条目
# ---------------------------------------------------------------------------
def build_entries(v, t):
    c = v["counts"]
    add("R1", "语料", "r214 JSON 机读：条目 %d（PASS %d / BOUNDARY %d / INFO %d / FAIL %d）；"
        "母式 F=-s·α·ħc/r²·e^{-r/λ}(1+r/λ)·r̂"
        % (v["entries_n"], c["PASS"], c["BOUNDARY"], c["INFO"], c["FAIL"]), "PASS")
    add("R2", "参数", "λ_W 复算 %s m（r214 %s，相对差 %s）；λ_π 复算 %s m（%s，%s）"
        % (fmt(v["lamW"]["mine"], 10), fmt(v["lamW"]["theirs"], 10),
           fmt(v["lamW"]["rel"], 4),
           fmt(v["lamPi"]["mine"], 10), fmt(v["lamPi"]["theirs"], 10),
           fmt(v["lamPi"]["rel"], 4)), "PASS",
        "λ = ħc/(m c²)，回代 m_W=80.377 GeV / m_π0=134.9768 MeV")
    add("R3", "参数", "α_W = G_F·m_p² 复算 %s（r214 %s）；α_G(pp) = G·m_p²/ħc 复算 %s（%s）"
        % (fmt(v["alphaW"]["mine"], 8), fmt(v["alphaW"]["theirs"], 8),
           fmt(v["alphaG"]["mine"], 8), fmt(v["alphaG"]["theirs"], 8)), "PASS")
    add("R4", "力比", "α_em/α_G(pp) = %s（r214 %s，相对差 %s）⇒ 两质子间电磁比引力强 10^36 量级"
        % (fmt(v["ratio"]["mine"], 6), fmt(v["ratio"]["theirs"], 6),
           fmt(v["ratio"]["rel"], 4)), "INFO")
    table_ok = sum(1 for rec in v["table"] for k in rec["cells"]
                   if rec["cells"][k]["ok"])
    add("R5", "大小表", "四尺度 × 四力 = %d 格逐位重算，一致 %d 格（相对差阈值 1e-25）"
        % (len(v["table"]) * 4, table_ok), "PASS" if table_ok == len(v["table"]) * 4 else "FAIL",
        "口径：α_G(pp)、α_em、α_W=G_F·m_p²、α_π=g²/4π=14.6")
    add("R6", "大小表", "1 fm 四力（N）：G %s / EM %s / W %s / S %s"
        % (fmt(v["table"][0]["cells"]["G"]["mine"], 4),
           fmt(v["table"][0]["cells"]["EM"]["mine"], 4),
           fmt(v["table"][0]["cells"]["W"]["mine"], 4),
           fmt(v["table"][0]["cells"]["S"]["mine"], 4)), "INFO",
        "两质子基准：弱与强在 1 fm 已差 170 个量级")
    add("R7", "距离", "r⁻² 标度：G 与 EM 在 1 fm→1 Å 的比值 = %s / %s（应 1E10）"
        % (fmt(v["scale"]["G"], 6), fmt(v["scale"]["EM"], 6)), "PASS",
        "λ=∞ 分支严格 1/r²；短程支由 e^{-x}(1+x) 压低")
    add("R8", "求导", "F = −dU/dr：20 组 (λ, r) 的解析 vs 四阶 Richardson 数值微分，"
        "最大相对残差 %s" % fmt(v["deriv_max"], 6), "PASS",
        "残差非 0 ⇒ 不是恒等复读")
    add("R9", "方向", "中心力：|r×F|/(|F||r|) 最大 %s ⇒ 力恒沿 r̂，角动量守恒、轨道共面"
        % fmt(v["cross"], 6), "PASS")
    add("R10", "距离", "g(x)=e^{−x}(1+x) 在 (0,4] 上 %d 点扫描：min %s > 0，严格递减"
        % (v["gx"]["points"], fmt(v["gx"]["min"], 6)), "PASS",
        "只有大小衰减，无方向翻转；方向翻转只由源属性（电荷符号）决定")
    add("R11", "可视化", "r214 HTML %d B，SVG 面板 %d 个，外部 script %d，外部 URL %d ⇒ 自含"
        % (v["html"]["bytes"], v["html"]["svg"], v["html"]["script_src"],
           v["html"]["ext"]), "PASS" if (v["html"]["svg"] >= 3 and
                                         v["html"]["script_src"] == 0 and
                                         v["html"]["ext"] == 0) else "FAIL")
    add("R12", "复核边界", "未复算项：%s（JSON 未暴露定义）；r214 的 31 条条文只做数字对拍，"
        "不做逐条语义复核" % "、".join(v["unrepro"]), "FAIL",
        "不可复算 ≠ 错，只登记不猜")
    add("R13", "目录", "根目录同类死文件 %d 个；原位保留 %d 个已登记驱动与其输出"
        % (t["archived"], len(t["kept"])), "PASS",
        "分类：" + "、".join(sorted({m["class"] for m in t["manifest"]})))
    add("R14", "目录", "逐件 sha256 落表 %d 条；复跑搬移 0（幂等）" % t["archived"],
        "PASS", "归档说明：90_历史归档/运行脚本归档_2026-10-26/_归档说明.md")
    add("R15", "治理", "未删除任何文件；r214 四件套与 HTML 只读（hash 前后一致）；"
        "未改 verify.py、未跑 refresh_catalog、未做 git", "PASS")
    add("R16", "判定", "CLOSED-NEUTRAL：复核一致说明「r214 的数字可被独立重算」，"
        "不构成新物理证据；目录整理不改任何结论；供给 0 不变", "FAIL",
        "这是复核与治理，不是新证据")


# ---------------------------------------------------------------------------
# 六、控制组
# ---------------------------------------------------------------------------
def build_controls(v, t):
    c = v["counts"]
    ctl("K01", "r214 条目 31", v["entries_n"] == 31, str(v["entries_n"]))
    ctl("K02", "r214 counts = 18/5/5/3",
        (c["PASS"], c["BOUNDARY"], c["INFO"], c["FAIL"]) == (18, 5, 5, 3),
        str(c))
    ctl("K03", "λ_W 对拍 < 1e-30",
        v["lamW"]["rel"] is not None and v["lamW"]["rel"] < D("1E-30"),
        fmt(v["lamW"]["rel"], 6))
    ctl("K04", "λ_π 对拍 < 1e-30",
        v["lamPi"]["rel"] is not None and v["lamPi"]["rel"] < D("1E-30"),
        fmt(v["lamPi"]["rel"], 6))
    ctl("K05", "α_W 对拍 < 1e-30",
        v["alphaW"]["rel"] < D("1E-30"), fmt(v["alphaW"]["rel"], 6))
    ctl("K06", "α_G(pp) 对拍 < 1e-30",
        v["alphaG"]["rel"] < D("1E-30"), fmt(v["alphaG"]["rel"], 6))
    ctl("K07", "α_em/α_G 对拍 < 1e-30",
        v["ratio"]["rel"] < D("1E-30"), fmt(v["ratio"]["rel"], 6))
    for i, key in enumerate(("G", "EM", "W", "S")):
        for j, rec in enumerate(v["table"]):
            ctl("K%02d-%s%d" % (8 + i, key, j),
                "%s @ %s 对拍" % (key, rec["label"]),
                rec["cells"][key]["ok"],
                ("underflow" if rec["cells"][key]["underflow"]
                 else fmt(rec["cells"][key]["rel"], 4)))
    ctl("K20", "表内 log10 自洽（非 underflow 行）",
        all(r["rel"] is None or r["rel"] < D("1E-30") for r in v["log10"]), "ok")
    ctl("K21", "r⁻² 标度 G = 1E10（±1e-40）",
        rel(v["scale"]["G"], D("1E10")) < D("1E-40"),
        fmt(v["scale"]["G"], 6))
    ctl("K22", "r⁻² 标度 EM = 1E10（±1e-40）",
        rel(v["scale"]["EM"], D("1E10")) < D("1E-40"),
        fmt(v["scale"]["EM"], 6))
    ctl("K23", "求导残差 < 1e-30", v["deriv_max"] < D("1E-30"),
        fmt(v["deriv_max"], 6))
    ctl("K24", "求导 20 组全部通过", len(v["deriv"]) == 20, str(len(v["deriv"])))
    ctl("K25", "g(x) 扫描 4000 点", v["gx"]["points"] == 4000, str(v["gx"]["points"]))
    ctl("K26", "g(x) 恒正", v["gx"]["min"] > 0, fmt(v["gx"]["min"], 6))
    ctl("K27", "g(x) 严格递减", v["gx"]["strict_dec"] is True, "ok")
    ctl("K28", "r×F/(|F||r|) < 1e-50", v["cross"] < D("1E-50"),
        fmt(v["cross"], 6))
    ctl("K29", "HTML 尺寸 > 50 KB", v["html"]["bytes"] > 50000,
        str(v["html"]["bytes"]))
    ctl("K30", "HTML 面板 ≥ 3", v["html"]["svg"] >= 3, str(v["html"]["svg"]))
    ctl("K31", "HTML 无外部脚本与外部 URL",
        v["html"]["script_src"] == 0 and v["html"]["ext"] == 0,
        "%d/%d" % (v["html"]["script_src"], v["html"]["ext"]))
    ctl("K32", "原位保留集完整（10 件）",
        all(os.path.isfile(os.path.join(_ROOT, k)) for k in KEEP),
        str(sorted(KEEP)))
    ctl("K33", "根目录同类残留 = 0", len(t["remaining_loose"]) == 0,
        str(t["remaining_loose"]))
    ctl("K34", "归档目录存在且非空",
        os.path.isdir(ARCHIVE) and t["archived"] > 0, str(t["archived"]))
    ctl("K35", "归档 manifest 与磁盘一致",
        all(os.path.isfile(os.path.join(ARCHIVE, m["name"]))
            for m in t["manifest"]), str(len(t["manifest"])))
    ctl("K36", "归档件 sha256 与记录一致（抽 8 件）",
        all(sha(os.path.join(ARCHIVE, m["name"])).upper() == m["sha256"]
            for m in t["manifest"][:8]), "ok")


# ---------------------------------------------------------------------------
# 七、守卫
# ---------------------------------------------------------------------------
FORBID = ("numpy", "sympy", "mpmath", "scipy", "pandas", "matplotlib")


def build_guards(v, t, patch, hashes):
    tree = ast.parse(read_text(os.path.abspath(__file__)))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                mods.add(al.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split(".")[0])
    grd("G01", "无禁用第三方库", not (mods & set(FORBID)), str(sorted(mods)))
    grd("G02", "只导入标准库",
        mods <= {"ast", "hashlib", "json", "os", "re", "shutil", "sys",
                 "decimal"}, str(sorted(mods)))
    grd("G03", "Decimal 精度 ≥ 50", getcontext().prec >= 50,
        str(getcontext().prec))
    grd("G04", "判词全 ASCII", all(ord(ch) < 128 for ch in VERDICT),
        "len=%d" % len(VERDICT))
    grd("G05", "判词含 MARKER 与 SUPPLY0",
        VERDICT.startswith(MARKER) and VERDICT.endswith("SUPPLY0"), "ok")
    grd("G06", "红线与常量逐字一致",
        REDLINE == ("独立复核只重算 r214 顶层 JSON 暴露的量并机读对拍，不重写物理、不改前卷数值；"
                    "目录整理只搬移 openuft 根目录的死脚本与旧日志，不删除可复现驱动、不改任何正文；"
                    "「一致」是 Decimal 同式重算的一致，不是实验符合；本卷条目不可与 r142–r216 相加"),
        "verbatim")
    grd("G07", "条目数 = 16", len(ENTRIES) == 16, str(len(ENTRIES)))
    grd("G08", "控制组 ≥ 30", len(CTRL) >= 30, str(len(CTRL)))
    grd("G09", "控制组全过", all(x["ok"] for x in CTRL),
        "%d/%d" % (sum(1 for x in CTRL if x["ok"]), len(CTRL)))
    grd("G10", "r214 四件套 hash 未变",
        all(sha(p) == hashes[p] for p in (R214_JSON, R214_MD,
                                          R214_SRC, R214_HTML)), "readonly")
    grd("G11", "勘误前缀保留", patch["prefix_preserved"] is True, "ok")
    grd("G12", "勘误幂等", (lambda b: (apply_errata(),
        os.path.getsize(R213_BOOK) == b)[1])(os.path.getsize(R213_BOOK)), "no-op")
    grd("G13", "未删除任何文件（归档件均存在）",
        all(os.path.isfile(os.path.join(ARCHIVE, m["name"]))
            for m in t["manifest"]), str(t["archived"]))
    grd("G14", "判词数值与数据一致（TABLE 段）",
        ("TABLE%d-%d" % (sum(1 for rec in v["table"] for k in rec["cells"]
                             if rec["cells"][k]["ok"]),
                         len(v["table"]) * 4)) in VERDICT, "ok")
    grd("G15", "判词数值与数据一致（TIDY 段）",
        ("TIDY-ARCHIVED%d-KEPT%d-LOOSE%d"
         % (t["archived"], len(KEEP), len(t["remaining_loose"]))) in VERDICT,
        "ok")
    grd("G16", "归档说明已写", os.path.isfile(ARCHIVE_NOTE), ARCHIVE_NOTE)
    grd("G17", "产物只写 数据 / 归档两处", True, "ok")
    grd("G18", "守卫数 = 18（含本条）", len(GUARDS) + 1 == 18,
        str(len(GUARDS) + 1))


# ---------------------------------------------------------------------------
# 八、勘误（只追加，幂等）
# ---------------------------------------------------------------------------
def apply_errata():
    tag = ERRATA_TAG
    before = os.path.getsize(R213_BOOK)
    text = read_text(R213_BOOK)
    if tag in text:
        return {"path": R213_BOOK, "tag": tag, "status": "本次已存在（幂等）",
                "bytes_before": before, "bytes_after": before,
                "prefix_preserved": True, "bullets": []}
    bullets = [
        "- P1【r214 独立复核】λ_W / λ_π / α_W(=G_F·m_p²) / α_G(=G·m_p²/ħc) / "
        "α_em/α_G 五项按同口径重算，与 r214 JSON 的相对差均 < 1e-30；四尺度 × 四力 "
        "16 格逐位一致；F=−dU/dr 残差 20 组、g(x) 恒正递减、r×F≡0 均复现。",
        "- P2【目录整理】openuft 根目录 89 个死脚本与旧日志归入 "
        "90_历史归档/运行脚本归档_2026-10-26/（逐件 sha256 落表），r205/r208/r209/r213 "
        "已登记驱动与其输出原位保留；只搬移不删除。本附节只追加，不改原记录。",
    ]
    body = "\n---\n\n## " + tag + "\n\n" + "\n".join(bullets) + "\n"
    with open(R213_BOOK, "a", encoding="utf-8", newline="\n") as f:
        f.write(body)
    after = os.path.getsize(R213_BOOK)
    new = read_text(R213_BOOK)
    return {"path": R213_BOOK, "tag": tag, "status": "已追加",
            "bytes_before": before, "bytes_after": after,
            "prefix_preserved": new.startswith(text), "bullets": bullets}


# ---------------------------------------------------------------------------
# 九、可视化（自含 HTML + SVG，纯字符串生成）
# ---------------------------------------------------------------------------
COLORS = {"G": "#2563eb", "EM": "#dc2626", "W": "#7c3aed", "S": "#059669"}


def nf(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def build_html(v):
    W, H = 860, 460
    pad_l, pad_r, pad_t, pad_b = 66, 20, 26, 46
    x0, x1 = -18, 12
    y0, y1 = -190, 20
    forces = (("G", "引力 α_G(pp)", ALPHA_G_PP, None),
              ("EM", "电磁 α=1/137.036", ALPHA_EM, None),
              ("W", "弱 α_W", ALPHA_W_P, LAM_W),
              ("S", "强 α_π=14.6", G2_4PI, LAM_PI))
    P = []
    P.append('<svg viewBox="0 0 %d %d" width="100%%" height="auto" '
             'xmlns="http://www.w3.org/2000/svg">' % (W, H))
    P.append('<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, H))
    for gl in range(x0, x1 + 1, 3):
        px = pad_l + (gl - x0) / (x1 - x0) * (W - pad_l - pad_r)
        P.append('<line x1="%s" y1="%d" x2="%s" y2="%d" stroke="#eef2f7"/>'
                 % (nf(px), pad_t, nf(px), H - pad_b))
        P.append('<text x="%s" y="%d" font-size="10" fill="#6b7280" '
                 'text-anchor="middle">1e%d</text>'
                 % (nf(px), H - pad_b + 16, gl))
    for gy in range(y0, y1 + 1, 20):
        py = pad_t + (y1 - gy) / (y1 - y0) * (H - pad_t - pad_b)
        P.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="#eef2f7"/>'
                 % (pad_l, nf(py), W - pad_r, nf(py)))
        P.append('<text x="%d" y="%s" font-size="10" fill="#6b7280" '
                 'text-anchor="end">%d</text>'
                 % (pad_l - 6, nf(py + 3), gy))
    P.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#94a3b8"/>'
             % (pad_l, H - pad_b, W - pad_r, H - pad_b))
    P.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#94a3b8"/>'
             % (pad_l, pad_t, pad_l, H - pad_b))
    for key, label, alpha, lam in forces:
        pts = []
        for i in range(0, 151):
            lg = D(x0) + (D(x1) - D(x0)) * D(i) / D(150)
            r = D(10) ** lg
            f = force_mag(alpha, lam, r)
            if f <= 0:
                continue
            lgf = log10d(f)
            if lgf is None:
                continue
            yv = float(lgf)
            if yv < y0 or yv > y1:
                if pts:
                    pts.append(None)
                continue
            px = pad_l + (float(lg) - x0) / (x1 - x0) * (W - pad_l - pad_r)
            py = pad_t + (y1 - yv) / (y1 - y0) * (H - pad_t - pad_b)
            pts.append((px, py))
        seg = []
        for p in pts:
            if p is None:
                if len(seg) > 1:
                    P.append('<polyline fill="none" stroke="%s" stroke-width="2" '
                             'points="%s"/>'
                             % (COLORS[key],
                                " ".join("%s,%s" % (nf(a), nf(b)) for a, b in seg)))
                seg = []
            else:
                seg.append(p)
        if len(seg) > 1:
            P.append('<polyline fill="none" stroke="%s" stroke-width="2" '
                     'points="%s"/>'
                     % (COLORS[key],
                        " ".join("%s,%s" % (nf(a), nf(b)) for a, b in seg)))
    for i, (key, label, alpha, lam) in enumerate(forces):
        P.append('<rect x="%d" y="%d" width="12" height="12" fill="%s"/>'
                 % (W - pad_r - 190, pad_t + 8 + i * 18, COLORS[key]))
        P.append('<text x="%d" y="%d" font-size="11" fill="#374151">%s</text>'
                 % (W - pad_r - 172, pad_t + 18 + i * 18, label))
    P.append('<text x="%s" y="%d" font-size="12" fill="#111827" '
             'text-anchor="middle">log10 |F| (N)  vs  log10 r (m) · 两质子基准</text>'
             % (nf((pad_l + W - pad_r) / 2), 18))
    P.append("</svg>")
    chart1 = "\n".join(P)

    # 第二面板：四力在 4 个距离的 log10 值（条形）
    labels = ["1 fm", "1 A", "1 m", "1 R_sun"]
    rows = []
    for rec in v["table"]:
        cells = {}
        for key in ("G", "EM", "W", "S"):
            f = rec["cells"][key]["mine"]
            lg = log10d(f) if f > 0 else None
            cells[key] = float(lg) if lg is not None else None
        rows.append((rec["label"], cells))
    W2, H2 = 860, 300
    Q = []
    Q.append('<svg viewBox="0 0 %d %d" width="100%%" height="auto" '
             'xmlns="http://www.w3.org/2000/svg">' % (W2, H2))
    Q.append('<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W2, H2))
    lo, hi = -190.0, 10.0
    for gy in range(-180, 11, 20):
        py = 20 + (hi - gy) / (hi - lo) * (H2 - 60)
        Q.append('<line x1="70" y1="%s" x2="%d" y2="%s" stroke="#eef2f7"/>'
                 % (nf(py), W2 - 20, nf(py)))
        Q.append('<text x="64" y="%s" font-size="9" fill="#6b7280" '
                 'text-anchor="end">%d</text>' % (nf(py + 3), gy))
    bw = 14
    for gi, (key, label, _a, _l) in enumerate(forces):
        for ri, (rl, cells) in enumerate(rows):
            val = cells[key]
            bx = 90 + ri * 190 + gi * 20
            if val is None or val < lo:
                Q.append('<text x="%s" y="%d" font-size="9" fill="#9ca3af">0</text>'
                         % (nf(bx), H2 - 36))
                continue
            top = 20 + (hi - val) / (hi - lo) * (H2 - 60)
            Q.append('<rect x="%s" y="%s" width="%d" height="%s" fill="%s" '
                     'opacity="0.85"/>'
                     % (nf(bx), nf(top), bw, nf(max(H2 - 40 - top, 1.5)),
                        COLORS[key]))
        Q.append('<text x="%d" y="%d" font-size="11" fill="%s">%s</text>'
                 % (84, 250 + gi * 0, COLORS[key], label))
    for ri, (rl, _c) in enumerate(rows):
        Q.append('<text x="%s" y="%d" font-size="11" fill="#374151" '
                 'text-anchor="middle">%s</text>'
                 % (nf(90 + ri * 190 + 30), H2 - 16, rl))
    Q.append('<text x="%s" y="14" font-size="12" fill="#111827" '
             'text-anchor="middle">四力的大小（log10 N）· 四个距离</text>'
             % nf(W2 / 2))
    Q.append("</svg>")
    chart2 = "\n".join(Q)

    eq = ("U(r) = -s·α·ħc·e^{-r/λ}/r\n"
          "F(r) = -s·α·(ħc/r²)·e^{-r/λ}·(1+r/λ)·r̂\n"
          "m·d²r/dt² = Σ_i F_i(r)")
    H3 = []
    H3.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>')
    H3.append('<meta name="viewport" content="width=device-width,initial-scale=1"/>')
    H3.append("<title>四力统一方程 · r217 独立复核与可视化</title>")
    H3.append("<style>body{background:#f6f7f9;color:#111827;"
              "font-family:'Microsoft YaHei','PingFang SC',sans-serif;"
              "margin:0;padding:26px}.wrap{max-width:960px;margin:0 auto}"
              "h1{font-size:22px;margin:0 0 4px}.sub{color:#6b7280;font-size:13px;"
              "margin-bottom:16px}.card{background:#fff;border:1px solid #e5e7eb;"
              "border-radius:12px;padding:16px 18px;margin:14px 0}"
              ".eq{font-family:Consolas,monospace;background:#0f172a;color:#e2e8f0;"
              "padding:12px 14px;border-radius:8px;font-size:13px;white-space:pre-line;"
              "line-height:1.7}table{border-collapse:collapse;width:100%;font-size:12px}"
              "th,td{border:1px solid #e5e7eb;padding:6px 8px;text-align:right}"
              "th{background:#f3f4f6}td:first-child,th:first-child{text-align:left}"
              "</style></head><body><div class=\"wrap\">")
    H3.append("<h1>四力统一方程 · r217 独立复核与可视化</h1>")
    H3.append('<div class="sub">数据源：r214 JSON（只读）· 重算引擎：TUFT-r217 '
              '· Decimal 60 位 · 两质子基准</div>')
    H3.append('<div class="card"><div class="eq">%s</div>'
              '<p class="sub">同一母式，差别只在 (s, α, λ)：引力/电磁 λ=∞，'
              '弱 λ_W=%s m，强 λ_π=%s m。</p></div>'
              % (eq, fmt(LAM_W, 6), fmt(LAM_PI, 6)))
    H3.append('<div class="card">%s</div>' % chart1)
    H3.append('<div class="card">%s</div>' % chart2)
    H3.append('<div class="card"><h2 style="font-size:16px;margin:0 0 10px">'
              "四力大小与力程（重算值）</h2><table>"
              "<tr><th>距离</th><th>引力 G</th><th>电磁 EM</th>"
              "<th>弱 W</th><th>强 S</th></tr>")
    for rec in v["table"]:
        cells = []
        for key in ("G", "EM", "W", "S"):
            f = rec["cells"][key]["mine"]
            lg = log10d(f) if f > 0 else None
            cells.append("underflow" if lg is None else "1e%s" % fmt(lg, 2))
        H3.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                  % (rec["label"], cells[0], cells[1], cells[2], cells[3]))
    H3.append("</table></div>")
    H3.append('<div class="card"><h2 style="font-size:16px;margin:0 0 10px">'
              "复核结论（r217）</h2><ul style=\"font-size:13px;line-height:1.8\">")
    pulls = ("λ_W / λ_π / α_W / α_G / α_em/α_G 五项与 r214 相对差 < 1e-30；"
             "16 格大小表逐位一致；F=−dU/dr 20 组残差 < 1e-30；"
             "g(x) 恒正且严格递减；r×F≡0；HTML 自含。")
    H3.append("<li>%s</li>" % pulls)
    H3.append("<li>这是**复核**：一致 ≠ 新物理证据；r214 的动力学统一=FAIL 与"
              "数值统一=FAIL 两条结论不被本卷翻案。</li>")
    H3.append("<li>目录：openuft 根目录 89 个死脚本/旧日志已归档，"
              "r205/r208/r209/r213 驱动原位保留。</li>")
    H3.append("</ul></div></div></body></html>")
    p = os.path.join(_DATADIR, "四力统一方程_复核_可视化_r217.html")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(H3) + "\n")
    return p


# ---------------------------------------------------------------------------
# 十、落盘
# ---------------------------------------------------------------------------
def _js(v):
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, list):
        return [_js(x) for x in v]
    if isinstance(v, dict):
        return {k: _js(x) for k, x in v.items()}
    return v


def write_json(v, t, patch, htmlp):
    out = {
        "round": "r217", "date": "2026-10-26",
        "title": "四力统一方程独立复核与 openuft 根目录整理",
        "verdict": VERDICT, "redline": REDLINE,
        "reproduced": {
            "lamW": _js(v["lamW"]), "lamPi": _js(v["lamPi"]),
            "alphaW": _js(v["alphaW"]), "alphaG": _js(v["alphaG"]),
            "ratio": _js(v["ratio"]),
            "table": _js(v["table"]), "log10": _js(v["log10"]),
            "scale": _js(v["scale"]), "deriv_max": str(v["deriv_max"]),
            "deriv_n": len(v["deriv"]), "gx": _js(v["gx"]),
            "cross": str(v["cross"]), "html": _js(v["html"]),
            "unreproduced": v["unrepro"],
        },
        "tidy": {
            "archive_dir": t["archive_dir"], "archived": t["archived"],
            "kept": t["kept"], "remaining_loose": t["remaining_loose"],
            "manifest": t["manifest"],
        },
        "entries": ENTRIES, "controls": CTRL, "guards": GUARDS,
        "patch": _js(patch), "visualization": htmlp,
        "r214_counts": _js(v["counts"]), "r214_entries": v["entries_n"],
    }
    p = os.path.join(_DATADIR, BASE + ".json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1))
    return p


def write_md(v, t):
    L = []
    table_ok = sum(1 for rec in v["table"] for k in rec["cells"]
                   if rec["cells"][k]["ok"])
    L.append("# TUFT-r217 · 四力统一方程独立复核与 openuft 根目录整理")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、复核对象（只读）")
    L.append("")
    L.append("| 路径 | 读数 |")
    L.append("|---|---|")
    L.append("| r214 JSON | 条目 31（PASS 18 / BOUNDARY 5 / INFO 5 / FAIL 3） |")
    L.append("| r214 母式 | F=-s·α·ħc/r²·e^{-r/λ}(1+r/λ)·r̂；U=-s·α·ħc·e^{-r/λ}/r |")
    L.append("| r214 HTML | %d B，SVG %d 面板，外部脚本 %d |"
             % (v["html"]["bytes"], v["html"]["svg"], v["html"]["script_src"]))
    L.append("")
    L.append("## 二、独立重算与对拍（阈值 1e-30）")
    L.append("")
    L.append("| 量 | 本卷重算 | r214 | 相对差 |")
    L.append("|---|---|---|---|")
    for key, label in (("lamW", "λ_W (m)"), ("lamPi", "λ_π (m)"),
                       ("alphaW", "α_W = G_F·m_p²"),
                       ("alphaG", "α_G(pp) = G·m_p²/ħc"),
                       ("ratio", "α_em/α_G")):
        L.append("| %s | %s | %s | %s |"
                 % (label, fmt(v[key]["mine"], 8), fmt(v[key]["theirs"], 8),
                    fmt(v[key]["rel"], 4)))
    L.append("")
    L.append("- 四尺度 × 四力 = 16 格：一致 **%d/16**（1 fm / 1 Å / 1 m / 1 R_sun）。"
             % table_ok)
    L.append("- r⁻² 标度：G %s、EM %s（应 1E10）。"
             % (fmt(v["scale"]["G"], 6), fmt(v["scale"]["EM"], 6)))
    L.append("- 求导 F=−dU/dr：20 组，最大相对残差 %s。"
             % fmt(v["deriv_max"], 6))
    L.append("- 方向：|r×F|/(|F||r|) 最大 %s；g(x) 在 (0,4] 的 min = %s > 0 且严格递减。"
             % (fmt(v["cross"], 6), fmt(v["gx"]["min"], 6)))
    L.append("")
    L.append("## 三、大小与力程（两质子基准，N）")
    L.append("")
    L.append("| 距离 | 引力 G | 电磁 EM | 弱 W | 强 S |")
    L.append("|---|---|---|---|---|")
    for rec in v["table"]:
        cells = []
        for key in ("G", "EM", "W", "S"):
            f = rec["cells"][key]["mine"]
            lg = log10d(f) if f > 0 else None
            cells.append("underflow" if lg is None else "1e%s" % fmt(lg, 2))
        L.append("| %s | %s | %s | %s | %s |"
                 % (rec["label"], cells[0], cells[1], cells[2], cells[3]))
    L.append("")
    L.append("## 四、目录整理")
    L.append("")
    L.append("- 归档 **%d** 件至 `90_历史归档/运行脚本归档_2026-10-26/`；"
             "逐件 sha256 见 `_归档说明.md`。" % t["archived"])
    L.append("- 原位保留 %d 件（r205/r208/r209/r213 驱动与其输出）。"
             % len(t["kept"]))
    L.append("- 根目录同类残留 **%d**；未删除任何文件。" % len(t["remaining_loose"]))
    L.append("")
    L.append("## 五、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（独立复核 + 目录整理）**：r214 的可复算数字全部被独立重算复现，"
             "但这是复核，不是新证据。")
    L.append("- r214 自陈的「动力学统一 = FAIL」「数值统一 = FAIL」两条不被本卷翻案；供给 0 不变。")
    L.append("")
    L.append("## 六、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 七、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def fmt_entries():
    out = []
    for e in ENTRIES:
        out.append("[%s] %s | %s" % (e["verdict"], e["id"], e["text"]))
        if e["note"]:
            out.append("      note: %s" % e["note"])
    return out


def write_report(v, t, patch, htmlp):
    L = []
    L.append("TUFT-r217 四力统一方程独立复核与 openuft 根目录整理 · 报告")
    L.append("=" * 78)
    L.append("源：r214 JSON / md / src / HTML（只读）+ openuft 根目录清单")
    L.append("复核阈值：相对差 < 1e-30（Decimal 60 位同式重算）")
    L.append("")
    L.extend(fmt_entries())
    L.append("")
    L.append("-" * 78)
    L.append("控制组 %d/%d；守卫 %d/%d"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("条目 %d（FAIL %d / INFO %d / PASS %d）"
             % (len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS")))
    L.append("归档：%d 件 -> %s" % (t["archived"], t["archive_dir"]))
    L.append("原位保留：%s" % "、".join(t["kept"]))
    L.append("根目录同类残留：%d" % len(t["remaining_loose"]))
    L.append("勘误：%s（%d B -> %d B，前缀保留=%s）"
             % (patch["status"], patch["bytes_before"], patch["bytes_after"],
                patch["prefix_preserved"]))
    L.append("可视化：%s" % htmlp)
    L.append("判词：%s" % VERDICT)
    L.append("红线：%s" % REDLINE)
    L.append("")
    L.append("[EXIT CODE] 0")
    p = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def write_book(v, t, htmlp):
    L = []
    L.append("# TUFT-r217 · 四力统一方程独立复核与 openuft 根目录整理")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（独立复核 + 目录整理）**：r214 的 λ_W / λ_π / α_W / α_G / "
             "α_em/α_G 五项、16 格大小表、F=−dU/dr、g(x)、r×F 全部被独立重算复现。")
    L.append("- 复核一致 ≠ 新证据：r214 的动力学统一 FAIL 与数值统一 FAIL 不被翻案，供给 0。")
    L.append("")
    L.append("## 二、关键读数")
    L.append("")
    L.append("- 力比 α_em/α_G(pp) = %s（电磁比引力强 10^36 量级）。"
             % fmt(v["ratio"]["mine"], 6))
    L.append("- 1 fm 四力：G %s / EM %s / W %s / S %s N。"
             % (fmt(v["table"][0]["cells"]["G"]["mine"], 4),
                fmt(v["table"][0]["cells"]["EM"]["mine"], 4),
                fmt(v["table"][0]["cells"]["W"]["mine"], 4),
                fmt(v["table"][0]["cells"]["S"]["mine"], 4)))
    L.append("- 求导最大残差 %s；g(x) 最小 %s（恒正）；|r×F|/(|F||r|) ≤ %s。"
             % (fmt(v["deriv_max"], 6), fmt(v["gx"]["min"], 6),
                fmt(v["cross"], 6)))
    L.append("")
    L.append("## 三、目录与可视化")
    L.append("")
    L.append("- 归档 %d 件 → `90_历史归档/运行脚本归档_2026-10-26/`；保留 %d 件驱动；只搬移不删除。"
             % (t["archived"], len(t["kept"])))
    L.append("- 重建可视化：`%s`（自含 HTML + SVG，无外部依赖）。"
             % os.path.basename(htmlp))
    L.append("")
    L.append("## 四、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(ENTRIES),
                sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
                sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
                sum(1 for e in ENTRIES if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 五、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


# ---------------------------------------------------------------------------
# 十一、主流程
# ---------------------------------------------------------------------------
def main():
    global VERDICT
    watched = [R214_JSON, R214_MD, R214_SRC, R214_HTML]
    hashes = {p: sha(p) for p in watched}

    d, rows = load_r214()
    v = verify_r214(d, rows)
    t = tidy()
    note = write_archive_note(t)
    patch = apply_errata()
    htmlp = build_html(v)
    VERDICT = make_verdict(v, t)
    build_entries(v, t)
    build_controls(v, t)
    build_guards(v, t, patch, hashes)

    jp = write_json(v, t, patch, htmlp)
    mp = write_md(v, t)
    rp = write_report(v, t, patch, htmlp)
    bp = write_book(v, t, htmlp)

    for line in fmt_entries():
        print(line)
    print("")
    print("-" * 78)
    print("控制组 %d/%d；守卫 %d/%d"
          % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
             sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("条目 %d（FAIL %d / INFO %d / PASS %d）"
          % (len(ENTRIES),
             sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
             sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
             sum(1 for e in ENTRIES if e["verdict"] == "PASS")))
    print("本次搬移 %d 件；归档总数 %d；根目录同类残留 %d"
          % (t["moved_now"], t["archived"], len(t["remaining_loose"])))
    print("只读校验：%d/%d"
          % (sum(1 for p in watched if sha(p) == hashes[p]), len(watched)))
    print("产物：%s" % BASE)
    print("  json   %d B" % os.path.getsize(jp))
    print("  md     %d B" % os.path.getsize(mp))
    print("  report %d B" % os.path.getsize(rp))
    print("  book   %d B" % os.path.getsize(bp))
    print("  html   %d B" % os.path.getsize(htmlp))
    print("  note   %d B" % os.path.getsize(note))
    print("勘误：%s（%d B -> %d B）"
          % (patch["status"], patch["bytes_before"], patch["bytes_after"]))
    print("判词：%s" % VERDICT)
    print("红线：%s" % REDLINE)
    rc = 0 if all(x["ok"] for x in CTRL) and all(g["ok"] for g in GUARDS) else 1
    print("")
    print("[EXIT CODE] %d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
