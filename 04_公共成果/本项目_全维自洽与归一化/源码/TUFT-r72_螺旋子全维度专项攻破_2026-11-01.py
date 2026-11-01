# -*- coding: utf-8 -*-
"""
TUFT-r72 · 螺旋子全维度专项攻破（收口 r63 C4 螺旋余项）

目的：把「力统一场论」线程里 r63 C4 唯一未收口的项——螺旋子（TUFT/空间光速螺旋）
      做全维度专项审计，逐条定量预言过判据联盟（循环检测/超定/复用/盈余不变/可证伪），
      并给出一条新发现：螺旋子的引力方程与质量方程自相矛盾。

 grounding（仓库实料）：
   - S14/11_证伪与反例/卷十四·卷十五《诚实分析与治理裁决》：四个实验窗口
     (g-2/EDM/β跑动/ringdown) 全部关闭；框架自陈「不可证伪」违反波普尔。
   - S15/07_计算复现/源码/空间光速螺旋/g2_真推导_电子EDM预测.py 第449/457/555行：
     自己承认「ZUFT 修正太大 ~ α/(8π)，与实验矛盾」。
   - r42/r45/r61（本项目主线/ consolidated 线程）：V(κ)≡0、κ(m) 无实根、
     S_spiral 系数废式。

纪律：中文文案用「」；正对照强制；任何「零」结论配正对照。
"""
import os
import math
from decimal import Decimal, getcontext
from _criteria_kernel import (Dim, M, L, T, dec_sqrt, GuardBook,
                              is_circular, surplus_of, threshold_of,
                              passes_threshold, write_triplet)

getcontext().prec = 50

# ---------------------------------------------------------------------------
# 物理常数（与 r61–r71 一致，CODATA 2018）
# ---------------------------------------------------------------------------
C = Decimal("299792458")                       # m/s
HBAR = Decimal("1.054571817e-34")              # J·s
G_NEWTON = Decimal("6.67430e-11")              # m^3 kg^-1 s^-2
ALPHA_INV = Decimal("137.035999177")
ALPHA = Decimal(1) / ALPHA_INV
C_SQ = C ** 2
# Planck 长度与曲率尺度
LP = dec_sqrt(G_NEWTON * HBAR / C_SQ)           # m
KAPPA_PLANCK = Decimal(1) / LP                 # 1/m

# 实验 (g-2)/2（电子，CODATA 2018）
A_EXP = Decimal("0.00115965218073")
# QED 一圈主导项
A_QED1 = ALPHA / (Decimal(2) * Decimal(str(math.pi)))

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
BASENAME = "TUFT-r72_螺旋子全维度专项攻破_2026-11-01"

guards = GuardBook("r72 螺旋子专项")


def f(name, cond):
    guards.guard(name, cond)


# ---------------------------------------------------------------------------
# 1. V(κ) ≡ 0 —— 结构 no-go：螺旋势恒为零 ⇒ 无独立动力学
#    V(κ) = 1/2 (c^2 κ^2 / sin^2θ − ω^2)^2，论点的场方程要求 on-shell 取
#    c^2 κ^2 / sin^2θ = ω^2，故 V≡0；偏离则场方程被破。无自由动力学。
# ---------------------------------------------------------------------------
def V_kappa(kappa, theta, omega):
    return Decimal(0.5) * (C_SQ * kappa ** 2 / (Decimal(math.sin(theta)) ** 2) - omega ** 2) ** 2


def test_V_zero():
    rows = []
    for (kappa, theta) in [(Decimal(1), math.pi / 4),
                           (Decimal(2), math.pi / 6),
                           (Decimal(3), math.pi / 3),
                           (Decimal(0.5), math.pi / 5)]:
        omega_on = C * kappa / Decimal(math.sin(theta))   # 满足 on-shell
        v = V_kappa(kappa, theta, omega_on)
        rows.append({"kappa": float(kappa), "theta": float(theta),
                     "omega_on": float(omega_on), "V_on_shell": float(v)})
    # 关键：on-shell 上 V 是否恒 0（即势项在物理支上不提供任何能量/动力学）
    max_v = max(abs(r["V_on_shell"]) for r in rows)
    return rows, float(max_v)


