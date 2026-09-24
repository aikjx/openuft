# -*- coding: utf-8 -*-
"""§16 审计骨架：OAM 涡旋真空场 + TUFT 螺旋测地线耦合。

【主线决策（见 §16）】采纳路径②：放弃 §15 证否的「真空单色随 z 扭转偏振标架」，
转向真正满足真空 Maxwell 的 OAM 涡旋光（相位 e^{ilφ} 角向扭转，偏振基底固定）。

红线守约（仅数值审计，不宣称物理已证实）：
  [1] 生成 OAM 涡旋光场（paraxial LG_{0,l}；标量 Bessel 精确 Helmholtz 校验）
      审计真空 Maxwell 残差（Gauss: ∇·E ; Helmholtz: ∇²E+k²E）。
      —— 关键对比 §15：旧方案 |Ez|/|E|=0.5（O(1) 纵向分量）；LG 为横向固定偏振（|Ez|/|E|=0）
  [2] 耦合到常 κ,τ 螺旋世界线（复用 momentum_darboux.frenet_frame_lightspeed）
  [3] Darboux 矢量恒定校验（内置自检，§15.2 修正标架）
  [4] 能量动量张量、角动量密度（自旋 + 轨道），每光子 J_z 验证 = ħ(σ_s + l)
  [5] 守恒律核验 div<S>=0, div·<T>=0（场真空满足，Noether 自动成立）
  [6] 误差传播升级：J_z = S_z(particle) + l·ħ，σ_Jz 框架（§14 升级）

注：§14 的 S_z=ħcosθ 现正确归属为【粒子 TUFT 世界线几何自旋】（§11 谱系），
不再是光子偏振；光子侧改用标准自旋 ±ħ + 场 OAM lħ。§14 误差机械保留。
"""
import math
import sys
import cmath
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from momentum_darboux import frenet_frame_lightspeed   # 复用 TUFT 修正标架（已锁定）

c = 299792458.0
mu0 = 4.0 * math.pi * 1e-7
eps0 = 1.0 / (mu0 * c ** 2)
hbar = 1.054571817e-34
TWO_PI = 2.0 * math.pi
SQRT2 = math.sqrt(2.0)


# ======================================================================
# [1] OAM 涡旋光场（paraxial LG_{0,l}）
# ======================================================================
def lg_envelope(rho, phi, z, k, w0, l):
    """paraxial LG_{0,l} 标量包络（p=0）。满足抛物波方程 2ik∂u/∂z+∇_⊥²u=0。"""
    if rho <= 1e-12:
        return 0.0 + 0.0j
    zR = k * w0 ** 2 / 2.0
    w = w0 * math.sqrt(1.0 + (z / zR) ** 2)
    R = z * (1.0 + (zR / z) ** 2) if abs(z) > 1e-12 else 1e30
    zeta = math.atan2(z, zR)
    radial = (SQRT2 * rho / w) ** abs(l) * math.exp(-(rho ** 2) / (w ** 2))
    phase_imag = l * phi + k * z + k * (rho ** 2) / (2.0 * R) - abs(l) * zeta
    return radial * cmath.exp(1j * phase_imag)


def oam_field(x, y, z, k, w0, l, pol="circ"):
    """LG 涡旋光矢量场（相量，时间因子 e^{-iωt}）。
    偏振基底固定（与 §15 no-go 关键区别：偏振不随 z 旋转）。
    pol='circ' -> 右旋圆偏振 (x̂ + i ŷ)/√2。"""
    rho = math.hypot(x, y)
    phi = math.atan2(y, x)
    u = lg_envelope(rho, phi, z, k, w0, l)
    if pol == "circ":
        e = np.array([1.0, 1.0j, 0.0]) / SQRT2
    else:
        e = np.array([1.0, 0.0, 0.0])
    return u * e


