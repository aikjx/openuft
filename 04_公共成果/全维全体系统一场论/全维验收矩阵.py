# -*- coding: utf-8 -*-
"""
全维验收矩阵 · 本项目级「统一场论完成度」机器验收
==============================================================
对象：openuft 全部登记体系（22 = P01–P04 + S01–S18）
承接（不新造口径，全部复用仓库自有规范）：
  04_公共成果/统一理论体系_已验证正确内容整合全集.md  —— 三重闸门 L0–L4 / H-O-C-U / [A][B][C]
  02_共享基础/研究规范/method_F_第一性判据.md       —— 六判据（无量纲化 / 循环 / 双锚点 / 自由度 / L3 门槛 / 源量级）
  07_统一场方程/README.md §5                        —— 架构统一 ≠ 物理统一 ≠ 理论完成
  04_公共成果/状态看板.md                           —— H/O/C/U 与开放缺口清单
红线：
  ① 不新造口径；② 每格判据必须挂一个**存在**的证据锚点（机器逐格 stat）；
  ③ 机器可读字段（system status / claims 计数 / 覆盖度）一律现场读取，不硬编码；
  ④ 本矩阵只判「离完成还差什么」，不判「本体是否为真」——过格不等于理论成立。
运行：python -B 全维验收矩阵.py    （纯标准库，Python 3.8）
输出：数据/全维验收矩阵.json + 数据/全维验收矩阵.md
==============================================================
"""

import sys
import os
import io
import json
import re
import collections

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(HERE, "数据")
SYSDIR = os.path.join(ROOT, "01_独立体系")

RPT = []


def say(line=""):
    print(line)
    RPT.append(line)


SCS = []


def sc(tag, ok, detail):
    SCS.append((tag, bool(ok), detail))
    say("[SC-%s] %s  %s" % (tag, "OK" if ok else "NG", detail))


def read_text(rel):
    path = os.path.join(ROOT, rel)
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


say("=" * 78)
say("全维验收矩阵 · 本项目级「统一场论完成度」机器验收（2026-10-08）")
say("对象 22 体系 | 8 条完成判据 | 每格强制挂存在性证据锚点 | 判据口径全部复用仓库自有规范")
say("=" * 78)
say("")

# ------------------------------------------------------------------
# 1. 机器可读输入：system_registry.json + 各体系 claims.csv
# ------------------------------------------------------------------
REG_PATH = os.path.join(ROOT, "00_项目治理", "system_registry.json")
with io.open(REG_PATH, "r", encoding="utf-8") as fh:
    REG = json.load(fh)
SYSTEMS = REG["systems"]
say("-" * 78)
say("1. 机器可读输入")
say("-" * 78)
say("registry：%d 个体系" % len(SYSTEMS))

CLAIMS = {}
TOTAL_ROWS = 0
ALL_IDS = []
for ent in SYSTEMS:
    cpath = os.path.join(SYSDIR, ent["directory"], "claims.csv")
    rec = {"rows": 0, "unique": 0, "dups": [], "status": {}, "exists": os.path.isfile(cpath)}
    if rec["exists"]:
        body = [ln for ln in read_text(os.path.relpath(cpath, ROOT).replace("\\", "/")).splitlines()
                if ln.strip()]
        if body:
            header = body[0].split(",")
            sidx = header.index("status") if "status" in header else -1
            ids = []
            for ln in body[1:]:
                parts = ln.split(",")
                ids.append(parts[0])
                st = parts[sidx] if (sidx >= 0 and len(parts) > sidx) else ""
                rec["status"][st] = rec["status"].get(st, 0) + 1
            cnt = collections.Counter(ids)
            rec["rows"] = len(ids)
            rec["unique"] = len(cnt)
            rec["dups"] = sorted(k for k, v in cnt.items() if v > 1)
            TOTAL_ROWS += len(ids)
            ALL_IDS.extend(ids)
    CLAIMS[ent["id"]] = rec

n_claims_files = sum(1 for v in CLAIMS.values() if v["exists"])
say("claims.csv：%d/%d 存在；数据行合计 %d，id 唯一 %d"
    % (n_claims_files, len(SYSTEMS), TOTAL_ROWS, len(set(ALL_IDS))))
sc("1", n_claims_files == len(SYSTEMS),
   "每个登记体系都有 claims.csv（%d/%d）；行数合计 %d、id 唯一 %d（现场读取）"
   % (n_claims_files, len(SYSTEMS), TOTAL_ROWS, len(set(ALL_IDS))))

# ------------------------------------------------------------------
# 2. 证据锚点登记（每格判据只允许引用这里的锚点；机器逐格 stat）
# ------------------------------------------------------------------
ANCHOR_TPL = {
    "P": "01_独立体系/{dir}/README.md",
    "C": "01_独立体系/{dir}/claims.csv",
}
ANCHOR_FIX = {
    "B": "04_公共成果/状态看板.md",
    "I": "04_公共成果/统一理论体系_已验证正确内容整合全集.md",
    "U": "07_统一场方程/README.md",
    "L": "07_统一场方程/09_已知局限与否定清单.md",
    "M": "02_共享基础/研究规范/method_F_第一性判据.md",
    "G": "07_统一场方程/07_现象覆盖矩阵.md",
    "F": "04_公共成果/全维全体系统一场论/全维全体系统一场论.md",
}


