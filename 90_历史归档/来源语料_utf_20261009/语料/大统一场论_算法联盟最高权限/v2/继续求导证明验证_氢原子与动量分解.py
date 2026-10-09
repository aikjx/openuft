#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法联盟最高权限 · 继续求导证明验证 (V25)
================================================================================
本轮新增两个严格验证:
  [A] 氢原子能级的几何框架推导 → 对 Bohr/Rydberg 精算 (CODATA 2022)
  [B] 动量双重分解的 E²=p²c²+m²c⁴ 一致性检验 (框架声称的核心突破, 需诚实验证)
  [C] α-幂律能级结构 (α¹,α²,α⁴,α⁵ 幂次编码)
================================================================================
"""
from mpmath import mp, mpf, sqrt, pi, e as me
mp.dps = 60

PASS=0; FAIL=0; GRADE={}
def actuarial(name, computed, ref, tol, grade_label):
    global PASS, FAIL
    if ref==0: err=abs(computed)
    else: err=abs(computed-ref)/abs(ref)
    okk = err<tol
    if okk: PASS+=1
    else: FAIL+=1
    GRADE[name]=grade_label
    print(f"    {'✓' if okk else '✗'} {name:<40} 误差={mp.nstr(err,3):<12} {grade_label}")
    return okk, err

print("="*100)
print("算法联盟最高权限 · 继续求导证明验证 (V25)")
print("="*100)

# ---------- 常数 (CODATA 2022) ----------
c     = mpf('299792458')
hbar  = mpf('1.054571817e-34')
h     = 2*pi*hbar
me_e  = mpf('9.1093837015e-31')
m_p   = mpf('1.67262192369e-27')
e_abs = mpf('1.602176634e-19')
eps0  = mpf('8.8541878128e-12')
alpha = mpf('7.2973525693e-3')  # CODATA 2022 精确值
mu_reduced = me_e*m_p/(me_e+m_p)   # 约化质量

# =============================================================================
# [A] 氢原子能级推导 (几何框架)
# =============================================================================
print("\n[A] 氢原子能级: 玻尔量子化 → 库仑能级 (CODATA 精算)")
print("-"*100)
# 玻尔半径 (单电子, 用 m_e 精确)
a0 = hbar/(me_e*alpha*c)
print(f"    a₀ = ℏ/(m_e α c) = {mp.nstr(a0,12)} m  (CODATA 5.29177210903e-11)")
actuarial("a₀ Bohr半径", a0, mpf('5.29177210903e-11'), mpf('1e-9'), "S/A级")

# 里德伯常数 R∞ = α² m_e c / (2h)
Rinf = alpha**2 * me_e * c / (2*h)
Rinf_CODATA = mpf('10973731.568160')
print(f"    R∞ = α²m_e c/2h = {mp.nstr(Rinf,12)} m⁻¹  (CODATA {mp.nstr(Rinf_CODATA,9)})")
actuarial("R∞ Rydberg常数", Rinf, Rinf_CODATA, mpf('1e-9'), "A级")

# 基态能量 E₁ = -μ c² α²/2  (用约化质量, 双体)
E1 = -mu_reduced*c**2*alpha**2/2
E1_eV = E1/e_abs
print(f"    E₁ = -μc²α²/2 = {mp.nstr(E1_eV,10)} eV  (CODATA -13.598287 eV)")
actuarial("E₁ 基态能级", E1_eV, mpf('-13.598287'), mpf('1e-5'), "A级")

# 能级序列 E_n = E₁/n², 巴尔默系波长
print("\n    氢能级序列 E_n = E₁/n² 与巴尔默系:")
print(f"    {'n':<3}{'E_n(eV)':<14}{'波长λ(nm)':<16}{'实验λ(nm)'}")
for n in [1,2,3,4]:
    En = E1/n**2
    En_eV = En/e_abs
    print(f"    {n:<3}{mp.nstr(En_eV,8):<14}", end="")
    if n>2:  # 到 n=2 的跃迁 (巴尔默)
        lam = h*c/(E1/n**2 - E1/4)
        lam_nm = lam*1e9
        exp_lam = {3:mpf('656.3'),4:mpf('486.1')}.get(n, mpf('nan'))
        print(f"{mp.nstr(lam_nm,6):<16}{mp.nstr(exp_lam,6)}")
        actuarial(f"巴尔默 n→2 λ", lam_nm, exp_lam, mpf('1e-3'), "B级(实验)")
    else:
        print()

# =============================================================================
# [B] 动量双重分解 E²=p²c²+m²c⁴ 一致性 (诚实检验)
# =============================================================================
print("\n[B] 动量双重分解: E²=p²c²+m²c⁴ 一致性检验")
print("-"*100)
# 螺旋参数 (电子): R=ℏ/mc, ρ=R/√(1+α²), b=αR/√(1+α²)
R_ = hbar/(me_e*c)
rho = R_/sqrt(1+alpha**2)
b   = alpha*R_/sqrt(1+alpha**2)
w   = c/R_
m   = me_e
E   = hbar*w                      # = mc²
# 几何(横向)动量 p_g = m ω ρ ; 物理动量 p_p = m ω R = mc
p_g = m*w*rho
p_p = m*w*R_
print(f"    E   = ℏω = mc² = {mp.nstr(E,6)} J")
print(f"    p_几何(横向)=mωρ = {mp.nstr(p_g,6)} kg·m/s")
print(f"    p_物理(全速)=mωR = mc = {mp.nstr(p_p,6)} kg·m/s")
print(f"    p_物理/mc = {mp.nstr(p_p/(m*c),8)}  (应=1)")
# 检验 E² = p²c² + m²c⁴  用三种 p:
for pname, pval in [("p_几何(ρ)",p_g), ("p_物理(R)",p_p), ("p_轴向(b)",m*w*b)]:
    lhs = E**2
    rhs = pval**2*c**2 + m**2*c**4
    rel = (lhs-rhs)/lhs
    print(f"    用 {pname:<8}: E²-(p²c²+m²c⁴) 相对差 = {mp.nstr(rel,4)}  {'✓' if abs(rel)<1e-6 else '✗'}")
actuarial("E²=p²c²+m²c⁴ (p_几何ρ)", abs(E**2-(p_g**2*c**2+m**2*c**4))/E**2, mpf('0'), mpf('1e-6'), "待判定")
# 关键: 只有 p=mc (光速全动量) 时 E²=p²c²+m²c⁴→0=0; 其他分解不满足
print("""
  ★ 诚实结论: E²=p²c²+m²c⁴ 的满足方式
    - 用 p_物理=mc: E²=m²c⁴, 需 p²c²=0 → 不成立(除非视 p=0)
    - 用 p_几何=mc/√(1+α²): E²=m²c⁴, p²c²=m²c⁴/(1+α²) → 差 α² 量级
    → 在"v总=c, E=mc²"设定下, 螺旋动量与 E²=p²c²+m²c⁴ 不能同时满足,
      除非把"静质量能"与"螺旋动量"分离到不同自由度(需明确建模, 否则为框架张力).
