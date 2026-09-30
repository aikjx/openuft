# -*- coding: utf-8 -*-
"""
TUFT 卷二十一 · 味物理仿真模块（OPEN_v1）
========================================
诚实边界声明（红线：数学自洽 != 实验证实）：
  * 本模块是「提案性 ansatz 数值探索」，所有系数（omega_i, T_B, 交叉 beta）
    均为**自由拟合参数**，不是从 TUFT 三本源公理 (kappa,tau,omega) 第一性导出。
  * Yukawa -> 挠率 VEV 的关系是**假设性平移**，未减少 SM 的自由参数个数
    （与 O-MASS / openuft v30 的诚实边界一致）。
  * CKM / PMNS 计算已修正为「分别对角化 up / down 型质量矩阵」，
    原大纲 `CKM = SVD(M_q)` 是数学错误（单矩阵 SVD 左奇异向量不是 CKM）。
  * 本模块不恢复卷十九已关闭的微观窗口（g-2 / EDM / ringdown）。
  * 运行依赖 jax + scipy；若环境缺失，模块仍可 import（函数在调用时才求值）。

修复记录：
  * 修复 CKM 定义：V_CKM = U_u^dagger @ U_d，而非单矩阵 SVD。
  * 把质量矩阵拆分为 up / down 两套（原先只有一套），各自带挠率诱导非对角项。
"""

import sys

try:
    import jax
    import jax.numpy as jnp
    from scipy.integrate import solve_ivp
    _HAS_JAX = True
except Exception as exc:  # pragma: no cover - 环境降级
    _HAS_JAX = False
    _IMPORT_ERROR = exc


# ========== 全局共享参数池 ==========
def param_pool(params):
    """把扁平参数向量解包为具名字典（仅作可读性封装，非物理推导）。"""
    g, lam, g1, g2, g3, g4, C_ferm, T_B = params
    return {"g": g, "lam": lam, "g1": g1, "g2": g2, "g3": g3,
            "g4": g4, "C_ferm": C_ferm, "T_B": T_B}


# ========== FRG Beta 流（卷20 + 规范耦合；系数为本卷 ansatz） ==========
def beta_frg(g):
    """
    14 维总 beta 向量：TUFT 引力挠率部分 + SM 规范耦合部分。
    注意：系数为本卷有效场论假设，未从第一性导出；交叉项 0.02*g3*gs 等
    是提案性挠率-规范耦合修正，无独立推导。
    """
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

    # 规范耦合 1-loop 结构 + 挠率交叉修正（ansatz）
    b_gs = -1 / (16 * jnp.pi**2) * (11 - 2 / 3 * 3) * gs**3 + 0.02 * g3 * gs
    b_gw = 1 / (16 * jnp.pi**2) * (22 / 3 - 2 / 3 * 3) * gw**3 + 0.015 * g3 * gw
    b_gy = 1 / (16 * jnp.pi**2) * (44 / 3 + 2 / 3 * 3) * gy**3 + 0.01 * g3 * gy
    return jnp.array([bg, blam, bg1, bg2, bg3, bg4,
                      ba0, ba1, ba2, ba3, ba4, b_gs, b_gw, b_gy])


# ========== 味质量矩阵生成（提案 ansatz） ==========
def build_quark_mass_matrix(T_B, omega_u, omega_c, omega_t,
                            delta12, delta13, delta23):
    """
    挠率诱导的夸克质量矩阵（提案）。
      m_f = omega_f * T_B                 （对角，绝对标度需外部拟合）
      delta_ij = 挠率诱导非对角混合项     （T_B 连续函数，本卷自由参数）
    这是 SM Yukawa 矩阵的「挠率 VEV 重述」——自由参数个数并未减少。
    """
    if not _HAS_JAX:
        raise RuntimeError("需要 jax：%s" % _IMPORT_ERROR)
    m_u = omega_u * T_B
    m_c = omega_c * T_B
    m_t = omega_t * T_B
    Mq = jnp.array([
        [m_u,    delta12, delta13],
        [delta12, m_c,    delta23],
        [delta13, delta23, m_t   ],
    ])
    return Mq


