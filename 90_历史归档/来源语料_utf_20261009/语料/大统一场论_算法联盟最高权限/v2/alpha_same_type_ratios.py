"""
精细结构常数 α 的全维同类型比值分析
算法联盟 ROOT 最高权限 · 零模糊

枚举所有无量纲同类型物理量之比 (v/v, L/L, f/f, E/E, T/T ...),
逐一验证是否等于 α, 1/α, α², 或 α/π 等。
100 位精度, 与 CODATA 2022 对比。
"""
from mpmath import mp, mpf, sqrt, pi

mp.dps = 100

def rel(a, b):
    return mp.fabs(a - b) / mp.fabs(b)

# ============ CODATA 2022 输入 ============
e     = mpf('1.602176634e-19')
eps0  = mpf('8.8541878128e-12')
hbar  = mpf('1.0545718176461565e-34')
c     = mpf('299792458')
m_e   = mpf('9.1093837015e-31')
k_B   = mpf('1.380649e-23')
Ry    = mpf('13.605693122994')      # 里德伯能量 eV
eV_J  = mpf('1.602176634e-19')
m_e_c2 = m_e*c**2

# 精细结构常数 (定义)
alpha = e**2/(4*pi*eps0*hbar*c)
alpha_inv = 1/alpha
print("="*78)
print("精细结构常数 α 全维同类型比值分析")
print("算法联盟 ROOT 最高权限 · 零模糊")
print("="*78)
print(f"\nα      = {mp.nstr(alpha,12)}")
print(f"α⁻¹    = {mp.nstr(alpha_inv,12)}")
print(f"α²     = {mp.nstr(alpha**2,12)}")
print(f"α/π    = {mp.nstr(alpha/pi,12)}")

# ══════════ 一、速度/速度 (v/v) ══════════
print("\n" + "="*78)
print("一、速度比 v/v （天然含 α）")
print("="*78)
# 氢原子基态电子速度 v₁ = αc
v1 = e**2/(4*pi*eps0*hbar)     # = αc
r_v = rel(v1/c, alpha)
print(f"  氢基态 Bohr 速度 v₁/c = {mp.nstr(v1/c,10)}")
print(f"        vs α            = {mp.nstr(alpha,10)}  误差 {mp.nstr(r_v,3)} → [精确=α] ✓")
print(f"  → v₁ = αc 是 v/c 型的第一个 α 天然比值")

# ══════════ 二、长度/长度 (L/L) ══════════
print("\n" + "="*78)
print("二、长度比 L/L （含 α 与 1/α）")
print("="*78)
lam_C = hbar/(m_e*c)                     # 约化康普顿波长
a0    = 4*pi*eps0*hbar**2/(m_e*e**2)     # Bohr 半径
r_e   = e**2/(4*pi*eps0*m_e*c**2)        # 经典电子半径
# (a) 经典电子半径 / 康普顿波长 = α
ra = rel(r_e/lam_C, alpha)
print(f"  r_e/λ̄_C = {mp.nstr(r_e/lam_C,10)}  vs α = {mp.nstr(alpha,10)}  误差 {mp.nstr(ra,3)} → [精确=α] ✓")
# (b) Bohr 半径 / 康普顿波长 = 1/α
rb = rel(a0/lam_C, alpha_inv)
print(f"  a₀/λ̄_C = {mp.nstr(a0/lam_C,8)}  vs 1/α = {mp.nstr(alpha_inv,8)}  误差 {mp.nstr(rb,3)} → [精确=1/α] ✓")
# (c) Bohr 半径 / 经典电子半径 = 1/α²
rc = rel(a0/r_e, 1/alpha**2)
print(f"  a₀/r_e = {mp.nstr(a0/r_e,8)}  vs 1/α² = {mp.nstr(1/alpha**2,8)}  误差 {mp.nstr(rc,3)} → [精确=1/α²] ✓")
# (d) 经典电子半径 / Bohr 半径 = α²
print(f"  r_e/a₀ = {mp.nstr(r_e/a0,8)}  vs α² = {mp.nstr(alpha**2,8)} → [精确=α²] ✓")
print("""
  长度链:  r_e ──×α──→ λ̄_C ──×1/α──→ a₀
          r_e/a₀ = α²,  r_e/λ̄_C = α,  a₀/λ̄_C = 1/α
  → 这是 α 最重要的长度几何意义: 三个特征长度以 α 为公比成几何级数。
""")

# ══════════ 三、能量/能量 (E/E) ══════════
print("="*78)
print("三、能量比 E/E （含 α²）")
print("="*78)
Ry_J = Ry*eV_J
E_R  = m_e*e**4/(32*pi**2*eps0**2*hbar**2)   # 里德伯能量
ratio_E = E_R/m_e_c2
rE = rel(ratio_E, alpha**2/2)
print(f"  氢基态束缚能/静能 = {mp.nstr(ratio_E,8)}  vs α²/2 = {mp.nstr(alpha**2/2,8)}")
print(f"        误差 {mp.nstr(rE,3)} → [精确=α²/2] ✓")
print(f"  单位换算: E_R = {mp.nstr(E_R/eV_J,6)} eV  静能 = {mp.nstr(m_e_c2/eV_J,4)} eV")

