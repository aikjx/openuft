# -*- coding: utf-8 -*-
"""
tuft_htuft_global_mcmc_v1.py
============================

H-TUFT 全局 MCMC 联合拟合 —— **H-TUFT 扩展层（复用卷二十三引擎，不重复造轮子）**

红线（与卷三十 §0 一致，守 TUFT「数学自洽 ≠ 实验证实」）：
- **归一化**：本文件**不重写**全局 MCMC 引擎，而是 `import tuft_global_mcmc_nested_OPEN_v1`
  （= 卷二十三「全局 MCMC 贝叶斯联合推断」，已是诚实实现），复用其：
  ①通道状态分类（CLOSED/OPEN/UNVALIDATED）；②CLOSED 通道的 -inf 硬排除；
  ③CMB 似然 `_ll_ns`/`_ll_r`；④先验机制与 `slow_roll`。
  本层只**新增** H-TUFT 专属通道（SGWB、CMB 手征 f_NL）与其参数空间。
- **不伪造数据**：原稿 §11 把 Ω_GW=1e-10、QNM 频移 σ=0.012、EDM σ=1e-29 当作
  「实测值」构造高斯 χ²。三者**均无实测**（EDM 只有上限、QNM 频移未测、
  Ω_GW 无弦谱探测）。本层按 UNVALIDATED 处理（贡献 0，不激活），**不编造测量**。
- **决定性事实**：H-TUFT 低能投影**继承** TUFT 已关闭的三窗口
  （EDM 超 1.28e16 / g-2 偏 75% / ringdown 5.74σ）。含这些通道的联合似然对
  **所有**样本恒为 0 ⇒ 后验为空、证据 `Z=0`（严格，无需采样）。
  故「全局拟合排名 H-TUFT 优于 ΛCDM」的预期**方向反了**：诚实结果是**双双被排除**。
- 原稿 §11 代码**不可运行**：`from tuft_EDM_实验对接_OPEN6 import compute_edm` 等
  六处 import 中，多个模块**无该函数**或**根本不存在**（见本文件 §自查 `_audit_imports`）。
- 编号说明：原稿标题「卷二十九」与既有 `tuft_卷二十九_..._审计白皮书.md` 冲突；
  本卷定为**卷三十**（见 md §0.1）。

依赖 numpy；复用 `tuft_global_mcmc_nested_OPEN_v1.py`（同目录）。
"""

import hashlib
import importlib.util
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:  # Windows GBK 控制台防 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import tuft_global_mcmc_nested_OPEN_v1 as base  # 卷二十三：单一真源
import tuft_htuft_cosmic_string_v1 as cs        # 本卷卷二十七：SGWB 脚手架


# ----------------------------------------------------------------------
# 1) H-TUFT 参数空间（原稿 §2）
# ----------------------------------------------------------------------
# 诚实修正：原稿 T_B∈[0,1e-22] 含 0（对数采样无定义）且无标度来源（卷二十 O-SCALE）。
HTUFT_PRIORS = [
    ("alpha",    0.0,   0.2,   "flat"),   # 拓扑耦合（无实验约束）
    ("Q_hel",    1.0,   3.0,   "disc"),   # 离散整数 1,2,3（混合离散采样）
    ("T_c",      1e14,  1e17,  "log"),    # 相变临界温度 GeV
    ("T_B",      1e-30, 1e-22, "log"),    # 背景挠率 eV（原稿含 0 → 已改正下限）
    ("kappa",    1e-4,  1e-2,  "log"),    # 孤子模态系数
    ("tau_corr", 0.0,   0.1,   "flat"),   # 弦张力挠率修正
]
HTUFT_NDIM = len(HTUFT_PRIORS)


# ----------------------------------------------------------------------
# 2) H-TUFT 通道表：继承 base 的 8 通道 + 新增 2 个（均 UNVALIDATED）
# ----------------------------------------------------------------------
HTUFT_EXTRA_CHANNELS = {
    "SGWB": dict(
        status="UNVALIDATED", kind="cosmo",
        reason="Ω_GW 幅度是自由参数、手征偏振无机制（卷二十七 §0.5）；无弦谱实测 "
               "⇒ 不激活（拒绝把 Ω_GW=1e-10 当作『数据』）",
    ),
    "CMB_chiral_fNL": dict(
        status="UNVALIDATED", kind="cmb",
        reason="手征 f_NL 无推导、无幅值（卷二十七 §0.6）⇒ 不激活",
    ),
}


def all_channel_status():
    """合并 base 的 8 通道 + H-TUFT 新增 2 通道的状态表。"""
    merged = dict(base.CHANNELS)
    merged.update(HTUFT_EXTRA_CHANNELS)
    return merged


# ----------------------------------------------------------------------
# 3) H-TUFT 前向模型（CMB 轴为占位，H-TUFT 未导出 ns-r 映射）
# ----------------------------------------------------------------------
def htuft_forward(theta):
    alpha, Q_hel, T_c, T_B, kappa, tau_corr = theta
    # CMB 轴：H-TUFT 未导出 ns-r 映射；借用 base 的 tau 参数化作占位（诚实标注）
    sr = base.slow_roll(2.7, 1.0)
    return dict(ok=True, ns=sr["ns"], r=sr["r"], alpha=alpha, Q_hel=Q_hel,
                T_c=T_c, T_B=T_B, kappa=kappa, tau_corr=tau_corr)


