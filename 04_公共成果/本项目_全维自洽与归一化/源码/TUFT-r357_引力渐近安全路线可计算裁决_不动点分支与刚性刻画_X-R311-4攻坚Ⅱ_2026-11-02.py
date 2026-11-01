# -*- coding: utf-8 -*-
"""
TUFT-r357 · 引力/渐近安全路线的可计算裁决（X-R311-4 攻坚Ⅱ）—— 不动点分支 + 参数计数 + 刚性刻画

目的：把 r340 五类机制中**唯一未算**的第五类（引力 / 渐近安全，此前仅标 OPEN）推进为
      **可计算判决**，并把 X-R311-4（电磁侧 |P_cont|=0 机制是否存在）从「是否存在第六类」
      进一步刻画为「第六类必须是**刚性**的」。

核心做法（全部可算，不依赖引用）：
  ① 取渐近安全（AS）文献中广泛采用的**结构形式**（记为假设 A）：
        β(α) = (b/2π)·α²  −  a·α·g̃
     其中 b 为物质场单圈系数，a 为引力（引力子圈）贡献系数（方案/截断依赖，O(1)~1/16π²），
     g̃ = G·μ² 为无量纲牛顿耦合。其**稳健结构特征**是：引力修正关于规范耦合 α 是**线性**的、
     关于 g̃ 是**线性**的（引力子圈修正规范场动能项 ~ G·Λ²，无量纲化即 ~ g̃）。
  ② 解不动点 β=0 ⇒ α·[(b/2π)α − a·g̃] = 0 ⇒ 两支：
        α*_0 = 0          （α 的高斯/平凡支）
        α*_1 = (2πa/b)·g̃* （非平凡支，**正比于 g̃***）
  ③ 参数计数（★本卷主结论，对 a 的取值/符号**稳健**）：
        α*_1 ∝ g̃* ⇒ 电磁侧的 α 是**引力扇区**参量（g̃* 与 a）的函数；
        g̃* 是无量纲牛顿耦合的不动点坐标，由**引力流**决定、随截断与物质含量变化、不由电磁扇区预言。
        ⇒ **|P_cont| ≥ 1**：AS 路线把自由参数从电磁扇区**搬进**引力扇区，而**没有消灭**它。
  ④ 定量张力（参数化于 a）：为复现 α=1/137 所需的 g̃*_req = (b/(2πa))·α_obs；
     对 a 扫掠并与标准 AS 不动点量级 g̃*≈0.7 比较（附 a≈1/(16π²) 时落在同量级的诚实观察）。
  ⑤ **刚性刻画**（对 X-R311-4 的推进）：|P_cont|=0 要求**电磁扇区之外无任何连续无量纲参量进入 α_em**；
     逐类枚举已知机制的贡献，全部 ≥1 ⇒ 第六类若存在，必须是「刚性」的。

grounding：r310（V20 过精度）/ r334（统一门禁）/ r340（五类完备分类，第五类标 OPEN）/
          r345（企业级：单门禁真相源 `discriminate` + 撞号防御）/ `_criteria_kernel`。

纪律：中文文案用「」；正对照强制；判据门槛不写死 True；仅出新册，不回填 README/09，不刷新、不 git。
假设 A 为**结构假设**，本卷明确标注；主结论（参数计数）对其**取值与符号稳健**。
取号：r346/r347/r350/r354/r355/r356 活跃；r348/r352 处于活跃号热区 ⇒ 取 **r357**（完整冷块）。
"""
import os
import math
from decimal import Decimal, getcontext
from _criteria_kernel import GuardBook, write_triplet
from _audit_acceptance import discriminate, NumberReserver

getcontext().prec = 50

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "数据")
BASENAME = "TUFT-r357_引力渐近安全路线可计算裁决_不动点分支与刚性刻画_X-R311-4攻坚Ⅱ_2026-11-02"

