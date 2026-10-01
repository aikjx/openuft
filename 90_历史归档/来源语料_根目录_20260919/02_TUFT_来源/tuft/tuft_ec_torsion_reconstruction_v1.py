# -*- coding: utf-8 -*-
"""
tuft_ec_torsion_reconstruction_v1.py
====================================

【攻坚续篇审读】「EC 挠率基底重构：解决 α 普适性 / 牛顿极限冲突」的逐条核验

被审对象（原稿主张）：
  A1 时空是带挠率的 4 维黎曼–嘉唐流形；A2 局域 R 由局域 ρ 与宇宙背景挠率场 τ0 共同决定；
  A3 R ∝ ρ/ρ_c；A4 特征尺度 L ≡ 1/√|R|（内禀，抹除循环定义）；A5 α 为真正无量纲普适常数。
  主方程：R = (8πG/c⁴)ρ + α(ρ/ρ_c)τ0²                    ……(2)
  关键关系：ρ_c = c⁴τ0²/(8πG)  ⇒ τ0² = 8πGρ_c/c⁴        ……(R1)
  升级：τ0 → τ0(x)，G_eff(x) = G(1 + α c⁴τ0(x)²/(8πGρ_c))
  声称：α 保持普适；局域 τ0≈const ⇒ **自动还原牛顿引力/GR**；大尺度带来宇宙学修正。

本文件的核验结论（全部可复跑）：
  ✅【原稿自查属实】L=1/√|R| 代入 R=α ρ/(ρ_c L²) ⇒ R(1−αρ/ρ_c)=0 ⇒ 只有平凡解（代数坍缩）。
  ❌【本卷新发现·坍缩 #2】把原稿**自身**的关系 (R1) 代回 G_eff：
       G_eff/G = 1 + α·(c⁴τ0²)/(8πGρ_c) = 1 + α  ⇒ **与 x 无关的常数**
     ⇒ 「G_eff 空间变化」这一**唯一新物理**被原稿自身的定义抵消
     ⇒ 模型 ≡ GR + 常数重整化 G→G(1+α) ⇒ **局域不可观测**（撞定理 D）。
  ❌【公理不相容】EC 挠率由**自旋密度**代数确定（无自旋物质 ⇒ τ≡0），
     而 (2) 把 τ0 耦合到**能量密度 ρ** ⇒ **无 EC 依据**；「EC 挠率基底」是**形式装饰**：
     真实动力学 = GR + 一个标量场（dilaton）⇒ 属**标量–张量类**，非 EC。
  ❌【精细调节搬家】关系 (R1) 要求 τ0 ≈ 2.49e-42 GeV ⇒ τ0/M_Pl ≈ 2.0e-61；
     ρ_c/M_Pl⁴ ≈ 1.66e-123 与 τ0²/M_Pl² ≈ 4.16e-122 **仅差 8π** ⇒ Λ 的 122 量级调节
     **原封不动**搬进 τ0² 的 122 量级调节（撞定理 B/D）。
  ❌【局域无新物理】G_eff/G − 1 = α(1+δ)（δ = δτ0²/τ0²）；太阳系内 δ≈0
     ⇒ 局域**严格 GR** ⇒「牛顿极限冲突」是靠**让新项局域消失**解决的
     （即：把模型做成**局域不可检验**），不是靠新机制。
  ⚠️【可约束】非局域部分是「变化的 G」⇒ 受 Ġ/G 与 Cassini(ω_BD>40000) 约束；
     实跑给出 α ≲ 1e-3（由 |Ġ/G|<1e-13 yr⁻¹）。
  ❌【§5 正是定理 J 预言的「弃 A」路径】引入动力学 τ 场 + 势 V(τ) ⇒ 新标度 = **外生输入**；
     原稿**未声明**它已放弃「α 为拓扑常数」——即：本卷实际**已不是** H-TUFT 拓扑框架。
  ❌【真空极限自相矛盾】§4 称 ρ→0 ⇒ R→0，但 §5 的 V(τ) 极小值（自称「暗能量」）会源曲率
     ⇒ de Sitter 真空 ⇒ 与「R→0」冲突。

依赖 numpy；不引入新假设。
"""

import hashlib
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---- 物理常数（SI 与自然单位两套，互为交叉核对） ----
G_SI = 6.67430e-11            # m^3 kg^-1 s^-2
C_SI = 2.99792458e8           # m/s
RHO_C_MASS = 8.53e-27         # kg/m^3（Planck 2018, h≈0.674 的质量密度）
M_PL_GEV = 1.2209e19          # 普朗克质量 [GeV]
HBARC_GEV_M = 1.97327e-16     # hbar*c [GeV*m]
H0_PER_YR = 7.25e-11          # H0 = 1/(13.8 Gyr) [1/yr]
LLR_BOUND_PER_YR = 1.0e-13    # |Ġ/G| 上限（月激光测距量级）
OMEGA_BD_MIN = 40000.0        # Cassini: ω_BD > 40000


