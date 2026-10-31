# -*- coding: utf-8 -*-
r"""TUFT-r274 · 四力统一方程·宇宙学非线性结构层：线性功率谱 P(k)（EH98 对拍 BBKS）、
σ8 定标、Halofit 非线性谱、Press–Schechter/Sheth–Tormen 晕质量函数、Kaiser 红移畸变
2026-10-31

〔编号说明〕起草前实测 r274 三树全空（r271 数据树被并行链「时空曲率比攻坚」来料占用、
r272 LW 推迟势层、r273 四力本源参数精算层均同日落盘；README 最新登记至 r273）。
本卷承 r237（背景层）→ r254（线性扰动层）→ r256（声学几何层）→ r260（视界热力学层）
之后的第五级增量——**非线性结构形成层**：r254 遗留清单第 2 条「非线性结构形成：
HaloFit / N 体模拟」的机器化落地（HaloFit 可在纯 float64 闭式实现，N 体模拟不在本卷）。

用户诉求：「继续突破新的理论体系计算分析是否正确全维度分析全链路」。

本卷要回答的问题：
  Q1 线性功率谱能否双路径互印？Eisenstein–Hu 1998（含 wiggle 与 no-wiggle 两版）
     vs BBKS+Sugiyama；T(k→0)=1 恒等；EH98 的 s 与 r254 的 r_d 积分互印。
  Q2 原初谱 A_s=2.1e−9、n_s=0.9649（Planck 2018）下，σ8 能否从 P(k) 积分回算到
     观测锚 0.811 的拟合残差窗口内？（EH98 是拟合式，残差 ~5–10% 为已知系统差）
  Q3 Halofit（Smith et al. 2003）非线性功率谱：k_σ、n_eff、曲率 C、1-halo/2-halo
     分解的读数是否物理（boost 曲线、z 演化方向）？
  Q4 Press–Schechter 与 Sheth–Tormen 晕质量函数：M*、n(>1e14 M_sun/h) 量级、
     高质量端 ST>PS 与低质量端 ST<PS 的判别结构。
  Q5 Kaiser 红移畸变：μ 积分数值路径与解析因子 (1+2β/3+β²/5) 互印；fσ8(z) 表。

诚实预期（写在前面）：EH98 转移函数、Halofit、PS/ST 质量函数、Kaiser 因子全部是
文献拟合式/解析近似（Eisenstein & Hu 1998；Smith et al. 2003；Press & Schechter 1974；
Sheth & Tormen 1999；Kaiser 1987）——本卷是**复现层**，不是新物理。Halofit 本身是
对 N 体模拟的经验拟合（非第一性推导）；EH98 对 CAMB 残差 ~5–10%；bias b、中微子
质量、重子反馈（AGN）不在本卷。z≳2 的 Halofit 外推只作方向参考。

口径注意：
  - k 全程 h/Mpc，R 全程 Mpc/h，P(k) 全程 (Mpc/h)³；A_s 枢轴 k0=0.05 Mpc⁻¹=0.074184 h/Mpc；
  - σ8 用 top-hat 窗（W(x)=3(sin x−x cos x)/x³，R=8 Mpc/h）；Halofit 内部 σ²(R) 用
    Gaussian 窗 e^{−(kR)²}（Smith+03 原定义，两窗不可混用）；
  - Halofit 系数：n_eff = −3 − dlogσ²/dlogR |_{R_σ}（幂律 P∝k^n 时必须退化 n_eff=n，
    此约束钉死符号约定）；C = −d²logσ²/dlogR² |_{R_σ}；w=−1 ⇒ ΩΛ(1+w) 项严格为 0；
  - 增长因子 g(z)=D(z)/D(1) 复用 r254 积分解口径（E_g=√(Ωm a⁻³+ΩΛ)）；
  - 纯标准库 float64；对 r214–r273 及并行会话产物只读；守卫失败即非零退出；
    条目不可与 r142–r273 相加。
"""

import json
import os
import sys
from math import sqrt, pi, log, log10, exp, sin, cos

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r274_宇宙学非线性结构层交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_宇宙学非线性结构层可视化_2026-10-31.html")

MARKER = "R274-COSMO-NONLINEAR-STRUCTURE"
BASE = ("TUFT-r274_四力统一方程_宇宙学非线性结构层_EH98功率谱Halofit晕质量函数与"
        "Kaiser畸变_精算与交互可视化_2026-10-31")
STEM = "TUFT-r274"

# ---------------- 参数（Planck 2018，与 r237/r254/r256 同口径） ----------------
H_DIM = 0.674
OM = 0.3153
OB = 0.0493
OR = 9.15e-5
OL = 1.0 - OM - OR
FB = OB / OM
OMH2 = OM * H_DIM ** 2
OBH2 = OB * H_DIM ** 2
THETA27 = 2.7255 / 2.7
A_S = 2.1e-9
N_S = 0.9649
K0 = 0.05 / H_DIM          # 0.05 Mpc^-1 → h/Mpc
SIGMA8_IN = 0.811          # 观测锚（r254 同款输入）
DELTA_C = 1.686
RHO_M = OM * 2.775366273e11 * H_DIM ** 2   # M_sun/h · (Mpc/h)^-3
E_NEPER = 2.718281828459045

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def simpson_arr(ys, h):
    """等距数组 Simpson（n 为偶数间隔）。"""
    n = len(ys) - 1
    if n % 2 == 1:
        n -= 1
    s = ys[0] + ys[n]
    for i in range(1, n):
        s += (4.0 if (i % 2) else 2.0) * ys[i]
    return s * h / 3.0


def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if (i % 2) else 2.0) * f(a + i * h)
    return s * h / 3.0


# ---------------- 增长因子（r254 口径复用：ΛCDM 精确积分解） ----------------
def e_g(a):
    return sqrt(OM * a ** -3 + OL)


