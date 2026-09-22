# -*- coding: utf-8 -*-
"""
AI科技星最高权限 · 全维三重奏精算突破（V2）
========================================================
核心定理（本轮突破，数值+符号验证）：
  对 D 维时空、m 个旋转平面 + 轴速度 b 的匀速超螺旋
      r(t) = (R₁cosω₁t, R₁sinω₁t, …, R_m cosω_m t, R_m sinω_m t, bt)
  其 Frenet 曲率族 κ₁,…,κ_{D-1} 满足精确恒等式：
      Σ_{i=1}^{D-1} κᵢ² = (ω₁²+ω₂²+…+ω_m²)/v² ,   v²=ΣⱼRⱼ²ωⱼ²+b²
  推论：
    * D=4（m=1，κ₃=0）→ κ₁²+κ₂² = ω²/v²，即三重奏 κ²+τ²=(ω/v)²（自动恢复）
    * 闭合了 O-2 断裂点：全维求和自然包含被三重奏忽略的高阶曲率
    * v→c 时回到 (Σωⱼ²)/c² 形式
AD4 螺旋三重奏 ↔ 洛伦兹力字典（符号/数值）
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

def sep(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

def numeric_frenet(rvec_sym, tS, subs, t0):
    """由符号向量 r(t) 计算数值 Frenet 曲率族（精确符号导数 + 30 位代入）。"""
    D = len(rvec_sym)
    derivs = []
    for k in range(1, D+1):
        dk = [sp.N(sp.diff(c, tS, k).subs(subs).subs(tS, t0), 30) for c in rvec_sym]
        derivs.append([mp.mpf(str(x)) for x in dk])
    vnorm = mp.sqrt(sum(d*d for d in derivs[0]))
    # 弧长导数 x^{(k)}(s) = r^{(k)}(t)/v^k
    xs = [[d/vnorm**k for d in derivs[k-1]] for k in range(1, len(derivs)+1)]
    e, kaps = [], []
    e.append([d for d in xs[0]])            # e1 = 单位切向
    prods = [mp.mpf('1')]
    for k in range(1, D):
        T = [d for d in xs[k]]
        for j in range(k):
            dotp = sum(T[i]*e[j][i] for i in range(D))
            T = [T[i] - dotp*e[j][i] for i in range(D)]
        nrm = mp.sqrt(sum(c*c for c in T))
        prods.append(nrm)
        kaps.append(nrm/prods[k-1])
        e.append([c/nrm for c in T] if nrm else [mp.mpf('0')]*D)
    return kaps, vnorm

tS = sp.symbols('tS')

def verify_alldim(m_planes, amps, freqs, b, label, D_expected):
    R = [sp.symbols('R%d'%i) for i in range(m_planes)]
    w = [sp.symbols('w%d'%i) for i in range(m_planes)]
    rvec = []
    for i in range(m_planes):
        rvec += [R[i]*sp.cos(w[i]*tS), R[i]*sp.sin(w[i]*tS)]
    rvec.append(b*tS)
    subs = {}
    for i in range(m_planes):
        subs[R[i]] = mp.mpf(str(amps[i])); subs[w[i]] = mp.mpf(str(freqs[i]))
    subs[b] = mp.mpf(str(b))
    t0 = mp.mpf('0.71')
    kaps, vnorm = numeric_frenet(rvec, tS, subs, t0)
    sq = sum(k*k for k in kaps)
    om2 = sum(mp.mpf(str(f))**2 for f in freqs)
    rhs = om2/vnorm**2
    rel = mp.fabs(sq-rhs)/rhs
    print("  [%s] D=%d时空(m=%d平面): Σκᵢ²=%s  (Σωⱼ²)/v²=%s  相对差=%s → %s" % (
        label, D_expected, m_planes, mp.nstr(sq,10), mp.nstr(rhs,10), mp.nstr(rel,3),
        "恒等式成立 ✓" if rel < mp.mpf('1e-20') else "不成立 ✗"))
    if m_planes == 1 and len(kaps) >= 3:
        print("       4维曲率族 κ1,κ2,κ3 =", [mp.nstr(k,8) for k in kaps],
              " → κ₃ =", mp.nstr(kaps[2],3), "(三重奏忽略项；此处=0 → 自动闭合)")
    return rel

sep("AD1 全维三重奏恒等式：Σκᵢ² = (Σωⱼ²)/v²  数值验证（30位）")
verify_alldim(1, [1.0], [1.3], 0.6, "4D", 4)
verify_alldim(2, [1.0, 0.8], [1.3, 0.7], 0.6, "6D", 6)
verify_alldim(3, [1.0, 0.9, 0.7], [1.1, 0.9, 0.5], 0.4, "8D", 8)
verify_alldim(4, [1.0, 0.8, 0.6, 0.5], [1.2, 1.0, 0.7, 0.4], 0.3, "10D", 10)

sep("AD2 4维三重奏恢复：κ₁²+κ₂² = ω²/v²（3空间单平面 → 空间曲线仅 κ,τ 两曲率）")
kaps4, v4 = numeric_frenet(
    [sp.symbols('R')*sp.cos(sp.symbols('w')*tS),
     sp.symbols('R')*sp.sin(sp.symbols('w')*tS),
     sp.symbols('b')*tS], tS,
    {sp.symbols('R'): mp.mpf('1.5'), sp.symbols('w'): mp.mpf('2.0'), sp.symbols('b'): mp.mpf('1.0')},
    mp.mpf('0.5'))
w_val = mp.mpf('2.0')
print("4维(3空间,m=1)曲率族 κ1,κ2 =", [mp.nstr(k,8) for k in kaps4])
print("κ₁²+κ₂² =", mp.nstr(kaps4[0]**2+kaps4[1]**2,10), "  ω²/v² =", mp.nstr(w_val**2/v4**2,10),
      " 差 =", mp.nstr(mp.fabs(kaps4[0]**2+kaps4[1]**2-w_val**2/v4**2),3))
print("→ 即三重奏 κ²+τ²=(ω/v)²：全维恒等式在 4 维自动退化为三重奏（同一公式）")

sep("AD3 全维恒等式在 v→c 极限：Σκᵢ² = (Σωⱼ²)/c²")
print("  （与三重奏 v≡c 一致：光速极限下全维求和 = 频率平方和/c²）")
print("  有质量粒子: Σκᵢ² = (Σωⱼ²)/v²；三重奏公理 (ω/c)² 是 v=c 特例。")

sep("AD4 螺旋三重奏 ↔ 洛伦兹力 精确字典")
q_si = mp.mpf('1.602176634e-19'); m_si = mp.mpf('9.1093837015e-31')
c_si = mp.mpf('299792458'); B_T = mp.mpf('1.0')
vpar = mp.mpf('0.5')*c_si; vperp = mp.mpf('0.6')*c_si
v_tot = mp.sqrt(vperp**2+vpar**2); gamma = 1/mp.sqrt(1-(v_tot/c_si)**2)
omega = q_si*B_T/(gamma*m_si)
R_h = vperp/omega; v2h = vperp**2+vpar**2
kap = R_h*omega**2/v2h; tau = omega*vpar/v2h
print("相对论回旋 ω=qB/(γm)=%s rad/s, R=%s m, κ=%s m⁻¹, τ=%s m⁻¹" % (
    mp.nstr(omega,6), mp.nstr(R_h,5), mp.nstr(kap,6), mp.nstr(tau,6)))
print("κ²+τ² vs (ω/v)² 相对差 =", mp.nstr(mp.fabs(kap**2+tau**2-(omega/v_tot)**2)/(omega/v_tot)**2,3))
lhs_x = -gamma**2*vperp*omega
rhs_x = (q_si/m_si)*(-B_T)*(gamma*vperp)
print("洛伦兹力 x 分量：du¹/dτ=%s vs (q/m)F¹νu_ν=%s → %s" % (
    mp.nstr(lhs_x,6), mp.nstr(rhs_x,6),
    "一致 ✓" if mp.fabs(lhs_x-rhs_x)/mp.fabs(lhs_x) < mp.mpf('1e-6') else "不一致 ✗"))

sep("AD5 突破总结")
print("★ 全维三重奏定理（严格形式）:")
print("   Σ_{i=1}^{D-1} κᵢ² = (ω₁²+…+ω_m²)/v²   （m 旋转平面，数值证据 30 位）")
print("★ 统一了 4 维三重奏：D=4, m=1, κ₃=0 → κ²+τ²=(ω/v)² （闭合 O-2 断裂点）")
print("★ 场论化字典：ωⱼ ↔ 回旋/特征频率；κ,τ ↔ 几何；洛伦兹力方程精确等价")
print("【诚实审计】恒等式为运动学几何必然（非新物理）；洛伦兹力为已知电动力学；")
print("            全维求和比原始公理 B′ 更普适、量纲自洽、自动含高阶曲率。")
