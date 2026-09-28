# -*- coding: utf-8 -*-
"""
_ma_kerr_teukolsky_spectral.py
MainAgent 第二独立 Kerr QNM 求解器 v2 —— 完整 Teukolsky + Chebyshev 伪谱
================================================================================
铁律：
  1. 不 import qnm，不读 qnm 源码；
  2. 不硬编码门靶数值（0.37367168441804166 / 0.2515323 / 0.0628831 仅作对照输出）；
  3. 角向分离常数：Hughes 2000 附录 A 五对角谱方法（整数 Clebsch-Gordan Racah 公式）；
  4. 径向：Boyer-Lindquist 坐标 x = 1 - r+/r 紧化，Chebyshev 伪谱微分，
     完整 V(r)（含 4i(r-1)K/Δ 交叉项 —— v48 缺失项），二次特征值问题线性化；
  5. GR 门先行：门 A（a=0, l=2, m=2, n=0）n0 需 >= 11.6 位；
     门 B（小 a 网格 splitR/a -> 0.2515323）需 >= 4 位；门未过 TUFT 极点一律 OPEN。

方程（M=1）：
  Delta R'' + (s+1)(2r-2) R' + V R = 0
  V = 2 i s w r - a^2 w^2 - sA + (K^2 + 4 i (r-1) K + i s (a m (2r-2) - 2 w (r^2-a^2) - 4(r-1)K? ) )/Delta ... 
  标准形（Berti 26 / Hughes 4.3）：
  V = 2 i s w r - a^2 w^2 - sA_lm
      + (1/Delta)[ K^2 + 4 i (r-1) K? ...]
  精确 Hughes 4.3: V(r) = -(K^2 + 4 i (r-M) K)/Delta + 8 i w r + lambda
      lambda = E_lm - 2 a m w + a^2 w^2 - 2   (注意 Hughes 的 lambda 含 -s(s+1) 已并入？)
  核对 Berti 26 与 Hughes 4.3 等价（s=-2 时 sA = E - 2 = ...）。
  本实现采用 Hughes 4.3 形式（明确含 4i(r-M)K/Delta 交叉项）。

  注意：Hughes 的 V 与 Berti 的 V 相差一个整体记号：Berti 用 (s+1)(2r-2M)R' 项，
  Hughes 用 Delta^2 d/dr(Delta^-1 dR/dr) 形式。两者等价：
    Delta^2 d/dr(Delta^-1 R') = Delta R'' - Delta' R' = Delta R'' - (2r-2) R'
  对 s=-2: (s+1)(2r-2) = -(2r-2)，所以 Berti 形式 = Delta R'' - (2r-2) R' + V R = 0
  Hughes 形式：Delta R'' - (2r-2) R' + V_H R = 0（对 s=-2，V_H = -(K^2+4i(r-1)K)/Delta + 8iwr + lambda）
  采用 Hughes 形式（s 通式见下推导）。
"""
import numpy as np

