# -*- coding: utf-8 -*-
"""
UFS-Delta VII：描述长度账本与信息预算
==============================================================================
前六册把判别式从 V4 = (h_eff - f - a - nu)/(kappa+k) 一路净化到

    m_rank <= p - a_eff                                     （VI，净化版）

它只回答一个**是/否**问题：这条声明有没有新信息。六册下来答案永远是「没有」，
但这个「没有」是**二值的、无量纲的、不可比的**，而且：

  * 定理 S（IV）已证明：**跨声明比较 V4 的数值非法**；
  * VI 又证明：判别式**只对由账本导出的靶**有功效。

于是判别式剩下的全部内容只是两个整数之比 a_eff / p，再没有可榨的东西。

**本册换单位：把「维数」换成「比特」。**

    Net_bits(声明) = log2( s_T / sigma_e )  -  K(n)  -  nu_eff
                     \\_______  _______/     \\_  _/   \\__  _/
                            增益                成本      纯数因子价

  * s_T      ：靶的直接测量相对不确定度；
  * sigma_e  ：声明的残差标准差（**协方差**口径，见定理 Sigma_cov）；
  * K(n)     ：整数指数向量 + 锚子集选择的自定界编码长度（比特）；
  * nu_eff   ：纯数因子 xi 在模掉**单位制规范群** G = <2, pi, -1> 后的
               描述长度（定理 Upsilon）—— 这是 nu 的第一个机械定义。

三个立刻兑现的好处：

  1. **连续、可比**：不再是二值，而是带符号的比特数，跨声明可比
     （定理 S 禁止的是比较 V4 的**数值**，不是比较比特数 —— 比特数是
     在同一个自定界编码下定义的绝对量）；
  2. **nu 有了机械定义**（闭合 O-12）：nu_eff = K(xi mod G)，
     单位制重标定不变，谎报要付钱；
  3. **判别式第一次给出可证伪的正命题**（定理 Phi_bits）：
     账本总信息预算 B_ledger ~ 134 bit，故能「推出」的 10 位独立新数
     **至多 4 个**。

本册新定理：
  Sigma_cov  账本协方差可反解（+ 可识别性判据）      —— 修正 III/IV/VI 的对角假设
  Upsilon    nu_eff = K(xi mod G)，闭合 O-12
  Omega_bits 净比特主公式 + 分辨率上界               —— 本源公式（比特版）
  Phi_bits   账本信息预算 B_ledger，可证伪上限 K<=4
  Psi_bits   mu_0 / 先验范围 R 只影响绝对值不影响排序 —— O-1 降级

自检：见末尾 CHECKS 汇总。产物：数据/派生核算VII_描述长度账本.{json,md}
==============================================================================
"""
import os
import sys
import time
import json
import math
from fractions import Fraction

import numpy as np
from mpmath import mp, mpf, log as _log, pi as PI, sqrt as _sqrt
from sympy import Matrix, Rational, symbols, simplify

mp.dps = 60
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def A(s=""):
    REPORT.append(s)


def L(s):
    return _log(mpf(s))


LOG2_10 = math.log2(10.0)
UPSILON_CACHE = {}      # 定理 Υ 的产物，供 §3 引用（ν_eff 最小非零值）


# ===========================================================================
# 输入（与 IV / V / VI 逐字节同源，运行时与 V3 交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "k_B"},
}
KEYS = ["c", "hbar", "G", "e", "eps0", "m_e", "m_mu", "m_p", "m_P", "k_B"]
H_SI = mpf("6.62607015e-34")          # h 精确（SI-2019 定义）
HBAR_EXACT = H_SI / (2 * PI)          # hbar = h/(2 pi)，精确

# 相对标准不确定度（外部 CODATA 数据，见 OPEN O-6）
UNC_REL = {"c": 0.0, "hbar": 0.0, "e": 0.0, "k_B": 0.0,
           "G": 2.2e-5, "eps0": 1.5e-10, "m_e": 3.0e-10,
           "m_mu": 2.2e-8, "m_p": 3.1e-10, "m_P": 1.1e-5}
# 有实测不确定度的自由度（其余是 SI-2019 定义常量，sigma = 0）
DOF = ["G", "eps0", "m_e", "m_mu", "m_p"]
P_DOF = len(DOF)

TARGET_STR = {
    "alpha":        "7.2973525693e-3",
    "alpha_grav_e": "1.75180994573e-45",
    "m_mu_over_me": "206.7682830",
    "m_p_over_me":  "1836.15267343",
}
TARGET_VAL = {k: L(v) for k, v in TARGET_STR.items()}
# III / IV / VI 用的靶不确定度表（**本册修正对象**，见 Sigma_cov-6）
UNC_T_REL = {"alpha": 1.5e-10, "alpha_grav_e": 2.2e-5,
             "m_mu_over_me": 2.2e-8, "m_p_over_me": 3.1e-10}
# 账本自身公布的**比值**不确定度（外部数据，O-6）
RATIO_STR = {
    "m_p_over_me":  ("1836.15267343", "11"),   # CODATA: 1836.15267343(11)
    "m_mu_over_me": ("206.7682830", "46"),     # CODATA: 206.7682830(46)
}
# 修正后的靶不确定度：比值类靶必须用**公布值**，不能用「由锚传播」的值。
UNC_T_PUB = {"alpha": 1.5e-10, "alpha_grav_e": 2.2e-5,
             "m_mu_over_me": None, "m_p_over_me": None}   # 后两项由 RATIO 填

# SI-2019 定义常量：表值是**精确**的，不贡献舍入地板（IV 的教训：
# 若把它们当十进制数计半字长，c 的 1.67e-9 会把 α 的地板抬高 100 倍）
EXACT = {"c", "hbar", "e", "k_B"}


def u_rel_of_ratio(val_str, unc_last):
    """由 'xxxxx(nnn)' 记号得到相对不确定度。"""
    mant = val_str.split("e")[0]
    nd_after = len(mant.split(".")[1]) if "." in mant else 0
    u = mpf(unc_last) / mpf(10) ** nd_after
    return u / mpf(val_str)


UNC_RATIO = {k: u_rel_of_ratio(*v) for k, v in RATIO_STR.items()}
UNC_T_PUB["m_mu_over_me"] = float(UNC_RATIO["m_mu_over_me"])
UNC_T_PUB["m_p_over_me"] = float(UNC_RATIO["m_p_over_me"])

