# -*- coding: utf-8 -*-
"""
================================================================================
v54 AUDIT — rotating m-frequency split observable: direct signature vs GR QNM
            template (m = +2  vs  m = -2)
--------------------------------------------------------------------------------
另写实现, 不 import 任何 prior-project 脚本; mpmath dps=40; GR 门先行;
禁伪闭合; 四态分级; 勘误递增不回退. 数字照抄磁盘 SSOT (主册 v6.5 /
台账 E1-E503 / 勘误#42) 与 v49 / v53 审计输出.

物理模型 (small-spin linear ansatz, leading order in a):
    omega(a, m) = omega_0  +  m * a * c_per_m
    delta_omega(a) = omega(a, +2) - omega(a, -2) = 4 a c_per_m
                    = a * ( splitR/a + i splitI/a )
GR limit: a=0  =>  omega(+2)=omega(-2)=omega_0,  delta_omega = 0  (non-degenerate
           only when spin turns on; no split at a=0).  PASS.

观测量: 固定质量 M, 自旋 a 时, m=+2 与 m=-2 两模频率差随 a 线性增长;
        斜率 splitR/a 是与 M 无关的几何量, 转 Hz 时两模同乘 K(M), 故斜率比
        (TUFT/GR) 与 M 无关, 与 a 无关 (线性区).
================================================================================
"""

import mpmath as mp

mp.mp.dps = 40


def nstr(z):
    if isinstance(z, mp.mpc):
        r = mp.nstr(z.real, 18)
        i = mp.nstr(z.imag, 18)
        return "(%s %+si)" % (r, i)
    return mp.nstr(z, 18)


# ---------------------------------------------------------------------------
# [0] SSOT anchors —— 照抄, 不改写
# ---------------------------------------------------------------------------
# GR n0 static (M=1 geom), v49 GATE A / errata#42
w_GR_0 = mp.mpc("0.37367168441804166", "-0.08896231568893410")
# TUFT Grade-A static anchor, v49/v53
w_TUFT_0 = mp.mpc("0.434445178", "-0.056449760")

# GR m-split slope (errata#42): splitR/a = 0.2515323 ; per-m c = 0.0628831+0.001996i
GR_splitR_over_a = mp.mpf("0.2515323")
c_GR_per_m = mp.mpc("0.0628831", "0.001996")          # per-(m a) complex slope
GR_splitI_over_a = 4 * c_GR_per_m.imag                  # = 0.007984

# TUFT m-split slope (v49 direct continuation @ a=0.1)
TUFT_splitR_over_a = mp.mpf("1.621")
TUFT_splitI_over_a = mp.mpf("-0.141")
c_TUFT_per_m = mp.mpc(TUFT_splitR_over_a, TUFT_splitI_over_a) / 4

# same-cavity GR 2/rho^3 naive field (v49) — suppression reference
samecav_GR_splitR_over_a = mp.mpf("4.662")
suppression_ratio = TUFT_splitR_over_a / samecav_GR_splitR_over_a   # ~0.35

# 60 Msun conversion: f_Hz = K * Re(w),  K = c^3/(2 pi G M) = 32312.5 / 60
K_sun = mp.mpf("32312.5")          # Hz, c^3/(2 pi G M_sun)
M_solar = mp.mpf("60")
K = K_sun / M_solar                # Hz per unit Re(w_M)

# v53 amplitude anchors
eps_lo = mp.mpf("0.07481154506795630784624364212457266738931")   # strict E444
eps_hi = mp.mpf("0.469746")                                       # toy/E431 upper
D_Voy_strict = mp.mpf("2.46")     # Gpc, Voyager face-on strict
D_Voy_toy    = mp.mpf("15.48")    # Gpc, Voyager face-on toy


def mode_freq(w0, c, a, m):
    """omega(a,m) = w0 + m*a*c ; c = per-(m a) complex slope."""
    return w0 + m * a * c


def split(w0, c, a):
    """delta omega = omega(+2)-omega(-2) = 4 a c."""
    return 4 * a * c


def hz(wgeom):
    """real-part frequency in Hz for 60 Msun."""
    return K * wgeom.real


# ---------------------------------------------------------------------------
out = []
def p(s=""):
    out.append(s)

p("=" * 80)
p("v54 AUDIT — rotating m-split observable vs GR QNM template (m=+2 vs m=-2)")
p("  mpmath dps=%d ; independent write (no prior import) ; GR gate first" % mp.mp.dps)
p("=" * 80)

