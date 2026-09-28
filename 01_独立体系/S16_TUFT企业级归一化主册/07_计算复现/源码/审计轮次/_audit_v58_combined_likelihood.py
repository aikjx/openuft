# -*- coding: utf-8 -*-
"""
==================================================================================
TUFT v58 合并似然定量判决：现有振铃数据对 TUFT +16.26% 到底多强
==================================================================================

纪律（与 v56/v57 同源）：
- 数值全部来自 v56 观测检验报告 / 已发表值，硬编码照抄；不 import v56/v57。
- 残差高斯、独立假设；H0=GR (delta=0) vs H1=TUFT (delta=+16.26%)。
- 两套并列不混用：(A) 朴素归算残差；(B) 已发表边际化 delta_f220。
- 90% CI -> 1sigma：sigma = (high90 - low90)/(2*1.645)（高斯等效半宽）。
- 禁伪闭合、禁 cherry-pick、不夸大方差挽救理论。

来源（v56 报告照抄）：
  Estelles et al. 2023 CQG (arXiv:2104.01906) O3 直接振铃 (2,2,0)；
  Abbott et al. 2016 PRL 116 221101 (arXiv:1602.03837) GW150914 经典单 n0；
  Capano et al. 2021 (arXiv:2105.05238) GW190521 泛音争议。
  TUFT 标称 +16.26%；灵敏带 c_m in [-0.369,-0.218] -> +8.82%~+21.17%。
"""
import math

# ------------------------------------------------------------------
# 常数
# ------------------------------------------------------------------
Z90 = 1.645           # 90% 双侧高斯 z 值
TUFT_DELTA = 16.26    # %  TUFT 标称频移
SENS_OPT_DELTA = 8.82  # % 灵敏带内最有利 TUFT（最小正 delta，离数据最近）
SENS_LO = 8.82
SENS_HI = 21.17

# ------------------------------------------------------------------
# 任务1：数据整理
# (name, delta_obs %, low90 %, high90 %)  —— 全部照抄 v56 报告 §3/§4
# ------------------------------------------------------------------
# (A) 朴素归算残差（固定 Mf/chif，忽略 M-chi-delta_f 简并；6 事件）
NAIVE_6 = [
    # name,                 d_obs, low90, high90
    ("GW150914",           -2.8,  -7.7,   3.6),
    ("GW170104",           -5.7, -15.5,  -1.0),
    ("GW190519_153544",    -8.4, -18.1,   0.4),
    ("GW190521_074359",    -2.2,  -7.8,   4.8),
    ("GW190630_185205",   -10.0, -29.1,   1.6),
    ("GW190828_063405",     3.8,  -7.4,  84.8),  # 无信息量（±85%）
]

# (B) 已发表边际化 delta_f220（Estelles 2023，正确计入 Mf-chi-delta_f 简并）
MARG_SINGLE = [
    # GW150914 单事件（pre+post-merger SNR 充分）
    ("GW150914_marg",       5.0,  -2.0,  16.0),  # +11.0/-7.0 -> 90% band [-2,+16]
]
MARG_JOINT = [
    # 六事件 hierarchical 联合（同 delta_f）
    ("sixevent_joint",      2.0,  -2.0,   6.0),  # +4.0/-4.0 -> 90% band [-2,+6]
]
# 注意：MARG_JOINT 包含 GW150914，与 MARG_SINGLE 嵌套，不能当独立事件合并。


def sigma_from_band(low90, high90):
    """90% 带 [low,high] -> 高斯等效 1sigma = (high-low)/(2*1.645)。"""
    return (high90 - low90) / (2.0 * Z90)


def event_table(events):
    """返回 [(name, d_obs, sigma1)]，sigma 为 %。"""
    out = []
    for name, d, lo, hi in events:
        out.append((name, d, sigma_from_band(lo, hi)))
    return out


