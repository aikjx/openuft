#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
apply_remap.py —— 列重映射执行器（OPEN-B8/B9/B10，批准后执行）
========================================================================
dry-run（默认）：预览将执行的改动，不改任何文件。
--apply：改写 CURATED 真源（S14 claims.csv 右移还原）。

S14 还原规则（已实证，行152 样本）：
  15 列右移行 → 还原为 14 列：new = r[0:8] + r[9:15]
  （丢弃 r[8] 空列；col8-13 依次左移 1 列：run_id←r[9], data_id←r[10],
   uncertainty←r[11], evidence_level←r[12], status←r[13], reviewer←r[14]）

S15/S17：单字母分级（O/C/H/U）映射待所属方选 A/B，脚本仅 dry-run 输出清单，不执行。

用法：python -B 00_项目治理/维护工具/apply_remap.py [--apply] [--strip-blank]
退出码：0 = 预览完成；1 = 有模式不符需人工复核
"""
from __future__ import print_function
import csv
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_here = Path(__file__).resolve()
ROOT = next((p for p in _here.parents if (p / "01_独立体系").is_dir()), _here.parents[2])
S14 = ROOT / "01_独立体系/S14_挠率统一场论TUFT/claims.csv"
S15 = ROOT / "01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/claims.csv"
S17 = ROOT / "01_独立体系/S17_统一场论核心公式/claims.csv"


def load(p):
    return list(csv.reader(p.open(encoding="utf-8", newline="")))


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    mode = "APPLY（改写真源）" if apply else "dry-run（仅预览）"
    print("=" * 64)
    print("列重映射执行器 | 模式: %s" % mode)
    print("=" * 64)

    # —— S14：15 列右移行还原 ——
    rows = load(S14)
    header, ncols = rows[0], len(rows[0])
    out, changed, skipped, bad = [header], [], [], []
    for i, r in enumerate(rows[1:], start=2):
        if not r or len(r) == ncols:
            out.append(r)
            continue
        if len(r) != 15:
            skipped.append((i, len(r)))
            out.append(r)
            continue
        if r[8].strip():
            bad.append((i, "col8(run_id)非空，右移模式不符"))
            out.append(r)
            continue
        new = r[0:8] + r[9:15]
        changed.append((i, r, new))
        out.append(new)
    print("== S14 claims.csv 右移还原（15列→14列） ==")
    print("  待还原右移行: %d | 跳过(非15列): %d | 模式不符: %d" % (len(changed), len(skipped), len(bad)))
    for i, old, new in changed:
        print("  行%d  run_id=%s evidence=%s status=%s reviewer=%s"
              % (i, new[8][:20], new[11][:14], new[12][:12], new[13][:12]))
    for s in bad[:5]:
        print("  [复核] 行%d: %s" % s)
    for s in skipped[:3]:
        print("  [skip] 行%d: 列数%d" % s)
    if apply and changed:
        with S14.open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerows(out)
        print("  → S14 已改写 %d 行（CURATED 真源）" % len(changed))
    else:
        print("  （dry-run，未改文件；确认后加 --apply 执行）")

    # —— S15/S17：单字母清单（待裁定 A/B，不执行） ——
    for key, p in (("S15", S15), ("S17", S17)):
        rr = load(p)
        hdr = rr[0]
        ei = hdr.index("evidence_level")
        single = [(i, r[0], r[ei].strip(), r[hdr.index("status")].strip() if "status" in hdr and len(r) > hdr.index("status") else "")
                  for i, r in enumerate(rr[1:], start=2)
                  if r and len(r) == len(hdr) and len(r[ei].strip()) == 1]
        print("== %s evidence_level 单字母（%d 行，待选 A/B，不执行） ==" % (key, len(single)))
        from collections import Counter
        for v, c in Counter(s[2] for s in single).most_common():
            print("    单字母 %s: %d 行" % (v, c))
    print("=" * 64)
    print("预览完成 —— 执行需：1) 所属方批准  2) 加 --apply")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
