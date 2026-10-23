# -*- coding: utf-8 -*-
"""
attack_C0186_暗光子攻破_2026-10-21.py
独立复算：T028「暗光子 / 新轻玻色子」· 额外 U(1) 规范玻色子 A'

定位：母册 T028（行 119）：暗光子 A' = 额外 U(1) 规范玻色子，撞 C1/C2。
主题：动力学混合 ε（L ⊃ -ε/2 F'_{μν} F^{μν}）、质量窗口 meV–GeV、实验搜索
约束（NA64/BABAR/LHCb）。

把"暗光子从哪来"压缩成五条可复核读数 + 一张输入账单：

  E1 暗光子现状事实：零发现（零结果）；NA64/BABAR/LHCb 排除线（实验值只引用不复算）。
  E2 **动力学混合重参数化 + ε 窗口 / 质量窗口精算（本册核心）**：
     对角化后 A' 对 EM 流耦合 = ε·e；ε 窗口 1e-16–1e-2 扫点；质量窗口 meV–GeV
     几何均值与跨度精算。
  E3 对撞机截面标度 σ ∝ ε² 核算：NA64 约束 ε² ≲ 1e-10 ⇒ ε ≲ 1e-5，
     复算各 ε 点相对 NA64 灵敏度的截面比值。
  E4 暗物质候选衔接 C0139（WIMP 线）：若 A' 为暗物质媒介，σv ∝ ε² g_D²/m_A'²，
     所需新参数账单。
  E5 裁定：暗光子 = 额外 U(1) 规范自由度（新对称性 + 新玻色子）；TUFT 无新规范群、
     无动力学混合供给 ⇒ 结构性负面，撞 C1/C2。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称已发现/解决暗光子；实验排除线只引用不复算；
数值均为标准粒子物理算术或实验约束复核；TUFT 已注销（C0133），
严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（实验/PDG 只引用不复算） ----------
# 动力学混合窗口（文献综述典型范围）
EPS_MIN = Decimal("1e-16")   # 超弱混合（hidden-sector 极暗端）
EPS_MAX = Decimal("1e-2")    # 强混合端（已被大部分实验排除）
# 暗光子质量窗口
M_MIN_eV = Decimal("1e-3")   # 1 meV
M_MAX_eV = Decimal("1e9")    # 1 GeV
# NA64（CERN）对低质量暗光子的约束：ε² ≲ 1e-10（m_A' ≲ 100 MeV，引用）
NA64_EPS2_BOUND = Decimal("1e-10")
# 精细结构常数（CODATA 引用）
ALPHA_EM = Fraction(1, 137)          # α ≈ 1/137.036，本册取 1/137 量级
# 标准 WIMP 热 relic 截面（Canonical，引用）
SIGMA_V_WIMP = Decimal("3e-26")      # cm^3/s


def e1_status():
    """暗光子现状事实（实验排除线只引用）。"""
    return {
        "discovered": False,
        "experiments_cited": ["NA64 (CERN)", "BABAR", "LHCb", "LSND/miniBooNE"],
        "na64_eps2_bound": NA64_EPS2_BOUND,   # m_A' ≲ 100 MeV
        "babar_eps_floor": "~2e-3",            # 亚 GeV 区
        "lhcb_eps_floor": "~1e-3",             # 双缪共振 2π–60 GeV
    }


def e2_mixing_and_windows():
    """动力学混合重参数化 + ε 窗口 / 质量窗口精算（核心）。"""
    # 对角化：L ⊃ -1/4 F^2 - 1/4 F'^2 - ε/2 F F'
    # 场重定义 A_μ -> A_μ + ε A'_μ 后，A' 对 EM 流的物理耦合 = ε·e
    # e = sqrt(4π α)，本册用 Decimal 精算（α=1/137 量级，π 取 Decimal 近似）
    pi_dec = Decimal("3.1415926535897932384626433832795028841971693993751")
    alpha_dec = Decimal(ALPHA_EM.numerator) / Decimal(ALPHA_EM.denominator)
    e_coupling_dec = (Decimal(4) * pi_dec * alpha_dec).sqrt()

    # ε 窗口扫点
    eps_ratio = EPS_MAX / EPS_MIN                    # 1e14
    eps_decades = (EPS_MAX.ln() - EPS_MIN.ln()) / Decimal(10).ln()
    eps_geom = (EPS_MIN * EPS_MAX).sqrt()            # sqrt(1e-18)=1e-9

    # 质量窗口（eV）
    mass_ratio = M_MAX_eV / M_MIN_eV                 # 1e12
    mass_decades = (M_MAX_eV.ln() - M_MIN_eV.ln()) / Decimal(10).ln()
    mass_geom_eV = (M_MIN_eV * M_MAX_eV).sqrt()      # sqrt(1e6)=1e3 eV=1 keV

    return {
        "e_coupling_order": e_coupling_dec,
        "eps_min": EPS_MIN, "eps_max": EPS_MAX,
        "eps_ratio": eps_ratio, "eps_decades": eps_decades, "eps_geom_mean": eps_geom,
        "mass_min_eV": M_MIN_eV, "mass_max_eV": M_MAX_eV,
        "mass_ratio": mass_ratio, "mass_decades": mass_decades,
        "mass_geom_mean_eV": mass_geom_eV,
        "physical_coupling": "g_A'EM = ε·e",
    }


def e3_collider_scaling():
    """对撞机截面 σ ∝ ε² 标度核算。"""
    eps_bound = NA64_EPS2_BOUND.sqrt()               # sqrt(1e-10)=1e-5
    # σ(ε)/σ(ε_bound) = (ε/ε_bound)^2
    def sig_ratio(eps):
        return (eps / eps_bound) ** 2
    r_max = sig_ratio(EPS_MAX)       # (1e-2/1e-5)^2 = 1e6
    r_min = sig_ratio(EPS_MIN)       # (1e-16/1e-5)^2 = 1e-22
    # NA64 覆盖的 ε 上边界以上被排除；以下未被 NA64 触及的十倍数
    uncovered_decades = (eps_bound.ln() - EPS_MIN.ln()) / Decimal(10).ln()  # 11
    excluded_decades = (EPS_MAX.ln() - eps_bound.ln()) / Decimal(10).ln()   # 3
    return {
        "na64_eps2_bound": NA64_EPS2_BOUND,
        "eps_bound": eps_bound,
        "sigma_ratio_at_eps_max": r_max,
        "sigma_ratio_at_eps_min": r_min,
        "uncovered_decades_below_bound": uncovered_decades,
        "excluded_decades_above_bound": excluded_decades,
    }


def e4_dm_link():
    """暗物质候选衔接 C0139（WIMP 线）。"""
    # 若 A' 为暗物质媒介：σv ∝ ε² · g_D² / m_A'²
    # 要达到 canonical σv ~ 3e-26 cm^3/s，需同时给定 g_D、m_A'、ε 三个新量。
    # 新参数账单：g_D（暗区规范耦合）、ε（动力学混合）、m_A'（A' 质量）。
    new_params = ["g_D (hidden U(1) gauge coupling)",
                  "epsilon (kinetic mixing)",
                  "m_A' (dark photon mass)"]
    return {
        "thermal_relic_sigma_v": SIGMA_V_WIMP,
        "scaling": "sigma_v ∝ eps^2 * g_D^2 / m_A'^2",
        "new_free_params": len(new_params),
        "param_list": new_params,
        "links_to": "C0139 WIMP 暗物质线",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0186 · 暗光子 / 新轻玻色子（母册 T028 · 额外 U(1)）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_status()
    w("\n[E1] 暗光子现状事实（实验排除线只引用不复算）")
    w("  是否发现：%s；至今日均为零结果。" % ("否（零发现）" if not g1["discovered"] else "是"))
    w("  在役/历史实验：%s" % ", ".join(g1["experiments_cited"]))
    w("  NA64（m_A'≲100 MeV）约束 ε² ≲ %s ⇒ ε ≲ %s"
      % (fv(g1["na64_eps2_bound"], "1e"), fv(g1["na64_eps2_bound"].sqrt(), "1e")))
    w("  BABAR 亚 GeV 区 ε ≳ %s 被排除；LHCb 双缪区 ε ≳ %s 被排除。"
      % (g1["babar_eps_floor"], g1["lhcb_eps_floor"]))
    w("  => 暗光子是**尚未发现的额外 U(1) 规范玻色子**，约束全部来自零结果上限。")
    entries.append(("E1", "暗光子零发现；NA64/BABAR/LHCb 均给上限约束（实验值只引用）",
                    "PASS", "实验排除线引用；本册不重测"))

    # ---- E2 ----
    g2 = e2_mixing_and_windows()
    w("\n[E2] 动力学混合重参数化 + 窗口精算（本册核心）")
    w("  L ⊃ -1/4 F^2 -1/4 F'^2 - ε/2 F F'；场重定义 A_μ->A_μ+ε A'_μ 后")
    w("  A' 对 EM 流物理耦合 = g_A'EM = ε·e（e≈%s，α=1/137 量级）。"
      % fv(g2["e_coupling_order"], "3f"))
    w("  ε 窗口：%s – %s；跨度 = %s（即 %s 个数量级）；几何均值 = %s"
      % (fv(g2["eps_min"], "1e"), fv(g2["eps_max"], "1e"),
         fv(g2["eps_ratio"], "1e"), fv(g2["eps_decades"], "1f"),
         fv(g2["eps_geom_mean"], "1e")))
    w("  质量窗口：%s eV – %s eV；跨度 = %s（即 %s 个数量级）；"
      % (fv(g2["mass_min_eV"], "1e"), fv(g2["mass_max_eV"], "1e"),
         fv(g2["mass_ratio"], "1e"), fv(g2["mass_decades"], "1f")))
    w("  几何均值 = %s eV = %s keV。"
      % (fv(g2["mass_geom_mean_eV"], "1e"), fv(g2["mass_geom_mean_eV"]/Decimal(1000), "1f")))
    w("  => 暗光子物理完全由 (ε, m_A') 两个自由参数张成：ε 跨 %s 个数量级、"
      "m_A' 跨 %s 个数量级，均为**外部输入的纯数与标度**。"
      % (fv(g2["eps_decades"], "0f"), fv(g2["mass_decades"], "0f")))
    entries.append(("E2", "ε 窗口 %s–%s（%s 个数量级，几何均值 %s）；"
                    "m_A' %s eV–%s eV（%s 个数量级，几何均值 %s eV）"
                    % (fv(g2["eps_min"], "1e"), fv(g2["eps_max"], "1e"),
                       fv(g2["eps_decades"], "0f"), fv(g2["eps_geom_mean"], "1e"),
                       fv(g2["mass_min_eV"], "1e"), fv(g2["mass_max_eV"], "1e"),
                       fv(g2["mass_decades"], "0f"), fv(g2["mass_geom_mean_eV"], "1e")),
                    "PASS", "Decimal 48 位精算；α=1/137 量级引用"))

    # ---- E3 ----
    g3 = e3_collider_scaling()
    w("\n[E3] 对撞机截面标度 σ ∝ ε² 核算")
    w("  NA64 约束 ε² ≲ %s ⇒ 换算 ε_bound = %s。"
      % (fv(g3["na64_eps2_bound"], "1e"), fv(g3["eps_bound"], "1e")))
    w("  σ(ε)/σ(ε_bound) = (ε/ε_bound)^2：")
    w("    ε=%s（强混合端）⇒ 截面为 NA64 灵敏度的 %s 倍（远在排除区内）。"
      % (fv(EPS_MAX, "1e"), fv(g3["sigma_ratio_at_eps_max"], "1e")))
    w("    ε=%s（超弱端）⇒ 截面仅为 NA64 灵敏度的 %s 倍（完全不可见）。"
      % (fv(EPS_MIN, "1e"), fv(g3["sigma_ratio_at_eps_min"], "1e")))
    w("  NA64 实际只排除 ε 上限 %s 个数量级（ε≳%s）；ε<%s 的 %s 个数量级对 NA64 不敏感。"
      % (fv(g3["excluded_decades_above_bound"], "0f"), fv(g3["eps_bound"], "1e"),
         fv(g3["eps_bound"], "1e"), fv(g3["uncovered_decades_below_bound"], "0f")))
    w("  => σ∝ε² 标度算术自洽：ε 每降一个数量级，截面降 100 倍（复算确认）。")
    entries.append(("E3", "σ∝ε²：NA64 ε²≲1e-10 ⇒ ε≲1e-5；"
                    "ε=1e-2 端截面为灵敏度 1e6 倍、ε=1e-16 端仅 1e-22 倍；"
                    "NA64 仅排除 3 个数量级、11 个数量级不敏感",
                    "PASS", "标准粒子物理截面标度算术复核"))

    # ---- E4 ----
    g4 = e4_dm_link()
    w("\n[E4] 暗物质候选衔接 C0139（WIMP 线）")
    w("  若 A' 为暗物质媒介，σv ∝ ε²·g_D²/m_A'²；达到 canonical 热 relic σv≈%s cm^3/s "
      "须同时给定：" % fv(g4["thermal_relic_sigma_v"], "1e"))
    for p in g4["param_list"]:
        w("    - %s" % p)
    w("  即 %d 个新自由参数（g_D、ε、m_A'），全部为外部输入；与 %s 同属暗物质自由度账单。"
      % (g4["new_free_params"], g4["links_to"]))
    w("  => 暗光子即便存在，也只是给暗物质线再加一个媒介玻色子，不减少任何外部输入。")
    entries.append(("E4", "A' 作 DM 媒介需新参数 g_D/ε/m_A'（%d 个外部输入），"
                    "与 C0139 WIMP 线同账单，不减少自由度" % g4["new_free_params"],
                    "PASS", "暗物质衔接；新参数账单"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  暗光子问题被精确翻译成两件事：(a) 额外 U(1) 规范对称性与 A' 规范玻色子从哪来；")
    w("  (b) 其动力学混合 ε 与质量 m_A' 两个自由标度从哪来。")
    w("  (a) TUFT/几何框架无新规范群供给——SM 规范群 SU(3)×SU(2)×U(1) 之外，")
    w("      框架不产出任何新的 U(1) 因子，也不产出 A' 这个新规范玻色子（撞 C1）。")
    w("  (b) 动力学混合项 -ε/2 F F' 是额外拉氏量自由度，框架不供给 ε 与 m_A'；")
    w("      ε 跨 14 个数量级、m_A' 跨 12 个数量级，全是外部输入（撞 C2）。")
    w("  => **T028 结构性负面（对 TUFT/几何框架）**；撞 C1（粒子内容：新规范玻色子须公设）"
      " / C2（绝对标度：m_A'、ε 须外部输入）。按母册登记撞 C1/C2 复核一致。")
    entries.append(("E5", "T028 结构性负面：暗光子=额外 U(1) 新规范自由度，"
                    "TUFT 无新规范群/无动力学混合供给", "PASS", "撞 C1/C2（母册登记一致）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "质量窗口跨度 = 1e12（1 meV–1 GeV = 12 个数量级）",
         g2["mass_ratio"] == Decimal("1e12")),
        ("G2", "质量窗口几何均值 = 1e3 eV = 1 keV",
         g2["mass_geom_mean_eV"] == Decimal("1e3")),
        ("G3", "ε 窗口几何均值 = 1e-9",
         g2["eps_geom_mean"] == Decimal("1e-9")),
        ("G4", "NA64 ε²≲1e-10 ⇒ ε_bound = 1e-5",
         g3["eps_bound"] == Decimal("1e-5")),
        ("G5", "σ(ε=1e-2)/σ(ε=1e-5) = 1e6（σ∝ε² 标度）",
         g3["sigma_ratio_at_eps_max"] == Decimal("1e6")),
        ("G6", "A' 作 DM 媒介引入 3 个新自由参数",
         g4["new_free_params"] == 3),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0186 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已发现/解决暗光子：实验排除线只引用；数值均为标准粒子物理算术或")
    w("  实验约束复核；TUFT 已注销（C0133），不把标准物理结果写成 TUFT 预测/修正。")
    w("  裁的是「TUFT/几何框架能否供给额外 U(1) 规范群与动力学混合」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0186_暗光子攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0186_暗光子攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0186_dark_photon",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_status": {k: str(v) for k, v in g1.items()},
            "E2_mixing_windows": {k: str(v) for k, v in g2.items()},
            "E3_collider": {k: str(v) for k, v in g3.items()},
            "E4_dm_link": {k: (str(v) if not isinstance(v, list) else v)
                           for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0186 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
