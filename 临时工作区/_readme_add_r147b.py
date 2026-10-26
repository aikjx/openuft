# -*- coding: utf-8 -*-
"""补登遗漏的两处：数据树条目 + r142 更正行（按行号定位 + 内容校验，不匹配失败即中止）。"""
import os
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")

with io.open(README, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")


def find_once(key, startswith=None):
    hits = []
    for i, ln in enumerate(lines):
        if key in ln and (startswith is None or ln.lstrip().startswith(startswith)):
            hits.append(i)
    return hits


d = find_once("TUFT-r143_\u5e38\u6e29\u8d85\u5bfc_\u5b9e\u9a8c\u6b65\u9aa4\u6750\u6599", "\u251c\u2500\u2500 TUFT-r143")
r = find_once("\u4e0b\u8f6e\u4ece r144 \u8d77", "**")
print("data hits:", d)
print("r142 hits:", r)

DATA_LINE = (
    "    \u251c\u2500\u2500 TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.json / .md / _report.txt  # \u65b0\u589e\uff08**r147 \u00b7 2026-10-22**\uff09"
    "M4 \u95ed\u5305\u673a\u68c0\u4ea7\u7269\uff089 \u6761\u5224\u5b9a + **9 \u6761 guard** + \u63a7\u5236\u7ec4 5 \u9879 + \u4f9d\u8d56\u96c6 18 \u6761 + metrics \u539f\u59cb\u673a\u8bfb\u91cf\uff1b"
    "key_numbers\uff1a**D2 \u5173\u95ed\u89e3 4 \u4e2a\uff0c\u96f6\u4ee3\u4ef7\u8005 1 \u4e2a\uff083.9[0]=FLIP\uff09**\u3001\u4ee3\u4ef7 1 \u8005 3 \u4e2a\uff1b"
    "**A4 \u5173\u95ed\u89e3 4 \u4e2a\u3001\u6700\u5c0f\u4ee3\u4ef7 1**\uff1b"
    "**A2&A3 \u4fdd\u7559\u87ba\u65cb\u4e0b\u53ef\u540c\u65f6\u5173\u95ed\u8005 0 \u4e2a**\uff084 \u7ec4\u5408\u4e2d 2 \u4e2a\u53ef\u5173\u95ed\u4f46\u5747\u653e\u5f03\u87ba\u65cb\uff09\uff1b"
    "**B4 \u679a\u4e3e 27 / C2 \u679a\u4e3e 3 / F2 \u679a\u4e3e 9\uff0c\u5173\u95ed\u89e3\u5747 0**\uff1b"
    "**F1 \u5173\u95ed\u89e3 3 \u4e2a**\uff08\u5b9e\u8d28\u552f\u4e00 = \u5220\u53bb\u5f0f 3.15 \u7684 (A\u20d7\u00d7E\u20d7)/c\u00b2 \u9879\uff09\uff1b"
    "**\u9700\u9ad8\u9636\u7b97\u5b50\u7684 FAIL 10 \u6761**\uff09"
)

R142_CORR = (
    "- **\u26052026-10-22 \u540e\u7eed\u66f4\u6b63\uff08\u89c1 r147\uff09**\uff1a\u672c\u5377\u300c\u4ecd\u672a\u95ed\u5408\u9879\u300d\u767b\u8bb0\u7684"
    "\u300c**\u4fee\u590d\u9879\u7684\u5019\u9009\u7a7a\u95f4\u7531\u4eba\u5de5\u5b9a\u4e49**\u300d\u5df2\u7531 **r147** \u5835\u4e0a \u2014\u2014 "
    "\u673a\u5668\u751f\u6210\u7f16\u8f91\u95ed\u5305\uff08{KEEP, FLIP, DEL, INS} \u5168\u679a\u4e3e\uff09\u540e\uff0c"
    "**\u672a\u53d1\u73b0**\u672c\u5377 P1\u2013P9 \u4e4b\u5916\u7684\u4efb\u4f55\u4f4e\u9636\u89e3 \u21d2 \u672c\u5377\u4fee\u590d\u6e05\u5355\u5728\u4f4e\u9636\u7b97\u5b50\u7a7a\u95f4\u5185**\u5b8c\u5907**\uff0c"
    "\u300c\u4fee\u590d\u5373\u81ea\u6740\u300d\u7ed3\u8bba\u4e0d\u53d7\u5f71\u54cd\uff1b"
    "**\u4f46\u672c\u5377 R7 \u5b9a\u4ef7\u9519\u8bef** \u2014\u2014 D2 \u7684\u7b26\u53f7\u7ffb\u8f6c\u6709 **4 \u4e2a\u89e3**\uff0c"
    "\u5176\u4e2d\u7ffb\u5f0f **3.9** \u662f**\u96f6\u4ee3\u4ef7**\u89e3\uff08\u4fdd\u6301\u5f0f 3.4 / 3.10 \u7b26\u53f7\u540c\u6e90\uff09\uff0c"
    "\u672c\u5377\u9009\u7684\u300c\u7ffb\u5f0f 3.10\u300d\u66f4\u8d35\uff0c\u4e14\u7ed9\u5b83\u8bb0\u7684\u300c3.4 \u4e0e 3.10 \u7b26\u53f7\u4e0d\u540c\u6e90\u300d\u8fd9\u7b14\u4ee3\u4ef7**\u5e76\u4e0d\u5b58\u5728**\u3002"
    "\u672c\u5377\u5176\u4f59\u5b9a\u4ef7\u7ecf r147 \u590d\u6838**\u4ecd\u6210\u7acb**\u3002"
)

assert len(d) == 1, "data anchor not unique: %r" % d
assert len(r) == 1, "r142 anchor not unique: %r" % r

# 从后往前插入，避免行号漂移
for idx, payload in sorted([(d[0], DATA_LINE), (r[0], R142_CORR)], key=lambda x: -x[0]):
    lines.insert(idx + 1, payload)

txt = "\n".join(lines)
if not txt.endswith("\n"):
    txt += "\n"
with io.open(README, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)
print("inserted; total lines:", len(lines))
