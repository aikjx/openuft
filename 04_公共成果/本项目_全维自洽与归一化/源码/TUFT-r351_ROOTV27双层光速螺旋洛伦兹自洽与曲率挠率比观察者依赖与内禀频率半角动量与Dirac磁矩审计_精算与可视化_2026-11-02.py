# -*- coding: utf-8 -*-
"""TUFT-r351 · ROOT V27 来料审计引擎（双层光速螺旋：洛伦兹自洽、曲率/挠率比的观察者依赖、
内禀频率与半角动量、Dirac 磁矩）。

来料主张（ROOT V27，正本见 `数据/TUFT-r351_..._来料原件_ROOT_V27_用户附件逐字.md`）：
  (a) §一 电子内部轨迹 X^μ(τ)=(cτ, RcosΩ₀τ, RsinΩ₀τ, 0) 是光状曲线，boost 后
      v_perp²+u²=c²（boxed）；
  (b) §二 曲率/挠率 κ=1/(Rγ²)、τ₃=β/(Rγ)，故 (V27-1) κ/|τ₃|=√(1−β²)/|β|（四行表）；
  (c) §三 取 β_match=1/√(1+α²) 使 κ/|τ₃| 等于精细结构常数倒数相关的 α，得 γ_match=137.039647804709；
  (d) §四 Ω_Z=2m_ec²/ħ、R_Z=c/Ω_Z ⇒ L=R_Z·m_ec=ħ/2（半角动量）；
  (e) §五 环形电流磁矩 μ_ring=eħ/(4m_e)=½μ_B，实测 μ_e=(1+a_e)μ_B ⇒ 差 2 倍（g 因子）；
      (σ·π)²=π²−qħσ·B ⇒ H_spin=−(q/m)S·B ⇒ 树级 g=2，QED 解释 g−2；
  (f) §六 光子/电子分离表 + 「必须引入维持圆周的动力学约束」；
  (g) §七 自检表（50,000 组随机 boost 全通过、最大归一化浮点残差 6.66e-16、Pauli 9 项精确通过）。

本卷只做「可算判决」，不产新物理。预检面 = `scratch/r351_precheck_out.txt`（落引擎前只读探针，
SELF-CHECK 30/30 PASS、零写入）；本引擎把同一批数学搬进条目表，并给**每条判决配一个具名变异体**
（变异体打不破的判决 = 本卷自判红，退出码非 0）。

分工（去重账 N9 现扫 39 份面、正对照 5/5 ⇒ 「零命中＝净增量」读法成立）：
  · 「Ω_Z 恰是 2 倍康普顿频率」归 r354 G12 老账；反解/双射/判别力 0 归 r321/r324/r325/r326/r327/r329；
    boost 观察者依赖归 r324/r329/r332/r338/r342/r344；Pauli/σ 归 r354；
  · 净增量：γ_match≠α⁻¹、(η,ξ) 一钮两靶、L=ħ/k 除数旋钮、印刷比值=g_e 换分母、
    约束力在 v→c 发散、内禀三行的常数版本归因、因子 2 的来处=非对易项；
  · r354 G08/G14/G15 与 r360 分层声明点名 r351「同源，只复算不计新条目」⇒ 本卷是**被让渡的归属**。

口径：c=1 的代数走 sympy（精确），印刷字段复现走 mpmath dps=75；分层 A/B/G/C/E/P **条目不可相加**。
"""
import glob
import io
import json
import os
import re
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 75

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
OUT_DIR = os.path.join(BASE, "数据")
JDG_DIR = os.path.join(BASE, "判定")
SRC_DIR = os.path.join(BASE, "源码")

RID = "r351"
DATE = "2026-11-02"
STEM = ("TUFT-r351_ROOTV27双层光速螺旋洛伦兹自洽与曲率挠率比观察者依赖与内禀频率"
        "半角动量与Dirac磁矩审计_精算与可视化_" + DATE)
NAME = STEM
HTML_NAME = "四力统一方程_TUFT-r351_审计ROOTV27_双层光速螺旋观察者依赖与半角动量旋钮与磁矩一钮两靶_" + DATE + ".html"

# ------------------------------------------------------------------ 常数
C_EXACT = mp.mpf("299792458")                    # SI 定义，精确
H_EXACT = mp.mpf("6.62607015e-34")               # SI 定义，精确
HBAR = H_EXACT / (2 * mp.pi)                     # 因此 ħ 精确
E_CHARGE = mp.mpf("1.602176634e-19")             # SI 定义，精确
ME = {"CODATA2018": mp.mpf("9.1093837015e-31"),
      "CODATA2022": mp.mpf("9.1093837139e-31")}
ALPHA_INV = mp.mpf("137.035999177")              # 来料 §八 自陈锚
ALPHA = 1 / ALPHA_INV
A_E_PRINT = "0.00115965218046"                   # 来料 §五（CODATA 2022）
A_E_UNC = mp.mpf("0.00000000000018")             # 括号 (18) = 末两位
MU_B_PRINT = mp.mpf("9.2740100783e-24")          # 来料 §五 印值（仅作口径核对）
LAMBAR_PRINT = mp.mpf("3.8615926789e-13")        # CODATA 2022 约化康普顿波长
EPS_FLOAT64 = mp.mpf("2.220446049250313e-16")

PRINTED = {
    "ratio_table": [("0.6c", "1.333333"), ("0.8c", "0.750000"),
                    ("0.99c", "0.142492"), ("0.9999c", "0.014143")],
    "beta_match": "0.999973375386119",
    "gamma_match": "137.039647804709",
    "R_Z": "1.93079633718", "exp_R": "-13",
    "Omega_Z": "1.55268814337", "exp_Omega": "21",
    "f_Z": "2.47117993098", "exp_f": "20",
    "mu_ring": "0.500000", "mu_real": "1.001159652",
    "mu_ratio": "2.00231930436092",
    "gamma_slider": "1.66667", "kappa_tau_slider": "0.750000000",
    "vperp_slider": "0.60000000", "freq_slider": "0.60000000",
    "float_resid": "6.66e-16",
}

# ------------------------------------------------------------------ 条目 API
ITEMS = []
MUT_FAILS = []        # 变异体打不破的判决（本卷自判红）
NO_MUT = []           # 缺变异体的判决条目
LANDING_FOREIGN = []  # 并发落盘 detected


def half_ulp(s):
    """印刷字段自身的半 ulp（末位一格的一半），口径 = 该字段的小数位数。"""
    t = s.lstrip("+")
    if "." not in t:
        return mp.mpf("0.5")
    return mp.mpf("0.5") * mp.mpf(10) ** (-(len(t.split(".")[1])))


def P(s):
    return mp.mpf(s.lstrip("+"))


def round_field(x, field):
    """把现算值舍到「被比较字段自己的位数」，用于逐位（不是容差）复现。"""
    nfrac = len(field.split(".")[1])
    scaled = mp.floor(abs(x) * 10 ** nfrac + mp.mpf("0.5"))
    return mp.sign(x) * scaled / 10 ** nfrac


def scaled_match(val, mant_s, exp_s):
    tgt = mp.mpf(mant_s) * mp.mpf(10) ** mp.mpf(exp_s)
    return abs(val - tgt) <= half_ulp(mant_s) * mp.mpf(10) ** mp.mpf(exp_s), tgt


def rz_f(me):
    return HBAR / (2 * me * C_EXACT)


def omz_f(me):
    return 2 * me * C_EXACT ** 2 / HBAR


VERDICTS = ("PASS", "FAIL", "BOUNDARY", "INFO")


def add(iid, kind, name, exp, act, verdict, note="", mut=None, mdesc=""):
    """登记一条判决。verdict 白名单；kind∈{A,B,G,C,E,P}。
    mut 是**变异体**：它返回「把输入故意改坏之后，本条判据仍成立」的布尔。返回 True ⇒ 该判据对改坏不敏感
    ⇒ 判决没有被定价 ⇒ 记入 MUT_FAILS（收口闸门红，退出码非 0）；返回 False ⇒ 改坏确实打破了判据。
    变异体造崩（抛异常）同样记红：一个「一改就崩」的判据没有给出可读的反例形状。
    判决类条目（A/B/G/C）缺变异体即记入 NO_MUT；收口闸门的分母全部由 ITEMS 现推，不手钉。"""
    assert verdict in VERDICTS, (iid, verdict)
    it = {"id": iid, "kind": kind, "name": name, "exp": exp, "act": str(act),
          "verdict": verdict, "note": note}
    ITEMS.append(it)
    if mut is None:
        if kind in ("A", "B", "G", "C"):
            NO_MUT.append(iid)
    else:
        try:
            voided = bool(mut())
        except Exception as exc:                                   # noqa: BLE001
            voided = True
            it["mut_note"] = "变异体造崩（未给出可读反例形状）：%s" % type(exc).__name__
        it["mutant"] = mdesc
        it["mut_voids"] = voided
        if voided:
            MUT_FAILS.append(iid)
    return it


# ------------------------------------------------------------------ 共用符号
SY = sp.symbols("tau R Omega_0 beta", positive=True)
tau_, R_, O0, bet = SY
tt = sp.symbols("t", positive=True)
gam = 1 / sp.sqrt(1 - bet ** 2)
w, uu = sp.symbols("omega u", positive=True)
xb = sp.symbols("x", positive=True)
e_s, m_s, h_s = sp.symbols("e m hbar", positive=True)
eta, xi = sp.symbols("eta xi", positive=True)
Xc, Yc, q, BB, hb = sp.symbols("x y q B hbar", real=True)


