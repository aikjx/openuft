# -*- coding: utf-8 -*-
"""【已作废 · 仅留作 lineage】自抓块现由 `_sync_r320_readme.py` 整段从判定册现推。
本驱动把「自抓 N 枚」按全局替换改名（判定册 ⑩ 记的就是这一型：块里一旦引用旧字面量，
全局 sub 会连引文一起改）⇒ 不得再对 README 运行。"""
"""r320 增量补丁：把「死账钉」这一型自捕缺陷登进 README 的 r320 小节。

纪律：
1. 二进制读 + 二进制写，行尾字节逐字保留（README 是 CRLF 敏感文件）。
2. 枚数不手打：从判定册面「五之二」小节现数 bullet 条数。
3. 只在 `### r320` 键内替换，替换次数必须 == 2（标题 1 + 登记行 1），否则拒写。
4. 幂等：文本里已经写着目标枚数就 SKIP，不重复追加。
5. 只动 README 一个文件，写前图像留在 scratch/ 里可还原。
"""
import glob
import io
import os
import re
import sys

# 硬拒跑（作废要有牙，不能只写注释）：自抓块现由 _sync_r320_readme.py 从判定册整段现推。
sys.stderr.write("SUPERSEDED 本驱动不再对 README 运行；改用 源码/_sync_r320_readme.py\n")
sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
README = os.path.join(ROOT, "README.md")
JUDG = glob.glob(os.path.join(ROOT, "判定", "判定_TUFT-r320_*.md"))
if len(JUDG) != 1:
    print("JUDG-FACE-AMBIGUOUS %d" % len(JUDG))
    sys.exit(2)

raw = open(README, "rb").read()
txt = raw.decode("utf-8")

# ---- 1) 枚数从判定册现数
ju = io.open(JUDG[0], encoding="utf-8", newline="").read()
i = ju.index("五之二")
blk = ju[i:]
blk = blk[:blk.index("\n## ")]
n_bugs = len([l for l in blk.splitlines() if l.startswith("- ")])
if n_bugs < 8:
    print("BUG-COUNT-SUSPECT %d（判定册这一节比上一轮还短，拒绝按它登记）" % n_bugs)
    sys.exit(2)
old = "自抓 7 枚仪器坑"
new = "自抓 %d 枚仪器坑" % n_bugs

# ---- 2) 定位 r320 键，区间内替换（不许碰别的卷）
ki = [m.start() for m in re.finditer(r"^### r320 ·", txt, re.M)]
if len(ki) != 1:
    print("R320-KEY-NOT-UNIQUE %d -> 拒绝写盘" % len(ki))
    sys.exit(2)
kend = txt.find("\n### ", ki[0] + 5)
if kend < 0:
    kend = len(txt)
sec = txt[ki[0]:kend]
if new in sec:
    print("SKIP（r320 小节已登记 %d 枚）" % n_bugs)
    sys.exit(0)
hits = sec.count(old)
if hits != 2:
    print("COUNT-ANCHOR-AMBIGUOUS 命中 %d 枚（期望 2：标题 + 登记行）-> 拒绝写盘" % hits)
    sys.exit(2)