# ---------------------------------------------------------------- 基础换算
def rho_c_energy_gev4():
    """宇宙临界密度（能量密度）[GeV^4]。

    换算链：kg/m^3 -> J/m^3 (×c²) -> GeV/m^3 (÷1.602176634e-10) -> GeV^4 (×(hbar*c)^3)。
    """
    rho_j_per_m3 = RHO_C_MASS * C_SI ** 2           # J/m^3
    gev_per_m3 = rho_j_per_m3 / 1.602176634e-10     # GeV/m^3
    return gev_per_m3 * HBARC_GEV_M ** 3            # GeV^4


def tau0_from_rho_c_gev():
    """由关系 (R1) 反解背景挠率 τ0 [GeV]：τ0² = 8πGρ_c（自然单位）。"""
    return np.sqrt(8.0 * np.pi * rho_c_energy_gev4() / M_PL_GEV ** 2)


def tau0_from_si():
    """SI 路径：τ0² = 8πGρ_c/c⁴ [m^-2] ⇒ τ0 [m^-1] ⇒ [GeV]。"""
    rho_j = RHO_C_MASS * C_SI ** 2
    tau0_m = np.sqrt(8.0 * np.pi * G_SI * rho_j / C_SI ** 4)
    return tau0_m * HBARC_GEV_M, tau0_m


# ---------------------------------------------------------------- 坍缩核验
def collapse_1_residual(alpha, rho_over_rhoc):
    """原稿自查项：R = α(ρ/ρ_c)(R/?) 代入 L=1/√|R| 后的残差 R(1−αρ/ρ_c)。"""
    return 1.0 - alpha * rho_over_rhoc


def g_eff_over_G(alpha, tau0_sq_gev2, rho_c_gev4):
    """原稿 G_eff：G_eff/G = 1 + α·c⁴τ0²/(8πGρ_c)。

    自然单位（G = 1/M_Pl²）下即 1 + α·τ0²·M_Pl²/(8πρ_c)。
    """
    return 1.0 + alpha * tau0_sq_gev2 * M_PL_GEV ** 2 / (8.0 * np.pi * rho_c_gev4)


def g_eff_deviation(alpha, delta_tau2_rel):
    """局域偏离：G_eff/G − 1 = α(1+δ) 中的**相对**变化部分 = α·δ。"""
    return alpha * delta_tau2_rel


def gdot_over_g(alpha, m):
    """若 τ0² ∝ a^(−m)，则 Ġ/G ≈ −α·m·H0/(1+α)（今日值）[1/yr]。"""
    return -alpha * m * H0_PER_YR / (1.0 + alpha)


def ec_torsion_from_spin(spin_density):
    """EC 挠率由自旋密度**代数**决定：T^λ_μν ∝ s^λ_μν。无自旋 ⇒ 0。"""
    return spin_density


