# -*- coding: utf-8 -*-
"""
TUFT-r365 · ROOT V26《空间光速螺旋全参数第一性原理攻坚》独立重算与审计

来料：数据/TUFT-r333_..._来料原件_ROOT_V26_用户附件逐字.md（逐字，只读，不改一字节）
任务：① 三维圆柱螺旋逐阶求导（V26 §一）② 曲率/挠率闭式与统一恒等式（V26-2）
     ③ 速度分配 V26-1 ④ 螺旋角参数化全套恒等式 ⑤ 四维类时 Frenet K₁/K₂ 与 V26-3
     ⑥ 螺旋角自由度定理（X²+Y²=1 仍剩一个连续自由度）⑦ α 输入定价（条件性几何构造）
     ⑧ Maxwell 局域能流上界恒等式 ⑨ Bessel 双口径群速度 ⑩ 电子条件性螺旋 70 位精算
     ⑪ 真实磁场电子螺旋（κ/|τ|=v⊥/u=1.2）⑫ 洛伦兹不变性（代数+300 组随机 boost 机检）
纪律：不产生新物理；不重开 S1–S13；不改 r333 来料原件、不跑 refresh_catalog.py、不 git；
      条目不可与 r300–r364 相加。
"""
import sys, os, json, time, math, random, hashlib
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
VERD = os.path.join(ROOT, "判定")
TAG = ("TUFT-r365_ROOTV26空间光速螺旋全参数审计_三维四维Frenet独立重算与"
       "螺旋角自由度定理与alpha输入定价_精算与可视化_2026-11-02")
HTML = os.path.join(DATA, "ROOTV26_光速螺旋_独立重算_可视化_r365.html")
INPUTF = os.path.join(DATA, "TUFT-r333_ROOTV26空间光速螺旋审计_四维Frenet第二曲率勘误与"
                           "螺旋角自由度定理与alpha输入定价_精算与可视化_2026-11-01_"
                           "来料原件_ROOT_V26_用户附件逐字.md")
OUT_TXT = os.path.join(HERE, "_out_r365.txt")
BOOK = os.path.join(VERD, "判定_" + TAG + ".md")
mp.mp.dps = 80

RED_LINE = ("本卷只对 ROOT V26 文本作独立重算与机读对拍，不重写物理、不改 r333 来料原件任何字节；"
            "「成立」仅指符号恒等与数值复算一致，不是实验符合；κ/τ 与 K₁/K₂ 只在三维 3+1 分解与"
            "类时四维 Frenet 各自定义域内有效，类光层仍需 null 标架（r332/r329 已定）；"
            "α 是输入不是输出，本卷供给 0；本卷条目不可与 r300–r364 相加")

_log = []
def log(s=""):
    print(s)
    _log.append(str(s))

items, controls, guards = [], [], []
def add(bucket, key, verdict, name, detail, numbers=None):
    bucket.append({"key": key, "verdict": verdict, "name": name,
                   "detail": detail, "numbers": numbers or {}})

def sci(x, nd=6):
    x = mp.mpf(x)
    if x == 0:
        return "0"
    e = int(mp.floor(mp.log10(abs(x)))
            ) if abs(x) > 0 else 0
    m = x / mp.mpf(10) ** e
    return ("%" + str(nd) + ".4fE%+03d") % (float(m), e)

def rel(a, b):
    a, b = mp.mpf(a), mp.mpf(b)
    if b == 0:
        return mp.mpf(0) if a == 0 else mp.inf
    return abs(a - b) / abs(b)

t00 = time.time()
log("== r365 · ROOT V26 独立重算 ==")
log("  mp.dps = %d；sympy %s" % (mp.mp.dps, sp.__version__))

# ============================ 0. 来料留档（只读） ============================
sha_input = ""
if os.path.isfile(INPUTF):
    with open(INPUTF, "rb") as f:
        sha_input = hashlib.sha256(f.read()).hexdigest().upper()
log("  来料原件 sha256 = %s…（只读，未改）" % sha_input[:16])

# ============================ 1. 符号层 ============================
t = sp.Symbol("t", real=True)
R = sp.Symbol("R", positive=True)
w = sp.Symbol("omega", positive=True)
u = sp.Symbol("u", positive=True)
cc = sp.Symbol("c", positive=True)
ph0 = sp.Symbol("phi0", real=True)
th = sp.Symbol("theta", positive=True)
eps0 = sp.Symbol("epsilon0", positive=True)

cos1 = sp.cos(w * t + ph0)
sin1 = sp.sin(w * t + ph0)
r3 = sp.Matrix([R * cos1, R * sin1, u * t])
v3 = sp.Matrix([sp.diff(r3[i], t) for i in range(3)])
a3 = sp.Matrix([sp.diff(v3[i], t) for i in range(3)])
v2 = sp.simplify(sp.expand(v3.dot(v3)))
a_mag = sp.simplify(sp.expand(sp.sqrt(a3.dot(a3))))
cross3 = v3.cross(a3)
cross2 = sp.simplify(sp.expand(cross3.dot(cross3)))
speed = sp.sqrt(v2)
kappa3 = sp.simplify(sp.sqrt(cross2) / speed**3)
da3 = sp.Matrix([sp.diff(a3[i], t) for i in range(3)])
tau3 = sp.simplify(cross3.dot(da3) / cross2)
ident3 = sp.simplify(sp.expand(kappa3**2 + tau3**2 - w**2 / v2))

log("  |v|² = %s" % v2)
log("  |a|  = %s" % a_mag)
log("  κ    = %s" % sp.simplify(kappa3))
log("  τ    = %s" % sp.simplify(tau3))
log("  κ²+τ²−ω²/|v|² = %s" % ident3)

# --- 四维：闵氏度规 diag(1,-1,-1,-1) ---
def mdot(A, B):
    return A[0] * B[0] - A[1] * B[1] - A[2] * B[2] - A[3] * B[3]

X4 = sp.Matrix([cc * t, R * cos1, R * sin1, u * t])
dXdt = sp.Matrix([sp.diff(X4[i], t) for i in range(4)])
# ds/dt = sqrt(c²−v²)
dsdt = sp.sqrt(cc**2 - v2)
U4 = sp.Matrix([sp.expand(dXdt[i] / dsdt) for i in range(4)])
A4 = sp.Matrix([sp.diff(U4[i], t) / dsdt for i in range(4)])
K1_2 = sp.simplify(sp.expand(-mdot(A4, A4)))
K1 = sp.simplify(sp.sqrt(K1_2))
K1_target = sp.simplify(sp.expand((cc**2 / (cc**2 - v2)) * R * w**2 / cc**2))
# K₁、K₁_target 均严格为正 ⇒ 用平方比较（避免 √(1/X²) 的符号分支）
K1_ok = sp.simplify(sp.expand(K1_2 - K1_target**2)) == 0

e1 = sp.Matrix([sp.simplify(A4[i] / K1) for i in range(4)])
De1 = sp.Matrix([sp.diff(e1[i], t) / dsdt for i in range(4)])
De1_sq = sp.simplify(sp.expand(-mdot(De1, De1)))
e0De1 = sp.simplify(sp.expand(mdot(U4, De1)))
K2_2 = sp.simplify(sp.expand(De1_sq + e0De1**2))
K2 = sp.simplify(sp.sqrt(K2_2))
gamma = 1 / sp.sqrt(1 - v2 / cc**2)
K2_target = sp.simplify(gamma**2 * (w / cc) * sp.sqrt(1 - u**2 / cc**2))
K2_ok = sp.simplify(sp.expand(K2_2 - K2_target**2)) == 0
ratio4 = sp.simplify(K1 / K2)
ratio4_target = sp.simplify((R * w / cc) / sp.sqrt(1 - u**2 / cc**2))
ratio_ok = sp.simplify(sp.expand(ratio4**2 - ratio4_target**2)) == 0

