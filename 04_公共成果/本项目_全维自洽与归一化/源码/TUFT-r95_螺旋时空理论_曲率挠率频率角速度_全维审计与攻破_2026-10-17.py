# -*- coding: utf-8 -*-
r'''
================================================================================
r95 | 螺旋时空理论全维分析（曲率/挠率/频率/角速度）— 求导机器验证 + 实验数据检验 + 完成度攻破
受理日 2026-10-17 | 纯标准库 | Decimal 60 位 | Fraction 四元组量纲 (M,L,T,Q)
================================================================================

来料：《螺旋时空理论全维分析：曲率、挠率、频率、角速度，求导推导与验证校验》
      （正本留档 数据/TUFT-螺旋时空理论_来料全文_2026-10-17.md）

【本册四段任务（用户指定 + 本册自设）】
  1) 求导机器验证：三分量加速度公式、物质导数展开、链式法则 —— 来料自评"代数正确"，
     本册用 60 位解析对拍 + 直角坐标二阶差分投影双路径判定（来料后续项 1：r 不固定展开）。
  2) k_B / k_E / k_m 全套量纲推演 —— 来料后续项 2，本册机器化。
  3) 静态引力还原通道：在公理 (1) 约束下能否给出牛顿 1/r^2 与球对称引力（本册自设）。
  4) 实验数据定量检验：开普勒（地球/火星真实数据）、玻尔速度与 alpha、
     交变磁场 -> 加速度场预言 vs 重力仪实测灵敏度、水星进动（本册自设）。

【红线】
  - 数学自洽 != 物理证实；
  - 求导正确 != 物理正确；
  - 本册是审计与可算判决册，不产生新物理；不修改来料任何字节。
================================================================================
'''
import io
import os
import sys
import json
import math
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

getcontext().prec = 60

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))          # .../本项目_全维自洽与归一化/源码
BASE = os.path.dirname(HERE)                                # .../本项目_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(BASE))               # .../openuft（仓库根）
DIR_DATA = os.path.join(BASE, "数据")

# ============================================================================
# 0. 外部输入常量（全部标 [C] 级外部输入；CODATA 2018 / IAU 2015 / SI 定义）
# ============================================================================
C_C = Decimal("299792458")                 # 光速，SI 定义值（精确）[C]
C_ALPHA = Decimal("7.2973525693E-3")       # 精细结构常数 CODATA 2018 [C]
C_A0 = Decimal("5.29177210903E-11")        # 玻尔半径 CODATA 2018 [C]
C_GN = Decimal("6.67430E-11")              # 牛顿引力常数 CODATA 2018 [C]
C_ME = Decimal("9.1093837015E-31")         # 电子质量 CODATA 2018 [C]
C_HBAR = Decimal("1.054571817E-34")        # 约化普朗克常数 CODATA 2018 [C]
C_QE = Decimal("1.602176634E-19")          # 元电荷 SI 定义值（精确）[C]
C_GN_STD = Decimal("9.80665")              # 标准重力加速度（定义值）[C]
C_GMSUN = Decimal("1.32712440018E20")      # 太阳 GM，IAU 2015 名义值 [C]
C_LAMC = Decimal("2.42631023867E-12")      # 电子康普顿波长 CODATA 2018 [C]

# 行星轨道（IAU / NASA 事实值）[C]
ORB_EARTH = ("地球", Decimal("1.495978707E11"), Decimal("365.256363"))
ORB_MARS = ("火星", Decimal("1.523679") * Decimal("1.495978707E11"), Decimal("686.980"))
# 水星近日点进动：GR 后牛顿残差 42.98 角秒/世纪（观测与 GR 一致）[C]
C_MERC_ADV = Decimal("42.98")

# 实验装置上限 [C]（均标 needs_official_confirmation）
LAB_B_STEADY = Decimal("45.22")       # NHMFL 稳态混合磁体 45.22 T [C][需核对]
LAB_B_PULSE = Decimal("100.75")       # LANL 非破坏脉冲磁体 100.75 T [C][需核对]
LAB_F_MAX = Decimal("1.0E6")          # 1 MHz 交变磁场驱动上限（保守估计）[C]
GRAV_SENS_SC = Decimal("1.0E-11")     # 超导重力仪 ~1 nGal = 1e-11 m/s^2 [C][需核对]
GRAV_SENS_ATOM = Decimal("1.0E-9")    # 原子干涉重力仪 ~1e-9 m/s^2 [C][需核对]

# ============================================================================
# 1. 量纲四元组 (M, L, T, Q)：用 Fraction 分量，运算为「相加/取负」
# ============================================================================
def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))

def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dmul(a, b):
    """量纲相乘 = 指数相加（本库历史上三次误写为逐分量相乘）"""
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)

def dstr(a):
    out = []
    for sym, v in zip(("M", "L", "T", "Q"), a):
        v = Fraction(v)
        if v == 0:
            continue
        if v == 1:
            out.append(sym)
        else:
            out.append("%s^%s" % (sym, str(v).replace("/", "/")))
    if not out:
        return "1"
    return " ".join(out)

def deq(a, b):
    return tuple(a) == tuple(b)

# 基本量纲
DIM_LEN = D(l=1)
DIM_TIME = D(t=1)
DIM_MASS = D(m=1)
DIM_CHG = D(q=1)
DIM_VEL = D(l=1, t=-1)
DIM_ACC = D(l=1, t=-2)                       # 加速度 LT^-2
DIM_OMEGA = D(t=-1)                          # 角速度 T^-1
DIM_OMEGADOT = D(t=-2)                       # 角加速度 T^-2
DIM_BFIELD = D(m=1, t=-1, q=-1)              # 磁感应强度 [T] = M T^-1 Q^-1
DIM_BDOT = D(m=1, t=-2, q=-1)                # dB/dt
DIM_CURLG = D(t=-2)                          # rot(G) 加速度/长度 = T^-2
DIM_CHARGE = D(q=1)                          # 电荷 = Q
DIM_FLUXV = D(l=3, t=-1)                     # 速度场通量 L^3 T^-1

# ============================================================================
# 2. 条目登记器
# ============================================================================
ITEMS = []
GUARDS = []

def add(code, status, title, detail="", key=None):
    ITEMS.append({
        "code": code,
        "status": status,
        "title": title,
        "detail": detail,
        "key": key,
    })
    return None

def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)

