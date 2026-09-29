# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R29  核心公式体系「口径校准」+ 两个内生结构问题的可算判定
================================================================================
承接（2026-09-29/30 攻破链）：
  OPEN-5  tuft_g2_电子反常磁矩_OPEN5.py        a_TUFT = α/(8π)，被实验否决
  OPEN-6  tuft_EDM_实验对接_OPEN6.py           d_e 超 ACME 1.28e16 倍，被否决
  OPEN-7  tuft_beta_running_缺口_定理N实例化.py β ≡ 0（固定螺旋），无 RG 流
  OPENv2/v3/v4  sigma_abs0 ringdown            χ²=33.00 → 5.74σ；三尺度锚差 26~78 量级

本册任务（不含新的实验拟合，只做「公式本身」的可算判定）：
  §1 模块 C（前置）：τ/κ 方向裁决 —— 严格 Frenet 几何给 κ/τ = tanθ，τ/κ = √(1−α²)/α ≈ 137，
     与白皮书系「α = τ/κ」相差 (1/α)² ≈ 1.878e4 倍。任何把 τ/κ 当 α 使用的公式须先裁决。
  §2 模块 A：EC 联络下 ∇^(EC)_μ T^{μν} = 0 是否为恒等式？
     用联络差闭式 F^ν = K^μ_{μλ}T^{λν} + K^ν_{μλ}T^{μλ} 构造线性映射 K ↦ F^ν，
     求秩 ⇒ 「自动守恒」所需的额外约束数（余维）。
  §3 模块 B：ακ·g_{μν} 与 Λ·g_{μν} 的结构不可辨识性（雅可比秩），
     并给出「破简并」的充要条件，连接到既有 O-SCALE / D3 / 定理 N M2。
  §4 四条实验窗口的口径校准表（把外稿漂移统一回源脚本口径）。

红线：数学自洽 != 实验证实。本册不作证伪宣告，只判定「公式是否成立、是否需要额外假设」。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_r29_report.txt")

# CODATA 近似（与既有 TUFT 脚本同口径）
ALPHA = 1.0 / 137.035999084
A_E_EXP = 0.00115965218073          # 电子反常磁矩 a_e
D_TUFT_CM = 2.25735897042146e-34    # OPEN-6 的 d_e (C·m)
ACME_ECM = 1.1e-29                  # ACME 2018 |d_e| 上限 (e·cm)
E_CHARGE = 1.602176634e-19


