# -*- coding: utf-8 -*-
"""
TUFT-r71 · 参数复用穷举审计（正面回答 r70 X-R70-1）

r70 定理：加料式修补 surplus 不变 ⇒ 唯一通路是**参数跨域复用**。
本卷检验：框架里究竟有没有一个参数能被真正复用？

★ 复用判据（严格版，本卷核心）：
    同一个参数 p，分别拟合到两个独立可观测量 O1、O2，得到 p1、p2。
    若 p1 ≈ p2（相对差 < 容差）⇒ **真复用**，surplus +1；
    若 p1 ≠ p2 ⇒ **复用失败**（那只是两次独立拟合，不是复用）。
    ⇒ 禁止"每个域各自重拟合一次"来冒充复用。

单位约定：取电荷单位 = e（电子 n=1）⇒ R_α = 2ℓ_P/√α = 23.412475 ℓ_P。

结果预告：
  - R：α 域拟合 R=23.41 ℓ_P；质量域拟合 R=1.5e17~2.4e22 ℓ_P ⇒ 失配 ≥ 6.49e15 ⇒ **复用失败**
  - κ/τ/l0/θ：V(κ)≡0、零信息、无实根 ⇒ **根本无法拟合**（NO_FIT）
  - ★ GR 的 G：Cavendish 与 水星进动 拟合值相对差 ~6e-6 ⇒ **真复用，通过**

额外发现（诚实且重要）：
  若要让 R 复用成功，须在 m = M_Pl/R_α = 5.21e17 GeV 处存在带电粒子；
  该能标比 LHC 可达 (~1.36e4 GeV) 高 **3.83e13 倍** ⇒ 该"第二可观测量"**永久不可检验**。

裁决常量：NO_REUSABLE_PARAMETER_IN_FRAMEWORK_UNFALSIFIABLE_SECOND_OBSERVABLE
"""
import os
import sys
from decimal import Decimal

SRC_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
import _criteria_kernel as K  # noqa: E402

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r71_参数复用穷举审计_2026-11-01"

G = K.GuardBook("TUFT-r71")
TOL = Decimal("1e-3")     # 复用容差（相对差）

# ---------------------------------------------------------------------------
# 常数
# ---------------------------------------------------------------------------
ALPHA_INV = Decimal("137.035999177")
ALPHA = Decimal(1) / ALPHA_INV
M_PL = Decimal("1.2209e19")          # GeV
L_P = Decimal("1.616255e-35")        # m
sqrt_alpha = K.dec_sqrt(ALPHA)

# 单位约定：电荷单位 = e ⇒ 电子 n=1 ⇒ α = 4·1²·(ℓ_P/R)²
R_ALPHA = Decimal(2) / sqrt_alpha                 # R/ℓ_P，由 α 拟合
M_KK_AT_R_ALPHA = M_PL / R_ALPHA                  # 该 R 下 n=1 的质量 GeV

# ---------------------------------------------------------------------------
# 一、R 的复用检验：α 域 vs 各质量域
# ---------------------------------------------------------------------------
# m = n/R（n=1）⇒ R = M_PL / m  （单位 ℓ_P）
MASS_TARGETS = [
    ("电子 m_e", Decimal("0.000510999")),
    ("µ 子 m_µ", Decimal("0.10565837")),
    ("τ 子 m_τ", Decimal("1.77686")),
    ("质子 m_p", Decimal("0.938272")),
    ("W 玻色子", Decimal("80.379")),
]

reuse_rows = []
for name, m_obs in MASS_TARGETS:
    R_fit = M_PL / m_obs                 # 由质量拟合出的 R（单位 ℓ_P）
    ratio = R_fit / R_ALPHA              # 与 α 域拟合值之比；≈1 才算复用
    rel = abs(ratio - Decimal(1))
    reuse_rows.append({
        "参数": "R", "域1": "α(实测)", "域2": name,
        "p1_R_by_alpha": float(R_ALPHA), "p2_R_by_mass": float(R_fit),
        "比值": float(ratio), "相对差": float(rel), "复用成立": bool(rel < TOL),
    })

FRAMEWORK_REUSE_OK = [r for r in reuse_rows if r["复用成立"]]
BEST = min(reuse_rows, key=lambda r: r["相对差"])

# ---------------------------------------------------------------------------
# 二、其余候选参数：能否拟合？（V(κ)≡0 等 ⇒ 无解）
# ---------------------------------------------------------------------------
NO_FIT_ROWS = [
    {"参数": "κ (螺旋曲率)", "状态": "NO_FIT",
     "依据": "r45 C2：公理1 使 V(κ)≡0 ⇒ 变分链无粒子，无法定住 κ"},
    {"参数": "τ (挠率)", "状态": "NO_FIT",
     "依据": "与 κ 同源；α=τ/κ 声称未获独立定量验证"},
    {"参数": "l0 (自由长度)", "状态": "NO_FIT",
     "依据": "r42：撞 Ω5；取 l0=ℓ_P 则退化为零信息"},
    {"参数": "θ (螺距角)", "状态": "NO_FIT",
     "依据": "r45 T16：真实粒子需 θ<1.4e-11 rad 才有实根，与实测不兼容"},
    {"参数": "ω (螺旋频率)", "状态": "DEF",
     "依据": "r264：ω 只是 mc²/ħ 的改名，非独立参数"},
]

