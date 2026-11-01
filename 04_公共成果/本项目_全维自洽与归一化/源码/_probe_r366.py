# -*- coding: utf-8 -*-
"""r366 占位脚本（先于任何大文件写入）

卷标题：
  TUFT-r366_整值多项式通有性审计_整性判别力恒零_牛顿系数被td钉死_陪集周期紧界N等于D_精算与可视化_2026-11-02

攻的目标：
  X-R358-1  实测 N=D（11/11）但未证；只证到 N | D·n!。真紧界未定。
  X-R358-2  D(c)=lcm_i den b_i(c) 随 c 的闭式：UND 区为何爆到 3.6e7。
  新方向     r346/r358 已两次「功劳归还」：定理 E/F 与引理 L 对任意整值多项式成立
             ⇒ 整性判据判别力恒零。本卷问：那什么才有判别力？
             答：牛顿系数向量 (a_0,...,a_n) 本身被 td 钉死（a_n=d、
             a_{n-1}=d(2n+1-d)/2、...），自由度 O(1) 而非 n+1 ⇒ 几何类在 Int(Z) 中是零测的。
"""
import os

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
RID = "r366"
STEM = ("TUFT-r366_整值多项式通有性审计_整性判别力恒零_牛顿系数被td钉死"
        "_陪集周期紧界N等于D_精算与可视化_2026-11-02")

trees = [("源码", os.path.join(BASE, "源码")),
         ("数据", os.path.join(BASE, "数据")),
         ("判定", os.path.join(BASE, "判定"))]

print("[probe] RID = %s" % RID)
print("[probe] STEM = %s" % STEM)
print("[probe] len(STEM) = %d" % len(STEM))

anc = "TUFT-r%s_" % RID
tot = 0
for tag, d in trees:
    try:
        fs = os.listdir(d)
    except Exception as e:
        print("[probe] %s  MISSING (%s)" % (tag, e))
        continue
    hit = sorted(f for f in fs if anc in f)
    tot += len(hit)
    print("[probe] %s  hit=%d" % (tag, len(hit)))
    for f in hit:
        print("          " + f[:100])

# 判定册另一处（r245-r273 在 数据/判定_*）
d = os.path.join(BASE, "数据")
hit2 = sorted(f for f in os.listdir(d) if ("判定_" + anc) in f)
tot += len(hit2)
print("[probe] 数据/判定_*  hit=%d" % len(hit2))

print("[probe] TOTAL = %d  ==> %s" % (tot, "COLD 可占用" if tot == 0 else "TAKEN 让号"))
