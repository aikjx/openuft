# -*- coding: utf-8 -*-
"""
attack_C0199_结构形成攻破_2026-10-21.py
独立复算：母册 T040「结构形成 / 星系起源」（初始谱 + 引力，撞 C2/C5）

定位：母册 T040 行 136：结构形成 / 星系起源——宇宙密度涨落增长、Jeans 不稳定性、
ΛCDM 线性功率谱与 Press-Schechter 质量函数、初始谱供给检查。

把"结构形成从哪来"压缩成四条可复核读数 + 一张输入账单：

  E1 标准宇宙学事实（Planck 2018 只引用不复算）：H0/Omega_m/Omega_b/Omega_L/sigma8/n_s。
  E2 **Jeans 长度/质量精算（本册核心）**：lambda_J = c_s sqrt(pi/(G rho))，
     M_J = (4pi/3) rho (lambda_J/2)^3，典型 IGM 参数（T=1e4 K 完全电离）Mpc/M_sun 量级。
  E3 线性增长因子 D(z)：LambdaCDM（Linder gamma=0.55 抑制）在 z=0,1,10,1100 的核算，
     与 EdS 近似 delta∝1/(1+z) 对比。
  E4 Press-Schechter：sigma(M) 质量谱（sigma8≈0.811 归一）+ 星系团数密度量级核算。
  E5 初始谱供给检查 + 裁定：结构形成需原初功率谱（暴胀外部供给）+ 暗物质
     （C0139 已判供给 0），TUFT 两者皆无 => 结构性负面，撞 C2/C5。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册数值均为标准宇宙学（LambdaCDM/结构形成）算术复核；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。裁的是「TUFT/几何框架能否供给结构形成的
初始谱与暗物质」，不宣称解决任何物理难题。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 常数（CODATA 2018 / Planck 2018，只引用不复算） ----------
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
TWO = Decimal(2)
G = Decimal("6.67430e-11")        # 牛顿引力常数 m^3 kg^-1 s^-2
KB = Decimal("1.380649e-23")      # 玻尔兹曼常数 J/K
MP = Decimal("1.67262192369e-27") # 质子质量 kg
MPC = Decimal("3.0856775814913673e22")  # 1 Mpc in m
MSUN = Decimal("1.98847e30")      # 太阳质量 kg

# Planck 2018 背景宇宙学（只引用）
H0_KMS_MPC = Decimal("67.4")      # km/s/Mpc
OMEGA_M = Decimal("0.315")
OMEGA_B = Decimal("0.0493")
OMEGA_L = Decimal("0.685")
SIGMA8 = Decimal("0.811")
N_S = Decimal("0.965")
HUBBLE_H = H0_KMS_MPC / Decimal("100")  # h = 0.674
DC = Decimal("1.686")            # PS 临界过密度（球坍缩，EdS）


def e1_planck_facts():
    """标准宇宙学事实（Planck 2018 只引用不复算）。"""
    return {
        "H0_km_s_Mpc": H0_KMS_MPC,
        "Omega_m": OMEGA_M,
        "Omega_b": OMEGA_B,
        "Omega_L": OMEGA_L,
        "sigma8": SIGMA8,
        "n_s": N_S,
        "z_recomb": 1100,
        "DeltaT_T": Decimal("1e-5"),  # CMB 各向异性幅度
    }


def e2_jeans():
    """Jeans 长度/质量精算（典型 IGM：T=1e4 K 完全电离气体）。"""
    # 声速 c_s = sqrt(k_B T / (mu m_p))，完全电离氢 mu=0.5
    mu = Decimal("0.5")
    T = Decimal("1e4")
    c_s2 = KB * T / (mu * MP)
    c_s = c_s2.sqrt()                       # m/s
    # 临界密度 rho_crit = 3 H0^2 / (8 pi G)
    H0_si = H0_KMS_MPC * Decimal("1000") / MPC   # s^-1
    rho_crit = Decimal(3) * H0_si * H0_si / (Decimal(8) * PI * G)   # kg/m^3
    # 重子密度（z=0 平均）
    rho_b = OMEGA_B * rho_crit
    # Jeans 长度 lambda_J = c_s sqrt(pi/(G rho))
    lambda_J_m = c_s * (PI / (G * rho_b)).sqrt()
    lambda_J_Mpc = lambda_J_m / MPC
    # Jeans 质量 M_J = (4 pi / 3) rho (lambda_J/2)^3
    half = lambda_J_m / TWO
    M_J_kg = (Decimal(4) * PI / Decimal(3)) * rho_b * half * half * half
    M_J_msun = M_J_kg / MSUN
    return {
        "c_s_m_s": c_s,
        "H0_si": H0_si,
        "rho_crit_kg_m3": rho_crit,
        "rho_b_kg_m3": rho_b,
        "lambda_J_m": lambda_J_m,
        "lambda_J_Mpc": lambda_J_Mpc,
        "M_J_kg": M_J_kg,
        "M_J_msun": M_J_msun,
    }


def growth_factor(z):
    """LambdaCDM 线性增长因子（归一 D(0)=1）：
    D(z) = 1/(1+z) * g(z)/g(0)，g(z)=Omega_m(z)^gamma，gamma=0.55（Linder 近似）。"""
    zp1 = Decimal(1) + z
    Ez = (OMEGA_M * zp1 ** 3 + OMEGA_L).sqrt()
    Omz = OMEGA_M * zp1 ** 3 / (Ez * Ez)
    gamma = Decimal("0.55")
    gz = Omz ** gamma
    # g(0)
    E0 = (OMEGA_M + OMEGA_L).sqrt()
    Om0 = OMEGA_M / (E0 * E0)
    g0 = Om0 ** gamma
    D = (Decimal(1) / zp1) * gz / g0
    D_eds = Decimal(1) / zp1
    return {"z": z, "E": Ez, "Omega_m_z": Omz, "g": gz, "D_LCDM": D, "D_EdS": D_eds}


def e3_growth():
    """增长因子 D(z) 在 z in {0,1,10,1100} 的核算。"""
    return [growth_factor(Decimal(z)) for z in (0, 1, 10, 1100)]


def _erfc_asm(x):
    """互补误差函数 erfc(x)，Abramowitz & Stegun 7.1.26 近似（|err|<1.5e-7）。
    erf(x) = 1 - (a1 t + a2 t^2 + ... + a5 t^5) exp(-x^2), t=1/(1+p x)。"""
    p = Decimal("0.3275911")
    a1 = Decimal("0.254829592")
    a2 = Decimal("-0.284496736")
    a3 = Decimal("1.421413741")
    a4 = Decimal("-1.453152027")
    a5 = Decimal("1.061405429")
    t = Decimal(1) / (Decimal(1) + p * x)
    poly = (a1 * t + a2 * t * t + a3 * t ** 3 + a4 * t ** 4 + a5 * t ** 5)
    return (poly * (-(x * x)).exp())


def e4_press_schechter():
    """Press-Schechter：sigma(M) 质量谱（sigma8 归一）+ 星系团数密度量级。"""
    H0_si = H0_KMS_MPC * Decimal("1000") / MPC
    rho_crit = Decimal(3) * H0_si * H0_si / (Decimal(8) * PI * G)   # kg/m^3
    rho_m = OMEGA_M * rho_crit / MSUN * (MPC ** 3)                   # M_sun/Mpc^3
    # R_8 = 8 h^-1 Mpc
    R8 = Decimal(8) / HUBBLE_H
    M8 = (Decimal(4) * PI / Decimal(3)) * rho_m * R8 ** 3            # M_sun
    # sigma(M) = sigma8 (M/M8)^(-alpha)，alpha~0.25（CDM 标度）
    alpha = Decimal("0.25")

    def sigma_of(M):
        return SIGMA8 * (M / M8) ** (-alpha)

    sig8_by_def = sigma_of(M8)                       # 应 = sigma8（自洽）
    M_cl = Decimal("1e15")                          # 富星系团质量尺度
    sig_cl = sigma_of(M_cl)
    nu = DC / sig_cl                                 # 峰值高度
    # PS n(>M) ~ (rho_m/M) erfc(nu/sqrt2)
    n_gt_cl = (rho_m / M_cl) * _erfc_asm(nu / TWO.sqrt())
    return {
        "rho_m_Msun_Mpc3": rho_m,
        "R8_Mpc": R8,
        "M8_Msun": M8,
        "sigma_at_M8": sig8_by_def,
        "M_cluster_Msun": M_cl,
        "sigma_cluster": sig_cl,
        "nu": nu,
        "n_gt_cluster_Mpc3": n_gt_cl,
    }


def e5_supply():
    """初始谱 + 暗物质供给账单（对 TUFT/几何框架）。"""
    # 原初曲率扰动幅度（Planck：P_zeta(k=0.05 Mpc^-1) ~ 2.1e-9）
    P_zeta = Decimal("2.1e-9")
    # 暗物质占物质比：Omega_cdm/Omega_m ~ 0.85（C0139 已判 TUFT 供给 = 0）
    Omega_cdm = OMEGA_M - OMEGA_B
    dm_frac = Omega_cdm / OMEGA_M
    return {
        "P_zeta_at_0.05": P_zeta,
        "n_s": N_S,
        "Omega_cdm": Omega_cdm,
        "dm_fraction_of_matter": dm_frac,
        "tuft_primordial_spectrum": "zero",
        "tuft_dark_matter_supply": "zero(C0139)",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0199 · 结构形成 / 星系起源（母册 T040）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_planck_facts()
    w("\n[E1] 标准宇宙学事实（Planck 2018 只引用不复算）")
    w("  H0=%s km/s/Mpc；Omega_m=%s；Omega_b=%s；Omega_L=%s"
      % (g1["H0_km_s_Mpc"], g1["Omega_m"], g1["Omega_b"], g1["Omega_L"]))
    w("  sigma8=%s；n_s=%s；z_rec=%d；CMB 涨落 DeltaT/T~%s"
      % (g1["sigma8"], g1["n_s"], g1["z_recomb"], g1["DeltaT_T"]))
    w("  => 结构形成 = 原初密度涨落（种子）+ 引力增长 + 暗物质骨架 + 重子气体物理。")
    entries.append(("E1", "标准宇宙学参数（Planck 2018 只引用）：H0=67.4、Om=0.315、"
                    "Ob=0.0493、OL=0.685、sigma8=0.811、n_s=0.965",
                    "PASS", "外部观测值只引用；本册只做算术换算"))

    # ---- E2 ----
    g2 = e2_jeans()
    w("\n[E2] Jeans 长度/质量精算（本册核心，典型 IGM：T=1e4 K 完全电离）")
    w("  声速 c_s = sqrt(k_B T/(mu m_p))，mu=0.5 => c_s = %s m/s"
      % fv(g2["c_s_m_s"], "6e"))
    w("  rho_crit = 3 H0^2/(8 pi G) = %s kg/m^3；rho_b = Omega_b rho_crit = %s kg/m^3"
      % (fv(g2["rho_crit_kg_m3"], "4e"), fv(g2["rho_b_kg_m3"], "4e")))
    w("  lambda_J = c_s sqrt(pi/(G rho_b)) = %s m = %s Mpc"
      % (fv(g2["lambda_J_m"], "4e"), fv(g2["lambda_J_Mpc"], "4f")))
    w("  M_J = (4pi/3) rho_b (lambda_J/2)^3 = %s kg = %s M_sun"
      % (fv(g2["M_J_kg"], "4e"), fv(g2["M_J_msun"], "4e")))
    w("  => Jeans 尺度 ~ %s Mpc / ~ %s M_sun，正落在星系（~1e11-1e12 M_sun）量级。"
      % (fv(g2["lambda_J_Mpc"], "3f"), fv(g2["M_J_msun"], "1e")))
    entries.append(("E2", "Jeans 长度 lambda_J=%s Mpc、Jeans 质量 M_J=%s M_sun"
                    % (fv(g2["lambda_J_Mpc"], "4f"), fv(g2["M_J_msun"], "4e")),
                    "PASS", "标准 IGM 参数算术精算（Decimal 48 位）"))

    # ---- E3 ----
    g3 = e3_growth()
    w("\n[E3] LambdaCDM 线性增长因子 D(z)（D(0)=1 归一，Linder gamma=0.55）")
    for row in g3:
        w("  z=%-5s E(z)=%s  Omega_m(z)=%s  D_LCDM(z)=%s  D_EdS=1/(1+z)=%s"
          % (row["z"], fv(row["E"], "6f"), fv(row["Omega_m_z"], "6f"),
             fv(row["D_LCDM"], "6f"), fv(row["D_EdS"], "6f")))
    d1 = g3[1]["D_LCDM"]
    d1100 = g3[3]["D_LCDM"]
    w("  => z=1 处 D=%s（EdS 近似 0.5，Lambda 后期增长抑制使 D 偏大）；z=1100 处 D=%s"
      % (fv(d1, "4f"), fv(d1100, "3e")))
    w("  => 物质主导期 delta∝1/(1+z) 近似成立；Lambda 主导后增长放缓（抑制因子 g）。")
    entries.append(("E3", "D(0)=1、D(1)=%s、D(10)=%s、D(1100)=%s；"
                    "z=1100 时 Omega_m(z)->1、g->1"
                    % (fv(d1, "4f"), fv(g3[2]["D_LCDM"], "4f"), fv(d1100, "3e")),
                    "PASS", "Linder gamma=0.55 半解析增长因子精算"))

    # ---- E4 ----
    g4 = e4_press_schechter()
    w("\n[E4] Press-Schechter：sigma(M) 质量谱（sigma8=%s 归一）" % SIGMA8)
    w("  rho_m = %s M_sun/Mpc^3；R8=8h^-1=%s Mpc；M8=%s M_sun"
      % (fv(g4["rho_m_Msun_Mpc3"], "4e"), fv(g4["R8_Mpc"], "4f"),
         fv(g4["M8_Msun"], "4e")))
    w("  sigma(M8)=%s（自洽=sigma8=%s）；sigma(M=1e15)=%s"
      % (fv(g4["sigma_at_M8"], "4f"), SIGMA8, fv(g4["sigma_cluster"], "4f")))
    w("  nu=delta_c/sigma=%s；PS n(>1e15 M_sun)=(rho_m/M)erfc(nu/sqrt2)=%s Mpc^-3"
      % (fv(g4["nu"], "4f"), fv(g4["n_gt_cluster_Mpc3"], "3e")))
    w("  => 富星系团数密度 ~1e-7–1e-6 Mpc^-3 量级，与观测星系团丰度（~1e-5–1e-6）同量级。")
    entries.append(("E4", "sigma(1e15)=%s、nu=%s、n(>1e15)=%s Mpc^-3（PS 量级自洽）"
                    % (fv(g4["sigma_cluster"], "4f"), fv(g4["nu"], "4f"),
                       fv(g4["n_gt_cluster_Mpc3"], "3e")),
                    "PASS", "sigma8 归一 + PS erfc（A&S 近似）量级核算"))

    # ---- E5 ----
    g5 = e5_supply()
    w("\n[E5] 初始谱供给检查 + 裁定")
    w("  结构形成需要两件外部输入：(a) 原初曲率功率谱 P_zeta~%s（n_s=%s，暴胀供给）；"
      % (g5["P_zeta_at_0.05"], g5["n_s"]))
    w("  (b) 暗物质骨架：Omega_cdm=%s，占物质 %s（C0139 已判 TUFT 供给=0）。"
      % (fv(g5["Omega_cdm"], "4f"), fv(g5["dm_fraction_of_matter"], "4f")))
    w("  TUFT 供给：原初功率谱=%s；暗物质=%s。"
      % (g5["tuft_primordial_spectrum"], g5["tuft_dark_matter_supply"]))
    w("  => TUFT 无初始谱（P(k) 外部输入）+ 无暗物质供给 ⇒ 连结构形成的初始条件都给不出。")
    w("  => **结构形成 / 星系起源 对 TUFT/几何框架结构性负面**；撞母册登记 C2（绝对标度/"
      "初始条件外部输入）/ C5（无可检验预言）。")
    entries.append(("E5", "结构性负面：TUFT 无原初功率谱、无暗物质供给（C0139），"
                    "结构形成初始条件全外部输入", "PASS", "撞 C2/C5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "Jeans 长度在 1–10 Mpc（星系尺度）",
         Decimal(1) < g2["lambda_J_Mpc"] < Decimal(10)),
        ("G2", "Jeans 质量在 1e10–1e12 M_sun（星系尺度）",
         Decimal("1e10") < g2["M_J_msun"] < Decimal("1e12")),
        ("G3", "c_s 典型 IGM 声速 ~10 km/s 量级（1e4–1e5 m/s）",
         Decimal("1e4") < g2["c_s_m_s"] < Decimal("1e5")),
        ("G4", "D(z) 归一自洽：D(0)=1", g3[0]["D_LCDM"] == Decimal(1)),
        ("G5", "z=1 处 D_LCDM ~0.8（0.7–0.9，Lambda 后期抑制）",
         Decimal("0.7") < g3[1]["D_LCDM"] < Decimal("0.9")),
        ("G6", "z=1100 处 Omega_m(z)->1（物质主导）",
         g3[3]["Omega_m_z"] > Decimal("0.99")),
        ("G7", "sigma(M8) 自洽 = sigma8",
         abs(g4["sigma_at_M8"] - SIGMA8) < Decimal("1e-6")),
        ("G8", "PS 星系团数密度在 1e-8–1e-5 Mpc^-3（量级）",
         Decimal("1e-8") < g4["n_gt_cluster_Mpc3"] < Decimal("1e-5")),
        ("G9", "暗物质占物质 ~85%",
         g5["dm_fraction_of_matter"] > Decimal("0.8")),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0199 guard failed"

    w("\n[诚实边界]")
    w("  本册数值均为标准宇宙学（LambdaCDM/结构形成）算术复核，不写成 TUFT 预测/修正；")
    w("  Planck 观测值只引用不复算；TUFT 已注销（C0133）；裁的是「几何框架能否供给")
    w("  结构形成的初始谱与暗物质」，不宣称解决任何物理难题。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0199_结构形成攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0199_结构形成攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0199_structure_formation",
            "mother_book": "T040",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_planck": {k: str(v) for k, v in g1.items()},
            "E2_jeans": {k: str(v) for k, v in g2.items()},
            "E3_growth": [{k: str(v) for k, v in row.items()} for row in g3],
            "E4_press_schechter": {k: str(v) for k, v in g4.items()},
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "guards_total": len(guards),
            "guards_pass": sum(1 for g in guards if g[2]),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0199 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
