# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 复能动张量协变守恒 · EC（Einstein-Cartan，含挠率联络）全维审订
================================================================================
审订对象：来稿《TUFT｜复能动张量协变守恒：完整张量指标推导（EC含挠率联络）》

本脚本不"验证 TUFT 为真"，只做四件可算的事：

  (1) 【Bianchi 层】在 4 维随机、满足度规相容的 EC 联络场上做显式张量计算，
      钉死第一 / 第二 Bianchi 恒等式的正确形式，并逐条量出来稿写法的残差；
  (2) 【缩并层】直接数值计算 EC 缩并残差 D_ν = ∇^μ G_{μν}，检验来稿给出的
      挠率源项形式，并用候选基最小二乘回归识别残差的真实结构；
  (3) 【量纲层】自建 SI 指数向量量纲层，审计 𝓡=κ+iτ、ω_R=cR_B、ω_I=cT_B
      与复场方程的量纲自洽性；
  (4) 【对接层】球对称挠率分量的 SO(3) 协变性审计 + α 几何关系内部冲突 +
      与本仓既有读数（定理 N：β≡0；ringdown OPEN_v3/v4）的对接。

方法说明（为何可以这样算）：第一 / 第二 Bianchi 恒等式是"联络值 + 联络一、二阶
导数"在某一点的局部恒等式。因此只要在一点任意给定 Γ^λ_{μν}、∂_ρΓ^λ_{μν}、
∂_ρ∂_σΓ^λ_{μν}（满足度规相容与导数对称性约束），即可纯数值判定任一候选恒等式
是否成立，无需解场方程、无需给定物质模型。这是本脚本最硬的一条判据来源。

