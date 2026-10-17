# -*- coding: utf-8 -*-
r"""
HST 来料原样留档：helical_wave_sim.py
=====================================
受理日 2026-10-17 | 来源：用户来料（与《螺旋空间理论体系 HST》同一批）。

**本文件为来料原样，未运行、未修改任何计算逻辑**（仅加本留档头）。
依赖 numpy / scipy / matplotlib（非本库纯标准库审计口径），故本册只做静态审计：
  - F01 是否「自检自证」（代入自己的公式算残差 ⇒ 恒零）；
  - F02 参数 beta=0.3 与 CMB 上界 beta<6e-29 m^-1 的量级差；
  - F03 依赖与不可复现性登记。
静态审计结论见：`判定_TUFT-r96-HST螺旋空间理论体系_全维审计_2026-10-17.md` F 段。
=====================================
"""
import numpy as np
from scipy.special import jv as bessel_j
from scipy.fft import fft, fftfreq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 物理常数 (使用自然单位 c=1 简化计算)
# ============================================================
c = 1.0  # 光速

# ============================================================
# 螺旋参数
# ============================================================
beta = 0.3  # 螺旋扭转率 (放大以清晰展示效应)

# ============================================================
# 验证 1: 色散关系的解析检验
# ============================================================
def verify_dispersion_analytical():
    """解析验证色散关系 ω = c|k - βm|"""
    print("=" * 60)
    print("验证 1: 色散关系 ω = c|k - βm| (解析)")
    print("=" * 60)
    
    k_values = np.linspace(0.5, 5.0, 20)
    m_values = [-2, -1, 0, 1, 2]
    
    print(f"\nβ = {beta}")
    print(f"{'k':>6} | ", end="")
    for m in m_values:
        print(f"{'m='+str(m):>10} ", end="")
    print()
    print("-" * 70)
    
    for k in k_values[::4]:  # 每隔4个打印一行
        print(f"{k:6.2f} | ", end="")
        for m in m_values:
            omega = c * abs(k - beta * m)
            print(f"{omega:10.4f} ", end="")
        print()
    
    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 左图: ω vs k for different m
    k = np.linspace(0, 5, 200)
    for m in m_values:
        omega = c * np.abs(k - beta * m)
        axes[0].plot(k, omega, label=f'm = {m}')
    axes[0].set_xlabel('k (axial wave number)', fontsize=12)
    axes[0].set_ylabel('ω (frequency)', fontsize=12)
    axes[0].set_title(f'Dispersion Relation: ω = c|k - βm| (β={beta})', fontsize=13)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 5)
    axes[0].set_ylim(0, 5)
    
    # 右图: 手征分裂
    k = np.linspace(0, 5, 200)
    for m_abs in [1, 2, 3]:
        omega_plus = c * np.abs(k - beta * m_abs)
        omega_minus = c * np.abs(k - beta * (-m_abs))
        delta_omega = omega_plus - omega_minus
        axes[1].plot(k, delta_omega, label=f'|m| = {m_abs}')
    
    axes[1].axhline(y=-2*c*beta, color='red', linestyle='--', 
                     label=f'High-freq limit: -2cβ = {-2*c*beta:.3f}')
    axes[1].set_xlabel('k', fontsize=12)
    axes[1].set_ylabel('Δω = ω(+m) - ω(-m)', fontsize=12)
    axes[1].set_title('Chiral Frequency Splitting', fontsize=13)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_dispersion.png'), dpi=150)
    plt.close()
    print("\n✓ 图已保存: fig1_dispersion.png")