def fv(x, n=25):
    """Decimal 定点输出：不用 quantize（高位数会抛 InvalidOperation），用 format E 记法"""
    try:
        s = format(Decimal(x), ".%dE" % n)
    except Exception:
        s = str(x)
    return s

def fs(x, n=25):
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    a = Decimal(a)
    b = Decimal(b)
    if b == 0:
        return None
    return abs(a - b) / abs(b)

# ============================================================================
# A 段｜求导链机器验证（来料后续项 1：r 不固定展开）
# ============================================================================
# 取 R0=1 m, omega(t)=w0+k t（70 位算，w0=1e8, k=1e14），保证 r*omega < c
R0_M = Decimal("1.0")
W0 = Decimal("1.0E8")
KDOT = Decimal("1.0E14")

with localcontext() as _lc:
    _lc.prec = 70
    V_TH = (R0_M * W0)                                   # v_theta = r*omega
    V_Z0 = (C_C * C_C - (R0_M * W0) ** 2).sqrt()         # 由公理(1) 反解 v_z
    AZ_EXACT = -(R0_M ** 2 * W0 / V_Z0) * KDOT           # 式(2) 精确值
    AR_EXACT = -(R0_M * W0 ** 2)
    AT_EXACT = R0_M * KDOT

# --- A01 公理 (1) 三项同量纲 -----------------------------------------------
# 注意：同量纲项「相加」时量纲不变，不能用逐分量相加（dadd）
_d1 = dpow(dmul(DIM_LEN, DIM_OMEGA), 2)     # (r*omega)^2
_d2 = dpow(DIM_VEL, 2)                      # v_z^2
_d3 = dpow(DIM_VEL, 2)                      # c^2
_ok = deq(_d1, _d2) and deq(_d2, _d3)
add("A01",
    "PASS" if _ok else "FAIL",
    "公理(1) (r*omega)^2+v_z^2=c^2 三项同量纲（齐次）",
    "[(r*omega)^2]=%s ；[v_z^2]=%s ；[c^2]=%s ；三者相等=%s"
    % (dstr(_d1), dstr(_d2), dstr(_d3), _ok))
guard("g_a01_axiom1_homogeneous", _ok)

# --- A02 式(2) A_z 量纲 = 加速度 -------------------------------------------
_d = ddiv(dmul(dpow(DIM_LEN, 2), DIM_OMEGA), DIM_VEL)   # r^2*omega/v_z : L
_d = dmul(_d, DIM_OMEGADOT)                             # * d(omega)/dt : L T^-2
_ok = deq(_d, DIM_ACC)
add("A02",
    "PASS" if _ok else "FAIL",
    "式(2) A_z=-(r^2*omega/v_z)*d(omega)/dt 量纲为加速度",
    "[A_z]=%s ；[加速度]=%s ；相等=%s" % (dstr(_d), dstr(DIM_ACC), _ok))
guard("g_a02_az_is_acceleration", _ok)

# --- A03 三分量量纲 + r 不固定完整展开（来料后续项1） -----------------------
_dr = dpow(DIM_LEN, 2)                                    # r^2
_dr = dmul(_dr, DIM_OMEGA)                                # r^2*omega
_dr = ddiv(_dr, DIM_VEL)                                  # /v_z
_dr = dmul(_dr, DIM_OMEGADOT)                             # *d(omega)/dt
_ok1 = deq(_dr, DIM_ACC)
_dr2 = dmul(DIM_LEN, DIM_OMEGA)                           # r*omega
_dr2 = ddiv(dmul(_dr2, DIM_OMEGA), DIM_VEL)               # *omega/v_z
_dr2 = dmul(_dr2, DIM_VEL)                                # * Dr/Dt (速度)
_ok2 = deq(_dr2, DIM_ACC)
_ok = _ok1 and _ok2
add("A03", "PASS" if _ok else "FAIL",
    "r 不固定时 A_z 完整两项量纲均为加速度（来料后续项1）",
    "完整式 A_z=-(r^2*omega/v_z)*d(omega)/dt-(r*omega^2/v_z)*(Dr/Dt)；"
    "[项1]=%s [项2]=%s 均为 %s" % (dstr(_dr), dstr(_dr2), dstr(DIM_ACC)))
guard("g_a03_az_full_two_terms_are_accel", _ok)

# r 不固定时相对误差（逼近式成立条件）：|omega*(Dr/Dt)| / |r*d(omega)/dt|
with localcontext() as _lc:
    _lc.prec = 70
    VR_TEST = Decimal("1.0E5")            # 径向漂移 1e5 m/s（外加，非公理导出）
    _t1 = abs(R0_M ** 2 * W0 / V_Z0 * KDOT)
    _t2 = abs(R0_M * W0 ** 2 / V_Z0 * VR_TEST)
    AZ_FULL = -(R0_M ** 2 * W0 / V_Z0 * KDOT + R0_M * W0 ** 2 / V_Z0 * VR_TEST)
    AZ_APRX = -(R0_M ** 2 * W0 / V_Z0 * KDOT)
    _ratio = _t2 / _t1
add("A03b", "PASS",
    "r 不固定时逼近式(论文式1) 的适用条件可量化",
    "取径向漂移 v_r=%s m/s：修正项/主项=%s ；A_z 完整值=%s ；近似值=%s"
    % (fs(VR_TEST, 6), fs(_ratio, 10), fv(AZ_FULL), fv(AZ_APRX)))
guard("g_a03b_ratio_finite", _ratio > 0)

# --- A04 链式法则 60 位解析对拍（式(2) 是公理(1) 的微分推论） ---------------
def _vz_of(w, r):
    return (C_C * C_C - (r * w) ** 2).sqrt()

with localcontext() as _lc:
    _lc.prec = 70
    _h = Decimal("1.0E-20")
    _w1 = W0 + KDOT * _h
    _w2 = W0 - KDOT * _h
    _dvz = (_vz_of(_w1, R0_M) - _vz_of(_w2, R0_M)) / (2 * _h)   # dv_z/dt 数值
    _az = -(R0_M ** 2 * W0 / V_Z0) * KDOT                        # 式(2)
    _res = abs(_dvz - _az) / abs(_az)
_ok = _res < Decimal("1E-15")
add("A04", "PASS" if _ok else "FAIL",
    "式(2) ≡ 公理(1) 的链式法则推论（60 位解析对拍）",
    "dv_z/dt(数值)=%s ；式(2)=%s ；相对残差=%s（差分截断极限，非 0 故排除恒等复读）"
    % (fv(_dvz), fv(_az), fs(_res, 6)))
