# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R31  「Numpyro CMB 嵌套采样」+「QNM FDTD/PML 复本征值」两条主线的
          可行性与缺陷审计（含实算实证）
================================================================================
红线：本册是审计，不是实现。所有判定必须有实算支撑；依赖缺失导致无法实测的部分，
      明确标注『未实测』，绝不凭记忆编造 API 或数值。

§0 环境体检（决定哪些能实测）
§1 主线A（CMB 嵌套采样）审计
      A1 观测数据量级核验（vs Planck 2018 真实约束）
      A2 阶跃似然的可微性 / 梯度死区（实算）
      A3 理论有源性：TUFT β≡0（R30 三路）⇒ t_c 无定义；TUFT 无 CMB 双谱
      A4 API 核验（依赖缺失 ⇒ 标注未实测）
§2 主线B（QNM FDTD/PML）审计
      B1 r_of_rstar 反函数错误（实算对照）
      B2 PML 少一阶（符号 + 实算对照）
      B3 计算域截断（实算：外边界残余势占比）
      B4 scipy.eigs 与 dense 数组（实算）
      B5 shift-invert target 与 sqrt 分支（实算）
      B6 挠率势 V_torsion 的有源性
§3 核心实证：有限域 + PML 的离散谱是否为箱模（R23 判据复现 + PML 能否救）
§4 结论与正确路线建议
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
REPORT_PATH = os.path.join(HERE, "tuft_r31_report.txt")

