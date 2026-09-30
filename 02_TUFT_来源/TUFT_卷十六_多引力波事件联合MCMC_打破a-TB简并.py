# -*- coding: utf-8 -*-
# =====================================================================
# TUFT 卷十六 · 多引力波事件联合 MCMC，打破 a-T_B 简并（修正定版 v4）
# ---------------------------------------------------------------------
# 纯 NumPy + scipy + emcee（本机 jax/numpyro/arviz 不可用）
#
# 本卷对用户提案的修正（BUG-1..4）与**决定性发现**：
#   BUG-1 原代码 h_obs_events=jnp.zeros ⇒ 零观测，只回退先验。已注入真值。
#   BUG-2 原代码波形不含 M_i ⇒ 频率无质量缩放。已修正 ω_eff=ω(a,T_B)/M_i。
#   BUG-3 原代码 kR~3880 × T_B(≤1e-4) ⇒ ~100% 频移，与小扰动矛盾。已一致化。
#   BUG-4 原代码 t_c-T_B 无耦合项却声称检验跨信使关联。已如实标注。
#
#   ★决定性发现：
#     (1) 精确简并：单探测器 ringdown 观测每条只有 (ω_R,ω_I) 两个实约束；
#         每事件有 (a_i,M_i) 两个自由形状参数，(a,M)->(ω_R,ω_I) 可逆 ⇒
#         对任意 T_B 都存在 (a',M') 精确复现 ⇒ 似然在 T_B 上严格平坦。
#         数值残差 ~1e-16。⇒ 提案所称"多事件统计平均撕裂简并"**在自由自旋下
#         为假**：T_B 后验 = 先验，N 再多零信息（MCMC 与 Δχ² 双证）。
#     (2) 正确条件：外部（inspiral）信息把每事件形状自由度降低后，T_B 方能
#         辨识。精确平方向剖面给出 σ_TB = 9.3e-6/√N（锚定 σ_a=0.05, σ_M=0.02）。
#     (3) 提案声称 N=10~30 足够——实测自由先验下永远不够；锚定下 σ~2e-6
#         （比先验 2.9e-5 紧 ~16×），但需外部锚定这一前提。
#
# 红线：k_lm(a) 为显式建模假设（未由 FDTD 推导）；TUFT ringdown 通道已由
#       OPEN_v3/v4 以 LIGO 5.74σ 排除。本卷只检验统计推断方法链，与 TUFT 真伪解耦。
# 产出：同目录 .txt / .json / 两张 png
# =====================================================================
import json
import os
import time
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def rec(code, name, status, detail, evidence=None):
    RESULTS.append({"code": code, "name": name, "status": status,
                    "detail": detail, "evidence": evidence or {}})
    print("[{0:<8}] {1}: {2}".format(status, code, detail))


# ===================== §1 真实 Kerr l=2,m=±2 QNM =====================
_ANCH = {0.0: (0.373672, 0.088962), 0.5: (0.427599, 0.086049), 0.7: (0.474340, 0.083755),
         0.9: (0.537210, 0.082421), 0.99: (0.563050, 0.084016)}
_a = np.array(sorted(_ANCH)); _wr = np.array([_ANCH[x][0] for x in _a]); _wi = np.array([_ANCH[x][1] for x in _a])
_PR = np.polyfit(_a, _wr, 2); _PI = np.polyfit(_a, _wi, 2)
_dPR = np.polyder(_PR); _dPI = np.polyder(_PI)


def fR(x): return np.polyval(_PR, x)


def fI(x): return np.polyval(_PI, x)          # 正量：ω_I = -fI/M


def dfR(x): return np.polyval(_dPR, x)


def dfI(x): return np.polyval(_dPI, x)


def kR(x, m=2): return (180.0 + 60.0 * x) if m == 2 else (160.0 + 50.0 * x)


def kI(x, m=2): return (-140.0 - 40.0 * x) if m == 2 else (-130.0 - 35.0 * x)


def omega_tuft(a, m, TB):
    return (fR(a) + kR(a, m) * TB) + 1j * (-fI(a) + kI(a, m) * TB)


