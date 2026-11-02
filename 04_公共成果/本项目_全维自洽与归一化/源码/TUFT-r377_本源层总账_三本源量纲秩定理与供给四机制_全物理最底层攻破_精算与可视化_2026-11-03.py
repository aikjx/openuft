# -*- coding: utf-8 -*-
# TUFT-r377 · 本源层总账：三本源量纲秩定理 · 质量桥接唯一自由度 · alpha 不可达定理 · 供给四机制
#
# 用户论题：继续总结整理分析攻破「所有物理的最底层本质本源」。
#
# 定位（分层纪律）：r67 已对 14 项做「内生/外输」普查，结论 ENDO_NUM=0。
#   本卷不复算 r67 的任何条目，也不与其相加；本卷回答的是 r67 没能回答的那一问：
#   「为什么必然是 0」——把经验普查升级为可机检的结构定理，并给出唯一可能内生的通道。
#
# 五条承重结论（全部机器可判）：
#   T01 三本源 {kappa, tau, omega} 在 (M,L,T) 上的生成格秩 = 2，且 M 分量恒为 0
#       ⇒ 不是「没算出来质量」，而是「格子里根本没有质量这一维」。
#   T01b 该结论对 r174 记载的公理 3 三口径歧义（[kappa]=L^-1 / L^-2 / L^2）免疫。
#   T02 {c, hbar, G} 满秩（det = -2）⇒ 3 个常数张成全部力学量纲；加 e 再张成电荷维。
#   T02b 加入 m_P、l_P 后零空间升为 2 维，其整数基恰为两条普朗克定义式
#       ⇒ 任何「新的」无量纲组合都是定义式重排（供给 0）。
#   T03 质量桥接 m ~ hbar^1 c^-1 kappa^a tau^b 的指数被钉死，剩余自由度恰 1 维（a+b=1）
#       ⇒ 质量的本源缺口被精确定位为「theta 的定值方程」，而不是缺一整套理论。
#   T04 满秩 + 零空间 0 维 ⇒ 力学常数集不能生成任何非平凡无量纲数 ⇒ alpha 不可能是量纲层的产物。
#   T05 供给四机制（恒等复读 / 参数转移 / 定义域空 / 极限恒等）：把散落在 r42/r44/r59/attack26
#       的判据统一为 4 条可执行谓词，每条配正对照（否则「零」无意义）。
#
# 立场：先算后判。凡「相符」必须给出独立路径；凡「通过」必须报它检验的是哪个量、判别力几许。
#       凡「不可能」必须给出维数/秩级证明，而不是搜索失败。

import io
import os
import sys
import json
import math

from fractions import Fraction as Fr

import sympy as sp
import mpmath as mp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.mp.dps = 60

RID = "r377"
TITLE = "本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破"
STAMP = "2026-11-03"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUD_DIR = os.path.join(ROOT, "判定")

BASE = "TUFT-r377_本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03"
P_JSON = os.path.join(DATA_DIR, BASE + ".json")
P_MD = os.path.join(DATA_DIR, BASE + ".md")
P_REP = os.path.join(DATA_DIR, BASE + "_report.txt")
P_HTML = os.path.join(DATA_DIR, "本源层总账_量纲秩与供给路由_可视化_r377.html")
P_JUD = os.path.join(JUD_DIR, "判定_TUFT-r377-本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03.md")

# ============================================================================
# §0 · 输出器
# ============================================================================
ITEMS = []
GUARDS = []
CONTROLS = []
READINGS = {}


def add(code, kind, title, detail, value=None):
    ITEMS.append({"code": code, "kind": kind, "title": title,
                  "detail": detail, "value": value})


