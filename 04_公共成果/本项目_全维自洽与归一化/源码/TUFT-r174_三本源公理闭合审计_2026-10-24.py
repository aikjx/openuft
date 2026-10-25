# -*- coding: utf-8 -*-
"""
TUFT-r174 · 三本源公理闭合审计（第一层验证 · 前置关卡）  2026-10-24

来料（只读，不改写）：
  A. openuft/04_公共成果/本项目_统一场论攻破/TUFT母册底层总纲_分层收口_2026-10-24.md §一（三条本源公理）
  B. 同目录 布局_剩余项分层归档_2026-10-24.md §〇（审校通过复本）
  C. 用户 2026-10-24《TUFT 验证与应用全方案》第一层（本次来稿）

分工声明（避免重复计数）：
  · r107 已判「挠率晕 τ_φ∝1/r + K 自由」这一支具体实现 FAIL；本册不重审该实现，
    改判**结构层**：不依赖 τ(r) 取什么形式，只依赖公理集本身。
  · r28/r29 已判「三元理无运算定义 / 映射缺口 2.585 bit」；本册只做**代数模型穷举**（构造模型这一项），
    不重复信息量计数。
  · r27/GMUFT 已判「L_tau 退化为常数 ⇒ τ 不传播」；本册把该性质**首次绑定到预言 A（挠率涡旋暗物质晕）**
    上做后果推演，属增量而非重复。

红线：本册只做数学自洽与结构性判定，不产生新物理，不宣称观测证实/否证。
"""
import os, sys, json, itertools
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60
HERE = Path(__file__).resolve().parent
BASE = HERE.parent                 # 04_公共成果/本项目_全维自洽与归一化
OUTD = BASE / "数据"
OUTD.mkdir(parents=True, exist_ok=True)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ENTRIES = []
def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))

GUARDS = []
def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] %s :: %s" % (name, msg))
    return ok

def fs(x):
    """Decimal/Fraction -> 定点科学计数字符串（不用 quantize，避免高位数 InvalidOperation）"""
    try:
        return format(Decimal(x), ".25E")
    except Exception:
        return str(x)

# =====================================================================
# 0. 量纲机器（四元组 M,L,T,Q）+ 自身守卫
# =====================================================================
def dmul(a, b):  return tuple(x + y for x, y in zip(a, b))
def ddiv(a, b):  return tuple(x - y for x, y in zip(a, b))
def dpow(a, n):  return tuple(x * n for x in a)
def dsqrt(a):    return tuple(Fraction(x, 2) for x in a)

ZERO = (Fraction(0),) * 4
DIM = {
    "c":    (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)),
    "G":    (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0)),
    "hbar": (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)),
    "m":    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    "E":    (Fraction(1), Fraction(2), Fraction(-2), Fraction(0)),
    "rhoE": (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0)),   # 能量密度 J/m^3
    "rhoM": (Fraction(1), Fraction(-3), Fraction(0), Fraction(0)),    # 质量密度
    "L":    (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    "T":    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    "kappa_F": (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)),  # Frenet 曲率/挠率 L^-1
}
def dstr(a):
    out = []
    for i, s in enumerate("MLTQ"):
        v = a[i]
        if v == 0:
            continue
        out.append("%s^%s" % (s, v))
    return "·".join(out) if out else "1"

# ---- 量纲工具自身守卫（先验工具，再用于判定）----
guard("G0-1 planck_length", dsqrt(ddiv(dmul(DIM["hbar"], DIM["G"]), dpow(DIM["c"], 3))) == DIM["L"],
      "[sqrt(hbar G/c^3)] 必须为 L")
guard("G0-2 inv_force", ddiv(DIM["G"], dpow(DIM["c"], 4)) ==
      (Fraction(-1), Fraction(-1), Fraction(2), Fraction(0)),
      "[G/c^4] 必须为 N^-1 = M^-1 L^-1 T^2")
guard("G0-3 energy_density", DIM["rhoE"] == (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0)),
      "能量密度量纲常量写死校验")
guard("G0-4 torsion_vs_connection", DIM["kappa_F"] == (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)),
      "挠率与 Christoffel 同量纲 L^-1")
guard("G0-5 c3_over_G", ddiv(dpow(DIM["c"], 3), DIM["G"]) ==
      (Fraction(1), Fraction(0), Fraction(-1), Fraction(0)),
      "[c^3/G] = M T^-1，乘 L^-1 得自旋密度 M L^-1 T^-1")
# =====================================================================
# A 段 · 公理 3「角频率–尺度绑定」三口径互斥（本次来稿与母册冲突）
# =================================================================----
# 口径 M（母册权威，母册 L43 / 审校 L23）：omega = c/l, l = sqrt(kappa^{-1})  => omega = c*sqrt(kappa)
# 口径 U（本次来稿 §一.1.3）：             omega = c/sqrt(kappa)
# 口径 T（TUFT 三重奏，库内已攻破册公认）：kappa^2 + tau^2 = (omega/c)^2，[kappa]=[tau]
OMEGA = (Fraction(0), Fraction(0), Fraction(-1), Fraction(0))   # T^-1

# 反解各自要求的 [kappa]
kap_M = dpow(ddiv(OMEGA, DIM["c"]), 2)      # omega = c kappa^{1/2}
kap_U = dpow(ddiv(DIM["c"], OMEGA), 2)      # omega = c kappa^{-1/2}
kap_T = ddiv(OMEGA, DIM["c"])               # omega/c = kappa （由三重奏，kappa~tau）