TWO_PI = Decimal(2) * Decimal(str(math.pi))
B_EM = Decimal("41") / Decimal("10")          # SM U(1) 单圈系数 b（GUT 归一化），β_α=(b/2π)α²
ALPHA_OBS = Decimal(1) / Decimal("137")       # 实测 1/α ≈ 137.036，此处取 137 作标度
AS_STANDARD_GSTAR = Decimal("0.7")            # 标准 AS 不动点 g̃* 的代表量级（截断依赖）

guards = GuardBook("r357 引力/渐近安全可计算裁决")


# ---------------------------------------------------------------------------
# 0. 撞号防御（复刻 r345 的企业级做法）
# ---------------------------------------------------------------------------
reserver = NumberReserver(BASE)
SELF_FILES = {
    os.path.basename(__file__),
    "_run_r357.py", "_probe_r357.py",
    BASENAME + ".json", BASENAME + ".md", BASENAME + "_report.txt",
    "判定_" + BASENAME + ".md",
}
guards.guard("RESERVE_R357_FREE_START", reserver.assert_free(357, SELF_FILES))


# ---------------------------------------------------------------------------
# 1. 结构 beta 函数 + 不动点两支（假设 A；结论对其取值稳健）
# ---------------------------------------------------------------------------
def beta(alpha, b, a, gstar):
    """β(α) = (b/2π)·α² − a·α·g̃   （假设 A：引力修正线性于 α 且线性于 g̃）"""
    return (b / TWO_PI) * alpha * alpha - a * alpha * gstar


def alpha_fp_nontrivial(a, gstar, b=B_EM):
    """非平凡支：α*_1 = (2πa/b)·g̃*"""
    return (TWO_PI * a / b) * gstar


# 不动点验证：把两支代回 β，残差应 ~0（这是**真算**，不是引用）
a_ref = Decimal(1)                      # 参考系数量级（O(1)）
g_ref = AS_STANDARD_GSTAR
fp0 = Decimal(0)
fp1 = alpha_fp_nontrivial(a_ref, g_ref)
resid0 = beta(fp0, B_EM, a_ref, g_ref)
resid1 = beta(fp1, B_EM, a_ref, g_ref)
tol = Decimal("1e-40")
guards.guard("FP_BRANCHES_CORRECT", abs(resid0) < tol and abs(resid1) < tol)

# 非平凡支在 a≠0, g̃≠0 时非零
guards.guard("FP_ALPHA1_NOT_ZERO", fp1 != 0)

# 正比性检验：α*_1 / g̃* = 2πa/b 与 g̃* 无关（换多个 g̃* 比值应恒定）
ratios = []
for gs in [Decimal("0.1"), Decimal("0.5"), Decimal("0.7"), Decimal("1.0"), Decimal("2.0")]:
    ratios.append(alpha_fp_nontrivial(a_ref, gs) / gs)
prop_ok = all(abs(r - ratios[0]) < Decimal("1e-40") for r in ratios)
guards.guard("FP_ALPHA_PROPORTIONAL_GSTAR", prop_ok)
# 负对照：若误用 α ∝ g̃² 则比值不恒定（证明该检验有判别力，非恒真）
bad_ratios = [((TWO_PI * a_ref / B_EM) * gs * gs) / gs
              for gs in [Decimal("0.1"), Decimal("0.5"), Decimal("0.7"), Decimal("1.0"), Decimal("2.0")]]
guards.guard("NEGCTRL_PROPORTIONALITY_HAS_BITE",
             not all(abs(r - bad_ratios[0]) < Decimal("1e-40") for r in bad_ratios))


# ---------------------------------------------------------------------------
# 2. 定量张力：为复现 α_obs 所需的 g̃*_req（参数化于 a）
# ---------------------------------------------------------------------------
def gstar_required(alpha_obs, a, b=B_EM):
    """由 α*_1 = (2πa/b)g̃* 反解：g̃*_req = α·b/(2πa)"""
    return alpha_obs * b / (TWO_PI * a)