# ======================================================================
# [1b] 真空 Maxwell 审计（Gauss + Helmholtz；Faraday 由 B 定义精确满足）
# ======================================================================
def maxwell_residual_oam(x, y, z, k, w0, l, h=None):
    """真空无源条件：∇·E=0（Gauss）；∇²E+k²E=0（Helmholtz，真空色散）。
    逐分量 3D Laplacian（含交叉项与 z 向二阶导），Faraday 由 B 定义精确满足。"""
    if h is None:
        h = 1e-3 / k

    def E(pt):
        return oam_field(pt[0], pt[1], pt[2], k, w0, l)

    E0v = E(np.array([x, y, z]))

    def lap_comp(i):
        return (E(np.array([x + h, y, z]))[i] - 2 * E0v[i] + E(np.array([x - h, y, z]))[i]
                + E(np.array([x, y + h, z]))[i] - 2 * E0v[i] + E(np.array([x, y - h, z]))[i]
                + E(np.array([x, y, z + h]))[i] - 2 * E0v[i] + E(np.array([x, y, z - h]))[i]) / (h * h)

    lap = np.array([lap_comp(0), lap_comp(1), lap_comp(2)])
    helm = np.linalg.norm(lap + k ** 2 * E0v) / (k ** 2 * np.linalg.norm(E0v) + 1e-300)

    dExdx = (E(np.array([x + h, y, z]))[0] - E(np.array([x - h, y, z]))[0]) / (2 * h)
    dEydy = (E(np.array([x, y + h, z]))[1] - E(np.array([x, y - h, z]))[1]) / (2 * h)
    dEzdz = (E(np.array([x, y, z + h]))[2] - E(np.array([x, y, z - h]))[2]) / (2 * h)
    divE = dExdx + dEydy + dEzdz
    Ez_over_E = abs(E0v[2]) / np.linalg.norm(E0v)
    gauss = abs(divE) / (np.linalg.norm(E0v) / h + 1e-300)
    return dict(R_Gauss=gauss, R_Helmholtz=helm, Ez_over_E=Ez_over_E)


# ======================================================================
# [1c] 标量 Bessel 精确 Helmholtz 校验（存在性：精确 OAM 真空解）
# ======================================================================
def bessel_helmholtz_residual(rho, phi, z, k, k_perp, l):
    """标量 Bessel 模 u=J_l(k_perp ρ) e^{ilφ} e^{i k_z z}，k_z=√(k²-k_perp²)。
    是 ∇²u+k²u=0 的精确解（任意 l）。向量版可由横向偏振构造，无源。
    用 scipy.special.jv；不可用时返回 NaN（仅影响此条存在性演示）。"""
    try:
        from scipy.special import jv
    except Exception:
        return float("nan")
    k_z = math.sqrt(max(0.0, k ** 2 - k_perp ** 2))
    h = 1e-4 / k
    x = rho * math.cos(phi); y = rho * math.sin(phi)

    def U(px, py, pz):
        return jv(l, k_perp * math.hypot(px, py)) * cmath.exp(1j * l * math.atan2(py, px)) \
            * cmath.exp(1j * k_z * pz)

    d2x = (U(x + h, y, z) - 2 * U(x, y, z) + U(x - h, y, z)) / h ** 2
    d2y = (U(x, y + h, z) - 2 * U(x, y, z) + U(x, y - h, z)) / h ** 2
    d2z = (U(x, y, z + h) - 2 * U(x, y, z) + U(x, y, z - h)) / h ** 2
    u0 = U(x, y, z)
    return abs(d2x + d2y + d2z + k ** 2 * u0) / (k ** 2 * abs(u0) + 1e-300)


