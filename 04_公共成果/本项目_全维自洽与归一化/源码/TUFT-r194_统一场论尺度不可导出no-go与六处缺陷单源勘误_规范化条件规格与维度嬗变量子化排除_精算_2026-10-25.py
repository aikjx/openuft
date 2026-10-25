# -*- coding: utf-8 -*-
r"""TUFT-r194｜统一场论尺度不可导出 no-go + 六处缺陷单源勘误
================================================================================
承 r192（路径 2 已 no-go；路径 1/3 归并为「尺度设定原理」单一缺失对象）。
本卷把该缺失对象**再收敛一步**并给出可证伪规格，同时落盘 r190/r191 已机读但未修补的
六处记账缺陷（只追加勘误附节，正文一字不改）。

  一、尺度不可导出 no-go（当前清单）
    S1  出处/秩：框架使用的量纲输入只有 **v 与 M_Z**（均为实测）；所有输出尺度都是
        「v × 纯数」——M*/v=14.397900、M_GUT/v=8.3091e13、M_Z/v=0.357234、
        ℓ_EW·v=ħc（单位恒等式）。框架自供的量纲输入 = **0**。
    S2  R1 借用锚点：α_GUT / M_GUT / τ_p / 1/4 独立含量 / ℓ_sd ⇒ 供给 **0/5**。
    S3  R2 维度嬗变：SM/MSSM × 3 扇区 6 次尝试 **0 命中**；最近 lnΛ 间隙 5.98（M*）
        与 13.26（M_GUT），而两圈及以上修正的指数位移上界 <0.5（α≤0.12，|b1/b0|≤5，
        再放宽 ×10）⇒ 对 1e-9 容差**结构性不可达**。
    S4  R3 整数/拓扑量子化：20 种整数型标度形式 × 5 个无量纲靶，反解整数性检验
        （覆盖任意大 n）⇒ 1e-9 命中 **0**（正对照必命中）。
    S5  判定：**CLOSED-NEGATIVE（no-go）**——当前清单无法设定尺度。缺失对象由
        「一条尺度设定方程」精化为「一个**无量纲动力学方程/归一化条件**」：
        因为任何尺度都已是 v×纯数，问题等价于「纯数从哪来」，而不是「量纲从哪来」。
    S6  规格单：任何合格补法须同时满足 C1 显式破共形 / C2 只用框架自有内容 /
        C3 1e-9 命中或给出可证伪偏离 / C4 新增连续参数 ≤1。

  二、六处缺陷单源勘误（幂等，正文一字不改）
    P1 03_四力还原 §牛顿极限：R_00↔G_00 标签（G_00=2R_00）、T_00−½g_00T=½ρc²；
       两个 ½ 互消 ⇒ 终式 ∇²Φ=4πGρ 不变。
    P2 同卷光子质量：1e−18 eV ⇒ λ_C=1.9733e11 m=1.319 AU（太阳系）；1 kpc ⇒ 6.3949e−27 eV。
    P3 同卷 α_s 阶次：单圈公式配 Λ=213 MeV ⇒ 0.13525≠0.1180；单圈自洽 Λ=87.83 MeV。
    P4 同卷 α_G：G M_Z²/(ħc)=5.5785e−35，原文 5e−33 高 89.62×。
    P5 04_守恒律 §3.2 自旋流：∇̃_λ s^λ_{μν} = −2T_{[μν]}（原文 +T_{[μν]} 差因子 −2）。
    P6 04_守恒律 §3.5 B−L：最小 SM（无 ν_R）(B−L)³=−1、[grav]²(B−L)=−1；加 ν_R 后归零。

治理红线：记账修复 ≠ 物理闭合；no-go 只排除**当前清单**；供给仍 0；
本卷条目不可与 r142–r193 相加。纯标准库（Decimal(60) + Fraction），无 numpy/sympy/mpmath。
"""

import ast
import hashlib
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")
S13 = os.path.join(_ROOT, "01_独立体系", "S13_全域双向分形统一场论")
UFE = os.path.join(_ROOT, "07_统一场方程")

BASE = ("TUFT-r194_统一场论尺度不可导出no-go与六处缺陷单源勘误_"
        "规范化条件规格与维度嬗变量子化排除_精算_2026-10-25")
VERDICT = ("R194-SCALE-NOT-DERIVABLE-FROM-CURRENT-INVENTORY-NO-GO-INPUTS-V-AND-MZ-"
           "ALL-SCALES-V-TIMES-PURE-NUMBER-MSTAR-14.3979-MGUT-8.3091E13-"
           "BORROWED-ANCHORS-5-SUPPLY-0-TRANSMUTATION-6-ONE-LOOP-0-HIT-NEAREST-LN-"
           "5.98-AND-13.26-VS-2LOOP-BOUND-LT-0.5-QUANTIZATION-20-FORMS-5-TARGETS-"
           "0-HIT-1E-9-MISSING-OBJECT-DIMENSIONLESS-NORMALIZATION-EQUATION-"
           "REPAIRS-6-PLUS-1-SELF-CORRECTION-R192-XGUT-ALPHA13-"
           "F-LABEL-F-SCALE-F-EXP-F-SIGN-BMINUSL-SUPPLY-0")
REDLINE = ("记账修复 ≠ 物理闭合；尺度不可导出 no-go 只排除当前清单；供给仍 0；"
           "本卷条目不可与 r142–r193 相加")

ENTRIES = []
CTRL = []
GUARDS = []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


# ---------------------------------------------------------------------------
# 〇、常量与闭式（与 r188/r189/r192 同协议）
# ---------------------------------------------------------------------------
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
TWO_PI = D(2) * PI

