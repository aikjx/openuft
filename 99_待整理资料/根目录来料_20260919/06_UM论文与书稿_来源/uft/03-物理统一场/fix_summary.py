# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\__全维总结整理_20260815.md"
with open(path, 'r', encoding='utf-8') as f:
    md = f.read()

repls = [
    # Top warning after date line
    ("**完整修复/发现/状态 · 2026-08-15 16:20 GMT+8**\n",
     "**完整修复/发现/状态 · 2026-08-15 16:20 GMT+8**\n\n"
     "> **E10 勘误（2026-08-15 20:50）**：本文撰写于 E10 发现前。文中所有 \"3.75@1.2%\" 声称已修正\n"
     "> 为 \"3.75@7.4%（独立实验 α₂=0.0338）\" 或 \"α_S/α_EM=15@0.6%（平凡整数比）\"。\n"
     "> 原 3.7959@1.2% 系循环论证（用框架假设 α_W=4α_EM 计算），详见 `__E10循环论证修正_20260815.md`。\n"),

    # Line 48 in section 1
    ("- 3.75 预测（α_S/α_W=15/4=3.75，实验 3.7959，偏差1.2%）",
     "- 3.75 预测（α_S/α_W=15/4=3.75，独立实验 3.49，**偏差7.4%**；原称3.7959@1.2%系循环论证，见E10）"),

    # Table row 5
    ("| 5 | **α_S/α_W = 3.75** | **弱预测** | **1.2%** |",
     "| 5 | **α_S/α_W = 3.75** | **弱预测** | **7.4%**（独立实验；原1.2%系循环） |"),

    # Final honest assessment
    ("唯一可检验预测：α_S/α_W = 3.75（偏差1.2%）",
     "最好预测：α_S/α_EM = 15（偏差0.6%，平凡整数比）；3.75@7.4%（非原称1.2%，见E10勘误）"),
]

count = 0
for old, new in repls:
    if old in md:
        md = md.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % repr(old[:40]))

# Also fix the "立即可行" section that says "聚焦唯一可检验预测"
md = md.replace(
    "1. **3.75 现象学论文**：聚焦唯一可检验预测，提交 EPJC/PRD",
    "1. **3.75 现象学论文**：聚焦预测（诚实标注 7.4% 偏差，非 1.2%），提交 EPJC/PRD")

with open(path, 'w', encoding='utf-8') as f:
    f.write(md)

print("Replaced %d patterns + 1 extra" % count)