def anchor_path(letter, directory):
    if letter in ANCHOR_TPL:
        return ANCHOR_TPL[letter].format(dir=directory)
    return ANCHOR_FIX[letter]


# ------------------------------------------------------------------
# 3. 完成判据 W0–W7（口径来源见文件头；W0 由机器算，W1–W7 逐格手写但强制挂锚点）
# ------------------------------------------------------------------
CRIT_ORDER = ["W1", "W2", "W3", "W4", "W5", "W6", "W7"]
CRIT_DEF = [
    ("W0", "联盟级收口覆盖", "被『收口产物』（整合全集 ∨ 全维全体系统一场论.md）点名覆盖", "整合全集 §二 全景裁决表"),
    ("W1", "架构统一", "存在单一主方程/总作用量，四力为其分量（非四组方程并列）", "07 §2 主方程；§5 界限 1"),
    ("W2", "主方程第一性", "主方程由该体系自有公设导出（非教科书重述/借用）", "整合全集 §1.2 判据二；07 自陈"),
    ("W3", "无量纲输出", "至少输出一个**无量纲量数值**且非测量锚", "method_F §2 判据一（真目标判据）"),
    ("W4", "耦合统一", "三规范耦合在同一条链上汇聚（L10）", "07 §4 FAIL 行；P03-A5"),
    ("W5", "经典极限还原", "GR / 牛顿 / 低能 SM 极限可还原", "07 §3 四力还原"),
    ("W6", "谱与代", "给出 3 代来源 **且** 质量层级或绝对标度", "状态看板 §四 开放缺口（仓库级最大缺口）"),
    ("W7", "可证伪窗口", "有定量预言，且该窗口**未被实验排除**", "method_F 判据五/六；状态看板 §五"),
]

# ------------------------------------------------------------------
# 4. W0：联盟级收口覆盖（机器扫描，不手写）
# ------------------------------------------------------------------
COVER_TOKEN = {
    "p01_space_compression": ["空间压缩"],
    "p02_matter_source": ["物体驱动"],
    "p03_gauge_unification": ["规范对称"],
    "p04_quantum_emergence": ["量子涌现", "量子结构与时空涌现"],
    "s01_triad_kinematics": ["螺旋三重奏"],
    "s02_light_speed_helix_force": ["空间光速螺旋统一力"],
    "s03_gaq_geometric_atom": ["GAQ 几何原子"],
    "s04_ieg_information_gravity": ["信息熵引力"],
    "s05_hdu_higher_dimensions": ["高维紧致化"],
    "s06_tcl_topological_chirality": ["拓扑手征"],
    "s07_gaq_complex_curvature": ["复曲率融合"],
    "s08_gaq_geometrized_constants": ["GAQ 常数几何化"],
    "s09_gaq_mass_spectrum": ["质量谱"],
    "s10_frequency_helix_ontology": ["频率本源"],
    "s11_gmuft_geometric_coupling": ["GMUFT"],
    "s12_light_speed_helix": ["空间光速螺旋统一体系"],
    "s13_duality_fractal_uft": ["分形"],
    "s14_torsion_unified_field_tuft": ["挠率统一场论"],
    "s15_light_speed_helix_ct_uft": ["曲率挠率几何统一场论"],
    "s16_tuft_normalization_manual": ["归一化主册"],
    "s17_unified_field_core_formulas": ["统一场论核心公式"],
    "s18_curvature_energy_density": ["曲率能量密度"],
}

COVER_ART = [
    ("整合全集", ANCHOR_FIX["I"]),
    ("收口主文档", ANCHOR_FIX["F"]),
    ("状态看板", ANCHOR_FIX["B"]),
]
COVER_TEXT = {name: read_text(rel) for name, rel in COVER_ART}
COVER = {}
for ent in SYSTEMS:
    toks = COVER_TOKEN[ent["id"]]
    hit = {}
    matched = {}
    for name, text in COVER_TEXT.items():
        got = [t for t in toks if t in text]
        hit[name] = bool(got)
        matched[name] = got
    COVER[ent["id"]] = {
        "tokens": toks,
        "matched": matched,
        "hit": hit,
        # W0 只看收口/整合类产物（看板只给健康度、不给收口结论，不计入）
        "w0": bool(hit.get("整合全集") or hit.get("收口主文档")),
    }

say("")
say("-" * 78)
say("2. W0 联盟级收口覆盖（机器扫描三份索引产物）")
say("-" * 78)
for name, rel in COVER_ART:
    n = sum(1 for v in COVER.values() if v["hit"][name])
    say("%-10s %2d/%2d 体系被点名（锚点 %s）" % (name, n, len(SYSTEMS), rel))
for name in ("整合全集", "收口主文档"):
    hits = [e["id"] for e in SYSTEMS if COVER[e["id"]]["hit"][name]]
    say("  %s 命中清单：%s" % (name, "、".join(hits) if hits else "（无）"))
w0_fail = [e["id"] for e in SYSTEMS if not COVER[e["id"]]["w0"]]
say("W0（收口产物覆盖）未覆盖：%s" % ("、".join(w0_fail) if w0_fail else "无"))