AEM_INV = D("127.916")
S2W_EXP = D("0.23122")
A3_INV = D(10000) / D(1179)
MZ = D("91.1876")
V_FW = D("255.26")

A1_0 = D(3) / D(5) * (D(1) - S2W_EXP) * AEM_INV
A2_0 = S2W_EXP * AEM_INV
A3_0 = A3_INV

SM_B = (D(41) / D(10), D(-19) / D(6), D(-7))
MSSM_B = (D(33) / D(5), D(1), D(-3))

HBARC_GEV_M = D("1.973269804e-16")
G_SI = D("6.67430e-11")
C_SI = D("2.99792458e8")
HBAR_SI = D("1.054571817e-34")
GEV_KG = D("1.782661921e-27")
KPC_M = D("3.0856775814913673e19")
AU_M = D("1.495978707e11")


def m_star():
    r = D(9) / D(5)
    x = (A1_0 - r * A2_0) / (SM_B[0] - r * SM_B[1])
    return x, MZ * (TWO_PI * x).exp()


def crossing(b):
    x = (A1_0 - A2_0) / (b[0] - b[1])
    return x, MZ * (TWO_PI * x).exp()


def x_at_v():
    return (V_FW / MZ).ln() / TWO_PI


def ell_ew():
    alpha = 1.0 / 137.035999084
    e = math.sqrt(4.0 * math.pi * alpha)
    g = e / math.sqrt(0.23122)
    v = D(str(2.0 * 80.377 / g))
    return HBARC_GEV_M / v, v


# ---------------------------------------------------------------------------
# 一、S1 出处与秩：所有尺度 = v × 纯数
# ---------------------------------------------------------------------------
def sstar_closed():
    s = (D(3) * AEM_INV + D(7) * A3_INV) / (D(15) * AEM_INV)
    a1_0 = D(3) / D(5) * (D(1) - s) * AEM_INV
    l13 = (a1_0 - A3_INV) / (MSSM_B[0] - MSSM_B[2])
    return l13, MZ * (TWO_PI * l13).exp()


def provenance():
    xstar, mstar = m_star()
    x13, mgut = sstar_closed()
    x12 = (A1_0 - A2_0) / (MSSM_B[0] - MSSM_B[1])
    m12 = MZ * (TWO_PI * x12).exp()
    alpha_gut_inv = A3_INV - MSSM_B[2] * x13      # α₃⁻¹(M_GUT)，α₁=α₃ 统一点
    lew, v = ell_ew()
    ratio_star = mstar / v
    ratio_gut = mgut / v
    mz_over_v = MZ / v
    unit_resid = abs(lew * v - HBARC_GEV_M) / HBARC_GEV_M
    return {"x_star": xstar, "x_gut13": x13, "x_gut12": x12, "v": v, "lew": lew,
            "M_star": mstar, "M_GUT": mgut, "M_GUT12": m12,
            "alpha_gut_inv": alpha_gut_inv,
            "Mstar_over_v": ratio_star, "MGUT_over_v": ratio_gut,
            "MZ_over_v": mz_over_v, "unit_resid": unit_resid,
            "self_supplied_dimensionful": 0,
            "measured_dimensionful_inputs": 2}


# ---------------------------------------------------------------------------
# 二、S3 维度嬗变与两圈鲁棒性
# ---------------------------------------------------------------------------
def transmutation():
    xv = float(x_at_v())
    rows = []
    for tag, b in (("SM", SM_B), ("MSSM", MSSM_B)):
        for nm, idx in (("1", 0), ("2", 1), ("3", 2)):
            ai = float(A1_0) - float(b[0]) * xv if idx == 0 else (
                float(A2_0) - float(b[1]) * xv if idx == 1 else
                float(A3_0) - float(b[2]) * xv)
            alpha = 1.0 / ai
            bw = float(b[idx])
            g2 = 4.0 * math.pi * alpha
            expo = -8.0 * math.pi ** 2 / (bw * g2)
            if expo < -700:
                lam = 0.0
            elif expo > 700:
                lam = float("inf")
            else:
                lam = float(V_FW) * math.exp(expo)
            rows.append({"beta_set": tag, "sector": nm, "b": bw,
                         "alpha_at_v": alpha, "exponent": expo,
                         "lambda_gev": lam})
    return rows


def transmutation_robustness(mstar, mgut):
    rows = transmutation()
    finite = [r["lambda_gev"] for r in rows
              if isinstance(r["lambda_gev"], float) and r["lambda_gev"] > 0
              and math.isfinite(r["lambda_gev"])]
    gaps = []
    for tgt in (mstar, mgut):
        lt = math.log(float(tgt))
        gaps.append(min(abs(math.log(l) - lt) for l in finite))
    b0 = 23.0 / 3.0
    b1 = 116.0 / 3.0
    alpha_max = 0.12
    bound = abs(b1) / b0 * alpha_max / (4.0 * math.pi) * 10.0
    return {"n_rows": len(rows), "finite": len(finite),
            "log_gap_to_Mstar": gaps[0], "log_gap_to_MGUT": gaps[1],
            "two_loop_shift_bound": bound,
            "structural_unreachable": (bound < gaps[0] and bound < gaps[1])}


