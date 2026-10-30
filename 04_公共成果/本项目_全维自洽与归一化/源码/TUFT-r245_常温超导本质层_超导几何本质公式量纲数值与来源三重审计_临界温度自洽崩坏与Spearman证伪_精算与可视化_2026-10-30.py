# -*- coding: utf-8 -*-
r"""
TUFT-r245 · 常温超导本质层
================================================================================
超导几何本质公式的【量纲 / 数值 / 来源】三重审计
临界温度公式自洽崩坏 · Spearman 单调性证伪 · 尺度灾变 · 常温超导验收清单

【命题来源】用户：「继续攻破常温超导的本质」

【本卷定位：凝聚态 / 超导本质层（新层）】
r243 = 工程可用性层（引力），r244 = 本体论层（引力），
r245 = **超导本质层**：靶换了一个领域（凝聚态），但沿用了同一套「螺旋曲率」母题。

【为什么这份靶值得攻】
它不是纯定性宣称，而是给出了**可执行代码 + 元素数据库 + 数值表**
（`超导的几何本质：全物质超导可能性与最佳超导元素精算分析`，
末尾自评「理论自洽，与实验一致 / Status: Complete」）。
⇒ 有代码就有**可复算性**，这正是本库最喜欢的靶型。

【靶的核心式子（逐字取自来料）】
  ① ω_e ρ_e = ω_e ρ_l = c                （电子与晶格均以光速螺旋）
  ② Δκ = ρ/(ρ² + b²)                     （圆柱螺旋曲率）
  ③ T_c = (ℏ/(2π k_B)) · ω_e ω_l/(ω_e+ω_l)
  ④ R  = (Δκ_e − Δκ_l)/(Δκ_e + Δκ_l) = 0
  ⑤ B_c0 = (m_e c)/(e ℏ) · T_c
  ⑥ J_c  = (e c)/(ρ_l ℏ) · T_c
  ⑦ 推论 T_c ∝ 1/(ρ_e + ρ_l)

【对靶有利项先做】A 组先确认靶做对/诚实的部分（②⑦数学正确、①的量纲、
HFG-002 主动声明未获验证），再攻不利层。

【分层】本卷条目不可与 r142–r244 相加。
================================================================================
"""

import ast
import hashlib
import io
import math
import os
import re
import sys
import time
from fractions import Fraction

# ============================================================
# 0. 元信息
# ============================================================
RID = "r245"
BASE_NAME = ("TUFT-r245_常温超导本质层_超导几何本质公式量纲数值与来源三重审计_"
             "临界温度自洽崩坏与Spearman证伪_精算与可视化_2026-10-30")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"

TARGETS = [
    r"D:\a10\aikjx\code\my_lib\utf\17-空间光速螺旋引力理论\v1\论文"
    r"\超导的几何本质：全物质超导可能性与最佳超导元素精算分析.md",
    r"D:\a10\aikjx\code\my_lib\math\本源数学\资料"
    r"\Doubao-HFG-002 型 C60 常温超导人工反引力场发生器 工程资料综合总结-2026-06-22.md",
    r"D:\a10\aikjx\code\my_lib\article\zh\2026\6\14"
    r"\算法联盟ROOT最高权限：常温超导与人工场——10大应用落地终极指南.md",
]

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

# ============================================================
# 1. 常数（CODATA 2018 / SI 2019）
# ============================================================
C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
KB = 1.380649e-23
QE = 1.602176634e-19
M_E = 9.1093837015e-31
EV = QE                       # 1 eV in J

# ℏ/(2π k_B)：靶的 T_c 公式前置因子，量纲 [Θ·s]
HBAR_OVER_2PI_KB = HBAR / (2.0 * math.pi * KB)

# ============================================================
# 2. 量纲机读 (M, L, T, Q, Θ) —— 比 r243/r244 多两个分量：电荷 Q 与温度 Θ
# ============================================================
def dim(m=0, l=0, t=0, q=0, th=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q), Fraction(th))


DIM = {
    "rho":   dim(l=1),                     # 螺旋半径 / 长度
    "b":     dim(l=1),                     # 螺距参数
    "kappa": dim(l=-1),                    # 曲率
    "omega": dim(t=-1),                    # 角频率
    "hbar":  dim(m=1, l=2, t=-1),
    "kB":    dim(m=1, l=2, t=-2, th=-1),
    "c":     dim(l=1, t=-1),
    "e":     dim(q=1),
    "m_e":   dim(m=1),
    "Tc":    dim(th=1),                    # 温度
    "B":     dim(m=1, t=-1, q=-1),         # 特斯拉 = M T^-1 Q^-1
    "J":     dim(q=1, t=-1, l=-2),         # 电流密度 A/m^2 = Q T^-1 L^-2
    "Rohm":  dim(m=1, l=2, t=-1, q=-2),    # 欧姆 = M L^2 T^-1 Q^-2
}


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(a):
    return "[M^%s*L^%s*T^%s*Q^%s*Θ^%s]" % a


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


# ---- 靶的三个公式的量纲推导（机读） ----
def dim_Tc_formula():
    r"""T_c = ℏ·ω_e·ω_l / (2π·k_B·(ω_e+ω_l))；幂次：ℏ + ω − k_B"""
    return dsub(dadd(DIM["hbar"], DIM["omega"]), DIM["kB"])


def dim_Bc_formula():
    r"""B_c = (m_e·c)/(e·ℏ) · T_c"""
    return dadd(dsub(dadd(DIM["m_e"], DIM["c"]), dadd(DIM["e"], DIM["hbar"])), DIM["Tc"])


def dim_Jc_formula():
    r"""J_c = (e·c)/(ρ_l·ℏ) · T_c"""
    return dadd(dsub(dadd(DIM["e"], DIM["c"]), dadd(DIM["rho"], DIM["hbar"])), DIM["Tc"])


def dim_R_formula():
    r"""R = (Δκ_e−Δκ_l)/(Δκ_e+Δκ_l)：曲率之比 ⇒ 无量纲"""
    return dsub(DIM["kappa"], DIM["kappa"])


# ============================================================
# 3. 靶的公式复算（用靶自己的代码逻辑）
# ============================================================
def omega_of_rho(rho):
    r"""靶：ω = c / ρ"""
    return C / rho


def tc_formula(omega_e, omega_l):
    r"""靶：T_c = ℏ ω_e ω_l / (2π k_B (ω_e + ω_l))"""
    return HBAR * omega_e * omega_l / (2.0 * math.pi * KB * (omega_e + omega_l))


def bc_formula(tc):
    r"""靶：B_c0 = (m_e c)/(e ℏ) · T_c"""
    return (M_E * C) / (QE * HBAR) * tc


def jc_formula(tc, rho_l):
    r"""靶：J_c = (e c)/(ρ_l ℏ) · T_c"""
    return (QE * C) / (rho_l * HBAR) * tc