sec2 = sec.replace(old, new)
added = (
    "\n    \u2467 **\u8de8\u5377\u5c3a\u5bf8\u9489\u6210\u4e86\u6b7b\u8d26**\uff08\u672c\u8f6e\u6536\u53e3\u671f\u95f4\u5b9e\u6d4b\uff1a"
    "\u540c\u4e00\u5f15\u64ce\u91cd\u8dd1\u4e00\u8d9f\uff0c\u672c\u5377\u6570\u636e\u9762\u7684 md5 \u81ea\u884c\u53d8\u52a8\uff0c"
    "\u6839\u56e0\u662f\u88ab\u5f15\u7684\u5e76\u53d1\u5377\u9762\u5728\u672c\u5377\u5199\u76d8\u4e4b\u540e\u4ecd\u5728\u88ab\u4ed6\u5377\u4f5c\u8005\u6539\u5199\uff0c"
    "\u800c V11/V13/V19 \u628a\u5b83\u4eec\u7684\u300c\u5b57\u8282 / md5\u300d\u5f53\u53ef\u5f15\u6570\u503c\u9489\u4e86\u4e0b\u6765\uff09"
    "\u21d2 \u51e1\u8de8\u5377\u5f15\u7528\u73b0\u573a\u5370\u51fa\u5b57\u8282\u6570 + md5\uff0c\u5e76\u9010\u5b57\u5e26\u4e0a"
    "\u300c\u53ea\u4f5c\u5f53\u4e0b\u89c2\u5bdf\uff0c\u4e0d\u53ef\u540e\u5f15\u300d\uff1b\u6536\u53e3\u65b0\u589e W14 \u9489\u666e\u67e5"
    "\uff08\u7f3a\u9650\u5b9a\u8bcd / \u76d8\u4e0a\u5df2\u65e0\u6b64\u9762\u5373\u5224\u6b7b\u8d26\uff09\uff0c"
    "M22 \u5265\u9650\u5b9a\u8bcd\u3001M23 \u9489\u4e00\u5f20\u4e0d\u5b58\u5728\u7684\u4ed6\u5377\u9762\u5404\u914d\u4e00\u679a\u7ea2\uff1b"
    "\n    \u2468 **\u672c\u5377\u81ea\u5df1\u4e5f\u9489\u81ea\u5df1\u7684\u4e2d\u95f4\u6001**\uff08G15 \u5370\u7684\u662f\u7b2c\u4e00\u8d9b\u843d\u76d8\u65f6\u81ea\u8eab\u5404\u9762\u7684 md5\uff0c"
    "\u800c\u7b2c\u4e8c/\u4e09\u8d9b\u8fd8\u5728\u91cd\u5199\u90a3\u4e9b\u9762 \u21d2 \u540c\u4e00\u578b\u6b7b\u8d26\uff0c\u5bf9\u8c61\u6362\u6210\u4e86\u672c\u5377\uff0c"
    "W14 \u5b9e\u6d4b\u300c\u76d8\u4e0a\u5df2\u65e0\u6b64\u9762\u300d\u7684\u672c\u5377\u65e7\u9489 3 \u679a\uff09"
    "\u21d2 G15 \u540d\u518c\u540c\u6837\u5e26\u9650\u5b9a\u8bcd\uff08\u6807\u7b7e\u300c\u672c\u5377\u81ea\u8eab\u5728\u540e\u7eed\u8d9b\u91cc\u7ee7\u7eed\u91cd\u5199\u8be5\u9762\u300d\uff09\uff0c"
    "\u5c3a\u5bf8\u901a\u9053\u4fdd\u7559\u4f5c\u8bc1\uff0c\u4f46\u660e\u5199\u5b83\u4e0d\u662f\u53ef\u540e\u5f15\u7684\u7ec8\u503c\u3002"
)
tail_anchor = "\u2466 ASCII runner \u7684 docstring \u5199\u4e86\u5b57\u9762\u53cd\u659c\u6760\u8def\u5f84 \u21d2 `unicodeescape` \u5d29\u3002"
if tail_anchor not in sec2:
    print("BULLET-7-ANCHOR-MISSING -> \u62d2\u7edd\u5199\u76d8")
    sys.exit(2)
sec3 = sec2.replace(tail_anchor, tail_anchor + added, 1)

after = txt[:ki[0]] + sec3 + txt[kend:]
# 键外一字不许动：拼回去的字符串必须恰好等于「原文在同一个切点上的两半 + 新键体」。
assert txt[:ki[0]] == after[:ki[0]] and txt[kend:] == after[len(after) - len(txt[kend:]):], "HEAD-TAIL-DRIFT"
if after.count(new) != 2 or after.count(old) != txt.count(old) - 2:
    print("COUNT-REPLACE-UNEXPECTED new=%d old=%d（期望键内 2 处替换）-> 拒绝写盘"
          % (after.count(new), after.count(old)))
    sys.exit(2)
nb = after.count("### r320 ·")
if nb != 1:
    print("KEY-COUNT-DRIFT %d -> 拒绝写盘" % nb)
    sys.exit(2)
delta = len(after.encode("utf-8")) - len(raw)

bak = os.path.join(ROOT, "scratch", "_bak_README_pre_r320bugcount_2026-11-01.md")
open(bak, "wb").write(raw)
open(README, "wb").write(after.encode("utf-8"))

re_read = open(README, "rb").read().decode("utf-8")
k2 = re_read.index("### r320 ·")
e2 = re_read.find("\n### ", k2 + 5)
live = re_read[k2:e2]
print("BUGS-FROM-FACE = %d" % n_bugs)
print("REPLACED %d 处（标题 + 登记行）；新增 %d 字节" % (hits, delta))
print("READBACK 标题含 %s = %s" % (new, new in live.splitlines()[0]))
print("READBACK ⑧⑨ 在场 = %s" % ("\u2467" in live and "\u2468" in live))
lost = [c for c in "\u2460\u2461\u2462\u2463\u2464\u2465\u2466" if c not in live]
print("READBACK 原七枚编号丢失 = %s（期望 []）" % lost)
print("READBACK 旧字样残留 = %d（期望 0）" % live.count(old))
print("BACKUP %s" % bak)
print("REG-PATCH-OK")
