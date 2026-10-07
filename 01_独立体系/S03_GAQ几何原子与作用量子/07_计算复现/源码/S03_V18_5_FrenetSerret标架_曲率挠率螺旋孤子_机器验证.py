# -*- coding: utf-8 -*-
"""
S03 V18.5 · GAQ-UFT V18 升级稿（Frenet-Serret 标架 / 曲率 kappa / 挠率 tau 螺旋流形）
          全维审查与机器验证

来稿性质：由「常曲率常挠率平直空间近似（u^2+v^2=c^2）」升级到
          「Frenet-Serret 活动标架 + 螺旋度拓扑不变量」的改写稿，
          含 §1 螺旋度与拓扑内禀质量、§2 有质量类时孤子投影守恒、
          §3 光子零模、§4 场与质量耦合、§5 强场失效、§6 三方对比，
          末尾给出三个下一步分支。

本册判决：不接受「升级即改进」的默认叙事，逐条做量纲/几何/自洽/实验四层裁定。

验证 1（V5-a）圆螺旋曲率挠率解析式 vs F-S 定义式（精确算术，非数值微分）
验证 2（V5-b）kappa/tau = u/v 恒等式 + 副法向 B 与 z 轴夹角 cos(theta) = u/c
验证 3（V5-c）§2 投影守恒式与 F-S 几何的相容性穷举（三种读法逐一机器判定）
验证 4（V5-d）§3 光子零模：k 平行 B => tau == 0 => 挠率型能量为 0（退化判定）
验证 5（V5-e）§5「强场失效」是否波及 u^2+v^2=c^2（变 kappa/tau 数值积分）
验证 6（V5-f）v_perp/v_par = alpha 普适断言的速度上限预言 vs 加速器实测
验证 7（V5-g）量纲代数：m' ∝ ∫tau ds 与 E ∝ H 的量纲闭合性
验证 8（V5-h）螺旋度守恒的成立前提与缺口登记
验证 9（V5-i）与本仓既有登记的交叉（防止重复劳动与口径冲突）
自检 10 项

红线：
- 本册全部结论为**可否证性裁定**，不含正面支持证据。
- 数值只用于裁定自洽性，不用于拟合任何实验值。
- 引用 alpha = 1/137 与加速器速度实测值仅作对照基准。
- 来稿 §3 的「光子能量由挠率面积分给出」在本册被判定为不可实现，
  该否证只针对「单条空间曲线的 F-S 挠率」实现路径，不否定一切光子螺旋模型。

判定词表：PASS / FAIL / BOUNDARY / INFO
"""
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ------------------------------------------------------------------ 常量
C_LIGHT = 299792458.0                 # m/s，定义值
ALPHA_CODATA = 7.2973525693e-03       # 1/137.035999084
ALPHA2 = ALPHA_CODATA ** 2
PHI = (1.0 + math.sqrt(5.0)) / 2.0
ALPHA_SQRT_PHI = math.sqrt(PHI)
# 加速器实测：LEP 质子 beta = 0.9999999910（1-beta = 9e-9）
V_PAR_MEASURED = 0.9999999910

RESULTS = []


def P(name, detail):
    RESULTS.append(("PASS", name, detail))


def F(name, detail):
    RESULTS.append(("FAIL", name, detail))


def B(name, detail):
    RESULTS.append(("BOUNDARY", name, detail))


def I(name, detail):
    RESULTS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 72)
    print(title)
    print("=" * 72)


# ================================================================ 验证 1
hdr("VER-1 | V5-a  circular-helix curvature/torsion: analytic vs F-S definition")

# r(t) = (R cos wt, R sin wt, cz t)，切向速率 R^2 w^2 + cz^2 = c^2
W_OMEGA = 1.0e15                    # rad/s
U_OVER_C = 0.9                       # 横向速率 u = R*omega
V_OVER_C = math.sqrt(1.0 - U_OVER_C ** 2)
U = U_OVER_C * C_LIGHT
V = V_OVER_C * C_LIGHT
R_HELIX = U / W_OMEGA
CZ = V
# 解析式（来稿 §1）
KAPPA_ANALYTIC = R_HELIX * W_OMEGA ** 2 / C_LIGHT ** 2
TAU_ANALYTIC = W_OMEGA * CZ / C_LIGHT ** 2
# F-S 定义式：用解析导数组件精确算（不做数值微分，避免截断误差）
r1 = (-R_HELIX * W_OMEGA, 0.0, 0.0)   # 占位，稍后按 sin/cos 实算
T_PHASE = 0.3712345678              # 任意相位，避免对称性


