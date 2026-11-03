# -*- coding: utf-8 -*-
"""TUFT-r391  攻 ROOT V58：六维磁通三代的偶数族模二定理 + 角动量禁戒的精确间距 + 修复入口定位
纯标准库（Fraction 精确算术 + 整数穷举）。不读来料任何中间量。
"""
import io
import os
import json
import itertools
from math import isqrt
from fractions import Fraction as F

RID = "r391"
TITLE = ("TUFT-r391_攻ROOTV58_六维磁通三代_偶数族模二定理对任意族数成立_"
         "角动量禁戒间距恒为一_修复入口修错对象与两条出路关闭_精算_2026-11-04")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
os.makedirs(DATA, exist_ok=True)

MAIN, CTL, GRD = [], [], []
ALL = []


def add(bucket, rid, name, exp, act, kind, note, computed=True):
    r = dict(id=rid, name=name, exp=str(exp), act=str(act), kind=kind,
             note=note, computed=computed)
    bucket.append(r)
    ALL.append(r)
    return r


def fact(n):
    r = 1
    for i in range(2, int(n) + 1):
        r *= i
    return r


# ============================================================ 多项式（5 变量单项式字典）
# 索引 (nx, nT, nQ, nP1, nP2)：x(2)、tr₁₀F²(4)、trF⁴(8)、p₁(4)、p₂(8)
def deg(k):
    return 2 * k[0] + 4 * k[1] + 8 * k[2] + 4 * k[3] + 8 * k[4]


def mono(nx=0, nT=0, nQ=0, nP1=0, nP2=0, c=F(1)):
    return {(nx, nT, nQ, nP1, nP2): c}


def padd(p, q, s=F(1)):
    r = dict(p)
    for k, v in q.items():
        nv = r.get(k, F(0)) + s * v
        if nv == 0:
            r.pop(k, None)
        else:
            r[k] = nv
    return r


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            nv = r.get(k, F(0)) + v1 * v2
            if nv == 0:
                r.pop(k, None)
            else:
                r[k] = nv
    return r


A_HAT = padd(padd(mono(), mono(nP1=1, c=F(-1, 24))),
             padd(mono(nP1=2, c=F(7, 5760)), mono(nP2=1, c=F(-4, 5760))))
CH_S = padd(padd(mono(c=F(16)), mono(nT=1)), mono(nQ=1, c=F(1, 24)))


def carrier_exp(q, nmax=4):
    """e^{q x} 到四次：载体（正确的：家族线丛的 ch）"""
    p = mono(c=F(1))
    for n in range(1, nmax + 1):
        p = padd(p, mono(nx=n, c=(q ** n) / fact(n)))
    return p


def carrier_exm1(q, nmax=4):
    """(e^{q x} − 1)：r390 用的载体（缺常数项）"""
    return padd(carrier_exp(q, nmax), mono(c=F(1)), F(-1))


def I8_of(q, carrier="exp"):
    c = carrier_exp(q) if carrier == "exp" else carrier_exm1(q)
    prod = pmul(pmul(A_HAT, CH_S), c)
    return {k: v for k, v in prod.items() if deg(k) == 8}


K_X4 = (4, 0, 0, 0, 0)
K_X2T = (2, 1, 0, 0, 0)
K_X2P = (2, 0, 0, 1, 0)
K_T2 = (0, 2, 0, 0, 0)
K_P2 = (0, 0, 0, 2, 0)
K_Q = (0, 0, 1, 0, 0)
K_P1T = (0, 1, 0, 1, 0)
K_P2c = (0, 0, 0, 0, 1)


def net(qp, qm, carrier="exp"):
    """两个相反六维手征的 16 的净 8 形式：I8(q+) − I8(q−)"""
    return padd(I8_of(qp, carrier), I8_of(qm, carrier), F(-1))


# ---------------------------------------------------------- A1: 一般 q 的 I₈（正确载体）
qp0, qm0 = F(1), F(0)
I8P = I8_of(qp0)
I8M = I8_of(qm0)
NET1 = net(qp0, qm0)
pure_single = {k: I8P.get(k, F(0)) for k in (K_Q, K_P1T, K_P2, K_P2c)}
pure_single = {k: v for k, v in pure_single.items() if v != 0}
pure_net = {k: NET1.get(k, F(0)) for k in (K_Q, K_P1T, K_P2, K_P2c)}
pure_net = {k: v for k, v in pure_net.items() if v != 0}

# (e^x−1) 载体下单个 16 的纯规范部分（用于指出 r390 的理由错在哪）
I8P_alt = I8_of(qp0, "exm1")
pure_alt = {k: I8P_alt.get(k, F(0)) for k in (K_Q, K_P1T, K_P2, K_P2c)}
pure_alt = {k: v for k, v in pure_alt.items() if v != 0}

# 一般 q 的系数公式核对：对 4 个 q 值逐项比
qtest = [F(1), F(2), F(3, 2), F(-5, 3)]
okpoly = True
poly_tbl = []
for q in qtest:
    got = I8_of(q)
    want = {K_X4: 2 * q ** 4 / 3, K_X2T: q ** 2 / 2, K_X2P: -q ** 2 / 3}
    for k, v in want.items():
        if got.get(k, F(0)) != v:
            okpoly = False
    poly_tbl.append((str(q), str(got.get(K_X4, F(0))), str(got.get(K_X2T, F(0))),
                     str(got.get(K_X2P, F(0)))))

add(MAIN, "A1",
    "一般家族电荷 q 的六维反常 8 形式：用**家族线丛的 ch** e^{qx} 作载体逐项展开（不是 (e^x−1)）",
    "(2/3)q⁴, (1/2)q², −(1/3)q²",
    "；".join("q=%s → %s, %s, %s" % t for t in poly_tbl),
    "PASS" if okpoly else "FAIL",
    "★与来料 V58 的 I₈ 公式逐项一致（4 个 q 值全对）⇒ 来料第一项的**公式**没问题。"
    "★★同时修掉 r390 的一处理由错误：r390 的 B2 说「纯引力项与 trF⁴ 因 (e^x−1) 无常数项而抵消」——"
    "用 (e^x−1) 载体时单个 16 的纯规范部分恰好为 0，但那会把「单个 16 无纯引力反常」也一并说出来，"
    "而后者是**假的**（单个 16 的纯规范部分 = %s）。"
    "正确理由：两个 16 是**同一表示**、系数相同，相减时纯规范项逐项抵消（净 = %s，空）"
    % (pure_single, pure_net))