guard("g_a04_chain_rule_identity", _ok)

# --- A05 直角坐标二阶差分 → 柱基投影（float 数值对拍，含步长收敛） ---------
# 轨迹：x=R0 cos(theta(t)), y=R0 sin(theta(t)), theta=W0*t+KDOT*t^2/2, t0=0
_fR = float(R0_M); _fw0 = float(W0); _fk = float(KDOT)
def _x(t):
    return _fR * math.cos(_fw0 * t + 0.5 * _fk * t * t)
def _y(t):
    return _fR * math.sin(_fw0 * t + 0.5 * _fk * t * t)
def _d2(f, t, h):
    return (f(t + h) - 2.0 * f(t) + f(t - h)) / (h * h)

_h1 = 1e-11
_h2 = _h1 / 2.0
_ax1 = _d2(_x, 0.0, _h1); _ay1 = _d2(_y, 0.0, _h1)
_ax2 = _d2(_x, 0.0, _h2); _ay2 = _d2(_y, 0.0, _h2)
# t0=0 处 theta=0 ⇒ e_r=(1,0), e_theta=(0,1)，投影即分量本身
_ar1, _at1 = _ax1, _ay1
_ar2, _at2 = _ax2, _ay2
_e1r = abs(_ar1 - float(AR_EXACT)) / abs(float(AR_EXACT))
_e1t = abs(_at1 - float(AT_EXACT)) / abs(float(AT_EXACT))
_e2r = abs(_ar2 - float(AR_EXACT)) / abs(float(AR_EXACT))
_e2t = abs(_at2 - float(AT_EXACT)) / abs(float(AT_EXACT))
_conv_r = _e1r / _e2r if _e2r > 0 else None
_ok = (_e1r < 1e-4) and (_e1t < 1e-4) and (_conv_r is not None and 3.0 < _conv_r < 5.0)
add("A05", "PASS" if _ok else "FAIL",
    "直角坐标二阶差分投影 = 论文的 (A_r, A_theta)（步长收敛 h^2）",
    "A_r: 差分 %s vs 公式 %s，相对 %s ；A_theta: 差分 %s vs 公式 %s，相对 %s ；"
    "h→h/2 误差收敛比=%s（理论 4）"
    % (fs(Decimal(repr(_ar1)), 10), fs(AR_EXACT, 10), fs(Decimal(repr(_e1r)), 4),
       fs(Decimal(repr(_at1)), 10), fs(AT_EXACT, 10), fs(Decimal(repr(_e1t)), 4),
       fs(Decimal(repr(_conv_r)), 4)))
guard("g_a05_finite_difference_matches_formula", _ok)

# --- A06 正面构造：螺旋流线的 Frenet 曲率/挠率与 omega ----------------------
# 曲线：x=R0 cos(omega t), y=R0 sin(omega t), z=v_z t；ds/dt=|V|=c
with localcontext() as _lc:
    _lc.prec = 70
    KAPPA = (R0_M * W0 ** 2) / (C_C ** 2)
    TAU = (W0 * V_Z0) / (C_C ** 2)
    _lhs = KAPPA ** 2 + TAU ** 2
    _rhs = (W0 / C_C) ** 2
    _res = abs(_lhs - _rhs) / _rhs
_ok = _res < Decimal("1E-40")
add("A06", "PASS" if _ok else "FAIL",
    "正面构造：螺旋流线 Frenet 不变量满足 kappa^2+tau^2=(omega/c)^2",
    "kappa=%s m^-1 ；tau=%s m^-1 ；kappa^2+tau^2=%s ；(omega/c)^2=%s ；相对残差=%s "
    "（与库内 S01/S02 三重奏 v=c 分支汇流）"
    % (fv(KAPPA), fv(TAU), fs(_lhs, 25), fs(_rhs, 25), fs(_res, 6)))
guard("g_a06_frenet_triad_identity", _ok)
_res_a06 = _res

# --- A07 kappa/tau = v_theta/v_z（把 H1 假说翻译为几何语言） ---------------
with localcontext() as _lc:
    _lc.prec = 70
    _kt = KAPPA / TAU
    _vv = (R0_M * W0) / V_Z0
    _res = abs(_kt - _vv) / _vv
_ok = _res < Decimal("1E-40")
add("A07", "PASS" if _ok else "FAIL",
    "kappa/tau ≡ v_theta/v_z（H1 假说 alpha=v_theta/v_z 的几何翻译）",
    "kappa/tau=%s ；v_theta/v_z=%s ；相对残差=%s"
    % (fv(_kt), fv(_vv), fs(_res, 6)))
guard("g_a07_kappa_over_tau_is_speed_ratio", _ok)

# --- A08 符号台账：D/Dt(=d_t+nabla_V) 与 nabla_V 的口径混用 ----------------
add("A08", "BOUNDARY",
    "论文把 D/Dt 定义为 nabla_V，但 A_theta/A_z 含 d_t 项而 A_r 不含 ⇒ 两个算子混用",
    "nabla_V 是纯空间协变导数（不含 d_t）；A_r=-r*omega^2 来自其 Christoffel 项，"
    "A_theta=r*d(omega)/dt 与 A_z=d(v_z)/dt 来自 d_t 项。二者并置于 A=nabla_V*V 时，"
    "静态场（d_t=0）必然 A_theta=A_z=0（见 G01）。属符号口径问题，不改变各分量公式本身。")
guard("g_a08_operator_mixing_flagged", True)

# ============================================================================
# G 段｜静态引力还原通道（本册自设承重项）
# ============================================================================
# --- G01 静态场：A_theta=A_z=0，唯一非零分量是向轴的 A_r --------------------
add("G01", "PASS",
    "静态（d_t=0）且 v_r=0、场与 theta 无关时，A_theta=A_z=0，仅 A_r=-r*omega^2 非零",
    "由 D/Dt=d_t+nabla_V：A_theta=d_t(v_theta)=0、A_z=d_t(v_z)+v_z*d_z(v_z)=0（v_z 只依赖 r）；"
    "A_r=-v_theta^2/r=-r*omega^2 保留。静态引力若要存在，只能落在 A_r 或 v_z 的空间梯度上（见 G02）。")
guard("g_g01_static_leaves_only_A_r", True)

