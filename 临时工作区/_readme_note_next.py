# -*- coding: utf-8 -*-
"""文末补一行编号消歧：r147 已被本文件上方《修复空间的机器生成与闭包定价》占用。"""
import os
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")

NOTE = (
    "> **\u7f16\u53f7\u6d88\u6b67\uff082026-10-22 01:50 \u8865\u8bb0\uff09**\uff1a"
    "\u4e0a\u65b9 r146 \u7ae0\u672b\u5199\u300c\u4e0b\u8f6e\u4ece r147 \u8d77\u300d\uff0c"
    "\u4f46 **r147 \u5df2\u7531\u672c\u6587\u4ef6\u4e0a\u65b9\u300a\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7\u300b"
    "\uff082026-10-22 01:45 \u5df2\u8dd1\u901a\u5e76\u5b8c\u6210\u56db\u5904\u767b\u8bb0\uff09\u5360\u7528**\u3002"
    "\u6309\u300c\u540e\u5230\u8005\u6539\u53f7\u4e0d\u8986\u76d6\u4ed6\u4eba\u300d\u7eaa\u5f8b\uff0c"
    "**\u4e0b\u8f6e\u5b9e\u9645\u4ece r148 \u8d77**\u3002"
)

with io.open(README, "r", encoding="utf-8") as f:
    txt = f.read()
if "r147 \u5df2\u7531\u672c\u6587\u4ef6\u4e0a\u65b9" in txt:
    print("already noted; skip")
else:
    if not txt.endswith("\n"):
        txt += "\n"
    txt += "\n" + NOTE + "\n"
    with io.open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("note appended")