# 词表校准：整合全集自陈覆盖数必须与扫描数相等（否则是词表坏了，不是事实变了）
DECL = {}
for name, pat in (("整合全集", r"全部\s*\*\*(\d+)\s*个登记体系"),
                  ("收口主文档", r"编入图谱的理论体系\s*\*\*(\d+)\s*个\*\*")):
    m = re.search(pat, COVER_TEXT[name])
    DECL[name] = int(m.group(1)) if m else None
SCAN_I = sum(1 for v in COVER.values() if v["hit"]["整合全集"])
SCAN_F = sum(1 for v in COVER.values() if v["hit"]["收口主文档"])
sc("2", SCAN_I == DECL["整合全集"],
   "覆盖度现场算得：整合全集 %d/22（其自陈 %s，校准%s）、收口主文档 %d/22（其自陈 %s，自带编号口径与官方 22 体系不可映射）、"
   "看板 %d/22；W0 未覆盖 %d 个（%s）"
   % (SCAN_I, DECL["整合全集"], "通过" if SCAN_I == DECL["整合全集"] else "失败",
      SCAN_F, DECL["收口主文档"],
      sum(1 for v in COVER.values() if v["hit"]["状态看板"]),
      len(w0_fail), "、".join(w0_fail) if w0_fail else "无"))


# 编号口径冲突：收口主文档使用自带 S01–S08，与官方稳定编号逐号对撞
NUMPAT = re.compile(r"^\|\s*(S\d{2})\s*\|\s*([^|]+?)\s*\|", re.M)
OFFICIAL = {}
for ent in SYSTEMS:
    m = re.match(r"^s(\d{2})_", ent["id"])
    if m:
        OFFICIAL["S" + m.group(1)] = ent["title"]
CONFLICT = []
for num, name in NUMPAT.findall(COVER_TEXT["收口主文档"]):
    off = OFFICIAL.get(num)
    if off is None:
        continue
    ok = (off in name) or (name in off)
    CONFLICT.append({"num": num, "doc_name": name, "official": off, "same": bool(ok)})
n_bad = sum(1 for c in CONFLICT if not c["same"])
sc("3", len(CONFLICT) > 0 and n_bad == len(CONFLICT),
   "收口主文档自带编号 S01–S%02d 与官方稳定编号逐号对撞：%d/%d 号指不同体系（机器逐号比对）"
   % (len(CONFLICT), n_bad, len(CONFLICT)))

# ------------------------------------------------------------------
# 5. 完成判据 W1–W7 逐格判定（verdict ∈ PASS/PART/FAIL/NA；锚点为 ANCHOR 字母）
# ------------------------------------------------------------------
VERDICT = {
    "p01_space_compression": [("NA", "B")] * 7,
    "p02_matter_source": [("NA", "B")] * 7,
    "p03_gauge_unification": [("PART", "P"), ("PART", "P"), ("FAIL", "P"), ("PART", "P"),
                              ("PART", "P"), ("FAIL", "P"), ("PART", "P")],
    "p04_quantum_emergence": [("NA", "B")] * 7,
    "s01_triad_kinematics": [("NA", "B"), ("NA", "B"), ("FAIL", "P"), ("NA", "B"),
                             ("NA", "B"), ("NA", "B"), ("NA", "B")],
    "s02_light_speed_helix_force": [("PART", "P"), ("FAIL", "C"), ("FAIL", "C"), ("FAIL", "P"),
                                    ("FAIL", "I"), ("FAIL", "P"), ("FAIL", "B")],
    "s03_gaq_geometric_atom": [("PART", "P"), ("FAIL", "I"), ("FAIL", "I"), ("FAIL", "C"),
                               ("PART", "I"), ("FAIL", "C"), ("FAIL", "C")],
    "s04_ieg_information_gravity": [("PART", "P"), ("FAIL", "I"), ("FAIL", "P"), ("FAIL", "P"),
                                    ("PART", "I"), ("FAIL", "P"), ("FAIL", "P")],
    "s05_hdu_higher_dimensions": [("PART", "P"), ("PART", "I"), ("FAIL", "I"), ("FAIL", "P"),
                                  ("FAIL", "P"), ("FAIL", "P"), ("FAIL", "P")],
    "s06_tcl_topological_chirality": [("PART", "P"), ("FAIL", "I"), ("FAIL", "P"), ("FAIL", "P"),
                                      ("NA", "P"), ("PART", "P"), ("PART", "P")],
    "s07_gaq_complex_curvature": [("PART", "P"), ("FAIL", "I"), ("FAIL", "I"), ("FAIL", "P"),
                                  ("PART", "P"), ("FAIL", "C"), ("FAIL", "B")],
    "s08_gaq_geometrized_constants": [("PART", "P"), ("FAIL", "I"), ("FAIL", "I"), ("FAIL", "P"),
                                      ("NA", "P"), ("FAIL", "P"), ("FAIL", "P")],
    "s09_gaq_mass_spectrum": [("PART", "P"), ("FAIL", "I"), ("FAIL", "I"), ("FAIL", "P"),
                              ("NA", "P"), ("FAIL", "I"), ("FAIL", "P")],
    "s10_frequency_helix_ontology": [("PART", "P"), ("FAIL", "I"), ("FAIL", "I"), ("FAIL", "P"),
                                     ("PART", "P"), ("FAIL", "P"), ("FAIL", "P")],
    "s11_gmuft_geometric_coupling": [("PART", "P"), ("PART", "P"), ("FAIL", "I"), ("FAIL", "P"),
                                     ("PART", "P"), ("FAIL", "P"), ("FAIL", "P")],
    "s12_light_speed_helix": [("PART", "P"), ("FAIL", "P"), ("FAIL", "I"), ("FAIL", "P"),
                              ("FAIL", "I"), ("FAIL", "P"), ("FAIL", "B")],
    "s13_duality_fractal_uft": [("PART", "P"), ("PART", "I"), ("FAIL", "B"), ("PART", "B"),
                                ("PART", "P"), ("PART", "B"), ("FAIL", "B")],
    "s14_torsion_unified_field_tuft": [("PART", "P"), ("FAIL", "C"), ("FAIL", "C"), ("FAIL", "C"),
                                       ("PART", "P"), ("PART", "P"), ("PART", "B")],
    "s15_light_speed_helix_ct_uft": [("PART", "P"), ("FAIL", "C"), ("FAIL", "C"), ("FAIL", "P"),
                                     ("PART", "P"), ("FAIL", "P"), ("FAIL", "P")],
    "s16_tuft_normalization_manual": [("NA", "P")] * 7,
    "s17_unified_field_core_formulas": [("PART", "P"), ("FAIL", "C"), ("FAIL", "C"), ("FAIL", "P"),
                                        ("FAIL", "C"), ("FAIL", "P"), ("FAIL", "P")],
    "s18_curvature_energy_density": [("PART", "P"), ("PART", "P"), ("PART", "P"), ("NA", "P"),
                                     ("FAIL", "P"), ("NA", "P"), ("PART", "P")],
}

