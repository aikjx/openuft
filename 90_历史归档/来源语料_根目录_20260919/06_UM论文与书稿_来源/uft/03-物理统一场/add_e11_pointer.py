# -*- coding: utf-8 -*-
import os

base = r"D:\a10\aikjx\code\my_lib\uft"

files = [
    "__H1重新校准_20260815.md",
    "__H1H4优化报告_20260815.md",
    "__SI伪影修正_20260815.md",
    "__全维总结整理_20260815.md",
]

e11 = ("> ⚠️ **E11 勘误**：本文件含 \"Q*=6.3 TeV\" 旧声称（H1 方案 B）。\n"
       "> 该 Q* 系 β 系数错误（低估 4.2×，N_eff=1）+ 循环匹配导致，\n"
       "> **正确 Q*≈87 GeV（M_Z 尺度）**。框架 1/128 ≈ 实验 α⁻¹(M_Z)=127.955（偏差 0.04%），非预测。\n"
       "> 详见 `__H1方案B复核_20260815.md` 和 `__勘误总表_E1-E10_20260815.md`。\n\n")

for name in files:
    fp = os.path.join(base, name)
    t = open(fp, 'r', encoding='utf-8').read()
    if "E11 勘误" in t:
        print("SKIP (already):", name)
        continue
    open(fp, 'w', encoding='utf-8').write(e11 + t)
    print("ADDED E11 pointer:", name)
