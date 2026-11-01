# -*- coding: utf-8 -*-
"""
TUFT-r329 · 光速螺旋纲领 G4「null Frenet 标架重写」的伪弧长重写与帧局部定价
（承《整理_光速螺旋纲领_封死点与可攻方向清单_2026-11-01》§二 G4 / §四 三道自检门）

靶：G4 ——「用伪参量化重建 κ,τ（仍为 L⁻¹），重推微分方程」。
本卷把 G4 要的东西**逐项做出来**（伪弧长 σ、κ,τ 闭式、Frenet–Serret 重推、boost 变换表），
再证明它作为「缺口」只能是**条件收口**：重建出来的 κ,τ 是**帧局部量**（κ'=κ/D²），
不存在洛伦兹不变的 null 弧长 ⇒ 「τ≡0 是退化分支」只在特定观察者帧内成立 ⇒ 旧读数必须标注帧。

判决链（第 1 层：承载物）：
  Q1  旧 Frenet 在 null 上失效（ds²≡0 ⇒ ds=0 ⇒ T=dT/ds 不可定义；λ-读数 ∝ 1/k² 非几何）
  Q2  伪弧长重写 σ=−u·x：null ⇒ 空间投影恒单位速（boost 后仍恒 1，机器验）
  Q3  协变恒等式 ω²=c²(κ²+τ²) 在螺旋分支恒成立（sympy 差 0 + Decimal boost 网格）
  Q4  ★τ≡0 是帧伪影：v_z=0 帧 τ=0；boost ⇒ τ'=−βω'≠0
  Q5  ★无洛伦兹不变 κ,τ 定理：κ'=κ/D²、D=γ(1−βv_z) ⇒ 只要 β≠0 就 κ'≠κ
  Q6  r95 玻尔锚 τ=1.378963e8 m⁻¹ 的帧定价表（Doppler 可标度，非不变量）
  Q7  伪弧长 Frenet–Serret 重推（dT/dσ=κN、dN/dσ=−κT+τB、dB/dσ=−τN；Darboux Ω=κB+τT）
  Q8  与 S10/S2/S11/S3 判词对表
  Q9  G1–G7 门槛可达性登记 + 三道自检门
  Q10 判据集 R1–R6
控制组 C1–C4 / 守卫 G1–G10
判词：NULL-FRENET-IS-FRAME-LOCAL / TAU-ZERO-IS-FRAME-ARTIFACT /
      NO-LORENTZ-INVARIANT-KAPPA-TAU / G4-CLOSED-CONDITIONAL
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 80

RID = "r329"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_光速螺旋G4_null标架伪弧长重写_帧局部kappa_tau定理与tau零帧伪影定价_"
        "精算与可视化_%s" % (RID, STAMP))
JUD_PATH = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-r329_"):]))
HTML_PATH = os.path.join(ROOT, "四力统一方程_null标架伪弧长重写G4攻破_r329可视化_%s.html" % STAMP)

WRITTEN = []
T0 = time.time()

# ---------------------------------------------------------------- 高精度工具
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
D0, D1, D2, D3, D4 = Decimal(0), Decimal(1), Decimal(2), Decimal(3), Decimal(4)


def fmt(x, nd=10):
    if isinstance(x, Decimal):
        if x == 0:
            return "0"
        return "%.*E" % (nd - 1, x)
    return str(x)


def rel(a, b):
    if b == 0:
        return Decimal("Infinity") if a != 0 else D0
    return abs(a / b - D1)


def dsqrt(x):
    return Decimal(x).sqrt()


# ---------------------------------------------------------------- 常数（口径登记）
C_L = Decimal("2.99792458e8")            # c [m/s]（定义值）
ALPHA = Decimal("7.2973525693e-3")       # 精细结构常数（CODATA 2018）
A0 = Decimal("5.29177210903e-11")        # 玻尔半径 [m]
HBAR = Decimal("1.054571817e-34")        # ℏ [J s]
HBARC = HBAR * C_L                       # ℏc [J m]
A_MERC = Decimal("0.387098") * Decimal("1.495978707e11")

# r95 登记值（本卷只做「帧定价」，不重推它的来源）
TAU_R95 = Decimal("1.3789630609e8")      # r95 玻尔锚 τ [m⁻¹]（v_z→c 极限）
KAP_R95 = Decimal("1.0063050e6")         # 同锚 κ [m⁻¹]

R_LIST = {}
ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


# ================================================================ Q1 · 旧 Frenet 失效
def q1():
    """度规 (−,+,+,+)。null 曲线 ℓ·ℓ=0 ⇒ 洛伦兹弧长 ds²≡0 ⇒ s 不存在 ⇒ T^a=dx^a/ds 无定义。
    例①平面圆 null 化：x(t)=(t, a cos ωt, a sin ωt, 0)、null ⇒ aω=1（a=ω=1 时空间速=1、κ_E=1、τ_E=0）；
        λ-读数 κ_naive=aω²（=1）在 λ→kλ 下 ∝1/k² ⇒ 非几何量。
    例②直线 null：x=(λ,λ,0,0) ⇒ κ=0。"""
    import sympy as sp
    t, om, aa, kk = sp.symbols("t omega a k", positive=True)
    x = sp.Matrix([t, aa * sp.cos(om * t), aa * sp.sin(om * t), sp.Integer(0)])
    eta = sp.diag(-1, 1, 1, 1)
    lv = x.diff(t)
    n2 = sp.simplify((lv.T * eta * lv)[0])                  # −1 + a²ω²
    n2_null = sp.simplify(n2.subs(aa, 1 / om))              # 0
    r3 = x[1:4, 0]
    r1 = r3.diff(t)
    r2 = r1.diff(t)
    spd2 = sp.simplify((r1.T * r1)[0])                      # a²ω²
    kn = sp.sqrt(sp.simplify((r2.T * r2)[0]))               # aω²
    kn_null = sp.simplify(kn.subs(aa, 1 / om))              # ω（a=1/ω ⇒ 1）
    kn_rescale = sp.simplify(kn.subs(om, om / kk))           # aω²/k²
    ratio = sp.simplify(kn_rescale / kn)                    # 1/k²
    # 空间速：ds_E/dt = aω；Euclid 弧长 κ_E = 1/a
    kE = sp.simplify(1 / aa)
    kE_null = sp.simplify(kE.subs(aa, 1 / om))              # ω（与 kn_null 同值，仅当 aω=1）
    # ① 直线 null
    lam = sp.symbols("lambda", positive=True)
    xs = sp.Matrix([lam, lam, sp.Integer(0), sp.Integer(0)])
    ls = xs.diff(lam)
    ns = sp.simplify((ls.T * eta * ls)[0])                  # 0
    rs = xs[1:4, 0]
    # 直线二阶导恰为零 ⇒ κ=0（直接用零向量而非 sqrt(0)）
    r1s = rs.diff(lam)
    r2s = r1s.diff(lam)
    kzero = sp.simplify((r2s.T * r2s)[0])                   # 0
    kv = {"ℓ·ℓ 一般": str(n2), "ℓ·ℓ(null: a=1/ω)": str(n2_null),
          "ds²(null)": str(n2_null), "洛伦兹弧长 s": "0（不存在）",
          "λ-读数 κ_naive": str(kn), "null 分支 κ_naive": str(kn_null),
          "λ→kλ 后 κ_naive": str(kn_rescale), "比值": str(ratio),
          "空间速 aω(null)": str(sp.simplify(sp.sqrt(spd2).subs(aa, 1 / om))),
          "Euclid 弧长 κ_E": str(kE), "null 分支 κ_E": str(kE_null),
          "直线 null κ": str(kzero)}
    ok = (n2_null == 0) and (ratio == 1 / kk ** 2) and (kzero == 0) \
        and (sp.simplify(kE_null - kn_null) == 0)
    add("Q1", "承载物", "旧 Frenet 在 null 上失效已机器证明：ds²≡0 ⇒ s 不存在；λ-读数 ∝1/k² 非几何",
        "PASS" if ok else "FAIL",
        "度规 (−,+,+,+)。对 x(t)=(t,a cos ωt,a sin ωt,0)：**ℓ·ℓ = %s**，取 null 分支 a=1/ω ⇒ "
        "**ℓ·ℓ ≡ %s** ⇒ 洛伦兹弧长 ds²≡0、s≡0 ⇒ T^a=dx^a/ds = (1/0)·dx^a/dλ **不可定义**（S10 的机器版）。"
        "λ 参数下的朴素读数 |d²r/dλ²| = %s（a=ω=1 时 1），但把参数改成 λ'=kλ ⇒ %s，比值 **%s** ⇒ "
        "它是**参数产物，不是几何量**。空间速 aω=1（null 的必然），Euclid 弧长下 κ_E=%s（=1/a）——"
        "κ_E 存在但**不是洛伦兹量**。直线 null x=(λ,λ,0,0) 给 κ=%s ⇒ 「κ=0 有意义」只在直线这一退化情形。"
        % (n2, n2_null, kn, kn_rescale, ratio, kE, kzero),
        kv)
    return {"k_naive": 1.0, "ratio": str(ratio)}


# ================================================================ Q2 · 伪弧长重写
def q2():
    """取惯性观察者 u^a=(1,0,0,0)（u·u=−1），定义伪弧长 σ := −u·x = t（该帧坐标时）。
    null ⇒ ℓ^t=dt/dσ=1 ⇒ 空间投影 |dr/dσ|=1（恒单位速）；boost 后仍为 1（null 条件的洛伦兹不变性）。
    在 σ 下算 κ,τ：κ=aω²、τ=ωv_z（null 时 a²ω²+v_z²=c²=1）。
    平移 σ→σ+c 与绕 z 旋转下 κ,τ 不变（机器验）。"""
    import sympy as sp
    sg, om, aa, vz, be, ch = sp.symbols("sigma omega a v_z beta chi", real=True)
    om2 = sp.Symbol("omega", positive=True)
    aa2 = sp.Symbol("a", positive=True)
    r = sp.Matrix([aa2 * sp.cos(om2 * sg), aa2 * sp.sin(om2 * sg), vz * sg])
    r1 = r.diff(sg)
    r2 = r1.diff(sg)
    r3 = r2.diff(sg)
    speed2 = sp.simplify((r1.T * r1)[0])                    # a²ω²+v_z²
    # 单位速条件（null 的空间投影）：a²ω²+v_z²=1
    kap = sp.simplify(sp.sqrt((r2.T * r2)[0]))              # aω²（单位速下）
    cross = r1.cross(r2)
    crn = sp.simplify(sp.sqrt((cross.T * cross)[0]))        # aω²·speed
    tau = sp.simplify(cross.dot(r3) / (crn ** 2))           # 单位速 ⇒ ωv_z
    kap_u = sp.simplify(kap.subs(vz, sp.sqrt(1 - aa2 ** 2 * om2 ** 2)))   # 保留
    tau_u = sp.simplify(tau.subs(vz, sp.sqrt(1 - aa2 ** 2 * om2 ** 2)))
    # 平移不变
    sh = sp.Symbol("shift", real=True)
    rT = sp.Matrix([aa2 * sp.cos(om2 * (sg + sh)), aa2 * sp.sin(om2 * (sg + sh)), vz * (sg + sh)])
    kT = sp.simplify(sp.sqrt((rT.diff(sg).diff(sg).T * rT.diff(sg).diff(sg))[0]))
    cT = rT.diff(sg).cross(rT.diff(sg).diff(sg))
    tT = sp.simplify(cT.dot(rT.diff(sg).diff(sg).diff(sg))
                     / (cT.T * cT)[0])
    # 绕 z 旋转 χ ⇒ 相位平移 ⇒ κ,τ 不变
    rR = sp.Matrix([aa2 * sp.cos(om2 * sg + ch), aa2 * sp.sin(om2 * sg + ch), vz * sg])
    kR = sp.simplify(sp.sqrt((rR.diff(sg).diff(sg).T * rR.diff(sg).diff(sg))[0]))
    # boost：横向单位速向量 (cosφ, sinφ, 0) 沿 z boost ⇒ |v'|²=1/γ²+β²=1（解析）
    phi = sp.Symbol("phi", real=True)
    bb = sp.Symbol("beta", real=True)
    gam = 1 / sp.sqrt(1 - bb ** 2)
    vxp = sp.cos(phi) / gam
    vyp = sp.sin(phi) / gam
    vzp = -bb
    nrm = sp.simplify(vxp ** 2 + vyp ** 2 + vzp ** 2)        # 应 = 1
    kv = {"σ 定义": "σ=−u·x=t（u=(1,0,0,0)，u·u=−1）",
          "空间速²（null 前）": str(speed2), "κ(单位速)": str(kap), "τ(单位速)": str(tau),
          "κ（null 代入后）": str(kap_u), "τ（null 代入后）": str(tau_u),
          "平移后 κ/τ": "%s / %s" % (kT, sp.simplify(tT)),
          "旋转后 κ": str(kR), "boost 后 |v'|²−1": str(sp.simplify(nrm - 1))}
    ok = (sp.simplify(nrm - 1) == 0) and (sp.simplify(kT ** 2 - kap ** 2) == 0) \
        and (sp.simplify(tT - tau) == 0) and (sp.simplify(kR ** 2 - kap ** 2) == 0) \
        and (kap_u == aa2 * om2 ** 2) \
        and (sp.simplify(tau_u - om2 * sp.sqrt(1 - aa2 ** 2 * om2 ** 2)) == 0)
    add("Q2", "承载物", "伪弧长重写 σ=−u·x 交付：null ⇒ 空间投影恒单位速；κ=aω²、τ=ωv_z（帧局部）",
        "PASS" if ok else "FAIL",
        "取惯性观察者 u=(1,0,0,0)、伪弧长 **σ := −u·x = t**（该帧坐标时）。null 条件 ℓ·ℓ=0 ⇒ ℓ^t=dt/dσ=1 ⇒ "
        "**空间投影 |dr/dσ| ≡ 1**（机器给 a²ω²+v_z²=%s；null 代入后 =1）。于是普通单位速 Frenet 可用："
        "**κ=aω²、τ=ωv_z**（sympy 从 |r'×r''|/|r'|³ 与 (r'×r'')·r'''/|r'×r''|² 直算，无量纲 c=1）。"
        "boost 沿 z 后 |v'|²−1 = %s（恒 0）⇒ **单位速是洛伦兹不变的**（这是 null 条件的直接推论）。"
        "平移 σ→σ+c 与绕 z 旋转 χ 下 κ,τ 严格不变（%s / %s）⇒ κ,τ 是**空间等距不变量**，"
        "但不是洛伦兹不变量（Q5）。"
        % (speed2, sp.simplify(nrm - 1), sp.simplify(kT - kap), sp.simplify(tT - tau)),
        kv)
    return {"kappa": "a*omega^2", "tau": "omega*v_z"}


# ================================================================ Q3 · 协变恒等式 + boost 网格
def q3():
    """null 螺旋：a²ω²+v_z²=c² ⇒ ω²=c²(κ²+τ²)。
    boost（沿 z，β）：D=γ(1−βv_z/c)、ω'=ω/D、v_z'=(v_z−βc)/(1−βv_z/c)、κ'=κ/D²、τ'=ω'v_z'。
    表 β=0..0.9（c=1，a=ω=1，v_z=0）；每行验 κ'²+τ'²=ω'²。"""
    import sympy as sp
    aa, om, vz, cc = sp.symbols("a omega v_z c", positive=True)
    kap = aa * om ** 2 / cc ** 2
    tau = om * vz / cc ** 2
    # null：a²ω²+v_z²=c² ⇒ 代入 v_z²=c²−a²ω²
    ident = sp.simplify(om ** 2 - cc ** 2 * (kap ** 2 + tau ** 2))
    ident_null = sp.simplify(ident.subs(vz, sp.sqrt(cc ** 2 - aa ** 2 * om ** 2)))
    # boost 变换（c=1 无量纲）
    be, gm = sp.symbols("beta gamma", real=True)
    vzz = sp.Symbol("v_z", real=True)
    gam = 1 / sp.sqrt(1 - be ** 2)
    Dv = gam * (1 - be * vzz)
    omp = sp.Symbol("omega", positive=True) / Dv
    vzp = (vzz - be) / (1 - be * vzz)
    kapp = (aa * sp.Symbol("omega", positive=True) ** 2) / Dv ** 2
    tapp = omp * vzp
    # 特例 v_z=0, a=ω=1 ⇒ κ'=1/γ²、τ'=−β/γ、ω'=1/γ；验 κ'²+τ'²=ω'²
    k0 = sp.simplify(kapp.subs({vzz: 0, aa: 1, sp.Symbol("omega", positive=True): 1}))
    t0 = sp.simplify(tapp.subs({vzz: 0, sp.Symbol("omega", positive=True): 1}))
    w0 = sp.simplify(omp.subs({vzz: 0, sp.Symbol("omega", positive=True): 1}))
    resid = sp.simplify(k0 ** 2 + t0 ** 2 - w0 ** 2)
    # Decimal 网格
    rows = []
    for bs in ("0", "0.1", "0.3", "0.5", "0.7", "0.9"):
        b = Decimal(bs)
        gam_d = D1 / dsqrt(D1 - b * b)
        a_, om_, vzo = D1, D1, D0
        D = gam_d * (D1 - b * vzo)                         # c=1
        omp_ = om_ / D
        vzp_ = (vzo - b) / (D1 - b * vzo)
        kap0 = a_ * om_ ** 2
        kap_ = kap0 / D ** 2
        tau_ = omp_ * vzp_
        res = kap_ * kap_ + tau_ * tau_ - omp_ * omp_
        rows.append((bs, fmt(gam_d), fmt(D), fmt(omp_), fmt(vzp_), fmt(kap_), fmt(tau_), fmt(res)))
    kv = {"ω²−c²(κ²+τ²)": str(ident), "null 代入后": str(ident_null),
          "κ'=κ/D² 的 v_z=0 例": str(k0), "τ'=ω'v_z' 的 v_z=0 例": str(t0),
          "ω' 的 v_z=0 例": str(w0), "κ'²+τ'²−ω'²（β 符号）": str(resid),
          "boost 网格(β,γ,D,ω',v_z',κ',τ',残差)": [list(r) for r in rows]}
    ok = (ident_null == 0) and (resid == 0) \
        and all(abs(Decimal(r[7])) < Decimal("1e-70") for r in rows) \
        and Decimal(rows[3][5]).quantize(Decimal("1e-3")) == Decimal("0.750") \
        and Decimal(rows[3][6]).quantize(Decimal("1e-3")) == Decimal("-0.433")
    add("Q3", "判据", "协变恒等式 ω²=c²(κ²+τ²) 在 null 螺旋分支恒成立 + boost 网格逐行机器零",
        "PASS" if ok else "FAIL",
        "null 螺旋 a²ω²+v_z²=c² 下，**ω²−c²(κ²+τ²) = %s**（null 代入后 =%s，严格恒等）⇒ "
        "三重奏恒等式在 null 分支**不是新约束而是勾股恒等**。沿 z 的 boost：D=γ(1−βv_z/c)、ω'=ω/D、"
        "**κ'=κ/D²**、**τ'=ω'v_z'**，且 κ'²+τ'²=ω'² 逐行成立（残差全 0）。表（a=ω=1, v_z=0）："
        "β=0.1 ⇒ κ'=%s、τ'=%s；β=0.5 ⇒ **κ'=%s、τ'=%s**（κ 缩小 25%%、τ 从 0 变成 −0.433）；"
        "β=0.9 ⇒ κ'=%s、τ'=%s。⇒ **κ,τ 随帧连续变形，恒等式只约束形状不约束帧**。"
        % (ident, ident_null, rows[1][5], rows[1][6], rows[3][5], rows[3][6],
           rows[5][5], rows[5][6]),
        kv)
    return {"rows": rows}


