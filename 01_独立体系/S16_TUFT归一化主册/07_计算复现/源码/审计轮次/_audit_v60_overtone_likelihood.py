# -*- coding: utf-8 -*-
"""
==================================================================================
TUFT v60 泛音 n=1 独立通道合并似然：基模 n0 被否后，高阶模 n=1 是否还有意外
==================================================================================

纪律（与 v56/v57/v58/v59 同源）：
- 数值全部来自已发表值 + qnm(0.4.4)/Berti (2,2,1) Kerr 表硬编码；不 import v56/v57/v58/v59。
- 残差高斯、独立；频率通道 H0: δf=0(GR) vs H1: δf=+16.26%(TUFT, 与 n0 同比例, v32)；
  阻尼通道 H0: δτ=0(GR) vs H1: δτ=+57.6%(TUFT, τ比=1.576, 与 n0 同比例)。
- 90% CI -> 1sigma；BF=exp(dlnL)；dB=10 log10 BF。
- 禁伪闭合、禁 cherry-pick、不夸大方差挽救理论；三结局都照写。

唯一已发表 n=1 泛音直接测量（GW150914，单事件）：
  Isi et al. 2019 PRL 123 111102 (arXiv:1905.00869) 无毛发检验：
    允许第一泛音频率/阻尼自由浮动，边缘化 M_f/χ_f 后：
      δf1 = -0.05 ± 0.20  (68% 置信 -> 1sigma=20%)
      δτ1 基本未约束，区间 -0.06 ≲ δτ1 ≲ +1.00
      无毛发(δf1=δτ1=0) vs 浮动模型 Bayes 因子 = 1.75
  注：任务括号给的 arXiv:1909.06188 实为数学论文，正确编号为 arXiv:1905.00869（透明记录，不改 SSOT 数）。
  Estelles 2023 (arXiv:2104.01906) 仅测 (2,2,0)，泛音固定 GR，无 n=1 数据。
  Capano 2021 (arXiv:2105.05238) 为 GW190521 (3,3,0) 次主导模，非 n=1 泛音，不计入本通道。
  Cotesta 2020 / Finch&Moore / PRD110 L041501(2024) 争议：全边缘化后泛音证据 BF 仅 2.3±0.1 -> 探测本身不鲁棒。

GR n1 锚（qnm 0.4.4 独立复算，与 SSOT v7.1 锚 0.34671099687909240-0.27391487529119870i 吻合 12 位）：
  a=0:  M*omega_R(n1)=0.346710996879, M*|omega_I|(n1)=0.273914875291
  自旋依赖用 qnm Kerr 表插值（下表硬编码）。
"""
import math

# ------------------------------------------------------------------
# 常数
# ------------------------------------------------------------------
Z90 = 1.645
GM_SUN_c3_MS = 4.925490947e-3     # ms per (Msun * geometric M)
K_HZ_PER_MSUN = 32312.5          # Hz per dimensionless omega (c^3/2piGM_sun)

TUFT_DF = 16.26     # %  TUFT n1 频移（v32，与 n0 同比例）
TUFT_DTAU = 57.60   # %  TUFT n1 阻尼偏移（τ比=1.576，与 n0 同比例）
SENS_OPT_DF = 8.82  # % 灵敏带最下端频移（离数据最近）
FREQ_LOW_RATIO = 1.0882/1.1626
OPT_DTAU = (1.57596*FREQ_LOW_RATIO - 1.0)*100.0   # ~ +47.5 %, pro-TUFT 透明收缩

# ------------------------------------------------------------------
# Kerr (2,2,1) n=1 表（qnm 0.4.4 独立复算硬编码；a=0 锚与 SSOT 一致）
# (a/M, M*omega_R, M*|omega_I|)
# ------------------------------------------------------------------
N1_TABLE = [
    (0.00, 0.346710997, 0.273914875),
    (0.10, 0.361909677, 0.272452107),
    (0.20, 0.378976357, 0.270545605),
    (0.30, 0.398390326, 0.268048570),
    (0.40, 0.420846677, 0.264733449),
    (0.50, 0.447407037, 0.260224554),
    (0.60, 0.479806665, 0.253846865),
    (0.63, 0.491072554, 0.251396507),
    (0.65, 0.499079082, 0.249579973),
    (0.67, 0.507531920, 0.247593313),
    (0.70, 0.521160765, 0.244238316),
    (0.78, 0.564794747, 0.232183490),
    (0.80, 0.577922397, 0.228148940),
    (0.90, 0.667657551, 0.195252068),
]

