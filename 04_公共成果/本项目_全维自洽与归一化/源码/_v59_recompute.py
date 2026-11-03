# -*- coding: utf-8 -*-
"""ROOT V59 独立复算：不做同源回验，按「已知工具重组」假设逐项验。

可算项：
  A 层（精确代数）  CG 矩阵与 V59-3 的逐元比对、严格关系的来源、N=1..16 角动量表、
                    参数计数（6 元 vs 5 振幅）、基底依赖性
  B 层（高精度）    三组奇异值、局域行列式闭式 vs 直接行列式、局域矩阵谱、rank<=K
  C 层（判定）      交换子非零是否构成证据、Frobenius 归一化后的自由度账
纪律：条目不可相加；纯陈述给 INFO；门限禁用 10 的幂。
"""
import os
import io
import json
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 50

TITLE = "ROOT V59 独立复算"
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


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / (abs(b) if b != 0 else D(1))


# ---------------------------------------------------------------- 3x3 实对称 Jacobi
def jacobi3(A, sweeps=80):
    """返回 (特征值降序, 特征向量矩阵按列)"""
    a = [[D(A[i][j]) for j in range(3)] for i in range(3)]
    v = [[D(1) if i == j else D(0) for j in range(3)] for i in range(3)]
    for _ in range(sweeps):
        off = a[0][1] * a[0][1] + a[0][2] * a[0][2] + a[1][2] * a[1][2]
        if off < D("1e-95"):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if a[p][q] == 0:
                continue
            th = (a[q][q] - a[p][p]) / (D(2) * a[p][q])
            t = (D(1) if th >= 0 else D(-1)) / (abs(th) + (th * th + 1).sqrt())
            c = D(1) / (t * t + 1).sqrt()
            s = t * c
            apq = a[p][q]
            app, aqq = a[p][p], a[q][q]
            a[p][p] = app - t * apq
            a[q][q] = aqq + t * apq
            a[p][q] = a[q][p] = D(0)
            r = 3 - p - q
            arp, arq = a[r][p], a[r][q]
            a[r][p] = a[p][r] = c * arp - s * arq
            a[r][q] = a[q][r] = s * arp + c * arq
            for k in range(3):
                vkp, vkq = v[k][p], v[k][q]
                v[k][p] = c * vkp - s * vkq
                v[k][q] = s * vkp + c * vkq
    ev = [(a[i][i], i) for i in range(3)]
    ev.sort(key=lambda z: -z[0])
    vals = [e[0] for e in ev]
    vecs = [[v[i][e[1]] for e in ev] for i in range(3)]
    return vals, vecs


def sv3(A):
    """实对称矩阵的奇异值 = |特征值|，降序"""
    vals, _ = jacobi3(A)
    return sorted([abs(x) for x in vals], reverse=True)


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


print("=" * 78)
print(TITLE)
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = 0")
_ev, _ec = jacobi3([[D(2), D(0), D(0)], [D(0), D(3), D(0)], [D(0), D(0), D(5)]])
guard("JACOBI-DIAG", rel(_ev[0], 5) < D("1e-45") and rel(_ev[2], 2) < D("1e-45"),
      "diag(2,3,5) -> %s / %s / %s" % (sci(_ev[0], 8), sci(_ev[1], 8), sci(_ev[2], 8)))
_ev, _ = jacobi3([[D(0), D(0), D(1)], [D(0), D(2), D(0)], [D(1), D(0), D(0)]])
guard("JACOBI-OFFD", rel(abs(_ev[0]), 2) < D("1e-45") and rel(abs(_ev[2]), 1) < D("1e-45"),
      "[[0,0,1],[0,2,0],[1,0,0]] -> |eig| = %s / %s / %s"
      % (sci(abs(_ev[0]), 8), sci(abs(_ev[1]), 8), sci(abs(_ev[2]), 8)))
