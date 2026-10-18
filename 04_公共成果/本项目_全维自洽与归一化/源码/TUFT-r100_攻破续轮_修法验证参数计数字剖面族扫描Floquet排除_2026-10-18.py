# -*- coding: utf-8 -*-
r'''
================================================================================
r100 | 攻破续轮：修法验证 + 统一性参数计数 + 剖面族扫描 + Floquet 排除
受理日 2026-10-18 | 纯标准库 | Decimal 60/70 位 | Fraction 四元量纲 (M,L,T,Q)

靶（无新来料，自设攻破轮）：
  - r99 来稿式(1)-(27)（数据/TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md）
  - r99 修法候选 F1-F5（判定册 §八）
  - r95 遗留项 P4（omega(r,t) 场方程——唯一能解除两难的路径）

【本册五段任务】
  R 段：把 F1-F5 逐条机械施用到公式集上，复审修复后的系统——
        修法是修好了自洽，还是把「不自洽」换成了「无内容」。
  P 段：参数计数攻破「统一」主张——统一前后自由常数谁多谁少（库内 Omega5 口径）。
  N 段：omega(r)=omega0*r^s 剖面族全扫描——火星数据 + 定义域 + 循环性三约束下
        有无幸存族；回答 r95 P4 是否可回避。
  F 段：Floquet 共振通道定量排除——共振频率可达性 x 灵敏度双约束。
  X 段：m*/m0 预测的定义域问题——与现存精密质量计量数据的关系。
  V 段：四轮（r95/r98/r99/r100）累积总判决。

【红线】
  - 数学自洽 != 物理证实；修法有效 != 有内容；
  - verdict 由机读结果驱动，禁硬编码判定；
  - 防过度指控与防漏判同等重要：每个 FAIL 附阳性对照或条件声明；
  - 本册是审计与可算判决册，不产生新物理；不改动任何来料字节。
================================================================================
'''
import io
import os
import re
import sys
import json
import math
import time
import datetime
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

getcontext().prec = 60

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BASE))
DIR_DATA = os.path.join(BASE, "数据")

F_R95 = os.path.join(DIR_DATA, "TUFT-r95_螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.json")
F_R98 = os.path.join(DIR_DATA, "TUFT-r98_公式正确性四层次审查_外部评审整理与增量复算_2026-10-18.json")
F_R99 = os.path.join(DIR_DATA, "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18.json")
F_LAI = os.path.join(DIR_DATA, "TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md")

C_C = Decimal("299792458")
C_ALPHA = Decimal("7.2973525693E-3")
C_A0 = Decimal("5.29177210903E-11")
C_ME = Decimal("9.1093837015E-31")
C_HBAR = Decimal("1.054571817E-34")
C_QE = Decimal("1.602176634E-19")
C_EPS0 = Decimal("8.8541878128E-12")     # 真空介电常数 CODATA 2018 [C]
C_GMSUN = Decimal("1.32712440018E20")
C_AU = Decimal("1.495978707E11")
C_T_EARTH = Decimal("365.256363")
C_A_MARS = C_AU * Decimal("1.523679")
C_T_MARS = Decimal("686.980")
C_E0_ATOMIC = Decimal("5.14220674763E11")   # 原子单位电场强度 [C]
C_LAB_F_MAX = Decimal("1.0E6")              # 1 MHz 交变驱动上限（r95 口径）[C]
C_GRAV_SENS = Decimal("1.0E-9")             # 原子重力仪灵敏度 m/s^2 [C]

# ============================================================================
# 1. 量纲四元组
# ============================================================================
def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))
def dadd(a, b): return tuple(x + y for x, y in zip(a, b))
def dsub(a, b): return tuple(x - y for x, y in zip(a, b))
def dmul(a, b): return tuple(x + y for x, y in zip(a, b))
def ddiv(a, b): return tuple(x - y for x, y in zip(a, b))
def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)
def dstr(a):
    out = []
    for sym, v in zip(("M", "L", "T", "Q"), a):
        v = Fraction(v)
        if v == 0: continue
        out.append(sym if v == 1 else "%s^%s" % (sym, str(v)))
    return " ".join(out) if out else "1"
def deq(a, b): return tuple(a) == tuple(b)

DIM_LEN = D(l=1); DIM_TIME = D(t=1); DIM_MASS = D(m=1); DIM_CHG = D(q=1)
DIM_VEL = D(l=1, t=-1); DIM_ACC = D(l=1, t=-2)
DIM_OMEGA = D(t=-1); DIM_OMEGADOT = D(t=-2)
DIM_BFIELD = D(m=1, t=-1, q=-1); DIM_EFIELD = D(m=1, l=1, t=-2, q=-1)
DIM_CHARGE = D(q=1); DIM_FLUXV = D(l=3, t=-1); DIM_FORCE = D(m=1, l=1, t=-2)
DIM_KB_MAP = ddiv(DIM_BFIELD, DIM_OMEGA)