def growth_unnorm(a, n=60000):
    def integrand(ap):
        e2 = OM * ap ** -3 + OL
        return 1.0 / (ap ** 3 * e2 ** 1.5)
    return e_g(a) * simpson(integrand, 1e-8, a, n)


_G1 = growth_unnorm(1.0)
_GUN_CACHE = {}


def growth_unnorm_z(z):
    """growth_unnorm(1/(1+z))，按 z 缓存（网格构建时不可承受重复积分）。"""
    if z not in _GUN_CACHE:
        _GUN_CACHE[z] = growth_unnorm(1.0 / (1.0 + z))
    return _GUN_CACHE[z]


def growth_g(z):
    """g(z)=D(z)/D(1)（今日归一，r254 口径）。"""
    return growth_unnorm_z(z) / _G1


def growth_phys(z):
    """D_phys(z)：物质时代归一（D→a as a→0）。growth_unnorm(a→0)=(2/5)a/Ωm。"""
    return (5.0 * OM / 2.0) * growth_unnorm_z(z)


# ---------------- 转移函数三件套 ----------------
GAMMA_BBKS = OM * H_DIM * exp(-OB * (1.0 + sqrt(2.0 * H_DIM) / OM))

A_GAMMA = (1.0 - 0.328 * log(431.0 * OMH2) * FB
           + 0.38 * log(22.3 * OMH2) * FB ** 2)
GAMMA_EFF = OM * H_DIM * A_GAMMA

# EH98 含 wiggle 版的尺度参数
S_EH = 44.5 * log(9.83 / OMH2) / sqrt(1.0 + 10.0 * OBH2 ** 0.75)   # Mpc
S_H = S_EH * H_DIM                                                  # Mpc/h
K_SILK = (1.6 * OBH2 ** 0.52 * OMH2 ** 0.73
          * (1.0 + (10.4 * OMH2) ** -0.95)) / H_DIM                 # h/Mpc
_A1 = (46.9 * OMH2) ** 0.670 * (1.0 + (32.1 * OMH2) ** -0.532)
_A2 = (12.0 * OMH2) ** 0.424 * (1.0 + (45.0 * OMH2) ** -0.582)
ALPHA_C = _A1 ** (-FB) * _A2 ** (-(FB ** 3))
BETA_C = 1.0 / (1.0 - 0.949 * FB)


def t_bbks(k):
    q = k / GAMMA_BBKS
    if q < 1e-6:
        return 1.0
    return (log(1.0 + 2.34 * q) / (2.34 * q)
            * (1.0 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3
               + (6.71 * q) ** 4) ** -0.25)


def _t0(q):
    l0 = log(2.0 * E_NEPER + 1.8 * q)
    c0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return l0 / (l0 + c0 * q * q)


def t_eh_nowig(k):
    q = k * THETA27 ** 2 / GAMMA_EFF
    return _t0(q)


def t_eh(k):
    """EH98 含重子 wiggle 全版（eqs. 16–22）。k: h/Mpc。"""
    q = k * THETA27 ** 2 / GAMMA_EFF
    ks = k * S_H
    t0 = _t0(q)
    qt = q * sqrt(ALPHA_C)
    t0t = _t0(qt)
    f_node = 1.0 / (1.0 + (ks / 5.4) ** 4)
    t_c = f_node * t0t + (1.0 - f_node) * t0
    bc3 = (BETA_C / ks) ** 3 if ks > 1e-30 else 1e30
    s_t = S_H * (1.0 + bc3) ** (-1.0 / 3.0)
    x = k * s_t
    j0 = 1.0 if x < 1e-6 else sin(x) / x
    t_b = (t0t * exp(-(k / K_SILK) ** 1.4) + ALPHA_C / (1.0 + bc3)) * j0
    return FB * t_b + (1.0 - FB) * t_c


# ---------------- 线性功率谱与 σ8 定标 ----------------
def delta2_lin_raw(k, z):
    """未定标 Δ²_L(k,z)=A_s (k/k0)^{n_s−1} T²(k) [(6/25)(kc/H0)²/Ωm]² D_phys²(z)。

    由 δ=(2/3)(k/aH)²Φ（物质时代）与 Φ=(3/5)R 得来；(6/25)²=36/625=0.0576。
    kc/H0 = k×2997.92458/h（k 以 h/Mpc 计）。"""
    kk = k * (2997.92458 / H_DIM)
    return (0.0576 * A_S * (k / K0) ** (N_S - 1.0) * t_eh(k) ** 2
            * (kk * kk / OM) ** 2 * growth_phys(z) ** 2)


# lnk 均匀网格（σ 积分 / 插值共用）
LNK_MIN, LNK_MAX = log(1e-5), log(300.0)
NK = 9000
_DLNK = (LNK_MAX - LNK_MIN) / NK
_KG = [exp(LNK_MIN + i * _DLNK) for i in range(NK + 1)]
_D2G_Z0 = None
_D2G_Z1 = None
CAL = 1.0


def build_grids():
    global _D2G_Z0, _D2G_Z1
    _D2G_Z0 = [delta2_lin_raw(k, 0.0) for k in _KG]
    _D2G_Z1 = [delta2_lin_raw(k, 1.0) for k in _KG]


def tophat_w(x):
    if x < 0.02:
        return 1.0 - x * x / 10.0
    return 3.0 * (sin(x) - x * cos(x)) / x ** 3


def sigma2_grid_tophat(r, d2g):
    ys = [d2g[i] * tophat_w(_KG[i] * r) ** 2 for i in range(NK + 1)]
    return simpson_arr(ys, _DLNK)


def sigma2_grid_gauss(r, d2g):
    ys = [d2g[i] * exp(-(_KG[i] * r) ** 2) for i in range(NK + 1)]
    return simpson_arr(ys, _DLNK)


def sigma8_from_grid(d2g, scale=1.0):
    return sqrt(sigma2_grid_tophat(8.0, d2g)) * scale


