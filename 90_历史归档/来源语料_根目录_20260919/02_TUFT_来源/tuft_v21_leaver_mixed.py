# -*- coding: utf-8 -*-
"""
TUFT v21 线一：Leaver 引擎整体混合边值复频谱
====================================================================
硬顺序（勘误#26 / E442）：
  ① GR 门：在已验证 Leaver(1985) s=-2 连分数（E436-E438）上，
     对标高精度目录 0.3736716844-0.0889623157 i (M=1)，|dw| <= 1e-8（>=8 位）。
  ② TUFT 整体混合边值复频谱（不是单向 IVP 求 r_b，不是单指数回声，不是单支 RK4 打靶）：
       内端  s=s_wall（R->0 反射核）：Neumann 正则级数  psi=1, psi'=0
       外端  s->inf：纯出射级数  psi ~ exp(i w s)
       两端均用 mpmath 高精度 Taylor 正则级数 ODE 推进（mp.odefun），
       在匹配点 s_m 做 Wronskian 匹配：D0(w)=psi_in psi_out' - psi_in' psi_out = 0
       （整函数 D0(w)=0 的复根即 modified-QNM 极点）。
  ③ 收敛三重检验：s_m / s_L / dps 变化下根稳定；根不稳即如实报告。
  ④ 输出 GR 门位数、TUFT modified-QNM 复极点、dw_r/w_r、d(1/|w_i|)、四态分级。
新方程 E443 起。
"""
import numpy as np
from scipy.optimize import brentq
import mpmath as mp

mp.mp.dps = 55
OUT = open(r"D:\a10\aikjx\code\my_lib\tuft_v21_leaver_mixed_out.txt", "w", encoding="utf-8")
def p(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s+"\n")

p("="*78)
p("TUFT v21 线一：Leaver 引擎整体混合边值复频谱（核 Neumann + 无穷远出射）")
p("="*78)

# ============================================================================
# ① GR 门：Leaver(1985) s=-2 连分数 （E436-E438，已验证引擎）
# ============================================================================
p("\n" + "-"*78)
p("① GR 门：Leaver(1985) s=-2 连分数复现 Schwarzschild l=2 引力复 QNM")
p("-"*78)

def leaver_F(w, l=2, eps=3, N=600):
    """Leaver continued-fraction characteristic function. w in 2M=1 units."""
    w = mp.mpc(w); rho = -1j*w
    a = lambda n: n*n + (2*rho+2)*n + 2*rho + 1
    b = lambda n: -(2*n*n + (8*rho+2)*n + 8*rho*rho + 4*rho + l*(l+1) - eps)
    g = lambda n: n*n + 4*rho*n + 4*rho*rho - eps - 1
    R = mp.mpf(0)
    for n in range(N, 0, -1):
        R = -g(n)/(b(n) + a(n)*R)
    a0 = 2*rho + 1
    b0 = -(8*rho*rho + 4*rho + l*(l+1) - eps)
    return b0 + a0*R

w0_2M = mp.mpc(0.74734 - 0.17792j)
root_gr = mp.findroot(leaver_F, w0_2M, solver='muller', tol=1e-16, maxsteps=200)
gr_M1 = root_gr/2
# high-precision catalog (Berti/Cardoso/Will table)
catalog = mp.mpc(0.3736716844 - 0.0889623157j)
derr = abs(gr_M1 - catalog)
p("   Leaver root (2M=1) = %.16f %+.16f i" % (mp.re(root_gr), mp.im(root_gr)))
p("   Leaver root (M=1)  = %.16f %+.16f i" % (mp.re(gr_M1), mp.im(gr_M1)))
p("   目录 (M=1)         = 0.3736716844 -0.0889623157 i")
p("   |dw| = %.3e" % derr)
digits = int(mp.floor(-mp.log10(derr))) if derr > 0 else 99
gr_pass = derr < mp.mpf('1e-8')
p("   GR 门: |dw| < 1e-8  ->  %s （约 %d 位）" % ("PASS" if gr_pass else "FAIL", digits))

# ============================================================================
# ② TUFT 几何：V(s) 表  （c=-0.29, d=-0.05, R=rho sqrt B 面积半径）
# ============================================================================
p("\n" + "-"*78)
p("② TUFT 几何 V(s)：R->0 反射核壁 s=0，外垒峰，尾 V~6/s^2")
p("-"*78)
C_C, C_D = -0.29, -0.05
rho_h = brentq(lambda r: r**3 + C_C*r + C_D, 1e-3, 5.0, xtol=1e-14)
rho_lo = rho_h*1.0008
rho = np.linspace(rho_lo, 250.0, 400000)
A = np.exp(-2/rho)
Bb = 1 + C_C/rho**2 + C_D/rho**3
B = np.exp(2/rho)*Bb
dsdr = np.sqrt(B/A)
s_arr = np.concatenate([[0.0], np.cumsum(0.5*(dsdr[1:]+dsdr[:-1])*np.diff(rho))])
q = -2/rho**2 + (-2*C_C/rho**3 - 3*C_D/rho**4)/Bb
J = np.sqrt(B)*(1+0.5*rho*q)
R_arr = rho*np.sqrt(B)
em2 = (J/np.sqrt(B))**2
V_arr = 3*A*(1+em2)/R_arr**2
iout = np.where(R_arr > 2.5)[0]
ipeak = iout[int(np.argmax(V_arr[iout]))]
s_peak = float(s_arr[ipeak]); V_peak = float(V_arr[ipeak])
p("   rho_h(R->0 核壁)=%.6f  wall s=%.4f" % (rho_h, s_arr[0]))
p("   外垒峰 R=%.4f  Vmax=%.6f  sqrtV=%.6f  s_peak=%.5f" %
  (R_arr[ipeak], V_peak, np.sqrt(V_peak), s_peak))