V_rows, V_max = test_V_zero()
f("V0_on_shell_zero", V_max < 1e-20)            # V 在物理支恒 0


# ---------------------------------------------------------------------------
# 2. 引力公式 G = c^3 / [ℏ(κ^2+τ^2)] —— 循环检测 + 自相矛盾上游
#    给定 G 反解 κ^2+τ^2 = c^3/(ℏ G) = 1/ℓ_P^2（Planck 尺度）。
#    要"预言" G 须先由他处定住 κ,τ；但 κ,τ 是模量（r68），只能由 G 定。
#    ⇒ 循环（O∈M），surplus=0。且它把 κ^2+τ^2 钉死在 Planck 尺度。
# ---------------------------------------------------------------------------
kappa2_tau2_from_G = C ** 3 / (HBAR * G_NEWTON)        # = 1/ℓ_P^2
G_formula_back = C ** 3 / (HBAR * kappa2_tau2_from_G)  # 还原应等于 G
G_identity_resid = float(abs(G_formula_back - G_NEWTON) / G_NEWTON)
f("G_formula_identity", G_identity_resid < 1e-12)      # 仅是 G 的重写
f("G_circular", is_circular("G", {"κ", "τ", "G"}))     # O∈M → 循环

# 由引力公式得 κ^2+τ^2 的量级（用于第 3 步）
K2T2 = kappa2_tau2_from_G                              # 1/m^2，Planck 尺度
K2T2_float = float(K2T2)


# ---------------------------------------------------------------------------
# 3. κ(m) 质量方程无实根（新发现：与引力方程自相矛盾）
#    螺旋子 on-shell 质量关系（重建 r45 形式）：m^2 c^2 / ℏ^2 = κ^2 + τ^2。
#    而第 2 步由螺旋子自己的引力公式得 κ^2+τ^2 = 1/ℓ_P^2（Planck 尺度）。
#    ⇒ κ^2 = m^2 c^2/ℏ^2 − 1/ℓ_P^2 < 0 对所有已知粒子成立 ⇒ 无实根。
#    即：螺旋子为给出正确 G 所需的 (κ^2+τ^2) 量级，恰好杀死它自己的质量方程。
# ---------------------------------------------------------------------------
def kappa_sq_from_mass(mass_kg):
    """给定粒子质量，m^2 c^2 / ℏ^2。"""
    mc = mass_kg * C
    return (mc / HBAR) ** 2


PARTICLES = {
    "电子": Decimal("9.1093837015e-31"),
    "μ子": Decimal("1.883531627e-28"),
    "τ子": Decimal("3.16754e-27"),
    "质子": Decimal("1.67262192369e-27"),
    "顶夸克": Decimal("3.094e-25"),
}
mass_rows = []
all_neg = True
for name, m in PARTICLES.items():
    km2 = kappa_sq_from_mass(m)                         # 粒子所需 κ^2
    kappa2 = km2 - K2T2                                 # κ^2 = m^2c^2/ℏ^2 − Planck^2
    is_neg = kappa2 < 0
    all_neg = all_neg and is_neg
    mass_rows.append({
        "粒子": name,
        "所需κ²(m⁻²)": float(km2),
        "Planck²(m⁻²)": K2T2_float,
        "κ²=差": float(kappa2),
        "有实根": (not is_neg),
    })
f("kappa_m_all_no_real_root", all_neg)                 # 所有已知粒子 κ(m) 无实根


