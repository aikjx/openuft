# -*- coding: utf-8 -*-
"""规范化各章 ## 标题编号：按文件顺序重新编号 X.1, X.2, ..."""
import glob, os, re

base = os.path.dirname(os.path.abspath(__file__))
ms_dir = os.path.join(base, "..", "manuscript")

pat = re.compile(r'^(## )(\d+)\.(\d+)([^\n]*)(\n?)$')

for f in sorted(glob.glob(os.path.join(ms_dir, "ch*.md"))):
    with open(f, encoding="utf-8") as fh:
        lines = fh.readlines()
    chapter_no = None
    n = 0
    changed = 0
    new_lines = []
    for ln in lines:
        m = pat.match(ln)
        if m and m.group(2):  # 顶层编号标题
            if chapter_no is None:
                chapter_no = m.group(2)
            n += 1
            new_ln = f"{m.group(1)}{chapter_no}.{n}{m.group(4)}{m.group(5)}"
            if new_ln != ln:
                changed += 1
            new_lines.append(new_ln)
        else:
            new_lines.append(ln)
    with open(f, "w", encoding="utf-8") as fh:
        fh.writelines(new_lines)
    print(f"{os.path.basename(f)}: 重编号 {changed} 处，章节号 {chapter_no}，共 {n} 个顶层标题")
