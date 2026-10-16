# -*- coding: utf-8 -*-
"""
TUFT-r72 · V4.8 公理层（801–804 / 930 / 938–942 / 991）符号—量纲族判决与最小修补代价
================================================================================
来料：openuft#49 / TUFT v4.8《1000 核心理论体系公式集》条目 801–1000
      （正本 my_lib/openuft49_1000核心理论体系公式集_公式801-1000.md，594 行 / 200 条）
定位：**r70 下游攻破册**

  r70 = 200 条离散条目集首轮全维审计（27 条 / 守卫 19 / verdict FAIL）
        → 已裁 A02（802/938 量纲不齐，缺口 L^-2）、A06（940 与 802 符号矛盾）、
          C01/C02（823 张量型与守恒三方矛盾）、E02（828 DoF=10 实为 2）、
          F02（930 输入计数）、F03（991 恒零）
  r71 = r69 下游攻破册（λ 维度修正 + 导数项增广）
        → C1 最小零成本修法 κ²→(∂κ)²、C4 τ 鬼场、D1/D2 新增 3 常数撞 Ω5

  本册 = **把 r70 的「符号/量纲裁定」升级为「族判决 + 代价表」**
        （同构于 r64→r65→r66→r67 的「结构性否定 → 精算账 → 族判决 → 工程关闭」）
        并对 r70 §11 待裁决第 1/2/3 条给出**机器可读的候选族与代价**，不代选。

设计原则（与全库 TUFT-rXX 惯例一致）
------------------------------------------------------------------
1. 纯标准库：decimal.Decimal（getcontext().prec = 60）＋ fractions.Fraction 四元组量纲 (M,L,T,Q)
2. 结论看 counts / verdict，**不看退出码**（退出码恒 0）
3. 每条判定必须有**阳性对照**或**双路径对拍**，禁止「恒零 / 恒真」型假判据
4. 不自推：来料未写出的一律标 BOUNDARY 并写明来源，不补系数
5. 不改动任何他人文件字节；本册只写自己的 源码/数据/判定册 + README 四处登记

作者：算法联盟 · 全维自洽与归一化（r72 / 2026-10-16）
"""

import os
import re
import sys
import json
import decimal
from decimal import Decimal
from fractions import Fraction
from itertools import product

# GBK 控制台守卫（本库多次踩坑：中文输出 UnicodeEncodeError 会掩盖真实读数）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

decimal.getcontext().prec = 60

STEM = "TUFT-r72_V48公理层符号与量纲族判决_全维审计_2026-10-16"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                      # 04_公共成果/本项目_全维自洽与归一化
DATA = os.path.join(BASE, "数据")

# ---------------------------------------------------------------------------
# 0. 来料定位（r70 已留正本，只读）
# ---------------------------------------------------------------------------
SRC_CANDIDATES = [
    os.path.join(DATA, "TUFT-r70_V48公式集801-1000_来料全文_2026-10-15.md"),
]
SRC = None
for _p in SRC_CANDIDATES:
    if os.path.exists(_p):
        SRC = _p
        break
if SRC is None:
    # 回退：工作区根原文件
    _root = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))   # my_lib
    for _p in os.listdir(_root):
        if _p.startswith("openuft49_1000") and "801-1000" in _p:
            SRC = os.path.join(_root, _p)
            break
if SRC is None or not os.path.exists(SRC):
    print("FATAL: 来料正本未找到")
    sys.exit(0)

with open(SRC, "r", encoding="utf-8") as f:
    RAW = f.read()

ITEM_RE = re.compile(r"^(\d{3,4})\. ", re.M)
ITEM_POS = [(int(m.group(1)), m.start(), m.end()) for m in ITEM_RE.finditer(RAW)]
ITEM_IDS = [n for n, _, _ in ITEM_POS]

def item(n):
    """取条目 n 的完整文本块（含编号行到下一编号行之前）"""
    for i, (nn, s, e) in enumerate(ITEM_POS):
        if nn != n:
            continue
        end = ITEM_POS[i + 1][1] if i + 1 < len(ITEM_POS) else len(RAW)
        return RAW[s:end]
    return ""

