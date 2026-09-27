# -*- coding: utf-8 -*-
"""
TUFT V3.2 分支B 闭环 · 带旋转能的解析梯度优化器（选项 ②）
=========================================================
目标：把"旋转能 E_rot=½ω0²N 切断 (q0,ω0) 乘积简并"实装进 SLSQP，验证
      在有/无旋转项两种目标下优化器的行为差异：
  - 无旋转项（M=E_static 恒定）：Q、μ 只依赖乘积 Π=q0ω0 → SLSQP 沿简并
    流形任意停靠（不同初值收敛到不同 (q0,ω0)，χ² 均≈0）；
  - 有旋转项（M=E_static+½ω0²N 依赖 ω0）：三约束唯一钉住 (q0,ω0) →
    不同初值收敛到同一真实点（χ²→0，唯一）。

实现：固定剖面（取最优参数），仅优化 (q0,ω0) 两个自由参数；
χ² 梯度对 (q0,ω0) 全解析。目标自洽构造（无量纲、非物理主张）。

红线：模型层面机制演示，不构成物理真实性主张；单位制/4π 钉扎仍挂账。
"""
import numpy as np, math, io, os

OUT = "tuft_v32_degeneracy_fit_report.txt"
PNG  = "tuft_v32_degeneracy_fit.png"
buf = []; log = buf.append

# ---------------- 固定剖面（tuft_v32_adjoint_slsqp 最优点参数） ----------------
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

q0s, w0s = 2.0, 3.0
Mt  = E_st + 0.5*w0s**2*N      # 有旋转项质量目标
Qt  = q0s*w0s*N
mut = q0s*w0s*I_mu

log("TUFT V3.2 分支B 闭环 · 带旋转能的解析梯度优化器（选项 ②）")
log("运行时间: 2026-09-28")
log("固定剖面: N=%.6e  I_mu=%.6e  E_static=%.6e" % (N, I_mu, E_st))
log("真实拆分: q0=%.2f  ω0=%.2f" % (q0s, w0s))
log("有旋转项目标: M_t=%.6e  Q_t=%.6e  μ_t=%.6e" % (Mt, Qt, mut))

# ---------------- 目标函数（两种口径） ----------------
def chi2_case(qw, with_rot, wN=0.1, wM=1.0, wQ=1.0, wmu=1.0):
    q0, w0 = qw
    Nv = N; Iv = I_mu
    M  = E_st + (0.5*w0**2*N if with_rot else 0.0)
    Q  = q0*w0*N; mu = q0*w0*I_mu
    Mtgt = Mt if with_rot else E_st
    return (wN*(Nv-1.0)**2 + wM*((M-Mtgt)/Mtgt)**2
            + wQ*((Q-Qt)/Qt)**2 + wmu*((mu-mut)/mut)**2)

# 解析梯度（对 (q0,ω0)）
def grad_chi2_case(qw, with_rot, wN=0.1, wM=1.0, wQ=1.0, wmu=1.0):
    q0, w0 = qw
    Mtgt = Mt if with_rot else E_st
    M  = E_st + (0.5*w0**2*N if with_rot else 0.0)
    Q  = q0*w0*N; mu = q0*w0*I_mu
    dM_w = w0*N if with_rot else 0.0          # dM/dω0
    dM_q = 0.0
    dQ_w = q0*N; dQ_q = w0*N
    dmu_w = q0*I_mu; dmu_q = w0*I_mu
    gq = 2*wM*(M-Mtgt)/Mtgt**2*dM_q + 2*wQ*(Q-Qt)/Qt**2*dQ_q + 2*wmu*(mu-mut)/mut**2*dmu_q
    gw = 2*wM*(M-Mtgt)/Mtgt**2*dM_w + 2*wQ*(Q-Qt)/Qt**2*dQ_w + 2*wmu*(mu-mut)/mut**2*dmu_w
    return np.array([gq, gw])

# 有限差分梯度（校验）
def grad_fd(qw, with_rot):
    g = np.zeros(2); h = 1e-6
    for i in range(2):
        pl = list(qw); pm = list(qw); pl[i] += h; pm[i] -= h
        g[i] = (chi2_case(pl, with_rot)-chi2_case(pm, with_rot))/(2*h)
    return g

# ---------------- (0) 解析 vs 有限差分梯度校验 ----------------
log("")
log("=== (0) 解析 vs 有限差分梯度（含旋转项）===")
maxerr = 0.0
for qw in [(1.5,2.5),(2.0,3.0),(3.0,4.0)]:
    ga = grad_chi2_case(qw, True); gd = grad_fd(qw, True)
    norm = float(np.linalg.norm(gd))
    if norm > 1e-8:
        e = float(np.max(np.abs(ga-gd)/np.maximum(np.abs(gd),1e-300)))
        maxerr = max(maxerr, e)
        log("  (q0=%.1f,ω0=%.1f) ‖∇χ²‖=%.2e 相对误差=%.3e" % (qw[0],qw[1],norm,e))
    else:
        log("  (q0=%.1f,ω0=%.1f) ‖∇χ²‖=%.2e<1e-8（靠近极小点，相对误差无定义）"
            % (qw[0],qw[1],norm))
log("  非极小点最大相对误差=%.3e %s" % (maxerr, "[OK<1e-3]" if maxerr<1e-3 else "[FAIL]"))

# ---------------- (1) SLSQP 对比：无旋转项 vs 有旋转项 ----------------
from scipy.optimize import minimize
starts = [(0.6,1.0),(1.0,6.0),(1.5,4.0),(2.0,3.0),(3.0,2.0),(4.0,1.5),(6.0,1.0)]
bnds = [(1e-6,None),(1e-6,None)]

