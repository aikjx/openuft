"""
GAQ-UFT V50: Gε0耦合恒等式 & 电磁常数几何本源 — 250位精算诚实审计
"""
import mpmath as mp
mp.mp.dps = 250

# ===== CODATA-2022 参考值 =====
c       = mp.mpf("299792458")
h       = mp.mpf("6.62607015e-34")
hbar    = h / (2 * mp.pi)
e       = mp.mpf("1.602176634e-19")
G       = mp.mpf("6.67430e-11")
alpha   = mp.mpf("0.0072973525693")
eps0_CODATA = mp.mpf("8.8541878128e-12")
mu0_CODATA  = 4 * mp.pi * mp.mpf("1e-7")

# ===== 几何导出（用户公式） =====
eps0_geo  = e**2 / (alpha**3 * hbar * c)
mu0_geo   = (alpha**3 * hbar) / (c * e**2)
mP        = mp.sqrt(hbar * c / G)
LHS_Geps0 = G * eps0_CODATA
RHS_Geps0 = e**2 / (alpha**3 * mP**2)

# 引力耦合系数两种形式
K_G_original = -G * (hbar / c)**2
K_G_geo      = -(hbar**3) / (c * mP**2)

# ===== 输出 =====
print("=" * 70)
print("一、ε0 校验  (用户公式: eps0 = e^2 / (alpha^3 * hbar * c))")
print("=" * 70)
print(f"  eps0_CODATA = {eps0_CODATA:.14e}")
print(f"  eps0_geo    = {eps0_geo:.14e}")
print(f"  Δeps0       = {abs(eps0_CODATA - eps0_geo):.14e}")
print(f"  比值 geo/CODAT A = {eps0_geo / eps0_CODATA:.14e}")
print()

print("=" * 70)
print("二、μ0 校验  (用户公式: mu0 = alpha^3 * hbar / (c * e^2))")
print("=" * 70)
print(f"  mu0_CODATA  = {mu0_CODATA:.14e}")
print(f"  mu0_geo     = {mu0_geo:.14e}")
print(f"  Δmu0        = {abs(mu0_CODATA - mu0_geo):.14e}")
print(f"  比值 geo/CODATA = {mu0_geo / mu0_CODATA:.14e}")
print()

print("=" * 70)
print("三、Gε0 耦合恒等式校验")
print("=" * 70)
print(f"  LHS  G * eps0_CODATA       = {LHS_Geps0:.14e}")
print(f"  RHS  e^2/(alpha^3 * mP^2)  = {RHS_Geps0:.14e}")
print(f"  Δ(Gε0)                      = {abs(LHS_Geps0 - RHS_Geps0):.14e}")
print(f"  比值 RHS/LHS                = {RHS_Geps0 / LHS_Geps0:.14e}")
print()

print("=" * 70)
print("四、引力耦合系数两种等价形式")
print("=" * 70)
print(f"  K_G_original = -G*(hbar/c)^2 = {K_G_original:.14e}")
print(f"  K_G_geo      = -hbar^3/(c*mP^2) = {K_G_geo:.14e}")
print(f"  ΔK_G         = {abs(K_G_original - K_G_geo):.14e}")
print()

print("=" * 70)
print("五、光速自校验 c = 1/sqrt(mu0_geo * eps0_geo)")
print("=" * 70)
c_recover = 1 / mp.sqrt(mu0_geo * eps0_geo)
print(f"  c_recover = {c_recover:.12e}")
print(f"  c_input   = {c:.12e}")
print(f"  Δc        = {abs(c_recover - c):.15e}")
print()

# ===== 诊断：4π/α² 因子 =====
print("=" * 70)
print("六、偏差因子诊断")
print("=" * 70)
factor = 4 * mp.pi / alpha**2
print(f"  4π / α²          = {factor:.14e}")
print(f"  eps0_geo/eps0_CODATA = {eps0_geo / eps0_CODATA:.14e}")
print(f"  mu0_CODATA/mu0_geo   = {mu0_CODATA / mu0_geo:.14e}")
print(f"  RHS_Geps0/LHS_Geps0  = {RHS_Geps0 / LHS_Geps0:.14e}")
print()

# ===== 修正公式校验 =====
print("=" * 70)
print("七、修正公式校验 (SI标准: alpha = e^2/(4π eps0 hbar c))")
print("=" * 70)
eps0_correct = e**2 / (4 * mp.pi * alpha * hbar * c)
mu0_correct  = (4 * mp.pi * alpha * hbar) / (c * e**2)
print(f"  eps0_correct = {eps0_correct:.14e}")
print(f"  eps0_CODATA  = {eps0_CODATA:.14e}")
print(f"  Δeps0_correct= {abs(eps0_correct - eps0_CODATA):.14e}")
print(f"  mu0_correct  = {mu0_correct:.14e}")
print(f"  mu0_CODATA   = {mu0_CODATA:.14e}")
print(f"  Δmu0_correct = {abs(mu0_correct - mu0_CODATA):.14e}")
print()

# 修正后的 Gε0 恒等式
Geps0_correct_RHS = e**2 / (4 * mp.pi * alpha * mP**2)
print(f"  修正后 RHS e²/(4πα mP²) = {Geps0_correct_RHS:.14e}")
print(f"  LHS  G * eps0_CODATA     = {LHS_Geps0:.14e}")
print(f"  Δ(修正后)                 = {abs(Geps0_correct_RHS - LHS_Geps0):.14e}")
print()

# ===== 标准关系验证 =====
print("=" * 70)
print("八、标准精细结构关系验证")
print("=" * 70)
alpha_from_eps0 = e**2 / (4 * mp.pi * eps0_CODATA * hbar * c)
print(f"  α (由ε0反算) = {alpha_from_eps0:.14e}")
print(f"  α (输入)     = {alpha:.14e}")
print(f"  Δα            = {abs(alpha_from_eps0 - alpha):.14e}")