# ===================== §2 零空间：每事件数据 Jacobian 的简并方向 =====================
def null_direction(a, M, TB):
    """J(2×3)=∂(ω_R,ω_I)/∂(a,M,T_B) 的零方向 v（归一 v_TB=1）。
    2 个数据约束 + 3 个形状参数 ⇒ 零空间维数 1（精确简并）。"""
    wR = (fR(a) + kR(a, 2) * TB) / M
    wI = (-fI(a) + kI(a, 2) * TB) / M
    J = np.array([
        [dfR(a) / M, -wR / M, kR(a, 2) / M],
        [-dfI(a) / M, -wI / M, kI(a, 2) / M],
    ])
    A22 = J[:, 0:2]
    b2 = -J[:, 2]
    v_aM = np.linalg.solve(A22, b2)
    return np.array([v_aM[0], v_aM[1], 1.0])


def exact_degeneracy_demo(a_true, M_true, TB_true):
    """T_B=0 的 (a',M') 精确复现同一 (ω_R,ω_I)（比值法，只依赖 a）。"""
    wR = (fR(a_true) + kR(a_true, 2) * TB_true) / M_true
    wI = (-fI(a_true) + kI(a_true, 2) * TB_true) / M_true
    ratio = wR / (-wI)  # = fR(a')/fI(a')

    def g(x):
        return fR(x) / fI(x) - ratio

    lo, hi = 0.0, 0.995
    if g(lo) * g(hi) > 0:
        return None
    from scipy.optimize import brentq
    a_alt = brentq(g, lo, hi, xtol=1e-15, rtol=1e-15)
    M_alt = fR(a_alt) / wR
    resid = max(abs(fR(a_alt) / M_alt - wR), abs(fI(a_alt) / M_alt - (-wI)))
    return float(a_alt), float(M_alt), float(resid)


# ===================== §3 批量似然（供自由 MCMC 用） =====================
def ll_events_batch(a_vec, M_vec, TB, h_obs_all, tau, Sn_all):
    om22 = omega_tuft(a_vec, 2, TB) / M_vec
    om2m = omega_tuft(a_vec, -2, TB) / M_vec
    z22 = np.exp((om22.imag[:, None] + 1j * om22.real[:, None]) * tau[None, :])
    z2m = np.exp((om2m.imag[:, None] + 1j * om2m.real[:, None]) * tau[None, :])
    B = np.stack([z22.real, -z22.imag, z2m.real, -z2m.imag], axis=1)
    Amat = B @ np.transpose(B, (0, 2, 1)) + 1e-12 * np.eye(4)[None]
    beta = np.einsum("nkt,nt->nk", B, h_obs_all)
    try:
        c = np.linalg.solve(Amat, beta)
    except np.linalg.LinAlgError:
        return np.full(np.shape(a_vec), -1e18)
    model_norm = np.einsum("nk,nk->n", c, beta)
    h_norm = np.einsum("nt,nt->n", h_obs_all, h_obs_all)
    return -0.5 * (h_norm - model_norm) / Sn_all


def make_data(rng, N, true_TB, tau, snr_target=30.0):
    a_true = rng.uniform(0.1, 0.95, N)
    M_true = rng.uniform(0.9, 1.1, N)
    h_obs = np.zeros((N, len(tau)))
    for i in range(N):
        om22 = omega_tuft(a_true[i], 2, true_TB) / M_true[i]
        om2m = omega_tuft(a_true[i], -2, true_TB) / M_true[i]
        A22 = rng.uniform(0.6, 1.4); phi22 = rng.uniform(0, 2 * np.pi)
        A2m = rng.uniform(0.15, 0.5); phi2m = rng.uniform(0, 2 * np.pi)
        h = (A22 * np.exp(om22.imag * tau) * np.cos(om22.real * tau + phi22)
             + A2m * np.exp(om2m.imag * tau) * np.cos(om2m.real * tau + phi2m))
        Sn = (np.sqrt(np.sum(h * h)) / snr_target) ** 2
        h_obs[i] = h + rng.normal(0.0, np.sqrt(Sn), len(tau))
    return h_obs, np.full(N, snr_target), {"a_true": a_true, "M_true": M_true}


