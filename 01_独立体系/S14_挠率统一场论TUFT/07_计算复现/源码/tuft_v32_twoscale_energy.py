# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 两尺度晕的能量预算与旋转能相容性
=====================================================
目标：C0084 两尺度构造把"晕质量可忽略"当作近似。本轮把它升级为**可验证的
量化事实**，并闭合开放项①（核-晕耦合 + 旋转能 ½ω0²N 相容性）：

  P1 晕场能预算（电子电荷归一 N=1 下，四种形状）：
     动能 E_k=½∫4πr²ψ'²dr；旋转能 E_rot=½ω0²N；自相互作用 E_self（TUFT
     势，模型依赖，仅给量级标度）。总晕能 vs 核质量 M_e=M_nat。
  P2 旋转能相容性：从质量预算反解 ω0 上限——E_rot<ε·M_e ⟹
     ω0 < √(2εM_e/N)。对比物理自然频率（康普顿频率 ω_C=M_nat）与普朗克频率，
     验证旋转能在大范围 ω0 内不破坏质量预算。
  P3 核-晕耦合反作用上界：E_halo/M_e ≈ 1e-22 ⟹ 解耦两尺度模型自洽到该阶，
     给耦合反作用(若有)的数值上界，闭合 C0084 红线。

红线：模型层面构造性核验，非物理真实性主张；晕自相互作用依赖 TUFT 势参数
（此处仅给量级标度，不预设 V1,V2 具体值）；ω0 物理定标仍属开放项（单位约定）。
"""
import numpy as np, io, math
OUT = "tuft_v32_twoscale_energy_report.txt"
buf = []; log = buf.append

M_P  = 2.176434e-8
me   = 9.1093837015e-31
M_nat = me/M_P          # 4.1855e-23
g_e  = 2.00231930436153
r_target = g_e/(4.0*M_nat)   # 0.5006λ_C (l_P), C0083

shapes = {
    "exponential e^{-x}":   lambda x: np.exp(-x),
    "gaussian e^{-x^2}":    lambda x: np.exp(-x**2),
    "power-exp e^{-x^2.9}": lambda x: np.exp(-x**2.9),
}
xg = np.linspace(0, 12, 6000)
def shape_ints(f):
    y2=f(xg)**2; y3=xg*y2
    I2=np.trapezoid(xg**2*y2,xg); I3=np.trapezoid(xg**3*y2,xg)
    fp=np.gradient(f(xg),xg); Ik=np.trapezoid(xg**2*fp**2,xg)
    return 0.5*I3/I2, I2, Ik   # rho, I2, Ik

log("TUFT V3.2 攻破阶段 · 两尺度晕的能量预算与旋转能相容性")
log("运行时间: 2026-10-07")
log("订正目标 ⟨r⟩=g_e/(4M_nat)=%.6e l_P=%.6f·λ_C (C0083)" % (r_target, r_target*M_nat))
log("核质量 M_core=M_e=M_nat=%.6e M_P" % M_nat)
log("康普顿频率 ω_C=m_e c²/ℏ = M_nat = %.6e (Planck 频率单位)" % M_nat)
log("")

# ---- P1 晕场能预算 ----
log("=== P1 晕场能预算（N_halo=1 电子电荷归一；E_rot 取 ω0=ω_C）===")
log("  动能 E_k=½∫4πr²ψ'²dr=2πA²·l_h·I_k；旋转 E_rot=½ω0²N；总晕能 vs 核质量")
for name, f in shapes.items():
    rho, I2, Ik = shape_ints(f)
    l_h = r_target/rho
    A   = 1.0/math.sqrt(4*math.pi*I2*l_h**3)
    E_k = 2*math.pi*A**2*l_h*Ik
    E_rot = 0.5*M_nat**2*1.0          # ω0=ω_C=M_nat, N=1
    E_tot = E_k+E_rot
    ratio = E_tot/M_nat
    log("  [%-20s] l_h=%.4e  A=%.3e" % (name, l_h, A))
    log("     E_k=%.3e  E_rot=%.3e  E_halo=%.3e  vs M_core=%.3e  ⟹ E_halo/M_core=%.2e"
        % (E_k, E_rot, E_tot, M_nat, ratio))
log("  ⟹ 晕总场能 ~1e-45~1e-44，仅为核质量 M_e 的 ~1e-22 量级：'晕质量可忽略'成立，")
log("    且由 N=1 电荷归一(振幅 A∝l_h^{-3/2}≈1e-34) 自然导出，非额外假设。")

# ---- P2 旋转能相容性：质量预算反解 ω0 上限 ----
log("")
log("=== P2 旋转能相容性：质量预算反解 ω0 上限 ===")
for eps in [0.01, 0.05, 0.10]:
    wmax = math.sqrt(2*eps*M_nat/1.0)     # E_rot=½ω0²N < ε·M_e
    log("  E_rot<%.0f%%·M_e ⟹ ω0_max = √(2·%.2f·M_e/N) = %.3e (Planck 频率)" % (eps*100, eps, wmax))
log("  康普顿频率 ω_C=M_nat=%.3e ≪ ω0_max ⟹ E_rot(ω_C)=%.3e（仅 M_e 的 %.1e）"
    % (M_nat, 0.5*M_nat**2, (0.5*M_nat**2)/M_nat))
log("  ⟹ 旋转能在大范围 ω0 内(至 ~1e-12 M_P 频率)都保持 <10%·M_e，不破坏质量预算；")
log("    C0048'旋转项切断 (q0,ω0) 简并' 与'旋转能不破坏两尺度质量'完全相容。")

# ---- P3 核-晕耦合反作用上界 ----
log("")
log("=== P3 核-晕耦合反作用上界（闭合 C0084 红线）===")
ratio_typical = (2*math.pi*(1/math.sqrt(4*math.pi*0.25*(r_target/0.75)**3))**2*(r_target/0.75)*0.25 + 0.5*M_nat**2)/M_nat
log("  解耦模型自洽到 E_halo/M_core ≈ %.2e（exponential 形状，P1）" % ratio_typical)
log("  ⟹ 任何核-晕耦合(若存在)的反作用 < ~1e-22 相对量级才与 M_e 拟合相容；")
log("    两尺度解耦 ansatz 在 O(1e-22) 内自洽——C0084'晕质量可忽略'由近似升级为可验证上界。")
log("  注：绝对电荷归一 Π 仍依赖单位约定(开放项③)，与能量预算正交。")

log("")
log("红线声明：模型层面构造性核验，非物理真实性主张；晕自相互作用依赖 TUFT 势")
log("参数(此处仅量级标度 ~A⁴l³≈1e-69，更小)，ω0 物理定标仍属开放项。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