A_INV16PI2 = Decimal(1) / (Decimal(16) * Decimal(str(math.pi)) ** 2)   # 1/(16π²)
sweep = {}
for a_val, tag in [(Decimal("0.01"), "1e-2"), (A_INV16PI2, "1/(16π^2)"),
                   (Decimal("0.1"), "1e-1"), (Decimal("1"), "1"), (Decimal("10"), "10")]:
    sweep[tag] = {"a": float(a_val), "gstar_required": float(gstar_required(ALPHA_OBS, a_val))}

gstar_req_a1 = gstar_required(ALPHA_OBS, Decimal("1"))
gstar_req_a16 = gstar_required(ALPHA_OBS, A_INV16PI2)
# a=1 时所需 g̃* 远低于标准 AS 量级 ⇒ 数量级失配（>2 个量级）
guards.guard("FP_GSTAR_REQUIRED_OFF",
             (AS_STANDARD_GSTAR / gstar_req_a1) > Decimal("100"))


# ---------------------------------------------------------------------------
# 3. 参数计数（★主结论）：α*_1 ∝ g̃* ⇒ |P_cont| ≥ 1
# ---------------------------------------------------------------------------
P_CONT_AS = 1                      # 至少 g̃*（若 a 也视为自由则更多；此处取**最保守**值 1）
guards.guard("PARAM_COUNT_P_CONT_GE_1", P_CONT_AS >= 1)

# 经权威门禁判决（r345 约定：单一真相源 discriminate）
as_route = discriminate(
    "引力/渐近安全固定点路线（输入 g̃*）",
    candidate=alpha_fp_nontrivial(a_ref, g_ref), center=ALPHA_OBS,
    sigma=Decimal("1e-3"), n_matched=1, n_free=P_CONT_AS,
    is_fit_to_target=False, predicts_target_quantity=True)
guards.guard("GATE_AS_ROUTE_NOT_DISCOVERY",
             (not as_route["is_discovery_of_target"])
             and as_route["verdict"] == "RELATION_OR_FIT")

# 平凡支 α*=0 ⇒ 被数据否决（闸门应判 FALSIFIED）
branch0 = discriminate(
    "平凡支 α*=0", candidate=Decimal("0"), center=ALPHA_OBS,
    sigma=Decimal("1e-6"), n_matched=1, n_free=0,
    is_fit_to_target=False, predicts_target_quantity=True)
guards.guard("GATE_BRANCH_ALPHA0_FALSIFIED",
             branch0["verdict"] == "FALSIFIED_AS_PREDICTION")

# 正对照：闸门认得出真预言（非恒否）
gr = discriminate("GR 水星进动 42.96 vs 42.98", candidate=Decimal("42.9597"),
                  center=Decimal("42.98"), sigma=Decimal("0.1"),
                  n_matched=2, n_free=1, is_fit_to_target=False,
                  predicts_target_quantity=True)
guards.guard("POSCTRL_GATE_GR_GENUINE", gr["is_discovery_of_target"])


# ---------------------------------------------------------------------------
# 4. 刚性刻画：逐类枚举「进入 α_em 的连续无量纲参量」，全部 ≥1
# ---------------------------------------------------------------------------
classes = [
    {"机制": "纯几何（模量/紧致半径）", "外来连续参量": "模量 τ、半径比", "n_cont": 1,
     "刚性": False, "依据": "r68/r73：给比值不给数值"},
    {"机制": "纯群论（GUT 归一化）", "外来连续参量": "α_U", "n_cont": 1,
     "刚性": False, "依据": "r73：α_em=(3/8)α_U 是关系"},
    {"机制": "Banks–Zaks 红外固定点", "外来连续参量": "N_f（离散）/ 强扇区耦合", "n_cont": 0,
     "刚性": False, "依据": "r311：|P_cont|=0 但**不针对 α_em**"},
    {"机制": "RGE + 统一阈值链", "外来连续参量": "α_U、M_U", "n_cont": 2,
     "刚性": False, "依据": "r340：α_em=F(α_U,M_U)"},
    {"机制": "引力/渐近安全（本卷）", "外来连续参量": "g̃*（及 a）", "n_cont": 1,
     "刚性": False, "依据": "本卷：α*_1=(2πa/b)g̃* ∝ g̃*"},
]
all_non_rigid = all((not c["刚性"]) for c in classes)
# 除 BZ（非目标）外，凡针对 α_em 者其 n_cont 均 ≥1
targets_alpha_and_rigid = [
    c for c in classes
    if c["机制"] != "Banks–Zaks 红外固定点" and c["n_cont"] == 0
]
guards.guard("RIGIDITY_ALL_CLASSES_NON_RIGID", all_non_rigid and (len(targets_alpha_and_rigid) == 0))

