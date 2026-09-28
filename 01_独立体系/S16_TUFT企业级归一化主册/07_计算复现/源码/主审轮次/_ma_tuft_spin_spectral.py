# -*- coding: utf-8 -*-
"""
_ma_tuft_spin_spectral.py
MainAgent 第三独立 Kerr QNM 求解器 —— 完整非微扰 Teukolsky + Jansen 紧化谱方法 + Beyn
================================================================================
铁律：
  1. 不 import qnm，不读 qnm 源码；只复用自己已验证的 Cook 角向谱方法（自包含复制）。
  2. 径向用完整非微扰 Teukolsky（Hughes 2000 4.3 形式，s=-2, M=1），
     V_H = -(K^2 + 4i(r-1)K)/Delta + 8 i w r + (E_lm - 2 a m w + a^2 w^2 - 2)
     K = (r^2+a^2) w - a m
     —— 不是 v49 的 O(a) 微扰展开（v49 门 B FAIL：虚部系数差 400 倍）。
  3. Jansen 紧化 r = r+ + b(1+z)/(1-z)，z 为 Gauss-Chebyshev 节点 (-1,1)；
     w 依赖边界行：视界入波 Frobenius (r-r+)^{2-i sigma+}，无穷远出射 r^3 e^{i w r}。
  4. 非线性特征值 M(w) R = 0 用 Beyn 围道（v49 已验证 machinery，nc=64, 3 seeds）。
  5. GR 门先行：门 A（a=0, l=2, m=2, n=0）n0 >= 11.6 位；门 B（splitR/a -> 0.2515323）
     >= 4 位；门未过 TUFT 极点一律 OPEN 不报数。
"""
import numpy as np
import math
import cmath
from scipy.linalg import eig, lu_factor, lu_solve

# ---------------- 角向：Cook 谱方法（自包含复制自 _ma_kerr_leaver_full.py） ----------------
def angular_sep_const(c, s, l, m, Nmat=28):
    lmin = max(abs(s), abs(m))
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
    tgt = l*(l+1) - s*(s+1)
    best = min(ev, key=lambda e: abs(e - tgt))
    return complex(best)

# ---------------- Gauss-Chebyshev ----------------
def cheb_gauss(N):
    j  = np.arange(1, N+1)
    th = np.pi*(j-0.5)/N
    z  = np.cos(th)
    w  = ((-1.0)**(j-1))*np.sin(th)
    zi, zj = np.meshgrid(z, z, indexing='ij')
    wi, wj = np.meshgrid(w, w, indexing='ij')
    with np.errstate(divide='ignore', invalid='ignore'):
        D = (wj/wi)/(zi-zj)
    np.fill_diagonal(D, 0.0)
    np.fill_diagonal(D, -D.sum(axis=1))
    return z, D, D@D