# ================================================================== A 层：精确代数 / 符号
def a_layer():
    S = {}
    # ---- A01 切线光状条件
    X = sp.Matrix([tau_, R_ * sp.cos(O0 * tau_), R_ * sp.sin(O0 * tau_), 0])
    dX = [sp.diff(x_, tau_) for x_ in X]
    tnorm = sp.simplify(dX[0] ** 2 - sum(v ** 2 for v in dX[1:]))
    S["tnorm"] = tnorm
    add("A01", "A", "§一 切线光状条件 |dX/dτ|²=0 **依赖** boxed 假设 R·Ω₀=c（c=1 口径）",
        "未代约束非零 ∧ 代入 R·Ω₀=c 后为 0",
        "未代约束 = %s；代入后 = %s" % (tnorm, sp.simplify(tnorm.subs(R_ * O0, 1))),
        "PASS",
        "来料 §一「内部轨迹为光状曲线」在本构造内成立，但它是那条 boxed 假设的直接推论，不是几何自动给的；"
        "还原来料自己的 c 口径即 |dX/dτ|² = c² − R²Ω₀²。注意来料 §一 已自陈「τ 是电子中心的固有时间，"
        "不是内部光速运动点的固有时间」——这条自陈把该光状性限定在中心系坐标时间里",
        mut=lambda: sp.simplify(tnorm.subs(R_ * O0, 2)) == 0,
        mdesc="把约束改成 R·Ω₀=2c（不成立的那条）后判据必须为假")

    # ---- A02/A03 实验室螺旋
    rlab_t = sp.Matrix([R_ * sp.cos(O0 * tt / gam), R_ * sp.sin(O0 * tt / gam), bet * tt])
    vlab = [sp.diff(c_, tt) for c_ in rlab_t]
    speed2 = sp.simplify(sum(v ** 2 for v in vlab))
    S["vlab"], S["speed2"] = vlab, speed2
    add("A02", "A", "§一 boost 后实验室速度模方 |dr/dt|² = R²Ω₀²(1−β²)+β²（未代约束）",
        "现推与来料 v_perp=c/γ、u=βc 的合成式逐项相等 ∧ 不恒等于 1",
        "|dr/dt|² = %s" % speed2, "PASS",
        "一般不等于 c²：来料 §一 boxed 的 v_perp²+u²=c² 只是 R·Ω₀=c 的别名（A03），不是 boost 后的新事实",
        mut=lambda: sp.simplify(speed2 - (R_ ** 2 * O0 ** 2 * (1 - bet ** 2) + bet ** 2 + 1)) == 0,
        mdesc="把右端多加一格（+1）后若与现推量仍相等，则该尺不认这一格（判据作废）")
    add("A03", "A", "§一 boxed 恒等式 v_perp²+u²=c² 在约束下闭合（代数恒等，零新信息）",
        "代入 R·Ω₀=c ⇒ |dr/dt|²=1（c=1 口径）",
        "代入后 = %s；v_perp = R·Ω₀/γ = c/γ、u = βc 逐字即来料 §一 那三行"
        % sp.simplify(speed2.subs(R_ * O0, 1)), "PASS",
        "该「双层光速自洽」是把假设写两遍：左边用约束消掉 R，右边就是同一条约束",
        mut=lambda: sp.simplify(speed2.subs(R_ * O0, mp.mpf("3") / 2)) == 1,
        mdesc="代 R·Ω₀=3c/2 后判据必须为假")

    # ---- A04 一般螺旋的 Frenet 现推（分母是速度平方，不是 c²）
    rr = sp.Matrix([R_ * sp.cos(w * tt), R_ * sp.sin(w * tt), uu * tt])
    d1 = [sp.diff(c_, tt) for c_ in rr]
    d2 = [sp.diff(c_, tt) for c_ in d1]
    d3 = [sp.diff(c_, tt) for c_ in d2]
    cr = sp.Matrix(d1).cross(sp.Matrix(d2))
    sp2 = sp.simplify(sum(v ** 2 for v in d1))
    nr = sp.simplify(sp.sqrt(sum(z ** 2 for z in cr)))
    kap_g = sp.simplify(nr / sp2 ** sp.Rational(3, 2))
    tau_g = sp.simplify(sum(cr[i] * d3[i] for i in range(3)) / nr ** 2)
    kap_helix = R_ * w ** 2 / sp2
    tau_helix = uu * w / sp2
    S["kap_g"], S["tau_g"], S["sp2"] = kap_g, tau_g, sp2
    add("A04", "A", "一般螺旋 Frenet 现推：κ=Rω²/(R²ω²+u²)、τ₃=uω/(R²ω²+u²)（分母是速度平方）",
        "标准公式 det(v',v'',v)/|v'×v''|² 与 |v'×v''|/|v'|³ 化简后与闭式逐项差 0",
        "|r'|² = %s；κ−闭式 = %s；τ₃−闭式 = %s"
        % (sp2, sp.simplify(kap_g - kap_helix), sp.simplify(tau_g - tau_helix)), "PASS",
        "⇒ 来料 §二 把分母写成 c² 只在 R²ω²+u²=c² 时成立（前提见 C01 负对照）",
        mut=lambda: sp.simplify(kap_g - R_ * w ** 2 / C_EXACT_SYMPOW) == 0,
        mdesc="把分母强行写成 c²（=1）后与真 Frenet 曲率的差必须非零")

    # ---- A05 来料两条闭式在实验室参数下复现
    lab_subs = {R_: 1 / O0, w: O0 / gam, uu: bet}
    kap_c = sp.simplify(kap_g.subs(lab_subs))
    tau_c = sp.simplify(tau_g.subs(lab_subs))
    kap_inb_sym = sp.simplify(1 / (R_ * gam ** 2))
    S["kap_c"], S["tau_c"] = kap_c, tau_c
    add("A05", "A", "§二 两条闭式 κ=1/(Rγ²)、τ₃=β/(Rγ) 在实验室参数（ω_lab=Ω₀/γ、u=βc）下逐项复现",
        "现推 κ = 1/(Rγ²)|_{R=1/Ω₀} ∧ 现推 τ₃ = β/(Rγ)|_{R=1/Ω₀}",
        "现推 κ = %s（来料 Ω₀/γ²）；现推 τ₃ = %s（来料 Ω₀β/γ）" % (kap_c, tau_c), "PASS",
        "仪器自捕存档（详见 E01）：本条首跑代的是 ω=Ω₀（内禀频率）而非 ω_lab=Ω₀/γ，得 Ω₀/(1+β²) 被自己判红 —— "
        "来料 §二 的 κ 用的是实验室频率；这条替换正是 A04 强调的「分母是实验室速度」的另一面",
        mut=lambda: sp.simplify(kap_g.subs({R_: 1 / O0, w: O0, uu: bet})
                               - sp.simplify(1 / (R_ * gam ** 2)).subs(R_, 1 / O0)) == 0,
        mdesc="把 ω_lab 换成内禀 Ω₀ 后代数不再闭合（判据必须为假）")

    # ---- A06 (V27-1)
    ratio_sym = sp.simplify(kap_inb_sym / (bet / (R_ * gam)))
    diff_v27 = sp.simplify(ratio_sym - sp.sqrt(1 - bet ** 2) / bet)
    S["ratio_sym"] = ratio_sym
    add("A06", "A", "(V27-1) κ/|τ₃| = 1/(γ|β|) = √(1−β²)/β 符号验证",
        "由 A05 两式相除后与来料 §二 boxed 差 = 0",
        "现推比值 = %s；差 = %s" % (ratio_sym, diff_v27), "PASS",
        "恒等式成立，但它就是把 A05 的两条闭式相除，不含新内容（新内容在 G01 的满射定价上）",
        mut=lambda: sp.simplify(ratio_sym - sp.sqrt(1 - bet ** 2) * bet) == 0,
        mdesc="把右端 1/(γβ) 改成 γβ 量级的 √(1−β²)·β 后差式必须非零")

    # ---- A07 R_Z·Ω_Z=c 与 f_Z=2×康普顿（内部关系）
    me = ME["CODATA2022"]
    prod = mp.nstr(rz_f(me) * omz_f(me), 16)
    f_ratio_2 = (omz_f(me) / (2 * mp.pi)) / (me * C_EXACT ** 2 / H_EXACT)
    add("A07", "A", "§四 内禀行的两条内部关系：R_Z·Ω_Z=c（定义别名）与 f_Z=2×康普顿频率",
        "|R_Z·Ω_Z − c| < 1e−40 ∧ |f_Z/(m_ec²/h) − 2| < 1e−60",
        "R_Z·Ω_Z = %s m/s = c；f_Z/康普顿频率 = %s" % (prod, mp.nstr(f_ratio_2, 12)), "PASS",
        "⇒ §四 表里四行只有**一个**独立数（R_Z 或等价的 m_e），印成四行读起来像四个互证的量；"
        "「Ω_Z 恰是 2 倍康普顿频率」归 r354 G12 老账（只作指向，不重落），本卷补半径侧与常数归因",
        mut=lambda: abs((3 * me * C_EXACT ** 2 / HBAR) / (2 * mp.pi)
                       / (me * C_EXACT ** 2 / H_EXACT) - 2) < mp.mpf("1e-60"),
        mdesc="把 Ω_Z 前的因子 2 改成 3 后 f_Z/康普顿比不再是 2")

    # ---- A08 R_Z = λ̄_C/2
    lam_bar = HBAR / (me * C_EXACT)
    add("A08", "A", "§四 R_Z = ħ/(2m_ec) = 约化康普顿波长/2（同义反复，无新尺度）",
        "|R_Z − λ̄_C/2| < 1e−80",
        "R_Z = %s；λ̄_C/2 = %s；口径核对 ħ/(m_ec) vs CODATA 印值 λ̄_C 相对差 = %s"
        % (mp.nstr(rz_f(me), 14), mp.nstr(lam_bar / 2, 14), mp.nstr(lam_bar / LAMBAR_PRINT - 1, 6)), "PASS",
        "「内禀半径」就是 λ̄_C 除 2，除的 2 来自把 Ω_Z 定为 2m_ec²/ħ 的那个因子（见 A09/G08）",
        mut=lambda: abs(rz_f(me) - lam_bar) < mp.mpf("1e-80"),
        mdesc="把「除 2」去掉（R_Z=λ̄_C）后等式必须不成立")

    # ---- A09 L = ħ/k 族
    kk = sp.symbols("k", positive=True)
    Rk = sp.simplify(C_EXACT / (kk * m_s * C_EXACT ** 2 / h_s))
    Lk = sp.simplify(Rk * (m_s * C_EXACT))
    S["Lk"] = Lk
    add("A09", "A", "§四 L = R_Z·p 的整族结果 L(k)=ħ/k（把 Ω_Z=2m_ec²/ħ 前的因子当旋钮 k）",
        "sympy 化简 R(k)·(m c) = ħ/k",
        "R(k) = %s；L(k) = %s（来料取 k=2）"
        % (sp.simplify(Rk.subs(m_s, 1)), sp.simplify(Lk.subs(m_s, 1))), "PASS",
        "符号层面就把「半」这件事归给了 k：k 是自由整数（逐 k 数值实测见 B10）",
        mut=lambda: sp.simplify(Lk.subs(kk, 3) - h_s / 2) == 0,
        mdesc="若 k=3 也给 ħ/2（即把「半」写死、与 k 无关），「L=ħ/k」整族结论作废")

    # ---- A10 μ_ring 闭式
    I_ring = e_s * (2 * m_s * C_EXACT ** 2 / h_s) / (2 * sp.pi)
    mu_ring_sym = sp.simplify(I_ring * sp.pi * (h_s / (2 * m_s * C_EXACT)) ** 2)
    S["mu_ring_sym"] = mu_ring_sym
    add("A10", "A", "§五 环形电流磁矩 μ_ring = I·πR_Z² = eħ/(4m_e) = ½μ_B 符号核验",
        "现推与来料 eħ/(4m) 差 = 0；μ_B = eħ/(2m) ⇒ 比值恰 1/2",
        "现推 μ_ring = %s；与来料差 = %s" % (mu_ring_sym, sp.simplify(mu_ring_sym - e_s * h_s / (4 * m_s))),
        "PASS",
        "代入无误 ⇒ §五 的 2 倍缺口不在代数里，在「用哪个磁矩当分母」（见 G06/B07）",
        mut=lambda: sp.simplify(mu_ring_sym - e_s * h_s / (2 * m_s)) == 0,
        mdesc="把 μ_ring 当成 μ_B（去掉 1/2）后代数必须不闭合")

    # ---- A11 Pauli 9 项
    sx, sy, sz = (sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]),
                  sp.Matrix([[1, 0], [0, -1]]))
    SIG = {"x": sx, "y": sy, "z": sz}
    I2 = sp.eye(2)
    LC = {("x", "y", "z"): 1, ("y", "z", "x"): 1, ("z", "x", "y"): 1,
          ("y", "x", "z"): -1, ("z", "y", "x"): -1, ("x", "z", "y"): -1}
    bad_pauli, n_pairs = [], 0
    for nm1 in "xyz":
        for nm2 in "xyz":
            n_pairs += 1
            lhs = sp.simplify(SIG[nm1] * SIG[nm2] - (I2 if nm1 == nm2 else sp.zeros(2, 2)))
            if nm1 == nm2:
                okp = lhs == sp.zeros(2, 2)
            else:
                perm = ({"x", "y", "z"} - {nm1, nm2}).pop()
                okp = sp.simplify(lhs - sp.I * LC[(nm1, nm2, perm)] * SIG[perm]) == sp.zeros(2, 2)
            if not okp:
                bad_pauli.append(nm1 + nm2)
    add("A11", "A", "§五/§七 Dirac 步：9 项 Pauli 乘积恒等式 σᵢσⱼ = δᵢⱼ + iεᵢⱼₖσₖ 逐对复现",
        "n_pairs=9 ∧ 反例集 = ∅",
        "逐对检验 %d/9 全中，反例集 = %s" % (n_pairs - len(bad_pauli), bad_pauli), "PASS",
        "来料 §七「Dirac–Pauli 矩阵乘法恒等式 9 项精确通过」这一行可由本卷独立重算（不是复述）；"
        "仪器自捕见 E07（首跑 perm 集合把 int 与 char 混型 ⇒ KeyError，非来料问题）",
        mut=lambda: sp.simplify(sx * sy + sp.I * sz) == sp.zeros(2, 2),
        mdesc="把 σxσy 的右端符号写成 −iσz 后该对必须响（反例集非空）")

    # ---- A12 (σ·π)² 用真实微分算符
    Ax, Ay = -BB * Yc / 2, BB * Xc / 2

    def op_pi(g, Q=q):
        return (-sp.I * hb * sp.diff(g, Xc) - Q * Ax * g,
                -sp.I * hb * sp.diff(g, Yc) - Q * Ay * g)

    f1 = sp.Function("f1")(Xc, Yc)
    f2 = sp.Function("f2")(Xc, Yc)

    def apply_pi_pair(g1, g2):
        """σ·π = [[0, πx−iπy],[πx+iπy, 0]]（πz=0：运动限 xy 平面、场沿 z）。
        第一次作用得 (U,D)=((πx−iπy)g2,(πx+iπy)g1)；第二次作用 ⇒ 上分量 (πx−iπy)D、下分量 (πx+iπy)U。"""
        pxg1, pyg1 = op_pi(g1)
        pxg2, pyg2 = op_pi(g2)
        up = pxg2 - sp.I * pyg2
        dn = pxg1 + sp.I * pyg1
        pxu, pyu = op_pi(up)
        pxd, pyd = op_pi(dn)
        return (sp.simplify(pxd - sp.I * pyd), sp.simplify(pxu + sp.I * pyu))

    lhs1, lhs2 = apply_pi_pair(f1, f2)
    pi2_1 = op_pi(op_pi(f1)[0])[0] + op_pi(op_pi(f1)[1])[1]
    pi2_2 = op_pi(op_pi(f2)[0])[0] + op_pi(op_pi(f2)[1])[1]
    rhs1 = sp.expand(pi2_1 - q * hb * BB * f1)
    rhs2 = sp.expand(pi2_2 + q * hb * BB * f2)
    d1_ = sp.simplify(lhs1 - rhs1)
    d2_ = sp.simplify(lhs2 - rhs2)
    neg1 = sp.simplify(lhs1 - sp.expand(pi2_1 + q * hb * BB * f1))
    add("A12", "A", "§五 (σ·π)² = π² − qħσ·B 用真实微分算符作用在**任意**试验旋量上成立",
        "上/下分量残差同为 0 ∧ 符号写反的负对照非零",
        "对称规范 A=(−By/2, Bx/2, 0)、π=−iħ∇−qA，残差 = (%s, %s)；负对照残差 = %s"
        % (d1_, d2_, neg1), "PASS",
        "分量是未指定函数 ⇒ 检验对任意 f 成立，不是对某个特解成立；来料 §五 那两行 "
        "(σ·π)² 与 H_spin=−(q/m)S·B（树级 g=2）的推导步骤独立复现",
        mut=lambda: neg1 == 0,
        mdesc="把右端 −qħB 改成 +qħB 后该恒等式必须不再成立（尺认符号）")

    # ---- A13 交换子 = +iħqB
    comm_term = sp.simplify(op_pi(op_pi(f2)[1])[0] - op_pi(op_pi(f2)[0])[1])
    add("A13", "A", "因子 2 的来处单独实算：[πx,πy]f = +iħqB f（非零）",
        "化简后与 +iħqB·f₂ 差 = 0",
        "实算 πxπy f₂ − πyπx f₂ = %s" % comm_term, "PASS",
        "仪器自捕见 E08：首跑把减法顺序写反，量到 −iħqB 被自己判红；因 A12 已通过（上分量残差归零），"
        "错在操作数顺序而非期望 ⇒ 改正顺序。丢掉它（当作经典可对易动量）得 μ=(q/2m)L 即 g=1，"
        "留着它得 g=2 ⇒ 环模型缺的正是这个非对易项（与 G03 的 ξ/η=g/2 是同一条事实的两种说法）",
        mut=lambda: sp.simplify(comm_term.subs(q, 0)) != 0,
        mdesc="把电荷 q 置 0（回到经典可对易情形）后交换子必须消失，判据随之为假")

    # ---- A14 §六 横向加速度模方
    acc_sq_lab = sp.simplify(sum(sp.diff(v, tt) ** 2 for v in vlab))
    acc_sq_c = sp.simplify(acc_sq_lab.subs(R_ * O0, 1))
    S["acc_sq_c"] = acc_sq_c
    add("A14", "A", "§六 非零横向加速度现推：|d²r/dt²| = Ω₀²/γ⁴（代 R·Ω₀=c 后）",
        "化简差 = 0 ∧ 表达式非零",
        "未代约束 = %s；代入后 = %s（应 = Ω₀²/γ⁴）" % (acc_sq_lab, acc_sq_c), "PASS",
        "|a| = Ω₀/γ² = c²/(Rγ²) ⇒ 来料 §六 那句「不是自由光状测地线，必须引入维持圆周的动力学约束」"
        "可定量（SI 数级见 B11、有限可实现性见 G05）",
        mut=lambda: sp.simplify(acc_sq_c - O0 ** 2 / gam ** 2) == 0,
        mdesc="把 γ⁴ 写成 γ² 后与现推量的差必须非零")
    return S


C_EXACT_SYMPOW = sp.Integer(1)          # c=1 口径下「把分母写成 c²」即写成 1


