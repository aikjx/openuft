# -*- coding: utf-8 -*-
"""统一方程元审计：r403 13 行候选总表的 unified 标签分层判别力。

对象：r403 判定册／JSON 的 13 行候选表（U01–U13），
不是三代质量不等式、不是 r404 代价下界、不是 r405 矩反例。查重已证实
「unified 标签在各层的假阳性率／口径降级复活／合取锁移除敏感性」未机验过。

两路机拼（数据源互不引用）：
  路 A = r403 JSON candidates[]（13 行，字段 forces/c0..c3/unified/status）
  路 B = r403 判定册 md §三 候选冻结总表（正则逐行抽列，语义白名单）
两路逐格比对后才允许后续判词。

门族：
  A 两路机拼 13 行一致（gate），反噬注入坏行必须 FAIL（neg）
  B 分层判别力：C3∧unified=1 / C3∧四力=0 / C2∧unified∧四力=2 /
    C0∧unified=7（假阳性 6/7）等，全部由表数据驱动不写死
  C 合取锁移除敏感性：移除 C3→7，移除 unified→2，两者全 0 才报锁
  D 口径降级复活：C3→C2 时四力统一 0→2，标注「形式统一非动力学统一」
  E 恒等门：C3 PASS ⊂ C2 PASS ⊂ C1 PASS 层级单调（单列不承重）

纪律：不重判 r403 任何候选、不新造方程、不产新物理、不宣称攻破 UFT；
独立预言计数 0；不占 RID、不登记 README、不与任何既有册相加。
"""
import glob
import json
import os
import re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
# HERE = openuft/04_公共成果/本项目_全维自洽与归一化/_统一方程元审计_*/
# 退三级 = openuft/ ; 数据/判定册均在 04_公共成果/本项目_全维自洽与归一化/
DATA_DIR = glob.glob(os.path.join(BASE, "04_*", "本项目_*", "数据"))[0]
JUDGE_DIR = glob.glob(os.path.join(BASE, "04_*", "本项目_*", "判定"))[0]

JP = glob.glob(os.path.join(DATA_DIR, "TUFT-r403_*统一方程*.json"))
MP = glob.glob(os.path.join(JUDGE_DIR, "判定_TUFT-r403_*统一方程*.md"))
assert len(JP) == 1, JP
assert len(MP) == 1, MP

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


# ---------------------------------------------------------------------------
# 路 A：r403 JSON
# ---------------------------------------------------------------------------
with open(JP[0], encoding="utf-8") as f:
    r403 = json.load(f)
assert r403["round"] == "r403"
assert r403["verdict"] == "NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK"
path_a = {}
for c in r403["candidates"]:
    path_a[c["id"]] = {
        "forces": c["forces"],
        "c0": c["c0"], "c1": c["c1"], "c2": c["c2"], "c3": c["c3"],
        "unified": bool(c["unified"]),
        "status": c["status"],
    }
assert len(path_a) == 13

# ---------------------------------------------------------------------------
# 路 B：r403 判定册 md §三 候选冻结总表，正则逐行 + 语义白名单抽列
# 表头：| ID | 方程族 | 覆盖 | C0 | C1 | C2 | C3 | 统一 | 状态 |
# 统一列中文「是」/「否**」；C0-C3 为 PASS/FAIL/BOUNDARY（可带 ** 加粗）
# 覆盖列含「2」「3」「四力」等；只按语义白名单取，不抓同名 kind 列。
# ---------------------------------------------------------------------------
with open(MP[0], encoding="utf-8") as f:
    md = f.read()
row_re = re.compile(r"^\|\s*(U\d{2})\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|")
path_b = {}
for line in md.splitlines():
    m = row_re.match(line)
    if not m:
        continue
    uid = m.group(1)
    if uid in path_b:
        continue
    fam, cov, c0, c1, c2, c3, uni, sta = [x.strip() for x in m.groups()[1:]]
    def clean(s):
        # md 表格里 status 带反引号 `VERIFIED-...`，层级带 ** 加粗，均属排版污染
        return s.replace("**", "").replace("`", "").strip()
    cov_clean = clean(cov)
    # 语义白名单：先中文数词，再阿拉伯数字；避免把括号里的其他数字误当力数
    if "四力" in cov_clean:
        forces = 4
    elif "三力" in cov_clean or "（3）" in cov:
        forces = 3
    elif "（2）" in cov or "弱 + 电磁" in cov:
        forces = 2
    else:
        forces = -1
    path_b[uid] = {
        "forces": forces,
        "c0": clean(c0), "c1": clean(c1), "c2": clean(c2), "c3": clean(c3),
        "unified": clean(uni) == "是",
        "status": clean(sta),
    }

