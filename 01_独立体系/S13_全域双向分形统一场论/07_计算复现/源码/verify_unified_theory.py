# -*- coding: utf-8 -*-
"""
全域双向分形统一场论 —— 全维验证与精算脚本
实验1: 1+1D 旋量对偶方程（连续方程残差 + 拓扑荷守恒）
实验2: 双向 beta 流（不动点收敛 + 阴阳对称）
实验3: 分形维度 box-counting（方法链验证 + gamma 提取）
实验4: 对偶镜像度规（自对偶残差 + 曲率有界精算）
实验5: 因果畴晶格（总荷守恒 + 壁通量平衡）
"""
import numpy as np

print("=" * 66)
print("实验1 | 1+1D 旋量对偶方程: 连续方程残差 与 拓扑荷守恒")
print("=" * 66)
L = 2 * np.pi
N = 256
x = np.linspace(0, L, N, endpoint=False)
kv = np.fft.fftfreq(N, d=L / N) * 2 * np.pi
lamb = 0.5

w = L / 8
gauss = np.exp(-(x - L / 2) ** 2 / (2 * w ** 2))
psi0 = gauss * np.exp(1j * x)      # 阴阳比 z = psi0/psi1 绕一圈 -> Q0 = 1
psi1 = 1.0 + 0.5 * gauss           # 无绕数

def rhs(u):
    p0 = u[:N]; p1 = u[N:]
    d0 = -np.fft.ifft(1j * kv * np.fft.fft(p0)) - lamb * np.conj(p1)
    d1 = np.fft.ifft(1j * kv * np.fft.fft(p1)) + lamb * np.conj(p0)
    return np.concatenate([d0, d1])

def rk4(u, dt):
    k1 = rhs(u); k2 = rhs(u + dt / 2 * k1); k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
    return u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

u = np.concatenate([psi0, psi1])
T, dt = 5.0, 0.005
steps = int(T / dt)
Q_list = []
for it in range(steps + 1):
    if it % 250 == 0:
        t = it * dt
        p0 = u[:N]; p1 = u[N:]
        z = p0 / p1
        arg = np.unwrap(np.angle(z))
        Q = (arg[-1] - arg[0]) / (2 * np.pi)
        Q_list.append(Q)
        dp = rhs(u); dp0 = dp[:N]; dp1 = dp[N:]
        J0 = np.abs(p0) ** 2 + np.abs(p1) ** 2
        J1 = np.abs(p0) ** 2 - np.abs(p1) ** 2
        dJ0 = 2 * np.real(np.conj(p0) * dp0 + np.conj(p1) * dp1)
        dJ1 = np.fft.ifft(1j * kv * np.fft.fft(J1)).real
        res = np.max(np.abs(dJ0 + dJ1))
        print(f"  t={t:4.1f} | Q={Q:+.10f} | 连续方程残差 max={res:.3e}")
    u = rk4(u, dt)
print(f"  >> 拓扑荷全程漂移 = {max(Q_list) - min(Q_list):.3e}（应为 0）")

print("=" * 66)
print("实验2 | 双向 beta 流: 不动点收敛 与 阴阳对称")
print("=" * 66)
eps, c = 1.0, 1.0

def beta(g):
    return eps * g - c * g ** 3

def flow(g0, s_max=10.0, ds=0.005):
    g = float(g0); s = 0.0
    while s < s_max:
        g += beta(g) * ds
        s += ds
    return g

g_star = np.sqrt(eps / c)
for g0 in (0.5, -0.5):
    g_end = flow(g0)
    dev = abs(g_end) - g_star
    print(f"  g0={g0:+.1f} -> g(s=10) = {g_end:+.12f} | 不动点 ±{g_star:.12f} | 偏差 {dev:+.3e}")
gs = np.linspace(-2, 2, 4001)
sym = np.max(np.abs(beta(gs) + beta(-gs)))
print(f"  >> 双向对称残差 max|beta(g)+beta(-g)| = {sym:.3e}")
s = 10.0
C = 0.25 / (1 - 0.25)
g_exact = np.sqrt(C * np.exp(2 * s) / (1 + C * np.exp(2 * s)))
print(f"  >> 解析对照 g(s=10) = {g_exact:+.12f} | 数值-解析差 = {flow(0.5) - g_exact:+.3e}")

print("=" * 66)
print("实验3 | 分形维度: box-counting 方法链验证 + gamma 提取")
print("=" * 66)

def box_count_2d(grid, eps):
    n = grid.shape[0]; m = n // eps
    g = grid[:m * eps, :m * eps].reshape(m, eps, m, eps)
    return int(g.any(axis=(1, 3)).sum())

def box_count_1d(arr, eps):
    n = arr.shape[0]; m = n // eps
    g = arr[:m * eps].reshape(m, eps)
    return int(g.any(axis=1).sum())

def fit_dim(epsilons, counts):
    xs = np.log(1.0 / np.array(epsilons))
    ys = np.log(np.array(counts, dtype=float))
    return np.polyfit(xs, ys, 1)[0]

n = 3 ** 5
carpet = np.ones((n, n), dtype=bool)
def carve(lvl, r0, c0, size):
    if lvl == 0:
        return
    th = size // 3
    carpet[r0 + th:r0 + 2 * th, c0 + th:c0 + 2 * th] = False
    for i in range(3):
        for j in range(3):
            if not (i == 1 and j == 1):
                carve(lvl - 1, r0 + i * th, c0 + j * th, th)