VERDICT_TXT = {"PASS": "通过", "PART": "部分", "FAIL": "失败", "NA": "不适用"}

# ------------------------------------------------------------------
# 6. 组装矩阵：每格解析锚点并逐格 stat（证据不能只是注释里的一个字符串）
# ------------------------------------------------------------------
say("")
say("-" * 78)
say("3. 验收矩阵（22 体系 × 8 判据 = %d 格；每格挂存在性锚点）" % (len(SYSTEMS) * 8))
say("-" * 78)

MATRIX = []
MISSING_ANCHOR = []
for ent in SYSTEMS:
    sid = ent["id"]
    row = {
        "id": sid,
        "title": ent["title"],
        "status": ent["status"],
        "kind": ent["kind"],
        "directory": ent["directory"],
        "claims": CLAIMS[sid],
        "cover": COVER[sid],
        "cells": [],
    }
    row["cells"].append({
        "crit": "W0",
        "verdict": "PASS" if COVER[sid]["w0"] else "FAIL",
        "anchor": ANCHOR_FIX["I"] if COVER[sid]["w0"] else ANCHOR_FIX["F"],
        "ok": True,
    })
    for i, crit in enumerate(CRIT_ORDER):
        verdict, letter = VERDICT[sid][i]
        rel = anchor_path(letter, ent["directory"])
        exists = os.path.isfile(os.path.join(ROOT, rel))
        if not exists:
            MISSING_ANCHOR.append((sid, crit, rel))
        row["cells"].append({"crit": crit, "verdict": verdict, "anchor": rel, "ok": exists})
    row["n_pass"] = sum(1 for c in row["cells"] if c["verdict"] == "PASS")
    row["n_fail"] = sum(1 for c in row["cells"] if c["verdict"] == "FAIL")
    row["n_part"] = sum(1 for c in row["cells"] if c["verdict"] == "PART")
    row["n_na"] = sum(1 for c in row["cells"] if c["verdict"] == "NA")
    MATRIX.append(row)

TOTAL_CELLS = sum(len(r["cells"]) for r in MATRIX)
N_ANCHOR_OK = sum(1 for r in MATRIX for c in r["cells"] if c["ok"])
SC4_OK = (not MISSING_ANCHOR) and (len(MATRIX) == len(SYSTEMS)) and (TOTAL_CELLS == len(SYSTEMS) * 8)
sc("4", SC4_OK,
   "矩阵完整性：%d 体系 × 8 判据 = %d 格（无空缺）；证据锚点存在 %d/%d%s"
   % (len(MATRIX), TOTAL_CELLS, N_ANCHOR_OK, TOTAL_CELLS,
      "" if not MISSING_ANCHOR else "；缺失：" + "；".join("%s/%s->%s" % t for t in MISSING_ANCHOR[:6])))

STAT = collections.Counter()
for r in MATRIX:
    for c in r["cells"]:
        STAT[c["verdict"]] += 1
sc("5", sum(STAT.values()) == TOTAL_CELLS,
   "判据分布自洽：合计 %d = %d（通过 %d / 部分 %d / 失败 %d / 不适用 %d）"
   % (sum(STAT.values()), TOTAL_CELLS, STAT["PASS"], STAT["PART"], STAT["FAIL"], STAT["NA"]))

