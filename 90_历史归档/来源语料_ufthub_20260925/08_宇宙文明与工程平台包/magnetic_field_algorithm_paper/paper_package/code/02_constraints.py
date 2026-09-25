"""
Part 2: 闭环条件、光速约束、传播条件联立精算验证
        + 量纲审查
"""
import numpy as np
from scipy import special
import sympy as sp

print("=" * 70)
print("Part 2: 约束联立精算与量纲审查")
print("=" * 70)

# ============================================================
# 2.1 量纲审查
# ============================================================
print("\n【2.1】量纲审查")
print("-" * 50)

# 基本量纲: [M]=质量, [L]=长度, [T]=时间
dim = {
    'k':   {'L': -1},   # 波数
    'L':   {'L': 1},    # 长度
    'h':   {'M': 1, 'L': 2, 'T': -1},  # 普朗克常数
    'omega': {'T': -1}, # 角频率
    'c':   {'L': 1, 'T': -1},  # 光速
    'a,b': {'L': 1},    # 螺旋半径/螺距
}

print("""
  量纲分析:
  ┌─────────────┬──────────────────┬──────────┐
  │ 物理量      │ 量纲             │ 说明     │
  ├─────────────┼──────────────────┼──────────┤
  │ k_n (波数)  │ [L⁻¹]            │ 必须     │
  │ L (纵向周期)│ [L]              │ 长度     │
  │ h (普朗克)  │ [M L² T⁻¹]       │ 作用量   │
  │ ω (角频率)  │ [T⁻¹]            │          │
  │ c (光速)    │ [L T⁻¹]          │          │
  │ a,b (螺旋)  │ [L]              │ 长度     │
  └─────────────┴──────────────────┴──────────┘

  检验 k_n = 2πn / h:
    2πn/h 的量纲 = 1/[M L² T⁻¹] = [M⁻¹ L⁻² T]
    但 k_n 要求量纲 = [L⁻¹]
    ❌ 量纲不匹配!

  检验 k_n = 2πn / L:
    2πn/L 的量纲 = 1/[L] = [L⁻¹]
    ✓ 量纲正确!

  结论: 原式中 h 应为纵向周期长度 L（高度/周期），
        而非普朗克常数。否则方程量纲不自洽。
""")

# ============================================================
# 2.2 螺旋几何与光速约束
# ============================================================
print("【2.2】螺旋几何与光速约束精算")
print("-" * 50)

# 螺旋参数
a_val = 0.01    # 螺旋半径 [m]
b_val = 0.01    # 螺距参数 [m]
L_val = 1.0     # 纵向周期 [m]
c_val = 2.99792458e8  # 光速 [m/s]

# 弧长元
ds_dtheta = np.sqrt(a_val**2 + b_val**2)
print(f"\n  螺旋几何:")
print(f"    半径 a = {a_val*100} cm")
print(f"    螺距 b = {b_val*100} cm")
print(f"    ds/dθ = √(a²+b²) = {ds_dtheta:.6f} m/rad")

# 光速约束: v = ω·ds/dθ = c
omega_val = c_val / ds_dtheta
print(f"\n  光速约束 v = ω·√(a²+b²) = c:")
print(f"    ω = c/√(a²+b²) = {omega_val:.6e} rad/s")
print(f"    f = ω/(2π) = {omega_val/(2*np.pi):.6e} Hz = {omega_val/(2*np.pi)/1e9:.4f} GHz")
print(f"    T = 2π/ω = {2*np.pi/omega_val:.6e} s")

# 验证: v = ω·√(a²+b²)
v_check = omega_val * ds_dtheta
print(f"\n  验证: v = ω·√(a²+b²) = {v_check:.6e} m/s")
print(f"        c           = {c_val:.6e} m/s")
print(f"        误差 = {abs(v_check - c_val)/c_val*100:.2e} %")

# ============================================================
# 2.3 纵向量子化与传播条件
# ============================================================
print(f"\n【2.3】纵向量子化 k_n = 2πn/L 与传播条件 κ²≥0")
print("-" * 50)