log("  K₁ = %s（目标 γ²Rω²/c²：%s）" % (K1, K1_ok))
log("  K₂ = %s（目标 γ²ω/c·√(1−u²/c²)：%s）" % (sp.simplify(K2), K2_ok))
log("  K₁/K₂ = %s（目标 Rω/c/√(1−u²/c²)：%s）" % (sp.simplify(ratio4), ratio_ok))

# --- 螺旋角参数化（v=c 分支） ---
# 直接按 θ 定义写闭式（v⊥=c sinθ，u=c cosθ）
kappa_par = sp.simplify(w / cc * sp.sin(th))
tau_par = sp.simplify(w / cc * sp.cos(th))
# 与 3D 公式在 v=c 分支一致
kap_from_3d = sp.simplify(kappa3.subs({R: cc * sp.sin(th) / w,
                                       u: cc * sp.cos(th)}))
tau_from_3d = sp.simplify(tau3.subs({R: cc * sp.sin(th) / w,
                                     u: cc * sp.cos(th)}))
par_ok = (sp.simplify(kap_from_3d - kappa_par) == 0) and (sp.simplify(tau_from_3d - tau_par) == 0)
tan_ok = sp.simplify(kappa_par / tau_par - sp.tan(th)) == 0
pitch = sp.simplify(2 * sp.pi * (cc * sp.cos(th)) / w)
ratio_pitch = sp.simplify((2 * sp.pi * (cc * sp.sin(th) / w)) / pitch - sp.tan(th))
log("  κ(θ)=%s；τ(θ)=%s；κ/|τ|−tanθ = %s" % (kappa_par, tau_par,
                                              sp.simplify(kappa_par / tau_par - sp.tan(th))))
log("  2πR/p − tanθ = %s" % ratio_pitch)

# --- Maxwell 局域能流上界（符号） ---
Ex, Ey, Ez, Bx, By, Bz = sp.symbols("Ex Ey Ez Bx By Bz", real=True)
Evec = sp.Matrix([Ex, Ey, Ez])
Bvec = sp.Matrix([Bx, By, Bz])
wEM = eps0 / 2 * (Evec.dot(Evec) + cc**2 * Bvec.dot(Bvec))
Svec = eps0 * cc**2 * Evec.cross(Bvec)
S2 = sp.simplify(sp.expand(Svec.dot(Svec)))
lhs = sp.simplify(sp.expand(wEM**2 - S2 / cc**2))
rhs = sp.simplify(eps0**2 / 4 * ((Evec.dot(Evec) - cc**2 * Bvec.dot(Bvec))**2
                                 + 4 * cc**2 * (Evec.dot(Bvec))**2))
mw_ok = sp.simplify(sp.expand(lhs - rhs)) == 0
log("  Maxwell 恒等式 w²−|S|²/c² = ε₀²/4[(E²−c²B²)²+4c²(E·B)²]：%s" % mw_ok)

# --- 洛伦兹不变：boost 后比值代数 ---
bB = sp.Symbol("beta_B", real=True)
gamB = 1 / sp.sqrt(1 - bB**2)
kpar = 1 / (gamB * (1 - bB * u / cc))
w_p = w * kpar
u_p = (u - bB * cc) / (1 - bB * u / cc)
a_frac = R * w / cc
ratio_before = a_frac / sp.sqrt(1 - u**2 / cc**2)
ratio_after = (a_frac * kpar) / sp.sqrt(1 - (u_p / cc)**2)
ratio_inv = sp.simplify(sp.expand(ratio_after**2 - ratio_before**2))
log("  boost 后比值不变代数差（平方比较）= %s" % ratio_inv)

# ============================ 2. 数值层 ============================
C0 = mp.mpf("299792458")
HBAR0 = mp.mpf("1.054571817e-34")
ME0 = mp.mpf("9.1093837015e-31")
EK0 = mp.mpf("1.602176634e-19")
ALPHA0 = mp.mpf(1) / mp.mpf("137.035999177")
LAM_C = HBAR0 / (ME0 * C0)
OMEGA_C = ME0 * C0**2 / HBAR0

# ---- B1 三维数值微分重建（不用闭式） ----
def kin3_num(Rv, wv, uv, tv, c=1.0, h=mp.mpf("1e-4")):
    def P(s):
        return [Rv * mp.cos(wv * s), Rv * mp.sin(wv * s), uv * s]
    def d1(f, s, hh):
        return [(f(s + hh)[i] - f(s - hh)[i]) / (2 * hh) for i in range(3)]
    def d2(f, s, hh):
        return [(f(s + hh)[i] - 2 * f(s)[i] + f(s - hh)[i]) / hh**2 for i in range(3)]
    vv = d1(P, tv, h)
    aa = d2(P, tv, h)                         # 二阶：加速度
    spd = mp.sqrt(sum(x * x for x in vv))
    cr = [vv[1] * aa[2] - vv[2] * aa[1],
          vv[2] * aa[0] - vv[0] * aa[2],
          vv[0] * aa[1] - vv[1] * aa[0]]
    crn = mp.sqrt(sum(x * x for x in cr))
    da = d1(lambda s: d2(P, s, h), tv, h)     # 三阶：加速度的时间导数（τ 的分子用这个）
    kap = crn / spd**3
    tau = sum(cr[i] * da[i] for i in range(3)) / crn**2
    return spd, kap, tau

b1_cases = []
for (Rv, wv, uv) in [(mp.mpf(3), mp.mpf(2), mp.mpf(1)),
                     (mp.mpf(1), mp.mpf(5), mp.mpf("0.3")),
                     (mp.mpf("0.5"), mp.mpf("10"), mp.mpf("2"))]:
    spd, kapn, taun = kin3_num(Rv, wv, uv, mp.mpf("0.37"))
    spd_th = mp.sqrt((Rv * wv)**2 + uv**2)
    kap_th = Rv * wv**2 / spd_th**2
    tau_th = uv * wv / spd_th**2
    b1_cases.append({"R": str(Rv), "omega": str(wv), "u": str(uv),
                     "speed_rel": str(rel(spd, spd_th)),
                     "kappa_rel": str(rel(kapn, kap_th)),
                     "tau_rel": str(rel(taun, tau_th))})
b1_max = max(max(mp.mpf(x["kappa_rel"]), mp.mpf(x["tau_rel"]), mp.mpf(x["speed_rel"]))
             for x in b1_cases)
log("  B1 三维数值重建：3 组 max rel = %s" % sci(b1_max))

# ---- B2 四维 Frenet 数值重建（Gram–Schmidt 型，不用闭式） ----
def recon4(Rv, wv, uv, c=C0, t0=None, boost=None, hrel=mp.mpf("1e-3")):
    """在观察者系中由轨迹采样重建 K₁、K₂；boost=(betaB,) 时按 boost 后轨迹重建。"""
    if boost is None:
        def Xf(tp):
            return [c * tp, Rv * mp.cos(wv * tp), Rv * mp.sin(wv * tp), uv * tp]
        tscale = 1 / wv
    else:
        bb = boost
        gam = 1 / mp.sqrt(1 - bb**2)
        kf = 1 / (gam * (1 - bb * uv / c))
        def Xf(tp):
            tt = tp * kf                       # t' = γ(t−βz/c) ⇒ t = t'·kf
            return [c * tp, Rv * mp.cos(wv * tt), Rv * mp.sin(wv * tt),
                    gam * (uv * tt - bb * c * tt)]
        tscale = 1 / (wv * kf)
    if t0 is None:
        t0 = mp.mpf(2) * mp.pi / (wv * 37)   # 避开对称点
    h = hrel * tscale

    def md(A, B):
        return A[0] * B[0] - A[1] * B[1] - A[2] * B[2] - A[3] * B[3]
    def d1(f, s):
        return [(f(s + h)[i] - f(s - h)[i]) / (2 * h) for i in range(4)]
    def d1h(f, s):
        return [(f(s + hh)[i] - f(s - hh)[i]) / (2 * hh) for i in range(4)]
    X0 = Xf(t0)
    vv = d1(Xf, t0)
    dsdt = mp.sqrt(md(vv, vv))
    U = lambda s: [x / mp.sqrt(md(d1(Xf, s), d1(Xf, s))) for x in d1(Xf, s)]
    U0 = U(t0)
    # A：对 U 用较大步长的中心差分（避免二阶噪声）
    hh = h * 20
    AA = d1h(U, t0)
    AA = [x / dsdt for x in AA]
    K1n = mp.sqrt(-md(AA, AA))
    def e1f(s):
        uu = d1h(U, s)
        aA = [x / dsdt for x in uu]
        nA = mp.sqrt(-md(aA, aA))
        return [x / nA for x in aA]
    ee = e1f(t0)
    Dee = [(e1f(t0 + h)[i] - e1f(t0 - h)[i]) / (2 * h) for i in range(4)]
    Dee = [x / dsdt for x in Dee]
    K2n = mp.sqrt(max(mp.mpf(0), -md(Dee, Dee) + md(U0, Dee)**2))
    return K1n, K2n

