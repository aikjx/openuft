# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R31  缺口定理 N 的 RG 流数值框架 + Planck CMB 双谱 MCMC + QNM FDTD 骨架
          —— 可导出性与可证伪性审计（可复跑）
================================================================================
承接：
  · 第77章 定理 N（M1/M2/M3 塌缩，openuft 满足度 0/0/1）
  · tuft_beta_running_缺口_定理N实例化（TUFT 固定螺旋 β ≡ 0）
  · tuft_暴胀CMB_全维求导精算（n_s/r/T_reh 全 FAIL）
  · TUFT_V22_三路联合拟合_可证伪性审计 D2-3（Planck f_NL 未探测，数据集不可作基准）
  · R20/R23/R25/R26/R27/R28（QNM 既有数值路径）
  · R29（τ/κ = tanθ = 1/α 口径校准）
  · OPEN_v3（σ_abs=0 联合排除 5.74σ）/ OPEN_v4（三尺度锚与 2.05M 差 26~78 量级）

本册审计的对象是**用户提出的数值框架原型**本身（RG ODE + χ² + MCMC + FDTD），
不是 TUFT 理论本体。审计分两层：
  A. 数学/数值层：公式是否自洽、数值方法是否有效（可 100% 判定）；
  B. 可导出性/可证伪层：参数是否由 TUFT 导出、数据是否真实存在（诚实判定）。

红线：数学自洽 != 实验证实。本册只做框架审计，不主张 TUFT 物理真实性；
      不修改任何既有脚本与理论方程。
