# -*- coding: utf-8 -*-
"""r252 深探：质量谱层（m_p/m_e 等）。只读，不改任何文件。"""
import re, os, math, io, sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "数据", "TUFT-r241_光速螺旋_来料原件_2026-10-30")
F1 = os.path.join(SRC, "基于光速螺旋流形的核心动力学方程组.md")
F2 = os.path.join(BASE, "数据", "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md")
F3 = os.path.join(BASE, "数据", "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md")

def read_text(p):
    try:
        with io.open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return ""

_ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def depollute(s):
    # 上游污染：字母 X 被替换成 \(\boldsymbol{X}\)（t 最普遍，\hbar 里的 b 同理）
    # 用精确字符串替换，避免正则转义陷阱
    for ch in _ALPHA:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    s = re.sub(r"[\r\n]+", "\n", s)
    return s

DOCS = {}
for tag, p in (("R241", F1), ("R241B", F2), ("R242", F3)):
    t = read_text(p)
    DOCS[tag] = depollute(t)
    print("[%s] chars=%d  lines=%d  path=%s" % (tag, len(t), t.count("\n") + 1, p))

ALL = "\n".join(DOCS.values())
print("ALL chars = %d" % len(ALL))
print("pollution check  \\(\\boldsymbol : %d" % ALL.count("\\(\\boldsymbol"))

def ctx(tag, pat, win=3, limit=12):
    lines = DOCS[tag].split("\n")
    out = []
    for i, s in enumerate(lines):
        if re.search(pat, s):
            out.append((i + 1, s))
    return out

def show(title, tag, pat, limit=12, win=2):
    hits = ctx(tag, pat)
    print("\n" + "=" * 78)
    print("## %s   [%s]  regex=%s   hits=%d" % (title, tag, pat, len(hits)))
    lines = DOCS[tag].split("\n")
    for (ln, s) in hits[:limit]:
        lo = max(0, ln - 1 - win)
        hi = min(len(lines), ln - 1 + win + 1)
        print("---- line %d ----" % ln)
        for k in range(lo, hi):
            mark = ">>" if k == ln - 1 else "  "
            print("%s %5d| %s" % (mark, k + 1, lines[k][:300]))

# ---------- 1. 质量比主战场 ----------
for tag in ("R241", "R241B", "R242"):
    show("质量比 m_p/m_e", tag, r"m_p\s*/\s*m_e|m_\{p\}|质子.{0,6}电子", limit=8)
    show("1836", tag, r"1836", limit=8)
    show("mathcal K", tag, r"\\mathcal\{K\}|\bK\\?_?\{?QCD|\\mathcal\{K\}", limit=8)

# ---------- 2. 是否用了 6\pi^5 之类数字巧合 ----------
print("\n" + "=" * 78)
print("## 数字巧合排查（先测后指控：语料里到底有没有）")
for expr, val in (("6\\pi^5", 6 * math.pi ** 5), ("6\\pi^{5}", 6 * math.pi ** 5),
                  ("\\pi^5", math.pi ** 5), ("1836.15", None),
                  ("2\\pi", 2 * math.pi), ("4\\pi", 4 * math.pi)):
    n = len(re.findall(re.escape(expr), ALL))
    print("  %-12s 出现 %d 次   数值=%s" % (expr, n, val))
print("  6pi^5 = %.7f   vs  1836.1526734  相对差=%.3e"
      % (6 * math.pi ** 5, abs(6 * math.pi ** 5 - 1836.15267343) / 1836.15267343))

# ---------- 3. 其他质量 / 费米子谱 ----------
print("\n" + "=" * 78)
print("## 费米子质量谱关键词计数（全语料）")
for kw in ("m_\\mu", "m_\\tau", "\\muon", "206.768", "3477", "1776.86", "105.658",
           "Koide", "koide", "\\frac{m_e+m_\\mu+m_\\tau}", "三代", "CKM",
           "PMNS", "中微子", "m_t", "m_b", "m_c", "m_s", "m_u", "m_d",
           "顶夸克", "底夸克", "173.1", "4.18", "1.27"):
    print("  %-26s %d" % (kw, len(re.findall(re.escape(kw), ALL))))

# ---------- 4. 积分 / Lambda_QCD ----------
for tag in ("R241", "R241B", "R242"):
    show("Lambda_QCD / 积分", tag, r"\\Lambda_\{?QCD|\\Lambda_\{QCD\}", limit=6)
    show("int dmu/mu", tag, r"\\int", limit=6)

# ---------- 5. 质量定义主干 ----------
for tag in ("R241", "R241B"):
    show("质量公式 boxed", tag, r"oxed\{m", limit=10)
    show("m = hbar ...", tag, r"oxed\{[^}]*m\s*=", limit=10)

# ---------- 6. 数值锚点 ----------
print("\n" + "=" * 78)
print("## 参考数值（用于后续对拍）")
mp_over_me = 1836.15267343
print("  m_p/m_e        = %.8f" % mp_over_me)
print("  ln(m_p/m_e)    = %.6f" % math.log(mp_over_me))
print("  sqrt(m_p/m_e)  = %.6f" % math.sqrt(mp_over_me))
print("  6*pi^5         = %.6f  (rel diff %.3e)" %
      (6 * math.pi ** 5, abs(6 * math.pi ** 5 - mp_over_me) / mp_over_me))
print("  (m_p/m_e)/3    = %.6f" % (mp_over_me / 3))
print("  (m_p/m_e)/3-1  = %.6f" % (mp_over_me / 3 - 1))
print("  alpha^-1       = 137.035999")
print("  alpha^-1 * 13.4 = %.4f" % (137.035999 * 13.4))
print("  exp(7.515428)  = %.4f" % math.exp(7.515428))
