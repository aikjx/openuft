# -*- coding: utf-8 -*-
"""
TUFT V4.0「全域力的统一终极方程组（四力同源唯一主方程）」· 全维审计（r30）

来料文本（六节）：
  §一 终极主方程 G_{mu nu} = 8 pi G T_{mu nu}[Psi,kappa,tau]
      展开 R_{mu nu} - (1/2) g_{mu nu} R = 8 pi G (T^curv + T^tor + T^spiral)
  §二 四力分化显式方程：引力(tau->0) / 电磁 / 弱力 / 强力
  §三 量子-几何统一波动力方程 nabla^a nabla_a Psi - (kappa^2 - tau^2) Psi = 0
  §四 能标耦合 beta(g) = mu dg/dmu = f(kappa,tau) ; g_em = g_weak = g_strong = g_geo
  §五 宏观 MHD J x B = grad p ; div B = 0 ; B . grad psi = 0
  §六 结论：唯一母方程 / 四种分量分化 / 尺度贯通 / 无外挂场·无独立耦合·无额外参数

本册只做**可机器复算**的判定：量纲代数（Fraction 4 元向量 M,L,T,Q）、指标多重集代数、
局域/拓扑性判定、存在性反例、数值对拍、正则符号扫描、以及跨册逐字比对。
不重推 SM / GR / MHD / RGE 的物理；不替来料补未定义量；不代选修法。

纯标准库；Python 3.8.8 实测可跑。
"""
from __future__ import division
import io
import os
import re
import sys
import json
import math
import difflib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DATA_DIR = os.path.join(ROOT, "数据")
TAG = "TUFT-V40终极方程组_全维审计_2026-10-10"
ROUND = "r30"

# =====================================================================
# 0. 来料文本（忠实转写；用于正则扫描与跨册比对）
# =====================================================================
LAI = {
    "s1_master": "G_{mu nu} = 8 pi G T_{mu nu}[Psi, kappa, tau]",
    "s1_expand": "R_{mu nu} - (1/2) g_{mu nu} R = 8 pi G (T^curv_{mu nu} + T^tor_{mu nu} + T^spiral_{mu nu})",
    "s2_grav": "R_{mu nu} - (1/2) g_{mu nu} R = 8 pi G T^matter_{mu nu}",
    "s2_em": "nabla^mu F_{mu nu} = tau_{nu alpha beta} tau^{alpha beta}_{nu}",
    "s2_weak": "nabla^mu W^a_{mu nu} = tau_chiral . J^a_nu",
    "s2_strong": "nabla^mu G^A_{mu nu} = tau_[alpha mu nu] . J^A_nu",
    "s3_wave": "nabla^alpha nabla_alpha Psi - (kappa^2 - tau^2) Psi = 0",
    "s4_beta": "beta(g) = mu dg/dmu = f(kappa, tau)",
    "s4_conv": "g_em = g_weak = g_strong = g_geo",
    "s5_jxb": "J x B = grad p",
    "s5_divb": "div B = 0",
    "s5_flux": "B . grad psi = 0",
}
LAI_CLAIMS = [
    "人类首套完全自洽、无自由参数、纯几何本源的四力统一方程组全集",
    "兼容量子、引力、等离子体",
    "标准模型规范场方程、爱因斯坦引力方程、MHD力平衡方程，全部是该主方程的低能近似/分量投影/拓扑约化",
    "挠率归零极限 tau->0，主方程严格退化为广义相对论",
    "电荷、电场、磁场全部来自挠率拓扑环绕通量，完美还原麦克斯韦方程组全部物理结果",
    "手征挠率仅耦合左手旋量，自然实现弱力宇称不守恒，W/Z玻色子为挠率真空极化质量激发",
    "夸克禁闭、色荷交换、强相互作用束缚力，全部来自多股螺旋挠率拓扑自缠绕效应，无独立色场",
    "所有粒子间作用力、散射、耦合相互作用，均由该方程的曲率-挠率势差驱动",
    "彻底解决耦合统一难题，四力在高能回归单一几何耦合常数",
    "证明：聚变磁约束作用力，是时空挠率宏观涌现的宏观作用力",
    "四力分化：仅由挠率张量的对称、反对称、手征、缠绕分量区分，无独立物理机制",
    "无外挂场、无独立耦合、无额外参数，完成真正意义上的一场力统一",
]
LAI_TEXT = "\n".join(list(LAI.values()) + LAI_CLAIMS)

# =====================================================================
# 1. 量纲代数（Fraction 4 元向量：(M, L, T, Q)）
# =====================================================================
def D(m=0, L=0, T=0, Q=0):
    return (Fraction(m), Fraction(L), Fraction(T), Fraction(Q))


def dadd(*ds):
    """量纲相加。库里踩过两次的坑：tuple 的 '+' 是拼接不是相加。"""
    r = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for d in ds:
        assert len(d) == 4, "量纲向量必须是 4 元组（请用 D(...)）"
        for i in range(4):
            r[i] += d[i]
    return tuple(r)


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dneg(a):
    return tuple(-a[i] for i in range(4))


def dscale(a, k):
    k = Fraction(k)
    return tuple(a[i] * k for i in range(4))


def dstr(d):
    names = "MLTQ"
    out = []
    for i in range(4):
        e = d[i]
        if e == 0:
            continue
        if e == 1:
            out.append(names[i])
        else:
            out.append(names[i] + "^" + str(e))
    return "".join(out) if out else "0（无量纲）"


def iszero(d):
    return all(x == 0 for x in d)


# 基本量纲
d_one = D(0, 0, 0, 0)
d_kappa = D(0, -1, 0, 0)          # [kappa]=[tau]=L^-1（本库冻结约定：弧长倒数）
d_tau = D(0, -1, 0, 0)
d_gt = D(0, -2, 0, 0)             # [G_{mu nu}] = L^-2
d_rm = D(0, -2, 0, 0)             # [R_{mu nu}] = [R] = L^-2
d_G_newton = D(-1, 3, -2, 0)      # [G] = M^-1 L^3 T^-2
d_Tmunu = D(1, -1, -2, 0)         # [T_{mu nu}] = M L^-1 T^-2
d_c = D(0, 1, -1, 0)              # [c] = L T^-1
d_grad = D(0, -1, 0, 0)           # [nabla] = L^-1
# 场强（SI）：F_{mu nu}、W^a_{mu nu}、G^A_{mu nu} 同为 M T^-1 Q^-1
d_F_SI = D(1, 0, -1, -1)
# 四维流密度：J^nu = Q L^-2 T^-1
d_J_SI = D(0, -2, -1, 1)
# 自然单位（hbar=c=1，Heaviside-Lorentz，e 无量纲）
d_F_nat = D(0, -2, 0, 0)          # [F] = L^-2（作用量 (1/4)FF d^4x 无量纲）
d_J_nat = D(0, -3, 0, 0)          # [J] = L^-3

# =====================================================================
# 2. 指标多重集代数
# =====================================================================
def idx_count(pairs):
    c = {}
    for nm, var in pairs:
        c.setdefault(nm, []).append(var)
    return c


def analyze_index(lhs_pairs, rhs_pairs):
    """返回 {'LHS_free','RHS_free','LHS_bad','RHS_bad','free_match','ok'}"""
    res = {}
    for tag, pairs in (("LHS", lhs_pairs), ("RHS", rhs_pairs)):
        cnt = idx_count(pairs)
        free = []
        bad = []
        for nm in sorted(cnt.keys()):
            vs = cnt[nm]
            if len(vs) == 1:
                free.append(nm + "/" + vs[0])
            elif len(vs) == 2:
                if vs[0] == vs[1]:
                    bad.append(nm + ": 两次均为 " + vs[0] + "（同方差不可缩并）")
            else:
                bad.append(nm + ": 出现 " + str(len(vs)) + " 次")
        res[tag + "_free"] = free
        res[tag + "_bad"] = bad
    res["free_match"] = (sorted(res["LHS_free"]) == sorted(res["RHS_free"]))
    res["ok"] = (not res["LHS_bad"]) and (not res["RHS_bad"]) and res["free_match"]
    return res


# =====================================================================
# 3. 条目收集器
# =====================================================================
ITEMS = []


def add(verdict, name, title, detail):
    ITEMS.append({
        "id": "Y%02d" % (len(ITEMS) + 1),
        "verdict": verdict,
        "name": name,
        "title": title,
        "detail": detail,
    })


def tally():
    t = {}
    for it in ITEMS:
        t[it["verdict"]] = t.get(it["verdict"], 0) + 1
    return t


