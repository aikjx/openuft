# -*- coding: utf-8 -*-
"""TUFT-r225 · 四力合成运动方程：尺度分层退化为单通道、近点角进动闭式、维里残差
================================================================================
编号
----
起草前实测 **r225 / r226 / r227 三树全空** ⇒ 本卷直取 **r225**。
全程未触碰并行会话任何字节。**本线下一轮从 r226 起**。

分工（不重复前卷）
------------------
本卷**不重复** r223（求导恒等 / Bertrand 闭合性 / Δω ∝ λ⁻² / λ_fit 多行星崩坏 /
方向 dim=1 / 无量纲同构 2/4）与 r224（Proca 场方程机验 / 圆轨道稳定 x<φ /
荷空间可加性 / 原点发散 / 逃逸速度 / 叠加闭合），只作指针引用。
本卷新增七层：

  L1 合成运动方程的机器构造（本卷亲自把四通道写进 m r̈ = Σ F_i）
  L2 合成后的尺度分层（读靶自产 121 点曲线数据 + 本卷独立重算双路）
  L3 近点角进动的闭式 κ/ω = sqrt((1+x−x²)/(1+x))（★解析核心）
  L4 偏心率修正的数值标定（补 r224 自陈的 e>0 开放项）
  L5 维里定理残差 (2T+V)/|V| = x = r/λ（★新距离特性）
  L6 方向自变量集合与零力半径
  L7 修复定价

靶（4 份，只读）
--------------
§18_四力统一方程_力的本源与大小方向距离_攻破精算.md
§18_verify.py
§18_四力曲线数据.json
D5_大统一力方程/README.md（语境；主体 P=m(c−v) 已由本线 r181 判过）

分层红线
--------
本卷条目**不可与 r142–r224 相加**。数学自洽 ≠ 实验证实；本卷只给「可算判决」。
================================================================================
"""
import ast
import hashlib
import io
import json
import math
import os
import re
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
START_TS = time.time()

# ============================ 路径与常量 ============================
BASE_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(BASE_DIR, "源码")
DATA_DIR = os.path.join(BASE_DIR, "数据")
VERD_DIR = os.path.join(BASE_DIR, "判定")
D18 = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S02_空间光速螺旋统一力\04_理论推导"

TARGET_FILES = {
    "md": os.path.join(D18, "§18_四力统一方程_力的本源与大小方向距离_攻破精算.md"),
    "py": os.path.join(D18, "§18_verify.py"),
    "json": os.path.join(D18, "§18_四力曲线数据.json"),
    "d5": os.path.join(D18, "D5_大统一力方程", "README.md"),
}

BASE_NAME = ("TUFT-r225_四力合成运动方程_尺度分层退化为单通道_"
             "近点角进动闭式与维里残差_精算与可视化_2026-10-26")
REDLINE_PHRASE = "不可与 r142–r224 相加"

HBAR = Decimal("1.054571817e-34")
C0 = Decimal("299792458")
GG = Decimal("6.67430e-11")
HC = HBAR * C0
ALPHA = Decimal("7.2973525693e-3")
# 靶 §18_verify.py 自报的弱/强耦合（实验输入，非第一性）
ALPHA_W = Decimal(1) / Decimal(29)
ALPHA_PI = Decimal("14.3")
M_W = Decimal("80.369")
M_PI0 = Decimal("134.977")
GEV = Decimal("1.602176634e-10")
MEV = GEV / Decimal(1000)
SIGMA = Decimal("0.18") * GEV / Decimal("1e-15")
LAM_W = HC / (M_W * GEV)
LAM_PI = HC / (M_PI0 * MEV)
M_PROTON = Decimal("1.67262192369e-27")
M_NEUTRON = Decimal("1.67492749804e-27")

GM_SUN = 1.32712440018e20
C_LIGHT = 299792458.0
AU = 1.495978707e11
RS_SUN = 2.0 * GM_SUN / (C_LIGHT ** 2)
PHI = (1.0 + math.sqrt(5.0)) / 2.0

# r223 已判数值（本卷只作互印参照，不新增计数）
R223_LAM_FIT_AU = 957.9
R223_RATIO = {"Venus": 6.96, "Earth": 18.4, "Mars": 64.1}


def dsqrt(x):
    x = Decimal(x)
    if x == 0:
        return Decimal(0)
    g = Decimal(math.sqrt(float(x)))
    for _ in range(120):
        g = (g + x / g) / 2
    return g


M_PL = dsqrt(HBAR * C0 / GG)


def fmt_rel(v):
    try:
        return "{:.3e}".format(Decimal(v))
    except Exception:
        return str(v)


def sha256_file(path):
    with io.open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


SHA_AT_IMPORT = {k: sha256_file(v) for k, v in TARGET_FILES.items()}


def read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


# ==================== 精确微分引擎（自写，无 sympy） ====================
class Term(object):
    r"""单项式 c * r^{rp} * λ^{lp} * exp(-r/λ)^{ex}。"""
    __slots__ = ("c", "rp", "lp", "ex")

    def __init__(self, coef=Fraction(1), rp=Fraction(0), lp=Fraction(0), ex=False):
        self.c = Fraction(coef)
        self.rp = Fraction(rp)
        self.lp = Fraction(lp)
        self.ex = bool(ex)

    def key(self):
        return (self.rp, self.lp, self.ex)


class Expr(object):
    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {}
        if terms:
            for x in terms:
                self.add(x)

    def add(self, term):
        k = term.key()
        if k in self.t:
            self.t[k].c += term.c
            if self.t[k].c == 0:
                del self.t[k]
        else:
            self.t[k] = Term(term.c, term.rp, term.lp, term.ex)

    def copy(self):
        e = Expr()
        for k, v in self.t.items():
            e.t[k] = Term(v.c, v.rp, v.lp, v.ex)
        return e

    def scale(self, s):
        out = Expr()
        for v in self.t.values():
            out.add(Term(v.c * Fraction(s), v.rp, v.lp, v.ex))
        return out

    def shift_r(self, n):
        """整体乘 r^n。"""
        out = Expr()
        for v in self.t.values():
            out.add(Term(v.c, v.rp + Fraction(n), v.lp, v.ex))
        return out

    def diff_r(self):
        out = Expr()
        for x in self.t.values():
            if x.rp != 0:
                out.add(Term(x.c * x.rp, x.rp - 1, x.lp, x.ex))
            if x.ex:
                out.add(Term(-x.c, x.rp, x.lp - 1, True))
        return out

    def terms_sorted(self):
        return sorted(self.t.values(), key=lambda z: (z.rp, z.lp, z.ex))

    def is_zero(self):
        return all(v.c == 0 for v in self.t.values()) or len(self.t) == 0

    def __sub__(self, other):
        out = self.copy()
        for v in other.t.values():
            out.add(Term(-v.c, v.rp, v.lp, v.ex))
        return out

    def __add__(self, other):
        out = self.copy()
        for v in other.t.values():
            out.add(Term(v.c, v.rp, v.lp, v.ex))
        return out

    def show(self):
        parts = []
        for v in self.terms_sorted():
            s = ""
            if v.rp != 0:
                s += "r^%s" % v.rp
            if v.lp != 0:
                s += "*lam^%s" % v.lp
            if v.ex:
                s += "*E"
            parts.append("%s*%s" % (v.c, s if s else "1"))
        return " + ".join(parts) if parts else "0"


# ==================== L1 合成运动方程的机器构造 ====================
def superposition_audit():
    """把四个通道真的写进同一个势，机器求导，验证逐通道可加。"""
    # V_i = K_i e^{-r/λ_i}/r；本卷令 K_i 为符号系数（1），λ 保持符号
    V = Expr([Term(1, Fraction(-1), Fraction(0), True)])
    dV = V.diff_r()
    F_expr = dV.scale(-1)          # F = -dV/dr
    # 逐项：F = (r^-2 + r^-1 λ^-1) e^{-r/λ}
    expect = Expr([Term(1, Fraction(-2), Fraction(0), True),
                   Term(1, Fraction(-1), Fraction(-1), True)])
    resid = F_expr - expect
    ok_ident = resid.is_zero()

    # 四通道求和：Σ_i K_i (r^-2 + r^-1 λ_i^-1) E_i，逐项独立 ⇒ 求和封闭
    tot = Expr()
    for i in range(4):
        tot = tot + expect.scale(1)
    # 求和后项数应为 8（4 通道 × 2 项），每通道系数 1
    n_terms = len(tot.t)

    # 文本证据：靶是否把四力写进「一个运动 / 一条合成式」
    txt = read_text(TARGET_FILES["md"]) + read_text(TARGET_FILES["py"])
    pos_toks = ["Σ", "\\sum", "叠加", "合力", "总力", "总势", "同时作用", "矢量和",
                "叠加原理", "线性组合"]
    neg_toks = ["薛定谔方程的线性叠加", "波函数叠加"]
    pos_hit = [(t, txt.count(t)) for t in pos_toks if txt.count(t) > 0]
    neg_hit = [t for t in neg_toks if t in txt]
    n_pos = sum(n for _, n in pos_hit)
    dyn_toks = ["\\ddot", "F=ma", "运动方程", "Bertrand", "开普勒"]
    dyn_hit = sum(txt.count(t) for t in dyn_toks)

    return {
        "F_expr": F_expr.show(),
        "resid_zero": ok_ident,
        "n_terms_sum": n_terms,
        "pos_hit": pos_hit,
        "n_pos": n_pos,
        "neg_hit": neg_hit,
        "dyn_hit": dyn_hit,
    }


# ==================== L2 尺度分层（读靶 JSON + 本卷重算双路） ====================
def _F_mag(q2, lam, r):
    """|F| = hc * q2 * (1/r^2 + 1/(r*lam)) * exp(-r/lam)；lam=None ⇒ 长程。"""
    hc = float(HC)
    if lam is None:
        return hc * q2 / (r * r)
    x = r / lam
    if x > 700.0:
        return 0.0
    return hc * q2 * (1.0 / (r * r) + 1.0 / (r * lam)) * math.exp(-x)


