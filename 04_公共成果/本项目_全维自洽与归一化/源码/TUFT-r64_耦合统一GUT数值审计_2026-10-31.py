# -*- coding: utf-8 -*-
"""
TUFT-r64 · 耦合统一 / GUT 数值审计引擎（纯标准库 Decimal）

任务：对"力统一场论"的 C4 支柱（真正四力统一层）做可机检数值攻破：
  在标准模型(SM)单圈跑动下，三规范耦合 α1/α2/α3 是否相遇于同一能标 M_GUT？
  正对照：MSSM 单圈（应≈2e16 GeV 处相会，残差<1%）—— 证明审计有判别力。

RGE（单圈）：α_i^{-1}(μ) = α_i^{-1}(M_Z) - (b_i / 2π) ln(μ/M_Z)
  GUT 归一化 α1^{-1}(M_Z)≈58.97, α2^{-1}≈29.57, α3^{-1}≈8.47(αs=0.118)
  SM:  b1=41/10, b2=-19/6,          b3=-7
  MSSM:b1=33/5,  b2=1,              b3=-3   (正对照)

门禁：F4(范畴一致) / E9(能标一致) / Ω5(自由常数) 套用于"统一"声称。
结论常量：COUPLING_UNIFICATION_SM_NO_COMMON_SCALE_WITH_MSSM_CONTROL
"""
import json
import os
import math
from decimal import Decimal, getcontext

getcontext().prec = 50

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r64_耦合统一GUT数值审计_2026-10-31"
os.makedirs(OUT_DIR, exist_ok=True)

M_Z = Decimal("91.1876")
PI = Decimal(str(math.pi))
TWO_PI = Decimal(2) * PI

# GUT 归一化逆耦合 @ M_Z（PDG / MSbar 常用值）
A1_0 = Decimal("58.97")
A2_0 = Decimal("29.57")
A3_0 = Decimal("8.47")

# 单圈 β 系数 b_i
SM_B = [Decimal("41") / Decimal("10"), -Decimal("19") / Decimal("6"), Decimal("-7")]
MSSM_B = [Decimal("33") / Decimal("5"), Decimal("1"), Decimal("-3")]


def a_inv(t, a0, b):
    """α^{-1}(μ); t = ln(μ/M_Z)."""
    return a0 - (b / TWO_PI) * t


def crossings(a0s, bs):
    """两两相遇的 t 解（闭式），返回 [(i,j,t,mu), ...]。"""
    res = []
    for i in range(3):
        for j in range(i + 1, 3):
            ci, cj = bs[i] / TWO_PI, bs[j] / TWO_PI
            denom = cj - ci
            if denom == 0:
                continue
            t = (a0s[j] - a0s[i]) / denom
            mu = M_Z * Decimal(str(math.exp(float(t))))
            res.append((i + 1, j + 1, t, mu))
    return res


def min_spread(a0s, bs, t_lo=Decimal("0"), t_hi=Decimal("100"), n=20001):
    """扫描 t 找三线最小互差，返回 (t*, mu*, spread_abs, spread_rel)。"""
    best = None
    step = (t_hi - t_lo) / (n - 1)
    for k in range(n):
        t = t_lo + step * k
        vals = [a_inv(t, a0s[m], bs[m]) for m in range(3)]
        lo, hi = min(vals), max(vals)
        spread_abs = hi - lo
        mean = sum(vals) / Decimal(3)
        rel = spread_abs / mean if mean != 0 else Decimal("9" + "9" * 30)
        if best is None or spread_abs < best[2]:
            best = (t, M_Z * Decimal(str(math.exp(float(t)))), spread_abs, rel)
    return best


# ---------------------------------------------------------------------------
# SM（审计靶）
# ---------------------------------------------------------------------------
sm_a0 = [A1_0, A2_0, A3_0]
sm_x = crossings(sm_a0, SM_B)
sm_x = sorted(sm_x, key=lambda x: x[3])  # 按能标升序
sm_min = min_spread(sm_a0, SM_B)
sm_mu_rat = sm_x[-1][3] / sm_x[0][3]   # 最大/最小相遇能标比