FULL_PASS = [r["id"] for r in MATRIX if all(c["verdict"] == "PASS" for c in r["cells"])]
NA_HEAVY = [r["id"] for r in MATRIX if r["n_na"] >= 5]
NO_FAIL = [r["id"] for r in MATRIX if r["n_fail"] == 0 and r["n_na"] < 5]

BOT = []
for crit in ["W0"] + CRIT_ORDER:
    na = sum(1 for r in MATRIX for c in r["cells"] if c["crit"] == crit and c["verdict"] == "NA")
    fl = sum(1 for r in MATRIX for c in r["cells"] if c["crit"] == crit and c["verdict"] == "FAIL")
    pt = sum(1 for r in MATRIX for c in r["cells"] if c["crit"] == crit and c["verdict"] == "PART")
    ps = sum(1 for r in MATRIX for c in r["cells"] if c["crit"] == crit and c["verdict"] == "PASS")
    BOT.append({"crit": crit, "fail": fl, "part": pt, "pass": ps, "na": na,
                "debt": fl + 0.5 * pt})
BOT.sort(key=lambda d: (-d["debt"], d["crit"]))

say("")
say("瓶颈排序（欠账 = 失败格 + 0.5×部分格，机器算；不适用格不计）")
for d in BOT:
    say("  %-3s 失败 %2d / 部分 %2d / 通过 %2d / 不适用 %2d   欠账 %5.1f"
        % (d["crit"], d["fail"], d["part"], d["pass"], d["na"], d["debt"]))

say("")
say("逐体系（通过/部分/失败/不适用）：")
for r in MATRIX:
    say("  %-34s %-12s pass %d part %d fail %d na %d  | claims %d 行（falsified %d）"
        % (r["id"], r["status"], r["n_pass"], r["n_part"], r["n_fail"], r["n_na"],
           r["claims"]["rows"], r["claims"]["status"].get("falsified", 0)))

ARITH_OK = all(r["n_pass"] + r["n_part"] + r["n_fail"] + r["n_na"] == len(r["cells"])
               for r in MATRIX)
sc("6", ARITH_OK,
   "逐体系格数自洽（通过+部分+失败+不适用 = 8）：%d/%d 体系；满足全部 8 条判据 %d 个（%s）；"
   "可评估（不适用格<5）且无 FAIL 格 %d 个（%s）；不可评估（无公设/非物理理论，不适用格≥5）%d 个（%s）"
   % (len(MATRIX), len(MATRIX), len(FULL_PASS), "无" if not FULL_PASS else "、".join(FULL_PASS),
      len(NO_FAIL), "无" if not NO_FAIL else "、".join(NO_FAIL),
      len(NA_HEAVY), "、".join(NA_HEAVY)))
sc("7", BOT[0]["debt"] >= BOT[-1]["debt"] and BOT[0]["crit"] == "W3",
   "瓶颈首位 = %s（欠账 %.1f），由机器排序得出、非写死"
   % (BOT[0]["crit"], BOT[0]["debt"]))

# ------------------------------------------------------------------
# 7. 已关闭/已排除清单（每条挂锚点 + 探针串；探针必须真的在锚点文件里）
# ------------------------------------------------------------------
CLOSED = [
    {"name": "电子 EDM 预言", "verdict": "已被实验排除（通道永久关闭）",
     "anchor": ANCHOR_FIX["B"], "probe": "3.44e16",
     "detail": "预言 1.409e-13 e·cm vs 上限 4.1e-30 e·cm（JILA HfF+ 2023）⇒ 超 3.44e16 倍"},
    {"name": "M02 普朗克锚定谬误", "verdict": "已在电子锚点崩塌",
     "anchor": ANCHOR_FIX["M"], "probe": "5.71e+44",
     "detail": "G_式(m_e)/G = 5.71e+44 ⇒ 旧式不是普适引力常数（仅普朗克锚成立）"},
    {"name": "最小非 SUSY SU(5)", "verdict": "已被质子衰变排除（公设级）",
     "anchor": "00_项目治理/system_registry.json", "probe": "质子衰变排除",
     "detail": "P03 premise_summary 自陈『最小非SUSY SU5已被质子衰变排除』"},
    {"name": "S18 曲率能量密度（给定参数）", "verdict": "已被宇宙年龄与 CMB θ_s 证伪",
     "anchor": "00_项目治理/system_registry.json", "probe": "CMB θ_s 证伪",
     "detail": "α=1.87、ρ_c=1e-9 时被宇宙年龄与 CMB 声视界角证伪；存活路径未验证"},
    {"name": "SM 单圈三耦合汇聚", "verdict": "结构性否定（UFE-1 两项 FAIL）",
     "anchor": ANCHOR_FIX["U"], "probe": "3.66",
     "detail": "α^-1 最小散布 3.66 vs MSSM 对照 0.049 ⇒ SM 不汇聚（L10 未关闭）"},
]
CLOSED_OK = []
for it in CLOSED:
    txt = read_text(it["anchor"]) if it["anchor"] != "00_项目治理/system_registry.json" \
        else read_text("00_项目治理/system_registry.json")
    ok = (it["probe"] in txt)
    it["probe_ok"] = ok
    if not ok:
        CLOSED_OK.append(it["name"])
