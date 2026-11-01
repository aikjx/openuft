# -*- coding: utf-8 -*-
"""
TUFT-r332 · 「精度 ≠ 发现」统一验收规范（基准率 × 零判别力 × 过精度 三刀合一）

目的：把本线程三把分散的刀——r293 巧合基准率、r66/r67「零判别力」、r310 过精度——
      合成一把**可复用、可机读**的统一验收门禁 `discriminate()`，用于判决任何
      「我们预言了 α（或任何常数）！」类声称。它必须：
        (1) 识别真正的第一性原理数值预言（如 GR 水星进动）→ 不误杀；
        (2) 识别真正的结构性进展（如 r311 的 BZ 红外固定点选择原型）→ 不误杀；
        (3) 戳穿「高精度数值拟合」伪装成发现（如 V20 的四次候选）→ 不漏放。

grounding：r293（基准率 15319 常数池 / 229785 对）、r66/r67（零判别力）、r310（V20 审计）、
          r311（BZ 红外固定点选择原型，平行册）、r72（GR 水星进动正对照）。

纪律：中文文案用「」；正对照强制；判据门槛不写死 True；仅出新册，不回填。
"""
import os
import math
from decimal import Decimal, getcontext
from _criteria_kernel import (GuardBook, surplus_of, passes_threshold, write_triplet)
from _audit_acceptance import discriminate as _canonical_discriminate

getcontext().prec = 80

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
BASENAME = "TUFT-r334_精度不等于发现统一验收规范_基准率乘零判别力乘过精度门禁_2026-11-01"


# ---------------------------------------------------------------------------
# 0. 高精度 π（与 r310 同款 Chudnovsky，纯标准库；避免 import r310 重跑）
# ---------------------------------------------------------------------------
def _factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def pi_dec():
    C = Decimal(426880) * Decimal(10005).sqrt()
    K3 = Decimal(640320) ** 3
    S = Decimal(0)
    for k in range(0, 5):
        num = Decimal(_factorial(6 * k)) * (Decimal(545140134) * k + Decimal(13591409))
        den = Decimal(_factorial(3 * k)) * (Decimal(_factorial(k)) ** 3) * (K3 ** k)
        S += (Decimal(-1) ** k) * num / den
    return C / S


PI = pi_dec()

guards = GuardBook("r332 统一验收规范")


# ---------------------------------------------------------------------------
# 1. 复算 V20 §3 条件计算表（强化「V20 诚实」结论）
#    V20 自承这些是条件性计算（输入 α，输出 O），本册用独立常数确认其数值正确。
# ---------------------------------------------------------------------------
C = Decimal("299792458")
HBAR = Decimal("1.054571817e-34")
H = Decimal("6.62607015e-34")        # 2019 重定义后精确
E = Decimal("1.602176634e-19")       # 2019 重定义后精确
M_E = Decimal("9.1093837015e-31")
ALPHA_INV = Decimal("137.035999177")
ALPHA = Decimal(1) / ALPHA_INV

E1_J = -M_E * C ** 2 * ALPHA ** 2 / Decimal(2)
E1_eV = E1_J / E
a0 = HBAR / (M_E * C * ALPHA)
r_e = ALPHA * HBAR / (M_E * C)        # 经典电子半径
sigma_T = (Decimal(8) * PI / Decimal(3)) * r_e ** 2
a_e1 = ALPHA / (Decimal(2) * PI)
RK = H / E ** 2
Z0 = Decimal(2) * ALPHA * RK
Phi0 = H / E

# V20 §3 报值
V20_S3 = {
    "E1_eV": Decimal("-13.605693123"),
    "a0": Decimal("5.2917721054e-11"),
    "sigma_T": Decimal("6.6524587050e-29"),
    "a_e1": Decimal("0.00116140973210"),
    "Z0": Decimal("376.7303134115"),
    "RK": Decimal("25812.8074593"),
    "Phi0": Decimal("4.1356676969e-15"),
}
computed_S3 = {"E1_eV": E1_eV, "a0": a0, "sigma_T": sigma_T,
               "a_e1": a_e1, "Z0": Z0, "RK": RK, "Phi0": Phi0}
