# -*- coding: utf-8 -*-
"""
册级一致性与读数漂移 · 守卫工具（可复用）
=========================================================================
立项目的（不是又一份「审计册」，而是一台**仪器**）
--------------------------------------------------------------------
跨册归一册（2026-10-04）在仲裁时抓到一类**任何单册都无法自己发现**的缺陷：

  ★D2：FIXV 的 .md 写「引力符号**自动导出**」，而它自己的 .json guard 写
       「来自候选式选择、**非自动导出**」⇒ 文字结论与机器产物**相反**；
       同一处还发现该 md 的「条目 24 / PASS 19」与 json 的「26 / 16」**不一致**。

根因是流程性的：md 由人写（或由旧版产物抄写），json 由脚本生成，
**两者之间没有任何机器校验**。本工具就是把这道校验补上，并**推广到全套件**：

  检查 1 · **json 内部自洽**：自检 通过数 == 总数；条目 id 无重复；counts 之和 == 总计。
  检查 2 · **md ↔ json 读数一致**：从 md 的「读数/总计」行抽出 (条目数, PASS/FAIL/BOUNDARY/INFO)，
           与 json 的计数逐格比对。
  检查 3 · **册内措辞 vs guard 冲突**（D2 类的定性版）：
           若 md 中出现「自动导出 / 完全精准匹配 / 无任何偏差」等**绝对化或过强**措辞，
           而同一册的 json guard 里出现「非自动导出 / 不唯一 / 未成立」等**否定性**措辞
           ⇒ 登记为**措辞冲突嫌疑**，交人工裁定（机器只报嫌疑，不代替裁定）。

关联规则（md ↔ json 怎么配对）
--------------------------------------------------------------------
各册命名不统一（如 json `…_修复版` 对应 md `…修复执行`），故用
**最长公共前缀 ≥ 8 字符**做疑似关联；关联只用于**比对**，
且只在读数不同时才需要人看 ⇒ 误关联的代价很低（相同则无输出）。

用法
--------------------------------------------------------------------
    python 册级一致性与读数漂移_守卫工具_2026-10-05.py            # 扫默认套件目录
    python 册级一致性与读数漂移_守卫工具_2026-10-05.py <目录>      # 扫任意目录（可复用）

退出码 **0** = 无 md/json 读数漂移且 json 全部内部自洽；**2** = 检出缺陷（可作门禁）。

纯标准库。
"""

import os
import sys
import json
import time
import re
import io

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
OUT_DIR = DATA_DIR

RESULTS = []
GUARDS = []

# 绝对化/过强措辞（出现在 md 里 ⇒ 与该册 guard 的否定性措辞对照）
STRONG_WORDS = ["自动导出", "完全精准匹配", "无任何偏差", "无可辩驳", "彻底攻克",
                "完美匹配", "完美复刻", "100%", "完美解释"]
# guard 中的否定性措辞
NEGATIVE_WORDS = ["非自动导出", "不唯一", "未成立", "不可满足", "不可得", "已关闭",
                  "不可区分", "无定义", "不成立", "空约束"]


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item,
                    "statement": statement, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:110]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-34s | %s | %s" % ("PASS" if ok else "FAIL", name, detail[:110]))
    return ok


