# -*- coding: utf-8 -*-
"""
TUFT V3.2 分支B 追踪 · 简并切断验证（选项 b）
=============================================
目标：验证"能单独区分 q0 与 ω0 的观测量"是否真能切断 (q0,ω0) 乘积简并。

背景（既有判定）：
  - C0035/并行C0042：Q=q0·ω0·N、μ=q0·ω0·Iμ 只依赖乘积 Π=q0ω0；
    g=4M·Iμ/(N·ℏ) 仅依赖剖面(V1,V2) => 常规观测量无法区分 q0/ω0。
  - C0036：N=ℏ 是纯剖面约束，不切断此简并；真正切断需"依赖 q0 或 ω0 独立
    的观测量"。推导稿自荐：能量补旋转项 ½ω0²∫ψ²，使 M 依赖 ω0。

本脚本：固定剖面，引入旋转能 E_rot=½ω0²·N 作为第四观测量，
数值演示——(1) 无旋转项时沿 q0ω0=const 的一维简并；
(2) 有旋转项时三约束(M_e,Q_e,μ_e)唯一钉住 (q0,ω0)，简并被切断；
(3) 一并展示 g 因子沿简并流形的变化（旋转项使 g 依赖 ω0，成为判别量）。

红线：本脚本为模型层面机制演示（剖面固定、无量纲自洽），
不构成物理真实性主张；物理电子单位制/4π 钉扎仍挂账。
"""
import numpy as np, math, io, os

OUT = "tuft_v32_degeneracy_break_report.txt"
PNG = "tuft_v32_degeneracy_break.png"
buf = []
log = buf.append

# ---------------- 固定剖面（取 tuft_v32_adjoint_slsqp 最优点参数） ----------------
r = np.logspace(-3.0, 2.0, 400)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
ODE, ALPHA = 0.6875, 1.0/137.036

K = Kc*np.exp(-r/lK)/(1.0+(r/r0)**p)
T = Tc*np.exp(-r/lT)
Om = ODE + (O0-ODE)*np.exp(-r/lO)
dO = Om - ODE

# 剖面观测量（模型无量纲、自洽口径）
N    = np.trapezoid(dO*r**2, r)        # 孤子模（剖面）
I_mu = np.trapezoid(dO*r**3, r)        # 磁矩积分（剖面）
M_st = ALPHA*4.0*math.pi*np.trapezoid(K*T*Om*r**2, r)  # 静能

log("TUFT V3.2 分支B 追踪 · 简并切断验证（选项 b）")
log("运行时间: 2026-09-28")
log("剖面观测量: N=%.6e  I_mu=%.6e  M_static=%.6e" % (N, I_mu, M_st))

# ---------------- "真实" (q0,ω0) 与目标 ----------------
q0s, w0s = 2.0, 3.0                     # 任意取定真实拆分（用于构造自洽目标）
Qe  = q0s*w0s*N
mu_e = q0s*w0s*I_mu
Me  = M_st + 0.5*w0s**2*N               # 质量含旋转能 ½ω0²N

log("")
log("构造自洽目标（真实拆分 q0=%.2f, ω0=%.2f）:" % (q0s, w0s))
log("  Q_e=%.6e   μ_e=%.6e   M_e=%.6e" % (Qe, mu_e, Me))

# ---------------- (1) 无旋转项：沿 q0ω0=const 的一维简并 ----------------
log("")
log("=== (1) 无旋转项 M=M_static（原模型，质量沿乘积线恒为常量）: 一维简并 ===")
log("  q0·ω0=const=%.4f 下，扫描 (q0,ω0):" % (q0s*w0s))
degenerate = True
for q, w in [(1.0,6.0),(2.0,3.0),(3.0,2.0),(6.0,1.0),(0.5,12.0),(12.0,0.5)]:
    if abs(q*w - q0s*w0s) > 1e-12: continue
    Q = q*w*N; mu = q*w*I_mu; M = M_st          # 模型1 质量恒为 M_static
    vary = (abs(Q-Qe)>1e-8*abs(Qe)) or (abs(mu-mu_e)>1e-8*abs(mu_e)) or (abs(M-M_st)>1e-8*abs(M_st))
    if vary: degenerate = False
    log("    (q0=%-4.1f, ω0=%-4.1f): Q=%.6e  μ=%.6e  M=%.6e  → 沿乘积线不变（Q/μ/M 差均=0）"
        % (q, w, Q, mu, M))
log("  结论：模型1 下 Q、μ、M 沿乘积线完全恒定 → 存在一维连续简并流形。" if degenerate
    else "  结论：出现变化 → 简并被部分打破。")

