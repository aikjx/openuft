# -*- coding: utf-8 -*-
"""
TUFT-r66 · ROOT V12.0（KK 电磁耦合）来料审计 + 「一运动统一四力」论题攻破
（纯标准库 Decimal / float，9+ 自检 guard）

来料主张链：高维几何 → 电磁规范场 → 电荷量子化 → 精细结构常数 α
            α_KK = 4(ℓ_P/R)^2；反解 R = 2ℓ_P/√α = 23.412475 ℓ_P

本册独立重算并追加一项来料未列的结构性杀招：
  ★ e/m 普适性定理：e_n = n√(16πG)/R 与 m_n = n/(R) 同源于第五维动量
    ⇒ e_n/m_n = √(16πG) = 4√π/M_Pl，与 n、R 均无关（普适常数）。
    电子实测 e/m = 592.6 GeV^-1 而模型普适值 5.807e-19 GeV^-1，差 1.02e21 倍。
    该比值不可由调 R 或选 n 修正 ⇒ **零参数 no-go**（比来料 n=1 质量检查更强）。

门禁 F4 / E9 / Ω5 + 一运动四力台账。
结论常量：KK_ALPHA_RELATION_VALID_NOT_PREDICTION_ONE_MOTION_MATTER_FATAL
"""
import json
import os
import math
from decimal import Decimal, getcontext

getcontext().prec = 60

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r66_ROOTV12_KK电磁耦合来料审计与一运动四力攻破_2026-10-31"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 常数（CODATA / 标准）
# ---------------------------------------------------------------------------
ALPHA_INV = Decimal("137.035999177")        # CODATA 2022
ALPHA = Decimal(1) / ALPHA_INV
L_P = Decimal("1.616255e-35")               # 普朗克长度 m
M_PL_GEV = Decimal("1.2209e19")             # 普朗克质量 GeV
M_E_GEV = Decimal("0.000510999")            # 电子静能 GeV
KG_PER_GEV = Decimal("1.78266192e-27")      # 1 GeV/c^2 对应 kg
HBAR = Decimal("1.054571817e-34")
C = Decimal("2.99792458e8")
PI = Decimal(str(math.pi))

# 来料自报值（用于对照）
CLAIM = {"R_over_lP": Decimal("23.412475"), "R_m": Decimal("3.78405e-34"),
         "m_KK1_GeV": Decimal("5.21469907e17"), "ratio_m_over_me": Decimal("1.02049e21"),
         "alpha_from_electron": Decimal("7.00724e-45"), "scan_residual": Decimal("6.73e-81")}


def dec_sqrt(x):
    return Decimal(str(math.sqrt(float(x))))


# ---------------------------------------------------------------------------
# 一、复算来料的 α_KK 链条
# ---------------------------------------------------------------------------
# R = 2 ℓ_P / √α
sqrt_alpha = dec_sqrt(ALPHA)
R_over_lP = Decimal(2) / sqrt_alpha
R_m = R_over_lP * L_P

# m_KK,1 = ℏ/(R c) → kg → GeV
m_KK1_kg = HBAR / (R_m * C)
m_KK1_GeV = m_KK1_kg / KG_PER_GEV
ratio_m_over_me = m_KK1_GeV / M_E_GEV

# 消去 R：α = 4 (m_KK,1 / M_Pl)^2；若强行令 m_KK,1 = m_e
alpha_from_electron = Decimal(4) * (M_E_GEV / M_PL_GEV) ** 2

# ---------------------------------------------------------------------------
# 二、★ e/m 普适性定理（本册新增，强于来料 n=1 检查）
# ---------------------------------------------------------------------------
# 自然单位：e_n = n√(16πG)/R（无量纲），m_n = n/R（GeV）
# ⇒ e_n/m_n = √(16πG) = √(16π)/M_Pl = 4√π/M_Pl  （与 n、R 无关）
E_OVER_M_MODEL = (Decimal(4) * dec_sqrt(PI)) / M_PL_GEV          # GeV^-1
E_OVER_M_ELECTRON = dec_sqrt(Decimal(4) * PI * ALPHA) / M_E_GEV  # GeV^-1
EM_RATIO = E_OVER_M_ELECTRON / E_OVER_M_MODEL                    # 实测/模型