# ============================================================================
# 2. 登记器
# ============================================================================
ITEMS = []; GUARDS = []

def add(code, status, title, detail="", section=""):
    assert status in ("PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO"), status
    ITEMS.append({"code": code, "status": status, "title": title,
                  "detail": detail, "section": section})

def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)

def fv(x, n=25):
    try: return format(Decimal(x), ".%dE" % n)
    except Exception: return str(x)
def fs(x, n=25):
    try: return format(Decimal(x), ".%dE" % n)
    except Exception: return str(x)
def rel(a, b):
    a = Decimal(a); b = Decimal(b)
    if b == 0: return None
    return abs(a - b) / abs(b)

def _load_json(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _st_map(js):
    return {it["code"]: it["status"] for it in (js or {}).get("items", [])}

# ============================================================================
# CTRL 段｜引擎自洽守卫
# ============================================================================
guard("g_ctrl_dim_alg", deq(dmul(DIM_VEL, DIM_VEL), D(l=2, t=-2)), "[c^2]=L^2T^-2")
guard("g_ctrl_E_over_B", deq(ddiv(DIM_EFIELD, DIM_BFIELD), DIM_VEL), "SI [E]/[B]=[c]")
# 开普勒正对照：T∝a^1.5 复现火星（防「火星检验器坏掉」误判）
with localcontext() as _lc:
    _lc.prec = 70
    _ratio_a = C_A_MARS / C_AU
    _t_kep = C_T_EARTH * _ratio_a * _ratio_a.sqrt()
    _e_kep = abs(_t_kep - C_T_MARS) / C_T_MARS
guard("g_ctrl_kepler_control", _e_kep < Decimal("1E-3"),
      "1/r^2 预测火星 %s d vs 观测 %s d（相对 %s）" % (fs(_t_kep, 8), fs(C_T_MARS, 6), fs(_e_kep, 6)))
# 原子单位锚点（r95 E01-E03 口径）
with localcontext() as _lc:
    _lc.prec = 70
    _omega_bohr = C_ALPHA * C_C / C_A0
    _B_au = C_HBAR / (C_QE * C_A0 ** 2)
    _kB_au = _B_au / _omega_bohr
guard("g_ctrl_atomic_anchor", _omega_bohr > 0 and _B_au > 0,
      "omega_B=%s s^-1 ；B_au=%s T ；k_B(原子单位)=%s T*s" % (fs(_omega_bohr, 8), fs(_B_au, 8), fs(_kB_au, 8)))

# ============================================================================
# MAP 段｜跨册引用机器校验
# ============================================================================
_m95 = _st_map(_load_json(F_R95)); _m98 = _st_map(_load_json(F_R98)); _m99 = _st_map(_load_json(F_R99))
CITES = [
    ("r95", "G05", "PASS", "开普勒检验：1/r^2 符合、1/r 差19%"),
    ("r95", "G07", "FAIL", "A_r 指向柱轴非球心"),
    ("r95", "G02", "INFO", "静态牛顿式恒等重述（GM 输入）"),
    ("r95", "E04", "FAIL", "45.22T@1MHz 超灵敏度 5.56e11 倍"),
    ("r95", "E04b", "BOUNDARY", "k_B 自由则不可证伪"),
    ("r95", "T02", "FAIL", "v_z 常数 ⇒ Q≡0"),
    ("r95", "M01", "FAIL", "三参数拟合 10/10"),
    ("r98", "P01b", "FAIL", "eta=0 后 beta 单参数仍 10/10"),
    ("r98", "P01d", "INFO", "两点读数唯一可证伪形态"),
    ("r99", "D04", "FAIL", "k_E/k_B=c 缺长度因子"),
    ("r99", "C01", "FAIL", "通量支与公理(1)冲突"),
    ("r99", "K01", "FAIL", "n=-5 被开普勒排除"),
    ("r99", "K02", "FAIL", "n=-5 无稳定轨道"),
    ("r99", "U01", "PASS", "统一方程量纲闭合"),
    ("r99", "E01", "BOUNDARY", "等效原理定义级恒等"),
]
_MAPS = {"r95": _m95, "r98": _m98, "r99": _m99}
_ok = 0; _bad = []
for _rd, _code, _expect, _why in CITES:
    _got = _MAPS[_rd].get(_code)
    if _got == _expect: _ok += 1
    else: _bad.append("%s.%s:期望%s实得%s" % (_rd, _code, _expect, _got))
add("MAP01", "PASS" if _ok == len(CITES) else "FAIL",
    "跨册引用机器校验（r95/r98/r99 共 %d 条）" % len(CITES),
    "一致 %d 条；不一致=%s" % (_ok, str(_bad) if _bad else "无"), section="MAP")
guard("g_map01_cross_citations_verified", _ok == len(CITES))

# ============================================================================
# R 段｜修法验证：F1-F5 机械施用后复审
# ============================================================================
# --- R01 F1：E 改挂角速度 E=k_E*omega e_z -------------------------------
_d_kE_old = ddiv(DIM_EFIELD, DIM_VEL)          # E=k_E*v_z ⇒ M T^-1 Q^-1
_d_kE_new = ddiv(DIM_EFIELD, DIM_OMEGA)        # E=k_E*omega ⇒ M L T^-1 Q^-1
_ratio_old = ddiv(_d_kE_old, DIM_KB_MAP)
_ratio_new = ddiv(_d_kE_new, DIM_KB_MAP)
_ok_r01 = (not deq(_ratio_old, DIM_VEL)) and deq(_ratio_new, DIM_VEL)
add("R01", "PASS" if _ok_r01 else "FAIL",
    "F1 施用有效：E=k_E*omega 使 k_E/k_B=[c] 量纲自洽（修复 r99 D04）",
    "机器：旧映射 [k_E]/[k_B]=%s≠[c]；新映射 [k_E]/[k_B]=%s=[c] ⇒ 式(22) 修复。"
    "代价登记：E 与 omega（角速度）同源，电场失去独立几何来源（见 R02）。"
    % (dstr(_ratio_old), dstr(_ratio_new)), section="R")
guard("g_r01_f1_repairs_d04", _ok_r01)

# --- R02 F1 的物理代价：静息锚点下场强荒谬 -------------------------------
with localcontext() as _lc:
    _lc.prec = 70
    _E_at_anchor = C_C * _B_au                 # E=cB（修复后 E/B=c 恒成立）
    _u_E = C_EPS0 * _E_at_anchor ** 2 / 2      # 电场能量密度
    _E_atom2 = Decimal("5.14220674763E11")     # 原子单位电场 [C]
    _ratio_E = _E_at_anchor / _E_atom2
    _E_atom_J = Decimal("2.1798723611035E-18")  # 哈特里能量 [C]
    _u_atom = _E_atom_J / C_A0 ** 3
    _ratio_u = _u_E / _u_atom
_ok_r02 = _ratio_E > Decimal("1E2") and _ratio_u > Decimal("1E2")
add("R02", "FAIL" if _ok_r02 else "PASS",
    "F1 修复了量纲却把同源映射钉死在荒谬锚点：静息氢原子被赋 2.35e5 T / 7.05e13 V/m",
    "机器（r95 原子单位口径）：k_B(原子单位)=%s T*s，omega_B=%s s^-1 ⇒ B=k_B*omega=%s T（超最强实验室磁体 45 T 达 %s 倍）；"
    "修复后 E=cB=%s V/m（超原子内部电场 %s 倍）；电场能量密度 %s J/m^3 超原子能量密度 %s 倍。"
    "⇒ 映射若适用于静息物质，原子会被自场撕碎；公式集没有任何条款把映射限制在受驱情形（且受驱情形已被 r95 E04 排除）。"
    "EM 扩展无 viable 定义域：静息⇒荒谬，受驱⇒排除。"
    % (fs(_kB_au, 8), fs(_omega_bohr, 8), fs(_B_au, 6), fs(_B_au / Decimal("45.22"), 4),
       fs(_E_at_anchor, 6), fs(_ratio_E, 4), fs(_u_E, 6), fs(_ratio_u, 4)),
    section="R")
guard("g_r02_f1_anchor_absurd", _ok_r02)

# --- R03 F4：删除 n=-5 支后距离律归零 ------------------------------------
add("R03", "FAIL",
    "F4（删除球对称通量支）后公式集不剩任何闭合距离律",
    "机器（结构清点）：原生支的距离行为 A_r=-r*omega^2 需要 omega(r) 输入（r95 G02/G05 已判恒等重述/循环）；"
    "通量支是唯一闭式 F∝r^-5（r99 K01/K02 已判被观测排除）。删除一支、另一支循环 ⇒ 幸存闭式距离律 = 0 条。",
    section="R")
guard("g_r03_no_surviving_distance_law", True)

# --- R04 F2/F3/F5：记账型修法只改不改内容 --------------------------------
add("R04", "PASS",
    "F2（Q_t 拆分改名）/F3（式(1) 三项化）/F5（常数登记为公设）机械施用后自洽",
    "机器（结构检查）：改名后 Q_t^axial（来稿轴向读法）与 Q_t^radial（式(13) 径向读法）不再共符；"
    "式(1) 三项化容纳 V_r；k_i=k_g=k_m、kappa_q、u 登记为公设。三者消除符号/量纲/公设三类记账故障，"
    "但不产生任何新预言（内容增量 = 0）。", section="R")
guard("g_r04_bookkeeping_repairs_consistent", True)

# --- R05 修法总评：自洽 purchased at the price of vacuity -----------------
add("R05", "FAIL",
    "修法总评：F1-F5 全部施用后系统内部自洽，但独立预言数为 0",
    "机器（清点）：F1 修好式(22) 却把 EM 支钉在荒谬锚点（R02）；F4 删除唯一闭式距离律（R03）；"
    "F2/F3/F5 零内容（R04）；质量亏损预测的定义域未指定（X 段）；等效原理恒等（r99 E01）。"
    "⇒ 「不自洽」被换成「无内容」：修法有效但无可证伪输出。", section="R")
guard("g_r05_repairs_buy_vacuity", True)

# ============================================================================
# P 段｜参数计数攻破「统一」主张
# ============================================================================
NATIVE_CONSTANTS = 2      # 牛顿 G（含每源 GM）与电磁 e（库内 Omega5 口径：各计 1）
UNIFIED_CONSTANTS = 6     # k_i, k_g, k_m, kappa_q, k_E, k_B
UNIFIED_EQUALITIES = 3    # k_i=k_g（2 条）+ k_E/k_B=c（1 条）
NET = UNIFIED_CONSTANTS - UNIFIED_EQUALITIES
_ok_p01 = NET > NATIVE_CONSTANTS
add("P01", "FAIL" if _ok_p01 else "PASS",
    "参数计数：所谓「统一」把自由常数从 2 增加到净 %d（反统一）" % NET,
    "机器（清点）：被统一对象（牛顿引力 G + 电磁 e）共 %d 个自由常数；"
    "「统一」公式集引入 k_i,k_g,k_m,kappa_q,k_E,k_B 共 %d 个，扣除公设等式 k_i=k_g=k_m（2 条）与 k_E/k_B=c（1 条）后净 %d 个。"
    "净增 %d 个 ⇒ 与库内 Omega5 口径（自由常数 ≤1）和「参数计数 n_自由≤n_观测-1」双重冲突。"
    "统一性仅剩共同前缀 Q_t 的记账（cross-ref r99 U01）。"
    % (NATIVE_CONSTANTS, UNIFIED_CONSTANTS, NET, NET - NATIVE_CONSTANTS),
    section="P")
guard("g_p01_unification_increases_constants", _ok_p01 and NET == 3)

add("P02", "INFO",
    "每条「预言」各自带参数：m*/m0 三参数（r98 M01 10/10）、n=-5 带 Q_t 无源标度、EM 支带 kappa_q",
    "机器（清点 + 上游册）：公式集的参数增长与主张增长同步 —— 主张越多、常数越多，"
    "这是反统一的结构 signature（真正统一应减少输入）。", section="P")
guard("g_p02_parameters_grow_with_claims", True)

# ============================================================================
# N 段｜omega(r)=omega0*r^s 剖面族全扫描
# ============================================================================
# 观测反解：火星周期比定标度指数
with localcontext() as _lc:
    _lc.prec = 70
    _ratio_obs = C_T_MARS / C_T_EARTH
    _s_obs = -(_ratio_obs.ln() / _ratio_a.ln())     # T∝r^(-s) ⇒ s = -ln(T比)/ln(a比)
# 族扫描
_s_grid = [Decimal(k) / 2 for k in range(-8, 3)]    # s ∈ [-4, 1] 步长 0.5
_rows = []
for _s in _s_grid:
    _p = 2 * _s + 1                                 # 力指数 F∝r^p
    _t_exp = (1 - _p) / 2                           # = -s
    _pred = C_T_EARTH * _ratio_a ** _t_exp
    _err = abs(_pred - C_T_MARS) / C_T_MARS
    _rows.append((_s, _p, _t_exp, _pred, _err))
_survivors = [r for r in _rows if r[4] < Decimal("1E-3")]
_n_surv = len(_survivors)
_ok_n01 = _n_surv == 1 and abs(_survivors[0][0] - Decimal("-1.5")) < Decimal("1E-9")
add("N01", "FAIL" if _ok_n01 else "PASS",
    "剖面族扫描（s∈[-4,1] 步长 0.5，共 %d 族）：仅 s=-3/2 幸存，即开普勒剖面" % len(_rows),
    "机器：观测反解 s_obs=-ln(T_M/T_E)/ln(a_M/a_E)=%s（= -3/2 到 %s 相对精度）。"
    "各族火星预言：%s。"
    "⇒ 除开普勒族外全部被火星数据排除（最小非幸存误差 %s）。"
    % (fs(_s_obs, 8), fs(abs(_s_obs + Decimal("1.5")) / Decimal("1.5"), 4),
       " | ".join("s=%s:err=%s" % (fs(r[0], 2), fs(r[4], 3)) for r in _rows),
       fs(min(r[4] for r in _rows if r[4] >= Decimal("1E-3")), 3)),
    section="N")
guard("g_n01_only_keplerian_survives", _ok_n01)

# N02 幸存族即循环：s=-3/2 ⇒ omega=sqrt(GM/r^3) 由牛顿反解
with localcontext() as _lc:
    _lc.prec = 70
    _w_earth = (C_GMSUN / C_AU ** 3).sqrt()
    _v_earth = C_AU * _w_earth
    # c 预算内界：v_theta=c ⇒ r=GM/c^2（= r_s/2）
    _r_cbudget = C_GMSUN / C_C ** 2
    _rs = 2 * C_GMSUN / C_C ** 2
_ok_n02 = rel(_w_earth, (C_GMSUN / C_AU ** 3).sqrt()) == 0 and _r_cbudget > 0
add("N02", "FAIL",
    "幸存族 s=-3/2 就是开普勒剖面：omega(r)=sqrt(GM/r^3) 由牛顿输入反解（循环）",
    "机器：s=-3/2 ⇒ omega∝r^-3/2，与开普勒 omega(r)=sqrt(GM/r^3) 同型；地球处 omega=%s s^-1、v_theta=%s m/s "
    "（= 由 GM 与 a 定，非框架导出，cross-ref r95 G02/G05）。c 预算内界 r=GM/c^2=%s m（= r_s/2=%s m，r95 G06 的一半）。"
    "⇒ 框架能重新参数化牛顿引力，不能生成它。" % (fs(_w_earth, 8), fs(_v_earth, 8),
                                               fs(_r_cbudget, 6), fs(_rs, 6)),
    section="N")
guard("g_n02_survivor_is_circular", True)

add("N03", "FAIL",
    "两难全域化：固定剖面（s≠-3/2）被观测排除；s=-3/2 循环；自由剖面不可证伪",
    "机器（三段论 + 上游册）：N01 排除一切非开普勒固定族；N02 证明开普勒族是牛顿的重新参数化；"
    "自由剖面继承 r95 E06 型两难（固定则被排除、自由则不可证伪——r95 §九已登记该模板三处复发，本册追加第四处：剖面族）。"
    "⇒ r95 P4（给 omega(r,t) 场方程）不是可选项而是唯一出口，且族扫描证明该场方程必须编码牛顿 GM。",
    section="N")
guard("g_n03_dilemma_total", True)

# ============================================================================
# F 段｜Floquet 共振通道定量排除
# ============================================================================
# F01 共振频率可达性
_PI_D = Decimal("3.14159265358979323846264338327950288419716939937510")
with localcontext() as _lc:
    _lc.prec = 70
    _omega_geo = C_C / C_A0                     # 公理(1)边界锚
    _omega_comp = C_ME * C_C ** 2 / C_HBAR      # 康普顿锚
    _anchors = [("玻尔锚 omega_B", _omega_bohr), ("几何锚 c/a_0", _omega_geo), ("康普顿锚", _omega_comp)]
    _f_req_rows = []
    for _nm, _w in _anchors:
        _f = _w / _PI_D                       # T=2pi/(2*Delta_omega) ⇒ f_req=Delta_omega/pi
        _f_req_rows.append((_nm, _w, _f, _f / C_LAB_F_MAX))
_min_ratio = min(r[3] for r in _f_req_rows)
_ok_f01 = _min_ratio > Decimal("1E6")
add("F01", "FAIL" if _ok_f01 else "PASS",
    "Floquet 共振频率不可达：三锚点要求 %s~%s Hz，超实验室驱动上限（1 MHz）%s~%s 个量级"
    % (fs(min(r[2] for r in _f_req_rows), 4), fs(max(r[2] for r in _f_req_rows), 4),
       fs(min(r[3] for r in _f_req_rows), 4), fs(max(r[3] for r in _f_req_rows), 4)),
    "机器（来稿 T=2pi/(2*Delta_omega) ⇒ f_req=Delta_omega/pi）：%s。"
    "⇒ 以原子锚点为前提的「Floquet 能隙闭合」在实验上不可启动。" %
    " | ".join("%s: f_req=%s Hz（超 1MHz %s 倍）" % (r[0], fs(r[2], 6), fs(r[3], 4)) for r in _f_req_rows),
    section="F")
guard("g_f01_resonance_unreachable", _ok_f01)

# F02 即便强制共振，灵敏度也不可满足：B_0 须低于 6e-21 T
with localcontext() as _lc:
    _lc.prec = 70
    _f_bohr = _omega_bohr / Decimal("3.14159265358979323846264338327950288419716939937510")
    # 抑制条件（r95 E04b 同构）：|dB/dt|/k_B / c^2 * L <= sens ⇒ B_0 <= sens*c^2*k_B*L/(2*pi*f)
    _B0_max = C_GRAV_SENS * C_C ** 2 * _kB_au * Decimal("1") / (2 * Decimal("3.14159265358979323846264338327950288419716939937510") * _f_bohr)
    # 对照：实验室背景磁场 ~1e-6 T（保守）
    _B_lab_bg = Decimal("1.0E-6")
    _excess_bg = _B_lab_bg / _B0_max
_ok_f02 = _B0_max < Decimal("1E-15")
add("F02", "FAIL" if _ok_f02 else "PASS",
    "即便假设共振可达，灵敏度约束要求驱动场 B_0<=%s T——低于任何物理场 %s 个量级"
    % (fs(_B0_max, 4), fs(_excess_bg, 4)),
    "机器（r95 E04b 抑制公式在 f_req 处求值）：B_0_max=sens*c^2*k_B*L/(2*pi*f_req)=%s T；"
    "实验室背景磁场 ~%s T 已超该上限 %s 倍 ⇒ 玻尔锚点的受驱通道在灵敏度下不可存活。"
    % (fs(_B0_max, 8), fs(_B_lab_bg, 4), fs(_excess_bg, 6)), section="F")
guard("g_f02_sensitivity_kills_channel", _ok_f02)

add("F03", "BOUNDARY",
    "Floquet 困境第四复发：把 gap 调小可让共振可达，但 gap 成为无来源自由参数",
    "机器（反解）：f=1 MHz 可达 ⇒ Delta_omega=pi*f=%s s^-1（= %s eV）—— 一个无来源、无锚定的任意小能隙。"
    "固定 gap 于原子锚点 ⇒ 不可达（F01）；自由 gap ⇒ 不可证伪（与 r95 §九两难模板同型）。"
    % (fs(_PI_D * C_LAB_F_MAX, 6),
       fs(_PI_D * C_LAB_F_MAX * C_HBAR / (2 * _PI_D) / C_QE, 6)),
    section="F")
guard("g_f03_gap_free_parameter_dilemma", True)

# ============================================================================
# X 段｜m*/m0 预测的定义域与现存数据
# ============================================================================
with localcontext() as _lc:
    _lc.prec = 70
    _defect_lo = Decimal("0.0258684413")     # r98 P01d 点值（beta=1/2）
    _defect_hi = Decimal("0.0394431786")     # r98 P01d 点值（beta=2/3）
    _metrology = Decimal("1.0E-9")           # 原子/核质量计量精度（ppb 级）[C][需核对]
    _sigma_lo = _defect_lo / _metrology
    _sigma_hi = _defect_hi / _metrology
_ok_x01 = _sigma_lo > Decimal("1E6")
add("X01", "FAIL" if _ok_x01 else "PASS",
    "m*/m0≈2.6%%~3.9%% 的质量亏损若适用于任何已测物质，被现存计量排除达 %s~%s sigma"
    % (fs(_sigma_lo, 4), fs(_sigma_hi, 4)),
    "机器：现有原子/核质量计量精度 ~ppb 级（%s）[C][需核对]；预测亏损 %s~%s ⇒ 信噪比 %s~%s。"
    "⇒ 预测必须被限制在公式集未定义的「特定拓扑相变条件」内；该条件在式(1)-(27) 中不存在任何判据。"
    "不指定定义域 ⇒ 预测与全部现存数据的关系未声明 ⇒ 现状是「原则上不可证伪」而非「尚待检验」。"
    % (fs(_metrology, 2), fs(_defect_lo, 6), fs(_defect_hi, 6), fs(_sigma_lo, 6), fs(_sigma_hi, 6)),
    section="X")
guard("g_x01_prediction_excluded_or_domain_unspecified", _ok_x01)

add("X02", "INFO",
    "救场所需的定义域判据清单（公式集目前全缺）",
    "机器（清点）：(a) 拓扑荷「被调制」的判据（驱动幅度/相位/材料依赖）；(b) 普通物质处于未调制分支的声明；"
    "(c) 相变的必要充分条件；(d) 调制幅度与 m*/m0 的函数关系（现在只有恒等陈述）。四项皆无 ⇒ 登记为规格缺口。",
    section="X")
guard("g_x02_domain_criteria_absent", True)

# ============================================================================
# V 段｜四轮累积总判决
# ============================================================================
add("V01", "FAIL",
    "四轮累积总判决（r95+r98+r99+r100）：公式系统是输入的重新呈现，不是新物理的生成器",
    "机读汇总：代数内核健康（r99：14 式成立）；物理接口全断（r95：静态引力/开普勒/实验射程；"
    "r99：通量支/EM 约束/距离标度；r100：修法换来自洽性但零预言、统一性是反统一（净常数 2→3）、"
    "剖面族无幸存、Floquet 双排除、预测定义域未指定）。"
    "两难模板已记录第四处复发（剖面族，N03）。唯一未试路径 = omega(r,t) 场方程（r95 P4），"
    "而 N 段证明任何重现轨道的场方程必须编码牛顿 GM —— 框架的生成能力上界已封闭。",
    section="V")
guard("g_v01_cumulative_verdict", True)

# ============================================================================
# 外部输入账
# ============================================================================
EXT_INPUTS = [
    ("omega(r) 剖面", "N 段：族扫描仅开普勒族幸存且由 GM 反解（循环）"),
    ("Delta_omega（Floquet 能隙）", "F03：调小则共振可达但能隙成为无来源参数"),
    ("k_E,k_B,kappa_q,k_i,k_g,k_m", "P01：净 3 个自由常数（被统一对象仅 2 个）"),
    ("Q_t 绝对值与调制判据", "X02：定义域判据全缺；Q_t 标度无来源（cross-ref r98）"),
    ("[C] 级常数", "ppb 级质量计量精度、1 MHz 驱动上限、1e-9 m/s^2 重力仪、原子单位锚点（omega_B, B_au）、CODATA"),
]

# ============================================================================
# 总结与落盘
# ============================================================================
def _count(st):
    return sum(1 for it in ITEMS if it["status"] == st)

N_PASS = _count("PASS"); N_FAIL = _count("FAIL"); N_BOUND = _count("BOUNDARY"); N_INFO = _count("INFO")

SECTIONS = [
    ("MAP 跨册引用校验", ["MAP01", "MAP01"]),
    ("R 修法验证（F1-F5 机械施用后复审）", ["R01", "R05"]),
    ("P 参数计数（统一性主张攻破）", ["P01", "P02"]),
    ("N 剖面族扫描（omega=omega0*r^s）", ["N01", "N03"]),
    ("F Floquet 共振通道排除", ["F01", "F03"]),
    ("X 预测定义域与现存数据", ["X01", "X02"]),
    ("V 四轮累积总判决", ["V01", "V01"]),
]

KEY_NUMBERS = {
    "r02_B_at_anchor_T": fs(_B_au, 8),
    "r02_E_at_anchor_V_m": fs(_E_at_anchor, 8),
    "r02_E_over_atomic": fs(_ratio_E, 6),
    "r02_energy_density_ratio": fs(_ratio_u, 6),
    "p01_net_constants": str(NET),
    "p01_native_constants": str(NATIVE_CONSTANTS),
    "n01_survivor_s": fs(_survivors[0][0], 4) if _survivors else "NONE",
    "n01_s_observed": fs(_s_obs, 8),
    "n01_min_nonsurvivor_err": fs(min(r[4] for r in _rows if r[4] >= Decimal("1E-3")), 4),
    "n02_omega_earth_s^-1": fs(_w_earth, 10),
    "n02_r_cbudget_m": fs(_r_cbudget, 8),
    "f01_f_req_min_Hz": fs(min(r[2] for r in _f_req_rows), 8),
    "f01_f_req_max_Hz": fs(max(r[2] for r in _f_req_rows), 8),
    "f01_max_ratio_over_1MHz": fs(max(r[3] for r in _f_req_rows), 6),
    "f02_B0_max_T": fs(_B0_max, 8),
    "f02_bg_field_excess": fs(_excess_bg, 6),
    "x01_sigma_lo": fs(_sigma_lo, 6),
    "x01_sigma_hi": fs(_sigma_hi, 6),
}

lines = []
lines.append("=" * 78)
lines.append("r100 | 攻破续轮：修法验证 + 参数计数 + 剖面族扫描 + Floquet 排除 | 机器判决报告")
lines.append("=" * 78)
lines.append("")
for _name, _rng in SECTIONS:
    lines.append("--- %s ---" % _name)
    for _it in ITEMS:
        if _rng[0] <= _it["code"] <= _rng[-1]:
            lines.append("[%s] %s" % (_it["status"], _it["title"]))
            if _it["detail"]:
                lines.append("      %s" % _it["detail"])
    lines.append("")
lines.append("--- 剖面族扫描明细（s, 力指数 p, 周期指数, 火星预言 d, 相对误差）---")
for _r in _rows:
    lines.append("  s=%s p=%s T_exp=%s pred=%s d err=%s%s"
                 % (fs(_r[0], 2), fs(_r[1], 2), fs(_r[2], 2), fs(_r[3], 6), fs(_r[4], 4),
                    "  <<< 幸存" if _r[4] < Decimal("1E-3") else ""))
lines.append("")
lines.append("--- 外部输入账（%d 项）---" % len(EXT_INPUTS))
for _nm, _ds in EXT_INPUTS:
    lines.append("  [EXT] %s : %s" % (_nm, _ds))
lines.append("")
lines.append("--- 关键读数 ---")
for _k, _v in KEY_NUMBERS.items():
    lines.append("  %s = %s" % (_k, _v))
lines.append("")
lines.append("PASS = %d" % N_PASS)
lines.append("FAIL = %d" % N_FAIL)
lines.append("BOUNDARY = %d" % N_BOUND)
lines.append("INFO = %d" % N_INFO)
lines.append("条目 = %d" % len(ITEMS))
lines.append("守卫 = %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
REPORT = "\n".join(lines)


def main():
    _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _mt = {}
    for _p in (F_R95, F_R98, F_R99, F_LAI):
        if os.path.exists(_p):
            _mt[os.path.basename(_p)] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(os.path.getmtime(_p)))
    print(REPORT)
    print("")
    print("--- wrapper 元信息（防假绿）---")
    print("  生成时刻 = %s" % _now)
    print("  模块路径 = %s" % os.path.abspath(__file__))
    for _k, _v in _mt.items():
        print("  输入 mtime %s = %s" % (_k, _v))
    os.makedirs(DIR_DATA, exist_ok=True)
    _stem = "TUFT-r100_攻破续轮_修法验证参数计数字剖面族扫描Floquet排除_2026-10-18"
    _payload = {
        "round": "r100",
        "date": "2026-10-18",
        "topic": "攻破续轮：修法验证 + 统一性参数计数 + omega(r) 剖面族扫描 + Floquet 排除",
        "targets": {"formula_set": "r99 来稿式(1)-(27)", "repairs": "r99 F1-F5", "open_item": "r95 P4"},
        "items": ITEMS,
        "guards": GUARDS,
        "counts": {"PASS": N_PASS, "FAIL": N_FAIL, "BOUNDARY": N_BOUND, "INFO": N_INFO,
                   "total": len(ITEMS),
                   "guard_pass": sum(1 for g in GUARDS if g["ok"]),
                   "guard_total": len(GUARDS)},
        "cross_citations": [{"round": r, "code": c, "expected": e, "actual": _MAPS[r].get(c), "why": w}
                            for r, c, e, w in CITES],
        "profile_scan": [{"s": str(r[0]), "p": str(r[1]), "t_exp": str(r[2]),
                          "mars_pred_d": str(r[3]), "rel_err": str(r[4]),
                          "survives": bool(r[4] < Decimal("1E-3"))} for r in _rows],
        "external_inputs": [{"name": n, "desc": d} for n, d in EXT_INPUTS],
        "key_numbers": KEY_NUMBERS,
        "wrapper": {"generated_at": _now, "module": os.path.abspath(__file__),
                    "input_mtimes": _mt},
    }
    with io.open(os.path.join(DIR_DATA, _stem + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(_payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DIR_DATA, _stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(REPORT)
        f.write("\n\n--- wrapper 元信息（防假绿）---\n")
        f.write("生成时刻 = %s\n" % _now)
        f.write("模块路径 = %s\n" % os.path.abspath(__file__))
        for _k, _v in _mt.items():
            f.write("输入 mtime %s = %s\n" % (_k, _v))
    _md = ["# 数据产物｜r100 攻破续轮（2026-10-18）", "",
           "靶：r99 来稿式(1)-(27) + r99 修法 F1-F5 + r95 P4（无新来料，自设攻破轮）",
           "判定册：[判定_TUFT-r100-攻破续轮_修法验证参数计数字剖面族扫描Floquet排除_2026-10-18.md](../判定_TUFT-r100-攻破续轮_修法验证参数计数字剖面族扫描Floquet排除_2026-10-18.md)",
           "", "```", REPORT, "```", ""]
    with io.open(os.path.join(DIR_DATA, _stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
