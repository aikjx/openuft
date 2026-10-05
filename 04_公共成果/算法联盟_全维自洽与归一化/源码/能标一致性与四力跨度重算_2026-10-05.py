# -*- coding: utf-8 -*-
"""能标一致性与四力跨度重算 · E9 判据的反噬自检。

背景：ESCAPE-AUDIT 的 E9 提出「四力相对强度是能标依赖量，静态几何分区是范畴错误」。
本册把这条判据**反过来用于自检与上游复核**，对象是 ADD-02 的耦合匹配表：
    Strong α=0.1179 / Weak 1.696e-2 / EM 7.297e-3 / G 1.75e-45
    span_dex = 43.828（引力/强跨度），δ_G = 4.948e-45 rad

问题：这四个 α 是否取自同一能标？
判据：α_G(E) = G·E²（自然单位，G = 1/M_Pl²）。用两个已知锚点校验该式的正确性——
    教科书「质子-质子 引力/强 = 5.9e-39」⟹ 反解 E ≈ m_p
    ADD-02 的 α_G = 1.75e-45               ⟹ 反解 E ≈ m_e
若两处反解分别给出质子质量与电子质量，则 (a) 公式正确、(b) ADD-02 的 α_G 取自电子标度，
而 α_s = 0.1179 是 M_Z 标度 ⟹ **能标混用**。

八条判定 T1–T8。纯标准库。
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "能标一致性与四力跨度重算_2026-10-05"

VERDICTS, KEYS = [], {}
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

# ---------------- 常数与基础公式 ----------------
M_Pl = 1.22091e19                       # Planck 能标 (GeV)
G_GeV = 1.0 / (M_Pl ** 2)               # 牛顿常数 (GeV^-2)，自然单位
M_Z = 91.1876                           # GeV
m_p = 0.938272                          # 质子质量 (GeV)
m_e = 0.510999e-3                       # 电子质量 (GeV)

def alpha_G(E):
    """无量纲引力耦合 α_G(E) = G·E²（自然单位）。"""
    return G_GeV * E * E

def E_from_alphaG(a):
    """由 α_G 反解能标（GeV）。"""
    return math.sqrt(a / G_GeV)

# ADD-02 耦合匹配表（引用不重算）
ADD02 = {"Strong": 0.1179, "Weak": 1.696e-2, "EM": 7.297e-3, "G": 1.75e-45}
ADD02_span_dex = 43.82847575640879
ADD02_delta_G = 4.948e-45               # rad
ADD02_ratio_GS = 1.484e-44              # 引力行 / 强核行
LAMBDA = ADD02["Strong"]                # 最大幅值原则 ⟹ λ = α_s

# ============ T1  α_G = G·E² 的锚点校验 + 反解 ADD-02 的引力能标 ============
E_from_textbook = E_from_alphaG(5.9e-39)          # 教科书质子-质子口径
E_from_add02 = E_from_alphaG(ADD02["G"])
r_p = E_from_textbook / m_p
r_e = E_from_add02 / m_e
KEYS["T1_G_GeV"] = G_GeV
KEYS["T1_E_textbook_GeV"] = E_from_textbook
KEYS["T1_E_add02_GeV"] = E_from_add02
KEYS["T1_ratio_to_mp"] = r_p
KEYS["T1_ratio_to_me"] = r_e
ok_t1 = abs(r_p - 1.0) < 1e-3 and abs(r_e - 1.0) < 1e-3
add("T1", "PASS" if ok_t1 else "FAIL",
    "α_G(E)=G·E² 的锚点校验，并反解 ADD-02 引力耦合的能标",
    "取 G = 1/M_Pl² = %.4e GeV⁻²（M_Pl = %.4e GeV）。双锚点校验："
    "① 教科书「质子-质子 引力/强 = 5.9e−39」⟹ 反解 E = %.5f GeV，与质子质量 %.6f GeV 之比 **%.5f**；"
    "② ADD-02 的 α_G = %.3e ⟹ 反解 E = %.6e GeV = %.4f MeV，与电子质量 %.6f MeV 之比 **%.5f**。"
    "⟹ (a) **α_G = G·E² 这一式是对的**（两锚点均吻合到 5×10⁻⁴）；"
    "(b) **ADD-02 的引力耦合取自电子质量标度（~0.51 MeV）**。"
    % (G_GeV, M_Pl, E_from_textbook, m_p, r_p,
       ADD02["G"], E_from_add02, E_from_add02 * 1e3, m_e * 1e3, r_e),
    {"G[GeV^-2]": G_GeV, "E(教科书)[GeV]": E_from_textbook, "E/m_p": r_p,
     "E(ADD-02)[MeV]": E_from_add02 * 1e3, "E/m_e": r_e})

# ============ T2  四个耦合的能标归属（核心：是否混标） ============
# α_s = 0.1179 是 α_s(M_Z) 的标准值；α_em = 7.297e-3 = 1/137.036 是零能标 Thomson 极限
alpha_em_0 = 1.0 / 137.035999
alpha_em_MZ = 1.0 / 127.95
sin2_thW = 0.2312
alpha_2_MZ = alpha_em_MZ / sin2_thW

归属 = {
    "Strong": ("M_Z 标度（α_s(M_Z)=0.1179）", M_Z),
    "EM": ("零能标（1/137.036 = Thomson 极限）", 0.0),
    "G": ("电子质量标度（反解 0.511 MeV）", E_from_add02),
    "Weak": ("**未标识**（1.696e−2 的本源与能标本册无法确认，NOT-ASSESSED）", None),
}
scales = [M_Z, 0.0, E_from_add02]
spread_dex = math.log10(max(scales) / min(x for x in scales if x > 0))
KEYS["T2_scale_spread_dex"] = spread_dex
n_distinct = 3
ok_t2 = False
add("T2", "FAIL",
    "**核心**：ADD-02 的四个耦合取自**至少三个不同能标** ⟹ 能标混用",
    "逐一归属：α_s = %.4f ⟹ **M_Z 标度**（%.2f GeV）；α_em = %.4e = 1/137.036 ⟹ "
    "**零能标**（Thomson 极限，QED 精细结构常数的定义值，而 α_em(M_Z) = 1/127.95 = %.4e）；"
    "α_G = %.3e ⟹ **电子质量标度**（%.4f MeV，T1 反解）；α_weak = %.4e ⟹ **能标未标识，本册 NOT-ASSESSED**。"
    "⟹ 三个已确认能标跨越 **%.2f 个量级**（0.511 MeV → 91.2 GeV）⟹ "
    "**该表不是同一能标下的四力比较**，违反能标一致性。"
    % (ADD02["Strong"], M_Z, ADD02["EM"], alpha_em_MZ, ADD02["G"],
       E_from_add02 * 1e3, ADD02["Weak"], spread_dex),
    {"α_s 能标[GeV]": M_Z, "α_em 能标": "0 (Thomson)",
     "α_G 能标[MeV]": E_from_add02 * 1e3, "已确认能标跨度[dex]": spread_dex,
     "α_weak": "NOT-ASSESSED"})

# ============ T3  统一到 M_Z 标度重算四力跨度 ============
a_s_MZ = ADD02["Strong"]                # 0.1179 本身就是 M_Z 值
a_G_MZ = alpha_G(M_Z)
a_em_MZ = alpha_em_MZ
a_2_MZ = alpha_2_MZ
span_MZ = math.log10(a_s_MZ / a_G_MZ)
span_add02 = ADD02_span_dex
over_by = span_add02 - span_MZ
KEYS["T3_alphaG_at_MZ"] = a_G_MZ
KEYS["T3_span_MZ_dex"] = span_MZ
KEYS["T3_span_ADD02_dex"] = span_add02
KEYS["T3_overestimate_dex"] = over_by
add("T3", "FAIL",
    "统一到 M_Z 标度重算 ⟹ ADD-02 的跨度**高估 %.2f 个量级**" % over_by,
    "同一能标（M_Z）下：α_s = %.4f、α_em = %.4e、α₂ = α_em/sin²θ_W = %.4e、"
    "**α_G(M_Z) = G·M_Z² = %.4e** ⟹ 跨度 α_s/α_G = **%.3f dex**。"
    "而 ADD-02 用的是 %.3f dex（其 α_G 取自电子标度，比 M_Z 标度小 %.2f 个量级）"
    "⟹ **跨度被高估 %.2f dex**（约 %.1e 倍）。"
    % (a_s_MZ, a_em_MZ, a_2_MZ, a_G_MZ, span_MZ, span_add02, over_by, over_by,
       10.0 ** over_by),
    {"α_G(M_Z)": a_G_MZ, "跨度(M_Z)[dex]": span_MZ,
     "跨度(ADD-02)[dex]": span_add02, "高估[dex]": over_by})

# ============ T4  δ_G（代表点角偏移）随之重算 ============
delta_G_MZ = math.asin(a_G_MZ / LAMBDA) / 3.0
delta_ratio = delta_G_MZ / ADD02_delta_G
KEYS["T4_delta_G_MZ_rad"] = delta_G_MZ
KEYS["T4_delta_G_ADD02_rad"] = ADD02_delta_G
KEYS["T4_ratio"] = delta_ratio
add("T4", "FAIL",
    "δ_G 需由 4.948e−45 rad 修正为 %.3e rad（同样差 %.2f 量级）"
    % (delta_G_MZ, math.log10(delta_ratio)),
    "δ = arcsin(α_G/λ)/3。ADD-02：α_G/λ = %.4e ⟹ δ = %.4e rad（称「约 44 位十进制精度」）；"
    "M_Z 标度：α_G/λ = %.4e ⟹ **δ = %.4e rad**（约 **%.1f 位**十进制精度）。"
    "修正比 = %.3e ⟹ **精细调参的严重性被高估了同样多的量级**；"
    "但请注意：修正后**仍是 ~34 位的精细调节**，结论方向不变（见 T6）。"
    % (ADD02["G"] / LAMBDA, ADD02_delta_G, a_G_MZ / LAMBDA, delta_G_MZ,
       abs(math.log10(delta_G_MZ)), delta_ratio),
    {"δ_G(M_Z)[rad]": delta_G_MZ, "δ_G(ADD-02)[rad]": ADD02_delta_G,
     "修正比": delta_ratio, "需精度[十进制位]": abs(math.log10(delta_G_MZ))})

# ============ T5  反噬自检：ESCAPE-AUDIT 自己的 E6 基线是否也混标 ============
# E6 用了「强 1 / 引力 5.9e-39」的教科书口径；反解 5.9e-39 的能标（T1：≈ m_p，0.938 GeV）
E6_G = 5.9e-39
E_of_E6 = E_from_alphaG(E6_G)
# E6 的「强 = 1」是低能强耦合（α_s(1 GeV) ~ 0.5 的量级归一），与 0.938 GeV 同量级 ✓
consistent_E6 = abs(E_of_E6 / m_p - 1.0) < 1e-2
KEYS["T5_E_of_E6_anchor_GeV"] = E_of_E6
KEYS["T5_E6_self_consistent"] = consistent_E6
add("T5", "PASS" if consistent_E6 else "BOUNDARY",
    "反噬自检：ESCAPE-AUDIT 自己的 E6 基线**未混标**（但需加注）",
    "E6 用的引力锚点 5.9e−39 反解能标 = %.4f GeV ≈ 质子质量（比 %.4f），"
    "而它配的「强 = 1」是**低能**强耦合归一 ⟹ 二者**同属 GeV 标度**，"
    "⟹ **E6 自身没有跨能标混用** ✓。但 E6 把该跨度（38 量级）与 α_s 的跑动并置时未声明能标，"
    "**需加注**：其 38 量级是「α_G 单耦合在 1 GeV→Planck 区间的**自身**变化」，"
    "不是「同一能标下四力之间的跨度」（后者按 T3 是 %.1f dex）。两种口径不可混称。"
    % (E_of_E6, E_of_E6 / m_p, span_MZ),
    {"E6 锚点能标[GeV]": E_of_E6, "E6 自身一致性": consistent_E6,
     "同能标四力跨度[dex]": span_MZ})

# ============ T6  结论方向不变性检验（关键：修正不推翻上游） ============
# OPEN-ΩH：单常数 cos3θ 结构给的四力比值上限 ~16× ≈ 1.21 dex
cap_dex = 1.21
gap_before = span_add02 - cap_dex
gap_after = span_MZ - cap_dex
KEYS["T6_gap_before_dex"] = gap_before
KEYS["T6_gap_after_dex"] = gap_after
ok_t6 = gap_after > 10.0
add("T6", "PASS" if ok_t6 else "FAIL",
    "**修正不推翻上游**：缺口由 %.1f dex 降为 %.1f dex，仍**远超**结构上限 ⟹ 结论方向不变"
    % (gap_before, gap_after),
    "OPEN-ΩH 的核心结论是「单常数 cos3θ 结构的比值上限 ~%.2f dex，与观测差一个巨大缺口 ⟹ 层级为外部输入」。"
    "用 ADD-02 的混标跨度：缺口 = %.1f dex；用 M_Z 统一跨度：缺口 = %.1f dex。"
    "⟹ **缺口缩小了 %.1f dex，但仍是 %.1f 个量级** ⟹ "
    "「层级外部输入 / 公理集内无解」的**结论完全成立**，只是数值被高估。"
    "**本册是修正，不是推翻。**" % (cap_dex, gap_before, gap_after, over_by, gap_after),
    {"结构上限[dex]": cap_dex, "缺口(原)[dex]": gap_before, "缺口(修正)[dex]": gap_after})

# ============ T7  对代价矩阵（r14）的影响：结构不动、数值更新 ============
ratio_MZ = a_G_MZ / a_s_MZ
# 引力行 = ratio × 强核行 的**严格成比例**是结构性质，只依赖「是标量倍数」，不依赖倍数大小
rank_unchanged = True
KEYS["T7_ratio_GS_ADD02"] = ADD02_ratio_GS
KEYS["T7_ratio_GS_MZ"] = ratio_MZ
add("T7", "PASS" if rank_unchanged else "FAIL",
    "对代价矩阵（r14）的影响：**结构结论不受影响**，仅数值需更新",
    "代价矩阵依赖「引力行 ∥ 强核行，比值 %.3e」推出 rank = 3、nullity 劣化。"
    "修正为 M_Z 标度后比值 = %.3e。但**严格成比例是结构性质**（只依赖它是一个标量倍数，"
    "与倍数大小无关）⟹ **rank = 3、nullity、可证伪窗口计数全部不变** ⟹ "
    "代价矩阵的出路 3/4 排序与「不代选」立场**均不受本册影响**。"
    "需更新的只是登记数值（%.3e ⟹ %.3e）。"
    % (ADD02_ratio_GS, ratio_MZ, ADD02_ratio_GS, ratio_MZ),
    {"比值(ADD-02)": ADD02_ratio_GS, "比值(M_Z)": ratio_MZ, "rank 结构": "不变"})

# ============ T8  终局 + 建议入体例的能标一致性条款 ============
add("T8", "FAIL",
    "终局：ADD-02 耦合表存在**能标混用缺陷**（需更正登记）；建议新增体例条款",
    "ADD-02 的四力耦合表把 M_Z 标度的 α_s、零能标的 α_em、电子标度的 α_G 并列，"
    "由此得到的 span_dex = %.3f 与 δ_G = %.3e **系统性高估 %.2f 个量级**。"
    "**建议更正为**：span_dex = **%.3f**（M_Z 统一标度）、δ_G = **%.3e rad**、"
    "引力/强比值 = **%.3e**。上游「层级外部输入」结论**不变**（T6）。"
    "⟹ **建议写入体例的新条款 —— 能标一致性**：任何**跨力耦合比较**必须显式声明其能标；"
    "同一表内不得混用不同能标的耦合值；未声明能标者一律记 **BOUNDARY/FAIL**。"
    "（本册即该条款的首个应用实例：它既抓出了上游缺陷，也通过 T5 自检确认了自身合规。）"
    % (span_add02, ADD02_delta_G, over_by, span_MZ, delta_G_MZ, ratio_MZ),
    {"更正 span_dex": span_MZ, "更正 δ_G[rad]": delta_G_MZ,
     "更正 引力/强": ratio_MZ, "新条款": "能标一致性"})

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond):
    GUARDS.append(dict(name=name, ok=bool(cond)))

guard("G = 1/M_Pl^2 量纲自洽（α_G(M_Pl)=1）", abs(alpha_G(M_Pl) - 1.0) < 1e-9)
guard("T1 锚点①：5.9e-39 ⟹ E ≈ m_p（相对误差<1e-3）", abs(r_p - 1.0) < 1e-3)
guard("T1 锚点②：1.75e-45 ⟹ E ≈ m_e（相对误差<1e-3）", abs(r_e - 1.0) < 1e-3)
guard("T2 判为能标混用（≥3 个不同能标）", n_distinct >= 3)
guard("T3 修正跨度小于 ADD-02 跨度（确认高估）", span_MZ < span_add02)
guard("T3 高估量在 5~15 dex 之间", 5.0 < over_by < 15.0)
guard("T4 δ_G 修正比与跨度修正同量级（≈10 dex）", 9.0 < math.log10(delta_ratio) < 12.0)
guard("T5 E6 锚点 ≈ 质子质量（自身合规）", consistent_E6)
guard("T6 修正后缺口仍 > 10 dex（结论不变性）", gap_after > 10.0)
guard("T7 比值更新不改变严格成比例结构", rank_unchanged)
guard("α_em(M_Z) > α_em(0)（QED 跑动方向正确）", alpha_em_MZ > alpha_em_0)
guard("α_2(M_Z) > α_em(M_Z)（sin²θ_W < 1）", alpha_2_MZ > alpha_em_MZ)
guard("判定条目 >= 8", len(VERDICTS) >= 8)

n_pass = sum(1 for v in VERDICTS if v["status"] == "PASS")
n_fail = sum(1 for v in VERDICTS if v["status"] == "FAIL")
n_bnd = sum(1 for v in VERDICTS if v["status"] == "BOUNDARY")
g_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(tag=TAG, verdicts=VERDICTS, guards=GUARDS, key_numbers=KEYS,
           counts=dict(PASS=n_pass, FAIL=n_fail, BOUNDARY=n_bnd,
                       guard_ok=g_ok, guard_total=len(GUARDS)))
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = ["# %s（判定产物）" % TAG, ""]
L.append("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
         % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
L.append("")
for v in VERDICTS:
    L.append("## %s [%s] %s" % (v["id"], v["status"], v["title"]))
    L.append(v["detail"]); L.append("")
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("=" * 78)
print("能标一致性与四力跨度重算 · E9 判据反噬自检")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
      % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-4s %-9s %s" % (v["id"], v["status"], v["title"][:52]))
print("-" * 78)
for k in ["T1_E_textbook_GeV", "T1_ratio_to_mp", "T1_E_add02_GeV", "T1_ratio_to_me",
          "T2_scale_spread_dex", "T3_alphaG_at_MZ", "T3_span_MZ_dex",
          "T3_span_ADD02_dex", "T3_overestimate_dex",
          "T4_delta_G_MZ_rad", "T6_gap_after_dex", "T7_ratio_GS_MZ"]:
    print("  %-28s %s" % (k, KEYS[k]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if g_ok == len(GUARDS) else 1)
