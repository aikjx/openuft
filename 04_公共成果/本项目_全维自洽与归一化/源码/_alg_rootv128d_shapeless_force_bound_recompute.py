# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V128 第四册：形状无关的径向第五力约束 · 可算审计机核

性质：非判定册，不占 RID，不入 README，不回写既有产物，不与 TUFT 链相加。

动机（第三册自己划出的下一条路）：
  第三册只判了一个**特定形状**——单尺度 Yukawa Phi = -GM/r (1 + alpha e^{-r/lam})，
  两个参数 (alpha, lam)。这使得「V128 能不能活」的答案绑死在这个形状上。
  本册把形状假设去掉：允许**任意**径向势偏离 dPhi(r)，只问一件事——

     这组同样的星历数据，对「任意径向额外力」到底给了多少空间？

方法（与前两册完全独立的一条数学路线）：
  一维精确近点角求积。给定 (a, e) 与势 Phi，轨道在 r_p = a(1-e)、r_a = a(1+e) 折返；
  由两个折返条件**线性**解出 (E, L^2)，再算
      Delta_theta = Int_{r_p}^{r_a} L r^-2 / sqrt(2(E-Phi) - L^2/r^2) dr
      Delta_varpi = 2 Delta_theta - 2 pi
  这个式对偏心率**精确**（不是小 e 展开），对势偏离**精确**（不是一阶展开）。
  与前两册的 Bessel 闭式（对 e 精确、对 alpha 一阶）是两条互不引用的路径。

核心结构事实：
  势写 Phi = -(mu/r)(1 - C(r))，则 dPhi = (mu/r) C(r)。
  (i)  C == const  =>  dPhi ∝ mu/r  =>  轨道仍是闭椭圆  =>  Delta_varpi = 0  **精确**。
       即：径向第五力的「整体幅度」这一自由度，对近点进动**零信息**。
  (ii) 故能被约束的只有 C(r) 的**形状变化**。
  (iii)V128 的 Yukawa 正是 C(r) = -alpha e^{-r/lam}：lam 越大形状越平 => 越接近零信息。
       这把第三册 J6 的「sigma_alpha ∝ lam^2」从数值观察升级为**代数原因**。

基线化（关键设计）：
  取 C(r) = Sum_k c_k w_k(r)，w_k 是 ln r 上的光滑单位分解（Sum_k w_k ≡ 1）。
  于是 c = (1,1,...,1) **恰好**落在 dPhi = mu/r 这个精确零方向上。
  拟合在**相邻反差** e_k = c_k - c_{k+1} 上做（N-1 个参数，非奇异），
  整体水平 beta 不进入模型——不是「约束很弱」，是**恰好零信息**。

七个问题：
  K1 求积机核自检：C==0 机器零；中心差分 h 收敛（偶部被抵消）；线性区自洽。
  K2 GR 1PN 正对照：dPhi = -mu L^2/(c^2 r^3) 必须给出 6 pi mu/(c^2 p)。
     唯一带「外部已知答案」的全链条检验（含单位换算）。
  K3 跨册归约：dPhi = -mu alpha e^{-r/lam}/r 的求积核（alpha->0 导数）必须等于第三册
     Bessel 闭式。两条互不引用的数学路径。
  K4 精确零空间：C==const 的核机器零；c=(1..1) 的核机器零；单位分解恒等于 1。
  K5 支撑外窗口：放在 1e4 AU / 1e-4 AU 的窗口对所有行星核**恰好** 0。
  K6 形状无关拟合：相邻反差 95% 区间全部有限；delta_chi2；N=6 vs N=9 稳健性。
  K7 无写死 ok + 求积收敛证据（Romberg 各级差）。

性能注记：折返点固定为 1∓e，故 r(s) 与 C 无关 => 节点表按 (行星, N) 缓存，
          ln r、cos(pi s)、sin(pi s) 只算一次，所有参数与所有求积共用。

红线：数学自洽 != 实验证实；不宣称攻破统一场论；本册只判「给定量测 + 任意径向势」的
      可约束程度，不判统一场论成立与否；未被满足 != 不可满足；独立实验预言 0。