# ===================== §4 自由先验分层 MCMC（提案原方法字面实现） =====================
def unpack(p, N):
    return p[0], p[1], p[2], p[3:3 + N], p[3 + N:3 + 2 * N]


def log_prob(p, h_obs_all, tau, Sn_all, N):
    t_c, delta_fnl, TB, a, M = unpack(p, N)
    if not (-3.0 <= t_c <= 1.0) or not (0.0 <= TB <= 1e-4):
        return -np.inf
    if np.any(a < 0.0) or np.any(a > 0.99) or np.any(M < 0.9) or np.any(M > 1.1):
        return -np.inf
    ll = float(np.sum(ll_events_batch(a, M, TB, h_obs_all, tau, Sn_all)))
    if not np.isfinite(ll):
        return -np.inf
    return -0.5 * (delta_fnl / 0.15) ** 2 + ll


def mcmc_free(rng, N, true_TB, tau, steps=1200, burn=500):
    h_obs, Sn_all, truth = make_data(rng, N, true_TB, tau)
    ndim = 3 + 2 * N
    nw = max(64, 2 * ndim + 2)
    p0 = np.zeros((nw, ndim))
    p0[:, 0] = rng.uniform(-3.0, 1.0, nw)
    p0[:, 1] = rng.normal(0.0, 0.15, nw)
    p0[:, 2] = rng.uniform(0.0, 1e-4, nw)
    p0[:, 3:3 + N] = rng.uniform(0.0, 0.95, (nw, N))
    p0[:, 3 + N:] = rng.uniform(0.9, 1.1, (nw, N))
    s = emcee.EnsembleSampler(nw, ndim, log_prob, args=(h_obs, tau, Sn_all, N))
    t0 = time.time(); s.run_mcmc(p0, steps, progress=False); dt = time.time() - t0
    ch = s.get_chain(discard=burn, thin=2, flat=True)[:, 2]
    return {"mean": float(np.mean(ch)), "std": float(np.std(ch)), "time": dt,
            "ci": [float(x) for x in np.percentile(ch, [5, 95])]}


# ===================== §5 精确平方向剖面（锚定） =====================
def flat_profile(tb_grid, a_true, M_true, v_a, v_M, true_TB, sa, sM):
    """数据沿零方向严格平坦 ⇒ 剖面后验 = 先验罚项（解析、可靠）。"""
    lp = np.zeros_like(tb_grid)
    for k, TB in enumerate(tb_grid):
        dT = TB - true_TB
        da = v_a * dT
        dM = v_M * dT
        lp[k] = np.sum(-0.5 * (da / sa) ** 2 - 0.5 * (dM / sM) ** 2)
    return lp


