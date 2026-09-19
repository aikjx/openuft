# -*- coding: utf-8 -*-
"""
TUFT v8 线二：从 Skyrme-Faddeev 拉氏量严格推导 V(n) 是否自然产生 Starobinsky 平台
新方程 E296 起。三态判决 + 四态分级。纯数值精算。
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

print("="*74)
print("TUFT v8 线二：V(n) Starobinsky 平台存在性严格判决")
print("="*74)

# ============================================================
# E296: Skyrme 项在 FRW 均匀背景下的约化
# F_{mu nu} = n . (d_mu n x d_nu n)
# 均匀宇宙 n=n(t): d_i n = 0, d_0 n = ndot != 0
# F_{0i} = n.(ndot x d_i n) = 0  (因 d_i n=0)
# F_{ij} = n.(d_i n x d_j n) = 0
# => Skyrme 项在均匀背景下恒等于 0
# ============================================================
print("\n[E296] Skyrme 项 FRW 均匀背景约化")
print("-"*74)
# 数值验证：取任意 n(t) = (sin th(t) cos ph, sin th(t) sin ph, cos th(t))
# 均匀 => 空间导数全 0。构造一个具体构型算 F
th = lambda t: 0.5*t + 0.1
ph = 0.3
def n_of(t):
    return np.array([np.sin(th(t))*np.cos(ph), np.sin(th(t))*np.sin(ph), np.cos(th(t))])
def ndot_of(t):
    thd = 0.5
    return np.array([thd*np.cos(th(t))*np.cos(ph), thd*np.cos(th(t))*np.sin(ph), -thd*np.sin(th(t))])
# F_{0i} 含空间导数，均匀时空间导数=0
# 直接算 F_{mu nu} 的所有分量：只有 (0,0) 反对称=0，(0,i) 含 d_i n=0
# 显式算 F_{0i} = n.(ndot x d_i n); d_i n=0 => 叉乘=0
# 数值：若强行令 d_i n 为小扰动 eps，看 F 如何随 eps 消失
for eps in [0.0, 1e-3, 1e-1, 1.0]:
    d_i_n = eps * np.array([1.0,0.5,0.2])  # 模拟非均匀空间导数
    t = 0.3
    F0i = np.dot(n_of(t), np.cross(ndot_of(t), d_i_n))
    print(f"  非均匀度 d_i n~{eps:5.2e} 时  F_{{0i}} = {F0i:.3e}")
print("  => 严格均匀(d_i n=0): F_{mu nu} = 0 对所有 mu,nu")
print("  => Skyrme 项 (1/4e^2) F^2 在 FRW 背景下 = 0，不贡献有效势")
print("  => 均匀暴胀段只剩: L = 1/2 (d_n)^2 - V(n)  [纯 O(3) sigma 模型]")

# ============================================================
# E297: S^2 球坐标约化 -> 两个自由度
# n=(sin th cos phi_a, sin th sin phi_a, cos th)
# L_k = 1/2[(d th)^2 + sin^2 th (d phi_a)^2]
# ============================================================
print("\n[E297] S^2 球坐标约化")
print("-"*74)
print("  动能度规: ds^2 = d th^2 + sin^2 th d phi_a^2")
print("  方位角 phi_a 方向有效动能权重 = sin^2 th")
print("  极点 th=0,pi 处权重=0 (方位角退化)；赤道 th=pi/2 权重最大=1")
print("  结论: 这是 S^2 非线性 sigma 模型，两个自由度，无全局平直方位角")

# ============================================================
# E298: Starobinsky 平台系数 c=sqrt(2/3) 的真正来源
# 标准 Starobinsky 作用量 S = ∫√-g [ M_Pl^2 R/2 + R^2/(6 M^2) ]
# 共形变换 g_{\mu\nu} -> Omega^2 g_{\mu\nu}, Omega^2 = 1 + R/(3M^2)
# 引入标量 phi = sqrt(3/2) M_Pl ln(1 + R/(3M^2))
# 则 R = 3 M^2 ( e^{sqrt(2/3) phi/M_Pl} - 1 )
# 势 V(phi) = (3/4) M^2 M_Pl^2 (1 - e^{-sqrt(2/3) phi/M_Pl})^2
# 关键: sqrt(2/3) 来自 phi = sqrt(3/2) M_Pl ln(...) 的正则化
# ============================================================
print("\n[E298] sqrt(2/3) 系数的来源追溯")
print("-"*74)
print("  Starobinsky R^2 作用量: S = ∫√-g [ M_Pl^2 R/2 + R^2/(6 M^2) ]")
print("  辅助场正则化: phi = sqrt(3/2) M_Pl ln(1 + R/(3M^2))")
print("  => 势 = (3/4) M^2 M_Pl^2 [ 1 - exp(-sqrt(2/3) phi/M_Pl) ]^2")
c_star = np.sqrt(2.0/3.0)
print(f"  平台斜率系数 c = sqrt(2/3) = {c_star:.6f}")
print("  该系数 = sqrt(3/2) 的倒数，纯由 R^2 引力共形变换定出")
print("  在纯 O(3) sigma 模型(E83 均匀约化)中无任何量给出 sqrt(2/3)")
print("  => sqrt(2/3) 不是 n 场动力学的自然常数，是 R^2 引力内禀常数")

# ============================================================
# E299: 量纲核查——K(kappa,tau) 能否给出 R^2
# E20: S = ∫√-g [ R/(16πG) + 1/2(d phi)^2 + alpha K(kappa,tau) + V(n) ]
# [R]=E^2, [1/G]=E^2 => [R/G]=E^4 OK
# 挠率 kappa,tau 作为 1-form 几何量: [kappa]=E
# 若 K = (1/2) a kappa^2 (二阶 Taylor): [K]=E^2
# 要 alpha K 量纲 E^4 => [alpha]=E^2
# 若 kappa = beta R: [beta]=E^{-1} (因 [kappa]=E,[R]=E^2)
# K = (1/2)a beta^2 R^2, 系数 a beta^2 [R^2] 量纲 E^2*E^{-2}=无量纲
# alpha K = (alpha a beta^2/2) R^2, 系数量纲 E^2 * 无量纲 = E^2
# 但 R^2 项要求系数量纲 E^{-2} !!!  => 量纲不匹配
# ============================================================
print("\n[E299] 量纲核查: K(kappa,tau) -> R^2 是否量纲自洽")
print("-"*74)
print("  挠率 kappa [量纲]=E (1-form, 长度倒数)")
print("  若 K = (1/2) a kappa^2: [K]=E^2")
print("  E20 中 alpha K 须量纲 E^4 => [alpha]=E^2")
print("  若 kappa = beta R: [beta]=E^{-1}")
print("  有效 R^2 系数 = alpha a beta^2/2, 量纲 = E^2 * E^{-2} = 无量纲")
print("  但作用量 √-g [c R^2] 要求 [c] = E^{-2}")
print("  *** 量纲硬伤: 差了 E^4 量纲 ***")
print("  结论: 从 kappa 二次项无法自然给出量纲正确的 R^2 项")
print("        必须独立手加 √-g [ R^2/(6 M^2) ]，系数 1/(6M^2) 量纲 E^{-2}")

# ============================================================
# E300: 数值检验——Starobinsky scalaron 与观测对比
# 标准慢滚: V = V0 (1 - e^{-c phi})^2, V0=(3/4) M^2 M_Pl^2, c=sqrt(2/3)
# ============================================================
print("\n[E300] Starobinsky 慢滚数值检验 (N=60)")
print("-"*74)
c = np.sqrt(2.0/3.0)
def V(p):    return (1.0 - np.exp(-c*p))**2
def Vp(p):   return 2*c*(1-np.exp(-c*p))*np.exp(-c*p)
def Vpp(p):
    e = np.exp(-c*p); return 2*c*c*e*(2*e-1)
def Vppp(p):
    e = np.exp(-c*p); return 2*c**3*e*(1-4*e)

# eps=1 端点
def eps(p): return 0.5*(Vp(p)/V(p))**2
phi_end = brentq(lambda p: eps(p)-1.0, 0.05, 3.0, xtol=1e-12)
print(f"  phi_end (eps=1) = {phi_end:.4f} M_Pl")

# N 积分: N = ∫_{phi_end}^{phi_N} V/V' dphi
def efold(phi_N):
    val,_ = quad(lambda p: V(p)/Vp(p), phi_end, phi_N, limit=300)
    return val
phi_N60 = brentq(lambda p: efold(p)-60.0, phi_end*1.01, phi_end*1000, xtol=1e-10)
phi_N50 = brentq(lambda p: efold(p)-50.0, phi_end*1.01, phi_end*1000, xtol=1e-10)

for label, pN in [("N=50", phi_N50), ("N=60", phi_N60)]:
    e = eps(pN)
    et = Vpp(pN)/V(pN)
    xi2 = Vp(pN)*Vppp(pN)/V(pN)**2
    ns = 1 - 6*e + 2*et
    r  = 16*e
    print(f"  {label}: phi={pN:.4f}  eps={e:.5f}  eta={et:.5f}  n_s={ns:.5f}  r={r:.5f}")

# 标准 Starobinsky 解析公式: n_s=1-2/N, r=12/N^2
print(f"  解析 N=60: n_s=1-2/60={1-2/60:.5f}, r=12/3600={12/3600:.5f}")
print(f"  Planck 2018: n_s=0.9649±0.0042, r<0.036")

# ============================================================
# E301: R^2 系数 alpha_R 与 scalaron 质量 M 的量级
# 标量扰动幅度 A_s = V/(24 pi^2 eps M_Pl^4) = 2.1e-9
# Starobinsky 平台 V_inf = (3/4) M^2 M_Pl^2, eps_inf = 3/(4 N^2)
# => V_inf/(24 pi^2 eps M_Pl^4) = 2.1e-9
# ============================================================
print("\n[E301] R^2 系数与 scalaron 质量 M 的量级反推")
print("-"*74)
A_s = 2.1e-9
N = 60.0
# 平台处 V/V_inf -> 1, eps = 3/(4N^2)
eps_inf = 3.0/(4*N**2)
# A_s = V_inf/(24 pi^2 eps M_Pl^4) => V_inf/M_Pl^4 = 24 pi^2 eps A_s
V_inf_over_Mpl4 = 24*np.pi**2*eps_inf*A_s
print(f"  eps_inf = 3/(4N^2) = {eps_inf:.5e}")
print(f"  V_inf / M_Pl^4 = 24 pi^2 eps A_s = {V_inf_over_Mpl4:.3e}")
# Starobinsky: V_inf = (3/4) M^2 M_Pl^2 => M^2/M_Pl^2 = (4/3) V_inf_over_Mpl4
M_over_Mpl = np.sqrt((4.0/3.0)*V_inf_over_Mpl4)
print(f"  scalaron 质量 M/M_Pl = sqrt(4/3 * V_inf/M_Pl^4) = {M_over_Mpl:.3e}")
M_GeV = M_over_Mpl * 2.435e18
print(f"  scalaron 质量 M = {M_GeV:.2e} GeV")
# R^2 系数: S 中 R^2/(6M^2), 即 alpha_R = 1/(6 M^2)
alpha_R_GeV_inv2 = 1.0/(6.0*M_GeV**2)
print(f"  R^2 系数 alpha_R = 1/(6 M^2) = {alpha_R_GeV_inv2:.3e} GeV^-2")
print(f"  暴胀能标 V_inf^(1/4) = {(V_inf_over_Mpl4)**0.25 * 2.435e18:.2e} GeV")

# ============================================================
# E302: 三态判决
# ============================================================
print("\n" + "="*74)
print("[E302] 三态判决")
print("="*74)
print("""
  问题: 从 E83 Skyrme-Faddeev 拉氏量, 能否自然导出 Starobinsky 平台?

  链条审计:
  (1) FRW 均匀背景下 Skyrme 项 F_{mu nu}=0  [E296]
      => 只剩纯 O(3) sigma 模型 1/2(d n)^2 - V(n)
  (2) S^2 约化给出两个自由度, 方位角方向权重 sin^2 th, 非全局平直 [E297]
  (3) 平台斜率 sqrt(2/3) 来自 R^2 引力共形变换, 非 sigma 模型常数 [E298]
  (4) 量纲核查: K(kappa,tau) 二阶展开无法给出量纲正确的 R^2 项 [E299]
      => 必须独立手加 R^2/(6M^2)
  (5) 加 R^2 后: n_s=0.968, r=0.003, M~10^13 GeV, 与 Planck 一致 [E300/E301]

  判决: 【需 1 个新公设】
    - 不是 CLOSED: 平台不来自 E83 物质拉氏量, sqrt(2/3) 不自然出现
    - 不是 否决:   手加 R^2 后方案成立且数据吻合
    - 是 需 1 新公设: 独立引入 √-g [ R^2/(6 M^2) ], scalaron 质量 M~10^13 GeV
      这是 TUFT 已有公理 (E83 物质 + E20 引力) 之外的第 N+1 项引力修正
""")

# ============================================================
# E303: 四态分级
# ============================================================
print("="*74)
print("[E303] 四态分级")
print("="*74)
print("""
  CLOSED   : 从 E83 自然导出 .................... [不满足]
  LIKELY   : 手加 R^2 后数据吻合, 参数 M~10^13 GeV [本方案]
  OPEN     : K(kappa,tau) 能否代替 R^2 仍未证
  REJECTED : 纯 E83 sigma 模型直接出平台 ........ [不满足, 量纲硬伤]

  最终分级: A3 平台 = LIKELY (升级为"条件性 CLOSED", 条件=接受 R^2 公设)
            严禁标纯 CLOSED (禁止伪闭合)
""")

print("="*74)
print("v8 线二 判决完成")
print("="*74)