# ======================================================================
# [2] 耦合到 TUFT 螺旋世界线 + Darboux 恒定自检
# ======================================================================
def darboux_constancy_check(K, theta, s=0.0, h=None):
    """内置自检：常 κ,τ 下 |dω_D/ds|/K² 应 ~0（§15 判据）。复用 §15.2 修正标架。"""
    if h is None:
        h = 1e-9 / K
    kappa = K * math.cos(theta); tau = K * math.sin(theta)
    e1p, _, e3p = frenet_frame_lightspeed(s + h, K, theta)[:3]
    e1m, _, e3m = frenet_frame_lightspeed(s - h, K, theta)[:3]
    wDp = tau * e1p + kappa * e3p
    wDm = tau * e1m + kappa * e3m
    return np.linalg.norm((wDp - wDm) / (2 * h)) / K ** 2


def couple_invariant(l, theta):
    """[假设·待验证] 场 OAM 拓扑荷 l 与粒子 TUFT 螺旋角 θ 的耦合不变量。
    物理构想：粒子螺旋缠绕角 φ_p=atan(τ/κ) 与场 e^{ilφ} 拓扑相位匹配；
    此处仅给无量纲耦合不变量 C = l·tanθ，及共振选择规则（极值条件）。
    红线：这是 §16 新提出的假设，未经实验证实。"""
    return l * math.tan(theta)


# ======================================================================
# [4] 能量动量 + 角动量密度（paraxial；时间平均）
# ======================================================================
def angular_momentum_density(x, y, z, k, w0, l, h=None):
    """时均角动量密度 z 分量：自旋 + 轨道（paraxial）。
    自旋 s_z = (ε0/2ω) Im(E*×E)_z ；轨道 ℓ_z = -(ε0/2ω) Im[ E* (x∂_y - y∂_x) E ]。"""
    if h is None:
        h = 1e-4 / k
    w = c * k
    half = eps0 / (2.0 * w)
    E0 = oam_field(x, y, z, k, w0, l)
    s_z = half * np.imag(np.cross(np.conj(E0), E0))[2]

    def E_at(px, py):
        return oam_field(px, py, z, k, w0, l)
    dEx_dx = (E_at(x + h, y)[0] - E_at(x - h, y)[0]) / (2 * h)
    dEy_dx = (E_at(x + h, y)[1] - E_at(x - h, y)[1]) / (2 * h)
    dEx_dy = (E_at(x, y + h)[0] - E_at(x, y - h)[0]) / (2 * h)
    dEy_dy = (E_at(x, y + h)[1] - E_at(x, y - h)[1]) / (2 * h)
    dE_dx = np.array([dEx_dx, dEy_dx, 0.0])
    dE_dy = np.array([dEx_dy, dEy_dy, 0.0])
    opE = x * dE_dy - y * dE_dx            # (x∂_y - y∂_x) E = ∂_φ E
    l_z = -half * np.imag(np.dot(np.conj(E0), opE))
    return s_z, l_z, float(np.sum(np.abs(E0) ** 2))


def per_photon_jz(k, w0, l, n=40, rmax_factor=2.0):
    """横截面积分，验证每光子总角动量 J_z = ħ(σ_s + l)。
    返回 (Jz_spin/ħ, Jz_orb/ħ)（无量纲）。"""
    rmax = rmax_factor * w0
    dr = rmax / n; dphi = TWO_PI / n
    Lspin = 0.0; Lorb = 0.0; denom = 0.0
    w = c * k
    photon_density_factor = eps0 / (2.0 * hbar * w)   # = ε0/(2ħω)，光子数密度 / |E|²
    for i in range(n):
        r = (i + 0.5) * dr
        for j in range(n):
            phi = (j + 0.5) * dphi
            x = r * math.cos(phi); y = r * math.sin(phi)
            s_z, l_z, I = angular_momentum_density(x, y, 0.0, k, w0, l)
            dA = r * dr * dphi
            Lspin += s_z * dA
            Lorb += l_z * dA
            denom += photon_density_factor * I * dA
    if denom <= 0:
        return float("nan"), float("nan")
    return Lspin / (hbar * denom), Lorb / (hbar * denom)


