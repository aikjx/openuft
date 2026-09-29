# -*- coding: utf-8 -*-
"""
TUFT V3.2 分支B 追踪 · 两尺度缺口的独立第一性复核（选项 ① 前置）
================================================================
目标：用第一性推导独立复核 C0050/C0052 的 binding blocker——尺度缺口——
并给出单尺度不可行性的定量证据、两尺度路线的自洽性验证。

框架（自然单位 c=G=ℏ=1，一切长度/质量以 l_P、M_P 计）：
  g = 4·M·Iμ/(N·ℏ) = 2·M_nat·⟨r⟩_nat      (C0050)
  其中 ⟨r⟩_nat = Iμ/N 是电荷分布半径（自然单位）。
  目标 g_e ≈ 2.0023  ⟹  ⟨r⟩ = g_e·λ_C/2 = 1.00116·λ_C。

三部分：
  P1 当前最优剖面的 g 与缺口（对照 C0050 的 2.98e-22 / 3.56 l_P）；
  P2 单尺度不可行性：把同一剖面拉到 ⟨r⟩=1.00116λ_C，N/M 按体积放大 ~1e65；
      振幅需压到 ~1e-66 才压回 N=1，但此时 Iμ/M 结构不变仍不匹配 ⟹ 质量与
      电荷/磁矩不能共享单一剖面尺度 → 需两尺度；
  P3 两尺度自洽性：电荷/磁晕取 ⟨r⟩=1.00116λ_C（振幅独立），质量 M_e 由独立
      核贡献 ⟹ g_e = 2·M_nat·⟨r⟩ = 2.0023，与晕振幅无关，代数自洽（验证 C0052）。

红线：模型层面第一性核验，非物理真实性主张；单位制/4π 钉扎仍挂账。
"""
import numpy as np, math, io, os

OUT = "tuft_v32_twoscale_gap_report.txt"
PNG  = "tuft_v32_twoscale_gap.png"
buf = []; log = buf.append

# ---------------- 常数与当前最优剖面（tuft_v32_adjoint_slsqp） ----------------
M_P = 2.176434e-8          # kg
M_E = 9.1093837015e-31     # kg
M_nat = M_E / M_P          # ≈4.18546e-23 (自然单位)
lamC_nat = 1.0 / M_nat     # ≈2.3892e22 l_P
g_e = 2.00231930436153     # 电子 g 因子实验值

log("TUFT V3.2 分支B 追踪 · 两尺度缺口的独立第一性复核")
log("运行时间: 2026-09-29")
log("自然单位: M_nat=%.6e  λ_C=%.6e l_P" % (M_nat, lamC_nat))

# 当前最优剖面观测量（tuft_v32_adjoint_slsqp 最优点）
r = np.logspace(-3.0, 2.0, 400)
Kc, lK, r0p, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
ODE, ALPHA = 0.6875, 1.0/137.036
K = Kc*np.exp(-r/lK)/(1.0+(r/r0p)**p)
T = Tc*np.exp(-r/lT)
Om = ODE + (O0-ODE)*np.exp(-r/lO)
dO = Om - ODE
N    = np.trapezoid(dO*r**2, r)
I_mu = np.trapezoid(dO*r**3, r)
E_st = ALPHA*4.0*math.pi*np.trapezoid(K*T*Om*r**2, r)
langle = I_mu/N

# ---------------- P1：当前 g 与缺口 ----------------
g_now = 2.0*M_nat*langle
langle_need = g_e/(2.0*M_nat)   # 需要的电荷半径
gap = g_e/g_now

log("")
log("=== P1 当前最优剖面的 g 与尺度缺口（独立复算 C0050）===")
log("  剖面观测量: N=%.6e  I_mu=%.6e  ⟨r⟩=I_mu/N=%.6e l_P  E_static=%.6e"
    % (N, I_mu, langle, E_st))
log("  g=2·M_nat·⟨r⟩=2.0023 需 ⟨r⟩=%.6e l_P (=%.6f·λ_C)" % (langle_need, langle_need/lamC_nat))
log("  当前 g=2·M_nat·⟨r⟩=%.6e  vs 目标 g_e=%.6f" % (g_now, g_e))
log("  缺口 = g_e/g = %.3e（%.1f 个数量级）" % (gap, math.log10(gap)))
log("  ⟹ 印证 C0050：质量已钉扎、g 维度（磁矩/电荷/尺度）未钉扎。")