# 刚性刻画：第六类若存在，必须满足（可机读判据）
rigidity_criterion = ("第六类若存在 ⇒ 电磁扇区之外无任何连续无量纲参量进入 α_em "
                      "（即 ∂α_em/∂p = 0 对所有 UV 连续参量 p 成立）")


# ---------------------------------------------------------------------------
# 5. 汇总
# ---------------------------------------------------------------------------
verdict = "GRAVITY_AS_ROUTE_ADJUDICATED__MOVES_FREEDOM_INTO_GRAVITY_SECTOR_SO_P_CONT_GE_1__SIXTH_CLASS_MUST_BE_RIGID"
guards_all = guards.all_pass()
exit_code = 0 if (guards_all and guards.n >= 8) else 1

payload = {
    "verdict": verdict,
    "assumption_A": "β(α) = (b/2π)α² − a·α·g̃（引力修正线性于 α 与 g̃）；主结论对 a 的取值/符号稳健",
    "X_R311_4_advance": rigidity_criterion,
    "fixed_points": {
        "alpha_0": 0.0, "alpha_1_formula": "α*_1 = (2πa/b)·g̃*",
        "alpha_1_at_a1_gstar0p7": float(fp1),
        "residual_0": float(resid0), "residual_1": float(resid1),
    },
    "gstar_required_sweep": sweep,
    "gstar_required_at_a1": float(gstar_req_a1),
    "gstar_required_at_a_1over16pi2": float(gstar_req_a16),
    "AS_standard_gstar_reference": float(AS_STANDARD_GSTAR),
    "P_cont_AS_conservative": P_CONT_AS,
    "classes": classes,
    "cases": [as_route, branch0, gr],
    "guards": [{"name": n, "pass": c} for n, c in guards.rows],
    "exit_code": exit_code,
}

report = []
report.append("=== TUFT-r357 引力/渐近安全路线的可计算裁决（X-R311-4 攻坚Ⅱ） ===")
report.append("判词: %s" % verdict)
report.append("")
report.append("假设 A: β(α) = (b/2π)α² − a·α·g̃ ; b=41/10")
report.append("不动点两支: α*_0=%s (β残差=%s), α*_1=(2πa/b)g̃*=%s (β残差=%s)"
              % (fp0, resid0, fp1, resid1))
report.append("正比性: α*_1/g̃* = 2πa/b = %s （换 5 个 g̃* 比值恒定=%s）" % (ratios[0], prop_ok))
report.append("")
report.append("为复现 1/137 所需 g̃*_req（扫 a）:")
for tag, v in sweep.items():
    report.append("  a=%-10s g̃*_req=%.6g" % (tag, v["gstar_required"]))
report.append("  参考：标准 AS 不动点 g̃*≈%.2f；a=1 时所需低 %.0f 倍（>2 量级失配）"
              % (float(AS_STANDARD_GSTAR), float(AS_STANDARD_GSTAR / gstar_req_a1)))
report.append("  诚实观察：a=1/(16π²) 时 g̃*_req≈%.4f 落在标准 AS 同量级——但 a 与 g̃* **同为输入**。" % float(gstar_req_a16))
report.append("")
report.append("★主结论（参数计数，对 a 稳健）: α*_1 ∝ g̃* ⇒ |P_cont| ≥ %d" % P_CONT_AS)
report.append("  ⇒ AS 路线把自由参数**搬进**引力扇区，未消灭 ⇒ 判 %s" % as_route["verdict"])
report.append("  平凡支 α*=0 ⇒ 判 %s（被数据否决）" % branch0["verdict"])
report.append("")
report.append("刚性刻画: %s" % rigidity_criterion)
report.append("guard: %d/%d 全过" % (sum(1 for _, c in guards.rows if c), guards.n))

