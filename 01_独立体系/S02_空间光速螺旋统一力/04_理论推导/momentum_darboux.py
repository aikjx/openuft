# -*- coding: utf-8 -*-
"""§13 光速螺旋场标架：动量密度 + Darboux 动量映射 + 模型对比复现。

对照 §13 文档逐条数值验证：
  - 时间平均动量密度 <g> = eps0|E0|^2/c * e3 （真空横波标准关系）；
  - 单光子动量 p_gamma = hbar K e3；
  - 动量-自旋-Darboux 耦合恒等式 p_gamma·omega_D = K^2 Sz （机器精度闭合）；
  - Part B 单光子动量随弧长 s 的横向振荡分量（时间平均归零，净动量沿 z）；
  - 输出 momentum_evolution.svg / darboux_coupling.svg。

红线：仅验证 S02 场标架分支内几何自洽；不替代 QED，所有预言待实验判决。
"""
import math
import sys

import numpy as np

# Windows GBK 控制台打印 κ/τ/π/² 等字符会报 UnicodeEncodeError，统一改 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0
mu0 = 4.0 * math.pi * 1e-7
eps0 = 1.0 / (mu0 * c ** 2)
hbar = 1.054571817e-34


# ==================================================================
# 场标架几何核心
# ==================================================================
def frenet_frame_lightspeed(s, K, theta):
    """返回 e1,e2,e3,kappa,tau,omegaD（Darboux 向量）。

    【2026-09-24 修正，依据 §15】原 §13 显式标架不满足其自身声明的 Frenet 方程
    （θ≠0 时残差达 O(1)，且 omega_D 随 s 变化），仅在 θ=0 成立。
    现改用 §15.2 修正标架：绕固定 Darboux 轴 omega_D=K*z_hat 以角速率 K 匀角速转动。

        e1 = ( cosθ cosφ,  cosθ sinφ,  sinθ)
        e2 = (-sinφ,       cosφ,       0   )
        e3 = (-sinθ cosφ, -sinθ sinφ,  cosθ),   φ = K s

    校验：Frenet 三式残差 ~1e-16（全 θ）；omega_D = tau*e1+kappa*e3 = K*z_hat 严格恒定。
    注：耦合恒等式 p·omega_D = K^2 Sz 仅依赖正交性，故此修正【不改变】§13 Part A 结论。
    """
    kappa = K * math.cos(theta)
    tau = K * math.sin(theta)
    phi = K * s
    e1 = np.array([math.cos(theta) * math.cos(phi),
                   math.cos(theta) * math.sin(phi),
                   math.sin(theta)])
    e2 = np.array([-math.sin(phi), math.cos(phi), 0.0])
    e3 = np.array([-math.sin(theta) * math.cos(phi),
                   -math.sin(theta) * math.sin(phi),
                   math.cos(theta)])
    omegaD = tau * e1 + kappa * e3
    return e1, e2, e3, kappa, tau, omegaD


def momentum_density(E0, e3):
    """时间平均动量密度 <g> = eps0|E0|^2/c * e3。
    注意：标量版 demo 漏写 1/c，此处修正以保证量纲与标准关系一致。
    """
    return (eps0 * E0 ** 2) / c * e3


def photon_momentum(K, e3):
    """单光子动量 p_gamma = hbar K e3。"""
    return hbar * K * e3


def darboux_coupling(K, theta):
    """返回 (p·omega_D, K^2 Sz, Sz/hbar)。"""
    s = 0.0
    _, _, e3, kappa, tau, omegaD = frenet_frame_lightspeed(s, K, theta)
    p = photon_momentum(K, e3)
    p_dot_omegaD = float(np.dot(p, omegaD))
    Sz = hbar * math.sqrt(max(0.0, 1.0 - (tau / K) ** 2))
    K2Sz = K ** 2 * Sz
    return p_dot_omegaD, K2Sz, Sz / hbar


