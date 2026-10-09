#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
claims.csv 列数鲁棒对齐修复工具（schema 自适应版）
=================================================
历史问题：部分体系的 claims.csv 在 statement 列含未转义逗号，导致用
固定列数解析时列错位（如 s12/s13 曾出现 rows 列数 = 11/12、10/11/17，
header = 12）。本工具用 csv 模块正确解析（处理引号），并对列数不符的
行做鲁棒归位：
  - 字段数 < 表头列数：尾部补空列（不破坏内容）。
  - 字段数 > 表头列数：多出的字段来自 statement 列的未转义逗号，
    将其并回 statement（索引 2）；若仍超出则继续并入，直到收敛。
  - 字段数 == 表头列数：保持不变（绝不改写已对齐文件）。

关键改进（相对旧版硬编码 NCOL=12）：
  - 表头列数 NCOL 逐文件动态读取，兼容 12 列 / 14 列 / 任意未来 schema。
  - 仅当确有行被改动时才回写文件，避免无谓改动与行尾差异。
  - 支持 --dry 预览（不落盘）。

用法：
  python claims_列对齐修复.py            # 扫描 01_独立体系 下全部 claims.csv 并修复
  python claims_列对齐修复.py --dry      # 仅报告，不落盘
"""
import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # openuft
SYS_DIR = ROOT / "01_独立体系"
STATEMENT_IDX = 2                                   # statement 列允许含逗号

DRY = "--dry" in sys.argv


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    if DRY:
        return
    path.write_text(text, encoding="utf-8")


def align_row(fields, ncol):
    """返回 (归位后的字段列表, 是否改动)。"""
    n = len(fields)
    if n == ncol:
        return fields, False
    if n < ncol:
        # 字段不足：尾部补空（数据未丢，仅占位补齐）
        return fields + [""] * (ncol - n), True
    # n > ncol：多出的字段来自 statement 的未转义逗号，并回 statement 列
    extra = n - ncol
    merged = ",".join(fields[STATEMENT_IDX:STATEMENT_IDX + extra + 1])
    new = (fields[:STATEMENT_IDX]
           + [merged]
           + fields[STATEMENT_IDX + extra + 1:])
    if len(new) > ncol:
        # 极端多逗号：继续递归并入 statement，直至收敛
        return align_row(new, ncol)
    return new, True


def fix_one(path: Path):
    text = read_text(path)
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return 0
    header = rows[0]
    ncol = len(header)
    out = [header]
    changed = 0
    for r in rows[1:]:
        if not r:                       # 保留空行
            out.append([])
            continue
        new, ch = align_row(r, ncol)
        if ch:
            changed += 1
        out.append(new)
    if changed:
        buf = io.StringIO()
        w = csv.writer(buf)
        for r in out:
            w.writerow(r)
        write_text(path, buf.getvalue())
    return changed


def main():
    paths = sorted(SYS_DIR.glob("*/claims.csv"))
    total_changed = 0
    print(f"[claims_列对齐修复] 扫描目录: {SYS_DIR}")
    print(f"[claims_列对齐修复] 模式: {'dry-run(不落盘)' if DRY else '修复并落盘'}")
    for p in paths:
        before = p.stat().st_mtime
        changed = fix_one(p)
        flag = "CHANGED" if changed else "ok"
        print(f"  [{flag}] {p.parent.name:40s} 改动行={changed}")
        if changed:
            total_changed += 1
    print(f"[claims_列对齐修复] 完成：{len(paths)} 个文件，{total_changed} 个需要/已修复。")
    return total_changed


if __name__ == "__main__":
    main()
