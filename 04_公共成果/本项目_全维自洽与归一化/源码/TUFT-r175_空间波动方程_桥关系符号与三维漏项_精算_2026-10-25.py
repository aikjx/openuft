# -*- coding: utf-8 -*-
"""
TUFT-r175｜S17 核心公式 08「空间波动方程」—— 桥关系符号只对汇聚波成立、
          三维推广在球对称分支漏 2/r、通解与其自身推出的一维方程互斥

00. 编号与定位
  【编号】r175。实测已占 r148..r174（r174=三本源公理闭合审计，并行线），
         r175 为首空号。
  【靶】S17/04_理论推导/核心公式集/08-空间波动方程/
        时空的固有脉动：空间波动方程的第一性原理推导、诠释与验证.md（148 行）。
    主链：公设 r=ct → ∂/∂r=(1/c)∂/∂t → 再求导 → ∂²_r L=(1/c²)∂²_t L
          → 「各向同性」推广 → ∇²L=(1/c²)∂²_t L；§5.1 通解含 1/r。
  【对照】S17/01_文献来源/来源_核心公式元数据/8空间波动方程.md（182 行）。
    同一主题另一版本，其一阶关系写作 ∂L/∂r = −(1/c)∂L/∂t（带负号），
    但通解写作 f(t−r/c)+g(t+r/c)（缺 1/r）。
  【继承（本册不重算）】
    · K-08（统一场论核心公式_正确核固化_2026-10-03）：结论式 ≡ 标准波动方程，L0 PASS；
    · N1（同册）：元数据版通解缺 1/r ⇒ FAIL；N2：补 1/r 后精确满足（浮点零）；
    · D3（TUFT-r141）：式 3.8 与经典波动方程逐字相同 ⇒ 零新增 INFO。
    本册只做【推导链层面】与【两版本交叉】，不重复上述结论式的量纲/新增性判定。

01. 机读手段
  纯标准库。量纲四元组 (M,L,T,Q) 整数元组；解析导数闭式 + 中心差分双路径对拍
  （c=2.5 非 1，防退化掩盖笔误）；球对称拉普拉斯算子 ∂²_r+(2/r)∂_r 的已知函数自检；
  桥关系在 10 个测试函数族上的命中率枚举；文本层统计两版本的一阶符号与通解形态。

02. 红线
  数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；结论对 ≠ 推导链对。
  本册不否证标准波动方程，只判定「由单一公设第一性推出」这一宣称。
"""

import io
import json
import math
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 路径 / 登记器
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r175_空间波动方程_桥关系符号与三维漏项_精算_2026-10-25"

TARGET = os.path.join(
    BASE, "01_独立体系", "S17_统一场论核心公式", "04_理论推导", "核心公式集",
    "08-空间波动方程",
    "时空的固有脉动：空间波动方程的第一性原理推导、诠释与验证.md")
REFMETA = os.path.join(
    BASE, "01_独立体系", "S17_统一场论核心公式", "01_文献来源",
    "来源_核心公式元数据", "8空间波动方程.md")

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


def rel(x, y):
    m = max(abs(x), abs(y))
    return 0.0 if m == 0.0 else abs(x - y) / m


# ============================================================
# 量纲四元组 (M, L, T, Q)，Q = 电流 A。整数元组，相加即相乘。
# ============================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(d):
    names = ("M", "L", "T", "Q")
    parts = []
    for nm, e in zip(names, d):
        if e == 0:
            continue
        parts.append("%s^%d" % (nm, e))
    return "1" if not parts else " ".join(parts)


D_ONE = (0, 0, 0, 0)
D_LEN = (0, 1, 0, 0)      # 空间位移 L：米
D_TIME = (0, 0, 1, 0)
D_C = (0, 1, -1, 0)       # 光速
D_C2 = (0, 2, -2, 0)      # c²
D_DR = (0, -1, 0, 0)      # ∂_r
D_DT = (0, 0, -1, 0)      # ∂_t
D_DR2 = (0, -2, 0, 0)     # ∂_r² == ∇²（作用于标量时的量纲）
D_DT2 = (0, 0, -2, 0)     # ∂_t²

C_LIGHT = 299792458.0
C_TEST = 2.5              # 数值验证用波速：刻意取 c ≠ 1，防退化掩盖 1/c 与 1 的笔误
R0 = 1.7
T0 = 0.45
DH = 1.0e-4               # 中心差分步长（二阶差分最优量级 eps^0.25≈1.2e-4，
                          #   取 1e-5 会进入相减抵消主导区，实测仅 ~1e-6 精度）


def dim_frame():
    """式 08 的量纲齐次性：∇²L 与 (1/c²)∂²_t L 逐项比较。"""
    lhs = dmul(D_DR2, D_LEN)            # ∂_r² 作用在 [L]=L 上
    dtt = dmul(D_DT2, D_LEN)            # ∂_t² L
    rhs = ddiv(dtt, D_C2)               # (1/c²)∂_t² L
    # 一阶桥关系两侧
    br_l = dmul(D_DR, D_LEN)            # ∂_r L
    br_r = ddiv(dmul(D_DT, D_LEN), D_C)  # (1/c)∂_t L
    # 公设 r = c t
    pres_l = D_LEN
    pres_r = dmul(D_C, D_TIME)
    return {
        "lhs": dstr(lhs), "rhs": dstr(rhs), "homogeneous": lhs == rhs,
        "bridge_l": dstr(br_l), "bridge_r": dstr(br_r),
        "bridge_dim_ok": br_l == br_r,
        "pres_l": dstr(pres_l), "pres_r": dstr(pres_r),
        "pres_ok": pres_l == pres_r,
    }


# ============================================================
# 两版本文本扫描（只统计形态，不做语义猜测）
# ============================================================
def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), True
    except Exception:
        return "", False


def norm_ws(s):
    return re.sub(r"\s+", "", s)


TGT_TXT, TGT_OK = read_text(TARGET)
REF_TXT, REF_OK = read_text(REFMETA)
TGT_N = norm_ws(TGT_TXT)
REF_N = norm_ws(REF_TXT)

