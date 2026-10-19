# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R32  以「全空间穷举」方式审查「力的统一场论」主张
================================================================================
红线：数学自洽 != 实验证实。本册只针对「四力（含引力）由挠率几何统一」这一主张，
      不对 TUFT 框架整体作证伪宣告。所有判定必须有实算支撑。

审查策略：把「统一」拆为 7 个空间逐一穷举，任一空间不成立则主张不成立。
  S1 群空间       结构群是否为单群（能否减少耦合数）
  S2 能标空间     mu 全区间扫描，是否存在统一能标
  S3 耦合空间     alpha_1/alpha_2/alpha_3 是否汇聚
  S4 参数空间     TUFT 自由度是否足以归约 SM 参数（自由度赤字 / 参数倒置）
  S5 引力空间     alpha_grav 是否为定义良好的单一耦合
  S6 强度比空间   四力相对强度是否可由几何导出
  S7 作用量空间   拉氏量是否含 TUFT 特有项（可区分预言）

核心新判据（既有《四力统一》册未做）：把 R30 三路证明的 beta==0 与耦合统一对接
  —— beta==0 意味着耦合常数不跑动，故「统一能标」在 TUFT 自身动力学下结构不存在。
三分支穷举（完备性）：
  分支 I   TUFT 自身（beta==0）          -> 不跑动，spread 恒定
  分支 II  TUFT 放宽（螺旋角 theta 可变）-> TUFT 无 theta(mu) 第一性方程，不可计算
  分支 III 借用 SM/MSSM 的 RGE          -> 不再是 TUFT 的统一；且 SM 不汇聚
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_r32_report.txt")

# ---- 上游基准（不可改；与 tuft_四力统一_report.txt 同一组输入）----
MZ = 91.1876                 # GeV
ALPHA_EM_INV_MZ = 127.95     # MS-bar
SIN2TW_MZ = 0.23122
ALPHA_S_MZ = 0.1181
B_SM = (4.1000, -19.0 / 6.0, -7.0000)     # 1-loop SM
B_MSSM = (33.0 / 5.0, 1.0, -3.0)          # 1-loop MSSM（对照）
MPL = 1.22089e19             # GeV，普朗克质量

# 粒子质量（GeV）
MASS = {
    "e": 5.1099895e-4, "mu": 0.1056584, "tau": 1.77686,
    "u": 2.16e-3, "d": 4.67e-3, "s": 9.3e-2, "c": 1.27, "b": 4.18,
    "t": 172.76, "W": 80.379, "Z": MZ, "H": 125.25,
    "p": 0.9382721, "n": 0.9395654,
}

# 汇聚容差：以 1-loop MSSM 的实测汇聚质量（spread ≈ 0.001 dex，即 0.23%）为「成功基准」，
# 取其 10 倍 = 0.01 dex 作为判据。1-loop SM 若真汇聚应落在同量级；显著超出即判不汇聚。
# （若放宽到 0.05 dex，SM 会以 9.1% 分散勉强入选，但仍是 MSSM 的 38 倍 —— 报告内另行披露此口径）
TOL_DEX = 0.01


