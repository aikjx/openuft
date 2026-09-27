# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  电子拟合 χ²/SLSQP —— 修正版（可运行）+ 可归一化性诊断
================================================================================

源稿（算法联盟最高权限｜TUFT V3.2 电子拟合 χ² 代价函数、解析梯度、SLSQP 精算
全链路）提出用径向稳态孤子 ansatz 拟合电子 (M_e, Q_e, μ_e)：

    -ψ_s'' - (2/r)ψ_s' = V1 ψ_s³ - V2 ψ_s⁵ ,   ψ_s'(0)=0,  ψ_s(∞)=0

本文件做三件事：
  1) 【代码修正】源稿代码含非法 Python 标识符（用 LaTeX 花括号 \\(...\\) 包裹），
     修正为合法标识符（C_rad / C_rad_num 等），使代码可运行。
  2) 【工程实现】文档自述"先有限差分梯度 + SLSQP，后换伴随解析梯度"——
     这里给出 scipy solve_ivp 打靶 + SLSQP 数值梯度的工程实现（快速路径）。
     同时保留 mpmath 高精度参考（dps 可调），作为可复现对照。
  3) 【基础审计】验证一个前置问题：该零质量径向 ODE 是否存在可归一化孤子。
     结论（决定性）：不存在——ψ(r) 渐近到非零常数 √(V1/V2)，N 与 E0 随截断
     R 以 R³ 发散，打靶边界 ψ(rmax)=0 无根。故 χ²/SLSQP 拟合失其优化对象，
     属结构障碍，先于精度/梯度讨论。