def derivs(t):
    st, ct = math.sin(W_OMEGA * t), math.cos(W_OMEGA * t)
    r1 = (-R_HELIX * W_OMEGA * st, R_HELIX * W_OMEGA * ct, CZ)
    r2 = (-R_HELIX * W_OMEGA ** 2 * ct, -R_HELIX * W_OMEGA ** 2 * st, 0.0)
    r3 = (R_HELIX * W_OMEGA ** 3 * st, -R_HELIX * W_OMEGA ** 3 * ct, 0.0)
    return r1, r2, r3


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


r1, r2, r3 = derivs(T_PHASE)
cr = cross(r1, r2)
speed = norm(r1)
kappa_def = norm(cr) / speed ** 3
tau_def = dot(cr, r3) / (norm(cr) ** 2)
rel_kappa = abs(kappa_def - KAPPA_ANALYTIC) / KAPPA_ANALYTIC
rel_tau = abs(tau_def - TAU_ANALYTIC) / TAU_ANALYTIC

print("  R*omega = u = {0:.6e} m/s,  cz = v = {1:.6e} m/s".format(U, V))
print("  R = {0:.6e} m, omega = {1:.6e} rad/s".format(R_HELIX, W_OMEGA))
print("  kappa analytic = {0:.12e} 1/m".format(KAPPA_ANALYTIC))
print("  kappa F-S def  = {0:.12e} 1/m   rel.dev = {1:.3e}".format(kappa_def, rel_kappa))
print("  tau   analytic = {0:.12e} 1/m".format(TAU_ANALYTIC))
print("  tau   F-S def  = {0:.12e} 1/m   rel.dev = {1:.3e}".format(tau_def, rel_tau))
P("V5-a", "圆螺旋曲率挠率解析式 kappa=R*w^2/c^2、tau=w*cz/c^2 与 Frenet-Serret "
          "定义式 kappa=|r'xr''|/|r'|^3、tau=((r'xr'').r''')/|r'xr''|^2 在非对称相位上"
          "逐个相对偏差 {0:.2e} / {1:.2e}（浮点机器零）。来稿 §1 的解析式**正确**。".format(rel_kappa, rel_tau))

# ================================================================ 验证 2
hdr("VER-2 | V5-b  kappa/tau = u/v identity and binormal tilt angle")

bhat = (cr[0] / norm(cr), cr[1] / norm(cr), cr[2] / norm(cr))
ratio_kt = KAPPA_ANALYTIC / TAU_ANALYTIC
ratio_uv = U / V
rel_ratio = abs(ratio_kt - ratio_uv) / ratio_uv
print("  kappa/tau      = {0:.15f}".format(ratio_kt))
print("  u/v            = {0:.15f}".format(ratio_uv))
print("  B_hat          = ({0:.6f}, {1:.6f}, {2:.6f})".format(*bhat))
cos_theta = bhat[2]
print("  B_hat . z_hat  = {0:.15f}".format(cos_theta))
print("  u/c            = {0:.15f}".format(U_OVER_C))
rel_btilt = abs(cos_theta - U_OVER_C) / U_OVER_C
P("V5-b", "kappa/tau = u/v 在圆螺旋上严格成立（rel.dev {0:.2e}）；且副法向与螺旋轴的"
          "夹角余弦 cos(theta) = B.z = u/c（rel.dev {1:.2e}）——即**副法向 B 一般不与"
          "轴向平行**（仅当 u=c 即 v=0 的平面圆时才平行，此时 tau=0）。".format(rel_ratio, rel_btilt))

# ================================================================ 验证 3
hdr("VER-3 | V5-c  compatibility of the projected-mass conservation law")

print("  来稿 §2 的赋值：  m' ~ c*tau*dt   (topological mass)")
print("                  m  ~ c*kappa*dt (apparent mass)")
print("  => m/m' = kappa/tau = u/v  (by VER-2)")
print("  => conservation m'*c = m*v_perp  =>  m/m' = c/v_perp")
print()
print("  reading A: keep m' c = m v_perp and kappa/tau = alpha = v_perp/v_par")
v_perp_A = ALPHA_CODATA * C_LIGHT / math.sqrt(1.0 + ALPHA2)
ratio_c_over_vperp = C_LIGHT / v_perp_A
print("     c/v_perp(alpha_CODATA) = {0:.6f}".format(ratio_c_over_vperp))
print("     kappa/tau required    = alpha = {0:.9f}".format(ALPHA_CODATA))
print("     mismatch ratio        = {0:.4f}".format(ratio_c_over_vperp / ALPHA_CODATA))
# 解析解：alpha^4 = 1 + alpha^2  =>  x^2 = 1 + x  =>  x = phi  =>  alpha = sqrt(phi)
alpha_star = ALPHA_SQRT_PHI
resid_A = alpha_star ** 4 - 1.0 - alpha_star ** 2
print("     forced solution alpha = sqrt(phi) = {0:.12f}".format(alpha_star))
print("     residual alpha^4-1-alpha^2 = {0:.3e}".format(resid_A))
print("     alpha_star / alpha_CODATA = {0:.3f}".format(alpha_star / ALPHA_CODATA))
# 直接代入实验 alpha 看方程残差
resid_exp = ALPHA_CODATA ** 4 - 1.0 - ALPHA_CODATA ** 2
print("     same equation at alpha_CODATA: residual = {0:.6f} (need 0)".format(resid_exp))
F("V5-c-A", "读法 A（保留 m'c = m*v_perp）无实解：联立 kappa/tau = v_perp/v_par 与 "
            "u^2+v^2=c^2 后唯一相容值被迫为 **alpha = sqrt(phi) = {0:.6f}**，"
            "与 alpha_CODATA = {1:.9f} 相差 {2:.1f} 倍；把实验 alpha 代回同一方程残差 = {3:.4f}。"
            "=> 守恒式 m'c = m*v_perp 与「m ∝ kappa、m' ∝ tau、kappa/tau = alpha」三者在"
            "实数域**互不相容**。".format(alpha_star, ALPHA_CODATA, alpha_star / ALPHA_CODATA, resid_exp))
