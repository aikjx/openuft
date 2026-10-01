# -*- coding: utf-8 -*-
"""
tuft_跨线归一化清册.py
========================

【横向归一化】把语料**全库** `*_report.txt` 统一清册，从磁盘**重算**合计，
与各处**声明/手写**的合计对账——原则：**不信任任何手写聚合数字**。

为何需要它（发现两套并行体系，互不核对）：
  · **卷系体系**：`*_CURATED.json`（CUR-01~CUR-24）+ `tuft_卷系_归一化总览` +
    `tuft_卷系_结构障碍定理族`（10 条 no-go）+ `tuft_卷系_构造可行性门禁`。
  · **跨册体系**：`tuft_跨册缺陷族检查.py`（18 册缺陷族计数）+ `tuft_判据门禁.py`（量纲门禁）
    + `tuft_总索引.md`（全库 tally 基准）。
  ⇒ 两套体系**各自自洽**，但**没有任何工具**把二者的覆盖范围与计数口径对上。

计数口径（本工具采用**与既有工具同源**的通用口径）：
  主口径 = 判定**标签计数** `[PASS] / [FAIL] / [BOUNDARY] / [INFO]`
           （对**全部**报告格式通用；这是 `tuft_总索引.py` 类的口径）。
  副口径 = 报告**自身**在文末写明的合计行（两种格式：单行 `PASS = 5 / FAIL = ...`；
           多行 `PASS = 5\\nFAIL = 35\\n...`）——仅部分报告具备。

三项产出：
  1. **清册**：全库报告的标签计数 + （若有）显式合计行；
  2. **对账**：从磁盘重算全库/子集合计 ↔ 各声明值；
  3. **自洽**：**标签计数 vs 显式合计行**逐份比对（**本工具的真发现源**：
     一份报告若不等于自己的合计行，即该报告内部不自洽）。

红线：只做**计数与覆盖对账**，不评价物理正确性，不改动任何真源。数学自洽 != 实验证实。
"""

import hashlib
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ("PASS", "FAIL", "BOUNDARY", "INFO")

# 主口径：判定标签（容忍 `[FAIL*]` 等变体）
TAG_RE = re.compile(r"\[(PASS|FAIL|BOUNDARY|INFO)\b")
# 副口径：显式合计行（逐标签取末次匹配；负向排除 `[PASS]`）
LABEL_RE = {k: re.compile(r"(?<![A-Za-z\[])%s\s*=\s*(\d+)" % k) for k in LABELS}
HASH_RE = re.compile(r"(?:自哈希|SHA256|sha256)[^0-9a-fA-F]{0,20}([0-9a-fA-F]{64})")

# 跨册缺陷族检查覆盖的 18 册（自 `tuft_跨册缺陷族.md` §一 表抄录）
CROSS18 = {
    "tuft_续篇_全维求导精算_report.txt", "tuft_相位pi_全维求导精算_report.txt",
    "tuft_色挠率_SU3_report.txt", "tuft_三路线_ABC_report.txt",
    "tuft_四力统一_report.txt", "tuft_黑洞热力学_report.txt",
    "tuft_暴胀CMB_report.txt", "tuft_r5_report.txt", "tuft_r6_report.txt",
    "tuft_O_SCALE_锚定方案_report.txt", "tuft_引力波_挠率扰动_report.txt",
    "tuft_B_自屏蔽_数值求解_report.txt", "tuft_B_根因溯源_report.txt",
    "tuft_B_UV完成_report.txt", "tuft_收口_修复优化_report.txt",
    "tuft_续篇_双结交换仿真_report.txt", "tuft_Q量子_report.txt",
    "tuft_Q量子A_report.txt",
}

# 各处**声明**的合计（仅用于对账；本工具不信任它们）
CLAIMS = {
    "跨册缺陷族.md（18 册子集）": ("18", (134, 164, 73, 183)),
    "总索引.md（全库基准，声明）": ("ALL", (400, 244, 170, 458)),
    "全景总报告.md（手写）": ("ALL", (373, 241, 129, 337)),
}


def count_tags(txt):
    c = {k: 0 for k in LABELS}
    for m in TAG_RE.finditer(txt):
        c[m.group(1)] += 1
    return (c["PASS"], c["FAIL"], c["BOUNDARY"], c["INFO"])


def parse_summary(txt):
    out = []
    for k in LABELS:
        ms = LABEL_RE[k].findall(txt)
        if not ms:
            return None
        out.append(int(ms[-1]))
    return tuple(out)


def line_of(fname):
    if fname.startswith("tuft_卷") or "补充卷" in fname or "攻坚" in fname \
            or "出路卷" in fname:
        return "卷系"
    if re.match(r"tuft_[rR]\d+_", fname):
        return "R系"
    return "其余"


