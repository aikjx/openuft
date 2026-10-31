# -*- coding: utf-8 -*-
r"""r264 前置只读探测：符号总表 / 四态分类 / ω 高精度数 / 四力力程对拍 / 八粒子表互算"""
import io
import os
import re
import unicodedata
import collections
from decimal import Decimal as D, getcontext

getcontext().prec = 60

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
MY = r"D:\a10\aikjx\code\my_lib"

TARGETS = [
    ("T0_定稿全书", os.path.join(MY, "TUFT_四力大统一_垂直原理螺旋统一场论_定稿全书.md")),
    ("T1_核心动力学方程组", os.path.join(MY, "_tmp_r246_来料", "基于光速螺旋流形的核心动力学方程组.md")),
    ("T2_修改攻破", os.path.join(MY, "_tmp_r246_来料", "修改攻破.md")),
    ("T3_V40", os.path.join(ROOT, "数据", "TUFT-V40终极力的统一方程_来料全文_2026-10-17.md")),
    ("T4_压缩版", os.path.join(ROOT, "数据", "TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md")),
    ("T5_S12", os.path.join(MY, "openuft", "01_独立体系", "S12_空间光速螺旋统一体系",
                            "13_论文与成果", "论文正文", "大统一方程全集.md")),
    ("T6_S02", os.path.join(MY, "openuft", "01_独立体系", "S02_空间光速螺旋统一力",
                            "04_理论推导", "§18_四力统一方程_力的本源与大小方向距离_攻破精算.md")),
    ("T7_S14", os.path.join(MY, "openuft", "01_独立体系", "S14_挠率统一场论TUFT",
                            "13_论文与成果", "论文正文", "原稿",
                            "四力统一_四大相互作用完整规范群统一结构_原文.md")),
]

TEXTS = {}
for nm, p in TARGETS:
    try:
        TEXTS[nm] = io.open(p, "r", encoding="utf-8", errors="replace").read()
        print("OK  %-22s %8d 行  %8d 字符" % (nm, TEXTS[nm].count("\n") + 1, len(TEXTS[nm])))
    except Exception as e:
        TEXTS[nm] = ""
        print("MISS %-22s %s" % (nm, e))

print("\n" + "=" * 78)
print("【一】符号候选自动发现（三种互补扫描）")
print("=" * 78)

LATEX_STOP = {"frac", "sqrt", "left", "right", "cdot", "times", "quad", "qquad", "text",
              "mathrm", "begin", "end", "label", "tag", "partial", "nabla", "sum", "int",
              "lim", "exp", "ln", "log", "sin", "cos", "tan", "mathbf", "boldsymbol", "rm",
              "displaystyle", "bar", "hat", "vec", "tilde", "dot", "ldots", "cdots"}

gc = collections.Counter()
lc = collections.Counter()
sc = collections.Counter()
for nm, t in TEXTS.items():
    for ch in t:
        try:
            n = unicodedata.name(ch)
        except ValueError:
            continue
        if ("GREEK" in n) or ("MATHEMATICAL" in n) or ("SCRIPT" in n):
            gc[ch] += 1
    for m in re.findall(r"\\([A-Za-z]+)", t):
        if m not in LATEX_STOP:
            lc[m] += 1
    for b, s in re.findall(r"([A-Za-zωκτρλ𝒦ℓ]+)_[\{]?([A-Za-z0-9*])[\}]?", t):
        sc["%s_%s" % (b, s)] += 1

print("Unicode 数学符号 TOP20:", " ".join("%s:%d" % (c, n) for c, n in gc.most_common(20)))
print()
print("LaTeX 宏 TOP20:", " ".join("%s:%d" % (c, n) for c, n in lc.most_common(20)))
print()
print("带下标符号 TOP12:", " ".join("%s:%d" % (c, n) for c, n in sc.most_common(12)))

print("\n" + "=" * 78)
print("【二】ω 高精度数（Decimal 60 位）")
print("=" * 78)

HBARC = D("197.3269804")        # MeV·fm
M_E = D("0.51099895000")        # MeV
C = D("299792458")
HBAR = D("1.054571817e-34")
G_N = D("6.67430e-11")
M_P_MEV = D("938.27208816")
MW_MEV = D("80377.0")
MPI0_MEV = D("134.9768")

# 电子康普顿频率 = m_e c^2 / hbar
w_e = M_E * D("1e6") * D("1.602176634e-19") / HBAR
w_e2 = (M_E / HBARC) * C * D("1e15")       # (m/hbarc)*c,  fm->m
print("ω_e = m_e c²/ħ  (路径1) = %.12e s⁻¹" % w_e)
print("ω_e = (m/ħc)·c       (路径2) = %.12e s⁻¹" % w_e2)
print("     靶给 L1755 = 7.763×10²⁰ s⁻¹   相对差 = %.3e" % (abs(w_e - D("7.763e20")) / w_e))

w_l3369 = D("4.803e40")
print()
print("ω(L3369) = %.6e s⁻¹" % w_l3369)
ratio = w_l3369 / w_e
# log10 via Decimal
def dex(x):
    return x.log10()
print("ω(L3369) / ω_e = %.12e  = %.7f dex   （靶自述 L3520：19.79 dex）" % (ratio, dex(ratio)))