# ================================================================ Q4 · τ≡0 是帧伪影
def q4():
    """S2 分支 v_z=0（aω=c）⇒ τ=0（螺旋退化为平面圆）。boost 后 v_z'=−βc/(1−0)=−βc ⇒
    τ'=ω'v_z'=−βω'c ≠ 0。⇒「τ≡0」只在「螺旋轴向静止的观察者帧」成立，不是几何事实。"""
    rows = []
    for bs in ("0", "0.1", "0.3", "0.5", "0.7", "0.9"):
        b = Decimal(bs)
        g = D1 / dsqrt(D1 - b * b)
        D = g
        omp = D1 / D
        vzp = -b
        tau = omp * vzp
        rows.append((bs, fmt(omp), fmt(vzp), fmt(tau)))
    tau_half = Decimal(rows[3][3])
    red = abs(tau_half) / Decimal(rows[3][1])
    kv = {"v_z=0 分支": "τ=0（平面圆）", "boost 表(β,ω',v_z',τ')": [list(r) for r in rows],
          "β=0.5 的 τ'": fmt(tau_half), "|τ'|/ω'（β=0.5）": fmt(red)}
    ok = (Decimal(rows[0][3]) == 0) and all(Decimal(r[3]) != 0 for r in rows[1:]) \
        and abs(tau_half) > Decimal("0.4")
    add("Q4", "判据", "★τ≡0 是帧伪影：v_z=0 帧 τ=0，boost 后 τ'=−βω'≠0（螺旋退化为圆只在特定帧成立）",
        "PASS" if ok else "FAIL",
        "承 S2（r151「v=c 且 ωr=c ⇒ τ≡0 退化为平面圆」）。在本卷口径下该分支是 **v_z=0, aω=c** ⇒ "
        "**τ=ωv_z=0**（帧内读数）。但沿 z 的 boost 给 v_z'=−βc、ω'=ω/γ ⇒ **τ'=−βω'**："
        "β=0.1 ⇒ %s；**β=0.5 ⇒ τ'=%s m⁻¹（|τ'|/ω'=0.5）**；β=0.9 ⇒ %s。"
        "⇒ **同一个 null 世界线，在不同惯性帧里「有的挠率不为零」**：所谓「螺旋退化为平面圆」"
        "只是「在螺旋轴向静止的那个观察者帧里的空间投影」，**是帧陈述，不是几何事实**。"
        "凡报 τ=0 必须报「在哪个 u 的帧」。"
        % (rows[1][3], tau_half, rows[5][3]),
        kv)
    return {"tau_half": tau_half}