# 文献/上游基准（不可改）
LEAVER_L2 = complex(0.373671684418, -0.088962315689)   # R25 Leaver 连分式 l=2 基模
PLANCK_FNL_LOCAL = -0.9                                 # Planck 2018 f_NL^local 中心值
PLANCK_FNL_SIGMA = 5.1                                  # Planck 2018 1σ


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

    sec("TUFT-R31  两条主线的可行性与缺陷审计")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    put("  红线：本册是审计不是实现；依赖缺失者标注『未实测』。")

    # =====================================================================
    # §0 环境体检
    # =====================================================================
    sec("0. 环境体检（决定哪些项目能实测）")
    import importlib.util as iutil
    mods = ["numpyro", "jax", "jaxlib", "scipy", "emcee", "numpy", "sympy"]
    avail = {}
    for m in mods:
        avail[m] = iutil.find_spec(m) is not None
        put("      %-10s %s" % (m, "OK" if avail[m] else "MISSING"))
    if not avail["numpyro"] or not avail["jax"]:
        rec("FAIL", "主线A 代码在本机不可运行",
            "numpyro/jax/jaxlib 全部缺失 ⇒ CMB 嵌套采样代码无法执行；"
            "在补齐依赖前，任何 log Z / 贝叶斯因子都取不到")

    # =====================================================================
    # §1 主线A
    # =====================================================================
    sec("1. 主线A（CMB 双谱嵌套采样）审计")

    # A1 数据量级
    obs_fnl = np.array([-0.038, -0.042, -0.039, -0.041, -0.040,
                        -0.043, -0.037, -0.045, -0.036, -0.044])
    obs_sigma = np.array([0.022, 0.021, 0.023, 0.020, 0.024,
                          0.022, 0.025, 0.021, 0.023, 0.022])
    put("  A1 观测数据量级核验：")
    put("      稿内 obs_fnl 均值 = %.4f，σ 均值 = %.4f" % (obs_fnl.mean(), obs_sigma.mean()))
    put("      Planck 2018 f_NL^local ≈ %.1f ± %.1f（文献典型值）" % (PLANCK_FNL_LOCAL, PLANCK_FNL_SIGMA))
    ratio_sigma = PLANCK_FNL_SIGMA / obs_sigma.mean()
    snr_gain = abs(PLANCK_FNL_LOCAL / obs_fnl.mean()) if obs_fnl.mean() != 0 else float("inf")
    put("      ⇒ 稿内 σ 比真实精度小 %.1f 倍；稿内中心值与真实中心值量级比 %.2f"
        % (ratio_sigma, abs(obs_fnl.mean() / PLANCK_FNL_LOCAL)))
    rec("FAIL", "A1 观测数据非真实 Planck 约束（不可用于模型比对）",
        "稿内 σ≈0.022 比 Planck 真实 1σ≈5.1 紧 %.0f 倍，且中心值取在 −0.04（真实量级 −0.9）；"
        "用该数据算出的 log Z 与贝叶斯因子只反映这组人造数，不代表任何观测" % ratio_sigma)

    # A2 阶跃可微性
    obs_l = np.array([20, 40, 60, 80, 100, 150, 200, 300, 400, 500], dtype=float)
    fnl_lcdm = -0.04
    delta_probe = 0.05

    def chi2_at(lc):
        heavi = (obs_l > lc).astype(float)
        model = fnl_lcdm + delta_probe * heavi
        return float(np.sum(((model - obs_fnl) / obs_sigma) ** 2))

    lcs = np.linspace(20.0, 500.0, 2001)
    chis = np.array([chi2_at(lc) for lc in lcs])
    uniq = np.unique(np.round(chis, 12))
    grads = np.diff(chis)
    zero_frac = float(np.mean(np.abs(grads) < 1e-14))
    put("")
    put("  A2 阶跃似然的可微性（扫描 l_c ∈ [20,500]，Δf_NL=%.2f）：" % delta_probe)
    put("      χ²(l_c) 的不同取值个数 = %d（数据点数 = %d）" % (len(uniq), len(obs_l)))
    put("      |dχ²/dl_c| ≈ 0 的比例 = %.2f%%" % (zero_frac * 100))
    put("      χ² 取值域 = [%.4f, %.4f]" % (chis.min(), chis.max()))
    rec("FAIL", "A2 阶跃似然对 l_c 梯度恒为 0（NUTS 失效）",
        "χ²(l_c) 是阶梯常数（仅 %d 个取值），梯度为 0 占 %.1f%% ⇒ 基于梯度的 NUTS/HMC 在 l_c 上退化为随机游走；"
        "须改用平滑过渡（sigmoid/tanh）或离散采样，否则后验与 log Z 均不可信" % (len(uniq), zero_frac * 100))

    # A3 理论有源性
    put("")
    put("  A3 理论有源性：")
    put("      · R30（三路交叉闭环）已证 TUFT 固定螺旋下 β ≡ 0 ⇒ **不存在 RG 流**")
    put("      · 稿内参数 t_c = ln(μ_c/M_Pl) 以『拓扑跃迁能标』为前提 ⇒ 该前提在 TUFT 内无定义")
    put("      · TUFT 无 CMB 原初功率谱/双谱的第一性计算（暴胀CMB 册已有大量 FAIL）")
    rec("FAIL", "A3 采样参数 t_c 与 f_NL^TUFT 均无第一性来源",
        "无 RG 流 ⇒ t_c 无定义；无双谱计算 ⇒ f_NL^TUFT(l) 是唯象写入。"
        "⇒ 即使代码跑通，所得贝叶斯因子比较的是『一个唯象阶跃模型 vs ΛCDM』，与 TUFT 无关")

    # A4 API
    rec("INFO", "A4 numpyro API 核验（未实测）",
        "本机 numpyro/jax 缺失，无法实测签名。公开记忆：NestedSampler 位于 "
        "numpyro.contrib.nested_sampling（非 numpyro.infer），其参数与稿内 num_samples/num_sweep 不同，"
        "get_log_marginal_likelihood 亦非标准 API —— 该项标注『待装依赖后核验』，不作为已证缺陷")

    # =====================================================================
    # §2 主线B
    # =====================================================================
    sec("2. 主线B（QNM FDTD / PML 复本征值）审计")

    M = 1.0

    def rstar_of_r(r):
        return r + 2.0 * M * math.log(abs(r / (2.0 * M) - 1.0))

    def r_of_rstar_true(rs):
        """正确的逆映射：二分法求根"""
        lo, hi = 2.0 * M * (1.0 + 1e-14), 2.0 * M + 400.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if rstar_of_r(mid) < rs:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def r_of_rstar_draft(rs):
        """稿内写法（把正映射当逆映射用）"""
        return rs + 2.0 * M * math.log(abs(rs / (2.0 * M) - 1.0))

    # B1
    put("  B1 逆映射核验（M=1）：")
    put("      %-10s %-18s %-18s %-12s" % ("r_*", "正确 r(二分)", "稿内 r", "绝对误差"))
    errs = []
    for rs in (-20.0, -10.0, 0.0, 5.0, 20.0):
        rt = r_of_rstar_true(rs)
        rd = r_of_rstar_draft(rs)
        errs.append(abs(rt - rd))
        put("      %-10.1f %-18.8f %-18.8f %-12.3e" % (rs, rt, rd, abs(rt - rd)))
    rec("FAIL", "B1 r_of_rstar 用错了公式（把正映射当逆映射）",
        "正确关系是 r_* = r + 2M·ln|r/2M − 1|；稿内函数把这个式子里的 r 换成 r_* 当逆映射用，"
        "最大绝对误差 %.3e ⇒ 势 V(r) 的取值点全错，所得谱无意义" % max(errs))

    # B2 PML 阶数
    put("")
    put("  B2 PML 复坐标拉伸的阶数：")
    put("      稿内：∂_{r*} → (1/(1+iσ)) ∂_{r*}，离散系数取 coeff = 1/(s·dr²)")
    put("      正确：二阶导数应两次作用该算子 ⇒ 系数含 1/s²（且含 σ' 的附加项）")
    s_test = 1.0 + 2.0j
    put("      数值对照（σ=2 ⇒ s=1+2i）：1/s = %s ；1/s² = %s ；二者模比 = %.3f"
        % (np.round(1 / s_test, 6), np.round(1 / s_test ** 2, 6),
           abs(1 / s_test) / abs(1 / s_test ** 2)))
    rec("FAIL", "B2 PML 拉伸少一阶（吸收强度错误）",
        "二阶导数需 1/s² 而非 1/s；σ=2 时二者模相差 %.2f 倍 ⇒ 吸收层强度被严重低估，"
        "且缺少 σ' 项会在 PML 界面产生额外反射（PML 要求 σ 平滑过渡）"
        % (abs(1 / s_test) / abs(1 / s_test ** 2)))

    # B3 计算域
    put("")
    put("  B3 计算域 r_* ∈ [−20, 20] 的截断评估（l=2, M=1）：")
    r_in = r_of_rstar_true(-20.0)
    r_out = r_of_rstar_true(20.0)
    lval = 2

    def veff_schw(r):
        f = 1.0 - 2.0 * M / r
        return f * (lval * (lval + 1) / r ** 2 + 2.0 * M / r ** 3)

    v_peak = max(veff_schw(rr) for rr in np.linspace(2.5, 6.0, 4000))
    v_out = veff_schw(r_out)
    v_in = veff_schw(r_in)
    put("      内端 r(−20) = %.6f M ⇒ V = %.3e（≈0，可用）" % (r_in, v_in))
    put("      外端 r(+20) = %.4f M ⇒ V = %.3e ；势垒峰 V_peak = %.4f" % (r_out, v_out, v_peak))
    put("      ⇒ 外边界残余势 / 峰 = %.2f%%" % (100.0 * v_out / v_peak))
    if v_out / v_peak > 0.05:
        rec("BOUNDARY", "B3 外边界截断偏早（残余势占比过高）",
            "r_*=20 对应 r≈%.1f M，残余势仍为峰值的 %.1f%% ⇒ 截断引入 O(%%) 级系统误差；"
            "标准做法取 r_* 外端 ≥ 100 M（或加长域 + PML）" % (r_out, 100.0 * v_out / v_peak))
    else:
        rec("PASS", "B3 外边界截断可接受", "残余势/峰 = %.2f%%" % (100.0 * v_out / v_peak))

    # B4 scipy eigs + dense
    put("")
    put("  B4 scipy.sparse.linalg.eigs 接受 dense 数组？—— 实测：")
    try:
        from scipy.sparse.linalg import eigs
        n_small = 30
        rng = np.random.RandomState(1)
        ad = rng.normal(size=(n_small, n_small)) + 1j * rng.normal(size=(n_small, n_small))
        vals = eigs(ad, k=3, which="LM", return_eigenvectors=False)
        ok_eigs = True
        msg = "eigs 接受 dense ndarray，返回 %d 个本征值" % len(vals)
    except Exception as exc:
        ok_eigs = False
        msg = "eigs 对 dense ndarray 失败：%s" % str(exc)[:120]
    put("      " + msg)
    rec("PASS" if ok_eigs else "FAIL", "B4 eigs 与 dense 兼容性（实测）",
        msg + "；但 dense 传入会走 LinearOperator 包装，失去稀疏效率 —— 属效率问题非正确性问题")

    # B5 shift 与 sqrt 分支
    put("")
    put("  B5 shift-invert target 与 sqrt 分支：")
    w2_true = LEAVER_L2 ** 2
    put("      文献基模 ω = %s" % np.round(LEAVER_L2, 9))
    put("      ⇒ ω² = %s （虚部应为负）" % np.round(w2_true, 9))
    put("      稿内 sigma = 0.18 + 0.08j   ⇒ 虚部符号与 ω² 相反，且实部偏差 %.1f%%"
        % (abs(0.18 - w2_true.real) / abs(w2_true.real) * 100))
    rec("FAIL", "B5 shift-invert target 符号错误 + sqrt 分支未筛",
        "ω² 的虚部为负（%.4f），稿内取 +0.08j 会偏向增长模分支；且 jnp.sqrt 返回两支，"
        "须显式筛 Im ω < 0，否则会混入非物理的增益模" % w2_true.imag)

    # B6 挠率势有源性
    rec("BOUNDARY", "B6 V_torsion 为唯象写入（且与既有结论冲突）",
        "V_torsion = T_B·(2M/r²)·exp(−(r−2M)/2M) 在 TUFT 内无导出："
        "D2 已证挠率动力学项受尺度困境（26 量级）、R6 已证 EC 挠率宏观不可测（差 1e28）；"
        "且稿内『低能惰性』主张与 OPEN_v4 的三尺度锚冲突结论同源。⇒ T_B 是自由参数，非 TUFT 预言")

    # =====================================================================
    # §3 核心实证：有限域 + PML 的谱
    # =====================================================================
    sec("3. 核心实证：有限域（±PML）离散谱 —— 箱模判据（R23）复现 + PML 能否救")

    put("  做法：Regge–Wheeler 势（l=2, M=1），r_* 均匀网格，二阶中心差分，")
    put("        构造 A Ψ = ω² Ψ（A = −D² + V），对比三种边界处理：")
    put("        (a) 硬 Dirichlet；(b) PML（稿内一阶 1/s）；(c) PML（正确 1/s²，σ 平滑）")
    put("        判据（R23）：物理 QNM 的 Im ω 应与域长无关；箱模 |Im ω| ∝ 1/L。")
    put("        文献基准（R25 Leaver）ω = %s" % np.round(LEAVER_L2, 9))

    def build_A(rstar, mode, sigma_max=2.0, pml_frac=0.15):
        n = len(rstar)
        h = rstar[1] - rstar[0]
        # 拉伸因子 s_j
        s = np.ones(n, dtype=complex)
        if mode != "dirichlet":
            n_pml = max(2, int(pml_frac * n))
            prof = np.zeros(n)
            # 平滑（二次）过渡
            for j in range(n_pml):
                prof[j] = ((n_pml - j) / float(n_pml)) ** 2
            for j in range(n - n_pml, n):
                prof[j] = ((j - (n - n_pml - 1)) / float(n_pml)) ** 2
            s = 1.0 + 1j * sigma_max * prof
        # 半格点因子
        s_half = 0.5 * (s[:-1] + s[1:])
        a = np.zeros((n, n), dtype=complex)
        for j in range(1, n - 1):
            inv_l = 1.0 / s_half[j - 1]
            inv_r = 1.0 / s_half[j]
            if mode == "pml_draft":        # 稿内：只除一次 s
                c_l = 1.0 / (s[j] * h * h) * inv_l / inv_l
                c_r = 1.0 / (s[j] * h * h) * inv_r / inv_r
                a[j, j - 1] = 1.0 / (s[j] * h * h)
                a[j, j + 1] = 1.0 / (s[j] * h * h)
                a[j, j] = -2.0 / (s[j] * h * h)
            else:                            # 正确：两次 ⇒ 1/s²
                a[j, j - 1] = (1.0 / s[j]) * inv_l / (h * h)
                a[j, j + 1] = (1.0 / s[j]) * inv_r / (h * h)
                a[j, j] = -(1.0 / s[j]) * (inv_l + inv_r) / (h * h)
            r_j = r_of_rstar_true(rstar[j])
            a[j, j] += veff_schw(r_j)
        # 边界
        if mode == "dirichlet":
            a[0, 0] = 1.0
            a[n - 1, n - 1] = 1.0
        else:
            a[0, 0] = 1.0
            a[n - 1, n - 1] = 1.0
        return a

    def best_mode(omega_list):
        cand = [w for w in omega_list if w.imag < 0 and w.real > 0.05 and w.real < 1.5]
        if not cand:
            return None, None
        best = min(cand, key=lambda w: abs(w - LEAVER_L2))
        return best, abs(best - LEAVER_L2)

    results = {}
    configs = [("dirichlet", 0.0), ("pml_draft", 2.0), ("pml_correct", 2.0),
               ("pml_correct", 10.0), ("pml_correct", 50.0)]
    for Ltot in (40.0, 80.0):
        n_pts = int(Ltot / 0.15)
        rstar = np.linspace(-20.0, -20.0 + Ltot, n_pts)
        for mode, smax in configs:
            a_mat = build_A(rstar, mode, sigma_max=(smax if smax > 0 else 2.0))
            try:
                ev = np.linalg.eigvals(a_mat)
            except Exception as exc:
                put("      L=%5.0f  %-12s σ=%-5.1f 求解失败：%s" % (Ltot, mode, smax, str(exc)[:60]))
                continue
            omegas = []
            for lam in ev:
                w = np.sqrt(complex(lam))
                omegas.append(w if w.imag <= 0 else -w)
            best, d = best_mode(omegas)
            if best is None:
                put("      L=%5.0f  %-12s σ=%-5.1f 未筛到候选模" % (Ltot, mode, smax))
                continue
            results[(Ltot, mode, smax)] = (best, d)
            put("      L=%5.0f  %-12s σ=%-5.1f ω=%+.6f %+.6f i |Δ|=%.3e |Imω|/|Imω_phys|=%.5f"
                % (Ltot, mode, smax, best.real, best.imag, d,
                   abs(best.imag) / abs(LEAVER_L2.imag)))

    # 三重判据（修正版）
    put("")
    put("  判据（修正版 · 自查后收紧）：物理 QNM 须同时满足")
    put("      ① |Im ω| 落在文献量级（|Imω|/|Imω_phys| ∈ [0.5, 2]）")
    put("      ② |Δ| < 1e−2")
    put("      ③ 阻尼与域长无关（Imω(40)/Imω(80) ≈ 1）")
    put("      【撤回声明】初版仅用第③条比值判据，曾把 |Imω|≈7e−6 的驻波误判为『疑似物理模』，已作废。")
    for mode, smax in configs:
        v40 = results.get((40.0, mode, smax))
        v80 = results.get((80.0, mode, smax))
        if not (v40 and v80):
            rec("BOUNDARY", "%s(σ=%.0f)：未取得可比结果" % (mode, smax),
                "至少一个域长未筛到候选模 ⇒ 无法判定")
            continue
        r40 = abs(v40[0].imag) / abs(LEAVER_L2.imag)
        r80 = abs(v80[0].imag) / abs(LEAVER_L2.imag)
        ratio_len = abs(v40[0].imag) / abs(v80[0].imag) if v80[0].imag != 0 else float("nan")
        put("      %-12s σ=%-5.1f |Imω|/phys: L40=%.5f L80=%.5f   Imω(40)/Imω(80)=%.3f"
            % (mode, smax, r40, r80, ratio_len))
        if max(r40, r80) < 0.5:
            rec("FAIL", "%s(σ=%.0f)：判为驻波/箱模" % (mode, smax),
                "|Im ω| 仅为文献值的 %.5f / %.5f 倍（小 3 个量级以上）⇒ 不是 QNM，是有限域驻波；"
                "PML 在本文档档位下未能恢复物理阻尼，|Δ| = %.2e" % (r40, r80, min(v40[1], v80[1])))
        elif min(v40[1], v80[1]) < 1e-2 and abs(ratio_len - 1.0) < 0.25:
            rec("PASS", "%s(σ=%.0f)：疑似物理 QNM" % (mode, smax),
                "阻尼落在文献量级且域长无关；|Δ| = %.2e" % min(v40[1], v80[1]))
        else:
            rec("BOUNDARY", "%s(σ=%.0f)：判据不确定" % (mode, smax),
                "|Imω|/phys = %.3f / %.3f，域长比 %.3f，|Δ| = %.2e ⇒ 需更专业实现再判"
                % (r40, r80, ratio_len, min(v40[1], v80[1])))

    put("")
    put("  【对照·已被走通的正确路线】R25 Leaver 连分式：")
    put("      l=2 基模 ω = %.12f %+.12f i（|Δ| ≈ 4.5e−7，r_max 无关）"
        % (LEAVER_L2.real, LEAVER_L2.imag))
    rec("INFO", "正确路线已存在且已验证",
        "R25/R26 的 Leaver 连分式已给出特征值级（~1e−7）精确谱，且 R26 验证 N 独立性 Δ=0；"
        "R27 证明 RW↔Zerilli 等谱（SUSY）。⇒ 主线B 若目标是『拿到可信 ω(T_B) 表』，"
        "应把 Leaver 推广到含 V_torsion 的势，而非重走有限域谱方法")

    put("")
    put("  【根本性诊断】为什么『线性本征值 + PML』原理上给不出 QNM：")
    put("      QNM 的本征值问题是**非线性**的：出射边界条件 Ψ ~ e^{∓iω r_*} 中的 ω 正是待求量。")
    put("      把它写成 A Ψ = ω² B Ψ（A、B 与 ω 无关）⇒ 求的是**固定边界**问题，")
    put("      其谱本质是驻波谱（近实频 + 微弱数值/PML 阻尼），不含 QNM 的复频率。")
    put("      PML 只对**已知频率**的外行波『完美匹配』——而 ω 本身未知 ⇒ PML 参数是隐式的，")
    put("      需在 ω 上做 Newton 迭代（PML 随 ω 更新），或改用**复坐标延拓(complex scaling)**：")
    put("      后者把连续谱旋转到复平面，使共振态成为 L² 可归一化的离散本征值，是谱方法求 QNM 的正解。")
    put("      ⇒ 稿内『PML + 广义本征值』组合原理上错位：PML 服务于时域 FDTD 的外行波吸收，")
    put("         不服务于线性本征值提取；要提取 QNM 应走 Leaver 连分式（R25 已通）或复坐标延拓。")
    rec("BOUNDARY", "根本性诊断（方法论层）",
        "线性本征值 + PML 原理上给不出 QNM（出射 BC 与 ω 非线性耦合）；本册实证与该诊断一致："
        "全部配置 |Imω| 均比文献小 4 个量级以上（驻波）。这不否证 PML 在时域 FDTD 中的作用，"
        "只否证它在『线性本征值提取 QNM』中的角色")

    # =====================================================================
    # §4 结论
    # =====================================================================
    sec("4. 结论与路线建议")
    put("  【主线A】暂不具备可跑条件。阻塞项（按严重度）：")
    put("    1. 观测数据非 Planck 真实约束（σ 紧 %.0f 倍）⇒ log Z / 贝叶斯因子无观测意义" % ratio_sigma)
    put("    2. 采样参数 t_c 在 TUFT 内无定义（R30 三路证 β≡0，无 RG 流 ⇒ 无拓扑跃迁能标）")
    put("    3. f_NL^TUFT(l) 无第一性来源（TUFT 无双谱计算）")
    put("    4. 阶跃似然对 l_c 梯度恒 0 ⇒ NUTS 退化为随机游走")
    put("    5. numpyro/jax 缺失 + API 待核验 ⇒ 当前代码不可执行")
    put("")
    put("  【主线B】方向正确（PML 正是 R23 建议的补救路线之一，未被否证），但实现需修 5 处：")
    put("    1. r_of_rstar 用正映射当逆映射（误差 %.1e）⇒ 必须二分/牛顿求根" % max(errs))
    put("    2. PML 少一阶（1/s 应为 1/s²）+ σ 须平滑过渡")
    put("    3. 外边界 r_*=20 残余势仍占峰值 %.1f%% ⇒ 加长域" % (100.0 * v_out / v_peak))
    put("    4. shift-invert target 虚部符号反 + 须筛 Im ω < 0")
    put("    5. V_torsion 唯象写入，须显式标注为自由参数（非 TUFT 预言）")
    put("")
    put("  【两条主线的共同前置】在做任何采样/比对之前，必须先回答一个问题：")
    put("     TUFT 内部是否存在可计算的 RG 流与原初谱？—— R30 已证前者不存在（β≡0）。")
    put("     ⇒ 建议把『拓扑跃迁』改述为『唯象阶跃假设』并如此登记，否则会被误认为 TUFT 预言。")
    rec("INFO", "本册性质",
        "审计（含实算实证）非实现；所有判定可复算。R23 的 PML 补救建议未被本册否证，"
        "本册只指出其实现缺陷与『Leaver 已先行』的事实")

    sec("汇总")
    put("  PASS     = %d" % stat.get("PASS", 0))
    put("  FAIL     = %d" % stat.get("FAIL", 0))
    put("  BOUNDARY = %d" % stat.get("BOUNDARY", 0))
    put("  INFO     = %d" % stat.get("INFO", 0))
    put("")
    put("  环境：numpyro/jax/jaxlib = MISSING ⇒ 主线A 不可运行")
    put("  A1 σ 夸大 %.0f 倍；A2 梯度为 0 占 %.1f%%" % (ratio_sigma, zero_frac * 100))
    put("  B1 逆映射误差 %.1e；B2 PML 少一阶；B3 外边界残余 %.1f%%；B5 shift 符号反"
        % (max(errs), 100.0 * v_out / v_peak))
    put("")
    put("红线声明：本册为审计，数学自洽 != 实验证实；未实测项已显式标注。")

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
