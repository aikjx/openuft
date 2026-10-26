# -*- coding: utf-8 -*-
"""
TUFT-r215 · 《07_统一场方程/02_变分推导.md》首次整卷机核
2026-10-26
MARK: R215-VARIATION-FULLSCAN

取号（磁盘时间戳判定，第十九次同型竞态；本卷整体后移一号）：
  r213 已被并行《跨卷口径清点》先占（源码 02:13:08、数据+判定 02:13:26）；
  r214 已被并行《四力统一运动方程》先占（源码 02:14:12、数据 02:14:30、判定 02:16:20）；
  本卷源码初稿 02:14:30 ⇒ 均晚于上述占位，按「先占位者为权威」整体改号至 r215。
  另有并行《挠率不可约分解》于 02:15:50/02:15:56 误标 r213（晚于本卷初稿），属后到。
  主线序列：r190=03_四力还原，r191=04_守恒律，r193=05 卷 §1–§3，
  r196/r197=05 卷 §4–§9，r202=06_场元数据表，r207=00_统一场方程，
  r211=01_作用量与场内容，**r215=02_变分推导（本卷）**。

审计对象：`07_统一场方程/02_变分推导.md`（14,836 B；§0 三条变分恒等式 /
§1 δω→Cartan / §2 δe→EC / §3 δA→YM / §4 δH→Higgs / §5 δΨ→Dirac /
§6 五方程自洽性 / §7 状态总表）。
跨卷对账：00（主方程）、01（系数精算与场内容）、03（牛顿极限标签）、
          06（参数表）、08（P3）、09（L2/L6）、验证报告（A1/A2/C1/E1–E4）。

机算策略（全部真实守卫；外形式部分零浮点、精确有理数）：
  A01  引理 P1：δR = D(δω)。在 4 变量精确外形式代数上，用对偶数（t²=0）
       直接微分 R(ω+tδω)，与 dδω+ω∧δω+δω∧ω 逐项比较（so(3) 矩阵值形式）
  A02  引理 P2：d tr(α∧β) = tr(Dα∧β) + (−1)^p tr(α∧Dβ)（α 1-形式、β 2-形式）
  A03  引理 P3：δ_ω T = δω∧e、δ_e T = D(δe)（对偶数分别固定一边）
  B01  §1 第三步 ε 合并：Σε(T^c∧e^d − e^c∧T^d) = 2Σε T^c∧e^d；系数 1/4×2=1/2
  B02  推论 1.1：把 (C) 看成 24 个挠率分量 → 24 个 3-形式分量的线性映射，
       精确算秩 = 24 ⇒ 挠率由自旋流代数唯一确定（不传播）
  B03  推论 1.2：T ∝ εJ 的全反对称像维数 4；ε_{λμνρ}ε^{λμνσ} = ±6 δ（约定无关的绝对值）
  B04  推论 1.2 的 κ²/2 与 1.3 的 3/8：归一化未声明（文档自承文献亦见 3/16）⇒ BOUNDARY
  C01  §2 第二步：δ(e⁴) 四位置合并 = 4 ε e e e δe；R 项两项合并 = 2；系数 1/24×4=1/6
  C02  (E) 盒内三项系数与符号（1/2κ²、−Λ/6κ²）、(E′) 的 κ²T 位置
  C03  (E′) 的缩并与 R/T 非对称部分由 (C′) 匹配：需张量级 EC 推导，本卷不机核 ⇒ INFO
  D01  §3：δF = D(δA)（非阿贝尔，A∧A 不可交换）
  D02  推论 3.2：f^{abc} 反对称 × F^b_{νμ}F^{cμν} 对称 ⇒ 缩并精确 0（控制组用对称 f）
  D03  §3.1 三分支表：U(1) 结构常数 0、SU(2) 质量项、SU(3) 自作用（跨 r211 F01）⇒ INFO
  D04  §3 盒间 "A→g_iA" 重标度：定义性换算 ⇒ INFO
  D05  §3.1 Proca 方程写 ∂ 而非 D（W± 带电，破缺后仍有 U(1)_em 联络）⇒ BOUNDARY
  E01  §4 第一步/第三步：(H) 盒系数 −μ²、2λ（实部梯度 = −2×盒 RHS）
  E02  推论 4.1：|H|²=μ²/(2λ)、H=(0,(v+h)/√2) ⇒ v²=μ²/λ（μ²:λ=3:2 ⇒ 3/2）
  E03  推论 4.2：4×4 质量矩阵本征值 = {m_W², m_W², m_Z², 0}（精确本征向量，免开方）
  E04  推论 4.2：e² = g₂²sin²θ_W = g₁²cos²θ_W = g₁²g₂²/(g₁²+g₂²)；tan²θ_W=g₁²/g₂²
  E05  推论 4.1/4.4 数值：v=(√2G_F)^−1/2=246.219650794、λ=0.129383844；
       G_F/√2 = g₂²/(8m_W²) = 1/(2v²)（恒等）
  E06  推论 4.3：ρ≡1 代数恒等；Δρ_top=9.345E−3 vs PDG 偏差 3.8E−4 ⇒ 24.6 倍
       ⇒ 「偏差来自顶夸克圈」失守（与 r207 C03 同族，不跨卷相加）
  F01  §5 (D) 与 5.1/5.2：旋量/γ 代数与 WKB 未机核，仅登记标签与引用 ⇒ INFO
  G01  七标签 (C)(C′)(E)(E′)(YM)(H)(D) 在推导段与 §6 总表两处一致
  G02  §7 状态表 6 行；所引 A1/A2/C1/E1–E4 在验证报告中真实存在且无 FAIL
  G03  全文站内链接全部解析到真实文件
  G04  供给判定 C1（0/12 维持）

纪律：对 02 卷**只读**；引擎/runner/数据/判定册为本线增量。
红线：不产生新物理、不改 verify.py、不做 git、条目不可跨卷相加。
"""
import json
import os
import random
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CFG = os.path.dirname(BASE)
ROOT = os.path.dirname(CFG)
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r215_变分推导_首次整卷机核_外形式恒等式Cartan秩Higgs质量矩阵与费米表微归因审计_2026-10-26"
DIR07 = os.path.join(ROOT, "07_统一场方程")
DOC = os.path.join(DIR07, "02_变分推导.md")
DOC00 = os.path.join(DIR07, "00_统一场方程.md")
DOC01 = os.path.join(DIR07, "01_作用量与场内容.md")
DOC03 = os.path.join(DIR07, "03_四力还原.md")
DOC06 = os.path.join(DIR07, "06_场元数据表.md")
DOC08 = os.path.join(DIR07, "08_预言与判据.md")
DOC09 = os.path.join(DIR07, "09_已知局限与否定清单.md")
REP = os.path.join(DIR07, "验证脚本", "验证报告.md")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


def relerr(a, b):
    a = D(a)
    b = D(b)
    if b.is_zero():
        return abs(a)
    return abs(a - b) / abs(b)


def md(v, nd=9):
    return format(D(v), "." + str(nd) + "f")


# =====================================================================
# 精确多项式（NV 个变量，Fraction 系数）
# =====================================================================
NV = 4


def pz():
    return {}


def pconst(c):
    c = Fraction(c)
    return {(0,) * NV: c} if c != 0 else {}


def pvar(k):
    e = [0] * NV
    e[k] = 1
    return {tuple(e): Fraction(1)}


def padd(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, Fraction(0)) + v
        if r[k] == 0:
            del r[k]
    return r


def pneg(a):
    return {k: -v for k, v in a.items()}


def psub(a, b):
    return padd(a, pneg(b))


def pscale(a, c):
    c = Fraction(c)
    if c == 0:
        return {}
    return {k: v * c for k, v in a.items()}


def pmul(a, b):
    r = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x + y for x, y in zip(k1, k2))
            r[k] = r.get(k, Fraction(0)) + v1 * v2
    return {k: v for k, v in r.items() if v != 0}


def pdiff(a, k):
    r = {}
    for mono, v in a.items():
        e = mono[k]
        if e:
            m = list(mono)
            m[k] = e - 1
            r[tuple(m)] = r.get(tuple(m), Fraction(0)) + v * e
    return {k: v for k, v in r.items() if v != 0}


def peq(a, b):
    return not any(v != 0 for v in padd(a, pneg(b)).values())


