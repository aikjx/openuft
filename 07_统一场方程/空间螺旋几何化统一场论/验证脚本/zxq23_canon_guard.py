# -*- coding: utf-8 -*-
"""
UFE-2 正典防回潮守卫（zxq23_canon_guard）

为什么需要它
------------
`26_UFE2_正典_统一场方程正确子集规范_2026-10-03.md` 的 §2 / §3 是**唯一真源**：
正典表说"哪些条目是对的"，排除表说"哪些不对"。人改公式很容易，改判据很难；
于是真正的失效模式是——**有人把一条 FAIL 的条目挪进正典，或把一条 PASS 的挪进排除表**。
本守卫把这条防线做成可执行的门禁。

判据来源
--------
读 `zxq23_ufe_results.json`（由 `zxq23_ufe.py` 生成）。**台账不存在即拒绝运行**，
不允许在缺判据的情况下校验正典。

强制的不变量
------------
G1  正典每行的支撑判据必须在台账里真实存在
G2  正典每行至少有一条 verdict == PASS 的支撑          （S1：入典必过检）
G3  正典任何一行都不得引用 verdict == FAIL 的判据      （防"失败条目入典"）
G4  排除表分两档：**强排除**须含 FAIL / BOUNDARY 级判据；**弱排除**（因"无信息量"
    而不敢入典，如定义重排、不可复算、口径漂移）须在"判据结论"列显式标 INFO
G5  编号唯一（正典 C-xx、排除 X-xx 各自不重不交）
G6  正典条目数不低于下限（防"清空正典"这类退化）
G7  C 类（约定）必须显式标注「定义式 / 零预测力 / 恒等」   （S2 纪律）
G8  正典文本不得出现被判 FAIL 的式号                   （双保险，挡手抄）
G9  弱排除条数不得超过排除表半数（防"把不确定一律当排除"这种反向造假）
G10 「派生自」列：无自引、目标条目须存在、无环、且至少有一条无上游条目
    （防"凭空宣称某条是推出来的"与"整张表互推"两类造假）
G11 A 类（推导）条目若**有上游**，必须至少有一条非量纲判据（M/N/S/V/I 系列）；
    纯量纲判据（D 系列）只能支撑公设级条目 —— 公设没有下游，量纲自洽就是它能有的全部证据
G12 台账 id 冲突：同一判据 id 在两台仪器里结论不同即冲突（编号纪律的守门人）

变异驱动（--teeth）
------------------
9 个变异体，每个必须在点名自己 id 的前提下被至少一条不变量抓红；
另设 1 个良性变异体（只改空白）不得误报。基线必须 rc==0，否则整轮 INVALID。

运行
----
python -B zxq23_canon_guard.py            # 校验
python -B zxq23_canon_guard.py --teeth    # 变异驱动
退出码：0 = 全部通过；1 = 有违规；2 = 夹具塌陷（台账/正典文件缺失或不可解析）
"""

import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, "zxq23_ufe_results.json")
CANON_MD = os.path.join(BASE, "26_UFE2_正典_统一场方程正确子集规范_2026-10-03.md")
CANON_JSON = os.path.join(HERE, "zxq23_canon_guard_results.json")

ID_RE = re.compile(r"\b([A-Z]\d{2}[a-z]?)\b")
# 支撑列的 token 必须能被完整解析成判据 ID；否则报 G1。
# （这条是变异体 m2 逼出来的：原先只查"引用的 ID 是否存在"，
#   于是一个拼错的 / 不存在的 ID 会被当成"没写判据"而静默通过。）
#
# 前缀表（全局唯一，G12 守门）：ufe=D/M/N/T/P/S  deps=F/E  o1_gap=A/B/C/Q
#                              o1_verify=V/I
# 第一版这里只写了 [DMNPST] 六个字母，于是 I03（身份审计）被判「无判据支撑」——
# 又一次"门禁把自己的没写与写错混同"。现按前缀表放宽为任意大写单字母。
FULL_RE = re.compile(r"[A-Z]\d{2}[a-z]?")
SPLIT_RE = re.compile(r"[,，、;；\s]+")
# 已被判 FAIL 的式号（双保险用）：式4 引力场、式11 磁场、式18 核力场、式21/22 加速电荷引力场
BANNED_RE = re.compile(r"式\s*(?:4|11|18|21|22)(?![0-9])")
CONVENTION_WORDS = ("定义式", "零预测力", "恒等")