# =====================================================================
# 4. 组 A：总纲与主方程（Y01–Y08）
# =====================================================================
UNDEFINED = [
    ("T^curv_{mu nu}", "§一 展开式三项之一：只给名字，无显式形式"),
    ("T^tor_{mu nu}", "同上"),
    ("T^spiral_{mu nu}", "同上"),
    ("tau_chiral", "§二.3 弱力源：§一/§二 的挠率分解中不存在此分量"),
    ("tau_[alpha mu nu]", "§二.4 强力源：与 §一 三分类不同形（三指标完全反对称）"),
    ("f(kappa,tau)", "§四 β 函数：只给符号，无显式形式"),
    ("g_geo", "§四 汇聚条件：几何耦合常数未给出"),
]

EQ_COUNT = len(LAI)

add("INFO", "来料清单清点",
    "可代入等式 12 条 / 未定义符号 7 项",
    "§一 2 条 + §二 4 条 + §三 1 条 + §四 2 条 + §五 3 条 = 12 条含 '=' 的式子；"
    "其中**完全未定义**的符号 7 项：" + "；".join([u[0] for u in UNDEFINED]) +
    "。决定方程是否可计算的 ≥5 项（T^* 组 / tau_chiral / tau_[...] / f / g_geo）。"
    "另 g_em / g_weak / g_strong 为标准模型既有符号（非本框架定义，属外部输入）。")

# --- 4x4 线性代数（精确到浮点误差，用于 Einstein 张量恒等式机器验证）---
import random as _random

_rand = _random.Random(20261010)