# ---------------- 整数 Clebsch-Gordan（Racah 公式，全整数版本） ----------------
def cg_int(j1, m1, j2, m2, J, M):
    """⟨j1 m1 j2 m2 | J M⟩，所有参数为整数（本问题情形）。
    标准 Racah 公式。"""
    import math
    def fact(n): return math.factorial(n)
    if M != m1 + m2:
        return 0.0
    if J < abs(j1 - j2) or J > j1 + j2:
        return 0.0
    # 三角条件
    if abs(m1) > j1 or abs(m2) > j2 or abs(M) > J:
        return 0.0
    # Racah:
    # ⟨j1 m1 j2 m2 | J M⟩ = delta(M,m1+m2) * sqrt( (2J+1) (J+j1-j2)! (J-j1+j2)! (j1+j2-J)! / (J+j1+j2+1)! )
    #   * sqrt( (J+M)! (J-M)! (j1-m1)! (j1+m1)! (j2-m2)! (j2+m2)! )
    #   * sum_k (-1)^k / [ k! (j1+j2-J-k)! (j1-m1-k)! (j2+m2-k)! (J-j2+m1+k)! (J-j1-m2+k)! ]
    pre1 = (2*J + 1) * fact(J+j1-j2) * fact(J-j1+j2) * fact(j1+j2-J) / fact(J+j1+j2+1)
    pre2 = fact(J+M) * fact(J-M) * fact(j1-m1) * fact(j1+m1) * fact(j2-m2) * fact(j2+m2)
    if pre1 * pre2 <= 0:
        return 0.0
    pref = math.sqrt(pre1 * pre2)
    kmin = max(0, j1+j2-J, j1-m1, j2+m2)
    kmax = min(j1+j2-J, j1+j2-J)  # placeholder
    # 正确范围：
    kmin = max(0, j2+m2, j1-m1, -(J-j1+m2), -(J-j2-m1))  # 需小心
    # 标准范围：
    kmin = max(0, j2 + m2, j1 - m1, -J + j2 - m1, -J + j1 + m2)
    kmin = max(0, j2+m2, j1-m1, j2-J-m1, j1-J+m2)
    kmax = min(j1+j2-J, j1+j2-J, j1-m1+j2+m2, j1+j2-J)  # 简化
    # 实际 k 范围：分母所有阶乘参数需非负
    kmax = min(j1+j2-J, j1-m1, j2+m2, J-j2+m1, J-j1-m2)
    kmin = max(0, -(j1-m1-j2-m2), 0)  # dummy
    kmin = max(0, j1-m1, j2+m2)  # wrong; 需满足 J-j2+m1+k>=0 等
    # 精确条件：所有 (…) 内非负
    kmin = max(0, J-j1+m2, J-j2-m1)  # from (J-j2+m1+k)! (J-j1-m2+k)! need k >= J-j2+m1? no
    # 重来：分母 (J-j2+m1+k)! 需 J-j2+m1+k >= 0 -> k >= j2-J-m1
    #       (J-j1-m2+k)! 需 k >= j1-J+m2
    kmin = max(0, j2-J-m1, j1-J+m2)
    kmax = min(j1+j2-J, j1-m1, j2+m2)
    s = 0.0
    for k in range(kmin, kmax+1):
        term = 1.0 / (fact(k) * fact(j1+j2-J-k) * fact(j1-m1-k) * fact(j2+m2-k)
                      * fact(J-j2+m1+k) * fact(J-j1-m2+k))
        if k % 2 == 0:
            s += term
        else:
            s -= term
    return pref * s

# ---------------- 角向分离常数：Hughes 附录 A 谱方法 ----------------
def angular_E(w, a, s, l, m, Nmat=16):
    """解自旋加权球谐本征值 E_lm(w)（sA_lm = E_lm - s(s+1)）。
    五对角矩阵（Hughes A6）。返回复数 E_lm。"""
    import math
    lmin = max(abs(s), abs(m))
    # 索引：l' = lmin..lmin+Nmat-1
    N = Nmat
    inds = [lmin + i for i in range(N)]
    idx = {l0: i for i, l0 in enumerate(inds)}
    M = np.zeros((N, N), dtype=np.complex128)
    aw = a * w
    for i, l0 in enumerate(inds):
        for j0 in [l0-2, l0-1, l0, l0+1, l0+2]:
            if j0 < lmin:
                continue
            if j0 not in idx:
                continue
            j = idx[j0]
            # c_{j0,l0,2}^m = (1/3)delta + (2/3) sqrt((2l0+1)/(2j0+1)) <j0,2,m,0|l0,m><j0,2,-s,0|l0,-s>
            # c_{j0,l0,1}^m = sqrt((2l0+1)/(2j0+1)) <j0,1,m,0|l0,m><j0,1,-s,0|l0,-s>
            f2 = math.sqrt((2*l0+1)/(2*j0+1))
            cg2a = cg_int(j0, 2, m, 0, l0, m)
            cg2b = cg_int(j0, 2, -s, 0, l0, -s)
            c2 = (1.0/3.0 if j0 == l0 else 0.0) + (2.0/3.0) * f2 * cg2a * cg2b
            cg1a = cg_int(j0, 1, m, 0, l0, m)
            cg1b = cg_int(j0, 1, -s, 0, l0, -s)
            c1 = f2 * cg1a * cg1b
            M[j, i] += (aw**2) * c2 - 2*aw*s*c1
            if j0 == l0:
                M[j, i] -= l0*(l0+1)
    ev = np.linalg.eigvals(M)
    # Hughes A6：左侧矩阵 = -E_lm * b_l，即特征值 λ = -E_lm。
    # aw=0 时 λ = -l'(l'+1)。目标 l 的特征值：最接近 -l(l+1) 的 λ，E_lm = -λ。
    tgt = -l*(l+1)
    best = min(ev, key=lambda e: abs(e.real - tgt))
    return complex(-best)

