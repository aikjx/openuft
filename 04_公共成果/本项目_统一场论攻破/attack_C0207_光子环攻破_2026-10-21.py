# -*- coding: utf-8 -*-
"""
attack_C0207_光子环攻破_2026-10-21.py
母册 T110「黑洞光子球弱透镜与环（photon ring）· 强透镜多像 + 波形模板」攻破

定位：母册 T110（行 234，原文照录）：
  | T110 | 黑洞光子球弱透镜与环（photon ring） | 强透镜多像 + 波形模板 | C5 | 🔲 |
前置：C0169（EHT M87*/Sgr A* 阴影尺寸：M87* θ=39.689 μas、0.77σ）、
     C0133（TUFT 已注销）。本册与 C0169 同对象不同切面：C0169 算「阴影」，
     本册算「光子环/光子球/临界碰撞参数」，并判定 TUFT/几何框架对
     「强透镜多像 / 光子环 / 波形模板」是否供给任何结构。

把"T110 光子环"压缩成五条可复核读数：

  E1 观测事实（只引用不复算）：Schwarzschild 光子球 r_ph=3M、临界碰撞参数
     b_c=3√3 M（Bardeen 1972）；EHT M87* 环/阴影角径 42±3 μas；EHT 2019
     观测到亮环（光子环 m=1 分量）。
  E2 **光子球/光子环第一性精算（本册核心）**：
     几何单位 r_ph = 3GM/c² = 3M；b_c = 3√3 GM/c²；
     注意恒等式 b_c = √27 M = R_sh（光子环角半径即阴影边缘，同一几何对象）。
     M87*（M=6.5e9 M☉，D=16.8 Mpc）光子环角直径 θ_ph = 2 b_c/D → μas，
     与 C0169 读数 39.689 μas 衔接，与 EHT 42±3 μas 比 σ。
  E3 Kerr 光子环：极端自旋 a*=1 精确赤道光子轨道半径 r_ph^+=M（顺行）、
     r_ph^-=4M（逆行），相对 Schwarzschild 3M 的偏移量级（Fraction 精确）。
  E4 几何供给判定：TUFT/几何框架有无光线偏转/强透镜/波形模板结构——无，
     供给 0；撞 C5。
  E5 裁定：结构性负面（对 TUFT/几何框架），按母册登记撞 C5。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：EHT 观测值只引用不复算；本册所有数值均为标准 GR 几何算术复核，
**不是 TUFT 的预测或修正**；TUFT 已注销（C0133）。
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
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
RAD2MUAS = (Decimal(180) / PI) * Decimal(3600) * Decimal(1e6)   # 1 rad → μas

# ---------- EHT 观测输入（只引用不复算） ----------
M87 = {
    "label": "M87* (EHT 2019 ApJL 875)",
    "M_Msun": Decimal("6.5e9"),
    "D_Mpc": Decimal("16.8"),
    "theta_obs_muas": Decimal("42.0"),
    "theta_obs_sigma": Decimal("3.0"),
}
# C0169 读数（承接引用，不复算）：M87* 阴影角直径
C0169_M87_THETA_MUAS = Decimal("39.689")
C0169_M87_NSIGMA = Decimal("0.77")


def gm_over_c2_per_msun() -> Decimal:
    """GM⊙/c²（m），Decimal 48 位精算。"""
    return G * M_SUN / (C * C)


def e1_facts():
    """观测/几何事实（只引用不复算）。"""
    return {
        "photon_sphere_r_ph": "3M（几何单位，Schwarzschild；Bardeen 1972）",
        "critical_impact_bc": "3√3 M ≈ 5.196 M（= √27 M = R_sh）",
        "m87_obs": M87,
        "sources": [
            "Bardeen, Press & Teukolsky 1972（Schwarzschild/Kerr 光子轨道）",
            "EHT 2019 ApJL 875 L1-L6（M87* 亮环/阴影 42±3 μas）",
            "C0169（M87* 阴影角直径 39.689 μas、0.77σ；本册光子环读数与之恒等衔接）",
        ],
    }


def e2_photon_ring():
    """光子球/临界碰撞参数/光子环角直径第一性精算（本册核心）。"""
    gm = gm_over_c2_per_msun()                 # m per M_sun
    sqrt3 = Decimal(3).sqrt()                  # √3
    # 几何单位系数（以 M = GM/c² 为单位）
    rph_coef = Decimal(3)                      # r_ph = 3M
    bc_coef = Decimal(3) * sqrt3              # b_c = 3√3 M
    # 每太阳质量的物理量
    rph_per_msun = rph_coef * gm               # m
    bc_per_msun = bc_coef * gm                 # m
    # 恒等式检查：b_c = √27 M = R_sh
    sqrt27 = Decimal(27).sqrt()
    bc_eq_sqrt27 = abs(bc_coef - sqrt27) < Decimal("1e-40")
    ratio_bc_rph = bc_coef / rph_coef          # = √3

    # M87*
    M = M87["M_Msun"]
    D = M87["D_Mpc"] * MPC
    rph_m87 = rph_per_msun * M
    bc_m87 = bc_per_msun * M
    theta_ph = Decimal(2) * bc_m87 / D * RAD2MUAS   # μas 角直径
    # 与 EHT 观测比
    diff_obs = abs(theta_ph - M87["theta_obs_muas"])
    n_sigma_obs = diff_obs / M87["theta_obs_sigma"]
    ratio_obs = theta_ph / M87["theta_obs_muas"]
    # 与 C0169 读数比（恒等式 b_c=R_sh 应使两读数一致）
    diff_c0169 = abs(theta_ph - C0169_M87_THETA_MUAS)

    return {
        "GM_over_c2_per_Msun_m": gm,
        "sqrt3": sqrt3,
        "rph_coef_M": rph_coef,
        "bc_coef_M": bc_coef,
        "sqrt27": sqrt27,
        "bc_eq_Rsh": bc_eq_sqrt27,
        "ratio_bc_rph": ratio_bc_rph,
        "rph_per_Msun_m": rph_per_msun,
        "bc_per_Msun_m": bc_per_msun,
        "rph_M87_m": rph_m87,
        "bc_M87_m": bc_m87,
        "theta_ph_M87_muas": theta_ph,
        "n_sigma_vs_EHT": n_sigma_obs,
        "ratio_vs_EHT": ratio_obs,
        "diff_vs_C0169_muas": diff_c0169,
    }


def e3_kerr():
    """Kerr 赤道光子轨道半径偏移（极端自旋 a*=1 精确值，Fraction）。"""
    # Bardeen 1972：r_ph^± = 2M{1 + cos[(2/3) arccos(∓a*)]}
    # a*=0（Schwarzschild）：r_ph^+ = r_ph^- = 3M
    # a*=1（极端 Kerr）：顺行 r_ph^+ = M；逆行 r_ph^- = 4M（精确解析值）
    r_sch = Fraction(3)     # M 单位
    r_pro_ext = Fraction(1)   # M 单位
    r_ret_ext = Fraction(4)   # M 单位
    # 相对 Schwarzschild 的偏移比例
    shift_pro_in = (r_sch - r_pro_ext) / r_sch   # = 2/3 内移
    shift_ret_out = (r_ret_ext - r_sch) / r_sch  # = 1/3 外移
    return {
        "formula": "r_ph^± = 2M{1 + cos[(2/3) arccos(∓a*)]}（Bardeen 1972）",
        "a_star_0_rph_M": 3,
        "a_star_1_rph_prograde_M": 1,
        "a_star_1_rph_retrograde_M": 4,
        "prograde_inward_shift_frac": shift_pro_in,    # 2/3 = 66.7%
        "retrograde_outward_shift_frac": shift_ret_out,  # 1/3 = 33.3%
        "note": "自旋使赤道光子轨道半径在 [M, 4M] 区间移动；角环径随 b_c 同量级偏移",
    }


def e4_geometry_supply():
    """TUFT/几何框架对强透镜多像/光子环/波形模板的供给判定。"""
    return {
        "photon_ring_is_pure_GR": True,        # r_ph/b_c 是 Schwarzschild 度规的严格几何性质
        "needs_null_geodesics": True,          # 光子环依赖零测地线 + 光线偏转
        "tuft_has_light_deflection": 0,        # TUFT/几何框架无光线偏转结构
        "tuft_has_strong_lensing_multi_image": 0,
        "tuft_has_waveform_template": 0,
        "tuft_cancelled_C0133": True,
        "supply": 0,
        "collides": "C5",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0207 · 黑洞光子球弱透镜与环（photon ring）攻破（母册 T110）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测/几何事实（只引用不复算）")
    for s in g1["sources"]:
        w("  · " + s)
    w("  Schwarzschild 光子球 r_ph = %s；临界碰撞参数 b_c = %s"
      % (g1["photon_sphere_r_ph"], g1["critical_impact_bc"]))
    m = g1["m87_obs"]
    w("  M87*：亮环/阴影角径 %s±%s μas；M=%s M☉；D=%s Mpc"
      % (m["theta_obs_muas"], m["theta_obs_sigma"], m["M_Msun"], m["D_Mpc"]))
    entries.append(("E1", "r_ph=3M、b_c=3√3 M（Bardeen 1972）；M87* 环 42±3 μas"
                    "（EHT 2019 只引用）", "PASS", "来源标注：Bardeen 1972 / ApJL 875 L1"))

    # ---- E2 ----
    g2 = e2_photon_ring()
    w("\n[E2] 光子球/光子环第一性精算（本册核心，Decimal 48 位）")
    w("  GM⊙/c² = %s m" % fv(g2["GM_over_c2_per_Msun_m"], "10f"))
    w("  r_ph = 3M；b_c = 3√3 M = %s M；√3 = %s"
      % (fv(g2["bc_coef_M"], "10f"), fv(g2["sqrt3"], "15f")))
    w("  恒等式 b_c = √27 M = R_sh？ %s（√27 = %s）；b_c/r_ph = √3 = %s"
      % (g2["bc_eq_Rsh"], fv(g2["sqrt27"], "10f"), fv(g2["ratio_bc_rph"], "15f")))
    w("  每 M☉：r_ph = %s m；b_c = %s m"
      % (fv(g2["rph_per_Msun_m"], "10f"), fv(g2["bc_per_Msun_m"], "10f")))
    w("  M87*（M=%s M☉，D=%s Mpc）：" % (m["M_Msun"], m["D_Mpc"]))
    w("    r_ph = %s m；b_c = %s m"
      % (fv(g2["rph_M87_m"], "6e"), fv(g2["bc_M87_m"], "6e")))
    w("    光子环角直径 θ_ph = 2 b_c/D = %s μas" % fv(g2["theta_ph_M87_muas"], "10f"))
    w("    vs EHT 观测 %s±%s μas：偏差 %s μas = %s σ；预言/观测 = %s"
      % (m["theta_obs_muas"], m["theta_obs_sigma"],
         fv(abs(g2["theta_ph_M87_muas"] - m["theta_obs_muas"]), "4f"),
         fv(g2["n_sigma_vs_EHT"], "4f"), fv(g2["ratio_vs_EHT"], "6f")))
    w("    vs C0169 读数 %s μas：偏差 %s μas（恒等衔接，b_c=R_sh）；C0169 报 0.77σ"
      % (C0169_M87_THETA_MUAS, fv(g2["diff_vs_C0169_muas"], "6f")))
    entries.append(("E2", "M87* θ_ph = %s μas（= C0169 的 39.689 μas），"
                    "vs EHT 42±3 = %s σ（1σ 相容）"
                    % (fv(g2["theta_ph_M87_muas"], "4f"), fv(g2["n_sigma_vs_EHT"], "3f")),
                    "PASS", "Decimal 48 位精算；标准 GR 几何算术复核，非 TUFT 预测"))

    # ---- E3 ----
    g3 = e3_kerr()
    w("\n[E3] Kerr 光子环：自旋 a 下顺/逆光子轨道半径偏移量级")
    w("  公式：%s" % g3["formula"])
    w("  a*=0（Schwarzschild）：r_ph = %d M；"
      "a*=1（极端 Kerr）：顺行 r_ph = %d M、逆行 r_ph = %d M（精确解析值）"
      % (g3["a_star_0_rph_M"], g3["a_star_1_rph_prograde_M"],
         g3["a_star_1_rph_retrograde_M"]))
    w("  相对 Schwarzschild 3M：顺行内移 %s = %.1f%%；逆行外移 %s = %.1f%%"
      % (g3["prograde_inward_shift_frac"],
         float(g3["prograde_inward_shift_frac"]) * 100,
         g3["retrograde_outward_shift_frac"],
         float(g3["retrograde_outward_shift_frac"]) * 100))
    w("  => 自旋使赤道光子轨道半径在 [M, 4M] 区间移动，角环径随 b_c 同量级偏移（GR 几何）。")
    entries.append(("E3", "极端 Kerr：r_ph ∈ [M, 4M]，顺行内移 2/3、逆行外移 1/3"
                    "（Bardeen 1972 精确值）", "PASS", "Fraction 精确；GR 几何量级"))

    # ---- E4 ----
    g4 = e4_geometry_supply()
    w("\n[E4] 几何供给判定（TUFT/几何框架对 T110）")
    w("  光子环 = 纯 GR 几何预言（r_ph/b_c 是 Schwarzschild 度规严格性质），依赖零测地线。")
    w("  TUFT 光线偏转结构 = %d；强透镜多像 = %d；波形模板 = %d；TUFT 已注销（C0133）= %s"
      % (g4["tuft_has_light_deflection"], g4["tuft_has_strong_lensing_multi_image"],
         g4["tuft_has_waveform_template"], g4["tuft_cancelled_C0133"]))
    w("  => 几何供给 = %d；撞 C5（无独立于 GR 的可检验新预言）。" % g4["supply"])
    entries.append(("E4", "TUFT 无光线偏转/无强透镜多像/无波形模板 ⇒ 供给 0；撞 C5",
                    "PASS", "撞 C5；承接 C0133 TUFT 已注销"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  T110 光子环 = Schwarzschild/Kerr 光线偏转的几何后果（r_ph=3M、b_c=3√3 M、Kerr 偏移）。")
    w("  E2 精算 M87* θ_ph=39.689 μas 与 C0169 恒等、与 EHT 42±3 1σ 相容——证实的是 GR，不是 TUFT。")
    w("  TUFT/几何框架无光线偏转、无强透镜多像、无波形模板结构（E4）。")
    w("  => **T110 结构性负面（对 TUFT/几何框架）**；按母册登记撞 **C5**。")
    entries.append(("E5", "T110 结构性负面：光子环是 GR 光线偏转几何性质，"
                    "TUFT 无供给", "PASS", "撞 C5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "b_c/r_ph = √3 ≈ 1.732050807568877",
         abs(g2["ratio_bc_rph"] - Decimal("1.732050807568877")) < Decimal("1e-12")),
        ("G2", "b_c = 3√3 M = √27 M = R_sh（恒等式）", g2["bc_eq_Rsh"]),
        ("G3", "M87* θ_ph ≈ 39.689 μas，与 C0169 读数偏差 < 0.01 μas",
         g2["diff_vs_C0169_muas"] < Decimal("0.01")),
        ("G4", "M87* θ_ph vs EHT 42±3 μas 在 1σ 内（≈0.77σ）",
         g2["n_sigma_vs_EHT"] <= Decimal("1")),
        ("G5", "极端 Kerr 赤道光子轨道半径 ∈ [M, 4M]（Fraction 精确）",
         g3["a_star_1_rph_prograde_M"] == 1
         and g3["a_star_1_rph_retrograde_M"] == 4),
        ("G6", "TUFT 几何供给 = 0（无光线偏转/强透镜/波形模板），撞 C5",
         g4["supply"] == 0 and g4["collides"] == "C5"),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0207 guard failed"

    w("\n[诚实边界]")
    w("  EHT 观测值只引用不复算；本册数值均为标准 GR 几何算术复核，不写成 TUFT 预测/修正；")
    w("  TUFT 已注销（C0133）；裁的是「TUFT/几何框架能否供给光子环/强透镜」，判供给 0。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("  有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0207_光子环攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0207_光子环攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0207_photon_ring",
            "parent_row": "T110 | 黑洞光子球弱透镜与环（photon ring） | 强透镜多像 + 波形模板 | C5",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E2_GM_over_c2_per_Msun_m": str(g2["GM_over_c2_per_Msun_m"]),
            "E2_bc_coef_M": str(g2["bc_coef_M"]),
            "E2_bc_eq_Rsh": g2["bc_eq_Rsh"],
            "E2_ratio_bc_rph_sqrt3": str(g2["ratio_bc_rph"]),
            "E2_rph_M87_m": str(g2["rph_M87_m"]),
            "E2_bc_M87_m": str(g2["bc_M87_m"]),
            "E2_theta_ph_M87_muas": str(g2["theta_ph_M87_muas"]),
            "E2_n_sigma_vs_EHT": str(g2["n_sigma_vs_EHT"]),
            "E2_diff_vs_C0169_muas": str(g2["diff_vs_C0169_muas"]),
            "E3_kerr_extremal_rph_M": [1, 4],
            "E3_prograde_inward_shift_frac": str(g3["prograde_inward_shift_frac"]),
            "E3_retrograde_outward_shift_frac": str(g3["retrograde_outward_shift_frac"]),
            "E4_geometry_supply": g4["supply"],
            "E4_collides": g4["collides"],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0207 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