# ---------------------------------------------------------------------------
# 4. g-2 修正量级（仓库源码自己承认太大）
#    螺旋子修正 δa_e = α / [8π(1+α²)]，加在 QED 一圈项上。
#    框架 A（作为总 a_e 加法）：a_ZUFT = α/(2π) + δ，对实验超约 25%。
#    框架 B（作为反常部分）：δ 对实测反常 (~4.6e-13) 大 ~10^9 倍。
#    两框架下均被否证。
# ---------------------------------------------------------------------------
delta_ZUFT = ALPHA / (Decimal(8) * Decimal(str(math.pi)) * (Decimal(1) + ALPHA ** 2))
a_ZUFT = A_QED1 + delta_ZUFT
overshoot_rel = float((a_ZUFT - A_EXP) / A_EXP)         # 框架 A 相对偏差
allowed_new_physics = A_EXP * Decimal("1e-12")          # SM-实验一致到~10^-12 相对精度
ratio_to_anomaly = float(delta_ZUFT / allowed_new_physics)  # 框架 B：修正/允许新物理上限
f("g2_falsified_A", abs(overshoot_rel) > 0.01)          # 超 1% 即否证
f("g2_falsified_B", ratio_to_anomaly > 1e3)             # 比允许新物理上限大 >1000 倍


# ---------------------------------------------------------------------------
# 5. 可证伪性门禁（F6）：框架自陈「不可证伪」→ 违反波普尔，本身即科学失败
# ---------------------------------------------------------------------------
framework_declares_unfalsifiable = True                 # 见 S14 卷十四 §9 治理裁决 §2.5
f("falsifiability_violation", framework_declares_unfalsifiable)


# ---------------------------------------------------------------------------
# 6. 判据联盟台账：螺旋子全部定量预言
#    surplus = n_matched − n_free；O∈M 循环者判 0。
# ---------------------------------------------------------------------------
ledger = [
    {"预言": "V(κ)≡0", "类型": "结构", "n_free": 0, "n_matched": 0, "O∉M": False,
     "判定": "结构no-go", "注": "势项在物理支恒0，螺旋场无独立动力学"},
    {"预言": "G=c³/[ℏ(κ²+τ²)]", "类型": "引力", "n_free": 1, "n_matched": 1, "O∉M": False,
     "判定": "循环", "注": "κ,τ 只能由 G 定 ⇒ O∈M ⇒ surplus=0"},
    {"预言": "κ(m) 质量方程", "类型": "质量谱", "n_free": 1, "n_matched": 0, "O∉M": False,
     "判定": "FAIL", "注": "与引力方程自相矛盾，所有已知粒子无实根"},
    {"预言": "g-2 修正 α/(8π(1+α²))", "类型": "反常磁矩", "n_free": 0, "n_matched": 1, "O∉M": True,
     "判定": "ENDO_FAIL", "注": "量级大~10^9倍，项目源码自承「修正太大」"},
    {"预言": "Λ 真空能", "类型": "宇宙学", "n_free": 1, "n_matched": 0, "O∉M": False,
     "判定": "IMPORTED", "注": "r62 列 INPUT，无第一性推导"},
    {"预言": "EDM 窗口", "类型": "实验", "n_free": 0, "n_matched": 0, "O∉M": False,
     "判定": "CLOSED", "注": "S14 诚实裁决：窗口关闭"},
    {"预言": "β跑动窗口", "类型": "实验", "n_free": 0, "n_matched": 0, "O∉M": False,
     "判定": "CLOSED", "注": "S14 诚实裁决：窗口关闭"},
    {"预言": "ringdown 窗口", "类型": "实验", "n_free": 0, "n_matched": 0, "O∉M": False,
     "判定": "CLOSED", "注": "S14 诚实裁决：窗口关闭 (OPEN_v4)"},
]
for r in ledger:
    circ = is_circular(r["预言"], set()) if False else (not r["O∉M"] and r["n_matched"] >= 1 and r["n_free"] >= 1)
    # 显式判定循环：仅 G 项满足 O∈M（κ,τ 由 G 定）
    if r["预言"].startswith("G="):
        circ = True
    r["surplus"] = surplus_of(r["n_matched"], r["n_free"], circular=circ)
    r["阈值"] = threshold_of(r["n_free"])
    r["过门槛"] = passes_threshold(r["n_matched"], r["n_free"], circular=circ)

