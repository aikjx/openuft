# -*- coding: utf-8 -*-
"""ROOT V60 独立复算：群分解 / 迹恒等式 / 反常账 / 四维零模计数 / 尺度换算。

原则：不抄来料公式，用 SO(12) 的权向量从零枚举，再与来料的断言比对。
  A 层（Fraction 精确）：66 与 32 的分解、tr F^2 / tr F^4 恒等式、试验谱反常账、
                        四维三反常的第三条独立路径、V60-7 与 V60-8 的关系
  B 层（Decimal）     ：R 与 M_6 的尺度换算、I_8 交叉项系数的口径差
  C 层（判定）        ：六维为零 != 四维为零、三代仍为输入、引力不在规范群内
纪律：条目不可相加；纯陈述给 INFO；判据由报价/定义推导，不用任意 10 的幂。
"""
import os
import io
import json
from itertools import combinations, product
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 50

TITLE = "ROOT V60 独立复算"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-10s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def sci(x, nd=10):
    x = D(x)
    if x == 0:
        return "0"
    sgn = "-" if x < 0 else ""
    ax = abs(x)
    e = 0
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%s%sE%+04d" % (sgn, format(ax, ".%df" % (nd - 1)), e)


# ================================================================ SO(12) 权结构
# 12 维矢量的 12 个权：第 a 个坐标 -> Cartan 指标 i=(a+1)//2、符号 [+1,-1]
# U(1)_F 荷：a<=10 为 0；a=11 为 +2；a=12 为 -2（与 V60 的 10_{+2} 归一化一致）
def vec_weights():
    out = []
    for a in range(1, 13):
        i = (a + 1) // 2 - 1
        s = F(1) if a % 2 == 1 else F(-1)
        q = F(0) if a <= 10 else (F(2) if a == 11 else F(-2))
        out.append((i, s, q, a))
    return out


def dot(w, H):
    """w 是 6 维 Cartan 坐标的稀疏权 (i,s) 列表"""
    return sum(s * H[i] for i, s in w)


VW = vec_weights()
CART = [(i, s) for (i, s, q, a) in VW]          # 12 个矢量权（稀疏）
Q_OF = [q for (i, s, q, a) in VW]

# Lambda^2 的 66 个权：取 a<b，权 = e_a + e_b（同 Cartan 时抵消为 0）
LAM2 = []
for a, b in combinations(range(12), 2):
    i1, s1 = CART[a]
    i2, s2 = CART[b]
    w = []
    if i1 == i2:
        pass                                     # s1+s2 = 0，零权
    else:
        w = [(i1, s1), (i2, s2)]
    q = Q_OF[a] + Q_OF[b]
    LAM2.append((w, q, a, b))

# 32 维旋量（even 手征）：6 个 +-1/2，符号乘积 = +1
SPIN = []
for s in product((1, -1), repeat=6):
    if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] != 1:
        continue
    w = [(i, F(s[i], 2)) for i in range(6)]
    q = F(s[5], 2) * 2                            # 第 6 个 Cartan = U(1)_F，归一化 x2
    SPIN.append((w, q, s))

print("=" * 78)
print(TITLE)
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = 0")
guard("DIM-66", len(LAM2) == 66, "Lambda^2(12) 维数 = %d" % len(LAM2))
guard("DIM-32", len(SPIN) == 32, "even 旋量维数 = %d" % len(SPIN))
_H = [F(1, 3), F(-2, 5), F(3, 7), F(1, 11), F(-2, 13), F(5, 17)]
_t12 = sum(dot([w], _H) ** 2 for w in [(i, s) for (i, s, q, a) in VW])
guard("TR-VEC", _t12 == 2 * sum(x * x for x in _H),
      "tr_12 F^2 = 2*sum H^2 : %s vs %s" % (_t12, 2 * sum(x * x for x in _H)))

# ================================================================ A 层
print("\n[A] 精确群论：分解 / 迹恒等式 / 反常账")

# A01  66 = 45_0 + 1_0 + 10_{+2} + 10_{-2}
cls = {}
for (w, q, a, b) in LAM2:
    so10_part = 2 if min(a, b) <= 9 else (1 if a <= 9 else 0)   # 0-indexed: a,b in 0..11
    cls[q] = cls.get(q, 0) + 1