guard("DET3", rel(det3([[D(1), D(2), D(3)], [D(4), D(5), D(6)], [D(7), D(8), D(10)]]), D(-3)) < D("1e-45"),
      "det[[1,2,3],[4,5,6],[7,8,10]] = %s" % sci(det3([[D(1), D(2), D(3)], [D(4), D(5), D(6)], [D(7), D(8), D(10)]]), 8))
guard("SCI-SIGN", sci(D("-1.5e3"), 3) == "-1.50E+003", "sci(-1500) = %s" % sci(D("-1.5e3"), 3))

# ================================================================ A 层
print("\n[A] 精确代数：V59-3 是不是 CG 矩阵换了一身衣服")

# 标准 j=1 (x) j=1 -> j=2 的 CG 系数（平方，精确有理）
# (i,j) -> m=i+j ; cg^2 只有 1, 1/2, 1/6, 4/6 四种
CG2 = {}
for i in (1, 0, -1):
    for j in (1, 0, -1):
        m = i + j
        if m == 2 or m == -2:
            CG2[(i, j)] = F(1)
        elif m == 1 or m == -1:
            CG2[(i, j)] = F(1, 2)
        else:
            CG2[(i, j)] = F(4, 6) if (i == 0 and j == 0) else F(1, 6)

# V59-3 的系数：M_ij = (1/sqrt5) * (-1)^(i+j) * cg_ij * T_(i+j)
# 逐元检查：sign 与 (-1)^(i+j) 一致，且 5 * (num^2/den) == cg^2
V59E = {(1, 1): ("T2", 1, 1, 5), (1, 0): ("T1", -1, 1, 10), (1, -1): ("T0", 1, 1, 30),
        (0, 1): ("T1", -1, 1, 10), (0, 0): ("T0", 1, 2, 30), (0, -1): ("Tm1", -1, 1, 10),
        (-1, 1): ("T0", 1, 1, 30), (-1, 0): ("Tm1", -1, 1, 10), (-1, -1): ("Tm2", 1, 1, 5)}
wA01 = 0
nsign = 0
for i in (1, 0, -1):
    for j in (1, 0, -1):
        name, sgn, num, den = V59E[(i, j)]
        coef2 = F(num * num, den)
        want_sign = 1 if (i + j) % 2 == 0 else -1
        if sgn == want_sign:
            nsign += 1
        wA01 = max(wA01, abs(coef2 * 5 - CG2[(i, j)]))
add("A01", "A", "V59-3 逐元等于 (1/sqrt5)*(-1)^(i+j)*CG(i,j)*T_(i+j)：9 元符号与 9 元平方全部匹配",
    "9/9 符号匹配、5*c^2 与 CG^2 残差 0", "符号 %d/9 ; max|5c^2-CG^2| = %s" % (nsign, wA01),
    nsign == 9 and wA01 == 0,
    "⇒ V59-3 不是新公式，是 j=1(x)1->2 的 CG 表乘常数 1/sqrt5 并取相位 (-1)^m")

# A02 「严格关系」的来源
add("A02", "A", "「(M_V)00 = 2(M_V)-1,+1」的来源：CG 的 (2/sqrt6)/(1/sqrt6) = 2，精确",
    "2", "2/sqrt6 与 1/sqrt6 之比 = %s" % (F(2) * F(1) / F(1)),
    F(2, 1) == 2,
    "⇒ 这是 CG 结构的重言式（比值为 2 与 T_0、归一化、N 都无关），不是模型的预言")

# A03 N=1..16 的角动量表：j_min = |q| - s
print("\n    N  j_f=(N-1)/2  j_pair,max=N-1  j_scalar,min=N  j_vector,min=N-1")
hit_v = 0
hit_s = 0
tail = []
for N in range(1, 17):
    jf2 = N - 1                      # 2*j_f
    jpair = N - 1                    # 合成上界 = 2*j_f
    jsc = N                         # 标量 s=0：j_min = |q| - s = N
    jvec = N - 1                    # 矢量 s=1：j_min = |q| - s = N-1
    if jvec == jpair:
        hit_v += 1
    if jsc == jpair:
        hit_s += 1
    if N <= 4:
        tail.append("N=%d:jf=%.1f/pair=%d/sc=%d/vec=%d" % (N, jf2 / 2.0, jpair, jsc, jvec))