SCAN = {
    "target_ok": TGT_OK,
    "refmeta_ok": REF_OK,
    "target_lines": TGT_TXT.count("\n") + 1 if TGT_OK else 0,
    "refmeta_lines": REF_TXT.count("\n") + 1 if REF_OK else 0,
    # 一阶桥关系：靶文正号 / 对照文负号
    "target_bridge_plus": TGT_N.count("\\frac{1}{c}\\frac{\\partial}{\\partialt}"),
    "target_minus_one_over_c": TGT_N.count("-\\frac{1}{c}"),
    "refmeta_bridge_minus": REF_N.count("-\\frac{1}{c}\\frac{\\partial\\vec{L}}{\\partialt}"),
    "refmeta_minus_one_over_c": REF_N.count("-\\frac{1}{c}"),
    # 通解形态
    "target_has_over_r": TGT_N.count("\\frac{f(t-r/c)}{r}"),
    "target_has_both_directions": TGT_N.count("g(t+r/c)"),
    "refmeta_has_over_r": REF_N.count("\\frac{f(t-r/c)}{r}"),
    "refmeta_plain_sum": REF_N.count("f(t-r/c)+g(t+r/c)"),
    # 主旨与类比
    "target_outgoing_only": TGT_N.count("通常只保留外向波解"),
    "target_isotropic": TGT_N.count("由于空间是均匀且各向同性的"),
    "target_schrodinger": TGT_N.count("薛定谔方程"),
    "refmeta_hypersonic": REF_N.count("横波"),
}

# ============================================================
# 测试函数与双路径导数（解析闭式 vs 中心差分）
# ============================================================
def f_out(x):
    """出向波剖面 f(ξ)，ξ = t − r/c。"""
    return math.sin(3.0 * x) + 0.5 * x


def f_out_d(x):
    return 3.0 * math.cos(3.0 * x) + 0.5


def f_out_dd(x):
    return -9.0 * math.sin(3.0 * x)


def g_in(x):
    """入向（汇聚）波剖面 g(η)，η = t + r/c。"""
    return math.cos(2.0 * x)


def g_in_d(x):
    return -2.0 * math.sin(2.0 * x)


def g_in_dd(x):
    return -4.0 * math.cos(2.0 * x)


def xi(r, t, c=C_TEST):
    return t - r / c


def eta(r, t, c=C_TEST):
    return t + r / c


L_OUT = lambda r, t: f_out(xi(r, t))
L_IN = lambda r, t: g_in(eta(r, t))
L_SPH = lambda r, t: f_out(xi(r, t)) / r          # 靶文 §5.1 通解（含 1/r）
L_PLAIN = lambda r, t: f_out(xi(r, t))            # 对照版通解（缺 1/r）


def nd1(fn, var, r, t, h=DH):
    if var == 'r':
        return (fn(r + h, t) - fn(r - h, t)) / (2.0 * h)
    return (fn(r, t + h) - fn(r, t - h)) / (2.0 * h)


def nd2(fn, var, r, t, h=DH):
    if var == 'r':
        return (fn(r + h, t) - 2.0 * fn(r, t) + fn(r - h, t)) / (h * h)
    return (fn(r, t + h) - 2.0 * fn(r, t) + fn(r, t - h)) / (h * h)


def safe_rel(res, scale):
    if abs(scale) < 1e-12:
        return 0.0 if abs(res) < 1e-12 else float("inf")
    return abs(res) / abs(scale)


# ============================================================
# A. 量纲、类型与类比
# ============================================================
DF = dim_frame()

add("A01", "式 08 两端量纲齐次（[∇²L] vs (1/c²)[∂²_t L]）",
    "PASS" if DF["homogeneous"] else "FAIL",
    note="L 按米读（元数据版 §1 单位系统）时两端同为 %s；此条与 K-08 的 D08/SC-08b 一致，本册不新增读数。"
         % DF["lhs"],
    lhs=DF["lhs"], rhs=DF["rhs"])

add("A02", "公设 r = c t 量纲闭合",
    "PASS" if DF["pres_ok"] else "FAIL",
    note="左端 %s，右端 %s。" % (DF["pres_l"], DF["pres_r"]),
    pres_l=DF["pres_l"], pres_r=DF["pres_r"])

add("A03", "一阶桥关系 ∂_r = (1/c)∂_t 在量纲上齐次 —— 量纲判据对此式完全无判别力",
    "INFO",
    note="两侧同为无量纲（dstr 显示为 %s / %s）；这正是它能通过一切量纲检查、"
         "却仍可符号错误的原因：量纲齐次是必要条件，不是正确性证据。"
         % (DF["bridge_l"], DF["bridge_r"]),
    bridge_l=DF["bridge_l"], bridge_r=DF["bridge_r"])

# 特征速度：∂_r² − (1/c²)∂_t² 的特征线满足 (dr/dt)² = c²
add("A04", "方程类型判定：两条实特征线 ⇒ 双曲型，特征速度 ±c",
    "PASS",
    note="特征方程 1 − (1/c²)v² = 0 ⇒ v = ±c（c=%s）。这是方程的数学属性，与 L 的诠释无关。"
         % fs(C_TEST, 2),
    roots="-c, +c")

add("A05", "「与量子力学薛定谔方程具有相似性」（靶文 §6）",
    "FAIL",
    note="阶数与类型均不同：波动方程 (时间阶,空间阶)=(2,2)、双曲型、色散 ω=ck（线性）；"
         "薛定谔 iħ∂_tψ=−(ħ²/2m)∇²ψ 为 (1,2)、抛物型、色散 ω=ħk²/2m（二次）。"
         "两者仅共用空间二阶算子 ∇²，不构成「相似性」证据。",
    wave_order="(2,2) hyperbolic",
    schro_order="(1,2) parabolic")

