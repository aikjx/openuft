# -*- coding: utf-8 -*-
import os

box = ("> **E10 勘误（2026-08-15 20:50）**：本文撰写于 E10 发现前。文中 \"3.75@1.2%\" 声称已修正\n"
       "> 为 \"3.75@7.4%（独立实验 α₂=0.0338）\" 或 \"α_S/α_EM=15@0.6%（平凡整数比）\"。\n"
       "> 原 3.7959@1.2% 系循环论证（用框架假设 α_W=4α_EM 计算），详见 `__E10循环论证修正_20260815.md` 和 `__全维总结整理_20260815.md`（已含 E10 修正）。\n\n")

# ===== File 1: __框架状态_20260815.md =====
f1 = r"D:\a10\aikjx\code\my_lib\uft\__框架状态_20260815.md"
with open(f1, 'r', encoding='utf-8') as f:
    md1 = f.read()

# Insert box after title block (after first ---)
anchor1 = "**2026-08-15 12:30 GMT+8 · 全部修复后最终状态**\n\n---\n"
if anchor1 in md1:
    md1 = md1.replace(anchor1, anchor1 + box, 1)
else:
    print("F1 anchor NOT FOUND")

repls1 = [
    ("| 6 | **α_S/α_W = 3.75** | **弱预测** | **1.2%** |",
     "| 6 | **α_S/α_W = 3.75** | **弱预测** | **7.4%**（E10修正：独立实验3.49） |"),
    ("实验值：  3.7959 ± 0.0031",
     "独立实验：3.49（α₂=0.0338；原3.7959系循环，见E10）"),
    ("偏差：    1.21%",
     "偏差：    7.4%（E10修正，非原称1.2%）"),
    ("## 🔬 唯一可检验预测",
     "## 🔬 唯一可检验预测（E10修正：3.75@7.4% 非 1.2%）"),
]
for old, new in repls1:
    if old in md1:
        md1 = md1.replace(old, new, 1)
    else:
        print("F1 NOT FOUND: %s" % repr(old[:30]))

with open(f1, 'w', encoding='utf-8') as f:
    f.write(md1)
print("F1 done")

# ===== File 2: __SI伪影修正_20260815.md =====
f2 = r"D:\a10\aikjx\code\my_lib\uft\__SI伪影修正_20260815.md"
with open(f2, 'r', encoding='utf-8') as f:
    md2 = f.read()

anchor2 = "**H4 深层修正 · 2026-08-15 14:45 GMT+8**\n\n---\n"
if anchor2 in md2:
    md2 = md2.replace(anchor2, anchor2 + box, 1)
else:
    print("F2 anchor NOT FOUND")

repls2 = [
    ("| 3 | **α_S/α_W = 3.75** | ✅ 唯一真预测（不依赖 κ 幂结构） |",
     "| 3 | **α_S/α_W = 3.75** | ⚠️ 弱预测（7.4%偏差，原称1.2%系循环，见E10） |"),
    ("核心价值：3.75 预测（唯一可检验）",
     "原核心价值：3.75 预测（实际7.4%偏差，非1.2%；最佳匹配α_S/α_EM=15@0.6%，见E10）"),
]
for old, new in repls2:
    if old in md2:
        md2 = md2.replace(old, new, 1)
    else:
        print("F2 NOT FOUND: %s" % repr(old[:30]))

with open(f2, 'w', encoding='utf-8') as f:
    f.write(md2)
print("F2 done")
