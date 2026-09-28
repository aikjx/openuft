# -*- coding: utf-8 -*-
"""
_audit_v57_gr_n0_leaver.py
================================================================================
TUFT v57 独立复算 GR Schwarzschild (2,2,n) Leaver 连分数 n0/n1 锚
--------------------------------------------------------------------------------
纪律：
  - 另写实现，不 import _ma_kerr_leaver_full / _ma_kerr_leaver / 任何 prior 脚本；
  - mpmath dps>=40（本脚本 dps=50）；
  - 数字照抄原始输出；不硬凑；不伪闭合；四态分级；勘误递增（无新勘误则 #42 held）。

【Leaver 连分数完整求导链（从 s=-2 Teukolsky 径向方程出发）】
--------------------------------------------------------------------------------
M=1。Schwarzschild 度规 Δ = r^2 - 2r = r(r-2)，r_+=2（外视界），r_-=0（内/奇点）。

(A) Teukolsky 径向方程（s=-2，K=r^2 ω，Δ'=2(r-1)）：
      Δ^{-s} d/dr (Δ^{s+1} dR/dr) + [ (K^2 - i s Δ')/Δ + 4 i ω r s - λ ] R = 0
    其中 λ = sA_lm = l(l+1) - s(s+1) = 6 - 2 = 4（a=0 分离常数）。

(B)  tortoise  r* = r + ln((r-2)/2)  (M=1)；σ_+ = (r_+^2 ω - m a)/(r_+ - r_-) = 2ω。

(C) Leaver ansatz（任务给定形式，"r" 已平移为 ρ = r_phys - 1，故两奇点 ρ=±1）：
      R = e^{iω r*} (r-1)^{-s - iσ} (r+1)^{s + iσ - iω(r_+ + r_-)} Σ_{n=0}^∞ a_n ((r-1)/(r+1))^n
    换回物理坐标 z = (r_phys - r_+)/(r_phys - r_-) = (r-2)/r：
      R = e^{iω r*} (r-2)^{-s - 2iω} r^{s + 2iω - iω(2+0)} Σ a_n z^n
        = e^{iω r*} (r-2)^{-s - 2iω} r^s Σ a_n z^n          (因 r_++r_-=2, σ=2ω)
    边界条件：视界 r→2 取 ingoing（e^{iω r*}，r*→-∞ 时衰减）；
              无穷 r→∞ 取 outgoing（QNM 要求 Im ω<0 时 e^{iω r*} 增长，构成离散谱）。

(D) 代入 ansatz，z=(r-2)/r 为变量，得到三项线性递推（Leaver 1985 Eq.12）：
      α_n a_n + β_n a_{n-1} + γ_n a_{n-2} = 0,   n>=1
    Schwarzschild 极限（a→0）由一般 Cook-Zalutskiy 参数退化得到（本脚本独立代入 a=0
    重新展开，见下 α/β/γ 闭式）：

      定义（M=1, s=-2, l=2, m=2, λ=4, σ=2ω）：
        α_n(ω) = n^2 + (4 - 4 i ω) n + (3 - 4 i ω)
        β_n (ω) = -2 n^2 + (-2 + 16 i ω) n + (-3 + 8 i ω + 32 ω^2)
        γ_n (ω) = n^2 + (-2 - 8 i ω) n + (-16 ω^2 + 8 i ω)

    （核对：以上为一般 Kerr 参数 D0..D4 在 a=0 的逐次展开：
       zeta=iω, xi=-s-iσ_+=2-2iω, eta=0, p=iω,
       alpha=-1-4iω, gamma=-1, delta=3-4iω, sigma_H=6-4iω,
       D0=delta, D1=4p-2α+γ-δ-2, D2=2α-γ+2, D3=α(4p-δ)-σ_H, D4=α(α-γ+1)；
       α_n=n^2+(D0+1)n+D0, β_n=-2n^2+(D1+2)n+D3, γ_n=n^2+(D2-3)n+D4-D2+2。）

(E) 连分数：递推要求级数在无穷远收敛（outgoing 边界），等价于在 n=0 处截断条件
        C_0(ω) ≡ β_0 + α_0 r_0(ω) = 0
    其中自底向上（tail at N）：
        r_n = -γ_{n+1} / (β_{n+1} + α_{n+1} r_{n+1}),   n = N-1, N-2, ..., 0
        r_N = tail（取 0，或 Nollert 渐近；本脚本用 tail=0 主测，并报 N=50/100/200/400 spread）。
    overtone n>=1：用第 n 阶反演连分数 C_n(ω)=β_n + α_n r_n = 0（r 从 N 降到 n）。

【v56 不收敛诊断（具体哪项错）】
--------------------------------------------------------------------------------
v56 _v56_probe_leaver.py 的系数：
    a(n) = n^2 + 2n(s+1) + (s+1)^2 - (lam+1) = (n-1)^2 - 5     (s=-2,lam=4)
    b(n) = -2(n+1)(n+1 - iω)
    c(n) = n^2 + 2ns + s^2 - (lam+1) = (n-2)^2 - 5
    g=a(N); for n: g=a(n)-b(n)c(n+1)/g; return 1+b(0)/g
错误逐项：
  (1) 对角 a(n)=(n-1)^2-5 完全不含 ω —— 正确 α_n 必须含 (4-4iω)n+(3-4iω)。
      v56 把"对角"和"次对角"的 ω 依赖搞混了，导致方程不是 Teukolsky 径向方程的
      谱条件，根自然落不到 QNM。
  (2) 连分数终止条件写成 1+b(0)/g（=0 即 b(0)/g=-1），而正确谱条件是
      β_0 + α_0 r_0 = 0（等价于 r_0 = -β_0/α_0）。归一化/首项错。
  (3) b(n),c(n) 结构（b(n)c(n+1) 耦合）与正确三项递推 α_n,β_n,γ_n 不对称：
      正确递推是 α_n a_n + β_n a_{n-1} + γ_n a_{n-2}=0，对角应是 α_n（含 n^2+(D0+1)n+D0），
      v56 把 a(n) 当对角却用了 (n+s+1)^2-(λ+1) 这种球谐展开余项形式，属张冠李戴。
结论：v56 失败根因 = 递推系数张冠李戴（对角缺 ω 依赖）+ 首项谱条件归一化错；
      不是 tail 方向（v56 也是 bottom-up）、不是分支切线、不是 Γ 相位。
"""
import mpmath as mp
mp.mp.dps = 50
j = 1j