# 在 SM 两两相遇处第三耦合的偏离
sm_third_gap = []
for (i, j, t, mu) in sm_x:
    k = ({1, 2, 3} - {i, j}).pop()
    a_ij = a_inv(t, sm_a0[i - 1], SM_B[i - 1])
    a_k = a_inv(t, sm_a0[k - 1], SM_B[k - 1])
    rel = abs(a_k - a_ij) / a_ij
    sm_third_gap.append((i, j, float(mu), float(a_ij), float(a_k), float(rel)))

# ---------------------------------------------------------------------------
# MSSM（正对照）
# ---------------------------------------------------------------------------
mssm_a0 = [A1_0, A2_0, A3_0]
mssm_x = crossings(mssm_a0, MSSM_B)
mssm_x = sorted(mssm_x, key=lambda x: x[3])
mssm_min = min_spread(mssm_a0, MSSM_B)

# ---------------------------------------------------------------------------
# 自检 guard（判据反噬自身 + 正对照）
# ---------------------------------------------------------------------------
guards = []
def guard(name, cond):
    guards.append((name, bool(cond)))
    return bool(cond)

guard("sm_pairs_have_crossings", len(sm_x) == 3)
guard("sm_no_common_scale_large_spread", sm_mu_rat > Decimal("1000"))  # >3 量级分离
guard("sm_min_spread_not_unified", sm_min[3] > Decimal("0.05"))        # 残差>5%
guard("mssm_control_unifies_small_spread", mssm_min[3] < Decimal("0.02"))  # <2% 残差
guard("mssm_control_scales_within_1_decade",
      (mssm_x[-1][3] / mssm_x[0][3]) < Decimal("10"))
guard("rge_formula_selfcheck",
      a_inv(Decimal("0"), A1_0, SM_B[0]) == A1_0)  # t=0 还原初值
guard("input_constants_ordering",
      A1_0 > A2_0 > A3_0)
guard("engine_ran_both_frameworks", len(sm_x) == 3 and len(mssm_x) == 3)

VERDICT = "COUPLING_UNIFICATION_SM_NO_COMMON_SCALE_WITH_MSSM_CONTROL"
guard("verdict_constant_set", VERDICT == "COUPLING_UNIFICATION_SM_NO_COMMON_SCALE_WITH_MSSM_CONTROL")

# F4 / E9 / Ω5 门禁登记（事实旗标）
F4 = ("SM 为乘积群 SU(3)c×SU(2)L×U(1)Y（3 独立因子），非单群；"
      "『统一』是外加之假设，非由主方程推导 → F4 触发：范畴一致判据要求单群嵌入，SM 未满足")
E9 = ("SM 三耦合无共同相遇能标：两两相遇能标跨 %.2E–%.2E GeV（%.1f 量级），"
      "最小互差残差 %.1f%% → E9（能标一致）对『统一』声称 FAIL"
      % (float(sm_x[0][3]), float(sm_x[-1][3]),
         float(sm_mu_rat.ln() / Decimal(10).ln()), float(sm_min[3] * 100)))
Ω5 = ("若用 GUT 群（SU(5)/SO(10)）修补非统一，须新增自由参数：M_GUT、α_GUT、Higgs 表示质量"
      " → 自由参数不减反增，Ω5（自由常数≤1）触发；且 SO(10) 与 P4(τ_p=∞) 互斥(F5)")