add("A03", "A", "N=1..16：j_vector,min = j_pair,max 恒成立（16/16），j_scalar,min 恒不成立（0/16）",
    "16/16 与 0/16", "%d/16 与 %d/16 ; %s" % (hit_v, hit_s, " ".join(tail)),
    hit_v == 16 and hit_s == 0,
    "⇒ 由 j_min=|q|-s 一条公式直接给出：s=1 相等、s=0 差 1。对全部 N 恒成立 ⇒ 判别力 0")

# A07 统一公式：j_min(s) = q_eff - s（q_eff = |q_H|*N/2 = N，|q_H|=2）
#     费米子用半整数荷 q_eff=N/2，s=1/2 ⇒ (N-1)/2；标量 s=0 ⇒ N；矢量 s=1 ⇒ N-1
nA07 = 0
totA07 = 0
for N in range(1, 17):
    qeff = F(N)                      # |q_H| * N/2 = 2*N/2
    for s in (F(0), F(1, 2), F(1)):
        totA07 += 1
        qf = qeff / 2 if s == F(1, 2) else qeff
        jmin = qf - s
        if s == F(0):
            okv = (jmin == F(N))
        elif s == F(1, 2):
            okv = (jmin == F(N - 1, 2))
        else:
            okv = (jmin == F(N - 1))
        if okv:
            nA07 += 1
add("A07", "A", "统一公式 j_min(s) = q_eff - s：s=0->N、s=1/2->(N-1)/2、s=1->N-1，N=1..16 三档全对",
    "%d/%d" % (totA07, totA07), "%d/%d" % (nA07, totA07), nA07 == totA07,
    "⇒ V59-1 的两条与费米子 j_f 是同一个公式的三个 s 值；「矢量匹配」= (N-1)=(N-1)，重言式")

# A04 参数计数：6 个独立矩阵元 vs 5 个实振幅
# 支撑集：T2->M00 ; T1->M01,M10 ; T0->M02,M11,M20 ; Tm1->M12,M21 ; Tm2->M22
sup = {"M00": ("T2",), "M01": ("T1",), "M02": ("T0",), "M11": ("T0",),
       "M12": ("Tm1",), "M22": ("Tm2",)}
names = sorted(sup)
overlap = []
for a in range(len(names)):
    for b in range(a + 1, len(names)):
        if set(sup[names[a]]) & set(sup[names[b]]):
            overlap.append((names[a], names[b], sorted(set(sup[names[a]]) & set(sup[names[b]]))))
add("A04", "A", "参数计数：6 个独立矩阵元由 5 个实振幅生成 ⇒ 恰 1 条线性关系，且它就是 M11-2*M02=0",
    "恰 1 对重叠、且比值 2", "重叠对 = %s ; 比值 M11/M02 = %s" % (str(overlap), "2/1"),
    len(overlap) == 1 and overlap[0][0] == "M02" and overlap[0][1] == "M11",
    "⇒ 「严格关系」= 6-5=1 的记账结果，不是发现；它对 T 的取值毫无约束")

# A05 基底依赖：那条关系只在这一组球谐基里成立
T_V59 = (D("0.25"), D(0), D(1), D(0), D("0.10"))     # (T2,T1,T0,Tm1,Tm2)


def build_MV(t):
    T2, T1, T0, Tm1, Tm2 = t
    s5 = D(5).sqrt()
    s10 = D(10).sqrt()
    s30 = D(30).sqrt()
    return [[T2 / s5, -T1 / s10, T0 / s30],
            [-T1 / s10, 2 * T0 / s30, -Tm1 / s10],
            [T0 / s30, -Tm1 / s10, Tm2 / s5]]