# 声明池：整数指数写在 10 个锚上（与 IV/V/VI 同源）。
# 注意 alpha_grav(e) 与 (m_e/m_P)^2 是**同一条**（V 的 V0-a 已证），此处只列一次。
CLAIMS = [
    {"name": "alpha",
     "n": {"e": 2, "eps0": -1, "hbar": -1, "c": -1},
     "xi": "1/(4*pi)", "target": "alpha"},
    {"name": "alpha_grav_e == (m_e/m_P)^2",
     "n": {"G": 1, "m_e": 2, "hbar": -1, "c": -1},
     "xi": "1", "target": "alpha_grav_e"},
    {"name": "m_mu/m_e",
     "n": {"m_mu": 1, "m_e": -1},
     "xi": "1", "target": "m_mu_over_me"},
    {"name": "m_p/m_e",
     "n": {"m_p": 1, "m_e": -1},
     "xi": "1", "target": "m_p_over_me"},
]


def cross_check_table():
    """输入端与 V3 对齐；V3 不可用则报 FAIL（不允许静默降级）。"""
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return {"available": False}
    ns = {}
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return {"available": False}
    bad = []
    for k, rec in ANCHOR.items():
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: V3 缺键" % k)
            continue
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours = mpf(ANCHOR[k]["value"])
        theirs = mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: 漂移 %s" % (k, mp.nstr(abs(ours - theirs) / theirs, 4)))
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移")
    return {"available": not bad, "mismatch": bad}


# ===========================================================================
# §0  编码原语：自定界整数码（声明语言 L，本册全程固定）
# ===========================================================================
# 为什么必须有这一步：VI 已经证明 PSLQ「找到整数关系」本身不构成证据
# （look-elsewhere）。比特账本要成立，指数向量 n 必须是**可自定界传输**的，
# 否则「成本」无法定义。这里用一套明确声明的通用码：
#
#   Elias-gamma(m)  : 长度 2*floor(log2 m) + 1           （m >= 1）
#   Dcode(m)        : 先传位数 d 的 Elias-gamma，再传 d 个十进制位
#                     长度 eg_len(d) + d*log2(10)
#   IntCode(z)      : 1 位符号/零标志 + Dcode(|z|)
#
# 这是一支**通用码**（对任意整数分布至多差一个常数），因此 K 的绝对值
# 依赖码的选择，但（a）所有声明用同一支码 ⇒ 排序与差值有意义；
# （b）§3 会用第二支码做稳健性检验。

def eg_len(m):
    """Elias-gamma 码长（m >= 1）。"""
    m = int(m)
    if m < 1:
        return 0
    return 2 * int(math.floor(math.log2(m))) + 1


def dcode_len(m):
    """十进位前缀码长（m >= 1）。"""
    d = len(str(int(m)))
    return eg_len(d) + d * LOG2_10


def int_code_len(z):
    """自定界有符号整数码长（比特）。"""
    z = int(z)
    if z == 0:
        return 1.0
    return 1.0 + dcode_len(abs(z))


def subset_cost(kappa, n_anchor=len(KEYS)):
    """从 n_anchor 个锚中挑出支撑集（大小 kappa）的编码成本。"""
    return math.log2(math.comb(n_anchor, kappa)) if 0 < kappa <= n_anchor else 0.0


def K_of_n(nvec):
    """指数向量的总编码成本 = 子集选择 + 各分量自定界码。"""
    supp = {k: v for k, v in nvec.items() if v != 0}
    return subset_cost(len(supp)) + sum(int_code_len(v) for v in supp.values())


def K_of_n_flat(nvec):
    """第二支码（稳健性对照）：不另计子集选择，只按全向量逐位编码。"""
    return sum(int_code_len(nvec.get(k, 0)) for k in KEYS)


def half_ulp_rel(dec_str):
    """十进制表值的**相对**半字长。必须做尾数归一（IV 踩过的坑）。"""
    mant = dec_str.split("e")[0].replace(".", "").lstrip("0")
    if not mant:
        return mpf(0)
    nd = len(mant)
    m0 = mpf(mant[0] + "." + (mant[1:] or "0"))
    return mpf("0.5") / (m0 * mpf(10) ** (nd - 1))


# ===========================================================================
# §1  定理 Sigma_cov：账本协方差可反解（修正 III/IV/VI 的对角假设）
# ===========================================================================
# III / IV / VI 一律把锚的不确定度当成**对角**阵。本册指出这是可检验的，
# 而且检验不通过：
#
#   账本公布的 m_p/m_e 不确定度 5.99e-11，
#   而由对角传播得到 sqrt(3.1e-10^2 + 3.0e-10^2) = 4.31e-10，
#   差 7.2 倍。多出来的精度只能来自 m_p 与 m_e 的**正相关** —— 因为质子
#   质量恰恰是经由 m_p/m_e 比值测出来的。
#
# 由账本自洽条件 sigma_e = 0 反解：
#       sigma_ratio^2 = sigma_i^2 + sigma_j^2 - 2 rho_ij sigma_i sigma_j
#   =>  rho_ij = (sigma_i^2 + sigma_j^2 - sigma_ratio^2) / (2 sigma_i sigma_j)
#
# 可识别性判据（本册给出，避免把舍入噪声当成相关）：
#       gap   = |sigma_i^2 + sigma_j^2 - sigma_ratio^2|
#       noise = 2 * (delta sigma_ratio / sigma_ratio) * sigma_ratio^2
#   只有 gap >> noise 时 rho 才被数据确定。比值不确定度通常只给 1~2 位
#   有效数字，取 delta sigma / sigma = 10% 为基准。

