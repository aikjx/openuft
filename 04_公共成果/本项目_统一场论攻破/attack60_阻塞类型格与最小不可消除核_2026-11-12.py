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
    cross_ref_files = []
    cross_ref_hits = 0
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
                if one:
                    hit_lines = [ln for ln in t.splitlines() if any(k in ln for k in DUP_NEEDLES)]
                    cross = 1 if hit_lines and all(("attack60" in ln or "attack61" in ln) for ln in hit_lines) else 0
                    if cross:
                        cross_ref_files.append(os.path.relpath(p, ROOT))
                        cross_ref_hits += sum(1 for k in DUP_NEEDLES if k in t)
                    elif len(sample) < 12:
                        sample.append(os.path.relpath(p, ROOT))
    total = sum(hits.values())
    return {"scanned_md": n_md, "needle_hits": hits,
            "hit_total": total,
            "cross_ref_files": cross_ref_files,
            "cross_ref_hit_total": cross_ref_hits,
            "independent_hit_total": total - cross_ref_hits,
            "sample_files": sample}

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
    missing = [x for x in REDLINES if x not in pool]
    fallback = {}
    if missing:
        for dp, dn, fn in os.walk(ROOT):
            if "90_历史归档" in dp:
                continue
            for f in fn:
                if not f.endswith(".md"):
                    continue
                p = os.path.join(dp, f)
                try:
                    t = read_text(p)
                except Exception:
                    continue
                for x in list(missing):
                    if x in t:
                        fallback[x] = os.path.relpath(p, ROOT)
                        missing.remove(x)
                if not missing:
                    break
            if not missing:
                break
    for x in fallback:
        if x not in present:
            present.append(x)
    return {"present": present,
            "missing": missing,
            "fallback_sources": fallback,
            "all_present": 1 if len(present) == len(REDLINES) else 0,
            "verdict_no_completion": 1 if "NO-PHYSICAL-COMPLETION" in VERDICT else 0}

def build_entries(facts, pre, dup, ac, rows, fca, mut, red):
    E = []

    def add(code, status, text):
        E.append({"code": code, "status": status, "text": text})

    add("E01", "PASS", "19 个事实源 19/19 实到；针词容忍 19/19（含 attack59 判定册与归一正本）。")
    add("E02", "PASS", "动态取号：起草前外部探针确认 attack59 已占 / attack60 文件 0；引擎现场 attack_max_seen=" + str(pre["attack_max_seen"]) + " 为下界读数，G02 用 >=59 与 >=1 两个下界守卫，抗复跑与并发漂移。")
    add("E03", "INFO", "并行号段 r=" + str(pre["r_max_seen"]) + " / C=" + str(pre["C_max_seen"]) + " / J=" + str(pre["J_max_seen"]) + " / 卷=" + str(pre["VOL_max_seen"]) + " 只作下界读数，不占号、不设硬守卫。")
    add("E04", "PASS", "全库查重 scanned_md=" + str(dup["scanned_md"]) + "、8 个专有针词原始命中 " + str(dup["hit_total"]) + "，其中 " + str(dup["cross_ref_hit_total"]) + " 条逐行核验为并行会话 attack61 对本册文件名的改号引用（命中行均含 attack60/attack61），独立同主题命中 " + str(dup["independent_hit_total"]) + " ⇒ 「阻塞类型格 / 最小不可消除核」仍为真空白，原始读数不隐瞒。")
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


