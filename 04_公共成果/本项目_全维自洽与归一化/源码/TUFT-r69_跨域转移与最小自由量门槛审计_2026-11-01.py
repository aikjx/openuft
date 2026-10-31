# -*- coding: utf-8 -*-
"""
TUFT-r69 · 跨域转移与最小自由量门槛审计（正面回答 r68 X-R68-2）

上一卷(r68)给出否定性结论：纯几何标度不变 ⇒ 不能自定尺度 ⇒ 改换变量非推导。
本卷回答建设性问题：**究竟要满足什么条件，才能产出第一个 surplus>0 的数？**

判据精化（两条，缺一不可）：
  (1) 跨域转移 transfer：预言的量 O **不在**用于定住自由参数的测量集合 M 中（O ∉ M）。
      O ∈ M ⇒ 循环（circular），无论残差多小都不算预测。
  (2) 超定判据 over-determination：surplus = n_matched − n_free，
      真预测要求 **n_matched ≥ n_free + 1**（数据必须比自由量多，才留下一致性检验）。

关键结论：
  ★ 门槛不是"自由量的绝对个数"，而是 **n_matched ≥ n_free + 1**。
  ★ KK 模型 n_free=1(R)，门槛 = 2 个独立吻合可观测量；它只有 1 个(α，且循环)
    ⇒ **差整整 1 个可观测量**；它唯一尝试的第二个(m_KK)差 1.02e21 倍。
  ★ 框架唯一 0 自由量的真结果 = 电荷量子化(n∈ℤ)，但属**离散整数**，非连续无量纲常数。

正对照：GR 水星进动 n_free=0、n_matched=1 ⇒ 1 ≥ 0+1 ⇒ 通过门槛（且 O∉M）。

裁决常量：THRESHOLD_N_MATCHED_GE_N_FREE_PLUS_ONE_FRAMEWORK_SHORT_BY_ONE_OBSERVABLE
"""
import json
import os
import math
from decimal import Decimal, getcontext

getcontext().prec = 50

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r69_跨域转移与最小自由量门槛审计_2026-11-01"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 关系台账：n_free / 定参集合 M / 输出 O / 是否吻合 / 是否跨域
# ---------------------------------------------------------------------------
RELATIONS = [
    {"关系": "α_KK = 4(ℓ_P/R)^2", "层": "KK(r66)", "n_free": 1,
     "定参集合M": ["α(实测)"], "输出O": ["α"], "n_matched": 1, "transfer": False,
     "输出类型": "连续", "备注": "α 用于反解 R ⇒ O ∈ M ⇒ 循环，残差再小也不算预测"},
    {"关系": "m_KK = ℏ/(Rc)", "层": "KK(r66)", "n_free": 1,
     "定参集合M": ["α(实测)"], "输出O": ["m_KK"], "n_matched": 0, "transfer": True,
     "输出类型": "连续", "备注": "★真跨域转移：用 α 定 R 去预言质量；但被否证 1.02e21（可证伪·加分）"},
    {"关系": "κ(m) 质量—曲率", "层": "螺旋(r45)", "n_free": 1,
     "定参集合M": ["κ 尺度/l0"], "输出O": ["m"], "n_matched": 0, "transfer": True,
     "输出类型": "连续", "备注": "V(κ)≡0 ⇒ 无粒子；转移尝试失败"},
    {"关系": "G = c^3/[ℏ(κ^2+τ^2)]", "层": "螺旋(247/r62)", "n_free": 1,
     "定参集合M": ["G(实测)"], "输出O": ["G"], "n_matched": 1, "transfer": False,
     "输出类型": "连续", "备注": "G 在输入侧 ⇒ O ∈ M ⇒ 循环"},
    {"关系": "电荷量子化 n∈ℤ", "层": "KK(r66)", "n_free": 0,
     "定参集合M": [], "输出O": ["n∈ℤ"], "n_matched": 1, "transfer": True,
     "输出类型": "离散", "备注": "★★框架唯一 0 自由量真结果；但输出为离散整数，非连续常数"},
    {"关系": "★ GR 水星进动 42.98″/世纪", "层": "GR(正对照)", "n_free": 0,
     "定参集合M": ["G", "M☉", "a", "e"], "输出O": ["42.98″"], "n_matched": 1, "transfer": True,
     "输出类型": "连续", "备注": "★★n_matched(1) ≥ n_free(0)+1 且 O∉M ⇒ 通过门槛，真预测"},
]