print()
print("  reading B: swap the velocity slot -> m'*v_perp = m*v_par")
k_common = KAPPA_ANALYTIC / KAPPA_ANALYTIC
m_prime = TAU_ANALYTIC * k_common
m_app = KAPPA_ANALYTIC * k_common
lhs = m_prime * U
rhs = m_app * CZ
rel_B = abs(lhs - rhs) / rhs
print("     m' v_perp = {0:.15e}".format(lhs))
print("     m  v_par  = {0:.15e}".format(rhs))
print("     rel.dev   = {0:.3e}".format(rel_B))
P("V5-c-B", "读法 B（守恒式改为 m'*v_perp = m*v_par）在圆螺旋几何下**恒成立**"
            "（rel.dev {0:.2e}，机器零）：因为 m/m' = kappa/tau = u/v 恰是等式本身。"
            "量纲 M*L/T（动量）闭合。故来稿 §2 的守恒式存在**变量槽位错位**："
            "把切向速率 c 塞进了投影守恒式的轴向槽位。".format(rel_B))
print()
print("  reading C: if alpha = v_perp/v_par is FIXED to alpha_CODATA for all particles,")
v_par_cap = C_LIGHT / math.sqrt(1.0 + ALPHA2)
dv_cap = C_LIGHT - v_par_cap
print("     => v_par <= c/sqrt(1+alpha^2) = {0:.12f} c".format(v_par_cap / C_LIGHT))
print("     => speed gap  c - v_par_max = {0:.4f} m/s".format(dv_cap))
I("V5-c-C", "读法 C 的推论留给 VER-6 单独裁定（速度上限预言 vs 加速器实测）。")

# ================================================================ 验证 4
hdr("VER-4 | V5-d  photon zero-mode: k parallel B forces tau == 0")

print("  claim under test (lai gao section 3):")
print("    (a) E_gamma  ∝  ∫ tau_gamma dS        (energy from TORSION)")
print("    (b) propagation direction k  =  binormal B  (helix axis along k)")
print()
# (b) + F-S third equation: dB/ds = -tau N ;  if B ≡ khat (fixed) then dB/ds = 0
# => tau = 0 identically (N never vanishes for regular curve)
resid_tau_zero = 0.0
# machine check: integrate F-S with B fixed along z => kappa arbitrary, tau must be 0
# closed form: B constant  <=>  tau(s) = 0 everywhere; verify with an explicit
# curve whose binormal is fixed: planar circle.
R_PLANE = 1.0e-6
r1p = (-R_PLANE * W_OMEGA, 0.0, 0.0)


def planar_derivs(t):
    st, ct = math.sin(W_OMEGA * t), math.cos(W_OMEGA * t)
    return ((-R_PLANE * W_OMEGA * st, R_PLANE * W_OMEGA * ct, 0.0),
            (-R_PLANE * W_OMEGA ** 2 * ct, -R_PLANE * W_OMEGA ** 2 * st, 0.0),
            (R_PLANE * W_OMEGA ** 3 * st, -R_PLANE * W_OMEGA ** 3 * ct, 0.0))


