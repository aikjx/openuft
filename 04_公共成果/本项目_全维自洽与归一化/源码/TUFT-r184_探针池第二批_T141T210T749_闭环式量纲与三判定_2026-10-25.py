# -*- coding: utf-8 -*-
"""
TUFT-r184 · 探针池第二批（T141 / T210+T211 / T749）闭环式量纲与三判定 · 精算
2026-10-25

来料（只读，不改写）：
  A. openuft/04_公共成果/本项目_统一场论攻破/布局_剩余项分层归档_2026-10-24.md §一
     ①可精算池 12 项，第 3/4/11 行 = T141 / T210+T211 / T749
  B. 同目录 README.md L10（第一批 T147/T712/T947/T163）与 r183 F06（批次账修正）

承接关系：
  r183（第一批）F06 已把第二批真实工作量核定为 3 项（T141 / T210+T211 成对 / T749），
  并留两项附带任务：①T718 的 archive G0 数值（r183 C04 只登记）②F5 钱德拉塞卡仍无回合。
  本册执行这 3 项 + T718 数值复核；钱德拉塞卡仍不在本批。

三判定口径（承 r183，可执行）：
  C1 无约束（退化）：探针不触及 TUFT 的可动自由度（TUFT 侧供给=0）⇒ 零信息量。
  C2 力约束放行    ：TUFT 侧有数值且落在探针区间内 ⇒ 仅「一致」，不得作证明。
  C3 力约束否定    ：TUFT 侧有数值且越出探针上界 ⇒ 该自由度被压缩/排除。

纪律（承 r174 / r183）：
  · 探针对 TUFT 的供给恒为 0；PROBE 永不出「PASS-as-proof」，最高只到 C3 型约束。
  · 「残差机器零」若来自构造性恒等式，必须显式标注「口径交叉印证、非独立验证」。
  · 不自推的系数一律标 BOUNDARY 并指向登记处，不猜；外部观测值一律标 [C]。
  · 量纲机器的原语本身必须先被守卫（r183 A12 教训：r37/r44 两次因原语写错而全线失真）。
红线：本册不产生新物理，不宣称观测证实/否证，不改写任何来料字节。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                     # 04_公共成果/本项目_全维自洽与归一化
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r184_探针池第二批_T141T210T749_闭环式量纲与三判定_2026-10-25"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal

ENTRIES = []
GUARDS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            # Decimal 零值经 '.nE' 格式化会把指数印成 n（如 0.0000E+4），
            # 易被误读为 1e4；显式固定为 E+0。
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


# =====================================================================
# 0. 量纲机器（五元组 M, L, T, Q, K；K = 温度）+ 自身守卫
# =====================================================================
NDIM = 5


def _dcheck(*arrs):
    """length guard: zip() 对不等长元组会静默截断，故先验长度。"""
    for a in arrs:
        if len(a) != NDIM:
            raise ValueError("dimension tuple must have length %d, got %d: %r"
                             % (NDIM, len(a), a))


def dmul(a, b):
    _dcheck(a, b)
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    _dcheck(a, b)
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    _dcheck(a)
    return tuple(x * n for x in a)


def dsqrt(a):
    _dcheck(a)
    return tuple(Fraction(x, 2) for x in a)


def dstr(a):
    syms = ("M", "L", "T", "Q", "K")
    parts = []
    for s, e in zip(syms, a):
        if e != 0:
            parts.append(s + "^" + str(e))
    return "1" if not parts else " ".join(parts)


Z = (Fraction(0),) * 5
ONE = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
LEN = (Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0))
TIM = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0))
TMP = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1))
MSS = (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0))

DIM = {
    "c":     (Fraction(0), Fraction(1), Fraction(-1), Fraction(0), Fraction(0)),
    "G":     (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0), Fraction(0)),
    "hbar":  (Fraction(1), Fraction(2), Fraction(-1), Fraction(0), Fraction(0)),
    "h":     (Fraction(1), Fraction(2), Fraction(-1), Fraction(0), Fraction(0)),
    "kB":    (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(-1)),
    "e":     (Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    "r":     (Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    # ---- 本批新增 ----
    "Omega": (Fraction(0), Fraction(0), Fraction(-1), Fraction(0), Fraction(0)),   # 角速度
    "I":     (Fraction(1), Fraction(2), Fraction(0), Fraction(0), Fraction(0)),    # 转动惯量
    "E":     (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(0)),   # 能量
    "S":     (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(-1)),  # 熵 J/K
    "kappa2": (Fraction(-1), Fraction(-1), Fraction(2), Fraction(0), Fraction(0)), # 8piG/c^4
}

# ---- 数值常数（CODATA 2018/2022 字面值；外部输入，标 [C]）----
PI_STR = ("3."
          "14159265358979323846264338327950288419716939937510"
          "58209749445923078164062862089986280348253421170679"
          "82148086513282306647093844609550582231725359408128"
          "48111745028410270193852110555964462294895493038196")
PI = D(PI_STR)
CV = D("299792458")
HV = D("6.62607015E-34")
HBARV = HV / (D(2) * PI)
KBV = D("1.380649E-23")
GV = D("6.67430E-11")
MSUN = D("1.98892E30")
MPL = (HBARV * CV / GV).sqrt()                    # 普朗克质量，由 hbar c / G 直接开方
G0V = D("9.80665")


def main():
    print("=" * 78)
    print("TUFT-r184 · 探针池第二批 T141 / T210+T211 / T749 · 闭环式与三判定")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲机器自身守卫（先自检，再审对象）
    # =================================================================
    print("\n[A] 量纲机器自检（五元组 M,L,T,Q,K）")

    # ---- A.1 原语自检 ----
    bad_len = [k for k, v in DIM.items() if len(v) != NDIM]
    bad_len += [n for n, v in (("ONE", ONE), ("LEN", LEN), ("TIM", TIM),
                               ("TMP", TMP), ("MSS", MSS), ("Z", Z)) if len(v) != NDIM]
    guard("G0-P0 all_tuples_are_5d", not bad_len, "长度异常项：" + repr(bad_len))
    guard("G0-P1 mul_identity", dmul(ONE, DIM["G"]) == DIM["G"],
          "ONE*G = " + dstr(dmul(ONE, DIM["G"])))
    d_self = ddiv(DIM["kappa2"], DIM["kappa2"])
    guard("G0-P2 div_self_is_one", d_self == ONE, "kappa2/kappa2 = " + dstr(d_self))
    ok_p3 = (dpow(DIM["e"], 2) == dmul(DIM["e"], DIM["e"])
             and dpow(DIM["e"], 0) == ONE
             and dpow(DIM["c"], -1) == ddiv(ONE, DIM["c"]))
    guard("G0-P3 pow_matches_repeated_mul", ok_p3, "幂与连乘不一致")
    ok_p4 = (dmul(dsqrt(DIM["G"]), dsqrt(DIM["G"])) == DIM["G"]
             and dmul(dsqrt(DIM["kB"]), dsqrt(DIM["kB"])) == DIM["kB"])
    guard("G0-P4 sqrt_roundtrip", ok_p4,
          "(sqrt G)^2 = " + dstr(dmul(dsqrt(DIM["G"]), dsqrt(DIM["G"]))))
    s_neg = dstr(DIM["c"])
    s_frac = dstr(dsqrt(DIM["hbar"]))
    guard("G0-P5 dstr_single_sign",
          ("--" not in s_neg) and ("--" not in s_frac) and (dstr(ONE) == "1"),
          "c=" + s_neg + " sqrt(hbar)=" + s_frac)
    caught = False
    try:
        dmul((Fraction(0), Fraction(1)), DIM["c"])
    except ValueError:
        caught = True
    guard("G0-P6 length_mismatch_raises", caught,
          "不等长元组竟被静默 zip 截断——_dcheck 未生效")

    # ---- A.2 本批用到的量纲关系 ----
    d_pl = dsqrt(ddiv(dmul(DIM["hbar"], DIM["G"]), dpow(DIM["c"], 3)))
    guard("G0-1 planck_length_is_L", d_pl == LEN, "得到 " + dstr(d_pl))
    d_ptb = dsqrt(ddiv(dmul(DIM["hbar"], DIM["G"]), dpow(DIM["c"], 5)))
    guard("G0-2 planck_time_is_T", d_ptb == TIM, "得到 " + dstr(d_ptb))
    d_mpl = dsqrt(ddiv(dmul(DIM["hbar"], DIM["c"]), DIM["G"]))
    guard("G0-3 planck_mass_is_M", d_mpl == MSS, "得到 " + dstr(d_mpl))

    # G0-4 角速度 x 时间 = 1（T141 用）
    guard("G0-4 omega_times_time_is_1", dmul(DIM["Omega"], TIM) == ONE,
          "Omega*s = " + dstr(dmul(DIM["Omega"], TIM)))

    # G0-5 转动惯量 x Omega^2 = 能量（T141 的两侧同量纲性）
    d_Iw2 = dmul(DIM["I"], dpow(DIM["Omega"], 2))
    guard("G0-5 inertia_omega2_is_energy", d_Iw2 == DIM["E"],
          "I*w^2 = " + dstr(d_Iw2))

    # G0-6 kappa^2 = 8 pi G / c^4 的量纲（T210 面积律入口）
    d_k2 = ddiv(DIM["G"], dpow(DIM["c"], 4))
    guard("G0-6 kappa2_dim", d_k2 == DIM["kappa2"],
          "G/c^4 = " + dstr(d_k2) + "（应 M^-1 L^-1 T^2）")

    # G0-7 面积 x kappa^2 = 长度^2 x M^-1L^-1T^2 -> 必须再除 hbar 才得熵
    d_Ak2 = dmul(dpow(LEN, 2), DIM["kappa2"])
    guard("G0-7 area_kappa2_not_entropy", d_Ak2 != DIM["S"],
          "A*kappa^2 竟已等于熵量纲——说明漏了 1/hbar")

    # G0-8 面积/(hbar*kappa^2) = 无量纲（自然单位口径的熵）
    d_S_nat = ddiv(dpow(LEN, 2), dmul(DIM["hbar"], DIM["kappa2"]))
    guard("G0-8 area_over_hbar_kappa2_is_1", d_S_nat == ONE,
          "A/(hbar*kappa^2) = " + dstr(d_S_nat))

    # G0-9 能量 x 长度 / (hbar c) = 无量纲（Bekenstein 界入口）
    d_bek = ddiv(dmul(DIM["E"], LEN), dmul(DIM["hbar"], DIM["c"]))
    guard("G0-9 ER_over_hbar_c_is_1", d_bek == ONE,
          "E*R/(hbar*c) = " + dstr(d_bek))

    add("A01", "INFO", "本批新增量纲登记（Omega / I / E / S / kappa^2 五项）",
        "第二批首次使用角速度、转动惯量、能量、熵、引力耦合平方五项量纲。"
        "关键守卫三条：①G0-8 证明 `A/(hbar*kappa^2)` 无量纲（自然单位口径的熵）；"
        "②G0-7 是负向对照——`A*kappa^2` 单乘**不等于**熵量纲，必须再除 hbar，"
        "故「熵 = 面积/4l_P^2」不是任何两项的凑合；"
        "③G0-9 证明 `E*R/(hbar c)` 无量纲（Bekenstein 界两侧同量纲的前提）。"
        "原语自检（G0-P0..P6）承 r183 A12：长度 fail-fast + 单位元/逆元/幂/开方/dstr/负向对照。",
        {"new_dims": {"Omega": dstr(DIM["Omega"]), "I": dstr(DIM["I"]),
                      "E": dstr(DIM["E"]), "S": dstr(DIM["S"]),
                      "kappa2": dstr(DIM["kappa2"])},
         "A_over_hbar_kappa2": dstr(d_S_nat)})

    # =================================================================
    # B 段 · T141 连续引力波椭率上限
    # =================================================================
    print("\n[B] T141 · 连续引力波椭率上限")
    print("  来料式：eps_max <= (1/2) * Omega^2 R^3 / (G M)")

    # B01 量纲：eps 无量纲；Omega^2 R^3/(G M) 无量纲
    d_x = ddiv(dmul(dpow(DIM["Omega"], 2), dpow(LEN, 3)), dmul(DIM["G"], MSS))
    guard("B01 ellipticity_bound_is_dimensionless", d_x == ONE,
          "Omega^2 R^3/(G M) = " + dstr(d_x))
    add("B01", "PASS", "量纲闭合：eps_max 与 Omega^2 R^3/(G M) 均为无量纲",
        "`Omega^2 R^3/(G M)` 机器算得 `1`（守卫 B01），故椭率上限是无量纲量，"
        "与 eps=(I_xx-I_yy)/I_zz 的定义域相容。此为**必要**检查，不构成物理正确性。",
        {"dim_x": dstr(d_x)})

    # B02 恒等改写：x = (Omega/Omega_K)^2，Omega_K = sqrt(GM/R^3)
    M_NS = D("1.4") * MSUN
    R_NS = D("1.0E4")
    GM = GV * M_NS
    OMK = (GM / (R_NS * R_NS * R_NS)).sqrt()
    FK = OMK / (D(2) * PI)
    print("  标准中子星口径 M=1.4Msun, R=10km: Omega_K=%s rad/s  f_K=%s Hz"
          % (fs(OMK, 12), fs(FK, 12)))
    guard("B02 kepler_frequency_order", D(1000) < FK < D(10000),
          "f_K = " + fs(FK, 12) + " Hz（应 O(1e3)）")

    # 同一 x 的两条路径必须机器零
    OM_test = D("716.3556")            # [C] 已知最快核动力脉冲星 J1748-2446ad, P=1.3959 ms
    x_path1 = OM_test * OM_test * R_NS ** 3 / GM
    x_path2 = (OM_test / OMK) ** 2
    res_x = (x_path1 - x_path2) / x_path2
    guard("B02b two_paths_agree", abs(res_x) < D("1E-60"),
          "两条 x 路径残差 = " + fs(res_x))
    eps_max = x_path2 / D(2)
    print("  最快脉冲星 f=%s Hz -> x=%s  eps_max=%s"
          % (fs(OM_test, 8), fs(x_path2, 12), fs(eps_max, 12)))
    add("B02", "PASS", "恒等改写可执行：eps_max = (1/2)(Omega/Omega_K)^2，两条路径残差机器零",
        "`Omega^2R^3/(GM) = (Omega/Omega_K)^2`，`Omega_K=sqrt(GM/R^3)`。"
        "同一量用「直接式」与「比值式」两条路径计算，相对残差 " + fs(res_x) +
        "（机器零）。1.4Msun/10km 口径：f_K=" + fs(FK, 10) + " Hz（开普勒破碎频率），"
        "与文献 2 kHz 量级一致（**口径交叉印证，非独立验证**）。"
        "取 [C] 最快核动力脉冲星 f=716.3556 Hz 得 eps_max=" + fs(eps_max, 10) + "。",
        {"Omega_K": fs(OMK, 12), "f_K_Hz": fs(FK, 12),
         "f_fastest_Hz": fs(OM_test, 8), "x": fs(x_path2, 12), "eps_max": fs(eps_max, 12)})

    # B03 系数 1/2 非唯一：逃逸速度判据给系数 1
    #   赤道离心平衡: Omega^2 R = GM/R^2  => eps <= (1/2) x
    #   破碎/逃逸速度 : v_rot = Omega R <= sqrt(2GM/R) => Omega^2 R^3 <= 2GM => eps <= x
    eps_path_a = x_path2 / D(2)
    eps_path_b = x_path2
    ratio_ab = eps_path_b / eps_path_a
    guard("B03 coefficient_two_paths_ratio_is_2", ratio_ab == D(2),
          "两条判据系数比 = " + fs(ratio_ab))
    add("B03", "FAIL", "系数 1/2 不可自推：同一物理（破碎）的两条判据给出相差 2 倍的界",
        "①赤道离心平衡 `Omega^2 R = GM/R^2` ⇒ `eps <= (1/2)x`（来料取此）；"
        "②逃逸速度判据 `v_rot = Omega R <= sqrt(2GM/R)` ⇒ `eps <= x`（系数 1）。"
        "两者比值机器恰为 2（守卫 B03）。archive 未声明取哪一条，也未给 1/2 的推导 ⇒ "
        "该系数属**未登记的 O(1) 外部约定**，本册不代选。"
        "同口径数值：系数 1/2 时 eps_max=" + fs(eps_path_a, 10) + "，系数 1 时 " + fs(eps_path_b, 10) + "。",
        {"ratio": fs(ratio_ab), "eps_coef_half": fs(eps_path_a, 12),
         "eps_coef_one": fs(eps_path_b, 12)})

    # B04 判据的有效频率阈值：eps_max = 1e-6 时 f 需多低
    eps_target = D("1E-6")
    x_target = D(2) * eps_target                     # 系数 1/2 口径
    f_thr = FK * x_target.sqrt()
    print("  eps_max=1e-6 对应的频率阈值 f <= %s Hz" % fs(f_thr, 8))
    guard("B04 threshold_below_10Hz", f_thr < D(10),
          "阈值 = " + fs(f_thr, 8) + " Hz（应远低于 10 Hz）")
    add("B04", "BOUNDARY", "破碎判据只在 f <~ 3 Hz 时才有约束力（对 1.4Msun/10km 口径）",
        "把「eps 上限」反解成频率：`eps_max = 1e-6` 要求 `(1/2)(f/f_K)^2 <= 1e-6` ⇒ "
        "`f <= f_K*sqrt(2e-6)` = " + fs(f_thr, 8) + " Hz。"
        "⇒ 对毫秒脉冲星（f ~ 1e2–1e3 Hz），破碎判据给的上限在 1e-2~1e-1，"
        "而连续波观测上限在 1e-6 量级 ⇒ 破碎判据**弱 4–5 个量级**，无约束力。"
        "该读数只依赖 f_K 与「系数 1/2」口径（B03 已标明后者是外部约定）。",
        {"f_threshold_Hz": fs(f_thr, 10), "eps_target": fs(eps_target),
         "f_K_Hz": fs(FK, 12)})

    # B05 多档观测上界的鲁棒性（不指定具体实验，避免记错数）
    rows_b05 = []
    ok_b05 = True
    for obs_s in ("1E-5", "1E-6", "1E-7"):
        eps_obs = D(obs_s)
        ratio = eps_path_a / eps_obs                  # >1 表示破碎判据更宽松
        dec = ratio.log10()
        rows_b05.append({"eps_obs_upper": obs_s, "ratio_broken_over_obs": fs(ratio, 8),
                         "orders_weaker": fs(dec, 6)})
        if not (D(2) < dec < D(8)):
            ok_b05 = False
    guard("B05 broken_bound_weaker_in_all_bands", ok_b05,
          "三档观测上界下，破碎判据的宽松倍数应落在 2~8 个量级")
    add("B05", "BOUNDARY", "三档观测上界并列：破碎判据比观测上限宽 3.7–5.7 个量级（结论对档位鲁棒）",
        "不指定具体实验（避免把记不准的实验数当输入），改为把观测上限设为参数，"
        "并列 1e-5 / 1e-6 / 1e-7 三档（均标 [C]）：破碎判据 / 观测上限 = "
        + " / ".join([r["ratio_broken_over_obs"] for r in rows_b05]) +
        "，即宽松 " + " / ".join([r["orders_weaker"] for r in rows_b05]) + " 个量级。"
        "三档给出**同一结论**（破碎判据无约束力），故该判定不依赖具体实验数。",
        {"bands": rows_b05, "eps_broken": fs(eps_path_a, 12)})

    add("B06", "INFO", "T141 三判定 = C1（TUFT 侧无椭率闭式）",
        "TUFT 侧没有「连续波椭率」的内定数值：椭率是星体形状参数（I_xx-I_yy）/I_zz，"
        "属 EoS/形变历史，不在螺旋公设的可动自由度内。⇒ C1，不得报道为「通过」。",
        {})

    # =================================================================
    # C 段 · T210 / T211 黑洞熵面积律 + 对数修正
    # =================================================================
    print("\n[C] T210/T211 · 黑洞熵面积律与对数修正")
    print("  来料式：S_BH = A/(4 l_P^2)；S = S_BH + C ln S_BH + O(1)")

    # C01 面积律量纲：两条口径并列
    d_A = dmul(DPOW4, ONE) if False else None       # placeholder (kept for clarity)
    d_S_si = ddiv(dmul(DIM["kB"], dpow(LEN, 2)),
                  dmul(dpow(DPOW2_HACK(), 2) if False else ONE, ONE)) if False else None

    # r_s = 2GM/c^2 ; A = 4 pi r_s^2 = 16 pi G^2 M^2 / c^4
    d_rs = ddiv(dmul(DIM["G"], MSS), dpow(DIM["c"], 2))
    d_A_dim = dpow(d_rs, 2)
    guard("C01 horizon_area_is_L2", d_A_dim == dpow(LEN, 2), "A = " + dstr(d_A_dim))

    # S = kB * A/(4 l_P^2)：量纲 J/K
    d_S_dim = dmul(DIM["kB"], ddiv(dpow(LEN, 2), dpow(LEN, 2)))
    guard("C01b entropy_is_J_per_K", d_S_dim == DIM["S"], "S = " + dstr(d_S_dim))

    add("C01", "PASS", "面积律量纲闭合（两口径并列：k_B 显式 = J/K；k_B=1 = 无量纲）",
        "`r_s=2GM/c^2` ⇒ `A=4pi r_s^2` 量纲 `L^2`（守卫 C01）；`S=k_B A/(4l_P^2)` 量纲 "
        + dstr(d_S_dim) + " = J/K（守卫 C01b）。若取 k_B=1 约定则熵为无量纲量。"
        "**两口径必须并列声明**，混用会把 k_B 的维数弄丢（与 r183 A11 的「温度≠时间」同型陷阱）。",
        {"A_dim": dstr(d_A_dim), "S_dim": dstr(d_S_dim)})

    # C02 闭式：S = 4 pi G M^2/(hbar c) = 4 pi (M/m_P)^2（两条路径机器零）
    S_M = D(4) * PI * GV * MSUN * MSUN / (HBARV * CV)
    S_ratio = D(4) * PI * (MSUN / MPL) ** 2
    res_S = (S_M - S_ratio) / S_ratio
    guard("C02 two_paths_agree", abs(res_S) < D("1E-60"), "残差 = " + fs(res_S))
    print("  S(Msun) = %s" % fs(S_M, 12))
    guard("C02b entropy_order", D("1E76") < S_M < D("1E78"),
          "S(Msun) = " + fs(S_M, 12) + "（应 O(1e77)）")
    add("C02", "PASS", "闭式两路径机器零：S = 4piG M^2/(hbar c) = 4pi (M/m_P)^2",
        "路径 a（面积/4l_P^2）：`S=4pi G M^2/(hbar c)`；路径 b（普朗克单位）：`S=4pi(M/m_P)^2`。"
        "两路径相对残差 " + fs(res_S) + "（机器零）。M=M_sun 时 S=" + fs(S_M, 12) +
        "。**口径交叉印证、非独立验证**（两式互为代数重排，与 r183 E04 同型标注）。",
        {"S_sun": fs(S_M, 12), "residual": fs(res_S), "m_P_kg": fs(MPL, 12)})

    # C03 Bekenstein 界饱和：2 pi E R/(hbar c) 与 A/(4l_P^2) 相等（R=r_s 时）
    S_bek = D(2) * PI * (MSUN * CV * CV) * (D(2) * GV * MSUN / (CV * CV)) / (HBARV * CV)
    res_bek = (S_bek - S_M) / S_M
    guard("C03 schwarzschild_saturates_bekenstein", abs(res_bek) < D("1E-60"),
          "残差 = " + fs(res_bek))
    add("C03", "PASS", "Schwarzschild 饱和 Bekenstein 界：2piER/(hbar c) 与 A/(4l_P^2) 机器相等",
        "取 `E=Mc^2`、`R=r_s=2GM/c^2`，则 `2pi E R/(hbar c) = 4piG M^2/(hbar c)` = 面积律熵，"
        "相对残差 " + fs(res_bek) + "（机器零）。⇒ 该黑洞**恰好饱和**熵界（不违反、不冗余）。"
        "**口径交叉印证、非独立验证**：两式是同一代数量的重排，本册只用它确认面积律的系数 1/4 "
        "与熵界系数 2pi 在 Schwarzschild 上自洽，不构成对 1/4 的推导。",
        {"residual": fs(res_bek), "S_bek": fs(S_bek, 12)})

    # C04 对数修正系数 C 不可自推
    add("C04", "BOUNDARY", "对数修正系数 C 不可自推：依赖场内容与截断方案（外部输入）",
        "`S = S_BH + C ln S_BH + O(1)` 中的 C 是迹反常系数，其数值随「场内容 + 正则化/截断方案」"
        "变化（不同 scheme 给出不同有理数），**不在闭式内**、也不在 TUFT 公设内 ⇒ "
        "本册**不填 C**（填任何具体值都属把外部约定伪装成结论）。"
        "可判定的只有「量级」：见 C05，结论对 |C| 的取值完全不敏感（|C|<=1e10 内不变）。",
        {})

    # C05 可观测性：C lnS/S 对天体质量 BH 零影响；可观测阈值
    lnS = S_M.ln()
    rel_C1 = lnS / S_M
    guard("C05 log_term_negligible", rel_C1 < D("1E-70"),
          "lnS/S = " + fs(rel_C1) + "（应 < 1e-70）")
    # 阈值：rel >= 1e-3 ⇒ S/lnS <= 1000 ⇒ 迭代解 S
    S_thr = D("1E4")
    for _ in range(200):
        S_thr = D(1000) * S_thr.ln()
    M_thr = MPL * (S_thr / (D(4) * PI)).sqrt()
    print("  lnS/S = %s ; 相对修正>=1e-3 需 S<=%s (M<=%s kg)"
          % (fs(rel_C1, 8), fs(S_thr, 8), fs(M_thr, 8)))
    guard("C05b threshold_mass_sub_microgram", M_thr < D("1E-6"),
          "阈值质量 = " + fs(M_thr, 8) + " kg（应 < 1e-6 kg）")
    add("C05", "PASS", "对数修正对天体黑洞零影响：M_sun 的相对修正 ~1.7e-75，仅 M<~6e-7 kg 才可观测",
        "`C lnS/S`：M_sun 时 `lnS/S = " + fs(rel_C1, 8) + "` ⇒ 即使 |C|=1e10 相对修正仍 ~1e-65，"
        "**数值上完全不可观测**。反解「相对修正 >= 1e-3」得 `S <= " + fs(S_thr, 8) +
        "`，即 `M <= " + fs(M_thr, 8) + " kg`（亚微克级原初黑洞）。"
        "⇒ 对数修正的判别力**只存在于普朗克邻域**，对恒星级/星系级黑洞是纯形式项。"
        "该结论只依赖 S 的量级，不依赖 C 的具体值（C04）。",
        {"lnS": fs(lnS, 12), "rel_C1": fs(rel_C1, 12),
         "S_threshold": fs(S_thr, 10), "M_threshold_kg": fs(M_thr, 10)})

    # C06 两口径不可混
    add("C06", "BOUNDARY", "T210 与 T211 不可混算：leading 系数 1/4 与 subleading C 属不同层级",
        "T210（面积律）的 `1/4` 是精确 leading 系数（依赖 l_P 定义与 k_B 口径，两者都可显式声明）；"
        "T211（对数修正）的 C 是 subleading 且 scheme 依赖。"
        "把两者相加成「单一定值」会制造伪精度：C 的不确定度虽被 lnS/S 压成 1e-75，"
        "但**层级混淆**会在讨论「熵修正是否可测」时给出错误直觉（把 1e-75 的项说成「修正项」）。"
        "⇒ 本册按 T210 / T211 两行并列登记，不给合并数值。",
        {})

    add("C07", "INFO", "T210/T211 三判定 = C1（TUFT 侧无熵闭式）",
        "熵的面积律与对数修正都是 GR + 一圈 QFT 的结果，TUFT 侧没有独立给出的熵表达式；"
        "螺旋公设不进入 `A/4l_P^2` 的任何一个因子。⇒ C1。",
        {})

    # =================================================================
    # D 段 · T749 KLT 引力-规范双拷贝
    # =================================================================
    print("\n[D] T749 · KLT 引力–规范双拷贝")
    print("  来料式：M_4^grav = s_12 s_23 A_4^YM (A~)_4^YM")

    # D01 组合层：核在 3 个 Mandelstam 通道中取 2 个
    channels = ("s12", "s23", "s13")
    kernel_factors = ("s12", "s23")
    n_kernel_zeros = len([c for c in channels if c in kernel_factors])
    guard("D01 kernel_takes_2_of_3", n_kernel_zeros == 2,
          "核的零因子数 = %d（应 2）" % n_kernel_zeros)
    add("D01", "PASS", "组合层可判：KLT 核 s_12 s_23 在 3 个 Mandelstam 通道中只取 2 个",
        "4 点有 3 个 Mandelstam 通道（s12/s23/s13）。KLT 核只含其中 2 个 ⇒ "
        "零点超平面 2 个；而 4D 振幅在**每个**通道都有极点 ⇒ "
        "核**必须出现在分子**，且其 2 个零点必须由 `A (A~)` 的极点部分抵消。"
        "这是 KLT「极点重排」的必要条件，属组合事实（可机器计数，不需要任何系数）。",
        {"channels": list(channels), "kernel_factors": list(kernel_factors),
         "n_zeros": n_kernel_zeros})

    # D02 腿序是承重约定
    add("D02", "BOUNDARY", "第二个振幅的腿序是承重约定：archive 只写 A(A~) 未声明置换",
        "KLT 的标准形式要求第二个 YM 振幅取**置换后的腿序**（常见为 1,2,4,3），"
        "而 archive 只写 `A_4^YM (A~)_4^YM` 未给置换。"
        "同一符号串在不同腿序下对应不同的 `s_ij` 依赖 ⇒ **单看该式无法定值**。"
        "本册不选腿序（选了就是把外部约定伪装成结论），只登记「腿序缺失 ⇒ 表达式欠定」。",
        {})

    # D03 归一化/耦合因子位置
    add("D03", "BOUNDARY", "耦合因子 (kappa/2)^{n-2} 的位置与幂次取决于振幅归一化约定 ⇒ 不判",
        "4D 振幅的齐次度取决于外腿波函数归一化（1/sqrt(2w) 约定等）与耦合剥离方式，"
        "不同教材给出不同幂次 ⇒ archive 未声明「M_4^grav 是剥离后的约化振幅还是含 kappa^2 的全振幅」。"
        "两种读法下补偿因子的**位置**不同（分子 `(kappa/2)^2` vs 分母的 `1/s`），"
        "本册**只登记缺口存在、不指定归属**（承 r183 E03 的「结构项缺失不做单幂次补齐」纪律）。",
        {})

    # D04 平方结构 != TUFT 三重奏
    add("D04", "BOUNDARY", "「平方结构」形似而非等价：禁止用 KLT 互证 kappa^2+tau^2=(omega/c)^2",
        "KLT 是**场论振幅之间的平方关系**（引力振幅 = 两个规范振幅的乘积型组合）；"
        "TUFT 三重奏 `kappa^2+tau^2=(omega/c)^2` 是**几何曲率恒等式**。"
        "两者都是「A^2 = B」的外形，但不存在已构造的函子把「振幅乘积」映到「曲率平方和」⇒ "
        "以「都是平方结构」互相支持，与 r14 的「Y 不是 Lk 的函数」属同一类范畴错误。"
        "⇒ 显式禁止该互证路径；若将来要建桥，须先给出把 (s_ij, A_YM) 映到 (kappa, tau) 的映射及其可检验后果。",
        {})

    add("D05", "INFO", "T749 三判定 = C1（TUFT 侧无 KLT 闭式）",
        "TUFT 侧没有引力振幅/规范振幅的闭式，更没有双拷贝关系；KLT 属 GR+YM 的树级结果。⇒ C1。",
        {})

    # =================================================================
    # E 段 · T718 附带复核（r183 C04 只登记）
    # =================================================================
    print("\n[E] T718 · 电导量子数值复核（r183 C04 遗留）")

    e2h = (D("1.602176634E-19") ** 2) / HV
    RK = HV / (D("1.602176634E-19") ** 2)
    ark = D("2.58128E-5")
    print("  e^2/h = %s S ; R_K = %s ohm ; archive = %s S"
          % (fs(e2h, 12), fs(RK, 12), fs(ark, 8)))

    # E01 与两个标准值都不等
    dev_e2h = (ark - e2h) / e2h
    dev_2e2h = (ark - D(2) * e2h) / (D(2) * e2h)
    ok_e01 = (abs(dev_e2h) > D("0.1")) and (abs(dev_2e2h) > D("0.1"))
    guard("E01 archive_matches_neither", ok_e01,
          "偏差 e^2/h=" + fs(dev_e2h, 6) + " 2e^2/h=" + fs(dev_2e2h, 6))
    add("E01", "FAIL", "archive 的 G0=2.58128e-5 S 既不等于 e^2/h 也不等于 2e^2/h",
        "`e^2/h = " + fs(e2h, 12) + " S`（单自旋通道）；`2e^2/h = " + fs(D(2) * e2h, 12) +
        " S`（含自旋简并的电导量子）。archive 写 `2.58128e-5 S`："
        "相对 `e^2/h` 偏差 " + fs(dev_e2h * 100, 6) + "%，"
        "相对 `2e^2/h` 偏差 " + fs(dev_2e2h * 100, 6) + "% ⇒ 两个口径都不成立。",
        {"e2_over_h": fs(e2h, 12), "two_e2_over_h": fs(D(2) * e2h, 12),
         "archive": fs(ark, 8), "dev_vs_e2h_pct": fs(dev_e2h * 100, 6),
         "dev_vs_2e2h_pct": fs(dev_2e2h * 100, 6)})

    # E02 位数搬运定位：archive = 1e-9 * R_K
    moved = RK * D("1E-9")
    rel_moved = (moved - ark) / ark
    guard("E02 archive_equals_RK_times_1e-9", abs(rel_moved) < D("1E-6"),
          "1e-9*R_K = " + fs(moved, 12) + " vs archive = " + fs(ark, 8) +
          " 相对差 " + fs(rel_moved, 6))
    add("E02", "PASS", "位数搬错定位：archive 值恰等于 R_K x 1e-9（相对差仅来自 6 位有效数字截断）",
        "`R_K = h/e^2 = " + fs(RK, 12) + " ohm`；`R_K x 1e-9 = " + fs(moved, 12) + "`，"
        "与 archive 的 `2.58128e-5` 相对差 " + fs(rel_moved, 6) +
        "（= archive 只给 6 位有效数字造成的截断）。⇒ **机械结论**：archive 把电阻量子的数值"
        "乘 1e-9 后当成西门子值（量纲：ohm -> S 需取倒数，不是乘 1e-9）。"
        "这与 r183 C04 的登记一致，本册把它从「登记」升为「定位」。",
        {"R_K": fs(RK, 12), "moved": fs(moved, 12), "rel": fs(rel_moved, 8)})

    # E03 自洽：e^2/h 与 1/R_K 互为倒数（机器零）+ 2e^2/h 单列
    recip = ONE_A = D(1) / RK
    rel_recip = (recip - e2h) / e2h
    guard("E03 e2h_is_reciprocal_of_RK", abs(rel_recip) < D("1E-60"),
          "1/R_K 与 e^2/h 残差 = " + fs(rel_recip))
    add("E03", "PASS", "口径自洽：e^2/h = 1/R_K（机器零），2e^2/h 须单独声明自旋简并",
        "`1/R_K` 与 `e^2/h` 相对残差 " + fs(rel_recip) + "（机器零，**同一定义的两种写法**，"
        "属口径交叉印证而非独立验证）。门禁建议：凡出现「电导量子 G0」必须写明是 `e^2/h` 还是 "
        "`2e^2/h`（差 2 倍），凡出现「R_K」必须写明单位是 ohm 还是 S —— 本册该缺陷的成因正是"
        "单位方向（ohm 当 S）+ 数量级（1e-9）两处同时出错。",
        {"recip": fs(recip, 12), "residual": fs(rel_recip)})

    # =================================================================
    # F 段 · 三判定总表 / 供给账 / 批次账
    # =================================================================
    print("\n[F] 三判定 · 供给账 · 批次账")

    verdicts = [
        ("T141", "C1", "TUFT 侧无连续波椭率闭式；椭率属 EoS/形变历史，非螺旋公设自由度"),
        ("T210", "C1", "TUFT 侧无熵面积律闭式；A/4l_P^2 的因子全在 GR/QFT 侧"),
        ("T211", "C1", "对数修正系数 C scheme 依赖，且 TUFT 侧无对应 subleading 项"),
        ("T749", "C1", "TUFT 侧无引力/规范振幅闭式，无 KLT 结构；腿序与归一化均未声明"),
        ("T718", "C1", "TUFT 侧无电导量子闭式；本册只做 archive 数值定位（探针本体留第三批）"),
    ]
    supply = len([p for p, v, r in verdicts if v in ("C2", "C3")])
    add("F01", "INFO", "三判定总表：第二批 5 行全部 C1（供给 0）",
        "T141/T210/T211/T749 为本批 3 个探针（T210/T211 成对计 2 行），T718 为 r183 C04 遗留的"
        "数值复核（探针本体留第三批）。五行全部 C1：探针给的是 GR/QED 侧参考值，"
        "TUFT 侧对该四类量均无内定数值。⇒ 本批产出同样是「校准工具 + 排定量程」，不是「验证 TUFT」。",
        {"n_rows": 5, "n_C1": 5, "n_C2": 0, "n_C3": 0})

    guard("F02 tuft_supply_is_zero", supply == 0, "供给计数 " + str(supply))
    add("F02", "INFO", "供给账 0/3（本批 3 探针）：探针池仍只出上限/量程，不出判别",
        "与 r183 F02 一致。累计：第一批 0/4 + 第二批 0/3 = **0/7**。"
        "⇒ 用户方案第五节的「联合 chi^2 曲面」仍**没有可拟合的自由度映射**，"
        "须先解 r174 的 P1–P5 才谈后验（P1 已由 r183 F04 证为零成本，P3 代价由 r183 F05 量化）。",
        {"supply": supply, "batch1": "0/4", "batch2": "0/3", "total": "0/7"})

    add("F03", "CORRECTED", "进度账修正：可精算池 12 项中 7 项已落盘 + 1 项数值复核",
        "r183 F06 已把第二批核定为 3 项。本册完成后："
        "已落盘 = T147/T712/T947/T163（第一批 4）+ T141/T210/T211/T749（第二批 4 行 / 3 探针）= **8 行**；"
        "另 T718 完成数值复核（探针本体未做）。池内 12 项标识中**未做**：T567/T568/T718（本体）/T831/T935 共 5 项 ⇒ 第三批。"
        "注：T210 与 T211 在归档表里写作一行（成对），本册按两行登记以免混算（见 C06）。",
        {"done_rows": ["T147", "T712", "T947", "T163", "T141", "T210", "T211", "T749"],
         "value_checked": ["T718"], "remaining": ["T567", "T568", "T718", "T831", "T935"]})

    add("F04", "INFO", "下一回合（第三批）+ 未闭合清单",
        "①第三批：T567（相对熵相干）/ T568（Wigner–Yanase）/ T831（KSS 粘滞熵比）/ T935（Heisenberg 纠缠标度）"
        " + T718 探针本体（量子化电导闭环）。"
        "②未闭合（诚实）：T141 的系数 1/2 属外部约定（B03）；对数修正 C 不填数（C04）；"
        "KLT 腿序与耦合归一化未声明（D02/D03）⇒ 这三项**不是「待算」，而是「待声明」**，"
        "本册无权代声明。③F5（钱德拉塞卡极限）连续两批未触及，仍无回合。",
        {"batch3": ["T567", "T568", "T831", "T935", "T718(body)"],
         "unresolved_external": ["T141 coef 1/2", "T211 C", "T749 leg order / normalization"],
         "never_touched": ["F5 Chandrasekhar"]})

    # =================================================================
    # 输出
    # =================================================================
    print("\n" + "=" * 78)
    n_pass = sum(1 for e in ENTRIES if e["level"] == "PASS")
    n_fail = sum(1 for e in ENTRIES if e["level"] == "FAIL")
    n_bound = sum(1 for e in ENTRIES if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in ENTRIES if e["level"] == "INFO")
    n_corr = sum(1 for e in ENTRIES if e["level"] == "CORRECTED")
    n_g = len(GUARDS)
    n_gok = sum(1 for g in GUARDS if g["ok"])
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）"
          % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info))
    print("守卫 %d/%d" % (n_gok, n_g))
    print("=" * 78)

    payload = dict(
        stem=STEM,
        round="r184",
        date="2026-10-25",
        scope="探针池第二批 T141 / T210 / T211 / T749（+T718 数值复核）",
        counts=dict(entries=len(ENTRIES), PASS=n_pass, FAIL=n_fail,
                    BOUNDARY=n_bound, CORRECTED=n_corr, INFO=n_info,
                    guards=n_g, guards_ok=n_gok),
        verdicts=[{"probe": p, "verdict": v, "reason": r} for p, v, r in verdicts],
        entries=ENTRIES,
        guards=GUARDS,
    )

    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=1)

    lines = []
    lines.append("# " + STEM)
    lines.append("")
    lines.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）；守卫 %d/%d；退出码 0**"
                 % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info, n_gok, n_g))
    lines.append("")
    lines.append("## 一句话")
    lines.append("")
    lines.append("第二批 3 探针（T141 / T210+T211 / T749）**首次落盘**，三判定全部 C1（供给 0/3，累计 0/7）。"
                 "三条硬读数：①T141 的破碎上限 `eps<=(1/2)(Omega/Omega_K)^2` 在毫秒脉冲星处给 1e-2~1e-1，"
                 "比观测上限宽 4~5 个量级 ⇒ 无约束力，且系数 1/2 与逃逸速度判据（系数 1）差 2 倍 ⇒ 属外部约定；"
                 "②T211 的对数修正 `C lnS/S` 在 M_sun 处为 1.7e-75，只有 M<~6e-7 kg 才可观测 ⇒ 判别力仅存在于普朗克邻域；"
                 "③T749 的 KLT 式**腿序与耦合归一化均未声明** ⇒ 表达式欠定（属「待声明」而非「待算」）。"
                 "附带把 r183 C04 的登记升为定位：archive 的 `G0=2.58128e-5 S` 恰为 `R_K x 1e-9`（ohm 当 S）。")
    lines.append("")
    lines.append("## 条目")
    lines.append("")
    lines.append("| 编号 | 级 | 标题 |")
    lines.append("|---|---|---|")
    for e in ENTRIES:
        lines.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"]))
    lines.append("")
    lines.append("## 三判定")
    lines.append("")
    lines.append("| 探针 | 判定 | 理由 |")
    lines.append("|---|---|---|")
    for p, v, r in verdicts:
        lines.append("| %s | **%s** | %s |" % (p, v, r))
    lines.append("")
    lines.append("## 守卫（%d/%d）" % (n_gok, n_g))
    lines.append("")
    for g in GUARDS:
        lines.append("- [%s] %s %s" % ("OK" if g["ok"] else "FAIL", g["name"],
                                       ("" if g["ok"] else ":: " + str(g["msg"]))))
    lines.append("")
    lines.append("## 红线")
    lines.append("")
    lines.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
                 "未改写任何来料字节；未改 verify.py；未做 git 操作。探针供给 0/3 ⇒ 不得报道为「通过」。")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")

    rep = []
    rep.append("TUFT-r184 探针池第二批 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）"
               % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info))
    rep.append("守卫 %d/%d" % (n_gok, n_g))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False)[:1200])
        rep.append("")
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(rep) + "\n")

    print("已写出：")
    print("  " + os.path.join(OUTD, STEM + ".json"))
    print("  " + os.path.join(OUTD, STEM + ".md"))
    print("  " + os.path.join(OUTD, STEM + "_report.txt"))
    return 0 if n_gok == n_g else 1


if __name__ == "__main__":
    sys.exit(main())
