#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 统一场论攻坚 · 强自引力区：Q-ball 的玻色星身份与坍缩判定（2026-10-07）
==========================================================================
识别：G≠0 下时间谐振 Q-ball（ψ=σe^{-iωt}）即标准玻色星（oscillating scalar soliton）。
本脚本用已收敛解实算引力自束缚能，并与玻色星最大质量界 M_max≈0.633·M_Pl²/m 对照，
定量判定 TUFT Q-ball 处于稳定支还是坍缩（黑洞）支。

量：c=1，G 作为可调耦合；M_Pl²=1/G。玻色星通用最大质量界（Schunck & Mielke 综述）：
  M_max ≈ 0.633·M_Pl²/m = 0.633/(G·m)，m=√(M2/2) 为标量场质量。
牛顿自引力束缚能（球对称、静电式自能）：
  E_grav = -(G/2)·∫₀^∞ [M(r)/r]·(4πr²ρ_E) dr，Φ=-G·M(r)/r。
绑定分数 |E_grav|/E₀ ≈ (1/2)·GM/(R c²)·(形状因子) 反映自引力强度。

诚实边界：本脚本给出玻色星最大质量界基准 + 实算束缚能的坍缩判定，是把 TUFT Q-ball
锚到已确立玻色星物理的第一步；不构造完整 Einstein-Klein-Gordon 整体解，不改变
UFT-3=0、L3=0。绝对尺度需外部锚。
"""
import os
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location as sffl

H = os.path.dirname(os.path.abspath(__file__))
_spec = sffl("qroute2", os.path.join(H, "V3.2_Qball_route2.py"))
Q = module_from_spec(_spec); _spec.loader.exec_module(Q)

V1, V2, M2 = Q.V1, Q.V2, Q.M2
OMEGA = mp.mpf("0.184147")   # 稳定点（§5.2）
mp.mp.dps = 40

def compute():
    s0 = Q.shoot_sigma0(OMEGA)
    if s0 is None:
        raise SystemExit("打靶未收敛")
    h = Q.RMAX / Q.STEPS
    arr = Q.integrate_full(s0, OMEGA)
    rs = [mp.mpf("0")] + [h * mp.mpf(i) for i in range(1, Q.STEPS + 1)]
    d = [mp.mpf("0")] * len(arr)
    for i in range(1, len(arr) - 1):
        d[i] = (arr[i + 1] - arr[i - 1]) / (2 * h)
    d[0] = (arr[1] - arr[0]) / h; d[-1] = (arr[-1] - arr[-2]) / h
    rhoE = [mp.mpf("4") * mp.pi * rr * rr * (OMEGA * OMEGA * a * a + dd * dd + Q.U(a * a))
            for rr, a, dd in zip(rs, arr, d)]
    Mr = [mp.mpf("0")] * len(rs); acc = mp.mpf("0")
    for i, rho in enumerate(rhoE):
        acc += rho * h; Mr[i] = acc
    return rs, rhoE, Mr, s0, arr

def simpson(fvals, h):
    n = len(fvals) - 1
    if n % 2 == 1: n -= 1
    s = fvals[0] + fvals[n]
    for i in range(1, n, 2): s += mp.mpf("4") * fvals[i]
    for i in range(2, n - 1, 2): s += mp.mpf("2") * fvals[i]
    return s * h / mp.mpf("3")

def main():
    rs, rhoE, Mr, s0, arr = compute()
    h = Q.RMAX / Q.STEPS
    E0 = Mr[-1]
    # 90% 质量半径
    tot = sum(rhoE); acc = mp.mpf("0"); Rcore = rs[-1]
    for i, rho in enumerate(rhoE):
        acc += rho
        if acc >= mp.mpf("0.9") * tot:
            Rcore = rs[i]; break
    m_scalar = mp.sqrt(M2 / mp.mpf("2"))
    print("=" * 72)
    print("TUFT V3.2 · 强自引力区：Q-ball 的玻色星身份与坍缩判定")
    print("ω=%.6f（稳定点） σ(0)=%.6f  E₀=%.6f  R_core(90%%质量)=%.6f  m=√(M2/2)=%.6f"
          % (float(OMEGA), float(s0), float(E0), float(Rcore), float(m_scalar)))
    for G in (mp.mpf("1"), mp.mpf("0.0056")):
        # 引力自束缚能 E_grav = -(G/2)∫ (M(r)/r)·(4πr²ρ_E) dr
        fint = [-(G / mp.mpf("2")) * (Mr[i] / rs[i]) * rhoE[i] for i in range(1, len(rs))]
        Egrav = simpson(fint, h)  # 注意 rs[0]=0 处被积 0/0→0，跳过
        comp = mp.mpf("2") * G * E0 / (Rcore)
        bind = abs(Egrav) / E0
        # 玻色星最大质量界 M_max=0.633·M_Pl²/m=0.633/(G·m)
        Mmax = mp.mpf("0.633") / (G * m_scalar)
        ratio = E0 / Mmax
        print("-" * 72)
        print("G=%.4g： E_grav=%.6g  绑定分数|E_grav|/E₀=%.4g  紧致度2GM/R=%.4g"
              % (float(G), float(Egrav), float(bind), float(comp)))
        print("  玻色星最大质量 M_max=0.633M_Pl²/m=%.6g   M/M_max=%.4g"
              % (float(Mmax), float(ratio)))
        if ratio > 1:
            print("  ⇒ M≫M_max（超最大质量界 %g 倍）：Q-ball 处于不稳定/坍缩支（G 下会坍缩为黑洞）"
                  % float(ratio))
        else:
            print("  ⇒ M<M_max：可存在稳定玻色星（自引力束缚标量星）")
    print("=" * 72)
    print("结论：G≠0 下 TUFT Q-ball = 玻色星；G=1（普朗克型单位）下超最大质量界→坍缩支；")
    print("稳定玻色星（暗物质候选）需小 G 或稀释（ω 小/R_core 大）参数区。")
    print("诚实边界：玻色星最大质量界为已确立文献结果（Schunck & Mielke）；本脚本用实算")
    print("束缚能+质量界基准做坍缩判定，非完整 Einstein-Klein-Gordon 整体解；UFT-3=0、L3=0 不变。")

if __name__ == "__main__":
    main()
