# -*- coding: utf-8 -*-
"""
attack_C0226_真空稳定性攻破_2026-10-21.py
独立复算：希格斯势真空稳定性（亚稳 vs 绝对稳定）· 力统一专项 · 耦合常数跑动
（母册 T259，行 391；撞 C2/C7）

把「希格斯真空是绝对稳定还是亚稳」压缩成五条可复核读数 + 一张输入账单：

  E1 SM 输入事实（PDG 只引用不复算）：m_H=125.10、m_t(pole)=173.06、v=246.22 GeV、
     α_s(M_Z)=0.1181、sin²θ_W=0.2312；y_t(M_t)=0.993660（衔接 C0194 质量谱口径）。
  E2 **一圈 RGE 跑动独立精算（本册核心）**：λ(M_t)=m_H²/(2v²) 起，
     RK4 联立 (λ, y_t, g_s, g, g') 单圈 β 函数积分到 Planck，
     求 λ(μ)→0 的不稳定性标度 Λ_I。
  E3 稳定性边界：固定 m_H，扫描 m_t 找临界 m_t^crit（λ 全程 ≥0 的顶夸克质量上限）。
  E4 真空寿命：Coleman–De Luccia 隧穿估计 S_4，τ_vac vs 宇宙年龄 T_U 比较。
  E5 供给检查：TUFT 是否供给 Higgs 势 / RGE 跑动（无）⇒ 结构性负面，撞 C2/C7。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。
SM 一圈 β 函数为标准粒子物理算术（Machacek–Vaughn / Buttazzo 口径）；
m_t/m_H/α_s 等 SM 参数为已知外部输入显式计数，本册不把它们写成 TUFT 预测。

诚实边界：本册为单圈主导项算术复核。两圈精算（Buttazzo et al. 2013）给出
Λ_I~1e10–1e11 GeV、m_t^crit~171 GeV；本册单圈结果因未计两圈正修正，
Λ_I 偏低、m_t^crit 偏低，但「亚稳、寿命 >> T_U」的物理结论不变。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG / SM 标准值，只引用不复算） ----------
M_H = Decimal("125.10")          # GeV，PDG 希格斯玻色子质量
M_T_POLE = Decimal("173.06")     # GeV，PDG 顶夸克 pole 质量
V_VEV = Decimal("246.22")        # GeV，电弱真空期望值 v
ALPHA_S_MZ = Decimal("0.1181")   # PDG，M_Z 处强耦合
SIN2_THETAW = Decimal("0.2312")  # PDG，弱混合角
Y_T_MT = Decimal("0.993660")     # 衔接 C0194 质量谱口径
M_PLANCK = Decimal("1.22e19")    # GeV，Planck 标度（外部）
T_U_SEC = Decimal("4.36e17")     # s，宇宙年龄 ≈13.8 Gyr（外部）
# M_t 处规范耦合初值（SM 标准跑动后取值，外部输入）
GS_MT = Decimal("1.17")          # g_s(M_t)，α_s(M_t)≈0.1089
G_MT = Decimal("0.64")           # g(M_t) SU(2)_L
GP_MT = Decimal("0.35")          # g'(M_t) U(1)_Y

PI = Decimal("3.1415926535897932384626433832795028841971693993751")
INV_16PI2 = Decimal(1) / (Decimal(16) * PI * PI)
GEV_INV_SEC = Decimal("6.582119569e-25")  # 1 GeV^-1 = 6.58e-25 s（ħ）
DT = Decimal("0.05")
N_STEPS = 1000  # t_max = 50 ≫ ln(M_Pl/M_t)≈38.8


def derivs(state):
    """SM 单圈 β 函数 d(·)/dt，t=ln(μ/M_t)（Machacek–Vaughn 口径）。
    state = (λ, y_t, g_s, g, g')；返回 d/dt 五元组。"""
    lam, yt, gs, g, gp = state
    lam2 = lam * lam
    yt2 = yt * yt
    yt4 = yt2 * yt2
    g2 = g * g
    gp2 = gp * gp
    g4 = g2 * g2
    gp4 = gp2 * gp2
    gs2 = gs * gs
    # (16π²) β_λ
    b_lam = (Decimal(24) * lam2
             - Decimal(6) * yt2 * lam - Decimal(6) * yt4
             + Decimal(9) / Decimal(8) * g4
             + Decimal(3) / Decimal(4) * g2 * gp2
             + Decimal(3) / Decimal(8) * gp4
             - (Decimal(3) / Decimal(2)) * lam * (Decimal(3) * g2 + gp2))
    # (16π²) β_y_t
    b_yt = yt * ((Decimal(9) / Decimal(2)) * yt2
                 - Decimal(8) * gs2
                 - (Decimal(9) / Decimal(4)) * g2
                 - (Decimal(17) / Decimal(20)) * gp2)
    # (16π²) β_g_s = -7 g_s^3
    b_gs = Decimal(-7) * gs * gs2
    # (16π²) β_g = -43/6 g^3
    b_g = (Decimal(-43) / Decimal(6)) * g * g2
    # (16π²) β_g' = +21/6 g'^3
    b_gp = (Decimal(21) / Decimal(6)) * gp * gp2
    return (b_lam * INV_16PI2, b_yt * INV_16PI2, b_gs * INV_16PI2,
            b_g * INV_16PI2, b_gp * INV_16PI2)


def rk4_step(state, dt):
    """四阶 Runge–Kutta 单步。"""
    k1 = derivs(state)
    s2 = tuple(state[i] + k1[i] * dt / 2 for i in range(5))
    k2 = derivs(s2)
    s3 = tuple(state[i] + k2[i] * dt / 2 for i in range(5))
    k3 = derivs(s3)
    s4 = tuple(state[i] + k3[i] * dt for i in range(5))
    k4 = derivs(s4)
    return tuple(state[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(5))


def integrate(lam0, yt0, n_steps=N_STEPS):
    """RK4 积分；返回轨迹 [(t, λ, yt, gs, g, gp), ...]。"""
    state = (lam0, yt0, GS_MT, G_MT, GP_MT)
    traj = [(Decimal(0),) + state]
    for i in range(n_steps):
        state = rk4_step(state, DT)
        traj.append(((i + 1) * DT,) + state)
    return traj


def e1_sm_inputs():
    lam0 = M_H * M_H / (Decimal(2) * V_VEV * V_VEV)
    return {
        "m_H": M_H, "m_t_pole": M_T_POLE, "v": V_VEV,
        "alpha_s_MZ": ALPHA_S_MZ, "sin2_thW": SIN2_THETAW,
        "y_t_Mt": Y_T_MT, "lambda_Mt": lam0,
        "g_s_Mt": GS_MT, "g_Mt": G_MT, "gp_Mt": GP_MT,
    }


def e2_rge_running(lam0, yt0):
    traj = integrate(lam0, yt0)
    t_cross = None
    lam_cross = None
    for row in traj:
        t, lam = row[0], row[1]
        if lam <= 0:
            t_cross, lam_cross = t, lam
            break
    t_end, lam_end, yt_end = traj[-1][0], traj[-1][1], traj[-1][2]
    Lambda_I = M_T_POLE * t_cross.exp() if t_cross is not None else None
    lam_min = min(r[1] for r in traj)
    return {
        "t_cross": t_cross, "lam_at_cross": lam_cross,
        "Lambda_I_GeV": Lambda_I,
        "lam_at_Planck": lam_end, "yt_at_Planck": yt_end,
        "lam_min": lam_min, "t_end": t_end,
        "log10_Lambda_I": Lambda_I.log10() if Lambda_I is not None else None,
    }


def e3_critical_mt(lam0):
    """bisection：找 min λ(μ)≥0 的临界 y_t0；m_t^crit = y_t^crit·v/√2。"""
    t_Pl = (M_PLANCK / M_T_POLE).ln()
    n_span = int((t_Pl / DT).to_integral_value(rounding="ROUND_CEILING"))

    def min_lam(yt0):
        return min(r[1] for r in integrate(lam0, yt0, n_steps=n_span))

    # bracket: y_low 给绝对稳定（min>0），y_high=实测给亚稳（min<0）
    y_low = Decimal("0.50")
    y_high = Y_T_MT
    for _ in range(60):
        y_mid = (y_low + y_high) / Decimal(2)
        if min_lam(y_mid) >= 0:
            y_low = y_mid
        else:
            y_high = y_mid
    yt_crit = (y_low + y_high) / Decimal(2)
    m_t_crit = yt_crit * V_VEV / Decimal(2).sqrt()
    return {
        "yt_crit": yt_crit, "m_t_crit_GeV": m_t_crit,
        "mt_measured": M_T_POLE,
        "margin_GeV": M_T_POLE - m_t_crit,
        "regime": "亚稳(metastable)" if M_T_POLE > m_t_crit else "绝对稳定",
    }


def e4_vacuum_lifetime(lam_end, Lambda_I):
    abs_lam = -lam_end
    S4 = Decimal(8) * PI * PI / (Decimal(3) * abs_lam)
    tau_sec = (Decimal(1) / Lambda_I) * GEV_INV_SEC * S4.exp()
    log10_tau = tau_sec.log10()
    log10_Tu = T_U_SEC.log10()
    return {
        "abs_lambda_at_Planck": abs_lam,
        "S4_bounce_action": S4,
        "log10_tau_sec": log10_tau, "log10_TU": log10_Tu,
        "log10_tau_over_TU": log10_tau - log10_Tu,
        "tau_gt_TU": (log10_tau - log10_Tu) > Decimal(10),
    }


def e5_tuft_supply():
    return {
        "tuft_has_higgs_potential": False,
        "tuft_has_rge_system": False,
        "tuft_has_higgs_field": False,
        "supply": 0,
        "verdict": "结构性负面：真空稳定性依赖 SM RGE 跑动结构（标准粒子物理算术），"
                   "TUFT 无 Higgs 势/无 RGE 供给。",
        "hits": "C2（绝对标度/跑动结构为 SM 外部输入）/ C7（数学自洽——稳定性结论为 SM 算术，TUFT 零贡献）",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0226 · 希格斯势真空稳定性（T259 · 力统一专项 · 耦合常数跑动）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_sm_inputs()
    w("\n[E1] SM 输入事实（PDG 只引用不复算）")
    w("  m_H = %s GeV；m_t(pole) = %s GeV；v = %s GeV"
      % (g1["m_H"], g1["m_t_pole"], g1["v"]))
    w("  α_s(M_Z) = %s；sin²θ_W = %s；y_t(M_t) = %s（衔接 C0194）"
      % (g1["alpha_s_MZ"], g1["sin2_thW"], g1["y_t_Mt"]))
    w("  g_s(M_t)=%s，g(M_t)=%s，g'(M_t)=%s" % (GS_MT, G_MT, GP_MT))
    w("  λ(M_t) = m_H²/(2v²) = %s²/(2·%s²) = %s"
      % (fv(M_H, "2f"), fv(V_VEV, "2f"), fv(g1["lambda_Mt"], "10f")))
    entries.append(("E1", "SM 输入：m_H=125.10, m_t=173.06, v=246.22；λ(M_t)=%s"
                    % fv(g1["lambda_Mt"], "8f"), "PASS",
                    "PDG 只引用；λ(M_t) 本册独立换算"))

    # ---- E2 ----
    g2 = e2_rge_running(g1["lambda_Mt"], Y_T_MT)
    w("\n[E2] 单圈 RGE 跑动独立精算（本册核心，RK4 积分）")
    w("  β_λ=(1/16π²)[24λ²−6y_t²λ−6y_t⁴+(9/8)g⁴+(3/4)g²g'²+(3/8)g'⁴−(3/2)λ(3g²+g'²)]")
    if g2["t_cross"] is not None:
        w("  λ(μ) 首次穿 0：t=ln(μ/M_t)=%s e-折，λ=%s"
          % (fv(g2["t_cross"], "4f"), fv(g2["lam_at_cross"], "4e")))
        w("  => 不稳定性标度 Λ_I = M_t·exp(t) = %s GeV（log10=%s）"
          % (fv(g2["Lambda_I_GeV"], "6e"), fv(g2["log10_Lambda_I"], "6f")))
    w("  终点 t=%s：λ(μ_Pl)=%s，y_t(μ_Pl)=%s；λ 全程最小=%s"
      % (fv(g2["t_end"], "2f"), fv(g2["lam_at_Planck"], "6e"),
         fv(g2["yt_at_Planck"], "6f"), fv(g2["lam_min"], "6e")))
    w("  => λ 在高标度穿零转负 ⇒ 亚稳真空（单圈主导项；两圈精算 Λ_I~1e10–1e11 GeV）。")
    entries.append(("E2", "λ(M_t)=%s 起，单圈 RK4 积分得 Λ_I≈%s GeV（log10=%s），"
                          "λ(Planck)=%s<0 ⇒ 亚稳"
                    % (fv(g1["lambda_Mt"], "8f"), fv(g2["Lambda_I_GeV"], "3e"),
                       fv(g2["log10_Lambda_I"], "4f"), fv(g2["lam_at_Planck"], "3e")),
                    "PASS", "纯 Decimal 48 位 RK4 (λ,y_t,g_s,g,g') 单圈 β"))

    # ---- E3 ----
    g3 = e3_critical_mt(g1["lambda_Mt"])
    w("\n[E3] 稳定性边界：临界顶夸克质量 m_t^crit（固定 m_H=125.10）")
    w("  bisection 得临界 y_t0 = %s；m_t^crit = y_t^crit·v/√2 = %s GeV"
      % (fv(g3["yt_crit"], "8f"), fv(g3["m_t_crit_GeV"], "6f")))
    w("  实测 m_t=%s GeV；裕度=%s GeV ⇒ 实测 > 临界 ⇒ 落在亚稳区"
      % (fv(g3["mt_measured"], "2f"), fv(g3["margin_GeV"], "4f")))
    w("  （两圈标准值 m_t^crit≈171–172 GeV；单圈因未计两圈正修正偏低，亚稳结论不变。）")
    entries.append(("E3", "m_t^crit=%s GeV（单圈）；实测 173.06 高出 %s GeV ⇒ 亚稳区"
                    % (fv(g3["m_t_crit_GeV"], "3f"), fv(g3["margin_GeV"], "3f")),
                    "PASS", "Decimal bisection 60 步；两圈标准 171–172 GeV"))

    # ---- E4 ----
    g4 = e4_vacuum_lifetime(g2["lam_at_Planck"], g2["Lambda_I_GeV"])
    w("\n[E4] 真空寿命：CDL 隧穿估计 vs 宇宙年龄")
    w("  Planck 处 |λ|=%s ⇒ S_4≈8π²/(3|λ|)=%s"
      % (fv(g4["abs_lambda_at_Planck"], "4e"), fv(g4["S4_bounce_action"], "4f")))
    w("  log10(τ_vac/s)=%s；log10(T_U/s)=%s；log10(τ_vac/T_U)=%s >>0"
      % (fv(g4["log10_tau_sec"], "4f"), fv(g4["log10_TU"], "4f"),
         fv(g4["log10_tau_over_TU"], "4f")))
    w("  => 亚稳真空寿命远超宇宙年龄（标准结论一致）。")
    entries.append(("E4", "S_4≈%s；log10(τ_vac/T_U)=%s >>0 ⇒ 寿命远超 T_U"
                    % (fv(g4["S4_bounce_action"], "2f"),
                       fv(g4["log10_tau_over_TU"], "2f")),
                    "PASS", "CDL 薄壁近似量级；τ>>T_U 稳健"))

    # ---- E5 ----
    g5 = e5_tuft_supply()
    w("\n[E5] 裁定：TUFT 供给检查")
    w("  TUFT 有 Higgs 势？%s；有 RGE 体系？%s；有 Higgs 场？%s"
      % (g5["tuft_has_higgs_potential"], g5["tuft_has_rge_system"],
         g5["tuft_has_higgs_field"]))
    w("  => %s" % g5["verdict"])
    w("  => 撞 %s" % g5["hits"])
    entries.append(("E5", "TUFT 供给 0：无 Higgs 势/无 RGE；真空稳定性纯 SM 算术，结构性负面",
                    "PASS", g5["hits"]))

    # ---- 守卫 ----
    guards = [
        ("G1", "λ(M_t) 落在 0.12–0.14（m_H=125.10 标准初值）",
         Decimal("0.12") < g1["lambda_Mt"] < Decimal("0.14")),
        ("G2", "λ 在高标度穿零（Λ_I > 1e3 GeV，远离电弱标度）",
         g2["Lambda_I_GeV"] is not None
         and Decimal("1e3") < g2["Lambda_I_GeV"] < M_PLANCK),
        ("G3", "λ(Planck) < 0（亚稳区，非绝对稳定）",
         g2["lam_at_Planck"] < 0),
        ("G4", "临界 m_t^crit 存在且 < 实测 173.06（落在亚稳区）",
         g3["m_t_crit_GeV"] < M_T_POLE and g3["m_t_crit_GeV"] > Decimal("100")),
        ("G5", "实测 m_t=173.06 > m_t^crit", M_T_POLE > g3["m_t_crit_GeV"]),
        ("G6", "真空寿命 τ_vac >> T_U（log10 比值 >10）",
         g4["log10_tau_over_TU"] > Decimal("10")),
        ("G7", "TUFT 供给 = 0（无 Higgs 势/RGE）", g5["supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0226 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决真空稳定性问题；数值为标准 SM 单圈 RGE 算术复核（Decimal 48 位 RK4）；")
    w("  m_H/m_t/α_s/规范耦合为 PDG 外部输入显式计数，不写成 TUFT 预测/修正；")
    w("  单圈主导项 Λ_I 偏低（两圈精算 1e10–1e11 GeV）；CDL 寿命为薄壁近似量级估计；")
    w("  TUFT 已注销（C0133）。裁的是「TUFT/几何框架能否供给 Higgs 势/RGE 跑动」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0226_真空稳定性攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0226_真空稳定性攻破_2026-10-21.json")
    out = {
        "name": "C0226_higgs_vacuum_stability",
        "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                    for e in entries],
        "E1_sm_inputs": {k: str(v) for k, v in g1.items()},
        "E2_rge": {k: str(v) for k, v in g2.items()},
        "E3_critical_mt": {k: str(v) for k, v in g3.items()},
        "E4_lifetime": {k: str(v) for k, v in g4.items()},
        "E5_tuft_supply": {k: str(v) for k, v in g5.items()},
        "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
        "exit_code": 0,
    }
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("C0226 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