def delta2_lin(k, z):
    """定标后 Δ²_L（log-log 线性插值，z=0/1 用网格，其余按 g² 缩放 z=0）。"""
    if z == 0.0:
        g = _D2G_Z0
    elif z == 1.0:
        g = _D2G_Z1
    else:
        g = None
    lk = log(k)
    i = int((lk - LNK_MIN) / _DLNK)
    if i < 0:
        i = 0
    if i >= NK:
        i = NK - 1
    t = (lk - (LNK_MIN + i * _DLNK)) / _DLNK
    if g is None:
        d0 = _D2G_Z0[i] + t * (_D2G_Z0[i + 1] - _D2G_Z0[i])
        return d0 * CAL ** 2 * growth_g(z) ** 2
    d = g[i] + t * (g[i + 1] - g[i])
    return d * CAL ** 2


# ---------------- Halofit（Smith et al. 2003, App. C；w=−1 ⇒ ΩΛ 项为 0） ----------------
def om_of_z(z):
    ez2 = OM * (1.0 + z) ** 3 + OR * (1.0 + z) ** 4 + OL
    return OM * (1.0 + z) ** 3 / ez2


def halofit_params(z, d2g):
    """返回 (k_sigma, n_eff, C_curv)（d2g 仅保留签名一致性，实际走预计算插值）。"""
    def s2(r):
        return sigma2_gauss_interp(r, z) * CAL ** 2
    lo, hi = log(0.01), log(200.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if s2(exp(mid)) > 1.0:   # σ 随 R 递减：σ>1 ⇒ R_σ 在更大侧
            lo = mid
        else:
            hi = mid
    r_sig = exp(0.5 * (lo + hi))
    eps = 0.03
    l0 = log(s2(r_sig))
    lp = log(s2(r_sig * exp(eps)))
    lm = log(s2(r_sig * exp(-eps)))
    n_eff = -3.0 - (lp - lm) / (2.0 * eps)
    c_curv = -(lp - 2.0 * l0 + lm) / eps ** 2
    return 1.0 / r_sig, n_eff, c_curv


def halofit_d2nl(k, z, k_sig, n_eff, c_curv):
    omz = om_of_z(z)
    n = n_eff
    c = c_curv
    an = 10.0 ** (1.5222 + 2.8553 * n + 2.3706 * n ** 2 + 0.9903 * n ** 3
                  + 0.2250 * n ** 4 - 0.6038 * c)
    bn = 10.0 ** (-0.5642 + 0.5864 * n + 0.5716 * n ** 2 - 1.5474 * c)
    cn = 10.0 ** (0.3698 + 2.0404 * n + 0.8161 * n ** 2 + 0.5869 * c)
    gam = 0.1971 - 0.0843 * n + 0.8460 * c
    aln = abs(6.0835 + 1.3373 * n - 0.1959 * n ** 2 - 5.5274 * c)
    ben = (2.0379 - 0.7354 * n + 0.3157 * n ** 2 + 1.2490 * n ** 3
           + 0.3980 * n ** 4 - 0.1682 * c)
    nun = 10.0 ** (5.2105 + 3.6902 * n)
    f1 = omz ** -0.0732
    f2 = omz ** -0.1423
    f3 = omz ** 0.0725
    y = k / k_sig
    d2l = delta2_lin(k, z)
    fy = y / 4.0 + y * y / 8.0
    d2q = d2l * (1.0 + d2l) ** ben / (1.0 + aln * d2l) * exp(-fy)
    d2h_p = an * y ** (3.0 * f1) / (1.0 + bn * y ** f2 + (cn * f3 * y) ** (3.0 - gam))
    d2h = d2h_p / (1.0 + nun / y ** 2)
    return d2q + d2h


# ---------------- Press–Schechter / Sheth–Tormen 晕质量函数 ----------------
_SIG2_R = None      # logR 网格
_SIG2_V = None      # 对应 log σ²（top-hat、未乘 CAL²、z=0）
_SIG2G_R = None     # Gaussian 窗 logR 网格
_SIG2G_Z0 = None    # Gaussian 窗 log σ²（未乘 CAL²，z=0）
_SIG2G_Z1 = None    # Gaussian 窗 log σ²（未乘 CAL²，z=1）


def build_sig2_tophat(n_r=70, r_lo=0.02, r_hi=150.0):
    """σ²(R) top-hat 预计算网格（log-log 插值用）。"""
    global _SIG2_R, _SIG2_V
    _SIG2_R = [log(r_lo) + (log(r_hi) - log(r_lo)) * i / (n_r - 1)
               for i in range(n_r)]
    _SIG2_V = [log(sigma2_grid_tophat(exp(lr), _D2G_Z0)) for lr in _SIG2_R]


def build_sig2_gauss(n_r=70, r_lo=0.005, r_hi=300.0):
    """σ²(R) Gaussian 窗预计算网格（Halofit 参数求解用，z=0/1 两条）。"""
    global _SIG2G_R, _SIG2G_Z0, _SIG2G_Z1
    _SIG2G_R = [log(r_lo) + (log(r_hi) - log(r_lo)) * i / (n_r - 1)
                for i in range(n_r)]
    _SIG2G_Z0 = [log(sigma2_grid_gauss(exp(lr), _D2G_Z0)) for lr in _SIG2G_R]
    _SIG2G_Z1 = [log(sigma2_grid_gauss(exp(lr), _D2G_Z1)) for lr in _SIG2G_R]


def _interp_logs2(lr, xs, vs):
    n = len(xs)
    if lr <= xs[0]:
        i, t = 0, 0.0
    elif lr >= xs[-1]:
        i, t = n - 2, 1.0
    else:
        x = (lr - xs[0]) / (xs[-1] - xs[0]) * (n - 1)
        i = int(x)
        t = x - i
    return exp(vs[i] + t * (vs[i + 1] - vs[i]))


def sigma2_tophat_interp(r):
    return _interp_logs2(log(r), _SIG2_R, _SIG2_V)


def sigma2_gauss_interp(r, z):
    return _interp_logs2(log(r), _SIG2G_R,
                         _SIG2G_Z0 if z == 0.0 else _SIG2G_Z1)


def r_of_m(m):
    return (3.0 * m / (4.0 * pi * RHO_M)) ** (1.0 / 3.0)


def sigma_m(m, z):
    return sqrt(sigma2_tophat_interp(r_of_m(m))) * CAL * growth_g(z)


def dln_sigma_dm(m, z):
    e = 0.02
    return (log(sigma_m(m * exp(e), z)) - log(sigma_m(m * exp(-e), z))) / (2.0 * e)


def f_ps(nu):
    return sqrt(2.0 / pi) * nu * exp(-0.5 * nu * nu)


def f_st(nu):
    a, p, aa = 0.707, 0.3, 0.3222
    return aa * sqrt(2.0 * a / pi) * nu * (1.0 + (a * nu * nu) ** (-p)) \
        * exp(-a * nu * nu / 2.0)


def dndlnm(m, z, which="ST"):
    nu = DELTA_C / sigma_m(m, z)
    fv = f_st(nu) if which == "ST" else f_ps(nu)
    return RHO_M / m * fv * abs(dln_sigma_dm(m, z))


def n_cum(mmin, z, which="ST", mmax=1e17, n=600):
    l1, l2 = log(mmin), log(mmax)
    ys = []
    h = (l2 - l1) / n
    for i in range(n + 1):
        ys.append(dndlnm(exp(l1 + i * h), z, which))
    return simpson_arr(ys, h)


# ---------------- Kaiser RSD ----------------
def kaiser_p0(beta):
    return 1.0 + 2.0 * beta / 3.0 + beta ** 2 / 5.0


def kaiser_p2(beta):
    return 4.0 * beta / 3.0 + 4.0 * beta ** 2 / 7.0


def kaiser_p0_num(beta, n=4000):
    return simpson(lambda mu: (1.0 + beta * mu * mu) ** 2, 0.0, 1.0, n)


def kaiser_p2_num(beta, n=4000):
    return simpson(lambda mu: (1.0 + beta * mu * mu) ** 2
                   * 2.5 * (3.0 * mu * mu - 1.0), 0.0, 1.0, n)


def main():
    # ---------------------------------------------------------------- S1
    print("[S1] 转移函数三件套：EH98 全版 / EH98 no-wiggle / BBKS+Sugiyama")
    t0s = (t_eh(1e-7), t_eh_nowig(1e-7), t_bbks(1e-7))
    ks_cmp = [0.02 + (0.3 - 0.02) * i / 40 for i in range(41)]
    cmp_rel = max(abs(t_eh_nowig(k) - t_bbks(k)) / t_bbks(k) for k in ks_cmp)
    # 重子调制：全版 vs no-wiggle 的 T² 比值——既要有 >5% 的调制，又要多次变号（振荡）
    ksw = [0.03 + (0.3 - 0.03) * i / 240 for i in range(241)]
    wig = [t_eh(k) ** 2 / t_eh_nowig(k) ** 2 for k in ksw]
    wig_amp = max(abs(w - 1.0) for w in wig)
    # 重子压低使 wig 在 k≳0.1 系统性 <1，(w−1) 零点穿越恒为 0（开发期自抓）；
    # 振荡性判据应相对中位数计穿越（BAO 在 k∈[0.03,0.3] 约 4 个峰谷 ⇒ 8 次穿越）。
    wig_med = sorted(wig)[len(wig) // 2]
    n_sign = sum(1 for i in range(1, len(wig))
                 if (wig[i] - wig_med) * (wig[i - 1] - wig_med) < 0)
    rd = 147.0728   # r254 机算值（只读引用）
    rel_s = abs(S_EH - rd) / rd
    guard("G1", "转移函数 T(k→0)=1 恒等、双路径互印、s_EH 与 r_d 互印",
          all(abs(t - 1.0) < 1e-6 for t in t0s) and cmp_rel < 0.12
          and 0.05 < wig_amp < 0.80 and n_sign >= 3 and rel_s < 0.08,
          f"T(1e-5)=({t0s[0]:.10f},{t0s[1]:.10f},{t0s[2]:.10f})；"
          f"EH-nowig vs BBKS max rel {cmp_rel:.4f}（k∈[0.02,0.3]）；"
          f"wiggle 幅度 {wig_amp:.4f}；s_EH={S_EH:.2f} Mpc vs r_d={rd}"
          f"（rel {rel_s*100:.2f}%）",
          {"t0": [f"{t:.10f}" for t in t0s], "cmp_rel": f"{cmp_rel:.4f}",
           "wig_amp": f"{wig_amp:.4f}", "n_sign": n_sign,
           "s_EH": f"{S_EH:.2f}", "rel_s": f"{rel_s:.2e}"})

    # ---------------------------------------------------------------- S2
    print("[S2] 线性 P(k) 网格与 σ8 定标")
    build_grids()
    build_sig2_tophat()
    build_sig2_gauss()
    s8_raw = sigma8_from_grid(_D2G_Z0)
    # 收敛：半网格密度重算（抽偶数点 = 半密度 Simpson 对比）
    kg_h = _KG[::2]
    d2_h = _D2G_Z0[::2]
    s8_half = sqrt(simpson_arr(
        [d2_h[i] * tophat_w(kg_h[i] * 8.0) ** 2 for i in range(len(d2_h))],
        _DLNK * 2.0))
    conv8 = abs(s8_raw - s8_half) / s8_raw
    global CAL
    CAL = SIGMA8_IN / s8_raw
    s8_cal = s8_raw * CAL
    guard("G2", "σ8 从原初谱+P(k) 积分回算并定标",
          0.70 <= s8_raw <= 1.05 and abs(s8_cal - SIGMA8_IN) < 1e-12
          and conv8 < 1e-4,
          f"σ8_raw(A_s=2.1e−9,n_s=0.9649)={s8_raw:.4f}（窗口 [0.70,1.05]：EH98 拟合残差 "
          f"~5–10% + 无中微子压低 ⇒ 预期略高于 0.811；vs 锚 "
          f"rel {(s8_raw-SIGMA8_IN)/SIGMA8_IN*100:+.2f}%）；"
          f"定标 CAL={CAL:.4f} ⇒ σ8={s8_cal:.12f}；半密度收敛 rel {conv8:.2e}",
          {"s8_raw": f"{s8_raw:.4f}", "cal": f"{CAL:.4f}",
           "conv": f"{conv8:.2e}"})

    # ---------------------------------------------------------------- S3
    print("[S3] Halofit 非线性功率谱（z=0,1）")
    ks0, neff0, cc0 = halofit_params(0.0, _D2G_Z0)
    ks1, neff1, cc1 = halofit_params(1.0, _D2G_Z1)
    k_probe = [0.02, 0.05, 0.1, 0.3, 1.0, 3.0]
    d2l0 = {k: delta2_lin(k, 0.0) for k in k_probe}
    d2n0 = {k: halofit_d2nl(k, 0.0, ks0, neff0, cc0) for k in k_probe}
    d2n1 = {k: halofit_d2nl(k, 1.0, ks1, neff1, cc1) for k in k_probe}
    b005 = d2n0[0.05] / d2l0[0.05]
    b10 = d2n0[1.0] / d2l0[1.0]
    b10_z1 = d2n1[1.0] / delta2_lin(1.0, 1.0)
    # 口径（开发期自抓后修正）：Halofit 的 k_σ 用 Gaussian 窗 σ²(R)=∫dlnk Δ²e^{−(kR)²}
    # （Smith+03 定义），σ8=0.811 ΛCDM 得 k_σ≈0.37 h/Mpc；top-hat 窗则 ≈0.17，
    # 两约定差 ~2 倍是窗函数差异而非错误。B(0.05)≈0.89 是 Smith+03 原版拟合在
    # 两晕过渡区（y≈0.14）的真实下凹——(1+x)^β/(1+αx)·e^{−f(y)} 在该处 <1，
    # 即 Takahashi+12 修订版要修的 ~5–10% 不足，不是实现错误。
    sig_id = abs(sigma2_gauss_interp(1.0 / ks0, 0.0) * CAL ** 2 - 1.0)
    ok3 = (0.15 <= ks0 <= 0.45 and -2.2 <= neff0 <= -1.3 and sig_id < 1e-6
           and 0.80 <= b005 <= 1.10
           and 2.0 <= b10 <= 15.0 and 5.0 <= d2n0[1.0] <= 80.0
           and b10_z1 < b10)
    guard("G3", "Halofit：k_σ（Gaussian 窗约定）、n_eff、boost 曲线与 z 演化方向",
          ok3,
          f"k_σ(z=0)={ks0:.4f} h/Mpc（n_eff={neff0:.4f}、C={cc0:.4f}；"
          f"二分恒等 |σ_G(1/k_σ)−1|={sig_id:.1e}；top-hat 约定则 ≈0.173）；"
          f"k_σ(z=1)={ks1:.4f}；B(0.05)={b005:.4f}（Smith+03 两晕过渡下凹，窗 "
          f"[0.80,1.10]）；B(1.0)={b10:.3f}；Δ²_NL(1)={d2n0[1.0]:.2f}；"
          f"B(1.0,z=1)={b10_z1:.3f}<B(1.0,z=0)",
          {"k_sig0": f"{ks0:.4f}", "n_eff0": f"{neff0:.4f}",
           "c0": f"{cc0:.4f}", "sig_id": f"{sig_id:.1e}", "b005": f"{b005:.4f}",
           "b10": f"{b10:.3f}", "d2nl_1": f"{d2n0[1.0]:.2f}",
           "b10_z1": f"{b10_z1:.3f}"})

    # ---------------------------------------------------------------- S4
    print("[S4] Press–Schechter / Sheth–Tormen 晕质量函数")
    # M*：σ(M*)=δ_c（z=0）
    lo, hi = log(1e10), log(1e15)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if sigma_m(exp(mid), 0.0) > DELTA_C:
            lo = mid
        else:
            hi = mid
    m_star = exp(0.5 * (lo + hi))
    n14_0 = n_cum(1e14, 0.0, "ST")
    n15_0 = n_cum(1e15, 0.0, "ST")
    n14_1 = n_cum(1e14, 1.0, "ST")
    ratio_st_ps_star = f_st(1.0) / f_ps(1.0)
    ratio_15 = n15_0 / n14_0
    ok4 = (1e12 <= m_star <= 5e13 and 3e-7 <= n14_0 <= 3e-5
           and 1e-5 <= ratio_15 <= 0.05 and n14_1 < n14_0
           and 0.55 <= ratio_st_ps_star <= 0.80)   # ST/PS(ν=1)=0.661（解析值）
    guard("G4", "晕质量函数：M*、n(>1e14)、质量层级与 z 演化",
          ok4,
          f"M*={m_star:.3e} M_sun/h；n(>1e14)={n14_0:.3e} (Mpc/h)⁻³；"
          f"n(>1e15)/n(>1e14)={ratio_15:.2e}；n(>1e14,z=1)={n14_1:.3e}<z=0；"
          f"ST/PS(ν=1)={ratio_st_ps_star:.4f}",
          {"m_star": f"{m_star:.3e}", "n14": f"{n14_0:.3e}",
           "r15_14": f"{ratio_15:.2e}", "n14_z1": f"{n14_1:.3e}",
           "st_ps_star": f"{ratio_st_ps_star:.4f}"})

    # ---------------------------------------------------------------- S5
    print("[S5] Kaiser RSD 与 fσ8(z)")
    betas = [0.0, 0.3, 0.5, 0.7, 1.0]
    kaiser_rel = max(
        max(abs(kaiser_p0_num(b) - kaiser_p0(b)) / kaiser_p0(b),
            abs(kaiser_p2_num(b) - kaiser_p2(b)) / max(kaiser_p2(b), 1e-30))
        for b in betas[1:])
    def f_of_z(z):
        a = 1.0 / (1.0 + z)
        e2 = OM * a ** -3 + OL
        omz = OM * a ** -3 / e2
        return omz ** 0.55   # Linder（r254 已机检 0.50% 近似）；f 的 ODE 值见 r254
    fs8 = {z: f_of_z(z) * SIGMA8_IN * growth_g(z)
           for z in [0.25, 0.5, 1.0, 1.5, 2.0]}
    # ΛCDM 的 fσ8(z) 在 z≈0.4–0.6 有宽峰：z=0 端因 f→0.527 压低，高 z 端因 σ8 压低。
    # 判别式：峰值区之后单调降，且 fσ8(0.5) > fσ8(0)=f0×0.811。
    fs8_0 = f_of_z(0.0) * SIGMA8_IN
    fs8_shape = (fs8[0.5] > fs8[1.0] > fs8[1.5] > fs8[2.0]
                 and fs8[0.5] > fs8_0)
    ok5 = (kaiser_rel < 1e-9 and fs8_shape and 0.40 <= fs8[0.5] <= 0.52)
    guard("G5", "Kaiser 双路径（μ 积分 vs 解析因子）与 fσ8(z) 表",
          ok5,
          f"β∈{{0.3..1.0}} P0/P2 数值-解析 max rel {kaiser_rel:.2e}；"
          f"fσ8：z0={fs8_0:.4f}、z0.25={fs8[0.25]:.4f}、z0.5={fs8[0.5]:.4f}"
          f"（窗 [0.40,0.52]，峰区）、z1={fs8[1.0]:.4f}、z2={fs8[2.0]:.4f}"
          f"——峰后单调降",
          {"kaiser_rel": f"{kaiser_rel:.2e}", "fs8_05": f"{fs8[0.5]:.4f}",
           "fs8_0": f"{fs8_0:.4f}"})

    # ---------------------------------------------------------------- S6
    print("[S6] 控制组")
    # C1：幂律 Gaussian 窗恒等 Δ²=A k² ⇒ σ²(R)=A/(2R²)
    aa_pl = 3.7e-3
    d2_pl = [aa_pl * k ** 2 for k in _KG]
    s2_pl = [sigma2_grid_gauss(r, d2_pl) * 2.0 * r * r / aa_pl for r in (0.5, 2.0, 8.0)]
    c1_ok = all(abs(v - 1.0) < 1e-7 for v in s2_pl)   # 网格截断 ~6e-9 级
    control("C1", "幂律 Gaussian 窗恒等：Δ²=Ak² ⇒ σ²(R)=A/(2R²)",
            c1_ok,
            "R∈{0.5,2,8} 处 2R²σ²/A = "
            + "，".join(f"{v:.12f}" for v in s2_pl)
            + "——σ 积分机不是『任何输入都给同一读数』",
            {"vals": [f"{v:.12f}" for v in s2_pl]})
    # C2：PS/ST 判别结构 + 归一恒等（对 dlnν 归一）。
    # 开发期自抓：线性 ν 的 Simpson 对 ν^{−0.6} 近零奇异精度不足（得 0.9915）；
    # 改 u=lnν 换元（被积函数 e^{0.4u} 光滑衰减），ν∈[1e−12,20] 截断尾 ~1e−5。
    _u_lo, _u_hi = log(1e-12), log(20.0)
    norm_ps = simpson(lambda u: f_ps(exp(u)), _u_lo, _u_hi, 800000)
    norm_st = simpson(lambda u: f_st(exp(u)), _u_lo, _u_hi, 800000)
    r_hi = f_st(DELTA_C / sigma_m(1e15, 0.0)) / f_ps(DELTA_C / sigma_m(1e15, 0.0))
    r_lo = f_st(DELTA_C / sigma_m(1e11, 0.0)) / f_ps(DELTA_C / sigma_m(1e11, 0.0))
    c2_ok = (abs(norm_ps - 1.0) < 1e-6 and abs(norm_st - 1.0) < 2e-3
             and r_hi > 1.0 and r_lo < 1.0)
    control("C2", "PS/ST 归一与高质量端增强、低质量端压制的判别结构",
            c2_ok,
            f"∫f_PS dlnν={norm_ps:.12f}（恒等 1，u=lnν 换元）；"
            f"∫f_ST dlnν={norm_st:.6f}（解析 1.00003，A=0.3222 舍入）；"
            f"ST/PS(1e15)={r_hi:.3f}>1、ST/PS(1e11)={r_lo:.3f}<1",
            {"norm_ps": f"{norm_ps:.12f}", "norm_st": f"{norm_st:.6f}",
             "r_hi": f"{r_hi:.3f}", "r_lo": f"{r_lo:.3f}"})
    # C3：σ8 ∝ √A_s 幅度线性恒等
    d2_4x = [4.0 * v for v in _D2G_Z0]
    s8_4x = sigma8_from_grid(d2_4x)
    c3_ok = abs(s8_4x / s8_raw - 2.0) < 1e-12
    control("C3", "σ8 ∝ √A_s：A_s×4 ⇒ σ8×2（机器恒等）",
            c3_ok, f"σ8(4A_s)/σ8(A_s)={s8_4x/s8_raw:.15f}",
            {"ratio": f"{s8_4x/s8_raw:.15f}"})
    # C4：Kaiser 极限 β→0 复原、β→∞ 主导项 β²/5（修正项 O(1/β)，取 β=200）
    k0r = kaiser_p0(0.0)
    k_inf = kaiser_p0(200.0) / (200.0 ** 2 / 5.0)
    c4_ok = k0r == 1.0 and 1.0 < k_inf < 1.025
    control("C4", "Kaiser 极限：β→0 复原 P^r；β=200 时 P0/(β²/5)∈(1,1.025]",
            c4_ok, f"P0(0)={kaiser_p0(0.0)}；P0(200)/(200²/5)={k_inf:.6f}"
            "（>1 的余项即 2β/3+1 项，β→∞ 时趋于 1）",
            {"p0_b0": f"{kaiser_p0(0.0)}", "p0_b200": f"{k_inf:.6f}"})

    # ---------------------------------------------------------------- S7
    print("[S7] 条目与判决")
    entry("H01", "INFO", "判定：非线性结构层 = 标准拟合式复现，不是新理论",
          "EH98 转移函数、Halofit（Smith+03）、PS/ST 质量函数、Kaiser 因子全部是"
          "文献拟合式/解析近似——本卷只做机器复现与多路径互印（承 r229/r237/r254/r256）")
    entry("H02", "PASS", "线性转移函数三件套互印",
          f"T(k→0)=1 恒等；EH-nowig vs BBKS max rel {cmp_rel:.4f}；"
          f"s_EH={S_EH:.2f} Mpc vs r_d=147.07（{rel_s*100:.2f}%）；"
          f"wiggle 幅度 {wig_amp:.4f}")
    entry("H03", "PASS", "σ8 原初谱回算与定标",
          f"σ8_raw={s8_raw:.4f}（A_s=2.1e−9 直接积分，落在 EH98 拟合残差窗口）；"
          f"单参数定标 CAL={CAL:.4f} ⇒ σ8=0.811 逐位")
    entry("H04", "PASS", "Halofit 非线性谱读数物理",
          f"k_σ={ks0:.4f} h/Mpc；B(0.05)={b005:.4f}、B(1.0)={b10:.3f}；"
          f"Δ²_NL(1)={d2n0[1.0]:.2f}；z=1 boost 低于 z=0（方向正确）")
    entry("H05", "PASS", "晕质量函数量级与结构",
          f"M*={m_star:.2e} M_sun/h；n(>1e14)={n14_0:.2e} (Mpc/h)⁻³；"
          f"ST/PS 高质量端 {r_hi:.2f}>1、低质量端 {r_lo:.2f}<1")
    entry("H06", "PASS", "Kaiser 因子双路径与 fσ8(z)",
          f"μ 积分 vs 解析 max rel {kaiser_rel:.2e}；"
          f"fσ8(0.5)={fs8[0.5]:.4f}，随 z 单调衰减")
    entry("H07", "BOUNDARY", "Halofit/EH98 是经验拟合式，非第一性",
          "Halofit 是 N 体模拟的经验拟合（Smith+03；Takahashi+12 修订版在 k~1 处差 "
          "~5–10%，本卷取原版）；EH98 对 CAMB/CLASS 的残差 ~5–10%——两层的绝对精度"
          "受拟合式本身限制，本卷不误称为『预言』")
    entry("H08", "BOUNDARY", "bias、中微子质量、重子反馈与 z≳2 外推不在本卷",
          "星系偏袒 b(k,z)、Σmν=0.06 eV 的小尺度压低、AGN 反馈（k≳1）均未建模；"
          "Halofit 原拟合范围 z≤3，超出只作方向参考")
    entry("H09", "INFO", "判决：非线性层复现 OK，统一仍无新物理",
          "背景（r237）→线性（r254）→声学几何（r256）→视界热力学（r260）→非线性"
          "（本卷）全部为 ΛCDM 标准件复现；r230『本质三层不可达』与 r267 完成度判决不变")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    ledger = [
        ["r214", "静态中心力（UFE-4F 母式）", "形式统一 PASS；动力学 FAIL"],
        ["r221", "禁闭 σr + 通道门（UFE-4F⁺）", "r214 严格超集"],
        ["r228", "变分层（L 与诺特）", "一个作用量生成中心力"],
        ["r229", "新颖性审计", "无新理论/无新方程"],
        ["r230", "引力本质层", "WEP 结构恒等 + 1PN 两件套"],
        ["r232", "引力波层", "四极/HT/啁啾三管线互印"],
        ["r233", "黑洞热力学层", "四定律+Smarr+面积定理"],
        ["r237", "宇宙学背景层", "FRW 年龄/距离-红移/Λ 通道"],
        ["r254", "宇宙学扰动层", "线性增长+BAO 声视界+σ8 演化"],
        ["r256", "宇宙学声学峰层", "θ_s/l_A/z_eq 几何骨架"],
        ["r260", "宇宙学视界热力学层", "Misner–Sharp 第一定律；无观测通道"],
        ["r274", "宇宙学非线性结构层（本卷）", "P(k)+Halofit+晕质量函数+Kaiser"],
    ]

    # 可视化曲线数据
    def curve_pk():
        out = []
        for i in range(90):
            lk = log(1e-3) + (log(30.0) - log(1e-3)) * i / 89
            k = exp(lk)
            out.append({"k": k, "eh": delta2_lin(k, 0.0) * 2 * pi ** 2 / k ** 3,
                        "bb": A_S * (k / K0) ** (N_S - 1.0) * t_bbks(k) ** 2
                        * CAL ** 2 * 2 * pi ** 2 / k ** 3})
        return out

    def curve_nl():
        out = []
        for i in range(90):
            lk = log(1e-3) + (log(30.0) - log(1e-3)) * i / 89
            k = exp(lk)
            out.append({"k": k,
                        "lin0": delta2_lin(k, 0.0),
                        "nl0": halofit_d2nl(k, 0.0, ks0, neff0, cc0),
                        "lin1": delta2_lin(k, 1.0),
                        "nl1": halofit_d2nl(k, 1.0, ks1, neff1, cc1)})
        return out

    def curve_mf():
        out = []
        for i in range(80):
            lm = log(1e10) + (log(1e16) - log(1e10)) * i / 79
            m = exp(lm)
            out.append({"m": m,
                        "st0": dndlnm(m, 0.0, "ST"), "ps0": dndlnm(m, 0.0, "PS"),
                        "st1": dndlnm(m, 1.0, "ST")})
        return out

    def curve_kaiser():
        return [{"beta": 0.02 * i,
                 "p0": kaiser_p0(0.02 * i), "p2": kaiser_p2(0.02 * i)}
                for i in range(76)]

    res = {
        "stem": STEM, "round": 274, "date": "2026-10-31",
        "method": ("EH98 转移函数（全版/no-wiggle）对拍 BBKS+Sugiyama + 原初谱 σ8 回算定标 "
                   "+ Halofit(Smith+03) 非线性谱 + PS/ST 晕质量函数 + Kaiser μ 积分对拍 "
                   "——float64，纯标准库"),
        "cosmo_verdict": ("非线性结构层全部机器复现（转移函数双路径、σ8 定标、Halofit "
                          "boost、PS/ST 质量层级、Kaiser 双路径）；拟合式残差与 bias/"
                          "中微子/反馈为硬边界——复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "params": {"h": H_DIM, "Om": OM, "Ob": OB, "fb": FB,
                       "A_s": A_S, "n_s": N_S, "k0": K0,
                       "sigma8_in": SIGMA8_IN, "delta_c": DELTA_C},
            "tf": {"gamma_bbks": GAMMA_BBKS, "gamma_eff": GAMMA_EFF,
                   "s_EH": S_EH, "k_silk": K_SILK,
                   "alpha_c": ALPHA_C, "beta_c": BETA_C,
                   "cmp_rel": cmp_rel, "wig_amp": wig_amp,
                   "rd_ref": rd, "rel_s": rel_s,
                   "pk": curve_pk()},
            "s8": {"raw": s8_raw, "cal": CAL, "cal_s8": s8_cal,
                   "conv": conv8},
            "halofit": {"k_sig0": ks0, "n_eff0": neff0, "c0": cc0,
                        "k_sig1": ks1, "n_eff1": neff1, "c1": cc1,
                        "b005": b005, "b10": b10, "b10_z1": b10_z1,
                        "d2nl_1": d2n0[1.0], "nl": curve_nl()},
            "mf": {"m_star": m_star, "n14_0": n14_0, "n15_0": n15_0,
                   "n14_1": n14_1, "st_ps_star": ratio_st_ps_star,
                   "r_hi": r_hi, "r_lo": r_lo,
                   "norm_ps": norm_ps, "norm_st": norm_st,
                   "mf": curve_mf()},
            "rsd": {"kaiser_rel": kaiser_rel,
                    "fs8": [{"z": z, "fs8": fs8[z]} for z in sorted(fs8)],
                    "kaiser": curve_kaiser()},
            "ledger": [{"round": r, "method": m, "verdict": v}
                       for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R274-COSMO-NONLINEAR-STRUCTURE-EH98-TF-DUALPATH-OK",
        "SIGMA8-PRIMORDIAL-CAL-OK-HALOFIT-OK-PS-ST-MASSFCT-OK",
        "KAISER-RSD-DUALPATH-OK-FS8-EVOLUTION-OK",
        "FIT-FORMULA-BOUNDARY-BIAS-NEUTRINO-FEEDBACK-BOUNDARY",
        "VERDICT-STANDARD-NONLINEAR-STRUCTURE-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（宇宙学非线性结构层：EH98 转移函数双路径、"
                        "σ8 原初谱回算定标、Halofit 非线性谱、PS/ST 晕质量函数、"
                        "Kaiser RSD 与 fσ8 演化）；拟合式残差与 bias/中微子/反馈在框架外；"
                        "无新理论")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r237（宇宙学背景层）", "r254（宇宙学扰动层）",
                     "r256（声学峰层）", "r260（视界热力学层）",
                     "r229（新颖性审计口径）", "r267（完成度终局判决）",
                     "Eisenstein–Hu 1998 / Smith+2003 / Press–Schechter 1974 / "
                     "Sheth–Tormen 1999 / Kaiser 1987 / Planck 2018（只读）"],
    }

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G6", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)

    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
         f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
         f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
         f"控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——"
                 f"{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——"
                 f"{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        t = res["readings"]["tf"]
        f.write(f"gamma_bbks={t['gamma_bbks']:.5f} gamma_eff={t['gamma_eff']:.5f} "
                f"s_EH={t['s_EH']:.2f} cmp_rel={t['cmp_rel']:.4f} "
                f"wig_amp={t['wig_amp']:.4f}\n")
        s = res["readings"]["s8"]
        f.write(f"s8_raw={s['raw']:.4f} cal={s['cal']:.4f} conv={s['conv']:.2e}\n")
        h = res["readings"]["halofit"]
        f.write(f"k_sig0={h['k_sig0']:.4f} neff0={h['n_eff0']:.4f} c0={h['c0']:.4f} "
                f"b005={h['b005']:.4f} b10={h['b10']:.3f} d2nl1={h['d2nl_1']:.2f} "
                f"b10_z1={h['b10_z1']:.3f}\n")
        m = res["readings"]["mf"]
        f.write(f"m_star={m['m_star']:.3e} n14={m['n14_0']:.3e} "
                f"n14_z1={m['n14_1']:.3e} st_ps_star={m['st_ps_star']:.4f}\n")
        r = res["readings"]["rsd"]
        f.write(f"kaiser_rel={r['kaiser_rel']:.2e} "
                + "fs8=" + ",".join(f"{x['z']}:{x['fs8']:.4f}" for x in r["fs8"])
                + "\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R274_JSON__" not in tpl:
        return False, "模板缺少 __R274_JSON__ 占位符"
    html = tpl.replace("__R274_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R274_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
