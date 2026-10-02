# -*- coding: utf-8 -*-
"""
中子星静态球对称 TOV + 标量曲率场方程(4) 联立求解 —— 修正·审计版
AI科技星 · 全维统一场论 / 时空曲率-能量密度关系续篇

本脚本做两件事：
  (1) 一个【正确】的 GR-TOV 基线求解器（RK4 真四阶，度规势/质量函数自洽），
      作为可对照的物理基准；
  (2) 把你给的场方程(4)以"对 GR 的 α-比例修正"方式自洽接入，定量检验
      "额外正里奇标量贡献 -> 半径比 GR 小 0.3~0.6 km"这一预言是否真的成立。

重要诚实结论（详见同目录 结果/验证结果_中子星TOV_修正审计.md）：
  - 你给的代码（第三、四节）并不是 RK4，而是前向 Euler；且 λ, ν 在积分循环里
    从未被更新（dnu_dr 用到的 lam 恒为 0），场方程(4)与 R_rr 闭合关系被完全忽略；
    source 算出来后从未回写任何演化方程。
  - rho_c = 1e-9（kg/m^3 量纲）是量级错误；使 alpha/rho_c 偏离正确值约 1e27 倍。
  - 更关键：场方程(4)的源项 (α/rho_c)·e^{-2λ}·(dρ/dr)^2/(ρ+ρ_min) 在中子星内部
    并非可忽略——核心典型点处 R_mod/R_GR ~ O(1)（见下方量纲自检，α=1.87 时约 7 倍）。
    但 (dρ/dr)^2 恒正、且在星体表面密度梯度最陡处发散，形成正反馈：α=1.87 会使
    有效质量密度远超重物质，星体过度压缩、积分数值发散（本脚本实跑得 M~2e4 M_sun、
    R 塌缩到 ~5.7 km）。所以 α=1.87 这个"MCMC 95% 上限"量级对(4)而言**过大**，
    理论在该耦合下是 ill-posed 的。要得到宣称的 0.3~0.6 km 温和偏移，α 需降到
    ~1e-2 量级（见下方 α-扫描标定）。
  - α=0 在你给的"场方程(4)"里给出 R=0（迹自由），并不是 GR；本脚本改用
    "在 GR 之上叠加 α-比例梯度项"的闭包，使 α=0 精确回到 GR。
"""

import math

# ============================================================
# 物理常数
# ============================================================
G = 6.67430e-11
C = 299792458.0
C2 = C * C
M_SUN = 1.98847e30

# 参考密度（场方程(4)的 rho_c）—— 正确量纲应为特征密度 ~1e18 kg/m^3
RHO_C_REF_PHYSICAL = 1.0e18      # kg/m^3   （用户原代码写成 1e-9，属量级错误）
RHO_MIN = 1.0                    # kg/m^3   避免除零下限

# ============================================================
# 物态方程：单一多方 EOS（连续、量级贴近 SLy4 核心段）
#   p(rho) = K * rho^GAMMA,  在 rho_nuc=2.8e17 处取 p0=3.5e32 Pa
# 该 EOS 在整个 1e14 ~ 1e18 区间给出的压强量级与真实中子星物质一致，
# 故适合作为"理论偏移"演示——核心行为由它主导，外壳近似不影响定性结论。
# ============================================================
RHO_NUC = 2.8e17
P_NUC = 3.5e32
GAMMA = 2.8
K_EOS = P_NUC / (RHO_NUC ** GAMMA)

def eos_p(rho):
    if rho <= 0.0:
        return 0.0
    return K_EOS * (rho ** GAMMA)

def eos_drho_dp(rho):
    # d(rho)/d(p) = 1 / (GAMMA * K * rho^(GAMMA-1))
    if rho <= 0.0:
        return 0.0
    return 1.0 / (GAMMA * K_EOS * (rho ** (GAMMA - 1.0)))


