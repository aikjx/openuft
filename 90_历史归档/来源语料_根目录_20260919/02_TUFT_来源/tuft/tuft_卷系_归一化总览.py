# -*- coding: utf-8 -*-
"""
tuft_卷系_归一化总览.py
=======================

TUFT / H-TUFT **卷系（卷十九~卷三十 + 补充卷A/B/C/D/E/F/G/H/I + 攻坚卷 + 攻坚续篇 + 出路卷）** 归一化与完整性审计引擎。

为何需要本工具（全维整理）：
  - 既有 `tuft_跨册缺陷族检查.py` / `tuft_判据门禁.py` **只覆盖 R 系 `*_report.txt`**；
  - **卷系**（H-TUFT 各卷 + 补充卷）此前**无**归一化/一致性/完整性审计；
  - 本工具把卷系的 CURATED 条目、脚本哈希、落盘状态、评级一次性归一到**单一可复跑产物**。

功能：
  1. 汇总全部 `*_CURATED.json` → 建立全局 CURATED 索引（CUR-01 …）；
  2. 完整性审计：编号缺号 / 重号 / 非连续；脚本落盘状态；**声明哈希 vs 实际哈希**；
  3. 归一化评级（H/O/C/U）+ 层级（L0–L3）：状态关键字自动定级 + 人工 override 定层级；
  4. 反回退守卫：已排除（❌）条目若被他册改标为待检验（⏳）→ 报警；
  5. 产物：`tuft_卷系_归一化总览.md` + `tuft_卷系_归一化总览.json`。

红线：数学自洽 != 实验证实。本工具只做**归一化与完整性审计**，不评价物理正确性、不改动任何真源。
"""

from __future__ import print_function

import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "tuft_卷系_归一化总览.md")
OUT_JSON = os.path.join(HERE, "tuft_卷系_归一化总览.json")