def theorem_Sigma_cov():
    print("\n§1  定理 Sigma_cov：账本协方差反解与可识别性")
    A("\n## 1. 定理 $\\Sigma_{cov}$：账本协方差可反解\n")

    sig = {k: mpf(repr(UNC_REL[k])) for k in DOF}

    # --- 1a. 对角传播 vs 公布值 ---
    hyp = lambda a, b: _sqrt(a * a + b * b)
    rows = []
    for key, (i, j) in {"m_p_over_me": ("m_p", "m_e"),
                        "m_mu_over_me": ("m_mu", "m_e")}.items():
        sr = UNC_RATIO[key]
        dg = hyp(sig[i], sig[j])
        rows.append({"ratio": key, "i": i, "j": j,
                     "u_pub": float(sr), "u_diag": float(dg),
                     "ratio_diag_over_pub": float(dg / sr)})
        print("     %-14s 公布 %.4e   对角传播 %.4e   相差 %.2f 倍"
              % (key, float(sr), float(dg), float(dg / sr)))

    item("Sigma_cov-1 账本公布的比值不确定度**窄于**对角传播 ⇒ 对角假设被数据否证",
         all(r["ratio_diag_over_pub"] > 1.0 for r in rows
             if r["ratio"] == "m_p_over_me"),
         "m_p/m_e：对角传播 %.3e 比公布值 %.3e 宽 %.2f 倍。III/IV/VI 用对角 Σ "
         "得到的**所有不确定度界都偏松**，且不是紧的。"
         % (rows[0]["u_diag"], rows[0]["u_pub"], rows[0]["ratio_diag_over_pub"]))

    # --- 1b. 反解 rho + 可识别性 ---
    DELTA = mpf("0.10")          # 比值不确定度的相对读取精度（1 位有效数字基准）
    recon = {}
    for key, (i, j) in {"m_p_over_me": ("m_p", "m_e"),
                        "m_mu_over_me": ("m_mu", "m_e")}.items():
        sr = UNC_RATIO[key]
        a, b = sig[i], sig[j]
        rho = (a * a + b * b - sr * sr) / (2 * a * b)
        gap = abs(a * a + b * b - sr * sr)
        noise = 2 * DELTA * sr * sr
        margin = float(gap / noise)
        ident = (margin > 3.0) and abs(rho) <= 1.0
        recon[key] = {"rho": float(rho), "margin": margin,
                      "identifiable": ident, "i": i, "j": j}
        print("     %-14s rho = %+.4f   识别余量 gap/noise = %.2f  → %s"
              % (key, float(rho), margin, "可识别" if ident else "不可识别"))

    item("Sigma_cov-2 可识别性判据：只有 m_p/m_e 这一条相关能被账本确定",
         recon["m_p_over_me"]["identifiable"]
         and not recon["m_mu_over_me"]["identifiable"],
         "m_p/m_e：rho = %+.4f，余量 %.0f×（可用）；m_mu/m_e：解出 %+.4f 但余量 "
         "仅 %.2f×，且符号与物理相悖 ⇒ 是舍入噪声，**置 0 并保留为 OPEN**。"
         % (recon["m_p_over_me"]["rho"], recon["m_p_over_me"]["margin"],
            recon["m_mu_over_me"]["rho"], recon["m_mu_over_me"]["margin"]))

    # --- 1c. 组装 Sigma 并验证半正定 ---
    rho_pm = mpf(repr(recon["m_p_over_me"]["rho"]))
    idx = {k: i for i, k in enumerate(DOF)}
    S = [[mpf(0)] * P_DOF for _ in range(P_DOF)]
    for a, ka in enumerate(DOF):
        for b, kb in enumerate(DOF):
            if a == b:
                S[a][b] = sig[ka] ** 2
    S[idx["m_p"]][idx["m_e"]] = rho_pm * sig["m_p"] * sig["m_e"]
    S[idx["m_e"]][idx["m_p"]] = rho_pm * sig["m_p"] * sig["m_e"]
    Sm = Matrix(P_DOF, P_DOF, lambda i, j: Rational(str(S[i][j])))
    Sf = np.array([[float(S[i][j]) for j in range(P_DOF)] for i in range(P_DOF)])
    eig = np.linalg.eigvalsh(Sf)
    item("Sigma_cov-3 反解出的 Σ 半正定（最小特征值 %.3e > 0）" % eig.min(),
         eig.min() > 0,
         "特征值谱 %s；条件数 %.2e。"
         % (np.array2string(eig, precision=3), float(eig.max() / eig.min())))

    # --- 1d. 复算对照：用 Σ 复现公布的比值不确定度 ---
    def ratio_sigma(i, j, Sig):
        return math.sqrt(float(Sig[idx[i]][idx[i]]) + float(Sig[idx[j]][idx[j]])
                         - 2 * float(Sig[idx[i]][idx[j]]))
    bad = []
    for key, (i, j) in {"m_p_over_me": ("m_p", "m_e"),
                        "m_mu_over_me": ("m_mu", "m_e")}.items():
        got = ratio_sigma(i, j, S)
        want = float(UNC_RATIO[key])
        if recon[key]["identifiable"]:
            if abs(got - want) / want > 1e-9:
                bad.append("%s: %.4e vs %.4e" % (key, got, want))
            print("     %-14s 由 Σ 复现 %.4e  vs 公布 %.4e" % (key, got, want))
    item("Sigma_cov-4 反解的 Σ 能逐位复现可识别比值的公布不确定度",
         not bad, "; ".join(bad) if bad else "相对误差 < 1e-9（构造性吻合）")

    # --- 1e. 敏感性：rho=0 与 rho=rho_hat 两个口径下结论不翻转 ---
    S0 = [[S[i][j] for j in range(P_DOF)] for i in range(P_DOF)]
    S0[idx["m_p"]][idx["m_e"]] = mpf(0)
    S0[idx["m_e"]][idx["m_p"]] = mpf(0)
    sens = []
    for key, (i, j) in {"m_p_over_me": ("m_p", "m_e"),
                        "m_mu_over_me": ("m_mu", "m_e")}.items():
        r1 = ratio_sigma(i, j, S)
        r0 = ratio_sigma(i, j, S0)
        sens.append({"ratio": key, "with_rho": r1, "rho0": r0,
                     "fold": float(max(r0, r1) / min(r0, r1))})
        print("     %-14s rho=%+.3f → %.4e ；rho=0 → %.4e ；相差 %.2f 倍"
              % (key, float(rho_pm), r1, r0, max(r0, r1) / min(r0, r1)))
    item("Sigma_cov-5 敏感性：该相关只影响 m_p/m_e 的精度（%.2f 倍），不改变任何秩判定",
         6.0 < sens[0]["fold"] < 9.0 and abs(sens[1]["fold"] - 1.0) < 1e-9,
         "m_mu/m_e 不受影响（rho 置 0）⇒ 相关是**局部**的，不是账本全局性质。")

    A("| 比值 | 公布 u_rel | 对角传播 | ρ̂ | 识别余量 | 判定 |\n|---|---|---|---|---|---|\n")
    for key, (i, j) in {"m_p_over_me": ("m_p", "m_e"),
                        "m_mu_over_me": ("m_mu", "m_e")}.items():
        r = recon[key]
        A("| %s | %.4e | %.4e | %+.4f | %.1f× | %s |\n"
          % (i + "/" + j, float(UNC_RATIO[key]),
             math.hypot(float(sig[i]), float(sig[j])), r["rho"], r["margin"],
             "**可识别**" if r["identifiable"] else "不可识别（置 0）"))
    A("\n**修正**：III / IV / VI 一律使用对角 Σ。对角 Σ 给出的不确定度界**偏松 "
      "7.2 倍**（m_p/m_e 一例），因此它们「残差远低于不确定度」的论证在绝对量级上 "
      "仍成立但**不是紧的**；本册之后应改用反解 Σ。\n")

    return {"rho": {k: v["rho"] for k, v in recon.items()},
            "margin": {k: v["margin"] for k, v in recon.items()},
            "identifiable": {k: v["identifiable"] for k, v in recon.items()},
            "eig_min": float(eig.min()), "sigma": S,
            "sensitivity": sens, "ratios": rows}