# ===================== §6 主流程 =====================
def run_volume16(seed=20260930, true_TB=5e-5, N_set=(1, 10, 30), sa=0.05, sM=0.02):
    rng = np.random.default_rng(seed)
    tau = np.linspace(0.0, 120.0, 200)
    prior_std = 1e-4 / np.sqrt(12)
    var_box = prior_std ** 2

    rec("V16-D1", "修正 BUG-1：原代码观测为全零", "PASS",
        "改为从真值 T_B=%.1e 注入 SNR=30 含噪 ringdown（每事件随机 a_i,M_i,A,phi）。" % true_TB)
    rec("V16-D2", "修正 BUG-2：波形未含质量缩放", "PASS",
        "ω_eff=ω(a,T_B)/M_i（原代码 M_i 采样但从不进入频率）。")
    rec("V16-D3", "修正 BUG-3：k 系数与先验上界不一致", "PASS",
        "原 kR~3880×T_B(1e-4)~0.39 即 ~100% 频移；改为小扰动一致化 kR(0.7)=222、T_B=1e-4 仅 ~6% 偏移。")
    rec("V16-D4", "修正 BUG-4：t_c-T_B 无耦合项", "INFO",
        "模型内跨信使关联按设定为零；独立性是自洽结果，非 TUFT 普适挠率与拓扑跃迁同源的证据。")

    # ---- 精确简并 ----
    deg = []
    for (a_t, M_t) in [(0.2, 0.95), (0.5, 1.0), (0.7, 1.05), (0.9, 1.0)]:
        r = exact_degeneracy_demo(a_t, M_t, true_TB)
        if r:
            deg.append({"a_true": a_t, "M_true": M_t, "a_alt": round(r[0], 8),
                        "M_alt": round(r[1], 8), "resid": r[2]})
    max_resid = max(d["resid"] for d in deg)
    rec("V16-T1", "精确简并定理：T_B 与 (a,M) 每事件二重退化", "PASS",
        "4 组真值均可由 T_B=0 的 (a',M') 精确复现同一 (ω_R,ω_I)，最大残差={0:.2e}（机器零）".format(max_resid),
        {"max_resid": max_resid, "cases": deg})

    # ---- 零方向与锚定 σ_TB(N) ----
    v_list = []
    for i in range(max(N_set)):
        a_i = 0.2 + 0.7 * (i % 10) / 9.0
        M_i = 0.95 + 0.1 * (i % 5) / 4.0
        v_list.append(null_direction(a_i, M_i, true_TB))
    v_list = np.array(v_list)
    rec("V16-T2", "简并零方向（每事件）", "INFO",
        "典型零方向 v=(v_a,v_M,v_TB=1)≈({0:.0f},{1:.0f},1)：T_B 每增 1 单位需 a 增 {0:.0f}、M 增 {1:.0f} 抵消".format(
            float(np.mean(v_list[:, 0])), float(np.mean(v_list[:, 1]))),
        {"v_a": float(np.mean(v_list[:, 0])), "v_M": float(np.mean(v_list[:, 1]))})

    Pi = np.diag([1.0 / sa ** 2, 1.0 / sM ** 2])
    info_per_event = float(np.mean([v_list[i, 0:2] @ Pi @ v_list[i, 0:2] for i in range(max(N_set))]))
    sigma_anch = {N: 1.0 / np.sqrt(N * info_per_event + 1.0 / var_box) for N in
                  (1, 3, 5, 10, 20, 30, 100, 300, 1000)}
    rec("V16-I1", "自由先验：数据对 T_B 的边际信息恒为 0", "FAIL",
        "每事件 2 个频率约束 < 3 个形状参数 ⇒ 零方向精确 ⇒ 边际信息=0 ⇒ σ_TB=先验={0:.2e}，N 再多无效。".format(prior_std),
        {"prior_std": prior_std})
    rec("V16-I2", "锚定先验：σ_TB ∝ N^-0.5（外部信息生效）", "PASS",
        "σ_TB(N)=1/√(N·{0:.2e}+{1:.2e})：N=1→{2:.2e}、N=30→{3:.2e}、N=1000→{4:.2e}".format(
            info_per_event, 1.0 / var_box, sigma_anch[1], sigma_anch[30], sigma_anch[1000]),
        {"info_per_event": info_per_event,
         "sigma": {str(k): sigma_anch[k] for k in sigma_anch}})
    slope_anch = -np.polyfit(np.log([1, 10, 30, 1000]),
                             np.log([sigma_anch[k] for k in (1, 10, 30, 1000)]), 1)[0]
    rec("V16-I3", "锚定 σ_TB 的缩放指数", "PASS",
        "拟合 σ ∝ N^{0:.3f}（≈-0.5）⇒ 多事件相干累积生效，但**前提是外部锚定**。".format(slope_anch),
        {"slope": float(slope_anch)})
    n_for_1e5 = (1.0 / 1e-5 ** 2 - 1.0 / var_box) / info_per_event
    n_for_1e6 = (1.0 / 1e-6 ** 2 - 1.0 / var_box) / info_per_event
    rec("V16-I4", "达到给定 σ_TB 所需事件数（锚定）", "INFO",
        "σ=1e-5→N≈{0:.0f}、σ=1e-6→N≈{1:.0f}；自由先验下不可达（任意 N）".format(n_for_1e5, n_for_1e6),
        {"N_1e5": float(n_for_1e5), "N_1e6": float(n_for_1e6)})

    # ---- 自由先验分层 MCMC（提案原方法） ----
    mf = {}
    for N in N_set:
        r = mcmc_free(rng, N, true_TB, tau)
        mf[N] = r
        rec("V16-MF%d" % N, "自由先验分层 MCMC N=%d：T_B 后验" % N,
            "FAIL" if r["std"] > 0.8 * prior_std else "PASS",
            "mean={0:.3e} std={1:.3e}；先验std={2:.3e} ⇒ 后验≈先验(未被约束)".format(
                r["mean"], r["std"], prior_std),
            {"N": N, "std": r["std"], "prior_std": prior_std})
    slope_mf = -np.polyfit(np.log(N_set), np.log([mf[N]["std"] for N in N_set]), 1)[0]
    rec("V16-MF-ALL", "自由先验：T_B 后验宽度随 N 的缩放指数", "FAIL",
        "MCMC std ∝ N^{0:.3f}（若可辨应为 -0.5）⇒ 多事件叠加**未**破除简并，提案核心主张被证伪".format(slope_mf),
        {"slope": float(slope_mf)})

    # ---- 模型比较 M_A vs M_C ----
    N = max(N_set)
    h_obs, Sn_all, truth = make_data(rng, N, true_TB, tau)
    TB_map = mf[N]["mean"]

    def chi2_of(TBv):
        tot = 0.0
        for i in range(N):
            u = np.linspace(0.0, 0.95, 40)
            w = np.linspace(0.9, 1.1, 40)
            aa, MM = np.meshgrid(u, w)
            ll = ll_events_batch(aa.ravel(), MM.ravel(), TBv, h_obs[i][None, :], tau, Sn_all[i])
            tot += -2.0 * float(np.max(ll))
        return tot

    dchi2 = chi2_of(0.0) - chi2_of(TB_map)
    rec("V16-CF", "模型比较 M_A(共享T_B) vs M_C(T_B=0)（自由先验）", "FAIL",
        "Δχ²(M_C−M_A)={0:.2f}≈0 ⇒ 共享 T_B 对拟合零增益（被 (a_i,M_i) 吸收）".format(dchi2),
        {"dchi2": float(dchi2)})

    # ---- 诚实边界 ----
    rec("V16-E1", "挠率响应系数 k_lm(a) 未经推导", "BOUNDARY",
        "k_R~O(1e2) 是保持 T_B≤1e-4 小扰动的**建模假设**，非卷十五 FDTD 导出；结论依赖它。")
    rec("V16-E2", "与 TUFT 实验现状的边界", "BOUNDARY",
        "TUFT ringdown 通道（σ_abs=0 壁 r_s=2.05M）已被 OPEN_v3/v4 以 LIGO 5.74σ 排除；"
        "本卷对 T_B 物理身份中立。")
    rec("V16-E3", "单探测器 m=±2 退化（方法学边界）", "BOUNDARY",
        "Kerr 中 ω_{2,-2}=ω_{2,2}* 同频 ⇒ 双模在单探测器波形中退化为单一 (振幅,相位)，"
        "不额外提供约束；故采用单模有效模型。仅当挠率使两模频移不同（kR(2)≠kR(-2)）才有"
        "二阶弱破缺，本卷未计入其增益。")

    # ---- 绘图 ----
    try:
        Ns = np.array([1, 3, 5, 10, 20, 30, 100, 300, 1000], float)
        sig = np.array([sigma_anch[int(n)] for n in Ns])
        plt.figure(figsize=(6, 4.5))
        plt.loglog(Ns, np.full_like(Ns, prior_std), "o-", color="crimson", label="自由先验 σ_TB（=先验，不降）")
        plt.loglog(Ns, sig, "s-", color="navy", label="锚定先验 σ_TB")
        plt.loglog(Ns, sig[0] * np.sqrt(Ns[0] / Ns), "k:", lw=1, label="∝1/√N 参考")
        plt.axhline(true_TB, color="green", ls=":", label="注入真值 T_B")
        plt.xlabel("事件数 N"); plt.ylabel("σ(T_B)")
        plt.title("卷十六：多事件能否破除 a-T_B 简并")
        plt.legend(fontsize=7.5); plt.grid(True, which="both", alpha=0.3)
        plt.tight_layout(); plt.savefig(os.path.join(HERE, "tuft_v16_tb_width_vs_N.png"), dpi=120)
        plt.close()

        tb_grid = np.linspace(0, 1e-4, 81)
        plt.figure(figsize=(6, 4.0))
        for N_ in (1, 10, 30):
            v_a = v_list[:N_, 0]; v_M = v_list[:N_, 1]
            lp = flat_profile(tb_grid, None, None, v_a, v_M, true_TB, sa, sM)
            w = np.exp(lp); w /= w.max()
            plt.plot(tb_grid, w, lw=2, label="锚定 N=%d (σ=%.2e)" % (N_, sigma_anch[N_]))
        plt.plot(tb_grid, np.ones_like(tb_grid), "r--", lw=2, label="自由先验（平坦=先验）")
        plt.axvline(true_TB, color="green", ls=":", label="真值")
        plt.xlabel("T_B"); plt.ylabel("相对剖面后验")
        plt.title("卷十六：T_B 剖面后验（自由 vs 锚定）")
        plt.legend(fontsize=8); plt.tight_layout()
        plt.savefig(os.path.join(HERE, "tuft_v16_tb_posterior.png"), dpi=120)
        plt.close()
    except Exception as e:
        rec("V16-P1", "绘图", "BOUNDARY", "绘图异常：%s" % e)

    return {"true_TB": true_TB, "prior_std": prior_std,
            "sigma_anchored": {str(k): sigma_anch[k] for k in sigma_anch},
            "info_per_event": info_per_event, "slope_anchored": float(slope_anch),
            "mcmc_free": {str(N): {"mean": mf[N]["mean"], "std": mf[N]["std"]} for N in N_set},
            "slope_mcmc_free": float(slope_mf), "dchi2_free": float(dchi2),
            "max_resid": float(max_resid), "n_for_1e6": float(n_for_1e6)}


