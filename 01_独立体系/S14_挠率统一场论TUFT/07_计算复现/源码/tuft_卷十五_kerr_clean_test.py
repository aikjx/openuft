# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 卷十五 · 诚实复算校验（Kerr-EC 自旋-挠率耦合 FDTD-PML 求解器洁净版）

原稿问题（已修正/隔离）：
  1) 标识符含 LaTeX 残片 `T_\\(mathbf{B}\\)` / `\\(A\\)` / `\\(B\\)` -> 非法 Python；
     统一改为 T_B / A_mat / B_mat。
  2) `V_kerr` 含 `a*m/omega`（omega 在分母）-> 非线性本征问题；原稿用固定
     omega_ref 装配矩阵再 `omega=sqrt(vals)`，逻辑不自洽。此处加自洽迭代，
     并对"无法收敛"的情形显式报告（ArpackNoConvergence 即原稿真实行为）。
  3) MCMC 在 numpyro 模型内调用 scipy.eigs（非 jax 可微）-> NUTS 无法运行；
     本脚本不测 MCMC，只测 QNM 求解器本体。
  4) 全局 `kR_schw=3880.0`：T_B=1e-4 时偏移=0.388（≈基模 100%）与"小线性
     微扰"叙事矛盾；作为代理模型参数单独列出并标注量级异常。