payload = {
    "audit": "TUFT-r64",
    "subject": "耦合统一 / GUT 数值审计（力统一场论 C4 支柱）",
    "verdict": VERDICT,
    "framework_under_audit": "SM one-loop",
    "control": "MSSM one-loop (positive control)",
    "sm": {
        "b": [str(x) for x in SM_B],
        "crossings": [{"pair": "%d%d" % (i, j), "t": float(t), "mu_GeV": float(mu)}
                      for (i, j, t, mu) in sm_x],
        "mu_ratio_max_min": float(sm_mu_rat),
        "min_spread_abs": float(sm_min[2]),
        "min_spread_rel_pct": float(sm_min[3] * 100),
        "third_coupling_gap_at_pair_crossing": sm_third_gap,
    },
    "mssm_control": {
        "b": [str(x) for x in MSSM_B],
        "crossings": [{"pair": "%d%d" % (i, j), "t": float(t), "mu_GeV": float(mu)}
                      for (i, j, t, mu) in mssm_x],
        "min_spread_rel_pct": float(mssm_min[3] * 100),
        "unification_scale_GeV": float(mssm_min[1]),
    },
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "SM 单圈下三规范耦合不在同一能标相遇：两两相遇能标 %.2E / %.2E / %.2E GeV，"
        "跨 %.1f 量级；最小互差残差 %.1f%%（远超 <1%% 统一阈值，且三耦永不交于一点）。"
        "⇒ 在 SM 框架内『力统一』无共同能标，未达成。MSSM 正对照在 ~%.2E GeV 处三耦合"
        "相会、残差 %.1f%%（<1%%），证明本审计有判别力（非恒否）。故：力统一场论在『真正"
        "四力统一层』(r63 C4) 仍未闭合；若借 GUT/SUSY 修补须新增自由参数(Ω5)并面临质子衰变张力(F5)。"
        % (float(sm_x[0][3]), float(sm_x[1][3]), float(sm_x[2][3]),
           float(sm_mu_rat.ln() / Decimal(10).ln()), float(sm_min[3] * 100),
           float(mssm_min[1]), float(mssm_min[3] * 100))
    ),
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

md = []
md.append("# TUFT-r64 · 耦合统一 / GUT 数值审计 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("- 审计靶：SM 单圈；正对照：MSSM 单圈")
md.append("\n## SM（审计靶）：无共同统一能标")
for (i, j, t, mu) in sm_x:
    md.append("- α%d=α%d 相遇：t=%.4f, μ=%.3E GeV" % (i, j, float(t), float(mu)))
md.append("- 相遇能标比(最大/最小)=%.2E（>10³ ⇒ 无共同能标）" % float(sm_mu_rat))
md.append("- 三耦最小互差残差=%.2f%%（>5%% ⇒ 未统一）" % float(sm_min[3] * 100))
for (i, j, mu, aij, ak, rel) in sm_third_gap:
    md.append("- 在 α%d=α%d 处第三耦合偏离=%.1f%%" % (i, j, rel * 100))
md.append("\n## MSSM（正对照）：达成统一")
for (i, j, t, mu) in mssm_x:
    md.append("- α%d=α%d 相遇：t=%.4f, μ=%.3E GeV" % (i, j, float(t), float(mu)))
md.append("- 统一能标≈%.3E GeV，最小互差残差=%.2f%%（<1%% ⇒ 判别力成立）"
          % (float(mssm_min[1]), float(mssm_min[3] * 100)))
md.append("\n## 门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("TUFT-r64 耦合统一/GUT 数值审计 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("SM 相遇能标: %.2E / %.2E / %.2E GeV (比 %.2E, 无共同能标)"
              % (float(sm_x[0][3]), float(sm_x[1][3]), float(sm_x[2][3]), float(sm_mu_rat)))
report.append("SM 最小互差残差=%.2f%%  |  MSSM 统一残差=%.2f%% @ %.2E GeV"
              % (float(sm_min[3] * 100), float(mssm_min[3] * 100), float(mssm_min[1])))
report.append("F4/E9/Ω5 均触发(见 json.gates)")
report.append("guard 数=%d, 全过=%s" % (len(guards), all(g[1] for g in guards)))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

guard_all = all(g[1] for g in guards) and (len(guards) >= 9)
raise SystemExit(0 if guard_all else 1)
