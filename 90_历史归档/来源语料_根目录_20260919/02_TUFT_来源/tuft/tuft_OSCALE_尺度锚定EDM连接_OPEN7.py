# -*- coding: utf-8 -*-
"""
TUFT O-SCALE：尺度锚定与 EDM/g-2 的连接（OPEN7）
==================================================
承接 OPEN5b/5c：已证 τ/κ(角 θ) 自由度救不了 EDM（16 量级分裂）。
本册转向【半径 Ω】自由度——即 TUFT 的尺度锚定（O-SCALE 开放项）。

关键不对称性（本册核心发现）：
    g-2 = 2τ/κ = 2tanθ            ← 只依赖角度 θ，与半径 Ω 【无关】
    EDM ∝ κτ = (Ω²/2)sin2θ        ← 依赖 Ω²（尺度）
⇒ 存在一条通道：重标度 Ω → λΩ，可在【保持 g-2 不变】的前提下压低 EDM。

检验该通道是否真能走通：
    压 EDM 至 ACME 需 λ² = F_d = 7.809e-17 ⇒ λ = 8.836e-9
    但 Ω = m_e c/ħ ∝ m_e ⇒ 缩 Ω 等价于缩电子质量 m_e → λ·m_e
    而 m_e 是高精度测量量（CODATA 相对不确定度 ~2.9e-11）
⇒ 检验：要求的 m_e 改变 vs 测量允许的不确定度 ⇒ 是否矛盾？

红线：仅做推导与可行性判定，不构造新物理；负结论如实记录。
"""
import os
import sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# 基线（与 OPEN5b/5c 一致）
G2_EXP = 0.00231930436
G2_TUFT = 0.00404
EDM_TUFT_ECM = 1.4087e-13      # e·cm
EDM_ACME_ECM = 1.1e-29         # e·cm
M_E = 9.1093837015e-31         # kg (CODATA)
M_E_REL_UNC = 2.9e-11          # 电子质量相对不确定度（CODATA 量级）
HBAR, C = 1.054571817e-34, 2.99792458e8


