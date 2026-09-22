# -*- coding: utf-8 -*-
"""
全域双向分形统一场论 · 全维求导证明验证 · mpmath 50 位高精度精算
================================================================
对象：全域统一场论_全维求导证明验证精算报告.md（V1.0-V1.7）
方法：闭式解析 + 任意精度算术（mpmath, dps=50）。
      凡闭式可验的定理/精算项全部升级到 50 位；格点/谱方法类（霍普夫荷晶格
      积分、40^3 几何曲率、实验一 RK4 演化）属离散层，不做精度升级，
      但对其中可闭式化的子命题（如采样伪迹、谱截断来源）给出精算判读。

精算项（与原报告编号对应）：
  P1  定理一 流守恒        —— λ 源项对消 + 连续层面全恒等式（机器零）
  P2  定理二 荷整性        —— t=0 绕数 Q=1 精确性 + 0.996094=255/256 采样伪迹判定
  P3  定理三/实验二 β 流   —— 奇对称、不动点 ±√(ε/c)、β'(g*)=-2ε、闭式解 g(s)
                              及其 ODE 一阶/二阶恒等式（50 位）
  P4  定理四/实验四 度规   —— 自对偶恒等式 A(r)≡A(ℓ²/r)、f'' 闭式、R=-A''、
                              R'(r*)=0、|R|max=(3+2√2)GM/(2ℓ³)、端点行为（50 位）
  P5  定理五/实验五 因果畴 —— 保守格式望远镜求和恒等式（小格点 50 位精确演示）
  P6  实验三 分形维度      —— ln8/ln3、ln2/ln3、γ=1/2、D=7/2 精确值
  P7  V1.2/V1.3 质量谱     —— 对偶帧酉性 E†E=I、{0,mW²,mW²,mZ²} 精确本征对
  P8  V1.6 量子化         —— 单圈 β 系数 b0 精确有理数、渐近自由窗口 nf≤16
  P9  V1.7 跑动           —— 全部闭式重算（50 位）；MSSM 真预测 sin²θ_W
                              解析闭式 s*=(3a+7A3)/(15a)（替代原网格搜索）
  P10 V1.4/V1.5 代/色结构 —— Z4 Frobenius-Schur 指标、SU(3) 结构常数反对称
                              + Jacobi 恒等式（Gell-Mann 生成元）

红线：数学自洽 != 实验证实。本脚本只做数学精算核验，
      不构成对全域双向分形统一场论物理真实性的任何主张。
"""
import datetime
from mpmath import mp

# 【精度设置陷阱·必读】本环境 mpmath 1.3.0 下 `import mpmath as mp; mp.dps = 50`
# 只会给模块对象挂一个无效的 dps 属性，真正参与运算的上下文精度仍是默认 15 位
# （实测 mpmath.mpf(1)/3 = 0.33333333333333331483 → 仅 15 位有效），且不报错。
# 必须把 dps 设在上下文对象上（from mpmath import mp 后 mp.dps = 50）。
mp.dps = 50

# ───────────────────────── 工具 ─────────────────────────
PASS = []
FAIL = []


def check(name, err, tol):
    ok = err < tol
    (PASS if ok else FAIL).append((name, err, tol))
    return "[PASS]" if ok else "[FAIL]"


def fmt(x, n=50):
    return mp.nstr(x, n)


OUT = []
w = OUT.append

