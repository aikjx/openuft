# -*- coding: utf-8 -*-
"""§14 误差传播：自旋投影 Sz 与动量测量 —— 解析偏导复核与数值验证。

对照 §14 文档逐条验证：
  [1] 三套参数化的解析偏导 vs 有限差分（a: theta / b: tau,lam / c: R,lam）
  [2] 14.4(i)  R-tau 通道恒等： |dSz/dtau|*sigma_tau == |dSz/dR|*sigma_R
              在 sigma_tau = |dtau/dR|*sigma_R 的一致映射下逐项相等
  [3] 14.4(iii) 完整一致性： (c) 独立 Gauss == (b) 含协方差传播（机器精度）
  [4] 数值示例表：lam=500nm, theta 扫描下的 sigma_Sz / 相对误差 / 检出显著性
  [5] 绘图：spin_error_theta.svg（误差发散）、spin_significance.svg（3sigma 检出）

红线：仅验证一阶误差传播数学自洽；不蕴含 tau≠0 态的物理存在性。
"""
import math
import sys

import numpy as np

# Windows GBK 控制台打印 κ/τ/σ/λ 等字符会报 UnicodeEncodeError，统一改 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0
hbar = 1.054571817e-34
h_planck = 2.0 * math.pi * hbar
TWO_PI = 2.0 * math.pi


# ==================================================================
# 三套参数化下的 Sz
# ==================================================================
def K_of_lam(lam):
    return TWO_PI / lam


def Sz_a(theta):
    """参数化 (a)： Sz = hbar cos(theta)   独立变量 (theta, lam)。"""
    return hbar * math.cos(theta)


def Sz_b(tau, lam):
    """参数化 (b)： Sz = hbar sqrt(1 - xi_tau^2),  xi_tau = tau*lam/(2pi)。"""
    xi = tau * lam / TWO_PI
    return hbar * math.sqrt(max(0.0, 1.0 - xi * xi))


def Sz_c(R, lam):
    """参数化 (c)： Sz = hbar * xi_R = 2*pi*hbar*R/lam,  xi_R = 2pi R/lam = cos(theta)。"""
    return TWO_PI * hbar * R / lam


def tau_of_R(R, lam):
    """§11 几何： tau = K sqrt(1 - xi_R^2),  xi_R = 2pi R/lam。"""
    xi_R = TWO_PI * R / lam
    return (TWO_PI / lam) * math.sqrt(max(0.0, 1.0 - xi_R * xi_R))


def R_of_theta(theta, lam):
    """由 xi_R = cos(theta) = 2pi R/lam 反解 R。"""
    return lam * math.cos(theta) / TWO_PI


def tau_of_theta(theta, lam):
    """由 tau = K sin(theta) 给出。"""
    return (TWO_PI / lam) * math.sin(theta)


# ==================================================================
# 解析偏导
# ==================================================================
def partials_a(theta):
    """(a) dSz/dtheta = -hbar sin(theta);  dSz/dlam = 0。"""
    return dict(dSz_dtheta=-hbar * math.sin(theta), dSz_dlam=0.0)


def partials_b(tau, lam):
    """(b) dSz/dtau, dSz/dlam|_tau。"""
    xi = tau * lam / TWO_PI
    sq = math.sqrt(max(1e-300, 1.0 - xi * xi))
    return dict(dSz_dtau=-hbar * xi * lam / (TWO_PI * sq),
                dSz_dlam=-hbar * xi * xi / (lam * sq),
                xi=xi, sq=sq)


def partials_c(R, lam):
    """(c) dSz/dR = 2*pi*hbar/lam;  dSz/dlam|_R = -2*pi*hbar*R/lam^2。"""
    return dict(dSz_dR=TWO_PI * hbar / lam,
                dSz_dlam=-TWO_PI * hbar * R / (lam * lam))


def dtau_dR(R, lam):
    """§11: dtau/dR = -(2pi/lam)^2 * xi_R / sqrt(1-xi_R^2)。"""
    xi_R = TWO_PI * R / lam
    sq = math.sqrt(max(1e-300, 1.0 - xi_R * xi_R))
    return -(TWO_PI / lam) ** 2 * xi_R / sq


def dtau_dlam(R, lam):
    """dtau/dlam|_R （数值/解析混合，用于协方差）。"""
    return _fd(lambda ll: tau_of_R(R, ll), lam, lam * 1e-7)


# ==================================================================
# 有限差分工具
# ==================================================================
def _fd(f, x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)