def _demo():
    print("=" * 76)
    print("攻坚续篇审读：EC 挠率基底重构 —— 逐条核验")
    print("=" * 76)

    print("\n" + "-" * 76)
    print("[1] 【原稿自查属实】L = 1/√|R| 代入旧标量式 ⇒ 代数坍缩")
    print("-" * 76)
    for a, rr in ((0.07, 0.5), (0.07, 1.0), (1.0, 1.0)):
        res = collapse_1_residual(a, rr)
        print("  α=%.2f, ρ/ρ_c=%.2f  ->  R(1-αρ/ρ_c)=0 的系数 = %+.4f  %s" % (
            a, rr, res, "（⇒ R 只能为 0）" if abs(res) > 1e-9 else "（⇒ 退化解 ρ=ρ_c/α）"))
    print("  ⇒ 原稿正确：该代数结构**不能承载非平凡局域解**。此点属实，方法上有真进步。")

    print("\n" + "-" * 76)
    print("[2] 【本卷新发现·坍缩 #2】G_eff 被原稿自身关系 (R1) 抵消")
    print("-" * 76)
    rho_c = rho_c_energy_gev4()
    tau0 = tau0_from_rho_c_gev()
    print("  由 (R1) 反解：ρ_c = %.4e GeV^4  =>  τ0 = %.4e GeV" % (rho_c, tau0))
    print("  代入 G_eff/G = 1 + α·τ0²/(8πGρ_c/c⁴)：")
    for a in (0.01, 0.1, 1.0):
        geff = g_eff_over_G(a, tau0 ** 2, rho_c)
        print("    α=%-5.2f  ->  G_eff/G = %.10f   （= 1+α = %.10f）" % (a, geff, 1.0 + a))
    print("  ⇒ G_eff/G = 1+α 为**常数**（与 x 无关）⇒ 「G_eff 空间变化」这一**唯一新物理**")
    print("    被原稿**自身**的定义抵消 ⇒ 模型 ≡ GR + 常数重整化 G→G(1+α) ⇒ 局域不可观测。")
    print("  ⚠ 且 R1 与「τ0(x) 空间变化」**互不相容**：R1 蕴含 ρ_c 随 x 变，而 ρ_c 是观测全局常数。")

    print("\n" + "-" * 76)
    print("[3] 【精细调节搬家】τ0 的量级与层级")
    print("-" * 76)
    tau0_si_gev, tau0_m = tau0_from_si()
    print("  SI 路径：τ0 = %.4e m^-1  ->  %.4e GeV（与自然单位路径 %.4e GeV 一致）" % (
        tau0_m, tau0_si_gev, tau0))
    print("  τ0/M_Pl = %.3e" % (tau0 / M_PL_GEV))
    print("  ρ_c/M_Pl^4      = %.3e" % (rho_c / M_PL_GEV ** 4))
    print("  τ0²/M_Pl²       = %.3e" % ((tau0 / M_PL_GEV) ** 2))
    print("  两者之比 = 1/(8π) = %.4f  ⇒  **同一个精细调节**（仅差一个 8π 因子）" % (
        (rho_c / M_PL_GEV ** 4) / ((tau0 / M_PL_GEV) ** 2)))
    print("  ⇒ Λ 的 ~122 量级调节**原封不动**搬进 τ0² 的 ~122 量级调节（撞定理 B/D）。")

    print("\n" + "-" * 76)
    print("[4] 【局域无新物理】偏离 = α·δ，太阳系内 δ≈0 ⇒ 严格 GR")
    print("-" * 76)
    for a, d in ((0.1, 0.0), (0.1, 1e-6), (0.1, 1e-2)):
        print("  α=%.2f, δτ0²/τ0²=%.0e  ->  (G_eff/G − 1) = %.3e" % (
            a, d, g_eff_deviation(a, d)))
    print("  ⇒ 「自动还原牛顿引力」靠的是**让新项局域消失**（δ→0），即把模型做成")
    print("    **局域不可检验**；这不是「解决冲突」，而是「删掉了冲突项」。")

    print("\n" + "-" * 76)
    print("[5] 【可约束】非局域部分是变化的 G ⇒ Ġ/G 给出 α 上限")
    print("-" * 76)
    print("  |Ġ/G| 观测上限 ≈ %.1e yr^-1（月激光测距量级）；H0 = %.3e yr^-1" % (
        LLR_BOUND_PER_YR, H0_PER_YR))
    for m in (1.0, 2.0, 3.0):
        a_max = LLR_BOUND_PER_YR / (m * H0_PER_YR)
        print("  τ0² ∝ a^-%.0f  ->  α_max = %.3e" % (m, a_max))
    print("  ⇒ α ≲ 1e-3（量级）——若 α 取 O(1)，模型被 |Ġ/G| 排除。")
    print("    另外 Cassini 要求 ω_BD > %.0f ⇒ 标量–张量耦合必须极弱（另一独立约束）。" % OMEGA_BD_MIN)

    print("\n" + "-" * 76)
    print("[6] 【公理不相容】EC 挠率由**自旋**代数决定，而原稿耦合到 ρ")
    print("-" * 76)
    for name, spin in (("理想流体/尘埃（ρ 的来源）", 0.0), ("辐射", 0.0),
                       ("极化费米子（自旋对齐）", 1.0)):
        print("  %-28s 自旋密度=%.1f  ->  EC 挠率 = %.1f" % (name, spin, ec_torsion_from_spin(spin)))
    print("  ⇒ 无自旋物质 ⇒ τ ≡ 0（EC 挠率**不**由能量密度源出）。")
    print("    原稿 (2) 把 τ0 耦合到 ρ ⇒ **无 EC 依据**；「EC 挠率基底」是**形式装饰**：")
    print("    真实动力学 = GR + 一个标量场（dilaton）⇒ 属**标量–张量类**，不是 EC。")

    print("\n" + "=" * 76)
    print("结论")
    print("=" * 76)
    print("  ① 原稿自查的「代数坍缩 #1」属实——方法上有真进步（诚实自诊）。")
    print("  ② 但其「修复」(2) 引出**坍缩 #2**：由原稿自身关系 (R1)，G_eff ≡ G(1+α) 常数")
    print("     ⇒ 唯一新物理被抵消 ⇒ 等价 GR + G 重整化（撞定理 D）。")
    print("  ③ A1（EC 基底）与 A2/A3（耦合到 ρ）**不相容**：EC 挠率源是自旋，不是能量密度。")
    print("  ④ ρ_c = c⁴τ0²/(8πG) 只把 Λ 精细调节**搬家**（同差 8π），未解决（撞定理 B/D）。")
    print("  ⑤ 局域严格 GR（δ≈0）⇒「牛顿极限冲突」是靠**删掉新项**解决的；")
    print("     非局域部分 = 变化的 G ⇒ Ġ/G 给出 α ≲ 1e-3。")
    print("  ⑥ §5 引入动力学 τ 场 + 势 V(τ) ⇔ **定理 J 预言的「弃 A」路径**：")
    print("     新标度由 V(τ) 的极小值给出 = **外生输入**；原稿未声明它已放弃「拓扑耦合」定义。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 76)
    print("本文件 SHA256 =", _selfhash())
    print("定位：攻坚续篇核验工具（非预言）。数学自洽 != 实验证实。")