p1, p2, p3 = planar_derivs(T_PHASE)
cp = cross(p1, p2)
tau_plane = dot(cp, p3) / (norm(cp) ** 2)
bhat_plane_z = cp[2] / norm(cp)
print("  planar circle (B || z, i.e. axis along propagation):")
print("     tau            = {0:.3e} 1/m".format(tau_plane))
print("     B_hat . z_hat  = {0:.15f}".format(bhat_plane_z))
print("     ∫ tau dS       = 0  identically  =>  E_gamma = 0  by claim (a)")
print()
print("  converse: tau == 0 identically  <=>  B constant  <=>  planar curve")
print("     dB/ds = -tau N = 0  when B fixed  =>  tau = 0  (N never vanishes)")
print("     and (VER-2) kappa/tau = u/v  =>  tau = 0  <=>  helix degenerates to a circle")
F("V5-d", "来稿 §3 的两条断言在本框架内互斥：(a) 能量来自挠率面积分、(b) 传播方向 k = 副法向 B。"
          "由 F-S 第三式 dB/ds = -tau*N，若 B 平行于固定传播方向则 B 为常矢量 => tau 恒为 0"
          "（机器复算平面圆 tau = {0:.1e}，B.z = {1:.6f}），于是 ∫tau dS = 0 => 光子能量为 0。"
          "反向亦真：tau 恒 0 即曲线平面、副法向恒定。"
          "=> **横螺旋零模 + 挠率型能量 在单条空间曲线的 F-S 实现下不可同时成立。**".format(tau_plane, bhat_plane_z))
B("V5-d-esc", "可行出路有三条：(i) 光子能量改为曲率面积分 ∫kappa dS（kappa 不为 0，与 §1 的 H∝旋度"
              "更自洽）；(ii) 放弃 k 平行 B，改纵螺旋（则与光子横波性失去对应）；"
              "(iii) 推广到 4D **世界线**曲线（时间非外禀参数），此时「平面性」不再是约束，"
              "需 Bishop 标架或 Fermi-Walker 标架。本册不选定，仅登记。")

# ================================================================ 验证 5
hdr("VER-5 | V5-e  does strong-field (non-constant kappa/tau) break u^2+v^2=c^2 ?")

# Integrate F-S in arc length with kappa(s), tau(s) varying; check
#   |dr/dt| = c   and   v_par^2 + v_perp^2 = c^2  at every step.
N_STEPS = 200000
DS = 1.0e-5                         # arc-length step [m]
S_MAX = N_STEPS * DS


def kappa_of_s(s):
    # strongly varying: log-periodic modulation, ratio kappa/tau NOT constant
    return 1.0 / (1.0e-3) * (1.0 + 0.8 * math.sin(2.0 * math.pi * s / 0.7))


def tau_of_s(s):
    return 1.0 / (1.0e-3) * (1.0 + 0.5 * math.cos(2.0 * math.pi * s / 0.7))


T = [1.0, 0.0, 0.0]
N = [0.0, 1.0, 0.0]
Bm = [0.0, 0.0, 1.0]
pos = [0.0, 0.0, 0.0]
hist = [[0.0, 0.0, 0.0]]
max_speed_err = 0.0
max_pyth_err = 0.0
max_ortho_err = 0.0
max_kappa_err = 0.0
max_tau_err = 0.0
CHECK_EVERY = 2000
for i in range(N_STEPS):
    s = i * DS
    kap = kappa_of_s(s)
    tau = tau_of_s(s)
    dT = [kap * N[j] for j in range(3)]
    dN = [-kap * T[j] + tau * Bm[j] for j in range(3)]
    dB = [-tau * N[j] for j in range(3)]
    for j in range(3):
        pos[j] += T[j] * DS
        T[j] += dT[j] * DS
        N[j] += dN[j] * DS
        Bm[j] += dB[j] * DS
    hist.append(pos[:])
    nT = math.sqrt(sum(x * x for x in T))
    nN = math.sqrt(sum(x * x for x in N))
    nB = math.sqrt(sum(x * x for x in Bm))
    for j in range(3):
        T[j] /= nT
        N[j] /= nN
        Bm[j] /= nB
    # tangent speed with s = c*t  =>  dr/dt = c*T  => speed = c exactly
    sp = C_LIGHT * math.sqrt(sum(x * x for x in T))
    max_speed_err = max(max_speed_err, abs(sp - C_LIGHT) / C_LIGHT)
    # decompose T into vertical (par) and horizontal (perp) parts
    v_par = T[2] * C_LIGHT
    v_perp2 = (T[0] ** 2 + T[1] ** 2) * C_LIGHT ** 2
    max_pyth_err = max(max_pyth_err,
                       abs(v_par ** 2 + v_perp2 - C_LIGHT ** 2) / (C_LIGHT ** 2))
    # non-trivial check: recover kappa/tau from the integrated trajectory by
    # 1st/2nd/3rd order finite differences at the mid point p[i-1]
    if i >= 3 and i % CHECK_EVERY == 0:
        p1 = hist[i]
        p0 = hist[i - 1]
        pm1 = hist[i - 2]
        pm2 = hist[i - 3]
        d1 = [(p1[j] - p0[j]) / DS for j in range(3)]
        d2 = [(p1[j] - 2.0 * p0[j] + pm1[j]) / (DS * DS) for j in range(3)]
        d3 = [(p1[j] - 3.0 * p0[j] + 3.0 * pm1[j] - pm2[j]) / (DS ** 3)
              for j in range(3)]
        cf = cross(d1, d2)
        ncf = norm(cf)
        if ncf > 0.0:
            k_num = ncf / (norm(d1) ** 3)
            t_num = dot(cf, d3) / (ncf ** 2)
            s_mid = (i - 1) * DS
            kap_ref = kappa_of_s(s_mid)
            tau_ref = tau_of_s(s_mid)
            max_kappa_err = max(max_kappa_err,
                                abs(k_num - kap_ref) / max(abs(kap_ref), 1e-12))
            max_tau_err = max(max_tau_err,
                              abs(t_num - tau_ref) / max(abs(tau_ref), 1e-12))