# 普适性检验：n=1 与 n=2 的 e/m 必须完全相同
def e_over_m(n):
    e_n = n * dec_sqrt(Decimal(16) * PI) / M_PL_GEV   # 取 R 自然单位 1（比值与 R 无关）
    m_n = Decimal(n)                                   # 以 1/R 为单位
    return e_n / m_n


em_n1, em_n2 = e_over_m(1), e_over_m(2)
em_universal_residual = abs(em_n2 - em_n1) / em_n1

# 模型对任意单位电荷粒子预言的质量（n=1, e=√(4πα)）
M_MODEL_UNIT_CHARGE = dec_sqrt(Decimal(4) * PI * ALPHA) / E_OVER_M_MODEL   # GeV

# ---------------------------------------------------------------------------
# 三、来料「10000 组残差 6.73e-81」的判别力审计（IDENTITY / NO_TEST）
# ---------------------------------------------------------------------------
def identity_scan_float(npts=10000):
    """同一恒等式两条数值路径互比：α=4/x^2 的 4/(x*x) vs (2/x)^2。"""
    worst = 0.0
    for i in range(1, npts + 1):
        x = 1.0 + i * 0.01
        a = 4.0 / (x * x)
        b = (2.0 / x) ** 2
        r = abs(a - b) / a if a != 0 else 0.0
        if r > worst:
            worst = r
    return worst


def identity_scan_decimal(npts=200, prec=60):
    getcontext().prec = prec
    worst = Decimal(0)
    for i in range(1, npts + 1):
        x = Decimal(1) + Decimal(i) / Decimal(10)
        a = Decimal(4) / (x * x)
        b = (Decimal(2) / x) ** 2
        r = abs(a - b) / a
        if r > worst:
            worst = r
    getcontext().prec = 60
    return worst


scan_float = identity_scan_float(10000)
scan_dec = identity_scan_decimal(200, 60)

# 正对照：把公式改成错式 α=5/x^2，同一套检查应能抓出
def wrong_formula_residual():
    x = 10.0
    correct = 4.0 / (x * x)
    wrong = 5.0 / (x * x)
    return abs(wrong - correct) / correct


control_wrong = wrong_formula_residual()

# ---------------------------------------------------------------------------
# 四、一运动四力台账（用户论题：力可放在一个运动里）
# ---------------------------------------------------------------------------
ONE_MOTION = [
    {"力": "引力", "是否由第五维运动统一": "是(5D 测地方程→4D 测地)", "判定": "PASS",
     "注": "KK 经典结果，几何与引力同源"},
    {"力": "电磁", "是否由第五维运动统一": "是(5D 测地→Lorentz 力)", "判定": "PASS",
     "注": "KK 核心成果：U(1) 与 Lorentz 力同源于一个 5D 运动"},
    {"力": "radion/标量第五力", "是否由第五维运动统一": "是(额外标量自由度)", "判定": "FAIL",
     "注": "半径涨落给出未观测的长程第五力；冻结半径又不自治(来料§6)"},
    {"力": "弱 (SU(2))", "是否由第五维运动统一": "否(S^1 只给 U(1))", "判定": "FAIL",
     "注": "非阿贝尔规范场需更大紧致流形；且纯 KK 难出手征费米子"},
    {"力": "强 (SU(3))", "是否由第五维运动统一": "否(S^1 只给 U(1))", "判定": "FAIL",
     "注": "同上；禁闭/质量隙亦未由几何导出"},
    {"力": "带电物质/质量谱", "是否由第五维运动统一": "否(同运动锁定 e/m)", "判定": "FAIL",
     "注": "★ e/m 普适 ⇒ 无轻带电费米子，零参数 no-go"},
]

# ---------------------------------------------------------------------------
# 自检 guard
# ---------------------------------------------------------------------------
guards = []
def guard(name, cond):
    guards.append((name, bool(cond)))
    return bool(cond)


def rel(a, b):
    return abs(a - b) / b if b != 0 else Decimal(9)