# ============================================================
# 验证 2: FDTD 模拟螺旋波动方程
# ============================================================
def fdtd_helical_wave():
    """
    FDTD 求解螺旋空间标量波动方程的径向部分。
    
    模式展开 Φ = R(ρ) e^{i(mχ + kζ - ωt)} 后，径向方程为 Bessel 方程:
      R'' + (1/ρ)R' + (K² - m²/ρ²)R = 0
    其中 K² = ω²/c² - (k-βm)²。
    
    验证策略: 用 Bessel 本征模作为初态，验证时间演化频率与解析预测一致。
    边界条件: R(ρ_max) = 0 → J_m(K·ρ_max) = 0 → K = j_{m,n}/ρ_max
    对应频率: ω = c·sqrt(K² + (k-βm)²)
    """
    print("\n" + "=" * 60)
    print("验证 2: FDTD 模拟螺旋波动方程 (本征模初态)")
    print("=" * 60)
    
    from scipy.special import jn_zeros
    
    # 网格参数
    N_rho = 400
    rho_max = 10.0
    d_rho = rho_max / (N_rho + 1)
    rho = np.linspace(d_rho, rho_max - d_rho, N_rho)  # 不包含端点
    
    # 时间步 (CFL)
    dt = 0.3 * d_rho / c
    N_t = 4000
    
    # 测试模式: 使用 Bessel 函数的第一个零点
    # J_m 的第 n 个零点
    modes = []
    for m in [0, 1, -1, 2, -2]:
        n_zero = 1  # 第一个零点
        jmn = jn_zeros(abs(m), n_zero)[0]
        K = jmn / rho_max
        k_axial = 2.0  # 固定轴向波数
        omega_analytical = c * np.sqrt(K**2 + (k_axial - beta * m)**2)
        modes.append({
            'm': m, 'k': k_axial, 'K': K, 'n_zero': n_zero,
            'omega_analytical': omega_analytical,
            'label': f'm={m:+d}, k={k_axial}'
        })
    
    # 零能模式: k = βm, K→0 (用第一个零点给出最小 K)
    m_zero = 1
    k_zero = beta * m_zero  # 使 (k-βm) = 0
    jmn_zero = jn_zeros(m_zero, 1)[0]
    K_zero = jmn_zero / rho_max
    omega_zero = c * K_zero  # ω = cK (因为 k-βm=0)
    modes.append({
        'm': m_zero, 'k': k_zero, 'K': K_zero, 'n_zero': 1,
        'omega_analytical': omega_zero,
        'label': f'm=+1, k=β (near-zero mode, ω=cK={omega_zero:.4f})'
    })
    
    results = {}
    
    for mode in modes:
        m = mode['m']
        K = mode['K']
        omega_ana = mode['omega_analytical']
        
        # 初始条件: 精确本征模 R(ρ) = J_|m|(Kρ)
        # 加上时间振荡: R(ρ, t=0) = J_|m|(Kρ), ∂R/∂t(0) = 0
        # → R(ρ, t) = J_|m|(Kρ) cos(ωt)
        R_init = bessel_j(abs(m), K * rho)
        
        # 归一化
        R_init = R_init / max(abs(R_init))
        
        # ∂R/∂t = 0 → R_prev = R_init (Verlet: R_{-1} = R_1 when v=0)
        # 更精确: R_{-1} = R_0 + dt²/2 · rhs(R_0)
        R = R_init.copy()
        
        # 计算初始 rhs 以获得更精确的 R_prev
        d2R = np.zeros(N_rho)
        d2R[1:-1] = (R[2:] - 2*R[1:-1] + R[:-2]) / d_rho**2
        dR = np.zeros(N_rho)
        dR[1:-1] = (R[2:] - R[:-2]) / (2*d_rho)
        # 边界: 在 ρ=d_rho 处用单侧差分
        dR[0] = (R[1] - R[0]) / d_rho
        dR[-1] = (R[-1] - R[-2]) / d_rho
        
        K_eff_sq = (mode['k'] - beta * m)**2
        rhs_init = c**2 * (d2R + dR/rho - (m**2/rho**2 + K_eff_sq)*R)
        rhs_init[0] = 0 if m != 0 else rhs_init[0]
        rhs_init[-1] = 0  # R(ρ_max) = 0
        
        R_prev = R - 0.5 * dt**2 * rhs_init  # Taylor 展开到 O(dt²)
        
        # 记录场的空间积分 (比单点更稳定)
        time_series = np.zeros(N_t)
        
        # FDTD 时间步进
        for n in range(N_t):
            # 二阶导数
            d2R = np.zeros(N_rho)
            d2R[1:-1] = (R[2:] - 2*R[1:-1] + R[:-2]) / d_rho**2
            
            # 一阶导数
            dR = np.zeros(N_rho)
            dR[1:-1] = (R[2:] - R[:-2]) / (2*d_rho)
            dR[0] = (R[1] - R[0]) / d_rho
            dR[-1] = (R[-1] - R[-2]) / d_rho
            
            # 波动方程
            rhs = c**2 * (d2R + dR/rho - (m**2/rho**2 + K_eff_sq)*R)
            
            # 边界条件
            if m != 0:
                rhs[0] = 0  # R(0) = 0 for m≠0
            rhs[-1] = 0  # R(ρ_max) = 0
            
            # Verlet
            R_next = 2*R - R_prev + dt**2 * rhs
            if m != 0:
                R_next[0] = 0
            R_next[-1] = 0
            
            R_prev = R.copy()
            R = R_next.copy()
            
            # 记录: 空间积分 (投影到本征模上)
            time_series[n] = np.sum(R * R_init * rho) * d_rho
        
        # FFT 提取频率
        # 减去直流分量
        ts = time_series - np.mean(time_series)
        
        freqs = fftfreq(N_t, dt) * 2 * np.pi
        spectrum = np.abs(fft(ts))
        
        pos_mask = freqs > 0.01  # 排除接近零的频率
        freqs_pos = freqs[pos_mask]
        spectrum_pos = spectrum[pos_mask]
        
        if len(spectrum_pos) > 0:
            peak_idx = np.argmax(spectrum_pos)
            omega_num = freqs_pos[peak_idx]
        else:
            omega_num = 0.0
        
        # FFT 分辨率
        df = 2*np.pi / (N_t * dt)
        
        results[mode['label']] = {
            'omega_analytical': omega_ana,
            'omega_numerical': omega_num,
            'error': abs(omega_num - omega_ana) / max(omega_ana, 1e-10) * 100,
            'df_resolution': df,
            'time_series': time_series,
            'spectrum': spectrum_pos,
            'freqs': freqs_pos,
        }
        
        status = "✓" if results[mode['label']]['error'] < 5 else "△"
        print(f"\n  模式: {mode['label']}")
        print(f"    K = {K:.4f}, (k-βm) = {mode['k'] - beta*m:.4f}")
        print(f"    解析频率: ω = {omega_ana:.4f}")
        print(f"    数值频率: ω = {omega_num:.4f} (FFT分辨率: {df:.4f})")
        print(f"    相对误差: {results[mode['label']]['error']:.2f}%  {status}")
    
    # 绘图
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # (a) 时间序列对比 (m=+1 vs m=-1)
    ax = axes[0, 0]
    for label in ['m=+1, k=2.0', 'm=-1, k=2.0']:
        if label in results:
            ts = results[label]['time_series']
            t = np.arange(len(ts)) * dt
            ax.plot(t[:800], ts[:800], label=label)
    ax.set_xlabel('Time', fontsize=11)
    ax.set_ylabel('Projection ⟨R|R₀⟩', fontsize=11)
    ax.set_title('(a) Time Series: Chiral Modes', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # (b) 频谱对比
    ax = axes[0, 1]
    for label in ['m=+1, k=2.0', 'm=-1, k=2.0', 'm=+0, k=2.0']:
        if label in results:
            r = results[label]
            spec_norm = r['spectrum'] / max(r['spectrum']) if max(r['spectrum']) > 0 else r['spectrum']
            ax.plot(r['freqs'], spec_norm, label=label)
            ax.axvline(x=r['omega_analytical'], color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('ω', fontsize=11)
    ax.set_ylabel('|FFT| (normalized)', fontsize=11)
    ax.set_title('(b) Frequency Spectrum', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 8)
    
    # (c) 色散关系验证: ω vs m
    ax = axes[1, 0]
    m_vals = [-2, -1, 0, 1, 2]
    k_test = 2.0
    omega_num = []
    omega_ana = []
    for m in m_vals:
        label_key = f'm={m:+d}, k={k_test}'
        if label_key in results:
            omega_num.append(results[label_key]['omega_numerical'])
            omega_ana.append(results[label_key]['omega_analytical'])
    
    ax.plot(m_vals, omega_ana, 'o-', label='Analytical (HST)', markersize=8, color='blue')
    if len(omega_num) > 0:
        ax.plot(m_vals, omega_num, 's--', label='FDTD Numerical', markersize=8, color='red')
    # 平直空间参考线
    omega_flat = [c * np.sqrt((jn_zeros(abs(m), 1)[0]/rho_max)**2 + k_test**2) for m in m_vals]
    ax.plot(m_vals, omega_flat, '^:', label='Flat space reference', markersize=8, color='green', alpha=0.5)
    ax.set_xlabel('m (angular momentum)', fontsize=11)
    ax.set_ylabel('ω', fontsize=11)
    ax.set_title(f'(c) Dispersion: ω vs m (k={k_test}, β={beta})', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # (d) 近零能模式
    ax = axes[1, 1]
    zero_label = f'm=+1, k=β (near-zero mode, ω=cK={omega_zero:.4f})'
    if zero_label in results:
        ts = results[zero_label]['time_series']
        t = np.arange(len(ts)) * dt
        ax.plot(t[:1500], ts[:1500], label=f'Near-zero mode (ω={omega_zero:.3f})')
        # 叠加 cos(ωt) 验证
        ax.plot(t[:1500], np.cos(omega_zero * t[:1500]) * max(abs(ts[:1500])), 
                'r--', alpha=0.5, label=f'cos({omega_zero:.3f}·t)')
        ax.set_xlabel('Time', fontsize=11)
        ax.set_ylabel('⟨R|R₀⟩', fontsize=11)
        ax.set_title('(d) Near-Zero Mode (k=βm)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_fdtd_verification.png'), dpi=150)
    plt.close()
    print("\n✓ 图已保存: fig2_fdtd_verification.png")
    
    return results

# ============================================================
# 验证 3: 手征分裂的精确测量
# ============================================================
def verify_chiral_splitting():
    """精确验证 Δω = 2cβ"""
    print("\n" + "=" * 60)
    print("验证 3: 手征分裂 Δω = 2cβ")
    print("=" * 60)
    
    beta_values = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    k = 3.0
    m = 1
    
    delta_omega_predicted = []
    delta_omega_actual = []
    
    for b in beta_values:
        omega_plus = c * abs(k - b * m)
        omega_minus = c * abs(k - b * (-m))
        delta = omega_plus - omega_minus
        delta_omega_actual.append(delta)
        delta_omega_predicted.append(-2 * c * b)  # 高频极限预测
    
    print(f"\n  k = {k}, m = {m}")
    print(f"  {'β':>6} | {'ω(+m)':>8} | {'ω(-m)':>8} | {'Δω实际':>8} | {'Δω预测':>8} | {'一致':>4}")
    print("  " + "-" * 55)
    
    for i, b in enumerate(beta_values):
        match = "✓" if abs(delta_omega_actual[i] - delta_omega_predicted[i]) < 0.01 else "✗"
        print(f"  {b:6.2f} | {c*abs(k-b*m):8.4f} | {c*abs(k+b*m):8.4f} | "
              f"{delta_omega_actual[i]:8.4f} | {delta_omega_predicted[i]:8.4f} | {match:>4}")
    
    # 绘图
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(beta_values, delta_omega_predicted, 'r--', linewidth=2, label='Predicted: Δω = -2cβ')
    ax.plot(beta_values, delta_omega_actual, 'bo', markersize=8, label='Actual')
    ax.set_xlabel('β', fontsize=12)
    ax.set_ylabel('Δω = ω(+m) - ω(-m)', fontsize=12)
    ax.set_title(f'Chiral Splitting Verification (k={k}, m={m})', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig3_chiral_splitting.png'), dpi=150)
    plt.close()
    print("\n✓ 图已保存: fig3_chiral_splitting.png")

# ============================================================
# 验证 4: Bessel 函数径向解
# ============================================================
def verify_bessel_solutions():
    """验证径向解 R(ρ) = J_m(Kρ)"""
    print("\n" + "=" * 60)
    print("验证 4: Bessel 函数径向解")
    print("=" * 60)
    
    rho = np.linspace(0.1, 10, 500)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 左图: 不同 m 的 Bessel 函数
    ax = axes[0]
    for m in [0, 1, 2, 3]:
        K = 1.0
        R = bessel_j(m, K * rho)
        ax.plot(rho, R, label=f'J_{m}(ρ)')
    ax.set_xlabel('ρ', fontsize=11)
    ax.set_ylabel('R(ρ)', fontsize=11)
    ax.set_title('(a) Radial Modes: J_m(Kρ)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    
    # 右图: 零能模式的幂律解
    ax = axes[1]
    for m in [1, 2, 3, 4]:
        R = rho ** m
        R = R / max(R)  # 归一化
        ax.plot(rho, R, label=f'ρ^{m}')
    ax.set_xlabel('ρ', fontsize=11)
    ax.set_ylabel('R(ρ) (normalized)', fontsize=11)
    ax.set_title('(b) Zero Mode: R ∝ ρ^|m|', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig4_bessel_modes.png'), dpi=150)
    plt.close()
    print("✓ 图已保存: fig4_bessel_modes.png")

# ============================================================
# 验证 5: 有效质量
# ============================================================
def verify_effective_mass():
    """验证光子有效质量 m_eff"""
    print("\n" + "=" * 60)
    print("验证 5: 光子有效质量 m_eff")
    print("=" * 60)
    
    # m_eff² c⁴ = -2ℏc²βm·p_z + ℏ²c²(β²m² + K²)
    # 自然单位 ℏ=c=1: m_eff² = -2βm·k + β²m² + K²
    
    k_values = np.linspace(0.1, 5, 200)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 左图: m_eff vs k
    ax = axes[0]
    for m in [1, 2, -1, -2]:
        K = 0
        m_eff_sq = -2 * beta * m * k_values + beta**2 * m**2 + K**2
        m_eff_sq = np.maximum(m_eff_sq, 0)  # 防止负值
        m_eff = np.sqrt(m_eff_sq)
        ax.plot(k_values, m_eff, label=f'm={m:+d}, K=0')
    ax.set_xlabel('k (axial momentum)', fontsize=11)
    ax.set_ylabel('m_eff (effective mass)', fontsize=11)
    ax.set_title(f'(a) Effective Mass vs k (β={beta})', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 3)
    
    # 右图: 色散关系 E vs p_z
    ax = axes[1]
    for m in [0, 1, -1, 2]:
        E = np.abs(k_values - beta * m)  # E = ω in natural units
        ax.plot(k_values, E, label=f'm={m}')
    ax.plot(k_values, k_values, 'k--', alpha=0.3, label='Light cone (m=0)')
    ax.set_xlabel('p_z = k', fontsize=11)
    ax.set_ylabel('E = ω', fontsize=11)
    ax.set_title('(b) Energy-Momentum Relation', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig5_effective_mass.png'), dpi=150)
    plt.close()
    print("✓ 图已保存: fig5_effective_mass.png")

# ============================================================
# 验证 6: Christoffel 符号与测地线
# ============================================================
def verify_christoffel_and_geodesics():
    """验证 Christoffel 符号和测地线方程"""
    print("\n" + "=" * 60)
    print("验证 6: Christoffel 符号与测地线")
    print("=" * 60)
    
    # 非零 Christoffel 符号:
    # Γ^ρ_{χχ} = -ρ
    # Γ^ρ_{χζ} = -βρ
    # Γ^ρ_{ζζ} = -β²ρ
    # Γ^χ_{ρχ} = 1/ρ
    # Γ^χ_{ρζ} = β/ρ
    
    # 验证 Ricci 张量为零 (数值)
    rho_vals = np.array([0.5, 1.0, 2.0, 5.0])
    
    print(f"\n  β = {beta}")
    print(f"  Ricci 张量数值验证 (应全部为零):")
    
    for rho in rho_vals:
        # Christoffel 符号
        G_rho_chi_chi = -rho
        G_rho_chi_zeta = -beta * rho
        G_rho_zeta_zeta = -beta**2 * rho
        G_chi_rho_chi = 1 / rho
        G_chi_rho_zeta = beta / rho
        
        # R_ρρ (简化计算)
        # R_ρρ = ∂_λ Γ^λ_{ρρ} - ∂_ρ Γ^λ_{ρλ} + ΓΓ - ΓΓ
        # Γ^λ_{ρρ} = 0, Γ^λ_{ρλ} = Γ^χ_{ρχ} = 1/ρ
        # ∂_ρ(1/ρ) = -1/ρ²
        
        # 完整计算 (使用修正后的 Christoffel):
        # R_ρρ = 0 - (-1/ρ²) + 0 - [(1/ρ)² + (β/ρ)(0) + (0)(β/ρ) + 0]
        # 等等, 让我用完整公式
        
        # R_ρρ = -∂_ρ(Γ^χ_{ρχ}) - Σ Γ^λ_{ρσ}Γ^σ_{ρλ}
        #      = -(-1/ρ²) - (1/ρ)² = 1/ρ² - 1/ρ² = 0
        R_rho_rho = 1/rho**2 - 1/rho**2
        
        # R_χχ = ∂_ρ(-ρ) + (1/ρ)(-ρ) - [(-ρ)(1/ρ) + (1/ρ)(-ρ)]
        #      = -1 - 1 - (-2) = 0
        R_chi_chi = -1 + (1/rho)*(-rho) - ((-rho)*(1/rho) + (1/rho)*(-rho))
        
        # R_ζζ = ∂_ρ(-β²ρ) + (1/ρ)(-β²ρ) - [(-βρ)(β/ρ) + (β/ρ)(-βρ)]
        #      = -β² - β² - (-2β²) = 0
        R_zeta_zeta = -beta**2 + (1/rho)*(-beta**2*rho) - ((-beta*rho)*(beta/rho) + (beta/rho)*(-beta*rho))
        
        # R_χζ = ∂_ρ(-βρ) + (1/ρ)(-βρ) - [(-βρ)(1/ρ) + (β/ρ)(-ρ)]
        #      = -β - β - (-2β) = 0
        R_chi_zeta = -beta + (1/rho)*(-beta*rho) - ((-beta*rho)*(1/rho) + (beta/rho)*(-rho))
        
        print(f"    ρ = {rho:.1f}: R_ρρ={R_rho_rho:.2e}, R_χχ={R_chi_chi:.2e}, "
              f"R_ζζ={R_zeta_zeta:.2e}, R_χζ={R_chi_zeta:.2e}")
    
    print("\n  ✓ Ricci 张量全部分量为零 — 确认 R_μν = 0")
    
    # 测地线模拟
    print(f"\n  测地线数值积分:")
    
    from scipy.integrate import solve_ivp
    
    def geodesic_rhs(t, y, beta, ell, P):
        """
        y = [rho, rho_dot, chi, zeta]
        守恒量: ell = ρ²(χ̇ + βζ̇), P = βℓ + ζ̇
        """
        rho, rho_dot, chi, zeta = y
        
        if rho < 0.01:
            rho = 0.01
        
        # 从守恒量解出速度
        zeta_dot = P - beta * ell
        chi_dot = ell / rho**2 - beta * zeta_dot
        
        # 径向加速度: ρ̈ = ℓ²/ρ³
        rho_ddot = ell**2 / rho**3
        
        return [rho_dot, rho_ddot, chi_dot, zeta_dot]
    
    # 测试: 有角动量的光子
    ell = 1.0
    P = 2.0
    rho0 = 2.0
    rho_dot0 = 0.0  # 初始径向速度为零 (圆轨道)
    
    # 检查是否满足类光条件: E²/c² = ρ̇² + ℓ²/ρ² + (P-βℓ)²
    E_sq = rho_dot0**2 + ell**2/rho0**2 + (P - beta*ell)**2
    E = np.sqrt(E_sq)
    
    print(f"    参数: ℓ={ell}, P={P}, ρ₀={rho0}, β={beta}")
    print(f"    能量: E = {E:.4f}")
    print(f"    ζ̇ = P - βℓ = {P - beta*ell:.4f}")
    print(f"    φ̇_lab = ℓ/ρ² = {ell/rho0**2:.4f}")
    
    # 类光条件验证
    v_z = (P - beta * ell) / E
    v_phi = ell / (rho0 * E)
    v_total = np.sqrt(v_z**2 + v_phi**2)
    print(f"    v_z = {v_z:.4f}, v_φ = {v_phi:.4f}")
    print(f"    |v| = {v_total:.6f} (应为 1.000000)")
    
    # 数值积分
    sol = solve_ivp(geodesic_rhs, [0, 20], [rho0, rho_dot0, 0, 0],
                     args=(beta, ell, P), dense_output=True,
                     max_step=0.01)
    
    t = np.linspace(0, 20, 1000)
    y = sol.sol(t)
    rho_t = y[0]
    chi_t = y[2]
    zeta_t = y[3]
    
    # 转换到实验室坐标
    phi_t = chi_t + beta * zeta_t
    x_lab = rho_t * np.cos(phi_t)
    y_lab = rho_t * np.sin(phi_t)
    z_lab = zeta_t
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # (a) 2D 投影轨迹 (x-y plane)
    ax = axes[0]
    ax.plot(x_lab, y_lab, linewidth=1.5, color='blue')
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.set_title('(a) Geodesic Projection (x-y plane)', fontsize=12)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    # (b) 径向振荡
    ax = axes[1]
    ax.plot(t, rho_t, linewidth=1.5)
    ax.set_xlabel('t (affine parameter)', fontsize=11)
    ax.set_ylabel('ρ', fontsize=11)
    ax.set_title('(b) Radial Evolution', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # (c) 速度验证
    ax = axes[2]
    v_z_t = (P - beta * ell) / E * np.ones_like(t)
    v_phi_t = ell / (rho_t * E)
    v_total_t = np.sqrt(v_z_t**2 + v_phi_t**2)
    ax.plot(t, v_z_t, label='v_z')
    ax.plot(t, v_phi_t, label='v_φ')
    ax.plot(t, v_total_t, 'k--', label='|v| (should be 1)')
    ax.set_xlabel('t', fontsize=11)
    ax.set_ylabel('velocity components', fontsize=11)
    ax.set_title('(c) Velocity (should sum to c=1)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig6_geodesics.png'), dpi=150)
    plt.close()
    print("\n✓ 图已保存: fig6_geodesics.png")

# ============================================================
# 验证 7: 综合汇总表
# ============================================================
def print_summary():
    """打印所有验证结果的汇总表"""
    print("\n" + "=" * 60)
    print("HST 数值验证 — 综合汇总")
    print("=" * 60)
    
    print("""
┌──────────────────────────────────────────────────────────────────┐
│                    验证结果汇总                                     │
├──────────────────────────┬────────────┬───────────────────────────┤
│ 检验项                    │ 结果       │ 说明                      │
├──────────────────────────┼────────────┼───────────────────────────┤
│ R_μν = 0 (Ricci 张量)    │ ✓ PASS     │ 所有分量为零               │
│ 色散 ω = c|k-βm|         │ ✓ PASS     │ FDTD 与解析一致            │
│ 手征分裂 Δω = 2cβ        │ ✓ PASS     │ 高频极限精确成立           │
│ 零能模式 ω=0 @ k=βm      │ ✓ PASS     │ 场不振荡                   │
│ Bessel 径向解             │ ✓ PASS     │ J_m(Kρ) 满足方程          │
│ 有效质量 m_eff            │ ✓ PASS     │ 与色散关系一致             │
│ 测地线 |v| = c            │ ✓ PASS     │ 光速不变                   │
│ 守恒量 ℓ, P               │ ✓ PASS     │ 沿测地线恒定               │
│ β→0 回退                  │ ✓ PASS     │ 回到平直柱坐标             │
│ 因果结构                  │ ✓ PASS     │ 光锥不变                   │
├──────────────────────────┼────────────┼───────────────────────────┤
│ 总体判定                  │ ALL PASS   │ 理论自洽                    │
└──────────────────────────┴────────────┴───────────────────────────┘
""")

# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     螺旋空间理论 (HST) 数值验证框架 v1.0                  ║")
    print("║     Helical Space Theory — Numerical Verification        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    verify_dispersion_analytical()
    fdtd_helical_wave()
    verify_chiral_splitting()
    verify_bessel_solutions()
    verify_effective_mass()
    verify_christoffel_and_geodesics()
    print_summary()
    
    print("\n所有验证完成。输出图片位于:", OUTPUT_DIR)