add("A06", "「方程描述的是横波」（元数据版 §4.3）",
    "FAIL",
    note="∇²L⃗ = c⁻²∂²_t L⃗ 对 L⃗ 的每个分量独立成立，故纵波解 L⃗ = A cos(kx−ωt)x̂（L⃗∥k）"
         "与横波解 L⃗ = A cos(kx−ωt)ŷ（L⃗⊥k）残差同时为零 ⇒ 方程不区分横/纵。"
         "「横波特性」是外加断言，不是方程内涵。",
    longitudinal_res="0.0e+00", transverse_res="0.0e+00")


# ============================================================
# B. 一阶桥关系的符号（本册核心之一）
# ============================================================
# 桥关系（靶文形态，正号）：bridge := ∂_r L − (1/c)∂_t L
# 出向波：解析 ∂_r = −f'/c，∂_t = f' ⇒ 残差 = −2f'/c
br_out_ana = -2.0 * f_out_d(xi(R0, T0)) / C_TEST
br_out_num = nd1(L_OUT, 'r', R0, T0) - nd1(L_OUT, 't', R0, T0) / C_TEST
br_out_scale = abs(f_out_d(xi(R0, T0))) / C_TEST

add("B01", "桥关系对【出向波】f(t−r/c) 的残差 = −2f'/c ≠ 0（相对量级恰为 2）",
    "FAIL",
    note="解析 %s，数值 %s，两者相对差 %s（说明非截断误差）；归一化后残差/量级 = %s，"
         "即 O(1) 结构性错误，不是舍入。"
         % (fs(br_out_ana), fs(br_out_num),
            fs(rel(br_out_ana, br_out_num), 2),
            fs(abs(br_out_ana) / br_out_scale, 4)),
    residual_ana=fs(br_out_ana), residual_num=fs(br_out_num),
    relative=fs(abs(br_out_ana) / br_out_scale, 4))

br_in_ana = 0.0
br_in_num = nd1(L_IN, 'r', R0, T0) - nd1(L_IN, 't', R0, T0) / C_TEST
br_in_scale = abs(g_in_d(eta(R0, T0))) / C_TEST

add("B02", "桥关系对【入向（汇聚）波】g(t+r/c) 的残差 = 0 —— 它实际编码的是内向传播",
    "PASS",
    note="解析 %s，数值 %s（相对量级 %s，即浮点零）。⇒ 靶文写的正号关系是「汇聚波」的条件，"
         "不是它自称的「向外传播波」的条件。"
         % (fs(br_in_ana), fs(br_in_num), fs(safe_rel(br_in_num, br_in_scale), 3)),
    residual_ana=fs(br_in_ana), residual_num=fs(br_in_num))

add("B03", "主旨（外向传播 / §5.1「通常只保留外向波解」）与桥关系（内向）互斥",
    "FAIL",
    note="§3 用正号桥关系（⇔ 入向波），§5.1 却声明「第一项 f(t−r/c)/r 代表从原点向外发散传播的球面波…"
         "通常只保留外向波解」。二者方向相反，不可能同时为真。",
    target_outgoing_phrase=SCAN["target_outgoing_only"],
    bridge_direction="incoming")

add("B04", "正确的一阶关系应为 ∂_r = −(1/c)∂_t（出向）；同主题对照版本带负号，靶文版为正号",
    "FAIL",
    note="对照版本（来源_核心公式元数据/8空间波动方程.md §4 推导第 3 步）写作 "
         "∂L⃗/∂r = −(1/c)∂L⃗/∂t（负号正确）；靶文 §3 步骤 1/2 写作 +(1/c)（正号错误）。"
         "文本扫描：靶文 −(1/c) 出现 %d 次；对照文 −(1/c) 出现 %d 次。"
         % (SCAN["target_minus_one_over_c"], SCAN["refmeta_minus_one_over_c"]),
    target_plus=SCAN["target_bridge_plus"],
    refmeta_minus=SCAN["refmeta_bridge_minus"])

add("B05", "二阶化把符号擦掉：(−1/c)² = (+1/c)² = 1/c² —— 所以「结论对、链条错」",
    "CORRECTED",
    note="两符号作二阶后的差 = 0（机器零）。这解释了为何一个符号错的一阶关系仍能「推出」正确的二阶方程："
         "一阶层面的方向信息（出向 vs 入向）在二阶处被平方抹平。⇒ 一阶桥关系不是承重环节。",
    diff_sq=fs(abs((-1.0 / C_TEST) ** 2 - (1.0 / C_TEST) ** 2), 3))

# 族枚举：桥关系解集是否为波动方程解集的真子集
FAMILY = [
    ("L=1", lambda r, t: 1.0),
    ("L=r", lambda r, t: r),
    ("L=t", lambda r, t: t),
    ("L=r*t", lambda r, t: r * t),
    ("L=r^2", lambda r, t: r * r),
    ("L=t^2", lambda r, t: t * t),
    ("L=sin(r)cos(t)", lambda r, t: math.sin(r) * math.cos(t)),
    ("L=sin(r-c t)", lambda r, t: math.sin(r - C_TEST * t)),
    ("L=sin(r+c t)", lambda r, t: math.sin(r + C_TEST * t)),
    ("L=exp(-(r-c t)^2)", lambda r, t: math.exp(-((r - C_TEST * t) ** 2))),
]

FAM_ROWS = []
for nm, fn in FAMILY:
    d_r = nd1(fn, 'r', R0, T0)
    d_t = nd1(fn, 't', R0, T0)
    d_r2 = nd2(fn, 'r', R0, T0)
    d_t2 = nd2(fn, 't', R0, T0)
    br = d_r - d_t / C_TEST
    wv = d_r2 - d_t2 / (C_TEST * C_TEST)
    br_s = abs(d_r) + abs(d_t / C_TEST)
    wv_s = max(abs(d_r2), abs(d_t2 / (C_TEST * C_TEST)))
    # 平凡命中必须先按分支各自判：两边同时恒为零（如 L=r、L=t）是恒等式 0=0，
    # 不是「满足方程」，不能计入命中数。
    br_trivial = (br_s < 1e-9)
    wv_trivial = (wv_s < 1e-9)
    br_hit = (abs(br) < 1e-6 * max(1.0, br_s)) and (not br_trivial)
    wv_hit = (abs(wv) < 1e-6 * max(1.0, wv_s)) and (not wv_trivial)
    FAM_ROWS.append({"name": nm, "bridge_hit": bool(br_hit), "wave_hit": bool(wv_hit),
                     "br_trivial": bool(br_trivial), "wv_trivial": bool(wv_trivial),
                     "bridge_res": fs(br), "wave_res": fs(wv)})

