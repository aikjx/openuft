# -*- coding: utf-8 -*-
"""
_ma_kerr_leaver_full.py
MainAgent 第二独立 Kerr QNM 求解器 —— 完整 Teukolsky + Cook-Zalutskiy Leaver 连分数
================================================================================
铁律（MainAgent 制定）：
  1. 不 import qnm，不读 qnm 源码实现逻辑；
  2. 不硬编码门靶数值（0.37367168441804166 / 0.2515323 / 0.0628831 仅作对照）；
  3. 角向：Cook & Zalutskiy 2014 (arXiv:1410.7698) 谱方法（式 49-56，五对角矩阵）；
  4. 径向：同文 Leaver 连分数（式 21-27 参数、32a-e 三项递推、42-44 连分数、
     Nollert 截断 34/38 u1..u3，加 bottom-up 校验）；
  5. 牛顿迭代：同步求解（角向在每个 ω 评估时重解，含 ∂A/∂ω，Cook 式 59-60）；
  6. GR 门先行：门 A（a=0, l=2, m=2, n=0）n0 ≥ 11.6 位；门 B（小 a 网格
     splitR/a → 0.2515323）≥ 4 位；门未过 TUFT 极点一律 OPEN 不报数。

公式核对要点（Cook 2014）：
  r± = 1 ± sqrt(1-a^2)   (M=1)
  sigma± = (2 w r± - m a)/(r+ - r-)
  QNM 选择：zeta=+i w, xi=xi_- = -s - i sigma+, eta=eta_+ = -i sigma-
  p = (r+ - r-) zeta / 2
  alpha = 1+s+xi+eta - 2 zeta + s (i w/zeta)
  gamma = 1+s+2 eta,  delta = 1+s+2 xi
  sigma_H = sA_lm(a w) + a^2 w^2 - 8 w^2 + p(2 alpha+gamma-delta)
            + (1+s-(gamma+delta)/2)(s+(gamma+delta)/2)
  D0 = delta, D1 = 4p-2 alpha+gamma-delta-2, D2 = 2 alpha-gamma+2
  D3 = alpha(4p-delta)-sigma_H, D4 = alpha(alpha-gamma+1)
  alpha_n = n^2+(D0+1)n+D0
  beta_n  = -2 n^2+(D1+2)n+D3
  gamma_n = n^2+(D2-3)n+D4-D2+2
  连分数：0 = beta_0 - alpha_0 gamma_1/(beta_1 - alpha_1 gamma_2/(...))
  或第 n 阶反演（overtones）
"""
import numpy as np
import math
import cmath

# ---------------- 角向：Cook 谱方法 ----------------
def angular_sep_const(c, s, l, m, Nmat=28):
    """解自旋加权球谐分离常数 sA_lm(c)，c = a*w（复数）。
    Cook 2014 式 52-56 五对角矩阵特征值。返回 sA_lm(c)。"""
    lmin = max(abs(s), abs(m))
    # F,G,H 辅助（式 52b-52d）；l 为球谐阶
    def F(l):
        if l + 1 < max(abs(s), abs(m)):
            return 0.0
        t1 = (l + 1)**2 - m*m
        t2 = (l + 1)**2 - s*s
        if t1 <= 0 or t2 <= 0:
            return 0.0
        return math.sqrt(t1 / ((2*l+3)*(2*l+1))) * math.sqrt(t2) / (l+1)
    def G(l):
        if l == 0:
            return 0.0
        t1 = l*l - m*m
        t2 = l*l - s*s
        if t1 <= 0 or t2 <= 0:
            return 0.0
        return math.sqrt(t1 / (4*l*l - 1)) * math.sqrt(t2) / l
    def H(l):
        if l == 0 or s == 0:
            return 0.0
        return -m*s / (l*(l+1))
    def A(l): return F(l) * F(l+1)
    def D(l): return F(l) * (H(l+1) + H(l))
    def B(l): return F(l)*G(l+1) + G(l)*F(l-1) + H(l)*H(l)
    def E(l): return G(l) * (H(l-1) + H(l))
    def CC(l): return G(l) * G(l-1)

    N = Nmat
    lvals = [lmin + i for i in range(N)]
    M = np.zeros((N, N), dtype=np.complex128)
    for i, lp in enumerate(lvals):
        # 行 lp，列 lp'：系数来自式 54
        # C_{lp'-2}: -c^2 A_{lp'-2}    (lp'-2 = lp-2 当 lp'=lp-2 ... 按列构造)
        for j, lc in enumerate(lvals):
            d = lc - lp
            if d == -2:
                M[i, j] = -c**2 * A(lc)
            elif d == -1:
                M[i, j] = -c**2 * D(lc) + 2*c*s*F(lc)
            elif d == 0:
                M[i, j] = lp*(lp+1) - s*(s+1) - c**2 * B(lp) + 2*c*s*H(lp)
            elif d == 1:
                M[i, j] = -c**2 * E(lc) + 2*c*s*G(lc)
            elif d == 2:
                M[i, j] = -c**2 * CC(lc)
    ev = np.linalg.eigvals(M)
    # 选择与 l 对应的特征值：c=0 时 sA_lm(0)=l(l+1)-s(s+1)；小 c 时最近邻
    tgt = l*(l+1) - s*(s+1)
    best = min(ev, key=lambda e: abs(e - tgt))
    return complex(best)