ids_b = sorted(path_b)
ids_a = sorted(path_a)
same_ids = ids_a == ids_b
field_mismatch = []
for uid in ids_a:
    if uid not in path_b:
        continue
    for k in ("forces", "c0", "c1", "c2", "c3", "unified", "status"):
        if path_a[uid][k] != path_b[uid][k]:
            field_mismatch.append((uid, k, path_a[uid][k], path_b[uid][k]))
add("A1-two-path-merge", "gate", "JSON 路与 md 抽列路 13 行逐格一致",
    "ids_a=%d ids_b=%d same_ids=%s mismatch=%d" % (
        len(ids_a), len(ids_b), same_ids, len(field_mismatch)),
    same_ids and len(field_mismatch) == 0 and len(ids_b) == 13,
    "两路数据源互不引用：路 A 读 JSON candidates，路 B 正则解析判定册 md 表格；"
    "不一致即拒绝进入后续判词。若 mismatch>0 打印前 3 条：" + str(field_mismatch[:3]))

# A2 反噬：往路 B 注入一个坏行（改 U01 forces），必须被 A1 抓出
poisoned = {k: dict(v) for k, v in path_b.items()}
if "U01" in poisoned:
    poisoned["U01"]["forces"] = 7
poison_detected = any(poisoned[u]["forces"] != path_a[u]["forces"] for u in ids_a if u in poisoned)
add("A2-poison-control", "neg", "注入坏行必须被两路机拼抓出(反噬)",
    "把 U01 forces 改 7 后 detected=%s" % poison_detected,
    poison_detected,
    "负对照：若注入任意坏行仍 ALL-PASS，则两路机拼判别力 0")

# 以下全部只用路 A（已与路 B 对齐）做分层统计
R = path_a
LEVELS = ("c0", "c1", "c2", "c3")


def sel(level=None, unified=None, forces4=None):
    out = []
    for uid, c in R.items():
        if level is not None and c[level] != "PASS":
            continue
        if unified is not None and c["unified"] != unified:
            continue
        if forces4 is not None and (c["forces"] == 4) != forces4:
            continue
        out.append(uid)
    return sorted(out)


c3_u = sel("c3", True)
c3_f4 = sel("c3", True, True)
c3_all = sel("c3")
c2_u_f4 = sel("c2", True, True)
c1_u_f4 = sel("c1", True, True)
c0_u = sel("c0", True)
c0_u_f4 = sel("c0", True, True)
c0_all = sel("c0")

# 金标准 = r403 唯一答案 U01（C3∧unified），假阳性 = 低层 unified 但非金标准
gold = set(c3_u)
false_pos_c0 = [u for u in c0_u if u not in gold]
false_pos_c2_f4 = [u for u in c2_u_f4 if u not in gold]

add("B1-c3-unified-one", "gate", "C3∧unified 恰 1 条 = 金标准",
    "n=%d set=%s" % (len(c3_u), c3_u),
    len(c3_u) == 1 and c3_u == ["U01"],
    "继承 r403 G20；不重判候选，只从表数据重数")
add("B2-c3-fourforce-zero", "gate", "C3∧unified∧四力 恰 0 条",
    "n=%d set=%s" % (len(c3_f4), c3_f4),
    len(c3_f4) == 0,
    "继承 r403 G21；注意结论必须标注 C3 口径")
add("B3-c3-pass-two", "gate", "C3 PASS 共 2 条但只有 1 条统一",
    "C3 PASS=%s; 其中 unified=%s" % (c3_all, c3_u),
    len(c3_all) == 2 and len(c3_u) == 1,
    "C3 PASS 与 unified 是两个正交维度：U02 C3 PASS 但统一=False")

add("B4-tier-downgrade-revive", "gate", "口径 C3→C2 时四力统一 0→2",
    "C3四力=%d; C2四力=%s; C1四力=%s; C0四力=%s" % (
        len(c3_f4), c2_u_f4, c1_u_f4, c0_u_f4),
    len(c3_f4) == 0 and len(c2_u_f4) == 2 and set(c2_u_f4) == {"U09", "U10"},
    "口径降级立刻复活 2 条『四力统一』，但其 status 分别为 "
    "PROFILE-LEVEL-ONLY / FORM-UNIFIED-DYNAMICS-NOT-UNIFIED ⇒ 形式统一非动力学统一")

