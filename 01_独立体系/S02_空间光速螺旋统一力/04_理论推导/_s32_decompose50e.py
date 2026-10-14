# -*- coding: utf-8 -*-
"""sym(10⊗10) 55 -> 分组；减 5̄ -> 50。含负值断言与规范化修复"""
from collections import Counter

def norm(w):
    return tuple(x - w[0] for x in w)

def proj(w):
    su3 = (w[0]-w[1], w[1]-w[2])
    s = (w[3]-w[4])
    y = -2*(w[0]+w[1]+w[2]) + 3*(w[3]+w[4])
    return su3, s, y

w5 = [tuple(1 if i==k else 0 for k in range(5)) for i in range(5)]
w10 = [tuple(w5[i][k]+w5[j][k] for k in range(5)) for i in range(5) for j in range(i+1,5)]
w10sym = [tuple(w10[i][k]+w10[j][k] for k in range(5)) for i in range(10) for j in range(i,10)]
cnt = Counter(norm(w) for w in w10sym)

def dump(cnt, title):
    print(f"\n=== {title} (总权重数 {sum(cnt.values())}) ===")
    agg = Counter()
    for w, m in cnt.items():
        su3, s, y = proj(w)
        agg[(su3, s, y)] += m
    assert all(v >= 0 for v in agg.values()), f"negative: {[(k,v) for k,v in agg.items() if v<0]}"
    for k, m in sorted(agg.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
        print(f"  s={k[1]:3d} Y3={k[2]:5d}  SU3=({k[0][0]:2d},{k[0][1]:2d})  n={m}")

dump(cnt, "sym(10⊗10) 全 55 权重")

# 减 5̄（用规范化键）
w5bar = [norm(tuple(-1 if i==k else 0 for k in range(5))) for i in range(5)]
for w in w5bar:
    assert cnt[w] >= 1, f"5̄ weight not in sym: {w}"
    cnt[w] -= 1
    if cnt[w] == 0: del cnt[w]
dump(cnt, "减 5̄ 后 = 50 表示")