n45 = sum(1 for (w, q, a, b) in LAM2 if a <= 9 and b <= 9)
n10p = sum(1 for (w, q, a, b) in LAM2 if a <= 9 and b == 10)
n10m = sum(1 for (w, q, a, b) in LAM2 if a <= 9 and b == 11)
n1 = sum(1 for (w, q, a, b) in LAM2 if a == 10 and b == 11)
add("A01", "A", "66 = 45_0 + 1_0 + 10_{+2} + 10_{-2}：按 (SO(10) 指标, U(1)_F 荷) 枚举 Lambda^2(12)",
    "(45, 10, 10, 1)", "(45,10,10,1) = (%d,%d,%d,%d) ; 荷分组 %s"
    % (n45, n10p, n10m, n1, sorted(cls.items())),
    (n45, n10p, n10m, n1) == (45, 10, 10, 1) and n45 + n10p + n10m + n1 == 66,
    "⇒ V60-1 精确成立；10_{-2} 确实在 Spin(12) 的伴随里（V59 的缺口被补上）")

# A02  32 = 16_{+1} + 16bar_{-1}
n16 = sum(1 for (w, q, s) in SPIN if s[5] == 1)
n16b = sum(1 for (w, q, s) in SPIN if s[5] == -1)
add("A02", "A", "32 = 16_{+1} + 16bar_{-1}：even 手征旋量按第 6 个 Cartan 的荷分组",
    "(16, 16) 且荷为 (+1, -1)",
    "(16,16) = (%d,%d) ; 荷集合 %s" % (n16, n16b, sorted(set(q for (w, q, s) in SPIN))),
    n16 == 16 and n16b == 16 and n16 + n16b == 32,
    "⇒ V60-2 精确成立")

# A03  tr_32 F^2 = 4 tr_12 F^2
wA03 = F(0)
for H in ([F(1, 3), F(-2, 5), F(3, 7), F(1, 11), F(-2, 13), F(5, 17)],
          [F(2), F(-1), F(5), F(3), F(-4), F(7)],
          [F(1, 2), F(1, 3), F(1, 5), F(1, 7), F(1, 11), F(1, 13)]):
    t32 = sum(dot(w, H) ** 2 for (w, q, s) in SPIN)
    t12 = sum(dot([(i, sg)], H) ** 2 for (i, sg, q, a) in VW)
    wA03 = max(wA03, abs(t32 - 4 * t12))
add("A03", "A", "tr_32 F^2 = 4 tr_12 F^2：32 个旋量权与 12 个矢量权各自求和（3 组有理 H）",
    "4", "max|tr_32F^2 - 4tr_12F^2| = %s" % wA03, wA03 == 0,
    "⇒ V60-3 精确成立；比值 4 = 2^{n-4}（n=6）")

# A04  tr_32 F^4 = -2 tr_12 F^4 + (3/2)(tr_12 F^2)^2
wA04 = F(0)
for H in ([F(1, 3), F(-2, 5), F(3, 7), F(1, 11), F(-2, 13), F(5, 17)],
          [F(2), F(-1), F(5), F(3), F(-4), F(7)],
          [F(1, 2), F(1, 3), F(1, 5), F(1, 7), F(1, 11), F(1, 13)]):
    t32_4 = sum(dot(w, H) ** 4 for (w, q, s) in SPIN)
    t12_4 = sum(dot([(i, sg)], H) ** 4 for (i, sg, q, a) in VW)
    t12_2 = sum(dot([(i, sg)], H) ** 2 for (i, sg, q, a) in VW)
    wA04 = max(wA04, abs(t32_4 - (-2 * t12_4 + F(3, 2) * t12_2 * t12_2)))
add("A04", "A", "tr_32 F^4 = -2 tr_12 F^4 + (3/2)(tr_12 F^2)^2：64 个旋量权直接四次求和（3 组有理 H）",
    "残差 0（-2 与 3/2 为来料系数）", "max|残差| = %s" % wA04, wA04 == 0,
    "⇒ V60-4 精确成立；不可约四次系数 -2 非零（这是后面要走 GS 的根）")