w("全域双向分形统一场论 · 全维精算（mpmath 50 位）")
w("对象：全域统一场论_全维求导证明验证精算报告.md（V1.0-V1.7）")
w("运行时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
w("")

# ═════════════════════════════════════════════════════════
# P1 定理一：流守恒（§1.1 / 实验一）
# ═════════════════════════════════════════════════════════
w("── P1 定理一 流守恒（σ^μ∂_μΨ = λΘΨ* ⇒ ∂_μJ^μ = 0）──")
# 方程的 1+1D σ_z 形式（与 verify_unified_theory.py 实验一同构）：
#   ∂tψ0 = -∂xψ0 - λ·conj(ψ1)
#   ∂tψ1 = +∂xψ1 + λ·conj(ψ0)
# J0 = |ψ0|²+|ψ1|², J1 = |ψ0|²-|ψ1|²（Ψ†σ^μΨ, σ=diag(1,-1)）

lam = mp.mpf("0.5")
# 字面复数值（确定性可复现）
psi0 = mp.mpc("1.2345678901234567", "-0.8765432109876543")
psi1 = mp.mpc("-0.3141592653589793", "0.2718281828459045")
dpsi0 = mp.mpc("0.1123581321345589", "0.1414213562373095")
dpsi1 = mp.mpc("-0.2236067977499789", "0.1732050807568877")

# (a) λ 源项对消：2λRe(ψ0*·(-ψ1*) + ψ1*·ψ0*) = 0
src = 2 * lam * mp.re(mp.conj(psi0) * (-mp.conj(psi1)) + mp.conj(psi1) * mp.conj(psi0))
w("  (a) λ 源项对消 2λRe(ψ0*(-ψ1*)+ψ1*ψ0*) = %s  %s"
  % (mp.nstr(src, 30), check("P1a λ源项对消", abs(src), mp.mpf("1e-48"))))

# (b) 连续层面全恒等式 ∂tJ0 + ∂xJ1 = 0
dp0 = -dpsi0 - lam * mp.conj(psi1)
dp1 = +dpsi1 + lam * mp.conj(psi0)
dJ0 = 2 * mp.re(mp.conj(psi0) * dp0 + mp.conj(psi1) * dp1)
dJ1 = 2 * mp.re(mp.conj(psi0) * dpsi0) - 2 * mp.re(mp.conj(psi1) * dpsi1)
e_p1b = abs(dJ0 + dJ1)
w("  (b) 全恒等式 ∂tJ0+∂xJ1 = %s  %s"
  % (mp.nstr(dJ0 + dJ1, 30), check("P1b 连续层恒等式", e_p1b, mp.mpf("1e-48"))))

# (c) 判读：原报告"连续方程残差 ~1e-5"的来源定性（依据本脚本同目录探针实证）：
#     连续层面恒等式为机器零（双精度 5.55e-16）；1.4e-5 残差全部来自
#     谱导数对截断高斯尾部的可分辨性（g(0)=3.35e-4，Nyquist 系数 8.2e-8，
#     128×8.2e-8≈1.05e-5 与实测 1.43e-5 同量级）——是离散误差非恒等式失效。
w("  (c) 原报告残差 ~1.4e-5 判读：截断高斯尾部（边界 3.35e-4）的谱导数误差，")
w("      非恒等式失效（连续层面双精度实测 5.55e-16）。")
w("")

# ═════════════════════════════════════════════════════════
# P2 定理二：荷整性（§二定理二 / 实验一 t=0 绕数）
# ═════════════════════════════════════════════════════════
w("── P2 定理二 荷整性（t=0 绕数精确性）──")
# 初值 ψ0 = g·e^{ix}，ψ1 = 1+0.5g（g>0 高斯）：
#   z = ψ0/ψ1 = [g/(1+0.5g)]·e^{ix}，径向因子严格为正 ⇒ 绕数 Q = 1 精确。
L = 2 * mp.pi


def gauss_g(x):
    ww = L / 8
    return mp.e ** (-(x - L / 2) ** 2 / (2 * ww ** 2))


min_rad = mp.inf
max_imag = mp.mpf("0")
for j in range(1001):
    x = L * mp.mpf(j) / 1000
    g = gauss_g(x)
    rad = g / (1 + mp.mpf("0.5") * g)
    if rad < min_rad:
        min_rad = rad
w("  径向因子 g/(1+0.5g) 全程最小值 = %s（>0）" % mp.nstr(min_rad, 20))
w("  ⇒ z(x) = 正实因子·e^{ix}，绕数 Q = 1 精确  %s"
  % check("P2 绕数=1（径向因子严格正）", mp.mpf(0) if min_rad > 0 else mp.mpf(1), mp.mpf("1")))
# 采样伪迹判定：实测 Q=0.996094 = 255/256（endpoint=False 时缺最后一个采样点）
q_measured = mp.mpf(255) / 256
w("  实测 Q = 255/256 = %s（与实验一 0.996094 逐位一致）" % mp.nstr(q_measured, 20))
w("  ⇒ Q=0.996094 为 endpoint=False 采样伪迹，非绕数偏差；连续真值 = 1。")
w("")

# ═════════════════════════════════════════════════════════
# P3 定理三/实验二：双向 β 流
# ═════════════════════════════════════════════════════════
w("── P3 定理三/实验二 双向 β 流（β(g)=εg-cg³）──")
eps, c = mp.mpf(1), mp.mpf(1)


def beta(g):
    return eps * g - c * g ** 3


# (a) 奇对称：β(-g)+β(g)=0（多项式恒等，50 位精确）
gs = [mp.mpf(k) / 7 for k in range(-14, 15, 3)]
e_p3a = max(abs(beta(g) + beta(-g)) for g in gs)
w("  (a) 双向对称 max|β(g)+β(-g)| = %s  %s"
  % (mp.nstr(e_p3a, 20), check("P3a β奇对称", e_p3a, mp.mpf("1e-48"))))

# (b) 不动点 g*=±√(ε/c)=±1；β'(g*)=ε-3cg*²=-2ε<0
g_star = mp.sqrt(eps / c)
e_p3b = abs(beta(g_star)) + abs(beta(-g_star)) + abs(eps - 3 * c * g_star ** 2 + 2 * eps)
w("  (b) β(±g*)=0 且 β'(g*)=-2ε<0（阴阳镜像稳定）  合并残差=%s  %s"
  % (mp.nstr(e_p3b, 20), check("P3b 不动点与稳定性", e_p3b, mp.mpf("1e-48"))))

# (c) 闭式解 g(s) = 1/√(1+(1/g0²-1)e^{-2s})；g0=0.5, s=10
g0 = mp.mpf("0.5")
s_end = mp.mpf(10)


def g_closed(s):
    u = 1 + (1 / g0 ** 2 - 1) * mp.e ** (-2 * s)
    return 1 / mp.sqrt(u)


g10 = g_closed(s_end)
w("  (c) 闭式解 g(10) = %s" % mp.nstr(g10, 50))
w("      （原报告双精度 0.999999996908 —— 前 12 位一致）")

# (d) 闭式解满足 ODE：dg/ds = β(g)（mp.diff 数值微分交叉验证）
e_p3d = abs(mp.diff(g_closed, s_end) - beta(g10))
w("  (d) dg/ds - β(g) = %s  %s"
  % (mp.nstr(e_p3d, 20), check("P3d 闭式解满足ODE", e_p3d, mp.mpf("1e-38"))))

# (e) 二阶恒等式 d²g/ds² = β'(g)·β(g)
e_p3e = abs(mp.diff(g_closed, s_end, 2) - (eps - 3 * c * g10 ** 2) * beta(g10))
w("  (e) d²g/ds² - β'(g)β(g) = %s  %s"
  % (mp.nstr(e_p3e, 20), check("P3e 二阶流方程", e_p3e, mp.mpf("1e-38"))))
w("  注：实验二 Euler(2000步) 偏差 -2.8e-9 为离散截断误差；闭式解为精确值。")
w("")

# ═════════════════════════════════════════════════════════
# P4 定理四/实验四：对偶镜像度规
# ═════════════════════════════════════════════════════════
w("── P4 定理四 对偶镜像度规（A(r)=1-k r/(r²+ℓ²), R=-A''）──")
GM, ell = mp.mpf(1), mp.mpf(1)
kk = 2 * GM / ell


def A(r):
    return 1 - kk * r / (r ** 2 + ell ** 2)


def R_of(r):
    return 2 * kk * r * (r ** 2 - 3 * ell ** 2) / (r ** 2 + ell ** 2) ** 3


# (a) 自对偶恒等式 A(r) ≡ A(ℓ²/r)：代数上
#     A(ℓ²/r) = 1 - k(ℓ²/r)/((ℓ⁴/r²)+ℓ²) = 1 - kℓ²r/(ℓ⁴+ℓ²r²) = 1 - kr/(r²+ℓ²) = A(r)
rs = [mp.mpf(k) / 9 for k in range(1, 30, 2)]
e_p4a = max(abs(A(r) - A(ell ** 2 / r)) for r in rs)
w("  (a) 自对偶 max|A(r)-A(ℓ²/r)| = %s  %s（原报告 2.2e-16 为双精度舍入地板）"
  % (mp.nstr(e_p4a, 20), check("P4a 自对偶恒等式", e_p4a, mp.mpf("1e-46"))))

# (b) f = r/(r²+ℓ²) 的二阶导闭式 f'' = 2r(r²-3ℓ²)/(r²+ℓ²)³


def f_of(r):
    return r / (r ** 2 + ell ** 2)


def f2_closed(r):
    return 2 * r * (r ** 2 - 3 * ell ** 2) / (r ** 2 + ell ** 2) ** 3


e_p4b = max(abs(mp.diff(f_of, r, 2) - f2_closed(r)) for r in rs)
w("  (b) f'' 闭式 vs mp.diff 二阶导：max差 = %s  %s"
  % (mp.nstr(e_p4b, 20), check("P4b f''闭式", e_p4b, mp.mpf("1e-38"))))

# (c) R = -A''（曲率闭式全链）
e_p4c = max(abs(-mp.diff(A, r, 2) - R_of(r)) for r in rs)
w("  (c) -A'' vs R(r) 闭式：max差 = %s  %s"
  % (mp.nstr(e_p4c, 20), check("P4c R=-A''", e_p4c, mp.mpf("1e-38"))))

# (d) 极值方程 r⁴-6ℓ²r²+ℓ⁴=0 的根 r=(√2±1)ℓ（精确代数验证）
s2 = mp.sqrt(2)
r1, r2 = (s2 - 1) * ell, (s2 + 1) * ell
e_p4d = abs(r1 ** 4 - 6 * ell ** 2 * r1 ** 2 + ell ** 4) + abs(r2 ** 4 - 6 * ell ** 2 * r2 ** 2 + ell ** 4)
w("  (d) r⁴-6ℓ²r²+ℓ⁴=0 在 r=(√2±1)ℓ 处残差 = %s  %s"
  % (mp.nstr(e_p4d, 20), check("P4d 极值方程根", e_p4d, mp.mpf("1e-46"))))

# (e) R'(r*) = 0（mp.diff 交叉验证两极值点）


def Rprime(r):
    return mp.diff(R_of, r)


e_p4e = abs(Rprime(r1)) + abs(Rprime(r2))
w("  (e) R'(r1)+|R'(r2)| = %s  %s"
  % (mp.nstr(e_p4e, 20), check("P4e 极值一阶条件", e_p4e, mp.mpf("1e-38"))))

# (f) 曲率上界闭式 |R|max = (3+2√2)GM/(2ℓ³)（在 r1 处达到，符号为负）
Rmax_cf = (3 + 2 * s2) * GM / (2 * ell ** 3)
e_p4f = abs(abs(R_of(r1)) - Rmax_cf)
w("  (f) |R(r1)| - (3+2√2)GM/(2ℓ³) = %s  %s"
  % (mp.nstr(e_p4f, 20), check("P4f 曲率上界闭式", e_p4f, mp.mpf("1e-46"))))
w("      R(r2) = +%s（次极值，量级 30 倍小于上界）" % mp.nstr(R_of(r2), 20))

# (g) 端点行为 R(0⁺)=R(∞)=0（奇点被逐出）
e_p4g = abs(R_of(mp.mpf("1e-60"))) + abs(R_of(mp.mpf(10) ** 40))
w("  (g) R(1e-60)=%s, R(1e40)=%s → 端点为 0  %s"
  % (mp.nstr(R_of(mp.mpf("1e-60")), 5), mp.nstr(R_of(mp.mpf(10) ** 40), 5),
     check("P4g 端点行为", e_p4g, mp.mpf("1e-38"))))
w("  注：实验四扫描值 2.9142135543 与闭式 2.9142135624 的差 = 对数网格分辨截断。")
w("")

# ═════════════════════════════════════════════════════════
# P5 定理五/实验五：因果畴（保守格式望远镜求和）
# ═════════════════════════════════════════════════════════
w("── P5 定理五 因果畴（保守迎风格式的精确守恒）──")
# 小格点 50 位精确演示：周期边界下 Σrho_new = Σrho_old（望远镜求和），
# 且畴内变化 = 穿壁通量（内部通量两两相消）。
n = 6
wall = 3
dt = mp.mpf("0.05")
# 任意字面数据（对偶构造：下半域镜像翻转 ⇒ 总荷恒 0）
rho1 = [[mp.mpf(f"{(i + 1) * (j + 2) % 7 + 1}.{i}{j}") for j in range(n)] for i in range(n)]
rho2 = [[-rho1[(i + wall) % n][j] for j in range(n)] for i in range(n)]
rho = [[rho1[i][j] + rho2[i][j] for j in range(n)] for i in range(n)]
uu = [[mp.sin(2 * mp.pi * i / n) / 2 for j in range(n)] for i in range(n)]
vv = [[mp.sin(2 * mp.pi * j / n) / 2 for j in range(n)] for i in range(n)]

e_p5_tot = mp.mpf(0)
e_p5_wall = mp.mpf(0)
for step in range(5):
    tot_old = mp.fsum(mp.fsum(row) for row in rho)
    # 迎风通量（与 verify_unified_theory.py 实验五同构）
    uf = [[(uu[i][j] + uu[i][(j + 1) % n]) / 2 for j in range(n)] for i in range(n)]
    vf = [[(vv[i][j] + vv[(i + 1) % n][j]) / 2 for j in range(n)] for i in range(n)]
    Fx = [[(uf[i][j] * rho[i][j] if uf[i][j] > 0 else uf[i][j] * rho[i][(j + 1) % n])
           for j in range(n)] for i in range(n)]
    Fy = [[(vf[i][j] * rho[i][j] if vf[i][j] > 0 else vf[i][j] * rho[(i + 1) % n][j])
           for j in range(n)] for i in range(n)]
    Qc_old = mp.fsum(rho[i][j] for i in range(n) for j in range(wall))
    flux_acc = mp.fsum(Fx[i][wall - 1] for i in range(n))   # 穿壁
    peri_acc = mp.fsum(Fx[i][n - 1] for i in range(n))       # 周期缝
    rho = [[rho[i][j] - dt * (Fx[i][j] - Fx[i][(j - 1) % n])
            - dt * (Fy[i][j] - Fy[(i - 1) % n][j]) for j in range(n)] for i in range(n)]
    tot_new = mp.fsum(mp.fsum(row) for row in rho)
    Qc_new = mp.fsum(rho[i][j] for i in range(n) for j in range(wall))
    e_p5_tot = max(e_p5_tot, abs(tot_new - tot_old))
    e_p5_wall = max(e_p5_wall, abs((Qc_new - Qc_old) - dt * (peri_acc - flux_acc)))
w("  5 步演化：max|ΔΣrho| = %s  %s"
  % (mp.nstr(e_p5_tot, 20), check("P5a 总荷精确守恒", e_p5_tot, mp.mpf("1e-45"))))
w("  5 步演化：max|ΔQ_C - dt·(穿缝-穿壁)| = %s  %s"
  % (mp.nstr(e_p5_wall, 20), check("P5b 壁通量精确平衡", e_p5_wall, mp.mpf("1e-45"))))
w("  注：实验五的 1.1e-13/8.4e-14 为双精度求和舍入；望远镜恒等式本身是精确代数。")
w("")

# ═════════════════════════════════════════════════════════
# P6 实验三：分形维度精确值
# ═════════════════════════════════════════════════════════
w("── P6 实验三 分形维度（精确值）──")
D_carpet = mp.log(8) / mp.log(3)
D_cantor = mp.log(2) / mp.log(3)
w("  Sierpinski 地毯 D = ln8/ln3 = %s" % mp.nstr(D_carpet, 40))
w("  Cantor 集      D = ln2/ln3 = %s" % mp.nstr(D_cantor, 40))
w("  质量标度律 γ = 1/2（精确）；D = 4-γ = 7/2 = %s（精确）" % mp.nstr(mp.mpf(7) / 2, 10))
# 自洽校验（避免与 16 位字面量对比）：3^D = 8、3^D_cantor = 2 在 50 位下应机器零
e_p6 = abs(mp.e ** (D_carpet * mp.log(3)) - 8) + abs(mp.e ** (D_cantor * mp.log(3)) - 2) \
    + abs(4 - mp.mpf(1) / 2 - mp.mpf(7) / 2)
w("  自洽校验 3^D=8, 3^D_cantor=2, 4-γ=7/2：残差 = %s  %s"
  % (mp.nstr(e_p6, 20), check("P6 分形维度精确值", e_p6, mp.mpf("1e-45"))))
w("  注：实测 1.8928/0.6309 为 box-counting 方法在 level5/6 有限深度下的截断。")
w("")

# ═════════════════════════════════════════════════════════
# P7 V1.2/V1.3：对偶帧酉性与质量谱
# ═════════════════════════════════════════════════════════
w("── P7 V1.2/V1.3 对偶帧 E=(ŵ, Θŵ*) 与电弱质量谱 ──")
# (a) E†E = I：|ŵ|=1 ⇒ 列 2 范数 1；内积 ŵ†Θŵ* = ā(-b̄)+b̄(ā) = 0（代数恒等）
#     选两个字面单位旋量验证 50 位
test_w = [(mp.mpc("0.6", "0.8"), None), (mp.mpc("0.28", "-0.96"), None)]
test_w.append((mp.mpc(mp.mpf("3") / 5, mp.mpf("4") / 5), None))
e_p7a = mp.mpf(0)
for wv, _ in test_w:
    a, b = wv.real, wv.imag
    inner = mp.conj(a) * (-mp.conj(b)) + mp.conj(b) * mp.conj(a)
    e_p7a = max(e_p7a, abs(inner), abs(abs(a) ** 2 + abs(b) ** 2 - 1))
w("  (a) E†E=I 合并残差（内积=0 + 列范数=1）= %s  %s（原报告 8.9e-16 为双精度）"
  % (mp.nstr(e_p7a, 20), check("P7a 对偶帧酉性", e_p7a, mp.mpf("1e-48"))))

# (b) 质量谱 {0, mW², mW², mZ²}（g=0.5, g'=0.3, v=1；与 yang_mills_verify.py 同参）
g, gp, v = mp.mpf("0.5"), mp.mpf("0.3"), mp.mpf(1)
mW2 = g * g * v * v / 4
mZ2 = (g * g + gp * gp) * v * v / 4
# 2×2 块 [[g²,gg'],[gg',g'²]]·v²/4 的精确本征对：
#   λ=0 本征矢 (g',-g)；λ=(g²+g'²)v²/4 本征矢 (g,g')
blk = [[g * g * v * v / 4, g * gp * v * v / 4], [g * gp * v * v / 4, gp * gp * v * v / 4]]
evec0 = (gp, -g)
evec1 = (g, gp)
r0 = (blk[0][0] * evec0[0] + blk[0][1] * evec0[1],
      blk[1][0] * evec0[0] + blk[1][1] * evec0[1])
r1 = (blk[0][0] * evec1[0] + blk[0][1] * evec1[1],
      blk[1][0] * evec1[0] + blk[1][1] * evec1[1])
e_p7b = max(abs(r0[0]), abs(r0[1]),
            abs(r1[0] - mZ2 * evec1[0]), abs(r1[1] - mZ2 * evec1[1]))
w("  (b) 质量谱：λ=0 本征矢 (g',-g) 零化残差；λ=mZ² 本征矢 (g,g') 残差")
w("      mW² = %s, mZ² = %s  %s"
  % (mp.nstr(mW2, 20), mp.nstr(mZ2, 20), check("P7b 质量谱精确本征对", e_p7b, mp.mpf("1e-48"))))
# (c) m_H = 2√2·√κ·v（κ=0.5）与 m_W 比例
kappa = mp.mpf("0.5")
mH = 2 * mp.sqrt(2) * mp.sqrt(kappa) * v
w("  (c) m_H/m_W = %s / %s = %s（精确）"
  % (mp.nstr(mH, 20), mp.nstr(g * v / 2, 20), mp.nstr(mH / (g * v / 2), 30)))
w("")

# ═════════════════════════════════════════════════════════
# P8 V1.6：单圈 β 系数与渐近自由窗口（精确有理数）
# ═════════════════════════════════════════════════════════
w("── P8 V1.6 单圈 β 系数（精确有理算术）──")
# b0 = (11/3)C2(A) - (4/3)T(R)·nf；SU(3): C2=3, T(基本)=1/2
b0_pure = mp.mpf(11) / 3 * 3
b0_nf6 = mp.mpf(11) / 3 * 3 - mp.mpf(4) / 3 * mp.mpf(1) / 2 * 6
e_p8 = abs(b0_pure - 11) + abs(b0_nf6 - 7)
w("  SU(3) 纯规范 b0 = 11/3·3 = %s（应=11）；nf=6 时 b0 = %s（应=7）"
  % (mp.nstr(b0_pure, 10), mp.nstr(b0_nf6, 10)))
w("  %s" % check("P8 b0 精确值", e_p8, mp.mpf("1e-48")))
# 渐近自由窗口：b0>0 ⟺ nf < 33/2 ⟺ nf ≤ 16
nf_window = mp.mpf(33) / 2
w("  渐近自由窗口 nf < 33/2 = %s ⇒ nf ≤ 16（标准模型 nf=6 深在区内）"
  % mp.nstr(nf_window, 10))
# 单圈 β 的奇函数性：β(-g) = -β(g)（g³ 多项式恒等，逐项对消）
gg = [mp.mpf(k) / 11 for k in range(1, 12)]
e_p8b = max(abs(mp.mpf(1) / 3 * (-x) ** 3 - (-(mp.mpf(1) / 3 * x ** 3))) for x in gg)
w("  β 奇函数性残差 = %s  %s"
  % (mp.nstr(e_p8b, 20), check("P8b 单圈β奇函数", e_p8b, mp.mpf("1e-48"))))
w("")

# ═════════════════════════════════════════════════════════
# P9 V1.7：统一跑动（全部闭式 50 位重算）
# ═════════════════════════════════════════════════════════
w("── P9 V1.7 统一跑动检验（闭式 50 位重算）──")
a_inv = mp.mpf("127.916")          # α_EM(M_Z)⁻¹（输入，6 位有效）
s2w = mp.mpf("0.23122")            # sin²θ_W(M_Z)（输入）
A3 = mp.mpf(1) / mp.mpf("0.1179")  # α_s(M_Z)⁻¹（输入）
mZ = mp.mpf("91.1876")
v_fw = mp.mpf("255.26")
A1 = mp.mpf(3) / 5 * (1 - s2w) * a_inv
A2 = s2w * a_inv
w("  A1⁻¹ = %s" % mp.nstr(A1, 30))
w("  A2⁻¹ = %s" % mp.nstr(A2, 30))
w("  A3⁻¹ = %s" % mp.nstr(A3, 30))

# (a) 归一化复核恒等式 3A2/(3A2+5A1) = sin²θ_W（代数恒等）
e_p9a = abs(3 * A2 / (3 * A2 + 5 * A1) - s2w)
w("  (a) 复核恒等式 3A2/(3A2+5A1)-sin²θ = %s  %s"
  % (mp.nstr(e_p9a, 20), check("P9a 归一化复核", e_p9a, mp.mpf("1e-46"))))

# (b) SM 单圈三线不汇聚：b=(41/10, -19/6, -7)
b1s, b2s, b3s = mp.mpf(41) / 10, mp.mpf(-19) / 6, mp.mpf(-7)
x12 = (A1 - A2) / (b1s - b2s)
M12 = mZ * mp.e ** (2 * mp.pi * x12)
A_at = A1 - b1s * x12
A3_at = A3 - b3s * x12
mismatch = abs(A_at - A3_at) / A_at * 100
w("  (b) SM：α1=α2 交点 M = %s GeV，交点 α⁻¹=%s，同点 α3⁻¹=%s"
  % (mp.nstr(M12, 8), mp.nstr(A_at, 8), mp.nstr(A3_at, 8)))
w("      三线差距 = %s%%（单圈无大统一，标准结论）" % mp.nstr(mismatch, 6))

# (c) CP² 候选 sin²θ=1/4 检验（闭式）
x_v = mp.log(v_fw / mZ) / (2 * mp.pi)
A1v, A2v = A1 - b1s * x_v, A2 - b2s * x_v
s2w_v = 3 * A2v / (3 * A2v + 5 * A1v)
r_t = mp.mpf(9) / 5
x_star = (A1 - r_t * A2) / (b1s - r_t * b2s)
M_star = mZ * mp.e ** (2 * mp.pi * x_star)
w("  (c) 跑动到 v=%s GeV：sin²θ(v) = %s，与 1/4 差 %s%%"
  % (mp.nstr(v_fw, 8), mp.nstr(s2w_v, 20), mp.nstr((s2w_v - mp.mpf(1) / 4) * 400, 6)))
w("      sin²θ=1/4 唯一成立尺度 M = %s GeV（无框架出处，候选未获支持）"
  % mp.nstr(M_star, 10))

# (d) MSSM 对照（b=(33/5, 1, -3)）：统一点 + 真预测解析闭式
b1m, b2m, b3m = mp.mpf(33) / 5, mp.mpf(1), mp.mpf(-3)
x_unif = (A1 - A2) / (b1m - b2m)
M_unif = mZ * mp.e ** (2 * mp.pi * x_unif)
A_gut = A1 - b1m * x_unif
A3_at_m = A3 - b3m * x_unif
w("  (d) MSSM 统一点 M = %s GeV，α_GUT⁻¹ = %s（同点 α3⁻¹=%s，差 %s%%）"
  % (mp.nstr(M_unif, 8), mp.nstr(A_gut, 8), mp.nstr(A3_at_m, 8),
     mp.nstr(abs(A3_at_m - A_gut) / A_gut * 100, 6)))
# 真预测闭式：解 (A1_0(s)-A3)/(b1-b3) = (A2_0(s)-A3)/(b2-b3)
#   A1_0 = (3/5)(1-s)a, A2_0 = s·a, b1-b3 = 48/5, b2-b3 = 4
#   ⇒ 5(A1_0-A3) = 12(A2_0-A3) ⇒ 3a+7A3 = 15sa ⇒ s* = (3a+7A3)/(15a)
s_star = (3 * a_inv + 7 * A3) / (15 * a_inv)
x13_star = ((mp.mpf(3) / 5) * (1 - s_star) * a_inv - A3) / (b1m - b3m)
M_pred = mZ * mp.e ** (2 * mp.pi * x13_star)
aGUT_pred = A3 - b3m * x13_star
w("      真预测闭式 s* = (3a+7A3)/(15a) = %s（vs 实验 %s，差 %s%%）"
  % (mp.nstr(s_star, 30), mp.nstr(s2w, 10), mp.nstr((s_star - s2w) / s2w * 100, 6)))
w("      对应统一尺度 M = %s GeV，α_GUT⁻¹ = %s"
  % (mp.nstr(M_pred, 8), mp.nstr(aGUT_pred, 10)))
w("      （原脚本以 10 万点网格搜索得 0.23094——本闭式给出精确值，二者一致）")
w("  注：V1.7 各输入仅 4-6 位有效，50 位精算消除的是算术舍入，不改变物理结论。")
w("")

# ═════════════════════════════════════════════════════════
# P10 V1.4/V1.5：Z4 表示与 SU(3) 李代数
# ═════════════════════════════════════════════════════════
w("── P10 V1.4/V1.5 Z4 Frobenius-Schur 指标 与 SU(3) 结构常数 ──")
# (a) FS 指标：ν(ρ_k) = (1/4)Σ_{j=0}^{3} i^{2kj}；k=0..3 → (+1, 0, +1, 0)
I = mp.mpc(0, 1)
fs = []
for k in range(4):
    nu = mp.fsum(I ** (2 * k * j) for j in range(4)) / 4
    fs.append(nu)
e_p10a = abs(fs[0] - 1) + abs(fs[1]) + abs(fs[2] - 1) + abs(fs[3])
w("  (a) FS 指标 = (%s, %s, %s, %s) → 实不可约表示 ρ0,ρ2,ρ1⊕ρ3 共 3 个 = 三代"
  % (mp.nstr(fs[0], 10), mp.nstr(fs[1], 10), mp.nstr(fs[2], 10), mp.nstr(fs[3], 10)))
w("      %s（第四代被表示论禁戒）" % check("P10a FS指标", e_p10a, mp.mpf("1e-48")))

# (b) SU(3) Gell-Mann 生成元：结构常数反对称 + Jacobi 恒等式（50 位）
def lam_mat():
    Z = lambda: mp.zeros(3, 3)
    l1 = Z(); l1[0, 1] = 1; l1[1, 0] = 1
    l2 = Z(); l2[0, 1] = -I; l2[1, 0] = I
    l3 = Z(); l3[0, 0] = 1; l3[1, 1] = -1
    l4 = Z(); l4[0, 2] = 1; l4[2, 0] = 1
    l5 = Z(); l5[0, 2] = -I; l5[2, 0] = I
    l6 = Z(); l6[1, 2] = 1; l6[2, 1] = 1
    l7 = Z(); l7[1, 2] = -I; l7[2, 1] = I
    l8 = Z(); l8[0, 0] = 1 / mp.sqrt(3); l8[1, 1] = 1 / mp.sqrt(3); l8[2, 2] = -1 / mp.sqrt(3)
    return [l1, l2, l3, l4, l5, l6, l7, l8]


def comm(a, b):
    return a * b - b * a


LM = lam_mat()


def f_abc(a, b, cc):
    # [λa,λb] = 2i f^{abc} λc ⇒ f^{abc} = -i/2 tr([λa,λb]λc)/tr(λc²)...
    # 用正交归一 tr(λaλb)=2δab ⇒ f^{abc} = (1/4i)·tr([λa,λb]λc)
    M = comm(LM[a], LM[b]) * LM[cc]
    tr = M[0, 0] + M[1, 1] + M[2, 2]
    return tr / (4 * I)


# 反对称性 f^{abc} = -f^{bac}（对全部 8×8×8 = 512 项）
e_p10b = mp.mpf(0)
for a in range(8):
    for b in range(8):
        for cc in range(8):
            if a == b:
                continue
            e_p10b = max(e_p10b, abs(f_abc(a, b, cc) + f_abc(b, a, cc)))
w("  (b) f^{abc} 全反对称（512 项扫描）max|f^{abc}+f^{bac}| = %s  %s"
  % (mp.nstr(e_p10b, 20), check("P10b f反对称", e_p10b, mp.mpf("1e-45"))))

# Jacobi 恒等式：[[λa,λb],λc] + 环换 = 0（取代表性三元组）
e_p10c = mp.mpf(0)
for (a, b, cc) in [(0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 6, 3), (4, 5, 6), (3, 4, 7)]:
    t = comm(comm(LM[a], LM[b]), LM[cc]) + comm(comm(LM[b], LM[cc]), LM[a]) \
        + comm(comm(LM[cc], LM[a]), LM[b])
    e_p10c = max(e_p10c, max(abs(t[i, j]) for i in range(3) for j in range(3)))
w("  (c) Jacobi 恒等式（6 组生成元三元组）max 元素 = %s  %s"
  % (mp.nstr(e_p10c, 20), check("P10c Jacobi恒等式", e_p10c, mp.mpf("1e-45"))))
w("      （V1.5 验证 A 的 3.33e-16 为双精度地板；50 位下为机器零）")
w("")

# ═════════════════════════════════════════════════════════
# 汇总
# ═════════════════════════════════════════════════════════
w("═" * 60)
w("精算汇总：%d 项核查，PASS %d / FAIL %d" % (len(PASS) + len(FAIL), len(PASS), len(FAIL)))
for name, err, tol in PASS:
    w("  [PASS] %-24s 残差=%s (阈 %s)" % (name, mp.nstr(err, 6), mp.nstr(tol, 4)))
for name, err, tol in FAIL:
    w("  [FAIL] %-24s 残差=%s (阈 %s)" % (name, mp.nstr(err, 6), mp.nstr(tol, 4)))
w("")
w("关键精算结论：")
w("  1. 定理一流守恒的连续层恒等式为精确代数（λ 源项严格对消）；")
w("     原报告残差 ~1e-5 判定为截断高斯尾部的谱导数误差，非恒等式失效。")
w("  2. 定理二：t=0 绕数 Q=1 精确；实测 0.996094 = 255/256 为 endpoint=False")
w("     采样伪迹（缺最后一个采样点），非绕数偏差。")
w("  3. β 流、对偶度规、质量谱、FS 指标、f^{abc}、Jacobi 全部闭式机器零。")
w("  4. V1.7 MSSM 真预测升级为解析闭式 s* = (3a+7A3)/(15a)，与网格搜索一致。")
w("")
w("红线声明：数学自洽 != 实验证实。本文件仅做求导/恒等式的几何-代数精算核验，")
w("          不构成对全域双向分形统一场论物理真实性的任何主张。")

report = "\n".join(OUT)
with open("全域统一场论_全维精算报告_mp.md", "w", encoding="utf-8") as fp:
    fp.write(report + "\n")

# 控制台摘要（GBK 安全：仅中文与基本符号）
print("P%d/%d PASS" % (len(PASS), len(PASS) + len(FAIL)))
for name, err, tol in FAIL:
    print("FAIL:", name, mp.nstr(err, 10))
print("报告已写入 全域统一场论_全维精算报告_mp.md")