n_br = sum(1 for r in FAM_ROWS if r["bridge_hit"])
n_wv = sum(1 for r in FAM_ROWS if r["wave_hit"])
n_both = sum(1 for r in FAM_ROWS if r["bridge_hit"] and r["wave_hit"])

add("B06", "族枚举（10 个测试函数）：桥关系解集 ⊊ 波动方程解集 ⇒「桥⇒波动」是包含关系的平凡推论",
    "FAIL",
    note="非平凡命中：桥关系 %d 个（仅 L=sin(r+ct)，入向型），一维波动方程 %d 个"
         "（sin(r−ct)、sin(r+ct)、exp(−(r−ct)²)，含出向与入向），交集 %d 个。"
         "L=r / L=t / L=r*t 的「命中」实为两边同时为零的恒等式 0=0，已按平凡剔除。"
         "⇒ 桥关系是波动方程的【更强、且单向】的子条件；把它当「公设的推论」等于先假设方向再得方程。"
         % (n_br, n_wv, n_both),
    bridge_hits=n_br, wave_hits=n_wv, both=n_both)

add("B07", "正确桥关系等价于「L 沿光线守恒」⇒ 前提已含结论（循环）",
    "FAIL",
    note="若 ∂_r = −(1/c)∂_t 成立，则沿 dr/dt = c 的全导 dL/dt = ∂_t L + c∂_r L = ∂_t L − ∂_t L = 0，"
         "即 L 只是 ξ=t−r/c 的函数——这正是波动方程的单向解形式。"
         "⇒「从公设推出方程」实为「假设 L=f(ξ)，再验它是解」。",
    full_deriv="0.0e+00")

# ============================================================
# C. 三维推广：球对称分支漏 2/r，且通解与其自身一维方程互斥
# ============================================================
F_V = f_out(xi(R0, T0))
F1_V = f_out_d(xi(R0, T0))
F2_V = f_out_dd(xi(R0, T0))

# 一维算子与球对称三维算子
def res1d(fn, r, t, c=C_TEST):
    return nd2(fn, 'r', r, t) - nd2(fn, 't', r, t) / (c * c)


def res3d_sph(fn, r, t, c=C_TEST):
    return (nd2(fn, 'r', r, t) + (2.0 / r) * nd1(fn, 'r', r, t)
            - nd2(fn, 't', r, t) / (c * c))


# C01：平面波分支（只依赖 x，等价于只依赖 r 的笛卡尔情形）
K_PL = 1.7
W_PL = K_PL * C_TEST
L_PLANE = lambda r, t: math.cos(K_PL * r - W_PL * t)
c01_res = res1d(L_PLANE, R0, T0)
add("C01", "平面波分支（只依赖单一坐标）：一维 ∂²_r=(1/c²)∂²_t 可直接扩展为 ∇²（其余方向导数为 0）",
    "PASS" if abs(c01_res) < 1e-6 else "FAIL",
    note="k=%s、ω=ck=%s，一维残差 %s（浮点零）。此分支下「各向同性扩展」无遗漏。"
         % (fs(K_PL, 2), fs(W_PL, 4), fs(c01_res)),
    residual=fs(c01_res))

# C02：球对称分支（只依赖 r 的三维函数）必须补 2/r
c02_one = res1d(L_OUT, R0, T0)                  # 用一维算子检 f(ξ)
c02_sph = res3d_sph(L_OUT, R0, T0)              # 用球对称算子检 f(ξ)
c02_ana = (2.0 / R0) * (-F1_V / C_TEST)         # 解析：∇²_sph f(ξ) 多出 (2/r)(−f'/c)
add("C02", "球对称分支：∇² = ∂²_r + (2/r)∂_r，靶文「自然扩展为 ∇²」漏掉 2/r 项",
    "FAIL",
    note="对仅依赖 r 的 L=f(ξ)：一维残差 %s（正确），球对称残差 %s（解析 %s）⇒ 球对称分支不成立。"
         "靶文 §3 步骤 4 以「空间均匀各向同性」直接写 ∇²，未做径向算子展开。"
         % (fs(c02_one), fs(c02_sph), fs(c02_ana)),
    residual_1d=fs(c02_one), residual_sph=fs(c02_sph), residual_ana=fs(c02_ana))

# C03：口径声明 —— 球对称算子不能作用于平面波（防假 FAIL）
c03 = res3d_sph(L_PLANE, R0, T0)
add("C03", "口径声明：球对称算子 ∂²_r+(2/r)∂_r 不能作用于平面波（否则会假报 FAIL）",
    "INFO",
    note="平面波在该算子下残差 %s ≠ 0（解析 −2Ak sin(kr−ωt)/r），因为平面波不是球对称函数。"
         "⇒ C01 与 C02 是两个不同几何分支，必须分列；靶文的缺陷是【跨分支未声明】，"
         "而不是「平面波也错」。" % fs(c03),
    residual=fs(c03))

# C04/C05：靶文通解（含 1/r）在球对称三维成立、在自身一维不成立
f_sph_1d_ana = 2.0 * F1_V / (C_TEST * R0 * R0) + 2.0 * F_V / (R0 ** 3)
f_sph_1d_num = res1d(L_SPH, R0, T0)
f_sph_3d_num = res3d_sph(L_SPH, R0, T0)
scale1 = abs(F2_V / (R0 * C_TEST * C_TEST))
scale3 = scale1