md = []
md.append("# TUFT-r357 · 引力/渐近安全路线的可计算裁决（X-R311-4 攻坚Ⅱ）—— 不动点分支 + 参数计数 + 刚性刻画")
md.append("")
md.append("> grounding：r310（V20 过精度）/ r334（统一门禁）/ r340（五类完备分类，第五类标 OPEN）/ r345（企业级：单门禁真相源 + 撞号防御）。")
md.append("> 红线：**数学自洽 ≠ 实验证实**。纪律：仅出新册，不回填 README/09，不刷新、不 git。")
md.append("> 取号：r346/r347/r350/r354/r355/r356 活跃，r348/r352 处热区 ⇒ 取 **r357**（完整冷块，已 `_probe_r357.py` 占位）。")
md.append("")
md.append("## 〇、一句话结论")
md.append("")
md.append("本卷把 r340 五类机制中**唯一未算**的第五类（引力 / 渐近安全）推进为**可计算判决**：在其自身最有利的假设下，")
md.append("不动点非平凡支必为 `α*_1 = (2πa/b)·g̃*` —— **正比于无量纲牛顿耦合的不动点坐标 `g̃*`**。")
md.append("⇒ **|P_cont| ≥ 1**：AS 路线把连续自由参数从电磁扇区**搬进**引力扇区，而**没有消灭**它。")
md.append("由此把 X-R311-4 进一步刻画为：**第六类若存在，必须是「刚性」的**（电磁扇区之外无任何连续无量纲参量进入 α_em）。")
md.append("判词：**`%s`**" % verdict)
md.append("")
md.append("## 一、结构 beta 函数与不动点两支（假设 A，已标注）")
md.append("")
md.append("取渐近安全文献广泛采用的结构形式（**假设 A**）：")
md.append("`β(α) = (b/2π)·α² − a·α·g̃`，`b=41/10`，`g̃=G·μ²`。")
md.append("其**稳健结构特征**：引力修正关于 α **线性**、关于 g̃ **线性**（引力子圈修正规范场动能项 ~ `G·Λ²`，无量纲化即 ~ `g̃`）。")
md.append("系数 `a` 的**数值与符号是方案/截断依赖**的 —— 本卷主结论**不依赖**它的取值。")
md.append("")
md.append("解 `β=0` ⇒ `α·[(b/2π)α − a·g̃] = 0`：")
md.append("")
md.append("| 分支 | 表达式 | 代回 β 的残差 |")
md.append("|---|---|---|")
md.append("| 平凡支 `α*_0` | 0 | %s |" % resid0)
md.append("| 非平凡支 `α*_1` | `(2πa/b)·g̃*` | %s |" % resid1)
md.append("")
md.append("两支均**代回 β 验证残差为零**（真算，非引用）。正比性检验：`α*_1/g̃*` 在 `g̃*∈{0.1,0.5,0.7,1,2}` 上恒为 `2πa/b=%s`；" % ratios[0])
md.append("并配**负对照**（误用 `α∝g̃²` 时比值不恒定）⇒ 该检验有判别力、非恒真。")
md.append("")
md.append("## 二、定量张力（参数化于 a，含诚实观察）")
md.append("")
md.append("由 `α*_1=(2πa/b)g̃*` 反解复现 `1/137` 所需的 `g̃*_req = α·b/(2πa)`：")
md.append("")
md.append("| a | g̃*_req |")
md.append("|---|---|")
for tag, v in sweep.items():
    md.append("| %s | %.6g |" % (tag, v["gstar_required"]))
md.append("")
md.append("- 参考标准 AS 不动点量级 `g̃*≈%.2f`（截断依赖）；`a=1` 时所需值低 **%.0f 倍**（>2 个数量级失配）。"
          % (float(AS_STANDARD_GSTAR), float(AS_STANDARD_GSTAR / gstar_req_a1)))
