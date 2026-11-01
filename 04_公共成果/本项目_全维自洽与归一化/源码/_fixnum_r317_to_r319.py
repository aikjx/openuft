# -*- coding: utf-8 -*-
"""把本卷源码从 r317 顺延为 r319（r317/r318 已被并行会话先占）。

纪律：
  * 只动**本卷自己**的源码文件（TUFT-r317_统一表示框架与二次超荷矩_*.py）
  * **不碰**并行会话的 TUFT-r317_ROOTV22_*.py / TUFT-r317_ROOTV24_*.py /
    _run_r317.py / _out_r317.txt（先到者保号，字节零改动）
  * 用 shutil.move 改名，不用 rm
"""
import io
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

OLD_TAG = "TUFT-r317_统一表示框架与二次超荷矩_"
NEW_TAG = "TUFT-r319_统一表示框架与二次超荷矩_"

cands = [f for f in os.listdir(HERE) if f.startswith(OLD_TAG) and f.endswith(".py")]
assert len(cands) == 1, "expected exactly 1 own source, got %r" % (cands,)
old = os.path.join(HERE, cands[0])
new = os.path.join(HERE, cands[0].replace("TUFT-r317_", "TUFT-r319_", 1))

txt = io.open(old, encoding="utf-8").read()
reps = [
    ('RID = "r317"', 'RID = "r319"'),
    ('TUFT-r317 · 统一表示框架与二次超荷矩', 'TUFT-r319 · 统一表示框架与二次超荷矩'),
    ('BASE = ("TUFT-r317_统一表示框架与二次超荷矩_', 'BASE = ("TUFT-r319_统一表示框架与二次超荷矩_'),
    ('print("[r317]', 'print("[r319]'),
]
for a, b in reps:
    n = txt.count(a)
    print("  %-58s count=%d" % (a[:58], n))
    txt = txt.replace(a, b)

# 兜底：确认再无裸 r317 残留（除注释里的「承 r317」之类历史引用）
left = txt.count("r317")
print("  remaining 'r317' occurrences =", left)

with io.open(old, "w", encoding="utf-8") as f:
    f.write(txt)
shutil.move(old, new)
print("  moved ->", os.path.basename(new))

# 并行会话的文件必须零改动（只读校验存在性，不写）
for guard_name in ["_run_r317.py", "_out_r317.txt"]:
    p = os.path.join(HERE, guard_name)
    print("  [keep] %-16s exists=%s size=%s"
          % (guard_name, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else "-"))

print("RENAME-OK")