# ==================================================================
# Part A 数值对照
# ==================================================================
def demo_part_a():
    lam = 500e-9
    K = 2 * math.pi / lam
    theta = math.pi / 4
    s_list = np.linspace(0, 2 * lam, 10)
    E0 = 1.0

    print("=== Light Speed Helix: Momentum & Darboux Inner Product ===")
    max_rel = 0.0
    for s in s_list:
        e1, e2, e3, kappa, tau, omegaD = frenet_frame_lightspeed(s, K, theta)
        g_avg = momentum_density(E0, e3)
        p_gamma = photon_momentum(K, e3)
        p_dot_omegaD = float(np.dot(p_gamma, omegaD))
        Sz = hbar * math.sqrt(max(0.0, 1.0 - (tau / K) ** 2))
        K2Sz = K ** 2 * Sz
        rel = abs(p_dot_omegaD - K2Sz) / abs(K2Sz) if K2Sz != 0 else 0.0
        max_rel = max(max_rel, rel)
        print(f"s={s:.2e}, tau={tau:.2e}, p.wD={p_dot_omegaD:.2e}, "
              f"K2*Sz={K2Sz:.2e}, Sz/hbar={Sz/hbar:.3f}")
    print(f"\n[Part A] 耦合恒等式 max 相对残差 = {max_rel:.3e}（机器精度闭合）")

    # 极限校验
    print("\n[Part A 极限校验]")
    p0, k0, r0 = darboux_coupling(K, 0.0)          # 圆偏振特例
    p1, k1, r1 = darboux_coupling(K, math.pi / 2)  # 纯扭转标架
    print(f"  theta=0   : p.wD={p0:.3e}, K^2*Sz={k0:.3e}, Sz/hbar={r0:.3f}")
    print(f"  theta=pi/2: p.wD={p1:.3e}, K^2*Sz={k1:.3e}, Sz/hbar={r1:.3f}")


# ==================================================================
# Part B 动量随弧长演化（绘图）
# ==================================================================
def momentum_evolution(K, theta, n=400):
    s_list = np.linspace(0.0, 2.0 * (2.0 * math.pi / K), n)  # 2 个波长
    px, py, pz = [], [], []
    for s in s_list:
        e3 = frenet_frame_lightspeed(s, K, theta)[2]
        p = photon_momentum(K, e3)
        px.append(p[0]); py.append(p[1]); pz.append(p[2])
    px, py, pz = np.array(px), np.array(py), np.array(pz)
    return s_list, px, py, pz


def plot_momentum_evolution():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lam = 500e-9
    K = 2 * math.pi / lam
    theta = math.pi / 4
    s_list, px, py, pz = momentum_evolution(K, theta)
    z_nm = s_list * 1e9

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(z_nm, px, label="p_x (transverse)")
    ax[0].plot(z_nm, py, label="p_y (transverse)")
    ax[0].plot(z_nm, pz, label="p_z (axial)")
    ax[0].set_xlabel("arc length s (nm)")
    ax[0].set_ylabel(r"photon momentum (kg m/s)")
    ax[0].set_title(r"Part B: $p_\gamma(s)$ components ($\theta=\pi/4$)")
    ax[0].legend(); ax[0].grid(alpha=0.3)

    # 横向分量时间平均（路径平均）应为零
    mean_px = px.mean(); mean_py = py.mean(); mean_pz = pz.mean()
    ax[1].bar(["<p_x>", "<p_y>", "<p_z>"],
              [mean_px, mean_py, mean_pz],
              color=["tab:blue", "tab:orange", "tab:green"])
    ax[1].set_ylabel("path-averaged momentum (kg m/s)")
    ax[1].set_title("path mean: transverse -> 0, net along z")
    for i, v in enumerate([mean_px, mean_py, mean_pz]):
        ax[1].text(i, v, f"{v:.2e}", ha="center", va="bottom", fontsize=8)
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("momentum_evolution.svg", format="svg")
    print("\n[Part B] saved momentum_evolution.svg")
    print(f"          <p_x>={mean_px:.3e}, <p_y>={mean_py:.3e}, <p_z>={mean_pz:.3e}")