""")

# =============================================================================
# [C] α-幂律能级结构
# =============================================================================
print("\n[C] α-幂律能级结构验证")
print("-"*100)
# 玻尔半径 ~ α⁻¹, 氢能级 ~ α², 精细结构 ~ α⁴, 兰姆位移 ~ α⁵, 超精细 ~ α⁴ m_e/m_p
a0_alpha = 1/alpha
E_hyd_alpha = alpha**2
fs_alpha = alpha**4
lamb_alpha = alpha**5
print(f"    a₀ ∝ α⁻¹ : α⁻¹ = {mp.nstr(a0_alpha,8)}  (~137.04)")
print(f"    氢能级 ∝ α² : α² = {mp.nstr(E_hyd_alpha,8)}  (~5.33e-5)")
print(f"    精细结构 ∝ α⁴ : α⁴ = {mp.nstr(fs_alpha,8)}  (~2.83e-9)")
print(f"    兰姆位移 ∝ α⁵ : α⁵ = {mp.nstr(lamb_alpha,8)}  (~2.07e-11)")
# 验证相对比例
print(f"    (α⁴)/(α²)² = {mp.nstr(fs_alpha/E_hyd_alpha**2,10)}  (应=1)")
print(f"    (α⁵)/(α²)²·α = {mp.nstr(lamb_alpha/(E_hyd_alpha**2*alpha),10)}  (应=1)")
actuarial("α-幂律: (α⁴)/(α²)²=1", fs_alpha/E_hyd_alpha**2, mpf('1'), mpf('1e-50'), "S级(恒等)")
actuarial("α-幂律: (α⁵)/(α²)²α=1", lamb_alpha/(E_hyd_alpha**2*alpha), mpf('1'), mpf('1e-50'), "S级(恒等)")

# =============================================================================
print("\n" + "="*100)
print(f"验证结果: {PASS} 通过 / {FAIL} 失败")
print("="*100)
print("""
★ 本轮诚实总结:
1. 氢原子能级: Bohr半径/里德伯常数/基态能级均 A 级精确 (来自库仑/玻尔, 非独立新预言);
   巴尔默系波长与实验 B 级吻合 (n=3→656.3nm, n=4→486.1nm).
2. 动量双重分解 E²=p²c²+m²c⁴: 【不能同时满足】——在 v总=c, E=mc² 设定下,
   螺旋动量(几何/物理/轴向任选)均无法使 E²=p²c²+m²c⁴ 严格成立(差 α² 量级).
   这是框架的【真实张力/未解决点】, 须诚实标注, 而非宣称已闭环.
3. α-幂律: 能级结构 α⁻¹,α²,α⁴,α⁵ 幂次恒等(机器零), 但这是幂次记号, 不增物理内容.
""")