def interp(table, chi, col):
    """线性插值 Kerr 表。col=1 -> omega_R; col=2 -> |omega_I|."""
    chi = float(chi)
    if chi <= table[0][0]: return table[0][col]
    if chi >= table[-1][0]: return table[-1][col]
    for k in range(len(table)-1):
        a0 = table[k][0]; a1 = table[k+1][0]
        if a0 <= chi <= a1:
            f = (chi-a0)/(a1-a0)
            return table[k][col] + f*(table[k+1][col]-table[k][col])
    return table[-1][col]

# ------------------------------------------------------------------
# 任务1：已发表泛音 n=1 数据（GW150914 单事件；Isi 2019）
# δf1 已是相对 GR Kerr 的分数偏差（Isi 边缘化 M_f/χ_f 后验），无需再朴素归算。
# 频率：δf1 = -0.05 ± 0.20 (68% 置信 = 1sigma)
# 阻尼：δτ1 未约束 [-0.06, +1.00]；无毛发 BF=1.75 略偏 GR
# ------------------------------------------------------------------
# 频率通道：(median %, 1sigma %)  —— Isi 直接报 68% 即 1sigma
FREQ = dict(med=-5.0, sig=20.0, src="Isi2019 PRL123 111102 (arXiv:1905.00869) Fig.4: δf1=-0.05±0.20 (68%)")

# 阻尼通道：发表区间 [-6%, +100%] 视为 90% 带；中心取 0（无毛发模，BF=1.75 偏 GR），
# 半宽 sigma = (100-(-6))/(2*1.645)。诚实标注：该通道无信息、不读成 TUFT 证据。
DAMP_LO90, DAMP_HI90 = -6.0, 100.0
DAMP_MED = 0.0
DAMP_SIG = (DAMP_HI90 - DAMP_LO90)/(2.0*Z90)   # ~32.2%

# GW150914  remnant (Isi ringdown): Mf=68 Msun, chi=0.63 (68% cred)
MW, CHI = 68.0, 0.63


def gauss_likelihood(med, sig, delta_h):
    """单高斯：med 为观测中心(%), sig 为1sigma(%)；返回 lnL0/lnL1/dlnL/BF/dB/n_excl。"""
    lnL0 = -0.5*(med/sig)**2
    lnL1 = -0.5*((med-delta_h)/sig)**2
    dl = lnL1 - lnL0
    bf = math.exp(dl)
    db = 10.0*math.log10(bf) if bf > 0 else float("-inf")
    n_excl = (med - delta_h)/sig   # 负=H1 在 med 上方被压
    return dict(med=med, sig=sig, lnL0=lnL0, lnL1=lnL1, dl=dl, BF=bf, dB=db, n_excl=n_excl)


# ==================================================================
lines = []
def p(s=""):
    lines.append(s); print(s)

p("="*82)
p("TUFT v60 泛音 n=1 独立通道合并似然：基模被否后高阶模是否还有意外")
p("="*82)
p("唯一已发表 n=1 直接测量：GW150914（Isi 2019）；Estelles2023 仅 n0；Capano2021=(3,3,0)非 n1。")
p("方法：独立高斯似然，不 import v56/v57/v58/v59；H0=GR(δ=0) vs H1=TUFT(n1 同 n0 比例)。")
p("")

