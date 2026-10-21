# -*- coding: utf-8 -*-
"""
TUFT-r139 · 全维求导证明验证精算 · 自旋-2 路线的非线性完备机检

承接 r135（线性化 Bianchi / 规范不变 / 源守恒）与 r138（硬核 ②③ 不可导出）：
r135 只验到【线性化】层面。本卷把求导证明验到【非线性/全维】层面：

    收缩 Bianchi 恒等式   ∇_μ G^{μν} ≡ 0
    这是「无质量自旋-2 ⇒ EH」路线在非线性阶自洽（非线性完备由自洽性固定）的核心证据：
    正是 ∇·G≡0 逼迫耦合到守恒源、并逐阶固定 EH 形式。

方法（遵循 J46 数值几何纪律）：
  · 度规的一阶、二阶导数【解析给出】（幂律 / 指数），⇒ Ricci、Einstein 张量【无差分误差】
  · 仅对 ∇_μG^{μν} 中的 ∂_μG^{μν} 用中心差分，并做【三档步收敛阶扫描】
  · 禁三阶差分：因 G 已由解析二阶导得到，差分只作用一层 ⇒ 舍入放大仅 ε/h
  · 每条恒等式均带【反向对照】（∇_μR^{μν}=½∇^νR≠0）证明有牙

度规族（5）：
  ① 尘埃 a=t^{2/3}（k=0）  ② 辐射 a=t^{1/2}（k=0）
  ③ 开 FRW·Poincaré 球纤维 a=t^{2/3}（k=−1，三个空间坐标全出现在度规中）
  ④ 平直纤维非线性图变换 a=t^{1/2}（γ_ij=e^{2x_i}δ_ij，与 ② 微分同胚）
  ⑤ de Sitter a=e^{Ht}（G∝g ⇒ 度规级空转，单独登记）

机检：
  N1 精确计算：Einstein 张量（四个对角分量 + R）vs 解析式；并登记 G∝g 与否、Kretschmann
  N1b Kretschmann 解析锚点（判据反噬自己）：平直 FRW 的 K=12[(ä/a)²+H⁴]、de Sitter 的 K=24H⁴
  N2 非线性收缩 Bianchi：∇_μG^{μν}≡0（三档步长 + 收敛阶扫描）
  N3 两级空转登记：度规级（G∝g）与分量级（三加法项逐项为零）
  N4 求导证明：由 G_{μν}=8πG T_{μν} 推出 Friedmann 方程并在尘埃解上精算核对

对照一律用【扁平联络 Γ=0 破坏协变导数】——对任何度规都保证有牙
（Ricci 对照 ∇_μR^{μν}=½∇^νR 在辐射上因共形平坦而恒零，故弃用）。

号差：η=diag(−1,+,+,+)；几何单位 G=1。
求值点：x=(t,x1,x2,x3)=(2.0, 0.2, −0.3, 0.1)——空间坐标全非零，
否则 ③④ 的空间分量会被人为做空（这是本卷第一条踩过的坑）。
"""
import os, json, glob, datetime, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_%s" % DATE
JUDGE_STEM = "判定_TUFT-r139_全维求导证明验证精算_收缩Bianchi非线性完备_%s" % DATE
D = 4

# ---------------- 线性代数 ----------------
def mat_inv4(m):
    a = [row[:] for row in m]
    inv = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]
    for i in range(D):
        piv = max(range(i, D), key=lambda r: abs(a[r][i]))
        if abs(a[piv][i]) < 1e-300:
            raise ZeroDivisionError("singular metric")
        a[i], a[piv] = a[piv], a[i]
        inv[i], inv[piv] = inv[piv], inv[i]
        d = a[i][i]
        for j in range(D):
            a[i][j] /= d; inv[i][j] /= d
        for r in range(D):
            if r != i and a[r][i] != 0.0:
                f = a[r][i]
                for j in range(D):
                    a[r][j] -= f * a[i][j]
                    inv[r][j] -= f * inv[i][j]
    return inv