def combined_gauss(events, delta_h):
    """
    高斯独立残差合并：
      L(delta) ∝ exp(-1/2 sum ((d_i - delta)/sigma_i)^2)
    返回 dict：
      P = sum 1/sigma_i^2  (precision)
      d_hat = (sum d_i/sigma_i^2)/P   (flat-prior posterior mean)
      sig_comb = 1/sqrt(P)            (combined 1sigma)
      lnL_h0 = -1/2 sum (d_i/sigma_i)^2
      lnL_h1 = -1/2 sum ((d_i-delta_h)/sigma_i)^2
      dlnL = lnL_h1 - lnL_h0
      BF = exp(dlnL)
      dB = 10 log10 BF
      n_sig_excl = (d_hat - delta_h)/sig_comb   (H1 被排除的 nsigma，>0 表示 H1 在 d_hat 上方被压)
    """
    rows = event_table(events)
    P = sum(1.0 / (s * s) for _, _, s in rows)
    d_hat = sum(d / (s * s) for _, d, s in rows) / P
    sig_comb = 1.0 / math.sqrt(P)
    lnL_h0 = -0.5 * sum((d / s) ** 2 for _, d, s in rows)
    lnL_h1 = -0.5 * sum(((d - delta_h) / s) ** 2 for _, d, s in rows)
    dlnL = lnL_h1 - lnL_h0
    bf = math.exp(dlnL)
    db = 10.0 * math.log10(bf) if bf > 0 else float("-inf")
    n_excl = (d_hat - delta_h) / sig_comb  # 负值=H1 在 d_hat 上方
    return {
        "n": len(rows), "P": P, "d_hat": d_hat, "sig_comb": sig_comb,
        "lnL_h0": lnL_h0, "lnL_h1": lnL_h1, "dlnL": dlnL,
        "BF": bf, "dB": db, "n_excl": n_excl, "rows": rows,
    }


def inflate(events, f=1.5):
    """把每个事件 sigma 乘 f：通过把 90% 带宽乘 f 实现（重新构造 low/high）。"""
    out = []
    for name, d, lo, hi in events:
        h90 = (hi - lo) / 2.0
        out.append((name, d, d - f * h90, d + f * h90))
    return out


def fmt_r(r):
    name, d, s = r
    return f"{name:<22} d_obs={d:+6.2f}%  sigma1={s:6.3f}%"


# ==================================================================
# 主输出
# ==================================================================
lines = []
def p(s=""):
    lines.append(s)
    print(s)

p("=" * 82)
p("TUFT v58 合并似然定量判决：现有振铃数据对 TUFT +16.26% 到底多强")
p("=" * 82)
p("假设：残差高斯、独立；H0=GR (delta=0) vs H1=TUFT (delta=+16.26%)。")
p("90% CI -> 1sigma：sigma = (high90-low90)/(2*1.645)。BF=exp(dlnL)；dB=10 log10 BF。")
p("")

# ---- 任务1 数据表 ----
p("[任务1] 各事件残差与 1sigma 误差（%）")
p("-" * 82)
p("(A) 朴素归算残差（固定 Mf/chif，忽略 M-chi-delta_f 简并）")
for r in event_table(NAIVE_6):
    p("  " + fmt_r(r))
p("")
p("(B) 已发表边际化 delta_f220（Estelles 2023，正确计入简并；与 A 并列不混用）")
for r in event_table(MARG_SINGLE):
    p("  " + fmt_r(r) + "   [单事件 GW150914]")
for r in event_table(MARG_JOINT):
    p("  " + fmt_r(r) + "   [六事件 hierarchical 联合；含 GW150914，与上嵌套不独立]")
p("")

# ---- 任务2 合并似然 ----
p("[任务2] 合并对数似然比 / Bayes 因子 / dB（H1=TUFT 标称 +16.26%）")
p("-" * 82)

sets = [
    ("朴素 6 事件集（含 GW190828 无信息量）", NAIVE_6),
    ("朴素 5 事件集（剔除 GW190828）",        [e for e in NAIVE_6 if not e[0].startswith("GW190828")]),
    ("边际化 GW150914 单事件",                MARG_SINGLE),
    ("边际化 六事件联合",                      MARG_JOINT),
]