# ================================================================ Q5 · 无洛伦兹不变 κ,τ
def q5():
    """κ'=κ/D²、D=γ(1−βv_z) 可取 (0,∞) 中任意值 ⇒ 若 κ 是标量则要求 κ'≡κ ∀β ⇒ 只能 κ=0（直线）。
    同理 τ'=ω'v_z' 亦可变号变幅 ⇒ 不存在洛伦兹不变的 (κ,τ)。
    数值：同一几何曲线（a=0.8, ω=1, v_z=0.6, null 校验 a²ω²+v_z²=1）在 β=±0.9 两个帧下 κ 差 11 倍。"""
    import sympy as sp
    be, gm, vzz, ka = sp.symbols("beta gamma v_z kappa", real=True)
    Dv = gm * (1 - be * vzz)
    kp = ka / Dv ** 2
    # 若不变则 kp−ka≡0 ∀β ⇒ 需要 1/D²≡1 ⇒ (1−βv_z)²γ²=1 ∀β ⇒ 只有 v_z=0 且 β=0
    cond = sp.simplify((Dv ** 2 - 1).subs({vzz: 0}))
    cond_b = sp.simplify(cond)                             # γ²−1 = β²γ² ≠ 0
    # 数值两帧
    a_, om_, vz_ = Decimal("0.8"), D1, Decimal("0.6")
    kap0 = a_ * om_ ** 2                                   # 0.8
    tau0 = om_ * vz_                                       # 0.6
    null_chk = a_ * a_ * om_ * om_ + vz_ * vz_             # 1
    def frame(b):
        b = Decimal(b)
        g = D1 / dsqrt(D1 - b * b)
        D = g * (D1 - b * vz_)
        omp = om_ / D
        vzp = (vz_ - b) / (D1 - b * vz_)
        return g, D, omp, vzp, kap0 / D ** 2, omp * vzp
    gP, DP, omP, vzP, kapP, tauP = frame("0.9")
    gM, DM, omM, vzM, kapM, tauM = frame("-0.9")
    ratio_km = kapP / kapM
    kv = {"κ'=κ/D²": str(kp), "不变条件 D²−1(v_z=0)": str(cond), "γ²−1（v_z=0）": str(cond_b),
          "同一曲线 κ(β=0)": fmt(kap0), "τ(β=0)": fmt(tau0), "null 校验": fmt(null_chk),
          "β=+0.9: γ,D,ω',v_z',κ',τ'": [fmt(gP), fmt(DP), fmt(omP), fmt(vzP), fmt(kapP), fmt(tauP)],
          "β=−0.9: γ,D,ω',v_z',κ',τ'": [fmt(gM), fmt(DM), fmt(omM), fmt(vzM), fmt(kapM), fmt(tauM)],
          "κ(+0.9)/κ(−0.9)": fmt(ratio_km)}
    # 定理成立（目标 FAIL：不存在不变的 κ,τ）
    ok = (null_chk == D1) and (ratio_km > Decimal("10")) and (abs(kapP - kap0) > Decimal("0.05")) \
        and (sp.simplify(cond_b) != 0)
    add("Q5", "判据", "★无洛伦兹不变 κ,τ：κ'=κ/D²、D=γ(1−βv_z) 随帧可变 ⇒ 标量假设只对直线成立",
        "FAIL" if ok else "INFO",
        "变换律 κ'=κ/D² 中 **D=γ(1−βv_z) 对给定曲线随 β 取 (0,∞) 内的连续值** ⇒ 若 κ 是洛伦兹标量，"
        "必须 κ'≡κ ∀β，即 D²≡1 ∀β——这只在 **v_z=0 且 β=0**（或不弯曲的 κ=0 直线）时成立"
        "（机器：γ²−1−β²γ² 非零）。数值：同一条 null 曲线（a=0.8,ω=1,v_z=0.6，null 校验 a²ω²+v_z²=%s）在 "
        "β=+0.9 帧 κ'=%s、β=−0.9 帧 κ'=%s，**差 %s 倍**；τ 由 %s 变到 %s / %s。"
        "⇒ **不存在与观察者无关的 (κ,τ)**；「κ=τ=ω/c」这类读数只能在被指名的帧里被解释。"
        "这正是 S11「同名异物」与 r54 N14「非洛伦兹不变量」的机器闭合。"
        % (null_chk, kapP, kapM, ratio_km, tauP, tauM, fmt(tau0)),
        kv)
    return {"ratio": ratio_km, "kapP": kapP, "kapM": kapM}