# --- G02 A_z 的静态形式 = 牛顿能量守恒（恒等重述） --------------------------
# A_z = v_z * d_z(v_z) = d_z(v_z^2/2)；要求 A_z = -GM/z^2 ⇒ v_z^2 = 2GM/z + C
add("G02", "INFO",
    "静态轴向引力 A_z=d_z(v_z^2/2)=-GM/z^2 ⇒ v_z^2=2GM/z+C —— 牛顿自由落体能量守恒的恒等重述",
    "该式是标准结果 d(v^2/2)/dz=-d(Phi)/dz（Phi=-GM/z）的等价写法；"
    "论文没有给出 GM 的来源，也没有给出 C 的取值机制 ⇒ 牛顿项是被**输入**的，非导出。")
guard("g_g02_static_Az_is_newton_identity", True)

# --- G03/G04 承重：{公理(1), 牛顿势, 开普勒} 三选二互斥 + 双行星实测否证 ----
_A_E = ORB_EARTH[1]           # 1 AU
_A_M = Decimal("5.7909E10")   # 水星半长轴 [C]
with localcontext() as _lc:
    _lc.prec = 70
    # 开普勒圆轨道速度（自洽，不引入额外外部数据）
    _vE = (C_GMSUN / _A_E).sqrt()
    _vM = (C_GMSUN / _A_M).sqrt()
    # 由 A_z=-GM/z^2 积分：v_z^2 = 2GM/z + C；公理(1) 给 v_theta^2 = c^2 - 2GM/z - C
    # 口径甲：用地球轨道标定 C（令该处 v_theta = 开普勒地球速度）
    _C_earth = C_C ** 2 - 2 * C_GMSUN / _A_E - _vE ** 2
    _vt2_at_merc = C_C ** 2 - 2 * C_GMSUN / _A_M - _C_earth
    # 口径乙：用水星轨道标定 C
    _C_merc = C_C ** 2 - 2 * C_GMSUN / _A_M - _vM ** 2
    _vt2_at_earth = C_C ** 2 - 2 * C_GMSUN / _A_E - _C_merc
    _vt_at_earth = _vt2_at_earth.sqrt() if _vt2_at_earth > 0 else None
    # 三选二互斥的解析判据：C = c^2 - 3GM/z 须为常数，而它随 z 变化
    _C_at_earth_need = C_C ** 2 - 3 * C_GMSUN / _A_E
    _C_at_merc_need = C_C ** 2 - 3 * C_GMSUN / _A_M
    _dC = abs(_C_at_earth_need - _C_at_merc_need)

_ok = _vt2_at_merc < 0
add("G03", "FAIL" if _ok else "PASS",
    "承重：{公理(1), 牛顿势 A_z=-GM/z^2, 开普勒 v_theta=sqrt(GM/z)} 三者互斥（三选二）",
    "联立得 C=c^2-3GM/z，要求 C 为常数却随 z 变：水星处需求 C=%s ；地球处需求 C=%s ；"
    "两处之差 %s（非零即互斥）"
    % (fs(_C_at_merc_need, 25), fs(_C_at_earth_need, 25), fs(_dC, 6)))
guard("g_g03_triple_exclusion_nonzero_gap", _dC > 0)

_ok = _vt2_at_merc < 0
add("G04", "FAIL" if _ok else "PASS",
    "实测否证甲：以地球轨道标定积分常数 C 后，水星处 v_theta^2<0（公理(1) 崩为虚数）",
    "C=%s ；水星处 v_theta^2=%s m^2/s^2（负 ⇒ v_theta 为虚，公理(1) 不可满足）"
    % (fs(_C_earth, 25), fs(_vt2_at_merc, 10)))
guard("g_g04_mercury_becomes_imaginary", _ok)

if _vt_at_earth is not None:
    _ratio = _vt_at_earth / _vE
    _bad = abs(_ratio - Decimal(1)) > Decimal("0.1")
    add("G04b", "FAIL" if _bad else "PASS",
        "实测否证乙：以水星轨道标定 C 后，地球处 v_theta 与真实公转速度不符",
        "地球处 v_theta=%s m/s ；真实公转速度 %s m/s ；比值=%s（理论要求 1）"
        % (fs(_vt_at_earth, 10), fs(_vE, 10), fs(_ratio, 6)))
    guard("g_g04b_earth_speed_mismatch", _bad)

# --- G05 1/r 力场 vs 1/r^2：地球/火星真实轨道数据检验 ----------------------
_a_mars = ORB_MARS[1]
_t_earth = ORB_EARTH[2]
_t_mars = ORB_MARS[2]
with localcontext() as _lc:
    _lc.prec = 70
    _ratio_a = _a_mars / _A_E
    _pred_kepler = _t_earth * _ratio_a * _ratio_a.sqrt()              # 1/r^2 ⇒ T∝a^1.5
    _pred_1over_r = _t_earth * _ratio_a                               # 1/r ⇒ T∝a
    _e_k = abs(_pred_kepler - _t_mars) / _t_mars
    _e_1 = abs(_pred_1over_r - _t_mars) / _t_mars
_ok = _e_k < Decimal("1E-3") and _e_1 > Decimal("1E-2")
add("G05", "PASS" if _ok else "FAIL",
    "开普勒检验：1/r^2 与观测符合 6e-5；若取 v_theta 常数（公理(1) 的自然读法）得 1/r，与观测差 19%",
    "火星周期：观测 %s d ；1/r^2 预测 %s d（相对 %s）；1/r 预测 %s d（相对 %s）"
    % (fs(_t_mars, 6), fs(_pred_kepler, 6), fs(_e_k, 3), fs(_pred_1over_r, 6), fs(_e_1, 4)))
guard("g_g05_kepler_discriminates_1_over_r", _ok)

# --- G06 适域下界：r < r_s ⇒ 公理(1) 失效 ----------------------------------
with localcontext() as _lc:
    _lc.prec = 70
    _rs_sun = 2 * C_GMSUN / (C_C ** 2)
    _rs_earth = 2 * Decimal("3.986004418E14") / (C_C ** 2)
add("G06", "BOUNDARY",
    "适域下界：v_theta^2=c^2-2GM/z-C >= 0 要求 z >= 2GM/(c^2-C)；C=0 时即 Schwarzschild 半径",
    "太阳 r_s=%s m（2953 m）；地球 r_s=%s m（8.87 mm）；且不取 C=c^2（该取值使 v_theta^2=-2GM/z 全域为负）。"
    % (fs(_rs_sun, 10), fs(_rs_earth, 10)))
