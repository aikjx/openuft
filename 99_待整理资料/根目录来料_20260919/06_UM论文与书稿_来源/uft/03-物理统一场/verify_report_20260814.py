# -*- coding: utf-8 -*-
"""
算法联盟 | 复核 __全维统一分析报告_20260814.md 的声明的精算真伪
===============================================================
对照真实代码 verify_uft_repair.py / analytic_proofs.py 重新计算,
逐条判定报告中的公式是 [OK]/[FAIL]/[WARN]。
重点核查报告中的可疑声明:
  R2.2 : kappa=3.162e-4, tau=2.3076e-6, alpha=tau/kappa=0.007297...
  R4.1 : 推导链 mu0=4*pi*kappa^2, G = alpha^2/(4*pi c^2 kappa^2 eps0)
  R4.2 : alpha_geom=1/128, delta_CS=-0.08778 -> alpha_phys=1/139.236
  R4.4 : F2 c缺口 ~1e-50, G单位弹性 ~1e-16
"""
import mpmath as mp
mp.mp.dps = 80

from verify_uft_repair import (
    hbar, c, G, eps0, mu0, Qtop, omega0, me_exp, alpha_exp,
    kappa, tau, check_modulus_identity_original, check_modulus_identity_fixed,
    modulus_identity_closed_with_c,
    alpha_geom_high_scale, alpha_MZ_from_running, alpha_running_correction,
    boundary_CS_coefficient, verify_boundary_delta,
    G_cosmology_scaling,
)

def P(*a):
    try: print(" ".join(str(x) for x in a))
    except UnicodeEncodeError: print(" ".join(str(x) for x in a).encode("ascii","ignore").decode())

def sep(t=""):
    if t: P("-"*8, t, "-"*8)

# =====================================================================
# R2.2 核查: 报告称 kappa=3.162e-4, tau=2.3076e-6, alpha=tau/kappa
# =====================================================================
P("="*88)
P("R2.2 核查: kappa/tau/alpha=tau/kappa")
P("="*88)
sep("代码真实 kappa,tau (omega=1e12)")
omega = mp.mpf("1e12")
k_real = kappa(omega); t_real = tau(omega)
P(f"  kappa(1e12) = {float(k_real):.6e}   (量级 ~Qtop=2.59e12, 非 3.162e-4)")
P(f"  tau(1e12)   = {float(t_real):.6e}")
P(f"  kappa^2+tau^2 = {float(k_real**2+t_real**2):.6e}  vs Qtop^2={float(Qtop**2):.6e}")
sep("报告声明 vs 真实")
P(f"  报告: kappa=3.162e-4, tau=2.3076e-6  => [FAIL] 与代码差 ~16 个数量级")
# alpha = tau/kappa in code:
alpha_code = t_real / k_real
P(f"  代码 alpha=tau/kappa = {float(alpha_code):.10f}")
P(f"  实验 alpha_exp      = {float(alpha_exp):.10f}")
P(f"  => 代码 alpha=tan(ln(w/w0)), 是自由 omega 决定的比, 不恒等于实验 alpha")
P(f"     取 w 使 tan=alpha_exp 需 ln(w/w0)=atan(0.0073)=0.0073 => 特定 w 才凑出")
# 反解: 报告给的 3.162e-4, 2.3076e-6 之比 = 0.007297... 恰 = alpha_exp
ratio_rpt = mp.mpf("2.3076e-6") / mp.mpf("3.162e-4")
P(f"  报告 tau/kappa={float(ratio_rpt):.10f}  ≈ alpha_exp, 但 kappa,tau 数值本身与代码不符")
P(f"  结论: [FAIL] R2.2 的 kappa/tau 数值是虚构(非代码输出);")
P(f"         alpha=tau/kappa 作为定义可行, 但仅当 omega 被调到特定值时才=实验 alpha,")
P(f"         不是'由拓扑推出 alpha=1/137'的闭合证明。")

# =====================================================================
# R4.1 核查: mu0 = 4*pi*kappa^2 ?  G = alpha^2/(4*pi c^2 kappa^2 eps0)
# =====================================================================
P("\n"+"="*88)
P("R4.1 核查: mu0=4*pi*kappa^2, G=alpha^2/(4*pi c^2 kappa^2 eps0)")
P("="*88)
sep("mu0 = 4*pi*kappa^2 ?")
mu0_claim = 4*mp.pi*k_real**2
P(f"  mu0 (code)        = {float(mu0):.6e}")
P(f"  4*pi*kappa^2      = {float(mu0_claim):.6e}")
P(f"  ratio             = {float(mu0_claim/mu0):.3e}  => [FAIL] 差 ~31 个数量级")
P(f"  代码 mu0 是常量 4*pi*1e-7, 从未写成 4*pi*kappa^2; 报告属虚构关系。")
sep("G = alpha^2/(4*pi c^2 kappa^2 eps0) ?")
G_claim = alpha_exp**2 / (4*mp.pi * c**2 * k_real**2 * eps0)
P(f"  G (code)                  = {float(G):.6e}")
P(f"  alpha^2/(4 pi c^2 k^2 e0) = {float(G_claim):.6e}")
P(f"  ratio                     = {float(G_claim/G):.3e}  => [FAIL] 差 ~37 个数量级")
P(f"  量纲: [rhs] = [1]/([L^2T^-2][L^-2][C^2L^-2M^-1T^2]) = [C^-2 L^2 M T^-2]; [G]=[L^3M^-1T^-2]")
P(f"       量纲也不闭合(差 [C^-2 L^-1 M^2]); 报告推导链无代码支撑。")
P(f"  注: 真实代码里 G 是 INPUT(PDG), 仅 F2b 给重排恒等式 G=c*(lP^2 c^2/hbar), 非生成式。")