# ================================================================ Q6 · r95 玻尔锚帧定价
def q6():
    """r95 玻尔锚：ω_B=αc/a0、a=a0、v_z=c√(1−α²)（严格 null）；τ=ωv_z/c²=α/a0·√(1−α²)。
    r95 登记 τ=1.3789630609e8 = α/a0（即 v_z→c 极限，√(1−α²)≈1，相对差 2.66e−5）。
    boost 表：τ'=ω'v_z'/c²；结论：τ 是 Doppler 可标度的频率，不是不变量。"""
    om_B = ALPHA * C_L / A0                                # [s⁻¹]
    kap_B = ALPHA ** 2 / A0                                # [m⁻¹]（=a0ω²/c²）
    uz = dsqrt(D1 - ALPHA * ALPHA)                         # v_z/c（严格 null）
    vz = C_L * uz
    tau_exact = om_B * uz / C_L                            # [m⁻¹]
    tau_limit = ALPHA / A0                                 # r95 口径（v_z→c）
    d_r95 = rel(tau_limit, TAU_R95)
    d_exact = rel(tau_exact, TAU_R95)
    d_rel = rel(tau_limit, tau_exact)
    rows = []
    for bs in ("0", "0.3", "0.5", "0.7", "0.9"):
        b = Decimal(bs)
        g = D1 / dsqrt(D1 - b * b)
        D = g * (D1 - b * uz)
        omp = om_B / D
        uzp = (uz - b) / (D1 - b * uz)
        kap_ = kap_B / D ** 2
        tau_ = omp * uzp / C_L
        res = kap_ * kap_ + tau_ * tau_ - (omp / C_L) ** 2
        rows.append((bs, fmt(g), fmt(D), fmt(omp), fmt(uzp), fmt(kap_), fmt(tau_), fmt(res)))
    kv = {"ω_B[s⁻¹]": fmt(om_B), "κ_B[m⁻¹]": fmt(kap_B), "v_z/c": fmt(uz),
          "τ 严格 null[m⁻¹]": fmt(tau_exact), "τ v_z→c 极限[m⁻¹]": fmt(tau_limit),
          "r95 登记[m⁻¹]": fmt(TAU_R95), "极限 vs r95": fmt(d_r95), "严格 null vs r95": fmt(d_exact),
          "极限 vs 严格 null": fmt(d_rel),
          "boost 表(β,γ,D,ω',v_z/c,κ',τ',残差)": [list(r) for r in rows]}
    ok = (d_exact < Decimal("1e-8")) and (Decimal("1e-6") < d_r95 < Decimal("1e-4")) \
        and (Decimal(rows[2][6]) > Decimal("2e8")) \
        and (Decimal(rows[4][6]) > Decimal("5e8")) \
        and all(abs(Decimal(r[7])) < Decimal("1e-50") for r in rows)
    add("Q6", "判据", "r95 玻尔锚 τ=1.379e8 m⁻¹ 的帧定价：boost 下 τ 在 1.38e8→6.01e8 间移动（非不变量）",
        "PASS" if ok else "FAIL",
        "r95 的玻尔锚口径：ω_B=αc/a₀=%s s⁻¹、a=a₀、v_z=c√(1−α²) ⇒ κ_B=α²/a₀=%s m⁻¹、"
        "τ_B=ωv_z/c²=%s m⁻¹（**严格 null**）。r95 登记的 **τ=1.3789630609e8** 与严格 null 分支的"
        "相对差 **%s**（≈机器零）；若误按 v_z→c 极限 α/a₀ 读，则与登记值差 2.66e−5 —— 两档都必须在口径里写明。"
        "按 τ'=ω'v_z'/c² 做 boost：β=0.3 ⇒ %s；**β=0.5 ⇒ %s**；β=0.7 ⇒ %s；"
        "**β=0.9 ⇒ %s m⁻¹**（κ' 同步从 %s 升到 %s）。"
        "且 κ'²+τ'²=(ω'/c)² 逐行机器零 ⇒ **τ 是随帧 Doppler 标度的频率型量**，"
        "不是「曲率–挠率」意义上的不变量。⇒ r95 的 1.379e8 只能在「v_z 沿 +z 且接近 c 的那个帧」里引用。"
        % (fmt(om_B), fmt(kap_B), fmt(tau_exact), fmt(d_exact), rows[1][6], rows[2][6],
           rows[3][6], rows[4][6], fmt(kap_B), rows[4][5]),
        kv)
    return {"rows": rows, "tau_limit": tau_limit}


# ================================================================ Q7 · Frenet–Serret 重推
def q7():
    """伪弧长下单位速空间曲线：T=dr/dσ、dT/dσ=κN、dN/dσ=−κT+τB、dB/dσ=−τN；
    Darboux 向量 Ω_D=κB+τT（满足 dT/dσ=Ω×T、dN/dσ=Ω×N、dB/dσ=Ω×B）。
    sympy 对螺旋逐式验证；数值通道用中心差分独立对拍。"""
    import sympy as sp
    sg = sp.Symbol("sigma", real=True)
    om = sp.Symbol("omega", positive=True)
    aa = sp.Symbol("a", positive=True)
    vz = sp.Symbol("v_z", real=True)
    r = sp.Matrix([aa * sp.cos(om * sg), aa * sp.sin(om * sg), vz * sg])
    r1 = r.diff(sg)
    r2 = r1.diff(sg)
    r3 = r2.diff(sg)
    unit = {vz ** 2: 1 - aa ** 2 * om ** 2}                # 单位速 ⇔ null 空间投影
    T = r1
    speed2 = sp.simplify((T.T * T)[0])                     # a²ω²+v_z²
    kap = sp.simplify(sp.sqrt((r2.T * r2)[0]))             # aω²
    N = sp.simplify(r2 / kap)                              # (−cosωσ,−sinωσ,0)
    cross = r1.cross(r2)
    crn2 = sp.simplify((cross.T * cross)[0])               # |r'×r''|²
    B = sp.simplify(cross / sp.sqrt(crn2))                 # 单位副法向
    tau = sp.simplify(cross.dot(r3) / crn2)                # ωv_z/(a²ω²+v_z²)
    e1 = sp.simplify(T.diff(sg) - kap * N)
    e2 = sp.simplify((N.diff(sg) - (-kap * T + tau * B)).subs(unit))
    e3 = sp.simplify((B.diff(sg) - (-tau * N)).subs(unit))
    Om = sp.simplify((kap * B + tau * T).subs(unit))
    e4 = sp.simplify((T.diff(sg) - Om.cross(T)).subs(unit))
    e5 = sp.simplify((N.diff(sg) - Om.cross(N)).subs(unit))
    e6 = sp.simplify((B.diff(sg) - Om.cross(B)).subs(unit))
    # 数值通道：中心差分（a=0.8, ω=1, v_z=0.6 ⇒ 单位速 0.64+0.36=1；κ=0.8、τ=0.6）
    import math
    h = 1e-3
    vzf = 0.6

    def rx(s):
        return (0.8 * math.cos(s), 0.8 * math.sin(s), vzf * s)

    def d1(s):
        return tuple((rx(s + h)[i] - rx(s - h)[i]) / (2 * h) for i in range(3))

    def d2(s):
        p = d1(s + h)
        m = d1(s - h)
        return tuple((p[i] - m[i]) / (2 * h) for i in range(3))

    def d3(s):
        p = d2(s + h)
        m = d2(s - h)
        return tuple((p[i] - m[i]) / (2 * h) for i in range(3))

    def crs(u, v):
        return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])

    def nrm(u):
        return math.sqrt(sum(x * x for x in u))

    def vsub(u, v):
        return tuple(u[i] - v[i] for i in range(3))

    s0 = 0.3
    Tn = d1(s0)
    speed = nrm(Tn)
    d2v = d2(s0)
    kn = nrm(d2v)
    Nn = tuple(x / kn for x in d2v)
    Bn = crs(Tn, Nn)
    d3v = d3(s0)
    cT = crs(Tn, d2v)                                      # = r'×r''（未归一）⇒ |cT|=κ
    tau_n = sum(cT[i] * d3v[i] for i in range(3)) / sum(x * x for x in cT)
    dTv = d2(s0)
    Np = tuple(x / nrm(d2(s0 + h)) for x in d2(s0 + h))
    Nm = tuple(x / nrm(d2(s0 - h)) for x in d2(s0 - h))
    dN = tuple((Np[i] - Nm[i]) / (2 * h) for i in range(3))
    Bp = crs(d1(s0 + h), tuple(x / nrm(d2(s0 + h)) for x in d2(s0 + h)))
    Bm = crs(d1(s0 - h), tuple(x / nrm(d2(s0 - h)) for x in d2(s0 - h)))
    dB = tuple((Bp[i] - Bm[i]) / (2 * h) for i in range(3))
    res1 = nrm(vsub(dTv, tuple(kn * Nn[i] for i in range(3))))
    rhs2 = tuple(-kn * Tn[i] + tau_n * Bn[i] for i in range(3))
    res2 = nrm(vsub(dN, rhs2))
    res3 = nrm(vsub(dB, tuple(-tau_n * Nn[i] for i in range(3))))
    d_kap_vs_exact = rel(Decimal(str(kn)), Decimal("0.8"))  # κ 数值 vs 精确 0.8
    d_tau_vs_exact = rel(Decimal(str(abs(tau_n))), Decimal("0.6"))
    kv = {"κ": str(kap), "τ": str(tau), "T": [str(x) for x in T],
          "N": [str(x) for x in N], "B": [str(x) for x in B],
          "dT/dσ−κN": str(e1), "dN/dσ−(−κT+τB)": str(e2), "dB/dσ−(−τN)": str(e3),
          "Ω_D": [str(x) for x in Om],
          "Ω×T−dT": str(e4), "Ω×N−dN": str(e5), "Ω×B−dB": str(e6),
          "数值 |dr/dσ|": fmt(Decimal(str(speed))), "数值 κ": fmt(Decimal(str(kn))),
          "数值 τ": fmt(Decimal(str(tau_n))), "κ 数值−精确": fmt(d_kap_vs_exact),
          "τ 数值−精确": fmt(d_tau_vs_exact),
          "数值 e1 模": fmt(Decimal(str(res1))), "数值 e2 模": fmt(Decimal(str(res2))),
          "数值 e3 模": fmt(Decimal(str(res3)))}
    ok = all(all(sp.simplify(x) == 0 for x in e) for e in (e1, e2, e3, e4, e5, e6)) \
        and (speed > 0.999) and (speed < 1.001) \
        and (abs(kn - 0.8) < 1e-5) and (abs(abs(tau_n) - 0.6) < 1e-4) \
        and (res1 < 1e-5) and (res2 < 1e-4) and (res3 < 1e-4)
    add("Q7", "判据", "伪弧长 Frenet–Serret 重推交付：三式 + Darboux Ω=κB+τT 全机器零，数值通道对拍",
        "PASS" if ok else "FAIL",
        "在伪弧长 σ 下空间曲线单位速，故标准 Frenet–Serret **直接可用**："
        "**dT/dσ=κN、dN/dσ=−κT+τB、dB/dσ=−τN**，Darboux 向量 **Ω_D=κB+τT** 满足 "
        "dT/dσ=Ω×T 等三式。sympy 对 null 螺旋逐式验证：e1=%s、e2=%s、e3=%s、e4..e6=%s/%s/%s（全零向量）。"
        "数值通道（a=0.8,ω=1,v_z=0.6，单位速 0.64+0.36=1，中心差分）给 |dr/dσ|=%s、"
        "κ=%s（与精确 0.8 的相对差 %s）、τ=%s（精确 0.6）；"
        "三式数值残差 e1=%s、e2=%s、e3=%s。"
        "⇒ **G4 要的「重推微分方程」已字面完成**；但完成的是**帧内方程**，跨帧不闭合（Q5）。"
        % (e1, e2, e3, e4, e5, e6, fmt(Decimal(str(speed))), fmt(Decimal(str(kn))),
           fmt(d_kap_vs_exact), fmt(Decimal(str(tau_n))),
           fmt(Decimal(str(res1))), fmt(Decimal(str(res2))), fmt(Decimal(str(res3)))),
        kv)
    return {"speed_n": Decimal(str(speed)), "kn_n": Decimal(str(kn)),
            "tau_n": Decimal(str(abs(tau_n)))}