print(f"\n  L = {L_val} m")
print(f"  κ_n² = ω²/c² - k_n² = 1/(a²+b²) - (2πn/L)²")
print(f"  传播条件: κ_n² ≥ 0  →  n ≤ L/(2π√(a²+b²))")

n_max = int(L_val / (2 * np.pi * ds_dtheta))
print(f"  n_max = floor(L/(2π√(a²+b²))) = floor({L_val/(2*np.pi*ds_dtheta):.4f}) = {n_max}")

# 列出所有传播模态
print(f"\n  {'n':>3} {'k_n [rad/m]':>14} {'κ_n² [1/m²]':>14} {'κ_n [1/m]':>12} {'状态':>6}")
print("  " + "-" * 55)
modes = []
for n in range(1, n_max + 3):
    kn = 2 * np.pi * n / L_val
    kappa2 = 1.0 / (a_val**2 + b_val**2) - kn**2
    if kappa2 >= 0:
        kappa = np.sqrt(kappa2)
        status = "传播"
        modes.append((n, kn, kappa))
    else:
        kappa = np.sqrt(-kappa2) * 1j
        status = "倏逝"
    print(f"  {n:3d} {kn:14.6f} {kappa2:14.4f} {str(kappa):>12} {status:>6}")

print(f"\n  → 共 {len(modes)} 个传播模态 (n=1..{n_max})")

# ============================================================
# 2.4 相位匹配一致性检验
# ============================================================
print(f"\n【2.4】相位匹配一致性检验（关键审查）")
print("-" * 50)

print("""
  场解: B = A·J_m(κr)·e^{i(mθ - k_n z - ω_n t)}
  螺旋轨迹: r=a, z=bθ

  沿螺旋轨迹, 相位 φ = mθ - k_n·bθ - ω_n t = (m - k_n b)θ - ω_n t

  若场沿螺旋以角速度 ω_rot 运动 (θ = ω_rot·t):
    φ(t) = (m - k_n b)ω_rot·t - ω_n·t
    恒定相位(刚性运动)要求: (m - k_n b)ω_rot = ω_n
    => ω_rot = ω_n / (m - k_n b)

  螺旋线速度: v = ω_rot · √(a²+b²)
    = ω_n · √(a²+b²) / (m - k_n b)

  设 v = c, 则:
    ω_n = c·(m - k_n b) / √(a²+b²)
""")

# 数值检验
print(f"  数值检验 (取 m=1, n=1):")
for m_test in [0, 1, 2]:
    kn1 = 2 * np.pi * 1 / L_val
    omega_n1 = c_val * (m_test - kn1 * b_val) / ds_dtheta
    print(f"    m={m_test}: ω_n = c·(m - k₁b)/√(a²+b²) = {omega_n1:.4e} rad/s", end="")
    if abs(omega_n1) > 0:
        f1 = omega_n1 / (2*np.pi)
        print(f"  (f={f1/1e9:.4f} GHz)")
    else:
        print(f"  → ω=0 静场!")

print("""
  ⚠ 重要发现:
  用户原约束 v = ω√(a²+b²) = c 隐含假设 ω_rot = ω_n,
  即 m - k_n b = 1, 亦即 b = (m-1)/k_n = (m-1)L/(2πn)。

  这是一个额外的螺距量子化条件!
  若不满足, 则螺旋线速度不等于 ω_n√(a²+b²),
  光速约束需修正为:
    ω_n = c·(m - k_n b) / √(a²+b²)

  联立: b = (m-1)L/(2πn) 时, 两个表述等价。
""")

# ============================================================
# 2.5 完整联立求解（含螺距量子化）
# ============================================================
print(f"【2.5】完整联立求解（含螺距量子化 b=(m-1)/k_n）")
print("-" * 50)

# 修正后的自洽系统:
# (1) k_n = 2πn/L
# (2) b_nm = (m-1)/k_n = (m-1)L/(2πn)   [螺距量子化, 来自相位匹配]
# (3) ω_nm = c/√(a² + b_nm²)             [光速约束]
# (4) κ² = ω²/c² - k_n² = 1/(a²+b²) - k_n² ≥ 0  [传播]