guard("g_g06_domain_lower_bound_positive", _rs_sun > 0 and _rs_earth > 0)

# --- G07 几何：柱对称向轴 vs 球对称向心 ------------------------------------
add("G07", "FAIL",
    "几何不匹配：柱坐标螺旋场的 A_r 指向柱轴，不是指向引力中心的球对称向心力",
    "V=v_theta*e_theta+v_z*e_z 的 A_r=-v_theta^2/r*e_r 垂直于柱轴；要表示太阳系球对称吸引，"
    "须在每点指向力心，单一螺旋场做不到（除非叠加连续族不同取向的螺旋场，论文未给）。"
    "⇒ 本理论在当前形式下只能在单一赤道平面内描述运动，不能给出三维球对称引力。")
guard("g_g07_axial_not_spherical", True)

# ============================================================================
# K 段｜k_B 全套量纲推演（来料后续项 2）
# ============================================================================
# 口径甲：同源映射 B = k_B * omega ⇒ [k_B] = [B]/[omega]
_kb1 = ddiv(DIM_BFIELD, DIM_OMEGA)
# 口径乙：耦合方程 rot(G) = -(1/(k_B c^2)) dB/dt ⇒ [k_B] = [dB/dt]/(c^2 * [rot G])
_kb2 = ddiv(DIM_BDOT, dmul(dpow(DIM_VEL, 2), DIM_CURLG))
_gap = dsub(_kb1, _kb2)
_gap_is_c2 = deq(_gap, dpow(DIM_VEL, 2))
add("K01", "PASS", "同源映射口径：B=k_B*omega ⇒ [k_B]=%s" % dstr(_kb1), "")
add("K02", "PASS", "耦合方程口径：rot(G)=-(1/(k_B c^2))*dB/dt ⇒ [k_B]=%s" % dstr(_kb2), "")
add("K03", "FAIL",
    "承重：同一常数 k_B 在两式中量纲相差 c^2，不可能是同一常数",
    "[k_B]_甲=%s ；[k_B]_乙=%s ；甲/乙=%s ；该比值恰为 c^2 的量纲=%s（即 甲 = 乙*c^2）"
    % (dstr(_kb1), dstr(_kb2), dstr(_gap), _gap_is_c2))
guard("g_k03_kb_gap_is_c_squared", _gap_is_c2 and not deq(_kb1, _kb2))

# 穷举：用 {c, hbar, e, m_e} 的 ±3 次幂能否补齐 c^2 缺口
_TARGET = dpow(DIM_VEL, 2)
_basis = {
    "c": (DIM_VEL, "c"),
    "hbar": (dmul(DIM_MASS, dmul(dpow(DIM_LEN, 2), dpow(DIM_TIME, -1))), "hbar"),
    "e": (DIM_CHG, "e"),
    "me": (DIM_MASS, "me"),
}
_hits = []
_ks = list(_basis.keys())
for a in range(-3, 4):
    for b in range(-3, 4):
        for cc in range(-3, 4):
            for d in range(-3, 4):
                _d = dpow(_basis[_ks[0]][0], a)
                _d = dadd(_d, dpow(_basis[_ks[1]][0], b))
                _d = dadd(_d, dpow(_basis[_ks[2]][0], cc))
                _d = dadd(_d, dpow(_basis[_ks[3]][0], d))
                if deq(_d, _TARGET):
                    _hits.append((a, b, cc, d))
_triv = sum(1 for h in _hits if h[1] == 0 and h[2] == 0 and h[3] == 0)
_nontriv = len(_hits) - _triv
add("K04",
    "FAIL",
    "缺口 c^2 的补齐因子穷举（{c,hbar,e,m_e}^[±3]）：命中 %d/2401，其中平凡解 %d、非平凡 %d"
    % (len(_hits), _triv, _nontriv),
    "唯一命中者恰是 c^2 本身（即公式里已显式存在的那个 1/c^2）⇒ 唯一的量纲修法 = 删掉耦合方程的 1/c^2，"
    "而这等价于承认同源映射的 k_B 与耦合方程的 k_B 是两个不同常数（需 +1 外部输入并显式改名）。"
    "命中组合=%s" % str(_hits))
guard("g_k04_no_nontrivial_completion", _nontriv == 0)

# ============================================================================
# E 段｜实验数据定量检验（本册自设）
# ============================================================================
_PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798")
with localcontext() as _lc:
    _lc.prec = 70
    # 内部自洽口径：由 a_0 = hbar/(m_e*c*alpha) 反解 alpha（与 a_0/m_e/hbar/c 同源）
    # 教训（库内既有）：跨常数恒等式检验必须先确认输入常数是否同一口径，
    # 否则残差被输入常数的最少有效位数主导，会把真恒等误判为「偏差」。
    _alpha_int = C_HBAR / (C_ME * C_C * C_A0)
    _alpha_gap = abs(_alpha_int - C_ALPHA) / C_ALPHA
    _v_theta_h1 = _alpha_int * C_C
    _omega_bohr = _alpha_int * C_C / C_A0
    _t_bohr = 2 * _PI / _omega_bohr
    _omega_comp = C_ME * C_C ** 2 / C_HBAR
    _alpha2_omegaC = _alpha_int ** 2 * _omega_comp
    _res_e2 = abs(_alpha2_omegaC - _omega_bohr) / _omega_bohr
_ok = _res_e2 < Decimal("1E-40")
add("E01", "INFO",
    "H1 假说 alpha=v_theta/v_z ⇒ v_theta=alpha*c = 玻尔基态速度 —— 教科书恒等重述",
    "v_theta=%s m/s ；alpha*c=%s m/s ；一致（玻尔模型 v_1=alpha*c，是本理论的输入而非导出）；"
    "内部自洽 alpha(由 a_0,m_e,hbar,c 反解)=%s 与字面 CODATA alpha=%s 之差=%s（仅登记不判）"
    % (fs(_v_theta_h1, 10), fs(_alpha_int * C_C, 10), fs(_alpha_int, 12),
       fs(C_ALPHA, 12), fs(_alpha_gap, 6)))
add("E02", "PASS" if _ok else "FAIL",
    "omega_Bohr = alpha^2 * omega_Compton（60 位恒等，正面构造）",
    "omega_B=alpha*c/a_0=%s s^-1（周期 %s s）；alpha^2*omega_C=%s s^-1；相对残差=%s"
    % (fs(_omega_bohr, 15), fs(_t_bohr, 15), fs(_alpha2_omegaC, 15), fs(_res_e2, 6)))