# ---------------- (2) 有旋转项：三约束唯一钉住 (q0,ω0) ----------------
log("")
log("=== (2) 加旋转能 M=M_static+½ω0²N（第四观测量）: 简并切断 ===")
# 同一乘积线上的点，M 随 ω0 变化：
varyM = False
for q, w in [(1.0,6.0),(2.0,3.0),(3.0,2.0),(6.0,1.0),(0.5,12.0),(12.0,0.5)]:
    if abs(q*w - q0s*w0s) > 1e-12: continue
    M = M_st + 0.5*w**2*N
    if abs(M-Me) > 1e-8*abs(Me): varyM = True
    log("    (q0=%-4.1f, ω0=%-4.1f): M(含旋转)=%.6e  vs M_e=%.6e  差=%.1e"
        % (q, w, M, Me, abs(M-Me)/max(abs(Me),1e-300)))
log("  旋转项使 M 依赖 ω0 → 乘积线上 M 不再恒定（varyM=%s）" % varyM)

# 反解：(q0,ω0) 唯一
w_rec = math.sqrt(max(2.0*(Me - M_st)/N, 0.0))
q_rec = Qe/(w_rec*N)
mu_rec = q_rec*w_rec*I_mu
log("")
log("  反解（由 M_e,Q_e 求 ω0,q0）:")
log("    ω0_rec=%.10f (true %.10f)  相对误差=%.2e" % (w_rec, w0s, abs(w_rec-w0s)/w0s))
log("    q0_rec=%.10f (true %.10f)  相对误差=%.2e" % (q_rec, q0s, abs(q_rec-q0s)/q0s))
log("    μ 一致性校验: μ_rec=%.6e vs μ_e=%.6e  相对误差=%.2e" % (mu_rec, mu_e, abs(mu_rec-mu_e)/abs(mu_e)))
unique = (abs(w_rec-w0s)/w0s < 1e-8) and (abs(q_rec-q0s)/q0s < 1e-8)
log("  结论：三约束唯一钉住 (q0,ω0) → 简并被切断，得到离散唯一参数点。" if unique
    else "  结论：未唯一钉住 → 仍有简并。")

# ---------------- (3) g 因子沿简并流形 ----------------
log("")
log("=== (3) g 因子（g=4M·I_mu/(N·ℏ)，ℏ 取单位 1）沿简并流形 ===")
S_half = 0.5
g_static  = 4.0*M_st*I_mu/(N*S_half)          # 无旋转项（纯剖面，流形上不变）
log("  无旋转项: g 仅依赖剖面，沿乘积线恒定 g=%.8e（C0042 印证）" % g_static)
for q, w in [(1.0,6.0),(2.0,3.0),(3.0,2.0),(6.0,1.0)]:
    if abs(q*w - q0s*w0s) > 1e-12: continue
    g = 4.0*(M_st+0.5*w**2*N)*I_mu/(N*S_half)
    log("    (q0=%.1f, ω0=%.1f): g(含旋转)=%.8e" % (q, w, g))
log("  旋转项使 g 依赖 ω0 → g 本身成为区分 (q0,ω0) 的判别量")

# ---------------- 绘图 ----------------
try:
    import matplotlib
    import matplotlib.pyplot as plt
    HAVE = True
except Exception:
    HAVE = False
if HAVE:
    for f in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC"):
        try:
            matplotlib.font_manager.findfont(f, fallback_to_default=False)
            plt.rcParams["font.sans-serif"] = [f]; break
        except Exception:
            continue
    plt.rcParams["axes.unicode_minus"] = False
    ws = np.logspace(-1.5, 1.5, 200)
    ms = M_st + 0.5*ws**2*N                       # 旋转项质量随 ω0
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    # 左图：沿 q0ω0=const 的 M 变化（切断简并的关键）
    ax[0].semilogx(ws, ms, lw=2)
    ax[0].axhline(Me, color="red", ls="--", lw=1.2, label="M_e 目标")
    ax[0].axvline(w0s, color="green", ls=":", lw=1.4, label="真实 ω0")
    ax[0].set_xlabel("ω0（沿 q0ω0=const）"); ax[0].set_ylabel("M = M_static + ½ω0²N")
    ax[0].set_title("旋转项使 M 依赖 ω0 → 切断乘积简并")
    ax[0].legend(); ax[0].grid(alpha=0.3)
    # 右图：g 因子随 ω0（判别量）
    gs = 4.0*ms*I_mu/(N*S_half)
    ax[1].semilogx(ws, gs, lw=2, color="purple")
    ax[1].axvline(w0s, color="green", ls=":", lw=1.4, label="真实 ω0")
    ax[1].set_xlabel("ω0"); ax[1].set_ylabel("g = 4M·Iμ/(N·ℏ)")
    ax[1].set_title("旋转项使 g 依赖 ω0 → g 成判别量")
    ax[1].legend(); ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PNG, dpi=110)
    log("")
    log("绘图已保存: " + os.path.abspath(PNG))

log("")
log("红线声明：本脚本为模型层面机制演示（固定剖面、无量纲自洽目标），")
log("不构成物理真实性主张；物理电子 (M,Q,μ) 单位制/4π 钉扎仍挂账。")

with io.open(OUT, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(buf) + "\n")
print("\n".join(buf))