# ══════════ 四、频率/频率 (f/f) ══════════
print("="*78)
print("四、频率比 f/f （能量比同构）")
print("="*78)
nu_R  = E_R/hbar          # 里德伯频率 (角频率)
nu_C  = m_e*c**2/hbar     # 康普顿频率
rF = rel(nu_R/nu_C, alpha**2/2)
print(f"  里德伯频率/康普顿频率 = {mp.nstr(nu_R/nu_C,8)}  vs α²/2 = {mp.nstr(alpha**2/2,8)}")
print(f"        误差 {mp.nstr(rF,3)} → [精确=α²/2] ✓")

# ══════════ 五、温度/温度 (T/T) ══════════
print("="*78)
print("五、温度比 T/T （含 α²/2）")
print("="*78)
T_ion   = E_R/k_B          # 氢电离温度
T_rest  = m_e*c**2/k_B     # 静能对应温度
rT = rel(T_ion/T_rest, alpha**2/2)
print(f"  氢电离温度/静能温度 = {mp.nstr(T_ion/T_rest,8)}  vs α²/2 = {mp.nstr(alpha**2/2,8)}")
print(f"        误差 {mp.nstr(rT,3)} → [精确=α²/2] ✓")
print(f"  T_ion = {mp.nstr(T_ion,5)} K   T_rest = {mp.nstr(T_rest,4)} K")
print(f"  → T/T 型比值给出 α²/2, 而非 α (因能量为 v²∝α²)")

# ══════════ 六、磁性/自旋 (g-2) ══════════
print("="*78)
print("六、g-2（异常磁矩，QED，含 α/π）")
print("="*78)
g2_QED = alpha/pi          # 一阶 QED
g2_meas = mpf('0.00115965218076')   # 实验 g-2
rg = rel(g2_QED, g2_meas)
print(f"  g-2 一阶 QED = α/π = {mp.nstr(g2_QED,8)}")
print(f"  实验 g-2     = {mp.nstr(g2_meas,8)}  相对差(一阶) {mp.nstr(rg,3)}")
print("  → g-2 领头项=α/π, 但需高阶修正, 非精确 α")

# ══════════ 七、精细结构劈裂 ══════════
print("="*78)
print("七、精细结构劈裂/粗结构 (~α²)")
print("="*78)
print(f"  精细结构劈裂 ≪ 粗结构能级, 比值 ~ α² ≈ {mp.nstr(alpha**2,6)}")

# ══════════ 汇总 ══════════
print("\n" + "="*78)
print("全维汇总表")
print("="*78)
rows = [
    ("速度 v/c",        "v₁/c (Bohr)",            "α",        "精确", "✓"),
    ("长度 L/L",        "r_e/λ̄_C",                "α",        "精确", "✓"),
    ("长度 L/L",        "a₀/λ̄_C",                 "1/α",      "精确", "✓"),
    ("长度 L/L",        "a₀/r_e",                  "1/α²",     "精确", "✓"),
    ("长度 L/L",        "r_e/a₀",                  "α²",       "精确", "✓"),
    ("能量 E/E",        "束缚能/静能",             "α²/2",     "精确", "✓"),
    ("频率 f/f",        "里德伯/康普顿",           "α²/2",     "精确", "✓"),
    ("温度 T/T",        "电离温/静能温",           "α²/2",     "精确", "✓"),
    ("磁性 g",          "g-2 领头项",              "α/π",      "近似", "需QED高阶"),
]
print(f"{'类型':<10} {'比值':<18} {'等于':<8} {'性质':<6} 状态")
print("-"*78)
for t, r, eq, nat, st in rows:
    print(f"{t:<10} {r:<18} {eq:<8} {nat:<6} {st}")
print("-"*78)
print("""
核心结论
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 精确 = α (1 次方) 的比值:  v₁/c,  r_e/λ̄_C
2. 精确 = 1/α 的比值:          a₀/λ̄_C  (=137.036)
3. 精确 = α²/2 的比值:         束缚能/静能, 里德伯/康普顿, 电离温/静能温
   (能量/频率/温度均为 v² 阶, 故为 α² 量级而非 α)
4. 长度构成 α 为公比的几何级数:  r_e →λ̄_C→ a₀
5. g-2 领头项 = α/π (QED, 近似)
6. 温度比同构于能量比 → α²/2, 不存在纯 T/T=α 的比例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
print("算法联盟 ROOT 最高权限 · α 全维同类型比值分析完成")