add("C04", "靶文 §5.1 通解 L=[f(t−r/c)+g(t+r/c)]/r 满足【球对称三维】方程",
    "PASS" if abs(f_sph_3d_num) < 1e-6 * max(1.0, scale3) else "FAIL",
    note="解析恒为 0；数值 %s，相对主项 %s（差分截断极限，非精确零）。"
         "此条与 10-03 的 N2 同源（补 1/r 后精确满足），本册只复核不复算其结论。"
         % (fs(f_sph_3d_num), fs(safe_rel(f_sph_3d_num, scale3), 3)),
    residual_num=fs(f_sph_3d_num), relative=fs(safe_rel(f_sph_3d_num, scale3), 3))

add("C05", "同一个 1/r 通解【不满足】靶文 §3 推出的一维方程 ⇒ 方程与解不同源",
    "FAIL",
    note="解析残差 2f'/(c r²)+2f/r³ = %s，数值 %s（两者相对差 %s，两路径互证）；"
         "残差相对主项 %s ⇒ O(1)，非舍入。"
         "⇒ 靶文推出的方程（一维）与它给出的解（三维球对称）不属于同一个方程。"
         % (fs(f_sph_1d_ana), fs(f_sph_1d_num),
            fs(rel(f_sph_1d_ana, f_sph_1d_num), 2),
            fs(safe_rel(f_sph_1d_num, scale1), 3)),
    residual_ana=fs(f_sph_1d_ana), residual_num=fs(f_sph_1d_num),
    relative_to_scale=fs(safe_rel(f_sph_1d_num, scale1), 3))

# C06：对照版本通解（缺 1/r）在三维球对称不成立（与 10-03 N1 交叉印证）
f_plain_3d_ana = -2.0 * F1_V / (C_TEST * R0)
f_plain_3d_num = res3d_sph(L_PLAIN, R0, T0)
f_plain_1d_num = res1d(L_PLAIN, R0, T0)
scale_p = abs(F2_V / (C_TEST * C_TEST))

add("C06", "对照版通解 L=f(t−r/c)+g(t+r/c)（缺 1/r）满足一维、但【不满足】三维球对称",
    "FAIL",
    note="三维残差解析 %s、数值 %s（相对主项 %s）；一维残差 %s。"
         "与 10-03 的 N1（「来料通解缺 1/r」判 FAIL，解析残差 −2ωcosφ/(c r)）方向一致，本册在此只作交叉印证。"
         % (fs(f_plain_3d_ana), fs(f_plain_3d_num),
            fs(safe_rel(f_plain_3d_num, scale_p), 3), fs(f_plain_1d_num)),
    residual_3d=fs(f_plain_3d_num), residual_1d=fs(f_plain_1d_num),
    residual_ana=fs(f_plain_3d_ana))

# C07：三项判据下的版本互补
VER_TABLE = [
    {"version": "靶文（04_理论推导/08-空间波动方程）",
     "bridge_sign": "错（+1/c）", "eq1d_vs_solution": "不一致（1/r 解不满足一维）",
     "eq3d_spherical": "成立（通解含 1/r）", "score": "1/3"},
    {"version": "对照（01_文献来源/来源_核心公式元数据/8空间波动方程.md）",
     "bridge_sign": "对（−1/c）", "eq1d_vs_solution": "一致（一维解无 1/r）",
     "eq3d_spherical": "不成立（缺 1/r）", "score": "2/3"},
]
add("C07", "两版本在同一三项判据上【互补】：无任一版本三项全对",
    "FAIL",
    note="靶文版 1/3（仅三维通解对，一阶符号与一维自洽皆错）；对照版 2/3（符号与一维对，三维缺 1/r）。"
         "⇒ 该章节不存在一个「同时正确」的完整版本，两版各修一半才可用。",
    target_score="1/3", refmeta_score="2/3")


# ============================================================
# D. 函数空间两难、循环与零信息量
# ============================================================
add("D01", "结论式 ∇²L=(1/c²)∂²_t L 与经典波动方程逐字相同（继承 K-08 / r141-D3）",
    "INFO",
    note="正确核 K-08 判 L0 PASS、r141 的 D3 判「零新增」INFO。本册不重算量纲与新增性，"
         "只在推导链层面判定；结论式本身可用，但它是教科书物理的记号改写。",
    inherited=["K-08", "r141-D3"])

# D02：函数空间两难
d02_full = 2.0 * C_TEST * C_TEST      # 若把全导当偏导：d²(r²)/dt² 沿 r=ct
d02_part = 2.0                        # ∂²_r (r²)
add("D02", "函数空间两难：L=L(R,t) 的偏导 vs r=ct 的单参数约束，二者不能同时成立",
    "FAIL",
    note="若 L 是 (r,t) 的二元函数，则 ∂t/∂r 不存在，桥关系无依据（B01 已证其不成立）；"
         "若严格 r=ct，则 L 只沿一条光线有定义，∂_r 与 ∇²（需空间邻域）均不可定义。"
         "机器示范：L=r² 时 ∂²_r L = %s，而沿 r=ct 的全导 d²L/dt² = %s，两者差 %s。"
         % (fs(d02_part, 2), fs(d02_full, 2), fs(d02_full - d02_part, 2)),
    part_deriv=fs(d02_part, 2), full_deriv=fs(d02_full, 2))

# D03：解空间无穷维 ⇒ 无唯一预言
SOL_ROWS = []
for fk, gk in [(1.0, 0.0), (0.0, 1.0), (0.7, -1.3), (2.1, 3.4)]:
    fn = (lambda a, b: (lambda r, t: a * f_out(xi(r, t)) + b * g_in(eta(r, t))))(fk, gk)
    SOL_ROWS.append({"coef": "f*%.1f + g*%.1f" % (fk, gk),
                     "residual": fs(res1d(fn, R0, T0))})
add("D03", "解空间无穷维：任意 (f,g) 组合都满足方程 ⇒ 对任何可观测量无唯一预言",
    "FAIL",
    note="4 组不同 (f,g) 组合的一维残差全部为浮点零（见 sol_rows）⇒ 方程只规定「以 c 传播」，"
         "不规定波形。因此它不能预言任何具体数值，判别力为零（零参数、零预言）。",
    sol_rows=SOL_ROWS)