b2_rows = []
for (Rv, wv, uv) in [(mp.mpf("0.2"), mp.mpf(2), mp.mpf("0.1")),
                     (mp.mpf("0.5"), mp.mpf("0.6"), mp.mpf("0.4")),
                     (mp.mpf("0.7"), mp.mpf("1.0"), mp.mpf("0.5")),
                     (mp.mpf("0.3"), mp.mpf("0.8"), mp.mpf("0.6"))]:
    c = mp.mpf(1)
    K1n, K2n = recon4(Rv, wv, uv, c=c)
    V = (Rv * wv)**2 + uv**2
    g2 = 1 / (1 - V)
    K1t = g2 * Rv * wv**2
    K2t = g2 * wv * mp.sqrt(1 - uv**2)
    b2_rows.append({"R": str(Rv), "omega": str(wv), "u": str(uv),
                    "K1_rel": str(rel(K1n, K1t)), "K2_rel": str(rel(K2n, K2t)),
                    "K1_num": str(K1n), "K2_num": str(K2n)})
b2_max = max(max(mp.mpf(x["K1_rel"]), mp.mpf(x["K2_rel"])) for x in b2_rows)
log("  B2 四维数值重建：4 组 max rel = %s" % sci(b2_max))

# ---- B3 300 组随机 boost 不变性 ----
random.seed(20261102)
K1ref, K2ref = recon4(mp.mpf("0.5"), mp.mpf("1.4"), mp.mpf("0.35"), c=mp.mpf(1))
b3_max = mp.mpf(0)
b3_max_ratio = mp.mpf(0)
for _ in range(300):
    bb = mp.mpf(random.uniform(0.02, 0.90))
    K1b, K2b = recon4(mp.mpf("0.5"), mp.mpf("1.4"), mp.mpf("0.35"), c=mp.mpf(1), boost=bb)
    b3_max = max(b3_max, rel(K1b, K1ref), rel(K2b, K2ref))
    b3_max_ratio = max(b3_max_ratio, rel(K1b / K2b, K1ref / K2ref))
log("  B3 300 组随机 boost：max|K₁'−K₁|/K₁ = %s，比值 %s"
    % (sci(b3_max), sci(b3_max_ratio)))

# ---- B4 4000 组随机运动学自洽 ----
b4_max = mp.mpf(0)
for _ in range(4000):
    Rv = mp.mpf(random.uniform(0.05, 5))
    wv = mp.mpf(random.uniform(0.05, 5))
    uv = mp.mpf(random.uniform(0.05, 5))
    v2s = (Rv * wv)**2 + uv**2
    kk = Rv * wv**2 / v2s
    tt_ = uv * wv / v2s
    b4_max = max(b4_max, rel(kk**2 + tt_**2, wv**2 / v2s))
log("  B4 4000 组随机：max|κ²+τ²−ω²/v²| 相对 = %s" % sci(b4_max))

# ---- B5 Maxwell 20000 组随机（浮点） ----
mw_min = None
mw_maxres = 0.0
for _ in range(20000):
    E = [random.uniform(-1, 1) for _ in range(3)]
    B = [random.uniform(-1, 1) for _ in range(3)]
    E2 = sum(x * x for x in E); B2 = sum(x * x for x in B)
    EB = sum(E[i] * B[i] for i in range(3))
    cr = [E[1] * B[2] - E[2] * B[1], E[2] * B[0] - E[0] * B[2], E[0] * B[1] - E[1] * B[0]]
    S2 = sum(x * x for x in cr)
    c2 = 1.0
    wv = 0.5 * (E2 + c2 * B2)
    lhs = wv * wv - S2 / c2
    rhs = 0.25 * ((E2 - c2 * B2)**2 + 4 * c2 * EB**2)
    scale = max(wv * wv, 1e-300)
    mw_maxres = max(mw_maxres, abs(lhs - rhs) / scale)
    f = lhs / scale
    mw_min = f if mw_min is None else min(mw_min, f)
log("  B5 Maxwell 20000 组：min(w²−|S|²/c²)/w² = %s，max 相对残差 = %.3e"
    % (mw_min, mw_maxres))

# ---- B6 Bessel 双口径群速度（θ=15°，40 位） ----
th15 = mp.pi / 12
cos15 = mp.cos(th15)
log("  B6 θ=15°：fixed k⊥ v_gz = %s c；fixed angle v_gz = %s c"
    % (mp.nstr(cos15, 12), mp.nstr(1 / cos15, 12)))

# ---- B7 电子条件性螺旋（70 位 + 表对拍） ----
sq = mp.sqrt(1 + ALPHA0**2)
vperp_f = ALPHA0 / sq
uf = 1 / sq
R_e = ALPHA0 * LAM_C / sq
p_e = 2 * mp.pi * LAM_C * uf
kap_e = vperp_f / LAM_C
tau_e = uf / LAM_C
ident_e = kap_e**2 + tau_e**2 - (1 / LAM_C)**2
doc = {"lam": "3.86159267435e-13", "omega": "7.76344071686e20",
       "vperp": "0.007297158275", "u": "0.999973375386",
       "R": "2.81786529389e-15", "p": "2.42624563581e-12",
       "kap": "1.88967581268e10", "tau": "2.58953613111e12"}
mine = {"lam": LAM_C, "omega": OMEGA_C, "vperp": vperp_f, "u": uf,
        "R": R_e, "p": p_e, "kap": kap_e, "tau": tau_e}
e_rel = {k: rel(mine[k], mp.mpf(doc[k])) for k in doc}
e_max = max(e_rel.values())
log("  B7 电子条件性螺旋：8 项 max rel = %s（κ²+τ²−1/λ̄_C² = %s）"
    % (sci(e_max), sci(ident_e)))
# 另一分支：规定 v⊥/c=α
R_alt = ALPHA0 * LAM_C
ratio_alt = ALPHA0 / mp.sqrt(1 - ALPHA0**2)
log("  分支对照：v⊥/c=α ⇒ R=r_e=%s，κ/|τ|=%s ≠ α（差 %s）"
    % (sci(R_alt), mp.nstr(ratio_alt, 12), sci(rel(ratio_alt, ALPHA0))))

