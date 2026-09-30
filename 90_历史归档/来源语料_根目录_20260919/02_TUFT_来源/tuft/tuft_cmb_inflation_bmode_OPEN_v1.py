# -*- coding: utf-8 -*-
"""
TUFT 卷二十二 · 宇宙学/暴胀/CMB 仿真模块（OPEN_v1）
===================================================
诚实边界声明（红线：数学自洽 != 实验证实）：
  * 本模块是「提案性 ansatz 数值探索」。挠率势 V(tau)=v0(1-exp(-tau^2)) 是**假设**，
    非从 TUFT 三本源公理 (kappa,tau,omega) 第一性导出。
  * 慢滚可观测量 (eps, eta, n_s, r) 对 THIS 势形式**仅取决于 tau_star**，g3 在
    V'/V、V''/V 中相消 —— 故本册「宇宙学经 FRG 的 g3 耦合味物理」的联合约束，
    在此势下对 n_s/r 实际不成立（诚实结构性注解）。
  * 草稿原示例代码 tau_star=0.35 落在本势的**陡坡非慢滚区**（eps=14.4, n_s=-62,
    r=231），已被 BICEP/Keck r<0.032 排除 ~4 个量级 —— 这是草稿的自相矛盾，
    已通过 tau 扫描修正：本势在 tau>~2 的**平台区**才可慢滚，且能同时给出
    n_s~0.965、r~1e-4（落在 Planck+BICEP 区间内），但 r 极小 => 非 TUFT 独有信号。
  * f_NL 阶跃、CAMB 完整功率谱为未计算/占位（见函数 stub）。
  * 本模块不恢复卷十九 2026-09-30 已关闭的微观窗口（g-2/EDM/ringdown 已排除）。

修复记录：
  * 草稿 `method="\mathcal{R}K45"` 是 LaTeX 串污染，已改为 `"RK45"`（否则 scipy 报错）。
  * 草稿 `Mp=1.0` 硬编码 + 势标度任意；保留自然单位约定并加量纲注解，不假装已归一化。
  * 新增 tau 扫描 + Planck/BICEP 诚实判定（pass/fail 打印），不美化输出。
  * 草稿 `jnp.linalg`/jax.grad 嵌套写法语法正确，保留但加数值自检。
"""

import sys

try:
    import jax
    import jax.numpy as jnp
    from scipy.integrate import solve_ivp
    _HAS_JAX = True
except Exception as exc:  # pragma: no cover
    _HAS_JAX = False
    _IMPORT_ERROR = exc


# ========== 全局共享参数池（继承卷21，新增 kc） ==========
def param_pool(params):
    g, lam, g1, g2, g3, g4, C_ferm, T_B, kc = params
    return {"g": g, "lam": lam, "g1": g1, "g2": g2, "g3": g3,
            "g4": g4, "C_ferm": C_ferm, "T_B": T_B, "kc": kc}


# ========== FRG Beta 流（与卷21同，系数为 ansatz） ==========
def beta_frg(g):
    if not _HAS_JAX:
        raise RuntimeError("需要 jax + scipy：%s" % _IMPORT_ERROR)
    (g, lam, g1, g2, g3, g4,
     a0, a1, a2, a3, a4, gs, gw, gy) = g
    bg = 0.6 * g**2 - 0.3 * g * g3
    blam = -1.2 * lam * g + 0.4 * g**2 + 0.25 * g3**2
    bg1 = 0.9 * g1**2 + 0.2 * g1 * g2 - 0.55 * g * g1 + 0.18 * g * g3
    bg2 = 0.8 * g2**2 + 0.22 * g1 * g2 - 0.48 * g * g2
    bg3 = 0.65 * g3**2 - 0.36 * g * g3 + 0.18 * g1 * g3 + 0.1 * g2 * g3
    bg4 = 0.55 * g4**2 + 0.28 * g3 * g4
    ba0 = -4 * a0 + 0.1 * g3 * a2
    ba1 = -3 * a1 + 0.2 * g3 * a3
    ba2 = -2 * a2 + 0.3 * g3 * a4
    ba3 = -1 * a3 - 0.15 * g * a1
    ba4 = -0.2 * g * a2
    b_gs = -1 / (16 * jnp.pi**2) * (11 - 2 / 3 * 3) * gs**3 + 0.02 * g3 * gs
    b_gw = 1 / (16 * jnp.pi**2) * (22 / 3 - 2 / 3 * 3) * gw**3 + 0.015 * g3 * gw
    b_gy = 1 / (16 * jnp.pi**2) * (44 / 3 + 2 / 3 * 3) * gy**3 + 0.01 * g3 * gy
    return jnp.array([bg, blam, bg1, bg2, bg3, bg4,
                      ba0, ba1, ba2, ba3, ba4, b_gs, b_gw, b_gy])


# ========== 挠率势与慢滚（本次诚实修正核心） ==========
def V_tau(tau, g3):
    """提案性挠率暴胀势：V = v0*(1-exp(-tau^2))，v0=0.01*g3。
    注：V'/V 与 V''/V 中 g3 相消 => n_s, r 仅由 tau 决定（本势结构特性）。"""
    if not _HAS_JAX:
        raise RuntimeError("需要 jax：%s" % _IMPORT_ERROR)
    v0 = 0.01 * g3
    return v0 * (1.0 - jnp.exp(-tau**2))


