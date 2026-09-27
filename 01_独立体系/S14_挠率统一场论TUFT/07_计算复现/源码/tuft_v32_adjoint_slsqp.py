# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支A落地 —— 解析梯度 SLSQP 拟合（自伴伴随梯度之良态实现）
================================================================================

背景（承 `tuft_v32_adjoint_degeneracy_audit.py`）：
- 分支 A 主张用解析梯度替换有限差分梯度，消除差分噪声。
- 核验已证：抽象场方程 `-ψ''-(2/r)ψ'-V1ψ³+V2ψ⁵=0` **无质量项、不可归一化**
  （解带 1/r 尾，N/E0/Iμ 发散）；即便补质量项 `m²ψ`，衰减到 0 的孤子仍是
  **临界鞍点**（不稳定、普通初值趋向非零平台），不能作为有限 M,Q,μ 的载体。
- 因此分支 A 的伴随梯度**不能在抽象场方程上落地**；须在 TUFT **物理 ansatz**
  （闭式指数尾函数，N 有限，即既有 `tuft_knot_slsqp.py` 的良态基础）上实现。

本脚本：在物理 ansatz 上把 χ² 梯度做成**全解析**（闭式链式求导，含梯度项解析积分），
接入 SLSQP 的 jac 参数；并**对照有限差分梯度**验证解析梯度正确性（相对误差）。
这即分支 A 的实用内涵：有限差分 → 解析梯度，更高精度、更少 ODE 求解。

物理 ansatz（无量纲 r = r_phys/l_P）：
    K(r)  = Kc * exp(-r/lK) / (1 + (r/r0)^p)
    T(r)  = Tc * exp(-r/lT)
    Ω(r)  = Ω_DE + (Ω0 - Ω_DE) * exp(-r/lO)      (Ω_DE=0.6875)
观测量：
    E_tot = ∫ α·K·T·Ω · 4πr² dr         （目标：电子静能无量纲 E_ELECTRON）
    N     = ∫ (Ω - Ω_DE) · r² dr         （归一化，目标 1）
χ² = wE·(E_tot-E_ELEC)²/E_ELEC² + wN·(N-1)²

