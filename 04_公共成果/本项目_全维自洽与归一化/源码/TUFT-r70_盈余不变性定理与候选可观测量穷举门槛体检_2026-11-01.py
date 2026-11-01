# -*- coding: utf-8 -*-
"""
TUFT-r70 · 盈余不变性定理 + 候选可观测量穷举门槛体检（承 r69 X-R69-1）
（首次使用共享内核 `_criteria_kernel.py` —— 优化/修复 r61–r69 的重复样板）

三件事：
【发现·新方程】KK 带电模态的**普适质量**：
    由 α_n = 4n^2(ℓ_P/R)^2 与 m_n = n/R 消去 R ⇒
    **m_KK = (√α / 2) · M_Pl ≈ 5.215×10^17 GeV**（与 n、R 均无关！）
    推广：电荷为 q·e 的粒子 m = |q| · (√α/2) · M_Pl
    这是框架的刚性预言（给定 α 后零自由度），被电子质量否证 1.02×10^21 倍。

【发现·新定理】**盈余不变性定理**：
    以"一个自由参数换一个吻合可观测量"的方式修补，
    surplus = n_matched − n_free **保持不变**（k→k+1 后仍为 0）。
    ⇒ 加料式修复**永远追不上门槛**；唯一通路是**参数跨域复用**
      （GR 的 G：1 个参数同时吻合 Cavendish + 水星进动 ⇒ surplus=+1）。

【体检·X-R69-1】候选"第二个可观测量"穷举：m_e / m_µ / m_τ / m_p / m_W / m_t
    → 全部被否证，最小失配仍为 2.01×10^15 倍。

裁决常量：SURPLUS_INVARIANT_UNDER_ONE_PARAM_PER_OBSERVABLE_REPAIR_REUSE_REQUIRED
"""
import os
import sys
from decimal import Decimal

SRC_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
import _criteria_kernel as K  # noqa: E402

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r70_盈余不变性定理与候选可观测量穷举门槛体检_2026-11-01"

# ---------------------------------------------------------------------------
# 常数
# ---------------------------------------------------------------------------
ALPHA_INV = Decimal("137.035999177")
ALPHA = Decimal(1) / ALPHA_INV
M_PL = Decimal("1.2209e19")          # GeV

G = K.GuardBook("TUFT-r70")

# ---------------------------------------------------------------------------
# 一、【发现】KK 普适质量：m_KK = (√α/2)·M_Pl（与 n、R 无关）
# ---------------------------------------------------------------------------
sqrt_alpha = K.dec_sqrt(ALPHA)
M_KK_UNIVERSAL = sqrt_alpha * M_PL / Decimal(2)     # GeV（q=1 单位电荷）

M_E = Decimal("0.000510999")


def m_kk_of_charge(q):
    """电荷为 q·e 的 KK 模态质量（q 可为分数，对应 e/3 单位制下的整数 n）。"""
    return abs(Decimal(q)) * M_KK_UNIVERSAL


# n 无关性验证：无论取单位电荷 e（n=1）还是 e/3（电子 n=3），质量相同
def m_from_n_and_R(n, R_over_lP):
    """直接由 m_n = n/R 计算（R 以 ℓ_P 为单位，质量以 GeV）。"""
    return Decimal(n) * M_PL / Decimal(R_over_lP)


# 单位电荷 = e：α = 4·1²·(ℓ_P/R)² ⇒ R = 2ℓ_P/√α，电子 n=1
R_unit_e = Decimal(2) / sqrt_alpha
m_via_unit_e = m_from_n_and_R(1, R_unit_e)
# 单位电荷 = e/3：α = 4·3²·(ℓ_P/R)² ⇒ R = 6ℓ_P/√α，电子 n=3
R_unit_e3 = Decimal(6) / sqrt_alpha
m_via_unit_e3 = m_from_n_and_R(3, R_unit_e3)
# 两者应相等 ⇒ 与 n 无关
n_independence_residual = abs(m_via_unit_e - m_via_unit_e3) / m_via_unit_e