results = {}
for label, ev in sets:
    R = combined_gauss(ev, TUFT_DELTA)
    results[label] = R
    p(f"")
    p(f"  集 = {label}  (n={R['n']})")
    p(f"    合并后 d_hat     = {R['d_hat']:+.3f}%")
    p(f"    合并 1sigma      = {R['sig_comb']:.3f}%")
    p(f"    lnL(H0=GR)      = {R['lnL_h0']:+.4f}")
    p(f"    lnL(H1=+16.26%) = {R['lnL_h1']:+.4f}")
    p(f"    dlnL=lnL(H1)-lnL(H0) = {R['dlnL']:+.4f}")
    p(f"    BF(H1/H0)        = {R['BF']:.4e}")
    verdict = "H1(TUFT) 偏好" if R['dlnL'] > 0 else "H0(GR) 偏好"
    p(f"    dB = 10log10(BF) = {R['dB']:+.3f} dB   ->  {verdict}")
    p(f"    H1=+16.26% 被排除 nsigma = {R['n_excl']:+.3f}  (负=H1 在 d_hat 上方被压)")

# ---- 任务3a 保守误差放大 x1.5 ----
p("")
p("[任务3a] 保守误差放大：1sigma x1.5 重算（结论是否翻转？）")
p("-" * 82)
for label, ev in sets:
    R = combined_gauss(inflate(ev, 1.5), TUFT_DELTA)
    p(f"  {label:<40} dlnL={R['dlnL']:+8.3f}  dB={R['dB']:+7.3f}  n_excl={R['n_excl']:+6.3f}  "
      f"({'GR' if R['dlnL']<0 else 'TUFT'} 偏好)")

# ---- 任务3b 灵敏带最乐观：delta=+8.82% ----
p("")
p(f"[任务3b] 灵敏带最乐观：c_m band 内取最有利 TUFT 的 delta=+{SENS_OPT_DELTA:.2f}%（离数据最近）")
p("-" * 82)
for label, ev in sets:
    R = combined_gauss(ev, SENS_OPT_DELTA)
    p(f"  {label:<40} dlnL={R['dlnL']:+8.3f}  BF={R['BF']:.3e}  dB={R['dB']:+7.3f}  n_excl={R['n_excl']:+6.3f}  "
      f"({'GR' if R['dlnL']<0 else 'TUFT'} 偏好)")

# ---- 任务3c H1 标称被排除的 nsigma（从合并似然曲线读）----
p("")
p("[任务3c] H1=TUFT 标称 +16.26% 被合并数据排除的显著性（nσ）")
p("-" * 82)
for label, ev in sets:
    R = combined_gauss(ev, TUFT_DELTA)
    # n_excl = (d_hat - delta_h)/sig_comb ; 数据在 d_hat，H1 在 +16.26%
    p(f"  {label:<40} d_hat={R['d_hat']:+6.2f}% ±{R['sig_comb']:5.2f}%  "
      f"H1=+16.26% 距 d_hat = {TUFT_DELTA-R['d_hat']:6.2f}% = {abs(R['n_excl']):5.2f}σ")

# ---- 判定摘要 ----
p("")
p("=" * 82)
p("[任务4] 诚实分级摘要")
p("=" * 82)
R6 = results["朴素 6 事件集（含 GW190828 无信息量）"]
R5 = results["朴素 5 事件集（剔除 GW190828）"]
Rj = results["边际化 六事件联合"]
p(f"朴素 6 事件 : dB={R6['dB']:+.2f} (GR 偏好 {abs(R6['dB']):.1f} dB)，H1 标称排除 {abs(R6['n_excl']):.2f}σ")
p(f"朴素 5 事件 : dB={R5['dB']:+.2f} (GR 偏好 {abs(R5['dB']):.1f} dB)，H1 标称排除 {abs(R5['n_excl']):.2f}σ")
p(f"边际化联合 : dB={Rj['dB']:+.2f} (GR 偏好 {abs(Rj['dB']):.1f} dB)，H1 标称排除 {abs(Rj['n_excl']):.2f}σ")
p("")
p("诚实标注：以上为 n0 单模、朴素残差未完全边际化 M-chi-delta_f；")
p("边际化联合集 (Estelles hierarchical) 是最干净约束，但含强 M-chi 简并事件。")
p("不挑数据、不为挽救理论而夸大方差。")

# 写文件
with open(r"D:\a10\aikjx\code\my_lib\_audit_v58_combined_likelihood_out.txt",
          "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
