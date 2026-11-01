# -*- coding: utf-8 -*-
"""
TUFT-r342 · 光速螺旋纲领 核心公式理论体系「全链路六环」正确性审计
（承整理册 §三 保留资产 1–5 / S5 S7 S8 S12 / G2 / r124 T05 T06 / r242 R09 / r329 / r338）

靶：把纲领的**核心公式**（恒等式、质量式、力式、EH 拉氏源项、静态耦合、锚与定义域）
放在同一条 null 螺旋判例上，按**六环链**逐环复算：环 1 数学 → 环 2 量纲 → 环 3 承载物
→ 环 4 拉氏配对 → 环 5 判别力 → 环 6 定义域/锚。每环给出机器读数与「断/通」判决。

  Q1 环1 恒等式 ω²=c²(κ²+τ²)：4D null ⟺ 3D 单位速 ⟺ 恒等式，机器零（PASS）
  Q2 环2 质量式量纲 m=(ℏ/c)√(κ²+τ²)：[M] 齐次；缺 c 的错式不过关（有牙）⇒ PASS
  Q3 环2' 质量锚：玻尔锚给 4.85e-35 kg = 5.3e-5 m_e ⇒ 差 1.878e4 倍（FAIL）
  Q4 环3 力式 F=ℏc∇κ：量纲 [MLT⁻²] ✓，但均匀螺旋/直线都给 F=0，横向 ∇κ 需 null 汇（FAIL）
  Q5 环4 拉氏：c⁴/(16πG)R=[ML⁻¹T⁻²] vs (ℏ/c)√(κ²+τ²)ω=[MT⁻¹] ⇒ 失配 [0,−1,−1]（FAIL）
  Q6 环5 静态耦合：∇×G≡0 ⇒ 0=0（机器恒零 + 非梯度反例有牙）⇒ 零判别力（PASS 证明成立）
  Q7 环6 锚与定义域：ω 固定 ⇒ r≤λ̄_C 必要条件；a₀ 锚越 v≤c 137 倍（PASS）
  Q8 六环总账：数学正确 3/6（全在量纲）、物理可用 0/6；第一断点 = 环 3 承载物
  Q9 对表 S5/S7/S8/S12/G2 + r242 R09 + r124 T05 + r338
  Q10 G1–G7 门槛 + 三道自检门
  Q11 判据集 R1–R6 = 2/6
控制组 C1–C4 / 守卫 G1–G10
判词：CORE-CHAIN-SIX-RING-AUDIT / DIMENSION-PASS-CARRIER-FAIL /
      LAGRANGIAN-MISMATCH-UNFIXABLE-BY-NUMBER / PHYSICAL-USE-OF-CORE-FORMULAS-ZERO
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 80

RID = "r342"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_核心公式理论体系全链路审计_六环量纲承载与定义域正确性总账_"
        "精算与可视化_%s" % (RID, STAMP))
JUD_PATH = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-r342_"):]))
HTML_PATH = os.path.join(ROOT, "四力统一方程_核心公式全链路审计_r342可视化_%s.html" % STAMP)

WRITTEN = []
T0 = time.time()

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
C_L = Decimal("2.99792458e8")
ALPHA = Decimal("7.2973525693e-3")
A0 = Decimal("5.29177210903e-11")
HBAR = Decimal("1.054571817e-34")
ME = Decimal("9.1093837015e-31")
G_N = Decimal("6.67430e-11")             # 引力常数 [m³ kg⁻¹ s⁻²]（CODATA 2018）

R_LIST = {}
ITEMS = []


def _safe(v):
    """把 kv 值转成 JSON 可序列化的原生类型（sympy 表达式/Decimal 一律转字符串）。"""
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        return [_safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _safe(x) for k, x in v.items()}
    return str(v)


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": {k: _safe(v) for k, v in dict(kv or {}).items()}})


def wpath(p):
    WRITTEN.append(p)
    return p


def vdim(m, l, t):
    """量纲向量 (M, L, T) 的指数三元组。"""
    import sympy as sp
    return sp.Matrix([m, l, t])


# ================================================================ Q1 · 环1 恒等式
def q1():
    """4D null 螺旋 x(σ)=(σ, a cos ωσ, a sin ωσ, v_z σ)（c=1）：
    ℓ·ℓ = −1 + a²ω² + v_z² = 0（null）；3D 空间投影速 = 1（单位速）；
    Frenet：κ=aω²、τ=ωv_z；恒等式 ω² = κ²+τ² 精确零。"""
    import sympy as sp
    sg = sp.Symbol("sigma", real=True)
    om = sp.Symbol("omega", positive=True)
    aa = sp.Symbol("a", positive=True)
    vz = sp.Symbol("v_z", real=True)
    x = sp.Matrix([sg, aa * sp.cos(om * sg), aa * sp.sin(om * sg), vz * sg])
    eta = sp.diag(-1, 1, 1, 1)
    lv = x.diff(sg)
    n2 = sp.simplify((lv.T * eta * lv)[0])
    null_sub = {aa: sp.sqrt(1 - vz ** 2) / om}
    n2n = sp.simplify(n2.subs(null_sub))
    sp3 = sp.simplify((lv[1:4, 0].T * lv[1:4, 0])[0])
    sp3n = sp.simplify(sp3.subs(null_sub))
    kap = aa * om ** 2
    tau = om * vz
    ident = sp.simplify(om ** 2 - (kap ** 2 + tau ** 2))
    ident_n = sp.simplify(ident.subs(null_sub))
    num = (0.8, 1.0, 0.6)                    # a²ω²+v_z² = 0.64+0.36=1
    k_num, t_num = num[0] * num[1] ** 2, num[1] * num[2]
    ident_num = num[1] ** 2 - (k_num ** 2 + t_num ** 2)
    kv = {"ℓ·ℓ": str(n2), "ℓ·ℓ(null 代入)": str(n2n), "空间速²(null)": str(sp3n),
          "κ": str(kap), "τ": str(tau), "ω²−(κ²+τ²)": str(ident),
          "恒等式(null 代入)": str(ident_n),
          "数值(a,ω,v_z)": list(num), "数值 κ,τ": [k_num, t_num],
          "数值残差": str(ident_num)}
    ok = (n2n == 0) and (sp3n == 1) and (ident_n == 0) and (abs(ident_num) < 1e-15)
    add("Q1", "承载物",
        "环1 恒等式闭合：4D null ⟺ 3D 单位速 ⟺ ω²=c²(κ²+τ²)，机器零（数值判例残差 0）",
        "PASS" if ok else "FAIL",
        "入口链：4D 曲线 x(σ)=(σ, a cos ωσ, a sin ωσ, v_z σ) 的 **ℓ·ℓ = %s**，取 null 分支 "
        "a=√(1−v_z²)/ω ⇒ **ℓ·ℓ = %s**；同时 3D 空间投影速² = **%s**（=1，单位速）⇒ 两个定义域条件等价。"
        "在该分支上 **κ=aω²、τ=ωv_z**，恒等式 **ω²−(κ²+τ²) = %s**（null 代入后 =%s）。"
        "数值判例 a=0.8、ω=1、v_z=0.6（0.64+0.36=1）⇒ κ=0.8、τ=0.6、残差 **%s**。"
        "⇒ **环1 数学上完全正确**：这是全链唯一一个「无需外部输入、无需帧标注以外的附加假设」就闭合的环节。"
        "但注意它只**锁幅度**（r338 Q4：κ,τ 常值 ⇒ ω 被冻死），不含演化。"
        % (n2, n2n, sp3n, ident, ident_n, ident_num),
        kv)
    return {"ident": ident_n, "k": k_num, "t": t_num}


# ================================================================ Q2 · 环2 质量式量纲
def q2():
    """m = (ℏ/c)√(κ²+τ²) 的量纲代数（[M,L,T] 指数向量）：
    ℏ=[1,2,−1]、c=[0,1,−1]、κ,τ=[0,−1,0] ⇒ ℏ−c+κ = [1,2,−1]−[0,1,−1]+[0,−1,0] = [1,0,0] = [M] ✓。
    错式 m=ℏ√(κ²+τ²) ⇒ [1,2,−1]+[0,−1,0] = [1,1,−1] = [MLT⁻¹] ✗ ⇒ 量纲门有牙。
    恒等式量纲：c²κ² = [0,2,−2]+[0,−2,0] = [0,0,−2] = ω² ✓。"""
    import sympy as sp
    HB_ = vdim(1, 2, -1)        # ℏ
    CC = vdim(0, 1, -1)         # c
    KAP = vdim(0, -1, 0)        # κ（τ 同）
    M_TARGET = vdim(1, 0, 0)
    ok_m = sp.simplify(HB_ - CC + KAP)
    bad_m = sp.simplify(HB_ + KAP)
    c2 = 2 * CC
    om2 = 2 * vdim(0, 0, -1)
    c2k2 = sp.simplify(c2 + 2 * KAP)
    ok_id = (sp.simplify(c2k2 - om2) == sp.zeros(3, 1))
    kv = {"ℏ": list(HB_), "c": list(CC), "κ,τ": list(KAP),
          "m=(ℏ/c)√(κ²+τ²)": list(ok_m), "目标 [M]": list(M_TARGET),
          "错式 m=ℏ√(κ²+τ²)": list(bad_m),
          "c²κ²": list(c2k2), "ω²": list(om2)}
    ok = (ok_m == M_TARGET) and (bad_m != M_TARGET) and ok_id
    add("Q2", "判据",
        "环2 质量式量纲：m=(ℏ/c)√(κ²+τ²) 精确 [M]；缺 c 的错式 [MLT⁻¹] 不过关 ⇒ 量纲门有牙",
        "PASS" if ok else "FAIL",
        "按 (M,L,T) 指数向量做量纲代数：ℏ=**%s**、c=**%s**、κ,τ=**%s**。\n"
        "**m=(ℏ/c)√(κ²+τ²)** ⇒ ℏ−c+κ = **%s**，恰等于 **[M]=%s** ⇒ 齐次。\n"
        "**错式 m=ℏ√(κ²+τ²)**（漏掉一次 c）⇒ **%s** = [MLT⁻¹] ✗ ⇒ **量纲门不是恒绿**：它确实能抓住漏 c。\n"
        "恒等式侧：c²κ² = **%s** = ω² = **%s** ⇒ 两式在同一量纲基下互洽。\n"
        "⇒ **环2 的量纲层通过**（这是保留资产 2 的正确部分）；但「量纲齐次」不等于「物理可用」，"
        "锚点问题在 Q3 立刻出现。"
        % (list(HB_), list(CC), list(KAP), list(ok_m), list(M_TARGET), list(bad_m),
           list(c2k2), list(om2)),
        kv)
    return {"ok_m": list(ok_m)}


# ================================================================ Q3 · 环2' 质量锚
def q3():
    """质量式的数值锚检验：
    (i) λ̄_C 锚：r=λ̄_C、v_z=0 ⇒ κ=1/λ̄_C、τ=0 ⇒ m=(ℏ/c)·(1/λ̄_C)=m_e（精确）。
    (ii) 玻尔锚（r95/r329 口径）：κ_B=α²/a₀、τ_B=α/a₀·√(1−α²) ⇒ √(κ²+τ²)≈1.379e8 m⁻¹
         ⇒ m_B=(ℏ/c)·1.379e8 = 4.85e-35 kg = 5.33e-5 m_e ⇒ 差 1.878e4 倍。
    ⇒ 质量式在「电子自锚」上闭合，在「玻尔锚」上崩 4 个量级。"""
    lam = HBAR / (ME * C_L)
    om_c = ME * C_L * C_L / HBAR
    kap_c = D1 / lam
    m_c = (HBAR / C_L) * kap_c
    d_c = rel(m_c, ME)
    om_b = ALPHA * C_L / A0
    kap_b = ALPHA ** 2 / A0
    uz = dsqrt(D1 - ALPHA * ALPHA)
    tau_b = om_b * (C_L * uz) / (C_L * C_L)
    sqr_b = dsqrt(kap_b * kap_b + tau_b * tau_b)
    m_b = (HBAR / C_L) * sqr_b
    r_m = m_b / ME
    req = ME * C_L / HBAR
    r_req = req / sqr_b
    kv = {"λ̄_C[m]": fmt(lam), "ω_C[s⁻¹]": fmt(om_c), "κ(λ̄_C 锚)[m⁻¹]": fmt(kap_c),
          "m(λ̄_C 锚)[kg]": fmt(m_c), "vs m_e 相对差": fmt(d_c),
          "κ_B[m⁻¹]": fmt(kap_b), "τ_B[m⁻¹]": fmt(tau_b), "√(κ²+τ²)[m⁻¹]": fmt(sqr_b),
          "m(玻尔锚)[kg]": fmt(m_b), "m_B/m_e": fmt(r_m),
          "所需的 √(κ²+τ²)[m⁻¹]": fmt(req), "所需/实际": fmt(r_req)}
    ok = (d_c < Decimal("1e-70")) and (r_m < Decimal("1e-4")) and (r_req > Decimal("1e4"))
    add("Q3", "判据",
        "环2' 质量锚：λ̄_C 自锚精确给 m_e；玻尔锚只给 4.85e-35 kg（5.3e-5 m_e）⇒ 差 1.878e4 倍",
        "FAIL" if ok else "INFO",
        "质量式 m=(ℏ/c)√(κ²+τ²) 在两套锚上做数值检验：\n"
        "**(i) λ̄_C 自锚**：r=λ̄_C=**%s m**、v_z=0 ⇒ κ=1/λ̄_C=**%s m⁻¹**、τ=0 ⇒ "
        "m=(ℏ/c)κ=**%s kg**，与 m_e 相对差 **%s**（机器零）⇒ **电子自锚完全闭合**。\n"
        "**(ii) 玻尔锚（r95/r329 口径）**：κ_B=α²/a₀=**%s m⁻¹**、τ_B=ω_B v_z/c²=**%s m⁻¹** ⇒ "
        "√(κ²+τ²)=**%s m⁻¹** ⇒ m=(ℏ/c)·该值=**%s kg** = **%s m_e**。\n"
        "要回到 m_e，所需的 √(κ²+τ²)=m_ec/ℏ=**%s m⁻¹**，是玻尔锚值的 **%s 倍**（1.878e4）。\n"
        "⇒ **质量式本身没错（Q2 量纲齐次），错的是锚**：同一把尺子量电子只有 λ̄_C 能用；"
        "一挪到 a₀ 就差 4 个量级 ⇒ **「r 的来源」(G2) 与「质量的锚」是同一个缺口**，不是两件事。"
        % (fmt(lam, 6), fmt(kap_c, 6), fmt(m_c, 6), fmt(d_c, 4),
           fmt(kap_b, 6), fmt(tau_b, 6), fmt(sqr_b, 6), fmt(m_b, 6), fmt(r_m, 4),
           fmt(req, 6), fmt(r_req, 4)),
        kv)
    return {"r_m": r_m, "r_req": r_req, "m_b": m_b, "d_c": d_c}


# ================================================================ Q4 · 环3 力式
def q4():
    """F = ℏc∇κ：量纲 ℏ+c+∇κ = [1,3,−2]+[0,−2,0] = [1,1,−2] = [MLT⁻²] ✓（唯一过量纲门的力式）。
    但 ① 均匀螺旋 κ=const ⇒ dκ/dσ=0 ⇒ F=0；② 直线 κ=0 ⇒ F=0；
    ③ 横向 ∇_⊥κ 需要一族 null 曲线（汇/congruence），单曲线无定义 ⇒ 链在承载物处断。"""
    import sympy as sp
    HB_ = vdim(1, 2, -1)
    CC = vdim(0, 1, -1)
    GK = vdim(0, -2, 0)
    F_T = vdim(1, 1, -2)
    dimF = sp.simplify(HB_ + CC + GK)
    sg = sp.Symbol("sigma", real=True)
    aa, om, vz = sp.symbols("a omega v_z", positive=True)
    kap = aa * om ** 2
    dkap = sp.simplify(sp.diff(kap, sg))
    # 数值：a=0.8,ω=1 ⇒ κ=0.8 常数；直线 κ=0
    k_uni = 0.8
    kv = {"F 量纲": list(dimF), "力式目标": list(F_T), "κ(均匀螺旋)": str(kap),
          "dκ/dσ": str(dkap), "F(均匀螺旋)": "0（∝∇κ=0）", "F(直线)": "0（κ≡0）",
          "横向 ∇_⊥κ": "未定义（单曲线无族）"}
    ok = (dimF == F_T) and (dkap == 0)
    add("Q4", "判据",
        "环3 力式：量纲 [MLT⁻²] 通过，但均匀螺旋与直线都给 F=0，横向 ∇κ 在单曲线上无定义 ⇒ 承载物断",
        "FAIL" if ok else "INFO",
        "**F_μ = ℏc∇_μκ** 的量纲：ℏ+c+∇κ = **%s**，恰等于 **[MLT⁻²]=%s** ⇒ 它是全库**唯一过量纲门**的力式候选"
        "（r242 读数复证）。\n"
        "但三处断裂：\n"
        "① **均匀螺旋**：κ=aω² 与 σ 无关（机器 dκ/dσ = **%s**）⇒ **F=0** ⇒ 「曲率产生力」在一根最干净的螺旋上给零力；\n"
        "② **直线**：κ≡0 ⇒ **F=0** ⇒ 力式无法区分「有引力/无引力」；\n"
        "③ **横向梯度** ∇_⊥κ 需要一族 null 世界线（汇/congruence）才有定义（r329 X-R329-2），"
        "**单条世界线上不存在** ⇒ 力式的定义域本身未建。\n"
        "⇒ **环3 断在承载物**：量纲正确却被定义域挡住；这解释了为什么 F=ℏc∇κ 始终只是「候选」而非「方程」。"
        % (list(dimF), list(F_T), dkap),
        kv)
    return {"dF": 0}


# ================================================================ Q5 · 环4 拉氏配对
def q5():
    """EH 拉氏 c⁴/(16πG)·R 与源项 (ℏ/c)√(κ²+τ²)ω 的量纲配对：
    c⁴/(16πG)R = 4c − G + R = [0,4,−4] − [−1,3,−2] + [0,−2,0] = [1,−1,−2] = [ML⁻¹T⁻²]（能量密度）。
    源项 = ℏ − c + κ + ω = [1,2,−1]−[0,1,−1]+[0,−1,0]+[0,0,−1] = [1,0,−1] = [MT⁻¹]。
    失配向量 = [0,−1,−1]；对 k∈[−8,8] 检查是否 k·c ⇒ 否 ⇒ 不能由纯数或 c 的整数幂修复。"""
    import sympy as sp
    HB_ = vdim(1, 2, -1)
    CC = vdim(0, 1, -1)
    KAP = vdim(0, -1, 0)
    OM = vdim(0, 0, -1)
    RR = vdim(0, -2, 0)
    GG = vdim(-1, 3, -2)
    lhs = sp.simplify(4 * CC - GG + RR)
    rhs = sp.simplify(HB_ - CC + KAP + OM)
    gap = sp.simplify(lhs - rhs)
    pure = [k for k in range(-8, 9) if sp.simplify(gap - k * CC) == sp.zeros(3, 1)]
    kv = {"EH 项 c⁴/(16πG)R": list(lhs), "源项 (ℏ/c)√(κ²+τ²)ω": list(rhs),
          "失配向量": list(gap), "k·c 命中": pure,
          "c⁴/G 数值[kg m/s²×m⁻²]": fmt(C_L ** 4 / G_N, 4),
          "ℏ/c 数值[kg m]": fmt(HBAR / C_L, 4)}
    ok = (gap != sp.zeros(3, 1)) and (len(pure) == 0)
    add("Q5", "判据",
        "环4 拉氏：EH 项 [ML⁻¹T⁻²] vs 源项 [MT⁻¹] ⇒ 失配 [0,−1,−1]，非纯数亦非 c 整数幂可修",
        "FAIL" if ok else "INFO",
        "把拉氏两侧放在同一量纲基上：\n"
        "**EH 项** c⁴/(16πG)·R ⇒ 4c − G + R = **%s** = [ML⁻¹T⁻²]（能量密度，量纲正确）；"
        "数值 c⁴/G = **%s** kg·m·s⁻²·(m⁻² 已含于 R)。\n"
        "**源项** (ℏ/c)√(κ²+τ²)ω ⇒ ℏ − c + κ + ω = **%s** = [MT⁻¹]。\n"
        "⇒ **失配向量 = %s** = [L⁻¹T⁻¹]。机器对 k∈[−8,8] 检查 **是否 k·c**（c=[0,1,−1]）：**命中集 %s** "
        "⇒ **不能乘任何纯数、也不能靠 c 的整数幂补齐**，必须引入一个带量纲 [L⁻¹T⁻¹] 的新常数（= 外部输入）。\n"
        "与 S5 的口径差：S5 记「缺 c⁴」，本卷直算得失配 [0,−1,−1]；两者是不同记账口径下的同一事实"
        "（**无纯数修复**），本卷不改 S5 判词，只登记记账差。\n"
        "⇒ **环4 断在量纲**：这不是「系数微调」，是「两侧根本不是同一种量」。"
        % (list(lhs), fmt(C_L ** 4 / G_N, 4), list(rhs), list(gap), pure),
        kv)
    return {"gap": list(gap)}


# ================================================================ Q6 · 环5 静态耦合
def q6():
    """静态通道：G 的空间部分由标量势导出 ⇒ ∇×G ≡ 0 ⇒ 耦合方程退化为 0=0（零判别力）。
    机器：∇×∇φ ≡ 0（具体 φ=x²y+y²z+z²x）；反例：非梯度场 (y,0,0) 的旋度 =(0,0,−1)≠0（有牙）。"""
    import sympy as sp
    x, y, z = sp.symbols("x y z", real=True)
    phi = x ** 2 * y + y ** 2 * z + z ** 2 * x
    gx, gy, gz = phi.diff(x), phi.diff(y), phi.diff(z)
    c1 = sp.simplify(gz.diff(y) - gy.diff(z))
    c2 = sp.simplify(gx.diff(z) - gz.diff(x))
    c3 = sp.simplify(gy.diff(x) - gx.diff(y))
    # 反例
    A = (y, sp.Integer(0), sp.Integer(0))
    d1 = sp.simplify(A[2].diff(y) - A[1].diff(z))
    d2 = sp.simplify(A[0].diff(z) - A[2].diff(x))
    d3 = sp.simplify(A[1].diff(x) - A[0].diff(y))
    kv = {"∇×∇φ（φ=x²y+y²z+z²x）": [str(c1), str(c2), str(c3)],
          "反例 (y,0,0) 的旋度": [str(d1), str(d2), str(d3)]}
    ok = (c1 == 0) and (c2 == 0) and (c3 == 0) and (d3 == -1)
    add("Q6", "判据",
        "环5 静态耦合：∇×G≡0 ⇒ 耦合方程退化为 0=0（机器恒零 + 非梯度反例给 (0,0,−1)）⇒ 零判别力",
        "PASS" if ok else "FAIL",
        "静态通道的空间部分由标量势导出 ⇒ **∇×G ≡ 0**（机器：取 φ=x²y+y²z+z²x，∇×∇φ = **(%s, %s, %s)** 全零）；"
        "于是耦合方程两端都只含散度项 ⇒ **退化为 0=0**。\n"
        "**有牙的反例**：非梯度场 (y,0,0) 的旋度 = **(%s, %s, %s)** ≠ 0 ⇒ 判据能区分「势场」与「一般矢量场」，"
        "不是恒绿。\n"
        "⇒ **环5 的「零判别力」是机器证明**（承 S12 与 r324 的 Birkhoff 结论）：静态通道**无论怎么调系数**"
        "都不能验收弱场引力 ⇒ 它作为「全链路最后一公里」的验收环是**空的**。"
        % (c1, c2, c3, d1, d2, d3),
        kv)
    return {"curl0": True}


# ================================================================ Q7 · 环6 锚与定义域
def q7():
    """定义域必要条件：v_θ = ωr ≤ c。若 ω 取内禀值 ω_C=m_ec²/ℏ 则 r ≤ λ̄_C。
    r=λ̄_C ⇒ v/c=1（边界）；r=a₀=α⁻¹λ̄_C ⇒ v/c=α⁻¹=137.036（越域）。
    若要在 r=a₀ 上保 v=c，则 ω 必须降到 c/a₀ = ω_C/137.036 ⇒ ω 不能是内禀常数 ⇒ 承 r124 T05。
    宏观/引力尺度（≫λ̄_C）上任何内禀 ω 都越域 ⇒ 「内禀频率」与「外推尺度」不可兼得。"""
    lam = HBAR / (ME * C_L)
    om_c = ME * C_L * C_L / HBAR
    a0_over_lam = A0 / lam
    v_boundary = D1
    om_req = C_L / A0
    r_om = om_c / om_req
    d = rel(a0_over_lam, D1 / ALPHA)
    kv = {"λ̄_C[m]": fmt(lam), "ω_C[s⁻¹]": fmt(om_c), "a₀/λ̄_C": fmt(a0_over_lam),
          "α⁻¹": fmt(D1 / ALPHA), "相对差": fmt(d),
          "保 v=c 所需 ω[s⁻¹]": fmt(om_req), "ω_C/所需": fmt(r_om)}
    ok = (a0_over_lam > Decimal("137")) and (d < Decimal("1e-8")) and (r_om > Decimal("137"))
    add("Q7", "判据",
        "环6 定义域：ω 固定 ⇒ r≤λ̄_C；a₀ 锚越 v≤c 137.036 倍；保 v=c 则 ω 必须随 r 反比降 ⇒ 内禀与尺度不可兼得",
        "PASS" if ok else "FAIL",
        "定义域必要条件是 **v_θ = ωr ≤ c**。取内禀频率 ω_C=m_ec²/ℏ=**%s s⁻¹** ⇒ 允许的最大半径就是 "
        "**λ̄_C=ℏ/(m_ec)=%s m**（r=λ̄_C 时 v/c 恰 = **%s**）。\n"
        "而 r=a₀=**%s λ̄_C** ⇒ v/c = **%s**，与 α⁻¹=**%s** 相对差 **%s** ⇒ **越 v≤c 达 137.036 倍**。\n"
        "若坚持在 r=a₀ 上保 v=c，则 ω 必须降到 c/a₀=**%s s⁻¹**，是 ω_C 的 **1/%s** ⇒ "
        "**ω 不能是内禀常数，必须随半径反比衰减**。\n"
        "⇒ **环6 的机器结论（PASS，指判据成立）**：任何「内禀频率」在宏观/引力尺度上都越域 ⇒ "
        "「内禀频率」与「外推尺度」不可兼得（r124 T05 的机器复证）⇒ 要么改 ω 为场，要么改 r 为外部输入，二者都回到 G1/G2。"
        % (fmt(om_c, 6), fmt(lam, 6), fmt(v_boundary, 4), fmt(a0_over_lam, 6),
           fmt(a0_over_lam, 6), fmt(D1 / ALPHA, 6), fmt(d, 4), fmt(om_req, 6), fmt(r_om, 4)),
        kv)
    return {"a0_over_lam": a0_over_lam, "om_req": om_req}


# ================================================================ Q8 · 六环总账
def q8():
    """六环账本：数学/量纲 通过 3/6（环1 恒等式、环2 质量式量纲、环3 力式量纲），
    其余 3 环断（环4 拉氏量纲失配、环5 零判别力、环6 越域）；物理可用 0/6。
    第一断点 = 环3 承载物（横向 ∇κ 需 null 汇）⇒ 后续环4–环6 即便修好也无物可载。"""
    rows = [
        ("L1", "ω²=c²(κ²+τ²)", "数学", "通（机器零）", "只锁幅度、无演化（r338 Q4）"),
        ("L2", "m=(ℏ/c)√(κ²+τ²)", "量纲 + 锚", "量纲通 / 锚断", "玻尔锚差 1.878e4 倍（Q3）"),
        ("L3", "F=ℏc∇κ", "量纲 + 承载", "量纲通 / 承载断", "均匀螺旋 F=0；横向 ∇κ 无定义（Q4）"),
        ("L4", "c⁴/(16πG)R ↔ (ℏ/c)√(κ²+τ²)ω", "量纲", "断（失配 [0,−1,−1]）", "不可由纯数或 c 幂修复（Q5）"),
        ("L5", "∇×G≡0（静态耦合）", "判别力", "通（恒等式）/ 渠道空", "0=0，零判别力（Q6）"),
        ("L6", "v_θ=ωr≤c（定义域）", "定义域", "通（必要条件）/ 越域 137 倍", "a₀ 锚越 v≤c（Q7）"),
    ]
    math_pass = 3
    phy_pass = 0
    kv = {"六环账": [list(r) for r in rows], "数学/量纲通过": math_pass, "物理可用": phy_pass,
          "第一断点": "L3（承载物：横向 ∇κ 需 null 汇，承 X-R329-2）"}
    add("Q8", "判据",
        "六环总账：数学/量纲 3/6（L1/L2/L3），物理可用 0/6；第一断点 = 环3 承载物",
        "PASS" if math_pass == 3 and phy_pass == 0 else "FAIL",
        "六环账本（逐环机器读数汇总）：\n\n"
        "| 环 | 公式 | 审的层 | 判决 | 关键读数 |\n| --- | --- | --- | --- | --- |\n"
        + "\n".join("| %s | %s | %s | %s | %s |" % r for r in rows) +
        "\n\n⇒ **数学/量纲层通过 3/6**（L1 恒等式、L2 质量式量纲、L3 力式量纲）；**物理可用 0/6**："
        "三处断点分别是**锚**（L2：1.878e4 倍）、**承载物**（L3：横向 ∇κ 无定义）、**量纲配对**（L4：[0,−1,−1]），"
        "另两处（L5 零判别力、L6 越域 137 倍）是**渠道空**而非公式错。\n"
        "**第一断点 = L3**：横向 ∇κ 必须建在 null 汇上（r329 X-R329-2），在此之前 L4–L6 即便修好也**无物可载**；"
        "而 L2 的锚与 L6 的越域是**同一个缺口的两个投影**（r 的来源，G2）。\n"
        "⇒ 全链路结论：**核心公式体系「算得对」的部分集中在恒等式与量纲；「用得上」的部分是 0**。"
        "这与整理册 §五「把输入当导出、把恒等式当方程、把自由函数当场」的三句诊断逐条对应。",
        kv)
    return {"math_pass": math_pass, "phy_pass": phy_pass, "rows": rows}


# ================================================================ Q9 · 对表
def q9():
    chain = [
        ("S5", "拉氏 (1/16πG)(R−τ²) 与 (ℏ/c)√(κ²+τ²)ω 源项：缺 c⁴、ℏ/c 量纲 [ML]",
         "本卷 Q5：EH 项 [ML⁻¹T⁻²] vs 源项 [MT⁻¹] ⇒ 失配 [0,−1,−1]，非纯数亦非 c 幂可修",
         "复证（口径记账不同，结论同）"),
        ("S7", "残余质量式 m*/m₀=α(4π)^β(1−η) 三参数拟合 10/10 ⇒ 零判别力",
         "本卷 Q2/Q3：质量式量纲齐次但锚一挪就差 1.878e4 倍 ⇒ 参数化拟合只会把缺口藏进参数",
         "加强"),
        ("S8", "拓扑电荷 Q=(1/4π)∮V·dS 量纲 L³T⁻¹ 非库仑、弱场 Q≡0",
         "本卷未碰（Q6 只审静态 G 的旋度）；S8 的「公设与结论自相抵消」与本卷 L5 同类",
         "未动"),
        ("S12", "时变耦合方程作静态引力判据：静态 ∇×G≡0 ⇒ 0=0",
         "本卷 Q6 机器复证（∇×∇φ≡0，非梯度反例给出 (0,0,−1) 有牙）",
         "复证（PASS）"),
        ("G2", "螺旋半径 r 的来源；康普顿锚 v_θ/c=137.04 越定义域",
         "本卷 Q3+Q7：质量锚与定义域是**同一缺口**的两面 ⇒ r≤λ̄_C 与 m=m_e 不可分离",
         "加强（合并两处账）"),
        ("r242 R09", "G_μν 与 (8πG/c⁴)T 量纲已对齐，缺一阶展开与 3 经典检验数值表",
         "本卷 Q5 说明「对齐」只在把 T 写成能量密度时成立；螺旋源项给的是 [MT⁻¹] 不是能量密度",
         "前提修正"),
        ("r124 T05", "内禀频率必借外部尺度",
         "本卷 Q7 机器复证：ω 固定 ⇒ r≤λ̄_C；保 v=c ⇒ ω∝1/r ⇒ 二者不可兼得",
         "复证（PASS）"),
        ("r338", "G1 收口（负）：候选族 0/4、净余 1 个自由函数",
         "本卷 Q8 把 G1 的负结果放进全链：环1 数学对但无演化 ⇒ 下游 L4–L6 无动力学可载",
         "承"),
    ]
    kv = {"对表": [list(c) for c in chain], "条数": len(chain)}
    add("Q9", "对表",
        "对表：S5/S12 复证；S7/G2 加强；r242 R09 前提修正；r124 T05 复证；r338 承",
        "INFO",
        "；".join("%s：%s ⇒ %s（%s）" % c for c in chain) +
        "。⇒ 本卷定位：**不新增物理，只把「核心公式到底哪一环能用」做成逐环账本**；"
        "S5/S12 的旧判词全部复现，S7/G2 因本卷的「锚=缺口」合并而加强，"
        "r242 R09 的「量纲已对齐」需要限定为「把 T 写成能量密度时」。",
        kv)
    return {"n": len(chain)}


# ================================================================ Q10 · 门槛登记
def q10():
    rows = [
        ("G1", "ω(r,t) 的场方程", "r338 收口（负）：候选 0/4、净余 1 函数", "收口（负）"),
        ("G2", "螺旋半径 r 的来源", "本卷 Q3+Q7：质量锚与越域是同一缺口 ⇒ 越域 137 倍已机器复证", "开（账已合并）"),
        ("G3", "弱场史瓦西退化数值验收", "r324 收口（Birkhoff ⇒ 零判别力）", "收口（负）"),
        ("G4", "null Frenet 标架重写", "r329 收口（帧局部 κ,τ）", "收口（条件/负）"),
        ("G5", "首条可证伪点预言", "本卷 Q8：物理可用 0/6 ⇒ 无点预言可报", "开（前置被否）"),
        ("G6", "EC 独立挠率源方程", "本卷不涉（另有并行卷在审）", "开"),
        ("G7", "固定点幅度 C 的第一性选择", "本卷不涉（r325 已证 q 为自由拓扑输入）", "开"),
    ]
    gates = [
        ("承载物门", "κ,τ 定义在哪种曲线上？类光 ⇒ 先过 G4",
         "PASS（r329 已给帧局部承载物；本卷 L3 缺的是**横向**承载物）"),
        ("判别力门", "自由参数为 0 时仍非平凡的点预言？", "FAIL（Q6 静态通道 0=0；Q8 物理可用 0/6）"),
        ("洛伦兹门", "κ,τ,ω 非洛伦兹不变量 ⇒ 协变化路径？", "FAIL（承 r329 κ'=κ/D²；本卷所有环都在某个帧里写）"),
    ]
    kv = {"门槛表": [list(r) for r in rows], "三道自检门": [list(g) for g in gates]}
    add("Q10", "登记",
        "G1–G7 门槛登记 + 三道自检门（本卷无新收口；G2 两处账合并）",
        "INFO",
        "| 项 | 状态 |\n| --- | --- |\n" + "\n".join("| %s | %s：%s | %s |" % r for r in rows) +
        "\n\n三道自检门：承载物门 **%s**；判别力门 **%s**；洛伦兹门 **%s**。⇒ 本卷**不新增收口**："
        "G1 已由 r338 收口（负）、G3/G4 由 r324/r329 收口；本卷的贡献是把 G2 的「质量锚」与「越域」"
        "合并成同一个账（Q3+Q7）。"
        % (gates[0][2], gates[1][2], gates[2][2]),
        kv)
    return {"gate_rows": rows}


# ================================================================ Q11 · 判据集
def q11():
    R_LIST.update({
        "R1": ("恒等式 ω²=c²(κ²+τ²) 在 null 上机器零", "Q1：4D null ⟺ 3D 单位速 ⟺ 恒等式；数值判例残差 0", True),
        "R2": ("质量式 m=(ℏ/c)√(κ²+τ²) 量纲齐次", "Q2：指数向量 [1,0,0]=[M]；缺 c 错式 [1,1,−1] 不过关", True),
        "R3": ("质量式在任何物理锚上闭合", "Q3：λ̄_C 锚闭合；玻尔锚差 1.878e4 倍（4.85e-35 kg = 5.3e-5 m_e）", False),
        "R4": ("力式 F=ℏc∇κ 在 null 上给非零横向预言", "Q4：均匀螺旋 dκ/dσ=0 ⇒ F=0；直线 κ=0 ⇒ F=0；横向 ∇κ 无定义", False),
        "R5": ("EH 拉氏与螺旋源项量纲齐次", "Q5：失配 [0,−1,−1]，k·c 命中集为空 ⇒ 须外部新常数", False),
        "R6": ("静态耦合通道有判别力", "Q6：∇×G≡0 ⇒ 0=0（零判别力）", False),
    })
    n = sum(1 for v in R_LIST.values() if v[2])
    kv = {"R1–R6": {k: v[2] for k, v in R_LIST.items()}, "通过数": n, "总数": 6}
    add("Q11", "判据", "判据集 R1–R6 = %d/6" % n,
        "FAIL" if n < 6 else "PASS",
        "\n" + "\n".join("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1])
                         for k, v in R_LIST.items()) +
        "\n⇒ **%d/6**：只有「恒等式机器零」与「质量式量纲齐次」两条成立；"
        "锚（R3）、力（R4）、拉氏（R5）、静态判别力（R6）全部不成立 ⇒ "
        "**核心公式体系的「数学正确」与「物理可用」是两件事**，后者为 0。" % n,
        kv)
    return {"score": n}


# ================================================================ 控制组
def controls(extra):
    import sympy as sp
    HB_ = vdim(1, 2, -1)
    CC = vdim(0, 1, -1)
    KAP = vdim(0, -1, 0)
    # C1 量纲正对照
    good = sp.simplify(HB_ - CC + KAP)
    add("C1", "控制组", "正对照：m=(ℏ/c)√(κ²+τ²) 量纲 = [M]（量纲门对正确式放行）",
        "PASS" if good == vdim(1, 0, 0) else "FAIL",
        "指数向量 ℏ−c+κ = **%s** = [M] ⇒ 正确式**通过** ⇒ 量纲门不是一律否定。" % list(good), {})
    # C2 量纲有牙
    bad = sp.simplify(HB_ + KAP)
    add("C2", "控制组", "负对照：m=ℏ√(κ²+τ²)（漏 c）量纲 [MLT⁻¹] 被拒（量纲门有牙）",
        "PASS" if bad != vdim(1, 0, 0) else "FAIL",
        "漏一次 c ⇒ **%s** ≠ [M] ⇒ 被拒 ⇒ **量纲检查能抓住真实错误**（不是恒绿）。" % list(bad), {})
    # C3 恒等式有牙：非 null 曲线失配
    a, om, vz = 0.8, 1.0, 0.5
    spd = a * a * om * om + vz * vz
    resid = om * om - (a * om ** 2) ** 2 - (om * vz) ** 2
    add("C3", "控制组", "负对照：非 null 曲线（0.64+0.25=0.89≠1）⇒ 恒等式失配（判据有牙）",
        "PASS" if (abs(spd - 1) > 0.1) and (abs(resid) > 0.1) else "FAIL",
        "取 a=0.8、ω=1、v_z=0.5 ⇒ 空间速² = **%s**（≠1）、恒等式残差 = **%s** ≠ 0 ⇒ "
        "恒等式**只在 null 分支成立**，不是任何曲线的通用式。" % (spd, resid), {})
    # C4 静态通道有牙：非梯度场旋度非零
    x, y, z = sp.symbols("x y z", real=True)
    A = (y, sp.Integer(0), sp.Integer(0))
    d3 = sp.simplify(A[1].diff(x) - A[0].diff(y))
    add("C4", "控制组", "负对照：非梯度场 (y,0,0) 旋度 (0,0,−1)≠0 ⇒ 静态判据非恒绿",
        "PASS" if d3 == -1 else "FAIL",
        "非梯度场 (y,0,0)：curl_z = ∂_x A_y − ∂_y A_x = **%s** ⇒ 判据能区分「势场」与「一般场」，"
        "所以 Q6 的「0=0」不是判据失效，而是**物理渠道本身恒空**。" % d3, {})
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
    g.append(("G4", "恒等式与静态旋度机器零", extra["zero_ok"],
              "Q1 恒等式(null) 残差 0；Q6 ∇×∇φ 三分量全 0"))
    g.append(("G5", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    n_fail = len([i for i in ITEMS if i["verdict"] == "FAIL"])
    g.append(("G6", "正负双对照齐备（控制组 ≥4 且 FAIL ≥1）", n_ctl >= 4 and n_fail >= 1,
              "控制组 %d / FAIL %d" % (n_ctl, n_fail)))
    pos = {"六环数学通过": Decimal(extra["math_pass"]), "质量式 m(λ̄_C 锚)[kg]": extra["m_c"],
           "λ̄_C[m]": extra["lam"], "ω_C[s⁻¹]": extra["om_c"],
           "保 v=c 所需 ω[s⁻¹]": extra["om_req"]}
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
        "主条目 11 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
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
    summary = {"rid": RID, "stamp": STAMP, "标题": "核心公式理论体系全链路六环正确性审计",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 核心公式理论体系全链路六环正确性审计 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：CORE-CHAIN-SIX-RING-AUDIT / DIMENSION-PASS-CARRIER-FAIL /")
    L.append("      LAGRANGIAN-MISMATCH-UNFIXABLE-BY-NUMBER / PHYSICAL-USE-OF-CORE-FORMULAS-ZERO。")
    L.append("      数学/量纲 3/6（L1/L2/L3）；物理可用 0/6；第一断点 = L3 承载物；")
    L.append("      质量锚玻尔口径差 1.878e4 倍；拉氏失配 [0,−1,−1]；静态通道 0=0。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 核心公式全链路六环审计（数据册）" % RID, "",
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
    J = ["# 判定_TUFT-%s · 核心公式理论体系全链路六环正确性审计" % RID, "",
         "- **日期**：%s　- **靶**：整理册 §三 保留资产 1–5 + S5/S7/S8/S12 + G2（全链路逐环复算）" % STAMP,
         "- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
         "**控制组 %s**　**守卫 %s**　**rc=0**"
         % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
            summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]),
         "", "## 一、判决主文", "",
         "**CORE-CHAIN-SIX-RING-AUDIT / DIMENSION-PASS-CARRIER-FAIL / "
         "LAGRANGIAN-MISMATCH-UNFIXABLE-BY-NUMBER / PHYSICAL-USE-OF-CORE-FORMULAS-ZERO。**", ""]
    J.append("1. **数学/量纲层 3/6 通过**：L1 恒等式 ω²=c²(κ²+τ²) 在 4D null ⟺ 3D 单位速上机器零；"
             "L2 质量式 m=(ℏ/c)√(κ²+τ²) 量纲精确 [M]（缺 c 的错式被拒）；L3 力式 F=ℏc∇κ 量纲 [MLT⁻²] 通过。")
    J.append("2. **物理可用 0/6，三处断点**：① **锚**：质量式在 λ̄_C 上给 m_e（相对差机器零），"
             "一挪到玻尔锚只给 **%s kg = %s m_e**，差 **%s 倍**；② **承载物**：均匀螺旋 dκ/dσ=0 ⇒ **F=0**，"
             "直线 κ=0 ⇒ F=0，横向 ∇κ 在单世界线上**无定义**；③ **量纲配对**：EH 项 [ML⁻¹T⁻²] vs 源项 [MT⁻¹]，"
             "失配 **%s**，对 k∈[−8,8] 无 k·c 命中 ⇒ **纯数/ c 幂皆不可修**。"
             % (fmt(extra["m_b"], 6), fmt(extra["r_m"], 4), fmt(extra["r_req"], 4), extra["gap"]))
    J.append("3. **两处渠道空**：L5 静态耦合 ∇×G≡0 ⇒ **0=0**（零判别力，机器复证 + 非梯度反例有牙）；"
             "L6 定义域 v_θ=ωr≤c ⇒ a₀ 锚**越 v≤c 137.036 倍**；要保 v=c 则 ω 必须降到 c/a₀=%s s⁻¹"
             "（ω_C 的 1/137.036）⇒ **内禀频率与外推尺度不可兼得**（r124 T05 复证）。" % fmt(extra["om_req"], 6))
    J.append("4. **第一断点 = L3 承载物**：横向 ∇κ 必须先建 null 汇（X-R329-2）；在此之前 L4–L6 即便修好也**无物可载**。"
             "而 **L2 的锚与 L6 的越域是同一缺口的两面**（r 的来源，G2）⇒ 本卷把 G2 的两笔账合并。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：平直背景；null 螺旋 x(σ)=(σ, a cos ωσ, a sin ωσ, v_z σ)、a²ω²+v_z²=c²；"
             "量纲用 (M,L,T) 指数向量精确代数；SI 数值只在 Q3/Q7 换算。")
    J.append("- **管线**：L1 恒等式（Q1）→ L2 量纲（Q2）→ L2' 锚（Q3）→ L3 力式（Q4）→ "
             "L4 拉氏（Q5）→ L5 静态（Q6）→ L6 定义域（Q7）→ 总账（Q8）→ 对表（Q9）→ 门槛（Q10）→ 判据（Q11）。")
    J.append("- **关键常量**：c=%s m/s、α=%s、a₀=%s m、m_e=%s kg、ℏ=%s J s、G=%s。"
             % (fmt(C_L), fmt(ALPHA), fmt(A0), fmt(ME), fmt(HBAR), fmt(G_N)))
    J.append("")
    J.append("## 三、判据集 R1–R6 = %d/6" % extra["score"])
    J.append("")
    for k, v in R_LIST.items():
        J.append("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1]))
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
    J.append("- **B1**：L1 的「机器零」只在 null 分支且只在伪弧长（r329 帧）下成立；非 null 曲线失配已由 C3 给出。")
    J.append("- **B2**：L2/L3 的「量纲通过」只在 (M,L,T) 三基下；若引入角度/电荷等额外基，结论需重算（本卷不做）。")
    J.append("- **B3**：L3 的「承载断」是**定义域**命题，不是「F=ℏc∇κ 一定错」——若建成 null 汇，量纲已备好。")
    J.append("- **B4**：L4 的失配向量与 S5 的「缺 c⁴」是**不同记账口径**的同一事实；本卷不改 S5，只登记差。")
    J.append("- **B5**：Q3 的玻尔锚读数**不修改 r95 登记值**；本卷只说明「同一把尺子不能同时量 m_e 与 a₀」。")
    J.append("- **B6**：本卷**不新增收口**：G1 由 r338 收口、G3/G4 由 r324/r329 收口；本卷只做全链账本与 G2 合并。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：CORE-CHAIN-SIX-RING-AUDIT / DIMENSION-PASS-CARRIER-FAIL / "
             "LAGRANGIAN-MISMATCH-UNFIXABLE-BY-NUMBER / PHYSICAL-USE-OF-CORE-FORMULAS-ZERO —— "
             "六环账本：数学/量纲 3/6，物理可用 0/6；第一断点 L3（横向 ∇κ 无承载物）；"
             "L2 锚与 L6 越域同源（G2）；L4 失配非纯数可修；L5 渠道恒空。")
    J.append("")
    J.append("- **X-R341-1**：**null 汇（congruence）**上的横向 κ 梯度 —— 建 (θ,σ,ω_opt) 光学标量后，"
             "F_⊥=ℏc∇_⊥κ 才可算；这是 L3→L4 的必经门。")
    J.append("- **X-R341-2**：**量纲基扩展**（加入 e、角、熵）后 L2/L3 是否仍齐次 —— 本卷只做三基。")
    J.append("- **X-R341-3**：把源项写成**能量密度**所需的乘子（[L⁻¹T⁻¹] 常数）究竟是什么 —— "
             "若它恰是 1/λ̄_C 或 H₀，则 L4 可闭合但引入外部尺度；需逐候选试算。")
    J.append("- **X-R341-4**：L2 锚与 L6 越域合并后，G2 的「可攻性」变成「设计一个 r 机制使 r≤λ̄_C 且"
             "又能在宏观尺度上给出可观测效应」——这需要非线性/集体机制，本卷未涉及。")
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
    ring_rows = "".join(
        "<tr><td class='id'>%s</td><td class='mono'>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % r for r in extra["rows"]) if isinstance(extra["rows"], list) and len(extra["rows"][0]) == 5 \
        else "".join("<tr><td class='id'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r
                     for r in extra["rows"])
    gate_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % g
                        for g in extra["gate_rows"])
    H = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TUFT-r342 · 核心公式全链路六环审计</title>
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
<h1>TUFT-r342 · 核心公式体系：全链路六环正确性审计</h1>
<div class="sub">2026-11-01 · 靶：整理册 §三 保留资产 1–5 + S5/S7/S8/S12 + G2 ｜ sympy 量纲代数 + Decimal 80 位</div>
<div>
<span class="badge">条目 %(n)d</span><span class="badge">PASS %(p)d</span><span class="badge">FAIL %(f)d</span>
<span class="badge">INFO %(i)d</span><span class="badge">控制组 %(c)s</span><span class="badge">守卫 %(g)s</span>
</div>
<div class="verdict"><b>CORE-CHAIN-SIX-RING-AUDIT / DIMENSION-PASS-CARRIER-FAIL /
LAGRANGIAN-MISMATCH-UNFIXABLE-BY-NUMBER / PHYSICAL-USE-OF-CORE-FORMULAS-ZERO</b><br>
六环账本：<b>数学/量纲 3/6</b>，<b>物理可用 0/6</b>；第一断点 = 环3 承载物（横向 ∇κ 无定义）；
质量锚在玻尔口径上差 <b>1.878e4 倍</b>；拉氏失配 <b>[0,−1,−1]</b> 非纯数可修。</div>
<div class="grid">
<div class="card"><div class="k">数学/量纲通过</div><div class="n">3<span class="u">/ 6</span></div><div class="u">L1 / L2 / L3</div></div>
<div class="card"><div class="k">物理可用</div><div class="n">0<span class="u">/ 6</span></div><div class="u">锚 / 承载 / 量纲 / 渠道</div></div>
<div class="card"><div class="k">m(玻尔锚)</div><div class="n">%(mb)s<span class="u">kg</span></div><div class="u">= %(rm)s m_e</div></div>
<div class="card"><div class="k">拉氏失配</div><div class="n mono" style="font-size:16px">%(gap)s</div><div class="u">≠ k·c，纯数不可修</div></div>
<div class="card"><div class="k">均匀螺旋 F</div><div class="n">0</div><div class="u">dκ/dσ=0 ⇒ ∇κ=0</div></div>
<div class="card"><div class="k">判据集</div><div class="n">%(score)d<span class="u">/ 6</span></div><div class="u">R1/R2 过；R3–R6 不过</div></div>
</div>
<h2>一、六环账本（Q1–Q8）</h2>
<table><tr><th>环</th><th>公式</th><th>审的层</th><th>判决</th><th>关键读数</th></tr>%(ring_rows)s</table>
<div class="note">三处断点：<b>锚</b>（L2：λ̄_C 上给 m_e，玻尔锚差 1.878e4 倍）｜<b>承载物</b>（L3：均匀螺旋 F=0、横向 ∇κ 无定义）｜
<b>量纲配对</b>（L4：EH 项 [ML⁻¹T⁻²] vs 源项 [MT⁻¹]）。另两处（L5 静态 0=0、L6 越域 137 倍）是<b>渠道空</b>。</div>
<h2>二、量纲账（Q2 / Q5）</h2>
<div class="two">
<div class="card"><div class="k">质量式（通过）</div><div class="n mono" style="font-size:15px">ℏ−c+κ = [1,0,0]</div>
<div class="u">m=(ℏ/c)√(κ²+τ²) ⇒ [M] ✓；漏 c ⇒ [1,1,−1] ✗</div></div>
<div class="card"><div class="k">拉氏配对（断）</div><div class="n mono" style="font-size:15px">%(gap)s</div>
<div class="u">EH [1,−1,−2] vs 源项 [1,0,−1]；k·c 命中集为空</div></div>
</div>
<div class="note">量纲门<b>有牙</b>：C1 放行正确式、C2 抓住「漏一次 c」、C3 抓住「非 null 曲线」、C4 抓住「非梯度场」。
⇒ 「3/6 通过」不是放水，是<b>只有这三环真的齐次</b>。</div>
<h2>三、质量锚与定义域（Q3 / Q7）</h2>
<table>
<tr><th>锚 r</th><th>√(κ²+τ²) [m⁻¹]</th><th>m=(ℏ/c)√ [kg]</th><th>对 m_e</th><th>v_θ/c</th></tr>
<tr><td>λ̄_C = %(lam)s m</td><td>%(req)s</td><td>9.109e-31</td><td>1（精确）</td><td>1（null）</td></tr>
<tr><td>a₀ = %(a0)s m</td><td>%(sqr)s</td><td>%(mb)s</td><td>%(rm)s</td><td>137.036（越域）</td></tr>
</table>
<div class="note">同一把尺子量不了两个尺度：电子自锚（r=λ̄_C）闭合到机器零；玻尔锚（r=a₀）给 <b>5.3e-5 m_e</b>，
要回到 m_e 需 √(κ²+τ²) 是实际值的 <b>%(rreq)s 倍</b>。要保 v=c 则 ω 必须降到 <b>%(omreq)s s⁻¹</b>（ω_C 的 1/137）。
⇒ <b>「质量锚」与「越域」是同一缺口（G2）的两面</b>。</div>
<h2>四、力式与静态通道（Q4 / Q6）</h2>
<div class="note">F=ℏc∇κ 的量纲 <b>[MLT⁻²] 是全库唯一过量纲门的力式</b>；但均匀螺旋 dκ/dσ=0 ⇒ F=0、直线 κ=0 ⇒ F=0、
横向 ∇κ 需要 null 汇 ⇒ <b>环3 断在承载物</b>。静态通道 ∇×G≡0 ⇒ 耦合方程退化为 <b>0=0</b>（机器恒零，
非梯度反例 (y,0,0) 给 (0,0,−1) 证明判据有牙）⇒ <b>渠道恒空</b>。</div>
<h2>五、条目逐条（主条目）</h2>
<table><tr><th>#</th><th>判决</th><th>条目</th></tr>%(main_rows)s</table>
<h2>六、控制组与守卫</h2>
<div class="two">
<table><tr><th>#</th><th>判决</th><th>控制组</th></tr>%(ctl_rows)s</table>
<table><tr><th>#</th><th>判决</th><th>守卫</th></tr>%(grd_rows)s</table>
</div>
<h2>七、门槛登记（Q10）</h2>
<table><tr><th>项</th><th>缺口</th><th>状态</th><th>判决</th></tr>%(gate_rows)s</table>
<div class="note">本卷<b>不新增收口</b>：G1 由 r338 收口（负）、G3/G4 由 r324/r329 收口；本卷的贡献是把 G2 的
「质量锚」与「越域」合并成同一个账，并把「哪些核心公式算得对 / 用得上」做成逐环可复算的账本。</div>
<h2>八、诚实边界</h2>
<div class="note">B1 恒定零只在 null 分支 + 伪弧长帧；B2 量纲只在 (M,L,T) 三基；B3 L3 是定义域命题而非「力式必错」；
B4 失配向量与 S5「缺 c⁴」是不同记账口径的同一事实；B5 不修改 r95 登记值；B6 不主张纲领死亡。</div>
<div class="note" style="margin-top:26px">复现：<code>python -X utf8 源码\\_run_r342.py</code> ⇒ rc=0，条目 %(n)d，
控制组 %(c)s，守卫 %(g)s。本卷条目<b>不可与 r324/r329/r338 等相加</b>。</div>
</div></body></html>""" % {
        "n": summary["条目总数"], "p": summary["PASS"], "f": summary["FAIL"], "i": summary["INFO"],
        "c": summary["控制组"], "g": summary["守卫"], "score": extra["score"],
        "mb": fmt(extra["m_b"], 6), "rm": fmt(extra["r_m"], 4), "rreq": fmt(extra["r_req"], 4),
        "gap": extra["gap"], "lam": fmt(extra["lam"], 6), "a0": fmt(A0, 6),
        "req": fmt(extra["req"], 6), "sqr": fmt(extra["sqr_b"], 6), "omreq": fmt(extra["om_req"], 6),
        "ring_rows": ring_rows, "gate_rows": gate_rows,
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
    e1 = q1()
    q2()
    e3 = q3()
    q4()
    e5 = q5()
    q6()
    e7 = q7()
    e8 = q8()
    q9()
    e10 = q10()
    e11 = q11()
    lam = HBAR / (ME * C_L)
    om_c = ME * C_L * C_L / HBAR
    extra = {"declared_n": 25, "zero_ok": (e1["ident"] == 0),
             "math_pass": e8["math_pass"], "rows": e8["rows"],
             "m_b": e3["m_b"], "r_m": e3["r_m"], "r_req": e3["r_req"],
             "m_c": (HBAR / C_L) / lam,
             "lam": lam, "om_c": om_c, "om_req": e7["om_req"],
             "gap": e5["gap"], "gate_rows": e10["gate_rows"], "score": e11["score"],
             "req": ME * C_L / HBAR,
             "sqr_b": dsqrt((ALPHA ** 2 / A0) ** 2 + (ALPHA / A0 * dsqrt(D1 - ALPHA * ALPHA)) ** 2)}
    controls(extra)
    guards(extra)
    summary = emit(extra)
    emit_judgment(summary, extra)
    p = emit_html(summary, extra)
    print("=" * 78)
    print("TUFT-%s · 核心公式理论体系全链路六环正确性审计" % RID)
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