def htuft_log_likelihood(fm, include_closed=True):
    ll = 0.0
    ll += base._ll_ns(fm)          # CMB ns（OPEN，占位）
    ll += base._ll_r(fm)           # CMB r（OPEN，单边上限）
    ll += 0.0                      # SGWB：UNVALIDATED，贡献 0（不伪造）
    ll += 0.0                      # CMB 手征 f_NL：UNVALIDATED，贡献 0
    if include_closed:
        ll += base._ll_edm(fm)         # -inf（H-TUFT 继承 TUFT 已关窗口）
        ll += base._ll_g2(fm)          # -inf
        ll += base._ll_ringdown(fm)    # -inf
    return ll


def htuft_log_prob(theta, include_closed=True):
    for (name, lo, hi, kind), val in zip(HTUFT_PRIORS, theta):
        if not (lo - 1e-12 < val < hi + 1e-12):
            return -np.inf
    fm = htuft_forward(theta)
    ll = htuft_log_likelihood(fm, include_closed=include_closed)
    return ll if np.isfinite(ll) else -np.inf


# ----------------------------------------------------------------------
# 4) 自查：核验原稿 §11 声称的似然子模块是否真的存在/可用（不执行，只读源码）
# ----------------------------------------------------------------------
_IMPORT_CLAIMS = [
    ("tuft_EDM_实验对接_OPEN6", "compute_edm"),
    ("tuft_g2_电子反常磁矩_OPEN5", "compute_g2"),
    ("tuft_sigma_abs0_ringdown_可检验性_OPEN_v2", "ringdown_qnm_shift"),
    ("tuft_beta_running_缺口_定理N实例化", "beta_rg_flow"),
    ("tuft_htuft_cosmic_string_v1", "omega_gw"),
    ("tuft_htuft_particle_spectrum_v1", "m_topological"),
]


def _module_has_symbol(modname, symbol):
    try:
        spec = importlib.util.find_spec(modname)
    except Exception as exc:
        return ("MISSING_MODULE", str(exc))
    if spec is None or not spec.origin:
        return ("MISSING_MODULE", "no spec")
    try:
        with open(spec.origin, "r", encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
    except Exception as exc:
        return ("UNREADABLE", str(exc))
    if ("def %s(" % symbol) in txt or ("class %s(" % symbol) in txt:
        return ("OK", os.path.basename(spec.origin))
    return ("MISSING_SYMBOL", "no %s() in %s" % (symbol, os.path.basename(spec.origin)))


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 76)
    print("H-TUFT 全局 MCMC 联合拟合 · H-TUFT 扩展层（复用卷二十三引擎）")
    print("红线：数学自洽 ≠ 实验证实；不伪造测量；已被排除的窗口不可被拟合救回")
    print("=" * 76)

    print("[A] H-TUFT 通道路由（继承 base 8 通道 + 新增 2）")
    for k, v in all_channel_status().items():
        print("    %-15s [%-11s] %s" % (k, v["status"], v["kind"]))

    print("[B] 决定性事实：含 CLOSED 通道时，联合似然恒为 -inf ⇒ Z=0（严格）")
    rng = np.random.default_rng(20260930)
    n_finite = 0
    n_try = 200
    for _ in range(n_try):
        th = [rng.uniform(lo, hi) for (_, lo, hi, _k) in HTUFT_PRIORS]
        if np.isfinite(htuft_log_prob(th, include_closed=True)):
            n_finite += 1
    print("    随机 %d 样本中有限 logL 数 = %d" % (n_try, n_finite))
    print("    ⇒ H-TUFT 全通道证据 Z_H-TUFT = 0 与 Z_TUFT = 0 相同（均被微观窗口排除）")

    print("[C] 新增通道的约束力审计（H-TUFT 6 参数是否被任何激活通道约束？）")
    active = [k for k, v in all_channel_status().items() if v["status"] == "OPEN"]
    unval = [k for k, v in all_channel_status().items() if v["status"] == "UNVALIDATED"]
    closed = [k for k, v in all_channel_status().items() if v["status"] == "CLOSED"]
    print("    激活(OPEN)=%s  未推导(UNVALIDATED)=%s  已关闭(CLOSED)=%s"
          % (active, unval, closed))
    print("    ⇒ H-TUFT 6 参数中，α/Q_hel/kappa 依赖味与散射（未激活）、")
    print("      T_c/T_B/tau_corr 依赖 SGWB/CMB 手征（UNVALIDATED）⇒ 全部无约束。")
    print("    ⇒ 无约束参数对证据贡献因子 1（后验=先验）⇒ H-TUFT 相对 TUFT **无证据增益**。")

    print("[D] 模型比对（诚实结论）")
    print("    Z_H-TUFT(全联合) = Z_TUFT(全联合) = 0（严格）")
    print("    lnB(H-TUFT / ΛCDM+SM) = -inf  ⇒ ΛCDM 压倒性占优")
    print("    lnB(H-TUFT / TUFT) = 0/0（两者同被排除）⇒ 原稿『定量比较二者优劣』**无意义**")

    print("[E] 原稿 §11 似然子模块可用性自查（证明其代码不可运行）")
    for mod, sym in _IMPORT_CLAIMS:
        state, info = _module_has_symbol(mod, sym)
        print("    %-42s %-14s %s" % (mod + "." + sym, state, info))

    print("-" * 76)
    print("诚实结论：本层为『复用型扩展脚手架』——全局拟合的诚实产出是**对 TUFT/H-TUFT")
    print("          的统计排除（Z=0）**，而非对 ΛCDM 的优势；原稿的『测量值』与 import 均虚构。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
