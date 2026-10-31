# -*- coding: utf-8 -*-
r"""
r251 探针 · 候选层：质量谱（m_p/m_e） vs 宇宙学常数 Λ
================================================================================
目的：判断哪一层有「靶给出的、带数值的、可机验的推导式」。
================================================================================
"""

import io
import math
import os
import re

DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
T = [
    os.path.join(DATA_DIR, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
]


def rt(p):
    try:
        return io.open(p, "r", encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


ALL = "".join(rt(p) for p in T)
RAW = rt(T[0])
LINES = RAW.split("\n")


def sec(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def show(pat, n=5, w=150, label=""):
    ms = list(re.finditer(pat, ALL))
    print("-- %s %s  命中 %d" % (label or pat, "", len(ms)))
    for m in ms[:n]:
        a, b = max(0, m.start() - w), min(len(ALL), m.end() + w)
        print("   ...%s..." % ALL[a:b].replace("\n", "\\n"))
    print("")


# ---------------------------------------------------------------- 候选 A
sec("候选 A · m_p/m_e 质子电子质量比（实测 1836.15267343）")
show(r"m_p/m_e", n=5, w=170, label="[m_p/m_e]")
show(r"1836", n=5, w=150, label="[1836]")
show(r"质量比", n=4, w=140, label="[质量比]")

# ---------------------------------------------------------------- 候选 B
sec("候选 B · 宇宙学常数 Λ / 暗能量")
show(r"宇宙学常数", n=4, w=150, label="[宇宙学常数]")
show(r"暗能量", n=3, w=140, label="[暗能量]")
show(r"哈勃", n=3, w=130, label="[哈勃]")

# ---------------------------------------------------------------- 候选 C
sec("候选 C · 自旋 / 磁矩 / 霍金温度")
show(r"霍金", n=3, w=130, label="[霍金]")
show(r"磁矩", n=3, w=130, label="[磁矩]")

# ---------------------------------------------------------------- 数值判定
sec("D · 关键实测值对照（供后续判据用）")
M_P = 1.67262192369e-27
M_E = 9.1093837015e-31
print("  m_p/m_e（CODATA）      = %.8f" % (M_P / M_E))
print("  m_p/m_e 常用近似        = 1836.15267343")
print("  √3/2                   = %.8f" % (math.sqrt(3) / 2))
print("  2π                     = %.8f" % (2 * math.pi))
print("  (2π)^2                 = %.8f" % ((2 * math.pi) ** 2))
print("  6π^5                   = %.4f" % (6 * math.pi ** 5))
print("  √(m_p/m_e)             = %.6f" % math.sqrt(M_P / M_E))
print("  ln(m_p/m_e)            = %.6f" % math.log(M_P / M_E))
print("  m_p/m_e / 1836         = %.8f" % ((M_P / M_E) / 1836))
print("  α^-1                   = %.6f" % (1 / 7.2973525693e-3))
print("  α^-1 / (m_p/m_e)       = %.6f" % ((1 / 7.2973525693e-3) / (M_P / M_E)))

print("\nDONE")