def scan():
    rows = []
    for fname in sorted(os.listdir(HERE)):
        if not fname.endswith("_report.txt"):
            continue
        try:
            with open(os.path.join(HERE, fname), encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except Exception as exc:
            rows.append({"file": fname, "line": line_of(fname), "tags": None,
                         "summary": None, "sha": None, "in_cross18": fname in CROSS18,
                         "err": str(exc)})
            continue
        hm = HASH_RE.search(txt)
        rows.append({"file": fname, "line": line_of(fname), "tags": count_tags(txt),
                     "summary": parse_summary(txt), "sha": hm.group(1) if hm else None,
                     "in_cross18": fname in CROSS18, "err": None})
    return rows


def total(rows):
    return [sum(r["tags"][k] for r in rows) for k in range(4)]


def _demo():
    rows = scan()
    allt = total(rows)
    s18 = [r for r in rows if r["in_cross18"]]
    t18 = total(s18)

    print("=" * 82)
    print("语料全库跨线归一化清册（从磁盘重算，不信任手写合计）")
    print("=" * 82)

    print("\n" + "-" * 82)
    print("[1] 清册总览（主口径 = 判定标签计数）")
    print("-" * 82)
    by = {}
    for r in rows:
        by.setdefault(r["line"], []).append(r)
    print("  %-8s %-8s %-14s %-10s %s" % ("线", "报告数", "标签合计 P/F/B/I", "有合计行", "内部自洽"))
    for ln in sorted(by):
        rs = by[ln]
        t = total(rs)
        nsum = sum(1 for r in rs if r["summary"])
        nok = sum(1 for r in rs if r["summary"] and r["summary"] == r["tags"])
        print("  %-8s %-8d %-14s %-10d %d/%d" % (
            ln, len(rs), "%d/%d/%d/%d" % tuple(t), nsum, nok, nsum))
    nsum = sum(1 for r in rows if r["summary"])
    nok = sum(1 for r in rows if r["summary"] and r["summary"] == r["tags"])
    print("  %-8s %-8d %-14s %-10d %d/%d" % ("**全库**", len(rows),
                                             "%d/%d/%d/%d" % tuple(allt), nsum, nok, nsum))

    print("\n" + "-" * 82)
    print("[2] 合计对账（重算 vs 声明）")
    print("-" * 82)
    print("  重算·全库（%d 份）：      %d / %d / %d / %d" % (len(rows), *allt))
    print("  重算·跨册 18 册子集：     %d / %d / %d / %d" % tuple(t18))
    for name, (scope, c) in CLAIMS.items():
        tgt = t18 if scope == "18" else allt
        d = [c[k] - tgt[k] for k in range(4)]
        print("  声明 %-26s %d/%d/%d/%d  ->  %s" % (
            name, c[0], c[1], c[2], c[3],
            "一致 ✅" if all(x == 0 for x in d) else "**Δ=%s**" % d))

    print("\n" + "-" * 82)
    print("[3] 内部自洽：报告「标签计数」vs 自身「显式合计行」（真发现源）")
    print("-" * 82)
    bad = [r for r in rows if r["summary"] and r["summary"] != r["tags"]]
    for r in bad:
        print("  %-52s 标签 %s  ≠  合计行 %s" % (
            r["file"][:52], "%d/%d/%d/%d" % r["tags"], "%d/%d/%d/%d" % r["summary"]))
    if not bad:
        print("  （有合计行的报告中，暂无内部不一致）")

    print("\n" + "-" * 82)
    print("[4] 覆盖缺口：未被跨册 18 册表覆盖的报告（%d 份）" % (
        len(rows) - len(s18)))
    print("-" * 82)
    for r in rows:
        if not r["in_cross18"]:
            print("  %-6s %-50s %s" % (
                r["line"], r["file"][:50], "%d/%d/%d/%d" % r["tags"]))

    print("\n" + "-" * 82)
    print("[5] 有哈希自报的报告（可用于防篡改对账）")
    print("-" * 82)
    hs = [r for r in rows if r["sha"]]
    print("  %d / %d 份报告自报 SHA256" % (len(hs), len(rows)))
    for r in hs[:6]:
        print("    %-46s %s…" % (r["file"][:46], r["sha"][:16]))
    if len(hs) > 6:
        print("    …（其余 %d 份略）" % (len(hs) - 6))

    print("\n" + "=" * 82)
    print("结论")
    print("=" * 82)
    print("  ① 两套归一化体系**并存且互不核对**（卷系 CURATED/定理族 ↔ 跨册缺陷族/总索引）。")
    print("  ② 从磁盘**重算**的全库标签合计见 [2]；凡 Δ≠0 即**聚合漂移**（声明值不可复算）。")
    print("  ③ [3] 逐份比对报告的标签计数与**它自己的合计行**——不等即为该报告内部不自洽。")
    print("  ④ 跨册 18 册表**未覆盖** %d 份报告（含全部卷系新报告）⇒ 覆盖缺口已量化。" % (
        len(rows) - len(s18)))
    print("  ⑤ 建议：**全库聚合数字一律由脚本重算生成、禁止手写**（单一真源 + 可复跑）；")
    print("     并把本清册纳入统一出口，使两套体系在**同一份产物**里对账。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 82)
    print("本文件 SHA256 =", _selfhash())
    print("定位：横向归一化清册（计数/对账/自洽/缺口，非预言）。数学自洽 != 实验证实。")