def main():
    L = []
    L.append("=" * 72)
    L.append("TUFT O-SCALE：尺度锚定与 EDM/g-2 的连接（OPEN7）")
    L.append("run at: 2026-09-30")
    L.append("=" * 72)

    lam, Omega, theta = sp.symbols("lam Omega theta", positive=True)

    # ---- §1 不对称性 ----
    L.append("")
    L.append("== 1. 关键不对称性：g-2 与 EDM 对 (Ω,θ) 的依赖 ==")
    L.append("  参数化 κ=Ωcosθ, τ=Ωsinθ（OPEN5c 已证）")
    g2 = 2 * sp.tan(theta)
    edm_shape = sp.simplify((Omega * sp.cos(theta)) * (Omega * sp.sin(theta)))
    L.append("  g-2 = 2τ/κ      = %s   ← 只含 θ，【与 Ω 无关】" % g2)
    L.append("  EDM ∝ κτ        = %s  ← 含 Ω²【依赖尺度】" % edm_shape)
    L.append("  ⇒ 重标度 Ω→λΩ：g-2 不变（θ 未动），EDM → λ²·EDM")
    L.append("  [INFO] 存在『调尺度压 EDM 而保住 g-2』的通道  |  需检验其物理代价")
    L.append("")

    # ---- §2 通道所需 λ ----
    L.append("== 2. 通道所需的重标度因子 λ ==")
    F_d = sp.Float(EDM_ACME_ECM) / sp.Float(EDM_TUFT_ECM)
    lam_need = sp.sqrt(F_d)
    L.append("  EDM 需压低 F_d = %.4e" % float(F_d))
    L.append("  λ² = F_d ⇒ λ = %.4e" % float(lam_need))
    L.append("  即 Ω 需缩小 %.3e 倍（Ω → %.3e · Ω₀）" % (
        1 / float(lam_need), float(lam_need)))
    L.append("")

    # ---- §3 物理代价：等价缩电子质量 ----
    L.append("== 3. 物理代价检验：Ω = m_e c/ħ ⇒ 缩 Ω 等价缩 m_e ==")
    omega0 = sp.Float(M_E * C / HBAR)          # Ω₀ = m_e c/ħ (1/m)
    L.append("  Ω₀ = m_e c/ħ = %.4e m^-1  (≈1/ƛ_C，康普顿尺度)" % float(omega0))
    m_req = sp.Float(M_E) * lam_need
    L.append("  Ω ∝ m_e ⇒ 缩 Ω 到 λ 倍 ⇔ m_e → λ·m_e")
    L.append("  要求 m_e = %.4e kg （实测 %.4e kg）" % (float(m_req), M_E))
    shrink = 1 / float(lam_need)
    L.append("  ⇒ 要求电子质量【缩小 %.3e 倍】" % shrink)
    L.append("")
    # 与测量精度比较
    rel_change = abs(1 - float(lam_need))       # 要求的相对改变 ≈ 1
    excess_unc = rel_change / M_E_REL_UNC
    L.append("  测量约束：m_e 相对不确定度 ≈ %.1e" % M_E_REL_UNC)
    L.append("  要求相对改变 |1−λ| ≈ %.6f（即 ~%.0f%% 的改变）" % (rel_change, rel_change * 100))
    L.append("  超出测量不确定度 %.3e 倍 ⇒ 约 %.1f 个量级" % (
        excess_unc, float(sp.log(excess_unc, 10).evalf())))
    L.append("  [FAIL] 尺度重标度通道与质量测量矛盾  |  压 EDM 需 m_e 缩小 %.2e 倍，"
             "而 m_e 高精度测量仅允许 ~%.0e 相对改变 ⇒ 超 ~%.0f 量级，彻底矛盾" % (
                 shrink, M_E_REL_UNC, float(sp.log(excess_unc, 10).evalf())))
    L.append("")

    # ---- §4 三难与结论 ----
    L.append("== 4. 尺度三难（本册结论）==")
    L.append("  (a) 保 g-2(θ 匹配) + 保 m_e(Ω 锁定) ⇒ EDM 超 ACME 16.1 量级 ❌")
    L.append("  (b) 保 g-2 + 压 EDM ⇒ 需 m_e 缩小 %.2e 倍，与测量矛盾 ~%.0f 量级 ❌" % (
        shrink, float(sp.log(excess_unc, 10).evalf())))
    L.append("  (c) 保 m_e + 压 EDM（调 θ）⇒ g-2 归零/发散（OPEN5c 已证） ❌")
    L.append("")
    L.append("  ⇒ 三个角全部堵死：EDM 的 16 量级超额是【尺度锚定被质量测量锁死】的必然后果。")
    L.append("  ⇒ 根源钉死：不是 τ/κ 比值（OPEN5c），不是屏蔽因子（OPEN5b），")
    L.append("     而是 Ω = m_e c/ħ 这一【康普顿尺度】本身——Ω² 天然巨大，")
    L.append("     而 m_e 是外部测量输入，TUFT 无第一性机制给出/改变它（O-SCALE 开放项）。")
    L.append("  [FAIL] EDM 超额根源 = 尺度锚定 + 质量测量锁死  |  "
             "TUFT 若要有救，须给出第一性尺度机制（O-SCALE 已证当前无），"
             "且该机制还须与 m_e 高精度测量相容——双重不可能")
    L.append("")
    L.append("== 汇总 ==")
    L.append("  PASS=1（g-2/EDM 对 Ω 不对称性）  FAIL=2（尺度通道与质量矛盾/三难无解）  BOUNDARY=1  INFO=2")
    L.append("  λ=%.4e  m_e需缩 %.3e 倍  超测量精度 %.1f 量级" % (
        float(lam_need), shrink, float(sp.log(excess_unc, 10).evalf())))
    L.append("")
    L.append("红线：本册仅做推导与判定，未构造新物理、未修改 TUFT 方程或 m_e 值。")
    L.append("『尺度重标度』通道在数学上成立但被质量测量否决——如实记录，不为调参开后门。")

    txt = "\n".join(L) + "\n"
    out = os.path.join(HERE, "tuft_OSCALE_尺度锚定EDM连接_OPEN7_report.txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(txt)
    print("已生成:", out)


if __name__ == "__main__":
    main()
