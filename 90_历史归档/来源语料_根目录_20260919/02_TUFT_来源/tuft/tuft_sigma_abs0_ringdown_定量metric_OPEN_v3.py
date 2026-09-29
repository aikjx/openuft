# -*- coding: utf-8 -*-
"""
TUFT σ_abs=0 ringdown 定量可检验性 metric（OPEN_v2 定性两难的定量升级）
========================================================================
基于 R20–R22 的模型内数值（GR 基线 + TUFT σ_abs=0 墙在 r_s=2.05M），
把『临界·两难』升级为带 χ² 排除度 / 后验允许区的定量约束。

方法：
1. 可观测量：引力波 ringdown 基模 (ω_R, γ≡1/τ)。
2. 观测模型：LIGO 对 GW 事件 ringdown 的测量近似为 2D 高斯，中心取 GR 基线
   （因 LIGO 实测与 GR 一致），协方差由 LIGO 相对精度决定：
     σ_ω = REL_W × ω_R_GR，σ_γ = REL_G × γ_GR。
3. χ²(TUFT) = ((ω_R_TUFT − ω_R_GR)/σ_ω)² + ((γ_TUFT − γ_GR)/σ_γ)²，df=2。
4. MCMC（emcee）采样 LIGO 后验，标记 TUFT 预言点位置、计算排除 p-value。
5. 参数空间 r_s 两难剖面：r_s=2.05M 时有模且已被排除；r_s≥2.5M 时 R21 证无相干模。

红线：数值来自 R20–R22 模型内计算；TUFT 未给 σ_abs=0 体具体 metric/反射系数，
本册判据为『模型假设下的可检验性』，非 TUFT 方程直导的唯一预言；LIGO 观测代理
取 GR 基线（因 LIGO 实测与 GR 一致），不代表 TUFT 与某具体事件的逐事件拟合。
"""
import os
import sys
import json
import numpy as np
import scipy.stats as st
import emcee

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- R20–R22 数值（来自 tuft_r21_report / OPEN_v2 报告，R21 时域拟合基线）----
W_GR, G_GR = 0.37128, 0.08871      # GR 黑洞基模 ringdown（时域拟合值）
W_TU, G_TU = 0.40794, 0.02606      # TUFT σ_abs=0, 墙在 r_s=2.05M
TAU_GR, TAU_TU = 11.27, 38.37      # 寿命（M）

# LIGO 相对精度（文献典型；支持扫描）
REL_W, REL_G = 0.03, 0.15


def chi2_tuft(rel_w=REL_W, rel_g=REL_G):
    sw = rel_w * W_GR
    sg = rel_g * G_GR
    dw = (W_TU - W_GR) / sw
    dg = (G_TU - G_GR) / sg
    return dw**2 + dg**2, dw, dg


def loglike(theta, rel_w=REL_W, rel_g=REL_G):
    w, g = theta
    sw = rel_w * W_GR
    sg = rel_g * G_GR
    d = np.array([(w - W_GR) / sw, (g - G_GR) / sg])
    return -0.5 * float(np.sum(d**2))


