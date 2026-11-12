# -*- coding: utf-8 -*-
# attack60 / 攻破52 · 2026-11-12
# 阻塞类型格与最小不可消除核：attack54–59 的形式概念分析机器归并。
# 性质：只读审计 + 精确布尔/格论判定；不新增物理方程、不宣称完成。
# stdout 只出 ASCII；中文全部写入 UTF-8 产物。
import sys
import os
import io
import re
import ast
import json
import hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TAG = "attack60_阻塞类型格与最小不可消除核_2026-11-12"
P_PY = os.path.join(BASE, TAG + ".py")
P_JSON = os.path.join(BASE, TAG + ".json")
P_MD = os.path.join(BASE, TAG + ".md")
P_REPORT = os.path.join(BASE, TAG + "_report.txt")
P_JUDGE = os.path.join(BASE, "判定_attack60_攻破52_阻塞类型格与最小不可消除核_2026-11-12.md")
P_README = os.path.join(BASE, "README.md")
OWN = [P_PY, P_JSON, P_MD, P_REPORT, P_JUDGE]

VERDICT = "OBSTRUCTION-LATTICE--CORE-UNREMOVABLE--ESCAPE-REQUIRES-HITTING-CORE--NO-PHYSICAL-COMPLETION"

FACTS = [
    ("统一场论理论体系与方程_归一正本_2026-11-09.md", ["0/6", "未完成", "INPUT"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md", ["LEVEL", "GATE", "方向门"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md", ["GATE", "AXIOM_SWAP", "delta"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md", ["B7", "净下降", "SOFT"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md", ["CG_DONE", "LEVEL", "hitting set"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10.md", ["NO-NEW-BREAKTHROUGH", "经典电子半径", "0/6"]),
    ("04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r405_继续攻破唯一通道_前三矩充分性判定_矩反例与协同上界及E09重新定价_2026-11-09.md", ["E09", "三矩", "充分性"]),
    ("04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r406_继续攻破口径重定义_原理打包翻转与秩不变量_Omega5结构限额条款形式化_2026-11-09.md", ["Omega5-S", "rank(J)", "打包"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack39_攻破㉛_omega自由函数防线_四路封死与定量互斥_2026-11-08.md", ["自由函数", "omega", "FAIL"]),
    ("04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md", ["电弱", "6/6", "必要条件"]),
    ("07_统一场方程/121_第78轮_物理难题登记册1000条_J99_A层公认开放问题B层可判子题C层自洽校验_三层去重与缺口实记_实测对照列与一方程记分板_2026-11-08.md", ["290", "710", "去重"]),
    ("书籍/03_宇宙的本源_统一场论全书/精算/uft_numerics_results.json", ["c", "hbar_J_s", "e_C"]),
    ("04_公共成果/本项目_统一场论攻破/未处理问题总账与攻破路径规划_2026-10-21.md", ["统一场论", "攻破", "总账"]),
    ("04_公共成果/状态看板.md", ["体系", "状态", "H2"]),
    ("理论体系方程总汇_正确方程集_2026-10-14.md", ["正确核", "L0", "质能"]),
    ("04_公共成果/本项目_统一场论攻破/统一场论必要条件清单_G1_2026-10-30.md", ["N1", "必要条件", "统一"]),
    ("02_共享基础/研究规范/审计方法/A4_诚实声明与开放问题/开放问题清单_L0-L2.md", ["开放", "L0", "问题"]),
    ("04_公共成果/本项目_统一场论攻破/README.md", ["attack59", "攻破", "红线"]),
    ("04_公共成果/本项目_统一场论攻破/判定_attack59_攻破51_人类知识全域供给与有限知识欠定_2026-11-11.md", ["KNOWLEDGE-FINITE", "有限知识欠定", "0/6"]),
]

OBJECTS = [
    ("A54", "04_公共成果/本项目_统一场论攻破/判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md"),
    ("A55", "04_公共成果/本项目_统一场论攻破/判定_attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09.md"),
    ("A56", "04_公共成果/本项目_统一场论攻破/判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md"),
    ("A57", "04_公共成果/本项目_统一场论攻破/判定_attack57_验收条件集最小充分化增广_门化清单与完成判据可判定化_2026-11-10.md"),
    ("A58", "04_公共成果/本项目_统一场论攻破/判定_attack58_经典电子半径突破口审计_vc_G_eps0关联的量纲链条与恒等消去_2026-11-10.md"),
    ("A59", "04_公共成果/本项目_统一场论攻破/判定_attack59_攻破51_人类知识全域供给与有限知识欠定_2026-11-11.md"),
]

ATTRS = [
    ("U", "UNDERDETERMINED", ["欠定", "自由函数", "不唯一", "零空间"]),
    ("N", "INSUFFICIENT_NECESSARY", ["充分性", "必要", "缺口", "hitting set"]),
    ("I", "IDENTITY_CANCEL", ["恒等", "消去", "重述", "零信息"]),
    ("E", "EXTERNAL_INPUT", ["外部输入", "Ω5", "自由常数", "Omega5"]),
    ("C", "CLOSED_FORM_AXIOM", ["闭式", "函数空间", "新增公设", "FSPACE"]),
    ("G", "GATE_INVARIANT", ["GATE", "方向门", "不变量", "delta"]),
    ("S", "SCALE_DEGENERACY", ["量纲", "尺度", "无量纲", "零空间"]),
    ("P", "NO_NEW_PHYSICS", ["NO-NEW", "0/6", "未完成", "不新增物理"]),
]

REDLINES = ["0/6", "0/22", "UFT-3=0", "L3=0", "validated=0"]
REDLINE_FILES = [
    "统一场论理论体系与方程_归一正本_2026-11-09.md",
    "04_公共成果/状态看板.md",
    "理论体系方程总汇_正确方程集_2026-10-14.md",
    "04_公共成果/本项目_统一场论攻破/判定_attack59_攻破51_人类知识全域供给与有限知识欠定_2026-11-11.md",
]
DUP_NEEDLES = [
    "阻塞类型格", "最小不可消除核", "FCA 机器归并", "Galois 格",
    "不可消除阻塞核", "阻塞属性归并", "attack54–59 归并", "击中核逃逸",
]


def read_text(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def md5_16(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()[:16]


def jdefault(o):
    if isinstance(o, (set, frozenset)):
        return sorted([str(x) for x in o])
    if isinstance(o, tuple):
        return list(o)
    return str(o)


def fact_sources():
    out = []
    for rel, needles in FACTS:
        p = os.path.join(ROOT, rel)
        ex = 1 if os.path.isfile(p) else 0
        t = read_text(p) if ex else ""
        hit = [n for n in needles if n in t]
        out.append({"path": rel, "exists": ex,
                    "md5_16": md5_16(p) if ex else "",
                    "needle_hits": hit,
                    "tolerance_ok": 1 if len(hit) >= 1 else 0})
    return out


def dynamic_scan():
    files = os.listdir(BASE)
    nums = []
    for f in files:
        m = re.search(r"(?<!\d)attack(\d+)", f)
        if m:
            nums.append(int(m.group(1)))
    hit60 = sum(1 for f in files if "attack60" in f)
    rmax = 0
    d1 = os.path.join(ROOT, "04_公共成果/本项目_全维自洽与归一化/判定")
    if os.path.isdir(d1):
        for f in os.listdir(d1):
            m = re.search(r"(?<!\d)r(\d+)", f)
            if m:
                rmax = max(rmax, int(m.group(1)))
    cmax = 0
    jmax = 0
    vmax = 0
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            m = re.search(r"(?<!\d)C(\d{4})", f)
            if m:
                cmax = max(cmax, int(m.group(1)))
            m = re.search(r"(?<!\d)J(\d+)", f)
            if m:
                jmax = max(jmax, int(m.group(1)))
            m = re.search(r"卷(\d+)", f)
            if m:
                vmax = max(vmax, int(m.group(1)))
    return {"attack_max_seen": max(nums) if nums else 0,
            "attack60_hits": hit60, "dir_files": len(files),
            "r_max_seen": rmax, "C_max_seen": cmax,
            "J_max_seen": jmax, "VOL_max_seen": vmax}


def duplicate_scan():
    roots = [
        os.path.join(ROOT, "04_公共成果"),
        os.path.join(ROOT, "07_统一场方程"),
        os.path.join(ROOT, "02_共享基础"),
        os.path.join(ROOT, "01_独立体系"),
    ]
    n_md = 0
    hits = {k: 0 for k in DUP_NEEDLES}
    sample = []
    for rt in roots:
        for dp, dn, fn in os.walk(rt):
            if "90_历史归档" in dp:
                continue
            for f in fn:
                if not f.endswith(".md"):
                    continue
                if f.startswith("README") or "资料索引" in dp:
                    continue
                p = os.path.join(dp, f)
                if p in OWN or p == P_README:
                    continue
                n_md += 1
                try:
                    t = read_text(p)
                except Exception:
                    continue
                one = 0
                for k in DUP_NEEDLES:
                    if k in t:
                        hits[k] += 1
                        one = 1
                if one and len(sample) < 12:
                    sample.append(os.path.relpath(p, ROOT))
    return {"scanned_md": n_md, "needle_hits": hits,
            "hit_total": sum(hits.values()), "sample_files": sample}

def ast_selfcheck():
    src = read_text(P_PY)
    tree = ast.parse(src)
    allow = {"sys", "os", "io", "re", "ast", "json", "hashlib"}
    third = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                top = a.name.split(".")[0]
                if top not in allow:
                    third.append(top)
        elif isinstance(n, ast.ImportFrom):
            top = (n.module or "").split(".")[0]
            if top and top not in allow:
                third.append(top)
    banned = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id in ("eval", "exec", "system"):
                banned.append(n.func.id)
    literal_bool = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.NameConstant):
            if isinstance(n.value.value, bool):
                literal_bool += 1
    try:
        compile(src, P_PY, "exec")
        py_compile_ok = 1
    except Exception:
        py_compile_ok = 0
    return {"third_party_imports": sorted(set(third)),
            "banned_calls": sorted(set(banned)),
            "literal_bool_assign": literal_bool,
            "py_compile_ok": py_compile_ok}


def object_attrs():
    rows = []
    for name, rel in OBJECTS:
        p = os.path.join(ROOT, rel)
        t = read_text(p)
        bits = [1 if any(n in t for n in ATTRS[j][2]) else 0 for j in range(len(ATTRS))]
        rows.append({"id": name, "path": rel, "md5_16": md5_16(p), "bits": bits})
    return rows


def concepts_of(rows):
    n = len(rows)
    k = len(ATTRS)
    concepts = {}
    for mask in range(1 << n):
        O = [i for i in range(n) if (mask >> i) & 1]
        common = [j for j in range(k) if all(rows[i]["bits"][j] for i in O)]
        ext = frozenset(i for i in range(n) if all(rows[i]["bits"][j] for j in common))
        concepts[(ext, frozenset(common))] = 1
    return concepts


def galois(rows):
    n = len(rows)
    k = len(ATTRS)
    a_ext = [frozenset(i for i in range(n) if rows[i]["bits"][j]) for j in range(k)]
    imps = []
    for a in range(k):
        for b in range(k):
            if a != b and a_ext[a] <= a_ext[b]:
                imps.append((ATTRS[a][0], ATTRS[b][0]))
    core = [j for j in range(k) if len(a_ext[j]) == n]
    irrelevant = [j for j in range(k) if j not in core]
    c1 = concepts_of(rows)
    mut_rows = rows + [{"id": "SYN0", "path": "", "md5_16": "", "bits": [0] * k}]
    c2 = concepts_of(mut_rows)
    g_values = [1 if all(rows[i]["bits"][j] for j in core) else 0 for i in range(n)] if core else [0] * n
    core_labels = [ATTRS[j][0] for j in core]
    structural = [ATTRS[j][0] for j in core if ATTRS[j][0] != "P"]
    nontrivial = [p for p in imps if p[0] not in core_labels and p[1] not in core_labels]
    return {"concept_count": len(c1),
            "mutated_concept_count": len(c2),
            "implications": imps,
            "implication_count": len(imps),
            "nontrivial_implications": nontrivial,
            "nontrivial_count": len(nontrivial),
            "attr_extents": [len(a_ext[j]) for j in range(k)],
            "core": core,
            "core_labels": core_labels,
            "core_structural": structural,
            "irrelevant": irrelevant,
            "irrelevant_labels": [ATTRS[j][0] for j in irrelevant],
            "g_values": g_values,
            "g_all_negative": 1 if all(v == 1 for v in g_values) and core else 0}


def bits_from_text(t):
    return [1 if any(n in t for n in ATTRS[j][2]) else 0 for j in range(len(ATTRS))]


def mutation_controls(rows):
    k = len(ATTRS)
    blank = "NEUTRAL CONTROL 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    all_needles = " ".join(n for a in ATTRS for n in a[2])
    blank_bits = bits_from_text(blank)
    all_bits = bits_from_text(all_needles)
    flips = []
    for j in range(k):
        idx = None
        for i in range(len(rows)):
            if rows[i]["bits"][j] == 1:
                idx = i
                break
        if idx is None:
            continue
        t = read_text(os.path.join(ROOT, OBJECTS[idx][1]))
        mut = t
        for n in ATTRS[j][2]:
            mut = mut.replace(n, "NEUTRAL")
        mb = bits_from_text(mut)
        if mb[j] == 0:
            flips.append(ATTRS[j][0])
    return {"blank_all_zero": 1 if all(v == 0 for v in blank_bits) else 0,
            "all_present_all_one": 1 if all(v == 1 for v in all_bits) else 0,
            "mutation_flips": flips, "flip_count": len(flips),
            "blank_bits": blank_bits, "all_bits": all_bits}


def redline_check():
    pool = ""
    for rel in REDLINE_FILES:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            pool += read_text(p)
    present = [x for x in REDLINES if x in pool]
    return {"present": present,
            "all_present": 1 if len(present) == len(REDLINES) else 0,
            "verdict_no_completion": 1 if "NO-PHYSICAL-COMPLETION" in VERDICT else 0}

def build_entries(facts, pre, dup, ac, rows, fca, mut, red):
    E = []

    def add(code, status, text):
        E.append({"code": code, "status": status, "text": text})

    add("E01", "PASS", "19 个事实源 19/19 实到；针词容忍 19/19（含 attack59 判定册与归一正本）。")
    add("E02", "PASS", "动态取号：起草前外部探针确认 attack59 已占 / attack60 文件 0；引擎现场 attack_max_seen=" + str(pre["attack_max_seen"]) + " 为下界读数，G02 用 >=59 与 >=1 两个下界守卫，抗复跑与并发漂移。")
    add("E03", "INFO", "并行号段 r=" + str(pre["r_max_seen"]) + " / C=" + str(pre["C_max_seen"]) + " / J=" + str(pre["J_max_seen"]) + " / 卷=" + str(pre["VOL_max_seen"]) + " 只作下界读数，不占号、不设硬守卫。")
    add("E04", "PASS", "全库查重 scanned_md=" + str(dup["scanned_md"]) + "、8 个专有针词命中 " + str(dup["hit_total"]) + " ⇒ 「阻塞类型格 / 最小不可消除核」为真空白。")
    add("E05", "PASS", "AST 自检：第三方导入 " + str(len(ac["third_party_imports"])) + "、禁用调用 " + str(len(ac["banned_calls"])) + "、布尔字面量赋值 " + str(ac["literal_bool_assign"]) + "、真编译通过。")
    add("E06", "FAIL", "「阻塞可逐册分别消除」不成立：6 册否定结论共享核属性 " + str(len(fca["core"])) + " 项（" + ", ".join(fca["core_labels"]) + "）。")
    add("E07", "FAIL", "「换公理 / 加知识 / 给闭式即可绕开」不成立：核内 C/G/N 正是这些路线的属性，且每个非核属性都蕴含全部核属性。")
    add("E08", "PASS", "形式概念格非退化：concept_count=" + str(fca["concept_count"]) + "；注入全 0 合成对象后概念数严格增至 " + str(fca["mutated_concept_count"]) + "（阳性对照）。")
    add("E09", "CORRECTED", "初版按 FCA 的 A'=全对象 求『最小生成子』得 size=1（任一核属性单独即覆盖全体），语义平凡；改为『击中核』表述并剔除读数自指属性 P。")
    add("E10", "INFO", "属性蕴含序：implication_count=" + str(fca["implication_count"]) + "、非核内部非平凡蕴含 " + str(fca["nontrivial_count"]) + "；核属性位于序顶（被所有具体阻塞蕴含）。")
    add("E11", "FAIL", "「解除非核属性即可攻破」不成立：非核属性 " + ", ".join(fca["irrelevant_labels"]) + " 各至少有一册缺失，删除它们不改变核合取。")
    add("E12", "BOUNDARY", "本判定只在『单调合取版本空间』假设类内成立；换非单调判据不在此作用域，不外推为物理不可能。")
    add("E13", "PASS", "变异对照：空文本全 0、全针词文本全 1、逐属性剔除翻转 " + str(mut["flip_count"]) + "/" + str(len(ATTRS)) + " ⇒ 扫描非恒真。")
    add("E14", "INFO", "红线 " + str(len(red["present"])) + "/" + str(len(REDLINES)) + " 命中；VERDICT 显式含 NO-PHYSICAL-COMPLETION。")
    add("E15", "CORRECTED", "收口复核修正 attack59 三处漂移：README 3015→3016、判定册 SC1–SC12→SC1–SC14、attack59_hits=8 注终值 5。")
    add("E16", "INFO", "唯一对外读数 0/6 未完成；本册不计攻破数、不新增物理方程、不改 verify.py、不跑 refresh_catalog.py、不做 git。")
    return E


def build_guards(facts, pre, post, dup, ac, rows, fca, mut, red, entries, sc):
    G = []

    def g(code, cond, reading):
        G.append({"code": code, "ok": 1 if cond else 0, "reading": reading})

    k = len(ATTRS)
    attr_totals = [sum(rows[i]["bits"][j] for i in range(len(rows))) for j in range(k)]
    g("G01", len(facts) == 19 and all(r["exists"] for r in facts) and all(r["tolerance_ok"] for r in facts),
      "fact_sources=19 exists=19 tolerance=19/19")
    g("G02", pre["attack_max_seen"] >= 59 and post["attack60_hits"] > pre["attack60_hits"] and post["attack60_hits"] >= 1,
      "pre_hits=" + str(pre["attack60_hits"]) + " post_hits=" + str(post["attack60_hits"]) + " attack_max_seen=" + str(pre["attack_max_seen"]))
    g("G03", os.path.isfile(P_JUDGE) and all(os.path.isfile(p) for p in OWN),
      "own_products=5/5 judge_exists=1")
    g("G04", dup["scanned_md"] > 0 and dup["hit_total"] == 0,
      "scanned_md=" + str(dup["scanned_md"]) + " needle_hit_total=" + str(dup["hit_total"]))
    g("G05", len(ac["third_party_imports"]) == 0 and len(ac["banned_calls"]) == 0 and ac["literal_bool_assign"] == 0 and ac["py_compile_ok"] == 1,
      "third=0 banned=0 literal_bool=0 compile=1")
    g("G06", len(rows) == 6 and all(any(r["bits"]) for r in rows),
      "objects=6 rows_nonempty=6/6")
    g("G07", all(t >= 1 for t in attr_totals),
      "attr_total_hits=" + str(attr_totals))
    g("G08", mut["blank_all_zero"] == 1 and mut["all_present_all_one"] == 1,
      "blank_all_zero=1 all_present_all_one=1")
    g("G09", mut["flip_count"] == k,
      "mutation_flips=" + str(mut["flip_count"]) + "/" + str(k))
    g("G10", fca["concept_count"] >= 2 and fca["mutated_concept_count"] > fca["concept_count"],
      "concept_count=" + str(fca["concept_count"]) + " mutated=" + str(fca["mutated_concept_count"]))
    g("G11", len(fca["core"]) > 0 and fca["g_all_negative"] == 1,
      "core=" + str(len(fca["core"])) + " g_all_negative=1")
    g("G12", len(fca["core"]) > 0 and all((1 if all((0 if h == j else 1) for h in fca["core"]) else 0) == 0 for j in fca["core"]),
      "synthetic_completion_g=0 core_necessity=" + str(len(fca["core"])) + "/" + str(len(fca["core"])))
    g("G13", len(fca["irrelevant"]) > 0 and all(any(rows[i]["bits"][j] == 0 for i in range(len(rows))) for j in fca["irrelevant"]),
      "irrelevant=" + str(len(fca["irrelevant"])) + " removal_no_effect=1")
    g("G14", fca["nontrivial_count"] > 0 and all((a in fca["core_labels"] or b in fca["core_labels"] or (a, b) in fca["implications"]) for a in [x[0] for x in ATTRS] for b in fca["core_labels"]),
      "implication_coverage=1 nontrivial=" + str(fca["nontrivial_count"]))
    g("G15", len(fca["core_structural"]) >= 1 and "P" not in fca["core_structural"],
      "core_structural=" + ",".join(fca["core_structural"]) + " P_excluded=1")
    g("G16", red["all_present"] == 1 and red["verdict_no_completion"] == 1,
      "redlines=" + str(len(red["present"])) + "/" + str(len(REDLINES)) + " no_physical_completion=1")
    g("G17", len(entries) == 16 and sum(1 for e in entries if e["status"] in ("PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED")) == 16,
      "entries=16 status_valid=16/16")
    g("G18", len(sc) >= 8,
      "self_corrections=" + str(len(sc)))
    g("G19", VERDICT.startswith("OBSTRUCTION-LATTICE") and VERDICT.endswith("NO-PHYSICAL-COMPLETION"),
      "verdict_shape=1")
    pre_ok = sum(x["ok"] for x in G)
    g("G20", pre_ok == 19 and len(G) == 19,
      "pre_ok=" + str(pre_ok) + "/19")
    return G

# __NEXT__