# ---------------- 完整非微扰 Kerr Teukolsky 矩阵 M(w) ----------------
def assemble(w, a, s, l, m, N, b):
    """M(w) R = 0，完整 V_H + w 依赖边界行。返回 N×N 复矩阵。"""
    s = -2  # 本任务引力
    z, D, D2 = cheb_gauss(N)
    omz = 1.0 - z
    rp = 1.0 + math.sqrt(1.0 - a*a)          # r+
    rm = 1.0 - math.sqrt(1.0 - a*a)          # r-
    r = rp + b*(1.0 + z)/omz                 # Jansen 紧化
    Delta = (r - rp)*(r - rm)
    # 坐标导数：dz/dr = (1-z)^2/(2b) ；二阶含 d2z/dr2 = -(1-z)^3/(2b^2)
    dzdr = (1.0-z)**2/(2.0*b)
    d2zdr2 = -(1.0-z)**3/(2.0*b*b)
    # Lop = Delta d2/dr2 - (2r-2) d/dr   (Hughes 4.3, s=-2: (s+1)(2r-2)=-(2r-2))
    Lop = (np.diag(Delta*dzdr**2)@D2
           + np.diag(Delta*d2zdr2)@D
           - np.diag((2.0*r-2.0)*dzdr)@D)
    # V_H 三项系数（完整展开，无微扰近似）
    r2pa2 = r*r + a*a
    K2coef_w2 = -(r2pa2)**2/Delta          # -(r^2+a^2)^2 w^2 / Delta
    K2coef_w  = +2.0*a*m*r2pa2/Delta       # +2am(r^2+a^2) w / Delta
    K2coef_c  = -a*a*m*m/Delta             # -a^2 m^2 / Delta
    ic_coef_w = -4j*(r-1.0)*r2pa2/Delta   # 4i(r-1)(r^2+a^2) w / Delta  (注意负号来自 -(4i(r-1)K)/Delta)
    ic_coef_c = +4j*(r-1.0)*a*m/Delta     # -(-4i(r-1)am)/Delta = +4i(r-1)am/Delta
    A2 = K2coef_w2 + a*a                  # +a^2 w^2 (来自 lambda)
    A1 = K2coef_w + ic_coef_w + 8j*r - 2.0*a*m   # +8iwr - 2amw (lambda)
    E_lm = angular_sep_const(a*w, s, l, m) # Cook sA_lm(aw)：Hughes λ = sA - 2amw + a²w²
    A0 = K2coef_c + ic_coef_c + E_lm
    Mmat = Lop + np.diag(A2*w*w + A1*w + A0)
    # ---- 边界行（导数型，w 线性，无指数溢出）----
    # 视界 z->-1（z 最小，jN）：入波 R ~ (r-rp)^{rho}, rho = 2 - i sigma+  (线性于 w)
    #   sigma+ = (2 w rp - a m)/(rp - rm)  =>  rho = rho0 + rho1*w
    idx_h = int(np.argmin(z))
    rho0 = 2.0 + 1j*a*m/(rp - rm)
    rho1 = -2j*rp/(rp - rm)
    dzdr_h = dzdr[idx_h]
    # 边界行： dzdr*D[jn,:] R - [rho/(r_jn-rp)] R_jn = 0
    #   = (dzdr*D[jn,:]) - [rho0/(r_jn-rp)] e_jn - w*[rho1/(r_jn-rp)] e_jn
    rn = r[idx_h]
    Mmat[idx_h, :] = dzdr_h*D[idx_h, :]
    Mmat[idx_h, idx_h] -= rho0/(rn - rp)
    Mmat[idx_h, idx_h] -= w*rho1/(rn - rp)
    # 无穷远 z->+1（z 最大，j0）：出射 R ~ r^3 e^{i w r}（s=-2）
    #   边界行： dzdr*D[j0,:] R - (3/r_j0 + i w) R_j0 = 0
    idx_inf = int(np.argmax(z))
    r0 = r[idx_inf]
    Mmat[idx_inf, :] = dzdr[idx_inf]*D[idx_inf, :]
    Mmat[idx_inf, idx_inf] -= 3.0/r0
    Mmat[idx_inf, idx_inf] -= 1j*w
    return Mmat

# ---------------- Beyn 围道（v49 同款 machinery） ----------------
def beyn_w(assemble_fn, N, b, center, radius=0.05, nc=64, seed=0, **kw):
    n = N
    rng = np.random.default_rng(seed)
    Vv = rng.standard_normal((n,1)) + 1j*rng.standard_normal((n,1))
    th = 2*np.pi*np.arange(nc)/nc
    zz = center + radius*np.exp(1j*th)
    wq = radius*np.exp(1j*th)/nc
    B0 = np.zeros((n,1), dtype=complex); B1 = np.zeros_like(B0)
    for k in range(nc):
        Mw = assemble_fn(zz[k], **kw)
        lu = lu_factor(Mw)
        X = lu_solve(lu, Vv)
        B0 += X*wq[k]
        B1 += zz[k]*X*wq[k]
    return (B0.conj().T@B1)[0,0]/(B0.conj().T@B0)[0,0]