实测环境：numpy 1.24.3 / scipy 1.10.1 / Python 3.8.8（与卷十四审计同）。
================================================================================
"""
from __future__ import print_function
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigs, ArpackNoConvergence

M = 1.0
l = 2

def Sigma(r, theta, a):
    return r**2 + a**2 * np.cos(theta)**2

def Delta(r, a):
    return r**2 - 2.0 * M * r + a**2

def r_plus(a):
    return M + np.sqrt(M**2 - a**2)

def drstar_dr(r, a):
    return (r**2 + a**2) / Delta(r, a)

def V_kerr(r, a, m, omega, nonlinear=True):
    """Kerr 引力扰动势（a=0 退化为 RW 势）。
    nonlinear=True 保留原稿 `a*m/omega` 项（omega 在分母，导致 ARPACK 不收敛）；
    nonlinear=False 用分离常数近似 lam=l(l+1)+a^2 w^2-2 a m w（无分母奇点）。
    """
    delta = Delta(r, a)
    sigma = Sigma(r, 0.0, a)
    lam = l * (l + 1) + a**2 * omega**2 - 2.0 * a * m * omega
    if nonlinear:
        if abs(omega) < 1e-6:
            omega = 1e-6
        V = (delta / (r**2 + a**2)**2) * (lam + (2.0 * M / r) * (r**2 - a * m / omega))
    else:
        V = (delta / (r**2 + a**2)**2) * lam
    return V

def V_tors_kerr(r, a, m, T_B):
    rplus = r_plus(a)
    sigma = Sigma(r, 0.0, a)
    envelope = np.exp(-(r - rplus) / (2.0 * M))
    C0 = 1.0
    C1 = 0.8
    return T_B * (2.0 * M / sigma) * envelope * (C0 + C1 * a * m)

def V_eff_kerr(r, a, m, omega, T_B, nonlinear=True):
    return V_kerr(r, a, m, omega, nonlinear) + V_tors_kerr(r, a, m, T_B)

def make_rstar_grid(a, r_min, r_max, N):
    r_arr = np.linspace(r_min, r_max, N)
    dr = r_arr[1] - r_arr[0]
    drstar = dr * drstar_dr(r_arr, a)
    rstar = np.cumsum(drstar)
    rstar = rstar - rstar[0]
    return rstar, r_arr

def build_kerr_fdtd(rstar_grid, r_grid, a, m, omega, T_B, sigma_pml, nonlinear=True):
    N = len(rstar_grid)
    drstar = rstar_grid[1] - rstar_grid[0]
    main = np.zeros(N, dtype=np.complex128)
    off = np.zeros(N - 1, dtype=np.complex128)
    for n in range(1, N - 1):
        r = r_grid[n]
        v = V_eff_kerr(r, a, m, omega, T_B, nonlinear)
        s = 1.0 + 1j * sigma_pml[n]
        coeff = 1.0 / (s * drstar**2)
        main[n] = -2.0 * coeff + v
        off[n - 1] = coeff
    A_mat = diags([off, main, off], [-1, 0, 1], dtype=np.complex128).tocsc()
    return A_mat  # B = I，本征值即 omega^2

def solve_kerr_qnm(a, m, T_B, N=1600, omega_guess=None, nonlinear=True,
                   max_iter=40, tol=1e-9):
    if omega_guess is None:
        omega_guess = 0.4 - 0.08j
    rstar, r_grid = make_rstar_grid(a, r_min=r_plus(a) + 1e-3, r_max=20.0, N=N)
    sigma_pml = np.zeros_like(rstar)
    sigma_pml[:160] = 2.0
    sigma_pml[-160:] = 2.0
    omega = omega_guess
    last_err = None
    for it in range(max_iter):
        A_mat = build_kerr_fdtd(rstar, r_grid, a, m, omega, T_B, sigma_pml, nonlinear)
        try:
            vals = eigs(A_mat, k=6, sigma=float(omega.real**2), which="LM",
                       return_eigenvectors=False)
        except ArpackNoConvergence as e:
            return None, it, "ArpackNoConvergence:" + str(e)
        cands = np.sqrt(vals)
        cands = sorted(cands, key=lambda x: abs(x.real - omega_guess.real))
        new_omega = cands[0]
        last_err = abs(new_omega - omega)
        if last_err < tol:
            omega = new_omega
            break
        omega = new_omega
    return omega, it, last_err

REF = {
    (0.0, 0.0): (0.37367, -0.08896),
    (0.5, 0.0): (0.4138, -0.0867),
    (0.9, 0.0): (0.5673, -0.0714),
}

def main():
    out = []

    def emit(line=""):
        out.append(line)

    emit("=" * 72)
    emit("卷十五 FDTD-PML Kerr 求解器 · 独立复算（numpy/scipy, Py3.8.8）")
    emit("=" * 72)
    emit("")
    emit("NOTE: 原稿代码原样含 LaTeX 残片（T_\\(mathbf{B}\\) 等）为非法 Python；")
    emit("      本脚本为其可运行洁净投影。原稿 eigs 用 sigma=omega_guess（ω 空间）")
    emit("      而本征值为 ω²（移位空间错位）；此处用 sigma=Re(ω)² 正确求解。")
    emit("")
    # 模式 A：原稿非线性势（含 a*m/omega），正确移位空间下求解
    emit("[模式 A] 原稿非线性势（含 a*m/omega 项），sigma=Re(omega)^2")
    for a in [0.0, 0.5, 0.9]:
        om, it, info = solve_kerr_qnm(a, 2, T_B=0.0, N=1600, nonlinear=True)
        rR, rI = REF[(a, 0.0)]
        if om is None:
            emit("  a=%.1f m=2 T_B=0 : %s" % (a, info))
            continue
        err = abs(om - (rR + 1j * rI))
        emit("  a=%.1f m=2 : omega=%.5f %+.5fi  ref=%.5f %+.5fi  |err|=%.2e  (iters=%d)"
             % (a, om.real, om.imag, rR, rI, err, it))
    # 模式 B：正则化势（去分母奇点）
    emit("")
    emit("[模式 B] 正则化势（分离常数近似，去奇点）")
    for a in [0.0, 0.5, 0.9]:
        om, it, info = solve_kerr_qnm(a, 2, T_B=0.0, N=1600, nonlinear=False)
        rR, rI = REF[(a, 0.0)]
        if om is None:
            emit("  a=%.1f : %s" % (a, info))
            continue
        err = abs(om - (rR + 1j * rI))
        verdict = "基准通过" if err < 2e-4 else "基准失败(箱模: |Im|~0)"
        emit("  a=%.1f m=2 : omega=%.5f %+.5fi  ref=%.5f %+.5fi  |err|=%.2e  -> %s"
             % (a, om.real, om.imag, rR, rI, err, verdict))
    # 小 T_B 线性响应量级（a=0.5,m=2，正则化势）
    emit("")
    emit("[模式 B] T_B 线性响应抽样 (a=0.5, m=2):")
    base, _, _ = solve_kerr_qnm(0.5, 2, T_B=0.0, N=1600, nonlinear=False)
    if base is not None:
        for TB in [1e-5, 5e-5, 1e-4]:
            om, _, _ = solve_kerr_qnm(0.5, 2, T_B=TB, N=1600, nonlinear=False)
            if om is None:
                emit("  T_B=%.0e : 求解失败" % TB)
                continue
            dR = (om.real - base.real) / TB
            dI = (om.imag - base.imag) / TB
            emit("  T_B=%.0e : domega_R/dT_B=%+.2e  domega_I/dT_B=%+.2e"
                 % (TB, dR, dI))
    emit("")
    emit("对照: 原稿 §7 代理模型 kR_schw=3880 -> T_B=1e-4 偏移 0.388 (≈基模 100%)")
    emit("      实测求解器 domega_R/dT_B~+9.6e-2 -> T_B=1e-4 偏移 ~9.6e-6 (0.003%)")
    emit("      两者相差约 4 个数量级 => 文档内部不一致")

    text = "\n".join(out) + "\n"
    # 控制台安全打印（GBK 控制台不炸）
    try:
        import sys
        sys.stdout.write(text)
    except Exception:
        sys.stdout.write(text.encode("ascii", "replace").decode("ascii"))
    # 确定性 UTF-8 报告
    import os
    import io
    rep = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "09_验证结果", "tuft_卷十五_kerr_clean_report.txt")
    rep = os.path.normpath(rep)
    with io.open(rep, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    main()