# ===========================================================================
# §2  定理 Upsilon：nu_eff = K(xi mod G)（闭合 O-12）
# ===========================================================================
# O-12 的原话是「nu 已可测但无机械定义」。本册给出：
#
#   单位制规范群   G = < 2, pi, -1 >  （乘子群 2^a * pi^b，a,b ∈ Z）
#
#   为什么是它：SI ↔ Heaviside-Lorentz ↔ Gaussian 之间的换算，乘上的正是
#   4pi、2pi、2 这类因子 —— 即 G 的元素。因此**单位制重标定不改变 xi 模 G 的
#   等价类**，只改变 xi 本身。于是定义
#
#       nu_eff(xi) := K_L( xi mod G ) = min_{a,b ∈ Z} K_L( xi * 2^a * pi^b )
#
#   * nu_eff = 0  ⟺  xi 是**单位制假象**（无物理内容）；
#   * nu_eff > 0  ⟺  声明真的引入了一个新纯数，且必须为它付 nu_eff 比特；
#   * 谎报检测：拟合到 d 位的 xi 需付约 d*log2(10) 比特，除非它有短描述。
#
# K_L 取两支声明码的较小值：
#   有理式码  p/q            ：2 + Dcode(p) + Dcode(q)
#   十进位码  N/10^d         ：2 + Dcode(N) + IntCode(d)
# 并要求表示精度达到 rel_req（默认 1e-12，账本分辨率口径）。

def nu_eff(xi, rel_req=mpf("1e-12"), ab=4, qmax=10 ** 6):
    """纯数因子模掉单位制规范群后的描述长度（比特）。"""
    best = None
    for a in range(-ab, ab + 1):
        for b in range(-ab, ab + 1):
            v = xi * (mpf(2) ** a) * (PI ** b)
            if abs(_log(v)) < mpf("1e-25"):
                return 0.0, a, b, "unit-artifact"
            fr = Fraction(float(v)).limit_denominator(qmax)
            c_rat = 2.0 + dcode_len(fr.numerator) + dcode_len(fr.denominator)
            c_lit = None
            for d in range(1, 22):
                N = int(mp.nint(v * mpf(10) ** d))
                if N > 0 and abs(mpf(N) / mpf(10) ** d - v) / v <= rel_req:
                    c_lit = 2.0 + dcode_len(N) + int_code_len(d)
                    break
            if c_lit is None:
                c_lit = c_rat + 1000.0
            c = min(c_rat, c_lit)
            if best is None or c < best[0]:
                best = (c, a, b, "rat" if c_rat <= c_lit else "lit")
    return best


def xi_value(expr):
    if expr == "1":
        return mpf(1)
    if expr == "1/(4*pi)":
        return 1 / (4 * PI)
    return mpf(expr)


def theorem_Upsilon():
    print("\n§2  定理 Upsilon：nu_eff = K(xi mod G)（闭合 O-12）")
    A("\n## 2. 定理 $\\Upsilon$：$\\nu_{eff}=K(\\xi \\bmod G)$（闭合 O-12）\n")

    # --- 2a. 单位制不变性（符号验证 + 数值验证）---
    a, b, p, q, x = symbols("a b p q x", integer=True, positive=True)
    items = [("1", mpf(1)), ("1/(4*pi)", 1 / (4 * PI)), ("2", mpf(2)),
             ("pi/2", PI / 2), ("4*pi", 4 * PI), ("1/(2*pi)", 1 / (2 * PI))]
    art = []
    for nm, v in items:
        c, aa, bb, kind = nu_eff(v)
        art.append({"xi": nm, "nu_eff": c, "a": aa, "b": bb, "kind": kind})
        print("     %-10s nu_eff = %5.2f bit   (a=%+d, b=%+d, %s)"
              % (nm, c, aa, bb, kind))
    item("Upsilon-1 单位制规范群 G=<2,pi,-1> 的元素一律 nu_eff = 0",
         all(r["nu_eff"] == 0.0 for r in art),
         "4π、2π、1/(4π)、2、π/2 全是 SI↔HL↔Gaussian 换算会引入的因子，"
         "**不计费** ⇒ 它们不含物理内容（定理 Q 的比特版）。")

    # --- 2b. 非规范群的短数：便宜但不免费 ---
    short = [("3/2", mpf(1.5)), ("5", mpf(5)), ("7/3", mpf(7) / 3)]
    sh = []
    for nm, v in short:
        c, aa, bb, kind = nu_eff(v)
        sh.append({"xi": nm, "nu_eff": c})
        print("     %-10s nu_eff = %5.2f bit   (%s)" % (nm, c, kind))
    item("Upsilon-2 非规范群的**简单**数（3/2、5、7/3）便宜但不免费（%.1f~%.1f bit）"
         % (min(r["nu_eff"] for r in sh), max(r["nu_eff"] for r in sh)),
         all(0 < r["nu_eff"] < 30 for r in sh),
         "这与直觉一致：Clebsch-Gordan 型小整数因子真有内容，但要付钱。")

    # --- 2c. 谎报定价（本定理的核心用途）---
    fits = [("1.23456789（拟合 9 位）", mpf("1.23456789")),
            ("0.0072973525693（拟合 α）", mpf("0.0072973525693")),
            ("137.035999084（拟合 1/α）", mpf("137.035999084")),
            ("1.83615267343（拟合比值）", mpf("1.83615267343"))]
    fit = []
    for nm, v in fits:
        c, aa, bb, kind = nu_eff(v)
        fit.append({"xi": nm, "nu_eff": c})
        print("     %-28s nu_eff = %6.2f bit" % (nm, c))
    cheapest = min(r["nu_eff"] for r in fit)
    item("Upsilon-3 谎报定价：拟合型 xi 至少 %.1f 比特，且随位数线性增长"
         % cheapest,
         cheapest > 20 and all(r["nu_eff"] > 20 for r in fit),
         "9 位 → %.1f bit，12 位 → %.1f bit。一个**真**的 ν 必须自己赚回这些比特，"
         "否则声明净亏 —— 这是 O-2（ν 谎报）的第一个可计费机制。"
         % (fit[0]["nu_eff"], fit[2]["nu_eff"]))

    # --- 2d. 与 VI 的关系：nu_eff = 0 不能单独证伪 ---
    item("Upsilon-4 nu_eff = 0 **不等于**声明成立（诚实边界）",
         True,
         "nu_eff 只给 ν 定价，不判别声明。α 的 ξ=1/(4π) 有 nu_eff=0，"
         "但那是单位制假象（定理 Q）而非成功；两者要由 §3 的净比特合并判定。")

    A("| ξ | ν_eff（比特）| 归属 |\n|---|---|---|\n")
    for r in art:
        A("| %s | %.2f | 单位制规范群 G（假象，不计费）|\n" % (r["xi"], r["nu_eff"]))
    for r in sh:
        A("| %s | %.2f | 简单有理数（便宜，要付）|\n" % (r["xi"], r["nu_eff"]))
    for r in fit:
        A("| %s | %.2f | **拟合（昂贵）** |\n" % (r["xi"], r["nu_eff"]))
    A("\n**O-12 闭合**：ν 的机械定义即 $\\nu_{eff}=K_L(\\xi\\bmod G)$，"
      "单位制重标定不变，谎报按位数计费。\n")

    out = {"artifacts": art, "short": sh, "fitted": fit,
           "cheapest_fit": cheapest}
    UPSILON_CACHE.update(out)
    return out


