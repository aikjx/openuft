# -*- coding: utf-8 -*-
r"""
元探针：对 TUFT-r244 的 9 条 FAIL 做反向体检（只读，不改任何产物）
================================================================================
探 9 件事：
 P1  E2 声称「靶命中 G-推导式 6 处」——这 6 处到底是什么？是假阳性吗？
 P2  C2 声称「测地偏离/潮汐 0 处」——token 集够不够宽？换同义词会不会有？
 P3  D1 声称「类光无 Frenet 标架」——靶是否提供了广义零标架（Cartan/伪弧长/Newman-Unti）？
 P4  D2/D3 用的质量式 m=(hbar/c)*sqrt(k^2+t^2) 在靶里是否真实存在？
 P5  D3 备注「κ 跨 4 个数量级」——实测跨几个？
 P6  来料 line 59/105/383/393 是否逐字位于声称的行号？
 P7  C2 的「黎曼/曲率张量 3 处」是什么上下文？
 P8  F1 修复定价是否结构性退化（SURVIVE 恒 0）？
 P9  κ 与 Riemann 的数值桥接：c^2*κ vs c^2*R*xi 同量纲，C1 的「量纲不同阶」是否够用？
================================================================================
"""

import io
import os
import re
import sys
from fractions import Fraction

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


def sec(s):
    print("")
    print("=" * 78)
    print(s)
    print("=" * 78)


# ---------------------------------------------------------------- P1
sec("P1 · E2 的 6 处 G-推导式命中：到底是什么？")
G_DERIV_RES = [
    re.compile(r"G\s*=\s*[^\n=]{0,80}?(?:κ|kappa)"),
    re.compile(r"G\s*=\s*[^\n=]{0,80}?(?:τ|tau)"),
    re.compile(r"(?:万有引力常数|引力常数)\s*(?:由|等于|推导|给出)\s*[^\n]{0,60}"),
]
for n, rgx in enumerate(G_DERIV_RES, 1):
    print("-- 正则 %d: %s" % (n, rgx.pattern))
    for m in rgx.finditer(ALL):
        a, b = max(0, m.start() - 45), min(len(ALL), m.end() + 45)
        print("   HIT: ...%s..." % ALL[a:b].replace("\n", "\\n"))
    print("   小计 %d" % len(rgx.findall(ALL)))

print("")
print("-- 窄窗复检（窗口 20 / 12 / 6 字符）：")
for w in (20, 12, 6):
    r1 = re.compile(r"G\s*=\s*[^\n=]{0,%d}?(?:κ|tau|τ)" % w)
    r2 = re.compile(r"G\s*=\s*[^\n=]{0,%d}?(?:κ|tau|τ)" % w)
    print("   窗口%2d: κ/τ 命中 %d" % (w, len(r1.findall(ALL))))
    for m in r1.finditer(ALL):
        a, b = max(0, m.start() - 40), min(len(ALL), m.end() + 40)
        print("        ...%s..." % ALL[a:b].replace("\n", "\\n"))

print("")
print("-- 负对照：注入『G 附近有 κ 但无推导』的文本，宽窗是否误报？")
NEG = ("引力常数 G = 6.67430e-11 在 SI 中定义。我们在第 3 章讨论了螺旋曲率 κ "
       "与挠率 τ 的性质，二者无关。另外 G = 6.674e-11 时 κ 的取值另行讨论。")
for n, rgx in enumerate(G_DERIV_RES, 1):
    print("   正则%d 在负对照上命中 %d（应 0）" % (n, len(rgx.findall(NEG))))
    for m in rgx.finditer(NEG):
        print("        FALSE-POS: %s" % m.group(0)[:90])

# ---------------------------------------------------------------- P2
sec("P2 · C2 的潮汐/测地偏离 token 覆盖度")
TOK_SETS = {
    "r244原集合": ["测地偏离", "测地线偏离", "潮汐", "geodesic deviation"],
    "扩展集合": ["测地偏离", "测地线偏离", "潮汐", "引潮力", "起潮力", "潮汐力",
                 "纳潮", "geodesic deviation", "tidal", "tide", "Tidal",
                 "引力梯度", "梯度引力", "潮汐张量", "electric Weyl", "Ricci"],
}
for name, toks in TOK_SETS.items():
    print("-- %s" % name)
    tot_raw = tot_all = 0
    for tk in toks:
        a, b = RAW.count(tk), ALL.count(tk)
        tot_raw += a
        tot_all += b
        if a or b:
            print("   %-22s RAW %-5d ALL %d" % (tk, a, b))
    print("   合计 RAW %d / ALL %d" % (tot_raw, tot_all))

