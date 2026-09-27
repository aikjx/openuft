#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 路线2 · 时间谐振 Q-ball 打靶数值（mpmath 高精度，可运行版）
====================================================================
本脚本落地《16_TUFT_V3.2统一场攻坚_解析整理_2026-09-27.md》§3 的修正建议，
供方向 B（数值）第一步直接开跑。相对来稿代码的四项修正：

  1) 径向 ODE 补入时间谐振项（ω 项），不再求解已被 V3 审计判不存在的静态分支；
  2) 翻正六阶势符号（V3.2-1：eq(1)+action 六阶项为负 ⇒ 势能下无界，须翻正才是有界）；
  3) 补入质量项 ½M²|ψ|² —— 纯六阶（无质量）势时 σ(r) 尾部为 sin(ωr)/r 振荡、非指数
     衰减，∫σ²d³x 发散 ⇒ 无有限能量 Q-ball；加质量项后尾部指数衰减，Q-ball 才成立；
  4) 自写 RK4 高精度积分器（mpmath 无 `odefun`），能量密度含 ½ω²σ² 相位动能项。

单位约定：剖面计算取 c=1（天然单位，时间轴重标度，N/E₀/Q 与 c 无关）；M=E₀/c² 在 c=1
下即 M=E₀。恢复 SI 的绝对质量/电荷需额外尺度锚（本稿无），故输出为标度自由的数值，不冒充
电子质量/电荷。

诚实边界（openuft 红线）：本脚本验证「有下界六次势 + 质量项」的时间谐振 Q-ball 修复候选
的数值自洽性（存在有限能量孤子剖面、E₀ 收敛、稳定判据 E₀/Q<1），不是粒子身份或统一场论
完成的声明。