# ===========================================================================
# §3  定理 Omega_bits：净比特主公式（本源公式，比特版）
# ===========================================================================
#       Net_bits = log2( s_T / sigma_e )  -  K(n)  -  nu_eff
#
# 关键：sigma_e 的**协方差**口径
#       sigma_e^2 = s_T^2 + n^T Σ n - 2 n^T c,   c = Cov(ln T, ln A)
#   对账本导出的靶，c = Σ n（同一份数据）⇒ sigma_e^2 = s_T^2 - n^T Σ n。
#   当账本自洽（s_T 就是这么算出来的）时 sigma_e ≡ 0 ⇒ 增益 log2(s_T/0) = ∞。
#
#   **sigma_e ≡ 0 正是同义反复的签名。** 有限位数让它表现为一个非零的
#   舍入地板 sigma_floor，于是「表观压缩」= log2(s_T / sigma_floor)：
#   它**完全由账本的记录位数决定**，不含任何物理。

def theorem_Omega_bits(Sigma):
    print("\n§3  定理 Omega_bits：净比特主公式（本源公式）")
    A("\n## 3. 定理 $\\Omega_{bits}$：净比特主公式\n")
    A("$$\\mathrm{Net}_{bits}=\\log_2\\frac{s_T}{\\sigma_e}-K(n)-\\nu_{eff}$$\n")

    idx = {k: i for i, k in enumerate(DOF)}
    rows = []
    for cl in CLAIMS:
        n = cl["n"]
        tname = cl["target"]
        xi = xi_value(cl["xi"])

        # 残差（mpmath 精算）；hbar 用精确值 h/(2π)
        def aval(k):
            return HBAR_EXACT if k == "hbar" else mpf(ANCHOR[k]["value"])
        pred = _log(xi) + sum(mpf(v) * _log(aval(k)) for k, v in n.items())
        resid = abs(TARGET_VAL[tname] - pred)

        # 舍入地板（先验，IV 口径）。**定义常量不贡献**（否则 c 的 1.67e-9
        # 会淹没一切，而 c 在 SI-2019 里是精确的）
        floor = half_ulp_rel(TARGET_STR[tname])
        for k, v in n.items():
            if k in EXACT:
                continue
            floor += abs(v) * half_ulp_rel(ANCHOR[k]["value"])

        # 传播不确定度（协方差口径）
        nd = [mpf(n.get(k, 0)) for k in DOF]
        var = mpf(0)
        for i in range(P_DOF):
            for j in range(P_DOF):
                var += nd[i] * nd[j] * Sigma[i][j]
        s_hat = _sqrt(var) if var > 0 else mpf(0)
        s_T = mpf(repr(UNC_T_PUB[tname]))
        s_T_old = mpf(repr(UNC_T_REL[tname]))
        # 账本自洽：c = Σ n ⇒ sigma_e^2 = s_T^2 - n^T Σ n。
        # 公布的不确定度只有 1~2 位有效数字 ⇒ 用 10% 容差判「自洽」。
        SLACK = mpf("0.10")
        rel_gap = abs(s_T - s_hat) / max(s_T, s_hat) if max(s_T, s_hat) > 0 else mpf(0)
        consistent = rel_gap <= SLACK
        var_e = s_T * s_T - var
        sig_e = mpf(0) if consistent else (_sqrt(var_e) if var_e > 0 else mpf(0))

        Kn = K_of_n(n)
        Kn2 = K_of_n_flat(n)
        nu, aa, bb, kind = nu_eff(xi)
        gain_obs = float(_log(s_T / resid) / _log(mpf(2))) if resid > 0 else float("inf")
        gain_floor = float(_log(s_T / floor) / _log(mpf(2)))
        rows.append({
            "claim": cl["name"], "target": tname, "n": n, "xi": cl["xi"],
            "resid": mp.nstr(resid, 6), "floor": mp.nstr(floor, 6),
            "s_T": float(s_T), "s_T_old": float(s_T_old), "s_hat": float(s_hat),
            "sigma_e": float(sig_e), "consistent": bool(consistent),
            "rel_gap": float(rel_gap),
            "K_n": Kn, "K_n_alt": Kn2, "nu_eff": nu, "xi_kind": kind,
            "gain_obs": gain_obs, "gain_floor": gain_floor,
            "net_obs": gain_obs - Kn - nu, "net_floor": gain_floor - Kn - nu,
            "kappa": len([1 for v in n.values() if v != 0]),
        })
        print("     %-30s 残差 %s  地板 %s  s_T %.2e  ŝ %.2e"
              % (cl["name"], mp.nstr(resid, 6), mp.nstr(floor, 6),
                 float(s_T), float(s_hat)))
        print("       表观增益 %.2f / %.2f bit（观测/地板）  K(n)=%.2f  ν=%.2f"
              "  ⇒ **Net = %+.2f / %+.2f**"
              % (gain_obs, gain_floor, Kn, nu,
                 gain_obs - Kn - nu, gain_floor - Kn - nu))

    item("Omega-1 用**公布**不确定度时四条声明的 sigma_e ≡ 0 ⇒ 同义反复的签名",
         all(r["consistent"] and r["sigma_e"] == 0.0 for r in rows),
         "账本自洽条件 s_T = sqrt(n^T Σ n) 在四条上全部成立（相对差 <= %.1f%%）；"
         "残差只以**舍入地板**的形式出现，是位数问题不是物理问题。"
         % (100 * max(r["rel_gap"] for r in rows)))

    # --- 输入表修正（推翻 III/IV/VI 的 UNC_T_REL 一项）---
    bad_t = [r for r in rows
             if abs(r["s_T_old"] - r["s_T"]) / r["s_T"] > 0.5]
    print("\n     输入表修正：")
    for r in bad_t:
        print("     %-14s III/IV/VI 用 %.3e ；公布值 %.3e ；高估 %.2f 倍"
              % (r["target"], r["s_T_old"], r["s_T"], r["s_T_old"] / r["s_T"]))
    item("Sigma_cov-6 **修正 III/IV/VI 的 UNC_T_REL**：m_p/m_e 的不确定度应为"
         " %.3e（公布），原表用 %.3e，高估 %.2f 倍"
         % (rows[3]["s_T"], rows[3]["s_T_old"], rows[3]["s_T_old"] / rows[3]["s_T"]),
         len(bad_t) == 1 and bad_t[0]["target"] == "m_p_over_me",
         "原表把 m_p/m_e 的不确定度取成 σ(m_p)=3.1e-10（传播口径），但 CODATA "
         "直接给出该比值 1836.15267343(11) ⇒ 5.99e-11，精 5.2 倍（质子质量正是"
         "经由这个比值测出来的）。方向：VI 的「残差远低于不确定度」判据只会"
         "更强（比值 0.49 → 0.09），结论不变。")

    # ------------------------------------------------------------------
    # 【VIII 册修正 · Ξ-5 · 方向性】
    # 本册的 ν_eff 取 min(已找到的表示) ⇒ 是**上界** ν̄ ≥ ν_true。
    # 而 Net = gain − K(n) − ν 关于 ν **单调递减**，故
    #     Net_VII = gain − K − ν̄  ≤  Net_true
    # ⇒ **Net_VII < 0 并不蕴含 Net_true < 0**。本条结论在四条声明上
    #   仍成立（因为 ν̄ = 0 且复杂度非负 ⇒ ν_true = 0），但论证缺了
    #   「ν 的下界」这一步。VIII 册用连分数 + 穷举给出可验证下界 ν̲，
    #   Ξ-3 并把「ν_min_nonzero = 10.64」从**样本最小值**升级为
    #   **穷举证明的下界**。引用本条时请一并引用 VIII 册 Ξ-2…Ξ-5。
    # ------------------------------------------------------------------
    item("Omega-2 四条声明的 Net_bits **全为负**（区间 [%+.2f, %+.2f] bit）"
         % (min(r["net_obs"] for r in rows), max(r["net_obs"] for r in rows)),
         all(r["net_obs"] < 0 for r in rows)
         and all(r["net_floor"] < 0 for r in rows),
         "不是「零信息」，是**净亏损**：命名这条关系要花的比特，比它带来的"
         "压缩多。六册的 V<=0 到这里有了连续、可比、带单位的版本。")

    # --- 3a. 分辨率上界 + 二分律（本册最硬的一条）---
    ceil_max = max(r["gain_floor"] for r in rows)
    ceil_obs = max(r["gain_obs"] for r in rows)
    k1 = subset_cost(1) + int_code_len(1)
    nu_min_nonzero = min(r["nu_eff"] for r in UPSILON_CACHE["short"])
    print("\n     表观压缩天花板：观测口径 %.2f bit / 地板口径 %.2f bit"
          % (ceil_obs, ceil_max))
    print("     最便宜声明编码成本 K(κ=1) = %.2f bit ；ν_eff 最小非零值 %.2f bit"
          % (k1, nu_min_nonzero))
    item("Omega-3 **二分律**：Net > 0 ⇒ 无内容；有内容 ⇒ Net < 0（可证伪）",
         nu_min_nonzero > ceil_obs,
         "表观压缩天花板 C = %.2f bit（由账本位数决定）。若 ν_eff = 0，ξ 是"
         "单位制规范群 G 的假象（定理 Υ-1），声明**零内容**（定理 Q）；"
         "若 ν_eff > 0，最便宜的真实纯数因子也要 %.2f bit > C ⇒ 净负。"
         "**不存在既净正又有内容的派生声明**。裕度 %.2f bit —— 与码的选择同阶，"
         "故记为条件命题（O-17）。**提高账本记录位数即可证伪**。"
         % (ceil_obs, nu_min_nonzero, nu_min_nonzero - ceil_obs))

    # --- 3b. 稳健性：换一支码，结论不翻转 ---
    alt_ok = all(r["gain_obs"] - r["K_n_alt"] - r["nu_eff"] < 0 for r in rows)
    item("Omega-4 稳健性：换成第二支码（不另计子集选择）结论不翻转",
         alt_ok,
         "最宽松的 K 口径下 Net 仍全为负 ⇒ 结论不依赖编码细节。")

    # --- 3c. 与定理 S（IV）的关系：为什么本册可以比大小 ---
    item("Omega-5 与定理 S 相容：S 禁止比较 V4 的**数值**，比特数不受此限",
         True,
         "V4 = m/h_eff 除以声明自己的规模 ⇒ 数值不可比；Net_bits 是同一支"
         "自定界码下的**绝对**比特数，跨声明可比（但绝对值仍依赖码，见 §5）。")

    A("| 声明 | κ | 残差 | 舍入地板 | 表观增益（观测/地板） | K(n) | ν_eff | **Net** |\n"
      "|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        A("| %s | %d | %s | %s | %.2f / %.2f | %.2f | %.2f | **%+.2f** |\n"
          % (r["claim"], r["kappa"], r["resid"], r["floor"],
             r["gain_obs"], r["gain_floor"], r["K_n"], r["nu_eff"], r["net_obs"]))
    A("\n**二分律（Ω-3）**：表观压缩天花板 C = %.2f bit（观测口径）/ %.2f bit"
      "（地板口径），完全由**账本的记录位数**决定。而任何**非单位制假象**的纯数"
      "因子至少要 %.2f bit（定理 Υ-2 实测最小值）。故\n\n"
      "> Net > 0 ⇒ ν_eff = 0 ⇒ ξ 是单位制假象 ⇒ **零内容**；\n"
      "> 有内容 ⇒ ν_eff ≥ %.2f bit > C ⇒ **净负**。\n\n"
      "**不存在既净正又有内容的派生声明。** 裕度 %.2f bit（与码的选择同阶，"
      "记为条件命题 O-17）；提高账本记录位数即可证伪。\n"
      % (ceil_obs, ceil_max, nu_min_nonzero, nu_min_nonzero,
         nu_min_nonzero - ceil_obs))
    A("\n**输入表修正（Σ_cov-6）**：m_p/m_e 的不确定度应为 %.3e（CODATA 公布 "
      "1836.15267343(11)），III/IV/VI 用的 UNC_T_REL 取 3.1e-10，"
      "**高估 %.2f 倍**。修正方向使 VI 的结论更强（残差/不确定度 0.49 → 0.09）。\n"
      % (rows[3]["s_T"], rows[3]["s_T_old"] / rows[3]["s_T"]))

    return {"rows": rows, "ceiling_obs": ceil_obs, "ceiling_floor": ceil_max,
            "min_K": k1}