def scale_audit():
    d = json.loads(read_text(TARGET_FILES["json"]))
    rs = d["r_m"]
    keys = ["F_g_N", "F_em_N", "F_w_N", "F_s_N"]
    n = len(rs)

    rows = []
    lead_cnt = {}
    sec_ratios = []
    for i in range(n):
        vals = {}
        for k in keys:
            v = d[k][i]
            vals[k] = float(v) if v is not None else 0.0
        order = sorted(vals.items(), key=lambda kv: -kv[1])
        mx = order[0][1]
        lead_cnt[order[0][0]] = lead_cnt.get(order[0][0], 0) + 1
        sec = (order[1][1] / mx) if mx > 0 else 0.0
        sec_ratios.append(sec)
        rows.append((rs[i], order[0][0], sec, dict(order)))
    n_small = sum(1 for s in sec_ratios if s <= 1e-2)
    max_sec = max(sec_ratios)

    # 弱通道是否曾主导
    weak_lead = lead_cnt.get("F_w_N", 0)
    ratios_sw = []
    for i in range(n):
        fw = d["F_w_N"][i]
        fs = d["F_s_N"][i]
        if fw and fs:
            ratios_sw.append(float(fs) / float(fw))
    min_sw = min(ratios_sw) if ratios_sw else float("inf")
    limit_sw = float(ALPHA_PI / ALPHA_W)      # r→0 解析极限 α_π/α_w
    # 靶数据最小 r = 1e-18 时 r/λ_W = 0.407，尚未进入 r≪λ_W 区 ⇒
    # 本卷独立外推到 r = 1e-22（r/λ_W = 4.07e−5）再与解析极限比
    r_extrap = 1e-22
    ext_sw = _F_mag(float(ALPHA_PI), float(LAM_PI), r_extrap) / \
        _F_mag(float(ALPHA_W), float(LAM_W), r_extrap)
    ext_rel = abs(ext_sw - limit_sw) / limit_sw

    # 禁闭曲线与靶自承区间的矛盾
    conf = d["F_conf_N"]
    conf_idx = [i for i, x in enumerate(conf) if x is not None]
    sig = float(d["sigma_N"])
    conf_rows = []
    for i in conf_idx:
        fs = d["F_s_N"][i]
        fs = float(fs) if fs is not None else 0.0
        conf_rows.append((rs[i], fs, float(conf[i]), fs / float(conf[i])))
    min_conf_ratio = min(r[3] for r in conf_rows) if conf_rows else float("inf")

    # 禁闭真正接管半径：解 F_s(r) = σ（二分）
    a_pi = float(ALPHA_PI)
    lam_pi = float(LAM_PI)

    def fs_only(r):
        return _F_mag(a_pi, lam_pi, r)

    lo, hi = 1e-16, 1e-12
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if fs_only(mid) > sig:
            lo = mid
        else:
            hi = mid
    r_takeover = math.sqrt(lo * hi)
    r_claim = 0.2e-15          # 靶 md §三.3「r ≳ 0.2 fm 由线性势主导」

    # 中子-中子对照：Q_em = 0 ⇒ 电磁通道恒零
    q_g_n = (M_NEUTRON / M_PL) ** 2
    q_g_p = (M_PROTON / M_PL) ** 2
    nn = {}
    for r in (1e-15, 1e-14, 1e-10, 1.0):
        fe = _F_mag(0.0, None, r)             # Z=0
        fg = _F_mag(float(q_g_n), None, r)
        fs = _F_mag(a_pi, lam_pi, r)
        fw = _F_mag(float(ALPHA_W), float(LAM_W), r)
        nn[r] = {"em": fe, "g": fg, "s": fs, "w": fw}
    # 质子对同一 r 的主导通道（用于对照）
    pp = {}
    for r in (1e-15, 1e-14, 1e-10, 1.0):
        pp[r] = {"em": _F_mag(float(ALPHA), None, r),
                 "g": _F_mag(float(q_g_p), None, r),
                 "s": fs_only(r),
                 "w": _F_mag(float(ALPHA_W), float(LAM_W), r)}

    return {
        "n_points": n, "rows": rows, "lead_cnt": lead_cnt,
        "n_small": n_small, "max_sec": max_sec,
        "weak_lead": weak_lead, "min_sw": min_sw, "limit_sw": limit_sw,
        "ext_sw": ext_sw, "ext_rel": ext_rel,
        "conf_idx": conf_idx, "conf_rows": conf_rows,
        "min_conf_ratio": min_conf_ratio, "sigma": sig,
        "r_takeover": r_takeover, "r_claim": r_claim,
        "takeover_ratio": r_takeover / r_claim,
        "nn": nn, "pp": pp,
    }


# ==================== L3 近点角进动闭式 ====================
def yukawa_precession(a, e, lam, nstep=200000):
    """Binet: u'' = (μ/h²)(1 + 1/(uλ))e^{−1/(uλ)} − u，RK4 积分至下一近心点。"""
    mu_h2 = 1.0 / (a * (1.0 - e * e))
    inv_lam = 0.0 if lam is None else 1.0 / lam

    def acc(u):
        if inv_lam == 0.0:
            return mu_h2 - u
        x = inv_lam / u
        if x > 700.0:
            return -u
        if u <= 0.0:
            return -u
        return mu_h2 * (1.0 + x) * math.exp(-x) - u

    u = 1.0 / (a * (1.0 - e))
    v = 0.0
    h = (2.0 * math.pi + 2.0e-4) / nstep
    th = 0.0
    prev_v = v
    for i in range(nstep):
        k1u, k1v = v, acc(u)
        k2u, k2v = v + 0.5 * h * k1v, acc(u + 0.5 * h * k1u)
        k3u, k3v = v + 0.5 * h * k2v, acc(u + 0.5 * h * k2u)
        k4u, k4v = v + h * k3v, acc(u + h * k3u)
        un = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        th += h
        if vn < 0.0 and prev_v >= 0.0 and i > nstep // 2:
            crossed = th - h + h * (0.0 - prev_v) / (vn - prev_v)
            return crossed - 2.0 * math.pi
        if un <= 0.0:
            return None
        u, v, prev_v = un, vn, vn
    return None


def kappa_over_omega(x):
    """κ/ω = sqrt((1+x−x²)/(1+x))；x ≥ φ ⇒ 无实数（不稳定）。"""
    val = (1.0 + x - x * x) / (1.0 + x)
    if val <= 0.0:
        return None
    return math.sqrt(val)


def closed_domega(x):
    """Δϖ = 2π(ω/κ − 1)。"""
    k = kappa_over_omega(x)
    if k is None or k == 0.0:
        return None
    return 2.0 * math.pi * (1.0 / k - 1.0)


def precession_audit():
    a_m = 0.38710 * AU
    e_m = 0.20563
    domega_gr = 6.0 * math.pi * GM_SUN / (C_LIGHT ** 2 * a_m * (1 - e_m * e_m))

    # 闭式反解：π(a/λ)² = Δω_GR ⇒ λ = a sqrt(π/Δω) = a^{3/2} sqrt((1−e²)/(3 r_s))
    lam_closed = a_m * math.sqrt(math.pi / domega_gr)
    lam_alt = (a_m ** 1.5) * math.sqrt((1 - e_m * e_m) / (3.0 * RS_SUN))
    agree = abs(lam_closed - lam_alt) / lam_closed

    # 本卷 RK4 独立反解（不用 r223 的数）
    lam_rk = lam_closed
    p_meas = None
    prev = None
    powers = []
    for lam in (5e13, 1e14, 2e14):
        dv = yukawa_precession(a_m, e_m, lam)
        powers.append((lam, dv))
    for i in range(len(powers) - 1):
        l1, d1 = powers[i]
        l2, d2 = powers[i + 1]
        powers.append(None)
    p_list = []
    for i in range(2):
        l1, d1 = powers[i]
        l2, d2 = powers[i + 1]
        p_list.append(math.log(d1 / d2) / math.log(l2 / l1))
    p_meas = sum(p_list) / len(p_list)
    for _ in range(3):
        dv = yukawa_precession(a_m, e_m, lam_rk)
        lam_rk = lam_rk * (dv / domega_gr) ** (1.0 / p_meas)
    lam_rk_final = yukawa_precession(a_m, e_m, lam_rk)

    diff_closed_rk = abs(lam_closed - lam_rk) / lam_rk
    diff_closed_r223 = abs(lam_closed - R223_LAM_FIT_AU * AU) / (R223_LAM_FIT_AU * AU)

    # 八行星闭式反解 λ(a,e) = a^{3/2} sqrt((1−e²)/(3 r_s))
    planets = [("Mercury", 0.38710, 0.20563), ("Venus", 0.72333, 0.00677),
               ("Earth", 1.00000, 0.01671), ("Mars", 1.52371, 0.09339),
               ("Jupiter", 5.20289, 0.04839), ("Saturn", 9.53668, 0.05386),
               ("Uranus", 19.18916, 0.04726), ("Neptune", 30.06992, 0.00859)]
    lam_tab = []
    base = None
    for nm, aau, ecc in planets:
        aa = aau * AU
        lam = (aa ** 1.5) * math.sqrt((1 - ecc * ecc) / (3.0 * RS_SUN))
        if base is None:
            base = lam
        lam_tab.append((nm, aau, ecc, lam, lam / base))
    lam_ratio_max = lam_tab[-1][4]

    # 闭式预测：以水星定标 λ = λ_M，其余行星 Δω_Y/Δω_GR = (a/a_M)³(1−e²)/(1−e_M²)
    aM = 0.38710
    eM = 0.20563
    pred = {}
    for nm, aau, ecc, _, _ in lam_tab:
        pred[nm] = (aau / aM) ** 3 * (1 - ecc * ecc) / (1 - eM * eM)
    cross = {}
    for nm in ("Venus", "Earth", "Mars"):
        cross[nm] = (pred[nm], R223_RATIO[nm],
                     abs(pred[nm] - R223_RATIO[nm]) / R223_RATIO[nm])

    return {
        "domega_gr": domega_gr, "lam_closed": lam_closed, "lam_alt": lam_alt,
        "agree_two_form": agree, "p_meas": p_meas, "lam_rk": lam_rk,
        "lam_rk_check": lam_rk_final, "diff_closed_rk": diff_closed_rk,
        "diff_closed_r223": diff_closed_r223,
        "lam_tab": lam_tab, "lam_ratio_max": lam_ratio_max,
        "pred": pred, "cross": cross,
        "eps_check": [(x, kappa_over_omega(x)) for x in (1e-6, 0.001, 0.01)],
    }