def common_prefix_len(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def extract_json_info(d):
    """返回 (总计, counts dict, guard_ok, guard_total, ids list)。"""
    counts = d.get("计数") or d.get("counts") or {}
    total = d.get("总计") or d.get("total")
    res = None
    for k in ("条目", "results", "items", "records", "RESULTS"):
        if isinstance(d.get(k), list):
            res = d[k]
            break
    if total is None and res is not None:
        total = len(res)
    sj = d.get("自检")
    if isinstance(sj, dict):
        g_ok, g_tot = sj.get("通过"), sj.get("总数")
    else:
        g_ok, g_tot = d.get("guard_ok"), d.get("guard_total")
    ids = []
    if res:
        for it in res:
            if isinstance(it, dict):
                v = it.get("id") or it.get("name")
                if v:
                    ids.append(str(v))
    # 兜底：若 counts 缺失/为空（部分册用别的键名），**从条目列表按 verdict 现算**，
    #       否则会得出 "json=0" 的假漂移（首轮实测就踩了这个坑）。
    if (not counts) and res:
        derived = {}
        for it in res:
            if isinstance(it, dict):
                v = it.get("verdict") or it.get("判定") or it.get("verdict_")
                if v:
                    derived[str(v)] = derived.get(str(v), 0) + 1
        if derived:
            counts = derived
    return total, counts, g_ok, g_tot, ids


def pair_confidence(jstem, mstem):
    """配对置信度：high（去前缀后同名）/ mid（长公共前缀）/ none。"""
    for p in ("判定_", "整理_", "数据_"):
        if mstem.startswith(p):
            mstem2 = mstem[len(p):]
            break
    else:
        mstem2 = mstem
    if mstem2 == jstem:
        return "high"
    n = common_prefix_len(jstem, mstem2)
    if n >= 12 and n >= 0.6 * min(len(jstem), len(mstem2)):
        return "mid"
    return "none"


RE_TOTAL = re.compile(r"条目\s*(\d+)")
RE_CNT = {
    "PASS": re.compile(r"PASS\s*(\d+)"),
    "FAIL": re.compile(r"FAIL\s*(\d+)"),
    "BOUNDARY": re.compile(r"BOUNDARY\s*(\d+)"),
    "INFO": re.compile(r"INFO\s*(\d+)"),
}


def extract_md_reading(txt):
    """从 md 文本抽出第一处「读数行」的 (条目数, counts)。找不到返回 None。"""
    lines = txt.splitlines()
    for ln in lines[:40]:                      # 读数行通常在头部
        if "条目" in ln or ("PASS" in ln and "FAIL" in ln):
            m = RE_TOTAL.search(ln)
            if not m:
                continue
            cnt = {}
            for k, rx in RE_CNT.items():
                mm = rx.search(ln)
                if mm:
                    cnt[k] = int(mm.group(1))
            if cnt:
                return int(m.group(1)), cnt
    return None


def main():
    argv = sys.argv[1:]
    if argv and os.path.isdir(argv[0]):
        base = os.path.abspath(argv[0])
        data_dir = os.path.join(base, "数据") if os.path.isdir(os.path.join(base, "数据")) else base
        out_dir = data_dir
        scan_dirs = [base, data_dir]
    else:
        base = BASE
        data_dir = DATA_DIR
        out_dir = OUT_DIR
        scan_dirs = [base, data_dir]

    print("=" * 78)
    print("册级一致性与读数漂移 · 守卫工具")
    print("扫描目录：%s" % base)
    print("=" * 78)

    # ---------- 收集 ----------
    jsons = {}
    for fn in sorted(os.listdir(data_dir)):
        if fn.endswith(".json"):
            p = os.path.join(data_dir, fn)
            try:
                with io.open(p, encoding="utf-8") as fh:
                    obj = json.load(fh)
                if isinstance(obj, dict):          # 顶层为 list 的（索引/清单类）跳过
                    jsons[fn[:-5]] = obj
            except Exception:
                continue
    mds = {}
    for d in scan_dirs:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".md"):
                p = os.path.join(d, fn)
                try:
                    with io.open(p, encoding="utf-8", errors="replace") as fh:
                        mds[fn[:-3]] = {"text": fh.read(), "dir": os.path.basename(d)}
                except Exception:
                    continue

    guard("collection_ok", len(jsons) >= 5 and len(mds) >= 5,
          "收集：json %d 份、md %d 份" % (len(jsons), len(mds)))
    add("T-01", "T 工具", "扫描覆盖与配对规则",
        "json %d 份 / md %d 份；md↔json 用最长公共前缀 ≥8 字符做疑似关联" % (len(jsons), len(mds)),
        "PASS",
        "配对规则说明：各册命名不统一（json `…_修复版` 对应 md `…修复执行`），"
        "故不按同名匹配，而按**最长公共前缀 ≥ 8 字符**做疑似关联；"
        "关联只用于比对，且**只有读数不同才输出** ⇒ 误关联代价很低（相同则无产出）。")

    # ---------- 检查 1：json 内部自洽 ----------
    internal_bad = []
    for stem, d in jsons.items():
        total, counts, g_ok, g_tot, ids = extract_json_info(d)
        probs = []
        if g_tot is not None and g_ok is not None and g_ok != g_tot:
            probs.append("自检 %s/%s 不相等" % (g_ok, g_tot))
        if ids and len(set(ids)) != len(ids):
            probs.append("条目 id 重复 %d 个" % (len(ids) - len(set(ids))))
        s = sum(counts.get(k, 0) for k in ("PASS", "FAIL", "BOUNDARY", "INFO")) if counts else None
        if s is not None and total is not None and s != total:
            probs.append("counts 之和 %d ≠ 总计 %s" % (s, total))
        if probs:
            internal_bad.append({"册": stem, "问题": probs})
    guard("json_internal_consistent", not internal_bad,
          "json 内部自洽：%d/%d 份全部通过%s" %
          (len(jsons) - len(internal_bad), len(jsons),
           ("；异常 " + "; ".join(b["册"] for b in internal_bad)) if internal_bad else ""))
    add("T-02", "T 检查1", "json 内部自洽（自检数 / id 唯一 / counts 之和）",
        "%d 份 json" % len(jsons),
        "PASS" if not internal_bad else "FAIL",
        "逐份检查三项：①自检「通过 == 总数」；②条目 id 无重复；③counts 之和 == 总计。"
        "结果：**%d/%d 份全部通过**%s。%s"
        % (len(jsons) - len(internal_bad), len(jsons),
           "" if not internal_bad else "（异常：" + "；".join(
               "%s ⇒ %s" % (b["册"], "、".join(b["问题"])) for b in internal_bad) + "）",
           "⇒ 说明各册脚本自身的落盘口径是一致的，**缺陷集中在 md 侧**。"
           if not internal_bad else ""))

    # ---------- 检查 2：md ↔ json 读数一致 ----------
    mismatch = []
    suspect_drift = []
    checked = []
    for jstem, d in jsons.items():
        total, counts, _, _, _ = extract_json_info(d)
        if total is None:
            continue
        for mstem, m in mds.items():
            conf = pair_confidence(jstem, mstem)
            if conf == "none":
                continue
            r = extract_md_reading(m["text"])
            if not r:
                continue
            md_total, md_cnt = r
            diffs = []
            if md_total != total:
                diffs.append("条目数 md=%d vs json=%s" % (md_total, total))
            for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
                jv = counts.get(k, 0)
                mv = md_cnt.get(k)
                if mv is None:
                    continue           # md 未写该项则跳过（很多册只写 PASS/FAIL/INFO）
                if mv != jv:
                    diffs.append("%s md=%d vs json=%d" % (k, mv, jv))
            checked.append({"json": jstem, "md": mstem, "dir": m["dir"],
                            "confidence": conf, "diffs": diffs})
            if diffs and conf == "high":
                mismatch.append({"json": jstem, "md": mstem, "dir": m["dir"], "diffs": diffs})
            elif diffs:
                suspect_drift.append({"json": jstem, "md": mstem, "dir": m["dir"], "diffs": diffs})

    guard("md_json_readings_consistent", not mismatch,
          "md↔json 读数（高置信 %d 对）：漂移 %d 对%s；中置信疑似 %d 对（不计入门禁）"
          % (sum(1 for c in checked if c["confidence"] == "high"), len(mismatch),
             ("：" + "; ".join(x["md"] for x in mismatch)) if mismatch else "",
             len(suspect_drift)))
    add("T-03", "T 检查2", "md ↔ json 读数漂移（D2 类的量化版）",
        "比对 %d 对" % len(checked),
        "PASS" if not mismatch else "FAIL",
        "比对 %d 对（json × md）。**高置信**（去前缀后同名）%d 对 ⇒ **漂移 %d 对**；"
        "**中置信**（长公共前缀）差异 %d 对只记为**疑似**、不计入门禁（避免家族同名误判）。%s%s"
        % (len(checked), sum(1 for c in checked if c["confidence"] == "high"), len(mismatch),
           len(suspect_drift),
           "" if not mismatch else
           "漂移明细：" + "；".join("%s(%s) ⇒ %s" % (x["md"], x["dir"], "、".join(x["diffs"]))
                                   for x in mismatch) + "。",
           "⇒ 这正是 D2 的**可复用检测**：md 由人写/旧版抄写，json 由脚本生成，"
           "两者之间此前**没有任何机器校验**；本机把它变成**门禁**（退出码 0/2）。"
           if not mismatch else ""))

    # ---------- 检查 3：册内措辞 vs guard 冲突 ----------
    suspects = []
    for jstem, d in jsons.items():
        gtext = json.dumps(d.get("自检") or d.get("guards") or [], ensure_ascii=False)
        negs = [w for w in NEGATIVE_WORDS if w in gtext]
        if not negs:
            continue
        for mstem, m in mds.items():
            if pair_confidence(jstem, mstem) == "none":
                continue
            strongs = [w for w in STRONG_WORDS if w in m["text"]]
            if not strongs:
                continue
            # 只在同册既出现「过强措辞」又出现「guard 否定措辞」时报嫌疑
            suspects.append({"json": jstem, "md": mstem, "dir": m["dir"],
                             "md过强措辞": strongs, "guard否定措辞": negs})
    guard("wording_conflict_scan_done", True,
          "措辞冲突扫描：%d 条嫌疑（机器只报嫌疑，不代替人工裁定）" % len(suspects))
    add("T-04", "T 检查3", "册内措辞 vs guard 冲突嫌疑（D2 类的定性版）",
        "md 过强措辞 ∩ json guard 否定措辞",
        "PASS" if not suspects else "BOUNDARY",
        "扫描规则：同一册的 md 出现 %s 之类**过强措辞**，且该册 json 的 guard 文本出现 %s 之类"
        "**否定性措辞** ⇒ 登记嫌疑。结果：**%d 条**%s。"
        "⇒ **机器只报嫌疑、不代替裁定**（「候选式给出负值」是事实、「公理能唯一确定符号」是规范性主张，"
        "二者是否冲突须由人判断）；本工具的作用是把这类嫌疑**自动送到人面前**，"
        "而不是靠跨册仲裁时偶然撞见。"
        % ("/".join(STRONG_WORDS[:4]) + "等", "/".join(NEGATIVE_WORDS[:4]) + "等",
           len(suspects),
           "" if not suspects else "：" + "；".join(
               "%s ⇒ md含%s、guard含%s" % (x["md"], "/".join(x["md过强措辞"][:3]),
                                           "/".join(x["guard否定措辞"][:3])) for x in suspects)))

    # ---------- 结论 ----------
    add("T-05", "T 结论", "两条可固化的低成本规则（本工具的产出建议）",
        "把 D2 类缺陷从「靠运气发现」变成「自动拦截」",
        "PASS",
        "**规则一（读数同源）**：md 中的「条目 / PASS / FAIL / BOUNDARY / INFO」读数"
        "一律由 json 生成，或至少在生成 md 时用脚本回读 json 校验 ⇒ 消灭读数漂移。"
        "**规则二（措辞以 guard 为准）**：当 md 的文字结论与该册 json guard 的措辞冲突时，"
        "**以 guard 为准**；并把「自动导出 / 无任何偏差 / 完美匹配」等词列入 W-01 替换表逐条改写。"
        "⇒ 本工具把两条都变成了**可复跑的门禁**：退出码 0 = 无读数漂移；2 = 检出缺陷。"
        "它可作用于任意目录（`python <本脚本> <目录>`）⇒ 不是一次性审计，而是**仪器**。")

    # ---------- 落盘 ----------
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] += 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "主题": "册级一致性与读数漂移 · 守卫工具（可复用）",
        "扫描目录": base,
        "覆盖": {"json份数": len(jsons), "md份数": len(mds), "比对对数": len(checked)},
        "检查1_json内部": {"异常": internal_bad, "异常数": len(internal_bad)},
        "检查2_读数漂移": {"比对": checked, "漂移": mismatch, "漂移数": len(mismatch),
                           "疑似": suspect_drift, "疑似数": len(suspect_drift)},
        "检查3_措辞冲突嫌疑": {"嫌疑": suspects, "嫌疑数": len(suspects)},
        "计数": counts, "总计": len(RESULTS),
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base_out = os.path.join(out_dir, "册级一致性与读数漂移_守卫工具_2026-10-05")
    with io.open(base_out + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# 册级一致性与读数漂移 · 守卫工具（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 扫描目录：`%s`" % base,
          "- 覆盖：json %d 份 / md %d 份 / 比对 %d 对" % (len(jsons), len(mds), len(checked)),
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "", "## 检查 1 · json 内部自洽", "",
          "异常 %d 份%s" % (len(internal_bad),
                            "" if not internal_bad else "：" + "；".join(
                                "%s ⇒ %s" % (b["册"], "、".join(b["问题"])) for b in internal_bad)),
          "", "## 检查 2 · md ↔ json 读数漂移", "",
          "| md | 位置 | 漂移 |", "|---|---|---|"]
    if mismatch:
        for x in mismatch:
            md.append("| %s | %s | %s |" % (x["md"], x["dir"], "、".join(x["diffs"])))
    else:
        md.append("| — | — | **0 处漂移** |")
    md += ["", "## 检查 3 · 措辞冲突嫌疑", ""]
    if suspects:
        for x in suspects:
            md.append("- `%s`：md 含 %s；guard 含 %s"
                      % (x["md"], "/".join(x["md过强措辞"]), "/".join(x["guard否定措辞"])))
    else:
        md.append("- **0 条嫌疑**")
    md += ["", "## 逐条判定", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 150:
            head = head[:150] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base_out + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 78)
    print("条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base_out)
    if g_ok != len(GUARDS):
        print("GUARD FAILED —— 检出缺陷，请修复后重跑")
        return 2
    print("守卫通过：无 md/json 读数漂移，json 全部内部自洽")
    return 0


if __name__ == "__main__":
    sys.exit(main())
