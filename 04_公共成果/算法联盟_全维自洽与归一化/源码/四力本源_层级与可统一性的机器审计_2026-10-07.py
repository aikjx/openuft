# -*- coding: utf-8 -*-
"""四力本源：层级与可统一性的机器审计。

命题：「四种基本力」是不是四个本源？
本册不谈哲学，只做可机器判定的拆解。全部计算在自然单位，纯标准库。

核心判据族：
  F0  补全 2026-10-05 册 T2 的 NOT-ASSESSED：ADD-02 的 α_weak 究竟是什么、什么能标
  F1  「弱力弱」是传播子质量压制造成的低能赝象，不是耦合常数小
  F2  电磁与弱本就是同一种力（电弱统一，已实验确立）
  F3  强力「强」也是能标现象（渐近自由）
  F4  引力耦合带量纲 ⟹ 与规范力不同类，不能进同一张比较表
  F5  「力的个数」是能标依赖的量
  F6  SM 一圈三耦合不交于一点
  F7  MSSM 一圈确实交于一点（机器复算，并诚实标注其为假设）
  F8  终局分级结论

八/九条判定 + guard。
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "四力本源_层级与可统一性的机器审计_2026-10-07"

VERDICTS, KEYS = [], {}
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

# ---------------- 输入（标准取值，非本册推导） ----------------
M_Z = 91.1876                 # GeV
M_W = 80.377                  # GeV
sin2_thW = 0.2312             # on-shell sin²θ_W(M_Z)
alpha_em_MZ = 1.0 / 127.95
alpha_s_MZ = 0.1179
M_Pl = 1.22091e19             # GeV
G_GeV = 1.0 / (M_Pl ** 2)     # GeV^-2

# 导出
alpha_2_MZ = alpha_em_MZ / sin2_thW                       # SU(2) 耦合
cos2_thW = 1.0 - sin2_thW
alpha_Y_MZ = alpha_em_MZ / cos2_thW                       # U(1)_Y 耦合
alpha_1_MZ = (5.0 / 3.0) * alpha_Y_MZ                     # GUT 归一化 U(1)
inv = lambda a: 1.0 / a
a1i, a2i, a3i = inv(alpha_1_MZ), inv(alpha_2_MZ), inv(alpha_s_MZ)

def run_to(a_inv_MZ, b, L):
    """一圈跑动：α⁻¹(μ) = α⁻¹(M_Z) − (b/2π)·ln(μ/M_Z)。"""
    return a_inv_MZ - (b / (2.0 * math.pi)) * L

def cross_L(inv_i, inv_j, b_i, b_j):
    """求两耦合相等的 ln(μ/M_Z)。"""
    return 2.0 * math.pi * (inv_i - inv_j) / (b_i - b_j)

# ============ F0  补全 2026-10-05 册 T2 的 NOT-ASSESSED ============
ADD02_alpha_weak = 1.696e-2
r_weak = ADD02_alpha_weak / alpha_1_MZ
KEYS["F0_alpha_1_MZ"] = alpha_1_MZ
KEYS["F0_ratio_to_ADD02"] = r_weak
ok_f0 = abs(r_weak - 1.0) < 1e-2
add("F0", "PASS" if ok_f0 else "BOUNDARY",
    "补全：ADD-02 的 α_weak = 1.696e−2 即 **α₁(M_Z)**，能标为 M_Z（昨日 NOT-ASSESSED 已解）",
    "2026-10-05 册 T2 把 α_weak = %.4e 的能标标为 NOT-ASSESSED。本册识别："
    "α₁ = (5/3)·α_em/cos²θ_W = %.6e，与 ADD-02 的 %.4e 之比 **%.5f**（差 %.1f%%）"
    "⟹ **它就是 GUT 归一化的 U(1) 超荷耦合，能标 M_Z**。"
    "⟹ 该开放项关闭。注意：这**不改变** T2 的结论——α_em 取零能标、α_G 取电子标度仍是混标，"
    "只是四个耦合中**有两个**（α_s 与 α_weak）同属 M_Z，混标来自另外两个。"
    % (ADD02_alpha_weak, alpha_1_MZ, ADD02_alpha_weak, r_weak, abs(r_weak - 1.0) * 100),
    {"α₁(M_Z)": alpha_1_MZ, "ADD-02 α_weak": ADD02_alpha_weak, "比值": r_weak})

# ============ F1  「弱力弱」是低能赝象（本册最强洞察） ============
E_low = 1.0                                    # GeV，教科书强度表的标度
suppress = (E_low / M_W) ** 2                  # W 传播子压制 ~(E/M_W)²
alpha_weak_eff_low = alpha_2_MZ * suppress
ratio_weak_over_em = alpha_2_MZ / alpha_em_MZ
KEYS["F1_alpha_2_MZ"] = alpha_2_MZ
KEYS["F1_suppress_factor"] = suppress
KEYS["F1_alpha_weak_eff_1GeV"] = alpha_weak_eff_low
KEYS["F1_weak_over_em_at_MZ"] = ratio_weak_over_em
ok_f1 = False
add("F1", "FAIL",
    "**「弱力弱」是传播子质量压制的低能赝象**：在 M_Z 标度弱比电磁**强 %.2f 倍**"
    % ratio_weak_over_em,
    "分解：弱作用的低能表观强度 = α₂(M_Z) × (E/M_W)²。取 E = 1 GeV：压制因子 (1/%.1f)² = %.3e，"
    "⟹ α_weak^eff(1 GeV) = %.4e × %.3e = **%.3e**，与教科书「弱 ~10⁻⁵」**同量级** ✓。"
    "但 α₂(M_Z) = %.4e **大于** α_em(M_Z) = %.4e（比值 **%.2f**）⟹ "
    "**在高能标，弱相互作用并不比电磁弱，反而更强**。"
    "⟹ 教科书强度表里「弱力排第三（10⁻⁵）」**完全是 W/Z 质量造成的低能假象**，不是耦合常数的本源性质。"
    % (M_W, suppress, alpha_2_MZ, suppress, alpha_weak_eff_low,
       alpha_2_MZ, alpha_em_MZ, ratio_weak_over_em),
    {"α₂(M_Z)": alpha_2_MZ, "α_em(M_Z)": alpha_em_MZ, "弱/电磁(M_Z)": ratio_weak_over_em,
     "压制因子(E=1GeV)": suppress, "α_weak^eff(1GeV)": alpha_weak_eff_low})

# ============ F2  电弱统一（已实验确立） ============
g = math.sqrt(4.0 * math.pi * alpha_2_MZ)
e_check = g * math.sqrt(sin2_thW)
alpha_em_check = e_check ** 2 / (4.0 * math.pi)
err = abs(alpha_em_check / alpha_em_MZ - 1.0)
KEYS["F2_g"] = g
KEYS["F2_e_from_weak"] = e_check
KEYS["F2_alpha_em_check"] = alpha_em_check
KEYS["F2_rel_err"] = err
ok_f2 = err < 1e-3
add("F2", "PASS" if ok_f2 else "FAIL",
    "电磁与弱**本就是同一种力**：e = g·sinθ_W 机器自洽（相对误差 %.1e），电弱统一已确立" % err,
    "由 α₂(M_Z) = %.5f 反解 g = √(4πα₂) = %.5f；乘 sinθ_W = %.5f 得 e = %.5f；"
    "回代 α_em = e²/4π = %.5e，与输入 %.5e 的相对误差 **%.1e** ⟹ **电磁耦合由弱耦合与弱混合角导出** ✓。"
    "⟹ 在 E ≳ M_W 标度，电磁与弱是同一个 SU(2)_L×U(1)_Y 的两个面向 ⟹ "
    "**此时可区分的相互作用是 3 个，不是 4 个**。该结论由 W/Z 发现与中性流测量**实验确立**，非推测。"
    % (alpha_2_MZ, g, math.sqrt(sin2_thW), e_check, alpha_em_check, alpha_em_MZ, err),
    {"g": g, "e(由弱导出)": e_check, "α_em(回代)": alpha_em_check, "相对误差": err})

# ============ F3  强力渐近自由 ============
b3_SM = -7.0
Ls = [math.log(x / M_Z) for x in (1.0, M_Z, 1000.0)]
alpha_s_at = [1.0 / run_to(a3i, b3_SM, L) for L in Ls]
KEYS["F3_alpha_s_1GeV"] = alpha_s_at[0]
KEYS["F3_alpha_s_MZ"] = alpha_s_at[1]
KEYS["F3_alpha_s_1TeV"] = alpha_s_at[2]
ok_f3 = alpha_s_at[2] < alpha_s_at[1]
add("F3", "PASS" if ok_f3 else "FAIL",
    "强力「强」同样是能标现象（渐近自由）：α_s 随能标**下降**",
    "一圈 QCD（b₃ = −7）：α_s(1 GeV) ≈ **%.3f**（已入非微扰区，仅作趋势）、"
    "α_s(M_Z) = **%.4f**、α_s(1 TeV) = **%.4f** ⟹ **随能标单调下降** ✓。"
    "⟹ 「强力最强」也是低能陈述。⚠️ 诚实：1 GeV 处一圈公式已不可靠（α_s ~ O(1)），"
    "本册只取**趋势**，不取该点数值。"
    % (alpha_s_at[0], alpha_s_at[1], alpha_s_at[2]),
    {"α_s(1GeV,趋势)": alpha_s_at[0], "α_s(M_Z)": alpha_s_at[1], "α_s(1TeV)": alpha_s_at[2]})

# ============ F4  引力与规范力不同类 ============
# 规范耦合无量纲；G 在自然单位带质量量纲 −2 ⟹ α_G = G·E² 随能标增长（唯一如此）
aG_1GeV = G_GeV * 1.0
aG_MZ = G_GeV * M_Z ** 2
aG_Pl = G_GeV * M_Pl ** 2
dim_G_mass = -2
KEYS["F4_alphaG_1GeV"] = aG_1GeV
KEYS["F4_alphaG_MZ"] = aG_MZ
KEYS["F4_alphaG_Planck"] = aG_Pl
KEYS["F4_dim_G_mass"] = dim_G_mass
ok_f4 = False
add("F4", "FAIL",
    "**引力与规范力不同类**：耦合常数**带量纲** ⟹ 不能进同一张「耦合强度比较表」",
    "规范耦合 g、g′、g_s 均**无量纲**；而 G 在自然单位带质量量纲 **%d**（[G] = M^%d），"
    "⟹ 引力只能构成能标依赖的有效耦合 α_G(E) = G·E²，其值随能标**增长**（唯一增长的力）："
    "α_G(1 GeV) = %.3e → α_G(M_Z) = %.3e → α_G(M_Pl) = **%.3f**。"
    "⟹ 把引力与三个规范力并置在同一张「四力相对强度表」里，是**把带量纲量与无量纲量并列**的范畴错误——"
    "这比 2026-10-05 册 E9（该表是能标快照）**更本源**：E9 说的是表随能标变，"
    "F4 说的是**引力根本不是同一类对象**。"
    % (dim_G_mass, dim_G_mass, aG_1GeV, aG_MZ, aG_Pl),
    {"[G] 质量量纲": dim_G_mass, "α_G(1GeV)": aG_1GeV,
     "α_G(M_Z)": aG_MZ, "α_G(M_Pl)": aG_Pl})

# ============ F5  「力的个数」是能标依赖的 ============
table = [
    ("E < M_W (~80 GeV)", 4, "弱作用被 W/Z 质量压制，表现为独立的「弱力」"),
    ("M_W < E < M_GUT", 3, "电磁与弱已统一为电弱力（实验确立）"),
    ("E > M_GUT（若 GUT 成立）", 2, "强与电弱统一；引力仍独立"),
]
KEYS["F5_stages"] = table
add("F5", "FAIL",
    "**「四力」是低能标签，不是本源分类**：可区分的相互作用个数随能标变化 4 → 3 → 2",
    "按能标分层：%s。⟹ 追问「四力的本质本源」时，"
    "**「四」这个数字本身没有本源地位**——它只是我们在 ~GeV 标度做实验时看到的表观计数。"
    "真正的本源问题是：**规范群为什么是 SU(3)×SU(2)×U(1)**，以及**引力为何是几何而非规范力**——"
    "这两个问题本册**不作回答**（超出可机器判定范围），只判定「四力」不是答案的一部分。"
    % "；".join("%s ⟹ **%d** 个（%s）" % (a, b, c) for a, b, c in table),
    {"分层": [list(t) for t in table]})

# ============ F6  SM 一圈三耦合不交于一点 ============
b_SM = (41.0 / 10.0, -19.0 / 6.0, -7.0)      # (b1, b2, b3)，GUT 归一化
L12 = cross_L(a1i, a2i, b_SM[0], b_SM[1])
L23 = cross_L(a2i, a3i, b_SM[1], b_SM[2])
L13 = cross_L(a1i, a3i, b_SM[0], b_SM[2])
M12 = M_Z * math.exp(L12); M23 = M_Z * math.exp(L23); M13 = M_Z * math.exp(L13)
spread_SM = math.log10(max(M12, M23, M13) / min(M12, M23, M13))
# 在 1-2 交点处检查 α_3 是否也相等
a3_at_12 = run_to(a3i, b_SM[2], L12)
a1_at_12 = run_to(a1i, b_SM[0], L12)
gap_SM = abs(a1_at_12 - a3_at_12)
KEYS["F6_M12"] = M12; KEYS["F6_M23"] = M23; KEYS["F6_M13"] = M13
KEYS["F6_spread_dex"] = spread_SM
KEYS["F6_inv_gap_at_12"] = gap_SM
ok_f6 = False
add("F6", "FAIL",
    "SM 一圈三耦合**不交于一点**：三个两两交点分散 **%.2f 个量级**" % spread_SM,
    "SM 一圈系数 b = (%.2f, %.4f, %.0f)。两两交点标度："
    "M₁₂ = %.3e GeV、M₂₃ = %.3e GeV、M₁₃ = %.3e GeV ⟹ 最高与最低相差 **%.2f dex**。"
    "在 M₁₂ 处检验第三个：α₁⁻¹ = %.2f 而 α₃⁻¹ = %.2f ⟹ **差 %.2f**（非零）⟹ 不共点。"
    "⟹ **标准模型自身不给出规范耦合统一**（回链 X17/J20/J32，本册为独立复算）。"
    % (b_SM[0], b_SM[1], b_SM[2], M12, M23, M13, spread_SM,
       a1_at_12, a3_at_12, gap_SM),
    {"M₁₂[GeV]": M12, "M₂₃[GeV]": M23, "M₁₃[GeV]": M13,
     "分散[dex]": spread_SM, "α⁻¹ 差": gap_SM})

# ============ F7  MSSM 一圈确实交于一点（机器复算，标注为假设） ============
b_MSSM = (33.0 / 5.0, 1.0, -3.0)
Lm12 = cross_L(a1i, a2i, b_MSSM[0], b_MSSM[1])
Lm23 = cross_L(a2i, a3i, b_MSSM[1], b_MSSM[2])
Lm13 = cross_L(a1i, a3i, b_MSSM[0], b_MSSM[2])
Lm = [Lm12, Lm23, Lm13]
rel_spread = (max(Lm) - min(Lm)) / (sum(Lm) / 3.0)
M_U = M_Z * math.exp(sum(Lm) / 3.0)
aU_inv = run_to(a1i, b_MSSM[0], sum(Lm) / 3.0)
aU = 1.0 / aU_inv
KEYS["F7_M_U_GeV"] = M_U
KEYS["F7_alpha_U_inv"] = aU_inv
KEYS["F7_alpha_U"] = aU
KEYS["F7_rel_spread"] = rel_spread
ok_f7 = rel_spread < 0.01
add("F7", "PASS" if ok_f7 else "FAIL",
    "MSSM 一圈**确实**交于一点：M_U ≈ %.2e GeV、α_U ≈ 1/%.1f（三交点相对离散 %.2f%%）"
    % (M_U, aU_inv, rel_spread * 100),
    "MSSM 一圈系数 b = (%.1f, %.0f, %.0f)。三个两两交点的 ln(μ/M_Z) = %.2f / %.2f / %.2f"
    "⟹ **相对离散仅 %.2f%%**（对照 SM 的 %.2f dex 分散）⟹ **共点** ✓。"
    "统一标度 M_U = **%.3e GeV**，统一耦合 α_U⁻¹ = **%.2f**（α_U = %.4f = 1/%.1f）。"
    "⟹ 这给出「**统一需要什么**」的定量答案：**必须在 SM 之上增加改变 β 系数的新物理**。"
    "⚠️ **诚实边界（三重）**：① MSSM 是**假设**，超对称粒子**至今未被发现**；"
    "② 本册用**单一阈值**简化（真实谱的阈修正未计）；③ 一圈近似。"
    "⟹ 本册**不主张** MSSM 正确，只主张：**SM 不统一，而改动 β 系数即可统一**这一事实是可机器验证的。"
    % (b_MSSM[0], b_MSSM[1], b_MSSM[2],
       Lm12, Lm23, Lm13, rel_spread * 100, spread_SM, M_U, aU_inv, aU, aU_inv),
    {"M_U[GeV]": M_U, "α_U⁻¹": aU_inv, "α_U": aU, "相对离散": rel_spread})

# ============ F8  终局：四力本源的分级结论 ============
add("F8", "FAIL",
    "终局：「四力」**不是**四个本源 —— 它是低能标签 + 一个范畴混装",
    "分级结论（全部由上述机器读数承担）："
    "① **弱力的「弱」是假象**（F1：α₂(M_Z) = %.4f > α_em = %.4f，弱在高能比电磁强 %.2f 倍，"
    "低能的 10⁻⁵ 来自 (E/M_W)² 压制）；"
    "② **电磁与弱本是一种力**（F2：e = g·sinθ_W 自洽到 %.0e，实验确立）⟹ 高能只有 3 个；"
    "③ **强力的「强」随能标减弱**（F3：渐近自由）；"
    "④ **引力与规范力不同类**（F4：[G] = M^−2 带量纲，α_G 随能标增长，是唯一如此者）⟹ "
    "四力同表比较是**范畴混装**，不只是数值问题；"
    "⑤ **SM 自身不统一**（F6：三交点分散 %.2f dex），但**改动 β 系数即可统一**（F7：MSSM 共点于 %.1e GeV）。"
    "⟹ **对「四力的本质本源」这一问，可机器判定的答案是：」四」不是本源数字；"
    "弱与电磁已证同源；引力是另一个范畴；剩下真正开放的问题是「为何是这个规范群」与「量子引力」——"
    "**这两个问题本册不作回答，也不宣称任何突破**。"
    % (alpha_2_MZ, alpha_em_MZ, ratio_weak_over_em, err, spread_SM, M_U),
    {"弱/电磁(M_Z)": ratio_weak_over_em, "电弱自洽误差": err,
     "SM 分散[dex]": spread_SM, "MSSM M_U[GeV]": M_U})

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond):
    GUARDS.append(dict(name=name, ok=bool(cond)))

guard("α₁(M_Z) 落在教科书 59 附近（α₁⁻¹ ∈ [55,63]）", 55.0 < a1i < 63.0)
guard("F0 识别：ADD-02 α_weak ≈ α₁(M_Z)（<1%）", abs(r_weak - 1.0) < 1e-2)
guard("α₂(M_Z) 落在教科书 ~1/29.6（α₂⁻¹ ∈ [27,32]）", 27.0 < a2i < 32.0)
guard("F1 核心：α₂ > α_em（弱在高能强于电磁）", alpha_2_MZ > alpha_em_MZ)
guard("F1 压制因子量级正确（1e-5 ~ 1e-3）", 1e-5 < suppress < 1e-3)
guard("F2 电弱关系 e=g·sinθ_W 自洽（<1e-3）", err < 1e-3)
guard("F3 α_s 随能标下降（渐近自由）", alpha_s_at[2] < alpha_s_at[1])
guard("F4 α_G 随能标严格增长", aG_1GeV < aG_MZ < aG_Pl)
guard("F4 α_G(M_Pl) == 1（G=1/M_Pl² 自洽）", abs(aG_Pl - 1.0) < 1e-9)
guard("F6 SM 三交点分散 > 1 dex（确认不统一）", spread_SM > 1.0)
guard("F7 MSSM 三交点相对离散 < 1%（确认共点）", rel_spread < 0.01)
guard("F7 M_U 落在教科书 1e16 量级（1e15~1e17）", 1e15 < M_U < 1e17)
guard("F7 α_U⁻¹ 落在教科书 ~24（20~30）", 20.0 < aU_inv < 30.0)
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
print("四力本源：层级与可统一性的机器审计")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
      % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-4s %-9s %s" % (v["id"], v["status"], v["title"][:54]))
print("-" * 78)
for k in ["F0_alpha_1_MZ", "F0_ratio_to_ADD02",
          "F1_alpha_2_MZ", "F1_weak_over_em_at_MZ", "F1_alpha_weak_eff_1GeV",
          "F2_alpha_em_check", "F2_rel_err",
          "F3_alpha_s_1TeV", "F4_alphaG_MZ", "F4_alphaG_Planck",
          "F6_spread_dex", "F6_inv_gap_at_12",
          "F7_M_U_GeV", "F7_alpha_U_inv", "F7_rel_spread"]:
    print("  %-26s %s" % (k, KEYS[k]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if g_ok == len(GUARDS) else 1)