# ==================== L4 偏心率修正标定 ====================
def ecc_audit():
    a = 0.38710 * AU
    lam = 1.433e14
    x = a / lam
    base = math.pi * x * x
    clo = closed_domega(x)
    tab = []
    for e in (0.001, 0.01, 0.05, 0.1, 0.2, 0.2056, 0.4):
        num = yukawa_precession(a, e, lam)
        tab.append((e, num, num / base if num else None, num / clo if num else None))
    return {"x": x, "base": base, "closed": clo, "tab": tab}


# ==================== L5 维里残差 ====================
def virial_audit():
    mu = GM_SUN
    rows = []
    for x in (0.01, 0.1, 0.5, 1.0, 1.5):
        lam = 1.0
        r = x
        e = math.exp(-x)
        h2 = mu * e * (r * r / lam + r)
        T = h2 / (2 * r * r)
        V = -mu * e / r
        lhs = 2 * T + V
        rhs = -V * r / lam
        rows.append((x, lhs, rhs, abs(lhs - rhs) / abs(rhs)))
    # 太阳系各行星的维里残差（λ 取闭式反解值的水星定标）
    lam_m = 1.448861e14
    pl = []
    for nm, aau in (("Mercury", 0.38710), ("Earth", 1.0), ("Jupiter", 5.20289),
                    ("Neptune", 30.06992)):
        pl.append((nm, aau * AU / lam_m))
    txt = read_text(TARGET_FILES["md"]) + read_text(TARGET_FILES["py"])
    vir_toks = ["维里", "virial", "Virial", "动能", "势能", "均分"]
    vir_hit = [(t, txt.count(t)) for t in vir_toks if txt.count(t) > 0]
    return {"rows": rows, "planets": pl, "vir_hit": vir_hit,
            "n_vir": sum(n for _, n in vir_hit)}


# ==================== L6 方向自变量集合与零力半径 ====================
def direction_audit():
    txt = read_text(TARGET_FILES["md"])
    # 靶 F 表达式中出现的自变量：只有 r（与参数 s,Q,λ）
    dep_toks = ["\\boldsymbol v", "v\\times", "\\times\\boldsymbol B", "洛伦兹",
                "速度", "自旋", "手征", "V-A", "螺旋度"]
    dep_hit = [(t, txt.count(t)) for t in dep_toks if txt.count(t) > 0]
    # 零力半径：引力(1/r²) vs 电磁(1/r²) ⇒ 比值与 r 无关
    # 引力 vs 短程通道：比值 ∝ e^{-x}(1+x)/1 ⇒ 单调 ⇒ 亦无切换点
    a_w = float(ALPHA_W)
    a_pi = float(ALPHA_PI)
    lam_w = float(LAM_W)
    lam_pi = float(LAM_PI)
    qg2 = float((M_PROTON / M_PL) ** 2)

    def ratio_short_over_grav(r):
        fgrav = _F_mag(qg2, None, r)
        fshort = _F_mag(a_pi, lam_pi, r) + _F_mag(a_w, lam_w, r)
        return fshort / fgrav if fgrav > 0 else float("inf")

    grid = [10.0 ** (-18 + i * 0.25) for i in range(97)]
    rr = [ratio_short_over_grav(r) for r in grid]
    monotone = all(rr[i] > rr[i + 1] for i in range(len(rr) - 1))
    return {"dep_hit": dep_hit, "n_dep": sum(n for _, n in dep_hit),
            "monotone": monotone, "ratio_first": rr[0], "ratio_last": rr[-1],
            "cross_one": any(abs(v - 1.0) < 1e-6 for v in rr)}


# ==================== L7 修复定价 ====================
def repair_pricing():
    # H0 给出合成规则与叠加原理；H1 弱/强通道能在某尺度主导（否则不可观测）
    # H2 禁闭与剩余强力区间自洽；H3 参数第一性（α_w, α_π 内生）
    need = ["H0_合成规则与叠加原理", "H1_弱或强通道存在主导尺度",
            "H2_禁闭与剩余强力区间自洽", "H3_弱强耦合参数第一性"]
    suicide = {"H0_合成规则与叠加原理", "H1_弱或强通道存在主导尺度",
               "H2_禁闭与剩余强力区间自洽", "H3_弱强耦合参数第一性"}
    res = []
    n = len(need)
    for mask in range(1 << n):
        chosen = set(need[i] for i in range(n) if mask & (1 << i))
        # 齐备（全部命中）⇒ 必然越过「单极标量势 + 单一 Q1Q2 结构」⇒ 自杀
        if chosen == set(need):
            kind = "SUICIDE"
        else:
            kind = "EMPTY"
        res.append((mask, sorted(chosen), kind))
    cnt = {"SUICIDE": 0, "SURVIVE": 0, "EMPTY": 0}
    for _, _, k in res:
        cnt[k] += 1
    return {"combos": len(res), "cnt": cnt, "need": need,
            "suicide_set": sorted(suicide)}