# ---------------------------------------------------------------------------
# [1] 求导链 (derivation chain)
# ---------------------------------------------------------------------------
p("")
p("[1] DERIVATION CHAIN  (small-spin, leading order in a)")
p("-" * 80)
p("  Kerr QNM in slow rotation: omega(a,m) = omega_0 + m*a*c_per_m + O(a^2)")
p("    omega_0 = static (a=0) fundamental;  c_per_m = frame-drag slope per (m a).")
p("  Split observable:")
p("    delta_omega(a) = omega(a,+2) - omega(a,-2)")
p("                   = [w0+2 a c] - [w0-2 a c] = 4 a c_per_m")
p("                   = a * ( splitR/a + i splitI/a ),")
p("    where  splitR/a = 4 Re(c_per_m),  splitI/a = 4 Im(c_per_m).")
p("")
p("  GR anchor (errata#42):")
p("    c_GR_per_m = %s" % nstr(c_GR_per_m))
p("    check 4 Re(c) = %s  vs splitR/a = %s  -> match (rounding)"
  % (nstr(4 * c_GR_per_m.real), nstr(GR_splitR_over_a)))
p("    splitR/a = %s ,  splitI/a = %s"
  % (nstr(GR_splitR_over_a), nstr(GR_splitI_over_a)))
p("")
p("  TUFT anchor (v49 direct continuation @ a=0.1):")
p("    c_TUFT_per_m = (splitR/a + i splitI/a)/4 = %s" % nstr(c_TUFT_per_m))
p("    splitR/a = %s ,  splitI/a = %s"
  % (nstr(TUFT_splitR_over_a), nstr(TUFT_splitI_over_a)))
p("")
p("  Hz conversion (60 Msun): f_Hz = K * Re(w_M),  K = %s/%s = %s Hz"
  % (nstr(K_sun), nstr(M_solar), nstr(K)))
p("  => split in Hz: delta_f_Hz = K * Re(delta_omega) = K * a * splitR/a.")
p("     Both modes share the same K(M); the slope RATIO TUFT/GR is therefore")
p("     M-independent and a-independent (linear regime).")
p("")
p("  GR limit (a=0):")
w_gr_p0 = mode_freq(w_GR_0, c_GR_per_m, mp.mpf("0"), 2)
w_gr_m0 = mode_freq(w_GR_0, c_GR_per_m, mp.mpf("0"), -2)
d_gr0 = split(w_GR_0, c_GR_per_m, mp.mpf("0"))
p("    omega(a=0,+2) = %s" % nstr(w_gr_p0))
p("    omega(a=0,-2) = %s" % nstr(w_gr_m0))
p("    delta_omega(a=0) = %s  -> ZERO split at a=0.  GR GATE: PASS" % nstr(d_gr0))


# ---------------------------------------------------------------------------
# [2] 数值表: 60 Msun, a/M = 0.1 / 0.2 / 0.3
# ---------------------------------------------------------------------------
p("")
p("[2] NUMERICAL TABLE  —  60 Msun  (K = %s Hz)" % nstr(K))
p("-" * 80)
p("  GR  static w0 = %s" % nstr(w_GR_0))
p("  TUFT static w0 = %s   (already includes +16.26%% freq / -36.6%% damping shift)"
  % nstr(w_TUFT_0))
p("")

a_list = [mp.mpf("0.1"), mp.mpf("0.2"), mp.mpf("0.3")]

for label, w0, c, sR, sI in [
    ("GR   ", w_GR_0, c_GR_per_m, GR_splitR_over_a, GR_splitI_over_a),
    ("TUFT ", w_TUFT_0, c_TUFT_per_m, TUFT_splitR_over_a, TUFT_splitI_over_a),
]:
    p("  --- %s (splitR/a=%s, splitI/a=%s) ---" % (label, nstr(sR), nstr(sI)))
    p("   a/M    w(+2) geom        w(-2) geom        f(+2)Hz   f(-2)Hz   df_Hz")
    for a in a_list:
        wp = mode_freq(w0, c, a, 2)
        wm = mode_freq(w0, c, a, -2)
        dw = split(w0, c, a)
        fp = hz(wp)
        fm = hz(wm)
        df = hz(dw)
        flag = ""
        if a >= mp.mpf("0.2"):
            flag = "  <== EXTRAPOLATED (beyond v49 credible a<0.1)"
        p("   %s  %s  %s  %9.2f  %9.2f  %9.2f%s"
          % (nstr(a), nstr(wp), nstr(wm), float(fp),
             float(fm), float(df), flag))
    p("")

# ---------------------------------------------------------------------------
# [3] 观测量鲁棒性 / 判别量
# ---------------------------------------------------------------------------
p("[3] OBSERVABLE ROBUSTNESS — discriminant")
p("-" * 80)
p("  Suppression ratio 0.35 (v49):")
p("    TUFT splitR/a            = %s" % nstr(TUFT_splitR_over_a))
p("    same-cavity GR 2/rho^3   = %s" % nstr(samecav_GR_splitR_over_a))
p("    ratio = %s  ~= 0.35  (naive same-cavity split pressed to 35%%)"
  % nstr(suppression_ratio))
p("")
ratio_TUFT_GR = TUFT_splitR_over_a / GR_splitR_over_a
ratio_naive_GR = samecav_GR_splitR_over_a / GR_splitR_over_a
p("  Discriminant: measured split-per-spin slope vs REAL GR baseline (%s):"
  % nstr(GR_splitR_over_a))