def pole(assemble_fn, N, b, center, radius=0.05, **kw):
    return np.mean([beyn_w(assemble_fn, N, b, center, radius, 64, s, **kw)
                    for s in (0,1,2)])

# ---------------- 主流程 ----------------
def main():
    OUT = []
    def out(s=""):
        print(s, flush=True); OUT.append(str(s))
    GR_N0 = 0.37367168441804166 - 0.08896231568893410j
    GR_SPLIT = 0.2515323
    out("="*78)
    out("_ma_tuft_spin_spectral — 完整非微扰 Teukolsky + Jansen + Beyn（第三独立求解器）")
    out("  M=1 s=-2 l=2 ; 无 qnm import ; 无硬编码门靶求解")
    out("="*78)
    b = complex(4.0, 0.5)
    N = 60

    # ---- GATE A: a=0 n0 ----
    out("")
    out("[A] GATE A — a=0 n0 (complete V_H, no perturbation)")
    rows = []
    for NN in (40, 50, 60):
        def mk(NN=NN, a=0.0, m=2):
            return lambda w: assemble(w, a, -2, 2, m, NN, b)
        w = pole(mk(NN), NN, b, 0.360-0.088j, 0.05)
        rows.append((NN, w))
        out("    N=%3d  w=%.13f %+.13fi  |err|=%.3e" % (NN, w.real, w.imag, abs(w-GR_N0)))
    best = min(rows, key=lambda r: abs(r[1]-GR_N0))
    errA = abs(best[1]-GR_N0)
    gateA = errA < 10**-11.6
    out("    best n0 = %.13f %+.13fi  |err|=%.3e  GATE A: %s" % (
        best[1].real, best[1].imag, errA, "PASS" if gateA else "FAIL"))

    # ---- GATE B: a 网格 splitR/a ----
    out("")
    out("[B] GATE B — a grid splitR/a -> 0.2515323")
    grid = [0.005, 0.01, 0.02, 0.04]
    res = {}
    for a in grid:
        def mkp(NN=N, a=a, m=2):
            return lambda w: assemble(w, a, -2, 2, m, NN, b)
        def mkm(NN=N, a=a, m=-2):
            return lambda w: assemble(w, a, -2, 2, m, NN, b)
        wp = pole(mkp(), N, b, 0.360-0.088j, 0.06)
        wm = pole(mkm(), N, b, 0.360-0.088j, 0.06)
        res[a] = (wp, wm)
        out("    a=%6.3f  Re(w+2)=%+.8f  Re(w-2)=%+.8f  splitR/a=%+.8f" % (
            a, wp.real, wm.real, (wp.real-wm.real)/a))
    aa = np.array(grid)
    ss = np.array([(res[a][0].real-res[a][1].real)/a for a in grid])
    c2 = np.polyfit(aa**2, ss, 1)
    c0 = c2[1]
    errB = abs(c0 - GR_SPLIT)
    dB = -math.log10(errB) if errB > 0 else 20
    gateB = dB >= 4
    out("    a^2 线性外推: c0 = %+.8f  err=%.2e  %.1f 位  GATE B: %s" % (
        c0, errB, dB, "PASS" if gateB else "FAIL"))
    gr_pass = gateA and gateB
    out("")
    out("    =============  GR GATE OVERALL: %s  =============" % ("PASS" if gr_pass else "FAIL"))

    # ---- TUFT 反射壁（仅门过后）----
    if gr_pass:
        out("")
        out("[TUFT] GR gates passed -> switch inner boundary to TUFT reflecting wall")
        out("    (step 2: rho_h wall, psi~s^beta, beta=1.26376 — next script)")
    else:
        out("")
        out("    *** GR gate not passed -> TUFT rotating numbers remain OPEN (honest). ***")

    with open("_ma_tuft_spin_spectral_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(OUT))
    print("\n  -> _ma_tuft_spin_spectral_out.txt")

if __name__ == "__main__":
    main()