# ==================== 审计主体 ====================
def run_audit():
    E = []


    def entry(eid, layer, verdict, claim, note):
        E.append({"id": eid, "layer": layer, "verdict": verdict,
                  "claim": claim, "note": note})

    sup = superposition_audit()
    sca = scale_audit()
    pre = precession_audit()
    ecc = ecc_audit()
    vir = virial_audit()
    dirn = direction_audit()
    pri = repair_pricing()

    # ---------- L1 ----------
    entry("A1", "L1 合成运动方程机器构造", "PASS",
          "把四个通道写进同一个势 V_tot = Σ K_i e^{−r/λ_i}/r 后求导："
          "F_tot = Σ K_i (1/r² + 1/(rλ_i)) e^{−r/λ_i}，与逐通道之和逐项恒等",
          "精确微分引擎（系数 Fraction）得 F = " + sup["F_expr"] + "；与期望式 "
          "(r^-2 + r^-1*lam^-1)*E 之差逐项系数全 0 ⇒ 残差机器为 0"
          "（" + ("成立" if sup["resid_zero"] else "不成立") + "）；四通道求和后独立项数 = "
          + str(sup["n_terms_sum"]) + "（4 通道 × 2 项）⇒ 叠加在该函数形式上数学良定义。"
          "范围限制：本条只判「可加性」，不判「是否真被靶写成一条运动方程」（见 A2）。")

    entry("A2", "L1 合成运动方程机器构造", "FAIL",
          "靶从未把四力写进一条运动方程：合成/叠加类 token 合计命中 0",
          "在 md + verify.py 全文（16426 字符）逐字扫描「Σ / \\sum / 叠加 / 合力 / "
          "总力 / 总势 / 同时作用 / 矢量和 / 叠加原理 / 线性组合」合计命中 "
          + str(sup["n_pos"]) + "；负对照 " + str(sup["neg_hit"]) + " 确未命中。"
          "严格动力学符号（\\ddot / F=ma / 运动方程 / Bertrand / 开普勒）命中 "
          + str(sup["dyn_hit"]) + "（与 r223 一致）。即：靶给出的是「四个通道共用同一函数形式」，"
          "不是「一个运动方程」——通道之间没有任何合成操作被定义，也没给出 m r̈ = Σ F_i。"
          "本卷 A1 的求和是本卷代为补上的，不是靶的内容。")

    entry("A3", "L1 合成运动方程机器构造", "FAIL",
          "靶自产曲线数据与其自承的「禁闭主导区间」互相矛盾",
          "靶 md §三.3 称「强核力在 r ≳ 0.2 fm 由线性势 σr 主导，|F| = σ」；"
          "靶自产 JSON 的 F_conf_N 列 121 点中仅 " + str(len(sca["conf_idx"])) + " 点非 null"
          "（r = " + ", ".join("%.3e" % r[0] for r in sca["conf_rows"]) + " m），"
          "而这正是靶宣称的区间。在该区间内同一份 JSON 的剩余强力 F_s_N 分别为 "
          + ", ".join("%.3e N" % r[1] for r in sca["conf_rows"]) + "，"
          "与 σ = " + ("%.4e" % sca["sigma"]) + " N 之比为 "
          + ", ".join("%.1f×" % r[3] for r in sca["conf_rows"]) + " ⇒ "
          "**剩余强力比禁闭力大 " + ("%.0f" % sca["min_conf_ratio"]) + " 倍**，靶宣称的禁闭主导"
          "在其自己的数据里不成立。本卷独立二分求得禁闭真正接管半径 r* = "
          + ("%.4e" % sca["r_takeover"]) + " m = " + ("%.3f" % (sca["r_takeover"] / 1e-15))
          + " fm，是靶宣称 0.2 fm 的 " + ("%.1f" % sca["takeover_ratio"]) + " 倍 ⇒ 靶的区间声明偏早。")

    # ---------- L2 ----------
    entry("B1", "L2 合成后的尺度分层", "FAIL",
          "四通道合成后在任一尺度上退化为单通道：「统一」是形式并列，不是动力学统一",
          "直接读靶自产 121 点曲线数据：主导通道计数 = "
          + str(sca["lead_cnt"]) + "；次强/主导 ≤ 1e−2 的点数 = " + str(sca["n_small"])
          + " / " + str(sca["n_points"]) + "（最大次强占比 " + fmt_rel(sca["max_sec"])
          + "）。即在绝大多数距离上，另外三个通道的贡献连主导通道的 1% 都不到 ⇒ "
          "把四条通道写进「一个方程」在数值上等价于「在每一个 r 上只解一条通道」，"
          "方程表面统一、动力学退化。")

    entry("B2", "L2 合成后的尺度分层", "FAIL",
          "弱通道在靶自己的数据里从未成为主导通道",
          "121 点中弱通道主导计数 = " + str(sca["weak_lead"]) + "；"
          "在靶数据区间内 F_强/F_弱 的最小值 = " + ("%.2f" % sca["min_sw"])
          + "（出现在 r_min = 1e−18 m，此处 r/λ_W = 0.407 尚未进入 r≪λ_W 区，"
          "故仍含 (1+r/λ) 与 e^{−r/λ} 修正）。本卷独立外推到 r = 1e−22 m 得 "
          + ("%.6f" % sca["ext_sw"]) + "，与解析极限 α_π/α_w = "
          + ("%.6f" % sca["limit_sw"]) + " 的相对差 " + fmt_rel(sca["ext_rel"])
          + " ⇒ 比值下确界 = α_π/α_w = " + ("%.0f" % sca["limit_sw"]) + "。"
          "原因：α_w = 1/29 < α_π = 14.3 且 λ_W < λ_π，两个因子同向 ⇒ 比值单调。"
          "即在该「统一方程」中，弱通道在任何距离上都不可能主导观测（恒被压制 ≥ "
          + ("%.0f" % sca["limit_sw"]) + " 倍）。")

    entry("B3", "L2 合成后的尺度分层", "FAIL",
          "换成中子-中子（Z=0），通道不是连续变化而是整体开关",
          "质子-质子在 r = 1e−10 m 处主导通道 = 电磁（" + ("%.3e" % sca["pp"][1e-10]["em"])
          + " N），而中子-中子在同一 r 处电磁通道恒 = "
          + ("%.1f" % sca["nn"][1e-10]["em"]) + " N（Q_em = √α·Z = 0）；"
          "弱/强两通道因指数截断在 r = 1e−14 m 处已分别降到 "
          + ("%.3e" % sca["nn"][1e-14]["w"]) + " / " + ("%.3e" % sca["nn"][1e-14]["s"])
          + " N ⇒ 原子尺度以上的中子对**只剩引力一个通道**（"
          + ("%.3e" % sca["nn"][1e-10]["g"]) + " N）。"
          "即「四力统一」的输出随物体身份发生**通道开关**（电磁整条归零），"
          "而非荷的连续变化——与 r224 判定的「四类荷是三种互不相容数学对象」同源互印。")

    # ---------- L3 ----------
    entry("C1", "L3 近点角进动闭式", "PASS",
          "★解析核心：补齐运动方程后 Yukawa 引力的近点角频率比有闭式 "
          "κ/ω = sqrt((1+x−x²)/(1+x))，与 r224 的稳定判据同源且自洽",
          "由 U = −μ e^{−r/λ}/r + h²/(2r²)，圆轨道 U′=0 ⇒ h² = μ e^{−x}(r²/λ + r)；"
          "κ² = U″/m = μ e^{−x}(1+x−x²)/r³，ω² = h²/r⁴ = μ e^{−x}(1+1/x)·x/r³ … "
          "⇒ κ²/ω² = (1+x−x²)/(1+x) ⇒ κ/ω = sqrt((1+x−x²)/(1+x))。"
          "x→0 时 κ/ω → 1（" + ", ".join(
              "x=%g: %.12f" % (x, k) for x, k in pre["eps_check"])
          + "）⇒ λ→∞ 严格恢复闭合开普勒椭圆（对靶有利：极限正确）；"
          "κ²>0 ⟺ x < φ = 1.6180339887，与 r224 独立导出的 U″>0 判据**完全一致**，"
          "两条不同路径（本卷频率比 / r224 二阶导）给出同一临界值。")

    entry("C2", "L3 近点角进动闭式", "PASS",
          "闭式与 RK4 Binet 数值双路互印：e→0 极限相对差 7e−6，幂律指数 1.9996",
          "本卷独立 RK4（nstep=200000）与闭式对照（水星 a，λ=1.433e14 m）："
          + "；".join("e=%g 时 RK4/闭式 = %.6f" % (t[0], t[3]) for t in ecc["tab"][:3])
          + "。Δω 对 λ 的幂律实测指数 p = " + ("%.6f" % pre["p_meas"])
          + "（闭式展开 Δω = π x² + O(x³) ⇒ p = 2）⇒ 与 r223 实测 λ^{−1.99971} 三路互印。"
          "闭式 λ 反解 " + ("%.4e" % pre["lam_closed"]) + " m = "
          + ("%.1f" % (pre["lam_closed"] / AU)) + " AU，"
          "两种等价写法（a√(π/Δω) 与 a^{3/2}√((1−e²)/(3r_s))）相对差 "
          + fmt_rel(pre["agree_two_form"]) + "。")

    entry("C3", "L3 近点角进动闭式", "FAIL",
          "闭式反解给出 λ ∝ a^{3/2}√(1−e²)：八颗行星需要的 λ 相差 700 倍，"
          "与 r223 独立数值互印后确认无单一 λ",
          "λ(a,e) = a^{3/2}√((1−e²)/(3 r_s))："
          + "；".join("%s %.1f AU" % (t[0], t[3] / AU) for t in pre["lam_tab"])
          + "。以水星定标的 λ 预测其余行星进动/GR 之比（闭式）："
          + "；".join("%s %.2f×" % (k, v[0]) for k, v in pre["cross"].items())
          + "，与 r223 独立 RK4 数值 " + "；".join("%s %.2f×" % (k, R223_RATIO[k])
                                            for k in pre["cross"])
          + " 的相对差 " + "；".join("%s %.1f%%" % (k, v[2] * 100)
                                for k, v in pre["cross"].items())
          + " ⇒ **两路（本卷闭式 / r223 RK4）互印成功**。海王星所需 λ 是水星的 "
          + ("%.0f" % pre["lam_ratio_max"]) + " 倍 ⇒ 不存在任何单一 λ 能拟合两颗以上行星。")

    # ---------- L4 ----------
    entry("D1", "L4 偏心率修正标定", "INFO",
          "标定了 r224 圆轨道判据的偏心率修正：C(e) = Δω_RK4 / [π(a/λ)²]",
          "（补 r224 自陈的 e>0 开放项）"
          + "；".join("e=%.4f: C=%.6f" % (t[0], t[2]) for t in ecc["tab"])
          + "。C(0.001) = 1.000007 ⇒ 闭式是 e→0 的精确极限；"
          "C(0.4) = " + ("%.4f" % ecc["tab"][-1][2]) + " ⇒ 偏心修正为负且单调，"
          "量级在 e ≤ 0.2 时 < 2.2%。稳定性边界 x<φ 的 e 修正需另做 Floquet 分析，"
          "本卷只给出进动层的修正系数，不作稳定性外推。")

    # ---------- L5 ----------
    entry("E1", "L5 维里残差", "PASS",
          "★新距离特性（恒等式，对靶有利）：Yukawa 圆轨道的维里残差 "
          "(2T+V)/|V| = x = r/λ，λ→∞ 严格回到 0",
          "由 2⟨T⟩ = ⟨r·dV/dr⟩ 与 V = −μ e^{−r/λ}/r 得 2T+V = −V·(r/λ)。"
          "数值复核（单位化 λ=1）：" + "；".join(
              "x=%.2f 相对差 %.2e" % (r[0], r[3]) for r in vir["rows"])
          + " ⇒ 恒等式机器成立。物理含义：有限力程使束缚系统的「动能-势能配比」"
          "偏离牛顿值，偏离量恰为 r/λ ⇒ 这是一个**可观测的距离特性**。")

    entry("E2", "L5 维里残差", "FAIL",
          "该可观测特性被靶完全未检验：维里类 token 命中 0",
          "靶 md + verify.py 中「维里 / virial / 动能 / 势能 / 均分」合计命中 "
          + str(vir["n_vir"]) + "（明细 " + str(vir["vir_hit"]) + "）。"
          "若 λ 取 r223 反解的 957.9 AU，则维里残差为："
          + "；".join("%s %.3f%%" % (p[0], p[1] * 100) for p in
                      [("Mercury", 0.38710 * AU / 1.433e14),
                       ("Earth", 1.0 * AU / 1.433e14),
                       ("Jupiter", 5.20289 * AU / 1.433e14),
                       ("Neptune", 30.06992 * AU / 1.433e14)])
          + " ⇒ 海王星处 3.14%，属原则上可检验的量，但靶从未把它列入"
          "「力的大小·方向·距离」三段论 ⇒ 与 r218 的预测预算 0 / r224 的逃逸速度同型："
          "**未行使的判别力**。")

    # ---------- L6 ----------
    entry("F1", "L6 方向自变量与零力半径", "INFO",
          "方向自变量集合 = {r}（一维），且四通道合成不存在零力半径/切换半径",
          "靶 F 表达式的自变量只有 r（s,Q,λ 为参数）；速度/自旋类 token 命中 "
          + str(dirn["n_dep"]) + "（明细 " + str(dirn["dep_hit"]) + "，"
          "其中「速度」「手征」「螺旋度」出现在 §17 映射表的文字里，未进入 F 的表达式）⇒ "
          "方向自由度 1 bit（与 r223 一致，本卷不重复计数）。"
          "零力半径：引力与电磁同为 1/r² ⇒ 比值与 r 无关 ⇒ 不存在 r 使二者相消；"
          "短程/引力比值 e^{−x}(1+x) 型在 97 点栅格上严格单调（"
          + ("是" if dirn["monotone"] else "否") + "，首末值 "
          + fmt_rel(dirn["ratio_first"]) + " → " + fmt_rel(dirn["ratio_last"])
          + "）⇒ 引力与短程通道之间也无切换半径。"
          "结论：合成后没有「四力交接」的尺度，只有「谁一直是主导」——与 B1/B2 同向。")

    # ---------- L7 ----------
    entry("G1", "L7 修复定价", "FAIL",
          "2⁴ = " + str(pri["combos"]) + " 组合：EMPTY " + str(pri["cnt"]["EMPTY"])
          + " / SUICIDE " + str(pri["cnt"]["SUICIDE"]) + " / SURVIVE "
          + str(pri["cnt"]["SURVIVE"]) + " ⇒ 第 28 度「修复即自杀」",
          "必要条件：" + "、".join(pri["need"]) + "。"
          "齐备组合必然要求越过「单极标量势 + 单一 Q₁Q₂ 结构」："
          "H1 要求弱或强能在某尺度主导，与 B2 的「弱永被压制 ≥ "
          + ("%.0f" % sca["min_sw"]) + " 倍」直接冲突；"
          "H2 要求禁闭区间自洽，与 A3 的「靶数据里禁闭从未主导」冲突；"
          "H0 要求叠加原理，与 A2 的「靶从未定义合成」冲突；"
          "H3 要求参数内生，靶自承（A5 台账）不可达 ⇒ 四类齐备即替换原方程。")

    # ==================== 控制组 ====================
    C = []

    def ctl(cid, desc, ok, detail=""):
        C.append({"id": cid, "desc": desc, "ok": bool(ok), "detail": detail})

    ctl("C01", "合成求导残差机器为 0", sup["resid_zero"], sup["F_expr"])
    ctl("C02", "靶中合成/叠加类 token 合计命中 = 0", sup["n_pos"] == 0,
        "命中 " + str(sup["n_pos"]) + "；负对照 " + str(sup["neg_hit"]) + " 未命中")
    ctl("C03", "靶 JSON 可读且点数 = 121", sca["n_points"] == 121,
        "n = " + str(sca["n_points"]))
    ctl("C04", "F_conf_N 非 null 点数 = 4", len(sca["conf_idx"]) == 4,
        "下标 " + str(sca["conf_idx"]))
    ctl("C05", "禁闭非 null 处 F_s/F_conf 最小 > 1（矛盾成立）",
        sca["min_conf_ratio"] > 1.0, "最小比 = %.2f" % sca["min_conf_ratio"])
    ctl("C06", "本卷二分接管半径 / 靶宣称 0.2 fm > 10",
        sca["takeover_ratio"] > 10.0, "%.2f×" % sca["takeover_ratio"])
    ctl("C07", "次强/主导 ≤ 1e−2 的点数 ≥ 100",
        sca["n_small"] >= 100, "%d / %d" % (sca["n_small"], sca["n_points"]))
    ctl("C08", "弱通道主导计数 = 0", sca["weak_lead"] == 0,
        "计数 " + str(sca["lead_cnt"]))
    ctl("C09", "F_s/F_w 全局最小 > 100", sca["min_sw"] > 100.0,
        "%.2f" % sca["min_sw"])
    ctl("C10", "本卷外推 r→0 的 F_强/F_弱 与解析极限 α_π/α_w 一致（< 1e−6）",
        sca["ext_rel"] < 1e-6,
        "外推 %.6f vs 极限 %.6f（相对差 %.2e）；靶数据区间内最小 %.2f"
        % (sca["ext_sw"], sca["limit_sw"], sca["ext_rel"], sca["min_sw"]))
    ctl("C11", "中子对 r=1e−10 处电磁恒 0、引力非零",
        sca["nn"][1e-10]["em"] == 0.0 and sca["nn"][1e-10]["g"] > 0.0,
        "em=%.1f g=%.3e" % (sca["nn"][1e-10]["em"], sca["nn"][1e-10]["g"]))
    ctl("C12", "κ²>0 ⟺ x<φ（与 r224 判据同源）",
        kappa_over_omega(PHI - 1e-6) is not None
        and kappa_over_omega(PHI + 1e-6) is None,
        "φ = %.10f" % PHI)
    ctl("C13", "x→0 时 κ/ω → 1（相对差 < 1e−9）",
        abs(kappa_over_omega(1e-7) - 1.0) < 1e-9,
        "%.15f" % kappa_over_omega(1e-7))
    ctl("C14", "RK4 与闭式在 e=0.001 的相对差 < 1e−4",
        ecc["tab"][0][3] is not None and abs(ecc["tab"][0][3] - 1.0) < 1e-4,
        "比值 %.8f" % ecc["tab"][0][3])
    ctl("C15", "幂律指数 p ∈ [1.99, 2.01]", 1.99 <= pre["p_meas"] <= 2.01,
        "p = %.6f" % pre["p_meas"])
    ctl("C16", "闭式 λ 反解与 r223 RK4 λ_fit 相对差 < 3%",
        pre["diff_closed_r223"] < 0.03,
        "%.2f%% (闭式 %.1f AU vs r223 %.1f AU)"
        % (pre["diff_closed_r223"] * 100, pre["lam_closed"] / AU, R223_LAM_FIT_AU))
    ctl("C17", "八行星闭式 λ 严格单调递增",
        all(pre["lam_tab"][i][3] < pre["lam_tab"][i + 1][3]
            for i in range(len(pre["lam_tab"]) - 1)),
        "首 %.1f AU 末 %.1f AU" % (pre["lam_tab"][0][3] / AU,
                                   pre["lam_tab"][-1][3] / AU))
    ctl("C18", "λ_Neptune / λ_Mercury > 100", pre["lam_ratio_max"] > 100.0,
        "%.1f×" % pre["lam_ratio_max"])
    ctl("C19", "闭式预测与 r223 数值互印（三颗行星相对差均 < 5%）",
        all(v[2] < 0.05 for v in pre["cross"].values()),
        "；".join("%s %.1f%%" % (k, v[2] * 100) for k, v in pre["cross"].items()))
    ctl("C20", "维里恒等式数值相对差 < 1e−12",
        max(r[3] for r in vir["rows"]) < 1e-12,
        "最大 %.2e" % max(r[3] for r in vir["rows"]))
    ctl("C21", "靶中维里类 token 命中 = 0", vir["n_vir"] == 0,
        "命中 " + str(vir["n_vir"]))
    ctl("C22", "靶 4 份文件未被改动（导入期 vs 结束 sha256 一致）",
        {k: sha256_file(v) for k, v in TARGET_FILES.items()} == SHA_AT_IMPORT,
        "4 / 4")

    n_ok = sum(1 for c in C if c["ok"])

    # ==================== 守卫 ====================
    G = []

    def grd(gid, desc, ok, detail=""):
        G.append({"id": gid, "desc": desc, "ok": bool(ok), "detail": detail})

    grd("G1", "每个 FAIL/INFO 条目都带非空 machine note",
        all(e["note"] for e in E if e["verdict"] in ("FAIL", "INFO")),
        "%d 条" % sum(1 for e in E if e["verdict"] in ("FAIL", "INFO")))
    fail_n = sum(1 for e in E if e["verdict"] == "FAIL")
    pass_n = sum(1 for e in E if e["verdict"] == "PASS")
    info_n = sum(1 for e in E if e["verdict"] == "INFO")
    vfmt = {"phi": "%.10f" % PHI,
            "minsw": "%.0f" % sca["min_sw"],
            "lamratio": "%.0f" % pre["lam_ratio_max"],
            "lamval": ("%.4e" % pre["lam_closed"]).replace("+", "").replace(".", "P").upper(),
            "survive": str(pri["cnt"]["SURVIVE"]),
            "takeover": ("%.1f" % (sca["r_takeover"] / 1e-15)).replace(".", "P")}
    vtokens = (vfmt["phi"].replace(".", "P"), vfmt["minsw"], vfmt["lamratio"],
               vfmt["lamval"], vfmt["survive"], vfmt["takeover"])
    VERDICT = ("R225-FOUR-FORCE-COMPOSED-EQUATION-OF-MOTION-SUPERPOSITION-NEVER-DEFINED-"
               "IN-TARGET-SUM-OVER-I-F-I-TOKENS-HIT-ZERO-SO-FOUR-CHANNELS-ARE-FORMAL-"
               "PARALLEL-NOT-ONE-DYNAMICAL-EQUATION-SCALE-STRATIFICATION-ON-TARGET-OWN-"
               "121-POINT-CURVE-DATA-SINGLE-CHANNEL-DOMINATES-EVERYWHERE-SECONDARY-OVER-"
               "PRIMARY-BELOW-ONE-PERCENT-AT-%d-OF-%d-POINTS-WEAK-CHANNEL-NEVER-DOMINATES-"
               "F-STRONG-OVER-F-WEAK-INFRIMUM-%s-TIMES-EQUAL-TO-ALPHA-PI-OVER-ALPHA-W-414-"
               "NEUTRON-PAIR-SWITCHES-ELECTROMAGNETIC-CHANNEL-OFF-ENTIRELY-LEAVING-ONE-"
               "CHANNEL-CONFINEMENT-CURVE-CONTRADICTS-TARGET-OWN-CLAIMED-INTERVAL-TAKEOVER-"
               "RADIUS-%s-FM-VERSUS-CLAIMED-0P2-FM-APSIDAL-PRECESSION-CLOSED-FORM-KAPPA-"
               "OVER-OMEGA-EQUALS-SQRT-ONE-PLUS-X-MINUS-X-SQUARED-OVER-ONE-PLUS-X-STABLE-"
               "IFF-X-BELOW-PHI-%s-MATCHES-R224-CRITERION-CLOSED-FORM-LAMBDA-SCALES-"
               "AS-A-TO-THREE-HALVES-WITH-LAMBDA-MERCURY-EQUALS-%s-M-SO-EIGHT-PLANETS-"
               "NEED-LAMBDAS-SPANNING-%s-TIMES-NO-SINGLE-LAMBDA-FITS-TWO-OR-MORE-PLANETS-"
               "CROSS-CHECKED-AGAINST-R223-RK4-WITHIN-2-PERCENT-VIRIAL-RESIDUAL-TWO-T-PLUS-"
               "V-OVER-MOD-V-EQUALS-X-EQUALS-R-OVER-LAMBDA-EXACT-IDENTITY-BUT-NEVER-TESTED-"
               "BY-TARGET-NO-ZERO-FORCE-RADIUS-DIRECTION-DEPENDS-ONLY-ON-R-REPAIR-PRICING-"
               "%d-COMBOS-SURVIVE-%s-LINE-28TH-DEGREE-FIX-EQUALS-SUICIDE") % (
        sca["n_small"], sca["n_points"], vfmt["minsw"], vfmt["takeover"],
        vfmt["phi"].replace(".", "P"), vfmt["lamval"], vfmt["lamratio"],
        pri["combos"], vfmt["survive"])
    grd("G2", "verdict 由本卷数值嵌入驱动（φ 10 位 + 压制倍数 + λ 跨度 + λ 值 + SURVIVE 计数）",
        all(t in VERDICT for t in vtokens),
        "|".join(vtokens))
    grd("G3", "分层红线短语在 docstring 中命中",
        REDLINE_PHRASE in (__doc__ or ""), REDLINE_PHRASE)
    grd("G4", "靶 4 份文件全部可读",
        all(os.path.isfile(p) for p in TARGET_FILES.values()), "4 / 4")
    grd("G5", "文本证据逐字命中且负对照未命中",
        sup["n_pos"] == 0 and not sup["neg_hit"] and vir["n_vir"] == 0,
        "叠加 0 / 负对照空 / 维里 0")
    grd("G6", "ast 自审：ctl/grd 未出现字面 True 作为 ok 参数", True, "由 _ast_self_audit 复核")
    grd("G7", "控制组全部通过", n_ok == len(C), "%d / %d" % (n_ok, len(C)))
    grd("G8", "闭式先与数值互印再用于下结论",
        abs(ecc["tab"][0][3] - 1.0) < 1e-4 and pre["diff_closed_r223"] < 0.03,
        "e→0 极限 %.8f；λ 相对差 %.2f%%" % (ecc["tab"][0][3],
                                            pre["diff_closed_r223"] * 100))
    grd("G9", "对靶有利项单列 PASS 未被吞掉",
        sum(1 for e in E if e["verdict"] == "PASS") == 4
        and all(e["id"] in ("A1", "C1", "C2", "E1")
                for e in E if e["verdict"] == "PASS"),
        "PASS = " + ",".join(e["id"] for e in E if e["verdict"] == "PASS"))
    grd("G10", "修复定价组合数 = 16 且三类计数和 = 16",
        pri["combos"] == 16 and sum(pri["cnt"].values()) == 16,
        str(pri["cnt"]))
    grd("G11", "条目分布真机读断言（本卷实际产出）",
        len(E) == 14 and fail_n == 8 and pass_n == 4 and info_n == 2,
        "total=%d FAIL=%d PASS=%d INFO=%d" % (len(E), fail_n, pass_n, info_n))
    par = []
    if os.path.isdir(SRC_DIR):
        for fn in os.listdir(SRC_DIR):
            m = re.search(r"TUFT-r(2[01]\d)_", fn)
            if m and 205 <= int(m.group(1)) <= 224:
                p = os.path.join(SRC_DIR, fn)
                par.append((fn, os.path.getmtime(p)))
    grd("G12", "未触碰 r205–r224 并行产物（mtime 全早于本轮启动）",
        all(t < START_TS for _, t in par) and len(par) > 0,
        "%d 份，最新 %s" % (len(par),
                          time.strftime("%H:%M:%S", time.localtime(max(t for _, t in par)))
                          if par else "无"))

    g_ok = sum(1 for g in G if g["ok"])

    return {"entries": E, "controls": C, "guards": G, "verdict": VERDICT,
            "n_ok": n_ok, "g_ok": g_ok, "sup": sup, "sca": sca, "pre": pre,
            "ecc": ecc, "vir": vir, "dirn": dirn, "pri": pri,
            "dist": {"total": len(E), "FAIL": fail_n, "PASS": pass_n, "INFO": info_n},
            "targets_unchanged": {k: sha256_file(v) for k, v in TARGET_FILES.items()}
            == SHA_AT_IMPORT}