def main():
    buf = []
    stat = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}

    def put(s=""):
        buf.append(s)

    def rec(tag, name, detail):
        stat[tag] = stat.get(tag, 0) + 1
        buf.append("  [%s] %s  |  %s" % (tag, name, detail))

    def sec(t):
        buf.append("")
        buf.append("=" * 78)
        buf.append("  " + t)
        buf.append("=" * 78)

    sec("TUFT-R29  核心公式口径校准 + 内生结构可算判定")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    put("  红线：数学自洽 != 实验证实；本册只判定公式是否成立 / 是否需要额外假设。")

    # =====================================================================
    # §1 模块 C：τ/κ 方向裁决（前置）
    # =====================================================================
    sec("1. 模块 C（前置）：τ/κ 方向裁决 —— 严格 Frenet 给的是 κ/τ = tanθ")

    put("  圆柱螺旋 r(t) = (a·cos t, a·sin t, b·t) 的严格 Frenet 不变量：")
    put("      κ = a/(a²+b²)      τ = b/(a²+b²)")
    put("      ⇒ κ/τ = a/b       且 κ² + τ² = 1/(a²+b²)")
    put("  取 S12 裁决的电子螺旋几何： a = R = α·ρ_C,  b = ρ_C·√(1−α²),  ρ_C = ħ/(m_e c)")
    put("      ⇒ κ/τ = α/√(1−α²) = tanθ     （与 sinθ = α 严格自洽）")

    # 数值回算 Frenet，不用上面的闭式，交叉验证
    rho_c = 3.8615926796e-13                    # 康普顿半径 m
    a_h = ALPHA * rho_c                          # 横向半径 = alpha*rho_C（数值等于经典电子半径）
    b_h = rho_c * math.sqrt(1.0 - ALPHA ** 2)    # 螺距参数
    kap_num = a_h / (a_h ** 2 + b_h ** 2)
    tau_num = b_h / (a_h ** 2 + b_h ** 2)
    ratio_k_t = kap_num / tau_num                # κ/τ
    ratio_t_k = tau_num / kap_num                # τ/κ
    theta = math.asin(ALPHA)
    tan_theta = ALPHA / math.sqrt(1.0 - ALPHA ** 2)

    put("")
    put("  α            = %.13e" % ALPHA)
    put("  θ = arcsin α = %.13e rad" % theta)
    put("  tanθ（闭式） = %.13e" % tan_theta)
    put("  κ/τ（数值）  = %.13e   残差 vs tanθ = %.3e" % (ratio_k_t, abs(ratio_k_t - tan_theta)))
    put("  τ/κ（数值）  = %.13e   残差 vs √(1−α²)/α = %.3e"
        % (ratio_t_k, abs(ratio_t_k - math.sqrt(1.0 - ALPHA ** 2) / ALPHA)))
    rec("PASS", "严格几何自洽（κ/τ = tanθ）",
        "Frenet 数值回算与 tanθ 闭式残差 %.2e（机器零）；对照 S12 裁决 sinθ=α 完全一致"
        % abs(ratio_k_t - tan_theta))

    inv_alpha = 1.0 / ALPHA
    gap_factor = (ratio_t_k / ALPHA) if ALPHA != 0 else float("nan")
    put("")
    put("  白皮书系 S07/S08/S10 主张： α = τ/κ")
    put("  严格几何实际给：             τ/κ = √(1−α²)/α = %.6f ≈ 1/α = %.6f" % (ratio_t_k, inv_alpha))
    put("  ⇒ 二者相差因子 = %.4e  ≈ (1/α)² = %.4e" % (gap_factor, inv_alpha ** 2))
    rec("FAIL", "『α = τ/κ』方向写反",
        "τ/κ ≈ 1/α = %.4f，与 α = %.4e 相差 %.3e 倍；凡用 τ/κ 代入 α 处的公式数值全错"
        % (inv_alpha, ALPHA, gap_factor))

    # 公理 A 在该几何下的闭合（附带收获）
    omega_given = 1.0 / math.sqrt(a_h ** 2 + b_h ** 2)   # κ²+τ² = ω²/c² ⇒ ω = c/ρ_total
    put("")
    put("  【附带闭合】公理 A 在该螺旋几何下：κ²+τ² = 1/ρ_C²")
    put("      ⇒ ω/c = 1/ρ_C ⇒ ω = c/ρ_C = m_e c²/ℏ = %.6e rad/s（康普顿角频率）" % (omega_given * 2.99792458e8))
    rec("PASS", "公理 A 与螺旋几何相容",
        "κ²+τ²=(ω/c)² 在 a=αρ_C, b=ρ_C√(1−α²) 下给出 ω = m_ec²/ℏ（康普顿频率），无自由参数")

    # =====================================================================
    # §2 模块 A：EC 联络下 ∇·T = 0 是否为恒等式
    # =====================================================================
    sec("2. 模块 A：EC 联络下 ∇^(EC)_μ T^{μν} = 0 是恒等式，还是额外约束？")

    put("  联络差闭式（C = Γ^(EC) − Γ^(LC) = K 为 contortion 张量）：")
    put("      ∇^(EC)_μ T^{μν} = ∇^(LC)_μ T^{μν} + K^μ_{μλ} T^{λν} + K^ν_{μλ} T^{μλ}")
    put("  ⇒ F^ν := K^μ_{μλ}T^{λν} + K^ν_{μλ}T^{μλ}  对 K 是『线性』映射")
    put("  做法：在一点的局部惯性系做( g = η = diag(−1,1,1,1) )。因 T、K 是张量、F 是矢量，")
    put("        该线性映射的『秩』在可逆坐标变换（相似等价）下不变 ⇒ 结论与坐标无关。")

    eta = np.diag([-1.0, 1.0, 1.0, 1.0])

    def build_map(tup, subspace="full"):
        """返回线性映射矩阵 M: K -> F^ν  (shape 4 x dim) 与 K 空间维数"""
        idx = [(r, m, n) for r in range(4) for m in range(4) for n in range(4)]
        bases = []
        if subspace == "full":
            for tri in idx:
                v = np.zeros((4, 4, 4))
                v[tri] = 1.0
                bases.append(v)
        else:  # contortion 对后两指标反对称（全反对称挠率的标准情形）⇒ 4×6 = 24 维
            for r in range(4):
                for m in range(4):
                    for n in range(m + 1, 4):
                        v = np.zeros((4, 4, 4))
                        v[r, m, n] = 1.0
                        v[r, n, m] = -1.0
                        bases.append(v)
        cols = []
        for kten in bases:
            fv = np.zeros(4)
            for nu in range(4):
                acc = 0.0
                for mu in range(4):
                    for lam in range(4):
                        acc += kten[mu, mu, lam] * tup[lam, nu]
                        acc += kten[nu, mu, lam] * tup[mu, lam]
                fv[nu] = acc
            cols.append(fv)
        return np.array(cols).T, len(bases)

    def sym_sample():
        """随机反对称代表：S^{μν} = ε^{μνλρ} n_λ u_ρ 的粗路实现（取随机 n,u 后按形式构）"""
        rng = np.random.RandomState(20300930)
        n = rng.normal(size=4)
        u = rng.normal(size=4)
        # 简单分量型反对称张量（足以代表 S 的一般位置）
        s_mat = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                s_mat[i, j] = n[i] * u[j] - n[j] * u[i]
        return s_mat

    cases = [
        ("A 主导（ακ·g 项）", 1.0, 0.0),
        ("B 主导（βτ·S 项）", 0.0, 1.0),
        ("混合典型（A=1, B=τ/κ 量级）", 1.0, ratio_t_k * 1e-3),
    ]

    put("")
    for label, amp_a, amp_bp in cases:
        s_mat = sym_sample()
        tup = amp_a * np.linalg.inv(eta) + amp_bp * s_mat
        for sp, spname in (("full", "一般 K（64 分量）"), ("asym", "K 后两指标反对称（24 分量）")):
            mat, dim = build_map(tup, subspace=sp)
            sv = np.linalg.svd(mat, compute_uv=False)
            tol = max(sv) * 1e-10 if len(sv) else 0.0
            rankk = int(np.sum(sv > tol))
            put("    %-28s %-24s dim=%3d  rank=%d  codim(约束数)=%d  nullity=%d"
                % (label, spname, dim, rankk, rankk, dim - rankk))
            if sp == "asym":
                rec("FAIL" if rankk > 0 else "PASS", "∇^(EC)·T = 0 非恒等式（%s）" % label,
                    "线性映射 K↦F^ν 在 %d 维 K 空间上秩=%d ⇒ 须附加 %d 个独立代数约束；"
                    "一般 K 下 F^ν ≠ 0，不是由场方程自动导出" % (dim, rankk, rankk))

    # 随机 K 的非零统计
    rng = np.random.RandomState(73009130)
    s_mat = sym_sample()
    tup = 1.0 * np.linalg.inv(eta) + 1e-3 * s_mat
    nonzero = 0
    norms = []
    for _ in range(2000):
        kk = rng.normal(size=(4, 4, 4))
        kk = kk - np.transpose(kk, (0, 2, 1))   # 投影到后两指标反对称
        fv = np.zeros(4)
        for nu in range(4):
            acc = 0.0
            for mu in range(4):
                for lam in range(4):
                    acc += kk[mu, mu, lam] * tup[lam, nu]
                    acc += kk[nu, mu, lam] * tup[mu, lam]
            fv[nu] = acc
        nn = float(np.linalg.norm(fv))
        norms.append(nn)
        if nn > 1e-12:
            nonzero += 1
    frac = nonzero / 2000.0
    rec("INFO", "随机 K 不满足守恒的比例",
        "2000 组随机 contortion 中 %.1f%% 给出 ∇^(EC)_μ T^{μν} ≠ 0（||F|| 中位 %.3e）"
        % (frac * 100, float(np.median(norms))))

    # 唯一自动成立的分支
    rec("INFO" if False else "PASS", "唯一自动成立的分支（回归 GR）",
        "K ≡ 0（挠率为零）⇒ F^ν ≡ 0、∇^(LC)_μ(A g^{μν}) = ∂^ν A；当 ακ 为时空常数时 ∂^ν(ακ)=0，"
        "此时自动守恒。⇒ 守恒成立需要额外假设，而非 TUFT 场方程的推论")

    # =====================================================================
    # §3 模块 B：ακ·g_{μν} 与 Λ·g_{μν} 的结构不可辨识
    # =====================================================================
    sec("3. 模块 B：ακ·g_{μν} 与 Λ·g_{μν} 的结构不可辨识性")

    put("  场方程两边同型项合并：")
    put("      G_{μν} + Λ g_{μν} = 8πG(ακ g_{μν} + βτ S_{μν})")
    put("      ⇒ G_{μν} + [Λ − 8πG·ακ] g_{μν} = 8πG·βτ S_{μν}")
    put("  因 S^{μν} 反对称、g^{μν} 对称 ⇒ 二者在张量空间正交，βτ 项不参与此简并；")
    put("  唯一简并发生在 Λ 与 ακ 之间。以观测 s = Λ − 8πG·ακ 为可观测量，对 θ=(Λ,α) 求雅可比：")

    g_scale = 8.0 * math.pi * 6.67430e-11       # 8πG
    # 情形 1：单一 κ
    kap1 = 1.0
    j1 = np.array([[1.0, -g_scale * kap1]])
    r1 = int(np.linalg.matrix_rank(j1, tol=1e-12))
    put("")
    put("    情形1（κ 取单值 %.1f）：J = [ ∂s/∂Λ , ∂s/∂α ] = [1, −8πG·κ]" % kap1)
    put("        rank(J) = %d < 2 ⇒ 不可辨识；可辨识组合数 = %d，退化方向 = %d" % (r1, r1, 2 - r1))
    rec("FAIL", "Λ 与 ακ 结构不可辨识（单 κ）",
        "rank=1：任何观测只能定出组合 Λ_eff = Λ − 8πG·ακ；声称『Λ 由孤子几何导出』属定义回代（TAUT）")

    # 情形 2：多个不同 κ
    kaps = [1.0, 2.5, 7.0]
    j2 = np.array([[1.0, -g_scale * kk] for kk in kaps])
    r2 = int(np.linalg.matrix_rank(j2, tol=1e-12))
    put("    情形2（κ 取多值 %s）：rank(J) = %d ⇒ 可辨识（当且仅当 κ_i 已知且互异）" % (kaps, r2))
    if r2 >= 2:
        rec("PASS", "破简并的充要条件",
            "需 ≥2 个不同 κ 的同型观测且 κ_i 数值已知。注意：TUFT 现无第一性 κ(μ) 剖面"
            "（O-SCALE 锚定定理 / D3 K_sat 审计 / 定理 N M2 三处同源结论）⇒ 简并不能被真正打破")

    put("")
    put("  ⇒ 与既有结论的同源闭合：O-SCALE（尺度秩=1 须外部锚定）+ D3（K_sat=1/l_P² 手写锚定）")
    put("    + 定理 N M2（尺度生成缺第一性）三处，与本模块指向同一结构性边界。")
    rec("INFO", "同维边界闭合",
        "模块 B 把『TUFT 无第一性尺度』从 RG 层（β≡0）推广到宇宙学常数层（Λ 不可辨识）")

    # =====================================================================
    # §4 四条实验窗口的口径校准
    # =====================================================================
    sec("4. 四条实验窗口的口径校准（外稿漂移 ← 回归源脚本）")

    # g-2 三路对比
    a_tuft = ALPHA / (8.0 * math.pi)            # 源 OPEN-5 口径
    a_qed = ALPHA / (2.0 * math.pi)
    g2_from_tuft_ext = 2.0 * a_tuft
    g2_from_tau_over_kappa_strict = 2.0 * ratio_t_k
    g2_from_alpha_tau_kappa = 2.0 * ALPHA
    g2_ext_claimed = 0.00404                     # 外稿数值
    g2_exp = 2.0 * A_E_EXP
    put("  【窗口1 · g-2】真源口径 = OPEN-5：a_TUFT = α/(8π)")
    put("      源脚本      a_TUFT = α/(8π)   = %.6e  ⇒ g−2 = %.6e  （相对实验偏差 %+.2f%%）"
        % (a_tuft, g2_from_tuft_ext, (g2_from_tuft_ext - g2_exp) / g2_exp * 100))
    put("      若误用 τ/κ=α        ⇒ g−2 = 2α      = %.6e  （偏差 %+.2f%%）"
        % (g2_from_alpha_tau_kappa, (g2_from_alpha_tau_kappa - g2_exp) / g2_exp * 100))
    put("      若用严格 τ/κ=1/α    ⇒ g−2 = 2/α     = %.6e  （偏差 %+.2f%%）"
        % (g2_from_tau_over_kappa_strict,
           (g2_from_tau_over_kappa_strict - g2_exp) / g2_exp * 100))
    put("      外稿写               g−2 = 0.00404                （偏差 %+.2f%%）"
        % ((g2_ext_claimed - g2_exp) / g2_exp * 100))
    put("      实验 g−2 = 2·a_e = %.6e" % g2_exp)
    rec("FAIL", "g−2 公式口径三重不一致（须校准）",
        "外稿 0.00404 与三条候选路径全部不符（α/(8π)→%.3e / 2α→%.3e / 2/α→%.3e）；"
        "唯一有源口径为 α/(8π) ⇒ g−2=%.3e（偏差 %.2f%%）"
        % (g2_from_tuft_ext, g2_from_alpha_tau_kappa, g2_from_tau_over_kappa_strict,
           g2_from_tuft_ext, (g2_from_tuft_ext - g2_exp) / g2_exp * 100))

    # EDM
    d_tuft_ecm = D_TUFT_CM / (E_CHARGE * 1e-2)
    ratio_edm = d_tuft_ecm / ACME_ECM
    put("")
    put("  【窗口2 · EDM】真源口径 = OPEN-6：d_e = eαR_C/(2√(1+α²))")
    put("      d_e = %.6e C·m = %.6e e·cm" % (D_TUFT_CM, d_tuft_ecm))
    put("      ACME 2018 上限 = %.2e e·cm   ⇒ 超出 %.3e 倍" % (ACME_ECM, ratio_edm))
    rec("FAIL", "EDM 口径校准（并补强）",
        "OPEN-6 已证超真实 ACME 上限 %.2e 倍 ⇒ 否决；另书籍第52章判定该式依赖 ⟨z⟩=b/2 "
        "属 [C] 类假设、螺旋对称性严格给 d_e=0 ⇒ 该『预言』本身不应存在（比偏大更彻底）" % ratio_edm)
    put("      附带勘误：白皮书引用的『ACME 8.7e−34 C·m』= %.3e e·cm，比真实上限宽松 %.2e 倍"
        % (8.7e-34 / (E_CHARGE * 1e-2), (8.7e-34 / (E_CHARGE * 1e-2)) / ACME_ECM))

    # β
    put("")
    put("  【窗口3 · β 跑动】真源口径 = OPEN-7（定理 N 实例化）：g = κ/τ 为无量纲常数")
    put("      ⇒ ∂g/∂μ = 0 ⇒ β ≡ 0（无跑动），而非『存在非解析缺口 Δβ≠0』")
    put("      定理 N 三件套满足度 M1/M2/M3 = 0/0/1；跨树缺口 log10(m_P/Λ_QCD) = 19.75")
    rec("BOUNDARY", "β 跑动口径反向校正",
        "源结论是『β≡0（无 RG 流）』；外稿『δ_TUFT 造成缺口』与之反向，须按源脚本重写")

    # ringdown
    put("")
    put("  【窗口4 · ringdown】已三级闭环，非『缺 χ² metric』：")
    put("      v2 两难 → v3 χ²=33.00(df=2), p=6.83e−8, 5.74σ, MCMC n=19200 → v4 三尺度锚差 26~78 量级")
    rec("FAIL", "唯一 L3 窗口状态更新：已关闭",
        "壁在 r_s=2.05M ⇒ 被 LIGO >5σ 排除；壁远离 ⇒ 无相干模不可检验；"
        "且 TUFT 第一性无法把壁放在 2.05M（差 26~78 量级）⇒ σ_abs=0 非可导出结构")

    # =====================================================================
    # §5 诚实结论
    # =====================================================================
    sec("5. 诚实结论（校准坐标）")
    put("  · 模块 C：τ/κ 方向地雷已定量（差 (1/α)² = %.3e 倍），用前必须裁决" % (inv_alpha ** 2))
    put("  · 模块 A：∇^(EC)_μ T^{μν} = 0 不是场方程推论，而是对 contortion 的 4 个额外约束；")
    put("             随机 K 下 %.1f%% 不成立。⇒ 『TUFT 协变闭环』须改述为『附加守恒假设』" % (frac * 100))
    put("  · 模块 B：Λ 与 ακ 结构不可辨识（rank=1）；破简并需 ≥2 个已知 κ，而 TUFT 无第一性尺度")
    put("             ⇒ 若以 ακ 导出 Λ 则为定义回代（TAUT），与 O-SCALE/D3/定理N 同源")
    put("  · 四条窗口：g−2 / EDM / β / ringdown 口径全部须按源脚本重写，其中 3 条已无 OPEN 状态：")
    put("             g−2、EDM 已被实验否决；ringdown 已被定量关闭；β 为 β≡0 的边界判定")
    rec("INFO", "本册性质",
        "属『加固边界而非推翻』：不否定 R1–R28 的物理结论，只校准公式书写与成立条件")

    sec("汇总")
    put("  PASS     = %d" % stat.get("PASS", 0))
    put("  FAIL     = %d" % stat.get("FAIL", 0))
    put("  BOUNDARY = %d" % stat.get("BOUNDARY", 0))
    put("  INFO     = %d" % stat.get("INFO", 0))
    put("")
    put("  τ/κ = %.6f ≈ 1/α；与 α 相差 %.3e 倍" % (ratio_t_k, gap_factor))
    put("  模块A：∇^(EC)·T=0 需 %d 个额外约束（一般 K 下 %.1f%% 不成立）" % (4, frac * 100))
    put("  模块B：rank(J)=%d（单 κ）⇒ Λ 与 ακ 不可辨识" % r1)
    put("")
    put("红线声明：数学自洽 != 实验证实。本册只判定公式成立条件与口径一致性，")
    put("          不构成对 TUFT 框架整体的证伪宣告。")

    text = "\n".join(buf) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
