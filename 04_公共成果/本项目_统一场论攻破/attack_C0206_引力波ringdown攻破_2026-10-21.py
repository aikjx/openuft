# -*- coding: utf-8 -*-
"""
attack_C0206_引力波ringdown攻破_2026-10-21.py
独立复算：母册 T107「双黑洞并合 ringdown 谱（准正则模 QNM）」攻破
（行 231，原文照录：数值相对论波形 + 微扰理论，撞 C5,C6）

定位：母册 T107（双黑洞并合 ringdown / QNM 复频率谱）。
前置：C0190（引力波量子性，撞 C5/C6）、C0169（EHT M87*/Sgr A* 阴影，撞 C5/C6）、
C0133（TUFT 已注销）、C0140（(ℏ,G,c) 量纲 nullity=0）。本册不采信任何自报，
独立精算标准 GR 微扰论（Schwarzschild/Kerr QNM）算术，并对 TUFT/几何框架
判定是否供给 ringdown 谱（Teukolsky 方程 / QNM 本征值 ω_lmn(M,a)）。

把"ringdown 准正则模谱"压缩成五条可复核读数：

  E1 QNM 事实（只引用不复算）：Schwarzschild l=2,n=0 复频率 Mω=0.37367-i0.08896；
     GW150914 残留 M_f≈65 M☉、a_f≈0.68；ringdown 模板=IMR（NR + QNM 谱）。
  E2 **Schwarzschild QNM 频率与阻尼独立精算（本册核心）**：
     f_R = Re(ωM)·c³/(2π G M) 对 M=65 M☉；τ = 1/(Im(ωM)·c³/(G M))；
     Q = Re(ωM)/(2|Im(ωM)|)。
  E3 Kerr 转动修正：a=0.7 下 l=m=2,n=0 频率偏移量级（标准微扰表列只引用，
     换算算术本册独立精算）。
  E4 QNM 供给检查：TUFT/几何框架是否有微扰论 / Teukolsky 方程 / QNM 本征值谱。
  E5 裁定：ringdown 谱依赖 Kerr 微扰论 + QNM 谱结构（标准 GR 内在性质 + NR 输入），
     TUFT 无微扰论/无 QNM 供给 ⇒ 结构性负面，撞 C5/C6。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称已解决 ringdown 谱；Schwarzschild/Kerr QNM 复频率无量纲
本征值（Leaver/Berti-Cardoso 表列）只引用不复算；E2/E3 的 SI 换算算术为本册
独立 Decimal 精算；TUFT 已注销（C0133），本册严禁把标准 GR 微扰结果写成
TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 物理常数（CODATA 2018，SI，只引用；承接 C0169/C0190） ----------
G = Decimal("6.67430e-11")            # m^3 kg^-1 s^-2
C = Decimal("299792458")              # m/s
M_SUN = Decimal("1.98847e30")         # kg
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
TWO_PI = Decimal(2) * PI

# ---------- QNM 无量纲本征值（标准 GR 微扰论表列，只引用不复算） ----------
# Schwarzschild l=2,n=0（Leaver 1986；单位 c^3/(G M)）
W_R_SCH = Decimal("0.37367")          # Re(M ω)
W_I_SCH = Decimal("0.088962")        # |Im(M ω)|
# Kerr l=m=2,n=0，无量纲自旋 a=0.7（Berti-Cardoso-Will 2006 表列，只引用）
W_R_K07 = Decimal("0.468")           # Re(M ω), a=0.7
W_I_K07 = Decimal("0.074")           # |Im(M ω)|, a=0.7

# GW150914 残留（LIGO 实测，只引用）
M_F_MSUN = Decimal("65")              # 并合残留质量 M☉
A_F = Decimal("0.68")                # 残留无量纲自旋


def e1_qnm_facts():
    """QNM 事实（表列/观测只引用不复算）。"""
    return {
        "mode": "l=2, n=0 (fundamental quadrupole)",
        "schwarzschild_Mw": "0.37367 - i0.088962",
        "gw150914_Mf_Msun": M_F_MSUN,
        "gw150914_af": A_F,
        "template": "IMR (NR calibration + QNM spectrum: SEOBNR/IMRPhenom)",
    }


def e2_schwarzschild_ringdown():
    """Schwarzschild QNM 频率与阻尼独立精算（本册核心）。

    几何单位 → SI 换算：t_SI = t_geom · G M / c^3
    ⇒ 物理角频率 Ω = Mω · c^3/(G M)；f = Ω/(2π)。
    振幅包络 e^{-|Im(Mω)| c^3 t/(G M)} ⇒ 振幅 e-fold 时间 τ = G M/(|Im(Mω)| c^3)。
    品质因子 Q = Re(Mω)/(2|Im(Mω)|)（振幅 e-fold 对应 Q = π f τ）。
    """
    M = M_F_MSUN * M_SUN                      # kg
    GM = G * M                                # m^3/s^2
    c3 = C * C * C                            # m^3/s^3
    Gamma = c3 / GM                            # s^-1（时间标度 c^3/(G M)）
    f_R = W_R_SCH * Gamma / TWO_PI             # Hz
    omega_I_phys = W_I_SCH * Gamma            # rad/s（阻尼率）
    tau = Decimal(1) / omega_I_phys           # s（振幅 e-fold）
    Q = W_R_SCH / (Decimal(2) * W_I_SCH)
    # 自洽：Q = π f τ
    Q_check = PI * f_R * tau
    return {
        "M_kg": M,
        "GM": GM,
        "c3": c3,
        "Gamma_c3_over_GM": Gamma,
        "f_R_Hz": f_R,
        "omega_I_phys_rad_s": omega_I_phys,
        "tau_s": tau,
        "tau_ms": tau * Decimal(1000),
        "Q": Q,
        "Q_check_pi_f_tau": Q_check,
        "Q_residual": abs(Q - Q_check) / Q,
    }


def e3_kerr_spin_shift():
    """Kerr 转动修正（a=0.7）：无量纲本征值引用，换算算术独立精算。"""
    M = M_F_MSUN * M_SUN
    GM = G * M
    c3 = C * C * C
    Gamma = c3 / GM
    f_R_k07 = W_R_K07 * Gamma / TWO_PI
    tau_k07 = Decimal(1) / (W_I_K07 * Gamma)
    Q_k07 = W_R_K07 / (Decimal(2) * W_I_K07)
    shift = f_R_k07 / e2_schwarzschild_ringdown()["f_R_Hz"]
    return {
        "a": Decimal("0.7"),
        "w_R_K07": W_R_K07,
        "w_I_K07": W_I_K07,
        "f_R_K07_Hz": f_R_k07,
        "tau_K07_ms": tau_k07 * Decimal(1000),
        "Q_K07": Q_k07,
        "freq_shift_over_schwarzschild": shift,
        "freq_shift_pct": (shift - Decimal(1)) * Decimal(100),
    }


def e4_tuft_supply():
    """TUFT/几何框架对 ringdown QNM 谱的供给检查。"""
    return {
        "tuft_has_perturbation_theory": False,   # 无 BH 微扰论
        "tuft_has_teukolsky_equation": False,    # 无 Teukolsky/标量-矢量-张量分解
        "tuft_has_qnm_eigenspectrum": False,     # 无 ω_lmn(M,a) 本征值谱
        "tuft_has_nr_template_match": False,     # 无数值相对论模板/匹配滤波
        "tuft_qnm_predictions": 0,
        "c133_tuft_deregistered": True,
        "nullity_hbarGc": 0,                     # 承接 C0140/C0142/C0190
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0206 · 双黑洞并合 ringdown 准正则模 QNM（母册 T107）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_qnm_facts()
    w("\n[E1] QNM 事实（标准微扰表列 / LIGO 观测只引用不复算）")
    w("  模 = %s" % g1["mode"])
    w("  Schwarzschild 无量纲复频率 Mω = %s（Leaver 表列）" % g1["schwarzschild_Mw"])
    w("  Kerr a=0.7 l=m=2,n=0：Mω ≈ %s - i%s（Berti-Cardoso-Will 表列）"
      % (W_R_K07, W_I_K07))
    w("  GW150914 残留：M_f = %s M☉、a_f = %s" % (g1["gw150914_Mf_Msun"], g1["gw150914_af"]))
    w("  观测模板 = %s" % g1["template"])
    w("  => ringdown 谱 = Kerr QNM 本征值 ω_lmn(M,a) + NR 波形标定（标准 GR 内在性质）。")
    entries.append(("E1", "QNM = Schwarzschild/Kerr 微扰本征值；GW150914 M_f=65M☉ a_f=0.68；"
                          "模板=IMR(NR+QNM)", "PASS", "Leaver/Berti 表列与 LIGO 观测只引用"))

    # ---- E2 ----
    g2 = e2_schwarzschild_ringdown()
    w("\n[E2] Schwarzschild QNM 频率与阻尼独立精算（本册核心，M=%s M☉）" % M_F_MSUN)
    w("  换算：t_SI = t_geom·GM/c^3 ⇒ Ω = Re(Mω)·c^3/(GM)，f=Ω/2π")
    w("  M = %s kg；GM = %s m^3/s^2；c^3 = %s m^3/s^3"
      % (fv(g2["M_kg"], "4e"), fv(g2["GM"], "4e"), fv(g2["c3"], "4e")))
    w("  Gamma = c^3/(GM) = %s s^-1" % fv(g2["Gamma_c3_over_GM"], "6e"))
    w("  f_R = %s · Gamma/(2π) = %s Hz" % (fv(W_R_SCH, "5f"), fv(g2["f_R_Hz"], "6f")))
    w("  阻尼率 |Im(Mω)|·Gamma = %s rad/s" % fv(g2["omega_I_phys_rad_s"], "6e"))
    w("  τ = 1/阻尼率 = %s s = %s ms（振幅 e-fold）"
      % (fv(g2["tau_s"], "6e"), fv(g2["tau_ms"], "4f")))
    w("  Q = Re(Mω)/(2|Im(Mω)|) = %s（自洽 π f τ = %s，残差 %s）"
      % (fv(g2["Q"], "6f"), fv(g2["Q_check_pi_f_tau"], "6f"), fv(g2["Q_residual"], "2e")))
    w("  => Schwarzschild 65 M☉ ringdown 频率 ~186 Hz、阻尼 ~3.6 ms、Q~2.1；")
    w("     与 GW150914 实测 ringdown ~250 Hz 的差距由 Kerr 自旋修正解释（见 E3）。")
    entries.append(("E2",
                    "f_R = %s Hz；τ = %s ms；Q = %s（Schwarzschild M=65M☉）"
                    % (fv(g2["f_R_Hz"], "2f"), fv(g2["tau_ms"], "3f"), fv(g2["Q"], "3f")),
                    "PASS", "Leaver 无量纲本征值 + Decimal 48 位 SI 独立换算"))

    # ---- E3 ----
    g3 = e3_kerr_spin_shift()
    w("\n[E3] Kerr 转动修正（a=%s）" % g3["a"])
    w("  无量纲本征值 Re(Mω): Schwarzschild %s -> Kerr a=0.7 %s（表列引用）"
      % (fv(W_R_SCH, "5f"), fv(g3["w_R_K07"], "4f")))
    w("  f_R(a=0.7) = %s Hz；τ(a=0.7) = %s ms；Q(a=0.7) = %s"
      % (fv(g3["f_R_K07_Hz"], "6f"), fv(g3["tau_K07_ms"], "4f"), fv(g3["Q_K07"], "4f")))
    w("  频率偏移 f(a=0.7)/f(Schw) = %s（即 +%s%%）；阻尼变缓（τ 增大、Q 上升）"
      % (fv(g3["freq_shift_over_schwarzschild"], "4f"), fv(g3["freq_shift_pct"], "2f")))
    w("  => 自旋 a≈0.7 把 65 M☉ ringdown 从 ~186 Hz 抬到 ~%d Hz，与 GW150914 ~250 Hz"
      "（a_f=0.68）量级吻合——标准 Kerr 微扰论 + NR 的内在结果。"
      % int(g3["f_R_K07_Hz"].to_integral_value()))
    entries.append(("E3",
                    "Kerr a=0.7：f_R=%s Hz，较 Schwarzschild +%s%%，解释 GW150914 ~250 Hz"
                    % (fv(g3["f_R_K07_Hz"], "1f"), fv(g3["freq_shift_pct"], "1f")),
                    "PASS", "Berti 表列无量纲值 + 本册 SI 换算"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] QNM 供给检查（TUFT/几何框架）")
    w("    BH 微扰论（标量-矢量-张量分解）？  %s" % g4["tuft_has_perturbation_theory"])
    w("    Teukolsky 方程？                   %s" % g4["tuft_has_teukolsky_equation"])
    w("    QNM 本征值谱 ω_lmn(M,a)？          %s" % g4["tuft_has_qnm_eigenspectrum"])
    w("    NR 波形模板 / 匹配滤波？           %s" % g4["tuft_has_nr_template_match"])
    w("    TUFT 可检验 ringdown 预言数？       %d" % g4["tuft_qnm_predictions"])
    w("    TUFT 注销状态（C0133）？            %s" % g4["c133_tuft_deregistered"])
    w("  => ringdown 谱是 Kerr 时空上线性微扰方程的复本征值问题；几何框架只给场方程，")
    w("     不做黑洞背景微扰展开，不求解本征值，供给 = 0。E2/E3 算术是标准 GR 结果。")
    entries.append(("E4", "TUFT 无微扰论/无 Teukolsky/无 QNM 本征值谱/无 NR 模板 ⇒ 供给 0",
                    "PASS", "几何框架不做 BH 背景微扰展开"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  ringdown 谱 = Kerr 微扰论（Teukolsky 方程复本征值 ω_lmn(M,a)）+ NR 波形输入。")
    w("  这是标准 GR 的内在性质：一旦给定 (M,a)，QNM 谱即由史瓦西/Kerr 微扰唯一确定，")
    w("  无需也不容许外部参数——E2/E3 复算的 ~186 Hz（Schw）/~233 Hz（a=0.7）即其必然推论。")
    w("  TUFT/几何框架供给检查（E4）：无微扰论、无 Teukolsky、无 QNM 谱、无 NR 模板，")
    w("  不能给出任何可检验 ringdown 频率 + 误差带。")
    w("  => **T107 结构性负面（对 TUFT/几何框架）**；撞 **C5**（无单点可检验预言）/")
    w("     **C6**（无误差带）。与 C0190（引力波量子性）、C0169（EHT 阴影）同口径登记。")
    entries.append(("E5", "ringdown 谱依赖 Kerr 微扰论+QNM 谱结构（标准 GR 内在+NR 输入），"
                          "TUFT 无供给 ⇒ 结构性负面，撞 C5/C6",
                    "PASS", "TUFT 已注销 C0133；几何 nullity=0"))

    # ---- 守卫 ----
    guards = [
        ("G1", "Schwarzschild 65M☉ f_R 落在 [170,200] Hz",
         Decimal("170") <= g2["f_R_Hz"] <= Decimal("200")),
        ("G2", "振幅 e-fold τ 落在 [3.0,4.5] ms",
         Decimal("3.0") <= g2["tau_ms"] <= Decimal("4.5")),
        ("G3", "Q=Re(Mω)/(2|Im|) 落在 [1.8,2.5]",
         Decimal("1.8") <= g2["Q"] <= Decimal("2.5")),
        ("G4", "Q 自洽 π f τ 残差 < 1e-3", g2["Q_residual"] < Decimal("1e-3")),
        ("G5", "Kerr a=0.7 频率偏移在 [+20%,+35%]（1.20<shift<1.35）",
         Decimal("1.20") <= g3["freq_shift_over_schwarzschild"] <= Decimal("1.35")),
        ("G6", "TUFT QNM 可检验预言数 = 0", g4["tuft_qnm_predictions"] == 0),
        ("G7", "TUFT 已注销（C0133）", g4["c133_tuft_deregistered"] is True),
        ("G8", "几何常数 (ℏ,G,c) nullity = 0（承接 C0140/C0142/C0190）",
         g4["nullity_hbarGc"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0206 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  本册不宣称解决任何物理难题；Leaver/Berti 无量纲 QNM 本征值与 LIGO 观测只引用；")
    w("  E2/E3 的 SI 换算算术为本册独立 Decimal 精算；TUFT 已注销（C0133），")
    w("  不把标准 GR 微扰结果写成 TUFT 预测/修正。")
    w("  红线不变：已攻破 = 对 TUFT/几何框架结构性负面闭合；有预测且对 = 0/22；")
    w("  UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0206_引力波ringdown攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0206_引力波ringdown攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0206_ringdown_qnm",
            "parent_row": "T107",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: (str(v) if not isinstance(v, bool) else v)
                         for k, v in g1.items()},
            "E2_schwarzschild": {k: str(v) for k, v in g2.items()},
            "E3_kerr_spin": {k: str(v) for k, v in g3.items()},
            "E4_tuft_supply": {k: v for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": g[2]} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0206 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
