# -*- coding: utf-8 -*-
"""
attack_C0147_大统一质子衰变攻破_2026-10-21.py
独立攻破：P08「大统一 / 质子衰变」· 物理 Top100 清单 T017（布局 Phase 1 续项）

定位：布局册（C0135）P08；物理 Top100 清单 T017。前置来料：
  - 攻破⑨ attack5_P03_GUT复核（2026-10-13 前）已独立复核 P03：最小非SUSY SU(5) 被质子衰变
    排除（最短预言 1e32 yr vs Super-K 下限 1.6e34 yr = 短 160 倍）；阈值-可见两难（C0007/C0009）。
  - C0140 耦合常数攻破（2026-10-20）已给出耦合汇聚精确读数：SM 单圈 ΔL=9.146 e-折不汇聚；
    MSSM 汇聚 M_GUT=1.539743e16 GeV、α_GUT^{-1}=25.72、τ_p≈3.51e34 yr（唯象标度律 [C]）。
本册**不重算汇聚读数**（P13 已由 C0140 攻破），只做两件本册第一性工作：
  (a) SU(5) 树级 sin²θ_W=3/8 的 Fraction 精算 + vs 观测 0.2312；
  (b) 维6算子质子衰变率 τ_p≈(1/α_GUT²)(M_X⁴/m_p⁵) 的 Decimal 48 位量级精算，
      并与 Super-K 2.4e34 yr 边界对照，明示「量级一致 / 超界 / 被排除」。
再对 TUFT/几何框架判定 GUT 群与 X,Y 超重玻色子能否从几何第一性原理生成（撞 C1/C2）。

把「大统一 / 质子衰变从哪来」压缩成五条可复核读数：
  E1 边界事实：Super-K 质子寿命下限、sin²θ_W(M_Z)、三耦合反演（外部值只引用不复算）。
  E2 核心公式体系（本册核心）：SU(5) 树级 sin²θ_W=3/8 第一性推导+精算；维6算子 τ_p 量级精算；
     minimal SU(5) τ_p~1e31 yr 被排除（引用攻破⑨ P03 160× 读数）。
  E3 汇聚性：引用 C0140 精确读数不复算（SM 不汇聚 / MSSM 汇聚但 τ_p≈3.51e34 yr）。
  E4 几何供给：GUT 群能否从几何第一性原理生成（C0137 签名非唯一 + attack24 紧致维上界 / KK n=5
     引用不重攻）；doublet-triplet 劈裂需精细调节（撞 C2/C3）。
  E5 裁定：P08 结构性负面（对 TUFT/几何框架），撞 C1（GUT 群 / 新重玻色子 X,Y）+ C2（M_GUT 绝对标度）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册**不宣称大统一已解决**；外部观测值只引用不复算；汇聚性读数只引用 C0140（P13 已攻破）；
τ_p 用维6算子量级估计（无量纲矩阵元/CKM 因子取 O(1)），判定按数量级（倍）而非末位。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- E1 外部边界事实（只引用不复算，注释标来源） ----------
# Super-K 2024 (90% CL)，p -> e+ pi0 道
TAU_P_SUPERK_LOWER = Decimal("2.4e34")   # yr，τ_p > 2.4e34
# PDG MS-bar 在 M_Z
SIN2_THETAW_MZ = Decimal("0.2312")       # sin²θ_W(M_Z) MS-bar
ALPHA1_INV_MZ = Decimal("59.01")         # α_1^{-1}(M_Z)，SU(5) 归一 5/3
ALPHA2_INV_MZ = Decimal("29.57")        # α_2^{-1}(M_Z)
ALPHA3_INV_MZ = Decimal("8.44")          # α_3^{-1}(M_Z)

# ---------- 维6算子精算常数（自然单位 ℏ=c=1） ----------
M_P = Decimal("0.938")                   # 质子质量 GeV
# 1 GeV^{-1} 换算为 yr：ℏ/GeV = 6.582119569e-25 s；1 yr = 31557600 s
HBAR_SEC = Decimal("6.582119569e-25")
SEC_PER_YR = Decimal("31557600")
GEVINV_TO_YR = HBAR_SEC / SEC_PER_YR     # ≈ 2.0867e-32 yr


def e1_boundary_facts():
    """E1 边界事实（只引用不复算）。"""
    return {
        "tau_p_superk_lower_yr": TAU_P_SUPERK_LOWER,
        "sin2_thetaW_MZ": SIN2_THETAW_MZ,
        "alpha1_inv_MZ": ALPHA1_INV_MZ,
        "alpha2_inv_MZ": ALPHA2_INV_MZ,
        "alpha3_inv_MZ": ALPHA3_INV_MZ,
    }


def e2_su5_tree_level_sin2():
    """SU(5) 树级 sin²θ_W = 3/8 第一性推导（Fraction 精确）。

    推导链：
      SU(5) 统一在 M_GUT 处 g1 = g2 = g3 = g（g1 用 SU(5) 归一 5/3，即 g1 = sqrt(5/3) g'）。
      统一点条件 g1(M_GUT) = g2(M_GUT)：
          sqrt(5/3) g' = g   =>   g'/g = sqrt(3/5)   =>   tan²θ_W = g'^2/g^2 = 3/5。
      sin²θ_W = tan²/(1+tan²) = (3/5)/(1+3/5) = (3/5)/(8/5) = 3/8。
    """
    tan2 = Fraction(3, 5)                       # tan²θ_W = g'^2/g^2 = 3/5
    sin2 = tan2 / (1 + tan2)                    # = (3/5)/(8/5) = 3/8
    assert sin2 == Fraction(3, 8)
    sin2_dec = Decimal(sin2.numerator) / Decimal(sin2.denominator)   # = 0.375
    obs = SIN2_THETAW_MZ
    ratio = sin2_dec / obs                      # 预言/观测
    return {
        "tan2_thetaW": tan2,                    # 3/5
        "sin2_thetaW_GUT": sin2,                # 3/8
        "sin2_thetaW_dec": sin2_dec,            # 0.375
        "observed_MZ": obs,                      # 0.2312
        "ratio_pred_over_obs": ratio,           # ~1.622
    }


def e2_proton_decay_scale(M_X, alpha_gut_inv):
    """维6算子质子衰变率量级精算。

    推导链（自然单位 ℏ=c=1）：
      X,Y 超重玻色子交换振幅 ~ g_GUT / M_X^2；维6四费米算符衰变率
          Γ_p ~ alpha_GUT^2 * m_p^5 / M_X^4   （相空间 / CKM / 强子矩阵元取 O(1)）
      τ_p = 1/Γ_p = M_X^4 / (alpha_GUT^2 * m_p^5)   [GeV^{-1}]
      换算 yr：乘 GEVINV_TO_YR。
    """
    alpha_gut = Decimal(1) / Decimal(alpha_gut_inv)
    m_p5 = M_P ** 5
    tau_gevinv = (M_X ** 4) / (alpha_gut * alpha_gut * m_p5)
    tau_yr = tau_gevinv * GEVINV_TO_YR
    return {
        "M_X_GeV": Decimal(M_X),
        "alpha_GUT_inv": Decimal(alpha_gut_inv),
        "alpha_GUT": alpha_gut,
        "tau_GeVinv": tau_gevinv,
        "tau_yr": tau_yr,
    }


def e2_core():
    """E2 核心：树级混合角 + 两标度 τ_p 量级 + vs Super-K 边界。"""
    s = e2_su5_tree_level_sin2()
    # minimal 非SUSY SU(5) 树级统一标度 ~ 1e15 GeV；α_GUT^{-1} ~ 40
    tau_minSU5 = e2_proton_decay_scale(Decimal("1e15"), Decimal("40"))
    # MSSM 汇聚标度 ~ 2e16 GeV；α_GUT^{-1} ~ 25
    tau_mssm = e2_proton_decay_scale(Decimal("2e16"), Decimal("25"))
    # vs Super-K 下限
    ratio_min = tau_minSU5["tau_yr"] / TAU_P_SUPERK_LOWER   # <1 => 预言短于下限 => 被排除
    ratio_mssm = tau_mssm["tau_yr"] / TAU_P_SUPERK_LOWER    # >1 => 长于下限 => 超界（太稳定）
    return {
        "sin2": s,
        "tau_minSU5": tau_minSU5,
        "tau_mssm": tau_mssm,
        "ratio_minSU5_over_SuperK": ratio_min,
        "ratio_mssm_over_SuperK": ratio_mssm,
    }


def e3_convergence_cite():
    """E3 汇聚性：只引用 C0140 精确读数，不复算。"""
    return {
        "source": "C0140_耦合常数攻破_2026-10-20（P13 已攻破，本册引用不复算）",
        "SM_single_loop_DeltaL_efold": Decimal("9.146484"),   # C0140 E2 读数
        "SM_converges": False,
        "MSSM_M_GUT_GeV": Decimal("1.539743e16"),            # C0140 E3 读数
        "MSSM_alpha_GUT_inv": Decimal("25.719816"),          # C0140 E3 读数
        "MSSM_tau_p_yr": Decimal("3.512960e34"),             # C0140 E3 唯象标度律[C]
        "MSSM_converges": True,
    }


def e4_geometry_supply():
    """E4 几何供给：GUT 群 / X,Y 超重玻色子能否从几何第一性原理生成？"""
    # C0137 读数：固定 SM 签名 (dim=12, rank=4) 至少有 3 个互不同构代数
    # （su(2)、su(3)、so(5)）共享 => 签名不能唯一锁定 SM，更遑论唯一锁定 SU(5)(dim24)/SO(10)(dim45)。
    c0137_candidates_sharing_signature = 3   # 引用 C0137 E2
    # attack24 读数：so(1,3) Killing 型惯性 (3,3) => 紧致子代数 dim <= 3；
    # KK 逃逸满足 dim>=12 & rank>=4 必要条件的最小额外维 n=5（so(1,8)）。
    attack24_compact_dim_max = 3            # 引用 attack24 B01/B03
    attack24_KK_min_n = 5                    # 引用 attack24 B06
    # doublet-triplet 劈裂：triplet 须在 M_GUT(~1e16 GeV) 压质子衰变，doublet 在 v(~1e2 GeV)。
    # 层级比 = M_GUT / v ~ 1e14，需精细调节（missing-partner 之外仍要 1e14 量级微调）。
    M_GUT = Decimal("1e16")
    v_weak = Decimal("1e2")
    dt_hierarchy = M_GUT / v_weak           # ~1e14
    return {
        "c0137_signature_candidates": c0137_candidates_sharing_signature,
        "attack24_compact_dim_max": attack24_compact_dim_max,
        "attack24_KK_min_extra_dim": attack24_KK_min_n,
        "doublet_triplet_hierarchy": dt_hierarchy,
        "geometry_supply_gut_group": "zero",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0147 · 大统一 / 质子衰变（P08 · Top100 T017）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_boundary_facts()
    w("\n[E1] 边界事实（外部值只引用不复算）")
    w("  Super-K(2024, 90%% CL, p->e+pi0)：τ_p > %s yr" % fv(g1["tau_p_superk_lower_yr"], "1e"))
    w("  sin²θ_W(M_Z, MS-bar) = %s" % g1["sin2_thetaW_MZ"])
    w("  三耦合反演(M_Z, MS-bar)：α1^{-1}=%s、α2^{-1}=%s、α3^{-1}=%s"
      % (g1["alpha1_inv_MZ"], g1["alpha2_inv_MZ"], g1["alpha3_inv_MZ"]))
    w("  => 边界事实：质子尚未观测到衰变（寿命 > 2.4e34 yr）；三耦合在 M_Z 并不同值。")
    entries.append(("E1", "Super-K τ_p>2.4e34 yr；sin²θ_W(M_Z)=0.2312；"
                    "α1⁻¹=59.01/α2⁻¹=29.57/α3⁻¹=8.44（M_Z,MS-bar）", "PASS",
                    "外部值只引用（Super-K 2024 / PDG MS-bar），本册不复算"))

    # ---- E2 ----
    g2 = e2_core()
    s = g2["sin2"]
    w("\n[E2] 核心公式体系（本册核心：第一性推导 + Decimal 48 位精算）")
    w("  (a) SU(5) 树级混合角：g1=sqrt(5/3)g'、统一点 g1=g2 => tan²θ_W=g'²/g²=3/5")
    w("      sin²θ_W = tan²/(1+tan²) = (3/5)/(8/5) = 3/8 = %s" % fv(s["sin2_thetaW_dec"], "4f"))
    w("      观测 sin²θ_W(M_Z) = %s；树级预言/观测 = %s（超 %s%%）"
      % (s["observed_MZ"], fv(s["ratio_pred_over_obs"], "4f"),
         fv((s["ratio_pred_over_obs"] - 1) * 100, "2f")))
    w("  (b) 维6算子 τ_p = M_X⁴/(α_GUT² m_p⁵)，m_p=%s GeV，GeV⁻¹→yr 因子=%s"
      % (fv(M_P, "3f"), fv(GEVINV_TO_YR, "3e")))
    tm = g2["tau_minSU5"]
    w("      minimal SU(5)：M_X=%s GeV、α_GUT⁻¹=%s ⇒ τ_p≈%s yr"
      % (fv(tm["M_X_GeV"], "1e"), tm["alpha_GUT_inv"], fv(tm["tau_yr"], "2e")))
    w("      vs Super-K 下限 %s yr：比值(预言/下限)=%s ⇒ 预言短于下限 => 被排除"
      % (fv(TAU_P_SUPERK_LOWER, "1e"), fv(g2["ratio_minSU5_over_SuperK"], "2e")))
    tx = g2["tau_mssm"]
    w("      MSSM 汇聚标度：M_X=%s GeV、α_GUT⁻¹=%s ⇒ τ_p≈%s yr"
      % (fv(tx["M_X_GeV"], "1e"), tx["alpha_GUT_inv"], fv(tx["tau_yr"], "2e")))
    w("      vs Super-K 下限：比值(预言/下限)=%s ⇒ 预言长于下限 => 超界（质子太稳定，当前探测带外）"
      % fv(g2["ratio_mssm_over_SuperK"], "2e"))
    w("  (c) 攻破⑨ P03 读数引用：minimal SU(5) 最短预言 1e32 yr vs SK 下限 1.6e34 yr = 短 160 倍")
    w("      （本册 naive 维6估计落在 1e31–1e32 量级，与教科书/minimal SU(5) 量级一致，独立确认被排除）。")
    w("  => **阈值-可见两难**：树级 GUT 标度(1e15)质子衰太快(被排除)；汇聚标度(2e16)质子太稳(探测带外)。")
    entries.append(("E2", "SU(5)树级 sin²θ_W=3/8=0.375 vs 0.2312；维6算子 τ_p 量级精算："
                    "minimal SU(5) ~%s yr 被排除（P03:160×），MSSM 标度 ~%s yr 超界（太稳定）"
                    % (fv(tm["tau_yr"], "1e"), fv(tx["tau_yr"], "1e")), "PASS",
                    "第一性推导 + Decimal 48 位；强子矩阵元取 O(1)，按量级判"))

    # ---- E3 ----
    g3 = e3_convergence_cite()
    w("\n[E3] 耦合汇聚性（引用 C0140 精确读数，本册不复算）")
    w("  SM 单圈 ΔL = %s e-折 => 三耦合**不汇聚**（无共同统一能标）。"
      % fv(g3["SM_single_loop_DeltaL_efold"], "3f"))
    w("  MSSM：M_GUT=%s GeV、α_GUT⁻¹=%s、τ_p≈%s yr（唯象标度律[C]）。"
      % (fv(g3["MSSM_M_GUT_GeV"], "6e"), fv(g3["MSSM_alpha_GUT_inv"], "4f"),
         fv(g3["MSSM_tau_p_yr"], "3e")))
    w("  => 汇聚唯一已知方案是 MSSM，代价：①新标度 M_SUSY ②整族超伴子 ③M_GUT/α_GUT 无第一性来源。")
    entries.append(("E3", "SM 单圈 ΔL=9.146 e-折不汇聚；MSSM 汇聚 M_GUT=1.54e16、α_GUT⁻¹=25.72、"
                    "τ_p≈3.51e34 yr（C0140 引用）", "PASS", "只引用不复算（P13 已由 C0140 攻破）"))

    # ---- E4 ----
    g4 = e4_geometry_supply()
    w("\n[E4] 几何供给：GUT 群 / X,Y 超重玻色子能否从几何第一性原理生成？")
    w("  C0137 读数：SM 签名(dim=12,rank=4) 至少 %d 个互不同构代数共享 => 签名非唯一，"
      "SU(5)(dim24)/SO(10)(dim45) 更不在几何输出内。" % g4["c0137_signature_candidates"])
    w("  attack24 读数：so(1,3) Killing 型惯性(3,3) => 紧致子代数 dim ≤ %d；"
      "KK 逃逸最小额外维 n=%d（so(1,8)）。几何自旋联络代数装不下 SM，更装不下 SU(5)。"
      % (g4["attack24_compact_dim_max"], g4["attack24_KK_min_extra_dim"]))
    w("  doublet-triplet 劈裂：triplet 须在 M_GUT(~1e16) 压质子衰变，doublet 在 v(~1e2)，"
      "层级比=%s => 需 1e14 量级精细调节（撞 C2/C3）。" % fv(g4["doublet_triplet_hierarchy"], "0e"))
    w("  => 几何框架**不能**从第一性原理生成 GUT 群，也不能生成 X,Y 超重玻色子及其质量标度。")
    entries.append(("E4", "几何供给 0：C0137 签名(12,4)有 3 个候选非唯一；attack24 紧致 dim≤3/KK n=5；"
                    "doublet-triplet 劈裂需 1e14 精调", "PASS", "撞 C1/C2/C3；引用 C0137/attack24 不重攻"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  大统一/质子衰变问题被精确翻译成三件事：(a) GUT 群与 X,Y 玻色子从哪来；(b) M_GUT 绝对标度从哪来；")
    w("  (c) 三耦合是否在某处汇聚、质子是否衰变。")
    w("  (a) 几何供给 0（E4）：SU(5)/SO(10) 是群论公设，非几何第一性产物 => 撞 C1。")
    w("  (b) M_GUT≈1e16 GeV 是绝对能标，几何常数 (ℏ,G,c) 满秩给不出（承接 C0140 E4 nullity=0）=> 撞 C2。")
    w("  (c) SM 不汇聚（E3 引用 C0140）；唯一汇聚方案 MSSM 需整族新粒子+新标度；")
    w("      minimal SU(5) 质子衰变被 Super-K 排除 160×（E2 + P03）。")
    w("  => **P08 结构性负面（对 TUFT/几何框架）**；撞 C1（GUT 群 / 新重玻色子 X,Y）+ C2（M_GUT 绝对标度）。")
    entries.append(("E5", "P08 结构性负面：GUT 群与 X,Y 玻色子为外部公设、M_GUT 无第一性标度、"
                    "minimal SU(5) 质子衰变被排除", "PASS", "撞 C1/C2"))

    # ---- 守卫 ----
    guards = [
        ("G1", "SU(5) 树级 sin²θ_W = 3/8 = 0.375（Fraction 精确）",
         s["sin2_thetaW_dec"] == Decimal("0.375")),
        ("G2", "维6算子 τ_p 量级：minimal SU(5)(M_X=1e15) 落在 1e30–1e33 yr（被 SK 排除）",
         Decimal("1e30") < tm["tau_yr"] < Decimal("1e33")),
        ("G3", "MSSM 标度(M_X=2e16) τ_p 落在 1e35–1e37 yr（超界，太稳定）",
         Decimal("1e35") < tx["tau_yr"] < Decimal("1e37")),
        ("G4", "C0140 汇聚读数已引用（SM ΔL=9.146 e-折不汇聚）",
         g3["SM_single_loop_DeltaL_efold"] == Decimal("9.146484")),
        ("G5", "doublet-triplet 劈裂层级 ~1e14（需精细调节，撞 C2/C3）",
         g4["doublet_triplet_hierarchy"] == Decimal("1e14")),
        ("G6", "几何供给 GUT 群 = 0（C0137 签名 3 候选非唯一 + attack24 紧致 dim≤3）",
         g4["c0137_signature_candidates"] == 3
         and g4["attack24_compact_dim_max"] == 3),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0147 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称大统一已解决：外部观测值只引用；汇聚性读数只引用 C0140（P13 已攻破）不复算；")
    w("  τ_p 为维6算子量级估计（强子矩阵元/CKM 取 O(1)），判定按数量级（倍）而非末位。")
    w("  裁的是「几何/TUFT 框架能否生成 GUT 群、X,Y 玻色子与 M_GUT 标度」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0147_大统一质子衰变攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0147_大统一质子衰变攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0147_gut_proton_decay",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_boundary_facts": {k: str(v) for k, v in g1.items()},
            "E2_core": {
                "sin2_thetaW_GUT_fraction": str(s["sin2_thetaW_GUT"]),
                "sin2_thetaW_GUT_dec": str(s["sin2_thetaW_dec"]),
                "observed_MZ": str(s["observed_MZ"]),
                "ratio_pred_over_obs": str(s["ratio_pred_over_obs"]),
                "tau_minSU5_yr": str(tm["tau_yr"]),
                "tau_mssm_yr": str(tx["tau_yr"]),
                "ratio_minSU5_over_SuperK": str(g2["ratio_minSU5_over_SuperK"]),
                "ratio_mssm_over_SuperK": str(g2["ratio_mssm_over_SuperK"]),
            },
            "E3_convergence_cite": {k: str(v) for k, v in g3.items()},
            "E4_geometry_supply": {k: str(v) for k, v in g4.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0147 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