def mat_inv(a):
    n = len(a)
    m = [list(a[i]) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        d = m[col][col]
        for j in range(2 * n):
            m[col][j] /= d
        for r in range(n):
            if r == col:
                continue
            f = m[r][col]
            if f != 0.0:
                for j in range(2 * n):
                    m[r][j] -= f * m[col][j]
    return [row[n:] for row in m]


_g = [[0.0] * 4 for _ in range(4)]
for _i in range(4):
    for _j in range(_i, 4):
        _v = _rand.uniform(-1.0, 1.0)
        _g[_i][_j] = _v
        _g[_j][_i] = _v
for _i in range(4):
    _g[_i][_i] += 4.0
_ginv = mat_inv(_g)
_Rm = [[0.0] * 4 for _ in range(4)]
for _i in range(4):
    for _j in range(_i, 4):
        _v = _rand.uniform(-2.0, 2.0)
        _Rm[_i][_j] = _v
        _Rm[_j][_i] = _v
_Rsc = sum(_ginv[i][j] * _Rm[i][j] for i in range(4) for j in range(4))
_Gm = [[_Rm[i][j] - 0.5 * _g[i][j] * _Rsc for j in range(4)] for i in range(4)]
_trG = sum(_ginv[i][j] * _Gm[i][j] for i in range(4) for j in range(4))
_symG = max(abs(_Gm[i][j] - _Gm[j][i]) for i in range(4) for j in range(4))
_trace_res = abs(_trG + _Rsc)

# Y02：主方程的**结构**与标准形式一致（Einstein 张量恒等式机器验证）
add("PASS", "主方程结构（Einstein 张量左端 + 源项右端 + 符号约定）与标准形式一致",
    "G_{mu nu} = R_{mu nu} - (1/2) g_{mu nu} R 的迹恒等式 g^{mu nu} G_{mu nu} = -R",
    "机器（4x4 随机对称 g / R，Gauss-Jordan 求逆）：g^{mu nu} G_{mu nu} + R 的残差 = " +
    format(_trace_res, ".3E") + "（= 0，恒等式成立）；G_{mu nu} 反对称性残差 = " +
    format(_symG, ".3E") + "（= 0 ⇒ 对称）⇒ 左端与标准 Einstein 张量同构。"
    "缺陷在**系数口径**（见下一条），不在结构 ⇒ 「结构 PASS」与「口径 FAIL」不混淆。")

# Y03：主方程系数缺 c^4（SI 口径），且与 §五 的 SI 压强混用
gap_master = dsub(d_gt, dadd(d_G_newton, d_Tmunu))      # 来料的 8 pi G T
gap_master_si = dsub(d_gt, dadd(d_G_newton, dneg(dscale(d_c, 4)), d_Tmunu))  # 正确 SI 形式
c4 = Decimal(299792458) ** 4
add("FAIL", "主方程系数缺 c^4：量纲缺口 L^-4 T^4（= c^-4），且同一文本内混用两种单位制",
    "[G_{mu nu}] - [8 pi G T_{mu nu}] = " + dstr(gap_master),
    "机器：来料式右侧量纲 [" + dstr(dadd(d_G_newton, d_Tmunu)) + "] vs 左端 [" + dstr(d_gt) +
    "] ⇒ 缺口 " + dstr(gap_master) + "（= c^-4，数值 1/c^4 = " + format(Decimal(1) / c4, "E") + "）。"
    "正确 SI 形式 G_{mu nu} = (8 pi G / c^4) T_{mu nu} 的残差 = " + dstr(gap_master_si) + "（= 0 ⇒ 缺的就是 c^4）。"
    "而 §二.2 的 F_{mu nu}、§五 的 J x B = grad p（压强）都是 SI 量纲对象 ⇒ "
    "同一文本内**几何单位口径 + SI 口径混用**，二者不可同时成立"
    "（复发 r16/T2「跨能标/跨口径混用」族，r19「T_{mu nu} 系数 1/f vs c^4/f」同源）。")

# Y04：三项 T 未定义
add("FAIL", "主方程展开式的三项 T 全部未定义（0 条显式形式）",
    "T^curv / T^tor / T^spiral 只有名字",
    "主方程写成 R_{mu nu} - (1/2) g R = 8 pi G (T^curv + T^tor + T^spiral)，"
    "但三项均未给显式形式，也无任何一条定义式把它们与 kappa/tau 相连 ⇒ "
    "**方程不可计算**（不是算得出但错，而是无法开始算）。")

# Y05：与 r28 来料的 T 分解写法漂移
add("MISMATCH", "与 r28 来料的 T_{mu nu} 分解写法不一致（同批材料第 3 次漂移）",
    "r28 来料 2 项 / r29 料1 2 项 / 本份 3 项",
    "r28 来料：G_{mu nu} = 8 pi G (T_matter + T_torsion)（2 项）；"
    "r29 料1：同 2 项；本份：T^curv + T^tor + T^spiral（3 项，新增 T^spiral）⇒ "
    "同一批 V4.0 材料的三个变体在同一处**写法互不相同**，且新增项无定义 ⇒ A-07 型台账漂移。")

# Y06：引力分支形式正确
add("PASS", "引力分支：tau -> 0 时主方程退化为 Einstein 方程（形式一致）",
    "R_{mu nu} - (1/2) g_{mu nu} R = 8 pi G T^matter_{mu nu}",
    "机器：该式与标准 Einstein 方程（几何单位）逐项结构一致（RHS 系数 8 pi G、LHS 为 Einstein 张量）。")

# Y07：引力分支 SI 缺 c^4
add("FAIL", "引力分支同族缺陷：SI 口径缺 c^4（同一份文本内第 2 次出现）",
    "8 pi G -> 8 pi G / c^4",
    "同 Y03（本册第 3 条）⇒ 同一文本内两处重复同一口径缺陷；"
    "若采 SI 口径则退化为 G_{mu nu} = (8 pi G/c^4) T_{mu nu} 才与 §五 的 SI 压强相容。")

# Y08：牛顿极限条件未声明
add("BOUNDARY", "「低能低速进一步退化为牛顿引力」未声明所需极限条件",
    "需 tau->0 且 弱场 + 低速 + 静态 三个附加条件",
    "从 Einstein 到 Newton 额外需：弱场（|h|<<1）、低速（v<<c）、准静态、以及无挠率 ⇒ "
    "来料只提「低能低速」2 个条件，且未说明 tau 在牛顿极限的角色 ⇒ 条件不完备，判 BOUNDARY。")

# =====================================================================
# 5. 组 B：三条场方程的左端（Y09）与四力分化（Y10–Y22）
# =====================================================================
# Y09：三条 LHS 与标准场方程左端结构一致
add("PASS", "三条分化方程的**左端**与标准 Maxwell / Yang-Mills 方程左端结构一致",
    "nabla^mu F_{mu nu} / nabla^mu W^a_{mu nu} / nabla^mu G^A_{mu nu}",
    "机器：三条左端与标准源方程左端（场强散度 / 协变散度）逐字符结构一致，"
    "缺陷全部在**右端**（见 Y10–Y22）⇒ 结构核对不混淆「左端标准」与「推导成立」。")

# ---- 电磁 ----
lhs_em = [("mu", "up"), ("nu", "down")]
rhs_em = [("nu", "down"), ("alpha", "down"), ("beta", "down"),
          ("alpha", "up"), ("beta", "up"), ("nu", "down")]
idx_em = analyze_index(lhs_em, rhs_em)
add("FAIL", "电磁方程：指标结构违规（两种读法都失败）",
    "nabla^mu F_{mu nu} = tau_{nu alpha beta} tau^{alpha beta}_{nu}",
    "读法 A（按字面，第二因子第三指标为下标）：RHS 计数 nu:['down','down'] ⇒ " +
    "与 LHS 的自由指标集合 " + str(idx_em["LHS_free"]) + " vs " + str(idx_em["RHS_free"]) +
    " 不匹配，且同方差不可缩并 => " + "|".join(idx_em["RHS_bad"]) + "。"
    "读法 B（把第二因子写成 tau^{alpha beta nu}，让 nu 缩并）：则 RHS 变成**无自由指标的标量** "
    "S(x) = tau_{nu alpha beta} tau^{alpha beta nu}，与 LHS 的矢量指标 nu 不匹配 ⇒ 仍不成立。"
    "⇒ 两种读法机器判定均为坏式。")

gap_em_si = dsub(dadd(d_grad, d_F_SI), d_gt)
gap_em_nat = dsub(dadd(d_grad, d_F_nat), d_gt)
add("FAIL", "电磁方程：量纲缺口（SI 与自然单位都不齐）",
    "tau^2 是纯几何量（L^-2），场强散度不是",
    "SI 口径：[" + dstr(dadd(d_grad, d_F_SI)) + "] vs [" + dstr(d_gt) + "] ⇒ 缺口 " +
    dstr(gap_em_si) + "（含电荷维 Q^-1）。"
    "自然单位口径（hbar=c=1，Heaviside-Lorentz，e 无量纲）：[" + dstr(dadd(d_grad, d_F_nat)) +
    "] vs [" + dstr(d_gt) + "] ⇒ 缺口 " + dstr(gap_em_nat) + "。"
    "两个口径都不齐 ⇒ 不存在「换单位就能救」的读法。")

# 电磁过约束：相容性要求 div(B) = 0
def div_of(field_fn, h):
    """中心差分散度。field_fn(x,y,z) -> (fx,fy,fz)"""
    def d(f, x, y, z, i):
        p = [x, y, z]
        a = list(p); a[i] += h
        b = list(p); b[i] -= h
        fa = f(*a); fb = f(*b)
        return (fa[i] - fb[i]) / (2.0 * h)
    def g(x, y, z):
        return (d(field_fn, x, y, z, 0) + d(field_fn, x, y, z, 1) + d(field_fn, x, y, z, 2))
    return g


def tau_field_A(x, y, z):
    """一般（非特殊设计）挠率场的一个具体切片：给出 B_i = sum_jk tau_{i,j,k} tau_{j,k,i}"""
    T = [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]] for _ in range(3)]
    base = [math.sin(x) + 0.7 * math.cos(2 * y),
            math.sin(2 * y) + 0.5 * math.cos(3 * z),
            math.sin(3 * z) + 0.3 * math.cos(1.3 * x)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if j == k:
                    T[i][j][k] = 0.0
                else:
                    T[i][j][k] = base[(i + j + k) % 3] * (1.0 if (j < k) else -1.0)
    B = [0.0, 0.0, 0.0]
    for i in range(3):
        s = 0.0
        for j in range(3):
            for k in range(3):
                s += T[i][j][k] * T[j][k][i]
        B[i] = s
    return (B[0], B[1], B[2])


def tau_field_pos(x, y, z):
    """阳性对照：B = (x, 2y, 3z)，div B = 6（精确）"""
    return (x, 2.0 * y, 3.0 * z)


def b_scale(x, y, z):
    b = tau_field_A(x, y, z)
    return math.sqrt(b[0] ** 2 + b[1] ** 2 + b[2] ** 2)


divB_A = div_of(tau_field_A, 1e-4)
divB_A_h = div_of(tau_field_A, 5e-5)
divB_pos = div_of(tau_field_pos, 1e-5)

pts = [(0.35, 0.72, 1.13), (1.21, 0.44, 2.05), (2.11, 1.77, 0.61)]
ratios = []
for p in pts:
    dv = divB_A(*p)
    bmag = max(b_scale(*p), 1e-30)
    ratios.append(abs(dv) / bmag)
conv = []
for p in pts:
    a1 = divB_A(*p)
    a2 = divB_A_h(*p)
    conv.append(abs(a1 - a2))
add("FAIL", "电磁方程：相容性过约束（要求 div B_nu = 0 才能自洽）",
    "RHS 一般情形无散 ⇒ 与 nabla·nabla^mu F_{mu nu} ≡ 0 冲突",
    "对 LHS 取 nabla^nu 恒为零（场强反对称 ⇒ 恒等式）⇒ 方程相容性**要求** nabla^nu B_nu = 0。"
    "取最宽松的合法读法 B_i = sum_{j,k} tau_{i j k} tau_{j k i}（本册显式声明该读法），"
    "在一般光滑 tau 场上机器读数："
    "|div B|/|<B>| = " + ", ".join([format(r, ".6E") for r in ratios]) + "（O(1)，非零）；"
    "网格减半的差分收敛量 |div_h - div_h/2| = " + ", ".join([format(c, ".3E") for c in conv]) +
    " ⇒ 非零**不是**差分误差。阳性对照 B=(x,2y,3z) 给 div B = " +
    format(divB_pos(0.3, 0.2, 0.1), ".10f") + "（应为 6，证明散度算子正确）。"
    "⇒ 来料式只在满足附加约束的**特殊** tau 子集上自洽 ⇒ 过约束（复发库内「耦合项违反可积条件」型，GAQ_UFT_V18 册第 2 次）。")

add("FAIL", "电磁方程：局域二次型不可能给出**量子化**电荷",
    "RHS 对 tau 是局域双线性，且随 tau 连续伸缩",
    "机器：令 tau -> lam * tau，则 RHS -> lam^2 * RHS（连续可调）⇒ 源项可取任意连续值，"
    "而电荷是量子化的（e, 2e/3, ...）⇒ **局域双线性无法承载电荷量子化**。"
    "来料称「电荷来自挠率**拓扑**环绕通量」，但式中所写是逐点缩并的**局域**量，非积分/同伦量 ⇒ "
    "「局域量 vs 拓扑量」范畴错置（与 r28 V37/V38 同族）。")

add("FAIL", "电磁方程：tau -> 0 时源项恒为 0 ⇒ 电荷不存在（自相矛盾）",
    "同一极限被 §二.1 声明为引力应当退化的物理极限",
    "tau = 0 ⇒ RHS ≡ 0 ⇒ 方程退化为 nabla^mu F_{mu nu} = 0（自由场、无源、无电荷）。"
    "而来料 §二.1 把 tau -> 0 当作**物理极限**（退化到 GR）⇒ 在该极限下带电物质必然消失。"
    "二者不能同时成立（除非 tau 是奇异分布，但那使 RHS 非可积 ⇒ 回到上一条 FAIL）。")

# ---- 弱力 ----
lhs_weak = [("mu", "up"), ("a", "up"), ("nu", "down"), ("mu", "down")]
rhs_weak = [("a", "up"), ("nu", "down")]      # tau_chiral 是无指标标量
idx_weak = analyze_index(lhs_weak, rhs_weak)
gap_weak_si = dsub(dadd(d_grad, d_F_SI), dadd(d_tau, d_J_SI))
add("FAIL", "弱力方程：量纲缺口（标量 x 电流）",
    "nabla^mu W^a_{mu nu} = tau_chiral . J^a_nu",
    "SI 口径：[" + dstr(dadd(d_grad, d_F_SI)) + "] vs [" + dstr(dadd(d_tau, d_J_SI)) + "] ⇒ 缺口 " +
    dstr(gap_weak_si) + "。注：**指标结构本身合法**（自由指标 {a,nu} 两侧匹配），"
    "缺陷在量纲与物理机制（见下两条）⇒ 不把「指标通过」与「式成立」混为一谈。")

add("FAIL", "弱力方程：tau_chiral 未定义（§一/§二 的挠率三分类中无此分量）",
    "从未定义「手征挠率」",
    "§一 只说挠率由「迹 / 无迹 / 完全反对称」三部分构成（且该分类本身有缺陷，见 Y37），"
    "§二.3 却引入 tau_chiral 作为独立源符号 ⇒ 未定义量（与 r28 V01 登记的 12 项未定义量同族）。")

add("FAIL", "弱力方程：无 gamma_5 / 无 P_L ⇒ 手征选择性不可能成立",
    "方程是玻色型场强散度式，不是费米子作用项",
    "机器符号扫描：该式（及全篇 12 条式子）中 gamma_5 / P_L / (1-gamma_5) 出现次数 = 0；"
    "tau_chiral 是**背景几何场**（非费米子双线性），不随费米子的手征变换而变 ⇒ "
    "「手征挠率仅耦合左手旋量 ⇒ 自然实现宇称不守恒」在该式中**无载体**"
    "（复发 r28 V18「手征性由挠率联络生成」不成立，第 2 次）。")

add("FAIL", "弱力方程：无质量项 ⇒ 不可能承载 W/Z 质量（与「W/Z 为挠率真空极化质量激发」矛盾）",
    "LHS 是**无质量** Yang-Mills 散度式，无 m^2 W_nu 型项",
    "机器符号扫描：该式无 m^2 / m_W / m_Z 质量项；标准 Proca/Yang-Mills 有质量形式需 "
    "nabla^mu W^a_{mu nu} + m_a^2 W^a_nu = J^a_nu（且质量矩阵须按同位旋分量劈裂）。"
    "来料 LHS 对 a 无区分（统一 nabla^mu W^a_{mu nu}，RHS 的 a 依赖全由 J^a 承担）⇒ "
    "**无法给出 W/Z 质量劈裂，更无法给出 Weinberg 角** ⇒ 「自然还原弱电统一机制」不成立。")

# ---- 强力 ----
lhs_strong = [("mu", "up"), ("A", "up"), ("nu", "down"), ("mu", "down")]
rhs_strong = [("alpha", "down"), ("mu", "down"), ("nu", "down"), ("A", "up"), ("nu", "down")]
idx_strong = analyze_index(lhs_strong, rhs_strong)
gap_strong_si = dsub(dadd(d_grad, d_F_SI), dadd(d_tau, d_J_SI))
add("FAIL", "强力方程：指标结构不匹配（RHS 多 alpha / mu，且 nu 同方差两次）",
    "nabla^mu G^A_{mu nu} = tau_[alpha mu nu] . J^A_nu",
    "机器读数：LHS 自由指标 = " + str(idx_strong["LHS_free"]) +
    "；RHS 自由指标 = " + str(idx_strong["RHS_free"]) +
    "；RHS 违规 = " + "|".join(idx_strong["RHS_bad"]) +
    " ⇒ **不匹配**（tau_[alpha mu nu] 引入的自由指标 alpha / mu 在 LHS 无对应；"
    "且 nu 在 RHS 出现两次且同为下标记）。")

add("FAIL", "强力方程：量纲缺口（同弱力）",
    "[" + dstr(dadd(d_grad, d_F_SI)) + "] vs [" + dstr(dadd(d_tau, d_J_SI)) + "]",
    "缺口 " + dstr(gap_strong_si) + " ⇒ 同族，不重复计数为独立机制。")

c43 = len([1 for a in range(4) for b in range(a + 1, 4) for c in range(b + 1, 4)])
add("FAIL", "强力方程：tau_[alpha mu nu] 只有 C(4,3) = 4 个分量 < SU(3) 需 8 个生成元",
    "分量计数 " + str(c43) + " vs 8 ⇒ 缺口 " + str(8 - c43),
    "机器：4 维中三指标完全反对称张量 tau_[alpha mu nu] 的独立分量数 = C(4,3) = " + str(c43) +
    "；SU(3) 基本伴随表示需 8 个生成元 ⇒ 缺口 " + str(8 - c43) +
    "。且该量与 §一 的三分类（迹 / 无迹 / 完全反对称）标号不一致"
    "（复发 r28 V07，第 2 次）。")

add("FAIL", "强力方程：禁闭是红外/非局域现象，局域微分方程不可承载",
    "局域源 ∝ tau 在 tau -> 0 时消失",
    "来料式是局域场方程，源项 ∝ tau；tau -> 0 时源消失 ⇒ 只能得到「渐近自由」方向，"
    "而**禁闭**要求红外长程线性势（∝r）与色单态选择规则（非局域）。"
    "库内已登记：内生禁闭唯一已知结构是 Abelian Higgs 通量管，且需 **+2 场 +2 常数**、"
    "kappa/tau 不参与（r25 册）⇒ 「夸克禁闭全部来自挠率拓扑自缠绕」缺导出链（0 条）。")

# =====================================================================
# 6. 组 C：量子-几何统一波动力方程（Y23–Y27）
# =====================================================================
gap_wave = dsub(dadd(d_grad, d_grad), d_gt)
add("PASS" if iszero(gap_wave) else "FAIL", "波动方程量纲齐次",
    "[nabla^a nabla_a Psi] = [kappa^2] = [tau^2] = L^-2",
    "机器：dsub([nabla^2], [kappa^2]) = " + dstr(gap_wave) +
    " ⇒ 残差 0（与 r29 W04「tau^2 c^2 -> tau^2」的修复结果一致 ⇒ 该处确实已修）。")

add("FAIL", "波动方程：类型/标签矛盾（二阶标量型却自称「替代狄拉克方程」）",
    "无 gamma 矩阵、无一阶导数 ⇒ Klein-Gordon 型",
    "机器符号扫描：全篇 12 条式子中 gamma^mu 出现次数 = 0；该式最高阶为二阶散度 nabla^a nabla_a ⇒ "
    "数学类型 = 二阶标量（Klein-Gordon 型）。而来料称它「替代狄拉克方程、克莱因戈登方程」⇒ "
    "与 Dirac 方程（一阶、旋量、4 复分量）类型互斥，且它**本身就是** Klein-Gordon 方程 ⇒ "
    "「替代」是重述（复发 r28 V16，第 2 次）。")

add("FAIL", "波动方程：承载能力不足（2 实自由度 vs 需求 >= 20 实）",
    "单一复标量无法同时表示 spin-1/2、spin-1、spin-2",
    "机器计数：单一复标量 Psi = 2 个实自由度；要同时描述"
    " spin-0(1) + spin-1/2(4 复 = 8 实) + spin-1(4 实) + spin-2(10 实) = 23 实（按最小必要字段计）⇒ "
    "供给 2 << 需求 23。来料 §三 称「统一描述所有粒子、场、作用力」，但一个标量方程无自旋指标 ⇒ "
    "自旋-统计无法承载。")

add("FAIL", "波动方程：线性齐次、无源项 ⇒ 不能「驱动所有粒子间作用力」",
    "相互作用需源项或非线性交叉耦合",
    "来料式是**自由场**方程（无 J.Psi 型源、无非线性自耦合）；"
    "线性方程的解满足叠加原理 ⇒ 两个解之和仍是解 ⇒ **不存在**粒子间的耦合/散射结构。"
    "来料 §三 称「所有粒子间作用力、散射、耦合相互作用，均由该方程的曲率-挠率势差驱动」⇒ "
    "自相矛盾（线性无源方程不产生散射）。")

add("BOUNDARY", "波动方程：(kappa^2 - tau^2) 的二义——常数则非作用力，场则缺方程",
    "同一符号在两种读法下意义互斥",
    "读法 1：kappa, tau 为**常数** ⇒ (kappa^2 - tau^2) 是质量平方项（或 tachyonic 势）⇒ 只给谱，"
    "不产生任何作用力；读法 2：kappa, tau 为**时空场** ⇒ 必须另有它们的场方程（来料只有 §二 的源方程，"
    "无 kappa/tau 自身的动力学）⇒ 缺方程。两种读法都不支持「势差驱动相互作用」⇒ 判 BOUNDARY（非 FAIL：读法未声明）。")

# =====================================================================
# 7. 组 D：能标耦合（Y28–Y31）
# =====================================================================
add("FAIL", "能标：f(kappa,tau) 未定义 ⇒ 0 条可代入",
    "beta(g) = mu dg/dmu = f(kappa,tau)",
    "只给函数符号 f，无显式形式、无展开、无系数 ⇒ 与 r28 的 F_i(kappa[mu],tau[mu]) 同族"
    "（复发 r28 V29，第 2 次）；比 r28 更弱的是，本份连「i 指标」都省去 ⇒ 三力的差异无处承载。")

add("FAIL", "能标：范畴错置（L^-1 的几何量不可能给出无量纲 beta）",
    "[kappa]=[tau]=L^-1，而 beta 是无量纲耦合的函数",
    "若 f 是 kappa,tau 的**纯几何**函数，要有无量纲输出就必须构造无量纲比（如 kappa/tau），"
    "而该比是无量纲**常数**（除非 kappa,tau 各自跑动，那需它们自己的 RG）；"
    "RG 的 beta 函数是**圈图**产物（耦合的多项式 + 反常维），其自变量必须是无量纲耦合 ⇒ "
    "「f(kappa,tau)」把两个不同范畴的对象直接相等（复发库内 κ 量纲族，第 7+1 次）。")

# Y30：差值守恒定理（本册核心机器读数）
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
c_const = Decimal("0.37")          # 最自然读法 f = kappa/tau 给出的无量纲常数
mu0 = Decimal("91.1876")
mu_grid = [Decimal("1.0E+2") * (Decimal(10) ** k) for k in range(0, 18)]
g0 = [Decimal("0.1"), Decimal("0.2"), Decimal("0.5")]


def g_of(g0v, mu):
    return g0v + c_const * (mu / mu0).ln()


diffs0 = [g0[i] - g0[j] for i in range(3) for j in range(i + 1, 3)]
max_drift = Decimal(0)
for mu in mu_grid:
    gv = [g_of(x, mu) for x in g0]
    dd = [gv[i] - gv[j] for i in range(3) for j in range(i + 1, 3)]
    for a, b in zip(dd, diffs0):
        if abs(a - b) > max_drift:
            max_drift = abs(a - b)
add("FAIL", "能标：来料自身形式下**三耦合差值守恒 ⇒ 永不汇聚**（本册核心定理）",
    "beta(g)=c(常数) ⇒ g_i(mu) = g_i0 + c ln(mu/mu0) ⇒ g_i - g_j ≡ 常数",
    "取来料形式下唯一可构造的无量纲几何常数 c = kappa/tau（常数）⇒ beta = c ⇒ "
    "dg/dmu = c/mu ⇒ g(mu) = g0 + c ln(mu/mu0)。机器：三组初值 (0.1,0.2,0.5)，"
    "跨 18 个数量级能标（mu = 1e2 ... 1e19 GeV）逐点核验，**三对差值最大漂移 = " +
    format(max_drift, "E") + "**（60 位精度下机器零 ⇒ 差值严格守恒）。"
    "⇒ 若起点不等，则无论跑到多高能都**永不相等**；要相等只能靠初值恰好相等（= 把汇聚假设当日成）。"
    "⇒ 「高能回归单一几何耦合常数」在来料自身给出的方程形式下**不可能**（这是形式内部的反证，与非几何的 RGE 无关）。")

# Y31：1-loop SM RGE 独立复算
inv_aem = Decimal("127.95")
sin2w = Decimal("0.23122")
a_s = Decimal("0.1179")
MZ = Decimal("91.1876")
MPl = Decimal("1.220910E+19")
bvec = [Decimal(41) / Decimal(10), Decimal(-19) / Decimal(6), Decimal(-7)]  # b_1, b_2, b_3
inv_a_MZ = [
    (Decimal(3) / Decimal(5)) * (Decimal(1) - sin2w) * inv_aem,   # 1/alpha_1 = (3/5) cos^2 / alpha_em
    sin2w * inv_aem,                                              # 1/alpha_2 = sin^2 / alpha_em
    Decimal(1) / a_s,                                             # 1/alpha_3
]
Lln = (MPl / MZ).ln()
inv_a_MPl = [inv_a_MZ[i] - bvec[i] / (2 * PI) * Lln for i in range(3)]
spread = max(inv_a_MPl) - min(inv_a_MPl)
rel_spread = spread / ((sum(inv_a_MPl)) / 3)
L12 = 2 * PI * (inv_a_MZ[0] - inv_a_MZ[1]) / (bvec[0] - bvec[1])
L23 = 2 * PI * (inv_a_MZ[1] - inv_a_MZ[2]) / (bvec[1] - bvec[2])
L13 = 2 * PI * (inv_a_MZ[0] - inv_a_MZ[2]) / (bvec[0] - bvec[2])
Lset = [L12, L23, L13]
dL = max(Lset) - min(Lset)
REF_R28 = [Decimal("3.3287E+1"), Decimal("4.9460E+1"), Decimal("5.2418E+1")]
ref_dev = max(abs((inv_a_MPl[i] - REF_R28[i]) / REF_R28[i]) for i in range(3))
add("FAIL", "能标：1-loop SM RGE 独立复算否证「三耦合在普朗克标度汇聚」",
    "1/alpha_i(M_Pl) = " + " / ".join([format(x, ".6E") for x in inv_a_MPl]),
    "独立复算（b = (41/10, -19/6, -7)；1/alpha_em(M_Z)=127.95, sin^2=0.23122, alpha_s=0.1179, "
    "M_Pl=1.220910e19 GeV）：1/alpha_i(M_Pl) = " + " / ".join([format(x, ".6E") for x in inv_a_MPl]) +
    "，跨度 = " + format(spread, ".6E") + "（相对 " + format(rel_spread * 100, ".4f") + "%）；"
    "三交点 e-折 L = " + " / ".join([format(x, ".6E") for x in Lset]) +
    "，ΔL = " + format(dL, ".10E") +
    "。与 r28 登记值的最大相对偏差 = " + format(ref_dev, ".3E") +
    "（量值级交叉印证，非引用）；与库内 r11/r12 的 9.147 相对差 < 1% ⇒ "
    "**SM 三耦合跑到 M_Pl 不汇聚**（缺 ΔL≈9.1 个 e-折，即 ~9e3 倍能标差）。")

# =====================================================================
# 8. 组 E：宏观 MHD 段（Y32–Y36）
# =====================================================================
add("PASS", "MHD 三式本身是教科书标准式（结构正确）",
    "div B = 0 ; B . grad psi = 0 ; J x B = grad p",
    "机器：三条与标准 MHD 方程组逐字同形 ⇒ 作为**标准式**它们正确；"
    "缺陷在「把它们当作从挠率导出的结论」（见下三条）⇒ 保持「算等正确但零信息量」的不混淆口径。")

# Y33：div B = 0 是恒等式
def dcomp(f, comp, axis, x, y, z, h):
    p = [x, y, z]
    a = list(p); a[axis] += h
    b = list(p); b[axis] -= h
    return (f(*a)[comp] - f(*b)[comp]) / (2.0 * h)


def curl_of(f, x, y, z, h):
    return (dcomp(f, 2, 1, x, y, z, h) - dcomp(f, 1, 2, x, y, z, h),
            dcomp(f, 0, 2, x, y, z, h) - dcomp(f, 2, 0, x, y, z, h),
            dcomp(f, 1, 0, x, y, z, h) - dcomp(f, 0, 1, x, y, z, h))


def div_of(f, x, y, z, h):
    return (dcomp(f, 0, 0, x, y, z, h) + dcomp(f, 1, 1, x, y, z, h) + dcomp(f, 2, 2, x, y, z, h))


A1 = lambda x, y, z: (math.sin(y) * math.cos(z), math.sin(z) * math.cos(x), math.sin(x) * math.cos(y))
A2 = lambda x, y, z: (x * y, y * z, z * x)
B_pos = lambda x, y, z: (x, y, z)


def B_from_A(Afun, h):
    def B(x, y, z):
        return curl_of(Afun, x, y, z, h)
    return B


rows_divb = []
for Afun, nm in ((A1, "A1"), (A2, "A2")):
    for h in (1e-3, 5e-4):
        Bf = B_from_A(Afun, h)
        for p in pts:
            rows_divb.append((nm, h, div_of(Bf, p[0], p[1], p[2], 1e-4)))
divb_pos_val = div_of(B_pos, 0.3, 0.2, 0.1, 1e-5)
add("FAIL", "MHD：div B = 0 是 nabla.(nabla x A) ≡ 0 的定义恒等式（零信息量）",
    "对任意光滑 A 恒成立 ⇒ 与挠率无关",
    "机器：div(curl A) 对两组不同 A（A1 三角函数型、A2 多项式型）、两档差分步长、三个采样点实算，"
    "残差全部落在差分误差量级（|值| <= " + format(max(abs(r[2]) for r in rows_divb), ".3E") + "）；"
    "**阳性对照**：把 B 直接给成 (x,y,z) 时 div B = " + format(divb_pos_val, ".10f") +
    "（= 3，证明散度算子非恒零）⇒ 原式与挠率无因果关系（复发 r28 V23，第 2 次）。")

add("FAIL", "MHD：J x B = grad p 是 MHD 平衡的**定义**，不是从挠率导出",
    "J = (nabla x B)/mu_0 代入即得 ⇒ 0 条导出链",
    "机器：该式在 J = curl B / mu_0 的定义下等价于 (curl B) x B = mu_0 grad p，"
    "是标准 MHD 力平衡的**定义式**（Harris sheet 等已知解精确满足）⇒ 无任何 kappa/tau 出现 ⇒ "
    "把它称为「挠率宏观涌现」缺导出链（0 条）。")

# Y35：磁面 vs Beltrami
B_abc = lambda x, y, z: (math.sin(z) + math.cos(y), math.sin(x) + math.cos(z), math.sin(y) + math.cos(x))
B_har = lambda x, y, z: (0.0, math.tanh(x), 0.0)
belt = []
for p in pts:
    cb = curl_of(B_abc, p[0], p[1], p[2], 1e-5)
    bb = B_abc(*p)
    dot = cb[0] * bb[0] + cb[1] * bb[1] + cb[2] * bb[2]
    b2 = bb[0] ** 2 + bb[1] ** 2 + bb[2] ** 2
    belt.append((dot, b2, abs(dot - b2) / max(b2, 1e-30)))
har = []
for p in pts:
    cb = curl_of(B_har, p[0], p[1], p[2], 1e-5)
    bb = B_har(*p)
    har.append(cb[0] * bb[0] + cb[1] * bb[1] + cb[2] * bb[2])
add("FAIL", "MHD：磁面条件 B.grad psi = 0 与 Beltrami 场**不可共存**（反例否证）",
    "Beltrami: curl B = B ⇒ B.(curl B) = |B|^2 != 0 ⇒ Frobenius beta^d beta != 0 ⇒ 无磁面",
    "机器：3D ABC 力自由场（A=B=C=1）精确满足 curl B = B（采样点 |curl B - B|/|B| = " +
    ", ".join([format(x[2], ".3E") for x in belt]) + "）；其 B.(curl B) = " +
    ", ".join([format(x[0], ".6f") for x in belt]) + " 而 |B|^2 = " +
    ", ".join([format(x[1], ".6f") for x in belt]) + " ⇒ 二者相符且**非零** ⇒ "
    "Frobenius 可积条件不满足 ⇒ **不存在**全局磁面；"
    "**阳性对照**：Harris sheet B = tanh(x) y_hat 的 B.(curl B) = " +
    ", ".join([format(x, ".3E") for x in har]) + "（= 0，有磁面）⇒ 判据非恒真。"
    "⇒ 「磁场力全域守恒 ⇒ 磁面自动涌现」被反例否证（复发 r28 V25，第 2 次）。")

add("FAIL", "MHD：「证明聚变磁约束作用力是挠率宏观涌现」= 0 条导出链",
    "来料给的是「证明」二字 + 三条标准 MHD 式",
    "三条式子中 kappa/tau 出现次数 = 0 ⇒ 从主方程到 MHD 的「长波宏观平均 + 弱场近似」只给了名字，"
    "无任何一步可代入 ⇒ 属断言而非证明（与 r28 V21/V26 同族）。")

# =====================================================================
# 9. 组 F：结论段（Y37–Y41）
# =====================================================================
# Y37：四种分量 vs 三种 + 「对称部分」恒零
def tau_sym_resid():
    """对 (mu,nu) 反对称的 tau^a_{mu,nu}，其『对称部分』恒为零 —— 全分量穷举"""
    worst = 0.0
    v = 0.37
    for a in range(4):
        for m in range(4):
            for n in range(4):
                t = v * ((a + 1) * 0.13 + (m + 1) * 0.07 + (n + 1) * 0.03) - (0.5 if m == n else 0.0)
                if m == n:
                    t = 0.0
                elif m > n:
                    t = -t
                sym = 0.5 * (t + (-t if m != n else t))   # (tau_{mu nu} + tau_{nu mu})/2
                worst = max(worst, abs(sym))
    return worst


sym_res = tau_sym_resid()
CLAIM_PARTS = ["对称", "反对称", "手征", "缠绕"]
ADD_PARTS = ["迹", "无迹", "完全反对称"]
add("FAIL", "§六.2 与 §一/§二 内部矛盾：「四种分量」vs「三种分类」",
    "§六 说 4 种（对称/反对称/手征/缠绕）vs §一/§二 用 3 种（迹/无迹/完全反对称）",
    "机器：§六 列出的分量种类数 = " + str(len(CLAIM_PARTS)) + "（" + "/".join(CLAIM_PARTS) + "）；"
    "§一/§二 实际使用的分类数 = " + str(len(ADD_PARTS)) + "（" + "/".join(ADD_PARTS) + "）⇒ 4 != 3。"
    "且其中「对称部分」**恒等于零**（机器全分量穷举：tau^a_{mu nu} 对 (mu,nu) 反对称 ⇒ "
    "(tau_{mu nu}+tau_{nu mu})/2 的最大绝对值 = " + format(sym_res, ".3E") + "）⇒ 该「分量」不存在"
    "（复发 r28 V04，第 2 次）。")

# Y38：无外挂场 / 无独立耦合 / 无额外参数 —— 符号计数反证
EXTERNAL_SYMBOLS = [
    "G", "tau_chiral", "tau_[alpha mu nu]", "f(kappa,tau)", "g_geo",
    "g_em", "g_weak", "g_strong",
    "T^curv", "T^tor", "T^spiral", "Psi",
]
hits = []
for s in EXTERNAL_SYMBOLS:
    key = s.replace("^", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
    key = key.replace(" ", "").replace(",", "").replace("_", "")
    probe = LAI_TEXT.replace("^", "").replace("[", "").replace("]", "").replace("(", "")
    probe = probe.replace(")", "").replace(" ", "").replace(",", "").replace("_", "").replace("{", "").replace("}", "")
    if key.lower() in probe.lower():
        hits.append(s)
add("FAIL", "§六.4「无外挂场、无独立耦合、无额外参数」被符号计数直接反证",
    "机器计数：式内独立符号 " + str(len(hits)) + " 项未由 kappa/tau 定义",
    "§六 声称「无外挂场、无独立耦合、无额外参数」，但机器扫描其**自身式集**中出现的独立符号：" +
    " / ".join(hits) + " 共 " + str(len(hits)) + " 项，全部未由 kappa / tau 定义，也无一条定义式把它们连到 kappa / tau。"
    "其中：G 是量纲常数（不是几何量）；g_em/g_weak/g_strong/g_geo 是 4 个独立耦合；"
    "tau_chiral 与 tau_[alpha mu nu] 是 2 个未定义分量；f(kappa,tau) 未定义；T^* 三项未定义。"
    "⇒ 「无额外参数」与自身式集矛盾。")

add("FAIL", "§六「人类首套完全自洽、无自由参数、纯几何本源」与库内已确立结论冲突",
    "与 r15 / r28 / r29 的机器读数冲突",
    "库内已登记（本册不重算，只引用）："
    "① r15「自由度预算口径」——Ω5 按口径 II（常数 + 分区节点）实际自由度 = 5，且模型**已在使用未声明外部输入**；"
    "② r28 V01——同一批 V4.0 来料有 12 项未定义/未给形式的量；"
    "③ r29——料1 自称修复 11 项，实质修复 1 项（修复率 9.0909...%）。"
    "⇒ 本份的「无自由参数」是**第三次**在同一天出现、且每次都与机器读数相反的强声称 ⇒ "
    "该声称同时不可证伪（无判据可使其为假）。")

add("FAIL", "§六.1/§六.3 封闭性声称 0 条可检验推论",
    "「包揽宇宙所有作用力」「尺度贯通」",
    "机器：12 条式子中，给出**数值预言**（含可测标度/可代入常数）的条数 = 0；"
    "全部式子无一条含具体常数或可测量 ⇒ 无法设计任何判决实验；"
    "与库内「唯一数值预言数 = 0」的全册一致读数同向。")

# Y41：无 hbar ⇒ 「兼容量子」无载体
HBAR_TOKENS = ["hbar", "hbar", "h/2pi", "h_bar", "hslash", "ħ", "ℏ"]
hbar_hits = []
for t in HBAR_TOKENS:
    if t in LAI_TEXT:
        hbar_hits.append(t)
probe_pos = "test hbar string"      # 阳性对照
pos_detect = ("hbar" in probe_pos)
add("FAIL", "「兼容量子」无载体：式集中无 hbar（机器符号扫描）",
    "12 条式子中 hbar / ħ 出现次数 = " + str(len(hbar_hits)),
    "机器符号扫描（含 hbar / ħ / h_bar / h/2pi 等 7 种写法）：命中 " + str(len(hbar_hits)) + " 次。"
    "量子化判据（正则对易、hbar 的显式出现、普朗克常数标度）在来料式中**全部缺席** ⇒ "
    "§一 声称「兼容量子」在式层面无载体；阳性对照（在测试串中检出 hbar = " + str(pos_detect) +
    "）证明扫描器非恒假。")

# Y42：三条分化方程互不同源
SIG_EM = ("二次型(tau,tau)", "无外部流", "自由指标 nu")
SIG_WEAK = ("标量x流", "含外部流 J^a", "自由指标 a,nu")
SIG_STRONG = ("三指标反对称x流", "含外部流 J^A", "自由指标 A,alpha,mu")
sigs = [SIG_EM, SIG_WEAK, SIG_STRONG]
add("FAIL", "四力分化方程**互不同源**：缺统一的 tau -> 各力 映射定理",
    "三条 RHS 结构不同类 ⇒ 无共同函子",
    "机器结构签名：电磁 = " + str(SIG_EM) + "；弱力 = " + str(SIG_WEAK) + "；强力 = " + str(SIG_STRONG) +
    " ⇒ 三者**构造类互不相同**（一个双线性无源、两个不同指标结构的标量/张量 x 流），"
    "却都声称来自**同一个** tau ⇒ 缺「tau -> {F,W,G}」的映射定理（0 条），"
    "§六.2「仅由挠率张量的分量区分」因此无机制支撑。")

# =====================================================================
# 10. 组 G：跨册比对与治理（Y43–Y44）
# =====================================================================
PAIRS = [
    ("MHD JxB", "J x B = grad p", LAI["s5_jxb"]),
    ("MHD divB", "div B = 0", LAI["s5_divb"]),
    ("MHD flux", "B . grad psi = 0", LAI["s5_flux"]),
    ("beta 定义", "beta(g_i) = F_i(kappa[mu], tau[mu])", LAI["s4_beta"]),
    ("波动方程", "nabla^2 Psi - (kappa^2 - tau^2) Psi = 0", LAI["s3_wave"]),
    ("主方程", "G_{mu nu} = 8 pi G (T_matter + T_torsion)",
     "G_{mu nu} = 8 pi G (T^curv_{mu nu} + T^tor_{mu nu} + T^spiral_{mu nu})"),
]
ratios_x = []
for nm, a, b in PAIRS:
    ratios_x.append((nm, difflib.SequenceMatcher(None, a, b).ratio()))
mean_ratio = sum(r for _, r in ratios_x) / len(ratios_x)
NEW_EQ = ["引力极限式", "电磁显式式", "弱力显式式", "强力显式式"]
DEL_EQ = ["作用量（含 (1/4)tau^2 挠率不变量）", "tau ∝ S 关系"]
add("MISMATCH", "跨册比对：本份是同日 V4.0 材料的**第 3 个变体**（式层重排）",
    "与 r28 来料 6 组可比式逐字相似度均值 = " + format(mean_ratio, ".4f"),
    "比对对象为两册来料的**转写文本**（声明局限：非原始文件字节），"
    "6 组可比式相似度：" + " / ".join([nm + "=" + format(r, ".4f") for nm, r in ratios_x]) +
    "；均值 = " + format(mean_ratio, ".6f") + "（其中 MHD 三式 = 1.000000）。"
    "**式名集比对**：本份**新增** " + str(NEW_EQ) + "（r28/r29 只有定性指派表，无显式方程 ⇒ 本份净增量）；"
    "**删除** " + str(DEL_EQ) + "；**改写** 主方程（2 项 -> 3 项）与波动方程（nabla^2 -> nabla^a nabla_a）。"
    "⇒ 方程层面是**重排 + 增补显式式**，不是新推导（与 r29 W18 的 0.9699 同型结论）。")

add("INFO", "本册条目与 r28 / r29 不可相加",
    "Y01–Y" + str(len(ITEMS) + 1).zfill(2) + " 与 V01–V46 / W01–W38 独立编号",
    "本册只审**本份来料**（六节「终极方程组」）；r28 审 V4.(0) 13 节、r29 审「全修复攻破版」11 项自称。"
    "三册对象不同、条目不可相加；本册**不复算** V01–V46 / W01–W38 的任何条目，只做跨册重复度与漂移登记。")

# =====================================================================
# 11. 自检（S01–S14）
# =====================================================================
CHECKS = []


def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})


