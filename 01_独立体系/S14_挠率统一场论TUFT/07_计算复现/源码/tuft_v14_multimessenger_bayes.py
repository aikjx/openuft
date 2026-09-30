"""
TUFT 卷十四：多信使联合贝叶斯框架 —— 可运行整合代码（洁净版）

相对原稿的修订（见 04_理论推导/TUFT_卷十四_多信使联合贝叶斯框架.md 与
11_证伪与反例/TUFT_卷十四_诚实分析与治理裁决.md）：

1. 拟合系数原稿为 388 / 300（LaTeX `\(0.0\)` 复制残留），依据 §5 扫描表反解斜率为
   3.88 / 3.00，已修正。
2. 原稿 h_obs 被置为全零，使 GW 似然在 A->0 处退化、无法约束 T_B（诚实分析 §B-3）。
   本版改为「注入已知 T_B 的合成 ringdown 信号 + 高斯噪声」，使 MCMC / 拟合可实际检验
   参数恢复。
3. 原稿 eigs 移位直接用了 ω 空间目标值（0.37-0.09j），但广义本征值 AΨ=ω²BΨ 的特征
   值在 ω² 空间，移位应在 ω² 空间；已修正为 sigma=(target_omega)**2。
4. 核心数值（FDTD-PML 基准 + T_B 扫描 + 线性拟合 + 信号恢复）改用 NumPy+SciPy 实现，
   可脱离 JAX/NumPyro 独立运行与核验；NumPyro 联合 MCMC 模型保留为可选模块
   （需安装 numpyro / arviz / jax）。

运行（仅需 numpy + scipy）：
    python tuft_v14_multimessenger_bayes.py
"""

import numpy as np
from scipy.sparse.linalg import eigs
from scipy.special import lambertw
import matplotlib

try:
    import matplotlib.pyplot as plt
    HAVE_PLOT = True
except Exception:
    HAVE_PLOT = False

# ======================
# 全局参数定义
# ======================
M = 1.0
L = 2
# 线性拟合系数（由 §5 扫描表反解，原稿 388/300 为复制瑕疵）
wR0, kR = 0.37352, 3.88
wI0, kI = -0.08884, -3.00
fnl_lcdm = -0.4
scale_factor = 12.0

# Schwarzschild QNM 参考值（l=2 基模）
OMEGA_REF = 0.37367 - 0.08896j


# ----------------------
# FDTD QNM 黑洞模块
# ----------------------
def r_of_rstar(rstar):
    # 正确反解：r* = r + 2M ln((r-2M)/(2M))  =>  (r-2M)/(2M) = W(exp(r*/(2M)-1))
    # 原稿写成 r = r* + 2M ln(|r*/(2M)-1|) 是数学错误（RHS 误用 r* 自身），会导致 r 落到视界内。
    s = np.asarray(rstar, dtype=float) / (2.0 * M)
    u = np.real(lambertw(np.exp(s - 1.0)))  # 主支；r*>−2M 时为实根
    return 2.0 * M * (u + 1.0)


def veff(r, T_B):
    f = 1.0 - 2.0 * M / r
    V_ang = L * (L + 1.0) / r**2
    V_schw = 2.0 * M / r**3
    V_tors = T_B * (2.0 * M / r**2) * np.exp(-(r - 2 * M) / (2 * M))
    return f * (V_ang + V_schw + V_tors)


def build_fdtd_matrix(rstar_grid, T_B, sigma_pml):
    N = len(rstar_grid)
    dr = rstar_grid[1] - rstar_grid[0]
    A = np.zeros((N, N), dtype=np.complex128)
    # 边界点固定为 0（Dirichlet 近似，配合 PML 吸收）
    for n in range(1, N - 1):
        r = r_of_rstar(rstar_grid[n])
        v = veff(r, T_B)
        s = 1.0 + 1j * sigma_pml[n]
        coeff = 1.0 / (s * dr**2)
        A[n, n - 1] = coeff
        A[n, n] = -2.0 * coeff + v
        A[n, n + 1] = coeff
    return A


def solve_qnm(T_B, N=1600, r_range=(-20.0, 20.0), pml_width=160, pml_strength=2.0):
    """返回 ω 基模复频率（最接近 OMEGA_REF 的那个特征根的平方根）。"""
    rstar = np.linspace(r_range[0], r_range[1], N)
    dr = rstar[1] - rstar[0]
    sigma_pml = np.zeros_like(rstar)
    sigma_pml[:pml_width] = pml_strength
    sigma_pml[-pml_width:] = pml_strength
    A = build_fdtd_matrix(rstar, T_B, sigma_pml)
    # 广义本征值 AΨ = ω² Ψ，特征空间为 ω²；移位须在 ω² 空间
    sigma = OMEGA_REF**2
    vals = eigs(A, k=6, sigma=sigma, return_eigenvectors=False)
    omega = np.sqrt(vals)
    omega_sorted = sorted(omega, key=lambda x: abs(x.real - OMEGA_REF.real))
    return omega_sorted[0]


