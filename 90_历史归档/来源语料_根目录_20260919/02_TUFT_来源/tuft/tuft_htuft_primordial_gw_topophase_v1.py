# -*- coding: utf-8 -*-
"""
tuft_htuft_primordial_gw_topophase_v1.py
========================================

H-TUFT 拓扑相变原初引力波 —— **脚手架（非预言）**

用途：补齐补充卷G 的 `script_ref`。内容对齐补充卷G §3/§4/§6/§10（原稿用 jax，此处 numpy）。

红线（承补充卷G §0 与本文件实跑）：
1. 原稿 §4 断言「拓扑泡壁碰撞辐射手征引力波 ΔΠ≠0」。**真空泡壁碰撞的标准结果是左右手对称（ΔΠ=0）**；
   非零 ΔΠ 需**视宇称破缺耦合**（Chern-Simons / 挠率手征项），原稿与卷二十七 §0.5 同样**未给机制**。
2. 原稿 `ΔΠ = σ_coeff·α^1.5`：`σ_coeff`、`α` 皆自由 ⇒ ΔΠ 是**自由参数**，不是导出量。
3. 原稿谱 `Ω = ω_peak·x²/(1+x⁴)`（x=k/k_*）：**两自由参数（ω_peak, k_*）的双幂律 ansatz**，
   无成核率/泡壁速度/β_H 等相变动力学输入 ⇒ 非预言（撞定理 B/D：自由参数编码连续量）。
4. 原稿 §3 `σ_wall ∝ α/l_Pl²`：α 无量纲 ⇒ 量纲 = [l_Pl⁻²] = [能量²]，
   但**面张力应为 [能量³]**（能量/面积）⇒ **量纲反**（同补充卷A 的 Ω_DM 量纲反之误）。
5. 「原初引力波与宇宙常数同源」建立在 **CUR-15（补充卷B）已实跑失败**的 Λ 导出之上
   （Ω_Λ 实跑 3.62e101 ≠ 0.6889）⇒ 依**定理 A** 不成立。
6. 原稿 §6 `tb_amp = 0.12·ΔΠ`：系数 `0.12` 为**魔法常数**，且振幅 ∝ ΔΠ（自身自由） ⇒ 不可预言。
7. 原稿「手征不对称 ⇒ 排除单场暴胀」**过度**：轴子暴胀/CS 耦合亦给手征 GW；只能排除**最小**单场暴胀。
8. 本文件**不声称**任何可检验预言；输出仅暴露原稿的定量/结构性缺陷。
9. 归一化：本卷与 **CUR-11（卷二十七）** 主题重叠（同为手征引力波 + CMB 手征），
   定位为「相变源深化（域壁 vs 弦）」并**复用**其口径，不重复登记主结构。

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

# 现役 CMB 张量上限（BICEP/Keck+Planck 2021 量级，r < 0.036 @95%CL）
R_UPPER_95CL = 0.036


def gw_omega(k, k_star, omega_peak):
    """原稿 §4 拓扑相变引力波谱（双幂律 ansatz）。"""
    x = np.asarray(k, dtype=float) / float(k_star)
    return omega_peak * x**2 / (1.0 + x**4)


def chiral_asymmetry(alpha, sigma_coeff):
    """原稿 §4 手征不对称：ΔΠ = σ_coeff · α^1.5。"""
    return float(sigma_coeff) * float(alpha) ** 1.5


def cmb_tb_cross(delta_pi, coeff=0.12):
    """原稿 §6 手征 GW 诱导的 TB 交叉关联近似振幅。"""
    return float(coeff) * float(delta_pi)


def peak_of_ansatz(k_star, omega_peak):
    """解析峰：dΩ/dx=0 ⇒ x=1 ⇒ k=k_*，Ω_peak = ω_peak/2。"""
    return float(k_star), float(omega_peak) / 2.0


def sigma_wall_dimension_check():
    """§3 `σ_wall ∝ α/l_Pl²` 的量纲审计。

    自然单位 (c=ħ=1)：长度⁻¹ = 能量。
    α 无量纲 ⇒ α·l_Pl⁻² = α·M_Pl²（能量²）。
    面张力 [能量/面积] = [能量³]（能量密度 M_Pl⁴ 除以长度 M_Pl⁻¹）。
    ⇒ 两者差**一个能量量纲**（缺一个 M_Pl 因子）。
    """
    alpha_power = 0.0                              # 无量纲
    claimed_energy_power = alpha_power + 2.0       # l_Pl⁻² = M_Pl²
    expected_energy_power = 3.0                    # 面张力 = M_Pl³
    return dict(claimed_energy_power=claimed_energy_power,
                expected_energy_power=expected_energy_power,
                mismatch_power=expected_energy_power - claimed_energy_power)


def check_chirality_is_free():
    """扫描 (α, σ_coeff)：证明 ΔΠ 是自由旋钮。"""
    rows = []
    for a in (0.02, 0.07, 0.20):
        for s in (0.10, 0.45, 1.00):
            rows.append((a, s, chiral_asymmetry(a, s)))
    return rows


def run_original_demo():
    """复刻原稿 §10 的实跑（jax → numpy）。"""
    alpha, sigma_coeff = 0.07, 0.45
    k_star, omega_peak = 0.008, 1.2e-16
    k_list = np.logspace(-3, -1, 12)
    om = np.array([gw_omega(k, k_star, omega_peak) for k in k_list])
    dpi = chiral_asymmetry(alpha, sigma_coeff)
    tb = cmb_tb_cross(dpi)
    return k_list, om, dpi, tb


def _demo():
    print("=" * 70)
    print("补充卷G §10 复刻实跑（numpy 版，参数取原稿默认）")
    print("=" * 70)
    k_list, om, dpi, tb = run_original_demo()
    print("  k (1/Mpc)        Omega_GW")
    for k, o in zip(k_list, om):
        print("  %.4e       %.3e" % (k, o))
    print("  手征不对称 Delta_Pi = %.3e" % dpi)
    print("  CMB TB 交叉振幅    = %.3e" % tb)

    kp, opk = peak_of_ansatz(0.008, 1.2e-16)
    print("\n  解析峰：k_* = %.4f /Mpc, Omega_peak = %.3e (= omega_peak/2)" % (kp, opk))
    print("  ⇒ 峰值与谱形**完全**由人为参数 (k_*, omega_peak) 决定，无相变动力学输入。")

    print("\n" + "=" * 70)
    print("[诚实体检 1] 畴壁面能量纲（§3  sigma_wall ~ alpha / l_Pl^2）")
    print("=" * 70)
    d = sigma_wall_dimension_check()
    print("  原稿能量幂次 = +%.0f（α 无量纲 · l_Pl^-2 = M_Pl^2）" % d["claimed_energy_power"])
    print("  应有能量幂次 = +%.0f（面张力 = 能量/面积 = M_Pl^3）" % d["expected_energy_power"])
    print("  差 = %.0f 个能量量纲（缺一个 M_Pl ~ 1.2e19 GeV 因子）⇒ **量纲不匹配**" % d["mismatch_power"])
    print("  （同类于补充卷A 的 Omega_DM 量纲反）。")

    print("\n" + "=" * 70)
    print("[诚实体检 2] Delta_Pi 自由度（§4  Delta_Pi = sigma_coeff * alpha^1.5）")
    print("=" * 70)
    for a, s, v in check_chirality_is_free():
        print("  alpha=%-5.2f sigma_coeff=%-5.2f -> Delta_Pi = %.4e" % (a, s, v))
    print("  ⇒ (alpha, sigma_coeff) 皆自由 ⇒ Delta_Pi 可取任意值，**不可预言**。")

    print("\n" + "=" * 70)
    print("[诚实体检 3] 手征机制（§4）")
    print("=" * 70)
    print("  真空泡壁碰撞的标准结果：GW 左右手产额对称 ⇒ Delta_Pi = 0。")
    print("  非零 Delta_Pi 需视宇称破缺耦合（CS 项 / 挠率手征项）——原稿未给，")
    print("  与卷二十七 §0.5 对『弦手征偏振无机制』的判定**同因**。")

    print("\n" + "=" * 70)
    print("[诚实体检 4] 与暴胀的可区分性（§5）")
    print("=" * 70)
    print("  『Delta_Pi != 0 ⇒ 排除单场暴胀』**过度**：轴子暴胀 / CS 耦合亦给手征 GW。")
    print("  正确表述：仅排除**最小**单场慢滚暴胀（其 Delta_Pi 恒为 0）。")
    print("  且原稿未给出 r：现役上限 r < %.3f（95%%CL）无法与该谱振幅对照。" % R_UPPER_95CL)

    print("\n" + "=" * 70)
    print("[诚实体检 5] 与既有条目重叠（归一化）")
    print("=" * 70)
    print("  CUR-11（卷二十七）：螺旋弦 SGWB + CMB 手征  —— 已登记同一检测通道。")
    print("  CUR-06（卷二十二）：挠率暴胀 + CMB 原初扰动 —— 暴胀定位冲突。")
    print("  CUR-15（补充卷B）：真空拓扑能/Λ          —— 本卷『同源』依赖其已失败结论。")
    print("  ⇒ 本卷定位为『相变源深化（域壁）』真增量，不重复登记主结构。")


def _selfhash():
    here = os.path.abspath(__file__)
    with open(here, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 70)
    print("本文件 SHA256 =", _selfhash())
    print("定位：脚手架（非预言）。数学自洽 != 实验证实。")
