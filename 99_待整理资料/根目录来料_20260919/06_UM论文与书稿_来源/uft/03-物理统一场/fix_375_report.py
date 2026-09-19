# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\__3.75现象学分析_20260814.md"
with open(path, 'r', encoding='utf-8') as f:
    md = f.read()

box = ("> # ⛔ E10 重大勘误（2026-08-15 20:50）：本文核心结论已失效\n"
       ">\n"
       "> **本报告的 \"3.75@1.2%\" 声称是循环论证，已被严格证伪。**\n"
       ">\n"
       "> - 错误：用框架假设 α_W = 4×α_EM 计算 \"实验值\" 3.7959，再声称验证框架\n"
       "> - 真实：独立实验 α₂(M_Z)=0.0338 时，α_S/α_W = **3.49（偏差 7.4%）**\n"
       "> - 框架真正最好匹配：α_S/α_EM = 15（偏差 0.6%，但只是整数比直接推论，平凡）\n"
       "> - 弱力整数 4 无效（α_W/α_EM = 4 vs 4.32，偏差 8.1%）\n"
       ">\n"
       "> **本报告的论文基础结论须重写。请勿直接引用文中 1.2% 数据。**\n"
       "> 详见 `__E10循环论证修正_20260815.md` 与 `__勘误总表_E1-E10_20260815.md`。\n"
       "\n")

anchor = "**可检验预测的深度分析 · 论文基础 · 2026-08-14 22:50 GMT+8**\n\n---\n"
if anchor in md:
    md = md.replace(anchor, anchor + box, 1)
else:
    print("ANCHOR NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(md)
print("Done: %s" % path)