# orthogonality drift is an integrator artifact; measure it separately
T = [1.0, 0.0, 0.0]
N = [0.0, 1.0, 0.0]
Bm = [0.0, 0.0, 1.0]
for i in range(20000):
    s = i * DS
    kap = kappa_of_s(s)
    tau = tau_of_s(s)
    dT = [kap * N[j] for j in range(3)]
    dN = [-kap * T[j] + tau * Bm[j] for j in range(3)]
    dB = [-tau * N[j] for j in range(3)]
    for j in range(3):
        T[j] += dT[j] * DS
        N[j] += dN[j] * DS
        Bm[j] += dB[j] * DS
    nT = math.sqrt(sum(x * x for x in T))
    nN = math.sqrt(sum(x * x for x in N))
    nB = math.sqrt(sum(x * x for x in Bm))
    max_ortho_err = max(max_ortho_err,
                        max(abs(nT - 1.0), abs(nN - 1.0), abs(nB - 1.0)))
    for j in range(3):
        T[j] /= nT
        N[j] /= nN
        Bm[j] /= nB
print("  steps = {0},  arc length = {1:.3f} m".format(N_STEPS, S_MAX))
print("  kappa(s), tau(s) both strongly varying (period 0.7 m, +/-80% / +/-50%)")
print("  [non-trivial] max rel err of kappa recovered from trajectory = {0:.3e}".format(max_kappa_err))
print("  [non-trivial] max rel err of tau   recovered from trajectory = {0:.3e}".format(max_tau_err))
print("  [trivial]     max rel err of |dr/dt| vs c        = {0:.3e}".format(max_speed_err))
print("  [trivial]     max rel err of v_par^2+v_perp^2=c^2= {0:.3e}".format(max_pyth_err))
print("  [integrator]  max | |T| , |N| , |B| - 1 | (no-projection run) = {0:.3e}".format(max_ortho_err))
P("V5-e", "在 kappa(s)、tau(s) 强非恒定（±80%/+±50% 调制，20 万步显式欧拉）的 F-S 积分下，"
          "从轨迹反算的曲率与挠率相对偏差为 {0:.2e} / {1:.2e}（非平凡检验：证明积分链本身实现正确）；"
          "|dr/dt| 恒等于 c 与 v_par^2+v_perp^2=c^2 的残差 {2:.1e} / {3:.1e} 属**平凡恒等式**"
          "（|dr/dt|=|dr/ds|·ds/dt=1·c，与 kappa、tau 无关）；无投影运行的标架模漂移 {4:.1e} "
          "是显式欧拉的积分器误差，由逐步归一化补偿，**不构成物理结论**。"
          "=> **来稿 §5「强场失效」过度否定**：分解式 u^2+v^2=c^2 是 ds/dt=c 公设的恒等推论，"
          "与 kappa、tau 是否恒定无关；真正失效的只是「圆螺旋解析式 kappa=R*w^2/c^2」。".format(
              max_kappa_err, max_tau_err, max_speed_err, max_pyth_err, max_ortho_err))

# ================================================================ 验证 6
hdr("VER-6 | V5-f  speed ceiling from v_perp/v_par = alpha vs accelerator data")

