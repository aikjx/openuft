# -*- coding: utf-8 -*-
"""
claims.csv schema 升级工具（check / apply / revert）
====================================================
依据 `缺漏诊断与新体系立项评估_2026-09-18.md §六.1`：把"登记无量纲预测"从
可选叙述变为**入库必填项**，UFT-3 才能被自动审计。

新列：
  - prediction_value : 无量纲靶的**预测数值** v_pred（空 = 未登记）
  - prediction_urel  : **相对误差棒** u_rel（空 = 未登记）

用法：
  python claims_schema_升级.py --check     # 只审计：schema 是否存在 + 各文件行宽分布
  python claims_schema_升级.py --apply     # 幂等加列（插在 prediction 与 run_id 之间）
  python claims_schema_升级.py --revert    # 回退（删除两列，恢复原状）

**安全设计（关键）**：新列插在 `prediction` 与 `run_id` 之间——**不追加到行尾**。
于是每行的行末两列仍是 (status, reviewer)，`体系健康度归一化总览.py` 与
`全维体系_第一性审查.py` 依赖的 `line[-2]` 定位不受影响。
**但**：若某文件的原行宽 ≠ 表头列数（既存"列错位"），`--apply` 会**拒绝**改动该文件的
数据行（只提示），因为它无法在错位行上安全插列。请先修列错位再 apply。

实现：文本级 quote-aware 插入（不做全量 CSV 重写），diff 仅"每行多两个逗号"。
"""
import os
import sys
import json
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # -> openuft
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")

NEW_COLS = ["prediction_value", "prediction_urel"]
ANCHOR = "run_id"          # 新列插在 run_id 之前（即紧接 prediction 之后）


def split_fields(line):
    """quote-aware 拆字段，保留原始引号，保证 rejoin 后文本零漂移。"""
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


def width_profile(lines):
    w = [len(split_fields(x)) for x in lines[1:] if x != ""]
    return Counter(w)


# ----------------------------- check -----------------------------
def do_check(systems):
    print("=" * 84)
    print("claims.csv 列对齐审计（--check）：schema 是否含新列 + 行宽分布")
    print("=" * 84)
    has_cols = 0
    misaligned = []
    for s in systems:
        p = os.path.join(ROOT, "01_独立体系", s["directory"], "claims.csv")
        if not os.path.isfile(p):
            print("  [--] %-40s 无 claims.csv" % s["id"])
            continue
        lines, _ = read_lines(p)
        hdr = lines[0].split(",")
        hlen = len(hdr)
        prof = width_profile(lines)
        ok_schema = all(c in hdr for c in NEW_COLS)
        has_cols += 1 if ok_schema else 0
        nrow = sum(prof.values())
        bad = sum(v for k, v in prof.items() if k != hlen)
        flag = "" if bad == 0 else "  <== 列错位 %d/%d 行" % (bad, nrow)
        if bad:
            misaligned.append((s["id"], bad, nrow))
        print("  %-42s 表头=%d 行宽=%s 新列=%s%s"
              % (s["id"], hlen, dict(prof), "有" if ok_schema else "无", flag))
    print("-" * 84)
    print("含新列的文件：%d/18；列错位文件：%d 个" % (has_cols, len(misaligned)))
    if misaligned:
        print("列错位明细：" + "；".join("%s %d/%d" % t for t in misaligned))
        print("⇒ 建议先修列错位，再 --apply（工具已拒绝在错位行上插列）。")
    return 0


# ----------------------------- apply -----------------------------
def do_apply(systems):
    print("=" * 84)
    print("claims.csv schema 升级：新增 %s / %s（插在 %s 之前）" % (NEW_COLS[0], NEW_COLS[1], ANCHOR))
    print("=" * 84)
    st = {"upgraded": 0, "already": 0, "empty": 0, "no-anchor": 0, "missing": 0, "blocked": 0}
    total_bad = 0
    for s in systems:
        p = os.path.join(ROOT, "01_独立体系", s["directory"], "claims.csv")
        if not os.path.isfile(p):
            st["missing"] += 1
            print("  [--] %-40s 无 claims.csv（方向占位）" % s["id"])
            continue
        lines, crlf = read_lines(p)
        if not lines or not lines[0].strip():
            st["empty"] += 1
            print("  [--] %-40s 空表" % s["id"])
            continue
        cols = lines[0].split(",")
        if all(c in cols for c in NEW_COLS):
            st["already"] += 1
            print("  [OK] %-40s 已含新列" % s["id"])
            continue
        if ANCHOR not in cols:
            st["no-anchor"] += 1
            print("  [!!] %-40s 缺锚 %s" % (s["id"], ANCHOR))
            continue
        pos = cols.index(ANCHOR)
        ncol = len(cols)
        prof = width_profile(lines)
        bad = sum(v for k, v in prof.items() if k != ncol)
        total_bad += bad
        # 错位行无法安全插列：保守起见，若有错位则拒绝改动该文件
        if bad:
            st["blocked"] += 1
            print("  [BL] %-40s 拒绝：列错位 %d 行（先修齐再 apply）" % (s["id"], bad))
            continue
        lines[0] = ",".join(cols[:pos] + NEW_COLS + cols[pos:])
        for k in range(1, len(lines)):
            if lines[k] == "":
                continue
            f = split_fields(lines[k])
            f[pos:pos] = ["", ""]
            lines[k] = ",".join(f)
        write_lines(p, lines, crlf)
        st["upgraded"] += 1
        print("  [UP] %-40s upgraded" % s["id"])
    print("-" * 84)
    print("升级 %d · 已含 %d · 空表 %d · 缺锚 %d · 无文件 %d · 因列错位拒绝 %d（错位行合计 %d）"
          % (st["upgraded"], st["already"], st["empty"], st["no-anchor"], st["missing"],
             st["blocked"], total_bad))
    return 0 if st["no-anchor"] == 0 else 1


# ----------------------------- revert -----------------------------
def do_revert(systems):
    print("=" * 84)
    print("claims.csv schema 回退：删除 %s / %s" % (NEW_COLS[0], NEW_COLS[1]))
    print("=" * 84)
    n = 0
    for s in systems:
        p = os.path.join(ROOT, "01_独立体系", s["directory"], "claims.csv")
        if not os.path.isfile(p):
            continue
        lines, crlf = read_lines(p)
        hdr = lines[0].split(",")
        if not all(c in hdr for c in NEW_COLS):
            continue
        pos = hdr.index(NEW_COLS[0])
        nc = len(hdr)
        lines[0] = ",".join(c for c in hdr if c not in NEW_COLS)
        for k in range(1, len(lines)):
            if lines[k] == "":
                continue
            f = split_fields(lines[k])
            if len(f) == nc and f[pos] == "" and f[pos + 1] == "":
                del f[pos:pos + 2]
                lines[k] = ",".join(f)
        write_lines(p, lines, crlf)
        n += 1
        print("  [RV] %-40s reverted" % s["id"])
    print("-" * 84)
    print("回退文件数：%d" % n)
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    reg = json.load(open(REG, encoding="utf-8"))
    systems = reg["systems"]
    if mode == "--check":
        return do_check(systems)
    if mode == "--apply":
        return do_apply(systems)
    if mode == "--revert":
        return do_revert(systems)
    print("用法：python claims_schema_升级.py [--check|--apply|--revert]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