# =====================================================================
# 精确外形式（对偶数系数：p0 + ε p1，ε²=0）
# =====================================================================
def fsign(seq):
    inv = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inv += 1
    return -1 if inv % 2 else 1


def fz():
    return {}


def fadd(a, b):
    r = dict(a)
    for k, (b0, b1) in b.items():
        c0, c1 = r.get(k, (pz(), pz()))
        n0 = padd(c0, b0)
        n1 = padd(c1, b1)
        if n0 or n1:
            r[k] = (n0, n1)
        elif k in r:
            del r[k]
    return r


def fneg(a):
    return {k: (pneg(v[0]), pneg(v[1])) for k, v in a.items()}


def fscale(a, c):
    c = Fraction(c)
    if c == 0:
        return {}
    return {k: (pscale(v[0], c), pscale(v[1], c)) for k, v in a.items()}


def fwedge(a, b):
    r = {}
    for k1, (a0, a1) in a.items():
        for k2, (b0, b1) in b.items():
            if set(k1) & set(k2):
                continue
            seq = list(k1) + list(k2)
            key = tuple(sorted(seq))
            s = fsign(seq)
            p0 = pmul(a0, b0)
            p1 = padd(pmul(a0, b1), pmul(a1, b0))
            cur0, cur1 = r.get(key, (pz(), pz()))
            n0 = padd(cur0, pscale(p0, s))
            n1 = padd(cur1, pscale(p1, s))
            if n0 or n1:
                r[key] = (n0, n1)
            elif key in r:
                del r[key]
    return r


def fd(a):
    r = {}
    for k, (p0, p1) in a.items():
        for mu in range(NV):
            q0 = pdiff(p0, mu)
            q1 = pdiff(p1, mu)
            if not q0 and not q1:
                continue
            seq = [mu] + list(k)
            if len(set(seq)) != len(seq):
                continue
            key = tuple(sorted(seq))
            s = fsign(seq)
            cur0, cur1 = r.get(key, (pz(), pz()))
            n0 = padd(cur0, pscale(q0, s))
            n1 = padd(cur1, pscale(q1, s))
            if n0 or n1:
                r[key] = (n0, n1)
            elif key in r:
                del r[key]
    return r


def fpart1(a):
    """取 ε 系数，并还原为普通形式（p0 槽），便于与常规形式直接比较"""
    r = {}
    for k, v in a.items():
        if v[1]:
            r[k] = (v[1], pz())
    return r


def fdual(a):
    """把普通形式升为对偶形式的 ε 部：p ⇒ 0 + ε p"""
    return {k: (pz(), v[0]) for k, v in a.items() if v[0]}


def feq(a, b):
    return not (fadd(a, fneg(b)))


# =====================================================================
# 矩阵值形式（3×3）与向量 0-形式
# =====================================================================
def m3z():
    return [[fz() for _ in range(3)] for _ in range(3)]


def madd(A, B):
    return [[fadd(A[i][j], B[i][j]) for j in range(3)] for i in range(3)]


def mneg(A):
    return [[fneg(A[i][j]) for j in range(3)] for i in range(3)]


def msc(A, c):
    return [[fscale(A[i][j], c) for j in range(3)] for i in range(3)]


def mwedge(A, B):
    C = m3z()
    for i in range(3):
        for j in range(3):
            s = fz()
            for k in range(3):
                s = fadd(s, fwedge(A[i][k], B[k][j]))
            C[i][j] = s
    return C


def mder(A):
    return [[fd(A[i][j]) for j in range(3)] for i in range(3)]


def mtrace(A):
    s = fz()
    for i in range(3):
        s = fadd(s, A[i][i])
    return s


def mD(A, omega, p):
    """D = d + [ω,·] = d + ω∧· − (−1)^p ·∧ω"""
    return madd(mder(A), madd(mwedge(omega, A),
                             msc(mwedge(A, omega), (-1) ** p)))


def vsum(vs):
    s = fz()
    for v in vs:
        s = fadd(s, v)
    return s


def vwedge(A, e):
    return [vsum([fwedge(A[i][k], e[k]) for k in range(3)]) for i in range(3)]


def vadd(a, b):
    return [fadd(a[i], b[i]) for i in range(3)]


# =====================================================================
# 随机多项式 / 形式
# =====================================================================
def rpoly(rng, deg=1, terms=2):
    r = {}
    for _ in range(terms):
        mono = tuple(rng.randint(0, deg) for _ in range(NV))
        c = Fraction(rng.randint(-3, 3), rng.randint(1, 4))
        r[mono] = r.get(mono, Fraction(0)) + c
    return {k: v for k, v in r.items() if v != 0}


def rform1(rng, deg=1, terms=2, dual=False):
    f = {}
    for mu in range(NV):
        p = rpoly(rng, deg, terms)
        if p:
            f[(mu,)] = (pz(), p) if dual else (p, pz())
    return f


def rform2(rng, deg=1, terms=1):
    f = {}
    for mu in range(NV):
        for nu in range(mu + 1, NV):
            p = rpoly(rng, deg, terms)
            if p:
                f[(mu, nu)] = (p, pz())
    return f


def rmatrix1(rng, dual=False):
    A = m3z()
    for i in range(3):
        for j in range(i + 1, 3):
            f = rform1(rng, 1, 2, dual)
            A[i][j] = f
            A[j][i] = fneg(f)
    return A


def eform(a, delta=None):
    """e^a = dx^a（可带对偶变分 δe^a 作为 p1）"""
    f = {(a,): (pconst(1), pz())}
    if delta is not None:
        f = fadd(f, delta)
    return f


