# -*- coding: utf-8 -*-
"""r367 产物字节数回填（不动点迭代）。

两个 md 互相引用对方与自己 ⇒ 自指。做法：
  1) 实测 json / report / html / src 的字节数（外部量，不随迭代变）
  2) 对 md 与 判定册 的自身字节数做不动点迭代 S = len(file(S))，写盘实测而非预测
  3) 全部写盘后复核：占位符清零、两文件内容与最后一次迭代一致
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: os.path.join(ROOT, *p)

import glob

_hit = glob.glob(os.path.join(ROOT, "数据", "TUFT-r367_*.md"))
if len(_hit) != 1:
    print("MD-GLOB hit=%d" % len(_hit))
    sys.exit(2)
STEM = os.path.basename(_hit[0])[:-len(".md")]

_hit2 = glob.glob(os.path.join(ROOT, "判定", "判定_*TUFT-r367_*.md"))
if len(_hit2) != 1:
    print("JUD-GLOB hit=%d" % len(_hit2))
    sys.exit(2)

_hit3 = glob.glob(os.path.join(ROOT, "*r367*.html"))
if len(_hit3) != 1:
    print("HTML-GLOB hit=%d" % len(_hit3))
    sys.exit(2)

MD = _hit[0]
JUD = _hit2[0]
HTML = _hit3[0]
JSON = os.path.join(ROOT, "数据", STEM + ".json")
REP = os.path.join(ROOT, "数据", STEM + "_report.txt")
SRC = os.path.join(ROOT, "源码", STEM + ".py")

for p in (MD, JUD, JSON, REP, HTML, SRC):
    if not os.path.exists(p):
        print("MISSING %s" % p)
        sys.exit(2)

ext = {
    "{JSONB}": str(os.path.getsize(JSON)),
    "{REPB}": str(os.path.getsize(REP)),
    "{HTMLB}": str(os.path.getsize(HTML)),
    "{SRCB}": str(os.path.getsize(SRC)),
}

md0 = io.open(MD, encoding="utf-8").read()
jd0 = io.open(JUD, encoding="utf-8").read()


def fill(t, mdb, judb):
    for k, v in ext.items():
        t = t.replace(k, v)
    t = t.replace("{MDB}", str(mdb)).replace("{JUDB}", str(judb))
    return t


def write(p, t):
    # 显式 newline='\n'：写盘字节数 = 字符串 UTF-8 字节数，不掺 CRLF 换算
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)


mdb, judb = 0, 0
hist = []
for it in range(80):
    write(MD, fill(md0, mdb, judb))
    write(JUD, fill(jd0, mdb, judb))
    n1 = os.path.getsize(MD)
    n2 = os.path.getsize(JUD)
    hist.append((n1, n2))
    if (n1, n2) == (mdb, judb):
        print("converged at iter %d: md=%d jud=%d" % (it, n1, n2))
        break
    mdb, judb = n1, n2
else:
    print("NOT-CONVERGED hist=%r" % (hist[-6:],))
    sys.exit(3)

# 复核
c1 = io.open(MD, encoding="utf-8").read()
c2 = io.open(JUD, encoding="utf-8").read()
left = [k for k in ("{JSONB}", "{REPB}", "{HTMLB}", "{SRCB}", "{MDB}", "{JUDB}")
        if k in c1 or k in c2]
if left:
    print("PLACEHOLDER-LEFT %r" % left)
    sys.exit(4)
if c1 != fill(md0, mdb, judb) or c2 != fill(jd0, mdb, judb):
    print("ROUNDTRIP-MISMATCH")
    sys.exit(5)

print("md=%d jud=%d json=%s rep=%s html=%s src=%s"
      % (os.path.getsize(MD), os.path.getsize(JUD),
         ext["{JSONB}"], ext["{REPB}"], ext["{HTMLB}"], ext["{SRCB}"]))
print("SIZES-OK")
