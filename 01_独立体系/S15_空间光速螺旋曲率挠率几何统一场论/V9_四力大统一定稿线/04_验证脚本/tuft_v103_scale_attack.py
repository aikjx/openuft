# -*- coding: utf-8 -*-
"""TUFT V9.15 观测尺度攻破 + 两处口径修复（本线独立贡献，与并行线 V9.14 g 因子并行）
A 组：V9.11 欠定论证的表述修复——连续自由度恰好 2↔2（非欠定）；q_EM=√α·Z 已是绑定式
B 组：π 介子力程口径修复——π⁰(1.4619 fm) vs π±(1.4139 fm) 偏差 3.3%，需统一
C 组：螺旋半径 vs 点状性——ρ_e=386.149 fm 与电子半径上界 r_e<2.8e-19 m 差 6 个数量级；
      形状因子偏离标度 q₀=ħc/ρ=m_e c²=0.511 MeV；Hopf 对照：拓扑保护缺失；
      公设语义二选一判定（空间延展→观测冲突 FAIL / 参数字典→世界线公设失去空间几何内容）
用法：python tuft_v103_scale_attack.py
"""
import json, math

HBARC = 197.3269804          # MeV·fm
ALPHA = 7.2973525693e-3
ME_MEV = 0.51099895          # MeV
ME_KG  = 9.1093837015e-31
R_E_UPPER = 2.8e-19          # m（LEP Bhabha 组合分析 95% CL，arXiv 2506.02450）

# ---------- A 组：欠定论证修复 ----------
A = {}
# A1 (ρ,b)→(m,α) 双射（复算 V9.11）
rho_e = HBARC/(ME_MEV*math.sqrt(1.0+ALPHA*ALPHA))   # fm（2.7：ρ=ħ/(mc√(1+α²))）
b_e = ALPHA*rho_e
m_check = HBARC/math.sqrt(rho_e*rho_e + b_e*b_e)    # MeV
A["A1_double"] = {"rho_e_fm": rho_e, "b_e_fm": b_e,
                  "m_check_MeV": m_check, "rel_dev_m": abs(m_check-ME_MEV)/ME_MEV,
                  "detJ_ne0": "det J = −m/ρ² ≠ 0 ⇒ (ρ,b)↔(m,α) 局部双射（2 连续 DOF ↔ 2 独立连续观测）"}
# A2 q_EM=√α·Z 绑定式（3.3 节）：q 的连续部分由 (ρ,b) 唯一确定
A["A2_qbound"] = {
    "q_EM_def": "q_EM = √α·Z，α=b/ρ ⇒ q_EM = √(b/ρ)·Z",
    "numeric": {"sqrt_alpha": math.sqrt(ALPHA), "sqrt_b_over_rho": math.sqrt(b_e/rho_e),
                "Z": 1.0, "q_EM": math.sqrt(ALPHA)},
    "point": "V9.11 C2『没有任何几何方程把 q 与 (ρ,b) 绑定』与 3.3 定义式直接矛盾：q_EM=√(b/ρ)·Z 即绑定式（√α 数值仍外输 = B02 已证失败；Z 为外部离散量子数）"}
# A3 连续 DOF 计数重算
A["A3_count"] = {
    "statement": ("{m,α} ↔ (ρ,b) 恰好 2↔2（双射，det J≠0）；q_EM 连续部分 √(b/ρ) 由 (ρ,b) 固定；"
                  "剩余自由度 Z 为离散外部量子数。连续自由度层面不欠定。"),
    "verdict": ("V9.11『欠定度≥1、q 无几何约束』为过强表述：q_EM 与几何有绑定（√α 数值外输≠无绑定）。"
                "B03 的计数层正确佐证 = 外输清单计数（√α 数值(B02)、Z 量子化、g_W、α_s、m_P 均外输），"
                "而非『连续欠定度≥1』。B03 本身 FAIL 维持（理由不变：耦合常数数值外输）。")}

# ---------- B 组：π 介子口径修复 ----------
B = {}
m_pi0, m_pipm = 134.9768, 139.570    # MeV（π⁰ / π±）
lam_pi0  = HBARC/m_pi0
lam_pipm = HBARC/m_pipm
B["ranges"] = {"lam_pi0_fm": lam_pi0, "lam_pipm_fm": lam_pipm,
               "rel_dev": abs(lam_pi0-lam_pipm)/lam_pi0,
               "book_44": "全书 4.4 节 λ_π≈1.462×10⁻¹⁵ m（π⁰ 口径）",
               "v912": "V9.12 18.3.1 表 λ_π=1.414 fm（π± 139.57 MeV 口径）"}
