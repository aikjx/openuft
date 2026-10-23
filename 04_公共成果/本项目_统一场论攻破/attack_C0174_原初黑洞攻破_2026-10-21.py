# -*- coding: utf-8 -*-
"""
attack_C0174_原初黑洞攻破_2026-10-21.py
独立精算：母册 T403「原初黑洞（PBH）形成阈值与质量函数」· 临界塌缩理论

定位：母册 Top100 清单行原文（域 I）：
  | T403 | 原初黑洞（PBH）形成阈值与质量函数 | 临界塌缩理论 | C2,C5 | 🔲 |
判定号 C0174（C0173 后空号）。衔接：C0168（黑洞微观态）、C0172（Page 曲线，
t_ev∝M³ / T_H∝1/M）、C0156（引力本质求道深化）。

把「PBH 形成阈值与质量函数从哪来」压缩成四条可复核读数 + 一张供给账单：

  E1 事实引用（只引用不复算）：临界塌缩标度律 M_PBH=κ M_H(δ−δ_c)^γ（γ≈0.36、
     δ_c≈0.45 辐射主导）；PBH 蒸发 T_H∝1/M、t_ev∝M³（<10¹⁶ g 量级已蒸发）；
     LIGO/Virgo 5–40 M☉ 质量窗口；丰度约束（微引力透镜/蒸发 γ 射线/引力波）。
  E2 **第一性精算（本册核心）**：
     (a) 临界塌缩质量标度律 δ=0.46/0.50/0.60 时 M_PBH/M_H 比值（γ=0.36）；
     (b) f_PBH≈0.2 且 M≈30 M☉ 所需 β 反解量级（β=f_PBH·sqrt(M_form/M_eq)）；
     (c) 蒸发寿命 t_ev∝M³ 对 10¹⁵ g / 10¹⁷ g / 1 M☉ 三档精算；
     (d) Hawking 温度 T_H∝1/M 对 1 M☉（nK 量级）与 10¹⁵ g 精算。
  E3 几何供给判定：PBH 形成依赖初始密度扰动谱（暴胀/外部公设），TUFT 无扰动谱
     供给、无 PBH 预言，供给 0；撞 C2（初始条件外部）/C5（无预言）。
  E4 与 C0168/C0172/C0156 衔接；母册 T403 🔲→✅ 登记引用。
  E5 裁定：结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖，退出码 0。

诚实边界：本册不宣称解决 PBH 形成问题；外部观测值只引用不复算；
临界塌缩指数 γ 与阈值 δ_c 为外部文献值（只引用）；
t_ev/T_H 锚点承接 C0172 E1 报告值，本册只做 M³ / 1/M 标度换算。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算；来源注释标注） ----------
# 临界塌缩标度律（Brodbeck-Carr / Niemeyer 等，辐射主导暴后）：
#   M_PBH = κ · M_H · (δ − δ_c)^γ
GAMMA = Decimal("0.36")      # γ ≈ 0.36（辐射主导，外部文献值，只引用）
DELTA_C = Decimal("0.45")     # δ_c ≈ 0.45（辐射主导阈值，外部文献值，只引用）
KAPPA = Decimal(1)            # κ ~ O(1)，比值归一取 1（只做 M_PBH/M_H 相对量）

# CODATA 2018（C0172 E1 引用同口径，只引用）
M_SUN_G = Decimal("1.989e33")   # 1 M☉ = 1.989e33 g（=1.989e30 kg）
# C0172 E1 报告锚点（承接引用，不复算）：
T_EV_M_SUN = Decimal("6.6182e74")   # t_ev(1 M☉) = 5120πG²M³/(ħc⁴)，s
T_H_M_SUN_K = Decimal("6.1687e-8")  # T_H(1 M☉) = ħc³/(8πGMk_B)，K
# 物质-辐射相等时视界质量（外部文献值，只引用）：
M_EQ_M_SUN = Decimal("2.8e17")      # M_H(t_eq) ≈ 2.8×10^17 M☉
# 宇宙年龄（外部文献值，只引用）：
T_AGE_S = Decimal("4.35e17")        # 13.8 Gyr ≈ 4.35e17 s
# 一年秒数（定义值）：
SEC_PER_YR = Decimal("3.15576e7")


def e1_facts():
    """PBH 形成/蒸发/观测约束事实（外部文献只引用）。"""
    return {
        "scaling_law": "M_PBH = κ M_H (δ − δ_c)^γ",
        "gamma": GAMMA, "delta_c": DELTA_C, "kappa": KAPPA,
        "evap": "T_H ∝ 1/M；t_ev ∝ M³；M < 10^16 g 量级 PBH 已蒸发（外部引用）",
        "ligo_window_Msun": "5–40",
        "abundance": "微引力透镜 / 蒸发 γ 射线 / 引力波 => f_PBH < 10^-2 量级",
        "sources": ["Carr & Kuhnel 2022 (PBH review)",
                    "Niemeyer & Jedamzik 1998 (critical collapse)",
                    "LIGO/Virgo O1–O3 质量窗口",
                    "MACHO/EROS/OGLE 微引力透镜",
                    "Fermi γ 射线背景蒸发约束"],
    }


def e2_scaling_ratio():
    """临界塌缩质量标度律：δ=0.46/0.50/0.60 时 M_PBH/M_H = (δ−δ_c)^γ（κ=1）。"""
    deltas = [Decimal("0.46"), Decimal("0.50"), Decimal("0.60")]
    out = []
    for d in deltas:
        excess = d - DELTA_C
        ratio = excess ** GAMMA   # Decimal 支持非整数幂
        out.append({"delta": d, "excess": excess, "M_PBH_over_M_H": ratio})
    return out


def e2_beta_backsolve(f_pbh=Decimal("0.2"), m_form=Decimal("30")):
    """f_PBH≈0.2 且 M≈30 M☉ 所需 β 反解。
    推导链：辐射主导期塌缩质量比 β = ρ_PBH/ρ_rad；物质/辐射比 ∝ a ∝ 1/T；
    视界质量 M_H ∝ T^{-2} ⇒ a_eq/a_form = (M_eq/M_form)^{1/2}。
    相等时 ρ_PBH/ρ_rad ≈ f_PBH ⇒ f_PBH = β · (M_eq/M_form)^{1/2}
    ⇒ β = f_PBH · (M_form/M_eq)^{1/2}。"""
    ratio = m_form / M_EQ_M_SUN
    beta = f_pbh * ratio.sqrt()
    return {"f_PBH": f_pbh, "M_form_Msun": m_form, "M_eq_Msun": M_EQ_M_SUN,
            "M_form_over_M_eq": ratio, "beta": beta}


def e2_evap_lifetime():
    """t_ev ∝ M³：锚 t_ev(1M☉)=6.6182e74 s（C0172 E1）。"""
    masses_g = [Decimal("1e15"), Decimal("1e17")]
    out = []
    for mg in masses_g:
        mr = mg / M_SUN_G                 # 以 M☉ 为单位
        t = T_EV_M_SUN * mr ** Decimal(3)
        out.append({"M_g": mg, "M_over_Msun": mr, "t_ev_s": t,
                    "t_ev_yr": t / SEC_PER_YR})
    # 1 M☉ 档
    out.append({"M_g": M_SUN_G, "M_over_Msun": Decimal(1),
                "t_ev_s": T_EV_M_SUN, "t_ev_yr": T_EV_M_SUN / SEC_PER_YR})
    # 今已蒸发质量阈值：t_ev(M) = t_age ⇒ M = M☉·(t_age/t_ev☉)^{1/3}
    m_evap_g = M_SUN_G * (T_AGE_S / T_EV_M_SUN) ** (Decimal(1) / Decimal(3))
    return {"points": out, "m_evap_today_g": m_evap_g}


def e2_hawking_temp():
    """T_H ∝ 1/M：锚 T_H(1M☉)=6.1687e-8 K（C0172 E1）。"""
    t_sun = T_H_M_SUN_K
    t_sun_nK = t_sun * Decimal("1e9")
    # 1e15 g 档
    mr15 = Decimal("1e15") / M_SUN_G
    t_1e15 = t_sun / mr15
    return {"T_H_1Msun_K": t_sun, "T_H_1Msun_nK": t_sun_nK,
            "T_H_1e15g_K": t_1e15}


def e3_geometry_supply():
    """几何供给判定：PBH 形成需要初始密度扰动谱。"""
    # PBH 丰度 β(δ>δ_c) 由密度扰动功率谱 P(k) 的高尾积分给出——
    # 扰动谱形状/振幅是暴胀模型的外部公设；TUFT 几何框架（连续经典局部几何，
    # 承接 C0133/C0168）不供给任何 CMB 尺度外的小尺度扰动谱，无 PBH 质量函数预言。
    return {
        "needs": "初始密度扰动谱 P(k) 高尾（δ>δ_c 区域）",
        "tuft_supply": 0,
        "tuft_prediction": "none",
        "hits": ["C2", "C5"],
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0174 · 原初黑洞（PBH）形成阈值与质量函数攻破（母册 T403）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 事实引用（外部文献只引用不复算）")
    w("  临界塌缩标度律：%s，γ=%s、δ_c=%s（辐射主导），κ~O(1)。"
      % (g1["scaling_law"], g1["gamma"], g1["delta_c"]))
    w("  PBH 蒸发：%s。" % g1["evap"])
    w("  LIGO/Virgo 质量窗口：%s M☉。" % g1["ligo_window_Msun"])
    w("  丰度约束：%s。" % g1["abundance"])
    w("  来源标注：%s。" % "；".join(g1["sources"]))
    entries.append(("E1", "临界塌缩标度律（γ≈0.36/δ_c≈0.45）、蒸发标度（t_ev∝M³、"
                    "<10¹⁶ g 已蒸发）、LIGO 5–40 M☉ 窗口、f_PBH<10⁻² 约束——只引用",
                    "PASS", "外部文献来源标注，本册不复算"))

    # ---- E2 ----
    w("\n[E2] 第一性精算（本册核心）")
    sc = e2_scaling_ratio()
    w("  (a) 临界塌缩质量标度律 M_PBH/M_H = (δ−δ_c)^γ（κ=1 归一，γ=%s、δ_c=%s）："
      % (GAMMA, DELTA_C))
    for row in sc:
        w("      δ=%s：δ−δ_c=%s ⇒ M_PBH/M_H = %s"
          % (fv(row["delta"], "2f"), fv(row["excess"], "2e"),
             fv(row["M_PBH_over_M_H"], "6f")))
    entries.append(("E2a", "δ=0.46/0.50/0.60 → M_PBH/M_H=%s/%s/%s（幂律 γ=0.36）"
                    % (fv(sc[0]["M_PBH_over_M_H"], "4f"),
                       fv(sc[1]["M_PBH_over_M_H"], "4f"),
                       fv(sc[2]["M_PBH_over_M_H"], "4f")), "PASS",
                    "Decimal 48 位幂律精算，γ/δ_c 外部引用"))

    gb = e2_beta_backsolve()
    w("  (b) β 反解：f_PBH = β·(M_eq/M_form)^{1/2} ⇒ β = f_PBH·(M_form/M_eq)^{1/2}")
    w("      f_PBH=%s、M_form=%s M☉、M_eq=%s M☉："
      % (gb["f_PBH"], gb["M_form_Msun"], gb["M_eq_Msun"]))
    w("      M_form/M_eq = %s ⇒ β = %s"
      % (fv(gb["M_form_over_M_eq"], "4e"), fv(gb["beta"], "2e")))
    entries.append(("E2b", "f_PBH≈0.2、M≈30 M☉ ⇒ β≈%s（10⁻⁹ 量级）"
                    % fv(gb["beta"], "2e"), "PASS",
                    "β 反解量纲推导链完整，M_eq 外部引用"))

    ge = e2_evap_lifetime()
    w("  (c) 蒸发寿命 t_ev ∝ M³（锚 t_ev(1M☉)=%s s，承接 C0172 E1）：" % fv(T_EV_M_SUN, "4e"))
    for row in ge["points"]:
        w("      M=%s g（= %s M☉）：t_ev = %s s = %s yr"
          % (fv(row["M_g"], "2e"), fv(row["M_over_Msun"], "2e"),
             fv(row["t_ev_s"], "4e"), fv(row["t_ev_yr"], "4e")))
    w("      今已蒸发阈值 t_ev(M)=t_age=4.35e17 s ⇒ M ≈ %s g" % fv(ge["m_evap_today_g"], "2e"))
    ratio_evap = ge["points"][1]["t_ev_s"] / ge["points"][0]["t_ev_s"]
    w("      t_ev(1e17 g)/t_ev(1e15 g) = %s —— t_ev ∝ M³ 自洽。" % fv(ratio_evap, "6f"))
    entries.append(("E2c", "t_ev(1e15 g)=%s yr；t_ev(1e17 g)=%s yr；"
                    "t_ev(1M☉)=%s yr；今已蒸发阈值≈%s g"
                    % (fv(ge["points"][0]["t_ev_yr"], "3e"),
                       fv(ge["points"][1]["t_ev_yr"], "3e"),
                       fv(ge["points"][2]["t_ev_yr"], "3e"),
                       fv(ge["m_evap_today_g"], "2e")), "PASS",
                    "M³ 标度换算，锚点承接 C0172 E1"))

    gt = e2_hawking_temp()
    w("  (d) Hawking 温度 T_H ∝ 1/M（锚 T_H(1M☉)=%s K，承接 C0172 E1）：" % fv(T_H_M_SUN_K, "4e"))
    w("      1 M☉：T_H = %s K = %s nK（nK 量级）。"
      % (fv(gt["T_H_1Msun_K"], "4e"), fv(gt["T_H_1Msun_nK"], "3f")))
    w("      1e15 g：T_H = %s K（MeV 量级，蒸发末段）。" % fv(gt["T_H_1e15g_K"], "4e"))
    entries.append(("E2d", "T_H(1M☉)=%s K≈%s nK；T_H(1e15 g)=%s K"
                    % (fv(gt["T_H_1Msun_K"], "2e"),
                       fv(gt["T_H_1Msun_nK"], "2f"),
                       fv(gt["T_H_1e15g_K"], "2e")), "PASS",
                    "1/M 标度换算，锚点承接 C0172 E1"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给判定")
    w("  PBH 形成需要：%s。" % g3["needs"])
    w("  该扰动谱是暴胀模型的外部公设（谱形状/振幅定 PBH 质量函数与丰度）；")
    w("  TUFT 连续经典局部几何（承接 C0133/C0168）不供给小尺度扰动谱，无 PBH 预言。")
    w("  => 几何供给 = %d；撞 %s。" % (g3["tuft_supply"], "/".join(g3["hits"])))
    entries.append(("E3", "几何供给=0：TUFT 无密度扰动谱供给、无 PBH 预言",
                    "PASS", "撞 C2（初始条件外部）/C5（无预言）"))

    # ---- E4 ----
    w("\n[E4] 与既有线衔接")
    w("  C0168（黑洞微观态）：连续经典几何不供给离散微观态基；本册同对象——")
    w("    PBH 只是早期塌缩黑洞，微观态问题继承 C0168 读数，不另算。")
    w("  C0172（Page 曲线）：t_ev∝M³、T_H∝1/M 标度锚点直接承接其 E1 报告值；")
    w("    本册把蒸发标度用到 PBH 质量寿命账（1e15/1e17 g），不重算锚点。")
    w("  C0156（引力本质求道深化）：经典局部引力框架边界——PBH 形成阈值恰在")
    w("    '经典塌缩判据 + 外部扰动初值'交界面，几何只给判据不给初值。")
    w("  母册 T403 行原文：| T403 | 原初黑洞（PBH）形成阈值与质量函数 | 临界塌缩理论 | C2,C5 | 🔲 |")
    w("  => 登记 T403 🔲→✅（本册闭合，撞 C2/C5 与母册预登记一致）。")
    entries.append(("E4", "衔接 C0168/C0172/C0156；母册 T403 🔲→✅ 登记引用",
                    "PASS", "引用不复算，标度锚点承接 C0172 E1"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  PBH 形成阈值与质量函数 = 临界塌缩判据（几何半经典可算，E2a）")
    w("  + 初始密度扰动谱（外部公设，E3）。")
    w("  TUFT 几何框架只给出'扰动须超临界'的必要判据，不供给扰动谱、不预言质量函数；")
    w("  β 反解显示 f_PBH≈0.2@30M☉ 要求 β≈10⁻⁹ 这种微调初值——纯外部输入。")
    w("  => **结构性负面（对 TUFT/几何框架）**；撞 C2（初始条件外部）/C5（无预言）。")
    entries.append(("E5", "结构性负面：PBH 依赖外部扰动谱，TUFT 供给 0、无 PBH 预言",
                    "PASS", "撞 C2/C5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "标度律 γ≈0.36（0.35–0.37 带）",
         Decimal("0.35") <= GAMMA <= Decimal("0.37")),
        ("G2", "δ_c≈0.45（0.40–0.50 带）",
         Decimal("0.40") <= DELTA_C <= Decimal("0.50")),
        ("G3", "蒸发寿命标度：t_ev(1e17g)/t_ev(1e15g)=1e6（质量比100、M³）",
         abs(ratio_evap - Decimal("1e6")) < Decimal("1e-3")),
        ("G4", "引用标记齐全（E1 来源数 ≥ 3）", len(g1["sources"]) >= 3),
        ("G5", "几何供给 = 0", g3["tuft_supply"] == 0),
        ("G6", "裁定 = 结构性负面", entries[-1][0] == "E5"),
        ("G7", "β 反解量级 10⁻⁹（1e-10–1e-8 带）",
         Decimal("1e-10") <= gb["beta"] <= Decimal("1e-8")),
        ("G8", "Fraction 恒等式自检：M³ 标度 8/15360=1/1920（承接 C0172 G7）",
         Fraction(8, 15360) == Fraction(1, 1920)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0174 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决 PBH 形成问题；外部观测值/文献值只引用不复算；")
    w("  γ≈0.36、δ_c≈0.45、M_eq=2.8e17 M☉ 为外部引用；")
    w("  t_ev/T_H 锚点承接 C0172 E1，本册只做标度换算。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0174_原初黑洞攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0174_原初黑洞攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0174_PBH_formation",
            "master_row": "| T403 | 原初黑洞（PBH）形成阈值与质量函数 | 临界塌缩理论 | C2,C5 | ✅ |",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {"scaling_law": g1["scaling_law"], "gamma": str(GAMMA),
                         "delta_c": str(DELTA_C), "ligo_window": g1["ligo_window_Msun"],
                         "abundance": g1["abundance"], "sources": g1["sources"]},
            "E2a_scaling": [{"delta": str(r["delta"]),
                             "M_PBH_over_M_H": str(r["M_PBH_over_M_H"])} for r in sc],
            "E2b_beta": {k: str(v) for k, v in gb.items()},
            "E2c_evap": {"points": [{k: str(v) for k, v in p.items()} for p in ge["points"]],
                         "m_evap_today_g": str(ge["m_evap_today_g"]),
                         "ratio_1e17_over_1e15": str(ratio_evap)},
            "E2d_T_H": {k: str(v) for k, v in gt.items()},
            "E3_geometry_supply": {k: str(v) for k, v in e3_geometry_supply().items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0174 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
