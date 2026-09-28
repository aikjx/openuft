# -*- coding: utf-8 -*-
"""
==================================================================================
TUFT v59 阻尼时间 tau 独立合并似然：第二预言 tau_TUFT/tau_GR=1.576 (+57.6%)
==================================================================================

纪律（与 v56/v57/v58 同源）：
- 数值全部来自公开发表值 + qnm/Berti (2,2,0) Kerr 表，硬编码照抄；不 import v56/v57/v58。
- 残差高斯、独立；H0: tau=GR (d_tau=0) vs H1: tau=1.576 tau_GR (d_tau=+57.6%)。
- 两套并列不混用：(A) 朴素归算残差 tau_obs vs tau_GR(Mf,chif)；(B) 已发表边际化 d_tau220。
- 90% CI -> 1sigma：sigma = (high90-low90)/(2*1.645)。
- 禁伪闭合、禁 cherry-pick、不夸大方差挽救理论。

TUFT 阻尼预言（SSOT v7.0 照抄）：
  Grade-A w = 0.434445178 - 0.056449760 i ; GR w = 0.3736716844 - 0.088962316 i (a=0)
  tau = M/|w_I| (几何单位) -> tau_TUFT/tau_GR = |w_I,GR|/|w_I,TUFT|
      = 0.088962316/0.056449760 = 1.57596 = +57.60%
  (阻尼率 gamma=1/tau 因此低 36.55%；Q_TUFT=3.848 vs Q_GR=2.100 @a=0)
  GR n0 阻尼随自旋 a 变化（Kerr 共转 (2,2,0)），按各事件 Mf/chif 折算。

来源：
  Estelles et al. 2023 CQG (arXiv:2104.01906) Table 2: tau220 中值 + 90% CI（6 事件，与 v56 同事件集）；
  同文献 Eq.(13)/(15) 已发表边际化 d_tau220 后验（正确计入 Mf-chif-d_tau 简并）。
  Kerr (2,2,0) w_I(chif)：qnm 包（Cook-Zalutskiy 谱 + Leaver 求根，= Bertti 表金标准），
      a=0 锚 w_I=0.0889623 与 v57 独立 Leaver 14.8 位复算一致。
"""
import math

# ------------------------------------------------------------------
# 常数
# ------------------------------------------------------------------
Z90 = 1.645
GM_SUN_c3_US = 4.92549       # microseconds
GM_SUN_c3_MS = GM_SUN_c3_US * 1e-3   # ms per (M_sun * tau in geometric M)
TUFT_WI_GR = 0.088962316     # a=0 GR n0 damping (v57 anchor)
TUFT_WI = 0.056449760        # Grade-A TUFT n0 damping
TUFT_TAU_RATIO = TUFT_WI_GR / TUFT_WI           # = 1.57596
TUFT_DTAU = (TUFT_TAU_RATIO - 1.0) * 100.0      # = +57.60 %

# 任务3b：最乐观 c_m 端。SSOT 只 tabulate 频率灵敏边 [+8.82%,+21.17%]，
# 未列阻尼灵敏带。频率下边对应 c_m 最不负（最靠近 GR），此时阻尼增强亦最小。
# 透明 pro-TUFT 估计：名义频移 +16.26% -> 下边 +8.82%（比值 1.0882/1.1626=0.936）；
# 同比例把 tau 比 1.576 向 GR 收缩：1.576*0.936=1.475 -> d_tau_opt≈+47.5%。
# 此为"对 TUFT 最宽容"的下界，非 Grade-A 数；结论若连它都排除则稳健。
FREQ_LOW_RATIO = 1.0882/1.1626
OPT_DTAU = (TUFT_TAU_RATIO*FREQ_LOW_RATIO - 1.0)*100.0   # ~ +47.5 %

# ------------------------------------------------------------------
# Kerr (2,2,0) |w_I|(chi)  (qnm / Bertti 表，s=-2,l=2,m=2,n=0)
# a=0 锚 0.0889623 与 v57 独立复算一致。
# ------------------------------------------------------------------
WI_TABLE = {
    0.65: 0.0824618,
    0.67: 0.0818452,
    0.70: 0.0807929,
    0.74: 0.0790927,
    0.78: 0.0769364,
}

# ------------------------------------------------------------------
# 任务1：观测数据（Estelles 2023 Table 2，照抄；与 v56 同 6 事件集）
# (name, Mf_IMR, chif_IMR, tau_obs_ms, tau_hi90_ms, tau_lo90_ms)
# ------------------------------------------------------------------
EVENTS = [
    # name,                 Mf,    chi,  tau_obs, +hi90, -lo90
    ("GW150914",           67.3,  0.67,  4.49,   1.09,  0.95),
    ("GW170104",           56.9,  0.65,  5.53,   3.47,  2.40),
    ("GW190519_153544",    144.1, 0.78, 10.33,   3.56,  3.07),
    ("GW190521_074359",    87.1,  0.70,  5.32,   1.48,  1.21),
    ("GW190630_185205",    66.2,  0.70,  3.87,   2.37,  1.80),
    ("GW190828_063405",    75.8,  0.74,  4.23,   4.17,  1.92),
]