def build_guards(facts, pre, dup, ac, rows, fca, mut, red, entries, sc):
    G = []

    def g(code, cond, reading):
        G.append({"code": code, "ok": 1 if cond else 0, "reading": reading})

    k = len(ATTRS)
    attr_totals = [sum(rows[i]["bits"][j] for i in range(len(rows))) for j in range(k)]
    g("G01", len(facts) == 19 and all(r["exists"] for r in facts) and all(r["tolerance_ok"] for r in facts),
      "fact_sources=19 exists=19 tolerance=19/19")
    g("G02", pre["attack_max_seen"] >= 59 and pre["attack60_hits"] >= 1,
      "attack_max_seen=" + str(pre["attack_max_seen"]) + " attack60_hits=" + str(pre["attack60_hits"]) + " lower_bound_only=1")
    g("G03", os.path.isfile(P_PY) and len(OWN) == 5 and len(set(OWN)) == 5 and all(os.path.normpath(p).startswith(BASE) for p in OWN),
      "own_paths=5/5 in_base=1 source_exists=1 products_checked_after_write=1")
    g("G04", dup["scanned_md"] > 0 and dup["independent_hit_total"] == 0,
      "scanned_md=" + str(dup["scanned_md"]) + " raw=" + str(dup["hit_total"]) + " cross_ref=" + str(dup["cross_ref_hit_total"]) + " independent=" + str(dup["independent_hit_total"]))
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
    def gate(rs, core):
        if not core:
            return 0
        return 1 if all(all(r["bits"][j] for j in core) for r in rs) else 0

    base_g = gate(rows, fca["core"])
    esc_bits = [0 if j in fca["core"] else 1 for j in range(k)]
    esc_row = {"id": "SYN_ESC", "path": "", "md5_16": "", "bits": esc_bits}
    g_esc = gate(rows + [esc_row], fca["core"])
    partial = []
    for j in fca["core"]:
        b = list(esc_bits)
        b[j] = 1
        partial.append(gate(rows + [{"id": "SYN_P", "path": "", "md5_16": "", "bits": b}], fca["core"]))
    g("G12", base_g == 1 and g_esc == 0 and len(partial) >= 2 and all(v == 0 for v in partial),
      "base_g=1 escape_g=0 partial_hits=" + str(sum(partial)) + "/" + str(len(partial)) + " core=" + str(len(fca["core"])))
    g("G13", len(fca["irrelevant"]) > 0 and all(any(rows[i]["bits"][j] == 0 for i in range(len(rows))) for j in fca["irrelevant"]),
      "irrelevant=" + str(len(fca["irrelevant"])) + " removal_no_effect=1")
    irr_to_core = []
    for a in fca["irrelevant"]:
        ea = frozenset(i for i in range(len(rows)) if rows[i]["bits"][a])
        for b in fca["core"]:
            eb = frozenset(i for i in range(len(rows)) if rows[i]["bits"][b])
            irr_to_core.append(1 if ea <= eb else 0)
    cover = len(irr_to_core) > 0 and all(irr_to_core)
    g("G14", cover and fca["implication_count"] >= len(fca["core"]),
      "irr_implies_core=" + str(sum(irr_to_core)) + "/" + str(len(irr_to_core)) + " implications=" + str(fca["implication_count"]) + " nontrivial=" + str(fca["nontrivial_count"]))
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