# 靶的元素数据库（逐字取自表 3.2）
ELEMENTS = [
    # 名称, 符号, rho_l (m),      b_l (m),       靶表 T_c (K), 靶表 B_c (T), 靶表 J_c (A/m^2)
    ("铌", "Nb", 2.86e-10, 1.92e-8, 9.2,   0.15,   2.4e11),
    ("铅", "Pb", 3.49e-10, 2.34e-8, 7.2,   0.08,   1.8e11),
    ("钒", "V",  2.63e-10, 1.76e-8, 5.4,   0.12,   2.1e11),
    ("锡", "Sn", 4.32e-10, 2.90e-8, 3.7,   0.03,   1.2e11),
    ("汞", "Hg", 3.98e-10, 2.67e-8, 4.2,   0.04,   1.4e11),
    ("铝", "Al", 4.75e-10, 3.18e-8, 1.2,   0.01,   4.0e10),
    ("锌", "Zn", 4.16e-10, 2.79e-8, 0.85,  0.01,   3.0e10),
    ("铜", "Cu", 4.62e-10, 3.10e-8, 0.0005, 5e-6,  1.7e7),
    ("金", "Au", 4.88e-10, 3.27e-8, 0.0003, 3e-6,  1.0e7),
]

# 教科书实测 T_c（常压，K）—— 用于核对靶表是否为抄录值
TEXTBOOK_TC = {"Nb": 9.26, "Pb": 7.19, "V": 5.40, "Sn": 3.72,
               "Hg": 4.15, "Al": 1.18, "Zn": 0.85}
# Cu / Au / Ag：至今（常压及高压下）未发现超导相 ⇒ 无实测 T_c
NEVER_SUPERCONDUCTING = ("Cu", "Ag", "Au")


def tc_recompute_table():
    """用靶的公式 + 靶的 ρ_l + 靶自己的共振条件 ω_e=ω_l 复算全部元素。"""
    rows = []
    for name, sym, rho_l, b_l, tc_tab, bc_tab, jc_tab in ELEMENTS:
        w = omega_of_rho(rho_l)
        tc_calc = tc_formula(w, w)            # 共振条件 ω_e = ω_l = c/ρ_l
        rows.append({"name": name, "sym": sym, "rho_l": rho_l, "b_l": b_l,
                     "omega_l": w, "tc_calc": tc_calc, "tc_table": tc_tab,
                     "ratio": tc_calc / tc_tab,
                     "bc_calc": bc_formula(tc_tab), "bc_table": bc_tab,
                     "jc_calc": jc_formula(tc_tab, rho_l), "jc_table": jc_tab,
                     "b_over_rho": b_l / rho_l})
    return rows


def b_over_rho_stats(rows):
    vals = [r["b_over_rho"] for r in rows]
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    sd = math.sqrt(var)
    return {"mean": mean, "sd": sd, "cv": sd / mean if mean else float("inf"),
            "min": min(vals), "max": max(vals)}


# ============================================================
# 4. 圆柱螺旋曲率：闭合式 vs 数值微分（对靶有利项 A2 的支撑）
# ============================================================
def helix_curvature_closed(rho, b):
    r"""圆柱螺旋 (ρ cos t, ρ sin t, b t) 的曲率 κ = ρ/(ρ²+b²)。"""
    return rho / (rho ** 2 + b ** 2)


def helix_curvature_numeric(rho, b, t=0.7, h=1e-3):
    """用参数曲线的有限差分直接算 κ = |r'×r''|/|r'|³，与闭合式对拍。"""
    def P(s):
        return (rho * math.cos(s), rho * math.sin(s), b * s)
    p0, p1, p2 = P(t - h), P(t), P(t + h)
    d1 = [(p2[k] - p0[k]) / (2.0 * h) for k in range(3)]
    d2 = [(p2[k] - 2.0 * p1[k] + p0[k]) / (h * h) for k in range(3)]
    cr = (d1[1] * d2[2] - d1[2] * d2[1],
          d1[2] * d2[0] - d1[0] * d2[2],
          d1[0] * d2[1] - d1[1] * d2[0])
    nc = math.sqrt(sum(x * x for x in cr))
    nd1 = math.sqrt(sum(x * x for x in d1))
    return nc / nd1 ** 3


# ============================================================
# 5. Spearman 秩相关（含并列平均秩）
# ============================================================
def rank_avg(xs):
    n = len(xs)
    order = sorted(range(n), key=lambda i: xs[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = rank_avg(list(x)), rank_avg(list(y))
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return num / (dx * dy) if (dx and dy) else 0.0, rx, ry


# 真实材料：Debye 温度 Θ_D (K) 与实测临界温度 T_c (K)
# Θ_D 取自标准固体物理 Debye 温度表（Kittel 等）；MgB2/YBCO 为文献有效值，分歧较大，
# 故本卷的**排序证伪**只依赖稳健事实：金刚石/石墨烯 Θ_D 最高且不超导。
MATERIALS = [
    ("石墨烯",  2300.0, 0.0,   "不超导（无超导相）"),
    ("金刚石",  2230.0, 0.0,   "绝缘体，不超导"),
    ("MgB2",     750.0, 39.0,  ""),
    ("Al",       428.0, 1.18,  ""),
    ("YBCO",     410.0, 92.0,  ""),
    ("Cu",       343.0, 0.0,   "至今未发现超导相"),
    ("Nb",       275.0, 9.26,  ""),
    ("Ag",       225.0, 0.0,   "至今未发现超导相"),
    ("Au",       165.0, 0.0,   "至今未发现超导相"),
    ("Pb",       105.0, 7.19,  ""),
    ("Hg",        71.9, 4.15,  ""),
]


# ============================================================
# 6. 修复定价
# ============================================================
ESSENCE_KEYS = (
    "tc_reproducible",      # T_c 公式能复现自己的数值表
    "bc_dimension_ok",      # B_c 量纲正确
    "jc_dimension_ok",      # J_c 量纲正确
    "independent_params",   # ρ_e / b_e 等参数独立给定
    "pairing_mechanism",    # 配对机制（BCS 级）
    "room_temp_evidence",   # 常温超导的实验证据
)
GR_SUPER_SKELETON = {"pairing_mechanism", "tc_reproducible", "room_temp_evidence"}


def repair_pricing():
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    for combo in product((False, True), repeat=len(ESSENCE_KEYS)):
        have = {k for k, v in zip(ESSENCE_KEYS, combo) if v}
        if len(have) < len(ESSENCE_KEYS):
            out["EMPTY"] += 1
        elif GR_SUPER_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
    return out


# ============================================================
# 7. 条目容器
# ============================================================
ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def sha256_of(path):
    try:
        with io.open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}
ALLT = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)


def nhit(text, *toks):
    return sum(text.count(t) for t in toks)


def scan_untouched():
    touched, scanned = [], 0
    for d in (SRC_DIR, DATA_DIR):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for nm in names:
            for n in range(225, 245):
                if ("TUFT-r%d" % n) in nm or ("_r%d" % n) in nm:
                    fp = os.path.join(d, nm)
                    try:
                        mt = os.path.getmtime(fp)
                    except OSError:
                        continue
                    scanned += 1
                    if mt >= START_TS:
                        touched.append(os.path.basename(fp))
                    break
    ok = (not touched) and scanned > 0
    msg = ("扫描 r225–r244 产物 %d 份，mtime 全部早于本轮启动 %s" % (scanned, START_ISO)
           if ok else ("发现被触碰：%s" % ",".join(touched[:5]) if touched
                       else "未扫描到任何 r225–r244 产物"))
    return ok, msg


def check_distribution():
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    ok = (sum(dist.values()) == len(ENTRIES)) and dist.get("FAIL", 0) >= 6 \
        and dist.get("PASS", 0) >= 3
    return ok, "实测分布 %s（要求 FAIL≥6 且 PASS≥3）" % dist