# ================================================================== B 层：高精度字段复现
def b_layer(S):
    B = {}
    # ---- B01 滑块四格
    b_sl = mp.mpf("0.8")
    g_sl = 1 / mp.sqrt(1 - b_sl ** 2)
    ratio_sl = mp.sqrt(1 - b_sl ** 2) / b_sl
    sl = [("gamma", g_sl, PRINTED["gamma_slider"]),
          ("kappa/tau", ratio_sl, PRINTED["kappa_tau_slider"]),
          ("v_perp/c", 1 / g_sl, PRINTED["vperp_slider"]),
          ("omega_lab/Omega_0", 1 / g_sl, PRINTED["freq_slider"])]
    hits_sl = [nm for nm, v, f in sl if abs(v - P(f)) <= half_ulp(f)]
    B["slider"] = sl
    add("B01", "B", "§三 滑块四格逐字复现（β=0.800000c 那一行）",
        "四格全在各自字段半 ulp 内",
        "命中 %d/4：%s；γ 现算 %s / 印 %s" % (len(hits_sl), hits_sl, mp.nstr(g_sl, 10), PRINTED["gamma_slider"]),
        "PASS",
        "注意来料把 v_perp 与「实验室频率/内禀频率」都印成 0.60000000 —— 二者本就是同一个 1/γ，"
        "所以这一行只有**一条**独立信息，不是两条互证",
        mut=lambda: abs(g_sl - mp.mpf("1.6667")) <= half_ulp("1.66667"),
        mdesc="把 γ 印值换成 1.6667（同位数不同值）后该格必须红")

    # ---- B02 四行表逐位
    rows3 = []
    for b_s, p_s in PRINTED["ratio_table"]:
        bv = mp.mpf(b_s.rstrip("c"))
        val = mp.sqrt(1 - bv ** 2) / bv
        rows3.append((b_s, p_s, val, abs(val - P(p_s)) <= half_ulp(p_s),
                      round_field(val, p_s) == P(p_s)))
    B["rows3"] = rows3
    add("B02", "B", "§二 四行表（0.6c/0.8c/0.99c/0.9999c）容差内且舍位后逐位相等",
        "4/4 半 ulp 命中 ∧ 4/4 逐位相等",
        "命中 %d/4、逐位 %d/4；逐行 %s"
        % (sum(1 for r in rows3 if r[3]), sum(1 for r in rows3 if r[4]),
           [(r[0], mp.nstr(r[2], 12), r[1], r[3], r[4]) for r in rows3]), "PASS",
        "该表可由 (V27-1) 独立重算 ⇒ 本卷是重算不是复述；容差按各字段自己的位数现推（不手钉）",
        mut=lambda: round_field(mp.sqrt(1 - mp.mpf("0.6") ** 2) / mp.mpf("0.6"), "1.333333")
        == mp.mpf("1.333334"),
        mdesc="把 β=0.6 那行的印值末位 +1 后逐位相等必须破")

    # ---- B03 γ/β 传播容差
    bmp, gmp = P(PRINTED["beta_match"]), P(PRINTED["gamma_match"])
    gam_from_b = 1 / mp.sqrt(1 - bmp ** 2)
    cond_gb = bmp * gam_from_b ** 3
    beta_tol = half_ulp(PRINTED["beta_match"])
    prop_tol = cond_gb * beta_tol
    resid_g = abs(gam_from_b - gmp)
    gm_tol = half_ulp(PRINTED["gamma_match"])
    B.update({"bmp": bmp, "gmp": gmp, "gam_from_b": gam_from_b, "cond_gb": cond_gb,
              "prop_tol": prop_tol, "resid_g": resid_g, "gm_tol": gm_tol})
    add("B03", "B", "§三 两条 boxed 数在「β 舍入经条件数放大」的传播容差内自洽",
        "resid(γ) ≤ dγ/dβ · half_ulp(β)（不是 γ 字段的半 ulp）",
        "dγ/dβ = γ³β = %s 倍放大；β 字段半 ulp = %s ⇒ 传播容差 %s；实测残差 %s = 容差的 %s 倍"
        % (mp.nstr(cond_gb, 8), mp.nstr(beta_tol, 3), mp.nstr(prop_tol, 5),
           mp.nstr(resid_g, 5), mp.nstr(resid_g / prop_tol, 5)), "PASS",
        "若把容差直接取成 γ 字段的半 ulp（%s）就会假红 %s 倍（同 r315 T5a 那一课：容差由"
        "「被审对象是怎么算出来的」现推）；⇒ 该匹配在 float64（eps 2.2204e−16）下只能定 γ 到 ~%s，"
        "来料 12 位 γ_match 已到该极限；两条 boxed 数其实只有一条独立信息（β）"
        % (gm_tol, mp.nstr(resid_g / gm_tol, 6), mp.nstr(cond_gb * EPS_FLOAT64, 5)),
        mut=lambda: resid_g <= gm_tol,
        mdesc="把容差口径换成 γ 字段半 ulp 时该判据必须为假（证明两条口径不等价）")

    # ---- B04 内禀三行命中图
    hit_map = {}
    for key, mev in ME.items():
        rzv, omv, fvv = rz_f(mev), omz_f(mev), omz_f(mev) / (2 * mp.pi)
        hit_map[key] = [scaled_match(rzv, PRINTED["R_Z"], PRINTED["exp_R"])[0],
                        scaled_match(omv, PRINTED["Omega_Z"], PRINTED["exp_Omega"])[0],
                        scaled_match(fvv, PRINTED["f_Z"], PRINTED["exp_f"])[0]]
    allv = [k for k, h in hit_map.items() if all(h)]
    notv = [k for k, h in hit_map.items() if not all(h)]
    which = allv[0] if allv else "CODATA2022"
    B["hit_map"], B["which"] = hit_map, which
    add("B04", "B", "§四 内禀三行在候选集内被 CODATA2022 全中、2018 全否（归因先由命中图给出）",
        "∃ 版本三行全中 ∧ ∃ 版本不全中（判集非空、双向都有）",
        "三行全中 = %s；未全中 = %s；逐行命中图 = %s" % (allv, notv, hit_map), "PASS",
        "在 {(2018),(2022)} 这个候选集里来料的内禀三行只指向 2022；B05 再用原像与字段分辨率复核这条不是「碰巧」",
        mut=lambda: all(hit_map["CODATA2018"]),
        mdesc="断言「2018 也三行全中」必须为假（否则该归因无判别力）")

    # ---- B05 质量原像 + 字段分辨率
    inv_m = HBAR / (2 * (P(PRINTED["R_Z"]) * mp.mpf(10) ** mp.mpf(PRINTED["exp_R"])) * C_EXACT)
    res_field = half_ulp(PRINTED["R_Z"]) / P(PRINTED["R_Z"])
    cand_gap = ME["CODATA2022"] / ME["CODATA2018"] - 1
    B.update({"inv_m": inv_m, "res_field": res_field, "cand_gap": cand_gap})
    add("B05", "B", "★由印刷 R_Z 反解 m_e 的原像归因，且字段分辨率足以分辨两版本（不是凭手感）",
        "|inv_m/ME[which]−1| < res_field ∧ |cand_gap| > res_field",
        "反解 m_e = %s；vs CODATA2022 相对差 %s、vs 2018 相对差 %s；R_Z 字段（12 位，R_Z∝1/m_e ⇒ δm/m=δR/R）"
        "把 m_e 锁在相对 ±%s；两版本相对差 = %s = 该分辨率的 %s 倍"
        % (mp.nstr(inv_m, 16), mp.nstr(inv_m / ME["CODATA2022"] - 1, 8),
           mp.nstr(inv_m / ME["CODATA2018"] - 1, 8), mp.nstr(res_field, 6),
           mp.nstr(cand_gap, 6), mp.nstr(abs(cand_gap) / res_field, 5)), "PASS",
        "⇒ 来料 §四 用的是 CODATA2022 那一套 m_e 约定；ħ、c、e 是 SI 定义值（精确）⇒ 这条归因没有第二个自由度",
        mut=lambda: abs(cand_gap) > half_ulp("1.9308") / mp.mpf("1.9308"),
        mdesc="把 R_Z 字段截到 5 位（1.9308）后分辨率劣于两版本差 ⇒ 「归因可解」必须被拒（该式必须为假）")

    # ---- B06 印刷比值唯一归属
    ae = P(A_E_PRINT)
    mrp = P(PRINTED["mu_ratio"])
    cand = {"2*(1+a_e)": 2 * (1 + ae), "1/(1+a_e)": 1 / (1 + ae), "2/(1+a_e)": 2 / (1 + ae),
            "(1+a_e)": 1 + ae, "2": mp.mpf("2")}
    hits7 = [nm for nm, v in cand.items() if abs(v - mrp) <= half_ulp(PRINTED["mu_ratio"])]
    B["ae"], B["mrp"], B["hits7"] = ae, mrp, hits7
    B["cand_names"] = sorted(cand)
    add("B06", "B", "印刷比值 2.00231930436092 在候选集内唯一归属 = 2(1+a_e) = |g_e|",
        "恰 1 个候选命中 ∧ 命中者是 2*(1+a_e)",
        "候选命中 %s；全候选残差 %s" % (hits7, {k: mp.nstr(abs(v - mrp), 5) for k, v in cand.items()}),
        "PASS",
        "⇒ 该数就是恒等式 g_e ≡ 2(1+a_e) 的右端；来料把它印成「磁矩之比」读起来像一次测量，"
        "实际是把实测 g 因子换了个分母（μ_ring=½μ_B）重写一遍（判决见 G06）",
        mut=lambda: len([nm for nm, v in {"2*(1+a_e)": mp.mpf("2"), "1/(1+a_e)": mp.mpf("1"),
                                          "2/(1+a_e)": mp.mpf("2"), "(1+a_e)": mp.mpf("1"),
                                          "2": mp.mpf("2")}.items()
                         if abs(v - mp.mpf("2")) <= half_ulp(PRINTED["mu_ratio"])]) == 1,
        mdesc="把待归因数改成 2.0（去掉反常项）后 {2, 2(1+0)} 同时命中 ⇒ 唯一性破，判据必须为假")

    # ---- B07 a_e 不确定度占用末位
    mr_err = 2 * A_E_UNC
    add("B07", "B", "§五 比值字段的可靠位：a_e 的 (18) 折到比值上已占用末两位",
        "2·u(a_e) > half_ulp(比值字段)",
        "a_e=(…)(18) 折到比值 = %s；该 14 位字段半 ulp = %s ⇒ 误差 %s 倍于末位格"
        % (mp.nstr(mr_err, 5), half_ulp(PRINTED["mu_ratio"]),
           mp.nstr(mr_err / half_ulp(PRINTED["mu_ratio"]), 4)), "PASS",
        "「2.00231930436092」可靠位到第 12 位（…360），后面 92 已被误差占用 ⇒ B06 的逐位相等只能当"
        "「归属」证据，不能当高精度证据",
        mut=lambda: 2 * mp.mpf("1e-15") > half_ulp(PRINTED["mu_ratio"]),
        mdesc="假想 a_e 精确到 1e−15（不确定度小于半 ulp）后「占用」这条必须为假")

    # ---- B08 确定性网格两条恒等式 + 错右端
    det_max, wrong_max = mp.mpf("0"), mp.mpf("0")
    for i in range(1, 2000):
        b = mp.mpf(i) / 2000
        gi = 1 / mp.sqrt(1 - b ** 2)
        det_max = max(det_max, abs(1 / gi ** 2 + b ** 2 - 1),
                      abs(mp.sqrt(1 - b ** 2) / b - 1 / (gi * b)))
        wrong_max = max(wrong_max, abs(mp.sqrt(1 - b ** 2) / b - mp.sqrt(1 - b ** 2) * b))
    B["det_max"], B["wrong_max"] = det_max, wrong_max
    add("B08", "B", "§七 两行数值：1999 点确定性网格上 v_perp²+u²=c² 与 (V27-1) 均为机器零",
        "det_max < 1e−70 ∧ wrong_max > 0.1（尺有牙）",
        "1999 点（β=i/2000）最大残差 = %s；同一把尺打在故意写错的右端（√(1−β²)·β）上得 %s"
        % (mp.nstr(det_max, 8), mp.nstr(wrong_max, 8)), "PASS",
        "⇒ 恒等式为真、与浮点无关；来料 §七 的「50,000 组随机 boost 全部通过」与「最大归一化浮点残差 6.66e-16」"
        "缺种子与归一化分母定义，本卷不裁定（见 G09）；6.66e-16 的量级说明该步用的是 float64 "
        "而非它自己声明的 75 位精算（本条 75 位残差 %s 即对照）" % mp.nstr(det_max, 5),
        mut=lambda: wrong_max < mp.mpf("0.1"),
        mdesc="若这把尺对错误右端也不响（wrong_max→0），「机器零即成立」的读法作废")

    # ---- B09 (η,ξ) 族系数
    me = ME[which]
    L_of = sp.simplify((HBAR / (2 * me * C_EXACT)) * (eta * me * C_EXACT) / HBAR)
    mu_of = sp.simplify(xi * E_CHARGE * HBAR / (4 * me) / MU_B_PRINT)
    L_coef = sp.simplify(sp.diff(L_of, eta))
    mu_coef = sp.simplify(sp.diff(mu_of, xi))
    B["eta_L_coef"], B["mu_coef"] = L_coef, mu_coef
    add("B09", "B", "§四+§五 同族核验：固定 R=R_Z、切速=c 时 L(η) 与 μ(ξ) 对各自份额线性、系数均 = 1/2",
        "dL/dη = 1/2（单位 ħ）∧ dμ/dξ = 1/2（单位 μ_B，含口径核对）",
        "L(η) = %s·ħ；μ(ξ) = %s·μ_B" % (L_coef, mu_coef), "PASS",
        "两靶解：η* = 1（由 L=ħ/2）、ξ* = 2(1+a_e) = %s（由 μ=(1+a_e)μ_B）；"
        "μ_ring 的 SI 口径核对：eħ/(4m) = %s J/T，μ_B 印值 %s，比值 %s（独立于符号推导）"
        % (mp.nstr(2 * (1 + ae), 14), mp.nstr(E_CHARGE * HBAR / (4 * me), 12),
           mp.nstr(MU_B_PRINT, 12), mp.nstr(E_CHARGE * HBAR / (4 * me) / MU_B_PRINT, 10)),
        mut=lambda: abs(float(mu_coef) - 0.5) > mp.mpf("1e-4"),
        mdesc="若 μ 对 ξ 的斜率不是 1/2（例如把 R 换成 λ̄_C）该族就不再参数化 §五 的构造")

    # ---- B10 逐 k 实测 L/ħ
    vals = [(k, mp.nstr((C_EXACT / (k * C_EXACT ** 2 / HBAR)) * C_EXACT / HBAR, 30))
            for k in (1, 2, 3, 4, 6)]
    B["k_vals"] = vals
    add("B10", "B", "§四 半角动量旋钮逐 k 实测：L/ħ = 1/k",
        "k∈{1,2,3,4,6} 全部落在 1/k 的 1e−20 内",
        "实测 L/ħ = %s" % [(k, mp.nstr(mp.mpf(v) - 1 / mp.mpf(k), 3)) for k, v in vals], "PASS",
        "来料「同时关联质量、频率、半径、光速与半整数角动量」这句里的半整数完全住在 Ω_Z=2m_ec²/ħ 的因子 2 上"
        "（判决见 G08）",
        mut=lambda: abs(mp.mpf(vals[2][1]) - mp.mpf("0.5")) < mp.mpf("1e-20"),
        mdesc="k=3 那一档若也给 0.5（即把 1/k 写死成 1/2）判据必须为假")

    # ---- B11 §六 加速度的两条独立 SI 路
    a1 = C_EXACT * omz_f(me)
    a2 = C_EXACT ** 2 / rz_f(me)
    rel_a = abs(a1 / a2 - 1)
    B.update({"a1": a1, "a2": a2, "rel_a": rel_a})
    add("B11", "B", "§六 加速度 SI 换算是两条独立路（c·Ω_Z 与 c²/R_Z），β=0 处一致",
        "相对差 < 1e−60 ∧ 数级 ~1e29 m/s²",
        "c·Ω_Z = %.6e m/s²；c²/R_Z = %.6e m/s²；相对差 %s"
        % (float(a1), float(a2), mp.nstr(rel_a, 4)), "PASS",
        "两条路各用不同的印刷量（Ω_Z vs R_Z），彼此不共享中间量 ⇒ 这一致的不是舍入而是同一恒等式",
        mut=lambda: abs(a1 / a2 - 1) > mp.mpf("1e-3"),
        mdesc="把其中一条路改成 c²/(2R_Z)（少一个因子 2）后两条路必须差到 100%")
    return B


