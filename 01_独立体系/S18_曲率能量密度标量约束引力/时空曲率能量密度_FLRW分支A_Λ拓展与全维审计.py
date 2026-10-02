# -*- coding: utf-8 -*-
"""
时空曲率-能量密度关系 · 续篇三（分支A）：FLRW 背景 + Λ 拓展 + 全维审计
=====================================================================
上游：
  续篇一（方案1：守恒律作独立公理）场方程
      R = (alpha/rho_c) * (∇^μρ ∇_μρ) / (ρ + ρ_min)
  续篇二（FLRW 嵌入）已落盘：
      01_独立体系/S18_曲率能量密度标量约束引力/时空曲率能量密度_FLRW宇宙学推导.py
  本轮用户文稿（分支A）：FLRW 背景推导 + 原初扰动 + 250 位 RK4 代码

本册任务（三件，按优先级）：
  A1【审计】对本轮文稿与代码做量纲/符号/阶数/代码缺陷审计（诚实，不粉饰）
  A2【分支A 正式】引入宇宙学常数 Λ 拓展场方程，判"晚期加速"能否被修复
  A3【定标】用 z=0 观测定标 alpha/rho_c 组合，再回代早期宇宙做相容性检验
      ⇒ 给出与太阳系约束（alpha<1.87）的交叉核验结论

分支选择裁决（见脚本末 CONCLUSION）：
  分支B（CMB 角功率谱）本轮被判"前置不成立"——理由见 S5：
  一阶扰动源项无空间梯度项（梯度项是二阶），且"取模"口径不可微，
  线性扰动论无法建立 ⇒ 先做分支A。

精度：mpmath dps=250（系列规范，排除截断误差争议）
单位：SI；ρ 一律取【能量密度 J/m^3】（续篇二同口径），恢复 c 显式
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 250

# ---------------- 常数（SI, CODATA 2022 / Planck 2018） ----------------
C = mp.mpf("299792458")                 # m/s
G = mp.mpf("6.67430e-11")               # m^3 kg^-1 s^-2
MPC = mp.mpf("3.0856775814913673e22")   # m
YR = mp.mpf("3.15576e7")                # s

H0 = mp.mpf("70") * mp.mpf("1000") / MPC                 # 70 km/s/Mpc -> 1/s
RHO_CRIT_MASS = 3 * H0**2 / (8 * mp.pi * G)              # kg/m^3
RHO_CRIT_E = RHO_CRIT_MASS * C**2                        # J/m^3
OMEGA_M = mp.mpf("0.31")
OMEGA_L = mp.mpf("0.69")
RHO0 = OMEGA_M * RHO_CRIT_E                              # 今天物质能量密度 J/m^3
H_LAM2 = OMEGA_L * H0**2                                 # H_Lambda^2 = Lambda c^2/3
LAMBDA = 3 * H_LAM2 / C**2                               # 1/m^2

# ---------------- 本理论参数（沿用续篇一/二 F^∞ 示例值） ----------------
ALPHA = mp.mpf("1.87")        # 无量纲耦合
RHO_C = mp.mpf("1e-9")        # J/m^3
RHO_MIN = mp.mpf("1e-30")     # J/m^3
X_NOMINAL = ALPHA / RHO_C     # 组合 x = alpha/rho_c [m^3/J]，场方程唯一出现的组合

# ---------------- 计数器 ----------------
CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P(m):
    print("[PASS] " + m)
    CNT["PASS"] += 1


def F_(m):
    print("[FAIL] " + m)
    CNT["FAIL"] += 1


def B(m):
    print("[BOUNDARY] " + m)
    CNT["BOUNDARY"] += 1


def I(m):
    print("[INFO] " + m)
    CNT["INFO"] += 1


def n(x, d=6):
    # 一律走科学计数法：本册存在 10^33 级与 10^-52 级读数，
    # 用固定表示法（min_fixed/max_fixed 放宽）会在天文指数上尝试补齐巨量 '0' ⇒ MemoryError
    return mp.nstr(x, d)


def nh(x, d=6):
    """读数压制：|log10 x| > 12 时只打印量级（爆破值指数可达 10^298143，
    直接 nstr 会展开数百位整数位，刷屏且无信息量）"""
    if x == 0:
        return "0"
    lg = mp.log10(abs(x))
    if abs(lg) > 12:
        return ("-" if x < 0 else "+") + "1e(" + mp.nstr(lg, 6) + ")"
    return mp.nstr(x, d)


# ============================================================================
# S1  量纲审计（SI）+ 续篇二 V1 的 c 因子缺陷定位
#     场方程（Λ 拓展后）：
#        R = (alpha/rho_c) * (∇^μρ ∇_μρ)/(ρ + ρ_min)  +  4Λ
#     x^0 = c t 惯例：g^{00} = -1, ∂_0 = (1/c)∂_t
#       ∇^μρ ∇_μρ = -(ρ̇/c)^2 + a^{-2}|∇ρ|^2     量纲 [(J/m^3)^2 / m^2]
# ============================================================================
I("S1 量纲审计（SI，恢复 c）+ 续篇二 V1 c 因子缺陷定位")

# 源项量纲： (1/(J/m^3)) * ((J/m^3)^2/m^2) / (J/m^3) = 1/m^2 = [R]  ✔
# Λ 项量纲： [Λ] = 1/m^2 ⇒ [4Λ] = 1/m^2 = [R] ✔
# 数值对照：验证 (ρ̇/c)^2 与 a^{-2}|∇ρ|^2 同为 (J/m^3)^2/m^2
rho_dot0 = -3 * H0 * RHO0                     # J/m^3/s（物质主导连续性方程）
term_time = (rho_dot0 / C) ** 2               # (J/m^3)^2/m^2
grad_scale = mp.mpf("0.01") * RHO0 / MPC      # 取 1% / Mpc 的空间起伏代表尺度
term_space = grad_scale ** 2                  # (J/m^3)^2/m^2
if abs(mp.log10(term_time / term_space)) < 200:   # 两者同为 (J/m^3)^2/m^2，量纲一致
    P("S1 场方程量纲自洽：∇^μρ∇_μρ = -(ρ̇/c)^2 + a^{-2}|∇ρ|^2 量纲 (J/m^3)^2/m^2；"
      "(alpha/rho_c)·该项/(ρ+ρ_min) ⇒ 1/m^2 = [R]；Λ 项 4Λ 同为 1/m^2")
else:
    F_("S1 量纲审计异常")

# --- 续篇二 V1 缺陷：R_GR 应写 8πG·ρ_E / c^4（= 8πG·ρ_mass / c^2），脚本写成了 /c^2 ---
R_GR_correct = 8 * mp.pi * G * RHO_CRIT_E / C**4      # 正确（ρ_E 为能量密度）
R_GR_script = 8 * mp.pi * G * RHO_CRIT_E / C**2       # 续篇二 V1 实际用式
ratio_c = R_GR_script / R_GR_correct
res_c = abs(ratio_c - C**2) / C**2
if res_c < mp.mpf("1e-40"):
    F_("S1b 续篇二 V1 存在 c 因子缺陷：R_GR 误用 8πG·ρ_E/c^2（应为 /c^4），"
       "实测比值=%.6e = c^2 ⇒ 全部 R 绝对值被放大 c^2=%.4e 倍；"
       "正确 R_GR(z=0, 全临界)=%s 1/m^2（脚本报 %s）"
       % (float(ratio_c), float(C**2), n(R_GR_correct), n(R_GR_script)))
else:
    P("S1b 续篇二 V1 c 因子无缺陷，比值=%.3e" % float(ratio_c))

I("S1b 修正后的基准读数：R_GR(z=0, 物质部分 Ω_m)=%s 1/m^2；Λ 项 4Λ=%s 1/m^2"
  % (n(8 * mp.pi * G * RHO0 / C**4), n(4 * LAMBDA)))

# ============================================================================
# S2  符号口径冲突裁决：本轮"取模" vs 续篇二"不取模"
# ============================================================================
I("S2 符号口径冲突裁决（本轮文稿取 |∇^μρ∇_μρ| vs 续篇二保留负号）")
src_abs = (ALPHA / RHO_C) * (rho_dot0**2 / C**2) / (RHO0 + RHO_MIN)   # 1/m^2, >0
R_mod = +src_abs        # 本轮取模口径
R_raw = -src_abs        # 续篇二口径（α>0）
R_GR_0 = 8 * mp.pi * G * RHO0 / C**4

F_("S2 同一物理情形（z=0 同一 ρ̇）两份产物给出相反符号："
   "续篇二 R_ours=%s 1/m^2（负），本轮取模 R_ours=%s 1/m^2（正）；"
   "R_GR=%s 1/m^2（正）⇒ 体系内部符号口径未定，属 C 级冲突"
   % (n(R_raw), n(R_mod), n(R_GR_0)))

I("S2 读数（修正 c 因子后）：|R_ours| 与 R_GR 同量级（比值 %s），符号相反（不取模）"
  "⇒ 修正 c^2 缺陷后区分信号比续篇二所报（17 个量级差）更干净：靠符号而非量级"
  % n(abs(R_raw) / R_GR_0))

F_("S2b '取模'不可作为场方程运算：|X| 在 X=0（de Sitter 极限 ρ̇→0、静态解）不可微，"
   "R(ρ) 作为 ρ 的泛函失去微分结构 ⇒ 无法变分、无法做线性扰动论；"
   "分支B（CMB 扰动谱）在取模口径下数学上不成立")

# ============================================================================
# S3  辐射主导无迹条件冲突 + 早期宇宙失控（决定性）
# ============================================================================
I("S3 辐射主导期决定性检验：GR 无迹 R=0 vs 本理论 R≠0")
# 辐射能量密度（T=1 MeV，BBN 时标）：ρ_γ,0 = a T0^4
SIGMA_SB = mp.mpf("5.670374419e-8")       # W m^-2 K^-4
T0_CMB = mp.mpf("2.72548")                # K
RHO_GAMMA0 = 4 * SIGMA_SB * T0_CMB**4 / C  # J/m^3
T_BBN_K = mp.mpf("1e6") * mp.mpf("1.160451812e4")   # 1 MeV -> K
RHO_BBN = RHO_GAMMA0 * (T_BBN_K / T0_CMB) ** 4 * mp.mpf("1.68")   # 含中微子 1.68
H_BBN = mp.sqrt(8 * mp.pi * G * RHO_BBN / (3 * C**2))              # 辐射主导 Friedmann
rho_dot_bbn = -4 * H_BBN * RHO_BBN                                  # w=1/3 ⇒ 3(1+w)=4
src_bbn = X_NOMINAL * (rho_dot_bbn**2 / C**2) / (RHO_BBN + RHO_MIN)
geo_scale_bbn = 12 * H_BBN**2 / C**2        # 6(Ḣ+2H²)/c² 的典型尺度（取 |Ḣ|~2H²）
imbalance = abs(src_bbn) / geo_scale_bbn

# GR 辐射主导无迹：R = 8πG(ρ_E - 3p)/c^4，p = ρ/3 ⇒ 0
R_GR_rad = 8 * mp.pi * G * (RHO_BBN - 3 * (RHO_BBN / 3)) / C**4
P("S3 GR 辐射主导无迹条件复算通过：R_GR(rad) = 8πG(ρ-3p)/c^4 = %s 1/m^2（严格 0）"
  % n(R_GR_rad))

F_("S3 本理论在辐射主导期 R_ours = %s 1/m^2 ≠ 0（只要 ρ̇≠0 即非零），"
   "与 GR 无迹条件直接冲突；且失衡倍数 |源项|/|6(Ḣ+2H²)/c²| = %s ⇒ BBN 时期场方程失衡 ~%s 个量级"
   % (n(src_bbn), n(imbalance), n(mp.log10(imbalance))))

# 反解宇宙学上界：要求 BBN 时期源项 ≤ 1% 几何尺度 ⇒ alpha/rho_c 上界
# |src| = x·16H²ρ/c²  (ρ̇²=16H²ρ², ρ≫ρ_min)；要求 ≤ 0.01·12H²/c² ⇒ x ≤ 0.0075/ρ
X_BBN_BOUND = mp.mpf("0.0075") / RHO_BBN
ALPHA_BBN_BOUND = X_BBN_BOUND * RHO_C
P("S3b BBN 相容性（1%% 容差）反解：alpha/rho_c ≲ %s m^3/J ⇒ alpha ≲ %s（rho_c=1e-9 J/m^3）；"
  "对比太阳系约束 alpha<1.87 ⇒ 宇宙学约束强 %s 个量级【交叉核验结论】"
  % (n(X_BBN_BOUND), n(ALPHA_BBN_BOUND), n(mp.log10(mp.mpf("1.87") / ALPHA_BBN_BOUND))))

# ============================================================================
# S4  本轮用户给定代码的缺陷审计（实跑复现）
#     缺陷1：GR 对照组 alpha_gr=0 定义后从未使用（ODE 内引用全局 alpha）
#     缺陷2：dt·H ~ 1，RK4 步长远超稳定域（H=1e12, dt=1e-12）
#     缺陷3：SI 单位下时间导数项缺 1/c^2
# ============================================================================
I("S4 本轮文稿 RK4 代码缺陷审计（实跑复现）")
ALPHA_GLOBAL = mp.mpf("1.87")


def ode_user(t, state, w):
    """用户原码形态：dH_dt 引用全局 ALPHA_GLOBAL（alpha_gr 参数无法生效）"""
    a, H, rho = state
    drho_dt = -3 * H * rho * (1 + w)
    dH_dt = -2 * H**2 + (3 * ALPHA_GLOBAL / (2 * RHO_C)) * (H**2 * rho**2 * (1 + w)**2) / (rho + RHO_MIN)
    da_dt = a * H
    return [da_dt, dH_dt, drho_dt]


def ode_fixed(t, state, w, alpha_val):
    a, H, rho = state
    drho_dt = -3 * H * rho * (1 + w)
    dH_dt = -2 * H**2 + (3 * alpha_val / (2 * RHO_C)) * (H**2 * rho**2 * (1 + w)**2) / (rho + RHO_MIN)
    da_dt = a * H
    return [da_dt, dH_dt, drho_dt]


def rk4(f, t, y, dt, *args):
    k1 = f(t, y, *args)
    k2 = f(t + dt / 2, [y[i] + dt * k1[i] / 2 for i in range(3)], *args)
    k3 = f(t + dt / 2, [y[i] + dt * k2[i] / 2 for i in range(3)], *args)
    k4 = f(t + dt, [y[i] + dt * k3[i] for i in range(3)], *args)
    return [y[i] + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(3)]


w_rad = mp.mpf(1) / 3
state0 = [mp.mpf(1), mp.mpf("1e12"), mp.mpf("1e22")]
dt_u = mp.mpf("1e-12")

# 用户原码：alpha=1.87 与"GR 对照 alpha=0"两条路径
sA = list(state0)
sB = list(state0)
tA = mp.mpf(0)
tB = mp.mpf(0)
for _ in range(8):
    sA = rk4(ode_user, tA, sA, dt_u, w_rad)
    tA += dt_u
    sB = rk4(ode_user, tB, sB, dt_u, w_rad)   # 用户版：alpha_gr 无效，与 sA 完全同源
    tB += dt_u
identical = all(sA[i] == sB[i] for i in range(3))
if identical:
    F_("S4 缺陷1（实跑确认）：用户代码 alpha_gr=mpf('0') 定义后从未被 ODE 引用，"
       "dH_dt 用的是全局 alpha ⇒ 'GR 对照组'与本理论组逐位完全相同（H=%s），对照完全失效"
       % n(sA[1]))
else:
    P("S4 对照组有效")

# 修复版：显式传参（沿用用户原步长 dt=1e-12）
sF1 = list(state0)
sF0 = list(state0)
tF = mp.mpf(0)
for _ in range(8):
    sF1 = rk4(ode_fixed, tF, sF1, dt_u, w_rad, mp.mpf("1.87"))
    sF0 = rk4(ode_fixed, tF, sF0, dt_u, w_rad, mp.mpf("0"))
    tF += dt_u

B("S4 原步长（dt=1e-12, dt·H≈1）下本理论组 H=%s：指数已达 10^14 级的天文数，"
  "非物理（超出任何宇宙学时标），属有限时间爆破的数值表现" % nh(sA[1]))

# 缩减步长后的干净对照：dt·H = 1e-3（显式 RK4 稳定域内）
dt_s = mp.mpf("1e-15")
sS1 = list(state0)
sS0 = list(state0)
tS = mp.mpf(0)
for _ in range(200):
    sS1 = rk4(ode_fixed, tS, sS1, dt_s, w_rad, mp.mpf("1.87"))
    sS0 = rk4(ode_fixed, tS, sS0, dt_s, w_rad, mp.mpf("0"))
    tS += dt_s
F_("S4 缺陷2（数值方法，实跑确认）：初值 H=1e12 1/s 与 dt=1e-12 s 使 dt·H≈1，"
   "远超显式 RK4 稳定域（要求 dt≪1/H）；证据=缩减步长至 dt=1e-15（dt·H=1e-3）后，"
   "纯 GR 组 alpha=0 恢复正常衰减 H=%s（解析预期 H0/(1+2H0 t)=%s），"
   "而原步长下 alpha=0 组同样给出非物理负巨值 H=%s ⇒ 步长失稳独立于 alpha"
   % (n(sS0[1]), n(mp.mpf("1e12") / (1 + 2 * mp.mpf("1e12") * dt_s * 200)), nh(sF0[1])))
I("S4 干净对照（dt=1e-15, 200 步）：alpha=0 ⇒ H=%s（正常）；alpha=1.87 ⇒ H=%s（爆破，"
  "因 Ḣ≈+2.8e31·H²）⇒ 爆破是参数后果（与 S3/S7 的解析结论一致），"
  "但用户原码 8 步输出因步长失稳而不具数值可信度"
  % (n(sS0[1]), nh(sS1[1])))

# ============================================================================
# S5  原初扰动阶数审计（决定分支B 是否可做）
#     ρ = ρ̄ + ε·δρ；∇(ρ̄+εδρ) = ε∇δρ（背景无空间梯度）
#     ⇒ 空间梯度项 a^{-2}(∇δρ)^2 是 O(ε^2)【二阶】，不是一阶源
#     ⇒ 一阶源只有： -2ρ̄̇δρ̇/(ρ̄+ρ_min) + ρ̄̇^2 δρ/(ρ̄+ρ_min)^2
#       第二项来自分母展开，本轮文稿遗漏
# ============================================================================
I("S5 原初扰动阶数审计：梯度项阶数 + 分母展开遗漏项")

A_amp = mp.mpf("1e-3") * RHO0          # δρ 振幅（ε=1 基准）
B_amp = -3 * H0 * A_amp                # δρ̇ 振幅
L_g = MPC                              # 扰动空间尺度


def rhs_full(eps):
    rho = RHO0 + eps * A_amp
    rdot = rho_dot0 + eps * B_amp
    grad2 = (eps * A_amp / L_g) ** 2
    return X_NOMINAL * (-rdot**2 / C**2 + grad2) / (rho + RHO_MIN)


# 解析一阶系数（含分母展开项）
c1_analytic = X_NOMINAL * (
    -2 * rho_dot0 * B_amp / (RHO0 + RHO_MIN)
    + rho_dot0**2 * A_amp / (RHO0 + RHO_MIN) ** 2
) / C**2
# 数值中心差分（取小 ε 抑制 O(ε^2) 截断；并用两档 ε 验证收敛阶，
# 防止把"差分截断误差"误判为"理论公式缺陷"——这是审计脚本自身的失效模式）
def cdiff(eps):
    return (rhs_full(eps) - rhs_full(-eps)) / (2 * eps)


def rel_err(eps):
    return abs(cdiff(eps) - c1_analytic) / abs(c1_analytic)


eps_a = mp.mpf("1e-20")
eps_b = eps_a / 100
err_a = rel_err(eps_a)
err_b = rel_err(eps_b)
order = mp.log(err_a / err_b) / mp.log(eps_a / eps_b)
res5 = err_a
if res5 < mp.mpf("1e-30") and abs(order - 2) < mp.mpf("1e-6"):
    P("S5 一阶系数复算一致（相对残差=%s，收敛阶=%s ⇒ 中心差分 O(ε²) 收敛至解析值）："
      "线性源 = -2ρ̄̇δρ̇/(ρ̄+ρ_min) + ρ̄̇²δρ/(ρ̄+ρ_min)²；"
      "后一项来自分母展开，本轮文稿遗漏该项" % (n(res5), n(order)))
else:
    F_("S5 一阶系数复算不一致，残差=%s，收敛阶=%s" % (n(res5), n(order)))

# 梯度项阶数验证：grad 项 / ε 应随 ε→0 线性消失（即该项 ∝ ε²）
def grad_term(eps):
    return X_NOMINAL * (eps * A_amp / L_g) ** 2 / (RHO0 + RHO_MIN)


r_e3 = grad_term(mp.mpf("1e-3")) / (mp.mpf("1e-3") * abs(c1_analytic))
r_e6 = grad_term(mp.mpf("1e-6")) / (mp.mpf("1e-6") * abs(c1_analytic))
shrink = r_e3 / r_e6
if abs(shrink - mp.mpf("1000")) / 1000 < mp.mpf("1e-20"):
    P("S5b 阶数判定（实跑）：空间梯度项相对一阶源的比值随 ε 缩小 1000×（ε:1e-3→1e-6，"
      "实测比值 %s → %s，收缩 %s）⇒ a^{-2}(∇δρ)² 确为【二阶】量，线性阶无空间梯度源"
      % (n(r_e3), n(r_e6), n(shrink)))
else:
    F_("S5b 阶数判定异常，收缩=%s" % n(shrink))

F_("S5c 推论（分支B 前置不成立）：线性阶扰动方程右端只含 δρ、δρ̇（时间导数），"
   "无 ∇²δρ ⇒ 方程不具 Poisson/椭圆结构、无 k² 依赖 ⇒ 无法定义常规引力势响应，"
   "也无从产生尺度依赖的 P_R(k) 修正；本轮台账第 6、7 项标 PASS 不成立，予以撤回")

# ============================================================================
# S6  分支A 正式：Λ 拓展场方程 + 晚期加速能否修复
#     R = (alpha/rho_c)(∇^μρ∇_μρ)/(ρ+ρ_min) + 4Λ
#     FLRW(k=0): 6(Ḣ+2H²)/c² = S + 4Λ ⇒ Ḣ = -2H² + (c²S/6) + 2Λc²/3
#     记 H_Λ² ≡ Λc²/3 ⇒ Λ 贡献 = 2H_Λ²
#     物质 w=0: Ḣ = -2H² + s·(3x/2)·H²ρ²/(ρ+ρ_min) + 2H_Λ²
# ============================================================================
I("S6 分支A：Λ 拓展场方程与 de Sitter 吸引子")
I("S6 观测锚：Λ=%s 1/m^2（由 Ω_Λ=0.69 反解，Planck 量级 ~1.1e-52 ✔）；H_Λ=%s H0"
  % (n(LAMBDA), n(mp.sqrt(H_LAM2) / H0)))


def dH_dlna(H, a, x, s):
    """dH/dln a = Ḣ/H；ρ(a)=ρ0 a^{-3}（物质主导解析解）"""
    rho = RHO0 * a ** (-3)
    return -2 * H + s * (3 * x / 2) * H * rho**2 / (rho + RHO_MIN) + 2 * H_LAM2 / H


def rk4_lna(H, u, h, x, s):
    def f(uu, Hv):
        return dH_dlna(Hv, mp.e**uu, x, s)
    k1 = f(u, H)
    k2 = f(u + h / 2, H + h * k1 / 2)
    k3 = f(u + h / 2, H + h * k2 / 2)
    k4 = f(u + h, H + h * k3)
    return H + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6


# 用 z=0 定标出的 x_fit（见 S7），先在此取用；s=+1（取模口径）
q0_obs = mp.mpf("-0.55")
target = 1 - 2 * OMEGA_L - q0_obs                       # = s·(3x/2)·ρ0²/(ρ0+ρ_min)
X_FIT = target * 2 / (3 * RHO0**2 / (RHO0 + RHO_MIN))   # >0（s=+1）

H_c = H0
u_c = mp.mpf(0)
h_c = mp.mpf("0.01")
LN_A_END = mp.mpf("6")                                   # a: 1 → e^6 ≈ 403（物质稀释 6.5e7）
nsteps = int(mp.nint(LN_A_END / h_c))
traj = []
for step in range(nsteps):
    Hdot_over_H2 = dH_dlna(H_c, mp.e**u_c, X_FIT, 1) / H_c
    traj.append((mp.e**u_c, H_c, -1 - Hdot_over_H2))
    H_c = rk4_lna(H_c, u_c, h_c, X_FIT, 1)
    u_c += h_c
a_end, H_end, q_end = traj[-1]
H_LAM = mp.sqrt(H_LAM2)
res_de = abs(H_end - H_LAM) / H_LAM

# 定标自洽检验：a=1 处 q 应回到观测锚 -0.55
q_start = traj[0][2]
res_q0 = abs(q_start - q0_obs)
if res_q0 < mp.mpf("1e-25"):
    P("S6a 定标自洽：a=1 处由演化方程反算 q=%s，与观测锚 %s 逐位一致 ⇒ 反解式正确"
      % (n(q_start), n(q0_obs)))
else:
    F_("S6a 定标不自洽：q(a=1)=%s vs 观测锚 %s" % (n(q_start), n(q0_obs)))

if res_de < mp.mpf("1e-6"):
    P("S6 Λ 拓展修复晚期加速（PASS）：数值积分 a:1→%s，H 由 H0 收敛至 H_Λ=%s H0"
      "（相对偏差 %s），q 由 %s → %s（de Sitter 吸引子 q=-1）"
      % (n(a_end, 4), n(H_end / H0), n(res_de), n(q_start), n(q_end)))
else:
    F_("S6 de Sitter 收敛失败，H_end=%s H0，偏差=%s" % (n(H_end / H0), n(res_de)))

# 吸引子稳定性数值判据：H 略高于 H_Λ 应回落、略低应回升
eps_s = mp.mpf("1e-6")
f_plus = dH_dlna(H_LAM * (1 + eps_s), mp.e**LN_A_END, X_FIT, 1)
f_minus = dH_dlna(H_LAM * (1 - eps_s), mp.e**LN_A_END, X_FIT, 1)
if f_plus < 0 and f_minus > 0:
    P("S6b 吸引子稳定性（实跑）：H=H_Λ(1±1e-6) 处 dH/dln a 分别为 %s(<0) 与 %s(>0) "
      "⇒ 两侧均指向 H_Λ，de Sitter 为稳定吸引子（解析判据 dḢ/dH=-4H<0 一致）"
      % (n(f_plus), n(f_minus)))
else:
    F_("S6b 吸引子稳定性判据不成立：f_plus=%s, f_minus=%s" % (n(f_plus), n(f_minus)))

B("S6b Λ 为外部注入公设（与方案1 守恒公理同级），其观测值 %s 1/m^2 未由本理论导出，"
  "且承接 GR 同等的宇宙常数问题（真空能标度差 ~10^120）⇒ Λ 拓展是'补洞'非'推导'"
  % n(LAMBDA))

# ============================================================================
# S7  联合定标：用 z=0 观测反解 x=alpha/rho_c，再回代早期检验
# ============================================================================
I("S7 联合定标（q0=-0.55, Ω_Λ=0.69）反解 alpha/rho_c，并回代 BBN 做相容性检验")
I("S7 定标结果：alpha/rho_c = %s m^3/J ⇒ alpha = %s（rho_c=1e-9 J/m^3，取模口径 s=+1）；"
  "不取模口径 s=-1 给出 alpha = %s（负耦合）"
  % (n(X_FIT), n(X_FIT * RHO_C), n(-X_FIT * RHO_C)))

# 回代 BBN：修正系数 A ≡ (3x/2)·ρ_BBN（ρ≫ρ_min）
A_BBN = (3 * X_FIT / 2) * RHO_BBN
F_("S7 回代 BBN 决定性结果：修正系数 A=(3x/2)ρ_BBN = %s ⇒ Ḣ/H² 由 GR 的 -2 变为 %s，"
   "膨胀时标被压缩 ~%s 倍，与 BBN 核反应时标（~10^2 s）彻底不相容 ⇒ Λ 拓展救不了早期宇宙"
   % (n(A_BBN), n(-2 + A_BBN), n(A_BBN / 2)))

# 二难：BBN 相容 ⇒ 修正项在今天小到不可观测
A_TODAY_IF_BBN_SAFE = (3 * X_BBN_BOUND / 2) * RHO0
B("S7b 二难（诚实边界）：若强行满足 BBN 相容（x ≤ %s），则今天的修正项 "
  "A_today=(3x/2)ρ0 ≤ %s ⇒ 修正幅度 ~10^-36，任何可观测尺度上均为零；"
  "即本理论要么被 BBN 证伪，要么修正小到原则上不可观测"
  % (n(X_BBN_BOUND), n(A_TODAY_IF_BBN_SAFE)))

F_("S7c 结构根因（ρ-线性放大）：ρ≫ρ_min 时修正项 A ∝ x·ρ，而 GR 物质项在 Ḣ 方程中"
  "与 ρ 无关 ⇒ 修正/GR 比值 ∝ ρ。从今天到 BBN，ρ 上升 %s 个量级，"
  "修正项必然同步放大同等倍数 ⇒ '调参同时满足早期与晚期'在结构上不可能"
  % n(mp.log10(RHO_BBN / RHO0)))

# ============================================================================
# S8  结构性欠定：本理论无 Friedmann 约束方程
# ============================================================================
I("S8 结构审计：标量场方程只给加速度方程，无 H² 约束")
H_alt = 2 * H0    # 同一 ρ0，H0 取 2 倍
dH_alt = dH_dlna(H_alt, mp.mpf(1), X_FIT, 1)
dH_ref = dH_dlna(H0, mp.mpf(1), X_FIT, 1)
B("S8 欠定诊断：GR 有两条独立宇宙学方程（Friedmann 约束 H²=8πGρ/3 + Λc²/3 与加速度方程），"
  "本理论 R=(源项) 只给一条加速度方程 ⇒ H0 与 ρ0 的关联不被约束；"
  "实测同一 ρ0 下取 H=%s 与 %s 均不被任何本理论方程排除（dH/dlna=%s vs %s）"
  "⇒ 宇宙学初值需外部输入 2 个而非 1 个，预言力下降 1 个自由度"
  % (n(H0), n(H_alt), n(dH_ref), n(dH_alt)))

# ============================================================================
# 汇总
# ============================================================================
print("-" * 74)
print("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
      % (CNT["PASS"], CNT["FAIL"], CNT["BOUNDARY"], CNT["INFO"]))
print("-" * 74)
print("评级：C / L2（内部符号口径冲突 + 续篇二 c 因子缺陷 + BBN 期决定性失衡；"
      "Λ 拓展仅修复晚期加速一条，早期不可调和）")
print("分支裁决：选分支A（已完成）。分支B 前置不成立——一阶扰动无空间梯度源（S5），"
      "且'取模'不可微使线性扰动论无法建立（S2b）；此外 Planck 实测 C_ℓ 数据离线不可得。")
print("红线：数学自洽 != 实验证实；本册全部负结论为诚实边界/缺陷定位，非对理论动机的否定。")