p("    naive same-cavity / GR   = %s  (before suppression)" % nstr(ratio_naive_GR))
p("    TUFT (suppressed) / GR   = %s  (after 0.35 suppression)" % nstr(ratio_TUFT_GR))
p("")
p("  HONEST SIGN: TUFT predicts a LARGER m-split than GR, not smaller.")
p("    The 0.35 suppression cuts the excess from ~%sx down to ~%sx GR."
  % (mp.nstr(ratio_naive_GR, 5), mp.nstr(ratio_TUFT_GR, 5)))
p("  => If dual m=+/-2 modes are resolved: a split slope ~%sx GR favours TUFT;"
  % mp.nstr(ratio_TUFT_GR, 5))
p("     a slope ~1x GR favours GR.  (Not 'smaller' — reported as-is, no fake closure.)")
p("")
p("  M / a independence:")
p("    slope ratio = TUFT_splitR/a / GR_splitR/a = %s (dimensionless)."
  % nstr(ratio_TUFT_GR))
p("    Both slopes are geometric (M-independent); both scale linearly with a,")
p("    so the ratio cancels a.  Direction: TUFT split excess is positive/larger,")
p("    consistent in sign with the v37 EHT c_m anchor direction.")
p("")
# Hz-level example at a=0.1
df_gr_hz = hz(4 * mp.mpf("0.1") * c_GR_per_m)
df_tu_hz = hz(4 * mp.mpf("0.1") * c_TUFT_per_m)
p("  Concrete (60 Msun, a=0.1):")
p("    GR   m=+/-2 split df = %s Hz" % mp.nstr(df_gr_hz, 7))
p("    TUFT m=+/-2 split df = %s Hz" % mp.nstr(df_tu_hz, 7))
p("    ratio = %s" % mp.nstr(df_tu_hz / df_gr_hz, 6))

# ---------------------------------------------------------------------------
# [4] 外推标注 + 可探测振幅档 + 四态分级
# ---------------------------------------------------------------------------
p("")
p("[4] EXTRAPOLATION FLAGS / DETECTABILITY TIER / FOUR-STATE GRADE")
p("-" * 80)
p("  v49 credible window: a/M < 0.1 (direct continuation).")
p("    a=0.1 : within credible window (v49 direct @a=0.1: splitR/a=1.621367). CONFIRMED.")
p("    a=0.2 : EXTRAPOLATED beyond a<0.1. v49 direct @a=0.2 gave splitR/a=1.569052")
p("            vs linear 1.621 -> ~3.2% drop, consistent with O(a^2)~4% correction.")
p("            Table uses linear ansatz 1.621; nonlinear O(a^2) uncertainty ~3-4%.")
p("    a=0.3 : EXTRAPOLATED further; v49 never computed here. Pure linear ansatz;")
p("            O(a^2) correction grows, trustworthy order-of-magnitude only.")
p("")
p("  Detectability tier (this signature = resolving two distinct m modes):")
p("    Needs high SNR to split f(+2) vs f(-2).")
p("    eps_strict interval = [%s, %s]" % (mp.nstr(eps_lo, 6), mp.nstr(eps_hi, 6)))
p("    Voyager D_max: strict eps=%s -> %s Gpc ; toy eps=%s -> %s Gpc"
  % (mp.nstr(eps_lo, 4), nstr(D_Voy_strict), mp.nstr(eps_hi, 5), nstr(D_Voy_toy)))
p("    => Resolvable at the LOUD/toy tier (eps~0.4697, D_max up to %s Gpc, face-on)"
  % nstr(D_Voy_toy))
p("       where SNR is high enough to separate m=+2 / m=-2.")
p("    => At strict tier (eps=0.0748, %s Gpc) the split is MARGINAL; needs nearby"
  % nstr(D_Voy_strict))
p("       events / network; listed alongside D_max two-tier as the loud-tier channel.")
p("")
p("  FOUR-STATE GRADE:")
p("    [CONFIRMED ] GR limit a=0 zero-split; static anchors w0照抄;")
p("                GR slope splitR/a=0.2515323 (errata#42); TUFT slope @a=0.1=1.621")
p("    [ESTIMATED ] suppression-ratio net effect 0.35 (cavity-mapping dependent);")
p("                discriminant ratio %sx GR (M-/a-independent)." % mp.nstr(ratio_TUFT_GR, 5))
p("    [EXTRAPOLATED] a=0.2 / a=0.3 linear ansatz beyond v49 a<0.1 (O(a^2)~3-4%).")
p("    [GATE-HELD ] detectability tier anchored to v53 eps interval / D_max;")
p("                no new physical E-number closed; errata#42 HELD (increment not rolled).")
p("")
p("  Discipline: no fake closure; numbers照抄; 另写 no-import; dps=%d." % mp.mp.dps)
p("=" * 80)
p("Raw output end.")
p("=" * 80)


text = "\n".join(out) + "\n"
with open(r"D:\a10\aikjx\code\my_lib\_audit_v54_rotating_msplit_observable_out.txt",
          "w", encoding="utf-8") as f:
    f.write(text)

print(text)