add("A01", "PASS", "口径 M（母册）反解 [kappa]",
    "母册 omega=c/l, l=sqrt(kappa^-1) 等价于 omega=c*sqrt(kappa)；由 [omega]=T^-1 反解得 "
    "[kappa]=%s，与审校册 L24 登记的 kappa~L^-2 逐位一致。" % dstr(kap_M),
    {"kappa_dim": dstr(kap_M)})
add("A02", "FAIL", "口径 U（本次来稿）反解 [kappa] 与母册差 L^4",
    "来稿写 omega=c/sqrt(kappa)，反解得 [kappa]=%s；与母册口径 %s 相差 %s。"
    "同一个符号 kappa 在两份权威来料里量纲相反（幂次差 1，量纲差平方）⇒ 引用前必须仲裁，否则后续所有代入全错。"
    % (dstr(kap_U), dstr(kap_M), dstr(ddiv(kap_U, kap_M))),
    {"kappa_dim": dstr(kap_U), "gap_vs_master": dstr(ddiv(kap_U, kap_M))})
add("A03", "FAIL", "口径 T（三重奏）与母册口径互斥，差 L^1",
    "TUFT 核心恒等式 kappa^2+tau^2=(omega/c)^2 要求 [kappa]=[tau]=%s（Frenet 曲率/挠率）；"
    "母册口径要求 %s。两者相差 %s ⇒ 若公理 3 的 kappa 指 Frenet 曲率，则 omega=c*sqrt(kappa) 量纲不成立。"
    % (dstr(kap_T), dstr(kap_M), dstr(ddiv(kap_M, kap_T))),
    {"kappa_dim": dstr(kap_T), "gap_vs_master": dstr(ddiv(kap_M, kap_T))})
add("A04", "CORRECTED", "唯一兼容读法：公理 3 的 kappa 是组合量 kappa^2+tau^2（符号同名异义）",
    "把公理 3 的 kappa 解释为组合量 Q=kappa_F^2+tau^2（[Q]=%s），则 omega=c*sqrt(Q)=c*sqrt(kappa_F^2+tau^2) "
    "**恰是三重奏本身**，且量与母册登记的 L^-2 一致 ⇒ 三口径中只有这一个读法能同时满足母册与三重奏。"
    "代价：符号 kappa 在公理 3 与 Frenet 曲率层不同义，须改名（建议 Q 或 Omega^2/c^2），这是零成本修法但**必须显式登记**。"
    % dstr(dpow(DIM["kappa_F"], 2)),
    {"combo_dim": dstr(dpow(DIM["kappa_F"], 2))})
add("A05", "FAIL", "平直极限行为相反：kappa->0 时两条口径给出 omega->0 与 omega->∞",
    "来稿要求检查「kappa->0 时 omega->∞ 是否不爆炸」，但该行为只在口径 U 下发生；"
    "母册口径 M 下 kappa->0 给出 omega->0（频率归零）。数值对拍：取 kappa=1e-6..1e-30，"
    "口径 M 的 omega 单调降到 0，口径 U 的 omega 单调升到 ∞ ⇒ **两条口径在平直极限给出定性相反的物理**，"
    "不可能同真。⇒ 来稿 §一.1「真空极限」这一条的待验问题在母册口径下根本不存在（是口径错置产生的伪问题）。",
    {})
# 数值对拍（口径 M 降 / 口径 U 升）
_c = Decimal("299792458")
_m = [Decimal("1E-6"), Decimal("1E-12"), Decimal("1E-18"), Decimal("1E-24"), Decimal("1E-30")]
_om_M = [( _c * k.sqrt() ) for k in _m]
_om_U = [( _c / k.sqrt() ) for k in _m]
guard("G-A5a 口径M单调降", all(_om_M[i] > _om_M[i+1] for i in range(len(_om_M)-1)), "kappa->0 时 omega=c*sqrt(kappa) 应单调降")
guard("G-A5b 口径U单调升", all(_om_U[i] < _om_U[i+1] for i in range(len(_om_U)-1)), "kappa->0 时 omega=c/sqrt(kappa) 应单调升")
add("A06", "INFO", "口径对拍数值（c=299792458 m/s）",
    "口径 M 的 omega：%s | 口径 U 的 omega：%s（同一组 kappa）。两者比值为 kappa 的一次幂，"
    "在 kappa=1e-30 处相差 1e30 倍。" % (
        ", ".join(fs(v) for v in _om_M[:3]), ", ".join(fs(v) for v in _om_U[:3])),
    {"omega_M": [fs(v) for v in _om_M], "omega_U": [fs(v) for v in _om_U]})

# =====================================================================
# B 段 · 公理 2 五项量纲遍历
# =====================================================================
d_Ricci   = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0))          # [R_mn]=L^-2
d_Lamg    = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0))          # [Lambda]=L^-2
d_divT    = dmul(DIM["kappa_F"], DIM["kappa_F"])                            # [d][T] = L^-1*L^-1
d_TT      = dmul(DIM["kappa_F"], DIM["kappa_F"])
d_rhs     = dmul(ddiv(DIM["G"], dpow(DIM["c"], 4)), DIM["rhoE"])
terms = {"R_mn": d_Ricci, "Lambda*g_mn": d_Lamg, "nabla^a T_amn": d_divT,
         "T*T": d_TT, "rhs (8piG/c^4)T_mn": d_rhs}