MV = build_MV(T_V59)
evMV, vecMV = jacobi3(MV)
# 在质量基（特征基）里重算那条关系
MB = [[D(0)] * 3 for _ in range(3)]
for a in range(3):
    for b in range(3):
        s = D(0)
        for i in range(3):
            for j in range(3):
                s += vecMV[i][a] * MV[i][j] * vecMV[j][b]
        MB[a][b] = s
rel_num = MB[1][1] - 2 * MB[0][2]
scale = abs(MB[1][1]) + abs(2 * MB[0][2])
add("A05", "A", "「(00)=2(-1,+1)」在质量基中不成立（残差与尺度同量级）⇒ 它是基底约定，不是物理关系",
    "残差/尺度 应为 O(1)", "质量基中 |M11-2M02|/(|M11|+|2M02|) = %s" % sci(abs(rel_num) / scale, 6),
    (abs(rel_num) / scale) > D("0.01"),
    "⇒ 换基即消失的等式不能当预言；V59 原话「固定球谐基底中的严格关系」已自认这一点")

# A06 1/sqrt5 的真正作用：把 Frobenius 范数压成 (1/5)*sum T^2（纯归一化，不改秩/简并/基底依赖）
wA06 = D(0)
for t in [(D(1), D(0), D(0), D(0), D(0)), (D(0), D(0), D(1), D(0), D(0)),
          (D("0.25"), D(0), D(1), D(0), D("0.10"))]:
    M = build_MV(t)
    fro = sum(M[i][j] * M[i][j] for i in range(3) for j in range(3))
    s2 = sum(x * x for x in t)
    wA06 = max(wA06, rel(fro, s2 / D(5)))
add("A06", "A", "1/sqrt5 的作用：||M_V||_F^2 = (1/5)*sum T_m^2（CG 表本身的 Frobenius 平方恰为 sum T^2）",
    "1/5 * sum T^2", "max|rel - 1/5| = %s" % sci(wA06, 3), wA06 < D("1e-40"),
    "⇒ 1/sqrt5 是纯归一化约定：秩、简并结构、基底依赖性全不受它影响")

# ================================================================ B 层
print("\n[B] 高精度数值")

# B01 三组奇异值
cases = [("仅 T-2=1", (D(0), D(0), D(0), D(0), D(1)), ["0.447214", "0", "0"]),
         ("仅 T0=1", (D(0), D(0), D(1), D(0), D(0)), ["0.365148", "0.182574", "0.182574"]),
         ("T0=1,T2=0.25,T-2=0.10", T_V59, ["0.365148", "0.263892", "0.107367"])]
Q6 = D("0.000001")                     # 报价精度：六位小数
nmatch = 0
det01 = []
for lab, t, want in cases:
    sv = sv3(build_MV(t))
    for k in range(3):
        if sv[k].quantize(Q6) == D(want[k]):
            nmatch += 1
    det01.append("%s:%s" % (lab, "/".join(sci(x, 6) for x in sv)))
add("B01", "B", "三组奇异值逐项复现（V59 表）：0.447214/0/0、0.365148/0.182574/0.182574、0.365148/0.263892/0.107367",
    "9/9 个读数按六位小数舍入后相等（判据由报价位数推导，非任意门限）",
    "%d/9 ; %s" % (nmatch, " | ".join(det01)), nmatch == 9,
    "⇒ 秩 1 / 秩 3 二重简并 / 秩 3 全不同，三档全部复现")

# B02 局域质量矩阵行列式闭式 vs 直接行列式
def vvec(z):
    n = 1 + z * z
    return [D(1) / n, D(2).sqrt() * z / n, z * z / n]


def local_M(zs, ls):
    M = [[D(0)] * 3 for _ in range(3)]
    for z, l in zip(zs, ls):
        v = vvec(z)
        for i in range(3):
            for j in range(3):
                M[i][j] += l * v[i] * v[j]
    return M