# A05  试验谱 32_+ + 2*12_+ + 56*1_-
irr4 = -2 + 2 * (1) + 56 * 0            # tr F^4 型的不可约系数：32->-2, 12->+1, 单态->0
grav = 32 + 2 * 12 - 56                 # 纯引力：手征维数带符号
add("A05", "A", "试验谱 32_+ + 2*12_+ + 56*1_-：不可约四次反常 -2+2*1 = 0、纯引力 32+24-56 = 0",
    "0 与 0", "四次 = %d ; 纯引力 = %d" % (irr4, grav), irr4 == 0 and grav == 0,
    "⇒ V60-5 的两条账都对；注意单态对四次项贡献 0（tr F^4=0），只对手征维数有贡献")

# A06-A08  四维三反常的第三条路径（指标定理 + 表示指标，不抄来料计数表）
# 零模：32 给 3 套 16_{+1}（左）+ 3 套 16bar_{-1}（右）；每个 12 给 |q|*N = 6 个 1_{+-2}
N_FLUX = 3
n16c = 3
n12c = 6                                # 每个 12 的 1_{+2} 零模数 = q*N = 2*3
# U(1)^3 : 左手 q^3 求和（右手记负）
u3 = n16c * 16 * (+1) ** 3 + (-1) * n16c * 16 * (-1) ** 3
u3 += 2 * (n12c * (+2) ** 3) + 2 * (-1) * (n12c * (-2) ** 3)
add("A06", "A", "四维 U(1)_F^3 = 288：用指标定理给 12 的零模数（|q|N=6）独立求和，不抄来料计数表",
    "288", "%d" % u3, u3 == 288,
    "⇒ 与 V60 的 288 一致；这一路只依赖「32 给 3+3 套」这条输入")

# SO(10)^2 U(1) : T(16)=2（T(10)=1 归一）
T16, T10 = F(2), F(1)
s2u1 = n16c * T16 * (+1) + (-1) * n16c * T16 * (-1)
add("A07", "A", "四维 SO(10)^2 U(1)_F = 12：T(16)=2（T(10)=1），3 套左 + 3 套右手",
    "12", "%d" % s2u1, s2u1 == 12,
    "⇒ 与 V60 的 12 一致")

# grav^2 - U(1) : dim 加权
g2u1 = n16c * 16 * (+1) + (-1) * n16c * 16 * (-1)
g2u1 += 2 * (n12c * (+2)) + 2 * (-1) * (n12c * (-2))
add("A08", "A", "四维 grav^2-U(1)_F = 144：维数加权（16 与单态）",
    "144", "%d" % g2u1, g2u1 == 144,
    "⇒ 与 V60 的 144 一致；三个数全部复现 ⇒ 第四节的一致性检验是真检验")

# A09  V60-8 = N * (V60-7 括号)
okA09 = (48 == N_FLUX * 16) and (6 == N_FLUX * 2) and (-6 == N_FLUX * (-2))
add("A09", "A", "(V60-8) 就是 (V60-7) 在 N=3 的代入：48=3*16、6=3*2、-6=3*(-2)",
    "三对系数全成比例", "48/16=%s 6/2=%s -6/-2=%s" % (48 / 16, 6 / 2, -6 / -2), okA09,
    "⇒ 两式不是两个独立结果；独立性只在 288/12/144 vs 48/6/6 那一步（A06-A08）")

# A10  A04 的第三条路径：逐单项式（不是取点）验证，给出闭式
def _pmul(p, q):
    out = {}
    for (a1, b1), c1 in p.items():
        for (a2, b2), c2 in q.items():
            k = (a1 + a2, b1 + b2)
            out[k] = out.get(k, F(0)) + c1 * c2
    return dict((k, v) for (k, v) in out.items() if v != 0)


def _padd(p, q):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, F(0)) + c
    return dict((k, v) for (k, v) in out.items() if v != 0)


def _ppow(p, n):
    r = {(0, 0): F(1)}
    for _ in range(n):
        r = _pmul(r, p)
    return r


badA10, c4, c22, n_odd = [], set(), set(), 0
for i in range(6):
    for j in range(i + 1, 6):
        t32 = {}
        for (w, q, s) in SPIN:
            t32 = _padd(t32, _ppow({(1, 0): w[i][1], (0, 1): w[j][1]}, 4))
        t12_2, t12_4 = {}, {}
        for (idx, sg, q, a) in VW:
            lin = {(1, 0): F(sg)} if idx == i else ({(0, 1): F(sg)} if idx == j else None)
            if lin is None:
                continue
            t12_2 = _padd(t12_2, _ppow(lin, 2))
            t12_4 = _padd(t12_4, _ppow(lin, 4))
        rhs = _padd(dict((k, -2 * v) for (k, v) in t12_4.items()),
                    dict((k, F(3, 2) * v) for (k, v) in _pmul(t12_2, t12_2).items()))
        if _padd(t32, dict((k, -v) for (k, v) in rhs.items())):
            badA10.append((i, j))
        c4.add(t32.get((4, 0), F(0)))
        c22.add(t32.get((2, 2), F(0)))
        if t32.get((3, 1), F(0)) != 0:
            n_odd += 1