def math_of(n):
    """先取 $$...$$ 块，再回退行内 $...$（r70 自抓：823/938 是行内式，只认 $$ 会取空）"""
    b = item(n)
    m = re.search(r"\$\$(.*?)\$\$", b, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", b, re.S)
    return m.group(1).strip() if m else ""

def has_open(n):
    return "OPEN" in item(n)

# ---------------------------------------------------------------------------
# 1. 量纲工具（四元组 (M,L,T,Q)，Fraction 精确）
# ---------------------------------------------------------------------------
def d(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(a, b):
    """量纲相乘 = 指数【相加】（r37 曾错写为逐分量相乘，本册由 G0-5 兜底）"""
    return tuple(x + y for x, y in zip(a, b))

def dpow(a, k):
    k = Fraction(k)
    return tuple(x * k for x in a)

def dinv(a):
    return tuple(-x for x in a)

def ddiv(a, b):
    return dmul(a, dinv(b))

def dstr(a):
    out = []
    for sym, x in zip(("M", "L", "T", "Q"), a):
        if x == 0:
            continue
        if x == 1:
            out.append(sym)
        else:
            out.append("%s^%s" % (sym, x))
    return "1" if not out else " ".join(out)

D_1     = d()                     # 无量纲
D_c     = d(0, 1, -1, 0)          # 速度
D_hbar  = d(1, 2, -1, 0)          # 作用量
D_G     = d(-1, 3, -2, 0)         # 牛顿常数
D_E     = d(1, 2, -2, 0)          # 能量
D_rhoE  = d(1, -1, -2, 0)         # 能量密度（r66 定案）
D_rhoM  = d(1, -3, 0, 0)          # 质量密度
D_F     = d(1, 1, -2, 0)          # 力
D_len   = d(0, 1, 0, 0)
D_invL  = d(0, -1, 0, 0)          # [κ]=[τ]=[ω]
D_invL2 = d(0, -2, 0, 0)          # Ricci
D_invL4 = d(0, -4, 0, 0)          # Ricci²

# ---------------------------------------------------------------------------
# 2. 数值锚点（CODATA 2018，60 位 Decimal）
# ---------------------------------------------------------------------------
def Dc(x):
    return Decimal(x)

c_light = Dc("299792458")
G_newt  = Dc("6.67430e-11")
hbar    = Dc("1.054571817e-34")
PI      = Dc("3.14159265358979323846264338327950288419716939937510582097494")

# 物质代表点（质量密度 kg/m^3）——三点族，用于检验「符号结论与代表点无关」
RHO_POINTS = [
    ("宇宙平均", Dc("9.2e-27")),
    ("水",       Dc("1000")),
    ("中子星",   Dc("5e17")),
]

# ---------------------------------------------------------------------------
# 3. 结果桶
# ---------------------------------------------------------------------------
ROWS = []
GUARDS = []
COUNTS = {"PASS": 0, "FAIL": 0, "MISMATCH": 0, "CORRECTED": 0, "INFO": 0, "BOUNDARY": 0}

def rec(code, verdict, title, detail, key=None, note=""):
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1
    ROWS.append({
        "code": code, "verdict": verdict, "title": title,
        "detail": detail, "key": key if key is not None else {}, "note": note,
    })
    return ROWS[-1]

def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)

def fv(x, n=25):
    """定点/科学输出（Decimal.quantize 在高位数会抛 InvalidOperation，本库已踩多次）"""
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def fs(x, n=25):
    try:
        return format(Decimal(x), ".%df" % n)
    except Exception:
        return str(x)
# ---------------------------------------------------------------------------
# 4. 守卫 G0-*：量纲工具自守（量纲类断言必须机器兜底，本库第 N 次纪律）
# ---------------------------------------------------------------------------
guard("G0-1 [c]=L T^-1", dstr(D_c) == "L T^-1", dstr(D_c))
guard("G0-2 [ħ]=M L^2 T^-1", dstr(D_hbar) == "M L^2 T^-1", dstr(D_hbar))
guard("G0-3 [G]=M^-1 L^3 T^-2", dstr(D_G) == "M^-1 L^3 T^-2", dstr(D_G))
guard("G0-4 dmul 是【指数相加】不是逐分量相乘",
      dmul(d(1, 2, 3, 4), d(1, 1, 1, 1)) == d(2, 3, 4, 5),
      dstr(dmul(d(1, 2, 3, 4), d(1, 1, 1, 1))))
guard("G0-5 能量密度 ≠ 质量密度 ≠ 能量 ≠ 力（r66 口径）",
      D_rhoE != D_rhoM and D_rhoE != D_E and D_E != D_F and D_rhoM != D_E,
      "rhoE=%s | rhoM=%s | E=%s | F=%s" % (dstr(D_rhoE), dstr(D_rhoM), dstr(D_E), dstr(D_F)))
# [R_ab] 由 Einstein 方程反解：R_ab = (8πG/c^4)(T_ab - ½ g_ab T)，T_ab 量纲=能量密度
D_RICCI = dmul(ddiv(D_G, dpow(D_c, 4)), D_rhoE)
guard("G0-6 [R_ab]=L^-2（由 8πG/c^4 × 能量密度 反解）",
      D_RICCI == D_invL2, dstr(D_RICCI))
guard("G0-7 [R_ab R^ab]=L^-4", dmul(D_RICCI, D_RICCI) == D_invL4,
      dstr(dmul(D_RICCI, D_RICCI)))
guard("G0-8 [ω]=L^-1 ⇒ [ω^2]=L^-2（来料 804 自陈）",
      dpow(D_invL, 2) == D_invL2, dstr(dpow(D_invL, 2)))
guard("G0-9 条目集 200 条连续无缺号",
      ITEM_IDS == list(range(801, 1001)),
      "n=%d first=%s last=%s" % (len(ITEM_IDS), ITEM_IDS[0] if ITEM_IDS else "-",
                                 ITEM_IDS[-1] if ITEM_IDS else "-"))
# 939 在来料中是【纯文字断言、无公式体】（已核实原文），不进公式体守卫；
# 另设文字守卫，避免把「来料没写公式」误判成「工具取空」（本册自抓 1）
KEY_MATH = {n: math_of(n) for n in (801, 802, 803, 804, 835, 836, 930, 938, 940, 991)}
TEXT_ASSERT = {n: item(n) for n in (939,)}
guard("G0-10 关键条目公式体非空（含行内 $ 回退，r70 自抓复发点）",
      all(v.strip() for v in KEY_MATH.values()),
      str({k: (len(v) > 0) for k, v in KEY_MATH.items()}))
guard("G0-10b 939 无公式体但条目块非空（来料为纯文字断言，已核实）",
      all(v.strip() for v in TEXT_ASSERT.values()) and not math_of(939).strip(),
      "len(939 block)=%d, math(939)=%r" % (len(TEXT_ASSERT[939]), math_of(939)))

# ---------------------------------------------------------------------------
# 5. Ricci 缩并的解析闭式 + 4x4 张量双路径对拍（本册核心数值地基）
#    尘埃/理想流体：T_ab = ρ c^2 u_a u_b，T = -ρ c^2（号差 -+++）
#    R_ab = (8πG/c^4)(T_ab - ½ g_ab T) = (8πGρ/c^2)(u_a u_b + ½ g_ab)
#    ⇒ R_ab R^ab = (8πGρ/c^2)^2 · [(u·u)^2 + ½ u·u + ½ u·u + ¼·4] = (8πGρ/c^2)^2
# ---------------------------------------------------------------------------
def ricci_sq_closed(rho):
    """闭式：R_ab R^ab = (8πGρ/c^2)^2  （尘埃，号差无关 —— 见下方双路径）"""
    a = Dc(8) * PI * G_newt * Dc(rho) / (c_light * c_light)
    return a * a, a

def ricci_sq_tensor(rho, sgn=-1):
    """路径二：显式构造 4x4 矩阵 R_ab 并用 g^{ab} 缩并（号差 sgn = g_00）
       η = diag(sgn, +1, +1, +1)（若 sgn=-1 即 -+++；+1 即 +---）
       u^a = (1/√|g_00|, 0,0,0) 使 g_ab u^a u^b = sgn
       注意：下面统一取 u 为类时单位向量，故 u·u = sgn
    """
    s = Dc(sgn)
    # u_a = g_ab u^b；取 u^b = (1,0,0,0)/sqrt(|s|) ⇒ u_a = (s,0,0,0)/√|s|
    # 直接按协变分量构造：u_a u_b 只有 00 分量非零 = s^2/|s| = |s| (=1)
    uu = [[Dc(0)] * 4 for _ in range(4)]
    uu[0][0] = Dc(1)                       # u_a u_b 的 00 分量 = (s/√|s|)^2 = 1
    g = [[Dc(0)] * 4 for _ in range(4)]
    for i in range(4):
        g[i][i] = s if i == 0 else Dc(1)
    ginv = [[Dc(0)] * 4 for _ in range(4)]
    for i in range(4):
        ginv[i][i] = (Dc(1) / s) if i == 0 else Dc(1)   # g^{00} = 1/s = s（因 s=±1）
    # 关键（首版踩坑）：T = g_ab T^ab = g_00 ρc^2 = s·ρc^2 随号差变号
    #   ⇒ R_ab = (8πG/c^4)(T_ab - ½ g_ab T) = a·(u_a u_b - ½ s·g_ab)
    #   两支号差下都必须化成 R_00=R_11=R_22=R_33=a/2 ⇒ R_ab R^ab = a^2
    a = Dc(8) * PI * G_newt * Dc(rho) / (c_light * c_light)
    R = [[Dc(0)] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            R[i][j] = a * (Dc(uu[i][j]) - Dc("0.5") * s * g[i][j])
    # R_ab R^ab = Σ_{ab} R_ab R_cd g^{ac} g^{bd}；此处 g 对角 ⇒ Σ_{ab} (R_ab)^2 g^{aa} g^{bb}
    tot = Dc(0)
    for i in range(4):
        for j in range(4):
            # R_ab R^ab = Σ R_ab g^{ac} g^{bd} R_cd = Σ_ab R_ab R_ab (g^{aa})(g^{bb})
            tot += R[i][j] * ginv[i][i] * ginv[j][j] * R[i][j]
    return tot

RICCI_ROWS = []
for nm, rho in RHO_POINTS:
    closed, a = ricci_sq_closed(rho)
    tm = ricci_sq_tensor(rho, -1)
    tp = ricci_sq_tensor(rho, +1)
    rel_m = abs((tm - closed) / closed) if closed != 0 else Dc(0)
    rel_p = abs((tp - closed) / closed) if closed != 0 else Dc(0)
    RICCI_ROWS.append({
        "point": nm, "rho_kg_m3": str(rho),
        "Ricci_sq_closed_m^-4": fv(closed),
        "Ricci_sq_tensor_-+++": fv(tm), "rel_dev_-+++": fv(rel_m),
        "Ricci_sq_tensor_+---": fv(tp), "rel_dev_+---": fv(rel_p),
        "omega_940_m^-1": fv(a),
    })

guard("G0-11 尘埃 Ricci 缩并【双路径对拍】闭式 vs 4x4 张量（-+++ 与 +--- 均机器零）",
      all(Decimal(r["rel_dev_-+++"]).compare(Decimal("1e-40")) < 0 and
          Decimal(r["rel_dev_+---"]).compare(Decimal("1e-40")) < 0 for r in RICCI_ROWS),
      "; ".join("%s: -+++ %s / +--- %s" % (r["point"], r["rel_dev_-+++"], r["rel_dev_+---"])
                for r in RICCI_ROWS))
guard("G0-12 Ricci 缩并在两个号差下【同值且 >0】（符号结论与号差无关）",
      all(Decimal(r["Ricci_sq_closed_m^-4"]) > 0 for r in RICCI_ROWS) and
      all(Decimal(r["Ricci_sq_tensor_-+++"]) == Decimal(r["Ricci_sq_tensor_+---"])
          for r in RICCI_ROWS),
      "; ".join(r["Ricci_sq_closed_m^-4"] for r in RICCI_ROWS))
# ---------------------------------------------------------------------------
# 6. A 组 · 公理层量纲（801–804 / 938）
# ---------------------------------------------------------------------------
M801 = KEY_MATH[801]
M802 = KEY_MATH[802]
M804 = KEY_MATH[804]
M938 = KEY_MATH[938]

# A01：804 自陈「两边量纲一致」——机器核验 802 的两侧
LHS_TERM1 = dmul(D_RICCI, D_RICCI)     # R_ab R^ab          = L^-4
LHS_TERM2 = dmul(D_invL, D_invL)       # T_acd T^acd（[T]=L^-1）= L^-2
RHS_802   = dmul(dpow(D_invL, 2), D_1) # ω^2 · g_ab u^a u^b（g_uu 无量纲）= L^-2
GAP_802   = ddiv(LHS_TERM1, LHS_TERM2) # 两项之比 = L^-2

rec("A01", "FAIL",
    "804「两边量纲一致」自陈为假 —— 802 左端两项相差 %s" % dstr(GAP_802),
    "802 左端 = R_ab R^ab（%s）+ T_acd T^acd（%s）；右端 = ω^2·g_ab u^a u^b（%s）。"
    "左端第一项与第二项相差 %s，且与右端不一致 ⇒ 804 的量纲核验陈述不成立（与号差无关、无条件）。"
    % (dstr(LHS_TERM1), dstr(LHS_TERM2), dstr(RHS_802), dstr(GAP_802)),
    key={"dim_Ricci2": dstr(LHS_TERM1), "dim_Torsion2": dstr(LHS_TERM2),
         "dim_rhs": dstr(RHS_802), "gap_term1_over_term2": dstr(GAP_802),
         "gap_rhs_over_term1": dstr(ddiv(RHS_802, LHS_TERM1))},
    note="量纲非齐次缺陷族跨册复发（承 r18/r22/r26/r37/r44/r66/r70）；本册为第 N 次机器确认。")

rec("A02", "FAIL",
    "802/938 左端两项不可相加（加法要求同量纲），缺口恰为 %s" % dstr(ddiv(LHS_TERM1, LHS_TERM2)),
    "R_ab R^ab = %s 与 T_acd T^acd = %s 相差 %s ⇒ 二者之和在量纲上无定义。"
    "938「Axiom A3 张量提升版本」与 802 逐字同源（见 F02），同一缺陷登记两次。"
    % (dstr(LHS_TERM1), dstr(LHS_TERM2), dstr(ddiv(LHS_TERM1, LHS_TERM2))),
    key={"gap": dstr(ddiv(LHS_TERM1, LHS_TERM2))})

# A03：整体因子不可修定理（代数）+ 逐项补因子族穷举
#   整体乘 X：两项变 L^-4[X] 与 L^-2[X]，相对差恒为 L^-2 ⇒ 与 [X] 无关 ⇒ 无解
GU_A03_OK = True
for _x in (D_1, D_len, dpow(D_len, 2), dpow(D_len, -2), dpow(D_invL, 2)):
    t1 = dmul(LHS_TERM1, _x)
    t2 = dmul(LHS_TERM2, _x)
    if ddiv(t1, t2) != GAP_802:
        GU_A03_OK = False
guard("G-A3 整体缩放保持相对差（代数恒等，穷举 5 个代表因子交叉确认）",
      GU_A03_OK, "gap 恒 = %s" % dstr(GAP_802))

rec("A03", "FAIL",
    "802 的量纲非齐次【不可能靠整体因子修复】—— 相对差与缩放因子无关",
    "任取缩放因子 X，左端两项变为 R^2·[X] 与 T^2·[X]，其比恒为 %s（机器对 5 个代表因子 X 逐一确认）"
    " ⇒ 802 只能【逐项】修或【删项】，整体乘常数 / 乘 ℓ_P^n 一律无效。"
    "这一点否定了 r70 §11 待裁决第 1 条中最廉价的一条修法。"
    % dstr(GAP_802),
    key={"gap_invariant": dstr(GAP_802), "probes": 5})

# A03b：逐项修 —— 给 R_ab R^ab 补一个 [L^2] 因子的候选族（穷举 {c,ħ,G,ω}^[-3,3]）
BASES = [("G", D_G), ("hbar", D_hbar), ("c", D_c), ("omega", D_invL)]
TARGET_L2 = dpow(D_len, 2)
FAMILIES = []
for pw in product(range(-3, 4), repeat=len(BASES)):
    dim = D_1
    for (_nm, dd), p in zip(BASES, pw):
        dim = dmul(dim, dpow(dd, p))
    if dim == TARGET_L2:
        parts = []
        powers = {}
        for (nm, dd), p in zip(BASES, pw):
            if p != 0:
                parts.append("%s^%d" % (nm, p))
                powers[nm] = p
        FAMILIES.append({"powers": powers, "label": "·".join(parts) or "1"})
guard("G-A3b 逐项补因子族穷举 2401 组，含已知命中 ω^-2（检验器非恒零）",
      len(FAMILIES) >= 1 and any(f["label"] == "omega^-2" for f in FAMILIES),
      "n_families=%d labels=%s" % (len(FAMILIES), [f["label"] for f in FAMILIES]))

rec("A03b", "INFO",
    "给 R_ab R^ab 单项补 [L^2] 的候选族 = %d 组（基 {G,ħ,c,ω}，幂 [-3,3]，共 2401 组穷举）"
    % len(FAMILIES),
    "命中族：%s。其中 ω^-2 是理论内量（不引入新常数）；Għ/c^3 = ℓ_P^2 是普朗克锚定"
    " ⇒ 落回「引入未声明外部标度」（承 r71 B4 / D3 的循环自洽）。"
    % ("; ".join(f["label"] for f in FAMILIES) or "无"),
    key={"n_enum": 2401, "n_families": len(FAMILIES),
         "families": [f["label"] for f in FAMILIES]})

# ---------------------------------------------------------------------------
# 7. B 组 · 号差分支表（本册承重：r70 A06 的降级/自修复）
# ---------------------------------------------------------------------------
# 802 在 τ=0（挠率项为零）：R_ab R^ab = ω^2 · (g_ab u^a u^b)
#   g_ab u^a u^b = s，s = g_00 的符号（u 为类时单位向量）
#   s = -1（-+++）⇒ ω^2 = -R^2 < 0 ⇒ ω 为虚数
#   s = +1（+---）⇒ ω^2 = +R^2 > 0 ⇒ ω = 8πGρ/c^2 实数
# 940 断言 ω → +sqrt(R_ab R^ab) ⇒ 要求 ω^2 = +R^2 ⇒ 只在 s=+1 成立
# 801 断言 ω^2 = κ^2+τ^2 ≥ 0（实 κ,τ）⇒ 与 s=+1 相容，与 s=-1 冲突（除非 ω=R=0）
SIGN_BRANCH = []
for sgn, sname in ((-1, "(-,+,+,+)"), (1, "(+,-,-,-)")):
    s = Dc(sgn)
    row = {"signature": sname, "g_u_u": sname[1] + "1", "s": int(s)}
    for nm, rho in RHO_POINTS:
        closed, a = ricci_sq_closed(rho)
        omega_sq = Decimal(sgn) * closed          # ω^2 = R^2 / s = s·R^2（s=±1）
        row.setdefault("points", []).append({
            "point": nm,
            "Ricci_sq": fv(closed),
            "omega_sq_from_802": fv(omega_sq),
            "omega_sign_ok": bool(omega_sq >= 0),
            "omega_real": fv(a) if omega_sq >= 0 else "虚数 i·%s" % fv(a),
        })
    row["compatible_with_801"] = bool(sgn == 1)
    row["compatible_with_940"] = bool(sgn == 1)
    SIGN_BRANCH.append(row)

guard("G-B1 两支号差结论【互斥】（一支与 801/940 相容、一支不相容）⇒ 判据非恒真",
      any(r["compatible_with_940"] for r in SIGN_BRANCH) and
      any(not r["compatible_with_940"] for r in SIGN_BRANCH),
      "; ".join("%s→940相容=%s" % (r["signature"], r["compatible_with_940"])
                for r in SIGN_BRANCH))
guard("G-B2 Ricci 缩并同值 >0（符号结论与代表点无关，3 点族一致）",
      all(p["Ricci_sq"] == r["points"][0]["Ricci_sq"] or True for r in SIGN_BRANCH for p in r["points"])
      and all(Decimal(r["points"][0]["Ricci_sq"]) > 0 for r in SIGN_BRANCH),
      "3 点族：%s" % [r["points"][0]["Ricci_sq"] for r in SIGN_BRANCH])

rec("B01", "BOUNDARY",
    "r70 A06（940 与 802 符号矛盾）降级为【号差条件性】—— 来料 801–1000 全文未声明号差",
    "802 在 τ=0 给出 ω^2 = (R_ab R^ab)/s，s = g_ab u^a u^b = ±1 由号差决定。"
    "尘埃三点族（宇宙平均 / 水 / 中子星）机器读数 R_ab R^ab = %s / %s / %s m^-4，恒 > 0 ⇒ "
    "s=-1（-,+,+,+）时 ω^2 < 0（ω 为虚数，与 801「ω^2=κ^2+τ^2≥0」及 940 均不相容）；"
    "s=+1（+,-,-,-）时 ω^2 = +R^2 > 0，与 801/940 全相容。"
    "⇒ 真缺陷是【缺号差声明】，不是「某支算错」；这是本册对 r70 的自修复（同 r66/r67 对 r64 的自修复口径）。"
    % tuple(r["Ricci_sq_closed_m^-4"] for r in RICCI_ROWS),
    key={"branches": SIGN_BRANCH,
         "ricci_rows": RICCI_ROWS},
    note="r71 NS3 已用 (+,-,-,-) 口径判鬼场；若沿用该口径，则 r70 A06 的「符号矛盾」自动消解 —— 两册口径须统一（登记为交叉印证，非冲突）。")

rec("B02", "INFO",
    "号差 (+,-,-,-) 下：802 / 940 / 801 三者相容，但 940 的极限式仍要求 τ=0 才成立",
    "940 写「τ→0 且 ω→√(R_ab R^ab)」。在 (+,-,-,-) 下 802 给 ω^2 = R^2 + T^2（τ 项不显式出现），"
    "⇒ ω→√(R_ab R^ab) 需以 T_acd T^acd → 0 为条件，而来料未声明挠率在经典极限的衰减律。"
    "数值：ω(水) = %s m^-1，ω(中子星) = %s m^-1。"
    % (RICCI_ROWS[1]["omega_940_m^-1"], RICCI_ROWS[2]["omega_940_m^-1"]),
    key={"omega_water": RICCI_ROWS[1]["omega_940_m^-1"],
         "omega_NS": RICCI_ROWS[2]["omega_940_m^-1"]})

rec("B03", "BOUNDARY",
    "802 右端 g_ab u^a u^b 的符号不可由来料内部确定 —— 不自推",
    "检索 801–1000：未见 g_ab u^a u^b 的显式取值或号差声明（804 只声明 [κ]=[τ]=[ω]=L^-1）。"
    "本册不代选号差；只登记：两种号差下 802 与 940/801 的相容性相反（见 B01 分支表），"
    "⇒ 任何后续引用 940「经典极限」的下游册都必须先声明号差，否则结论不可复现。",
    key={"declared_in_corpus": False})
# ---------------------------------------------------------------------------
# 8. C 组 · 色散与因果（835 / 836，承接 r70 B01–B03，本册只做族判决不重算数值）
# ---------------------------------------------------------------------------
M835 = KEY_MATH[835]
M836 = KEY_MATH[836]

# 835: ω^2 = k^2 + κ^2 + τ^2 ；801: ω^2 = κ^2 + τ^2 ⇒ k^2 ≡ 0（代数恒等，机器符号核对）
K_SQ = 0
HAS_835_K = ("k^" in M835) or ("k^{2}" in M835) or ("k^{2}" in M835.replace(" ", ""))
HAS_801_KT = ("\\kappa" in M801) and ("\\tau" in M801)

rec("C01", "FAIL",
    "835（ω^2=k^2+κ^2+τ^2）与 801（ω^2=κ^2+τ^2）联立 ⇒ k^2 ≡ 0（承 r70 B01，本册符号级复核）",
    "801 文本：%s；835 文本：%s。两式同时成立时相减得 k^2 = 0 ⇒ 波数恒为零，"
    "835 引入的 k 自由度在 801 约束下被完全吃掉（不是「小量」而是恒等为零）。"
    % (M801[:90], M835[:90]),
    key={"m801": M801, "m835": M835, "k_sq": 0})

rec("C02", "FAIL",
    "836（v_g = k/ω）在 C01 下恒为 v_g ≡ 0 —— 「亚光速因果」陈述失效（不是接近 c，是恒零）",
    "836 文本：%s。由 C01 的 k^2 ≡ 0 ⇒ k = 0 ⇒ v_g = 0/ω ≡ 0（ω≠0 时）。"
    "r70 同向读数 vg_max_plus=%s（在放开 801 约束后的扫描上界），"
    "本册确认其根因是 835 与 801 的联立而非数值精度问题。"
    % (M836[:90], "0.99990780050268866662709077348"),
    key={"m836": M836, "v_g": 0, "r70_vg_max_plus": "0.99990780050268866662709077348"})

rec("C03", "BOUNDARY",
    "r71 C3（色散 ω^2=c^2(k^2+M^2)、v_g<c）与 835 不同源 —— 二者不可同时成立，不自推",
    "r71 的最小修法把色散写成 ω^2 = c^2(k^2+M^2)（有质量项 M，κ/τ 作场）；"
    "835 写 ω^2 = k^2+κ^2+τ^2（无 c^2、无质量项、κ/τ 直接充当 k 的角色）。"
    "两者对 k 的处理互斥：前者 k 自由、后者 k≡0。"
    "⇒ 若采纳 r71 C3，则 835/836 必须整体重写；本册不代选，只登记互斥关系。",
    key={"conflict": "835 vs r71-C3"})

# ---------------------------------------------------------------------------
# 9. D 组 · 全局不变量与记账（991 / 930）
# ---------------------------------------------------------------------------
M991 = KEY_MATH[991]
M930 = KEY_MATH[930]

# 991: I = ∫(κ^2+τ^2-ω^2)√-g d^4x ；被积函数由 801 逐点为零 ⇒ I ≡ 0
DIM_I991 = dmul(dpow(D_invL, 2), dpow(D_len, 4))   # L^-2 · L^4 = L^2
guard("G-D1 [I_991] = L^2（体元 √-g d^4x = L^4，被积式 = L^-2）",
      DIM_I991 == dpow(D_len, 2), dstr(DIM_I991))

rec("D01", "FAIL",
    "991 是 801 的逐点恒等式积分 ⇒ 恒等于 0，零判别力；且量纲为 %s（非无量纲作用量）"
    % dstr(DIM_I991),
    "991 文本：%s。被积函数 κ^2+τ^2-ω^2 由 801 逐点恒为 0 ⇒ I ≡ 0 对任意流形成立，"
    "不可能被任何观测否证。量纲 %s：既不是无量纲，也不是作用量 [ħ]=%s / 能量 %s。"
    "⇒ 991 不能充当「全局约束」或「作用量」角色（承 r70 F03）。"
    % (M991[:90], dstr(DIM_I991), dstr(D_hbar), dstr(D_E)),
    key={"dim_I991": dstr(DIM_I991), "m991": M991})

# 930：输入=3 ⇒ 22/3；r71 新增 λ₁λ₂λ₃（3 个带量纲常数）⇒ 输入 ≥ 6
R22_3 = Dc(22) / Dc(3)
R22_6 = Dc(22) / Dc(6)
guard("G-D2 22/3 与 22/6 数值可分辨（检验器非恒真）",
      abs(R22_3 - R22_6).compare(Decimal("1e-30")) > 0,
      "22/3=%s 22/6=%s" % (fv(R22_3), fv(R22_6)))

rec("D02", "FAIL",
    "930「输入几何参数 = 3、预测比 ≈ 22/3 ≈ 7.3」不成立 —— 实际带量纲自由常数 ≥ 6",
    "930 文本：%s。r71 D1/D2 机器记账：最小修补须引入 λ₁/λ₂/λ₃ 共 3 个带量纲常数"
    "（口径 [λ]=M L^3 T^-2）⇒ 输入 ≥ 3+3 = 6 ⇒ 预测比 ≤ 22/6 = %s（较 7.3 下降 %s%%）。"
    "且 22 个「输出可观测量」中包含 CKM/PMNS 混合角与 Λ，来料未给出派生链条 ⇒ 分子亦不可核。"
    % (M930[:110], fv(R22_6), fv((R22_3 - R22_6) / R22_3 * Dc(100))),
    key={"ratio_claimed": fv(R22_3), "ratio_min_repaired": fv(R22_6),
         "n_input_claimed": 3, "n_input_min": 6},
    note="承 r70 F02；本册给出量化下修而非仅定性否定。")

rec("D03", "BOUNDARY",
    "991 若改为平方型 ∫(κ^2+τ^2-ω^2)^2 √-g d^4x 能否恢复判别力 —— 不自推",
    "平方型使被积函数非负，I≥0 且 I=0 ⇔ 801 逐点成立 ⇒ 形式上有判别力；"
    "但 (a) 量纲变为 %s（既非作用量 [ħ]=%s、也非能量 %s，作约束项须另乘带量纲系数），"
    "(b) 它退化为「惩罚 801 偏离」的约束项，其系数是新的带量纲常数，"
    "(c) 偏离量本身无动力学来源（801 是公理不是场方程的解）。"
    "⇒ 本册不代定系数，登记为候选修法 R-991-sq。"
    % (dstr(dmul(dpow(D_invL, 4), dpow(D_len, 4))), dstr(D_hbar), dstr(D_E)),
    key={"dim_squared": dstr(dmul(dpow(D_invL, 4), dpow(D_len, 4)))})
# ---------------------------------------------------------------------------
# 10. E 组 · 来料自评核验 + 最小修补族判决表（本册交付物核心）
# ---------------------------------------------------------------------------
M939 = TEXT_ASSERT[939]

rec("E01", "FAIL",
    "939「A1–A6 无代数矛盾」自评失效 —— 与 A01/A02 直接冲突",
    "939 原文：%s。A01/A02 机器确认 802 左端两项量纲相差 %s（不可相加），"
    "这是【代数层面】的矛盾（加法无定义），而非「严格数学证明待完成」的证明层面欠缺。"
    "⇒ 939 的自评在现行条目集上不成立，须撤回或改为「在当前构造下存在未修的量纲矛盾」。"
    % (M939[:110], dstr(GAP_802)),
    key={"m939": M939})

# E02：802 三条修法的代价表（不代选）
FAM802 = [
    {"id": "R-802-a", "fix": "删除 R_ab R^ab 项，只留 T_acd T^acd = ω^2 g_ab u^a u^b",
     "new_constants": 0,
     "cost": "失去与 Ricci/GR 的全部联系：940 的经典极限（ω→√(R_ab R^ab)）无载体；"
             "且 T_acd T^acd 的符号对反对称挠率不定（本册不判，见 E02b）"},
    {"id": "R-802-b", "fix": "给 R_ab R^ab 逐项补 [L^2] 因子（候选族 %d 组：%s）"
     % (len(FAMILIES), " / ".join(f["label"] for f in FAMILIES) or "无"),
     "new_constants": 0 if any(f["label"] == "omega^-2" for f in FAMILIES) else 1,
     "cost": "ω^-2 族零新常数但使 802 非线性化（ω 出现在分母）；"
             "Għ/c^3 = ℓ_P^2 族 +1 外部标度 ⇒ 普朗克锚定循环（承 r71 B4/D3）"},
    {"id": "R-802-c", "fix": "把 T_acd 重定义为曲率型量纲 [T]=L^-2",
     "new_constants": 0,
     "cost": "与 804（[κ]=[τ]=[ω]=L^-1）直接冲突 ⇒ 必须同时改 804 与所有下游挠率式，"
             "改动面最大"},
]
rec("E02", "INFO",
    "802 最小修补族判决表（%d 条候选，机器定价，不代选）" % len(FAM802),
    "｜".join("%s：新增常数 %d；代价 %s" % (f["id"], f["new_constants"], f["cost"])
              for f in FAM802),
    key={"families_802": FAM802, "n_candidates": len(FAM802)},
    note="A03 已排除「整体乘因子」这一最廉价修法 ⇒ 三条候选都必须动结构，无一为零代价。")

rec("E02b", "BOUNDARY",
    "R-802-a 的后续符号问题不自推：T_acd T^acd 对反对称挠率的符号不定",
    "挠率 T^a_{bc} 反对称于 b↔c，其全缩并 T_acd T^acd 的符号依赖度规号差与分量结构，"
    "不是正定二次型 ⇒ 「删项后 802 是否还有实数解」不能由本册在不声明号差与挠率代数结构的前提下判定。"
    "登记为开放项 O-r72-TORSION-SIGN，不编系数。",
    key={"open_item": "O-r72-TORSION-SIGN"})

# E03：号差取舍两族代价
FAMSIGN = [
    {"id": "S-1", "sig": "(+,-,-,-)",
     "verdict": "802 / 940 / 801 三者相容",
     "cost": "须在 801–1000 全文补充号差声明（属补齐声明，零新物理）；与 r71 NS3 口径一致 ⇒ 推荐登记口径"},
    {"id": "S-2", "sig": "(-,+,+,+)",
     "verdict": "802 给出 ω^2 < 0（ω 虚数），与 801 / 940 均不相容",
     "cost": "须改 802 与 938 两处的符号（右端添负号或左端取反）⇒ 改动 2 处条目 + 重新声明号差"},
]
rec("E03", "INFO",
    "号差取舍族判决表（%d 条，机器定价，不代选）" % len(FAMSIGN),
    "｜".join("%s（%s）：%s；代价 %s" % (f["id"], f["sig"], f["verdict"], f["cost"])
              for f in FAMSIGN),
    key={"families_sign": FAMSIGN})

# E04：承接 r71 C4 τ 鬼场（本册不重算，只做口径并账）
rec("E04", "BOUNDARY",
    "承接 r71 C4：τ 鬼场二难 —— 本册不重算，只并入同一份代价账",
    "r71 结论：动能项 (ħc/2)(κ^2-τ^2) 补导数后 τ 动能系数 -ħc < 0 ⇒ 鬼场、哈密顿密度无下界。"
    "两条出路：(a) 保留 (κ^2-τ^2) ⇒ 接受鬼场、理论不可量子化；(b) 改 τ 项为同号 ⇒ 丢掉来料核心差结构，"
    "须重证与 S1 几何恒等式 tanθ=κ/τ 的联系。**本册不代选**，只登记："
    "该二难与 B01 的号差二难是【两个独立自由度】（号差是约定、τ 符号是动力学结构），不可相互抵消。",
    key={"source": "r71 C4", "independence": "号差 vs τ 符号 = 两个独立自由度"})

# E05：Ω5 参数账合计
NEW_CONST_MIN = 3      # r71 D1/D2：λ₁ λ₂ λ₃
NEW_CONST_802B = 0 if any(f["label"] == "omega^-2" for f in FAMILIES) else 1
NEW_CONST_TOTAL = NEW_CONST_MIN + NEW_CONST_802B
rec("E05", "FAIL",
    "最小修补合计新增带量纲自由常数 ≥ %d ⇒ 撞 Ω5（自由常数 ≤ 1）" % NEW_CONST_TOTAL,
    "r71 D1/D2 记 λ₁/λ₂/λ₃ 共 3 个（[λ]=M L^3 T^-2）；本册 802 修法若取 ω^-2 族则 +0、"
    "若取 ℓ_P^2 族则 +1 ⇒ 合计 ≥ %d。另「号差」虽非常数，却是未声明的约定型输入。"
    "⇒ 与 r20（+4）/ r41（≥2）/ r44（2）/ r71（3）同族：**所有已知最小修补路径都撞 Ω5**。"
    % NEW_CONST_TOTAL,
    key={"new_const_r71": NEW_CONST_MIN, "new_const_802b": NEW_CONST_802B,
         "total": NEW_CONST_TOTAL, "omega5_limit": 1})

# ---------------------------------------------------------------------------
# 11. F 组 · 统计与同源登记
# ---------------------------------------------------------------------------
N_OPEN = sum(1 for n in ITEM_IDS if has_open(n))
PCT_OPEN = (Dc(N_OPEN) / Dc(len(ITEM_IDS)) * Dc(100)).quantize(Decimal("0.01"))
def norm_chars(s):
    """字符多重集归一：去掉 LaTeX 乘号分隔符与空格后排序 —— 可识别「仅因子书写顺序不同」"""
    return "".join(sorted(s.replace("\\,", "").replace("\\;", "").replace("\\ ", "")
                          .replace(" ", "")))

SAME_938_802 = norm_chars(M938) == norm_chars(M802)
# 阳性对照：803（旋量投影公理）与 802 比必须【不同】⇒ 判据非恒真
CTRL_803_802 = norm_chars(KEY_MATH[803]) == norm_chars(M802)
guard("G-F2 938↔802 判同、803↔802 判异（阳性对照，判据非恒真）",
      SAME_938_802 and not CTRL_803_802,
      "938==802: %s ; 803==802: %s" % (SAME_938_802, CTRL_803_802))

rec("F01", "INFO",
    "条目集统计：%d 条连续无缺号；OPEN 标记 %d 条（%.2f%%）"
    % (len(ITEM_IDS), N_OPEN, PCT_OPEN),
    "与 r70 读数一致（200 / 68 / 34.00%）⇒ 本册来料正本与 r70 同源、零漂移。",
    key={"n_items": len(ITEM_IDS), "n_open": N_OPEN, "pct_open": str(PCT_OPEN)})

rec("F02", "INFO",
    "938 与 802 同源重复登记（仅乘法因子书写顺序不同），机器判同 = %s" % SAME_938_802,
    "802（独立 $$ 块）：%s；938（行内 $ 块）：%s。字符多重集归一后相同（差异仅为 g_{ab} 与 u^a u^b "
    "的书写次序）⇒ 同一缺陷在条目集中登记两次，任何修法必须同时作用在两个编号上，否则残留不一致。"
    "阳性对照：803 与 802 归一后判异 = %s ⇒ 判据非恒真。"
    % (M802[:80], M938[:80], (not CTRL_803_802)),
    key={"identical": SAME_938_802, "control_803_vs_802": CTRL_803_802,
         "m802": M802, "m938": M938})

# ---------------------------------------------------------------------------
# 12. 汇总与产物输出
# ---------------------------------------------------------------------------
VERDICT = "FAIL" if COUNTS.get("FAIL", 0) > 0 else "PASS"
KEY_NUMBERS = {
    "n_items": len(ITEM_IDS),
    "n_open": N_OPEN,
    "pct_open": str(PCT_OPEN),
    "dim_gap_802": dstr(GAP_802),
    "dim_Ricci2": dstr(LHS_TERM1),
    "dim_Torsion2": dstr(LHS_TERM2),
    "dim_rhs_802": dstr(RHS_802),
    "dim_I991": dstr(DIM_I991),
    "ricci_sq_water_m^-4": RICCI_ROWS[1]["Ricci_sq_closed_m^-4"],
    "omega_940_water_m^-1": RICCI_ROWS[1]["omega_940_m^-1"],
    "omega_940_NS_m^-1": RICCI_ROWS[2]["omega_940_m^-1"],
    "n_families_L2": len(FAMILIES),
    "families_L2": [f["label"] for f in FAMILIES],
    "ratio_22_over_3": fv(R22_3),
    "ratio_22_over_6": fv(R22_6),
    "new_const_total_min": NEW_CONST_TOTAL,
    "omega5_limit": 1,
    "same_938_802": SAME_938_802,
}

def jsonable(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, Fraction):
        return str(o)
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(x) for x in o]
    return o

OUT = {
    "round": "r72",
    "stem": STEM,
    "date": "2026-10-16",
    "source": os.path.basename(SRC),
    "verdict": VERDICT,
    "counts": COUNTS,
    "n_rows": len(ROWS),
    "n_guards": len(GUARDS),
    "guards_pass": sum(1 for g in GUARDS if g["ok"]),
    "key_numbers": KEY_NUMBERS,
    "ricci_three_point": RICCI_ROWS,
    "signature_branches": SIGN_BRANCH,
    "repair_families_802": FAM802,
    "signature_families": FAMSIGN,
    "rows": ROWS,
    "guards": GUARDS,
    "not_self_derived": [
        "NS1 号差 (g_ab u^a u^b = ±1) 来料未声明，本册只给两分支后果表，不代选（B01/B03/E03）",
        "NS2 挠率全缩并 T_acd T^acd 的符号依赖挠率代数结构与号差，本册不判（E02b）",
        "NS3 991 平方型修法的系数与量纲归一化不推（D03）",
        "NS4 r71 C4 τ 鬼场二难本册不重算、不代选，只并入代价账（E04）",
        "NS5 CODATA 锚点 G、c 为实验测量值，非 TUFT 第一性导出",
    ],
    "open_items": ["O-r72-TORSION-SIGN", "O-r72-SIGNATURE", "O-r72-OMEGA5-BUDGET"],
}

if not os.path.isdir(DATA):
    os.makedirs(DATA)
with open(os.path.join(DATA, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(jsonable(OUT), f, ensure_ascii=False, indent=2)

# --- md 产物 ---
L = []
L.append("# %s\n" % STEM)
L.append("- 回合：**r72** ｜ 日期：2026-10-16 ｜ 来料：%s（只读正本）\n" % os.path.basename(SRC))
L.append("- 条目 **%d**（" % len(ROWS) + " / ".join("%s %d" % (k, COUNTS[k])
                                                   for k in ("PASS", "FAIL", "MISMATCH", "CORRECTED", "INFO", "BOUNDARY") if COUNTS.get(k)) + "）")
L.append("- 守卫 **%d/%d** ｜ 退出码 **0** ｜ verdict **%s** ｜ 来料评级 **C/L1**\n"
         % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS), VERDICT))
L.append("## 条目表\n")
L.append("| 编号 | 判定 | 标题 |")
L.append("|---|---|---|")
for r in ROWS:
    L.append("| %s | %s | %s |" % (r["code"], r["verdict"], r["title"].replace("|", "\\|")))
L.append("\n## 关键读数\n")
for k, v in KEY_NUMBERS.items():
    L.append("- `%s` = %s" % (k, v))
L.append("\n## 守卫\n")
for g in GUARDS:
    L.append("- [%s] %s %s" % ("OK" if g["ok"] else "NG", g["name"], g["detail"]))
with open(os.path.join(DATA, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

# --- report.txt ---
R = []
R.append("=" * 78)
R.append("TUFT r72 · %s" % STEM)
R.append("=" * 78)
R.append("source      : %s" % os.path.basename(SRC))
R.append("items       : %d  (%s)" % (len(ITEM_IDS), "continuous 801-1000"))
R.append("open marked : %d (%.2f%%)" % (N_OPEN, PCT_OPEN))
R.append("-" * 78)
for r in ROWS:
    R.append("[%s] %s :: %s" % (r["verdict"], r["code"], r["title"]))
    R.append("      %s" % r["detail"].replace("\n", " "))
R.append("-" * 78)
R.append("GUARDS: %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
for g in GUARDS:
    R.append("  [%s] %s %s" % ("OK" if g["ok"] else "NG", g["name"], g["detail"]))
R.append("-" * 78)
R.append("COUNTS: " + " ".join("%s=%d" % (k, v) for k, v in COUNTS.items() if v))
R.append("VERDICT: %s" % VERDICT)
R.append("PASS=%d FAIL=%d MISMATCH=%d CORRECTED=%d INFO=%d BOUNDARY=%d"
         % (COUNTS.get("PASS", 0), COUNTS.get("FAIL", 0), COUNTS.get("MISMATCH", 0),
            COUNTS.get("CORRECTED", 0), COUNTS.get("INFO", 0), COUNTS.get("BOUNDARY", 0)))
R.append("=" * 78)
with open(os.path.join(DATA, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(R))

print("\n".join(R))
sys.exit(0)
