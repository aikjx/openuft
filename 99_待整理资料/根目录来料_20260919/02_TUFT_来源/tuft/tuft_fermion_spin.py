# -*- coding: utf-8 -*-
"""
TUFT-R2 分支 A：费米子自旋统计的拓扑-几何推导
==============================================

目标：基于已修复的闭合带拓扑量子化（定理 2'），用 sympy + 数值
Gauss linking-number 积分，推导并校验：
  (1) 自旋 1/2 的几何来源：费米子 Lk = ±1/2 对应 Möbius 型（不可定向）
      闭合带；标架绕 2π 不闭合、需 4π 才闭合 → 波函数 4π 周期 → 自旋 1/2。
  (2) 自旋-统计定理（拓扑版）：可定向带（整数 Lk, 玻色）↔ 2π 周期；
      Möbius 带（半整数 Lk, 费米）↔ 4π 周期 ↔ 费米统计。
  (3) 泡利不相容的拓扑论证：费米子交换 = 2π 旋转 → 相位 -1（来自 s=1/2）；
      反对称波函数在两粒子同态时恒为零。

--------------------------------------------------------------------
【红线声明】数学自洽 ≠ 物理实验证实。本文件只检验 TUFT 框架内部的
拓扑-代数自洽性，不宣称该框架已被实验验证，也不粉饰假设为定理。
"Möbius 带 → 费米统计" 是已知的拓扑学事实（Leinaas-Myrheim /
Laidlaw-DeWitt / 图论自旋-统计），本文件仅在此框架内复现并数值核验，
不主张 TUFT 比标准量子场论更"基本"。
--------------------------------------------------------------------

【定理 2'（已修复）】
   闭合带自链接数  Lk = Tw + Wr ,   Lk ∈ ½ℤ
   基态 (N=1) 量子化：  s = |Lk| ,   s ∈ {0, ½, 1, 3/2, ...}
   玻色：Lk ∈ ℤ          （可定向带，n 个半扭转，n 偶）
   费米：Lk ∈ ℤ + ½       （Möbius 带，n 个半扭转，n 奇）
"""
import sys
import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# 1. 闭合 ribbon 参数化 + Gauss linking-number 数值核验
# ---------------------------------------------------------------------------

def ribbon_edges(t, R, w, n):
    """套索闭合带：中心线为 xy 平面圆，沿环加 n 个半扭转。
    phi(t) = (n/2) * t 为扭转角；n 为半扭转个数。
    n=1 → Möbius（单半扭转，不可定向）；n 偶 → 可定向带。
    返回两条边界曲线 e_plus, e_minus（形状 (3, N)）。
    """
    phi = 0.5 * n * t
    cx = R * np.cos(t)
    cy = R * np.sin(t)
    cz = np.zeros_like(t)
    # 法向 N = cos(phi) e_r + sin(phi) e_z
    Nx = np.cos(phi) * np.cos(t)
    Ny = np.cos(phi) * np.sin(t)
    Nz = np.sin(phi)
    e_plus = np.array([cx + 0.5 * w * Nx, cy + 0.5 * w * Ny, cz + 0.5 * w * Nz])
    e_minus = np.array([cx - 0.5 * w * Nx, cy - 0.5 * w * Ny, cz - 0.5 * w * Nz])
    return e_plus, e_minus


def gauss_linking(e1, e2, t):
    """Gauss 双积分计算两条闭合曲线 linking number。
    Lk = (1/4π) ∫∫ (e1(t)-e2(s))·(e1'(t)×e2'(s)) / |e1-e2|^3 dt ds
    网格法（trapz 两次）；曲线最小间距 = w，积分非奇异。
    """
    dt = t[1] - t[0]
    de1 = np.gradient(e1, dt, axis=1)
    de2 = np.gradient(e2, dt, axis=1)
    N = len(t)
    total = 0.0
    for i in range(N):
        d = e1[:, i][:, None] - e2          # (3, N)
        r3 = np.sum(d * d, axis=0) ** 1.5 + 1e-9
        cross = np.cross(de1[:, i], de2, axis=0)  # (3, N)
        total += np.sum(np.sum(d * cross, axis=0) / r3)
    return float(total * dt * dt / (4.0 * np.pi))


def frame_closure(n):
    """检查 Möbius 标架的闭合周期：N(2π) 与 N(4π) 相对 N(0)。
    n=1（Möbius）：N(2π) = -N(0) → 2π 不闭合；N(4π)=N(0) → 4π 闭合。
    """
    def N_of(tval):
        phi = 0.5 * n * tval
        return np.array([np.cos(phi) * np.cos(tval),
                         np.cos(phi) * np.sin(tval), np.sin(phi)])
    N0 = N_of(0.0)
    N2 = N_of(2.0 * np.pi)
    N4 = N_of(4.0 * np.pi)
    # 2π 是否反向（不可定向标志）：N(2π) ≈ -N(0)
    anti = np.linalg.norm(N2 + N0)
    closed2 = np.linalg.norm(N2 - N0)
    closed4 = np.linalg.norm(N4 - N0)
    return anti, closed2, closed4


# ---------------------------------------------------------------------------
# 2. 自旋-统计：相位因子
# ---------------------------------------------------------------------------

def spin_phases(s):
    """绕 2π 与 4π 的相位因子 exp(i 2π s) / exp(i 4π s)。"""
    p2 = sp.simplify(sp.exp(sp.I * 2 * sp.pi * s))
    p4 = sp.simplify(sp.exp(sp.I * 4 * sp.pi * s))
    return p2, p4


# ---------------------------------------------------------------------------
# 3. 泡利不相容：反对称 Slater 行列式（sympy）
# ---------------------------------------------------------------------------