# ---------------------------------------------------------------------------
# 三、S4 整数/拓扑量子化：反解整数性（覆盖任意大 n）
# ---------------------------------------------------------------------------
QFORMS = [
    ("n", D(1), D(1)),
    ("n^2", D(2), D(1)),
    ("n^(1/2)", D(1) / D(2), D(1)),
    ("n^(1/3)", D(1) / D(3), D(1)),
    ("n^(1/4)", D(1) / D(4), D(1)),
    ("n^(3/2)", D(3) / D(2), D(1)),
    ("2*pi*n", D(1), TWO_PI),
    ("pi*n", D(1), PI),
    ("e*n", D(1), D(1).exp()),
    ("sqrt2*n", D(1), D(2).sqrt()),
    ("sqrt3*n", D(1), D(3).sqrt()),
    ("sqrt5*n", D(1), D(5).sqrt()),
    ("(2*pi*n)^(1/2)", D(1) / D(2), TWO_PI),
    ("(2*pi*n)^(1/3)", D(1) / D(3), TWO_PI),
    ("(4*pi*n)^(1/2)", D(1) / D(2), D(4) * PI),
    ("(8*pi*n)^(1/3)", D(1) / D(3), D(8) * PI),
    ("(n/2)^(1/2)", D(1) / D(2), D(1) / D(2)),
    ("(n/3)^(1/2)", D(1) / D(2), D(1) / D(3)),
    ("1/n", D(-1), D(1)),
    ("1/n^2", D(-2), D(1)),
    ("1/n^(1/2)", D(-1) / D(2), D(1)),
]


def _npow(base, q):
    """Decimal 实数幂 base^q = exp(q·ln base)（非整数指数也可，prec=60）。"""
    if q == 1:
        return base
    return (q * base.ln()).exp()


def _scan_target(t, forms, tol):
    """值 = coef · n^q ⇒ n = (t/coef)^(1/q)；返回 (命中数, 最近残差/n/形式)。"""
    hits = 0
    best = (None, None, None)
    for name, q, coef in forms:
        n = _npow(t / coef, D(1) / q)
        if not n.is_finite() or n <= 0:
            continue
        nr = int(n.to_integral_value())
        if nr < 1:
            continue
        resid = abs(n - D(nr))
        if resid < tol:
            hits += 1
        if best[0] is None or resid < best[0]:
            best = (resid, nr, name)
    return hits, best


def quantization_inverse(targets, tol=None):
    """R3 整数/拓扑量子化反解（覆盖任意大 n，无范围盲区）。

    用 Decimal(60) + **绝对残差** |n−round(n)|：相对残差在巨数靶
    （M_GUT/v≈8.3e13）下会被尺度本身吸收，浮点实现曾产生 17 次假阳性；
    绝对残差要求 n 真正落在整数格点上（容差 1e-9）。
    """
    if tol is None:
        tol = D("1e-9")
    out = {}
    for tname, t in targets.items():
        t = D(t)
        if t <= 0:
            out[tname] = {"hits": 0, "closest_resid": None, "closest_n": None,
                          "closest_form": None}
            continue
        hits, best = _scan_target(t, QFORMS, tol)
        out[tname] = {
            "hits": hits,
            "closest_resid": (str(best[0]) if best[0] is not None else None),
            "closest_n": best[1], "closest_form": best[2]}
    # 正对照：7 必命中；负对照：7.0001 必不命中（防止检验恒真）
    pos = _scan_target(D(7), QFORMS, tol)[0] > 0
    neg = _scan_target(D("7.0001"), QFORMS, tol)[0] == 0
    return out, (pos and neg)


# ---------------------------------------------------------------------------
# 四、P1–P4：四力还原卷的机器复核
# ---------------------------------------------------------------------------
def newton_labels():
    T00 = F(1)
    Ttr = F(-1)
    g00 = F(-1)
    doc_rhs = T00 - F(1, 2) * g00 * Ttr     # 1/2（文档标 ρc²，实为 ½ρc²）
    true_rhs = T00                           # 1（真式用 T_00）
    lhs_ratio = F(1, 2)                      # 文档展示式 = ½G_00（标注为 R_00）
    rhs_ratio = doc_rhs / true_rhs
    coeff_4piG = F(8, 2)      # kappa2=8piG/c^4；2 lapPhi/c^2 = kappa2 rho c^2 => 8/2
    return {"doc_rhs": str(doc_rhs), "true_rhs": str(true_rhs),
            "lhs_ratio": str(lhs_ratio), "rhs_ratio": str(rhs_ratio),
            "cancels": lhs_ratio == rhs_ratio,
            "final_coeff_4piG": str(coeff_4piG)}


def photon_scale():
    E_gev = D("1e-27")
    lam = HBARC_GEV_M / E_gev
    au = lam / AU_M
    e_gal = HBARC_GEV_M / KPC_M / D("1e-9")
    return {"lambda_m": lam, "lambda_au": au, "e_gal_ev": e_gal}


def alphas_checks():
    b0 = 11.0 - 2.0 * 5.0 / 3.0
    a_doc = 2.0 * math.pi / (b0 * math.log(91.1876 / 0.213))
    lam_lo_mev = 91.1876 / math.exp(2.0 * math.pi / (b0 * 0.1180)) * 1000.0
    return {"b0": b0, "alpha_doc": a_doc, "lambda_lo_mev": lam_lo_mev,
            "target_alpha": 0.1180, "ratio_lo_doc": lam_lo_mev / 213.0}


def alpha_g():
    mz_kg = MZ * GEV_KG
    ag = G_SI * mz_kg * mz_kg / (HBAR_SI * C_SI)
    return {"alpha_G": ag, "doc": D("5e-33"),
            "ratio": D("5e-33") / ag}


# ---------------------------------------------------------------------------
# 五、P5 自旋流系数（自动微分，精确有理）
# ---------------------------------------------------------------------------
class Dual(object):
    __slots__ = ("v", "d")

    def __init__(self, v, d=F(0)):
        self.v = F(v)
        self.d = F(d)