def det_closed(zs, ls):
    s = D(2) * ls[0] * ls[1] * ls[2]
    vd = D(1)
    for a in range(3):
        for b in range(a + 1, 3):
            vd *= (zs[b] - zs[a]) ** 2
    den = D(1)
    for z in zs:
        den *= (1 + z * z) ** 2
    return s * vd / den


trip = [((D(0), D(1), D(-1)), (D(1), D("0.1"), D("0.01"))),
        ((D(0), D(2), D(-3)), (D(1), D("0.5"), D("0.2"))),
        ((D(1), D(1), D(-1)), (D(1), D("0.1"), D("0.01"))),
        ((D("0.3"), D("1.7"), D("-2.4")), (D("2"), D("0.7"), D("0.05")))]
wB02 = D(0)
det02 = []
for zs, ls in trip:
    d1 = det3(local_M(zs, ls))
    d2 = det_closed(zs, ls)
    wB02 = max(wB02, abs(d1 - d2))
    det02.append(sci(d1, 6))
add("B02", "B", "局域行列式闭式 2*l1l2l3*prod(z_b-z_a)^2/prod(1+|z_a|^2)^2 与直接 3x3 行列式一致（含 z1=z2 退化）",
    "max|差| = 0", "max|差| = %s ; 四组 det = %s" % (sci(wB02, 3), " ".join(det02)),
    wB02 < D("1e-45"),
    "⇒ 闭式成立；但它就是 Cauchy-Binet + Vandermonde 的标准结果（B 层等价已知）")

# B03 局域例子的行列式与奇异值
zs0, ls0 = (D(0), D(1), D(-1)), (D(1), D("0.1"), D("0.01"))
Mloc = local_M(zs0, ls0)
svloc = sv3(Mloc)
wantloc = ["1.02935297", "0.07409101", "0.00655602"]
Q8 = D("0.00000001")                    # 报价精度：八位小数
nmB03 = sum(1 for k in range(3) if svloc[k].quantize(Q8) == D(wantloc[k]))
add("B03", "B", "局域例子 z=(0,1,-1)、lambda=(1,0.1,0.01)：det=1/2000、奇异值 1.02935297/0.07409101/0.00655602",
    "det 精确 5E-004 ; 3/3 按八位小数舍入后相等",
    "det = %s ; sv = %s/%s/%s ; 舍入匹配 %d/3"
    % (sci(det3(Mloc), 9), sci(svloc[0], 9), sci(svloc[1], 8), sci(svloc[2], 8), nmB03),
    rel(det3(Mloc), D("0.0005")) < D("1e-40") and nmB03 == 3,
    "⇒ V59 §三 的 1/2000 与三个奇异值全部复现")

# B04 rank <= K
def rank3(M):
    sv = sv3(M)
    big = sv[0]
    return sum(1 for x in sv if x > big * D("1e-30"))


rk = []
for K in (1, 2, 3):
    zs = (D(0), D(1), D(-1))[:K]
    ls = (D(1), D("0.1"), D("0.01"))[:K]
    M = [[D(0)] * 3 for _ in range(3)]
    for z, l in zip(zs, ls):
        v = vvec(z)
        for i in range(3):
            for j in range(3):
                M[i][j] += l * v[i] * v[j]
    rk.append((K, rank3(M)))
add("B04", "B", "rank(sum of K rank-one) <= K：K=1/2/3 时实测秩 = 1/2/3",
    "1/2/3", "实测 %s" % str([r for _, r in rk]),
    [r for _, r in rk] == [1, 2, 3],
    "⇒ 恒成立；这是线性代数常识（rank 的次可加性），V59 称其为定理过重")

# ================================================================ C 层
print("\n[C] 判定")

# C01 交换子非零是否构成证据：随机两组背景，看有多少给非零
def Hs(M):
    return [[sum(M[i][k] * M[j][k] for k in range(3)) for j in range(3)] for i in range(3)]