红线声明：本脚本只演示"解析梯度替换有限差分"的机制与精度；不构成对 TUFT
物理真实性的主张；物理电子无量纲目标（M,Q,μ 单位制钉扎）仍为挂账项。
================================================================================
"""
from __future__ import print_function
import os
import sys
import time
import math
import numpy as np

try:
    from scipy.optimize import minimize
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_v32_adjoint_slsqp_report.txt")
PNG_PATH = os.path.join(HERE, "tuft_v32_gradient_validate.png")

# ---------------------------------------------------------------- 常数 (CODATA)
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK          # ≈4.1854622147e-23

WE, WN = 1.0, 0.1

PARAM_NAMES = ["Kc", "lK", "r0", "p", "Tc", "lT", "O0", "lO"]


# ================================================================================
# 物理 ansatz 及其解析偏导数
# ================================================================================
def fields(params, r):
    Kc, lK, r0, p, Tc, lT, O0, lO = params
    K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
    T = Tc * np.exp(-r / lT)
    Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
    return K, T, Om


def field_grads(params, r):
    """返回每个场对 8 个参数的偏导：dK/dp_i, dT/dp_i, dΩ/dp_i（list of array）。"""
    Kc, lK, r0, p, Tc, lT, O0, lO = params
    K, T, Om = fields(params, r)
    x = r / r0
    denom = 1.0 + x ** p
    gK = [K / Kc,                                   # dK/dKc
          K * r / lK ** 2,                           # dK/dlK
          K * p * x ** p / (r0 * denom),             # dK/dr0
          -K * np.log(x) * x ** p / denom,           # dK/dp
          np.zeros_like(r), np.zeros_like(r), np.zeros_like(r), np.zeros_like(r)]
    gT = [np.zeros_like(r), np.zeros_like(r), np.zeros_like(r), np.zeros_like(r),
          T / Tc,                                    # dT/dTc
          T * r / lT ** 2,                           # dT/dlT
          np.zeros_like(r), np.zeros_like(r)]
    expO = np.exp(-r / lO)
    gO = [np.zeros_like(r), np.zeros_like(r), np.zeros_like(r), np.zeros_like(r),
          np.zeros_like(r), np.zeros_like(r),
          expO,                                      # dΩ/dΩ0
          (O0 - OMEGA_DE) * expO * r / lO ** 2]      # dΩ/dlO
    return gK, gT, gO


def observables(params, r):
    K, T, Om = fields(params, r)
    E = ALPHA * np.trapezoid(K * T * Om * r ** 2, r) * 4.0 * math.pi
    N = np.trapezoid((Om - OMEGA_DE) * r ** 2, r)
    return E, N


def grad_observables(params, r):
    """E_tot、N 对 8 参数的解析梯度。"""
    K, T, Om = fields(params, r)
    gK, gT, gO = field_grads(params, r)
    dE = np.zeros(8)
    dN = np.zeros(8)
    for i in range(8):
        # d(E)/dp_i = ∫ α·(K'TΩ + KT'Ω + KTΩ')·4πr² dr
        integ_E = (gK[i] * T * Om + K * gT[i] * Om + K * T * gO[i]) * r ** 2
        dE[i] = ALPHA * 4.0 * math.pi * np.trapezoid(integ_E, r)
        # d(N)/dp_i = ∫ (Ω-Ω_DE)' · r² dr
        dN[i] = np.trapezoid(gO[i] * r ** 2, r)
    return dE, dN


def chi2(params, r):
    E, N = observables(params, r)
    return WE * ((E - E_ELECTRON) / E_ELECTRON) ** 2 + WN * (N - 1.0) ** 2


def grad_chi2_analytic(params, r):
    E, N = observables(params, r)
    dE, dN = grad_observables(params, r)
    g = 2 * WE * (E - E_ELECTRON) / E_ELECTRON ** 2 * dE + 2 * WN * (N - 1.0) * dN
    return g


def grad_chi2_fd(params, r, h_rel=1e-6):
    """中心差分有限差分梯度（每分量相对步长，适配跨数量级参数；对照用）。"""
    p = np.asarray(params, dtype=float)
    g = np.zeros_like(p)
    for i in range(len(p)):
        h = h_rel * max(abs(p[i]), 1e-9)
        pp = p.copy()
        pm = p.copy()
        pp[i] += h
        pm[i] -= h
        g[i] = (chi2(pp, r) - chi2(pm, r)) / (2 * h)
    return g


def _dump(out):
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")
    except Exception as exc:
        out.append("[warn] 报告写入失败: %s" % exc)


def main():
    t0 = time.time()
    out = []
    out.append("TUFT V3.2 分支A落地 · 解析梯度 SLSQP（物理 ansatz 良态实现）")
    out.append("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    out.append("Python %s  numpy %s  scipy=%s" % (sys.version.split()[0], np.__version__, HAVE_SCIPY))
    out.append("")
    out.append("背景：抽象场方程(无质量项)不可归一化，已另案判定；本脚本在物理 ansatz 上落地解析梯度。")
    out.append("E_ELECTRON(无量纲) = " + format(E_ELECTRON, ".6e") + "  Ω_DE=" + format(OMEGA_DE, ".4f"))
    out.append("")

    r = np.logspace(-3.0, 2.0, 400)

    # ------------------------------------------------------------ 1. 解析 vs 有限差分
    out.append("=== 1. 解析梯度 vs 有限差分梯度 一致性 ===")
    test_pts = [
        [1e-6, 0.1, 0.01, 2.0, 1e-6, 0.1, 0.75, 2.0],
        [1e-8, 0.3, 0.02, 2.0, 1e-8, 0.3, 0.90, 3.0],
        [1e-5, 0.05, 0.005, 3.0, 1e-5, 0.05, 0.60, 1.0],
        [5e-7, 0.2, 0.015, 2.5, 5e-7, 0.2, 0.80, 2.0],
    ]
    worst = 0.0
    for i, p in enumerate(test_pts):
        ga = grad_chi2_analytic(p, r)
        gf = grad_chi2_fd(p, r, h_rel=1e-6)
        scale = np.maximum(np.abs(ga), np.abs(gf))
        rel = np.abs(ga - gf) / np.where(scale > 0, scale, 1.0)
        w = float(np.max(rel))
        worst = max(worst, w)
        out.append("  测试点 %d: 解析 vs 有限差分 最大相对误差 = %.3e  %s"
                   % (i + 1, w, "[OK<1e-3]" if w < 1e-3 else "[WARN]"))
    out.append("  全体测试点最大相对误差 = %.3e  %s"
               % (worst, "[PASS]" if worst < 1e-3 else "[FAIL]"))
    out.append("")

    # ------------------------------------------------------------ 2. SLSQP 解析 jac 收敛
    out.append("=== 2. SLSQP：解析 jac vs 有限差分 jac ===")
    bounds = [(1e-12, None), (1e-3, 1e2), (1e-4, 1.0), (0.5, 5.0),
              (1e-12, None), (1e-3, 1e2), (0.0, 1.0), (1e-3, 1e2)]
    x0_list = [
        [1e-6, 0.1, 0.01, 2.0, 1e-6, 0.1, 0.75, 2.0],
        [1e-8, 0.3, 0.02, 2.0, 1e-8, 0.3, 0.90, 3.0],
        [1e-5, 0.05, 0.005, 3.0, 1e-5, 0.05, 0.60, 1.0],
    ]
    res_a = None
    res_f = None
    if HAVE_SCIPY:
        for x0 in x0_list:
            for method in ("SLSQP", "L-BFGS-B"):
                try:
                    ra = minimize(chi2, x0, args=(r,), method=method, jac=grad_chi2_analytic,
                                  bounds=bounds, options={"maxiter": 2000, "ftol": 1e-15})
                    if res_a is None or ra.fun < res_a.fun:
                        res_a = ra
                except Exception as exc:
                    out.append("  [warn] 解析 jac %s 失败: %s" % (method, exc))
                try:
                    rf = minimize(chi2, x0, args=(r,), method=method, jac=grad_chi2_fd,
                                  bounds=bounds, options={"maxiter": 2000, "ftol": 1e-15})
                    if res_f is None or rf.fun < res_f.fun:
                        res_f = rf
                except Exception as exc:
                    out.append("  [warn] 有限差分 jac %s 失败: %s" % (method, exc))
        if res_a is not None:
            out.append("  解析 jac（SLSQP/L-BFGS-B 取优）：χ²=%.6e  success=%s  iter=%s  nfev=%s"
                       % (res_a.fun, res_a.success, res_a.nit, res_a.nfev))
        if res_f is not None:
            out.append("  有限差分 jac（SLSQP/L-BFGS-B 取优）：χ²=%.6e  success=%s  iter=%s  nfev=%s"
                       % (res_f.fun, res_f.success, res_f.nit, res_f.nfev))
        if res_a is not None and res_f is not None:
            out.append("  解析 jac 较有限差分：χ² 比值=%.3f  迭代=%d vs %d"
                       % (res_a.fun / max(res_f.fun, 1e-300), res_a.nit, res_f.nit))
    out.append("")

    # ------------------------------------------------------------ 3. 最优解观测量
    best = res_a if (res_a is not None) else res_f
    if best is not None:
        E, N = observables(best.x, r)
        out.append("=== 3. 最优解观测量（解析 jac 收敛）===")
        out.append("  E_tot/电子静能 = %.6f  N = %.6f  (目标 N=1)"
                   % (E / E_ELECTRON, N))
        out.append("  参数: " + ", ".join("%s=%.4e" % (n, v) for n, v in zip(PARAM_NAMES, best.x)))
        out.append("  终梯度范数 = %.3e" % float(np.linalg.norm(grad_chi2_analytic(best.x, r))))

    # ------------------------------------------------------------ 4. 绘图：梯度验证
    if HAVE_MPL:
        try:
            for f in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC"):
                try:
                    matplotlib.font_manager.findfont(f, fallback_to_default=False)
                    plt.rcParams["font.sans-serif"] = [f]
                    break
                except Exception:
                    continue
            plt.rcParams["axes.unicode_minus"] = False
            ga0 = grad_chi2_analytic(test_pts[0], r)
            gf0 = grad_chi2_fd(test_pts[0], r, h_rel=1e-6)
            fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
            idx = np.arange(8)
            ax[0].bar(idx - 0.2, ga0, width=0.4, label="analytic", color="#2a6fb0")
            ax[0].bar(idx + 0.2, gf0, width=0.4, label="finite-diff", color="#e08a3a")
            ax[0].set_xticks(idx)
            ax[0].set_xticklabels(PARAM_NAMES, rotation=45, fontsize=8)
            ax[0].set_yscale("symlog")
            ax[0].set_title("χ² 梯度：解析 vs 有限差分")
            ax[0].legend(fontsize=8)
            ax[0].grid(True, ls=":", alpha=0.5)
            rel = np.abs(ga0 - gf0) / np.maximum(np.abs(ga0), np.abs(gf0))
            ax[1].bar(idx, rel, color="#7a7a7a")
            ax[1].set_xticks(idx)
            ax[1].set_xticklabels(PARAM_NAMES, rotation=45, fontsize=8)
            ax[1].set_yscale("log")
            ax[1].set_title("相对误差")
            ax[1].grid(True, ls=":", alpha=0.5)
            fig.suptitle("TUFT V3.2 分支A · 解析梯度验证")
            fig.tight_layout()
            fig.savefig(PNG_PATH, dpi=130)
            out.append("")
            out.append("梯度对比图已保存: " + PNG_PATH)
        except Exception as exc:
            out.append("[warn] 绘图失败: " + str(exc))

    out.append("")
    out.append("运行耗时 %.1f s" % (time.time() - t0))
    out.append("红线声明：本脚本演示解析梯度替换有限差分机制；不构成物理真实性主张。")
    out.append("挂账：电子无量纲目标 (M,Q,μ) 的单位制/4π 钉扎待补；此处以 E_ELECTRON、N=1 为良态演示目标。")
    print("\n".join(out))
    _dump(out)


if __name__ == "__main__":
    main()