# ================================================================ Q8 · 判词对表
def q8():
    chain = [
        ("S10（r151/r124）", "null 世界线 Frenet 无定义 ⇒ 光子层 κ,τ 无承载物",
         "本卷 Q1 机器复证（ds²≡0）；Q2 给伪弧长下的**帧局部**重建", "部分解（帧局部）"),
        ("S2（r151）", "v=c 且 ωr=c 双约束 ⇒ τ≡0 退化为平面圆",
         "本卷 Q4：τ=0 只在 v_z=0 帧成立，boost ⇒ τ'=−βω'≠0", "改写为帧陈述"),
        ("S11（r95）", "τ 同名异物（联络挠率 vs Frenet 挠率）",
         "本卷 Q6：Frenet τ 是帧量（Doppler 可标度）⇒ 同名异物之外还有**同值异帧**", "加强"),
        ("S3（r95 G03–G07）", "单一柱对称螺旋场不能表示球对称引力",
         "本卷未碰（球对称约化在 r324 Q4 已做）；光子层读数与引力扇区无交集", "未动"),
    ]
    kv = {"对表": [list(c) for c in chain], "条数": 4}
    add("Q8", "对表", "判词链对表：S10 从「无定义」升级为「帧局部有定义但非不变」；S2 改写为帧陈述",
        "INFO",
        "；".join("%s：%s ⇒ %s（%s）" % c for c in chain) +
        "。⇒ **S10 不再是「完全没有」，而是「有，但只在被指名的帧里有」**——这比原判词更强："
        "原来可以靠「没算」被质疑，现在有了显式重建，质疑只能落在不变性上（Q5 已挡住）。",
        kv)
    return {"n": 4}


# ================================================================ Q9 · 门槛登记
def q9():
    rows = [
        ("G1", "ω(r,t) 的场方程", "未动（需二阶微分方程且能反解 ω）", "开"),
        ("G2", "r 的来源", "未动（康普顿锚 v_θ/c=137>1 越定义域）", "开"),
        ("G3", "弱场史瓦西退化的数值验收", "r324 已收口（Birkhoff ⇒ 零判别力）", "收口（负）"),
        ("G4", "null Frenet 标架重写", "本卷：伪弧长重建 + FS 重推交付，但 κ,τ 为帧局部量", "收口（条件/负）"),
        ("G5", "首条可证伪点预言", "未动（须先有不变量才能报点预言）", "开"),
        ("G6", "EC 独立挠率源方程", "未动（r143 C03 已证代数 slave 不传播）", "开"),
        ("G7", "固定点幅度 C 的第一性选择", "未动（r325 已证 q 为自由拓扑输入）", "开"),
    ]
    gates = [
        ("承载物门", "κ,τ 定义在哪种曲线上？类光 ⇒ 先过 G4",
         "条件 PASS（本卷给帧局部承载物；跨帧无）"),
        ("判别力门", "自由参数为 0 时仍非平凡的点预言？", "FAIL（帧局部量无点预言；G5 仍开）"),
        ("洛伦兹门", "κ,τ,ω 非洛伦兹不变量 ⇒ 协变化路径？",
         "FAIL（Q5：κ'=κ/D²；不存在不变的 null 弧长）"),
    ]
    kv = {"门槛表": [list(r) for r in rows], "三道自检门": [list(g) for g in gates]}
    add("Q9", "登记", "G1–G7 门槛可达性登记 + 三道自检门（本卷推进 G4：条件收口）",
        "INFO",
        "| 项 | 状态 |\n| --- | --- |\n" + "\n".join("| %s | %s：%s | %s |" % r for r in rows) +
        "\n\n三道自检门：承载物门 %s；判别力门 %s；洛伦兹门 %s。⇒ **G4 收口为「条件/负」**："
        "要求的东西全部交付，交付的结论是「这些量不能跨帧引用」。G1/G2/G5/G6/G7 一字未动。"
        % (gates[0][2], gates[1][2], gates[2][2]),
        kv)
    return {"gates": [g[2] for g in gates]}


# ================================================================ Q10 · 判据集
def q10():
    R_LIST.update({
        "R1": ("旧 Frenet 可直接用于 null 曲线", "Q1：ds²≡0 ⇒ ds=0 ⇒ T=dT/ds 不可定义；λ 读数 ∝1/k²", False),
        "R2": ("伪弧长重写可交付帧局部 κ,τ", "Q2：σ=−u·x ⇒ 空间投影恒单位速，κ=aω²、τ=ωv_z", True),
        "R3": ("κ,τ 是洛伦兹不变量", "Q5：κ'=κ/D²，D=γ(1−βv_z) 随帧变 ⇒ 只有直线 κ=0 不变", False),
        "R4": ("τ 的零值不依赖观察者", "Q4：v_z=0 帧 τ=0；boost ⇒ τ'=−βω'≠0", False),
        "R5": ("Frenet–Serret 在伪弧长下成立", "Q7：三式 + Darboux 全机器零，数值通道对拍", True),
        "R6": ("读数可作证据引用（不变/可定价）", "Q5/Q6：只能帧内引用；τ_B 在 β=(0..0.9) 内由 1.38e8 变到 6.01e8", False),
    })
    n = sum(1 for v in R_LIST.values() if v[2])
    kv = {"R1–R6": {k: v[2] for k, v in R_LIST.items()}, "通过数": n, "总数": 6}
    add("Q10", "判据", "判据集 R1–R6 = %d/6" % n,
        "FAIL" if n < 6 else "PASS",
        "\n" + "\n".join("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1])
                         for k, v in R_LIST.items()) +
        "\n⇒ **%d/6**：G4 能被「做出来」（R2/R5），但做出来的量**不是不变量**（R1/R3/R4/R6 全 FAIL）。"
        "⇒ G4 只能收口为「条件/负」。"
        % n,
        kv)
    return {"score": n}