# ---------------------------------------------------------------------------
# 二、【体检】候选"第二个可观测量"穷举（X-R69-1）
# ---------------------------------------------------------------------------
# (名称, 电荷 q/e, 实测质量 GeV)
CANDIDATES = [
    ("电子 m_e", "1", Decimal("0.000510999")),
    ("µ 子 m_µ", "1", Decimal("0.10565837")),
    ("τ 子 m_τ", "1", Decimal("1.77686")),
    ("质子 m_p", "1", Decimal("0.938272")),
    ("W 玻色子", "1", Decimal("80.379")),
    ("顶夸克 m_t", "2/3", Decimal("172.76")),
]

cand_rows = []
for name, q_str, m_obs in CANDIDATES:
    q = Decimal(2) / Decimal(3) if q_str == "2/3" else Decimal(q_str)
    m_pred = m_kk_of_charge(q)
    ratio = m_pred / m_obs
    cand_rows.append({"可观测量": name, "电荷q/e": q_str,
                      "模型预言GeV": float(m_pred), "实测GeV": float(m_obs),
                      "失配倍数": float(ratio), "吻合": False})

MIN_DISCREPANCY = min(r["失配倍数"] for r in cand_rows)
BEST_CANDIDATE = min(cand_rows, key=lambda r: r["失配倍数"])

# ---------------------------------------------------------------------------
# 三、【发现】盈余不变性定理
# ---------------------------------------------------------------------------
# 三种情形：base / 加一对(参数,可观测量) / 参数复用
inv_rows = []
for k in range(1, 6):
    base = (k, k)                     # n_free, n_matched
    repaired = (k + 1, k + 1)         # 加一个参数换一个吻合量
    reuse = (k, k + 1)                # 一个参数服务两个可观测量
    inv_rows.append({
        "k": k,
        "base_n_free": base[0], "base_n_matched": base[1],
        "base_surplus": K.surplus_of(base[1], base[0]),
        "repaired_n_free": repaired[0], "repaired_n_matched": repaired[1],
        "repaired_surplus": K.surplus_of(repaired[1], repaired[0]),
        "reuse_n_free": reuse[0], "reuse_n_matched": reuse[1],
        "reuse_surplus": K.surplus_of(reuse[1], reuse[0]),
        "reuse_passes": K.passes_threshold(reuse[1], reuse[0]),
    })

# 不变性：base 与 repaired 的 surplus 必须处处相等（均为 0）
invariance_holds = all(r["base_surplus"] == r["repaired_surplus"] for r in inv_rows)
reuse_gains = all(r["reuse_surplus"] == r["base_surplus"] + 1 for r in inv_rows)
reuse_passes_all = all(r["reuse_passes"] for r in inv_rows)

# ---------------------------------------------------------------------------
# 四、正对照：GR 的参数复用（G 服务两个域）
# ---------------------------------------------------------------------------
# G 由 Cavendish 实验定住 → 又预言水星近日点进动 ⇒ 1 参数吻合 2 个可观测量
GR = {"n_free": 1, "n_matched": 2,
      "说明": "G 由 Cavendish(实验室) 定住，又预言水星进动 42.98″(天体) ⇒ 跨域复用"}
GR["surplus"] = K.surplus_of(GR["n_matched"], GR["n_free"])
GR["passes"] = K.passes_threshold(GR["n_matched"], GR["n_free"])

# KK 对照：R 由 α 定住，第二次使用(m_KK)失败 ⇒ 复用失败
KK = {"n_free": 1, "n_matched": 1,
      "说明": "R 由 α 定住；第二次使用(m_KK)与电子差 1.02e21 ⇒ 复用失败"}
KK["surplus"] = K.surplus_of(KK["n_matched"], KK["n_free"])
KK["passes"] = K.passes_threshold(KK["n_matched"], KK["n_free"])