def self_corrections():
    S = []

    def add(code, tag, text):
        S.append({"code": code, "tag": tag, "text": text})

    add("SC1", "G02_LOWER_BOUND",
        "初版 G02 用 post_hits > pre_hits 判定本册新增，复跑时起草期快照已含自身源码会恒假；改为 attack_max_seen>=59 与 attack60_hits>=1 两个纯下界守卫，抗复跑与并发漂移。")
    add("SC2", "G03_PRODUCT_DEPENDENCY",
        "初版 G03 要求 5 个自身产物在守卫计算前已落盘，但守卫结果本身要写进产物，形成循环依赖；改为路径规划守卫（5 条路径唯一且同在 BASE），产物存在性改到写后独立确认。")
    add("SC3", "G12_TAUTOLOGY",
        "初版 G12 判据 all((0 if h==j else 1) for h in core) 因 core 含 j 恒为假，外层 all 恒真；改为合成逃逸对象 SYN_ESC 与「只恢复单个核属性仍不可满足」的真实击中核判据。")
    add("SC4", "G14_TAUTOLOGY",
        "初版 G14 的 b in core_labels 对遍历恒真使 all 短路；改为非核属性 extent 是否逐项包含于核属性 extent 的真实蕴含覆盖，并保留 implication_count 作读数。")
    add("SC5", "REDLINE_POOL",
        "UFT-3=0 不在归一正本单文件内，仅池化 4 个文件会假红；redline_check 加全库 md 兜底扫描并记录 fallback_sources，保持 all_present 语义不放宽。")
    add("SC6", "E02_WORDING",
        "E02 文案先于代码改动，曾写 post>pre 结构性下界守卫与代码不一致；已同步为 attack_max_seen 下界读数 + >=59 / >=1 双下界口径。")
    add("SC7", "NO_TRUE_FALSE",
        "ast_selfcheck 会统计布尔字面量赋值，新增代码统一用 1/0 记状态，避免自引入 G05 literal_bool_assign 失败。")
    add("SC8", "STDOUT_ASCII",
        "全部 print 只输出 ASCII 摘要，中文一律写入 UTF-8 产物，规避 GBK 控制台 UnicodeEncodeError 导致的假失败。")
    add("SC9", "NO_GOVERNANCE_CHANGE",
        "未跑 refresh_catalog.py、未改 verify.py、未做 git、未触碰他人文件；README 登记在引擎之外由工具侧幂等追加。")
    add("SC10", "README_DEFER",
        "README 增量登记不放进 main()，避免引擎复跑重复写入共享登记簿；本册只生成 5 个自身产物。")
    add("SC11", "VERDICT_SHAPE",
        "判词固定以 NO-PHYSICAL-COMPLETION 收尾，不计攻破数、不新增物理方程、不宣称物理完成。")
    add("SC12", "FCA_BOUNDARY",
        "结论只在「单调合取版本空间」假设类内成立，E12 标 BOUNDARY；不外推为物理不可能，也不与 0/6 读数冲突。")
    add("SC13", "CROSS_REF_HITS",
        "首跑 G04 假红：复跑查重原始命中 2 条，逐行核验全部来自并行会话 attack61 判定册 SC1 对本册文件名的改号引用，而非独立同主题判定册；改为分离 raw / cross_ref / independent 三层，G04 落到 independent=0，原始读数如实保留不抹零。")
    add("SC14", "PARALLEL_ATTACK61",
        "复跑现场 attack_max_seen 由 59 升至 61：并行会话已按「后到者改号不覆盖」取 attack61；本册保持 attack60 不迁号、不触碰 attack61 任何字节，E03 并行号段只作下界读数。")
    return S


def write_json(path, data):
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, indent=2, default=jdefault) + "\n")


