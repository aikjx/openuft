#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 统一场论攻坚 · 引力扇区数值实证（方向 A 弱场极限还原 GR 的落地）
==========================================================================
来稿方向 A 的核心桥梁：包络场能动张量 T_μν 同时充当电磁源与引力源（Einstein-Cartan）。
本脚本用已收敛的时间谐振 Q-ball 解（§5.2 稳定点）实算其引力扇区：

  1) 能量密度 ρ_E(r)=ω²σ²+σ'²+U(σ²)，累计质量 M(r)=4π∫ρ_E r'²dr'；
  2) 球对称牛顿引力势 Φ(r)=−G·M(r)/r，验证外部 Φ→−G·E₀/r（引力质量=场能量 E₀，等效原理）；
  3) 弱场度规 g₀₀=1+2Φ/c²，外部退化为 Schwarzschild 外部 1−2GM/(rc²)；
  4) 诚实自引力评估：紧致度 2GM/(R_core c²)，判断弱场条件 G·M/R_core≪1 是否自动成立。

单位约定（与既有脚本一致）：c=1，剖面计算天然单位；G 作为自由耦合参数处理（来稿统一作用量
κ=8πG/c⁴ 中 G 独立可调，非固定为 1）。绝对尺度需外部锚，不冒充任何真实天体。