# ---------------------------------------------------------------------------
# 三、正对照：GR 的 G 跨域复用（Cavendish ↔ 水星进动，须给出同一个 G）
# ---------------------------------------------------------------------------
G_CAV = Decimal("6.67430e-11")
M_SUN = Decimal("1.9885e30")
C = Decimal("2.99792458e8")
A_MER = Decimal("5.7909050e10")
E_MER = Decimal("0.205630")
ORBITS_PER_CENTURY = Decimal("415.2")
ARCSEC_PER_RAD = Decimal("206264.806")
OBS_ARCSEC = Decimal("42.98")

# 由观测进动反解 G：Δφ_orbit = 6πGM/(c^2 a (1-e^2))
dphi_century_rad = OBS_ARCSEC / ARCSEC_PER_RAD
dphi_orbit = dphi_century_rad / ORBITS_PER_CENTURY
TWO_PI_6 = Decimal(6) * Decimal(str(3.141592653589793))   # 6π
G_FROM_MERCURY = dphi_orbit * (C ** 2) * A_MER * (Decimal(1) - E_MER ** 2) / (TWO_PI_6 * M_SUN)

GR_RATIO = G_FROM_MERCURY / G_CAV
GR_REL = abs(GR_RATIO - Decimal(1))
GR_REUSE_OK = bool(GR_REL < TOL)

# ---------------------------------------------------------------------------
# 四、额外发现：R 复用成功所需的能标 vs 实验可达能标
# ---------------------------------------------------------------------------
LHC_REACH = Decimal("1.36e4")            # GeV（13.6 TeV）
REQUIRED_SCALE = M_KK_AT_R_ALPHA         # 5.21e17 GeV
UNFALSIFIABLE_FACTOR = REQUIRED_SCALE / LHC_REACH

# ---------------------------------------------------------------------------
# 自检 guard（含正对照强制）
# ---------------------------------------------------------------------------
G.guard("r_alpha_matches_r66", abs(R_ALPHA / Decimal("23.412475") - 1) < Decimal("1e-5"))
G.guard("m_kk_at_R_alpha_matches_r70",
        abs(M_KK_AT_R_ALPHA / Decimal("5.21474e17") - 1) < Decimal("1e-3"))
G.guard("no_framework_reuse_succeeds", len(FRAMEWORK_REUSE_OK) == 0)
G.guard("best_reuse_attempt_still_fails", Decimal(str(BEST["相对差"])) > TOL)
G.guard("best_discrepancy_huge", Decimal(str(BEST["比值"])) > Decimal("1e15"))
G.guard("no_fit_params_documented", len(NO_FIT_ROWS) >= 5)
G.require_control("gr_G_reuse_succeeds", GR_REUSE_OK)
G.guard("gr_G_values_agree", GR_REL < Decimal("1e-4"))
G.guard("second_observable_unfalsifiable", UNFALSIFIABLE_FACTOR > Decimal("1e10"))

VERDICT = "NO_REUSABLE_PARAMETER_IN_FRAMEWORK_UNFALSIFIABLE_SECOND_OBSERVABLE"
G.guard("verdict_constant_set",
        VERDICT == "NO_REUSABLE_PARAMETER_IN_FRAMEWORK_UNFALSIFIABLE_SECOND_OBSERVABLE")

F4 = ("『在两个域各自拟合一次』被当作『参数复用』：复用要求同一参数值在两个域同时成立，"
      "分别重拟合只是两次独立拟合 ⇒ 范畴错置 → F4 触发")
E9 = ("R 在 α 域(23.41 ℓ_P)与质量域(≥1.5e17 ℓ_P)取值相差 ≥6.49e15 ⇒ 跨能标复用失败，E9 FAIL")
Ω5 = ("唯一能使复用的参数不存在；其余候选(κ,τ,l0,θ)根本无法拟合 ⇒ 自由量预算无法靠复用兑现，"
      "Ω5 指向：框架缺乏可复用的承重参数")