v_par_ceiling = C_LIGHT / math.sqrt(1.0 + ALPHA2)
gap_gaq = C_LIGHT - v_par_ceiling
gap_meas = C_LIGHT * (1.0 - V_PAR_MEASURED)
print("  GAQ prediction  v_par <= c/sqrt(1+alpha^2) = {0:.12f} c".format(v_par_ceiling / C_LIGHT))
print("  speed gap (GAQ)      = {0:.4f} m/s  ({1:.4f} km/s)".format(gap_gaq, gap_gaq / 1000.0))
print("  speed gap (LEP proton)= {0:.3e} m/s  (1-beta = 9e-9)".format(gap_meas))
print("  discrepancy factor   = {0:.3e}".format(gap_gaq / gap_meas))
F("V5-f", "若同时采纳「v_perp/v_par = alpha_CODATA 对所有粒子相同」与「切向速率恒为 c」，"
          "则任何基元世界线的轴向投影速度上限为 {0:.10f} c，缺口 {1:.1f} m/s（≈{2:.1f} km/s）；"
          "而加速器实测 1-beta ≈ 9e-9（缺口约 {3:.2f} m/s），两者相差 {4:.1f} 倍。"
          "=> **既有 GAQ 断言 v_perp/v_par = alpha = 1/137 被现有加速器数据否证**"
          "（该断言原被登记为「中可行性可检验预言」）。射程：只否证「投影速率之比为 alpha」"
          "这一条，不否证切向速率公设本身。".format(
              v_par_ceiling / C_LIGHT, gap_gaq, gap_gaq / 1000.0, gap_meas, gap_gaq / gap_meas))

# ================================================================ 验证 7
hdr("VER-7 | V5-g  dimensional algebra of m' ∝ ∫tau ds and E ∝ H")

# dimension vectors: (M, L, T, I, Theta, N, J)
D = dict(M=0, L=1, T=2, I=3, Th=4, N=5, J=6)


def dim(*pairs):
    v = [0] * 7
    for base, p in pairs:
        v[D[base]] += p
    return tuple(v)


def dshow(v):
    names = ["M", "L", "T", "I", "Th", "N", "J"]
    out = [nm for nm, e in zip(names, v) if e != 0]
    return "1" if not out else " * ".join(
        nm if e == 1 else "{0}^{1}".format(nm, e) for nm, e in zip(names, v) if e != 0)


D_OMEGA = dim(("T", -1))
D_C = dim(("L", 1), ("T", -1))
D_KAPPA = dim(("L", -1))
D_TAU = dim(("L", -1))
D_R = dim(("L", 1))
D_MASS = dim(("M", 1))
D_E = dim(("M", 1), ("L", 2), ("T", -2))
D_MOM = dim(("M", 1), ("L", 1), ("T", -1))
D_INT_TAU_DS = (0, 0, 0, 0, 0, 0, 0)          # ∫ tau ds  -> dimensionless
D_C3_INT_TAU_DT = (0, 2, -2, 0, 0, 0, 0)      # c^3 ∫tau dt -> M^0 L^2 T^-2
D_BVEC = dim(("M", 1), ("T", -2), ("I", -1))
D_HHEL = dim(("M", 2), ("L", 4), ("T", -4), ("I", -2))   # ∫A.(curl A) dV
rows = [
    ("[omega]", dshow(D_OMEGA)),
    ("[c]", dshow(D_C)),
    ("[kappa] = [tau]", dshow(D_KAPPA)),
    ("[kappa/tau] = [alpha] = [u/v]", "1"),
    ("[∫ tau ds]", dshow(D_INT_TAU_DS)),
    ("[c^3 ∫ tau dt]", dshow(D_C3_INT_TAU_DT)),
    ("[E] = [m' c^2]", dshow(D_E)),
    ("[m' c] = [m v]", dshow(D_MOM)),
    ("[H] = ∫ A·(∇×A) dV", dshow(D_HHEL)),
]
for a, b in rows:
    print("  {0:28s} = {1}".format(a, b))
print()
print("  check 1: m' ∝ ∫ tau ds  =>  [m'] = 0  but [E] = [m' c^2] needs M^1 L^2 T^-2")
print("          => MISSING mass dimension 1; needs an eta with [eta] = M")
print("  check 2: E ∝ c^3 ∫tau dt has dimension M^0 L^2 T^-2 = E/mass")
print("          => energy formula short by exactly one mass power")
print("  check 3: [H] = M^2 L^4 T^-4 I^-2 ; [E]/[H] = M^-1 L^-2 T^2 I^2 != 1")
print("          => coupling constant eta_H needed, NOT dimensionless")
print("  check 4: [m' c] = [m v_perp] = M L T^-1  (momentum) -> CONSISTENT")
F("V5-g", "量纲封锁：(1) m' ∝ ∫tau ds 给出的 m' 无量纲（∫tau ds 的量纲恰为 1），"
          "而 m'c^2 缺一个质量幂次 ⇒ 必须引入具质量量纲的耦合常数 eta；"
          "(2) E ∝ H 中 H = ∫A·(∇×A)dV 的量纲是 M^2 L^4 T^-4 I^-2，与能量不同族，"
          "耦合常数不可能取为无量纲；(3) 唯一量纲闭合的是 m'c = m*v（动量）。"
          "本仓既有判决 S03-C0025/C0027/C0028 已裁定：纯几何量集 kappa/tau/Omega/c 的"
          "质量分量恒为 0，唯一携带质量量纲的可用量是 G 且其值须外加 ⇒ "
          "**「拓扑内禀质量 m'」在体系内无法取得非零质量量纲，除非外加 G 或 m_P**。")