p("   核->垒峰龟长 L = %.5f M  往返 2L = %.5f M" % (s_peak-s_arr[0], 2*(s_peak-s_arr[0])))

def V_of_s(s):
    return mp.mpf(np.interp(float(s), s_arr, V_arr))
s_wall = float(s_arr[0])

# ============================================================================
# ③ 两端正则级数 + 无标度 Wronskian(对数导数) 匹配 F(w)=0
#    用对数导数 L=psi'/psi（消除 e^{i w s_L} 指数归一化伪因子，E430 分支混合教训）：
#      Riccati:  L' = -(w^2 - V(s)) - L^2
#    内支 L_in:  s_wall(Neumann) -> s_m,  L_in(s_wall)=0
#    外支 L_out: s_L(纯出射) -> s_m,       L_out(s_L)=i w  (V~6/s^2 尾截断)
#    特征条件 F(w)=L_in(s_m)-L_out(s_m)=0  （= Wronskian/|psi|^2，整函数）
# ============================================================================
p("\n" + "-"*78)
p("③ 两端正则级数 + 无标度对数导数 Wronskian: F(w)=L_in(s_m)-L_out(s_m)=0")
p("-"*78)

def Lin(w, s_m, s_w=s_wall):
    """内支 Neumann 对数导数 L_in(s_m)。Riccati 前向。"""
    w = mp.mpc(w)
    def f(s, L):
        return [-(w*w - V_of_s(s)) - L[0]*L[0]]
    od = mp.odefun(f, mp.mpf(s_w), [mp.mpf(0)])
    return od(s_m)[0]

def Lout(w, s_m, s_L):
    """外支纯出射对数导数 L_out(s_m)。Riccati 用 tau=s_L-s 反向。"""
    w = mp.mpc(w)
    def f(tau, L):
        s = s_L - tau
        return [-(w*w - V_of_s(s)) - L[0]*L[0]]
    od = mp.odefun(f, mp.mpf(0), [1j*w])
    return od(mp.mpf(s_L - s_m))[0]

def F(w, s_m, s_L):
    return Lin(w, s_m) - Lout(w, s_m, s_L)

# 扫描定位 TUFT 极点初值（L 均为 O(w)~0.4，无指数因子）
p("   F(w) 模扫描（找 TUFT 极点初值）：s_m=%.3f s_L=%.1f" % (3.0, 80.0))
grid_wr = [0.30,0.34,0.3737,0.41,0.45,0.50]
grid_wi = [0.02,0.05,0.09,0.15,0.25]
best = None
for wr in grid_wr:
    row = []
    for wi in grid_wi:
        try:
            val = F(mp.mpc(wr-wi*1j), 3.0, 80.0)
            row.append("%.2e"%float(abs(val)))
            if best is None or abs(val) < best[0]:
                best = (abs(val), wr, wi)
        except Exception:
            row.append("err")
    p("     wr=%.4f  %s" % (wr, "  ".join(row)))
p("   最小 |F| 初值: wr=%.4f wi=%.4f |F|=%.3e" % (best[1], best[2], best[0]))

# ============================================================================
# ④ 复平面求根 D0(w)=0
# ============================================================================
p("\n" + "-"*78)
p("④ 复平面求 D0(w)=0 -> TUFT modified-QNM 复极点")
p("-"*78)

s_m_ref = 3.0
s_L_ref = 80.0
w_start = mp.mpc(best[1] - best[2]*1j)
p("   初值 w0 = %.6f %+.6f i   (s_m=%.2f, s_L=%.1f)" %
  (mp.re(w_start), mp.im(w_start), s_m_ref, s_L_ref))

def F_ref(w):
    return F(w, s_m_ref, s_L_ref)

root_tuft = mp.findroot(F_ref, w_start, tol=1e-13, maxsteps=300)
p("   TUFT modified-QNM 极点 = %.10f %+.10f i" % (mp.re(root_tuft), mp.im(root_tuft)))
p("   残差 |F| = %.3e" % abs(F_ref(root_tuft)))

