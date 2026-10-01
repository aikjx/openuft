# -*- coding: utf-8 -*-
"""
tuft_htuft_vacuum_topology_lambda_v1.py
=======================================

H-TUFT 真空拓扑能与宇宙学常数 —— 求解器（**脚手架，非预言**）

红线（与补充卷B §0 一致，守 TUFT「数学自洽 ≠ 实验证实」）：
- 原稿 §10 用 `jax`（本机不可用）；本文件用 numpy 复刻，语义等价。
- 本文件首要用途是**诚实复核原稿自值**，并**量纲审计**。结论：
  ①原稿公式 `rho_top = alpha*chi*M_Pl^4/V_4` **量纲错**（应为 [能量]^4，实得
    [能量]^4/[长度]^4）；②原稿脚本混用 SI 引力常数 G=6.6743e-11 与 GeV 单位
    （自然单位应为 G=1/M_Pl^2≈6.7e-39）；③实跑 Ω_Λ ≈ 3.6e101（观测 0.6889），
    **差 ~102 量级**；④若补上 V_4=哈勃四体积，却变成 ~1e-92，**差 ~46 量级（过小）**；
  ⑤**结构性定理**：拓扑项 ∫F∧F 是**全导数/与度规无关** ⇒ 对 T_μν 贡献=0 ⇒
    **不能产生宇宙学常数**（这正是本路线的根本困难，非数值问题）。
- 本文件**不声称**导出了 Λ；输出仅用于暴露原稿缺陷并给出量纲自洽的对照。

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

# 物理常数（原稿值）
M_PL_GEV = 1.2209e19          # 普朗克质量 [GeV]
G_SI = 6.67430e-11            # 原稿所用引力常数（SI, m^3 kg^-1 s^-2）——单位存疑
OMEGA_LAMBDA_PLANCK = 0.6889  # Planck 2018
# 观测真空能密度（量级）：ρ_Λ ≈ (2.3 meV)^4
RHO_LAMBDA_OBS_GEV4 = (2.3e-3 * 1e-9) ** 4   # (2.3 meV -> GeV)^4 ≈ 2.8e-46
H0_PER_S = 67.66 / 3.086e19   # 原稿 H0 换算 [1/s]
GEV_PER_S = 6.582119569e-25   # 1 s^-1 = 6.582e-25 GeV（ℏ）


def rho_topological(alpha, chi, M_pl):
    """原稿 §3：真空拓扑能密度（alpha·chi·M_Pl⁴/V_4；此处先不含 V_4）。"""
    return alpha * chi * M_pl ** 4


def Lambda_from_rho(rho_top, G=None):
    """原稿 §3：Lambda = 8πG ρ_top（G 缺省用原稿的 SI 值）。"""
    g = G_SI if G is None else G
    return 8.0 * np.pi * g * rho_top


def omega_lambda(Lam, H0):
    """原稿 §5：Omega_Lambda = Lambda/(3 H0^2)。"""
    return Lam / (3.0 * H0 ** 2)


def sha256_of_this_file():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _demo():
    print("=" * 80)
    print("H-TUFT 真空拓扑能与宇宙学常数 · 脚手架实跑（非预言；首要用途=复核原稿自值）")
    print("红线：数学自洽 ≠ 实验证实；拓扑项不源引力（结构性困难）")
    print("=" * 80)

    alpha, chi = 0.07, 2

    print("[A] 复现原稿 §10：alpha=0.07, chi=2, M_Pl=1.2209e19 GeV, H0=%.4e 1/s" % H0_PER_S)
    rho_t = rho_topological(alpha, chi, M_PL_GEV)
    lam = Lambda_from_rho(rho_t)                # 用原稿 SI G
    om = omega_lambda(lam, H0_PER_S)
    print("    rho_top = %.4e (GeV^4 形态，未含 V_4)" % rho_t)
    print("    Lambda  = %.4e  (原稿 SI G=%.4e)" % (lam, G_SI))
    print("    Omega_Lambda_pred = %.4e   （Planck 目标 = %.4f）" % (om, OMEGA_LAMBDA_PLANCK))
    print("    偏差倍数 = %.3e  ⇒ 差 ~%.1f 个量级" %
          (om / OMEGA_LAMBDA_PLANCK, np.log10(abs(om / OMEGA_LAMBDA_PLANCK))))
    print("    ⇒ 原稿『从拓扑参数导出 Omega_Lambda』的宣称**不成立**（差 ~10^102）。")

    print("[B] 量纲审计")
    print("    目标：rho_top 应为 [能量]^4（GeV^4）")
    print("    原稿：alpha*chi*M_Pl^4/V_4 ⇒ [能量]^4/[长度]^4（多除长度^4，量纲错）")
    print("    原稿脚本 G=6.6743e-11 是 SI 值；自然单位 G=1/M_Pl^2 = %.4e（GeV^-2）"
          % (1.0 / M_PL_GEV ** 2))
    print("    ⇒ SI G 与 GeV G 相差 %.3e 倍 ⇒ Lambda=8πG rho 混用单位，数值无意义。"
          % (G_SI / (1.0 / M_PL_GEV ** 2)))

    print("[C] 若补上 V_4（哈勃四体积，自然单位）")
    H0_gev = H0_PER_S * GEV_PER_S              # GeV
    V4_hub = (1.0 / H0_gev) ** 4               # GeV^-4
    rho_t_v4 = rho_t / V4_hub
    print("    H0 = %.4e GeV ; 1/H0 = %.4e GeV^-1 ; V_4 = %.4e GeV^-4"
          % (H0_gev, 1.0 / H0_gev, V4_hub))
    print("    rho_top(with V_4) = %.4e GeV^4" % rho_t_v4)
    print("    观测 rho_Lambda ≈ %.4e GeV^4" % RHO_LAMBDA_OBS_GEV4)
    print("    ⇒ 比值 = %.3e  ⇒ 差 ~%.1f 个量级（**过小**，非过大）"
          % (rho_t_v4 / RHO_LAMBDA_OBS_GEV4, np.log10(abs(rho_t_v4 / RHO_LAMBDA_OBS_GEV4))))

    print("[D] 是否规避了 10^120 灾难？")
    print("    朴素（丢 V_4）rho_top = %.4e GeV^4" % rho_t)
    print("    比值 rho_top/rho_Lambda = %.3e  ⇒ 差 ~%.1f 个量级（≈ 原 10^120 灾难）"
          % (rho_t / RHO_LAMBDA_OBS_GEV4, np.log10(abs(rho_t / RHO_LAMBDA_OBS_GEV4))))
    print("    ⇒ 原稿『天然规避 10^120』**不成立**：含 V_4 变 10^46 过小，不含则复现 10^120。")

    print("[E] 结构性定理（本路线根本困难，非数值）")
    print("    拓扑项 ∫F∧F 为全导数/与度规无关 ⇒ 变分 δS/δg = 0 ⇒ 对 T_μν 贡献 = 0")
    print("    ⇒ **拓扑项不能产生宇宙学常数**（与 A 中欧拉示性数同理，均为总导数项）")
    print("    注：4 维 Gauss-Bonnet / Nieh-Yan 亦为总导数，不进入体运动方程。")

    print("[F] 与卷三十全局框架的关系（不可被本通道救回）")
    print("    卷三十已证全联合 Z=0（EDM/g-2/ringdown 恒 -inf）；新增 chi2_Lambda 不能救回。")

    print("-" * 80)
    print("诚实结论：原稿 5 处硬伤——①Omega_Lambda 实跑差 ~102 量级；②公式量纲错；")
    print("          ③SI/自然单位混用；④『规避 10^120』不成立；⑤拓扑项不源引力（结构不可能）。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