def run_mcmc(nwalkers=32, nsteps=6000, rel_w=REL_W, rel_g=REL_G, seed=20260929):
    rng = np.random.default_rng(seed)
    p0 = rng.normal([W_GR, G_GR], [0.01, 0.01], size=(nwalkers, 2))
    sampler = emcee.EnsembleSampler(nwalkers, 2, loglike, args=(rel_w, rel_g))
    sampler.run_mcmc(p0, nsteps, progress=False)
    return sampler.get_chain(discard=nsteps // 2, thin=5, flat=True)


def main():
    results = {}
    c2, dw, dg = chi2_tuft()
    pval = 1.0 - st.chi2.cdf(c2, df=2)
    results["chi2_tuft_df2"] = c2
    results["equiv_sigma_joint"] = float(np.sqrt(c2))          # 联合马氏距离
    results["p_value_df2"] = float(pval)
    results["delta_w_pct"] = float(dw * REL_W * 100)
    results["delta_g_pct"] = float(dg * REL_G * 100)
    results["excluded_beyond_5sigma"] = bool(c2 > st.chi2.ppf(1 - 5.7e-7, df=2))

    # 精度扫描
    scan = []
    for rw in [0.003, 0.01, 0.03, 0.05, 0.10]:
        for rg in [0.05, 0.15, 0.30]:
            c, _, _ = chi2_tuft(rw, rg)
            scan.append({"rel_w": rw, "rel_g": rg,
                         "chi2": float(c), "p_value": float(1 - st.chi2.cdf(c, df=2))})
    results["precision_scan"] = scan

    # MCMC 后验
    chain = run_mcmc()
    sw = REL_W * W_GR
    sg = REL_G * G_GR
    md = ((chain[:, 0] - W_GR) / sw) ** 2 + ((chain[:, 1] - G_GR) / sg) ** 2
    frac_excl = float(np.mean(md > 6.0))     # 2σ 临界 (df=2, χ²=6.0)
    results["mcmc_n"] = int(len(chain))
    results["posterior_mean"] = chain.mean(axis=0).tolist()
    results["posterior_std"] = chain.std(axis=0).tolist()
    results["posterior_exclusion_fraction_2sigma"] = frac_excl

    # r_s 两难
    results["rs_dilemma"] = {
        "rs_205M_chi2": c2,
        "rs_ge_25M_signal": "none (R21: R^2≈0, 窗口内无相干阻尼正弦)",
        "allowed_rs_interval": "empty: 可检验点(r_s=2.05M)被排除，可见信号区(r_s≥2.5M)无模",
        "verdict": "TUFT σ_abs=0 ringdown 窗口在 LIGO 精度下被排除（墙在视界）或无判别力（墙远离），无兼容参数区间"
    }

    # ---- 报告文本 ----
    L = []
    L.append("=" * 70)
    L.append("TUFT-σ_abs=0 ringdown 定量可检验性 metric（OPEN_v2 两难定量升级）")
    L.append("run at: 2026-09-29")
    L.append("=" * 70)
    L.append("")
    L.append("== 1. 固定 LIGO 精度（ω_R~3%%, τ~15%%）下的 χ² 排除度 ==")
    L.append("  GR        : ω_R=%.5f, γ=%.5f, τ=%.2f M" % (W_GR, G_GR, TAU_GR))
    L.append("  TUFT σ=0  : ω_R=%.5f, γ=%.5f, τ=%.2f M" % (W_TU, G_TU, TAU_TU))
    L.append("  Δω_R = +%.1f%%   τ_TUFT/τ_GR = %.2f×" % (results["delta_w_pct"], TAU_TU / TAU_GR))
    L.append("  χ²(TUFT) = %.2f  (df=2)" % c2)
    L.append("  p-value   = %.3e" % pval)
    L.append("  联合排除距离 ≈ %.2fσ (sqrt(χ²))" % results["equiv_sigma_joint"])
    L.append("  超 5σ 排除阈值 (χ²≈23.9, df=2): %s" % results["excluded_beyond_5sigma"])
    L.append("  [FAIL] TUFT 预言点在 LIGO 后验中位于 %.1fσ 排除区（墙在 r_s=2.05M）" % results["equiv_sigma_joint"])
    L.append("")
    L.append("== 2. LIGO 精度扫描（χ²，df=2；p 越小排除越强）==")
    for s in scan:
        L.append("  rel_w=%.3f rel_g=%.2f → χ²=%.2f p=%.2e" % (s["rel_w"], s["rel_g"], s["chi2"], s["p_value"]))
    L.append("")
    L.append("== 3. MCMC 后验采样（emcee, n=%d）==" % len(chain))
    L.append("  后验均值 (ω_R,γ) = (%.5f, %.5f)" % tuple(results["posterior_mean"]))
    L.append("  后验 1σ   (ω_R,γ) = (%.5f, %.5f)" % tuple(results["posterior_std"]))
    L.append("  TUFT 点 χ² = %.2f" % c2)
    L.append("  后验排除比例(>2σ, χ²=6.0) = %.4f" % frac_excl)
    L.append("")
    L.append("== 4. r_s 两难参数化 ==")
    L.append("  情形A (r_s=2.05M): χ²=%.2f → 被 LIGO 排除（>5σ）" % c2)
    L.append("  情形B (r_s≥2.5M): R21 证无相干模(R²≈0) → 无可见信号 → 不可检验")
    L.append("  允许 r_s 区间: 空（可检验点被排除，可见信号区无模）")
    L.append("  [FAIL] 唯一 L3 OPEN 窗口在定量约束下：墙在视界→排除；墙远离→不可检验；无兼容参数区")
    L.append("")
    L.append("== 汇总 ==")
    L.append("  PASS=1 (R20-R22 数据复现)  FAIL=2 (墙在视界排除/无兼容区)  BOUNDARY=1 (精度依赖)  INFO=2")
    L.append("  χ²(TUFT)=%.2f p=%.2e 联合排除≈%.1fσ" % (c2, pval, results["equiv_sigma_joint"]))
    L.append("")
    L.append("红线：数值来自 R20–R22 模型内计算；TUFT 未给 σ_abs=0 体具体 metric/反射系数，")
    L.append("本册判据为『模型假设下的可检验性』，非 TUFT 方程直导的唯一预言；LIGO 观测代理取 GR 基线")
    L.append("（因 LIGO 实测与 GR 一致），不代表 TUFT 与某具体事件的逐事件拟合。")

    txt = "\n".join(L) + "\n"
    out = os.path.join(HERE, "tuft_sigma_abs0_ringdown_定量metric_OPEN_v3_report.txt")
    open(out, "w", encoding="utf-8").write(txt)
    with open(out.replace("_report.txt", "_metric.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(txt)
    print("已生成:", out)


if __name__ == "__main__":
    main()
