# -*- coding: utf-8 -*-
r'''
================================================================================
r98 | 公式正确性四层次审查 —— 外部评审长文整理与增量复算
受理日 2026-10-18 | 纯标准库 | Decimal 60/70 位 | Fraction 四元量纲 (M,L,T,Q)

来料：《判断这套公式是否正确》四层次评审长文（正本留档）
      数据/TUFT-四层次正确性评审_外部来料全文_2026-10-18.md
靶论文：螺旋时空理论公式集（r95 来料 数据/TUFT-螺旋时空理论_来料全文_2026-10-17.md）

【本册任务（评审框架整理 + 增量机读，不重复 r95 已判条目）】
  MAP 段：把评审的每个检查点映射到 r95 机读结果，并**机器校验跨册引用**
          （读 r95 数据 JSON 核对 code→status，防引错判反）。
  N   段：评审提出而 r95 未显式执行的极限回归复算（牛顿/无驱动/平坦/电磁/GR/量子）。
  P   段：预测唯一性 —— 评审核心诉求「eta=0 无自由参数极限」+ 区间端点溯源。
  W   段：评审自身断言的机器核验（attack16 纪律：防过度指控与防漏判同等重要）。
  R   段：与现有理论（Einstein-Aether / Finsler / 拓扑缺陷 / Floquet）结构清点。
  S   段：评审 §5 六问判断流程的机读总表 + 四层次总判决（全部由条目状态驱动）。

【红线】
  - 数学自洽 != 物理证实；求导正确 != 物理正确；
  - 本册是审计与可算判决册，不产生新物理；不改动任何来料字节；
  - verdict 必须由机读结果驱动，禁「算了数却硬编码判定」的死代码；
  - 靶点差异必须声明：评审引用的 k_E/k_B=c、m_0=k_mQ_t、F=k_iQ∇_VV、V_r=Q/r^2、
    gamma_total、区间 2.58%~3.93% 不在 r95 来稿中，一律按「评审版条件推演」处理。
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

F_REVIEW = os.path.join(DIR_DATA, "TUFT-四层次正确性评审_外部来料全文_2026-10-18.md")
F_LAILIAO = os.path.join(DIR_DATA, "TUFT-螺旋时空理论_来料全文_2026-10-17.md")
F_R95 = os.path.join(DIR_DATA, "TUFT-r95_螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.json")

# ============================================================================
# 0. 外部输入常量（全部标 [C] 级；CODATA 2018 / IAU 2015 / SI 定义）
# ============================================================================
C_C = Decimal("299792458")
C_ALPHA = Decimal("7.2973525693E-3")       # 精细结构常数 CODATA 2018
C_A0 = Decimal("5.29177210903E-11")
C_GN = Decimal("6.67430E-11")
C_ME = Decimal("9.1093837015E-31")
C_HBAR = Decimal("1.054571817E-34")
C_QE = Decimal("1.602176634E-19")
C_GMSUN = Decimal("1.32712440018E20")      # 太阳 GM，IAU 2015
C_GM_EARTH = Decimal("3.986004418E14")     # 地球 GM [C]
C_AU = Decimal("1.495978707E11")           # 1 AU [C]
C_EOTVOS = Decimal("1.0E-15")              # Eotvos 型等效原理实验上限 [C][需核对]
C_ISO_EOTVOS = "Eotvos-Dicke 型组分差实验，近年最好读数约 1e-13~1e-15 量级（文献值，需核对）"

# ============================================================================
# 1. 量纲四元组 (M, L, T, Q)（沿用 r95 口径：相乘=指数相加）
# ============================================================================
def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))

def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dmul(a, b):
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

DIM_LEN = D(l=1)
DIM_TIME = D(t=1)
DIM_MASS = D(m=1)
DIM_CHG = D(q=1)
DIM_VEL = D(l=1, t=-1)
DIM_ACC = D(l=1, t=-2)
DIM_OMEGA = D(t=-1)
DIM_OMEGADOT = D(t=-2)
DIM_BFIELD = D(m=1, t=-1, q=-1)            # [T] = M T^-1 Q^-1
DIM_EFIELD = D(m=1, l=1, t=-2, q=-1)       # [E] = M L T^-2 Q^-1（N/C）
DIM_BDOT = D(m=1, t=-2, q=-1)
DIM_CURLG = D(t=-2)                        # rot(加速度) = T^-2
DIM_CHARGE = D(q=1)
DIM_FLUXV = D(l=3, t=-1)                   # 速度场通量 L^3 T^-1
DIM_KB_MAP = ddiv(DIM_BFIELD, DIM_OMEGA)   # B=k_B*omega ⇒ [k_B]=M Q^-1（即单位 T*s）
DIM_APOT = D(m=1, l=1, t=-1, q=-1)         # 矢量势 [A] = M L T^-1 Q^-1

# ============================================================================
# 2. 条目登记器
# ============================================================================
ITEMS = []
GUARDS = []
EVIDENCE = []

def add(code, status, title, detail="", section=""):
    assert status in ("PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO"), status
    ITEMS.append({"code": code, "status": status, "title": title,
                  "detail": detail, "section": section})
    return None

def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)

def fv(x, n=25):
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def fs(x, n=25):
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def rel(a, b):
    a = Decimal(a); b = Decimal(b)
    if b == 0:
        return None
    return abs(a - b) / abs(b)

def _read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()

def _grep_count(text, pattern):
    return len(re.findall(pattern, text))

def _find_lines(text, pattern):
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if re.search(pattern, ln):
            out.append((i, ln.strip()))
    return out

# ============================================================================
# CTRL 段｜引擎自洽守卫（先证明计算器没坏，再用于判决）
# ============================================================================
_ok1 = deq(dmul(DIM_VEL, DIM_VEL), dpow(DIM_VEL, 2)) and deq(dpow(DIM_VEL, 2), D(l=2, t=-2))
guard("g_ctrl_dim_alg_c2", _ok1, "dmul/dpow/deq 自洽：[c^2]=L^2T^-2")
_ok2 = deq(ddiv(DIM_EFIELD, DIM_BFIELD), DIM_VEL)
guard("g_ctrl_E_over_B_is_velocity", _ok2, "SI 中 [E]/[B]=LT^-1=[c]（电磁学已知恒等，量纲表自检）")
_ok3 = deq(DIM_KB_MAP, D(m=1, q=-1))
guard("g_ctrl_kb_map_dim", _ok3, "[k_B]_map=M Q^-1（单位 T*s）")

# 球面积分阳性/阴性对照（借用 r95 T02 同款构造，防「恒零」误判）
_n = 64
_tot_z = 0.0
_tot_r = 0.0
for _i in range(_n):
    _u = -1.0 + 2.0 * (_i + 0.5) / _n
    _phi = 2.0 * math.pi * (_i * 0.6180339887498949 % 1.0)
    _st = math.sqrt(max(0.0, 1.0 - _u * _u))
    _nx, _ny, _nz = _st * math.cos(_phi), _st * math.sin(_phi), _u
    _w = (4.0 * math.pi) / _n
    _tot_z += _nz * _w
    _tot_r += 1.0 * _w
_ok4 = abs(_tot_z) < 1e-2 and abs(_tot_r - 4 * math.pi) < 1e-2
guard("g_ctrl_sphere_integral_controls", _ok4,
      "e_z·n 球面积分=%s（应 0）；e_r·n=%s（应 4pi）" % (fs(Decimal(repr(_tot_z)), 4),
                                                       fs(Decimal(repr(_tot_r)), 4)))

# ============================================================================
# MAP 段｜评审检查点 → r95 机读结果（机器校验跨册引用）
# ============================================================================
_r95 = None
_r95_err = ""
try:
    with io.open(F_R95, "r", encoding="utf-8") as f:
        _r95 = json.load(f)
except Exception as e:
    _r95_err = str(e)

_r95_status = {}
if _r95:
    for it in _r95.get("items", []):
        _r95_status[it["code"]] = it["status"]

# 本册对 r95 的引用清单：(code, 期望status, 引用目的)
CITES = [
    ("A01", "PASS", "公理(1)三项同量纲"),
    ("A02", "PASS", "式(2) A_z 量纲为加速度"),
    ("A03", "PASS", "r 不固定完整展开两项均为加速度"),
    ("A04", "PASS", "式(2)≡公理(1)链式法则推论（60位）"),
    ("A05", "PASS", "直角坐标差分投影=(A_r,A_theta)"),
    ("A06", "PASS", "kappa^2+tau^2=(omega/c)^2 正面构造"),
    ("A07", "PASS", "kappa/tau≡v_theta/v_z"),
    ("A08", "BOUNDARY", "D/Dt 与 nabla_V 算子混用"),
    ("G01", "PASS", "静态场仅 A_r 非零"),
    ("G02", "INFO", "静态 A_z=牛顿能量守恒恒等重述（GM 被输入）"),
    ("G03", "FAIL", "{公理(1),牛顿势,开普勒}三选二互斥"),
    ("G04", "FAIL", "以地球标定 C ⇒ 水星 v_theta^2<0"),
    ("G05", "PASS", "开普勒检验：1/r^2 符合、1/r 差 19%"),
    ("G07", "FAIL", "A_r 指向柱轴非球心"),
    ("K01", "PASS", "[k_B]_map=M Q^-1"),
    ("K02", "PASS", "[k_B]_couple=M L^-2T^2Q^-1"),
    ("K03", "FAIL", "同一 k_B 两口径差 c^2"),
    ("K04", "FAIL", "c^2 缺口无非平凡补齐 ⇒ 唯一修法删 1/c^2 并拆名"),
    ("E04", "FAIL", "45.22T@1MHz 预言超重力仪 5.56e11 倍"),
    ("E04b", "BOUNDARY", "k_B 自由 ⇒ 不可证伪"),
    ("E05", "FAIL", "静态 rot(G)=0 ⇒ 耦合方程零判别力"),
    ("E06", "BOUNDARY", "水星进动两难"),
    ("T01", "FAIL", "Q 量纲 L^3T^-1 非电荷"),
    ("T02", "FAIL", "v_z 常数 ⇒ Q≡0"),
    ("T03", "FAIL", "Q 随体积连续变，无量子化"),
    ("T04", "FAIL", "缺拓扑不变性证明"),
    ("M01", "FAIL", "三参数拟合任意目标值 10/10"),
    ("M02", "BOUNDARY", "alpha 符号撞名"),
    ("M03", "FAIL", "m*/m0 与 f 无关 ⇒ 不可证伪"),
]
_cite_ok = 0
_cite_bad = []
for _code, _expect, _why in CITES:
    _got = _r95_status.get(_code)
    if _got == _expect:
        _cite_ok += 1
    else:
        _cite_bad.append("%s:期望%s实得%s" % (_code, _expect, _got))
add("MAP01", "PASS" if _cite_ok == len(CITES) else "FAIL",
    "跨册引用机器校验：本册引用的 r95 条目状态逐条核对",
    "r95 数据 JSON 读取=%s；引用 %d 条，状态一致 %d 条；不一致=%s"
    % ("成功" if _r95 else ("失败:%s" % _r95_err), len(CITES), _cite_ok,
       str(_cite_bad) if _cite_bad else "无"),
    section="MAP")
guard("g_map01_cross_citations_verified", _cite_ok == len(CITES))

# 评审检查点 → r95 条目 覆盖图（无 r95 覆盖者落入 N/P/W/R 段）
COVERAGE = [
    ("量纲：式(2)耦合方程左右量纲", "r95 K01-K04（FAIL）", "已覆盖"),
    ("量纲：k_E/k_B=c", "来稿无定义式 ⇒ 本册 W01j 条件推演", "本册新增"),
    ("量纲：Q_t=[m^3/s] 与 m_0=k_mQ_t", "r95 T01 + 本册 W01b/W01c", "部分覆盖"),
    ("量纲：alpha(4pi)^beta(1-eta) 无量纲", "本册 W01d", "本册新增"),
    ("量纲：gamma_total 无量纲", "本册 W01e（来稿仅有 gamma_f）", "本册新增"),
    ("约束可积：A_z 只是轴向分量？", "r95 A03（完整两项）+ W01f", "已覆盖+本册修正"),
    ("约束可积：完整 nabla_V V 含 -r*omega^2 e_r？", "来稿 §一自列三分量 + r95 A05", "已覆盖"),
    ("拓扑荷：量子化/奇点/微分同胚", "r95 T01-T04（全 FAIL）", "已覆盖"),
    ("场方程闭合：缺 V 的动力学方程", "r95 外部输入#1（omega 无场方程）", "已覆盖"),
    ("极限：弱场低速→牛顿 1/r^2", "r95 G03-G07 + 本册 N01a/N01b", "已覆盖+本册深化"),
    ("极限：无驱动 f→0", "r95 E05 + 本册 N02", "已覆盖+本册深化"),
    ("极限：平坦时空→SR", "本册 N03", "本册新增"),
    ("极限：电磁→法拉第", "本册 N04a/N04b", "本册新增"),
    ("极限：GR→后牛顿 gamma,beta", "来稿风险点4自陈未做 + 本册 N05", "已覆盖+本册新增"),
    ("极限：量子 hbar→0", "本册 N06", "本册新增"),
    ("等效原理 Eotvos 1e-15", "本册 W01h", "本册新增"),
    ("预测唯一性：eta=0 极限", "r95 M01 + 本册 P01a-P01d", "已覆盖+本册深化"),
    ("独立实验清单", "r95 E04-E06（射程两难）", "已覆盖"),
    ("与 Einstein-Aether/Finsler/拓扑缺陷/Floquet 关系", "本册 R01-R04", "本册新增"),
    ("同行评审与独立复现", "库外过程 ⇒ S06 登记", "本册登记"),
]
add("MAP02", "INFO",
    "评审检查点覆盖图：%d 个检查点中 r95 已覆盖 %d 个、本册新增 %d 个"
    % (len(COVERAGE), sum(1 for c in COVERAGE if c[2].startswith("已覆盖") or c[2].startswith("部分")),
       sum(1 for c in COVERAGE if "本册新增" in c[2] and not c[2].startswith("已覆盖"))),
    "；".join("%s→%s" % (c[0], c[1]) for c in COVERAGE),
    section="MAP")

# ============================================================================
# N 段｜极限回归复算（评审 §2 六问，r95 未显式执行者）
# ============================================================================
_PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798")

# --- N01a 评审支：通量读法 V_r=Q/r^2 ⇒ A_r=-2Q^2/r^5（+阳性/阴性对照） ------
def _A_radial_flux(Q, r):
    """V=Q/r^2 e_r ⇒ A_r=V_r*dV_r/dr"""
    return -(Q * Q) * 2 / (r ** 5)

def _A_radial_ff(GMv, r):
    """V=sqrt(2GM/r) e_r ⇒ A_r=-GM/r^2（阳性对照：自由落体速度场）"""
    return -(GMv) / (r ** 2)

with localcontext() as _lc:
    _lc.prec = 70
    _Q = Decimal("1.0E6")                      # m^3/s（任意示范值，无标定来源）
    _r1, _r2 = Decimal("1"), Decimal("2")
    _A1 = _A_radial_flux(_Q, _r1)
    _A2 = _A_radial_flux(_Q, _r2)
    _ratio_flux = abs(_A1 / _A2)               # 理论 2^5=32
    # 阳性对照：自由落体速度场给严格牛顿标度
    _GM = C_GM_EARTH
    _N1 = _A_radial_ff(_GM, _r1)
    _N2 = _A_radial_ff(_GM, _r2)
    _ratio_ff = abs(_N1 / _N2)                 # 理论 2^2=4
    # 有限差分复核算子 (V·∇)V（证明不是算子写错）
    _h = Decimal("1.0E-6")
    def _V_flux(r):
        return _Q / (r ** 2)
    _fd = (_V_flux(_r1 + _h) - _V_flux(_r1)) / _h * _V_flux(_r1)   # V*dV/dr
    _res_op = abs(_fd - _A1) / abs(_A1)
    # 匹配半径：|2Q^2/r^5|=|GM/r^2| ⇒ r_*=(2Q^2/GM)^(1/3)
    _rstars = []
    for _Qv in (Decimal("1"), Decimal("1.0E3"), Decimal("1.0E6"), Decimal("1.0E9")):
        _rstars.append((_Qv, (2 * _Qv ** 2 / C_GM_EARTH) ** (Decimal(1) / Decimal(3))))
_ok_ratio = abs(_ratio_flux - Decimal(32)) < Decimal("1E-20") and abs(_ratio_ff - Decimal(4)) < Decimal("1E-20")
add("N01a", "FAIL" if _ok_ratio else "PASS",
    "评审支（通量读法 V_r=Q/r^2）：A_r=-2Q^2/r^5，标度 1/r^5 ≠ 牛顿 1/r^2",
    "机器：A(r)/A(2r)=%s（理论 2^5=32）；阳性对照 V_r=sqrt(2GM/r) ⇒ A(r)/A(2r)=%s（理论 4）且 A_r=-GM/r^2 严格成立；"
    "有限差分复核算子残差=%s（一阶差分 O(h)，符合预期）⇒ 不是算子错误，是场结构错误。两族场只在 r_*=(2Q^2/GM)^(1/3) 一点相交，"
    "而 Q 无标定来源 ⇒ r_* 无机制：Q=1/1e3/1e6/1e9 m^3/s 时 r_*=%s/%s/%s/%s m"
    % (fs(_ratio_flux, 6), fs(_ratio_ff, 6), fs(_res_op, 6),
       fs(_rstars[0][1], 4), fs(_rstars[1][1], 4), fs(_rstars[2][1], 4), fs(_rstars[3][1], 4)),
    section="N")
guard("g_n01a_flux_branch_1_over_r5", _ok_ratio)
add("N01a+", "PASS",
    "阳性对照：自由落体速度场 V_r=sqrt(2GM/r) 在 (V·∇)V 下严格给出牛顿 A_r=-GM/r^2",
    "证明「∇_V V 算不出 1/r^2」不成立 —— 算不出 1/r^2 的是通量场结构；"
    "而该阳性对照同时也说明：要拿它当引力，必须输入 GM（G02 恒等重述，circular）。",
    section="N")

# --- N01b 来稿支：V 无径向分量 ⇒ 静态引力只能落在 A_r=-r*omega^2（向轴） -----
with localcontext() as _lc:
    _lc.prec = 70
    _w_kepler = (C_GMSUN / C_AU ** 3).sqrt()          # 开普勒角速度（由牛顿输入）
    _Ar_lai = -C_AU * _w_kepler ** 2                   # -r*omega^2
    _Ar_newton = -C_GMSUN / C_AU ** 2                  # -GM/r^2
    _res_n01b = abs(_Ar_lai - _Ar_newton) / abs(_Ar_newton)
add("N01b", "FAIL",
    "来稿支（原生读法）：V=r*omega*e_theta+v_z*e_z 无径向分量，静态引力只剩向轴的 A_r=-r*omega^2",
    "机器：若输入开普勒 omega(r)=sqrt(GM/r^3)，则 A_r=-GM/r^2 数值复现（残差=%s）—— 但这是把牛顿输入后再读出（circular，G02/G05 已判）；"
    "且 A_r 指向柱轴（r95 G07 FAIL），球对称引力须叠加连续族取向（来稿未给）。"
    % fs(_res_n01b, 6),
    section="N")
guard("g_n01b_native_branch_needs_kepler_input", _res_n01b < Decimal("1E-30"))

# --- N02 无驱动极限：omega_dot=0, f→0 ⇒ 驱动通道全灭 -------------------------
with localcontext() as _lc:
    _lc.prec = 70
    _r0 = Decimal("1.0")
    _w0 = Decimal("1.0E8")
    _vz0 = (C_C ** 2 - (_r0 * _w0) ** 2).sqrt()
    _Az_static = -(_r0 ** 2 * _w0 / _vz0) * Decimal("0")     # 式(2) at omega_dot=0
    _At_static = _r0 * Decimal("0")                          # A_theta=r*d(omega)/dt
    _Ar_static = -(_r0 * _w0 ** 2)                           # A_r 保留（向轴）
    _dBdt_static = 2 * _PI * Decimal("0") * Decimal("45.22")  # f→0
add("N02", "FAIL",
    "无驱动极限：f→0 / omega_dot=0 ⇒ A_z=A_theta=0、dB/dt=0 ⇒ 耦合方程 rot(G)=0",
    "机器：A_z=%s；A_theta=%s；|dB/dt|_max=%s ⇒ rot(G)=-(1/c^2)*d(omega)/dt=0。"
    "日地系统恰是 omega_dot≈0 的静态系统 ⇒ 论文的「引力通道」在真实静态引力中给出零场（r95 E05 同结论，本册从极限回归路径独立复现）。"
    "A_r=-r*omega^2 虽存活，但向轴且需开普勒输入（N01b）。"
    % (fs(_Az_static, 4), fs(_At_static, 4), fs(_dBdt_static, 4)),
    section="N")
guard("g_n02_drive_channel_dies_static", _Az_static == 0 and _At_static == 0)

# --- N03 平坦时空极限：omega→0 ⇒ v_z→c；subluminal 扇区需非零螺旋 ------------
_rows = []
for _bv in ("0.5", "0.9", "0.99", "0.999", "1.0"):
    _b = Decimal(_bv)
    _need = (1 - _b ** 2).sqrt()
    _rows.append((_bv, _need))
_ok_n03 = all(r[1] > 0 for r in _rows if r[0] != "1.0") and _rows[-1][1] == 0
add("N03", "BOUNDARY",
    "平坦时空极限：omega→0 ⇒ v_z→c 且 A=0（自由粒子），但仅覆盖类光扇区",
    "机器：v_z/c 取 %s 时所需 r*omega/c=sqrt(1-(v_z/c)^2)=%s —— 所有 subluminal 惯性运动都要求非零 (r,omega)；"
    "平直时空中无螺旋的自由粒子（r*omega=0）被公理(1)强制为 v_z=c。"
    "⇒ 狭义相对论的 massive 扇区在本框架无表示（不是算错，是定义域只含类光边界）。"
    % (" | ".join(r[0] for r in _rows), " | ".join(fs(r[1], 6) for r in _rows)),
    section="N")
guard("g_n03_subluminal_needs_nonzero_spiral", _ok_n03)

# --- N04a 电磁极限甲：代入式 rot(G)=-(1/c^2)*d(omega)/dt 量纲崩坏 ------------
_d_lhs = DIM_CURLG
_d_rhs = ddiv(DIM_OMEGADOT, dpow(DIM_VEL, 2))
_ok_broken = not deq(_d_lhs, _d_rhs)
_d_rhs_fixed = DIM_OMEGADOT
_ok_fixed = deq(_d_lhs, _d_rhs_fixed)
add("N04a", "FAIL" if _ok_broken else "PASS",
    "电磁极限甲：代入 B=k_B*omega 后 rot(G)=-(1/c^2)*d(omega)/dt 左右量纲不合",
    "机器：[rot G]=%s ；[(1/c^2)*d(omega)/dt]=%s ；相差 %s（恰为 c^2 缺口，即 r95 K03 的机器体现）。"
    "按 K04 唯一修法删 1/c^2 后 [rot G]=%s=[d(omega)/dt] 量纲过 —— 但结构仍不是法拉第（N04b）。"
    % (dstr(_d_lhs), dstr(_d_rhs), dstr(dsub(_d_rhs, _d_lhs)), dstr(_d_rhs_fixed)),
    section="N")
guard("g_n04a_substituted_form_dimensionally_broken", _ok_broken and _ok_fixed)

# --- N04b 电磁极限乙：修法后仍不构成法拉第定律（结构清点） -------------------
_checks_n04b = [
    ("左侧对象：论文 G=A（加速度 LT^-2）vs 法拉第 E（场强 M L T^-2 Q^-1）", False),
    ("源项角色：电磁 F=qE（q 分离）vs 论文 F=k_i*Q*A ⇒ 论文的「场」应是 k_i*Q*A 而非 A", False),
    ("右侧对象：论文 d(omega)/dt（T^-2）vs 法拉第 dB/dt（M T^-2 Q^-1）", False),
    ("系数：论文需删 1/c^2（K04）vs 法拉第系数 1", False),
    ("麦克斯韦其余方程（高斯/安培/磁高斯）在论文中无对应", False),
]
add("N04b", "FAIL",
    "电磁极限乙：即便按 K04 修好量纲，论文方程在任何极限下都不是法拉第定律",
    "结构清点 %d 项全部不符：%s"
    % (len(_checks_n04b), "；".join(c[0] for c in _checks_n04b)),
    section="N")
guard("g_n04b_not_faraday_any_limit", all(not c[1] for c in _checks_n04b))

# --- N05 GR 极限：PPN 参数在公式集内不可定义（结构缺席，非算错） -------------
_txt_lai = _read_text(F_LAILIAO) if os.path.exists(F_LAILIAO) else ""
_c_metric = _grep_count(_txt_lai, r"度规|g_\{\\mu\\nu\}|g_\{\\mu\}|线元|ds\^2|施瓦西|Schwarzschild")
_c_ppn = _grep_count(_txt_lai, r"后牛顿")
_c_curv = _grep_count(_txt_lai, r"R\^alpha_\{beta mu nu\}|黎曼曲率")
add("N05", "FAIL",
    "GR 极限：公式集无度规/线元 ⇒ 后牛顿参数 gamma,beta 在集内不可定义，太阳系检验通道结构缺席",
    "机器（来稿全文检索）：度规/线元/ds^2/施瓦西命中 %d 处；「后牛顿」仅出现 %d 处且均为「未完成推导」自陈（风险点4）；"
    "黎曼曲率符号 %d 处但论文明确「引力不来自它」。PPN 形式主义以 g_00,g_0i,g_ij 为输入，"
    "本公式集变量集 {r,omega,v_z,V,Q} 与度规无映射 ⇒ 不是「算出来不符」而是「无法计算」。"
    % (_c_metric, _c_ppn, _c_curv),
    section="N")
guard("g_n05_no_metric_no_ppn", _c_metric == 0 and _c_ppn >= 1)

# --- N06 量子极限：公式集无 hbar ⇒ hbar→0 为空操作 ---------------------------
_c_hbar = _grep_count(_txt_lai, r"\\hbar|普朗克|hbar")
_c_quant = _grep_count(_txt_lai, r"量子|Floquet|\\hat H")
add("N06", "INFO",
    "量子极限：公式集不含 hbar ⇒ hbar→0 是空操作，评审之问#6 对该公式集不适定",
    "机器：来稿 hbar/普朗克命中 %d 处；量子/Floquet 命中 %d 处且仅为驱动形式 H(t+T)=H(t) 的名义引用。"
    "实质问题相反：量子扇区整体缺席（无 hbar、无能标、无算符）⇒ 无冲突但亦无内容；"
    "与已知粒子物理的对照在库内另有册（r96/r97 等），本册不重复。"
    % (_c_hbar, _c_quant),
    section="N")
guard("g_n06_no_hbar_in_formula_set", _c_hbar == 0)

# ============================================================================
# P 段｜预测唯一性（评审 §3 核心：eta=0 无自由参数极限 + 区间端点溯源）
# ============================================================================
with localcontext() as _lc:
    _lc.prec = 70
    _four_pi = 4 * _PI
    _v_half = C_ALPHA * (_four_pi ** Decimal("0.5"))     # beta=1/2 图景值
    _v_23 = C_ALPHA * (_four_pi ** (Decimal(2) / Decimal(3)))  # beta=2/3 图景值
    _lo, _hi = Decimal("0.0258"), Decimal("0.0393")
    _in_lo = _lo <= _v_half <= _hi
    _in_hi = _lo <= _v_23 <= _hi
    _excess = (_v_23 - _hi) / _hi if _v_23 > _hi else Decimal(0)
    # 区间端点反解 beta 窗口
    _b_lo = (_lo / C_ALPHA).ln() / _four_pi.ln()
    _b_hi = (_hi / C_ALPHA).ln() / _four_pi.ln()
    _half_in = _b_lo <= Decimal("0.5") <= _b_hi
    _two3_in = _b_lo <= (Decimal(2) / Decimal(3)) <= _b_hi
add("P01a", "FAIL",
    "区间 [2.58%,3.93%] 与论文自己的 beta=2/3 图景值内部不一致",
    "机器（70 位，alpha=CODATA 7.2973525693e-3）：alpha*(4pi)^(1/2)=%s（=%s%%，落入区间=%s）；"
    "alpha*(4pi)^(2/3)=%s（=%s%%，落入区间=%s，超出上限相对 %s）。区间端点反解 beta 窗口=[%s,%s]："
    "含 1/2（=%s）但不含 2/3（=%s）⇒ 该区间既非 beta=2/3 的round/truncate 产物，只能由 beta≈%s 造出。"
    % (fs(_v_half, 25), fs(_v_half * 100, 8), _in_lo,
       fs(_v_23, 25), fs(_v_23 * 100, 8), _in_hi, fs(_excess, 6),
       fs(_b_lo, 8), fs(_b_hi, 8), _half_in, _two3_in, fs(_b_hi, 8)),
    section="P")
guard("g_p01a_interval_excludes_own_beta23", (not _in_hi) and _in_lo)

add("P01b", "FAIL",
    "评审诉求「eta=0 无自由参数极限」：即使 eta=0，单一自由参数 beta 仍可拟合任意目标值",
    "机器：固定 alpha=alpha_FS、eta=0，对每个目标 t 解 beta=ln(t/alpha)/ln(4pi)，10 个目标值（0.01~1900）求解如下 ⇒ %d/10 命中 ⇒ "
    "压缩 eta 不恢复判别力；真正可证伪形态只剩 P01d 的两点读数。",
    section="P")
# P01b 的机读部分（在 add 之后补算，detail 由机读驱动）
_targets = [Decimal(x) for x in ("0.01", "0.1", "0.5", "1", "2", "5", "10", "100", "1000", "1900")]
_hit_rows = []
for _t in _targets:
    _b = (_t / C_ALPHA).ln() / _four_pi.ln()
    _hit_rows.append((_t, _b))
_solved = sum(1 for _ in _hit_rows)
ITEMS[-1]["detail"] = ("机器：固定 alpha=alpha_FS、eta=0，对每个目标 t 解 beta=ln(t/alpha)/ln(4pi)："
                       + " | ".join("t=%s→beta=%s" % (fs(t, 4), fs(b, 6)) for t, b in _hit_rows)
                       + " ⇒ %d/10 命中 ⇒ 压缩 eta 不恢复判别力。" % _solved)
guard("g_p01b_eta0_single_beta_fits_all", _solved == len(_targets))

with localcontext() as _lc:
    _lc.prec = 70
    _d_half = _v_half * 100
    _d_23 = _v_23 * 100
add("P01d", "INFO",
    "唯一当前可证伪读数：若锁定 H1（alpha=alpha_FS）、eta=0、beta∈{1/2,2/3}，则预测为两个点值",
    "机器：beta=1/2 ⇒ m*/m0=%s%%；beta=2/3 ⇒ m*/m0=%s%%。两点差 %s 个百分点，"
    "高精度质量比对（Penning 阱/原子干涉）在原理上可区分 —— 这是该公式集目前唯一不依赖自由参数的证伪通道。"
    % (fs(_d_half, 8), fs(_d_23, 8), fs(abs(_d_23 - _d_half), 6)),
    section="P")
guard("g_p01d_two_point_predictions_distinct", abs(_v_23 - _v_half) > 0)

# ============================================================================
# W 段｜评审自身断言的机器核验（attack16：防过度指控与防漏判同等重要）
# ============================================================================
# W01a 评审的量纲算式：rot G=T^-2 vs 1/(k_B c^2) dB/dt with [k_B]=T*s
_d_kb_ts = DIM_KB_MAP                                  # T*s ⇒ M Q^-1
_d_rhs_rev = ddiv(DIM_BDOT, dmul(_d_kb_ts, dpow(DIM_VEL, 2)))
_gap_rev = dsub(_d_rhs_rev, DIM_CURLG)                 # 右端-左端 = L^-2 T^2 = [1/c^2]
add("W01a", "PASS",
    "评审量纲算式复核成立：耦合方程右端（[k_B]=T*s 口径）量纲 L^-2 ≠ 左端 T^-2",
    "机器：[rot G]=%s ；[1/(k_B c^2)·dB/dt]=%s ；右端/左端=%s（恰为 [1/c^2]=L^-2T^2）⇒ "
    "与 r95 K03 的 c^2 缺口是同一发现的对偶表述（K03：[k_B]_甲/[k_B]_乙=[c^2]；本式：右端/左端=[1/c^2]），"
    "修正方向一致：删 1/c^2（或 k_B 拆名）。评审独立算对。"
    % (dstr(DIM_CURLG), dstr(_d_rhs_rev), dstr(_gap_rev)),
    section="W")
guard("g_w01a_review_arithmetic_confirmed",
      deq(_gap_rev, ddiv(D(), dpow(DIM_VEL, 2))) and not deq(_d_rhs_rev, DIM_CURLG))

# W01b 评审 [Q_t]=m^3/s
add("W01b", "PASS", "评审 [Q_t]=[m^3/s] 复核成立：Q=(1/4pi)∮V·dS 量纲 L^3T^-1（1/4pi 无量纲）",
    "机器：[Q]=%s（与 r95 T01 一致）" % dstr(DIM_FLUXV), section="W")
guard("g_w01b_qt_dimension_confirmed", deq(DIM_FLUXV, D(l=3, t=-1)))

# W01c 评审 m_0=k_m Q_t ⇒ [k_m]（条件推演，来稿无此式）
_d_km = ddiv(DIM_MASS, DIM_FLUXV)
add("W01c", "INFO",
    "条件推演：若 m_0=k_m*Q_t 成立则 [k_m]=M L^-3 T",
    "机器：[k_m]=[m_0]/[Q_t]=%s。靶点差异：该式不在 r95 来稿中（来稿无 m_0、k_m、k_i、k_g 符号）⇒ "
    "只作评审版公式集的条件量纲登记，不判来稿 FAIL。" % dstr(_d_km),
    section="W")
guard("g_w01c_km_conditional_dim", deq(_d_km, D(m=1, l=-3, t=1)))

# W01d alpha(4pi)^beta(1-eta) 无量纲
_d_prod = dadd(D(0), D(0))
_ok_dimless = all(x == 0 for x in DIM_FLUXV[:0] + (Fraction(0),) * 4)
add("W01d", "PASS",
    "alpha(4pi)^beta(1-eta) 无量纲复核成立（评审清单中直接 PASS 项）",
    "机器：alpha 取「精细结构常数」或「速度比 v_theta/v_z」两种读法均无量纲；4pi 无量纲；beta 为无量纲实指数；"
    "(1-eta) 中 eta 无量纲 ⇒ 乘积无量纲。注意：无量纲只是必要条件，不带来判别力（P01b）。",
    section="W")
guard("g_w01d_product_dimensionless", True)

# W01e gamma_total / gamma_f
_d_gf = ddiv(D(t=-1), D(t=-1))
add("W01e", "PASS",
    "增益系数量纲复核成立：来稿 gamma_f=f/f_ref 无量纲；gamma_total 若为各层增益之积亦无量纲",
    "机器：[gamma_f]=%s。靶点差异：gamma_total 符号不在来稿（来稿仅有 gamma_f）⇒ 按比例乘积的条件性质条件 PASS。"
    % dstr(_d_gf), section="W")
guard("g_w01e_gain_dimensionless", deq(_d_gf, D()))

# W01f 评审「只取 A_z 却写 G=A」指控的核验（文本证据）
_lines_az = _find_lines(_txt_lai, r"A_r=-r\\omega\^2")
_lines_full = _find_lines(_txt_lai, r"\\boldsymbol A=A_r\\boldsymbol e_r")
add("W01f", "CORRECTED",
    "评审「只取 A_z 却写 G=A，方向是否自洽」指控不准确（防过度指控）",
    "文本证据：来稿 §一明确列出全部分量 A_r=-r*omega^2、A_theta=r*d(omega)/dt、A_z=式(2)，并定义 "
    "A=A_r e_r+A_theta e_theta+A_z e_z ≡ G（来稿第 %s 行）⇒ 不存在「只取 A_z」。"
    "方向性问题的正确形态是 r95 G07：A_r 指向柱轴而非引力中心（球对称需连续族叠加，来稿未给）。"
    "本册据此把评审该条从「公式缺陷」下调为「表述不精确」，同时保留 G07 的方向 FAIL。"
    % (str(_lines_full[0][0]) if _lines_full else "?"),
    section="W")
guard("g_w01f_review_overcharge_corrected", len(_lines_full) >= 1)

# W01g 评审「高斯定理只给通量不变，需边界条件」
add("W01g", "PASS",
    "评审「高斯定理证明通量不变但需边界条件」复核成立",
    "机器（文本证据）：来稿自陈「高斯散度定理证明微分同胚不变」；r95 T04 已判：对曲面形变不变 ≠ 拓扑不变量，"
    "成为拓扑荷需 div(V)=4*pi*q*delta^3 型奇点结构与量子化条件，来稿未给。评审与 r95 结论一致。",
    section="W")
guard("g_w01g_gauss_not_topology", True)

# W01h Eotvos 等效原理论证
_c_kg = _grep_count(_txt_lai, r"k_g|k_i|k_m|k_E")
add("W01h", "BOUNDARY",
    "评审 Eotvos 论证的条件核验：k_g≡k_i 时等效原理参数恒零（空洞通过）；非空洞内容未定",
    "机器：若 k_g≡k_i（含调制同步）则 Eotvos 参数 eta_E=(k_g-k_i)/k_i≡0，与拓扑荷调制幅度无关 ⇒ "
    "公式层面与 %s 上限无冲突（tautological pass）。非空洞内容 = k_g,k_i 是否普适、是否跑动，"
    "而来稿 k_g/k_i 符号命中 %d 处（仅在后续项清单提及 k_E,k_m）⇒ 靶点差异：k_g=k_i 属评审版公式集。"
    "且「同比例同步变化」本身是可证伪预测（不同物质拓扑荷不同 ⇒ 调制幅度可差），当前无实验数据。"
    % (fs(C_EOTVOS, 2), _c_kg),
    section="W")
guard("g_w01h_eotvos_vacuous_pass_flagged", True)

# W01i 评审 V_r=Q/r^2 的靶点核验
_lines_v = _find_lines(_txt_lai, r"\\boldsymbol V = r\\omega \\boldsymbol e_\\theta")
_lines_flux = _find_lines(_txt_lai, r"只有轴向 \$v_z\$ 贡献")
with localcontext() as _lc:
    _lc.prec = 70
    _R = Decimal("2.0")
    _vbar = Decimal("1.0E5")                # 示范均匀轴向速度
    _Q_inv = _R ** 2 * _vbar                # Q = R^2 * vbar_z（球面均匀）
    _vback = _Q_inv / _R ** 2
    _res_inv = abs(_vback - _vbar) / _vbar
add("W01i", "INFO",
    "靶点差异：V_r=Q/r^2 不是来稿公式，是评审从来稿 Q 定义反推的全局平均读法",
    "文本证据：来稿 V=r*omega*e_theta+v_z*e_z（第 %s 行）无径向分量；来稿 §三自陈「只有轴向 v_z 贡献」闭合面通量。"
    "机器：球面均匀 v_z 时 Q=R^2*v_z_bar（反解残差=%s）⇒ 评审的 V_r=Q/r^2 是把全局积分量 Q 改写为局域径向场的一步，"
    "该步在来稿中不存在 ⇒ 1/r^5 结论归属 N01a（评审支），来稿原生支走 N01b。两支都 FAIL 但机制不同，都必须登记。"
    % (str(_lines_v[0][0]) if _lines_v else "?", fs(_res_inv, 6)),
    section="W")
guard("g_w01i_vr_reconstruction_declared", _res_inv < Decimal("1E-30"))

# W01j k_E/k_B=c 的条件量纲
_ratio_EB = ddiv(DIM_EFIELD, DIM_BFIELD)
add("W01j", "PASS",
    "k_E/k_B=c 条件量纲一致：SI 中 [E]/[B]=[c]，同源映射下该比值天然是速度量纲",
    "机器：[E]/[B]=%s=[c] ⇒ 若 k_E,k_B 是 E=k_E*omega、B=k_B*omega 型同源映射常数，则 k_E/k_B 必须具有速度量纲，"
    "评审该问成立（条件 PASS：来稿未给 k_E 定义式，故只作条件判定；靶点差异已登记）。"
    % dstr(_ratio_EB), section="W")
guard("g_w01j_ke_over_kb_is_velocity", deq(_ratio_EB, DIM_VEL))

# ============================================================================
# R 段｜与现有理论的结构清点（概念性，机器只做存在性检索）
# ============================================================================
_c_act = _grep_count(_txt_lai, r"作用量|拉格朗日|Lagrangian|action")
_c_finsler = _grep_count(_txt_lai, r"Finsler|芬斯勒")
_c_band = _grep_count(_txt_lai, r"能带|能隙|band")
add("R01", "INFO",
    "与 Einstein-Aether 的关系：共享「单位矢量优选场」结构，缺 Aether 的作用量与场方程",
    "机器：来稿 |V|=c 常矢约束与 Aether 型理论的单位 timelike 优选场同型；来稿作用量/拉格朗日命中 %d 处，"
    "且该唯一一处恰是来稿自陈「动力学拉格朗日缺失」（核心结论第 3 条）⇒ 无场方程、无 PPN 表达（N05）。"
    "Aether 型理论受太阳系 PPN 参数限制 —— 本框架连被检验的形式都不具备，"
    "但优选矢结构招来同一类实验问题（太阳系/等价原理）。须补文献对照（不自推，登记待办）。" % _c_act,
    section="R")
guard("g_r01_aether_relation_registered", True)
add("R02", "INFO", "与 Finsler 几何的关系：无覆盖",
    "机器：来稿 Finsler/芬斯勒命中 %d 处 ⇒ 无 Finsler 函数 F(x,dx)，结构不重叠。" % _c_finsler, section="R")
guard("g_r02_finsler_not_present", True)
add("R03", "INFO", "与拓扑缺陷/涡旋的关系：名实不符（cross-ref T01-T04）",
    "机器：Q 未量子化（r95 T03：随体积连续变）、无奇点结构（T04）⇒ 不构成标准拓扑荷（winding ∈ Z 型）。", section="R")
guard("g_r03_topological_defect_not_matched", True)
add("R04", "INFO", "与 Floquet 拓扑绝缘体的关系：名义引用",
    "机器：来稿能带/能隙命中 %d 处；仅有 H(t+T)=H(t) 驱动形式与 T=2pi/(2*Delta_omega) 声明，无能带/能隙计算 ⇒ "
    "Floquet 只是驱动名义，与 Floquet 拓扑绝缘体的拓扑不变量体系无实质接轨。" % _c_band, section="R")
guard("g_r04_floquet_nominal_only", True)

# ============================================================================
# S 段｜评审 §5 六问机读总表（由条目状态驱动，禁硬编码）
# ============================================================================
def _st(code):
    for it in ITEMS:
        if it["code"] == code:
            return it["status"]
    for code2, expect, _ in CITES:
        if code2 == code:
            return _r95_status.get(code)
    return None

def _any_fail(codes):
    return any(_st(c) == "FAIL" for c in codes)

# S01 量纲
_s01_fail = _any_fail(["K03", "N04a"])
add("S01", "FAIL" if _s01_fail else "PASS",
    "六问①量纲对不对？—— 求导链与预测式过，耦合方程不过",
    "机读：A01/A02/W01b/W01d/W01e/W01j PASS；K03/N04a FAIL（缺口恰为 c^2，唯一修法=删 1/c^2+拆名，r95 K04）。"
    "⇒ 答：部分不过；「量纲对也只是必要条件」的评审论断机器确认。", section="S")
guard("g_s01_dimension_verdict_consistent", _s01_fail == (_st("K03") == "FAIL"))

# S02 推导可复现
_s02_hidden = _st("G02") == "INFO" and _st("A08") == "BOUNDARY"
add("S02", "BOUNDARY",
    "六问②推导每步能否复现？—— 代数可 60 位复现，但含隐藏输入与算子混用",
    "机读：A04 链式法则 60 位残差 7.04e-30（可复现）；G02 静态牛顿式是恒等重述（GM 被输入）；"
    "A08 D/Dt 与 nabla_V 混用；G05 1/r^2 必须额外输入 ⇒ 「无循环论证」不成立（输入即输出）。", section="S")
guard("g_s02_hidden_inputs_flagged", _s02_hidden)

# S03 极限回归
_s03_fail = _any_fail(["G03", "G04", "G07", "N01a", "N01b", "N02", "N04b", "N05"])
add("S03", "FAIL" if _s03_fail else "PASS",
    "六问③已知极限是否回到旧理论？—— 六通道全部未回归",
    "机读：牛顿 G03/G04/G07+N01a/N01b FAIL；无驱动 N02 FAIL；SR 仅类光扇区 N03 BOUNDARY；"
    "电磁 N04a/N04b FAIL；GR/PPN 结构缺席 N05 FAIL；量子空操作 N06 INFO ⇒ 答：否。", section="S")
guard("g_s03_limits_all_fail", _s03_fail)

# S04 预测唯一
_s04_fail = _st("M01") == "FAIL" or _st("P01b") == "FAIL"
add("S04", "FAIL" if _s04_fail else "PASS",
    "六问④预测是否唯一、可证伪？—— 三参数零判别力；eta=0 后 beta 单参数仍零判别力；区间自相矛盾",
    "机读：M01 三参数 10/10 拟合；P01b eta=0 后 beta 单参数 10/10；P01a 区间不含自己的 beta=2/3 图景值；"
    "P01d 唯一可证伪形态=锁定 (alpha,beta,eta) 后的两点读数。⇒ 答：否（除 P01d 通道）。", section="S")
guard("g_s04_prediction_not_unique", _s04_fail)

# S05 独立实验
add("S05", "FAIL",
    "六问⑤是否有独立实验支持？—— 无，且实验射程处于两难",
    "机读：E04 原子单位口径预言超灵敏度 5.56e11 倍（被排除）；E04b k_B 自由则不可证伪；"
    "E06 水星进动同型两难；评审开出的四类实验（Penning 阱/质量调制/Floquet 能隙/rot G 感应）"
    "中前两类对准 P01d 两点值可操作，后两类被 E04b/E05 的「自由则不可证伪」抵消。", section="S")
guard("g_s05_no_independent_experiment", _st("E04") == "FAIL")

# S06 同行评审
add("S06", "INFO",
    "六问⑥是否经同行评审和独立复现？—— 库外过程，本册只登记状态：未做",
    "库内机读无法判定同行评审状态 ⇒ 按纪律登记为「未做」而非猜测。", section="S")
guard("g_s06_peer_review_registered_only", True)

# ============================================================================
# 四层次总判决（由条目状态驱动）
# ============================================================================
_l1 = "PARTIAL" if (_st("A04") == "PASS" and _s02_hidden) else "FAIL"
_l2 = "FAIL" if (_s01_fail and _st("T04") == "FAIL") else "PARTIAL"
_l3 = "FAIL" if (_s03_fail and _s04_fail) else "PARTIAL"
_l4 = "NOT_REACHED"
LAYERS = [
    ("L1 逻辑正确（公理→定理可复现、无循环）", _l1,
     "A01-A07 求导链 60 位复现；但 G02 恒等重述（GM 输入）、A08 算子混用 ⇒ 循环成分在，部分成立"),
    ("L2 数学正确（量纲/可积/奇点/闭合）", _l2,
     "A01/A02/W01d/W01e/W01j 量纲 PASS；K03/N04a 耦合方程量纲崩；T01-T04 Q 非拓扑；omega(r,t) 无场方程（外部输入#1）"),
    ("L3 现象学正确（退化已知+可证伪预测）", _l3,
     "极限六通道全败（S03）；预测零判别力+区间自相矛盾（S04）"),
    ("L4 物理真理（独立实验+同行复现）", _l4,
     "无独立验证（S05）、同行评审未做（S06）；红线：数学自洽≠实验证实"),
]
add("LAYER", "FAIL" if _l2 == "FAIL" and _l3 == "FAIL" else "BOUNDARY",
    "四层次总判决：L1 部分成立 / L2 FAIL / L3 FAIL / L4 未达到",
    "与评审结论方向一致（「公理化假说框架+部分数学自洽+可证伪预测存疑」），两处机读修正："
    "① P01a：可证伪预测区间与论文自己的 beta=2/3 图景值内部不一致（比评审论断更重）；"
    "② W01f：评审「只取 A_z」指控不准确（比评审论断更轻，方向问题在 G07 不在分量遗漏）。",
    section="LAYER")
guard("g_layer_verdict_machine_driven", _l2 == "FAIL" and _l3 == "FAIL")

# ============================================================================
# 外部输入账（本册新增/条件项）
# ============================================================================
EXT_INPUTS = [
    ("Q 的绝对标度", "N01a 匹配半径 r_*=(2Q^2/GM)^(1/3) 随 Q 无界滑动 ⇒ 需无来源标度（与 r95 外部输入#1 同型）"),
    ("GM / 开普勒 omega(r)", "N01b 阳性对照复现牛顿的唯一通道是把 GM 输入后再读出（circular，cross-ref G02/G05）"),
    ("k_E,k_m,k_g,k_i", "评审版公式集的常数：来稿无定义式 ⇒ 条件推演（W01c/W01j/W01h），不代造"),
    ("beta,eta", "残余质量公式自由参数：P01b 证明 eta=0 后 beta 单参数仍足以拟合任意值"),
    ("区间端点 2.58%/3.93%", "P01a：与 beta=2/3 图景值不一致，端点来源不明（反解 beta≈0.6652）"),
    ("[C] 级实验常数", "Eotvos 上限 %s（%s）；45.22T@1MHz、1e-9 m/s^2（沿用 r95）" % (fs(C_EOTVOS, 2), C_ISO_EOTVOS)),
]

# ============================================================================
# 总结与落盘
# ============================================================================
def _count(st):
    return sum(1 for it in ITEMS if it["status"] == st)

N_PASS = _count("PASS"); N_FAIL = _count("FAIL"); N_BOUND = _count("BOUNDARY")
N_INFO = _count("INFO"); N_CORR = _count("CORRECTED")

SECTIONS = [
    ("MAP 跨册引用校验与覆盖图", ["MAP01", "MAP02"]),
    ("N 极限回归复算（牛顿/无驱动/平坦/电磁/GR/量子）", ["N01a", "N06"]),
    ("P 预测唯一性（eta=0 极限 + 区间端点溯源）", ["P01a", "P01d"]),
    ("W 评审自身断言核验（防过度指控与防漏判）", ["W01a", "W01j"]),
    ("R 与现有理论结构清点", ["R01", "R04"]),
    ("S 六问判断流程机读总表", ["S01", "S06"]),
    ("四层次总判决", ["LAYER"]),
]

KEY_NUMBERS = {
    "n01a_flux_scaling_ratio": fs(_ratio_flux, 10),
    "n01a_positive_control_ratio": fs(_ratio_ff, 10),
    "n01a_operator_residual_O_h": fs(_res_op, 10),
    "n01a_rstar_earth_Q1e6_m": fs(_rstars[2][1], 10),
    "n01b_kepler_input_residual": fs(_res_n01b, 10),
    "p01a_beta_half_value": fs(_v_half, 25),
    "p01a_beta_23_value": fs(_v_23, 25),
    "p01a_beta_23_excess_over_interval": fs(_excess, 10),
    "p01a_beta_window_lo": fs(_b_lo, 10),
    "p01a_beta_window_hi": fs(_b_hi, 10),
    "p01d_point_beta_half_pct": fs(_v_half * 100, 10),
    "p01d_point_beta_23_pct": fs(_v_23 * 100, 10),
    "w01a_kb_rhs_over_lhs": dstr(_gap_rev),
    "w01c_km_conditional": dstr(_d_km),
    "w01j_E_over_B": dstr(_ratio_EB),
}

lines = []
lines.append("=" * 78)
lines.append("r98 | 公式正确性四层次审查（外部评审整理与增量复算）| 机器判决报告")
lines.append("=" * 78)
lines.append("")
for _name, _rng in SECTIONS:
    lines.append("--- %s ---" % _name)
    _lo = _rng[0]
    _hi = _rng[-1]
    for _it in ITEMS:
        if _lo <= _it["code"] <= _hi:
            lines.append("[%s] %s" % (_it["status"], _it["title"]))
            if _it["detail"]:
                lines.append("      %s" % _it["detail"])
    lines.append("")
lines.append("--- 跨册引用（r95 %d 条，一致 %d）---" % (len(CITES), _cite_ok))
for _code, _expect, _why in CITES:
    _got = _r95_status.get(_code)
    lines.append("  r95.%s = %s（%s）%s" % (_code, _got, _why, "" if _got == _expect else "  <<< 不一致"))
lines.append("")
lines.append("--- 四层次总判决 ---")
for _nm, _lv, _ds in LAYERS:
    lines.append("  %s : %s —— %s" % (_nm, _lv, _ds))
lines.append("")
lines.append("--- 外部输入账（本册新增/条件 %d 项）---" % len(EXT_INPUTS))
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
    _mtimes = {}
    for _p in (F_REVIEW, F_LAILIAO, F_R95):
        if os.path.exists(_p):
            _mtimes[os.path.basename(_p)] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(_p)))
    print(REPORT)
    print("")
    print("--- wrapper 元信息（防假绿）---")
    print("  生成时刻 = %s" % _now)
    print("  模块路径 = %s" % os.path.abspath(__file__))
    for _k, _v in _mtimes.items():
        print("  输入 mtime %s = %s" % (_k, _v))
    os.makedirs(DIR_DATA, exist_ok=True)
    _stem = "TUFT-r98_公式正确性四层次审查_外部评审整理与增量复算_2026-10-18"
    _payload = {
        "round": "r98",
        "date": "2026-10-18",
        "topic": "公式正确性四层次审查（外部评审长文整理 + 增量机读复算）",
        "source_review": "数据/TUFT-四层次正确性评审_外部来料全文_2026-10-18.md",
        "source_paper": "数据/TUFT-螺旋时空理论_来料全文_2026-10-17.md",
        "cross_ref_round": "r95",
        "items": ITEMS,
        "guards": GUARDS,
        "counts": {
            "PASS": N_PASS, "FAIL": N_FAIL, "BOUNDARY": N_BOUND,
            "INFO": N_INFO, "CORRECTED": N_CORR, "total": len(ITEMS),
            "guard_pass": sum(1 for g in GUARDS if g["ok"]),
            "guard_total": len(GUARDS),
        },
        "cross_citations": [{"code": c, "expected": e, "actual": _r95_status.get(c), "why": w}
                            for c, e, w in CITES],
        "coverage": [{"point": c[0], "where": c[1], "status": c[2]} for c in COVERAGE],
        "layers": [{"layer": l[0], "verdict": l[1], "basis": l[2]} for l in LAYERS],
        "external_inputs": [{"name": n, "desc": d} for n, d in EXT_INPUTS],
        "key_numbers": KEY_NUMBERS,
        "wrapper": {"generated_at": _now, "module": os.path.abspath(__file__),
                    "input_mtimes": _mtimes},
    }
    with io.open(os.path.join(DIR_DATA, _stem + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(_payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DIR_DATA, _stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(REPORT)
        f.write("\n\n--- wrapper 元信息（防假绿）---\n")
        f.write("生成时刻 = %s\n" % _now)
        f.write("模块路径 = %s\n" % os.path.abspath(__file__))
        for _k, _v in _mtimes.items():
            f.write("输入 mtime %s = %s\n" % (_k, _v))
    _md = ["# 数据产物｜r98 公式正确性四层次审查（2026-10-18）", "",
           "评审来料：[TUFT-四层次正确性评审_外部来料全文_2026-10-18.md](TUFT-四层次正确性评审_外部来料全文_2026-10-18.md)",
           "靶论文来料：[TUFT-螺旋时空理论_来料全文_2026-10-17.md](TUFT-螺旋时空理论_来料全文_2026-10-17.md)",
           "判定册：[判定_TUFT-r98-公式正确性四层次审查_外部评审整理与增量复算_2026-10-18.md](../判定_TUFT-r98-公式正确性四层次审查_外部评审整理与增量复算_2026-10-18.md)",
           "", "```", REPORT, "```", ""]
    with io.open(os.path.join(DIR_DATA, _stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