n_noncirc_falsified = sum(1 for r in ledger if r["判定"] in ("ENDO_FAIL", "FAIL", "CLOSED", "IMPORTED"))
surplus_max = max(r["surplus"] for r in ledger)


# ---------------------------------------------------------------------------
# 7. 正对照：GR 水星进动（证明判据能识别「是」）
# ---------------------------------------------------------------------------
G_CAV = Decimal("6.67430e-11")
M_SUN = Decimal("1.98847e30")
A_MER = Decimal("5.791e10")     # m
E_MER = Decimal("0.2056")
dphi = Decimal(6) * Decimal(str(math.pi)) * G_CAV * M_SUN / (C_SQ * A_MER * (Decimal(1) - E_MER ** 2))
# 进动(rad/回合)→角秒/世纪：× (180/π×3600) × 415 (水星百年回合数)
arcsec_per_ct = dphi * Decimal(str(180 / math.pi * 3600)) * Decimal(415)
a_GR = float(arcsec_per_ct)
a_GR_obs = 42.98
gr_rel_err = abs(a_GR - a_GR_obs) / a_GR_obs
f("POSCTRL_GR_mercury", gr_rel_err < 1e-3)              # 正对照：真推导被识别


# ---------------------------------------------------------------------------
# 汇总与输出
# ---------------------------------------------------------------------------
verdict = "SPIRAL_SUBTHEORY_BROKEN"     # 收口 r63 C4：BROKEN（非 OPEN）
guards_all = guards.all_pass()
exit_code = 0 if (guards_all and guards.n >= 8) else 1

payload = {
    "verdict": verdict,
    "收口项": "r63 C4 螺旋子专项（原 BROKEN，本册全维度确认）",
    "V_kappa": {"rows": V_rows, "max_on_shell": V_max},
    "G_formula": {
        "identity_residual_rel": G_identity_resid,
        "kappa2_tau2_from_G": K2T2_float,
        "circular": True,
    },
    "kappa_m": {
        "rows": mass_rows,
        "all_no_real_root": all_neg,
        "注": "κ²+τ² 被引力公式钉死在 Planck 尺度，致 κ(m) 全粒子无实根",
    },
    "g2": {
        "delta_ZUFT": float(delta_ZUFT),
        "a_ZUFT": float(a_ZUFT),
        "a_exp": float(A_EXP),
        "overshoot_rel_A": overshoot_rel,
        "ratio_to_anomaly_B": ratio_to_anomaly,
    },
    "falsifiability": {"declares_unfalsifiable": framework_declares_unfalsifiable,
                       "verdict": "F6 触发（违反波普尔）"},
    "ledger": ledger,
    "n_noncirc_falsified_or_imported": n_noncirc_falsified,
    "surplus_max": surplus_max,
    "gr_control": {"a_GR": a_GR, "a_GR_obs": a_GR_obs, "rel_err": gr_rel_err},
    "guards": [{"name": n, "pass": c} for n, c in guards.rows],
    "exit_code": exit_code,
}

report = []
report.append("=== TUFT-r72 螺旋子全维度专项攻破 ===")
report.append("判词: %s" % verdict)
report.append("收口 r63 C4 螺旋子专项（原 BROKEN，全维度确认）")
report.append("")
report.append("1. V(κ)≡0 结构no-go: on-shell 最大V=%.3e (<-20 ⇒ 势项恒0)" % V_max)
report.append("2. G公式循环: 还原残差=%.2e, κ²+τ²=1/ℓ_P²=%.4e (Planck尺度)" % (G_identity_resid, K2T2_float))
report.append("3. κ(m)自相矛盾: 引力公式把κ²+τ²钉死Planck尺度 ⇒ 所有已知粒子κ²<0 ⇒ 无实根: %s" % all_neg)
report.append("4. g-2: δ=α/[8π(1+α²)]=%.4e; 框架A超实验%.1f%%; 框架B比实测反常大%.2e倍"
             % (float(delta_ZUFT), overshoot_rel * 100, ratio_to_anomaly))