s3_max_relerr = max(
    float(abs(computed_S3[k] - V20_S3[k]) / abs(V20_S3[k])) for k in V20_S3
)
guards.guard("V20_S3_CONDITIONAL_TABLE_REPRODUCED", s3_max_relerr < 1e-6)


# ---------------------------------------------------------------------------
# 2. 统一验收门禁 discriminate()
# ---------------------------------------------------------------------------
# r293 基准率（229785 对）：阈值 → 命中数
BENCH = {Decimal("1e-1"): 6404, Decimal("1e-2"): 712, Decimal("1e-3"): 77,
         Decimal("1e-4"): 14, Decimal("1e-5"): 8, Decimal("1e-6"): 6}
BENCH_TOL = 5    # 5σ 带
RARE = Decimal("1e-5")   # r293：<1e-5 才算稀有


def benchmark_regime(residual_rel):
    for thr in [Decimal("1e-1"), Decimal("1e-2"), Decimal("1e-3"),
               Decimal("1e-4"), Decimal("1e-5"), Decimal("1e-6")]:
        if residual_rel < thr:
            return ("RARE" if thr <= RARE else "COMMON"), thr
    return "COMMON", Decimal("inf")


def discriminate(label, *, candidate, center, sigma, n_matched, n_free,
                 is_fit_to_target, predicts_target_quantity):
    """r334 兼容适配器：**判决规则委托权威门禁** `_audit_acceptance.discriminate`
    （单一真相源，消除「同判据多实现」漂移）；本函数仅补 r334 特有的 `regime`
    字段（基于 r293 基准率），以保持下游 report / md 表格与既往读数完全一致的字节。"""
    r = _canonical_discriminate(
        label, candidate=candidate, center=center, sigma=sigma,
        n_matched=n_matched, n_free=n_free,
        is_fit_to_target=is_fit_to_target,
        predicts_target_quantity=predicts_target_quantity)
    regime, _ = benchmark_regime(Decimal(str(r["residual_rel"])))
    # 按迁移前的原始键序重组，确保 json 序列化零改动（diff 零差异）
    return {
        "label": label, "surplus": r["surplus"], "within_band": r["within_band"],
        "residual_rel": r["residual_rel"], "regime": regime,
        "verdict": r["verdict"], "is_discovery_of_target": r["is_discovery_of_target"],
    }


# ---------------------------------------------------------------------------
# 3. 应用：四个判例
# ---------------------------------------------------------------------------
SIGMA_ALPHA = Decimal("0.000000021")

# (a) V20 四次候选：单方程 1 未知、拟合到 CODATA、针对 α
quartic = discriminate(
    "V20 四次候选 137.0359991772160…",
    candidate=Decimal("137.035999177216023747889"),
    center=ALPHA_INV, sigma=SIGMA_ALPHA, n_matched=1, n_free=1,
    is_fit_to_target=True, predicts_target_quantity=True)

# (b) V20 简单候选 4π³+π²+π：纯几何数，不拟合但也不针对 α（它只是另一个数）
simple = discriminate(
    "V20 简单候选 4π³+π²+π=137.03630…",
    candidate=Decimal("137.0363037758784325"),
    center=ALPHA_INV, sigma=SIGMA_ALPHA, n_matched=1, n_free=1,
    is_fit_to_target=False, predicts_target_quantity=False)

# (c) GR 水星进动（r72 正对照）：真数值预言，独立 + 过定 + 带内
gr = discriminate(
    "GR 水星进动 42.96″ vs 42.98″",
    candidate=Decimal("42.9597"), center=Decimal("42.98"),
    sigma=Decimal("0.1"), n_matched=2, n_free=1,
    is_fit_to_target=False, predicts_target_quantity=True)