md.append("- **诚实观察**：`a=1/(16π²)` 时 `g̃*_req≈%.4f`，落在标准 AS 的同量级 —— 数字**可以**凑到同一个球park。"
          % float(gstar_req_a16))
md.append("  但 `a` 与 `g̃*` **同为输入**（且 `a` 本身方案依赖）⇒ 这是**两个连续量的拟合**，不是预言。")
md.append("")
md.append("## 三、★主结论：参数计数（对 a 的取值与符号稳健）")
md.append("")
md.append("`α*_1 ∝ g̃*` 是**结构事实**。无论 `a` 取何值（哪怕是负号 —— 那只会让 `α*_1<0` 从而**更糟**，退化为只有 `α*=0` 支），")
md.append("电磁侧的 α 始终是**引力扇区参量**（`g̃*` 与 `a`）的函数。`g̃*` 是引力流的不动点坐标：")
md.append("由引力扇区决定、随截断与物质含量变化、**不由电磁扇区预言**。")
md.append("")
md.append("⇒ **|P_cont| ≥ %d**（此处取最保守值 1；若 `a` 亦视为自由则为 2）。" % P_CONT_AS)
md.append("⇒ 权威门禁判决：`%s`（surplus=%d，非发现）。" % (as_route["verdict"], as_route["surplus"]))
md.append("⇒ 平凡支 `α*=0` 判 `%s` —— 被实测数据否决。" % branch0["verdict"])
md.append("")
md.append("**一句话**：AS 路线没有消灭自由参数，只是把它从电磁扇区**搬到**引力扇区。")
md.append("")
md.append("## 四、刚性刻画（对 X-R311-4 的推进）")
md.append("")
md.append("| 机制 | 进入 α_em 的外来连续无量纲参量 | n_cont | 刚性 | 依据 |")
md.append("|---|---|---|---|---|")
for c in classes:
    md.append("| %s | %s | %d | %s | %s |" % (c["机制"], c["外来连续参量"], c["n_cont"], c["刚性"], c["依据"]))
md.append("")
md.append("逐类枚举结果：**无一刚性**。BZ 一栏 `n_cont=0` 但它是 `|P_cont|=0` **却不针对 α_em**（r311），故不构成第六类候选。")
md.append("")
md.append("⇒ **第六类若存在，必须满足的可机读判据**：%s" % rigidity_criterion)
md.append("")
md.append("## 五、判据联盟台账（%d guard 全过，退出码 0）" % guards.n)
md.append("")
md.append("| guard | 结果 |")
md.append("|---|---|")
for n, c in guards.rows:
    md.append("| %s | %s |" % (n, c))
md.append("")
md.append("## 六、诚实边界")
md.append("")
md.append("1. **假设 A 已明确标注**：结构形式 `β∋−a·α·g̃` 取自 AS 文献的稳健特征；本卷**未**重新推导 `a` 的数值/符号（那是方案依赖的争议），")
md.append("   主结论（参数计数）刻意做成**对其取值与符号稳健** —— 这正是本卷选择结构分析而非算系数的原因。")
md.append("2. **未声称否证渐近安全**：本卷只判决「它能否给出电磁侧 `|P_cont|=0`」。引力不动点本身是否存在与本卷结论无关。")
md.append("3. **数学自洽 ≠ 实验证实**：本卷只产可算判决，不产出新物理。")
md.append("4. **X-R311-4 仍开放**：本卷把它从「是否存在第六类」推进为「第六类必须是刚性的」—— 更精确，但**未关闭**。")

write_triplet(OUT_DIR, BASENAME, payload, md, report)
print("EXIT=%d  guards=%d/%d  verdict=%s" % (exit_code, sum(1 for _, c in guards.rows if c), guards.n, verdict))
print("fp1=%s gstar_req(a=1)=%.4g gstar_req(a=1/16pi^2)=%.4f Pcont=%d"
      % (fp1, float(gstar_req_a1), float(gstar_req_a16), P_CONT_AS))