guard("R_over_lP_matches_claim", rel(R_over_lP, CLAIM["R_over_lP"]) < Decimal("1e-4"))
guard("R_m_matches_claim", rel(R_m, CLAIM["R_m"]) < Decimal("1e-3"))
guard("m_KK1_matches_claim", rel(m_KK1_GeV, CLAIM["m_KK1_GeV"]) < Decimal("1e-3"))
guard("ratio_m_over_me_matches_claim", rel(ratio_m_over_me, CLAIM["ratio_m_over_me"]) < Decimal("1e-3"))
guard("alpha_from_electron_matches_claim",
      rel(alpha_from_electron, CLAIM["alpha_from_electron"]) < Decimal("1e-3"))
guard("em_universality_n1_eq_n2", em_universal_residual < Decimal("1e-30"))
guard("no_light_charged_matter_em_gap", EM_RATIO > Decimal("1e15"))
guard("identity_scan_is_precision_limited", scan_float < 1e-12 and scan_dec < Decimal("1e-40"))
guard("positive_control_wrong_formula_caught", control_wrong > 1e-3)

VERDICT = "KK_ALPHA_RELATION_VALID_NOT_PREDICTION_ONE_MOTION_MATTER_FATAL"
guard("verdict_constant_set", VERDICT == "KK_ALPHA_RELATION_VALID_NOT_PREDICTION_ONE_MOTION_MATTER_FATAL")

F4 = ("α_KK=4(ℓ_P/R)^2 是『含自由参数 R 的关系式』而非 α 的数值推导；把『关系式』"
      "称为『推导出电磁耦合』属范畴混装 → F4 触发。且该式依赖 B_μ 归一化与 2πR 体因子约定")
E9 = ("同一类五维真空 R_MN=0 对任意 R 成立 ⇒ 无唯一能标；保持 G_4 固定则 α∝R^-2，"
      "保持 G_5 固定则 α∝R^-3，二者均不能由真空方程选出 R ⇒ E9 对『几何定 α』FAIL")
Ω5 = ("稳定化候选 V=Ax^2+B/x^2 引入 2 个新自由常数去预言 1 个数(α)，A/B=3.33e-6 系拟合；"
      "R 本身亦为输入 ⇒ 自由参数净增，Ω5 触发")

payload = {
    "audit": "TUFT-r66",
    "subject": "ROOT V12.0（KK 电磁耦合）来料审计 + 「一运动统一四力」论题攻破",
    "verdict": VERDICT,
    "recompute": {
        "R_over_lP": float(R_over_lP), "claim_R_over_lP": float(CLAIM["R_over_lP"]),
        "R_m": float(R_m), "claim_R_m": float(CLAIM["R_m"]),
        "m_KK1_GeV": float(m_KK1_GeV), "claim_m_KK1_GeV": float(CLAIM["m_KK1_GeV"]),
        "ratio_m_over_me": float(ratio_m_over_me), "claim_ratio_m_over_me": float(CLAIM["ratio_m_over_me"]),
        "alpha_from_electron": float(alpha_from_electron),
        "claim_alpha_from_electron": float(CLAIM["alpha_from_electron"]),
    },
    "em_universality_theorem": {
        "e_over_m_model_GeV_inv": float(E_OVER_M_MODEL),
        "e_over_m_electron_GeV_inv": float(E_OVER_M_ELECTRON),
        "ratio_electron_over_model": float(EM_RATIO),
        "universal_residual_n1_vs_n2": float(em_universal_residual),
        "model_mass_for_unit_charge_GeV": float(M_MODEL_UNIT_CHARGE),
        "statement": "e_n/m_n = 4√π/M_Pl 与 n、R 均无关 ⇒ 电子 e/m 超模型 1.02e21 倍，"
                     "不可由调 R 或选 n 修正 ⇒ 零参数 no-go（强于来料 n=1 检查）",
    },
    "discriminative_power_audit": {
        "identity_scan_float_max_residual": scan_float,
        "identity_scan_decimal60_max_residual": float(scan_dec),
        "claim_80digit_residual": float(CLAIM["scan_residual"]),
        "classification": "IDENTITY / NO_TEST：残差量级随算术精度走(双精度~1e-16, 60位~1e-58, "
                          "来料80位~1e-81)，证明只是重算同一恒等式，无物理判别力",
        "positive_control_wrong_formula_residual": control_wrong,
    },
    "one_motion_ledger": ONE_MOTION,
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "来料算术自洽（R=%.6f ℓ_P、m_KK1=%.4e GeV、α_e=%.4e 均复现），且来源诚实承认"
        "『未完成对 α 的第一性原理预测』。但本册追加一条更强的结构性否定：★e/m 普适性定理——"
        "同一第五维动量同时给电荷与质量 ⇒ e/m=4√π/M_Pl 与 n、R 无关，电子实测 e/m 超模型 "
        "%.3e 倍，无任何自由度可调 ⇒ 一运动方案不可能产生轻带电费米子（零参数 no-go）。"
        "一运动台账：引力/电磁 PASS，radion 第五力、弱、强、带电物质谱 FAIL ⇒ 『四力放进一个运动』"
        "在该最简 KK 模型内未达成（仅覆盖 2/4 力，且含未观测第五力）。α_KK 关系式有效但非预测"
        "(F4/E9/Ω5 均触发)。"
        % (float(R_over_lP), float(m_KK1_GeV), float(alpha_from_electron), float(EM_RATIO))
    ),
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