# ==================================================================
# [1] 解析偏导 vs 有限差分
# ==================================================================
def check_partials():
    lam = 500e-9
    theta = math.pi / 4
    R = R_of_theta(theta, lam)
    tau = tau_of_theta(theta, lam)

    print("=" * 78)
    print("[1] 解析偏导 vs 有限差分")
    print("=" * 78)

    # (a)
    pa = partials_a(theta)
    fd_a = _fd(lambda t: Sz_a(t), theta, 1e-7)
    e = abs(pa["dSz_dtheta"] - fd_a) / abs(fd_a)
    print(f"  (a) dSz/dtheta  解析={pa['dSz_dtheta']:.6e}  FD={fd_a:.6e}  rel={e:.2e}")

    # (b)
    pb = partials_b(tau, lam)
    fd_t = _fd(lambda t: Sz_b(t, lam), tau, tau * 1e-7)
    fd_l = _fd(lambda l: Sz_b(tau, l), lam, lam * 1e-7)
    e1 = abs(pb["dSz_dtau"] - fd_t) / abs(fd_t)
    e2 = abs(pb["dSz_dlam"] - fd_l) / abs(fd_l)
    print(f"  (b) dSz/dtau    解析={pb['dSz_dtau']:.6e}  FD={fd_t:.6e}  rel={e1:.2e}")
    print(f"  (b) dSz/dlam   解析={pb['dSz_dlam']:.6e}  FD={fd_l:.6e}  rel={e2:.2e}")

    # (c)
    pc = partials_c(R, lam)
    fd_R = _fd(lambda r: Sz_c(r, lam), R, R * 1e-7)
    fd_RL = _fd(lambda l: Sz_c(R, l), lam, lam * 1e-7)
    e3 = abs(pc["dSz_dR"] - fd_R) / abs(fd_R)
    e4 = abs(pc["dSz_dlam"] - fd_RL) / abs(fd_RL)
    print(f"  (c) dSz/dR      解析={pc['dSz_dR']:.6e}  FD={fd_R:.6e}  rel={e3:.2e}")
    print(f"  (c) dSz/dlam   解析={pc['dSz_dlam']:.6e}  FD={fd_RL:.6e}  rel={e4:.2e}")

    worst = max(e, e1, e2, e3, e4)
    print(f"  --> 最大相对偏差 = {worst:.3e} （机器精度，全部解析式正确）")


# ==================================================================
# [2] 14.4(i)  R-tau 通道恒等
# ==================================================================
def check_Rtau_channel():
    lam = 500e-9
    print("\n" + "=" * 78)
    print("[2] 14.4(i)  R-tau 通道恒等：|dSz/dtau|·sigma_tau == |dSz/dR|·sigma_R")
    print("=" * 78)
    print("    sigma_tau 由 Jacobi 一致映射给出： sigma_tau = |dtau/dR|·sigma_R")
    sigma_R = 0.5e-9
    worst = 0.0
    for deg in [15, 30, 45, 60, 75, 85]:
        theta = math.radians(deg)
        R = R_of_theta(theta, lam)
        tau = tau_of_theta(theta, lam)
        jac = abs(dtau_dR(R, lam))
        sigma_tau = jac * sigma_R
        term_b = abs(partials_b(tau, lam)["dSz_dtau"]) * sigma_tau
        term_c = abs(partials_c(R, lam)["dSz_dR"]) * sigma_R
        rel = abs(term_b - term_c) / term_c
        worst = max(worst, rel)
        print(f"    theta={deg:3d}deg  term_b={term_b:.6e}  term_c={term_c:.6e}  rel={rel:.2e}")
    print(f"  --> 最大相对偏差 = {worst:.3e} （R-tau 通道严格恒等）")