B["verdict"] = ("口径漂移确认：π⁰ 1.4619 fm vs π± 1.4139 fm，相对偏差 3.3%。"
                "修复：全书统一 π⁰ 口径（与 4.4、第十一章、V9.11 C3 表一致）；"
                "V9.12 表 λ_π 若保留 π± 须显式标注粒子种类，不得混用。")

# ---------- C 组：螺旋半径 vs 点状性（新攻破） ----------
C = {}
# C1 尺度与动量标度
C["C1_scales"] = {
    "rho_e_fm": rho_e, "rho_e_m": rho_e*1e-15,
    "b_e_fm": b_e,
    "q0_MeV_hbarc_over_rho": HBARC/rho_e,          # = m_e c² = 0.511 MeV（数学必然：ρ=ħ/(mc)）
    "m_e_c2_MeV": ME_MEV,
    "ratio_rho_over_r_upper": (rho_e*1e-15)/R_E_UPPER,  # 6 个数量级
}
# C2 电荷延展假设下的形状因子偏离（球近似 F≈1−⟨r²⟩q²/(6ħ²c²)，⟨r²⟩~ρ²）
def form_factor_deviation(q_MeV, rho_fm):
    # (qρ/ħc)² = (q[MeV]·ρ[fm]/ħc[MeV·fm])²
    x = q_MeV*rho_fm/HBARC
    return x*x/6.0
C["C2_ff"] = {
    "q_points_MeV": [0.05, 0.1, 0.511, 1.0],
    "deviation": {("q=%.3f MeV"%q): form_factor_deviation(q, rho_e) for q in [0.05, 0.1, 0.511, 1.0]},
    "note": "若电荷按螺旋轨迹延展（半径 ρ_e=386 fm 筒面），形状因子在 q≈0.511 MeV 处偏离 ~16%——"
            "MeV 级 Bhabha/Møller 散射（% 精度）即可排除；实验给出 r_e<2.8e-19 m（6 个数量级余量）。"}
# C3 Hopf 对照
C["C3_hopf"] = {
    "hopf": "Hopf 孤子框架（2026-04 提案）：康普顿尺度内部结构 + 拓扑保护电形状因子 G_E=1+O(10⁻¹⁴)，"
            "磁形状因子 F_M 在 q≈0.52 MeV 处降至 0.5——结构靠拓扑机制隐藏、并在磁通道显形（可检验）",
    "tuft": "TUFT 无任何等价保护机制（B03：无数值内容）；电荷若延展即被电形状因子直接排除，若集中于质心则需书中不存在的机制",
    "parallel": "注意：q₀=ħc/ρ_e=0.511 MeV=m_e c² 与 Hopf 磁形状因子显形标度 0.52 MeV 数值巧合同源"
                "（都是康普顿波长标度），但 TUFT 无 Hopf 的拓扑保护叙事。"}
# C4 公设语义二选一
C["C4_verdict"] = (
    "公设语义二选一（不新增 FAIL 数量，但定位公设的观测地位）：\n"
    "  (a) 空间延展读法：ρ_e=386 fm 是电子真实空间结构 → 形状因子 q≈0.5 MeV 偏离 ~16%，"
    "与 r_e<2.8e-19 m（6 个数量级）观测冲突 → 观测层 FAIL（除非引入书中不存在的电荷集中/拓扑保护机制）；\n"
    "  (b) 参数字典读法：ρ 不表示空间延展，仅提供 (m,α) 映射（V9.11 17.4 已承认 L2 独立场论、几何=参数字典）"
    "→ 『类光螺旋世界线』公设失去空间几何内容，降级为参数化母题（不冲突但公设本体论承诺缩减）；\n"
    "  两条路都不撤销既有判定（B01-B03、QCD、3.4、g 因子缺口维持）；本攻破的净结果是："
    "公设『世界线』的物理语义首次被正面审计——V9.5-V9.13 攻破的是下游，这里是源头。")

# ---------- 汇总 ----------
out = {"A_underdetermination_fix": A, "B_pion_range_fix": B, "C_scale_attack": C,
       "summary": {
           "A": "欠定论证修复：连续 DOF 2↔2 恰好确定；q_EM=√α·Z 绑定式；B03 佐证改为外输清单计数",
           "B": "π 介子口径漂移确认（3.3%），统一 π⁰ 口径",
           "C": ("螺旋半径 vs 点状性：ρ_e=386.149 fm vs r_e<2.8e-19 m，比值 %.1e（6 个数量级）；"
                 "形状因子偏离标度 0.511 MeV；Hopf 无保护对照；公设语义二选一（延展→FAIL / 参数字典→公设降级）"
                 % ((rho_e*1e-15)/R_E_UPPER)),
       }}
with open(r"D:\a10\aikjx\code\my_lib\tuft_v103_scale_attack_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