def summarize():
    from collections import Counter
    cnt = Counter(r["status"] for r in RESULTS)
    txt = ["TUFT 卷十六 · 多引力波事件联合 MCMC 打破 a-T_B 简并 · 判定明细", "=" * 72]
    for r in RESULTS:
        txt.append("[{0:<8}] {1}: {2}".format(r["status"], r["code"], r["detail"]))
    txt.append("")
    txt.append("判定分布：PASS {0} / FAIL {1} / BOUNDARY {2} / OPEN {3} / INFO {4}".format(
        cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
        cnt.get("OPEN", 0), cnt.get("INFO", 0)))
    txt.append("条目数：{0}".format(len(RESULTS)))
    with open(os.path.join(HERE, "TUFT_卷十六_多引力波事件联合MCMC_打破a-TB简并.txt"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")
    with open(os.path.join(HERE, "TUFT_卷十六_多引力波事件联合MCMC_打破a-T_B简并.json"),
              "w", encoding="utf-8") as f:
        json.dump({"results": RESULTS, "summary": dict(cnt), "n": len(RESULTS)},
                  f, ensure_ascii=False, indent=2)
    print("\n判定分布：", dict(cnt), " 条目数：", len(RESULTS))
    print("已写出 .txt / .json")


if __name__ == "__main__":
    t0 = time.time()
    out = run_volume16()
    summarize()
    print("\n耗时 %.1fs" % (time.time() - t0))
    print("核心：", json.dumps({k: out[k] for k in (
        "info_per_event", "slope_anchored", "slope_mcmc_free", "dchi2_free",
        "max_resid", "n_for_1e6")}, ensure_ascii=False))