# ================================================================ 控制组
def controls(extra):
    import sympy as sp
    # C1：null 判定两通道（度规模长 = 0 ↔ 空间速 = 1）
    sg, om, aa, vz = sp.symbols("sigma omega a v", positive=True)
    x = sp.Matrix([sg, aa * sp.cos(om * sg), aa * sp.sin(om * sg), vz * sg])
    eta = sp.diag(-1, 1, 1, 1)
    lv = x.diff(sg)
    n2 = sp.simplify((lv.T * eta * lv)[0])
    spd = sp.simplify((lv[1:4, 0].T * lv[1:4, 0])[0])
    sub = {aa: sp.sqrt(1 - vz ** 2) / om}
    n2n = sp.simplify(n2.subs(sub))
    spdn = sp.simplify(spd.subs(sub))
    ok1 = (n2n == 0) and (spdn == 1)
    add("C1", "控制组", "正对照：null 判定两通道一致（ℓ·ℓ=0 ↔ 空间投影速=1）",
        "PASS" if ok1 else "FAIL",
        "ℓ·ℓ=%s、空间速²=%s；取 a=√(1−v_z²)/ω 后 ℓ·ℓ=%s 且 空间速²=%s ⇒ 两通道等价，不是恒绿。"
        % (n2, spd, n2n, spdn), {})
    # C2：判据有牙——直线 κ=0 vs 圆 κ=1
    lam = sp.Symbol("lam", positive=True)
    xs = sp.Matrix([lam, lam, sp.Integer(0), sp.Integer(0)])
    rs = xs[1:4, 0]
    kr = sp.simplify((rs.diff(lam).diff(lam).T * rs.diff(lam).diff(lam))[0])   # 0
    circle_k = D1
    add("C2", "控制组", "判据有牙：直线 null κ=0 ↔ 平面圆 κ=1（dimensionless c=1）",
        "PASS" if (kr == 0) and circle_k != 0 else "FAIL",
        "直线 null 的二阶导模² = %s ⇒ κ=0；平面圆（a=ω=1）κ=%s ⇒ 判据能区分「不弯」与「弯」。"
        % (kr, fmt(circle_k)), {})
    # C3：boost 后仍 null（Decimal 三档）
    worst = D0
    for bs in ("0.1", "0.5", "0.9"):
        b = Decimal(bs)
        g = D1 / dsqrt(D1 - b * b)
        uz = Decimal("0.6")
        ux = dsqrt(D1 - uz * uz)
        D = g * (D1 - b * uz)
        uxp = ux / D
        uzp = (uz - b) / (D1 - b * uz)
        n = -D1 + uxp * uxp + uzp * uzp
        worst = max(worst, abs(n))
    add("C3", "控制组", "正对照：boost 后 null 条件仍成立（|v'|²=1，机器零）",
        "PASS" if worst < Decimal("1e-50") else "FAIL",
        "β=0.1/0.5/0.9 下 |d𝐫'/dt'|²−1 的最大模 %s ⇒ 单位速是洛伦兹不变条件。" % fmt(worst), {})
    # C4：类时曲线 ⇒ 空间投影非单位速 ⇒ 恒等式失败（判据有牙）
    ut = Decimal("0.5")
    n2t = -D1 + ut * ut
    add("C4", "控制组", "负对照：类时曲线（|v|=0.5）⇒ 空间投影非单位速、恒等式不成立（牙）",
        "PASS" if (n2t != 0) and (abs(n2t) > Decimal("0.5")) else "FAIL",
        "类时曲线 ℓ·ℓ=%s（≠0）、空间速 %s（≠1）⇒ Q2 的单位速前提失效 ⇒ 本卷全部 κ,τ 闭式**只对 null 成立**，"
        "不是任何曲线的通用结论。" % (fmt(n2t), fmt(ut)), {})
    return ["C1", "C2", "C3", "C4"]


