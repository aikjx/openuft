# -*- coding: utf-8 -*-
"""
claims.csv 列对齐修复（全维 · 约束式智能对齐 v2）
==================================================
问题：s06/s12/s13/s14 的 claims.csv 有**既存列错位**——
  * 多数行比表头**少 1–2 列**：缺的恒是 `prediction`（及个别中间列）；
  * 少数行因语句里**未转义逗号**（如 `Cl(4,4)`、`{0,0,0,8κv²}`）而**多**若干字段。

对齐模型（12 列）：
  claim_id, hypothesis_revision, statement, assumptions, derivation,
  prediction, run_id, data_id, uncertainty, evidence_level, status, reviewer

规则（不靠猜，带自校验）：
  * 短行 (k<12)：在 **index 5（derivation 之后）补 (12-k) 个空字段**——缺的恰是常为空的
    prediction/run_id/data_id；
  * 等长 (k=12)：不动；
  * 长行 (k>12)：**DP 最优分段**把 k 个原始字段划成 12 段（段内用逗号拼回），
    硬锚：段0 匹配 `^[SP]\\d+-C\\d+$`、段9 ∈ EVIDENCE、段10 ∈ STATUS；
    软评分：statement 偏长、derivation 含路径符。
  * 任一行对齐后**两端锚复验不过 → 标记 UNRESOLVED，不写**。

用法：
  python claims_列对齐修复.py --dry-run   # 只诊断（默认）
  python claims_列对齐修复.py --fix       # 就地写回（仅通过复验的行）
"""
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # -> openuft
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")

CLAIM_RE = re.compile(r"^[SP]\d+-C\d+$")
EVID = {"mathematical_result", "numerical_check", "mathematical_check", "conjecture",
        "numerical_result", "experimental"}
STAT = {"verified", "falsified", "unreviewed", "unreproduced", "repaired", "open"}
NCOL = 12
NEG = -1e9


def split_fields(line):
    fields, cur, inq, i = [], [], False, 0
    while i < len(line):
        ch = line[i]
        if inq:
            cur.append(ch)
            if ch == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    cur.append('"')
                    i += 1
                else:
                    inq = False
        else:
            if ch == '"':
                inq = True
                cur.append(ch)
            elif ch == ",":
                fields.append("".join(cur))
                cur = []
            else:
                cur.append(ch)
        i += 1
    fields.append("".join(cur))
    return fields


def csv_join(fields):
    """按 CSV 规则拼接：含逗号/引号/换行的字段加引号（内部引号翻倍）。"""
    out = []
    for f in fields:
        if ("," in f) or ('"' in f) or ("\n" in f):
            out.append('"' + f.replace('"', '""') + '"')
        else:
            out.append(f)
    return ",".join(out)


def score(col, text, n):
    """col: 0..11；text: 段内拼接文本；n: 段内原始字段数。"""
    if col == 0:                                   # claim_id
        return 1000 if (n == 1 and CLAIM_RE.match(text.strip())) else (NEG if n == 0 else -800)
    if col == 9:                                   # evidence_level（硬）
        if n == 0:
            return NEG
        return 200 if text.strip() in EVID else NEG
    if col == 10:                                  # status（硬）
        if n == 0:
            return NEG
        return 200 if text.strip() in STAT else NEG
    if col == 1:                                   # hypothesis_revision
        if n == 0:
            return -500
        return 60 if re.match(r"^[A-Za-z0-9._\-]{1,24}$", text.strip()) else -80
    if col == 2:                                   # statement：偏长
        return -500 if n == 0 else min(len(text), 800) / 8.0
    if col == 3:                                   # assumptions
        return 0 if n == 0 else (50 if re.search(r"[AP]\d", text) else 0)
    if col == 4:                                   # derivation
        return 0 if n == 0 else (50 if ("/" in text or "#" in text or ";" in text) else -30)
    if col == 5:                                   # prediction
        return 0 if n == 0 else (15 if (text == "" or "/" in text or "=" in text) else 0)
    if col == 6:                                   # run_id
        return 0 if n == 0 else (20 if ("run" in text or "template" in text) else
                                 (10 if "/" in text or text == "" else 0))
    if col == 7:                                   # data_id
        return 0 if n == 0 else (10 if (text == "" or "/" in text) else 0)
    if col == 8:                                   # uncertainty
        return 0 if n == 0 else min(len(text), 200) / 40.0
    if col == 11:                                  # reviewer
        return 20 if (n == 0 or text == "" or "ALG" in text or len(text) <= 24) else -20
    return 0