same = all(v == d_Ricci for v in terms.values())
add("B01", "PASS" if same else "FAIL", "公理 2 五项量纲齐次性",
    "五项量纲：%s。全部等于 %s ⇒ 公理 2 **量纲自洽**（审校 L20 的『EC 标准形式』在量纲层成立）。"
    "注意：这要求挠率与 Christoffel 同量纲 L^-1，TUFT 的 Frenet 挠率恰为 L^-1 ⇒ 兼容。" %
    ("; ".join("%s=%s" % (k, dstr(v)) for k, v in terms.items()), dstr(d_Ricci)),
    {k: dstr(v) for k, v in terms.items()})
guard("G-B1 五项齐次", same, "公理2 五项必须同为 L^-2")
add("B02", "BOUNDARY", "量纲齐次 ≠ 结构闭合（B01 不解除任何下游阻塞）",
    "量纲齐次是必要条件不是充分条件：它只说明五项可以相加，不保证该式是某个作用量的 EL 方程、"
    "不保证散度守恒、不保证方程组闭合。C/D 段分别检验这三点。", {})
# =====================================================================
# C 段 · 协变散度 / Bianchi（含挠率）——全库首次扫描
#  几何恒等式是 off-shell 的，可在任意 (g,T) 上检验，无需先解场方程。
# =====================================================================
import sympy as sp

x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
XX = [x0, x1, x2, x3]
p, q, r, s = sp.symbols("p q r s")            # 度规参数
u1, u2, u3, u4 = sp.symbols("u1 u2 u3 u4")    # 挠率振幅
Lam = sp.symbols("Lambda")
SYMS = [p, q, r, s, u1, u2, u3, u4, Lam]

NPT = {x0: sp.Rational(3, 7), x1: sp.Rational(11, 5), x2: sp.Rational(13, 9), x3: sp.Rational(17, 4),
       p: sp.Rational(1, 3), q: sp.Rational(2, 7), r: sp.Rational(5, 11), s: sp.Rational(4, 9),
       u1: sp.Rational(7, 13), u2: sp.Rational(3, 8), u3: sp.Rational(5, 6), u4: sp.Rational(2, 15),
       Lam: sp.Rational(9, 7)}

def is_zero(e):
    """有理函数恒零判定：cancel 是有理式的范式化简，恒零必返回 0（严密）。"""
    try:
        c = sp.cancel(sp.together(e))
    except Exception:
        c = sp.simplify(e)
    return (c == 0), c

def magnitude(e):
    try:
        v = sp.N(e.subs(NPT), 40)
        return abs(complex(v)) if v.is_number else float("nan")
    except Exception:
        return float("nan")