================================================================================
"""
from __future__ import print_function

import os
import sys
import json
import math
import time

import numpy as np
from scipy.integrate import solve_ivp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_TXT = os.path.join(HERE, "tuft_r31_report.txt")
REPORT_JSON = os.path.join(HERE, "tuft_r31_report.json")

SEED = 20260930

# ----------------------------------------------------------------- 物理常数 / 观测锚
ALPHA = 1.0 / 137.035999084
TWO_PI = 2.0 * math.pi

# Planck 2018 (arXiv:1807.06211, 表 5)：局域型 f_NL = -0.9 ± 5.1（未探测非高斯性）
FNL_LOCAL_OBS = -0.9
FNL_LOCAL_SIG = 5.1
# BICEP/Keck 2021 上限
R_TENSOR_MAX = 0.036
# 宇宙学（Planck 2018）
A_S = 2.1e-9
ETA0_MPC = 1.4e4          # 到最后散射面的共形距离 ~14000 Mpc（l ≈ k·η0）
L_MIN, L_MAX = 2.0, 2500.0
M_PL_RED_GEV = 2.435e18   # 约化普朗克质量

# ----------------------------------------------------------------- 判定记录器
OUT = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
ITEMS = []


def put(s=""):
    OUT.append(s)
    print(s)


def sec(t):
    put("")
    put("=" * 78)
    put("  " + t)
    put("=" * 78)


def rec(tag, key, name, detail, data=None):
    COUNTS[tag] += 1
    ITEMS.append({"tag": tag, "key": key, "name": name,
                  "detail": detail, "data": data if data is not None else {}})
    put("  [%s] %s  |  %s" % (tag, name, detail))


def P(key, name, detail, data=None):
    rec("PASS", key, name, detail, data)


def F(key, name, detail, data=None):
    rec("FAIL", key, name, detail, data)


def B(key, name, detail, data=None):
    rec("BOUNDARY", key, name, detail, data)


def I(key, name, detail, data=None):
    rec("INFO", key, name, detail, data)


# ================================================================= §0 环境门禁
def s0_env():
    sec("§0  运行环境与依赖门禁（决定本报告的可执行边界）")
    have_jax = True
    jax_ver = "-"
    try:
        import jax  # noqa
        jax_ver = jax.__version__
    except Exception:
        have_jax = False
    have_numpyro = True
    try:
        import numpyro  # noqa
    except Exception:
        have_numpyro = False

    put("  Python %s | numpy %s | scipy %s" % (
        sys.version.split()[0], np.__version__, __import__("scipy").__version__))
    put("  jax = %s | numpyro = %s" % (jax_ver if have_jax else "NOT INSTALLED",
                                       "yes" if have_numpyro else "NOT INSTALLED"))
    if have_jax:
        P("S0.1", "jax 可用", "主路径可用 JAX 自动微分交叉校验（版本 %s）" % jax_ver)
    else:
        B("S0.1", "jax 不可用 ⇒ 降级 numpy 主路径",
          "本机 Python3.8 未安装 jax/jaxlib；本脚本用 numpy+scipy 实跑并通过有限差分"
          "证明梯度性质（结论与 JAX 一致，因结论是分段常数性而非实现细节）；"
          "JAX 原型另见 tuft_r31_JAX原型_rg_cmb_qnm.py（未实跑，诚实标注）")
    if not have_numpyro:
        B("S0.2", "numpyro 不可用 ⇒ 嵌套采样未实跑",
          "本机无 numpyro；用户要求的'接入 numpyro 嵌套采样'无法在本环境执行。"
          "本册改为给出**可运行的等价管线**（网格边缘化 + 闭式 profile + 纯 numpy "
          "Metropolis），并指出 numpyro/NUTS 在该模型上的**结构性失效原因**（§6.1）")
    return have_jax


# ================================================================= §1 公理口径审计
def s1_axiom():
    sec("§1  仓库公理口径审计：低能固定点 r0 = tanθ 到底取多少（三套口径）")
    put("  用户约定：α^(-1) = 2π/θ ⇒ θ = 2πα；r(t) = tanθ(t)；低能固定点 r0 = tan(2πα)。")
    put("  用户给定 r0 = 0.0918；本册实算核对。")

    theta_A = TWO_PI * ALPHA                      # 公理口径 A
    r_A = math.tan(theta_A)
    r_user = 0.0918
    theta_user = math.atan(r_user)                # 反解用户值对应的角度
    ratio_theta = theta_user / theta_A

    # 口径 B：R29 交叉发现（严格 Frenet：τ/κ = tanθ；白皮书 α = τ/κ ⇒ tanθ = 1/α）
    r_B = 1.0 / ALPHA
    theta_B = math.atan(r_B)

    put("  θ_A = 2πα = %.9f rad ⇒ r_A = tanθ_A = %.9f" % (theta_A, r_A))
    put("  用户 r0 = %.4f ⇒ θ_user = arctan(r0) = %.9f rad = %.4f × θ_A" %
        (r_user, theta_user, ratio_theta))
    put("  口径B（R29：tanθ = τ/κ = 1/α）⇒ θ_B = %.6f rad，r_B = %.3f" % (theta_B, r_B))

    rel_A = abs(r_user - r_A) / abs(r_A)
    if rel_A > 0.05:
        F("S1.1", "r0 = 0.0918 与公理 α^(-1)=2π/θ 不自洽",
          "公理给 θ=2πα=%.6f ⇒ r0=%.6f；用户值 0.0918 对应 θ=%.6f = %.4f×θ_A（≈4πα）。"
          "相对偏差 %.1f%%（≈2 倍因子），属公理读取的 2 倍漂移，不是舍入"
          % (theta_A, r_A, theta_user, ratio_theta, rel_A * 100.0),
          {"r_axiom": r_A, "r_user": r_user, "theta_ratio": ratio_theta})
    else:
        P("S1.1", "r0 与公理自洽", "偏差 %.2e" % rel_A)

    ratio_AB = r_B / r_A
    F("S1.2", "与 R29 口径（tanθ = τ/κ = 1/α）冲突约 %.0f 倍（%.1f 个量级）"
      % (ratio_AB, math.log10(ratio_AB)),
      "R29 交叉发现：白皮书'α = τ/κ'方向写反，实际 τ/κ ≈ 1/α ⇒ tanθ = 1/α = %.3f；"
      "而公理 A 给 tanθ = %.6f。二者相差 %.4g（≈%.1f 个量级），且 θ_A=%.4f rad 与 "
      "θ_B=%.4f rad 相差 %.1f 倍 ⇒ r0 存在**至少三套互不兼容的口径**（A/B/用户值）"
      % (r_B, r_A, ratio_AB, math.log10(ratio_AB), theta_A, theta_B, theta_B / theta_A),
      {"r_A": r_A, "r_B": r_B, "ratio": ratio_AB})

    I("S1.3", "固定点 r0 是**约定输入**而非导出量",
      "三套口径互差 2~2988 倍，且 TUFT 内无任何方程选定其一（R29 已证 τ/κ 由孤子解"
      "额外选定、稳态条件不约束比值）⇒ 把 r0 当作 RG 流的红外固定点是**外部锚定**，"
      "与 O-SCALE 最小锚定定理同构")

    # 后续统一用用户值 r0=0.0918（审计对象），同时给出 r_A 作对照
    return r_user, r_A


# ================================================================= §2 RG 流 ODE
def rg_exact(t, r_init, t_c, lam, dbeta, r0):
    """分段解析解（t_init = 0 > t_c；t 从 0 向 -60 走）。"""
    t = np.asarray(t, dtype=float)
    A = r_init - r0 + dbeta / lam
    rI = r0 - dbeta / lam + A * np.exp(lam * t)                 # t >= t_c
    r_tc = r0 - dbeta / lam + A * np.exp(lam * t_c)
    rII = r0 + (r_tc - r0) * np.exp(lam * (t - t_c))            # t <  t_c
    return np.where(t >= t_c, rI, rII), r_tc


def make_rhs(t_c, lam, dbeta, r0):
    def rhs(t, r):
        return lam * (r - r0) + (dbeta if t > t_c else 0.0)
    return rhs


def rk4_fixed(rhs, t_grid, r_init):
    r = np.empty_like(t_grid)
    r[0] = r_init
    for k in range(len(t_grid) - 1):
        t0, t1 = t_grid[k], t_grid[k + 1]
        h = t1 - t0
        k1 = rhs(t0, r[k])
        k2 = rhs(t0 + h / 2.0, r[k] + h * k1 / 2.0)
        k3 = rhs(t0 + h / 2.0, r[k] + h * k2 / 2.0)
        k4 = rhs(t1, r[k] + h * k3)
        r[k + 1] = r[k] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    return r


def s2_rg(r0):
    sec("§2  RG 流 ODE：解析解 / 数值解 / 跃变结构 / 符号判据")
    put("  方程：dr/dt = λ(r − r0) + Δβ_r·H(t − t_c)，  t = ln(μ/M_Pl)，t 增大 = 高能")
    put("  积分区间：t: 0（普朗克） → −60（低能）；r_init = 0.12；r0 = %.4f" % r0)

    r_init = 0.12
    t_c = -15.0
    t_grid = np.linspace(0.0, -60.0, 2001)

    # ---------- 2.1 符号判据：λ 的符号决定 IR 是否吸引 ----------
    put("")
    put("  [2.1] 用户声明 λ<0 为'红外吸引固定点'。实算检验（沿 t 递减方向积分）：")
    res_sym = {}
    for lam in (-1.0, +1.0):
        dbeta = 0.05
        _, _ = rg_exact(np.array([t_c]), r_init, t_c, lam, dbeta, r0)
        r_end = rg_exact(np.array([-60.0]), r_init, t_c, lam, dbeta, r0)[0][0]
        r_tc = rg_exact(np.array([t_c]), r_init, t_c, lam, dbeta, r0)[1]
        res_sym[lam] = (r_tc, r_end)
        put("        λ=%+.1f : r(t_c)=%.6e , r(−60)=%.6e" % (lam, r_tc, r_end))
    r_neg = res_sym[-1.0][1]
    r_pos = res_sym[+1.0][1]

    if abs(r_neg) > 1e6:
        F("S2.1", "λ<0 并非红外吸引，而是**指数发散**（符号错误）",
          "沿 t 减小方向，解 r(t)=r0+(r(t_c)−r0)e^{λ(t−t_c)}：λ<0 且 t−t_c<0 ⇒ 指数"
          "因子 e^{|λ||t−t_c|}→∞。实算 λ=−1 给 r(−60)=%.3e（相对 r0 放大 %.2e 倍）；"
          "λ=+1 才给 r(−60)=%.6f → r0（吸引）。用户'λ 负=红外吸引'与自身方程方向相反"
          % (r_neg, abs(r_neg / r0), r_pos),
          {"r_end_lam_neg": r_neg, "r_end_lam_pos": r_pos})
    else:
        B("S2.1", "λ<0 未发散（参数选取所致）", "r(-60)=%.3e" % r_neg)
    P("S2.1b", "正确符号为 λ>0（IR 吸引）",
      "λ=+1 实算 r(−60)=%.9f → r0=%.4f，相对偏差 %.2e；与'低能回归固定点'一致"
      % (r_pos, r0, abs(r_pos - r0) / abs(r0)))

    # ---------- 2.2 解析 vs 数值（λ=+1，正确符号） ----------
    lam, dbeta = 1.0, 0.05
    rhs = make_rhs(t_c, lam, dbeta, r0)
    r_ex, r_tc_ex = rg_exact(t_grid, r_init, t_c, lam, dbeta, r0)

    # (a) 分段 solve_ivp（在 t_c 处断开）
    seg1 = solve_ivp(rhs, (0.0, t_c), [r_init], t_eval=t_grid[t_grid >= t_c],
                     rtol=1e-10, atol=1e-12)
    seg2 = solve_ivp(rhs, (t_c, -60.0), [seg1.y[0][-1]], t_eval=t_grid[t_grid < t_c],
                     rtol=1e-10, atol=1e-12)
    r_split = np.concatenate([seg1.y[0], seg2.y[0]])
    err_split = float(np.max(np.abs(r_split - r_ex) / np.maximum(np.abs(r_ex), 1e-12)))

    # (b) 单段 solve_ivp（默认容差，直接跨过 t_c）
    one = solve_ivp(rhs, (0.0, -60.0), [r_init], t_eval=t_grid, rtol=1e-6, atol=1e-9)
    r_one = one.y[0]
    err_one = float(np.max(np.abs(r_one - r_ex) / np.maximum(np.abs(r_ex), 1e-12)))

    # (c) 固定步长 RK4（2000 步，t_c 不落在网格点上）
    r_rk4 = rk4_fixed(rhs, t_grid, r_init)
    err_rk4 = float(np.max(np.abs(r_rk4 - r_ex) / np.maximum(np.abs(r_ex), 1e-12)))

    put("")
    put("  [2.2] 解析解 vs 三种数值积分（λ=+1, Δβ=0.05, t_c=−15），逐点最大相对误差：")
    put("        (a) 分段 solve_ivp（t_c 处断开）      : %.3e" % err_split)
    put("        (b) 单段 solve_ivp 直接跨 t_c(rtol1e-6): %.3e" % err_one)
    put("        (c) 固定步长 RK4（2000 步）           : %.3e" % err_rk4)

    if err_split < 1e-6:
        P("S2.2", "解析解 = 分段数值积分（互为交叉验证）",
          "最大逐点相对误差 %.3e（机器/容差级）⇒ 解析分段解可用作真值基准" % err_split,
          {"err_split": err_split})
    else:
        F("S2.2", "解析解与分段数值积分不一致", "误差 %.3e" % err_split)

    worst = max(err_one, err_rk4)
    if worst > 1e-2:
        F("S2.3", "直接跨阶跃积分（JAX odeint 用法）产生显著误差",
          "单段积分最大相对误差 %.3e、固定步长 RK4 %.3e —— 因 odeint/RK 假设 RHS 光滑，"
          "而 H(t−t_c) 是不连续项，跨步时整步用错分支（误差 ~ Δβ·Δt），且自适应求解器"
          "在阶跃处步长塌缩、静默接受误差。正确做法 = 分段解析/分段积分（本册采用）"
          % (err_one, err_rk4),
          {"err_single_ivp": err_one, "err_rk4": err_rk4})
    else:
        B("S2.3", "本参数下跨阶跃积分未暴露显著误差（结构性风险仍在）",
          "单段 %.3e / RK4 %.3e：因 λ>0 的吸引子把段I的位移在 IR 端'遗忘'，终点误差被"
          "抹平；但 (i) λ<0 或 Δβ 更大时会被指数放大，(ii) 自适应求解器步长塌缩导致"
          "成本不可控。⇒ 结论是方法不可靠，不是本例碰巧通过" % (err_one, err_rk4),
          {"err_single_ivp": err_one, "err_rk4": err_rk4})

    # ---------- 2.3 跃变结构 ----------
    eps = 1e-6
    d_plus = lam * (r_tc_ex - r0) + dbeta
    d_minus = lam * (r_tc_ex - r0)
    jump = d_plus - d_minus
    # 辅助演示：靠近起点的 t_c2=-2（尚未饱和），左右导数差同样严格 = Δβ_r 且数值非零
    t_c2 = -2.0
    _, r_tc2 = rg_exact(np.array([t_c2]), r_init, t_c2, lam, dbeta, r0)
    d_plus2 = lam * (r_tc2 - r0) + dbeta
    d_minus2 = lam * (r_tc2 - r0)
    jump2 = d_plus2 - d_minus2
    put("")
    put("  [2.3] 一阶导数有限跳变（缺口定理 N 的核心非解析性）：")
    put("        t_c=−15（主演示，已饱和到 r*_UV）：(dr/dt)|+ = %+.6e , |− = %+.6e , 跳变 = %+.6e"
        % (d_plus, d_minus, jump))
    put("        t_c=−2 （未饱和对照）：           (dr/dt)|+ = %+.6e , |− = %+.6e , 跳变 = %+.6e"
        % (d_plus2, d_minus2, jump2))
    put("        两种情形跳变均严格 = Δβ_r = %.6f（与固定点饱和程度无关）" % dbeta)
    if abs(jump - dbeta) < 1e-12 * max(1.0, abs(dbeta)) and abs(r_tc_ex) < 1e3 \
            and abs(jump2 - dbeta) < 1e-12 * max(1.0, abs(dbeta)):
        P("S2.4", "缺口定理 N 的非解析性成立（一阶导数有限跳变 = Δβ_r）",
          "左右导数差在 t_c=−15 与 t_c=−2 两种情形下均为 %.6f = Δβ_r ⇒ 与固定点饱和程度"
          "无关，RG 流 C⁰ 非 C¹，满足'缺口=导数不连续'的形式定义" % dbeta,
          {"jump": jump, "jump2": jump2, "delta_beta": dbeta})
    else:
        F("S2.4", "跃变幅度与 Δβ_r 不符", "跳变 %.6f/%.6f vs Δβ %.6f" % (jump, jump2, dbeta))

    # ---------- 2.4 δ_TUFT 的显著区间宽度 ----------
    t_probe = np.array([0.0, -1.0, -3.0, -5.0, -10.0, -14.0, -15.5, -20.0, -40.0, -60.0])
    drdt = np.array([lam * (rr - r0) + (dbeta if tt > t_c else 0.0)
                     for tt, rr in zip(t_probe, rg_exact(t_probe, r_init, t_c, lam, dbeta, r0)[0])])
    relax = 3.0 / abs(lam)
    frac = relax / 60.0
    put("")
    put("  [2.4] δ_TUFT ∝ dr/dt 沿 t 的剖面（弛豫长度 1/|λ| = %.2f）：" % (1.0 / abs(lam)))
    for tt, dd in zip(t_probe, drdt):
        put("        t=%6.1f : dr/dt = %+.6e" % (tt, dd))
    B("S2.5", "'δ_TUFT 仅在 t≈t_c 附近显著'需 |λ| 足够大（非自动成立）",
      "Heaviside 是阶跃不是钟形：t>t_c 全程 dr/dt 非零，直到 r 饱和到新的固定点 "
      "r*_UV = r0 − Δβ/λ = %.6f。显著区间宽度 ≈ 3/|λ| = %.2f，占全区间 %.1f%%；"
      "|λ| 小（慢弛豫）时 δ_TUFT 在**整段高能区都活跃**，与'仅 t_c 附近'的物理论述不符"
      % (r0 - dbeta / lam, relax, frac * 100.0),
      {"relax_len": 1.0 / abs(lam), "window_frac": frac, "r_uv_star": r0 - dbeta / lam})

    return dict(r0=r0, lam=lam, dbeta=dbeta, t_c=t_c, r_init=r_init,
                err_split=err_split, err_one=err_one, err_rk4=err_rk4)


# ================================================================= §3 定理 N 冲突
def s3_theoremN(rg):
    sec("§3  与定理 N 实例化（β ≡ 0）的正面冲突判定")
    put("  既有结论（tuft_beta_running_缺口_定理N实例化，PASS5/FAIL2/BOUNDARY3/INFO4）：")
    put("    TUFT 耦合取几何比值 g = κ/τ（固定螺旋）⇒ κ,τ 为实常数 ⇒ β(g) ≡ 0，无能标跑动。")
    put("  本框架要求：dr/dt ≠ 0（r = tanθ 随 μ 演化）⇒ θ 随能标变 ⇒ κ/τ 随能标变。")
    F("S3.1", "本 RG 框架与'固定螺旋 β≡0'直接互斥",
      "β≡0 的固定点要求 dr/dt ≡ 0（∀t）；本框架的解在 t>t_c 段 dr/dt ≠ 0（实算 "
      "t=0 处 dr/dt = %+.3e）。二者只能取一：本框架等价于**放弃固定螺旋**，"
      "即打开定理 N 的 M3（尺度依赖几何）" % (rg["lam"] * (rg["r_init"] - rg["r0"]) + rg["dbeta"]),
      {"drdt_at_planck": rg["lam"] * (rg["r_init"] - rg["r0"]) + rg["dbeta"]})
    F("S3.2", "按定理 N，打开 M3 ⇒ 必须同时补 M1+M2 ⇒ 塌缩为 Yang–Mills",
      "定理 N：自造尺子需 M1(泛函量子化/cutoff) + M2(非阿贝尔自耦合) + M3(经典无尺度)；"
      "补齐三者后规范动力学即 Yang–Mills，螺旋退化为 F 的几何图像。"
      "本框架的 Δβ_r 与 λ 无 M1/M2 支撑，是**纯运动学注入**：给了一个跑动的形状，"
      "没给跑动的机制。启用它 = 承认 TUFT 是 [B] 级有效编码（与既有结论同构）")
    I("S3.3", "β 总函数的可算性边界",
      "用户写 β(g,t) = b0g³ + b1g⁵ + δ_TUFT(r(t))，δ_TUFT ∝ dr/dt："
      "SM 微扰项 b0/b1 是外部借用（非 TUFT 导出），δ_TUFT 又是自由参数"
      "⇒ 该式是**两源相加的现象学模板**，不是 TUFT 的耦合预言")


# ================================================================= §4 CMB 双谱公式与数据
def s4_cmb_formula():
    sec("§4  CMB 双谱层：公式结构与观测数据审计")

    # 4.1 局部型双谱标准式
    put("  标准局部型（Planck 约定）：")
    put("    ⟨ζ(k1)ζ(k2)ζ(k3)⟩ = (2π)³ δ³(Σk) B_ζ(k1,k2,k3)")
    put("    B_ζ = (6/5) f_NL [ P_ζ(k1)P_ζ(k2) + P_ζ(k2)P_ζ(k3) + P_ζ(k3)P_ζ(k1) ]")
    put("  用户式：B_ζ = 6 f_NL/(2π)² · ζ(k1)ζ(k2)ζ(k3)/(k1²k2²k3²) · δ³(Σk)")
    F("S4.1", "局部型双谱公式三处不成立",
      "(a) 因子：标准系数 6/5，用户写 6（差 5 倍）；(b) 左端是**系综平均** ⟨ζζζ⟩，"
      "右端写的是随机场实现 ζζζ —— 双谱是统计量不是场的确定函数，式子范畴错；"
      "(c) 幂次：P_ζ(k) ∝ k^(−3)（近标度不变 A_s k^(−3)），故 P(k1)P(k2) ∝ "
      "k1^(−3)k2^(−3)，用户写 (k1²k2²k3²)^(−1) ⇒ 幂次与量纲均不符（差 k^(−4)）",
      {"factor_ratio": 5.0})

    # 4.2 f_NL 基线数值
    put("")
    put("  用户代码：fnl_lcdm = −0.04（注释'Planck2018基线局部fNL'）")
    put("  Planck 2018 官方局域型：f_NL^local = %.1f ± %.1f（68%% CL，未探测）"
        % (FNL_LOCAL_OBS, FNL_LOCAL_SIG))
    F("S4.2", "f_NL 基线数值错误（−0.04 不是任何 Planck 值）",
      "Planck 2018 局域型 f_NL = −0.9 ± 5.1；等边 −26 ± 47；正交 −38 ± 24。"
      "−0.04 与官方值差绝对值 %.2f（相对中心值差 %.0f%%），且**符号与量级均无出处**，"
      "直接代入 χ² 会把模型基线整体偏移 0.86（≈ 0.17σ），虽小但属无来源数值"
      % (abs(-0.04 - FNL_LOCAL_OBS), abs((-0.04 - FNL_LOCAL_OBS) / FNL_LOCAL_OBS) * 100.0),
      {"planck_local": [FNL_LOCAL_OBS, FNL_LOCAL_SIG], "user_baseline": -0.04})

    # 4.3 逐 l 的 f_NL 观测是否存在
    put("")
    put("  χ² = Σ_{l∈Planck bins} (f_TUFT(l) − f_obs,l)²/σ_l²  需要**逐多极 l 的 f_NL 观测**。")
    F("S4.3", "Planck 不提供逐 l 的 f_NL(l) 观测序列（数据类型不存在）",
      "Planck 的 f_NL 是对**给定形状模板的单一全局振幅**的最佳拟合（温度+偏振联合 "
      "一个数字 + 一条误差），不是按 l 分箱的非高斯性测量；WMAP/Planck 的 "
      "f_NL(l) 类'逐多极'结果在官方 likelihood 中并不作为标准数据产品发布。"
      "⇒ 用户 χ² 所需的 obs_l / obs_fnl / obs_sigma 三数组**没有公开数据来源**")
    F("S4.4", "同族既有判据（V22·D2-3）已判该类 CMB 数据不可作检验基准",
      "TUFT_V22_三路联合拟合_可证伪性审计 D2-3：'Planck 2018 等边/局域型 f_NL 未探测"
      "（|f_NL| ≲ O(10) 上限内与 0 相容）… 数据集来源未标注且与公开结果冲突 ⇒ "
      "不可用作检验基准'。本册沿用该判据，不在无来源数据上构造 χ²")

    # 4.4 灵敏度预算（假设未来有逐 l 数据）
    put("")
    put("  [4.5] 假设性灵敏度预算（**仅作仪器/统计可行性估计，不代入真实观测**）：")
    for nb in (10, 20, 40, 100):
        n2 = nb / 2.0
        sd = FNL_LOCAL_SIG * math.sqrt(1.0 / n2 + 1.0 / n2)
        put("        分箱数 N=%3d（各半）⇒ σ(Δf_NL) = %.3f ，95%% 可探测阈值 |Δf| ≳ %.2f"
            % (nb, sd, 1.96 * sd))
    sd40 = FNL_LOCAL_SIG * math.sqrt(4.0 / 40.0)
    B("S4.5", "即便存在逐 l 数据，Planck 级误差下阶跃可探测阈值 ≈ %.1f（N=40 分箱）"
      % (1.96 * sd40),
      "σ(Δf) = σ_l·√(1/n₁+1/n₂)；Planck σ_l≈5.1 ⇒ N=40 时 σ(Δf)=%.2f，95%% 阈值 %.2f。"
      "即 TUFT 若预言 |Δf_NL| ≲ 3，即便有逐 l 数据也**分辨不出**；反之若 |Δf| ≳ 5 "
      "则早已被全局 f_NL 的单值测量排除。⇒ 该通道的可检验窗口被两头夹死"
      % (sd40, 1.96 * sd40),
      {"sigma_delta_f_N40": sd40, "threshold_95": 1.96 * sd40})


# ================================================================= §5 μ_c → l_c 映射
def s5_mapping():
    sec("§5  拓扑跃迁能标 μ_c → 临界多极 l_c 的映射可定性与可识别窗口")
    k_min = L_MIN / ETA0_MPC
    k_max = L_MAX / ETA0_MPC
    dlnk = math.log(k_max / k_min)
    # 暴胀能标（由 r 上限反推 H_inf）
    H_over_Mpl = math.pi * math.sqrt(A_S * R_TENSOR_MAX / 2.0)
    H_inf_gev = H_over_Mpl * M_PL_RED_GEV
    t_inf = math.log(H_over_Mpl)
    prior_width = 60.0
    hit = dlnk / prior_width

    put("  l ≈ k·η0，η0 ≈ %.0f Mpc ⇒ l∈[%g,%g] 对应 k∈[%.3e, %.3e] Mpc⁻¹"
        % (ETA0_MPC, L_MIN, L_MAX, k_min, k_max))
    put("  CMB 覆盖的共形波数跨度：Δln k = ln(k_max/k_min) = %.3f" % dlnk)
    put("  由 r < %.3f 反推 H_inf/M_Pl = %.3e ⇒ H_inf ≈ %.3e GeV ⇒ t_inf = %.2f"
        % (R_TENSOR_MAX, H_over_Mpl, H_inf_gev, t_inf))
    put("  （t = ln(μ/M_Pl)，故整个 CMB 观测窗口集中在 t ≈ %.1f 附近）" % t_inf)

    F("S5.1", "μ_c → k_c 的映射不可定（缺 reheating 历史）",
      "k_c = a(t_k)H(t_k) 的视界穿越条件需完整的 a(t) 演化（暴胀 e-folds N + 重加热史）。"
      "既有 tuft_暴胀CMB_全维求导精算已判 T_reh≈1e14 GeV 是'直接给定'（§5 FAIL）、"
      "N 与 n_s 需两个非物理自由度同时调节。ΔN 每差 1 个 e-fold ⇒ k_c 差 e 倍；"
      "reheating 不确定 ΔN ~ O(10) ⇒ l_c 不确定 ~ e^10 ≈ %.2e 倍 ⇒ **映射不可定**"
      % math.exp(10.0),
      {"delta_lnk": dlnk, "t_inf": t_inf, "H_inf_GeV": H_inf_gev})

    B("S5.2", "t_c 的可识别窗口仅占先验区间 %.1f%%（精细调节度量）" % (hit * 100.0),
      "RG 变量 t 的先验跨度 60（μ 跨 26 个量级），而 CMB 只覆盖 Δt ≈ Δln k = %.2f "
      "的一小段（中心 t≈%.1f）。若 t_c 均匀先验，落在可观测窗口的概率仅 %.1f%% ⇒ "
      "要做 CMB 检验必须先**假定 t_c 恰好落在 t_inf 附近**，这本身是一个新的自由假设"
      % (dlnk, t_inf, hit * 100.0),
      {"window": dlnk, "prior": prior_width, "hit_prob": hit})

    F("S5.3", "f_NL 跳变幅度 Δf_NL 与几何量 Δβ_r 之间无导出关系",
      "框架给了两条链：RG 侧 (t_c, Δβ_r) 与 CMB 侧 (l_c, Δf_NL)，但 (i) μ_c→l_c 无映射"
      "（S5.1），(ii) Δβ_r→Δf_NL 无任何方程 —— 拓扑跃迁如何进入原初三点函数、"
      "为何表现为**局域型**形状而非等边/正交/褶皱形状，全未给出。"
      "⇒ 两条链各自独立参数化，联合拟合没有物理连接，只是两个自由模型的并列")


# ================================================================= §6 采样器审计
def chi2_cmb(delta_f, l_c, l_obs, f_obs, sig, f_base):
    model = f_base + delta_f * (l_obs > l_c).astype(float)
    return float(np.sum(((model - f_obs) / sig) ** 2))


def profile_delta_f(l_c, l_obs, f_obs, sig, f_base):
    """对给定 l_c，Δf_NL 的加权最小二乘闭式解与标准差。"""
    m = (l_obs > l_c).astype(float)
    w = 1.0 / sig ** 2
    den = float(np.sum(w * m))
    if den <= 0.0:
        return 0.0, float("inf"), float("inf")
    num = float(np.sum(w * m * (f_obs - f_base)))
    dhat = num / den
    return dhat, 1.0 / math.sqrt(den), chi2_cmb(dhat, l_c, l_obs, f_obs, sig, f_base)


def s6_sampler():
    sec("§6  采样器审计：硬阶跃下 NUTS/HMC 的结构性失效与可运行的替代管线")
    rng = np.random.default_rng(SEED)

    n_bins = 40
    l_obs = np.linspace(60.0, 2440.0, n_bins)
    sig = np.full(n_bins, FNL_LOCAL_SIG)
    f_base = FNL_LOCAL_OBS
    l_c = l_obs[20]
    delta_f = 3.0

    # 合成观测（显式标注：合成数据，非 Planck 数据）
    f_obs = f_base + delta_f * (l_obs > l_c).astype(float)

    # ---- 6.1 硬阶跃的梯度性质：区间内恒零 + 分箱边界处不连续 ----
    l_probe = 0.5 * (l_obs[20] + l_obs[21])       # 探测点取在相邻两 bin 之间
    half = 0.5 * (l_obs[21] - l_obs[20])
    h_in = 0.1 * half                              # 不跨越任何 bin 边界
    h_out = 1.5 * half                             # 跨越 bin 边界

    def grad_lc(h):
        return (chi2_cmb(delta_f, l_probe + h, l_obs, f_obs, sig, f_base)
                - chi2_cmb(delta_f, l_probe - h, l_obs, f_obs, sig, f_base)) / (2.0 * h)

    g_in, g_out = grad_lc(h_in), grad_lc(h_out)
    put("  [6.1] χ² 对 l_c 的中心差分（探测点 l=%.1f，bin 半间距 %.1f）：" % (l_probe, half))
    put("        区间内 h=%.1f（不跨边界）⇒ ∂χ²/∂l_c = %.6e" % (h_in, g_in))
    put("        跨边界 h=%.1f            ⇒ ∂χ²/∂l_c = %.6e" % (h_out, g_out))
    if abs(g_in) < 1e-12:
        F("S6.1", "jnp.where 硬阶跃 ⇒ ∂χ²/∂l_c ≡ 0（梯度型采样器结构性失效）",
          "χ²(l_c) 是**分段常数**函数：只有当 l_c 跨过某个 bin 的 l 值才改变，区间内恒为"
          "常数 ⇒ 导数恒 0（实算 %.1e），在 bin 边界处**不连续**（跨边界差分 %.3e 是"
          "台阶跳变，不是导数）。后果：NUTS/HMC/MALA/Langevin 依赖梯度，对 l_c"
          "（以及 RG 侧的 t_c）**零梯度信息** ⇒ 后验看似'收敛'实则停在初值附近（假收敛），"
          "且链永远不会跨过 bin 边界去探索其它阶跃位置。JAX 的 jnp.where 只在选中分支"
          "回传梯度，阶跃对阈值的梯度是**结构零**，不是可数值改进的近似"
          % (g_in, g_out),
          {"grad_in": g_in, "grad_across": g_out})
    else:
        B("S6.1", "区间内梯度非零（与分段常数预期不符，需复核）",
          "h_in=%.1f ⇒ %.3e" % (h_in, g_in))

    # ---- 6.2 软化阶跃的两难 ----
    def chi2_soft(delta_f, l_c, w):
        z = np.clip(-(l_obs - l_c) / w, -40.0, 40.0)   # 防 exp 溢出
        s = 1.0 / (1.0 + np.exp(z))
        return float(np.sum(((f_base + delta_f * s - f_obs) / sig) ** 2))

    put("")
    put("  [6.2] sigmoid 软化 H_w(l)=(1+e^{−(l−l_c)/w})^{−1} 的梯度范数 vs 宽度 w：")
    rows = []
    for w in (200.0, 50.0, 10.0, 2.0, 0.5):
        hh = 1e-3 * max(w, 1e-6)
        g = (chi2_soft(delta_f, l_c + hh, w) - chi2_soft(delta_f, l_c - hh, w)) / (2 * hh)
        rows.append((w, g))
        put("        w=%7.1f : |∂χ²/∂l_c| = %.4e" % (w, abs(g)))
    B("S6.2", "软化阶跃：w 大则抹掉物理跳变、w 小则梯度退化（两难，非免费午餐）",
      "w=200 时模型退化为平滑过渡（不再是'阶跃'预言）；w=0.5 时梯度峰宽 ~w ⇒ "
      "NUTS 步长须 ≪ w 才不跳变，采样效率崩塌（等价于回到离散问题）。"
      "⇒ 软化只是把离散困难换成病态条件数，不解决问题",
      {"rows": rows})

    # ---- 6.3 网格边缘化 + 闭式 profile（本册给出的可执行修正） ----
    cands = 0.5 * (l_obs[:-1] + l_obs[1:])
    best = None
    for lc in cands:
        dh, sd, c2 = profile_delta_f(lc, l_obs, f_obs, sig, f_base)
        if best is None or c2 < best[2]:
            best = (lc, dh, c2, sd)
    # 数值最小化交叉验证
    from scipy.optimize import minimize_scalar
    num_opt = minimize_scalar(lambda x: chi2_cmb(x, best[0], l_obs, f_obs, sig, f_base),
                              bounds=(-50, 50), method="bounded")
    put("")
    put("  [6.3] 网格边缘化结果：l̂_c = %.1f（真值 %.1f），Δ̂f = %.4f（真值 %.4f）"
        % (best[0], l_c, best[1], delta_f))
    put("        闭式 Δ̂f = %.9f ；数值最小化 Δ̂f = %.9f ；差 %.2e"
        % (best[1], num_opt.x, abs(best[1] - num_opt.x)))
    if abs(best[1] - num_opt.x) < 1e-6 and abs(best[0] - l_c) < (l_obs[1] - l_obs[0]):
        P("S6.3", "网格边缘化 + 闭式 profile 恢复真值（可执行、可复跑）",
          "l_c 只有 N−1 个不同取值（阶跃位置在 bin 间），对每个候选 l_c 对 Δf 做加权"
          "线性最小二乘得闭式解；实算恢复 l̂_c=%.1f、Δ̂f=%.4f，与数值最小化一致（差 %.1e）"
          "⇒ 这是该模型的**正确估计方法**，不需要也不需要梯度采样器"
          % (best[0], best[1], abs(best[1] - num_opt.x)),
          {"l_hat": best[0], "df_hat": best[1]})
    else:
        F("S6.3", "网格边缘化未能恢复真值", "l̂_c=%.1f, Δ̂f=%.4f" % (best[0], best[1]))

    # ---- 6.4 纯 numpy Metropolis（numpyro 不可用时的等价 MCMC） ----
    n_step = 40000
    lc_cur = cands[len(cands) // 2]
    df_cur = 0.0
    cur = chi2_cmb(df_cur, lc_cur, l_obs, f_obs, sig, f_base)
    lc_samples = np.empty(n_step)
    df_samples = np.empty(n_step)
    acc = 0
    bin_w = l_obs[1] - l_obs[0]
    for k in range(n_step):
        # l_c: 离散随机游走（±1 个 bin）
        step = int(rng.integers(-3, 4))
        lc_new = lc_cur + step * bin_w
        lc_new = float(np.clip(lc_new, cands[0], cands[-1]))
        df_new = df_cur + rng.normal(0.0, 0.5)
        new = chi2_cmb(df_new, lc_new, l_obs, f_obs, sig, f_base)
        if math.log(rng.random()) < 0.5 * (cur - new):
            lc_cur, df_cur, cur = lc_new, df_new, new
            acc += 1
        lc_samples[k] = lc_cur
        df_samples[k] = df_cur
    burn = n_step // 5
    lc_post = lc_samples[burn:]
    df_post = df_samples[burn:]
    put("")
    put("  [6.4] 纯 numpy Metropolis（%d 步，burn %d，接受率 %.2f）："
        % (n_step, burn, acc / float(n_step)))
    put("        Δf_NL 后验均值 %.4f ± %.4f（真值 %.4f）"
        % (df_post.mean(), df_post.std(), delta_f))
    put("        l_c 后验中位数 %.1f（真值 %.1f）" % (np.median(lc_post), l_c))
    if abs(df_post.mean() - delta_f) < 0.5 and abs(np.median(lc_post) - l_c) < 3 * bin_w:
        P("S6.4", "离散随机游走 Metropolis 与网格边缘化一致（交叉验证通过）",
          "后验 Δf=%.3f±%.3f、l_c 中位 %.1f，与闭式解 (%.3f, %.1f) 一致 ⇒ "
          "本册给出的管线自洽；numpyro 版本应改用**离散 l_c 的枚举/边缘化**而非 NUTS"
          % (df_post.mean(), df_post.std(), np.median(lc_post), best[1], best[0]),
          {"post_df_mean": float(df_post.mean()), "post_df_std": float(df_post.std()),
           "post_lc_median": float(np.median(lc_post)), "acc_rate": acc / float(n_step)})
    else:
        B("S6.4", "Metropolis 与闭式解有偏差（离散游走混合不足）",
          "Δf 后验 %.3f±%.3f vs 闭式 %.3f；l_c %.1f vs %.1f"
          % (df_post.mean(), df_post.std(), best[1], np.median(lc_post), best[0]))

    # ---- 6.5 注入-恢复：区分「管线错误」与「灵敏度不足」 ----
    def scan_best(fo):
        best_lc, best_dh, best_sd, best_c2 = cands[0], 0.0, 1.0, 1e18
        tmax = 0.0
        for lc in cands:
            dh, sd, c2 = profile_delta_f(lc, l_obs, fo, sig, f_base)
            t = abs(dh) / sd if (sd > 0 and np.isfinite(sd)) else 0.0
            if t > tmax:
                tmax = t
            if c2 < best_c2:
                best_c2, best_lc, best_dh, best_sd = c2, lc, dh, sd
        return (best_lc, best_dh, best_sd, tmax)

    n_exp = 300
    sd40 = FNL_LOCAL_SIG * math.sqrt(4.0 / 40.0)   # 与 §4.5 灵敏度预算同源

    # (i) 零注入：标定多重比较（look-elsewhere）阈值 t95
    tmax0 = []
    for e in range(n_exp):
        noise = rng.normal(0.0, FNL_LOCAL_SIG, size=n_bins)
        fo = np.full(n_bins, f_base) + noise
        tmax0.append(scan_best(fo)[3])
    tmax0 = np.array(tmax0)
    t95 = float(np.quantile(tmax0, 0.95))
    fp_raw = float(np.mean(tmax0 > 1.96))
    fp_cal = float(np.mean(tmax0 > t95))

    put("")
    put("  [6.5] 零注入（Δf_true=0，%d 次）标定扫描阈值：" % n_exp)
    put("        未校准 1.96σ 的假发现率 = %.1f%% ；校准阈值 t95 = %.2f ⇒ 假发现率 %.1f%%"
        % (100 * fp_raw, t95, 100 * fp_cal))
    if fp_raw > 0.15 and fp_cal <= 0.10:
        F("S6.5", "网格搜索存在多重比较（look-elsewhere）膨胀，1.96σ 阈值不可用",
          "在 %d 个候选 l_c 上取最显著 ⇒ 零注入下 1.96σ'发现'率高达 %.1f%%（标称 5%%）；"
          "用零注入分布标定的 t95=%.2f 才恢复到 %.1f%% ⇒ 任何'检测到阶跃'的宣称"
          "必须用 t95 而非 1.96σ（条件于'最显著 l_c'会系统性放大 |Δ̂f|）"
          % (len(cands), 100 * fp_raw, t95, 100 * fp_cal),
          {"fp_raw": fp_raw, "t95": t95, "fp_calibrated": fp_cal})
    else:
        B("S6.5", "多重比较膨胀未显著", "raw %.3f t95 %.2f" % (fp_raw, t95))

    # (ii) 双信号场景：强信号检验管线、弱信号检验灵敏度
    scen = {}
    for df_true in (3.0, 8.0):
        hits = cov = det = 0
        hats = []
        for e in range(n_exp):
            noise = rng.normal(0.0, FNL_LOCAL_SIG, size=n_bins)
            fo = f_base + df_true * (l_obs > l_c).astype(float) + noise
            bb = scan_best(fo)
            if abs(bb[0] - l_c) < bin_w:
                hits += 1
            if abs(bb[1] - df_true) <= 1.96 * bb[2]:
                cov += 1
            if bb[3] > t95:
                det += 1
            hats.append(bb[1])
        hats = np.array(hats)
        scen[df_true] = dict(hit=hits / n_exp, cov=cov / n_exp, det=det / n_exp,
                             mean=float(hats.mean()), bias=float(hats.mean() - df_true))
        tag = "6.7" if abs(df_true - 3.0) < 1e-9 else "6.8"
        put("")
        put("  [%s] 注入 Δf_true=%.1f（%d 次）：l_c 命中 %.1f%% ，Δf 覆盖率 %.1f%% ，"
            % (tag, df_true, n_exp, 100 * hits / n_exp, 100 * cov / n_exp))
        put("        检出率（|t|>t95）= %.1f%% ；Δ̂f 均值 %.3f（偏差 %+.3f）"
            % (100 * det / n_exp, float(hats.mean()), float(hats.mean()) - df_true))

    a, b = scen[3.0], scen[8.0]
    if b["det"] > 0.8 and b["cov"] > 0.85:
        P("S6.6", "强信号场景（Δf=8）恢复达标 ⇒ 估计管线本身正确",
          "Δf=8：检出 %.0f%%、覆盖 %.0f%%、偏差 %+.3f ⇒ 网格+闭式 profile 的统计管线无误"
          % (100 * b["det"], 100 * b["cov"], b["bias"]),
          {"scen8": b})
    else:
        F("S6.6", "强信号场景仍未恢复 ⇒ 管线有误",
          "det=%.2f cov=%.2f bias=%+.3f" % (b["det"], b["cov"], b["bias"]))

    if a["det"] >= 0.95 and abs(a["bias"]) < 0.1:
        P("S6.7", "弱信号场景恢复达标",
          "det=%.2f cov=%.2f bias=%+.3f" % (a["det"], a["cov"], a["bias"]))
    else:
        B("S6.7", "弱信号（Δf=3≈2σ）检出有限且 Δ̂f 有向上选择偏差（非管线错误）",
          "Δf=3：检出 %.0f%%（恰在 1.96σ 阈值附近，本就非确定）、l_c 命中 %.0f%%（低，阶跃"
          "位置难定）、Δ̂f 均值偏差 %+.3f（条件于'最显著 l_c'使 |Δ̂f| 系统性偏大）。与 §4.5 "
          "灵敏度预算一致：N=40 分箱时 95%% 阈值 %.2f，Δf=3 恰在阈值之下 ⇒ 弱信号下"
          "'未被排除'与'被支持'难以区分；该偏差来自网格扫描的选择效应，已用 t95 校准部分修正"
          % (100 * a["det"], 100 * a["hit"], a["bias"], 1.96 * sd40),
          {"scen3": a})

    I("S6.8", "真实 Planck 数据下该模型不可识别（不是'待检验'而是'无数据可检验'）",
      "现有公开量只有单一 f_NL = −0.9 ± 5.1（一个数字）。在单一约束下，"
      "f_base 与 Δf_NL 完全简并（观测只约束 f_base + Δf·⟨step(l)⟩ 的一个组合），"
      "l_c 更不可识别 ⇒ 以**现有公开数据**该 CMB 通道不可检验。要做真检验必须拿到 "
      "Planck 官方 bispectrum likelihood（逐构型的模态分解），不是自造逐 l 数组")
    return best


# ================================================================= §7 QNM FDTD 骨架
def s7_qnm():
    sec("§7  并行分支：黑洞 QNM FDTD 骨架审计（与既有 R20/R23/R25/R26/R27/R28 对账）")

    # 7.1 有效势
    M = 1.0
    r = 3.0 * M
    f = 1.0 - 2.0 * M / r
    dfdr = 2.0 * M / r ** 2
    l = 2
    v_user = f * (l * (l + 1) / r ** 2 + dfdr / (2.0 * r))
    v_rw = f * (l * (l + 1) / r ** 2 - 6.0 * M / r ** 3)
    v_scalar = f * (l * (l + 1) / r ** 2 + 2.0 * M / r ** 3)
    put("  Schwarzschild（M=1），r=3M，l=2 处三种势的数值对比：")
    put("    用户式  V = f[l(l+1)/r² + (1/2r)f']  = %.6f" % v_user)
    put("    标准 RW  V = f[l(l+1)/r² − 6M/r³]    = %.6f  （引力扰动 s=2，axial）" % v_rw)
    put("    标准标量 V = f[l(l+1)/r² + 2M/r³]    = %.6f  （s=0）" % v_scalar)
    F("S7.1", "有效势既非 Regge–Wheeler 也非标量势（系数/自旋权未声明）",
      "(1/2r)f' = M/r³，用户式给 +1·M/r³；标准 RW（s=2）为 −6M/r³（**符号相反**），"
      "标量（s=0）为 +2M/r³。r=3M 处：用户 %.6f vs RW %.6f（差 %.0f%%）、vs 标量 "
      "%.6f（差 %.0f%%）⇒ 势属于 s 未声明、系数错误的第三种；用它的 QNM 谱无法与 "
      "GR 基线或 LIGO 残差对接" % (v_user, v_rw, abs((v_user - v_rw) / v_rw) * 100,
                                  v_scalar, abs((v_user - v_scalar) / v_scalar) * 100),
      {"v_user": v_user, "v_rw": v_rw, "v_scalar": v_scalar})

    # 7.2 伪代码矩阵的结构缺陷
    N = 60
    rstar = np.linspace(-50.0, 150.0, N)
    dr = rstar[1] - rstar[0]
    omega = 0.4
    mat = np.zeros((N, N))
    for n in range(1, N - 1):
        mat[n, n - 1] = 1.0 / dr ** 2
        mat[n, n] = -2.0 / dr ** 2 + omega ** 2 - v_user
        mat[n, n + 1] = 1.0 / dr ** 2
    det = float(np.linalg.det(mat))
    rank = int(np.linalg.matrix_rank(mat))
    put("")
    put("  [7.2] 按用户伪代码装配 N=%d 的矩阵（首尾行不填）⇒ det = %.3e ，rank = %d/%d"
        % (N, det, rank, N))
    if abs(det) < 1e-8 and rank < N:
        F("S7.2", "伪代码矩阵严格奇异（首末行全零）⇒ det ≡ 0，无任何判别力",
          "伪代码只对 n=1..N−2 填充，第 0 行与第 N−1 行**整行为零** ⇒ 矩阵必有零行,"
          "det ≡ 0（实算 %.3e，秩 %d/%d）。即便填满边界，把 ω² 放进对角后"
          "'求 det M(ω)=0'也只对**线性**特征值问题成立，而这里 ω 以 ω² 出现且"
          "边界条件是 ω 依赖的 ⇒ 是非线性特征值问题，一次 det 给不出复频率"
          % (det, rank, N),
          {"det": det, "rank": rank, "N": N})
    else:
        B("S7.2", "矩阵非奇异（与预期不符，需复核）", "det=%.3e rank=%d" % (det, rank))

    F("S7.3", "入射/出射波边界是 ω 依赖的 Robin 条件，不能省",
      "QNM 的正确边界：视界侧 Ψ ~ e^{−iω r*}（r*→−∞）、无穷远 Ψ ~ e^{+iω r*}"
      "（r*→+∞）⇒ 离散化后是 Ψ' = ∓iωΨ，系数含未知 ω ⇒ 非线性特征值问题；"
      "用固定 Dirichlet（Ψ=0）会把连续谱污染成箱模（见 R23：|Imω| ∝ 1/L 的箱模判据）")

    F("S7.4", "挠率势 V_torsion = T_B·e^{−r/3} 无导出、且该通道已被既有判定关闭",
      "(a) 形式唯象（指数是手写、量纲/系数无来源）；(b) T_B 本身无 TUFT 导出："
      "D2 挠率动力学仅 C2(Proca) 唯一健康且存在'尺度困境'（承载粒子 λ~1e−27 m vs "
      "宏观可探测 ≳0.1 m，冲突 26 量级）；D3 证 K_sat=1/l_P² 是手写普朗克锚定；"
      "(c) OPEN_v3 已对 σ_abs=0 反射壁给出 χ²=33.00(df=2)、p=6.8e−8、**联合排除 5.74σ**；"
      "OPEN_v4 证 TUFT 三尺度锚给出的壁在 1e−26 M / 1e−78 M，与可检验所需的 2.05 M "
      "差 26~78 量级 ⇒ **挠率/反射壁的 ringdown 新预言窗口已关闭**")

    I("S7.5", "不重复造轮子：QNM 应直接复用 R25/R26（Leaver 连分式）而非新造 FDTD",
      "既有路径与结论：R20（实频散射稳定；外向射击法求复 QNM 指数不稳定）、"
      "R23（Chebyshev 谱配点失败：QNM 两端指数增长 + 出波 BC ⇒ 退化为箱模，"
      "判据 |Imω|∝1/L）、R25/R26（Leaver 连分式，基模 0.373672−0.088962i，"
      "|Δ|=4.5e−7，唯一达成特征值级精度的路径）、R27（RW↔Zerilli SUSY 等谱）、"
      "R28（Kerr/Teukolsky 是 4 项递推，需 Nollert 广义连分式）。"
      "⇒ FDTD 只会重复 R20/R23 已记录的失败模式；正确增量 = 在 R25 Leaver 上加挠率势")


# ================================================================= §8 结论与优先级
def s8_priority(rg, best):
    sec("§8  参数自由度审计、优先级建议与诚实结论")

    n_free = {"t_c": "拓扑跃迁能标（RG 侧）",
              "Δβ_r": "RG 跳变幅度（RG 侧）",
              "λ": "线性斜率（RG 侧）",
              "r0": "低能固定点（口径 3 套，S1）",
              "Δf_NL": "CMB 跳变幅度（CMB 侧）",
              "l_c": "临界多极（CMB 侧）",
              "T_B": "背景挠率（QNM 侧）"}
    put("  自由参数清点（本框架引入、且 TUFT 内无导出方程的量）：")
    for k, v in n_free.items():
        put("    · %-6s %s" % (k, v))
    F("S8.1", "7 个自由参数 vs 0 条 TUFT 导出方程 ⇒ 预测力为零（特设模板）",
      "同族判据（OPEN5b）：'2 自由度拟合 2 观测量 ⇒ 特设且零预测力'。本框架更甚："
      "RG 侧 4 参数 + CMB 侧 2 参数 + QNM 侧 1 参数，彼此之间**无映射方程**"
      "（S5.1/S5.3）⇒ 不是'TUFT 预言 f_NL 阶跃'，而是'用一个阶跃模板拟合未来的数据'。"
      "任何观测结果（有跳变/无跳变/任意 l_c）都可通过调参复现 ⇒ **不可证伪**")

    F("S8.2", "自洽性校验四条（用户 §4）的逐条判定",
      "(1) t=t_c 有限跃变、非解析 —— **成立**（S2.4 PASS，纯数学）；"
      "(2) t≪t_c 退化为光滑流并趋于 r0 —— **仅在 λ>0 下成立**，用户声明的 λ<0 使 IR "
      "指数发散（S2.1 FAIL）；(3) t≫t_c 进入'高能拓扑相' —— **不成立**：解迅速饱和到 "
      "新固定点 r*_UV = r0 − Δβ/λ = %.6f，不是持续演化的新相，且无第二相的动力学"
      "（S2.5 BOUNDARY）；(4) 低能 δ_TUFT→0 与 No-Go III/VI 兼容 —— **成立**但代价是"
      "与定理 N 的 β≡0 实例化冲突（S3.1 FAIL）：整个 RG 流是外部注入"
      % (rg["r0"] - rg["dbeta"] / rg["lam"]))

    put("")
    put("  [优先级建议] 用户问：先做 numpyro 嵌套采样跑 CMB 后验，还是先完善 FDTD 边界？")
    put("   → **都不建议按原计划执行，建议按下列顺序**：")
    put("    P1（必做，纯方法、100%% 可完成）：把 CMB 分支的估计器从'NUTS 采样硬阶跃'")
    put("       改为'网格边缘化 + 闭式 profile'（S6.3/S6.4 已实跑通过）。在此之前跑")
    put("       numpyro 得到的后验是**假收敛**（S6.1：梯度恒零），属于错误结果而非进展。")
    put("    P2（必做，数据层）：确认不存在逐 l 的 f_NL 观测（S4.3），改用 (a) 合成数据")
    put("       注入-恢复做管线验证（S6.5 已完成），或 (b) Planck 官方 bispectrum")
    put("       likelihood 做真实检验 —— 后者是数据获取任务，不是代码任务。")
    put("    P3（降优先）：FDTD 分支**不新造**。既有 R25/R26 的 Leaver 连分式已达成")
    put("       1e−6 精度；R20/R23 已记录 FDTD/谱配点的两类失败模式；且挠率 ringdown")
    put("       通道的可检验窗口已被 OPEN_v3(5.74σ)/OPEN_v4(26~78 量级) 关闭（S7.4）。")
    put("       若坚持做，正确增量 = 在 R25 Leaver 递推中加入挠率势项，而非重写 FDTD。")
    put("    P4（若要保留 RG 框架）：必须显式声明它打开定理 N 的 M3 ⇒ 承认 [B] 级")
    put("       有效编码（S3.2），并把 λ 改号（S2.1）、把 r0 的口径统一（S1）。")
    B("S8.3", "本框架的定位：现象学模板，不是 TUFT 的可证伪预言",
      "数学层（ODE 是否有解、跃变是否成立、估计器是否收敛）是**可判定且本册已判定**的；"
      "物理层（Δβ_r、t_c、Δf_NL、l_c 的取值与相互映射）**全部是外部输入**。"
      "⇒ 即便 P1–P2 全部跑通，得到的也只是'阶跃模型在未来的拟合能力'，"
      "不构成对 TUFT 的检验；反之若未来观测到 f_NL 阶跃，也不能归功于 TUFT。")
    I("S8.4", "体系安全（与用户 §6.3 一致）",
      "两个预言通道（CMB 阶跃 / 挠率 ringdown）即便全部被否决，TUFT 的复张量几何与 "
      "EC 约束流形仍作为几何框架保留，仅拓扑跃迁与挠率预言被剔除 —— 本册同意该隔离原则，"
      "并补充：被剔除的是**数值框架层**，定理 N / β≡0 / O-SCALE 等既有边界结论不受影响")


# ================================================================= main
def main():
    t0 = time.time()
    put("")
    put("=" * 78)
    put("  TUFT-R31  缺口定理 N 的 RG 流数值框架 + CMB 双谱 MCMC + QNM FDTD 骨架")
    put("             —— 可导出性与可证伪性审计")
    put("=" * 78)
    put("  run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    put("  红线：数学自洽 != 实验证实。本报告只审计框架，不主张 TUFT 物理真实性；")
    put("        不修改任何既有脚本与理论方程。")

    s0_env()
    r0, r_A = s1_axiom()
    rg = s2_rg(r0)
    s3_theoremN(rg)
    s4_cmb_formula()
    s5_mapping()
    best = s6_sampler()
    s7_qnm()
    s8_priority(rg, best)

    sec("汇总")
    put("  PASS     = %d" % COUNTS["PASS"])
    put("  FAIL     = %d" % COUNTS["FAIL"])
    put("  BOUNDARY = %d" % COUNTS["BOUNDARY"])
    put("  INFO     = %d" % COUNTS["INFO"])
    put("  ── 核心结论 ──")
    put("  · 用户原型中的硬缺陷（已实算定位）：r0=0.0918 与公理差 2 倍且与 R29 口径差 3 量级；")
    put("    λ<0 不是红外吸引而是指数发散（应为 λ>0）；jnp.where 硬阶跃使 ∂χ²/∂l_c≡0 ⇒")
    put("    NUTS 假收敛；FDTD 伪代码矩阵首末行全零 ⇒ det≡0 无判别力；有效势非 RW 非标量。")
    put("  · CMB 通道：**不存在 Planck 逐 l 的 f_NL 观测**（V22·D2-3 已判同类数据不可作基准）；")
    put("    正确估计器 = 网格边缘化 + 闭式 profile（已实跑通过，注入-恢复覆盖率达标）。")
    put("  · QNM 通道：挠率/反射壁窗口已被 OPEN_v3(5.74σ) 与 OPEN_v4(26~78 量级) 关闭；")
    put("    ⇒ 复用 R25/R26 Leaver，不新造 FDTD。")
    put("  · 可导出性：7 自由参数 / 0 条导出方程，两侧无映射 ⇒ 现象学模板，不可证伪。")
    put("")
    put("红线声明：数学自洽 != 实验证实。本册为框架审计，不主张 TUFT 物理真实性。")

    text = "\n".join(OUT) + "\n"
    try:
        with open(REPORT_TXT, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_TXT)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))

    payload = {
        "script": os.path.basename(__file__),
        "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "seed": SEED,
        "counts": COUNTS,
        "items": ITEMS,
        "elapsed_sec": time.time() - t0,
        "red_line": "数学自洽 != 实验证实",
    }
    try:
        with open(REPORT_JSON, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print("[OK] 明细已写入 " + REPORT_JSON)
    except Exception as exc:
        print("[warn] json 写入失败: " + str(exc))


if __name__ == "__main__":
    main()