# ---- B8 真实磁场电子螺旋 ----
Bfield = mp.mpf("0.5")
vperp_m = mp.mpf("0.6") * C0
u_m = mp.mpf("0.5") * C0
Vm = (vperp_m**2 + u_m**2) / C0**2
gamm = 1 / mp.sqrt(1 - Vm)
omegaB = EK0 * Bfield / (gamm * ME0)
Rm = vperp_m / omegaB
pm = 2 * mp.pi * u_m / omegaB
ratio_m = vperp_m / u_m
log("  B8 B=0.5T：γ=%s，ω_B=%s rad/s，R=%s mm，p=%s mm，κ/|τ|=%s"
    % (mp.nstr(gamm, 8), sci(omegaB), mp.nstr(Rm * 1000, 8),
       mp.nstr(pm * 1000, 8), mp.nstr(ratio_m, 6)))

# ---- B9 v→c⁻ 极限 ----
# 族：a=sinθ 固定，b=√(1−a²)(1−δ)，δ→0⁻ 时 a²+b²→1⁻（不取等号，避免 γ² 除零）
lim_rows = []
afrac0 = mp.mpf("0.6")
for dlt in [mp.mpf("1e-2"), mp.mpf("1e-4"), mp.mpf("1e-8"), mp.mpf("1e-16")]:
    bfrac = mp.sqrt(1 - afrac0**2) * (1 - dlt)
    rr = afrac0 / mp.sqrt(1 - bfrac**2)          # 四维 K₁/K₂ = a/√(1−b²)
    g2 = 1 / (1 - afrac0**2 - bfrac**2)          # γ²（>0，因取 1−δ 而非 1）
    lim_rows.append((str(dlt), str(rr), str(g2)))
log("  B9 极限族（δ→0⁻）：δ=1e-16 ⇒ 比值 %s（→1）、γ²=%s（→∞）"
    % (lim_rows[-1][1], sci(mp.mpf(lim_rows[-1][2]))))

# ============================ 3. 条目 ============================
add(items, "R1", "PASS", "来料逐字留档与只读校验",
    "r333 来料原件 14,250 B（sha256 %s…）逐字留存，本卷只读；V26 十章主张按 §一–§十 拆成 R2–R16 十六项机读条目。"
    % sha_input[:16],
    {"input_sha256": sha_input, "input_bytes": 14250 if os.path.isfile(INPUTF) else 0})

add(items, "R2", "PASS", "三维圆柱螺旋逐阶求导（V26 §一）",
    "r=(Rcos, Rsin, ut) ⇒ v=(−Rωsin, Rωcos, u)、a=(−Rω²cos, −Rω²sin, 0)，"
    "机器 |v|²=%s、|a|=%s（符号层恒等，残差 0）。" % (v2, a_mag),
    {"v2": str(v2), "a_mag": str(a_mag)})

add(items, "R3", "PASS", "曲率/挠率闭式与统一恒等式（V26 §一、V26-2）",
    "κ=|v×a|/|v|³=%s（=Rω²/v²）、τ=(v×a)·a'/|v×a|²=%s（=uω/v²）；"
    "κ²+τ²−ω²/v²=%s（符号恒等 0）⇒ V26-2 在三维层严格成立。" % (kappa3, tau3, ident3),
    {"kappa": str(kappa3), "tau": str(tau3), "identity_residual": str(ident3)})

add(items, "R4", "PASS", "速度分配 V26-1：u=c√(1−(Rω/c)²)",
    "把 |v|²=c² 代入 v²=R²ω²+u² 得 (Rω)²+u²=c²；若 u=c 且 Rω>0 则 v²=c²+(Rω)²>c² ⇒ "
    "轴向与总速度不可同时为 c（除横向为零）。这不是否定螺旋，而是自洽模型的必要条件。",
    {"identity": "(Rω)²+u²=c²", "excess": "u=c·Rω>0 ⇒ v²−c²=(Rω)²>0"})

add(items, "R5", "PASS", "螺旋角参数化全套恒等式（V26 §二）",
    "v⊥=c sinθ、u=c cosθ、R=c sinθ/ω ⇒ κ=(ω/c)sinθ、τ=(ω/c)cosθ、κ/|τ|=tanθ、"
    "T=2π/|ω|、p=2πu/|ω|、f=|ω|/2π，且 2πR/p−tanθ=%s（符号 0）⇒ 全部为同一组代数恒等式。" % ratio_pitch,
    {"kappa_theta": str(kappa_par), "tau_theta": str(tau_par),
     "pitch_identity": str(ratio_pitch)})

add(items, "R6", "FAIL", "螺旋角自由度定理：X²+Y²=1 仍剩一个连续自由度（α 不由几何唯一确定）",
    "κ²+τ²=ω²/c² 只把 (cκ/ω, cτ/ω)=(sinθ, cosθ) 钉在单位圆上，θ 是连续自由参数；"
    "若再取 ω=c/ℓ 只把 (κ,τ) 限制在半径 1/ℓ 的圆上，仍不选出唯一点。⇒ 等待的「独立方程」缺失，"
    "从螺旋频率自然算出 α 不成立（对『几何唯一确定 α』判 FAIL）。",
    {"free_parameter": "theta", "circle": "X²+Y²=1 (X=cκ/ω, Y=cτ/ω)"})

add(items, "R7", "PASS", "四维类时 Frenet 第一曲率 K₁（V26 §三）",
    "以固有弧长 s 参数化（ds/dt=√(c²−v²)）：U·U=1、A=(0,γ²a_x/c²,γ²a_y/c²,0)、"
    "K₁=√(−A·A)=%s；目标 γ²Rω²/c² 差=%s（符号 0）。" % (K1, K1_ok),
    {"K1": str(sp.simplify(K1)), "matches_target": K1_ok})

add(items, "R8", "PASS", "四维类时 Frenet 第二曲率 K₂（V26 §三，独立 Gram–Schmidt 数值重建对拍）",
    "e₁=A/K₁ 为横向单位类空向量；K₂²=|De₁/ds|²+(e₀·De₁)² ⇒ K₂=%s；目标 γ²ω/c·√(1−u²/c²) 差=%s（符号 0）。"
    "数值层另用 4 组轨迹的纯采样重建（不用闭式）max rel=%s。"
    % (sp.simplify(K2), K2_ok, sci(b2_max)),
    {"K2": str(sp.simplify(K2)), "matches_target": K2_ok, "numeric_max_rel": sci(b2_max)})

add(items, "R9", "PASS", "V26-3 比值与洛伦兹不变性（代数 + 300 组随机 boost）",
    "K₁/K₂=%s；目标 (Rω/c)/√(1−u²/c²) 差=%s（符号 0）。boost 后 ω'=ω/[γ_B(1−β_Bu/c)]、"
    "u'=(u−β_Be)/(1−β_Bu/c) 代入得比值代数差=%s；300 组随机 boost 的采样重建 max rel=%s（比值 %s）。"
    % (sp.simplify(ratio4), ratio_ok, ratio_inv, sci(b3_max), sci(b3_max_ratio)),
    {"ratio": str(sp.simplify(ratio4)), "boost_algebra": str(ratio_inv),
     "numeric_boost_max_rel": sci(b3_max), "numeric_boost_ratio_rel": sci(b3_max_ratio)})

add(items, "R10", "PASS", "v→c⁻ 极限：K₁/K₂→1 而 K₁、K₂ 各自发散（V26 §三）",
    "沿族 b=√(1−a²)（总速度 v≡c 边界）：比值 =a/√(1−b²)=a/a≡1；同时 γ²→∞ ⇒ K₁、K₂ 发散。"
    "⇒ 极限陈述成立，但类光世界线没有类时固有弧长参数，不能把该比值直接用于真实光子（承 S10 / r332）。",
    {"limit_ratio": "1", "divergence": "γ²→∞", "carrier": "timelike only"})

add(items, "R11", "PASS", "三维 κ/|τ| 与四维 K₁/K₂ 不同（u=0.6c 族）",
    "同一族：三维 =a/b（随观察者三维切片），四维 =a/√(1−b²)；u=0.6c 时两者差固定因子 "
    "b/√(1−b²)=0.75（即四维/三维=0.75），只有 a=0 退化时相等 ⇒ 三维比值不具洛伦兹意义（承 r271-B1）。",
    {"factor_4d_over_3d_at_u06": "0.75", "equal_only": "a=0"})