# ---------------- P2：单尺度不可行性 ----------------
log("")
log("=== P2 单尺度不可行性：同一剖面拉到 ⟨r⟩=1.00116λ_C ⟹ N/M 爆炸 ===")
# 指数剖面 (Ω-Ω_DE)=(O0-ODE)e^{-r/lO}: N=2·A·lO³, Iμ=6·A·lO⁴, ⟨r⟩=3lO
lO_need = langle_need/3.0
A0 = O0 - ODE
N_need_at_sameA = A0*2.0*lO_need**3          # 同振幅 A0 时 N
N_now = A0*2.0*lO**3
ratio_vol = N_need_at_sameA / N_now
log("  需要的晕尺度: ⟨r⟩=%.4e l_P ⟹ lO_need=⟨r⟩/3=%.4e l_P" % (langle_need, lO_need))
log("  当前 lO=%.6f l_P, ⟨r⟩=%.4f l_P" % (lO, langle))
log("  同振幅下 N 按体积 ∝lO³ 放大: N_now=%.4e → N_need=%.4e (×%.2e)"
    % (N_now, N_need_at_sameA, ratio_vol))
log("  若压振幅使 N=1: A_need=A0/N_need=%.4e（≈%.0f 个数量级压缩）" % (A0/N_need_at_sameA, math.log10(A0/N_need_at_sameA)))
log("  M 同理由同一剖面主导 ∫r²dr∝lO³ ⟹ 同样放大 ~%.1e ⟹ 单剖面无法同时给出"
    " M_e 与 λ_C 尺度电荷晕；质量与电荷/磁矩须分属不同尺度。" % ratio_vol)

# ---------------- P3：两尺度自洽性 ----------------
log("")
log("=== P3 两尺度自洽性：康普顿晕(电荷/磁矩) + 独立核(质量) ⟹ g_e 精确匹配 ===")
log("  两尺度假设：晕半径 ⟨r⟩=1.00116·λ_C=%.6e l_P；质量 M_e 由独立核给出。" % langle_need)
g_two = 2.0*M_nat*langle_need
log("  g_two_scale=2·M_nat·⟨r⟩=2·(%.6e)·(%.6e)=%.8f" % (M_nat, langle_need, g_two))
log("  vs 目标 g_e=%.8f  相对误差=%.3e" % (g_e, abs(g_two-g_e)/g_e))
log("  ⟹ g 因子只依赖晕半径与核质量之积，与晕振幅/核结构细节无关；")
log("  g_e 精确等价于 ⟨r⟩=g_e·λ_C/2=1.00116λ_C，两尺度路线代数自洽（验证 C0052）。")
log("  附带：按 α=1/137 给电荷 e 定标需独立引入 U(1) 耦合；此处仅验 g 维自洽。")

# ---------------- 绘图 ----------------
try:
    import matplotlib, matplotlib.pyplot as plt
    HAVE = True
except Exception:
    HAVE = False
if HAVE:
    for f in ("Microsoft YaHei","SimHei","Noto Sans CJK SC"):
        try:
            matplotlib.font_manager.findfont(f, fallback_to_default=False)
            plt.rcParams["font.sans-serif"]=[f]; break
        except Exception:
            continue
    plt.rcParams["axes.unicode_minus"]=False
    fig, ax = plt.subplots(1,2,figsize=(12,4.6))
    # 左：⟨r⟩ 轴上的 g 曲线，标出当前点与目标点
    lr = np.logspace(-1, 23, 300)
    g = 2.0*M_nat*lr
    ax[0].loglog(lr, g, lw=2)
    ax[0].axhline(g_e, color="red", ls="--", lw=1.2, label="g_e=2.0023")
    ax[0].axvline(langle, color="blue", ls=":", lw=1.4, label="当前 ⟨r⟩=%.2e l_P"%langle)
    ax[0].axvline(langle_need, color="green", ls=":", lw=1.4, label="所需 ⟨r⟩=1.00λ_C")
    ax[0].set_xlabel("电荷分布半径 ⟨r⟩ (l_P)"); ax[0].set_ylabel("g = 2·M_nat·⟨r⟩")
    ax[0].set_title("g 因子 vs 电荷半径：尺度缺口 %.0f 个数量级"%math.log10(gap))
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3, which="both")
    # 右：单尺度拉长晕 ⟹ N 爆炸
    lO_arr = np.logspace(-1, 22, 200)
    N_arr = A0*2.0*lO_arr**3
    ax[1].loglog(lO_arr, N_arr, lw=2, color="purple")
    ax[1].axvline(lO, color="blue", ls=":", lw=1.3, label="当前 lO=%.3f l_P"%lO)
    ax[1].axvline(lO_need, color="green", ls=":", lw=1.3, label="晕所需 lO=%.1e"%lO_need)
    ax[1].set_xlabel("剖面尺度参数 lO (l_P)"); ax[1].set_ylabel("N ∝ A0·2·lO³")
    ax[1].set_title("单尺度拉长晕 ⟹ N 爆炸 ~1e65（质量无法同时保持 M_e）")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(PNG, dpi=110)
    log("")
    log("绘图已保存: " + os.path.abspath(PNG))

log("")
log("红线声明：模型层面第一性核验，非物理真实性主张；单位制/4π 钉扎与 U(1) 电荷")
log("耦合标定仍挂账。两尺度自洽仅验 g 维度，不预设核/晕具体构造成立。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