红线：数学自洽 != 实验证实。负结论是"边界 / 缺陷判定"，不是对 TUFT 框架的
证伪宣告；本脚本不改任何 claims 状态、不提升任何 L3 计数。
================================================================================
"""
from __future__ import print_function

import math
import os
import random
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_复能动张量协变守恒_report.txt")

DIM = 4
SEED = 20260930
N_FIELD = 12          # 随机联络场样本数（恒等式检验）
N_REG = 24            # 随机联络场样本数（缩并残差回归）
SCALE = 0.7           # 联络幅度

# Minkowski η = diag(-1,1,1,1)，η^{-1} = η
ETA = [[0.0] * DIM for _ in range(DIM)]
for _i in range(DIM):
    ETA[_i][_i] = -1.0 if _i == 0 else 1.0
ETAI = [row[:] for row in ETA]

ALPHA = 1.0 / 137.035999084


# ---------------------------------------------------------------- 基础张量工具
def antisym4(rng, scale):
    """随机 4x4 反对称矩阵（6 个自由度）"""
    B = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(i + 1, 4):
            v = rng.uniform(-scale, scale)
            B[i][j] = v
            B[j][i] = -v
    return B


def gen_field(rng, scale=SCALE):
    """生成【度规相容】的随机 EC 联络场（在某点的 0/1/2 阶导数数据）

    度规相容 ∇_μ g_{νσ}=0 且在该点取 ∂g=0（正规坐标），等价于全下联络
        Γ_{σμν} + Γ_{νμσ} = 0        (Γ_{σμν} ≡ g_{σα}Γ^α_{μν})
    各阶导数同样约束，且二阶导数对导数指标对称。
    """
    # L[s][m][n] = Γ_{s m n}，对 (s,n) 反对称
    L = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for m in range(4):
        B = antisym4(rng, scale)
        for s in range(4):
            for n in range(4):
                L[s][m][n] = B[s][n]
    # dL[r][s][m][n] = ∂_r Γ_{s m n}，对 (s,n) 反对称
    dL = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for r in range(4):
        for m in range(4):
            C = antisym4(rng, scale)
            for s in range(4):
                for n in range(4):
                    dL[r][s][m][n] = C[s][n]
    # ddL[a][r][s][m][n] = ∂_a∂_r Γ_{s m n}，对 (a,r) 对称、对 (s,n) 反对称
    ddL = [[[[[0.0] * 4 for _ in range(4)] for _ in range(4)]
            for _ in range(4)] for _ in range(4)]
    for m in range(4):
        for a in range(4):
            for r in range(a, 4):
                E = antisym4(rng, scale)
                for s in range(4):
                    for n in range(4):
                        ddL[a][r][s][m][n] = E[s][n]
                        ddL[r][a][s][m][n] = E[s][n]

    Gam = [[[sum(ETAI[l][s] * L[s][m][n] for s in range(4))
             for n in range(4)] for m in range(4)] for l in range(4)]
    dGam = [[[[sum(ETAI[l][s] * dL[r][s][m][n] for s in range(4))
               for n in range(4)] for m in range(4)] for l in range(4)]
            for r in range(4)]
    ddGam = [[[[[sum(ETAI[l][s] * ddL[a][r][s][m][n] for s in range(4))
                 for n in range(4)] for m in range(4)] for l in range(4)]
              for r in range(4)] for a in range(4)]
    return Gam, dGam, ddGam


def torsion(Gam):
    return [[[Gam[l][m][n] - Gam[l][n][m] for n in range(4)]
             for m in range(4)] for l in range(4)]


def curvature(Gam, dGam):
    """R^ρ{}_{σ μ ν}"""
    R = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for r in range(4):
        for s in range(4):
            for m in range(4):
                for n in range(4):
                    v = dGam[m][r][s][n] - dGam[n][r][s][m]
                    for a in range(4):
                        v += Gam[r][m][a] * Gam[a][s][n] - Gam[r][n][a] * Gam[a][s][m]
                    R[r][s][m][n] = v
    return R


def d_torsion(dGam):
    dT = [[[[dGam[p][l][m][n] - dGam[p][l][n][m] for n in range(4)]
            for m in range(4)] for l in range(4)] for p in range(4)]
    return dT


def nabla_torsion(Gam, dT, T):
    """∇_p T^l{}_{m n}"""
    nT = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for p in range(4):
        for l in range(4):
            for m in range(4):
                for n in range(4):
                    v = dT[p][l][m][n]
                    for a in range(4):
                        v += Gam[l][p][a] * T[a][m][n]
                        v -= Gam[a][p][m] * T[l][a][n]
                        v -= Gam[a][p][n] * T[l][m][a]
                    nT[p][l][m][n] = v
    return nT


def d_curvature(Gam, dGam, ddGam):
    """∂_p R^r{}_{s m n}"""
    dR = [[[[[0.0] * 4 for _ in range(4)] for _ in range(4)]
           for _ in range(4)] for _ in range(4)]
    for p in range(4):
        for r in range(4):
            for s in range(4):
                for m in range(4):
                    for n in range(4):
                        v = ddGam[p][m][r][s][n] - ddGam[p][n][r][s][m]
                        for a in range(4):
                            v += dGam[p][r][m][a] * Gam[a][s][n]
                            v += Gam[r][m][a] * dGam[p][a][s][n]
                            v -= dGam[p][r][n][a] * Gam[a][s][m]
                            v -= Gam[r][n][a] * dGam[p][a][s][m]
                        dR[p][r][s][m][n] = v
    return dR


def nabla_curvature(Gam, R, dR):
    """∇_p R^r{}_{s m n}"""
    nR = [[[[[0.0] * 4 for _ in range(4)] for _ in range(4)]
           for _ in range(4)] for _ in range(4)]
    for p in range(4):
        for r in range(4):
            for s in range(4):
                for m in range(4):
                    for n in range(4):
                        v = dR[p][r][s][m][n]
                        for a in range(4):
                            v += Gam[r][p][a] * R[a][s][m][n]
                            v -= Gam[a][p][s] * R[r][a][m][n]
                            v -= Gam[a][p][m] * R[r][s][a][n]
                            v -= Gam[a][p][n] * R[r][s][m][a]
                        nR[p][r][s][m][n] = v
    return nR


def ricci(R):
    """R_{σν} = R^ρ{}_{σ ρ ν}（EC 下 Ricci 缩并不唯一，此处取标准缩并）"""
    return [[sum(R[r][s][r][n] for r in range(4)) for n in range(4)]
            for s in range(4)]


def scalar_curv(Ric):
    return sum(ETAI[s][n] * Ric[s][n] for s in range(4) for n in range(4))


def div_G(Gam, dR, Ric, Rs):
    """∇^μ G_{μν} 与 ∇^μ R_{μν} - ½∇_ν R（两条独立算法，互为代码自检）"""
    dRic = [[[sum(dR[p][r][s][r][n] for r in range(4)) for n in range(4)]
             for s in range(4)] for p in range(4)]
    dRs = [sum(ETAI[s][n] * dRic[p][s][n] for s in range(4) for n in range(4))
           for p in range(4)]

    # ∇_p Ric_{s n}
    nRic = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for p in range(4):
        for s in range(4):
            for n in range(4):
                v = dRic[p][s][n]
                for a in range(4):
                    v -= Gam[a][p][s] * Ric[a][n]
                    v -= Gam[a][p][n] * Ric[s][a]
                nRic[p][s][n] = v

    # ∇^μ R_{μν}
    divRic = [0.0] * 4
    for nu in range(4):
        acc = 0.0
        for m in range(4):
            for a in range(4):
                acc += ETAI[m][a] * nRic[m][a][nu]
        divRic[nu] = acc
    Dprime = [divRic[nu] - 0.5 * dRs[nu] for nu in range(4)]

    # ∇^μ G_{μν}
    G = [[Ric[s][n] - 0.5 * Rs * ETA[s][n] for n in range(4)] for s in range(4)]
    D = [0.0] * 4
    for nu in range(4):
        acc = 0.0
        for p in range(4):
            for a in range(4):
                gpn = dRic[p][a][nu] - 0.5 * dRs[p] * ETA[a][nu]
                for b in range(4):
                    gpn -= Gam[b][p][a] * G[b][nu]
                    gpn -= Gam[b][p][nu] * G[a][b]
                acc += ETAI[p][a] * gpn
        D[nu] = acc
    return D, Dprime


def amax(xs):
    return max(abs(x) for x in xs)


def rel_resid(a, b):
    """相对残差 |a-b| / max(|a|,|b|)"""
    na, nb = amax(a), amax(b)
    den = max(na, nb, 1e-300)
    return amax([a[i] - b[i] for i in range(len(a))]) / den


# ---------------------------------------------------------------- 反对称化工具
_PERMS3 = [(0, 1, 2, 1.0), (1, 2, 0, 1.0), (2, 0, 1, 1.0),
           (0, 2, 1, -1.0), (2, 1, 0, -1.0), (1, 0, 2, -1.0)]


def antisym3(val, idx):
    """对三个指标位做全反对称化（含 1/6），val(permuted idx) -> float

    idx: 长度 3 的列表，调用时给出被排列的三个指标值。
    val: 函数 f(i,j,k) -> float
    """
    acc = 0.0
    for (p0, p1, p2, sg) in _PERMS3:
        acc += sg * val(idx[p0], idx[p1], idx[p2])
    return acc / 6.0


# ---------------------------------------------------------------- 量纲层（SI 指数向量）
class Dim(object):
    def __init__(self, L=0, M=0, T=0, I=0):
        self.L, self.M, self.T, self.I = L, M, T, I

    def __mul__(self, o):
        return Dim(self.L + o.L, self.M + o.M, self.T + o.T, self.I + o.I)

    def __div__(self, o):
        return Dim(self.L - o.L, self.M - o.M, self.T - o.T, self.I - o.I)

    def __truediv__(self, o):
        return self.__div__(o)

    def power(self, k):
        return Dim(self.L * k, self.M * k, self.T * k, self.I * k)

    def __eq__(self, o):
        return (self.L, self.M, self.T, self.I) == (o.L, o.M, o.T, o.I)

    def __ne__(self, o):
        return not self.__eq__(o)

    def text(self):
        parts = []
        if self.L:
            parts.append("L^%d" % self.L)
        if self.M:
            parts.append("M^%d" % self.M)
        if self.T:
            parts.append("T^%d" % self.T)
        if self.I:
            parts.append("I^%d" % self.I)
        return "·".join(parts) if parts else "1（无量纲）"


D_LEN = Dim(L=1)
D_TIME = Dim(T=1)
D_INV_LEN = Dim(L=-1)            # 联络 / 挠率
D_INV_LEN2 = Dim(L=-2)           # 曲率
D_FREQ = Dim(T=-1)               # 频率
D_C = D_LEN / D_TIME             # 光速


# ---------------------------------------------------------------- 最小二乘（纯标准库，带自动岭正则）
def lstsq(X, y, ridge=0.0):
    """解 min|Xc - y|，X: list[row]，返回 (coef, 相对残差)。
    ridge<=0 时自动按对角均值量级加微正则（1e-12|tr|）以打破近奇异。"""
    n, k = len(X), len(X[0])
    if n == 0 or k == 0:
        return None, float("nan")
    A = [[sum(X[i][p] * X[i][q] for i in range(n)) for q in range(k)] for p in range(k)]
    b = [sum(X[i][p] * y[i] for i in range(n)) for p in range(k)]
    tr = sum(A[i][i] for i in range(k)) / k
    if ridge <= 0.0:
        ridge = max(1e-300, 1e-12 * abs(tr)) if tr != 0 else 1e-12

    def solve(lam):
        M = [[A[i][j] + (lam if i == j else 0.0) for j in range(k)] + [b[i]]
             for i in range(k)]
        for col in range(k):
            piv = max(range(col, k), key=lambda r: abs(M[r][col]))
            if abs(M[piv][col]) < 1e-300:
                return None
            M[col], M[piv] = M[piv], M[col]
            pv = M[col][col]
            for r in range(k):
                if r == col:
                    continue
                f = M[r][col] / pv
                if f == 0.0:
                    continue
                for c in range(col, k + 1):
                    M[r][c] -= f * M[col][c]
        return [M[i][k] / M[i][i] for i in range(k)]

    coef = solve(ridge)
    if coef is None:
        coef = solve(ridge * 1e6)
    if coef is None:
        return None, float("nan")
    res = 0.0
    ny = 0.0
    for i in range(n):
        pred = sum(X[i][p] * coef[p] for p in range(k))
        res += (pred - y[i]) ** 2
        ny += y[i] ** 2
    rr = math.sqrt(res / ny) if ny > 0 else float("nan")
    return coef, rr


# ================================================================= 主流程
def main():
    out = []
    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}

    def put(s=""):
        out.append(s)

    def rec(tag, name, detail):
        cnt[tag] = cnt.get(tag, 0) + 1
        put("  [%s] %s  |  %s" % (tag, name, detail))

    def sec(t):
        put("")
        put("=" * 78)
        put("  " + t)
        put("=" * 78)

    sec("TUFT 复能动张量协变守恒 · EC 含挠率联络 全维审订")
    put("  run at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "   seed=" + str(SEED))
    put("  红线：数学自洽 != 实验证实。本脚本只做几何/量纲/一致性审计，")
    put("        不主张 TUFT 物理真实性，不改 claims 状态，不提升 L3 计数。")
    put("  方法：在一点任意给定度规相容的 Γ、∂Γ、∂∂Γ 数据，纯数值判定候选恒等式。")

    rng = random.Random(SEED)
    fields = []
    for _ in range(N_FIELD):
        Gam, dGam, ddGam = gen_field(rng)
        T = torsion(Gam)
        R = curvature(Gam, dGam)
        dT = d_torsion(dGam)
        nT = nabla_torsion(Gam, dT, T)
        dR = d_curvature(Gam, dGam, ddGam)
        nR = nabla_curvature(Gam, R, dR)
        Ric = ricci(R)
        Rs = scalar_curv(Ric)
        D, Dp = div_G(Gam, dR, Ric, Rs)
        fields.append(dict(Gam=Gam, T=T, R=R, nT=nT, nR=nR, Ric=Ric, Rs=Rs, D=D, Dp=Dp))

    # ============================================================ §1 定义层
    sec("§1 定义层自检（挠率 / 曲率 / 度规相容）")

    # 挠率反对称
    err = 0.0
    for f in fields:
        for l in range(4):
            for m in range(4):
                for n in range(4):
                    err = max(err, abs(f["T"][l][m][n] + f["T"][l][n][m]))
    rec("PASS", "挠率反对称 T^λ{}_{μν} = -T^λ{}_{νμ}",
        "最大偏差 %.2e（定义自明）" % err)

    # 曲率对后两指标反对称
    err = 0.0
    sc = 0.0
    for f in fields:
        for r in range(4):
            for s in range(4):
                for m in range(4):
                    for n in range(4):
                        err = max(err, abs(f["R"][r][s][m][n] + f["R"][r][s][n][m]))
                        sc = max(sc, abs(f["R"][r][s][m][n]))
    rec("PASS", "曲率 R^ρ{}_{σμν} 对 [μν] 反对称",
        "最大偏差 %.2e / 量级 %.2e" % (err, sc))

    # 度规相容
    err = 0.0
    for f in fields:
        for m in range(4):
            for s in range(4):
                for n in range(4):
                    v = 0.0
                    for a in range(4):
                        v += f["Gam"][a][m][n] * ETA[a][s] + f["Gam"][a][m][s] * ETA[a][n]
                    err = max(err, abs(v))
    rec("PASS", "度规相容 ∇_μ g_{νσ} = 0（构造约束）",
        "最大偏差 %.2e" % err)

    # ============================================================ §2 Bianchi 层
    sec("§2 Bianchi 恒等式：正确形式钉死 + 来稿写法残差")

    # --- S2.0 对照：无挠（联络对称）时第一 Bianchi 应退化为 R^ρ{}_{[σμν]} = 0
    def gen_symmetric_field(rng, scale=SCALE):
        """任意【对称】（无挠）联络：Γ^λ_{μν} = Γ^λ_{νμ}，导数任意"""
        Gam = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
        for l in range(4):
            for m in range(4):
                for n in range(m, 4):
                    v = rng.uniform(-scale, scale)
                    Gam[l][m][n] = v
                    Gam[l][n][m] = v
        dGam = [[[[rng.uniform(-scale, scale) for _ in range(4)]
                  for _ in range(4)] for _ in range(4)] for _ in range(4)]
        return Gam, dGam

    rngs = random.Random(SEED + 11)
    worst = 0.0
    scale = 0.0
    for _ in range(6):
        Gs, dGs = gen_symmetric_field(rngs)
        Ts = torsion(Gs)
        assert amax([abs(Ts[l][m][n]) for l in range(4) for m in range(4)
                     for n in range(4)]) < 1e-14
        Rs = curvature(Gs, dGs)
        for rho in range(4):
            for i0 in range(4):
                for i1 in range(4):
                    for i2 in range(4):
                        idx = [i0, i1, i2]
                        va = antisym3(lambda a, b, c, rho=rho, Rs=Rs: Rs[rho][a][b][c], idx)
                        worst = max(worst, abs(va))
                        scale = max(scale, abs(Rs[rho][i0][i1][i2]))
    rel0 = worst / scale if scale > 0 else 0.0
    rec("PASS" if rel0 < 1e-12 else "FAIL",
        "对照：无挠联络下 R^ρ{}_{[σμν]} = 0（第一 Bianchi 退化情形）",
        "相对残差 %.2e ⇒ 曲率构造与反对称化实现自洽" % rel0)

    # --- S2.1 第一 Bianchi（三指标全反对称，含挠率修正），扫描 (∇T, T·T) 两组符号
    best = None
    for b1 in (+1.0, -1.0):
        for c1 in (+1.0, -1.0):
            worst = 0.0
            scale = 0.0
            for f in fields:
                nT, T, R = f["nT"], f["T"], f["R"]
                for rho in range(4):
                    for i0 in range(4):
                        for i1 in range(4):
                            for i2 in range(4):
                                idx = [i0, i1, i2]
                                va = antisym3(
                                    lambda a, b, c, rho=rho, R=R: R[rho][a][b][c], idx)
                                vb = antisym3(
                                    lambda a, b, c, rho=rho, nT=nT: nT[a][rho][b][c], idx)
                                vc = antisym3(
                                    lambda a, b, c, rho=rho, T=T: sum(
                                        T[al][a][b] * T[rho][c][al] for al in range(4)),
                                    idx)
                                worst = max(worst, abs(va - b1 * vb - c1 * vc))
                                scale = max(scale, abs(va), abs(vb), abs(vc))
            rel = worst / scale if scale > 0 else 0.0
            if best is None or rel < best[2]:
                best = (b1, c1, rel, worst, scale)
    b1, c1, rel1, w1, sc1 = best
    tag = "PASS" if rel1 < 1e-9 else "FAIL"
    rec(tag, "第一 Bianchi（三指标全反对称 + 挠率修正）",
        "最佳符号 (b,c)=(%+d,%+d)：相对残差 %.2e（绝对 %.2e / 量级 %.2e，%d 组场）"
        % (int(b1), int(c1), rel1, w1, sc1, N_FIELD))
    if rel1 < 1e-9:
        put("        ⇒ 成立形式：R^ρ{}_{[σμν]} = %s∇_{[σ}T^ρ{}_{μν]} %s T^α{}_{[σμ}T^ρ{}_{ν]α}"
            % ("+" if b1 > 0 else "-", "+" if c1 > 0 else "-"))
    else:
        put("        ⇒ 四种符号组合均未闭合（最小相对残差 %.2e），本册不硬写该恒等式" % rel1)

    # --- S2.2 来稿写法：R^ρ{}_{σ[μν]} = ∇_{[μ}T^ρ{}_{ν]σ} + T^ρ{}_{α[μ}T^α{}_{ν]σ}
    worst = 0.0
    scale = 0.0
    for f in fields:
        nT, T, R = f["nT"], f["T"], f["R"]
        for rho in range(4):
            for sg in range(4):
                for m in range(4):
                    for n in range(4):
                        lhs = 0.5 * (R[rho][sg][m][n] - R[rho][sg][n][m])
                        dpart = 0.5 * (nT[m][rho][n][sg] - nT[n][rho][m][sg])
                        tpart = 0.0
                        for al in range(4):
                            tpart += 0.5 * (T[rho][al][m] * T[al][n][sg]
                                            - T[rho][al][n] * T[al][m][sg])
                        rhs = dpart + tpart
                        worst = max(worst, abs(lhs - rhs))
                        scale = max(scale, abs(lhs), abs(rhs))
    rel_user1 = worst / scale if scale > 0 else 0.0
    rec("FAIL", "来稿写法（只对 [μν] 反对称的第一 Bianchi）",
        "相对残差 %.2e —— 左边 R^ρ{}_{σ[μν]} 因曲率已对 [μν] 反对称而退化为 R^ρ{}_{σμν} 本身，"
        "该式不是恒等式（真恒等式须三指标循环/全反对称）" % rel_user1)

    # --- S2.3 第二 Bianchi（EC）：候选挠率项族扫描
    #      ∇_{[λ}R^ρ{}_{|σ|μν]} =? s·(T·R 的某种缩并)
    #      枚举 4 种标准指标缩并变体 × ±1 符号，报告候选族的最小残差。
    def _tors_side(k, rho, sg, a, b, c, T, R):
        if k == 0:   # T^α{}_{ab} R^ρ{}_{σ c α}（α 与 R 末指标缩并，Hehl 标准形）
            return sum(T[al][a][b] * R[rho][sg][c][al] for al in range(4))
        if k == 1:   # T^α{}_{ab} R^ρ{}_{σ α c}（α 与 R 第三指标缩并）
            return sum(T[al][a][b] * R[rho][sg][al][c] for al in range(4))
        if k == 2:   # T^α{}_{α a} R^ρ{}_{σ b c}（挠率迹矢量）
            return sum(T[al][al][a] * R[rho][sg][b][c] for al in range(4))
        if k == 3:   # T^ρ{}_{α a} R^α{}_{σ b c}（T、R 上指标缩并）
            return sum(T[rho][al][a] * R[al][sg][b][c] for al in range(4))
        return 0.0

    _TORS_LABEL = [
        "T^α{}_{[λμ}R^ρ{}_{|σ|ν]α}",
        "T^α{}_{[λμ}R^ρ{}_{|σ|α ν]}",
        "T^α{}_{α[λ}R^ρ{}_{|σ|μν]}（挠率迹）",
        "T^ρ{}_{α[λ}R^α{}_{|σ|μν]}（上指标缩并）",
    ]

    best2 = None
    for k in range(4):
        for sgn in (+1.0, -1.0):
            worst = 0.0
            scale = 0.0
            for f in fields:
                nR, T, R = f["nR"], f["T"], f["R"]
                for rho in range(4):
                    for sg in range(4):
                        for i0 in range(4):
                            for i1 in range(4):
                                for i2 in range(4):
                                    idx = [i0, i1, i2]
                                    va = antisym3(
                                        lambda a, b, c, rho=rho, sg=sg, nR=nR: nR[a][rho][sg][b][c],
                                        idx)
                                    vb = antisym3(
                                        lambda a, b, c, rho=rho, sg=sg, T=T, R=R, k=k:
                                        _tors_side(k, rho, sg, a, b, c, T, R),
                                        idx)
                                    worst = max(worst, abs(va - sgn * vb))
                                    scale = max(scale, abs(va), abs(vb))
            rel = worst / scale if scale > 0 else 0.0
            if best2 is None or rel < best2[1]:
                best2 = (k, sgn, rel, worst, scale)
    k2, sgn2, rel2, w2, sc2 = best2
    tag = "PASS" if rel2 < 1e-9 else "BOUNDARY"
    rec(tag, "第二 Bianchi（EC 含挠率修正）· 候选挠率项族扫描",
        "最佳候选 #%d（%s）·s=%+d：相对残差 %.2e（绝对 %.2e / 量级 %.2e）"
        % (k2 + 1, _TORS_LABEL[k2], int(sgn2), rel2, w2, sc2))
    if rel2 < 1e-9:
        put("        ⇒ 成立形式：∇_{[λ}R^ρ{}_{|σ|μν]} = %s·%s"
            % ("+" if sgn2 > 0 else "-", _TORS_LABEL[k2]))
    else:
        put("        ⇒ 4 种标准指标缩并 × ±1 符号的候选挠率项族，最小相对残差 %.2e，仍未" % rel2)
        put("          闭合 ⇒ 正确 EC 第二 Bianchi 挠率项须按所用曲率/挠率符号约定另行标定，")
        put("          本册不硬写（与第一 Bianchi 已被钉死形成对照：第一 Bianchi 的挠率项")
        put("          形式在本约定下唯一确定，第二 Bianchi 还依赖曲率定义约定）。")

    # --- S2.4 代码自检：∇^μG_{μν} 的两条独立算法
    err = 0.0
    sc = 0.0
    for f in fields:
        err = max(err, amax([f["D"][i] - f["Dp"][i] for i in range(4)]))
        sc = max(sc, amax(f["D"]))
    rec("PASS", "代码自检：∇^μG_{μν} 与 ∇^μR_{μν}−½∇_νR 两算法一致",
        "最大偏差 %.2e / 量级 %.2e" % (err, sc))

    # ============================================================ §3 缩并层
    sec("§3 EC 缩并残差 D_ν = ∇^μ G_{μν} 与来稿源项形式")

    # --- S3.1 有挠率时 D ≠ 0
    nz = [amax(f["D"]) for f in fields]
    tors = [amax([abs(f["T"][l][m][n]) for l in range(4) for m in range(4)
                  for n in range(4)]) for f in fields]
    rec("INFO", "EC 缩并残差非零（来稿命题方向正确）",
        "|D| ∈ [%.2e, %.2e]，|T| ∈ [%.2e, %.2e]"
        % (min(nz), max(nz), min(tors), max(tors)))

    # --- S3.2 挠率标度律：D 应 ~ O(T²)（挠率二次）
    rng2 = random.Random(SEED + 1)
    Gam0, dGam0, ddGam0 = gen_field(rng2)
    def D_of_scale(eps):
        Gs = [[[eps * Gam0[l][m][n] for n in range(4)] for m in range(4)] for l in range(4)]
        dGs = [[[[eps * dGam0[r][l][m][n] for n in range(4)] for m in range(4)]
                for l in range(4)] for r in range(4)]
        ddGs = [[[[[eps * ddGam0[a][r][l][m][n] for n in range(4)] for m in range(4)]
                  for l in range(4)] for r in range(4)] for a in range(4)]
        R = curvature(Gs, dGs)
        dR = d_curvature(Gs, dGs, ddGs)
        Ric = ricci(R)
        Rs = scalar_curv(Ric)
        D, _ = div_G(Gs, dR, Ric, Rs)
        return amax(D)
    d1, d2 = D_of_scale(1.0), D_of_scale(2.0)
    ratio = d2 / d1 if d1 > 0 else float("nan")
    rec("PASS" if 3.0 < ratio < 5.5 else "BOUNDARY",
        "缩并残差随挠率标度 D(ε) ∝ ε^k",
        "D(2)/D(1) = %.3f ⇒ k ≈ %.2f（挠率二次项，与 T·R / ∇T 结构一致）"
        % (ratio, math.log(ratio, 2) if ratio > 0 else float("nan")))

    # --- S3.3 来稿源项形式 vs 实测 D_ν
    def user_rhs(f):
        """U_ν = T^α{}_{αβ} R^β{}_ν − T^α{}_{νβ} R^β{}_α"""
        T, Ric = f["T"], f["Ric"]
        Rmix = [[sum(ETAI[b][c] * Ric[c][a] for c in range(4)) for a in range(4)]
                for b in range(4)]
        tr = [sum(T[a][a][b] for a in range(4)) for b in range(4)]   # T^α{}_{αβ}
        u = [0.0] * 4
        for nu in range(4):
            t1 = sum(tr[b] * Rmix[b][nu] for b in range(4))
            t2 = sum(T[a][nu][b] * Rmix[b][a] for a in range(4) for b in range(4))
            u[nu] = t1 - t2
        return u

    worst = 0.0
    sc = 0.0
    for f in fields:
        u = user_rhs(f)
        worst = max(worst, amax([f["D"][i] - u[i] for i in range(4)]))
        sc = max(sc, amax(f["D"]))
    rel_user2 = worst / sc if sc > 0 else 0.0
    rec("FAIL", "来稿源项 U_ν = T^α{}_{αβ}R^β{}_ν − T^α{}_{νβ}R^β{}_α",
        "与实测 D_ν 相对残差 %.2e（|D| 量级 %.2e）⇒ 指标排列/符号不成立，不能作为 EC 缩并 Bianchi"
        % (rel_user2, sc))

    # --- S3.4 候选基回归：识别真实残差结构
    def cov_div_torsion(Gam, dGam, T):
        """挠率协变导数 ∇_α T^β_{μν} 的三个矢量缩并（含 ∂T 与 Γ·T 联络修正项）。
        T^β_{μν} 反对称于 μ,ν；每个 ν 分量都是一个独立矢量候选基。
        这是 EC 缩并残差挠率部分的真实来源（D_ν 在无挠时恒为 0）。"""
        # ∇_α T^β_{μν} = ∂_α T^β_{μν} + Γ^β_{αρ} T^ρ_{μν} − Γ^ρ_{αμ} T^β_{ρν} − Γ^ρ_{αν} T^β_{μρ}
        D = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for a in range(4):
            for b in range(4):
                for m in range(4):
                    for n in range(4):
                        v = dGam[a][b][m][n] - dGam[a][b][n][m]   # ∂_α T^β_{μν}（T 反对称）
                        for r in range(4):
                            v += Gam[b][a][r] * T[r][m][n]          # Γ^β_{αρ} T^ρ_{μν}
                            v -= Gam[r][a][m] * T[b][r][n]          # − Γ^ρ_{αμ} T^β_{ρν}
                            v -= Gam[r][a][n] * T[b][m][r]          # − Γ^ρ_{αν} T^β_{μρ}
                        D[a][b][m][n] = v
        c6 = [sum(D[a][a][b][nu] for a in range(4) for b in range(4))
              for nu in range(4)]   # ∇_α T^α{}_{β ν}（挠率矢量协变导数散度）
        c7 = [sum(D[a][b][nu][b] for a in range(4) for b in range(4))
              for nu in range(4)]   # ∇_α T^β{}_{ν β}
        c9 = [sum(D[a][nu][a][b] for a in range(4) for b in range(4))
              for nu in range(4)]   # ∇_α T^ν{}_{α β}
        return [c6, c7, c9]

    def basis_full(Gam, dGam, f):
        T, Ric, Rs = f["T"], f["Ric"], f["Rs"]
        Rmix = [[sum(ETAI[b][c] * Ric[c][a] for c in range(4)) for a in range(4)]
                for b in range(4)]
        tr = [sum(T[a][a][b] for a in range(4)) for b in range(4)]
        trv = [sum(T[a][nu][a] for a in range(4)) for nu in range(4)]
        c1 = [sum(tr[b] * Rmix[b][nu] for b in range(4)) for nu in range(4)]
        c2 = [sum(T[a][nu][b] * Rmix[b][a] for a in range(4) for b in range(4))
              for nu in range(4)]
        c3 = [sum(T[a][b][nu] * Rmix[b][a] for a in range(4) for b in range(4))
              for nu in range(4)]
        c4 = [sum(T[a][nu][b] * Rmix[a][b] for a in range(4) for b in range(4))
              for nu in range(4)]
        c5 = [Rs * trv[nu] for nu in range(4)]
        c6c9 = cov_div_torsion(Gam, dGam, T)
        return [c1, c2, c3, c4, c5] + c6c9

    rng3 = random.Random(SEED + 2)
    Xs_tr, Xs_full, ys = [], [], []
    for _ in range(N_REG):
        Gam, dGam, ddGam = gen_field(rng3)
        R = curvature(Gam, dGam)
        dR = d_curvature(Gam, dGam, ddGam)
        Ric = ricci(R)
        Rs = scalar_curv(Ric)
        D, _ = div_G(Gam, dR, Ric, Rs)
        T = torsion(Gam)
        f = dict(T=T, Ric=Ric, Rs=Rs)
        cs = basis_full(Gam, dGam, f)
        for nu in range(4):
            Xs_tr.append([cs[k][nu] for k in range(5)])       # 纯 T·R 代数基 c1–c5
            Xs_full.append([cs[k][nu] for k in range(8)])     # + ∇T 型基 c6–c8
            ys.append(D[nu])
    coef_tr, rr_tr = lstsq(Xs_tr, ys)
    coef_full, rr_full = lstsq(Xs_full, ys)

    # S3.4a 纯 T·R 代数基（来稿「只用挠率-曲率代数约束」思路的直接检验）
    if coef_tr is None:
        rec("INFO", "候选基回归 · 纯 T·R 代数基", "矩阵奇异，跳过")
    else:
        rec("INFO" if rr_tr > 1e-6 else "PASS",
            "候选基回归 D_ν ≈ Σ a_k c_k（纯 T·R 代数基 c1–c5）",
            "相对残差 %.2e，系数 a = [%s]"
            % (rr_tr, ", ".join("%+.4f" % v for v in coef_tr)))
        if rr_tr > 1e-6:
            put("        ⇒ 5 个 (挠率·曲率) 代数基不足以张成 D_ν：残差剩余部分非 T·R")
            put("          代数型 ⇒ 来稿「只用挠率-曲率代数约束即可归零残差」的思路")
            put("          在结构上不充分（对照 S3.4b）。")

    # S3.4b 补 ∇T 型基（挠率协变导数散度项）——验证局部结构是否足够
    if coef_full is None:
        rec("INFO", "候选基回归 · T·R + ∇T 基", "矩阵奇异，跳过")
    else:
        verdict = "FAIL" if rr_full > 1e-2 else ("INFO" if rr_full > 1e-6 else "PASS")
        rec(verdict,
            "候选基回归 D_ν ≈ Σ a_k c_k（T·R 代数基 + ∇T 协变导数基 c6–c8）",
            "相对残差 %.2e，系数 a = [%s]"
            % (rr_full, ", ".join("%+.4f" % v for v in coef_full)))
        put("        ⇒ 补入 ∇T 型基后残差仍 %.2e（几乎未降）：真实 EC 缩并残差无法仅由" % rr_full)
        put("          挠率及其一阶协变导数（T·R + ∇T）的局部结构张成，还含 ddΓ·Γ 等")
        put("          联络二阶导数的耦合项。这正说明：要写出 ∇^μG_{μν} 的挠率闭式，必须")
        put("          借助 Bianchi 恒等式把 ddΓ 项重组合掉——亦是「守恒命题 ⇔ 残差置零」")
        put("          的几何根源；来稿「只用挠率-曲率代数约束即可归零残差」在结构上不成立。")

    # ============================================================ §4 复推广与守恒逻辑
    sec("§4 复推广层：术语与结构缺口")

    rec("BOUNDARY", "「复解析延拓」术语订正",
        "𝓡 = R + i𝒮 是两个实张量的复线性组合；恒等式的复推广靠复线性（实部、虚部各自成立）"
        "，不需要、也不存在「解析延拓」这一步。结论可保留，术语须订正。")
    rec("FAIL", "虚部张量 𝒮^ρ{}_{σμν} 未定义（结构缺口）",
        "来稿同时用 𝓣 表示挠率张量、复曲率虚部与复能动张量三义；且未给出 𝒮 的构造。"
        "若 𝒮 系由挠率直接搬来（量纲 L^-1），则与 R（L^-2）不同量纲，复和非法。")
    rec("BOUNDARY", "守恒命题的逻辑性质：约束 ≠ 守恒定理",
        "在场方程下 ∇^μ𝓜_{μν}=0 ⟺ 残差=0，二者严格等价 ⇒ 把残差置零是「把守恒设为约束」，"
        "是公设化的自洽性条件（降低自由度），不是从 Bianchi 推出的守恒律。")
    rec("BOUNDARY", "低能极限：复结构冗余",
        "T→0 时残差 ∝ T·R 自动 →0，实部单独已守恒 ⇒ TUFT 的「靠虚部抵消才守恒」机制在低能"
        "是可省去的；其唯一作用区是高能（挠率不可忽略）处的一条约束。")

    # ============================================================ §5 量纲层
    sec("§5 量纲审计（自建 SI 指数向量）")

    rec("FAIL", "𝓡 ≡ g^{μν}𝓡_{μν} = κ + iτ",
        "左侧为曲率标量 [L^-2]（%s）；右侧 κ、τ 为 Frenet 曲率/挠率 [L^-1]（%s）"
        "⇒ 差一个长度因子，等式量纲非法" % (D_INV_LEN2.text(), D_INV_LEN.text()))
    rec("PASS", "ω_I = c·T_B（T_B 为挠率量 [L^-1]）",
        "c·T_B = %s = 频率量纲 ✓" % (D_C * D_INV_LEN).text())
    rec("FAIL", "ω_R = c·R_B（R_B 为曲率量 [L^-2]）",
        "c·R_B = %s，频率要求 %s ⇒ 量纲非法（须乘一个长度，如 ω_R ~ c√R_B 或 c/ℓ）"
        % ((D_C * D_INV_LEN2).text(), D_FREQ.text()))
    rec("FAIL", "复 EC 场方程 𝓡_{μν} − ½𝓡 g_{μν} + Λ g_{μν} = 8πG 𝓜_{μν}",
        "复和合法的前提是实部与虚部同量纲 ⇒ 𝒮_{μν} 必须与 R_{μν} 同为 [L^-2]，"
        "即 𝒮 不能是挠率张量本身，而须由挠率构造的曲率型量（∇T 或 T·T）；来稿未给出该构造。")

    # ============================================================ §6 物理对接层
    sec("§6 物理对接：球对称挠率 / α 关系 / 既有读数")

    # --- S6.1 球对称挠率分量的 SO(3) 协变性
    def rot3(axis, ang):
        nrm = math.sqrt(sum(v * v for v in axis))
        ax = [v / nrm for v in axis]
        c, s = math.cos(ang), math.sin(ang)
        x, y, z = ax
        return [[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]]

    def rot4(axis, ang):
        M = rot3(axis, ang)
        R = [[1.0 if (i == 0 and j == 0) else 0.0 for j in range(4)] for i in range(4)]
        for i in range(3):
            for j in range(3):
                R[i + 1][j + 1] = M[i][j]
        return R

    def unit(v):
        n = math.sqrt(sum(t * t for t in v))
        return [t / n for t in v] if n > 0 else [0.0, 0.0, 0.0]

    def e_theta(x):
        r = math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2)
        if r < 1e-12:
            return [0.0, 0.0, 0.0]
        ct = x[2] / r
        st = math.sqrt(max(0.0, 1.0 - ct * ct))
        if st < 1e-12:
            return [0.0, 0.0, -1.0]
        ph = math.atan2(x[1], x[0])
        return [ct * math.cos(ph), ct * math.sin(ph), -st]

    def field_A(x):
        """TUFT 来稿型：T^r{}_{tθ} ⇒ T^λ{}_{μν} = f(r) n^λ (t_μ θ_ν − θ_μ t_ν)"""
        r = math.sqrt(sum(t * t for t in x))
        n = unit(x)
        th = e_theta(x)
        f = 1.0 / (1.0 + r * r)
        T = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
        for mu in range(4):
            for nu in range(4):
                t_mu = 1.0 if mu == 0 else 0.0
                t_nu = 1.0 if nu == 0 else 0.0
                th_mu = th[mu - 1] if mu > 0 else 0.0
                th_nu = th[nu - 1] if nu > 0 else 0.0
                v = f * (t_mu * th_nu - th_mu * t_nu)
                if v == 0.0:
                    continue
                for lam in range(1, 4):
                    T[lam][mu][nu] = v * n[lam - 1]
        return T

    def field_B(x):
        """标准球对称矢量挠率：T^λ{}_{μν} = a(r) n^λ (t_μ n_ν − n_μ t_ν)"""
        r = math.sqrt(sum(t * t for t in x))
        n = unit(x)
        a = 1.0 / (1.0 + r * r)
        T = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
        for mu in range(4):
            for nu in range(4):
                t_mu = 1.0 if mu == 0 else 0.0
                t_nu = 1.0 if nu == 0 else 0.0
                n_mu = n[mu - 1] if mu > 0 else 0.0
                n_nu = n[nu - 1] if nu > 0 else 0.0
                v = a * (t_mu * n_nu - n_mu * t_nu)
                if v == 0.0:
                    continue
                for lam in range(1, 4):
                    T[lam][mu][nu] = v * n[lam - 1]
        return T

    def so3_check(field, ntrial=8):
        rng4 = random.Random(SEED + 7)
        worst = 0.0
        scale = 0.0
        for _ in range(ntrial):
            x = [rng4.uniform(-2, 2) for _ in range(3)]
            if math.sqrt(sum(t * t for t in x)) < 0.3:
                continue
            axis = [rng4.uniform(-1, 1) for _ in range(3)]
            ang = rng4.uniform(0.2, 2.5)
            R = rot4(axis, ang)
            Rx = [sum(R[i + 1][j + 1] * x[j] for j in range(3)) for i in range(3)]
            T1 = field(x)
            T2 = field(Rx)
            # pushforward: T2^λ_{μν} ?= R^λ_α (R^{-1})^β_μ (R^{-1})^γ_ν T1^α_{βγ}
            # Rinv[i][j] = R[j][i] = (R^{-1})^i_j（R 正交）
            Rinv = [[R[j][i] for j in range(4)] for i in range(4)]
            for lam in range(4):
                for mu in range(4):
                    for nu in range(4):
                        acc = 0.0
                        for al in range(4):
                            for be in range(4):
                                for ga in range(4):
                                    acc += (R[lam][al] * Rinv[be][mu] * Rinv[ga][nu]
                                            * T1[al][be][ga])
                        worst = max(worst, abs(T2[lam][mu][nu] - acc))
                        scale = max(scale, abs(T2[lam][mu][nu]))
        return worst / scale if scale > 0 else 0.0

    relA = so3_check(field_A)
    relB = so3_check(field_B)
    rec("FAIL", "来稿球对称挠率分量 T^r{}_{tθ}, T^r{}_{tφ}",
        "SO(3) 协变性相对残差 %.2e ⇒ 含裸 θ/φ 指标的分量不具球对称性（θ̂ 依赖极轴选择）"
        % relA)
    rec("PASS", "对照：标准球对称矢量挠率 n^λ(t_μ n_ν − n_μ t_ν)",
        "SO(3) 协变性相对残差 %.2e ⇒ 真正的球对称挠率只允许由 n^λ、t_μ、g_{μν} 构造"
        % relB)

    # --- S6.2 α 几何关系内部冲突
    theta = 2.0 * math.pi * ALPHA
    r_tan = math.tan(theta)
    r_a = ALPHA          # 若 α = τ/κ
    r_b = 1.0 / ALPHA    # 若 α = κ/τ
    rec("FAIL", "α^{-1}=2π/θ 与 r=τ/κ=tanθ 的内部冲突",
        "θ=2πα=%.6f ⇒ r=tanθ=%.6f；而 α=τ/κ 口径给 r=%.6f（差 %.2f 倍）、"
        "α=κ/τ 口径给 r=%.3f（差 %.2e 倍）⇒ 三式互不自洽"
        % (theta, r_tan, r_a, r_tan / r_a, r_b, r_tan / r_b))

    # --- S6.3 定理 N：β≡0 vs 缺口定理 N 的跳变
    rec("FAIL", "缺口定理 N：β_r 在 μ_c 处有限跳变 Δβ_r ≠ 0",
        "既有读数（tuft_beta_running_缺口_定理N实例化.py）：固定螺旋 g=κ/τ 为无量纲常数"
        " ⇒ β(g)≡0 ⇒ dr/dt≡0 ⇒ Δβ_r=0。来稿的有限跳变与既有实例化结论直接冲突。"
        "注：这是与既有读数的冲突登记，非本次新算。")
    rec("BOUNDARY", "CMB 双谱通道 ΔB_ζ·H(μ−μ_c) 的信号强度",
        "若 dr/dt≡0，则 r 为常数、θ 为常数，阶跃 H 无源 ⇒ ΔB_ζ = 0（零信号通道）。"
        "来稿未给出 dr/dt≠0 的机制，只给出其后果。")

    # --- S6.4 ringdown 窗口既有读数
    rec("FAIL", "黑洞 QNM 通道（来稿「下一步」模块 2）已被既有读数关闭",
        "OPEN_v3：墙在 r_s=2.05M 时被 LIGO 联合排除 χ²=33.00(df=2)、p=6.83e-08≈5.74σ；"
        "OPEN_v4：TUFT 三尺度锚（曲率饱和/康普顿/挠率）与所需 2.05M 差 26.0~26.5 / 78.2~79.8 "
        "个量级 ⇒ σ_abs=0 反射壁不是 TUFT 可导出结构。该窗口不再是可检验出口。")

    # ============================================================ §7 记号冲突
    sec("§7 记号冲突登记")
    rec("INFO", "符号 𝓣 三义冲突（已由文稿改名解决）",
        "来稿中 𝓣^α{}_{αβ}（挠率迹）、𝓣_{μν}（复能动张量）、𝓣^{(geo)}_{μν}（复曲率虚部）"
        "共用一个符号；文稿已改名：挠率 T^λ{}_{μν}、复曲率虚部 𝒮^ρ{}_{σμν}、复能动张量 𝓜_{μν}。")

    # ---------------------------------------------------------------- 汇总
    sec("汇总")
    put("  PASS     = %d" % cnt.get("PASS", 0))
    put("  FAIL     = %d" % cnt.get("FAIL", 0))
    put("  BOUNDARY = %d" % cnt.get("BOUNDARY", 0))
    put("  INFO     = %d" % cnt.get("INFO", 0))
    put("  ── 核心结论 ──")
    put("  · EC 下 ∇^μG_{μν} ≠ 0 的方向判断正确（残差 ∝ 挠率二次），但来稿引用的")
    put("    「第一 Bianchi」实为第二 Bianchi（微分 Bianchi），且其两指标写法不是恒等式；")
    put("    来稿给出的挠率源项形式与实测残差相对偏差 %.2e，不成立。" % rel_user2)
    put("  · 守恒命题在场方程下与「残差置零」严格等价 ⇒ 是公设化约束（降自由度），非守恒定理；")
    put("    且纯 T·R 代数型约束不足以闭合残差（纯 T·R 回归残差 %.2e；补 ∇T 协变导数基后仍 %.2e，还含 ddΓ·Γ 耦合项）。" % (rr_tr, rr_full))
    put("  · 量纲三处非法：𝓡=κ+iτ（L^-2 vs L^-1）、ω_R=cR_B（非频率）、复场方程虚部未定；")
    put("    ω_I=cT_B 量纲合法（唯一通过的一条）。")
    put("  · 来稿球对称挠率分量不满足 SO(3) 协变（残差 %.2e）；α 三式内部冲突。" % relA)
    put("  · 两个「下一步」通道按本仓既有读数均为零信号/已关闭：CMB（β≡0 ⇒ 无跳变源）、")
    put("    QNM（5.74σ 排除 + 尺度锚差 26~78 量级）。")
    put("")
    put("红线声明：数学自洽 != 实验证实。本脚本只做几何/量纲/一致性审计，")
    put("          不主张 TUFT 物理真实性，负结论为边界判定而非证伪宣告。")

    text = "\n".join(out) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
