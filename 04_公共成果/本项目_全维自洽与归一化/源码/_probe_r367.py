# -*- coding: utf-8 -*-
"""r367 占位（先于任何大文件写入）

卷标题：
  TUFT-r367_完全交与加权超曲面的牛顿系数闭式_陪集周期N等于D的反例搜索与轨道数定理_精算与可视化_2026-11-03

攻的目标
  X-R366-1  完全交 X_{d_1..d_r} 与加权超曲面的牛顿系数闭式（X-R339-3 的子问题）
            猜想（Koszul 复形 + χ 加性的直接推广）：
              a_m = Σ_{S ⊆ [r]} (−1)^{|S|} C(N − d_S, N − m)，  d_S = Σ_{i∈S} d_i
            r=1 时退化为 r366 定理 H（因 C(n+1, n+1−m) = C(n+1, m)）
            对拍路径：td = Πd_i · [h^n]( e^{kh} T(h)^{N+1} / Π_i T(d_i h) )
  X-R366-2  「N = D ⟺ 解集在 Z/H 上是单轨道」—— 本卷做广域反例搜索：
            若找到轨道数 k > 1 的几何陪集 ⇒ 直接否证 N = D（比「归约」强）
            关键观察：β_n = D·a_n = D·d ≡ 0 (mod D) ⇒ f 模 D 后最高次项恒消失

诚实预设
  r358 的例子 C(m,2) mod 2 的解集是 {0,1} mod 4（2 个类）⇒ 一般整值多项式可以多轨道。
  问题因此变成：几何类的 β 是否永远只给单轨道？本卷用广域搜索回答（搜到反例即否证，
  搜不到也不算证明，只给加强的证据与样本量）。
"""
import os

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
RID = "r367"
DATE = "2026-11-03"
STEM = ("TUFT-r367_完全交与加权超曲面的牛顿系数闭式_陪集周期N等于D的反例搜索与轨道数定理"
        "_精算与可视化_%s" % DATE)

trees = [("源码", os.path.join(BASE, "源码")),
         ("数据", os.path.join(BASE, "数据")),
         ("判定", os.path.join(BASE, "判定"))]

print("[probe] RID = %s" % RID)
print("[probe] DATE = %s" % DATE)
print("[probe] STEM = %s" % STEM)
print("[probe] len(STEM) = %d" % len(STEM))

anc = "TUFT-r%s_" % RID
tot = 0
for tag, d in trees:
    try:
        fs = os.listdir(d)
    except Exception as e:
        print("[probe] %s MISSING (%s)" % (tag, e))
        continue
    hit = sorted(f for f in fs if anc in f)
    tot += len(hit)
    print("[probe] %s hit=%d" % (tag, len(hit)))
    for f in hit:
        print("          " + f[:100])

d = os.path.join(BASE, "数据")
hit2 = sorted(f for f in os.listdir(d) if ("判定_" + anc) in f)
tot += len(hit2)
print("[probe] 数据/判定_* hit=%d" % len(hit2))
print("[probe] TOTAL = %d ==> %s" % (tot, "COLD 可占用" if tot == 0 else "TAKEN 让号"))