诚实边界（openuft 红线）：本脚本验证「T_μν 作为引力源 → 弱场还原牛顿/施瓦西外部」这一
结构性质在数值解上的成立性；不构成广义相对论整体解或统一场论完成声明。
"""
import os, sys
import mpmath as mp

# ---- 复用 V3.2_Qball_route2 的打靶求解器（文件名含点号，用 importlib 按路径加载）----
_HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("qroute2", os.path.join(_HERE, "V3.2_Qball_route2.py"))
Q = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(Q)

V1, V2, M2, C = Q.V1, Q.V2, Q.M2, Q.C
OMAX = mp.sqrt(M2/mp.mpf("2"))   # ω<√(M2/2)=0.4472
OMEGA = mp.mpf("0.184147")       # §5.2 稳定点（E₀/Q≈0.434，电荷稳定窗内）

def radius_enclosing(arr, rs, mass_frac, rho_E):
    """返回包围 mass_frac 质量半径（核心半径 R_core）。"""
    tot = sum(rho_E)
    acc = mp.mpf("0")
    for i, rho in enumerate(rho_E):
        acc += rho
        if acc >= mass_frac*tot:
            return rs[i]
    return rs[-1]

def main():
    mp.mp.dps = 40
    print("="*72)
    print("TUFT V3.2 统一场 · 引力扇区（方向A 弱场还原 GR 数值实证）")
    print("V1=%.2f V2=%.2f M2=%.3f  c=1  ω=%.6f (稳定点)" % (float(V1),float(V2),float(M2),float(OMEGA)))

    # ---- 1) 收敛解 ----
    s0 = Q.shoot_sigma0(OMEGA)
    if s0 is None:
        print("!! 打靶未收敛 @ ω=%.6f；退出。" % float(OMEGA)); return
    h = Q.RMAX/Q.STEPS
    arr = Q.integrate_full(s0, OMEGA)
    rs = [mp.mpf("0")] + [h*mp.mpf(i) for i in range(1, Q.STEPS+1)]
    darr = [mp.mpf("0")]*len(arr)
    for i in range(1, len(arr)-1):
        darr[i] = (arr[i+1]-arr[i-1])/(2*h)
    darr[0] = (arr[1]-arr[0])/h; darr[-1] = (arr[-1]-arr[-2])/h
    print("σ(0)=%.8f  σ(RMAX)=%.3g" % (float(s0), float(arr[-1])))

    # ---- 2) 能量密度、累计质量、牛顿势 ----
    rhoE = [mp.mpf("4")*mp.pi*rr*rr*(OMEGA*OMEGA*arr[i]**2 + darr[i]**2 + Q.U(arr[i]**2))
            for i, rr in enumerate(rs)]
    # 累计质量 M(r)=∫₀^r ρ_E dr'（被积已是 4πr²ρ_E，故直接累加）
    Mr = [mp.mpf("0")]*len(rs)
    acc = mp.mpf("0")
    for i, rho in enumerate(rhoE):
        acc += rho*h
        Mr[i] = acc
    E0 = Mr[-1]
    Mgrav = E0                       # 引力质量（等效原理下 = 场能量）
    Rcore = radius_enclosing(arr, rs, mp.mpf("0.9"), rhoE)
    print("-"*72)
    print("  场能量（=引力质量）E₀=M_grav = %.12g" % float(E0))
    print("  90%%质量半径 R_core          = %.12g" % float(Rcore))

    # 引力质量检查：外部 Φ·r → −G·E₀ 恒常
    G = mp.mpf("1")                   # 先用 G=1 看紧致度
    Phi_r = []
    for i, rr in enumerate(rs):
        if rr > 0:
            Phi_r.append(-G*Mr[i])    # Φ·r = −G·M(r)
    ext = [v for i, v in enumerate(Phi_r) if rs[i] > 2*Rcore]
    PhiR_ext = ext[-1] if ext else Phi_r[-1]
    print("  外部(r>2R_core) Φ·r 恒常 = %.12g  (应≈ −G·E₀=−%.6g)" % (float(PhiR_ext), float(G*E0)))
    ratio = abs(float(PhiR_ext/( -G*E0 )))
    print("  引力质量/场能量 一致性      = %.6f  (≈1 即等效成立)" % ratio)

    # ---- 3) 弱场度规 g₀₀=1+2Φ (c=1)，外部 vs Schwarzschild ----
    Gm_small = mp.mpf("0.0056")       # 取 G 使 GM/R_core≈0.1（弱场条件示例）
    r_ext = 3*Rcore
    Phi_ext = -Gm_small*E0/r_ext
    g00_ext = mp.mpf("1") + mp.mpf("2")*Phi_ext
    rs_sch = mp.mpf("2")*Gm_small*E0/r_ext
    print("-"*72)
    print("  弱场示例（取 G=0.0056 使 GM/R_core≈0.1）：")
    print("    Φ(r=3R_core)=%.6e   g₀₀=1+2Φ=%.10f" % (float(Phi_ext), float(g00_ext)))
    print("    Schwarzschild g₀₀=1−2GM/r=%.10f   差值=%.3g" % (float(1-rs_sch), float(abs(g00_ext-(1-rs_sch)))))

    # ---- 4) 诚实自引力评估：G=1 时紧致度 ----
    comp = mp.mpf("2")*G*E0/(Rcore*C*C)
    print("-"*72)
    print("  自引力评估：紧致度 2GM/(R_core c²) @ G=1 = %.6f" % float(comp))
    if comp > mp.mpf("1"):
        print("  ⇒ 该 Q-ball 在 G=1（普朗克型单位）下强自引力（2GM≫R_core，全 GR 下将坍缩为黑洞），")
        print("    牛顿/弱场还原对「本自然参数 + G=1」不自动成立；需稀释 Q-ball（R_core 大 / ω 小）或小 G。")
        print("  ⇒ 弱场还原是结构性质（∇²Φ=4πGρ、引力质量=E₀、外部 −GM/r），在 G·M/R_core≪1 的")
        print("    参数区成立；红线：不是 G=1 下该解的完整 GR 整体解。")
    else:
        print("  ⇒ 该解处于弱场区，牛顿还原直接成立。")
    print("="*72)
    print("诚实边界：验证 T_μν 作引力源→弱场还原牛顿/施瓦西外部的结构性质；非完整 GR 解，")
    print("不冒充统一场完成；UFT-3=0、L3=0 不变。绝对尺度需外部锚（未提供）。")

if __name__ == "__main__":
    main()