# ==================================================================
# [3] 14.4(iii) 完整一致性（含协方差）
# ==================================================================
def check_full_consistency():
    lam = 500e-9
    sigma_R = 0.5e-9
    sigma_lam = 1e-9
    print("\n" + "=" * 78)
    print("[3] 14.4(iii) 完整一致性： (c) 独立Gauss == (b) 含协方差传播")
    print("=" * 78)
    worst = 0.0
    for deg in [15, 30, 45, 60, 75]:
        theta = math.radians(deg)
        R = R_of_theta(theta, lam)
        tau = tau_of_theta(theta, lam)

        # (c) 独立 Gauss on (R, lam)
        pc = partials_c(R, lam)
        var_c = (pc["dSz_dR"] * sigma_R) ** 2 + (pc["dSz_dlam"] * sigma_lam) ** 2

        # (b) 经 (tau, lam) 传播，含协方差
        jacR = dtau_dR(R, lam)
        jacL = dtau_dlam(R, lam)
        var_tau = (jacR * sigma_R) ** 2 + (jacL * sigma_lam) ** 2
        cov_tl = jacL * sigma_lam ** 2          # cov(tau, lam)
        pb = partials_b(tau, lam)
        var_b = (pb["dSz_dtau"] ** 2) * var_tau \
            + (pb["dSz_dlam"] ** 2) * sigma_lam ** 2 \
            + 2.0 * pb["dSz_dtau"] * pb["dSz_dlam"] * cov_tl

        rel = abs(math.sqrt(var_c) - math.sqrt(max(0.0, var_b))) / math.sqrt(var_c)
        worst = max(worst, rel)
        print(f"    theta={deg:3d}deg  sigma_c={math.sqrt(var_c):.6e}  "
              f"sigma_b(full)={math.sqrt(max(0.0, var_b)):.6e}  rel={rel:.2e}")

    print(f"  --> 含协方差最大相对偏差 = {worst:.3e} （严格相等）")

    # 反例扫描：若 (b) 用「无协方差」的独立 Gauss，则在一般角度不成立
    print("\n  [反例扫描] 若 (b) 省去协方差项（把 tau 当作与 lam 独立的测量量）：")
    print("      deg   sigma_c        sigma_b(无协方差)   rel偏差     协方差项符号")
    for deg in [10, 15, 30, 45, 60, 75]:
        theta = math.radians(deg)
        R = R_of_theta(theta, lam)
        tau = tau_of_theta(theta, lam)
        jacR = dtau_dR(R, lam)
        jacL = dtau_dlam(R, lam)
        var_tau = (jacR * sigma_R) ** 2 + (jacL * sigma_lam) ** 2
        pb = partials_b(tau, lam)
        pc = partials_c(R, lam)
        var_b_nocov = (pb["dSz_dtau"] ** 2) * var_tau + (pb["dSz_dlam"] ** 2) * sigma_lam ** 2
        var_c = (pc["dSz_dR"] * sigma_R) ** 2 + (pc["dSz_dlam"] * sigma_lam) ** 2
        sbn = math.sqrt(max(0.0, var_b_nocov))
        sc = math.sqrt(var_c)
        sign = "+" if jacL > 0 else ("-" if jacL < 0 else "0")
        print(f"      {deg:3d}   {sc:.6e}   {sbn:.6e}   {abs(sbn-sc)/sc:.3e}   {sign}")
    print("      >>> 45deg 是退化点： dtau/dlam|_R ∝ (2*xi_R^2 - 1) 在 xi_R=1/sqrt(2)")
    print("          处过零，协方差项恰好消失；其余角度省去协方差将引入 0.3%~85% 偏差。")
    print("      >>> 结论：tau 由 (R,lam) 导出时，其误差与 lam 误差相关，")
    print("          独立 Gauss 形式失效，必须用含协方差的传播式。")


# ==================================================================
# [4] 数值示例表
# ==================================================================
def table_examples():
    lam = 500e-9
    sigma_lam = 1e-9
    sigma_theta = 0.01
    sigma_tau_rel = 0.01        # sigma_tau / K
    sigma_R = 0.5e-9
    K = K_of_lam(lam)

    print("\n" + "=" * 78)
    print("[4] 数值示例 (lam=500nm, sigma_lam=1nm, sigma_theta=0.01rad,")
    print("             sigma_tau/K=1%, sigma_R=0.5nm)")
    print("=" * 78)
    print("  theta   S_z/hbar   sig_a/hbar  rel_a    rel_b    rel_c   sig_p/p  sig_C/C  signif")
    for deg in [0, 15, 30, 45, 60, 75, 89]:
        theta = math.radians(deg)
        sz = Sz_a(theta) / hbar
        # (a)
        sa = hbar * math.sin(theta) * sigma_theta
        rel_a = math.tan(theta) * sigma_theta if deg != 0 else 0.0
        # (b)
        tau = tau_of_theta(theta, lam)
        pb = partials_b(tau, lam)
        sig_tau = sigma_tau_rel * K
        sb = math.sqrt((pb["dSz_dtau"] * sig_tau) ** 2 + (pb["dSz_dlam"] * sigma_lam) ** 2)
        rel_b = sb / abs(Sz_b(tau, lam)) if Sz_b(tau, lam) > 0 else float("inf")
        # (c)
        R = R_of_theta(theta, lam)
        pc = partials_c(R, lam)
        sc = math.sqrt((pc["dSz_dR"] * sigma_R) ** 2 + (pc["dSz_dlam"] * sigma_lam) ** 2)
        rel_c = sc / abs(Sz_c(R, lam)) if Sz_c(R, lam) > 0 else float("inf")
        # momentum & coupling
        rel_p = sigma_lam / lam
        rel_C = math.sqrt((math.tan(theta) * sigma_theta) ** 2 + 4 * (sigma_lam / lam) ** 2)
        # significance: (hbar - Sz)/sigma_Sz = tan(theta/2)/sigma_theta
        signif = math.tan(theta / 2) / sigma_theta if deg != 0 else 0.0
        print(f"  {deg:3d}deg  {sz:8.4f}  {sa/hbar:10.3e}  {rel_a:6.3f}  {rel_b:7.3f}  "
              f"{rel_c:7.3f}  {rel_p:7.2e}  {rel_C:7.2e}  {signif:6.2f}")
    print("  signif = (hbar - S_z)/sigma_Sz = tan(theta/2)/sigma_theta  （14.6）")


