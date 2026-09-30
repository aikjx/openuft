# -*- coding: utf-8 -*-
"""
TUFT 卷二十三 · 全局 MCMC 贝叶斯联合推断（OPEN_v1）
====================================================
诚实边界声明（红线：数学自洽 != 实验证实；本卷统计方法论的
"全局统一拟合成功"结论被既有事实推翻，见 §0 勘误）：

  * 本卷草稿称"8 通道联合拟合，存在允许的 T_B 后验区间同时满足全部 8 通道"。
    这是**错误**的：据 2026-09-30 更正（记忆 ID 84665624），TUFT 四个微观/
    可检验窗口（g-2、EDM、β 跑动、ringdown）**已全部关闭**：
      - EDM：真实 TUFT 推导预言 1.409e-13 e·cm，超 ACME 2018 上限 1.1e-29 e·cm
             达 1.28e16 倍 ⇒ 已排除（与参数池无关，属固定数值）；
      - g-2：a_TUFT = α/(8π) = 2.904e-4，vs 实验 1.159652e-3，偏差 74.96% ⇒ 已排除；
      - ringdown：σ_abs=0 反射壁在 r_s=2.05M，与 LIGO 所需差 26 量级、
             联合排除 5.74σ ⇒ 已关闭。
    ⇒ 含这 3 个通道（EDM/g-2/ringdown，即通道 1/2/3）的 8 通道联合似然对
      **所有**参数样本恒为 0，后验为空，证据 Z = 0（严格，无需采样）。
    本卷代码据此将通道 1/2/3 硬编码为 CLOSED（恒返回 logL=-inf），
    不假装"联合拟合成功"。

  * CMB 通道（4/5）的 n_s, r **仅由 tau_star 决定**（本卷势 V=v0(1-e^{-τ²})
    中 g3 在 V'/V、V''/V 中相消，见卷二十二数值核验）。故 CMB 轴与 FRG 参数池
    **脱耦**：单参数池"耦合所有通道"对 CMB 轴结构上是空的。
    诚实推论：CMB-only 拟合只约束 tau_star≈2.7，对其余 18 个参数零约束。

  * 草稿前向模型 d_e = C_ferm * T_B 不是 TUFT 推导出的 EDM（真实推导值
    1.409e-13 e·cm，与参数池无关）；本卷用 CLOSED 通道表达排除，不再用该线性近似。

  * 草稿先验是桩（仅约束 g, lam 两个参数）。本卷实现全部 19 个参数的
    平坦 / 对数平坦先验，范围显式写入审计日志，避免人为裁剪。

  * 草稿 tau_star=0.35 落在本势陡坡非慢滚区（卷二十二核验：n_s=-62, r=231，
    已被 BICEP 排除 ~4 量级）。本卷 tau_star 先验覆盖 [0.1,5]，CMB 拟合
    自然把后验推到平台区 ~2.7。

  * 环境：jax/dynesty 未安装。本卷用 numpy + 解析慢滚导数重写前向模型
    （可运行，依赖 numpy/scipy/emcee）；dynesty 嵌套采样用守卫包住，
    缺失时改建证分析（见 §嵌套采样诚实结论：3 通道关闭 ⇒ Z_TUFT=0 严格）。

  * 通道 6/7（CKM/PMNS）与 f_NL（通道 8）的前向映射在 TUFT 中**尚未推导**
    （卷二十一味物理仍为待检验假设，f_NL 阶跃未计算）。本卷标记为 UNVALIDATED，
    似然中**不激活**（贡献 0，不伪造），仅保留架构占位。
"""

import sys
import hashlib
import json

import numpy as np
from scipy.integrate import solve_ivp

try:
    import emcee
    _HAS_EMCEE = True
except Exception as _e:  # pragma: no cover
    _HAS_EMCEE = False
    _EMCEE_ERR = _e

try:
    import dynesty
    _HAS_DYNESTY = True
except Exception as _e:  # pragma: no cover
    _HAS_DYNESTY = False
    _DYNESTY_ERR = _e