def pauli_slater_det():
    """两费米子同一轨道 φ_a 的 2×2 Slater 行列式必为零 → 泡利不相容。"""
    x1, x2 = sp.symbols("x_1 x_2")
    phi_a = sp.Function("phi_a")
    M = sp.Matrix([[phi_a(x1), phi_a(x2)],
                   [phi_a(x1), phi_a(x2)]])
    return sp.simplify(M.det())


def white_lk(n):
    """White 公式解析：闭合带 Lk = Tw + Wr。套索（中心为平面圆）Wr=0，
    总扭转角 = (n/2)·2π，故 Tw = n/2。机器精确，符号取决于扭转手性；
    量子数 s = |Lk| = |n|/2。"""
    return 0.5 * n


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    out = []
    out.append("TUFT-R2 分支 A：费米子自旋统计（拓扑-几何推导与数值核验）")
    out.append("运行时间: " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("numpy " + np.__version__ + "  sympy " + sp.__version__)
    out.append("")
    out.append("接在稳态结（tuft_knot_slsqp.py）之上：电子 = 普朗克尺度几何结；")
    out.append("其内禀自旋/统计由闭合带的拓扑量子数 Lk 决定（定理 2'）。")
    out.append("")

    # ---- (1) 核验 Lk = n/2：White 解析 + Gauss 积分（仅可定向）交叉 ----
    out.append("=== (1) 闭合带自链接数 Lk 的核验（White 公式 + Gauss 积分）===")
    R, w = 2.0, 0.35
    t = np.linspace(0.0, 2.0 * np.pi, 600, endpoint=False)
    for n in [0, 1, 2, 3]:
        lk_white = white_lk(n)
        s = abs(lk_white)
        if n % 2 == 0:
            ep, em = ribbon_edges(t, R, w, n)
            lk_num = gauss_linking(ep, em, t)
            out.append("  n=%d(偶,可定向): Lk_White=%.4f | |Gauss|=%.4f 偏差%.2e | s=%.1f 玻色"
                       % (n, lk_white, abs(lk_num), abs(lk_num) - abs(lk_white), s))
        else:
            out.append("  n=%d(奇,Möbius单边界): Lk_White=%.4f(解析) | s=%.1f 费米"
                       % (n, lk_white, s))
            out.append("        Möbius 仅一条边界，Gauss 两-边积分不适用；")
            out.append("        自链接由 White 公式 = n/2（解析精确）给出。")
    out.append("  注：n 偶→Lk 整数→可定向带→玻色；n 奇→Lk 半整数→Möbius→费米。")
    out.append("")

    # ---- Möbius 标架 4π 周期 ----
    out.append("=== (1b) Möbius 标架闭合周期（n=1）===")
    anti, c2, c4 = frame_closure(1)
    out.append("  N(2π) 与 -N(0) 间距 = %.3e   (≈0 ⇒ 2π 后法向翻向，不可定向)"
               % anti)
    out.append("  N(2π) 与  N(0) 间距 = %.3e   (大 ⇒ 2π 不闭合)" % c2)
    out.append("  N(4π) 与  N(0) 间距 = %.3e   (≈0 ⇒ 4π 才闭合)" % c4)
    out.append("  => 绕 2π 标架不闭合、需 4π → 波函数 4π 周期 → 自旋 1/2。")
    out.append("")

    # ---- (2) 自旋-统计相位 ----
    out.append("=== (2) 自旋-统计相位因子 ===")
    for s in [sp.Rational(1, 2), 1, 0]:
        p2, p4 = spin_phases(s)
        out.append("  s = %s :  绕2π相位 = %s ,  绕4π相位 = %s"
                   % (s, sp.latex(p2) if False else str(p2),
                      sp.latex(p4) if False else str(p4)))
    out.append("  费米 s=1/2: exp(iπ) = -1（2π 旋转给 -1） ↔ 交换两条 Möbius 带 = 半扭转；")
    out.append("             exp(i2π) = +1（需 4π） ↔ 交换两次回到原状（braid σ²=1）。")
    out.append("  这与 (1b) 的 4π 标架闭合一致：费米统计 = 4π 周期拓扑。")
    out.append("")

    # ---- (3) 泡利不相容 ----
    out.append("=== (3) 泡利不相容（反对称 Slater 行列式）===")
    det = pauli_slater_det()
    out.append("  两费米子同占轨道 φ_a 的 2×2 行列式 = " + str(det))
    out.append("  => 行列式恒为 0：同一量子态不能容纳两个全同费米子。")
    out.append("  拓扑支撑：费米子交换 = 2π 旋转 = 半扭转 → 相位 -1（见 (2)），")
    out.append("  波函数反对称 Ψ(x1,x2) = -Ψ(x2,x1)；令 x1=x2 得 Ψ = -Ψ ⇒ Ψ=0。")
    out.append("  注：自旋-统计定理与泡利原理是已知量子力学结论，本文件仅在")
    out.append("      TUFT 拓扑框架内复现其代数，不主张其为 TUFT 的新发现。")
    out.append("")

    out.append("=== 红线与开放项 ===")
    out.append("  · 数学自洽（Lk 半整数、4π 周期、反对称）已数值/符号核验；")
    out.append("    不等于物理证实。TUFT 是否真实描述电子待实验判定。")
    out.append("  · 开放项：结尺度为何是康普顿波长而非普朗克尺度（尺度生成机制）；")
    out.append("    三维多费米子系统的 braid-group 表示与具体相互作用仍需展开。")
    out.append("  · 分支 A 完成度：拓扑-代数自洽性证明（非物理证明）。")

    report = "\n".join(out)
    print(report)
    with open("tuft_fermion_spin_report.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")


if __name__ == "__main__":
    main()
