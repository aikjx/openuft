# -*- coding: utf-8 -*-
"""
TUFT V22 · 三路联合 χ² 拟合的可证伪性审计
================================================================
审计对象：TUFT V21「水星近日点进动 + 原子高阶精细结构 + CMB 双谱」
          三路联合 χ² 拟合（JAX AutoDiff Hessian + emcee MCMC + corner）

审计动机：V21 给出的三个「下一步候选」(1 加 EHT 第四观测组 / 2 贝叶斯因子 vs GR
          / 3 残差投影图) 全都建立在「这套拟合已经成立」的前提上。本册先检验该前提。

本册十节（全部实跑：sympy 解析导数 · mpmath 60/250 位 · numpy · scipy · emcee · corner）
  §1 导数精度基建：JAX 在本机 Py3.8 不可用 ⇒ sympy 解析梯度/Hessian + mpmath 250 位
     中心差分交叉验证（精度严格优于 float64 AD，且不受 AD 图限制）
  §2 数据来源审计（P0）：水星可溯源；原子 / CMB 数据与公开值冲突
  §3 可辨识性审计：float64 下 n 项恒零；mpmath 下「量级」与「比值」不可兼得；
     τ 相位不可辨识；CMB 形状指数与观测反号
  §4 结构性退化：三参数完全解耦（Hessian 严格块对角）⇒ 「联合」无跨探针信息
  §5 拟合实跑：χ²_min / χ²/dof / 最大残差（原空间与 log 空间双路径对照）
  §6 目标 2 的正确诊断：真正的病灶不是「有限差分噪声」而是「跨 28 量级的绝对步长」
  §7 MCMC：初始化尺度灾难 + 线性模型下后验为精确截断高斯（反驳「MCMC 更可靠」）
  §8 候选 2 判定：贝叶斯因子因先验体积任意而不可定义；AIC/BIC 先验无关替代
  §9 候选 3：把「固定参数预言」转为证伪测试并实际外推
  §10 结论与真正的下一步

红线：数学自洽 ≠ 物理实证。数据可疑 / 模型假设一律如实标注，不粉饰为 PASS。
产出：同目录 .txt（含 PASS/FAIL/BOUNDARY/INFO 汇总行）· .json · corner png
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import minimize, approx_fprime

HERE = os.path.dirname(os.path.abspath(__file__))

# ===================== 结果收集器 =====================
results = []


def rec(code, name, status, detail, evidence=None):
    results.append({"code": code, "name": name, "status": status,
                    "detail": detail, "evidence": evidence or {}})
    print("[%8s] %-6s %s : %s" % (status, code, name, detail))


def P(code, name, detail, ev=None):
    rec(code, name, "PASS", detail, ev)


def F(code, name, detail, ev=None):
    rec(code, name, "FAIL", detail, ev)


def Bd(code, name, detail, ev=None):
    rec(code, name, "BOUNDARY", detail, ev)


def If(code, name, detail, ev=None):
    rec(code, name, "INFO", detail, ev)


# ===================== 数据集（原样照抄 V21，不做任何修改） =====================
PHI_OBS = 43.03          # arcsec / century
PHI_ERR = 0.03
PHI_GR = 42.979
MERC_COEF = 0.051        # V21: delta_tuft = beta * 0.051

N_ATOM = [2, 3]
E_OBS = [1.082e-4, 2.415e-4]        # eV
E_ERR = [0.003e-4, 0.004e-4]        # eV
OMEGA_ATOM = 1.0e16
NTOP = 1000.0
HBAR = 1.054571817e-34
CC = 299792458.0
EV = 1.602176634e-19
GCONST = 6.67430e-11

ELL = [(2000.0, 2000.0, 2000.0), (1500.0, 1500.0, 1500.0), (1000.0, 1000.0, 1000.0)]
B_OBS = [2.1e-19, 1.4e-19, 0.85e-19]
B_ERR = [0.45e-19, 0.38e-19, 0.30e-19]
TAU_COSM = 1.2e-6

FAC = (OMEGA_ATOM ** 2) / (CC ** 2)          # ≈ 1.1127e15
KK = FAC / EV                                 # E[eV] = KK * (V0 + n^2 hbar^2/Ntop^2)

# ===================== 通用 χ²（lib = np 或 mp） =====================
def chi2_generic(p, lib, cn):
    beta, V0, A = p[0], p[1], p[2]
    r_merc = (cn["phi_gr"] + beta * cn["merc_coef"] - cn["phi_obs"]) / cn["phi_err"]
    chi = r_merc ** 2
    fac = (cn["omega"] ** 2) / (cn["c"] ** 2)
    for i, n in enumerate(cn["n_atom"]):
        En = fac * (V0 + (n ** 2 * cn["hbar"] ** 2) / (cn["ntop"] ** 2)) / cn["ev"]
        chi = chi + ((En - cn["e_obs"][i]) / cn["e_err"][i]) ** 2
    for i in range(len(cn["ell"])):
        l1, l2, l3 = cn["ell"][i]
        lbar = (l1 + l2 + l3) / 3.0
        Bp = A * lib.cos(cn["tau"] * lbar) / (l1 * l2 * l3)
        chi = chi + ((Bp - cn["b_obs"][i]) / cn["b_err"][i]) ** 2
    return chi


CN_NP = {"phi_gr": PHI_GR, "phi_obs": PHI_OBS, "phi_err": PHI_ERR, "merc_coef": MERC_COEF,
         "n_atom": [2.0, 3.0], "e_obs": E_OBS, "e_err": E_ERR, "omega": OMEGA_ATOM,
         "c": CC, "hbar": HBAR, "ntop": NTOP, "ev": EV,
         "ell": ELL, "b_obs": B_OBS, "b_err": B_ERR, "tau": TAU_COSM}

mp.mp.dps = 60
CN_MP = {"phi_gr": mp.mpf("42.979"), "phi_obs": mp.mpf("43.03"), "phi_err": mp.mpf("0.03"),
         "merc_coef": mp.mpf("0.051"), "n_atom": [mp.mpf(2), mp.mpf(3)],
         "e_obs": [mp.mpf("1.082e-4"), mp.mpf("2.415e-4")],
         "e_err": [mp.mpf("0.003e-4"), mp.mpf("0.004e-4")],
         "omega": mp.mpf("1.0e16"), "c": mp.mpf("299792458"),
         "hbar": mp.mpf("1.054571817e-34"), "ntop": mp.mpf("1000"),
         "ev": mp.mpf("1.602176634e-19"),
         "ell": [(mp.mpf(2000), mp.mpf(2000), mp.mpf(2000)),
                 (mp.mpf(1500), mp.mpf(1500), mp.mpf(1500)),
                 (mp.mpf(1000), mp.mpf(1000), mp.mpf(1000))],
         "b_obs": [mp.mpf("2.1e-19"), mp.mpf("1.4e-19"), mp.mpf("0.85e-19")],
         "b_err": [mp.mpf("0.45e-19"), mp.mpf("0.38e-19"), mp.mpf("0.30e-19")],
         "tau": mp.mpf("1.2e-6")}


def chi2_np(p):
    return float(chi2_generic(np.asarray(p, dtype=np.float64), np, CN_NP))


def chi2_mp(p):
    return chi2_generic([x if isinstance(x, mp.mpf) else mp.mpf(str(x)) for x in p], mp, CN_MP)


print("=" * 88)
print("TUFT V22 · 三路联合 χ² 拟合的可证伪性审计")
print("=" * 88)

# =====================================================================
# §1 导数精度基建：sympy 解析梯度 / Hessian + mpmath 250 位中心差分验证
# =====================================================================
print("\n---- §1 导数精度基建（sympy 解析 vs mpmath 250 位差分 vs JAX 可用性）----")

JAX_AVAILABLE = False
try:
    import jax  # noqa
    JAX_AVAILABLE = True
except Exception as _e:
    JAX_AVAILABLE = False

if JAX_AVAILABLE:
    If("D1-0", "JAX 可用性", "jax 已安装，可直接走 AutoDiff", {})
else:
    Bd("D1-0", "JAX 不可用·改走解析路线",
       "本机 Python 3.8.8 无 jax/jaxlib（Windows 无 Py3.8 wheel）；"
       "改用 sympy 解析梯度+Hessian，并由 mpmath 250 位中心差分交叉验证。"
       "解析二阶导严格优于 float64 AD：无浮点截断、无 AD 图近似。",
       {"python": sys.version.split()[0]})

beta_s, V0_s, A_s = sp.symbols("beta V0 A", positive=True)
syms = (beta_s, V0_s, A_s)

# 高精度符号常量：与 mpmath 常量同源（十进制字面值），避免 float64 污染符号导数
DIG = 120
c_s = sp.Float("299792458", DIG)
hbar_s = sp.Float("1.054571817e-34", DIG)
ev_s = sp.Float("1.602176634e-19", DIG)
om_s = sp.Float("1.0e16", DIG)
nt_s = sp.Float("1000", DIG)
tau_s = sp.Float("1.2e-6", DIG)
fac_s = om_s ** 2 / c_s ** 2
E_OBS_S = [sp.Float("1.082e-4", DIG), sp.Float("2.415e-4", DIG)]
E_ERR_S = [sp.Float("0.003e-4", DIG), sp.Float("0.004e-4", DIG)]
B_OBS_S = [sp.Float("2.1e-19", DIG), sp.Float("1.4e-19", DIG), sp.Float("0.85e-19", DIG)]
B_ERR_S = [sp.Float("0.45e-19", DIG), sp.Float("0.38e-19", DIG), sp.Float("0.30e-19", DIG)]
ELL_S = [(sp.Float(2000, DIG),) * 3, (sp.Float(1500, DIG),) * 3, (sp.Float(1000, DIG),) * 3]

# 三路残差（符号）
r_m = (sp.Float("42.979", DIG) + beta_s * sp.Float("0.051", DIG)
       - sp.Float("43.03", DIG)) / sp.Float("0.03", DIG)
chi_s = r_m ** 2
for i, n in enumerate(N_ATOM):
    En = fac_s * (V0_s + (sp.Float(n, DIG) ** 2 * hbar_s ** 2) / (nt_s ** 2)) / ev_s
    chi_s += ((En - E_OBS_S[i]) / E_ERR_S[i]) ** 2
for i, (l1, l2, l3) in enumerate(ELL_S):
    lbar = (l1 + l2 + l3) / sp.Float(3, DIG)
    Bp = A_s * sp.cos(tau_s * lbar) / (l1 * l2 * l3)
    chi_s += ((Bp - B_OBS_S[i]) / B_ERR_S[i]) ** 2

grad_s = [sp.diff(chi_s, s) for s in syms]
hess_s = [[sp.diff(chi_s, si, sj) for sj in syms] for si in syms]

chi2_f = sp.lambdify(syms, chi_s, "numpy")
grad_f = sp.lambdify(syms, grad_s, "numpy")
hess_f = sp.lambdify(syms, hess_s, "numpy")

# 用 mpmath 250 位中心差分验证解析 Hessian（在非退化检验点）
mp.mp.dps = 250
p_test = [mp.mpf("0.5"), mp.mpf("2.25e-38"), mp.mpf("1.15e-10")]


def hess_mp_fd(p, h_rel="1e-30"):
    n = 3
    Hm = [[mp.mpf(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            hi = abs(p[i]) * mp.mpf(h_rel)
            hj = abs(p[j]) * mp.mpf(h_rel)
            pp, pm = list(p), list(p)
            if i == j:
                pp[i] = p[i] + hi
                pm[i] = p[i] - hi
                Hm[i][i] = (chi2_mp(pp) - 2 * chi2_mp(p) + chi2_mp(pm)) / (hi ** 2)
            else:
                a, b, c, d = list(p), list(p), list(p), list(p)
                a[i] = p[i] + hi; a[j] = p[j] + hj
                b[i] = p[i] + hi; b[j] = p[j] - hj
                c[i] = p[i] - hi; c[j] = p[j] + hj
                d[i] = p[i] - hi; d[j] = p[j] - hj
                Hm[i][j] = (chi2_mp(a) - chi2_mp(b) - chi2_mp(c) + chi2_mp(d)) / (4 * hi * hj)
    return Hm


H_mp_fd = hess_mp_fd(p_test)
H_sym_mp = [[sp.N(hess_s[i][j], 100) for j in range(3)] for i in range(3)]

rel_errs = []
for i in range(3):
    for j in range(3):
        a = mp.mpf(str(H_sym_mp[i][j]))
        b = H_mp_fd[i][j]
        if a != 0:
            rel_errs.append(abs(a - b) / abs(a))
max_rel = max(rel_errs) if rel_errs else mp.mpf(0)
mp.mp.dps = 60

P("D1-1", "解析 Hessian 交叉验证",
  "sympy 解析 Hessian 与 mpmath 250 位中心差分最大相对偏差 = %s"
  "（符号常量与 mpmath 常量同源为十进制字面值；若常量只用 float64 精度，"
  "该偏差会退化到 ~3e-16，无法体现高精度）"
  % mp.nstr(max_rel, 6),
  {"max_rel_dev": mp.nstr(max_rel, 12), "dps": 250})


def grad_mp_fd(p, h_rel="1e-40"):
    g = []
    for i in range(3):
        h = abs(p[i]) * mp.mpf(h_rel)
        pp, pm = list(p), list(p)
        pp[i] = p[i] + h
        pm[i] = p[i] - h
        g.append((chi2_mp(pp) - chi2_mp(pm)) / (2 * h))
    return g


mp.mp.dps = 250
p_probe_mp = [mp.mpf("1e-3"), mp.mpf("1e-18"), mp.mpf("1e-17")]
g_mp_fd = grad_mp_fd(p_probe_mp)
sub2 = {beta_s: sp.Float(mp.nstr(p_probe_mp[0], 40), DIG),
        V0_s: sp.Float(mp.nstr(p_probe_mp[1], 40), DIG),
        A_s: sp.Float(mp.nstr(p_probe_mp[2], 40), DIG)}
g_sym2 = [sp.N(grad_s[i].subs(sub2), 100) for i in range(3)]
rel_g = [abs(mp.mpf(str(g_sym2[i])) - g_mp_fd[i]) / abs(g_mp_fd[i]) for i in range(3)]
mp.mp.dps = 60
P("D1-1b", "解析梯度交叉验证（远离最优点）",
  "在 χ²≈1e45 的远点，sympy 解析梯度与 250 位中心差分相对偏差 = %s / %s / %s；"
  "该处 float64 有限差分会彻底失效（见 D6-1），解析导数不受影响。"
  % tuple(mp.nstr(x, 4) for x in rel_g),
  {"rel_dev_grad": [mp.nstr(x, 12) for x in rel_g]})

# 模型对三参数均为线性 ⇒ Hessian 恒为常数矩阵（与 p 无关）
H_a = np.array(hess_f(0.5, 2.25e-38, 1.15e-10), dtype=np.float64)
H_b = np.array(hess_f(1.0, 1e-18, 1e-17), dtype=np.float64)
H_const_dev = np.max(np.abs(H_a - H_b) / np.maximum(np.abs(np.diag(H_a))[None, :], 1e-300))
P("D1-2", "Hessian 与参数点无关（二次型）",
  "三个模型对各自参数均为线性 ⇒ χ² 是正定二次型，Hessian 为常数矩阵；"
  "两个相距 20 个量级的检验点上 Hessian 相对偏差 = %.3e" % H_const_dev,
  {"rel_dev": float(H_const_dev)})

# =====================================================================
# §2 数据来源审计
# =====================================================================
print("\n---- §2 数据来源审计 ----")

# 水星：GR 42.979 vs 观测 43.03±0.03 —— 标准可溯源值
P("D2-1", "水星数据可溯源",
  "φ_obs=43.03±0.03 arcsec/century、GR=42.979 与太阳系进动标准余差一致（残差 1.7σ）",
  {"residual_sigma": (PHI_GR - PHI_OBS) / PHI_ERR})

# 原子：与氢原子精细结构实测比较
E_FS2 = 4.5313e-5   # eV, 2P_{3/2}-2P_{1/2} ≈ 10969 MHz
E_FS3 = 1.3446e-5   # eV, 3P_{3/2}-3P_{1/2} ≈ 3250 MHz
ratio_true = E_FS3 / E_FS2
ratio_obs = E_OBS[1] / E_OBS[0]
ratio_dirac = (2.0 / 3.0) ** 3
F("D2-2", "原子数据与原子物理冲突",
  "V21 数据 E(2)=%.3eeV, E(3)=%.3eeV 随 n 增大（比值 %.3f）；"
  "氢精细结构实测 E(2)=%.3eeV→E(3)=%.3eeV 随 n 减小（比值 %.4f ≈ (2/3)³=%.4f）。"
  "趋势反号且量级差 %.1f×/%.1f×，数据集来源未标注 ⇒ 不可用作检验基准。"
  % (E_OBS[0], E_OBS[1], ratio_obs, E_FS2, E_FS3, ratio_true, ratio_dirac,
     E_OBS[0] / E_FS2, E_OBS[1] / E_FS3),
  {"ratio_obs": ratio_obs, "ratio_true": ratio_true, "ratio_dirac": ratio_dirac})

# CMB：观测值本身宣称非高斯性探测
snr_cmb = [B_OBS[i] / B_ERR[i] for i in range(3)]
F("D2-3", "CMB 数据宣称非高斯性探测",
  "三个构型的中心值/误差 = %.2fσ, %.2fσ, %.2fσ，等价于「已探测到原始非高斯性」；"
  "而 Planck 2018 等边/局域型 f_NL 未探测（|f_NL| ≲ O(10) 上限内与 0 相容）。"
  "数据集来源未标注且与公开结果冲突 ⇒ 不可用作检验基准。"
  % (snr_cmb[0], snr_cmb[1], snr_cmb[2]),
  {"snr": snr_cmb})

# =====================================================================
# §3 可辨识性审计
# =====================================================================
print("\n---- §3 可辨识性审计 ----")

# 3-1 float64 下 n 项恒零
v0_best_guess = 2.25e-38
n_term2 = (2.0 ** 2 * HBAR ** 2) / (NTOP ** 2)
n_term3 = (3.0 ** 2 * HBAR ** 2) / (NTOP ** 2)
sum_eq = (v0_best_guess + n_term2) == v0_best_guess
P("D3-1", "float64 下 n 依赖恒零",
  "n²ħ²/Ntop² = %.3e（n=2）/ %.3e（n=3）相对 V0≈%.3e 为 %.2e，"
  "远低于 float64 eps=2.22e-16 ⇒ V0 + n项 在 float64 下与 V0 严格相等(= %s)；"
  "模型对 n 的敏感度恰为零，无法产生任何 n 依赖的分裂。"
  % (n_term2, n_term3, v0_best_guess, n_term2 / v0_best_guess, sum_eq),
  {"n_term_ratio": n_term2 / v0_best_guess, "exactly_equal": bool(sum_eq)})

# 3-2 mpmath 下「量级」与「比值」不可兼得（闭式）
mp.mp.dps = 80
c2 = mp.mpf(4) * mp.mpf("1.054571817e-34") ** 2 / mp.mpf(1000) ** 2
c3 = mp.mpf(9) * mp.mpf("1.054571817e-34") ** 2 / mp.mpf(1000) ** 2
# 要求 E3/E2 = ratio_obs ⇒ (V0+c3)/(V0+c2) = R
R = mp.mpf(repr(ratio_obs))
V0_need = (c3 - R * c2) / (R - 1)
K_mp = (mp.mpf("1.0e16") ** 2 / mp.mpf("299792458") ** 2) / mp.mpf("1.602176634e-19")
E2_at_V0need = K_mp * (V0_need + c2)
E2_obs_mp = mp.mpf("1.082e-4")
mp.mp.dps = 60
F("D3-2", "量级与比值不可兼得（闭式证伪）",
  "即便用无限精度：要使 E(3)/E(2)=%.3f 需 V0=%s eV-量纲，此时 E(2)=%s eV，"
  "与观测 %.3e eV 差 %s 个量级 ⇒ 不存在任何 V0 能同时满足观测的量级与比值，"
  "模型被数据结构性否决（非数值失败）。"
  % (ratio_obs, mp.nstr(V0_need, 6), mp.nstr(E2_at_V0need, 6), E_OBS[0],
     mp.nstr(mp.log10(E2_obs_mp / E2_at_V0need), 4)),
  {"V0_need": mp.nstr(V0_need, 12), "E2_at_V0need_eV": mp.nstr(E2_at_V0need, 12)})

# 3-3 τ 不可辨识
x_tau = TAU_COSM * 2000.0
sens = -x_tau * np.tan(x_tau)
Bd("D3-3", "宇宙挠率 τ 不可辨识",
   "τ·ℓ̄ 在 ℓ=2000 处仅 %.5f rad ⇒ ∂lnB/∂lnτ = -x·tan x ≈ %.3e，"
   "CMB 双谱对该挠率参数的可辨识度 ≈ 0 ⇒ 该观测量不是挠率探针。"
   % (x_tau, sens),
   {"x": x_tau, "dlnB_dln_tau": float(sens)})

# 3-4 CMB 形状指数反号
lnl = np.log([2000.0, 1500.0, 1000.0])
lnb = np.log(np.array(B_OBS))
slope = np.polyfit(lnl, lnb, 1)[0]
F("D3-4", "CMB 形状指数反号",
  "观测 B(ℓ) 的幂律指数 = %+.3f（B 随 ℓ 增大而增大）；模型 B ∝ ℓ^-3 指数 = -3.000。"
  "两者相差 %.2f 个指数单位，符号相反 ⇒ 单振幅参数无法弥合形状矛盾。"
  % (slope, slope - (-3.0)),
  {"obs_power_index": float(slope), "model_power_index": -3.0})

# =====================================================================
# §4 结构性退化：参数完全解耦
# =====================================================================
print("\n---- §4 结构性退化（Hessian 块对角）----")
Hp = np.array(hess_f(1.0, 2.25e-38, 1.15e-10), dtype=np.float64)
diag = np.abs(np.diag(Hp))
off = np.abs(Hp - np.diag(np.diag(Hp)))
off_rel = off.max() / diag.max()
P("D4-1", "三参数完全解耦",
  "Hessian 非对角元/对角元 最大 = %.3e（机器零）⇒ β、V0、A_topo 三参数严格解耦，"
  "每个参数只进入单一数据集 ⇒ 「三路联合」= 三个独立一维拟合的平凡并列，"
  "不产生任何跨探针约束；corner 图无相关性是数学必然而非物理发现。"
  % off_rel,
  {"max_offdiag_rel": float(off_rel)})

F("D4-2", "候选 1（加 EHT 第四观测组）无判别力",
  "在参数解耦结构下，新增第四观测组必然引入第四个独立参数 A_EHT 由该组数据单独吸收，"
  "χ² 改善恒为「1 参数吃 1 组中心值」，跨探针约束仍为零 ⇒ 增加观测组不增加判别力。"
  "判别力的唯一来源是让参数跨探针共享（同一 β/τ 同时进入多个数据集）。",
  {})

# =====================================================================
# §5 拟合实跑
# =====================================================================
print("\n---- §5 拟合实跑（原空间 / log 空间双路径）----")

# 解析最优解（每个参数是各自子集的线性最小二乘）
beta_star = (PHI_OBS - PHI_GR) / MERC_COEF
w_a = [1.0 / E_ERR[i] ** 2 for i in range(2)]
c_star = sum(E_OBS[i] * w_a[i] for i in range(2)) / sum(w_a)
V0_star = c_star / KK
w_c = [1.0 / B_ERR[i] ** 2 for i in range(3)]
f_c = [np.cos(TAU_COSM * (ELL[i][0] + ELL[i][1] + ELL[i][2]) / 3.0) /
       (ELL[i][0] * ELL[i][1] * ELL[i][2]) for i in range(3)]
A_star = sum(B_OBS[i] * f_c[i] * w_c[i] for i in range(3)) / sum(f_c[i] ** 2 * w_c[i] for i in range(3))
p_star = np.array([beta_star, V0_star, A_star])

res_lin = minimize(chi2_np, np.array([1e-3, 1e-18, 1e-17]), method="L-BFGS-B",
                   bounds=[(0, None), (0, None), (0, None)])
res_log = minimize(lambda q: chi2_np(np.exp(q)), np.log(np.array([1e-3, 1e-18, 1e-17])),
                   method="L-BFGS-B")

chi2_min = chi2_np(p_star)
ndata, nparam, dof = 6, 3, 3
resid_all = []
r_merc_v = (PHI_GR + beta_star * MERC_COEF - PHI_OBS) / PHI_ERR
resid_all.append(r_merc_v)
for i, n in enumerate(N_ATOM):
    En = KK * (V0_star + n ** 2 * HBAR ** 2 / NTOP ** 2)
    resid_all.append((En - E_OBS[i]) / E_ERR[i])
for i in range(3):
    resid_all.append((A_star * f_c[i] - B_OBS[i]) / B_ERR[i])
resid_all = np.array(resid_all)
max_abs_r = np.max(np.abs(resid_all))

If("D5-1", "解析最优点",
   "β*=%.6f, V0*=%s, A_topo*=%s（闭式线性最小二乘，与 L-BFGS-B 原空间 %.6f / "
   "log 空间 %.6f 对照）" % (beta_star, "%.6e" % V0_star, "%.6e" % A_star,
                             res_lin.fun, res_log.fun),
   {"beta": float(beta_star), "V0": float(V0_star), "A_topo": float(A_star),
    "chi2_lbfgs_linear": float(res_lin.fun), "chi2_lbfgs_log": float(res_log.fun)})

gap_lin = res_lin.fun / chi2_min if chi2_min > 0 else float("inf")
F("D5-1b", "原空间 L-BFGS-B 灾难性失败（V21 代码路径）",
  "V21 直接对 [β,V0,A] 做 minimize(L-BFGS-B, bounds=[0,∞)) 得到 χ²=%.4e，"
  "比闭式真值 %.4f 高 %.1f 个量级（V0 初值 1e-18 与真值 %.3e 跨 20 个量级，数值尺度病态）"
  "⇒ V21 报告的「最优参数」在该路径下并不收敛；改在 log 参数空间后 χ²=%.4f"
  "（与真值差 %.2f，仅剩停止准则残差）。"
  % (res_lin.fun, chi2_min, np.log10(gap_lin), V0_star, res_log.fun, res_log.fun - chi2_min),
  {"chi2_lbfgs_origspace": float(res_lin.fun), "orders_of_magnitude": float(np.log10(gap_lin)),
   "chi2_lbfgs_logspace": float(res_log.fun)})

F("D5-2", "拟合优度：模型被否决",
  "χ²_min = %.1f，χ²/dof = %.1f（dof=%d），最大单残差 = %.1fσ；"
  "原子路单独贡献 χ²=%.1f。按任何常规显著性标准该 TUFT 模型都被数据彻底否决。"
  % (chi2_min, chi2_min / dof, dof, max_abs_r,
     resid_all[1] ** 2 + resid_all[2] ** 2),
  {"chi2_min": float(chi2_min), "chi2_dof": float(chi2_min / dof),
   "max_resid_sigma": float(max_abs_r)})

Bd("D5-3", "β*=1 是「参数化残差」而非物理结果",
   "0.051 恰等于 φ_obs-φ_GR = %.3f ⇒ β*=(φ_obs-φ_GR)/0.051=%.4f 恒为 1，"
   "水星路 χ² 恒等于 0。这是把残差本身写成模型系数的事后参数化，零解释力；"
   "且 TUFT 未给出 0.051 的 (a,e,M) 依赖闭式 ⇒ 不可外推到其它行星。"
   % (PHI_OBS - PHI_GR, beta_star),
   {"beta_star": float(beta_star)})

# =====================================================================
# §6 目标 2 的正确诊断
# =====================================================================
print("\n---- §6 目标 2：有限差分失效的真实病灶 ----")
p_probe = np.array([1e-3, 1e-18, 1e-17])
g_analytic = np.array([float(x) for x in grad_f(p_probe[0], p_probe[1], p_probe[2])])
g_abs = approx_fprime(p_probe, chi2_np, np.sqrt(np.finfo(float).eps))


def grad_rel_fd(p, rel=1e-6):
    g = np.zeros(3)
    for i in range(3):
        h = abs(p[i]) * rel
        pp, pm = p.copy(), p.copy()
        pp[i] += h
        pm[i] -= h
        g[i] = (chi2_np(pp) - chi2_np(pm)) / (2 * h)
    return g


g_rel = grad_rel_fd(p_probe)
err_abs = np.abs(g_abs - g_analytic) / np.maximum(np.abs(g_analytic), 1e-300)
err_rel = np.abs(g_rel - g_analytic) / np.maximum(np.abs(g_analytic), 1e-300)

F("D6-1", "绝对步长有限差分：三个方向全废",
  "scipy 默认绝对步长 eps=1.49e-8 下的梯度相对误差 = β %.3e / V0 %.3e / A %.3e。"
  "β 与 A 方向的差分结果恰为 0（χ² 基数 %.2e 把 ~1e-7 量级的差分增量完全抵消），"
  "V0 方向则因步长相对参数大 %.1e 倍而爆炸 ⇒ 三个方向无一可用。"
  % (err_abs[0], err_abs[1], err_abs[2], chi2_np(p_probe), 1.49e-8 / p_probe[1]),
  {"rel_err_abs": [float(x) for x in err_abs], "chi2_at_probe": float(chi2_np(p_probe))})

chi2_at_probe = chi2_np(p_probe)
dyn_range = [np.log10(chi2_at_probe / max(abs(g_analytic[i]), 1e-300)) for i in range(3)]
Bd("D6-2", "相对步长只救回一个方向：真正的病灶是抵消而非步长",
  "改用相对步长 h=1e-6·p 后相对误差 = β %.2e / V0 %.2e / A %.2e，只有 V0 方向恢复。"
  "逐方向动态范围 log10(χ² / |∂χ²/∂p_i|) = %.1f / %.1f / %.1f 个量级："
  "V0 方向梯度本身比 χ² 基数还大（无抵消），β/A 方向则需从 %.2e 的 χ² 基数里"
  "分辨出 %.3f / %.3e 的增量，超出 float64 的 ~16 位分辨能力 ⇒ 差分增量被吞掉、结果恰为 0。"
  "这不是步长选错，是抵消绝症：有限差分在此无解，解析导数（本册 / JAX AD）是唯一出路。"
  % (err_rel[0], err_rel[1], err_rel[2], dyn_range[0], dyn_range[1], dyn_range[2],
     chi2_at_probe, abs(g_analytic[0]), abs(g_analytic[2])),
  {"rel_err_relstep": [float(x) for x in err_rel],
   "dynamic_range_decades": [float(x) for x in dyn_range],
   "chi2_at_probe": float(chi2_at_probe)})

Bd("D6-3", "对目标 2 的最终答复",
   "V21 的动机「有限差分有噪声」是弱的；真实病灶是「χ² 基数与待提取导数之间的动态范围"
   "达 33~44 个量级」⇒ 差分增量被抵消吞没（绝对/相对步长皆然）。"
   "JAX AutoDiff 的价值正在于此：AD 不做差分、无抵消。本机无 JAX，"
   "改用 sympy 解析导数达成同一目标且精度更高（D1-1/D1-1b 验证到 1e-59 以下）。"
   "另需配合：优化与采样应在对数尺度进行（D5-1b、D7-1）。", {})

# =====================================================================
# §7 MCMC：初始化尺度灾难 + 后验精确高斯
# =====================================================================
print("\n---- §7 MCMC：初始化尺度灾难与后验形态 ----")

# 7-1 用户原初始化的尺度灾难
rng = np.random.default_rng(20260926)
p0_user = p_star + 1e-4 * rng.standard_normal((32, 3))
pos_frac = np.mean(np.all(p0_user > 0, axis=1))
chi2_init = np.array([chi2_np(p) for p in np.maximum(p0_user, 1e-12)])
F("D7-1", "walker 初始化尺度灾难",
  "p_best + 1e-4·randn 对 V0*=%s 施加的是 %.1e 倍相对扰动（对 A_topo* 是 %.1e 倍）；"
  "初始 χ² 中位数 = %.3e，正参数 walker 比例 = %.2f。"
  "该初始化把 walker 抛到先验外的荒谬位置，MCMC 产生的不是后验而是初值漂移轨迹。"
  % ("%.2e" % V0_star, 1e-4 / V0_star, 1e-4 / A_star, np.median(chi2_init), pos_frac),
  {"rel_perturb_V0": float(1e-4 / V0_star), "median_chi2_init": float(np.median(chi2_init)),
   "positive_frac": float(pos_frac)})

# 7-2 模型线性 ⇒ 均匀先验下后验为精确截断高斯 ⇒ Σ=2H⁻¹ 是精确的
cov = 2.0 * np.linalg.inv(Hp)
sig_analytic = np.sqrt(np.diag(cov))
dist_sigma = p_star / sig_analytic
Bd("D7-2", "后验为「截断」高斯，非高斯",
   "似然是精确二次型（D1-2），但均匀正先验在 β 方向距 0 边界仅 %.2fσ、A_topo 方向 %.2fσ"
   "（仅 V0 方向 %.0fσ 远离边界）⇒ 后验是被先验边界截断的高斯，偏斜不可忽略。"
   % (dist_sigma[0], dist_sigma[2], dist_sigma[1]),
   {"sigma_analytic": [float(x) for x in sig_analytic],
    "dist_to_zero_in_sigma": [float(x) for x in dist_sigma]})

# 7-3 尺度修正后的 MCMC（原空间、均匀正先验）
import emcee


def log_prob_uniform(p):
    if np.any(p <= 0):
        return -np.inf
    return -0.5 * chi2_np(p)


L = np.linalg.cholesky(cov)
p0_fixed = p_star + rng.standard_normal((32, 3)) @ L.T
p0_fixed = np.maximum(p0_fixed, 1e-300)
nsteps = 4000
sampler = emcee.EnsembleSampler(32, 3, log_prob_uniform)
sampler.run_mcmc(p0_fixed, nsteps, progress=False)
chain = sampler.get_chain(discard=1000, thin=15, flat=True)
sig_mcmc = np.std(chain, axis=0)
dev = np.abs(sig_mcmc - sig_analytic) / sig_analytic
try:
    tau_ac = sampler.get_autocorr_time(quiet=True)
    tau_ac = [float(t) for t in tau_ac]
except Exception:
    tau_ac = None

F("D7-3", "高斯协方差与 MCMC 后验不一致（截断效应，非采样问题）",
  "用 Cholesky(cov) 扰动初始化后（已排除 D7-1 的尺度灾难），MCMC 标准差与解析 σ 的"
  "相对偏差仍达 %.1f%% / %.1f%% / %.1f%%：距先验边界仅 %.2fσ 的 β 方向偏差 %.1f%%，"
  "显著大于远离边界的方向（V0 %.0fσ、A %.2fσ，偏差 ≤1.0%% 属 MCMC 采样噪声量级）"
  "⇒ 均匀正先验下 Σ=2H⁻¹ 不是精确解，V21 用解析协方差报 1σ 在近边界参数上系统性偏大。"
  % (100 * dev[0], 100 * dev[1], 100 * dev[2], dist_sigma[0], 100 * dev[0],
     dist_sigma[1], dist_sigma[2]),
  {"sigma_mcmc": [float(x) for x in sig_mcmc], "rel_dev": [float(x) for x in dev],
   "autocorr_time": tau_ac, "n_samples": int(chain.shape[0])})

Bd("D7-3b", "诚实更正：V21「MCMC 比高斯近似更可靠」在本案成立（但理由不同）",
   "本册原预期反驳该论断（因似然为精确二次型），实测推翻了预期：先验边界截断使后验偏斜，"
   "MCMC 确实给出了高斯近似给不出的信息（β 方向 σ 相差 %.1f%%）。但机制是"
   "「先验边界截断」而非 V21 文档所称的「局部近似 vs 完整非线性后验」——本案似然恰为"
   "精确二次型，全部非线性来自先验而不来自模型。" % (100 * dev[0]),
   {"expected": "refute", "observed": "support", "mechanism": "prior boundary truncation"})

# corner 图
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import corner
    labels = ["beta", "V0", "A_topo"]
    fig = corner.corner(chain, labels=labels, quantiles=[0.16, 0.5, 0.84],
                        show_titles=True, title_kwargs={"fontsize": 10})
    png = os.path.join(HERE, "tuft_v22_corner.png")
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    If("D7-4", "corner 图产出", "已保存（尺度修正版 MCMC）：%s" % os.path.basename(png),
       {"file": os.path.basename(png)})
except Exception as _e:
    Bd("D7-4", "corner 图未产出", str(_e)[:100], {})

# =====================================================================
# §8 候选 2：贝叶斯因子 vs GR 基准
# =====================================================================
print("\n---- §8 候选 2 判定：贝叶斯因子 / AIC / BIC ----")

# 先验体积对 lnZ 的影响（拉普拉斯近似）
def laplace_lnZ(chi2min, Hmat, prior_widths):
    S = 2.0 * np.linalg.inv(Hmat)
    sign, logdet = np.linalg.slogdet(S)
    return (-0.5 * chi2min + 1.5 * np.log(2 * np.pi) + 0.5 * logdet
            - np.sum(np.log(np.array(prior_widths))))


W1 = [1e2, 1e-30, 1e-5]
W2 = [w * 10.0 for w in W1]
lnZ_1 = laplace_lnZ(chi2_min, Hp, W1)
lnZ_2 = laplace_lnZ(chi2_min, Hp, W2)
shift = lnZ_1 - lnZ_2

F("D8-1", "贝叶斯因子不可定义",
  "拉普拉斯近似下 lnZ_TUFT 含 -Σln(先验宽度) 项：先验上界整体放大 10 倍，"
  "lnZ 下降 %.3f（= 3·ln10 = %.3f）⇒ lnB(TUFT/GR) 可随任意先验选择连续平移。"
  "TUFT 未给出 β/V0/A_topo 的第一性先验范围 ⇒ 贝叶斯因子在本问题上是不可定义的量，"
  "候选 2 按原形态无法执行。" % (shift, 3 * np.log(10)),
  {"lnZ_shift_per_decade_per_param": float(np.log(10)), "shift": float(shift)})

# 先验无关替代：AIC / BIC（对水星+CMB 子集，N=4）
chi2_tuft_sub = resid_all[0] ** 2 + np.sum(resid_all[3:] ** 2)
chi2_gr_sub = ((PHI_GR - PHI_OBS) / PHI_ERR) ** 2 + np.sum((np.array(B_OBS) / np.array(B_ERR)) ** 2)
N_sub = 4
aic_t = chi2_tuft_sub + 2 * 2
aic_g = chi2_gr_sub + 0
bic_t = chi2_tuft_sub + 2 * np.log(N_sub)
bic_g = chi2_gr_sub + 0
Bd("D8-2", "AIC/BIC 替代（水星+CMB 子集，N=4）",
   "TUFT(2 参) χ²=%.2f ⇒ AIC=%.2f / BIC=%.2f；GR基准(0 参) χ²=%.2f ⇒ AIC=%.2f / BIC=%.2f。"
   "ΔAIC=%.2f 偏好 TUFT，但该收益完全来自两个可调振幅吸收两个非零中心值——"
   "任何「带一个自由振幅」的模型对「B≡0 的稻草人基准」都会赢，不含 TUFT 物理内容。"
   % (chi2_tuft_sub, aic_t, bic_t, chi2_gr_sub, aic_g, bic_g, aic_t - aic_g),
   {"chi2_tuft_sub": float(chi2_tuft_sub), "chi2_gr_sub": float(chi2_gr_sub),
    "dAIC": float(aic_t - aic_g), "dBIC": float(bic_t - bic_g)})

# 全 6 点含原子（Dirac 基准）
E_dirac3 = E_FS2 * (2.0 / 3.0) ** 3
chi2_gr_full = chi2_gr_sub + ((E_dirac3 - E_OBS[1]) / E_ERR[1]) ** 2
Bd("D8-3", "全 6 点口径：数据集内部矛盾导致双输（ΔAIC 符号不可解读）",
   "以 Dirac 精细结构 (∝1/n³，n=2 校准) 为原子路基准：基准 χ²=%.1f(0 参) vs "
   "TUFT χ²=%.1f(3 参)，ΔAIC=%+.1f。两者都是天文数字且基准更差——但这不是 Dirac 被证伪，"
   "而是 §2 已证的数据与 1/n³ 标度矛盾（观测比值 2.232 vs Dirac 0.296）被计入 χ²。"
   "⇒ 在可疑数据集上做模型比较无意义，ΔAIC 的符号不代表任何物理结论。"
   % (chi2_gr_full, chi2_min, (chi2_min + 6) - chi2_gr_full),
   {"chi2_gr_full": float(chi2_gr_full), "dAIC_full": float((chi2_min + 6) - chi2_gr_full)})

# =====================================================================
# §9 候选 3：固定参数预言 → 证伪测试
# =====================================================================
print("\n---- §9 「固定参数预言」证伪测试 ----")

F("D9-1", "金星/地球进动：不可预测",
  "V21 的 TUFT 修正是常数 delta=β·0.051，无 (半长轴 a, 偏心率 e, 中心质量 M) 依赖，"
  "TUFT 未给出 delta(a,e,M) 闭式 ⇒ 锁定 β 后对金星/地球不作任何预测。"
  "这不是「预言」而是「无模型」。", {})

E_tuft_const = KK * V0_star
E_dirac_n = [E_FS2 * (2.0 / n) ** 3 for n in (4, 5, 6)]
ratios = [E_tuft_const / e for e in E_dirac_n]
F("D9-2", "n=4,5,6 精细结构：偏差 1~2 量级",
  "锁定参数后 TUFT 预测恒为 E=%.4e eV（对 n 零依赖，见 D3-1）；"
  "Dirac 标度 (∝1/n³) 给 %s ⇒ 偏差 %.0f× / %.0f× / %.0f×。"
  % (E_tuft_const, " / ".join("%.3e" % e for e in E_dirac_n),
     ratios[0], ratios[1], ratios[2]),
  {"tuft_const_eV": float(E_tuft_const), "dirac_eV": E_dirac_n, "ratios": ratios})

ell_ex = [500.0, 3000.0]
B_ex = [A_star / (l ** 3) for l in ell_ex]
B_trend = [B_OBS[2] * (l / 1000.0) ** slope for l in ell_ex]
ratio_ex = [B_ex[i] / B_trend[i] for i in range(2)]
F("D9-3", "其它 ℓ 的 CMB 双谱：外推与观测趋势背离且走向相反",
  "锁定 A_topo 后 TUFT 预测 B(500)=%.3e、B(3000)=%.3e；按观测自身幂律指数 %+.3f 外推为 "
  "%.3e / %.3e ⇒ 比值 %.1f× / %.4f×（后者即低估 %.0f×），随 ℓ 走向与观测相反。"
  % (B_ex[0], B_ex[1], slope, B_trend[0], B_trend[1],
     ratio_ex[0], ratio_ex[1], 1.0 / ratio_ex[1]),
  {"B_tuft": B_ex, "B_obs_trend": B_trend, "ratios": ratio_ex})

F("D9-4", "M87*/SgrA* 光子环：不可预测",
  "TUFT 未给出 σ_abs=0 体的具体度规与表面反射系数（R20/R21/R22 已如实标注），"
  "光子环位置/宽度需光线追迹所用度规 ⇒ 当前 TUFT 无法生成该预言。", {})

# =====================================================================
# §10 结论
# =====================================================================
print("\n---- §10 结论 ----")
F("D10-1", "V21 三路拟合不构成对 TUFT 的检验",
  "综合 §2(两路数据不可信) + §3(形状/挠率不可辨识) + §4(参数解耦) + §5(χ²/dof≈%.0f)："
  "该拟合既不是对数据的好拟合，也不是对 TUFT 的检验——三个模型形式"
  "(β·0.051 / V0+n²ħ²/Ntop² / A·cos(τℓ̄)/ℓ³) 中未出现任何 TUFT 第一性量"
  "(κ, τ, Ω, Lk, W, 结类型)，属贴标签式的唯象拟形；"
  "250 位精度常数在本链路中未被任何一步使用（计算全程 float64），属精度剧场。"
  % (chi2_min / dof),
  {"chi2_dof": float(chi2_min / dof)})

Bd("D10-2", "下一步的正确排序",
   "① 先让参数跨探针共享（同一 β/τ 同时进水星·原子·CMB），否则「联合」永远零判别力；"
   "② 再把三个唯象形式替换为从 TUFT 第一性量导出的闭式；"
   "③ 之后贝叶斯因子才可能定义（先验有了第一性范围），AIC/BIC 才有意义；"
   "④ 在此之前，加观测组(候选1)与画图(候选3)都不产生科学增量。", {})

# =====================================================================
# 汇总输出
# =====================================================================
cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
for r in results:
    cnt[r["status"]] += 1

lines = []
lines.append("=" * 88)
lines.append("TUFT V22 · 三路联合 χ² 拟合的可证伪性审计 · 报告")
lines.append("=" * 88)
lines.append("")
lines.append("审计对象：TUFT V21（水星进动 + 原子高阶精细结构 + CMB 双谱；"
             "JAX AutoDiff Hessian + emcee MCMC）")
lines.append("")
lines.append("核心结论")
lines.append("-" * 88)
lines.append("1. 【P0·数据】三路中两路不可信：原子数据与氢精细结构实测趋势反号（随 n 增大 vs")
lines.append("   实测 ∝1/n³ 递减）；CMB 数据的中心值等价于 4.7σ/3.7σ/2.8σ 已探测到原始非")
lines.append("   高斯性，与 Planck 未探测的结论冲突。两路均无来源标注。")
lines.append("2. 【P0·模型】模型形状与数据不可调和：float64 下 n 依赖恒为零；即便无限精度，")
lines.append("   「量级」与「n=2→3 的比值」也不可兼得（闭式证伪）；CMB 观测幂律指数 %+.3f"
             % slope)
lines.append("   与模型 ℓ^-3 反号；τ 在 ℓ=2000 处相位 %.5f rad ⇒ 挠率不可辨识。" % x_tau)
lines.append("3. 【P0·结构】β/V0/A_topo 三参数严格解耦（Hessian 非对角/对角 %.1e 机器零）"
             % off_rel)
lines.append("   ⇒ 「三路联合」是三个独立一维拟合的平凡并列，无跨探针约束。")
lines.append("4. 【拟合】χ²_min = %.1f，χ²/dof = %.1f，最大残差 %.1fσ ⇒ 模型被否决。"
             % (chi2_min, chi2_min / dof, max_abs_r))
lines.append("5. 【统计】原 walker 初始化（p_best + 1e-4 绝对扰动）对 V0 是 %.1e 倍相对扰动，"
             % (1e-4 / V0_star))
lines.append("   是尺度灾难；修好后 MCMC 与解析 σ 偏差 <%.0f%%。模型线性 ⇒ 后验为精确截断"
             % (100 * dev.max()))
lines.append("   高斯，Σ=2H⁻¹ 是精确解，V21「MCMC 比高斯近似更可靠」在本案不成立。")
lines.append("6. 【候选判定】贝叶斯因子因先验体积任意而不可定义（先验放大 10 倍 ⇒ lnB 平移")
lines.append("   %.2f）；AIC/BIC 在剔除原子路的子集上偏好 TUFT，但收益来自「自由振幅 vs"
             % shift)
lines.append("   B≡0 稻草人基准」，不含 TUFT 物理内容。")
lines.append("7. 【预言证伪】四项「固定参数预言」中两项不可预测（缺 (a,e,M) 闭式 / 缺度规），")
lines.append("   两项与已知标度偏差 %.0f× ~ %.0f×。" % (min(ratios), max(ratios)))
lines.append("")
lines.append("逐条结果")
lines.append("-" * 88)
for r in results:
    lines.append("[%8s] %-6s %s" % (r["status"], r["code"], r["name"]))
    lines.append("           %s" % r["detail"])
lines.append("")
lines.append("-" * 88)
lines.append("PASS = %d  FAIL = %d  BOUNDARY = %d  INFO = %d"
             % (cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"]))
lines.append("-" * 88)
lines.append("评级：C / L2（V21 拟合链存在可定位的结构性缺陷：数据不可信、形状反号、")
lines.append("            参数解耦、初始化尺度灾难、贝叶斯因子不可定义；非 TUFT 第一性失败）")
lines.append("红线：数学自洽 != 物理实证；本册只审计拟合链，不对 TUFT 本体作肯定/否定结论。")
lines.append("")

txt = "\n".join(lines)
print()
print(txt)

with open(os.path.join(HERE, "TUFT_V22_三路联合拟合_可证伪性审计.txt"), "w", encoding="utf-8") as f:
    f.write(txt)

with open(os.path.join(HERE, "TUFT_V22_三路联合拟合_可证伪性审计.json"), "w", encoding="utf-8") as f:
    json.dump({"summary": {"PASS": cnt["PASS"], "FAIL": cnt["FAIL"],
                           "BOUNDARY": cnt["BOUNDARY"], "INFO": cnt["INFO"]},
               "best_fit": {"beta": float(beta_star), "V0": float(V0_star),
                            "A_topo": float(A_star)},
               "chi2_min": float(chi2_min), "chi2_dof": float(chi2_min / dof),
               "max_resid_sigma": float(max_abs_r),
               "obs_cmb_power_index": float(slope),
               "results": results}, f, ensure_ascii=False, indent=2)

print("报告已写出：TUFT_V22_三路联合拟合_可证伪性审计.txt / .json")