# Windows GBK 控制台无法编码 emoji/箭头，统一改 utf-8 容错（不影响文件日志）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ========== 全局参数空间（19 维，与草稿 §2 一致） ==========
# (g, lam, g1, g2, g3, g4, a0..a4, C_ferm, wu,wc,wt,we,wmu,wtau, tau_star)
PRIORS = [
    # name, lo, hi, kind('flat'|'log')
    ("g", 1e-3, 0.5, "flat"),
    ("lam", 1e-3, 0.5, "flat"),
    ("g1", 1e-3, 0.5, "flat"),
    ("g2", 1e-3, 0.5, "flat"),
    ("g3", 1e-3, 0.5, "flat"),
    ("g4", 1e-3, 0.5, "flat"),
    ("a0", -1.0, 1.0, "flat"),
    ("a1", -1.0, 1.0, "flat"),
    ("a2", -1.0, 1.0, "flat"),
    ("a3", -1.0, 1.0, "flat"),
    ("a4", -1.0, 1.0, "flat"),
    ("C_ferm", 1e-4, 1.0, "log"),
    ("wu", 1e18, 1e24, "log"),
    ("wc", 1e18, 1e24, "log"),
    ("wt", 1e18, 1e24, "log"),
    ("we", 1e18, 1e24, "log"),
    ("wmu", 1e18, 1e24, "log"),
    ("wtau", 1e18, 1e24, "log"),
    ("tau_star", 0.1, 5.0, "flat"),
]
NDIM = len(PRIORS)
TAU_IDX = NDIM - 1  # tau_star 在末位


# ========== FRG Beta 流（继承卷21/22，numpy 版） ==========
def beta_frg(g):
    g, lam, g1, g2, g3, g4, a0, a1, a2, a3, a4, gs, gw, gy = g
    bg = 0.6 * g**2 - 0.3 * g * g3
    blam = -1.2 * lam * g + 0.4 * g**2 + 0.25 * g3**2
    bg1 = 0.9 * g1**2 + 0.2 * g1 * g2 - 0.55 * g * g1 + 0.18 * g * g3
    bg2 = 0.8 * g2**2 + 0.22 * g1 * g2 - 0.48 * g * g2
    bg3 = 0.65 * g3**2 - 0.36 * g * g3 + 0.18 * g1 * g3 + 0.1 * g2 * g3
    bg4 = 0.55 * g4**2 + 0.28 * g3 * g4
    ba0 = -4 * a0 + 0.1 * g3 * a2
    ba1 = -3 * a1 + 0.2 * g3 * a3
    ba2 = -2 * a2 + 0.3 * g3 * a4
    ba3 = -1 * a3 - 0.15 * g * a1
    ba4 = -0.2 * g * a2
    b_gs = -1.0 / (16 * np.pi**2) * (11 - 2.0 / 3 * 3) * gs**3 + 0.02 * g3 * gs
    b_gw = 1.0 / (16 * np.pi**2) * (22.0 / 3 - 2.0 / 3 * 3) * gw**3 + 0.015 * g3 * gw
    b_gy = 1.0 / (16 * np.pi**2) * (44.0 / 3 + 2.0 / 3 * 3) * gy**3 + 0.01 * g3 * gy
    return np.array([bg, blam, bg1, bg2, bg3, bg4, ba0, ba1, ba2, ba3, ba4, b_gs, b_gw, b_gy])


def frg_flow(uv_vec):
    """积分 FRG 流，返回 (g3_ir, T_B) 或 None（积分失败=自洽惩罚）。"""
    def ode(s, y):
        return beta_frg(y)
    try:
        sol = solve_ivp(ode, (-8.0, 8.0), uv_vec, method="RK45",
                         rtol=1e-6, atol=1e-8)
    except Exception:
        return None
    if not sol.success:
        return None
    g3_ir = float(sol.y[4, -1])
    T_B = 1.2e-10 * g3_ir
    return g3_ir, T_B