# ========== CKM / PMNS 计算（已修正） ==========
def compute_ckm(M_u, M_d):
    """
    正确物理：CKM = U_u^dagger @ U_d。
    须分别对角化 up 型与 down 型质量矩阵：
        M_u = U_u diag(M_u^diag) U_u^dagger
        M_d = U_d diag(M_d^diag) U_d^dagger
        V_CKM = U_u^dagger U_d
    原大纲 `CKM = SVD(M_q)[0]` 错误：单矩阵 SVD 左奇异向量不是 CKM。
    （实对称矩阵情形 U 为正交，故 U^dagger = U^T。）
    """
    if not _HAS_JAX:
        raise RuntimeError("需要 jax：%s" % _IMPORT_ERROR)
    U_u, _, _ = jnp.linalg.svd(M_u)
    U_d, _, _ = jnp.linalg.svd(M_d)
    CKM = U_u.T @ U_d
    return CKM


def compute_pmns(M_ell, M_nu):
    """PMNS = U_ell^dagger @ U_nu（同上，分别对角化带电轻子与中微子质量矩阵）。"""
    if not _HAS_JAX:
        raise RuntimeError("需要 jax：%s" % _IMPORT_ERROR)
    U_ell, _, _ = jnp.linalg.svd(M_ell)
    U_nu, _, _ = jnp.linalg.svd(M_nu)
    PMNS = U_ell.T @ U_nu
    return PMNS


# ========== 主仿真流程 ==========
def global_tuft_flavor_simulation(uv_params, omega_quark, mix_params,
                                  omega_lepton=None, mix_lepton=None):
    """
    提案性参数扫描：跑 FRG 流 -> 得红外 g3 -> 命题性 T_B -> 构造 up/down 质量矩阵
    -> 计算 CKM。所有标量均为待拟合参数。
    """
    if not _HAS_JAX:
        raise RuntimeError("需要 jax + scipy：%s" % _IMPORT_ERROR)

    def frg_ode(s, g):
        return beta_frg(g)

    sol = solve_ivp(frg_ode, (-8, 8), uv_params, method="RK45")
    g3_ir = sol.y[4, -1]
    T_B = 1.2e-10 * g3_ir  # 提案性标度关系，待拟合

    ou, oc, ot = omega_quark
    d12, d13, d23 = mix_params
    # up 型与 down 型取不同（但同源 T_B）的非对角项，以产生非平庸 CKM
    M_u = build_quark_mass_matrix(T_B, ou, oc, ot, d12, d13, d23)
    M_d = build_quark_mass_matrix(T_B, ou * 0.97, oc * 0.98, ot * 0.999,
                                  d12 * 1.10, d13 * 0.90, d23 * 1.05)
    CKM = compute_ckm(M_u, M_d)

    result = {"frg_sol": sol, "T_B": T_B, "M_u": M_u, "M_d": M_d, "CKM": CKM}

    if omega_lepton is not None and mix_lepton is not None:
        ol_e, ol_mu, ol_tau = omega_lepton
        e12, e13, e23 = mix_lepton
        M_ell = build_quark_mass_matrix(T_B, ol_e, ol_mu, ol_tau, e12, e13, e23)
        # 中微子质量（跷跷板，提案）：更小标度
        M_nu = build_quark_mass_matrix(T_B * 1e-9, ol_e * 0.1, ol_mu * 0.1, ol_tau * 0.1,
                                       e12 * 0.5, e13 * 0.5, e23 * 0.5)
        PMNS = compute_pmns(M_ell, M_nu)
        result["M_ell"] = M_ell
        result["M_nu"] = M_nu
        result["PMNS"] = PMNS

    return result


def _demo():
    uv_init = [0.21, 0.012, 0.11, 0.052, 0.084, 0.042,
               0.01, 0.001, 0.02, 0.002, 0.0005, 1.18, 0.36, 0.18]
    omega_quark = [0.0021, 0.28, 16.2]
    mix = [0.12e-10, 0.008e-10, 0.045e-10]
    omega_lepton = [0.0018, 0.26, 15.9]
    mix_lep = [0.30e-10, 0.10e-10, 0.20e-10]
    res = global_tuft_flavor_simulation(uv_init, omega_quark, mix,
                                        omega_lepton, mix_lep)
    print("T_B = %.6e" % res["T_B"])
    print("CKM (提案性, 未拟合到真实值):")
    print(res["CKM"])
    print("PMNS (提案性, 未拟合到真实值):")
    print(res["PMNS"])
    # 幺正性自检（构造保证，但数值就近检查）
    c = res["CKM"]
    dev = float(jnp.max(jnp.abs(c.T @ c - jnp.eye(3))))
    print("CKM 幺正性偏差 = %.3e (应 ~0)" % dev)


if __name__ == "__main__":
    if not _HAS_JAX:
        print("[WARN] jax/scipy 不可用，仅展示模块结构；跳过数值演示。")
        print("       导入错误: %s" % _IMPORT_ERROR)
        sys.exit(0)
    _demo()
