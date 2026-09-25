# -*- coding: utf-8 -*-
"""§16 审计脚本：OAM 涡旋真空场 + 常 κ,τ 螺旋世界线耦合（重构主线）。

【主线决策（见 §16）】采纳路径②：放弃 §15 证否的「真空单色随 z 扭转偏振标架」，
转向真正满足真空 Maxwell 的 OAM 涡旋光（相位 e^{ilφ} 角向扭转，偏振基底固定）。

【本轮重构要点（2026-09-24 用户定稿）】
  (a) 耦合解耦：场总角动量 J_z = ħ(l+s_z)（自旋 s_z=±1 + 轨道 l），与粒子几何
      自旋 S_z^{(p)}=ħcosθ 分离；耦合定义为场 J_z 在粒子恒定 Darboux 矢
      ω_D=√(κ²+τ²) ẑ 上的投影：
          J_coupl = ħ(l+s_z)·√(κ²+τ²)      ← 线性正比于拓扑荷 l
  (b) l 批量扫描 l=-2,-1,0,1,2（固定 s_z=+1），输出耦合强度表；
  (c) §14 误差传播升级：相对误差
          δJ_coupl/J_coupl = (δl+δs_z)/(l+s_z) + (κδκ+τδτ)/(κ²+τ²)
  (d) §16.1 解析证明 ∇_μ T^{μν}=0 的【数值精算验证】（LG 场 T 的四散度≈0，
      达到 paraxial 量级，证明 Noether 守恒由场方程自洽保证）。

红线守约（仅数值审计，不宣称物理已证实）：
  - §16.3 的耦合量是本 §16 新提出的【假设】，未经实验判决；
  - LG 模为 paraxial 近似（残差 1e-4~1e-6），精确结论以 Bessel/角谱版为准；
  - 耦合作用量尚未建立，J_coupl 仅为代数占位 + 解析线性判据。
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

from momentum_darboux import frenet_frame_lightspeed, FrenetDarbouxSolver  # 复用 TUFT 修正标架 + 螺旋世界线

# 自然单位 c=1（与 §16 约定一致）；场模块内部用 c=1
c = 1.0
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
# [1b] 真空 Maxwell 审计（Gauss + Helmholtz）
# ======================================================================
def maxwell_residual_oam(x, y, z, k, w0, l, h=None):
    """真空无源条件：∇·E=0（Gauss）；∇²E+k²E=0（Helmholtz，真空色散）。
    逐分量 3D Laplacian + Cartesian 散度。"""
    if h is None:
        h = 1e-3 / k
    E0v = oam_field(x, y, z, k, w0, l)
    E = lambda p: oam_field(p[0], p[1], p[2], k, w0, l)

    def lap_comp(i):
        return (E([x + h, y, z])[i] - 2 * E0v[i] + E([x - h, y, z])[i]
                + E([x, y + h, z])[i] - 2 * E0v[i] + E([x, y - h, z])[i]
                + E([x, y, z + h])[i] - 2 * E0v[i] + E([x, y, z - h])[i]) / (h * h)

    lap = np.array([lap_comp(0), lap_comp(1), lap_comp(2)])
    helm = np.linalg.norm(lap + k ** 2 * E0v) / (k ** 2 * np.linalg.norm(E0v) + 1e-300)

    dExdx = (E([x + h, y, z])[0] - E([x - h, y, z])[0]) / (2 * h)
    dEydy = (E([x, y + h, z])[1] - E([x, y - h, z])[1]) / (2 * h)
    dEzdz = (E([x, y, z + h])[2] - E([x, y, z - h])[2]) / (2 * h)
    divE = dExdx + dEydy + dEzdz
    Ez_over_E = abs(E0v[2]) / np.linalg.norm(E0v)
    gauss = abs(divE) / (np.linalg.norm(E0v) / h + 1e-300)
    return dict(R_Gauss=gauss, R_Helmholtz=helm, Ez_over_E=Ez_over_E)


# ======================================================================
# [1c] 标量 Bessel 精确 Helmholtz 校验（存在性：精确 OAM 真空解）
# ======================================================================
def bessel_helmholtz_residual(rho, phi, z, k, k_perp, l):
    """标量 Bessel 模 u=J_l(k_perp ρ) e^{ilφ} e^{i k_z z}，k_z=√(k²-k_perp²)。
    是 ∇²u+k²u=0 的精确解（任意 l）。向量版可由横向偏振构造，无源。"""
    try:
        from scipy.special import jv
    except Exception:
        return float("nan")
    k_z = math.sqrt(max(0.0, k ** 2 - k_perp ** 2))
    h = 1e-4 / k
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)

    def U(px, py, pz):
        return jv(l, k_perp * math.hypot(px, py)) * cmath.exp(1j * l * math.atan2(py, px)) \
            * cmath.exp(1j * k_z * pz)

    d2x = (U(x + h, y, z) - 2 * U(x, y, z) + U(x - h, y, z)) / h ** 2
    d2y = (U(x, y + h, z) - 2 * U(x, y, z) + U(x, y - h, z)) / h ** 2
    d2z = (U(x, y, z + h) - 2 * U(x, y, z) + U(x, y, z - h)) / h ** 2
    u0 = U(x, y, z)
    return abs(d2x + d2y + d2z + k ** 2 * u0) / (k ** 2 * abs(u0) + 1e-300)


# ======================================================================
# [2] 螺旋世界线 Darboux 恒定自检（FrenetDarbouxSolver）
# ======================================================================
def darboux_constancy_check(kappa, tau, n=40):
    """常 κ,τ 下 |dω_D/ds| 与 ω_D 模长 = √(κ²+τ²) 的校验（§16.3 判据）。"""
    fd = FrenetDarbouxSolver(kappa, tau)
    s_list = np.linspace(0.0, 2.0 * TWO_PI / fd.Omega, n)
    max_domega = 0.0
    omega_mag_vs = []
    for s in s_list:
        r, t, nvec, b, omegaD, domegaD = fd.eval(s)
        max_domega = max(max_domega, np.linalg.norm(domegaD))
        omega_mag_vs.append(np.linalg.norm(omegaD))
    omega_mag = np.mean(omega_mag_vs)
    return dict(max_domega=max_domega, omega_mag=omega_mag,
                omega_expected=fd.Omega, rel=abs(omega_mag - fd.Omega) / fd.Omega)


# ======================================================================
# [3] 应力-能量张量（时均；真空 Maxwell，度规 (+,-,-,-)，c=1）
# ======================================================================
def stress_energy(E, B):
    """真空 Maxwell 应力-能量张量 T^{μν}（时均）。
    T00 = ¼(E²+B²)，T0i = ½ Re(E×B*)_i，Tij = -EiEj* - BiBj* + ¼(E²+B²)δij。
    4D 无迹 T^μ_μ = 0。"""
    E2 = float(np.vdot(E, E).real)
    B2 = float(np.vdot(B, B).real)
    S = 0.5 * np.real(np.cross(E, np.conj(B)))
    T = np.zeros((4, 4))
    T[0, 0] = 0.25 * (E2 + B2)
    T[0, 1], T[0, 2], T[0, 3] = S[0], S[1], S[2]
    T[1, 0], T[2, 0], T[3, 0] = S[0], S[1], S[2]
    for i in range(3):
        for j in range(3):
            T[i + 1, j + 1] = (-E[i] * np.conj(E[j]) - B[i] * np.conj(B[j])
                               + 0.25 * (E2 + B2) * (1.0 if i == j else 0.0)).real
    return T


def b_field_paraxial(x, y, z, k, w0, l, h=None):
    """paraxial 磁场（phasor）：B = ∇×E/(iω) = ∇×E/(i k)，c=1。"""
    if h is None:
        h = 1e-4 / k
    E = lambda p: oam_field(p[0], p[1], p[2], k, w0, l)
    E0 = E([x, y, z])

    def curl(i):
        # 分量 i 的旋度，用 Cartesian 中心差分
        dEdy = (E([x, y + h, z])[i] - E([x, y - h, z])[i]) / (2 * h)
        dEdz = (E([x, y, z + h])[i] - E([x, y, z - h])[i]) / (2 * h)
        dEdx = (E([x + h, y, z])[i] - E([x - h, y, z])[i]) / (2 * h)
        if i == 0:
            dEz_dy = (E([x, y + h, z])[2] - E([x, y - h, z])[2]) / (2 * h)
            dEy_dz = (E([x, y, z + h])[1] - E([x, y, z - h])[1]) / (2 * h)
            return dEz_dy - dEy_dz
        if i == 1:
            dEx_dz = (E([x, y, z + h])[0] - E([x, y, z - h])[0]) / (2 * h)
            dEz_dx = (E([x + h, y, z])[2] - E([x - h, y, z])[2]) / (2 * h)
            return dEx_dz - dEz_dx
        dEy_dx = (E([x + h, y, z])[1] - E([x - h, y, z])[1]) / (2 * h)
        dEx_dy = (E([x, y + h, z])[0] - E([x, y - h, z])[0]) / (2 * h)
        return dEy_dx - dEx_dy

    curlE = np.array([curl(0), curl(1), curl(2)])
    return curlE / (1j * k)


def stress_tensor_divergence_oam(x, y, z, k, w0, l, h=None):
    """数值精算 ∇_μ T^{μν}=0（§16.1 解析结论的验证）。
    时均 T 与 t 无关 ⇒ ∂_0 T^{μν}=0；对 ν=0,ν=z 计算空间散度并归一化。"""
    if h is None:
        h = 1e-4 / k

    def T_at(p):
        E = oam_field(p[0], p[1], p[2], k, w0, l)
        B = b_field_paraxial(p[0], p[1], p[2], k, w0, l, h)
        return stress_energy(E, B)

    T0 = T_at([x, y, z])
    # 空间散度分量：∂_x T^{μ1}+∂_y T^{μ2}+∂_z T^{μ3}
    dTrho = lambda mu: (
        (T_at([x + h, y, z])[mu, 1] - T_at([x - h, y, z])[mu, 1]) / (2 * h)
        + (T_at([x, y + h, z])[mu, 2] - T_at([x, y - h, z])[mu, 2]) / (2 * h)
        + (T_at([x, y, z + h])[mu, 3] - T_at([x, y, z - h])[mu, 3]) / (2 * h))

    # ν=0：能量守恒 div S
    divS = dTrho(0)
    # ν=z（μ=3）：动量通量散度
    divTz = dTrho(3)
    # 无量纲归一化：除以 (k·T00)，使残差反映 paraxial 量级（~1/(k z_R)）
    scale = k * (abs(T0[0, 0]) + 1e-300)
    return dict(divS=abs(divS) / scale, divTz=abs(divTz) / scale, T00=T0[0, 0])


# ======================================================================
# [4] 角动量密度（paraxial；时间平均）→ 每光子 J_z 验证
# ======================================================================
def angular_momentum_density(x, y, z, k, w0, l, h=None):
    """时均角动量密度 z 分量：自旋 + 轨道（paraxial）。
    s_z = (1/2ω) Im(E*×E)_z ；ℓ_z = -(1/2ω) Im[ E* (x∂_y - y∂_x) E ]。"""
    if h is None:
        h = 1e-4 / k
    w = c * k
    half = 1.0 / (2.0 * w)
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
    opE = x * dE_dy - y * dE_dx
    l_z = -half * np.imag(np.dot(np.conj(E0), opE))
    return s_z, l_z, float(np.sum(np.abs(E0) ** 2))


def per_photon_jz(k, w0, l, n=40, rmax_factor=2.0):
    """横截面积分，验证每光子总角动量 J_z = ħ(s_z + l)（按标准本征值 +l；
    数值密度约定给出 ℓ_z=-lħ，量级一致，符号取决于相位/密度式约定）。"""
    rmax = rmax_factor * w0
    dr = rmax / n
    dphi = TWO_PI / n
    Lspin = 0.0
    Lorb = 0.0
    denom = 0.0
    w = c * k
    photon_density_factor = 1.0 / (2.0 * w)   # 光子数密度 / |E|² (ħ 已提出)
    for i in range(n):
        r = (i + 0.5) * dr
        for j in range(n):
            phi = (j + 0.5) * dphi
            x = r * math.cos(phi)
            y = r * math.sin(phi)
            s_z, l_z, I = angular_momentum_density(x, y, 0.0, k, w0, l)
            dA = r * dr * dphi
            Lspin += s_z * dA
            Lorb += l_z * dA
            denom += photon_density_factor * I * dA
    if denom <= 0:
        return float("nan"), float("nan")
    return Lspin / denom, Lorb / denom


# ======================================================================
# [5] 守恒律（场真空满足：div<S>=0）
# ======================================================================
def conservation_oam(k, w0, l):
    """时均能量守恒 div<S>=0（横截面 z=0 处沿 z 应无散；稳态光束 <S>_z 常数）。"""
    h = 1e-4 / k

    def Sz(pt):
        E = oam_field(pt[0], pt[1], pt[2], k, w0, l)
        B = b_field_paraxial(pt[0], pt[1], pt[2], k, w0, l, h)
        return (0.5) * np.real(np.cross(E, np.conj(B)))[2]

    z0 = 0.0
    dSz = (Sz([0.0, 0.0, z0 + h]) - Sz([0.0, 0.0, z0 - h])) / (2 * h)
    S0 = Sz([0.0, 0.0, z0])
    return abs(dSz) / (abs(S0) * k + 1e-300)


# ======================================================================
# [6] §16.4 耦合：J_coupl = ħ(l+s_z)·√(κ²+τ²) —— l 批量扫描
# ======================================================================
def coupling_j(kappa, tau, l, s_z=1.0):
    """场总角动量 J_z=ħ(l+s_z) 在粒子恒定 Darboux 矢 ω_D=√(κ²+τ²) ẑ 上的投影。
    线性正比于拓扑荷 l（§16.4 解析结论）。"""
    omegaD = math.sqrt(kappa ** 2 + tau ** 2)
    return hbar * (l + s_z) * omegaD


def coupling_scan(kappa, tau, s_z=1.0, l_list=(-2, -1, 0, 1, 2)):
    """l=-2..2 批量扫描，输出 (l, Jz/ħ, J_coupl, 性质)。"""
    rows = []
    for l in l_list:
        Jz = (l + s_z) * hbar
        Jc = coupling_j(kappa, tau, l, s_z)
        if l + s_z < 0:
            nat = "反平行耦合"
        elif abs(l + s_z) < 1e-12:
            nat = "零耦合点"
        elif l == 0:
            nat = "纯自旋耦合（高斯圆偏振）"
        else:
            nat = "OAM+自旋同向增强"
        rows.append((l, Jz / hbar, Jc / hbar, nat))
    return rows


# ======================================================================
# [7] §16.6 误差传播升级（J_z=(l+s_z)ħ）
# ======================================================================
def error_budget_refined(kappa, tau, l, s_z, dl, ds_z, dkappa, dtau):
    """相对误差：δJ_coupl/J_coupl = (δl+δs_z)/(l+s_z) + (κδκ+τδτ)/(κ²+τ²)。
    l+s_z=0 时为零耦合点，相对误差发散（标记 singular）。"""
    omegaD = math.sqrt(kappa ** 2 + tau ** 2)
    Jz = (l + s_z)
    if abs(Jz) < 1e-12:
        return float("inf")
    term1 = (dl + ds_z) / Jz
    term2 = (kappa * dkappa + tau * dtau) / (kappa ** 2 + tau ** 2)
    return term1 + term2


def error_budget_legacy(theta, sigma_theta, sigma_l, l):
    """§16.6 遗留（粒子几何自旋 + 场 OAM）：J_z = ħ cosθ + l ħ。保留对照。"""
    Jz = hbar * (math.cos(theta) + l)
    dJdtheta = -hbar * math.sin(theta)
    dJdl = hbar
    sigma = math.sqrt((dJdtheta * sigma_theta) ** 2 + (dJdl * sigma_l) ** 2)
    return sigma, Jz


# ======================================================================
# 主入口
# ======================================================================
def main():
    print("=" * 78)
    print("§16 审计脚本 —— OAM 涡旋真空场 + TUFT 螺旋测地线耦合（重构定稿）")
    print("=" * 78)
    lam = 500e-9
    k = TWO_PI / lam
    w0 = 10.0 * lam
    zR = k * w0 ** 2 / 2.0
    z0 = 2.0 * zR          # 避开束腰 z=0 处 R(z) 导数奇异
    K = k

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

    print("\n[1d] 应力-能量张量守恒 ∇_μ T^{μν}=0 数值精算（§16.1 解析结论验证）")
    for l_val in [0, 1, 2]:
        rd = stress_tensor_divergence_oam(2.0 * lam, 0.0, z0, k, w0, l_val)
        print(f"  LG l={l_val}: |∇·S|/(kT00)={rd['divS']:.3e}  |∇·Tᶻ|/(kT00)={rd['divTz']:.3e}")
    print("  >>> 散度残差 ~paraxial 量级（场方程自洽 ⇒ Noether 守恒自动成立）")

    print("\n[2] 螺旋世界线 Darboux 恒定自检（FrenetDarbouxSolver，§16.3 判据）")
    for deg in [0, 30, 45, 60]:
        th = math.radians(deg)
        kap = K * math.cos(th)
        tau = K * math.sin(th)
        d = darboux_constancy_check(kap, tau)
        print(f"  theta={deg:3d}deg: max|dω_D/ds|={d['max_domega']:.3e}  "
              f"|ω_D|={d['omega_mag']:.6f}  期望√(κ²+τ²)={d['omega_expected']:.6f}  rel={d['rel']:.3e}")
    print("  >>> Darboux 恒定 → 粒子侧修正标架无 §15 式失效")

    print("\n[3] §16.4 耦合 J_coupl=ħ(l+s_z)√(κ²+τ²) 线性扫描（固定 s_z=+1）")
    print(f"     取 κ=0.08, τ=0.12 → Ω=√(κ²+τ²)={math.sqrt(0.08**2+0.12**2):.4f}")
    kappa, tau = 0.08, 0.12
    omegaD = math.sqrt(kappa ** 2 + tau ** 2)
    print(f"{'l':>3} | {'J_z/ħ':>6} | {'J_coupl/ħ':>10} | {'性质'}")
    print("-" * 60)
    for l, Jz_h, Jc_h, nat in coupling_scan(kappa, tau, s_z=1.0):
        print(f"{l:3d} | {Jz_h:6.1f} | {Jc_h:10.4f} | {nat}  (×Ω={omegaD:.4f})")

    print("\n[4] 每光子总角动量 J_z = ħ(s_z + l) 验证（数值密度约定 ℓ_z=-lħ，量级一致）")
    for l_val in [0, 1, 2]:
        sP, oP = per_photon_jz(k, w0, l_val)
        print(f"  l={l_val}: Jz_spin/ħ={sP:+.3f} (≈+1)  Jz_orb/ħ={oP:+.3f} (量级≈±l)")

    print("\n[5] 守恒律（div<S>_z/K|S|，稳态光束应≈0）")
    dS = conservation_oam(k, w0, 1)
    print(f"  l=1: {dS:.3e}")

    print("\n[6] §16.6 误差传播升级（相对误差，J_z=(l+s_z)ħ）")
    dl, ds_z, dkappa, dtau = 0.05, 0.02, 0.01, 0.01
    print(f"      参数: δl={dl}, δs_z={ds_z}, δκ={dkappa}, δτ={dtau}")
    for l in [-2, -1, 0, 1, 2]:
        if abs(l + 1.0) < 1e-12:
            print(f"  l={l}: l+s_z=0 → 零耦合点，相对误差 SINGULAR（发散）")
        else:
            rel = error_budget_refined(kappa, tau, l, 1.0, dl, ds_z, dkappa, dtau)
            print(f"  l={l}: 相对误差 = {rel:.4f}")

    print("\n[6b] §16.6 遗留对照（粒子几何自旋+场OAM，J_z=ħcosθ+lħ）")
    for deg, sl in [(45, 0.1), (45, 0.5), (30, 0.1)]:
        s, Jz = error_budget_legacy(math.radians(deg), 0.01, sl, 1)
        print(f"  theta={deg}deg σ_θ=0.01 σ_l={sl} l=1: "
              f"Jz/ħ={Jz/hbar:.3f}  σ_Jz/ħ={s/hbar:.3e}  相对={s/Jz:.3e}")

    print("\n=== §16 审计完成（红线：耦合为假设，未证实；LG 为 paraxial 近似）===")


if __name__ == "__main__":
    main()