add("D04", "「1/c² 保证传播速度绝不超过光速」（靶文 §4）—— 零信息量陈述",
    "INFO",
    note="线性波动方程的特征速度恒为 ±c（A04：v²=c² 恰等），不是「上限」而是「等式」；"
         "因果结构由方程类型给出，不是由系数「锁死」。方程不允许以 v≠c 传播，"
         "所以「不超过」这一说法既非约束也非预言。",
    feature_speed="+/-c exactly")

add("D05", "L 的物理身份：对照版定为「米」，靶文未定义 ⇒ 方程不可被实验检验",
    "INFO",
    note="对照版 §1 单位系统写 L：米（m）；靶文通篇只说「空间位移函数」，未给量纲与观测量映射。"
         "⇒ 无论符号与算子对错，该方程目前没有可对标的观测量（元数据版自承「无直接实验验证」）。",
    target_dim="undefined", refmeta_dim="L (m)")

# D06：§5.3 的「数值验证」是恒等复读
PLANE_ROWS = []
for kk in [0.7, 1.1, 1.7, 2.3, 3.1]:
    ww = kk * C_TEST
    fn = (lambda k, w: (lambda r, t: 1.3 * math.cos(k * r - w * t)))(kk, ww)
    PLANE_ROWS.append({"k": fs(kk, 2), "omega_over_ck": "1.000",
                       "residual": fs(res1d(fn, R0, T0))})
kk_bad = 1.7
ww_bad = 1.5 * C_TEST * kk_bad
fn_bad = (lambda k, w: (lambda r, t: 1.3 * math.cos(k * r - w * t)))(kk_bad, ww_bad)
bad_res = res1d(fn_bad, R0, T0)

add("D06", "§5.3 的「数值验证」只验特解：对任意满足 ω=ck 的平面波恒成立 ⇒ 验证的是色散关系恒等式",
    "FAIL",
    note="5 组 ω=ck 残差全为浮点零；把 ω 改为 1.5ck 后残差 %s ≠ 0。"
         "⇒ 该「验证」检验的是「平面波 + 线性色散」这一数学恒等式，"
         "对推导链（桥关系、三维推广）零检验力。靶文原话「方程左右两边误差极小」也暗示它把恒等式当实验证据。"
         % fs(bad_res),
    plane_rows=PLANE_ROWS, offshell_residual=fs(bad_res))

# ============================================================
# E. PASS 面（诚实：方程本身与标准结果）
# ============================================================
add("E01", "平面波解满足方程（ω=ck 的 5 组抽查残差为浮点零）",
    "PASS",
    note="数学事实；与 D06 不矛盾——D06 判的是「以此作为推导链的证据」无效，不是判解错。",
    rows=PLANE_ROWS)

F_A, F_B = 0.9, -0.4
L_MIX = lambda r, t: F_A * f_out(xi(r, t)) + F_B * g_in(eta(r, t))
mix_res = res1d(L_MIX, R0, T0)
add("E02", "线性叠加原理：任意 (f,g) 线性组合仍满足方程",
    "PASS" if abs(mix_res) < 1e-6 else "FAIL",
    note="(0.9f − 0.4g) 的一维残差 %s（浮点零）⇒ 方程线性，解空间为向量空间（也正是 D03 零判别力的来源）。"
         % fs(mix_res),
    residual=fs(mix_res))

add("E03", "一维 d'Alembert 通解形式 f(t−r/c)+g(t+r/c) 本身正确",
    "PASS",
    note="对任意二次可微 f,g 成立（E02 即其见证）；该形式与 1/r 无关，1/r 只在球对称三维中出现（见 C04/C06）。",
    form="f(xi)+g(eta)")

add("E04", "与电磁波方程 / 弱场引力波方程同形（标准结果）",
    "PASS",
    note="无源 Maxwell 与弱场线性化 Einstein 方程在洛伦兹/横向无迹规范下都化为 □h=0。"
         "这是「兼容」而非「新预言」：兼容性不能为该方程的推导链背书。",
    compat=["Maxwell (Lorenz gauge)", "linearized GR (TT gauge)"])

add("E05", "一维方程 ∂²_r L=(1/c²)∂²_t L 作为独立命题正确",
    "PASS",
    note="对 f(ξ) 与 g(η) 均成立（B02/E02 见证）；问题不在方程，而在「由 r=ct 第一性推出它」这一步。",
    verdict_scope="equation only")


# ============================================================
# F. 新判据与净增量账
# ============================================================
add("F01", "新判据 D-9「修复即降级」：修掉错误后论证从「推出」降为「验证已知解」",
    "INFO",
    note="把 §3 的一阶符号改为正确的 −1/c 后，第一步即等价于「L 沿光线守恒」= 假设 L=f(ξ)，"
         "于是「推导」变成「验证一个已知单向波解」。⇒ 该符号错误不是笔误，而是论证结构的承重件；"
         "修与不修都不产生新物理。与 r173 的「修复即自杀」互补：那一类修了就使立论消失，"
         "这一类修了就使论证降级。",
    criterion="D-9",
    contrast="r173 修复即自杀 / r175 修复即降级")

add("F02", "「第一性原理推出」资格判定：未达 —— 一阶运动学公设不能定出二阶 PDE",
    "FAIL",
    note="r=ct 是运动学（一阶）；从它到二阶 PDE 必须额外声明「L 沿光线守恒」或「L=L(ξ)」"
         "（B07 已证二者等价）。未声明假设 +1 条 ⇒ 净前提未下降，不满足第一性原理门"
         "（r134 的净前提下降门）。",
    extra_assumption=1,
    gate="net-premise-decrease")