guard("g_e02_omega_bohr_equals_alpha2_omegaC", _ok)

# E03：三个 omega 锚点下的 kappa/tau（r=a_0）—— 标度自由的机器表现
with localcontext() as _lc:
    _lc.prec = 70
    _anchors = [("omega_B=alpha*c/a_0", _omega_bohr),
                ("omega_geo=c/a_0（公理(1)边界）", C_C / C_A0),
                ("omega_C=m_e*c^2/hbar", _omega_comp)]
    _rows = []
    for _nm, _w in _anchors:
        _vt = C_A0 * _w / C_C            # v_theta/c
        if _vt <= 1:                     # 边界 v_theta=c（v_z=0，螺旋退化为圆）仍在定义域
            _vz = (C_C ** 2 - (C_A0 * _w) ** 2).sqrt()
            _k = (C_A0 * _w ** 2) / (C_C ** 2)
            _t = (_w * _vz) / (C_C ** 2)
            _rows.append((_nm, _vt, _k, _t))
        else:
            _rows.append((_nm, _vt, None, None))
    _KAPPA_BOHR = _rows[0][2]
    _TAU_BOHR = _rows[0][3]
    _kappa_span = _rows[1][2] / _rows[0][2]
    _viol = _rows[2][1]                  # v_theta/c for omega_C
_ok = _viol > 1
add("E03", "BOUNDARY",
    "三个 omega 锚点（r=a_0）下标度不定：康普顿锚直接违反公理(1)",
    "锚点 v_theta/c / kappa / tau：%s；kappa 跨度=%s（=1/alpha^2）；康普顿锚 v_theta/c=%s > 1 ⇒ 不在定义域"
    % (" | ".join("%s: %s / %s / %s" % (r[0], fs(r[1], 6),
        fs(r[2], 6) if r[2] is not None else "N/A",
        fs(r[3], 6) if r[3] is not None else "N/A") for r in _rows),
       fs(_kappa_span, 8), fs(_viol, 8)))
guard("g_e03_compton_anchor_violates_axiom1", _ok)

# --- A09 符号台账：联络挠率 T≡0（来料） vs 螺旋流线 Frenet 挠率 tau（库内） ---
# 位置说明：必须在 E03 之后，因为要引用 E03 定义的 _TAU_BOHR。
add("A09", "INFO",
    "同名异物：来料 T^alpha_{mu nu}≡0 是联络挠率（Levi-Civita 的恒真性质，属约定非物理假设）；"
    "库内 tau 是螺旋流线的 Frenet 挠率（玻尔锚点 tau=%s m^-1，非零；数值见 E03）"
    % fs(_TAU_BOHR, 10),
    "(a) 对任意黎曼流形，Levi-Civita 联络恒满足 T(u,v)=grad_u v-grad_v u-[u,v]=0 ⇒ 选用它是记账约定，"
    "不构成物理内容，也不能作为「挠率不参与物理」的证据（记零信息量）；"
    "(b) 螺旋流线只要 v_z≠0 就有 Frenet 挠率 tau=omega*v_z/c^2≠0；v_z=0 时螺旋退化为圆、tau=0；"
    "(c) ⇒ 来料风险点 6「挠率全程为零，不要引入挠率做修正」若被读作「Frenet 挠率也不存在」，"
    "则与本册 A06 的正面构造直接冲突。正确读法：无挠仅针对联络，Frenet 挠率仍应保留。")
guard("g_a09_torsion_homonym_flagged", True)

# E04：耦合方程的实验射程（两口径）
_PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798")
with localcontext() as _lc:
    _lc.prec = 70
    _B_au = C_HBAR / (C_QE * C_A0 ** 2)          # 原子单位磁感应强度 = 2.35e5 T
    _kB_a = _B_au / _omega_bohr                   # 口径甲：用原子单位标定 k_B
    _dBdt = 2 * _PI * LAB_F_MAX * LAB_B_STEADY    # 45.22 T @ 1 MHz
    _curlG = _dBdt / (_kB_a * C_C ** 2)           # |rot G| 预言 [s^-2]
    _G_pred = _curlG * Decimal("1")               # 取特征尺度 L=1 m
    _excess = _G_pred / GRAV_SENS_ATOM
    _kB_needed = _dBdt / (GRAV_SENS_ATOM * C_C ** 2)
_ok = _excess > Decimal("1E6")
add("E04",
    "FAIL" if _ok else "PASS",
    "实验射程甲：45.22T@1MHz 交变磁场预言 1m 尺度加速度场 %s m/s^2（%s g），超实测灵敏度 %s 倍"
    % (fs(_G_pred, 8), fs(_G_pred / C_GN_STD, 6), fs(_excess, 6)),
    "k_B(原子单位口径)=%s T·s ；|dB/dt|=%s T/s ；|rot G|=%s s^-2 ；与实测灵敏度 %s m/s^2 之比=%s"
    % (fs(_kB_a, 10), fs(_dBdt, 10), fs(_curlG, 10), fs(GRAV_SENS_ATOM, 6), fs(_excess, 6)))
guard("g_e04_lab_prediction_exceeds_sensitivity", _ok)
add("E04b", "BOUNDARY",
    "实验射程乙：k_B 若自由，则任何灵敏度都能被某个 k_B 容纳",
    "要把预言压到 %s m/s^2 以下只需 k_B >= %s T·s（比原子单位口径大 %s 倍）⇒ 该通道当前不可证伪"
    % (fs(GRAV_SENS_ATOM, 6), fs(_kB_needed, 6), fs(_kB_needed / _kB_a, 6)))
guard("g_e04b_kB_free_unfalsifiable", True)

# E05：静态引力 rot(G)=0 ⇒ 耦合方程对静态引力零判别力
add("E05", "FAIL",
    "静态引力是保守场 ⇒ rot(G)≡0 ⇒ 耦合方程退化为 d(omega)/dt=0（0=0），对静态引力零判别力",
    "牛顿型 G=-GM/r^2*e_r（或任何 G=-grad(Phi)）满足 rot(G)=0；代入 rot(G)=-(1/c^2)*d(omega)/dt "
    "得 d(omega)/dt=0。⇒ 该耦合方程只在时变情形有内容，而时变情形被 E04 排除。")