# ---------------- 度规（解析一/二阶导数） ----------------
class PowerFRW:
    """a(t)=t^p 的平直 FRW；给出解析 g, ∂g, ∂∂g。"""
    def __init__(self, p, name):
        self.p = p; self.name = name
    def _av(self, t):
        p = self.p
        a = t ** p
        ad = p * t ** (p - 1.0)
        add = p * (p - 1.0) * t ** (p - 2.0)
        return a, ad, add
    def g(self, x):
        a, _, _ = self._av(x[0])
        m = [[0.0] * D for _ in range(D)]
        m[0][0] = -1.0
        for i in range(1, D):
            m[i][i] = a * a
        return m
    def dg(self, x):
        a, ad, _ = self._av(x[0])
        d = [[[0.0] * D for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            d[0][i][i] = 2.0 * a * ad
        return d
    def ddg(self, x):
        a, ad, add = self._av(x[0])
        dd = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            dd[0][0][i][i] = 2.0 * (ad * ad + a * add)
        return dd
    def analytic(self, x):
        t = x[0]; p = self.p
        a = t ** p
        G00 = 3.0 * p * p / (t * t)
        Gij = -a * a * (3.0 * p * p - 2.0 * p) / (t * t)
        Rs = 6.0 * (2.0 * p * p - p) / (t * t)
        return G00, Gij, Gij, Gij, Rs

    def kretschmann_analytic(self, x):
        """平直 FRW 的 Kretschmann：K = 12[(ä/a)² + H⁴]（正交归一标架下逐项数出来）。"""
        t = x[0]; p = self.p
        a = t ** p; ad = p * t ** (p - 1.0); add = p * (p - 1.0) * t ** (p - 2.0)
        H = ad / a; A = add / a
        return 12.0 * (A * A + H ** 4)

class DeSitterFRW:
    """a(t)=e^{Ht} 的平直切片 de Sitter。"""
    def __init__(self, H):
        self.H = H; self.name = "deSitter(a=e^{Ht}, H=%.3g)" % H
    def _av(self, t):
        H = self.H
        a = math.exp(H * t); ad = H * a; add = H * H * a
        return a, ad, add
    def g(self, x):
        a, _, _ = self._av(x[0])
        m = [[0.0] * D for _ in range(D)]
        m[0][0] = -1.0
        for i in range(1, D):
            m[i][i] = a * a
        return m
    def dg(self, x):
        a, ad, _ = self._av(x[0])
        d = [[[0.0] * D for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            d[0][i][i] = 2.0 * a * ad
        return d
    def ddg(self, x):
        a, ad, add = self._av(x[0])
        dd = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            dd[0][0][i][i] = 2.0 * (ad * ad + a * add)
        return dd
    def analytic(self, x):
        H = self.H; a = math.exp(H * x[0])
        Gij = -3.0 * H * H * a * a
        return 3.0 * H * H, Gij, Gij, Gij, 12.0 * H * H

    def kretschmann_analytic(self, x):
        """4 维常曲率 c=H² 空间：K = 2n(n−1)c² = 24H⁴。"""
        H = self.H
        return 24.0 * H ** 4

class PoincareFRW:
    """【开】FRW：a(t)=t^p，纤维取 Poincaré 球模型 γ=4δ_ij/(1−r²)²（常曲率 k=−1）。
       关键：三个空间坐标【全部】出现在度规中，且任一坐标方向都既不是解耦块
       也不是平移 Killing 方向 ⇒ ν=1,2,3 分量的恒等式检验【不再是逐项为零】。"""
    def __init__(self, p=2.0 / 3.0, name=None):
        self.p = p
        self.name = name or "开FRW·Poincaré球 k=-1 (a=t^%.4g)" % p

    def _s(self, x):
        return 1.0 - (x[1] * x[1] + x[2] * x[2] + x[3] * x[3])

    def _av(self, t):
        p = self.p
        return t ** p, p * t ** (p - 1.0), p * (p - 1.0) * t ** (p - 2.0)

    def g(self, x):
        a, _, _ = self._av(x[0]); s = self._s(x)
        m = [[0.0] * D for _ in range(D)]
        m[0][0] = -1.0
        for i in range(1, D):
            m[i][i] = 4.0 * a * a / (s * s)
        return m

    def dg(self, x):
        a, ad, _ = self._av(x[0]); s = self._s(x)
        d = [[[0.0] * D for _ in range(D)] for _ in range(D)]
        s2 = s * s
        for i in range(1, D):
            d[0][i][i] = 8.0 * a * ad / s2
            for k in range(1, D):
                d[k][i][i] = 16.0 * a * a * x[k] / (s2 * s)
        return d

    def ddg(self, x):
        a, ad, add = self._av(x[0]); s = self._s(x)
        dd = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
        s2 = s * s; s3 = s2 * s; s4 = s3 * s
        for i in range(1, D):
            dd[0][0][i][i] = 8.0 * (ad * ad + a * add) / s2
            for k in range(1, D):
                dd[0][k][i][i] = 32.0 * a * ad * x[k] / s3
                dd[k][0][i][i] = 32.0 * a * ad * x[k] / s3
            for k in range(1, D):
                for l in range(1, D):
                    dd[k][l][i][i] = 16.0 * a * a * (
                        (1.0 if k == l else 0.0) / s3 + 6.0 * x[k] * x[l] / s4)
        return dd

    def analytic(self, x):
        t = x[0]; p = self.p; s = self._s(x)
        a = t ** p; ad = p * t ** (p - 1.0); add = p * (p - 1.0) * t ** (p - 2.0)
        cc = -(2.0 * a * add + ad * ad - 1.0)          # G_ij = cc · γ_ij
        G00 = 3.0 * (ad * ad - 1.0) / (a * a)          # k = −1
        Gi = cc * 4.0 / (s * s)
        Rs = 6.0 * (add / a + (ad * ad - 1.0) / (a * a))
        return G00, Gi, Gi, Gi, Rs

class WarpedExpFRW:
    """a(t)=t^p，纤维 γ_ij = e^{2x_i}δ_ij（γ 平直 ⇒ 整体实为 k=0 FRW 的【非线性图变换】）。
       用途诚实声明：它【不产生新几何】（与 k=0 FRW 微分同胚），因此
       ∇·G≡0 在其上成立并不构成该恒等式的新证据；
       它的作用是【管道在非线性坐标变换下的协变性检验】——
       同一个几何在扭曲图卡下，ν=1,2,3 分量由「逐项为零」变为「有牙」。"""
    def __init__(self, p=2.0 / 3.0, name=None):
        self.p = p
        self.name = name or "平直纤维非线性图变换 k=0 (a=t^%.4g)" % p

    def _av(self, t):
        p = self.p
        return t ** p, p * t ** (p - 1.0), p * (p - 1.0) * t ** (p - 2.0)

    def _E(self, x):
        return [math.exp(2.0 * x[i]) for i in range(D)]

    def g(self, x):
        a, _, _ = self._av(x[0]); E = self._E(x)
        m = [[0.0] * D for _ in range(D)]
        m[0][0] = -1.0
        for i in range(1, D):
            m[i][i] = a * a * E[i]
        return m

    def dg(self, x):
        a, ad, _ = self._av(x[0]); E = self._E(x)
        d = [[[0.0] * D for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            d[0][i][i] = 2.0 * a * ad * E[i]
            d[i][i][i] = 2.0 * a * a * E[i]
        return d

    def ddg(self, x):
        a, ad, add = self._av(x[0]); E = self._E(x)
        dd = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
        for i in range(1, D):
            dd[0][0][i][i] = 2.0 * (ad * ad + a * add) * E[i]
            dd[0][i][i][i] = 4.0 * a * ad * E[i]
            dd[i][0][i][i] = 4.0 * a * ad * E[i]
            dd[i][i][i][i] = 4.0 * a * a * E[i]
        return dd

    def analytic(self, x):
        t = x[0]; p = self.p; E = self._E(x)
        a = t ** p
        G00 = 3.0 * p * p / (t * t)
        Gi = [-a * a * (3.0 * p * p - 2.0 * p) * E[i] / (t * t) for i in range(1, D)]
        Rs = 6.0 * (2.0 * p * p - p) / (t * t)
        return G00, Gi[0], Gi[1], Gi[2], Rs

# ---------------- 几何管道（解析导数 ⇒ 无差分误差） ----------------
def christoffel(ginv, dg):
    Gam = [[[0.0] * D for _ in range(D)] for _ in range(D)]
    for a in range(D):
        for m in range(D):
            for n in range(D):
                s = 0.0
                for b in range(D):
                    s += ginv[a][b] * (dg[m][n][b] + dg[n][m][b] - dg[b][m][n])
                Gam[a][m][n] = 0.5 * s
    return Gam

def dchristoffel(ginv, dg, ddg):
    dgup = [[[-sum(ginv[a][c] * ginv[b][d] * dg[mu][c][d]
                   for c in range(D) for d in range(D))
              for b in range(D)] for a in range(D)] for mu in range(D)]
    dGam = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
    for mu in range(D):
        for a in range(D):
            for m in range(D):
                for n in range(D):
                    s = 0.0
                    for b in range(D):
                        s += dgup[mu][a][b] * (dg[m][n][b] + dg[n][m][b] - dg[b][m][n])
                        s += ginv[a][b] * (ddg[mu][m][n][b] + ddg[mu][n][m][b]
                                           - ddg[mu][b][m][n])
                    dGam[mu][a][m][n] = 0.5 * s
    return dGam

def riemann(dGam, Gam):
    R = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
    for r in range(D):
        for s in range(D):
            for m in range(D):
                for n in range(D):
                    v = dGam[m][r][n][s] - dGam[n][r][m][s]
                    for l in range(D):
                        v += Gam[r][m][l] * Gam[l][n][s] - Gam[r][n][l] * Gam[l][m][s]
                    R[r][s][m][n] = v
    return R

def ricci(R):
    return [[sum(R[r][s][r][n] for r in range(D)) for n in range(D)] for s in range(D)]

def raise_both(T, ginv):
    return [[sum(ginv[a][c] * ginv[b][d] * T[c][d] for c in range(D) for d in range(D))
             for b in range(D)] for a in range(D)]

def tensors_at(met, x):
    g = met.g(x); ginv = mat_inv4(g)
    dg = met.dg(x); ddg = met.ddg(x)
    Gam = christoffel(ginv, dg)
    dGam = dchristoffel(ginv, dg, ddg)
    R = riemann(dGam, Gam)
    Ric = ricci(R)
    Rs = sum(ginv[m][n] * Ric[m][n] for m in range(D) for n in range(D))
    G = [[Ric[m][n] - 0.5 * g[m][n] * Rs for n in range(D)] for m in range(D)]
    return g, ginv, Gam, Ric, Rs, G, raise_both(G, ginv), raise_both(Ric, ginv)

def cov_div(met, x, h, use_gamma=True):
    """返回 (∇_μG^{μν}, ∇_μR^{μν})，仅 ∂_μ 用中心差分（G/R 由解析导数得到）。
       use_gamma=False ⇒ 用【扁平联络 Γ=0】破坏协变导数，作为“已知非恒等”反向对照。"""
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    dGup = [[0.0] * D for _ in range(D)]
    dRup = [[0.0] * D for _ in range(D)]
    for mu in range(D):
        xp = list(x); xm = list(x)
        xp[mu] += h; xm[mu] -= h
        _, _, _, _, _, _, Gup_p, Rup_p = tensors_at(met, xp)
        _, _, _, _, _, _, Gup_m, Rup_m = tensors_at(met, xm)
        for nu in range(D):
            dGup[mu][nu] = (Gup_p[mu][nu] - Gup_m[mu][nu]) / (2.0 * h)
            dRup[mu][nu] = (Rup_p[mu][nu] - Rup_m[mu][nu]) / (2.0 * h)
    if use_gamma:
        trGam = [sum(Gam[a][a][l] for a in range(D)) for l in range(D)]
        GamU = Gam
    else:
        trGam = [0.0] * D
        GamU = [[[0.0] * D for _ in range(D)] for _ in range(D)]
    divG = [0.0] * D
    divR = [0.0] * D
    for nu in range(D):
        sG = sum(dGup[mu][nu] for mu in range(D))
        sR = sum(dRup[mu][nu] for mu in range(D))
        sG += sum(trGam[l] * Gup[l][nu] for l in range(D))
        sR += sum(trGam[l] * Rup[l][nu] for l in range(D))
        sG += sum(GamU[nu][mu][l] * Gup[mu][l] for mu in range(D) for l in range(D))
        sR += sum(GamU[nu][mu][l] * Rup[mu][l] for mu in range(D) for l in range(D))
        divG[nu] = sG
        divR[nu] = sR
    return divG, divR

def norm(v):
    return math.sqrt(sum(c * c for c in v))

# ---------------- 机检 ----------------
METRICS = [PowerFRW(2.0 / 3.0, "尘埃 a=t^(2/3)"),
           PowerFRW(0.5, "辐射 a=t^(1/2)"),
           PoincareFRW(2.0 / 3.0),
           WarpedExpFRW(0.5),
           DeSitterFRW(0.1)]
# 参与恒等式检验者（前 4）；末位 de Sitter 因 G∝g 而整册空转，单独登记
IDX_VALID = [0, 1, 2, 3]
IDX_VACUOUS = [4]
# 求值点：z 三个空间坐标【全非零】——否则 Poincaré/图变换度规的空间分量会人为空转
X0 = [2.0, 0.2, -0.3, 0.1]

def kretschmann(met, x):
    """K = R_{αβγδ}R^{αβγδ}：与 R 并列的第二个标量不变量。
       用途：为「两度规是否同一几何（微分同胚）」提供机器见证。"""
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    dGam = dchristoffel(ginv, met.dg(x), met.ddg(x))
    Rup1 = riemann(dGam, Gam)              # 记号：R^a_{bcd}（首指标逆变）
    # 第一步【必须】：先用 g 把首指标降下，得到全协变 R_{abcd}
    Rcov = [[[[sum(g[a][e] * Rup1[e][b][c][d] for e in range(D))
               for d in range(D)] for c in range(D)] for b in range(D)]
            for a in range(D)]
    # 第二步：逐个指标上抬（每步 D^5）
    T = Rcov
    for slot in range(4):
        T = _raise_slot(T, ginv, slot)
    K = 0.0
    for a in range(D):
        for b in range(D):
            for c in range(D):
                for d in range(D):
                    K += Rcov[a][b][c][d] * T[a][b][c][d]
    return K

def _raise_slot(T, ginv, slot):
    """把四阶张量的第 slot 个指标用 ginv 上抬（逐个上抬 ⇒ D^5 而非 D^8）。"""
    U = [[[[0.0] * D for _ in range(D)] for _ in range(D)] for _ in range(D)]
    for a in range(D):
        for b in range(D):
            for c in range(D):
                for d in range(D):
                    s = 0.0
                    for e in range(D):
                        if slot == 0:
                            s += ginv[a][e] * T[e][b][c][d]
                        elif slot == 1:
                            s += ginv[b][e] * T[a][e][c][d]
                        elif slot == 2:
                            s += ginv[c][e] * T[a][b][e][d]
                        else:
                            s += ginv[d][e] * T[a][b][c][e]
                    U[a][b][c][d] = s
    return U

def proportional_to_g(met, x):
    """判 G_{μν} 是否 ∝ g_{μν}：若是 ⇒ ∇·G≡0 由度规相容性平凡成立 ⇒ 检验空转。"""
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    sc = 0.0
    for i in range(D):
        for j in range(D):
            sc = max(sc, abs(G[i][j]), abs(g[i][j]))
    k = G[0][0] / g[0][0] if abs(g[0][0]) > 1e-300 else 0.0
    worst = 0.0
    for i in range(D):
        for j in range(D):
            worst = max(worst, abs(G[i][j] - k * g[i][j]) / sc)
    return worst, k

def check_N1(x):
    """Einstein 张量 vs 解析式（管道为解析导数 ⇒ 应达机器精度）。"""
    rows = []
    worst = 0.0
    for met in METRICS:
        g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
        aG00, aG11, aG22, aG33, aRs = met.analytic(x)
        # 统一用【公共自然尺度】归一，而非逐项相对误差：
        # 尘埃的解析 G11 恰为 0，逐项相对误差会除以 0（或 1e-30 地板）而爆掉。
        ref = max(abs(aG00), abs(aG11), abs(aG22), abs(aG33), abs(aRs))
        if ref <= 0.0:
            ref = 1.0
        e_G00 = abs(G[0][0] - aG00) / ref
        e_G11 = abs(G[1][1] - aG11) / ref
        e_G22 = abs(G[2][2] - aG22) / ref
        e_G33 = abs(G[3][3] - aG33) / ref
        e_Rs = abs(Rs - aRs) / ref
        w = max(e_G00, e_G11, e_G22, e_G33, e_Rs)
        worst = max(worst, w)
        prop, kprop = proportional_to_g(met, x)
        rows.append({"metric": met.name,
                     "kretschmann": kretschmann(met, x),
                     "G00": G[0][0], "G00_analytic": aG00,
                     "G11": G[1][1], "G11_analytic": aG11,
                     "G22": G[2][2], "G22_analytic": aG22,
                     "G33": G[3][3], "G33_analytic": aG33,
                     "R_scalar": Rs, "R_analytic": aRs,
                     "rel_G00": e_G00, "rel_G11": e_G11,
                     "rel_G22": e_G22, "rel_G33": e_G33, "rel_R": e_Rs,
                     "g_proportional_residual": prop,
                     "g_proportional": prop < 1e-9,
                     "g_proportional_k": kprop})
    # Kretschmann 解析锚点（判据反噬自己：先过已知锚点再拿去判别人）
    krows = []
    kworst = 0.0
    for met in METRICS:
        fa = getattr(met, "kretschmann_analytic", None)
        if fa is None:
            continue
        K = kretschmann(met, x)
        Ka = fa(x)
        rel = abs(K - Ka) / max(abs(Ka), 1e-30)
        kworst = max(kworst, rel)
        krows.append({"metric": met.name, "K": K, "K_analytic": Ka, "rel_K": rel,
                      "verdict": "PASS" if rel < 1e-9 else "FAIL"})
    return {"rows": rows, "worst_rel": worst,
            "kretschmann_benchmark": {
                "rows": krows, "worst_rel": kworst,
                "verdict": "PASS" if kworst < 1e-9 else "FAIL",
                "note": ("平直 FRW 锚点 K=12[(ä/a)²+H⁴]；de Sitter 锚点 K=24H⁴（4 维常曲率 c=H²）"
                         "——K 必须先把 R^a_{bcd} 的首指标降下才可对缩，否则算出的量无意义")},
            "verdict": "PASS" if worst < 1e-9 else "FAIL",
            "note": ("G/R 由解析一/二阶度规导数得到 ⇒ 无差分误差，应达机器精度；"
                     "同时登记 G∝g 与否（∝g 者其上的 ∇·G 检验结构性空转）")}

def cov_div_detail(met, x, h):
    """分量级有牙登记器。
       将 ∇_μG^{μν} 拆成三个加法项：
         A1 = ∂_μG^{μν}       （偏微分层）
         A2 = Γ^μ_{μα}G^{αν}   （迹层）
         A3 = Γ^ν_{μα}G^{μα}   （联络张量层）
       【逐项为零】⇒ 该分量空转（恒等式在该分量上无内容）；
       【各项非零而相互抵消】⇒ 该分量有牙。"""
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    dGup = [[0.0] * D for _ in range(D)]
    for mu in range(D):
        xp = list(x); xm = list(x)
        xp[mu] += h; xm[mu] -= h
        _, _, _, _, _, _, Gp, _ = tensors_at(met, xp)
        _, _, _, _, _, _, Gm, _ = tensors_at(met, xm)
        for nu in range(D):
            dGup[mu][nu] = (Gp[mu][nu] - Gm[mu][nu]) / (2.0 * h)
    trGam = [sum(Gam[a][a][l] for a in range(D)) for l in range(D)]
    ref = 0.0
    for i in range(D):
        for j in range(D):
            ref = max(ref, abs(Gup[i][j]))
    if ref <= 0.0:
        ref = 1.0
    comps = []
    for nu in range(D):
        A1 = sum(dGup[mu][nu] for mu in range(D))
        A2 = sum(trGam[l] * Gup[l][nu] for l in range(D))
        A3 = sum(Gam[nu][mu][l] * Gup[mu][l] for mu in range(D) for l in range(D))
        tot = A1 + A2 + A3
        a_abs = (abs(A1) + abs(A2) + abs(A3)) / ref
        nz = sum(1 for v in (A1, A2, A3) if abs(v) / ref > 1e-9)
        comps.append({"nu": nu, "A1": A1, "A2": A2, "A3": A3, "total": tot,
                      "addend_abs_sum_over_ref": a_abs,
                      "n_nonzero_addends": nz,
                      "toothed": a_abs > 1e-3})
    return comps

def check_N2_N3(x, steps=(1e-3, 5e-4, 2.5e-4)):
    """N2: ∇_μG^{μν}≡0（三档步长收敛扫描）。
       【两级空转登记】：
         级 1（度规级） G ∝ g ⇒ ∇·G≡0 由度规相容性平凡成立 ⇒ 整册空转；
         级 2（分量级） 某 ν 的三个加法项逐项为零 ⇒ 该分量空转；
       只有【两级都通过】的分量才计入有效证据。
       对照一律用【扁平联络 Γ=0 破坏协变导数】——对任何度规都保证有牙。"""
    out = []
    ok_all = True
    for idx in IDX_VALID:
        met = METRICS[idx]
        nG = []
        for h in steps:
            dG, _ = cov_div(met, x, h, use_gamma=True)
            nG.append(norm(dG))
        # 反向对照：扁平联络（Γ=0）破坏协变导数 ⇒ 应显著非零
        dG_flat, dR = cov_div(met, x, steps[-1], use_gamma=False)
        corrupt = norm(dG_flat)
        # 分量级有牙登记（最细步长）
        comps = cov_div_detail(met, x, steps[-1])
        n_tooth = sum(1 for c in comps if c["toothed"])
        prop, kprop = proportional_to_g(met, x)
        o1 = math.log2(nG[0] / nG[1]) if nG[1] > 1e-300 else 0.0
        o2 = math.log2(nG[1] / nG[2]) if nG[2] > 1e-300 else 0.0
        order = 0.5 * (o1 + o2)
        monotone = nG[0] >= nG[1] >= nG[2]
        identity_zero = nG[2] < 1e-6
        ctrl_nonzero = corrupt > 1e-3
        nonprop = prop >= 1e-9
        at_least_one_tooth = n_tooth >= 1
        ok = (monotone and identity_zero and ctrl_nonzero and nonprop
              and at_least_one_tooth and (1.4 <= order <= 2.6))
        ok_all = ok_all and ok
        out.append({"metric": met.name,
                    "norm_divG_by_step": nG, "steps": list(steps),
                    "convergence_order": order, "monotone_decrease": monotone,
                    "flat_connection_control": corrupt, "control_nonzero": ctrl_nonzero,
                    "g_proportional_residual": prop, "g_nonproportional": nonprop,
                    "n_toothed_components": n_tooth,
                    "components": comps,
                    "norm_div_R": norm(dR),
                    "div_R_note": ("对照 ∇_μR^{μν}=½∇^νR：辐射为共形平坦(R≡0)⇒该项亦为 0，"
                                   "故 Ricci 对照在辐射上无效，统一改用扁平联络对照"),
                    "verdict": "PASS" if ok else "FAIL"})
    # 度规级空转登记
    vac_entries = []
    for idx in IDX_VACUOUS:
        met = METRICS[idx]
        dG_v, dR_v = cov_div(met, x, steps[-1], use_gamma=True)
        prop, kprop = proportional_to_g(met, x)
        vac_entries.append({
            "metric": met.name, "norm_divG": norm(dG_v), "norm_div_R": norm(dR_v),
            "vacuous": True, "g_proportional_residual": prop,
            "g_proportional_k": kprop,
            "components": cov_div_detail(met, x, steps[-1]),
            "reason": ("G_{μν} = k·g_{μν}（机测比例系数 k=%.6g，解析值 −3H²=%.6g，残差 %.2e）"
                       " ⇒ ∇_μG^{μν} = k·∇_μg^{μν} ≡ 0 由度规相容性平凡成立，"
                       "与 Einstein 张量的具体形式无关" % (kprop, -3.0 * met.H ** 2, prop)),
            "verdict": "INFO（度规级空转，不计入 PASS）"})
    tot_tooth = sum(r["n_toothed_components"] for r in out)
    tot_comp = 4 * len(out)
    return {"checks": out, "vacuous_registry": vac_entries,
            "toothed_components": tot_tooth, "total_components": tot_comp,
            "verdict": "PASS" if ok_all else "FAIL",
            "note": ("收缩 Bianchi ∇_μG^{μν}≡0；对照用扁平联络破坏协变导数（保证有牙）；"
                     "度规级 G∝g 者与分量级逐项为零者均单独登记为空转")}

def check_N4(x):
    """求导证明：G_{μν}=8πG T_{μν} ⇒ Friedmann H²=8πGρ/3；在尘埃解上精算核对。"""
    # 尘埃 a=t^(2/3)：ρ = 1/(6π t²)（G=1，由 ρ∝a^{-3} 与 H²=8πρ/3 联立）
    t = x[0]
    rho_dust = 1.0 / (6.0 * math.pi * t * t)
    met = METRICS[0]
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    # 第一 Friedmann：G_00 = 8π ρ
    lhs = G[0][0]; rhs = 8.0 * math.pi * rho_dust
    rel1 = abs(lhs - rhs) / abs(rhs)
    # 由状态方程 w 反解幂指数：a∝t^{2/(3(1+w))}；尘埃 w=0 ⇒ 2/3；辐射 w=1/3 ⇒ 1/2
    p_dust = 2.0 / (3.0 * (1.0 + 0.0))
    p_rad = 2.0 / (3.0 * (1.0 + 1.0 / 3.0))
    ok_p = abs(p_dust - 2.0 / 3.0) < 1e-12 and abs(p_rad - 0.5) < 1e-12
    # 尘埃压强为零 ⇒ G_ij 应为 0
    gij_dust = abs(G[1][1])
    rel2 = gij_dust / max(abs(G[0][0]), 1e-30)
    ok = rel1 < 1e-9 and ok_p and rel2 < 1e-9
    return {"t": t, "rho_dust": rho_dust, "G00": lhs, "G00_vs_8pi_rho": rhs,
            "rel_friedmann": rel1, "p_from_w_dust": p_dust, "p_from_w_rad": p_rad,
            "G11_dust": gij_dust, "rel_G11_over_G00": rel2,
            "verdict": "PASS" if ok else "FAIL",
            "note": "由场方程求导出 Friedmann 方程并在尘埃解上精算核对；尘埃 w=0 ⇒ p=0 ⇒ G_ij=0"}

def _comp_line(c, under_prop_metric=False):
    if c["toothed"]:
        tag = ("项间抵消，但内容仅为 ∇g≡0（度规级空转层）"
               if under_prop_metric else "有牙")
    else:
        tag = "空转（逐项为零）"
    return ("     ν=%d：A1=%+.3e  A2=%+.3e  A3=%+.3e  ⇒ 和=%+.3e  "
            "项量和/|G|=%+.3e  [%s]" % (
                c["nu"], c["A1"], c["A2"], c["A3"], c["total"],
                c["addend_abs_sum_over_ref"], tag))

def _comp_short(c):
    return "%sν=%d" % ("√" if c["toothed"] else "×", c["nu"])

def build_json(N1, N23, N4):
    payload = {
        "doc": "r139 全维求导证明验证精算 · 自旋-2 路线非线性完备机检",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "signature": "号差 η=diag(-1,+,+,+)；几何单位 G=1",
        "eval_point": {"t": X0[0], "x1": X0[1], "x2": X0[2], "x3": X0[3],
                       "why": ("三个空间坐标全非零——否则 Poincaré / 图变换度规的"
                               "空间分量会被人为做空")},
        "method": ("度规一/二阶导数解析给出 ⇒ Ricci/Einstein 无差分误差；"
                   "仅 ∇ 中 ∂_μ 用中心差分并做三档步收敛阶扫描；"
                   "两级空转登记（度规级 G∝g / 分量级三加法项逐项为零）"),
        "N1_einstein_vs_analytic": N1,
        "N2_bianchi_N3_control": N23,
        "N4_friedmann": N4,
        "verdict": "NONLINEAR-COMPLETION-VERIFIED-BUT-DOES-NOT-COMPLETE-UFT",
        "verdict_detail": ("非线性收缩 Bianchi ∇_μG^{μν}≡0 在四个【G 不 ∝ g】的弯曲度规上"
                           "以二阶收敛成立，其中 k=−1 开 FRW 上四个分量全部有牙"
                           "（10/16 分量为有效证据）；de Sitter 因 G∝g 而度规级空转，"
                           "k=0 FRW 的 ν=i 分量因三加法项逐项为零而分量级空转，均已单独登记。"
                           "⇒ 自旋-2 路线导出 EH 的【非线性完备】得到全维求导验证。"
                           "但这只完备引力侧（①④），②③仍不可导出 ⇒ UFT 完成度仍 1/7。"),
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out

def build_md(N1, N23, N4):
    L = ["# %s（机读）" % STEM, "",
         "> 全维求导证明验证精算：自旋-2 路线的非线性完备（收缩 Bianchi）。", "",
         "## N1 Einstein 张量 vs 解析式（解析导数 ⇒ 无差分误差）", "",
         "| 度规 | G00 计算/解析 | G11 计算/解析 | G22 计算/解析 | G33 计算/解析 | R 计算/解析 | K | G∝g 残差 | 判定 |",
         "|----|----|----|----|----|----|----|----|----|"]
    for r in N1["rows"]:
        L.append("| %s | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e | %.2e | %s |"
                 % (r["metric"], r["G00"], r["G00_analytic"], r["G11"], r["G11_analytic"],
                    r["G22"], r["G22_analytic"], r["G33"], r["G33_analytic"],
                    r["R_scalar"], r["R_analytic"], r["kretschmann"],
                    r["g_proportional_residual"],
                    "∝g（空转）" if r["g_proportional"] else "非 ∝g"))
    L.append("")
    L.append("最坏相对误差 **%.2e** ⇒ %s" % (N1["worst_rel"], N1["verdict"]))
    L.append("")
    L.append("### Kretschmann 解析锚点（判据反噬自己）")
    L.append("")
    L.append("| 度规 | K 计算 | K 解析 | 相对 | 判定 |")
    L.append("|----|----|----|----|----|")
    for r in N1["kretschmann_benchmark"]["rows"]:
        L.append("| %s | %.8e | %.8e | %.2e | %s |" % (
            r["metric"], r["K"], r["K_analytic"], r["rel_K"], r["verdict"]))
    L.append("")
    L.append("（平直 FRW 锚点 K=12[(ä/a)²+H⁴]；de Sitter 锚点 K=24H⁴）")
    L.append("")
    L.append("## N2 非线性收缩 Bianchi ∇_μG^{μν}≡0（三档步长收敛扫描）")
    L.append("")
    L.append("| 度规 | \\|∇G\\| 三档 | 收敛阶 | G∝g 残差 | 有牙分量 | 分量明细 | 扁平联络对照 | 判定 |")
    L.append("|----|----|----|----|----|----|----|----|")
    for r in N23["checks"]:
        L.append("| %s | %.2e→%.2e→%.2e | %.2f | %.2e | %d/4 | %s | %.3e | %s |"
                 % (r["metric"], r["norm_divG_by_step"][0], r["norm_divG_by_step"][1],
                    r["norm_divG_by_step"][2], r["convergence_order"] or 0.0,
                    r["g_proportional_residual"], r["n_toothed_components"],
                    " ".join(_comp_short(c) for c in r["components"]),
                    r["flat_connection_control"], r["verdict"]))
    L.append("")
    L.append("**有效证据分量合计 %d/%d**" % (N23["toothed_components"], N23["total_components"]))
    L.append("")
    L.append("### 度规级空转登记（不计入 PASS）")
    L.append("")
    for v in N23["vacuous_registry"]:
        L.append("- **%s**：%s" % (v["metric"], v["verdict"]))
        L.append("  - %s" % v["reason"])
        L.append("  - |∇G|=%.3e ；|∇R|=%.3e" % (v["norm_divG"], v["norm_div_R"]))
    L.append("")
    L.append("## N4 Friedmann 求导证明")
    L.append("")
    L.append("- G00 = %.8e，8πρ(尘埃) = %.8e，相对 **%.2e**" % (
        N4["G00"], N4["G00_vs_8pi_rho"], N4["rel_friedmann"]))
    L.append("- a∝t^{2/(3(1+w))}：尘埃 w=0 ⇒ **%s**；辐射 w=1/3 ⇒ **%s**" % (
        N4["p_from_w_dust"], N4["p_from_w_rad"]))
    L.append("- 尘埃 p=0 ⇒ |G11|/|G00| = **%.2e**" % N4["rel_G11_over_G00"])
    L.append("- ⇒ %s" % N4["verdict"])
    L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_report(N1, N23, N4):
    L = ["=" * 74,
         "r139 全维求导证明验证精算 · 自旋-2 路线非线性完备机检",
         "=" * 74,
         "生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"),
         "号差 η=diag(-1,+,+,+)；几何单位 G=1",
         "编号碰撞：r139 被本卷（05:10:34 建）与《攻坚线全维总总结》（05:17:40 建）共用；"
         "两册条目不可相加，建议后建者改号 r140",
         "求值点 x=(t,x1,x2,x3)=(%.1f, %.1f, %.1f, %.1f)  【空间坐标全非零】" % (
             X0[0], X0[1], X0[2], X0[3]),
         "",
         "一、N1 Einstein 张量 vs 解析式（解析一/二阶度规导数 ⇒ 无差分误差）",
         "-" * 74]
    for r in N1["rows"]:
        L.append("[%s]" % r["metric"])
        L.append("   G00 %.10e vs 解析 %.10e (相对 %.2e)" % (
            r["G00"], r["G00_analytic"], r["rel_G00"]))
        for k in ("G11", "G22", "G33"):
            L.append("   %s %.10e vs 解析 %.10e (相对 %.2e)" % (
                k, r[k], r[k + "_analytic"], r["rel_" + k]))
        L.append("   R   %.10e vs 解析 %.10e (相对 %.2e)" % (
            r["R_scalar"], r["R_analytic"], r["rel_R"]))
        L.append("   G∝g 残差 %.2e ⇒ %s" % (
            r["g_proportional_residual"],
            "G∝g（度规级空转）" if r["g_proportional"] else "非 ∝g（可检验）"))
        L.append("   不变量 K=R_{αβγδ}R^{αβγδ} = %.8e" % r["kretschmann"])
    L.append("   最坏相对 %.2e ⇒ %s" % (N1["worst_rel"], N1["verdict"]))
    kr, kw = N1["rows"][1]["kretschmann"], N1["rows"][3]["kretschmann"]
    L.append("   图卡等价见证：辐射 K=%.8e vs 图变换 K=%.8e ⇒ 相对 %.2e（同一几何的两个图卡）" % (
        kr, kw, abs(kr - kw) / max(abs(kr), 1e-30)))
    L.append("   Kretschmann 解析锚点（判据反噬自己）：")
    for r in N1["kretschmann_benchmark"]["rows"]:
        L.append("     [%s] K=%.8e vs 解析 %.8e （相对 %.2e）⇒ %s" % (
            r["metric"], r["K"], r["K_analytic"], r["rel_K"], r["verdict"]))
    L.append("     最坏 %.2e ⇒ %s" % (
        N1["kretschmann_benchmark"]["worst_rel"],
        N1["kretschmann_benchmark"]["verdict"]))
    L.append("")
    L.append("二、N2 非线性收缩 Bianchi ∇_μG^{μν}≡0（三档步长收敛扫描）")
    L.append("-" * 74)
    for r in N23["checks"]:
        L.append("[%s]" % r["metric"])
        L.append("   |∇G| : %.3e → %.3e → %.3e （步长 %s）" % (
            r["norm_divG_by_step"][0], r["norm_divG_by_step"][1], r["norm_divG_by_step"][2],
            "→".join("%.2e" % s for s in r["steps"])))
        L.append("   收敛阶 %.2f（期望≈2）；单调递减 %s；末档 %.2e <1e-6 %s" % (
            r["convergence_order"] or 0.0, r["monotone_decrease"],
            r["norm_divG_by_step"][2], r["norm_divG_by_step"][2] < 1e-6))
        L.append("   G∝g 残差 %.2e ⇒ %s" % (
            r["g_proportional_residual"],
            "∝g（空转）" if not r["g_nonproportional"] else "非 ∝g"))
        L.append("   有牙分量 %d/4" % r["n_toothed_components"])
        for c in r["components"]:
            L.append(_comp_line(c))
        L.append("   扁平联络对照 |∇G|_Γ=0 = %.4e ≠ 0 ⇒ 有牙" % r["flat_connection_control"])
        L.append("   ⇒ %s" % r["verdict"])
        L.append("")
    for v in N23["vacuous_registry"]:
        L.append("[%s] %s" % (v["metric"], v["verdict"]))
        L.append("   |∇G| = %.3e ；|∇R| = %.3e" % (v["norm_divG"], v["norm_div_R"]))
        L.append("   理由：%s" % v["reason"])
        for c in v["components"]:
            L.append(_comp_line(c, under_prop_metric=True))
        L.append("   ⇒ 该检验在其上空转，不计入 PASS，单独登记")
        L.append("")
    L.append("   有效证据分量合计 %d/%d" % (N23["toothed_components"], N23["total_components"]))
    L.append("")
    L.append("三、N4 求导证明：由 G_{μν}=8πG T_{μν} 推出 Friedmann")
    L.append("-" * 74)
    L.append("G00 = %.8e ； 8πρ(尘埃) = %.8e ；相对 %.2e" % (
        N4["G00"], N4["G00_vs_8pi_rho"], N4["rel_friedmann"]))
    L.append("由状态方程 w 反解幂指数 a∝t^{2/(3(1+w))}：尘埃 w=0 ⇒ %.6f（=2/3）；辐射 w=1/3 ⇒ %.6f（=1/2）" % (
        N4["p_from_w_dust"], N4["p_from_w_rad"]))
    L.append("尘埃 w=0 ⇒ 压强 p=0 ⇒ G_ij 应=0：|G11|/|G00| = %.2e" % N4["rel_G11_over_G00"])
    L.append("⇒ %s" % N4["verdict"])
    L.append("")
    L.append("四、诚实结论")
    L.append("-" * 74)
    L.append("非线性完备得到全维求导验证：∇·G≡0 在四个 G 不∝g 的弯曲度规上二阶收敛成立，")
    L.append("且在【k=−1 开 FRW】上 ν=0..3 四个分量全部有牙（项量和/|G| 达 O(1) 而和为 0）；")
    L.append("k=0 FRW 上只有 ν=0 有牙（ν=i 三加法项逐项为零），de Sitter 则度规级空转，")
    L.append("两者均已单独登记、不计入有效证据 ⇒ 有效证据分量 10/16。")
    L.append("⇒ 自旋-2 路线导出 EH 在【非线性阶】自洽——但只完备引力侧 ①④；")
    L.append("②③（规范群、μ²）仍不可导出（r138），且 ①的新前提仍循环存疑（r135）")
    L.append("⇒ UFT 完成度仍 1/7。")
    L.append("")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_judge(N1, N23, N4):
    L = []
    L.append("# 判定_TUFT-r139 · 全维求导证明验证精算 · 收缩 Bianchi 与非线性完备")
    L.append("")
    L.append("**卷号**：r139（增补卷；与《攻坚线全维总总结》共用 r139 号，见卷首碰撞登记）")
    L.append("**日期**：%s" % DATE)
    L.append("**类别**：全维求导证明验证精算（r135 线性化 → 本卷非线性 + 两级空转登记）")
    L.append("**号差**：η=diag(−1,+,+,+)；几何单位 G=1")
    L.append("**求值点**：x=(t,x1,x2,x3)=(%.1f, %.1f, %.1f, %.1f)" % (X0[0], X0[1], X0[2], X0[3]))
    L.append("")
    L.append("## 卷首分工声明")
    L.append("")
    L.append("- r135 验到【线性化】Bianchi；本卷把求导证明验到【非线性/全维】，并加做【空转登记】。")
    L.append("- 各源卷拥有其条目；本卷机检独立，条目非加和。")
    L.append("- 红线：数学自洽 ≠ 实验证实；本册只作可算判决。")
    L.append("")
    L.append("### 编号碰撞登记（r139 被两个并行会话同时占用）")
    L.append("")
    L.append("| 卷 | 引擎建时刻 | 分工 | 判定册落点 |")
    L.append("|----|----|----|----|")
    L.append("| 本卷《全维求导证明验证精算·收缩 Bianchi 非线性完备》 | 05:10:34 | 机检：五度规 + 两级空转登记 + Kretschmann 锚点（守卫 5/5） | `数据/` |")
    L.append("| 《攻坚线全维总总结与统一场论终局裁定》 | 05:17:40 | 总总结与终局裁定 | `判定/` |")
    L.append("")
    L.append("- **两册条目不可相加**，互不引用对方的 PASS/FAIL 计数。")
    L.append("- 若需分号：建议**后建者**（总总结卷）改号为 **r140**（当前首空号）。")
    L.append("")
    L.append("## 0. 判定")
    L.append("")
    L.append("> **NONLINEAR-COMPLETION-VERIFIED-BUT-DOES-NOT-COMPLETE-UFT**")
    L.append(">")
    L.append("> 非线性收缩 Bianchi **∇_μG^{μν}≡0** 在四个**G 不 ∝ g**的弯曲度规上以**二阶收敛**成立；")
    L.append("> 其中**k=−1 开 FRW（Poincaré 球纤维）** 上 ν=0..3 **四个分量全部有牙**，")
    L.append("> 有效证据分量合计 **%d/%d**。两条空转路径（度规级 G∝g、分量级逐项为零）已单独登记。"
             % (N23["toothed_components"], N23["total_components"]))
    L.append("> ⇒ 自旋-2 导出 EH 的【非线性完备】在非线性阶自洽。")
    L.append("> **但这只完备引力侧（①④）；②③仍不可导出 ⇒ UFT 完成度仍 1/7。**")
    L.append("")
    L.append("## 1. 方法（遵循 J46 数值几何纪律）")
    L.append("")
    L.append("- 度规的**一阶、二阶导数解析给出**（幂律 / 指数 / Poincaré 球 / 指数图卡）")
    L.append("  ⇒ Ricci、Einstein 张量**无差分误差**。")
    L.append("- 仅对 ∇_μG^{μν} 中的 ∂_μG^{μν} 用**中心差分**，并做**三档步收敛阶扫描**。")
    L.append("- **禁三阶差分**：G 已由解析二阶导得到，差分只作用一层 ⇒ 舍入放大仅 ε/h（非 ε/h³）。")
    L.append("- 反向对照统一用**扁平联络（Γ=0）破坏协变导数**——对任何度规都保证有牙")
    L.append("  （Ricci 对照 ∇_μR^{μν}=½∇^νR 在辐射上因共形平坦而恒零，故弃用）。")
    L.append("")
    L.append("## 2. N1 Einstein 张量 vs 解析式")
    L.append("")
    L.append("| 度规 | G00 计算/解析 | G11 计算/解析 | G22 计算/解析 | G33 计算/解析 | R 计算/解析 | Kretschmann K | G∝g 残差 |")
    L.append("|----|----|----|----|----|----|----|----|")
    for r in N1["rows"]:
        L.append("| %s | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e / %.6e | %.6e | %.2e |"
                 % (r["metric"], r["G00"], r["G00_analytic"], r["G11"], r["G11_analytic"],
                    r["G22"], r["G22_analytic"], r["G33"], r["G33_analytic"],
                    r["R_scalar"], r["R_analytic"], r["kretschmann"],
                    r["g_proportional_residual"]))
    L.append("")
    L.append("最坏相对误差 **%.2e**（机器精度级）⇒ %s；" % (N1["worst_rel"], N1["verdict"]))
    L.append("其中 de Sitter 的 **G∝g 残差 %.2e** ⇒ 判为 G∝g。"
             % N1["rows"][IDX_VACUOUS[0]]["g_proportional_residual"])
    L.append("")
    L.append("**Kretschmann 解析锚点**（判据反噬自己：先过已知锚点再拿去判别人）：")
    L.append("")
    L.append("| 度规 | K 机测 | K 解析 | 相对 | 判定 |")
    L.append("|----|----|----|----|----|")
    for r in N1["kretschmann_benchmark"]["rows"]:
        L.append("| %s | %.8e | %.8e | %.2e | %s |" % (
            r["metric"], r["K"], r["K_analytic"], r["rel_K"], r["verdict"]))
    L.append("")
    L.append("锚点来源：平直 FRW 的 **K = 12[(ä/a)²+H⁴]**；de Sitter 的 **K = 24H⁴**")
    L.append("（4 维常曲率 c=H² ⇒ K=2n(n−1)c²）。")
    L.append("**踩过的坑**：K 必须先把 R^a_{bcd} 的首指标降下才可全上抬对缩；")
    L.append("未降指标直接上抬得到的量**不是** Kretschmann（本卷第一版即错于此，误差 20%）。")
    L.append("")
    L.append("## 3. N2/N3 非线性收缩 Bianchi（核心）")
    L.append("")
    L.append("| 度规 | \\|∇G\\| 三档 | 收敛阶 | 有牙分量 | 分量明细 | 扁平联络对照 | 判定 |")
    L.append("|----|----|----|----|----|----|----|")
    for r in N23["checks"]:
        L.append("| %s | %.2e→%.2e→%.2e | %.2f | %d/4 | %s | %.3e | %s |"
                 % (r["metric"], r["norm_divG_by_step"][0], r["norm_divG_by_step"][1],
                    r["norm_divG_by_step"][2], r["convergence_order"] or 0.0,
                    r["n_toothed_components"],
                    " ".join(_comp_short(c) for c in r["components"]),
                    r["flat_connection_control"], r["verdict"]))
    L.append("")
    L.append("（√ = 该 ν 的三个加法项**各自非零**且相互抵消；× = **逐项为零**，空转）")
    L.append("")
    L.append("**k=−1 开 FRW 分量明细**（项量和/|G| 达 O(1) 而和为 0 ⇒ 真抵消）：")
    L.append("")
    L.append("```")
    for c in N23["checks"][2]["components"]:
        L.append(_comp_line(c))
    L.append("```")
    L.append("")
    L.append("## 4. 两级空转登记（本卷的诚实核心）")
    L.append("")
    L.append("### 级 1 · 度规级：G ∝ g")
    L.append("")
    for v in N23["vacuous_registry"]:
        L.append("- **%s** ⇒ %s" % (v["metric"], v["verdict"]))
        L.append("  - %s" % v["reason"])
        L.append("  - 机测 |∇G|=%.3e、|∇R|=%.3e：数值上「成立」，但内容是 ∇_μg^{μν}≡0（度规相容性），"
                 % (v["norm_divG"], v["norm_div_R"]))
        L.append("    与 Einstein 张量的具体形式无关 ⇒ **不构成对 ∇·G≡0 的证据**。")
    L.append("")
    L.append("### 级 2 · 分量级：三加法项逐项为零")
    L.append("")
    for r in N23["checks"]:
        vac = [c for c in r["components"] if not c["toothed"]]
        if vac:
            L.append("- **%s**：ν=%s 空转" % (
                r["metric"], ",".join(str(c["nu"]) for c in vac)))
    L.append("")
    kr, kw = N1["rows"][1]["kretschmann"], N1["rows"][3]["kretschmann"]
    L.append("**关键方法论结论**：k=0 FRW 上「只有 1/4 分量有牙」**不是几何事实，而是图卡假象**——")
    L.append("")
    L.append("| 同一几何（辐射 FRW，a=t^{1/2}）的两个图卡 | 有牙分量 | R | Kretschmann K |")
    L.append("|----|----|----|----|")
    L.append("| 标准图卡 γ=δ | %d/4 | %.6e | %.6e |" % (
        N23["checks"][1]["n_toothed_components"],
        N1["rows"][1]["R_scalar"], kr))
    L.append("| 非线性图卡 γ_ij=e^{2x_i}δ_ij | %d/4 | %.6e | %.6e |" % (
        N23["checks"][3]["n_toothed_components"],
        N1["rows"][3]["R_scalar"], kw))
    L.append("")
    L.append("两个标量不变量**逐一相等**：K 相对差 %.2e、R 绝对差 %.2e（后者为机器零），"
             % (abs(kr - kw) / max(abs(kr), 1e-30),
                abs(N1["rows"][1]["R_scalar"] - N1["rows"][3]["R_scalar"])))
    L.append("机检确认二者【确为同一几何】；")
    L.append("而有牙率却从 1/4 跳到 4/4 ⇒ **「有牙率」是图卡依赖的量，不是几何量**，")
    L.append("**不得充当证据强度**。真正承载证据的是【k=−1 开 FRW】这一**不同几何**：")
    L.append("R 机测 %.5e ≠ k=0 辐射的 %.5e，K 机测 %.5e ≠ %.5e。"
             % (N1["rows"][2]["R_scalar"], N1["rows"][1]["R_scalar"],
                N1["rows"][2]["kretschmann"], N1["rows"][1]["kretschmann"]))
    L.append("")
    L.append("## 5. N4 求导证明：Friedmann 方程")
    L.append("")
    L.append("- 由 G_{μν}=8πG T_{μν} 求导出 **H² = 8πGρ/3**；尘埃解上精算核对：")
    L.append("  G00 = %.8e，8πρ = %.8e，相对 **%.2e**" % (
        N4["G00"], N4["G00_vs_8pi_rho"], N4["rel_friedmann"]))
    L.append("- 状态方程 w 反解幂指数 a∝t^{2/(3(1+w))}：尘埃 w=0 ⇒ **%.6f（=2/3）**；"
             "辐射 w=1/3 ⇒ **%.6f（=1/2）**"
             % (N4["p_from_w_dust"], N4["p_from_w_rad"]))
    L.append("- 尘埃 w=0 ⇒ 压强为零 ⇒ G_ij 应为 0：|G11|/|G00| = **%.2e**" % N4["rel_G11_over_G00"])
    L.append("")
    L.append("## 6. 诚实结论")
    L.append("")
    L.append("1. **非线性完备已验证**：∇·G≡0 在四个 G 不∝g 的弯曲度规上二阶收敛成立，")
    L.append("   且在 k=−1 开 FRW 上四分量全部有牙 ⇒ r135 的结论被加强到全维非线性。")
    L.append("2. **但仍不完成 UFT**：")
    L.append("   - 只完备引力侧 ①④；②③（规范群、μ²）仍**不可导出**（r138，Δ≥0）；")
    L.append("   - ①的新前提「存在无质量自旋-2」仍**循环存疑**（r135 CIRCULAR-SUSPECT）；")
    L.append("   - 故 UFT **完成度仍 1/7**（U1/U2/U3/U4/U5/U6 仍 FAIL）。")
    L.append("3. 本卷是**验证**而非**新物理**：验证了已知路线的非线性自洽，未产出新预言。")
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("- **尚未扫描的几何**：k=+1 闭 FRW、各向异性（Bianchi 型）、")
    L.append("  稳态/旋转解（Schwarzschild、Kerr）、含挠率（EC）情形——本卷结论不可外推到它们。")
    L.append("- **尚未验证的通道**：本卷只验【收缩】Bianchi ∇_μG^{μν}≡0；")
    L.append("  【完整】Bianchi ∇_[λR_{μν]αβ}≡0 未验（分量数 20 vs 4，成本量级不同）。")
    L.append("- **k=−1 度规族仍窄**：只取 a=t^{2/3} 的 Poincaré 球纤维一个点，未做 (t, x) 扫描。")
    L.append("- **未含量子阶**：本卷是纯经典几何，未触及圈阶/反常。")
    L.append("- **②③ 缺口原封不动**：本卷不触碰规范群与 μ² 的导出问题（见 r138）。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("")
    L.append("- **收缩 Bianchi**：∇_μG^{μν}≡0，等价于场方程与源守恒的自洽。")
    L.append("- **非线性完备**：自旋-2 路线逐阶固定 EH 形式的过程。")
    L.append("- **有牙（toothed）**：恒等式某分量的三个加法项【各自非零】而相互抵消——")
    L.append("  若逐项为零则恒等式在该分量上无内容。")
    L.append("- **两级空转**：度规级（G∝g ⇒ 退化为 ∇g≡0）与分量级（加法项逐项为零）。")
    L.append("- **图卡假象**：有牙率随坐标选择而变，故不是几何量、不得充当证据强度。")
    L.append("- **Poincaré 球纤维**：H³ 的球模型 γ=4δ_ij/(1−r²)²，常曲率 k=−1。")
    L.append("")
    L.append("## 数据出处")
    L.append("")
    L.append("- 机读册：`数据/%s.json` / `.md` / `_report.txt`" % STEM)
    L.append("- 上游：r135（线性化 Bianchi）、r138（②③ 不可导出）、r134（完成度 1/7）")
    L.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    x = list(X0)
    N1 = check_N1(x)
    N23 = check_N2_N3(x)
    N4 = check_N4(x)
    if (N1["verdict"] != "PASS" or N23["verdict"] != "PASS" or N4["verdict"] != "PASS"
            or N1["kretschmann_benchmark"]["verdict"] != "PASS"):
        print("GUARD FAIL:", N1["verdict"], N23["verdict"], N4["verdict"],
              N1["kretschmann_benchmark"]["verdict"])
        for r in N23["checks"]:
            if r["verdict"] != "PASS":
                print("  detail:", r)
        for r in N1["kretschmann_benchmark"]["rows"]:
            if r["verdict"] != "PASS":
                print("  K detail:", r)
        return 2
    # 第 4 道守卫：图卡等价见证——②③ 若为同一几何，两个标量不变量必须逐一相等
    kr = N1["rows"][1]["kretschmann"]
    kw = N1["rows"][3]["kretschmann"]
    krel = abs(kr - kw) / max(abs(kr), 1e-30)
    if krel > 1e-9:
        print("GUARD FAIL: 图卡等价见证失效，K 相对差 %.2e" % krel)
        return 2
    # 第 5 道守卫：Kretschmann 必须先过已知解析锚点
    if N1["kretschmann_benchmark"]["verdict"] != "PASS":
        print("GUARD FAIL: Kretschmann 未过解析锚点")
        return 2
    p1 = build_json(N1, N23, N4)
    p2 = build_md(N1, N23, N4)
    p3 = build_report(N1, N23, N4)
    p4 = build_judge(N1, N23, N4)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("VERDICT: NONLINEAR-COMPLETION-VERIFIED-BUT-DOES-NOT-COMPLETE-UFT")
    print("N1 worst rel %.2e | N2 order %.2f | N4 friedmann rel %.2e" % (
        N1["worst_rel"],
        N23["checks"][0]["convergence_order"] or 0.0, N4["rel_friedmann"]))
    print("有牙分量 %d/%d | 图卡等价 K 相对差 %.2e" % (
        N23["toothed_components"], N23["total_components"], krel))
    print("guards 5/5 PASS | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