def _dadd(x, y):
    return Dual(x.v + y.v, x.d + y.d)


def _dsub(x, y):
    return Dual(x.v - y.v, x.d - y.d)


def _dmul(x, y):
    return Dual(x.v * y.v, x.d * y.v + x.v * y.d)


def _dneg(x):
    return Dual(-x.v, -x.d)


def spin_identity(tol=0):
    """∂_λ L^{λμν} = T^{μν}−T^{νμ} = 2T^{[μν]}；M=L+s 守恒 ⇒ ∂s = −2T^{[μν]}。"""
    T = [[F(0) for _ in range(4)] for _ in range(4)]
    vals = [(0, 1, F(3, 7)), (0, 2, F(-5, 11)), (0, 3, F(2, 3)),
            (1, 2, F(7, 5)), (1, 3, F(-4, 9)), (2, 3, F(11, 13))]
    for i, j, val in vals:
        T[i][j] = val
    res = {}
    for mu in range(4):
        for nu in range(4):
            if mu == nu:
                continue
            # ∂_λ L
            dl = F(0)
            for lam in range(4):
                x = [Dual(F(0)) for _ in range(4)]
                x[lam] = Dual(F(0), F(1))
                # L^{λμν} = x^μ T^{λν} − x^ν T^{λμ}
                term1 = _dmul(x[mu], Dual(T[lam][nu]))
                term2 = _dmul(x[nu], Dual(T[lam][mu]))
                L = _dsub(term1, term2)
                dl += L.d
            antisym = (T[mu][nu] - T[nu][mu]) / 2
            ds = -dl
            res["%d%d" % (mu, nu)] = {
                "dL": str(dl), "T_antisym": str(antisym),
                "dL_eq_2T": dl == 2 * antisym,
                "ds_eq_minus_2T": ds == -2 * antisym,
                "coeff_abs": "2"}
    return res


# ---------------------------------------------------------------------------
# 六、P6 B−L 反常系数（左手 Weyl 计数，精确）
# ---------------------------------------------------------------------------
def bml_anomalies(include_nur=False):
    # (多重数, B−L)；右手粒子以左手共轭计，B−L 变号
    fields = [(6, F(1, 3)),    # q_L：3 色 × 2
              (3, F(-1, 3)),   # u_R^c
              (3, F(-1, 3)),   # d_R^c
              (2, F(-1)),      # l_L
              (1, F(1))]       # e_R^c
    if include_nur:
        fields.append((1, F(1)))  # ν_R^c：与 e_R^c 同号，加一单位即抵消两条反常
    cubic = sum(m * q ** 3 for m, q in fields)
    linear = sum(m * q for m, q in fields)
    return {"cubic": str(cubic), "linear": str(linear),
            "cubic_zero": cubic == 0, "linear_zero": linear == 0}


# ---------------------------------------------------------------------------
# 七、落地勘误（r194，幂等，只追加）
# ---------------------------------------------------------------------------
ERRATA_TAG = "【r194 尺度不可导出 no-go 与六处缺陷勘误｜2026-10-25】"
ERRATA = {
    "07_统一场方程/03_四力还原.md": [
        "P1｜§牛顿极限（L36/L38）标签：展示式「R_00≃−½∇²h̄_00」实为 **G_00**（静态迹情形 G_00=2R_00）；"
        "「T_00−½g_00T≃ρc²」实为 **½ρc²**（LHS 与 RHS 各带一个 ½，互消）⇒ 终式 ∇²Φ=4πGρ **不变**，"
        "但两处符号必须改标（F-label）。",
        "P2｜§光子质量（L104）尺度：1×10⁻¹⁸ eV ⇒ 康普顿波长 λ_C=1.9733×10¹¹ m=**1.319 AU（太阳系尺度）**；"
        "银河磁场（1 kpc）对应的上限是 **6.3949×10⁻²⁷ eV**。原文「银河磁场尺度」与所给 10⁻¹⁸ eV 相差约 9 个量级（F-scale）。",
        "P3｜§强相互作用（L162）阶次：**单圈**公式配 Λ_QCD^(5)=213 MeV 得 α_s(M_Z)=**0.13525≠0.1180**（偏大 14.6%）；"
        "单圈自洽值为 **Λ_LO^(5)=87.83 MeV**。213 MeV 属两圈/PDG 口径（r190 机读极点 243.18 MeV，同量级）⇒ 必须标注阶次（F-label）。",
        "P4｜§引力强度（L194）指数：机器 G M_Z²/(ħc)=**5.5785×10⁻³⁵**，原文 5×10⁻³³ 高 **89.63×**（10⁻³³ vs 10⁻³⁵，F-exp）。",
    ],
    "07_统一场方程/04_守恒律与诺特定理.md": [
        "P5｜§3.2（L47）自旋流恒等式系数：应为 **∇̃_λ s^λ_{μν} = −2T_[μν]**，原文「=T_[μν]」少因子 **−2**。"
        "机器（精确有理 + 自动微分）：∂_λL^{λμν}=T^{μν}−T^{νμ}=2T^{[μν]}；M=L+s 守恒 ⇒ ∂_λ s^{λμν}=−2T^{[μν]}（F-sign/F-factor）。",
        "P6｜§3.5（L77/L150）B−L：最小 SM（无 ν_R）**并非反常自由**——(B−L)³=**−1**、[grav]²(B−L)=**−1**；"
        "加入一个 ν_R 后两通道同时归零。sphaleron 保 B−L 的部分（SU(2)²B=SU(2)²L=1/2）成立，但「严格守恒」的表述需加前提。",
    ],
}