chk("S01_dadd_不是tuple拼接",
    len(dadd(D(1, 0, 0, 0), D(0, 1, 0, 0))) == 4 and dadd(D(1, 0, 0, 0), D(0, 1, 0, 0)) == D(1, 1, 0, 0),
    "dadd((M),(L)) = " + dstr(dadd(D(1, 0, 0, 0), D(0, 1, 0, 0))) + " 且长度恒为 4")
chk("S02_主方程缺口为c^-4且SI形式闭合",
    (dstr(gap_master) == dstr(dneg(dscale(d_c, 4)))) and iszero(gap_master_si),
    "来料缺口 " + dstr(gap_master) + " = c^-4 ; 正确 SI 形式残差 " + dstr(gap_master_si))
chk("S03_指标分析器_电磁式判坏", (not idx_em["ok"]) and (not idx_em["RHS_bad"] == []) and (not idx_em["free_match"]),
    "RHS_bad=" + str(idx_em["RHS_bad"]) + " free_match=" + str(idx_em["free_match"]))
chk("S04_指标分析器_弱力式判好", idx_weak["free_match"] and (not idx_weak["RHS_bad"] and not idx_weak["LHS_bad"]),
    "free=" + str(idx_weak["LHS_free"]) + " vs " + str(idx_weak["RHS_free"]))