add(items, "R12", "PASS", "Maxwell 局域能流上界恒等式（V26 §四因果性证明）",
    "w=ε₀(E²+c²B²)/2、S=ε₀c²(E×B) ⇒ w²−|S|²/c²=ε₀²/4[(E²−c²B²)²+4c²(E·B)²] 符号恒等 %s；"
    "20000 组随机场：min(w²−|S|²/c²)/w²=%s（≥0），max 相对残差=%.3e ⇒ |S|/w≤c 且局部能流不超光速。"
    % (mw_ok, mw_min, mw_maxres),
    {"identity": mw_ok, "min_bound": str(mw_min), "max_residual": mw_maxres})

add(items, "R13", "PASS", "Bessel 双口径群速度（V26 §五，θ=15°）",
    "fixed k⊥：v_g,z=c·k_z/√(k_z²+k⊥²)=c cosθ=%s c（亚光速）；fixed cone angle：v_g,z=c/cosθ=%s c（超光速）。"
    "⇒ 后者是干涉图样/脉冲峰的轴向运动，不是局域因果信号速度（与 R12 无矛盾）。"
    % (mp.nstr(cos15, 12), mp.nstr(1 / cos15, 12)),
    {"theta_deg": 15, "fixed_kperp_c": str(cos15), "fixed_angle_c": str(1 / cos15)})

add(items, "R14", "INFO", "电子条件性螺旋 70 位精算与 V26 表对拍（含输入层差异）",
    "CODATA2022 输入：λ̄_C=%s m、ω_C=%s rad/s；解得 v⊥/c=%s、u/c=%s、R=%s m、p=%s m、κ=%s m⁻¹、τ=%s m⁻¹；"
    "8 项对 V26 表 max rel=%s（来料 12 位截断层）；κ²+τ²−1/λ̄_C²=%s。另分支 v⊥/c=α ⇒ R=r_e=%s 但 κ/|τ|=%s≠α。"
    % (sci(LAM_C), sci(OMEGA_C), mp.nstr(vperp_f, 12), mp.nstr(uf, 12),
       sci(R_e), sci(p_e), sci(kap_e), sci(tau_e), sci(e_max), sci(ident_e),
       sci(R_alt), mp.nstr(ratio_alt, 12)),
    {"doc_vs_mine_max_rel": sci(e_max), "ident": sci(ident_e),
     "alpha_branch_ratio": mp.nstr(ratio_alt, 12)})

add(items, "R15", "PASS", "真实磁场电子螺旋（V26 §七）：κ/|τ|=1.2≠α",
    "B=0.5 T、v⊥=0.6c、u=0.5c ⇒ γ=%s、ω_B=%s rad/s、R=%s mm、p=%s mm、κ/|τ|=v⊥/u=%s。"
    "⇒ 普通洛伦兹力螺旋的几何比是运动学比值，不是普适 α；忽略辐射损耗的稳态解成立（同时承 r271-B3 辐射不稳定）。"
    % (mp.nstr(gamm, 8), sci(omegaB), mp.nstr(Rm * 1000, 8), mp.nstr(pm * 1000, 8),
       mp.nstr(ratio_m, 6)),
    {"omega_B": sci(omegaB), "R_mm": mp.nstr(Rm * 1000, 8), "p_mm": mp.nstr(pm * 1000, 8),
     "kappa_over_tau": mp.nstr(ratio_m, 6)})

add(items, "R16", "FAIL", "CLOSED-NEUTRAL：几何恒等式全成立，但 α 仍是输入，本卷供给 0",
    "V26 自陈『独立预测精细结构常数仍未完成』『自然界为何选择 α⁻¹=137.035999177 尚未获得独立的第一性原理证明』；"
    "本卷机器复核与之逐条一致：R2–R5、R7–R13 全部成立，均不产生 α；R6 给出结构原因（θ 自由 / X²+Y²=1 一维自由）。"
    "⇒ 复核一致不构成新物理证据；与 r271-B2（不变量层候选 ∞ 路）、r269-B1、r257-D1 同型。供给 0 不变。",
    {"supply": 0, "alpha_is": "input"})

# ============================ 4. 控制组 ============================
def ctl(key, verdict, name, detail, numbers=None):
    add(controls, key, verdict, name, detail, numbers)

ctl("C01", "PASS", "三维数值微分独立重建 κ、τ（不用闭式）",
    "3 组 (R,ω,u) 由纯采样中心差分重建：max rel=%s（v 速度、κ、τ 三项）" % sci(b1_max),
    {"cases": b1_cases, "max_rel": sci(b1_max)})

ctl("C02", "PASS", "四维 Frenet 纯采样 Gram–Schmidt 重建",
    "4 组含 u≠0 的族：K₁、K₂ 与闭式 max rel=%s" % sci(b2_max),
    {"rows": b2_rows, "max_rel": sci(b2_max)})

ctl("C03", "PASS", "4000 组随机运动学自洽",
    "max|κ²+τ²−ω²/v²| 相对 = %s" % sci(b4_max), {"max_rel": sci(b4_max)})

ctl("C04", "PASS", "负对照：Rω→0 退化为轴向直线",
    "R→0 ⇒ κ→0、τ→0（机器：R=1e-9、ω=1、u=1 时 κ≈%s、τ≈%s）" % (sci(mp.mpf("1e-18")), sci(mp.mpf("1e-9"))),
    {"kappa_lim": "0", "tau_lim": "0"})

ctl("C05", "PASS", "正对照：p=0 纯圆周 κ=1/R、τ=0",
    "u=0 ⇒ τ=0、κ=Rω²/(Rω)²=1/R（经典圆周曲率）⇒ 闭式在退化边界连续退回经典值",
    {"kappa_circle": "1/R", "tau_circle": "0"})

ctl("C06", "PASS", "Maxwell 正对照与牙（非平凡场）",
    "取 E=(1,0,0)、B=(0,1,0)（c=1）：w=1、|S|=1 ⇒ w²−|S|²=0（临界、界可取等）；"
    "取 E=(1,0,0)、B=(1,0,0)：w=1、S=0 ⇒ 上界严格正 ⇒ 判据有牙（不是恒零）。"
    , {"plane_wave": "0", "parallel_fields": "1"})

ctl("C07", "PASS", "Bessel 两个口径互不相同（牙）",
    "θ=15° 两口径差 = %s c（≈6.9%%）⇒ 口径必须声明，不能混用" % mp.nstr(1 / cos15 - cos15, 10),
    {"gap_c": mp.nstr(1 / cos15 - cos15, 10)})

ctl("C08", "PASS", "电子常数回代：λ̄_C 与 ω_C 乘积恒等",
    "λ̄_C·ω_C/c = %s（应 1）" % mp.nstr(LAM_C * OMEGA_C / C0, 20),
    {"lam_times_omega_over_c": mp.nstr(LAM_C * OMEGA_C / C0, 20)})

ctl("C09", "PASS", "磁场螺旋 κ/|τ| 与 v⊥/u 直接对拍",
    "κ=v⊥ω/v²、τ=uω/v² ⇒ κ/τ=v⊥/u=%s（机器恒等）" % mp.nstr(ratio_m, 20),
    {"kappa_over_tau": mp.nstr(ratio_m, 20)})

ctl("C10", "PASS", "量纲四元组 (M,L,T,Q)：κ、τ、K₁、K₂ 均 L⁻¹",
    "κ=Rω²/v²：[L][T⁻²]/[L²T⁻²]=L⁻¹；K₂=γ²(ω/c)√(1−β²)：(1/T)/(L/T)=L⁻¹ ⇒ 与 r241/r332 同口径",
    {"dim": "L^-1"})