# ========== 挠率势与慢滚（解析导数，g3 在比值中相消） ==========
def slow_roll(tau, g3_ir):
    v0 = 0.01 * g3_ir
    e = np.exp(-tau**2)
    V = v0 * (1.0 - e)
    if V <= 0:
        return dict(eps=np.inf, eta=np.inf, V=V, ns=np.nan, r=np.inf, nt=np.nan, slow=False)
    Vp = v0 * 2.0 * tau * e
    Vpp = v0 * 2.0 * e * (1.0 - 2.0 * tau**2)
    eps = 0.5 * (Vp / V) ** 2
    eta = Vpp / V
    ns = 1.0 - 6.0 * eps + 2.0 * eta
    r = 16.0 * eps
    nt = -r / 8.0
    slow = (eps < 0.1) and (abs(eta) < 0.1)
    return dict(eps=eps, eta=eta, V=V, ns=ns, r=r, nt=nt, slow=slow)


# ========== 前向映射算子 ==========
def forward_model(theta, frg=True):
    (g, lam, g1, g2, g3, g4, a0, a1, a2, a3, a4, C_ferm,
     wu, wc, wt, we, wmu, wtau, tau_star) = theta
    if frg:
        res = frg_flow(np.array([g, lam, g1, g2, g3, g4, a0, a1, a2, a3, a4,
                                 0.36, 0.18, 0.12]))  # gs,gw,gy 取草稿值
        if res is None:
            return dict(ok=False, reason="FRG integration failed")
        g3_ir, T_B = res
    else:
        # n_s, r 与 g3_ir 无关（g3 在 V'/V、V''/V 中相消），似然阶段可跳过 FRG
        g3_ir, T_B = 1.0, float("nan")
    sr = slow_roll(tau_star, g3_ir)
    # 微观可观测量（CLOSED 通道，仅用于审计输出；非 TUFT 真实推导）
    d_e_adhoc = C_ferm * T_B
    g2_shift_adhoc = 0.85 * C_ferm * T_B
    delta_omega_adhoc = 0.42 * T_B * (1 - 0.7)
    return dict(ok=True, g3_ir=g3_ir, T_B=T_B,
                ns=sr["ns"], r=sr["r"], nt=sr["nt"], slow=sr["slow"],
                eps=sr["eps"], eta=sr["eta"],
                d_e_adhoc=d_e_adhoc, g2_shift_adhoc=g2_shift_adhoc,
                delta_omega_adhoc=delta_omega_adhoc, tau_star=tau_star)


# ========== 八大观测通道 ==========
CLOSED_REASON = {
    "EDM": "TUFT 真实推导 EDM=1.409e-13 e·cm，超 ACME 2018 上限 1.1e-29 e·cm 达 "
            "1.28e16 倍（2026-09-30 更正）；与参数池无关，恒排除。",
    "g2": "a_TUFT=alpha/(8pi)=2.904e-4 vs 实验 1.159652e-3，偏差 74.96%"
          "（2026-09-30 更正）；恒排除。",
    "ringdown": "sigma_abs=0 反射壁在 r_s=2.05M，与 LIGO 所需差 26 量级、"
                "联合排除 5.74sigma（OPEN_v4）；恒排除。",
}

# 通道状态：OPEN / CLOSED / UNVALIDATED
CHANNELS = {
    "EDM":       dict(status="CLOSED",      kind="micro"),
    "g2":        dict(status="CLOSED",      kind="micro"),
    "ringdown":  dict(status="CLOSED",      kind="gw"),
    "ns":        dict(status="OPEN",        kind="cmb"),
    "r":         dict(status="OPEN",        kind="cmb"),
    "CKM":       dict(status="UNVALIDATED", kind="flavor"),
    "PMNS":      dict(status="UNVALIDATED", kind="flavor"),
    "f_NL":      dict(status="UNVALIDATED", kind="cmb"),
}


def _ll_edm(fm):
    return -np.inf  # CLOSED

def _ll_g2(fm):
    return -np.inf  # CLOSED

def _ll_ringdown(fm):
    return -np.inf  # CLOSED

def _ll_ns(fm):
    # Planck 2018: ns=0.9649 +- 0.0042（对角近似）
    return -0.5 * ((fm["ns"] - 0.9649) / 0.0042) ** 2

def _ll_r(fm):
    # BICEP/Keck: r<0.032 (95% CL)，单边上限
    if fm["r"] > 0.032:
        return -100.0
    return 0.0