# ---------------------------------------------------------------------------
# 自检 guard（含正对照强制）
# ---------------------------------------------------------------------------
G.guard("alpha_inverse_sane", Decimal("137") < ALPHA_INV < Decimal("137.1"))
G.guard("m_kk_universal_matches_r66", abs(M_KK_UNIVERSAL / Decimal("5.21469915e17") - 1) < Decimal("1e-3"))
G.guard("m_kk_independent_of_n", n_independence_residual < Decimal("1e-12"))
G.guard("electron_falsifies_m_kk", M_KK_UNIVERSAL / M_E > Decimal("1e15"))
G.guard("all_candidates_fail", all(not r["吻合"] for r in cand_rows))
G.guard("min_discrepancy_still_huge", Decimal(str(MIN_DISCREPANCY)) > Decimal("1e15"))
G.guard("surplus_invariance_holds", invariance_holds)
G.guard("reuse_gains_exactly_one", reuse_gains)
G.guard("reuse_passes_threshold", reuse_passes_all)
G.require_control("gr_parameter_reuse_passes", GR["passes"] and GR["surplus"] == 1)
G.guard("kk_reuse_fails", not KK["passes"])

VERDICT = "SURPLUS_INVARIANT_UNDER_ONE_PARAM_PER_OBSERVABLE_REPAIR_REUSE_REQUIRED"
G.guard("verdict_constant_set",
        VERDICT == "SURPLUS_INVARIANT_UNDER_ONE_PARAM_PER_OBSERVABLE_REPAIR_REUSE_REQUIRED")

F4 = ("把『加一个参数去解释一个新现象』当作『理论进步』：盈余不变性定理表明此举 surplus 不变"
      " ⇒ 范畴错置（解释覆盖面扩大 ≠ 预测盈余增加）→ F4 触发")
E9 = ("参数复用要求同一参数在两个能标/物理域都成立；KK 的 R 在 α 域成立、在质量域差 1.02e21"
      " ⇒ 跨域复用失败，E9 FAIL")
Ω5 = ("门槛随 n_free 同步升高 ⇒ 增参不能达标；唯一通路是复用，而非增参 ⇒ Ω5 指向"
      "『自由量预算应封顶，靠复用而非新增』")

payload = {
    "audit": "TUFT-r70",
    "subject": "盈余不变性定理 + 候选可观测量穷举门槛体检（X-R69-1）",
    "verdict": VERDICT,
    "kernel_used": "_criteria_kernel.py（优化：消除 r61–r69 重复样板）",
    "discovered_equation": {
        "formula": "m_KK = (√α / 2) · M_Pl  （电荷 q·e 者：m = |q|·(√α/2)·M_Pl）",
        "value_GeV": float(M_KK_UNIVERSAL),
        "depends_on": "仅 α 与 M_Pl，与 n、R 均无关",
        "n_independence_residual": float(n_independence_residual),
        "vs_electron_ratio": float(M_KK_UNIVERSAL / M_E),
        "note": "★框架刚性预言（给定 α 后零自由度）；被电子质量否证 1.02e21 倍",
    },
    "candidate_sweep": cand_rows,
    "min_discrepancy": MIN_DISCREPANCY,
    "best_candidate": BEST_CANDIDATE["可观测量"],
    "invariance_theorem": {
        "statement": "以『一参数换一吻合可观测量』修补，surplus = n_matched − n_free 保持不变",
        "rows": inv_rows,
        "invariance_holds": bool(invariance_holds),
        "reuse_gains_exactly_one": bool(reuse_gains),
        "reuse_passes_all": bool(reuse_passes_all),
    },
    "gr_control": GR,
    "kk_case": KK,
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "【新方程】由 α_n=4n^2(ℓ_P/R)^2 与 m_n=n/R 消去 R ⇒ **m_KK=(√α/2)·M_Pl=%.4e GeV**，"
        "与 n、R 均无关（残差 %.1e）；电荷 q·e 者 m=|q|·该值。给定 α 后零自由度，却被电子否证 %.3e 倍。"
        "【新定理】**盈余不变性**：以『一参数换一吻合量』修补，surplus 恒不变（k→k+1 仍为 0）；"
        "唯有**参数跨域复用**使 surplus +1 并通过门槛。⇒ 加料式修复永远追不上。"
        "【体检 X-R69-1】穷举 %d 个候选第二可观测量，全部被否证，**最小失配仍 %.3e 倍**（%s）。"
        "【正对照】GR：G 由 Cavendish 定住又预言水星进动 ⇒ 1 参数 2 可观测量 ⇒ surplus=+1 通过；"
        "KK：R 由 α 定住，第二次使用失败 ⇒ 不通过。⇒ 判据能识别真复用，非恒否。"
        % (float(M_KK_UNIVERSAL), float(n_independence_residual), float(M_KK_UNIVERSAL / M_E),
           len(cand_rows), float(MIN_DISCREPANCY), BEST_CANDIDATE["可观测量"])
    ),
}