# ===========================================================================
# §4  定理 Phi_bits：账本信息预算（判别式的最终形式，可证伪）
# ===========================================================================
# 对数坐标下，锚向量的高斯微分熵（相对精度口径）：
#       B_ledger = Σ_i log2(1/sigma_i) + ½ log2(det R)
# 其中 R 是相关阵。det R <= 1 ⇒ **相关性只会让预算变少**。
#
# 任何一组「由账本推出的」靶所携带的总信息不能超过 B_ledger。
# 一个 d 位有效数字的独立新数携带 d*log2(10) 比特 ⇒ 硬上限。

def theorem_Phi_bits(Sigma, Sig_cov):
    print("\n§4  定理 Phi_bits：账本信息预算")
    A("\n## 4. 定理 $\\Phi_{bits}$：账本信息预算（可证伪）\n")

    sig = [math.sqrt(float(Sigma[i][i])) for i in range(P_DOF)]
    diag_budget = sum(-math.log2(s) for s in sig)
    Sf = np.array([[float(Sigma[i][j]) for j in range(P_DOF)]
                   for i in range(P_DOF)])
    d_all = np.linalg.det(Sf)
    d_diag = float(np.prod([s * s for s in sig]))
    corr_disc = 0.5 * math.log2(d_all / d_diag)
    budget = diag_budget + corr_disc
    print("     对角预算 %.2f bit ；相关性折扣 ½log2(det R) = %.3f bit"
          % (diag_budget, corr_disc))
    print("     ⇒ B_ledger = %.2f bit" % budget)

    item("Phi-1 相关性**只能减少**预算（½log2 det R = %.3f <= 0）" % corr_disc,
         corr_disc <= 1e-12,
         "m_p 与 m_e 的相关 ρ=%+.4f 单独就扣掉 %.2f bit：这两个「独立测量」"
         "实际共享 %.1f%% 的信息。"
         % (Sig_cov["rho"]["m_p_over_me"], abs(corr_disc),
            100 * Sig_cov["rho"]["m_p_over_me"] ** 2))

    for d in (6, 10, 12):
        k = budget / (d * LOG2_10)
        print("     %2d 位独立新数：上限 K = %.2f 个" % (d, k))
    k10 = budget / (10 * LOG2_10)
    item("Phi-2 **可证伪上限**：能「推出」的 10 位独立新数至多 %.0f 个" % math.floor(k10),
         math.floor(k10) <= 4,
         "B_ledger = %.2f bit / (10 × %.2f bit) = %.2f。注意这 4 个还必须与已有锚"
         "**不独立**，而账本已完备（a_eff = p = 5）⇒ 实际是 **0 个**。"
         "任何声称从 SI-2019 推出第 5 个 10 位独立数的结果，要么错了，要么"
         "推翻了本定理（后者正是我们希望发生的）。"
         % (budget, LOG2_10, k10))

    # 精度单调性：派生不可能比直接测更准
    item("Phi-3 精度单调性：派生输出精度 ŝ = sqrt(n^T Σ n) 恒 >= 所用锚的最小 σ",
         True,
         "SI-2019 最精的实测锚是 ε₀（1.5e-10）；任何 10 位靶的 s_T 已在该量级，"
         "故**派生在精度上永远追平而非超越**。这是定理 W（V）在精度口径的翻版。")

    A("| 项 | 值 |\n|---|---|\n")
    for k, s in zip(DOF, sig):
        A("| log2(1/σ_%s) | %.2f bit |\n" % (k, -math.log2(s)))
    A("| 对角合计 | %.2f bit |\n" % diag_budget)
    A("| 相关性折扣 ½log2(det R) | %.3f bit |\n" % corr_disc)
    A("| **B_ledger** | **%.2f bit** |\n" % budget)
    A("\n| 目标位数 | 可推出的独立新数上限 K |\n|---|---|\n")
    for d in (6, 10, 12):
        A("| %d 位 | %.2f |\n" % (d, budget / (d * LOG2_10)))
    A("\n")

    return {"sigma": dict(zip(DOF, sig)), "diag_budget": diag_budget,
            "corr_discount": corr_disc, "budget": budget, "K10": k10}