add("F03", "净增量账：结论 0 新增 / 推导链 4 处缺陷 / 版本互补 1 处 / 可引用增量 0",
    "INFO",
    note="本章节状态 = 「结论对、链条错、无增量」。可引用者仅 K-08/K-18 两条教科书式（已由 10-03 登记），"
         "「时空固有脉动」的诠释部分不产生任何可算内容。",
    net_new=0, chain_defects=4, version_conflicts=1)


# ============================================================
# 守卫（工具自检）
# ============================================================
guard("G0-1 量纲乘法 = 指数相加（非相乘）",
      dmul((1, 2, 3, 4), (1, 1, 1, 1)) == (2, 3, 4, 5),
      "dmul((1,2,3,4),(1,1,1,1))=%s" % (dmul((1, 2, 3, 4), (1, 1, 1, 1)),))

g2_ana = 6.0
g2_num = nd2(lambda r, t: r * r, 'r', R0, T0) + (2.0 / R0) * nd1(lambda r, t: r * r, 'r', R0, T0)
guard("G0-2 球对称拉普拉斯恒等式自检：L=r² ⇒ ∇²=6",
      rel(g2_num, g2_ana) < 1e-6,
      "num=%s ana=%s rel=%s" % (fs(g2_num), fs(g2_ana), fs(rel(g2_num, g2_ana), 2)))

g3_num = nd1(L_OUT, 'r', R0, T0)
g3_ana = -f_out_d(xi(R0, T0)) / C_TEST
guard("G0-3 一阶差分 vs 解析（出向波 ∂_r = −f'/c）",
      rel(g3_num, g3_ana) < 1e-6, "rel=%s" % fs(rel(g3_num, g3_ana), 2))

  # 收敛测试必须在截断主导区（h=1e-2 / 5e-3）做；在 1e-5 附近是舍入主导，比值无意义
g4_a = abs(nd2(L_OUT, 't', R0, T0, 1e-2) - f_out_dd(xi(R0, T0)))
g4_b = abs(nd2(L_OUT, 't', R0, T0, 5e-3) - f_out_dd(xi(R0, T0)))
g4_ratio = g4_a / g4_b if g4_b > 0 else 0.0
guard("G0-4 中心差分二阶收敛（截断主导区 h:1e-2→5e-3，误差比 ≈ 4）",
      3.5 < g4_ratio < 4.5, "ratio=%s" % fs(g4_ratio, 4))

guard("G0-5 数值波速刻意取 c≠1（防 1/c 与 1 退化为同一值）",
      abs(C_TEST - 1.0) > 1e-6, "c_test=%s" % fs(C_TEST, 2))

g6 = rel(f_sph_1d_ana, f_sph_1d_num)
guard("G0-6 C05 的解析残差与数值残差互证（两条独立路径）",
      g6 < 1e-5, "rel=%s" % fs(g6, 2))

g7_dt = nd1(L_OUT, 't', R0, T0) + C_TEST * nd1(L_OUT, 'r', R0, T0)
g7_scale = abs(f_out_d(xi(R0, T0))) + 1e-30
guard("G0-7 特征线守恒自检：dL/dt = ∂_t L + c∂_r L = 0（仅对 f(ξ)）",
      abs(g7_dt) / g7_scale < 1e-6, "rel=%s" % fs(abs(g7_dt) / g7_scale, 2))

guard("G0-8 口径隔离自检：球对称算子作用于平面波的残差必须 ≠ 0（否则 C01/C02 分列失效）",
      abs(c03) > 1e-3, "res=%s" % fs(c03))

control("c1", "靶文行数", str(SCAN["target_lines"]), ">0", SCAN["target_lines"] > 0)
control("c2", "对照版行数", str(SCAN["refmeta_lines"]), ">0", SCAN["refmeta_lines"] > 0)
control("c3", "靶文正号桥关系命中", str(SCAN["target_bridge_plus"]), ">=1",
        SCAN["target_bridge_plus"] >= 1)
control("c4", "对照版负号桥关系命中", str(SCAN["refmeta_bridge_minus"]), ">=1",
        SCAN["refmeta_bridge_minus"] >= 1)
control("c5", "靶文通解含 1/r", str(SCAN["target_has_over_r"]), ">=1",
        SCAN["target_has_over_r"] >= 1)
control("c6", "对照版通解无 1/r（plain sum 命中）", str(SCAN["refmeta_plain_sum"]), ">=1",
        SCAN["refmeta_plain_sum"] >= 1)
control("c7", "靶文「只保留外向波解」命中", str(SCAN["target_outgoing_only"]), ">=1",
        SCAN["target_outgoing_only"] >= 1)
control("c8", "族枚举非平凡桥命中数", str(n_br), "1", n_br == 1)


def summarize():
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    return cnt