lam = C / w_l3369
lP = D("1.616255e-35")
print()
print("λ = c/ω(L3369) = %.12e m  = %.6f ℓ_P" % (lam, lam / lP))
lamC_e_fm = HBARC / M_E
print("λ̄_C(e) = ħc/m_e = %.10f fm   （以 fm 读数）" % lamC_e_fm)
print("⇒ λ/ℓ_P = %.6f  vs  λ̄_C(e)[fm] = %.6f   相对差 = %.3e"
      % (lam / lP, lamC_e_fm, abs(lam / lP - lamC_e_fm) / lamC_e_fm))

print("\n--- 单位依赖检验：ℓ_P 用 fm 还是 m ---")
# 靶的式子 ω = sqrt(κ²+τ²)·c/ℓ_P；κ 单位是 fm⁻¹（表内），所以 ℓ_P 必须用 fm 才量纲通
lP_fm = D("1.616255e-20")     # fm
w_if_fm = D("2.5896051e-3") * C / lP_fm / D("1e-15")   # κ0(e) [fm^-1] * c[m/s] / lP[fm] -> 1/s
print("κ_0(e)=2.5896051e-3 fm⁻¹, ℓ_P=1.616255e-20 fm ⇒ ω = κ·c/ℓ_P = %.6e s⁻¹" % w_if_fm)
w_if_m = D("2.5896051e-3") * C / lP / D("1e-15")
print("若 ℓ_P 误用 m（1.616255e-35）        ⇒ ω = %.6e s⁻¹" % w_if_m)
print("⇒ 单位选择造成的漂移 = %.7f dex" % dex(w_if_m / w_if_fm))

print("\n" + "=" * 78)
print("【三】四力力程对拍（用靶自己的数值当锚）")
print("=" * 78)
LAM_W = HBARC / MW_MEV * D("1e-15")          # m
LAM_PI = HBARC / MPI0_MEV * D("1e-15")       # m
print("靶自给 λ_W  = %.6e m   (ħc/m_W)" % LAM_W)
print("靶自给 λ_π0 = %.6e m   (ħc/m_π0)" % LAM_PI)
print()
print("λ_ω = c/ω(L3369) = %.6e m" % lam)
for nm, L in (("弱", LAM_W), ("强(π⁰)", LAM_PI)):
    print("  %-8s λ_i/λ_ω = %.6e   = %.4f dex" % (nm, L / lam, dex(L / lam)))
print("  引力/电磁 靶自给 λ=∞ ⇒ 与 λ_ω 之比 = ∞")
print()
print("反解：要 λ=λ_W 需 ω = c/λ_W = %.7e s⁻¹" % (C / LAM_W))
print("      要 λ=λ_π0 需 ω = c/λ_π0 = %.7e s⁻¹" % (C / LAM_PI))

print("\n" + "=" * 78)
print("【四】八粒子表 λ×(ω/c) 互算（L3211-3219，表内残差列全写 0.0）")
print("=" * 78)
ROWS = [
    ("e-", "0.51099895", "386.1592678", "2.5896051e-3"),
    ("p", "938.27208816", "0.21030389", "4.7549098"),
    ("n", "939.5654205", "0.21001541", "4.7479947"),
    ("pi+-", "139.57039", "1.4138169", "0.31951116"),
    ("pi0", "134.9768", "1.4619326", "0.33041480"),
    ("W", "80377.0", "2.4550180e-3", "5.54905e-4"),
    ("Z", "91187.6", "2.1639647e-3", "4.89037e-4"),
    ("H", "125250.0", "1.5754564e-3", "3.56059e-4"),
]
bad = 0
for nm, m, l_, w in ROWS:
    L, W = D(l_), D(w)
    prod = L * W
    off = abs(prod - 1)
    tag = "OK" if off < D("1e-6") else "违规"
    if tag == "违规":
        bad += 1
    print("  %-6s λ=%-14s ω/c=%-14s λ·(ω/c)=%-16s 偏差=%.4e  %s"
          % (nm, l_, w, ("%.8g" % prod), off, tag))
print("  ⇒ 违规 %d / 8 行" % bad)
print()
print("交叉验证 λ 列（是否 = ħc/m）:")
for nm, m, l_, w in ROWS:
    L = D(l_)
    pred = HBARC / D(m)
    print("  %-6s λ表=%-14s ħc/m=%-14s 相对差=%.3e" % (nm, l_, ("%.8g" % pred), abs(L - pred) / pred))

print("\n" + "=" * 78)
print("【五】关键词词频（参数总账层用语）")
print("=" * 78)
for k in ("赋值", "拟合", "自由参数", "外部输入", "实验赋值", "循环定义", "补充公设",
          "待定", "内生", "外输", "无独立观测", "公设量", "判别性"):
    tot = sum(t.count(k) for t in TEXTS.values())
    per = "  ".join("%s:%d" % (nm[:6], t.count(k)) for nm, t in TEXTS.items() if t.count(k))
    print("  %-8s 合计 %5d   %s" % (k, tot, per))

print("\n" + "=" * 78)
print("【六】关键行抽查")
print("=" * 78)
t0 = TEXTS["T0_定稿全书"].splitlines()
for ln in (1755, 1353, 1784, 192, 2405, 3369, 3520, 307, 309, 313, 2180, 3226, 707, 1037):
    if ln <= len(t0):
        print("  L%-5d %s" % (ln, t0[ln - 1][:110]))
t2 = TEXTS["T2_修改攻破"].splitlines()
print("  T2 L965 %s" % (t2[964][:110] if len(t2) >= 965 else "(越界)"))
t3 = TEXTS["T3_V40"].splitlines()
print("  T3 L23  %s" % (t3[22][:110] if len(t3) >= 23 else "(越界)"))