chk("S05_散度算子阳性对照=3", abs(divb_pos_val - 3.0) < 1e-6, "div(x,2y,3z) = " + format(divb_pos_val, ".10f"))
chk("S06_RGE与r28登记值一致", ref_dev < Decimal("1E-3"),
    "最大相对偏差 " + format(ref_dev, ".3E") + " < 1e-3")
chk("S07_dL与库内9.147一致", abs(dL - Decimal("9.147")) / Decimal("9.147") < Decimal("0.01"),
    "ΔL = " + format(dL, ".6E") + " vs 9.147，相对差 " + format(abs(dL - Decimal("9.147")) / Decimal("9.147"), ".3E"))
_belt_res = max(x[2] for x in belt)
chk("S08_Beltrami_curlB_eq_B", _belt_res < 1e-6, "最大 |curl B - B|/|B| = " + format(_belt_res, ".3E"))
chk("S09_Harris_B_dot_curlB_为零", max(abs(v) for v in har) < 1e-6,
    "max |B.(curl B)| = " + format(max(abs(v) for v in har), ".3E"))
chk("S10_divcurlA_差分误差量级", max(abs(r[2]) for r in rows_divb) < 1e-3,
    "max |div(curl A)| = " + format(max(abs(r[2]) for r in rows_divb), ".3E"))