_LL_FUNCS = {
    "EDM": _ll_edm, "g2": _ll_g2, "ringdown": _ll_ringdown,
    "ns": _ll_ns, "r": _ll_r,
    # UNVALIDATED 不激活（贡献 0），不在此登记
}

_OPEN_OR_UNVAL = ["ns", "r", "CKM", "PMNS", "f_NL"]


def log_likelihood(fm, include_closed=False):
    ll = 0.0
    # OPEN CMB
    ll += _ll_ns(fm)
    ll += _ll_r(fm)
    # UNVALIDATED：不激活（贡献 0，不伪造）
    if include_closed:
        # CLOSED 通道恒 -inf ⇒ 整条链 -inf
        ll += _ll_edm(fm)
        ll += _ll_g2(fm)
        ll += _ll_ringdown(fm)
    return ll


# ========== 先验（全 19 维显式） ==========
def log_prior(theta):
    lp = 0.0
    for (name, lo, hi, kind), val in zip(PRIORS, theta):
        if not (lo < val < hi):
            return -np.inf
        if kind == "log":
            lp -= np.log(val)
        else:
            lp -= np.log(hi - lo)
    return lp


def log_prob(theta, include_closed=False, frg=False):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    fm = forward_model(theta, frg=frg)
    if not fm["ok"]:
        return -np.inf  # 自洽惩罚（FRG 积分失败等）
    ll = log_likelihood(fm, include_closed=include_closed)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


# ========== MCMC（emcee） ==========
def _init_walkers(nwalkers, rng, tau_center=2.7):
    p0 = np.empty((nwalkers, NDIM))
    for i, (name, lo, hi, kind) in enumerate(PRIORS):
        if kind == "log":
            p0[:, i] = np.exp(rng.uniform(np.log(lo), np.log(hi), nwalkers))
        else:
            p0[:, i] = rng.uniform(lo, hi, nwalkers)
    p0[:, TAU_IDX] = rng.uniform(tau_center - 0.5, tau_center + 0.5, nwalkers)
    return p0