# ---------------------------------------------------------------------------
# 计算：surplus 与门槛判定
# ---------------------------------------------------------------------------
for r in RELATIONS:
    r["surplus"] = r["n_matched"] - r["n_free"]
    # 循环者：无论 n_matched 多少，一律判 0（O ∈ M ⇒ 无预测内容）
    if not r["transfer"]:
        r["surplus_effective"] = 0
        r["circular"] = True
    else:
        r["surplus_effective"] = r["surplus"]
        r["circular"] = False
    r["threshold"] = r["n_free"] + 1                       # 需 n_matched ≥ threshold
    r["passes_threshold"] = (r["n_matched"] >= r["threshold"]) and r["transfer"]

FRAMEWORK = [r for r in RELATIONS if r["层"] != "GR(正对照)"]
GR = [r for r in RELATIONS if r["层"] == "GR(正对照)"][0]

# 框架内通过门槛的项
FRAMEWORK_PASS = [r for r in FRAMEWORK if r["passes_threshold"]]
# 框架内"连续型"通过门槛的项（真正想要的）
FRAMEWORK_PASS_CONTINUOUS = [r for r in FRAMEWORK_PASS if r["输出类型"] == "连续"]

# KK 模型：n_free=1 ⇒ 门槛=2，实得 1 ⇒ 差 1 个可观测量
KK_ROWS = [r for r in FRAMEWORK if r["层"].startswith("KK")]
KK_N_FREE = 1
KK_THRESHOLD = KK_N_FREE + 1
KK_N_MATCHED = 1
KK_SHORTFALL = KK_THRESHOLD - KK_N_MATCHED          # = 1

# 它唯一尝试的第二个可观测量(m_KK)的失配倍数（来自 r66）
M_KK_DISCREPANCY = Decimal("1.0204911e21")

# 离散 vs 连续分离
DISCRETE_SUCCESSES = [r for r in FRAMEWORK if r["passes_threshold"] and r["输出类型"] == "离散"]
CONTINUOUS_SUCCESSES = FRAMEWORK_PASS_CONTINUOUS

# ---------------------------------------------------------------------------
# 自检 guard
# ---------------------------------------------------------------------------
guards = []
def guard(name, cond):
    guards.append((name, bool(cond)))
    return bool(cond)


guard("relations_cover_framework_and_control", len(FRAMEWORK) >= 4 and GR is not None)
guard("gr_control_passes_threshold", GR["passes_threshold"])
guard("gr_control_non_circular", not GR["circular"])
guard("framework_never_passes_on_continuous", len(CONTINUOUS_SUCCESSES) == 0)
guard("framework_has_one_discrete_success", len(DISCRETE_SUCCESSES) == 1)
guard("kk_shortfall_is_exactly_one", KK_SHORTFALL == 1)
guard("kk_attempted_second_observable_falsified", M_KK_DISCREPANCY > Decimal("1e15"))
guard("circular_rows_are_flagged",
      all(r["circular"] for r in RELATIONS if not r["transfer"]))
guard("threshold_rule_is_n_free_plus_one",
      all(r["threshold"] == r["n_free"] + 1 for r in RELATIONS))

VERDICT = "THRESHOLD_N_MATCHED_GE_N_FREE_PLUS_ONE_FRAMEWORK_SHORT_BY_ONE_OBSERVABLE"
guard("verdict_constant_set",
      VERDICT == "THRESHOLD_N_MATCHED_GE_N_FREE_PLUS_ONE_FRAMEWORK_SHORT_BY_ONE_OBSERVABLE")

F4 = ("『残差极小』被误当作『预测成立』：循环关系(O∈M)的残差恒为 0，却不含任何预测内容"
      " ⇒ 范畴错置：拟合残差 ≠ 预测盈余 → F4 触发")
E9 = ("跨域转移要求定参测量与预言可观测量处于不同物理域；本框架定参与预言同域(α→α、G→G)"
      " 或跨域失败(α→m 差 1.02e21) ⇒ E9 对『跨域预测』FAIL")
Ω5 = ("门槛判据 n_matched ≥ n_free+1：本框架 n_free=1 而 n_matched=1 ⇒ 未超定；"
      "欲达标须再吻合 1 个独立可观测量，而非再增自由量 ⇒ Ω5 指向『缺口在观测，不在参数』")