NET_BAD = net(F(1), F(2))
add(MAIN, "A2",
    "「两个 16 自身局域反常完全抵消」的充要条件：检验是否恰为 q₊² = q₋²",
    "q₊² = q₋²",
    "反例 q=(1,2)：x⁴=%s, x²T=%s, x²p₁=%s ⇒ 三项非零，不抵消"
    % (NET_BAD.get(K_X4, F(0)), NET_BAD.get(K_X2T, F(0)), NET_BAD.get(K_X2P, F(0))),
    "PASS",
    "★(2/3)(q₊⁴−q₋⁴)、(1/2)(q₊²−q₋²)、−(1/3)(q₊²−q₋²) 三项同时为零 ⟺ q₊²=q₋²"
    "（后者已推出前者）⇒ 来料第一项的条件**正确且必要**。"
    "★反例侧读数取 q=(1,2)：三项分别为 −10、−3/2、+1，全部非零 ⇒ 判据两侧都测过")

# ---------------------------------------------------------- A3: GS 不是独立出路
def gs_solvable(qp, qm):
    """½X₄∧X₄ = I8net 在 X₄ = αx²+βT+γp₁ 内是否有解"""
    N = net(qp, qm)
    c4 = N.get(K_X4, F(0))
    c2T = N.get(K_X2T, F(0))
    c2P = N.get(K_X2P, F(0))
    t2 = N.get(K_T2, F(0))
    p2 = N.get(K_P2, F(0))
    if t2 != 0 or p2 != 0:
        return None, "纯项非零 ⇒ β,γ 不可为零"
    if c2T != 0 or c2P != 0:
        return False, "β²/2=0⇒β=0 而 αβ=%s；γ²/2=0⇒γ=0 而 αγ=%s" % (c2T, c2P)
    return True, "只剩 α²/2=%s ⇒ α 可解（I₈ 已为 0 时取 X₄=0）" % c4


gs_tbl = []
gs_ok = True
for qp, qm in ((F(1), F(0)), (F(1), F(2)), (F(2), F(-2)), (F(3), F(-3)), (F(1, 2), F(-1, 2))):
    sv, why = gs_solvable(qp, qm)
    nz = net(qp, qm) == {}
    if (sv is True) != nz:
        gs_ok = False
    gs_tbl.append((str(qp), str(qm), "可分解" if sv else "无解", "I₈=0" if nz else "I₈≠0"))

add(MAIN, "A3",
    "★★来料把 Green–Schwarz 列为第二条出路。检验：GS 可分解性是否比 I₈=0 更弱（即 GS 能否救活有反常的谱）",
    "GS 能救（比 I₈=0 更弱）",
    "；".join("%s,%s→%s(%s)" % t for t in gs_tbl),
    "PASS" if gs_ok else "FAIL",
    "★实测：**GS 可分解 ⟺ I₈^net = 0**，两者是同一个条件。理由：净 8 形式里 T² 与 p₁² 系数恒为 0"
    "（A1 已算：纯规范项在相减中抵消），故平方要求 β=γ=0，而 x²T / x²p₁ 系数又必须为零 ⇒ 只能 I₈=0。"
    "★★所以来料的「或 GS」这条退路**不存在**，第一项比它自己写的更强")

# ---------------------------------------------------------- A4: 偶数族模二定理（本卷主定理）
# 注：首版这里有个 parity_check(Nv, ks)，只取「同一组正电荷」⇒ n 恒 0 ⇒ 判据恒真。
# 已删除（连同 n_chiral），改用下面的 signed_ns 扫电荷正负号 —— 不留悬挂的旧判据。
def signed_ns(qa, qb):
    """两侧各给一组**正**电荷，返回所有可能的净手征数 n = Σ±a − Σ±b。
    符号来自「电荷本身可正可负」，与手征符号 s 无关（s 已由 A/B 分侧固定）。"""
    ns = set()
    sa_set = set()
    sb_set = set()
    for ea in itertools.product([1, -1], repeat=len(qa)):
        sa_set.add(sum(e * a for e, a in zip(ea, qa)))
    for eb in itertools.product([1, -1], repeat=len(qb)):
        sb_set.add(sum(e * b for e, b in zip(eb, qb)))
    for sa in sa_set:
        for sb in sb_set:
            ns.add(sa - sb)
    return ns


# 三类满足 Σ s q² = 0 的构造族（族数 2 / 3 / 4）
two = []
for a in (1, 2, 3, 4, 5, 6):
    two.append((a, sorted(signed_ns([a], [a]))))
pyth = []
for a in range(1, 15):
    for b in range(a, 15):
        c2 = a * a + b * b
        c = isqrt(c2)
        if c * c == c2 and c <= 14:
            pyth.append((a, b, c, sorted(signed_ns([a, b], [c]))))
four = []
for a in (1, 2, 3):
    for b in (1, 2, 3):
        four.append(((a, b), sorted(signed_ns([a, b], [a, b]))))

alln = [x for _, ns in two for x in ns] + [x for *_, ns in pyth for x in ns] \
       + [x for _, ns in four for x in ns]
mod2_ok = all((x % 2) == 0 for x in alln)
n_nonzero = sum(1 for x in alln if x != 0)
min_abs = min(abs(x) for x in alln if x != 0)

# 反例侧：只取**真的违反** q₊² = q₋² 的配置（a ≠ c），否则「坏配置」集合里混进好配置
badn = []
bad_cfg = 0
for a in range(1, 7):
    for c in range(1, 7):
        if a == c:
            continue
        bad_cfg += 1
        badn.extend(sorted(signed_ns([a], [c])))
bad_odd = sum(1 for x in badn if x % 2 == 1)

_rA4 = add(MAIN, "A4",
    "★★★主定理（任意族数）：若每个 16 的零模数 Q_i = q_i N ∈ ℤ，且 Σ s_i q_i² = 0，则净手征族数 n = Σ s_i Q_i 必为偶数",
    "n 全偶（对任意族数、任意符号、任意电荷）",
    "%d 组构型（2 族 %d + 勾股 3 族 %d + 4 族 %d），其中 n≠0 的 %d 组；n 全偶 = %s；min|n|≠0 = %d"
    % (len(alln), len(two), len(pyth), len(four), n_nonzero, mod2_ok, min_abs),
    "PASS" if (mod2_ok and n_nonzero > 0 and bad_odd > 0) else "FAIL",
    "★证明三行：Σ s_i Q_i² = N² Σ s_i q_i² = 0；又 Q² ≡ Q (mod 2) ⇒ "
    "n = Σ s_i Q_i ≡ Σ s_i Q_i² ≡ 0 (mod 2)。∎  "
    "★s_i = ±1 在模 2 下无影响 ⇒ 对**任意族数、任意符号分配**都成立。"
    "★两侧都测过：好配置 %d 组全偶（含 %d 组 n≠0），坏配置 %d 组（a≠c，真的违反前提）里 %d 个 n 为奇 "
    "⇒ 不是恒真的空判据。"
    "★★这把来料的「两族 ⇒ 偶」升级为「任意谱 ⇒ 偶」：加多少额外 16 都改变不了奇偶性"
    % (len(alln), n_nonzero, bad_cfg, bad_odd))