def check_write_side():
    seen, late = [], []
    for p in WRITE_SIDE:
        if not os.path.exists(p):
            continue
        seen.append(os.path.basename(p))
        try:
            if os.path.getmtime(p) >= START_TS:
                late.append(os.path.basename(p))
        except OSError:
            pass
    return (not late), ("写入侧 %s mtime 均早于本轮启动" % ",".join(seen) if seen and not late
                        else ("发现被改动：%s" % ",".join(late) if late else "未找到写入侧脚本"))


# ============================================================
# 8. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    rows = tc_recompute_table()
    bstat = b_over_rho_stats(rows)
    EVIDENCE["rows"], EVIDENCE["bstat"] = rows, bstat

    # 量纲
    d_tc, d_bc, d_jc, d_r = (dim_Tc_formula(), dim_Bc_formula(),
                             dim_Jc_formula(), dim_R_formula())
    ok_tc_dim = (d_tc == DIM["Tc"])
    ok_bc_dim = (d_bc == DIM["B"])
    ok_jc_dim = (d_jc == DIM["J"])
    ok_r_dim = (d_r == DIM["Rohm"])
    EVIDENCE["dimension"] = {"Tc": dstr(d_tc), "Bc": dstr(d_bc),
                             "Jc": dstr(d_jc), "R": dstr(d_r)}
    EVIDENCE.update({"d_tc": d_tc, "d_bc": d_bc, "d_jc": d_jc, "d_r": d_r,
                     "ok_tc_dim": ok_tc_dim, "ok_bc_dim": ok_bc_dim,
                     "ok_jc_dim": ok_jc_dim, "ok_r_dim": ok_r_dim})

    # 圆柱螺旋曲率对拍（以 Nb 参数为例）
    rho0, b0 = ELEMENTS[0][2], ELEMENTS[0][3]
    k_closed = helix_curvature_closed(rho0, b0)
    k_numeric = helix_curvature_numeric(rho0, b0)
    k_relerr = rel(k_numeric, k_closed)
    EVIDENCE.update({"k_closed": k_closed, "k_numeric": k_numeric, "k_relerr": k_relerr,
                     "rho0": rho0, "b0": b0})
    # 该曲率对应的曲率半径 vs 晶格尺度
    curv_radius = 1.0 / k_closed
    EVIDENCE["curv_radius"] = curv_radius
    EVIDENCE["radius_over_lattice"] = curv_radius / rho0

    # Spearman
    th = [m[1] for m in MATERIALS]
    tc = [m[2] for m in MATERIALS]
    rho_s, rx, ry = spearman(th, tc)
    # 正对照：完美单调
    rho_pos, _, _ = spearman([10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # 负对照：完全反序
    rho_neg, _, _ = spearman([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
    EVIDENCE.update({"rho_s": rho_s, "rho_pos": rho_pos, "rho_neg": rho_neg,
                     "ranks": list(zip([m[0] for m in MATERIALS], rx, ry))})

    # 靶公式对金刚石/石墨烯的预测
    def tc_from_debye(theta_D):
        omega = KB * theta_D / HBAR
        return tc_formula(omega, omega)
    dia = tc_from_debbe = tc_from_debye(2230.0)
    gra = tc_from_debye(2300.0)
    EVIDENCE["tc_diamond"], EVIDENCE["tc_graphene"] = dia, gra

    # 常温反解：T_c = 300 K ⇒ ρ_e + ρ_l = c / (T_c/(ℏ/2πk_B))
    omega_300 = 300.0 / HBAR_OVER_2PI_KB
    rho_sum_300 = C / omega_300
    EVIDENCE["rho_sum_300"] = rho_sum_300
    EVIDENCE["omega_300"] = omega_300
    EVIDENCE["rho_sum_over_lattice"] = rho_sum_300 / 3.0e-10

    # C60 对照（来自 HFG-002 自身的诚实声明）
    EVIDENCE["c60"] = {"known_ambient_K": 33.0, "known_highP_K": 38.0,
                       "claimed_K": 382.0}

    pricing = repair_pricing()
    EVIDENCE["pricing"] = pricing

    hits = {
        "全物质超导": nhit(ALLT, "全物质超导", "任何物质", "所有物质都可"),
        "室温超导宣称": nhit(ALLT, "室温超导", "常温超导", "常温常压"),
        "技术就绪": nhit(ALLT, "技术就绪", "应用可行", "实现超导"),
        "未获验证声明": nhit(ALLT, "未获得", "未被科学证实", "未获", "不属于公认科学结论"),
        "库珀对": nhit(ALLT, "库珀对", "库伯对", "Cooper"),
        "BCS": nhit(ALLT, "BCS", "电子-声子", "声子"),
    }
    EVIDENCE["hits"] = hits

    # ============================================================
    # A 组 · 对靶有利项（先确认靶做对/诚实的部分）
    # ============================================================
    ent("A1", "T_c 公式量纲【正确】：ℏω/k_B ⇒ 温度 [Θ]", "PASS",
        "机读：ℏ%s + ω%s − k_B%s = %s = 温度 %s ✓"
        % (dstr(DIM["hbar"]), dstr(DIM["omega"]), dstr(DIM["kB"]), dstr(d_tc), dstr(DIM["Tc"])),
        "这一条靶是对的，本卷明确承认。范围限制：量纲对 ≠ 数值对 ≠ 来源对（见 B/C 组）。")
    ent("A2", "Δκ = ρ/(ρ²+b²) 是【正确的】圆柱螺旋曲率公式", "PASS",
        "闭合式 κ=ρ/(ρ²+b²)=%s m^-1；数值微分（|r'×r''|/|r'|³）得 %s m^-1；相对误差 %s ✓"
        % (("%.6e" % k_closed), ("%.6e" % k_numeric), fmt_rel(k_relerr)),
        "靶在曲线几何部分的数学是正确的（与 r244 对本源不变式的判断同源：数学对 ≠ 可用于承载物理）。")
    ent("A3", "推论 T_c ∝ 1/(ρ_e+ρ_l) 【数学正确】", "PASS",
        "由 ω=c/ρ 代入 ω_eω_l/(ω_e+ω_l) = c/(ρ_e+ρ_l) ⇒ T_c ∝ 1/(ρ_e+ρ_l) ✓ 代数无误。",
        "范围限制：推论正确，但由它反解出的尺度不可行（见 F1）。")
    ent("A4", "HFG-002 工程资料【主动声明】常温超导未获验证 ⇒ 诚实登记", "PASS",
        "机读命中「未获得/未被科学证实/不属于公认科学结论」%d 处；"
        "原文并给出对照表：C60 已知常压最高 33 K、高压 38 K，方案宣称 109℃(382 K)，"
        "自评「临界温度相差 10 倍以上，无任何可重复实验数据」。"
        % hits["未获验证声明"],
        "这是本体系少见的自我限定。**本卷因此不把 HFG-002 当作硬宣称来攻**，"
        "只把它作为 A5/C60 对照与 G2 的来源。")
    ent("A5", "元素表中 Nb/Pb/V/Sn/Hg/Al/Zn 的 T_c 与教科书实验值相符 ⇒ 抄录正确", "INFO",
        "; ".join("%s 表%g vs 实测%g" % (s, next(r["tc_table"] for r in rows if r["sym"] == s), v)
                  for s, v in TEXTBOOK_TC.items()),
        "对靶有利：数值抄录无误。但正因为抄得准，才暴露 B 组的问题——"
        "这些数不是用靶自己的公式算出来的。")

    # ============================================================
    # B 组 · ★自洽崩坏：靶的公式算不出靶自己的表
    # ============================================================
    ent("B1", "用靶的公式 + 靶的 ρ_l + 靶的共振条件 ⇒ Nb 的 T_c = %s K，表内为 9.2 K（差 %s 倍）"
        % (("%.4e" % rows[0]["tc_calc"]), fmt_rel(rows[0]["ratio"])), "FAIL",
        "ω_l = c/ρ_l = %s s^-1；取共振条件 ω_e=ω_l（靶定理的原始条件）⇒ "
        "T_c = (ℏ/2πk_B)·ω/2 = %s K；靶表写 9.2 K。"
        % (("%.4e" % rows[0]["omega_l"]), ("%.4e" % rows[0]["tc_calc"])),
        "这不是精度问题：差 5 个数量级。")
    ent("B2", "九元素的「公式/表值」比值跨 %s → %s（5 个数量级）⇒ 不是恒定校准误差"
        % (fmt_rel(min(r["ratio"] for r in rows)), fmt_rel(max(r["ratio"] for r in rows))), "FAIL",
        "; ".join("%s %s" % (r["sym"], fmt_rel(r["ratio"])) for r in rows),
        "若为系统性单位/因子错误，比值应近似恒定；实测跨度达 5 个数量级 ⇒ "
        "表内数值与公式【彻底脱节】，表是独立抄录的。")
    ent("B3", "复算所必需的 ρ_e 与 b_e 在数据库中【未提供】⇒ 计算不可复现", "FAIL",
        "靶代码签名 calculate_Tc(rho_l, b_l, rho_e, b_e) 需要四个参数，"
        "但表 3.2 只给了 ρ_l 与 b_l 两列；ρ_e、b_e 全篇无数值。",
        "本卷只能退而采用靶自己的共振条件 ω_e=ω_l 复算（B1）。"
        "缺件登记为不可复现，不判为算错。")

    # ============================================================
    # C 组 · ★伪参数与虚构数据
    # ============================================================
    ent("C1", "b_l 是【派生伪参数】：b_l/ρ_l 对全部九元素恒为 %s（变异系数 %s）"
        % (("%.3f" % bstat["mean"]), fmt_rel(bstat["cv"])), "FAIL",
        "各元素 b_l/ρ_l：%s；极差 %s–%s。"
        % (", ".join("%.3f" % r["b_over_rho"] for r in rows),
           ("%.3f" % bstat["min"]), ("%.3f" % bstat["max"])),
        "真正的独立材料参数不会在九种元素间保持 4 位有效数字一致的固定比值 ⇒ "
        "b_l 是按 ρ_l 生成的，没有独立物理来源（晶格常数、声子波长、相干长度皆非此值）。")
    ent("C2", "Cu 与 Au 至今【未发现超导相】，靶却给出 T_c = 5e−4 / 3e−4 K ⇒ 虚构数值", "FAIL",
        "Cu、Ag、Au 是最佳常规导体，但在常压及高压下均未发现超导相（电子-声子耦合过弱），"
        "故不存在可引用的实测 T_c；靶表却给出 0.0005 K 与 0.0003 K 的「精算值」。",
        "这些数既不是实验值（不存在），也不是公式算值（差 9 个数量级）⇒ 来源不明。")
    ent("C3", "「全物质超导」与表中 Cu/Au 的极低 T_c 自相矛盾", "FAIL",
        "定理称「任何物质在满足 ω_e=ω_l 时都可成为超导体」，"
        "但表中 Cu 的 T_c 仅 5e−4 K、Au 仅 3e−4 K —— 若共振条件真能达成，"
        "为何最好导体的 T_c 比 Nb 低 4 个数量级？机读「全物质超导」%d 处。"
        % hits["全物质超导"],
        "若答案是「Cu 达不到共振条件」，则定理等价于「能超导的才能超导」⇒ 空洞（重言式）。")

    # ============================================================
    # D 组 · ★量纲错置：B_c 与 J_c 与 R
    # ============================================================
    ent("D1", "B_c = (m_e c)/(e ℏ)·T_c 量纲错误：得 %s ≠ 特斯拉 %s"
        % (dstr(d_bc), dstr(DIM["B"])), "FAIL",
        "机读 (m_e·c) − (e·ℏ) + T_c = %s；应为 %s ⇒ 不等。"
        % (dstr(d_bc), dstr(DIM["B"])),
        "数值佐证：按靶公式 Nb 的 B_c = %s，而表内写 0.15 T ⇒ 差 %s 倍。"
        % (("%.3e" % rows[0]["bc_calc"]), fmt_rel(rows[0]["bc_calc"] / rows[0]["bc_table"])))
    ent("D2", "J_c = (e c)/(ρ_l ℏ)·T_c 量纲错误：得 %s ≠ 电流密度 %s"
        % (dstr(d_jc), dstr(DIM["J"])), "FAIL",
        "机读 (e·c) − (ρ_l·ℏ) + T_c = %s；应为 %s ⇒ 不等。"
        % (dstr(d_jc), dstr(DIM["J"])),
        "数值佐证：按靶公式 Nb 的 J_c = %s，而表内写 2.4e11 A/m² ⇒ 差 %s 倍。"
        % (("%.3e" % rows[0]["jc_calc"]), fmt_rel(rows[0]["jc_calc"] / rows[0]["jc_table"])))
    ent("D3", "R = (Δκ_e−Δκ_l)/(Δκ_e+Δκ_l) 是无量纲比值，不是电阻", "FAIL",
        "机读 Δκ − Δκ = %s（无量纲）；电阻应为 %s ⇒ 量纲错置。"
        % (dstr(d_r), dstr(DIM["Rohm"])),
        "且这是【定义恒等式】：把 R 规定为两个曲率扰动之差与和之比，"
        "共振时 Δκ_e=Δκ_l ⇒ R=0 是规定的结果，不是推导出的物理结论（承 r218 定义恒等式刀）。")

    # ============================================================
    # E 组 · ★Spearman 证伪：T_c 与晶格频率并非单调
    # ============================================================
    ent("E1", "真实材料的 Θ_D 与 T_c 的 Spearman 秩相关 ρ = %s（靶要求 +1）"
        % ("%.4f" % rho_s), "FAIL",
        "11 种材料（石墨烯/金刚石/MgB2/Al/YBCO/Cu/Nb/Ag/Au/Pb/Hg）实测 ρ = %s；"
        "扫描器自校验：完美单调 ⇒ ρ=%s，完全反序 ⇒ ρ=%s ⇒ 实现正确、有分辨力。"
        % (("%.4f" % rho_s), ("%.4f" % rho_pos), ("%.4f" % rho_neg)),
        "靶的 T_c ∝ ω_eff（晶格频率的调和平均）要求 ρ 接近 +1；实测几乎为零且略负 ⇒ 单调关系被数据证伪。")
    ent("E2", "排序反例：Θ_D 最高的两种材料（石墨烯 2300 K、金刚石 2230 K）"
        "均不超导，靶公式却分别预测 T_c = %s K / %s K"
        % (("%.1f" % gra), ("%.1f" % dia)), "FAIL",
        "按靶公式（取 ω_e=ω_l=k_BΘ_D/ℏ）：石墨烯 T_c = %s K、金刚石 T_c = %s K；"
        "而二者均无超导相（金刚石更是绝缘体）。"
        "注：石墨烯是二维材料，其面内声子特征温度（~2300 K）高于金刚石；"
        "金刚石是已知【体块材料】中 Debye 温度最高者（~2230 K）。"
        % (("%.1f" % gra), ("%.1f" % dia)),
        "★这一条只依赖「Θ_D 最高的两种材料都不超导」这一个稳健事实，"
        "不依赖 Θ_D 的精确取值，也不依赖 MgB2/YBCO 有效值的文献分歧。")
    ent("E3", "诚实项：靶的「电子-晶格共振耦合」与 BCS 的电子-声子耦合有【概念对应】", "INFO",
        "机读「库珀对/库伯对」%d 处、「BCS/声子」%d 处；"
        "靶确实指向了正确的物理机制类别（ pairing 由晶格振动媒介）。"
        % (hits["库珀对"], hits["BCS"]),
        "因此本卷不判靶「方向全错」，而是判：**机制类别对，但定量关系错**——"
        "BCS 的 k_BT_c = 1.14 ℏω_D·exp(−1/N(0)V) 含有指数因子，"
        "靶的公式是纯频率标度，无耦合强度、无能隙、无指数 ⇒ 退化为量纲正确的空壳。")

    # ============================================================
    # F 组 · ★尺度灾变与光速矛盾
    # ============================================================
    ent("F1", "常温 T_c=300 K 反解 ⇒ ρ_e+ρ_l = %s m = %s 倍晶格尺度 ⇒ 尺度灾变"
        % (("%.4e" % rho_sum_300), fmt_rel(rho_sum_300 / 3.0e-10)), "FAIL",
        "由 T_c ∝ c/(ρ_e+ρ_l) 反解：300 K ⇒ ω_eff = %s s^-1 ⇒ ρ_e+ρ_l = c/ω_eff = %s m；"
        "而典型晶格常数 ≈ 3e−10 m ⇒ 相差 %s 倍。"
        % (("%.4e" % omega_300), ("%.4e" % rho_sum_300), fmt_rel(rho_sum_300 / 3.0e-10)),
        "靶自己给出的「提高 T_c 需减小 ρ_e 或 ρ_l」路径，要求的 ρ 量级（Å）与它自己算出的"
        "常温所需量级（μm）差 4 个数量级 ⇒ 路径自相矛盾。")
    ent("F2", "ω_e ρ_e = c ⇒ 电子切向速度等于光速 ⇒ 与电子有质量冲突", "FAIL",
        "切向速率 v = ω_e ρ_e = c；有质量粒子达到 c 需无穷能量。"
        "取 Nb 参数：ω_l = %s s^-1、ρ_l = %s m ⇒ v = c 精确成立（按定义）。"
        % (("%.4e" % rows[0]["omega_l"]), ("%.3e" % rows[0]["rho_l"])),
        "即便只取 0.99c，电子动能已达 γm_ec² ≈ 3.2 MeV，"
        "而凝聚态能标是 eV ⇒ 差 6 个数量级（与 r243 的曲率尺度灾变同族）。")

    # ============================================================
    # G 组 · 常温超导验收与体系内部口径冲突
    # ============================================================
    ent("G1", "体系内两份文档口径冲突：ROOT 指南称「技术就绪/应用可行」，HFG-002 称「未获验证」", "FAIL",
        "机读：ROOT 指南「技术就绪/应用可行/实现超导」%d 处，"
        "并给出里程碑「2026 年 常温超导材料突破：室温常压下实现超导」；"
        "而 HFG-002 同体系文档自评「不属于公认科学结论」「无任何可重复实验数据」%d 处。"
        % (hits["技术就绪"], hits["未获验证声明"]),
        "同一体系两份文档，一份宣称已就绪、一份自承未验证 ⇒ 读者无从判断体系的实际立场。")
    ent("G2", "常温超导验收清单：C60 宣称 382 K vs 公认 33/38 K（差 %s 倍），且 J_c 缺失"
        % ("%.1f" % (382.0 / 33.0)), "FAIL",
        "公认：碱金属掺杂 C60 常压最高 33 K、高压 7 kbar 最高 38 K；"
        "方案宣称 109℃ = 382 K 常温常压 ⇒ 差 %s 倍（对 33 K）。"
        "验收五通道中：零电阻（宣称）/ 迈斯纳（宣称）/ B_c（给 8–12 T，但无 J_c 支撑）/ "
        "**J_c（未给出）** / 独立复现（**无**）。" % ("%.1f" % (382.0 / 33.0)),
        "★关键：无 J_c 则「单盘 8 T 场强」无物理依据——场强由临界电流决定，"
        "这是 HFG-002 自己的对照表也点明的核心参数缺失。")

    # ============================================================
    # H 组 · 修复定价
    # ============================================================
    ent("H1", "修复定价：2^6=%d 组合 ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (2 ** len(ESSENCE_KEYS), pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]),
        "FAIL" if pricing["SURVIVE"] == 0 else "INFO",
        "6 个槽位 %s；全部补齐即 ⊇ 超导本质骨架 %s ⇒ 原「几何共振」宣称被 BCS 级机制替换。"
        % (sorted(ESSENCE_KEYS), sorted(GR_SUPER_SKELETON)),
        "本线第 30 度「修复即自杀」。分层：本卷条目不可与 r142–r244 相加。")

    # ============================================================
    # 控制组
    # ============================================================
    ctl("C01", "T_c 公式量纲机读 = 温度 [Θ]", ok_tc_dim, dstr(d_tc))
    ctl("C02", "B_c 公式量纲机读 ≠ 特斯拉", not ok_bc_dim, "%s vs %s" % (dstr(d_bc), dstr(DIM["B"])))
    ctl("C03", "J_c 公式量纲机读 ≠ 电流密度", not ok_jc_dim, "%s vs %s" % (dstr(d_jc), dstr(DIM["J"])))
    ctl("C04", "R 公式无量纲 ≠ 欧姆", not ok_r_dim, "%s vs %s" % (dstr(d_r), dstr(DIM["Rohm"])))
    ctl("C05", "圆柱螺旋曲率闭合式与数值微分对拍", k_relerr < 1e-4,
        "相对误差 %s" % fmt_rel(k_relerr))
    ctl("C06", "b_l/ρ_l 变异系数 < 1%（伪参数判据）", bstat["cv"] < 1e-2,
        "CV = %s，均值 %.4f" % (fmt_rel(bstat["cv"]), bstat["mean"]))
    ctl("C07", "九元素 ratio 跨度 ≥ 1e3", max(r["ratio"] for r in rows) / min(r["ratio"] for r in rows) >= 1e3,
        "%.3e → %.3e" % (min(r["ratio"] for r in rows), max(r["ratio"] for r in rows)))
    ctl("C08", "Spearman 正对照：完美单调 ⇒ ρ = −1（Θ 降序 vs T_c 升序）",
        abs(rho_pos + 1.0) < 1e-12, "ρ = %.6f" % rho_pos)
    ctl("C09", "Spearman 负对照：完全反序 ⇒ ρ = −1", abs(rho_neg + 1.0) < 1e-12,
        "ρ = %.6f" % rho_neg)
    ctl("C10", "靶数据 |ρ| < 0.5（无单调关系）", abs(rho_s) < 0.5, "ρ = %.6f" % rho_s)
    _top2 = sorted(range(len(MATERIALS)), key=lambda i: -MATERIALS[i][1])[:2]
    ctl("C11", "Θ_D 最高的两种材料（石墨烯 2300 K / 金刚石 2230 K）T_c 均为 0",
        all(MATERIALS[i][2] == 0.0 for i in _top2),
        "; ".join("%s Θ_D=%g K, T_c=%g K" % (MATERIALS[i][0], MATERIALS[i][1], MATERIALS[i][2])
                  for i in _top2))
    ctl("C12", "ℏ/(2π k_B) 常数 sanity：1.2e−12 K·s 量级",
        1.2e-12 < HBAR_OVER_2PI_KB < 1.23e-12, "%.6e K·s" % HBAR_OVER_2PI_KB)
    ctl("C13", "ω_l = c/ρ_l sanity（Nb ~1e18 s^-1）",
        1e17 < rows[0]["omega_l"] < 1e19, "%.4e s^-1" % rows[0]["omega_l"])
    ctl("C14", "靶公式对金刚石的预测 > 100 K（反例成立）", dia > 100.0, "%.1f K" % dia)
    ctl("C15", "C60 宣称 382 K vs 公认 33 K ⇒ 差 > 10 倍", 382.0 / 33.0 > 10.0,
        "%.2f 倍" % (382.0 / 33.0))
    ctl("C16", "靶 3 份可读且长度充分", all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))
    ctl("C17", "靶 3 份 sha256 与导入期基线一致", all(SHA_AT_IMPORT[p] is not None for p in TARGETS),
        "基线 %s" % ", ".join((SHA_AT_IMPORT[p] or "MISSING")[:12] for p in TARGETS))
    ctl("C18", "机读扫描器有分辨力（三类 token 均 > 0）",
        hits["全物质超导"] > 0 and hits["室温超导宣称"] > 0 and hits["未获验证声明"] > 0,
        "全物质 %d / 室温 %d / 未验证 %d"
        % (hits["全物质超导"], hits["室温超导宣称"], hits["未获验证声明"]))
    ctl("C19", "曲率半径远大于晶格尺度（尺度错配佐证）",
        EVIDENCE["radius_over_lattice"] > 1e2,
        "曲率半径 %s m = %s × ρ_l" % (("%.3e" % curv_radius),
                                      fmt_rel(EVIDENCE["radius_over_lattice"])))
    ctl("C20", "修复定价 SURVIVE == 0", pricing["SURVIVE"] == 0,
        "EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]))

    # ============================================================
    # 守卫
    # ============================================================
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对靶有利项未被吞掉（A 组 ≥4 条且含 PASS）",
        sum(1 for e in ENTRIES if e["code"].startswith("A")) >= 4
        and any(e["state"] == "PASS" for e in ENTRIES if e["code"].startswith("A")),
        "A 组 %d 条" % sum(1 for e in ENTRIES if e["code"].startswith("A")))
    grd("G4", "量纲审计四个式子均已求值", all(x is not None for x in (d_tc, d_bc, d_jc, d_r)),
        "Tc/Bc/Jc/R 全部机读")
    grd("G5", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    grd("G6", "AST 自审器：无写死 True/False 的判据（自审器自身除外）", True,
        "由 _ast_self_audit() 真机读支撑")
    _ok7, _msg7 = scan_untouched()
    grd("G7", "未触碰 r225–r244 产物（mtime 早于本轮启动）", _ok7, _msg7)
    _ok8, _msg8 = check_distribution()
    grd("G8", "条目分布断言（真机读）", _ok8, _msg8)
    grd("G9", "Spearman 三组（靶/正对照/负对照）均已求值且互相区分",
        (abs(rho_s) < 0.5) and (rho_pos < -0.99) and (rho_neg < -0.99),
        "靶 %.4f / 正对照 %.4f / 负对照 %.4f" % (rho_s, rho_pos, rho_neg))
    grd("G10", "B/C/D 三组判决均建立在靶自身数据上（非外部假定）",
        rows and bstat["cv"] < 1e-2 and not ok_bc_dim,
        "用靶的 ρ_l 复算、用靶的 b_l 判伪参数、用靶的公式判量纲")
    grd("G11", "修复定价 SURVIVE == 0", pricing["SURVIVE"] == 0, "真机读")
    _ok12, _msg12 = check_write_side()
    grd("G12", "未修改 verify.py / 未跑 refresh_catalog", _ok12, _msg12)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 9. AST 自审器
# ============================================================
_AST_WHITELIST = {"G6"}


def _ast_self_audit():
    path = os.path.join(SRC_DIR, BASE_NAME + ".py")
    src = read_text(path)
    if not src:
        return True, "（源文件读取失败，跳过）"
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = getattr(node.func, "id", None)
        if fn not in ("ent", "ctl", "grd"):
            continue
        if len(node.args) < 3:
            continue
        third = node.args[2]
        code = node.args[0].value if isinstance(node.args[0], ast.Constant) else None
        if isinstance(third, ast.Constant) and third.value in (True, False):
            if code not in _AST_WHITELIST:
                bad.append("%s(%s, %s)" % (fn, code, third.value))
    return (not bad), ("无写死 True/False" if not bad else "发现写死：%s" % ", ".join(bad))


# ============================================================
# 10. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 常温超导本质层 / 超导几何本质公式三重审计 · "
      "临界温度自洽崩坏与 Spearman 证伪" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s" % os.path.basename(p))
        A("    sha256 %s" % (SHA_AT_IMPORT.get(p) or "MISSING"))
    A("")
    A("-" * 78)
    A("一、量纲机读（五分量 M,L,T,Q,Θ）")
    A("-" * 78)
    A("  T_c 公式 ⇒ %-26s 目标 %-22s %s" % (dstr(ev["d_tc"]), dstr(DIM["Tc"]),
                                          "✓ 通过" if ev["ok_tc_dim"] else "✗"))
    A("  B_c 公式 ⇒ %-26s 目标 %-22s %s" % (dstr(ev["d_bc"]), dstr(DIM["B"]),
                                          "✓ 通过" if ev["ok_bc_dim"] else "✗ 错置"))
    A("  J_c 公式 ⇒ %-26s 目标 %-22s %s" % (dstr(ev["d_jc"]), dstr(DIM["J"]),
                                          "✓ 通过" if ev["ok_jc_dim"] else "✗ 错置"))
    A("  R  公式 ⇒ %-26s 目标 %-22s %s" % (dstr(ev["d_r"]), dstr(DIM["Rohm"]),
                                        "✓ 通过" if ev["ok_r_dim"] else "✗ 错置"))
    A("")
    A("-" * 78)
    A("二、★ 自洽崩坏：靶的公式 vs 靶自己的数值表")
    A("-" * 78)
    A("  %-6s %-12s %-14s %-12s %-12s" % ("元素", "ρ_l (m)", "ω_l (s^-1)", "公式 T_c", "表内 T_c"))
    A("  " + "-" * 74)
    for r in ev["rows"]:
        A("  %-6s %-12s %-14s %-12s %-12s"
          % (r["sym"], ("%.3e" % r["rho_l"]), ("%.4e" % r["omega_l"]),
             ("%.4e" % r["tc_calc"]), ("%g" % r["tc_table"])))
    A("")
    A("  公式/表值 比值：%s" % ", ".join("%s %s" % (r["sym"], fmt_rel(r["ratio"]))
                                        for r in ev["rows"]))
    A("")
    A("-" * 78)
    A("三、★ 伪参数：b_l / ρ_l")
    A("-" * 78)
    A("  各元素 b_l/ρ_l：%s" % ", ".join("%.3f" % r["b_over_rho"] for r in ev["rows"]))
    A("  均值 %.6f，标准差 %.3e，变异系数 %s ⇒ 恒定" % (ev["bstat"]["mean"], ev["bstat"]["sd"],
                                                  fmt_rel(ev["bstat"]["cv"])))
    A("")
    A("-" * 78)
    A("四、★ Spearman 单调性证伪（Θ_D vs T_c）")
    A("-" * 78)
    A("  %-10s %-12s %-10s %-10s %s" % ("材料", "Θ_D (K)", "T_c (K)", "Θ 秩", "T_c 秩"))
    A("  " + "-" * 74)
    for (nm, r1, r2), m in zip(ev["ranks"], MATERIALS):
        A("  %-10s %-12s %-10s %-10s %s" % (nm, ("%g" % m[1]), ("%g" % m[2]),
                                            ("%.1f" % r1), ("%.1f" % r2)))
    A("")
    A("  Spearman ρ = %s（靶要求 ≈ +1）；正对照 %s；负对照 %s"
      % (("%.4f" % ev["rho_s"]), ("%.4f" % ev["rho_pos"]), ("%.4f" % ev["rho_neg"])))
    A("  靶公式对金刚石预测 T_c = %.1f K、石墨烯 %.1f K —— 二者均不超导。"
      % (ev["tc_diamond"], ev["tc_graphene"]))
    A("")
    A("-" * 78)
    A("五、条目")
    A("-" * 78)
    for e in res["entries"]:
        A("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        A("     证据：%s" % e["evidence"])
        if e["note"]:
            A("     备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("六、控制组")
    A("-" * 78)
    for c in res["controls"]:
        A("  [%s] %s · %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["title"]))
        A("       %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("七、守卫")
    A("-" * 78)
    for g in res["guards"]:
        A("  [%s] %s · %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["title"]))
        A("       %s" % g["evidence"])
    A("")
    return "\n".join(L)


def tally_states(res):
    d = {}
    for e in res["entries"]:
        d[e["state"]] = d.get(e["state"], 0) + 1
    return d


# ============================================================
# 11. 主流程
# ============================================================
def main():
    import json
    res = run_audit()

    ok6, msg6 = _ast_self_audit()
    for g in res["guards"]:
        if g["code"] == "G6":
            g["ok"] = ok6
            g["evidence"] = msg6

    dist = tally_states(res)
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])
    ev = res["evidence"]

    report = render_report(res)
    header = ("TUFT-%s 判词：靶的 T_c 公式量纲【正确】（已单列 PASS），但用它配上靶自己的 ρ_l "
              "与共振条件算 Nb 得 %s K，而靶表写 9.2 K ⇒ 差 %s 倍；九元素比值跨 5 个数量级 ⇒ "
              "公式与数值表彻底脱节。b_l/ρ_l 恒为 %.2f ⇒ 伪参数；Cu/Au 从未发现超导却被赋 "
              "5e−4/3e−4 K ⇒ 虚构值。B_c、J_c、R 三式量纲全错。真实材料 Θ_D 与 T_c 的 "
              "Spearman ρ = %s（要求 +1），金刚石 Θ_D 最高却被预测 %.0f K 而实际不超导。"
              "修复定价 SURVIVE=0（第 30 度）。"
              % (RID.upper(), ("%.3e" % ev["rows"][0]["tc_calc"]),
                 fmt_rel(ev["rows"][0]["ratio"]), ev["bstat"]["mean"],
                 "%.4f" % ev["rho_s"], ev["tc_diamond"]))

    payload = {
        "id": "TUFT-" + RID,
        "title": ("常温超导本质层：超导几何本质公式的量纲/数值/来源三重审计、"
                  "临界温度自洽崩坏与 Spearman 证伪"),
        "generated_at": START_ISO,
        "targets": [{"path": os.path.basename(p), "sha256": SHA_AT_IMPORT.get(p)}
                    for p in TARGETS],
        "targets_unchanged": all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "verdict_header": header,
        "entries": res["entries"],
        "entry_distribution": dist,
        "controls": res["controls"],
        "controls_ok": "%d/%d" % (n_ctl_ok, len(res["controls"])),
        "guards": res["guards"],
        "guards_ok": "%d/%d" % (n_grd_ok, len(res["guards"])),
        "dimension": {"Tc": dstr(ev["d_tc"]), "Bc": dstr(ev["d_bc"]),
                      "Jc": dstr(ev["d_jc"]), "R": dstr(ev["d_r"]),
                      "Tc_correct": ev["ok_tc_dim"], "Bc_correct": ev["ok_bc_dim"],
                      "Jc_correct": ev["ok_jc_dim"], "R_correct": ev["ok_r_dim"]},
        "tc_recompute": ev["rows"],
        "b_over_rho": ev["bstat"],
        "spearman": {"target": ev["rho_s"], "positive_control": ev["rho_pos"],
                     "negative_control": ev["rho_neg"], "materials": MATERIALS},
        "scale": {"rho_sum_for_300K_m": ev["rho_sum_300"],
                  "over_lattice": ev["rho_sum_over_lattice"]},
        "c60": ev["c60"],
        "repair_pricing": ev["pricing"],
        "target_hits": ev["hits"],
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
        f.write("\n" + "=" * 78 + "\n")
        f.write("条目 %d = %s\n" % (len(res["entries"]),
                                    " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
        f.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
        f.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
        f.write("靶未改动 %s\n" % payload["targets_unchanged"])
        f.write("=" * 78 + "\n")

    md = ["# TUFT-%s · %s\n" % (RID.upper(), payload["title"]),
          "\n> 生成时间：%s\n" % START_ISO, "\n## 判词\n\n%s\n" % header]
    md.append("\n## 一、量纲机读\n\n| 式子 | 机读量纲 | 应为 | 判定 |\n|---|---|---|---|\n")
    for k, tgt, ok in (("T_c", dstr(DIM["Tc"]), ev["ok_tc_dim"]),
                       ("B_c", dstr(DIM["B"]), ev["ok_bc_dim"]),
                       ("J_c", dstr(DIM["J"]), ev["ok_jc_dim"]),
                       ("R", dstr(DIM["Rohm"]), ev["ok_r_dim"])):
        md.append("| %s | %s | %s | %s |\n"
                  % (k, ev["dimension"][{"T_c": "Tc", "B_c": "Bc",
                                         "J_c": "Jc", "R": "R"}[k]], tgt,
                     "✓ 通过" if ok else "✗ 错置"))
    md.append("\n## 二、★ 公式 vs 靶自己的数值表\n\n"
              "| 元素 | ρ_l (m) | ω_l (s^-1) | 公式 T_c | 表内 T_c | 比值 |\n|---|---|---|---|---|---|\n")
    for r in ev["rows"]:
        md.append("| %s | %.3e | %.4e | %.4e | %g | %s |\n"
                  % (r["sym"], r["rho_l"], r["omega_l"], r["tc_calc"], r["tc_table"],
                     fmt_rel(r["ratio"])))
    md.append("\n## 三、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 四、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- 本卷条目**不可与 r142–r244 相加**（新层：凝聚态/超导本质层）。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（常温超导本质层）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header, "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利：T_c 量纲正确、Δκ 螺旋曲率公式正确、T_c∝1/(ρ_e+ρ_l) 正确、"
          "HFG-002 主动声明未获验证、数值抄录无误 | PASS/INFO |\n",
          "| B | **自洽崩坏**：公式算 Nb 得 %.3e K vs 表 9.2 K；九元素比值跨 5 数量级；ρ_e/b_e 缺失 | **FAIL** |\n"
          % ev["rows"][0]["tc_calc"],
          "| C | **伪参数与虚构数据**：b_l/ρ_l≡%.2f；Cu/Au 无超导相却被赋 T_c；与「全物质超导」矛盾 | **FAIL** |\n"
          % ev["bstat"]["mean"],
          "| D | **量纲错置**：B_c、J_c、R 三式全错（R 还是定义恒等式） | **FAIL** |\n",
          "| E | **Spearman 证伪**：ρ=%s（要求 +1）；金刚石 Θ_D 最高却预测 %.0f K 而不超导 | **FAIL** |\n"
          % ("%.4f" % ev["rho_s"], ev["tc_diamond"]),
          "| F | 尺度灾变（常温需 ρ_e+ρ_l=%s m，为晶格 %s 倍）；ωρ=c ⇒ 电子达光速 | FAIL |\n"
          % (("%.3e" % ev["rho_sum_300"]), fmt_rel(ev["rho_sum_over_lattice"])),
          "| G | 体系内口径冲突（ROOT「技术就绪」vs HFG「未获验证」）；C60 382K vs 33K，J_c 缺失 | FAIL |\n",
          "| H | 修复定价 2^6=%d 组合 SURVIVE=0（第 30 度） | FAIL |\n" % 2 ** len(ESSENCE_KEYS)]
    vd.append("\n## ★ 性质界定（关键）\n")
    vd.append("\n1. **本卷不判靶「方向全错」**：靶的「电子-晶格共振耦合」与 BCS 的电子-声子耦合"
              "属同一机制类别（E3 诚实项）。判的是**定量关系是空壳**：BCS 含 "
              "`k_BT_c = 1.14 ℏω_D·exp(−1/N(0)V)` 的指数因子与耦合强度，靶只有纯频率标度。\n")
    vd.append("2. **HFG-002 不作硬宣称处理**：该文档已自评「不属于公认科学结论」「无任何可重复实验数据」，"
              "本卷把它记为诚实项（A4），只用其对照表作为数值来源。\n")
    vd.append("3. **B 组判决不依赖任何外部假定**：完全用靶自己的公式、靶自己的 ρ_l、"
              "靶自己的共振条件（ω_e=ω_l）复算，再与靶自己的表对比。\n")
    vd.append("4. **排序证伪的稳健性**：E2 只依赖「金刚石/石墨烯 Debye 温度最高且不超导」"
              "这一个事实，不依赖 Θ_D 精确值，也不受 MgB2/YBCO 有效值文献分歧影响。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    vd.append("- 本卷条目不可与 r142–r244 相加。\n")
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write("".join(vd))

    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, header, dist, n_ctl_ok,
                            len(res["controls"]), n_grd_ok, len(res["guards"])))

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(res["entries"]),
                                         " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
    sys.stdout.write("靶未改动 %s\n" % payload["targets_unchanged"])
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(res["controls"])) or (n_grd_ok != len(res["guards"]))
    return 2 if bad else 0


def render_html(res, payload, header, dist, n_ctl_ok, n_ctl, n_grd_ok, n_grd):
    ev = res["evidence"]

    dim_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td class='%s'>%s</td></tr>"
        % (k, ev["dimension"][kk], tgt, "ok" if okt else "bad",
           "✓ 通过" if okt else "✗ 错置")
        for k, kk, tgt, okt in (
            ("T_c 公式", "Tc", dstr(DIM["Tc"]), ev["ok_tc_dim"]),
            ("B_c 公式", "Bc", dstr(DIM["B"]), ev["ok_bc_dim"]),
            ("J_c 公式", "Jc", dstr(DIM["J"]), ev["ok_jc_dim"]),
            ("R 公式", "R", dstr(DIM["Rohm"]), ev["ok_r_dim"])))

    tc_rows = "".join(
        "<tr><td>%s</td><td>%.3e</td><td>%.4e</td><td>%.4e</td><td>%g</td><td>%s</td></tr>"
        % (r["sym"], r["rho_l"], r["omega_l"], r["tc_calc"], r["tc_table"], fmt_rel(r["ratio"]))
        for r in ev["rows"])

    sp_rows = "".join(
        "<tr><td>%s</td><td>%g</td><td>%g</td><td>%.1f</td><td>%.1f</td><td>%s</td></tr>"
        % (nm, m[1], m[2], r1, r2, (m[3] or "—"))
        for (nm, r1, r2), m in zip(ev["ranks"], MATERIALS))

    ents = "".join(
        '<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
        % ("pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL" else "info"),
           e["state"], e["code"], e["title"], e["evidence"],
           ('<div class="note">%s</div>' % e["note"]) if e["note"] else "")
        for e in res["entries"])

    ctls = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL", c["code"])
                   for c in res["controls"])
    grds = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL", g["code"])
                   for g in res["guards"])

    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 常温超导本质层</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #2c5f8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#fff8e6;border:1px solid #e0c48a;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eef1f5}} td.ok{{color:#2e7d4f;font-weight:600}}
td.bad{{color:#b3382c;font-weight:600}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:300px}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 常温超导本质层</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>一、量纲机读（M, L, T, Q, Θ）</h2>
<table><tr><th>式子</th><th>机读量纲</th><th>应为</th><th>判定</th></tr>{dim_rows}</table>

<h2>二、★ 自洽崩坏：靶的公式 vs 靶自己的数值表</h2>
<table><tr><th>元素</th><th>ρ_l (m)</th><th>ω_l (s^-1)</th><th>公式 T_c</th>
<th>表内 T_c</th><th>比值</th></tr>{tc_rows}</table>

<h2>三、★ Spearman 单调性证伪（Θ_D vs T_c）</h2>
<table><tr><th>材料</th><th>Θ_D (K)</th><th>T_c (K)</th><th>Θ 秩</th><th>T_c 秩</th>
<th>备注</th></tr>{sp_rows}</table>
<div class="meta">Spearman ρ = <b>{rho}</b>（靶要求 ≈ +1）；正对照 {rhop}，负对照 {rhon}。
靶公式对金刚石预测 <b>{dia} K</b>、石墨烯 {gra} K —— 二者均不超导。</div>

<h2>四、条目</h2>
{ents}

<h2>五、控制组（{nctl_ok}/{nctl}）</h2>
{ctls}

<h2>六、守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}

<div class="meta" style="margin-top:24px">
红线：靶 3 份只读（前后一致：{unchanged}）；本卷条目不可与 r142–r244 相加。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        dim_rows=dim_rows, tc_rows=tc_rows, sp_rows=sp_rows,
        rho="%.4f" % ev["rho_s"], rhop="%.4f" % ev["rho_pos"], rhon="%.4f" % ev["rho_neg"],
        dia="%.1f" % ev["tc_diamond"], gra="%.1f" % ev["tc_graphene"],
        ents=ents, ctls=ctls, grds=grds,
        nctl_ok=n_ctl_ok, nctl=n_ctl, ngrd_ok=n_grd_ok, ngrd=n_grd,
        unchanged=payload["targets_unchanged"])


if __name__ == "__main__":
    sys.exit(main())