fp_rate = Fraction(len(false_pos_c0), len(c0_u)) if c0_u else Fraction(0)
add("B5-c0-false-positive", "gate", "C0∧unified=7 其中假阳性 6",
    "n=%d gold=%s 假阳性=%s rate=%s" % (
        len(c0_u), sorted(gold), false_pos_c0, str(fp_rate)),
    len(c0_u) == 7 and len(false_pos_c0) == 6 and fp_rate == Fraction(6, 7),
    "unified 标签在 C0 层假阳性率 6/7；判别力随层级放宽而衰减")
add("B6-c2-false-positive", "gate", "C2∧unified∧四力 假阳性 2/2",
    "n=%d 假阳性=%s" % (len(c2_u_f4), false_pos_c2_f4),
    len(c2_u_f4) == 2 and len(false_pos_c2_f4) == 2,
    "即使在 C2『还原层』，四力 unified 标签仍 2/2 假阳性")

# ---------------------------------------------------------------------------
# C 合取锁移除敏感性：把 C3 与 unified 当作两个条件，看移除任一后计数
# ---------------------------------------------------------------------------
remove_c3 = sel("c0", True)          # 只保留 unified，去掉 C3 门槛 = C0∧unified
remove_unified = sel("c3")           # 只保留 C3，去掉 unified = C3 PASS
both = sel("c3", True)
add("C1-lock-removal", "gate", "合取锁移除任一条件即失锁",
    "移除C3→%d(%s); 移除unified→%d(%s); 两者都在→%d(%s)" % (
        len(remove_c3), remove_c3, len(remove_unified), remove_unified,
        len(both), both),
    len(remove_c3) == 7 and len(remove_unified) == 2 and len(both) == 1
    and len(remove_c3) != 1 and len(remove_unified) != 1,
    "两个条件都承重：移除 C3→7 条，移除 unified→2 条，均非唯一；"
    "只有合取才得 1。与全链整理册的 N1/N2/N3 合取锁同型但对象不同，不相加")

# 反噬：注入一个假四力候选（C3 PASS + unified + forces4），G21 必须翻转
fake = {"X99": {"forces": 4, "c0": "PASS", "c1": "PASS", "c2": "PASS",
                "c3": "PASS", "unified": True, "status": "FAKE-INJECTED"}}
aug = dict(R)
aug.update(fake)
fake_c3_f4 = sorted(u for u, c in aug.items()
                    if c["c3"] == "PASS" and c["unified"] and c["forces"] == 4)
add("C2-inject-flip", "neg", "注入假四力候选使 C3∧四力 0→1",
    "注入前=%d 注入后=%d set=%s" % (len(c3_f4), len(fake_c3_f4), fake_c3_f4),
    len(c3_f4) == 0 and len(fake_c3_f4) == 1 and fake_c3_f4 == ["X99"],
    "负对照：判据必须能被一个假候选翻红；若注入后仍 0 则该计数是写死常量")

# 负对照：等口径配置——若把所有 C0 PASS 都当 C3，则 C3∧unified 从 1→7
all_as_c3 = [u for u in R if R[u]["c0"] == "PASS" and R[u]["unified"]]
add("C3-mutant-level-collapse", "neg", "层级塌缩(C0 当 C3)使唯一答案 1→7",
    "塌缩后=%d (原 %d)" % (len(all_as_c3), len(c3_u)),
    len(all_as_c3) == 7 and len(c3_u) == 1 and len(all_as_c3) != len(c3_u),
    "负对照沿『判据无法吸收的方向』位移：抹掉层级差异后唯一答案立刻失真")

# ---------------------------------------------------------------------------
# E 层级单调性检验：原假设 C3 PASS ⊂ C2 ⊂ C1 ⊂ C0。
# ★首跑 FAIL：U12（几何势族）C0=FAIL 但 C1=PASS ⇒ 破坏 C0⊇C1 蕴含。
# 按纪律不放宽门限救绿，如实登记为结构异常门（gate，断言「异常恰 1 条」）
# + 负对照（neg：若抹掉 U12 异常则门必须翻红）。
# 注意这是 r403 表内的数据事实，r403 原文未指出该层级蕴含被破坏。
# ---------------------------------------------------------------------------
mono = {}
for lv in LEVELS:
    mono[lv] = set(u for u, c in R.items() if c[lv] == "PASS")
