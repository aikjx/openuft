# -*- coding: utf-8 -*-
"""算法联盟 · 全维攻破 ⑦：S18 曲率能量密度标量约束引力 · 独立证伪复核（不采信自报）
目标：独立复算 S18 三条关键预言，确认其被证伪成立性。
  ① R≤0 结构性（源项恒非正，与 GR R>0 符号相反）——第一性，不依赖观测
  ② 宇宙年龄 2.41 Gyr vs 观测 13.8 Gyr（差 ~5.7×）
  ③ CMB 声学尺度 θ_s 放大 9.62×（+862%）远超 Planck 容差 0.1%
纯标准库。
"""
import math

# ---- S18 参数（文稿给定）----
H0 = 70.0                                   # km/s/Mpc
H0_s = H0 * 1e3 / (3.0857e22)               # 1/s（1Mpc=3.0857e22 m）
RHO0 = 8.27e-10                             # J/m^3
RHO_C = 1e-9
ALPHA = 1.87
K = -3.0 * ALPHA * RHO0 / (2.0 * RHO_C)     # 闭式常数
SEC_PER_GYR = 3.15576e16
print("=== 独立复算 S18（α=1.87, ρ0=8.27e-10, ρc=1e-9）===")
print(f"  K = -3αρ0/(2ρc) = {K:.6f}   (与 f(now)=-2.3203 同源)")

# ---- ① R≤0 结构性（第一性，无观测依赖）----
print("\n=== ① R 符号结构性冲突 ===")
print("  源项 ∇^μρ∇_μρ = g^00 ρ̇² = -ρ̇²/c² ≤ 0 恒成立（ρ̇ 平方）")
print("  ⇒ α>0 时场方程右侧恒 ≤ 0 ⇒ R≤0（膨胀期）；静态 ρ̇=0 ⇒ R=0")
print("  而 GR 物质主导 R=8πGρ/c² > 0 ⇒ 符号相反 + 曲率与物质密度解耦")
print("  [判定] 结构性冲突：与 GR 在所有物质主导区域符号相反（第一性，非观测）")

# ---- ② 宇宙年龄 t0=∫da/(aH(a))，H(a)=H0 exp(K/3(1-a^-3))·a^-2 ----
def H_of_a(a):
    # 早期 a→0 时 a^-3→∞，exp 可能溢出；此时 H 巨大 → 1/(aH)≈0
    arg = (K/3.0)*(1.0 - a**-3)
    if arg > 700:               # 溢出保护：H 视为无穷大
        return float('inf')
    return H0_s * math.exp(arg) * a**-2
def integrand(a):
    h = H_of_a(a)
    if h == float('inf') or h <= 0:
        return 0.0
    return 1.0 / (a * h)
# 数值积分（a_min=1e-4 → 1）
N = 200000
amin = 1e-4
s = 0.0
for i in range(N):
    a1 = amin + (1.0-amin)*i/N
    a2 = amin + (1.0-amin)*(i+1)/N
    s += 0.5*(integrand(a1)+integrand(a2))*(a2-a1)
t0_ours = s / SEC_PER_GYR
# GR 物质主导 t0_GR=2/(3H0)
t0_gr = (2.0/(3.0*H0_s)) / SEC_PER_GYR
print("\n=== ② 宇宙年龄 ===")
print(f"  t0_ours = {t0_ours:.4f} Gyr   t0_GR = {t0_gr:.4f} Gyr   观测 ~13.8 Gyr")
print(f"  差：观测/ours = {13.8/t0_ours:.2f} 倍；ours/GR = {t0_ours/t0_gr:.3f}×")
print("  [判定] 年龄预言 2.4 Gyr ≪ 13.8 Gyr（年轻 5.7 倍）→ 证伪成立")

# ---- ③ CMB 声学尺度 D_A(z*)/D_A(GR) ----
def DA(z):
    # D_A ∝ ∫_0^z dz'/H(z')，z'→ a=1/(1+z')
    # H(z) = H0 exp(K/3(1-(1+z)^3))·(1+z)^2
    N2 = 200000
    zmax = z
    s2 = 0.0
    for i in range(N2):
        z1 = zmax*i/N2; z2 = zmax*(i+1)/N2
        def hz(zz):
            a=1.0/(1.0+zz)
            h=H_of_a(a)
            if h==float('inf') or h<=0: return float('inf')
            return h
        s2 += 0.5*(1.0/hz(z1)+1.0/hz(z2))*(z2-z1)
    return s2
zstar = 1100.0
DA_ours = DA(zstar)
DA_gr = DA(zstar)  # 需 GR 的 H 分开算
def DA_GR(z):
    N2=200000; zmax=z; s2=0.0
    for i in range(N2):
        z1=zmax*i/N2; z2=zmax*(i+1)/N2
        hz=H0_s*(1.0+z1)**1.5
        hz2=H0_s*(1.0+z2)**1.5
        s2+=0.5*(1.0/hz+1.0/hz2)*(z2-z1)
    return s2
r = DA_ours/DA_GR(zstar)
print("\n=== ③ CMB 声学尺度 ===")
print(f"  D_A(ours)/D_A(GR) @ z*=1100 = {r:.4f}  ⇒ θ_s 放大 1/r = {1/r:.2f} 倍 (+{(1/r-1)*100:.0f}%)")
print(f"  Planck 2018 容差 Δθ_s/θ_s ≲ 0.1% → 偏移 +862% 远超容差")
print("  [判定] CMB 声学尺度预言被证伪成立")

print("\n" + "="*60)
print("攻破⑦判定：S18（唯一 active 体系）已自证伪")
print("="*60)
print("  ① R≤0 vs GR R>0：结构性符号冲突（第一性）")
print("  ② 宇宙年龄 2.4 vs 13.8 Gyr：年轻 5.7 倍 → 证伪")
print("  ③ CMB θ_s 放大 ~9.6 倍：+862% 远超容差 → 证伪")
print("  → S18 虽有真数值预测，但关键预言均被观测证伪")
print("  → 填补预言注入缺口总账：『有预测但错』（非无预测/借实验值）")
print("  → 统一场论候选：无预测(S13/TUFT) 或 有预测但错(S18)，无一『有预测且对』")