# ---------------------------------------------------------------- P3
sec("P3 · D1：靶是否提供广义零曲线标架（对靶有利的反例搜索）")
NULL_FRAME = ["Cartan", "cartan", "伪弧长", "拟弧长", "pseudo-arc", "pseudo arc",
              "Newman", "Sachs", "零标架", "类光标架", "伪正交", "零曲线",
              "null frame", "null curve", "零测地", "重新参数", "重参数",
              "reparamet", "仿射参数", "affine parameter"]
for tk in NULL_FRAME:
    a, b = RAW.count(tk), ALL.count(tk)
    if a or b:
        print("   %-20s RAW %-4d ALL %d" % (tk, a, b))
        for m in re.finditer(re.escape(tk), ALL):
            s, e = max(0, m.start() - 60), min(len(ALL), m.end() + 60)
            print("        ...%s..." % ALL[s:e].replace("\n", "\\n"))
            break
print("   （未列出的 token 即 0 处）")

# ---------------------------------------------------------------- P4
sec("P4 · D2/D3 的质量式 m=(ℏ/c)√(κ²+τ²) 在靶里是否真实存在")
PATS = [r"m\s*=\s*\(?\s*ℏ\s*/\s*c\s*\)", r"ℏ\s*/\s*c", r"hbar\s*/\s*c",
        r"√\s*\(\s*κ", r"sqrt\s*\(\s*κ", r"κ\s*²\s*\+\s*τ", r"κ\^2\s*\+\s*τ"]
for p in PATS:
    hits = re.findall(p, ALL)
    print("   %-28s ALL %d" % (p, len(hits)))
for m in re.finditer(r"ℏ\s*/\s*c", ALL):
    s, e = max(0, m.start() - 90), min(len(ALL), m.end() + 90)
    print("       ctx: ...%s..." % ALL[s:e].replace("\n", "\\n"))
print("-- 质量相关行抽样：")
for m in re.finditer(r"[^。\n]{0,60}质量[^。\n]{0,80}(?:κ|曲率)[^。\n]{0,60}", RAW):
    print("       %s" % m.group(0).strip()[:170])

# ---------------------------------------------------------------- P5
sec("P5 · D3 「κ 跨 4 个数量级」复核")
g = 9.80665
HBAR = 6.62607015e-34 / (2 * 3.141592653589793)
C = 299792458.0
rows = []
for v in (0.0, 1.0, 10.0, 100.0, 1000.0):
    kap = 0.0 if v == 0 else g / v ** 2
    rows.append((v, kap, (HBAR / C) * kap))
for v, k, mm in rows:
    print("   v=%-8g kappa=%-14.6g m=%-12.6g kg" % (v, k, mm))
import math
k1, k1000 = rows[1][1], rows[4][1]
print("   κ(1)/κ(1000) = %.6g  ⇒ %.4g 个数量级" % (k1 / k1000, math.log10(k1 / k1000)))
print("   m(1)/m(1000) = %.6g  ⇒ %.4g 个数量级" % (rows[1][2] / rows[4][2],
                                                   math.log10(rows[1][2] / rows[4][2])))
print("   验 κ*v^2 是否恒等于 g：")
for v, k, _ in rows[1:]:
    print("       v=%-7g κ*v^2=%.10g  (g=%.10g) 差 %.3g" % (v, k * v ** 2, g, k * v ** 2 - g))

# ---------------------------------------------------------------- P6
sec("P6 · 来料 line 59/105/383/393 逐字核验")
LINES = RAW.split("\n")
print("   来料原件总行数 %d" % len(LINES))
for ln in (59, 105, 217, 255, 383, 393):
    idx = ln - 1
    if idx < len(LINES):
        print("   line %-4d | %s" % (ln, LINES[idx].strip()[:150]))
    else:
        print("   line %-4d | <超出范围>" % ln)

# ---------------------------------------------------------------- P7
sec("P7 · C2 的「黎曼/曲率张量 3 处」上下文")
for tk in ("Riemann", "黎曼", "曲率张量"):
    for m in re.finditer(re.escape(tk), ALL):
        s, e = max(0, m.start() - 70), min(len(ALL), m.end() + 70)
        print("   [%s] ...%s..." % (tk, ALL[s:e].replace("\n", "\\n")))