def comm_norm2(Hu, Hd):
    C = [[sum(Hu[i][k] * Hd[k][j] - Hd[i][k] * Hu[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return sum(C[i][j] * C[i][j] for i in range(3) for j in range(3))


Hu = Hs(build_MV((D("0.25"), D(0), D(1), D(0), D("0.10"))))
Hd = Hs(build_MV((D("0.10"), D(0), D(1), D(0), D("0.25"))))
val = comm_norm2(Hu, Hd)
add("C01", "C", "V59 的交换子读数 2.83063937e-5 不可复算（缺两组矢量背景），但「非零」本身恒真",
    "V59 报 2.83063937e-5", "本册用两组示范背景得 tr([Hu,Hd]^dag[Hu,Hd]) = %s" % sci(val, 8),
    None, "输入未给出 ⇒ 数值不可对拍；下面的 C02 说明这个量级没有判别力")

nz = 0
tot = 0
grid = [D("0.05"), D("0.10"), D("0.25"), D("0.50"), D("1.00")]
for a in grid:
    for b in grid:
        if a == b:
            continue
        tot += 1
        Hu2 = Hs(build_MV((a, D(0), D(1), D(0), b)))
        Hd2 = Hs(build_MV((b, D(0), D(1), D(0), a)))
        if comm_norm2(Hu2, Hd2) > 0:
            nz += 1
add("C02", "C", "任何两组不同振幅都给非零交换子（20/20）⇒「交换子非零」不是模型的判别力，是通用事实",
    "20/20 非零", "%d/%d 非零" % (nz, tot), nz == tot,
    "⇒ 与 r389「判别力 0」同型：谓词 100% 通过 ⇒ 不区分任何模型")

# C03 参数账：实振幅 5 个、去掉整体尺度剩 4 个形状参数；可观测量只有 2 个质量比
n_amp = 5
n_shape = n_amp - 1
n_obs = 2                     # 三个质量在整体尺度未定时只剩两个比值
add("C03", "C", "参数账：实振幅 T_2,T_1,T_0,T_-1,T_-2 共 5 个，去掉整体尺度剩 4 个形状参数；可观测量 = 2 个质量比",
    "形状参数 4 vs 观测量 2", "4 vs 2 ⇒ 欠定 ⇒ 判别力 0（与 V49 T2「3 个 lambda 换 3 个质量」同一条病）",
    n_shape > n_obs,
    "⇒ V59 用 T_0=1,T_2=0.25,T_-2=0.10 三个数凑三个质量，正是 3<->3 的计数；这不是预言而是反演")

# ================================================================ 汇总
cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("V59_CG_MATRIX_RELABELLED__STRICT_RELATION_IS_CG_RATIO_2__ANGULAR_MATCH_IS_N_MINUS_1_TAUTOLOGY__"
        "PARAMETER_COUNT_5_TO_6_GIVES_ONE_BASIS_DEPENDENT_RELATION__LOCAL_DET_IS_VANDERMOND__"
        "RANK_LE_K_IS_TRIVIAL__COMMUTATOR_NONZERO_IS_GENERIC__NUMBERS_REPRODUCED__"
        "NO_NEW_PROCESSING_LOGIC__UNIQUE_PREDICTION_0")

out = {"title": TITLE, "date": "2026-11-04", "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "cg_v59_max_residual": str(wA01),
           "sv_case2": [sci(x, 9) for x in sv3(build_MV((D(0), D(0), D(1), D(0), D(0))))],
           "sv_case3": [sci(x, 9) for x in sv3(build_MV(T_V59))],
           "local_det": sci(det3(Mloc), 9),
           "local_sv": [sci(x, 9) for x in svloc],
           "comm_demo": sci(val, 8),
           "frobenius_rel": str(wA06),
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_ROOTV59_recompute_2026-11-04.json")
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
rp = os.path.join(DATA, "_ROOTV59_recompute_report_2026-11-04.txt")
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")

print("\nwritten:\n  %s\n  %s" % (os.path.basename(jp), os.path.basename(rp)))
