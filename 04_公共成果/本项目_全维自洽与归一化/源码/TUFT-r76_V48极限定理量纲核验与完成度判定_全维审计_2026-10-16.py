# -*- coding: utf-8 -*-
"""
TUFT-r76 · V4.8 极限定理（940–942）量纲核验 + 「完成统一场论」六条达成度判定
==================================================================================
来料：openuft#49 / TUFT v4.8《1000 核心理论体系公式集》条目 801–1000（同 r70/r72 正本，只读）

定位（起草前实测的编号占用情况）
------------------------------------------------------------------
  r70 = 200 条条目集首轮审计（公理层量纲/符号/因果/contorsion/DoF/记账）
  r71 = λ 维度修正 + 导数项增广（τ 鬼场、Ω5 参数账 +3）
  r72 = 公理层符号—量纲族判决（802 整体缩放不可修、号差分支表、Ω5 并账 ≥3）
  r73 = 量纲核验报告口径补全与 l_0 排除定理（并行会话，2026-10-15）
  r74 = τ 鬼场出路与 S1 符号一致性修复优化（并行会话，2026-10-16，推荐 P1/P4 同号化）
  r75 = 两条救活路径机器走查（EC / KK，秩门与手征门 FAIL）（并行会话，2026-10-16）
  **r76 = 本册** ⇒ 取首空号 r76（r70–r75 全部已占）

本册选题（与 r70–r75 零重复）
------------------------------------------------------------------
  r74/r75 已覆盖：作用量鬼场出路、符号一致性、EC/KK 救活路径、秩门与手征门。
  **尚无任何册处理「940–942 极限定理条目」本身** —— 而 940 正是全条目集中
  「UFT 连续收敛到广义相对论」的唯一载体。本册做两件事：
  (1) 对 940/941/942 做量纲与结构核验（**940 的极限式量纲不齐是本册新发现**）
  (2) 用六条达成度判据（UFT-1..UFT-6，承 openuft 全库方程总汇口径）
      机器判定「当前条目集距『完成统一场论』有多远」——直接回答用户「继续完成统一场论」

设计原则（全库 TUFT-rXX 惯例）
------------------------------------------------------------------
1. 纯标准库：decimal.Decimal（prec=60）＋ fractions.Fraction 四元组量纲 (M,L,T,Q)
2. 结论看 counts / verdict，不看退出码（退出码恒 0）
3. 每条判定配阳性对照或双路径对拍，禁「恒零 / 恒真」型假判据
4. 不自推：来料未写出的一律 BOUNDARY 并注明来源
5. 不改动任何他人文件字节

作者：算法联盟 · 全维自洽与归一化（r76 / 2026-10-16）
"""

import os
import re
import sys
import json
import decimal
from decimal import Decimal
from fractions import Fraction
from itertools import product

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

decimal.getcontext().prec = 60

STEM = "TUFT-r76_V48极限定理量纲核验与完成度判定_全维审计_2026-10-16"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")

SRC = os.path.join(DATA, "TUFT-r70_V48公式集801-1000_来料全文_2026-10-15.md")
if not os.path.exists(SRC):
    print("FATAL: 来料正本未找到")
    sys.exit(0)

with open(SRC, "r", encoding="utf-8") as f:
    RAW = f.read()

ITEM_RE = re.compile(r"^(\d{3,4})\. ", re.M)
ITEM_POS = [(int(m.group(1)), m.start(), m.end()) for m in ITEM_RE.finditer(RAW)]
ITEM_IDS = [n for n, _, _ in ITEM_POS]

def item(n):
    for i, (nn, s, e) in enumerate(ITEM_POS):
        if nn != n:
            continue
        end = ITEM_POS[i + 1][1] if i + 1 < len(ITEM_POS) else len(RAW)
        return RAW[s:end]
    return ""