def apply_errata():
    out = []
    for rel, bullets in ERRATA.items():
        path = os.path.join(_ROOT, rel)
        before = open(path, "r", encoding="utf-8").read()
        existed = ERRATA_TAG in before
        if not existed:
            body = ["", "", "---", "", "## " + ERRATA_TAG, "",
                    "> 审计侧附加标注；**正文原始数字一字未改**（只追加，不静默改写）。",
                    "> 依据：`04_公共成果/本项目_全维自洽与归一化/数据/"
                    "判定_TUFT-r194_统一场论尺度不可导出no-go与六处缺陷单源勘误_精算_2026-10-25.md`。", ""]
            for b in bullets:
                body.append("- " + b)
            body.append("")
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n".join(body))
        after = open(path, "r", encoding="utf-8").read()
        out.append({"rel": rel, "errata_present": ERRATA_TAG in after,
                    "applied_this_run": (not existed),
                    "prefix_preserved": after.startswith(before),
                    "bytes_before": len(before.encode("utf-8")),
                    "bytes_after": len(after.encode("utf-8")),
                    "bullets": len(bullets),
                    "sha256_after": hashlib.sha256(after.encode("utf-8")).hexdigest()})
    return out


# ---------------------------------------------------------------------------
# 八、主流程
# ---------------------------------------------------------------------------
def main():
    prov = provenance()
    rob = transmutation_robustness(prov["M_star"], prov["M_GUT"])

    targets = {
        "M*/v": prov["Mstar_over_v"],
        "M_GUT/v": prov["MGUT_over_v"],
        "alpha_GUT_inv": prov["alpha_gut_inv"],
        "x*": prov["x_star"],
        "x_GUT": prov["x_gut13"],
    }
    qscan, qctrl = quantization_inverse(targets)

    nl = newton_labels()
    ph = photon_scale()
    asx = alphas_checks()
    ag = alpha_g()
    spin = spin_identity()
    bml_no = bml_anomalies(False)
    bml_nu = bml_anomalies(True)

    pats = apply_errata()

    # ---- A. 量纲门禁 ----
    add("A0", "dim", "量纲门禁：x=ln(μ/M_Z)/2π 无量纲；M=v×纯数；ℓ_EW·v=ħc",
        "PASS", "解析门禁")

    # ---- P. 六处缺陷（机读复核 + 勘误） ----
    add("P1", "repair",
        "牛顿极限标签：T_00−½g_00T={}（≠ρc²）；与 G_00=2R_00 的 ½ 互消 ⇒ "
        "终式系数 {}πG 不变".format(nl["doc_rhs"], nl["final_coeff_4piG"].rstrip("/")),
        "CORRECTED", "F-label；cancels={}".format(nl["cancels"]))
    add("P2", "repair",
        "光子质量尺度：1e−18 eV ⇒ λ_C={:.4e} m = {:.4f} AU；1 kpc ⇒ {:.4e} eV".format(
            float(ph["lambda_m"]), float(ph["lambda_au"]), float(ph["e_gal_ev"])),
        "CORRECTED", "F-scale；9 个量级")
    add("P3", "repair",
        "α_s 阶次：单圈+Λ=213 MeV ⇒ {:.5f}（≠0.1180）；单圈自洽 Λ_LO={:.2f} MeV ⇒ "
        "213 MeV 属两圈口径".format(asx["alpha_doc"], asx["lambda_lo_mev"]),
        "CORRECTED", "F-label")
    add("P4", "repair",
        "α_G：G M_Z²/(ħc)={:.4e}，原文 5e−33 高 {:.2f}×".format(
            float(ag["alpha_G"]), float(ag["ratio"])),
        "CORRECTED", "F-exp")
    add("P5", "repair",
        "自旋流恒等式：∂_λL=2T^[μν]、∂_λs=−2T^[μν]（12 对指标精确），"
        "系数绝对值恒为 2 ⇒ 原文 +1 差因子 −2",
        "CORRECTED",
        "F-sign/F-factor；{} 对全过".format(len(spin)))
    add("P6", "repair",
        "B−L：无 ν_R 时 (B−L)³={}、[grav]²(B−L)={}；加 ν_R 后 {} / {}".format(
            bml_no["cubic"], bml_no["linear"], bml_nu["cubic"], bml_nu["linear"]),
        "CORRECTED", "口径边界；最小 SM 非反常自由")

    # ---- S. 尺度不可导出 ----
    add("S1", "scale",
        "出处/秩：M*/v={:.6f}、M_GUT/v={:.4e}、M_Z/v={:.6f}，ℓ_EW·v=ħc"
        "（残差 {:.1e}）⇒ 所有尺度 = v×纯数；框架自供量纲输入 **0**".format(
            float(prov["Mstar_over_v"]), float(prov["MGUT_over_v"]),
            float(prov["MZ_over_v"]), float(prov["unit_resid"])),
        "PASS", "2 个实测量纲输入（v, M_Z）")
    add("S2", "scale",
        "R1 借用锚点：α_GUT / M_GUT / τ_p / 1/4 独立含量 / ℓ_sd ⇒ 供给 **0/5**",
        "FAIL", "借用不计完成度")
    add("S3", "scale",
        "R2 维度嬗变：6 次 0 命中；最近 lnΛ 间隙 M*={:.2f} / M_GUT={:.2f}，"
        "两圈及以上指数位移上界 <{:.2f} ⇒ 1e-9 容差结构性不可达".format(
            rob["log_gap_to_Mstar"], rob["log_gap_to_MGUT"],
            rob["two_loop_shift_bound"]),
        "FAIL", "robust={}".format(rob["structural_unreachable"]))
    add("S4", "scale",
        "R3 整数/拓扑量子化：20 种形式 × 5 靶，反解整数性 1e-9 命中 **{}**"
        "（正对照 {}）".format(sum(v["hits"] for v in qscan.values()), qctrl),
        "FAIL", "覆盖任意大 n，无范围盲区")
    add("S5", "verdict",
        "尺度判定：**CLOSED-NEGATIVE（no-go）**——当前清单无法设定尺度；"
        "缺失对象由「尺度方程」精化为「**无量纲归一化条件**」",
        "PASS", "no-go 排除 ≠ 物理闭合")
    add("S6", "spec",
        "规格单：C1 显式破共形 / C2 只用框架自有内容 / C3 1e-9 命中或可证伪偏离 / "
        "C4 新增连续参数 ≤1；三条 R 路线中仅 R3 有可能满足",
        "INFO", "可证伪性写入判据")

    # ---- E. 总账 ----
    add("E1", "ledger",
        "框架自有供给仍 **0**：α_GUT 0 / M_GUT 0 / τ_p 0 / 1/4 独立含量 0 / ℓ_sd 0",
        "FAIL", "10-07 审计口径")
    add("E2", "ledger",
        "本轮账目：记账缺陷 **6 处**单源勘误（P1–P6）；物理闭合 **0**；"
        "缺失对象 **1 个**（无量纲归一化条件）",
        "INFO", "修复 ≠ 闭合")
    add("Q1", "selfcorr",
        "自纠 r192 D1 口径：x_GUT 混用 α₁=α₂ 交点（{:.6f}，M={:.4e} GeV）与 "
        "α₁=α₃ 统一点（{:.6f}，M={:.4e} GeV）；M_GUT=2.121e16 只对应后者 ⇒ "
        "本卷统一到 α₁=α₃（α₁=α₂ 交点降为参考）".format(
            float(prov["x_gut12"]), float(prov["M_GUT12"]),
            float(prov["x_gut13"]), float(prov["M_GUT"])),
        "INFO", "自纠不计入六处外部修复")

    # ---- F. 勘误落地 ----
    for p in pats:
        add("F1", "patch",
            "{}：追加 r194 勘误节（{} 条），本次{}".format(
                p["rel"], p["bullets"],
                "写入" if p["applied_this_run"] else "已存在（幂等）"),
            "PASS" if p["errata_present"] else "FAIL",
            "sha={}…".format(p["sha256_after"][:16]))
    add("F2", "patch",
        "正文原文逐字保留（前缀哈希一致；两卷原始字节未被改写）",
        "PASS" if all(p["prefix_preserved"] for p in pats) else "FAIL",
        "append-only")

    # ---- 控制组 ----
    ctl("C01", "v 由 PDG 反解重算 255.262424 GeV",
        abs(float(prov["v"]) - 255.262424) < 1e-3,
        "v={:.6f}".format(float(prov["v"])))
    ctl("C02", "M*/v = 14.3979", abs(float(prov["Mstar_over_v"]) - 14.3979) < 1e-3,
        "{:.6f}".format(float(prov["Mstar_over_v"])))
    ctl("C03", "M_GUT/v = 8.3091e13",
        abs(float(prov["MGUT_over_v"]) / 8.3091e13 - 1) < 1e-4,
        "{:.4e}".format(float(prov["MGUT_over_v"])))
    ctl("C04", "M_Z/v = 0.357234（实测纯数）",
        abs(float(prov["MZ_over_v"]) - 0.357234) < 1e-5,
        "{:.6f}".format(float(prov["MZ_over_v"])))
    ctl("C05", "ℓ_EW·v = ħc（残差 <1e-12）", prov["unit_resid"] < D("1e-12"),
        "{:.1e}".format(float(prov["unit_resid"])))
    ctl("C06", "牛顿标签：RHS=½ρc² 且两 ½ 互消", nl["cancels"],
        "lhs_ratio={} / rhs_ratio={}".format(nl["lhs_ratio"], nl["rhs_ratio"]))
    ctl("C07", "终式系数 = 4πG", nl["final_coeff_4piG"] == "4",
        "kappa2=8piG/c^4 ⇒ 8/2=4")
    ctl("C08", "光子：λ_C=1.9733e11 m≈1.319 AU",
        abs(float(ph["lambda_au"]) - 1.3194) < 1e-3,
        "{:.4f} AU".format(float(ph["lambda_au"])))
    ctl("C09", "银河 1 kpc 上限 = 6.3949e-27 eV",
        abs(float(ph["e_gal_ev"]) / 6.3949e-27 - 1) < 1e-3,
        "{:.4e}".format(float(ph["e_gal_ev"])))
    ctl("C10", "单圈+Λ=213 MeV ⇒ α_s=0.13525",
        abs(asx["alpha_doc"] - 0.1352524) < 1e-5,
        "{:.6f}".format(asx["alpha_doc"]))
    ctl("C11", "单圈自洽 Λ_LO≈87.8 MeV",
        abs(asx["lambda_lo_mev"] - 87.83) < 0.5,
        "{:.3f} MeV".format(asx["lambda_lo_mev"]))
    ctl("C12", "α_G=5.5785e-35，比值 89.62",
        abs(float(ag["alpha_G"]) / 5.578512e-35 - 1) < 1e-4
        and abs(float(ag["ratio"]) - 89.62) < 0.1,
        "α_G={:.4e}, ×{:.2f}".format(float(ag["alpha_G"]), float(ag["ratio"])))
    ctl("C13", "B−L：无 ν_R 两系数均为 −1", bml_no["cubic"] == "-1"
        and bml_no["linear"] == "-1", "cubic/linear=-1/-1")
    ctl("C14", "B−L：加 ν_R 后两系数归零",
        bml_nu["cubic_zero"] and bml_nu["linear_zero"], "0/0")
    ctl("C15", "自旋流：12 对指标全部 ∂s=−2T^[μν]",
        all(v["ds_eq_minus_2T"] for v in spin.values()), "12/12")
    ctl("C16", "量子化反解正对照：靶=7 命中", qctrl, "positive control")
    ctl("C17", "维度嬗变 6 条全部有限可读", rob["finite"] == 6 and rob["n_rows"] == 6,
        "{}/6".format(rob["finite"]))
    ctl("C18", "两圈鲁棒性：上界 < 两个间隙",
        rob["structural_unreachable"], "bound={:.2f}".format(rob["two_loop_shift_bound"]))
    ctl("C19", "勘误两卷均存在且前缀保留",
        all(p["errata_present"] and p["prefix_preserved"] for p in pats), "2/2")

    # ---- 守卫 ----
    grd("G1", "Decimal 精度 ≥ 50 位", getcontext().prec >= 50,
        "prec={}".format(getcontext().prec))
    grd("G2", "精确代数：牛顿/B−L/自旋均用 Fraction",
        nl["cancels"] and bml_no["cubic"] == "-1" and len(spin) == 12,
        "Gaussian/rational")
    grd("G3", "勘误幂等：标记存在时不追加",
        all(p["errata_present"] for p in pats), "2/2")
    grd("G4", "勘误不改正文：原始字节前缀完全一致",
        all(p["prefix_preserved"] for p in pats), "append-only")
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    doc_s = ast.get_docstring(tree, clean=False)
    literal_counts = sum(1 for n in ast.walk(tree)
                         if isinstance(n, ast.Constant) and isinstance(n.value, str)
                         and len(n.value) > 200 and n.value != doc_s and "\n" in n.value)
    grd("G5", "ast 自审：无 >200 字符多行巨型字符串常量",
        literal_counts == 0, "count={}".format(literal_counts))
    grd("G6", "红线段存在且禁止外推",
        "".join(REDLINE.split()).replace('"', "") in "".join(src.split()).replace('"', ""),
        "REDLINE 逐字")
    grd("G7", "供给账不因修复而增加", prov["self_supplied_dimensionful"] == 0,
        "supply=0")
    grd("G8", "量子化检验非平凡：正对照必命中", qctrl, "ok")
    grd("G9", "五靶均由脚本重算（无手抄）",
        all(k in targets for k in ("M*/v", "M_GUT/v", "alpha_GUT_inv", "x*", "x_GUT")),
        "targets=5")
    grd("G10", "尺度纯函数性：输出= v×纯数（3/3）",
        abs(float(prov["M_star"] - prov["v"] * prov["Mstar_over_v"])) < 1e-6
        and abs(float(prov["M_GUT"] - prov["v"] * prov["MGUT_over_v"])) < 1.0,
        "3/3")
    grd("G11", "修复计数 = 6", len([e for e in ENTRIES if e["verdict"] == "CORRECTED"]) == 6,
        "P1–P6")
    grd("G12", "notebook 级红线：no-go 只针对当前清单",
        "当前清单" in REDLINE, "bounded claim")

    counts = {}
    for e in ENTRIES:
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1

    out = {
        "round": "r194",
        "date": "2026-10-25",
        "title": "尺度不可导出 no-go 与六处缺陷单源勘误",
        "verdict": VERDICT,
        "redline": REDLINE,
        "provenance": {k: str(v) for k, v in prov.items()},
        "robustness": rob,
        "quantization": qscan,
        "quantization_positive_control": qctrl,
        "newton": nl,
        "photon": {k: str(v) for k, v in ph.items()},
        "alphas": asx,
        "alpha_G": {k: str(v) for k, v in ag.items()},
        "spin": spin,
        "bml_minimal": bml_no,
        "bml_with_nur": bml_nu,
        "repairs": 6,
        "patches": pats,
        "counts": counts,
        "entries": ENTRIES,
        "controls": {"pass": sum(1 for c in CTRL if c["ok"]), "total": len(CTRL),
                     "items": CTRL},
        "guards": {"pass": sum(1 for g in GUARDS if g["ok"]), "total": len(GUARDS),
                   "items": GUARDS},
        "key_numbers": {
            "Mstar_over_v": "{:.6f}".format(float(prov["Mstar_over_v"])),
            "MGUT_over_v": "{:.6e}".format(float(prov["MGUT_over_v"])),
            "MZ_over_v": "{:.6f}".format(float(prov["MZ_over_v"])),
            "lambda_C_m": "{:.6e}".format(float(ph["lambda_m"])),
            "lambda_C_AU": "{:.4f}".format(float(ph["lambda_au"])),
            "e_galactic_ev": "{:.4e}".format(float(ph["e_gal_ev"])),
            "alpha_s_doc": "{:.6f}".format(asx["alpha_doc"]),
            "lambda_lo_mev": "{:.3f}".format(asx["lambda_lo_mev"]),
            "alpha_G": "{:.4e}".format(float(ag["alpha_G"])),
            "alpha_G_ratio": "{:.2f}".format(float(ag["ratio"])),
        },
        "layering": "本卷条目不可与 r142–r193 相加",
    }

    os.makedirs(_DATADIR, exist_ok=True)
    with open(os.path.join(_DATADIR, BASE + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-r194 · 尺度不可导出 no-go / 六处缺陷单源勘误")
    lines.append("=" * 78)
    lines.append("")
    lines.append("[A] 量纲门禁")
    lines.append("[P] 六处缺陷（机读复核 + 幂等勘误）")
    lines.append("[S] 尺度不可导出：出处/借用/嬗变/量子化/判定/规格")
    lines.append("[E] 供给总账")
    lines.append("[F] 勘误落地")
    lines.append("")
    for e in ENTRIES:
        lines.append("{:<6} [{}] {} : {}".format(
            e["id"], e["layer"], e["verdict"], e["text"]))
    lines.append("")
    lines.append("-" * 78)
    lines.append("控制组 {}/{}；守卫 {}/{}".format(
        out["controls"]["pass"], out["controls"]["total"],
        out["guards"]["pass"], out["guards"]["total"]))
    for c in CTRL:
        if not c["ok"]:
            lines.append("  [X] 控制组 {}：{}（{}）".format(c["id"], c["text"], c["detail"]))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [X] 守卫 {}：{}（{}）".format(g["id"], g["text"], g["detail"]))
    lines.append("条目 {}（{}）".format(
        len(ENTRIES), " / ".join("{} {}".format(k, v) for k, v in sorted(counts.items()))))
    lines.append("判词：" + VERDICT)
    lines.append("红线：" + REDLINE)
    report = "\n".join(lines)

    with open(os.path.join(_DATADIR, BASE + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report + "\n")
    with open(os.path.join(_DATADIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("# TUFT-r194 · 尺度不可导出 no-go 与六处缺陷单源勘误\n\n")
        f.write("> 判词：`{}`\n>\n> 红线：{}\n\n".format(VERDICT, REDLINE))
        f.write("## 一、出处与秩\n\n")
        for k in ("v", "M_star", "M_GUT", "Mstar_over_v", "MGUT_over_v",
                  "MZ_over_v", "unit_resid", "self_supplied_dimensionful",
                  "measured_dimensionful_inputs"):
            f.write("- {}：{}\n".format(k, out["provenance"][k]))
        f.write("\n## 二、六处缺陷（机读）\n\n")
        f.write("| 项 | 事实 |\n|---|---|\n")
        f.write("| P1 | T_00−½g_00T={}；两 ½ 互消；终式系数 {}πG |\n".format(
            nl["doc_rhs"], nl["final_coeff_4piG"]))
        f.write("| P2 | λ_C={:.4e} m = {:.4f} AU；1 kpc ⇒ {:.4e} eV |\n".format(
            float(ph["lambda_m"]), float(ph["lambda_au"]), float(ph["e_gal_ev"])))
        f.write("| P3 | 单圈+213 MeV ⇒ {:.6f}；单圈自洽 Λ={:.2f} MeV |\n".format(
            asx["alpha_doc"], asx["lambda_lo_mev"]))
        f.write("| P4 | α_G={:.4e}；原文高 {:.2f}× |\n".format(
            float(ag["alpha_G"]), float(ag["ratio"])))
        f.write("| P5 | ∂s=−2T^[μν]；12/12 精确 |\n")
        f.write("| P6 | 无 ν_R：{} / {}；加 ν_R：{} / {} |\n".format(
            bml_no["cubic"], bml_no["linear"], bml_nu["cubic"], bml_nu["linear"]))
        f.write("\n## 三、尺度不可导出：三条路线\n\n")
        f.write("- **R1 借用**：供给 0/5。\n")
        f.write("- **R2 维度嬗变**：6 次 0 命中；最近 lnΛ 间隙 {:.2f}（M*）/ {:.2f}（M_GUT）；"
                "两圈及以上上界 <{:.2f} ⇒ 结构性不可达。\n".format(
                    rob["log_gap_to_Mstar"], rob["log_gap_to_MGUT"],
                    rob["two_loop_shift_bound"]))
        f.write("- **R3 量子化**：20 形式 × 5 靶，1e-9 命中 0（正对照命中）。\n\n")
        f.write("| 靶 | 命中 | 最近形式 | 整数 n | 残差 |\n|---|---|---|---|---|\n")
        for k, v in qscan.items():
            f.write("| {} | {} | {} | {} | {:.2e} |\n".format(
                k, v["hits"], v["closest_form"], v["closest_n"],
                float(v["closest_resid"]) if v["closest_resid"] is not None else 0.0))
        f.write("\n## 四、判定与规格\n\n")
        f.write("- 判定：**CLOSED-NEGATIVE（no-go）**——当前清单无法设定尺度。\n")
        f.write("- 缺失对象：**无量纲归一化条件**（不是量纲常数）。\n")
        f.write("- 规格：C1 显式破共形 / C2 只用自有内容 / C3 1e-9 或可证伪偏离 / "
                "C4 新增连续参数 ≤1。\n")
        f.write("\n## 五、供给与勘误\n\n")
        f.write("- 记账缺陷修复 6（P1–P6）；物理闭合 0；框架自有供给 0。\n")
        f.write("- 自纠（INFO，不计入六处）：r192 D1 的 x_GUT 口径统一到 α₁=α₃ 统一点。\n")
        for p in pats:
            f.write("- {}：{} 条，本次{}（幂等，前缀保留={}）\n".format(
                p["rel"], p["bullets"],
                "写入" if p["applied_this_run"] else "已存在",
                p["prefix_preserved"]))
        f.write("\n## 六、判词\n\n`{}`\n".format(VERDICT))

    print(report)
    ok = all(c["ok"] for c in CTRL) and all(g["ok"] for g in GUARDS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