viol_up = {}
for i in range(len(LEVELS) - 1):
    hi, lo = LEVELS[i + 1], LEVELS[i]
    viol_up[hi + "-not-in-" + lo] = sorted(mono[hi] - mono[lo])
all_viol = sorted({u for vs in viol_up.values() for u in vs})
add("E1-level-monotone", "gate", "层级蕴含检查：恰 U12 破坏 C0⊇C1",
    "sizes=%s; 破坏集合=%s; 明细=%s" % (
        {lv: len(mono[lv]) for lv in LEVELS}, all_viol, viol_up),
    all_viol == ["U12"] and R["U12"]["c0"] == "FAIL" and R["U12"]["c1"] == "PASS",
    "如实登记：U12 几何势族 C0=FAIL（量纲层不过）却 C1=PASS（数学复现过），"
    "破坏 C0⊇C1 蕴含；r403 未指出该异常。C2⊆C1⊆C0 对其余 12 行成立。"
    "首跑原假设「全层级单调」被数据证伪，不放宽门限、改断言为「异常恰 1 条」")

# 负对照：若抹掉 U12 的 C0=FAIL（改成 PASS），异常集合应为空 ⇒ 门必须翻红
patched = {k: dict(v) for k, v in R.items()}
patched["U12"]["c0"] = "PASS"
p_mono = {lv: set(u for u, c in patched.items() if c[lv] == "PASS") for lv in LEVELS}
p_viol = sorted({u for i in range(3)
                 for u in (p_mono[LEVELS[i + 1]] - p_mono[LEVELS[i]])})
add("E2-patch-monotone-neg", "neg", "抹掉 U12 异常后 E1 必须翻红",
    "原异常=%s; 修补后异常=%s" % (all_viol, p_viol),
    all_viol == ["U12"] and p_viol == [],
    "负对照：证明 E1 的异常读数由 U12 真实承载，不是恒真陈述或解析假象")

# ---------------------------------------------------------------------------
# 结论
# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("UNIFIED-LABEL-META--TWO-PATH-MERGE-13-ROWS-EXACT--"
               "C3-UNIFIED-IS-1-GOLD-U01--C3-FOURFORCE-IS-0-ONLY-IN-C3-CALIBER--"
               "C3-TO-C2-DOWNGRADE-REVIVES-2-FORMAL-ONLY--"
               "C0-FALSE-POSITIVE-6-OF-7--CONJUNCTION-LOCK-BOTH-CONDITIONS-LOAD-BEARING--"
               "U12-BREAKS-C0-C1-LEVEL-IMPLICATION-TRUE-ANOMALY--"
               "NO-NEW-EQUATION--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "UNIFIED-LABEL-META-FAIL--" + "-".join(fail)

result = {
    "subject": "统一方程元审计：r403 unified 标签分层判别力与口径依赖",
    "object_boundary": "对象是 r403 的 13 行候选总表（U01-U13）；"
                       "与三代质量不等式 V50/V51、r404 代价下界、r405 矩反例均非同一对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "two_path": {"path_a_source": os.path.basename(JP[0]),
                 "path_b_source": os.path.basename(MP[0]),
                 "rows": len(ids_a), "mismatch": len(field_mismatch)},
    "strata": {
        "C3_unified": c3_u, "C3_fourforce_unified": c3_f4,
        "C3_PASS_all": c3_all, "C2_unified_fourforce": c2_u_f4,
        "C1_unified_fourforce": c1_u_f4,
        "C0_unified": c0_u, "C0_false_positive": false_pos_c0,
        "C0_false_positive_rate": str(fp_rate),
    },
    "gates": gates,
}
with open(os.path.join(HERE, "_unified_label_meta.json"), "w",
          encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = ["统一方程元审计 · r403 unified 标签分层判别力", "=" * 64,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 64]
for g in gates:
    lines.append("[%s] %-26s %-10s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.append("-" * 64)
lines.append("分层: " + json.dumps(result["strata"], ensure_ascii=False))
lines.append("两路机拼: 路A=" + result["two_path"]["path_a_source"])
lines.append("          路B=" + result["two_path"]["path_b_source"])
lines.append("-" * 64)
lines.append("只读继承 r403; 不重判候选、不新造方程; 全确定性无随机")
with open(os.path.join(HERE, "_unified_label_meta_report.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