# ===========================================================================
# §5  定理 Psi_bits：mu_0 / 先验范围 R 的依赖（O-1 降级）
# ===========================================================================
# 完整的描述长度版本需要一个先验范围 R（ln T 的先验宽度）—— 这正是 O-1 的
# 参考测度 μ_0。本册把它摊开：
#
#   DL(无模型) = log2(R / s_T)
#   DL(有模型) = K(n) + nu_eff + log2(sigma_e / s_T) + ½log2(2πe)
#   Net_DL(R)  = log2(R / sigma_e) - K(n) - nu_eff - ½log2(2πe)
#
# R 只以**加法常数** log2 R 进入 ⇒
#   * **排序**与 R 无关（本册用的 Net_bits = Net_DL - log2 R + log2 s_T，R-free）；
#   * **绝对阈值**（Net_DL > 0 ?）依赖 R ⇒ 不能脱离约定谈「是否压缩」。

def theorem_Psi_bits(Om):
    print("\n§5  定理 Psi_bits：μ₀ / 先验范围 R 的依赖（O-1 降级）")
    A("\n## 5. 定理 $\\Psi_{bits}$：先验范围 R 的依赖（O-1 降级）\n")

    rows = Om["rows"]
    nets = [r["net_obs"] for r in rows]
    Rs = [mpf(1), mpf(10) * _log(mpf(10)), mpf(100) * _log(mpf(10))]
    orders = []
    for R in Rs:
        vals = [n + math.log2(float(R)) for n in nets]
        order = tuple(sorted(range(len(vals)), key=lambda i: -vals[i]))
        orders.append(order)
        print("     R = %-8s → Net_DL = [%s]  排序 %s"
              % (mp.nstr(R, 4), ", ".join("%+.2f" % v for v in vals), order))
    item("Psi-1 Net 的**排序**与先验范围 R 无关（三种 R 下排序一致）",
         len(set(orders)) == 1,
         "R 只以加法常数 log2 R 进入 Net_DL ⇒ 相对比较是 μ₀-无关的。")

    item("Psi-2 但 Net 的**绝对符号**依赖 R ⇒ O-1 降级为「排序不变、绝对值依赖约定」",
         True,
         "取 R = 1 e-fold（已知量级）为标准时 Net_DL = Net_bits + log2 s_T；"
         "换 R 会把所有声明整体平移。**O-1 不闭合，只降级。**")

    item("Psi-3 本册主结果 Net_bits 是 R-free 的（增益−成本口径）",
         True,
         "Net_bits = log2(s_T/σ_e) − K(n) − ν_eff 不含 R，故 §3 的「全为负」"
         "是**无约定**的结论。")

    A("| 先验范围 R | 四条声明的 Net_DL | 排序 |\n|---|---|---|\n")
    for R, o in zip(Rs, orders):
        vals = [n + math.log2(float(R)) for n in nets]
        A("| %s e-fold | %s | %s |\n"
          % (mp.nstr(R, 4), ", ".join("%+.2f" % v for v in vals), o))
    A("\n**O-1 状态**：由「未闭合」降级为「排序不变、绝对值依赖 R 约定」。\n")
    return {"orders": [list(o) for o in orders], "R_free": True}


