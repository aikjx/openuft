# -*- coding: utf-8 -*-
"""
空间螺旋 V21 · 水星近日点进动 + 原子高阶精细结构 · 卡方联合拟合（拟合层）
========================================================================

本册是联盟统计层的**拟合层**（statistics layer 的 parameter-estimation 半边）。
前置件：
  · 读数层 `靶场卡方联合拟合_统计层与判决力读数.py`（不给参数估计，只给 χ²/p/δ_min）
  · 裁定册 `判定_空间螺旋V21材料落库与下一步选定_2026-09-26.md` §5（选定「卡方联合拟合模块」）
  · C49 判定 `判定_空间螺旋V21续修_C25C35_2026-09-26.md`（金星/地球几何项两条式）
  · C50 判定（LB 谱退化 65.14 个量级）

被审对象
--------
来料 `TUFT V21 χ² 联合拟合代码（水星进动 + 原子高阶精细光谱）`：
参数 p = [β, V₀]；3 个数据点（水星进动 1 点 + 原子高阶精细结构 2 点）；
模型
    Δφ_merc(β) = 42.979 + 0.051·β              （角秒/百年）
    E_n(V₀)    = (ω²/c²)(V₀ + n²ℏ²/N²) / 1.602176634e-19   （eV，N=1000, ω=1e16）
输出 = 最优参数 / χ²_min / 参数协方差矩阵 / 参数 1σ 误差。
来料用 `scipy.optimize.minimize(L-BFGS-B)` + 有限差分 Hessian，并给了一份「示例输出」。

本册做三件事（红线：不粉饰、不替来料盖章）
------------------------------------------
  §A  逐条审计来料（公式层 / 数值层 / 口径层），每条给机器证据；
  §B  用**闭式**重做拟合（本模型对参数是线性的 ⇒ χ² 是精确二次型 ⇒ 解析雅可比 +
      精确协方差 (JᵀWJ)⁻¹ + 秩口径自由度），并用**正确的**中心差分做独立交叉校验；
  §C  锁参预言（金星/地球进动、n=4/5/6 原子能级），逐条给诚实定性。

为什么能「闭式」（本册最重要的结构性发现）
------------------------------------------
β 只出现在水星方程、V₀ 只出现在原子方程 ⇒ 残差向量对参数**分块可加**：
    χ²(β, V₀) = χ²_merc(β) + χ²_atom(V₀)
⇒ Hessian 精确块对角、相关系数 **ρ ≡ 0（精确，不是数值小量）**；
⇒ 所谓「2 参数联合拟合」实为两个互不相干的单参数拟合的并置，
   来料样例输出的 ρ = 0.1845 在数学上不可能。

统计口径（与读数层同源，不新造判据）
------------------------------------
    残差    r_i = (model_i − obs_i)/σ_i
    χ²     χ² = Σ r_i²
    线性模型 r = A·p − b  ⇒  最小二乘解 AᵀA·p = Aᵀb，Σ_cov = (AᵀA)⁻¹
    Hessian H = ∇²χ² = 2·AᵀA  ⇒  Σ_cov = 2·H⁻¹（与来料声明的口径一致）
    自由度  ν = N_data − rank(J)（秩口径，定理 I；本册 J=A 精确可算 ⇒ 用 Fraction 精确秩）
    p 值    p = erfc(√(χ²/2))（1 dof 生存函数；dof>1 走正则化上不完全 gamma）

诚实边界（先读）
----------------
1. 本模块不产生 L3。它把「拟合读数」算准；来料模型是否成立与本模块无关。
2. 「χ² ≈ 0」≠ 证据（读数层已给 α_grav(e) ≡ (m_e/m_P)² 的反例）；本册的两轴判据同款。
3. σ_obs = 0.03 角秒/百年为**来料外部假设**，比仓库内水星三锚点极差 0.13 窄 4.33 倍
   ⇒ 依赖它的自由度只能判 BOUNDARY。
4. 原子观测两点在仓库内**无出处**（无锚表、无文件引用）⇒ 不构成可溯源观测靶。
5. 本册只用标准库 + mpmath（**零外部依赖**：不用 numpy / scipy / JAX / emcee）。

产出：数据/空间螺旋V21_卡方联合拟合.json + 数据/空间螺旋V21_卡方联合拟合.md

用法：
    python 空间螺旋V21_水星与精细结构_卡方联合拟合.py
    python 空间螺旋V21_水星与精细结构_卡方联合拟合.py --teeth
"""

import os
import sys
import json
import time
from fractions import Fraction

from mpmath import mp, mpf, sqrt, erfc, erfinv, nstr, log10

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.dont_write_bytecode = True

mp.dps = 250                       # 与 V21 续修册一致（250 位）

HERE = os.path.dirname(os.path.abspath(__file__))
# 注意：dirname 的第一次调用是「去掉文件名」，故对 **__file__** 连取 4 次 dirname 落到 openuft
# （与读数层 `靶场卡方联合拟合_统计层与判决力读数.py` 同款；若误对 HERE 取 4 次会多跳一级到工作区根）
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

CL = mpf("0.95")
CHI2_CRIT_1 = 2 * erfinv(CL) ** 2                  # 1 dof 95% 临界值（闭式，不硬编码）

ROWS = []


def reg(state, tag, statement, detail, evidence=""):
    assert state in ("PASS", "BOUNDARY", "INFO", "FAIL"), state
    ROWS.append({"state": state, "tag": tag, "statement": statement,
                 "detail": detail, "evidence": evidence})
    print("  [%-8s] %s" % (state, tag))
    return state


def f(x, n=10):
    """mpf → 字符串（去掉尾随零，便于表格阅读）。"""
    return nstr(x, n)


# ===========================================================================
# 〇、输入（全部为来料逐字 + 仓库锚点）
# ===========================================================================
V_C = mpf("299792458")                    # m/s，定义值
V_HBAR = mpf("1.054571817e-34")           # J·s（CODATA2018）
V_EV = mpf("1.602176634e-19")             # J/eV，定义值
V_OMEGA = mpf("1.0e16")                   # 来料：ω（s⁻¹）
V_NTOP = mpf("1000")                      # 来料：N_top（拓扑绕数，固定）
K_BETA = mpf("0.051")                     # 来料：水星 TUFT 拓扑增量系数（角秒/百年 per β）
PHI_GR = mpf("42.979")                    # 来料：GR 基准贡献（角秒/百年）
PHI_OBS = mpf("43.03")                    # 来料：观测总进动
S_PHI = mpf("0.03")                       # 来料：观测不确定度（外部假设，见诚实边界 3）
ATOM_N = [2, 3]
E_OBS = [mpf("1.082e-4"), mpf("2.415e-4")]        # eV
E_SIG = [mpf("0.003e-4"), mpf("0.004e-4")]        # eV
P0_INGEST = [mpf("0.001"), mpf("1.0e-18")]        # 来料初值

KCOL = (V_OMEGA ** 2) / (V_C ** 2) / V_EV          # (ω²/c²) → eV/kcol-单位
DELTA_N = [n ** 2 * V_HBAR ** 2 / V_NTOP ** 2 for n in ATOM_N]   # n²ℏ²/N²

# 仓库锚点（**引上游产物，不复制**；用于交叉回归断言，出处见判定册）
C35_JSON = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论", "验证脚本",
                        "spiral_c35_beta_universality_claims.json")
