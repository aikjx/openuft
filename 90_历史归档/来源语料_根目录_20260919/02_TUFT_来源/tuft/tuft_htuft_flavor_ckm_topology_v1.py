# -*- coding: utf-8 -*-
"""
tuft_htuft_flavor_ckm_topology_v1.py
====================================

H-TUFT 味物理：拓扑隧穿 CKM 矩阵 —— **脚手架（非预言）**

用途：补齐补充卷F 的 `script_ref`。内容对齐补充卷F §4/§5/§10（原稿用 jax，此处 numpy）。

红线（承补充卷F §0 与本文件实跑）：
- 原稿 §5 断言「拓扑隧穿带来复相位，自动生成 CKM 的 CP 破坏相位」。本文件**实跑反证**：
  形如 `V_ij = exp(-β|i-j| + iδ)` 的矩阵（**单一全局相位** δ）其 **Jarlskog 不变量 J = 0**
  ⇒ **不产生 CP 破坏**（J 需要**相对**相位，全局相位可被场重定义消除）。
- 原稿 |V| 层级只**定性**；定量对实测：|V_ub| 差 ~26×、|V_cb| 差 ~7.5×、对角元恒 =1（实测 <1）。
- 原稿 §3 质量式 `m ∝ α√Q(1+λn)` 与 **CUR-12（卷二十八）** 的 `m = m0(0.21Q²+0.08n_s+κ(πn)²)`
  **是两套不同的公式**（同语料内两个质量公式 ⇒ 内部不一致）；且 `(1+λn)` 给 `1:1.22:1.44`，
  比 CUR-12 的 `1:4:9` **更远离**实测 `1:207:3477`。
- 本文件**不声称**任何可检验预言；输出仅暴露原稿的定量/结构性缺陷。
- 归一化：本卷与 **CUR-12** 主题重叠，定位为「CKM 深化」并**复用** CUR-12 引擎，不另起炉灶。

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

# PDG |V_CKM|（Wolfenstein 级别近似）
CKM_MEASURED = np.array([
    [0.97373, 0.22430, 0.00382],
    [0.22430, 0.97350, 0.04220],
    [0.00860, 0.04100, 0.99910],
])
MEASURED_MASS_RATIOS = (1.0, 206.77, 3477.2)   # m_e : m_mu : m_tau


def ckm_amplitude(n_i, n_j, beta, delta):
    """原稿 §5：拓扑隧穿振幅 V_ij = exp(-β|n_i-n_j| + iδ)。"""
    return np.exp(-beta * abs(n_i - n_j)) * np.exp(1j * delta)


def build_ckm_raw(beta, delta, size=3):
    """原稿 §10 的隧穿矩阵（未做 SVD）。"""
    V = np.zeros((size, size), dtype=complex)
    for i in range(size):
        for j in range(size):
            V[i, j] = ckm_amplitude(i, j, beta, delta)
    return V


def build_ckm_svd(beta, delta, size=3):
    """原稿 §10 的 SVD 近似幺正版（U@Vh 为极分解因子）。"""
    V = build_ckm_raw(beta, delta, size)
    U, S, Vh = np.linalg.svd(V)
    return U @ Vh


def jarlskog(V):
    """Jarlskog 不变量 J = Im(V_us V_cb V_ub* V_cs*)（CKM CP 破坏度量；J=0 ⇒ 无 CP 破坏）。"""
    return float(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))


def fermion_mass(n, alpha, Q_base, lam):
    """原稿 §3/§10：m ∝ α·√Q_base·(1+λn)（与 CUR-12 公式不同）。"""
    return alpha * np.sqrt(Q_base) * (1.0 + lam * n)


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 80)
    print("H-TUFT 拓扑隧穿 CKM · 脚手架实跑（非预言；首要用途=复核原稿自值）")
    print("红线：全局相位 ⇒ J=0 ⇒ 不产生 CP 破坏；量级只定性")
    print("=" * 80)
    beta, delta = 1.15, 0.78

    print("[A] 原稿隧穿矩阵 |V_ij| = exp(-β|i-j|)（β=%.2f）vs 实测 |V_CKM|" % beta)
    V_raw = build_ckm_raw(beta, delta)
    labels = (("Vud", 0, 0), ("Vus", 0, 1), ("Vub", 0, 2),
              ("Vcb", 1, 2), ("Vtb", 2, 2))
    print("    %-5s %-12s %-12s %s" % ("元素", "模型|V|", "实测|V|", "偏差倍数"))
    for name, i, j in labels:
        m, e = abs(V_raw[i, j]), CKM_MEASURED[i, j]
        print("    %-5s %-12.4f %-12.5f %.2f×" % (name, m, e, m / e))

    print("[B] CP 破坏：Jarlskog 不变量（原稿称『自动生成 CP 相位』）")
    print("    J(原稿隧穿矩阵, 单一全局相位 δ=%.2f) = %.3e" % (delta, jarlskog(V_raw)))
    V_svd = build_ckm_svd(beta, delta)
    print("    J(SVD 近似幺正版)                     = %.3e" % jarlskog(V_svd))
    print("    ⇒ J = 0（解析必然：V = e^{iδ}·A，A 实对称 ⇒ 相位相消）")
    print("    ⇒ **不产生 CP 破坏**；『自动生成 CP 相位』= 错（全局相位可被场重定义消除）")

    print("[C] 质量层级（原稿 §3：m ∝ √Q_base·(1+λn)，λ=0.22）")
    lam, alpha, Q_base = 0.22, 0.07, 12
    ms = [fermion_mass(n, alpha, Q_base, lam) for n in (0, 1, 2)]
    ratios = np.array(ms) / ms[0]
    print("    模型层级 = %.3f : %.3f : %.3f" % tuple(ratios))
    print("    实测层级 = %.1f : %.1f : %.1f" % MEASURED_MASS_RATIOS)
    print("    ⇒ 失败倍数 = %.1f× / %.1f×（**比 CUR-12 的 1:4:9 更远离**实测）"
          % (MEASURED_MASS_RATIOS[1] / ratios[1], MEASURED_MASS_RATIOS[2] / ratios[2]))
    print("    注：CUR-12（卷二十八）用 m=m0(0.21Q²+0.08n_s+κ(πn)²) ⇒ 同语料两套质量公式，不一致")

    print("[D] 诚实结论")
    print("    ⇒ ①CP 破坏未生成（J=0，结构性）；②|V_ub| 差 ~26×、|V_cb| 差 ~7.5×（只定性）；")
    print("      ③质量层级失败更甚且与 CUR-12 公式冲突；④『解释为何只三代』(§2) 是断言，")
    print("      与卷二十八 §4.3『稳定性判据缺失』/卷二十九 H2(⑤级) 直接冲突。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