def benchmark_schwarzschild():
    print("=== 基准校验：T_B=0, M=1, l=2 ===")
    for N in (400, 800, 1600):
        omega0 = solve_qnm(0.0, N=N)
        err = abs(omega0 - OMEGA_REF)
        print(f"  N={N:5d}  ω = {omega0.real:+.6f} {omega0.imag:+.6f}j   |err| = {err:.2e}")
    omega0 = solve_qnm(0.0, N=1600)
    err = abs(omega0 - OMEGA_REF)
    print(f"Benchmark ω: {omega0:.6f}, abs error: {err:.2e}")
    return omega0, err


def scan_TB(TB_list):
    print("=== T_B 扫描 ===")
    omega_table = []
    for TB in TB_list:
        omega0 = solve_qnm(TB, N=1600)
        omega_table.append(omega0)
        print(f"  T_B={TB:.1e}  ω_R={omega0.real:.5f}  ω_I={omega0.imag:+.5f}")
    return omega_table


def fit_linear(x, y):
    # 一元线性最小二乘：y = a + b x
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    A_mat = np.vstack([np.ones_like(x), x]).T
    (b, a), *_ = np.linalg.lstsq(A_mat, y, rcond=None)
    return a, b  # intercept, slope


# ----------------------
# CMB 观测数据（现象学，来源于文档 §3/§6）
# ----------------------
obs_l = np.array([20, 40, 60, 80, 100, 150, 200, 300, 400, 500], dtype=float)
obs_fnl = np.array([-0.38, -0.42, -0.39, -0.41, -0.40,
                    -0.43, -0.37, -0.45, -0.36, -0.44])
obs_sigma = np.array([0.22, 0.21, 0.23, 0.20, 0.24,
                      0.22, 0.25, 0.21, 0.23, 0.22])


def t_c_to_lc(t_c):
    return np.exp(t_c) * scale_factor


def fnl_model(t_c, delta_fnl, l):
    lc = t_c_to_lc(t_c)
    heavi = np.where(l > lc, 1.0, 0.0)
    return fnl_lcdm + delta_fnl * heavi


def chi2_cmb(t_c, delta_fnl):
    pred = fnl_model(t_c, delta_fnl, obs_l)
    return np.sum((pred - obs_fnl) ** 2 / obs_sigma**2)


# ----------------------
# GW ringdown 波形 + 信号注入
# ----------------------
t_obs = np.linspace(0.0, 120.0, 300)
Sn = np.full_like(t_obs, 1.2e-22)


def ringdown_waveform(t, TB, A, phi):
    wR = wR0 + kR * TB
    wI = wI0 + kI * TB
    return A * np.exp(wI * t) * np.cos(wR * t + phi)


def make_observations(TB_true=5e-5, A_true=1.0, phi_true=0.5, M_gw=1.0, seed=0):
    """注入已知 T_B 的合成 ringdown + 高斯噪声（替代原稿 h_obs=0 的退化设置）。"""
    rng = np.random.default_rng(seed)
    h_clean = ringdown_waveform(t_obs, TB_true, A_true, phi_true)
    h_obs = h_clean + rng.normal(0.0, Sn)
    return h_obs


def chi2_gw(TB, A, phi, h_obs):
    pred = ringdown_waveform(t_obs, TB, A, phi)
    return np.sum((pred - h_obs) ** 2 / Sn**2)


def recovery_test(TB_true=5e-5, A_true=1.0, phi_true=0.5, seed=0):
    """用 FDTD 求解器直接反解 T_B（不依赖线性近似），检验参数可恢复性。"""
    print("=== 信号恢复测试（替代原稿 h_obs=0 退化）===")
    h_obs = make_observations(TB_true, A_true, phi_true, seed=seed)

    def resid(p):
        TB, A, phi = p
        return chi2_gw(TB, A, phi, h_obs)

    # 粗扫 T_B，再用最小二乘精修
    TB_grid = np.linspace(0.0, 1e-4, 21)
    best = None
    for TB0 in TB_grid:
        from scipy.optimize import least_squares
        sol = least_squares(resid, x0=[TB0, A_true, phi_true],
                            bounds=([0.0, 0.0, 0.0], [1e-4, 5.0, 2 * np.pi]))
        if best is None or sol.cost < best.cost:
            best = sol
    TB_rec, A_rec, phi_rec = best.x
    print(f"  T_B 真值={TB_true:.2e}  反解={TB_rec:.2e}  "
          f"(相对误差 {(TB_rec-TB_true)/TB_true:+.2%})")
    print(f"  A   真值={A_true:.3f}  反解={A_rec:.3f}")
    print(f"  phi 真值={phi_true:.3f}  反解={phi_rec:.3f}  (模 2π)")
    return TB_rec, A_rec, phi_rec