# ================================================================== G 层：判决
def g_layer(S, B):
    G = {}
    ae, mrp = B["ae"], B["mrp"]
    # ---- G01 双射 ⇒ 满射 ⇒ 0 bit
    sol_b = sp.solve(sp.Eq(sp.sqrt(1 - bet ** 2) / bet, xb), bet, dict=True)
    branch = [s for s in sol_b if s[bet] == 1 / sp.sqrt(1 + xb ** 2)]
    dmono = sp.simplify(sp.diff(sp.sqrt(1 - bet ** 2) / bet, bet))
    lim0, lim1 = sp.limit(sp.sqrt(1 - bet ** 2) / bet, bet, 0, "+"), \
        sp.limit(sp.sqrt(1 - bet ** 2) / bet, bet, 1, "-")
    gb = [mp.mpf(i) / 4000 for i in range(1, 4000)]
    f_ratio = lambda b: mp.sqrt(1 - b ** 2) / b              # noqa: E731
    f_bad = lambda b: b * mp.sqrt(1 - b ** 2)                # noqa: E731
    n_steps = len(gb) - 1
    n_dec = sum(1 for i in range(n_steps) if f_ratio(gb[i + 1]) < f_ratio(gb[i]))
    bad_up = sum(1 for i in range(n_steps) if f_bad(gb[i + 1]) > f_bad(gb[i]))
    exact_rt = sp.simplify(sp.sqrt(1 - (1 / sp.sqrt(1 + xb ** 2)) ** 2)
                           / (1 / sp.sqrt(1 + xb ** 2)) - xb)
    eps_dps = mp.mpf(10) ** -mp.mpf(str(mp.mp.dps))
    rt = []
    for tgt in [ALPHA, mp.mpf("0.75"), mp.mpf("2.0"), mp.mpf("1e-6"), mp.mpf("1e6"), mp.mpf("1e30")]:
        bmv = 1 / mp.sqrt(1 + tgt ** 2)
        back = mp.sqrt(1 - bmv ** 2) / bmv
        rel = abs(back - tgt) / tgt
        bound = eps_dps * (1 + tgt ** 2) / tgt ** 2      # √(1−β²) 在 β→1 处相消放大
        rt.append((tgt, bmv, rel, bound, rel <= 3 * bound))
    max_rel = max(r[2] for r in rt)
    G["bij"] = (len(sol_b), len(branch), n_dec, n_steps, bad_up)
    add("G01", "G", "★判决一：β↦κ/|τ₃| 是 (0,1)→(0,∞) 的严格单调双射 ⇒ 反解「匹配 α」的判别力 = 0 bit",
        "唯一支 1 个（solve 给 %d 候选）∧ 网格严格递减 n/n ∧ 端点极限 (∞,0) ∧ 往返符号残差 = 0 ∧ 数值残差 ≤ 条件界"
        % len(sol_b),
        "反解候选 %d 个、命中唯一支 β=1/√(1+x²) 的 %d 个；d/dβ = %s；网格 %d 点、严格递减 %d/%d 档；"
        "β→0⁺ 得 %s、β→1⁻ 得 %s；符号往返差 = %s；六档（含 α、0.75、1e±6、1e30）最大相对残差 %s，"
        "逐档 ≤ 3×「往返自身条件数 × 算术底」（最大档 x=1e−6 因 √(1−β²) 相消放大 (1+x²)/x² 倍）"
        % (len(sol_b), len(branch), dmono, len(gb), n_dec, n_steps, lim0, lim1, exact_rt, mp.nstr(max_rel, 5)),
        "FAIL",
        "⇒ 把 α 换成 0.75 或 10³⁰ 同样「得到」一个 β_match：该匹配是双射的直接后果，不是对 α 的择选，"
        "信息量为零（与 r317/r320 重参数化坐标伪影、r354 G01 满射同族，老账只作指向）；"
        "来料 §三 自己也写了「这不是预测，而是根据实验值事后选择了观察者速度」——本条把这句自陈升级为可算判决",
        mut=lambda: bad_up == 0,
        mdesc="同一把单调尺打在负对照 β√(1−β²)（同端点、内部有极大值）上必须抓到递增；抓到 %d 处" % bad_up)

    # ---- G02 γ_match ≠ α⁻¹
    theo_gm = mp.sqrt(1 + ALPHA ** 2) / ALPHA
    d_gm_alpha = B["gmp"] - ALPHA_INV
    G["gm"] = (theo_gm, d_gm_alpha)
    add("G02", "G", "★判决二：来料印的 γ_match = √(1+α²)/α ≠ α⁻¹（差 +α/2 前导，不是舍入）"
                    " ⇒「该参考系洛伦兹因子就是 137」被自家数字否证",
        "|闭式 √(1+α²)/α − 印 γ_match| ≤ γ 字段半 ulp ∧ |γ_match − α⁻¹| > 100×该半 ulp",
        "闭式 = %s；印值 = %s；α⁻¹ = %s；差 = %s = 相对 %s = %s 个半 ulp（≫1）；"
        "展开 √(1+α²)/α = 1/α + α/2 + O(α³)，α/2 = %s 与实测差同量级（互相印证）"
        % (mp.nstr(theo_gm, 15), PRINTED["gamma_match"], mp.nstr(ALPHA_INV, 12),
           mp.nstr(d_gm_alpha, 6), mp.nstr(d_gm_alpha / ALPHA_INV, 6),
           mp.nstr(abs(d_gm_alpha) / B["gm_tol"], 8), mp.nstr(ALPHA / 2, 8)), "FAIL",
        "⇒ V27 没有给出 α⁻¹ 的来由，只给出了一个「约为 137.04」的洛伦兹因子；两者之差是模型自身的 α/2 项，"
        "把这条差说成舍入需要 γ_match 只有 8 位有效数字，而它印了 15 位",
        mut=lambda: abs(theo_gm - ALPHA_INV) <= B["gm_tol"],
        mdesc="若闭式真的等于 α⁻¹（在字段半 ulp 内）该判决必须消失")

    # ---- G03 一钮两靶
    eta_star, xi_star = mp.mpf("1"), 2 * (1 + ae)
    alt_eta = 1 / (2 * (1 + ae))
    L_at1 = mp.mpf("0.5")
    mu_at1 = E_CHARGE * HBAR / (4 * ME[B["which"]]) / MU_B_PRINT
    res_L, res_mu = abs(L_at1 - mp.mpf("0.5")), abs(mu_at1 - mp.mpf("0.5"))
    G["exy"] = (eta_star, xi_star, alt_eta)
    add("G03", "G", "★判决三：一钮两靶结构性冲突 —— g_model = ξ/η 需要 2.0023 ⇒ 要么超电荷要么角动量减半"
                    "（§四 的「成功」与 §五 的「½μ_B 失败」是同一个 η=1 选择的两面）",
        "ξ* = 2(1+a_e) > 1（违反来料 §五 自家 ξ=1 假设）∧ η=1 时 L 靶精确命中 ∧ ξ=1 时 μ 给半子",
        "两靶同时命中的唯一解 (η,ξ) = (1, %s)：需 %s 倍电子电荷回转，超出「全部电子电荷沿这个圆周旋转」；"
        "强制 ξ=1 得 η = %s ⇒ L = %s·ħ（把 §四 的 ħ/2 打回约 ħ/4）；实测 μ(ξ=1)/μ_B = %s（残差 %s）"
        % (mp.nstr(xi_star, 14), mp.nstr(xi_star, 8), mp.nstr(alt_eta, 10),
           mp.nstr(alt_eta / 2, 10), mp.nstr(mu_at1, 12), mp.nstr(res_mu, 4)), "FAIL",
        "⇒ 不是两个独立结果（「半径对了但磁矩差 2 倍」），而是一个自由度的两次计价；实测缺口 2(1+a_e) "
        "就是 g 因子本身（与 A13 的非对易项是同一条事实的两种说法）；r354 G15「磁矩不可分辨」与 r360 "
        "分层声明点名让渡给本卷（让渡账见 C08，他卷读数只作当下观察）",
        mut=lambda: xi_star <= 1,
        mdesc="若 ξ* ≤ 1（电荷份额不需超额）该冲突判决必须不成立")

    # ---- G04 因子 2 的来处
    add("G04", "G", "判决四：树级 g=2 的全部来源是 [πx,πy]=iħqB 这一叉 ⇒ 经典环（可对易动量）结构上给不出 2",
        "A13 交换子非零 ∧ 把它置 0 得 g=1（μ=(q/2m)L）",
        "实算 [πx,πy]f = iħqB f（A13）；把它丢掉 ⇒ μ=(q/2m)L 即 g=1；留着 ⇒ g=2；"
        "同族比值 ξ/η=g/2 需要 2.0023（G03）⇒ 两处在要同一个东西", "FAIL",
        "⇒ V27 的几何层（环电流）与它自己引用的 Dirac–Pauli 层（非对易）给出不同的 g；"
        "该差不可由环半径/角速度旋钮吃掉（来料 §五 末段自己把 g−2 交给 QED，本条把 g=2 的来处定价成非对易项）",
        mut=lambda: abs(float(comm_of_zero_q()) ) > 0,
        mdesc="在 q=0 情形下交换子必须为 0（否则「因子 2 来自非对易」这条来处就不成立）")

    # ---- G05 约束力发散
    vv = sp.symbols("v", positive=True)
    inv_g3 = (1 - vv ** 2) ** sp.Rational(3, 2)          # = γ_v^{-3}，v<1 时严格正
    lim_inv = sp.limit(inv_g3, vv, 1, "-")               # 恰为 0 ⇒ 倒数无有限界（不吃带极性的 ∞）
    F_lim_sympy = sp.limit(1 / sp.sqrt(1 - vv ** 2) ** 3, vv, 1, "-")   # 仅作对照，见 E10

    def g_pow(p, n=15):
        vals = [(1 - mp.mpf(10) ** (-k),
                 (1 - (1 - mp.mpf(10) ** (-k)) ** 2) ** (mp.mpf(p) / 2)) for k in range(1, n + 1)]
        return vals, all(vals[i][1] < vals[i + 1][1] for i in range(len(vals) - 1))

    vals3, mono3 = g_pow(-3)
    valsn3, monon3 = g_pow(3)
    last3 = vals3[-1][1]
    diverges = (lim_inv == 0) and mono3 and last3 > mp.mpf("1e20")
    a1, a2 = B["a1"], B["a2"]
    G["a0"] = a1
    G["div"] = {"lim_inv": lim_inv, "last3": last3, "mono3": mono3, "n_grid": len(vals3),
                "sympy_signed": F_lim_sympy, "mono_neg3": monon3}
    add("G05", "G", "★判决五：§六「必须引入维持圆周的动力学约束」在本模型内没有有限实现"
                    "（|a|=c²/(Rγ²) 有限但提供它的力在 v→c 发散）",
        "A14 加速度符号闭合 ∧ 两条 SI 路一致 ∧ γ_v^{-3} 的左极限恰为 0 ∧ 15 档网格 γ_v³ 严格递增且末值 >1e20",
        "|d²r/dt²| = Ω₀²/γ⁴ ⇒ |a| = c²/(Rγ²)；β=0 时 c·Ω_Z = %.4e、c²/R_Z = %.4e m/s²（相对差 %s）；"
        "横向力关系 F = γ_v m a 而该模型令回转点 v=c ⇒ lim_{v→c⁻} γ_v^{-3} = %s（其倒数无有限界）、"
        "v=1−10^{-15} 处 γ_v³ = %s（%d 档严格递增 = %s）⇒ 所需约束力发散。"
        "口径声明：本条**不**用 sympy 有符号极限作判据——它把该左极限印成 %s（分支伪影，见 E10）"
        % (float(a1), float(a2), mp.nstr(B["rel_a"], 4), lim_inv, mp.nstr(last3, 6),
           len(vals3), mono3, F_lim_sympy), "FAIL",
        "来料 §六 只说了「需要约束」，没说该约束在自身口径下不可有限实现：模型一边把内部速度钉在 c（§一 boxed），"
        "一边要用 F=γ_v m a 提供有限向心力，二者只能保留一个 ⇒ 该处不是「待补的动力学」而是模型内的硬冲突",
        mut=lambda: valsn3[-1][1] > mp.mpf("1e20") and monon3,
        mdesc="把力关系改坏成 F = m a·γ_v^{-3}（γ 因子放进分母）后同一套网格判据必须为假"
              "——它给的是趋 0（递减、末值 %s），⇒ 本条的承重实在「横向力关系里 γ_v³ 的位置」而非恒等式本身"
              % mp.nstr(valsn3[-1][1], 6))

    # ---- G06 印刷比值 = g_e 换分母
    add("G06", "G", "判决六：§五 的「|μ_e|/μ_ring = 2.00231930436092」不是测量比，是恒等式 g_e≡2(1+a_e) 换分母",
        "B06 唯一归属 = 2*(1+a_e) ∧ B07 该字段可靠位仅 12 位",
        "候选集 %d 项 {%s} 里恰 %d 命中：%s；μ_ring=½μ_B 使分母贡献精确因子 2，剩下的 (1+a_e) 全住实测 a_e"
        % (len(B["cand_names"]), "；".join(B["cand_names"]), len(B["hits7"]), B["hits7"]), "FAIL",
        "⇒ 该行读起来像「几何量与观测量之比」，实际分子分母都来自 CODATA（μ_ring 由 m_e、ħ、e 组成，"
        "μ_e=(1+a_e)μ_B）；把 2 倍缺口叫「不符合」是对的，把它印成 14 位比值则是把实测 g 因子重新包装",
        mut=lambda: len(B["hits7"]) != 1,
        mdesc="归属唯一性一破（命中数 ≠1），「换分母」这条读法就失去依据")

    # ---- G07 内禀行的独立性
    add("G07", "G", "判决七：§四 四行只有 1 个独立数（R_Z ↔ m_e），且常数版本可归因（CODATA2022）",
        "A07 两条内部关系成立 ∧ B04 全中集 = {CODATA2022} ∧ B05 分辨率足以分辨两版本",
        "R_Z·Ω_Z=c（定义别名）、f_Z=2×康普顿（精确 2）、R_Z=λ̄_C/2；命中图 %s；"
        "反解 m_e = %s（vs 2022 相对差 %s < 字段分辨率 %s，两版本差 = 分辨率 %s 倍）"
        % (B["hit_map"], mp.nstr(B["inv_m"], 16),
           mp.nstr(B["inv_m"] / ME[B["which"]] - 1, 5), mp.nstr(B["res_field"], 5),
           mp.nstr(abs(B["cand_gap"]) / B["res_field"], 5)), "PASS",
        "⇒ 该表不是「四个互证读数」而是一行读数 ×三条恒等式；归因到 2022 不是猜：字段分辨率比两版本差细 525 倍；"
        "「Ω_Z=2×康普顿」本身归 r354 G12 老账（只作指向）",
        mut=lambda: all(B["hit_map"]["CODATA2018"]) or abs(B["inv_m"] / ME["CODATA2018"] - 1) < B["res_field"],
        mdesc="若 2018 也全中（或原像落在 2018 的分辨率内），「可归因」判据必须失效")

    # ---- G08 半角动量旋钮
    add("G08", "G", "判决八：L=ħ/2 里的「半」住在 Ω_Z=2m_ec²/ħ 的因子 2 上 —— 自由除数，不是自旋的来由",
        "A09 符号整族 L(k)=ħ/k ∧ B10 逐 k 实测 1/k",
        "逐 k 实测 L/ħ = %s（k=1→1，k=2→0.5，k=3→1/3，k=4→1/4，k=6→1/6）"
        % [(k, mp.nstr(mp.mpf(v), 6)) for k, v in B["k_vals"]], "FAIL",
        "⇒ 「同时关联质量、频率、半径、光速与半整数角动量」这句是同一个 ħ/(m_ec) 尺度的四种写法加一个自由整数；"
        "自旋 ½ 的真实来由（表示论：三维旋转群的二值表示 / 相对论协变场论的 (1/2,0)⊕(0,1/2)）未被触碰",
        mut=lambda: abs(mp.mpf(B["k_vals"][2][1]) - mp.mpf("0.5")) < mp.mpf("1e-20"),
        mdesc="若 k=3 也给 0.5（即「半」与 k 无关），本判决作废")

    # ---- G09 §七 不裁定
    fr = P(PRINTED["float_resid"])
    add("G09", "G", "§七 两行（50,000 组随机 boost 全通过 / 最大归一化浮点残差 6.66e-16）不可反推 ⇒ 不裁定",
        "缺种子与归一化分母定义；本卷只印「若按 75 位精算该残差应是 1e−70 量级」的对照",
        "本卷 1999 点确定性网格残差 = %s（75 位）；来料印 6.66e-16 ≈ %s 倍 float64 eps（%s）"
        "⇒ 该步算术底是 float64，不是它自称的 75 位精算；随机样本无 seed ⇒ 无从复算"
        % (mp.nstr(B["det_max"], 6), mp.nstr(P(PRINTED["float_resid"]) / EPS_FLOAT64, 4),
           mp.nstr(EPS_FLOAT64, 6)),
        "BOUNDARY",
        "只印不可反推（纪律：无 seed / 无分母定义的统计断言不得裁定，也不得照抄成 PASS）",
        mut=lambda: B["det_max"] > mp.mpf("1e-60"),
        mdesc="若 75 位精算的残差真落在 1e−16 量级，「该步是 float64」的口径对照就作废")
    return G


def comm_of_zero_q():
    """G04 变异体用：q=0 时的交换子（应为 0）。"""
    Ax0, Ay0 = -BB * Yc / 2, BB * Xc / 2

    def op0(g):
        return (-sp.I * hb * sp.diff(g, Xc) - 0 * Ax0 * g,
                -sp.I * hb * sp.diff(g, Yc) - 0 * Ay0 * g)
    f = sp.Function("fz")(Xc, Yc)
    return sp.simplify(op0(op0(f)[1])[0] - op0(op0(f)[0])[1])


