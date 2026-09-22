# -*- coding: utf-8 -*-
import os

root = r"D:\a10\aikjx\code\my_lib\uft"
patterns = ["3.7959", "1.2%", "1.21%", "偏差1.2", "偏差 1.2", "1.2\\%"]

# Files that SHOULD now be free of the erroneous 3.75@1.2% claim (except in E10 correction notes)
must_fix = [
    os.path.join(root, "arxiv/main.tex"),
    os.path.join(root, "arxiv/README.md"),
    os.path.join(root, "arxiv/SUBMISSION_CHECKLIST.md"),
    os.path.join(root, "__全维总结整理_20260815.md"),
    os.path.join(root, "__框架状态_20260815.md"),
    os.path.join(root, "__SI伪影修正_20260815.md"),
    os.path.join(root, "__3.75现象学分析_20260814.md"),
    os.path.join(root, "memory/2026-08-14.md"),
    os.path.join(root, "memory/2026-08-15.md"),
]

print("=== MUST-FIX FILES VERIFICATION ===")
for fp in must_fix:
    if not os.path.exists(fp):
        print("MISSING: %s" % fp)
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    hits = []
    for p in patterns:
        c = txt.count(p)
        if c > 0:
            hits.append("%s:%d" % (p, c))
    name = os.path.basename(fp)
    if hits:
        print("[HAS OLD CLAIM] %-40s %s" % (name, ", ".join(hits)))
    else:
        print("[CLEAN]        %-40s" % name)

# Also report the erroneous files still present (audit trail, not fixed)
print("\n=== HISTORICAL (AUDIT TRAIL, NOT MODIFIED) ===")
exts = (".md", ".tex", ".txt")
all_hits = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(exts):
            continue
        fp = os.path.join(dp, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
        except:
            continue
        # count only if NOT in the must_fix set and NOT mother errata table
        if fp in must_fix:
            continue
        if "__勘误总表_E1-E10" in f or "__E10循环论证修正" in f:
            continue
        c = sum(txt.count(p) for p in patterns)
        if c > 0:
            all_hits.append((fp, c))

total = sum(c for _, c in all_hits)
print("Historical files still containing old claims: %d (total %d occurrences)" % (len(all_hits), total))
for fp, c in sorted(all_hits, key=lambda x: -x[1])[:20]:
    print("  %4d  %s" % (c, fp))