用法：  python V3.2_Qball_route2.py [dps]
默认 dps=60（可调；250 位较慢，同样可用）。
"""
import sys
import mpmath as mp

# ---------- 可调参数（TUFT V3.2 耦合常数 + 修复项） ----------
V1   = mp.mpf("1.2")     # 四次势系数（保持来稿值）
V2   = mp.mpf("0.4")     # 六次势系数（翻正符号后为有界项）
M2   = mp.mpf("0.4")     # 质量项系数 ½M²|ψ|²（修复新增；需满足 V1²>4·M2·V2）
C    = mp.mpf("1")       # 天然单位 c=1（见头注）
Q0C  = mp.mpf("1.0")     # 电荷耦合系数（来稿值）
RMAX = mp.mpf("14")      # 积分半径上限（质量项 1/m≈1.6，取 14 已 ≫ 孤子半径）
STEPS= 700               # 径向网格数（精度-速度折中；250 位大网格可在需要时加大）
SHOOT_IT= 45             # σ(0) 打靶二分迭代次数（≈2^-45 精度）

def U(w):
    """有下界六次势（修复版）：U(σ²)=½M2·w − (V1/4)w² + (V2/6)w³，w=σ²。
    有界性：w→∞ 时 +V2/6·w³>0 ⇒ 下界存在。"""
    return mp.mpf("0.5")*M2*w - (V1/mp.mpf("4"))*w**2 + (V2/mp.mpf("6"))*w**3

def dUdw(w):
    """dU/dw = ½M2 − (V1/2)w + (V2/2)w²。"""
    return mp.mpf("0.5")*M2 - (V1/mp.mpf("2"))*w + (V2/mp.mpf("2"))*w**2

def f(sigma, omega):
    """径向源项 f(σ)=[U'(σ²)−ω²]σ（c=1，ψ=σe^{-iωt}）。"""
    w = sigma**2
    return (dUdw(w) - omega*omega) * sigma

def rhs_dsigma(r, sigma, dsigma, omega):
    """σ'' = −(2/r)σ' + f(σ,ω)。r→0 用解析正则展开。"""
    if r <= mp.mpf("1e-24"):
        return f(sigma, omega)/mp.mpf("3")
    return -(mp.mpf("2")/r)*dsigma + f(sigma, omega)

def integrate_full(sigma0, omega):
    """RK4 从 r=0 积分 σ(r)（σ(0)=σ0, σ'(0)=0），返回 (网格数组, 网格半径数组)。"""
    h = RMAX/STEPS
    r = mp.mpf("0")
    s = sigma0
    ds = mp.mpf("0")
    # 首步用正则展开跨过 r=0：σ(h)≈σ0+(f(σ0)/6)h²，σ'(h)≈(f(σ0)/3)h
    f0 = f(sigma0, omega)
    s  = sigma0 + (f0/mp.mpf("6"))*h*h
    ds = (f0/mp.mpf("3"))*h
    r  = h
    arr = [sigma0, s]
    for _ in range(STEPS-1):
        k1d = rhs_dsigma(r, s, ds, omega)
        k2d = rhs_dsigma(r+h/mp.mpf("2"), s+(h/mp.mpf("2"))*ds, ds+(h/mp.mpf("2"))*k1d, omega)
        k3d = rhs_dsigma(r+h/mp.mpf("2"), s+(h/mp.mpf("2"))*(ds+(h/mp.mpf("2"))*k1d), ds+(h/mp.mpf("2"))*k2d, omega)
        k4d = rhs_dsigma(r+h, s+h*(ds+(h/mp.mpf("2"))*k2d), ds+h*k3d, omega)
        ds += (h/mp.mpf("6"))*(k1d + mp.mpf("2")*k2d + mp.mpf("2")*k3d + k4d)
        s  += h*ds
        r  += h
        arr.append(s)
    return arr

def end_value(sigma0, omega):
    """打靶目标：σ(RMAX)。"""
    arr = integrate_full(sigma0, omega)
    return arr[-1]

def shoot_sigma0(omega):
    """对给定 ω 打靶 σ(0) 使 σ(RMAX)→0（局部 Q-ball 解）。
    先向上扫描 σ0 找首个 end<0（+→− 符号变化，位于假真空平台值 σ₊ 附近），
    再在窄括号内二分驱动 end→0。返回 σ0 或 None。"""
    def end(s0):
        return end_value(s0, omega)
    # 1) 粗扫描找首个 end<0
    step = mp.mpf("0.05"); s0 = mp.mpf("0.05"); s0max = mp.mpf("3.0")
    s_prev, e_prev = s0, end(s0)
    lo = hi = None
    while s0 < s0max:
        e = end(s0)
        if e < 0:
            lo, hi = s_prev, s0
            break
        s_prev, e_prev = s0, e
        s0 += step
    if lo is None:
        return None
    # 2) 窄括号二分：end(lo)>0(或已≤0)、end(hi)<0
    flo = end(lo)
    fhi = end(hi)
    if flo*fhi > 0 and flo > 0:
        # 若 lo 端已进入负区，向回退一步
        lo -= step; flo = end(lo)
        if flo*fhi > 0:
            return None
    for _ in range(SHOOT_IT):
        mid = (lo+hi)/2
        fm = end(mid)
        if flo*fm <= 0:
            hi = mid; fhi = fm
        else:
            lo = mid; flo = fm
    return (lo+hi)/2

def simpson_int(fvals, h):
    """复合 Simpson 积分（fvals 长度=STEPS+1，等距 h）。"""
    n = len(fvals)-1
    if n % 2 == 1:
        n -= 1  # 取偶
    s = fvals[0] + fvals[n]
    for i in range(1, n, 2):
        s += mp.mpf("4")*fvals[i]
    for i in range(2, n-1, 2):
        s += mp.mpf("2")*fvals[i]
    return s*h/mp.mpf("3")

def compute_profile(omega, sigma0):
    """收敛剖面网格 → N、Q、E₀、M、E₀/Q。"""
    h = RMAX/STEPS
    arr = integrate_full(sigma0, omega)
    # 半径网格
    rs = [mp.mpf("0")] + [h*mp.mpf(i) for i in range(1, STEPS+1)]
    # σ' 用中心差分（首/尾用单边）
    darr = [mp.mpf("0")]*len(arr)
    for i in range(1, len(arr)-1):
        darr[i] = (arr[i+1]-arr[i-1])/(2*h)
    darr[0] = (arr[1]-arr[0])/h
    darr[-1] = (arr[-1]-arr[-2])/h
    # N = ∫4πr²σ²dr
    fN = [mp.mpf("4")*mp.pi*rr*rr*arr[i]**2 for i, rr in enumerate(rs)]
    N = simpson_int(fN, h)
    # E₀ = ∫4πr²[ω²σ² + σ'² + U(σ²)]dr   （规范能量密度 T⁰⁰=|φ̇|²+|∇φ|²+W）
    fE = []
    for i, rr in enumerate(rs):
        w = arr[i]**2
        fE.append(mp.mpf("4")*mp.pi*rr*rr*(omega*omega*w + darr[i]**2 + U(w)))
    E0 = simpson_int(fE, h)
    Q = mp.mpf("2")*omega*N
    M = E0/(C*C)
    # 剖面 CSV 落盘（与 V3_Qball_profile.csv 体例一致）
    try:
        import os
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "V3.2_Qball_profile.csv")
        with open(base, "w", encoding="utf-8") as fh:
            fh.write("r,sigma\n")
            for i, rr in enumerate(rs):
                fh.write("%s,%s\n" % (mp.nstr(rr, 16), mp.nstr(arr[i], 16)))
    except Exception as e:
        print("  (profile CSV 写入跳过: %s)" % e)
    return N, Q, E0, M, arr

