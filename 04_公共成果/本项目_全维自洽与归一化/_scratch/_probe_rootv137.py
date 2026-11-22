# -*- coding: utf-8 -*-
"""一次性探针：ROOT V137 核心结构是否成立（命中后再写引擎）。
只验四件事：迹恒等式 / 完美平方可解性 / radion 系数被迫性 / 背景几何唯一性。"""
from fractions import Fraction as F
import itertools, random

# ---------------- 1 迹恒等式（16 权重 = 偶数个负号）
W = []
for s in itertools.product([1, -1], repeat=5):
    if sum(1 for v in s if v < 0) % 2 == 0:
        W.append([F(v, 2) for v in s])
assert len(W) == 16


def dot(x, w):
    return sum(F(a) * F(b) for a, b in zip(x, w))


def tr2(x):
    return sum(dot(x, w) ** 2 for w in W)


def tr4(x):
    return sum(dot(x, w) ** 4 for w in W)


def vec2(x):
    return 2 * sum(F(c) * F(c) for c in x)


def vec4(x):
    return 2 * sum(F(c) ** 4 for c in x)


pts = [[F(1), F(2), F(3), F(4), F(5)],
       [F(1), F(0), F(0), F(0), F(0)],
       [F(3, 7), F(-5, 11), F(0), F(2), F(-1, 13)],
       [F(-2), F(9, 4), F(1, 3), F(-7, 5), F(11, 6)]]
random.seed(7)
for _ in range(6):
    pts.append([F(random.randint(-9, 9), random.randint(1, 9)) for _ in range(5)])

bad2 = bad4 = 0
for x in pts:
    if tr2(x) != 2 * vec2(x):
        bad2 += 1
    if tr4(x) != F(3, 4) * vec2(x) ** 2 - vec4(x):
        bad4 += 1
print("TRACE  2nd fails=%d  4th fails=%d  (n=%d)" % (bad2, bad4, len(pts)))
x = pts[0]
print("  sample x=(1,2,3,4,5): tr16_2=%s vs 2*tr10_2=%s" % (tr2(x), 2 * vec2(x)))
print("  tr16_4=%s vs 3/4*(tr10_2)^2-tr10_4=%s" % (tr4(x), F(3, 4) * vec2(x) ** 2 - vec4(x)))

# ---------------- 2 I8^total 是否完美平方：X=a*p1+b*Q+c*y2，X^2 = k*I8
# I8 = (1/2) Q y^2 - (1/3) p1 y^2 + (2/3) y^4
# X^2 = a^2 p1^2 + 2ab p1 Q + b^2 Q^2 + 2ac p1 y2 + 2bc Q y2 + c^2 y4
sols = []
for a in range(-6, 7):
    for b in range(-6, 7):
        for c in range(-6, 7):
            if a == 0 and b == 0 and c == 0:
                continue
            # 目标系数：p1^2:0, p1Q:0, Q^2:0, p1y2:-1/3, Qy2:1/2, y4:2/3
            tgt = [F(0), F(0), F(0), F(-1, 3), F(1, 2), F(2, 3)]
            got = [F(a * a), F(2 * a * b), F(b * b), F(2 * a * c), F(2 * b * c), F(c * c)]
            ks = set(g / t for g, t in zip(got, tgt) if t != 0)
            zeros_ok = all(g == 0 for g, t in zip(got, tgt) if t == 0)
            if zeros_ok and len(ks) == 1 and list(ks)[0] != 0:
                sols.append((a, b, c, list(ks)[0]))
print("PERFECT-SQUARE integer solutions:", sols)

# ---------------- 3 radion：V=A e^-6s + B e^-2s - C e^-4s，V(0)=V'(0)=0 迫 A=B=C/2
forced = []
for A in range(1, 40):
    for B in range(1, 40):
        for C in range(1, 40):
            if A + B - C != 0:
                continue
            if -6 * A - 2 * B + 4 * C != 0:
                continue
            forced.append((A, B, C))
ratio_ok = all(2 * A == C and A == B for A, B, C in forced)
print("RADION forced triples (A,B,C) with A,B,C<40: n=%d  all A=B=C/2: %s  e.g.%s"
      % (len(forced), ratio_ok, forced[:5]))

# ---------------- 4 背景：三种常曲率二维内空间
# 内方程恒给 Lam = 4 pi G B^2/g^2 > 0。外方程：k*1/R^2 + Lam = -4 pi G B^2/g^2, k=+1(S2) 0(T2) -1(H2)
Lam = 1  # 归一化
for name, k in [("S^2", 1), ("T^2", 0), ("H^2", -1)]:
    # k/R^2 = -2 Lam  ->  R^2 = -k/(2 Lam) > 0 需要 -k>0
    kk = -k
    ok = (kk > 0)
    print("BG %-4s k=%+d  R^2 = %s  consistent=%s" % (name, k, ("%s/(2Lam)" % kk), ok))