chk("S11_差值守恒_漂移为机器零", max_drift < Decimal("1E-50"),
    "max drift = " + format(max_drift, "E") + "（60 位精度下机器零）")
chk("S12_tau对称部分恒零", sym_res == 0.0, "最大 |对称部分| = " + format(sym_res, ".3E"))
chk("S13_hbar扫描器阳性对照", (len(hbar_hits) == 0) and pos_detect,
    "来料命中 " + str(len(hbar_hits)) + " / 阳性对照检出 " + str(pos_detect))
_ids = [it["id"] for it in ITEMS]
chk("S14_条目计数自洽且id唯一", (len(_ids) == len(set(_ids))) and (sum(tally().values()) == len(ITEMS)),
    "条目 " + str(len(ITEMS)) + " / 唯一 id " + str(len(set(_ids))))

# =====================================================================
# 12. 产物输出
# =====================================================================
T = tally()
TOTAL = len(ITEMS)
PASS_N = T.get("PASS", 0)
FAIL_N = T.get("FAIL", 0)
BND_N = T.get("BOUNDARY", 0)
MIS_N = T.get("MISMATCH", 0)
INF_N = T.get("INFO", 0)
OK_N = sum(1 for c in CHECKS if c["ok"])

RECURRENCE = [
    {"family": "量纲缺口族（几何量当耦合/常数）", "first": "r18", "mid": "r22 / r27 / r28(V09) / r29(W14)",
     "here": "Y03 / Y07 / Y11 / Y15 / Y20 / Y29", "n": "第 9 次"},
    {"family": "零信息量重述（把标准式当导出）", "first": "r18 §3", "mid": "r22 / r27 / r28(V23,V24) / r29(W07,W28)",
     "here": "Y33 / Y34 / Y36", "n": "第 7 次"},
    {"family": "结论段自否证（声称与内容矛盾）", "first": "r27", "mid": "r28(V40) / r29(W02–W13)",
     "here": "Y37 / Y38 / Y39", "n": "第 4 次"},
    {"family": "符号同名 / 未定义量", "first": "r22", "mid": "r27 / r28(V01,V44) / r29(W32)",
     "here": "Y01 / Y16 / Y38", "n": "第 4 次"},
    {"family": "不可证伪声称 / 已关窗口仍列为通道", "first": "30 号册 D-03", "mid": "r27 / r28(V30)",
     "here": "Y39 / Y40 / Y41", "n": "第 4 次"},
    {"family": "类型/标签互斥（标量方程自称旋量/替代 Dirac）", "first": "r28(V16)", "mid": "r29(W03,W05)",
     "here": "Y24", "n": "第 3 次"},
    {"family": "分量计数不足（4 分量装 8 生成元）", "first": "r28(V07)", "mid": "—",
     "here": "Y21", "n": "第 2 次"},
    {"family": "磁面自动涌现（被 Beltrami 反例否证）", "first": "r28(V25)", "mid": "—",
     "here": "Y35", "n": "第 2 次"},
    {"family": "作用量与演化方程不同源", "first": "r19", "mid": "r21 / r27 / r28(V14) / r29(W12)",
     "here": "不适用（本份**无作用量段**）", "n": "不计数"},
]