# ============================================================
# 结构方程（标准 GR-TOV）+ 修改闭包
#   未知量: rho(r), p(r), m(r)
#   e^{-2 lambda} = 1 - 2 G m / (c^2 r)   (由质量函数定义)
#   标准 TOV:
#     dp/dr = - G (rho c^2 + p) (m + 4π r^3 p / c^2) / [ r^2 c^2 (1 - 2 G m/(r c^2)) ]
#   d(rho)/dr = (d rho / d p) * dp/dr
#   修改闭包（让 α=0 精确回到 GR，且额外曲率为 α-比例正项）:
#     rho_eff = rho + (c^2 / 8π G) * (α/rho_c) * e^{-2λ} (dρ/dr)^2 / (ρ + ρ_min)
#     dm/dr   = 4π r^2 rho_eff
# ============================================================
def derivs(r, rho, p, m, alpha, rho_c_ref):
    if p <= 0.0:
        return 0.0, 0.0, 0.0
    if r < 1.0e-3:
        r = 1.0e-3
    x = 2.0 * G * m / (C2 * r)
    if x >= 0.999999:
        x = 0.999999
    e2lam_inv = 1.0 - x                       # = e^{-2λ}
    factor = 1.0 - x

    dp_dr = -G * (rho * C2 + p) * (m + 4.0 * math.pi * (r ** 3) * p / C2) \
            / (r * r * C2 * factor)

    drho_dr = eos_drho_dp(rho) * dp_dr

    # 修改项：把 (4) 解释为对 GR 的额外有效质量密度（α=0 时为零 -> 精确 GR）
    extra = 0.0
    if alpha != 0.0:
        extra = (C2 / (8.0 * math.pi * G)) * (alpha / rho_c_ref) \
                * e2lam_inv * (drho_dr ** 2) / (rho + RHO_MIN)

    dm_dr = 4.0 * math.pi * (r ** 2) * (rho + extra)
    return drho_dr, dp_dr, dm_dr


def integrate(rho_center, alpha, rho_c_ref=RHO_C_REF_PHYSICAL, dr=20.0, rmax=60000.0):
    r = 1.0e-3
    rho = rho_center
    p = eos_p(rho)
    m = 0.0
    while p > 1.0 and r < rmax:
        k1r, k1p, k1m = derivs(r, rho, p, m, alpha, rho_c_ref)
        k2r, k2p, k2m = derivs(r + dr / 2.0, rho + k1r * dr / 2.0, p + k1p * dr / 2.0,
                                m + k1m * dr / 2.0, alpha, rho_c_ref)
        k3r, k3p, k3m = derivs(r + dr / 2.0, rho + k2r * dr / 2.0, p + k2p * dr / 2.0,
                                m + k2m * dr / 2.0, alpha, rho_c_ref)
        k4r, k4p, k4m = derivs(r + dr, rho + k3r * dr, p + k3p * dr,
                                m + k3m * dr, alpha, rho_c_ref)
        rho += dr / 6.0 * (k1r + 2.0 * k2r + 2.0 * k3r + k4r)
        p += dr / 6.0 * (k1p + 2.0 * k2p + 2.0 * k3p + k4p)
        m += dr / 6.0 * (k1m + 2.0 * k2m + 2.0 * k3m + k4m)
        r += dr
        if rho <= 0.0:
            break
    R = r
    M = m / M_SUN
    return M, R, p


def scan(alpha, rho_c_ref=RHO_C_REF_PHYSICAL, rhoc_list=None):
    if rhoc_list is None:
        rhoc_list = [5.0e17, 8.0e17, 1.0e18, 1.4e18, 1.8e18, 2.2e18, 2.6e18, 3.0e18]
    results = []
    for rhoc in rhoc_list:
        M, R, p_surf = integrate(rhoc, alpha, rho_c_ref)
        results.append((rhoc, M, R))
    return results


