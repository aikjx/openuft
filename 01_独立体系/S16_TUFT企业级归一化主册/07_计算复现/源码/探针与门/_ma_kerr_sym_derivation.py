# -*- coding: utf-8 -*-
"""
_ma_kerr_sym_derivation.py
MainAgent 第二独立 Kerr QNM 求解器 · 步骤 1：第一性原理符号推导
=============================================================
目标：从 Teukolsky 径向方程（Berti 0905.2975 式 25/26；Hughes gr-qc/9910091 式 4.2/4.3）
      用 sympy 直接推导 Leaver(Jaffe) 径向三项递推系数 alpha_n/beta_n/gamma_n 的显式闭式，
      不读取付费墙后的 Leaver 1985 原文，也不读取/import qnm 源码 —— 完全独立。

方程（M=1, 任意自旋权重 s, 角向分离常数 A_lm）：
    Delta R'' + (s+1)(2r-2) R' + V R = 0
    V = 2 i s w r - a^2 w^2 - A
        + (1/Delta)[ (r^2+a^2)^2 w^2 - 4 a m w r + a^2 m^2
                     + i s ( a m (2r-2) - 2 w (r^2-a^2) ) ]

Jaffe-Leaver ansatz（Berti 式 82）：
    R = e^{i w r} (r-rp)^{rho_p} (r-rm)^{rho_m} F(x),   x = (r-rp)/(r-rm),  F = sum_n a_n x^n
    rho_p = -s - i sigma_p,   rho_m = -1 - s + i w + i sigma_p
    sigma_p = (w rp - a m)/(rp - rm)
    rp = 1 + sqrt(1-a^2),  rm = 1 - sqrt(1-a^2),  rp-rm = 2 sqrt(1-a^2)

验证：a->0 极限下三项递推退化到 Schwarzschild Leaver 递推（可独立核对文献值）。
输出：alpha_n, beta_n, gamma_n 的闭式（关于 n 的多项式），落盘 txt。
"""
import sympy as sp
import time