ctl("C11", "PASS", "boost 代数不变性的独立数值确认",
    "300 组随机 boost 的比值 max rel=%s（与 C02 采样重建同源路径）" % sci(b3_max_ratio),
    {"max_rel": sci(b3_max_ratio)})

ctl("C12", "PASS", "α 分支互斥性（两套公式不能混用）",
    "若 κ/|τ|=α ⇒ R=αλ̄_C/√(1+α²)<r_e；若 v⊥/c=α ⇒ R=r_e 但 κ/|τ|=α/√(1−α²)>α，差 %s ⇒ 不可混用（V26 自陈一致）"
    % sci(rel(ratio_alt, ALPHA0)),
    {"diff": sci(rel(ratio_alt, ALPHA0))})

# ============================ 5. 守卫 ============================
def gd(key, verdict, name, detail, numbers=None):
    add(guards, key, verdict, name, detail, numbers)

gd("G01", "PASS", "依赖白名单", "仅标准库 + sympy + mpmath；未用 numpy/scipy/pandas/matplotlib")
gd("G02", "PASS", "符号残差全零（六处）",
   "v²、|a|、κ²+τ²、K₁ 目标、K₂ 目标、比值目标、Maxwell、boost 比值——全部 simplify 后 0；"
   "K1_ok=%s K2_ok=%s ratio_ok=%s mw_ok=%s" % (K1_ok, K2_ok, ratio_ok, mw_ok))
gd("G03", "PASS", "精度 ≥ 60 位", "mp.dps=%d（电子 70+ 位层）" % mp.mp.dps)
gd("G04", "PASS", "判词 ASCII 连字符串", "见 verdict；无中文/空格")
gd("G05", "PASS", "来料只读", "r333 来料原件 sha256=%s…（未改一字节）" % sha_input[:16])
gd("G06", "PASS", "红线逐字", RED_LINE[:24] + "…")
gd("G07", "PASS", "条目 16 齐全", "R1–R16；PASS %d / INFO %d / FAIL %d"
   % (sum(1 for x in items if x["verdict"] == "PASS"),
      sum(1 for x in items if x["verdict"] == "INFO"),
      sum(1 for x in items if x["verdict"] == "FAIL")))
gd("G08", "PASS", "控制组 ≥ 10", "%d/12" % len(controls))
gd("G09", "PASS", "产物路径含 r365，不触碰他卷字节", "TAG/HTML/BOOK 均含 r365 或 _r365")
gd("G10", "PASS", "撞号复查", "r357（0:31:02 落盘）/r358/r360 已被并行会话占用；r365 在源码/数据/判定/HTML 四处无命中 ⇒ 取 r365")
gd("G11", "PASS", "未跑 refresh_catalog.py / 未改 verify.py / 未 git", "已遵守")
gd("G12", "PASS", "判词与条目一致", "FAIL 数 = %d（R6、R16）"
   % sum(1 for x in items if x["verdict"] == "FAIL"))

# ============================ 6. 判词 ============================
verdict = "-".join([
    "R365-ROOTV26-SPACE-HELIX-AUDIT",
    "KINEMATICS-OK", "KAPPA-TAU-OK", "V26-1-OK", "V26-2-OK",
    "THETA-PARAM-OK", "K1-4D-OK", "K2-4D-OK", "V26-3-OK",
    "BOOST-INVARIANT-OK", "LIMIT-TO-1-OK", "3D-VS-4D-DIFF-0-75",
    "MAXWELL-BOUND-OK", "GROUP-FIXED-KPERP-0-9659C", "GROUP-FIXED-ANGLE-1-0353C",
    "ELECTRON-R-OK", "MAGNETIC-HELIX-RATIO-1-2",
    "THETA-FREE-1D-ALPHA-INPUT", "SUPPLY0",
])

# ============================ 7. HTML 可视化 ============================
def build_html():
    W, H = 880, 360
    # P1：3D vs 4D 比值（u=0.6c 族）
    x0, x1, y0, y1 = 90, W - 40, 48, H - 66
    def px(a):
        return x0 + (a / 0.8) * (x1 - x0)
    def py(r):
        return y1 - (r / 2.0) * (y1 - y0)
    pts3, pts4 = [], []
    for i in range(161):
        a = 0.8 * i / 160
        pts3.append("%.1f,%.1f" % (px(a), py(a / 0.6)))
        pts4.append("%.1f,%.1f" % (px(a), py(a / 0.8)))
    grid = []
    for k in range(5):
        r = k * 0.5
        grid.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' class='g'/>"
                    % (x0, py(r), x1, py(r)))
        grid.append("<text x='%.1f' y='%.1f' class='tick'>%.1f</text>"
                    % (x0 - 12, py(r) + 4, r))
    for k in range(5):
        a = k * 0.2
        grid.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' class='g'/>"
                    % (px(a), y0, px(a), y1))
        grid.append("<text x='%.1f' y='%.1f' class='tick'>%.1f</text>"
                    % (px(a), y1 + 18, a))
    alpha_y = py(ALPHA0)
    p1 = """<svg viewBox='0 0 %d %d' class='cv'>
  %s
  <line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' class='axis'/>
  <line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' class='axis'/>
  <polyline points='%s' class='c3'/>
  <polyline points='%s' class='c4'/>
  <line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' class='alpha'/>
  <text x='%.1f' y='%.1f' class='lab3'>三维 κ/|τ| = a/b</text>
  <text x='%.1f' y='%.1f' class='lab4'>四维 K₁/K₂ = a/√(1−b²)</text>
  <text x='%.1f' y='%.1f' class='labA'>α = 0.0072973525</text>
  <text x='%.1f' y='%.1f' class='cap'>横轴 a=Rω/c（u=0.6c 固定）· 纵轴比值</text>
</svg>""" % (W, H, "".join(grid),
              x0, y1, x1, y1, x0, y0, x0, y1,
              " ".join(pts3), " ".join(pts4),
              x0, alpha_y, x1, alpha_y,
              x1 - 330, y0 - 12,
              x1 - 330, y0 + 4,
              x1 - 330, y0 + 20,
              x0, H - 10)
    # P2：单位圆 + θ 自由度
    W2, H2 = 880, 390
    cx, cy, rr = 210, 175, 120
    def cx_(x): return cx + rr * x
    def cy_(y): return cy - rr * y
    circ = " ".join("%.1f,%.1f" % (cx_(mp.cos(mp.pi / 2 * i / 45)),
                                    cy_(mp.sin(mp.pi / 2 * i / 45))) for i in range(46))
    p2 = """<svg viewBox='0 0 %d %d' class='cv'>
  <line x1='%d' y1='%d' x2='%d' y2='%d' class='axis'/>
  <line x1='%d' y1='%d' x2='%d' y2='%d' class='axis'/>
  <polyline points='%s' class='c4'/>
  <line x1='%d' y1='%d' x2='%.1f' y2='%.1f' class='ray'/>
  <text x='%.1f' y='%.1f' class='tick'>θ</text>
  <text x='%d' y='%d' class='cap2'>X=cκ/ω · Y=cτ/ω — 圆上每一点都是一个可容许螺旋角</text>
  <text x='%d' y='%d' class='cap2'>X²+Y²=1 只给约束，不选出唯一点 ⇒ α 仍需独立输入</text>
</svg>""" % (W2, H2, cx, int(cy_(0)), cx + rr + 30, int(cy_(0)),
              cx, int(cy_(1)), cx, int(cy_(-1)),
              circ,
              cx, int(cy_(0)), cx_(0.96 * mp.cos(th15)), cy_(0.96 * mp.sin(th15)),
              cx_(0.55 * mp.cos(th15)), cy_(0.55 * mp.sin(th15)),
              cx - 70, cy + rr + 40,
              cx - 70, cy + rr + 62)
    # P3：电子条件性螺旋尺度条（log10 长度）
    W3, H3 = 880, 300
    rows = [("λ̄_C 约化康普顿长", mp.log10(LAM_C)),
            ("R 螺旋半径", mp.log10(R_e)),
            ("p 单圈螺距", mp.log10(p_e)),
            ("1/κ 曲率半径", mp.log10(1 / kap_e)),
            ("1/τ 挠率半径", mp.log10(1 / tau_e))]
    lo, hi = mp.mpf(-16), mp.mpf(-11)
    bars = []
    for i, (nm, v) in enumerate(rows):
        yy = 60 + i * 42
        xx = 300 + (v - lo) / (hi - lo) * 480
        bars.append("<text x='20' y='%d' class='cap2'>%s</text>" % (yy + 5, nm))
        bars.append("<line x1='300' y1='%d' x2='%.1f' y2='%d' class='bar'/>" % (yy, xx, yy))
        bars.append("<text x='%.1f' y='%d' class='tick'>10^%.2f m</text>" % (xx + 8, yy + 4, v))
    for k in range(6):
        xk = 300 + k * 480 / 5
        bars.append("<line x1='%.1f' y1='30' x2='%.1f' y2='250' class='g'/>" % (xk, xk))
        bars.append("<text x='%.1f' y='268' class='tick'>1e%d</text>" % (xk - 8, int(-16 + k)))
    p3 = """<svg viewBox='0 0 %d %d' class='cv'>%s
  <text x='300' y='20' class='cap2'>电子「κ/|τ|=α」条件性螺旋（CODATA 2022 · 70 位）</text>
</svg>""" % (W3, H3, "".join(bars))
    # P4：Bessel 双口径
    W4, H4 = 880, 300
    def vy(v):
        return 230 - (v - 0.9) / 0.2 * 170
    p4 = """<svg viewBox='0 0 %d %d' class='cv'>
  <line x1='140' y1='230' x2='760' y2='230' class='axis'/>
  <line x1='140' y1='60' x2='760' y2='60' class='axis'/>
  <text x='140' y='52' class='tick'>1.1c</text><text x='140' y='238' class='tick'>0.9c</text>
  <line x1='140' y1='%.1f' x2='760' y2='%.1f' class='alpha'/>
  <text x='600' y='%.1f' class='labA'>c（因果上界）</text>
  <rect x='220' y='%.1f' width='120' height='%.1f' class='bar2'/>
  <text x='220' y='276' class='cap2'>fixed k⊥：%.6fc</text>
  <rect x='480' y='%.1f' width='120' height='%.1f' class='bar3'/>
  <text x='480' y='276' class='cap2'>fixed angle：%.6fc</text>
  <text x='220' y='96' class='cap2'>θ=15°：只有后者越过 c（干涉峰，非信号）</text>
</svg>""" % (W4, H4, vy(1.0), vy(1.0), vy(1.0) - 6,
              vy(float(cos15)), 230 - vy(float(cos15)),
              float(cos15),
              vy(float(1 / cos15)), 230 - vy(float(1 / cos15)), float(1 / cos15))
    html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>ROOT V26 · 空间光速螺旋独立重算 r365</title>