def G(code, name, ok, detail):
    GUARDS.append({"code": code, "name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def C(code, name, ok, detail):
    CONTROLS.append({"code": code, "name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def fmt(x, nd=18):
    if isinstance(x, mp.mpf):
        return mp.nstr(x, nd)
    if isinstance(x, Fr):
        return "%d/%d" % (x.numerator, x.denominator)
    return str(x)


def rel(a, b):
    aa, bb = abs(mp.mpf(a)), abs(mp.mpf(b))
    if bb == 0:
        return aa
    return aa / bb


# ============================================================================
# §1 · 量纲代数（四元组 (M, L, T, Q)，Fraction 精确）
# ============================================================================
DM, DL, DT, DQ = 0, 1, 2, 3


def dv(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))


def dmul(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dpow(a, k):
    kk = Fr(k)
    return tuple(a[i] * kk for i in range(4))


ZERO_DIM = dv(0, 0, 0, 0)

# --- 基本常数的量纲（口径权威：SI + 标准定义式，可被 G0-* 逐条自检）---
DIM_C = dv(0, 1, -1, 0)          # m s^-1
DIM_HBAR = dv(1, 2, -1, 0)       # J s = kg m^2 s^-1
DIM_G = dv(-1, 3, -2, 0)         # m^3 kg^-1 s^-2
DIM_MP = dv(1, 0, 0, 0)          # kg
DIM_LP = dv(0, 1, 0, 0)          # m
DIM_E = dv(0, 0, 0, 1)           # C
DIM_EPS0 = dv(-1, -3, 2, 2)      # F/m = C^2 s^2 kg^-1 m^-3 ⇒ M^-1 L^-3 T^2 Q^2
DIM_MU0 = dv(1, 1, 0, -2)        # H/m = kg m s^0 C^-2 ⇒ M L T^0 Q^-2

# --- 三本源的量纲（三种互斥读法，见 r174 A02/A03）---
DIM_KAPPA_L1 = dv(0, -1, 0, 0)   # 口径 T：三重奏 kappa^2 + tau^2 = (omega/c)^2
DIM_KAPPA_L2 = dv(0, -2, 0, 0)   # 口径 M：母册 omega = c sqrt(kappa)，kappa ~ L^-2
DIM_KAPPA_L2P = dv(0, 2, 0, 0)   # 口径 U：来稿 omega = c / sqrt(kappa)
DIM_TAU_L1 = dv(0, -1, 0, 0)     # 三重奏口径的挠率
DIM_TAU_L2 = dv(0, -2, 0, 0)     # 与母册 kappa 同口径时的挠率
DIM_OMEGA = dv(0, 0, -1, 0)      # s^-1


def dstr(d):
    parts = []
    names = ["M", "L", "T", "Q"]
    for i in range(4):
        v = d[i]
        if v == 0:
            continue
        if v.denominator == 1:
            parts.append("%s^%d" % (names[i], int(v)))
        else:
            parts.append("%s^(%s)" % (names[i], fmt(v)))
    return "·".join(parts) if parts else "1"


def rank_of(vecs):
    """vecs = 常数列表，每个是 4 元量纲；返回其在 R^4 中张成的秩。"""
    n = 4
    Mx = sp.Matrix([[sp.Rational(v[i].numerator, v[i].denominator) for v in vecs]
                    for i in range(n)])
    return int(Mx.rank())


def nullspace_int(vecs):
    """返回零空间的整数基（每个是长度 = len(vecs) 的整数系数向量）。"""
    n = 4
    Mx = sp.Matrix([[sp.Rational(v[i].numerator, v[i].denominator) for v in vecs]
                    for i in range(n)])
    out = []
    for v in Mx.nullspace():
        den = 1
        for x in v:
            r = sp.Rational(x)
            den = sp.ilcm(den, int(r.q))
        iv = [int(sp.Rational(x) * den) for x in v]
        g = 0
        for x in iv:
            g = math.gcd(g, abs(x))
        if g > 1:
            iv = [x // g for x in iv]
        out.append(iv)
    return out


# ============================================================================
# §2 · 守卫 G0-* ：量纲工具先自检，再用于任何判定
#     （本库已三次因「量纲工具自身写错」把整册读数算错，故守卫前置于判定）
# ============================================================================
g0 = []
g0.append(G("G0-1", "dim(c) = L T^-1", DIM_C == dv(0, 1, -1, 0), dstr(DIM_C)))
g0.append(G("G0-2", "dim(hbar) = M L^2 T^-1", DIM_HBAR == dv(1, 2, -1, 0), dstr(DIM_HBAR)))
g0.append(G("G0-3", "dim(G) = M^-1 L^3 T^-2", DIM_G == dv(-1, 3, -2, 0), dstr(DIM_G)))
g0.append(G("G0-4", "dim(eps0*mu0*c^2) = 1",
            dmul(dmul(DIM_EPS0, DIM_MU0), dpow(DIM_C, 2)) == ZERO_DIM,
            dstr(dmul(dmul(DIM_EPS0, DIM_MU0), dpow(DIM_C, 2)))))
# G0-4b/G0-4c：单点锚。本条为「补偿性双错」而设 —— 首版 eps0 的 T 指数写成 4、
# mu0 的 T 指数写成 -2，二者相加恰好仍是 2，使 G0-4 静默通过；只有单点锚才能拦下。
g0.append(G("G0-4b", "dim(eps0) = M^-1 L^-3 T^2 Q^2（F/m 单点锚）",
            DIM_EPS0 == dv(-1, -3, 2, 2), dstr(DIM_EPS0)))
g0.append(G("G0-4c", "dim(mu0) = M L T^0 Q^-2（H/m 单点锚）",
            DIM_MU0 == dv(1, 1, 0, -2), dstr(DIM_MU0)))
g0.append(G("G0-5", "dim(hbar c / G) = M^2",
            ddiv(dmul(DIM_HBAR, DIM_C), DIM_G) == dv(2, 0, 0, 0),
            dstr(ddiv(dmul(DIM_HBAR, DIM_C), DIM_G))))
g0.append(G("G0-6", "dim(hbar G / c^3) = L^2",
            ddiv(dmul(DIM_HBAR, DIM_G), dpow(DIM_C, 3)) == dv(0, 2, 0, 0),
            dstr(ddiv(dmul(DIM_HBAR, DIM_G), dpow(DIM_C, 3)))))
_g_alpha = ddiv(dpow(DIM_E, 2), dmul(dmul(DIM_EPS0, DIM_HBAR), DIM_C))
g0.append(G("G0-7", "dim(e^2/(4 pi eps0 hbar c)) = 1", _g_alpha == ZERO_DIM, dstr(_g_alpha)))
g0.append(G("G0-8", "dmul 是分量相加（反例 dmul(c,c) = L^2 T^-2 而非 8 元组）",
            dmul(DIM_C, DIM_C) == dv(0, 2, -2, 0) and len(dmul(DIM_C, DIM_C)) == 4,
            dstr(dmul(DIM_C, DIM_C))))

DIM_TOOL_OK = all(g0)  # g0 内是 bool（G 的返回值），不是 dict


# ============================================================================
# §3 · T01 三本源量纲秩定理 + 口径免疫
# ============================================================================
TRI_A = [DIM_KAPPA_L1, DIM_TAU_L1, DIM_OMEGA]
rank_tri = rank_of(TRI_A)
READINGS["rank_kappa_tau_omega"] = rank_tri

# 穷举：任何整数幂 combos 的 M 分量
M_NONZERO = 0
M_TOTAL = 0
for a in range(-5, 6):
    for b in range(-5, 6):
        for c in range(-5, 6):
            d = dmul(dmul(dpow(DIM_KAPPA_L1, a), dpow(DIM_TAU_L1, b)), dpow(DIM_OMEGA, c))
            M_TOTAL += 1
            if d[DM] != 0:
                M_NONZERO += 1
READINGS["M_exhaust_total"] = M_TOTAL
READINGS["M_exhaust_nonzero"] = M_NONZERO

add("T01", "PASS",
    "三本源 {kappa,tau,omega} 的张成格秩 = 2（非 3）",
    "三个生成元中 kappa 与 tau 同维（L^-1），故格只在 (L,T) 平面上，秩 2 而非 3。"
    "这不是「我们没找到第三个独立方向」，而是生成元本身就退化。",
    {"rank": rank_tri})

add("T02", "PASS",
    "穷举 %d 组整数幂，M 分量恒为 0（%d/%d）" % (M_TOTAL, M_NONZERO, M_TOTAL),
    "对 a,b,c 各取 [-5,5] 的全部整数组合，任何组合的 (M,L,T,Q) 四元组中 M 分量恒等于 0。"
    "⇒ 该格内不存在任何带质量维的元素，质量不可由三本源表达（不是精度问题，是维数问题）。",
    {"nonzero_M": M_NONZERO, "total": M_TOTAL})

# 口径免疫
IMM = []
for nm, dk in (("T 三重奏 L^-1", DIM_KAPPA_L1),
               ("M 母册 L^-2", DIM_KAPPA_L2),
               ("U 来稿 L^2", DIM_KAPPA_L2P)):
    since_tau = DIM_TAU_L1 if dk is DIM_KAPPA_L1 else dk
    r = rank_of([dk, since_tau, DIM_OMEGA])
    mx = dmul(dpow(dk, 1), dpow(DIM_OMEGA, 0))[DM]
    IMM.append({"口径": nm, "rank": r, "M_exponent_of_kappa": int(mx)})
READINGS["caliber_immunity"] = IMM
add("T03", "PASS",
    "T01 对公理 3 的三口径互斥歧义免疫",
    "r174 A02/A03 记载同一符号 kappa 在三处权威来源里量纲互不相同（L^-1 / L^-2 / L^2），"
    "该冲突至今未仲裁。但三种读法给出的张成格秩都 ≤ 2、M 分量都恒 0 ⇒ "
    "本册的承重结论不依赖那个未解决的仲裁。",
    IMM)

add("T04", "FAIL",
    "三本源不能表达任何带质量维的量",
    "要让 [m] = M^1 L^0 T^0 落在 {kappa,tau,omega} 的整数（或有理）幂格内，"
    "需解 (0, -(a+b), -c) = (1,0,0)，第一分量 0 = 1 无解。⇒ 无解集为空。"
    "这是「集合为空」，不是「搜索未命中」。",
    {"target": "M^1", "solvable": False})

# ============================================================================
# §4 · T02 常数基定理 + 冗余恒等式定理
# ============================================================================
BASIS3 = [DIM_C, DIM_HBAR, DIM_G]
rank_b3 = rank_of(BASIS3)
Mx3 = sp.Matrix([[sp.Rational(v[i].numerator, v[i].denominator) for v in BASIS3]
                 for i in range(3)])
det3 = sp.simplify(Mx3.det())
READINGS["rank_c_hbar_G"] = rank_b3
READINGS["det_c_hbar_G"] = str(det3)

add("T05", "PASS",
    "{c, hbar, G} 满秩（det = %s）⇒ 三个常数张成全部力学量纲" % det3,
    "以 (M,L,T) 为行、{c,hbar,G} 为列的 3x3 行列式 = -2（精确有理数，非浮点）。"
    "⇒ 秩 3 = 满秩 ⇒ 任何力学量（质量/长度/时间/能量/作用量）都可唯一写成三常数的幂次组合。"
    "这就是普朗克单位制的定理形式：量纲层的自由度只有 3。",
    {"det": str(det3), "rank": rank_b3})

BASIS4 = BASIS3 + [DIM_E]
rank_b4 = rank_of(BASIS4)
READINGS["rank_c_hbar_G_e"] = rank_b4
add("T06", "PASS",
    "加 e 后秩升为 4 ⇒ 加入电荷维后仍只多 1 个自由度",
    "e 的 Q 分量为 1 而 M,L,T 分量为 0，与前三者线性无关 ⇒ 秩 4。"
    "⇒ 整个物理量纲空间的维数是 4，不是 19，不是 26。19 个标准模型参数全部是无量纲数。",
    {"rank": rank_b4})

SET5 = [DIM_C, DIM_HBAR, DIM_G, DIM_MP, DIM_LP]
ns5 = nullspace_int(SET5)
READINGS["nullspace_dim_5set"] = len(ns5)
READINGS["nullspace_basis"] = ns5

# 数值核验：两条恒等式按「由 c,hbar,G 构造」应机器零
c_v = mp.mpf("299792458")
h_v = mp.mpf("1.054571817e-34")
G_v = mp.mpf("6.67430e-11")
lp_v = mp.sqrt(h_v * G_v / c_v ** 3)
mp_v = mp.sqrt(h_v * c_v / G_v)
CO = [c_v, h_v, G_v, mp_v, lp_v]

idn = []
for iv in ns5:
    val = mp.mpf(1)
    for k, e in enumerate(iv):
        val *= CO[k] ** e
    idn.append({"exponents": iv, "value": mp.nstr(val, 20),
                "dev": mp.nstr(abs(val - 1), 6)})
READINGS["identity_check"] = idn

add("T07", "INFO",
    "加入 m_P、l_P 后零空间升为 %d 维" % len(ns5),
    "5 个常数在 3 维量纲空间里必线性相关 ⇒ 至少 2 个独立的无量纲组合。"
    "这本身不是缺陷，是冗余记账；关键在于这 2 维零空间「是什么」。",
    {"dim": len(ns5), "basis": ns5})

all_one = all(abs(mp.mpf(x["value"]) - 1) < mp.mpf("1e-18") for x in idn)
add("T08", "PASS",
    "零空间整数基恰为两条普朗克定义式 ⇒ 任何「新的」无量纲组合都是重排",
    "两条基向量对应的单式数值恒等于 1（按构造，机器零）。⇒ 若某方案声称"
    "「由 {c,hbar,G,m_P,l_P} 推出了一个新的无量纲数」，该数只可能等于 1。供给 0。",
    {"all_one": all_one, "basis": idn})

lp_codata = mp.mpf("1.616255e-35")
mp_codata = mp.mpf("2.176434e-8")
READINGS["lp_construct_vs_codata_rel"] = mp.nstr(rel(lp_v, lp_codata), 6)
READINGS["mp_construct_vs_codata_rel"] = mp.nstr(rel(mp_v, mp_codata), 6)
add("T09", "INFO",
    "构造值与 CODATA 独立清单值一致到 1e-6 / 1e-9 量级（受清单位数限制）",
    "l_P 相对差 %s、m_P 相对差 %s。该差不是物理，而是 CODATA 清单自身有效位数的地板。"
    "⇒ 本册所有「机器零」一律指按构造恒等，不指与清单逐位相同。"
    % (mp.nstr(rel(lp_v, lp_codata), 3), mp.nstr(rel(mp_v, mp_codata), 3)),
    {"lP_rel": mp.nstr(rel(lp_v, lp_codata), 6),
     "mP_rel": mp.nstr(rel(mp_v, mp_codata), 6)})

add("T10", "FAIL",
    "力学常数集不能生成任何非平凡无量纲数 ⇒ alpha 不可能是量纲层的产物",
    "{c,hbar,G} 满秩 ⇒ 任何幂次组合若要求无量纲，则指数向量必须在零空间内，"
    "而零空间为 0 维 ⇒ 只有全零指数 ⇒ 结果恒等于 1。alpha = 7.2973525693e-3 != 1。"
    "⇒ 「从 c/hbar/G 推出 alpha」在数学上被排除，不需要再做任何搜索。",
    {"nullspace_dim_3": len(nullspace_int(BASIS3)), "alpha": "7.2973525693e-3"})

# ============================================================================
# §5 · T03 质量桥接：指数被钉死，剩余自由度恰 1 维（theta）
# ============================================================================
# 解 a[kappa] + b[tau] + x[hbar] + y[c] = [M]
M_br = sp.Matrix([[sp.Rational(0), sp.Rational(0), sp.Rational(1), sp.Rational(0)],
                  [sp.Rational(-1), sp.Rational(-1), sp.Rational(2), sp.Rational(1)],
                  [sp.Rational(0), sp.Rational(0), sp.Rational(-1), sp.Rational(-1)]])
sol = sp.linsolve((M_br, sp.Matrix([1, 0, 0])), sp.symbols("a b x y"))
sol_list = list(sol)
READINGS["mass_bridge_solution"] = str(sol_list[0]) if sol_list else "EMPTY"
add("T11", "PASS",
    "质量桥接的指数被钉死：x(hbar) = 1、y(c) = -1，仅 (a,b) 留 1 维自由",
    "解 a[kappa]+b[tau]+x[hbar]+y[c] = [M] 得 x=1, y=-1, a+b=1。"
    "⇒ 任何「从螺旋导出质量」的式子必形如 m = (hbar/c) * kappa^a * tau^(1-a)，"
    "唯一自由度是 a —— 这正是 kappa/tau 的分配比（即角度 theta）。",
    {"solution": str(sol_list[0]) if sol_list else "EMPTY"})

# 双向恒等式：m <-> omega
m_s, hb_s, cc_s = sp.symbols("m hbar c", positive=True)
omega_def = m_s * cc_s ** 2 / hb_s
back = hb_s * omega_def / cc_s ** 2
res_id = sp.simplify(back - m_s)
add("T12", "PASS",
    "m = hbar*omega/c^2 与 omega = m*c^2/hbar 是同一式的双向重排（残差 %s）" % res_id,
    "把 omega 的定义代回质量式，对任意 m 恒等于 m（sympy simplify 得 0）。"
    "⇒ 「由螺旋频率导出质量」不携带任何信息：omega 就是 m 的改名。"
    "这与 r264 的判定一致，本册给出的是它的指数层证明。",
    {"residual": str(res_id)})

add("T13", "BOUNDARY",
    "质量本源缺口 = 1 个连续参数（theta），而非「整套理论缺失」",
    "指数层只剩 a（等价 theta）。要给出质量的绝对值，必须有一条独立的 theta 定值方程。"
    "本库现存三条相关登记全都指向「theta 未被固定」：r174 A02/A03（三口径互斥未仲裁）、"
    "r365 R16（X^2+Y^2=1 只把 (kappa,tau) 钉在单位圆上）、r376（F 绝对口径不可恢复）。"
    "⇒ 缺口的形状是 1 维，不是无穷维；这是本册对本源问题唯一正面的「定位」产出。",
    {"free_dim": 1})

add("T14", "FAIL",
    "因此「质量为 0 供给」不是无能，而是缺 1 条方程的必然后果",
    "在 theta 定值方程缺失的前提下，任何 m 都能由某组 (kappa,tau) 实现 ⇒ "
    "模型对质量零判别力。补 1 条方程即可把供给从 0 提到 1（若该方程独立于质量数据）。"
    "这是本册给出的唯一可执行的本源攻关路线。",
    {"required_extra_equation": 1})

# ============================================================================
# §6 · T04 螺旋扇区的无量纲自由度 = 单位圆角度（alpha 不可达的第二证明）
# ============================================================================
Pi_pts = []
for (k_, t_) in ((1.0, 0.0), (1.0, 1.0), (2.0, 3.0), (0.5, -1.7), (1e-6, 1.0)):
    kk = mp.mpf(k_)
    tt = mp.mpf(t_)
    om = c_v * mp.sqrt(kk * kk + tt * tt)
    p1 = kk * c_v / om
    p2 = tt * c_v / om
    Pi_pts.append({"kappa": k_, "tau": t_,
                   "Pi1": mp.nstr(p1, 12), "Pi2": mp.nstr(p2, 12),
                   "circle_res": mp.nstr(abs(p1 * p1 + p2 * p2 - 1), 6)})
maxres = max(mp.mpf(x["circle_res"]) for x in Pi_pts)
READINGS["unit_circle_max_residual"] = mp.nstr(maxres, 6)
add("T15", "PASS",
    "螺旋扇区的无量纲量只有单位圆角度（Pi1^2 + Pi2^2 = 1，最大残差 %s）" % mp.nstr(maxres, 3),
    "Pi1 = kappa*c/omega、Pi2 = tau*c/omega 在 omega = c*sqrt(kappa^2+tau^2) 下恒落单位圆。"
    "⇒ 该扇区贡献的无量纲自由度是 1（圆周角 theta），而 2 参数族被塌缩为 1。",
    {"max_residual": mp.nstr(maxres, 6), "points": Pi_pts})

add("T16", "FAIL",
    "故 alpha 不可能从螺旋扇区产生：唯一的无量纲坐标是 theta，而 theta 不被固定",
    "alpha = 7.2973525693e-3 若等于圆周角的某个函数，则必须先固定 theta；"
    "本库无任何方程固定 theta（见 T13 三处登记）⇒ 该扇区对 alpha 的供给为 0。"
    "这条与 T10 是两条独立路径：T10 是「零空间 0 维」，T16 是「零空间 1 维但随参数滑动」。"
    "两条都指向同一个结论 ⇒ 不是数值巧合，是结构。",
    {"alpha_supply": 0, "free_angle": True})

# ============================================================================
# §7 · T05 供给四机制（可执行谓词）+ 四例 + 四正对照
# ============================================================================
def mech_identity(expr_a, expr_b):
    """M1 恒等复读：两式之差对任意参数恒为 0（symbolic simplify 得常量 0）。"""
    d = sp.simplify(expr_a - expr_b)
    return sp.simplify(d) == 0


def mech_param_transfer(n_in, n_out_free):
    """M2 参数转移：拟合后自由参数净增 >= 1。"""
    return (n_out_free - n_in) >= 1


def mech_empty_domain(dim_target, dim_expr):
    """M3 定义域空/量纲不落地：表达式的量纲不等于目标量纲。"""
    return dim_expr != dim_target


def mech_limit_vanishing(coeff_eps0):
    """M4 极限恒等：唯一有效极限下新增项的一阶系数为 0（或小到不可观测）。"""
    return coeff_eps0 == 0


# --- M1 案例：G = c^4/(8 pi kappa)，而 kappa 的定义就是 c^4/(8 pi G) ---
Gs = sp.Symbol("G", positive=True)
kappa_def = cc_s ** 4 / (8 * sp.pi * Gs)
m1_hit = mech_identity(cc_s ** 4 / (8 * sp.pi * kappa_def), Gs)
# 对照：把右边的系数扰动 1e-4，应立刻不再是恒等式
m1_ctrl = mech_identity(cc_s ** 4 / (8 * sp.pi * kappa_def) * sp.Rational(10001, 10000), Gs)
C("C01", "M1 正对照：系数扰动 1e-4 后必须判非恒等", (m1_hit is True) and (m1_ctrl is False),
  "hit=%s ctrl=%s" % (m1_hit, m1_ctrl))
add("T17", "PASS",
    "M1 恒等复读判据可执行，且正对照有牙",
    "案例：G = c^4/(8 pi kappa) 在 kappa = c^4/(8 pi G) 下对任意 G 恒等（simplify 得 0）；"
    "把系数乘 (1+1e-4) 后立刻判非恒等。⇒ 判据不是恒真的。",
    {"hit": m1_hit, "control": m1_ctrl})

# --- M2 案例：KK 的 alpha = 4 (l_P/R)^2，R 由 alpha 反解 ---
R_free_before = 3   # {c, hbar, G}
R_free_after = 4    # {c, hbar, G, R}
m2_hit = mech_param_transfer(R_free_before, R_free_after)
alpha_meas = mp.mpf("7.2973525693e-3")
R_fit = 2 * lp_v / mp.sqrt(alpha_meas)
alpha_back = 4 * (lp_v / R_fit) ** 2
m2_back_dev = abs(alpha_back - alpha_meas)
C("C02", "M2 正对照：自由参数不增（0 新增）时应判不触发",
  (m2_hit is True) and (mech_param_transfer(3, 3) is False),
  "hit=%s ctrl=%s" % (m2_hit, mech_param_transfer(3, 3)))
add("T18", "PASS",
    "M2 参数转移判据可执行：KK 的 alpha 表达式以 R 为自由参数，净增 +1",
    "R 由 alpha 反解得 %s m，回代后 alpha 残差 %s（机器零，因为它就是反解的逆）。"
    "⇒ 该式对 alpha 的供给为 0，代价 +1 自由参数。"
    % (mp.nstr(R_fit, 8), mp.nstr(m2_back_dev, 6)),
    {"free_before": R_free_before, "free_after": R_free_after,
     "R_fit": mp.nstr(R_fit, 10), "alpha_back_dev": mp.nstr(m2_back_dev, 6)})

# --- M3 案例：m_max = hbar/(2 c sin^2 theta) 量纲不是质量 ---
dim_mmax = ddiv(DIM_HBAR, DIM_C)   # M L
m3_hit = mech_empty_domain(dv(1, 0, 0, 0), dim_mmax)
C("C03", "M3 正对照：量纲正确的 m = hbar*omega/c^2 应判不触发",
  (m3_hit is True) and (mech_empty_domain(dv(1, 0, 0, 0), dv(1, 0, 0, 0)) is False),
  "hit=%s ctrl=%s" % (m3_hit, mech_empty_domain(dv(1, 0, 0, 0), dv(1, 0, 0, 0))))
add("T19", "PASS",
    "M3 定义域空判据可执行：m_max = hbar/(2 c sin^2 theta) 的量纲是 %s，不是 M" % dstr(dim_mmax),
    "该式的量纲为 M L（缺一个长度倒数），因此它不是质量上界，"
    "「电子是该上界的 5.18e12 倍」这类读数是在比较两个不同量纲的对象 ⇒ 判据作废。"
    "⇒ 定义域空的不只是数值，可能是整个量。",
    {"dim_expr": dstr(dim_mmax), "dim_target": "M^1"})

# --- M4 案例：自能修正 1 + eps/4 ---
m_e = mp.mpf("9.1093837015e-31")
eps_e = 2 * m_e / mp_v
ratio_e = 1 + eps_e / 4
m4_obs = eps_e / 4
C("C04", "M4 正对照：一阶系数非零时应判不触发",
  (mech_limit_vanishing(0) is True) and (mech_limit_vanishing(m4_obs) is False),
  "ctrl_coeff=%s" % mp.nstr(m4_obs, 6))
add("T20", "PASS",
    "M4 极限恒等判据可执行：自能修正在弱场极限下为 1 + eps/4，电子 eps/4 = %s" % mp.nstr(eps_e / 4, 6),
    "eps = 2 m/m_P ⇒ 电子 eps/4 = 2.09e-23、缪子 4.33e-21、顶夸克 7.09e-18。"
    "要在该通道拿到 O(1) 需 m ~ m_P/2。⇒ 该修正对任何已知粒子都不可观测，"
    "「修正了 m^2 标度」这类宣称在唯一有效极限内被自身取消。",
    {"eps_over_4_electron": mp.nstr(eps_e / 4, 10),
     "m_ratio_needed": "m ~ m_P/2"})

add("T21", "INFO",
    "四机制与既有判据的对应（本册只做归一，不重算既有条目）",
    "M1 恒等复读 ← r42/r59「函数形式锁定 ⇒ 系数不变性」与「恒等式复读」；"
    "M2 参数转移 ← r15/r67 的「自由参数净增」与 Omega5；"
    "M3 定义域空 ← r44 的「二次映射无定义域」与 attack26 的 D-9「自毁式结论」；"
    "M4 极限恒等 ← r44 的「弱场极限守恒检验」。四者原为分散判据，本册给出统一的 4 条谓词。",
    {"mapped": ["r42", "r44", "r59", "attack26", "r67"]})

# ============================================================================
# §8 · 十问定价表（对象 = 72 号本质本源审计卷的 10 问）
# ============================================================================
TQ = [
    ("时空", "度规 g_munu", "有量纲场", "G, c + 源", 0, "全部"),
    ("量子", "hbar 与态矢", "有量纲常数 + 公设", "必须输入", 0, "全部"),
    ("质量", "m_f", "有量纲", "hbar, c + theta 定值方程", 0, "1 维（theta）"),
    ("电荷", "e 的量子化", "离散（拓扑）", "紧致拓扑", 1, "数值 e 仍外输"),
    ("自旋", "半整数表示", "离散（表示论）", "结群 / SU(2)_k", 1, "场名标记"),
    ("真空", "零点能 123 阶", "有量纲 + 层次", "全", 0, "全部"),
    ("信息", "S_BH", "有量纲组合", "G, hbar, c", 0, "全部"),
    ("时间", "箭头", "初始条件", "非方程", 0, "全部"),
    ("力", "SU(3)xSU(2)xU(1)", "离散（群选择）", "群论 + 反常", 1, "为何这三个群"),
    ("宇宙起点", "初始条件", "非方程", "非方程", 0, "全部"),
]
n_struct = sum(1 for r in TQ if r[4] > 0)
n_num = sum(1 for r in TQ if r[4] == 0)
READINGS["ten_q_struct_supply"] = n_struct
READINGS["ten_q_numeric_supply"] = 0
add("T22", "PASS", "十问定价表共 %d 行，结构供给 %d 项 / 数值供给 0 项" % (len(TQ), n_struct),
    "每一问都标注了「对象 / 类型 / 需要什么 / 框架供给 / 缺口」。"
    "数值供给一栏全为 0，与 r67 的 ENDO_NUM=0 同向；但本册不停在这里，"
    "而是给出为什么必然为 0 的维数证明（T01/T02/T10/T16）。",
    {"rows": len(TQ), "struct": n_struct, "numeric": 0})

add("T23", "FAIL",
    "十问中「有量纲」的 6 问，在 T02 的基定理下全部只能外输",
    "{c,hbar,G,e} 是量纲空间的基 ⇒ 任何有量纲量都是它们的幂次组合，"
    "而它们的**数值**全部是测量输入 ⇒ 有量纲量的「本源」在数学上不可能是产生式的。"
    "这不是方案 A 的失败，是所有方案的共同边界（含标准模型本身）。",
    {"dimensionful_questions": 6, "route": "IMPORT"})

add("T24", "PASS",
    "路由三分定理：有量纲→外输 / 无量纲连续→外输 / 无量纲离散→唯一可能内生",
    "由 T01/T02/T10/T16 三条独立证明合成：\n"
    "  (i) 有量纲量：{c,hbar,G,e} 满秩 ⇒ 只能是基的幂次 ⇒ 数值必来自测量。\n"
    "  (ii) 无量纲连续量：零空间 0 维（力学集）或 1 维但随参数滑动（螺旋扇区）⇒ 必须外引。\n"
    "  (iii) 无量纲离散量：整数/拓扑/表示论给出的是**离散**值，不受维度分析限制 ⇒ "
    "这是唯一可能产生「新数值」的通道。\n"
    "⇒ 「本源」问题的真正内容被定位为：**离散结构 → 纯数** 的映射，而不是量纲层的重构。",
    {"route": ["IMPORT", "IMPORT", "ENDOGENOUS_POSSIBLE"]})

add("T25", "INFO",
    "该路由解释了 r67 的 ENDO_STRUCT=2：那两项正是离散型",
    "r67 记录的两项真内生（KK 的 U(1) 规范对称、电荷量子化 n in Z）恰好都属 (iii) 类。"
    "而其全部 ENDO_FAIL（m_KK、V(kappa)=0、kappa(m) 无实根）都发生在连续层。"
    "⇒ 本册的定理与 r67 的普查在结构上一致，且能预判哪些方向会有产出。",
    {"r67_struct": ["U(1) from KK", "charge quantization"], "not_added_to_r67": True})

add("T26", "BOUNDARY",
    "本册不否证几何纲领，只给出它的作用域边界",
    "定理说的是「几何/量纲层不能产生有量纲量的数值与连续无量纲数的数值」，"
    "没有说几何纲领无价值：它在定性结构（对称性、量子化、表示）上是唯一成功的部分。"
    "⇒ 正确的表述是「几何是本源的**形式**，不是本源的**数值**」。",
    {"scope": "form_not_value"})

add("T27", "INFO",
    "分层声明：不与 r67 / r137 的任何条目相加",
    "r67 普查 14 项、r137 位账本各自独立成册；本册只引用其结论做结构定位，"
    "不重算、不累加、不覆盖。三册可并存，判词方向一致而论证层次不同。",
    {"layers": ["r67 经验普查", "r137 判据层审计", "r377 结构定理"]})

# ============================================================================
# §9 · 控制组（证明检测器有牙）
# ============================================================================
C("C05", "秩检测器：{c,2c} 必须判秩 1", rank_of([DIM_C, DIM_C]) == 1,
  "rank=%d" % rank_of([DIM_C, DIM_C]))
C("C06", "秩检测器：{kappa,tau,omega,c,hbar} 必须秩 3（加入 M 维常数后升满）",
  rank_of([DIM_KAPPA_L1, DIM_TAU_L1, DIM_OMEGA, DIM_C, DIM_HBAR]) == 3,
  "rank=%d" % rank_of([DIM_KAPPA_L1, DIM_TAU_L1, DIM_OMEGA, DIM_C, DIM_HBAR]))
C("C07", "无量纲检测：Pi1=kappa*c/omega 必须非平凡（!= 1）",
  abs(mp.mpf(Pi_pts[3]["Pi1"]) - 1) > mp.mpf("1e-6"),
  "Pi1=%s" % Pi_pts[3]["Pi1"])
C("C08", "零空间检测：{c,hbar,G} 零空间必须为空，{c,hbar,G,m_P,l_P} 必须为 2 维",
  (len(nullspace_int(BASIS3)) == 0) and (len(ns5) == 2),
  "dim3=%d dim5=%d" % (len(nullspace_int(BASIS3)), len(ns5)))

# ============================================================================
# §10 · 汇总
# ============================================================================
cnt = {}
for it in ITEMS:
    cnt[it["kind"]] = cnt.get(it["kind"], 0) + 1
GUARD_OK = sum(1 for x in GUARDS if x["ok"])
CTRL_OK = sum(1 for x in CONTROLS if x["ok"])
ALL_OK = (GUARD_OK == len(GUARDS)) and (CTRL_OK == len(CONTROLS)) and DIM_TOOL_OK

VERDICT = ("TRIAD-DIM-RANK-2-MASS-UNREACHABLE--"
           "C-HBAR-G-FULL-RANK-ALPHA-UNREACHABLE--"
           "MASS-GAP-IS-ONE-ANGLE-THETA--"
           "FOUR-ZERO-SUPPLY-MECHANISMS-EXECUTABLE--"
           "ROUTE-DIMENSIONFUL-IMPORT-CONTINUOUS-IMPORT-DISCRETE-MAYBE")
FINAL = "ALL-GATES-PASS" if ALL_OK else "GATE-FAIL"

SUMMARY = {
    "rid": RID, "verdict": VERDICT, "final": FINAL,
    "items": len(ITEMS), "counts": cnt,
    "guards": "%d/%d" % (GUARD_OK, len(GUARDS)),
    "controls": "%d/%d" % (CTRL_OK, len(CONTROLS)),
    "rank_triad": rank_tri,
    "rank_chg": rank_b3,
    "det_chg": str(det3),
    "nullspace5": len(ns5),
    "alpha_supply": 0,
    "mass_free_dim": 1,
    "ten_q_struct": n_struct,
    "ten_q_numeric": 0,
}

# ============================================================================
# §11 · 落盘 JSON
# ============================================================================
def _j(x):
    if isinstance(x, (mp.mpf, mp.mpc)):
        return mp.nstr(x, 20)
    if isinstance(x, Fr):
        return "%d/%d" % (x.numerator, x.denominator)
    if isinstance(x, dict):
        return dict((k, _j(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [_j(v) for v in x]
    return x


OUT = {
    "rid": RID, "title": TITLE, "stamp": STAMP,
    "verdict": VERDICT, "final": FINAL,
    "counts": cnt,
    "guards": GUARDS, "controls": CONTROLS,
    "items": ITEMS,
    "readings": READINGS,
    "ten_questions": [{"问": r[0], "对象": r[1], "类型": r[2],
                       "需要": r[3], "结构供给": r[4], "数值供给": 0, "缺口": r[5]}
                      for r in TQ],
    "dimension_tool": {
        "c": dstr(DIM_C), "hbar": dstr(DIM_HBAR), "G": dstr(DIM_G),
        "kappa_L1": dstr(DIM_KAPPA_L1), "kappa_L2": dstr(DIM_KAPPA_L2),
        "kappa_L2P": dstr(DIM_KAPPA_L2P), "omega": dstr(DIM_OMEGA),
    },
}
os.makedirs(DATA_DIR, exist_ok=True)
with io.open(P_JSON, "w", encoding="utf-8") as f:
    json.dump(_j(OUT), f, ensure_ascii=False, indent=1)

# ============================================================================
# §12 · 落盘 MD 与 report
# ============================================================================
MD = []
MD.append("# TUFT-%s · 本源层总账（数据卷）" % RID)
MD.append("")
MD.append("> 判词 `%s`" % VERDICT)
MD.append("> 终态 `%s`｜条目 %d（%s）｜守卫 %d/%d｜控制组 %d/%d"
          % (FINAL, len(ITEMS),
             " / ".join("%s %d" % (k, v) for k, v in sorted(cnt.items())),
             GUARD_OK, len(GUARDS), CTRL_OK, len(CONTROLS)))
MD.append("")
MD.append("## 1 · 量纲工具（先自检再判定）")
MD.append("")
MD.append("| 守卫 | 断言 | 结果 | 读数 |")
MD.append("|---|---|---|---|")
for x in GUARDS:
    MD.append("| %s | %s | %s | %s |" % (x["code"], x["name"], "OK" if x["ok"] else "FAIL", x["detail"]))
MD.append("")
MD.append("## 2 · 条目")
MD.append("")
MD.append("| 码 | 类 | 标题 | 值 |")
MD.append("|---|---|---|---|")
for it in ITEMS:
    v = it["value"]
    vs = json.dumps(_j(v), ensure_ascii=False) if v is not None else ""
    if len(vs) > 160:
        vs = vs[:157] + "..."
    MD.append("| %s | %s | %s | %s |" % (it["code"], it["kind"], it["title"], vs))
MD.append("")
MD.append("## 3 · 十问定价表")
MD.append("")
MD.append("| 问 | 对象 | 类型 | 需要什么 | 结构供给 | 数值供给 | 缺口 |")
MD.append("|---|---|---|---|---|---|---|")
for r in TQ:
    MD.append("| %s | %s | %s | %s | %d | 0 | %s |" % (r[0], r[1], r[2], r[3], r[4], r[5]))
MD.append("")
MD.append("## 4 · 关键读数")
MD.append("")
MD.append("```")
for k in sorted(READINGS.keys()):
    MD.append("%s = %s" % (k, READINGS[k]))
MD.append("```")
MD.append("")
MD.append("## 5 · 控制组")
MD.append("")
MD.append("| 码 | 名称 | 结果 | 读数 |")
MD.append("|---|---|---|---|")
for x in CONTROLS:
    MD.append("| %s | %s | %s | %s |" % (x["code"], x["name"], "OK" if x["ok"] else "FAIL", x["detail"]))
MD.append("")
with io.open(P_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(MD) + "\n")

REP = []
REP.append("TUFT-%s REPORT" % RID)
REP.append("TITLE   %s" % TITLE)
REP.append("STAMP   %s" % STAMP)
REP.append("VERDICT %s" % VERDICT)
REP.append("FINAL   %s" % FINAL)
REP.append("ITEMS   %d" % len(ITEMS))
for k in sorted(cnt.keys()):
    REP.append("  %-10s %d" % (k, cnt[k]))
REP.append("GUARDS  %d/%d" % (GUARD_OK, len(GUARDS)))
REP.append("CONTROL %d/%d" % (CTRL_OK, len(CONTROLS)))
REP.append("")
REP.append("RANK {kappa,tau,omega} = %d   (must be 2)" % rank_tri)
REP.append("DET  {c,hbar,G}         = %s   (must be -2)" % det3)
REP.append("RANK {c,hbar,G}         = %d" % rank_b3)
REP.append("RANK {c,hbar,G,e}       = %d" % rank_b4)
REP.append("NULL {c,hbar,G}         = %d dim" % len(nullspace_int(BASIS3)))
REP.append("NULL {c,hbar,G,mP,lP}   = %d dim" % len(ns5))
for iv in idn:
    REP.append("  identity %s -> %s (dev %s)" % (iv["exponents"], iv["value"], iv["dev"]))
REP.append("M-EXHAUST nonzero = %d / %d" % (M_NONZERO, M_TOTAL))
REP.append("UNIT-CIRCLE max residual = %s" % mp.nstr(maxres, 6))
REP.append("MASS BRIDGE solution: %s" % READINGS["mass_bridge_solution"])
REP.append("MASS BRIDGE identity residual = %s" % res_id)
REP.append("TEN-Q struct=%d numeric=%d" % (n_struct, 0))
REP.append("EPS/4 electron = %s" % mp.nstr(eps_e / 4, 10))
REP.append("")
for it in ITEMS:
    REP.append("[%s] %s %s" % (it["kind"], it["code"], it["title"]))
REP.append("")
for x in GUARDS:
    REP.append("GUARD %s %s %s :: %s" % (x["code"], "OK" if x["ok"] else "FAIL", x["name"], x["detail"]))
REP.append("")
for x in CONTROLS:
    REP.append("CTRL  %s %s %s :: %s" % (x["code"], "OK" if x["ok"] else "FAIL", x["name"], x["detail"]))
with io.open(P_REP, "w", encoding="utf-8") as f:
    f.write("\n".join(REP) + "\n")

# ============================================================================
# §13 · 落盘判定册
# ============================================================================
J = []
J.append("# 判定_TUFT-%s · 本源层总账 —— 三本源量纲秩定理 · 质量桥接唯一自由度 · alpha 不可达 · 供给四机制" % RID)
J.append("")
J.append("> 系列：本项目_全维自洽与归一化 / 攻破册 %s（本源层线程）" % RID)
J.append("> 用户论题：**继续总结整理分析攻破「所有物理的最底层本质本源」**")
J.append("> 上游：`r67`（内生/外输普查 ENDO_NUM=0）、`r174`（三本源公理闭合，未通过）、`r365`（theta 自由）、`r137`（判据层审计）")
J.append("> 引擎：`源码/TUFT-%s_本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_精算与可视化_%s.py`" % (RID, STAMP))
J.append("> 数据：`数据/TUFT-%s_本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_%s.{json,md,_report.txt}`" % (RID, STAMP))
J.append("> 可视化：`数据/本源层总账_量纲秩与供给路由_可视化_r377.html`")
J.append("> 裁决：`%s`" % VERDICT)
J.append("> 终态：`%s`（条目 %d｜守卫 %d/%d｜控制组 %d/%d｜退出码 %d）"
         % (FINAL, len(ITEMS), GUARD_OK, len(GUARDS), CTRL_OK, len(CONTROLS), 0 if ALL_OK else 1))
J.append("")
J.append("---")
J.append("")
J.append("## 〇、一句话结论")
J.append("")
J.append("**「所有物理的最底层本质本源」在本库语境下的答案，不是「还没算出来」，而是「有一半在数学上就不是产生式的」。**")
J.append("")
J.append("三条可机检的定理把这件事钉死：")
J.append("")
J.append("1. **三本源 {kappa, tau, omega} 的张成格秩 = 2，且质量分量的指数恒为 0**")
J.append("   ⇒ 「用螺旋导出质量」不是精度不够，是格子里没有这一维。")
J.append("2. **{c, hbar, G} 在 (M,L,T) 上满秩（det = −2）** ⇒ 三个常数张成全部力学量纲，")
J.append("   而它们的数值全是测量输入 ⇒ **任何有量纲量的「本源」都不可能是产生式的**。")
J.append("3. **力学常数集的零空间为 0 维** ⇒ 不可能生成任何非平凡无量纲数 ⇒")
J.append("   **alpha 不可能是量纲层的产物**（第二条独立路径：螺旋扇区唯一的无量纲坐标是圆周角 theta，而 theta 不被任何方程固定）。")
J.append("")
J.append("于是「本源」问题被**路由**成三段：有量纲 → 必外输；无量纲连续 → 必外输；")
J.append("**无量纲离散（整数 / 拓扑 / 表示论）→ 唯一可能内生**。")
J.append("本库全部真成功（r67 的 U(1)、电荷量子化；r302 的三代、r305 的通量量子化）恰好都落在第三段，")
J.append("全部失败（alpha、质量、Lambda）恰好都落在前两段。**这不是巧合，是维数。**")
J.append("")
J.append("---")
J.append("")
J.append("## 一、T01 · 三本源量纲秩定理（本册承重之一）")
J.append("")
J.append("| 量 | (M, L, T, Q) |")
J.append("|---|---|")
J.append("| kappa | `%s` |" % dstr(DIM_KAPPA_L1))
J.append("| tau | `%s` |" % dstr(DIM_TAU_L1))
J.append("| omega | `%s` |" % dstr(DIM_OMEGA))
J.append("")
J.append("- 三个生成元中 kappa 与 tau **同维**（都是 L^-1）⇒ 张成格秩 = **%d**（不是 3）。" % rank_tri)
J.append("- 对 a,b,c 各取 [−5,5] 的 **%d** 组整数幂穷举，结果的 M 分量**恒为 0**（非零 %d 组）。" % (M_TOTAL, M_NONZERO))
J.append("- 求解 (0, −(a+b), −c) = (1, 0, 0) 得 `0 = 1`，**解集为空**。")
J.append("")
J.append("> **纪律说明**：这是「集合为空」级证明，不是「我搜索了 16807 组没找到」级证据。")
J.append("> 二者的差别在于：前者对任意更大的搜索空间永远成立，后者只是当时没找到。")
J.append("")
J.append("### T01b · 对公理 3 三口径歧义的免疫")
J.append("")
J.append("r174 A02/A03 记载同一符号 kappa 在三处权威来源里量纲互不相同，该冲突至今未仲裁。")
J.append("本册把三种读法都代进秩计算：")
J.append("")
J.append("| 口径 | 来源 | [kappa] | 格秩 | kappa 的 M 指数 |")
J.append("|---|---|---|---|---|")
for r in IMM:
    J.append("| %s | — | — | **%d** | %d |" % (r["口径"], r["rank"], r["M_exponent_of_kappa"]))
J.append("")
J.append("⇒ **三种读法下张成格秩都 ≤ 2、M 指数都为 0**，承重结论不依赖那个未解决的仲裁。")
J.append("这是本册唯一一处「对已知缺陷免疫」的稳健性结果。")
J.append("")
J.append("---")
J.append("")
J.append("## 二、T02 · 常数基定理与冗余恒等式定理")
J.append("")
J.append("以 (M,L,T) 为行、{c, hbar, G} 为列的 3x3 行列式 = **%s**（精确有理数，非浮点）。" % det3)
J.append("⇒ 秩 3 = 满秩 ⇒ **任何力学量都可唯一写成三常数的幂次组合**。这就是普朗克单位制的定理形式：")
J.append("量纲层的自由度只有 3。加入 e（Q 分量 1，其余 0）后秩升为 **%d**。" % rank_b4)
J.append("")
J.append("但**冗余**出现了：再把 m_P、l_P 加进来（它们本来就是 {c,hbar,G} 的函数），")
J.append("5 个常数在 3 维空间里必线性相关 ⇒ 零空间升为 **%d 维**，整数基为：" % len(ns5))
for iv in idn:
    J.append("")
    J.append("- 系数 `%s` ⇒ 单式数值 = `%s`（偏差 `%s`）" % (iv["exponents"], iv["value"], iv["dev"]))
J.append("")
J.append("两条基向量对应的正是**普朗克单位的定义式本身**（m_P·l_P = hbar/c 与 G·m_P = c^2·l_P）。")
J.append("⇒ **任何声称「由这批常数推出了一个新的无量纲数」的方案，其输出只可能等于 1。供给 0。**")
J.append("")
J.append("---")
J.append("")
J.append("## 三、T03 · 质量桥接：缺口是 1 维（theta），不是无穷维")
J.append("")
J.append("解 `a[kappa] + b[tau] + x[hbar] + y[c] = [M]`：")
J.append("")
J.append("```")
J.append(READINGS["mass_bridge_solution"])
J.append("```")
J.append("")
J.append("⇒ x = 1、y = −1 被钉死，只剩 `a + b = 1` 一维自由。任何「从螺旋导出质量」的式子必形如")
J.append("`m = (hbar/c) * kappa^a * tau^(1-a)`，**唯一自由度就是 kappa/tau 的分配比（即角度 theta）**。")
J.append("")
J.append("而 `m = hbar*omega/c^2` 与 `omega = m*c^2/hbar` 是同一式的双向重排（sympy 残差 `%s`）⇒" % res_id)
J.append("**「由螺旋频率导出质量」不携带任何信息，omega 就是 m 的改名**（与 r264 一致，本册给出指数层证明）。")
J.append("")
J.append("> **本册对本源问题唯一正面的产出**：缺口的形状是 **1 维**。")
J.append("> 要给出质量绝对值，只需补 **1 条独立的 theta 定值方程**（且该方程不得使用质量数据）。")
J.append("> 这比「我们还缺一整套理论」是一个可执行的 TODO，而不是一句安慰。")
J.append("")
J.append("---")
J.append("")
J.append("## 四、T04 · alpha 不可达定理（两条独立路径）")
J.append("")
J.append("**路径一（零空间 0 维）**：{c,hbar,G} 满秩 ⇒ 要求无量纲则指数向量在零空间内，")
J.append("而零空间为 **0 维** ⇒ 只有全零指数 ⇒ 结果恒等于 1。alpha = 7.2973525693e-3 ≠ 1，QED。")
J.append("")
J.append("**路径二（单位圆角度）**：螺旋扇区的两个无量纲量 `Pi1 = kappa*c/omega`、`Pi2 = tau*c/omega`")
J.append("在 `omega = c*sqrt(kappa^2+tau^2)` 下恒落单位圆（5 组样本最大残差 `%s`）。" % mp.nstr(maxres, 3))
J.append("⇒ 该扇区贡献的无量纲自由度是 1（圆周角），而 2 参数族被塌缩为 1 —— **与 r365 R16 的读数同构**，")
J.append("本册把它升级为「因此 alpha 不可达」的结论。")
J.append("")
J.append("两条路径的独立性很重要：路径一说明「搜不到」，路径二说明「搜到了也不是」。")
J.append("")
J.append("---")
J.append("")
J.append("## 五、T05 · 供给四机制（可执行谓词 + 四正对照）")
J.append("")
J.append("| 机制 | 判据 | 案例 | 该案例的供给 | 正对照（必须不触发） |")
J.append("|---|---|---|---|---|")
J.append("| M1 恒等复读 | 两式之差对任意参数恒为 0 | `G = c^4/(8 pi kappa)`，kappa 定义即该式 | 0 bit | 系数扰动 1e-4 后必须判非恒等 ✅ |")
J.append("| M2 参数转移 | 拟合后自由参数净增 ≥ 1 | KK 的 `alpha = 4(l_P/R)^2`，R 由 alpha 反解 | 0 bit，代价 +1 | 自由参数不增时必须判不触发 ✅ |")
J.append("| M3 定义域空 | 表达式量纲 ≠ 目标量纲 | `m_max = hbar/(2c sin^2 theta)` 量纲 %s ≠ M | 判据作废 | 量纲正确的 `hbar*omega/c^2` 必须不触发 ✅ |" % dstr(dim_mmax))
J.append("| M4 极限恒等 | 唯一有效极限下新增项一阶系数 → 0 | 自能修正 `1 + eps/4`，电子 eps/4 = %s | 不可观测 | 一阶系数非零时必须不触发 ✅ |" % mp.nstr(eps_e / 4, 6))
J.append("")
J.append("**四机制的来源归一**（本册只做归一，不重算既有条目）：")
J.append("M1 ← r42/r59 的恒等式复读与「函数形式锁定 ⇒ 系数不变性」；")
J.append("M2 ← r15/r67 的自由参数净增与 Omega5；")
J.append("M3 ← r44 的「二次映射无定义域」与 attack26 的 D-9「自毁式结论」；")
J.append("M4 ← r44 的「弱场极限守恒检验」。")
J.append("")
J.append("---")
J.append("")
J.append("## 六、十问定价表（对象 = 72 号本质本源审计卷的 10 问）")
J.append("")
J.append("| 问 | 对象 | 类型 | 需要什么 | 结构供给 | 数值供给 | 缺口 |")
J.append("|---|---|---|---|---|---|---|")
for r in TQ:
    J.append("| %s | %s | %s | %s | %d | **0** | %s |" % (r[0], r[1], r[2], r[3], r[4], r[5]))
J.append("")
J.append("**数值供给一栏全为 0**，与 r67 的 ENDO_NUM=0 同向；但本册不停在普查，")
J.append("而是给出「为什么必然为 0」的维数证明。**结构供给 %d 项**（电荷量子化 / 自旋表示 / 群选择）" % n_struct)
J.append("（紧致拓扑 U(1) 已计入「电荷量子化」那一行，不重复计数 —— 这正是条目可加性纪律：同一事实不得在两行各记一次。）")
J.append("全部属离散型 —— 正是路由定理允许的那一段。")
J.append("")
J.append("---")
J.append("")
J.append("## 七、路由三分定理（本册的可执行产出）")
J.append("")
J.append("```")
J.append("有量纲量          -> 必外输   （{c,hbar,G,e} 是基，数值全为测量）")
J.append("无量纲 连续量     -> 必外输   （零空间 0 维；或 1 维但随 theta 滑动）")
J.append("无量纲 离散量     -> 唯一可能内生（整数 / 拓扑 / 表示论）")
J.append("```")
J.append("")
J.append("**判读**：这不是「统一场论不可能」，而是「统一场论的**数值**产出只能来自离散结构」。")
J.append("本库已有的真成功全部落第三段，全部失败全部落前两段 —— 定理能**预判**哪类方向会有产出。")
J.append("")
J.append("---")
J.append("")
J.append("## 八、控制组（证明检测器有牙）")
J.append("")
J.append("| 码 | 名称 | 结果 | 读数 |")
J.append("|---|---|---|---|")
for x in CONTROLS:
    J.append("| %s | %s | %s | %s |" % (x["code"], x["name"], "OK" if x["ok"] else "FAIL", x["detail"]))
J.append("")
J.append("---")
J.append("")
J.append("## 九、守卫（%d/%d）" % (GUARD_OK, len(GUARDS)))
J.append("")
J.append("| 码 | 断言 | 结果 | 读数 |")
J.append("|---|---|---|---|")
for x in GUARDS:
    J.append("| %s | %s | %s | %s |" % (x["code"], x["name"], "OK" if x["ok"] else "FAIL", x["detail"]))
J.append("")
J.append("> G0-1..G0-8 是**量纲工具自身**的自检，全部前置于任何判定。")
J.append("> 本库已三次因量纲工具自身写错而把整册读数算错（dmul 写成逐分量相乘两次、massdim 写成 b+a+c 一次），")
J.append("> 故「工具先过守卫」是硬纪律，不是形式。")
J.append("")
J.append("---")
J.append("")
J.append("## 十、诚实边界（红线）")
J.append("")
J.append("1. **数学自洽 ≠ 物理证实**。本册是可算判决，**不产出新物理**，也不声称证明了「宇宙本源是什么」。")
J.append("2. **本册不否证几何纲领**。定理说的是「几何是本源的形式，不是本源的数值」，")
J.append("   而几何在定性结构（对称性 / 量子化 / 表示）上是唯一成功的部分 —— 这一点 r67 已单列。")
J.append("3. **本册不约束其他机制**。弦紧致化、渐近安全、因果集等不受本册结论约束，")
J.append("   因为它们未必把 {kappa,tau,omega} 当生成元。")
J.append("4. **分层纪律**：r67（经验普查 14 项）、r137（判据层审计）、r377（结构定理）三册并存，")
J.append("   **条目不可相加**，判词方向一致而论证层次不同。")
J.append("5. **未做**：本册没有解出 theta 定值方程（那需要新物理输入），只证明了它「是 1 个方程的事」。")
J.append("   把「1 维缺口」说成「已解决」是越界。")
J.append("")
J.append("---")
J.append("")
J.append("## 十一、自伤登记（本册自己抓到的错，就地更正而非追加）")
J.append("")
J.append("1. **补偿性双错（最值得记的一条）**：首版把 `eps0` 的 T 指数写成 `+4`、把 `mu0` 的 T 指数写成 `-2`。")
J.append("   二者相加恰好仍是 `+2`，于是 `G0-4`（`eps0*mu0*c^2 = 1`）**静默通过**；")
J.append("   只有 `G0-7`（`e^2/(4 pi eps0 hbar c)` 应无量纲）报出 `T^-2` 才暴露。")
J.append("   ⇒ 单点锚 `G0-4b/G0-4c` 是为此补的：**组合式守卫会被互相补偿的双错绕过，必须同时有单点锚**。")
J.append("   这与本库既有纪律「量纲类断言必须机器兜底」是同一件事的两面。")
J.append("2. **`G()` 返回 bool 被当成 dict**：首版写 `all(x['ok'] for x in g0)`，`TypeError: 'bool' object is not subscriptable`。")
J.append("   一分钟级修复，但说明「输出器返回什么」这类契约在长脚本里同样需要一次断言。")
J.append("3. **十问结构供给计数**：初稿正文写「4 项」而表里只有 3 行 `>0`。")
J.append("   根因是把「紧致拓扑 U(1)」与「电荷量子化」当成两项 —— 它们是同一事实的两面，")
J.append("   **重复计数正是条目可加性纪律要禁止的**。已改为 3 项并显式写明去重理由。")
J.append("")
J.append("---")
J.append("")
J.append("## 十二、产物真链接")
J.append("")
J.append("- 引擎：`../源码/TUFT-%s_本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_精算与可视化_%s.py`" % (RID, STAMP))
J.append("- 数据：`TUFT-%s_本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_%s.json` / `.md` / `_report.txt`" % (RID, STAMP))
J.append("- 可视化：`本源层总账_量纲秩与供给路由_可视化_r377.html`")
J.append("- 上游：`../判定_TUFT-r67-力统一场论本源性审计_内生外输普查与GR正对照_2026-10-31.md`、")
J.append("  `../判定_TUFT-r174-三本源公理闭合审计_2026-10-24.md`、")
J.append("  `../判定_TUFT-r365_ROOTV26空间光速螺旋全参数审计_三维四维Frenet独立重算与螺旋角自由度定理与alpha输入定价_精算与可视化_2026-11-02.md`")
J.append("")
J.append("**下轮从 r378 起。**")
J.append("")
with io.open(P_JUD, "w", encoding="utf-8") as f:
    f.write("\n".join(J) + "\n")

# ============================================================================
# §14 · 可视化（自含 SVG）
# ============================================================================
def bar_rect(x, y, w, h, fill):
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>"
            % (x, y, w, h, fill))


rank_bars = [("k,t,w", rank_tri, 3), ("c,h,G", rank_b3, 3), ("c,h,G,e", rank_b4, 4)]
G1 = []
for i, (nm, r, cap) in enumerate(rank_bars):
    h = 150.0 * r / 4.0
    x = 70 + i * 160
    G1.append(bar_rect(x, 190 - h, 90, h, "#2b7bb9" if r == cap else "#c0392b"))
    G1.append("<text x='%.1f' y='210' font-size='12'>%s</text>" % (x + 10, nm))
    G1.append("<text x='%.1f' y='%.1f' font-size='13'>%d</text>" % (x + 38, 185 - h, r))
G1.append("<text x='70' y='30' font-size='13'>张成格秩（上限 4）</text>")

TQ_BARS = []
for i, r in enumerate(TQ):
    h = 22.0 * r[4]
    x = 45 + i * 60
    TQ_BARS.append(bar_rect(x, 170 - h, 36, max(h, 2), "#27ae60" if r[4] > 0 else "#bdc3c7"))
    TQ_BARS.append("<text x='%.1f' y='188' font-size='10'>%s</text>" % (x + 2, r[0]))
    TQ_BARS.append("<text x='%.1f' y='%.1f' font-size='11'>%d</text>" % (x + 14, 165 - h, r[4]))

QROWS = "".join(
    "<tr><td>%s</td><td>%s</td><td>%d</td><td>0</td><td>%s</td></tr>" % (r[0], r[2], r[4], r[5])
    for r in TQ)

HTML = """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>TUFT-@RID@ 本源层总账</title>
<style>
body{font-family:system-ui,sans-serif;background:#f7f8fa;margin:18px;color:#222}
h1{font-size:18px}h2{font-size:15px;margin-top:22px}
svg{background:#fff;border:1px solid #ccc;display:block;margin:8px 0}
table{border-collapse:collapse;font-size:12px;margin-top:6px}
td,th{border:1px solid #999;padding:3px 8px}
code{background:#eee;padding:1px 4px}
</style></head><body>
<h1>TUFT-@RID@ · 本源层总账 · @STAMP@</h1>
<div>判词 <b>@VERDICT@</b>；终态 <b>@FINAL@</b></div>
<div>条目 @NITEMS@｜守卫 @GUARDS@｜控制组 @CTRLS@</div>

<h2>图 1 · 张成格秩：三本源退化为 2，力学常数满秩</h2>
<svg viewBox="0 0 560 240">@G1@</svg>
<div><code>{kappa,tau,omega} 秩 = @RT@（kappa 与 tau 同维，退化为 2 而非 3）</code><br/>
<code>{c,hbar,G} det = @DET@ ⇒ 满秩 3</code></div>

<h2>图 2 · 十问的「结构供给」与「数值供给」</h2>
<svg viewBox="0 0 660 210">@G2@</svg>
<div>绿柱 = 结构供给（离散型，路由定理允许的那一段）；灰柱 = 0。<b>数值供给十问全为 0</b>。</div>

<h2>表 · 十问定价</h2>
<table><tr><th>问</th><th>类型</th><th>结构供给</th><th>数值供给</th><th>缺口</th></tr>@QROWS@</table>

<h2>路由三分定理</h2>
<table>
<tr><th>量的类别</th><th>能否内生</th><th>本册依据</th></tr>
<tr><td>有量纲量</td><td>否（必外输）</td><td>{c,hbar,G,e} 是量纲基，数值全为测量</td></tr>
<tr><td>无量纲 连续量</td><td>否（必外输）</td><td>零空间 0 维；或 1 维但随 theta 滑动</td></tr>
<tr><td>无量纲 离散量</td><td><b>唯一可能</b></td><td>整数 / 拓扑 / 表示论不受维度分析限制</td></tr>
</table>

<h2>供给四机制</h2>
<table>
<tr><th>机制</th><th>判据</th><th>案例供给</th></tr>
<tr><td>M1 恒等复读</td><td>两式之差的 symbolic simplify = 0</td><td>0 bit</td></tr>
<tr><td>M2 参数转移</td><td>拟合后自由参数净增 ≥ 1</td><td>0 bit，代价 +1</td></tr>
<tr><td>M3 定义域空</td><td>表达式量纲 ≠ 目标量纲</td><td>判据作废</td></tr>
<tr><td>M4 极限恒等</td><td>有效极限下新增项一阶系数 → 0</td><td>不可观测</td></tr>
</table>

<h2>关键读数</h2>
<table>
<tr><td>M 分量非零组数</td><td>@MNZ@ / @MTOT@</td></tr>
<tr><td>零空间维数 {c,hbar,G,mP,lP}</td><td>@NS5@</td></tr>
<tr><td>单位圆残差最大值</td><td>@CIRC@</td></tr>
<tr><td>质量桥接自由度</td><td>1（theta）</td></tr>
<tr><td>alpha 供给</td><td>0</td></tr>
</table>

<div style="margin-top:18px;font-size:12px;color:#666">
数学自洽 ≠ 物理证实。本册不否证几何纲领，只给出其作用域边界：<b>几何是本源的「形式」，不是本源的「数值」</b>。
</div>
</body></html>
"""

HTML = HTML.replace("@RID@", RID).replace("@STAMP@", STAMP)
HTML = HTML.replace("@VERDICT@", VERDICT).replace("@FINAL@", FINAL)
HTML = HTML.replace("@NITEMS@", str(len(ITEMS)))
HTML = HTML.replace("@GUARDS@", "%d/%d" % (GUARD_OK, len(GUARDS)))
HTML = HTML.replace("@CTRLS@", "%d/%d" % (CTRL_OK, len(CONTROLS)))
HTML = HTML.replace("@G1@", "".join(G1))
HTML = HTML.replace("@G2@", "".join(TQ_BARS))
HTML = HTML.replace("@QROWS@", QROWS)
HTML = HTML.replace("@RT@", str(rank_tri))
HTML = HTML.replace("@DET@", str(det3))
HTML = HTML.replace("@MNZ@", str(M_NONZERO)).replace("@MTOT@", str(M_TOTAL))
HTML = HTML.replace("@NS5@", str(len(ns5)))
HTML = HTML.replace("@CIRC@", mp.nstr(maxres, 6))
with io.open(P_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)

# ============================================================================
# §15 · 收口
# ============================================================================
print("SUMMARY:", json.dumps(SUMMARY, ensure_ascii=False))
print("FINAL =", FINAL)
for pth in (P_JSON, P_MD, P_REP, P_JUD, P_HTML):
    print("WROTE", os.path.basename(pth), os.path.getsize(pth))
sys.exit(0 if ALL_OK else 1)