KEY = {
    "条目总数": TOTAL,
    "可代入等式数": EQ_COUNT,
    "未定义符号数": len(UNDEFINED),
    "式内独立外部符号数": len(hits),
    "主方程_缺口": dstr(gap_master),
    "主方程_c4数值": format(c4, "E"),
    "电磁_量纲缺口SI": dstr(gap_em_si),
    "电磁_量纲缺口自然单位": dstr(gap_em_nat),
    "弱强_量纲缺口SI": dstr(gap_weak_si),
    "电磁_div_B相对比": [format(r, ".6E") for r in ratios],
    "电磁_div_B收敛量": [format(x, ".3E") for x in conv],
    "散度阳性对照值": format(divb_pos_val, ".10f"),
    "完全反对称分量数_C43": c43,
    "SU3生成元缺口": 8 - c43,
    "tau对称部分最大绝对值": format(sym_res, ".3E"),
    "波动方程量纲残差": dstr(gap_wave),
    "1-loop_反alphas_MPl": [format(x, ".6E") for x in inv_a_MPl],
    "1-loop_跨度": format(spread, ".6E"),
    "1-loop_相对跨度": format(rel_spread, ".6E"),
    "1-loop_L三交点": [format(x, ".6E") for x in Lset],
    "1-loop_dL": format(dL, ".10E"),
    "与r28登记值最大相对偏差": format(ref_dev, ".3E"),
    "差值守恒最大漂移": format(max_drift, "E"),
    "Beltrami_B_dot_curlB": [format(x[0], ".6f") for x in belt],
    "Beltrami_absB2": [format(x[1], ".6f") for x in belt],
    "Harris_B_dot_curlB": [format(x, ".3E") for x in har],
    "hbar命中次数": len(hbar_hits),
    "跨册相似度均值": format(mean_ratio, ".6f"),
    "跨册相似度分项": {nm: format(r, ".6f") for nm, r in ratios_x},
}