# (B) 已发表边际化 d_tau220 后验（Estelles Eq.13 / Eq.15，正确计入简并）
# (name, d_med %, d_lo90 %, d_hi90 %)  90% band = [med+lo, med+hi]
MARG_SINGLE = [
    ("GW150914_marg",        7.0,  -23.0,  26.0),   # 0.07 +0.26/-0.23 -> band[-16,+33]
]
MARG_JOINT = [
    ("sixevent_joint",      10.0,  -14.0,  14.0),   # 0.10 +0.14/-0.14 -> band[-4,+24]
]


def tau_gr_ms(mf, chi):
    """GR 标称 tau = Mf/|w_I(chi)| in ms = Mf*GM_sun/c^3 / |w_I|."""
    return mf * GM_SUN_c3_MS / WI_TABLE[chi]


def sigma_from_band(low90, high90):
    return (high90 - low90) / (2.0 * Z90)


# ------------------------------------------------------------------
# 任务2：朴素残差表
# ------------------------------------------------------------------
def naive_rows():
    rows = []
    for name, mf, chi, tobs, thi, tlo in EVENTS:
        tgr = tau_gr_ms(mf, chi)
        d = (tobs/tgr - 1.0)*100.0
        # fractional uncertainty on tau_obs -> fractional residual band
        err_hi = thi/tobs*100.0
        err_lo = tlo/tobs*100.0
        band_lo = d - err_lo
        band_hi = d + err_hi
        rows.append((name, mf, chi, tgr, tobs, d, band_lo, band_hi))
    return rows


def combined_gauss(rows_ds, delta_h):
    """rows_ds: [(name, d_obs%, low90%, high90%)]; delta_h: H1 d_tau in %."""
    rows = [(n, d, sigma_from_band(lo, hi)) for n, d, lo, hi in rows_ds]
    P = sum(1.0/(s*s) for _, _, s in rows)
    d_hat = sum(d/(s*s) for _, d, s in rows)/P
    sig = 1.0/math.sqrt(P)
    lnL0 = -0.5*sum((d/s)**2 for _, d, s in rows)
    lnL1 = -0.5*sum(((d-delta_h)/s)**2 for _, d, s in rows)
    dl = lnL1 - lnL0
    bf = math.exp(dl)
    db = 10.0*math.log10(bf) if bf > 0 else float("-inf")
    n_excl = (d_hat - delta_h)/sig   # 负=H1 在 d_hat 上方被压
    return {"n": len(rows), "d_hat": d_hat, "sig": sig, "lnL0": lnL0, "lnL1": lnL1,
            "dl": dl, "BF": bf, "dB": db, "n_excl": n_excl, "rows": rows}


def inflate(rows_ds, f=1.5):
    out = []
    for n, d, lo, hi in rows_ds:
        h = (hi-lo)/2.0
        out.append((n, d, d-f*h, d+f*h))
    return out


# ==================================================================
lines = []
def p(s=""):
    lines.append(s); print(s)

p("="*82)
p("TUFT v59 阻尼时间 tau 独立合并似然：第二预言 tau_TUFT/tau_GR=1.576 (+57.6%)")
p("="*82)
p(f"Grade-A w_TUFT=0.434445178-0.056449760i ; w_GR(a=0)=0.3736716844-0.088962316i")
p(f"tau_TUFT/tau_GR = |w_I,GR|/|w_I,TUFT| = 0.088962316/0.056449760 = {TUFT_TAU_RATIO:.5f}")
p(f"                                              -> H1 d_tau = +{TUFT_DTAU:.2f}% (阻尼率低 36.55%)")
p("假设：残差高斯、独立；H0: d_tau=0 (GR) vs H1: d_tau=+57.6% (TUFT)。")
p("90% CI->1sigma: sigma=(hi-lo)/(2*1.645)。BF=exp(ΔlnL)；dB=10log10(BF)。")
p("")

# ---- 任务1/2 数据表 ----
p("[任务1+2] 各事件 tau 观测 / GR 归算 / 朴素残差（Estelles 2023 Table 2）")
p("-"*82)
p(f"{'event':<22}{'Mf':>6}{'chi':>6}{'tau_GR':>9}{'tau_obs':>9}{'d_tau':>9}  90%残差带")
naive = naive_rows()
NAIVE_DS = []
for name, mf, chi, tgr, tobs, d, blo, bhi in naive:
    p(f"{name:<22}{mf:>6.1f}{chi:>6.2f}{tgr:>8.3f}ms{tobs:>8.2f}ms{d:>+8.1f}%  [{blo:>+7.1f}%,{bhi:>+7.1f}%]")
    NAIVE_DS.append((name, d, blo, bhi))
