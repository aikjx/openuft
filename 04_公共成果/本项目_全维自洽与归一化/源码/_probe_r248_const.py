# -*- coding: utf-8 -*-
r"""
r248 探针 · 常数谱系层：靶宣称「TUFT 减少基本常数数目」
================================================================================
探 8 件事：
 P1  α_* = √3/2（裸耦合固定点）在靶里怎么来的？有没有推导？是不是 Frenet 几何必然？
 P2  「减少基本常数数目」的宣称原文与计数（到底减了几个？）
 P3  普朗克标度 M_P / l_P / t_P 的导出链
 P4  c、ℏ 是公理还是导出？
 P5  有没有能标 / 跑动方程 / 匹配条件（α_* 与实测 α 之间）？
 P6  常数总数清点：靶列了几个"输入"、几个"导出"？
 P7  √3/2 与螺旋几何：κ/τ 取什么值才得 √3/2？是唯一吗？
 P8  与实测 α=1/137.036 的差距与靶是否给出桥接
================================================================================
"""

import io
import math
import os
import re

DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
TARGETS = [
    os.path.join(DATA_DIR, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
]


def read_text(p):
    try:
        with io.open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


T = {p: read_text(p) for p in TARGETS}
RAW = T[TARGETS[0]]
ALL = "".join(T[p] for p in TARGETS)
LINES = RAW.split("\n")


def sec(s):
    print("")
    print("=" * 78)
    print(s)
    print("=" * 78)


def show(pat, n=6, w=110, corpus=ALL, tag="ALL"):
    print("-- 正则 %s  (语料=%s)" % (pat, tag))
    ms = list(re.finditer(pat, corpus))
    print("   命中 %d 处" % len(ms))
    for m in ms[:n]:
        a, b = max(0, m.start() - w), min(len(corpus), m.end() + w)
        print("   ...%s..." % corpus[a:b].replace("\n", "\\n"))
    print("")


# ---------------------------------------------------------------- P1
sec("P1 · α_* = √3/2 裸耦合固定点：来源与推导")
for pat in [r"裸耦合", r"固定点", r"alpha_\*", r"α_\*", r"α\*",
            r"\\sqrt\{3\}/2", r"√3/2", r"frac\{\\sqrt\{3\}\}\{2\}"]:
    show(pat, n=4, w=130)

# ---------------------------------------------------------------- P2
sec("P2 · 「减少基本常数数目」宣称")
for pat in [r"减少.{0,20}常数", r"常数数目", r"基本常数.{0,30}(?:减|少|降)",
            r"(?:减|少|降低).{0,10}独立.{0,10}常数"]:
    show(pat, n=4, w=130)

# ---------------------------------------------------------------- P3
sec("P3 · 普朗克标度 M_P / l_P / t_P 导出链")
for pat in [r"普朗克质量", r"普朗克时间", r"M_P", r"l_P", r"t_P"]:
    print("   %-14s ALL %d  RAW %d" % (pat, len(re.findall(pat, ALL)), len(re.findall(pat, RAW))))
print("")

# ---------------------------------------------------------------- P4
sec("P4 · c / ℏ 是公理还是导出？")
for pat in [r"光速.{0,15}公理", r"约化普朗克常数", r"涡旋角动量量子", r"传播速度公理"]:
    show(pat, n=3, w=110)

# ---------------------------------------------------------------- P5
sec("P5 · 能标 / 跑动 / 匹配条件（α_* 与实测 α 的桥接）")
for pat in [r"能标", r"跑动", r"重整化", r"renormaliz", r"running",
            r"匹配条件", r"精细结构常数", r"1/137", r"137\.03"]:
    print("   %-16s ALL %d" % (pat, len(re.findall(pat, ALL))))
print("")

# ---------------------------------------------------------------- P6
sec("P6 · 常数谱系段落（line 5720-5760 原文）")
for i in range(5718, min(5762, len(LINES))):
    print("   line %-5d | %s" % (i + 1, LINES[i].strip()[:150]))

# ---------------------------------------------------------------- P7
sec("P7 · √3/2 与螺旋几何：κ/τ 取什么值才得 √3/2？是否唯一？")
print("   圆柱螺旋 x=a cos t, y=a sin t, z=bt：")
print("     κ = a/(a²+b²),  τ = b/(a²+b²)  ⇒ κ/τ = a/b（自由，非几何固定）")
print("     切矢轴向分量 Tz = b/√(a²+b²) = 1/√(1+(a/b)²)")
for ratio in (1.0 / math.sqrt(3.0), 1.0, math.sqrt(3.0), 0.5, 2.0):
    tz = 1.0 / math.sqrt(1.0 + ratio ** 2)
    print("     a/b=%.6f ⇒ Tz=%.6f %s" % (ratio, tz,
                                          ("  ← √3/2 命中" if abs(tz - math.sqrt(3) / 2) < 1e-12
                                           else "")))
print("")
print("   ⇒ Tz=√3/2 对应 a/b = 1/√3，即 κ/τ = 1/√3；这是【一个选择】，不是几何必然。")
print("   ⇒ 同理任何 Tz∈(0,1) 都可由某个 a/b 实现 ⇒ √3/2 无唯一性。")

# ---------------------------------------------------------------- P8
sec("P8 · α_* 与实测 α 的差距")
a_star = math.sqrt(3.0) / 2.0
alpha = 7.2973525693e-3
print("   α_* = √3/2      = %.10f" % a_star)
print("   α (实测, 精细结构) = %.10e = 1/%.6f" % (alpha, 1.0 / alpha))
print("   比值 α_*/α       = %.4f  （差 %.2f 倍）" % (a_star / alpha, a_star / alpha))
print("   靶是否给出能标/跑动方程把二者接上？见 P5。")

print("")
print("DONE")