def slow_roll(tau, g3):
    """返回 (eps, eta, V)。Mp 取自然单位 1.0（量纲约定，非第一性归一化）。"""
    if not _HAS_JAX:
        raise RuntimeError("需要 jax：%s" % _IMPORT_ERROR)
    V = V_tau(tau, g3)
    Vp = jax.grad(lambda x: V_tau(x, g3))(tau)
    Vpp = jax.grad(jax.grad(lambda x: V_tau(x, g3)))(tau)
    Mp = 1.0
    eps = Mp**2 / 2.0 * (Vp / V) ** 2
    eta = Mp**2 * Vpp / V
    return eps, eta, V


def compute_cosmo_obs(tau_star, g3):
    eps, eta, V = slow_roll(tau_star, g3)
    ns = 1.0 - 6.0 * eps + 2.0 * eta
    r = 16.0 * eps
    nt = -r / 8.0
    return {"eps": float(eps), "eta": float(eta), "ns": float(ns),
            "r": float(r), "nt": float(nt), "V": float(V)}


# ========== tau 扫描：定位慢滚平台区 + 诚实判定 ==========
def scan_slow_roll(g3, tau_grid=None):
    """扫描 tau，报告哪段满足慢滚、能否同时落在 Planck/BICEP 区间。
    诚实结论（已数值确认）：本势在 tau>~2 平台区慢滚；tau~2.7 时
    n_s~0.965, r~1e-4（区间内）；tau=0.35（草稿原值）落在陡坡区，n_s=-62, r=231，已排除。"""
    if tau_grid is None:
        tau_grid = jnp.linspace(0.1, 4.0, 80)
    rows = []
    for t in tau_grid:
        o = compute_cosmo_obs(float(t), g3)
        slow_ok = (o["eps"] < 0.1) and (abs(o["eta"]) < 0.1)
        ns_ok = abs(o["ns"] - 0.9649) < 0.05
        r_ok = o["r"] < 0.032
        rows.append((float(t), o, slow_ok, ns_ok, r_ok))
    return rows


# ========== 主仿真流程 ==========
def global_tuft_cosmo_simulation(uv_params, tau_star):
    if not _HAS_JAX:
        raise RuntimeError("需要 jax + scipy：%s" % _IMPORT_ERROR)

    def frg_ode(s, g):
        return beta_frg(g)

    sol = solve_ivp(frg_ode, (-8, 8), uv_params, method="RK45")  # 修复：草稿为 "\mathcal{R}K45"
    g3_ir = float(sol.y[4, -1])
    T_B = 1.2e-10 * g3_ir
    obs = compute_cosmo_obs(tau_star, g3_ir)
    # 诚实判定
    obs["slow_roll_ok"] = (obs["eps"] < 0.1) and (abs(obs["eta"]) < 0.1)
    obs["ns_in_Planck"] = abs(obs["ns"] - 0.9649) < 0.05
    obs["r_in_BICEP"] = obs["r"] < 0.032
    obs["g3_ir"] = g3_ir
    obs["T_B"] = T_B
    obs["frg_sol"] = sol
    return obs


# ========== 占位：f_NL 阶跃 / CAMB 接口（未计算） ==========
def f_NL_step_feature(t_c=None):
    """TUFT 提案：相变 t_c 处 f_NL 阶跃。当前未计算（无相变动力学实现）。
    返回 None 表示未实现，绝不伪造数值。"""
    return None


def camb_power_spectrum(*args, **kwargs):
    """占位：对接 CAMB 生成完整 CMB 温度/B模功率谱。当前未实现。
    实现需外部 camb 库 + 把 TUFT (n_s, r, f_NL) 映射为 camb 输入。"""
    raise NotImplementedError("CAMB 接口未实现：需外部 camb 库与输入映射")


def _demo():
    uv_init = [0.21, 0.012, 0.11, 0.052, 0.084, 0.042,
               0.01, 0.001, 0.02, 0.002, 0.0005, 1.18, 0.36, 0.18]
    # 草稿原值 tau_star=0.35（陡坡非慢滚，已排除）——保留以展示失败
    res_bad = global_tuft_cosmo_simulation(uv_init, 0.35)
    print("[草稿原值 tau=0.35] 非慢滚、已被 BICEP 排除：")
    print("  eps=%.4e ns=%.4f r=%.4e slow_roll_ok=%s r_in_BICEP=%s"
          % (res_bad["eps"], res_bad["ns"], res_bad["r"],
             res_bad["slow_roll_ok"], res_bad["r_in_BICEP"]))

    # 修正：平台区 tau=2.70，可同时落 Planck+BICEP
    res = global_tuft_cosmo_simulation(uv_init, 2.70)
    print("[修正 tau=2.70] 平台区慢滚：")
    print("  T_B=%.6e  g3_ir=%.4f" % (res["T_B"], res["g3_ir"]))
    print("  eps=%.4e eta=%.4e ns=%.4f r=%.4e n_T=%.4e"
          % (res["eps"], res["eta"], res["ns"], res["r"], res["nt"]))
    print("  slow_roll_ok=%s  ns_in_Planck=%s  r_in_BICEP=%s"
          % (res["slow_roll_ok"], res["ns_in_Planck"], res["r_in_BICEP"]))
    print("  诚实注：r~1e-4 极小 => 与多数小 r 暴胀模型无区分度；f_NL 阶跃/camb 未计算")


if __name__ == "__main__":
    if not _HAS_JAX:
        print("[WARN] jax/scipy 不可用，仅展示模块结构。")
        print("       导入错误: %s" % _IMPORT_ERROR)
        sys.exit(0)
    _demo()
