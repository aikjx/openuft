# -*- coding: utf-8 -*-
"""修正 r148 源码树行的树形前缀（└── -> ├──）+ 更新文末编号消歧补记。"""
import os
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")

with io.open(README, "r", encoding="utf-8") as f:
    txt = f.read()

bad = "\u2502   \u2514\u2500\u2500 TUFT-r148_D5"
good = "\u2502   \u251c\u2500\u2500 TUFT-r148_D5"
n = txt.count(bad)
txt = txt.replace(bad, good)

old_note_head = "> **\u7f16\u53f7\u6d88\u6b67\uff082026-10-22 01:50 \u8865\u8bb0\uff09**\uff1a"
new_note = (
    "> **\u7f16\u53f7\u6d88\u6b67\uff082026-10-22 02:10 \u66f4\u65b0\uff09**\uff1a"
    "\u4e0a\u65b9 r146 / r147 \u4e24\u7ae0\u7ae0\u672b\u5206\u522b\u5199\u300c\u4e0b\u8f6e\u4ece r147 \u8d77\u300d\u4e0e"
    "\u300c\u4e0b\u8f6e\u5b9e\u9645\u4ece r148 \u8d77\u300d\uff0c\u4f46 **r147 \u4e0e r148 \u73b0\u5747\u5df2\u88ab\u5360\u7528** \u2014\u2014 "
    "r147 = \u300a\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7\u300b\uff0801:45\uff09\uff1b"
    "r148 = \u300aD5 \u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u9996\u653b\u4e0e\u4fee\u590d\u5b9a\u4ef7\u300b\uff0802:00\uff09\u3002"
    "\u6309\u300c\u540e\u5230\u8005\u6539\u53f7\u4e0d\u8986\u76d6\u4ed6\u4eba\u300d\u7eaa\u5f8b\uff0c"
    "**\u4e0b\u8f6e\u5b9e\u9645\u4ece r149 \u8d77**\u3002"
)
i = txt.find(old_note_head)
if i >= 0:
    j = txt.find("\n", i)
    # 该补记可能跨两行，取到空行为止
    k = txt.find("\n\n", i)
    end = min(j + 1, k + 1) if k > 0 else j + 1
    txt = txt[:i] + new_note + "\n" + txt[end:]
    note_done = True
else:
    note_done = False

with io.open(README, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)

print("prefix fixed:", n)
print("note updated:", note_done)
