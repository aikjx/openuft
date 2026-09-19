# -*- coding: utf-8 -*-
import os

root = r"D:\a10\aikjx\code\my_lib\uft"

# Historical md reports that still contain old 3.75@1.2% claims (audit trail).
# These already have detailed boxes: __全维总结整理, __框架状态, __SI伪影修正, __3.75现象学分析
targets = [
    "__H1H4优化报告_20260815.md",
    "__H1重新校准_20260815.md",
    "__v_c修复全维通过_20260814.md",
    "__全维分析完整报告_20260814.md",
    "__全链路审计修正综合报告_20260814.md",
    "__勘误表与优化路线图_20260814.md",
    "__四力五维全明_20260814.md",
    "__框架最终总结_20260814.md",
    "__科学家认可策略_20260814.md",
    "__科学家认可策略_审计校准版_20260814.md",
    "__验证与大统一方程_20260814.md",
    "__arXiv论文包完成报告_20260814.md",
]

pointer = (
    "> \u26a0\ufe0f **E10 \u52d8\u8bef**\uff1a\u672c\u6587\u4ef6\u53ef\u80fd\u542b \"3.75@1.2%\" \u65e7\u58f0\u79f0\uff0c"
    "\u5df2\u4fee\u6b63\u4e3a \"3.75@7.4%\uff08\u5faa\u73af\u8bba\u8bc1\uff09\"\u3002"
    "\u8be6\u89c1 `__\u52d8\u8bef\u603b\u8868_E1-E10_20260815.md`\u3002\n>\n"
)

count = 0
for name in targets:
    fp = os.path.join(root, name)
    if not os.path.exists(fp):
        print("MISSING: %s" % name)
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        txt = f.read()
    if "E10" in txt[:800]:
        print("SKIP (has E10 already): %s" % name)
        continue
    # Insert at very top (blockquote before title is valid markdown)
    txt = pointer + txt
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(txt)
    count += 1
    print("ADDED pointer: %s" % name)

print("\nAdded to %d files" % count)