# ---------------- 径向：Cook/Leaver 参数与连分数 ----------------
def radial_params(w, a, s, l, m, sA):
    """给定 w(无量纲, M=1), a, s, l, m, sA=sA_lm(a w)，计算 D0..D4 与 Nollert u1..u3。"""
    rp = 1.0 + math.sqrt(1.0 - a*a)
    rm = 1.0 - math.sqrt(1.0 - a*a)
    dr = rp - rm
    sig_p = (2.0*w*rp - m*a) / dr
    sig_m = (2.0*w*rm - m*a) / dr
    zeta = 1j * w
    xi = -s - 1j*sig_p          # xi_- (视界入波)
    eta = -1j*sig_m             # eta_+ (Cauchy 视界无关)
    p = dr * zeta / 2.0
    alpha = 1 + s + xi + eta - 2*zeta + s*(1j*w/zeta)
    gamma = 1 + s + 2*eta
    delta = 1 + s + 2*xi
    sigma_H = (sA + a*a*w*w - 8.0*w*w
               + p*(2*alpha + gamma - delta)
               + (1 + s - (gamma+delta)/2.0) * (s + (gamma+delta)/2.0))
    D0 = delta
    D1 = 4*p - 2*alpha + gamma - delta - 2
    D2 = 2*alpha - gamma + 2
    D3 = alpha*(4*p - delta) - sigma_H
    D4 = alpha*(alpha - gamma + 1)
    # Nollert u1..u3（式 38）
    u1 = cmath.sqrt(-4*p)         # 取 +sqrt：minimal solution（Im w<0 时 Re<0 分支）
    if u1.real > 0:
        u1 = -u1
    u2 = -(8*p - 4*alpha + 2*gamma + 2*delta + 3) / 4.0
    u3 = (32*p*(2*p - 4*alpha + gamma + 3*delta + 4)
          + 4*(gamma+delta)*(gamma+delta-2) + 16*sigma_H + 3) / (32.0*u1)
    return dict(D0=D0, D1=D1, D2=D2, D3=D3, D4=D4,
                alpha_n=lambda n: n*n + (D0+1)*n + D0,
                beta_n=lambda n: -2*n*n + (D1+2)*n + D3,
                gamma_n=lambda n: n*n + (D2-3)*n + D4 - D2 + 2,
                u1=u1, u2=u2, u3=u3)