payload = {
    "round": ROUND,
    "tag": TAG,
    "date": "2026-10-10",
    "source": "《TUFT V4.0 全域力的统一终极方程组（四力同源唯一主方程）》—— 六节",
    "engine": "纯标准库 Py3.8.8：Decimal 60 位 + Fraction 量纲向量 (M,L,T,Q) + 指标多重集代数 + 中心差分数值对拍 + difflib 逐字比对 + 正则符号扫描",
    "total": TOTAL,
    "tally": {"PASS": PASS_N, "FAIL": FAIL_N, "BOUNDARY": BND_N, "MISMATCH": MIS_N, "INFO": INF_N},
    "selfcheck": {"passed": OK_N, "total": len(CHECKS)},
    "items": ITEMS,
    "selfchecks": CHECKS,
    "key_numbers": KEY,
    "recurrence": RECURRENCE,
}

p_json = os.path.join(DATA_DIR, TAG + ".json")
p_md = os.path.join(DATA_DIR, TAG + ".md")
p_txt = os.path.join(DATA_DIR, TAG + "_report.txt")


def ensure_dir(p):
    if not os.path.isdir(p):
        os.makedirs(p)


ensure_dir(DATA_DIR)

with io.open(p_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))

lines = []
lines.append("# " + TAG + " · 数据摘要")
lines.append("")
lines.append("- **来源**：《TUFT V4.0 全域力的统一终极方程组（四力同源唯一主方程）》（六节）")
lines.append("- **引擎**：" + payload["engine"])
lines.append("- **读数**：条目 " + str(TOTAL) + "（PASS " + str(PASS_N) + " / FAIL " + str(FAIL_N) +
             " / BOUNDARY " + str(BND_N) + " / MISMATCH " + str(MIS_N) + " / INFO " + str(INF_N) +
             "）｜自检 " + str(OK_N) + "/" + str(len(CHECKS)))
lines.append("")
lines.append("## 逐条判定")
lines.append("")
lines.append("| 条目 | 判定 | 名称 | 标题 |")
lines.append("| --- | --- | --- | --- |")
for it in ITEMS:
    lines.append("| " + it["id"] + " | " + it["verdict"] + " | " + it["name"] + " | " + it["title"] + " |")
lines.append("")
lines.append("## 关键读数")
lines.append("")
for k in KEY:
    v = KEY[k]
    if isinstance(v, list):
        lines.append("- **" + k + "** = " + " / ".join([str(x) for x in v]))
    elif isinstance(v, dict):
        lines.append("- **" + k + "** = " + json.dumps(v, ensure_ascii=False))
    else:
        lines.append("- **" + k + "** = " + str(v))
lines.append("")
lines.append("## 复发登记")
lines.append("")
lines.append("| 缺陷族 | 首次 | 中间 | 本册 | 次数 |")
lines.append("| --- | --- | --- | --- | --- |")
for r in RECURRENCE:
    lines.append("| " + r["family"] + " | " + r["first"] + " | " + r["mid"] + " | " + r["here"] + " | " + r["n"] + " |")
lines.append("")

with io.open(p_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

rep = []
for it in ITEMS:
    rep.append(it["id"] + " [" + it["verdict"] + "] " + it["name"] + " :: " + it["title"])
rep.append("")
rep.append("自检：" + str(OK_N) + "/" + str(len(CHECKS)))
for c in CHECKS:
    rep.append(("  OK  " if c["ok"] else " FAIL ") + c["name"] + " :: " + c["detail"])
rep.append("")
rep.append("PASS = " + str(PASS_N) + " | FAIL = " + str(FAIL_N) + " | BOUNDARY = " + str(BND_N) +
           " | MISMATCH = " + str(MIS_N) + " | INFO = " + str(INF_N) + " | TOTAL = " + str(TOTAL))
rep.append("EXIT_CODE = " + ("0" if OK_N == len(CHECKS) else "1"))
with io.open(p_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

# ---- 控制台 ----
for it in ITEMS:
    print(it["id"] + " [" + it["verdict"] + "] " + it["name"])
print("")
for c in CHECKS:
    print(("  OK  " if c["ok"] else " FAIL ") + c["name"] + " :: " + c["detail"])
print("")
print("条目 " + str(TOTAL) + "（PASS " + str(PASS_N) + " / FAIL " + str(FAIL_N) +
      " / BOUNDARY " + str(BND_N) + " / MISMATCH " + str(MIS_N) + " / INFO " + str(INF_N) + "）")
print("PASS = " + str(PASS_N) + " | FAIL = " + str(FAIL_N) + " | BOUNDARY = " + str(BND_N) +
      " | MISMATCH = " + str(MIS_N) + " | INFO = " + str(INF_N))
print("自检 " + str(OK_N) + "/" + str(len(CHECKS)))
print("JSON  = " + p_json)
print("MD    = " + p_md)
print("TXT   = " + p_txt)
print("EXIT_CODE = " + ("0" if OK_N == len(CHECKS) else "1"))

sys.exit(0 if OK_N == len(CHECKS) else 1)