def main():
    t0 = time.time()
    # ---------- 符号 ----------
    r, rp, rm, a, w, m, s, A = sp.symbols('r rp rm a w m s A', complex=True)
    x = sp.symbols('x')
    n = sp.symbols('n', integer=True, positive=True)
    a_n = sp.Function('a')

    # 逆变换：x=(r-rp)/(r-rm)  =>  r = (rp - rm x)/(1-x)
    r_expr = (rp - rm*x)/(1-x)
    Delta = (r-rp)*(r-rm)
    Delta_x = sp.simplify(Delta.subs(r, r_expr))
    # Delta = (rp-rm)^2 x/(1-x)^2  （期望；验证）
    Delta_x = sp.simplify(Delta_x)

    # ---------- 势 V(r)（M=1） ----------
    K = (r**2 + a**2)*w - a*m
    V = (2*sp.I*s*w*r - a**2*w**2 - A
         + (K**2 + sp.I*s*(a*m*(2*r-2) - 2*w*(r**2 - a**2)))/Delta)

    # ---------- ansatz ----------
    sigma_p = (w*rp - a*m)/(rp - rm)
    rho_p = -s - sp.I*sigma_p
    rho_m = -1 - s + sp.I*w + sp.I*sigma_p

    F = a_n(x)
    R = sp.exp(sp.I*w*r_expr) * (r_expr-rp)**rho_p * (r_expr-rm)**rho_m * F

    # ---------- 代入方程，化为 x 空间的 ODE ----------
    # dR/dr = (dR/dx)(dx/dr),  dx/dr = 1/(dr/dx)
    drdx = sp.diff(r_expr, x)
    dxdr = 1/drdx
    Rp = sp.diff(R, x)*dxdr
    Rpp = sp.diff(sp.diff(R, x)*dxdr, x)*dxdr

    ode = Delta.subs(r, r_expr)*Rpp + (s+1)*(2*r_expr-2)*Rp + V.subs(r, r_expr)*R

    # 消除极点：乘 (1-x)^k * x^(-p)，使得结果是 x 的多项式 * F 的线性组合
    # 期望结构：系数为 x 的洛朗级数。先乘 (1-x)^4 / x^1 试探，再逐步确定。
    # 用 simplify 与 collect 找最低负幂。
    # 策略：对 ode/x^(rho-free) 做 aseries 太慢；直接乘 (1-x)^2 因子后收集。
    # 先看极点阶数：
    fac_candidates = [(1-x)**4, (1-x)**4/x]
    best = None
    for fac in fac_candidates:
        expr = sp.simplify(ode*fac)
        # 展开成关于 x 的多项式（截断？不能截断，F 是级数）
        # 以 F, F', F'' 线性化：subs F(x)->y, a_n(x)->a_n, a_n(x-1)? 不行。
        # 用 aseries? 改用分部：把 F 视作未知函数，提取系数需知道 F 的导数阶。
        # 采用：把 expr 写成 A(x) F'' + B(x) F' + C(x) F，其中 A,B,C 是 x 的有理函数。
        # 方法：sympy 无直接提取，用 substitute F->y(x) 并按 y',y'',y 收集（sympy 支持 coeff 于 y 的导数）。
        y = sp.Function('y')(x)
        expr_y = expr.subs(a_n(x), y)
        A_x = sp.simplify(sp.expand(expr_y).coeff(sp.diff(y, x, 2)))
        B_x = sp.simplify(sp.expand(expr_y).coeff(sp.diff(y, x, 1)))
        C_x = sp.simplify(sp.expand(expr_y).coeff(y))
        # 检查极点：A_x, B_x, C_x 的极点阶
        poles = []
        for name, ex in [('A', A_x), ('B', B_x), ('C', C_x)]:
            # 数值探极点：代入若干 x 值看发散
            poles.append((name, sp.simplify(ex)))
        best = (fac, poles)
        print(f"fac={fac}: A,B,C 化简完成")
    A_x, B_x, C_x = best[1][0][1], best[1][1][1], best[1][2][1]

    # 极点阶数检测：x->0 与 x->1 的行为
    for label, ex in [('A', A_x), ('B', B_x), ('C', C_x)]:
        # 洛朗最低幂
        ser0 = sp.series(sp.simplify(ex), x, 0, 3).removeO()
        ser1 = sp.series(sp.simplify(ex), x, 1, 3).removeO()
        print(f"  [{label}] x~0: {ser0}")

    # 现在 F = sum a_n x^n。A(x)F'' + B(x)F' + C(x)F = 0
    # 每项都写成 x 的有理式 * 级数，收集 x^j 系数得到递推。
    # 设 A(x) = sum_p aA_p x^p (洛朗，p>=pmin)，同理 B, C。
    # 则系数 x^j： sum_n a_n [ (n)(n-1) aA_{j-n} + n aB_{j-n} + aC_{j-n} ] = 0
    # 我们直接用 sympy 对给定 n 构造前几项递推做数值验证；闭式用 rational 系数匹配。
    # 方案：将 A,B,C 展开为洛朗级数（在 x=0），得到系数序列，然后对一般 n 拟合闭式。

    # ---------- 洛朗展开 A,B,C 于 x=0 ----------
    # 用 series 取到足够阶（例如 8 阶），并包含负幂
    def laurent(ex, x0=0, nterms=8):
        """在 x0 处洛朗展开，返回 dict {幂:系数}"""
        s = sp.series(ex, x, x0, nterms+4).removeO()
        # series 可能含 O；用 Poly 提取
        # 转成 Poly 于 x-x0
        p = sp.Poly(s, x)
        return {k: sp.simplify(c) for k, c in p.terms()}

    LA = laurent(A_x, 0, 10)
    LB = laurent(B_x, 0, 10)
    LC = laurent(C_x, 0, 10)
    pmin = min(min(LA), min(LB), min(LC))
    pmax = max(max(LA), max(LB), max(LC))
    print(f"洛朗幂范围: [{pmin}, {pmax}]")

    # ---------- 三项递推验证 ----------
    # 对 x^j 系数：sum_{p<=j} [ j-p 阶项 ]：
    # 记 A(x) = sum_p A_p x^p, B(x)=sum_p B_p x^p, C(x)=sum_p C_p x^p
    # F'' = sum_n n(n-1) a_n x^{n-2};  A F'' 中 x^{n+p-2}
    # 要求 n+p-2 = j => p = j-n+2
    # 系数 = sum_n a_n [ (n)(n-1) A_{j-n+2} + n B_{j-n+1} + C_{j-n} ]
    # 令 k = j-n => n = j-k：
    #   coeff_j = sum_k a_{j-k} [ (j-k)(j-k-1) A_{k+2} + (j-k) B_{k+1} + C_k ]
    # 三项递推成立 ⇔ 对 j 足够大，k 只取 {-1,0,1}（a_{j+1}, a_j, a_{j-1}）之外系数为零。
    # 数值验证：取 j=10, 检查 k=2,3 的贡献是否恒为零（符号上）。

    def coeff_k(j, k):
        """x^j 系数中来自 a_{j-k} 的贡献"""
        Ak = LA.get(k+2, 0)
        Bk = LB.get(k+1, 0)
        Ck = LC.get(k, 0)
        nv = j-k
        return sp.simplify(nv*(nv-1)*Ak + nv*Bk + Ck)

    print("\n--- 三项结构验证（非邻项贡献必须为 0）---")
    ok = True
    for j in [10, 12, 15]:
        for k in [2, 3, 4, -2]:
            c = coeff_k(j, k)
            # 数值探测是否为 0（代入随机数值）
            subs = {rp: 1+sp.sqrt(1-a**2), rm: 1-sp.sqrt(1-a**2)}
            cnum = complex(sp.N(c.subs(subs).subs({a: 0.3, w: 0.5-0.1*sp.I, m: 2, s: -2, A: 4.0})))
            print(f"  j={j}, k={k:+d}: 符号简化为 0? {sp.simplify(c)==0}  数值 |c|={abs(cnum):.2e}")
            if abs(cnum) > 1e-6:
                ok = False
    print(f"三项结构: {'PASS' if ok else 'FAIL'}")

    # ---------- 闭式提取 ----------
    # 邻项：k=-1 (a_{j+1}), k=0 (a_j), k=1 (a_{j-1})
    # gamma_n 对应 a_{n-1}：以 j=n+1 取 k=1 → a_n
    # 定义：alpha_n a_{n+1} + beta_n a_n + gamma_n a_{n-1} = 0
    #   取 j=n：k=-1 → a_{n+1}: alpha_n = coeff_k(n, -1)
    #          k=0  → a_n:      beta_n  = coeff_k(n, 0)
    #          k=1  → a_{n-1}:  gamma_n = coeff_k(n, 1)
    alpha_n = coeff_k(n, -1)
    beta_n = coeff_k(n, 0)
    gamma_n = coeff_k(n, 1)

    # 用 rp, rm 的对称关系化简：rp+rm=2, rp*rm=a^2
    for ex, name in [(alpha_n, 'alpha_n'), (beta_n, 'beta_n'), (gamma_n, 'gamma_n')]:
        ex = sp.simplify(ex)
        # 替换 rm = 2-rp, 保留 rp; 再替换 rp = 1+sqrt(1-a^2)
        ex = sp.simplify(ex.subs(rm, 2-rp))
        ex = sp.simplify(ex.subs(rp, 1+sp.sqrt(1-a**2)))
        print(f"\n{name} = {ex}")
        print(f"  次数（n 的多项式阶）: {sp.degree(sp.Poly(sp.expand(ex), n)) if ex.has(n) else '常数'}")

    # 保存闭式到文件
    out = []
    out.append("TUFT T01 · MainAgent 第二独立实现 · 符号推导结果")
    out.append("Teukolsky 径向 Leaver 三项递推闭式 (M=1, s=-2 时退化；任意 s 通用)")
    out.append(f"alpha_n = {alpha_n}")
    out.append(f"beta_n  = {beta_n}")
    out.append(f"gamma_n = {gamma_n}")
    out.append(f"sigma_p = {sigma_p}")
    out.append(f"rho_p   = {rho_p}")
    out.append(f"rho_m   = {rho_m}")
    out.append(f"符号推导耗时 {time.time()-t0:.1f}s")
    with open(r"D:\a10\aikjx\code\my_lib\_ma_kerr_sym_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\n已落盘 _ma_kerr_sym_out.txt，总耗时 {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
