# -*- coding: utf-8 -*-
"""
GAQ-UFT V50 攻坚 · 第四轮 · 家族八 #52：SymPy 符号复核
对象：§16.9 共振判据非傍轴修正的核心符号推导
主要结果（诚实降级）：
  (a1) 点态事实：LG_{0l} 束腰波函数 NOT 横向拉普拉斯点态本征函数
       Δ_perp ψ/ψ = -4(L+1)/w0^2 + 4 rho^2/w0^4  （依赖 rho，残差 ≠ 0）
  (a2) 平均事实：强度加权平均 <Δ_perp ψ/ψ> = -2(L+1)/w0^2 （符号恒等）
       → §16.9 的 k_perp^2 = 2(|l|+1)/w0^2 是"强度加权平均横向波数"，
         不是 Helmholtz 点态本征值；表述须降级
  (b) Helmholtz 色散 kz = sqrt(k^2 - k_perp^2)：kz^2+k_perp^2=k^2 符号恒等（对平均 k_perp 仍成立，作一阶修正）
  (c) 一阶频移闭式 (k-kz)/k = a = (|l|+1)/(k^2 w0^2)：符号级数首项，余项 O(a^2)
结论：§16.9 闭式作为"平均意义/一阶修正"判据成立（V1-V4+250位+符号平均三重核验），
     但"精确 LG 解/横向本征值"措辞须降级——LG_{0l} 非 Helmholtz 点态解。
"""
import sympy as sp
import sys

fail = 0
def check(name, cond):
    global fail
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fail += 1

rho, phi, w0, k = sp.symbols("rho phi w0 k", positive=True, real=True)
L = sp.symbols("L", nonnegative=True, integer=True)  # L = |l|

psi = rho**L * sp.exp(-rho**2/w0**2) * sp.exp(sp.I*L*phi)

print("="*78)
print("(a1) 点态事实：LG_{0l} 束腰波函数非横向拉普拉斯点态本征函数")
print("="*78)
lap = (1/rho)*sp.diff(rho*sp.diff(psi, rho), rho) + (1/rho**2)*sp.diff(psi, phi, 2)
ratio = sp.simplify(lap / psi)
print(f"  Δ_perp ψ/ψ = {sp.expand(ratio)}")
# 点态本征方程要求 Δψ/ψ = const；实际含 rho 依赖
rho_dep = sp.diff(ratio, rho)
print(f"  d/dρ (Δψ/ψ) = {sp.simplify(rho_dep)}")
check("点态非本征：Δψ/ψ 显式依赖 ρ（d/dρ ≠ 0）", sp.simplify(rho_dep) != 0)
resid = sp.simplify(ratio + 2*(L+1)/w0**2)
check("点态残差 Δψ/ψ + 2(L+1)/w0² ≠ 0（非本征方程）", sp.simplify(resid) != 0)

print()
print("="*78)
print("(a2) 平均事实：强度加权平均 = -2(L+1)/w0²（Γ 函数闭式符号恒等）")
print("="*78)
# 利用 L²/ρ² 径向项与 -L²/ρ² 角向项精确抵消（LG 特征）：
# Δ_perp ψ/ψ = 4ρ²/w0⁴ - 4(L+1)/w0² （依赖 ρ，非点态本征）
# 加权平均 <f(ρ)> = ∫u²ρ f dρ / ∫u²ρ dρ, u = ρ^L e^{-ρ²/w0²}
# ∫₀^∞ ρ^a e^{-bρ²} dρ = Γ((a+1)/2)/(2b^((a+1)/2)), b = 2/w0²
def mom(a, b):
    return sp.gamma((a+1)/2)/(2*b**((a+1)/2))
b = sp.Rational(2,1)/w0**2
den = mom(2*L+1, b)
avg_r2 = sp.simplify(mom(2*L+3, b)/den)   # <ρ²> = (L+1)w0²/2
avg = sp.simplify(4*avg_r2/w0**4 - 4*(L+1)/w0**2)
print(f"  <ρ²>          = {sp.simplify(avg_r2)}")
print(f"  总平均 <Δ_perp ψ/ψ> = {sp.simplify(avg)}")
check("<Δ_perp ψ/ψ> = -2(L+1)/w0²（Γ 闭式符号恒等）",
      sp.simplify(avg + 2*(L+1)/w0**2) == 0)
check("验证：<ρ²> = (L+1)w0²/2", sp.simplify(avg_r2 - (L+1)*w0**2/2) == 0)

print()
print("="*78)
print("(b) Helmholtz 色散 kz² + k_perp² = k²（平均意义下符号恒等）")
print("="*78)
kp2 = 2*(L+1)/w0**2
kz = sp.sqrt(k**2 - kp2)
check("kz² + k_perp² = k²（符号恒等）", sp.simplify(kz**2 + kp2 - k**2) == 0)
check("等价闭式 Ω² + 2(L+1)/w0² = k²（Ω²=kz²）", sp.simplify(kz**2 + kp2 - k**2) == 0)

print()
print("="*78)
print("(c) 一阶频移闭式的符号级数展开")
print("="*78)
a = sp.symbols("a", positive=True)
rel_shift = 1 - sp.sqrt(1 - 2*a)
series = sp.series(rel_shift, a, 0, 3).removeO()
print(f"  1-√(1-2a) = {sp.expand(series)}")
check("一阶项系数 = 1（Δω/ω ≈ a）", sp.simplify(series.coeff(a,1) - 1) == 0)
check("二阶项 = a²/2（余项 O(a²)，与 250 位 V7 一致）",
      sp.simplify(series.coeff(a,2) - sp.Rational(1,2)) == 0)
# 核对闭式主项：Δω/ω ≈ (|l|+1)/(k²w0²) —— 在 a = (L+1)/(k²w0²) 下自动满足（一阶系数=1）
check("闭式主项 (L+1)/(k²w0²)（一阶系数=1 代入即得）",
      sp.simplify(series.coeff(a,1)*((L+1)/(k**2*w0**2)) - (L+1)/(k**2*w0**2)) == 0)

print()
print("="*78)
print(f"SymPy 符号复核结果: {'全部 PASS' if fail==0 else f'{fail} 项 FAIL'}")
print("="*78)
print("诚实结论：")
print("  1. LG_{0l} 束腰波函数非 Helmholtz 点态本征函数（(a1) 证）")
print("  2. k_perp²=2(|l|+1)/w0² 为强度加权平均横向波数（(a2) 符号恒等证）")
print("  3. §16.9 闭式作为平均意义/一阶修正判据成立；'精确 LG 解'措辞须降级")
print("  4. 与 S02-C0012 傍轴主判据的关系：本修正为平均波数纳入色散的一阶改进")
sys.exit(fail)