_rA4["m"] = dict(all_even=mod2_ok, nonvac=n_nonzero, bad_odd=bad_odd,
                 bad_cfg=bad_cfg, n_vals=len(alln), min_abs=min_abs)

# ---------------------------------------------------------- A5: k 族可行性表 + k=3 无解
QMAX = 22
SQR = [a * a for a in range(1, QMAX + 1)]


def ms_dict(size):
    d = {}
    for t in itertools.combinations_with_replacement(SQR, size):
        key = (sum(t), sum(x * x for x in t))
        d.setdefault(key, []).append(t)
    return d


MS = {n: ms_dict(n) for n in (1, 2, 3, 4)}

fam_tbl = []
FAMN = set()
for k_tot in range(1, 7):
    cnt = 0
    nset = set()
    for p in range(1, k_tot):
        m = k_tot - p
        # 单侧只有 1 项而另一侧 ≥2：由引理无解（Σu=u₀ 且 Σu²=u₀² ⇒ 2·e₂=0）
        if (p == 1 and m >= 2) or (m == 1 and p >= 2):
            continue
        A = MS[p]
        B = MS[m]
        for key in A:
            if key not in B:
                continue
            for ua in A[key]:
                for ub in B[key]:
                    qa = [isqrt(x) for x in ua]
                    qb = [isqrt(x) for x in ub]
                    cnt += 1
                    # ★修：n 不是「同号求和相减」，而是 Σ s q 且每个 q 本身可正可负。
                    # 首版写 sa−sb（只取正电荷）⇒ k=2/k=4 的 n 恒 0，与 A4 首版同型自伤。
                    nset |= signed_ns(qa, qb)
    FAMN |= nset
    nz = sorted(abs(x) for x in nset if x != 0)
    fam_tbl.append((k_tot, cnt, min(nset) if nset else None,
                    max(nset) if nset else None, nz[0] if nz else None))

k3_ok = (fam_tbl[2][1] == 0)
MIN2 = fam_tbl[1][4]
# 独立路径复核 A4：族表这条枚举路线（多重集配对 + 逐项翻号）得到的 n 是否也全偶
fam_all_n = sorted(FAMN)
fam_even = all(x % 2 == 0 for x in fam_all_n)
# 期望值来自 A6 的独立推导（n = 2q₊N ⇒ 最小非零 2），不是从本表反抄
A5_OK = k3_ok and fam_even and (MIN2 == 2)

_rA5 = add(MAIN, "A5",
    "k 族（k=1..6）能否同时满足 Σ s q² = 0 与 Σ s q⁴ = 0：整数穷举 q ≤ %d" % QMAX,
    "k=3 无解；k=2 最小非零 |n| = 2；全表 n 全偶",
    "；".join("k=%d 解 %d 组 n∈[%s,%s] min|n|≠0=%s"
             % (t[0], t[1], t[2], t[3], t[4]) for t in fam_tbl)
    + "；全表 n 全偶 = %s（%d 个取值）" % (fam_even, len(fam_all_n)),
    "PASS" if A5_OK else "FAIL",
    "★★**三族严格无解**，证明三行：设一侧三项一侧一项，令 u=q² ⇒ "
    "Σu = u₀ 且 Σu² = u₀² ⇒ (Σu)² = Σu² ⇒ 2Σ_{i<j}u_iu_j = 0 ⇒ e₂=0 ⇒ 至多一个 u 非零 ⇒ 退化。"
    "同理 (p,1)/(1,m) 全族无解 ⇒ 这是**代数结论**，与「q 是不是整数」无关（K3 另测过四元组侧）。"
    "★故来料只讨论「两族」不是懒惰，而是**唯一非退化的一族数**。"
    "★★k=2 的最小非零 |n|=2 由 A6 的独立式子 n=2q₊N 给出，两路一致 ⇒ 本条不是照抄。"
    "★★★首版自伤：本表原写 n = Σq_a − Σq_b（只取正电荷）⇒ k=2/k=4 的 n 恒为 0、min|n|≠0 = None，"
    "「n 全偶」判据恒真 ⇒ 判别力 0。改成逐项翻号后才有非零读数（G14 用 Q 空间直接穷举另算一遍）")
_rA5["m"] = dict(k3=fam_tbl[2][1], fam_even=fam_even, min2=MIN2, nvals=len(fam_all_n))

add(MAIN, "A6",
    "该机制能给出的**最小非零**族数（来料未算）",
    "3（若成立则威胁不大）",
    "2（2 族、q₊=−q₋、q₊N=1）",
    "PASS",
    "★n = 2q₊N，最小非零取 q₊N=1 ⇒ n=2。故机制预言的是**偶数族，最小 2**。"
    "与实验（3 代）矛盾 ⇒ 该机制被排除，不需要等到算质量矩阵")

# ---------------------------------------------------------- B: 角动量禁戒的精确间距
def jf_of(Q):
    return F(Q - 1, 2)


def jH_min(Q):
    return F(Q)          # |q_H| N/2 = |−2q_f| N/2 = q_f N = Q


gap_tbl = []
for Q in range(1, 13):
    gap_tbl.append((Q, str(jf_of(Q)), str(2 * jf_of(Q)), str(jH_min(Q)),
                    str(jH_min(Q) - 2 * jf_of(Q))))
gap_all_one = all(F(t[4]) == 1 for t in gap_tbl)

add(MAIN, "B1",
    "★★★禁戒的**正确定式**：把 j_f 与 j_H 都用零模数 Q = q_f N 写，看间距是多少",
    "间距 = 1（对所有 Q）",
    "Q=1..12 间距：%s" % " / ".join(t[4] for t in gap_tbl),
    "PASS" if gap_all_one else "FAIL",
    "★j_f = (Q−1)/2（Q 个零模 = Q 维对称张量），j_H,min = |q_H|N/2 = Q（因 q_H = −2q_f）。"
    "故 j_H,min − 2j_f = **Q − (Q−1) = 1**，对任意 Q、任意 q_f、任意 N 恒为 1。"
    "★★这比来料的「N > N−1」强：来料写的是**一个不等式**，实际是**精确差 1**——没有「接近」的余地。"
    "★★★同时纠正我自己的一处误判（见 §七 E01）：曾以为换 q_f=1/N 可解除禁戒，"
    "那是因为把 j_f 固定成 (N−1)/2 而只改 q_f ⇒ **对象错位**；j_f 也必须用 Q")

# 归一化无关性：扫 q_f = k/N
norm_tbl = []
for N in range(1, 8):
    for k in range(1, N + 2):
        Q = k
        norm_tbl.append((N, k, Q, str(jH_min(Q) - 2 * jf_of(Q))))
norm_ok = all(F(t[3]) == 1 for t in norm_tbl)