def plot_darboux_coupling():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lam = 500e-9
    K = 2 * math.pi / lam
    theta_list = np.linspace(0.0, math.pi / 2, 200)
    pdot, k2sz, sz_ratio = [], [], []
    for th in theta_list:
        pd, kk, rr = darboux_coupling(K, th)
        pdot.append(pd); k2sz.append(kk); sz_ratio.append(rr)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(theta_list, pdot, label=r"$p_\gamma\cdot\omega_D$")
    ax[0].plot(theta_list, k2sz, "--", label=r"$K^2 S_z$")
    ax[0].set_xlabel(r"$\theta$")
    ax[0].set_ylabel("coupling (J)")
    ax[0].set_title(r"Part A: $p_\gamma\cdot\omega_D = K^2 S_z$")
    ax[0].legend(); ax[0].grid(alpha=0.3)

    ax[1].plot(theta_list, sz_ratio)
    ax[1].set_xlabel(r"$\theta$")
    ax[1].set_ylabel(r"$S_z/\hbar$")
    ax[1].set_title(r"Part C2: continuous spin projection $0..1$")
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("darboux_coupling.svg", format="svg")
    print("[Part A/C2] saved darboux_coupling.svg")


# ==================================================================
# Frenet–Darboux 螺旋世界线求解器（§16 复用）
# ==================================================================
class FrenetDarbouxSolver:
    """常 κ,τ 螺旋世界线的 Frenet–Darboux 几何。

    【弧长参数化（与 §16 重校一致）】
        Ω = √(κ²+τ²),  R = κ/Ω²,  P = τ/Ω²
        r(s) = (R cos(Ωs), R sin(Ωs), P Ω s),    |dr/ds| = 1
    注：§16 用户草稿 r(s)=κ/(κ²+τ²)(cos Ωs, sin Ωs, τ s) 第三分量少 √(κ²+τ²)
    因子（仅当 τ=0 才等）；此处用单位速率正确形式，耦合结果只依赖 ω_D 模长
    Ω，故不影响 §16.4 的耦合解析值。

    Darboux 矢量：ω_D = τ t + κ b = Ω ẑ  （恒定，与 frenet_frame_lightspeed 的
    ω_D = K ẑ 同一约定，K=Ω, θ=atan2(τ,κ)）。

    eval(s) -> (r, t, n, b, ω_D, dω_D/ds)。
    """

    def __init__(self, kappa, tau):
        self.kappa = float(kappa)
        self.tau = float(tau)
        self.Omega = math.sqrt(self.kappa ** 2 + self.tau ** 2)
        self.R = self.kappa / (self.Omega ** 2)   # 螺旋半径
        self.P = self.tau / (self.Omega ** 2)

    def eval(self, s):
        Om = self.Omega
        phi = Om * s
        cphi = math.cos(phi)
        sphi = math.sin(phi)
        r = np.array([self.R * cphi, self.R * sphi, self.P * Om * s])
        t = np.array([-self.R * Om * sphi, self.R * Om * cphi, self.P * Om])
        # |t|² = R²Om² + P²Om² = (R²+P²)Om² = Om²/Om² = 1  ✓
        n = np.array([-cphi, -sphi, 0.0])
        b = np.cross(t, n)
        omegaD = self.tau * t + self.kappa * b
        domegaD = np.zeros(3)
        return r, t, n, b, omegaD, domegaD


# ==================================================================
# 主入口
# ==================================================================
def main():
    demo_part_a()
    plot_momentum_evolution()
    plot_darboux_coupling()
    print("\n=== §13 复现完成 ===")


if __name__ == "__main__":
    main()
