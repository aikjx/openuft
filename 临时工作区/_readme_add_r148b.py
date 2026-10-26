# -*- coding: utf-8 -*-
"""补登 r148 的源码树与数据树两处（幂等：已存在则跳过）。"""
import os
import io
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")

# 复用上一步脚本里的三行长文本（避免重复粘贴）
spec = importlib.util.spec_from_file_location(
    "prev", os.path.join(ROOT, "scratch", "_readme_add_r148.py"))
# 不执行它（会重写文件），改为直接读其源码取常量
with io.open(os.path.join(ROOT, "scratch", "_readme_add_r148.py"), "r", encoding="utf-8") as f:
    src = f.read()
ns = {}
start = src.index("SRC_LINE = (")
end = src.index("JUDGE_LINE = (")
exec(src[start:end], ns)
SRC_LINE = ns["SRC_LINE"]
start2 = src.index("DATA_LINE = (")
end2 = src.index("CHAPTER = ")
exec(src[start2:end2], ns)
DATA_LINE = ns["DATA_LINE"]

with io.open(README, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

if any("TUFT-r148_D5" in ln and ln.lstrip().startswith("\u251c\u2500\u2500") for ln in lines) and \
   any("TUFT-r148_D5" in ln and ln.lstrip().startswith("\u2502") for ln in lines):
    print("already registered; skip")
    raise SystemExit(0)

SRC_ANCHOR = "\u2502   \u251c\u2500\u2500 TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.py"
DATA_ANCHOR = "    \u251c\u2500\u2500 TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.json"

out = []
hit = {"src": 0, "data": 0}
for ln in lines:
    out.append(ln)
    if hit["src"] == 0 and ln.startswith(SRC_ANCHOR):
        out.append(SRC_LINE)
        hit["src"] = 1
    elif hit["data"] == 0 and ln.startswith(DATA_ANCHOR):
        out.append(DATA_LINE)
        hit["data"] = 1

with io.open(README, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))

print("hits:", hit)