guard("g_e05_static_limit_trivial", True)

# E06：水星近日点进动两难
_ok = True
add("E06",
    "BOUNDARY",
    "水星进动两难：若理论=牛顿则预言附加进动 0（观测 %s 角秒/世纪，被排除）；若 omega(r) 自由则不可证伪"
    % fs(C_MERC_ADV, 4),
    "理论未给出 omega(r) 的场方程 ⇒ 附加进动可通过调 omega(r) 取任意值"
    "⇒ 与 E04b/k_B 同型的「固定则被排除、自由则不可证伪」两难。")
guard("g_e06_mercury_dilemma_flagged", _ok)

# ============================================================================
# T 段｜拓扑电荷
# ============================================================================
add("T01", "FAIL",
    "拓扑电荷 Q 量纲为 L^3T^-1，不是电荷量纲 Q（库仑）—— 名实不符",
    "[Q]=[(1/4pi)*flux(V)]=%s ；[电荷]=%s ；相等=%s（1/4pi 无量纲）"
    % (dstr(DIM_FLUXV), dstr(DIM_CHARGE), deq(DIM_FLUXV, DIM_CHARGE)))
guard("g_t01_Q_not_charge_dimension", not deq(DIM_FLUXV, DIM_CHARGE))

# T02：v_z 常数 ⇒ 闭合面通量恒为 0（含阳性对照）
_n = 64
_tot_z = 0.0
_tot_r = 0.0
for _i in range(_n):
    _u = -1.0 + 2.0 * (_i + 0.5) / _n
    _phi = 2.0 * math.pi * (_i * 0.6180339887498949 % 1.0)
    _st = math.sqrt(max(0.0, 1.0 - _u * _u))
    _nx, _ny, _nz = _st * math.cos(_phi), _st * math.sin(_phi), _u
    _w = (4.0 * math.pi) / _n          # 单位球等权面积分（cos 加权已含于采样）
    _tot_z += _nz * _w                 # e_z·n 的通量
    _tot_r += 1.0 * _w                 # e_r·n = 1（阳性对照，应为 4pi）
_ok = abs(_tot_z) < 1e-2 and abs(_tot_r - 4 * math.pi) < 1e-2
add("T02", "FAIL" if abs(_tot_z) < 1e-2 else "PASS",
    "弱场近似 v_z≈c（常数）下拓扑电荷 Q≡0 —— 公设与结论自相抵消",
    "对闭曲面，常矢量 e_z 的通量恒为 0（机器球面积分=%s）；阳性对照 e_r·n 积分=%s（理论 4pi）"
    "⇒ 检验器非恒零。论文恰在弱场近似 v_z≈c 下使用 Q ⇒ Q 恒为零。"
    % (fs(Decimal(repr(_tot_z)), 6), fs(Decimal(repr(_tot_r)), 6)))
guard("g_t02_constant_vz_gives_zero_Q", _ok)

# T03：v_z 非常数 ⇒ Q 随体积变，无量子化
with localcontext() as _lc:
    _lc.prec = 70
    _kz = Decimal("1.0E-6")                       # 外加轴向梯度（无来源）
    _R1, _R2 = Decimal("1.0"), Decimal("2.0")
    _Q1 = C_C * _kz * _R1 ** 3 / 3
    _Q2 = C_C * _kz * _R2 ** 3 / 3
add("T03", "FAIL",
    "v_z 非常数时 Q=(1/4pi)*c*k*V 随包围体积 V 连续变化，无量纲无关的量子化",
    "取 v_z=c(1+k z)、k=%s m^-1：R=1 m 时 Q=%s ；R=2 m 时 Q=%s ；比值=%s（=体积比，非整数比）"
    % (fs(_kz, 6), fs(_Q1, 10), fs(_Q2, 10), fs(_Q2 / _Q1, 6)))
guard("g_t03_Q_scales_with_volume", True)

add("T04", "FAIL",
    "「拓扑电荷」缺少拓扑不变性证明——高斯定理只给出对曲面形变不变，不等于拓扑不变量",
    "要成为拓扑荷需 div(V)=4*pi*q*delta^3 型的奇点结构与量子化条件，论文未给奇点边界条件"
    "（论文自陈：「没有证明 Q 量子化；本质是通量荷」）。")
guard("g_t04_topological_claim_unproven", True)

# ============================================================================
# M 段｜残余质量公式
# ============================================================================
_targets = [Decimal(x) for x in ("0.01", "0.1", "0.5", "1", "2", "5", "10", "100", "1000", "1900")]
_solved = 0
for _t in _targets:
    _found = False
    for _b in range(-3, 4):
        _f = (4 * Decimal("3.14159265358979323846264338327950288419716939937510")) ** _b
        for _eta in (Decimal("0"), Decimal("0.5")):
            _a = _t / (_f * (1 - _eta))
            if 0 < _a <= 1:
                _found = True
                break
        if _found:
            break
    if _found:
        _solved += 1
_ok = _solved == len(_targets)
add("M01", "FAIL" if _ok else "PASS",
    "残余质量公式 m*/m_0=alpha*(4pi)^beta*(1-eta) 三参数可拟合任意目标值 ⇒ 零判别力",
    "10 个目标值（0.01~1900）全部命中 %d/10；(alpha,beta,eta) 三者自由，值域覆盖 (0,(4pi)^3]"
    % _solved)
guard("g_m01_three_knobs_fit_anything", _ok)

add("M02", "BOUNDARY",
    "符号 alpha 撞名：精细结构常数 与 速度比 v_theta/v_z 用同一记号",
    "同一记号承载「已知常数 1/137」与「待定几何比」两个角色；且后者依赖 (r,omega) 的绝对标度，"
    "而 (r,omega) 无来源（O-SCALE 同构）。")
guard("g_m02_alpha_symbol_clash", True)

add("M03", "FAIL",
    "残余质量比值与驱动频率 f 无关 ⇒ 相变后的任何预言都不可被 f 证伪",
    "论文自陈：越过阈值后残余质量比值是普适常数、与 f 和驱动强度无关 ⇒ 该量对实验无响应，"
    "与 E05 的静态零判别力同型。")
guard("g_m03_f_independence_unfalsifiable", True)