# ---- 任务2：GR n1 归算（GW150914）----
p("[任务2] GR n=1 标称归算（GW150914 remnant Mf=68 Msun, chi=0.63，Isi ringdown）")
p("-"*82)
wR = interp(N1_TABLE, CHI, 1)
wI = interp(N1_TABLE, CHI, 2)
f_gr = (K_HZ_PER_MSUN/MW)*wR
tau_gr = MW*GM_SUN_c3_MS/wI
p(f"  Kerr (2,2,1) @chi={CHI}:  M*omega_R={wR:.6f},  M*|omega_I|={wI:.6f}")
p(f"  GR n1 预期 f221 = (32312.5/{MW:.0f})*{wR:.4f} = {f_gr:.1f} Hz")
p(f"  GR n1 预期 tau221 = {MW:.0f}*{GM_SUN_c3_MS*1000:.3f}us/{wI:.4f} = {tau_gr:.3f} ms  (文献~1.4ms 一致)")
p(f"  Isi δf1=-5% -> f_obs = 0.95*{f_gr:.1f} = {0.95*f_gr:.1f} Hz (残差已含 Mf/chi 边缘化)")
p("")
p("  (对照: n0 @chi=0.63 M*omega_R=0.5045, f220~{:.1f} Hz; 泛音 n1 频率低于 n0，符合 Isi 正文"
  " 'higher n does not imply higher frequency, rather the opposite')".format((K_HZ_PER_MSUN/MW)*0.5045))
p("")

# ---- 任务1 数据表 ----
p("[任务1] 已发表泛音 n=1 测量值（GW150914，单事件）")
p("-"*82)
p(f"  频率 δf1:  {FREQ['med']:+.0f}% ± {FREQ['sig']:.0f}% (1sigma; Isi 报 68% 置信)")
p(f"             隐含 90% 带 = [{FREQ['med']-Z90*FREQ['sig']:+.1f}%, {FREQ['med']+Z90*FREQ['sig']:+.1f}%]")
p(f"  阻尼 δτ1:  发表区间 [{DAMP_LO90:+.0f}%, {DAMP_HI90:+.0f}%] 基本未约束；无毛发 vs 浮动 BF=1.75 略偏 GR")
p(f"             高斯记账: 中心={DAMP_MED:+.0f}%(无毛发模), sigma1={DAMP_SIG:.1f}%  [诚实: 无信息, 不读成 TUFT 证据]")
p(f"  探测本身争议: Cotesta2020 BF~1; Finch&Moore BF 0.1-10; PRD110 L041501(2024) 全边缘化 BF=2.3±0.1 -> 不鲁棒")
p("")

# ---- 任务3：频率通道合并似然 ----
p("[任务3a] 频率通道合并似然：H0: δf=0(GR) vs H1: δf=+16.26%(TUFT n1)")
p("-"*82)
R = gauss_likelihood(FREQ["med"], FREQ["sig"], TUFT_DF)
p(f"  观测: med={R['med']:+.1f}% ± {R['sig']:.1f}% (1sigma)")
p(f"  lnL(H0=GR)      = {R['lnL0']:+.4f}")
p(f"  lnL(H1=+16.26%) = {R['lnL1']:+.4f}")
p(f"  dlnL = {R['dl']:+.4f}   BF={R['BF']:.4f}   dB={R['dB']:+.3f} dB  ->  {'H0(GR)偏好' if R['dl']<0 else 'H1(TUFT)偏好'}")
p(f"  H1=+16.26% 距 med = {TUFT_DF-R['med']:.2f}% = {abs(R['n_excl']):.3f} sigma  (负=H1 在 med 上方被压)")
p("")
# 3a 保守 x1.5
Rx = gauss_likelihood(FREQ["med"], FREQ["sig"]*1.5, TUFT_DF)
p(f"  [保守 1sigma x1.5] sigma={FREQ['sig']*1.5:.1f}%: dlnL={Rx['dl']:+.3f}  BF={Rx['BF']:.3f}  dB={Rx['dB']:+.3f}  n_excl={Rx['n_excl']:+.3f}")
# 3b 最乐观 c_m 端 +8.82%
Ro = gauss_likelihood(FREQ["med"], FREQ["sig"], SENS_OPT_DF)
p(f"  [最乐观 c_m 端 H1=+{SENS_OPT_DF:.2f}%]  dlnL={Ro['dl']:+.3f}  BF={Ro['BF']:.3f}  dB={Ro['dB']:+.3f}  n_excl={Ro['n_excl']:+.3f}")
p("")