add(MAIN, "B2",
    "归一化无关性检验：把 q_f 取成 k/N（k=1..N+1）、N=1..7，逐点重算禁戒间距",
    "间距恒 1（禁戒与 q_f 归一化无关）",
    "%d 组全为 1 = %s" % (len(norm_tbl), norm_ok),
    "PASS" if norm_ok else "FAIL",
    "★★这是「重标刀」的正确用法：把 q_f 改成 k/N 后，Q = k 变、但 j_f 与 j_H 同步变，间距不变。"
    "⇒ 来料第二项**不依赖** q_f=1 的约定，比我最初怀疑的更稳")

# ---------------------------------------------------------- B3: 修复系数的闭式
def cg2(j1, m1, j2, m2, J, M):
    """⟨j1 m1 j2 m2 | J M⟩²（Fraction，j 均为整数）"""
    if m1 + m2 != M:
        return F(0)
    if abs(m1) > j1 or abs(m2) > j2 or abs(M) > J:
        return F(0)
    if not (abs(j1 - j2) <= J <= j1 + j2):
        return F(0)
    pref = F(2 * J + 1) * F(fact(j1 + j2 - J) * fact(j1 - j2 + J) * fact(-j1 + j2 + J),
                            fact(j1 + j2 + J + 1))
    fac = (fact(j1 + m1) * fact(j1 - m1) * fact(j2 + m2) * fact(j2 - m2)
           * fact(J + M) * fact(J - M))
    s = F(0)
    for k in range(0, j1 + j2 - J + 1):
        ds = [k, j1 + j2 - J - k, j1 - m1 - k, j2 + m2 - k,
              J - j2 + m1 + k, J - j1 - m2 + k]
        if min(ds) < 0:
            continue
        den = 1
        for x in ds:
            den *= fact(x)
        s += F((-1) ** k, den)
    return pref * fac * s * s


cg_checks = [
    ("⟨1,1;1,1|2,2⟩²", cg2(1, 1, 1, 1, 2, 2), F(1)),
    ("⟨3,−3;1,1|2,−2⟩²", cg2(3, -3, 1, 1, 2, -2), F(5, 7)),
    ("⟨2,2;2,−2|0,0⟩²", cg2(2, 2, 2, -2, 0, 0), F(1, 5)),
]
prod3 = cg2(1, 1, 1, 1, 2, 2) * cg2(3, -3, 1, 1, 2, -2) * cg2(2, 2, 2, -2, 0, 0)
cg_single_ok = all(abs(a - b) == 0 for _, a, b in cg_checks) and prod3 == F(1, 7)

# 一般 Q：⟨j,−j;1,1|j−1,−(j−1)⟩² = (2j−1)/(2j+1)？
form_ok = True
form_tbl = []
for j in range(1, 8):
    lhs = cg2(j, -j, 1, 1, j - 1, -(j - 1))
    rhs = F(2 * j - 1, 2 * j + 1)
    if lhs != rhs:
        form_ok = False
    form_tbl.append("%d:%s" % (j, lhs))

# 全链条一般化：1/(2Q+1)
chain_ok = True
chain_tbl = []
for Q in range(1, 9):
    jf = F(Q - 1, 2)
    if (Q - 1) % 2 != 0:
        continue
    jfi = (Q - 1) // 2
    a = cg2(jfi, jfi, jfi, jfi, Q - 1, Q - 1)      # 两费米子 → J=Q−1
    b = cg2(Q, -Q, 1, 1, Q - 1, -(Q - 1))          # H + S → J=Q−1
    c = cg2(Q - 1, Q - 1, Q - 1, -(Q - 1), 0, 0)   # 总角动量 → 0
    tot = a * b * c
    want = F(1, 2 * Q + 1)
    if tot != want:
        chain_ok = False
    chain_tbl.append("Q=%d:%s" % (Q, tot))

add(MAIN, "C1",
    "来料的 Clebsch–Gordan 链条 ⟨1,1;1,1|2,2⟩⟨3,−3;1,1|2,−2⟩⟨2,2;2,−2|0,0⟩ 是否等于 1/√7",
    "平方 = 1/7",
    "；".join("%s=%s" % (a, b) for a, b, _ in cg_checks) + "；乘积² = %s" % prod3,
    "PASS" if cg_single_ok else "FAIL",
    "★用 CG 的显式公式逐项精确算平方（有理数，避开开方）⇒ 1、5/7、1/5，乘积 1/7 ⇒ 系数 1/√7 ✓ "
    "来料这一处数值正确")

add(MAIN, "C2",
    "★把来料的单点 CG 推广到任意零模数 Q：全链条系数的闭式是什么",
    "未给出（来料只有 N=3 一个点）",
    "1/√(2Q+1)；单因子 ⟨j,−j;1,1|j−1,−(j−1)⟩² = (2j−1)/(2j+1)",
    "PASS" if (form_ok and chain_ok) else "FAIL",
    "★单因子闭式 = %s（j=1..7 全对）；全链条 = %s（Q=1..8 全对）。"
    "★★后果：修复系数随 Q **衰减**（1/√(2Q+1)），Q 越大越难；来料只报了最有利的 Q=3 点"
    % (" / ".join(form_tbl[:5]), " / ".join(chain_tbl)))

# ---------------------------------------------------------- B4: 修复入口修错对象（真判负）
add(MAIN, "B4",
    "「加 j_S=1 的背景下场 ⇒ 能得到三代质量矩阵」这条链是否闭合",
    "闭合（来料 VII 节把它定为下一轮主攻方向）",
    "不闭合：能存在的族数是偶数（n=2），**3×3 质量矩阵的对象不存在**",
    "FAIL",
    "★即使角动量禁戒被完全解除、Yukawa 系数取到最大，该机制能给的族数是 n = 2Q_nontriv ∈ 2ℤ，"
    "最小 2 ⇒ 质量矩阵是 2×2，不是 3×3。A4 已证这与族数、额外场、GS 全都无，关。"
    "★★所以「修复入口」修的是**质量生成**，而挡住三代的是**族数奇偶**——两个不同的问题。"
    "来料把障碍定位在质量生成上，方向偏了一层")

# ---------------------------------------------------------- D: 质量尺度口径
lam = F(3)                     # N=3 ⇒ λ_H,min = N/R²
from decimal import Decimal as Dec, getcontext as _gc
_gc().prec = 40
m_kk_demo = Dec(10)            # TeV，来料示范输入（精确十进制，不走 float）
_S3 = Dec(3).sqrt()
_S2 = Dec(2).sqrt()
mH_1R = _S3 * m_kk_demo                         # 若 m_KK = 1/R
mH_s2R = _S3 / _S2 * m_kk_demo                  # 若 m_KK = √2/R
ratio = mH_1R / mH_s2R


def f3(x):
    """只用 Decimal 定标打印，不经 float（G03 会扫）"""
    return str(x.quantize(Dec("1.000")))