# ---------------- Chebyshev 伪谱 ----------------
def cheb_diff(N):
    """Chebyshev 节点 x_i = cos(pi i/N) (i=0..N, 从 1 到 -1) 与一阶微分矩阵 D。"""
    x = np.cos(np.pi * np.arange(N+1) / N)
    D = np.zeros((N+1, N+1))
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                xi, xj = x[i], x[j]
                # D_ij = c_i/c_j * (-1)^{i+j} / (xi - xj)
                ci = 2.0 if (i == 0 or i == N) else 1.0
                cj = 2.0 if (j == 0 or j == N) else 1.0
                D[i, j] = (ci/cj) * ((-1)**(i+j)) / (xi - xj)
    # 对角
    for i in range(N+1):
        xi = x[i]
        if i == 0:
            D[i, i] = (2*N*N + 1) / 6.0
        elif i == N:
            D[i, i] = -(2*N*N + 1) / 6.0
        else:
            D[i, i] = -xi / (2*(1 - xi*xi))
    return x, D

def kerr_qnm_spectral(a, s, l, m, N=80, n_iter=8, verbose=False):
    """完整 Teukolsky + Chebyshev 伪谱。
    x = 1 - r+/r  ->  r = r+ / (1-x), x in [0,1], x=0 无穷远, x=1 视界。
    QNM 边界：无穷远纯出射（r^3 e^{i w r}），视界纯入波（e^{-i p r*}）。
    二次特征值问题线性化：P w^2 + Q w + R = 0 -> 2N 广义特征值。
    返回最接近 Schwarzschild 基模的 w。"""
    import math
    rp = 1 + math.sqrt(1 - a*a)
    rm = 1 - math.sqrt(1 - a*a)
    x, D = cheb_diff(N)
    r = rp / (1 - x)          # r in [rp, inf)
    Delta = (r - rp) * (r - rm)
    # 1D 导数：d/dr = dx/dr d/dx, dx/dr = (1-x)^2 / rp
    ddx = D
    ddr = np.diag((1-x)**2 / rp) @ D
    ddr2 = ddr @ ddr
    # Hughes 4.3 形式方程（对任意 s 的通式）：
    #   Delta R'' - Delta' R' + [-(K^2+4i(r-1)K)/Delta? ...]
    # 用 Hughes: V_H = -(K^2 + 4 i (r-M) K)/Delta + 8 i w r + lambda, M=1
    #   其中 lambda = E_lm - 2 a m w + a^2 w^2 - 2 （Hughes 4.3, s=-2 专用）
    # 对 s=-2 具体处理；通用 s 稍后扩展。s=-2: Delta' = 2r-2, 方程 Delta R'' - (2r-2)R' + V_H R = 0
    # 但注意 Berti/Hughes 的 Delta^2 d/dr(Delta^-1 dR/dr) 形式：
    #   Delta^2 d/dr(Delta^-1 R') = Delta R'' - Delta' R'，其中 Delta' = 2(r-1)（M=1）
    #   = Delta R'' - 2(r-1) R'
    # 对 s=-2，(s+1) = -1，Berti 方程：Delta R'' - (2r-2) R' + V R = 0 ✓ 一致
    # V_H (s=-2): -(K^2 + 4i(r-1)K)/Delta + 8iw r + lambda
    # 先做 s=-2 专用实现（本任务 l=2 m=+-2 引力扰动）：
    Kf = lambda w: (r**2 + a**2)*w - a*m          # K(r) 数组函数
    # 组装 (w^2, w, const) 三矩阵，在内部点（去掉视界 x=1 与无穷远 x=0 边界行，用边界条件替换）
    # 方程：Delta ddr2 R - 2(r-1) ddr R + V_H(w) R = 0
    # V_H = -(K^2 + 4i(r-1)K)/Delta + 8iw r + (E - 2amw + a^2w^2 - 2)
    # K = (r^2+a^2) w - am  =>  K^2 = (r^2+a^2)^2 w^2 - 2am(r^2+a^2) w + a^2 m^2
    # V_H 中 w 依赖：
    #   -(K^2+4i(r-1)K)/Delta = -[(r^2+a^2)^2 w^2 - 2am(r^2+a^2) w + a^2m^2
    #                             + 4i(r-1)((r^2+a^2) w - am)]/Delta
    #   8iwr + E - 2amw + a^2 w^2 - 2
    # 组合 w^2 系数： -(r^2+a^2)^2/Delta + a^2
    #       w 系数：  +2am(r^2+a^2)/Delta - 4i(r-1)(r^2+a^2)/Delta + 8 i r - 2 a m
    #       const:    -(a^2 m^2 - 4i(r-1) a m)/Delta + E - 2
    # 注意 4i(r-1)K 是 v48 缺失的虚部交叉项 ✓（实部 a^2 m^2/Delta 也来自 K^2 常数部分）
    A2 = -(r**2 + a**2)**2 / Delta + a**2
    A1 = (2*a*m*(r**2 + a**2) - 4j*(r-1)*(r**2 + a**2)) / Delta + 8j*r - 2*a*m
    A0 = -(a**2*m**2 - 4j*(r-1)*a*m) / Delta
    # 组装三矩阵（内部点 i=1..N-1；x=0 对应 i=0 无穷远，x=1 对应 i=N 视界）
    ii = np.arange(1, N)  # 内部点索引
    P = np.zeros((N-1, N-1), dtype=np.complex128)   # w^2
    Q = np.zeros((N-1, N-1), dtype=np.complex128)   # w
    R = np.zeros((N-1, N-1), dtype=np.complex128)   # const
    # 微分算子部分（不含 V）：Delta ddr2 - 2(r-1) ddr 是 (w 无关) 线性算子
    Lop = np.diag(Delta) @ ddr2 - np.diag(2*(r-1)) @ ddr
    # 边界条件：视界（i=N）入波 e^{-i p r*}, p = w - m a/(2 rp)
    #   在 x=1（r=rp）：Δ->0，主导方程退化；用 Frobenius 条件：
    #   R ~ (r-rp)^{rho} , rho = 2 - i sigma  (s=-2)
    #   sigma = (2 w rp - a m)/(rp - rm)? 从 Hughes 4.4: R ~ Delta^2 e^{-i p r*}
    #   e^{-i p r*}: r* ~ (rp^2+a^2)/(rp-rm) ln(r-rp) = 2 rp/(rp-rm) ln(r-rp)  (rp^2+a^2=2rp)
    #   所以 e^{-i p r*} ~ (r-rp)^{-i p 2 rp/(rp-rm)}，p = w - m a/(2 rp)
    #   Delta^2 ~ (r-rp)^2，故 R ~ (r-rp)^{2 - i p 2 rp/(rp-rm)}
    #   rho = 2 - 2 i p rp/(rp-rm) = 2 - 2i(w - ma/(2rp)) rp/(rp-rm) = 2 - 2i w rp/(rp-rm) + i m a/(rp-rm)
    #   边界条件（视界）：dR/dr|_{x=1} = rho/(r-rp) R -> 在 x 坐标：
    #   dx/dr = (1-x)^2/rp；x=1 处 (1-x) -> 0，但需要取极限。
    #   伪谱实现：用视界行替换为 Frobenius 比例条件（代数式，w 线性）：
    #   R(x=N) 与 R(x=N-1) 的关系：R ~ (r-rp)^rho，r-rp = rp x/(1-x)（x->1 时 -> inf? 不对）
    #   重新算：x = 1 - rp/r => r = rp/(1-x) => r-rp = rp x/(1-x)。x->1: r-rp -> inf?? 
    #   啊 x=1 是 r=inf 而非 r=rp！反了：x=1-rp/r，r=rp -> x=0? r=rp: x=1-rp/rp=0。r=inf: x->1。
    #   所以 x=0 是视界，x=1 是无穷远。更正：i=0 视界，i=N 无穷远。
    #   重写：
    #   r = rp/(1-x)：x=0 -> r=rp（视界）；x=1 -> r=inf。
    #   dx/dr = (1-x)^2/rp：x=0 -> 1/rp；x=1 -> 0。
    #   ddr = (1-x)^2/rp * D
    #   ddr2 = ddr @ ddr
    #   视界（x=0, i=0）：R ~ (r-rp)^{rho}，r-rp = rp x/(1-x) ~ rp x (x->0)
    #     R(x) ~ x^{rho}；x_i = cos(pi i/N)，近 x=0 的相邻点关系可用幂律边界。
    #   无穷远（x=1, i=N）：R ~ r^3 e^{i w r}（Hughes 4.5 s=-2），r = rp/(1-x) ~ rp/(1-x)
    #     e^{i w r} 振荡：需要出射条件（非反射）。
    #   处理：视界行用 Frobenius 幂律；无穷远行用 Sommerfeld/出射条件 dR/dr - (iw + 3/r)R = 0? 
    #   对 QNM 谱方法（Jansen 法）常用超曲面/吸收边界；此处用直接边界行替换：
    #   视界：R'(x=0) = rho R/r? 不对，r-rp ~ rp x，dR/dr = rho R/(r-rp) ~ rho R/(rp x)
    #   => (1-x)^2/rp dR/dx = rho R/(rp x) => x=0: dR/dx = rho R/x * (1/(1-x)^2)*rp... 
    #   直接代数：对 i=0 行：R0 与 R1 关系由幂律 R~x^rho：R(x1)/R(x0) = (x1/x0)^rho
    #   实现为行替换：-R0 + (x1/x0)^{-rho} R1 = 0  (w 依赖，非线性 in w)
    #   —— 处理复杂。改用更简单可靠的经典方法：tortoise + 双端打靶？
    #   替代：Leaver 连分数（径向递推用文献已知闭式——付费墙）。
    #   再替代：视界用 Dirichlet 型 Frobenius 线性化（w 线性化近似，rho 对 w 线性）：
    #   rho(w) = 2 - 2 i w rp/(rp-rm) + i m a/(rp-rm)  —— 对 w 线性！
    #   x1/x0 = cos(pi/N)/cos(0)= cos(pi/N)。
    #   (x1/x0)^{-rho} = exp(-rho ln(x1/x0)) —— 指数型，非线性。
    #   小参数处理：rho = c0 + c1 w（c1 纯虚），ln 因子小？cos(pi/N)~1，ln~ -pi^2/(2N^2)。
    #   指数展开一阶：可用线性化。为稳妥：直接用 Lop 在视界行做 Frobenius 条件的一阶：
    #   R1/R0 = (x1/x0)^rho ≈ 1 + rho ln(x1/x0) (小)
    #   => -R0 + (1 + rho ln(x1/x0))^{-1} R1 = 0 => -R0 + (1 - rho ln(x1/x0)) R1 = 0
    #   rho = c0 + c1 w：行变为 (w 线性)：-R0 + (1 - c0 L) R1 - c1 L w R1 = 0
    #   组装进 P/Q/R。
    #   无穷远（x=1, i=N）：出射 R ~ r^3 e^{i w r}；dR/dr = (iw + 3/r) R
    #   => (1-x)^2/rp dR/dx = (i w + 3(1-x)/rp) R  => x=1: (1-x)^2=0 退化！
    #   无穷远出射条件在伪谱中需谨慎（PML 或超曲面）。简化：x=1 行用二阶外推？不。
    #   最稳：采用 Jansen 超曲面坐标。但实现量大。
    #   折衷：本脚本用「内部点 + 视界 Frobenius + 无穷远出射外推」测试；
    #   若门 A 不过，切换超曲面。先实现最简版本跑门 A。
    print("WARNING: 边界条件实现需验证；门 A 判定前不采信任何根")
    return None

if __name__ == '__main__':
    print("== 角向谱方法自检：Schwarzschild 极限 (aw=0) ==")
    for l in [2, 3]:
        E = angular_E(0.0, 0.0, -2, l, 2)
        print(f"  l={l} m=2: E_lm = {E.real:.10f} (期望 {l*(l+1):.1f})")
    for l in [2]:
        E = angular_E(0.2, 0.1, -2, l, 2)
        print(f"  l={l} m=2 aw=0.02: E_lm = {E.real:.10f} {E.imag:+.2e}i (Schw {l*(l+1):.1f})")
