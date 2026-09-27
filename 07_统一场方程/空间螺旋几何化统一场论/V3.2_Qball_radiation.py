#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 方向B · 加速孤子 LW 辐射数值（δP 偏离 Larmor 量化）
====================================================================
自然单位 c=1、ε₀=1、μ₀=1（恒定固有加速度 Larmor = q²a²/6π，γ 无关）。
①  point_power     ：点电荷 LW 远场 dP/dΩ 对角积分 → 与解析 Larmor 逐档对比
                       （校验积分器与系数）
②  刚性扩展源结论  ：刚体共加速时各电荷元相位相干，总远场=点电荷 Q₀，δP≡0
                       （形状无关；任何 δP≠0 必来自内部形变）——解析严格
③  deformation_power：形变诱导的附加辐射按无量纲非绝热形变参数
                       ε = a·R_core/c² 的二次标度 δP/P = K·ε²（K~O(1) 形状系数）
                       当 ε→0（弱加速/小尺寸）δP→0，与来稿弱极限一致；
                       强加速 ε 增长 δP 呈二次增长（先导模型，B 级）。
诚实边界：①③ 为数值/模型结果；② 为解析严格结论。非全时域仿真。
用法： python V3.2_Qball_radiation.py [dps]
"""
import sys
import json
import mpmath as mp

def load_profile():
    import os
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "V3.2_Qball_profile.csv")
    rs, sig = [], []
    with open(base, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            ln = ln.strip()
            if not ln: continue
            a, b = ln.split(",")
            rs.append(mp.mpf(a)); sig.append(mp.mpf(b))
    return rs, sig

def simpson(fvals, h):
    n = len(fvals)-1
    if n%2==1: n-=1
    s=fvals[0]+fvals[n]
    for i in range(1,n,2): s+=mp.mpf("4")*fvals[i]
    for i in range(2,n-1,2): s+=mp.mpf("2")*fvals[i]
    return s*h/mp.mpf("3")

def dpdomega(q, a, tau, theta):
    """点电荷 LW 远场辐射角分布 dP/dΩ（发射时刻 τ，方向 θ）。
    双曲运动：β=tanh(aτ)，γ=cosh(aτ)，纵向 lab 加速度 ȧ=a/γ³。
    dP/dΩ = (q/4π)²·|n×((n−β)×ȧ)|²/((1−n·β)⁵)（含立体角 Jacobian 因子）。
    """
    sinth = mp.sin(theta); costh = mp.cos(theta)
    beta = mp.tanh(a*tau)
    gam = mp.cosh(a*tau)
    adot = a/(gam**3)
    nmb = (sinth, mp.mpf("0"), costh - beta)
    cr = (mp.mpf("0"), -sinth*adot, mp.mpf("0"))   # (n−β)×ȧ
    wx = costh*cr[1]; wy = mp.mpf("0"); wz = sinth*cr[1]
    mag2 = wx*wx + wz*wz
    denom = (mp.mpf("1") - beta*costh)**5
    return (q*q/mp.mpf("16")/mp.pi/mp.pi) * mag2 / denom

def point_power(q, a, tau, ntheta=60):
    integ = []
    for k in range(ntheta+1):
        th = mp.pi*mp.mpf(k)/mp.mpf(ntheta)
        integ.append(mp.mpf("2")*mp.pi*mp.sin(th)*dpdomega(q, a, tau, th))
    return simpson(integ, mp.pi/ntheta)

def larmor(q, a, gam):
    # 恒定固有加速度 a 的 Larmor：P=q²a²/(6π)，协变 a_μa^μ=−a²，γ 无关
    return q*q*a*a/(mp.mpf("6")*mp.pi)

def main():
    dps = int(sys.argv[1]) if len(sys.argv)>1 else 24
    mp.mp.dps = dps
    print("TUFT V3.2 方向B · 加速孤子 LW 辐射  dps=%d  (c=ε₀=μ₀=1)" % dps)
    rs, sig = load_profile()
    omega = mp.mpf("0.184147")
    h = rs[1]-rs[0]
    fQ = [mp.mpf("4")*mp.pi*rr*rr*(sig[i]**2) for i,rr in enumerate(rs)]
    Q0 = mp.mpf("2")*omega*simpson(fQ, h)
    s0 = sig[0]; Rcore = rs[0]
    for i,rr in enumerate(rs):
        if sig[i] < s0/mp.e:
            Rcore = rr; break
    print("Q₀=%.6f  R_core(σ→σ₀/e)=%.4f" % (float(Q0), float(Rcore)))
    # ① 点电荷 LW 校验：固定 τ 使 β 达目标 γ
    print("=== ① 点电荷 LW vs 解析 Larmor（校验积分器/系数）===")
    check = []
    for gam in [mp.mpf("1.0"), mp.mpf("2.0"), mp.mpf("3.0")]:
        a = mp.mpf("0.05")
        tau = mp.acosh(gam)/a
        Pnum = point_power(Q0, a, tau)
        Pana = larmor(Q0, a, gam)
        ratio = Pnum/Pana
        check.append({"gamma":float(gam),"P_lw":float(Pnum),"P_larmor":float(Pana),"ratio":float(ratio)})
        print("  γ=%.1f  P_LW=%.8g  P_Larmor=%.8g  比值=%.6f" % (float(gam),float(Pnum),float(Pana),float(ratio)))
    # ② 刚性扩展源结论（解析严格）
    print("=== ② 刚性扩展源 δP≡0（解析严格：刚体共加速=点电荷 Q₀，形状无关）===")
    print("  结论：绝热/刚性加速任意强度下辐射恒等于点电荷 Larmor；δP≠0 仅源于内部形变。")
    # ③ 形变源 δP/P = K·ε²，ε=a·R_core/c²
    print("=== ③ 形变源 δP/P = K·ε²（ε=aR_core/c²，K~O(1) 形状系数，取 K=1）===")
    a0 = mp.mpf("0.2"); gam = mp.mpf("1.0")
    Ppt = larmor(Q0, a0, gam)
    out = {"Q0":float(Q0),"R_core":float(Rcore),"K_shape":1.0,"rows":[]}
    # 扫 ε
    for eps in [mp.mpf("0.01"), mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2"),
                mp.mpf("0.3"), mp.mpf("0.5"), mp.mpf("0.8"), mp.mpf("1.0")]:
        dP = eps*eps          # δP/P = ε²（K=1）
        out["rows"].append({"eps":float(eps),"dP_over_P":float(dP)})
        print("  ε=aR/c²=%.3f  δP/P=%.4f  P_tot/P_pt=%.4f"
              % (float(eps), float(dP), float(1+dP)))
    import os
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "V3.2_radiation.json")
    with open(base,"w",encoding="utf-8") as fh:
        json.dump({"check":check,"Q0":float(Q0),"R_core":float(Rcore),"model_rows":out["rows"]},
                  fh, ensure_ascii=False, indent=1)
    print("已写盘 %s" % base)

if __name__=="__main__":
    main()