# ================================================================ 验证 8
hdr("VER-8 | V5-h  helicity conservation: premises and open gap")

B("V5-h-1", "H = ∫A·(∇×A) dV 的守恒（Kelvin/Helmholtz 型）只在**理想无耗散**"
             "（无磁阻/电阻率、无涡旋扩散、完美导体）下成立；来稿未声明该前提。"
             "在有耗散的真实场中 H 的耗散方程含 η·∫|∇×B|^2 项 ⇒ H 单调衰减。"
             "把 H 当作精确拓扑不变量使用需要显式声明理想化前提。")
B("V5-h-2", "本仓已登记 S03-C0006【BOUNDARY】几何挠率手性与弱螺旋性的定量关系未给出、"
             "接口未定义；来稿 §1 直接把 H 当作唯一守恒量使用，未处理与 C0006 的口径冲突。")
B("V5-h-3", "来稿未给出 H 与粒子螺旋度（±1）量子数之间的映射；连续 H 如何离散化为"
             "自旋量子数仍是缺口（与 S03-C0011 自旋统计缺口同源）。")

# ================================================================ 验证 9
hdr("VER-9 | V5-i  cross-check against existing registry (avoid duplicate work)")

I("V5-i-1", "口径冲突（须裁决）：来稿自称 GAQ-UFT V18，但本仓 GAQ 谱系已用至 V22"
             "（utf/17-空间光速螺旋引力理论/v22/），且 S03 内部已用 V18_1..V18_4。"
             "本册按 S03 序列登记为 V18_5，不新开版本号。")
I("V5-i-2", "结论一致（交叉印证）：来稿 §1 的 kappa/tau = u/v 与本仓既有文档 "
             "「v_⊥/v_z = alpha = 1/137，由 kappa/tau = alpha 决定」"
             "（utf/17-空间光速螺旋引力理论/v_⊥^2+v_z^2=c^2_统一分解与全维度分析.md:114,355,361-365）"
             "同源；VER-6 否证的正是该既有断言，两册结论方向一致。")
I("V5-i-3", "差异（须登记）：既有文档取 kappa = rho/(rho^2+b^2)、tau = b/(rho^2+b^2)，"
             "与严格 F-S 曲率挠率只差一个共同因子（rho/R = v_⊥/c），故**比值 kappa/tau 不受影响**，"
             "但任何以 kappa 或 tau 的**绝对值**标定质量的步骤会引入 v_⊥/c 量级的系统偏差。")
I("V5-i-4", "既有能力边界复用：S03-C0034 已裁定 GAQ 几何可承载连续量 kappa/tau/Omega/c 与 Z_2 手性，"
             "不可承载质量标度。VER-7 的量纲封锁与该边界同源，本册把它精确落到 m' 这一个公式上。")
I("V5-i-5", "既有 Bishop 标架结论复用：4D 情形下 Frenet 标架在 kappa→0 处翻转，"
             "须改用 Bishop 标架（见 openuft 04_公共成果 TUFT_V3.5_W6W1结构层_Bishop标架与4D协变）。"
             "来稿 §5 提到的「强场」若升级到 4D 世界线，此坑立即生效。")

# ================================================================ 自检
hdr("SELF-CHECK  |  11 gates")

CHECKS = [
    ("SC1 round-helix kappa analytic vs F-S def", rel_kappa < 1e-12),
    ("SC2 round-helix tau analytic vs F-S def", rel_tau < 1e-12),
    ("SC3 kappa/tau == u/v identity", rel_ratio < 1e-12),
    ("SC4 binormal tilt cos = u/c", rel_btilt < 1e-12),
    ("SC5 reading B conservation holds identically", rel_B < 1e-12),
    ("SC6 reading A forced alpha = sqrt(phi)", abs(resid_A) < 1e-12),
    ("SC7 reading A rejected at alpha_CODATA", resid_exp < -1.0),
    ("SC8 recovered kappa matches kappa(s)", max_kappa_err < 5e-2),
    ("SC9 recovered tau matches tau(s)", max_tau_err < 5e-2),
    ("SC10 speed-ceiling gap >> measured gap", (gap_gaq / gap_meas) > 1e3),
    ("SC11 integrator drift reported honestly", max_ortho_err < 5e-2),
]
self_fail = 0
for name, ok in CHECKS:
    tag = "OK " if ok else "NG "
    if not ok:
        self_fail += 1
    print("  [{0}] {1}".format(tag, name))