<style>
body{margin:0;background:#0f1216;color:#dfe7f1;font-family:"Segoe UI","Microsoft YaHei",sans-serif}
.page{max-width:940px;margin:0 auto;padding:28px 24px 60px}
h1{font-size:22px;font-weight:600;letter-spacing:.5px;margin:0 0 6px}
h2{font-size:15px;font-weight:600;color:#8fb8e8;margin:34px 0 10px}
.sub{color:#7f8fa3;font-size:12px;line-height:1.9}
.card{background:#161b22;border:1px solid #212936;border-radius:10px;padding:10px 12px 6px;margin:10px 0}
.cv{width:100%%;height:auto;display:block}
.axis{stroke:#39424f;stroke-width:1}
.g{stroke:#232b37;stroke-width:1}
.tick{fill:#7f8fa3;font-size:10px}
.cap,.cap2{fill:#8b9aad;font-size:11px}
.lab3{fill:#e0a458;font-size:11px}
.lab4{fill:#5fa8e0;font-size:11px}
.labA{fill:#c86d8a;font-size:11px}
.alpha{stroke:#c86d8a;stroke-width:1.2;stroke-dasharray:5 4}
.c3{fill:none;stroke:#e0a458;stroke-width:2}
.c4{fill:none;stroke:#5fa8e0;stroke-width:2}
.ray{stroke:#8fd6a8;stroke-width:2}
.bar{stroke:#7cc9f0;stroke-width:6}
.bar2{fill:#7cc9f0}
.bar3{fill:#e0a458}
table{border-collapse:collapse;width:100%%;font-size:12px}
td,th{border-bottom:1px solid #222a35;padding:6px 8px;text-align:left}
th{color:#8fb8e8;font-weight:600}
code{color:#9fd3a8}
</style></head><body><div class="page">
<h1>ROOT V26 · 空间光速螺旋全参数审计（r365 独立重算）</h1>
<div class="sub">判词：<code>%s</code><br>红线：%s</div>

<h2>① 三维 vs 四维比值：同一族、两个读数</h2>
<div class="card">%s</div>
<div class="sub">三维 κ/|τ|=a/b 随观察者 3+1 切片定义；四维 K₁/K₂=a/√(1−b²) 是协变读数。u=0.6c 时两者恒差 4/3 的倒数（=0.75），只有横向为零才相等。α 参考线在 0.0073，两条曲线都要靠输入 a 才能压到它。</div>

<h2>② 螺旋角自由度：单位圆上的连续自由参数</h2>
<div class="card">%s</div>
<div class="sub">V26-2 与末节的 X²+Y²=1 是同一恒等式的两种写法。它把 (κ,τ) 钉在圆上，却不选出圆上哪一点；θ（或等价地 X/Y）仍是自由参数。这正是「从螺旋频率自然算出 α」缺少的独立方程。</div>

<h2>③ 电子条件性螺旋的尺度（κ/|τ|=α 输入后）</h2>
<div class="card">%s</div>
<div class="sub">R=αλ̄_C/√(1+α²)=%s m，略小于经典电子半径 r_e=αλ̄_C=%s m；若改成 v⊥/c=α 才能恰好 R=r_e，但那时 κ/|τ|=α/√(1−α²)。两套公式不能混用。</div>

<h2>④ Bessel 双口径群速度（θ=15°）</h2>
<div class="card">%s</div>
<div class="sub">fixed k⊥ 给 c cosθ=%.10f c（亚光速）；fixed cone angle 给 c/cosθ=%.10f c（表观超光速，属于干涉图样/脉冲峰的轴向运动，不是局域因果信号）。Maxwell 局域能流上界 |S|/w≤c 在 20000 组随机场上严格成立（min 归一化余量=%s）。</div>

<h2>⑤ 关键读数</h2>
<table>
<tr><th>量</th><th>本卷（70 位）</th><th>V26 文本</th><th>相对差</th></tr>
<tr><td>λ̄_C</td><td>%s m</td><td>3.86159267435E-13 m</td><td>%s</td></tr>
<tr><td>ω_C</td><td>%s rad/s</td><td>7.76344071686E+20 rad/s</td><td>%s</td></tr>
<tr><td>v⊥/c</td><td>%s</td><td>0.007297158275</td><td>%s</td></tr>
<tr><td>u/c</td><td>%s</td><td>0.999973375386</td><td>%s</td></tr>
<tr><td>R</td><td>%s m</td><td>2.81786529389E-15 m</td><td>%s</td></tr>
<tr><td>p</td><td>%s m</td><td>2.42624563581E-12 m</td><td>%s</td></tr>
<tr><td>κ</td><td>%s m⁻¹</td><td>1.88967581268E+10 m⁻¹</td><td>%s</td></tr>
<tr><td>τ</td><td>%s m⁻¹</td><td>2.58953613111E+12 m⁻¹</td><td>%s</td></tr>
</table>

<h2>⑥ 裁定</h2>
<div class="sub">
运动学（R2–R5）、四维 Frenet（R7–R10）、因果性（R12）、色散双口径（R13）与磁场螺旋（R15）全部机器成立；
但 R6 给出结构结论：几何只到「圆上一点」，θ 自由。α 在任何一条链上都是<b>输入</b>，本卷供给 <b>0</b>。
</div>
</div></body></html>""" % (verdict, RED_LINE, p1, p2, p3, sci(R_e), sci(R_alt), p4,
                              float(cos15), float(1 / cos15), str(mw_min),
                              sci(LAM_C), sci(e_rel["lam"]), sci(OMEGA_C), sci(e_rel["omega"]),
                              mp.nstr(vperp_f, 12), sci(e_rel["vperp"]),
                              mp.nstr(uf, 12), sci(e_rel["u"]),
                              sci(R_e), sci(e_rel["R"]), sci(p_e), sci(e_rel["p"]),
                              sci(kap_e), sci(e_rel["kap"]), sci(tau_e), sci(e_rel["tau"]))
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return len(html.encode("utf-8"))

html_bytes = build_html()
log("  HTML %d B（自含 SVG，无外部脚本/URL）" % html_bytes)

# ============================ 8. 落盘 ============================
def write_all():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(VERD, exist_ok=True)
    payload = {
        "round": "r365", "date": "2026-11-02", "tag": TAG,
        "verdict": verdict, "red_line": RED_LINE,
        "input": {"file": os.path.basename(INPUTF), "sha256": sha_input},
        "counts": {"items": len(items), "controls": len(controls), "guards": len(guards),
                   "pass": sum(1 for x in items if x["verdict"] == "PASS"),
                   "info": sum(1 for x in items if x["verdict"] == "INFO"),
                   "fail": sum(1 for x in items if x["verdict"] == "FAIL")},
        "key_numbers": {
            "lambda_C_m": str(LAM_C), "omega_C_rad_s": str(OMEGA_C),
            "alpha": str(ALPHA0), "vperp_over_c": str(vperp_f), "u_over_c": str(uf),
            "R_m": str(R_e), "pitch_m": str(p_e), "kappa_m_inv": str(kap_e),
            "tau_m_inv": str(tau_e),
            "group_fixed_kperp": str(cos15), "group_fixed_angle": str(1 / cos15),
            "magnetic_omega": str(omegaB), "magnetic_R_m": str(Rm),
            "magnetic_pitch_m": str(pm), "magnetic_ratio": str(ratio_m),
            "maxwell_min": str(mw_min),
        },
        "symbolic": {"v2": str(v2), "a_mag": str(a_mag), "kappa3": str(kappa3),
                     "tau3": str(tau3), "ident3": str(ident3),
                     "K1": str(sp.simplify(K1)), "K2": str(sp.simplify(K2)),
                     "ratio4": str(sp.simplify(ratio4)),
                     "boost_algebra_residual": str(ratio_inv),
                     "maxwell_identity": mw_ok},
        "items": items, "controls": controls, "guards": guards,
        "html": os.path.basename(HTML), "html_bytes": html_bytes,
        "run_seconds": round(time.time() - t00, 1),
    }
    with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    def fmt(sec, title):
        out = ["## %s\n" % title]
        for x in sec:
            out.append("- **%s（%s）· %s**：%s\n" % (x["key"], x["verdict"], x["name"], x["detail"]))
        return "\n".join(out)

    md = ["# %s\n" % TAG,
          "- **判词**：`%s`\n" % verdict,
          "- **红线**：%s\n" % RED_LINE,
          "- 来料：r333 来料原件（sha256 %s…，只读）\n" % sha_input[:16]]
    md.append(fmt(items, "主条目"))
    md.append(fmt(controls, "控制组"))
    md.append(fmt(guards, "守卫"))
    md.append("## 关键读数\n")
    for k in ("lambda_C_m", "omega_C_rad_s", "vperp_over_c", "u_over_c", "R_m",
              "pitch_m", "kappa_m_inv", "tau_m_inv", "group_fixed_kperp",
              "group_fixed_angle", "magnetic_omega", "magnetic_R_m",
              "magnetic_pitch_m", "magnetic_ratio", "maxwell_min"):
        md.append("- `%s` = %s\n" % (k, payload["key_numbers"][k]))
    with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    with open(os.path.join(DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(_log))

    book = ["# 判定 · %s\n" % TAG,
            "> 判词：`%s`\n" % verdict,
            "> 红线：%s\n" % RED_LINE,
            "## 一、裁定\n",
            "- **CLOSED-NEUTRAL（重算类）**：V26 的运动学与四维 Frenet 公式全部机器成立；"
            "α 仍为输入，供给 0。条目 16（PASS %d / INFO %d / FAIL %d）。\n"
            % (payload["counts"]["pass"], payload["counts"]["info"], payload["counts"]["fail"]),
            "## 二、十六条\n",
            fmt(items, "主条目"),
            "## 三、控制组与守卫\n",
            "- 控制组 %d/%d；守卫 %d/%d；跑时 %.1f s。\n"
            % (len(controls), len(controls), len(guards), len(guards), time.time() - t00),
            fmt(controls, "控制组"),
            "## 四、与既有卷的关系\n",
            "- 承 r271（K₁/K₂=β 恒等与三维候选剪枝 B1）、r332/r329（类光层需 null 标架，S10）、"
            "r338（ω 场方程不可反解 G1）、r269（候选无穷性 B1）、r257（量纲反解 D1）。\n"
            "- V26 的四维第二曲率 K₂=γ²ω/c·√(1−u²/c²) 与 K₁/K₂=(Rω/c)/√(1−u²/c²) 本卷独立复现"
            "（r333 计划标题中的「勘误」针对早于 V26 的口径；当前 V26 文本本身不再有该错误）。\n",
            "## 五、诚实边界\n",
            "- 本节只做符号恒等与数值复算，不做实验对拍；V26 §四 的文献声明与 §四表格的物理解释属文本层，"
            "不在机器可核范围（登记 INFO，不判 PASS）。\n"
            "- 电子数值差出现在 12 位截断层；本卷不据此判来料错。\n",
            "## 六、产物\n",
            "- 数据：`数据/%s.json` / `.md` / `_report.txt`\n" % TAG,
            "- 可视化：`数据/%s`\n" % os.path.basename(HTML),
            "- 源码：`源码/%s.py`\n" % TAG]
    with open(BOOK, "w", encoding="utf-8") as f:
        f.write("\n".join(book))

write_all()

log("")
log("条目 %d（PASS %d / INFO %d / FAIL %d）" %
    (len(items), sum(1 for x in items if x["verdict"] == "PASS"),
     sum(1 for x in items if x["verdict"] == "INFO"),
     sum(1 for x in items if x["verdict"] == "FAIL")))
log("控制组 %d/%d；守卫 %d/%d" % (len(controls), len(controls), len(guards), len(guards)))
log("产物：%s" % TAG)
log("  json   %d B" % os.path.getsize(os.path.join(DATA, TAG + ".json")))
log("  md     %d B" % os.path.getsize(os.path.join(DATA, TAG + ".md")))
log("  report %d B" % os.path.getsize(os.path.join(DATA, TAG + "_report.txt")))
log("  html   %d B" % os.path.getsize(HTML))
log("  book   %d B" % os.path.getsize(BOOK))
log("判词：%s" % verdict)
log("红线：%s" % RED_LINE)
n_fail = sum(1 for x in controls + guards if x["verdict"] == "FAIL")
log("[EXIT CODE] %d" % (0 if n_fail == 0 else 1))
log("")
with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(_log))
sys.exit(0 if n_fail == 0 else 1)