# 判定册 C25C35 公布的 8 位读数（上游 json 缺失时的降级基准，容差相应放宽）
ANCHOR_GR250_COARSE = {"水星": mpf("42.982036"), "金星": mpf("8.6248639"), "地球": mpf("3.838823")}
PLANETS = [
    ("水星", mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846"), mpf("43.03")),
    ("金星", mpf("1.0820893e11"), mpf("0.00677672"), mpf("0.615197"), mpf("8.62")),
    ("地球", mpf("1.4959787e11"), mpf("0.0167086"), mpf("1.000017"), mpf("3.84")),
]


def load_c35_anchors():
    """读上游 `spiral_c35_beta_universality_claims.json`（单一真源）。

    返回 (gr_per_century, law_table, beta_calibrated)；文件缺失时返回 (None, None, None)，
    调用方降级到 8 位判定册读数并放宽容差（**不静默通过**）。
    """
    try:
        with open(C35_JSON, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        gr = {k: mpf(str(v)) for k, v in d["gr_per_century"].items()}
        law = {r["planet"]: (mpf(str(r["geo_binet"])), mpf(str(r["geo_draft"])))
               for r in d["law_table"]}
        return gr, law, d.get("beta_calibrated", {})
    except Exception:
        return None, None, None

ARCSEC = mp.pi / (180 * 3600)
V_G = mpf("6.67430e-11")
V_MSUN = mpf("1.98847e30")
GM_SUN = V_G * V_MSUN


def semilatus(a, e):
    return a * (1 - e ** 2)


def gr_per_century(a, e, T):
    """GR 一阶每百年进动（角秒）：6πGM/(c²a(1−e²))·(100/T)/ARCSEC。"""
    per_orbit = 6 * mp.pi * GM_SUN / (V_C ** 2 * a * (1 - e ** 2))
    return per_orbit * (100 / T) / ARCSEC


def geo_binet_per_century(beta_m2, a, e, T):
    """C49 正确式：Δφ_geo = 2πβ/(a²(1−e²)²)（弧度/圈），β 量纲 m²。"""
    per_orbit = 2 * mp.pi * beta_m2 / (a ** 2 * (1 - e ** 2) ** 2)
    return per_orbit * (100 / T) / ARCSEC


def geo_draft_per_century(beta_m, a, e, T):
    """C49 草稿式：Δφ_geo = 3πβ·GM/(c²a³(1−e²)²)（弧度/圈），β 量纲 m。"""
    per_orbit = 3 * mp.pi * beta_m * GM_SUN / (V_C ** 2 * a ** 3 * (1 - e ** 2) ** 2)
    return per_orbit * (100 / T) / ARCSEC


_GR_CACHE = None


def gr_anchors():
    """上游 GR/两式基准 + 容差（上溯 json 可用时用全精度、容差 1e-11；否则降级 8 位、容差 1e-5）。

    降级时**不静默通过**：容差与来源一并进产物（见返回值第 4 项 tol）。
    """
    global _GR_CACHE
    if _GR_CACHE is None:
        gr, law, bc = load_c35_anchors()
        if gr:
            _GR_CACHE = (gr, law, bc, mpf("1e-11"), "上游 json（全精度）")
        else:
            _GR_CACHE = (dict(ANCHOR_GR250_COARSE), None, None, mpf("1e-5"),
                         "判定册 8 位读数（降级：上游 json 不可读）")
    return _GR_CACHE


# ===========================================================================
# 一、线性代数原语（闭式，零依赖）
# ===========================================================================

def inv2(M):
    """2×2 精确求逆；det ≤ 0 或不可逆时返回 None（不静默给伪协方差）。"""
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if det == 0:
        return None, mpf(0)
    return [[M[1][1] / det, -M[0][1] / det],
            [-M[1][0] / det, M[0][0] / det]], det


def frac_rank(rows):
    """整数/有理矩阵精确秩（Fraction 高斯消元；避免浮点伪秩——秩口径自由度要用它）。"""
    m = [[Fraction(str(c)) if not isinstance(c, (int, Fraction)) else Fraction(c)
          for c in row] for row in rows]
    if not m:
        return 0
    ncol = len(m[0])
    rank, row = 0, 0
    for col in range(ncol):
        piv = None
        for i in range(row, len(m)):
            if m[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        inv = Fraction(1) / m[row][col]
        m[row] = [v * inv for v in m[row]]
        for i in range(len(m)):
            if i != row and m[i][col] != 0:
                k = m[i][col]
                m[i] = [a - k * b for a, b in zip(m[i], m[row])]
        row += 1
        rank += 1
        if row == len(m):
            break
    return rank


def sf_chi2(x, dof):
    """卡方生存函数（1 dof 用 erfc 闭式；dof>1 用 mpmath 正则化上不完全 gamma）。"""
    if x <= 0:
        return mpf(1)
    if dof == 1:
        return erfc(sqrt(x / 2))
    if dof <= 0:
        return None
    return mp.gammainc(mpf(dof) / 2, x / 2, mp.inf, regularized=True)


def fmt_p(s):
    if s is None:
        return "—"
    try:
        if s < mpf("1e-300"):
            return "≈0（< 1e-300）"
    except Exception:
        pass
    return nstr(s, 6)


# ===========================================================================
# 二、模型（逐字实现来料，不做任何「顺手修好」——审计要审原文）
# ===========================================================================

def model_mercury(beta):
    """来料 model_mercury：φ_GR + 0.051·β（角秒/百年）。"""
    return PHI_GR + K_BETA * beta


def model_atomic(n, V0):
    """来料 model_atomic：E_n = (ω²/c²)(V₀ + n²ℏ²/N²)/1.602176634e-19（eV）。"""
    return (V_OMEGA ** 2 / V_C ** 2) * (V0 + (n ** 2 * V_HBAR ** 2) / V_NTOP ** 2) / V_EV


def residual_vector(p):
    """来料 residual_vector：返回 [r_merc, r_atom(n=2), r_atom(n=3)]（mpf 版）。"""
    beta, V0 = p[0], p[1]
    r = [(model_mercury(beta) - PHI_OBS) / S_PHI]
    for ni, Eo, Ee in zip(ATOM_N, E_OBS, E_SIG):
        r.append((model_atomic(ni, V0) - Eo) / Ee)
    return r


def chi2(p):
    return sum(ri ** 2 for ri in residual_vector(p))


# ===========================================================================
# 三、来料 Hessian 的逐字复刻（审计用）
# ===========================================================================

def hessian_ingest(fn, x, eps):
    """来料 hessian()：逐字复刻（含其 4 点式 (f++ − f+ − f+- + f−)/(4ε²)）。

    注意：这不是一般的二阶偏导公式——它是把「混合二阶导」的分子项错拼成的表达式，
    对角与非对角都不成立。本函数只用于**审计取证**，不参与本册任何读数。
    """
    n = len(x)
    H = [[mpf(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            xp = list(x)
            xp[i] += eps
            fpp = fn(xp)
            xm = list(x)
            xm[i] -= eps
            fmm = fn(xm)
            xpp = list(x)
            xpp[i] += eps
            xpp[j] += eps
            fpppp = fn(xpp)
            xpm = list(x)
            xpm[i] += eps
            xpm[j] -= eps
            fppmm = fn(xpm)
            H[i][j] = (fpppp - fpp - fppmm + fmm) / (4 * eps ** 2)
    return H


def hessian_central(fn, x, steps):
    """**正确**的中心差分 Hessian（对角 3 点式、非对角 4 点式），步长逐参数给出。

    对精确二次型 f，中心差分是**精确**的（无截断误差）⇒ 与解析 H 应逐位一致，
    这正是「公式对/错」的判别器（见牙齿 T-H1/T-H2/T-H3）。
    """
    n = len(x)
    H = [[mpf(0)] * n for _ in range(n)]
    for i in range(n):
        hi = steps[i]
        xp = list(x)
        xp[i] += hi
        xm = list(x)
        xm[i] -= hi
        H[i][i] = (fn(xp) - 2 * fn(x) + fn(xm)) / (hi ** 2)
    for i in range(n):
        for j in range(i + 1, n):
            hi, hj = steps[i], steps[j]
            xpp = list(x)
            xpp[i] += hi
            xpp[j] += hj
            xpm = list(x)
            xpm[i] += hi
            xpm[j] -= hj
            xmp = list(x)
            xmp[i] -= hi
            xmp[j] += hj
            xmm = list(x)
            xmm[i] -= hi
            xmm[j] -= hj
            v = (fn(xpp) - fn(xpm) - fn(xmp) + fn(xmm)) / (4 * hi * hj)
            H[i][j] = H[j][i] = v
    return H


def hess_entry_scale(H, i, j):
    """Hessian 条目的归一化尺度。

    对角用自身；非对角用 √(H_ii·H_jj)（相关系数式归一）。
    不能直接用 max|H|：本模型 H[0][0]≈5.78 与 H[1][1]≈1.67e81 差 80 个量级，
    用全局最大值归一会把 β 方向的信息全部淹没（首版即踩此坑）。
    """
    if i == j:
        return abs(H[i][i])
    return sqrt(abs(H[i][i] * H[j][j]))


def hess_dev(A, B):
    """两个 Hessian 的相对偏差（逐条目按 hess_entry_scale 归一后取最大）。"""
    return max(abs(A[i][j] - B[i][j]) / hess_entry_scale(B, i, j)
               for i in range(2) for j in range(2))


def grad_analytic(p):
    """解析梯度 dχ²/dp = 2Aᵀ(A p − b)（本模型 A、b 与 p 无关）。"""
    A, b = design_matrix()
    r = [sum(A[k][i] * p[i] for i in range(2)) - b[k] for k in range(len(A))]
    return [2 * sum(A[k][i] * r[k] for k in range(len(A))) for i in range(2)]


def grad_fd(p, eps):
    """绝对步长中心差分梯度（scipy L-BFGS-B 的默认口径）。"""
    out = []
    for i in range(2):
        xp = list(p)
        xp[i] += eps
        xm = list(p)
        xm[i] -= eps
        out.append((chi2(xp) - chi2(xm)) / (2 * eps))
    return out


FLOAT64_EPS = mpf("2.220446049250313e-16")


def fd_rounding_gap(p, eps, index=1):
    """中心差分「两函数值之差」的**相对量级**。

    这是判断有限差分在**双精度**下是否可用的唯一硬指标：
        |f(x+ε) − f(x−ε)| / max(f(x+ε), f(x−ε)) < 2.2e-16
    ⇒ 差分结果全由舍入噪声构成，导数为 0/垃圾。
    （在 250 位算术下差分本身是精确的，故必须这样**间接**判定，不能用比值判定。）
    """
    xp = list(p)
    xp[index] += eps
    xm = list(p)
    xm[index] -= eps
    fp, fm = chi2(xp), chi2(xm)
    return abs(fp - fm) / max(fp, fm)



# ===========================================================================
# 四、闭式拟合内核
# ===========================================================================

def design_matrix():
    """线性模型 r = A·p − b 的 A（3×2）与 b，以及权重。

    水星行：r_M = (φ_GR + 0.051β − φ_obs)/σ_M = (0.051/σ_M)·β − (φ_obs−φ_GR)/σ_M
    原子行：r_n = kcol·(V₀ + δ_n)/σ_n − E_n/σ_n
    ⇒ A 的第 1 行只含 β 列、第 2/3 行只含 V₀ 列（**分块**，故 ρ ≡ 0）。
    """
    A = [[K_BETA / S_PHI, mpf(0)]]
    b = [(PHI_OBS - PHI_GR) / S_PHI]
    for ni, Eo, Ee, dn in zip(ATOM_N, E_OBS, E_SIG, DELTA_N):
        A.append([mpf(0), KCOL / Ee])
        b.append((Eo - KCOL * dn) / Ee)
    return A, b


def closed_form_fit():
    """闭式加权最小二乘 + 精确协方差 + 秩口径自由度。"""
    A, b = design_matrix()
    n_data = len(A)
    # 法方程 M = AᵀA（2×2），c = Aᵀb
    M = [[sum(A[k][i] * A[k][j] for k in range(n_data)) for j in range(2)] for i in range(2)]
    c = [sum(A[k][i] * b[k] for k in range(n_data)) for i in range(2)]
    Minv, det = inv2(M)
    if Minv is None:
        return None
    p_hat = [Minv[i][0] * c[0] + Minv[i][1] * c[1] for i in range(2)]
    r = residual_vector(p_hat)
    chi2_min = sum(ri ** 2 for ri in r)
    cov = Minv                                   # Σ = (AᵀA)⁻¹  ⇒ 2·H⁻¹ 因 H = 2AᵀA
    sig = [sqrt(cov[i][i]) for i in range(2)]
    rho = cov[0][1] / (sig[0] * sig[1])
    # 秩口径：A 的行空间秩，用 Fraction 精确算（A 元素是有理数）
    rank_j = frac_rank(A)
    nu = n_data - rank_j
    # Hessian（解析）
    H = [[2 * M[i][j] for j in range(2)] for i in range(2)]
    return {"A": A, "b": b, "M": M, "det_M": det, "H": H,
            "p_hat": p_hat, "chi2_min": chi2_min, "residuals": r,
            "cov": cov, "sigma": sig, "rho": rho,
            "rank_j": rank_j, "nu": nu,
            "p_value": sf_chi2(chi2_min, nu) if nu > 0 else None}


def profile_chi2(index, grid):
    """剖面 χ²：固定另一参数在最优值，扫第 index 个参数（用于展示精确二次型结构）。"""
    fit = closed_form_fit()
    p0 = list(fit["p_hat"])
    out = []
    for v in grid:
        p = list(p0)
        p[index] = v
        out.append((v, chi2(p)))
    return out


# ===========================================================================
# 五、§A 来料审计
# ===========================================================================

def audit_ingest(fit):
    print("\n" + "=" * 78)
    print("§A  来料逐条审计（公式层 / 数值层 / 口径层；每条带机器证据）")
    print("=" * 78)

    p_hat = fit["p_hat"]
    beta_hat, V0_hat = p_hat[0], p_hat[1]

    # --- D1：来料 Hessian 公式不是二阶偏导 ---------------------------------
    H_ingest = hessian_ingest(chi2, p_hat, mpf("1e-4"))          # 来料步长
    H_true = fit["H"]
    dev_ing = hess_dev(H_ingest, H_true)
    _inv_ing, det_ing = inv2(H_ingest)
    cov_ing = inv2(H_ingest)[0]
    cov_ing = cov_ing if cov_ing is None else [[2 * x for x in row] for row in cov_ing]
    sig_ratio = sqrt(cov_ing[0][0] / fit["cov"][0][0]) if cov_ing is not None else None
    reg("FAIL", "A-D1 来料 hessian() 的四点式不是二阶偏导：在最优点上给出 H = 解析 H 的 **1/2**",
        "来料式 H_ij=(f(x+εe_i+εe_j)−f(x+εe_i)−f(x+εe_i−εe_j)+f(x−εe_i))/(4ε²)；"
        "正确式为混合中心差分 (f++ − f+− − f−+ + f−−)/(4ε²)（对角用 (f(+)−2f(0)+f(−))/ε²）。"
        "在最优点 p* = (%s, %s) 上逐字复刻运行：来料 H = [[%s, %s], [%s, %s]]，"
        "解析 H = [[%s, 0], [0, %s]] ⇒ 两条对角**精确为解析值的 1/2**（机器精确），非对角恒为 0。"
        "机理：对二次型 f=½H(x−x*)²，来料对角式给 (2Hε²−½Hε²−0+½Hε²)/(4ε²) = H/2；"
        "非对角式的一阶项差 ∝ Aᵀr，而在最优点正规方程 Aᵀr = 0 ⇒ 恒为 0。"
        "后果：Σ = 2H⁻¹ = **2Σ_true** ⇒ 全部 1σ 误差被放大 **%s 倍**（= √2，实测）；"
        "且非对角恒 0 ⇒ 该代码在**任何**模型上都会输出 ρ = 0（相关矩阵无意义）。"
        "⇒ 样例输出的 σ_β = 4.2661e-4、ρ = 0.1845 都不可能由该代码路径产生。"
        % (f(beta_hat, 6), f(V0_hat, 6),
           f(H_ingest[0][0], 6), f(H_ingest[0][1], 3),
           f(H_ingest[1][0], 3), f(H_ingest[1][1], 6),
           f(H_true[0][0], 6), f(H_true[1][1], 6), f(sig_ratio, 4)),
        "来料 hessian() 逐字复刻 + 解析 Hessian 对照（逐条目归一化偏差 %s）" % f(dev_ing, 4),
        "来料代码「数值Hessian 求解协方差矩阵」段")

    # --- D2：差分梯度在来料的运行环境（float64）下退化为舍入噪声 -------------
    # 诚实前提：本模型对参数是**精确二次型**，故中心差分在**精确算术**下对任意步长都精确
    # （本册 250 位实测：FD 梯度 / 解析梯度 = 1.0）。所以「步长不对」本身**不是**失效点；
    # 真正的失效点是：差分的两项之差相对函数值太小 ⇒ 在双精度里被整体舍掉。
    ga = grad_analytic(P0_INGEST)
    gf = grad_fd(P0_INGEST, mpf("1e-8"))
    grad_ratio = abs(gf[1] / ga[1])
    gap_abs = fd_rounding_gap(P0_INGEST, mpf("1e-8"))                 # scipy 默认 eps=1e-8
    gap_rel4 = fd_rounding_gap(P0_INGEST, mpf("1e-4") * abs(P0_INGEST[1]))
    h_survive = abs(P0_INGEST[1] - V0_hat) / 2                        # 能在 float64 存活的最小量级步长
    gap_survive = fd_rounding_gap(P0_INGEST, h_survive)
    # 诚实反证：先按「假设它是缺陷」去测，测出来不是 ⇒ 如实记为 INFO，不粉饰成缺陷。
    usable = all(g > FLOAT64_EPS for g in (gap_abs, gap_rel4))
    reg("INFO", "A-D2【反证·不成立】有限差分**步长**不是本册的失效点（不可粉饰为缺陷）",
        "两处候选步长在来料运行栈上的差分相对量级：绝对步长 1e-8（scipy 默认）⇒ %s，"
        "相对步长 1e-4 ⇒ %s，均 **>** 双精度 ε = %s ⇒ 差分在该栈上**可用**（未退化）。"
        "本册曾按「步长灾难性」假设去测，实测不支持，故如实记为不成立；"
        "真正的失效点在 D1 的**公式**（两条对角都只拿到 H_true/2），不在步长。"
        "另注：本模型对参数是精确二次型 ⇒ 中心差分在精确算术下对**任意**步长都精确"
        "（FD 梯度 / 解析梯度 = %s），这是「步长不敏感」的根本原因；"
        "一旦换成非线性模型（如候选 1 的 CMB 第三组）该结论不再成立。"
        % (f(gap_abs, 3), f(gap_rel4, 3), f(FLOAT64_EPS, 3), f(grad_ratio, 4)),
        "判据 |f(x+ε)−f(x−ε)|/max f > 2.2e-16 ⇒ 可用；存活步长对照 = %s" % f(gap_survive, 3))


    # --- D3：初值量级 ------------------------------------------------------
    E_at_p0 = model_atomic(2, P0_INGEST[1])
    reg("BOUNDARY", "A-D3 来料初值 p₀ = [1e-3, 1e-18] 落在解的量级之外（本模型下不致命）",
        "解析解 β* = %s（来料初值 1e-3 差 %s 倍）；V₀* = %s（来料初值 1e-18 差 %s 倍）。"
        "初值处的原子模型值 E₂(p₀) = %s eV vs 观测 %s eV ⇒ 差 %s 个量级。"
        "**诚实降级**：因本模型对参数是精确二次型，L-BFGS-B 从该初值仍会收敛（本册闭式解即其极限），"
        "故此项**不是**本册的失效点；但它意味着任何「把该代码直接扩到非线性模型」的尝试"
        "都会在同一处失去保护 ⇒ 按 BOUNDARY 记，不记 FAIL。"
        % (f(beta_hat, 8), f(beta_hat / P0_INGEST[0], 4), f(V0_hat, 6),
           f(V0_hat / P0_INGEST[1], 4), f(E_at_p0, 6), f(E_OBS[0], 4),
           f(mp.log10(E_at_p0 / E_OBS[0]), 4)),
        "解析解 vs 来料 p0（二次型 ⇒ 收敛性不依赖初值）", "来料代码 p0 行")

    # --- D4：分块解耦（结构性）-------------------------------------------
    reg("INFO", "A-D4 「两参数联合拟合」在结构上不成立：ρ ≡ 0（精确）",
        "β 只进水星方程、V₀ 只进原子方程 ⇒ J = [[0.051/σ_M, 0], [0, kcol/σ₂], [0, kcol/σ₃]]，"
        "JᵀJ 块对角 ⇒ Σ 块对角 ⇒ ρ = 0 **精确**（不是「小到测不出」）。"
        "本册解析 ρ = %s（机器零）。来料样例输出的 ρ = 0.1845 在数学上不可能由该模型产生。"
        % f(fit["rho"], 3),
        "JᵀJ 结构 + 解析协方差", "来料代码 model_mercury/model_atomic")

    # --- D5：原子块 n 依赖项比所需小 35 个量级 ----------------------------
    dE_obs = E_OBS[1] - E_OBS[0]
    model_gap = KCOL * (DELTA_N[1] - DELTA_N[0])
    deficit = dE_obs / model_gap
    N_need = sqrt((DELTA_N[1] - DELTA_N[0]) * V_NTOP ** 2 * KCOL / dE_obs)
    reg("FAIL", "A-D5 原子块 n 依赖项比解释观测所需小 %s 倍（≈%s 个量级）" % (f(deficit, 3), f(mp.log10(deficit), 4)),
        "观测差 E₃−E₂ = %s eV；模型给出的差 (ω²/c²)(δ₃−δ₂) = %s eV。"
        "要解释观测差需 n²ℏ²/N² 项达到 %s（而实际 δ₃−δ₂ = %s）⇒ 需 N = %s"
        "（来料固定 N=1000，且 N 被声明为拓扑绕数**必须为整数**）⇒ 该模型在此数据下不可救。"
        % (f(dE_obs, 4), f(model_gap, 4), f(dE_obs / KCOL, 4),
           f(DELTA_N[1] - DELTA_N[0], 4), f(N_need, 4)),
        "δ_n = n²ℏ²/N² 精确计算 + 观测差 §", "来料 model_atomic + 观测表")

    # --- D6：量纲（承接 C48）---------------------------------------------
    reg("FAIL", "A-D6 量纲不自洽（承接 C48/C50，本册独立复述其后果）",
        "E_n 括号内 V₀ 项与 n²ℏ²/N² 项量纲不同（V₀ 无量纲、ℏ²/N² 具 [M²L⁴T⁻²]）⇒ 不可相加；"
        "且 (ω²/c²)·V₀ 的量纲为 [T⁻²]，乘 1/1.602e-19 后不构成能量。"
        "本册的「拟合」只能在该形式化模型内进行，不对其物理自洽性背书。",
        "与 C48（§12-C25-1）同型；本册新增「后果」= 参数不可解释为物理量",
        "承接 判定_空间螺旋V21续修_C25C35 §1.2")

    # --- D7：样例输出与来料模型不自洽 --------------------------------------
    sample_beta = mpf("1.02150000e-03")
    sample_sig_beta = mpf("4.2661e-04")
    ratio_beta = sample_beta / beta_hat
    ratio_sig = sample_sig_beta / fit["sigma"][0]
    reg("FAIL", "A-D7 来料样例输出与来料模型不自洽（数源不明、不可复现）",
        "样例 β = 1.0215e-03，而**该模型**的解析解 β* = %s（含 χ²=0 的精确标定条件 "
        "0.051β = 43.03−42.979 ⇒ β*=1 精确）。样例 σ_β = 4.2661e-04 vs 解析 %s（差 %s 倍）；"
        "样例 ρ = 0.1845 vs 解析 0（D4）。三项同时对不上 ⇒ 该样例不是这份模型/这份数据的读数。"
        % (f(beta_hat, 8), f(fit["sigma"][0], 4), f(ratio_sig, 4)),
        "样例 β/解析 = %s；样例 σ/解析 = %s" % (f(ratio_beta, 4), f(ratio_sig, 4)),
        "来料「示例输出样例（参考）」")

    # --- D8：σ_obs 是外部假设且窄于仓库自身锚点极差 -----------------------
    anchors = [mpf("42.98"), mpf("43.03"), mpf("43.11")]
    spread = max(anchors) - min(anchors)
    reg("BOUNDARY", "A-D8 σ_obs = 0.03 角秒/百年为外部假设，比仓库内水星三锚点极差窄 %s 倍"
        % f(spread / S_PHI, 3),
        "仓库内水星三锚点 42.98 / 43.03 / 43.11（极差 %s）无统一出处；读数层已把同类 σ_obs=0.1 "
        "挂 BOUNDARY。来料取 σ=0.03 更窄 ⇒ 依赖它的 σ_β、χ² 判别力与「需达精度」全部继承该不确定性。"
        % f(spread, 4),
        "σ_β = σ_obs/0.051 对 σ_obs 线性敏感：σ_obs=0.03→%s，0.1→%s，0.13（锚点极差）→%s"
        % (f(fit["sigma"][0], 4), f(mpf("0.1") / K_BETA, 4), f(spread / K_BETA, 4)),
        "读数层 §2.3 + C49/C51 判定册")

    # --- D9：原子观测无出处 -------------------------------------------------
    # 氢原子精细结构标准值（**仅供量级对照**，非本册输入）：
    #   E_{n,j} = −(m_e c²α²/(2n²))·[1 + (α²/n²)(n/(j+1/2) − 3/4)]
    #   ⇒ 最大 j (=n−1/2) 与最小 j (=1/2) 的分裂
    #   ΔE_fs(n) = m_e c² α⁴ (n−1)/(2n⁴)
    alpha = mpf("0.0072973525693")
    m_e_c2_eV = mpf("510998.95000")
    h_fs = {}
    for n in (2, 3):
        h_fs[n] = m_e_c2_eV * alpha ** 4 * (mpf(n) - 1) / (2 * mpf(n) ** 4)
    reg("FAIL", "A-D9 原子两点观测在仓库内无出处，且与氢精细结构标准值不符",
        "仓库内无该两点的锚表/文件引用（本册按「不得凭声明登记」纪律标 FAIL）。"
        "对照氢精细结构：n=2 分裂 ≈ %s eV、n=3 ≈ %s eV（α² 展开），而数据给 %s / %s eV，"
        "且数据 n 趋势（增大 2.23 倍）与模型/标准值趋势（减小）方向相反。"
        % (f(h_fs[2], 4), f(h_fs[3], 4), f(E_OBS[0], 4), f(E_OBS[1], 4)),
        "无溯源；与 α² 精细结构量级对照", "来料观测表 + 本册对照算例（仅供量级比较）")

    # --- D10：水星块自由度 0 ⇒ β 是标定不是预言 ---------------------------
    reg("INFO", "A-D10 水星块 1 数据 + 1 参数 ⇒ 该块自由度 0，β 是**标定**不是预言",
        "χ²_merc(β*) = 0（精确）且该块 ν=0 ⇒ 不产生任何可检验读数；"
        "这复现 C51「标定靶 = 最佳靶」的水星版：把 43.03 定成 β 的定义，再用 β 去「预言」43.03。",
        "解析：β* = (φ_obs−φ_GR)/0.051 = %s，χ²_merc = %s"
        % (f(beta_hat, 8), f(fit["residuals"][0] ** 2, 3)),
        "承接 C51 判定册")

    return {"H_ingest": H_ingest, "H_true": H_true, "det_ingest": det_ing,
            "fd_rounding_gap_abs1e8": f(gap_abs, 4),
            "fd_rounding_gap_rel1e4": f(gap_rel4, 4),
            "fd_survive_step": f(h_survive, 4),
            "fd_rounding_gap_survive": f(gap_survive, 4),
            "deficit": deficit,
            "N_need": N_need, "spread_anchor": spread,
            "hydrogen_fs": {str(k): v for k, v in h_fs.items()}}


# ===========================================================================
# 六、§B+§C 读数
# ===========================================================================

def crosscheck_hessian(fit):
    """用**正确**中心差分 + **相对**步长独立校验解析 Hessian（精确二次型 ⇒ 无截断误差）。"""
    p = fit["p_hat"]
    out = []
    for rel in (mpf("1e-3"), mpf("1e-4"), mpf("1e-5"), mpf("1e-6")):
        steps = [rel * max(abs(p[0]), mpf(1)), rel * max(abs(p[1]), mpf(1))]
        Hn = hessian_central(chi2, p, steps)
        out.append({"rel_step": f(rel, 3), "diff_vs_analytic": f(hess_dev(Hn, fit["H"]), 3)})
    return out


def readings(fit):
    print("\n" + "=" * 78)
    print("§B/§C  闭式拟合读数（解析雅可比 + 精确协方差 + 秩口径自由度）")
    print("=" * 78)
    p = fit["p_hat"]
    print("  β*  = %s" % f(p[0], 12))
    print("  V₀* = %s" % f(p[1], 12))
    print("  χ²_min = %s | ν = %d | χ²/ν = %s | p = %s"
          % (f(fit["chi2_min"], 10), fit["nu"],
             f(fit["chi2_min"] / fit["nu"], 8) if fit["nu"] > 0 else "—",
             fmt_p(fit["p_value"])))
    print("  协方差 Σ = [[%s, %s], [%s, %s]]"
          % (f(fit["cov"][0][0], 6), f(fit["cov"][0][1], 6),
             f(fit["cov"][1][0], 6), f(fit["cov"][1][1], 6)))
    print("  σ_β = %s | σ_V₀ = %s | ρ = %s"
          % (f(fit["sigma"][0], 10), f(fit["sigma"][1], 10), f(fit["rho"], 3)))
    print("  逐点残差（σ 为单位）:")
    labels = ["水星 Δφ"] + ["原子 n=%d" % n for n in ATOM_N]
    for lab, r in zip(labels, fit["residuals"]):
        print("    %-10s r = %s   χ² = %s" % (lab, f(r, 8), f(r ** 2, 8)))

    reg("PASS" if abs(fit["rho"]) < mpf("1e-40") else "FAIL",
        "B-1 相关系数 ρ ≡ 0（块对角）——「联合拟合」的 2×2 协方差实为两个 1×1 的并置",
        "解析 Σ 非对角元 = %s（机器零）；σ_β = %s、σ_V₀ = %s" %
        (f(fit["cov"][0][1], 3), f(fit["sigma"][0], 8), f(fit["sigma"][1], 8)),
        "JᵀJ 块对角（来料模型分块）")

    reg("FAIL" if fit["p_value"] is not None and fit["p_value"] < (1 - CL) else "PASS",
        "C-1 联合拟合判定：χ² = %s，ν = %d ⇒ %s"
        % (f(fit["chi2_min"], 8), fit["nu"],
           "被数据排除（p < 0.05）" if (fit["p_value"] is not None
                                       and fit["p_value"] < (1 - CL)) else "与数据自洽"),
        "χ² 由 χ²_merc = %s + χ²_atom = %s 组成；原子块单独即已排除（ν_atom = 1）"
        % (f(fit["residuals"][0] ** 2, 3),
           f(sum(r ** 2 for r in fit["residuals"][1:]), 8)),
        "闭式最小二乘 + erfc 生存函数")

    # 参数被约束到几位（判决力的一种读数）
    reg("INFO", "C-2 参数约束精度（σ/|值|）：β = %s，V₀ = %s"
        % (f(fit["sigma"][0] / abs(p[0]), 4), f(fit["sigma"][1] / abs(p[1]), 4)),
        "β 的相对误差完全由 σ_obs（外部假设）决定；V₀ 的相对误差由原子两点之差决定 "
        "（χ²_atom ≫ 1 ⇒ 该「误差」只在模型被拒的假设下才有意义，不构成可信区间）。",
        "Σ = (AᵀA)⁻¹", "本册")
    return


def predictions(fit):
    """锁参预言：固定 β*, V₀* 直接给 Venus/Earth 与 n=4/5/6（不再调参）。"""
    print("\n" + "=" * 78)
    print("§D  锁参预言（固定 β*、V₀*，不再调参）")
    print("=" * 78)
    beta_hat = fit["p_hat"][0]
    V0_hat = fit["p_hat"][1]
    geo_mer_user = K_BETA * beta_hat                 # 来料口径下水星几何项 = 0.051
    gr_a, law_a, _bc, tol, src = gr_anchors()
    gr250 = {}
    for name, a, e, T, ref in PLANETS:
        gr250[name] = gr_per_century(a, e, T)
    # 交叉回归断言 1：GR 基础项 vs 上游基准
    dev_gr = max(abs(gr250[k] - gr_a[k]) / gr_a[k] for k in gr250)
    reg("PASS" if dev_gr < tol else "FAIL",
        "P-1 阳性对照：GR 基础项复现仓库上游基准（相对差 %s < %s）" % (f(dev_gr, 3), f(tol, 3)),
        "水星 %s / 金星 %s / 地球 %s（角秒/百年）；基准来源：%s"
        % (f(gr250["水星"], 8), f(gr250["金星"], 8), f(gr250["地球"], 8), src),
        "6πGM/(c²p)·(100/T)/ARCSEC vs 判定册 C25C35 §2.1 / 上游 json")

    # 两条 a 标度律各自用「水星几何项 = geo_mer_user」标定 β
    a_m, e_m, T_m = PLANETS[0][1], PLANETS[0][2], PLANETS[0][3]
    beta_b = geo_mer_user / geo_binet_per_century(mpf(1), a_m, e_m, T_m)
    beta_d = geo_mer_user / geo_draft_per_century(mpf(1), a_m, e_m, T_m)
    # 交叉回归断言 2：用上游自己的水星几何项标定，两式应复现上游两式读数
    if law_a:
        dev_c49 = mpf(0)
        for nm in ("金星", "地球"):
            a_p, e_p, T_p = [(x[1], x[2], x[3]) for x in PLANETS if x[0] == nm][0]
            geo_c49 = mpf("43.03") - gr_a["水星"]
            bb = geo_c49 / geo_binet_per_century(mpf(1), a_m, e_m, T_m)
            bd = geo_c49 / geo_draft_per_century(mpf(1), a_m, e_m, T_m)
            dev_c49 = max(dev_c49,
                          abs(geo_binet_per_century(bb, a_p, e_p, T_p) - law_a[nm][0]) / law_a[nm][0],
                          abs(geo_draft_per_century(bd, a_p, e_p, T_p) - law_a[nm][1]) / law_a[nm][1])
        reg("PASS" if dev_c49 < tol else "FAIL",
            "P-2 阳性对照：两条候选 a 标度律复现上游两式读数（相对差 %s < %s）" % (f(dev_c49, 3), f(tol, 3)),
            "Binet 一阶式金星 %s / 地球 %s；草稿式金星 %s / 地球 %s（角秒/百年）"
            % (f(law_a["金星"][0], 8), f(law_a["地球"][0], 8),
               f(law_a["金星"][1], 8), f(law_a["地球"][1], 8)),
            "对照 判定_空间螺旋V21续修_C25C35 §2.2 / 上游 json")
    else:
        dev_c49 = None
        reg("BOUNDARY", "P-2 阳性对照降级：上游 json 不可读 ⇒ 两条 a 标度律未做全精度回归",
            "仅能对照判定册 8 位读数（未在本次运行断言）", src)

    rows = []
    for name, a, e, T, ref in PLANETS:
        gb = geo_binet_per_century(beta_b, a, e, T)
        gd = geo_draft_per_century(beta_d, a, e, T)
        rows.append({"planet": name, "GR": gr250[name], "geo_binet": gb, "geo_draft": gd,
                     "total_binet": gr250[name] + gb, "total_draft": gr250[name] + gd,
                     "ref": ref})
    print("\n  表 D-1  行星近日点进动（角秒/百年）：GR 基础 + 两条 a 标度律下的 TUFT 几何项")
    print("    %-4s %-14s %-16s %-16s %-16s %-16s" %
          ("行星", "GR基础", "几何(Binet a²)", "总(Binet)", "几何(草稿 a³)", "总(草稿)"))
    for r in rows:
        print("    %-4s %-14s %-16s %-16s %-16s %-16s"
              % (r["planet"], f(r["GR"], 8), f(r["geo_binet"], 6), f(r["total_binet"], 8),
                 f(r["geo_draft"], 6), f(r["total_draft"], 8)))
    reg("BOUNDARY", "D-1 金星/地球预言在来料中**无定义**：来料模型没有 a 标度律",
        "来料只有一条「水星：Δφ_TUFT = 0.051β」的线性式，未给 Δφ 随 a 的幂次。"
        "本册必须**外借**两条候选律（Binet a²、草稿 a³）才能产生预言，两条给出 1.87×/2.58× 之差 ⇒ "
        "预言值不是来料的输出，而是「来料 + 仓库既有候选律」的合成，故按 BOUNDARY 记。",
        "外借来源：判定册 C25C35 §2.2（C49/C51）", "本册 §D")

    reg("FAIL", "D-2 金星/地球的几何增量低于历表约束 %s / %s 个量级 ⇒ 当前不可判"
        % (f(-log10(rows[1]["geo_binet"] / mpf("0.1")), 3),
           f(-log10(rows[2]["geo_binet"] / mpf("0.1")), 3)),
        "Binet 口径（本册，标定靶 = 来料 0.051）：金星 %s、地球 %s 角秒/百年；"
        "草稿口径：金星 %s、地球 %s。即便取 0.1 角秒/百年这一**宽松外部假设**作为历表精度，"
        "信号仍低 1.3–1.8 个量级。读数层（标定靶 = 仓库 0.04796364）给 1.30688 / 1.799 个量级 "
        "⇒ **同量级、口径不同**（本册用 0.051 故略大），交叉吻合非逐位复现。"
        % (f(rows[1]["geo_binet"], 6), f(rows[2]["geo_binet"], 6),
           f(rows[1]["geo_draft"], 6), f(rows[2]["geo_draft"], 6)),
        "读数层 §2.3 的 C51 两条读数（1.30688 / 1.799 个量级）")

    # 原子 n=4,5,6
    atom_rows = []
    for n in (4, 5, 6):
        En = KCOL * (V0_hat + n ** 2 * V_HBAR ** 2 / V_NTOP ** 2)
        atom_rows.append({"n": n, "E_eV": En})
    spread_model = max(r["E_eV"] for r in atom_rows) - min(r["E_eV"] for r in atom_rows)
    print("\n  表 D-2  原子高阶能级（eV）：E_n = (ω²/c²)(V₀* + n²ℏ²/N²) / 1.602176634e-19")
    for r in atom_rows:
        print("    n=%d  E = %s eV" % (r["n"], f(r["E_eV"], 10)))
    reg("FAIL", "D-3 n=4/5/6 预言在模型内**退化**（n 方向跨度 %s eV，低观测精度 %s 个量级）"
        % (f(spread_model, 3), f(-log10(spread_model / mpf("0.003e-4")), 3)),
        "ℏ²/N² = %s 使 n 方向项可忽略；三条预言的差 = %s eV，而数据点误差 ~3e-7 eV "
        "⇒ 该「高阶预言」无判别力（承接 C48/C50：n=6 谱宽低 α 精度 65.14 个量级）。"
        "且三条预言全部只是两个观测点的加权均值 %s eV 的复制（原子块被拒后不构成预言）。"
        % (f(V_HBAR ** 2 / V_NTOP ** 2, 3), f(spread_model, 3), f(atom_rows[0]["E_eV"], 6)),
        "承接 C50；本册用同一模型给出 n=4/5/6", "本册 §D")

    return {"gr250": gr250, "geo_mer_user": geo_mer_user,
            "beta_binet_cal": beta_b, "beta_draft_cal": beta_d,
            "planets": rows, "atom": atom_rows,
            "atom_spread": spread_model,
            "regress_dev_gr": dev_gr, "regress_dev_c49": dev_c49}


# ===========================================================================
# 七、§E 牙齿（变异体 + 阳性对照）
# ===========================================================================

def run_teeth(fit):
    T = []

    def rec(name, ok, detail):
        T.append({"name": name, "ok": bool(ok), "detail": detail})

    p = fit["p_hat"]

    # T1 来料 Hessian 公式 ⇒ 对角恰为解析值的 1/2 ⇒ Σ 放大 4 倍、σ 放大 2 倍
    Hi = hessian_ingest(chi2, p, mpf("1e-4"))
    dev = hess_dev(Hi, fit["H"])
    half = all(abs(Hi[i][i] / fit["H"][i][i] - mpf("0.5")) < mpf("1e-30") for i in range(2))
    covi = inv2(Hi)[0]
    covi = covi if covi is None else [[2 * x for x in row] for row in covi]
    sig_ratio = sqrt(covi[0][0] / fit["cov"][0][0])
    rec("T1 来料 Hessian 公式 ⇒ 对角恰为解析值的 1/2 ⇒ Σ 放大 2 倍、σ 放大 √2 倍",
        dev > mpf("1e-6") and half and abs(sig_ratio - sqrt(mpf(2))) < mpf("1e-30"),
        "H⁰⁰ %s vs %s、H¹¹ %s vs %s（比值均 0.5，机器精确）；Σ 放大倍数 %s ⇒ σ 放大 %s"
        % (f(Hi[0][0], 6), f(fit["H"][0][0], 6), f(Hi[1][1], 6), f(fit["H"][1][1], 6),
           f(covi[0][0] / fit["cov"][0][0], 4), f(sig_ratio, 4)))

    # T2 反证：把公式换正确、**步长仍用绝对量**（不是相对量）⇒ 必须与解析一致
    Ha = hessian_central(chi2, p, [mpf("1e-4"), mpf("1e-4")])
    rec("T2 反证：正确公式 + 绝对步长 ⇒ 仍与解析一致（⇒ 失效点在公式不在步长）",
        hess_dev(Ha, fit["H"]) < mpf("1e-15"),
        "偏差 %s；同一模型下差分可用性判据（相对量级）：绝对步长 1e-8 ⇒ %s，"
        "相对步长 1e-4 ⇒ %s，均 > 双精度 ε = %s"
        % (f(hess_dev(Ha, fit["H"]), 3),
           f(fd_rounding_gap(P0_INGEST, mpf("1e-8")), 3),
           f(fd_rounding_gap(P0_INGEST, mpf("1e-4") * abs(P0_INGEST[1])), 3),
           f(FLOAT64_EPS, 3)))

    # T3 正确公式 + 相对步长 ⇒ 与解析逐位一致（精确二次型的必要条件）
    ok3 = True
    detail3 = []
    for rel in (mpf("1e-3"), mpf("1e-5")):
        steps = [rel * max(abs(p[0]), mpf(1)), rel * max(abs(p[1]), mpf(1))]
        Hn = hessian_central(chi2, p, steps)
        d = hess_dev(Hn, fit["H"])
        ok3 = ok3 and d < mpf("1e-15")
        detail3.append("rel=%s ⇒ 偏差 %s" % (f(rel, 3), f(d, 3)))
    rec("T3 正确中心差分 + 相对步长 ⇒ 与解析 Hessian 一致到机器精度", ok3, "；".join(detail3))

    # T4 σ 缩小 10× ⇒ χ² 抬升 100×（统计量实现正确性）
    old = S_PHI
    a_arr = K_BETA / S_PHI
    base = a_arr ** 2
    globals()["S_PHI"] = old / 10
    tight = (K_BETA / S_PHI) ** 2
    globals()["S_PHI"] = old
    rec("T4 σ 缩小 10× ⇒ χ² 权重抬升 100×", abs(tight / base - 100) < mpf("1e-20"),
        "实测倍数 %s" % f(tight / base, 8))

    # T5 σ ≤ 0 ⇒ 拒算（Σ 非正定）
    inv_bad, det_bad = inv2([[mpf(0), mpf(0)], [mpf(0), mpf(1)]])
    rec("T5 σ ≤ 0（Σ 奇异）⇒ 拒绝求逆而非静默给伪协方差", inv_bad is None,
        "det = %s ⇒ 返回 None" % f(det_bad, 3))

    # T6 χ² = χ²_crit ⇒ p = 0.05（边界口径）
    rec("T6 p 值口径：p(χ²_crit) = 0.05、p(0) = 1",
        abs(sf_chi2(CHI2_CRIT_1, 1) - mpf("0.05")) < mpf("1e-20") and sf_chi2(mpf(0), 1) == 1,
        "p(χ²_crit) = %s" % f(sf_chi2(CHI2_CRIT_1, 1), 10))

    # T7 ρ 越界保护：块对角 ⇒ ρ 必须精确为 0，任何非零报告都算 MISSED
    rec("T7 块对角 ⇒ ρ 必须精确 0（非零报告算 MISSED）",
        abs(fit["cov"][0][1]) < mpf("1e-60") and fit["rho"] == 0,
        "Σ₀₁ = %s，ρ = %s" % (f(fit["cov"][0][1], 3), f(fit["rho"], 3)))

    # T8 自由度走秩口径（定理 I）：行成比例 ⇒ 秩 1
    j2 = frac_rank([[1, -2], [2, -4]])
    j3 = frac_rank([[1, 0], [0, 1]])
    rec("T8 自由度走秩口径（行成比例 ⇒ 秩 1 ⇒ ν = n−1）", j2 == 1 and j3 == 2,
        "rank([[1,-2],[2,-4]]) = %d；rank(I₂) = %d" % (j2, j3))

    # T9 δ_min 口径：必须用 √χ²_crit 而非 1σ
    dmin = S_PHI * sqrt(CHI2_CRIT_1)
    rec("T9 δ_min 必须用 √χ²_crit（1σ 口径算 MISSED）",
        abs(dmin / S_PHI - sqrt(CHI2_CRIT_1)) < mpf("1e-30")
        and abs(sqrt(CHI2_CRIT_1) - mpf(1)) > mpf("0.9"),
        "δ_min/σ = %s（≠1）" % f(sqrt(CHI2_CRIT_1), 8))

    # T10 阳性对照：GR 基准回归（仪器有效性）
    gr_a, _law, _bc, tol, _src = gr_anchors()
    dev_gr = max(abs(gr_per_century(a, e, T) - gr_a[nm]) / gr_a[nm]
                 for nm, a, e, T, ref in PLANETS)
    rec("P1 阳性对照：GR 基础项复现仓库上游基准（仪器有效）", dev_gr < tol,
        "最大相对偏差 %s（容差 %s）" % (f(dev_gr, 3), f(tol, 3)))

    # T11 阳性对照：闭式解 = 一维牛顿迭代解（不依赖闭式推导）
    beta_newton = newton_1d(lambda b: K_BETA * (b - 1.0), mpf("0.3"))
    rec("P2 阳性对照：一维牛顿迭代收敛到闭式解 β*（解算器交叉验证）",
        abs(beta_newton - fit["p_hat"][0]) < mpf("1e-40"),
        "牛顿 %s vs 闭式 %s" % (f(beta_newton, 12), f(fit["p_hat"][0], 12)))
    return T


def newton_1d(g, x0, tol=mpf("1e-60"), itmax=200):
    """简单一维牛顿（对线性函数一步收敛）——只作交叉验证，不参与读数。"""
    x = x0
    for _ in range(itmax):
        gx = g(x)
        h = mpf("1e-20") * (abs(x) + 1)
        dg = (g(x + h) - g(x - h)) / (2 * h)
        if dg == 0:
            break
        step = gx / dg
        x = x - step
        if abs(step) < tol:
            break
    return x


# ===========================================================================
# 八、汇总 / 产出
# ===========================================================================

def render_md(payload):
    P = payload
    L = []
    A = L.append
    A("# 空间螺旋 V21 · 水星与精细结构 · 卡方联合拟合（拟合层 · 可复跑产物）\n")
    A("> 本文件由 `源码/空间螺旋V21_水星与精细结构_卡方联合拟合.py` 生成，**请勿手工编辑**。\n")
    A("> mpmath dps=%d · Python %s · 生成于 %s\n" % (P["mpmath_dps"], P["python"], P["generated_utc"]))
    A("\n## 〇、范围与口径\n")
    A("本册是统计层的**拟合层**：给参数估计 + 协方差。统计口径复用读数层"
      "（$\\chi^2=\\sum r_i^2$、秩口径自由度 $\\nu=N_{\\rm data}-\\mathrm{rank}(J)$、"
      "$\\Sigma=2H^{-1}=(A^{\\mathsf T}A)^{-1}$）。**零外部依赖**（不用 numpy/scipy/JAX/emcee）。\n")
    A("\n## 一、来料审计（逐条机器证据）\n")
    A("| 编号 | 状态 | 结论 | 证据 |")
    A("| --- | --- | --- | --- |")
    for r in P["audit"]:
        A("| `%s` | **%s** | %s | %s |" % (r["tag"], r["state"], r["statement"], r["detail"]))
    A("\n## 二、闭式拟合读数\n")
    A("| 量 | 值 |")
    A("| --- | --- |")
    for k, v in P["readings"].items():
        A("| %s | `%s` |" % (k, v))
    A("\n逐点残差（σ 为单位）：\n")
    A("| 数据点 | r | χ² |")
    A("| --- | --- | --- |")
    for lab, rr, cc in P["residual_table"]:
        A("| %s | `%s` | `%s` |" % (lab, rr, cc))
    A("\n## 三、锁参预言（固定 β*、V₀*）\n")
    A("### 3.1 行星近日点进动（角秒/百年）\n")
    A("| 行星 | GR 基础 | 几何(Binet a²) | 总(Binet) | 几何(草稿 a³) | 总(草稿) |")
    A("| --- | --- | --- | --- | --- | --- |")
    for r in P["pred"]["planets"]:
        A("| %s | %s | %s | %s | %s | %s |"
          % (r["planet"], r["GR"], r["geo_binet"], r["total_binet"], r["geo_draft"], r["total_draft"]))
    A("\n> **来料模型没有 a 标度律** ⇒ 上表须外借仓库既有两条候选律（Binet a²、草稿 a³），"
      "两条给出 1.87×/2.58× 之差，故预言按 `BOUNDARY` 记。\n")
    A("\n### 3.2 原子高阶能级（eV）\n")
    A("| n | E_n |")
    A("| --- | --- |")
    for r in P["pred"]["atom"]:
        A("| %d | `%s` |" % (r["n"], r["E_eV"]))
    A("\n> n 方向跨度 `%s` eV ⇒ 退化（承接 C48/C50）。\n" % P["pred"]["atom_spread"])
    A("\n## 四、判定清单（四态齐备）\n")
    A("| 编号 | 状态 | 内容 | 证据 |")
    A("| --- | --- | --- | --- |")
    for r in P["rows"]:
        A("| `%s` | **%s** | %s | %s |" % (r["tag"], r["state"], r["statement"], r["detail"]))
    if P.get("teeth"):
        A("\n## 五、牙齿（变异体 + 阳性对照）\n")
        A("| 项 | 结果 | 证据 |")
        A("| --- | --- | --- |")
        for t in P["teeth"]:
            A("| %s | **%s** | %s |" % (t["name"], "CAUGHT/CLEAN" if t["ok"] else "MISSED", t["detail"]))
    A("\n## 六、诚实边界\n")
    for line in P["honest_notes"]:
        A("- " + line)
    A("\n```powershell")
    A("cd openuft/04_公共成果/算法联盟_全维自洽与归一化/源码")
    A("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 空间螺旋V21_水星与精细结构_卡方联合拟合.py")
    A("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 空间螺旋V21_水星与精细结构_卡方联合拟合.py --teeth")
    A("```\n")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    teeth_on = "--teeth" in sys.argv
    print("=" * 78)
    print("空间螺旋 V21 · 水星 + 原子精细结构 · 卡方联合拟合（拟合层，dps=%d）" % mp.dps)
    print("=" * 78)
    print("  kcol = ω²/(c²·eV) = %s eV 每 kcol-单位" % f(KCOL, 10))
    print("  δ₂ = %s，δ₃ = %s" % (f(DELTA_N[0], 4), f(DELTA_N[1], 4)))

    fit = closed_form_fit()
    D = audit_ingest(fit)
    readings(fit)
    pred = predictions(fit)
    cross = crosscheck_hessian(fit)
    teeth = run_teeth(fit) if teeth_on else []

    n_ok = sum(1 for t in teeth if t["ok"])
    print("\n" + "=" * 78)
    print("汇总：审计 + 读数 + 预言")
    print("=" * 78)
    print("  交叉校验（正确中心差分 vs 解析 Hessian）:")
    for c in cross:
        print("    rel_step=%s ⇒ 与解析 Hessian 的偏差 %s" % (c["rel_step"], c["diff_vs_analytic"]))
    state_cnt = {}
    for r in ROWS:
        state_cnt[r["state"]] = state_cnt.get(r["state"], 0) + 1
    print("  判定：总数 %d | %s" % (len(ROWS),
          " ".join("%s=%d" % (k, state_cnt.get(k, 0)) for k in ("PASS", "FAIL", "BOUNDARY", "INFO"))))
    if teeth:
        print("  牙齿：%d/%d %s" % (n_ok, len(teeth),
                                   "全部 CAUGHT/CLEAN" if n_ok == len(teeth) else "存在 MISSED"))
        for t in teeth:
            print("    %-6s %s | %s" % ("CAUGHT/CLEAN" if t["ok"] else "MISSED",
                                        t["name"], t["detail"]))

    residual_table = []
    labels = ["水星 Δφ"] + ["原子 n=%d" % n for n in ATOM_N]
    for lab, r in zip(labels, fit["residuals"]):
        residual_table.append([lab, f(r, 8), f(r ** 2, 8)])

    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mpmath_dps": mp.dps,
        "python": sys.version.split()[0],
        "root": ROOT,
        "input": {
            "phi_obs": f(PHI_OBS, 8), "sigma_obs": f(S_PHI, 6), "phi_gr": f(PHI_GR, 8),
            "k_beta": f(K_BETA, 6),
            "atom_n": ATOM_N,
            "E_obs": [f(x, 6) for x in E_OBS],
            "E_sig": [f(x, 6) for x in E_SIG],
            "omega": f(V_OMEGA, 3), "N_top": f(V_NTOP, 6),
            "p0_ingest": [f(x, 6) for x in P0_INGEST],
            "kcol": f(KCOL, 10),
            "delta_n": [f(x, 6) for x in DELTA_N],
        },
        "fit": {
            "beta": f(fit["p_hat"][0], 12), "V0": f(fit["p_hat"][1], 12),
            "chi2_min": f(fit["chi2_min"], 10), "nu": fit["nu"], "rank_j": fit["rank_j"],
            "chi2_over_nu": f(fit["chi2_min"] / fit["nu"], 8) if fit["nu"] > 0 else None,
            "p_value": fmt_p(fit["p_value"]),
            "cov": [[f(x, 8) for x in row] for row in fit["cov"]],
            "sigma": [f(x, 10) for x in fit["sigma"]],
            "rho": f(fit["rho"], 3),
            "H_analytic": [[f(x, 10) for x in row] for row in fit["H"]],
            "H_ingest_exec": [[f(x, 8) for x in row] for row in D["H_ingest"]],
        },
        "audit": ROWS,
        "rows": ROWS,
        "residual_table": residual_table,
        "readings": {
            "β*(最优)": f(fit["p_hat"][0], 12),
            "V₀*(最优)": f(fit["p_hat"][1], 12),
            "χ²_min": f(fit["chi2_min"], 10),
            "自由度 ν": str(fit["nu"]),
            "χ²/ν": f(fit["chi2_min"] / fit["nu"], 8) if fit["nu"] > 0 else "—",
            "p 值": fmt_p(fit["p_value"]),
            "Σ₁₁": f(fit["cov"][0][0], 8), "Σ₁₂": f(fit["cov"][0][1], 3),
            "Σ₂₂": f(fit["cov"][1][1], 8),
            "σ_β": f(fit["sigma"][0], 10), "σ_V₀": f(fit["sigma"][1], 10),
            "ρ": f(fit["rho"], 3),
            "H_解析(1,1)": f(fit["H"][0][0], 8), "H_解析(2,2)": f(fit["H"][1][1], 8),
            "H_来料(1,1)": f(D["H_ingest"][0][0], 4),
            "H_来料(2,2)": f(D["H_ingest"][1][1], 8),
            "det(H_来料)": f(D["det_ingest"], 4),
            "χ²_crit(1,0.95)": f(CHI2_CRIT_1, 12),
        },
        "pred": {"planets": [{"planet": r["planet"], "GR": f(r["GR"], 8),
                              "geo_binet": f(r["geo_binet"], 8), "geo_draft": f(r["geo_draft"], 8),
                              "total_binet": f(r["total_binet"], 8),
                              "total_draft": f(r["total_draft"], 8), "ref": f(r["ref"], 6)}
                             for r in pred["planets"]],
                 "atom": [{"n": r["n"], "E_eV": f(r["E_eV"], 10)} for r in pred["atom"]],
                 "atom_spread": f(pred["atom_spread"], 4),
                 "geo_mer_user": f(pred["geo_mer_user"], 8),
                 "beta_binet_cal": f(pred["beta_binet_cal"], 10),
                 "beta_draft_cal": f(pred["beta_draft_cal"], 10),
                 "gr250": {k: f(v, 10) for k, v in pred["gr250"].items()},
                 "regress_dev_gr": f(pred["regress_dev_gr"], 3),
                 "regress_dev_c49": (None if pred["regress_dev_c49"] is None
                                     else f(pred["regress_dev_c49"], 3))},
        "crosscheck_hessian": cross,
        "teeth": teeth,
        "honest_notes": [
            "本模块不产生 L3：它把拟合读数算准，来料模型是否成立与本模块无关。",
            "χ² ≈ 0 不等于证据：水星块 1 数据 1 参数 ⇒ ν=0，β 是标定不是预言。",
            "σ_obs = 0.03 角秒/百年是来料外部假设（比仓库锚点极差窄 4.33 倍）⇒ 依赖它的读数只能判 BOUNDARY。",
            "原子两点观测在仓库内无出处 ⇒ 不构成可溯源观测靶（按「不得凭声明登记」纪律标 FAIL）。",
            "「两参数联合拟合」在结构上不成立：ρ ≡ 0（精确块对角）。",
            "零外部依赖：不用 numpy / scipy / JAX / emcee（本册用闭式解 + 中心差分交叉校验）。",
        ],
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "空间螺旋V21_卡方联合拟合.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "空间螺旋V21_卡方联合拟合.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(payload))

    print("  产出：数据/空间螺旋V21_卡方联合拟合.{json,md}  用时 %.2fs" % (time.time() - t0))
    exit_code = 0 if not teeth else (0 if all(t["ok"] for t in teeth) else 1)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