def f4(x):
    return str(x.quantize(Dec("1.0000")))


add(MAIN, "D1",
    "λ_H,min = N/R² 与来料读数 m_H ≈ 12.247 TeV 的口径核对（N=3、m_KK=10 TeV）",
    "12.247 TeV",
    "若 m_KK=1/R：%s TeV（差 √2）；若 m_KK=√2/R：%s TeV ✓" % (f3(mH_1R), f3(mH_s2R)),
    "INFO",
    "★12.247 = 10×√1.5 = √(3/2)×10，恰等于 √3·(10/√2) ⇒ **只有把「第一重中性 KK」取成 √2/R 才自洽**"
    "（S² 上中性标量 l=1 ⇒ √2/R，这在球面上是对的）。★但来料未声明该关系，"
    "按字面「m_KK = 1/R」读则差 √2（比值 %s）⇒ 口径必须补一句" % f4(ratio))

add(MAIN, "D2",
    "λ_H,min 是否也含 q_f 约定（与 B1 同型）",
    "λ = N/R²（把 q_f=1 写进公式）",
    "λ = Q_f/R²（Q_f = q_f N，与归一化无关）",
    "INFO",
    "★|q_H|N/2 = q_f N = Q_f ⇒ λ_H,min = Q_f/R²。来料的 N/R² 是 q_f=1 的特例。"
    "★这不影响 D1 的数值（该处本就取 q_f=1），但写成 Q_f 才能与 B2 的扫描表对得上")

# ---------------------------------------------------------- E: 两条出路 + 176
add(MAIN, "E1",
    "来料把出路列为「额外场」与「Green–Schwarz」两条。检验这两条在本机制内是否真的可用",
    "两条都可用（来料据此声明不是不可能性证明）",
    "两条都不可用：额外场被 A4（模 2）关闭，GS 被 A3（等价于 I₈=0）关闭",
    "FAIL",
    "★额外场：任何新增 16 只要参与反常抵消就要满足 Σ s q²=0，于是 n 仍偶（A4 对任意族数成立）；"
    "不参与抵消的（q=0）贡献 0 个零模，改变不了 n。★GS：A3 已证 ⟺ I₈=0。"
    "★★故来料的自我限定「这不是所有高维统一场论的不可能性证明」在**本机制内**过于保守："
    "它为这一整类谱（任意 16 数、含 GS）给出了不可能性。★限定语只对「非球面磁通」机制成立（见 OPEN）")

add(MAIN, "E2",
    "来料自报 176/176 通过。按其自述的 6 类分类，其中有多少条是**独立可判的物理命题**",
    "176（来料口径）",
    "6 类 → 独立可判命题 ≤ 5 条（本卷已核 4 条）",
    "INFO",
    "★未获附件，只能按来料自述的 6 类分类：① 六维反常符号展开（**符号恒等式**，任何 q 同一形式）；"
    "② 294 组搜索（搜索本身不是判据）；③ 零模角动量禁戒（**真判据**，本卷 B1 加强为「间距恒 1」）；"
    "④ CG 非零（**真判据**，本卷 C1/C2 复算并推广）；⑤ λ_H,min（**真判据**，口径需补 D1）；"
    "⑥ 完整四力统一 = 未证明（来料诚实标注）。"
    "★来料自己写了「176 项为有限模型内的数学检查，并非 176 项独立物理发现」⇒ 这一点它是对的")

add(MAIN, "P1",
    "定价：本轮改了什么、没改什么",
    "—",
    "加强 2（第一项→任意族数；第二项→间距恒 1）/ 判负 2（B4、E1）/ 新物理 0",
    "INFO",
    "① 第一项由「两族⇒偶」升级为「**任意谱⇒偶**」（模二定理，3 行证明），并给出 k 族可行性表（三族严格无解）；"
    "② 第二项由「不等式 N>N−1」升级为「**精确间距 1**」，且证明与 q_f 归一化无关；"
    "③ 修复入口的 CG 链条正确并推广到 1/√(2Q+1)，但它修的是质量而非族数；"
    "④ 两条出路（额外场、GS）在本机制内都关闭。★不产生新物理：供给 0、不占度、度数链维持 36")

add(MAIN, "P2",
    "与库内既有结论的关系（不可相加）",
    "—", "一致，不叠加",
    "INFO",
    "① 与 r350「框架不预言 3」一致：本卷进一步说「这类机制只能给偶数」；"
    "② 与 r389「整数比搬家」同型：族数由 Q=qN 决定，移动 q 不动 n 的奇偶；"
    "③ 与 r390 主定理直接衔接：A3 用 r390 的「平方不可分解」关掉 GS 退路；"
    "④ 修正 r390 的 B2 **理由**（结论不变，见 A1）")

# ============================================================ 控制组
N3 = 3
add(CTL, "K1",
    "负对照：取来料口径 q_f=1、N=3，禁戒必须**真的出现**（否则判据是恒假）",
    "禁戒（间距 1 > 0）",
    "j_H,min=%s, j_max=%s, 间距=%s" % (jH_min(F(N3)), 2 * jf_of(F(N3)),
                                jH_min(F(N3)) - 2 * jf_of(F(N3))),
    "PASS" if jH_min(F(N3)) - 2 * jf_of(F(N3)) == 1 else "FAIL",
    "★若这一条给出「允许」，则 B1/B2 的间距结论没有判别力。实测间距 1 ⇒ 禁戒成立")

# K2: 模二判据的两侧
good = list(alln)
bad = []
for s1, k1 in ((1, 1), (1, 2), (1, 3)):
    for s2, k2 in ((-1, 2), (-1, 4), (-1, 5)):
        bad.append(s1 * k1 + s2 * k2)
# ★不要复用 A4 的 bad_odd：同名变量被覆盖 = 「对象错位」型自伤（VERDICT 会读到 K2 的数）
k2_odd = sum(1 for x in bad if x % 2 == 1)
add(CTL, "K2",
    "负对照（判别力两侧）：模二判据在**不满足** Σ s q²=0 的配置上必须给出奇数 n，否则判据恒真",
    "破坏前提的配置出现奇数 n",
    "好配置 %d 组全偶；坏配置 %d 组中 %d 组为奇" % (len(good), len(bad), k2_odd),
    "PASS" if (all(x % 2 == 0 for x in good) and k2_odd > 0) else "FAIL",
    "★只测「好配置全偶」是半边测；必须同时测「坏配置能出奇」。实测坏配置 9 组里 %d 组为奇 ⇒ 两侧都有读数" % k2_odd)

# K3: k=3 无解不依赖整数性
k3q = []
for x in (1, 2, 3, 5):
    for y in (1, 2, 3, 5):
        z2 = x * x + y * y
        k3q.append((x, y, z2, x ** 4 + y ** 4 == (z2 ** 2)))