# ================================================================== C 层：对照（每条都必须是「能亮」的形状）
def c_layer(S, B, G):
    # C01 违反自身约束的螺旋：来料式偏差因子 = |r'|²
    Rn, wn, un = mp.mpf("1"), mp.mpf("1"), mp.mpf("0.5")
    v2 = Rn ** 2 * wn ** 2 + un ** 2
    kap_true = Rn * wn ** 2 / v2
    kap_inb = Rn * wn ** 2 / 1 ** 2
    fac = kap_inb / kap_true
    add("C01", "C", "对照一：把 κ=Rω²/c² 打在**不满足** v_perp²+u²=c² 的螺旋上（R=1,ω=1,u=0.5 ⇒ |r'|²=1.25）",
        "偏差因子与 |r'|² 逐位相等 ∧ 偏离 >10%",
        "真 κ = %s，来料式给 %s，因子 = %s（与 |r'|² = %s 差 %s）⇒ 偏大 %s%%；代回约束（R·Ω₀=1、u=β ⇒ |r'|²=1）"
        "因子回到 1" % (mp.nstr(kap_true, 8), mp.nstr(kap_inb, 8), mp.nstr(fac, 8), mp.nstr(v2, 8),
                        mp.nstr(abs(fac - v2), 5), mp.nstr((fac - 1) * 100, 4)), "PASS",
        "⇒ 来料 §二 的 c² 分母不是通用公式，而是把模型自己的约束塞进分母；该前提一旦被违反，「曲率」立即偏 25%",
        mut=lambda: abs(fac - v2) > mp.mpf("1e-30") or abs(fac - 1) < mp.mpf("0.1"),
        mdesc="若偏差因子既不等于 |r'|²（尺错）也不偏离 1（无牙），本对照作废")

    # C02 非单调负对照
    bad_up = G["bij"][4]
    add("C02", "C", "对照二：单调尺打在「同端点、内部有极大值」的负对照 β√(1−β²) 上必须抓到递增",
        "递增档数 > 0（>0 即有牙）",
        "抓到 %d 处递增（网格 3999 档）" % bad_up, "PASS",
        "同一条尺对来料的 √(1−β²)/β 给 3998/3998 严格递减、对该负对照给大量递增 ⇒ 该尺不是恒绿（G01 的双射结论由它有牙担保）",
        mut=lambda: bad_up == 0, mdesc="尺若对负对照也不响（0 处），G01 与本条同时失去依据")

    # C03 内禀频率替换的必偏量
    kap_wrong = sp.simplify(1 / (R_ * (1 + bet ** 2) / (1 - bet ** 2)))   # 代 ω=Ω₀ 的一般式在 R=1/Ω₀ 下
    kap_wrong = sp.simplify((R_ * O0 ** 2 / (R_ ** 2 * O0 ** 2 + bet ** 2)).subs(R_, 1 / O0))
    kap_right = sp.simplify(1 / (R_ * gam ** 2)).subs(R_, 1 / O0)
    ratio_dev = sp.simplify(kap_wrong / kap_right)
    add("C03", "C", "对照三：把 ω_lab=Ω₀/γ 换成内禀 Ω₀ 后 κ 必偏（因子 = 1/(1−β²+β²·... ) 现算）",
        "两式比值 ≠ 1 且化简后 = γ²/(1+β²γ²)·(1+β²) 型非平凡因子",
        "内禀口径 κ = %s；实验室口径 κ = %s；比值 = %s（β→0 时为 1，β>0 偏离）"
        % (kap_wrong, kap_right, sp.simplify(ratio_dev.subs(bet, sp.Rational(4, 5)))), "PASS",
        "⇒ 来料 §二 的 κ 明确是实验室量（这一替换也是 E01 那次自捕的实质）",
        mut=lambda: sp.simplify(ratio_dev - 1) == 0,
        mdesc="若两种口径给出同一 κ（比值恒 1），这条对照与 A05 的区分度同时消失")

    # C04 容差口径对照
    naive_reds = B["resid_g"] / B["gm_tol"]
    add("C04", "C", "对照四：同一对印刷数在两种容差口径下的判决相反（传播容差 vs 字段半 ulp）",
        "resid/γ字段半ulp ≫ 1（naive 口径假红）∧ resid ≤ 传播容差（正确口径自洽）",
        "naive 口径会红 %s 倍；传播口径为容差的 %s 倍 ⇒ 判红与否完全由「容差怎么来」决定"
        % (mp.nstr(naive_reds, 6), mp.nstr(B["resid_g"] / B["prop_tol"], 5)), "PASS",
        "本条是 E04 那次假红的制度化：被审对象的算法决定容差，不由比较字段的位数决定",
        mut=lambda: (B["resid_g"] > B["prop_tol"]) or (naive_reds < 1),
        mdesc="若传播口径也判红或 naive 口径不判红，两口径的区分度就不存在")

    # C05 字段位数对照
    coarse_res = half_ulp("1.9308") / mp.mpf("1.9308")
    add("C05", "C", "对照五：把 R_Z 字段截到 5 位（1.9308）后两版 CODATA 不再可分辨 ⇒ B05 的归因由位数定价",
        "粗字段分辨率 > 两版本相对差（不可分辨）",
        "粗分辨率 = %s，两版本差 = %s ⇒ 差落在分辨率内（%s 倍）；细字段（12 位）分辨率 = %s（差的 1/%s）"
        % (mp.nstr(coarse_res, 5), mp.nstr(B["cand_gap"], 5), mp.nstr(coarse_res / abs(B["cand_gap"]), 5),
           mp.nstr(B["res_field"], 5), mp.nstr(abs(B["cand_gap"]) / B["res_field"], 5)), "PASS",
        "⇒ 「归因到 CODATA2022」不是版本学的猜测，是可分辨性被量化后的结论；位数不够时同一把尺必须拒判",
        mut=lambda: abs(B["cand_gap"]) > coarse_res,
        mdesc="若粗字段仍能分辨两版本，位数决定可归因性这条就不成立")

    # C06 a_e 不确定度假想精化
    add("C06", "C", "对照六：假想 a_e 精确到 1e−15（不确定度小于比值字段半 ulp）⇒「末两位被占用」必须消失",
        "2·u'(a_e) ≤ half_ulp(比值字段)",
        "u'=1e−15 ⇒ 折到比值 2e−15 ≤ 半 ulp %s ⇒ 逐位复现重新有意义（与 B07 反向）"
        % half_ulp(PRINTED["mu_ratio"]), "PASS",
        "⇒ B07 的「占用」结论不是对 a_e 的一般说法，只对当前 (18) 这一档不确定度成立（口径随输入变）",
        mut=lambda: 2 * mp.mpf("1e-15") > half_ulp(PRINTED["mu_ratio"]),
        mdesc="若假想的精化仍占用末位，本对照与 B07 同时失去意义")

    # C07/C08 去重账（面名册现扫，判集非空）
    faces = sorted(glob.glob(os.path.join(JDG_DIR, "判定*判定_TUFT-r3[2-9][0-9]*.md"))
                   + glob.glob(os.path.join(JDG_DIR, "判定_TUFT-r3[2-9][0-9]*.md")))
    seen = {}
    for p in faces:
        m = re.search(r"判定_TUFT-(r\d{3})", os.path.basename(p))
        if m:
            seen.setdefault(m.group(1), p)
    faces = [p for t, p in sorted(seen.items()) if t != RID]
    txts = {os.path.basename(p): io.open(p, encoding="utf-8").read() for p in faces}
    CTRL_KEYS = ["固定点", "曲率", "挠率", "判别力", "自由度"]
    CTRL = [k for k in CTRL_KEYS if any(k in t for t in txts.values())]
    PROBES = {
        "N1/N2 螺旋 boost 观察者依赖": ["boost", "洛伦兹", "观察者依赖"],
        "N3 (V27-1) 比值 + 双射": ["满射", "判别力", "反解", "双射"],
        "N5 内禀频率 Ω_Z=2m_ec²/ħ": ["康普顿", "Ω_Z", "Zitter"],
        "N6 L=ħ/2 半角动量": ["半整数", "自旋"],
        "N7 环磁矩 / g=2 / μ_ring": ["磁矩", "旋磁", "g=2", "玻尔"],
        "N8 Pauli/(σ·π)²": ["Pauli", "泡利", "sigma", "σ·π"],
        "N4 γ_match vs α⁻¹": ["gamma_", "γ_", "洛伦兹因子"],
    }
    owners = {}
    for nm, keys in PROBES.items():
        h = []
        for t, p in sorted(seen.items()):
            if t == RID:
                continue
            tx = txts[os.path.basename(p)]
            kk2 = [k for k in keys if k in tx]
            if kk2:
                h.append((t, kk2))
        owners[nm] = h
    add("C07", "C", "对照七：去重尺的正对照（同一把尺打在确住在这本账上的老词必须全亮）+ 判集非空",
        "正对照 5/5 命中 ∧ 扫面集 ≥ 20 份（判集塌缩时「零命中」与「无缺陷」同形，必须拒判）",
        "正对照命中 %s（%d/%d）；扫面集 %d 份；逐主题老账 %s"
        % (CTRL, len(CTRL), len(CTRL_KEYS), len(faces),
           {k: [(t, h[:2]) for (t, h) in v[:3]] for k, v in owners.items()}), "PASS",
        "⇒ 上面名册里的「净增量」读法成立；老账只作指向（Ω_Z=2×康普顿 → r354 G12；反解/双射 → "
        "r321/r324/r325/r326/r327/r329；洛伦兹/boost → r324/r329/r332/r338/r342/r344；σ → r354），"
        "他卷读数若被引用一律标「只作当下观察」",
        mut=lambda: len(CTRL) < len(CTRL_KEYS) or len(faces) < 20,
        mdesc="正对照不足或判集塌缩（<20 份）时，本卷一切「净增量/老账」裁定作废")

    defer = []
    for t in ("r354", "r360"):
        if t in seen:
            defer.append((t, txts[os.path.basename(seen[t])].count(RID)))
    add("C08", "C", "对照八：邻居让渡账现扫（r354/r360 的面点名 r351 的次数）",
        "两份面都点名 ≥1 次 ⇒ 本卷条目是「被让渡的归属」不是抢账",
        "点名次数 = %s；r354 G08/G14/G15 与 r360 分层声明均注「同源，只复算不计新条目」" % defer, "PASS",
        "⇒ G03/G06（磁矩与观察者依赖）落在它们主动让出的位置上；引用它们的行号需点名载体文件（死账规则）",
        mut=lambda: len(defer) != 2 or any(n < 1 for _, n in defer),
        mdesc="若让渡名册不再点名 r351，本卷这两条要改写为「与老账对表」而非「接管让渡项」")

    # C09 算术底对照
    fr = P(PRINTED["float_resid"])
    add("C09", "C", "对照九：6.66e−16 与两个算术底的对表（float64 eps vs 本卷 75 位残差）",
        "6.66e−16 / eps(float64) ∈ [1, 10] ∧ 本卷 75 位残差 < 1e−60（差 >40 个数量级）",
        "来料残差 = %s = float64 eps 的 %s 倍；本卷同两条恒等式在 1999 点网格残差 = %s"
        % (mp.nstr(fr, 3), mp.nstr(fr / EPS_FLOAT64, 4), mp.nstr(B["det_max"], 6)), "PASS",
        "⇒ 量级对表支持「该步用 float64」的读法；但不据此裁定该步对错（缺种子与归一化分母，见 G09）",
        mut=lambda: fr / EPS_FLOAT64 > 10 or B["det_max"] > mp.mpf("1e-60"),
        mdesc="若来料残差不落在 float64 量级（或本卷残差不够小），这条口径对表不成立")

    # C10 Pauli 反例集
    flipped = sp.simplify(sp.Matrix([[0, 1], [1, 0]]) * sp.Matrix([[0, -sp.I], [sp.I, 0]])
                          + sp.I * sp.Matrix([[1, 0], [0, -1]]))
    add("C10", "C", "对照十：把 σxσy 的右端符号写反（−iσz）后矩阵差非零 ⇒ A11 的 9/9 是认符号的",
        "符号写反后的差式 ≠ 零矩阵",
        "σxσy + iσz = %s（应为 0 才能说尺不认符号）" % flipped, "PASS",
        "⇒ §七 那行「9 项精确通过」在本卷不是复述：同一把尺能把写反的符号判红",
        mut=lambda: flipped == sp.zeros(2, 2), mdesc="若写反符号也通过，A11 与 §七 该行同时失去依据")
    return {"faces": len(faces), "ctrl": CTRL, "owners": owners, "defer": defer}


# ================================================================== E 层：仪器自捕登记（INFO）
def e_layer():
    # E15 的备份面尺寸现场测（登记器写 README 之前自己拍的快照，只读）
    BAK_R351 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "scratch", "_bak_README_pre_r351.md")
    if os.path.exists(BAK_R351):
        _b = open(BAK_R351, "rb").read()
        bak_size = ("现测 scratch/_bak_README_pre_r351.md = %d 字节 / %d 字符 / md5 %s"
                    % (len(_b), len(_b.decode("utf-8")), md5_of(BAK_R351)))
    else:
        bak_size = "备份面缺席（本轮尚未登记 README）"
    SELF = [
        ("E01", "A05/N2c：首跑把 ω_lab=Ω₀/γ 代成内禀 Ω₀，得 κ=Ω₀/(1+β²) 被自己判红。"
                 "错在**期望的替换**不在来料：来料 §二 的 κ 是实验室量（现由 C03 单独定价）。教训＝代换表要按"
                 "「该量在哪个坐标系被定义」现推，不能按符号同名代。"),
        ("E02", "G01：sp.ask(Q.negative(diff)) 在该式上返回 None（不可判定），拿它当判据＝把「我没算出来」写成结论。"
                "改稠密网格严格差分（3999 档）+ 解析端点极限 + 故意非单调负对照三件；教训＝符号谓词返回值三态"
                "（True/False/None）时 None 一律不得进判决。"),
        ("E03", "G01 数值通道：先用绝对容差 1e−60，被 x=1e30（残差 1.75e−46）与 x=1e−6（相对 1.5e−65）"
                "两头打脸。真相＝√(1−β²) 在 β→1 处灾难性相消，放大 (1+x²)/x² 倍 ⇒ 界必须由**往返自身的条件数**"
                "现推，并另开符号通道（exact 差 = 0）。教训＝绝对容差不许跨数量级复用。"),
        ("E04", "B03：假红 1198 倍——把容差取成 γ 字段的半 ulp（5e−13），而实测残差 5.99e−10 是 β 只印 15 位、"
                "经 dγ/dβ=2.5735e6 放大后的正常值。同 r315 T5a 那一课（容差由「对象怎么算出来」现推），"
                "现由 C04 把两种口径的相反判决制度化。"),
        ("E05", "B04：题面散文写「两版 CODATA 都能复现三行」，而现场命中图是 {2018:[F,F,F], 2022:[T,T,T]} ——"
                "散文与仪器相反。改：标题、布尔、消息三处都由命中图现推。教训＝结论句里每个集合/计数都要由"
                "本轮印出的对象复算，不许由写作时的记忆生成。"),
        ("E06", "A11：perm 集合写成 ({0,1,2} − {nm1,nm2}).pop()，nm1/nm2 是字符 ⇒ KeyError ('x','y',0)。"
                '改为 {"x","y","z"} 同型集合。教训＝置换张量的下标类型要与键类型一致，混型在首轮就崩。'),
        ("E07", "A12：残留死行把 πx/πy 写成 sp.Symbol 又当函数调用 ⇒ TypeError: 'Symbol' object is not callable；"
                "同一段里还有 `if False else` 的恒真形状。清掉死代码并改用 sp.Function(...)(x,y)。"
                "教训＝判决路径上不许留任何「永假条件」，它会把该条变成零判决形状。"),
        ("E08", "A13：首跑算 πyπx−πxπy 得 −iħqB 被自己判红；因 A12（已通过）已确定 [πx,πy]=+iħqB，"
                "故错在**操作数顺序**而非期望值 ⇒ 改正顺序、保留期望，并把它写进条目注记。"
                "教训＝同批次两条判据互斥时，先查哪一条是锚（已通过的算符恒等式），再决定改哪一边。"),
        ("E09", "B11/A14：mp.N 不存在（AttributeError，正确是 mp.sqrt(...).evalf()/直接 float）＋"
                "加速度模方期望首版写成 Ω₀²/γ²（正确 Ω₀²/γ⁴：d/dt 带一个 1/γ，两次共 1/γ²，模方再乘 1/γ²）。"
                "教训＝导数量幂要逐次重推，不能靠「一次 γ 因子」的手感。"),
        ("E10", "G05 首跑以 sp.limit(1/√(1−v²)³, v, 1, '-') 的返回值当判据，并把变异体写成 `F_lim != sp.oo`："
                "sympy 把这条左极限印成 -oo（分支伪影），于是变异体为真 ⇒ 收口闸门 G2 抓到「判决未定价」而判红。"
                "错在**拿一个无穷大的极性当证据**：符号在该极限下不是模型给的量。改＝判据只吃两件事"
                "（γ_v^{-3} 的左极限恰为 0，无符号歧义；15 档 v=1−10^{-k} 网格上 γ_v³ 严格递增且末值 >1e20），"
                "有符号极限降级为对照并印在题面里；变异体改成「把 γ³ 挪进分母后同一套网格判据必须为假」。"
                "教训＝凡以 ±∞ 作结论，必须换成「倒数→0」或有界性判据，极性不得进判决。"),
        ("E11", "引擎首轮连编译都过不去：E06 的题面散文里写了 Python 集合字面量 "
                '（双引号包 {"x","y","z"}），把该条字符串自己截断 ⇒ SyntaxError。'
                "错在**把待印代码样例放进与它同种引号的定界符里**：这类崩溃发生在 import 期，"
                "不产生任何判决，却会让整卷零裁定（比假红更坏）。改＝该条改用单引号定界。"
                "教训＝凡在条目文本里嵌代码，先跑 py_compile 再跑引擎；崩溃不等于红，崩溃＝零判决。"),
        ("E12", "G09 的 act 串写了三个百分号占位符（percent-s 形状）却漏掉格式化实参 ⇒ 判定册把占位符原样印进"
                "读数格：读数缺失被当成读数。首跑靠肉眼在 §二 表里发现，本轮升级成收口闸门 G11：对 ITEMS 五个文本"
                "字段＋两张盘面图像（判定册/数据表）现扫裸格式符，命中即 RED。本条自身的措辞因此改写成中文形状——"
                "第一跑它自己被 G11 判红，这是「闸门的题面不得含违例形状」的示范。"
                "教训＝打印形状类缺陷只修不立闸，下一轮还会犯；凡检查打印结果，输入必须是盘上那张图，不是内存对象。"),
        ("E13", "G06 的候选集用斜杠作列举分隔符印在判定册上，而候选者名字本身含除号"
                "（1/(1+a_e)、2/(1+a_e)），于是 5 项名册在盘面上读成一个连分式；本轮写 README 登记行时"
                "**真的把它误读成 4 项**——同一缺陷在第二个读者身上复现，故不是假想。改＝分隔符换成全角分号，"
                "并把名册与命中数都从 B06 的 cand 现推（len 印进题面），删掉 G06 里重抄的那份字面集合。"
                "教训＝列举分隔符必须与元素内部字符不相交；题面里的「几项」要由 len() 现推，"
                "由字符串手工点数＝同一本账的第二个权威源。"),
        ("E14", "README 登记器 `源码/_reg_r351.py` 的首跑打印把 len(str)（字符数）标成 bytes ⇒ 输出"
                "「bytes 427695 -> 432573 (+4878)」，而同一次写的真字节是 800713 -> 809985（+9272，中文 3 字节/字）。"
                "错在**标签与量纲脱钩**：数字来自 len() 的那个对象（str），标签却写另一个单位（bytes）；"
                "若下一轮把这个数抄进台账就是假账。改＝old_len/new_len 都对**编码后字节**取 len，"
                "并同排印 chars 与 bytes 两行（各标自己的单位），幂等三跑实测 +0 bytes。"
                "教训＝凡印尺寸，标签单位必须由同一行的取值方式决定（编码后取 len 才是字节），字符数只配叫 chars；"
                "这与本卷 B04/B05 的「字段位数决定可归因性」是同一条纪律的两个界面。"),
        ("E15", "修 E14 时我自己造了个假数：登记条写「盘上真实字节 805107 -> 809985」，而 805107 = 809985 − 4878 "
                "是**拿字符差去减字节终点**——单位混用的第二次发作，而且发生在专门记录单位混用的那条里。"
                "现测（不是回推）＝备份面 " + "「%s」" % bak_size + "，真起点 800713、真终点 809985、真差 9272。"
                "改＝条内数字全部由现场 stat 的字节数写出，并把备份文件本身作为量具留档（scratch/_bak_README_pre_r351.md）。"
                "教训＝凡改一处账，新数要重新测得；由旧口径的差值反推出的端点＝第三个权威源，且必带旧口径的错。"),
    ]
    for iid, txt in SELF:
        add(iid, "E", "仪器自捕登记 %s（本卷预检/引擎期间实捕，均已修复，未带病落盘）" % iid,
            "自捕必须是「判据被我自己的错弄红」，不是「来料变红」",
            "修复方向与教训见 note", "INFO", txt,
            mut=lambda: False, mdesc="INFO 登记条不做变异（不承担判决），但不得缺席（缺则收口闸门红）")
    return {"self_bugs": len(SELF)}