红线声明：本文件只做数学/数值结构与可行性检验，不构成对 TUFT 物理真实性的
任何主张；不对电子 g 因子作物理解读判定。
================================================================================
"""
import time
import numpy as np

# ====================== 常数（电子实验值，CODATA）======================
Me  = 9.1093837015e-31     # kg
Qe  = 1.602176634e-19       # C
mue = -9.2847647043e-24     # J/T
c   = 299792458.0           # m/s
hbar = 1.054571817e-34      # J·s

wM, wQ, wmu = 1.0, 1.0, 1.0
RMAX = 40.0                 # 源稿 r_max（注意：见诊断，此截断掩盖发散）

# ======================================================================
# 一、scipy 工程实现（快路径，本文件实际运行入口）
# ======================================================================
def _rhs_factory(V1, V2, r0):
    def rhs(t, y):
        psi, dpsi = y
        if t < r0:
            return [dpsi, 0.0]
        ddpsi = -(2.0 / t) * dpsi + V1 * psi ** 3 - V2 * psi ** 5
        return [dpsi, ddpsi]
    return rhs


def solve_psi(V1, V2, psi0, RMAX=RMAX, r0=1e-9):
    """打靶求解径向孤子轮廓，返回 solve_ivp 解对象。"""
    from scipy.integrate import solve_ivp
    sol = solve_ivp(_rhs_factory(V1, V2, r0), (r0, RMAX), [psi0, 0.0],
                    method='RK45', rtol=1e-12, atol=1e-14,
                    dense_output=True, max_step=0.05)
    return sol


def shoot_residual(V1, V2, psi0, RMAX=RMAX):
    return solve_psi(V1, V2, psi0, RMAX).y[0, -1]


def shoot_psi0(V1, V2, guess=0.75, RMAX=RMAX):
    """求使 psi(RMAX)=0 的 psi0——诊断将显示该根不存在（无正常化孤子）。"""
    from scipy.optimize import brentq

    def f(x):
        return shoot_residual(V1, V2, x, RMAX)

    x1, x2 = guess * 0.5, guess * 2.0
    for _ in range(8):
        try:
            return brentq(f, x1, x2)
        except ValueError:
            x1 *= 0.5
            x2 *= 2.0
    raise RuntimeError(
        f"shoot fail V1={V1} V2={V2}: 在 psi0∈[{x1},{x2}] 内 psi(RMAX) 不变号"
        "——无正常化孤子（见诊断），ψ(r) 渐近到非零常数 √(V1/V2)")


def compute_observables(V1, V2, q0, omega0, RMAX=RMAX, n=400001):
    """返回 (M, Q0, mu, C_rad, N, E0, I_mu, psi0)。
    C_rad = (1/N)·∫4πr⁴·ψ²·(3V1ψ²−5V2ψ⁴) dr （辐射修正系数，源稿记 C）。"""
    psi0 = shoot_psi0(V1, V2, RMAX=RMAX)
    sol = solve_psi(V1, V2, psi0, RMAX)

    r = np.linspace(1e-12, RMAX, n)
    psi = sol.sol(r)[0]
    dpsi = sol.sol(r)[1]
    N  = np.trapezoid(4 * np.pi * r**2 * psi**2, r)
    E0 = np.trapezoid(4 * np.pi * r**2 * (0.5 * dpsi**2
                       + (V1 / 4) * psi**4 - (V2 / 6) * psi**6), r)
    I_mu = np.trapezoid(2 * np.pi * r**3 * psi**2, r)
    C_num = np.trapezoid(4 * np.pi * r**2 * psi**2
                         * (3 * V1 * psi**2 - 5 * V2 * psi**4) * r**2, r)

    M  = E0 / c**2
    Q0 = q0 * omega0 * N
    mu = q0 * omega0 * I_mu
    C_rad = C_num / N
    return M, Q0, mu, C_rad, N, E0, I_mu, psi0


def chi2_lambda(x, RMAX=RMAX):
    V1, V2, q0, omega0 = x
    try:
        M, Q0, mu, C_rad, N, E0, I_mu, psi0 = compute_observables(V1, V2, q0, omega0, RMAX)
    except Exception:
        return 1e12
    resM  = (M - Me) / Me
    resQ  = (Q0 - Qe) / Qe
    resmu = (mu - mue) / mue
    return float(wM * resM**2 + wQ * resQ**2 + wmu * resmu**2)


def grad_fd(x, eps=1e-5):
    g = np.zeros(4)
    for i in range(4):
        xp = x.copy(); xp[i] += eps
        xm = x.copy(); xm[i] -= eps
        g[i] = (chi2_lambda(xp) - chi2_lambda(xm)) / (2 * eps)
    return g


# ======================================================================
# 二、可归一化性诊断（决定性的前置审计）
# ======================================================================
def diagnostic():
    out = []
    out.append("TUFT V3.2 电子拟合 —— 可归一化性 / 可行性 诊断")
    out.append("(零质量径向 ODE: -psi''-(2/r)psi' = V1 psi^3 - V2 psi^5)")
    out.append("=" * 64)

    out.append("\n[A] 渐近平台与 psi0 无关性（V1=1.2,V2=0.4, sqrt(V1/V2)=%.4f）"
               % np.sqrt(1.2 / 0.4))
    for psi0 in (0.05, 0.3, 0.75, 1.2, 2.5):
        sol = solve_psi(1.2, 0.4, psi0, RMAX=150.0)
        out.append("    psi0=%5.2f  ->  psi(150)=%+.6f" % (psi0, sol.sol(150.0)[0]))

    out.append("\n[B] 平台值 = sqrt(V1/V2) 普适性")
    for (V1, V2) in [(1.2, 0.4), (3.0, 0.3), (2.0, 2.0), (0.5, 0.1)]:
        sol = solve_psi(V1, V2, 0.75, RMAX=150.0)
        out.append("    V1=%.1f,V2=%.1f  sqrt(V1/V2)=%.4f  psi(150)=%.4f"
                   % (V1, V2, np.sqrt(V1 / V2), sol.sol(150.0)[0]))

    out.append("\n[C] N,E0 随截断 R 发散（R^3）=> 不可归一化")
    for R in (20.0, 50.0, 100.0, 200.0, 400.0):
        sol = solve_psi(1.2, 0.4, 0.75, RMAX=R)
        rr = np.linspace(1e-9, R, 200001)
        N  = np.trapezoid(4 * np.pi * rr**2 * sol.sol(rr)[0]**2, rr)
        E0 = np.trapezoid(4 * np.pi * rr**2 * (0.5 * sol.sol(rr)[1]**2
                           + 0.3 * sol.sol(rr)[0]**4 - (0.4/6) * sol.sol(rr)[0]**6), rr)
        out.append("    R=%6.1f  N(R)=%12.4e  E0(R)=%12.4e  psi(R)=%+.4f"
                   % (R, N, E0, sol.sol(R)[0]))

    out.append("\n[D] 打靶边界 psi(RMAX)=0 无根（shoot_psi0 抛 RuntimeError）")
    try:
        shoot_psi0(1.2, 0.4)
        out.append("    [意外] 找到根")
    except RuntimeError as e:
        out.append("    [确认] %s" % e)

    out.append("\n[E] 符号结构：mu = q0*omega0*I_mu > 0 vs 目标 mu_e < 0")
    out.append("    q0,omega0>0 界内 mu 恒 > 0；mu_e=-9.284e-24 < 0")
    out.append("    => 第 3 通道 (mu-mu_e)^2 结构上不可满足（mu 只能 -> 0+，resmu~-1）")

    out.append("\n[F] g 因子形状无关性：g_TUFT = 2*M*mu/(Q0*S) = 4*M*I_mu/(N*hbar)")
    out.append("    q0, omega0 在 g 因子中相消，g 仅依赖剖面 (V1,V2)")

    out.append("\n[G] 可行性：mpmath dps=250 下 odefun 单次打靶求解 >4 分钟未完成")
    out.append("    => SLSQP 内嵌套数百次高精度 ODE 求值，该数值路径不可行")
    return out


# ======================================================================
# 三、mpmath 高精度参考（源稿修正标识符版；仅供文档/复现，直接运行过慢）
# ======================================================================
def mpmath_reference(dps=250, V1="1.2", V2="0.4", q0="1.0", omega0="0.2", RMAX="40"):
    """源稿 mpmath 框架的修正版：仅修非法标识符，结构原样。dps 过大时极慢，
    仅供对照源稿；实际拟合建议用上方 scipy 快路径。"""
    import mpmath as mp
    mp.mp.dps = dps
    V1, V2 = mp.mpf(V1), mp.mpf(V2)
    q0, omega0 = mp.mpf(q0), mp.mpf(omega0)
    r_max = mp.mpf(RMAX)

    def tuft_ode(r, state):
        psi, dpsi = state
        if r < mp.mpf("1e-30"):
            return [mp.mpf(0), mp.mpf(0)]
        ddpsi = -(2 / r) * dpsi + V1 * psi**3 - V2 * psi**5
        return [dpsi, ddpsi]

    def solve_soliton(psi0_guess):
        def shoot(psi0):
            sol = mp.odefun(tuft_ode, 0, [psi0, mp.mpf(0)], r_max)
            return sol(r_max)[0]
        psi0_root = mp.findroot(shoot, psi0_guess)
        return mp.odefun(tuft_ode, 0, [psi0_root, mp.mpf(0)], r_max)

    sol_sol = solve_soliton(mp.mpf("0.75"))
    N = mp.quad(lambda r: 4 * mp.pi * r**2 * sol_sol(r)[0]**2, [0, r_max])
    E0 = mp.quad(lambda r: 4 * mp.pi * r**2 * (mp.mpf("0.5") * sol_sol(r)[1]**2
                 + V1 / 4 * sol_sol(r)[0]**4 - V2 / 6 * sol_sol(r)[0]**6), [0, r_max])
    I_mu = mp.quad(lambda r: 2 * mp.pi * r**3 * sol_sol(r)[0]**2, [0, r_max])
    C_num = mp.quad(lambda r: 4 * mp.pi * r**2 * sol_sol(r)[0]**2
                    * (3 * V1 * sol_sol(r)[0]**2 - 5 * V2 * sol_sol(r)[0]**4) * r**2,
                    [0, r_max])
    return {
        "M": E0 / mp.mpf("299792458")**2, "Q0": q0 * omega0 * N,
        "mu": q0 * omega0 * I_mu, "C_rad": C_num / N,
        "N": N, "E0": E0, "I_mu": I_mu,
    }


# ======================================================================
# 四、入口：诊断 + （可选）SLSQP 优化
# ======================================================================
if __name__ == "__main__":
    t0 = time.time()
    lines = diagnostic()
    for ln in lines:
        print(ln)

    # 尝试 SLSQP（预期：因无正常化孤子，打靶失败 -> chi2 全部返回 1e12，
    # 优化无法起步）。保留以如实呈现"该路径不可行"。
    print("\n==== 尝试启动 SLSQP 参数优化 ====")
    from scipy.optimize import minimize
    x0 = np.array([1.2, 0.4, 1.0, 0.2])
    bounds = [(1e-4, None), (1e-4, None), (1e-4, None), (1e-4, None)]
    print("初始点单次 chi2 =", chi2_lambda(x0))
    res = minimize(chi2_lambda, x0, method="SLSQP", jac=grad_fd, bounds=bounds,
                   options={"maxiter": 30, "disp": False, "ftol": 1e-10})
    print("收敛标志:", res.success, res.message)
    print("最优参数:", res.x)
    print("最优 chi2:", res.fun)
    print("\n运行总耗时 %.2f s" % (time.time() - t0))