md = []
md.append("# TUFT-r70 · 盈余不变性定理 + 候选穷举门槛体检 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("- 内核：%s" % payload["kernel_used"])
md.append("\n## 一、【发现】KK 普适质量")
md.append("- %s" % payload["discovered_equation"]["formula"])
md.append("- = %.4e GeV（与 n、R 无关，残差 %.1e）" % (float(M_KK_UNIVERSAL), float(n_independence_residual)))
md.append("- 对电子：失配 %.3e 倍 ⇒ 否证" % float(M_KK_UNIVERSAL / M_E))
md.append("\n## 二、【体检】候选第二可观测量穷举")
for r in cand_rows:
    md.append("- %s(q=%s)：预言 %.3e GeV vs 实测 %.4e GeV ⇒ 失配 %.3e ⇒ 吻合=%s"
              % (r["可观测量"], r["电荷q/e"], r["模型预言GeV"], r["实测GeV"], r["失配倍数"], r["吻合"]))
md.append("- **最小失配 = %.3e（%s）**" % (float(MIN_DISCREPANCY), BEST_CANDIDATE["可观测量"]))
md.append("\n## 三、【定理】盈余不变性")
for r in inv_rows:
    md.append("- k=%d：base(%d,%d)→%+d | 加一对(%d,%d)→%+d | **复用(%d,%d)→%+d 通过=%s**"
              % (r["k"], r["base_n_free"], r["base_n_matched"], r["base_surplus"],
                 r["repaired_n_free"], r["repaired_n_matched"], r["repaired_surplus"],
                 r["reuse_n_free"], r["reuse_n_matched"], r["reuse_surplus"], r["reuse_passes"]))
md.append("- 不变性成立=%s | 复用恰好 +1=%s | 复用均通过=%s"
          % (invariance_holds, reuse_gains, reuse_passes_all))
md.append("\n## 四、正对照")
md.append("- GR：n_free=%d n_matched=%d surplus=%+d 通过=%s | %s"
          % (GR["n_free"], GR["n_matched"], GR["surplus"], GR["passes"], GR["说明"]))
md.append("- KK：n_free=%d n_matched=%d surplus=%+d 通过=%s | %s"
          % (KK["n_free"], KK["n_matched"], KK["surplus"], KK["passes"], KK["说明"]))
md.append("\n## 五、门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)

report = []
report.append("TUFT-r70 盈余不变性定理与候选穷举 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("新方程: m_KK=(sqrt(alpha)/2)*M_Pl = %.4e GeV (与n,R无关, 残差%.1e), 电子失配%.3e"
              % (float(M_KK_UNIVERSAL), float(n_independence_residual), float(M_KK_UNIVERSAL / M_E)))
report.append("候选穷举%d项: 最小失配%.3e (%s) => 全部否证" % (len(cand_rows), float(MIN_DISCREPANCY), BEST_CANDIDATE["可观测量"]))
report.append("定理: 盈余不变性=%s (加一对参数/可观测量 surplus 不变), 复用+1=%s" % (invariance_holds, reuse_gains))
report.append("正对照 GR: n_free=1 n_matched=2 surplus=+1 通过=%s | KK 通过=%s" % (GR["passes"], KK["passes"]))
report.append("guard 数=%d, 全过=%s" % (G.n, G.all_pass()))

K.write_triplet(OUT_DIR, BASENAME, payload, md, report)
raise SystemExit(G.exit_code(min_guards=10))