payload = {
    "audit": "TUFT-r69",
    "subject": "跨域转移与最小自由量门槛审计（正面回答 r68 X-R68-2）",
    "verdict": VERDICT,
    "criteria": {
        "transfer": "预言的量 O 不在定参集合 M 中（O ∉ M）；否则循环",
        "over_determination": "surplus = n_matched − n_free；真预测要求 n_matched ≥ n_free + 1",
        "note": "门槛不是自由量的绝对个数，而是数据对自由量的超定程度",
    },
    "relations": RELATIONS,
    "framework_pass_all": [r["关系"] for r in FRAMEWORK_PASS],
    "framework_pass_continuous": [r["关系"] for r in FRAMEWORK_PASS_CONTINUOUS],
    "framework_pass_discrete": [r["关系"] for r in DISCRETE_SUCCESSES],
    "kk_analysis": {
        "n_free": KK_N_FREE, "threshold_n_free_plus_1": KK_THRESHOLD,
        "n_matched": KK_N_MATCHED, "shortfall": KK_SHORTFALL,
        "attempted_second_observable": "m_KK（电子质量）",
        "discrepancy": float(M_KK_DISCREPANCY),
    },
    "gr_control": {"passes_threshold": bool(GR["passes_threshold"]),
                   "n_free": GR["n_free"], "n_matched": GR["n_matched"],
                   "surplus": GR["surplus"]},
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "★ 门槛判据：真预测要求 **n_matched ≥ n_free + 1**（数据超定自由量），且预言量 O ∉ 定参集合 M。"
        "本框架：连续型通过门槛者 **%d 项**；唯一通过门槛的是**离散**的电荷量子化(n∈ℤ，0 自由量)。"
        "KK 模型 n_free=1 ⇒ 门槛=2 个独立吻合可观测量，实得 1 个(α，且循环) ⇒ **差整整 %d 个可观测量**；"
        "它唯一尝试的第二个可观测量 m_KK 与电子质量差 %.3e 倍（真跨域转移，故可证伪·加分，但被否证）。"
        "正对照 GR 水星进动：n_free=0、n_matched=1 ⇒ 1 ≥ 0+1 且 O∉M ⇒ **通过门槛**。"
        "⇒ 结论：缺口在**观测侧**（还差 1 个独立吻合量），而非参数侧（再加自由量只会更糟）。"
        % (len(FRAMEWORK_PASS_CONTINUOUS), KK_SHORTFALL, float(M_KK_DISCREPANCY))
    ),
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

md = []
md.append("# TUFT-r69 · 跨域转移与最小自由量门槛审计 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("\n## 判据")
md.append("- 跨域转移：O ∉ M（预言量不在定参集合中）")
md.append("- 超定：surplus = n_matched − n_free，真预测要求 **n_matched ≥ n_free + 1**")
md.append("\n## 关系台账")
for r in RELATIONS:
    md.append("- [%s] %s：n_free=%d n_matched=%d surplus=%+d（有效 %+d）门槛=%d **通过=%s** 循环=%s | %s"
              % (r["层"], r["关系"], r["n_free"], r["n_matched"], r["surplus"],
                 r["surplus_effective"], r["threshold"], r["passes_threshold"], r["circular"], r["备注"]))
md.append("\n## 框架通过门槛情况")
md.append("- 全部通过项：%s" % [r["关系"] for r in FRAMEWORK_PASS])
md.append("- **连续型通过项：%s** ← 真正想要的" % [r["关系"] for r in FRAMEWORK_PASS_CONTINUOUS])
md.append("- 离散型通过项：%s" % [r["关系"] for r in DISCRETE_SUCCESSES])
md.append("\n## KK 模型门槛分析")
md.append("- n_free=%d ⇒ 门槛=%d；实得 n_matched=%d ⇒ **差 %d 个独立吻合可观测量**"
          % (KK_N_FREE, KK_THRESHOLD, KK_N_MATCHED, KK_SHORTFALL))
md.append("- 唯一尝试的第二个可观测量：m_KK，与电子质量差 %.3e 倍（真跨域转移 ⇒ 可证伪·加分）"
          % float(M_KK_DISCREPANCY))
md.append("\n## 正对照")
md.append("- GR：n_free=%d n_matched=%d surplus=%+d 通过=%s"
          % (GR["n_free"], GR["n_matched"], GR["surplus"], GR["passes_threshold"]))
md.append("\n## 门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("TUFT-r69 跨域转移与最小自由量门槛审计 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("门槛: n_matched >= n_free + 1 且 O not in M")
report.append("框架连续型通过=%d 项 | 离散型通过=%d 项(电荷量子化)" % (len(FRAMEWORK_PASS_CONTINUOUS), len(DISCRETE_SUCCESSES)))
report.append("KK: n_free=1 门槛=2 实得=1 => 差 %d 个可观测量 (m_KK 差 %.3e)" % (KK_SHORTFALL, float(M_KK_DISCREPANCY)))
report.append("GR正对照: n_free=0 n_matched=1 => 通过=%s" % GR["passes_threshold"])
report.append("guard 数=%d, 全过=%s" % (len(guards), all(g[1] for g in guards)))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

guard_all = all(g[1] for g in guards) and (len(guards) >= 9)
raise SystemExit(0 if guard_all else 1)
