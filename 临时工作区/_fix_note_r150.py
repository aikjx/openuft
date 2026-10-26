# -*- coding: utf-8 -*-
"""更新文末编号消歧补记：r147 / r148 / r149 均已占，下轮实际从 r150 起。"""
import os
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")
with io.open(README, "r", encoding="utf-8") as f:
    txt = f.read()

head = "> **编号消歧（2026-10-22 02:10 更新）**"
NEW = (
    "> **编号消歧（2026-10-22 02:20 更新）**\uff1a"
    "\u4e0a\u65b9 r146 / r147 / r148 \u4e09\u7ae0\u7ae0\u672b\u5206\u522b\u5199\u300c\u4e0b\u8f6e\u4ece r147 \u8d77\u300d\u3001"
    "\u300c\u4e0b\u8f6e\u5b9e\u9645\u4ece r148 \u8d77\u300d\u3001\u300c\u4e0b\u8f6e\u4ece r149 \u8d77\u300d\uff0c"
    "\u4f46 **r147 / r148 / r149 \u73b0\u5747\u5df2\u88ab\u5360\u7528** \u2014\u2014 "
    "r147 = \u300a\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7\u300b\uff0801:45\uff09\uff1b"
    "r148 = \u300aD5 \u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u9996\u653b\u4e0e\u4fee\u590d\u5b9a\u4ef7\u300b\uff0802:00\uff09\uff1b"
    "r149 = \u300a\u5782\u76f4\u539f\u7406\u4e0e\u529b\u7684\u672c\u6e90\u00b7\u516c\u8bbe\u5c42\u653b\u7834\u4e0e\u5224\u522b\u6027\u5b9a\u4ef7\u300b\uff0802:14\uff09\u3002"
    "\u6309\u300c\u540e\u5230\u8005\u6539\u53f7\u4e0d\u8986\u76d6\u4ed6\u4eba\u300d\u7eaa\u5f8b\uff0c"
    "**\u4e0b\u8f6e\u5b9e\u9645\u4ece r150 \u8d77**\u3002"
)

i = txt.find(head)
if i < 0:
    print("anchor not found; skip")
else:
    j = txt.find("\n", i)
    txt = txt[:i] + NEW + "\n" + txt[j + 1:]
    with io.open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("note updated")