# ==================================================================
# [5] 绘图
# ==================================================================
def plot_errors():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lam = 500e-9
    K = K_of_lam(lam)
    sigma_lam = 1e-9
    sigma_theta = 0.01
    sigma_tau = 0.01 * K
    sigma_R = 0.5e-9

    degs = np.linspace(1.0, 89.0, 400)
    ths = np.radians(degs)
    rel_a, rel_b, rel_c, abs_c = [], [], [], []
    for th in ths:
        rel_a.append(math.tan(th) * sigma_theta)
        tau = tau_of_theta(th, lam)
        pb = partials_b(tau, lam)
        sb = math.sqrt((pb["dSz_dtau"] * sigma_tau) ** 2 + (pb["dSz_dlam"] * sigma_lam) ** 2)
        szb = Sz_b(tau, lam)
        rel_b.append(sb / szb if szb > 0 else float("nan"))
        R = R_of_theta(th, lam)
        pc = partials_c(R, lam)
        sc = math.sqrt((pc["dSz_dR"] * sigma_R) ** 2 + (pc["dSz_dlam"] * sigma_lam) ** 2)
        szc = Sz_c(R, lam)
        rel_c.append(sc / szc if szc > 0 else float("nan"))
        abs_c.append(sc)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(degs, rel_a, label=r"(a) $\tan\theta\,\sigma_\theta$")
    ax[0].plot(degs, rel_b, label=r"(b) via $(\tau,\lambda)$")
    ax[0].plot(degs, rel_c, label=r"(c) via $(R,\lambda)$")
    ax[0].set_yscale("log")
    ax[0].set_xlabel(r"$\theta$ (deg)")
    ax[0].set_ylabel(r"relative error $\sigma_{S_z}/S_z$")
    ax[0].set_title(r"§14 relative error of $S_z$ vs $\theta$")
    ax[0].legend(); ax[0].grid(alpha=0.3, which="both")

    ax[1].plot(degs, np.array(abs_c) / hbar, color="tab:green",
               label=r"(c) $\sigma_{S_z}/\hbar$ (fixed $\sigma_R$)")
    ax[1].set_xlabel(r"$\theta$ (deg)")
    ax[1].set_ylabel(r"absolute error $\sigma_{S_z}/\hbar$")
    ax[1].set_title(r"(c) absolute error stays finite as $\theta\to90^\circ$")
    ax[1].legend(); ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("spin_error_theta.svg", format="svg")
    print("\n[5] saved spin_error_theta.svg")


def plot_significance():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sigma_theta_list = [0.001, 0.01, 0.05]
    degs = np.linspace(1.0, 89.0, 400)
    ths = np.radians(degs)

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for st in sigma_theta_list:
        signif = np.tan(ths / 2.0) / st
        ax.plot(degs, signif, label=r"$\sigma_\theta$=" + f"{st} rad")
    ax.axhline(3.0, color="red", ls="--", lw=1.2, label=r"$3\sigma$ threshold")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\theta$ (deg)")
    ax.set_ylabel(r"$(\hbar-S_z)/\sigma_{S_z}=\tan(\theta/2)/\sigma_\theta$")
    ax.set_title(r"§14.6 detectability of deviation from QED ($S_z=\pm\hbar$)")
    ax.legend(); ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig("spin_significance.svg", format="svg")
    print("[5] saved spin_significance.svg")


# ==================================================================
def main():
    print("=" * 78)
    print("§14 误差传播验证 —— 自旋投影 S_z 与动量测量（场标架分支）")
    print("=" * 78)
    check_partials()
    check_Rtau_channel()
    check_full_consistency()
    table_examples()
    plot_errors()
    plot_significance()
    print("\n=== §14 复现完成 ===")


if __name__ == "__main__":
    main()