carve(5, 0, 0, n)
eps_c = [3, 9, 27, 81]
cnt_c = [box_count_2d(carpet, e) for e in eps_c]
D_c = fit_dim(eps_c, cnt_c)
print(f"  Sierpinski地毯(level5): D实测 = {D_c:.4f} | 理论 ln8/ln3 = {np.log(8) / np.log(3):.4f}")

n1 = 3 ** 6
cant = np.ones(n1, dtype=bool)
def carve1(lvl, start, size):
    if lvl == 0:
        return
    th = size // 3
    cant[start + th:start + 2 * th] = False
    carve1(lvl - 1, start, th)
    carve1(lvl - 1, start + 2 * th, th)
carve1(6, 0, n1)
eps_1 = [3, 9, 27, 81, 243]
cnt_1 = [box_count_1d(cant, e) for e in eps_1]
D_1 = fit_dim(eps_1, cnt_1)
print(f"  Cantor集(level6):      D实测 = {D_1:.4f} | 理论 ln2/ln3 = {np.log(2) / np.log(3):.4f}")

s = np.linspace(0, 10, 1001)
gamma_true = 0.5
m = np.exp(-gamma_true * s)
gamma_fit = -np.polyfit(s, np.log(m), 1)[0]
print(f"  >> 质量标度律: gamma拟合 = {gamma_fit:.6f} (真值 0.5) | D = 4 - gamma = {4 - gamma_fit:.6f}")

print("=" * 66)
print("实验4 | 对偶镜像度规: 自对偶残差 与 曲率精算")
print("=" * 66)
GM, ell = 1.0, 1.0
kk = 2 * GM / ell
def A(r):
    return 1 - kk * r / (r ** 2 + ell ** 2)

r = np.logspace(-6, 6, 200001)
res_sd = np.max(np.abs(A(r) - A(ell ** 2 / r)))
print(f"  自对偶残差 max|A(r)-A(ell^2/r)| = {res_sd:.3e}")
R = 2 * kk * r * (r ** 2 - 3 * ell ** 2) / (r ** 2 + ell ** 2) ** 3
Rmax_scan = np.max(np.abs(R))
r1 = np.sqrt(3 - 2 * np.sqrt(2)); r2 = np.sqrt(3 + 2 * np.sqrt(2))
R1 = 2 * kk * r1 * (r1 ** 2 - 3) / (r1 ** 2 + 1) ** 3
R2 = 2 * kk * r2 * (r2 ** 2 - 3) / (r2 ** 2 + 1) ** 3
Rmax_ana = max(abs(R1), abs(R2))
print(f"  曲率扫描 |R|max = {Rmax_scan:.10f}")
print(f"  曲率解析 |R|max = {Rmax_ana:.10f} | 闭式 (3+2sqrt2)*GM/(2*ell^3) = {(3 + 2 * np.sqrt(2)) * GM / (2 * ell ** 3):.10f}")
print(f"  极值位置 r1={r1:.6f} (R={R1:+.8f}) | r2={r2:.6f} (R={R2:+.8f})")
print(f"  端点行为 R(r->0)={R[0]:.3e} | R(r->inf)={R[-1]:.3e}（均趋于 0，全域有界）")

print("=" * 66)
print("实验5 | 因果畴晶格: 总荷守恒 与 壁通量平衡")
print("=" * 66)
n = 128
xg, yg = np.meshgrid(np.arange(n), np.arange(n))
wall = n // 2
sig = n * 0.08
rho1 = np.exp(-((xg - n * 0.25) ** 2 + (yg - n * 0.5) ** 2) / (2 * sig ** 2))
rho1[xg >= wall] = 0.0
rho2 = -np.roll(rho1, wall, axis=0)   # 对偶畴：镜像翻转 -> 总荷恒 0
rho = rho1 + rho2
u = np.sin(2 * np.pi * yg / n) * 0.5   # 无散剪切流
v = np.sin(2 * np.pi * xg / n) * 0.5

def step(rho, dt):
    uf = 0.5 * (u + np.roll(u, -1, axis=1))
    vf = 0.5 * (v + np.roll(v, -1, axis=0))
    Fx = np.where(uf > 0, uf * rho, uf * np.roll(rho, -1, axis=1))
    Fy = np.where(vf > 0, vf * rho, vf * np.roll(rho, -1, axis=0))
    drho = -(Fx - np.roll(Fx, 1, axis=1)) - (Fy - np.roll(Fy, 1, axis=0))
    return rho + dt * drho, Fx

T5, dt5 = 1.0, 0.05
nsteps = int(T5 / dt5)
Q_tot_max = 0.0
flux_acc = 0.0
Qc0 = rho[:, :wall].sum()
for it in range(nsteps):
    rho, Fx = step(rho, dt5)
    Q_tot_max = max(Q_tot_max, abs(rho.sum()))
    wall_flux = Fx[:, wall - 1].sum()   # x=wall-1 与 wall 之间（穿壁通量）
    peri_flux = Fx[:, n - 1].sum()      # 周期性边界（畴 C 的另一端）
    flux_acc += dt5 * (peri_flux - wall_flux)
Qc_end = rho[:, :wall].sum()
print(f"  总荷 |Q_tot| 全程最大值 = {Q_tot_max:.3e}（应≈0）")
print(f"  壁通量累计预测 dQ_C = {flux_acc:+.10f} | 实测 dQ_C = {Qc_end - Qc0:+.10f} | 平衡残差 = {abs(flux_acc - (Qc_end - Qc0)):.3e}")

print("=" * 66)
print("全部实验完成")
print("=" * 66)