print(f"\n  修正后自洽方程组:")
print(f"    k_n     = 2πn/L")
print(f"    b_nm    = (m-1)/k_n = (m-1)L/(2πn)")
print(f"    ω_nm    = c / √(a² + b_nm²)")
print(f"    κ²      = 1/(a²+b_nm²) - k_n² ≥ 0")

# 数值求解
print(f"\n  参数: a={a_val}m, L={L_val}m")
print(f"\n  {'n':>3} {'m':>3} {'b_nm [m]':>12} {'ω_nm [rad/s]':>14} {'κ² [1/m²]':>12} {'传播?':>6}")
print("  " + "-" * 60)

solutions = []
for n in range(1, 6):
    kn = 2 * np.pi * n / L_val
    for m in range(0, 5):
        if m == 0:
            b_nm = 0  # m=0 特殊处理
        else:
            b_nm = (m - 1) / kn
        denom = np.sqrt(a_val**2 + b_nm**2)
        if denom < 1e-30:
            continue
        omega_nm = c_val / denom
        kappa2 = 1.0 / (a_val**2 + b_nm**2) - kn**2
        prop = "✓" if kappa2 >= 0 else "✗"
        print(f"  {n:3d} {m:3d} {b_nm:12.6f} {omega_nm:14.4e} {kappa2:12.2f} {prop:>6}")
        if kappa2 >= 0:
            solutions.append((n, m, b_nm, omega_nm, np.sqrt(kappa2)))

print(f"\n  自洽传播解数: {len(solutions)}")

# ============================================================
# 2.6 与传统圆波导对比
# ============================================================
print(f"\n【2.6】与传统圆波导对比")
print("-" * 50)

R_wg = 0.01  # 波导半径 1cm
# 传统圆波导 TE_{m,p} 模式: J'_m(κR)=0, 截止频率 f_c = κ_{mp}c/(2π)
# TM_{m,p}: J_m(κR)=0
# 取 TM 模式: J_m(x)=0 的根
print(f"\n  传统圆波导 (R={R_wg*100}cm) 对比:")
print(f"  {'模式':>8} {'κ·R (贝塞尔零点)':>18} {'f_c [GHz]':>12}")
print("  " + "-" * 40)
for m in range(0, 3):
    # J_m 前2个零点
    zeros = special.jn_zeros(m, 2)
    for p, z in enumerate(zeros):
        fc = z * c_val / (2 * np.pi * R_wg)
        print(f"  TM_{m}{p+1:<5d} {z:18.6f} {fc/1e9:12.4f}")

print("""
  对比要点:
  ┌──────────────┬─────────────────────┬──────────────────────┐
  │ 维度         │ 传统圆波导          │ 本闭环螺旋算法       │
  ├──────────────┼─────────────────────┼──────────────────────┤
  │ 径向量子化   │ J_m(κR)=0 (壁边界)  │ 无径向壁, κ自由      │
  │ 角向量子化   │ m∈Z (相同)          │ m∈Z (相同)           │
  │ 纵向量子化   │ k连续               │ k_n=2πn/L (离散)     │
  │ 频率关系     │ ω²=c²(k²+κ²)        │ ω=c/√(a²+b²) (固定)  │
  │ 螺距         │ 无概念              │ b=(m-1)L/(2πn) (量子)│
  │ 截止         │ f>f_c 才传播        │ n≤L/(2π√(a²+b²))    │
  │ 物理图像     │ 导行波              │ 闭环螺旋光速流       │
  └──────────────┴─────────────────────┴──────────────────────┘
""")

# 保存解数据供可视化使用
np.savez('/home/user/Doubao/chats/38442004002046210/modes.npz',
         a=a_val, b=b_val, L=L_val, c=c_val,
         ds_dtheta=ds_dtheta, omega_val=omega_val,
         n_max=n_max, solutions=np.array(solutions, dtype=object),
         modes=np.array([(m[0], m[1], m[2]) for m in modes]))
print("解数据已保存。")