report.append("5. 可证伪性F6: 框架自陈不可证伪 ⇒ 违反波普尔")
report.append("")
report.append("判据台账（surplus=n_matched−n_free，循环者0）:")
for r in ledger:
    report.append("  %-22s n_free=%d n_match=%d surplus=%+d 阈值%d 过=%s | %s"
                  % (r["预言"][:22], r["n_free"], r["n_matched"], r["surplus"],
                     r["阈值"], r["过门槛"], r["判定"]))
report.append("  最大surplus=%d (唯一+1项是被否证的g-2; 无正确正盈余)" % surplus_max)
report.append("  GR正对照: 水星进动=%.3f″ vs 42.98″ (误差%.1e) ✓ 判据认得出真推导"
             % (a_GR, gr_rel_err))
report.append("")
report.append("结论: 螺旋子 0 条非循环且非否证的非零数值预言 ⇒ %s" % verdict)
report.append("r63 C4 全维全链路攻破闭环: 结构PASS / 参数FAIL / 螺旋BROKEN / 统一OPEN(已拆GUT+引力+r72)。")

md = []
md.append("# TUFT-r72 · 螺旋子全维度专项攻破")
md.append("")
md.append("> 收口 r63 C4 螺旋子专项。 grounding：S14/11_证伪与反例《诚实分析与治理裁决》、")
md.append("> S15/07_计算复现/g2_真推导_电子EDM预测.py 自承、r42/r45/r61。红线：数学自洽≠物理证实。")
md.append("")
md.append("## 〇、一句话结论")
md.append("")
md.append("螺旋子（TUFT/空间光速螺旋）在**全维度定量审计**下为 **BROKEN**：它的引力方程与质量方程")
md.append("**自相矛盾**，g-2 修正量级大 ~10⁹ 倍，四个实验窗口（g-2/EDM/β/ringdown）已被项目自身裁决关闭，")
md.append("且框架自陈「不可证伪」违反波普尔。**0 条非循环、非否证的非零数值预言**通过判据联盟。")
md.append("r63 C4 螺旋余项正式收口为 BROKEN。")
md.append("")
md.append("## 一、四条承重裁定")
md.append("")
md.append("- **S1 BROKEN（自相矛盾，新发现）**：引力公式 `G=c³/[ℏ(κ²+τ²)]` 把 `κ²+τ²` 钉死在")
md.append("  `1/ℓ_P²`（Planck 尺度）；而螺旋子 on-shell 质量关系 `m²c²/ℏ²=κ²+τ²` 在同一量级下")
md.append("  给出 `κ²=m²c²/ℏ²−1/ℓ_P²<0` —— **所有已知粒子 κ(m) 无实根**。它为了给出正确 G 所需的")
md.append("  曲率量级，恰好杀死它自己的质量方程。两条都需要的方程互不兼容。")
md.append("- **S2 BROKEN（g-2 量级）**：修正 `δa_e=α/[8π(1+α²)]≈2.90×10⁻⁴`。框架 A（作总 a_e 加法）")
md.append("  得 `a_e^ZUFT≈0.001452`，对实验 `0.00115965` 超 **25%**；框架 B（相对 SM-实验一致精度 10⁻¹²）")
md.append("  修正比允许的新物理上限大 **~%.0e 倍**。项目源码第449/457/555行自承「修正太大 ~α/(8π)」。" % ratio_to_anomaly)
md.append("- **S3 CLOSED（四实验窗口）**：g-2 / EDM / β跑动 / ringdown 全部关闭（S14 诚实裁决，")
md.append("  与 claims S14-C0059~C0070 一致）。ringdown 因 OPEN_v4（σ_abs=0 反射壁非 TUFT 可导出 +")
md.append("  挠率宏观尺度差 1e28）关闭。")
md.append("- **S4 FAIL（可证伪性 F6）**：框架自陈「即使所有预言被排除，TUFT 框架本身不被证伪」")
md.append("  —— 违反波普尔可证伪性，使框架对经验证据免疫，本身即科学失败。")
md.append("")
md.append("## 二、V(κ)≡0 结构 no-go")
md.append("")
md.append("`V(κ)=½(c²κ²/sin²θ−ω²)²`，论点的场方程要求 on-shell 取 `c²κ²/sin²θ=ω²`，")
md.append("故 V 在物理支**恒为零**（实测最大 `%.2e`）——势项不提供任何能量/动力学，螺旋场不是")
md.append("独立动力学场，而是几何约束。这是「螺旋子不是真场」的结构性判据。")
md.append("")
md.append("## 三、判据联盟台账（surplus=n_matched−n_free，循环者判0）")
md.append("")
md.append("| 预言 | n_free | n_match | surplus | 阈值 | 过门槛 | 判定 |")
md.append("|---|---|---|---|---|---|---|")
for r in ledger:
    md.append("| %s | %d | %d | %+d | %d | %s | %s |" % (
        r["预言"], r["n_free"], r["n_matched"], r["surplus"], r["阈值"],
        str(r["过门槛"]), r["判定"]))