add("A10", "A", "闭式 tr_32 F^4 = 2*sum H^4 + 12*sum_{i<j} H^2H^2：15 对 Cartan 上逐单项式相消（全 Fraction 多项式）",
    "t^4 系数 {2}、t^2s^2 系数 {12}、t^3s 系数 0、残差为空",
    "t^4 %s ; t^2s^2 %s ; t^3s 非零对数 %d ; 残差非空对数 %d / 15"
    % (sorted(c4), sorted(c22), n_odd, len(badA10)),
    (not badA10) and c4 == set([F(2)]) and c22 == set([F(12)]) and n_odd == 0,
    "⇒ V60-4 的第三条路径：不是取三点，而是逐单项式相消 ⇒ -2 与 3/2 不是拟合出来的；同时给出闭式")

# A11  另一手征旋量 32'（odd 符号积）的迹：是否与 32 同值（决定「迹恒等式能否定手征」）
SPIN_ODD = []
for s in product((1, -1), repeat=6):
    if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] != -1:
        continue
    w = [(i, F(s[i], 2)) for i in range(6)]
    SPIN_ODD.append((w, F(s[5], 2) * 2, s))
d2, d4, same_form = F(0), F(0), True
for H in ([F(1, 3), F(-2, 5), F(3, 7), F(1, 11), F(-2, 13), F(5, 17)],
          [F(2), F(-1), F(5), F(3), F(-4), F(7)],
          [F(1, 2), F(1, 3), F(1, 5), F(1, 7), F(1, 11), F(1, 13)]):
    a2 = sum(dot(w, H) ** 2 for (w, q, s) in SPIN)
    b2 = sum(dot(w, H) ** 2 for (w, q, s) in SPIN_ODD)
    a4 = sum(dot(w, H) ** 4 for (w, q, s) in SPIN)
    b4 = sum(dot(w, H) ** 4 for (w, q, s) in SPIN_ODD)
    d2 = max(d2, abs(a2 - b2))
    d4 = max(d4, abs(a4 - b4))
    t12_4 = sum(dot([(i, sg)], H) ** 4 for (i, sg, q, a) in VW)
    t12_2 = sum(dot([(i, sg)], H) ** 2 for (i, sg, q, a) in VW)
    same_form = same_form and (b4 == -2 * t12_4 + F(3, 2) * t12_2 * t12_2)
add("A11", "A", "32' 与 32 的两条迹完全相同（32' = 32 经 H_6 -> -H_6），故迹恒等式对手征不敏感",
    "max|tr32'F^2 - tr32F^2| = 0 且 max|tr32'F^4 - tr32F^4| = 0",
    "dim2 %d/%d ; 差 %s 与 %s ; 32' 是否满足同一恒等式 %s"
    % (len(SPIN), len(SPIN_ODD), d2, d4, same_form),
    (d2 == 0 and d4 == 0 and same_form and len(SPIN_ODD) == 32),
    "⇒ 迹恒等式里没有手征信息；V60-5 的 +- 号来自外手征（Weyl 投影），是外部输入"
      " ⇒ 手征是此处唯一决定归零成败的输入，却不能由本框架选出")

# ================================================================ B 层
print("\n[B] 数值：尺度换算与口径")

HC = D("0.1973269804")            # GeV*fm
GEV_INV_M = D(1) / (HC * D("1e-15"))     # 1 GeV^-1 对应多少米
R_GEV = D(2).sqrt() * HC / D("10000")    # 10 TeV 第一非零球面模：m = sqrt2/R
R_M = R_GEV * D("1e-15")
add("B01", "B", "第一中性球面 KK 模 10 TeV（l=1，m=sqrt2/R）⇒ R = sqrt2*hbar*c/(10 TeV)",
    "2.79E-020 m", "%s m" % sci(R_M, 6), abs(R_M - D("2.79e-20")) < D("0.005e-20"),
    "用到的约定：S^2 上 l=1 的 m^2 = l(l+1)/R^2 = 2/R^2；若改用 1/R 则为 1.97E-020 m")