def run_open_mcmc(nsteps=2000, nwalkers=64, seed=20260930):
    if not _HAS_EMCEE:
        print("[WARN] emcee 缺失：%s" % _EMCEE_ERR)
        return None
    rng = np.random.default_rng(seed)
    p0 = _init_walkers(nwalkers, rng)
    sampler = emcee.EnsembleSampler(nwalkers, NDIM, log_prob, args=(False,))
    sampler.run_mcmc(p0, nsteps, progress=False)
    chain = sampler.get_chain(discard=max(100, nsteps // 4), thin=10, flat=True)
    return sampler, chain


def run_full_demo(nsteps=400, nwalkers=64, seed=7):
    """演示：含 CLOSED 通道时，所有 walker 的 log_prob 恒 -inf ⇒ 后验为空。"""
    if not _HAS_EMCEE:
        print("[WARN] emcee 缺失：%s" % _EMCEE_ERR)
        return None
    rng = np.random.default_rng(seed)
    p0 = _init_walkers(nwalkers, rng)
    sampler = emcee.EnsembleSampler(nwalkers, NDIM, log_prob, args=(True,))
    sampler.run_mcmc(p0, nsteps, progress=False)
    chain = sampler.get_chain(discard=50, thin=10, flat=True)
    lps = np.array([log_prob(row, True) for row in chain])
    return sampler, chain, lps


# ========== 嵌套采样 / 证据（诚实处理） ==========
def run_nested_open():
    """OPEN 通道（CMB-only）的贝叶斯证据。CLOSED 通道使全 8 通道 Z=0（严格）。"""
    if not _HAS_DYNESTY:
        print("[INFO] dynesty 缺失；全 8 通道证据 Z_TUFT=0 严格（3 通道恒排除）。")
        print("       OPEN(CMB-only) 证据需 dynesty；此处仅给定性结论（有限、"
              "由 tau_star 主导，强先验依赖）。")
        return None
    # 简化：对 OPEN 模型（仅 tau_star 有效）跑 dynesty 需要自定义 prior 变换，
    # 此处留接口，不做完整实现（避免伪造数值）。
    print("[INFO] dynesty 可用但未在此 v1 跑完整 OPEN 证据（需 prior 变换实现）。")
    return None


# ========== 后验审计 + SHA256 ==========
def audit_best(chain):
    if chain is None or len(chain) == 0:
        return None
    # 取 tau_star 边际后验统计（n_s, r 与 g3_ir 无关，无需 FRG）
    ts = chain[:, TAU_IDX]
    lo, med, hi = np.percentile(ts, [16, 50, 84])
    sr = slow_roll(med, 1.0)
    payload = dict(
        tau_star_1sigma=[float(lo), float(hi)],
        tau_star_median=float(med),
        ns=float(sr["ns"]), r=float(sr["r"]),
        g3_ir=float("nan"), T_B=float("nan"),
    )
    blob = json.dumps(payload, sort_keys=True).encode("utf-8")
    payload["sha256"] = hashlib.sha256(blob).hexdigest()
    return payload


# ========== 主入口 ==========
def _demo():
    print("=" * 70)
    print("TUFT 卷二十三 · 全局 MCMC 贝叶斯联合推断（OPEN_v1）· 诚实演示")
    print("=" * 70)
    print("通道状态：")
    for k, v in CHANNELS.items():
        mark = {"OPEN": "✅开放", "CLOSED": "❌已关闭", "UNVALIDATED": "⏳未推导"}[v["status"]]
        print("  %-9s %s [%s]" % (k, mark, v["status"]))
    print("-" * 70)

    # 1) OPEN(CMB-only) 拟合：验证流水线可运行，恢复 tau_star
    print("[1] OPEN 通道 MCMC（CMB n_s/r，CKM/PMNS/f_NL 未激活）...")
    res = run_open_mcmc(nsteps=2000, nwalkers=64)
    if res is not None:
        sampler, chain = res
        aud = audit_best(chain)
        ts = chain[:, TAU_IDX]
        print("    样本数=%d，tau_star 1σ=[%.3f, %.3f]，中位=%.3f"
              % (len(ts), aud["tau_star_1sigma"][0], aud["tau_star_1sigma"][1],
                 aud["tau_star_median"]))
        print("    对应 n_s=%.4f, r=%.3e（Planck 0.9649±0.0042 / BICEP r<0.032）"
              % (aud["ns"], aud["r"]))
        print("    诚实注：其余 18 个参数在 CMB-only 下完全无约束（后验=先验）。")
        print("    诚实注：SHA256(tau_star 后验摘要)=%s" % aud["sha256"])
    print("-" * 70)

    # 2) 全 8 通道演示：CLOSED 通道使后验为空
    print("[2] 全 8 通道联合（含 EDM/g-2/ringdown）：")
    if _HAS_EMCEE:
        _, _, lps = run_full_demo(nsteps=400, nwalkers=64)
        n_finite = int(np.sum(np.isfinite(lps)))
        print("    walker 中有限 log_prob 样本数 = %d / %d" % (n_finite, len(lps)))
        print("    ⇒ 联合似然恒为 0，后验为空，8 通道证据 Z_TUFT = 0（严格）。")
    else:
        print("    emcee 缺失，跳过；但由 CLOSED 通道定义即可得 Z_TUFT=0。")
    print("-" * 70)

    # 3) 模型证据比对诚实结论
    print("[3] 模型证据比对（TUFT vs ΛCDM）：")
    print("    Z_TUFT(全8通道) = 0 严格 ⇒ ln B = -∞ ⇒ ΛCDM 压倒性占优。")
    print("    Z_TUFT(OPEN/CMB-only) 有限但参数维度 19 ≫ ΛCDM~6 ⇒ "
          "Occam 罚项使 ln B 仍为负（先验依赖，须敏感性测试）。")
    print("    草稿『量化 TUFT 相对 ΛCDM 的统计优势』方向反了：")
    print("    诚实预期是统计劣势。")
    print("=" * 70)


if __name__ == "__main__":
    if not _HAS_EMCEE:
        print("[WARN] 需安装 emcee（本环境 numpy/scipy 已具备）。")
        sys.exit(0)
    _demo()