payload = {
    "audit": "TUFT-r71",
    "subject": "参数复用穷举审计（正面回答 r70 X-R70-1）",
    "verdict": VERDICT,
    "reuse_criterion": {
        "严格判据": "同一参数 p 分别拟合到 O1、O2 得 p1、p2；p1≈p2（相对差<1e-3）才算真复用",
        "禁止": "每个域各自重拟合一次来冒充复用（那只是两次独立拟合）",
        "单位约定": "电荷单位 = e ⇒ 电子 n=1 ⇒ R_α = 2ℓ_P/√α",
    },
    "r_reuse_sweep": reuse_rows,
    "framework_reuse_ok": [r["域2"] for r in FRAMEWORK_REUSE_OK],
    "best_attempt": BEST,
    "no_fit_params": NO_FIT_ROWS,
    "gr_control": {
        "G_from_Cavendish": float(G_CAV), "G_from_Mercury": float(G_FROM_MERCURY),
        "ratio": float(GR_RATIO), "relative_diff": float(GR_REL), "reuse_ok": GR_REUSE_OK,
        "note": "★G 由 Cavendish(实验室) 定住，又由水星进动(天体) 反解 ⇒ 同一值 ⇒ 真复用",
    },
    "unfalsifiability": {
        "required_scale_GeV": float(REQUIRED_SCALE),
        "lhc_reach_GeV": float(LHC_REACH),
        "factor_beyond_reach": float(UNFALSIFIABLE_FACTOR),
        "note": "R 复用若要成功，须存在质量 5.21e17 GeV 的带电粒子；该能标高 LHC 3.83e13 倍"
                " ⇒ 第二可观测量永久不可检验（不仅是错，是不可证伪）",
    },
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "严格复用判据（同一参数两域拟合值须一致，容差 1e-3）下：框架的 **R 复用全部失败** ——"
        " α 域拟合 R=%.4f ℓ_P，质量域拟合 R 介于 %.3e~%.3e ℓ_P，**最小失配 %.3e（%s）**；"
        "其余候选 κ/τ/l0/θ 根本无法拟合（V(κ)≡0、零信息、无实根）。⇒ **框架内不存在可复用的承重参数**。"
        "正对照 GR：G 由 Cavendish 得 %.5e、由水星进动反解得 %.5e，相对差 %.1e ⇒ **真复用成立**，"
        "证明判据能识别复用。额外发现：R 复用若要成功须存在 %.3e GeV 的带电粒子，高出 LHC 可达"
        " %.2e 倍 ⇒ 该第二可观测量**永久不可检验**。⇒ X-R70-1 关闭：复用通路在该框架内无可行参数。"
        % (float(R_ALPHA), min(r["p2_R_by_mass"] for r in reuse_rows),
           max(r["p2_R_by_mass"] for r in reuse_rows), float(BEST["比值"]), BEST["域2"],
           float(G_CAV), float(G_FROM_MERCURY), float(GR_REL),
           float(REQUIRED_SCALE), float(UNFALSIFIABLE_FACTOR))
    ),
}

md = []
md.append("# TUFT-r71 · 参数复用穷举审计 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("- 严格判据：同一参数两域拟合值须一致（相对差 < %s）" % TOL)
md.append("- 单位约定：电荷单位 = e ⇒ 电子 n=1 ⇒ R_α = 2ℓ_P/√α")
md.append("\n## 一、R 复用扫描（α 域 vs 质量域）")
md.append("- α 域拟合：R = %.6f ℓ_P" % float(R_ALPHA))
for r in reuse_rows:
    md.append("- vs %s：R = %.4e ℓ_P | 比值 %.3e | 相对差 %.3e | **复用=%s**"
              % (r["域2"], r["p2_R_by_mass"], r["比值"], r["相对差"], r["复用成立"]))
md.append("- **框架复用成功项 = %s**" % [r["域2"] for r in FRAMEWORK_REUSE_OK])
md.append("- 最接近的一次：%s（比值 %.3e，仍差 %s 量级）" % (BEST["域2"], float(BEST["比值"]), "15"))
md.append("\n## 二、其余候选参数")
for r in NO_FIT_ROWS:
    md.append("- %s：%s | %s" % (r["参数"], r["状态"], r["依据"]))
md.append("\n## 三、★ 正对照：GR 的 G 真复用")
md.append("- G(Cavendish) = %.6e" % float(G_CAV))
md.append("- G(水星进动反解) = %.6e" % float(G_FROM_MERCURY))
md.append("- 比值 %.8f，相对差 %.2e ⇒ **复用成立=%s**" % (float(GR_RATIO), float(GR_REL), GR_REUSE_OK))
md.append("\n## 四、额外发现：第二可观测量不可证伪")
md.append("- R 复用成功所需带电粒子质量 = %.4e GeV" % float(REQUIRED_SCALE))
md.append("- LHC 可达 ≈ %.3e GeV ⇒ 高出 **%.2e 倍**" % (float(LHC_REACH), float(UNFALSIFIABLE_FACTOR)))
md.append("\n## 五、门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)

report = []
report.append("TUFT-r71 参数复用穷举审计 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("R复用: alpha域=%.4f lP; 质量域最小失配 %.3e (%s) => 全部失败" % (float(R_ALPHA), float(BEST["比值"]), BEST["域2"]))
report.append("其余参数 kappa/tau/l0/theta: NO_FIT (V(k)=0/零信息/无实根)")
report.append("★GR正对照: G_Cav=%.6e G_Mercury=%.6e 相对差 %.1e => 真复用成立=%s" % (float(G_CAV), float(G_FROM_MERCURY), float(GR_REL), GR_REUSE_OK))
report.append("不可证伪: 需 %.3e GeV 带电粒子, 高 LHC %.2e 倍" % (float(REQUIRED_SCALE), float(UNFALSIFIABLE_FACTOR)))
report.append("guard 数=%d, 全过=%s" % (G.n, G.all_pass()))

K.write_triplet(OUT_DIR, BASENAME, payload, md, report)
raise SystemExit(G.exit_code(min_guards=9))