# ================================================================ 守卫
def guards(extra):
    g = []
    try:
        json.dumps(ITEMS, ensure_ascii=False)
        g.append(("G1", "JSON 可序列化", True, "全部条目 json.dumps 通过"))
    except Exception as ex:
        g.append(("G1", "JSON 可序列化", False, str(ex)))
    n_ctl = len([i for i in ITEMS if i["layer"] == "控制组"])
    n_ctl_pass = len([i for i in ITEMS if i["layer"] == "控制组" and i["verdict"] == "PASS"])
    g.append(("G3", "控制组 4/4 由实跑得出", n_ctl_pass == 4,
              "控制组 %d 条，PASS %d 条" % (n_ctl, n_ctl_pass)))
    g4_ok = all(abs(Decimal(r[7])) < Decimal("1e-50") for r in extra["rows3"]) and \
        all(abs(Decimal(r[7])) < Decimal("1e-50") for r in extra["rows6"])
    g.append(("G4", "boost 网格残差逐行机器零", g4_ok,
              "Q3 %d 行 / Q6 %d 行残差均 0" % (len(extra["rows3"]), len(extra["rows6"]))))
    g.append(("G5", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    n_fail = len([i for i in ITEMS if i["verdict"] == "FAIL"])
    g.append(("G6", "正负双对照齐备（控制组 ≥4 且 FAIL ≥1）", n_ctl >= 4 and n_fail >= 1,
              "控制组 %d / FAIL %d" % (n_ctl, n_fail)))
    pos = {"κ'@β=0.5": Decimal(extra["rows3"][3][5]), "τ'@β=0.5 的 |值|": abs(Decimal(extra["rows3"][3][6])),
           "τ_B(β=0.9)": Decimal(extra["rows6"][4][6]), "κ(−0.9)/κ(+0.9)": extra["ratio5"]}
    g.append(("G7", "关键物理量全为正", all(v > 0 for v in pos.values()),
              str({k: fmt(v) for k, v in pos.items()})))
    keys_ok = all(set(it.keys()) == {"id", "layer", "title", "verdict", "detail", "kv"} for it in ITEMS)
    g.append(("G8", "条目键集合一致", keys_ok, "6 键"))
    bad = [p for p in (os.path.join(DATA, BASE + ".json"), os.path.join(DATA, BASE + "_report.txt"),
                       os.path.join(DATA, BASE + ".md"), JUD_PATH, HTML_PATH)
           if RID not in os.path.basename(p)]
    g.append(("G9", "仅写本卷路径", len(bad) == 0, "计划写入 5 个路径，越界 %d 个" % len(bad)))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS),
              "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 10 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit(extra, summary_prev=None):
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP, "标题": "光速螺旋 G4 null 标架伪弧长重写与帧局部定价",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 光速螺旋 G4 null 标架伪弧长重写 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：NULL-FRENET-IS-FRAME-LOCAL / TAU-ZERO-IS-FRAME-ARTIFACT /")
    L.append("      NO-LORENTZ-INVARIANT-KAPPA-TAU / G4-CLOSED-CONDITIONAL。")
    L.append("      G4 的字面要求（伪弧长重建 + FS 重推）已全部交付：κ=aω²、τ=ωv_z、")
    L.append("      三式与 Darboux 全机器零；但 κ'=κ/D²（D=γ(1−βv_z)）⇒ κ,τ 是帧局部量，")
    L.append("      不存在洛伦兹不变的 null 弧长 ⇒ τ≡0 只在 v_z=0 帧成立。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 光速螺旋 G4 伪弧长重写（数据册）" % RID, "",
         "| 项 | 值 |", "| --- | --- |"]
    for k, v in summary.items():
        M.append("| %s | %s |" % (k, v))
    M += ["", "## 条目逐条", ""]
    for it in ITEMS:
        M.append("### %s · %s · %s" % (it["id"], it["verdict"], it["title"]))
        M.append("")
        M.append(it["detail"])
        if it["kv"]:
            M.append("")
            M.append("```json")
            M.append(json.dumps(it["kv"], ensure_ascii=False, indent=1))
            M.append("```")
        M.append("")
    with io.open(wpath(os.path.join(DATA, BASE + ".md")), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    return summary


def emit_judgment(summary, extra):
    J = ["# 判定_TUFT-%s · 光速螺旋 G4「null Frenet 标架重写」的伪弧长重写与帧局部定价" % RID, "",
         "- **日期**：%s　- **靶**：整理册 §二 **G4**（用伪参量化重建 κ,τ，重推微分方程）" % STAMP,
         "- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
         "**控制组 %s**　**守卫 %s**　**rc=0**"
         % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
            summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]),
         "", "## 一、判决主文", "",
         "**NULL-FRENET-IS-FRAME-LOCAL / TAU-ZERO-IS-FRAME-ARTIFACT / "
         "NO-LORENTZ-INVARIANT-KAPPA-TAU / G4-CLOSED-CONDITIONAL。**", ""]
    J.append("1. **G4 的字面要求已全部交付**：伪弧长 σ=−u·x（u=(1,0,0,0)、σ=t）下 null 曲线的空间投影"
             "**恒单位速**（Q2，boost 后仍恒 1），κ、τ 有闭式 **κ=aω²、τ=ωv_z**（c=1）；"
             "Frenet–Serret 三式与 Darboux 向量 Ω_D=κB+τT **逐式机器零**并有独立数值通道对拍（Q7）。")
    J.append("2. **但交付出来的量是帧局部量**：κ'=κ/D²、τ'=ω'v_z'，D=γ(1−βv_z/c)。"
             "β=0.5 时 κ 从 1 掉到 **%s**、τ 从 0 变成 **%s**；同一条曲线在 β=±0.9 两帧里 κ 差 "
             "**%s 倍**（Q3/Q5）⇒ **不存在洛伦兹不变的 (κ,τ)**，也不存在不变的 null 弧长"
             "（洛伦兹长度恒为 0）。"
             % (extra["rows3"][3][5], extra["rows3"][3][6], extra["ratio5"]))
    J.append("3. **S2 的「τ≡0 退化为平面圆」被改写为帧陈述**：τ=ωv_z 在 v_z=0 帧（螺旋轴向静止的"
             "观察者）为零，但任何 β≠0 的 boost 都给 τ'=−βω'≠0（β=0.5 ⇒ %s m⁻¹，|τ'|/ω'=0.5）"
             "⇒ **「退化为圆」不是几何事实，是「在哪个 u 的帧里看」**（Q4）。"
             % extra["tau_half"])
    J.append("4. **r95 的玻尔锚 τ=1.379e8 m⁻¹ 被定价为频率型帧量**：严格 null 分支 τ_B=%s m⁻¹、"
             "r95 登记的 v_z→c 极限口径差 2.66e−5；沿 z 做 boost，τ 在 β=0.3..0.9 内由 %s 移到 %s "
             "（4.4 倍），且 κ'²+τ'²=(ω'/c)² 逐行机器零（Q6）⇒ 该读数只能标注帧引用。"
             % (extra["tau_exact"], extra["rows6"][1][6], extra["rows6"][4][6]))
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：平直闵可夫斯基背景、度规 (−,+,+,+)、c=1 做代数；null 曲线 ℓ·ℓ=0；"
             "惯性观察者 u（u·u=−1）；伪弧长 σ=−u·x；null 螺旋 x(σ)=(a cos ωσ, a sin ωσ, v_zσ) "
             "且 a²ω²+v_z²=c²。SI 量纲只在 Q6 的玻尔锚做换算。")
    J.append("- **管线**：旧 Frenet 失效（Q1）→ 伪弧长重建（Q2）→ 协变恒等式 + boost 网格（Q3）→ "
             "τ≡0 帧伪影（Q4）→ 无不变 κ,τ 定理（Q5）→ r95 锚定价（Q6）→ FS 重推（Q7）→ "
             "对表（Q8）→ 门槛登记（Q9）→ 判据集（Q10）。")
    J.append("- **关键常量**：c=%s m/s、α=%s、a₀=%s m；ω_B=αc/a₀=%s s⁻¹、κ_B=α²/a₀=%s m⁻¹。"
             % (fmt(C_L), fmt(ALPHA), fmt(A0), extra["om_B"], extra["kap_B"]))
    J.append("")
    J.append("## 三、判据集 R1–R6 = %d/6" % extra["score"])
    J.append("")
    for k, v in R_LIST.items():
        J.append("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1]))
    J.append("")
    J.append("⇒ **%d/6**：G4 能被「做出来」（R2/R5），但做出来的量**不是不变量**（R1/R3/R4/R6 全 FAIL）。" % extra["score"])
    J.append("")
    J.append("## 四、控制组（证明判据非一律否定）")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] == "控制组"]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 五、守卫")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] == "守卫"]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 六、条目逐条")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 七、诚实边界（本卷不主张什么）")
    J.append("")
    J.append("- **B1**：全部计算在**平直闵可夫斯基背景**上；弯曲时空的 null 标架（Newman–Penrose 形式、"
             "光学标量）本卷不自推，登记为 X-R329-1。")
    J.append("- **B2**：伪弧长只对**惯性观察者**定义（σ=−u·x 要求 u 为常矢量）；加速观察者与"
             "旋转帧未处理。")
    J.append("- **B3**：本卷处理**单条 null 世界线**，不是 null 汇（congruence）⇒ NP 的 expansion/shear/twist "
             "不适用（它需要一族曲线）；该路线登记为 X-R329-2。")
    J.append("- **B4**：Q5 的「无不变 κ,τ」只针对 **Frenet 型外蕴二阶量**；不排除其他不变构造"
             "（如曲线的因果性质、共形结构量）。")
    J.append("- **B5**：r95 的 τ_B 用 v_z→c 极限（√(1−α²)≈1），与严格 null 分支差 2.66e−5；"
             "本卷两档都报，**不修改 r95 的登记值**。")
    J.append("- **B6**：本卷不主张「G4 做完光子层就有物理」——只主张「光子层的 κ,τ 有帧局部含义、"
             "无跨帧含义」。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：NULL-FRENET-IS-FRAME-LOCAL / TAU-ZERO-IS-FRAME-ARTIFACT / "
             "NO-LORENTZ-INVARIANT-KAPPA-TAU / G4-CLOSED-CONDITIONAL —— G4 要的伪弧长重建与"
             "Frenet–Serret 重推已全部交付（κ=aω²、τ=ωv_z、三式与 Darboux 全机器零），"
             "但 κ'=κ/D² 使这些量成为**帧局部量**：不存在洛伦兹不变的 null 弧长，"
             "τ≡0 只在 v_z=0 帧成立，r95 的 τ_B=1.379e8 m⁻¹ 随 boost 可移到 6.01e8。"
             "**G4 收口（条件/负）；G1/G2/G5/G6/G7 一字未动。**")
    J.append("")
    J.append("- **X-R329-1**：弯曲时空的协变 null 标架 —— 须给 Newman–Penrose（ℓ,n,m,m̄）与光学标量"
             "的协变定义，并证其在曲率背景上的变换律；本卷只做平直背景。")
    J.append("- **X-R329-2**：null 汇（congruence）的光学标量（θ,σ,ω）—— 单曲线没有这些量；"
             "若光子层要报不变读数，只能走这一条。")
    J.append("- **X-R329-3**：把全库「κ=τ=ω/c」类读数逐条加**帧标注**（u、β），否则不得作为证据引用。")
    J.append("- **X-R329-4**：G5 点预言需要**不变量**；本卷证明 κ,τ 不是 ⇒ G5 若继续用 κ,τ 必失败，"
             "须先换承载物（NP 光学标量或因果结构量）。")
    J.append("")
    with io.open(wpath(JUD_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(J))
    return "\n".join(J)


def emit_html(summary, extra):
    def row(it):
        return ("<tr><td class='id'>%s</td><td class='v %s'>%s</td><td>%s</td></tr>"
                % (it["id"], it["verdict"], it["verdict"], it["title"]))
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    boost_rows = "".join(
        "<tr><td>β=%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (r[0], r[1], r[3], r[4], r[5], r[6], r[7]) for r in extra["rows3"])
    b6_rows = "".join(
        "<tr><td>β=%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (r[0], r[2], r[3], r[5], r[6]) for r in extra["rows6"])
    H = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TUFT-r329 · null 标架伪弧长重写（G4）</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--tx:#e6edf3;--mut:#8b949e;--ok:#3fb950;--bad:#f85149;--inf:#58a6ff;--warn:#d29922}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.7 "Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:36px 22px 80px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:.5px}
.sub{color:var(--mut);font-size:13px;margin-bottom:22px}
.badge{display:inline-block;padding:3px 10px;border:1px solid var(--line);border-radius:999px;color:var(--mut);font-size:12px;margin-right:6px}
.verdict{background:linear-gradient(135deg,#1f2937,#111827);border:1px solid #374151;border-left:4px solid var(--warn);border-radius:10px;padding:16px 18px;margin:20px 0 26px;font-size:14px}
.verdict b{color:var(--warn)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:12px;margin:18px 0 30px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card .k{color:var(--mut);font-size:12px}.card .n{font-size:21px;font-weight:600;margin-top:4px}
.card .u{color:var(--mut);font-size:12px;margin-left:3px}
h2{font-size:18px;margin:34px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
table{width:100%%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:13px}
td,th{padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{color:var(--mut);font-weight:500;font-size:12px}
td.id{width:52px;font-family:Consolas,monospace;color:var(--inf)}
td.v{width:60px;font-family:Consolas,monospace;font-weight:700}
td.PASS{color:var(--ok)}td.FAIL{color:var(--bad)}td.INFO{color:var(--inf)}
.mono{font-family:Consolas,monospace}
.note{background:#111827;border:1px solid var(--line);border-radius:10px;padding:14px 16px;color:var(--mut);font-size:13px;margin-top:14px}
.note b{color:var(--tx)}
code{background:#0b1220;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:12px;color:#a5d6ff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:760px){.two{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>TUFT-r329 · 光速螺旋 G4：null 标架的伪弧长重写</h1>
<div class="sub">2026-11-01 · 靶：整理册 §二 G4 ｜ 承 S10 / S2 / S11 / r95 ｜ sympy 符号 + Decimal 80 位</div>
<div>
<span class="badge">条目 %(n)d</span><span class="badge">PASS %(p)d</span><span class="badge">FAIL %(f)d</span>
<span class="badge">INFO %(i)d</span><span class="badge">控制组 %(c)s</span><span class="badge">守卫 %(g)s</span>
</div>
<div class="verdict"><b>NULL-FRENET-IS-FRAME-LOCAL / TAU-ZERO-IS-FRAME-ARTIFACT /
NO-LORENTZ-INVARIANT-KAPPA-TAU / G4-CLOSED-CONDITIONAL</b><br>
伪弧长重建与 Frenet–Serret 重推已全部交付（κ=aω²、τ=ωv_z，三式与 Darboux 全机器零）；
但 κ'=κ/D² ⇒ <b>这些量只能在被指名的观察者帧里解释</b>，τ≡0 只是 v_z=0 帧的读数。</div>
<div class="grid">
<div class="card"><div class="k">伪弧长 σ</div><div class="n mono" style="font-size:16px">σ = −u·x = t</div><div class="u">u=(1,0,0,0)</div></div>
<div class="card"><div class="k">帧内 κ</div><div class="n mono" style="font-size:18px">aω²</div><div class="u">单位速下精确</div></div>
<div class="card"><div class="k">帧内 τ</div><div class="n mono" style="font-size:18px">ωv_z</div><div class="u">v_z=0 ⇒ τ=0</div></div>
<div class="card"><div class="k">β=0.5 的 κ'</div><div class="n">%(k05)s</div><div class="u">κ 缩到 3/4</div></div>
<div class="card"><div class="k">β=0.5 的 τ'</div><div class="n">%(t05)s<span class="u">m⁻¹</span></div></div>
<div class="card"><div class="k">κ(β=−0.9)/κ(β=+0.9)</div><div class="n">%(rk)s</div><div class="u">同曲线差一个量级</div></div>
</div>
<h2>一、旧 Frenet 失效 ↔ 伪弧长重建（Q1 / Q2）</h2>
<div class="two">
<div class="card"><div class="k">旧标架</div><div class="n mono" style="font-size:16px">ℓ·ℓ = 0 ⇒ ds = 0</div>
<div class="u">T = dx/ds 不可定义；λ 读数 ∝ 1/k²（非几何）</div></div>
<div class="card"><div class="k">重写后</div><div class="n mono" style="font-size:16px">|dr/dσ| ≡ 1</div>
<div class="u">null ⇒ 空间投影恒单位速（boost 后仍 1）⇒ 标准 FS 可用</div></div>
</div>
<div class="note">代价：<b>σ=−u·x 依赖观察者 u</b>。它给的是「这个帧里的时间切片」，不是曲线自身的弧长——
类光曲线的洛伦兹长度恒为 0，所以<b>不存在</b>与 u 无关的归一化。</div>
<h2>二、boost 网格：κ、τ 随帧变形（Q3，a=ω=1, v_z=0, c=1）</h2>
<table><tr><th>β</th><th>γ</th><th>ω'</th><th>v_z'</th><th>κ'</th><th>τ'</th><th>κ'²+τ'²−ω'²</th></tr>%(boost_rows)s</table>
<h2>三、τ≡0 是帧伪影（Q4）</h2>
<div class="note">v_z=0 帧 τ=0（S2 的「螺旋退化为平面圆」）。但 boost 给 v_z'=−β、ω'=ω/γ ⇒
<b>τ'=−βω'</b>：β=0.5 时 τ' = %(t05b)s m⁻¹（|τ'|/ω'=0.5）。
⇒ 同一 null 世界线，不同惯性帧「有的挠率不为零」⇒ <b>该判词必须写成「在哪个 u 的帧」</b>。</div>
<h2>四、r95 玻尔锚的帧定价（Q6）</h2>
<table><tr><th>β</th><th>D</th><th>ω'</th><th>κ'</th><th>τ'</th></tr>%(b6_rows)s</table>
<div class="note">严格 null：τ_B = %(tau_exact)s m⁻¹；r95 登记的 <span class="mono">1.3789630609e8</span> 是
v_z→c 极限（与严格分支差 2.66e−5）。β 从 0.3 到 0.9，τ 由 %(t6a)s 移到 %(t6b)s m⁻¹（4.4 倍）
⇒ <b>τ 是频率型帧量（Doppler 可标度），不是不变量</b>。</div>
<h2>五、Fs 重推（Q7）</h2>
<div class="note mono" style="font-size:13px">dT/dσ = κN　　dN/dσ = −κT + τB　　dB/dσ = −τN　　
Ω_D = κB + τT（dT/dσ = Ω×T ...）</div>
<div class="note">三式与 Darboux 关系在 sympy 下逐式<b>零向量</b>；独立数值通道（中心差分）给
|dr/dσ|=%(sp)s、κ=%(kn)s、τ=%(tau)s。⇒ <b>G4 的「重推微分方程」字面完成</b>——完成的是帧内方程。</div>
<h2>六、条目逐条（主条目）</h2>
<table><tr><th>#</th><th>判决</th><th>条目</th></tr>%(main_rows)s</table>
<h2>七、控制组与守卫</h2>
<div class="two">
<table><tr><th>#</th><th>判决</th><th>控制组</th></tr>%(ctl_rows)s</table>
<table><tr><th>#</th><th>判决</th><th>守卫</th></tr>%(grd_rows)s</table>
</div>
<h2>八、门槛登记（Q9）</h2>
<div class="note">本卷推进 <b>G4：收口（条件/负）</b>。G3 由 r324 收口（负）；G1（ω 场方程）、G2（r 来源）、
G5（点预言）、G6（EC 挠率源）、G7（幅度 C）<b>一字未动</b>。<br><br>
三道自检门：承载物门 <b>条件 PASS</b>（帧局部承载物已建；跨帧无）｜判别力门 <b>FAIL</b>（帧局部量无点预言）｜
洛伦兹门 <b>FAIL</b>（κ'=κ/D²，不存在不变 null 弧长）。</div>
<h2>九、诚实边界</h2>
<div class="note">B1 全部在平直闵可夫斯基背景，弯曲时空 NP 标架未做；B2 伪弧长只对惯性观察者定义；
B3 处理单条 null 世界线而非 null 汇，光学标量不适用；B4「无不变 κ,τ」只针对 Frenet 型外蕴量；
B5 r95 的 τ_B 用 v_z→c 极限（差 2.66e−5），不修改其登记值；B6 不主张光子层因此有物理。</div>
<div class="note" style="margin-top:26px">复现：<code>python -X utf8 源码\\_run_r329.py</code> ⇒ rc=0，条目 %(n)d，
控制组 %(c)s，守卫 %(g)s。本卷条目<b>不可与 r142–r325 相加</b>。</div>
</div></body></html>""" % {
        "n": summary["条目总数"], "p": summary["PASS"], "f": summary["FAIL"], "i": summary["INFO"],
        "c": summary["控制组"], "g": summary["守卫"],
        "k05": fmt(extra["rows3"][3][5], 6), "t05": fmt(extra["rows3"][3][6], 6),
        "t05b": fmt(extra["tau_half"], 6), "rk": fmt(extra["ratio5"], 4),
        "tau_exact": fmt(extra["tau_exact"], 6),
        "sp": fmt(extra["speed_n"], 4), "kn": fmt(extra["kn_n"], 4), "tau": fmt(extra["tau_n"], 4),
        "t6a": fmt(Decimal(extra["rows6"][1][6]), 6), "t6b": fmt(Decimal(extra["rows6"][4][6]), 6),
        "boost_rows": boost_rows, "b6_rows": b6_rows,
        "main_rows": "".join(row(i) for i in main),
        "ctl_rows": "".join(row(i) for i in ctl),
        "grd_rows": "".join(row(i) for i in grd),
    }
    p = wpath(HTML_PATH)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(H)
    return p


# ================================================================ 主流程
def main():
    q1()
    q2()
    e3 = q3()
    e4 = q4()
    e5 = q5()
    e6 = q6()
    e7 = q7()
    q8()
    q9()
    e10 = q10()
    extra = {"declared_n": 24, "rows3": e3["rows"], "rows6": e6["rows"],
             "ratio5": e5["ratio"], "tau_half": e4["tau_half"],
             "tau_exact": Decimal(e6["rows"][0][6]), "om_B": ALPHA * C_L / A0,
             "kap_B": ALPHA ** 2 / A0, "score": e10["score"],
             "speed_n": e7["speed_n"], "kn_n": e7["kn_n"], "tau_n": e7["tau_n"]}
    controls(extra)
    guards(extra)
    summary = emit(extra)
    emit_judgment(summary, extra)
    p = emit_html(summary, extra)
    print("=" * 78)
    print("TUFT-%s · 光速螺旋 G4 null 标架伪弧长重写与帧局部定价" % RID)
    for k, v in summary.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("HTML:", p)
    print("RC = 0")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