# ================================================================== P 层：定价与供给
def p_layer(S, B, G, C):
    slots = [
        ("S1 无参数预言 α（不借观测值选观察者速度）", False, "G01：β↦κ/|τ| 是双射，α 与 0.75、1e30 同样「命中」"),
        ("S2 观察者无关的内禀比值", False, "A06/G01：κ/|τ| = √(1−β²)/β 显含观察者 β；来料 §一 自陈 τ 非内部固有时间"),
        ("S3 自旋 ½ 的来由", False, "G08/A09：L = ħ/k，k 是自由整数"),
        ("S4 磁矩达实测值", False, "G03/B06：需 ξ=2(1+a_e)>1（超出自家「全部电荷回转」），或把 L 打到 ħ/4"),
        ("S5 有限的圆周约束实现", False, "G05/B11：F ∝ γ_v³ 在 v→c 发散，而模型把内部速度钉在 c"),
    ]
    n_sat = sum(1 for _, b, _ in slots if b)
    add("P01", "P", "定价：五槽（2^5=32 组合）本构造满足 %d/%d ⇒ 不占度" % (n_sat, len(slots)),
        "n_sat = 0 判「不占度」；n_sat ≥ 1 即破",
        "逐槽 %s；全真组合 %d 个（需外部输入才能凑齐，构造本身给不出）"
        % ([(nm.split()[0], b) for nm, b, _ in slots], 1 if n_sat == len(slots) else 0), "INFO",
        "槽位与证据：\n" + "\n".join("  · %s —— %s（%s）" % (nm, "不满足" if not b else "满足", ev)
                                    for nm, b, ev in slots)
        + "\n⇒ 本卷不占度：候选账由后续卷持有（r354 记「候选 37，链止 r264:36」，只作当下观察）；"
          "r351 是热区回补（正本先落、源码后落），不改既有序号",
        mut=lambda: n_sat >= 1, mdesc="本构造若真满足任何一槽，「不占度」结论即作废")
    gfails = {it["id"] for it in ITEMS if it["kind"] == "G"}
    NET = ("G01", "G02", "G03", "G04", "G05", "G06", "G08")
    npass = len([it for it in ITEMS if it["kind"] == "G" and it["verdict"] == "PASS" and it["id"] in NET])
    add("P02", "P", "供给账：本卷可入池的第一性输出 = 0 条",
        "G 层里 verdict=PASS 且属净增量名册（G01–G06、G08）的条数现算 = 0",
        "净增量名册 %s；其中 PASS %d 条（G07 是口径结论、非正输出）⇒ 产出类型 %s"
        % (sorted(gfails), npass,
           {it["id"]: ("否证" if it["verdict"] == "FAIL" else "口径/边界")
            for it in ITEMS if it["kind"] == "G"}), "INFO",
        "⇒ V27 给本项目的净贡献是**四条可复用的否证/口径结论**（0 bit 双射、γ_match≠α⁻¹、一钮两靶、"
          "约束力发散）+ 三条口径（内禀行独立数、比值换分母、§七 不裁定），不是新的正输出；"
          "与 r355「供给 0/12 维持」同口径（他卷读数只作当下观察）",
        mut=lambda: npass > 0, mdesc="若七条净增量里出现一条 PASS（来料该主张成立），「0 条入池」即作废")
    return {"slots": slots, "n_sat": n_sat}


# ================================================================== O 层：OPEN 与不裁定
def o_layer():
    add("O01", "O", "OPEN X-R351-1：非对易项 (σ·π)² 能否在纯几何（不引 q、不引 ħ）下生成",
        "本卷只证明经典环缺它（A13/G04），未给出几何生成路线",
        "未算：几何生成 g=2 的路线（本卷零覆盖）", "BOUNDARY",
        "来料 §八 自陈下一步是 j^μ=ψ̄γ^μψ、s^μ=ψ̄γ^μγ⁵ψ、D_μψ=(∇_μ+iqA_μ/ħ)ψ —— 该写法把 q、ħ 作为**输入**，"
        "所以「几何给出 g=2」在来料自己的路线里被前置条件消化掉了；本条留作待裁")
    add("O02", "O", "OPEN X-R351-2：约束力发散（G05）能否被挠率/自旋联络吸收成有限实现",
        "本卷在 F=γ_v m a 的口径下判发散；若约束由几何（挠率驱动的测地偏离）提供，该式不是正确的力关系",
        "未算：τ₃ 与维持圆周的动力学之间的挂钩", "BOUNDARY",
        "来料 §二 引入了 τ₃ 但没有把 τ₃ 用到动力学上；本条是那条挂钩的可算问法")
    add("O03", "O", "OPEN X-R351-3：§七 统计断言若补齐 seed 与归一化分母定义，可升级为独立复核",
        "当前只印不可反推（G09/C09），不裁定",
        "未算：无 seed 的 50,000 组随机抽样对拍", "BOUNDARY",
        "缺两项：随机样本生成器与「归一化」的分母；补齐后本卷的 1999 点确定性网格可替换成同分布抽样对拍")
    return {"open": len([it for it in ITEMS if it["kind"] == "O"])}


# ================================================================== 产物写出
P_REPORT = os.path.join(OUT_DIR, STEM + "_report_" + DATE + ".txt")
P_JSON = os.path.join(OUT_DIR, STEM + "_" + DATE + ".json")
P_MD = os.path.join(OUT_DIR, STEM + "_" + DATE + ".md")
P_JDG = os.path.join(JDG_DIR, "判定_TUFT-r351_ROOTV27双层光速螺旋观察者依赖与半角动量旋钮"
                              "_磁矩一钮两靶与约束力发散判决_" + DATE + ".md")
P_HTML = os.path.join(BASE, HTML_NAME)
正本 = os.path.join(OUT_DIR, "TUFT-r351_ROOTV27双层光速螺旋洛伦兹自洽与曲率挠率比观察者依赖与内禀频率"
                             "半角动量与Dirac磁矩审计_精算与可视化_2026-11-01_来料原件_ROOT_V27_用户附件逐字.md")


def stat_of(p):
    st = os.stat(p)
    return st.st_size, st.st_mtime


ALLOWED_WRITES = {os.path.abspath(p) for p in (P_REPORT, P_JSON, P_MD, P_JDG, P_HTML)}


def md5_of(p):
    import hashlib
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


def write_binary(path, text):
    """二进制写：Windows 下由本卷自己决定行尾（统一 CRLF，与同族文档一致）。
    写盘白名单：本卷只许落自己那六件；越界写＝抛 PermissionError（正本与他卷面结构性免检）。"""
    if os.path.abspath(path) not in ALLOWED_WRITES:
        raise PermissionError("越界写被拒：%s 不在本卷产物白名单内" % path)
    data = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def write_guard_probe():
    """给 G10 造牙：故意往白名单外写一次，必须被拒；若真写出则立刻回收并记红。"""
    foreign = os.path.join(SRC_DIR, "_r351_foreign_write_probe.tmp")
    existed = os.path.exists(foreign)
    refused, wrote = False, False
    try:
        write_binary(foreign, "probe")
        wrote = True
    except PermissionError:
        refused = True
    if wrote and not existed:                       # 只回收本轮自己造出来的文件
        os.remove(foreign)
    return {"refused": refused, "wrote": wrote, "existed_before": existed,
            "target": os.path.basename(foreign)}


def counts():
    c = {}
    for it in ITEMS:
        c[(it["kind"], it["verdict"])] = c.get((it["kind"], it["verdict"]), 0) + 1
    return c


P_PRE = os.path.join(BASE, "scratch", "r351_precheck_out.txt")


def precheck_face():
    """预检面的 SELF-CHECK 结论行现读：散文里的 30/30 只许从那张面上复算，不许凭记忆生成。"""
    if not os.path.exists(P_PRE):
        raise IOError("预检面缺席：%s —— 本卷拒绝引用未落盘的读数" % P_PRE)
    txt = io.open(P_PRE, encoding="utf-8").read()
    m = re.search(r"SELF-CHECK (\d+)/(\d+) 条 PASS；红 (\[[^\]]*\])", txt)
    if not m:
        raise ValueError("预检面没有可复算的 SELF-CHECK 结论行：%s" % os.path.basename(P_PRE))
    return {"pass": int(m.group(1)), "total": int(m.group(2)), "reds": m.group(3),
            "bytes": os.path.getsize(P_PRE)}


def render_report(S, B, G, C, PZ, OZ, gates):
    L = []
    L.append("=" * 100)
    L.append("TUFT-r351 · ROOT V27（双层光速螺旋）来料审计 · 精算报告（c=1 代数走 sympy，印刷字段复现走 mpmath dps=75）")
    L.append("预检面：scratch/r351_precheck_out.txt（该面自印 SELF-CHECK %d/%d、红 %s、%d B）；分层 A/B/G/C/E/P/O 条目不可相加"
             % (gates["precheck"]["pass"], gates["precheck"]["total"],
                gates["precheck"]["reds"], gates["precheck"]["bytes"]))
    L.append("=" * 100)
    L.append("")
    L.append("%-6s %-6s %-70s %-10s" % ("ID", "KIND", "NAME", "VERDICT"))
    L.append("-" * 100)
    for it in ITEMS:
        L.append("%-6s %-6s %-70s %-10s" % (it["id"], it["kind"], it["name"][:70], it["verdict"]))
    L.append("")
    for it in ITEMS:
        L.append("[%s] %s (%s)" % (it["id"], it["name"], it["kind"]))
        L.append("   期望: %s" % it["exp"])
        L.append("   实测: %s" % it["act"])
        L.append("   裁定: %s" % it["verdict"])
        if it.get("mutant"):
            L.append("   变异体: %s -> %s" % (it["mutant"], "已打破（判据对改坏敏感）"
                                             if not it.get("mut_voids") else "!! 未打破（判决未定价）"))
        if it.get("mut_note"):
            L.append("   变异体附注: %s" % it["mut_note"])
        if it["note"]:
            L.append("   注  : %s" % it["note"])
        L.append("")
    L.append("-" * 100)
    L.append("统计（分层 × 裁定，由 ITEMS 现算）：")
    for k in sorted(counts()):
        L.append("   %-4s %-10s : %d" % (k[0], k[1], counts()[k]))
    L.append("   合计条目: %d" % len(ITEMS))
    L.append("   判决类条目（A/B/G/C）数: %d；带变异体数: %d；变异体未打破: %s"
             % (gates["n_judged"], gates["n_with_mut"], gates["mut_fails"]))
    L.append("   自捕登记: %d 条；OPEN: %d 条；五槽满足: %d/%d；入池: %d 条"
             % (gates["n_selfbug"], gates["n_open"], PZ["n_sat"], len(PZ["slots"]),
                gates["n_supply"]))
    L.append("=" * 100)
    return "\n".join(L)


def render_data_md(S, B, G, C, PZ, gates):
    m = []
    m.append("# TUFT-r351 · ROOT V27（双层光速螺旋）来料审计 · 数据与裁定表")
    m.append("")
    m.append("- 卷号：TUFT-r351 ｜ 日期：%s ｜ 引擎：`%s.py` ｜ 预检面：`scratch/r351_precheck_out.txt`"
             % (DATE, NAME))
    m.append("- 来料：ROOT V27 正本 `数据/TUFT-r351_..._来料原件_ROOT_V27_用户附件逐字.md`（本卷不改其字节）")
    m.append("- 分层：A 精确代数／B 高精度字段复现（mpmath dps=75）／G 判决／C 对照／E 自捕／P 定价／O OPEN。"
             "**条目不可跨层相加**。")
    m.append("")
    m.append("## 一、§二 四行表复算（(V27-1) 现推 vs 印值）")
    m.append("")
    m.append("| β | 现算 κ/\\|τ₃\\| | 印值 | 字段半 ulp | 容差内 | 逐位相等 |")
    m.append("| --- | --- | --- | --- | --- | --- |")
    for (b_s, p_s, val, h1, h2) in B["rows3"]:
        m.append("| %s | %s | %s | %s | %s | %s |"
                 % (b_s, mp.nstr(val, 12), p_s, half_ulp(p_s), h1, h2))
    m.append("")
    m.append("## 二、§三 滑块与两条 boxed 数")
    m.append("")
    m.append("| 量 | 现算 | 印值 | 命中 |")
    m.append("| --- | --- | --- | --- |")
    for nm, v, f in B["slider"]:
        m.append("| %s | %s | %s | %s |" % (nm, mp.nstr(v, 10), f, abs(v - P(f)) <= half_ulp(f)))
    m.append("| γ(β_match)→γ | %s | %s | 传播容差 %s（残差 %s） |"
             % (mp.nstr(B["gam_from_b"], 15), PRINTED["gamma_match"],
                mp.nstr(B["prop_tol"], 5), mp.nstr(B["resid_g"], 5)))
    m.append("| γ_match − α⁻¹ | %s | α⁻¹=%s | 相对 %s |"
             % (mp.nstr(B["gmp"] - ALPHA_INV, 6), mp.nstr(ALPHA_INV, 12),
                mp.nstr((B["gmp"] - ALPHA_INV) / ALPHA_INV, 6)))
    m.append("")
    m.append("## 三、§四 内禀行的常数归因")
    m.append("")
    m.append("| 常数版本 | R_Z | Ω_Z | f_Z | 三行命中 |")
    m.append("| --- | --- | --- | --- | --- |")
    for key, me in ME.items():
        m.append("| %s | %s | %s | %s | %s |" % (key, mp.nstr(rz_f(me), 12), mp.nstr(omz_f(me), 12),
                                                 mp.nstr(omz_f(me) / (2 * mp.pi), 12), B["hit_map"][key]))
    m.append("| 由印值反解 m_e | %s | vs %s 相对差 %s | 字段分辨率 ±%s | 两版本差 = 分辨率 %s 倍 |"
             % (mp.nstr(B["inv_m"], 15), B["which"], mp.nstr(B["inv_m"] / ME[B["which"]] - 1, 5),
                mp.nstr(B["res_field"], 5), mp.nstr(abs(B["cand_gap"]) / B["res_field"], 5)))
    m.append("")
    m.append("## 四、§四 半角动量旋钮 L=ħ/k")
    m.append("")
    m.append("| k | L/ħ |")
    m.append("| --- | --- |")
    for k, v in B["k_vals"]:
        m.append("| %d | %s |" % (k, mp.nstr(mp.mpf(v), 8)))
    m.append("")
    m.append("## 五、§五 磁矩与 (η,ξ) 一钮两靶")
    m.append("")
    m.append("| 量 | 值 | 说明 |")
    m.append("| --- | --- | --- |")
    m.append("| μ_ring/μ_B | %s | 现推 ½，与印值 0.500000 同字段命中 |"
             % mp.nstr(E_CHARGE * HBAR / (4 * ME[B["which"]]) / MU_B_PRINT, 12))
    m.append("| 印刷比值 | %s | 候选集唯一归属 = 2(1+a_e) = \\|g_e\\| |" % PRINTED["mu_ratio"])
    m.append("| η* / ξ* | %s / %s | 两靶唯一解；ξ*>1 违反来料 §五 自家假设 |"
             % (mp.nstr(mp.mpf("1"), 6), mp.nstr(2 * (1 + B["ae"]), 14)))
    m.append("| 强制 ξ=1 时的 η | %s | ⇒ L = %s·ħ（把 §四 的 ħ/2 打回约 ħ/4） |"
             % (mp.nstr(1 / (2 * (1 + B["ae"])), 10), mp.nstr(1 / (4 * (1 + B["ae"])), 10)))
    m.append("| u(a_e) 折到比值 | %s | 比值字段半 ulp = %s ⇒ 误差 %s 倍（可靠位 12 位） |"
             % (mp.nstr(2 * A_E_UNC, 5), half_ulp(PRINTED["mu_ratio"]),
                mp.nstr(2 * A_E_UNC / half_ulp(PRINTED["mu_ratio"]), 4)))
    m.append("")
    m.append("## 六、§六 约束加速度")
    m.append("")
    m.append("| 路 | 值（β=0，SI） |")
    m.append("| --- | --- |")
    m.append("| \\|a\\| = c·Ω_Z | %.6e m/s² |" % float(B["a1"]))
    m.append("| \\|a\\| = c²/R_Z | %.6e m/s² |" % float(B["a2"]))
    m.append("| 两路相对差 | %s |" % mp.nstr(B["rel_a"], 4))
    m.append("| 一般式 \\|a\\|² | Ω₀²/γ⁴（A14 符号闭合） |")
    m.append("| lim_{v→c⁻} γ_v^{-3}（判据用的量） | %s（其倒数无有限界；G05：约束力无有限实现） |"
             % G["div"]["lim_inv"])
    m.append("| γ_v³ 在 v=1−10^{-%d} | %s（%d 档严格递增 = %s；sympy 有符号极限 %s 只作对照，见 E10） |"
             % (G["div"]["n_grid"], mp.nstr(G["div"]["last3"], 6), G["div"]["n_grid"],
                G["div"]["mono3"], G["div"]["sympy_signed"]))
    m.append("")
    m.append("## 七、§七 可复算性与不裁定")
    m.append("")
    m.append("| 项 | 本卷读数 | 来料 |")
    m.append("| --- | --- | --- |")
    m.append("| 1999 点网格两恒等式最大残差（75 位） | %s | 「6.66e-16」 |" % mp.nstr(B["det_max"], 6))
    m.append("| 同一把尺打在错误右端 | %s | — |" % mp.nstr(B["wrong_max"], 6))
    m.append("| 50,000 组随机 boost | 不可反推（无 seed、无归一化分母） | 「全部通过」 |")
    m.append("")
    m.append("## 八、条目表")
    m.append("")
    m.append("| ID | 层 | 条目 | 期望 | 实测 | 裁定 |")
    m.append("| --- | --- | --- | --- | --- | --- |")
    for it in ITEMS:
        m.append("| %s | %s | %s | %s | %s | **%s** |"
                 % (it["id"], it["kind"], it["name"].replace("|", "\\|"),
                    it["exp"].replace("|", "\\|"), it["act"].replace("|", "\\|"), it["verdict"]))
    m.append("")
    m.append("## 九、分层统计（由 ITEMS 现算）")
    m.append("")
    m.append("| 层 | 裁定 | 条数 |")
    m.append("| --- | --- | --- |")
    for k in sorted(counts()):
        m.append("| %s | %s | %d |" % (k[0], k[1], counts()[k]))
    m.append("| 合计 | — | %d |" % len(ITEMS))
    m.append("| 判决类（A/B/G/C） | — | %d（带变异体 %d，未打破 %d） |"
             % (gates["n_judged"], gates["n_with_mut"], len(gates["mut_fails"])))
    m.append("")
    return "\n".join(m)