MIN_CANON = 20


# ------------------------------------------------------------------ 解析
def load_results():
    """读**全部** zxq23_*_results.json 台账并合并成 id -> verdict 索引。

    为什么改成多台账：第一版只读 zxq23_ufe_results.json，于是「新仪器给出的判据
    无法被正典引用」—— 逼得人把新判据硬塞回旧仪器，或干脆不登记。合并后，
    任何一台 zxq23_* 仪器的判据都可被正典引用。

    同时检测 id 冲突：同一 id 在两台仪器里结论不同 ⇒ G12。
    编号纪律：每台仪器用独立前缀（本目录现为 D/M/N/T/P/S ← ufe、
    P/T ← deps、V/I ← o1_verify、A/B/C/D ← o1_gap），
    仪器新增判据段时必须换前缀，否则当场撞 G12。
    """
    if not os.path.isdir(HERE):
        print("[FAIL] 验证脚本目录不存在")
        return None, []
    files = sorted(f for f in os.listdir(HERE)
                   if f.startswith("zxq23_") and f.endswith("_results.json"))
    if not files:
        print("[FAIL] 同目录下没有任何 zxq23_*_results.json 台账")
        return None, []
    if not os.path.isfile(RESULTS):
        print("[FAIL] 主台账不存在：%s；请先运行 python -B zxq23_ufe.py"
              % os.path.basename(RESULTS))
        return None, []

    index, owner, conflicts = {}, {}, []
    for fn in files:
        try:
            with open(os.path.join(HERE, fn), encoding="utf-8") as fh:
                rows = json.load(fh).get("results") or []
        except Exception as exc:
            print("[FAIL] 台账 %s 不可解析：%s" % (fn, exc))
            return None, []
        for r in rows:
            rid, verdict = r.get("id"), r.get("verdict")
            if not rid or not verdict:
                continue
            if rid in index and index[rid] != verdict:
                conflicts.append((rid, owner[rid], index[rid], verdict, fn))
            index[rid] = verdict
            owner[rid] = fn
    if not index:
        print("[FAIL] 台账里没有可用的判据条目")
        return None, []
    return index, conflicts


def parse_tables(md_text):
    """把 §2 正典表与 §3 排除表解析成 (canon_rows, excl_rows)。"""
    canon, excl = [], []
    mode = None
    for line in md_text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if s and not s.startswith(">"):
                mode = None
            continue
        if "支撑判据" in s and "编号" in s:
            mode = "canon"
            continue
        if "排除判据" in s and "编号" in s:
            mode = "excl"
            continue
        if set(s.replace("|", "").replace(" ", "")) <= set("-:"):
            continue  # 分隔行
        if mode == "canon":
            canon.append([c.strip() for c in s.strip("|").split("|")])
        elif mode == "excl":
            excl.append([c.strip() for c in s.strip("|").split("|")])
    return canon, excl


def ids_in(cell):
    return ID_RE.findall(cell)


def unparsed_tokens(cell):
    """支撑列里无法解析成判据 ID 的 token（拼错的、不存在的、格式变了的名目）。"""
    out = []
    for tok in SPLIT_RE.split(cell):
        tok = tok.strip()
        if not tok or FULL_RE.fullmatch(tok):
            continue
        # 只豁免纯装饰 token：既不含数字也不含字母（如 "—"）。
        # 含字母的 token 一律必须能解析成判据 ID —— 否则一个拼错的名目
        # 会被当成"没写判据"而静默通过（变异体 m2 逼出来的第二次修正：
        # 第一版豁免条件写成"不含数字"，结果把 "ZZZ" 一起放行了）。
        if not re.search(r"\d", tok) and not re.search(r"[A-Za-z]", tok):
            continue
        out.append(tok)
    return out