p("")
p("(B) 已发表边际化 d_tau220（Estelles Eq.13/15，正确计入 Mf-chi-dtau 简并；与 A 并列不混用）")
for n, d, lo, hi in MARG_SINGLE:
    p(f"  {n:<22} med={d:+.1f}%  90%band=[{d+lo:+.1f}%,{d+hi:+.1f}%]")
for n, d, lo, hi in MARG_JOINT:
    p(f"  {n:<22} med={d:+.1f}%  90%band=[{d+lo:+.1f}%,{d+hi:+.1f}%]  [hierarchical/同d_tau联合；含GW150914]")
p("")

# ---- 任务3 合并似然 ----
p("[任务3] 合并对数似然比 / BF / dB（H1 = TUFT 标称 +%.2f%%）" % TUFT_DTAU)
p("-"*82)
sets = [
    ("朴素 6 事件集（含 GW190828）", NAIVE_DS),
    ("朴素 5 事件集（剔 GW190828）", [e for e in NAIVE_DS if not e[0].startswith("GW190828")]),
    ("边际化 GW150914 单事件",      MARG_SINGLE),
    ("边际化 六事件联合",            MARG_JOINT),
]
res = {}
for label, ev in sets:
    R = combined_gauss(ev, TUFT_DTAU)
    res[label] = R
    p(f"")
    p(f"  集 = {label}  (n={R['n']})")
    p(f"    d_hat     = {R['d_hat']:+.3f}%")
    p(f"    1sigma    = {R['sig']:.3f}%")
    p(f"    lnL(H0=GR)= {R['lnL0']:+.4f}")
    p(f"    lnL(H1=+{TUFT_DTAU:.1f}%)= {R['lnL1']:+.4f}")
    p(f"    dlnL      = {R['dl']:+.4f}")
    p(f"    BF(H1/H0) = {R['BF']:.4e}")
    verdict = "H1(TUFT)偏好" if R['dl'] > 0 else "H0(GR)偏好"
    p(f"    dB        = {R['dB']:+.3f} dB  ->  {verdict}")
    p(f"    H1 被排除 nsigma = {R['n_excl']:+.3f}  (负=H1 在 d_hat 上方被压)")

# ---- 3a 保守放大 x1.5 ----
p("")
p("[任务3a] 保守误差放大：1sigma x1.5 重算")
p("-"*82)
for label, ev in sets:
    R = combined_gauss(inflate(ev, 1.5), TUFT_DTAU)
    p(f"  {label:<38} dlnL={R['dl']:+8.3f}  dB={R['dB']:+7.3f}  n_excl={R['n_excl']:+6.3f}  ({'GR' if R['dl']<0 else 'TUFT'}偏好)")

# ---- 3b 最乐观 c_m 端 ----
p("")
p(f"[任务3b] 最乐观 c_m 端：取离数据最近的 tau 比 -> d_tau_opt=+{OPT_DTAU:.2f}%")
p("-"*82)
p(f"  (SSOT 未 tabulate 阻尼灵敏带；按频率下边 c_m 同比例向 GR 收缩 tau 比，pro-TUFT 透明估计)")
for label, ev in sets:
    R = combined_gauss(ev, OPT_DTAU)
    p(f"  {label:<38} dlnL={R['dl']:+8.3f}  BF={R['BF']:.3e}  dB={R['dB']:+7.3f}  n_excl={R['n_excl']:+6.3f}  ({'GR' if R['dl']<0 else 'TUFT'}偏好)")

# ---- 3c H1 标称排除 nsigma ----
p("")
p("[任务3c] H1=TUFT 标称 +%.2f%% 被排除的显著性" % TUFT_DTAU)
p("-"*82)
for label, ev in sets:
    R = combined_gauss(ev, TUFT_DTAU)
    p(f"  {label:<38} d_hat={R['d_hat']:+6.2f}% ±{R['sig']:5.2f}%  H1=+{TUFT_DTAU:.1f}% 距 d_hat={TUFT_DTAU-R['d_hat']:6.2f}% = {abs(R['n_excl']):5.2f}sigma")

# ---- 任务4 分级摘要 ----
p("")
p("="*82)
p("[任务4] 诚实分级摘要")
p("="*82)
for label in ["朴素 6 事件集（含 GW190828）", "朴素 5 事件集（剔 GW190828）", "边际化 六事件联合"]:
    R = res[label]
    p(f"{label:<34} dB={R['dB']:+.1f}  H1 标称排除 {abs(R['n_excl']):.2f}sigma")
Rg = res["边际化 GW150914 单事件"]
p(f"{'边际化 GW150914 单事件':<34} dB={Rg['dB']:+.1f}  H1 标称排除 {abs(Rg['n_excl']):.2f}sigma")
p("")
p("诚实标注：仅 n0 单模；朴素残差固定 Mf/chi（乐观排除上限），最干净=边际化联合；")
p("c_m 阻尼灵敏带 SSOT 未 tabulate，3b 为 pro-TUFT 透明收缩估计，不夸大方差挽救理论。")

with open(r"D:\a10\aikjx\code\my_lib\_audit_v59_damping_likelihood_out.txt",
          "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