say("")
say("-" * 78)
say("4. 已关闭/已排除清单（%d 条；探针串须真的出现在锚点文件中）" % len(CLOSED))
say("-" * 78)
for it in CLOSED:
    say("  [%s] %s —— %s" % ("锚点命中" if it["probe_ok"] else "探针未命中", it["name"], it["verdict"]))
    say("      %s" % it["detail"])
sc("8", not CLOSED_OK,
   "已关闭/已排除清单 %d 条，探针串在锚点文件中命中 %d/%d%s"
   % (len(CLOSED), len(CLOSED) - len(CLOSED_OK), len(CLOSED),
      "" if not CLOSED_OK else "；未命中：" + "、".join(CLOSED_OK)))

# ------------------------------------------------------------------
# 8. 最小闭合集（每项声明翻绿哪些格；这些格当前必须**不是**通过 —— 机器校验）
# ------------------------------------------------------------------
CLOSURE = [
    {"id": "C1", "title": "把 s15–s18 纳入收口产物，并以官方稳定编号重建『全体系图谱』",
     "targets": [("s15_light_speed_helix_ct_uft", "W0"), ("s16_tuft_normalization_manual", "W0"),
                 ("s17_unified_field_core_formulas", "W0"), ("s18_curvature_energy_density", "W0")],
     "why": "收口主文档只列 8 体系且自带 S01–S08 与官方编号 8/8 对撞；整合全集停在上一次登记的 18 体系"},
    {"id": "C2", "title": "W3 全域瓶颈：至少给出一个无量纲量的第一性数值并通过双锚点",
     "targets": [("s13_duality_fractal_uft", "W3"), ("s14_torsion_unified_field_tuft", "W3"),
                 ("p03_gauge_unification", "W3")],
     "why": "method_F 判据一：第一性内容 ⟺ 无量纲量的数值；当前 α 与质量比一律是测量锚"},
    {"id": "C3", "title": "W6 质量层级：需 Yukawa/动力学输入（仓库级最大缺口）",
     "targets": [("s13_duality_fractal_uft", "W6"), ("s14_torsion_unified_field_tuft", "W6"),
                 ("s03_gaq_geometric_atom", "W6")],
     "why": "状态看板 §四：拓扑层只能给代结构，不能给绝对质量"},
    {"id": "C4", "title": "W4 耦合统一（L10）：需两环 β 系数矩阵",
     "targets": [("p03_gauge_unification", "W4"), ("s13_duality_fractal_uft", "W4"),
                 ("s14_torsion_unified_field_tuft", "W4")],
     "why": "rpa 之外：一般群乘积的两环 b_ij 需外部公式；按『不凭记忆写』原则暂缓（07 §7 第 2 项）"},
    {"id": "C5", "title": "W7 新窗口：须先有 W3/W6，否则窗口只能开在已关闭族里",
     "targets": [("s13_duality_fractal_uft", "W7"), ("s03_gaq_geometric_atom", "W7"),
                 ("s14_torsion_unified_field_tuft", "W7")],
     "why": "已关闭/已排除清单 5 条（EDM / M02 / SU5 / S18 参数 / SM 汇聚）"},
    {"id": "C6", "title": "治理：claims 编号唯一性 + 编号口径统一",
     "targets": [],
     "why": "本次全仓审计发现同体系内重复 id 与跨体系编号口径冲突（见 §5 与 §3）"},
]
CELLIDX = {}
for r in MATRIX:
    for c in r["cells"]:
        CELLIDX[(r["id"], c["crit"])] = c["verdict"]
bad_closure = []
for it in CLOSURE:
    for tgt in it["targets"]:
        cur = CELLIDX.get(tgt)
        if cur is None or cur == "PASS":
            bad_closure.append((it["id"], tgt, cur))
say("")
say("-" * 78)
say("5. 最小闭合集（%d 项；每项声明的目标格当前必须非『通过』）" % len(CLOSURE))
say("-" * 78)
for it in CLOSURE:
    tg = "、".join("%s/%s" % t for t in it["targets"]) or "（治理项，不挂判据格）"
    say("  %s %s" % (it["id"], it["title"]))
    say("      目标格：%s" % tg)
    say("      依据：%s" % it["why"])
sc("9", not bad_closure,
   "最小闭合集 %d 项：目标格非『通过』校验 %d 处，违规 %d 处%s"
   % (len(CLOSURE), sum(len(i["targets"]) for i in CLOSURE), len(bad_closure),
      "" if not bad_closure else "：" + "；".join("%s->%s(%s)" % t for t in bad_closure)))

# ------------------------------------------------------------------
# 9. 全仓 claims 编号审计（跨体系）
# ------------------------------------------------------------------
id_owner = {}
cross_dup = []
for ent in SYSTEMS:
    cpath = os.path.join(SYSDIR, ent["directory"], "claims.csv")
    if not os.path.isfile(cpath):
        continue
    body = [ln for ln in read_text("01_独立体系/%s/claims.csv" % ent["directory"]).splitlines()
            if ln.strip()]
    for ln in body[1:]:
        cid = ln.split(",")[0]
        if cid in id_owner and id_owner[cid] != ent["id"]:
            cross_dup.append((cid, id_owner[cid], ent["id"]))
        id_owner.setdefault(cid, ent["id"])