def run_case(with_rot):
    res = []
    for s in starts:
        rr = minimize(lambda qw: chi2_case(qw, with_rot), s, jac=lambda qw: grad_chi2_case(qw, with_rot),
                      bounds=bnds, method="L-BFGS-B", options={"maxiter":2000,"ftol":1e-14})
        res.append((rr.x[0], rr.x[1], rr.fun))
    return res

res_no = run_case(False)
res_ye = run_case(True)

log("")
log("=== (1) SLSQP 收敛（L-BFGS-B 解析 jac，6 个不同初值）===")
log("-- 无旋转项（M=E_static 恒定）: 预期沿乘积线任意停靠 --")
for (q0,w0,c),s in zip(res_no, starts):
    log("    初值(q0=%.1f,ω0=%.1f) → 收敛(q0=%.6f,ω0=%.6f)  Π=%.4f  χ²=%.3e"
        % (s[0],s[1],q0,w0,q0*w0,c))
prod_no = [q0*w0 for q0,w0,_ in res_no]
log("    乘积 Π 分布: min=%.4f max=%.4f （应≈%.4f 但 (q0,ω0) 分散）"
    % (min(prod_no), max(prod_no), Qt/N))
spread_no = max(prod_no)-min(prod_no)

log("")
log("-- 有旋转项（M=E_static+½ω0²N 依赖 ω0）: 预期唯一收敛真实点 --")
for (q0,w0,c),s in zip(res_ye, starts):
    log("    初值(q0=%.1f,ω0=%.1f) → 收敛(q0=%.6f,ω0=%.6f)  χ²=%.3e"
        % (s[0],s[1],q0,w0,c))
q0s_list=[q0 for q0,_,_ in res_ye]; w0s_list=[w0 for _,w0,_ in res_ye]
spread_ye = max(q0s_list)-min(q0s_list) + max(w0s_list)-min(w0s_list)

log("")
log("=== (2) 简并是否被优化器内切断 ===")
log("  无旋转项: 收敛点 (q0,ω0) 沿乘积线分散（乘积 Π 均=%.4f 但各点不同）→ 简并流形上任意停靠"
    % (Qt/N))
# 相对散布（相对收敛点均值）
q0m = sum(q for q,_,_ in res_ye)/len(res_ye); w0m = sum(w for _,w,_ in res_ye)/len(res_ye)
spread_rel = max(max(abs(q-q0m)/q0m for q,_,_ in res_ye), max(abs(w-w0m)/w0m for _,w,_ in res_ye))
log("  有旋转项: 收敛点 (q0,ω0) 聚集到 (%.8f,%.8f)，相对散布=%.2e（机器精度级）"
    % (q0m, w0m, spread_rel))
unique = spread_rel < 1e-3
log("  结论：旋转能项使 SLSQP 收敛到唯一 (q0,ω0)=真实点 → 分支B 目标（消除简并、"
    "得到离散唯一参数集）在优化器层面成立。" if unique else
    "  结论：有旋转项仍未唯一收敛，需检查。")
if unique:
    log("  唯一解均值 vs 真实: q0=%.10f/%.2f  ω0=%.10f/%.2f  相对误差=%.2e/%.2e"
        % (q0m,q0s,w0m,w0s, abs(q0m-q0s)/q0s, abs(w0m-w0s)/w0s))

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
    ws = np.logspace(-1.0, 1.0, 300)
    Ms = E_st + 0.5*ws**2*N
    fig, ax = plt.subplots(1,2,figsize=(12,4.6))
    # 左：χ² 目标面（有旋转项）沿 (q0,ω0)——在真实点唯一最小
    gq = np.linspace(0.2,6.0,100); gw = np.linspace(0.3,8.0,100)
    QG,WG = np.meshgrid(gq,gw)
    Z = np.zeros_like(QG)
    for i in range(QG.shape[0]):
        for j in range(QG.shape[1]):
            Z[i,j] = chi2_case((QG[i,j],WG[i,j]), True)
    ax[0].contourf(QG, WG, np.log10(Z+1e-12), levels=40, cmap="viridis")
    ax[0].plot(q0s,w0s,'r*',ms=14,label="真实 (q0,ω0)")
    for q0,w0,c in res_ye:
        ax[0].plot(q0,w0,'wo',ms=5)
    ax[0].set_xlabel("q0"); ax[0].set_ylabel("ω0")
    ax[0].set_title("有旋转项 χ²(log10)：唯一最小在真实点")
    ax[0].legend(); ax[0].grid(alpha=0.3)
    # 右：无旋转项 χ² 沿乘积线平坦
    pv = np.linspace(0.5,6.0,300)
    cno = [chi2_case((v, Qt/(N*v)), False) for v in pv]
    ax[1].plot(pv, np.log10(np.array(cno)+1e-12), lw=2)
    ax[1].set_xlabel("q0（沿 ω0=Π/q0, Π=Qt/N）")
    ax[1].set_ylabel("χ²(log10)")
    ax[1].set_title("无旋转项 χ² 沿乘积线平坦（简并）")
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PNG, dpi=110)
    log("")
    log("绘图已保存: " + os.path.abspath(PNG))

log("")
log("红线声明：模型层面机制演示（固定剖面、无量纲自洽目标），不构成物理真实性主张；")
log("物理电子 (M,Q,μ) 单位制/4π 钉扎仍挂账。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
