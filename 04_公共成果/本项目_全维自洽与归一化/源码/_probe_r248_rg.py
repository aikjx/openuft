# -*- coding: utf-8 -*-
r"""
r248 探针 2 · RG 跑动层：靶用「自己的」单圈公式能否得到「自己的」饱和值？
================================================================================
靶的等式清单（来料）：
 8.  QED单圈β函数
 9.  1/α(μ) = 1/α_obs − (2/3π)·ln(μ/μ_0)      ← 标准单圈，正是产生兰道极点的那条
 10. α(μ) → α_* = √3/2   (μ→μ_Planck)          ← 饱和断言

本探针问：把 9 号式代入 μ=μ_Planck，得到什么？与 10 号的 0.866 差多少？
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


def rt(p):
    try:
        with io.open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


ALL = "".join(rt(p) for p in TARGETS)
RAW = rt(TARGETS[0])
LINES = RAW.split("\n")


def sec(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------- 数值
sec("A · 靶自己的单圈公式在普朗克能标给出什么？")
ALPHA_OBS = 7.2973525693e-3
A_STAR = math.sqrt(3.0) / 2.0
M_E_MEV = 0.51099895000          # 电子质量 MeV
M_Z = 91.1876                    # GeV
M_PLANCK_GEV = 1.220890e19
M_PLANCK_MEV = M_PLANCK_GEV * 1.0e3

print("  α_obs        = %.10e  (1/α_obs = %.6f)" % (ALPHA_OBS, 1.0 / ALPHA_OBS))
print("  α_* = √3/2   = %.10f" % A_STAR)
print("  μ_0 = m_e c² = %.9f MeV； μ_Planck = %.6e MeV" % (M_E_MEV, M_PLANCK_MEV))


def alpha_at(mu, mu0=M_E_MEV, a0=ALPHA_OBS):
    v = 1.0 / a0 - (2.0 / (3.0 * math.pi)) * math.log(mu / mu0)
    return (1.0 / v) if v > 0 else float("inf")


a_pl = alpha_at(M_PLANCK_MEV)
ln_pl = math.log(M_PLANCK_MEV / M_E_MEV)
print("")
print("  ln(μ_Planck/μ_0)            = %.6f" % ln_pl)
print("  (2/3π)·ln                   = %.6f" % ((2.0 / (3.0 * math.pi)) * ln_pl))
print("  1/α(μ_Planck)               = %.6f" % (1.0 / a_pl))
print("  ⇒ α(μ_Planck) 【用靶自己的 9 号式】 = %.8e" % a_pl)
print("  靶 10 号式断言的饱和值        = %.8f" % A_STAR)
print("  ⇒ 差 %.4f 倍（靶公式值 / 靶断言值 = %.6f）" % (A_STAR / a_pl, a_pl / A_STAR))

print("")
print("  ★要让 α 真正达到 α_*=√3/2，需要：")
ln_need = (1.0 / ALPHA_OBS - 1.0 / A_STAR) * (3.0 * math.pi / 2.0)
print("     ln(μ/μ_0) = (1/α_obs − 1/α_*)·3π/2 = %.6f" % ln_need)
print("     log10(μ/μ_0) = %.4f  ⇒ μ/μ_0 = 10^%.4f" % (ln_need / math.log(10), ln_need / math.log(10)))
print("     即 μ ≈ 10^%.2f MeV" % (ln_need / math.log(10) + math.log10(M_E_MEV)))
print("     而 μ_Planck ≈ 10^%.2f MeV" % math.log10(M_PLANCK_MEV))
print("     ⇒ 饱和点比普朗克能标高 10^%.2f 倍" % (ln_need / math.log(10) + math.log10(M_E_MEV) - math.log10(M_PLANCK_MEV)))
print("")
print("  ★兰道极点位置（1/α=0）：")
ln_lp = (1.0 / ALPHA_OBS) * (3.0 * math.pi / 2.0)
print("     ln(μ_LP/μ_0) = (1/α_obs)·3π/2 = %.6f  ⇒ log10 = %.4f" % (ln_lp, ln_lp / math.log(10)))
print("     靶文中出现的 645.77 是否为该值？%.6f" % ln_lp)

# ---------------------------------------------------------------- 大统一
sec("B · 大统一固定点 0.866 vs 标准模型单圈跑动值")
A_S_MZ = 0.1180
ALPHA_EM_MZ = 1.0 / 127.95
SIN2 = 0.23121
a1_mz = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2)
a2_mz = ALPHA_EM_MZ / SIN2
a3_mz = A_S_MZ
B = (41.0 / 10.0, -19.0 / 6.0, -7.0)
print("  M_Z = %.4f GeV；α_em(M_Z)=1/127.95；sin²θ=%.5f；α_s=%.4f" % (M_Z, SIN2, A_S_MZ))
print("  GUT 归一：α_1(M_Z)=%.6f  α_2(M_Z)=%.6f  α_3(M_Z)=%.6f" % (a1_mz, a2_mz, a3_mz))
print("")
print("  %-12s %-12s %-12s %-12s" % ("μ [GeV]", "α_1", "α_2", "α_3"))
for mu in (1.0e10, 1.0e13, 1.0e16, 1.0e19):
    row = []
    for a0, b in ((a1_mz, B[0]), (a2_mz, B[1]), (a3_mz, B[2])):
        v = 1.0 / a0 - (b / (2.0 * math.pi)) * math.log(mu / M_Z)
        row.append(1.0 / v if v > 0 else float("inf"))
    print("  %-12s %-12.6f %-12.6f %-12.6f" % ("%.0e" % mu, row[0], row[1], row[2]))
a_uni = [1.0 / (1.0 / a0 - (b / (2.0 * math.pi)) * math.log(1.0e16 / M_Z))
         for a0, b in ((a1_mz, B[0]), (a2_mz, B[1]), (a3_mz, B[2]))]
print("")
print("  在 10^16 GeV 处三值 %.5f / %.5f / %.5f" % tuple(a_uni))
print("  靶断言三值都 = α_* = %.6f" % A_STAR)
print("  ⇒ 比值 %.2f×  /  %.2f×  /  %.2f×" % (A_STAR / a_uni[0], A_STAR / a_uni[1], A_STAR / a_uni[2]))

# ---------------------------------------------------------------- 屏蔽因子
sec("C · P_0 屏蔽因子：是推导还是拟合？")
p0 = A_STAR / ALPHA_OBS - 1.0
print("  α_obs = α_0/(1+P_0) ⇒ P_0 = α_0/α_obs − 1 = %.6f" % p0)
for pat in [r"\\mathcal\{P\}_0", r"P_0", r"屏蔽因子", r"极化屏蔽", r"极化率"]:
    print("   %-20s ALL %d" % (pat, len(re.findall(pat, ALL))))
print("")
for m in list(re.finditer(r"\\mathcal\{P\}_0", ALL))[:6]:
    a, b = max(0, m.start() - 110), min(len(ALL), m.end() + 130)
    print("   ...%s..." % ALL[a:b].replace("\n", "\\n"))

# ---------------------------------------------------------------- 修正 β
sec("D · 是否存在「修正后的 β 函数」（而不只是渐近断言）？")
for pat in [r"修正后.{0,20}β", r"β\s*\(\s*\\alpha\s*\)\s*=", r"\\beta\\left", r"饱和.{0,20}β",
            r"非微扰", r"屏蔽.{0,15}β"]:
    ms = list(re.finditer(pat, ALL))
    print("   %-24s 命中 %d" % (pat, len(ms)))
    for m in ms[:3]:
        a, b = max(0, m.start() - 70), min(len(ALL), m.end() + 110)
        print("       ...%s..." % ALL[a:b].replace("\n", "\\n"))

# ---------------------------------------------------------------- α=√3/2 定义恒等式
sec("E · α = l_h/√(r₀²+l_h²) 是不是定义恒等式？")
HBAR = 1.054571817e-34
C = 299792458.0
M_E = 9.1093837015e-31
r0 = HBAR / (2.0 * M_E * C)
lh = (math.sqrt(3.0) / 2.0) * HBAR / (M_E * C)
print("  r₀ = ℏ/(2 m_e c)          = %.8e m" % r0)
print("  l_h = (√3/2)·ℏ/(m_e c)    = %.8e m   ← √3/2 在这里【被塞进去】" % lh)
print("  √(r₀²+l_h²)                = %.8e m   （= ℏ/(m_e c)，约化康普顿波长）" % math.sqrt(r0 ** 2 + lh ** 2))
print("  α = l_h/√(r₀²+l_h²)        = %.12f" % (lh / math.sqrt(r0 ** 2 + lh ** 2)))
print("  √3/2                       = %.12f" % A_STAR)
print("  残差                       = %.3e" % abs(lh / math.sqrt(r0 ** 2 + lh ** 2) - A_STAR))
print("")
print("  代数：√(r₀²+l_h²) = (ℏ/(m_ec))·√(1/4 + 3/4) = ℏ/(m_ec)")
print("        α = (√3/2)(ℏ/(m_ec)) / (ℏ/(m_ec)) = √3/2   ← 恒等，与 m_e、c、ℏ **全部无关**")
print("  ⇒ √3/2 是 l_h 定义里的输入，不是推导结果（定义恒等式刀）。")

print("\nDONE")