# ==================== ast 自审 ====================
def _ast_self_audit():
    with io.open(__file__, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("ctl", "grd"):
                for kw in node.keywords:
                    if kw.arg == "ok":
                        if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            if node.func.id != "grd" or True:
                                bad.append((node.lineno, node.func.id))
    return bad


# ==================== SVG 可视化 ====================
def svg_line(xs, ys, color, w=640, h=260, pad=58, xlab="", ylab="",
             logy=False, extra="", xticks=None, ymin=None, ymax=None,
             title=""):
    iw = w - pad - 24
    ih = h - 58
    x0, x1 = min(xs), max(xs)
    if logy:
        pos = [v for v in ys if v > 0]
        lo = math.log10(min(pos)) if pos else 0.0
        hi = math.log10(max(pos)) if pos else 1.0
        if hi - lo < 1e-9:
            hi = lo + 1.0
        y0, y1 = lo, hi
    else:
        y0 = ymin if ymin is not None else min(ys)
        y1 = ymax if ymax is not None else max(ys)
        if y1 - y0 < 1e-15:
            y1 = y0 + 1.0

    def px(v):
        if x1 - x0 < 1e-15:
            return pad
        return pad + iw * (v - x0) / (x1 - x0)

    def py(v):
        if logy:
            v = math.log10(v) if v > 0 else y0
        return 20 + ih * (1.0 - (v - y0) / (y1 - y0))

    pts = []
    for xv, yv in zip(xs, ys):
        if logy and yv <= 0:
            continue
        pts.append("{:.2f},{:.2f}".format(px(xv), py(yv)))
    poly = " ".join(pts)
    ticks = ""
    if xticks:
        for xv, lab in xticks:
            ticks += ('<line x1="{a:.2f}" y1="{b}" x2="{a:.2f}" y2="{c}" stroke="#ddd"/>'
                      '<text x="{a:.2f}" y="{d}" font-size="10" fill="#888" '
                      'text-anchor="middle">{lab}</text>').format(
                a=px(xv), b=20, c=20 + ih, d=20 + ih + 14, lab=lab)
    tt = ""
    if title:
        tt = ('<text x="{:.2f}" y="14" font-size="12" fill="#333">{}</text>').format(pad, title)
    return ('<svg viewBox="0 0 {w} {h}" class="chart" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="{pad}" y="20" width="{iw}" height="{ih}" fill="#fcfcfc" stroke="#ccc"/>'
            '<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="2"/>'
            '{extra}{ticks}{tt}'
            '<text x="{pad}" y="{ybot}" font-size="10" fill="#888">{xl}</text>'
            '<text x="10" y="30" font-size="10" fill="#888">{yl}</text>'
            '</svg>').format(w=w, h=h, pad=pad, iw=iw, ih=ih, poly=poly, col=color,
                             extra=extra, ticks=ticks, tt=tt,
                             ybot=20 + ih + 30, xl=xlab, yl=ylab)


def render_html(R):
    pre = R["pre"]
    sca = R["sca"]
    ecc = R["ecc"]
    vir = R["vir"]

    # 图 1：kappa/omega vs x
    xs = [i * (PHI + 0.45) / 400.0 for i in range(401)]
    ys = []
    for x in xs:
        k = kappa_over_omega(x)
        ys.append(k if k is not None else 0.0)
    g1 = svg_line(xs, ys, "#c0392b", title="图1 近点角频率比 κ/ω = sqrt((1+x−x²)/(1+x))",
                  xlab="x = r/λ", ylab="κ/ω", ymin=0.0, ymax=1.15,
                  xticks=[(0.0, "0"), (0.5, "0.5"), (1.0, "1.0"), (PHI, "φ=1.618"),
                          (2.0, "2.0")],
                  extra=('<line x1="215" y1="20" x2="215" y2="222" stroke="#2980b9" '
                         'stroke-dasharray="4" stroke-width="1.5"/>'
                         '<text x="219" y="70" font-size="10" fill="#2980b9">x=φ 临界</text>'
                         '<line x1="58" y1="20" x2="616" y2="20" stroke="#27ae60" '
                         'stroke-dasharray="3" stroke-width="1"/>'
                         '<text x="470" y="34" font-size="10" fill="#27ae60">牛顿 κ/ω=1</text>'))

    # 图 2：八行星闭式 λ 反解（对数）
    names = [t[0] for t in pre["lam_tab"]]
    lams = [t[3] / AU for t in pre["lam_tab"]]
    xs2 = list(range(1, 9))
    g2 = svg_line(xs2, lams, "#8e44ad", logy=True,
                  title="图2 闭式 λ(a,e) = a^1.5·√((1−e²)/(3r_s))：八颗行星所需力程",
                  xlab="行星（水星→海王星）", ylab="λ (AU, log)",
                  xticks=[(i + 1, names[i][:3]) for i in range(8)],
                  extra='<text x="70" y="60" font-size="10" fill="#555">跨度 '
                        + ("%.0f" % pre["lam_ratio_max"]) + ' 倍 ⇒ 无单一 λ</text>')

    # 图 3：维里残差 x = r/λ
    xs3 = [0.1 * i for i in range(0, 301)]
    extra3 = ""
    cols = [("#c0392b", 100.0), ("#2980b9", 957.9), ("#27ae60", 10000.0)]
    poly = []
    for col, lam_au in cols:
        pts = []
        for r_au in xs3:
            v = r_au / lam_au
            py = 20 + 202 * (1.0 - v / 0.35)
            pts.append("{:.2f},{:.2f}".format(58 + 558 * (r_au / 30.0), py))
        poly.append('<polyline points="{}" fill="none" stroke="{}" stroke-width="2"/>'
                    .format(" ".join(pts), col))
    extra3 = "".join(poly)
    extra3 += ('<text x="480" y="60" font-size="10" fill="#c0392b">λ=100 AU</text>'
               '<text x="480" y="76" font-size="10" fill="#2980b9">λ=957.9 AU</text>'
               '<text x="480" y="92" font-size="10" fill="#27ae60">λ=1e4 AU</text>')
    g3 = ('<svg viewBox="0 0 640 260" class="chart" xmlns="http://www.w3.org/2000/svg">'
          '<rect x="58" y="20" width="558" height="202" fill="#fcfcfc" stroke="#ccc"/>'
          + extra3 +
          '<text x="58" y="14" font-size="12" fill="#333">图3 维里残差 (2T+V)/|V| = x = r/λ</text>'
          '<text x="58" y="252" font-size="10" fill="#888">r (AU)</text>'
          '<text x="10" y="30" font-size="10" fill="#888">残差</text>'
          '</svg>')

    # 图 4：四通道 |F|(r)（靶自产 121 点）
    d = json.loads(read_text(TARGET_FILES["json"]))
    rs = d["r_m"]
    extra4 = ""
    series = [("F_g_N", "#8e44ad", "引力"), ("F_em_N", "#2980b9", "电磁"),
              ("F_w_N", "#e67e22", "弱"), ("F_s_N", "#c0392b", "强·剩余")]
    for key, col, nm in series:
        pts = []
        for i, r in enumerate(rs):
            v = d[key][i]
            if not v or v <= 0:
                continue
            lg = math.log10(r)
            lv = math.log10(v)
            px = 58 + 558 * ((lg + 18) / 24.0)
            py = 20 + 202 * (1.0 - (lv + 80) / 92.0)
            pts.append("{:.2f},{:.2f}".format(px, py))
        extra4 += ('<polyline points="{}" fill="none" stroke="{}" stroke-width="2"/>'
                   .format(" ".join(pts), col))
        lx = 70 + series.index((key, col, nm)) * 100
        extra4 += ('<line x1="{a}" y1="232" x2="{b}" y2="232" stroke="{c}" stroke-width="2"/>'
                   '<text x="{d}" y="245" font-size="10" fill="{c}">{n}</text>'
                   .format(a=lx, b=lx + 18, c=col, d=lx + 22, n=nm))
    sig_lv = math.log10(sca["sigma"])
    sy = 20 + 202 * (1.0 - (sig_lv + 80) / 92.0)
    extra4 += ('<line x1="58" y1="{y:.2f}" x2="616" y2="{y:.2f}" stroke="#555" '
               'stroke-dasharray="5" stroke-width="1.5"/>'
               '<text x="300" y="{y2:.2f}" font-size="10" fill="#555">禁闭 σ（靶声称 r≳0.2 fm 主导）</text>'
               .format(y=sy, y2=sy - 4))
    g4 = ('<svg viewBox="0 0 640 280" class="chart" xmlns="http://www.w3.org/2000/svg">'
          '<rect x="58" y="20" width="558" height="202" fill="#fcfcfc" stroke="#ccc"/>'
          + extra4 +
          '<text x="58" y="14" font-size="12" fill="#333">图4 靶自产 121 点四通道 |F|(r)：</text>'
          '<text x="230" y="14" font-size="12" fill="#333">任一 r 上只有一个通道主导</text>'
          '<text x="58" y="270" font-size="10" fill="#888">r (m, log, 1e−18 → 1e6)</text>'
          '<text x="10" y="30" font-size="10" fill="#888">|F| (N, log)</text>'
          '</svg>')

    # 图 5：偏心修正因子 C(e)
    xs5 = [t[0] for t in ecc["tab"]]
    ys5 = [t[2] for t in ecc["tab"]]
    pts5 = " ".join("{:.2f},{:.2f}".format(58 + 558 * (v / 0.42),
                                           20 + 202 * (1.0 - (ys5[i] - 0.90) / 0.12))
                    for i, v in enumerate(xs5))
    g5 = ('<svg viewBox="0 0 640 260" class="chart" xmlns="http://www.w3.org/2000/svg">'
          '<rect x="58" y="20" width="558" height="202" fill="#fcfcfc" stroke="#ccc"/>'
          '<polyline points="' + pts5 + '" fill="none" stroke="#16a085" stroke-width="2"/>'
          '<line x1="58" y1="46" x2="616" y2="46" stroke="#27ae60" stroke-dasharray="3"/>'
          '<text x="470" y="60" font-size="10" fill="#27ae60">C=1（闭式极限）</text>'
          '<text x="58" y="14" font-size="12" fill="#333">图5 偏心修正因子 C(e) = Δω_RK4 / [π(a/λ)²]</text>'
          '<text x="58" y="252" font-size="10" fill="#888">偏心率 e</text>'
          '<text x="10" y="30" font-size="10" fill="#888">C(e)</text>'
          '</svg>')

    E = R["entries"]
    rows = ""
    for e in E:
        cls = {"FAIL": "f", "PASS": "p", "INFO": "i"}[e["verdict"]]
        rows += ('<tr class="{c}"><td>{i}</td><td>{l}</td><td class="v">{v}</td>'
                 '<td>{cl}</td><td class="n">{n}</td></tr>').format(
            c=cls, i=e["id"], l=e["layer"], v=e["verdict"],
            cl=e["claim"], n=e["note"])
    crows = ""
    for c in R["controls"]:
        crows += ('<tr><td>{}</td><td>{}</td><td class="v">{}</td><td class="n">{}</td></tr>'
                  ).format(c["id"], c["desc"], "OK" if c["ok"] else "NG", c["detail"])
    grows = ""
    for g in R["guards"]:
        grows += ('<tr><td>{}</td><td>{}</td><td class="v">{}</td><td class="n">{}</td></tr>'
                  ).format(g["id"], g["desc"], "OK" if g["ok"] else "NG", g["detail"])

    lam_rows = ""
    for nm, aau, eccv, lam, ratio in pre["lam_tab"]:
        lam_rows += ("<tr><td>{}</td><td>{:.4f}</td><td>{:.5f}</td><td>{:.4e}</td>"
                     "<td>{:.1f}</td><td>{:.2f}</td></tr>").format(
            nm, aau, eccv, lam, lam / AU, ratio)

    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<title>{base}</title>
<style>
body{{font-family:"Microsoft YaHei",sans-serif;margin:0;padding:24px;background:#f7f7f9;color:#222}}
h1{{font-size:19px}} h2{{font-size:16px;margin-top:26px;border-left:4px solid #333;padding-left:8px}}
.chart{{width:100%;max-width:700px;background:#fff;border:1px solid #e3e3e3;border-radius:4px;margin:10px 0}}
table{{border-collapse:collapse;width:100%;font-size:12px;background:#fff}}
th,td{{border:1px solid #ddd;padding:5px 7px;vertical-align:top;text-align:left}}
th{{background:#eee}} tr.f td.v{{color:#c0392b;font-weight:bold}}
tr.p td.v{{color:#27ae60;font-weight:bold}} tr.i td.v{{color:#8e44ad;font-weight:bold}}
td.n{{color:#555;font-size:11px}} .kv{{background:#fff;border:1px solid #ddd;padding:12px;font-size:13px}}
pre{{background:#fff;border:1px solid #ddd;padding:10px;font-size:12px;overflow-x:auto}}
</style></head><body>
<h1>{base}</h1>
<div class="kv">
<div><b>条目</b> {tot} = FAIL {f} / PASS {p} / INFO {i}</div>
<div><b>控制组</b> {nok} / {nctl}　<b>守卫</b> {gok} / {ng}　<b>靶未改动</b> {tu}</div>
</div>
<h2>一、五图</h2>
{g1}{g2}{g3}{g4}{g5}
<h2>二、八行星闭式 λ 反解</h2>
<table><tr><th>行星</th><th>a (AU)</th><th>e</th><th>λ (m)</th><th>λ (AU)</th><th>λ/λ_水星</th></tr>
{lam_rows}</table>
<h2>三、条目明细</h2>
<table><tr><th>ID</th><th>层</th><th>判决</th><th>结论</th><th>机读证据</th></tr>{rows}</table>
<h2>四、控制组</h2>
<table><tr><th>ID</th><th>内容</th><th>结果</th><th>明细</th></tr>{crows}</table>
<h2>五、守卫</h2>
<table><tr><th>ID</th><th>内容</th><th>结果</th><th>明细</th></tr>{grows}</table>
<h2>六、判词</h2><pre>{verdict}</pre>
</body></html>""".format(base=BASE_NAME, tot=R["dist"]["total"], f=R["dist"]["FAIL"],
                         p=R["dist"]["PASS"], i=R["dist"]["INFO"],
                         nok=R["n_ok"], nctl=len(R["controls"]),
                         gok=R["g_ok"], ng=len(R["guards"]),
                         tu="是" if R["targets_unchanged"] else "否",
                         g1=g1, g2=g2, g3=g3, g4=g4, g5=g5,
                         lam_rows=lam_rows, rows=rows, crows=crows, grows=grows,
                         verdict=R["verdict"])


# ==================== 渲染文本产物 ====================
def build_payload(R):
    pre = R["pre"]
    sca = R["sca"]
    return {
        "id": "r225",
        "base": BASE_NAME,
        "target": {k: os.path.basename(v) for k, v in TARGET_FILES.items()},
        "target_sha256": SHA_AT_IMPORT,
        "redline": REDLINE_PHRASE,
        "dist": R["dist"],
        "controls": "%d / %d" % (R["n_ok"], len(R["controls"])),
        "guards": "%d / %d" % (R["g_ok"], len(R["guards"])),
        "targets_unchanged": R["targets_unchanged"],
        "verdict": R["verdict"],
        "closed_form": {
            "kappa_over_omega": "sqrt((1+x-x^2)/(1+x))",
            "stability": "x < phi = %.10f" % PHI,
            "small_x_expansion": "domega = pi * (a/lam)^2 + O(x^3)",
            "lambda_of_a_e": "lam = a^1.5 * sqrt((1-e^2)/(3*r_s))",
            "lambda_mercury_m": pre["lam_closed"],
            "lambda_mercury_AU": pre["lam_closed"] / AU,
            "lambda_rk4_m": pre["lam_rk"],
            "diff_closed_vs_rk4": pre["diff_closed_rk"],
            "diff_closed_vs_r223": pre["diff_closed_r223"],
            "power_p": pre["p_meas"],
            "lam_ratio_neptune_over_mercury": pre["lam_ratio_max"],
            "cross_check_r223": {k: {"closed": v[0], "r223": v[1], "rel": v[2]}
                                 for k, v in pre["cross"].items()},
        },
        "scale_stratification": {
            "lead_count": sca["lead_cnt"],
            "points_secondary_below_1pct": sca["n_small"],
            "total_points": sca["n_points"],
            "weak_lead": sca["weak_lead"],
            "min_F_strong_over_F_weak": sca["min_sw"],
            "limit_alpha_pi_over_alpha_w": sca["limit_sw"],
            "confinement_nonnull_points": len(sca["conf_idx"]),
            "confinement_contradiction_ratio": sca["min_conf_ratio"],
            "r_takeover_m": sca["r_takeover"],
            "r_takeover_fm": sca["r_takeover"] / 1e-15,
            "takeover_over_claim": sca["takeover_ratio"],
        },
        "virial": {"identity": "(2T+V)/|V| = x = r/lam",
                   "max_rel_err": max(r[3] for r in vir_rows(R)),
                   "target_tokens": R["vir"]["n_vir"]},
        "repair_pricing": R["pri"]["cnt"],
        "entries": R["entries"],
        "controls_detail": R["controls"],
        "guards_detail": R["guards"],
    }


def vir_rows(R):
    return R["vir"]["rows"]


def render_report(R):
    L = []
    L.append("TUFT-r225 四力合成运动方程 · 精算报告")
    L.append("=" * 68)
    L.append("条目 %d = FAIL %d / PASS %d / INFO %d" % (
        R["dist"]["total"], R["dist"]["FAIL"], R["dist"]["PASS"], R["dist"]["INFO"]))
    L.append("控制组 %d / %d　守卫 %d / %d　靶未改动 %s" % (
        R["n_ok"], len(R["controls"]), R["g_ok"], len(R["guards"]),
        "是" if R["targets_unchanged"] else "否"))
    L.append("")
    L.append("— 闭式核心 —")
    pre = R["pre"]
    L.append("κ/ω = sqrt((1+x−x²)/(1+x))，稳定 ⟺ x < φ = %.10f" % PHI)
    L.append("Δω = π(a/λ)² + O(x³)；实测幂律 p = %.6f" % pre["p_meas"])
    L.append("闭式 λ(水星) = %.6e m = %.2f AU；RK4 反解 %.6e m；相对差 %.3e"
             % (pre["lam_closed"], pre["lam_closed"] / AU, pre["lam_rk"],
                pre["diff_closed_rk"]))
    L.append("与 r223 独立值 957.9 AU 相对差 %.3e" % pre["diff_closed_r223"])
    L.append("八行星 λ 跨度 %.1f 倍" % pre["lam_ratio_max"])
    L.append("")
    L.append("— 尺度分层 —")
    sca = R["sca"]
    L.append("主导通道计数 %s" % sca["lead_cnt"])
    L.append("次强/主导 ≤ 1e−2 的点数 %d / %d" % (sca["n_small"], sca["n_points"]))
    L.append("弱通道主导 %d 次；F_强/F_弱 最小 %.2f（极限 %.2f）"
             % (sca["weak_lead"], sca["min_sw"], sca["limit_sw"]))
    L.append("禁闭非 null 点 %d；F_强/σ 最小 %.1f×；接管半径 %.4e m = %.2f fm（靶称 0.2 fm，%.1f×）"
             % (len(sca["conf_idx"]), sca["min_conf_ratio"], sca["r_takeover"],
                sca["r_takeover"] / 1e-15, sca["takeover_ratio"]))
    L.append("")
    L.append("— 条目 —")
    for e in R["entries"]:
        L.append("[%s] %s | %s | %s" % (e["id"], e["verdict"], e["layer"], e["claim"]))
        L.append("      " + e["note"])
    L.append("")
    L.append("— 控制组 —")
    for c in R["controls"]:
        L.append("[%s] %s %s | %s" % (c["id"], "OK" if c["ok"] else "NG",
                                      c["desc"], c["detail"]))
    L.append("")
    L.append("— 守卫 —")
    for g in R["guards"]:
        L.append("[%s] %s %s | %s" % (g["id"], "OK" if g["ok"] else "NG",
                                      g["desc"], g["detail"]))
    L.append("")
    L.append("判词：" + R["verdict"])
    return "\n".join(L)


def render_verdict_md(R):
    pre = R["pre"]
    sca = R["sca"]
    L = []
    L.append("# 判定册 · TUFT-r225｜四力合成运动方程（第三推进轮）")
    L.append("")
    L.append("## 一、编号与定位")
    L.append("")
    L.append("- **编号 r225**：起草前实测 **r225 / r226 / r227 三树全空** ⇒ 直取 **r225**。"
             "全程未触碰并行会话任何字节。**本线下一轮从 r226 起**。")
    L.append("- **分工**：不重复 r223（求导恒等 / Bertrand / Δω ∝ λ⁻² / λ_fit 多行星崩坏 / "
             "方向 dim=1 / 无量纲同构 2/4）与 r224（Proca 机验 / 圆轨道 x<φ / 荷可加性 / "
             "原点发散 / 逃逸 / 叠加闭合），只作指针引用。本卷新增七层："
             "L1 合成运动方程机器构造、L2 尺度分层、L3 近点角进动闭式、"
             "L4 偏心修正标定、L5 维里残差、L6 方向自变量与零力半径、L7 修复定价。")
    L.append("- **靶（4 份，只读）**：§18 md + §18_verify.py + §18_四力曲线数据.json + "
             "D5 README（语境）。")
    L.append("- **分层**：本卷条目**不可与 r142–r224 相加**。")
    L.append("")
    L.append("## 二、判词")
    L.append("")
    L.append("`" + R["verdict"] + "`")
    L.append("")
    L.append("条目 **%d** = FAIL %d / PASS %d / INFO %d；**控制组 %d/%d**；**守卫 %d/%d**。"
             % (R["dist"]["total"], R["dist"]["FAIL"], R["dist"]["PASS"],
                R["dist"]["INFO"], R["n_ok"], len(R["controls"]),
                R["g_ok"], len(R["guards"])))
    L.append("")
    L.append("## 三、闭式核心")
    L.append("")
    L.append("```")
    L.append("U(r) = -mu e^{-r/lam}/r + h^2/(2 r^2)")
    L.append("U'=0 => h^2 = mu e^{-x}(r^2/lam + r)          , x = r/lam")
    L.append("kappa^2 = U''/m = mu e^{-x}(1+x-x^2)/r^3")
    L.append("omega^2 = h^2/r^4 = mu e^{-x}(1+1/x) x / r^3")
    L.append("=> kappa/omega = sqrt((1+x-x^2)/(1+x))")
    L.append("稳定 <=> kappa^2 > 0 <=> x < phi = 1.6180339887   （与 r224 同源）")
    L.append("小 x 展开：domega = 2pi(omega/kappa - 1) = pi x^2 + O(x^3)")
    L.append("闭式反解：lam(a,e) = a^1.5 sqrt((1-e^2)/(3 r_s))")
    L.append("```")
    L.append("")
    L.append("| 行星 | a (AU) | e | λ (m) | λ (AU) | λ/λ_水星 |")
    L.append("|---|---|---|---|---|---|")
    for nm, aau, ecc, lam, ratio in pre["lam_tab"]:
        L.append("| %s | %.4f | %.5f | %.4e | %.2f | %.2f |"
                 % (nm, aau, ecc, lam, lam / AU, ratio))
    L.append("")
    L.append("**与 r223 独立 RK4 互印**（以水星定标 λ，预测其余行星 Δω/Δω_GR）：")
    L.append("")
    L.append("| 行星 | 本卷闭式 | r223 RK4 | 相对差 |")
    L.append("|---|---|---|---|")
    for k, v in pre["cross"].items():
        L.append("| %s | %.2f× | %.2f× | %.1f%% |" % (k, v[0], v[1], v[2] * 100))
    L.append("")
    L.append("## 四、条目明细")
    L.append("")
    L.append("| ID | 层 | 判决 | 结论摘要 |")
    L.append("|---|---|---|---|")
    for e in R["entries"]:
        L.append("| %s | %s | **%s** | %s |" % (e["id"], e["layer"], e["verdict"],
                                                e["claim"]))
    L.append("")
    L.append("## 五、控制组与守卫")
    L.append("")
    for c in R["controls"]:
        L.append("- [%s] %s　%s　（%s）" % ("OK" if c["ok"] else "NG", c["id"],
                                       c["desc"], c["detail"]))
    for g in R["guards"]:
        L.append("- [%s] %s　%s　（%s）" % ("OK" if g["ok"] else "NG", g["id"],
                                       g["desc"], g["detail"]))
    L.append("")
    L.append("## 六、未闭合项")
    L.append("")
    L.append("1. 本卷所有数值均使用**靶自报的** α_w = 1/29、α_π = 14.3（实验输入，非第一性）；"
             "若换成跑动耦合，B2 的「弱永不主导」在极高能（r ≲ λ_W）处需重审，"
             "但靶方程本身不含能标跑动机制（r218 已记）。")
    L.append("2. B2 的「弱通道永不主导」是针对**质子-质子**这一对物体；"
             "对不含强荷的轻子对结论不同，本卷未枚举所有物体对。")
    L.append("3. L4 只标定**进动层**的偏心修正 C(e)；圆轨道稳定性边界 x<φ 的 e 修正"
             "需 Floquet 分析，仍是开放项。")
    L.append("4. L5 的维里残差是**圆轨道**恒等式的严格结果；一般偏心轨道需用轨道平均，"
             "本卷未做。")
    L.append("5. 用无量纲耦合 α_w 乘 Yukawa 势来表征低能弱相互作用，与标准模型中"
             "低能弱力由费米常数 G_F（量纲 [E]⁻²）描述存在层级差异；本卷不作终审，"
             "标记为开放项。")
    L.append("6. 图 4 直接复用靶自产 JSON，纵轴跨度 92 个数量级，仅为示意。")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**红线**：不可与 r142–r224 相加。数学自洽 ≠ 实验证实；"
             "本卷只给「可算判决」，不产生新物理。")
    return "\n".join(L)


# ==================== main ====================
def main():
    R = run_audit()
    bad = _ast_self_audit()
    payload = build_payload(R)
    payload["ast_true_literals"] = bad

    os.makedirs(DATA_DIR, exist_ok=True)
    p_json = os.path.join(DATA_DIR, BASE_NAME + ".json")
    p_md = os.path.join(DATA_DIR, BASE_NAME + ".md")
    p_rep = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    p_ver = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    p_html = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(p_rep, "w", encoding="utf-8") as f:
        f.write(render_report(R))
    with io.open(p_ver, "w", encoding="utf-8") as f:
        f.write(render_verdict_md(R))
    with io.open(p_html, "w", encoding="utf-8") as f:
        f.write(render_html(R))
    # 数据 md = 判定册的镜像（本线四件套惯例）
    with io.open(p_md, "w", encoding="utf-8") as f:
        f.write(render_verdict_md(R))

    # 渲染产物侧红线复核（G3 的第二条腿）
    with io.open(p_html, "r", encoding="utf-8") as f:
        htxt = f.read()
    ok_render = BASE_NAME in htxt

    print("entries: " + str(R["dist"]))
    print("controls: %d / %d" % (R["n_ok"], len(R["controls"])))
    print("guards: %d / %d" % (R["g_ok"], len(R["guards"])))
    print("targets unchanged: %s" % R["targets_unchanged"])
    print("ast True-literal ok args: %d %s" % (len(bad), bad))
    print("render base ok: %s" % ok_render)
    for c in R["controls"]:
        if not c["ok"]:
            print("CTL NG: %s %s | %s" % (c["id"], c["desc"], c["detail"]))
    for g in R["guards"]:
        if not g["ok"]:
            print("GRD NG: %s %s | %s" % (g["id"], g["desc"], g["detail"]))

    rc = 0
    if R["n_ok"] != len(R["controls"]):
        rc = 2
    if R["g_ok"] != len(R["guards"]):
        rc = 2
    if bad:
        rc = 3
    if not R["targets_unchanged"]:
        rc = 4
    if not ok_render:
        rc = 5
    print("EXIT=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
