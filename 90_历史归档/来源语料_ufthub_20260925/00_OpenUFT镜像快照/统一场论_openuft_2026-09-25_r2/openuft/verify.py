# -*- coding: utf-8 -*-
"""
verify.py — OpenUFT 仓库门禁（结构契约校验）
用法:  python3 -B verify.py
检查项:
  [1] claims.csv 结构与枚举合规（14 列、evidence_level@12、status@13、引用存在）
  [2] module catalog 结构校验（system.json 全量快照 vs 当前派生视图，无漂移）
  [3] markdown 断链检查（含 LaTeX 误报豁免：含 $ 或 \\( 的行跳过；
      目标含 \times 等数学记号视为算式非路径）
任一 FAIL → 退出码 1。
"""
import csv
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))

# ---------------- [1] claims ----------------
def check_claims():
    from claims_columns_normalize import HEADER, STATUS_ENUM, EV_LEVEL_ENUM, CSV_PATH
    if not os.path.exists(CSV_PATH):
        return ["claims.csv 缺失"]
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return ["claims.csv 为空"]
    if [h.strip() for h in rows[0]] != HEADER:
        return ["claims.csv 表头不符 14 列规范"]
    errs, seen = [], set()
    for i, row in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in row):
            continue
        if len(row) != 14:
            errs.append(f"第{i}行列数={len(row)}")
            continue
        cid, ev, st = row[0].strip(), row[11].strip(), row[12].strip()
        if not cid:
            errs.append(f"第{i}行 claim_id 空")
        if cid in seen:
            errs.append(f"第{i}行 claim_id 重复 {cid}")
        seen.add(cid)
        if st not in STATUS_ENUM:
            errs.append(f"第{i}行 status={st!r} 非法")
        for t in ev.split("+"):
            if t.strip() not in EV_LEVEL_ENUM:
                errs.append(f"第{i}行 evidence_level token {t!r} 非法")
        sr = row[8].strip()
        if sr and not sr.startswith(("http", "§", "见")):
            if not os.path.exists(os.path.join(REPO, sr)):
                errs.append(f"第{i}行 script_ref 不存在: {sr}")
    return errs

# ---------------- [2] module catalog ----------------
def check_catalog():
    import module_catalog
    issues, _ = module_catalog.check()
    return issues or []

# ---------------- [3] broken links ----------------
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def is_math_line(line):
    return ("$" in line) or ("\\(" in line)


def is_math_target(t):
    return any(k in t for k in ("\\", "times", "cdot", "frac", "{", "}"))


def check_links():
    errs = []
    for root, _dirs, files in os.walk(REPO):
        if ".registry" in root or ".git" in root or "书籍" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            with open(path, encoding="utf-8") as f:
                for ln, line in enumerate(f, 1):
                    if is_math_line(line):
                        continue
                    for m in LINK_RE.finditer(line):
                        t = m.group(1)
                        if t.startswith(("http://", "https://", "#", "mailto:")):
                            continue
                        if is_math_target(t):
                            continue  # 算式被误判为链接（如 SO10 的 (3\times16)）
                        p = os.path.join(REPO, t)
                        if not os.path.exists(p):
                            errs.append(f"{os.path.relpath(path, REPO)}:{ln} -> {t}")
    return errs

# ---------------- main ----------------
def main():
    fails = []
    c = check_claims()
    if c:
        fails.append(("[1] claims", c))
    else:
        print("[PASS] claims.csv 结构与枚举合规")
    cat = check_catalog()
    if cat:
        fails.append(("[2] module catalog", cat))
    else:
        print("[PASS] module catalog 结构一致")
    lk = check_links()
    if lk:
        fails.append(("[3] markdown 断链", lk))
    else:
        print("[PASS] markdown 链接完整")
    if fails:
        for tag, items in fails:
            print(f"[FAIL] {tag}:")
            for it in items[:40]:
                print("  -", it)
        print(f"\n门禁 FAIL：{len(fails)} 类问题")
        return 1
    print("\n门禁 PASS：结构契约、claims、链接全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