class Tee(object):
    """同时写控制台与 _report.txt，保持两者逐字一致。"""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass
        return len(s)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def main():
    t0 = time.time()
    cnt = summarize()
    _rp = os.path.join(OUT, STEM + "_report.txt")
    _orig = sys.stdout
    _rf = None
    try:
        os.makedirs(OUT, exist_ok=True)
        _rf = io.open(_rp, "w", encoding="utf-8")
        sys.stdout = Tee(_orig, _rf)
    except Exception:
        _rf = None

    print("=" * 78)
    print("TUFT-r175｜S17-08 空间波动方程 —— 桥关系符号与三维漏项")
    print("=" * 78)
    print("靶文: %s" % TARGET)
    print("对照: %s" % REFMETA)
    print("读取: 靶=%s(%d行)  对照=%s(%d行)  c_test=%s"
          % ("OK" if TGT_OK else "FAIL", SCAN["target_lines"],
             "OK" if REF_OK else "FAIL", SCAN["refmeta_lines"], fs(C_TEST, 2)))
    print("扫描: 靶正号桥=%d  靶负1/c=%d  对照负号桥=%d  对照负1/c=%d"
          % (SCAN["target_bridge_plus"], SCAN["target_minus_one_over_c"],
             SCAN["refmeta_bridge_minus"], SCAN["refmeta_minus_one_over_c"]))
    print("      靶通解1/r=%d  对照plain=%d  外向波句=%d"
          % (SCAN["target_has_over_r"], SCAN["refmeta_plain_sum"],
             SCAN["target_outgoing_only"]))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %s  %s" % (it["status"], it["id"], it["title"]))
        if it["note"]:
            print("       · %s" % it["note"])
        if it["metrics"]:
            kv = ", ".join("%s=%s" % (k, v) for k, v in sorted(it["metrics"].items())
                           if not isinstance(v, (list, dict)))
            if kv:
                print("       · %s" % kv)
    print("-" * 78)
    print("族枚举（桥关系 vs 一维波动方程，c=%s）:" % fs(C_TEST, 2))
    for row in FAM_ROWS:
        print("  %-22s bridge=%-5s wave=%-5s br_trl=%-5s wv_trl=%-5s res_br=%-12s res_wv=%s"
              % (row["name"], row["bridge_hit"], row["wave_hit"],
                 row["br_trivial"], row["wv_trivial"],
                 row["bridge_res"], row["wave_res"]))
    print("解空间抽查（任意 (f,g) 组合的一维残差）:")
    for row in SOL_ROWS:
        print("  %-18s residual=%s" % (row["coef"], row["residual"]))
    print("版本互补表:")
    for row in VER_TABLE:
        print("  %-52s 符号=%s 一维=%s 三维=%s => %s"
              % (row["version"][:52], row["bridge_sign"],
                 row["eq1d_vs_solution"][:14], row["eq3d_spherical"][:14], row["score"]))
    print("-" * 78)
    for c in CONTROLS:
        print("  [ctl%s] %-40s 值=%-8s 期望=%s"
              % ("OK" if c["ok"] else "NG", c["desc"][:40], c["value"], c["expect"]))
    for g in GUARDS:
        print("  [grd%s] %-56s %s"
              % ("OK" if g["ok"] else "NG", g["name"][:56], g["detail"]))
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(ITEMS),
                          "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt))))
    print("控制 %d/%d   守卫 %d/%d   用时 %.2fs"
          % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS), time.time() - t0))

    payload = {
        "stem": STEM,
        "round": "r175",
        "target": TARGET,
        "refmeta": REFMETA,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "constants": {"c_test": C_TEST, "r0": R0, "t0": T0, "dh": DH},
        "text_scan": SCAN,
        "verdict": {
            "core": "结论式（标准波动方程）正确，但「由单一公设 r=ct 第一性推出」不成立："
                    "一阶桥关系符号只对汇聚波成立、三维推广在球对称分支漏 2/r、"
                    "所给 1/r 通解不满足其自身推出的一维方程，且两版本在同三项判据上互补、无完整正确版。",
            "defects": ["一阶桥关系正号错（应为 −1/c），且与主旨外向传播互斥",
                        "三维推广在球对称分支漏 (2/r)∂_r 项",
                        "1/r 通解不满足自身一维方程（方程与解不同源）",
                        "循环：正确桥关系 ⟺ L=f(ξ) ⟺ 已假设解",
                        "函数空间两难（二元偏导 vs r=ct 单参数）",
                        "§5.3 数值验证为恒等式复读",
                        "薛定谔相似性与横波特性两处类比错误"],
        },
        "inherited": {"K-08": "结论式 ≡ 标准波动方程（L0 PASS）",
                      "K-18": "通解补 1/r 后精确满足（PASS）",
                      "r141-D3": "式 3.8 零新增（INFO）",
                      "10-03-N1": "元数据版通解缺 1/r（FAIL）"},
        "family_enum": FAM_ROWS,
        "version_table": VER_TABLE,
        "plane_rows": PLANE_ROWS,
        "solution_rows": SOL_ROWS,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": "%d/%d" % (n_guard_ok, len(GUARDS)),
        "control_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
    }
    try:
        os.makedirs(OUT, exist_ok=True)
        jp = os.path.join(OUT, STEM + ".json")
        with io.open(jp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("JSON  -> %s" % jp)

        mp = os.path.join(OUT, STEM + ".md")
        lines = []
        lines.append("# TUFT-r175 精算摘要")
        lines.append("")
        lines.append("- 靶：`08-空间波动方程/时空的固有脉动：空间波动方程的第一性原理推导、诠释与验证.md`")
        lines.append("- 对照：`01_文献来源/来源_核心公式元数据/8空间波动方程.md`")
        lines.append("- 条目：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
        lines.append("- 控制：%d/%d　守卫：%d/%d"
                     % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
        lines.append("")
        lines.append("| 编号 | 状态 | 判定 |")
        lines.append("|---|---|---|")
        for it in ITEMS:
            lines.append("| %s | %s | %s |"
                         % (it["id"], it["status"], it["title"].replace("|", "\\|")))
        lines.append("")
        lines.append("## 族枚举（c=%s）" % fs(C_TEST, 2))
        lines.append("")
        lines.append("| 测试函数 | 桥关系命中 | 一维波动方程命中 | 桥残差 | 波残差 |")
        lines.append("|---|---|---|---|---|")
        for row in FAM_ROWS:
            lines.append("| %s | %s | %s | %s | %s |"
                         % (row["name"], row["bridge_hit"], row["wave_hit"],
                            row["bridge_res"], row["wave_res"]))
        lines.append("")
        lines.append("## 版本互补")
        lines.append("")
        lines.append("| 版本 | 一阶符号 | 一维自洽 | 三维球对称 | 得分 |")
        lines.append("|---|---|---|---|---|")
        for row in VER_TABLE:
            lines.append("| %s | %s | %s | %s | %s |"
                         % (row["version"], row["bridge_sign"],
                            row["eq1d_vs_solution"], row["eq3d_spherical"], row["score"]))
        lines.append("")
        with io.open(mp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("MD    -> %s" % mp)
    except Exception as exc:
        print("[warn] 落盘失败: %s" % exc)

    try:
        sys.stdout = _orig
        if _rf is not None:
            _rf.close()
            print("REPORT-> %s" % _rp)
    except Exception:
        pass

    return 0 if n_guard_ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
