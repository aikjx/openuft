# -*- coding: utf-8 -*-
"""
claims_columns_normalize.py — OpenUFT claims.csv 结构/枚举归一工具
规则：
  * claims.csv 必须为 14 列；evidence_level 在第 12 列、status 在第 13 列（1-based）；
  * 14 列结构不可漂移（增删列 = 错误）；
  * status     ∈ {verified, falsified, open, superseded}
  * evidence_level ∈ {mathematical_result, numerical_check, experimental, observational}
    允许多 token 复合（用 '+' 连接），每个 token 必须在枚举内；
  * claim_id 唯一；script_ref 指向的脚本必须存在（相对仓库根）。
用法：
  python3 claims_columns_normalize.py            # 校验并输出统计
  python3 claims_columns_normalize.py --fix      # 仅做允许的修复（去空白、引号归一），不改结论
"""
import csv
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(REPO, "claims.csv")

HEADER = [
    "claim_id", "system", "section", "claim_zh", "claim_en", "statement",
    "scope", "derivation_ref", "script_ref", "numeric_value", "residual",
    "evidence_level", "status", "last_checked",
]  # 14 列；evidence_level 位于 1-based 第 12 列(index 11)，status 位于 13 列(index 12)

STATUS_ENUM = {"verified", "falsified", "open", "superseded"}
EV_LEVEL_ENUM = {"mathematical_result", "numerical_check", "experimental", "observational"}


def normalize_ev_level(raw):
    tokens = [t.strip() for t in raw.split("+") if t.strip()]
    for t in tokens:
        if t not in EV_LEVEL_ENUM:
            raise ValueError(f"非法 evidence_level token: {t!r}（枚举: {sorted(EV_LEVEL_ENUM)}）")
    return "+".join(tokens)


def main():
    if not os.path.exists(CSV_PATH):
        print(f"[FAIL] 未找到 {CSV_PATH}")
        return 1
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        print("[FAIL] claims.csv 为空")
        return 1
    header = [h.strip() for h in rows[0]]
    if header != HEADER:
        print("[FAIL] 表头与 14 列规范不符")
        print(f"  规范: {HEADER}")
        print(f"  实际: {header}")
        return 1

    errors, seen_ids = [], set()
    stats = {s: 0 for s in STATUS_ENUM}
    ev_stats = {}
    for i, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue
        if len(row) != 14:
            errors.append(f"第 {i} 行列数 = {len(row)}（应为 14，禁止列漂移）")
            continue
        cid, ev, st = row[0].strip(), row[11].strip(), row[12].strip()
        if not cid:
            errors.append(f"第 {i} 行 claim_id 为空")
        elif cid in seen_ids:
            errors.append(f"第 {i} 行 claim_id 重复: {cid}")
        seen_ids.add(cid)
        if st not in STATUS_ENUM:
            errors.append(f"第 {i} 行 status={st!r} 非法（枚举: {sorted(STATUS_ENUM)}）")
        else:
            stats[st] += 1
        try:
            ev = normalize_ev_level(ev)
        except ValueError as e:
            errors.append(f"第 {i} 行 {e}")
        ev_stats[ev] = ev_stats.get(ev, 0) + 1
        # script_ref 存在性
        sr = row[8].strip()
        if sr and not sr.startswith(("http", "§", "见")):
            p = os.path.join(REPO, sr)
            if not os.path.exists(p):
                errors.append(f"第 {i} 行 script_ref 不存在: {sr}")

    if errors:
        print("[FAIL] claims.csv 校验未通过:")
        for e in errors:
            print("  -", e)
        return 1

    print("[PASS] claims.csv 结构与枚举全部合规")
    print(f"  claim 总数: {len(seen_ids)}")
    print(f"  status 分布: {stats}")
    print(f"  evidence_level 分布: {ev_stats}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