# ============================================================================
# 外部输入账（理论侧）
# ============================================================================
EXT_INPUTS = [
    ("omega(r,t)", "螺旋角速度场：无场方程 ⇒ 实为自由函数（自由度无界，非「一个常数」）"),
    ("r", "螺旋半径：无来源，且 r=const 是外加近似"),
    ("v_z", "轴向速度：由公理(1) 反解，但 C（积分常数）无取值机制"),
    ("C", "牛顿势积分常数：E03/G03/G04 显示单一 C 无法同时容纳水星与地球"),
    ("k_B", "同源映射常数：量纲未标定，且两式口径差 c^2"),
    ("GM", "引力源参数：理论未导出（牛顿项是被输入的）"),
    ("G=A 公设", "引力场 = 矢量场协变加速度：公设映射，非求导导出（论文自陈）"),
    ("H1", "alpha = 精细结构常数 = v_theta/v_z：物理假说（论文自陈）"),
    ("beta, eta", "残余质量公式的两个自由参数：无取值范围、无推导"),
    ("f_ref, Delta_omega", "Floquet 周期与频率重标度基准：无来源"),
    ("螺旋轴取向", "每点一个方向 ⇒ 连续族自由度（球对称引力须叠加连续族，论文未给）"),
    ("[C]级实验常数", "c, alpha, a_0, G, m_e, hbar, e, GM_sun, 行星轨道, 45.22T, 1MHz, 1e-9 m/s^2, 42.98 角秒/世纪"),
]

# ============================================================================
# 总结与落盘
# ============================================================================
def _count(st):
    return sum(1 for it in ITEMS if it["status"] == st)

N_PASS = _count("PASS")
N_FAIL = _count("FAIL")
N_BOUND = _count("BOUNDARY")
N_INFO = _count("INFO")
N_CORR = _count("CORRECTED")
N_MIS = _count("MISMATCH")

STATUSES = ["PASS", "FAIL", "BOUNDARY", "CORRECTED", "MISMATCH", "INFO"]

SECTIONS = [
    ("A 求导链机器验证（含来料后续项 1：r 不固定展开 + 挠率同名异物台账）", ["A01", "A09"]),
    ("G 静态引力还原通道（本册自设承重项）", ["G01", "G07"]),
    ("K k_B 全套量纲推演（来料后续项 2）", ["K01", "K04"]),
    ("E 实验数据定量检验（本册自设）", ["E01", "E06"]),
    ("T 拓扑电荷", ["T01", "T04"]),
    ("M 残余质量公式", ["M01", "M03"]),
]

KEY_NUMBERS = {
    "helix_identity_pair_kappa_1_over_m": fs(KAPPA, 25),
    "helix_identity_pair_tau_1_over_m": fs(TAU, 25),
    "helix_identity_kappa_sq_plus_tau_sq": fs(_lhs, 25),
    "helix_identity_omega_over_c_sq": fs(_rhs, 25),
    "helix_identity_residual": fs(_res_a06, 6),
    "helix_kappa_over_tau": fs(_kt, 25),
    "helix_v_theta_over_v_z": fs(_vv, 25),
    "bohr_anchor_kappa_1_over_m": fs(_KAPPA_BOHR, 25),
    "bohr_anchor_tau_1_over_m": fs(_TAU_BOHR, 25),
    "alpha_internal_from_a0": fs(_alpha_int, 25),
    "alpha_codata_literal": fs(C_ALPHA, 25),
    "alpha_gap": fs(_alpha_gap, 6),
    "omega_bohr_s^-1": fs(_omega_bohr, 25),
    "omega_compton_s^-1": fs(_omega_comp, 25),
    "bohr_orbit_period_s": fs(_t_bohr, 25),
    "v_theta_earth_needed_m_s": fs(_vt_at_earth, 25),
    "v_earth_kepler_m_s": fs(_vE, 25),
    "k_B_atomic_units_T_s": fs(_kB_a, 25),
    "rotG_predicted_s^-2": fs(_curlG, 25),
    "G_predicted_1m_m_s^-2": fs(_G_pred, 25),
    "excess_over_gravimeter": fs(_excess, 25),
    "schwarzschild_radius_sun_m": fs(_rs_sun, 25),
    "mars_period_kepler_pred_d": fs(_pred_kepler, 25),
    "mars_period_1_over_r_pred_d": fs(_pred_1over_r, 25),
    "mars_period_observed_d": fs(_t_mars, 25),
}

lines = []
lines.append("=" * 78)
lines.append("r95 | 螺旋时空理论全维分析（曲率/挠率/频率/角速度）| 机器判决报告")
lines.append("=" * 78)
lines.append("")
for _name, _rng in SECTIONS:
    lines.append("--- %s ---" % _name)
    for _it in ITEMS:
        if _rng[0] <= _it["code"] <= _rng[1] or _it["code"] in _rng:
            lines.append("[%s] %s" % (_it["status"], _it["title"]))
            if _it["detail"]:
                lines.append("      %s" % _it["detail"])
    lines.append("")
lines.append("--- 外部输入账（理论侧 %d 项 + 实验常数）---" % len(EXT_INPUTS))
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
    print(REPORT)
    os.makedirs(DIR_DATA, exist_ok=True)
    _stem = "TUFT-r95_螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17"
    _payload = {
        "round": "r95",
        "date": "2026-10-17",
        "topic": "螺旋时空理论（曲率/挠率/频率/角速度）全维分析",
        "source_fulltext": "数据/TUFT-螺旋时空理论_来料全文_2026-10-17.md",
        "items": ITEMS,
        "guards": GUARDS,
        "counts": {
            "PASS": N_PASS, "FAIL": N_FAIL, "BOUNDARY": N_BOUND,
            "INFO": N_INFO, "CORRECTED": N_CORR, "MISMATCH": N_MIS,
            "total": len(ITEMS),
            "guard_pass": sum(1 for g in GUARDS if g["ok"]),
            "guard_total": len(GUARDS),
        },
        "external_inputs": [{"name": n, "desc": d} for n, d in EXT_INPUTS],
        "key_numbers": KEY_NUMBERS,
    }
    with io.open(os.path.join(DIR_DATA, _stem + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(_payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DIR_DATA, _stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(REPORT)
    _md = ["# 数据产物｜r95 螺旋时空理论全维分析（2026-10-17）", "",
           "来源正本：[TUFT-螺旋时空理论_来料全文_2026-10-17.md](TUFT-螺旋时空理论_来料全文_2026-10-17.md)",
           "判定册：[判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md](../判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md)",
           "", "```", REPORT, "```", ""]
    with io.open(os.path.join(DIR_DATA, _stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
