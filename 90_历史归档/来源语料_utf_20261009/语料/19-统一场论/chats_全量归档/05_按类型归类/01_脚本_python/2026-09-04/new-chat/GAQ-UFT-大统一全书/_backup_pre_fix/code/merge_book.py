# -*- coding: utf-8 -*-
"""合并 manuscript/*.md 为 deliverables/final.md 并统计中文字数。"""
import glob, os, re

base = os.path.dirname(os.path.abspath(__file__))
book = os.path.join(base, "..")
ms_dir = os.path.join(book, "manuscript")
out = os.path.join(book, "deliverables", "final.md")

files = sorted(glob.glob(os.path.join(ms_dir, "*.md")))
parts = []
total_han = 0
for f in files:
    with open(f, encoding="utf-8") as fh:
        txt = fh.read()
    parts.append(txt)
    # 去掉代码块与公式符号后统计汉字数
    body = re.sub(r"```.*?```", "", txt, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$", "", body, flags=re.S)
    body = re.sub(r"\$[^$\n]*\$", "", body)
    han = len(re.findall(r"[\u4e00-\u9fff]", body))
    total_han += han
    print(f"{os.path.basename(f)}: 汉字 {han}")

merged = "\n\n---\n\n".join(parts)
with open(out, "w", encoding="utf-8") as fh:
    fh.write(merged)
print("-"*50)
print(f"合并完成: {len(files)} 章 -> {out}")
print(f"正文汉字总数(不含公式/代码): {total_han}")
print(f"目标 48000 (80%~120% = {int(48000*0.8)}~{int(48000*1.2)})")
