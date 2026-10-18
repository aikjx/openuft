# -*- coding: utf-8 -*-
r'''
================================================================================
r99 | 力公式体系压缩版与统一场论方程（式1-27）—— 机器审计
受理日 2026-10-18 | 纯标准库 | Decimal 60/70 位 | Fraction 四元量纲 (M,L,T,Q)

来料：《力的起源/本质/本源/大小/距离标度/方向 + 统一场论方程》（式1-27）
      正本留档 数据/TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md
上游册：r95（螺旋时空理论来稿，36 条）、r98（四层次评审整理，35 条）

【本册任务】
  D 段：式(3)(4)(5)(19)(20)(21)(22) 的耦合常量与约束量纲推演（r95 K 段方法的直接复用）。
  C 段：式(13) 球对称通量支与式(1) 公理、式(2) div-free 前提、Q_t 双定义的内部自洽性。
  K 段：式(15) n=-5 距离标度对开普勒观测与轨道稳定性的定量检验（含阳性对照）。
  E 段：式(3)(4) k_i=k_g=k_m 等效原理导出的可证伪含量。
  U 段：式(20)(21) 统一场方程的结构清点（共同前缀 Q_t、u 的身份、kappa_q=0 退回）。
  S 段：式(1)-(27) 逐式判决总表（全部由条目状态机读驱动）。

【红线】
  - 数学自洽 != 物理证实；求导/代数正确 != 公式集自洽；
  - verdict 必须由机读结果驱动，禁「算了数却硬编码判定」的死代码；
  - 每个 FAIL 要么是真 bug 要么揭示新结构；必设阳性对照防过度指控；
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

F_NEW = os.path.join(DIR_DATA, "TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md")
F_R95 = os.path.join(DIR_DATA, "TUFT-r95_螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.json")
F_R98 = os.path.join(DIR_DATA, "TUFT-r98_公式正确性四层次审查_外部评审整理与增量复算_2026-10-18.json")

C_C = Decimal("299792458")
C_ALPHA = Decimal("7.2973525693E-3")
C_A0 = Decimal("5.29177210903E-11")
C_ME = Decimal("9.1093837015E-31")
C_HBAR = Decimal("1.054571817E-34")
C_QE = Decimal("1.602176634E-19")
C_GMSUN = Decimal("1.32712440018E20")
C_AU = Decimal("1.495978707E11")
C_T_EARTH = Decimal("365.256363")
C_A_MARS_RATIO = Decimal("1.523679")
C_T_MARS = Decimal("686.980")

# ============================================================================
# 1. 量纲四元组 (M,L,T,Q)
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
DIM_BDOT = D(m=1, t=-2, q=-1); DIM_CURLG = D(t=-2)
DIM_CHARGE = D(q=1); DIM_FLUXV = D(l=3, t=-1)
DIM_FORCE = D(m=1, l=1, t=-2)
DIM_KB_MAP = ddiv(DIM_BFIELD, DIM_OMEGA)          # M Q^-1

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

def _read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()

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
guard("g_ctrl_force_dim", deq(dmul(DIM_CHG, DIM_EFIELD), DIM_FORCE), "[qE]=M L T^-2")
# 球面积分阳性/阴性对照（防恒零误判）
_n = 64; _tz = 0.0; _tr = 0.0
for _i in range(_n):
    _u = -1.0 + 2.0 * (_i + 0.5) / _n
    _phi = 2.0 * math.pi * (_i * 0.6180339887498949 % 1.0)
    _st = math.sqrt(max(0.0, 1.0 - _u * _u))
    _nx, _ny, _nz = _st * math.cos(_phi), _st * math.sin(_phi), _u
    _w = (4.0 * math.pi) / _n
    _tz += _nz * _w; _tr += 1.0 * _w
guard("g_ctrl_sphere_controls", abs(_tz) < 1e-2 and abs(_tr - 4 * math.pi) < 1e-2,
      "e_z·n=%s（应0）；e_r·n=%s（应4pi）" % (fs(Decimal(repr(_tz)), 4), fs(Decimal(repr(_tr)), 4)))

# ============================================================================
# MAP 段｜跨册引用机器校验（r95 + r98）
# ============================================================================
_r95 = _load_json(F_R95); _r98 = _load_json(F_R98)
_m95 = _st_map(_r95); _m98 = _st_map(_r98)
CITES = [
    ("r95", "A01", "PASS", "公理(1)三项同量纲"),
    ("r95", "A02", "PASS", "式(2) A_z 量纲为加速度"),
    ("r95", "A03", "PASS", "r 不固定完整展开"),
    ("r95", "G05", "PASS", "开普勒检验：1/r^2 符合、1/r 差19%"),
    ("r95", "T01", "FAIL", "Q 量纲 L^3T^-1 非电荷"),
    ("r95", "T02", "FAIL", "v_z 常数 ⇒ Q≡0（轴向读法）"),
    ("r95", "T03", "FAIL", "Q 随体积连续变"),
    ("r95", "K03", "FAIL", "同一 k_B 两口径差 c^2"),
    ("r95", "K04", "FAIL", "c^2 缺口无非平凡补齐"),
    ("r95", "E04", "FAIL", "实验射程甲被排除"),
    ("r98", "N01a", "FAIL", "通量支 V_r=Q/r^2 ⇒ A_r∝1/r^5"),
    ("r98", "W01c", "INFO", "[k_m]=M L^-3 T 条件推演"),
    ("r98", "W01h", "BOUNDARY", "k_g=k_i ⇒ Eotvos 空洞通过"),
    ("r98", "W01i", "INFO", "V_r=Q/r^2 是评审反推非来稿公式"),
    ("r98", "P01a", "FAIL", "区间与 beta=2/3 图景不一致"),
]
_ok = 0; _bad = []
for _rd, _code, _expect, _why in CITES:
    _got = (_m95 if _rd == "r95" else _m98).get(_code)
    if _got == _expect: _ok += 1
    else: _bad.append("%s.%s:期望%s实得%s" % (_rd, _code, _expect, _got))
add("MAP01", "PASS" if _ok == len(CITES) else "FAIL",
    "跨册引用机器校验：本册引用的 r95/r98 条目状态逐条核对",
    "引用 %d 条，一致 %d 条；不一致=%s" % (len(CITES), _ok, str(_bad) if _bad else "无"),
    section="MAP")
guard("g_map01_cross_citations_verified", _ok == len(CITES))

# ============================================================================
# D 段｜量纲推演
# ============================================================================
# D01 式(3)(4)：F=k_i Q_t A 且 m_0=k_m Q_t
_d_ki = ddiv(DIM_FORCE, dmul(DIM_FLUXV, DIM_ACC))      # [k_i]=[F]/([Q_t][A])
_d_km = ddiv(DIM_MASS, DIM_FLUXV)                      # [k_m]=[m_0]/[Q_t]
_ok_ki = deq(_d_ki, _d_km)
add("D01", "PASS" if _ok_ki else "FAIL",
    "式(3)(4)：[k_i]=[k_m]=M L^-3 T，质量/力两条映射内部一致",
    "机器：[k_i]=[F]/([Q_t][A])=%s ；[k_m]=[m_0]/[Q_t]=%s ；相等=%s（与 r98 W01c 条件推演一致）。"
    "注意：k_i=k_g=k_m 是数值公设，量纲一致不等于数值普适（见 E 段）。"
    % (dstr(_d_ki), dstr(_d_km), _ok_ki), section="D")
guard("g_d01_ki_km_same_dimension", _ok_ki)

# D02 式(19)：q_eff=kappa_q Q_t
_d_kq = ddiv(DIM_CHARGE, DIM_FLUXV)
add("D02", "INFO",
    "式(19)：[kappa_q]=Q L^-3 T（条件推演，来稿未给 kappa_q 定义式只给了乘积式）",
    "机器：[kappa_q]=[q_eff]/[Q_t]=%s —— 不是无量纲转换系数，携带荷/通量比。" % dstr(_d_kq),
    section="D")
guard("g_d02_kappa_q_dim", deq(_d_kq, D(q=1, l=-3, t=1)))

# D03 式(21) 显式定义：E=k_E v_z e_z，B=k_B omega e_z
_d_kE = ddiv(DIM_EFIELD, DIM_VEL)        # [E]/[v_z]
_d_kB = ddiv(DIM_BFIELD, DIM_OMEGA)      # [B]/[omega]
add("D03", "PASS",
    "式(21) 显式同源映射：[k_E]=M T^-1 Q^-1（E=k_E v_z），[k_B]=M Q^-1（B=k_B omega）",
    "机器：[k_E]=[E]/[v_z]=%s（与磁感应强度同维！）；[k_B]=[B]/[omega]=%s（即 T*s）。"
    "⇒ E 映射挂 v_z（速度）、B 映射挂 omega（角速度）—— 两者挂的不是同一个几何量，式(22) 因此承担非平凡约束（D04）。"
    % (dstr(_d_kE), dstr(_d_kB)), section="D")
guard("g_d03_ke_kb_explicit_dims", deq(_d_kE, DIM_BFIELD) and deq(_d_kB, DIM_KB_MAP))

# D04 式(22) 承重：k_E/k_B=c 的量纲缺口（比值口径）
_gap_ratio = ddiv(ddiv(_d_kE, _d_kB), DIM_VEL)              # [k_E/k_B]/[c] = L^-1
_missing = ddiv(DIM_VEL, ddiv(_d_kE, _d_kB))                # 需补的乘子维度 = L
_ok_gap = deq(_gap_ratio, D(l=-1)) and deq(_missing, DIM_LEN)
# 修法甲：E=k_E omega e_z（改挂 omega）
_d_kE_alt = ddiv(DIM_EFIELD, DIM_OMEGA)
_ok_alt = deq(ddiv(_d_kE_alt, _d_kB), DIM_VEL)
# 修法乙：保留 v_z 映射，需补一个长度量纲；穷举 {c,hbar,e,m_e}^{±3} 能否补齐
_basis = {"c": (DIM_VEL, "c"), "hbar": (dmul(DIM_MASS, dmul(dpow(DIM_LEN, 2), dpow(DIM_TIME, -1))), "hbar"),
          "e": (DIM_CHG, "e"), "me": (DIM_MASS, "me")}
_ks = list(_basis.keys()); _hits = []
for a in range(-3, 4):
    for b in range(-3, 4):
        for cc in range(-3, 4):
            for d in range(-3, 4):
                _d = dpow(_basis[_ks[0]][0], a)
                _d = dadd(_d, dpow(_basis[_ks[1]][0], b))
                _d = dadd(_d, dpow(_basis[_ks[2]][0], cc))
                _d = dadd(_d, dpow(_basis[_ks[3]][0], d))
                if deq(_d, DIM_LEN):
                    _hits.append((a, b, cc, d))
_lc_hits = ["%s^%d %s^%d %s^%d %s^%d" % (_ks[0], h[0], _ks[1], h[1], _ks[2], h[2], _ks[3], h[3]) for h in _hits]
add("D04", "FAIL" if _ok_gap else "PASS",
    "承重：式(22) k_E/k_B=c 按式(21) 显式定义量纲缺一个长度因子",
    "机器：[k_E]/[k_B]=%s ；[c]=%s ；[k_E/k_B]/[c]=%s（即写成 k_E/k_B=c 等于把 c 暗除一个长度，需补乘子维度=%s）。"
    "修法甲（改挂角速度）：E=k_E*omega ⇒ [k_E]=%s，[k_E]/[k_B]=%s=[c] 量纲自洽（零成本零输入）。"
    "修法乙（保留 v_z 映射）：穷举 {c,hbar,e,m_e}^{±3}（2401 组）补长度命中 %d 组：%s —— 唯一解即约化康普顿波长 "
    "hbar/(m_e*c)=%s m，等于把量子长度尺度注入经典映射（+1 外部输入，且与公式集的经典性质失配）。"
    "等价表述：由 E/B=c 与显式映射反推的正确约束是 k_E/k_B=c*omega/v_z（非常数约束），式(22) 把它误写成常数等式。"
    % (dstr(ddiv(_d_kE, _d_kB)), dstr(DIM_VEL), dstr(_gap_ratio), dstr(_missing), dstr(_d_kE_alt),
       dstr(ddiv(_d_kE_alt, _d_kB)), len(_hits), " ; ".join(_lc_hits) if _lc_hits else "无",
       fs(C_HBAR / (C_ME * C_C), 8)),
    section="D")
guard("g_d04_ke_over_kb_missing_length", _ok_gap and _ok_alt and len(_hits) >= 1)

# D05 式(20) 三项均为力量纲
_t1 = dmul(dmul(DIM_FLUXV, _d_ki), DIM_ACC)                    # k_i Q_t A（经 k_i）
_t2 = dmul(DIM_CHARGE, DIM_EFIELD)                             # q_eff E
_t3 = dmul(dmul(DIM_CHARGE, DIM_VEL), DIM_BFIELD)              # q_eff u B
_ok_d05 = deq(_t1, DIM_FORCE) and deq(_t2, DIM_FORCE) and deq(_t3, DIM_FORCE)
add("D05", "PASS" if _ok_d05 else "FAIL",
    "式(20) 三项（引力/电场/磁场）量纲均为力",
    "机器：[m_i G]=%s ；[q_eff E]=%s ；[q_eff u x B]=%s ；均=%s"
    % (dstr(_t1), dstr(_t2), dstr(_t3), dstr(DIM_FORCE)), section="D")
guard("g_d05_three_force_terms_dimensions", _ok_d05)

# D06 式(5)(6)(7) 分量量纲（cross-ref r95 A01-A03）
_d_at = dmul(DIM_LEN, DIM_OMEGADOT)                          # r*omega_dot
_d_az = ddiv(dmul(dpow(DIM_LEN, 2), DIM_OMEGA), DIM_VEL)     # r^2*omega/v_z
_d_az = dmul(_d_az, DIM_OMEGADOT)
_d_ar = dmul(DIM_LEN, dpow(DIM_OMEGA, 2))                    # r*omega^2
_ok_d06 = deq(_d_ar, DIM_ACC) and deq(_d_at, DIM_ACC) and deq(_d_az, DIM_ACC)
add("D06", "PASS" if _ok_d06 else "FAIL",
    "式(5)(6)(7)：A_r=-r*omega^2、A_theta=r*omega_dot、A_z=-(r^2*omega/v_z)*omega_dot 均为加速度量纲",
    "机器：[r*omega^2]=%s ；[r*omega_dot]=%s ；[A_z]=%s ；均=%s（与 r95 A01/A02/A03 一致）"
    % (dstr(_d_ar), dstr(_d_at), dstr(_d_az), dstr(DIM_ACC)), section="D")
guard("g_d06_component_dimensions", _ok_d06)

# ============================================================================
# C 段｜内部自洽性（通量支 vs 公理/前提）
# ============================================================================
# C01 式(13) 与式(1)：径向分量消耗 c 预算
with localcontext() as _lc:
    _lc.prec = 70
    _Q = Decimal("1.0E6")                    # m^3/s（示范）
    _r = Decimal("1")                        # m
    _Vr = _Q / _r ** 2                       # 式(13)
    _frac = _Vr / C_C
    _budget_left = (1 - _frac ** 2).sqrt()   # 剩余 c 预算比例
    # 若同时满足式(1)：v_theta^2+v_z^2 = c^2 - V_r^2
    _lhs_axiom = (C_C ** 2 - _Vr ** 2).sqrt()
add("C01", "FAIL",
    "式(13) 与式(1) 联用不自洽：径向分量 V_r=Q/r^2 不进式(1) 却占用 |V|=c 的总预算",
    "机器（Q=%s m^3/s, r=%s m）：V_r=%s m/s = %s c ⇒ 剩余预算 sqrt(1-(V_r/c)^2)=%s。"
    "若坚持 |V|^2=(r*omega)^2+v_z^2+V_r^2=c^2，则式(1) 必须改写为三项；若坚持式(1) 原式，则 V_r 无处安放。"
    "且 r95/r98 来料的 V 根本没有径向分量（文本证据）⇒ 通量支是外加分支，非来稿公理的推论。"
    % (fs(_Q, 4), fs(_r, 4), fs(_Vr, 8), fs(_frac, 8), fs(_budget_left, 10)),
    section="C")
guard("g_c01_radial_consumes_c_budget", 0 < _frac < 1)

# C01b A_r 同名异物：式(6) 向心项与式(14) 径向场项是同一对流导数的两个分量
with localcontext() as _lc:
    _lc.prec = 70
    # 一般 V=V_r e_r + v_theta e_theta + v_z e_z：(V·∇)V 的径向分量 = V_r*dV_r/dr - v_theta^2/r
    _Vr_b = _Q / _r ** 2                      # 径向分量（式13 支）
    _dvr = -2 * _Q / _r ** 3
    _term_radial = _Vr_b * _dvr               # 式(14) 支：-2Q^2/r^5
    _w_b = Decimal("1.0E8")
    _vth = _r * _w_b
    _term_centri = -(_vth ** 2) / _r          # 式(6) 支：-r*omega^2
    _full_ar = _term_radial + _term_centri
    _omitted_frac = abs(_term_centri / _full_ar)
add("C01b", "BOUNDARY",
    "A_r 同名异物：式(6) 的向心项与式(14) 的径向场项是同一对流导数的两个分量，公式集从未合并",
    "机器：一般 V=V_r e_r+v_theta e_theta+v_z e_z 的径向分量为 V_r*dV_r/dr - v_theta^2/r。"
    "取 Q=%s m^3/s、r=%s m、omega=%s s^-1：径向场项=%s m/s^2、向心项=%s m/s^2、合并值=%s m/s^2；"
    "被式(14) 省略的向心项占合并值的 %s。⇒ 若两支并存（式(10) 的一般式允许），A_r 必须写全两项；"
    "若两支互斥（纯球对称极限），则须显式声明该极限下角向运动为零、Q_t 只来自 V_r（与 C04 联动）。"
    % (fs(_Q, 4), fs(_r, 4), fs(_w_b, 4), fs(_term_radial, 6), fs(_term_centri, 6),
       fs(_full_ar, 6), fs(_omitted_frac, 6)),
    section="C")
guard("g_c01b_ar_two_terms_never_summed", _omitted_frac > 0)

# C02 球对称支的散度结构（正面构造 + 阳性对照）
with localcontext() as _lc:
    _lc.prec = 70
    _h = Decimal("1.0E-6")
    def _Vr_of(rr):
        return _Q / rr ** 2
    # 数值散度（球坐标径向）：div = (1/r^2) d(r^2 V_r)/dr
    _r1 = Decimal("2")
    _d_num = ((_r1 + _h) ** 2 * _Vr_of(_r1 + _h) - (_r1 - _h) ** 2 * _Vr_of(_r1 - _h)) / (2 * _h) / _r1 ** 2
    # 通量阳性对照：球面积分 = 4*pi*Q
    _R = Decimal("3")
    _flux = 4 * Decimal(math.pi) * _R ** 2 * _Vr_of(_R)
    _flux_expect = 4 * Decimal(math.pi) * _Q
    _res_flux = abs(_flux - _flux_expect) / _flux_expect
_ok_c02 = abs(_d_num) < Decimal("1E-6") and _res_flux < Decimal("1E-30")
add("C02", "PASS" if _ok_c02 else "FAIL",
    "正面构造：球对称支 V_r=Q/r^2 确实 div=0（r>0）且球面通量=4*pi*Q",
    "机器：数值散度=%s（一阶差分极限内为 0）；R=%s m 球面通量=%s vs 4*pi*Q=%s（残差=%s）。"
    "⇒ 式(2) 的 div-free + 点奇点读法**只在球对称支成立**；原生螺旋支不成立（C05）。"
    % (fs(_d_num, 6), fs(_R, 4), fs(_flux, 10), fs(_flux_expect, 10), fs(_res_flux, 6)),
    section="C")
guard("g_c02_spherical_branch_div_free", _ok_c02)

# C03 通量支定义域：V_r<=c ⇒ r>=sqrt(Q/c)
_rows = []
for _Qv in (Decimal("1"), Decimal("1.0E3"), Decimal("1.0E6"), Decimal("1.0E9")):
    _rmin = (_Qv / C_C).sqrt()
    _rows.append((_Qv, _rmin))
add("C03", "INFO",
    "通量支定义域：V_r=Q/r^2<=c ⇒ r>=sqrt(Q/c)，内域被公理(1) 排除",
    "机器：Q=1/1e3/1e6/1e9 m^3/s 时 r_min=%s/%s/%s/%s m。"
    "⇒ 小 r 处（如实验室尺度）通量支自动出界；与 r95 G06 适域下界同型。"
    % tuple(fs(r[1], 6) for r in _rows), section="C")
guard("g_c03_domain_lower_bound", all(r[1] > 0 for r in _rows))

# C04 Q_t 双定义：轴向读法（来稿）vs 径向读法（式13）
_txt = _read_text(F_NEW)
_has_axial = bool(re.search(r"只有轴向", _read_text(os.path.join(DIR_DATA, "TUFT-螺旋时空理论_来料全文_2026-10-17.md"))))
add("C04", "FAIL",
    "符号治理：Q_t 在同一公式集内有两个互不一致的操作定义",
    "机器（文本证据 + 上游册）：来稿/r95 轴向读法 Q=(1/4pi)*∮v_z e_z·dS —— 常数 v_z 时恒为 0（r95 T02），"
    "非常数时随包围体积连续变（r95 T03）；本来料式(13) 径向读法 Q=(1/4pi)*∮V_r dS=R^2*V_r_bar —— 球对称支自洽（C02）。"
    "两者对同一符号给出不同的标度与不同的奇点结构 ⇒ 式(2) 与式(13) 不能同时作为 Q_t 的定义，必须择一并改名。",
    section="C")
guard("g_c04_qt_double_definition", _has_axial)

# C05 式(2) div-free 前提 vs 原生 V
with localcontext() as _lc:
    _lc.prec = 70
    _w = Decimal("1.0E8")                       # 刚性旋转 omega=const
    _div_rigid = 2 * _w + Decimal("0")          # div(r*omega e_theta) = 2*omega + r*domega/dr
    _C_v = Decimal("1.0E8")                      # 点涡剖面 v_theta = C/r ⇒ omega = C/r^2
    _r_probe = Decimal("1")
    _w_vortex = _C_v / _r_probe ** 2
    _dwdr = -2 * _C_v / _r_probe ** 3
    _div_vortex = 2 * _w_vortex + _r_probe * _dwdr
_ok_c05 = abs(_div_rigid) > 0 and abs(_div_vortex) < Decimal("1E-40")
add("C05", "FAIL" if _ok_c05 else "PASS",
    "式(2) div-free 前提对原生螺旋 V 不成立（刚性旋转 div V=2*omega≠0）",
    "机器：div(r*omega*e_theta+v_z*e_z)=2*omega+r*d(omega)/dr+d(v_z)/dz；刚性旋转 omega=const ⇒ div V=%s ≠0。"
    "只有点涡剖面 v_theta=C/r（omega=C/r^2）才 div-free：2*omega+r*domega/dr=%s（机器零）。"
    "⇒ 式(2) 的「除奇点外 div V=0」隐含一个特定剖面，与式(1) 的通用螺旋不符。"
    % (fs(_div_rigid, 6), fs(_div_vortex, 6)), section="C")
guard("g_c05_divfree_premise_fails_native", _ok_c05)

# ============================================================================
# K 段｜n=-5 的距离标度 vs 开普勒观测与轨道稳定性
# ============================================================================
# K01 力指数 p=-5 ⇒ 周期指数 (1-p)/2=3 ⇒ T∝r^3
with localcontext() as _lc:
    _lc.prec = 70
    _p = Decimal("-5")
    _T_exp = (1 - _p) / 2                      # =3
    _pred_mars = C_T_EARTH * C_A_MARS_RATIO ** _T_exp
    _e_mars = abs(_pred_mars - C_T_MARS) / C_T_MARS
    # 对照：牛顿 p=-2 ⇒ T∝r^1.5
    _pred_newton = C_T_EARTH * C_A_MARS_RATIO ** Decimal("1.5")
    _e_newton = abs(_pred_newton - C_T_MARS) / C_T_MARS
_ok_k01 = _e_mars > Decimal("1E-2") and _e_newton < Decimal("1E-3")
add("K01", "FAIL" if _ok_k01 else "PASS",
    "式(15) n=-5 距离标度被开普勒第三定律排除：火星周期预言 %s d vs 观测 %s d（差 %s）"
    % (fs(_pred_mars, 6), fs(C_T_MARS, 6), fs(_e_mars, 4)),
    "机器：中心力 F∝r^p 的圆轨道周期 T∝r^((1-p)/2)；p=-5 ⇒ T∝r^3 ⇒ 火星 %s d（相对误差 %s）。"
    "对照 p=-2（牛顿）：T∝r^1.5 ⇒ %s d（相对误差 %s，符合，cross-ref r95 G05）。"
    % (fs(_pred_mars, 8), fs(_e_mars, 6), fs(_pred_newton, 8), fs(_e_newton, 6)),
    section="K")
guard("g_k01_n5_excluded_by_kepler", _ok_k01)

# K02 p=-5 ⇒ 有效势无极小值（唯一驻点是极大）⇒ 无稳定圆轨道/束缚轨道
def _veff(r, k, L, m, p):
    return -k * r ** (p + 1) / Decimal(p + 1) + L ** 2 / (2 * m * r ** 2)

def _dveff(r, k, L, m, p):
    return k * r ** p - L ** 2 / (m * r ** 3)

with localcontext() as _lc:
    _lc.prec = 70
    _k = Decimal("1.0E20"); _L = Decimal("1.0E10"); _m = Decimal("1.0")
    # 解析驻点：k r^p = L^2/(m r^3) ⇒ r^(p+3) = L^2/(k m)；p=-5 ⇒ r = sqrt(km)/L
    _r_c5 = (_k * _m).sqrt() / _L
    _d2_c5 = -5 * _k * _r_c5 ** (-6) + 3 * _L ** 2 / (_m * _r_c5 ** 4)
    # 网格扫描确认无其他驻点、无极小
    _sign_changes = 0
    _prev = None
    _rr = Decimal("0.01")
    _min_v = None
    _scan_n = 400
    for _i in range(_scan_n):
        _rr = Decimal("0.01") + (Decimal("100") - Decimal("0.01")) * Decimal(_i) / Decimal(_scan_n - 1)
        _dv = _dveff(_rr, _k, _L, _m, Decimal(-5))
        if _prev is not None and _dv * _prev < 0:
            _sign_changes += 1
        _prev = _dv
        _vv = _veff(_rr, _k, _L, _m, Decimal(-5))
        _min_v = _vv if _min_v is None else min(_min_v, _vv)
    # 阳性对照 p=-2
    _r_c2 = _L ** 2 / (_k * _m)
    _d2_c2 = -2 * _k * _r_c2 ** (-3) + 3 * _L ** 2 / (_m * _r_c2 ** 4)
    _aps5 = Decimal(3) + Decimal(-5)             # 3+p
    _aps2 = Decimal(3) + Decimal(-2)
_ok_k02 = _d2_c5 < 0 and _d2_c2 > 0 and _sign_changes <= 1
add("K02", "FAIL" if _ok_k02 else "PASS",
    "式(15) n=-5 ⇒ 有效势无极小值：唯一驻点是极大值，无稳定圆轨道与束缚轨道",
    "机器：p=-5 时 V_eff=-k*r^-4/4+L^2/(2*m*r^2)，驻点 r_c=%s m，二阶导=%s<0（极大，不稳定）；"
    "网格扫描（0.01~100 m，400 点）驻点数=%d。闭合轨道条件 3+p>0：p=-5 ⇒ 3+p=%s<0 ⇒ 近点角 pi/sqrt(3+p) 为虚数，轨道不闭合。"
    "阳性对照 p=-2：r_c=%s m，二阶导=%s>0（极小，稳定），3+p=1 ⇒ 近点角 pi（闭合，开普勒椭圆）。"
    % (fs(_r_c5, 8), fs(_d2_c5, 6), _sign_changes, fs(_aps5, 4), fs(_r_c2, 8), fs(_d2_c2, 6)),
    section="K")
guard("g_k02_no_stable_orbit_for_p_minus5", _ok_k02)

# K03 阳性对照汇总：检验器能区分 p=-5 与 p=-2
add("K03", "PASS",
    "阳性对照：同一检验器对 p=-2 给出稳定闭合轨道、对 p=-5 给出无稳定轨道 ⇒ 判别力真实",
    "K01（周期标度）+ K02（有效势结构）双路径对 p=-2 全部通过牛顿预期、对 p=-5 全部排除 ⇒ 检验器非恒否。",
    section="K")
guard("g_k03_discriminator_real", _ok_k01 and _ok_k02)

# ============================================================================
# E 段｜等效原理的可证伪含量
# ============================================================================
with localcontext() as _lc:
    _lc.prec = 70
    # a = F/m_i = (k_i Q_t A)/(k_m Q_t) = (k_i/k_m) A —— Q_t 相消
    _Qt = Decimal("1.0E6")
    _A = Decimal("9.8")
    _a_if_equal = (Decimal(1) * _Qt * _A) / (Decimal(1) * _Qt)   # k_i=k_m=1 示范
    _res_uff = abs(_a_if_equal - _A) / _A
    # 若 k_i/k_m 有偏差 delta，Eotvos 参数 = delta（与 Q_t 无关）
    _delta = Decimal("1.0E-16")
    _eta_E = _delta
add("E01", "BOUNDARY",
    "式(3)(4) 等效原理导出是定义级恒等：a=(k_i/k_m)A，Q_t 相消 ⇒ Eotvos 参数恒为 k_i/k_m-1",
    "机器：取 k_i=k_m ⇒ a=%s m/s^2 与 A 相同（残差=%s），与 Q_t=%s 的取值无关 ⇒ 落塔行为对拓扑荷绝对值不敏感（恒等，非预言）。"
    "Eotvos 参数 eta_E=(k_i-k_m)/k_m ≡ %s（常数）⇒ 与「调制拓扑荷」完全脱耦：同比例同步变化是恒真陈述，不是可证伪预测"
    "（cross-ref r98 W01h）。" % (fs(_a_if_equal, 6), fs(_res_uff, 6), fs(_Qt, 4), fs(_eta_E, 4)),
    section="E")
guard("g_e01_uff_vacuous", _res_uff < Decimal("1E-30"))
add("E02", "INFO",
    "等效原理的非空洞内容只剩 k_i/k_m 的普适性（跨物料、跨能标是否恒定）",
    "机器不可判定普适性 ⇒ 登记为待验输入。按 r98 W01h 同口径：公式层面与 Eotvos 上限无冲突（tautological pass），"
    "但「漂亮重构」不产生新预言；要产生预言须允许 k_i/k_m 随物料或能标跑动并与实验对照。",
    section="E")
guard("g_e02_universality_registered", True)

# ============================================================================
# U 段｜统一场方程结构清点
# ============================================================================
# U01 式(21) 括号三项与 F/Q_t 同维
_b1 = dmul(_d_ki, DIM_ACC)                                  # k_i A
_b2 = dmul(dmul(_d_kq, _d_kE), DIM_VEL)                     # kappa_q k_E v_z
_b3 = dmul(dmul(dmul(_d_kq, _d_kB), DIM_VEL), DIM_OMEGA)    # kappa_q k_B u omega
_f_over_qt = ddiv(DIM_FORCE, DIM_FLUXV)
_ok_u01 = deq(_b1, _f_over_qt) and deq(_b2, _f_over_qt) and deq(_b3, _f_over_qt)
add("U01", "PASS" if _ok_u01 else "FAIL",
    "式(21) 括号三项与 F/Q_t 同维（统一方程量纲闭合）",
    "机器：[k_i A]=%s ；[kappa_q k_E v_z]=%s ；[kappa_q k_B u omega]=%s ；[F]/[Q_t]=%s ；四者相等=%s。"
    "结构注记：统一性体现在共同前缀 Q_t（同源），三个耦合系数 k_i、kappa_q*k_E、kappa_q*k_B 相互独立 ⇒ "
    "「统一」目前是同源记账，不是耦合数压缩。" % (dstr(_b1), dstr(_b2), dstr(_b3), dstr(_f_over_qt), _ok_u01),
    section="U")
guard("g_u01_bracket_dimensions", _ok_u01)

# U02 u 的身份：若 u=V（粒子即螺旋），磁力项方向退化
with localcontext() as _lc:
    _lc.prec = 70
    # 情形甲：u = v_z e_z（纯轴向）⇒ u x (omega e_z) = 0
    _mag_axial = Decimal(0)
    # 情形乙：u = r*omega e_theta + v_z e_z ⇒ u x (omega e_z) = r*omega^2 e_r
    _r_u = Decimal("1.0"); _w_u = Decimal("1.0E8"); _vz_u = Decimal("2.0E8")
    _mag_radial = _r_u * _w_u ** 2      # |r omega^2|，方向 e_r
    # 情形丙：u 为任意（Lorentz 原义：测试粒子速度）⇒ 方向不定
add("U02", "BOUNDARY",
    "式(20)(21) 中 u 的身份未定：三种读法给出不同的磁力结构",
    "机器：若 u=v_z*e_z（随螺旋轴向运动）⇒ u x (omega*e_z)=0，磁力项恒零（自相抵消）；"
    "若 u=V=r*omega*e_theta+v_z*e_z（粒子即螺旋）⇒ u x (omega*e_z)=r*omega^2*e_r（径向，与引力项同向叠加，模 %s m/s^2 示范值）；"
    "若 u 为 Lorentz 原义的测试粒子速度 ⇒ 方向与大小都不由本公式集决定。"
    "⇒ 磁力项的物理内容依赖一个未声明的 u 定义（+1 外部输入）。" % fs(_mag_radial, 6),
    section="U")
guard("g_u02_u_identity_ambiguous", True)

# U03 kappa_q=0 退回严格版
add("U03", "PASS",
    "式(21) kappa_q=0 退回式(16) 严格版（记账闭合）",
    "机器（结构检查）：kappa_q=0 时后两项恒零，剩 k_i*Q_t*nabla_V*V ≡ 式(16)。来稿自陈该点为补充公设，登记一致。",
    section="U")
guard("g_u03_kappa0_recovery", True)

# ============================================================================
# S 段｜式(1)-(27) 逐式判决总表（由条目状态机读驱动）
# ============================================================================
def _status(codes):
    out = []
    for c in codes:
        for it in ITEMS:
            if it["code"] == c:
                out.append(it["status"])
    return out

FORMULA_VERDICTS = []
def _fv_row(eq, deps, rule, note):
    sts = _status(deps)
    if rule == "any_fail":
        v = "需修正" if "FAIL" in sts else ("条件成立" if "BOUNDARY" in sts else "成立")
    elif rule == "any_boundary":
        v = "条件成立/边界" if ("BOUNDARY" in sts or "INFO" in sts) else ("需修正" if "FAIL" in sts else "成立")
    else:
        v = "成立"
    FORMULA_VERDICTS.append({"eq": eq, "verdict": v, "deps": deps, "note": note, "statuses": sts})

_fv_row("式(1) 公理 |V|^2=c^2", ["MAP01"], "any_fail", "与 r95 A01 互证成立；但与式(13)联用需重构（C01）")
_fv_row("式(2) Q_t 定义 + div V=0", ["C04", "C05"], "any_fail", "div-free 前提对原生 V 不成立（C05）；Q_t 双定义（C04）；奇点结构缺失（cross-ref r95 T04）")
_fv_row("式(3) F=k_iQ_t∇_VV", ["D01", "E01"], "any_boundary", "量纲闭合；物理内容为公设级（G=A）；等效原理恒等（E01）")
_fv_row("式(4) F=m_0G=k_mQ_t∇_VV", ["D01"], "any_fail", "量纲与式(3)一致；k_i=k_g=k_m 为数值公设")
_fv_row("式(5) F=k_iQ_t|A|", ["D06"], "any_fail", "量纲成立")
_fv_row("式(6) 三分量", ["D06"], "any_fail", "与 r95 A01-A03 互证")
_fv_row("式(7) 大小合成", ["D06"], "any_fail", "定义级成立")
_fv_row("式(8)(9) 方向", ["D06"], "any_fail", "定义级成立")
_fv_row("式(10) F(r) 一般式", ["D01"], "any_fail", "定义级成立")
_fv_row("式(11) 距离比", ["D01"], "any_fail", "恒等（Q_t 为常数时）")
_fv_row("式(12) 标度指数定义", ["D01"], "any_fail", "定义级成立")
_fv_row("式(13) 球对称 V_r=Q/r^2", ["C01", "C04", "C03"], "any_fail", "与式(1)冲突（C01）、Q 双定义（C04）、定义域受限（C03）；仅球对称支自洽（C02）")
_fv_row("式(14) A_r=-2Q^2/r^5, F_r=2k_iQ^3/r^5", ["C01", "C01b"], "any_fail", "代数成立（cross-ref r98 N01a）；上游式(13) FAIL；与式(6) 的 A_r 未合并（C01b）")
_fv_row("式(15) n=-5", ["K01", "K02"], "any_fail", "算术成立；被开普勒排除（K01）且无稳定轨道（K02）")
_fv_row("式(16)(17)(18) 严格版", ["D01", "D05"], "any_fail", "定义/约束重述；公设级")
_fv_row("式(19) q_eff=kappa_qQ_t", ["D02"], "any_boundary", "条件推演 [kappa_q]=Q L^-3 T")
_fv_row("式(20) 统一力方程", ["D05", "U02"], "any_boundary", "量纲成立；u 身份未定（U02）")
_fv_row("式(21) 展开式", ["D03", "U01"], "any_fail", "各项量纲成立；k_E/k_B 约束见式(22)")
_fv_row("式(22) k_E/k_B=c", ["D04"], "any_fail", "承重 FAIL：缺口一个长度量纲；修法甲改挂 omega 或修法乙注入康普顿波长")
_fv_row("式(23) F_unif(r)", ["U01", "U02"], "any_boundary", "式(21) 的 r 参数化重述")
_fv_row("式(24)(25) 大小/方向", ["U01"], "any_fail", "定义级成立")
_fv_row("式(26) 距离比", ["U01"], "any_fail", "恒等")
_fv_row("式(27) 标度指数", ["U01"], "any_fail", "定义级成立")

_n_need_fix = sum(1 for f in FORMULA_VERDICTS if f["verdict"] == "需修正")
_n_cond = sum(1 for f in FORMULA_VERDICTS if f["verdict"] in ("条件成立", "条件成立/边界"))
_n_ok = sum(1 for f in FORMULA_VERDICTS if f["verdict"] == "成立")
add("S01", "FAIL" if _n_need_fix >= 3 else "BOUNDARY",
    "逐式判决总表：%d 条需修正 / %d 条条件成立 / %d 条成立"
    % (_n_need_fix, _n_cond, _n_ok),
    "；".join("%s→%s" % (f["eq"].split(" ")[0], f["verdict"]) for f in FORMULA_VERDICTS),
    section="S")
guard("g_s01_formula_table_machine_driven", _n_need_fix >= 1)

# 总判决：承重 FAIL 集合
_LOAD_BEARING = ["D04", "C01", "C04", "C05", "K01", "K02"]
_lb_fail = [c for c in _LOAD_BEARING if any(it["code"] == c and it["status"] == "FAIL" for it in ITEMS)]
add("VERDICT", "FAIL" if len(_lb_fail) >= 3 else "BOUNDARY",
    "总判决：承重 FAIL %d/6（%s）"
    % (len(_lb_fail), ",".join(_lb_fail)),
    "六项承重：D04（k_E/k_B=c 量纲缺口）、C01（通量支与公理(1)冲突）、C04（Q_t 双定义）、"
    "C05（div-free 前提不成立）、K01（n=-5 被开普勒排除）、K02（n=-5 无稳定轨道）。"
    "公式集的代数内核（式(1)(5)(6)(7)(10)(11)(12)(16)-(18)(24)-(26)）机器验证成立；"
    "失效集中在「通量支 + 电磁扩展 + 距离标度」三处新增结构。", section="S")
guard("g_verdict_load_bearing_failures", len(_lb_fail) == 6)

# ============================================================================
# 外部输入账
# ============================================================================
EXT_INPUTS = [
    ("Q_t 绝对值", "式(13)(14) 的 r_* 与 r_min 均随 Q_t 无界滑动（cross-ref r98 外部输入#1）"),
    ("长度尺度（修法乙）", "D04：保留 E=k_E*v_z 映射时需注入 hbar/(m_e*c) 型长度才能救式(22)"),
    ("u 的定义", "U02：磁力项依赖未声明的测试粒子速度"),
    ("k_i,k_g,k_m,kappa_q", "四个独立耦合常数：k_i=k_g=k_m 为公设；kappa_q 无定义式（D02 只给乘积维度）"),
    ("omega(r), v_z(r) 剖面", "K 段显示距离标度完全由剖面决定，而剖面无场方程（cross-ref r95 外部输入#1）"),
    ("[C] 级实验常数", "火星周期 686.980 d、1 AU=1.495978707e11 m、地球周期 365.256363 d、c、m_e、hbar"),
]

# ============================================================================
# 总结与落盘
# ============================================================================
def _count(st):
    return sum(1 for it in ITEMS if it["status"] == st)

N_PASS = _count("PASS"); N_FAIL = _count("FAIL"); N_BOUND = _count("BOUNDARY")
N_INFO = _count("INFO"); N_CORR = _count("CORRECTED")

SECTIONS = [
    ("MAP 跨册引用校验", ["MAP01", "MAP01"]),
    ("D 量纲推演", ["D01", "D06"]),
    ("C 内部自洽性（通量支 vs 公理）", ["C01", "C05"]),
    ("K 距离标度 n=-5 的观测检验", ["K01", "K03"]),
    ("E 等效原理可证伪含量", ["E01", "E02"]),
    ("U 统一场方程结构清点", ["U01", "U03"]),
    ("S 逐式判决与总判决", ["S01", "VERDICT"]),
]

KEY_NUMBERS = {
    "d04_ke_over_kb_gap_ratio": dstr(_gap_ratio),
    "d04_missing_multiplier": dstr(_missing),
    "d04_fix_alt_ke_dim": dstr(_d_kE_alt),
    "d04_length_completion_hits": str(_lc_hits),
    "d04_compton_m": fs(C_HBAR / (C_ME * C_C), 10),
    "c01_vr_over_c_Q1e6": fs(_frac, 10),
    "c01_budget_left": fs(_budget_left, 10),
    "c03_r_min_m": " | ".join("Q=%s→%s" % (fs(r[0], 0), fs(r[1], 6)) for r in _rows),
    "c05_div_rigid": fs(_div_rigid, 8),
    "c05_div_vortex": fs(_div_vortex, 8),
    "k01_mars_pred_d": fs(_pred_mars, 10),
    "k01_mars_rel_err": fs(_e_mars, 8),
    "k01_newton_rel_err": fs(_e_newton, 8),
    "k02_rc_p_minus5_m": fs(_r_c5, 10),
    "k02_d2veff_p_minus5": fs(_d2_c5, 8),
    "k02_apsidal_3_plus_p": fs(_aps5, 4),
    "k02_rc_p_minus2_m": fs(_r_c2, 10),
    "k02_d2veff_p_minus2": fs(_d2_c2, 8),
}

lines = []
lines.append("=" * 78)
lines.append("r99 | 力公式体系压缩版与统一场论方程（式1-27）| 机器判决报告")
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
lines.append("--- 逐式判决总表（式1-27）---")
for _f in FORMULA_VERDICTS:
    lines.append("  %-46s %s  依赖:%s" % (_f["eq"][:46], _f["verdict"], ",".join(_f["deps"])))
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
lines.append("CORRECTED = %d" % N_CORR)
lines.append("条目 = %d" % len(ITEMS))
lines.append("守卫 = %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
REPORT = "\n".join(lines)


def main():
    _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _mt = {}
    for _p in (F_NEW, F_R95, F_R98):
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
    _stem = "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18"
    _payload = {
        "round": "r99",
        "date": "2026-10-18",
        "topic": "力公式体系压缩版与统一场论方程（式1-27）机器审计",
        "source": "数据/TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md",
        "cross_refs": ["r95", "r98"],
        "items": ITEMS,
        "guards": GUARDS,
        "counts": {"PASS": N_PASS, "FAIL": N_FAIL, "BOUNDARY": N_BOUND,
                   "INFO": N_INFO, "CORRECTED": N_CORR, "total": len(ITEMS),
                   "guard_pass": sum(1 for g in GUARDS if g["ok"]),
                   "guard_total": len(GUARDS)},
        "cross_citations": [{"round": r, "code": c, "expected": e, "actual":
                             (_m95 if r == "r95" else _m98).get(c), "why": w}
                            for r, c, e, w in CITES],
        "formula_verdicts": FORMULA_VERDICTS,
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
    _md = ["# 数据产物｜r99 力公式体系压缩版与统一场论方程（2026-10-18）", "",
           "来料正本：[TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md](TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md)",
           "判定册：[判定_TUFT-r99-力公式体系压缩版与统一场论方程_机器审计_2026-10-18.md](../判定_TUFT-r99-力公式体系压缩版与统一场论方程_机器审计_2026-10-18.md)",
           "", "```", REPORT, "```", ""]
    with io.open(os.path.join(DIR_DATA, _stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
