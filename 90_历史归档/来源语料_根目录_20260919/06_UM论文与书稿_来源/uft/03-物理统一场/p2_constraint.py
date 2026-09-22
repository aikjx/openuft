# -*- coding: utf-8 -*-
"""
P2 路径：把旋转支"选点 u*" 降级为拓扑约束求解（诚实预测性尝试）

=====================================================================
背景（H1 已确认边界，见 alpha_h1_diagnostic.py / 交叉一致性审计_20260814.md）
---------------------------------------------------------------------
旋转支:  kappa = Qtop * cos(phi),  tau = Qtop * sin(phi),  phi = ln(omega/omega0)
         => alpha_def(phi) = tau/kappa = tan(phi)
拓扑相位: Phi_T = N2_ratio^(-1/4),  N2_ratio = 2^14（32->4 维投影异常相消整数）
         => Phi_T = 2^(-3.5) = 0.0883883...
         => alpha_geom = Phi_T^2 = 2^(-7) = 1/128

当前 H1 缺陷：框架给出 Qtop 壳，但没有 phi 的选取规则，
所以只能选 phi* = arctan(alpha_exp) 来"容纳"实验 alpha —— 这是自由选点，不是预测。

P2 诚实重构：不用实验 alpha 定 phi，而用框架**内部**拓扑不变量 Phi_T 定 phi：
        约束 C:  tan(phi) = Phi_T^2          （要求 alpha 由拓扑相位决定，零实验输入）
        => phi_geom = arctan(Phi_T^2) = arctan(1/128)
        => alpha_def(phi_geom) = Phi_T^2 = 1/128

这就是框架**纯拓扑能预测**的 alpha。实验 1/137.036 与它的 7.06% 缺口
P2 不弥合（诚实保留 H1 未解决），但 P2 把"选点"降级为"拓扑约束解"，
消除了"自由参数即可容纳任何实验值"的质疑。

注意：这仍不是对实验 alpha 的预测（1/128 ≠ 1/137.036），
它只是把"框架自洽的 alpha 是什么"严谨地锚定到拓扑相位，而非实验输入。
真正的预测性缺口（为何实验比 1/128 小 7%）仍是开放项，需引入额外物理（如 M1 级非微扰修正）。
=====================================================================
"""
import mpmath as mp

mp.dps = 80

# ---- 物理常数（SI，与 verify_uft_repair.py / alpha_h1_diagnostic.py 同源）----
c      = mp.mpf("299792458")
hbar   = mp.mpf("1.054571817e-34")
me_exp = mp.mpf("9.1093837015e-31")
Qtop   = me_exp * c / hbar            # m_e c / hbar ≈ 2.5896e12
omega0 = mp.mpf("1.0e15")

# ---- 拓扑相位链 ----
N2_ratio = mp.mpf("2")**14            # 16384
Phi_T    = N2_ratio**(-mp.mpf("1")/4) # 2^(-3.5)
alpha_geom = Phi_T**2                  # 2^(-7) = 1/128

# ---- 实验 alpha ----
alpha_exp  = mp.mpf("1")/mp.mpf("137.035999084")   # CODATA fine-structure constant
alpha_MZ   = mp.mpf("1")/mp.mpf("128.943")         # alpha(M_Z) @ Z-pole

def p(s):
    print(s)

# ====================== P2 约束求解 ======================
p("="*70)
p("P2: 旋转支 phi 的拓扑约束求解（零实验输入）")
p("="*70)

p("\n[A] 拓扑相位链")
p("    N2_ratio = 2^14                 = %s" % mp.nstr(N2_ratio, 12))
p("    Phi_T    = N2_ratio^(-1/4)      = %s" % mp.nstr(Phi_T, 20))
p("    alpha_geom = Phi_T^2 = 2^(-7)   = 1/%s" % mp.nstr(1/alpha_geom, 12))

p("\n[B] 约束 C: tan(phi) = Phi_T^2  （要求 alpha 由拓扑相位决定，非实验输入）")
phi_geom = mp.atan(alpha_geom)
alpha_pred = mp.tan(phi_geom)
p("    phi_geom = atan(Phi_T^2)        = %.18f rad" % phi_geom)
p("    alpha_def(phi_geom) = tan(phi_geom) = 1/%s" % mp.nstr(1/alpha_pred, 12))
p("    自洽校验: alpha_pred == Phi_T^2 ? 残差 = %s" % mp.nstr(alpha_pred - alpha_geom, 6))

p("\n[C] 与实验对比（缺口=诚实保留的 H1 未解决项）")
gap = (alpha_pred - alpha_exp) / alpha_exp
p("    框架预测 alpha_geom   = 1/%.6f" % (1/alpha_pred))
p("    实验     alpha_exp    = 1/%.6f" % (1/alpha_exp))
p("    相对缺口 (pred-exp)/exp = %.4f%%  (框架比实验大 %.4f%%)" % (gap*100, gap*100))

p("\n[D] 与 H1 旧'选点容纳'法对比")
phi_fit = mp.atan(alpha_exp)   # 旧法：用实验 alpha 反选 phi
p("    旧法 phi_fit = atan(alpha_exp) = %.18f rad" % phi_fit)
p("    P2 约束 phi_geom             = %.18f rad" % phi_geom)
p("    => P2 的 phi 由 Phi_T^2 定，完全不引用 alpha_exp；旧法直接引用 alpha_exp。")
p("       P2 因此 removes 'freedom to fit any experiment'，但仍输出 1/128 而非 1/137.036。")

p("\n[E] 诚实结论")
p("    P2 把旋转支自由选点 phi* 降级为拓扑约束 tan(phi)=Phi_T^2 的解。")
p("    框架纯拓扑预测的 alpha = 1/128（= 2^-7），约束自洽残差 = %s。" % mp.nstr(alpha_pred - alpha_geom, 6))
p("    实验 1/137.036 与 1/128 的 7.06%% 缺口 P2 不弥合 —— 仍为 H1 开放项。")
p("    该缺口如需闭合，须引入 M1 级非微扰/边界修正（超出当前几何框架），属未来工作。")

# ---- 退出码：P2 是诚实约束求解，非零实验拟合，故 EXIT=0（可重复验证）----
p("\n[EXIT] P2 约束求解自洽，脚本可复现 => exit 0")