# ------------------------------------------------------------------
# 常数（SSOT 锚，仅作对照；不硬编码进求解器）
# ------------------------------------------------------------------
S = -2
L = 2
M = 2
LAM = L*(L+1) - S*(S+1)     # 4
ANCHOR_N0 = mp.mpc(mp.mpf('0.37367168441804166'), mp.mpf('-0.08896231568893410'))
ANCHOR_N1 = mp.mpc(mp.mpf('0.34671099687909240'), mp.mpf('-0.27391487529119870'))


def make_coeffs(omega):
    """返回 (alpha(n), beta(n), gamma(n)) 闭包，omega 为 mpc。"""
    iw = 1j * omega
    # D0..D4 在 a=0 的闭式（独立代入展开，见模块 docstring）
    D0 = mp.mpf(3) - 4*iw
    D1 = -mp.mpf(4) + 16*iw
    D2 = mp.mpf(1) - 8*iw
    D3 = -mp.mpf(3) + 8*iw + 32*omega*omega
    D4 = -mp.mpf(1) - 16*omega*omega
    def alpha(n):
        n = mp.mpf(n)
        return n*n + (D0 + 1)*n + D0
    def beta(n):
        n = mp.mpf(n)
        return -2*n*n + (D1 + 2)*n + D3
    def gamma(n):
        n = mp.mpf(n)
        return n*n + (D2 - 3)*n + D4 - D2 + 2
    return alpha, beta, gamma


def radial_cf(omega, N=200, overtone=0, tail=0):
    """Leaver 连分数 C_k(omega)=beta_k + alpha_k r_k。tail 为 r_N 初值（默认 0）。"""
    a_, b_, g_ = make_coeffs(omega)
    r = tail
    # 自底向上：r_n = -g_{n+1}/(b_{n+1} + a_{n+1} r_{n+1})
    for n in range(N-1, overtone-1, -1):
        r = -g_(n+1) / (b_(n+1) + a_(n+1)*r)
    return b_(overtone) + a_(overtone)*r


def solve(guess, N=200, overtone=0, tol=mp.mpf('1e-30')):
    f = lambda w: radial_cf(w, N=N, overtone=overtone)
    root = mp.findroot(f, guess, solver='newton', tol=tol, maxsteps=200, verbose=0)
    return root, f(root)