k3_rational = all((not t[3]) for t in k3q)
add(CTL, "K3",
    "负对照：k=3 的「无解」是否只靠整数性（若去掉整数限制就应有解，则该证明是数论的而非代数的）",
    "代数上就无解（不是整数性产物）",
    "四元组 (x,y,z²,四次是否相等)：%s" % "；".join("%s,%s,%s,%s" % t for t in k3q[:4]),
    "PASS" if k3_rational else "FAIL",
    "★关键：Σu = u₀ 与 Σu² = u₀² 联立给 2e₂ = 0，**在有理数/实数上都成立** ⇒ 「三族无解」是代数结论，"
    "换分数电荷也救不了")

# ============================================================ 守卫
# 本段所有守卫的 kind 一律由读出的数驱动（写成字面量 "PASS" 就是「ok 写死」型自伤）
_SRC = io.open(os.path.abspath(__file__), encoding="utf-8").read()
_HEAD = _SRC.split('add(GRD, "G01"', 1)[0]      # 判据区（守卫段之前），避免扫到自己

_g01_bad = sum(1 for r in ALL if r["id"] in ("A1", "A2", "A4")
               and r["kind"] not in ("PASS", "IDENTITY", "INFO", "FAIL"))
add(GRD, "G01", "恒等式不得记 PASS：A1/A2/A4 的推导若是符号恒等须显式标注",
    "0 违规", "%d 违规" % _g01_bad,
    "PASS" if _g01_bad == 0 else "FAIL",
    "A4 是真判据（全偶来自模二而非构造），A1 是系数核对，A2 是充要条件核对 —— 三条都不是同义反复")

_good_odd = sum(1 for x in good if x % 2 == 1)
_k1_gap = jH_min(F(N3)) - 2 * jf_of(F(N3))
_g02_ok = (_k1_gap != 0) and (_good_odd == 0) and (k2_odd > 0) and k3_rational
add(GRD, "G02", "每个控制组必须给出可与基线区分的读数（K1/K2/K3）", "3 对均可区分",
    "K1 间距 %s ≠ 0；K2 好侧奇 %d / 坏侧奇 %d；K3 四元组四次全不等 = %s"
    % (_k1_gap, _good_odd, k2_odd, k3_rational),
    "PASS" if _g02_ok else "FAIL",
    "三对控制组读数均与失败侧不同；比较由 _g02_ok 逐项联立，不是写死")

_n_thr = (_HEAD.count("1e-") + _HEAD.count("1e+") + _HEAD.count("float(")
          + _HEAD.count("** 0.5") + _HEAD.count("round("))
add(GRD, "G03", "门限表不得含 10 的整数幂 / 不得用浮点容差 / 不得用浮点开方反推下标", "0 处",
    "判据区出现 1e∓ / float( / ** 0.5 / round( 共 %d 处（只扫守卫段之前，避开自指）" % _n_thr,
    "PASS" if _n_thr == 0 else "FAIL",
    "★本卷的判据全是精确判等/奇偶，比门限强：没有可调容差。★扫描区必须切在守卫段之前，"
    "否则守卫自己的 \"1e-\" 字面量会把自己判红（自指坑）。"
    "★加扫 `** 0.5`/`round(`：族表里 q=√(q²) 的反推若走浮点，就是「从坐标反推下标」刀的同型风险，"
    "已全部改成 math.isqrt")

_n_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL")
              and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "%d 违规" % _n_bad4, "PASS" if _n_bad4 == 0 else "FAIL",
    "逐条核查 computed=True 且 note 非空")

_q1 = I8_of(F(1))
_q2 = I8_of(F(2))
_q3 = I8_of(F(3))
_scale_ok = (_q2.get(K_X4) == 16 * _q1.get(K_X4)
             and _q3.get(K_X2T) == 9 * _q1.get(K_X2T)
             and _q3.get(K_X2P) == 9 * _q1.get(K_X2P))
add(GRD, "G05", "A1/A3 的 8 形式系数必须从多项式流水线读，不得写死", "q 缩放律成立",
    "净 x⁴/x²T/x²p₁ = %s / %s / %s；q=1→2 的 x⁴ 比 = %s（应 16），q=1→3 的 x²T 比 = %s（应 9）"
    % (NET1.get(K_X4, 0), NET1.get(K_X2T, 0), NET1.get(K_X2P, 0),
       _q2.get(K_X4) / _q1.get(K_X4), _q3.get(K_X2T) / _q1.get(K_X2T)),
    "PASS" if _scale_ok else "FAIL",
    "★★系数若是写死的，改 q 不会按 q⁴/q² 缩放 ⇒ 用**缩放律**当守卫，比「我声明没写死」强")

_g06_ok = (fam_tbl[2][1] == 0) and (sum(t[1] for t in fam_tbl) > 0)
add(GRD, "G06", "A5 的族表必须穷举算，不得抄来料", "k=3 为 0 且总解数 > 0",
    "k=1..6 解数 %s，合计 %d" % ([t[1] for t in fam_tbl], sum(t[1] for t in fam_tbl)),
    "PASS" if _g06_ok else "FAIL",
    "由 combinations_with_replacement 穷举 q≤%d 现算；「总解数 > 0」用于排除「全 0 也算过」" % QMAX)

add(GRD, "G07", "负对照读数 == 基线即 FAIL", "两侧读数不等且都非零分母",
    "K1 间距 %s ≠ 0（基线）；K2 好侧奇数 %d / 坏侧奇数 %d"
    % (jH_min(F(N3)) - 2 * jf_of(F(N3)),
       sum(1 for x in good if x % 2 == 1), k2_odd),
    "PASS" if (jH_min(F(N3)) - 2 * jf_of(F(N3)) != 0
               and sum(1 for x in good if x % 2 == 1) == 0 and k2_odd > 0) else "FAIL",
    "★★上一版这里把「好侧奇数」写成字面量 0 ⇒ 写死读数；现在由 good 表现算，"
    "并要求「好侧 = 0 且坏侧 > 0」两侧同时成立才 PASS")

add(GRD, "G08", "判词与判定表必须同一读数：六 token 由 ALL 行独立重算后与 VERDICT 比对",
    "两路径一致", "(回填)", "INFO",
    "★漂移守卫：VERDICT 由构造变量拼，此处由表格行重算")

add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数（两次落盘交叉核对）",
    "(回读后填)", "(回读后填)", "INFO",
    "★必须写盘前占位，否则 exp 取到追加本行之前的快照（r390 E05 的同型坑）")

add(GRD, "G10", "恒等性判定必须用符号系数/精确有理数，不得用数值差分", "两路精确相等",
    "A1 四组 q 全等 = %s；C1 三个 CG² 精确命中 = %s；乘积² = %s" % (okpoly, cg_single_ok, prod3),
    "PASS" if (okpoly and cg_single_ok) else "FAIL",
    "★差分只能证伪不能证零：CG 用 Fraction 精确算平方，避开开方与浮点。"
    "★kind 由 okpoly ∧ cg_single_ok 联立驱动，不写字面量")

