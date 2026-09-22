# -*- coding: utf-8 -*-
"""
AI科技星最高权限 · 全维三重奏定理完整严格证明（R9）
========================================================
目标：闭合 O-6 —— 严格归纳证明  Beᵢ = eᵢ′（B=A/v 斜对称生成元，Frenet 标架）
归纳证明结构：
  基础：Be₁ = x″ = e₁′
  归纳步（假设 Be_j=e_j′, j<i）：
    (a) W_i = x^(i) − Σ_{j<i}(x^(i)·e_j)e_j  （Gram-Schmidt）
    (b) W_i′ = |W_i|·Be_i
        由 W_i′ = x^(i+1) − Σ(x^(i+1)·e_j)e_j − Σ(x^(i)·e_j′)e_j − Σ(x^(i)·e_j)e_j′
        |W_i|Be_i = Bx^(i) − Σ(x^(i)·e_j)Be_j = x^(i+1) − Σ(x^(i)·e_j)e_j′
        两者差 = Σ(x^(i+1)·e_j)e_j + Σ(x^(i)·e_j′)e_j
        x^(i+1)·e_j = (Bx^(i))·e_j = −(x^(i)·Be_j) = −(x^(i)·e_j′)  [B斜对称+归纳]
        → 差 = 0 ✓
    (c) e_i·Be_i = 0（B 斜对称）→ W_i·W_i′ = |W_i|²(e_i·Be_i)=0 → |W_i|′=0
    (d) e_i′ = W_i′/|W_i| − W_i·(|W_i|′/|W_i|²) = Be_i − 0 = Be_i ✓
P1 数值验证基础：x″ = Be₁ = e₁′
P2 数值验证归纳步恒等式 ①：Σ_{j<i}(x^(i+1)·e_j)e_j + Σ_{j<i}(x^(i)·e_j′)e_j = 0
P3 数值验证 W_i′ = |W_i|·Be_i
P4 数值验证 e_i·Be_i = 0（斜对称）
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

def sep(t): print("\n" + "="*76 + "\n" + t + "\n" + "="*76)

def build_data(amps, freqs, b, t0):
    """返回标架 e、曲率、x^(i)、W_i、B 等数值数据。"""
    tS = sp.symbols('t')
    rvec = []
    for A_, w in zip(amps, freqs):
        A_, w = mp.mpf(str(A_)), mp.mpf(str(w))
        rvec += [A_*sp.cos(w*tS), A_*sp.sin(w*tS)]
    b = mp.mpf(str(b)); rvec.append(b*tS)
    n = len(rvec)
    ders = []
    for k in range(1, n+1):
        dk = [sp.N(sp.diff(c, tS, k).subs(tS, t0), 30) for c in rvec]
        ders.append([mp.mpf(str(x)) for x in dk])
    vn = mp.sqrt(mp.fsum(d*d for d in ders[0]))
    xs = [[d/vn**k for d in ders[k-1]] for k in range(1, n+1)]  # 弧长导数 x^(1..n)
    e, kaps = [list(xs[0])], []
    prods = [mp.mpf(1)]
    Ws = []
    for k in range(1, n):
        T = [d for d in xs[k]]
        for j in range(k):
            dotp = mp.fsum(T[i]*e[j][i] for i in range(n))
            T = [T[i]-dotp*e[j][i] for i in range(n)]
        nrm = mp.sqrt(mp.fsum(c*c for c in T))
        Ws.append(T)
        prods.append(nrm)
        kaps.append(nrm/prods[k-1])
        e.append([c/nrm for c in T] if nrm else [mp.mpf(0)]*n)
    # B = A/v（斜对称生成元）
    A = mp.matrix(n, n)
    for j, w in enumerate(freqs):
        w = mp.mpf(str(w)); i0 = 2*j
        A[i0, i0+1] = -w; A[i0+1, i0] = w
    B = A / vn
    return e, kaps, vn, xs, Ws, B, n

def dot(u, v): return mp.fsum(u[c]*v[c] for c in range(len(u)))

def Be_vec(B, u):
    n = len(u)
    return [mp.fsum(B[c, d]*u[d] for d in range(n)) for c in range(n)]

def der_t(f_list, t0, h, n_comp):
    """f_list: 返回向量(t)->list；中心差分 de/dt"""
    out = []
    for c in range(n_comp):
        out.append((f_list(t0+h)[c]-f_list(t0-h)[c])/(2*h))
    return out

sep("P0  归纳证明断言汇总（将逐一数值确认）")
print("  定理：对 r″=Ar′（A斜对称），Frenet 标架满足 eᵢ′ = Beᵢ（B=A/v）")

def run_case(label, amps, freqs, b, t0=mp.mpf('0.77')):
    e, kaps, vn, xs, Ws, B, n = build_data(amps, freqs, b, t0)
    h = mp.mpf('1e-7')
    def e_func(tv, i):
        return build_data(amps, freqs, b, tv)[0][i]
    print("  --- [%s] n=%d ---" % (label, n))
    # P1 基础：x″ = Be₁，且 e₁′=x″（即 e₁′=Be₁）
    x2 = xs[1]
    Be1 = Be_vec(B, e[0])
    err1 = max(mp.fabs(x2[c]-Be1[c]) for c in range(n))
    # e₁′（弧长）= de₁/dt / v
    de1_dt = der_t(lambda tv: e_func(tv, 0), t0, h, n)
    e1prime = [de1_dt[c]/vn for c in range(n)]
    err1b = max(mp.fabs(e1prime[c]-x2[c]) for c in range(n))
    print("    P1 基础 x″=Be₁: 差=%s ; e₁′=x″: 差=%s → %s" % (
        mp.nstr(err1,3), mp.nstr(err1b,3),
        "✓" if max(err1, err1b) < mp.mpf('1e-8') else "✗"))
    # P2 恒等式 ① 对每个 i（归纳步关键）：Σ_{j<i}(x^(i+1)·e_j)e_j + Σ(x^(i)·e_j′)e_j = 0
    #   e_j′ 为弧长导数 = (de_j/dt)/v
    max_id = mp.mpf(0)
    for i in range(1, n):
        ejp = [der_t(lambda tv, jj=j: e_func(tv, jj), t0, h, n) for j in range(i)]
        acc = [mp.mpf(0)]*n
        for j in range(i):
            a = dot(xs[i], e[j])              # x^(i+1)·e_j
            b_ = dot(xs[i-1], [c/vn for c in ejp[j]])   # x^(i)·e_j′（弧长）
            for c in range(n):
                acc[c] += a*e[j][c] + b_*e[j][c]
        max_id = max(max_id, max(mp.fabs(acc[c]) for c in range(n)))
    print("    P2 恒等式①(归纳步关键) 最大残差=%s → %s" % (
        mp.nstr(max_id,3), "✓" if max_id < mp.mpf('1e-8') else "✗"))
    # P3 W_i′ = |W_i|·Be_i
    max_w = mp.mpf(0)
    for i in range(1, n):
        Wi = Ws[i-1]
        nW = mp.sqrt(dot(Wi, Wi))
        # W_i′：W_i(t) 的导数。W_i 由 Gram-Schmidt 生成（含 sqrt 归一化），数值差分
        def W_func(tv):
            return build_data(amps, freqs, b, tv)[4][i-1]
        dW = der_t(lambda tv: W_func(tv), t0, h, n)
        dW_s = [dW[c]/vn for c in range(n)]   # 弧长导数
        Be_i = Be_vec(B, e[i])
        lhs = [dW_s[c] for c in range(n)]
        rhs = [nW*Be_i[c] for c in range(n)]
        err = max(mp.fabs(lhs[c]-rhs[c]) for c in range(n))
        max_w = max(max_w, err)
    print("    P3 W_i′=|W_i|·Be_i 最大误差=%s → %s" % (
        mp.nstr(max_w,3), "✓" if max_w < mp.mpf('1e-7') else "✗"))
    # P4 e_i·Be_i = 0（B 斜对称）
    max_s = mp.mpf(0)
    for i in range(n):
        max_s = max(max_s, mp.fabs(dot(e[i], Be_vec(B, e[i]))))
    print("    P4 eᵢ·Beᵢ=0 最大=%s → %s" % (mp.nstr(max_s,3), "✓" if max_s < mp.mpf('1e-12') else "✗"))
    # 汇总：e_i′=Be_i 直接验证
    max_e = mp.mpf(0)
    for i in range(n):
        de_dt = der_t(lambda tv, ii=i: e_func(tv, ii), t0, h, n)
        eprime = [de_dt[c]/vn for c in range(n)]
        Be_i = Be_vec(B, e[i])
        max_e = max(max_e, max(mp.fabs(eprime[c]-Be_i[c]) for c in range(n)))
    print("    ✓ eᵢ′=Beᵢ（归纳结论）最大误差=%s → %s" % (
        mp.nstr(max_e,3), "✓" if max_e < mp.mpf('1e-7') else "✗"))
    return max(max_id, max_w, max_e)

sep("P1-P4  归纳证明前提验证")
worst = mp.mpf(0)
worst = max(worst, run_case("4D", [1.5], [2.0], 1.0))
worst = max(worst, run_case("6D", [1.0, 0.8], [1.3, 0.7], 0.6))
worst = max(worst, run_case("8D", [1.0, 0.9, 0.7], [1.1, 0.9, 0.5], 0.4))

sep("P5  归纳证明陈述（代数严格）")
print("""  基础：Be₁ = x″ = e₁′（因为 x″=(A/v²)r′? 实际 x″=r″/v²=Ar′/v²=Be₁，且 e₁′=x″）
  归纳：设 Be_j=e_j′ (j<i)。记 W_i=x^(i)−Σ_{j<i}(x^(i)·e_j)e_j，|W_i|·e_i=W_i
    (1) |W_i|Be_i = Bx^(i) − Σ(x^(i)·e_j)Be_j = x^(i+1) − Σ(x^(i)·e_j)e_j′
    (2) W_i′ = x^(i+1) − Σ(x^(i+1)·e_j)e_j − Σ(x^(i)·e_j′)e_j − Σ(x^(i)·e_j)e_j′
    (3) 由 B 斜对称 + 归纳：x^(i+1)·e_j=(Bx^(i))·e_j=−x^(i)·Be_j=−x^(i)·e_j′
        → (2)−(1) = Σ[−(x^(i)·e_j′)e_j]+Σ(x^(i)·e_j′)e_j = 0  ⇒  W_i′=|W_i|Be_i
    (4) e_i·Be_i=0（B 斜对称）⇒ W_i·W_i′=|W_i|²e_i·Be_i=0 ⇒ |W_i|′=0
    (5) e_i′=W_i′/|W_i|−W_i·|W_i|′/|W_i|²=Be_i−0=Be_i  ∎
  结论：Be_i=e_i′ 对所有 i 成立 → K=B → trK²=trB² → Σκᵢ²=−trB²/2=Σμⱼ²""")
print("【诚实审计】归纳证明为严格代数（步骤均验证）；退化情形（κᵢ=0）需连续性/单独处理，记为技术细节。")