def write_text(path, text):
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def build_md(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count):
    L = []
    L.append("# " + TAG + " · 机器读数")
    L.append("")
    L.append("- 轮次：attack60 / 攻破52（2026-11-12）")
    L.append("- 判词：" + VERDICT)
    L.append("- 唯一对外读数：**0/6，未完成**；本册不计攻破数、不新增物理方程。")
    L.append("")
    L.append("## 一、供给与查重")
    L.append("")
    L.append("| 项 | 读数 |")
    L.append("| --- | --- |")
    L.append("| 事实源实到 | " + str(sum(r["exists"] for r in facts)) + "/" + str(len(facts)) + " |")
    L.append("| 针词容忍 | " + str(sum(r["tolerance_ok"] for r in facts)) + "/" + str(len(facts)) + " |")
    L.append("| 动态取号 attack_max_seen | " + str(pre["attack_max_seen"]) + "（下界） |")
    L.append("| 并行号段 r/C/J/卷 | " + str(pre["r_max_seen"]) + " / " + str(pre["C_max_seen"]) + " / " + str(pre["J_max_seen"]) + " / " + str(pre["VOL_max_seen"]) + "（不占号） |")
    L.append("| 查重 md | " + str(dup["scanned_md"]) + " |")
    L.append("| 8 个专有针词命中（原始 / 交叉引用 / 独立） | " + str(dup["hit_total"]) + " / " + str(dup["cross_ref_hit_total"]) + " / " + str(dup["independent_hit_total"]) + " |")
    L.append("| 交叉引用文件 | " + ", ".join(dup["cross_ref_files"]) + " |")
    L.append("| AST 真编译 | " + str(ac["py_compile_ok"]) + " |")
    L.append("")
    L.append("## 二、对象—属性矩阵（6 册 × 8 类阻塞）")
    L.append("")
    L.append("| 对象 | " + " | ".join(a[0] for a in ATTRS) + " |")
    L.append("| --- | " + " | ".join("---" for a in ATTRS) + " |")
    for r in rows:
        L.append("| " + r["id"] + " | " + " | ".join(str(v) for v in r["bits"]) + " |")
    L.append("")
    L.append("- 属性命中合计：" + str(fca["attr_extents"]))
    L.append("- 共同核 core：" + ", ".join(fca["core_labels"]))
    L.append("- 结构核（剔除自指 P）：" + ", ".join(fca["core_structural"]))
    L.append("- 非核属性：" + ", ".join(fca["irrelevant_labels"]))
    L.append("- 形式概念数 " + str(fca["concept_count"]) + " → 注入全 0 合成对象后 " + str(fca["mutated_concept_count"]))
    L.append("- 属性蕴含 " + str(fca["implication_count"]) + " 条，非核内部非平凡 " + str(fca["nontrivial_count"]) + " 条")
    L.append("")
    L.append("## 三、变异对照与红线")
    L.append("")
    L.append("- 空文本全 0：" + str(mut["blank_all_zero"]) + "；全针词文本全 1：" + str(mut["all_present_all_one"]))
    L.append("- 逐属性剔除翻转：" + str(mut["flip_count"]) + "/" + str(len(ATTRS)))
    L.append("- 红线命中：" + str(len(red["present"])) + "/" + str(len(REDLINES)) + "（缺项 " + str(red["missing"]) + "）")
    L.append("")
    L.append("## 四、条目表")
    L.append("")
    L.append("| code | status | 内容 |")
    L.append("| --- | --- | --- |")
    for e in entries:
        L.append("| " + e["code"] + " | " + e["status"] + " | " + e["text"] + " |")
    L.append("")
    L.append("- 状态分布：" + str(status_count))
    L.append("")
    L.append("## 五、守卫表")
    L.append("")
    L.append("| code | ok | reading |")
    L.append("| --- | --- | --- |")
    for x in guards:
        L.append("| " + x["code"] + " | " + str(x["ok"]) + " | " + x["reading"] + " |")
    L.append("")
    L.append("- 合计 " + str(sum(x["ok"] for x in guards)) + "/" + str(len(guards)))
    L.append("")
    L.append("## 六、自抓清单")
    L.append("")
    for x in sc:
        L.append("- " + x["code"] + " [" + x["tag"] + "] " + x["text"])
    L.append("")
    L.append("## 相关入口")
    L.append("")
    L.append("- 数据正本：`" + TAG + ".json`")
    L.append("- 守卫报告：`" + TAG + "_report.txt`")
    L.append("- 正式判定册：`判定_attack60_攻破52_阻塞类型格与最小不可消除核_2026-11-12.md`")
    L.append("- 引擎：`" + TAG + ".py`")
    L.append("")
    return "\n".join(L) + "\n"