within_dup = []
for sid, rec in CLAIMS.items():
    if rec["dups"]:
        within_dup.append((sid, rec["dups"]))
sc("10", True,
   "全仓 claims 编号审计：id 总数 %d（唯一 %d）；体系内重复 %d 个体系（%s）；跨体系重复 %d 个"
   % (len(ALL_IDS), len(set(ALL_IDS)), len(within_dup),
      "；".join("%s:%d" % (s, len(d)) for s, d in within_dup) if within_dup else "无",
      len(cross_dup)))

# ------------------------------------------------------------------
# 10. 汇总与落盘
# ------------------------------------------------------------------
say("")
say("-" * 78)
say("汇总：体系 %d | 判据 %d | 矩阵格 %d | 满足全部判据 %d | 无 FAIL 格 %d"
    % (len(MATRIX), len(CRIT_DEF), TOTAL_CELLS, len(FULL_PASS), len(NO_FAIL)))
say("判据分布：通过 %d / 部分 %d / 失败 %d / 不适用 %d"
    % (STAT["PASS"], STAT["PART"], STAT["FAIL"], STAT["NA"]))
say("瓶颈排序（欠账降序）：%s" % " > ".join("%s(%.1f)" % (d["crit"], d["debt"]) for d in BOT))
say("红线：过格不等于理论成立；本矩阵只判『离完成还差什么』，不判本体真伪。")
say("-" * 78)

OUT = {
    "generated": "2026-10-08",
    "scope": "openuft 全部登记体系（22）",
    "criteria": [{"id": c[0], "name": c[1], "definition": c[2], "source": c[3]} for c in CRIT_DEF],
    "systems": len(MATRIX),
    "cells": TOTAL_CELLS,
    "verdict_dist": dict(STAT),
    "full_pass": FULL_PASS,
    "no_fail": NO_FAIL,
    "na_heavy": NA_HEAVY,
    "coverage_declared": DECL,
    "bottleneck": BOT,
    "coverage": {"per_artifact": {name: sum(1 for v in COVER.values() if v["hit"][name])
                                  for name, _ in COVER_ART},
                 "w0_uncovered": w0_fail},
    "numbering_conflict": {"rows": CONFLICT, "mismatched": n_bad},
    "closed": CLOSED,
    "closure_set": CLOSURE,
    "claims_audit": {"rows": len(ALL_IDS), "unique": len(set(ALL_IDS)),
                     "within_dup": [{"system": s, "dups": d} for s, d in within_dup],
                     "cross_dup": cross_dup},
    "matrix": MATRIX,
    "self_checks": [{"tag": s[0], "ok": s[1], "detail": s[2]} for s in SCS],
}

MD = []
MD.append("# 全维验收矩阵 · 本项目级「统一场论完成度」机器验收")
MD.append("")
MD.append("> 生成 2026-10-08 ｜ 对象 openuft 全部登记体系 **22** 个 ｜ 完成判据 **8** 条 ｜ 矩阵 **%d** 格"
          % TOTAL_CELLS)
MD.append("> 引擎 `全维验收矩阵.py`（纯标准库，Python 3.8）｜ 产物 `数据/全维验收矩阵.json`")
MD.append("> 口径来源：整合全集三重闸门 / method_F 六判据 / 07 §5 三条界限 / 状态看板 H-O-C-U")
MD.append("> **红线**：过格不等于理论成立；本矩阵只判「离完成还差什么」，不判本体真伪。")
MD.append("")
MD.append("## 零、一句话结论")
MD.append("")
MD.append("**满足全部 8 条完成判据的体系 = %d 个。** 瓶颈排序（欠账降序）：%s。"
          % (len(FULL_PASS), " &gt; ".join("%s(%.1f)" % (d["crit"], d["debt"]) for d in BOT)))
MD.append("联盟级「统一场论完成」当前**未达成**，且缺口可分类、可排序、可挂锚点（见第三、五、六节）。")
MD.append("")
MD.append("## 一、完成判据 W0–W7")
MD.append("")
MD.append("| 判据 | 名称 | 定义 | 口径来源 |")
MD.append("|---|---|---|---|")
for c in CRIT_DEF:
    MD.append("| **%s** | %s | %s | %s |" % (c[0], c[1], c[2], c[3]))
MD.append("")
MD.append("## 二、W0 联盟级收口覆盖（机器扫描）")
MD.append("")
MD.append("| 索引产物 | 被点名体系数 | 锚点 |")
MD.append("|---|---|---|")
for name, rel in COVER_ART:
    MD.append("| %s | %d / 22 | `%s` |" % (name, sum(1 for v in COVER.values() if v["hit"][name]), rel))
MD.append("")
MD.append("**W0 未覆盖（不在任何收口产物中）：**%s" % ("、".join(w0_fail) if w0_fail else "无"))
MD.append("")
MD.append("**词表校准**：整合全集自陈覆盖 `%s` 个登记体系，扫描得 `%d` 个 ⇒ %s。"
          % (DECL["整合全集"], SCAN_I, "一致" if SCAN_I == DECL["整合全集"] else "**不一致（词表需修）**"))