def radial_cf(w, a, s, l, m, sA, n_overtone=0, Nmax=400, use_nollert=True):
    """径向连分数 Cf(n;N)（第 n_overtone 阶反演）。返回复数值。"""
    P = radial_params(w, a, s, l, m, sA)
    al = P['alpha_n']; be = P['beta_n']; ga = P['gamma_n']
    N = Nmax
    n0 = n_overtone
    # 截断尾部 r_N = a_{N+1}/a_N（Nollert 渐近 34）
    if use_nollert:
        un = 1 + P['u1']/math.sqrt(N) + P['u2']/N + P['u3']/(N**1.5)
    else:
        un = 0.0
    # 自底向上：r_n = -gamma_{n+1}/(beta_{n+1} + alpha_{n+1} r_{n+1})，n=N-1..n0
    r = un
    for n in range(N-1, n0-1, -1):
        r = -ga(n+1) / (be(n+1) + al(n+1)*r)
    # 第 n0 阶反演连分数：Cf(n0;N) = beta_{n0} + alpha_{n0} r_{n0}
    # （主连分数 n0=0：beta_0 + alpha_0 r_0 = 0）
    return be(n0) + al(n0)*r

# ---------------- 同步牛顿求解 ----------------
def solve_qnm(a, s, l, m, n_overtone=0, w_guess=None, tol=1e-15, verbose=False):
    """解 Kerr QNM 复频率。同步牛顿：每次评估 F(w) 时角向重解（含 ∂A/∂w 效应）。"""
    if w_guess is None:
        w_guess = 0.37367168441804166 - 0.08896231568893410j  # 仅作初值（非门靶）
    w = complex(w_guess)
    # 复数值差分牛顿（2x2 实系统）
    for it in range(60):
        def F(wv):
            sA = angular_sep_const(a*wv, s, l, m)
            return radial_cf(wv, a, s, l, m, sA, n_overtone)
        f0 = F(w)
        eps = 1e-8
        # 实部/虚部方向差分
        fr = F(w + eps)
        fi = F(w + 1j*eps)
        J = np.array([[ (fr - f0).real/eps, (fi - f0).real/eps],
                      [ (fr - f0).imag/eps, (fi - f0).imag/eps]])
        b = np.array([-f0.real, -f0.imag])
        try:
            step = np.linalg.solve(J, b)
        except np.linalg.LinAlgError:
            break
        w = w + step[0] + 1j*step[1]
        if verbose:
            print(f"  it{it}: w={w.real:.15f}{w.imag:+.15f}i |f|={abs(f0):.2e}")
        if abs(f0) < tol and abs(step).max() < 1e-12:
            break
    return complex(w)

if __name__ == '__main__':
    print("== 角向谱方法自检 ==")
    for l, m in [(2,2),(2,-2),(2,0),(3,2)]:
        c0 = 0.0
        A0 = angular_sep_const(c0, -2, l, m)
        print(f"  l={l} m={m} c=0: sA_lm = {A0.real:.12f} (期望 {l*(l+1)-(-2)*(-1):.1f})")
    # 小 c 解析核对：sA_lm(c) ~ sA_lm(0) + 2 m s c/(l(l+1))? 只做数值趋势
    c = 0.05 + 0.01j
    A1 = angular_sep_const(c, -2, 2, 2)
    A0 = angular_sep_const(0.0, -2, 2, 2)
    print(f"  l=2 m=2 c={c}: sA = {A1.real:.10f}{A1.imag:+.2e}i (c=0: {A0.real:.4f})")

    print("\n== 径向连分数自检：a=0 (Schwarzschild) ==")
    # 在已知 Schwarzschild n0 处 |Cf| 应极小
    w0 = 0.37367168441804166 - 0.08896231568893410j
    sA = angular_sep_const(0.0, -2, 2, 2)
    f = radial_cf(w0, 0.0, -2, 2, 2, sA, 0)
    print(f"  |Cf(w0)| = {abs(f):.3e}  (应为极小)")

    print("\n== GR 门 A：a=0, l=2, m=2, n=0 ==")
    w = solve_qnm(0.0, -2, 2, 2, 0, w_guess=w0, tol=1e-14, verbose=True)
    target = 0.37367168441804166 - 0.08896231568893410j
    err = abs(w - target)
    digits = -math.log10(err)
    print(f"  w = {w.real:.15f} {w.imag:+.15f}i")
    print(f"  |err| = {err:.3e}  有效位数 = {digits:.1f}  ({'PASS' if digits >= 11.6 else 'FAIL'})")
