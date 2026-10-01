# -*- coding: utf-8 -*-
"""
tuft_htuft_particle_spectrum_v1.py
==================================

H-TUFT 拓扑孤子量子数与质量/CKM 数值求解 —— **脚手架（非预言）**

用途：补齐 CUR-12（卷二十八）的 `script_ref`（此前为未落盘）。
内容与**卷二十八 §10.3「修正可运行版」对齐**（numpy；原稿 §10.1 用 jax）。

红线（承卷二十八 §5/§6/§10.2/§10.4）：
- 质量公式 `m = m0·(0.21 Q² + 0.08 n_s + κ(πn)²)` 的**三个系数全自由**（无第一性导出）；
  `M0 = 0.511e-3 GeV` 是**外部锚**（②级，非第一性）——「引进外部锚即放弃第一性质量预言」（卷二十九 H5）。
- 三代质量层级**实跑失败**：模态谱 `(πn)² = 1:4:9` vs 实测 `1:206.8:3477.6` ⇒ 差 **52× / 386×**。
- CKM 纯拓扑 ansatz **给近单位阵**，非 CKM 结构（须自由 θ~0.2 才得 |V12|≈0.223）。
- 【本文件对 §10.3 的一处修正】原文 `build_unitary_overlap` 用 `np.linalg.eigh(H − H†)`——
  `H − H†` 是**反厄米**矩阵，`eigh` 假定厄米，结果无效。本文件改用**极分解**
  `V = H (H†H)^{-1/2}`（对 `H†H` 用 eigh，合法），得到真正的幺正矩阵。
- 本文件**不声称**任何可检验预言；输出仅暴露原稿的定量失败与形式修复。

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

M0 = 0.511e-3            # 外部锚（电子质量，GeV）——②级，非第一性
A_COEF, B_COEF = 0.21, 0.08   # m_top 自由系数
MEASURED_RATIOS = (1.0, 206.77, 3477.2)   # m_e : m_mu : m_tau（PDG pole）
CKM_V12 = 0.22500        # |V_us| 实测（用于对照）


def m_topological(Q_hel, n_s):
    return A_COEF * Q_hel ** 2 + B_COEF * n_s


def mode_energy(n, kappa):
    return kappa * (np.pi * n) ** 2


def m_physical(Q_hel, n_s, kappa, n, m0=M0):
    """物理质量（修复三：给 GeV 单位）。"""
    return m0 * (m_topological(Q_hel, n_s) + mode_energy(n, kappa))


def build_unitary_overlap(H):
    """极分解幺正化 V = H·(H†H)^{-1/2}（对 H†H 用 eigh，合法）。

    注：原文用 eigh(H − H†)（反厄米）——结果无效；此处为修正版。
    """
    A = H.conj().T @ H
    w, V = np.linalg.eigh(A)              # A 厄米半正定
    w = np.clip(w, 1e-300, None)
    inv_sqrt = V @ np.diag(w ** -0.5) @ V.conj().T
    return H @ inv_sqrt


def yukawa_overlap(Psi_i, Psi_j, measure):
    """修复二：L2 内积（替代楔积），良定义。"""
    return np.sum(Psi_i.conj() * Psi_j * measure)


def build_toy_overlap(alpha, Q_base, size=3):
    """卷二十八 §10.1 玩具交叠矩阵 M_ij = 0.15·e^{iαQ(i−j)}/(1+|i−j|·0.4)。"""
    M = np.zeros((size, size), dtype=complex)
    for i in range(size):
        for j in range(size):
            M[i, j] = 0.15 * np.exp(1j * alpha * Q_base * (i - j)) / (1 + abs(i - j) * 0.4)
    return M


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 78)
    print("H-TUFT 拓扑粒子谱系 · 脚手架实跑（非预言）")
    print("红线：质量三系数自由；层级实跑失败；CKM ansatz 近似单位阵")
    print("=" * 78)

    Q_hel, n_s, kappa = 1.0, 1.0, 0.0035
    print("[A] 三代质量（Q_hel=%.0f, n_s=%.0f, kappa=%.4f, M0=%.3e GeV 外部锚）"
          % (Q_hel, n_s, kappa, M0))
    masses = [m_physical(Q_hel, n_s, kappa, n) for n in (1, 2, 3)]
    for n, m in zip((1, 2, 3), masses):
        print("    代 %d: m = %.4e GeV" % (n, m))

    pred_total = np.array(masses) / masses[0]
    pred_mode = np.array([1.0, 4.0, 9.0])
    print("    预测层级(总)   = %.3f : %.3f : %.3f" % tuple(pred_total))
    print("    预测层级(模态) = %.1f : %.1f : %.1f" % tuple(pred_mode))
    print("    实测层级       = %.1f : %.1f : %.1f" % MEASURED_RATIOS)
    fails = [MEASURED_RATIOS[i] / pred_mode[i] for i in (1, 2)]
    print("    ⇒ 模态谱失败倍数 = %.1f× / %.1f×（与卷二十八 §5.2「52×/386×」一致）"
          % (fails[0], fails[1]))

    print("[B] CKM 交叠幺正化（极分解；原文 eigh(H−H†) 修正）")
    H = build_toy_overlap(alpha=0.08, Q_base=1.0)
    V = build_unitary_overlap(H)
    row = np.linalg.norm(V, axis=1)
    col = np.linalg.norm(V, axis=0)
    print("    行范数 = [%.3f, %.3f, %.3f]；列范数 = [%.3f, %.3f, %.3f]（幺正 ⇒ 全 1）"
          % (row[0], row[1], row[2], col[0], col[1], col[2]))
    print("    |V| 矩阵：")
    for i in range(3):
        print("      [%s]" % "  ".join("%.4f" % abs(V[i, j]) for j in range(3)))
    print("    |V12| = %.4f  vs 实测 CKM |V_us| = %.4f  ⇒ 纯拓扑 ansatz 近单位阵（非 CKM 结构）"
          % (abs(V[0, 1]), CKM_V12))

    print("[C] Yukawa L2 内积（修复二）示例")
    psi_i = np.array([1.0, 0.5, 0.2], dtype=complex)
    psi_j = np.array([0.5, 1.0, 0.3], dtype=complex)
    print("    <Psi_i|Psi_j>_L2 = %.4f（良定义，替代楔积）"
          % float(np.real(yukawa_overlap(psi_i, psi_j, 1.0))))

    print("-" * 78)
    print("诚实结论：形式修复（幺正/带单位/良定义）完成，但质量层级仍失败 52×/386×、")
    print("          CKM 仍近单位阵 ⇒ 脚手架不携带可检验物理量（承卷二十八 §10.4）。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