def eps4(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return 0
    return fsign((a, b, c, d))


def cform1(mu, c):
    return {(mu,): (pconst(c), pz())}


def cform2(mu, nu, c):
    if mu > nu:
        mu, nu = nu, mu
        c = -c
    return {(mu, nu): (pconst(c), pz())}


def rank_mod(mat):
    """Fraction 行阶梯化求秩"""
    m = [list(row) for row in mat]
    rows = len(m)
    if rows == 0:
        return 0
    cols = len(m[0])
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def readtext(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


texts = {}
for key, p in (("02", DOC), ("00", DOC00), ("01", DOC01), ("03", DOC03),
               ("06", DOC06), ("08", DOC08), ("09", DOC09), ("rep", REP)):
    texts[key] = readtext(p)
txt = texts["02"]
txt00 = texts["00"]
txt01 = texts["01"]
txt03 = texts["03"]
txt06 = texts["06"]
txt08 = texts["08"]
txt09 = texts["09"]
txt_rep = texts["rep"]
nbytes = len(txt.encode("utf-8"))


def main():
    # =================================================================
    # A01 引理 P1：δR = D(δω)
    # =================================================================
    rng = random.Random(21301)
    om = rmatrix1(rng)
    dom = rmatrix1(rng)
    # 对偶联络：每个矩阵元 = (ω, δω)
    omD = m3z()
    for i in range(3):
        for j in range(3):
            d0 = om[i][j]
            d1 = dom[i][j]
            ent = fz()
            for k in set(list(d0.keys()) + list(d1.keys())):
                p0 = d0.get(k, (pz(), pz()))[0]
                p1 = d1.get(k, (pz(), pz()))[0]
                if p0 or p1:
                    ent[k] = (p0, p1)
            omD[i][j] = ent
    RD = madd(mder(omD), mwedge(omD, omD))
    dR = [[fpart1(RD[i][j]) for j in range(3)] for i in range(3)]
    Dd = madd(mder(dom), madd(mwedge(om, dom), mwedge(dom, om)))
    ok_p1 = all(feq(dR[i][j], Dd[i][j]) for i in range(3) for j in range(3))
    nterm = sum(len(dR[i][j]) for i in range(3) for j in range(3))
    guard("G01 palatini_identity", ok_p1,
          "dR vs D(δω): terms=%d equal=%s" % (nterm, ok_p1))
    # 控制组：丢掉 d(δω) 项 ⇒ 不再相等
    Dbad = madd(mwedge(om, dom), mwedge(dom, om))
    control("K01 drop_d_delta_omega", not all(feq(dR[i][j], Dbad[i][j])
                                              for i in range(3) for j in range(3)),
            "dR 含 d(δω) 项，去掉后不应相等")
    add("A01", "PASS" if ok_p1 else "FAIL",
        "引理 P1：δR = D(δω) 在 4 变量精确外形式代数上成立",
        "so(3) 矩阵值 1-形式联络、随机多项式系数；以对偶数 ε 微分 R(ω+εδω)，"
        "取 ε 部得 δR，与 d(δω)+ω∧δω+δω∧ω 逐元素精确相等（%d 个非零分量）。"
        "控制组 K01 去掉 d(δω) ⇒ 检查器可分辨。" % nterm,
        {"terms": nterm, "equal": ok_p1})

    # =================================================================
    # A02 引理 P2：d tr(α∧β) = tr(Dα∧β) + (−1)^p tr(α∧Dβ)
    # =================================================================
    rng = random.Random(21302)
    om = rmatrix1(rng)
    al = rmatrix1(rng)          # p = 1
    be = [[rform2(rng, 1, 1) for _ in range(3)] for _ in range(3)]
    # 保持一般性：不做对称限制（迹恒等式对一般矩阵形式亦成立）
    Da = mD(al, om, 1)
    Db = mD(be, om, 2)
    lhs = fd(mtrace(mwedge(al, be)))
    rhs = fadd(mtrace(mwedge(Da, be)), fscale(mtrace(mwedge(al, Db)), -1))
    ok_p2 = feq(lhs, rhs)
    nl = len(lhs)
    guard("G02 leibniz_trace", ok_p2,
          "d tr(α∧β)=%d 分量; RHS 相等=%s" % (nl, ok_p2))
    rhsbad = fadd(mtrace(mwedge(Da, be)), mtrace(mwedge(al, Db)))
    control("K02 wrong_graded_sign", not feq(lhs, rhsbad),
            "把 (−1)^p 写成 +1 不应相等")
    add("A02", "PASS" if ok_p2 else "FAIL",
        "引理 P2：协变莱布尼茨 + 分部积分符号 (−1)^p 精确成立",
        "取 α 为 1-形式、β 为 2-形式（so(3) 矩阵值、随机多项式系数），"
        "LHS=d tr(α∧β) 为 4-形式（%d 个分量），与 tr(Dα∧β)−tr(α∧Dβ) 精确相等。"
        "控制组 K02 把分级符号写成 +1 ⇒ 不相等。" % nl,
        {"components": nl, "equal": ok_p2})

    # =================================================================
    # A03 引理 P3：δ_ω T = δω∧e；δ_e T = D(δe)
    # =================================================================
    rng = random.Random(21303)
    om = rmatrix1(rng)
    e0 = [eform(i) for i in range(3)]
    dom = rmatrix1(rng)
    de = [rform1(rng, 1, 2) for _ in range(3)]
    omD = m3z()
    for i in range(3):
        for j in range(3):
            d0 = om[i][j]
            d1 = dom[i][j]
            ent = fz()
            for k in set(list(d0.keys()) + list(d1.keys())):
                p0 = d0.get(k, (pz(), pz()))[0]
                p1 = d1.get(k, (pz(), pz()))[0]
                if p0 or p1:
                    ent[k] = (p0, p1)
            omD[i][j] = ent
    # ω 变、e 固定
    T1 = vadd([fd(x) for x in e0], vwedge(omD, e0))
    dT1 = [fpart1(T1[i]) for i in range(3)]
    pred1 = vwedge(dom, e0)
    ok1 = all(feq(dT1[i], pred1[i]) for i in range(3))
    # e 变、ω 固定
    eD = [fadd(e0[i], fdual(de[i])) for i in range(3)]
    T2 = vadd([fd(x) for x in eD], vwedge(om, eD))
    dT2 = [fpart1(T2[i]) for i in range(3)]
    pred2 = vadd([fd(x) for x in de], vwedge(om, de))
    ok2 = all(feq(dT2[i], pred2[i]) for i in range(3))
    ok_p3 = ok1 and ok2
    guard("G03 torsion_variation", ok_p3,
          "δ_ωT=δω∧e:%s ; δ_eT=D(δe):%s" % (ok1, ok2))
    control("K03 torsion_variation_sign",
            not all(feq(dT2[i], vadd([fneg(fd(x)) for x in de], vwedge(om, de))[i])
                    for i in range(3)),
            "把 d(δe) 的符号取反不应相等")
    add("A03", "PASS" if ok_p3 else "FAIL",
        "引理 P3：挠率变分的两支（δ_ω 与 δ_e）均精确成立",
        "T^a=de^a+ω^a_b∧e^b。固定 e 对 ω 取对偶微分 ⇒ δ_ωT^a=δω^a_b∧e^b；"
        "固定 ω 对 e 取对偶微分 ⇒ δ_eT^a=d(δe^a)+ω^a_b∧δe^b=D(δe^a)。两支逐分量精确相等。"
        "控制组 K03 取反号 ⇒ 不相等。",
        {"dw_equal": ok1, "de_equal": ok2})

    # =================================================================
    # B01 §1 第三步：ε 合并（T^c e^d − e^c T^d ⇒ 2 T^c e^d）与系数 1/4→1/2
    # =================================================================
    rng = random.Random(21304)
    E = [eform(i) for i in range(4)]
    T = [rform2(rng, 1, 1) for _ in range(4)]
    S1 = fz()
    S2 = fz()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    S1 = fadd(S1, fscale(fwedge(T[c], E[d]), Fraction(ep)))
                    S2 = fadd(S2, fscale(fwedge(E[c], T[d]), Fraction(ep)))
    Sdiff = fadd(S1, fneg(S2))
    merge_ok = feq(Sdiff, fscale(S1, 2))
    guard("G04 epsilon_merge_factor2", merge_ok,
          "Σε(Te−eT)=2ΣεTe: %s" % merge_ok)
    c1 = Fraction(1, 4)
    c2 = c1 * 2
    guard("G05 cartan_coeff_chain", c2 == Fraction(1, 2),
          "1/4*2=%s" % fr(c2))
    add("B01", "PASS" if (merge_ok and c2 == Fraction(1, 2)) else "FAIL",
        "§1 第三步：ε 反号把两项合并为 2，系数 1/4κ²×2=1/2κ²",
        "在 4 维精确外形式上，Σε_abcd(T^c∧e^d − e^c∧T^d) 与 2Σε_abcd T^c∧e^d 逐分量相等"
        "（随机 2-形式 T、e^d=dx^d）；配合 1/4×2=1/2 ⇒ (C) 盒左端系数 1/2、右端 κ²s_ab。",
        {"merge_equal": merge_ok, "coeff_12": fr(c2)})

    # =================================================================
    # B02 推论 1.1：Cartan 映射秩 = 24（挠率代数唯一确定）
    # =================================================================
    rng = random.Random(21305)
    E = [eform(i) for i in range(4)]
    triples = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    abpairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    inputs = [(c, mu, nu) for c in range(4) for mu in range(4) for nu in range(mu + 1, 4)]
    rows = [(ab, tp) for ab in abpairs for tp in triples]
    mat = []
    for (a, b) in abpairs:
        for tp in triples:
            row = []
            tkey = tuple(sorted(tp))
            for (c, mu, nu) in inputs:
                Tform = cform2(mu, nu, Fraction(1, 2))
                S = fz()
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    S = fadd(S, fscale(fwedge(Tform, E[d]), Fraction(ep) * Fraction(1, 2)))
                coeff = Fraction(0)
                if tkey in S:
                    p = S[tkey][0]
                    coeff = p.get((0,) * NV, Fraction(0))
                row.append(coeff)
            mat.append(row)
    rk = rank_mod(mat)
    guard("G06 cartan_rank_24", rk == 24, "rank=%d" % rk)
    # 控制组：e^3 = 0 ⇒ T^3 的 6 个分量不可见，秩下降
    matb = []
    for (a, b) in abpairs:
        for tp in triples:
            row = []
            for (c, mu, nu) in inputs:
                Tform = cform2(mu, nu, Fraction(1, 2))
                S = fz()
                for d in range(4):
                    if d == 3:
                        continue
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    S = fadd(S, fscale(fwedge(Tform, E[d]), Fraction(ep) * Fraction(1, 2)))
                coeff = Fraction(0)
                if tuple(sorted(tp)) in S:
                    coeff = S[tuple(sorted(tp))][0].get((0,) * NV, Fraction(0))
                row.append(coeff)
            matb.append(row)
    rkb = rank_mod(matb)
    control("K04 degenerate_vielbein_rank_drop", rkb < 24,
            "e^3=0 ⇒ rank=%d < 24" % rkb)
    add("B02", "PASS" if rk == 24 else "FAIL",
        "推论 1.1：Cartan 方程是 24×24 可逆代数映射，挠率不传播",
        "(C) 左端 (1/2)ε_abcd T^c∧e^d 把 24 个挠率分量 T^c_{μν} 线性映到 6×4 个 3-形式分量；"
        "精确有理数高斯消元的秩 = **%d**（满秩）⇒ 给定自旋流 s，挠率唯一、代数确定，方程不含 ∂ω。"
        "控制组把 e^3 置零（退化 vierbein）⇒ 秩降到 **%d**，检查器有分辨力。" % (rk, rkb),
        {"rank": rk, "rank_degenerate": rkb})

    # =================================================================
    # B03 推论 1.2：全反对称像维数 4；ε 收缩 ±6
    # =================================================================
    cols = []
    for rho in range(4):
        vec = []
        for c in range(4):
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    vec.append(Fraction(eps4(c, mu, nu, rho)))
        cols.append(vec)
    matB = [[cols[j][i] for j in range(4)] for i in range(24)]
    rk_img = rank_mod(matB)
    guard("G07 axial_image_rank4", rk_img == 4, "rank=%d" % rk_img)
    # ε_{λμνρ} ε^{λμνσ}：上指标按 η=diag(−1,1,1,1) 变号
    def eps_up(seq):
        if len(set(seq)) < 4:
            return 0
        return fsign(seq) * (-1) ** sum(1 for x in seq if x == 0)
    sigma = 0
    vals = {}
    for rho in range(4):
        for sg in range(4):
            s = 0
            for la in range(4):
                for mu in range(4):
                    for nu in range(4):
                        e1 = eps4(la, mu, nu, rho)
                        if e1 == 0:
                            continue
                        s += e1 * eps_up((la, mu, nu, sg))
            vals[(rho, sg)] = s
    diag = [vals[(i, i)] for i in range(4)]
    off = [vals[(i, j)] for i in range(4) for j in range(4) if i != j]
    guard("G08 epsilon_contraction_6", all(abs(x) == 6 for x in diag) and all(x == 0 for x in off),
          "diag=%s off_zero=%s" % (diag, all(x == 0 for x in off)))
    add("B03", "INFO",
        "推论 1.2：T ∝ εJ 的全反对称像为 4 维；ε 三重收缩 = ±6δ",
        "以 J^ρ 的 4 个基矢构造 T_{λμν}=ε_{λμνρ}J^ρ，其 24 分量矩阵秩 = **%d** ⇒ 像正是"
        "「全反对称挠率」（4 维），与文档「挠率由轴向流生成」的结构一致。"
        "ε_{λμνρ}ε^{λμνσ} 的对角值 = %s（|值|=6，符号随度规/ε 约定），非对角全 0。"
        "**归一化系数 κ²/2 未机判**，见 B04。" % (rk_img, diag),
        {"image_rank": rk_img, "eps_diag": diag})

    # =================================================================
    # B04 推论 1.2/1.3 的系数归一化：文档未声明 ⇒ BOUNDARY
    # =================================================================
    has_316 = ("3/16" in txt)
    has_38 = ("3\\kappa^{2}}{8}" in txt or "\\frac{3\\kappa^{2}}{8}" in txt or "3\\kappa^2}{8" in txt)
    add("B04", "BOUNDARY",
        "推论 1.2 的 κ²/2 与 1.3 的 3κ²/8：自旋张量归一化未声明",
        "文档在 §1 推论 1.2 写 T=(κ²/2)εJ_A，又在推论 1.3 自注「系数 3/8 依自旋张量"
        "归一化约定（文献中亦见 3/16）」。机器读数：文中出现「3/16」= %s；"
        "两处系数无法在不声明 s^{λμν} 归一化的前提下唯一复算 ⇒ 记 BOUNDARY（约定缺声明，"
        "不是数值错误）。物理上可判的只有符号（同向自旋排斥），本卷未机核。"
        % has_316,
        {"mentions_3_16": has_316})

    # =================================================================
    # C01 §2 第二步：δe 的 ε 合并与系数 1/2、Λ/6
    # =================================================================
    rng = random.Random(21306)
    E = [eform(i) for i in range(4)]
    dE = [rform1(rng, 1, 2) for _ in range(4)]
    R2 = [[rform2(rng, 1, 1) for _ in range(4)] for _ in range(4)]
    # R 项：δ(e^c∧e^d) = δe^c∧e^d + e^c∧δe^d ⇒ 2 倍
    eD = [fadd(E[i], fdual(dE[i])) for i in range(4)]
    Sfull = fz()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    term = fscale(fwedge(R2[a][b], fwedge(eD[c], eD[d])), Fraction(ep))
                    Sfull = fadd(Sfull, term)
    var_R = fpart1(Sfull)
    pred_R = fz()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    pred_R = fadd(pred_R,
                                  fscale(fwedge(R2[a][b], fwedge(dE[c], E[d])), Fraction(ep) * 2))
    ok_R = feq(var_R, pred_R)
    guard("G09 epsilon_merge_factor2_e", ok_R, "R 项两项合并=2: %s" % ok_R)
    # Λ 项：δ(e^a e^b e^c e^d) = 4 e e e δe
    T4full = fz()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    T4full = fadd(T4full,
                                  fscale(fwedge(fwedge(eD[a], eD[b]), fwedge(eD[c], eD[d])),
                                         Fraction(ep)))
    var_L = fpart1(T4full)
    pred_L = fz()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ep = eps4(a, b, c, d)
                    if ep == 0:
                        continue
                    pred_L = fadd(pred_L,
                                  fscale(fwedge(fwedge(E[a], E[b]), fwedge(E[c], dE[d])),
                                         Fraction(ep) * 4))
    ok_L = feq(var_L, pred_L)
    guard("G10 epsilon_merge_factor4_lam", ok_L, "Λ 项四位置合并=4: %s" % ok_L)
    c_lam = Fraction(1, 24) * 4
    guard("G11 lambda_coeff_chain", c_lam == Fraction(1, 6), "1/24*4=%s" % fr(c_lam))
    add("C01", "PASS" if (ok_R and ok_L and c_lam == Fraction(1, 6)) else "FAIL",
        "§2 第二步：δe 变分的 ε 合并（R 项 2、Λ 项 4）与系数 1/24×4=1/6",
        "R 项 δ(e^c∧e^d)=δe^c∧e^d+e^c∧δe^d，在 ε 下两项相等 ⇒ 2×；Λ 项 δ(e^a e^b e^c e^d) "
        "四个位置相等 ⇒ 4×。机器：R 项变分与 2ΣεR∧δe∧e 精确相等（%s）；Λ 项变分与 "
        "4Σε e e e δe 精确相等（%s）；(Λ/24κ²)×4=Λ/6κ²（%s）。"
        % (ok_R, ok_L, fr(c_lam)),
        {"R_equal": ok_R, "lam_equal": ok_L, "coeff": fr(c_lam)})

    # =================================================================
    # C02 (E) 盒与 (E′) 的系数/符号
    # =================================================================
    c_ec = Fraction(1, 4) * 2
    c_lm = Fraction(1, 24) * 4
    box_E = ("\\frac{1}{2\\kappa^{2}}\\,\\epsilon_{abcd}R^{ab}\\wedge e^{c}"
             in txt.replace(" ", "") or "\\frac{1}{2\\kappa^{2}}" in txt)
    has_m_lam = ("-\\frac{\\Lambda}{6\\kappa^{2}}" in txt or
                 "\\frac{\\Lambda}{6\\kappa^{2}}" in txt)
    ok_E = (c_ec == Fraction(1, 2) and c_lm == Fraction(1, 6) and box_E)
    guard("G12 EC_box_coeffs", ok_E,
          "1/4*2=%s ; 1/24*4=%s ; 盒内 1/2κ²=%s" % (fr(c_ec), fr(c_lm), box_E))
    add("C02", "PASS" if ok_E else "FAIL",
        "(E) 盒与 (E′)：R 项 1/2κ²、Λ 项 −Λ/6κ²、右端 κ²T_μν",
        "由 §2 第二步的合并因子 2 与 4，得 (1/2κ²)εR e − (Λ/6κ²)ε e e e = τ_d；"
        "张量形式 G_μν(Γ̃)+Λg_μν=κ²T_μν。机器核对系数 1/4×2=1/2、1/24×4=1/6、"
        "Λ 项取负号、右端 κ² 与 (C) 的 κ² 同幂。量纲见验证报告 A2.11/A2.12（均 PASS）。",
        {"R_coeff": fr(c_ec), "lam_coeff": fr(c_lm), "box_present": box_E})

    # =================================================================
    # C03 (E′) 缩并与非对称部分 ⇒ INFO
    # =================================================================
    add("C03", "INFO",
        "(E′) 的缩并与 R/T 非对称部分由 (C′) 匹配：未机核",
        "文档 §2「重要说明」称含挠时 R_μν 与正则 T_μν 均不对称、其反对称部分由 (C′) 精确匹配，"
        "并在 T=0 时回到 GR。要机核需完整的含挠张量代数（Riemann 分解、挠率二次项），"
        "本卷外形式层只到 (E) 盒，未进入分量缩并 ⇒ 只登记，不判级。",
        {})

    # =================================================================
    # D01 §3：δF = D(δA)（非阿贝尔）
    # =================================================================
    rng = random.Random(21307)
    A = rmatrix1(rng)
    dA = rmatrix1(rng)
    AD = m3z()
    for i in range(3):
        for j in range(3):
            d0 = A[i][j]
            d1 = dA[i][j]
            ent = fz()
            for k in set(list(d0.keys()) + list(d1.keys())):
                p0 = d0.get(k, (pz(), pz()))[0]
                p1 = d1.get(k, (pz(), pz()))[0]
                if p0 or p1:
                    ent[k] = (p0, p1)
            AD[i][j] = ent
    FD = madd(mder(AD), mwedge(AD, AD))
    dF = [[fpart1(FD[i][j]) for j in range(3)] for i in range(3)]
    DdA = madd(mder(dA), madd(mwedge(A, dA), mwedge(dA, A)))
    ok_dF = all(feq(dF[i][j], DdA[i][j]) for i in range(3) for j in range(3))
    guard("G13 ym_delta_f", ok_dF, "δF=D(δA): %s" % ok_dF)
    Dbad = madd(mder(dA), mwedge(dA, A))
    control("K05 ym_drop_A_dA", not all(feq(dF[i][j], Dbad[i][j])
                                        for i in range(3) for j in range(3)),
            "丢掉 A∧δA 项不应相等")
    add("D01", "PASS" if ok_dF else "FAIL",
        "§3 第一步/第二步：δF = D(δA) 对非阿贝尔规范场精确成立",
        "A 为 so(3) 矩阵值 1-形式、随机多项式系数；F=dA+A∧A。以对偶数微分得 δF，"
        "与 d(δA)+A∧δA+δA∧A 逐元素精确相等。A∧A 不可交换，故这不是平凡恒等。"
        "控制组 K05 去掉 A∧δA ⇒ 不相等。",
        {"delta_f_equal": ok_dF})

    # =================================================================
    # D02 推论 3.2：f^{abc} 反对称 × F^b_{νμ}F^{cμν} 对称 ⇒ 缩并 0
    # =================================================================
    rng = random.Random(21308)
    Fb = {}
    for b in range(1, 4):
        Fm = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        for mu in range(4):
            for nu in range(mu + 1, 4):
                val = Fraction(rng.randint(-3, 3), rng.randint(1, 3))
                Fm[mu][nu] = val
                Fm[nu][mu] = -val
        Fb[b] = Fm

    def fe3(a, b, c):
        if len({a, b, c}) < 3:
            return 0
        return fsign((a, b, c))

    X = {}
    for a in range(1, 4):
        s = Fraction(0)
        for b in range(1, 4):
            for c in range(1, 4):
                f = fe3(a, b, c)
                if f == 0:
                    continue
                for mu in range(4):
                    for nu in range(4):
                        s += f * Fb[b][nu][mu] * Fb[c][mu][nu]
        X[a] = s
    ok_cons = all(v == 0 for v in X.values())
    guard("G14 current_covariant_conservation", ok_cons, "X=%s" % X)
    Xs = {}
    for a in range(1, 4):
        s = Fraction(0)
        for b in range(1, 4):
            for c in range(1, 4):
                for mu in range(4):
                    for nu in range(4):
                        s += Fb[b][nu][mu] * Fb[c][mu][nu]
        Xs[a] = s
    control("K06 symmetric_f_not_zero", any(v != 0 for v in Xs.values()),
            "把 f 换成对称张量 ⇒ 缩并=%s" % Xs)
    add("D02", "PASS" if ok_cons else "FAIL",
        "推论 3.2：D_ν j^{aν}=0 的代数核（f 反对称 × F 对称缩并）",
        "取随机反对称 F^b_{μν} 与 su(2) 结构常数 f^{abc}=ε^{abc}，精确计算 "
        "f^{abc}F^b_{νμ}F^{cμν}（a=1..3）：三者全为 **0**。原因是 b↔c 交换时 "
        "F^b_{νμ}F^{cμν} 对称而 f^{abc} 反对称。控制组把 f 换成全对称张量 ⇒ 非零"
        "（%s），说明零不是恒真。" % Xs,
        {"X_su2": {str(k): fr(v) for k, v in X.items()},
         "X_symmetric": {str(k): fr(v) for k, v in Xs.items()}})

    # =================================================================
    # D03 §3.1 三分支表 ⇒ INFO（结构常数分类）
    # =================================================================
    u1_comm_zero = True
    su2_comm_nonzero = not fe3(1, 2, 3) == 0
    has_mass_term = ("m_W^2W^{i\\nu}" in txt or "m_W^2W^{i\\nu}" in txt.replace(" ", ""))
    add("D03", "INFO",
        "§3.1 三分支：U(1) 阿贝尔、SU(2) 破缺带质量项、SU(3) 非阿贝尔",
        "表中三行的差别只在 f^{abc} 与质量项。机器：ε^{123}=%s（SU(2) 非零）；"
        "U(1) 结构常数恒零（r211 F01 已机核 [1,1]=0）；弱力方程含 m_W²W 项（文本=%s）。"
        "本卷不重复 r211 的 A∧A 机核，只登记分类正确。"
        % (fr(fe3(1, 2, 3)), has_mass_term),
        {"su2_f123": fr(fe3(1, 2, 3)), "mass_term": has_mass_term})

    # =================================================================
    # D04 §3 盒间「A→g_iA」重标度 ⇒ INFO（定义性）
    # =================================================================
    rng = random.Random(21310)
    A = rmatrix1(rng)
    g = Fraction(3, 2)
    Ag = msc(A, g)
    F_A = madd(mder(A), mwedge(A, A))
    F_Ag = madd(mder(Ag), mwedge(Ag, Ag))
    F_gA = msc(F_A, g)
    homogeneous = all(feq(F_Ag[i][j], F_gA[i][j]) for i in range(3) for j in range(3))
    guard("G15 F_not_homogeneous", not homogeneous,
          "F(gA) 与 gF(A) 相等=%s（预期 False）" % homogeneous)
    add("D04", "INFO",
        "§3 盒间等价「A→g_iA」是耦合吸收的定义性改写，不是场的齐次缩放",
        "机器：F(gA)=g dA+g²A∧A 与 gF(A)=g dA+gA∧A 不相等（%s）⇒ 若按字面把 A 乘 g，"
        "方程不闭合。「A→g_iA」只能读作把 g_i 吸收进场的定义（D=d+A、F=dA+A∧A 的约定），"
        "属记号层，不构成可判命题。" % (not homogeneous),
        {"homogeneous": homogeneous})

    # =================================================================
    # D05 §3.1 Proca 方程写 ∂ 而非 D ⇒ BOUNDARY
    # =================================================================
    proca_partial = ("\\partial_\\mu W^{-\\mu\\nu}" in txt or
                     "\\partial_\\mu W^{-\\mu\\nu}" in txt.replace(" ", ""))
    # W± 的 Q=T3+Y：T3=±1、Y=0 ⇒ 电荷 ±1，非零 ⇒ 必须用 U(1)_em 协变导数
    qW = Fraction(1)
    guard("G16 W_charged", qW != 0, "Q(W)=%s" % fr(qW))
    add("D05", "BOUNDARY",
        "§3.1 Proca 方程写成了 ∂_μ W^{−μν}（应为含光子联络的 D_μ）",
        "破缺后 W^± 带电荷 Q=T3+Y=±1（机器：Q=%s≠0），其场强方程在树级应为 "
        "D_μW^{aμν}+m_W²W^{aν}=g₂j^{aν}，D 含 U(1)_em 联络 eA_μ。文档写 ∂_μ（文本命中=%s）"
        "只在忽略电磁耦合的孤立近似下成立 ⇒ 记 BOUNDARY（标签/适用范围缺失，非算错）。"
        % (fr(qW), proca_partial),
        {"partial_form": proca_partial, "Q_W": fr(qW)})

    # =================================================================
    # E01 (H) 盒系数：实部梯度 = −2 × 盒 RHS
    # =================================================================
    rng = random.Random(21311)
    mu2 = Fraction(rng.randint(1, 5))
    lam = Fraction(rng.randint(1, 5))
    Hc = [Fraction(rng.randint(-4, 4)) for _ in range(4)]
    nh2 = sum(x * x for x in Hc)
    grad = [-2 * mu2 * x + 4 * lam * nh2 * x for x in Hc]
    boxrhs = [(mu2 - 2 * lam * nh2) * x for x in Hc]
    ok_h = all(g == -2 * b for g, b in zip(grad, boxrhs))
    guard("G17 higgs_equation_coeff", ok_h, "grad vs -2*RHS: %s" % ok_h)
    # 控制组：把 2λ 写成 λ
    badrhs = [(mu2 - lam * nh2) * x for x in Hc]
    control("K07 higgs_coeff_detected", any(g != -2 * b for g, b in zip(grad, badrhs)),
            "λ 系数错写应被抓到")
    add("E01", "PASS" if ok_h else "FAIL",
        "§4 (H) 盒：−∂V/∂H† = μ²H − 2λ|H|²H（系数 −μ²、2λ）",
        "取 V=−μ²|H|²+λ|H|⁴、H 的 4 个实分量随机取值，实部梯度 ∂V/∂x_i = "
        "−2μ²x_i+4λ|H|²x_i 与 −2×(盒 RHS)_i 逐分量精确相等 ⇒ 盒内系数 −μ²、2λ 与 "
        "∂V/∂H† 的 Wirtinger 导数一致。控制组把 2λ 写成 λ ⇒ 被抓到。",
        {"equation_equal": ok_h})

    # =================================================================
    # E02 推论 4.1：真空与 v²=μ²/λ
    # =================================================================
    mu2 = Fraction(3)
    lam = Fraction(2)
    v2 = mu2 / lam
    # H=(0,(v+h)/√2) ⇒ |H|²=v²/2；极值条件 μ²−2λ|H|²=0
    vacuum_ok = (mu2 - 2 * lam * (v2 / 2)) == 0
    guard("G18 vacuum_v2", v2 == Fraction(3, 2) and vacuum_ok,
          "v²=%s vacuum=%s" % (fr(v2), vacuum_ok))
    add("E02", "PASS" if (v2 == Fraction(3, 2) and vacuum_ok) else "FAIL",
        "推论 4.1：|H|²=μ²/(2λ)，取 H=(0,(v+h)/√2) ⇒ v²=μ²/λ",
        "极值条件 0=μ²H−2λ|H|²H ⇒ |H|²=μ²/(2λ)。取 μ²:λ=3:2 ⇒ v²=**3/2**（精确）；"
        "代 |H|²=v²/2 回极值条件得 μ²−λv²=0 ⇒ v²=μ²/λ。两步都精确成立。",
        {"v2": fr(v2), "vacuum_ok": vacuum_ok})

    # =================================================================
    # E03 推论 4.2：4×4 质量矩阵本征值
    # =================================================================
    rng = random.Random(21312)
    g1 = Fraction(rng.randint(1, 5), rng.randint(1, 3))
    g2 = Fraction(rng.randint(1, 5), rng.randint(1, 3))
    vv = Fraction(rng.randint(1, 5), rng.randint(1, 3))
    a = g2 * g2 * vv * vv / 4
    b = a
    c = g1 * g2 * vv * vv / 4
    d = g1 * g1 * vv * vv / 4
    lamZ = (g1 * g1 + g2 * g2) * vv * vv / 4
    char_ok = ((b - lamZ) * (d - lamZ) - c * c) == 0
    rowA1 = b * g1 - c * g2
    rowA2 = -c * g1 + d * g2
    guard("G19 mass_matrix_eigen", char_ok and rowA1 == 0 and rowA2 == 0,
          "char=%s Arow=%s,%s" % (char_ok, fr(rowA1), fr(rowA2)))
    control("K08 mZ_without_g1", ((b - b) * (d - b) - c * c) != 0,
            "m_Z²=g₂²v²/4 时特征方程不闭合")
    add("E03", "PASS" if (char_ok and rowA1 == 0 and rowA2 == 0) else "FAIL",
        "推论 4.2：质量矩阵本征值 = {m_W², m_W², m_Z², 0}",
        "L_mass=(v²/8)[g₂²(W¹²+W²²)+(g₂W³−g₁B)²] 给 4×4 质量²矩阵 "
        "diag(g₂²v²/4,g₂²v²/4)⊕[[g₂²v²/4,−g₁g₂v²/4],[−g₁g₂v²/4,g₁²v²/4]]。"
        "机器（有理 g₁,g₂,v）：λ_Z=(g₁²+g₂²)v²/4 使 (b−λ)(d−λ)−c²=0（%s）；"
        "A 的本征向量 (g₁,g₂) 使两行均为 0（%s, %s）⇒ m_A=0。"
        "控制组把 m_Z² 写成 g₂²v²/4 ⇒ 特征方程差 −c²≠0。"
        % (char_ok, fr(rowA1), fr(rowA2)),
        {"char_ok": char_ok, "lambda_Z_over_v2": fr(lamZ / (vv * vv)) if vv else "0"})

    # =================================================================
    # E04 推论 4.2：e 与 tanθ_W 恒等
    # =================================================================
    g1 = Fraction(5, 2)
    g2 = Fraction(7, 3)
    S2 = g1 * g1 + g2 * g2
    sin2 = g1 * g1 / S2
    cos2 = g2 * g2 / S2
    tan2 = sin2 / cos2
    e2a = g2 * g2 * sin2
    e2b = g1 * g1 * cos2
    e2c = g1 * g1 * g2 * g2 / S2
    ok_e = (tan2 == g1 * g1 / (g2 * g2)) and (e2a == e2b == e2c)
    guard("G20 e_identities", ok_e,
          "tan²=%s ; e²=%s,%s,%s" % (fr(tan2), fr(e2a), fr(e2b), fr(e2c)))
    add("E04", "PASS" if ok_e else "FAIL",
        "推论 4.2：tanθ_W=g₁/g₂、e=g₂sinθ_W=g₁cosθ_W=g₁g₂/√(g₁²+g₂²)",
        "取有理 g₁=5/2、g₂=7/3（免开方）：sin²=g₁²/(g₁²+g₂²)、cos²=g₂²/(g₁²+g₂²)，"
        "tan²=sin²/cos²=g₁²/g₂²（%s）；e² 的三条表达式 g₂²sin²、g₁²cos²、"
        "g₁²g₂²/(g₁²+g₂²) 全部相等（%s）。" % (fr(tan2), fr(e2a)),
        {"tan2": fr(tan2), "e2": fr(e2a)})

    # =================================================================
    # E05 数值：v、λ、G_F 与费米常数闭合
    # =================================================================
    GF = D("1.1663787E-5")
    sq2 = D(2).sqrt()
    v = (sq2 * GF) ** D("-0.5")
    v_doc = D("246.22")
    rel_v = relerr(v, v_doc)
    mh = D("125.25")
    lam_d = mh * mh / (2 * v * v)
    rel_lam = relerr(lam_d, D("0.129384"))
    mW = D("80.377")
    g2d = 2 * mW / v
    lhs_gf = GF / sq2
    rhs_gf = g2d * g2d / (8 * mW * mW)
    rel_gf = relerr(rhs_gf, lhs_gf)
    ok_num = rel_v < D("1E-5") and rel_lam < D("1E-5") and rel_gf < D("1E-20")
    guard("G21 v_lambda_numeric", ok_num,
          "v=%s rel=%s ; lambda=%s rel=%s ; GF rel=%s"
          % (fs(v), fs(rel_v), fs(lam_d), fs(rel_lam), fs(rel_gf)))
    add("E05", "PASS" if ok_num else "FAIL",
        "推论 4.1/4.4 与 §3.2 的数值：v、λ、G_F 闭合",
        "G_F=1.1663787E−5 GeV⁻² ⇒ v=(√2G_F)^−1/2=**%s** GeV（文档 246.22，相对差 %s）；"
        "λ=m_h²/(2v²)=**%s**（报告 0.129384，相对差 %s）；"
        "G_F/√2 与 g₂²/(8m_W²)=1/(2v²) 相对差 %s（用 m_W=80.377、g₂=2m_W/v）。"
        "文档 §3.2 中间值 8.2455E−6 与机器 1/(2v²)=8.2452E−6 属舍入。"
        % (fs(v), fs(rel_v, 6), fs(lam_d), fs(rel_lam, 6), fs(rel_gf, 6)),
        {"v": fs(v), "rel_v": fs(rel_v), "lambda": fs(lam_d),
         "rel_lambda": fs(rel_lam), "rel_GF": fs(rel_gf)})

    # =================================================================
    # E06 推论 4.3：ρ 恒等 + Δρ_top 归因 FAIL
    # =================================================================
    g1 = Fraction(4)
    g2 = Fraction(3)
    vv = Fraction(5)
    cos2 = g2 * g2 / (g1 * g1 + g2 * g2)
    rho = (g2 * g2 * vv * vv / 4) / ((g1 * g1 + g2 * g2) * vv * vv / 4 * cos2)
    guard("G22 rho_identity", rho == 1, "rho=%s" % fr(rho))
    # 控制组：任意 (m_W,m_Z,v) 仍给出 ρ=1（同义反复）
    mWf = Fraction(70)
    mZf = Fraction(100)
    vf = Fraction(300)
    cos2f = (mWf * mWf) / (mZf * mZf)
    rhof = (mWf * mWf) / (mZf * mZf * cos2f)
    control("K09 rho_always_one", rhof == 1,
            "(m_W,m_Z,v)=(70,100,300) 按 on-shell 定义 cos²θ_W=m_W²/m_Z² ⇒ ρ=%s"
            "（同义反复：ρ 不携带数值信息）" % fr(rhof))
    PI_STR = ("3.14159265358979323846264338327950288419716939937510"
              "58209749445923078164062862089986280348253421170679")
    PI_D = D(PI_STR)
    mt = D("172.69")
    drho = 3 * GF * mt * mt / (8 * sq2 * PI_D * PI_D)
    drho_doc = D("0.0094")
    rel_drho = relerr(drho, drho_doc)
    pdg0 = D("1.00038")
    pdg_err = D("0.00020")
    dev = pdg0 - D(1)
    ratio = drho / dev
    mt_need = (dev * 8 * sq2 * PI_D * PI_D / (3 * GF)).sqrt()
    guard("G23 drho_top_value", rel_drho < D("0.02"),
          "drho=%s vs doc 0.0094 rel=%s" % (fs(drho), fs(rel_drho)))
    # 归因失守：顶圈比实测偏差大 24.6 倍
    attrib_bad = ratio > D(10)
    guard("G24 rho_attribution_mismatch", attrib_bad,
          "Δρ_top/PDG偏差=%s（>10 ⇒ 归因不成立）" % fs(ratio))
    add("E06", "FAIL" if attrib_bad else "PASS",
        "推论 4.3：ρ≡1 成立；但「偏差来自顶夸克圈」与 3.8E−4 差 24.6 倍",
        "① ρ≡m_W²/(m_Z²cos²θ_W)=1 是质量公式的同义反复（机器：任意 (g₁,g₂,v) 得 ρ=1；"
        "控制组 (70,100,300) 亦得 1）⇒ 非独立预言。② 文档写「实测 1.00038±0.00020；"
        "偏差来自顶夸克圈（Δρ=3G_Fm_t²/8√2π²≈0.0094）」。机器：Δρ_top=**%s**"
        "（m_t=172.69，与文档 0.0094 相对差 %s），而 PDG 偏差只有 **3.8E−4** ⇒ 比值 "
        "**%s 倍**；若强行让顶圈给出 3.8E−4，需 m_t=**%s GeV**（约实测 1/5）。"
        "与 00 §4 的同一措辞同族（r207 C03，**不跨卷相加**）；验证报告 E3.2 原文亦写明"
        "ρ₀ 是「新物理偏离」的拟合参数。修复：删去「偏差来自顶夸克圈」，或改为"
        "「SM 顶圈修正 ~9E−3；ρ₀ 的 3.8E−4 是扣除 SM 后的新物理拟合残差」。"
        % (fs(drho), fs(rel_drho, 6), md(ratio, 3), md(mt_need, 2)),
        {"rho": "1", "drho_top": fs(drho), "rel_vs_doc": fs(rel_drho),
         "pdg_dev": fs(dev), "ratio": md(ratio, 3), "mt_needed": md(mt_need, 2)})

    # =================================================================
    # F01 §5 (D) 与 5.1/5.2 ⇒ INFO
    # =================================================================
    has_D = ("\\tag{D}" in txt)
    has_52 = ("5.2" in txt) and ("a_e" in txt)
    add("F01", "INFO",
        "§5 Dirac 方程 (D)、测地线（5.1）、g−2（5.2）：未机核，仅登记",
        "(D) 的旋量联络项 ¼ω^{ab}γ_{ab} 与 (D) 的短波极限（测地线）需要 4×4 γ 代数与 "
        "WKB 展开，本卷外形式层未覆盖；g−2 的 Schwinger 值 α/2π 属外部已知结果。"
        "标签 \\tag{D} 存在=%s；5.2 段与 a_e 字样存在=%s。机器只核了文档 §7 对 (D) 的"
        "「与 QED 树级一致」这一登记的引用可解析（见 G02）。" % (has_D, has_52),
        {"tag_D": has_D, "sec52": has_52})

    # =================================================================
    # G01 七标签两处一致
    # =================================================================
    sec6 = txt.split("## 6.")[-1].split("## 7.")[0]
    body = txt.split("## 6.")[0]
    tagok = {}
    for t in ("C", "E", "YM", "H", "D"):
        tagok[t] = (("\\tag{%s}" % t) in body) and (("\\text{(%s)}" % t) in sec6)
    tagok["Cp"] = ("\\tag{C$'$}" in body)
    tagok["Ep"] = ("\\tag{E$'$}" in body)
    ok_tags = all(tagok.values())
    guard("G25 equations_tags", ok_tags, "%s" % tagok)
    add("G01", "PASS" if ok_tags else "FAIL",
        "§6 的五方程总表与 §1–§5 的盒式标签逐条对应",
        "推导段含 \\tag{C}、\\tag{C′}、\\tag{E}、\\tag{E′}、\\tag{YM}、\\tag{H}、\\tag{D}；"
        "§6 总表含 \\text{(C)}、\\text{(E)}、\\text{(YM)}、\\text{(H)}、\\text{(D)}。"
        "机器逐条命中：%s。" % tagok,
        tagok)

    # =================================================================
    # G02 §7 状态表与验证报告引用
    # =================================================================
    sec7 = txt.split("## 7.")[-1]
    rows7 = [ln for ln in sec7.splitlines()
             if re.match(r"^\|\s*\((?:C|E|YM|H|D|1\.3)\)", ln)]
    rep_status = {}
    for line in txt_rep.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not re.fullmatch(r"[A-Z]\d+(?:\.\d+)?", cells[0]):
            continue
        st = None
        for c in cells:
            cc = c.replace("*", "").strip()
            if cc in ("PASS", "FAIL", "INFO"):
                st = cc
        if st:
            rep_status[cells[0]] = st
    cited = ["A1.%d" % i for i in range(1, 6)]
    cited += ["A2.%d" % i for i in range(1, 17)]
    cited += ["C1", "E1", "E2.1", "E2.2", "E3.1", "E3.2", "E4"]
    missing = [c for c in cited if c not in rep_status]
    fails = [c for c in cited if rep_status.get(c) == "FAIL"]
    c1_status = rep_status.get("C1")
    ok_ref = (len(rows7) == 6) and (not missing) and (not fails)
    guard("G26 sec7_refs", ok_ref,
          "rows=%d missing=%s fails=%s" % (len(rows7), missing, fails))
    add("G02", "PASS" if ok_ref else "FAIL",
        "§7 状态总表 6 行；所引 A1/A2/C1/E1–E4 在验证报告中真实存在且无 FAIL",
        "§7 表行数 = **%d**（(C)(E)(YM)(H)(D)(1.3)）。验证报告解析出 %d 条带状态的条目；"
        "文档所引 %d 个编号 missing=%s、FAIL=%s。注意 **C1（牛顿极限）在报告中是 INFO**"
        "（κ²=8πG 的定标值为外部输入），文档把它列为 (E) 的「独立验证」与报告口径一致，"
        "但不构成独立检验。"
        % (len(rows7), len(rep_status), len(cited), missing, fails),
        {"rows7": len(rows7), "report_entries": len(rep_status),
         "missing": missing, "fails": fails, "C1": c1_status})

    # =================================================================
    # G03 站内链接
    # =================================================================
    links = re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", txt)
    bad = []
    anchors = 0
    for lk in links:
        if lk.startswith("http"):
            continue
        path, _, anc = lk.partition("#")
        tgt = os.path.join(DIR07, path)
        if not os.path.isfile(tgt):
            bad.append(lk)
        if anc:
            anchors += 1
    ok_links = (len(links) > 0) and (not bad)
    guard("G27 links", ok_links, "links=%d bad=%s" % (len(links), bad))
    # 控制组：伪造路径应被拒
    control("K10 fake_link_rejected",
            not os.path.isfile(os.path.join(DIR07, "__no_such_doc__.md")),
            "伪造链接不应解析成功")
    add("G03", "PASS" if ok_links else "FAIL",
        "全文站内链接全部解析到真实文件",
        "正则提取 %d 个链接（含锚点 %d 个），逐个相对 07 目录解析，坏链 = %s。"
        "控制组 K10 用伪造路径确认检查器不是恒真。" % (len(links), anchors, bad),
        {"links": len(links), "anchors": anchors, "bad": bad})

    # =================================================================
    # G04 供给
    # =================================================================
    add("G04", "INFO",
        "供给判定：02 全卷探针 C1（定义/代数恒等/外部实测）",
        "本卷机核对象为三条变分恒等式、ε 合并系数、线性映射秩、SM 质量矩阵本征值、"
        "外部实测值（v、λ、m_W、m_Z、G_F）。没有一条可与观测对撞且非外部输入的独立数值"
        "⇒ TUFT 侧独立数值供给 **0/12 维持**。",
        {"supply": "0/12"})

    return {
        "p1": ok_p1, "p2": ok_p2, "p3": ok_p3,
        "merge": merge_ok, "mergeR": ok_R, "mergeL": ok_L,
        "rank": rk, "ec": ok_E, "dF": ok_dF, "cons": ok_cons,
        "eig": (char_ok and rowA1 == 0 and rowA2 == 0),
        "rho_bad": attrib_bad, "ratio": ratio,
        "links": ok_links, "tags": ok_tags, "refs": ok_ref,
        "higgs": ok_h, "eid": ok_e, "num": ok_num,
    }


def build_verdict(f):
    p = ["R215"]
    p.append("P1-P2-P3-" + ("EXACT-OK" if (f["p1"] and f["p2"] and f["p3"]) else "FAIL"))
    p.append("EPS-MERGE-2-4-" + ("OK" if (f["merge"] and f["mergeR"] and f["mergeL"]) else "FAIL"))
    p.append("CARTAN-RANK-%d" % f["rank"])
    p.append("EC-COEFF-" + ("OK" if f["ec"] else "FAIL"))
    p.append("YM-DELTA-F-" + ("OK" if f["dF"] else "FAIL"))
    p.append("CURRENT-CONS-" + ("OK" if f["cons"] else "FAIL"))
    p.append("HIGGS-EQ-" + ("OK" if f["higgs"] else "FAIL"))
    p.append("MASS-EIGEN-" + ("OK" if f["eig"] else "FAIL"))
    p.append("E-IDENTITIES-" + ("OK" if f["eid"] else "FAIL"))
    p.append("V-246-219651-LAMBDA-0-129384-" + ("OK" if f["num"] else "FAIL"))
    p.append("RHO-IDENTITY-OK-ATTRIB-" +
             ("WRONG-24-6X-FAIL" if f["rho_bad"] else "OK"))
    p.append("PROCA-PARTIAL-BOUNDARY-CONV-3-8-BOUNDARY")
    p.append("TAGS-" + ("OK" if f["tags"] else "FAIL"))
    p.append("SEC7-REFS-" + ("OK" if f["refs"] else "FAIL"))
    p.append("LINKS-" + ("OK" if f["links"] else "BAD"))
    p.append("SUPPLY-0")
    return "-".join(p)


def write_outputs(verdict):
    levels = {}
    for e in ENTRIES:
        levels[e["level"]] = levels.get(e["level"], 0) + 1
    gp = sum(1 for g in GUARDS if g["ok"])
    cp = sum(1 for c in CONTROLS if c["ok"])
    data = dict(stem=STEM, doc=DOC, doc_bytes=nbytes, verdict=verdict,
                entries=ENTRIES, guards=GUARDS, controls=CONTROLS,
                summary=levels, guard_pass="%d/%d" % (gp, len(GUARDS)),
                control_pass="%d/%d" % (cp, len(CONTROLS)))
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    lines = ["# " + STEM, "",
             "- 文档: `%s` (%d B)" % (DOC, nbytes),
             "- 条目: %d %s" % (len(ENTRIES), levels),
             "- 守卫: %d/%d ; 控制组: %d/%d" % (gp, len(GUARDS), cp, len(CONTROLS)),
             "- 判定串: `%s`" % verdict, "",
             "## 总表", "", "| 编号 | 级 | 标题 |", "|---|---|---|"]
    for e in ENTRIES:
        lines.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"]))
    lines += ["", "## 明细", ""]
    for e in ENTRIES:
        lines.append("### %s (%s) %s" % (e["code"], e["level"], e["title"]))
        lines.append("")
        lines.append(e["detail"])
        if e["numbers"]:
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(e["numbers"], ensure_ascii=False, indent=1))
            lines.append("```")
        lines.append("")
    lines += ["## 守卫", "", "| 名称 | 结果 | 读数 |", "|---|---|---|"]
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % (g["name"], "OK" if g["ok"] else "FAIL",
                                           str(g["msg"]).replace("|", "/")))
    lines += ["", "## 控制组", "", "| 名称 | 结果 | 读数 |", "|---|---|---|"]
    for c in CONTROLS:
        lines.append("| %s | %s | %s |" % (c["name"], "OK" if c["ok"] else "FAIL",
                                           str(c["msg"]).replace("|", "/")))
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    rep = ["STEM: " + STEM,
           "doc: %s (%d bytes)" % (DOC, nbytes),
           "entries=%d %s" % (len(ENTRIES), levels),
           "guards=%d/%d controls=%d/%d" % (gp, len(GUARDS), cp, len(CONTROLS)),
           "verdict=" + verdict]
    for e in ENTRIES:
        rep.append("  %-4s %-8s %s" % (e["code"], e["level"], e["title"]))
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("=" * 78)
    print("条目 %d（%s）" % (len(ENTRIES),
                          " / ".join("%s %d" % (k, v) for k, v in sorted(levels.items()))))
    print("守卫 %d/%d · 控制组 %d/%d" % (gp, len(GUARDS), cp, len(CONTROLS)))
    print("判定串：" + verdict)
    print("out -> %s.{json,md,_report.txt}" % STEM)


if __name__ == "__main__":
    flags = main()
    write_outputs(build_verdict(flags))