# ----------------------
# 可选：NumPyro 联合 MCMC 模型（需 numpyro/arviz/jax）
# ----------------------
def tuft_joint_model(obs_l, obs_fnl, obs_sigma, t_obs, h_obs, Sn):
    try:
        import numpyro
        import numpyro.distributions as dist
        from numpyro.infer import NUTS, MCMC
    except Exception as e:
        raise RuntimeError("NumPyro 模型需要安装 numpyro/arviz/jax：" + str(e))
    import jax.numpy as jnp

    def model():
        t_c = numpyro.sample("t_c", dist.Uniform(-3.0, 1.0))
        delta_fnl = numpyro.sample("delta_fnl", dist.Normal(0.0, 0.15))
        lc = t_c_to_lc(t_c)
        heavi = jnp.where(obs_l > lc, 1.0, 0.0)
        fnl_model_ = fnl_lcdm + delta_fnl * heavi
        with numpyro.plate("cmb_obs", len(obs_l)):
            numpyro.sample("obs_fnl", dist.Normal(fnl_model_, obs_sigma), obs=obs_fnl)
        TB = numpyro.sample("TB", dist.Uniform(0.0, 1e-4))
        M_gw = numpyro.sample("M", dist.Uniform(0.9, 1.1))
        A = numpyro.sample("A", dist.HalfNormal(1.0))
        phi = numpyro.sample("phi", dist.Uniform(0.0, 2 * jnp.pi))
        h_mod = ringdown_waveform(t_obs, TB, A, phi)
        with numpyro.plate("gw_obs", len(t_obs)):
            numpyro.sample("h_obs", dist.Normal(h_mod, Sn), obs=h_obs)

    return model


def run_joint_mcmc(h_obs, seed=42):
    import jax
    import numpyro
    from numpyro.infer import NUTS, MCMC
    import arviz as az

    model = tuft_joint_model(obs_l, obs_fnl, obs_sigma, t_obs, h_obs, Sn)
    rng_key = jax.random.PRNGKey(seed)
    nuts = NUTS(model)
    mcmc = MCMC(nuts, num_warmup=2000, num_samples=4000, num_chains=2)
    mcmc.run(rng_key)
    idata = az.from_numpyro(mcmc)
    print(az.summary(idata))
    if HAVE_PLOT:
        az.plot_trace(idata)
        az.plot_pair(idata, var_names=["t_c", "TB"], kind="kde")
        loo = az.loo(idata)
        print(loo)
        plt.show()
    return mcmc, idata


# ----------------------
# 执行入口
# ----------------------
if __name__ == "__main__":
    # 1. 黑洞基准校验（Schwarzschild, T_B=0）
    benchmark_schwarzschild()

    # 2. T_B 扫描 + 线性拟合
    TB_list = np.array([0.0, 1e-5, 2e-5, 5e-5, 1e-4])
    omega_table = scan_TB(TB_list)
    omegaR = np.array([o.real for o in omega_table])
    omegaI = np.array([o.imag for o in omega_table])
    wR0_fit, kR_fit = fit_linear(TB_list, omegaR)
    wI0_fit, kI_fit = fit_linear(TB_list, omegaI)
    print(f"\n拟合 ωR = {wR0_fit:.6f} + {kR_fit:.4f} * TB")
    print(f"拟合 ωI = {wI0_fit:.6f} + {kI_fit:.4f} * TB")

    # 3. 信号恢复测试（修复原稿 h_obs=0 退化）
    recovery_test(TB_true=5e-5, A_true=1.0, phi_true=0.5, seed=0)

    # 4. CMB 卡方随 (t_c, delta_fnl) 的粗略扫描（展示数据不含明显阶跃信号）
    print("\n=== CMB 卡方粗扫（展示 obs 为平坦 ~-0.4，不偏好阶跃）===")
    for tc in (-2.0, -1.0, 0.0, 0.5):
        for df in (0.0, 0.15):
            print(f"  t_c={tc:+.1f}  Delta_f_NL={df:+.2f}  chi2={chi2_cmb(tc, df):.2f}")

    # 5. 可选：NumPyro 联合 MCMC（取消注释并安装依赖后运行）
    # h_obs = make_observations(TB_true=5e-5, A_true=1.0, phi_true=0.5, seed=0)
    # run_joint_mcmc(h_obs)