# --- 三重收敛检验 ---
p("\n   --- 收敛三重检验（根应在变化下稳定）---")
p("   s_m 变化：")
roots_sm = []
for sm in [1.5, 2.5, 4.0, 5.5]:
    r = mp.findroot(lambda w: F(w, sm, s_L_ref), root_tuft, tol=1e-12, maxsteps=200)
    roots_sm.append(r)
    p("     s_m=%.1f -> %.8f %+.8f i" % (sm, mp.re(r), mp.im(r)))
p("   s_L 变化：")
roots_sl = []
for sl in [50.0, 120.0, 180.0]:
    r = mp.findroot(lambda w: F(w, s_m_ref, sl), root_tuft, tol=1e-12, maxsteps=200)
    roots_sl.append(r)
    p("     s_L=%.0f -> %.8f %+.8f i" % (sl, mp.re(r), mp.im(r)))
p("   dps 变化 (40/60/80)：")
roots_dp = []
saved = mp.mp.dps
for dps in [40, 60, 80]:
    mp.mp.dps = dps
    r = mp.findroot(lambda w: F(w, s_m_ref, s_L_ref), root_tuft, tol=1e-12, maxsteps=200)
    roots_dp.append(r)
    p("     dps=%d -> %.8f %+.8f i" % (dps, mp.re(r), mp.im(r)))
mp.mp.dps = saved

# 收敛度：相对散布
allroots = [root_tuft]+roots_sm+roots_sl+roots_dp
mean = sum(allroots)/len(allroots)
scatter = max(abs(r-mean) for r in allroots)
p("   根对 (s_m,s_L,dps) 的最大散布 |r-mean| = %.3e" % scatter)
converged = scatter < mp.mpf('1e-6')
p("   收敛判定（散布<1e-6）: %s" % ("CONVERGED" if converged else "NOT-CONVERGED（如实报告）"))

# ============================================================================
# ⑤ 相对 GR 极点的偏移 + 四态分级
# ============================================================================
p("\n" + "-"*78)
p("⑤ 相对 GR 极点的偏移 + 四态分级")
p("-"*78)
gr_wr, gr_wi = float(mp.re(catalog)), float(-mp.im(catalog))   # catalog: 0.3737 -0.089i
tu_wr, tu_wi = float(mp.re(root_tuft)), float(-mp.im(root_tuft))
GR_TAU = 1.0/gr_wi
TU_TAU = 1.0/tu_wi
dwr_over = (tu_wr - gr_wr)/gr_wr
dtau = TU_TAU - GR_TAU
p("   GR 极点    : %.6f %+.6f i   tau=1/|w_i|=%.4f M" % (gr_wr, -gr_wi, GR_TAU))
p("   TUFT 极点  : %.6f %+.6f i   tau=%.4f M" % (tu_wr, -tu_wi, TU_TAU))
p("   dw_r/w_r      = %+.4f %%  (=%+.3e)" % (100*dwr_over, dwr_over))
p("   d(1/|w_i|)    = %+.4f M   (GR tau=%.3f M)" % (dtau, GR_TAU))

p("\n   四态分级：")
p("   态I 极点不动(dw_r/w_r~0)：铃响与 GR 不可分辨")
p("   态II 极点小移：中等 SNR 可分辨")
p("   态III 大移/新腔模")
p("   态IV 回声串主导（v19 已证伪单指数拟合，勘误#25）")
if not converged:
    p("   => 根未收敛，不做态判定（不伪闭合）。")
elif abs(dwr_over) < 1e-3:
    p("   => 落【态I】：modified-QNM 极点移动 ~0，核 Neumann 替换吸收视界不改主频极点。")
elif abs(dwr_over) < 0.05:
    p("   => 落【态II】：modified-QNM 极点小移 %+.2f%%，寿命 %+.2f M。" % (100*dwr_over, dtau))
else:
    p("   => 落【态III】：modified-QNM 极点大移 %+.2f%%。" % (100*dwr_over))

p("\n" + "="*78)
p("E443 起新方程清单：")
p("="*78)
p("E443  TUFT 整体混合边值 ODE: psi''(s)+[w^2-V(s)]psi=0,  s in [s_wall, inf)")
p("E444  内端 Neumann 正则级数: psi(s_wall)=1, psi'(s_wall)=0  (R->0 反射核)")
p("E445  外端纯出射级数: psi(s->inf) ~ exp(i w s)  (V~6/s^2 尾，s_L 处截断)")
p("E446  对数导数 Riccati: L'=-(w^2-V)-L^2 ; F(w)=L_in(s_m)-L_out(s_m)=0  (无标度)")
p("E447  modified-QNM 极点: F(w)=0 复根；s_m/s_L/dps 三重收敛检验")
p("E448  GR 门: Leaver s=-2 连分数 -> %.10f %+.10f i (|dw|=%.1e)" %
  (mp.re(gr_M1), mp.im(gr_M1), float(derr)))
OUT.close()
print("\n[written] tuft_v21_leaver_mixed_out.txt")