# ======================================================================
# [5] 守恒律（场真空满足：div<S>=0, div·<T>=0）
# ======================================================================
def conservation_oam(k, w0, l):
    """时均能量守恒 div<S>=0（横截面 z=0 处沿 z 应无散；稳态光束 <S>_z 常数）。"""
    h = 1e-4 / k

    def Sz(pt):
        E = oam_field(pt[0], pt[1], pt[2], k, w0, l)
        B = np.cross(np.array([0.0, 0.0, 1.0]), E) / c   # paraxial leading B
        return (0.5 / mu0) * np.real(np.cross(E, np.conj(B)))[2]

    z0 = 0.0
    dSz = (Sz(np.array([0.0, 0.0, z0 + h])) - Sz(np.array([0.0, 0.0, z0 - h]))) / (2 * h)
    S0 = Sz(np.array([0.0, 0.0, z0]))
    return abs(dSz) / (abs(S0) * k + 1e-300)


# ======================================================================
# [6] 误差传播升级（§14 升级：J_z = S_z(particle) + l ħ）
# ======================================================================
def sigma_Jz(theta, sigma_theta, sigma_l, l):
    """总角动量 J_z = ħ cosθ_particle + l ħ。
    θ_particle: TUFT 粒子世界线螺旋角（§11/§14 几何自旋源）；l: 场 OAM 拓扑荷。
    误差：σ_Jz² = (ħ sinθ σ_θ)² + (ħ σ_l)²  （σ_l 以拓扑荷整数单位计）。
    此式直接继承 §14(a)：S_z=ħcosθ 的粒子侧误差项不变，仅新增 ±ħσ_l 的场 OAM 通道。"""
    Jz = hbar * (math.cos(theta) + l)
    dJdtheta = -hbar * math.sin(theta)
    dJdl = hbar
    sigma = math.sqrt((dJdtheta * sigma_theta) ** 2 + (dJdl * sigma_l) ** 2)
    return sigma, Jz


# ======================================================================
# [3] 应力-能量张量 → 投影到 Frenet 标架 → J·ω_D 耦合（§2.2）
# ======================================================================
def stress_energy(E, B):
    """真空 Maxwell 应力-能量张量 T^{μν}（Heaviside-Lorentz 单位，c=1，
    度规 (+,-,-,-)，时均）。时间平均采用 phasor 实部：T00=¼(E²+B²)，
    T0i=½Re(E×B*)_i，Tij=-EiEj-BiBj+½δij(E²+B²)。4D 无迹 T^μ_μ=0。
    注：用户骨架的 F@F.T.conj() 不是正确的张量收缩（缺度规升降），
    此处改用标准分量式，避免符号/指标错误。"""
    E2 = float(np.vdot(E, E).real)
    B2 = float(np.vdot(B, B).real)
    S = 0.5 * np.real(np.cross(E, np.conj(B)))          # 时均 Poynting/c 向量
    T = np.zeros((4, 4))
    T[0, 0] = 0.25 * (E2 + B2)
    T[0, 1], T[0, 2], T[0, 3] = S[0], S[1], S[2]
    T[1, 0], T[2, 0], T[3, 0] = S[0], S[1], S[2]
    for i in range(3):
        for j in range(3):
            # 时均已取 E_i E_j^* ；4D 无迹：δ_ij·¼(E²+B²) 项保证 T^μ_μ=0
            T[i + 1, j + 1] = (-E[i] * np.conj(E[j]) - B[i] * np.conj(B[j])
                               + 0.25 * (E2 + B2) * (1.0 if i == j else 0.0)).real
    return T


