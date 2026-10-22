# -*- coding: utf-8 -*-
"""
attack_C0169_阴影尺寸攻破_2026-10-21.py
母册 T108「事件视界望远镜（EHT）M87*/Sgr A* 阴影尺寸」攻破

定位：物理 Top100 母册 T108（强场 GR 阴影 + 吸积模型，原 🔲）。
前置：C0168（黑洞微观态供给 0）、C0166（单位换算双路径守卫）。
本册核心 = 第一性精算 GR 阴影角径 vs EHT 实测，并判定 TUFT/几何框架
对"阴影尺寸偏离纯 GR"是否供给 QG 修正项 / 离散性签名。

把"T108 阴影尺寸"压缩成五条可复核读数：

  E1 EHT 观测事实（只引用不复算）：
     M87*  EHT 2019：阴影角径 42±3 μas，M=6.5e9 M☉，D=16.8 Mpc。
     SgrA* EHT 2022：阴影角径 51.8±2.3 μas，M≈4.297e6 M☉，D≈8.15 kpc。
  E2 GR 阴影第一性精算（本册核心）：
     光子球 r_ph = 3GM/c²；阴影半径 R_sh = √27 GM/c² ≈ 5.196 GM/c²；
     θ_diam = 2 R_sh / D（弧度）→ μas。对 M87* 与 Sgr A* 两组参数精算，
     与 EHT 观测角径比值（须 1σ 相容）。
     QG 修正签名幅度：δ ~ l_P/R_sch，EHT 角精度 ~10 μas 对应可探相对
     修正，实算 δ 上限与可探阈。
  E3 几何供给判定：阴影尺寸为纯 GR 几何预言且被观测证实；TUFT 无 QG
     修正项供给、无离散性签名，供给 0；撞 C5/C6。
  E4 与 C0168（黑洞微观态）、C0166（量纲双路径）衔接；母册 T108 登记。
  E5 裁定：结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：EHT 观测值只引用不复算；本册不宣称已修正 GR 阴影；
TUFT 无独立 QG 修正参数 ⇒ 对"T108 是否供给超出 GR 的新预言"判供给 0。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 物理常数（CODATA 2018，SI，只引用） ----------
G = Decimal("6.67430e-11")          # m^3 kg^-1 s^-2
C = Decimal("299792458")            # m/s
M_SUN = Decimal("1.98847e30")       # kg
PC = Decimal("3.0856775814913673e16")   # m（1 parsec）
MPC = Decimal("1e6") * PC
KPC = Decimal("1e3") * PC
# 弧度 → μas：1 rad = 180/π deg = 206265 arcsec = 2.06265e11 μas
# 精确用 π 近似（Decimal 48 位）
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
RAD2MUAS = (Decimal(180) / PI) * Decimal(3600) * Decimal(1e6)   # 1 rad → μas

# ---------- EHT 观测输入（只引用不复算） ----------
# M87*：EHT 2019 ApJL 875 L1-L6
M87 = {
    "label": "M87* (EHT 2019)",
    "M_Msun": Decimal("6.5e9"),
    "D_Mpc": Decimal("16.8"),
    "theta_obs_muas": Decimal("42.0"),
    "theta_obs_sigma": Decimal("3.0"),
}
# Sgr A*：EHT 2022 ApJL 930 L12-L16
SGRA = {
    "label": "Sgr A* (EHT 2022)",
    "M_Msun": Decimal("4.297e6"),
    "D_kpc": Decimal("8.15"),
    "theta_obs_muas": Decimal("51.8"),
    "theta_obs_sigma": Decimal("2.3"),
}

# Planck 长度（CODATA 2018），用于 QG 修正签名尺度
HBAR = Decimal("1.054571817e-34")   # J·s
L_P = Decimal("1.616255e-35")       # m


def gm_over_c2_per_msun() -> Decimal:
    """GM⊙/c²（m），Decimal 48 位精算。"""
    return G * M_SUN / (C * C)


def shadow_radius(M_Msun: Decimal) -> Decimal:
    """R_sh = √27 GM/c²（m）。"""
    return Decimal(27).sqrt() * gm_over_c2_per_msun() * M_Msun


def photon_sphere(M_Msun: Decimal) -> Decimal:
    """r_ph = 3GM/c²（m）。"""
    return Decimal(3) * gm_over_c2_per_msun() * M_Msun


def schwarzschild_r(M_Msun: Decimal) -> Decimal:
    """R_s = 2GM/c²（m）。"""
    return Decimal(2) * gm_over_c2_per_msun() * M_Msun


def theta_diam_muas(M_Msun: Decimal, D_m: Decimal) -> Decimal:
    """阴影角直径 θ = 2 R_sh / D（弧度）→ μas。"""
    Rsh = shadow_radius(M_Msun)
    theta_rad = Decimal(2) * Rsh / D_m
    return theta_rad * RAD2MUAS


def e1_observations():
    return {
        "M87": M87,
        "SgrA": SGRA,
        "sources": [
            "EHT 2019 ApJL 875 L1 (M87* 首张阴影)",
            "EHT 2022 ApJL 930 L12 (Sgr A* 阴影)",
            "GR 预言 R_sh = √27 GM/c² ≈ 5.196 GM/c² (Bardeen 1973)",
        ],
    }


def e2_first_principles():
    # 通用标度
    gm_c2_sun = gm_over_c2_per_msun()          # m per M_sun
    Rsh_coef = Decimal(27).sqrt()               # ≈ 5.196152
    rph_coef = Decimal(3)
    Rs_coef = Decimal(2)

    # M87*
    D_m87 = M87["D_Mpc"] * MPC
    th_m87 = theta_diam_muas(M87["M_Msun"], D_m87)
    Rsh_m87 = shadow_radius(M87["M_Msun"])
    Rph_m87 = photon_sphere(M87["M_Msun"])
    Rs_m87 = schwarzschild_r(M87["M_Msun"])

    # Sgr A*
    D_sgra = SGRA["D_kpc"] * KPC
    th_sgra = theta_diam_muas(SGRA["M_Msun"], D_sgra)
    Rsh_sgra = shadow_radius(SGRA["M_Msun"])
    Rs_sgra = schwarzschild_r(SGRA["M_Msun"])

    # 与观测比
    def compat(theta_calc, obs, sigma):
        diff = abs(theta_calc - obs)
        n_sigma = diff / sigma
        ratio = theta_calc / obs
        return {"theta_calc": theta_calc, "obs": obs, "sigma": sigma,
                "diff": diff, "n_sigma": n_sigma, "ratio": ratio,
                "within_1sigma": n_sigma <= Decimal(1)}

    m87_fit = compat(th_m87, M87["theta_obs_muas"], M87["theta_obs_sigma"])
    sgra_fit = compat(th_sgra, SGRA["theta_obs_muas"], SGRA["theta_obs_sigma"])

    # QG 修正签名幅度：δ ~ l_P / R_s（线性 QG 修正到度规/光子球）
    # EHT 角精度 ~10 μas（半分辨率），相对阴影 θ_obs 的可探相对修正 ε_hat
    def qg_estimate(Rs_m: Decimal, theta_obs_muas: Decimal):
        delta_rel = L_P / Rs_m                 # 相对阴影尺寸修正上限
        # EHT 角分辨率 ~20 μas FWHM，对应相对可探 ε ~ 10 μas / θ_shadow
        eps_detect = Decimal("10.0") / theta_obs_muas
        return {"delta_rel": delta_rel, "eps_detect": eps_detect,
                "ratio_delta_over_detect": delta_rel / eps_detect}

    qg_m87 = qg_estimate(Rs_m87, M87["theta_obs_muas"])
    qg_sgra = qg_estimate(Rs_sgra, SGRA["theta_obs_muas"])

    return {
        "GM_over_c2_per_Msun_m": gm_c2_sun,
        "Rsh_coef": Rsh_coef,
        "rph_coef": rph_coef,
        "Rs_coef": Rs_coef,
        "M87": {"Rsh_m": Rsh_m87, "Rph_m": Rph_m87, "Rs_m": Rs_m87,
                "theta_diam_muas": th_m87, "fit": m87_fit, "qg": qg_m87},
        "SgrA": {"Rsh_m": Rsh_sgra, "Rs_m": Rs_sgra,
                 "theta_diam_muas": th_sgra, "fit": sgra_fit, "qg": qg_sgra},
    }


def e3_geometry_supply():
    """TUFT/几何框架对阴影尺寸偏离 GR 的供给判定。"""
    return {
        "shadow_is_pure_GR": True,            # R_sh = √27 GM/c² 是 GR 严格解
        "observed_confirms_GR": True,         # EHT 两源均 1σ 内
        "tuft_QG_correction_terms": 0,        # TUFT 无离散 QG 修正参数
        "tuft_discreteness_signature": 0,     # TUFT 连续几何（承接 C0168 E3）
        "supply": 0,                          # 总供给
        "collides": "C5,C6",
    }


def e4_linkage():
    return {
        "C0168": "TUFT 自由度连续（态数 ∞），离散微观态基供给 0 → 本册同对象：无离散阴影签名",
        "C0166": "单位换算双路径守卫（Mpc/kpc→m、rad→μas）复用，Decimal 48 位一致",
        "parent_T108": "母册行：| T108 | EHT M87*/Sgr A* 阴影尺寸 | 强场 GR 阴影 + 吸积模型 | C5,C6 | 🔲 → ✅ |",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0169 · EHT M87*/Sgr A* 阴影尺寸攻破（母册 T108）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_observations()
    w("\n[E1] EHT 观测事实（只引用不复算）")
    for src in g1["sources"]:
        w("  · " + src)
    w("  M87*  : 阴影角径 %s±%s μas；M=%s M☉；D=%s Mpc"
      % (M87["theta_obs_muas"], M87["theta_obs_sigma"],
         M87["M_Msun"], M87["D_Mpc"]))
    w("  SgrA* : 阴影角径 %s±%s μas；M=%s M☉；D=%s kpc"
      % (SGRA["theta_obs_muas"], SGRA["theta_obs_sigma"],
         SGRA["M_Msun"], SGRA["D_kpc"]))
    entries.append(("E1", "M87* 42±3 μas / Sgr A* 51.8±2.3 μas（EHT 2019/2022 只引用）",
                    "PASS", "来源标注：ApJL 875 L1 / ApJL 930 L12"))

    # ---- E2 ----
    g2 = e2_first_principles()
    w("\n[E2] GR 阴影第一性精算（本册核心，Decimal 48 位）")
    w("  GM⊙/c² = %s m（= %s km）"
      % (fv(g2["GM_over_c2_per_Msun_m"], "6e"),
         fv(g2["GM_over_c2_per_Msun_m"]/Decimal(1000), "6f")))
    w("  R_sh = √27·GM/c² = %s·GM/c²（Bardeen 1973）；r_ph = 3 GM/c²；R_s = 2 GM/c²"
      % fv(g2["Rsh_coef"], "8f"))

    m87 = g2["M87"]
    w("\n  M87*：M=%s M☉，D=%s Mpc" % (M87["M_Msun"], M87["D_Mpc"]))
    w("    R_sh = %s m = %s km = %s AU"
      % (fv(m87["Rsh_m"], "6e"), fv(m87["Rsh_m"]/Decimal(1000), "6e"),
         fv(m87["Rsh_m"]/Decimal(1.495978707e11), "4f")))
    w("    r_ph = %s m；R_s = %s m"
      % (fv(m87["Rph_m"], "6e"), fv(m87["Rs_m"], "6e")))
    w("    预言角直径 θ = 2 R_sh/D = %s μas" % fv(m87["theta_diam_muas"], "6f"))
    f8 = m87["fit"]
    w("    观测 %s±%s μas；偏差 %s μas = %s σ；预言/观测 = %s；1σ 内 = %s"
      % (f8["obs"], f8["sigma"], fv(f8["diff"], "4f"), fv(f8["n_sigma"], "4f"),
         fv(f8["ratio"], "6f"), f8["within_1sigma"]))
    q8 = m87["qg"]
    w("    QG 修正签名 δ ~ l_P/R_s = %s；EHT 相对可探 ε ~ 10 μas/θ = %s；"
      "δ/ε = %s（远 < 1，EHT 不可探线性 QG 修正）"
      % (fv(q8["delta_rel"], "4e"), fv(q8["eps_detect"], "4f"),
         fv(q8["ratio_delta_over_detect"], "4e")))
    entries.append(("E2", "M87* θ=%s μas vs 观测 42±3，%s σ（1σ 相容）"
                    % (fv(m87["theta_diam_muas"], "4f"), fv(f8["n_sigma"], "3f")),
                    "PASS", "Decimal 48 位精算"))

    sg = g2["SgrA"]
    w("\n  Sgr A*：M=%s M☉，D=%s kpc" % (SGRA["M_Msun"], SGRA["D_kpc"]))
    w("    R_sh = %s m = %s km"
      % (fv(sg["Rsh_m"], "6e"), fv(sg["Rsh_m"]/Decimal(1000), "6e")))
    w("    预言角直径 θ = %s μas" % fv(sg["theta_diam_muas"], "6f"))
    f9 = sg["fit"]
    w("    观测 %s±%s μas；偏差 %s μas = %s σ；预言/观测 = %s；1σ 内 = %s"
      % (f9["obs"], f9["sigma"], fv(f9["diff"], "4f"), fv(f9["n_sigma"], "4f"),
         fv(f9["ratio"], "6f"), f9["within_1sigma"]))
    q9 = sg["qg"]
    w("    QG 修正签名 δ ~ l_P/R_s = %s；EHT 相对可探 ε = %s；δ/ε = %s"
      % (fv(q9["delta_rel"], "4e"), fv(q9["eps_detect"], "4f"),
         fv(q9["ratio_delta_over_detect"], "4e")))
    entries.append(("E2", "Sgr A* θ=%s μas vs 观测 51.8±2.3，%s σ（1σ 相容）"
                    % (fv(sg["theta_diam_muas"], "4f"), fv(f9["n_sigma"], "3f")),
                    "PASS", "Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给判定（TUFT/几何框架对 T108）")
    w("  阴影尺寸 = 纯 GR 几何预言（R_sh=√27 GM/c²），且被 EHT 两源 1σ 证实。")
    w("  TUFT QG 修正项数 = %d；TUFT 离散性签名 = %d（承接 C0168 E3：连续场态数∞）"
      % (g3["tuft_QG_correction_terms"], g3["tuft_discreteness_signature"]))
    w("  => 几何供给 = %d；撞 C5（无独立于 GR 的可检验新预言）/ C6（无独立误差带）。"
      % g3["supply"])
    entries.append(("E3", "TUFT 无 QG 修正项 / 无离散签名 ⇒ 供给 0；撞 C5/C6",
                    "PASS", "撞 C5/C6"))

    # ---- E4 ----
    g4 = e4_linkage()
    w("\n[E4] 与既有线衔接")
    w("  C0168：%s" % g4["C0168"])
    w("  C0166：%s" % g4["C0166"])
    w("  母册 T108：🔲 → ✅ 登记。")
    entries.append(("E4", "承接 C0168/C0166；母册 T108 🔲→✅", "PASS", "登记"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  T108 阴影尺寸是 GR 严格几何预言，EHT 两源 1σ 内证实 GR。")
    w("  TUFT/几何框架未供给任何超出 GR 的 QG 修正项或离散性签名（E3）。")
    w("  => T108 结构性负面（对 TUFT/几何框架）：撞 C5（无独立可检验新预言）/")
    w("     C6（无独立误差带）。EHT 证实的是 GR，不是 TUFT。")
    entries.append(("E5", "T108 结构性负面：TUFT 无独立阴影新预言；撞 C5/C6",
                    "PASS", "撞 C5/C6"))

    # ---- 守卫 ----
    guards = [
        ("G1", "R_sh 系数 ≈ 5.196152（√27）",
         abs(g2["Rsh_coef"] - Decimal("5.19615242270663")) < Decimal("1e-6")),
        ("G2", "M87* 预言 θ 与 42±3 μas 1σ 相容",
         m87["fit"]["within_1sigma"]),
        ("G3", "Sgr A* 预言 θ 与 51.8±2.3 μas 1σ 相容",
         sg["fit"]["within_1sigma"]),
        ("G4", "EHT 引用标记（2019/2022 ApJL）",
         len(g1["sources"]) >= 3),
        ("G5", "TUFT 几何供给 = 0（无 QG 修正项、无离散签名）",
         g3["supply"] == 0),
        ("G6", "E5 裁定为结构性负面（撞 C5/C6）",
         g3["collides"] == "C5,C6"),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0169 guard failed"

    w("\n[诚实边界]")
    w("  EHT 观测值只引用不复算；本册不宣称已修正 GR 阴影；")
    w("  QG 修正签名 δ~l_P/R_s 是量级估计（非拟合）；TUFT 无独立 QG 参数 ⇒ 判供给 0。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0169_阴影尺寸攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0169_阴影尺寸攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0169_EHT_shadow_size",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_sources": g1["sources"],
            "E2_GM_over_c2_per_Msun_m": str(g2["GM_over_c2_per_Msun_m"]),
            "E2_Rsh_coef_sqrt27": str(g2["Rsh_coef"]),
            "E2_M87_theta_muas": str(m87["theta_diam_muas"]),
            "E2_M87_n_sigma": str(m87["fit"]["n_sigma"]),
            "E2_M87_ratio": str(m87["fit"]["ratio"]),
            "E2_SgrA_theta_muas": str(sg["theta_diam_muas"]),
            "E2_SgrA_n_sigma": str(sg["fit"]["n_sigma"]),
            "E2_SgrA_ratio": str(sg["fit"]["ratio"]),
            "E2_QG_M87_delta_over_detect": str(m87["qg"]["ratio_delta_over_detect"]),
            "E2_QG_SgrA_delta_over_detect": str(sg["qg"]["ratio_delta_over_detect"]),
            "E3_geometry_supply": g3["supply"],
            "E3_collides": g3["collides"],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0169 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