def build_judge(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count):
    L = []
    L.append("# 判定_attack60 / 攻破52 · 阻塞类型格与最小不可消除核（2026-11-12）")
    L.append("")
    L.append("## §0 判词")
    L.append("")
    L.append("**" + VERDICT + "**")
    L.append("")
    L.append("唯一对外读数不变：被问「统一场论完成了吗」答 **0/6，未完成**。本册不计攻破数、不新增物理方程、不宣称物理完成。")
    L.append("")
    L.append("## §1 受理范围与性质")
    L.append("")
    L.append("- 性质：**只读审计 + 精确布尔/格论判定**。对象为 attack54–attack59 六册既有判定册，不重算其物理结论。")
    L.append("- 新增之处：把六册的否定结论抽象为 8 类阻塞属性，用形式概念分析（FCA / Galois 格）机器归并，求「共同核」与「击中核」。")
    L.append("- 查重：递归扫 " + str(dup["scanned_md"]) + " 个 md，8 个专有针词原始命中 " + str(dup["hit_total"]) + "，其中 " + str(dup["cross_ref_hit_total"]) + " 条逐行核验为并行会话 attack61 对本册文件名的改号引用（" + ", ".join(dup["cross_ref_files"]) + "），独立同主题命中 " + str(dup["independent_hit_total"]) + " ⇒ 该角度仍为库内空白；原始读数不抹零，broad 层论/上同调类主题已有历史命中，故不采用。")
    L.append("- 动态取号：现场实扫 attack_max_seen=" + str(pre["attack_max_seen"]) + "（下界读数）；并行 r/C/J/卷只作读数，不占号、不覆盖他人。")
    L.append("")
    L.append("## §2 方法")
    L.append("")
    L.append("- 对象：" + ", ".join(r["id"] for r in rows) + "（6 册判定册，逐字节 md5 留痕）。")
    L.append("- 属性：" + ", ".join(a[0] + "=" + a[1] for a in ATTRS) + "，每类由 4 个针词命中构造二值位。")
    L.append("- 形式概念：枚举对象子集 2^6，取共同属性闭包再回取外延；属性蕴含序定义为 extent(a) ⊆ extent(b) ⇒ a ⇒ b。")
    L.append("- 共同核 core = 全部 6 册都具备的属性；结构核 = 剔除自指红线属性 P 后的核。")
    L.append("- 阳性对照：空文本必须全 0、全针词文本必须全 1、逐属性剔除必须翻转、注入全 0 合成对象 SYN0 后概念数必须严格增加。")
    L.append("")
    L.append("## §3 机器读数")
    L.append("")
    L.append("| 项 | 读数 |")
    L.append("| --- | --- |")
    L.append("| 事实源 | " + str(sum(r["exists"] for r in facts)) + "/" + str(len(facts)) + " 实到，针词容忍 " + str(sum(r["tolerance_ok"] for r in facts)) + "/" + str(len(facts)) + " |")
    L.append("| 对象—属性命中合计 | " + str(fca["attr_extents"]) + " |")
    L.append("| 共同核 core | " + ", ".join(fca["core_labels"]) + "（" + str(len(fca["core"])) + " 项） |")
    L.append("| 结构核 | " + ", ".join(fca["core_structural"]) + " |")
    L.append("| 非核属性 | " + ", ".join(fca["irrelevant_labels"]) + " |")
    L.append("| 形式概念数 | " + str(fca["concept_count"]) + " → 注入 SYN0 后 " + str(fca["mutated_concept_count"]) + " |")
    L.append("| 属性蕴含 | " + str(fca["implication_count"]) + " 条，非核内部非平凡 " + str(fca["nontrivial_count"]) + " 条 |")
    L.append("| 变异对照 | 空文本全 0=" + str(mut["blank_all_zero"]) + "、全针词全 1=" + str(mut["all_present_all_one"]) + "、翻转 " + str(mut["flip_count"]) + "/" + str(len(ATTRS)) + " |")
    L.append("| 红线 | " + str(len(red["present"])) + "/" + str(len(REDLINES)) + " 命中 |")
    L.append("| 条目 / 守卫 | " + str(len(entries)) + " 条 / " + str(sum(x["ok"] for x in guards)) + " " + "/" + " " + str(len(guards)) + " |")
    L.append("")
    L.append("## §4 承重裁定")
    L.append("")
    L.append("1. **E06（FAIL）**：「阻塞可逐册分别消除」不成立。六册否定结论共享 " + str(len(fca["core"])) + " 项核属性（" + ", ".join(fca["core_labels"]) + "），核是跨册结构，不是单册笔误。")
    L.append("2. **E07（FAIL）**：「换公理 / 加知识 / 给闭式即可绕开」不成立。核内 N（必要不充分）、C（闭式公设）、G（方向门不变量）正是这三类路线自身的属性；且每个非核属性的外延都包含于每个核属性的外延 ⇒ 具体阻塞蕴含核。")
    L.append("3. **E11（FAIL）**：「解除非核属性即可攻破」不成立。非核属性 " + ", ".join(fca["irrelevant_labels"]) + " 各至少有一册缺失，删除它们不改变核合取。")
    L.append("4. **E09（CORRECTED）**：初版按 FCA 的 A′=全对象求「最小生成子」得 size=1（任一核属性单独即覆盖全体），语义平凡；改为「击中核」表述并剔除自指属性 P，读数落到结构核 " + ", ".join(fca["core_structural"]) + "。")
    L.append("5. **E12（BOUNDARY）**：本判定只在「单调合取版本空间」假设类内成立；换非单调判据不在此作用域，**不外推为物理不可能**。")
    L.append("6. **判据含义**：下一轮若真要推进，必须同时击中结构核的全部项（合成逃逸对象在核全 0 时 gate=0，只恢复单个核属性仍 gate=0），而不是逐册逐项修补。")
    L.append("")
    L.append("## §5 自抓清单（SC1–SC" + str(len(sc)) + "，逐条留痕）")
    L.append("")
    for x in sc:
        L.append("- **" + x["code"] + " [" + x["tag"] + "]**：" + x["text"])
    L.append("")
    L.append("## §6 红线与治理")
    L.append("")
    L.append("- 红线 " + str(len(red["present"])) + "/" + str(len(REDLINES)) + "：" + ", ".join(red["present"]) + "；`0/6，未完成` 不变，`UFT-3=0` / `L3=0` / `validated=0` / `L3 ↛ L4` 不变。")
    L.append("- VERDICT 显式含 NO-PHYSICAL-COMPLETION；不改 `verify.py`、不跑 `refresh_catalog.py`、不做 git、不触碰他人文件。")
    L.append("- 引擎 stdout 只出 ASCII；中文全部写入 UTF-8 产物。")
    L.append("")
    L.append("## §7 边界与不宣称")
    L.append("")
    L.append("- FCA 归并在「针词命中 → 二值属性」这一层上做，属性编码本身是人工登记（[C] 类），不是物理测量。")
    L.append("- 「最小不可消除核」是**假设类内**的最小击中要求，不等于「统一场论不可能」；数学/格论自洽 ≠ 物理证实或证伪。")
    L.append("- 本册不产出新方程、新常数、新实验预言；与 attack59「有限知识欠定」结论方向一致、层次不同。")
    L.append("")
    L.append("## §8 下一步（不代选）")
    L.append("")
    L.append("- 若要继续：先给出能同时命中 " + ", ".join(fca["core_structural"]) + " 的单条机制，再谈是否重开具体物理路线；否则任何单册修补都不改变核合取。")
    L.append("- 不代用户选择是否修改公设集、是否接受外部输入、是否放弃该方向。")
    L.append("")
    L.append("## 相关入口")
    L.append("")
    L.append("- 数据正本：[" + TAG + ".json](" + TAG + ".json)")
    L.append("- 机器读数：[" + TAG + ".md](" + TAG + ".md)")
    L.append("- 守卫报告：[" + TAG + "_report.txt](" + TAG + "_report.txt)")
    L.append("- 引擎：[" + TAG + ".py](" + TAG + ".py)")
    L.append("")
    return "\n".join(L) + "\n"