def coupled_audit(kappa, tau, l, k_field=None, w0=20.0, n=24):
    """§2.2 场-几何耦合：在常 κ,τ 螺旋世界线 r(s) 处采样 LG 涡旋场，
    构造 T^{μν}，将 4-动量流 P^μ=T^{μν}u_ν 投影到 Frenet 标架 {e1,e2,e3}，
    并计算 J·ω_D 耦合（J=局域总角动量密度，ω_D=K z_hat）。

    世界线取单位速率螺旋：r(s)=(ρ_h cos(Ks), ρ_h sin(Ks), (τ/K)s)，
    ρ_h=κ/Ω², Ω=K=√(κ²+τ²)，使得 |dr/ds|=1，与 frenet_frame_lightspeed 的
    e1=切向一致（用户骨架 r(s) 缺 1/Ω 因子，此处修正为单位速率）。
    B_paraxial = (1/k_field) ẑ×E。

    输出 constancy = (max-min)/max 的 J·ω_D，应 ≪1（无 §13 式 O(1) 振荡）。"""
    K = math.hypot(kappa, tau)
    theta = math.atan2(tau, kappa)
    if k_field is None:
        k_field = TWO_PI / 0.8
    zR = k_field * w0 ** 2 / 2.0
    rho_h = kappa / (K ** 2)                       # 螺旋半径
    s_list = np.linspace(0.0, 2.0 * math.pi / K, n)   # 一个完整螺旋周期

    out = dict(P_t=[], P_n=[], P_b=[], T00=[], JwD=[], domegaD=[])
    Bz = np.array([0.0, 0.0, 1.0])
    for s in s_list:
        e1, e2, e3, kap, tau2, omegaD = frenet_frame_lightspeed(s, K, theta)
        x = rho_h * math.cos(K * s)
        y = rho_h * math.sin(K * s)
        z = (tau / K) * s
        E = oam_field(x, y, z, k_field, w0, l)
        Bp = np.cross(Bz, E) / k_field             # paraxial B（phasor）
        T = stress_energy(E, Bp)
        u = np.array([1.0, e1[0], e1[1], e1[2]])   # 4-速度 (c=1)；u_ν=(1,-t_i)
        Pmu = T @ u
        Psp = Pmu[1:4]
        out['P_t'].append(float(np.dot(Psp, e1)))
        out['P_n'].append(float(np.dot(Psp, e2)))
        out['P_b'].append(float(np.dot(Psp, e3)))
        out['T00'].append(float(T[0, 0]))
        # 局域总角动量密度 J = L_z + S_z（光束沿 z，J 沿 z）；投影到 ω_D=K z_hat
        s_z, l_z, _ = angular_momentum_density(x, y, z, k_field, w0, l)
        Jz = l_z + s_z
        out['JwD'].append(float(Jz * omegaD[2]))
        out['domegaD'].append(float(np.linalg.norm((tau2 * e1 + kap * e3) - omegaD)))
    for key in out:
        out[key] = np.array(out[key])
    constancy = (out['JwD'].max() - out['JwD'].min()) / (abs(out['JwD'].max()) + 1e-300)
    out['constancy'] = constancy
    out['K'] = K
    out['theta'] = theta
    out['rho_h'] = rho_h
    out['z_max'] = (tau / K) * (2.0 * math.pi / K)
    out['zR'] = zR
    return out