# 人工层级 override（诚实评级；层级需判断，不自动生成）。等级由状态关键字自动推导。
LEVEL = {
    "CUR-01": "L3", "CUR-02": "L3", "CUR-03": "L3",
    "CUR-04": "L1", "CUR-05": "L2", "CUR-06": "L2",
    "CUR-07": "L2", "CUR-08": "L2", "CUR-09": "L1", "CUR-10": "L1",
    "CUR-11": "L2", "CUR-12": "L2", "CUR-13": "L2",
    "CUR-14": "L2", "CUR-15": "L2", "CUR-16": "L2", "CUR-17": "L1", "CUR-18": "L2",
    "CUR-19": "L2", "CUR-20": "L2", "CUR-21": "L2", "CUR-22": "L1", "CUR-23": "L2",
    "CUR-24": "L1", "CUR-25": "L1",
}
# 反回退：这些条目状态**必须是** ❌ 系（已排除/已关闭/已触发/核心失败）
MUST_BE_EXCLUDED = {"CUR-01", "CUR-02", "CUR-03", "CUR-13", "CUR-14", "CUR-15", "CUR-18", "CUR-20", "CUR-21", "CUR-22", "CUR-23", "CUR-24", "CUR-25"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def grade_of(status):
    """按**条目自身的前导状态标记**定级（避免误吃正文里的『已关闭/失败』等词）：
    以 ❌ 开头 -> C（已排除/已关闭/已触发/核心失败）；以 ⏳ 或 ✅ 开头 -> O；其余 -> U。"""
    s = (status or "").strip()
    if s.startswith("❌"):
        return "C"
    if s.startswith("⏳") or s.startswith("✅"):
        return "O"
    return "U"


def eid_num(eid):
    m = re.match(r"CUR-(\d+)", eid or "")
    return int(m.group(1)) if m else None


def load_curated():
    docs = []
    for fname in sorted(os.listdir(HERE)):
        if not fname.endswith("_CURATED.json"):
            continue
        path = os.path.join(HERE, fname)
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception as exc:
            docs.append((fname, None, "UNREADABLE: %s" % exc))
            continue
        docs.append((fname, doc, None))
    return docs


def main():
    docs = load_curated()
    entries = {}
    problems = []

    for fname, doc, err in docs:
        if doc is None:
            problems.append(("CURATED 不可读", fname, err)); continue
        vol = doc.get("volume", "?")
        for ent in doc.get("entries", []):
            eid = ent.get("entry_id", "?")
            base = (ent.get("script_ref", "") or "").split("（")[0].strip().strip("`")
            declared = ent.get("script_sha256", None)
            path = os.path.join(HERE, base) if base else ""
            landed = bool(base) and os.path.isfile(path)

            if not base:
                land_state = "NO_SCRIPT_REF"
            elif not landed:
                land_state = "NOT_LANDED"
            elif declared is None:
                land_state = "UNDECLARED_HASH"
            elif sha256_file(path) == declared:
                land_state = "MATCH"
            else:
                land_state = "HASH_DRIFT"
            if land_state in ("NOT_LANDED", "HASH_DRIFT", "UNDECLARED_HASH"):
                problems.append(("脚本问题", "%s@%s" % (eid, fname), land_state))

            if eid in entries:
                problems.append(("重号", eid, "已存在于 %s" % entries[eid]["file"]))
                continue
            entries[eid] = {
                "entry_id": eid, "file": fname, "volume": vol,
                "name": ent.get("name", ""), "script_ref": base,
                "script_sha256": declared, "land_state": land_state,
                "status": ent.get("status", ""),
                "grade": grade_of(ent.get("status", "")),
                "level": LEVEL.get(eid, "L2"),
                "category": ent.get("category", ""),
            }

    # 编号连续性与缺号
    nums = sorted(n for n in (eid_num(e) for e in entries) if n is not None)
    missing = [n for n in range(1, (max(nums) + 1) if nums else 1) if n not in nums]

    # 反回退守卫
    regressions = []
    for eid, e in entries.items():
        if eid in MUST_BE_EXCLUDED and e["grade"] != "C":
            regressions.append((eid, e["status"]))
            problems.append(("反回退违规", eid, "应为 ❌ 系，实为 %s" % e["grade"]))

    # 评级统计
    tally = {"H": 0, "O": 0, "C": 0, "U": 0}
    lvl = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
    for e in entries.values():
        tally[e["grade"]] = tally.get(e["grade"], 0) + 1
        lvl[e["level"]] = lvl.get(e["level"], 0) + 1
    # 缺号视为 U（未固化）
    tally["U"] += len(missing)
    lvl["L0"] += len(missing)

    # ---- 产物 ----
    md = []
    md.append("# TUFT / H-TUFT 卷系归一化总览（自动生成）\n")
    md.append("> 由 `tuft_卷系_归一化总览.py` 生成（可复跑）。覆盖**卷系**（卷十九~卷三十 + 补充卷A/B/C/D/E/F/G/H/I + 攻坚卷 + 攻坚续篇 + 出路卷）：")
    md.append("> R 系 `*_report.txt` 的归一化见 `tuft_跨册缺陷族检查.py` / `tuft_判据门禁.py`（本工具不重复）。")
    md.append("> 红线：数学自洽 != 实验证实。本表只做归一化与完整性审计，不改动真源。\n")

    md.append("## 一、CURATED 索引（CUR-01 ~ CUR-%02d）\n" % (max(nums) if nums else 0))
    md.append("| entry | 卷 | 名称 | script_ref | 落盘/哈希 | 状态(grade) | 层级 |")
    md.append("|---|---|---|---|---|---|---|")
    for eid in sorted(entries, key=lambda x: (eid_num(x) or 999)):
        e = entries[eid]
        md.append("| %s | %s | %s | `%s` | %s | %s (%s) | %s |" % (
            eid, e["volume"], e["name"], e["script_ref"] or "—",
            e["land_state"], (e["status"] or "")[:44], e["grade"], e["level"]))
    md.append("")

    md.append("## 二、完整性审计\n")
    md.append("- 条目总数：**%d**；编号范围 CUR-%s ~ CUR-%s" % (
        len(entries), ("%02d" % min(nums)) if nums else "-", ("%02d" % max(nums)) if nums else "-"))
    md.append("- **缺号**：" + (("、".join("CUR-%02d" % n for n in missing)) if missing else "无 ✅"))
    md.append("- **重号**：" + ("有（见问题清单）⚠️" if any(p[0] == "重号" for p in problems) else "无 ✅"))
    hl = [e for e in entries.values() if e["land_state"] == "HASH_DRIFT"]
    nl = [e for e in entries.values() if e["land_state"] == "NOT_LANDED"]
    md.append("- **哈希漂移**：" + (("、".join("%s(%s)" % (e["entry_id"], e["script_ref"]) for e in hl)) if hl else "无 ✅"))
    md.append("- **脚本未落盘**：" + (("、".join("%s(%s)" % (e["entry_id"], e["script_ref"]) for e in nl)) if nl else "无 ✅"))
    md.append("- **反回退守卫**：" + ("⚠️ %s" % regressions if regressions else "全部 ❌ 条目保持 ❌ ✅"))
    md.append("")

    md.append("## 三、归一化评级（H 可信地基 / O 欠定诚实边界 / C 缺陷冲突 / U 未展开）\n")
    md.append("| 等级 | 条目数 |")
    md.append("|---|---|")
    for g in ("H", "O", "C", "U"):
        md.append("| %s | %d |" % (g, tally.get(g, 0)))
    md.append("")
    md.append("层级分布：L0=%d · L1=%d · L2=%d · L3=%d" % (
        lvl.get("L0", 0), lvl.get("L1", 0), lvl.get("L2", 0), lvl.get("L3", 0)))
    md.append("")
    md.append("> **归一化结论**：`H=0`——卷系**无一条达到可信地基**；`C=%d`（已排除/已关闭/核心失败）；" % tally.get("C", 0))
    md.append("> `O=%d`（待检验/自洽无预言）；`U=%d`（缺号未固化）。" % (tally.get("O", 0), tally.get("U", 0)))
    md.append("")

    md.append("## 四、问题清单\n")
    if problems:
        md.append("| 类别 | 对象 | 说明 |")
        md.append("|---|---|---|")
        for cat, obj, note in problems:
            md.append("| %s | %s | %s |" % (cat, obj, note))
    else:
        md.append("无不一致项 ✅")
    md.append("")

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({
        "entries": [entries[k] for k in sorted(entries, key=lambda x: (eid_num(x) or 999))],
        "missing": missing, "tally": tally, "levels": lvl,
        "problems": [{"cat": c, "obj": o, "note": n} for c, o, n in problems],
        "regressions": regressions,
    }, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("已生成: %s" % OUT_MD)
    print("  条目 %d；缺号 %s；问题 %d" % (
        len(entries), ("CUR-%02d" % missing[0] if missing else "无"), len(problems)))
    print("  评级：H=%d O=%d C=%d U=%d；层级 L0=%d L1=%d L2=%d L3=%d" % (
        tally.get("H", 0), tally.get("O", 0), tally.get("C", 0), tally.get("U", 0),
        lvl.get("L0", 0), lvl.get("L1", 0), lvl.get("L2", 0), lvl.get("L3", 0)))
    for cat, obj, note in problems:
        print("  [%s] %s -> %s" % (cat, obj, note))


if __name__ == "__main__":
    main()