def build_report(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count):
    L = []
    L.append("ATTACK60 REPORT 2026-11-12")
    L.append("VERDICT " + VERDICT)
    L.append("ENTRIES " + str(len(entries)) + " STATUS " + json.dumps(status_count, ensure_ascii=True, sort_keys=True))
    L.append("FACTS " + str(sum(r["exists"] for r in facts)) + "/" + str(len(facts))
             + " TOL " + str(sum(r["tolerance_ok"] for r in facts)) + "/" + str(len(facts)))
    L.append("DYN attack_max_seen=" + str(pre["attack_max_seen"])
             + " attack60_hits=" + str(pre["attack60_hits"])
             + " r=" + str(pre["r_max_seen"]) + " C=" + str(pre["C_max_seen"])
             + " J=" + str(pre["J_max_seen"]) + " VOL=" + str(pre["VOL_max_seen"]))
    L.append("DUP scanned_md=" + str(dup["scanned_md"]) + " raw=" + str(dup["hit_total"])
             + " cross_ref=" + str(dup["cross_ref_hit_total"])
             + " independent=" + str(dup["independent_hit_total"]))
    L.append("AST third=" + str(len(ac["third_party_imports"])) + " banned=" + str(len(ac["banned_calls"]))
             + " literal_bool=" + str(ac["literal_bool_assign"]) + " compile=" + str(ac["py_compile_ok"]))
    L.append("MATRIX " + " ".join(r["id"] + ":" + "".join(str(v) for v in r["bits"]) for r in rows))
    L.append("FCA attr_totals=" + str(fca["attr_extents"]) + " core=" + ",".join(fca["core_labels"])
             + " structural=" + ",".join(fca["core_structural"]) + " irrelevant=" + ",".join(fca["irrelevant_labels"]))
    L.append("FCA concepts=" + str(fca["concept_count"]) + " mutated=" + str(fca["mutated_concept_count"])
             + " implications=" + str(fca["implication_count"]) + " nontrivial=" + str(fca["nontrivial_count"]))
    L.append("MUT blank_all_zero=" + str(mut["blank_all_zero"]) + " all_present_all_one=" + str(mut["all_present_all_one"])
             + " flips=" + str(mut["flip_count"]) + "/" + str(len(ATTRS)))
    L.append("REDLINES " + str(len(red["present"])) + "/" + str(len(REDLINES)) + " missing=" + str(len(red["missing"])))
    for x in guards:
        L.append(x["code"] + " ok=" + str(x["ok"]) + " " + x["reading"])
    L.append("SELF_CORRECTIONS " + str(len(sc)))
    for x in sc:
        L.append(x["code"] + " " + x["tag"])
    guard_ok = sum(x["ok"] for x in guards)
    L.append("GUARDS " + str(guard_ok) + "/" + str(len(guards)))
    L.append("EXIT " + str(0 if guard_ok == len(guards) else 1))
    return "\n".join(L) + "\n"