R_gi = R_M / (HC * D("1e-15"))           # R in GeV^-1
VOL = 4 * D("3.14159265358979323846264338327950288419716939937510") * R_gi * R_gi
MPL_RED = D("2.4353e18")                  # reduced Planck / GeV
M6 = (MPL_RED * MPL_RED / VOL) ** D("0.25")
MPL_FULL = D("1.220910e19")
M6_full = (MPL_FULL * MPL_FULL / VOL) ** D("0.25")
add("B02", "B", "M_6 由 M_Pl^2 = M_6^4 * Vol(S^2) 反解（Vol=4*pi*R^2）",
    "6.97E+010 GeV（reduced Planck）", "%s GeV ; 用全 Planck 则 %s GeV（因子 %s）"
    % (sci(M6, 6), sci(M6_full, 6), sci(M6_full / M6, 4)),
    abs(M6 - D("6.97e10")) / D("6.97e10") < D("0.01"),
    "⇒ 与来料一致；但 2.4 倍的约定差必须写出来 —— 这个「条件性尺度」不是唯一的")

# B03  I_8 交叉项系数的口径差
# 标准 Â(T)ch(E)：交叉项 = Ahat_4 * ch_4 = (-p1/24)*(T2/2) = -T2*p1/48
standard = F(-1, 48)
v60_coef = F(-2, 16)                     # (1/16)T2*(T2-2p1) 的交叉项 = -2/16
add("B03", "B", "I_8 的交叉项系数：标准 (-p1/24)(T2/2) = -1/48，来料给 -2/16 = -1/8",
    "-1/48（标准 Â*ch 展开）", "来料 %s ; 标准 %s ; 比值 %s"
    % (v60_coef, standard, v60_coef / standard), None,
    "差 6 倍 = 3!，符合 p1 与 tr R^2 的常见归一化差；V60 未写死 ch 与 Â 的归一化 ⇒ 该系数不可独立核（记 INFO 而非 FAIL）")

# B04  零模数约定的敏感性：|qN| vs |qN|+1
sc = F(4, 3)        # 每个 16 的零模数 3 -> 4
sc2 = F(7, 6)       # 每个 12 的单态零模数 6 -> 7
u3_p = sc * n16c * 16 * (+1) ** 3 + sc * (-1) * n16c * 16 * (-1) ** 3
u3_p += 2 * (sc2 * n12c * (+2) ** 3) + 2 * (-1) * (sc2 * n12c * (-2) ** 3)
s2_p = sc * n16c * T16 * (+1) + sc * (-1) * n16c * T16 * (-1)
g2_p = sc * n16c * 16 * (+1) + sc * (-1) * n16c * 16 * (-1)
g2_p += 2 * (sc2 * n12c * (+2)) + 2 * (-1) * (sc2 * n12c * (-2))
add("B04", "B", "四维三反常对零模数约定敏感：|qN| 给 288/12/144，|qN|+1 给另一组",
    "288 / 12 / 144（|qN|）", "%d / %d / %d（|qN|+1）; 比值 %s"
    % (u3_p, int(s2_p), int(g2_p), [str(F(u3_p, u3)), str(F(s2_p, s2u1)), str(F(g2_p, g2u1))]), None,
    "⇒ 非零性在两套约定下都不变（结论稳健），但三个具体数不是唯一预言；"
    "本册凡引 288/12/144 必同时注明约定 = |qN|")

# ================================================================ C 层
print("\n[C] 判定")

add("C01", "C", "六维不可约反常为零 != 四维反常为零：288 / 12 / 144 三者全非零",
    "四维应全为 0 才算抵消", "288 / 12 / 144（来料与 A06-A08 一致）", False,
    "⇒ 试验谱在四维是反常的，必须靠 GS；V60 自己写了这一点，本册确认")

add("C02", "C", "三代仍为输入：N=3 是手放的磁通，不是被理论选出的",
    "应内生", "N=3 手放；r350 已证框架不预言 3（0/13）", False,
    "⇒ 与 V50/V59 同一条缺口，本轮未变")

add("C03", "C", "Spin(12) 把自旋 2 包含进同一规范作用", "应包含",
    "不包含：引力仍有独立耦合尺度 M_6", False,
    "⇒ 四力唯一本源未证明；V60 自己在第五节写了这句，本册确认")

