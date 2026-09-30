# -*- coding: utf-8 -*-
"""
tuft_htuft_darkmatter_soliton_v1.py
===================================

H-TUFT 高拓扑荷孤子暗物质 —— 遗迹丰度 & 直接探测截面求解器（**脚手架，非预言**）

红线（与补充卷A §0 一致，守 TUFT「数学自洽 ≠ 实验证实」）：
- 原稿 §10 使用 `jax`（本机不可用），系数（1.2e14、0.28、1.0537e-5、1.2e-44）
  全部是**魔数**（无推导）。本文件用 numpy 复刻，语义等价。
- 本文件的首要用途是**诚实复核原稿自身数值**：证明原稿「可复现 Planck Ω_DM=0.265」
  的宣称**不成立**（实跑 Ω_DM ~1e-26，差 ~25 量级）。
- `n_freeze ∝ 1/T_f³` **量纲自相矛盾**：数密度 n 应为 [能量]³（∝ T³），
  原稿写 1/T³ 使 ρ=m·n 量纲退化，故 Ω_DM 数值无物理意义。
- `m_soliton=m_top·Q^γ` 的 γ（1.4~1.8）与 m_top **均为自由参数**，与「Ω_DM 不是
  自由输入、是派生量」的宣称**矛盾**（§0.4）。本文件演示：要命中 0.265 必须反向调参。
- 本文件**不声称**任何可检验预言；输出仅用于暴露原稿公式的数值/量纲缺陷。

依赖 numpy；不引入新假设。
"""

import hashlib
import os
import sys

import numpy as np

try:  # Windows GBK 控制台防 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 原稿常量（补充卷A §10）
MAGIC = dict(n_coeff=1.2e14, Tf_frac=0.28, rho_crit=1.0537e-5, sigma0=1.2e-44)
OMEGA_DM_PLANCK = 0.265


def soliton_mass(Q_hel, m_top, gamma):
    """高拓扑荷孤子质量（原稿 §4：m = m_top · Q^γ）。"""
    return m_top * Q_hel ** gamma


def omega_dm_pred(alpha, Tc, Q_hel, m_top, gamma):
    """原稿 §10 丰度公式（逐字复刻，含其量纲问题）。"""
    T_f = MAGIC["Tf_frac"] * Tc
    n_freeze = MAGIC["n_coeff"] * alpha ** 1.5 / T_f ** 3     # 原稿：∝ 1/T^3（量纲存疑）
    m_dm = soliton_mass(Q_hel, m_top, gamma)
    rho_dm = m_dm * n_freeze
    omega = rho_dm / MAGIC["rho_crit"]
    return dict(omega=omega, m_dm=m_dm, n_freeze=n_freeze, T_f=T_f, rho_dm=rho_dm)


def sigma_direct(alpha, Q_hel, sigma0=None):
    """原稿 §5：挠率介导孤子-核子散射截面 σ = σ0·α²·Q²（σ0 为魔数）。"""
    s0 = MAGIC["sigma0"] if sigma0 is None else sigma0
    return s0 * alpha ** 2 * Q_hel ** 2


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 78)
    print("H-TUFT 高拓扑荷孤子暗物质 · 脚手架实跑（非预言；首要用途=复核原稿自值）")
    print("红线：数学自洽 ≠ 实验证实；魔数与量纲须先修")
    print("=" * 78)

    alpha, Q_hel, Tc, m_top, gamma = 0.07, 12, 1e15, 0.12, 1.5

    print("[A] 复现原稿 §10 参数：alpha=0.07, Q_hel=12, Tc=1e15, m_top=0.12, gamma=1.5")
    r = omega_dm_pred(alpha, Tc, Q_hel, m_top, gamma)
    print("    T_f = %.3e (GeV)  n_freeze = %.4e" % (r["T_f"], r["n_freeze"]))
    print("    m_dm = %.4e (GeV)  rho_dm = %.4e" % (r["m_dm"], r["rho_dm"]))
    print("    Omega_DM_pred = %.4e   （Planck 目标 = %.3f）" % (r["omega"], OMEGA_DM_PLANCK))
    ratio = OMEGA_DM_PLANCK / r["omega"] if r["omega"] else float("inf")
    print("    偏差倍数 = %.3e  ⇒ 差 ~%.1f 个量级" % (ratio, np.log10(abs(ratio))))
    print("    ⇒ 原稿『可复现 Planck Omega_DM』的宣称**不成立**。")

    print("[B] 量纲自检：n_freeze 应为 [能量]^3（∝ T^3），原稿为 ∝ 1/T^3")
    n_t3 = MAGIC["n_coeff"] * alpha ** 1.5 * r["T_f"] ** 3
    print("    原稿 n_freeze = %.3e (GeV^-3 形态)" % r["n_freeze"])
    print("    若按 n ∝ T^3（同系数）：n = %.3e (GeV^3)  ⇒ 差 %.3e 倍" %
          (n_t3, n_t3 / r["n_freeze"]))
    print("    ⇒ rho = m·n 的量纲随实现方式改变，Omega_DM 数值无物理意义。")

    print("[C] 反解证明『Omega_DM 是派生量』不成立（须反向调参才能命中 0.265）")
    n_req = OMEGA_DM_PLANCK * MAGIC["rho_crit"] / r["m_dm"]
    mtop_req = OMEGA_DM_PLANCK * MAGIC["rho_crit"] / r["n_freeze"]
    print("    命中 0.265 需 n_freeze = %.3e（原稿给 %.3e，差 %.2e 倍）"
          % (n_req, r["n_freeze"], n_req / r["n_freeze"]))
    print("    或需 m_top = %.3e GeV（原稿取 0.12；荒谬量级）" % mtop_req)
    print("    ⇒ 丰度不是被『导出』，而是被 m_top/γ/n_coeff 反向对齐拟合。")

    print("[D] 直接探测截面：原稿自称『远低于 WIMP』是否成立？")
    sig = sigma_direct(alpha, Q_hel)
    print("    原稿 sigma0 = %.2e cm^2（本身即 WIMP 量级魔数）" % MAGIC["sigma0"])
    print("    alpha^2*Q_hel^2 = %.4f  ⇒ sigma = %.3e cm^2" % (alpha ** 2 * Q_hel ** 2, sig))
    print("    参照（WIMP-nucleon SI，近似量级）：XENONnT/LZ 最佳 ~1e-48 ~ 1e-47 cm^2")
    print("    ⇒ sigma 与 sigma0 同量级（仅低 ~0.15 dex），**并非**『远低于 WIMP』；")
    print("      在低质量端反而可能落入/触碰当前上限 ⇒ 原稿自称自相矛盾。")

    print("[E] 与卷三十全局框架的关系（不可被本通道救回）")
    print("    卷三十已证：全联合 Z=0（EDM/g-2/ringdown 三窗已关，恒 -inf）。")
    print("    新增 chi2_DM **不能**使联合证据>0 ⇒ 本通道无法改变全局排除结论。")

    print("-" * 78)
    print("诚实结论：本模块暴露原稿 4 处硬伤——①Omega_DM 实跑差 ~25 量级；")
    print("          ②n_freeze 量纲反；③丰度靠反向调参而非派生；④截面自称『远低于 WIMP』不成立。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
