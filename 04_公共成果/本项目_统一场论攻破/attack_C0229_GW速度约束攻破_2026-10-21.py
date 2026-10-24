# -*- coding: utf-8 -*-
"""
attack_C0229_GW速度约束攻破_2026-10-21.py
独立复算：T137「引力波速度与光速之差（GW170817 余约束）」· L 线域 G 批

母册 T137（原文照录）：
  | T137 | 引力波速度与光速之差（GW170817 余约束） | 传播色散 + 宇宙学积分 | C5,C6 | 🔲 |

定位：GW170817 / GRB170817A 速度约束核算。引力波先到、伽马暴晚到 ~1.7 s，
距离 ~40 Mpc，跨 ~1.3×10^7 年飞行 ⇒ 把 1.7 s 的到达时差折算成对
|v_g−c|/c 的上限。本册**不采信任何自报**，用 Decimal 48 位独立精算四条读数：

  E1 观测事实（GW170817/GRB170817A：延迟 Δt≈1.7 s、距离 L≈1.23×10^23 m，
     c=299792458 m/s 精确值——外部引用，只引用不复算）。
  E2 **同源核算（本册核心）**：ε ≡ |v_g−c|/c ≤ Δt/(L/c) = c·Δt/L 精算。
  E3 色散约束：v_g = c(1−A(f))，f∈[30,1000] Hz 带宽内 A 的频域上限
     （建模 A(f)=K/f²，仿有质量引力子色散）。
  E4 物理分解：1.7 s 到达差 = 源内发射延迟 Δt_int + 传播时差；
     剔除 Δt_int=0/0.5/1.0 s 后的真上限序列。
  E5 供给检查与裁定：TUFT 是否供给引力波传播/速度结构（无）⇒ 结构性负面，
     按母册登记撞 C5（可检验）/ C6（误差带）。

归因口径（硬纪律）：全部数值为**标准广义相对论/观测算术复核**（Lorentz 不变性、
无质量自旋-2 引力子以 c 传播）；TUFT 已注销（C0133）；严禁把标准物理结果写成
TUFT 预测/修正。红线：不宣称解决物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；
「有预测且对 = 0/22」；UFT-3=0 保持；数学自洽 ≠ 实验证实。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖，退出码 0。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（GW170817 文献值，只引用不复算） ----------
# 真空中光速 c（SI 精确值，CODATA 2019）
C_LIGHT = Decimal("299792458")            # m/s，精确
# GW170817 光度距离 ≈ 40 Mpc = 40×10^6 pc × 3.0857×10^16 m/pc ≈ 1.23×10^23 m
# （Abbott et al. 2017, LIGO/Virgo 合作组；距离为外部引用输入，本册按 1.23e23 m 核算）
DIST_M = Decimal("1.23e23")              # m，外部输入（~40 Mpc）
# GRB170817A 触发相对 GW 并合峰的到达延迟 ≈ 1.7 s（Fermi-GBM；文献 1.74 s，
# 母册口径 1.7 s——外部引用输入，本册按 1.7 s 核算）
DT_OBS = Decimal("1.7")                   # s，外部输入
# LIGO/Virgo GW170817 有效频带 ≈ 30 Hz（潮汐进入带）至 ~1 kHz（并合/振铃）
F_LO = Fraction(30)                       # Hz，外部引用（带低端）
F_HI = Fraction(1000)                     # Hz，外部引用（带高端）
# 普朗克常数 h（SI 精确值，用于 E3 色散模型等效换算）
H_SI = Decimal("6.62607015e-34")         # J·s，精确
EV_J = Decimal("1.602176634e-19")         # J/eV，精确
# 源内发射延迟分解（E4 模型假设：并合 → 喷流冲破的固有延迟，文献估计 0.1–10 s 量级；
# 本册按 0 / 0.5 / 1.0 s 三档做敏感性分解，属本册模型参数非外部观测值）
DT_INT_LIST = [Decimal("0"), Decimal("0.5"), Decimal("1.0")]


def e1_obs_facts():
    """E1 · 观测事实（外部引用，只引用不复算）。"""
    return {
        "event": "GW170817 + GRB170817A（双中子星并合，2017-08-17）",
        "delay_s": DT_OBS,
        "distance_m": DIST_M,
        "c_m_s": C_LIGHT,
        "band_hz": [float(F_LO), float(F_HI)],
    }


def e2_speed_bound():
    """E2 · 同源核算（核心）：ε ≡ |v_g−c|/c ≤ Δt/(L/c)。

    推导链（一阶）：v_g = c(1−ε)，|ε|≪1
      L/v_g = L/[c(1−ε)] ≈ (L/c)(1+ε)
      ⇒ 传播时差 Δt_travel = L/v_g − L/c ≈ (L/c)·ε
      ⇒ |ε| ≤ Δt_obs / (L/c) = c·Δt_obs/L
    """
    L_over_c = DIST_M / C_LIGHT                 # 光行时（秒）
    eps_max = DT_OBS / L_over_c                 # = c·Δt/L
    return {
        "L_over_c_s": L_over_c,
        "L_over_c_yr": L_over_c / Decimal("31557600"),   # 儒略年 365.25 d
        "eps_max": eps_max,
    }


def e3_dispersion_bound():
    """E3 · 色散约束：v_g = c(1−A(f))，A(f)=K/f² 模型下频域上限。

    推导链：同并合事件全部频段相干到达（波形在 30 Hz–1 kHz 内相干），
    频段两端传播时差 Δt_disp = (L/c)·[A(f_lo)−A(f_hi)] ≤ Δt_obs
    ⇒ A(f_lo)−A(f_hi) ≤ Δt_obs/(L/c) = ε_max
    A(f)=K/f²：K = ε_max/(1/f_lo² − 1/f_hi²)；
      A(f_lo)=K/f_lo²、A(f_hi)=K/f_hi²。
    等效有质量引力子色散：v_g² = c²[1−(m_g c²/(h f))²]
      ⇒ A(f) = (m_g c²)²/[2(h f)²]，反解 m_g c² = h f √(2A)。
    """
    g2 = e2_speed_bound()
    eps_max = g2["eps_max"]
    inv_flo2 = Decimal(1) / Decimal(int(F_LO * F_LO))
    inv_fhi2 = Decimal(1) / Decimal(int(F_HI * F_HI))
    diff = inv_flo2 - inv_fhi2                  # Hz^-2
    K = eps_max / diff                          # Hz²
    A_lo = K / Decimal(int(F_LO * F_LO))              # 无量纲，f=30 Hz 处
    A_hi = K / Decimal(int(F_HI * F_HI))             # 无量纲，f=1000 Hz 处
    # 等效引力子质量（本册模型换算，非外部引用）
    mg_c2_J = H_SI * Decimal(int(F_LO)) * (Decimal(2) * A_lo).sqrt()
    mg_c2_eV = mg_c2_J / EV_J
    return {
        "inv_flo2": inv_flo2, "inv_fhi2": inv_fhi2, "diff": diff,
        "K_Hz2": K, "A_at_30Hz": A_lo, "A_at_1000Hz": A_hi,
        "mg_c2_J": mg_c2_J, "mg_c2_eV": mg_c2_eV,
        "eps_max_ref": eps_max,
    }


def e4_decomposition():
    """E4 · 物理分解：1.7 s = 源内延迟 Δt_int + 传播时差 ε·(L/c)。

    真上限序列：ε ≤ (Δt_obs − Δt_int)/(L/c)，Δt_int∈{0, 0.5, 1.0} s。
    符号注记：观测为 GW 先到 1.7 s；若 v_g<c，引力波应**晚到**，
    故 v_g<c 的允许窗须由源内延迟兜底——本分解给出各档 ε 上限。
    """
    L_over_c = e2_speed_bound()["L_over_c_s"]
    rows = []
    for dt_int in DT_INT_LIST:
        dt_net = DT_OBS - dt_int
        eps = dt_net / L_over_c
        rows.append({"dt_int_s": dt_int, "dt_net_s": dt_net, "eps": eps})
    return {"L_over_c_s": L_over_c, "rows": rows}


def e5_supply():
    """E5 · TUFT 供给检查：引力波传播/速度结构供给 = 0。"""
    return {
        "tuft_propagation_sector": "none",       # 无引力子传播扇区
        "tuft_dispersion_relation": "none",      # 无色散关系
        "tuft_speed_structure": 0,               # 无速度结构供给
        "tuft_status": "注销（C0133 终审）",
        "standard_physics_basis": "GR 无质量自旋-2 引力子以 c 传播（Lorentz 不变性）",
        "registered_against": "C5（可检验）/ C6（误差带）",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0229 · 引力波速度与光速之差（GW170817 余约束）攻破")
    w("母册 T137 · L 线域 G 批 · 传播色散 + 宇宙学积分 · 撞 C5/C6")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_obs_facts()
    w("\n[E1] 观测事实（外部引用，只引用不复算）")
    w("  事件：%s" % g1["event"])
    w("  到达延迟 Δt_obs = %s s（GW 先到、GRB170817A 晚到；Fermi-GBM 触发）"
      % g1["delay_s"])
    w("  距离 L = %s m（~40 Mpc；Abbott et al. 2017）" % g1["distance_m"])
    w("  光速 c = %s m/s（SI 精确值）" % g1["c_m_s"])
    w("  GW 相干频带 f ∈ [%g, %g] Hz（LIGO/Virgo 有效带）"
      % (g1["band_hz"][0], g1["band_hz"][1]))
    w("  => 以上四项为外部输入（GW170817 观测 + SI 常数），本册只做算术折算。")
    entries.append(("E1",
                    "GW170817/GRB170817A：Δt=%s s、L=%s m、c 精确、带 [30,1000] Hz"
                    % (g1["delay_s"], g1["distance_m"]),
                    "PASS", "外部引用只引用；本册无观测重采集"))

    # ---- E2 ----
    g2 = e2_speed_bound()
    w("\n[E2] 同源核算（本册核心）：ε = |v_g−c|/c ≤ Δt/(L/c) = c·Δt/L")
    w("  推导：v_g=c(1−ε) ⇒ L/v_g−L/c ≈ (L/c)·ε ⇒ |ε| ≤ Δt_obs/(L/c)")
    w("  光行时 L/c = %s s" % fv(g2["L_over_c_s"], "6e"))
    w("  光行时 L/c = %s 年（≈ %s×10^7 年）"
      % (fv(g2["L_over_c_yr"], "4f"),
         format(g2["L_over_c_yr"] / Decimal("1e7"), ".3f")))
    w("  => |v_g−c|/c ≤ c·Δt/L = %s  ≈ %s×10^-15"
      % (fv(g2["eps_max"], "6e"),
         format(g2["eps_max"] * Decimal("1e15"), ".4f")))
    w("  （已知量级 ~10^-15；母册口径 3e-15 量级，本册 Decimal 精算一致。）")
    entries.append(("E2",
                    "|v_g−c|/c ≤ %s（≈%.3f×10^-15）；光行时 L/c≈%s s≈%s×10^7 年"
                    % (fv(g2["eps_max"], "6e"),
                       float(g2["eps_max"] * Decimal("1e15")),
                       fv(g2["L_over_c_s"], "4e"),
                       format(g2["L_over_c_yr"] / Decimal("1e7"), ".3f")),
                    "PASS", "Decimal 48 位独立精算；外部输入仅 Δt/L/c 三项"))

    # ---- E3 ----
    g3 = e3_dispersion_bound()
    w("\n[E3] 色散约束：v_g=c(1−A(f))，A(f)=K/f² 模型下频域上限")
    w("  相干到达 ⇒ 频段两端时差 (L/c)·[A(30)−A(1000)] ≤ Δt_obs")
    w("  1/f_lo²−1/f_hi² = %s−%s = %s Hz^-2"
      % (fv(g3["inv_flo2"], "6e"), fv(g3["inv_fhi2"], "2e"), fv(g3["diff"], "6e")))
    w("  K = ε_max / diff = %s Hz²" % fv(g3["K_Hz2"], "6e"))
    w("  A(30 Hz) ≤ %s；A(1000 Hz) ≤ %s"
      % (fv(g3["A_at_30Hz"], "6e"), fv(g3["A_at_1000Hz"], "6e")))
    w("  等效有质量引力子（A=(m_g c²/(hf))²/2）：")
    w("    m_g c² ≤ %s J ≈ %s eV"
      % (fv(g3["mg_c2_J"], "4e"), fv(g3["mg_c2_eV"], "4e")))
    entries.append(("E3",
                    "A(30Hz)≤%s、A(1000Hz)≤%s；等效 m_g c²≤%s eV"
                    % (fv(g3["A_at_30Hz"], "4e"), fv(g3["A_at_1000Hz"], "3e"),
                       fv(g3["mg_c2_eV"], "3e")),
                    "PASS", "A(f)=K/f² 为本册色散模型（仿有质量引力子），非外部引用"))

    # ---- E4 ----
    g4 = e4_decomposition()
    w("\n[E4] 物理分解：1.7 s = 源内喷流发射延迟 Δt_int + 传播时差 ε·(L/c)")
    w("  真上限序列 ε ≤ (Δt_obs−Δt_int)/(L/c)：")
    for row in g4["rows"]:
        w("    Δt_int=%s s ⇒ 净时差 %s s ⇒ ε ≤ %s"
          % (row["dt_int_s"], row["dt_net_s"], fv(row["eps"], "6e")))
    w("  符号注记：观测为 GW **先到**；若 v_g<c 引力波应晚到，故 v_g<c 窗须由")
    w("  源内延迟兜底——剔除源内延迟后真上限收紧至 ~1.7×10^-15（Δt_int=1 s 档）。")
    entries.append(("E4",
                    "ε 序列：Δt_int=0/0.5/1.0 s ⇒ ε≤%s/%s/%s"
                    % (fv(g4["rows"][0]["eps"], "2e"),
                       fv(g4["rows"][1]["eps"], "2e"),
                       fv(g4["rows"][2]["eps"], "2e")),
                    "PASS", "Δt_int 为本册敏感性分解参数（文献量级 0.1–10 s）"))

    # ---- E5 ----
    g5 = e5_supply()
    w("\n[E5] 供给检查与裁定")
    w("  TUFT 引力波传播扇区：%s；色散关系：%s；速度结构供给：%d"
      % (g5["tuft_propagation_sector"], g5["tuft_dispersion_relation"],
         g5["tuft_speed_structure"]))
    w("  TUFT 状态：%s" % g5["tuft_status"])
    w("  本约束的物理基础：%s" % g5["standard_physics_basis"])
    w("  => 引力波速度约束 = GR 传播结构（标准物理）+ GW170817 观测（标准观测）；")
    w("     TUFT 无引力波传播/无速度结构可供给，连可被本检验触及的预言面都没有。")
    w("  => **结构性负面（对 TUFT/几何框架）**；按母册 T137 登记撞 %s。"
      % g5["registered_against"])
    entries.append(("E5",
                    "TUFT 传播/速度供给=0（C0133 已注销）；约束纯属 GR+观测，"
                    "结构性负面，撞 C5/C6",
                    "PASS", "母册 T137 登记撞点照录"))

    # ---- 守卫 ----
    guards = [
        ("G1", "ε_max 量级 10^-15（>1e-15 且 <1e-14）",
         g2["eps_max"] > Decimal("1e-15") and g2["eps_max"] < Decimal("1e-14")),
        ("G2", "光行时 L/c ∈ [4.0e14, 4.2e14] s",
         g2["L_over_c_s"] > Decimal("4.0e14") and g2["L_over_c_s"] < Decimal("4.2e14")),
        ("G3", "A(30Hz)/ε_max ∈ [1.0, 1.01]（1/f_hi² 项可忽略自洽）",
         Decimal("1.0") <= g3["A_at_30Hz"] / g3["eps_max_ref"] <= Decimal("1.01")),
        ("G4", "TUFT 引力波传播/速度结构供给 = 0", g5["tuft_speed_structure"] == 0),
        ("G5", "分解单调性：Δt_int 越大 ε 上限越小",
         g4["rows"][0]["eps"] > g4["rows"][1]["eps"] > g4["rows"][2]["eps"]),
        ("G6", "等效引力子质量上限 < 1e-19 eV（量级自洽）",
         g3["mg_c2_eV"] < Decimal("1e-19")),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0229 guard failed"

    w("\n[诚实边界（红线）]")
    w("  本册不宣称解决引力波速度物理；全部读数为标准 GR/观测算术复核，")
    w("  非 TUFT 预测/修正（TUFT 已注销 C0133）；外部观测值只引用不复算。")
    w("  红线不变：「不宣称解决任何物理难题」；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("  「有预测且对 = 0/22」；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0229_GW速度约束攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0229_GW速度约束攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0229_gw_speed_constraint",
            "mother_row": "T137 引力波速度与光速之差（GW170817 余约束）| 传播色散+宇宙学积分 | C5,C6",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_obs_facts": {k: (str(v) if not isinstance(v, list) else v)
                             for k, v in g1.items()},
            "E2_speed_bound": {k: str(v) for k, v in g2.items()},
            "E3_dispersion": {k: str(v) for k, v in g3.items()},
            "E4_decomposition": {"L_over_c_s": str(g4["L_over_c_s"]),
                                 "rows": [{k: str(vv) for k, vv in r.items()}
                                          for r in g4["rows"]]},
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "external_inputs": {
                "delta_t_obs_s": str(DT_OBS),
                "distance_m": str(DIST_M),
                "c_m_s": str(C_LIGHT),
                "band_hz": [float(F_LO), float(F_HI)],
            },
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0229 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