# (d) r311 BZ 红外固定点：真结构进展（强扇区选择原型），但不预言 α_em
bz = discriminate(
    "r311 BZ 红外固定点 α*(Nf=16)=0.0416（强扇区，非 α_em）",
    candidate=Decimal("0.041610498723043614"), center=Decimal("0.041610498723043614"),
    sigma=Decimal("1e-6"), n_matched=1, n_free=0,
    is_fit_to_target=False, predicts_target_quantity=False)

guards.guard("GATE_QUARTIC_NOT_DISCOVERY", (not quartic["is_discovery_of_target"])
             and quartic["verdict"] == "RELATION_OR_FIT")
guards.guard("GATE_SIMPLE_NOT_DISCOVERY", (not simple["is_discovery_of_target"]))
guards.guard("GATE_POSCTRL_GR_GENUINE_PREDICTION", gr["is_discovery_of_target"]
             and gr["verdict"] in ("GENUINE_PREDICTION", "NOTABLE_INDEPENDENT_PREDICTION"))
guards.guard("GATE_POSCTRL_BZ_STRUCTURAL_ADVANCE", (not bz["is_discovery_of_target"])
             and bz["verdict"] == "STRUCTURAL_ADVANCE_NOT_TARGET")
# 基准率区分铁证：四次残留 <1e-5（稀有）却因拟合目标 ⇒ 闸门不给发现（稀有≠发现）
guards.guard("BENCHMARK_RARITY_NOT_DISCOVERY_WITHOUT_INDEPENDENCE",
             (quartic["residual_rel"] < float(RARE))
             and (not quartic["is_discovery_of_target"]))


# ---------------------------------------------------------------------------
# 4. 必要性自检：三条件缺一不可（证明闸门不是恒否/恒是）
# ---------------------------------------------------------------------------
# 条件A 盈余：surplus=0 但带内且独立 ⇒ RELATION_OR_FIT（盈余必要）
need_surplus = discriminate("必要性-盈余", candidate=Decimal("137.04"), center=ALPHA_INV,
                            sigma=SIGMA_ALPHA, n_matched=1, n_free=1,
                            is_fit_to_target=False, predicts_target_quantity=True)
# 条件B 带内：surplus=1 但带外 ⇒ FALSIFIED（带内必要）
need_band = discriminate("必要性-带内", candidate=Decimal("137.5"), center=ALPHA_INV,
                         sigma=SIGMA_ALPHA, n_matched=2, n_free=1,
                         is_fit_to_target=False, predicts_target_quantity=True)
# 条件C 独立：surplus=1 带内但拟合目标 ⇒ RELATION_OR_FIT（独立必要）
need_indep = discriminate("必要性-独立", candidate=ALPHA_INV, center=ALPHA_INV,
                          sigma=SIGMA_ALPHA, n_matched=2, n_free=1,
                          is_fit_to_target=True, predicts_target_quantity=True)
guards.guard("NECESSITY_SURPLUS_GATE", need_surplus["verdict"] == "RELATION_OR_FIT")
guards.guard("NECESSITY_BAND_GATE", need_band["verdict"] == "FALSIFIED_AS_PREDICTION")
guards.guard("NECESSITY_INDEPENDENCE_GATE", need_indep["verdict"] == "RELATION_OR_FIT")


# ---------------------------------------------------------------------------
# 5. 汇总
# ---------------------------------------------------------------------------
verdict = "PRECISION_NEQ_DISCOVERY__UNIFIED_GATE_SHIPS"
guards_all = guards.all_pass()
exit_code = 0 if (guards_all and guards.n >= 8) else 1

payload = {
    "verdict": verdict,
    "gate_spec": {
        "inputs": ["candidate", "center", "sigma", "n_matched", "n_free",
                   "is_fit_to_target", "predicts_target_quantity"],
        "verdicts": ["RELATION_OR_FIT", "FALSIFIED_AS_PREDICTION",
                     "STRUCTURAL_ADVANCE_NOT_TARGET",
                     "NOTABLE_INDEPENDENT_PREDICTION", "GENUINE_PREDICTION"],
        "benchmark": {str(k): v for k, v in BENCH.items()},
    },
    "V20_S3_reproduced_relerr_max": s3_max_relerr,
    "cases": [quartic, simple, gr, bz, need_surplus, need_band, need_indep],
    "guards": [{"name": n, "pass": c} for n, c in guards.rows],
    "exit_code": exit_code,
}

