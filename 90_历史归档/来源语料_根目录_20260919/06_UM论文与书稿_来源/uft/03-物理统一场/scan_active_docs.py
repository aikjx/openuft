# -*- coding: utf-8 -*-
import os, sys

out_path = r"D:\a10\aikjx\code\my_lib\uft\03-物理统一场\scan_active_out.txt"
sys.stdout = open(out_path, 'w', encoding='utf-8')

root = r"D:\a10\aikjx\code\my_lib\uft"

suspicious = ["0.03106", "3.7959", "1.2%", "1.21%", "6.3 TeV", "Q*=6.3",
              "Q* = 6.3", "6.34 TeV", "85% complete", "genuine falsifiable",
              "85%", "Q*=6336", "Q*=6340"]

def iter_files():
    for dp, dn, fn in os.walk(root):
        if "memory" in dp:
            continue
        for f in fn:
            if f.endswith(".txt"):
                continue
            if f.startswith("__") and f.endswith(".md"):
                yield os.path.join(dp, f)
            elif dp.endswith("arxiv"):
                if f.endswith((".py", ".tex", ".md", ".bib")):
                    yield os.path.join(dp, f)
            elif os.path.basename(dp) == "03-物理统一场" and f.endswith(".py"):
                yield os.path.join(dp, f)

print("=== SCAN: suspicious numeric claims in ACTIVE docs ===\n")
total = 0
flagged = []
for fp in iter_files():
    try:
        lines = open(fp, 'r', encoding='utf-8', errors='ignore').read().split('\n')
    except:
        continue
    for i, line in enumerate(lines, 1):
        for s in suspicious:
            if s in line:
                ctx = " ".join(lines[max(0,i-3):min(len(lines),i+1)])
                marked = any(k in ctx for k in
                             ["E10", "E11", "circular", "retract", "勘误", "wrong",
                              "错误", "撤回", "invalid", "ERRONEOUS", "void", "失效",
                              "证伪", "CORRECTED", "废除", "deprecated", "superseded",
                              "已修", "已撤", "撤销", "弃用", "WITHDRAWN"])
                rel = os.path.relpath(fp, root)
                flagged.append((rel, i, s, line.strip()[:90], marked))
                total += 1
                break

unmarked = [x for x in flagged if not x[4]]
marked = [x for x in flagged if x[4]]

print("TOTAL hits: %d | marked(errata): %d | UNMARKED: %d\n" % (total, len(marked), len(unmarked)))
print("--- UNMARKED (potential leaks needing fix) ---")
for rel, i, s, txt, _ in unmarked:
    print("  %-45s L%-4d [%s] %s" % (rel, i, s, txt))
print("\n--- MARKED (errata mentions, OK) ---")
for rel, i, s, txt, _ in marked[:50]:
    print("  %-45s L%-4d [%s] %s" % (rel, i, s, txt))
if len(marked) > 50:
    print("  ... (%d more marked)" % (len(marked)-50))
print("\nDONE. Output also at:", out_path)
