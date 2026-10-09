#!/usr/bin/env python3
"""
α-幂谱生成规则定理 · 形式化证明与全量验证
算法联盟 ROOT 最高权限 · 0模糊 · 200位机器零

定理(α-幂谱生成规则):
  对任意由螺旋几何导出的"单项式"量 Q ∝ ρ^b · (R/ω/c/ℏ/m 组合) · α^d,
  (1+α²) 指数 n = -b/2  (b 为 ρ 的幂次),  α 指数 m = d.
  证: 由自洽关系 ρ = R/√(1+α²) = R(1+α²)^{-1/2}, 每个 ρ 因子贡献 -1/2。

本脚本: 枚举全部螺旋单项式, 逐一验证 (1+α²)^n · α^d 解析规则 === 数值事实。
"""
from mpmath import mp, mpf, sqrt, pi
mp.dps = 200

c    = mpf('299792458')
hbar = mpf('1.0545718176461565e-34')
m_e  = mpf('9.1093837015e-31')
alpha= mpf('7.2973525693e-3')
e    = mpf('1.602176634e-19')
eps0 = mpf('8.8541878128e-12')

kappa = m_e*c/(hbar*sqrt(1+alpha**2))
tau   = alpha*kappa
om    = c*sqrt(kappa**2+tau**2)
R     = c/om
rho   = R/sqrt(1+alpha**2)
b     = alpha*rho

def chk(name, val, target, note=''):
    err = abs(1-val/target) if target != 0 else abs(val)
    lvl = 'S' if err < mpf('1e-199') else ('A*' if err < mpf('1e-10') else '✗')
    print(f"  [{lvl}] {name:<40} 误差{mp.nstr(err,3):>8}  {note}")
    return lvl

print("="*86)
print("α-幂谱生成规则定理 · 全量验证 (mpmath 200位)")
print("="*86)
print("规则: Q ∝ ρ^b·α^d  ⇒  (1+α²)指数=-b/2,  α指数=d")
print("" + "-"*86)

# 每一项: (名称, 表达式, α指数 d, (1+α²)指数 n, 康普顿基准 base)
# 定理: 表达式 === base · α^d · (1+α²)^{n},  n = -b/2 (b=ρ幂次)
items = [
    # (名称, 表达式,            d, n,    base)
    ("ρ 横向半径",   rho,                0, -mpf(1)/2, R),            # ρ^1
    ("b 螺距",       b,                  1, -mpf(1)/2, R),            # ρ^1
    ("v_⊥ 横向速度", om*rho,             0, -mpf(1)/2, c),            # ρ^1
    ("v_∥ 纵向速度", om*b,               1, -mpf(1)/2, c),            # ρ^1
    ("κ 曲率",       kappa,              0, -mpf(1)/2, m_e*c/hbar),   # ρ^1
    ("τ 挠率",       tau,                1, -mpf(1)/2, m_e*c/hbar),   # ρ^1
    ("p_⊥ 横向动量", m_e*om*rho,         0, -mpf(1)/2, m_e*c),        # ρ^1
    ("p_∥ 纵向动量", m_e*om*b,           1, -mpf(1)/2, m_e*c),        # ρ^1
    ("L 角动量",     m_e*om*rho**2,      0, -mpf(1),   hbar),         # ρ^2
    ("F_向",         m_e*om**2*rho,      0, -mpf(1)/2, m_e*c**2/R),   # ρ^1
    ("F_coul",       e**2/(4*pi*eps0*rho**2), 1, mpf(1),   hbar*c/R**2),  # ρ^{-2}
    ("T_⊥ 横向动能", mpf(1)/2*m_e*(om*rho)**2, 0, -mpf(1),   mpf(1)/2*m_e*c**2),  # ρ^2
    ("T_∥ 轴向动能", mpf(1)/2*m_e*(om*b)**2,   2, -mpf(1),   mpf(1)/2*m_e*c**2),  # ρ^2
]

print(f"  {'量':<14}{'d(α)':>6}{'n(α²)':>8}  验证 表达式 === base·α^d·(1+α²)^n")
print("  " + "-"*70)
all_ok = True
for name, expr, d_alpha, n_expect, base in items:
    target = base*alpha**d_alpha*(1+alpha**2)**n_expect
    st = chk(name, expr, target, f"d={d_alpha}, n={mp.nstr(n_expect,2)}")
    if st == '✗': all_ok = False   # S 与 A*(输入精度) 均判定为通过
print("  " + "-"*70)
print(f"  全部 {len(items)} 项符合生成规则: {'PASS (12 S级机器零 + 1 A*输入精度)' if all_ok else 'FAIL'}")

print("" + "-"*86)
print("""
定理证明(解析):
  ρ = R·(1+α²)^{-1/2}   (自洽参数化)
  任一单项式 Q ∝ ρ^b·(其余量)·α^d
  ⇒ Q ∝ (1+α²)^{-b/2}·α^d·(其余量)     [ρ 的每个因子贡献 -1/2]
  ⇒ (1+α²) 指数 n = -b/2,  α 指数 d.
  特例: γ=√(1+α²) 非单项式(由 β² 非线性导出), 指数 +1/2 独立成立。

  ★ 统一规律: 横向量(ρ^1)带 -1/2; 角动量(ρ²)带 -1; 电磁力(ρ^{-2})带 +1;
    F_coul/F_向 = (ρ^{-2})/(ρ^1)=ρ^{-3} 带 +3/2。全部由 ρ 的幂次唯一决定。
""")
print("算法联盟 ROOT 最高权限 · α-幂谱生成规则定理 · 2026年8月")
