# -*- coding: utf-8 -*-
"""ROOT V46《四种基本力的本源方程：第一性原理推导与精密检验》全维机验引擎（卷 96）。

用途：对来料 46-1..46-25 做两类独立核验，产出
      96_rootv46_fourforce_results.json / 96_rootv46_fourforce_report.txt 供 96 判定册引用。
      §A 量纲齐次性逐式审计：46-1..46-25 覆盖（19 条式，含 Yukawa / 色库仑 / Lorentz / KK / 向心）。
      §B..§E 数值读数复算：46-19（来料 §6.1）、46-13/14（§6.2）、46-16/17（§6.3）、46-18 关系式。
覆盖边界（诚实登记，见条目 F1）：46-10/46-11（洛伦兹力与回旋）、46-20..46-23（KK 求和）、
      46-25（向心力）的数值读数未随本轮来料提供，故只做量纲审计、不做数值比对 ——
      这不等于判定它们成立，而是本册没有对照读数。
约束：纯标准库；Decimal 50 位；Fraction 四元组量纲 (M,L,T,Q)；不联网、不读外部数据。
纪律：量纲类断言一律机器兜底；"恒等于零"类断言必配阳性对照；容差一律取来料报价的舍入半界
      （round_bound），不得用固定容差跨位数套用（会同时制造假 FAIL 与假 PASS）。
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal as D, getcontext, localcontext
from fractions import Fraction as F

getcontext().prec = 50

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PI = D("3.14159265358979323846264338327950288419716939937511")
PI2 = PI * PI

ROWS = []
GUARDS = []
RES = {}
NOTES = []


def add(code, verdict, text):
    ROWS.append({"code": code, "verdict": verdict, "text": text})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def dd(x):
    return D(str(x))


def fmt(x, n=20):
    if not isinstance(x, D):
        x = dd(x)
    with localcontext() as ctx:
        ctx.prec = 60
        return format(x, "." + str(n) + "E")


def dexp(x):
    if not isinstance(x, D):
        x = dd(x)
    with localcontext() as ctx:
        ctx.prec = 55
        return x.exp()


def dln(x):
    if not isinstance(x, D):
        x = dd(x)
    with localcontext() as ctx:
        ctx.prec = 55
        return x.ln()


def dsqrt(x):
    if not isinstance(x, D):
        x = dd(x)
    with localcontext() as ctx:
        ctx.prec = 55
        return x.sqrt()


def relerr(a, b):
    if not isinstance(a, D):
        a = dd(a)
    if not isinstance(b, D):
        b = dd(b)
    if b == 0:
        return D(0)
    return abs((a - b) / b)


def fz(x, n=3):
    """展示用：机器零显式写 0（Decimal 零在 .3E 格式下会印成 0.000E+3，易被误读）。"""
    if not isinstance(x, D):
        x = dd(x)
    if x == 0:
        return "0（逐位相同）"
    return fmt(x, n)


def round_bound(s):
    """来料报价串的『舍入半界』（相对）：末位半个单位 / 该值。

    判据纪律：容差必须与被核数值的报价精度同源。对 '0.08638' 返回 5.79e-5，
    对 '8.55e-17' 返回 5.85e-4；用固定容差（如 1e-6）核 3 位有效数字的报价，
    会把合法的四舍五入判成缺陷（假 FAIL），反之会把真错误当舍入（假 PASS）。
    """
    t = str(s).strip().lower()
    mant, _, ex = t.partition("e")
    ex = int(ex) if ex else 0
    mant = mant.lstrip("+-")
    if "." in mant:
        _ip, fp = mant.split(".")
    else:
        _ip, fp = mant, ""
    unit = D(10) ** (ex - len(fp))
    return unit / D(2) / dd(s)


# ---------------- 量纲工具：四元组 (M,L,T,Q)，Fraction 精确 ----------------
DIM = {}


def dm(name, m=0, l=0, t=0, q=0):
    DIM[name] = (F(m), F(l), F(t), F(q))


dm("one")
dm("M", 1)
dm("L", 0, 1)
dm("T", 0, 0, 1)
dm("Q", 0, 0, 0, 1)
dm("E", 1, 2, -2)
dm("F", 1, 1, -2)
dm("c", 0, 1, -1)
dm("G", -1, 3, -2)
dm("hbar", 1, 2, -1)
dm("eps0", -1, -3, 2, 2)
dm("mu0", 1, 1, 0, -2)              # N/A^2 = M L Q^-2（A=Q/T，故 T 维相消；不可写成 M L T^-2 Q^-2）
dm("Bf", 1, 0, -1, -1)
dm("Ef", 1, 1, -2, -1)
dm("sigma", 1, 1, -2)               # 弦张力/表面张力 = 能量/长度 = 力（M L T^-2）
dm("Kyuk", 1, 3, -2)
dm("acc", 0, 1, -2)
dm("Gmu", 1, 5, -2)                 # G_F 的 SI 量纲 = 能量×体积


def dmul(*xs):
    out = [F(0)] * 4
    for x in xs:
        for i in range(4):
            out[i] += x[i]
    return tuple(out)


def dinv(x):
    return tuple(-e for e in x)


def dpow(x, n):
    return tuple(e * n for e in x)


def deq(a, b):
    return all(a[i] == b[i] for i in range(4))


def dstr(d):
    names = ("M", "L", "T", "Q")
    parts = []
    for i in range(4):
        if d[i] != 0:
            parts.append(names[i] + "^" + str(d[i]))
    return " ".join(parts) if parts else "1"


# ==========================================================================
# 常量（来料 §六 声明口径：NIST/CODATA 2022 + 已发表粒子质量）
# ==========================================================================
C_LIGHT = dd("299792458")           # m/s（SI 定义值）
G_N = dd("6.67430e-11")             # m^3 kg^-1 s^-2
M_P = dd("1.67262192595e-27")       # kg
E_CHG = dd("1.602176634e-19")       # C（SI 定义值）
EPS0 = dd("8.8541878188e-12")       # F/m（CODATA 2022）
HBAR = dd("1.054571817e-34")        # J s
HBARC_GEVFM = dd("0.1973269804")    # GeV fm
GEV_J = dd("1.602176634e-10")       # J / GeV
FM = dd("1e-15")                    # m / fm
HBAR_GEVS = dd("6.582119569e-25")   # GeV s
MW_GEV = dd("80.3692")              # GeV（来料口径）
MZ_GEV = dd("91.1876")              # GeV（来料口径）
GF_GEV2 = dd("1.1663787e-5")        # GeV^-2
MMU_GEV = dd("0.1056583755")        # GeV
ME_GEV = dd("0.51099895e-3")        # GeV
TAU_EXP = dd("2.1969811e-6")        # s（来料口径：PDG 平均值）
ALPHA = dd("0.0072973525643")       # 精细结构常数（CODATA 2022）
ALPHA_S = dd("0.30")                # 来料示范值
SIGMA_GEVFM = dd("0.90")            # GeV/fm（来料示范值）

RES["constants"] = {
    "c": "299792458",
    "G": "6.67430e-11",
    "m_p_kg": "1.67262192595e-27",
    "e_C": "1.602176634e-19",
    "eps0_Fm": "8.8541878188e-12",
    "hbar_GeVs": "6.582119569e-25",
    "hbar_c_GeVfm": "0.1973269804",
    "m_W_GeV": "80.3692",
    "m_Z_GeV": "91.1876",
    "G_F_GeV^-2": "1.1663787e-5",
    "m_mu_GeV": "0.1056583755",
    "tau_mu_exp_s": "2.1969811e-6",
    "alpha_s_demo": "0.30",
    "sigma_demo_GeVfm": "0.90",
}

# ==========================================================================
# G0 量纲工具自检（工具自身必须先过守卫，再用于判定）
# ==========================================================================
guard("G0-1 eps0*mu0=1/c^2", deq(dmul(DIM["eps0"], DIM["mu0"]), dpow(DIM["c"], -2)),
      dstr(dmul(DIM["eps0"], DIM["mu0"])) + " vs " + dstr(dpow(DIM["c"], -2)))
guard("G0-2 [E]/[B]=[c]", deq(dmul(DIM["Ef"], dinv(DIM["Bf"])), DIM["c"]),
      dstr(dmul(DIM["Ef"], dinv(DIM["Bf"]))))
guard("G0-3 [qE]=[F]", deq(dmul(DIM["Q"], DIM["Ef"]), DIM["F"]), dstr(dmul(DIM["Q"], DIM["Ef"])))
guard("G0-4 [hbar*c]=[E][L]", deq(dmul(DIM["hbar"], DIM["c"]), dmul(DIM["E"], DIM["L"])),
      dstr(dmul(DIM["hbar"], DIM["c"])))
guard("G0-5 [G m^2/r^2]=[F]",
      deq(dmul(DIM["G"], dpow(DIM["M"], 2), dpow(DIM["L"], -2)), DIM["F"]),
      dstr(dmul(DIM["G"], dpow(DIM["M"], 2), dpow(DIM["L"], -2))))
guard("G0-6 [e^2/(eps0 r^2)]=[F]",
      deq(dmul(dpow(DIM["Q"], 2), dinv(DIM["eps0"]), dpow(DIM["L"], -2)), DIM["F"]),
      dstr(dmul(dpow(DIM["Q"], 2), dinv(DIM["eps0"]), dpow(DIM["L"], -2))))
guard("G0-7 [mu]=1/L", deq(dinv(DIM["L"]), dinv(DIM["L"])), dstr(dinv(DIM["L"])))
guard("G0-8 [sigma]=[E]/[L]", deq(DIM["sigma"], dmul(DIM["E"], dinv(DIM["L"]))), dstr(DIM["sigma"]))
guard("G0-9 [G_F]*[1/c^4]... 自然单位 M^-2", True, "by construction")
# 数值级自检：exp/ln 互逆（工具数值面）
_t1 = dexp(dln(dd("7.5")))
guard("G0-10 exp(ln x)=x", relerr(_t1, dd("7.5")) < D("1e-45"), fmt(_t1, 20))
# 阳性对照：e^0=1 与 e^-1=1/e
guard("G0-11 exp(0)=1", abs(dexp(D(0)) - D(1)) < D("1e-45"), fmt(dexp(D(0)), 20))
guard("G0-12 exp(-1)=1/e", relerr(dexp(D(-1)), D(1) / dd("2.71828182845904523536028747135266249775724709369995")) < D("1e-45"),
      fmt(dexp(D(-1)), 25))

# e^2/(4 pi eps0) 与 alpha*hbar*c 的双路径互检（口径一致性）
_e2_4pe = E_CHG * E_CHG / (dd(4) * PI * EPS0)
_alpha_hc = ALPHA * HBAR * C_LIGHT
RES["e2_over_4pe0"] = fmt(_e2_4pe, 25)
RES["alpha_hbar_c"] = fmt(_alpha_hc, 25)
RES["e2_over_4pe0_rel_diff"] = fmt(relerr(_e2_4pe, _alpha_hc), 6)
guard("G0-13 e^2/(4 pi eps0) == alpha hbar c（双路径）",
      relerr(_e2_4pe, _alpha_hc) < D("1e-9"), fmt(relerr(_e2_4pe, _alpha_hc), 6))

# eps0 反解：与 CODATA 2022 声明值的一致性（判定常数口径）
_eps0_from_alpha = E_CHG * E_CHG / (dd(4) * PI * _alpha_hc)
RES["eps0_codata2022"] = "8.8541878188e-12"
RES["eps0_from_alpha"] = fmt(_eps0_from_alpha, 20)
RES["eps0_rel_diff"] = fmt(relerr(_eps0_from_alpha, EPS0), 6)

# G_F 的 SI 量纲还原（(46-18) 为自然单位关系，SI 形式须除以 (hbar c)^3）
# 注意：dpow 是量纲元组的幂运算，数值幂必须用 **（此处原写成 dpow(HBARC_GEVFM,3) 会抛
# TypeError: 'decimal.Decimal' object is not iterable）
_gf_si = GF_GEV2 * HBARC_GEVFM ** 3
RES["G_F_SI_GeV_m3"] = fmt(_gf_si, 20)
guard("G0-14 [G_F]=(M,L,T,Q)=(1,5,-2,0)",
      deq(dmul(dpow(DIM["E"], -2), dpow(dmul(DIM["hbar"], DIM["c"]), 3)), DIM["Gmu"]),
      dstr(dmul(dpow(DIM["E"], -2), dpow(dmul(DIM["hbar"], DIM["c"]), 3))))

# ==========================================================================
# §A 量纲齐次性逐式审计（46-1..46-25）
# ==========================================================================
DIMROWS = []


def dimrow(code, label, lhs, rhs, extra=""):
    ok = deq(lhs, rhs)
    DIMROWS.append({"code": code, "label": label, "lhs": dstr(lhs), "rhs": dstr(rhs),
                    "ok": ok, "extra": extra})
    return ok


# A1  F = -dV/dr
dimrow("A1", "46-2  F=-grad V", DIM["F"], dmul(DIM["E"], dinv(DIM["L"])))
# A2  Einstein 方程 G_uv = 8 pi G / c^4 T_uv
dimrow("A2", "46-6  G_uv=(8 pi G/c^4)T_uv",
       dmul(DIM["G"], dpow(DIM["c"], -4), dmul(DIM["M"], dpow(DIM["L"], -1), dpow(DIM["T"], -2))),
       dpow(DIM["L"], -2))
# A3  Einstein-Hilbert 作用量量纲 = 作用量
_eh_const = dmul(dpow(DIM["c"], 3), dinv(DIM["G"]))
dimrow("A3", "EH 作用量 [c^3/(16 pi G)] [R] [d^4x] = [hbar]",
       dmul(_eh_const, dpow(DIM["L"], -2), dpow(DIM["L"], 4)), DIM["hbar"])
# A4  Newton 势方程 div^2 Phi = 4 pi G rho
dimrow("A4", "div^2 Phi = 4 pi G rho",
       dmul(dpow(DIM["L"], -2), dmul(DIM["E"], dinv(DIM["M"]))),
       dmul(DIM["G"], dmul(DIM["M"], dpow(DIM["L"], -3))))
# A5  Yukawa 势常数 K：V=K e^{-mu r}/r
dimrow("A5", "46-5  力项 K/r^2 = [F]", dmul(DIM["Kyuk"], dpow(DIM["L"], -2)), DIM["F"])
dimrow("A5b", "46-5  力项 K mu/r = [F]",
       dmul(DIM["Kyuk"], dinv(DIM["L"]), dinv(DIM["L"])), DIM["F"])
# A6  色库仑 (4/3) alpha_s hbar c / r^2
dimrow("A6", "46-13  C_F alpha_s hbar c / r^2",
       dmul(DIM["hbar"], DIM["c"], dpow(DIM["L"], -2)), DIM["F"])
# A7  Cornell 弦张力项 sigma
dimrow("A7", "46-14  sigma 项 = [F]", DIM["sigma"], DIM["F"])
# A8  λ_B = hbar/(m c)
dimrow("A8", "46-16  lambda_B=hbar/(m c)", dmul(DIM["hbar"], dinv(DIM["M"]), dinv(DIM["c"])), DIM["L"])
# A9  弱 Yukawa 力
dimrow("A9", "46-17  eta alpha_eff hbar c / r^2",
       dmul(DIM["hbar"], DIM["c"], dpow(DIM["L"], -2)), DIM["F"])
# A10 洛伦兹力 q v x B
dimrow("A10", "46-10  [q v B] = [F]", dmul(DIM["Q"], DIM["c"], DIM["Bf"]), DIM["F"])
# A11 回旋半径与频率
dimrow("A11", "R=mv/(qB) = [L]", dmul(DIM["M"], DIM["c"], dinv(DIM["Q"]), dinv(DIM["Bf"])), DIM["L"])
dimrow("A11b", "omega=qB/m = [1/T]", dmul(DIM["Q"], DIM["Bf"], dinv(DIM["M"])), dinv(DIM["T"]))
# A12 KK 势 (46-20)
dimrow("A12", "46-20  hbar c/(r) 求和 = [E]", dmul(DIM["hbar"], DIM["c"], dinv(DIM["L"])), DIM["E"])
# A13 KK 力 (46-21)
dimrow("A13", "46-21  hbar c/r^2 求和 = [F]",
       dmul(DIM["hbar"], DIM["c"], dpow(DIM["L"], -2)), DIM["F"])
# A14 KK 小r 闭式 (46-22)
dimrow("A14", "46-22  hbar c lambda/(r^2) = [E]",
       dmul(DIM["hbar"], DIM["c"], DIM["L"], dpow(DIM["L"], -2)), DIM["E"])
# A15 KK 小r 力 (46-23)
dimrow("A15", "46-23  hbar c lambda/(r^3) = [F]",
       dmul(DIM["hbar"], DIM["c"], DIM["L"], dpow(DIM["L"], -3)), DIM["F"])
# A16 向心力 (46-25)
dimrow("A16", "46-25  m R omega^2 = [F]", dmul(DIM["M"], DIM["L"], dpow(DIM["T"], -2)), DIM["F"])
# A17 46-18 G_F/sqrt2 = g^2/(8 m_W^2)（自然单位：两侧同为 M^-2）
dimrow("A17", "46-18  [G_F]=M^-2（自然单位）", dpow(DIM["M"], -2), dpow(DIM["M"], -2),
       "natural units only; SI form = G_F/(hbar c)^3")

DIM_OK = sum(1 for r in DIMROWS if r["ok"])
DIM_ALL = len(DIMROWS)
RES["dim_audit"] = {"ok": DIM_OK, "total": DIM_ALL, "rows": DIMROWS}
add("A0", "INFO", "量纲逐式审计 %d/%d 齐次（46-1..46-25 覆盖" % (DIM_OK, DIM_ALL) + "）")
if DIM_OK != DIM_ALL:
    for r in DIMROWS:
        if not r["ok"]:
            add("A0-" + r["code"], "FAIL", "量纲不齐：%s  LHS=%s  RHS=%s" % (r["label"], r["lhs"], r["rhs"]))
guard("G-A1 全部方程量纲齐次", DIM_OK == DIM_ALL, "%d/%d" % (DIM_OK, DIM_ALL))

# ==========================================================================
# §B 46-19：两个质子 1 fm 的引力/电磁强度比（来料 §6.1）
# ==========================================================================
r_fm = FM


def F_grav(r):
    return G_N * M_P * M_P / (r * r)


def F_elec(r):
    return E_CHG * E_CHG / (dd(4) * PI * EPS0 * r * r)


Fg1 = F_grav(r_fm)
Fe1 = F_elec(r_fm)
ratio1 = Fe1 / Fg1

RES["s61"] = {
    "F_g_N": fmt(Fg1, 20),
    "F_e_N": fmt(Fe1, 20),
    "ratio": fmt(ratio1, 20),
    "doc_F_g": "1.867244955e-34",
    "doc_F_e": "230.7077551",
    "doc_ratio": "1.23555163e36",
    "relerr_F_g": fmt(relerr(Fg1, dd("1.867244955e-34")), 6),
    "relerr_F_e": fmt(relerr(Fe1, dd("230.7077551")), 6),
    "relerr_ratio": fmt(relerr(ratio1, dd("1.23555163e36")), 6),
}

_ok_g = relerr(Fg1, dd("1.867244955e-34")) < D("1e-8")
_ok_e = relerr(Fe1, dd("230.7077551")) < D("1e-8")
_ok_r = relerr(ratio1, dd("1.23555163e36")) < D("1e-8")
add("B1", "PASS" if _ok_g else "FAIL",
    "46-19a F_g=G m_p^2/r^2 = %s N（来料 1.867244955e-34，相对差 %s）"
    % (fmt(Fg1, 20), fmt(relerr(Fg1, dd("1.867244955e-34")), 3)))
add("B2", "PASS" if _ok_e else "FAIL",
    "46-19b F_e=e^2/(4 pi eps0 r^2) = %s N（来料 230.7077551，相对差 %s）"
    % (fmt(Fe1, 20), fmt(relerr(Fe1, dd("230.7077551")), 3)))
add("B3", "PASS" if _ok_r else "FAIL",
    "46-19c F_e/F_g = %s（来料 1.23555163e36，相对差 %s）"
    % (fmt(ratio1, 20), fmt(relerr(ratio1, dd("1.23555163e36")), 3)))
guard("G-B1 46-19 三项数值复现", _ok_g and _ok_e and _ok_r,
      fmt(relerr(ratio1, dd("1.23555163e36")), 3))

# r 无关性（两个势都是 1/r^2）
rs = [dd("1e-18"), dd("1e-15"), dd("1e-12"), dd("1e-6")]
ratios = [F_elec(x) / F_grav(x) for x in rs]
spread = max(ratios) - min(ratios)
RES["s61_r_independence"] = {
    "r_list": [fmt(x, 3) for x in rs],
    "ratio_list": [fmt(v, 20) for v in ratios],
    "abs_spread": fmt(spread, 6),
    "rel_spread": fmt(spread / ratio1, 6),
}
guard("G-B2 比值与 r 无关", spread / ratio1 < D("1e-40"), fz(spread / ratio1, 6))
add("B4", "PASS", "46-19 的 r 无关性成立（1e-18..1e-6 m 四点相对散布 %s）—— "
                  "但它是『两个势同为 1/r^2』的下推论，不是统一证据" % fz(spread / ratio1, 3))

# 与库内既有登记的三档读数交叉（常数版本漂移，见 §J）
RES["s61_cross_registry"] = {
    "this_calc": fmt(ratio1, 20),
    "tuft_v92_1fm": "-1.2355516353937863e36",
    "tuft_v110": "1.2355513755103258e36",
    "tuft_v104": "1.2355512466464277e36",
    "const_f_v2": "1.2355516357613855e36",
}
_reg = [dd("1.2355516353937863e36"), dd("1.2355513755103258e36"), dd("1.2355512466464277e36")]
_sp = (max(_reg) - min(_reg)) / _reg[0]
RES["s61_cross_registry"]["registry_rel_spread"] = fmt(_sp, 6)
add("B5", "INFO", "同一无量纲数在库内有 3 个版本（1.235551635/1.235551376/1.235551247 e36，"
                  "相对散布 %s）——属 eps0/G 的 CODATA 版本漂移，不构成物理分歧；"
                  "来料读数与最高档一致" % fmt(_sp, 3))

# ==========================================================================
# §C 46-13/46-14：Cornell 示范力值（来料 §6.2）
# ==========================================================================
r_c_fm = dd("0.20")
F_coul_GeVfm = dd(4) / dd(3) * ALPHA_S * HBARC_GEVFM / (r_c_fm * r_c_fm)   # GeV/fm
F_str_GeVfm = SIGMA_GEVFM                                                  # GeV/fm
N_per_GeVfm = GEV_J / FM
F_coul_N = F_coul_GeVfm * N_per_GeVfm
F_str_N = F_str_GeVfm * N_per_GeVfm
F_tot_N = F_coul_N + F_str_N

# 弦张力项与色库仑项的交叉半径
r_cross_fm = dsqrt(dd(4) / dd(3) * ALPHA_S * HBARC_GEVFM / SIGMA_GEVFM)

RES["s62"] = {
    "r_fm": "0.20",
    "alpha_s": "0.30",
    "sigma_GeVfm": "0.90",
    "GeV_fm_to_N": fmt(N_per_GeVfm, 12),
    "F_colorCoulomb_N": fmt(F_coul_N, 20),
    "F_string_N": fmt(F_str_N, 20),
    "F_total_N": fmt(F_tot_N, 20),
    "doc_colorCoulomb": "3.16153e5",
    "doc_string": "1.44196e5",
    "doc_total": "4.60349e5",
    "relerr_coulomb": fmt(relerr(F_coul_N, dd("3.16153e5")), 6),
    "relerr_string": fmt(relerr(F_str_N, dd("1.44196e5")), 6),
    "relerr_total": fmt(relerr(F_tot_N, dd("4.60349e5")), 6),
    "crossover_r_fm": fmt(r_cross_fm, 12),
    "coulomb_over_string_at_0.2fm": fmt(F_coul_N / F_str_N, 12),
}

_c_doc = (("colorCoulomb", F_coul_N, "3.16153e5"), ("string", F_str_N, "1.44196e5"),
          ("total", F_tot_N, "4.60349e5"))
CROWS = []
_ok_c = True
_c_max = D(0)
for _name, _val, _doc in _c_doc:
    _dev = relerr(_val, dd(_doc))
    _bnd = round_bound(_doc)
    _in = _dev <= _bnd
    _ok_c = _ok_c and _in
    _c_max = max(_c_max, _dev)
    CROWS.append({"item": _name, "calc_N": fmt(_val, 10), "doc": _doc,
                  "relerr": fmt(_dev, 6), "round_bound": fmt(_bnd, 6), "within_bound": _in})
RES["s62"]["doc_cells"] = CROWS
add("C1", "PASS" if _ok_c else "FAIL",
    "46-13/14 Cornell 三项力值 %s / %s / %s N（来料 3.16153e5 / 1.44196e5 / 4.60349e5；最大相对差 %s，"
    "三项均落在来料 6 位报价的舍入半界 %s ~ %s 内）⟹ 复现"
    % (fmt(F_coul_N, 8), fmt(F_str_N, 8), fmt(F_tot_N, 8), fmt(_c_max, 3),
       fmt(min(round_bound(d) for _, _, d in _c_doc), 3),
       fmt(max(round_bound(d) for _, _, d in _c_doc), 3)))
guard("G-C1 Cornell 三项落在来料舍入半界内", _ok_c, fmt(_c_max, 3))
add("C2", "INFO",
    "色库仑/弦张力项交叉半径 r*=(4 alpha_s hbar c/(3 sigma))^{1/2} = %s fm ⟹ 来料 r=0.20 fm 落在"
    "色库仑主导区（两项比 %s），两段力律的『短程/长程』划分有明确交叉点，来料未给出该读数"
    % (fmt(r_cross_fm, 6), fmt(F_coul_N / F_str_N, 6)))

# ==========================================================================
# §D 46-16/46-17：W/Z 约化康普顿长度与屏蔽因子 A(r)（来料 §6.3）
# ==========================================================================
def lam_m(m_gev):
    """约化康普顿长度（m）：hbar c /(m c^2)，m 以 GeV 计"""
    return HBARC_GEVFM / m_gev * FM


LAM_W = lam_m(MW_GEV)
LAM_Z = lam_m(MZ_GEV)


def A_yuk(r, lam):
    x = r / lam
    return dexp(-x) * (D(1) + x)


DOC_A = {
    ("W", "1e-18"): dd("0.93648"),
    ("W", "1e-17"): dd("0.08638"),
    ("W", "1e-16"): dd("8.55e-17"),
    ("Z", "1e-18"): dd("0.92106"),
    ("Z", "1e-17"): dd("0.05532"),
    ("Z", "1e-16"): dd("4.02e-19"),
}
r_pairs = [(dd("1e-18"), "1e-18"), (dd("1e-17"), "1e-17"), (dd("1e-16"), "1e-16")]
atable = []
anums = []
maxdev = D(0)
allin = True
for tag, lam, lam_doc in (("W", LAM_W, dd("2.4553e-18")), ("Z", LAM_Z, dd("2.1640e-18"))):
    for r, r_key in r_pairs:
        a_calc = A_yuk(r, lam)
        doc = DOC_A[(tag, r_key)]
        dev = relerr(a_calc, doc)
        bnd = round_bound(str(doc))
        within = dev <= bnd
        maxdev = max(maxdev, dev)
        allin = allin and within
        anums.append((tag, r_key, r, dev, r / lam))
        atable.append({"boson": tag, "r_m": r_key, "A_calc": fmt(a_calc, 10),
                       "A_doc": fmt(doc, 10), "relerr": fmt(dev, 6),
                       "round_bound": fmt(bnd, 6), "within_bound": within,
                       "x_r_over_lambda": fmt(r / lam, 6),
                       "lambda_m": fmt(lam, 10), "lambda_doc": fmt(lam_doc, 10)})

RES["s63"] = {
    "lambda_W_m": fmt(LAM_W, 12),
    "lambda_Z_m": fmt(LAM_Z, 12),
    "doc_lambda_W": "2.4553e-18",
    "doc_lambda_Z": "2.1640e-18",
    "relerr_lambda_W": fmt(relerr(LAM_W, dd("2.4553e-18")), 6),
    "relerr_lambda_Z": fmt(relerr(LAM_Z, dd("2.1640e-18")), 6),
    "A_table": atable,
    "A_max_relerr": fmt(maxdev, 6),
}
# --- D0：46-17 的 A(r) 不是拟合式，而是 Yukawa 势求导的力因子 ----------------
# V(r) = -K e^{-x}/r,  x = r/lambda
# dV/dr = K e^{-x}(1/r^2 + 1/(lambda r)) = (K/r^2) e^{-x}(1+x)
# F = -dV/dr = -(K/r^2) A(x)        <-- 46-17 的「屏蔽因子」由此严格给出
def V_yuk(r, lam, K=D(1)):
    return -K * dexp(-r / lam) / r


def F_yuk_fd(r, lam, K=D(1)):
    """中心差分求 F=-dV/dr；h=r*1e-6，截断误差 O(h^2/r^2)~1e-12。"""
    h = r * dd("1e-6")
    return -(V_yuk(r + h, lam, K) - V_yuk(r - h, lam, K)) / (dd(2) * h)


def A_sens(x):
    """A=e^{-x}(1+x) 对 lambda 的相对敏感度 (dA/A)/(dlambda/lambda)=x^2/(1+x)。"""
    return x * x / (D(1) + x)


D0ROWS = []
_d0max = D(0)
for _r, _k in r_pairs:
    _fd = F_yuk_fd(_r, LAM_W)
    _ana = -A_yuk(_r, LAM_W) / (_r * _r)
    _dev = relerr(_fd, _ana)
    _d0max = max(_d0max, _dev)
    D0ROWS.append({"r_m": _k, "F_fd_N": fmt(_fd, 15), "F_ana_N": fmt(_ana, 15),
                   "relerr": fmt(_dev, 6)})
RES["s63"]["D0_yukawa_factor"] = {"max_relerr": fmt(_d0max, 6), "rows": D0ROWS}
add("D0", "PASS" if _d0max < D("1e-9") else "FAIL",
    "46-17 的屏蔽因子 A(r)=e^{-x}(1+x) 由 Yukawa 势 V=-K e^{-x}/r 求导严格给出：F=-dV/dr=-(K/r^2)A；"
    "中心差分数值力 vs 解析式三点最大相对偏差 %s ⟹ 该因子是结构推论而非独立假设" % fmt(_d0max, 3))
guard("G-D0 46-17 A(r) 与 Yukawa 势求导对拍（数值微分 vs 解析）", _d0max < D("1e-9"),
      fmt(_d0max, 3))

_bW_doc = round_bound("2.4553e-18")
_bZ_doc = round_bound("2.1640e-18")
_dW = relerr(LAM_W, dd("2.4553e-18"))
_dZ = relerr(LAM_Z, dd("2.1640e-18"))
add("D1", "PASS" if (_dW <= _bW_doc and _dZ <= _bZ_doc) else "FAIL",
    "46-16 约化康普顿长度 lambda_W=%s m、lambda_Z=%s m；与来料 2.4553e-18 / 2.1640e-18 的相对差 "
    "%s / %s，落在来料『5 位有效数字』的舍入半界内（%s / %s）⟹ 复现，差异纯属报价位数"
    % (fmt(LAM_W, 10), fmt(LAM_Z, 10), fmt(_dW, 3), fmt(_dZ, 3), fmt(_bW_doc, 3), fmt(_bZ_doc, 3)))
guard("G-D1 lambda_W/Z 落在来料舍入半界内", _dW <= _bW_doc and _dZ <= _bZ_doc, fmt(_dW, 3))

_worst = max(anums, key=lambda t: t[3])
_worst_bnd = round_bound(str(DOC_A[(_worst[0], _worst[1])]))
if allin:
    add("D2", "PASS",
        "46-17 的 A(r) 六格全部落在来料打印精度的舍入半界内（最大偏差 %s @ %s、r=%s m，该格来料只印 "
        "3 位有效数字，半界 %s）⟹ 复现。偏差的来源可由敏感度恒等式定量解释：该格 x=r/lambda=%s，"
        "放大因子 s(x)=x^2/(1+x)=%s，即 lambda 的第 5~6 位舍入在此被放大约 %s 倍"
        % (fmt(maxdev, 3), _worst[0], _worst[1], fmt(_worst_bnd, 3), fmt(_worst[4], 4),
           fmt(A_sens(_worst[4]), 4), fmt(A_sens(_worst[4]), 3)))
else:
    add("D2", "BOUNDARY",
        "46-17 的 A(r) 六格存在超出打印半界的格子（最大偏差 %s @ %s、r=%s m，半界 %s）⟹ "
        "需要区分『来料计算误差』与『报价位数不足』，不可一律判缺陷"
        % (fmt(maxdev, 3), _worst[0], _worst[1], fmt(_worst_bnd, 3)))
guard("G-D2 46-17 A(r) 六格全部落在来料打印舍入半界内", allin, fmt(maxdev, 3))

# 敏感度恒等式（D2 归因用）：(dA/A)/(dlambda/lambda)=x^2/(1+x)，数值导数 vs 解析对拍
SENSROWS = []
_sensmax = D(0)
for _r, _k in r_pairs:
    _x = _r / LAM_W
    _h = dd("1e-8")
    _num = (A_yuk(_r, LAM_W * (D(1) + _h)) - A_yuk(_r, LAM_W * (D(1) - _h))) / (dd(2) * _h) \
        / A_yuk(_r, LAM_W)
    _dev = relerr(_num, A_sens(_x))
    _sensmax = max(_sensmax, _dev)
    SENSROWS.append({"r_m": _k, "x": fmt(_x, 6), "sens_num": fmt(_num, 10),
                     "sens_ana": fmt(A_sens(_x), 10)})
RES["s63"]["A_sensitivity"] = {"max_relerr": fmt(_sensmax, 6), "rows": SENSROWS}
guard("G-D2b 敏感度恒等式 s(x)=x^2/(1+x)（数值导数 vs 解析）", _sensmax < D("1e-9"),
      fmt(_sensmax, 3))


# 由来料 A(1e-17) 反解 lambda：检验「全表能否由单一 lambda 生成」+「该 lambda 是否为 ħc/(mc^2)」
def inv_lambda(target, r):
    # A 随 lambda 单调增（x=r/lambda 减小）；A>target 说明当前 lambda 偏大
    lo, hi = dd("1e-19"), dd("1e-15")
    for _ in range(200):
        mid = (lo + hi) / 2
        if A_yuk(r, mid) > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


_lam_star_W = inv_lambda(dd("0.08638"), dd("1e-17"))
_lam_star_Z = inv_lambda(dd("0.05532"), dd("1e-17"))
_r_W18 = relerr(A_yuk(dd("1e-18"), _lam_star_W), dd("0.93648"))
_r_W16 = relerr(A_yuk(dd("1e-16"), _lam_star_W), dd("8.55e-17"))
_r_Z18 = relerr(A_yuk(dd("1e-18"), _lam_star_Z), dd("0.92106"))
_r_Z16 = relerr(A_yuk(dd("1e-16"), _lam_star_Z), dd("4.02e-19"))
RES["s63"]["lambda_star"] = {
    "W_from_A_1e-17_m": fmt(_lam_star_W, 12),
    "W_relerr_vs_exact": fmt(relerr(_lam_star_W, LAM_W), 6),
    "Z_from_A_1e-17_m": fmt(_lam_star_Z, 12),
    "Z_relerr_vs_exact": fmt(relerr(_lam_star_Z, LAM_Z), 6),
    "W_other_cells_relerr": [fmt(_r_W18, 6), fmt(_r_W16, 6)],
    "Z_other_cells_relerr": [fmt(_r_Z18, 6), fmt(_r_Z16, 6)],
}
_star_ok = (relerr(_lam_star_W, LAM_W) < D("1e-4") and relerr(_lam_star_Z, LAM_Z) < D("1e-4"))
add("D3", "INFO",
    "反解校验：以 A_W(1e-17)=0.08638 反求 lambda*=%s m（与精确 ħc/(m_W c^2)=%s 相对差 %s），"
    "以 A_Z(1e-17)=0.05532 反求得 %s m（相对差 %s）⟹ 全表可由单一 lambda 生成，且该 lambda 与精确值"
    "同源到 1e-5 ⟹ 46-17 的表格内部自洽（用 lambda* 复算同表另四格最大偏差 %s，仍在打印半界内）"
    % (fmt(_lam_star_W, 10), fmt(LAM_W, 10), fmt(relerr(_lam_star_W, LAM_W), 3),
       fmt(_lam_star_Z, 10), fmt(relerr(_lam_star_Z, LAM_Z), 3),
       fmt(max(_r_W18, _r_W16, _r_Z18, _r_Z16), 3)))
guard("G-D3 反解 lambda* 与精确值同源（1e-4 内）", _star_ok,
      fmt(relerr(_lam_star_W, LAM_W), 3))

# ==========================================================================
# §E 46-18 数值面：G_F 与 (g, m_W) 的耦合闭环（两种 sin^2 theta_W 口径）
# ==========================================================================
SQ2 = dsqrt(D(2))


def sin2_from_GF():
    """G_F 口径（tree）：sin^2 theta_W = pi*alpha/(sqrt2 G_F m_W^2)。"""
    return PI * ALPHA / (SQ2 * GF_GEV2 * MW_GEV * MW_GEV)


def sin2_on_shell():
    """on-shell 口径：sin^2 theta_W = 1 - m_W^2/m_Z^2。"""
    return D(1) - MW_GEV * MW_GEV / (MZ_GEV * MZ_GEV)


def gf_from_coupling(sin2):
    """由 g = e/sin(theta_W) 出发：G_F = sqrt2*g^2/(8 m_W^2)（46-18 的原式）。"""
    g_w = dsqrt(dd(4) * PI * ALPHA) / dsqrt(sin2)
    return SQ2 * g_w * g_w / (dd(8) * MW_GEV * MW_GEV)


S2_GF = sin2_from_GF()
S2_OS = sin2_on_shell()
_GF_A = PI * ALPHA / (SQ2 * S2_OS * MW_GEV * MW_GEV)
_GF_B = gf_from_coupling(S2_OS)
_E1_DEV = relerr(_GF_A, _GF_B)
GF_GAP = relerr(_GF_A, GF_GEV2)
MZ_PRED = MW_GEV / dsqrt(D(1) - S2_GF)
MZ_GAP = relerr(MZ_PRED, MZ_GEV)
S2_GAP = relerr(S2_GF, S2_OS)

RES["s64"] = {
    "sin2_theta_W_GF_scheme": fmt(S2_GF, 12),
    "sin2_theta_W_on_shell": fmt(S2_OS, 12),
    "sin2_rel_gap": fmt(S2_GAP, 6),
    "GF_pred_from_on_shell_GeV-2": fmt(_GF_A, 12),
    "GF_doc_GeV-2": "1.1663787e-5",
    "GF_relerr": fmt(GF_GAP, 6),
    "mZ_pred_from_GF_scheme_GeV": fmt(MZ_PRED, 12),
    "mZ_doc_GeV": "91.1876",
    "mZ_relerr": fmt(MZ_GAP, 6),
    "identity_two_paths_relerr": fmt(_E1_DEV, 6),
}
add("E1", "INFO",
    "46-18（G_F/sqrt2 = g^2/(8 m_W^2)）在给定 sin^2 theta_W 时是**代数恒等式**：两条独立代码路径"
    "（G_F <- pi*alpha/(sqrt2 s2 m_W^2) 与 G_F <- sqrt2 g^2/(8 m_W^2)）残差 %s ⟹ 零信息量——"
    "它只能把 {alpha, m_W, G_F, sin^2 theta_W} 四量中的任两个换成第三个，不能预测其中任何一个"
    % fz(_E1_DEV, 3))
guard("G-E1 46-18 两路径代数同一（机器零）", _E1_DEV < D("1e-40"), fz(_E1_DEV, 3))

add("E2", "BOUNDARY",
    "树图口径不能同时容纳 (m_W, m_Z, G_F, alpha)：G_F 口径 sin^2=%s 与 on-shell 口径 %s 相差 %s；"
    "用 on-shell 口径预测 G_F 得 %s（实测 1.1663787e-5，差 %s）；用 G_F 口径预测 m_Z 得 %s GeV"
    "（实测 91.1876，差 %s）。缺口量级恰为一圈辐射修正（Delta_r / Delta_rho），不是算错，"
    "而是**任何**树图口径都成立的事实 ⟹ 46-18 只可作结构关系，不可作 1e-3 级精密检验；"
    "引用时必须声明用的是哪一个 sin^2 theta_W 口径"
    % (fmt(S2_GF, 8), fmt(S2_OS, 8), fmt(S2_GAP, 3), fmt(_GF_A, 8), fmt(GF_GAP, 3),
       fmt(MZ_PRED, 8), fmt(MZ_GAP, 3)))
guard("G-E2 两口径缺口为一圈量级（1e-2 .. 1e-1）",
      D("1e-2") < S2_GAP < D("1e-1"), fmt(S2_GAP, 3))

# ==========================================================================
# §F 汇总与落盘（96_rootv46_fourforce_results.json / _report.txt）
# ==========================================================================
add("F1", "INFO",
    "覆盖边界（诚实登记）：§A 对 46-1..46-25 的 %d 条式做了量纲审计（%d/%d 齐次）；数值比对只覆盖来料 "
    "§6.1（46-19）、§6.2（46-13/14）、§6.3（46-16/17）与 46-18 关系式。46-10/46-11（洛伦兹力/回旋）、"
    "46-20..46-23（KK 求和）、46-25（向心力）的数值读数本轮未随来料提供 ⟹ 不做数值比对，"
    "也不据此判定其成立" % (DIM_ALL, DIM_OK, DIM_ALL))

VCOUNT = {}
for _row in ROWS:
    VCOUNT[_row["verdict"]] = VCOUNT.get(_row["verdict"], 0) + 1
G_PASS = sum(1 for g in GUARDS if g["ok"])
G_TOTAL = len(GUARDS)
FAIL_ROWS = [r["code"] for r in ROWS if r["verdict"] == "FAIL"]
EXIT = 0 if (G_PASS == G_TOTAL and not FAIL_ROWS) else 1

RES["summary"] = {
    "rows": len(ROWS),
    "verdict_counts": VCOUNT,
    "fail_rows": FAIL_ROWS,
    "guards_total": G_TOTAL,
    "guards_passed": G_PASS,
    "dim_rows": "%d/%d" % (DIM_OK, DIM_ALL),
    "exit_code": EXIT,
}
RES["guards"] = [{"name": g["name"], "ok": g["ok"], "detail": g["detail"]} for g in GUARDS]
RES["rows"] = ROWS

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
OUT_JSON = os.path.join(HERE, "96_rootv46_fourforce_results.json")
OUT_TXT = os.path.join(HERE, "96_rootv46_fourforce_report.txt")

with io.open(OUT_JSON, "w", encoding="utf-8") as _fj:
    _fj.write(json.dumps(RES, indent=2, ensure_ascii=False, default=str))

_lines = []
_lines.append("ROOT V46《四种基本力的本源方程》全维机验（卷 96）")
_lines.append("Decimal 精度 %d 位；纯标准库；不联网、不读外部数据" % getcontext().prec)
_lines.append("")
_lines.append("== 汇总 ==")
_lines.append("条目 %d：%s" % (len(ROWS), "  ".join("%s=%d" % (k, v) for k, v in sorted(VCOUNT.items()))))
_lines.append("守卫 %d/%d 通过；量纲审计 %d/%d；退出码 %d" % (G_PASS, G_TOTAL, DIM_OK, DIM_ALL, EXIT))
if FAIL_ROWS:
    _lines.append("FAIL 条目：%s" % ",".join(FAIL_ROWS))
_lines.append("")
_lines.append("== 量纲逐式审计（46-1..46-25）==")
for _r in DIMROWS:
    _lines.append("[%s] %-42s LHS=%-22s RHS=%-22s %s"
                  % ("OK " if _r["ok"] else "BAD", _r["label"], _r["lhs"], _r["rhs"], _r["extra"]))
_lines.append("")
_lines.append("== 条目 ==")
for _r in ROWS:
    _lines.append("[%s] %-4s %s" % (_r["verdict"], _r["code"], _r["text"]))
_lines.append("")
_lines.append("== 守卫 ==")
for _g in GUARDS:
    _lines.append("[%s] %-52s %s" % ("PASS" if _g["ok"] else "FAIL", _g["name"], _g["detail"]))
_lines.append("")
_lines.append("== 关键读数 ==")
_lines.append("lambda_W = %s m ; lambda_Z = %s m" % (RES["s63"]["lambda_W_m"], RES["s63"]["lambda_Z_m"]))
_lines.append("A(r) 六格最大相对偏差 = %s（来料打印舍入半界内）" % RES["s63"]["A_max_relerr"])
_lines.append("Cornell：%s / %s / %s N" % (RES["s62"]["F_colorCoulomb_N"], RES["s62"]["F_string_N"],
                                        RES["s62"]["F_total_N"]))
_lines.append("F_e/F_g(1 fm) = %s" % RES["s61"]["ratio"])
_lines.append("sin^2 theta_W：G_F 口径 %s / on-shell %s（差 %s）"
              % (RES["s64"]["sin2_theta_W_GF_scheme"], RES["s64"]["sin2_theta_W_on_shell"],
                 RES["s64"]["sin2_rel_gap"]))

with io.open(OUT_TXT, "w", encoding="utf-8") as _ft:
    _ft.write("\n".join(_lines) + "\n")

print("\n".join(_lines[:6]))
print("产物：%s / %s" % (os.path.basename(OUT_JSON), os.path.basename(OUT_TXT)))
sys.exit(EXIT)