def main():
    buf = []
    stat = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}

    def put(s=""):
        buf.append(s)

    def rec(tag, name, detail):
        stat[tag] = stat.get(tag, 0) + 1
        buf.append("  [%s] %s  |  %s" % (tag, name, detail))

    def sec(t):
        buf.append("")
        buf.append("=" * 78)
        buf.append("  " + t)
        buf.append("=" * 78)

    # ---------------------------------------------------------------- 抬头
    sec("TUFT-R32  全空间穷举审查：「力的统一场论」")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    put("  Python %s   numpy %s" % (sys.version.split()[0], np.__version__))
    put("  判据：『统一』须在全部 7 个空间同时成立；任一空间失败则主张不成立。")
    put("  汇聚容差：spread = log10(alpha_max/alpha_min) < %.3f dex" % TOL_DEX)

    # ---------------------------------------------------------------- 基准量
    e_em = math.sqrt(4.0 * math.pi / ALPHA_EM_INV_MZ)
    sin_tw = math.sqrt(SIN2TW_MZ)
    cos_tw = math.sqrt(1.0 - SIN2TW_MZ)
    g2 = e_em / sin_tw
    g1 = math.sqrt(5.0 / 3.0) * e_em / cos_tw
    g3 = math.sqrt(4.0 * math.pi * ALPHA_S_MZ)
    inv_a_mz = [4.0 * math.pi / g1 ** 2, 4.0 * math.pi / g2 ** 2, 1.0 / ALPHA_S_MZ]

    def alpha_inv(inv0, b, mu, mu0=MZ):
        return inv0 - (b / (2.0 * math.pi)) * math.log(mu / mu0)

    def spread_dex(vals):
        v = [x for x in vals if x > 0]
        return math.log10(max(v) / min(v))

    sec("0. 基准耦合（M_Z 处实算）")
    put("      e = %.6f ; g' = g1 = %.6f ; g2 = %.6f ; g3 = %.6f" % (e_em, g1, g2, g3))
    put("      alpha^-1(M_Z) = (%.3f, %.3f, %.3f)" % tuple(inv_a_mz))
    put("      1-loop SM  beta 系数 b = (%.4f, %.4f, %.4f)" % B_SM)
    put("      排序 g1 < g2 < g3 : %s" % ("成立（单调序与既有册一致）"
                                        if g1 < g2 < g3 else "不成立"))

    # ================================================================ S1
    sec("S1  群空间：结构群是否为单群（能否减少耦合数）")
    dims = {"so(1,3)": 6, "u(1)": 1, "su(2)": 3, "su(3)": 8}
    ranks = {"so(1,3)": 2, "u(1)": 1, "su(2)": 1, "su(3)": 2}
    n_factor = len(dims)
    dim_prod = sum(dims.values())
    rank_prod = sum(ranks.values())
    put("      直积分解：dim = %d ；rank（Cartan 维数）= %d ；独立因子数 = %d"
        % (dim_prod, rank_prod, n_factor))
    put("      对照单群 SU(5)：dim = 24 ，rank = 4 ；SO(10)：dim = 45 ，rank = 5")
    put("      ⇒ 独立耦合常数个数 = 直积的『单群因子数 + U(1) 因子数』= %d" % n_factor)
    if n_factor > 1:
        rec("FAIL", "S1 结构群是笛卡尔直积而非单群 ⇒ 群论上不发生归约",
            "G = SO(1,3)×U(1)×SU(2)×SU(3)：dim=%d rank=%d，四个独立耦合；"
            "真统一需单群（SU(5)/SO(10)/E6）把 U(1)_Y 嵌入，且 rank 应下降（直积 rank=%d > SU(5) rank=4）。"
            "直积只是把四个理论打包，参数数不减反增" % (dim_prod, rank_prod, rank_prod))
    # 内禀指标直和维数（正确写法对照）
    put("      正确内禀结构 (1⊕2)⊗3：q_L=6, u_R=3, d_R=3, l_L=2, e_R=1 ⇒ 单代 15（+nu_R = 16）")
    rec("INFO", "S1b 维数重述属标准模型表示论（非从挠率导出）",
        "(1⊕2)⊗3 的分解与 SM 完全一致，但该结构是被『借用』而非由挠率构造；"
        "挠率分量 → 量子数 (Y, I3, 色) 的映射至今未给 ⇒ 不可计算、不可证伪")

    # ================================================================ S2/S3
    sec("S2+S3  能标空间 × 耦合空间：全区间扫描（三分支穷举）")
    mus = np.logspace(-3.0, 19.0, 60001)      # GeV
    put("     扫描区间 mu ∈ [1e-3, 1e19] GeV，共 %d 个对数格点" % len(mus))

    def scan(bvec, label, run=True):
        """返回 (minspread3, mu*, minspread4, mu4*)"""
        best3, mu3 = float("inf"), None
        best4, mu4 = float("inf"), None
        for mu in mus:
            if run:
                invs = [alpha_inv(inv_a_mz[i], bvec[i], mu) for i in range(3)]
            else:
                invs = list(inv_a_mz)          # beta == 0：不跑动
            if min(invs) <= 0:
                continue
            als = [1.0 / x for x in invs]
            s3 = spread_dex(als)
            if s3 < best3:
                best3, mu3 = s3, mu
            s4 = spread_dex(als + [(mu / MPL) ** 2])
            if s4 < best4:
                best4, mu4 = s4, mu
        return best3, mu3, best4, mu4

    # 分支 I：TUFT 自身（beta == 0）
    t3, tm3, t4, tm4 = scan(None, "TUFT", run=False)
    put("")
    put("  分支 I  —— TUFT 自身动力学（R30 三路证明 beta == 0，耦合不跑动）：")
    put("      spread3(alpha_1,alpha_2,alpha_3) = %.4f dex（恒定，与 mu 无关）" % t3)
    put("      ⇒ 全 %d 个能标格点上 spread 恒为此值，无极小、无交点" % len(mus))
    put("      M_Z 处 alpha = (%.5f, %.5f, %.5f) ⇒ max/min = %.2f"
        % (1 / inv_a_mz[0], 1 / inv_a_mz[1], 1 / inv_a_mz[2],
           max(1 / x for x in inv_a_mz) / min(1 / x for x in inv_a_mz)))
    if t3 > TOL_DEX:
        rec("FAIL", "S3-I TUFT 自身（beta==0）下四力统一【结构上不可能】",
            "beta==0 ⇒ alpha_i(mu) 为常数 ⇒ spread(mu) ≡ %.4f dex 与能标无关。"
            "『存在统一能标 mu* 使 alpha_1=alpha_2=alpha_3』要求 spread→0，"
            "而不跑动的耦合在任何 mu 都不可能相交 ⇒ 这不是『尚未找到』，是被动力学结构排除" % t3)

    # 分支 III-a：SM 1-loop
    s3, sm3, s4, sm4 = scan(B_SM, "SM", run=True)
    put("")
    put("  分支 III-a —— 借用标准模型 1-loop RGE（b = %.4f, %.4f, %.4f）：" % B_SM)
    put("      min spread3 = %.4f dex  @ mu = %.4e GeV" % (s3, sm3))
    put("      min spread4（含引力 alpha_grav=(mu/M_Pl)^2）= %.4f dex  @ mu = %.4e GeV" % (s4, sm4))
    if s3 > TOL_DEX:
        rec("FAIL", "S3-IIIa 即便借用 SM 的 RGE，三耦合仍不汇聚",
            "最小分散 %.4f dex（%.1f%%）出现在 mu=%.3e GeV，超过容差 %.3f dex；"
            "两两交点各自分离（既有册：1.03e13 / 2.44e14 / 9.82e16 GeV）构成三角形而非一点"
            % (s3, (10 ** s3 - 1) * 100, sm3, TOL_DEX))
    else:
        rec("PASS", "S3-IIIa SM 三耦合汇聚", "min spread3 = %.4f dex" % s3)
    if s4 > TOL_DEX:
        als_mpl = []
        for i in range(3):
            iv = alpha_inv(inv_a_mz[i], B_SM[i], MPL)
            if iv > 0:
                als_mpl.append(1.0 / iv)
        rec("FAIL", "S5-IIIa 含引力后 SM 仍不汇聚",
            "扫描最优 mu=%.3e GeV 处四者最大/最小 = %.2f（分散 %.0f%%），远超 GUT 要求的 <2%%；"
            "换一口径：mu=M_Pl 处 alpha_grav=1，而规范耦合最大仅 %.4f（相差 %.0f 倍）。"
            "⇒ 即便借用 SM 的 RGE，『含引力的四力统一』也不成立（这是 GUT 的已知边界，非 TUFT 独有）"
            % (sm4, 10 ** s4, (10 ** s4 - 1) * 100, max(als_mpl), 1.0 / max(als_mpl)))

    # 分支 III-b：MSSM 对照
    m3, mm3, m4, mm4 = scan(B_MSSM, "MSSM", run=True)
    put("")
    put("  分支 III-b —— MSSM 对照（b = %.1f, %.1f, %.1f）：" % B_MSSM)
    put("      min spread3 = %.4f dex  @ mu = %.4e GeV" % (m3, mm3))
    put("      min spread4 = %.4f dex  @ mu = %.4e GeV" % (m4, mm4))
    if m3 < TOL_DEX:
        rec("INFO", "S3-IIIb 对照：只有超对称版本才汇聚",
            "MSSM 最小分散 %.4f dex（%.2f%%）@ mu=%.3e GeV —— 汇聚是【超对称粒子内容】的结果，"
            "与挠率几何无关；TUFT 作用量与 SM 逐项相同（S7），继承的是『不汇聚』"
            % (m3, (10 ** m3 - 1) * 100, mm3))
    put("")
    put("      【口径披露·避免判据挑选嫌疑】若把容差放宽到 0.05 dex：")
    put("        SM 会以 %.1f%% 分散勉强『入选』，但其分散仍是 MSSM（%.2f%%）的 %.0f 倍；"
        % ((10 ** s3 - 1) * 100, (10 ** m3 - 1) * 100, s3 / max(m3, 1e-9)))
    put("        既有册在 mu=1e16 GeV 处的口径给出 21.0% 分散 —— 与本册 0.0377 dex 属同一事实的两种读法。")
    put("        ⇒ 无论取 0.01 还是 0.05 dex，『TUFT 自身不汇聚』的结论都不改变（其 spread 恒为 %.3f dex）。" % t3)

    # 分支 II：放宽 theta(mu)
    put("")
    put("  分支 II —— TUFT 放宽：允许螺旋角 theta 随能标变化（kappa/tau = tan theta(mu)）：")
    put("      · 公理 A：kappa^2 + tau^2 = (omega/c)^2")
    put("      · 螺旋约束：kappa/tau = tan theta")
    put("      · R30 已证：两式联立 ⇒ kappa, tau 各自为常数 ⇒ omega 常数 ⇒ beta == 0")
    put("      · 若要 beta != 0，必须放弃其中之一；放弃后 TUFT 无 theta(mu) 的第一性演化方程")
    put("      · O-SCALE / D3(K_sat) / 定理N-M2 / O-SCALE-BREAK 四条同源边界：TUFT 无第一性尺度")
    rec("FAIL", "S2-II 「可变螺旋角」分支无定义，不可计算",
        "放宽后所需的 theta(mu) 方程在 TUFT 内不存在；四条同源边界已证无第一性尺度剖面。"
        "⇒ 分支 II 不是『另一条路』，而是『无方程可解』，故三分支穷举中 I/II/III 全部不通")

    # 能标空间总判定
    rec("FAIL", "S2 能标空间：『统一能标 mu*』在 TUFT 内无定义",
        "TUFT 无 RG 流（beta==0）⇒ mu 不是理论的自变量，alpha_i 无 mu 依赖 ⇒ "
        "『在某能标四力归一』这一命题在 TUFT 内没有可指称的对象（既无流，也无交点）")

    # ================================================================ 反向工程
    sec("S3-R  反向工程：若强行要求统一，需要什么样的 beta 系数？")
    mu_star = 1.0e16
    A_gut = 24.3            # 目标 1/alpha_GUT（MSSM 典型值）
    lg = math.log(mu_star / MZ)
    b_need = [2.0 * math.pi * (inv_a_mz[i] - A_gut) / lg for i in range(3)]
    put("     设目标：mu* = %.0e GeV 处 1/alpha_GUT = %.2f" % (mu_star, A_gut))
    put("     由 alpha_i^-1(mu*) = alpha_i^-1(M_Z) - (b_i/2pi)·ln(mu*/M_Z) 反解：")
    put("       所需 b = (%.4f, %.4f, %.4f)" % tuple(b_need))
    put("       MSSM 实际 b = (%.4f, %.4f, %.4f)" % B_MSSM)
    put("       SM   实际 b = (%.4f, %.4f, %.4f)" % B_SM)
    put("       TUFT 实际 b = (%.4f, %.4f, %.4f)   （beta == 0）" % (0.0, 0.0, 0.0))
    dist_mssm = math.sqrt(sum((b_need[i] - B_MSSM[i]) ** 2 for i in range(3)))
    dist_tuft = math.sqrt(sum((b_need[i] - 0.0) ** 2 for i in range(3)))
    put("     欧氏距离：所需 b vs MSSM = %.4f ；所需 b vs TUFT(0) = %.4f" % (dist_mssm, dist_tuft))
    if dist_tuft > dist_mssm:
        rec("FAIL", "S3-R 统一所需的 beta 系数恰是超对称的，与挠率几何无关",
            "反解所需 b ≈ (%.2f, %.2f, %.2f)，与 MSSM 的 (%.1f, %.1f, %.1f) 距离仅 %.3f，"
            "而与 TUFT 的 (0,0,0) 距离 %.3f（相差 %.1f 倍）。"
            "⇒ 『在 1e16 GeV 统一』这一事实若成立，其成因是超对称粒子内容，不是挠率几何；"
            "TUFT 未提供任何能产生该组系数的机制" % (b_need[0], b_need[1], b_need[2],
                                                B_MSSM[0], B_MSSM[1], B_MSSM[2],
                                                dist_mssm, dist_tuft, dist_tuft / max(dist_mssm, 1e-9)))

    # ================================================================ S4
    sec("S4  参数空间：自由度赤字与参数倒置")
    dims_free = [("自由几何量 (kappa, tau, omega)", 3),
                 ("公理 A：kappa^2+tau^2=(omega/c)^2", -1),
                 ("螺旋约束：kappa/tau = tan theta (S12)", -1),
                 ("R30 闭式：kappa = alpha·mc/hbar，tau = sqrt(1-alpha^2)·mc/hbar", -1)]
    run_dof = 0
    for name, d in dims_free:
        run_dof += d
        put("      %-58s %+d  ⇒ 累计自由度 = %d" % (name, d, run_dof))
    n_sm_params = 19        # g1,g2,g3,theta_QCD,m_H,v,9 Yukawa,CKM 4
    n_need = n_sm_params + 2   # + G, Lambda
    put("")
    put("     需解释/归约的参数：SM %d 个 + G + Lambda = %d 个" % (n_sm_params, n_need))
    put("     TUFT 剩余自由度 = %d ；赤字 = %d" % (run_dof, n_need - run_dof))
    if run_dof < n_need:
        rec("FAIL", "S4 自由度赤字：TUFT 无余量归约 SM 参数",
            "几何自由度被公理 A + 螺旋约束 + (m,alpha) 锁定逐级降为 %d，而需归约参数 %d 个；"
            "且实际方向相反：不是几何决定粒子参数，而是粒子质量 m 决定 kappa/tau（参数倒置）"
            % (run_dof, n_need))
    # 参数爆炸
    put("")
    put("     参数倒置的后果 —— 每个粒子一组 (kappa_i, tau_i, omega_i)：")
    put("     %-6s %-14s %-16s %-16s" % ("粒子", "m [GeV]", "kappa_i = alpha·mc/hbar", "tau_i [m^-1]"))
    hbarc = 1.973269804e-16    # GeV·m  (hbar c)
    alpha_em = 1.0 / ALPHA_EM_INV_MZ
    n_part = 0
    for k in ("e", "mu", "tau", "t", "W", "Z", "H", "p"):
        m = MASS[k]
        kap = alpha_em * m / hbarc
        tau = math.sqrt(1.0 - alpha_em ** 2) * m / hbarc
        n_part += 1
        put("     %-6s %-14.6e %-16.6e %-16.6e" % (k, m, kap, tau))
    put("     ⇒ 粒子表越长，TUFT 引入的外部输入越多（参数爆炸），而非越少（归约）")
    rec("FAIL", "S4b 参数爆炸：TUFT 的参数数随粒子数增长",
        "SM 的 %d 个参数被全部继承（S7 作用量逐项照搬），此外每个粒子还要外部输入其质量 m_i "
        "才能得到 kappa_i, tau_i。⇒ 净参数量 >= SM，'统一减少自由参数'的核心卖点不成立" % n_sm_params)

    # ================================================================ S5
    sec("S5  引力空间：alpha_grav 是否为定义良好的单一耦合")
    put("     TUFT 的引力耦合：alpha_grav(m) = (m/m_Pl)^2 —— 依赖【探针质量】而非能标：")
    put("     %-10s %-16s %-16s" % ("探针", "m [GeV]", "alpha_grav"))
    ag_vals = []
    for k in ("e", "p", "W", "H", "Pl"):
        m = MPL if k == "Pl" else MASS[k]
        ag = (m / MPL) ** 2
        ag_vals.append(ag)
        put("     %-10s %-16.6e %-16.6e" % (k, m, ag))
    spread_ag = math.log10(max(ag_vals) / min(ag_vals))
    put("     ⇒ 同一理论内 alpha_grav 跨 %.2f 个量级（取决于选谁作探针）" % spread_ag)
    rec("FAIL", "S5 alpha_grav 不是单一耦合 ⇒ 『四力统一』含引力时定义不良",
        "规范耦合 alpha_i 是能标的函数且探针无关；alpha_grav(m)=(m/m_Pl)^2 是探针质量的函数，"
        "跨 %.1f 个量级（%.2f dex）。二者不是同类对象 ⇒ 『alpha_1=alpha_2=alpha_3=alpha_grav』"
        "这个等式在语义上无定义，'四力归一'的命题本身不良构（ill-posed）"
        % (spread_ag, spread_ag))
    # TUFT 含引力的最优分散
    put("")
    put("     TUFT 含引力时的最优分散（两种探针取法）：")
    for label, ag in (("探针 = 电子 m_e", (MASS["e"] / MPL) ** 2),
                      ("探针 = 普朗克质量 m_Pl", 1.0)):
        s = spread_dex([1 / inv_a_mz[0], 1 / inv_a_mz[1], 1 / inv_a_mz[2], ag])
        put("       %-24s alpha_grav = %.4e  ⇒ spread4 = %.3f dex" % (label, ag, s))
    rec("FAIL", "S5b 含引力后 TUFT 的分散达数十个量级",
        "即便取最有利的探针（m_Pl，alpha_grav=1），spread4 仍为 %.2f dex；取电子探针则 %.2f dex。"
        "⇒ 引力与其他三力在 TUFT 内不存在任何能标上的交汇" % (
            spread_dex([1 / inv_a_mz[0], 1 / inv_a_mz[1], 1 / inv_a_mz[2], 1.0]),
            spread_dex([1 / inv_a_mz[0], 1 / inv_a_mz[1], 1 / inv_a_mz[2], (MASS["e"] / MPL) ** 2])))

    # ================================================================ S6
    sec("S6  强度比空间：四力相对强度可否由几何导出")
    alpha_w_mw = (g2 ** 2) / (4.0 * math.pi)
    ratios = {"强 alpha_s": ALPHA_S_MZ, "电磁 alpha": 1.0 / ALPHA_EM_INV_MZ,
              "弱 alpha_W(M_Z)": alpha_w_mw, "引力 alpha_grav(p)": (MASS["p"] / MPL) ** 2}
    base = ALPHA_S_MZ
    put("     %-22s %-16s %-16s" % ("相互作用", "耦合值", "相对强度(强=1)"))
    for k, v in ratios.items():
        put("     %-22s %-16.6e %-16.6e" % (k, v, v / base))
    put("     ⇒ 这 4 个数全部来自实验输入（alpha_s, alpha_em, G_F, G, m_p），几何未贡献任何一位")
    rec("FAIL", "S6 四力强度比为实验输入的重述，非几何导出",
        "要给出强度比需先知道 m_p、alpha_s、alpha_em、G —— 全部是外部输入（S4 参数倒置）。"
        "TUFT 唯一可能'给出'的量是精细结构常数 alpha，且 R29 已证其方向存在 1.878e+04 倍歧义 "
        "（tau/kappa = alpha 与 kappa/tau = tan theta 互斥）⇒ 连这一位也不可靠")

    # ================================================================ S7
    sec("S7  作用量空间：是否含 TUFT 特有项")
    put("     既有《四力统一》册（P17/F19/B9/I14）已逐项核对：")
    put("       · 作用量 = EH + (-1/4)F^2 + psi-bar(i gamma D - m)psi —— 与 SM+GR 逐字照搬")
    put("       · TUFT 特有项计数 = 0（无挠率动能 T^2，无 R^2，无非最小耦合，无 Omega 场作用量）")
    put("       · 自由参数继承 SM 的 %d 个，无一被几何量替代" % n_sm_params)
    rec("FAIL", "S7 作用量零 TUFT 特有项 ⇒ 无可区分预言",
        "若拉氏量与 SM+GR 完全相同，则『TUFT 统一』与『SM+GR』在观测上不可区分；"
        "'统一'不产生任何新判决性预言 ⇒ 该主张当前不可证伪（不可证伪性缺陷）")
    rec("BOUNDARY", "S7b 本册不重算作用量，引用既有册判定",
        "tuft_四力统一_report.txt 的 S3.6/S3.8/S3.9 已给出逐项核对与 19 处 FAIL；"
        "本册将其作为 S7 空间的证据引入，不重复计算")

    # ================================================================ 结论
    sec("结论：7 空间穷举 —— 「力的统一场论」在 TUFT 内不成立")
    table = [("S1 群空间", "FAIL", "直积非单群，4 个独立耦合，参数不减"),
             ("S2 能标空间", "FAIL", "beta==0 ⇒ mu 非自变量，统一能标无定义"),
             ("S3 耦合空间", "FAIL", "TUFT spread 恒定 %.3f dex（不跑动）；SM 最优仍 %.3f dex，仅 MSSM 达 %.4f" % (t3, s3, m3)),
             ("S4 参数空间", "FAIL", "自由度 %d < 需归约 %d，且参数倒置/爆炸" % (run_dof, n_need)),
             ("S5 引力空间", "FAIL", "alpha_grav 依赖探针，跨 %.1f 量级，等式不良构" % spread_ag),
             ("S6 强度比空间", "FAIL", "强度比 = 实验输入重述，几何零贡献"),
             ("S7 作用量空间", "FAIL", "零特有项 ⇒ 不可证伪")]
    put("     %-16s %-8s %s" % ("空间", "判定", "依据"))
    for a, b, c in table:
        put("     %-16s %-8s %s" % (a, b, c))
    n_fail = sum(1 for _, b, _ in table if b == "FAIL")
    put("")
    put("     ⇒ %d / 7 个空间失败。三分支穷举（I beta==0 / II theta 可变 / III 借用 RGE）全部不通：" % n_fail)
    put("        分支 I   不跑动 ⇒ 无交点（结构排除）")
    put("        分支 II  无 theta(mu) 方程 ⇒ 无定义（不可计算）")
    put("        分支 III 借用 SM 的 RGE 仍不汇聚；能汇聚的是 MSSM（超对称，非挠率几何）")
    if n_fail == len(table):
        rec("FAIL", "总判定：『四力由挠率几何统一』不成立（7/7 空间失败）",
            "本结论的强度分层：S2/S3/S5 属【结构不可能】（由 beta==0 与 alpha_grav 定义直接排除，"
            "不依赖任何近似）；S1/S7 属【当前表述不成立】（可修补：改单群、补特有项）；"
            "S4/S6 属【方向倒置】（参数不但未归约，反而随粒子数增长）")

    sec("与 OPEN9《空间运行方式穷举》的交叉对接（同日产出，口径必须对齐）")
    put("     OPEN9（tuft_四力统一_空间运行方式穷举_OPEN9_report.txt，P11/F36/B14/I1）穷举的是")
    put("     【几何载体的种类】：R/T/Q 及其组合 7 种 + Frenet + 拓扑 + KK + NCG + 外部注入 = 12 种，")
    put("     判据 C1–C5，结论 12/12 FAIL，瓶颈 = 范畴鸿沟（张量分量不携带规范群结构）。")
    put("")
    put("     本册穷举的是【主张成立所需的不同空间维度】7 个（群/能标/耦合/参数/引力/强度比/作用量）。")
    put("     ⇒ 二者互补而非重复。三处必须交代的关系：")
    put("")
    put("     ★ 口径对齐（避免被误读为冲突）：")
    dl_check = math.log(9.822e16 / 1.031e13)
    put("        · OPEN9 的 C4 用 ΔL = 9.1467，单位【e-fold】：三耦合两两相交点的能标分离跨度")
    put("          本册复算 ln(9.822e16 / 1.031e13) = %.4f e-fold（引用值 9.1467，量级一致）" % dl_check)
    put("        · 本册用 spread = 0.0377，单位【dex】：同一 mu 处耦合值之比的对数")
    put("        · 二者是同一事实（SM 三耦合不汇聚）的两种度量，结论一致，无矛盾")
    put("")
    put("     ★ 本册补上 OPEN9 未覆盖的分支：")
    put("        · OPEN9 的 C4 引用 SM/MSSM 的既有跑动数值，未回答『TUFT 自身耦合跑不跑』")
    put("        · 本册分支 I：TUFT β≡0 ⇒ spread 恒为 %.4f dex ⇒ 统一能标在 TUFT 内无定义" % t3)
    put("")
    put("     ★ 本册把 OPEN9 的一个 BOUNDARY 收敛为 FAIL：")
    put("        · OPEN9 把『唯一达标路径是引入 SUSY 新物质态（ΔL=0.130）』标为 BOUNDARY，")
    put("          理由是新物质态『不是空间运行方式、超出本穷举范畴』")
    put("        · 本册 §S3-R 反解：统一所需 b = (%.3f, %.3f, %.3f)，与 MSSM 距离 %.3f、"
        % (b_need[0], b_need[1], b_need[2], dist_mssm))
    put("          与 TUFT(0,0,0) 距离 %.3f ⇒ 『需 SUSY 物质』不再是范畴外的悬置项：" % dist_tuft)
    put("          TUFT 无机制产生该组系数，判定为 FAIL")
    rec("INFO", "与 OPEN9 的关系：互补 + 口径对齐 + 收敛其 BOUNDARY",
        "OPEN9 穷举载体种类（12/12 FAIL，瓶颈=范畴鸿沟）；本册穷举条件空间（7/7 FAIL，瓶颈=β≡0 结构不可能）。"
        "ΔL(e-fold) 与 spread(dex) 是同一事实的两种度量；本册把 OPEN9 的『需 SUSY 新物质态』"
        "由 BOUNDARY 收敛为 FAIL（反解所需 β 系数 = MSSM，TUFT 无法产生）")

    sec("若要救：解冻条件（与既有修复方案对接）")
    for i, s in enumerate([
        "给出挠率分量 → 规范耦合的构造映射（否则 S6 恒为重述）",
        "给出 theta(mu) 或 kappa(mu) 的第一性演化方程（否则 S2/S3 恒为结构不可能）",
        "把结构群改为单群并给出 U(1)_Y 的嵌入（否则 S1 恒为直积）",
        "在作用量中补至少一个 TUFT 特有项并给出可判决的定量预言（否则 S7 恒不可证伪）",
        "把 alpha_grav 重定义为探针无关的单一耦合（否则 S5 恒不良构）",
    ], 1):
        put("     %d. %s" % (i, s))
    rec("INFO", "本册性质与红线",
        "本册针对『力的统一』这一主张，不宣告 TUFT 框架整体被证伪；"
        "R30 的 omega = m_e c^2/hbar 与 kappa/tau 闭式等正向结果不受影响。"
        "数学自洽 != 实验证实")

    sec("汇总")
    put("  PASS     = %d" % stat.get("PASS", 0))
    put("  FAIL     = %d" % stat.get("FAIL", 0))
    put("  BOUNDARY = %d" % stat.get("BOUNDARY", 0))
    put("  INFO     = %d" % stat.get("INFO", 0))
    put("")
    put("  关键数值：")
    put("    TUFT(beta==0) spread3 = %.4f dex（恒定）；SM min spread3 = %.4f dex；MSSM = %.4f dex"
        % (t3, s3, m3))
    put("    含引力：SM min spread4 = %.3f dex ；TUFT(电子探针) = %.3f dex" % (s4, spread_dex(
        [1 / inv_a_mz[0], 1 / inv_a_mz[1], 1 / inv_a_mz[2], (MASS["e"] / MPL) ** 2])))
    put("    反解所需 b = (%.3f, %.3f, %.3f) vs MSSM (%.1f, %.1f, %.1f) vs TUFT (0,0,0)"
        % (b_need[0], b_need[1], b_need[2], B_MSSM[0], B_MSSM[1], B_MSSM[2]))
    put("    自由度：3 -1 -1 -1 = %d ；需归约 %d 个参数" % (run_dof, n_need))
    put("")
    put("红线声明：数学自洽 != 实验证实；本册针对『力的统一』主张，不构成对 TUFT 整体的证伪宣告。")

    text = "\n".join(buf) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