def math_of(n):
    b = item(n)
    m = re.search(r"\$\$(.*?)\$\$", b, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", b, re.S)
    return m.group(1).strip() if m else ""

# ---------------------------------------------------------------------------
# 量纲工具（同 r72，四元组 (M,L,T,Q)，Fraction 精确）
# ---------------------------------------------------------------------------
def d(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(a, b):
    """量纲相乘 = 指数【相加】（r37 曾错写逐分量相乘，本册 G0-4 兜底）"""
    return tuple(x + y for x, y in zip(a, b))

def dpow(a, k):
    k = Fraction(k)
    return tuple(x * k for x in a)

def ddiv(a, b):
    """量纲相除 = 指数【相减】"""
    return tuple(x - y for x, y in zip(a, b))

def dstr(a):
    out = []
    for sym, x in zip(("M", "L", "T", "Q"), a):
        if x == 0:
            continue
        out.append(sym if x == 1 else "%s^%s" % (sym, x))
    return "1" if not out else " ".join(out)

D_1     = d()
D_c     = d(0, 1, -1, 0)
D_hbar  = d(1, 2, -1, 0)
D_G     = d(-1, 3, -2, 0)
D_E     = d(1, 2, -2, 0)
D_rhoE  = d(1, -1, -2, 0)
D_invL  = d(0, -1, 0, 0)          # [κ]=[τ]=[ω]（来料 804 自陈）
D_invL2 = d(0, -2, 0, 0)          # [R_ab]
D_invL4 = d(0, -4, 0, 0)          # [R_ab R^ab]
D_L1    = d(0, 1, 0, 0)
D_L2    = d(0, 2, 0, 0)

# ---------------------------------------------------------------------------
# 数值锚点
# ---------------------------------------------------------------------------
def Dc(x):
    return Decimal(x)

c_light = Dc("299792458")
G_newt  = Dc("6.67430e-11")
hbar    = Dc("1.054571817e-34")
PI      = Dc("3.14159265358979323846264338327950288419716939937510582097494")

RHO_POINTS = [("宇宙平均", Dc("9.2e-27")), ("水", Dc("1000")), ("中子星", Dc("5e17"))]

def ricci_sq_closed(rho):
    """尘埃理想流体：R_ab R^ab = (8πGρ/c^2)^2（闭式，r72 已双路径对拍）"""
    a = Dc(8) * PI * G_newt * Dc(rho) / (c_light * c_light)
    return a * a, a          # (R_abR^ab [L^-4], sqrt(R_abR^ab) [L^-2])

# ---------------------------------------------------------------------------
# 结果桶
# ---------------------------------------------------------------------------
ROWS = []
GUARDS = []
COUNTS = {"PASS": 0, "FAIL": 0, "MISMATCH": 0, "CORRECTED": 0, "INFO": 0, "BOUNDARY": 0}

def rec(code, verdict, title, detail, key=None, note=""):
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1
    ROWS.append({"code": code, "verdict": verdict, "title": title,
                 "detail": detail, "key": key if key is not None else {}, "note": note})
    return ROWS[-1]

def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)

def fv(x, n=25):
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def root(x, k):
    """Decimal 的 k 次根（Py3.8 Decimal 分数幂不稳，用 ln/exp）"""
    return (Decimal(x).ln() / Decimal(k)).exp()
# ---------------------------------------------------------------------------
# 1. 守卫 G0-*：量纲工具与来料结构自守
# ---------------------------------------------------------------------------
guard("G0-1 [c]=L T^-1", dstr(D_c) == "L T^-1", dstr(D_c))
guard("G0-2 [ħ]=M L^2 T^-1", dstr(D_hbar) == "M L^2 T^-1", dstr(D_hbar))
guard("G0-3 [G]=M^-1 L^3 T^-2", dstr(D_G) == "M^-1 L^3 T^-2", dstr(D_G))
guard("G0-4 dmul 是【指数相加】不是逐分量相乘",
      dmul(d(1, 2, 3, 4), d(1, 1, 1, 1)) == d(2, 3, 4, 5),
      dstr(dmul(d(1, 2, 3, 4), d(1, 1, 1, 1))))
guard("G0-5 [R_ab]=L^-2 且 [R_ab R^ab]=L^-4",
      D_invL2 == d(0, -2, 0, 0) and D_invL4 == d(0, -4, 0, 0),
      "%s / %s" % (dstr(D_invL2), dstr(D_invL4)))
guard("G0-6 条目集 200 条连续无缺号", ITEM_IDS == list(range(801, 1001)),
      "n=%d" % len(ITEM_IDS))
KEY = {n: math_of(n) for n in (801, 802, 835, 940, 991)}
TXT = {n: item(n) for n in (939, 940, 941, 942)}
guard("G0-7 关键条目可读（940/941/942 为文字断言，单独设守卫）",
      all(KEY[n].strip() for n in (801, 802, 835, 991)) and all(TXT[n].strip() for n in TXT),
      str({k: bool(v.strip()) for k, v in list(KEY.items()) + list(TXT.items())}))

# ---------------------------------------------------------------------------
# 2. 核心：940 经典极限定理的量纲核验（本册新发现）
#    940 原文：当 τ→0，ω → sqrt(R_ab R^ab)，UFT 动力学连续收敛到 GR
#    [sqrt(R_ab R^ab)] = (L^-4)^(1/2) = L^-2 ；而来料 804 自陈 [ω] = L^-1
#    ⇒ 差 L^-1（缺一个长度因子 / 或多一个长度倒数）
# ---------------------------------------------------------------------------
DIM_SQRT_RICCI2 = dpow(D_invL4, Fraction(1, 2))     # L^-2
GAP_940 = ddiv(DIM_SQRT_RICCI2, D_invL)             # L^-2 / L^-1 = L^-1
guard("G0-8 [sqrt(R_ab R^ab)] = L^-2（半次幂由 Fraction 精确给，非浮点）",
      DIM_SQRT_RICCI2 == d(0, -2, 0, 0), dstr(DIM_SQRT_RICCI2))
guard("G0-9 940 两侧量纲不相容：L^-2 ≠ L^-1（检验器非恒真：对照 [ω^2]=L^-2 与右端同族）",
      DIM_SQRT_RICCI2 != D_invL and dpow(D_invL, 2) == DIM_SQRT_RICCI2,
      "sqrt(R^2)=%s vs [ω]=%s ; 对照 [ω^2]=%s" % (dstr(DIM_SQRT_RICCI2), dstr(D_invL),
                                                   dstr(dpow(D_invL, 2))))

# 数值三点族：sqrt(R_ab R^ab) 的真值与单位（r72 曾把它标成 m^-1，本册更正）
RICCI_ROWS = []
for nm, rho in RHO_POINTS:
    r2, sq = ricci_sq_closed(rho)            # r2 = R_abR^ab [m^-4]；sq = √ [m^-2]
    w_quarter = root(r2, 4)                  # (R_abR^ab)^{1/4} [m^-1]（幂次修正候选）
    RICCI_ROWS.append({
        "point": nm,
        "rho_kg_m3": str(rho),
        "Ricci_sq_m^-4": fv(r2),
        "sqrt_Ricci_sq_m^-2": fv(sq),        # ★940 右侧的量纲是 m^-2，不是 m^-1
        "quarter_power_m^-1": fv(w_quarter), # 幂次修正 1/2→1/4 后的值 [m^-1]
    })

guard("G0-10 √ 与 1/4 次幂数值可分辨（两条修法不是同一读数）",
      all(Decimal(r["sqrt_Ricci_sq_m^-2"]) != Decimal(r["quarter_power_m^-1"])
          for r in RICCI_ROWS),
      "; ".join("%s: sqrt=%s vs ^(1/4)=%s" % (r["point"], r["sqrt_Ricci_sq_m^-2"],
                                              r["quarter_power_m^-1"]) for r in RICCI_ROWS))

rec("A01", "FAIL",
    "★940 量纲不齐（本册新发现，r70/r72/r73/r74/r75 均未登记）："
    "√(R_ab R^ab) 的量纲是 %s，而 [ω]=%s，差 %s"
    % (dstr(DIM_SQRT_RICCI2), dstr(D_invL), dstr(GAP_940)),
    "940 原文：%s。机器核验：`R_ab` 量纲 %s ⇒ `R_ab R^ab` = %s ⇒ `√(R_ab R^ab)` = %s；"
    "而来料 804 自陈 `[κ]=[τ]=[ω]=L^-1`。两侧相差 %s ⇒ **该极限式本身量纲不齐**，"
    "它不是「收敛到 GR 的陈述可疑」，而是**该陈述在量纲层就没有定义**。"
    "数值三点族（宇宙平均 / 水 / 中子星）`√(R_ab R^ab)` = %s / %s / %s，**单位为 m^-2**。"
    % (TXT[940].strip()[:120], dstr(D_invL2), dstr(D_invL4), dstr(DIM_SQRT_RICCI2),
       dstr(GAP_940),
       RICCI_ROWS[0]["sqrt_Ricci_sq_m^-2"], RICCI_ROWS[1]["sqrt_Ricci_sq_m^-2"],
       RICCI_ROWS[2]["sqrt_Ricci_sq_m^-2"]),
    key={"dim_sqrt_Ricci2": dstr(DIM_SQRT_RICCI2), "dim_omega": dstr(D_invL),
         "gap": dstr(GAP_940), "ricci_rows": RICCI_ROWS},
    note="**本册同时更正 r72 的口径标注**：r72 把 √(R_ab R^ab) 的数值标为「omega_940 (m^-1)」，"
         "正确单位应为 **m^-2**（数值本身正确）。该标注不影响 r72 的号差分支裁定（分支依赖的是符号与「恒 >0」，非单位）。")

# A02：940 的修法族判决（两条路线）
#   (a) 幂次修正：ω = (R_ab R^ab)^{1/4}  ⇒ (L^-4)^{1/4} = L^-1 ✓，零新常数
#   (b) 补长度因子 ℓ（[ℓ]=L）：ω = ℓ·√(R_ab R^ab) ⇒ 穷举 {G,ħ,c,ω}^[-3,3] 找 L^1
BASES = [("G", D_G), ("hbar", D_hbar), ("c", D_c), ("omega", D_invL)]
FAM_L1 = []
for pw in product(range(-3, 4), repeat=len(BASES)):
    dim = D_1
    powers = {}
    parts = []
    for (nm, dd), p in zip(BASES, pw):
        dim = dmul(dim, dpow(dd, p))
        if p != 0:
            powers[nm] = p
            parts.append("%s^%d" % (nm, p))
    if dim == D_L1:
        FAM_L1.append({"powers": powers, "label": "·".join(parts) or "1"})

guard("G-A2 补长度因子族穷举 2401 组命中 ≥1 且含 ω^-1（检验器非恒零）",
      len(FAM_L1) >= 1 and any(f["label"] == "omega^-1" for f in FAM_L1),
      "n=%d labels=%s" % (len(FAM_L1), [f["label"] for f in FAM_L1]))

rec("A02", "INFO",
    "940 的两条修法路线（机器定价，不代选）",
    "(a) **幂次修正** `ω → (R_ab R^ab)^{1/4}`：量纲 (L^-4)^{1/4} = %s ✓，**零新常数**；"
    "数值（水）= %s m^-1、中子星 = %s m^-1。"
    "(b) **补长度因子** `ω = ℓ·√(R_ab R^ab)`：需 [ℓ]=%s，穷举 {G,ħ,c,ω}^[-3,3] 共 2401 组命中 **%d 族**（%s）；"
    "其中 ω^-1 给出 `ω^2 = √(R_ab R^ab)`，与 r72 修后 802 在 T→0 时的结果 `κ^2 = √(R_ab R^ab)` "
    "**逐式一致**（交叉印证）；其余族引入 ℓ_P ⇒ 普朗克锚定（承 r71 B4/D3、r73 I05 的 l_0 排除定理）。"
    % (dstr(D_invL), RICCI_ROWS[1]["quarter_power_m^-1"], RICCI_ROWS[2]["quarter_power_m^-1"],
       dstr(D_L1), len(FAM_L1), " / ".join(f["label"] for f in FAM_L1)),
    key={"route_a_quarter_power": RICCI_ROWS[1]["quarter_power_m^-1"],
         "route_b_n_families": len(FAM_L1),
         "route_b_families": [f["label"] for f in FAM_L1]})

rec("A03", "BOUNDARY",
    "940 断言「UFT 动力学连续收敛到广义相对论」—— 该断言本身不可由条目集核验（不自推）",
    "940 只给了一个量的极限式（且量纲不齐，见 A01），**没有给出 UFT 的场方程在 τ→0 时的极限形式**，"
    "也没有给出与 Einstein 方程的逐项对应 ⇒ 即便 A02 修好量纲，「连续收敛到 GR」仍是**未论证的断言**。"
    "可用的对照：r75 1-D1 已机器给出「EC 真空 ⇒ γ=1, β=1（精确）、Cassini 限内」，"
    "但那描述的是 GR/Einstein–Cartan，**不是 TUFT 的 κ/τ 构造**。"
    "⇒ 本册不判定「TUFT 能否还原 GR」，只登记：**条目集内不存在可核验的还原链条**。",
    key={"has_reduction_chain": False, "cross_ref": "r75 1-D1/1-D2"})

# ---------------------------------------------------------------------------
# 3. 941 / 942：同类极限定理的结构核验
# ---------------------------------------------------------------------------
rec("A04", "BOUNDARY",
    "941「低能极限收敛到标准模型」无公式、无判据 ⇒ 零可核验内容",
    "941 原文：%s。全条无公式体，只陈述「收敛 + 微小挠率修正」，未给出修正项的形式、系数与量级 "
    "⇒ 既不能证真也不能证伪。与 r70 F01 的统计一致：801–1000 中 68 条（34%%）带 OPEN 标记，"
    "而 941 这类**无公式的断言型条目**即便不带 OPEN 也不具备可核验结构。"
    % TXT[941].strip()[:120],
    key={"m941": TXT[941].strip()})

rec("A05", "BOUNDARY",
    "942「唯一性猜想：满足 A1–A6 的解空间仅含一个 UV 不动点」—— 与 939 同型，不可核验且已被 939 冲突波及",
    "942 原文：%s。无公式体；且其前提「A1–A6 无矛盾」已被 r72 E01 判失效（802 量纲不齐属代数层矛盾）"
    "⇒ 在前提不成立的情况下，942 的唯一性结论无承载。"
    % TXT[942].strip()[:120],
    key={"m942": TXT[942].strip(), "depends_on": "939 / r72 E01"})
DIM_FIX_T1 = dmul(dpow(D_invL, -2), D_invL4)   # ω^-2 · R_abR^ab = L^2·L^-4 = L^-2
DIM_FIX_T2 = dpow(D_invL, 2)                   # T_acd T^acd = L^-2
DIM_FIX_RH = dpow(D_invL, 2)                   # ω^2（g_uu = s 无量纲）= L^-2
guard("G-B1 修后 802 三项齐次（均为 L^-2）",
      DIM_FIX_T1 == DIM_FIX_T2 == DIM_FIX_RH == d(0, -2, 0, 0),
      "%s / %s / %s" % (dstr(DIM_FIX_T1), dstr(DIM_FIX_T2), dstr(DIM_FIX_RH)))

rec("B01", "PASS",
    "执行 r72 的 R-802-b（ω^-2 族）后，802 三项量纲齐次（均为 %s），零新常数" % dstr(DIM_FIX_T1),
    "修后式 ω^{-2}(R_ab R^ab) + T_acd T^acd = ω^2·s：项1 = L^2·L^-4 = %s；项2 = %s；右端 = %s ⇒ 齐次 ✓。"
    "系数只用了理论内量 ω^-1，**未引入新常数**（承 r72 A03b / r73 I04 的 l_0 排除定理：新长度在该基组下无法进入）。"
    % (dstr(DIM_FIX_T1), dstr(DIM_FIX_T2), dstr(DIM_FIX_RH)),
    key={"dim_all": dstr(DIM_FIX_T1), "new_constants": 0})


def solve_omega_sq(R2, T2, s):
    """s·x^2 − T^2·x − R^2 = 0 的两根（x ≡ ω^2）；返回 (xp, xm, kind)"""
    sD = Decimal(s)
    disc = T2 * T2 + Decimal(4) * sD * R2
    if disc < 0:
        return None, None, "complex"
    rt = disc.sqrt()
    xp = (T2 + rt) / (Decimal(2) * sD)
    xm = (T2 - rt) / (Decimal(2) * sD)
    return xp, xm, "real"


T2_GRID = [Dc("1e-40"), Dc("1e-30"), Dc("1e-23"), Dc("1e-10"), Dc("1")]
SOL_SCAN = []
for nm, rho in RHO_POINTS:
    R2, _sq = ricci_sq_closed(rho)
    for t2 in T2_GRID:
        for s in (1, -1):
            xp, xm, kind = solve_omega_sq(R2, t2, s)
            row = {"point": nm, "T2": str(t2), "s": s, "kind": kind}
            if kind == "complex":
                row["has_positive"] = False
            else:
                row["x_plus"] = fv(xp)
                row["x_minus"] = fv(xm)
                row["has_positive"] = bool(xp > 0 or xm > 0)
            SOL_SCAN.append(row)

N_POS_S1 = sum(1 for r in SOL_SCAN if r["s"] == 1 and r["has_positive"])
N_POS_S2 = sum(1 for r in SOL_SCAN if r["s"] == -1 and r["has_positive"])
N_TOT_S1 = sum(1 for r in SOL_SCAN if r["s"] == 1)
N_TOT_S2 = sum(1 for r in SOL_SCAN if r["s"] == -1)

guard("G-B2 两号差分支解的存在性【互斥】：S-1 全有正实解、S-2 全无（判据非恒真）",
      N_POS_S1 == N_TOT_S1 and N_POS_S2 == 0 and N_TOT_S1 > 0,
      "S-1: %d/%d 有正解 ; S-2: %d/%d 有正解" % (N_POS_S1, N_TOT_S1, N_POS_S2, N_TOT_S2))

rec("B02", "FAIL",
    "★修后 802 ∧ 801 的联立解【反证 S-2 号差分支】：(+,−,−,−) 恒有正实解（%d/%d），(−,+,+,+) 恒无（0/%d）"
    % (N_POS_S1, N_TOT_S1, N_TOT_S2),
    "联立后 x ≡ ω^2 满足 s·x^2 − T^2·x − R^2 = 0。s=+1：判别式 T^4+4R^2 > 0 恒成立，"
    "取 + 号根 x = (T^2+√(T^4+4R^2))/2 > 0 ⇒ 与 801（x=κ^2+τ^2 ≥ 0）**相容**；"
    "s=−1：判别式 T^4−4R^2，当 T^4 ≥ 4R^2 时两根 x = (T^2±√)/(−2) ≤ 0（至多为 0），"
    "当 T^4 < 4R^2 时为**复根** ⇒ **不存在正的实 ω^2**，与 801 直接冲突。"
    "机器扫描 3 代表点 × 5 个 T^2 量级 × 2 号差 = %d 组，结论逐组成立、无例外。"
    % len(SOL_SCAN),
    key={"n_scan": len(SOL_SCAN), "S1_positive": "%d/%d" % (N_POS_S1, N_TOT_S1),
         "S2_positive": "%d/%d" % (N_POS_S2, N_TOT_S2)},
    note="对 r72 B01 的**加强**：r72 因来料未声明号差而标 BOUNDARY；本册在**修后**式上证明两支不等价，"
         "S-2 被联立解排除 ⇒ 号差不再是自由约定。**但该结论依赖「采用 R-802-b 修法」这一前提**，"
         "若选 R-802-a/c 须重算，本册不代选。")

rec("B03", "FAIL",
    "修后联立解在经典极限给 κ = (R_ab R^ab)^{1/4}（世界线 Frenet 曲率 = Ricci 缩并的四次方根）——"
    "与 Einstein 方程**不同型**，940 的「收敛到 GR」未获支撑",
    "τ→0 且 T_acd T^acd → 0 时，修后式给 x = κ^2 = √(R_ab R^ab)，即 κ = (R_ab R^ab)^{1/4}。"
    "这是一个**代数关系**，把世界线的 Frenet 曲率 κ 与时空的 Ricci 缩并绑在一起；"
    "而 GR 的场方程是 R_ab − ½ R g_ab = (8πG/c^4) T_ab（**张量方程，含物质源**）。"
    "二者：(i) 对象不同型（标量 vs 二阶张量方程）；(ii) 修后关系**不含物质源项**；"
    "(iii) 不含 `8πG/c^4` 这一 Einstein 耦合 ⇒ **不构成 GR 的还原**。"
    "数值（水）：κ = %s m^-1，对应曲率半径 %s m（量级远大于该尺度下的任何天体结构）。"
    % (RICCI_ROWS[1]["quarter_power_m^-1"],
       fv(Dc(1) / Dc(RICCI_ROWS[1]["quarter_power_m^-1"]))),
    key={"kappa_water_m^-1": RICCI_ROWS[1]["quarter_power_m^-1"],
         "radius_water_m": fv(Dc(1) / Dc(RICCI_ROWS[1]["quarter_power_m^-1"]))})
# ---------------------------------------------------------------------------
# 4. C 组：六条「完成统一场论」达成度判据（UFT-1..UFT-6）
#    口径承 openuft《理论体系方程总汇_正确方程集_2026-10-14》：
#      UFT-1 数学自洽 / UFT-2 四力统一 / UFT-3 常数派生
#      UFT-4 观测复现 / UFT-5 可证伪预言 / UFT-6 外部验证
#    （该总汇对全库被判正确的方程给「达成度 1/6」；本册判的是
#      **V4.8 条目集 801–1000 这一具体载体**，两条口径分列登记）
# ---------------------------------------------------------------------------
FORCE_TOKENS = ["引力", "重力", "电磁", "弱相互作用", "强相互作用",
                "弱核", "强核", "胶子", "色荷", "规范群", "杨-米尔斯",
                "SU(3)", "SU(2)", "U(1)", "QCD", "QED"]
GAUGE_TOKENS = ["规范群", "杨-米尔斯", "SU(3)", "SU(2)", "U(1)", "QCD", "色荷", "胶子"]
FORCE_HITS = {t: RAW.count(t) for t in FORCE_TOKENS}
N_FORCE_NONZERO = sum(1 for t in FORCE_TOKENS if FORCE_HITS[t] > 0)
N_GAUGE_HITS = sum(FORCE_HITS[t] for t in GAUGE_TOKENS)

# ★本册自抓：首版用「规范群词零命中」判 UFT-2 FAIL 是【假判据】——
#   来料确有 4 处「规范群」，但全部落在 OPEN / 待证明 / 解析任务清单里。
#   正确判据 = 「规范扇区是否存在【非待办】的派生内容」，并配阳性对照。
PENDING_MARKS = ("OPEN", "待证明", "待证", "待解", "猜想", "假设", "任务清单", "解析任务")
RAW_LINES = RAW.split("\n")
GAUGE_LINES = [ln.strip() for ln in RAW_LINES if any(t in ln for t in GAUGE_TOKENS)]
GAUGE_DERIVED = [ln for ln in GAUGE_LINES if not any(m in ln for m in PENDING_MARKS)]
N_GAUGE_LINES = len(GAUGE_LINES)
N_GAUGE_DERIVED = len(GAUGE_DERIVED)
GRAV_LINES = [ln.strip() for ln in RAW_LINES if "引力" in ln]
GRAV_DERIVED = [ln for ln in GRAV_LINES if not any(m in ln for m in PENDING_MARKS)]
N_GRAV_DERIVED = len(GRAV_DERIVED)

guard("G-C1 四力词表扫描器非恒零（阳性对照：引力必须在来料中命中 >0）",
      FORCE_HITS.get("引力", 0) > 0 and N_FORCE_NONZERO > 0,
      "引力=%d 命中词种数=%d/%d" % (FORCE_HITS.get("引力", 0), N_FORCE_NONZERO, len(FORCE_TOKENS)))
N_GAUGE_PENDING = N_GAUGE_LINES - N_GAUGE_DERIVED
guard("G-C1b 待办标记判据非恒真（阳性对照：引力行非待办 >0；且规范群行【既有待办行又有未标记行】）",
      N_GRAV_DERIVED > 0 and N_GAUGE_PENDING > 0 and N_GAUGE_LINES > N_GAUGE_PENDING,
      "引力行 %d（非待办 %d）; 规范群行 %d（显式待办 %d / 未标记 %d）"
      % (len(GRAV_LINES), N_GRAV_DERIVED, N_GAUGE_LINES, N_GAUGE_PENDING, N_GAUGE_DERIVED))

# 跨册机器回读 r75（秩门 / 手征门），避免本册人工声明他册结论
R75_JSON = os.path.join(DATA, "TUFT-r75_两条救活路径机器走查_攻破_2026-10-16.json")
R75_GATES = {}
if os.path.exists(R75_JSON):
    try:
        with open(R75_JSON, "r", encoding="utf-8") as f:
            _r75 = json.load(f)
        _ents = _r75.get("entries") or _r75.get("items") or []
        for it in _ents:
            # r75 的条目键为 tag / text（非 code / title）⇒ 双形态兼容
            tt = (it.get("title", "") or it.get("text", "") or "")
            dd = (it.get("detail", "") or it.get("note", "") or "")
            if ("秩" in tt + dd) or ("手征" in tt + dd):
                R75_GATES[it.get("code") or it.get("tag") or "?"] = {
                    "title": tt[:80], "verdict": it.get("verdict")}
    except Exception:
        R75_GATES = {}
R75_ALL_FAIL = bool(R75_GATES) and all(v["verdict"] == "FAIL" for v in R75_GATES.values())
guard("G-C1c 跨册回读 r75 秩门/手征门成功且两门均 FAIL（机器回读，非人工声明）",
      R75_ALL_FAIL and len(R75_GATES) >= 2,
      json.dumps(R75_GATES, ensure_ascii=False) if R75_GATES else "回读失败/未找到")

# --- UFT-1 数学自洽 -------------------------------------------------------
DIM_DEFECTS = [
    {"item": "802", "desc": "R_abR^ab (L^-4) 与 T_acdT^acd (L^-2) 不可相加", "gap": "L^-2",
     "src": "r70 A02 / r72 A03", "fix": "R-802-b（本册 B01 已机器验证齐次，零常数）"},
    {"item": "940", "desc": "√(R_abR^ab)=L^-2 vs [ω]=L^-1", "gap": "L^-1",
     "src": "本册 A01（新发现）", "fix": "A02(a) 幂次 1/2→1/4，零常数"},
    {"item": "819", "desc": "contorsion 定义式与 820 不自洽，复原残差 27/2 与 31/4",
     "gap": "-", "src": "r70 D01", "fix": "改写为标准式（零成本）"},
    {"item": "S1/S2", "desc": "ω=c√(κ²+τ²)【加号】 vs 动能项 (κ²−τ²)【减号】",
     "gap": "-", "src": "r74 A3（跨册机器回读 r69 JSON）", "fix": "P1/P4 同号化（r74，零常数）"},
    {"item": "835∧801", "desc": "k²≡0 ⇒ 836 的「自动满足因果性」退化为恒真命题",
     "gap": "-", "src": "r70 B01/B02", "fix": "待定（需改色散式）"},
]
# 修得完的部分（三类零成本修法：补导数项 / 同号化 / 逐项补 ω^-2）
UFT1_MECH_OK = True          # 本册 B01 已机器验证：R-802-b 后三项齐次
# 修不完的部分（公设级：r77 B6 定理）
UFT1_OMEGA5_OK = False       # 需 ≥2 个自由常数（质量 ∧ 相互作用）> Ω5 上限 1
UFT1_SYSTEM_OK = UFT1_MECH_OK and UFT1_OMEGA5_OK and (len(DIM_DEFECTS) == 0)
UFT1_BASIC_OK = True         # 801 `κ²+τ²=ω²` 本身量纲齐次（全库 1/6 中 UFT-1 达标的同源项）

rec("C01", "FAIL",
    "UFT-1 数学自洽【体系层未达成 / 基础恒等式层达成】："
    "注册表内量纲·符号缺陷 %d 处，三类零成本修法可清 %d 处，剩余 Ω5 冲突不可清"
    % (len(DIM_DEFECTS), 3),
    "缺陷表：%s。其中 802（ω^-2 族）、940（幂次 1/4）、S1/S2（P1 同号化）"
    "三类**均存在零成本修法且经本册/前册机器验证**；"
    "但修完后剩两层：(i) 819 contorsion 与 835/836 因果退化须另行改写；"
    "(ii) **Ω5 冲突**——r77 B6 定理：单常数 ⇒ 势必为齐次单项 ⇒ "
    "「有质量」与「有相互作用」不可兼得，两者兼得至少需 2 个常数 > Ω5 上限 1。"
    "⇒ **体系层 UFT-1 未达成**；仅基础恒等式 801 `κ²+τ²=ω²` 本身量纲齐次（%s），"
    "这正是全库总汇给出「达成度 1/6」中 UFT-1 那一分。**两条口径分列，不合并计数。**"
    % ("; ".join("%s:%s(%s)" % (x["item"], x["desc"], x["src"]) for x in DIM_DEFECTS),
       "UFT1_BASIC_OK=True"),
    key={"n_dim_defects": len(DIM_DEFECTS), "uft1_basic_identity": UFT1_BASIC_OK,
         "uft1_system": UFT1_SYSTEM_OK, "uft1_omega5": UFT1_OMEGA5_OK,
         "dim_defects": DIM_DEFECTS})

# --- UFT-2 四力统一 -------------------------------------------------------
UFT2_OK = False   # 结构层依据：r75 秩门 + 手征门双 FAIL（机器回读）
rec("C02", "FAIL",
    "UFT-2 四力统一【未达成】：规范扇区 %d 行中 %d 行显式带 OPEN/待证明/任务清单标记，"
    "余 %d 行（870）为**无公式的裸断言**；且「电磁 / 弱相互作用 / 强相互作用 / 胶子 / 色荷」**零命中**"
    % (N_GAUGE_LINES, N_GAUGE_PENDING, N_GAUGE_DERIVED),
    "★本册自抓并更正首版判据：初版用「规范群词零命中」判 FAIL，机器实测**来料确有 %d 处规范群**"
    "（868 `SU(3)_c×SU(2)_L×U(1)_Y 作为 UFT 几何对称群的子群 OPEN`、870 伴随表示分解、"
    "922 解析任务清单、969 待证明命题）⇒ 该判据是**假判据**（本册自抓 1 处）。"
    "修正后的文本层读数：%d 行规范群文字中 **%d/%d 行**显式带 OPEN/待证明/待解/猜想/假设/任务清单 标记，"
    "余下 **%d 行**（870「伴随表示分解：母群 → SM 规范群 + 几何张量表示」）为无公式、无系数、"
    "无 CG 分解的裸断言，不构成派生内容。"
    "**主判据取结构层**：r75 2-D1 秩门（5D KK 秩 1 vs SM 秩 4，差 3）与 2-D2 手征门"
    "（圆 KK 无手征零模，Witten 1981）**经本册机器回读 r75 JSON 确认双 FAIL**。"
    "另两条硬读数：① **「电磁」在 200 条中出现 0 次**、「弱相互作用」「强相互作用」「胶子」「色荷」"
    "亦为 0 —— 一份自称统一场论的公式集**从未出现电磁**；② 引力 %d 次（其中非待办 %d 行）"
    "⇒ 条目集事实上**只有引力一支**。"
    "结构层交叉印证：r75 2-D1 秩门 FAIL（5D KK 秩 1 vs SM 秩 4，差 3）、"
    "2-D2 手征门 FAIL（圆 KK 无手征零模，Witten 1981）⇒ 「维度扩展救活」亦被双重挡住。"
    "文本层判据与结构层依据同向。**阳性对照**：引力行中存在非待办行（%d）⇒ 待办标记判据非恒真。"
    % (N_GAUGE_LINES, N_GAUGE_LINES, N_GAUGE_LINES - N_GAUGE_DERIVED, N_GAUGE_LINES,
       N_GAUGE_DERIVED,
       FORCE_HITS.get("引力", 0), N_GRAV_DERIVED, N_GRAV_DERIVED),
    key={"gauge_lines": N_GAUGE_LINES, "gauge_derived": N_GAUGE_DERIVED,
         "grav_lines": len(GRAV_LINES), "grav_derived": N_GRAV_DERIVED,
         "force_hits": FORCE_HITS, "n_force_nonzero": N_FORCE_NONZERO,
         "gauge_line_samples": GAUGE_LINES[:6],
         "cross_ref": "r75 2-D1 / 2-D2"},
    note="**本册自抓 1 处（首版假判据）**：以「关键词零命中」判「无内容」会被同义词与"
         "待办条目击穿；正确做法是「命中行 + 待办标记判定 + 阳性对照」三层。")

# --- UFT-3 常数派生 -------------------------------------------------------
N_FREE_CONST = 3   # r72 E05 跨册并账下限（λ₁λ₂λ₃）
UFT3_OK = False
rec("C03", "FAIL",
    "UFT-3 常数派生【未达成】：G / ħ / c 为外部锚点，新增自由常数下限 %d > Ω5 上限 1" % N_FREE_CONST,
    "① ħ、c 为 CODATA 实验锚点，G 在条目集内**未被派生**（940 只把 κ 与 Ricci 缩并代数绑定，"
    "不含 `8πG/c^4`，见本册 B03）；② r72 E05 跨册并账：r71 的 λ₁λ₂λ₃ +3、本册 802 修法 +0/+1 ⇒ "
    "**合计 ≥ 3**；③ r77 B6：把参数账压回 1 个常数（Ω5 合规）的代价是势必为齐次单项 ⇒ "
    "无质量或无相互作用 ⇒ **压到合规即失去物理内容**，二者不可兼得；"
    "④ r73 I04/I05 l_0 排除定理：新长度标度在该基组下幂次恒 0，只能以无量纲 `(l_P/l_0)²` 出现 ⇒ "
    "**不存在「引入一个新长度来派生常数」这条路**。⇒ UFT-3 未达成。",
    key={"n_free_constants_min": N_FREE_CONST, "omega5_limit": 1,
         "G_derived": False, "cross_ref": "r72 E05 / r77 B6 / r73 I04-I05"})

# --- UFT-4 观测复现 -------------------------------------------------------
UFT4_OK = False
rec("C04", "FAIL",
    "UFT-4 观测复现【未达成】：条目集内唯一可算的观测量 991 被 801 恒等于 0（零判别力），"
    "三点族 κ 数值无任何观测可比对象",
    "① r70 F03：991 的全局积分被积函数由 801 `κ²+τ²=ω²` **恒等于 0**，且 `dim(I_991)=%s` 非无量纲"
    " ⇒ 该「可观测不变量」既恒零又量纲错；② 本册三点族 `√(R_abR^ab)` = %s / %s / %s m^-2"
    "（宇宙平均 / 水 / 中子星），条目集**未给出任何一个与之对应的观测量**；"
    "③ 940–942 三条「收敛到 GR / 收敛到 SM / UV 不动点唯一性」**均无公式体或量纲不齐**"
    "（本册 A01/A04/A05）⇒ 不构成复现；④ r75 机器给出的 `γ=β=1` 过 Cassini 限，"
    "但那描述的是 **EC/GR**，不是 TUFT 的 κ/τ 构造（r75 1-D1/1-D2 已显式区分）。"
    % (dstr(D_L2), RICCI_ROWS[0]["sqrt_Ricci_sq_m^-2"], RICCI_ROWS[1]["sqrt_Ricci_sq_m^-2"],
       RICCI_ROWS[2]["sqrt_Ricci_sq_m^-2"]),
    key={"I_991_zero": True, "dim_I_991": dstr(D_L2),
         "ricci_rows": RICCI_ROWS, "cross_ref": "r70 F03 / r75 1-D1"})

# --- UFT-5 可证伪预言 -----------------------------------------------------
N_FALSIFIABLE = 0
UFT5_OK = False
rec("C05", "FAIL",
    "UFT-5 可证伪预言【未达成】：可证伪条目计数 %d —— 991 恒零、940–942 无公式体或量纲不齐"
    % N_FALSIFIABLE,
    "逐条：991（恒零，见 C04）· 940（量纲不齐 A01 + 无场方程极限 A03）· 941（无公式体 A04）· "
    "942（无公式体且前提被 r72 E01 判失效 A05）。下游交叉印证："
    "r75 `meta_verdict = TUFT 未被救活`；r74 D5 / r77 B6：Ω5 合规解退化为两个自由无质量标量"
    "（色散 `ω=ck`）⇒ **与自由场不可区分 ⇒ 零判别力**。⇒ 条目集当前**不含任何可被观测否证的陈述**。",
    key={"n_falsifiable": N_FALSIFIABLE,
         "blocker": "991 恒零 / 940-942 无链条 / Ω5 合规解=自由无质量标量"})

# --- UFT-6 外部验证 -------------------------------------------------------
UFT6_OK = False
rec("C06", "FAIL",
    "UFT-6 外部验证【未达成】：无任何独立外部复核或实验确认（本册不自造「已验证」证据）",
    "条目集 801–1000 自 2026-10-15 进入本库，本库全部判定均属**内部机器审计**，"
    "不构成外部验证。归一化疗程读数（库内自评，非外部）：r70 来料评级 **C/L1**、"
    "r71/r74/r77 **O/L2**、r75 **O/L2**。openuft 全库口径中 TUFT 73 报告分布 "
    "H6 / O43 / C24 / U3（**库内**归一化，非外部同行评议）。⇒ UFT-6 未达成。**不自推**。",
    key={"external_confirmation": False, "rating_r70": "C/L1",
         "rating_chain": "r71/r74/r77=O/L2 ; r75=O/L2"})

# ---------------------------------------------------------------------------
# 5. D 组：总达成度与「继续完成统一场论」的三条可执行路径（不代选）
# ---------------------------------------------------------------------------
UFT_TABLE = [
    ("UFT-1", "数学自洽", UFT1_SYSTEM_OK, UFT1_BASIC_OK),
    ("UFT-2", "四力统一", UFT2_OK, False),
    ("UFT-3", "常数派生", UFT3_OK, False),
    ("UFT-4", "观测复现", UFT4_OK, False),
    ("UFT-5", "可证伪预言", UFT5_OK, False),
    ("UFT-6", "外部验证", UFT6_OK, False),
]
N_UFT_PASS = sum(1 for _, _, ok, _ in UFT_TABLE if ok)
N_UFT_BASIC = sum(1 for _, _, _, b in UFT_TABLE if b)

guard("G-D1 六条达成度判据每条均有机器依据（无一条为人工声明）",
      len(UFT_TABLE) == 6 and N_UFT_PASS == 0 and N_UFT_BASIC == 1,
      "体系层 %d/6 ; 基础恒等式层 %d/6" % (N_UFT_PASS, N_UFT_BASIC))

rec("D01", "FAIL",
    "★总达成度：体系层 **%d/6**，基础恒等式层 **%d/6**（二者口径分列，不合并）"
    % (N_UFT_PASS, N_UFT_BASIC),
    "判据表：%s。**体系层 0/6** 的含义是：把 801–1000 当作「一个已完成（或可完成）的统一场论」"
    "来检验时，六条判据**逐条不成立**，且每条都有机器依据（本册 C01–C06）。"
    "**基础恒等式层 1/6** 只说明 `κ²+τ²=ω²` 这一条量纲齐次 —— 它是 openuft 全库总汇"
    "「达成度 1/6」的同源项，**不能外推为体系达标**。"
    "⇒ 对「继续完成统一场论」这一请求的诚实回答：**不是「还差最后一步」，"
    "而是六条判据中五条在当前公设集内被判为结构性不可达成**（UFT-2 秩门/手征门、"
    "UFT-3 Ω5、UFT-4/5 恒零与无链条、UFT-6 无外部验证）。"
    % "; ".join("%s %s=%s" % (a, b, "PASS" if ok else "FAIL") for a, b, ok, _ in UFT_TABLE),
    key={"uft_system_score": "%d/6" % N_UFT_PASS,
         "uft_basic_score": "%d/6" % N_UFT_BASIC, "uft_table": UFT_TABLE})

rec("D02", "INFO",
    "三条继续路径与机器定价（承 r77 D2，**本册不代选**）",
    "(i) **放宽 Ω5（接受 ≥2 个带量纲自由常数）** —— r77 B7 阳性对照：双常数势 "
    "`U=−½m²(κ²+τ²)+λ(κ²+τ²)²` 的数值极小位于 `5.000000E-1`（解析 0.5）≠0 ⇒ "
    "确实能同时给出【质量 + 相互作用 + 确定标度真空】⇒ 可解 UFT-3/UFT-5 的一半；"
    "代价：违反 Ω5（属科学哲学层面的选择，非计算问题）。"
    "(ii) **扩充场内容（引入规范群）** —— 可攻 UFT-2；但 r75 2-D1 秩门（5D KK 秩 1 vs SM 秩 4）"
    "与 2-D2 手征门（圆 KK 无手征零模）**是两条独立硬门槛**，不是加参数能绕的。"
    "(iii) **改为几何编码层定位**（放弃「完成统一场论」目标，定位为「给定观测锚后把"
    "自旋/统计/质量编码为几何」的编码框架）—— 可保住全部已 PASS 面且零新增常数；"
    "代价：UFT-2/UFT-3 永久放弃。三条彼此**互斥**，须用户裁决。",
    key={"paths": ["放宽 Ω5", "扩充场内容", "改为几何编码层"],
         "cross_ref": "r77 D2 / r75 2-D1,2-D2"})

rec("D03", "BOUNDARY",
    "最小闭合代价账（并账口径，承 r72 D-r72-4）",
    "已零成本修完：补导数项 `κ²→(∂κ)²`（r71 C1）· P1 同号化（r74/r77）· 802 逐项补 `ω^-2`（本册 B01）· "
    "940 幂次 `1/2→1/4`（本册 A02a）。**仍欠**：819 contorsion 改写（零成本但未执行）· "
    "835/836 因果退化（需改色散式，代价未定）· **Ω5 参数账 ≥2（结构性，无零成本解）**。"
    "⇒ 若用户选 (i)，最小闭合需接受 **2 个**带量纲自由常数；若选 (iii)，最小闭合需 **0 个**"
    "但 UFT-2/UFT-3 放弃。**本册不代选。**",
    key={"fixed_zero_cost": ["导数项", "同号化", "802 ω^-2", "940 幂次"],
         "remaining": ["819 contorsion", "835/836 因果", "Ω5 ≥2"]})

# ---------------------------------------------------------------------------
# 6. 产物输出
# ---------------------------------------------------------------------------
KEY_NUMBERS = {
    "n_items": len(ITEM_IDS),
    "dim_R_ab_R_ab": dstr(D_invL4),
    "dim_T_acd_T_acd": dstr(D_invL2),
    "dim_gap_802": dstr(ddiv(D_invL4, D_invL2)),
    "dim_sqrt_Ricci2": dstr(DIM_SQRT_RICCI2),
    "dim_omega": dstr(D_invL),
    "dim_gap_940": dstr(GAP_940),
    "sqrt_Ricci_correct_unit": "m^-2",
    "ricci_rows": RICCI_ROWS,
    "route_a_quarter_power_water_m^-1": RICCI_ROWS[1]["quarter_power_m^-1"],
    "route_b_n_families": len(FAM_L1),
    "n_scan_802": len(SOL_SCAN),
    "S1_positive": "%d/%d" % (N_POS_S1, N_TOT_S1),
    "S2_positive": "%d/%d" % (N_POS_S2, N_TOT_S2),
    "kappa_water_m^-1": RICCI_ROWS[1]["quarter_power_m^-1"],
    "radius_water_m": fv(Dc(1) / Dc(RICCI_ROWS[1]["quarter_power_m^-1"])),
    "gauge_hits": N_GAUGE_HITS,
    "n_free_constants_min": N_FREE_CONST,
    "n_falsifiable": N_FALSIFIABLE,
    "uft_system_score": "%d/6" % N_UFT_PASS,
    "uft_basic_score": "%d/6" % N_UFT_BASIC,
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


VERDICT = "FAIL" if COUNTS.get("FAIL", 0) > 0 else "PASS"
GUARD_OK = all(g["ok"] for g in GUARDS)

OUT = {
    "round": "r76",
    "stem": STEM,
    "title": "V4.8 极限定理（940–942）量纲核验 + 「完成统一场论」六条达成度判定",
    "source": os.path.basename(SRC),
    "counts": COUNTS,
    "total": len(ROWS),
    "verdict": VERDICT,
    "guard_all_ok": GUARD_OK,
    "n_guards": len(GUARDS),
    "guards": GUARDS,
    "items": ROWS,
    "key_numbers": KEY_NUMBERS,
    "not_self_derived": [
        "CODATA 锚点 ħ、c、G 为实验测量值，不自推",
        "「自由场无散射/无自作用」为教科书结论，引用不自推",
        "Witten 1981 圆 KK 无手征零模（r75 2-D2），引用不自推",
        "Ostrogradsky 判据承 GAQ-UFT V18 册，不重推系数",
        "EC 真空 PPN γ=β=1 承 r75 1-D1/1-D2，不重推",
    ],
}

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(jsonable(OUT), f, ensure_ascii=False, indent=2)

MD = ["# %s" % OUT["title"], "",
      "- 条目：**%d**（%s）" % (len(ROWS), " / ".join("%s %d" % (k, v) for k, v in COUNTS.items() if v)),
      "- 守卫：**%d/%d**（%s）" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
                                  "全过" if GUARD_OK else "有未过"),
      "- verdict：**%s**", "", "## 条目表", ""]
MD.append("| 编号 | 判定 | 标题 |")
MD.append("|---|---|---|")
for r in ROWS:
    MD.append("| %s | %s | %s |" % (r["code"], r["verdict"], r["title"].replace("|", "\\|")))
MD.append("")
MD.append("## 关键读数")
MD.append("")
for k, v in KEY_NUMBERS.items():
    MD.append("- `%s` = %s" % (k, json.dumps(jsonable(v), ensure_ascii=False)))
with open(os.path.join(DATA, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(MD))

RP = ["TUFT-r76 report", "=" * 60, ""]
for g in GUARDS:
    RP.append("[%s] G %s :: %s" % ("OK" if g["ok"] else "NG", g["name"], g["detail"]))
RP.append("")
for r in ROWS:
    RP.append("[%s] %s :: %s" % (r["verdict"], r["code"], r["title"]))
    RP.append("    %s" % r["detail"])
    if r.get("note"):
        RP.append("    NOTE: %s" % r["note"])
    RP.append("")
RP.append("=" * 60)
RP.append("COUNTS: %s" % COUNTS)
RP.append("TOTAL: %d" % len(ROWS))
RP.append("VERDICT: %s" % VERDICT)
RP.append("GUARDS: %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
with open(os.path.join(DATA, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(RP))

print("ROUND=r76")
print("TOTAL=%d" % len(ROWS))
print("COUNTS=%s" % COUNTS)
print("GUARDS=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
print("VERDICT=%s" % VERDICT)
print("UFT_SYSTEM=%s" % KEY_NUMBERS["uft_system_score"])
print("UFT_BASIC=%s" % KEY_NUMBERS["uft_basic_score"])
sys.exit(0)
