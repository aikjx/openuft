#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
claims_columns_audit.py —— claims.csv 列语义对账审计
======================================================
自动演化引擎的「列语义健康分析」：对活跃 01_独立体系 各 claims.csv 逐列统计值形态，
识别列语义串列（evidence_level 被 uncertainty 污染、status 被 evidence 词串列、
reviewer 被分级字母串列等），输出每体系精确的列语义健康报告 —— 为 OPEN-B8/B9/B10
（列错位裁定）提供可核验证据。

形态分类：short=<16字(词/字母)  long=>=16字  num=纯数字  empty=空
串列规则（仅报告证据，不擅自改真源）：
  · evidence_level 列出现 long 文本 → 疑 uncertainty 串列
  · evidence_level 列为单字母 → 疑 reviewer 分级串列
  · status 列值 ∈ evidence 词表 → 疑 evidence_level 串列
  · reviewer 列值 ∈ {H,O,C,U} → 疑分级字母串列（reviewer 应为人/角色）

用法：python -B 00_项目治理/维护工具/claims_columns_audit.py [--json]
退出码：0 = 分析完成（审计不判定 PASS/FAIL，仅报告证据）
"""
from __future__ import print_function

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_here = Path(__file__).resolve()
# parents[0]=维护工具, parents[1]=00_项目治理, parents[2]=openuft；带存在性校验定位根
ROOT = next((p for p in _here.parents if (p / "01_独立体系").is_dir()), _here.parents[2])
EVIDENCE_WORDS = {
    "mathematical_result", "numerical_check", "conjecture", "structural",
    "mathematical_check", "experimental_constraint", "observational_check",
    "numerical_result", "structural_claim", "methodological", "observational",
    "mathematical_framework", "review", "hypothesis", "verified",
}
GRADE_LETTERS = set("OCHU")
STATUS_WORDS = {"open", "falsified", "verified", "partial", "closed", "rejected", "unreviewed", "pending"}
# 检测目标列
TARGET = ("prediction", "prediction_value", "prediction_urel", "uncertainty",
          "evidence_level", "status", "reviewer", "data_id", "run_id")


def shape(v):
    v = v.strip()
    if not v:
        return "empty"
    if re.fullmatch(r"[+-]?[\d.]+(?:[eE][+-]?\d+)?", v):
        return "num"
    if len(v) >= 16:
        return "long"
    return "short"


def audit_one(csvf):
    rel = csvf.relative_to(ROOT).as_posix()
    try:
        rows = list(csv.reader(csvf.open(encoding="utf-8", newline="")))
    except Exception as e:
        return {"file": rel, "err": str(e)}
    if not rows:
        return {"file": rel, "err": "empty"}
    header = rows[0]
    out = {"file": rel, "header_cols": len(header), "data_rows": 0, "header": header}
    shape_by_col = {h: Counter() for h in TARGET if h in header}
    samples = {h: [] for h in TARGET if h in header}
    col_idx = {h: header.index(h) for h in TARGET if h in header}
    for r in rows[1:]:
        if not r:
            continue
        out["data_rows"] += 1
        for h, idx in col_idx.items():
            if idx < len(r):
                v = r[idx].strip()
                if not v:
                    continue
                shape_by_col[h][shape(v)] += 1
                if len(samples[h]) < 4:
                    samples[h].append(v[:26])
    # 串列证据
    flags = []
    if "evidence_level" in shape_by_col:
        c = shape_by_col["evidence_level"]
        if c.get("long"):
            flags.append("evidence_level 列 %d 个长文本(≥16字) → 疑 uncertainty 串列" % c["long"])
        letters = [s for s in samples.get("evidence_level", []) if len(s.strip()) == 1 and s.strip().upper() in GRADE_LETTERS]
        if letters:
            flags.append("evidence_level 列单字母分级 %s → 疑 reviewer 分级串列" % sorted(set(letters)))
    if "status" in shape_by_col:
        # 仅当 status 值属证据词表且非合法状态词时才判定串列；verified 等合法状态不误报
        ev_in_status = [s for s in samples.get("status", [])
                        if (s.lower().strip() in EVIDENCE_WORDS and s.lower().strip() not in STATUS_WORDS) or "+" in s]
        if ev_in_status:
            flags.append("status 列出现证据词 %s → 疑 evidence_level 串列" % ev_in_status)
    if "reviewer" in shape_by_col:
        letters = [s for s in samples.get("reviewer", []) if len(s.strip()) == 1 and s.strip().upper() in GRADE_LETTERS]
        if letters:
            flags.append("reviewer 列单字母分级 %s → 疑分级字母串列（reviewer 应为人/角色）" % sorted(set(letters)))
    if "uncertainty" in shape_by_col:
        c = shape_by_col["uncertainty"]
        if c.get("long"):
            flags.append("uncertainty 列 %d 个长文本（uncertainty 建议短语义，供参考）" % c["long"])
    out["col_shapes"] = {h: dict(c) for h, c in shape_by_col.items()}
    out["col_samples"] = {h: s for h, s in samples.items()}
    out["flags"] = flags
    return out


def main():
    want_json = "--json" in sys.argv[1:]
    results = []
    for f in sorted((ROOT / "01_独立体系").rglob("claims.csv")):
        results.append(audit_one(f))
    if want_json:
        print(json.dumps(results, ensure_ascii=False))
        return 0
    # —— 表头归一化对账：找出权威表头（出现频率最高），量化体系间 schema 一致性 ——
    valid = [r for r in results if "header" in r]
    headers = Counter(tuple(r["header"]) for r in valid)
    authoritative, auth_cnt = headers.most_common(1)[0]
    devs = [r for r in valid if tuple(r["header"]) != authoritative]
    header_diff = []  # (file, 缺失列, 多余列, 顺序差异)
    for r in valid:
        h = tuple(r["header"])
        if h == authoritative:
            continue
        missing = [c for c in authoritative if c not in h]
        extra = [c for c in h if c not in authoritative]
        # 顺序差异：相对权威表头中同列的出现位置偏移
        order_shift = []
        for i, c in enumerate(h):
            if c in authoritative:
                j = authoritative.index(c)
                if j != i:
                    order_shift.append("%s@%d" % (c, j))
        header_diff.append((r["file"], missing, extra, order_shift))
    print("=" * 64)
    print("表头归一化对账（权威表头 · 出现 %d/%d 体系）" % (auth_cnt, len(valid)))
    print("  权威列数: %d" % len(authoritative))
    print("  权威列序: %s" % " | ".join(authoritative))
    if devs:
        print("  ── 偏离体系 %d 个（列数/列名/顺序与权威不一致） ──" % len(header_diff))
        for file, missing, extra, order_shift in header_diff:
            print("   ◆ %s" % file)
            if missing:
                print("      缺列: %s" % ", ".join(missing))
            if extra:
                print("      多列: %s" % ", ".join(extra))
            if order_shift:
                print("      顺序偏移: %s" % ", ".join(order_shift))
    else:
        print("  ✓ 全部体系表头一致 —— 归一化达成")
    print("=" * 64)
    print("claims.csv 列语义对账审计（活跃 01_独立体系）")
    print("=" * 64)
    for r in results:
        print("\n◆ %s  (%d 列 / %d 数据行)" % (r.get("file", "?"), r.get("header_cols", 0), r.get("data_rows", 0)))
        if r.get("err"):
            print("   ERR: %s" % r["err"])
            continue
        for h, shapes in r.get("col_shapes", {}).items():
            if shapes:
                print("   %-18s %s" % (h, ", ".join("%s=%d" % kv for kv in shapes.items())))
        if r.get("flags"):
            for fl in r["flags"]:
                print("   ⚠ %s" % fl)
        else:
            print("   ✓ 列语义健康（无串列证据）")
    print("\n" + "=" * 64)
    print("审计完成 —— 证据仅供 OPEN-B8/B9/B10 列语义裁定，未篡改任何真源")
    return 0


if __name__ == "__main__":
    sys.exit(main())