def main():
    dps = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    mp.mp.dps = dps
    print("="*72)
    print("TUFT V3.2 路线2 · 时间谐振 Q-ball 打靶  (mpmath dps=%d)" % dps)
    print("V1=%.2f  V2=%.2f  M2=%.3f  RMAX=%s  STEPS=%d" % (float(V1),float(V2),float(M2),RMAX,STEPS))
    cond = V1**2 - mp.mpf("4")*M2*V2
    print("假真空条件 V1²−4·M2·V2 = %.6f  (>0 才支持 Q-ball)" % float(cond))
    if cond <= 0:
        print("!! 不满足假真空条件；请增大 V1 或减小 M2。退出。")
        return
    omax = mp.sqrt(M2/mp.mpf("2"))   # ω²<U'(0)=½M2 ⇒ ω<√(M2/2)
    print("ω 上界（质量阈值）ω<√(M2/2)=%.6f" % float(omax))

    found = False
    for k in range(1, 10):
        omega = omax*mp.mpf(k)/mp.mpf("10")
        s0 = shoot_sigma0(omega)
        if s0 is not None:
            N, Q, E0, M, arr = compute_profile(omega, s0)
            print("-"*72)
            print("收敛 Q-ball @ ω=%.8f   σ(0)=%.8f   σ(RMAX)=%.3g"
                  % (float(omega), float(s0), float(arr[-1])))
            print("  电荷荷量 N=∫σ²d³x        = %.12g" % float(N))
            print("  物理电荷 Q=2ωN            = %.12g" % float(Q))
            print("  能量 E₀                  = %.12g" % float(E0))
            print("  M=E₀/c² (c=1)            = %.12g" % float(M))
            print("  稳定判据 E₀/Q            = %.12g  (<1 则荷守恒下稳定)" % float(E0/Q))
            # 尾部落差检查（指数衰减证据）
            print("  尾部(σ(3RMAX/4)/σ(0))     = %.3g  (≪1 即局部化)" % float(arr[3*STEPS//4]/s0))
            found = True
            break
    if not found:
        print("!! 扫描 ω 段未找到收敛局部解；需调整参数或 ω 网格。")
        return
    print("="*72)
    print("诚实边界：本结果验证「有下界六次势 + 质量项」修复候选的数值自洽性。")
    print("绝对质量/电荷需尺度锚（未提供），不冒充电子质量/电荷；统一场完成度不受影响。")

if __name__ == "__main__":
    main()