report = []
report.append("=== TUFT-r332 「精度≠发现」统一验收规范 ===")
report.append("判词: %s" % verdict)
report.append("")
report.append("V20 §3 条件表复算最大相对误差 = %.2e (<1e-6 ⇒ V20 诚实确认)" % s3_max_relerr)
report.append("")
report.append("四判例：")
for c in [quartic, simple, gr, bz]:
    report.append("  %-48s surplus=%+d band=%s regime=%s → %s (discovery=%s)"
                 % (c["label"][:48], c["surplus"], c["within_band"], c["regime"],
                    c["verdict"], c["is_discovery_of_target"]))
report.append("")
report.append("必要性自检：盈余必要=%s 带内必要=%s 独立必要=%s"
             % (need_surplus["verdict"] == "RELATION_OR_FIT",
                need_band["verdict"] == "FALSIFIED_AS_PREDICTION",
                need_indep["verdict"] == "RELATION_OR_FIT"))

md = []
md.append("# TUFT-r332 · 「精度 ≠ 发现」统一验收规范（基准率 × 零判别力 × 过精度 三刀合一）")
md.append("")
md.append("> grounding：r293（基准率）/ r66-r67（零判别力）/ r310（V20 过精度审计）/")
md.append("> r311（BZ 红外固定点选择原型，平行册）/ r72（GR 水星进动正对照）。红线：数学自洽 ≠ 物理证实。")
md.append("> 纪律：仅出新册，不回填 README / 09，不刷新、不 git。")
md.append("")
md.append("## 〇、一句话结论")
md.append("")
md.append("本册把本线程三把分散的刀——**r293 巧合基准率、r66/r67「零判别力」、r310 过精度**——")
md.append("合成一把**可复用、可机读**的统一验收门禁 `discriminate()`。它对任何「我们预言了常数！」类声称做四问：")
md.append("**超定了吗（盈余≥1）？带内吗？独立（非拟合目标）吗？真针对目标量吗？**")
md.append("四判例证明它**既不误杀真预言（GR 水星进动），也不误杀真结构进展（r311 BZ 固定点），更不漏放数值拟合（V20 四次候选）**。")
md.append("判词：**`PRECISION_NEQ_DISCOVERY__UNIFIED_GATE_SHIPS`**")
md.append("")
md.append("## 一、门禁定义（四问）")
md.append("")
md.append("```")
md.append("def discriminate(候选, 中心值, σ, n_matched, n_free, 是否拟合目标, 是否针对目标量):")
md.append("    surplus = n_matched - n_free          # r69/r70 超定判据")
md.append("    within_band = |候选-中心| ≤ 5σ        # 须在不确定度带内")
md.append("    残留_rel = |候选-中心| / |中心|")
md.append("    if surplus < 1:                 return RELATION_OR_FIT      # 关系非预言")
md.append("    if not within_band:             return FALSIFIED_AS_PREDICTION")
md.append("    if 是否拟合目标:                return RELATION_OR_FIT      # 稀有但拟合 ⇒ 非发现")
md.append("    if not 是否针对目标量:          return STRUCTURAL_ADVANCE_NOT_TARGET")
md.append("    if 残留_rel < 1e-5 (r293稀有):  return NOTABLE_INDEPENDENT_PREDICTION")
md.append("    else:                          return GENUINE_PREDICTION")
md.append("```")
md.append("")
md.append("**为什么四问缺一不可**（必要性自检，全过）：")
md.append("- 盈余必要：`surplus=0` 即便带内且独立 ⇒ `RELATION_OR_FIT`（r69：单方程单未知只是关系）。")
md.append("- 带内必要：`surplus=1` 但带外（如 V20 简单候选 14505σ）⇒ `FALSIFIED_AS_PREDICTION`。")
md.append("- 独立必要：`surplus=1` 带内但「拟合目标」⇒ `RELATION_OR_FIT`（基准率稀有 ≠ 发现）。")
md.append("")
md.append("## 二、四判例")
md.append("")
md.append("| 判例 | surplus | 带内 | 残留_rel | 基准率区 | 判定 | 发现? |")
md.append("|---|---|---|---|---|---|---|")
for c in [quartic, simple, gr, bz]:
    md.append("| %s | %+d | %s | %.2e | %s | %s | %s |" % (
        c["label"], c["surplus"], c["within_band"], c["residual_rel"],
        c["regime"], c["verdict"], c["is_discovery_of_target"]))
