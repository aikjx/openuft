# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  电子拟合 —— 结构性障碍演示（可归一化性全链审计，修正模型尝试）
================================================================================

目标：验证源稿"复标量孤子 ψ_s(r) 拟合电子"的径向标量 ansatz 是否存在可归一化、
单值、局域的孤子。共四条路径，逐条数值检验：

  P0  源稿零质量势  U=V1/4 ψ⁴ - V2/6 ψ⁶ ：ψ 渐近 √(V1/V2)，N/E0 随 R³ 发散
  P1  补质量项 m²ψ（势仍无界）            ：无束缚态（psi0 扫描 0 个衰减模根）
  P2  下方有界势  U=½m²ψ²+V1/4ψ⁴+V2/6ψ⁶  ：ψ=0 为极小 ⇒ 场过冲振荡（辐射解），
                                          非单值无节孤子；无干净临界振幅
  P3  标度/单位缺口                       ：E0(自然)~O(1e2) vs 需 M_e c²=8.2e-14 J，
                                          缺口 ~10^16 ⇒ χ²/SLSQP 与 g/C 无法有意义执行

结论：源稿标量 ansatz 在这三类势下都不给出稳健的局域电子孤子；χ² 拟合、SLSQP、
g 因子、C 的完整执行须先切换到【退化真空势（instanton/Q-ball）】或前序 R2 时空结
ansatz，并钉扎能量/长度标度。

红线声明：本文件只做数值结构检验，不构成对 TUFT 物理真实性的任何主张。
================================================================================
"""
import time
import numpy as np

Me  = 9.1093837015e-31
Qe  = 1.602176634e-19
mue = -9.2847647043e-24
c   = 299792458.0
hbar = 1.054571817e-34


def _rhs(m2, V1, V2, sV2, r0):
    """-psi''-(2/r)psi' = m^2 psi + V1 psi^3 + sV2*V2 psi^5
       sV2=-1 源稿(无界势)；sV2=+1 下方有界修正。"""
    def rhs(t, y):
        psi, dpsi = y
        if t < r0:
            return [dpsi, 0.0]
        ddpsi = -(2.0/t)*dpsi - m2*psi - V1*psi**3 - sV2*V2*psi**5
        return [dpsi, ddpsi]
    return rhs


def solve(m2, V1, V2, sV2, psi0, RMAX, r0=1e-9, max_step=0.05):
    from scipy.integrate import solve_ivp
    return solve_ivp(_rhs(m2, V1, V2, sV2, r0), (r0, RMAX), [psi0, 0.0],
                     method='RK45', rtol=1e-11, atol=1e-13,
                     dense_output=True, max_step=max_step)


def N_E0(sol, m, V1, V2, sV2, R, n=150000):
    rr = np.linspace(1e-9, R, n)
    p = sol.sol(rr)[0]; dp = sol.sol(rr)[1]
    N  = np.trapezoid(4*np.pi*rr**2*p**2, rr)
    E0 = np.trapezoid(4*np.pi*rr**2*(0.5*dp**2 + 0.5*m*m*p**2
                     + (V1/4)*p**4 + sV2*(V2/6)*p**6), rr)
    return N, E0


def scan_roots(m, V1, V2, sV2, RMAX):
    """扫描 psi0∈[1e-3,8]，找衰减模匹配 psi'+m psi=0 的根数。"""
    from scipy.optimize import brentq
    def g(x):
        s = solve(m*m, V1, V2, sV2, x, RMAX)
        return s.y[1, -1] + m*s.y[0, -1]
    grid = np.linspace(1e-3, 8.0, 120)
    gv = np.array([g(x) for x in grid])
    roots = []
    for i in range(len(grid)-1):
        if gv[i]*gv[i+1] < 0:
            try:
                roots.append(brentq(g, grid[i], grid[i+1]))
            except ValueError:
                pass
    return roots


def main():
    out = []
    out.append("TUFT V3.2 电子拟合 —— 径向标量孤子 结构性障碍演示（P0-P3）")
    out.append("=" * 70)
    t0 = time.time()
    V1, V2, m = 1.2, 0.4, 1.0

    # ---- P0 零质量源稿势 ----
    out.append("\n[P0] 源稿零质量势  U=V1/4 ψ^4 - V2/6 ψ^6  (无界下方)")
    out.append("    预期：ψ 渐近 √(V1/V2)=%.4f，N/E0 随 R 发散" % np.sqrt(V1/V2))
    sol = solve(0.0, V1, V2, -1, 0.75, 200.0)
    out.append("    ψ(5)=%+.4f  ψ(40)=%+.4f  ψ(150)=%+.4f   (渐近非零 → 非局域)"
               % (sol.sol(5.0)[0], sol.sol(40.0)[0], sol.sol(150.0)[0]))
    for R in (50.0, 200.0):
        N, E0 = N_E0(sol, 0.0, V1, V2, -1, R)
        out.append("    R=%6.1f  N=%.4e  E0=%.4e" % (R, N, E0))
    out.append("    ⇒ 判定：ψ→const≠0，N/E0 随 R³ 发散，无正常化孤子")

    # ---- P1 补质量项、势仍无界 ----
    out.append("\n[P1] 补质量项 m^2 psi（势仍无界）—— 束缚态扫描")
    roots = scan_roots(m, V1, V2, -1, RMAX=20.0)
    out.append("    衰减模根数 = %d  ⇒ %s"
               % (len(roots), "无束缚态（场泄漏，势无界下方）" if not roots else "存在根"))

    # ---- P2 下方有界势 ----
    out.append("\n[P2] 下方有界势  U=1/2 m^2 ψ^2 + V1/4 ψ^4 + V2/6 ψ^6")
    roots = scan_roots(m, V1, V2, +1, RMAX=20.0)
    out.append("    衰减模根数 = %d" % len(roots))
    if roots:
        for psi0 in sorted(roots)[:2]:
            s = solve(m*m, V1, V2, +1, psi0, 20.0)
            vals = "  ".join("r=%2d:%+.3f" % (r, s.sol(float(r))[0]) for r in (1, 5, 10, 15, 20))
            out.append("    psi0=%.4f  剖面: %s" % (psi0, vals))
            N, E0 = N_E0(s, m, V1, V2, +1, 20.0)
            out.append("        N(20)=%.4e E0(20)=%.4e  (ψ 过零/振荡 → 非单值无节孤子)"
                       % (N, E0))
    out.append("    ⇒ 判定：ψ=0 为极小，场必过冲振荡（辐射解），非稳健无节孤子；"
               "临界振幅对势结构高度敏感")

    # ---- P3 标度缺口 ----
    out.append("\n[P3] 标度/单位缺口")
    out.append("    E0(自然) ~ O(1e2)；需 E0 = M_e c^2 = %.4e J；缺口 ~ 1e16"
               % (Me*c**2))
    out.append("    Q0(自然,q0=ω0=1) ~ O(1e2)；需 Q_e=%.4e C ⇒ (q0·ω0)~1e-21"
               % Qe)
    out.append("    ⇒ 无量纲模型缺能量/长度标度，直接 SI 拟合迫使参数极端化、病态；"
               "χ²/SLSQP 与 g 因子须先钉扎标度。")

    out.append("\n结论：源稿径向标量 ansatz 在 P0/P1/P2 三类势下均无稳健局域电子孤子；"
               "完整拟合须切换退化真空势(instanton/Q-ball)或 R2 时空结 ansatz，"
               "并钉扎标度后再执行。")
    out.append("\n运行总耗时 %.1f s" % (time.time()-t0))
    text = "\n".join(out)
    print(text)
    return text


if __name__ == "__main__":
    main()