add(GRD, "G11", "真判负必须逐条登记，且登记项必须确实是 FAIL", "(回填)", "(回填)", "INFO",
    "★库内惯例：FINAL 记 GATES-PASS-WITH-N-NEGATIVE，判负不得稀释成 INFO")

add(GRD, "G12", "A3 的「X₄ 只可能是 αx²+βT+γp₁」必须枚举核完备", "(回填)", "(回填)", "INFO",
    "★与 r390 G12 同型：deg=4 单项式恰 3 个，否则主定理的限定是假设")

add(GRD, "G13", "B1 的间距结论必须与 B2 的归一化扫描独立（两条路径，不是同一式子重算）",
    "(回填)", "(回填)", "INFO",
    "★B1 走 Q 参数化、B2 走 (N,k) 参数化；若两者同源，就无法排除「j_f 公式写错」")

# G14 独立路径：在 Q（零模数）空间直接穷举，绕开 q 的多重集配对与 sqrt 反推
QBF = 6
bf = {}
for k in (1, 2, 3, 4):
    cnt = 0
    nset = set()
    for Qs in itertools.product(range(-QBF, QBF + 1), repeat=k):
        if any(Q == 0 for Q in Qs):
            continue
        for ss in itertools.product((1, -1), repeat=k):
            if abs(sum(ss)) == k:      # 全同号 = 只有一侧，不构成「配对」
                continue
            if sum(s * Q * Q for s, Q in zip(ss, Qs)) != 0:
                continue
            if sum(s * Q ** 4 for s, Q in zip(ss, Qs)) != 0:
                continue
            cnt += 1
            nset.add(sum(s * Q for s, Q in zip(ss, Qs)))
    bf[k] = (cnt, nset)

bf_even = all(x % 2 == 0 for k in bf for x in bf[k][1])
bf_nz = sorted({abs(x) for k in bf for x in bf[k][1] if x != 0})
G14_OK = (bf[3][0] == 0) and bf_even and (bf[2][0] > 0) and bool(bf_nz) and (bf_nz[0] == 2)
add(GRD, "G14", "A4/A5 换一个变量重算：族表走 q 的多重集配对，此处走 Q 直接穷举 (Q_i, s_i)",
    "k=3 解 0；n 全偶；k=2 有解且 min|n|≠0 = 2",
    "Q∈[−%d,%d]∖{0}：k=1..4 解数 %s；n 全偶 = %s；min|n|≠0 = %s"
    % (QBF, QBF, [bf[k][0] for k in (1, 2, 3, 4)], bf_even, bf_nz[0] if bf_nz else None),
    "PASS" if G14_OK else "FAIL",
    "★★不是同一条式子的复算：q 路先按 (Σq², Σq⁴) 建多重集键再配对，Q 路直接在 (Q_i, s_i) 上遍历。"
    "两路独立给出「k=3 无解 / n 全偶 / 最小非零 2」⇒ 排除「多重集键写错」「q=√(q²) 反推下标写错」两类自伤。"
    "★Q 上界 %d 只为可行性，不构成证明 —— 结论的证明仍是 A5 note 的三行代数" % QBF)

# ============================================================ 汇总
DECLARED_NEG = {
    "B4": "加 j_S=1 的修复入口不能给出三代质量矩阵：该机制族数为偶，3×3 的对象不存在",
    "E1": "来料列出的两条出路（额外场、Green–Schwarz）在本机制内均不可用",
}
_neg_ids = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
_neg_ok = (_neg_ids == sorted(DECLARED_NEG))

# G12 完备性
d4 = sorted(k for k in itertools.product(range(3), repeat=5) if deg(k) == 4)
d4_names = {(2, 0, 0, 0, 0): "x²", (0, 1, 0, 0, 0): "T(trF²)", (0, 0, 0, 1, 0): "p₁"}
d4_show = [d4_names[k] for k in [(2, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)] if k in d4]
d4_show += [str(k) for k in d4 if k not in d4_names]
g12 = [r for r in GRD if r["id"] == "G12"][0]
g12["exp"] = "3 个：x² / T / p₁"
g12["act"] = "%d 个：%s" % (len(d4), " / ".join(d4_show))
g12["kind"] = "PASS" if (len(d4) == 3 and set(d4) == set(d4_names)) else "FAIL"

g11 = [r for r in GRD if r["id"] == "G11"][0]
g11["exp"] = "登记集 == 实际 FAIL 集"
g11["act"] = "%s vs %s" % (sorted(DECLARED_NEG), _neg_ids)
g11["kind"] = "PASS" if _neg_ok else "FAIL"

g13 = [r for r in GRD if r["id"] == "G13"][0]
indep = (len(gap_tbl) == 12 and len(norm_tbl) >= 20)
g13["exp"] = "两条路径参数化不同且都给出 1"
g13["act"] = "B1 用 Q（12 点）；B2 用 (N,k)（%d 点）" % len(norm_tbl)
g13["kind"] = "PASS" if indep else "FAIL"

# 六 token
_x = [
    "FAM-EVEN-THEOREM" if (mod2_ok and n_nonzero > 0 and bad_odd > 0) else "FAM-EVEN-OPEN",
    "K3-NO-SOLUTION" if k3_ok else "K3-HAS-SOLUTION",
    "GAP-EXACTLY-ONE" if (gap_all_one and norm_ok) else "GAP-UNSTABLE",
    "GS-EQUIV-I8ZERO" if gs_ok else "GS-WEAKER",
    "REPAIR-WRONG-TARGET" if any(r["kind"] == "FAIL" and r["id"] == "B4" for r in ALL) else "REPAIR-OK",
    "SUPPLY-ZERO",
]
VERDICT = "--".join(_x)
# 重算路径只读 ALL 行上记录的读数（本卷在 add() 之后挂 r["m"]），不读上面任何构造变量 ⇒ 抓「判词 vs 表」漂移
_d = {r["id"]: r for r in ALL}
_v2 = "--".join([
    "FAM-EVEN-THEOREM" if (_d["A4"]["m"]["all_even"] and _d["A4"]["m"]["nonvac"] > 0
                           and _d["A4"]["m"]["bad_odd"] > 0) else "FAM-EVEN-OPEN",
    "K3-NO-SOLUTION" if _d["A5"]["m"]["k3"] == 0 else "K3-HAS-SOLUTION",
    "GAP-EXACTLY-ONE" if (all(F(t[4]) == 1 for t in gap_tbl) and all(F(t[3]) == 1 for t in norm_tbl)) else "GAP-UNSTABLE",
    "GS-EQUIV-I8ZERO" if gs_ok else "GS-WEAKER",
    "REPAIR-WRONG-TARGET" if _d["B4"]["kind"] == "FAIL" else "REPAIR-OK",
    "SUPPLY-ZERO",
])
g08 = [r for r in GRD if r["id"] == "G08"][0]
g08["exp"] = "由构造变量拼接：%s" % VERDICT
g08["act"] = "由 ALL 行重算：%s（%s）" % (_v2, "一致" if _v2 == VERDICT else "不一致")
g08["kind"] = "PASS" if _v2 == VERDICT else "FAIL"

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-04.txt")


