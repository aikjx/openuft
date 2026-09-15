# -*- coding: utf-8 -*-
"""claims.csv 列数规范化（可复跑，非破坏性）

背景：仓库内 claims.csv 的 header 为 12 列，但历史数据行多为 11 列
（S12 rows=[11,12]、S13 rows=[10,11,17]），未转义英文逗号会导致**列错位**，
固定列号读取会静默误判（算法联盟已改用"行末两列定位 status"来规避）。

本工具：把指定体系 claims.csv 的**数据行**规范化为固定列数（默认 11，与仓库惯例一致）：
  - 多出的字段合并进 statement（第 3 列），用中文全角"，"连接 —— **不丢内容**；
  - 字段数已等于目标的行原样保留；
  - 不足目标的行不处理（仅告警），避免臆造内容。

用法：
  python claims_columns_normalize.py --system S14_挠率统一场论TUFT --target 11
  python claims_columns_normalize.py --system S14_挠率统一场论TUFT --check    # 只检查不改
"""
import argparse
import csv
import io
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYSTEMS = ROOT / "01_独立体系"

try:  # Windows GBK 控制台无法输出 ✅ 等字符
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def normalize(path, target=11, write=True):
    rows = list(csv.reader(io.open(path, encoding="utf-8-sig", newline="")))
    if not rows:
        return [], []
    header = rows[0]
    out, changes, warns = [header], [], []
    for idx, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        if len(row) == target:
            out.append(row)
            continue
        if len(row) > target:
            n_extra = len(row) - target
            merged = "，".join(row[2:2 + n_extra + 1])
            new = row[:2] + [merged] + row[2 + n_extra + 1:]
            if len(new) != target:  # 理论不会发生，保险
                warns.append("行 %d 规范化后仍为 %d 列（跳过）" % (idx, len(new)))
                out.append(row)
                continue
            out.append(new)
            changes.append("行 %d：%d → %d 列（合并 %d 个字段到 statement）"
                           % (idx, len(row), len(new), n_extra))
        else:
            warns.append("行 %d 仅 %d 列（< %d，未处理，需人工补字段）" % (idx, len(row), target))
            out.append(row)
    if write and changes:
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, lineterminator="\n")
            writer.writerows(out)
    return changes, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--system", required=True, help="体系中文目录名，如 S14_挠率统一场论TUFT")
    ap.add_argument("--target", type=int, default=11)
    ap.add_argument("--check", action="store_true", help="只检查不改")
    args = ap.parse_args()

    path = SYSTEMS / args.system / "claims.csv"
    if not path.is_file():
        print("未找到: " + str(path))
        return True
    changes, warns = normalize(path, args.target, write=not args.check)
    print("文件: %s（目标 %d 列，模式=%s）" % (path.as_posix(), args.target,
                                             "检查" if args.check else "写入"))
    for c in changes:
        print("  [fix] " + c)
    for w in warns:
        print("  [warn] " + w)
    if not changes and not warns:
        print("  ✅ 所有数据行已是 %d 列" % args.target)
    return False


if __name__ == "__main__":
    sys.exit(main())