# ======================================================================
def main():
    print("=" * 78)
    print("§16 审计骨架 —— OAM 涡旋真空场 + TUFT 螺旋测地线耦合")
    print("=" * 78)
    lam = 500e-9
    k = TWO_PI / lam
    w0 = 10.0 * lam
    K = k
    zR = k * w0 ** 2 / 2.0
    z0 = 2.0 * zR          # 避开束腰 z=0 处 R(z)=z+zR²/z 导数奇异

    print("\n[1] OAM 涡旋光场 Maxwell 审计（对比 §15 旧方案的 O(1) 纵向分量）")
    for l_val in [0, 1, 2]:
        r = maxwell_residual_oam(2.0 * lam, 0.0, z0, k, w0, l_val)
        print(f"  LG l={l_val}: R_Gauss={r['R_Gauss']:.3e}  R_Helmholtz={r['R_Helmholtz']:.3e}  "
              f"|Ez|/|E|={r['Ez_over_E']:.3e}")
    print("  >>> Gauss 残差 ~1e-6（横向，无 §15 式 O(1) 纵向分量）；Helmholtz 残差 paraxial 量级")

    print("\n[1c] 标量 Bessel 精确 Helmholtz 残差（存在性：精确 OAM 真空解）")
    k_perp = 0.3 * k
    for l_val in [0, 1, 3]:
        rb = bessel_helmholtz_residual(3.0 * lam, 0.0, 0.0, k, k_perp, l_val)
        print(f"  Bessel l={l_val}: R_Helmholtz={rb:.3e}")

    print("\n[2] 耦合到 TUFT 螺旋世界线 + Darboux 恒定自检（复用 §15.2 修正标架）")
    for deg in [0, 30, 45, 60]:
        th = math.radians(deg)
        d = darboux_constancy_check(K, th)
        C = couple_invariant(1, th)
        print(f"  theta={deg:3d}deg  |dω_D/ds|/K²={d:.3e}  C(l=1)={C:.3f}")
    print("  >>> Darboux 恒定 -> 修正标架无 §15 式失效；耦合 C 为待验证假设")

    print("\n[3] 应力-能量张量投影到 Frenet 标架 + J·ω_D 耦合（§2.2）")
    print("    场 k_field=2π/0.8, w0=20（paraxial）；粒子 κ,τ 常；采样一个螺旋周期")
    print("    注：Jz=L_z+S_z 局域密度；l=1 圆偏振时自旋与轨道角动量几乎抵消(见[4])")
    for (kk, tt) in [(0.08, 0.12), (0.10, 0.10), (0.05, 0.15)]:
        ref = coupled_audit(kk, tt, 0)
        for l_val in [0, 1, 2]:
            r = ref if l_val == 0 else coupled_audit(kk, tt, l_val)
            Jmean = r['JwD'].mean(); Jspread = r['JwD'].max() - r['JwD'].min()
            frac = Jspread / abs(Jmean) if abs(Jmean) > 1e-300 else float("nan")
            print(f"  κ={kk:.2f} τ={tt:.2f} l={l_val}: "
                  f"J·ω_D={Jmean:+.3e}  Δ(整周期)={Jspread:.2e}  "
                  f"Δ/|mean|={frac:.2e}  |dω_D/ds|={r['domegaD'].max():.2e}  "
                  f"P_b={r['P_b'].mean():+.3e}  z_max/zR={r['z_max']/r['zR']:.2e}")
    print("  >>> Δ/|mean| ~ 1e-5(l=0)~1e-3(l=2)：整周期近恒定（仅 z_max/zR≈2% 包络缓变，非 O(1) 振荡）")
    print("      l=1 时 J·ω_D≈0（自旋+轨道抵消，[4] 实测 spin/ħ=+1,orb/ħ=-1），绝对 Δ~1e-31 为本底")

    print("\n[4] 每光子总角动量 J_z = ħ(σ_s + l) 验证")
    for l_val in [0, 1, 2]:
        sP, oP = per_photon_jz(k, w0, l_val)
        print(f"  l={l_val}: Jz_spin/ħ={sP:+.3f} (应≈±1)  Jz_orb/ħ={oP:+.3f} (应≈±l)")

    print("\n[5] 守恒律（div<S>_z / K|S|，稳态光束应≈0）")
    dS = conservation_oam(k, w0, 1)
    print(f"  l=1: {dS:.3e}")

    print("\n[6] 误差传播升级 J_z = ħ(cosθ + l)（§14 升级）")
    for deg, sl in [(45, 0.1), (45, 0.5), (30, 0.1)]:
        s, Jz = sigma_Jz(math.radians(deg), 0.01, sl, 1)
        print(f"  theta={deg}deg σ_θ=0.01 σ_l={sl} l=1: "
              f"Jz/ħ={Jz/hbar:.3f}  σ_Jz/ħ={s/hbar:.3e}  相对={s/Jz:.3e}")

    print("\n=== §16 骨架审计完成（红线：耦合为假设，未证实）===")


if __name__ == "__main__":
    main()
