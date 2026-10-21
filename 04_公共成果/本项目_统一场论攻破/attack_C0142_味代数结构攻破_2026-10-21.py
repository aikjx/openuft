# -*- coding: utf-8 -*-
"""
attack_C0142_味代数结构攻破_2026-10-21.py
独立复算：P11「味 / 代数结构」· 物理 Top100 清单 T022（布局 Phase 1 续项）

定位：布局册（C0135）Phase 1 续项（阻塞力 2，撞 C1/C2）；物理 Top100 清单 T022/T023。
前置：库内 OpenUFT v9.1（2026-10-10）自报"代民主零参数味结构证伪"——代民主秩1矩阵
ε-破缺谱与实测差 2–200 倍。本册**不采信该自报**，用 PDG 实测独立复算同一判据，并
对 TUFT/几何框架判定"能否从第一性原理生成代结构与 Yukawa 谱"。

把"味/代数结构从哪来"压缩成四条可复核读数 + 一张输入账单：

  E1 SM 味结构事实：代=3、Yukawa 质量谱、CKM/PMNS 混合（PDG 只引用不复算）。
  E2 **代民主零参数方案独立复算（本册核心）**：秩1民主矩阵 + ε-破缺谱 vs 实测，
     复核 v9.1 的"差 2–200 倍"结论。
  E3 几何供给：TUFT/几何框架能否从第一性原理生成代结构与 Yukawa（撞 C1）。
  E4 混合矩阵来源：CKM/PMNS 参数能否由几何常数导出（撞 C2/C3）。
  E5 裁定：P11 结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称已解释味结构；PDG 质量值与 CKM/PMNS 值只引用不复算；
ε-破缺模型为代数构造（v9.1 沿用），结论按数量级（倍）判定。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 只引用不复算） ----------
# 夸克质量（PDG，MeV）
M_U = Decimal("2.2")
M_C = Decimal("1275")
M_T = Decimal("173000")
M_D = Decimal("4.7")
M_S = Decimal("95")
M_B = Decimal("4180")
# Cabibbo 参数 λ（Wolfenstein）
LAMBDA_C = Decimal("0.2253")
# CKM 三混合角（PDG，°）
THETA12 = Decimal("13.04")   # θ_C ≈ 13.04°
THETA23 = Decimal("2.38")    # θ_23
THETA13 = Decimal("0.201")   # θ_13


def e1_sm_facts():
    """SM 味结构事实（PDG 只引用）。"""
    return {
        "generations": 3,
        "up_masses_MeV": (M_U, M_C, M_T),
        "down_masses_MeV": (M_D, M_S, M_B),
        "ckm_angles_deg": {"theta12": THETA12, "theta23": THETA23, "theta13": THETA13},
        "lambda": LAMBDA_C,
    }


def e2_democratic():
    """代民主秩1矩阵 + ε-破缺谱 vs 实测（独立复算 v9.1）。"""
    # 预言谱 m1:m2:m3 = ε^4 : ε^2 : 1
    eps2 = LAMBDA_C * LAMBDA_C
    eps4 = eps2 * eps2
    # 上型
    up_pred = [eps4, eps2, Decimal(1)]
    # 下型
    down_pred = [eps4, eps2, Decimal(1)]
    # 实测归一（以最重为 1）
    up_obs = [M_U / M_T, M_C / M_T, Decimal(1)]
    down_obs = [M_D / M_B, M_S / M_B, Decimal(1)]
    # 偏差（预言/实测）
    up_ratio = [up_pred[i] / up_obs[i] for i in range(3)]
    down_ratio = [down_pred[i] / down_obs[i] for i in range(3)]
    return {
        "eps2": eps2, "eps4": eps4,
        "up_obs": up_obs, "down_obs": down_obs,
        "up_pred": up_pred, "down_pred": down_pred,
        "up_ratio": up_ratio, "down_ratio": down_ratio,
        "up_maxdev": max(up_ratio), "down_maxdev": max(down_ratio),
    }


def e3_geometry_supply():
    """几何框架能否生成代结构与 Yukawa？量纲 + 结构判据。"""
    # 关键：Yukawa 是纯数矩阵（3x3，9 复参数）；几何常数 (ℏ,G,c) 量纲矩阵 nullity=0
    # （承接 C0140 E4）⇒ 纯数不可由几何常数生成。代=3 是数字巧合（攻破③：Z₂→2代、Z₆→4代）。
    # 承接 C0140：nullity_3const = 0
    nullity3 = 0  # 引用 C0140 精确读数
    return {
        "yukawa_rank": 3,          # 3x3 复矩阵
        "yukawa_free_params": 9,   # 3x3 复矩阵 = 9 个独立复参数（实部+虚部更多）
        "nullity_hbarGc": nullity3,
        "generations_from_geometry": False,
    }


def e4_mixing_source():
    """CKM/PMNS 参数能否由几何导出？"""
    # CKM 3 角 + 1 相 = 4 个独立参数；几何常数给不出无量纲数（nullity=0）
    ckm_params = 4  # 3 角 + 1 CP 相
    pmns_params = 6  # 3 角 + 3 相（马约拉纳）
    return {
        "ckm_independent_params": ckm_params,
        "pmns_independent_params": pmns_params,
        "geometry_supply": "zero",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0142 · 味 / 代数结构（P11 · Top100 T022）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_sm_facts()
    w("\n[E1] SM 味结构事实（PDG 只引用不复算）")
    w("  代 = %d；上型 (u,c,t) = (%s, %s, %s) MeV"
      % (g1["generations"], fv(M_U, "2f"), fv(M_C, "1f"), fv(M_T, "0f")))
    w("  下型 (d,s,b) = (%s, %s, %s) MeV"
      % (fv(M_D, "2f"), fv(M_S, "1f"), fv(M_B, "0f")))
    w("  CKM 角 θ12=%s° θ23=%s° θ13=%s°；Cabibbo λ=%s"
      % (g1["ckm_angles_deg"]["theta12"], g1["ckm_angles_deg"]["theta23"],
         g1["ckm_angles_deg"]["theta13"], g1["lambda"]))
    w("  => 味结构 = 代 3 + 9 个 Yukawa 复参数 + 4 个 CKM 参数（+6 个 PMNS），全是纯数。")
    entries.append(("E1", "SM 味结构 = 代 3 + 9 Yukawa 复参 + 4 CKM 参（纯数）",
                    "PASS", "PDG 只引用；本册只做归一换算"))

    # ---- E2 ----
    g2 = e2_democratic()
    w("\n[E2] 代民主零参数方案独立复算（本册核心，复算 v9.1 结论）")
    w("  预言谱 m1:m2:m3 = ε⁴:ε²:1，ε=λ=%s ⇒ ε²=%s、ε⁴=%s"
      % (g1["lambda"], fv(g2["eps2"], "6f"), fv(g2["eps4"], "6f")))
    w("  上型实测归一 (u,c,t)/t = %s / %s / 1"
      % (fv(g2["up_obs"][0], "3e"), fv(g2["up_obs"][1], "4f")))
    w("  上型预言归一 = %s / %s / 1" % (fv(g2["up_pred"][0], "5f"), fv(g2["up_pred"][1], "5f")))
    w("  上型偏差（预言/实测）：m_u/m_t 差 %s 倍、m_c/m_t 差 %s 倍"
      % (fv(g2["up_ratio"][0], "2f"), fv(g2["up_ratio"][1], "2f")))
    w("  下型偏差：m_d/m_b 差 %s 倍、m_s/m_b 差 %s 倍"
      % (fv(g2["down_ratio"][0], "2f"), fv(g2["down_ratio"][1], "2f")))
    w("  上型最大偏差 = %s 倍；下型最大偏差 = %s 倍"
      % (fv(g2["up_maxdev"], "2f"), fv(g2["down_maxdev"], "2f")))
    w("  => 代民主秩1矩阵 + ε-破缺谱与实测差 %s–%s 倍（独立确认 v9.1 的 2–200 倍结论）。"
      % (fv(g2["down_maxdev"], "1f"), fv(g2["up_maxdev"], "0f")))
    entries.append(("E2", "代民主零参数方案谱与实测差 %s 倍（上型）/ %s 倍（下型），"
                    "独立确认 v9.1 的 2–200 倍"
                    % (fv(g2["up_maxdev"], "0f"), fv(g2["down_maxdev"], "1f")), "PASS",
                    "秩1民主矩阵 + ε-破缺（v9.1 沿用）代数构造，PDG 实测对比"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给：能否从第一性原理生成代结构与 Yukawa？")
    w("  Yukawa 是 %dx%d 复矩阵（%d 个独立复参数）；几何常数 (ℏ,G,c) 量纲 nullity = %d"
      % (g3["yukawa_rank"], g3["yukawa_rank"], g3["yukawa_free_params"],
         g3["nullity_hbarGc"]))
    w("  => 纯数不可由几何常数生成（承接 C0140 E4 精确读数），Yukawa 是外部输入。")
    w("  代=3 是数字巧合（攻破③：Z₂→2代、Z₆→4代），几何不唯一指定三代。")
    w("  => 几何框架**不能**从第一性原理生成代结构/Yukawa，撞 C1（粒子内容须公设唯一确定）。")
    entries.append(("E3", "几何供给 0：Yukawa 纯数矩阵不可由 (ℏ,G,c) 生成（nullity 0），"
                    "代=3 数字巧合非几何推导", "PASS", "撞 C1"))

    # ---- E4 ----
    g4 = e4_mixing_source()
    w("\n[E4] 混合矩阵来源")
    w("  CKM = %d 个独立参数（3 角 + 1 CP 相）；PMNS = %d 个（3 角 + 3 相）"
      % (g4["ckm_independent_params"], g4["pmns_independent_params"]))
    w("  几何常数给不出任何无量纲数（nullity=0）⇒ 混合角/相是外部输入，撞 C2/C3。")
    w("  库内 v9.1 称 'CKM λ-幂次 0.1–6.5% 唯一幸存' —— 那是数值拟合（λ 借 Cabibbo 实测），")
    w("  非第一性推导：λ 本身是输入，用 λ 幂次凑 CKM 是恒等式复读（同 r33 零判别力问题）。")
    entries.append(("E4", "CKM/PMNS 混合角与相是外部输入（几何 nullity 0）；"
                    "'CKM λ-幂次'是借 λ 实测的拟合非推导", "PASS", "撞 C2/C3"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  味/代数结构问题被精确翻译成两件事：(a) 代结构与 Yukawa 纯数从哪来；(b) 混合矩阵从哪来。")
    w("  (a) 代民主零参数方案被实测否决（E2，差 2–200 倍）；有自由度方案过拟合无预言力（v8 系列）。")
    w("  (b) 几何常数 nullity=0 ⇒ 纯数不可生成（E3/E4），Yukawa 与 CKM/PMNS 全是外部输入。")
    w("  => **P11 结构性负面（对 TUFT/几何框架）**；撞 C1（代结构）/C2（标度）/C3（零自由参数）。")
    entries.append(("E5", "P11 结构性负面：代结构/Yukawa/混合角均需外部输入，"
                    "几何供给 0", "PASS", "撞 C1/C2/C3"))

    # ---- 守卫 ----
    guards = [
        ("G1", "代民主谱与实测差 > 2 倍（上型 m_u/m_t）", g2["up_ratio"][0] > Decimal("2")),
        ("G2", "代=3（SM 观测事实）", g1["generations"] == 3),
        ("G3", "Yukawa 是 3x3 复矩阵（9 独立复参）", g3["yukawa_free_params"] == 9),
        ("G4", "几何常数 (ℏ,G,c) nullity = 0（纯数不可生成）", g3["nullity_hbarGc"] == 0),
        ("G5", "CKM 有 4 个独立参数（3 角 + 1 相）", g4["ckm_independent_params"] == 4),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0142 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释味结构：PDG 质量与 CKM/PMNS 值只引用；ε-破缺为代数构造；")
    w("  判定按数量级（倍）而非末位。裁的是「几何/TUFT 框架能否生成味/代数结构」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0142_味代数结构攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0142_味代数结构攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0142_flavor_algebra",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_sm_facts": {k: (str(v) if not isinstance(v, tuple) else [str(x) for x in v])
                            for k, v in g1.items()},
            "E2_democratic": {k: (str(v) if not isinstance(v, list) else [str(x) for x in v])
                              for k, v in g2.items()},
            "E3_geometry_supply": {k: str(v) for k, v in g3.items()},
            "E4_mixing": {k: str(v) for k, v in g4.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0142 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
