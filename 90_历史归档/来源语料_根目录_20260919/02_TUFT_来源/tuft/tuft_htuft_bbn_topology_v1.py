# -*- coding: utf-8 -*-
"""
tuft_htuft_bbn_topology_v1.py
=============================

H-TUFT 拓扑缺陷的 BBN（原初核合成）约束 —— **首次实算（脚手架 + 划界工具）**

背景（本文件要检验的既有宣称）：
  - 卷二十七 §8/§9：「BBN 边界**自动满足**」（§9 表自评为 ❌ 宣称：未计算注入上限；
    §11 [E] 的量级粗检「通过」**只因 `A_gw` 人为取小**）。
  - 补充卷G（CUR-19）§8：「螺旋弦衰变产生的粒子辐射不会破坏轻元素丰度，**自动满足** BBN 边界」。
  - 判据 L：「拓扑缺陷演化**违反 BBN**」为证伪触发条件。
  ⇒ 本文件把这条**从未计算**的约束真正算出来。

红线（本文件实跑）：
1. **区分两类「壁」**（原稿混用，这是 BBN 结论的关键）：
   (a) **气泡壁**（bubble wall）：一级相变期间瞬态存在，碰撞后消失 ⇒ 只贡献引力波能量密度；
   (b) **畴壁网络**（domain wall network）：破缺真真空**简并**（`pi_0(V) != 0`）时**持久**存在，
       进入 scaling regime 后 `rho_wall ~ sigma * H`，`rho_wall/rho_rad ∝ T^{-2}`
       ⇒ 随宇宙降温**增长** ⇒ **畴壁问题（domain wall problem）**。
   补充卷G §3 明确把相变壁称作「拓扑畴壁」，但**从未指定** `pi_0(V)` 是否为非平凡
   ⇒ **BBN 结论在原稿中是未定的**，「自动满足」**未证**。
2. **对畴壁分支给出定量上限**：`sigma_wall` 必须满足 BBN 的 `Delta N_eff` 上限。
3. **引力波通道**：`Delta N_eff` 贡献极小（`~1e-9` 级）⇒ 该通道**安全**。
   ⇒ 危险的不是引力波，而是**持久畴壁网络**。
4. **「自动满足」是自证循环**：取 `A_gw`/`sigma` 足够小 ⇒ 约束「通过」；这不是证据（见定理 H）。

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

# ---- BBN 纪元常数 ----
M_PL_GEV = 1.2209e19          # 普朗克质量 [GeV]
T_BBN_GEV = 1.0e-3            # BBN 起始 ~1 MeV
G_STAR_BBN = 10.75            # 1 MeV 处有效自由度
NEFF_SM = 3.044               # 标准模型 N_eff
NEFF_OBS = 2.99               # Planck 2018 (TT,TE,EE+lowE+lensing)
NEFF_SIGMA = 0.17             # 1 sigma
DNEFF_MAX = 2.0 * NEFF_SIGMA  # 95% CL 上限 ~0.34（本文件取 0.30 保守）

# Delta N_eff <-> rho_extra/rho_gamma : Delta N_eff = (8/7)(11/4)^(4/3) * (rho_extra/rho_gamma)
K_NEFF = (8.0 / 7.0) * (11.0 / 4.0) ** (4.0 / 3.0)   # ~4.404


def rho_rad(T, g_star=G_STAR_BBN):
    """辐射能量密度 [GeV^4]。"""
    return (np.pi ** 2 / 30.0) * g_star * T ** 4


def hubble(T, g_star=G_STAR_BBN):
    """辐射主导期哈勃参数 [GeV]。"""
    return 1.66 * np.sqrt(g_star) * T ** 2 / M_PL_GEV


def dw_scaling_density(sigma, T, g_star=G_STAR_BBN):
    """畴壁 scaling regime 能量密度：每个哈勃体积一面墙 ⇒ rho ~ sigma * H。"""
    return sigma * hubble(T, g_star)


def dw_fraction(sigma, T, g_star=G_STAR_BBN):
    """rho_wall / rho_rad（畴壁分支）。"""
    return dw_scaling_density(sigma, T, g_star) / rho_rad(T, g_star)


def delta_neff_from_frac(frac):
    """由 rho_extra/rho_gamma 反推 Delta N_eff。"""
    return K_NEFF * frac


def sigma_max_from_neff(T=T_BBN_GEV, dneff_max=DNEFF_MAX, g_star=G_STAR_BBN):
    """BBN 上限反解畴壁张力 sigma_wall 的上限 [GeV^3]。"""
    frac_max = dneff_max / K_NEFF
    return frac_max * rho_rad(T, g_star) / hubble(T, g_star)


def t_dominate(sigma, g_star=G_STAR_BBN):
    """使 rho_wall = rho_rad 的温度 [GeV]（低于此温度畴壁主导）。"""
    return np.sqrt(1.66 * sigma / (0.32899 * M_PL_GEV * np.sqrt(g_star)))


def gw_delta_neff(rho_gw_over_rho_rad):
    """引力波对 Delta N_eff 的贡献（极小）。"""
    return K_NEFF * rho_gw_over_rho_rad


def sigma_of_scale(scale_gev):
    """把「能量标度 L」换算为 sigma = L^3。"""
    return scale_gev ** 3


def _demo():
    print("=" * 74)
    print("补充卷I：H-TUFT 拓扑缺陷的 BBN 约束 —— 首次实算")
    print("=" * 74)
    print("背景常数：T_BBN=1 MeV, g_*=%.2f, N_eff(SM)=%.3f, 观测 %.2f±%.2f" % (
        G_STAR_BBN, NEFF_SM, NEFF_OBS, NEFF_SIGMA))

    print("\n" + "-" * 74)
    print("[0] Delta N_eff <-> rho_extra/rho_gamma 换算")
    print("-" * 74)
    print("  K = (8/7)(11/4)^(4/3) = %.4f" % K_NEFF)
    for dn in (0.1, DNEFF_MAX, 1.0):
        print("  Delta N_eff = %.2f  <=>  rho_extra/rho_gamma = %.4f" % (dn, dn / K_NEFF))
    print("  => 95%%CL 上限取 Delta N_eff_max = %.2f  =>  frac_max = %.4f" % (
        DNEFF_MAX, DNEFF_MAX / K_NEFF))

    print("\n" + "-" * 74)
    print("[1] 【量化】畴壁分支：sigma_wall 的 BBN 上限")
    print("-" * 74)
    s_max = sigma_max_from_neff()
    print("  sigma_max = %.4e GeV^3   =>  sigma_max^(1/3) = %.1f GeV = %.2f TeV" % (
        s_max, s_max ** (1.0 / 3.0), s_max ** (1.0 / 3.0) / 1e3))
    print("  （即畴壁张力不得高于 ~8 TeV 量级，否则 1 MeV 前畴壁主导辐射）")

    print("\n" + "-" * 74)
    print("[2] 【对照】若 sigma 取普朗克/相变标度会怎样")
    print("-" * 74)
    cases = [
        ("普朗克 (M_Pl)^3", M_PL_GEV),
        ("相变标度 (1e15 GeV)^3 [卷二十九 T_c 上限]", 1.0e15),
        ("(1 TeV)^3", 1.0e3),
        ("(8 TeV)^3 ≈ 上限", s_max ** (1.0 / 3.0)),
    ]
    for name, scale in cases:
        sig = sigma_of_scale(scale)
        fr = dw_fraction(sig, T_BBN_GEV)
        print("  sigma=%s: frac(1MeV)=%.3e, Delta N_eff=%.3e  %s" % (
            name, fr, delta_neff_from_frac(fr),
            "[**超标 %.2e 倍**]" % (fr / (DNEFF_MAX / K_NEFF)) if fr > DNEFF_MAX / K_NEFF else "[OK]"))

    print("\n" + "-" * 74)
    print("[3] 【机制】畴壁问题是**增长型**：rho_wall/rho_rad ∝ T^{-2}")
    print("-" * 74)
    sigma_probe = sigma_of_scale(1.0e15)     # 相变标度
    for T in (1.0e15, 1.0e12, 1.0e9, 1.0e6, 1.0e3, 1.0e-3):
        print("  T=%9.1e GeV  rho_wall/rho_rad = %.3e   Delta N_eff = %.3e" % (
            T, dw_fraction(sigma_probe, T), delta_neff_from_frac(dw_fraction(sigma_probe, T))))
    print("  => 降温 10^18 倍，比值涨 10^36 倍（不存在『自动满足』）。")
    print("  畴壁主导温度 T_dom = %.3e GeV（= %.3e MeV）" % (
        t_dominate(sigma_probe), t_dominate(sigma_probe) * 1e3))
    print("  上限张力对应 T_dom = %.3e GeV（= %.3e MeV）⇒ 恰在 BBN 门限附近（自洽）" % (
        t_dominate(s_max), t_dominate(s_max) * 1e3))

    print("\n" + "-" * 74)
    print("[4] 【澄清】引力波通道是安全的（危险的不是 GW）")
    print("-" * 74)
    for ogw in (1e-9, 1e-7, 1e-5):
        print("  rho_GW/rho_rad = %.1e  ->  Delta N_eff = %.3e" % (ogw, gw_delta_neff(ogw)))
    print("  => GW 即使取 1e-5，Delta N_eff ~ 4e-5，远低于 0.3 上限（安全）。")

    print("\n" + "-" * 74)
    print("[5] 【自证循环】『自动满足』的实质（定理 H）")
    print("-" * 74)
    print("  卷二十七 §9 自评已指出：量级粗检『通过』**只因 A_gw 人为取小**。")
    print("  实跑佐证：frac ∝ sigma（或 A_gw），取小 ⇒ 约束通过；取大 ⇒ 约束破坏。")
    print("  约束的**满足与否只由自由参数决定** ⇒ 它**不是**理论的一次检验（定理 H）。")

    print("\n" + "=" * 74)
    print("结论")
    print("=" * 74)
    print("  ① 畴壁分支（pi_0(V)!=0）：BBN 给出 **量化上限 sigma_wall <~ %.1f TeV 的三次方**；" % (s_max ** (1.0 / 3.0) / 1e3))
    print("     普朗克量级张力超限 ~%.2e 倍，相变标度张力超限 ~%.2e 倍。" % (
        dw_fraction(sigma_of_scale(M_PL_GEV), T_BBN_GEV) / (DNEFF_MAX / K_NEFF),
        dw_fraction(sigma_of_scale(1e15), T_BBN_GEV) / (DNEFF_MAX / K_NEFF)))
    print("  ② 气泡壁分支（pi_0(V)=0，瞬态）：GW 通道安全，BBN 可通过（但需锚定 GW 谱）。")
    print("  ③ 原稿**从未指定** `pi_0(V)`，故『自动满足』**未证**；且在畴壁分支下**被排除**。")
    print("  ④ 该约束对自由参数单调依赖 ⇒ 满足它是**取小**而非**预言**（定理 H）。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 74)
    print("本文件 SHA256 =", _selfhash())
    print("定位：脚手架 + 划界工具（非预言）。数学自洽 != 实验证实。")