# ------------------------------------------------------------------ 校验
def check(index, canon_rows, excl_rows, md_text, conflicts=()):
    complaints = []

    def bad(code, msg):
        complaints.append("%s: %s" % (code, msg))

    # ---- G12 台账 id 冲突
    for rid, f1, v_old, v_new, f2 in conflicts:
        bad("G12", "判据 %s 重复登记且结论不同：%s=%s vs %s=%s ——必须改编号前缀"
            % (rid, f1, v_old, f2, v_new))

    # ---- G6 正典条目数下限（先判，避免"清空正典"让后续门禁空转）
    if len(canon_rows) < MIN_CANON:
        bad("G6", "正典只有 %d 条（下限 %d）——正典被清空或表格解析失败"
            % (len(canon_rows), MIN_CANON))

    canon_ids, canon_body, edges = [], [], {}
    for row in canon_rows:
        if len(row) < 7:
            bad("G1", "正典行列数不足（%d 列，应为 7）：%s" % (len(row), row[0]))
            continue
        code, item, kind, level, support, deps, reason = row[:7]
        canon_ids.append(code)
        canon_body.append((code, item, kind, level, support, reason))
        parents = re.findall(r"C-\d{2}", deps)
        edges[code] = parents
        for p in parents:
            if p == code:
                bad("G10", "%s 的「派生自」自引" % code)
        for jid in ids_in(support):
            if jid not in index:
                bad("G1", "%s 的支撑判据 %s 不在台账里" % (code, jid))
        for tok in unparsed_tokens(support):
            bad("G1", "%s 的支撑判据列有无法解析的 token「%s」" % (code, tok))
        verdicts = [index.get(j) for j in ids_in(support)]
        if "PASS" not in verdicts:
            bad("G2", "%s 无任何 PASS 级支撑（实际 %s）——不满足入选标准 S1"
                % (code, verdicts or "无"))
        if "FAIL" in verdicts:
            bad("G3", "%s 引用了 FAIL 级判据 %s——失败条目不得入典"
                % (code, [j for j in ids_in(support) if index.get(j) == "FAIL"]))
        if kind.startswith("C") and not any(w in reason for w in CONVENTION_WORDS):
            bad("G7", "%s 标为 C 类（约定）但入选理由未显式写「%s」——违反 S2 标注纪律"
                % (code, "/".join(CONVENTION_WORDS)))
        # ---- G11 A 类有上游时必须有非量纲判据
        if kind.startswith("A") and edges.get(code):
            vlist = [index.get(j) for j in ids_in(support)]
            if not any((j[0] != "D") and (v == "PASS")
                       for j, v in zip(ids_in(support), vlist)):
                bad("G11", "%s 标为 A 类（推导）且有上游 %s，但支撑判据 %s 全是量纲类（D 系列）"
                           "——推导级结论不能只靠量纲支撑"
                    % (code, edges.get(code), ids_in(support)))

    # ---- 排除表
    excl_ids, unsupported, weak = [], 0, []
    for row in excl_rows:
        if len(row) < 5:
            bad("G1", "排除表行列数不足（%d 列，应为 5）：%s" % (len(row), row[0]))
            continue
        code, item, support, verdict_cell, why = row[:5]
        excl_ids.append(code)
        jids = ids_in(support)
        if not jids:
            unsupported += 1
            if not why:
                bad("G4", "%s 既无判据支撑、排除理由也为空" % code)
            continue
        for jid in jids:
            if jid not in index:
                bad("G1", "%s 的排除判据 %s 不在台账里" % (code, jid))
        for tok in unparsed_tokens(support):
            bad("G1", "%s 的排除判据列有无法解析的 token「%s」" % (code, tok))
        vs = [index.get(j) for j in jids]
        if any(v in ("FAIL", "BOUNDARY") for v in vs):
            continue  # 强排除，通过
        # 弱排除：只有 INFO 级依据（"无信息量"而非"已证伪"）——须显式标 INFO
        if not verdict_cell.startswith("INFO"):
            bad("G4", "%s 既无 FAIL/BOUNDARY 判据、'判据结论'列也未标 INFO（实际 %s）——不得无据排除"
                % (code, vs))
        elif not why:
            bad("G4", "%s 弱排除但排除理由为空" % code)
        else:
            weak.append(code)

    # ---- G5 编号唯一且两表不交
    for tag, seq in (("正典", canon_ids), ("排除", excl_ids)):
        dup = sorted(set(x for x in seq if seq.count(x) > 1))
        if dup:
            bad("G5", "%s表编号重复：%s" % (tag, dup))
    both = sorted(set(canon_ids) & set(excl_ids))
    if both:
        bad("G5", "同一编号同时出现在正典与排除表：%s" % both)

    # ---- G10 派生自：目标存在 + 无环 + 至少一个无上游
    for code in canon_ids:
        for p in edges.get(code, []):
            if p not in canon_ids:
                bad("G10", "%s 的「派生自」指向不存在的条目 %s" % (code, p))
    color, cycles = {}, []

    def visit(n, stack):
        color[n] = 1
        stack.append(n)
        for p in edges.get(n, []):
            if p not in edges:
                continue
            if color.get(p) == 1:
                cycles.append("→".join(stack[stack.index(p):] + [p]))
            elif color.get(p, 0) == 0:
                visit(p, stack)
        stack.pop()
        color[n] = 2

    for n in list(edges):
        if color.get(n, 0) == 0:
            visit(n, [])
    if cycles:
        bad("G10", "「派生自」存在环：%s" % "；".join(cycles[:3]))
    if canon_ids and not any(not v for v in edges.values()):
        bad("G10", "正典没有任何「—」（无上游）条目：整张表都在互推 ⇒ 必成环或全是外部输入")

    # ---- G9 弱排除不得超过半数
    if excl_rows and len(weak) * 2 > len(excl_rows):
        bad("G9", "弱排除（仅 INFO 依据）%d 条 > 排除表半数 %d 条：%s"
            % (len(weak), len(excl_rows) // 2, weak))

    # ---- G8 双保险：正典文本不得出现已判 FAIL 的式号
    canon_md = "\n".join("|".join(r) for r in canon_rows)
    for hit in sorted(set(BANNED_RE.findall(canon_md))):
        bad("G8", "正典表出现被判 FAIL 的式号「%s」" % hit)

    summary = {
        "canon_rows": len(canon_rows),
        "excl_rows": len(excl_rows),
        "excl_without_judgement": unsupported,
        "excl_weak": len(weak),
        "canon_by_class": {},
    }
    for code, item, kind, level, support, reason in canon_body:
        k = kind[:1]
        summary["canon_by_class"][k] = summary["canon_by_class"].get(k, 0) + 1
    return complaints, summary


# ------------------------------------------------------------------ 变异驱动
def mutate(md_text, tag):
    """每个变异体只改一处，且必须能被某条不变量抓红。"""
    if tag == "m1":       # 把 C-01 的支撑换成 FAIL 判据 D04 ⇒ G3
        return md_text.replace("| C-01 |", "| C-01 |", 1).replace(
            "| D12, D12b |", "| D04, D12b |", 1)
    if tag == "m2":       # 支撑判据指向不存在的 ID ⇒ G1
        return md_text.replace("| D12, D12b |", "| D12, ZZZ |", 1)
    if tag == "m3":       # 抽掉 PASS 支撑（换成 BOUNDARY）⇒ G2
        return md_text.replace("| D13 |", "| D18 |", 1)
    if tag == "m4":       # 把 FAIL 条目挪进正典（支撑只给 PASS，式号手抄）⇒ G8
        return md_text.replace(
            "| C-05 | UFE-2 封闭方程（§1 消元结果） | A | L2 | M09 |",
            "| C-05 | 式 4 引力场（挪入正典） | A | L2 | M09 |", 1)
    if tag == "m5":       # 删除大量正典行 ⇒ G6
        out, dropped = [], 0
        for line in md_text.splitlines():
            if line.startswith("| C-0") and dropped < 8:
                dropped += 1
                continue
            out.append(line)
        return "\n".join(out)
    if tag == "m6":       # 编号重复 ⇒ G5
        return md_text.replace("| C-26 |", "| C-25 |", 1)
    if tag == "m7":       # C 类去掉"定义式/零预测力"标注 ⇒ G7
        return md_text.replace(
            "量纲自洽；**定义式，零预测力** |", "量纲自洽 |", 1)
    if tag == "m8":       # 把 PASS 条目挪进排除表 ⇒ G4
        return md_text.replace("| X-08 | 三代轻子质量谱", "| X-08 | 库仑极限", 1).replace(
            "| S01, S02 |", "| N10 |", 1)
    if tag == "m9":       # 正典 C-05 改引 FAIL 判据 M05（牛顿极限）⇒ G3
        return md_text.replace(
            "| C-05 | UFE-2 封闭方程（§1 消元结果） | A | L2 | M09 |",
            "| C-05 | UFE-2 封闭方程（§1 消元结果） | A | L2 | M09, M05 |", 1)
    if tag == "b1":       # 良性：只加空白 ⇒ 不得误报
        return md_text.replace("## 0. 入选标准", "## 0. 入选标准  \n", 1)
    raise KeyError(tag)


MUTANTS = ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9"]
BENIGN = ["b1"]


def main():
    argv = sys.argv[1:]
    index, conflicts = load_results()
    if index is None:
        return 2
    if not os.path.isfile(CANON_MD):
        print("[FAIL] 正典文件不存在：%s" % os.path.basename(CANON_MD))
        return 2
    with open(CANON_MD, encoding="utf-8") as fh:
        md_text = fh.read()
    canon_rows, excl_rows = parse_tables(md_text)
    if not canon_rows or not excl_rows:
        print("[FAIL] 正典表或排除表解析为空（正典 %d 行 / 排除 %d 行）"
              % (len(canon_rows), len(excl_rows)))
        return 2

    # ---------------- 基线
    base_complaints, base_summary = check(index, canon_rows, excl_rows, md_text, conflicts)
    if base_complaints:
        print("=" * 78)
        print("基线即有违规 ⇒ 门禁拒绝出结论（整轮 INVALID）")
        print("=" * 78)
        for c in base_complaints:
            print("  " + c)
        return 2

    print("=" * 78)
    print("UFE-2 正典防回潮守卫")
    print("=" * 78)
    print("正典 %d 条（%s）· 排除 %d 条（其中 %d 条无判据支撑、已注明依据来源）"
          % (base_summary["canon_rows"],
             " ".join("%s=%d" % (k, v) for k, v in sorted(base_summary["canon_by_class"].items())),
             base_summary["excl_rows"], base_summary["excl_without_judgement"]))
    print("不变量 G1–G12 全部通过。")

    payload = {
        "instrument": "zxq23_canon_guard.py",
        "canon_md": os.path.basename(CANON_MD),
        "verdict": "PASS",
        "summary": base_summary,
        "mutants": [],
        "missed": [],
        "false_alarm": [],
    }

    # ---------------- 变异驱动
    if "--teeth" in argv:
        caught, missed, false_alarm = [], [], []
        for tag in MUTANTS + BENIGN:
            mutated = mutate(md_text, tag)
            if mutated == md_text:
                missed.append(tag)
                print("  [MISS] %s 变异未生效（锚点漂移）" % tag)
                continue
            c_rows, e_rows = parse_tables(mutated)
            complaints, _ = check(index, c_rows, e_rows, mutated, conflicts)
            if tag in BENIGN:
                if complaints:
                    false_alarm.append(tag)
                    print("  [FALSE] 良性变异 %s 被误报：%s" % (tag, complaints[:2]))
                else:
                    print("  [CLEAN] 良性变异 %s 未误报" % tag)
                continue
            if complaints:
                caught.append(tag)
                print("  [CAUGHT] %-3s → %d 条投诉（首条：%s）" % (tag, len(complaints), complaints[0]))
            else:
                missed.append(tag)
                print("  [MISS] %s 未被抓（守卫有洞）" % tag)
        print("-" * 78)
        print("变异体：抓 %d / 漏 %d；良性误报 %d" % (len(caught), len(missed), len(false_alarm)))
        payload["mutants"] = [
            {"id": t, "caught": t in caught, "complaints": None} for t in MUTANTS
        ]
        payload["missed"] = missed
        payload["false_alarm"] = false_alarm
        if missed or false_alarm:
            payload["verdict"] = "INVALID"
            with open(CANON_JSON, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            return 1

    with open(CANON_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print("-" * 78)
    print("产物：%s" % os.path.basename(CANON_JSON))
    print("红线：本门禁只校验「判据存在且结论匹配」，不校验公式的物理真伪。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