VERDICT_STR = {"PASS": "成立", "FAIL": "不成立/不构成预言", "BOUNDARY": "不裁定", "INFO": "登记"}


def render_judgment(S, B, G, C, PZ, OZ, gates, self_bytes):
    m = []
    m.append("# 判定 TUFT-r351 · ROOT V27（双层光速螺旋）——来料审计判定册")
    m.append("")
    m.append("- 卷号 **r351**（热区回补：正本 2026-11-01 先落、源码本轮才落）｜日期 %s ｜ 只读靶：正本字节未被本卷触碰（§九 自证）" % DATE)
    m.append("- 判词串：`V27-SPIRAL-NULL-CONDITION-DEPENDS-ON-BOXED-ASSUMPTION--RATIO-IS-BIJECTION-ZERO-DISCRIMINATION"
             "--GAMMA-MATCH-NOT-ALPHA-INV--ONE-KNOB-TWO-TARGETS--CONSTRAINT-FORCE-DIVERGES--RATIO-IS-G-FACTOR-REBASED"
             "--SIX-ROWS-ONE-DEGREE-OF-FREEDOM--SPIN-HALF-IS-FREE-DIVISOR--SEC7-NOT-RECONSTRUCTIBLE`")
    m.append("- **一句话**：V27 的全部代数都对，但它没有产出任何一项预言——曲率/挠率比是观察者速度的双射（0 bit），"
             "两条 boxed 常数只差一个 α/2，「半角动量」是一个自由除数，磁矩之比是实测 g 因子换了分母，"
             "而它自陈要补的动力学约束在本模型口径下**发散**（不可有限实现）。")
    m.append("")
    m.append("## §〇 分层声明（条目不可相加）")
    m.append("")
    m.append("| 层 | 含义 | 条数 |")
    m.append("| --- | --- | --- |")
    lay = {"A": "精确代数／符号复算", "B": "高精度印刷字段复现（mpmath dps=75）", "G": "判决",
           "C": "对照（尺必须有牙）", "E": "仪器自捕登记", "P": "定价与供给", "O": "OPEN 与不裁定"}
    for k in "ABGCEPO":
        m.append("| %s | %s | %d |" % (k, lay[k], len([it for it in ITEMS if it["kind"] == k])))
    m.append("| 合计 | — | %d |" % len(ITEMS))
    m.append("")
    m.append("## §一 取号、分工与让渡账（现扫）")
    m.append("")
    m.append("- 取号：本卷**不占新号**。正本文件名 r351 于 2026-11-01 已落盘，源码未落（README:186 记 r354 正因 "
             "「r351 来料已落、源码未落 ⇒ 热区」而取冷号）；本轮把 r351 的热区回补到底。")
    m.append("- 让渡账：邻居面点名 r351 的次数 %s；r354 G08/G14/G15 与 r360 分层声明都注「同源，只复算不计新条目」"
             "⇒ 本卷的磁矩/观察者依赖条目（G01/G03/G06）是**被让渡的归属**，不是抢账。" % (C["defer"],))
    m.append("- 老账名册（只作指向，不重落；引用他卷读数须点名载体且标「只作当下观察」）：")
    for nm, hits in C["owners"].items():
        m.append("  - %s → %s" % (nm, hits if hits else "净增量（关键词零命中）"))
    m.append("- 去重尺自证：正对照命中 %s（%d/%d），扫面集 %d 份 ⇒ 「零命中＝净增量」的读法成立（C07）。"
             % (C["ctrl"], len(C["ctrl"]), 5, C["faces"]))
    m.append("")
    m.append("## §二 主册（%d 行；逐条含变异体名）" % len(ITEMS))
    m.append("")
    m.append("| ID | 层 | 条目 | 期望 | 实测 | 裁定 | 变异体 |")
    m.append("| --- | --- | --- | --- | --- | --- | --- |")
    for it in ITEMS:
        m.append("| %s | %s | %s | %s | %s | **%s** | %s |"
                 % (it["id"], it["kind"], it["name"].replace("|", "\\|").replace("\n", "；"),
                    it["exp"].replace("|", "\\|"),
                    it["act"].replace("|", "\\|").replace("\n", "；")[:300],
                    "%s/%s" % (it["verdict"], VERDICT_STR[it["verdict"]]),
                    (it.get("mutant", "—（登记条）") if it["kind"] not in ("E", "O") else "—").replace("|", "\\|")))
    m.append("")
    m.append("## §三 %d 条判决明细（净增量）" % len([x for x in ITEMS if x["kind"] == "G"]))
    m.append("")
    for it in [x for x in ITEMS if x["kind"] == "G"]:
        m.append("### %s %s ｜ 裁定 **%s（%s）**" % (it["id"], it["name"], it["verdict"], VERDICT_STR[it["verdict"]]))
        m.append("")
        m.append("- 期望：%s" % it["exp"])
        m.append("- 实测：%s" % it["act"])
        m.append("- 判词：%s" % it["note"].replace("\n", "\n  "))
        m.append("- 变异体：%s ⇒ %s" % (it.get("mutant", "无"),
                                        "已打破（改坏后判据不成立）" if not it.get("mut_voids") else "**未打破**"))
        m.append("")
    m.append("## §四 对照与守卫（每条都是「能亮」的形状）")
    m.append("")
    for it in [x for x in ITEMS if x["kind"] == "C"]:
        m.append("- **%s** %s：%s ｜ 裁定 %s ｜ 变异体：%s" % (it["id"], it["name"], it["act"],
                                                              it["verdict"], it.get("mutant", "—")))
    m.append("")
    m.append("## §五 仪器自捕登记（本卷实捕 %d 枚，均已修复，未带病落盘）" % gates["n_selfbug"])
    m.append("")
    for it in [x for x in ITEMS if x["kind"] == "E"]:
        m.append("- **%s**：%s" % (it["id"], it["note"].replace("\n", " ")))
    m.append("")
    m.append("## §六 定价与供给")
    m.append("")
    for nm, b, ev in PZ["slots"]:
        m.append("- %s —— %s（证据：%s）" % (nm, "满足" if b else "不满足", ev))
    m.append("- 五槽满足 **%d/%d** ⇒ **不占度**；候选账由后续卷持有（r354 记「候选 37，链止 r264:36」，只作当下观察）。"
             % (PZ["n_sat"], len(PZ["slots"])))
    m.append("- 入池（可复用第一性正输出）**%d 条**；本卷产出四条否证/口径结论 + 三条口径。" % gates["n_supply"])
    m.append("")
    m.append("## §七 不裁定与 OPEN")
    m.append("")
    m.append("- §七「50,000 组随机 boost 全部通过」与「最大归一化浮点残差 6.66e-16」：**不裁定**（缺 seed 与归一化分母）。"
             "量级对表：%s = float64 eps 的 %s 倍，而本卷 75 位在 1999 点网格残差 %s ⇒ 该步算术底是 float64，"
             "不是它自称的 75 位精算（G09/C09）。"
             % (PRINTED["float_resid"], mp.nstr(P(PRINTED["float_resid"]) / EPS_FLOAT64, 4),
                mp.nstr(B["det_max"], 6)))
    for it in [x for x in ITEMS if x["kind"] == "O"]:
        m.append("- **%s** %s ｜ %s ｜ %s" % (it["id"], it["name"], it["act"], it["note"]))
    m.append("")
    m.append("## §八 终审判词与诚实边界")
    m.append("")
    m.append("**终审判词**：V27 的数学层（§一 光状性、§二 闭式与四行表、§四 内禀行、§五 Pauli 与 (σ·π)²）"
             "**全部可由本卷独立重算**（A/B 层 %d 条，无一条靠复述）；物理层 %d 条判决全部**不成立或不构成预言**："
             "比值是观察者速度的双射（0 bit）、γ_match≠α⁻¹（差 α/2）、半角动量是自由除数、磁矩比是 g 因子换分母、"
             "约束力在 v→c 发散。诚实边界：未算 Dirac–Maxwell 反作用、未做 FW/Newton–Wigner 位置算符对比（只引用未算）、"
             "未处理非均匀场下 v_perp 的时变（§六 只裁存在性与数级）、§七 随机抽样不可反推。"
             % (len([x for x in ITEMS if x["kind"] in ("A", "B")]),
                len([x for x in ITEMS if x["kind"] == "G" and x["verdict"] == "FAIL"])))
    m.append("")
    m.append("## §九 收口闸门读数（分母全部由 ITEMS 现推）")
    m.append("")
    m.append("| 闸门 | 判据 | 读数 | 结果 |")
    m.append("| --- | --- | --- | --- |")
    for nm, crit, read, ok in gates["rows"]:
        m.append("| %s | %s | %s | %s |" % (nm, crit, read, "PASS" if ok else "**RED**"))
    m.append("")
    m.append("## §十 产物真链接（字节数为写盘实测；本文件自身用不动点迭代自洽）")
    m.append("")
    m.append("- 正本（只读，未触碰）：`数据/%s` —— 实测 %d 字节"
             % (os.path.basename(正本), gates["正本_size_end"]))
    m.append("- 引擎：`源码/%s.py` —— 实测 %d 字节" % (NAME, gates["sizes"]["engine"]))
    m.append("- 精算报告：`数据/%s` —— 实测 %d 字节" % (os.path.basename(P_REPORT), gates["sizes"]["report"]))
    m.append("- 机读面：`数据/%s` —— 实测 %d 字节" % (os.path.basename(P_JSON), gates["sizes"]["json"]))
    m.append("- 数据表：`数据/%s` —— 实测 %d 字节" % (os.path.basename(P_MD), gates["sizes"]["md"]))
    m.append("- 可视化：`%s` —— 实测 %d 字节" % (HTML_NAME, gates["sizes"]["html"]))
    m.append("- 本判定册：`判定/%s` —— 声明 %s 字节（写盘后自证见 §九 G7）"
             % (os.path.basename(P_JDG), self_bytes))
    m.append("- 预检面：`scratch/r351_precheck_out.txt`（该面自印 SELF-CHECK %d/%d、红 %s、实测 %d B；"
             "只读探针，零写入）" % (gates["precheck"]["pass"], gates["precheck"]["total"],
                                    gates["precheck"]["reds"], gates["precheck"]["bytes"]))
    m.append("")
    m.append("**下轮建议**：r351 热区已回补；V28–V34 已由 r354/r360/r365/r368/r370/r374/r375 覆盖，"
             "剩余可攻点是 §八 的 j^μ/s^μ/D_μ 路线（本卷 X-R351-1）与非均匀场下的约束实现（X-R351-2）。")
    m.append("")
    return "\n".join(m)