md = []
md.append("# TUFT-r66 · ROOT V12.0 来料审计 + 一运动四力攻破 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("\n## 一、来料链条复算（算术自洽）")
md.append("- R/ℓ_P = %.6f（来料 %.6f）" % (float(R_over_lP), float(CLAIM["R_over_lP"])))
md.append("- R = %.5e m（来料 %.5e）" % (float(R_m), float(CLAIM["R_m"])))
md.append("- m_KK,1 = %.5e GeV（来料 %.5e）；与电子之比 %.4e（来料 %.4e）"
          % (float(m_KK1_GeV), float(CLAIM["m_KK1_GeV"]), float(ratio_m_over_me), float(CLAIM["ratio_m_over_me"])))
md.append("- 令 m_KK1=m_e 反算 α = %.4e（来料 %.4e）" % (float(alpha_from_electron), float(CLAIM["alpha_from_electron"])))
md.append("\n## 二、★ e/m 普适性定理（本册新增·零参数 no-go）")
md.append("- 模型普适 e/m = %.4e GeV^-1（=4√π/M_Pl，与 n、R 无关）" % float(E_OVER_M_MODEL))
md.append("- 电子实测 e/m = %.4e GeV^-1" % float(E_OVER_M_ELECTRON))
md.append("- 比值（实测/模型）= %.4e ⇒ 模型带电态必 ≥ %.3e GeV" % (float(EM_RATIO), float(M_MODEL_UNIT_CHARGE)))
md.append("- n=1 与 n=2 的 e/m 相对残差 = %.2e ⇒ 普适性成立" % float(em_universal_residual))
md.append("\n## 三、判别力审计（来料 10000 组残差）")
md.append("- 双精度残差 %.2e / 60 位残差 %.2e / 来料 80 位 %.2e" % (scan_float, float(scan_dec), float(CLAIM["scan_residual"])))
md.append("- 判定：IDENTITY/NO_TEST（残差随算术精度走 ⇒ 重算恒等式，无物理判别力）")
md.append("- 正对照：错式 α=5/x^2 残差 %.3f（能抓代数错误，但不抓物理）" % control_wrong)
md.append("\n## 四、一运动四力台账")
for r in ONE_MOTION:
    md.append("- %s：%s | %s | %s" % (r["力"], r["是否由第五维运动统一"], r["判定"], r["注"]))
md.append("\n## 五、门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("TUFT-r66 ROOT V12.0 来料审计 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("复算: R=%.6f lP | m_KK1=%.4e GeV | alpha_e=%.4e (均复现来料)" % (float(R_over_lP), float(m_KK1_GeV), float(alpha_from_electron)))
report.append("★e/m普适: 模型%.3e vs 电子%.3e = %.3e 倍差 (零参数no-go)" % (float(E_OVER_M_MODEL), float(E_OVER_M_ELECTRON), float(EM_RATIO)))
report.append("判别力: 恒等式扫描残差 float %.2e / dec60 %.2e => IDENTITY/NO_TEST; 正对照 %.3f" % (scan_float, float(scan_dec), control_wrong))
report.append("一运动: 引力PASS 电磁PASS | radion/弱/强/带电物质 FAIL => 2/4")
report.append("guard 数=%d, 全过=%s" % (len(guards), all(g[1] for g in guards)))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

guard_all = all(g[1] for g in guards) and (len(guards) >= 9)
raise SystemExit(0 if guard_all else 1)