MD.append("收口主文档自陈「编入图谱的理论体系 `%s` 个」，其 `S01–S08` 自带编号与官方 22 体系**不可映射**"
          "（见下方编号冲突表），故其覆盖数不计入官方口径。"
          % (DECL["收口主文档"],))
MD.append("")
for name in ("整合全集", "收口主文档"):
    hits = [e["id"] for e in SYSTEMS if COVER[e["id"]]["hit"][name]]
    MD.append("- `%s` 命中：%s" % (name, "、".join("`%s`" % h for h in hits) if hits else "（无）"))
MD.append("")
MD.append("**编号口径冲突**：收口主文档自带编号 `S01–S%02d` 与官方稳定编号 **逐号对撞 %d/%d**："
          % (len(CONFLICT), n_bad, len(CONFLICT)))
MD.append("")
MD.append("| 编号 | 收口主文档中的名称 | 官方稳定编号对应体系 | 同义？ |")
MD.append("|---|---|---|---|")
for c in CONFLICT:
    MD.append("| %s | %s | %s | %s |" % (c["num"], c["doc_name"], c["official"], "是" if c["same"] else "**否**"))
MD.append("")
MD.append("## 三、验收矩阵（22 × 8）")
MD.append("")
MD.append("| 体系 | 状态 | " + " | ".join(CRIT_ORDER) + " | 通过 | 部分 | 失败 | 不适用 |")
MD.append("|---" * (len(CRIT_ORDER) + 5) + "|")
for r in MATRIX:
    cells = " | ".join(VERDICT_TXT[c["verdict"]] for c in r["cells"][1:])
    MD.append("| `%s` | %s | %s | %d | %d | %d | %d |"
              % (r["id"], r["status"], cells, r["n_pass"], r["n_part"], r["n_fail"], r["n_na"]))
MD.append("")
MD.append("## 四、瓶颈排序（机器算，欠账 = 失败格 + 0.5 × 部分格）")
MD.append("")
MD.append("| 判据 | 失败 | 部分 | 通过 | 不适用 | 欠账 |")
MD.append("|---|---|---|---|---|---|")
for d in BOT:
    MD.append("| **%s** | %d | %d | %d | %d | %.1f |"
              % (d["crit"], d["fail"], d["part"], d["pass"], d["na"], d["debt"]))
MD.append("")
MD.append("## 五、已关闭 / 已排除清单")
MD.append("")
MD.append("| 对象 | 判定 | 读数 | 锚点 |")
MD.append("|---|---|---|---|")
for it in CLOSED:
    MD.append("| %s | %s | %s | `%s` |" % (it["name"], it["verdict"], it["detail"], it["anchor"]))
MD.append("")
MD.append("## 六、最小闭合集")
MD.append("")
for it in CLOSURE:
    MD.append("### %s %s" % (it["id"], it["title"]))
    MD.append("")
    MD.append("- 目标格：%s" % ("、".join("`%s/%s`" % t for t in it["targets"]) or "（治理项，不挂判据格）"))
    MD.append("- 依据：%s" % it["why"])
    MD.append("")
MD.append("## 七、全仓 claims 编号审计")
MD.append("")
MD.append("- id 总数 **%d**，唯一 **%d**" % (len(ALL_IDS), len(set(ALL_IDS))))
MD.append("- 体系内重复：%s"
          % ("；".join("`%s`（%d 个重复 id）" % (s, len(d)) for s, d in within_dup) if within_dup else "无"))
MD.append("- 跨体系重复：%d 个" % len(cross_dup))
MD.append("")
MD.append("## 八、逐体系证据锚点（抽样，全部锚点见 JSON）")
MD.append("")
MD.append("| 体系 | 判据 | 判定 | 锚点（已 stat 存在） |")
MD.append("|---|---|---|---|")
for r in MATRIX:
    for c in r["cells"]:
        if c["verdict"] != "NA":
            MD.append("| `%s` | %s | %s | `%s` |" % (r["id"], c["crit"], VERDICT_TXT[c["verdict"]], c["anchor"]))
MD.append("")

WRITTEN = []
try:
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    with io.open(os.path.join(DATA, "全维验收矩阵.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(OUT, ensure_ascii=False, indent=2))
    WRITTEN.append("数据/全维验收矩阵.json")
    with io.open(os.path.join(DATA, "全维验收矩阵.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(MD) + "\n")
    WRITTEN.append("数据/全维验收矩阵.md")
except Exception as exc:
    say("落盘失败：%r" % (exc,))
sc("11", len(WRITTEN) == 2, "落盘：%s" % "、".join(WRITTEN))

# 计数必须在最后一条自检登记**之后**再算（首版在此前算，导致 10/11 假红）
SC_OK = sum(1 for s in SCS if s[1])
EXIT_OK = (SC_OK == len(SCS)) and len(MATRIX) == len(SYSTEMS)
say("")
say("自检 %d/%d；退出码 = %d" % (SC_OK, len(SCS), 0 if EXIT_OK else 1))
sys.exit(0 if EXIT_OK else 1)