def build(torsion_on):
    g = sp.zeros(4, 4)
    g[0, 0] = -(1 + p * x1)
    g[1, 1] =   1 + q * x1
    g[2, 2] =   1 + r * x2
    g[3, 3] =   1 + s * x1
    gi = g.inv()

    # --- Levi-Civita ---
    GamLC = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for m in range(4):
            for n in range(4):
                e = 0
                for l in range(4):
                    if gi[a, l] == 0:
                        continue
                    e += gi[a, l] * (sp.diff(g[l, n], XX[m]) + sp.diff(g[l, m], XX[n])
                                     - sp.diff(g[m, n], XX[l]))
                GamLC[a][m][n] = sp.Rational(1, 2) * e

    # --- 挠率 T^a_{mn}（反对称于 m,n）---
    Tu = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    if torsion_on:
        Tu[0][1][2] = u1 * x3;  Tu[0][2][1] = -u1 * x3
        Tu[1][0][2] = u2 * x2;  Tu[1][2][0] = -u2 * x2
        Tu[2][0][3] = u3 * x1;  Tu[2][3][0] = -u3 * x1
        Tu[3][0][1] = u4 * x2;  Tu[3][1][0] = -u4 * x2
    Tl = [[[sp.simplify(sum(g[a, l] * Tu[l][m][n] for l in range(4)))
            for n in range(4)] for m in range(4)] for a in range(4)]

    # --- 挠率张量（contortion）：K_{lmn} = (T_{lmn} - T_{mnl} + T_{nlm})/2 ---
    Kl = [[[sp.Rational(1, 2) * (Tl[l][m][n] - Tl[m][n][l] + Tl[n][l][m])
            for n in range(4)] for m in range(4)] for l in range(4)]
    Ku = [[[sum(gi[a, l] * Kl[l][m][n] for l in range(4))
            for n in range(4)] for m in range(4)] for a in range(4)]
    Gam = [[[GamLC[a][m][n] + Ku[a][m][n] for n in range(4)] for m in range(4)] for a in range(4)]

    # --- Riemann R^a_{s m n} ---
    R = [[[[None] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for sg in range(4):
            for m in range(4):
                for n in range(4):
                    e = (sp.diff(Gam[a][n][sg], XX[m]) - sp.diff(Gam[a][m][sg], XX[n])
                         + sum(Gam[a][m][l] * Gam[l][n][sg] for l in range(4))
                         - sum(Gam[a][n][l] * Gam[l][m][sg] for l in range(4)))
                    R[a][sg][m][n] = e
    Ric = [[sum(R[a][sg][a][n] for a in range(4)) for n in range(4)] for sg in range(4)]
    Rs = sum(gi[i, j] * Ric[i][j] for i in range(4) for j in range(4))
    E = [[Ric[m][n] - sp.Rational(1, 2) * g[m, n] * Rs + Lam * g[m, n] for n in range(4)]
         for m in range(4)]

    def nabla02(A, al, m, n):
        return (sp.diff(A[m][n], XX[al])
                - sum(Gam[l][al][m] * A[l][n] for l in range(4))
                - sum(Gam[l][al][n] * A[m][l] for l in range(4)))

    def div02(A):
        out = []
        for n in range(4):
            tot = 0
            for m in range(4):
                for a in range(4):
                    if gi[m, a] == 0:
                        continue
                    tot += gi[m, a] * nabla02(A, a, m, n)
            out.append(tot)
        return out

    # --- 公理 2 的两项挠率修正 ---
    def nabla03(T, b, a, m, n):
        return (sp.diff(T[a][m][n], XX[b])
                - sum(Gam[l][b][a] * T[l][m][n] for l in range(4))
                - sum(Gam[l][b][m] * T[a][l][n] for l in range(4))
                - sum(Gam[l][b][n] * T[a][m][l] for l in range(4)))

    divT = [[sum(gi[a, b] * nabla03(Tl, b, a, m, n)
                 for a in range(4) for b in range(4) if gi[a, b] != 0)
             for n in range(4)] for m in range(4)]
    TT = [[sum((sum(gi[be, l] * Tl[m][al][l] for l in range(4)))
               * (sum(gi[al, sg] * Tl[be][n][sg] for sg in range(4)))
               for al in range(4) for be in range(4))
           for n in range(4)] for m in range(4)]
    LHS = [[E[m][n] + divT[m][n] - TT[m][n] for n in range(4)] for m in range(4)]
    return dict(g=g, gi=gi, GamLC=GamLC, Kl=Kl, Ku=Ku, Gam=Gam, R=R, Ric=Ric, Rs=Rs,
                E=E, divT=divT, TT=TT, LHS=LHS, Tl=Tl, div02=div02)

print("  [C] 挠率关（阳性对照）...")
B0 = build(False)
print("  [C] 挠率开（主检验）...")
B1 = build(True)

# ---- 代码自身守卫（先验工具，再用于判定）----
ok_c0 = True
for n in range(4):
    z, _ = is_zero(B0["div02"](B0["E"])[n])
    ok_c0 = ok_c0 and z
guard("G-C0 无挠率 Bianchi 恒零", ok_c0,
      "阳性对照：T=0 时 ∇^μ(R_μν-½g_μνR+Λg_μν) 必须逐分量恒零，否则本管线有 bug")

ok_c1 = True
for al in range(4):
    for m in range(4):
        for n in range(4):
            e = (sp.diff(B1["g"][m, n], XX[al])
                 - sum(B1["Gam"][l][al][m] * B1["g"][l, n] for l in range(4))
                 - sum(B1["Gam"][l][al][n] * B1["g"][m, l] for l in range(4)))
            z, _ = is_zero(e)
            ok_c1 = ok_c1 and z
guard("G-C1 含挠率度量相容", ok_c1, "∇_λ g_μν 必须为 0（含挠率联络）")

ok_c2, ok_c3 = True, True
for l in range(4):
    for m in range(4):
        for n in range(4):
            z, _ = is_zero(B1["Kl"][l][m][n] + B1["Kl"][n][m][l]); ok_c2 = ok_c2 and z
            z, _ = is_zero(B1["Kl"][l][m][n] - B1["Kl"][l][n][m] - B1["Tl"][l][m][n]); ok_c3 = ok_c3 and z
guard("G-C2 挠率张量反对称 K_lmn=-K_nml", ok_c2, "contortion 定义自检")
guard("G-C3 挠率还原 K_lmn-K_lnm=T_lmn", ok_c3, "contortion 必须还原出给定挠率")

ok_c4 = True
for a in range(4):
    for sg in range(4):
        for m in range(4):
            for n in range(4):
                z, _ = is_zero(B1["R"][a][sg][m][n] + B1["R"][a][sg][n][m])
                ok_c4 = ok_c4 and z
guard("G-C4 Riemann 反对称于 (m,n)", ok_c4, "Riemann 定义自检")

# ---- 主检验 1：含挠率时 Einstein 部分的散度 ----
dEin = B1["div02"](B1["E"])
ze = [is_zero(v)[0] for v in dEin]
mg = [magnitude(v) for v in dEin]
add("C01", "FAIL" if not all(ze) else "PASS", "含挠率时 ∇^μ G_μν(Γ) 是否守恒",
    "挠率开启后，∇^μ(R_μν-½g_μνR+Λg_μν) 逐分量恒零判据 = %s；在点采样处量级 = %s。"
    "（Λg_μν 项因度量相容恒为零，不参与。）若非恒零，则该 Einstein 张量不能用 ∇^(Γ) 定义守恒流。"
    % (ze, ["%.6E" % v for v in mg]),
    {"zero_flags": ze, "magnitudes": ["%.6E" % v for v in mg]})

# ---- 主检验 2：公理 2 完整 LHS 的散度 ----
dL = B1["div02"](B1["LHS"])
zl = [is_zero(v)[0] for v in dL]
ml = [magnitude(v) for v in dL]
add("C02", "FAIL" if not all(zl) else "PASS", "公理 2 完整 LHS 的协变散度（拒证判据）",
    "LHS_μν = R_μν-½g_μνR+Λg_μν+∇^αT_αμν-T_μα^βT_βν^α，其 ∇^μ 逐分量恒零判据 = %s，点采样量级 = %s。"
    "若非恒零，则在 RHS 取标准物质能动张量（满足 ∇·T=0）时，公理 2 **把 0 约束为非 0** ⇒ "
    "按来稿 §一.1 自设条款『散度不守恒 → 直接标记公理不自洽，拒证』，该式在本口径下判不自洽。"
    % (zl, ["%.6E" % v for v in ml]),
    {"zero_flags": zl, "magnitudes": ["%.6E" % v for v in ml]})

# ---- 主检验 3：LHS 的反对称部分 vs 对称物质源 ----
anti = [[sp.cancel(B1["LHS"][m][n] - B1["LHS"][n][m]) for n in range(4)] for m in range(4)]
za = [is_zero(anti[m][n])[0] for m in range(4) for n in range(m + 1, 4)]
ma = [magnitude(anti[m][n]) for m in range(4) for n in range(m + 1, 4)]
add("C03", "FAIL" if not all(za) else "PASS", "LHS 的反对称部分 vs 对称物质能动张量",
    "∇^αT_αμν 因挠率反对称于 (μ,ν) 而是**反对称**张量；含挠率 Ricci 一般也不对称。"
    "LHS_{[μν]} 恒零判据 = %s，点采样量级 = %s。若非恒零，则公理 2 要求『对称的 T_μν = 含反对称部分的 LHS』，"
    "除非把 RHS 换成含自旋的**非对称**正则能动张量（标准 EC 正是如此）——但母册 L39 明写 T_μν 为『物质能动张量』，未声明非对称 ⇒ 口径未登记。"
    % (za, ["%.6E" % v for v in ma]),
    {"zero_flags": za, "magnitudes": ["%.6E" % v for v in ma]})

# ---- 主检验 4：反对称部分在无挠率时是否消失（阳性对偶）----
anti0 = [[sp.cancel(B0["LHS"][m][n] - B0["LHS"][n][m]) for n in range(4)] for m in range(4)]
z0 = all(is_zero(anti0[m][n])[0] for m in range(4) for n in range(4))
guard("G-C5 无挠率 LHS 对称", z0, "T=0 时 LHS 必须对称（Einstein 张量对称性）")
add("C05", "BOUNDARY", "诚实边界：C01/C02 的非零散度**不等于** EC 理论本身错",
    "标准 Einstein–Cartan 中，含挠率联络的 Einstein 张量**本来就不满足** ∇^(Γ)·G=0；"
    "它的一致性由两件事共同保证：(a) 第二条场方程（Cartan 式，变分联络得到 T∝自旋）；"
    "(b) 物质侧用**含自旋的正则能动张量**，其 ∇^(Γ)·T 恰由曲率×自旋项补偿而非零。"
    "⇒ C01/C02 的正确读法是：**公理 2 单独一条 + 母册 L39 的『物质能动张量』（默认对称、按标准守恒）"
    "这两者联立时才是矛盾的**。要解除矛盾必须同时补 (a) 与 (b)，而母册两处均未登记 ⇒ "
    "这不是『EC 被否证』，而是『母册登记的版本相对标准 EC 缺了两件东西』（与 D01/D02 同一根因）。",
    {"needs": ["第二条场方程(Cartan式)", "非对称正则能动张量"]})
add("C04", "PASS" if z0 else "FAIL", "零挠率极限 LHS 恢复对称（与 GR 一致）",
    "T=0 时 LHS_{[μν]} 恒零 = %s ⇒ 公理 2 在零挠率极限退化为标准 Einstein+Λ 方程，"
    "**结构上**平滑回 GR。注意：这是定义性恒真（任何『GR + 挠率附加项』写法都满足），"
    "不构成对 TUFT 的证据（换任意挠率附加项结果不变）。" % z0, {"zero": z0})
# =====================================================================
# D 段 · 结构闭合性：自由度计数 / 挠率传播阶 / 挠率晕两难
# =====================================================================
n_g   = 10                        # 对称 g_{mu nu}
n_T   = 4 * 6                     # T^a_{mn} 反对称于 (m,n)：4 * C(4,2)
n_unk = n_g + n_T
n_eq_sym, n_eq_full = 10, 16
add("D01", "FAIL", "自由度计数：公理 2 单条方程对 (g,T) 欠定",
    "未知量 = g_{μν}(%d) + T^α_{μν}(%d) = %d；公理 2 只给 1 个张量方程 "
    "（按对称部分 %d 个分量 / 按全分量 %d 个）⇒ 欠定 %d 或 %d 个自由度。"
    "标准 Einstein–Cartan 是**一对**方程（变分度规给的爱因斯坦式 + 变分联络给的 Cartan 式 T∝自旋）；"
    "母册只登记了前者 ⇒ **方程组不闭合**。" % (n_g, n_T, n_unk, n_eq_sym, n_eq_full,
                                            n_unk - n_eq_sym, n_unk - n_eq_full),
    {"unknowns": n_unk, "eq_sym": n_eq_sym, "eq_full": n_eq_full,
     "deficit_sym": n_unk - n_eq_sym, "deficit_full": n_unk - n_eq_full})

term_order = {                     # 各项对各场的导数阶
    "R_mn":               {"g": 2, "T": 0},
    "Lambda*g_mn":        {"g": 0, "T": 0},
    "nabla^a T_amn":      {"g": 0, "T": 1},
    "T*T":                {"g": 0, "T": 0},
}
maxT = max(v["T"] for v in term_order.values())
maxg = max(v["g"] for v in term_order.values())
add("D02", "FAIL", "挠率无传播方程：公理 2 对 T 的最高导数阶 = 1，无 □T",
    "逐项导数阶：%s ⇒ T 的最高阶 = %d，g 的最高阶 = %d。"
    "传播（波动型）自由度需要对该场出现**二阶**导数（□T）；公理 2 对 T 只出现一阶散度 ∇^αT_αμν，"
    "是约束型而非双曲型 ⇒ **挠率不传播**（真空中无挠率波）。这与 r27 的『L_tau 退化 ⇒ τ 不传播』同构，"
    "本册把它首次接到预言 A/B 上做后果推演。" %
    ("; ".join("%s:g%d/T%d" % (k, v["g"], v["T"]) for k, v in term_order.items()), maxT, maxg),
    {"max_order_T": maxT, "max_order_g": maxg})
guard("G-D2 挠率最高一阶", maxT == 1 and maxg == 2, "g 应二阶、T 应一阶")

# ---- 定量：挠率要撑起暗物质晕，需要多大 τ / 多大自旋密度 ----
c_  = Decimal("299792458")
G_  = Decimal("6.67430E-11")
hb_ = Decimal("1.054571817E-34")
mp_ = Decimal("1.67262192E-27")
pi_ = Decimal("3.14159265358979323846264338327950288419716939937510")
c4_8piG = c_ ** 4 / (8 * pi_ * G_)         # N
c3_8piG = c_ ** 3 / (8 * pi_ * G_)         # kg/s
rho_DM  = Decimal("4.806E-5")              # J/m^3  (0.3 GeV/cm^3 能量密度)
tau_need = (rho_DM / c4_8piG).sqrt()       # m^-1
L_tau    = Decimal(1) / tau_need           # m
MPC      = Decimal("3.0856775814913673E22")
s_req    = tau_need * c3_8piG              # kg m^-1 s^-1（自旋密度量纲）
rho_b    = Decimal("5.0E-22")              # 星系晕处重子质量密度量级 kg/m^3
n_b      = rho_b / mp_
s_halo   = (hb_ / 2) * n_b
n_nuc    = Decimal("1.6E44")               # 核密度 m^-3
s_nuc    = (hb_ / 2) * n_nuc
r_halo   = s_req / s_halo
r_nuc    = s_req / s_nuc
add("D03", "INFO", "挠率撑起暗物质晕所需 τ 的量级（系数取自公理 2 自身的 T·T 项）",
    "把公理 2 的 −T_{μα}^βT_{βν}^α 移项到右端，等效能量密度 ρ_eff ≈ (c⁴/8πG)·τ²。"
    "令 ρ_eff = 局域暗物质密度 %s J/m³ ⇒ τ_需 = %s m⁻¹（特征尺度 1/τ = %s m = %s Mpc）。"
    "注意该尺度（%s Mpc）已远大于星系晕尺度（~0.1 Mpc）⇒ 若把 τ 取成晕尺度 1/(0.1 Mpc)，"
    "其等效能量密度会**过冲**约 %s 倍（≈2 个量级）；这本身就是一条独立于自旋论证的拟合张力。"
    % (fs(rho_DM), fs(tau_need), fs(L_tau), fs(L_tau / MPC), fs(L_tau / MPC),
       fs((Decimal("0.1") * MPC) ** -2 / tau_need ** 2)),
    {"c4_over_8piG": fs(c4_8piG), "tau_need_m^-1": fs(tau_need),
     "scale_m": fs(L_tau), "scale_Mpc": fs(L_tau / MPC),
     "overshoot_at_0.1Mpc": fs((Decimal("0.1") * MPC) ** -2 / tau_need ** 2)})
add("D04", "FAIL", "若补标准 EC Cartan 方程（挠率 ∝ 自旋密度），挠率晕所需自旋密度超星系晕可得上限 39.5 个量级",
    "Cartan 方程把挠率**代数地**绑到局域自旋密度：s ≈ τ·c³/(8πG)（量纲唯一确定到无量纲 O(1) 因子）。"
    "代入 D03 的 τ_需 ⇒ s_需 = %s kg·m⁻¹·s⁻¹。对照：星系晕处重子（ρ_b≈%s kg/m³）**全部极化**也只有 "
    "s_晕 = (ℏ/2)·n_b = %s ⇒ 欠缺 %s 倍 ≈ **39.5 个数量级**，远超任何 O(1) 系数不确定度 ⇒ "
    "该分支被定量否证。诚实标注：若改用**核密度**参照（n=%s m⁻³，s_核=%s），缺口仅 %s 倍，"
    "落在系数不确定度内 ⇒ 核密度参照**不能**作为否证依据，本册不引用它下结论；"
    "真正承重的是星系晕处那 39.5 个量级（暗晕恰恰在重子稀薄处，这正是要害）。"
    % (fs(s_req), fs(rho_b), fs(s_halo), fs(r_halo), fs(n_nuc), fs(s_nuc), fs(r_nuc)),
    {"s_req": fs(s_req), "s_halo_polarized": fs(s_halo), "gap_halo": fs(r_halo),
     "s_nuclear": fs(s_nuc), "gap_nuclear": fs(r_nuc)})
add("D05", "FAIL", "★承重裁定：预言 A（挠率涡旋暗物质晕）落入『不闭合 ⇔ 不可证伪』两难",
    "分支 (i) **不补第二条场方程**：τ(r) 是自由函数（24 维欠定，D01），任何旋转曲线都能被某个 τ(r) 拟合 ⇒ "
    "零判别力、不可证伪（与 r107 判 K 自由同一病根，但此处不依赖 τ 的具体形式，是结构级的）。"
    "分支 (ii) **补标准 EC Cartan 方程**：挠率代数地由自旋密度决定、不传播（D02）、真空恒零 ⇒ "
    "延伸到无物质区的『涡旋晕』不可能存在（D04 定量欠缺 40 个量级）。"
    "⇒ 预言 A 只在『既不闭合又不可证伪』的缝隙里成立：**这不是可检验预言，是欠定拟合框架**。"
    "同理，挠率不传播 ⇒ 真空中无挠率波 ⇒ 预言 B 的『传播过程累积的挠率相位漂移』在公理 2 下恒为零。",
    {"branch_i": "欠定24维·零判别力", "branch_ii": "Cartan代数·真空τ=0·不传播"})

# =====================================================================
# E 段 · 三元理（三态尺度代数）：构造模型穷举
# =====================================================================
add("E01", "BOUNDARY", "三元理审计的前置结论：运算定义缺失 ⇒ 自洽性审计的输入不存在",
    "r28（判定册 L318）已判：『三态尺度代数』要求运算+封闭性+单位元，而全表无任何运算定义。"
    "本册据此确认：**在没有运算表之前，『三元理是否自洽』既不能判真也不能判假**——"
    "缺失的是公理输入，不是一致性。来稿 §四.C 要求『构造模型』，本册用穷举代替猜测（E02/E03）。", {})
cells = list(itertools.product(range(3), repeat=9))    # 3^9 = 19683
cnt_assoc = cnt_comm_assoc = cnt_monoid = cnt_monoid_id1 = cnt_group = 0
for tab in cells:
    op = [[tab[3 * a + b] for b in range(3)] for a in range(3)]
    assoc = all(op[op[a][b]][cc] == op[a][op[b][cc]] for a in range(3) for b in range(3) for cc in range(3))
    if not assoc:
        continue
    cnt_assoc += 1
    if not all(op[a][b] == op[b][a] for a in range(3) for b in range(3)):
        continue
    cnt_comm_assoc += 1
    ids = [e for e in range(3) if all(op[e][a] == a and op[a][e] == a for a in range(3))]
    if not ids:
        continue
    cnt_monoid += 1
    if 1 in ids:
        cnt_monoid_id1 += 1
        if all(any(op[a][b] == ids[0] for b in range(3)) for a in range(3)):
            cnt_group += 1
add("E02", "INFO", "三元理代数模型穷举（3^9 = 19683 张二元运算表）",
    "在 {0,1,∞} 上穷举全部二元运算，筛选：结合 %d 个 → 结合+交换 %d 个 → 含幺交换半群 %d 个 → "
    "（其中单位元恰为『1』）%d 个 → 构成群 %d 个。"
    "⇒ **存在**自洽的代数结构，因此三元理不与自身矛盾；但可行结构不止一个。" %
    (cnt_assoc, cnt_comm_assoc, cnt_monoid, cnt_monoid_id1, cnt_group),
    {"assoc": cnt_assoc, "comm_assoc": cnt_comm_assoc, "monoid": cnt_monoid,
     "monoid_id_is_1": cnt_monoid_id1, "group": cnt_group})
add("E03", "FAIL", "三元理欠定：可行代数结构多种互不等价 ⇒ 无判别力",
    "满足『含幺交换半群』的运算表有 %d 张（单位元为 1 的 %d 张），彼此给出不同的物理映射 ⇒ "
    "在未指定运算表前，任何『由三元理推出 X』的推导都隐含了一个未声明的选择，"
    "选择自由度 ≥ log₂(%d) = %.4f bit。这不是『三元理错』，而是『三元理尚未定义到可判定的粒度』。" %
    (cnt_monoid, cnt_monoid_id1, max(cnt_monoid, 1), float(Decimal(max(cnt_monoid, 1)).ln() / Decimal(2).ln())),
    {"monoid": cnt_monoid, "choice_bits": "%.6f" % float(Decimal(max(cnt_monoid, 1)).ln() / Decimal(2).ln())})
cliff_dims = [2 ** n for n in range(0, 9)]
add("E04", "FAIL", "『三元理是克利福德代数/场代数的超集』在向量空间维数层即被否证",
    "实克利福德代数的维数只能取 %s（2^n）；三元理的载体是 3 个元素的集合/3 维代数，"
    "维数 3 ∉ {2^n} ⇒ 不可能作为克利福德代数的超集或与其同构。来稿 §四.C 的『超集』目标在该读法下不可达；"
    "若『超集』指的是分类学覆盖而非代数嵌入，则它不是代数命题，应降级为分类框架（r29 方向丙同结论）。" %
    str(cliff_dims[:9]), {"clifford_dims": cliff_dims[:9]})

# =====================================================================
# F 段 · 分工声明 / 拒证条款 / 批次裁决
# =====================================================================
add("F01", "INFO", "与既有册的分工（零重复计数）",
    "r107：判『τ_φ∝1/r + K 自由』这一支实现 FAIL（本册不重审该形式，改判结构层）。"
    "r28/r29：判『三元理无运算定义』+『映射信息缺口 2.585 bit』（本册只补代数模型穷举 E02/E03，不重复计数信息量）。"
    "r27/GMUFT：判『τ 不传播』（本册首次把它接到预言 A/B 上做后果推演 D02/D05）。"
    "本册新增且此前无人登记的：A02/A03/A05（公理 3 三口径互斥 + 平直极限相反）、"
    "C01–C03（含挠率散度，全库首次）、D01/D02/D05（欠定 + 不传播 + 挠率晕两难）。", {})
add("F02", "INFO", "★流程裁决：来稿 §五 的前提不成立——第一批探针只锁定、未落盘",
    "攻破目录 README L10 只写『第一批攻坚锁定 T147/T712/T947/T163（Decimal 250 位）』；"
    "全仓检索无对应 attack/判定落盘产物 ⇒ 第一批**尚未执行**。"
    "来稿 §五.1 直接排第二批（T163/T141/T210/T749）会与第一批重叠（T163 同时出现在两批）。"
    "建议顺序：先补第一批落盘 → 再排第二批（去重后为 T141/T210/T749 + 新补 1 项）；"
    "且第一层（本册）的 A02/A03 口径冲突未仲裁前，任何把 κ 代入探针式的计算都会继承该歧义。", {})
add("F03", "PASS", "拒证条款（按来稿 §三，逐条给出执行判据）",
    "R1 PTA：HD 角相关在误差内无挠率形变 ⇒ 全局挠率振幅上限压低。但 D02 已证公理 2 下挠率不传播 ⇒ "
    "本版本**先验地**预测零形变，R1 只能压上限不能区分（判据失效，须先修 D01/D02）。"
    "R2 磁星双折射：同理，光子-挠率耦合在公理 2 中不存在（公理 2 只有引力扇区）⇒ 该检验需要先补耦合项，"
    "补了就是新自由度，须登记外部输入。"
    "R3 EHT 阴影：零挠率极限回 GR（C04）⇒ 本版本先验预测与 Kerr 一致，R3 同样只能压上限。"
    "⇒ **三条拒证条款在本版本下全部退化为『上限约束』，无一条具备区分力**——根因是 D05 的两难，不是实验精度不够。",
    {"r1": "先验零形变·仅上限", "r2": "耦合项未定义·需新自由度", "r3": "零挠率回GR·仅上限"})

add("F04", "INFO", "最小修法清单（按代价升序，不代选，须用户裁决）",
    "P1【零成本】公理 3 的 κ 改名为 Q（=κ_F²+τ²）并显式登记口径（解 A02/A03/A05）。"
    "P2【零成本】在母册明文声明 RHS 的 T_μν 是否为含自旋的非对称正则能动张量（解 C03 的口径未登记）。"
    "P3【零成本】登记是否采用标准 EC 第二条场方程（Cartan 式 T∝自旋）——登记后 C05 的矛盾自动解除，"
    "但代价是 D05 分支 (ii) 生效 ⇒ **预言 A 被否证**（真空 τ≡0、挠率不传播）。"
    "P4【+1 动力学场】若要保住预言 A，必须给挠率加动能项（□T / (∇T)²），"
    "即引入挠率传播自由度 ⇒ 不再是标准 EC，且与『无新粒子』叙事的节俭性主张冲突，须登记为新公设 + 新参数。"
    "P5【+1 耦合】若要保住预言 C（磁星双折射），需补光子–挠率耦合项 ⇒ 新自由度，同样须登记。"
    "⇒ **P1/P2/P3 是必做的记账；P4/P5 是路线选择，代价都是新增自由度**。",
    {"P1": "κ→Q 改名·零成本", "P2": "声明 T_μν 对称性·零成本",
     "P3": "登记 Cartan 式·零成本但否证预言A", "P4": "挠率动能项·+1场", "P5": "光子-挠率耦合·+1耦合"})

# =====================================================================
# 输出
# =====================================================================
LV = ["PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO", "MISMATCH"]
cnt = {k: sum(1 for e in ENTRIES if e["level"] == k) for k in LV}
gok = sum(1 for g_ in GUARDS if g_["ok"])
title = "TUFT-r174 三本源公理闭合审计（第一层·前置关卡） 2026-10-24"
lines = [title, "=" * 78, ""]
for e in ENTRIES:
    lines.append("[%s] %s · %s" % (e["level"], e["code"], e["title"]))
    lines.append("    " + e["detail"])
    if e["numbers"]:
        lines.append("    numbers: " + json.dumps(e["numbers"], ensure_ascii=False))
    lines.append("")
lines.append("条目 %d（%s）" % (len(ENTRIES), " ".join("%s=%d" % (k, cnt[k]) for k in LV)))
lines.append("守卫 %d/%d" % (gok, len(GUARDS)))
rep = "\n".join(lines)
print(rep)

payload = dict(title=title, generated="2026-10-24", round="r174",
               source=["TUFT母册底层总纲_分层收口_2026-10-24.md",
                       "布局_剩余项分层归档_2026-10-24.md",
                       "用户《TUFT 验证与应用全方案》2026-10-24"],
               entries=ENTRIES, guards=GUARDS,
               counts=cnt, guard_pass=gok, guard_total=len(GUARDS))
stem = "TUFT-r174_三本源公理闭合审计_2026-10-24"
(OUTD / (stem + ".json")).write_text(
    json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
(OUTD / (stem + "_report.txt")).write_text(rep, encoding="utf-8")
md = ["# " + title, "",
      "> 源码：`源码/TUFT-r174_三本源公理闭合审计_2026-10-24.py`",
      "> 数据：`数据/%s.{json,_report.txt}`" % stem, "",
      "## 读数", "",
      "条目 **%d**（%s）｜守卫 **%d/%d**｜退出码 0" %
      (len(ENTRIES), " ".join("%s=%d" % (k, cnt[k]) for k in LV), gok, len(GUARDS)), "",
      "## 条目", ""]
for e in ENTRIES:
    md.append("### %s · %s · %s" % (e["code"], e["level"], e["title"]))
    md.append("")
    md.append(e["detail"])
    md.append("")
md.append("## 守卫")
md.append("")
md.append("| 守卫 | 结果 |")
md.append("|---|---|")
for g_ in GUARDS:
    md.append("| %s | %s |" % (g_["name"], "PASS" if g_["ok"] else "FAIL"))
(OUTD / (stem + ".md")).write_text("\n".join(md), encoding="utf-8")
print("\n[OK] 条目 %d / 守卫 %d/%d" % (len(ENTRIES), gok, len(GUARDS)))
sys.exit(0)