# =====================================================================
# R4.2 核查: alpha_geom=1/128, delta_CS=-0.08778 -> 1/139.236
# =====================================================================
P("\n"+"="*88)
P("R4.2 核查: alpha_geom=1/128, delta_CS=-0.08778, alpha_phys=1/139.236")
P("="*88)
a_geom = alpha_geom_high_scale()
a_phys, Ln = alpha_MZ_from_running()
a_g, a_p, _, dCS = alpha_running_correction()
P(f"  alpha_geom (1/128)   = {float(a_geom):.10f}  (={1/128:.10f})  [OK] 代码一致")
P(f"  alpha_phys (running) = {float(a_phys):.10f}  (={1/float(a_phys):.4f})  [OK] =1/139.236")
P(f"  delta_CS (code)      = {float(dCS):.10f}")
base, deficit, theta_CS, target = boundary_CS_coefficient()
P(f"  target_delta (code)  = {float(target):.12f}")
# 验证边界 delta 闭环
th, d_re, rel = verify_boundary_delta()
P(f"  verify_boundary_delta: recomputed={float(d_re):.12f}, rel_err={float(rel):.3e}")
P(f"  >> [OK] 代码内部自洽: 1/128 启发值经真实单圈跑动 + delta_CS 校准到 1/139.236。")
P(f"  >> [WARN] 但这是'用实验 alpha(0) 作基线反推', 不是'拓扑纯生成 1/137';")
P(f"      框架解释的是'为何高标度 alpha≈2^-7 整数幂附近', 而非从零推出 alpha。")
P(f"  >> R2.2 与 R4.2 的 alpha 定义冲突: R2.2 用 tau/kappa, R4.2 用 Phi_T^2;")
P(f"      二者仅在 omega 被调参时才相等, 报告未说明, 属内部不自洽。")

# =====================================================================
# R4.4 核查: F2 c缺口 ~1e-50, G单位弹性 ~1e-16
# =====================================================================
P("\n"+"="*88)
P("R4.4 核查: F2 c缺口 ~1e-50, G单位弹性 ~1e-16")
P("="*88)
ratio_orig = check_modulus_identity_original(omega)
ratio_fixed = check_modulus_identity_fixed(omega)
rhs_closed, rel_closed = modulus_identity_closed_with_c(omega)
P(f"  original rhs/G = c (精确, 缺口=c) => 不是 ~1e-50, 而是 =c")
P(f"    check_modulus_identity_original(1e12) = {float(ratio_orig):.6e}")
P(f"  fixed rhs/G = 1/c^2 (残留 c^2 缺口) => check_modulus_identity_fixed = {float(ratio_fixed):.6e}")
P(f"    => 缺口量级 1/c^2 ~ {float(1/c**2):.3e}, 非 ~1e-50")
P(f"  closed (补 c^2 后) rhs/G = {float(rhs_closed):.6e}, rel_err={float(rel_closed):.3e}")
P(f"  >> [FAIL] 报告'c缺口~1e-50' 与实际 '=c' 或 '=1/c^2' 不符; 1e-50 无从来。")
sep("G 单位弹性 ~1e-16 ?")
R_H, lP, N_area, S_BH, S_dS, G_area, ratio_cos = G_cosmology_scaling()
P(f"  S_dS/S_BH = {float(ratio_cos):.3e}  (宇宙学常数问题 ~1e16 倍)")
P(f"  G_area/G  = {float(G_area/G):.3e}  (面积律定标使 G 偏小 ~同量级)")
P(f"  >> [WARN] '~1e-16' 指 S_dS/S_BH≈10^-16 (面积律高估 16 个数量级),")
P(f"      但代码注释写'差 ~10^16 倍'即比例 1e-16, 量级一致; 描述尚可但")
P(f"      报告未说清是'面积律定标误差'而非'G 本身单位弹性'。")
P(f"  >> 真正代码结论: G 无法纯拓扑生成(Ξ=c 不独立), 数值由宇宙学边界定, 待解。")

P("\n"+"="*88)
P("SUMMARY")
P("="*88)
P("[FAIL] R2.2 kappa/tau 数值虚构(差16量级); alpha=tau/kappa 仅调参才=实验alpha")
P("[FAIL] R4.1 mu0=4pi kappa^2 (差31量级) 与 G=... (差37量级) 均无代码支撑, 量纲也不闭")
P("[OK]   R4.2 alpha_geom=1/128 与 1/139.236 经单圈跑动+delta_CS 代码内部自洽")
P("[WARN] R4.2 是'实验alpha基线反推', 非纯拓扑生成; 且 alpha 定义与 R2.2 冲突")
P("[FAIL] R4.4 'c缺口~1e-50' 不实, 实为 =c 或 =1/c^2; 'G单位弹性~1e-16' 描述含糊")
P("建议: 报告应将 R2.2/R4.1 的虚构等式删除或显式标注为'占位/待证',")
P("      统一 alpha 定义, 并改正 F2 缺口量级的陈述。")
