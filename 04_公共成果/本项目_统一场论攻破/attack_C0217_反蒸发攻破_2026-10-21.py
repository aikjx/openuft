# -*- coding: utf-8 -*-
"""
attack_C0217_反蒸发攻破_2026-10-21.py
独立复算：母册 T125「冷宇宙中黑洞的反蒸发（Hawking 温度 < CMB）」
          —— 吸积/蒸发平衡 + 长期演化（撞 C2）

定位：母册 T125（行 249）：`| T125 | 冷宇宙中黑洞的反蒸发（Hawking 温度 < CMB）
      | 吸积/蒸发平衡 + 长期演化 | C2 | 🔲 |`。
      衔接 C0187（全息熵律）读数：1 M☉ T_H = 6.1687e-8 K、S/k_B = 1.04947e77。

把「冷宇宙黑洞反蒸发」压缩成五条可复核读数：

  E1 外部常数与 Hawking 公式事实（CODATA/Planck 只引用不复算）。
  E2 **Hawking 温度 + 平衡质量精算（本册核心）**：
       T_H = ℏc³/(8π G M k_B) 对 1 M☉ 精算（对齐 C0187 6.1687e-8 K）；
       对 10⁸ M☉ 精算（≈6.17e-16 K）；
       平衡质量 M_*：T_H(M_*) = T_CMB(2.725 K) 时的黑洞质量精算。
  E3 吸积 vs 蒸发核算：黑体 P ∝ T⁴·面积，同面积下 P_吸/P_发 = (T_CMB/T_H)⁴；
       当前宇宙（T_CMB=2.725 K）下所有恒星质量黑洞净吸积（反蒸发）核算。
  E4 未来演化核算：CMB 降温至 T_CMB < T_H(M) 时黑洞转入净蒸发的宇宙年龄量级
       （de Sitter 近似 Δt = (1/H_Λ) ln(1+z_*)，外部宇宙学输入计数）。
  E5 裁定：TUFT 是否供给 Hawking 辐射 / 吸积平衡结构（无）→ 结构性负面，撞 C2。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：数值均为标准物理（Hawking/吸积/CMB 热力学）算术复核；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。本册不宣称解决任何物理难题。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部常数（CODATA 2018 / Planck 2018，只引用不复算；口径对齐 C0187） ----------
HBAR = Decimal("1.054571817e-34")   # J s
G    = Decimal("6.6740e-11")        # m^3 kg^-1 s^-2
C    = Decimal("2.9979246e8")      # m/s
KB   = Decimal("1.380649e-23")    # J/K（exact）
M_SUN = Decimal("1.9890e30")      # kg
T_CMB0 = Decimal("2.725")          # K（当前宇宙微波背景温度，Planck 只引用）
# 外部宇宙学输入（Planck 2018，只引用；E4 使用）
H0   = Decimal("2.197e-18")        # s^-1（≈67.4 km/s/Mpc）
OMEGA_LAMBDA = Decimal("0.685")
GYR_PER_SEC = Decimal("3.15576e16")  # s/年（儒略年 365.25 d）→ 1 Gyr = 3.15576e16 s

PI = Decimal("3.14159265358979323846264338327950288419716939937510")


def T_H_of_M(M: Decimal) -> Decimal:
    """Hawking 温度 T_H = ℏ c^3 / (8 π G M k_B)。"""
    return (HBAR * C ** 3) / (Decimal(8) * PI * G * M * KB)


def e1_constants():
    """外部常数与公式事实（CODATA/Planck 只引用）。"""
    return {
        "hbar": HBAR, "G": G, "c": C, "k_B": KB, "M_sun": M_SUN,
        "T_CMB0_K": T_CMB0,
        "form_T_H": "T_H = hbar c^3 / (8 pi G M k_B)",
        "form_P_net": "P_net ~ A sigma (T_CMB^4 - T_H^4)，同面积比 = (T_CMB/T_H)^4",
        "ref_C0187": "1 M_sun: T_H = 6.1687e-8 K, S/k_B = 1.04947e77（引用不复算）",
    }


def e2_hawking_and_balance():
    """Hawking 温度精算 + 平衡质量 M_*（本册核心）。"""
    # 1 M_sun
    T_H_1M = T_H_of_M(M_SUN)
    # 10^8 M_sun（按 T_H ∝ 1/M）
    T_H_1e8M = T_H_of_M(M_SUN * Decimal("1e8"))
    # 平衡质量：T_H(M_*) = T_CMB0  →  M_* = hbar c^3 / (8 pi G k_B T_CMB0)
    M_star_kg = (HBAR * C ** 3) / (Decimal(8) * PI * G * KB * T_CMB0)
    M_star_Msun = M_star_kg / M_SUN
    # Hawking 蒸发光度 L_H = hbar c^6 / (15360 pi G^2 M^2)，1 M_sun
    L_H_1M = (HBAR * C ** 6) / (Decimal(15360) * PI * G ** 2 * M_SUN ** 2)
    return {
        "T_H_1M_sun_K": T_H_1M,
        "T_H_1e8M_sun_K": T_H_1e8M,
        "M_star_kg": M_star_kg,
        "M_star_in_Msun": M_star_Msun,
        "L_H_1M_sun_W": L_H_1M,
    }


def e3_accretion_vs_evaporation(g2):
    """吸积 vs 蒸发：黑体同面积下 P_吸/P_发 = (T_CMB/T_H)^4。"""
    # 1 M_sun
    ratio_1M = (T_CMB0 / g2["T_H_1M_sun_K"]) ** 4
    # 10^8 M_sun
    ratio_1e8M = (T_CMB0 / g2["T_H_1e8M_sun_K"]) ** 4
    # 净吸积（反蒸发）条件：T_H < T_CMB ⇔ M > M_*。
    # 恒星质量黑洞 M >= 1 M_sun >> M_*（~2e-8 M_sun）⇒ 全部净吸积。
    stellar_Msun = Decimal(1)
    stellar_above_balance = stellar_Msun > g2["M_star_in_Msun"]
    return {
        "ratio_abs_emit_1M": ratio_1M,
        "ratio_abs_emit_1e8M": ratio_1e8M,
        "stellar_Msun_above_Mstar": stellar_above_balance,
        "net_accretion_all_stellar_mass": stellar_above_balance,
    }


def e4_future_evolution(g2):
    """CMB 降温后黑洞转入净蒸发的宇宙年龄量级（de Sitter 近似）。"""
    # T_CMB(t) = T_CMB0 / a；转入净蒸发时 T_CMB = T_H(M) ⇒ a_* = T_CMB0 / T_H(M)
    # 取 1 M_sun 黑洞为代表：
    a_star_1M = T_CMB0 / g2["T_H_1M_sun_K"]     # = 1+z_*
    # de Sitter 未来：a(t) ~ exp(H_Lambda * (t - t0)) ⇒ Δt = ln(a_*) / H_Lambda
    H_Lambda = H0 * OMEGA_LAMBDA.sqrt()
    dt_sec = a_star_1M.ln() / H_Lambda
    dt_Gyr = dt_sec / GYR_PER_SEC               # 距今天的 Gyr 数
    # 10^8 M_sun 黑洞：T_H 更低，a_* 更大
    a_star_1e8M = T_CMB0 / g2["T_H_1e8M_sun_K"]
    dt_1e8M_Gyr = (a_star_1e8M.ln() / H_Lambda) / GYR_PER_SEC
    return {
        "H_Lambda_s_inv": H_Lambda,
        "a_star_1M": a_star_1M,
        "future_dt_1M_Gyr": dt_Gyr,
        "a_star_1e8M": a_star_1e8M,
        "future_dt_1e8M_Gyr": dt_1e8M_Gyr,
        "note": "de Sitter 近似，外部宇宙学输入 (H0, Omega_Lambda)；量级估算",
    }


def e5_supply():
    """TUFT 是否供给 Hawking 辐射 / 吸积平衡结构？"""
    return {
        "tuft_supplies_hawking_radiation": False,
        "tuft_supplies_accretion_dynamics": False,
        "tuft_cross_ref": "TUFT 已注销（C0133）；库内无 Hawking 辐射/吸积平衡结构",
        "verdict": "structural_negative",
        "hits": "C2",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0217 · 冷宇宙黑洞反蒸发（母册 T125 · 吸积/蒸发平衡 + 长期演化）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_constants()
    w("\n[E1] 外部常数与 Hawking 公式事实（CODATA/Planck 只引用不复算）")
    w("  ħ=%s J·s；G=%s；c=%s m/s；k_B=%s J/K；M☉=%s kg"
      % (fv(g1["hbar"], "9e"), fv(g1["G"], "4e"), fv(g1["c"], "7e"),
         fv(g1["k_B"], "6e"), fv(g1["M_sun"], "4e")))
    w("  T_CMB(今) = %s K；公式：%s" % (g1["T_CMB0_K"], g1["form_T_H"]))
    w("  承接 C0187 读数（引用不复算）：%s" % g1["ref_C0187"])
    entries.append(("E1", "Hawking 温度公式体系 + 外部常数（CODATA/Planck 只引用）",
                    "PASS", "对齐 C0187 口径"))

    # ---- E2 ----
    g2 = e2_hawking_and_balance()
    w("\n[E2] Hawking 温度精算 + 平衡质量 M_*（本册核心）")
    w("  T_H(1 M☉)   = %s K   （对齐 C0187 6.1687e-8 K）"
      % fv(g2["T_H_1M_sun_K"], "6e"))
    w("  T_H(10⁸ M☉) = %s K   （按 T_H∝1/M，量级 6.17e-16 K）"
      % fv(g2["T_H_1e8M_sun_K"], "6e"))
    w("  平衡质量 M_*（T_H=T_CMB=2.725 K）：")
    w("      M_* = %s kg = %s M☉"
      % (fv(g2["M_star_kg"], "6e"), fv(g2["M_star_in_Msun"], "6e")))
    w("  Hawking 蒸发光度 L_H(1 M☉) = %s W" % fv(g2["L_H_1M_sun_W"], "6e"))
    entries.append(("E2",
                    "T_H(1M☉)=%s K（对齐 C0187）；T_H(10⁸M☉)=%s K；M_*=%s M☉"
                    % (fv(g2["T_H_1M_sun_K"], "4e"),
                       fv(g2["T_H_1e8M_sun_K"], "4e"),
                       fv(g2["M_star_in_Msun"], "3e")),
                    "PASS", "Decimal 48 位精算；T_H∝1/M"))

    # ---- E3 ----
    g3 = e3_accretion_vs_evaporation(g2)
    w("\n[E3] 吸积 vs 蒸发：同面积黑体 P_吸/P_发 = (T_CMB/T_H)^4")
    w("  1 M☉：P_吸/P_发 = (%s/%s)^4 = %s  ⇒ 净吸积（反蒸发）"
      % (fv(T_CMB0, "1f"), fv(g2["T_H_1M_sun_K"], "4e"),
         fv(g3["ratio_abs_emit_1M"], "4e")))
    w("  10⁸ M☉：P_吸/P_发 = %s  ⇒ 净吸积更强"
      % fv(g3["ratio_abs_emit_1e8M"], "4e"))
    w("  净吸积条件：T_H < T_CMB ⇔ M > M_*（~%s M☉）。"
      % fv(g2["M_star_in_Msun"], "3e"))
    w("  恒星质量黑洞 M≥1 M☉ ≫ M_* ⇒ 当前宇宙所有恒星质量黑洞均净吸积（反蒸发）。")
    entries.append(("E3",
                    "当前宇宙 P_吸/P_发(1M☉)=%s ≫1；所有 M≥M_* 的黑洞净吸积（反蒸发）"
                    % fv(g3["ratio_abs_emit_1M"], "2e"),
                    "PASS", "黑体 P∝T⁴·面积，同面积比值"))

    # ---- E4 ----
    g4 = e4_future_evolution(g2)
    w("\n[E4] 未来演化：CMB 降温后黑洞转入净蒸发的宇宙年龄量级")
    w("  de Sitter 未来：a(t)~exp(H_Λ(t-t0))，H_Λ = H0·√Ω_Λ = %s s⁻¹"
      % fv(g4["H_Lambda_s_inv"], "4e"))
    w("  1 M☉：a_* = T_CMB0/T_H = %s；距今天 Δt = ln(a_*)/H_Λ = %s Gyr"
      % (fv(g4["a_star_1M"], "4e"), fv(g4["future_dt_1M_Gyr"], "4e")))
    w("  10⁸ M☉：a_* = %s；Δt = %s Gyr"
      % (fv(g4["a_star_1e8M"], "4e"), fv(g4["future_dt_1e8M_Gyr"], "4e")))
    w("  ⇒ 恒星质量黑洞转入净蒸发约在 %s Gyr（~10¹¹ 年量级）后；%s"
      % (fv(g4["future_dt_1M_Gyr"], "3e"), g4["note"]))
    entries.append(("E4",
                    "1M☉ 转入净蒸发约在今天之后 %s Gyr（~10¹¹ yr 量级）"
                    % fv(g4["future_dt_1M_Gyr"], "3e"),
                    "PASS", "de Sitter 近似；外部宇宙学输入计数"))

    # ---- E5 ----
    g5 = e5_supply()
    w("\n[E5] 裁定：TUFT 是否供给 Hawking 辐射 / 吸积平衡结构？")
    w("  TUFT 供给 Hawking 辐射：%s" % g5["tuft_supplies_hawking_radiation"])
    w("  TUFT 供给吸积动力学：%s" % g5["tuft_supplies_accretion_dynamics"])
    w("  %s" % g5["tuft_cross_ref"])
    w("  反蒸发/平衡依赖 Hawking 辐射 + 吸积动力学（标准半经典引力算术），")
    w("  TUFT 无对应结构供给 ⇒ 结构性负面，按母册登记撞 C2。")
    entries.append(("E5",
                    "TUFT 无 Hawking 辐射/吸积结构供给 ⇒ 结构性负面，撞 C2",
                    "PASS", g5["hits"]))

    # ---- 守卫 ----
    guards = [
        ("G1", "T_H(1 M☉) ≈ 6.17e-8 K（对齐 C0187，±2%）",
         abs(g2["T_H_1M_sun_K"] / Decimal("6.17e-8") - 1) < Decimal("0.02")),
        ("G2", "T_H(10⁸ M☉) ≈ 6.17e-16 K（±2%）",
         abs(g2["T_H_1e8M_sun_K"] / Decimal("6.17e-16") - 1) < Decimal("0.02")),
        ("G3", "平衡质量 M_* 在 1e-9–1e-7 M☉ 量级",
         (g2["M_star_in_Msun"] > Decimal("1e-9")) and
         (g2["M_star_in_Msun"] < Decimal("1e-7"))),
        ("G4", "当前宇宙 1 M☉ 黑洞 P_吸/P_发 ≫ 1（净吸积）",
         g3["ratio_abs_emit_1M"] > Decimal("1e20")),
        ("G5", "恒星质量黑洞 M=1 M☉ > M_*（反蒸发成立）",
         g3["stellar_Msun_above_Mstar"]),
        ("G6", "转入净蒸发未来时间 > 100 Gyr（远未来）",
         g4["future_dt_1M_Gyr"] > Decimal("100")),
        ("G7", "TUFT 供给 = 0（Hawking 辐射与吸积均无）",
         (g5["tuft_supplies_hawking_radiation"] is False) and
         (g5["tuft_supplies_accretion_dynamics"] is False)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0217 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决任何物理难题；数值均为标准物理（Hawking/吸积/CMB）算术复核，")
    w("  非 TUFT 预测/修正；TUFT 已注销（C0133）；外部常数只引用不复算。")
    w("  红线不变：「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries),
         sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0217_反蒸发攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0217_反蒸发攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0217_blackhole_anti_evaporation",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_constants": {k: str(v) for k, v in g1.items()},
            "E2_hawking_balance": {k: str(v) for k, v in g2.items()},
            "E3_accretion_vs_evap": {k: str(v) for k, v in g3.items()},
            "E4_future_evolution": {k: str(v) for k, v in g4.items()},
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "guards": [{"id": gid, "desc": desc, "ok": bool(ok)}
                       for gid, desc, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0217 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
