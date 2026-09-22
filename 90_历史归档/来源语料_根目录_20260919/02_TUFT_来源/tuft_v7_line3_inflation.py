# -*- coding: utf-8 -*-
"""
TUFT v7 线三：暴胀嵌入候选扫描
E256 起，慢滚参数 + Planck 2018 对比 + reheating 兼容性
纯数值精算，四态分级：CLOSED / LIKELY / OPEN / REJECTED
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ============================================================
# 物理常数（自然单位 M_Pl = 1）
# ============================================================
Mpl = 1.0
Mpl_MeV = 2.435e18          # 约化 Planck 质量 [MeV]
m_Hubble0_MeV = 1.5e-33     # 今日哈勃 [MeV] ~ H0
g_star = 106.75             # SM 相对论自由度
T_BBN_MeV = 4.0             # BBN 下限 [MeV]（保守值）

# Planck 2018 (TT,TE,EE+lowE+lensing+BK15)
PLANCK_ns = 0.9649
PLANCK_ns_err = 0.0042
PLANCK_r_max = 0.036        # 95% CL 上限
PLANCK_alpha = -0.0045      # 典型中心值（跑动，弱约束）

print("="*72)
print("TUFT v7 线三：暴胀嵌入候选扫描")
print("="*72)

# ============================================================
# 慢滚工具函数
# ============================================================
def slow_roll(V, Vp, Vpp, Vppp, phi):
    """返回 eps, eta, xi2 at phi（M_Pl=1）"""
    eps = 0.5 * (Vp(phi)/V(phi))**2
    eta = Vpp(phi)/V(phi)
    xi2 = Vp(phi)*Vppp(phi)/(V(phi)**2)  # M_Pl^4 * V'V'''/V^2
    return eps, eta, xi2

def efold_integrand(phi, V, Vp):
    """dN/dphi = V/(M_Pl^2 V')  (慢滚近似，从 phi_end 到 phi)"""
    return V(phi)/Vp(phi)  # M_Pl=1

def find_phifor_N(V, Vp, phi_end, N_target):
    """从 phi_end（eps=1）出发，反推 N_target e-folds 前的场值"""
    # 积分从 phi_end 到 phi，要求 N = ∫ V/V' dphi = N_target
    # 由于 phi 从 phi_big 滚到 phi_end，N = ∫_{phi_end}^{phi_big} V/V' dphi
    def f(phi_guess):
        # 积分方向：从 phi_end 到 phi_guess
        val, _ = quad(lambda p: efold_integrand(p, V, Vp), phi_end, phi_guess, limit=200)
        return val - N_target
    # 估计 phi_guess 范围
    # 先试一个大范围
    lo, hi = phi_end, phi_end * 100
    # 如果 f(hi) < 0，需要更大
    for scale in [10, 100, 1000, 1e4, 1e5, 1e6]:
        try:
            if f(phi_end*scale) > 0:
                lo = phi_end
                hi = phi_end*scale
                break
        except Exception:
            continue
    else:
        return None
    try:
        return brentq(f, lo, hi, xtol=1e-10, maxiter=500)
    except Exception:
        return None

def ns_r_alpha(eps, eta, xi2):
    ns = 1.0 - 6.0*eps + 2.0*eta
    r = 16.0*eps
    # alpha_s = dn_s/dlnk = -24 eps^2 + 16 eps eta - 2 xi^2
    alpha = -24.0*eps**2 + 16.0*eps*eta - 2.0*xi2
    return ns, r, alpha

# ============================================================
# 方案 A：n 场真空极化（早期 n 场缓慢滚过 V(n) 平坦方向）
# 扫描多种势形
# ============================================================
print("\n" + "="*72)
print("【方案 A】n 场真空极化：早期 n 场缓慢滚过 V(n) 平坦方向")
print("="*72)

# --- A1: 二次型混沌 V = 1/2 m^2 phi^2 ---
print("\n--- A1: 二次型混沌 V=(1/2)m^2 phi^2 ---")
def V_a1(p): return 0.5*p**2
def Vp_a1(p): return p
def Vpp_a1(p): return np.ones_like(p) if hasattr(p,'__len__') else 1.0
def Vppp_a1(p): return np.zeros_like(p) if hasattr(p,'__len__') else 0.0

# eps = (1/2)(1/phi)^2 * ... 实际: V'/V = 1/phi, eps = 1/(2 phi^2)
# eps=1 => phi_end = 1/sqrt(2)
phi_end_a1 = 1.0/np.sqrt(2.0)
for Nt in [50, 60]:
    phi_N = find_phifor_N(V_a1, Vp_a1, phi_end_a1, Nt)
    eps, eta, xi2 = slow_roll(V_a1, Vp_a1, Vpp_a1, Vppp_a1, phi_N)
    ns, r, alpha = ns_r_alpha(eps, eta, xi2)
    print(f"  N={Nt:2d}: phi={phi_N:.4f}  eps={eps:.5f}  eta={eta:.5f}  "
          f"n_s={ns:.5f}  r={r:.5f}  alpha_s={alpha:.6f}")

# --- A2: 四次型 V = lambda phi^4 ---
print("\n--- A2: 四次型混沌 V=lambda phi^4 ---")
def V_a2(p): return p**4
def Vp_a2(p): return 4*p**3
def Vpp_a2(p): return 12*p**2
def Vppp_a2(p): return 24*p
# eps = 0.5*(4/phi)^2 = 8/phi^2 => phi_end = sqrt(8)
phi_end_a2 = np.sqrt(8.0)
for Nt in [50, 60]:
    phi_N = find_phifor_N(V_a2, Vp_a2, phi_end_a2, Nt)
    eps, eta, xi2 = slow_roll(V_a2, Vp_a2, Vpp_a2, Vppp_a2, phi_N)
    ns, r, alpha = ns_r_alpha(eps, eta, xi2)
    print(f"  N={Nt:2d}: phi={phi_N:.4f}  eps={eps:.5f}  eta={eta:.5f}  "
          f"n_s={ns:.5f}  r={r:.5f}  alpha_s={alpha:.6f}")

# --- A3: 平台型（Starobinsky R^2 类）V = L^4(1 - e^{-c phi})^2 ---
print("\n--- A3: 平台型 Starobinsky 类 V=L^4(1-e^{-c phi})^2, c=sqrt(2/3) ---")
c_star = np.sqrt(2.0/3.0)
def V_a3(p): return (1.0 - np.exp(-c_star*p))**2
def Vp_a3(p):
    return 2*c_star*(1-np.exp(-c_star*p))*np.exp(-c_star*p)
def Vpp_a3(p):
    e = np.exp(-c_star*p)
    return 2*c_star**2*e*(2*e - 1)
def Vppp_a3(p):
    e = np.exp(-c_star*p)
    return 2*c_star**3*e*(1 - 4*e)
# 找 phi_end (eps=1)
def eps_a3(p):
    return 0.5*(Vp_a3(p)/V_a3(p))**2
# 数值找 eps=1
from scipy.optimize import brentq as _bq
# 小 p 时 V~L^4 c^2 p^2, 大 p 时 V~L^4, V'~2c L^4 e^{-cp} -> eps->0
# eps=1 在 p 较小处
try:
    phi_end_a3 = _bq(lambda p: eps_a3(p)-1.0, 0.05, 3.0, xtol=1e-10)
except Exception:
    phi_end_a3 = 0.27
print(f"  phi_end (eps=1) = {phi_end_a3:.4f}")
for Nt in [50, 60]:
    phi_N = find_phifor_N(V_a3, Vp_a3, phi_end_a3, Nt)
    if phi_N is None:
        print(f"  N={Nt}: 积分失败")
        continue
    eps, eta, xi2 = slow_roll(V_a3, Vp_a3, Vpp_a3, Vppp_a3, phi_N)
    ns, r, alpha = ns_r_alpha(eps, eta, xi2)
    print(f"  N={Nt:2d}: phi={phi_N:.4f}  eps={eps:.5f}  eta={eta:.5f}  "
          f"n_s={ns:.5f}  r={r:.5f}  alpha_s={alpha:.6f}")

# --- A4: 山顶型 V = V0(1 - (phi/mu)^2)^2  (场从山顶 phi~0 滚向 phi=mu)
print("\n--- A4: 山顶型 V=V0(1-(phi/mu)^2)^2, mu 扫描 ---")
print("  (V'<0, 场从 phi~0 滚向 phi=mu; N=∫ V/(-V') dphi)")
for mu_hill in [5.0, 10.0, 20.0, 50.0]:
    def V_a4(p, mu=mu_hill): return (1.0-(p/mu)**2)**2
    def Vp_a4(p, mu=mu_hill): return 2*(1-(p/mu)**2)*(-2*p/mu**2)
    def Vpp_a4(p, mu=mu_hill): return (-4/mu**2)*(1-3*(p/mu)**2)
    def Vppp_a4(p, mu=mu_hill): return 24*p/mu**4
    def eps_a4(p, mu=mu_hill): return 0.5*(Vp_a4(p,mu)/V_a4(p,mu))**2
    phi_end_a4 = _bq(lambda p: eps_a4(p)-1.0, 0.01, 0.99*mu_hill, xtol=1e-10)
    total_N,_ = quad(lambda p: V_a4(p)/(-Vp_a4(p)), 1e-10, phi_end_a4, limit=500)
    print(f"  mu={mu_hill:5.1f}: phi_end={phi_end_a4:.3f}, max_N={total_N:.1f}")
    for Nt in [60]:
        if Nt > total_N:
            print(f"    N={Nt}: 不可达")
            continue
        def f_a4(phi_N, mu=mu_hill, phi_end=phi_end_a4, Nt=Nt):
            val,_ = quad(lambda p: V_a4(p,mu)/(-Vp_a4(p,mu)), phi_N, phi_end, limit=500)
            return val - Nt
        try:
            phi_N = _bq(f_a4, 1e-10, phi_end_a4*0.9999, xtol=1e-12, maxiter=1000)
        except Exception:
            continue
        e = 0.5*(Vp_a4(phi_N)/V_a4(phi_N))**2
        et = Vpp_a4(phi_N)/V_a4(phi_N)
        xi = Vp_a4(phi_N)*Vppp_a4(phi_N)/V_a4(phi_N)**2
        ns, r, al = ns_r_alpha(e, et, xi)
        print(f"    N={Nt}: eps={e:.6f} eta={et:.6f} n_s={ns:.5f} r={r:.5f} alpha_s={al:.6f}")

# ============================================================
# 方案 B：ψ 场早期版本（与晚期 quintessence 同一 ψ？）
# 晚期 ψ: lambda=0.5 thawing quintessence
# 关键矛盾：同一标量既要早期暴胀（慢滚），又要晚期解冻（近冻结）
# ============================================================
print("\n" + "="*72)
print("【方案 B】ψ 场早期版本：与晚期 quintessence 同一 ψ？")
print("="*72)

# 晚期 quintessence 约束：m_psi ~ H0 ~ 1e-33 eV ~ 1e-39 MeV
# 今日 ψ 近冻结（thawing），势能曲率极小
# 若同一 ψ 驱动暴胀，则暴胀时 V(psi) 需 ~ 1e-10 M_Pl^4（GUT 量级）
# 但今日 V(psi) ~ V_DE ~ (2.3 meV)^4 ~ 1e-47 GeV^4
#
# 矛盾量化：
#   暴胀标度 V_inf^{1/4} ~ 1e16 GeV = 1e25 MeV
#   暗能量标度 V_DE^{1/4} ~ 2.3 meV = 2.3e-3 MeV
#   比值 V_inf / V_DE ~ (1e25 / 2.3e-3)^4 ~ (4.3e27)^4 ~ 3.5e111
# 单标量势必须在 psi 从 psi_inf 滚到 psi_0 时降低 ~10^111 倍
# 这要求 psi 位移 ~ M_Pl 且势极陡 -> 与慢滚矛盾

V_inf_quarter_MeV = 1.0e25   # 暴胀能标（约 GUT）
V_DE_quarter_MeV = 2.3e-3    # 暗能量能标 [MeV]
ratio_V = (V_inf_quarter_MeV/V_DE_quarter_MeV)**4
print(f"\n  暴胀能标 V_inf^(1/4) ~ {V_inf_quarter_MeV:.1e} MeV")
print(f"  暗能标度 V_DE^(1/4) ~ {V_DE_quarter_MeV:.1e} MeV")
print(f"  势高比 V_inf/V_DE ~ {ratio_V:.2e}")

# B1: 若 ψ 是线性势 V = V0 + m^2 psi^2/2（晚期 m~H0）
# 暴胀要求 eps = 0.5 (m^2 psi/V)^2 < 0.0023 (r<0.036)
# 但 m_psi ~ H0 -> 在暴胀尺度下 m 极小，势近平坦 -> eps 极小 -> r 极小（OK）
# 问题：暴胀结束后 ψ 滚到 psi=0（V=V0=0），但今日 V_DE 不为零
# 若 V0=0，则今日 V=0（除非 ψ 不在 0）-> 暗能量缺失
# 若 V0=V_DE，则暴胀能标 = V_DE（不可能，太低）

# 数值：假设 ψ 暴胀子是二次型但 m_psi 被晚期约束
# 晚期 m_psi ~ H0 / sqrt(2) ~ 1e-33 eV
# 暴胀时 phi_inf ~ sqrt(2N) M_Pl（二次型）
# V_inf = 0.5 m^2 phi^2 ~ 0.5 * (1e-33 eV)^2 * (M_Pl)^2
m_psi_eV = 1e-33  # 晚期 quintessence 质量
Mpl_eV = 2.4e27
V_inf_B_eV4 = 0.5 * (m_psi_eV)**2 * (np.sqrt(120.0)*Mpl_eV)**2
print(f"\n  B1: 若 m_psi~H0 驱动二次暴胀:")
print(f"      V_inf ~ {V_inf_B_eV4:.2e} eV^4 = {V_inf_B_eV4**0.25:.2e} eV = {V_inf_B_eV4**0.25*1e-9:.2e} GeV")
print(f"      (要求 V_inf^(1/4)~1e16 GeV = 1e25 eV)")
print(f"      -> 能标低 ~{1e25/(V_inf_B_eV4**0.25):.1e} 倍，不可能产生 CMB 扰动")

# B2: 自然暴胀势 V = L^4[1 + cos(psi/f)] 或 V = L^4(1-cos(psi/f))
# 若同一 ψ，f 需 < M_Pl 才能 r 大... 但晚期解冻要求 f >> M_Pl
# 自然暴胀 f~M_Pl, n_s~0.96, r~0.1(太大) 或 f>>M_Pl r<<0.036
# 晚期解冻：thawing quintessence 要求势极平（m~H0），与自然暴胀 f~M_Pl 不一致
# B2: 自然暴胀势 V = L^4(1-cos(psi/f))
# 慢滚: eps = 0.5(1/f^2)cot^2(x/2), eta = (1/f^2)cos(x)/(1-cos(x)), x=psi/f
# N = 2 f^2 [ln(cos(x_end/2)) - ln(cos(x_N/2))]
# eps_end=1: cot(x_end/2) = sqrt(2)*f => tan(x_end/2)=1/(sqrt(2)f)
print(f"\n  B2: 自然暴胀势 V=L^4(1-cos(psi/f)) 扫描:")
for f_val in [5.0, 10.0, 50.0, 100.0]:  # f/M_Pl
    Nt = 60
    tan_end = 1.0/(np.sqrt(2.0)*f_val)
    x_end_half = np.arctan(tan_end)
    cos_end_half = np.cos(x_end_half)
    # N = 2 f^2 [ln(cos_end_half) - ln(cos_N_half)]
    ln_cos_N_half = np.log(cos_end_half) - Nt/(2.0*f_val**2)
    if ln_cos_N_half >= 0:
        print(f"    f={f_val:.0f}Mpl: N=60 不可达")
        continue
    cos_N_half = np.exp(ln_cos_N_half)
    x_N_half = np.arccos(cos_N_half)
    x_N = 2.0*x_N_half
    eps_N = 0.5*(1.0/f_val**2)*(1.0/np.tan(x_N_half)**2)
    eta_N = (1.0/f_val**2)*np.cos(x_N)/(1.0-np.cos(x_N))
    xi2_N = 0.0
    ns, r, alpha = ns_r_alpha(eps_N, eta_N, xi2_N)
    print(f"    f={f_val:.0f}Mpl: eps={eps_N:.5f}  eta={eta_N:.5f}  "
          f"n_s={ns:.5f}  r={r:.5f}  alpha={alpha:.6f}")

# ============================================================
# 方案 C：常数 K=V(n0) 作为暴胀常数
# ============================================================
print("\n" + "="*72)
print("【方案 C】常数 K=V(n0) 作为暴胀常数（纯 de Sitter）")
print("="*72)
print("\n  V=K=const => V'=0, V''=0, V'''=0")
print("  eps=0, eta=0, xi2=0")
print("  n_s=1.0000, r=0.0000, alpha_s=0.0000")
print("  问题：纯 de Sitter 无 graceful exit，N 无穷大，暴胀永不结束")
print("  Planck: n_s=0.9649±0.0042 -> n_s=1.0 偏离 ~8.3 sigma（不可接受）")
print("  -> 无动力学退出机制，无法接入 reheating")

# ============================================================
# Reheating 兼容性
# ============================================================
print("\n" + "="*72)
print("【Reheating 兼容性分析】")
print("="*72)

# reheating 温度公式: T_rh = (90/(8 pi^3 g_*))^{1/4} sqrt(Gamma M_Pl)
# Gamma ~ inflaton 衰变率
# 引力衰变: Gamma ~ m^3 / M_Pl
# 规范耦合衰变: Gamma ~ alpha m
prefactor = (90.0/(8.0*np.pi**3*g_star))**0.25
print(f"\n  T_rh = {prefactor:.4f} * sqrt(Gamma * M_Pl)")
print(f"  BBN 下限: T_rh > {T_BBN_MeV} MeV")

# 对各方案估计 reheating 温度
# 假设 inflaton 质量 m_inf ~ sqrt(V_inf)/M_Pl
# A1 二次型: m ~ sqrt(V_inf)/phi_inf, V_inf^(1/4)~1e16 GeV
# A3 平台型: m ~ 1e13 GeV (Starobinsky)
# A4 山顶型: 取决于 V0

# 引力衰变 T_rh
print("\n  --- 引力衰变 Gamma ~ m^3/M_Pl ---")
for label, m_inf_GeV in [("A1 二次型", 1e13), ("A3 平台型", 1e13), ("A4 山顶型", 1e12)]:
    # m_inf in GeV, M_Pl = 2.4e18 GeV
    m_inf_MeV = m_inf_GeV*1e3
    Mpl_MeV = 2.435e21  # 约化 M_Pl in MeV (2.435e18 GeV = 2.435e21 MeV)
    Gamma_MeV = (m_inf_MeV**3)/Mpl_MeV  # 引力衰变率 [MeV]
    T_rh_MeV = prefactor*np.sqrt(Gamma_MeV*Mpl_MeV)
    ok = "OK" if T_rh_MeV > T_BBN_MeV else "FAIL"
    print(f"  {label}: m~{m_inf_GeV:.0e} GeV, T_rh~{T_rh_MeV:.3e} MeV [{ok}]")

# 规范耦合衰变 T_rh（Gamma ~ alpha m）
print("\n  --- 规范耦合衰变 Gamma ~ alpha m (alpha~1e-2) ---")
for label, m_inf_GeV in [("A1 二次型", 1e13), ("A3 平台型", 1e13), ("A4 山顶型", 1e12)]:
    m_inf_MeV = m_inf_GeV*1e3
    Mpl_MeV = 2.435e21
    alpha = 1e-2
    Gamma_MeV = alpha*m_inf_MeV
    T_rh_MeV = prefactor*np.sqrt(Gamma_MeV*Mpl_MeV)
    ok = "OK" if T_rh_MeV > T_BBN_MeV else "FAIL"
    print(f"  {label}: m~{m_inf_GeV:.0e} GeV, T_rh~{T_rh_MeV:.3e} MeV [{ok}]")

# ============================================================
# 辐射主导接入（E41/E42: 辐射期 u/H=3）
# ============================================================
print("\n  --- 辐射主导接入（E42: u/H=3）---")
print("  暴胀结束 -> reheating -> 辐射主导(u/H=3)")
print("  要求 reheating 后宇宙以辐射为主，能量密度 rho_rad ~ T^4")
print("  接入条件: T_rh 时 rho_rad 主导，物质分量可忽略")
print("  若 T_rh > BBN 下限且 reheating 瞬时完成，则平滑接入 E42")

# ============================================================
# Planck 2018 对比汇总
# ============================================================
print("\n" + "="*72)
print("【Planck 2018 对比汇总】")
print("="*72)
print(f"  Planck 2018: n_s={PLANCK_ns}±{PLANCK_ns_err}, r<{PLANCK_r_max}, alpha_s~{PLANCK_alpha}")
print()

# 汇总表（用实际计算值）
results = [
    ("A1 二次型 N=60",       0.96674, 0.13306, -0.000553),
    ("A2 四次型 N=60",       0.95082, 0.26230, -0.000806),
    ("A3 平台Star N=60",     0.96783, 0.00296, -0.000523),
    ("A4 山顶 mu=20 N=60",   0.96420, 0.05186, -0.000454),
    ("B1 同ψ二次型",          None,    None,    None),
    ("B2 自然f=5 N=60",      0.95219, 0.03124, -0.000655),
    ("B2 自然f=10 N=60",     0.96594, 0.09624, -0.000771),
    ("B2 自然f=50 N=60",     0.96694, 0.13064, -0.000559),
    ("C 常数K",              1.00000, 0.00000,  0.000000),
]
print(f"  {'方案':<22s} {'n_s':>8s} {'r':>8s} {'alpha_s':>10s}  判定")
print("  "+"-"*66)
for name, ns, r, al in results:
    if ns is None:
        print(f"  {name:<22s} {'N/A':>8s} {'N/A':>8s} {'N/A':>10s}  能标不足")
        continue
    # n_s 检验
    ns_dev = abs(ns - PLANCK_ns)/PLANCK_ns_err
    ns_ok = ns_dev < 2.0
    # r 检验
    r_ok = r < PLANCK_r_max
    # alpha 检验（粗略）
    al_ok = abs(al - PLANCK_alpha) < 0.01
    grade = "PASS" if (ns_ok and r_ok) else ("PARTIAL" if (ns_ok or r_ok) else "FAIL")
    print(f"  {name:<22s} {ns:8.4f} {r:8.4f} {al:10.5f}  {grade} (ns_dev={ns_dev:.1f}sig)")

# ============================================================
# 四态分级
# ============================================================
print("\n" + "="*72)
print("【四态分级】")
print("="*72)
print("""
  CLOSED  = 已被 TUFT 内部机制完全解释且数据吻合
  LIKELY  = 候选可行但需微调
  OPEN    = 存在未解决矛盾，需外部输入
  REJECTED= 明确被 Planck 数据或逻辑排除

  方案 A1 (二次型):   n_s=0.967 OK, r=0.133 FAIL(>0.036)    -> REJECTED
  方案 A2 (四次型):   n_s=0.951 FAIL, r=0.262 FAIL           -> REJECTED
  方案 A3 (平台型):   n_s=0.968 OK, r=0.003 OK              -> LIKELY
  方案 A4 (山顶型):   mu=20: n_s=0.964 OK, r=0.052 BORDER   -> OPEN (n_s/r 不可兼得)
  方案 B1 (同ψ二次):  能标低 10^27 倍                       -> REJECTED
  方案 B2 (自然暴胀): f=5: n_s=0.952 偏; f>=10: r>=0.096    -> REJECTED
  方案 C  (常数K):    n_s=1.0 偏离8σ, 无 graceful exit      -> REJECTED

  结论：TUFT 内部仅 A3（n 场平台方向）通过 Planck 检验
        其余方案需外部暴胀子或额外自由度
""")

# ============================================================
# 新方程 E256-E265
# ============================================================
print("="*72)
print("【新方程 E256-E265】")
print("="*72)
print("""
E256: eps  = (M_Pl^2/2)(V'/V)^2                         [慢滚一阶]
E257: eta  = M_Pl^2 (V''/V)                             [慢滚二阶]
E258: xi^2 = M_Pl^4 (V'V'''/V^2)                        [慢滚三阶]
E259: N    = (1/M_Pl^2) ∫_{phi_end}^{phi} (V/V') dphi   [e-fold 数]
E260: n_s  = 1 - 6eps + 2eta                           [标量谱指数]
E261: r    = 16 eps                                     [张量-标量比]
E262: alpha_s = dn_s/dlnk = -24eps^2 + 16eps eta - 2xi^2 [跑动]
E263: phi_end 由 eps=1 确定                             [暴胀结束]
E264: T_rh = (90/(8π^3 g_*))^{1/4} sqrt(Γ M_Pl)        [reheating 温度]
E265: T_rh > 4 MeV 且 rho_rad 主导 => 接入 E42(u/H=3)  [兼容性判据]
""")

print("="*72)
print("扫描完成")
print("="*72)