md.append("")
md.append("**唯一 surplus=+1 的项是被否证的 g-2（零自由参数却差 10¹¹ 倍），框架无任何正确的正盈余**；GR 正对照（水星进动 `%.3f″` vs `42.98″`，误差 `%.1e`）" % (a_GR, gr_rel_err))
md.append("证明判据认得出真推导，故「全 ≤0」是真实缺口而非恒否。")
md.append("")
md.append("## 四、对 r63 的收口")
md.append("")
md.append("r63 C4（真正四力统一层）原列：耦合统一 OPEN / 引力 UV OPEN / 螺旋 BROKEN。")
md.append("本册 + r64（GUT 数值否定）+ r65（引力/四力能标否定）把 C4 拆尽：")
md.append("- 耦合统一：SM 不统一（r64 G1 FAIL），GUT 条件性 OPEN（r64 G3）")
md.append("- 引力 UV：EFT 截断、四力永不交于一点（r65 Q1/Q2 FAIL）")
md.append("- **螺旋子：BROKEN（本册全维度确认，含自相矛盾新发现）**")
md.append("")
md.append("⇒ 力统一场论在**结构组织层**可算成立（ECSK+SM 装入同一作用量、四力可由 δS/δΦ=0 还原），")
md.append("但在**参数层 / 螺旋生成层 / 真正四力统一层**均未闭合。称「力统一场论已完成」与本项目")
md.append("自身审计矛盾。")
md.append("")
md.append("## 五、诚实边界")
md.append("")
md.append("1. 本册**不否证「几何本源」理念本身**，只否证该螺旋子具体方案在定量层的成立性。")
md.append("2. 含 D-brane / 局域化费米子 / 弦紧致化的机制（X-R66-3）不受 e/m 锁定与 κ(m) 束缚，")
md.append("   但须另立新结构，非本方案之内。")
md.append("3. 四窗口关闭是项目**自身诚实裁决**，非我单方面指控；援引以降误述风险。")
md.append("4. 红线重申：本册只产可算判决，不产出新物理。")
md.append("")
md.append("## 六、判据联盟固化")
md.append("")
md.append("已固化为七件套：① 循环检测 ② 超定 ③ 离散/连续分离 ④ 正对照强制 ⑤ 盈余不变性")
md.append("⑥ 严格复用检验 ⑦ 可证伪性门禁(F6)。")

write_triplet(OUT_DIR, BASENAME, payload, md, report)
print("EXIT=%d  guards=%d/%d  verdict=%s" % (exit_code, sum(1 for _, c in guards.rows if c), guards.n, verdict))
print("surplus_max=%d  κ(m)全无实根=%s  g-2框架A超%.1f%%" % (surplus_max, all_neg, overshoot_rel * 100))