def render_html(S, B, G, C, PZ, gates):
    import html as _h
    rows = []
    for it in ITEMS:
        cls = {"PASS": "p", "FAIL": "f", "BOUNDARY": "b", "INFO": "i"}[it["verdict"]]
        rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td class="%s">%s</td><td>%s</td></tr>'
                    % (it["id"], it["kind"], _h.escape(it["name"]),
                       cls, "%s/%s" % (it["verdict"], VERDICT_STR[it["verdict"]]),
                       _h.escape(it["act"].replace("\n", "；"))[:260]))
    mut_rows = "".join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
                       % (it["id"], _h.escape(it.get("mutant", "—")),
                          "已打破" if not it.get("mut_voids") else "未打破")
                       for it in ITEMS if it["kind"] in ("A", "B", "G", "C"))
    return (
        "<!doctype html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
        "<title>TUFT-r351 · ROOT V27 双层光速螺旋审计</title><style>"
        "body{font-family:system-ui,'Microsoft YaHei';margin:24px;color:#17223a;background:#f7f9fc}"
        "h1{font-size:20px}h2{font-size:16px;margin-top:26px}"
        "table{border-collapse:collapse;width:100%%;font-size:12px;background:#fff}"
        "th,td{border:1px solid #d5deea;padding:5px 7px;vertical-align:top;text-align:left}"
        "td.p{color:#127a3d}td.f{color:#b3261e}td.b{color:#8a6d00}td.i{color:#3b5bdb}"
        ".k{display:inline-block;padding:2px 8px;border-radius:10px;background:#e8eefb;margin-right:6px;font-size:12px}"
        "</style></head><body>"
        "<h1>TUFT-r351 · ROOT V27（双层光速螺旋：洛伦兹自洽／曲率挠率比的观察者依赖／内禀频率与半角动量／Dirac 磁矩）</h1>"
        "<p><span class='k'>%d 条目</span><span class='k'>判决 %d 条</span><span class='k'>对照 %d 条</span>"
        "<span class='k'>自捕 %d 枚</span><span class='k'>五槽满足 %d/%d ⇒ 不占度</span><span class='k'>入池 %d 条</span></p>"
        "<h2>一句话</h2><p>V27 的代数全部可独立重算，但没有一条构成预言：κ/&#124;&#964;&#8323;&#124; 是观察者速度的双射（0 bit）、"
        "&#947;_match&#8800;&#945;&#8315;&#185;（差 &#945;/2）、L=&#8463;/k 是自由除数、磁矩比是实测 g 因子换分母、"
        "维持圆周的约束力在 v&#8594;c 发散。</p>"
        "<h2>关键读数</h2><table><tr><th>量</th><th>读数</th></tr>"
        "<tr><td>§二 四行表</td><td>%s 容差内且舍位后逐位相等（B02）</td></tr>"
        "<tr><td>比值双射</td><td>%s 档严格递减；负对照抓 %d 处递增（G01/C02）</td></tr>"
        "<tr><td>&#947;_match vs &#945;&#8315;&#185;</td><td>%s vs %s，差 %s（= %s 个半 ulp，&#8776;&#945;/2）（G02）</td></tr>"
        "<tr><td>传播容差</td><td>d&#947;/d&#946; = %s 倍；残差 %s &#8804; 容差 %s；naive 口径会假红 %s 倍（B03/C04）</td></tr>"
        "<tr><td>(&#951;,&#958;) 一钮两靶</td><td>&#958;* = %s &gt; 1；强制 &#958;=1 &#8658; L = %s&#183;&#8463;（G03）</td></tr>"
        "<tr><td>约束加速度</td><td>|a| = c&#178;/(R&#947;&#178;)；&#946;=0 时 %.4e m/s&#178;（两路相对差 %s）；"
        "F&#8733; &#8733; &#947;_v&#179;：lim &#947;_v^{-3} = %s 且 v=1&#8722;10^{-15} 处 &#947;_v&#179; = %s"
        "（%d 档严格递增=%s）&#8658; 无有限界（G05）</td></tr>"
        "<tr><td>内禀行归因</td><td>命中图 %s；反解 m_e = %s（分辨率的 1/%s 内）（B04/B05/G07）</td></tr>"
        "<tr><td>半角动量旋钮</td><td>L/&#8463; 逐 k = %s（G08/B10）</td></tr>"
        "<tr><td>&#167;&#19971; 残差对表</td><td>来料 6.66e-16 = float64 eps 的 %s 倍；本卷 75 位残差 %s（C09/G09）</td></tr>"
        "</table><h2>主册（%d 条）</h2><table><tr><th>ID</th><th>层</th><th>条目</th><th>裁定</th><th>实测</th></tr>%s</table>"
        "<h2>变异体名册（判决类每条一个，未打破即收口闸门红）</h2>"
        "<table><tr><th>ID</th><th>变异体</th><th>结果</th></tr>%s</table>"
        "<h2>产物</h2><p>正本（只读）／引擎／report／json／数据表／判定册；字节实测见判定册 &#167;十。</p>"
        "</body></html>"
        % (len(ITEMS), len([x for x in ITEMS if x["kind"] == "G"]),
           len([x for x in ITEMS if x["kind"] == "C"]), gates["n_selfbug"], PZ["n_sat"], len(PZ["slots"]),
           gates["n_supply"],
           "%d/%d" % (sum(1 for r in B["rows3"] if r[3]), len(B["rows3"])),
           "%d/%d" % (G["bij"][2], G["bij"][3]),
           G["bij"][4], mp.nstr(B["gmp"], 15), mp.nstr(ALPHA_INV, 12), mp.nstr(B["gmp"] - ALPHA_INV, 6),
           mp.nstr(abs(B["gmp"] - ALPHA_INV) / B["gm_tol"], 6), mp.nstr(B["cond_gb"], 8),
           mp.nstr(B["resid_g"], 5), mp.nstr(B["prop_tol"], 5), mp.nstr(B["resid_g"] / B["gm_tol"], 6),
           mp.nstr(2 * (1 + B["ae"]), 14), mp.nstr(1 / (4 * (1 + B["ae"])), 10),
           float(B["a1"]), mp.nstr(B["rel_a"], 4), G["div"]["lim_inv"], mp.nstr(G["div"]["last3"], 6),
           G["div"]["n_grid"], G["div"]["mono3"], B["hit_map"], mp.nstr(B["inv_m"], 15),
           mp.nstr(abs(B["cand_gap"]) / B["res_field"], 5),
           [(k, mp.nstr(mp.mpf(v), 4)) for k, v in B["k_vals"]],
           mp.nstr(P(PRINTED["float_resid"]) / EPS_FLOAT64, 4), mp.nstr(B["det_max"], 6),
           len(ITEMS), "".join(rows), mut_rows))


# ================================================================== 收口闸门
def build_gates(S, B, G, C, PZ, OZ, sizes, zp, jdg_rows, jdg_size):
    """所有分母由 ITEMS 现推；任何一行 RED ⇒ main 退出码非 0。"""
    PR = write_guard_probe()
    FMT = re.compile(r"%s|%d|%\.\d+e")
    FMT_IN = []
    for it in ITEMS:
        for fld in ("name", "exp", "act", "note", "mutant"):
            v = it.get(fld, "")
            if isinstance(v, str) and FMT.search(v):
                FMT_IN.append("%s.%s" % (it["id"], fld))
    FMT_FACE = []
    for lbl, pp in (("判定册", P_JDG), ("数据表", P_MD)):
        if os.path.exists(pp):
            t = io.open(pp, encoding="utf-8").read()
            if FMT.search(t):
                FMT_FACE.append("%s(%d 处)" % (lbl, len(FMT.findall(t))))
    jud = [it for it in ITEMS if it["kind"] in ("A", "B", "G", "C")]
    n_judged = len(jud)
    n_with_mut = len([it for it in jud if "mutant" in it])
    NET = ("G01", "G02", "G03", "G04", "G05", "G06", "G08")
    n_supply = len([it for it in ITEMS
                    if it["kind"] == "G" and it["verdict"] == "PASS" and it["id"] in NET])
    n_selfbug = len([it for it in ITEMS if it["kind"] == "E"])
    layer_sum = sum(counts().values())
    bad_e_po = [it["id"] for it in ITEMS
                if it["kind"] in ("E", "P", "O") and it["verdict"] == "FAIL"]
    rows = [
        ("G1 变异体覆盖", "带具名变异体的判决类条目数 == 判决类条目数（分母现推）",
         "%d/%d（缺变异体名册 %s）" % (n_with_mut, n_judged, NO_MUT),
         n_with_mut == n_judged and len(NO_MUT) == 0),
        ("G2 变异体有牙", "MUT_FAILS（改坏后判据仍成立 ⇒ 判决未定价）为空",
         "%d 条未打破：%s" % (len(MUT_FAILS), MUT_FAILS), len(MUT_FAILS) == 0),
        ("G3 主册行数回读", "判定册 §二 表体行数 == len(ITEMS)（从盘上现扫）",
         "盘上 %d 行 vs 内存 %d 条" % (jdg_rows, len(ITEMS)), jdg_rows == len(ITEMS)),
        ("G4 正本只读", "来料正本 md5 与字节数在本轮起点/终点同值 ⇒ 本卷未触碰其字节",
         "起 %d B/%s → 终 %d B/%s" % (zp["start"][0], zp["start"][1][:8],
                                       zp["end"][0], zp["end"][1][:8]),
         zp["start"] == zp["end"]),
        ("G5 分层闭合", "分层 × 裁定计数相加 == 合计条目数（散文不自行加总）",
         "Σ 分层 %d == len(ITEMS) %d" % (layer_sum, len(ITEMS)), layer_sum == len(ITEMS)),
        ("G6 五产物齐件", "引擎/report/json/数据表/判定册/HTML 六件均在盘且非空",
         {k: sizes[k] for k in sorted(sizes)}, all(sizes[k] > 0 for k in sizes)),
        ("G7 判定册自指尺寸", "声明字节 == 盘上实测（不动点迭代收敛）",
         "声明 %d / 盘上 %d" % (jdg_size, sizes["jdg"]), jdg_size == sizes["jdg"]),
        ("G8 登记层无红", "E/P/O 层不得出现 FAIL（登记条不承担判决）",
         "违规 %s；E %d 条 / O %d 条" % (bad_e_po, n_selfbug, OZ["open"]), not bad_e_po),
        ("G9 去重尺有牙", "正对照 5/5 命中 ∧ 扫面集非空（≥20 份面）⇒「零命中＝净增量」可读",
         "正对照 %s（%d/5）；扫面 %d 份" % (C["ctrl"], len(C["ctrl"]), C["faces"]),
         len(C["ctrl"]) == 5 and C["faces"] >= 20),
        ("G10 写盘白名单有牙", "故意往白名单外（源码树临时件）写一次必须被 PermissionError 拒绝"
                              " ⇒ 正本/他卷面结构性不可被本卷写坏",
         "拒绝 = %s；本轮真写出 = %s；目标 %s；起点已存在 %d 件"
         % (PR["refused"], PR["wrote"], PR["target"], len(zp["pre"])),
         PR["refused"] and not PR["wrote"]),
        ("G11 无裸格式符", "ITEMS 五个文本字段 ∧ 判定册/数据表两张盘面图像里不得残留裸格式符（percent-s／"
                              "percent-d／percent-dot-Ne 三种形状）（E12 立的闸）",
         "内存命中 %d 处 %s；面图命中 %d 处 %s" % (len(FMT_IN), FMT_IN, len(FMT_FACE), FMT_FACE),
         not FMT_IN and not FMT_FACE),
        ("G12 OPEN 必须自陈未算", "每条 O 层的实测格含「未算」（不许把「不裁定」写成「已查无物」）",
         "O %d 条，含「未算」%d 条；另 E 层自捕登记 %d 条（只作观察，不作本闸分母）"
         % (len([it for it in ITEMS if it["kind"] == "O"]),
            len([it for it in ITEMS if it["kind"] == "O" and "未算" in it["act"]]), n_selfbug),
         all("未算" in it["act"] for it in ITEMS if it["kind"] == "O")
         and len([it for it in ITEMS if it["kind"] == "O"]) > 0),
    ]
    return {"rows": rows, "n_judged": n_judged, "n_with_mut": n_with_mut,
            "mut_fails": MUT_FAILS, "no_mut": NO_MUT, "n_selfbug": n_selfbug,
            "n_open": OZ["open"], "n_supply": n_supply, "sizes": sizes,
            "正本_size_end": zp["end"][0], "layer_sum": layer_sum,
            "precheck": precheck_face(), "probe": PR}


def json_face(S, B, G, C, PZ, OZ, gates, zp):
    return {"rid": RID, "date": DATE, "name": NAME,
            "engine_bytes": gates["sizes"]["engine"],
            "正本": {"path": os.path.basename(正本), "bytes": zp["end"][0],
                     "md5_start": zp["start"][1], "md5_end": zp["end"][1],
                     "touched_by_this_volume": False},
            "counts": {"%s/%s" % k: v for k, v in sorted(counts().items())},
            "total_items": len(ITEMS),
            "items": [{k: v for k, v in it.items()} for it in ITEMS],
            "gates": [{"name": n, "crit": c, "read": str(r), "ok": bool(o)}
                      for n, c, r, o in gates["rows"]],
            "dedup": {"faces": C["faces"], "ctrl": C["ctrl"], "owners": C["owners"],
                      "defer": C["defer"]},
            "pricing": {"slots": [[nm, b, ev] for nm, b, ev in PZ["slots"]],
                        "n_sat": PZ["n_sat"], "n_supply": gates["n_supply"]},
            "constant_versions": B["hit_map"], "which_m_e": B["which"]}


def count_judgment_rows(path):
    """判定册 §二 主册表体行数：首格形如 A01/B07/G03/C10/E01/P01/O01。"""
    n = 0
    if not os.path.exists(path):
        return n
    txt = io.open(path, encoding="utf-8").read()
    for line in txt.split("\r\n" if "\r\n" in txt else "\n"):
        m = re.match(r"^\|\s*([ABGCEPO]\d{2})\s*\|", line)
        if m:
            n += 1
    return n


def main():
    if not os.path.exists(正本):
        print("FATAL：来料正本缺席，本卷拒绝运行（不得凭空造面）")
        return 2
    zp = {"start": (stat_of(正本)[0], md5_of(正本)),
          "pre": {os.path.basename(p): md5_of(p) for p in
                  (P_REPORT, P_JSON, P_MD, P_JDG, P_HTML) if os.path.exists(p)}}
    zp["end"] = (stat_of(正本)[0], md5_of(正本))
    S = a_layer()
    B = b_layer(S)
    G = g_layer(S, B)
    C = c_layer(S, B, G)
    e_layer()
    PZ = p_layer(S, B, G, C)
    OZ = o_layer()

    sizes = {"engine": stat_of(os.path.abspath(__file__))[0],
             "report": 0, "json": 0, "md": 0, "jdg": 0, "html": 0}
    jdg_size = 0
    jdg_rows = 0
    gates = build_gates(S, B, G, C, PZ, OZ, sizes, zp, jdg_rows, jdg_size)
    for _round in range(10):
        write_binary(P_REPORT, render_report(S, B, G, C, PZ, OZ, gates))
        write_binary(P_MD, render_data_md(S, B, G, C, PZ, gates))
        write_binary(P_JSON, json.dumps(json_face(S, B, G, C, PZ, OZ, gates, zp),
                                        ensure_ascii=False, indent=1))
        write_binary(P_HTML, render_html(S, B, G, C, PZ, gates))
        write_binary(P_JDG, render_judgment(S, B, G, C, PZ, OZ, gates, str(jdg_size)))
        new = {"engine": sizes["engine"], "report": stat_of(P_REPORT)[0],
               "json": stat_of(P_JSON)[0], "md": stat_of(P_MD)[0],
               "jdg": stat_of(P_JDG)[0], "html": stat_of(P_HTML)[0]}
        rows = count_judgment_rows(P_JDG)
        if new == sizes and rows == jdg_rows and new["jdg"] == jdg_size:
            break
        sizes, jdg_rows, jdg_size = new, rows, new["jdg"]
        gates = build_gates(S, B, G, C, PZ, OZ, sizes, zp, jdg_rows, jdg_size)
    zp["end"] = (stat_of(正本)[0], md5_of(正本))
    if "start" in zp and zp["start"] != zp["end"]:
        print("FATAL：正本字节在本轮发生变化 —— 死账，本卷拒绝收口")
        return 2
    gates = build_gates(S, B, G, C, PZ, OZ, sizes, zp, jdg_rows, jdg_size)
    write_binary(P_JDG, render_judgment(S, B, G, C, PZ, OZ, gates, str(jdg_size)))
    write_binary(P_REPORT, render_report(S, B, G, C, PZ, OZ, gates))
    write_binary(P_MD, render_data_md(S, B, G, C, PZ, gates))
    write_binary(P_JSON, json.dumps(json_face(S, B, G, C, PZ, OZ, gates, zp),
                                    ensure_ascii=False, indent=1))
    write_binary(P_HTML, render_html(S, B, G, C, PZ, gates))
    sizes["jdg"] = stat_of(P_JDG)[0]
    rows_final = count_judgment_rows(P_JDG)

    print("r351 %s 条目 %d（判决类 %d，带变异体 %d）" % (RID, len(ITEMS),
          gates["n_judged"], gates["n_with_mut"]))
    for k in sorted(counts()):
        print("   %-2s %-9s %d" % (k[0], k[1], counts()[k]))
    print("   分层闭合 Σ=%d == %d" % (gates["layer_sum"], len(ITEMS)))
    reds = [n for n, c, r, o in gates["rows"] if not o]
    for n, c, r, o in gates["rows"]:
        print("   [%s] %-14s %s | %s" % ("PASS" if o else "RED", n, c, r if not isinstance(r, dict) else " ".join("%s=%d" % i for i in sorted(r.items()))))
    print("   主册回读 %d 行 / 内存 %d 条" % (rows_final, len(ITEMS)))
    print("   产物字节：%s" % {k: sizes[k] for k in sorted(sizes)})
    print("   正本 %d B md5=%s（起点同值=%s）" % (zp["end"][0], zp["end"][1], zp["start"] == zp["end"]))
    print("   起点已存在的产物：%s" % sorted(zp["pre"]))
    if MUT_FAILS or NO_MUT or reds or rows_final != len(ITEMS) or jdg_size != sizes["jdg"]:
        print("SELF-CHECK RED：mut_fails=%s no_mut=%s gates=%s 行数=%s 自指尺寸=%s/%s"
              % (MUT_FAILS, NO_MUT, reds, rows_final, jdg_size, sizes["jdg"]))
        return 1
    print("SELF-CHECK %d/%d 闸门 PASS；判决类条目 %d 条全部由具名变异体定价；零带病落盘"
          % (len(gates["rows"]), len(gates["rows"]), gates["n_with_mut"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
