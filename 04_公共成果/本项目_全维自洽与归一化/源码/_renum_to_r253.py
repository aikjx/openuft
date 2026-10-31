# -*- coding: utf-8 -*-
"""把本卷整体从 r251 迁到 r253（后到者改号）。源码 UTF-8，路径写在脚本内。"""
import io
import os

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"

OLD = os.path.join(
    SRC,
    "TUFT-r251_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性"
    "_七靶大统一方程判决_精算与可视化_2026-10-30.py")
NEW = os.path.join(
    SRC,
    "TUFT-r253_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性"
    "_七靶大统一方程判决_精算与可视化_2026-10-31.py")

assert os.path.isfile(OLD), "OLD missing"
assert not os.path.exists(NEW), "NEW exists"

t = io.open(OLD, "r", encoding="utf-8").read()
n0 = t.count("r251")

PAIRS = [
    # 1. BASE_NAME 主体
    ('"TUFT-r251_力', '"TUFT-r253_力'),
    # 2. 标题（docstring / report / md / html 共 5 处）
    ('TUFT-r251 · 力的无模型定理层', 'TUFT-r253 · 力的无模型定理层'),
    # 3. RID
    ('RID = "r251"', 'RID = "r253"'),
    # 4. 日期后缀
    ('_七靶大统一方程判决_精算与可视化_2026-10-30")',
     '_七靶大统一方程判决_精算与可视化_2026-10-31")'),
    # 5. 定位段
    ('r250 = 耦合常数跑动与能标层，\n本卷 r251 = **无模型定理层**',
     'r250 = 耦合常数跑动与能标层，\nr251 = 下游物理应用层（并行会话：垂直原理 FRW 与黑洞无奇点），\n本卷 r253 = **无模型定理层**'),
    # 6. 分层小标题
    ('【★与 r247/r248/r249/r250 的分层（不可相加）】',
     '【★与 r248/r249/r250/r251 的分层（不可相加）】'),
    # 7. 分层铁律上界
    ('本卷条目不可与 r142–r250 相加。', '本卷条目不可与 r142–r252 相加。'),
    # 8. 未动扫描范围
    ('"""真机读：扫 r225–r250 产物，mtime 是否早于本轮启动。"""',
     '"""真机读：扫 r225–r251 产物，mtime 是否早于本轮启动。\n'
     '    ★r252 正被并行会话探测写入，为避免与并发写竞争而排除在外。"""'),
    ('if not (225 <= n <= 250):', 'if not (225 <= n <= 251):'),
    ('- r225–r250 产物未改动', '- r225–r251 产物未改动'),
    # 9. 度数
    ('第 32 度', '第 34 度'),
    # 10. 撞号记录
    ('      "r249（低能极限推导层）、r250（耦合常数跑动与能标层）被并行会话占用 ⇒ 本卷取 **r251**。")',
     '      "r249（低能极限推导层）、r250（耦合常数跑动与能标层）、\\n"\n'
     '      "r251（下游物理应用层，落盘 10-31 08:09:31，早于本卷 08:18:26）被并行会话占用；\\n"\n'
     '      "r252 同期处于并行会话探测中 ⇒ 后到者整体改号，本卷取 **r253**。")'),
]

for a, b in PAIRS:
    if a not in t:
        raise SystemExit("MISS: " + a[:60])
    t = t.replace(a, b)

io.open(NEW, "w", encoding="utf-8").write(t)

# 复核：剩余的 r251 只应出现在「提及他人卷号」的语境里
left = [ln for ln in t.splitlines() if "r251" in ln]
print("renamed ->", os.path.basename(NEW))
print("r251 before=%d after=%d" % (n0, t.count("r251")))
print("--- residual r251 lines (应仅为提及并行会话 r251) ---")
for ln in left:
    print("   ", ln.strip()[:120])
print("r253 count =", t.count("r253"))
print("第 34 度 count =", t.count("第 34 度"))