add("C04", "C", "32 的磁通只留下三套物质表示", "应恰好 3 套",
    "3 套 16_{+1} + 3 套 16bar_{-1}，共 6 套", False,
    "⇒ 额外零模未消除；需要边界投影或质量配对，V60 列为 V61 任务 1")

add("C05", "C", "来料 20/20 项核验可独立复核", "应给清单",
    "未给逐项清单（只给分类表）", None,
    "⇒ 只能逐类复算，不能对拍 20 这个数；本册逐条替代之（不追 20 这个计数）")

# C06  来料自身两组四维反常读数（V60-7 的 16/2/-2 与 288/12/144）能否共存
per_gen = (16, 2, 16)       # 单个 16_{+1}：(dim*q^3, T(16)*q, dim*q)
v60_7 = (16, 2, -2)
r1, r2, r3 = F(288, 48), F(12, 6), F(144, -6)
okC06 = (r1 == r2 == r3) and (v60_7[2] == per_gen[2])
add("C06", "C", "（V60-7）的 16 / 2 / -2 是同一个 16_{+1} 的三项，且与 288/12/144 只差统一归一化",
    "第三项应为 dim(16)*q = 16；两组比值应全等",
    "第三项给 -2（需 dim*q = -2 ⇒ 只有 dim=1,q=-2 的单态满足，16 给不出）；"
    "比值 288/48 = %s, 12/6 = %s, 144/(-6) = %s" % (r1, r2, r3), okC06,
    "⇒ 同一行三项来自两个不同谱（前两项=一个 16，第三项=一个 q=-2 单态）；"
    "两组四维读数比值 6/2/-24 互不相等 ⇒ 不能靠统一归一化调和，是内部张力而非口径差")

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("V60_REP_GAP_REPAIRED_66_SUPSET_10_MINUS2_OK__TRACE_IDENTITIES_CLOSED_FORM_OK__CHIRALITY_BLIND_OK__"
        "TRIAL_SPECTRUM_IRRE4_AND_GRAV_CANCEL_OK__FOUR_DIM_ANOMALIES_288_12_144_INDEPENDENTLY_REPRODUCED_OK__"
        "SIX_DIM_ZERO_NEQ_FOUR_DIM_ZERO_FAIL__EXTRA_ZEROMODES_3_PLUS_3_FAIL__"
        "SPIN12_DOES_NOT_CONTAIN_SPIN2_FAIL__GENERATION_NUMBER_STILL_INPUT_FAIL__"
        "V60_7_THREE_TERMS_MIX_TWO_SPECTRA_FAIL__NO_NEW_PROCESSING_LOGIC__UNIQUE_PREDICTION_0")

out = {"title": TITLE, "date": "2026-11-04", "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "decomp_66": [n45, n10p, n10m, n1],
           "decomp_32": [n16, n16b],
           "anom_4d": [u3, int(s2u1), int(g2u1)],
           "R_m": sci(R_M, 8),
           "M6_reduced": sci(M6, 8),
           "M6_full": sci(M6_full, 8),
           "M6_ratio": sci(M6_full / M6, 4),
           "closed_form_tr4": {"t4": str(sorted(c4)[0]) if len(c4) == 1 else sorted(map(str, c4)),
                               "t2s2": str(sorted(c22)[0]) if len(c22) == 1 else sorted(map(str, c22)),
                               "odd_terms_nonzero": n_odd,
                               "residual_pairs": len(badA10)},
           "ratio_two_4d_triples": [str(r1), str(r2), str(r3)],
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_ROOTV60_recompute_2026-11-04.json")
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  复算报告  2026-11-04" % TITLE)
L.append("=" * 78)
L.append("判词：%s" % VERD)
L.append("")
for r in ROWS:
    L.append("%-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("       exp = %s" % r["exp"])
    L.append("       act = %s" % r["act"])
    if r["note"]:
        L.append("       note= %s" % r["note"])
L.append("")
L.append("守卫 %d/%d" % (gok, len(GUARDS)))
for g in GUARDS:
    L.append("  %-12s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
rp = os.path.join(DATA, "_ROOTV60_recompute_report_2026-11-04.txt")
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")

print("\nwritten:\n  %s\n  %s" % (os.path.basename(jp), os.path.basename(rp)))