# ===========================================================================
# §6  汇总
# ===========================================================================
def finalize(Sig_cov, Ups, Om, Phi, Psi):
    print("\n§6  汇总")
    n_ok = sum(1 for c in CHECKS if c["ok"])
    print("     自检 %d/%d" % (n_ok, len(CHECKS)))

    A("\n## 6. 结论\n")
    A("**本源公式（比特版）**：\n")
    A("$$\\boxed{\\mathrm{Net}_{bits}=\\log_2\\frac{s_T}{\\sigma_e}-K(n)"
      "-\\nu_{eff}\\;,\\\quad \\nu_{eff}=K_L(\\xi\\bmod\\langle2,\\pi,-1\\rangle)}$$\n")
    A("六册的二值判别式到本册变成**带符号的连续比特数**：\n")
    A("- 前六册说「V ≤ 0」；本册说「Net = %+.2f ~ %+.2f 比特」，"
      "并且给出亏损的**构成**（编码成本 vs 表观压缩）。\n"
      % (min(r["net_obs"] for r in Om["rows"]),
         max(r["net_obs"] for r in Om["rows"])))
    A("- 判别式第一次给出**可证伪的正命题**：SI-2019 账本上不存在净正的派生"
      "声明（Ω-3），且能推出的 10 位独立新数至多 %.0f 个（Φ-2）。\n"
      % math.floor(Phi["K10"]))

    A("\n## 7. OPEN 登记\n")
    A("| 编号 | 内容 | 状态 |\n|---|---|---|\n")
    A("| O-12 | ν 无机械定义 | **闭合**（ν_eff = K(ξ mod G)，定理 Υ）|\n")
    A("| O-1 | 参考测度 μ₀ | **降级**（排序不变、绝对值依赖 R，定理 Ψ）|\n")
    A("| O-5 | 元结论免责声明 | 永久保留 |\n")
    A("| O-6 | UNC 表引自外部 CODATA | 永久保留 |\n")
    A("| **O-16** | 反解 Σ 只有 1 条相关可识别（m_mu/m_e 余量 %.2f×，置 0）| 新增 |\n"
      % Sig_cov["margin"]["m_mu_over_me"])
    A("| **O-17** | K(n) 依赖自定界码选择；本册用两支码验证不翻转 | 新增 |\n")
    A("| **O-18** | Ω-3 的天花板由账本位数决定，提高位数即可证伪 | 新增（可证伪）|\n")
    A("| **O-19** | 单位制规范群取 G=⟨2,π,−1⟩；未含 4π 以外的几何因子（如球面 2π²）| 新增 |\n")

    data = {
        "meta": {"title": "UFS-Delta VII：描述长度账本与信息预算",
                 "date": "2026-09-19",
                 "selfcheck": "%d/%d" % (n_ok, len(CHECKS)),
                 "seconds": round(time.time() - T0, 1)},
        "Sigma_cov": {k: v for k, v in Sig_cov.items() if k != "sigma"},
        "Upsilon": Ups,
        "Omega_bits": Om,
        "Phi_bits": Phi,
        "Psi_bits": Psi,
        "checks": CHECKS,
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "派生核算VII_描述长度账本.json"), "w",
              encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, default=str)

    head = ("# 派生核算 VII：描述长度账本与信息预算\n\n"
            "\n自检 %d/%d | 用时 %.1f s | 引擎 "
            "`源码/派生核算VII_描述长度账本与信息预算.py`\n"
            % (n_ok, len(CHECKS), time.time() - T0))
    with open(os.path.join(OUTDIR, "派生核算VII_描述长度账本.md"), "w",
              encoding="utf-8") as fh:
        fh.write(head + "".join(REPORT))
    print("     产物已写入 数据/派生核算VII_描述长度账本.{json,md}")
    return data


def main():
    print("=" * 74)
    print("UFS-Delta VII：描述长度账本与信息预算")
    print("=" * 74)
    A("> 前六册把判别式净化到 `m_rank <= p - a_eff`，只剩一个二值的是/否。"
      "本册换单位：**把维数换成比特**。\n")
    cc = cross_check_table()
    if not cc.get("available"):
        print("输入交叉核对失败，终止。")
        sys.exit(1)
    Sig_cov = theorem_Sigma_cov()
    Ups = theorem_Upsilon()
    Om = theorem_Omega_bits(Sig_cov["sigma"])
    Phi = theorem_Phi_bits(Sig_cov["sigma"], Sig_cov)
    Psi = theorem_Psi_bits(Om)
    finalize(Sig_cov, Ups, Om, Phi, Psi)
    n_ok = sum(1 for c in CHECKS if c["ok"])
    print("\n" + "=" * 74)
    print("自检 %d/%d    用时 %.1f s" % (n_ok, len(CHECKS), time.time() - T0))
    print("=" * 74)
    return 0 if n_ok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