if __name__ == '__main__':
    out = []
    def p(*s):
        line = ' '.join(str(x) for x in s)
        print(line)
        out.append(line)

    p("="*84)
    p("TUFT v57：独立复算 GR Schwarzschild (2,2,n) Leaver 连分数锚")
    p("="*84)
    p(f"dps={mp.mp.dps}  M=1  s={S}  l={L}  m={M}  lambda=sA_lm(a=0)={LAM}")
    p(f"Schwarzschild: r_+=2, r_-=0, sigma=2omega, Delta=r^2-2r")

    # ---------------------------------------------------------------
    # [1] 在锚点处测 |C_0|，验证系数正确（不是求根，是体检）
    # ---------------------------------------------------------------
    p("\n[1] 系数体检：|C_0(anchor)| 应 ~1e-15 以下")
    for N in [50, 100, 200, 400, 800]:
        c = radial_cf(ANCHOR_N0, N=N, overtone=0)
        p(f"    N={N:4d}: |C_0(w0)| = {mp.nstr(mp.norm(c),3)}")

    # ---------------------------------------------------------------
    # [2] n0 独立求根：从粗略初值出发（不紧贴锚）
    # ---------------------------------------------------------------
    p("\n[2] n0 独立求根（粗初值 0.40 - 0.10 i，N=200）")
    guess0 = mp.mpc(0.40, -0.10)
    root0, fres0 = solve(guess0, N=200, overtone=0)
    p(f"    w_n0 = {mp.nstr(root0, 25)}")
    p(f"    |C_0(root)| = {mp.nstr(mp.norm(fres0),3)}")
    err0 = abs(root0 - ANCHOR_N0)
    dig0 = -mp.log10(err0) if err0 > 0 else mp.inf
    p(f"    |w_calc - w_Berti| = {mp.nstr(err0,5)}")
    p(f"    有效位数 = {mp.nstr(dig0,4)} 位  (目标 >=10)")

    # ---------------------------------------------------------------
    # [3] n0 截断 N 收敛性 spread
    # ---------------------------------------------------------------
    p("\n[3] n0 截断 N 收敛性（同一粗初值，不同 N 重解）")
    prev = None
    for N in [50, 100, 200, 400]:
        rN, _ = solve(guess0, N=N, overtone=0)
        d_anchor = abs(rN - ANCHOR_N0)
        spread = abs(rN - prev) if prev is not None else mp.mpf('0')
        p(f"    N={N:4d}: w={mp.nstr(rN,20)}  |vs anchor|={mp.nstr(d_anchor,3)}  |vs prev|={mp.nstr(spread,2)}")
        prev = rN

    # ---------------------------------------------------------------
    # [4] n1 第二对照
    #     谱条件 C_0(ω)=0 的零点即全部 QNM overtone；Newton 从 n1 附近盆地起步。
    #     （注：level-1 反演连分数 C_1=0 在本系数约定下会落到非目标根
    #       0.4254-0.2445i，故采用同一 C_0 行列式条件 + n1 初值盆地，物理上正确。）
    # ---------------------------------------------------------------
    p("\n[4] n1 第二对照（C_0=0 行列式条件，粗初值 0.35 - 0.27 i，N=200）")
    guess1 = mp.mpc(0.35, -0.27)
    root1, fres1 = solve(guess1, N=200, overtone=0)
    p(f"    w_n1 = {mp.nstr(root1, 25)}")
    p(f"    |C_0(root)| = {mp.nstr(mp.norm(fres1),3)}")
    err1 = abs(root1 - ANCHOR_N1)
    dig1 = -mp.log10(err1) if err1 > 0 else mp.inf
    p(f"    |w_calc - w_Berti(n1)| = {mp.nstr(err1,5)}")
    p(f"    有效位数 = {mp.nstr(dig1,4)} 位")

    p("\n[4b] n1 截断 N 收敛性")
    prev = None
    for N in [50, 100, 200, 400]:
        rN, _ = solve(guess1, N=N, overtone=0)
        d_anchor = abs(rN - ANCHOR_N1)
        spread = abs(rN - prev) if prev is not None else mp.mpf('0')
        p(f"    N={N:4d}: w={mp.nstr(rN,20)}  |vs anchor|={mp.nstr(d_anchor,3)}  |vs prev|={mp.nstr(spread,2)}")
        prev = rN

    # ---------------------------------------------------------------
    # [5] 汇总四态分级
    # ---------------------------------------------------------------
    p("\n" + "="*84)
    p("[5] 四态分级")
    p("="*84)
    ok0 = dig0 >= 10
    p(f"  n0: |err|={mp.nstr(err0,3)} -> {mp.nstr(dig0,3)} 位  {'PASS(>=10)' if ok0 else 'FAIL(<10)'}")
    p(f"  n1: |err|={mp.nstr(err1,3)} -> {mp.nstr(dig1,3)} 位")
    if ok0:
        p("  -> 观测检验报告中 'a=0 锚' 由【引用锚(Berti 表)】升级为【独立复算锚】。")
        p("  -> 四态：独立 Leaver 连分数复算 n0 达 >=10 位，GR 门自陈缺口闭合。")
        p("  -> 勘误：无新勘误（#42 held）；本轮补 v56 自陈缺口，不改 SSOT 数值。")
    else:
        p("  -> 未达 10 位，如实报告卡在哪一项，不硬凑；锚仍为引用 Berti 标准值。")

    with open(r"D:\a10\aikjx\code\my_lib\_audit_v57_gr_n0_leaver_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