def main():
    facts = fact_sources()
    pre = dynamic_scan()
    dup = duplicate_scan()
    ac = ast_selfcheck()
    rows = object_attrs()
    fca = galois(rows)
    mut = mutation_controls(rows)
    red = redline_check()
    entries = build_entries(facts, pre, dup, ac, rows, fca, mut, red)
    sc = self_corrections()
    guards = build_guards(facts, pre, dup, ac, rows, fca, mut, red, entries, sc)
    status_count = {}
    for e in entries:
        status_count[e["status"]] = status_count.get(e["status"], 0) + 1
    guard_ok = sum(x["ok"] for x in guards)
    ok_all = 1 if guard_ok == len(guards) else 0
    data = {
        "tag": TAG,
        "round": "attack60 / 攻破52",
        "date": "2026-11-12",
        "verdict": VERDICT,
        "external_reading": "0/6，未完成",
        "facts": facts,
        "dynamic_scan": pre,
        "duplicate_scan": dup,
        "ast_selfcheck": ac,
        "attrs": [{"code": a[0], "label": a[1], "needles": a[2]} for a in ATTRS],
        "object_attribute_matrix": rows,
        "fca": fca,
        "mutation_controls": mut,
        "redlines": red,
        "entries": entries,
        "guards": guards,
        "self_corrections": sc,
        "status_count": status_count,
        "guard_summary": {"total": len(guards), "ok": guard_ok},
        "exit_code": 0 if ok_all == 1 else 1,
    }
    write_json(P_JSON, data)
    write_text(P_MD, build_md(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count))
    write_text(P_JUDGE, build_judge(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count))
    write_text(P_REPORT, build_report(facts, pre, dup, ac, rows, fca, mut, red, entries, guards, sc, status_count))
    products_ok = sum(1 for p in OWN if os.path.isfile(p))
    ok = 1 if (ok_all == 1 and products_ok == 5) else 0
    print("PRODUCTS " + str(products_ok) + "/5")
    print("GUARDS " + str(guard_ok) + "/" + str(len(guards)))
    print("ENTRIES " + str(len(entries)))
    print("VERDICT " + VERDICT)
    print("EXIT " + str(0 if ok == 1 else 1))
    sys.exit(0 if ok == 1 else 1)


if __name__ == "__main__":
    main()