# ---- 任务3：阻尼通道合并似然 ----
p("[任务3b] 阻尼通道合并似然：H0: δτ=0(GR) vs H1: δτ=+57.6%(TUFT n1)")
p("-"*82)
Rd = gauss_likelihood(DAMP_MED, DAMP_SIG, TUFT_DTAU)
p(f"  观测: med={Rd['med']:+.1f}% ± {Rd['sig']:.1f}% (1sigma; 发表带[-6,+100], 中心=无毛发模)")
p(f"  lnL(H0=GR)      = {Rd['lnL0']:+.4f}")
p(f"  lnL(H1=+57.6%)  = {Rd['lnL1']:+.4f}")
p(f"  dlnL = {Rd['dl']:+.4f}   BF={Rd['BF']:.4f}   dB={Rd['dB']:+.3f} dB  ->  {'H0(GR)偏好' if Rd['dl']<0 else 'H1(TUFT)偏好'}")
p(f"  H1=+57.6% 距 med = {TUFT_DTAU-Rd['med']:.2f}% = {abs(Rd['n_excl']):.3f} sigma")
p(f"  [诚实标注] 发表带[-6,+100]同时套住 GR(0) 与 TUFT(+57.6%) -> 阻尼通道无分辨力；Isi 自报无毛发 BF=1.75 偏 GR")
p("")
Rdx = gauss_likelihood(DAMP_MED, DAMP_SIG*1.5, TUFT_DTAU)
p(f"  [保守 1sigma x1.5] sigma={DAMP_SIG*1.5:.1f}%: dlnL={Rdx['dl']:+.3f}  BF={Rdx['BF']:.3f}  dB={Rdx['dB']:+.3f}  n_excl={Rdx['n_excl']:+.3f}")
Rdo = gauss_likelihood(DAMP_MED, DAMP_SIG, OPT_DTAU)
p(f"  [最乐观 c_m 端 H1=+{OPT_DTAU:.1f}%]  dlnL={Rdo['dl']:+.3f}  BF={Rdo['BF']:.3f}  dB={Rdo['dB']:+.3f}  n_excl={Rdo['n_excl']:+.3f}")
p("")

# ---- 任务4：诚实分级 ----
p("="*82)
p("[任务4] 三通道结论（n0频率 / n0阻尼 / n1）与四态分级")
p("="*82)
p("  n0 频率 (v58): TUFT +16.26% 在边际化联合 5.86σ 排除；数据残差 +2%±2.4% -> 兼容 GR")
p("  n0 阻尼 (v59): TUFT +57.6% 在边际化联合 5.59σ 排除；数据残差 +10%±8.5% -> 兼容 GR")
p(f"  n1 频率 (本轮): med={FREQ['med']:+.0f}%±{FREQ['sig']:.0f}%; TUFT +16.26% 仅 {abs(R['n_excl']):.2f}σ  away; dB={R['dB']:+.1f}")
p(f"                  -> 残差在 GR 侧(-5%, 距 GR 仅 {abs(FREQ['med']/FREQ['sig']):.2f}σ)，不支持 TUFT(+16% 距 {abs(R['n_excl']):.2f}σ)")
p(f"  n1 阻尼 (本轮): 发表带[-6,+100]无信息; TUFT +57.6% 仅 {abs(Rd['n_excl']):.2f}σ; 无毛发 BF=1.75 偏 GR")
p("")
p("  三结局判定：")
p("   (1) n1 也排除?  否 — n1 频率 TUFT +16% 仅 1.06σ、阻尼 1.79σ，均不显著排除。")
p("   (2) n1 兼容 GR、偏离 TUFT?  是 — 频率残差 med=-5%(GR侧)，无任何正频移/长阻尼指向 TUFT；")
p("       与 n0 同向（同证 GR 侧），但分辨力不足（±20%），不能独立排除 TUFT。")
p("   (3) n1 残差反贴近 TUFT(与 n0 矛盾)?  否 — med=-5% 而非 +16%，无孤例。")
p("")
p("  四态分级: n1 频率=【兼容 GR / 但未达分辨力(不证伪不证实 TUFT)】; n1 阻尼=【无信息】。")
p("  总判定: n0 双通道(5.86σ/5.59σ)已干净否定 TUFT 复谱; n1 高阶模落在 GR 侧(-5%)但误差棒")
p("  ±20% 太宽、且泛音探测本身不鲁棒(全边缘化 BF~2.3)，既不能独立排除 TUFT，也不构成任何")
p("  复活证据；与 n0 无矛盾。不据 n1 复活理论，也不据 n1 夸大为第三重独立排除。")

with open(r"D:\a10\aikjx\code\my_lib\_audit_v60_overtone_likelihood_out.txt",
          "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