def dp_align(fields):
    """DP：把 k 个字段划成 12 段（可含空段），硬锚 + 软评分。返回 (groups, ok)。"""
    k = len(fields)
    dp = [[NEG] * (k + 1) for _ in range(NCOL + 1)]
    bk = [[-1] * (k + 1) for _ in range(NCOL + 1)]
    dp[0][0] = 0.0
    for g in range(1, NCOL + 1):
        for i in range(0, k + 1):
            best, bj = NEG, -1
            for j in range(0, i + 1):
                s = score(g - 1, ",".join(fields[j:i]), i - j)
                if s <= NEG:
                    continue
                v = dp[g - 1][j] + s
                if v > best:
                    best, bj = v, j
            dp[g][i], bk[g][i] = best, bj
    if dp[NCOL][k] <= NEG:
        return None, False
    groups, i = [], k
    for g in range(NCOL, 0, -1):
        j = bk[g][i]
        if j < 0:
            return None, False
        groups.append(",".join(fields[j:i]))
        i = j
    groups.reverse()
    ok = (CLAIM_RE.match(groups[0].strip()) is not None
          and groups[9].strip() in EVID and groups[10].strip() in STAT)
    return groups, ok


def align(fields):
    k = len(fields)
    if not CLAIM_RE.match(fields[0].strip()):
        return fields, "bad-head", False
    if k == NCOL:
        return fields, "ok", True
    if k < NCOL:
        n = NCOL - k
        out = fields[:5] + [""] * n + fields[5:]
        ok = (len(out) == NCOL and out[9].strip() in EVID and out[10].strip() in STAT)
        return out, "pad %d@5" % n, ok
    groups, ok = dp_align(fields)
    if groups is None:
        return fields, "dp-infeasible", False
    return groups, "dp(%d->12)" % k, ok


def read_lines(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    crlf = "\r\n" in raw
    return raw.replace("\r\n", "\n").split("\n"), crlf


def write_lines(path, lines, crlf):
    out = "\n".join(lines)
    if crlf:
        out = out.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)


def process(systems, fix):
    print("=" * 96)
    print("claims.csv 列对齐修复 v2（%s）" % ("FIX 就地写回" if fix else "DRY-RUN 只诊断"))
    print("=" * 96)
    tot_fix = tot_unres = 0
    for s in systems:
        p = os.path.join(ROOT, "01_独立体系", s["directory"], "claims.csv")
        if not os.path.isfile(p):
            continue
        lines, crlf = read_lines(p)
        if not lines or not lines[0].strip():
            continue
        hlen = len(lines[0].split(","))
        rows, changed = [], 0
        for k in range(1, len(lines)):
            if lines[k] == "":
                rows.append(lines[k])
                continue
            f = split_fields(lines[k])
            if len(f) == hlen:
                rows.append(lines[k])
                continue
            out, how, ok = align(f)
            if ok:
                changed += 1
                tot_fix += 1
                rows.append(csv_join(out))
                print("  [FIX] %-14s k=%-2d -> 12  (%s)" % (f[0], len(f), how))
                if how.startswith("dp"):
                    for c in range(NCOL):
                        seg = out[c]
                        print("        %-18s = %s" % (["claim_id", "hyp_rev", "statement", "assumptions",
                                                       "derivation", "prediction", "run_id", "data_id",
                                                       "uncertainty", "evidence", "status", "reviewer"][c],
                                                      (seg[:90] + "…") if len(seg) > 90 else seg))
            else:
                tot_unres += 1
                rows.append(lines[k])
                print("  [!!!] %-14s k=%-2d -> UNRESOLVED (%s)  # 人工复核" % (f[0], len(f), how))
        if fix and changed:
            write_lines(p, [lines[0]] + rows, crlf)
            print("  >>> 写回 %s（修复 %d 行）" % (s["id"], changed))
    print("-" * 96)
    print("可自动修复行：%d；UNRESOLVED（需人工）：%d" % (tot_fix, tot_unres))
    if not fix and tot_fix:
        print("⇒ 复核无误后 --fix；随后 claims_schema_升级.py --apply。")
    return 0


def main():
    reg = json.load(open(REG, encoding="utf-8"))
    return process(reg["systems"], "--fix" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