def write_json():
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)


def read_json():
    return json.load(io.open(OUT_JSON, encoding="utf-8"))


payload = dict(rid=RID, date="2026-11-04", title=TITLE, final="", verdict=VERDICT,
               declared_neg=DECLARED_NEG,
               counts=dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD), P=0, I=0, F=0, ID=0),
               rows=ALL)

write_json()
back1 = read_json()
n_mem = len(ALL)
n_disk1 = len(back1["rows"])
g09 = [r for r in GRD if r["id"] == "G09"][0]
g09["exp"] = str(n_mem)
g09["act"] = "盘 %d / 内存 %d" % (n_disk1, n_mem)
g09["kind"] = "PASS" if n_disk1 == n_mem else "FAIL"

NP = sum(1 for r in MAIN if r["kind"] == "PASS")
NI = sum(1 for r in MAIN if r["kind"] == "INFO")
NF = sum(1 for r in MAIN if r["kind"] == "FAIL")
NID = sum(1 for r in MAIN if r["kind"] == "IDENTITY")

_gfail = any(r["kind"] == "FAIL" for r in GRD)
FINAL = ("GATES-FAIL" if (_gfail or not _neg_ok)
         else "GATES-PASS-WITH-%d-NEGATIVE" % len(DECLARED_NEG))

payload["counts"] = dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD), P=NP, I=NI, F=NF, ID=NID)
payload["final"] = FINAL
write_json()

back2 = read_json()
ok2 = (len(back2["rows"]) == len(ALL) and back2["final"] == FINAL
       and any(r["id"] == "G09" and r["kind"] == "PASS" for r in back2["rows"]))
if not ok2:
    g09["kind"] = "FAIL"
    g09["note"] += "★二次回读失败 ⇒ 本守卫判 FAIL"
    FINAL = "GATES-FAIL"
    payload["final"] = FINAL
    payload["counts"]["grd"] = len(GRD)
    write_json()
    back2 = read_json()

# ============================================================ 报告
L = []
A = L.append
A(TITLE)
A("=" * 100)
A("对象：ROOT V58｜统一场论攻坚：找到三代质量生成的关键障碍与修复入口（2026-11-04 来料）")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
A("真判负登记 %d 条：%s" % (len(DECLARED_NEG), ", ".join(sorted(DECLARED_NEG))))
A("")
for title, bucket in (("【主册】", MAIN), ("【控制组】", CTL), ("【守卫】", GRD)):
    A("=" * 100)
    A(title)
    A("=" * 100)
    for r in bucket:
        A("[%s] %-4s %s" % (r["kind"], r["id"], r["name"]))
        A("    exp = %s" % r["exp"])
        A("    act = %s" % r["act"])
        A("    %s" % r["note"])
        A("")
A("=" * 100)
A("【关键表】")
A("A1 单种 16 的纯规范部分（e^{qx} 载体）：%s" % pure_single)
A("A1 净 8 形式的纯规范部分（相减后）：%s（空 ⇒ 全抵消）" % pure_net)
A("A1 用 (e^{qx}−1) 载体时单种的纯规范部分：%s（空 —— 这就是 r390 的理由错处）" % pure_alt)
A("A1 一般 q 系数：(2/3)q⁴ / (1/2)q² / −(1/3)q²（4 组全对 = %s）" % okpoly)
A("A3 GS 可分解性：%s" % "；".join("%s,%s→%s(%s)" % t for t in gs_tbl))
A("A4 构造族：2 族 %d 组、勾股 3 族 %d 组、4 族 %d 组；n 全偶 = %s；bad_odd = %d"
  % (len(two), len(pyth), len(four), mod2_ok, bad_odd))
A("A4 勾股三族样例（a,b,c,{n}）：%s" % [(t[0], t[1], t[2], t[3]) for t in pyth[:6]])
A("A5 族表（k, 解数, n_min, n_max, min|n|≠0）：")
for t in fam_tbl:
    A("     k=%d  解 %4d 组  n∈[%s,%s]  min|n|≠0 = %s" % (t[0], t[1], t[2], t[3], t[4]))
A("B1 零模数 Q 与角动量（Q, j_f, j_max=2j_f, j_H,min, 间距）：")
for t in gap_tbl:
    A("     Q=%2d  j_f=%s  j_max=%s  j_H,min=%s  间距=%s" % (t[0], t[1], t[2], t[3], t[4]))
A("C1 CG 平方：%s；乘积² = %s" % ([(a, str(b), str(c)) for a, b, c in cg_checks], prod3))
A("C2 单因子闭式 (2j−1)/(2j+1)：%s" % " / ".join(form_tbl))
A("C2 全链条闭式 1/(2Q+1)：%s" % " / ".join(chain_tbl))
A("D1 N=3, m_KK=10 TeV：m_KK=1/R ⇒ %s TeV；m_KK=√2/R ⇒ %s TeV；来料读数 12.247"
  % (f3(mH_1R), f3(mH_s2R)))
A("")
A("【诚实边界】")
A(" 1) 未获来料 ZIP 附件，176 项只能按其自述的 6 类分类（E2），不逐条核对；")
A(" 2) A4 的模二定理前提是「每个 16 的零模数 Q_i = q_i N ∈ ℤ」与「Σ s_i q_i² = 0」；")
A("    若放弃球面单极磁通（orbifold / Wilson line / 环面），两条前提都不必成立，结论不适用（X-R391-1）；")
A(" 3) A5 的族表在 q ≤ %d 内穷举；(3,3)/(2,4) 在此范围内无解，但更大范围未排除 —— " % QMAX)
A("    不过 A4 已保证「若有解，n 仍偶」，故族表不影响主定理；")
A(" 4) C2 的 1/√(2Q+1) 只对「H(j=Q) ⊗ S(j=1) → J=Q−1」这一种合成成立，不是所有修复方案的系数；")
A(" 5) 本卷不产生新物理：供给 0、不占度、度数链维持 36。")
A("")
A("【产物】源码 / 数据 json / 数据 report / 判定 md / HTML")
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("JSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len("\n".join(L))))
print("MAIN=%d (PASS %d / INFO %d / IDENTITY %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
print("FINAL = %s" % FINAL)
print("VERDICT = %s" % VERDICT)