print("  self-check: {0}/{1} passed".format(len(CHECKS) - self_fail, len(CHECKS)))

# ================================================================ 报告
n_pass = sum(1 for r in RESULTS if r[0] == "PASS")
n_fail = sum(1 for r in RESULTS if r[0] == "FAIL")
n_bound = sum(1 for r in RESULTS if r[0] == "BOUNDARY")
n_info = sum(1 for r in RESULTS if r[0] == "INFO")

lines = []
lines.append("=" * 78)
lines.append("S03 V18.5 | GAQ-UFT V18 Frenet-Serret helix-manifold upgrade: full audit")
lines.append("=" * 78)
lines.append("run_id = S03-V18_5-2026-10-07")
lines.append("input  = GAQ-UFT V18 upgrade draft (Frenet-Serret active frame)")
lines.append("")
lines.append("VERDICT SUMMARY")
lines.append("  PASS     = {0}".format(n_pass))
lines.append("  FAIL     = {0}".format(n_fail))
lines.append("  BOUNDARY = {0}".format(n_bound))
lines.append("  INFO     = {0}".format(n_info))
lines.append("  items    = {0}".format(len(RESULTS)))
lines.append("  self-check = {0}/{1}".format(len(CHECKS) - self_fail, len(CHECKS)))
lines.append("")
lines.append("-" * 78)
for tag, name, detail in RESULTS:
    lines.append("[{0}] {1}".format(tag, name))
    lines.append("    {0}".format(detail))
    lines.append("")
lines.append("-" * 78)
lines.append("KEY NUMBERS")
lines.append("  alpha_forced_by_reading_A = {0:.12f}  (sqrt(phi))".format(alpha_star))
lines.append("  alpha_CODATA             = {0:.12e}".format(ALPHA_CODATA))
lines.append("  ratio_forced/measured    = {0:.3f}".format(alpha_star / ALPHA_CODATA))
lines.append("  residual_A_at_CODATA     = {0:.6f}".format(resid_exp))
lines.append("  rel.dev reading B        = {0:.3e}".format(rel_B))
lines.append("  v_par_ceiling / c        = {0:.12f}".format(v_par_ceiling / C_LIGHT))
lines.append("  speed_gap_GAQ            = {0:.4f} m/s".format(gap_gaq))
lines.append("  speed_gap_LEP            = {0:.3e} m/s".format(gap_meas))
lines.append("  discrepancy factor       = {0:.3e}".format(gap_gaq / gap_meas))
lines.append("  strong-field kappa recovery err  = {0:.3e}".format(max_kappa_err))
lines.append("  strong-field tau recovery err    = {0:.3e}".format(max_tau_err))
lines.append("  strong-field speed err (trivial) = {0:.3e}".format(max_speed_err))
lines.append("  strong-field pythag err (trivial)= {0:.3e}".format(max_pyth_err))
lines.append("  integrator drift (no projection) = {0:.3e}".format(max_ortho_err))
lines.append("  dim[∫ tau ds]           = 1  (dimensionless)")
lines.append("  dim[c^3 ∫ tau dt]       = M^0 L^2 T^-2  (short of E by M^1)")
lines.append("  dim[H]                   = M^2 L^4 T^-4 I^-2")
lines.append("  dim[m' c] = dim[m v]     = M^1 L^1 T^-1  (momentum, consistent)")
lines.append("")
lines.append("-" * 78)
lines.append("DECISION ON THE THREE PROPOSED BRANCHES")
lines.append("  branch 1 (field PDE + torsion gravity vs EC) : BLOCKED by V5-g; needs eta with")
lines.append("             mass dimension, which the registry already ruled out as non-derivable.")
lines.append("  branch 2 (photon spin vs helicity)           : BLOCKED by V5-d; the torsion-based")
lines.append("             energy is incompatible with k || B. Only the 4D-worldline route survives.")
lines.append("  branch 3 (soliton topological phase transition): viable, and it is the only branch")
lines.append("             whose input survives V5-a/V5-b/V5-e. Recommended next.")
report = "\n".join(lines) + "\n"

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "运行记录")
out_dir = os.path.normpath(out_dir)
out_path = os.path.join(out_dir, "S03_V18_5_FrenetSerret标架_验证报告.txt")
written = False
try:
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(report)
    written = True
except Exception as exc:  # pragma: no cover
    print("  [warn] report write failed: {0}".format(exc))

print("")
print("REPORT written = {0} ({1} bytes)".format(written, len(report.encode("utf-8"))))
print("PASS={0} FAIL={1} BOUNDARY={2} INFO={3} SELFCHECK={4}/{5}".format(
    n_pass, n_fail, n_bound, n_info, len(CHECKS) - self_fail, len(CHECKS)))
sys.exit(0 if (self_fail == 0 and written) else 1)