# ---------------------------------------------------------------- P8
sec("P8 · F1 修复定价是否结构性退化")
from itertools import product
KEYS = ("intrinsic_curvature", "geodesic_deviation", "covariant_frenet",
        "timelike_carrier", "g_from_geometry")
SKEL = {"intrinsic_curvature", "geodesic_deviation", "covariant_frenet"}
cnt = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
for combo in product((False, True), repeat=len(KEYS)):
    have = {k for k, v in zip(KEYS, combo) if v}
    if len(have) < len(KEYS):
        cnt["EMPTY"] += 1
    elif SKEL.issubset(have):
        cnt["SUICIDE"] += 1
    else:
        cnt["SURVIVE"] += 1
print("   现行判定：%s" % cnt)
print("   ⇒ len(have)<5 的组合恒为 EMPTY，唯一满配组合必含 SKEL ⇒ SURVIVE 恒 0（结构性）")
print("")
print("-- 判别力测试：是否存在任何 5 槽位方案能让 SURVIVE>0？")
print("   现行规则下：不可能。枚举器对『任意』靶的输出都是 (31,1,0)。")
print("   反证：把 SKEL 换成 {intrinsic_curvature} 单元素，重算：")
SKEL2 = {"intrinsic_curvature"}
c2 = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
for combo in product((False, True), repeat=len(KEYS)):
    have = {k for k, v in zip(KEYS, combo) if v}
    if len(have) < len(KEYS):
        c2["EMPTY"] += 1
    elif SKEL2.issubset(have):
        c2["SUICIDE"] += 1
    else:
        c2["SURVIVE"] += 1
print("   ⇒ %s  同样 SURVIVE=0" % c2)
print("   结论：只要『满配』是 SURVIVE 的前置条件且 SKEL⊆满配，SURVIVE 恒 0。")
print("   正确做法：SURVIVE 的前置条件应改为『满足最小可交付要求』，而非『全部槽位补齐』。")

print("")
print("-- 最小可交付要求重定义后的三档：")
REQ = {"intrinsic_curvature", "geodesic_deviation"}   # 至少要能出 L^-2 级潮汐
c3 = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
surv = []
for combo in product((False, True), repeat=len(KEYS)):
    have = {k for k, v in zip(KEYS, combo) if v}
    if not REQ.issubset(have):
        c3["EMPTY"] += 1
    elif SKEL.issubset(have):
        c3["SUICIDE"] += 1
    else:
        c3["SURVIVE"] += 1
        surv.append(sorted(have))
print("   %s" % c3)
for s in surv:
    print("       SURVIVE 组合：%s" % s)

# ---------------------------------------------------------------- P9
sec("P9 · C1 的反例强度：c²κ 与 c²Rξ 同量纲")
G = 6.67430e-11
GME = 3.986004418e14
RE = 6378137.0
AU = 1.495978707e11
GMS = 1.32712440018e20
for label, GM, r in (("地球表面", GME, RE), ("1 AU(太阳)", GMS, AU)):
    k_ansatz = GM / (C ** 2 * r ** 2)          # 靶 ansatz κ(r)，λ=0（对靶最有利）
    riem = 2.0 * GM / (C ** 2 * r ** 3)        # Riemann 量级 R
    sq = riem ** 0.5                            # sqrt(R)，量纲 L^-1
    a_from_k = C ** 2 * k_ansatz                # 靶路线：c^2*kappa → 加速度
    tidal_per_m = 2.0 * GM / r ** 3             # GR 路线：潮汐梯度 s^-2
    print("   %s:" % label)
    print("       靶 κ_ansatz   = %.6g m^-1" % k_ansatz)
    print("       sqrt(Riem)    = %.6g m^-1   ⇒ κ/sqrt(R) = %.6g" % (sq, k_ansatz / sq))
    print("       c^2*κ         = %.6g m/s^2  （力图像）" % a_from_k)
    print("       潮汐梯度      = %.6g s^-2   （需分离矢量 ξ 才成加速度）" % tidal_per_m)
    print("       ⇒ 二者量纲桥接后【同为 L T^-2】，故『量纲不同阶』单独不足以定罪")

print("")
print("DONE")