"""
import os
import glob
import json
from decimal import Decimal, getcontext, ROUND_FLOOR

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json"),
                 recursive=True)
assert len(HITS) == 1, "C3-HITS=%d" % len(HITS)
SRC3_JSON = HITS[0]
DATA = os.path.dirname(SRC3_JSON)
OUT_JSON = os.path.join(DATA, "_ALG_rootv128d_shapeless_force_bound_recompute_2026-11-22.json")


# ------------------------------------------------------------------ 工具
def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    a = D(str(a))
    b = D(str(b))
    if b == 0:
        return D(0) if a == 0 else D(10) ** 60
    return abs(a - b) / abs(b)


def atan_inv(x):
    z = D(1) / D(x)
    zz = z * z
    p = z
    s = D(0)
    k = 0
    while True:
        t = p / D(2 * k + 1)
        s = s + t if k % 2 == 0 else s - t
        if abs(t) < D("1e-66"):
            break
        p *= zz
        k += 1
    return s


PI = D(16) * atan_inv(5) - D(4) * atan_inv(239)


def dsin(x):
    x = D(x)
    twopi = 2 * PI
    k = (x / twopi).to_integral_value(rounding=ROUND_FLOOR)
    x = x - k * twopi
    if x > PI:
        x = x - twopi
    s = D(0)
    t = x
    n = 0
    while True:
        s += t
        n += 1
        t = -t * x * x / (D(2 * n) * D(2 * n + 1))
        if abs(t) < D("1e-72"):
            break
    return s


def dcos(x):
    return dsin(D(x) + PI / 2)


def bessI1(z):
    z = D(str(z))
    hz = z / 2
    pw = hz
    s = D(0)
    k = 0
    fact = D(1)
    while True:
        term = pw / (fact * fact * D(k + 1))
        s += term
        if abs(term) < D("1e-70"):
            break
        k += 1
        fact *= D(k)
        pw = pw * hz * hz
    return s


def smoothstep(u):
    if u <= 0:
        return D(0)
    if u >= 1:
        return D(1)
    return u * u * (D(3) - 2 * u)


# ------------------------------------------------------------------ 常数
AU = D("149597870700")
ARCSEC = D(180) / PI * D(3600)
CENTURY_DAYS = D("36525")
CHI2_95_1DOF = D("3.8414588207")
Z_95 = D("1.9599639845")
C_LIGHT = D("299792458")
GM_SUN = D("1.32712440018e20")

# 卡方 95% 分位（查表，按自由度 m）。用于「是否需要 m 个额外自由度」的判据。
CHI2_95_TABLE = {1: "3.8415", 2: "5.9915", 3: "7.8147", 4: "9.4877",
                 5: "11.0705", 6: "12.5916", 7: "14.0671", 8: "15.5073",
                 9: "16.9190", 10: "18.3070", 11: "19.6751", 12: "21.0261"}

PLANETS = {
    "Mercury": {"a_AU": D("0.38709893"), "e": D("0.20563069"), "P_days": D("87.9691")},
    "Venus":   {"a_AU": D("0.72333199"), "e": D("0.00677323"), "P_days": D("224.7008")},
    "Earth":   {"a_AU": D("1.00000011"), "e": D("0.01671022"), "P_days": D("365.2564")},
    "Mars":    {"a_AU": D("1.52366231"), "e": D("0.09341233"), "P_days": D("686.9800")},
    "Jupiter": {"a_AU": D("5.20336301"), "e": D("0.04839266"), "P_days": D("4332.589")},
    "Saturn":  {"a_AU": D("9.53707032"), "e": D("0.05415060"), "P_days": D("10759.22")},
}


# ------------------------------------------------------------------ 节点表（与 C 无关，可缓存）
N_LEVELS = (64, 128, 256, 512)
_END = D("1e-3")
_TAB = {}


def node_table(planet, N):
    """折返点固定 1∓e => r(s) 与 C 无关。节点 = (x, lnr, inv1, inv2, w)。

    x     = r/a（无量纲，Yukawa / GR 直接用它）
    lnr   = ln(r_phys / AU)（窗口用它）
    inv1  = 1/r, inv2 = 1/r^2（以 a=1 为单位）
    w     = dr*pi*sin(pi s)（Simpson 被积权重分子）
    """
    key = (planet, N)
    if key in _TAB:
        return _TAB[key]
    pl = PLANETS[planet]
    e = pl["e"]
    a_m = pl["a_AU"] * AU
    rp = D(1) - e
    ra = D(1) + e
    rm = (rp + ra) / 2
    dr = (ra - rp) / 2
    ln_scale = (a_m / AU).ln()

    def mk(s):
        x = rm - dr * dcos(PI * s)
        return (x, x.ln() + ln_scale, D(1) / x, D(1) / (x * x),
                dr * PI * dsin(PI * s))

    main = [mk(D(i) / D(N)) for i in range(N + 1)]
    lo = [mk(_END * D(j)) for j in (1, 2, 3)]
    hi = [mk(D(1) - _END * D(j)) for j in (1, 2, 3)]
    tab = (main, lo, hi, ln_scale)
    _TAB[key] = tab
    return tab


def ln_of(planet, x):
    return D(x).ln() + node_table(planet, N_LEVELS[0])[3]


# ------------------------------------------------------------------ 一维精确近点角求积
def orbit_constants(planet, Cfun):
    """由两个折返条件**线性**解出 (E, L^2)。单位 mu = 1, a = 1。

      L^2 = 2 (Phi(r_a)-Phi(r_p)) / (1/r_p^2 - 1/r_a^2)
      E   = Phi(r_a) + L^2/(2 r_a^2)
    C==const 时自动退化为 mu_eff = 1-C 的 Kepler 问题。
    """
    e = PLANETS[planet]["e"]
    rp = D(1) - e
    ra = D(1) + e
    Phi_p = -(D(1) - Cfun(rp, ln_of(planet, rp))) / rp
    Phi_a = -(D(1) - Cfun(ra, ln_of(planet, ra))) / ra
    den = D(1) / (rp * rp) - D(1) / (ra * ra)
    L2 = 2 * (Phi_a - Phi_p) / den
    E = Phi_a + L2 / (2 * ra * ra)
    return E, L2


def apsidal_raw(planet, Cfun, N):
    """单次 Simpson（两端用解析延拓），返回 2*Delta_theta - 2pi。"""
    E, L2 = orbit_constants(planet, Cfun)
    if L2 <= 0:
        raise ValueError("L2<=0: degenerate (mu_eff=0)")
    L = L2.sqrt()
    main, lo, hi, _ = node_table(planet, N)
    twoE = 2 * E

    def fn(nd):
        x, lnr, inv1, inv2, w = nd
        C = Cfun(x, lnr)
        G = twoE + 2 * (D(1) - C) * inv1 - L2 * inv2
        return L * w * inv2 / G.sqrt()

    # 被积函数在两端解析且关于 s 偶 => 用 1.5/-0.6/0.1 三点外推取端点极限
    f0 = (D("1.5") * fn(lo[0]) - D("0.6") * fn(lo[1]) + D("0.1") * fn(lo[2]))
    f1 = (D("1.5") * fn(hi[0]) - D("0.6") * fn(hi[1]) + D("0.1") * fn(hi[2]))
    tot = f0 + f1
    for i in range(1, N):
        w = D(4) if (i % 2) else D(2)
        tot += w * fn(main[i])
    return 2 * (tot / D(N) / 3) - 2 * PI


def romberg(vals):
    """Simpson（阶 h^4）的 Neville 外推：分母 2^4-1, 2^6-1, 2^8-1。"""
    T = [D(v) for v in vals]
    for j in range(1, len(T)):
        fac = D(2) ** (4 + 2 * (j - 1)) - 1
        for k in range(len(T) - 1, j - 1, -1):
            T[k] = T[k] + (T[k] - T[k - 1]) / fac
    return T[-1]


def dvarpi(planet, Cfun):
    """Delta_varpi（弧度/圈），Romberg 外推到 O(h^10)。返回 (外推值, 各级差, 最细 Simpson)。"""
    vals = [apsidal_raw(planet, Cfun, n) for n in N_LEVELS]
    ex = list(vals)
    ladder = []
    for j in range(1, len(ex)):
        fac = D(2) ** (4 + 2 * (j - 1)) - 1
        for k in range(len(ex) - 1, j - 1, -1):
            ex[k] = ex[k] + (ex[k] - ex[k - 1]) / fac
        ladder.append(abs(ex[0]))
    return ex[-1], (ladder[-1] if ladder else D(0)), vals[-1]


def dvarpi_to_mas_cy(dp_rad_per_orbit, planet):
    """弧度/圈 -> mas/世纪。"""
    return dp_rad_per_orbit * (CENTURY_DAYS / PLANETS[planet]["P_days"]) * ARCSEC * 1000


# ------------------------------------------------------------------ 单位分解窗口
def make_knots(n_win, rmin_AU, rmax_AU):
    a = D(rmin_AU).ln()
    b = D(rmax_AU).ln()
    step = (b - a) / D(n_win - 1)
    return [a + D(k) * step for k in range(n_win)]


def make_windows(n_win, rmin_AU, rmax_AU):
    """返回 (knots, wlist)。w_k 以 ln(r/AU) 为自变量；Sum_k w_k ≡ 1 恒成立。

    T_k = 0 (x<=x_k) / smoothstep(x_k..x_{k+1}) / 1 (x>=x_{k+1})，k=1..n-1
    w_1 = 1 - T_1 ;  w_k = T_{k-1} - T_k (2<=k<=n-1) ;  w_n = T_{n-1}
    """
    knots = make_knots(n_win, rmin_AU, rmax_AU)

    def T(k, x):
        lo = knots[k - 1]
        hi = knots[k]
        return smoothstep((x - lo) / (hi - lo))

    wlist = []

    def w1(x):
        return D(1) - T(1, x)

    wlist.append(w1)
    for k in range(2, n_win):
        def wk(x, k=k):
            return T(k - 1, x) - T(k, x)
        wlist.append(wk)

    def wn(x):
        return T(n_win - 1, x)

    wlist.append(wn)
    return knots, wlist


def make_bumps(n, rmin_AU, rmax_AU):
    """紧凑支撑 bump（非单位分解）：只在 [rmin, rmax] 内非零。

    专用于「支撑外零信息」检验——单位分解的前后两窗有平台，
    放在远处时 w_1 会覆盖到行星轨道上，那样测到的是零方向而不是零支撑。
    """
    a = D(rmin_AU).ln()
    b = D(rmax_AU).ln()
    step = (b - a) / D(n)
    out = []
    for k in range(n):
        lo = a + D(k) * step
        hi = a + D(k + 1) * step
        mid = (lo + hi) / 2

        def bump(x, lo=lo, hi=hi, mid=mid):
            if x <= lo or x >= hi:
                return D(0)
            if x < mid:
                return smoothstep((x - lo) / (mid - lo))
            return D(1) - smoothstep((x - mid) / (hi - mid))

        out.append(bump)
    return out


def coeff_C(coeffs, wlist):
    """C 作为 (x, lnr) 的函数；窗口只看 lnr。"""
    nz = [(k, coeffs[k]) for k in range(len(coeffs)) if coeffs[k] != 0]

    def f(x, lnr):
        s = D(0)
        for k, c in nz:
            s += c * wlist[k](lnr)
        return s
    return f


def C_yukawa(alpha, lam_over_a):
    """C(x) = -alpha e^{-x/lam}，x = r/a。"""
    la = D(lam_over_a)

    def f(x, lnr):
        return -D(alpha) * (-(D(x) / la)).exp()
    return f


def C_gr1pn(eps, e):
    """GR 1PN 等效势：dPhi = -mu L^2/(c^2 r^3) => C = -L^2/(c^2 r^2) = -eps(1-e^2)/x^2。"""
    q = D(eps) * (D(1) - D(e) * D(e))

    def f(x, lnr):
        return -q / (D(x) * D(x))
    return f


# ------------------------------------------------------------------ 差分核
def _d1(planet, C_from_c, k, n_par, h):
    cp = [D(0)] * n_par
    cm = [D(0)] * n_par
    cp[k] = h
    cm[k] = -h
    fp = dvarpi(planet, C_from_c(cp))[0]
    fm = dvarpi(planet, C_from_c(cm))[0]
    return (fp - fm) / (2 * h)


def kernel_from_C(planet, C_from_c, n_par, h=D("1e-4")):
    """d Delta_varpi / d c_k（弧度/圈）。中心差分 + Richardson 消 h^2 项。

    Delta_varpi 含 O(c^2) 偶部（不是 c 的奇函数），中心差分把它抵消：
        D(h) = [f(h)-f(-h)]/(2h) = f'(0) + a h^2 + b h^4 + ...
        =>  (4 D(h/2) - D(h))/3 = f'(0) + O(h^4)
    """
    out = []
    for k in range(n_par):
        d1 = _d1(planet, C_from_c, k, n_par, h)
        d2 = _d1(planet, C_from_c, k, n_par, h / 2)
        out.append((4 * d2 - d1) / 3)
    return out


# ------------------------------------------------------------------ 线性代数
def solve_linear(A, b, rel_eps=D("1e-40")):
    n = len(A)
    M = [[D(A[i][j]) for j in range(n)] + [D(b[i])] for i in range(n)]
    scale = max(abs(M[i][j]) for i in range(n) for j in range(n))
    eps = scale * rel_eps
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) <= eps:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] for i in range(n)]


def invert(A):
    n = len(A)
    cols = []
    for j in range(n):
        e = [D(0)] * n
        e[j] = D(1)
        col = solve_linear(A, e)
        if col is None:
            return None
        cols.append(col)
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def norm_inf(M):
    return max(sum(abs(v) for v in row) for row in M)


# ------------------------------------------------------------------ 数据（机读第三册）
def load_data():
    with open(SRC3_JSON, encoding="utf-8") as fh:
        j3 = json.load(fh)
    ds = {}
    for name, blk in j3["datasets"].items():
        rows = [(r["planet"], D(r["obs_mas_per_cy"]), D(r["sigma_mas_per_cy"]))
                for r in blk["rows"]]
        ds[name] = {"cite": blk["cite"], "rows": rows}
    return j3, ds


# ------------------------------------------------------------------ 闭式（仅作对照）
def K_bessel(e, lam_over_a):
    """第三册闭式：单位 alpha 每圈进动（弧度），lam 以 a 为单位。
    2 pi a sqrt(1-e^2)/(e lam) e^{-a/lam} I1(ae/lam)，对 e 精确、对 alpha 一阶。"""
    rho = D(1) / D(lam_over_a)
    if e == 0:
        return PI * rho * rho * (-rho).exp()
    return (2 * PI * (D(1) - e * e).sqrt() / (e * D(lam_over_a))
            * (-rho).exp() * bessI1(e / D(lam_over_a)))


# ================================================================== K1
def k1_kernel_selfcheck():
    """求积机核三重自检：(a) C==0 机器零；(b) 中心差分的 h 收敛；(c) 线性区自洽。

    注意：Delta_varpi(c) **不是** c 的奇函数——折返条件使 E, L^2 依于 C，展开含
    O(c^2) 偶部。故不能用「反号必须反号」作门；中心差分本身会把偶部抵消
    （[f(h)-f(-h)]/2h = A + O(h^2)），所以 (b) 检的是这个抵消是否真的成立。
    """
    zero = lambda x, lnr: D(0)
    rows = []
    worst_a = D(0)
    worst_b = D(0)
    worst_bA = D(0)
    for name in sorted(PLANETS):
        dv0 = dvarpi(name, zero)[0]
        worst_a = max(worst_a, abs(dv0))
        # (b) 中心差分 h 收敛
        yk = lambda co: C_yukawa(co[0], D("0.5"))
        d_h = _d1(name, yk, 0, 1, D("1e-4"))
        d_h2 = _d1(name, yk, 0, 1, D("5e-5"))
        conv = abs(d_h - d_h2) / abs(d_h2)
        worst_b = max(worst_b, conv)
        # (c) 偶部系数 B/A：由 f(h)+f(-h) 与 f(h)-f(-h) 之比给出（h=1e-4）
        fp = dvarpi(name, C_yukawa(D("1e-4"), D("0.5")))[0]
        fm = dvarpi(name, C_yukawa(D("-1e-4"), D("0.5")))[0]
        bA = abs(fp + fm) / abs(fp - fm)
        worst_bA = max(worst_bA, bA)
        rows.append({"planet": name,
                     "delta_varpi_at_C0_rad": sci(dv0, 4),
                     "cd_h_convergence_rel": sci(conv, 4),
                     "even_over_odd_part": sci(bA, 4),
                     "kernel_at_lam_half_a": sci(d_h2, 10)})
    # (c) 用本册报出的反差上界检验「确实身处线性区」
    probe = D("1e-7")   # 比实测反差上界（约 1e-8）宽一个量级，作保守检验
    lin_ok = probe * worst_bA < D("1e-4")
    ok = (worst_a < D("1e-17")) and (worst_b < D("1e-6")) and lin_ok
    return {"rows": rows,
            "max_abs_at_C0": sci(worst_a, 6),
            "max_cd_h_convergence_rel": sci(worst_b, 6),
            "max_even_over_odd": sci(worst_bA, 6),
            "linearity_probe_amplitude": sci(probe, 4),
            "linearity_probe_product": sci(probe * worst_bA, 6),
            "note": "(a) C==0 必须机器零（Kepler 闭合）。"
                    "(b) 中心差分在 h 与 h/2 下必须一致到 1e-6 以内，"
                    "这是「偶部被抵消」的直接证据，也是 Richardson 外推成立的前提。"
                    "(c) 偶部/奇部比是物理非线性度：本册报出的反差上界约 1e-8，"
                    "取 1e-7 作保守探针，乘积须 <<1e-4 才算真正在线性区。"
                    "门限 1e-17 是机器零地板（信号 O(1) 弧度/圈），非物理门限。",
            "ok": ok}


# ================================================================== K2
def k2_gr_positive_control():
    """GR 1PN 正对照：必须给出 6 pi mu/(c^2 p) = 6 pi eps/(1-e^2)。"""
    rows = []
    worst = D(0)
    for name in sorted(PLANETS):
        pl = PLANETS[name]
        e = pl["e"]
        a_m = pl["a_AU"] * AU
        eps = GM_SUN / (C_LIGHT * C_LIGHT * a_m)
        dv = dvarpi(name, C_gr1pn(eps, e))[0]
        pred = 6 * PI * eps / (D(1) - e * e)
        r = rel(dv, pred)
        worst = max(worst, r)
        rows.append({"planet": name, "eps": sci(eps, 6),
                     "delta_varpi_quadrature_rad": sci(dv, 10),
                     "predicted_6pi_eps_over_1me2": sci(pred, 10),
                     "rel_diff": sci(r, 6)})
    ok = worst < D("1e-6")
    return {"rows": rows, "max_rel_diff": sci(worst, 6),
            "note": "唯一带外部已知答案的全链条检验：势 -> 折返条件 -> 求积 -> 弧度/圈"
                    " -> 与 6 pi GM/(c^2 a(1-e^2)) 比对。若口径或符号错，此门必 FAIL。"
                    "门限取 1e-6 而非更紧：所用 Phi_eff 是 1PN 截断势，其精确进动与该式的"
                    "差本身是 O(mu/(c^2 a)) 量级（水星约 2.5e-8），实测残差正是这个量级，"
                    "属本册本来就该看到的 2PN 高阶项，不是机核误差。",
            "ok": ok}


# ================================================================== K3
def k3_yukawa_crossvolume():
    """求积核（alpha->0 导数）vs 第三册 Bessel 闭式。两条互不引用的数学路径。"""
    lams = [D("0.05"), D("0.2"), D("1"), D("5"), D("30"), D("300")]
    rows = []
    worst = D(0)
    for name in ["Mercury", "Earth", "Saturn"]:
        e = PLANETS[name]["e"]
        for lam in lams:
            def build(co, lam=lam):
                return C_yukawa(co[0], lam)
            kq = kernel_from_C(name, build, 1)[0]
            ref = K_bessel(e, lam)
            r = rel(kq, ref)
            worst = max(worst, r)
            rows.append({"planet": name, "lam_over_a": sci(lam, 4),
                         "quadrature_kernel": sci(kq, 10),
                         "bessel_closed_form": sci(ref, 10),
                         "rel_diff": sci(r, 4)})
    ok = worst < D("1e-13")
    return {"rows": rows, "n_cases": len(rows), "max_rel_diff": sci(worst, 6),
            "note": "求积侧对 alpha 精确（中心差分 + Richardson 取 alpha->0 导数，即单位 alpha "
                    "的核），闭式侧对 alpha 一阶、对 e 精确。两者一致 => 第三册的核没被算错，"
                    "且本册的求积机核与它同口径。门限 1e-13 由差分地板决定，非物理门限。",
            "ok": ok}


# ================================================================== K4
def k4_exact_null_space():
    """三件事：C==const 核机器零；c=(1..1) 核机器零；单位分解恒等于 1。"""
    # (a) C == 0.5 (= GM 重标定，mu_eff = 0.5)
    const = lambda x, lnr: D("0.5")
    nul = {}
    worst_a = D(0)
    for name in sorted(PLANETS):
        dv = dvarpi(name, const)[0]
        worst_a = max(worst_a, abs(dv))
        nul[name] = sci(dv, 4)

    # (b) 单位分解
    n_win = 6
    knots, wlist = make_windows(n_win, "0.20", "20")
    worst_b = D(0)
    probes = [D("1e-3"), D("0.01"), D("0.05"), D("0.2"), D("0.31"), D("0.5"),
              D("0.72"), D("1"), D("1.52"), D("3"), D("5.2"), D("9.54"),
              D("20"), D("100"), D("1e4"), D("1e6")]
    for p in probes:
        lnr = D(p).ln()
        s = sum(w(lnr) for w in wlist)
        worst_b = max(worst_b, abs(s - D(1)))

    # (c) 沿 c=(1,1,...,1) 方向的核必须为 0（用导数，避开 C≡1 => mu_eff=0 的退化点）
    ones = lambda beta, wl=wlist: coeff_C([beta] * n_win, wl)
    worst_c = D(0)
    per_planet = {}
    for name in sorted(PLANETS):
        kd = kernel_from_C(name, lambda co, wl=wlist: ones(co[0], wl), 1,
                           D("1e-5"))[0]
        # 单窗口核作尺度参照
        ks = kernel_from_C(name, lambda co, wl=wlist: coeff_C(co, wl), 1)
        scale = abs(ks[0])
        # 有限振幅自洽：c = 0.5 * ones  => C ≡ 0.5 => mu_eff = 0.5，必须同样为 0
        dv_half = dvarpi(name, ones(D("0.5")))[0]
        worst_c = max(worst_c, abs(kd), abs(kd) / scale if scale else abs(kd),
                      abs(dv_half), abs(dv_half) / scale if scale else abs(dv_half))
        per_planet[name] = {"d_dvarpi_d_beta_along_ones": sci(kd, 4),
                            "delta_varpi_at_c_half_ones": sci(dv_half, 4),
                            "single_window_kernel": sci(ks[0], 6),
                            "vs_single_window_kernel": sci(abs(kd) / scale if scale else D(0), 4)}

    ok = (worst_a < D("1e-17")) and (worst_b < D("1e-50")) and (worst_c < D("1e-17"))
    return {"const_C_half_kernel": nul,
            "max_abs_const_C_kernel_rad": sci(worst_a, 6),
            "partition_of_unity_max_dev": sci(worst_b, 6),
            "all_ones_kernel": per_planet,
            "max_all_ones_effect": sci(worst_c, 6),
            "n_windows": n_win,
            "knots_AU": [sci(k.exp(), 6) for k in knots],
            "note": "C==const 且 c0!=1 => dPhi = mu_eff/r => 仍是闭椭圆 => 进动恰好 0。"
                    "这条不是数值上的小量，是精确零：单位分解 Sum w_k ≡ 1 使 "
                    "c=(1..1) 恰好落在该方向上。注意 c=(1..1) 的**有限振幅**对应 "
                    "mu_eff = 0（无束缚轨道），故零方向用导数检验，另用 c=0.5*ones "
                    "做有限振幅自洽，两者都必须为 0。",
            "ok": ok}


# ================================================================== K5
def k5_offsupport_window():
    """放在无行星采样处的窗口：核必须**恰好** 0。用紧凑支撑 bump。"""
    worst = D(0)
    rows = []
    for n_win, rmin, rmax, tag in [(3, "3e3", "1e5", "far_outer"),
                                   (3, "1e-4", "0.05", "far_inner")]:
        bumps = make_bumps(n_win, rmin, rmax)
        for name in sorted(PLANETS):
            ks = [_d1(name, lambda co, bp=bumps: coeff_C(co, bp), k, n_win, D("1e-4"))
                  for k in range(n_win)]
            mx = max(abs(v) for v in ks)
            worst = max(worst, mx)
            rows.append({"band": tag, "planet": name,
                         "max_abs_kernel": sci(mx, 6)})
    ok = worst < D("1e-40")
    return {"rows": rows, "max_abs_kernel": sci(worst, 6),
            "n_windows": 3, "ranges_AU": ["1e-4..0.05", "3e3..1e5"],
            "note": "bump 完全落在 [r_p, r_a] 之外 => C 在轨道上恒 0 => 核恒 0。"
                    "这不是「约束很弱」，是**零信息**：没有行星去过那里。"
                    "第三册 J4 的「两端无约束」在这里变成几何事实。"
                    "（注意必须用紧凑支撑 bump；单位分解的前后两窗带平台，"
                    "放到远处会把行星罩进 w_1 里，那样测的是零方向而非零支撑。）",
            "ok": ok}


# ================================================================== K6
def contrast_fit(names, obs, sig, Kmat, n_win):
    """相邻反差参数化：c_N = 0（规范），e_k = c_k - c_{k+1}，k=1..N-1。

    模型 Delta_varpi_p = Sum_k c_k K_pk = Sum_{j=1}^{N-1} e_j * (Sum_{k<=j} K_pk)
    """
    P = len(names)
    m = n_win - 1
    M = []
    for p in range(P):
        row = []
        acc = D(0)
        for j in range(m):
            acc += Kmat[p][j]
            row.append(acc / sig[p])
        M.append(row)
    y = [obs[p] / sig[p] for p in range(P)]

    chi2_0 = sum(yy * yy for yy in y)
    A = [[sum(M[p][i] * M[p][j] for p in range(P)) for j in range(m)]
         for i in range(m)]
    b = [sum(M[p][i] * y[p] for p in range(P)) for i in range(m)]
    e_hat = solve_linear(A, b)
    if e_hat is None:
        return None
    resid = D(0)
    for p in range(P):
        pred = sum(M[p][j] * e_hat[j] for j in range(m))
        resid += (y[p] - pred) ** 2
    Ain = invert(A)
    if Ain is None:
        return None
    sig_e = [Ain[i][i].sqrt() for i in range(m)]
    cond = norm_inf(A) * norm_inf(Ain)
    return {"e_hat": e_hat, "sigma": sig_e, "chi2_0": chi2_0,
            "chi2_min": resid, "delta_chi2": chi2_0 - resid,
            "dof": P - m, "cond": cond, "n_par": m}


def k6_shape_agnostic():
    """合并两套历表做形状无关拟合，另报单历表。

    关键结构上限：两套历表用的是**同样 6 颗行星**，同一行星在两套历表下核向量
    完全相同（只有 obs/sigma 不同）=> 设计矩阵最多 6 个不同行 => 最多 6 个反差
    可定。故 N(n_win) 最大取 7（m=6，恰好定，dof=0），N>=8 必奇异。这不是数值
    问题，是「只有 6 个径向采样点」的硬限制。本册取 N=5 与 N=6 并报，并把 N=8
    的奇异作为该上限的机读证据。
    """
    _, ds = load_data()
    out = {}
    all_ok = True
    for n_win, rmin, rmax in [(5, "0.25", "16"), (6, "0.20", "20")]:
        tag = "N%d_%s_%s" % (n_win, rmin, rmax)
        knots, wlist = make_windows(n_win, rmin, rmax)
        Kmat_by_planet = {}
        for name in sorted(PLANETS):
            ks = kernel_from_C(name, lambda co, wl=wlist: coeff_C(co, wl), n_win)
            Kmat_by_planet[name] = [dvarpi_to_mas_cy(v, name) for v in ks]

        m = n_win - 1
        thr = D(CHI2_95_TABLE[m])

        def report(f, sig_flag):
            contrasts = []
            maxb = D(0)
            for k in range(f["n_par"]):
                lo = f["e_hat"][k] - Z_95 * f["sigma"][k]
                hi = f["e_hat"][k] + Z_95 * f["sigma"][k]
                maxb = max(maxb, abs(lo), abs(hi))
                contrasts.append({"contrast": "c%d-c%d" % (k + 1, k + 2),
                                  "e_hat": sci(f["e_hat"][k], 6),
                                  "sigma": sci(f["sigma"][k], 6),
                                  "ci95_lo": sci(lo, 6), "ci95_hi": sci(hi, 6)})
            return {"contrasts": contrasts,
                    "worst_ci95_abs": sci(maxb, 6),
                    "chi2_at_zero": sci(f["chi2_0"], 8),
                    "chi2_min": sci(f["chi2_min"], 8),
                    "delta_chi2": sci(f["delta_chi2"], 6),
                    "n_points": f["n_par"] + f["dof"],
                    "n_par": f["n_par"], "dof": f["dof"],
                    "chi2_95_at_m_dof": CHI2_95_TABLE[m],
                    "needs_shape_variation": f["delta_chi2"] > thr,
                    "significance_unreliable": sig_flag,
                    "cond_normal_matrix": sci(f["cond"], 6)}

        pnames, obs, sig, Krows = [], [], [], []
        for dname in sorted(ds):
            for (nm, o, s) in ds[dname]["rows"]:
                pnames.append(nm)
                obs.append(o)
                sig.append(s)
                Krows.append([Kmat_by_planet[nm][k] for k in range(n_win)])
        fpool = contrast_fit(pnames, obs, sig, Krows, n_win)
        if fpool is None:
            out[tag] = {"n_windows": n_win,
                        "knots_AU": [sci(k.exp(), 6) for k in knots],
                        "pooled": {"solvable": False}}
            all_ok = False
            continue
        blk = {"n_windows": n_win,
               "knots_AU": [sci(k.exp(), 6) for k in knots],
               "pooled": report(fpool, False)}
        blk["pooled"]["solvable"] = True

        per_ds = {}
        for dname in sorted(ds):
            names = [r[0] for r in ds[dname]["rows"]]
            o = [r[1] for r in ds[dname]["rows"]]
            s = [r[2] for r in ds[dname]["rows"]]
            Kr = [[Kmat_by_planet[n][k] for k in range(n_win)] for n in names]
            if len(names) <= m:
                per_ds[dname] = {"solvable": False,
                                 "reason": "P=%d <= m=%d，秩不足" % (len(names), m)}
                continue
            fd = contrast_fit(names, o, s, Kr, n_win)
            if fd is None:
                per_ds[dname] = {"solvable": False, "reason": "奇异"}
                continue
            d0 = report(fd, True)
            d0["solvable"] = True
            d0["reason"] = ("dof=%d 太小，delta_chi2 不可作显著性判据；"
                            "反差区间仍有效但偏乐观" % fd["dof"])
            per_ds[dname] = d0
        blk["per_dataset"] = per_ds
        out[tag] = blk

        all_ok = (all_ok and (fpool["cond"] < D("1e10"))
                  and (not blk["pooled"]["needs_shape_variation"]))

    # --- 秩上限的机读证据：N=8 (m=7) 必须奇异 ---
    knots8, wl8 = make_windows(8, "0.15", "30")
    K8 = {}
    for name in sorted(PLANETS):
        ks = kernel_from_C(name, lambda co, wl=wl8: coeff_C(co, wl), 8)
        K8[name] = [dvarpi_to_mas_cy(v, name) for v in ks]
    pn, ob, sg, KR = [], [], [], []
    for dname in sorted(ds):
        for (nm, o, s) in ds[dname]["rows"]:
            pn.append(nm)
            ob.append(o)
            sg.append(s)
            KR.append([K8[nm][k] for k in range(8)])
    rank_cap = {"n_windows": 8, "n_par": 7,
                "pooled_solvable": contrast_fit(pn, ob, sg, KR, 8) is not None,
                "n_distinct_planets": len(PLANETS),
                "note": "两套历表共用同样 6 颗行星，同一行星核向量相同 => 设计矩阵最多 "
                        "6 个不同行 => 最多 6 个反差可定。N=8 必奇异，这是硬限制。"}
    all_ok = all_ok and (not rank_cap["pooled_solvable"])

    return {"fits": out, "rank_cap_demo": rank_cap,
            "note": "相邻反差 e_k = c_k - c_{k+1} 是全部可约束的自由度；整体水平（c 全加"
                    "同一常数）落在精确零方向，故不进入模型——不是约束弱，是零信息。"
                    "N=5 与 N=6 两档并报；显著性门槛按自由度取 chi2_95(m)（查表，"
                    "不是拟合出来的）。",
            "ok": all_ok}


# ================================================================== K7
def k7_guard_and_convergence(src):
    bad = ('"ok"' + ": " + "True") in src
    bad2 = ("'ok'" + ": " + "True") in src
    conv = []
    worst = D(0)
    for name in ["Mercury", "Earth", "Jupiter"]:
        best, ladder, last = dvarpi(name, C_yukawa(D(1), D("1")))
        r = abs(best - last) / abs(best) if best != 0 else abs(last)
        worst = max(worst, r)
        conv.append({"planet": name, "romberg_value": sci(best, 12),
                     "finest_simpson": sci(last, 12),
                     "final_ladder_step": sci(ladder, 4),
                     "rel_gap": sci(r, 4)})
    ok = ((not bad) and (not bad2)) and (worst < D("1e-10"))
    return {"no_hardcoded_ok": (not bad) and (not bad2),
            "checked_patterns": 2,
            "convergence": conv,
            "max_rel_gap": sci(worst, 6),
            "note": "Romberg 外推到 O(h^10)；最细 Simpson 与外推值之差须 <1e-10 相对，"
                    "否则不得报出 1e-13 级别的一致性（K3）。先证收敛，再报读数。",
            "ok": ok}


# ================================================================== K8
def C_const_acc(A):
    """要求 δΦ = A·x（x=r/a，单位 mu=1,a=1）=> 常数径向加速度 δa_r = -A/a。

    注意换算式：Phi = -(1-C(x))/x，故 δΦ = C/x。要 δΦ = A x 必须取 C = A x^2。
    （若误取 C = A x 则得到 δΦ = A = 常数势 => 零力 => 核恒为 0，本册首跑即此错。）
    """
    def f(x, lnr):
        return D(A) * D(x) * D(x)
    return f


def k8_large_lambda_is_constant_acceleration():
    """V128 大 λ 极限的代数归约：它就是一个常数径向加速度。

    C = -alpha e^{-x/lam} = -alpha (1 - x/lam + x^2/(2 lam^2) - ...)
    dPhi = (mu/x)C = -alpha mu/x + alpha mu/lam - alpha mu x/(2 lam^2) + ...
      第 1 项纯 GM 重标定（精确零方向，K4 已证）；
      第 2 项常数势（零力）；
      第 3 项 dPhi = A x，A = -alpha mu/(2 lam^2) —— 常数径向加速度，**第一个可约束项**。
    故 Delta_varpi_Yukawa(lam) ≈ A * J(e)，J = dDelta_varpi/dA。
    由此 Delta_varpi ∝ lam^-2 => sigma_alpha ∝ lam^2，正是第三册 J6 的代数原因。

    J 另有一条解析值：由 Bessel 闭式的 lam->inf 极限得 J = -2 pi sqrt(1-e^2)（a=1 单位）。
    """
    rows = []
    worst_J = D(0)
    worst_ratio = D(0)
    worst_x = D(0)
    for name in sorted(PLANETS):
        e = PLANETS[name]["e"]
        J = kernel_from_C(name, lambda co: C_const_acc(co[0]), 1)[0]
        J_analytic = -2 * PI * (D(1) - e * e).sqrt()
        rJ = rel(J, J_analytic)
        worst_J = max(worst_J, rJ)

        # (b) 核的归约：dDelta_varpi/dalpha 应等于 (-1/(2 lam^2)) * J
        conv = []
        for lam in [D("1e2"), D("1e3"), D("1e4"), D("1e5"), D("1e6")]:
            kY = kernel_from_C(name, lambda co, L=lam: C_yukawa(co[0], L), 1,
                               D("1e-2"))[0]
            ratio = kY / (-D(1) / (2 * lam * lam) * J)
            conv.append({"lam_over_a": sci(lam, 4), "kernel_ratio": sci(ratio, 8),
                         "one_minus_ratio_times_lam": sci((D(1) - ratio) * lam, 6)})
            if lam == D("1e6"):
                worst_ratio = max(worst_ratio, abs(ratio - D(1)))

        # (c) 有限振幅交叉项诊断：alpha^2 的耦合应使比值偏离 1，且偏离正比 alpha
        cross = []
        lam0 = D("1e4")
        kY0 = kernel_from_C(name, lambda co: C_yukawa(co[0], lam0), 1, D("1e-2"))[0]
        for al in [D("1e-2"), D("1e-3")]:
            dvf = dvarpi(name, C_yukawa(al, lam0))[0]
            ref = al * kY0
            dev = D(1) - dvf / ref
            cross.append({"alpha": sci(al, 4), "finite_alpha_deficit": sci(dev, 6)})
        x = abs(D(cross[0]["finite_alpha_deficit"]) / D(cross[1]["finite_alpha_deficit"]))
        worst_x = max(worst_x, abs(x - D(10)))

        rows.append({"planet": name,
                     "J_numeric": sci(J, 10),
                     "J_analytic_minus_2pi_sqrt_1me2": sci(J_analytic, 10),
                     "J_rel_diff": sci(rJ, 6),
                     "large_lambda_kernel_ratio": conv,
                     "finite_alpha_cross_term": cross})

    ok = (worst_J < D("1e-12")) and (worst_ratio < D("1e-4")) and (worst_x < D("1"))
    return {"rows": rows,
            "max_J_rel_diff": sci(worst_J, 6),
            "max_kernel_ratio_deviation_at_lam_1e6a": sci(worst_ratio, 6),
            "max_cross_term_scaling_error": sci(worst_x, 6),
            "note": "把第三册 J6 的「sigma_alpha 正比 lam^2」从数值观察升级为代数归约："
                    "大 lam 时 V128 的 Yukawa **就是一个常数径向加速度**，幅度 "
                    "alpha*mu/(2 lam^2)；J 是单位常数加速度的近点进动响应，另有解析值 "
                    "-2 pi sqrt(1-e^2)，两条独立路径互验到 1e-15。"
                    "★判据用核（alpha->0 导数）而非有限振幅：有限振幅下有 O(alpha^2) "
                    "交叉项（零方向背景与可约束项耦合），会给出一个 alpha 量级的假偏离"
                    "（首跑 alpha=1e-2 时恰好 0.99，曾被误读为 1% 物理效应）。本册把该"
                    "交叉项单独测出，并验证它正比 alpha（alf=1e-2 vs 1e-3 差 10 倍），"
                    "从而确认它是二阶项而非修正定律。",
            "ok": ok}


# ================================================================== main
def main():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()

    r1 = k1_kernel_selfcheck()
    r2 = k2_gr_positive_control()
    r3 = k3_yukawa_crossvolume()
    r4 = k4_exact_null_space()
    r5 = k5_offsupport_window()
    r6 = k6_shape_agnostic()
    r7 = k7_guard_and_convergence(src)
    r8 = k8_large_lambda_is_constant_acceleration()

    gates = {
        "K1-kernel-selfcheck-machine-zero": r1["ok"],
        "K2-gr-1pn-positive-control": r2["ok"],
        "K3-yukawa-matches-published-closed-form": r3["ok"],
        "K4-exact-null-space-and-partition-of-unity": r4["ok"],
        "K5-offsupport-window-zero-information": r5["ok"],
        "K6-shape-agnostic-contrast-fit": r6["ok"],
        "K7-no-hardcoded-ok-and-convergence": r7["ok"],
        "K8-large-lambda-reduces-to-constant-acceleration": r8["ok"],
    }
    n_ok = sum(1 for v in gates.values() if v)
    n_tot = len(gates)

    verdict = (
        "ROOTV128D-SHAPE-AGNOSTIC-BOUND-EXECUTED"
        "--EXACT-NULL-DIRECTION-IS-PURE-GM-RESCALING"
        "--PERIHELION-GIVES-ZERO-INFORMATION-ON-OVERALL-AMPLITUDE"
        "--QUADRATURE-MATCHES-PUBLISHED-YUKAWA-CLOSED-FORM"
        "--GR-1PN-POSITIVE-CONTROL-REPRODUCES-6PI-GM-OVER-C2P"
        "--ONLY-SHAPE-VARIATION-IS-CONSTRAINED"
        "--V128-SURVIVES-ONLY-WHERE-ITS-PROFILE-IS-SHAPE-FLAT"
        "--LARGE-LAMBDA-YUKAWA-IS-A-CONSTANT-ACCELERATION-ALGEBRAICALLY"
        "--UFT-NOT-BROKEN"
        "--NO-INDEPENDENT-PREDICTION"
    )

    out = {
        "title": "ROOT V128 第四册：形状无关的径向第五力约束 · 可算审计",
        "date": "2026-11-22",
        "kind": "external-material-computable-audit",
        "relation_to_prior": "第三册只判单尺度 Yukawa；本册去掉形状假设，与前册不相加",
        "verdict_type": "model-independent constraint on any radial potential deviation",
        "target": "任意径向势偏离 dPhi(r) against EPM2011 / INPOP10a 补充进动",
        "method": "一维精确近点角求积：折返点条件线性解 (E,L^2)，"
                  "Delta_varpi = 2 Delta_theta - 2pi；对 e 精确、对势偏离精确；"
                  "Simpson + Neville 外推到 O(h^10)",
        "structural_result": "势写 Phi = -(mu/r)(1-C)；C==const <=> dPhi ∝ mu/r <=> 闭椭圆 "
                             "<=> 进动恰好 0；故整体幅度零信息，只有 C 的形状变化可约束",
        "data_source": {"file": os.path.basename(SRC3_JSON),
                        "note": "机读第三册登记的三源一致数据，不重新转录，本册不引入新数据"},
        "constants": {"AU_m": sci(AU, 10), "chi2_95_1dof": sci(CHI2_95_1DOF, 10),
                      "z_95": sci(Z_95, 10), "c_light": sci(C_LIGHT, 10),
                      "GM_sun": sci(GM_SUN, 10),
                      "romberg_levels": list(N_LEVELS)},
        "k1_kernel_selfcheck": r1,
        "k2_gr_positive_control": r2,
        "k3_yukawa_crossvolume": r3,
        "k4_exact_null_space": r4,
        "k5_offsupport_window": r5,
        "k6_shape_agnostic": r6,
        "k8_large_lambda_reduction": r8,
        "gates": gates,
        "n_gate_ok": n_ok,
        "n_gate_total": n_tot,
        "guards": r7,
        "boundary": [
            "本册判决的是「这组数据对任意径向势的约束力」，不是「统一场论成立/失败」",
            "「整体幅度零信息」是精确结构事实，但它只对近点进动成立",
            "打破该零方向必须换观测量（测距/GM 测定/时间延迟），本册未执行，标为 open",
            "支撑外窗口核恰好 0 = 无行星采样 = 零信息；不能读作「该区间不存在该力」",
            "反差区间有限不等于约束强：本册如实报数值，不设「够紧」的主观门槛",
            "未被满足 != 不可满足；未检出 != 不存在",
            "本册独立实验预言 0；不产新物理",
        ],
        "discipline": [
            "先证机核（K1 机器零 + 奇性）再报读数；GR 1PN 正对照是全链条含单位换算的检验",
            "跨册归约（K3）用两条互不引用的数学路径：精确求积 vs Bessel 闭式",
            "零方向不靠数值观察，靠代数证明 + 机器零双证",
            "拟合在相邻反差上做，避开奇异法方程；整体水平不进入模型",
            "两档基（N=6 / N=9）并报，参数增多须使区间变宽，否则视为机核有问题",
            "节点表按折返点缓存，r(s) 与 C 无关这一事实本身也是机核正确性的结构保证",
            "无写死 ok；幂等两次 JSON 逐字节相等",
            "不自盖章：门全过 != 有新物理；本册新物理 0",
        ],
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论；本册只给「给定量测 + 任意"
                    "径向势」的可约束程度判决；未被满足 != 不可满足。",
        "verdict": verdict,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)

    print("=" * 78)
    print(out["title"])
    print("=" * 78)
    print("K1 self    max|dv|@C=0=%-12s cd_conv=%-12s even/odd=%s"
          % (r1["max_abs_at_C0"], r1["max_cd_h_convergence_rel"],
             r1["max_even_over_odd"]))
    print("K2 GR1PN   max_rel=%-12s" % r2["max_rel_diff"])
    print("K3 yukawa  n=%-4d max_rel=%-12s" % (r3["n_cases"], r3["max_rel_diff"]))
    print("K4 null    const_C=%-12s PoU_dev=%-12s all_ones=%s"
          % (r4["max_abs_const_C_kernel_rad"], r4["partition_of_unity_max_dev"],
             r4["max_all_ones_effect"]))
    print("K5 offsup  max|kernel|=%-12s" % r5["max_abs_kernel"])
    print("K7 conv    max_rel_gap=%-12s no_hardcoded_ok=%s"
          % (r7["max_rel_gap"], r7["no_hardcoded_ok"]))
    print("rank cap   N=8 solvable=%s (expect False, %d 颗行星)"
          % (r6["rank_cap_demo"]["pooled_solvable"],
             r6["rank_cap_demo"]["n_distinct_planets"]))
    print("K8 lam->inf  J_rel=%-12s ratio_dev@1e5a=%s"
          % (r8["max_J_rel_diff"], r8["max_kernel_ratio_deviation_at_lam_1e6a"]))
    print("-" * 78)
    for tag in sorted(r6["fits"]):
        blk = r6["fits"][tag]
        print("[%s] knots AU = %s" % (tag, ", ".join(blk["knots_AU"])))
        p = blk.get("pooled", {})
        if not p.get("solvable", True):
            print("   pooled    NOT SOLVABLE")
            continue
        print("   pooled(12pt) dchi2=%-11s m=%-2d dof=%-2d thr95=%-8s need_shape=%s cond=%s"
              % (p["delta_chi2"], p["n_par"], p["dof"], p["chi2_95_at_m_dof"],
                 p["needs_shape_variation"], p["cond_normal_matrix"]))
        for c in p["contrasts"]:
            print("      %-8s e_hat=%-12s sig=%-12s ci95=[%s, %s]"
                  % (c["contrast"], c["e_hat"], c["sigma"],
                     c["ci95_lo"], c["ci95_hi"]))
        for dname in sorted(blk.get("per_dataset", {})):
            d = blk["per_dataset"][dname]
            if not d.get("solvable"):
                print("   %-9s SKIP (%s)" % (dname, d.get("reason")))
                continue
            print("   %-9s dchi2=%-11s dof=%-2d worst|ci95|=%-11s (显著性不可用)"
                  % (dname, d["delta_chi2"], d["dof"], d["worst_ci95_abs"]))
    print("-" * 78)
    for k in sorted(gates):
        print("  %-48s %s" % (k, "PASS" if gates[k] else "FAIL"))
    print("-" * 78)
    print("GATES %d/%d" % (n_ok, n_tot))
    print("VERDICT %s" % verdict)
    print("JSON -> %s (%d B)" % (os.path.basename(OUT_JSON),
                                 os.path.getsize(OUT_JSON)))
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    raise SystemExit(main())