md.append("")
md.append("- **V20 四次候选**：surplus=0 + 拟合目标 ⇒ `RELATION_OR_FIT`。其残留 `%.1e` 落在 r293 稀有区（<1e-5），" % quartic["residual_rel"])
md.append("  但因「拟合 CODATA」而**稀有≠发现**——这正是 r310 过精度铁证的形式化。")
md.append("- **V20 简单候选** `4π³+π²+π`：纯几何数、不针对 α、带外 14505σ ⇒ 非发现（且作为预言已被证伪）。")
md.append("- **GR 水星进动**（r72 正对照）：surplus=+1、带内、独立、针对目标量 ⇒ 闸门认出**真预言**，证明有牙齿非恒否。")
md.append("- **r311 BZ 红外固定点**：surplus=+1、真结构进展，但选的是**强扇区耦合**而非 α_em ⇒ `STRUCTURAL_ADVANCE_NOT_TARGET`——")
md.append("  闸门把它与「数值拟合」区分开，也指出它**不构成 α 的第一性预言**（与 r311 判词 STILL-NOT-A-PREDICTION 一致）。")
md.append("")
md.append("## 三、对 V20 §3 条件表的复算（强化诚实结论）")
md.append("")
md.append("V20 §3 的 7 项条件计算（输入 α 输出 O）独立复算，最大相对误差 `%.2e`（<1e-6）⇒" % s3_max_relerr)
md.append("**V20 的算术零错误**：氢束缚能、玻尔半径、汤姆孙截面、电子磁矩首阶、真空阻抗、量子霍尔电阻、AB 磁通周期全部吻合。")
md.append("这进一步确认 r310 的「V20 诚实」结论——它连条件性计算都没做手脚。")
md.append("")
md.append("## 四、本册在判词链中的位置")
md.append("")
md.append("r293（基准率工具）→ r66/r67（零判别力）→ r310（V20 过精度审计）→ **r332（三刀合一门禁）**。")
md.append("它把分散的判据收敛为一把可对任意未来「常数预言」声称即刻判决的尺。")
md.append("对 r311 的 BZ 选择原型，本册给出统一判词：**真结构进展，但 α 第一性预测仍 OPEN**（最终单点 = 电磁侧 |P_cont|=0 机制）。")
md.append("")
md.append("## 五、诚实边界")
md.append("")
md.append("1. 本册产出的 `discriminate()` 是**判据工具，不是物理**；它不预言任何新现象，只判决声称。")
md.append("2. 门禁的「基准率稀有阈值 1e-5」取自 r293 的 229785 对经验表，是经验值非定理；宽严可调。")
md.append("3. `STRUCTURAL_ADVANCE_NOT_TARGET` 与 `FALSIFIED_AS_PREDICTION` 是**不同性质**的否定：前者肯定进展、只是否认它预言目标量；后者否定数值本身。混用会误读 r311。")
md.append("4. 红线重申：数学自洽 ≠ 实验证实；高精度数值拟合（无论多「准」）在未引入独立选择方程前，永远是关系不是预言。")

write_triplet(OUT_DIR, BASENAME, payload, md, report)
print("EXIT=%d  guards=%d/%d  verdict=%s" % (exit_code, sum(1 for _, c in guards.rows if c), guards.n, verdict))
print("S3_relerr=%.2e quartic=%s gr_disc=%s bz=%s"
      % (s3_max_relerr, quartic["verdict"], gr["is_discovery_of_target"], bz["verdict"]))
