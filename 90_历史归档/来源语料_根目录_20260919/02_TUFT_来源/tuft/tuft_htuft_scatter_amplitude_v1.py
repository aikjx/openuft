# -*- coding: utf-8 -*-
"""
tuft_htuft_scatter_amplitude_v1.py
==================================

H-TUFT 螺旋孤子 2→2 拓扑散射振幅 —— **脚手架（非预言）**

用途：补齐 CUR-10（卷二十六）的 `script_ref`（此前为「预期，未落盘」）。
内容与**卷二十六 §11 逐字对齐**（仅将原稿的 `jax` 换为 numpy，语义等价）。

红线（承卷二十六 §0）：
- `A_dyn = 1/(s − 0.01i)` 是**玩具极点**，无运动学推导；
- `A_top = 0.12·exp(iαΔQ√s)`：`0.12` 为**任意常数**，相位形式**未从 S_top 导出**；
- 该相位随 √s 振荡，与卷二十六 §6「Q_hel 严格守恒 ⇒ 相位应为常数」**内部矛盾**；
- 纯加性振幅**未展示 S 矩阵幺正化**。
- 本文件**不声称**任何可检验预言；输出仅为管道脚手架。

依赖 numpy；不引入新假设。
"""

import hashlib
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def scattering_amplitude(s, Q1, Q2, alpha):
    """H-TUFT 螺旋孤子 2→2 拓扑散射振幅（脚手架：A_dyn 玩具极点，A_top 幅度/相位均自由）。"""
    A_dyn = 1.0 / (s - 1.0j * 0.01)                    # 玩具极点，无运动学推导
    delta_Q = Q1 - Q2                                  # 注：§6 称 Q_hel 守恒，此处用入射差（内部不一致）
    A_top = 0.12 * np.exp(1j * alpha * delta_Q * np.sqrt(s))  # 0.12 任意；相位形式未从 S_top 导出
    return A_dyn + A_top


def diff_cross_section(s, Q1, Q2, alpha):
    amp = scattering_amplitude(s, Q1, Q2, alpha)
    sigma = np.abs(amp) ** 2
    sigma_sm = np.abs(1.0 / (s - 1.0j * 0.01)) ** 2
    return sigma, sigma - sigma_sm


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 76)
    print("H-TUFT 拓扑散射振幅 · 脚手架实跑（非预言）")
    print("红线：A_dyn 玩具极点；A_top 幅度/相位均自由；与 §6 守恒律矛盾")
    print("=" * 76)
    alpha, Q1, Q2 = 0.08, 1, -1
    s = np.linspace(1.0, 120.0, 2000)
    phase = alpha * (Q1 - Q2) * np.sqrt(s)
    print("[A] 相位跨度：alpha*ΔQ*√s = %.3f .. %.3f rad（= %.2f 个 2π 周期）"
          % (phase[0], phase[-1], (phase[-1] - phase[0]) / (2 * np.pi)))
    sigma, dsigma = diff_cross_section(s, Q1, Q2, alpha)
    print("[B] |A_top|^2 = 0.12^2 = %.4f（任意量级）；|Δσ| 峰值 = %.4f" %
          (0.12 ** 2, np.max(np.abs(dsigma))))
    print("[C] 诚实：整段 s∈[1,120] 相位仅扫过 <1 个完整周期（周期全由自由 α 决定）")
    print("    纯加性振幅，未展示 S 矩阵幺正化 ⇒ 管道脚手架，非预言")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