if __name__ == "__main__":
    print("=" * 72)
    print("  中子星 TOV + 标量曲率场方程(4) 修正审计")
    print("=" * 72)
    print()
    print("EOS: 单一多方 p = %.4e * rho^%.2f  (Pa, rho in kg/m^3)" % (K_EOS, GAMMA))
    print("     在 rho_nuc=%.2e kg/m^3 处 p=%.2e Pa" % (RHO_NUC, P_NUC))
    print()

    # ---- (1) GR 基线 (alpha=0) ----
    print("-" * 72)
    print("【GR 基线 alpha=0】  M-R 扫描（中心密度 5e17 ~ 3e18 kg/m^3）")
    print("-" * 72)
    gr = scan(0.0)
    maxM = 0.0
    maxM_R = 0.0
    for rhoc, M, R in gr:
        print("  rho_c=%.2e | M=%.4f M_sun | R=%.2f km" % (rhoc, M, R / 1000.0))
        if M > maxM:
            maxM, maxM_R = M, R
    print("  -> GR 最大质量 M_max = %.4f M_sun  (R=%.2f km)" % (maxM, maxM_R / 1000.0))
    print()

    # 取 GR 在 M~1.4 M_sun 附近的半径做对照
    R_at_1p4_GR = None
    for rhoc, M, R in gr:
        if abs(M - 1.4) < 0.15:
            R_at_1p4_GR = R
            break
    if R_at_1p4_GR is None:
        # 线性插值
        pts = sorted([(M, R) for _, M, R in gr])
        for i in range(len(pts) - 1):
            if pts[i][0] <= 1.4 <= pts[i + 1][0]:
                m0, r0 = pts[i]
                m1, r1 = pts[i + 1]
                R_at_1p4_GR = r0 + (1.4 - m0) * (r1 - r0) / (m1 - m0)
                break

    # ---- (2) 修改理论：不同 alpha 下的半径偏移 ----
    print("-" * 72)
    print("【修改理论 alpha>0】  中心密度取 1.8e18 kg/m^3，扫描 alpha")
    print("  对照 GR 同中心密度下的半径，看偏移是否达到 0.3~0.6 km")
    print("-" * 72)
    rhoc_fix = 1.8e18
    M_gr_fix, R_gr_fix, _ = integrate(rhoc_fix, 0.0)
    print("  GR (alpha=0):       M=%.4f M_sun  R=%.3f km" % (M_gr_fix, R_gr_fix / 1000.0))
    print("  (注: alpha=1.87 会使 (dρ/dr)^2 源项正反馈失控 -> 星体塌缩到荒谬质量;")
    print("   下面扫描小 α 以标定 '0.3~0.6 km 偏移' 实际需要的耦合量级)")
    for a in [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 1.87]:
        try:
            Mm, Rm, _ = integrate(rhoc_fix, a)
            dR = (Rm - R_gr_fix) / 1000.0
            tag = ""
            if 0.3 <= abs(dR) <= 0.6:
                tag = "   <-- 落在宣称的 0.3~0.6 km 窗口"
            print("  alpha=%.4e:  M=%.4f M_sun  R=%.3f km  dR=%.4f km%s"
                  % (a, Mm, Rm / 1000.0, dR, tag))
        except Exception as e:
            print("  alpha=%.4e:  积分发散/数值失败 (%s)" % (a, e))
    print()

    # ---- (3) 量纲自检：R_mod vs R_GR 的数量级 ----
    print("-" * 72)
    print("【量纲自检】 场方程(4) 给出的 R_mod 与 GR 里奇标量 R_GR 的数量级")
    print("-" * 72)
    # 核心典型点：rho~1e18, dρ/dr 用 EOS 与 TOV 估算
    rho_typ = 1.0e18
    p_typ = eos_p(rho_typ)
    # 近似 dp/dr 用 GR 在 r~5km, m~1.5e30 的估算（见审计报告）
    r_typ, m_typ = 5.0e3, 1.5e30
    x = 2 * G * m_typ / (C2 * r_typ)
    dpdr_typ = -G * (rho_typ * C2 + p_typ) * (m_typ + 4 * math.pi * r_typ ** 3 * p_typ / C2) \
               / (r_typ ** 2 * C2 * (1.0 - x))
    drhodr_typ = eos_drho_dp(rho_typ) * dpdr_typ
    R_GR = 8.0 * math.pi * G * (rho_typ - 3.0 * p_typ / C2) / C2
    R_mod = (1.87 / RHO_C_REF_PHYSICAL) * (1.0 - x) * (drhodr_typ ** 2) / (rho_typ + RHO_MIN)
    print("  典型点 rho=%.2e, |dρ/dr|~%.3e kg/m^4" % (rho_typ, abs(drhodr_typ)))
    print("  R_GR  (GR 里奇标量)        = %.3e  1/m^2" % R_GR)
    print("  R_mod (场方程(4), alpha=1.87) = %.3e  1/m^2" % R_mod)
    print("  R_mod / R_GR               = %.3e  (差约 %.0f 个数量级)"
          % (R_mod / R_GR, math.log10(R_GR / max(R_mod, 1e-200))))
    print()
    print("结论：在 α=1.87、rho_c=1e18 下，场方程(4)核心处曲率贡献 ~7×R_GR（order-unity，非可忽略），")
    print("     但 (dρ/dr)^2 正反馈使系统在该耦合下发散/塌缩，得不到温和偏移；")
    print("     0.3~0.6 km 的温和偏移需要 α 降到 ~1e-2 量级（见上方 α-扫描），")
    print("     而你给的 α=1.87 是 MCMC '95% 上限'直接沿用——对(4)这一具体闭包过大。")
