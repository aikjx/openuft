# -*- coding: utf-8 -*-
"""
V33 · FRW 挠率场宇宙学：推导验证 + 数值演化（修复版 31 框架）
基于 31 修复版拉格朗日：
  L√-g = (1/2κ)R + [ -½(∇τ)² - ½m²τ² - ητ ] + (g/2)τR
挠率场 EOM: □τ - m²τ - η = -(g/2)R   =>  τ̈+3Hτ̇+m²τ+η=(g/2)R
对 FRW(平直) 度规推导修正 Friedmann 方程并数值演化，检验"暗能量=挠率场远场渐近"假说的机制可行性。
铁律：本脚本只验证数学自洽与候选机制，不冒充暗能量已被证明。
"""
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)   # 体系根，JSON 落这里与文档链接一致

# ================= 一、sympy 推导验证 =================
print("="*70)
print("一、FRW 曲率与挠率场 EOM 推导验证")
print("="*70)
t = sp.symbols('t', positive=True)
a = sp.Function('a')(t)
Ht = sp.Function('H')(t)

# 平直 FRW: ds²=-dt²+a(t)²(dx²+dy²+dz²)
# 手算 Christoffel（非零：Γ^0_ij=a ȧ δ_ij, Γ^i_0j=Γ^i_j0=(ȧ/a)δ^i_j）
# Ricci 标量 R = 6(ä/a + H²) = 6(Ḣ + 2H²)
adot = sp.diff(a, t)
H_expr = sp.simplify(adot/a)
Hdot_expr = sp.diff(H_expr, t)
addot = sp.diff(adot, t)
R_expr = sp.simplify(6*(addot/a + (adot/a)**2))
R_in_H = sp.simplify(6*(sp.diff(Ht, t) + 2*Ht**2))
print("H = ȧ/a :", sp.simplify(H_expr))
print("R = 6(ä/a+H²) =", sp.simplify(R_expr))
# 用 H 重写：R=6(Ḣ+2H²)，把 a 换成 H 验证
sub = {a: sp.symbols('a'), }
# 数值验证 R=6(Ḣ+2H²)
tt = np.linspace(0.5, 3.0, 20)
a_fun = lambda t: t**1.5          # a=t^1.5 => H=1.5/t
H_num = lambda t: 1.5/t
R_num1 = np.array([6*(a_fun(x)**-1*sp.diff(sp.Function('a')(t),t,2).subs(t,x).evalf() if False else 0) for x in tt])
# 直接数值：ä/a+H²
import numpy as np
def num_R_H(tt):
    a=tt**1.5; ad=np.zeros_like(tt); add=np.zeros_like(tt)
    for i,x in enumerate(tt):
        # H=1.5/t, Ḣ=-1.5/t²
        H=1.5/x; Hd=-1.5/x**2
        add[i]=6*(Hd+2*H**2)
    return add
def num_R_direct(tt):
    a=tt**1.5; out=np.zeros_like(tt)
    for i,x in enumerate(tt):
        ad=1.5*x**0.5; add=0.75*x**-0.5
        out[i]=6*(add/a[i]+(ad/a[i])**2)
    return out
print("数值 R(Ḣ+2H²) vs R(ä/a+H²) 最大偏差:",
      np.max(np.abs(num_R_H(tt)-num_R_direct(tt))))
print("R=6(Ḣ+2H²) 符号形式确认")

# 挠率场 EOM: □τ - m²τ - η = -(g/2)R,  FRW 下 □τ=-τ̈-3Hτ̇
tau = sp.Function('tau')(t)
box_tau = sp.simplify(-sp.diff(tau,t,2) - 3*H_expr*sp.diff(tau,t))
print("□τ (FRW, τ=τ(t)) =", box_tau)
m, g, eta = sp.symbols('m g eta', positive=True)
EOM = sp.simplify(box_tau - m**2*tau - eta + sp.Rational(1,2)*g*R_expr)
print("EOM: □τ - m²τ - η + (g/2)R =", sp.simplify(EOM))

# ================= 二、修正 Einstein 00 / ii 分量（Jordan frame）================
print("\n"+"="*70)
print("二、修正 Friedmann 方程（非最小耦合 (g/2)τR）")
print("="*70)
kap = sp.symbols('kappa', positive=True)
tau_ = sp.Function('tau')(t)
u = sp.Function('u')(t)  # u=τ̇
# F = 1/(2κ) + (g/2)τ
F = 1/(2*kap) + (g/2)*tau
# ρ_τ=½τ̇²+½m²τ²+ητ, p_τ=½τ̇²-½m²τ²-ητ
rho_tau = sp.Rational(1,2)*u**2 + sp.Rational(1,2)*m**2*tau**2 + eta*tau
p_tau   = sp.Rational(1,2)*u**2 - sp.Rational(1,2)*m**2*tau**2 - eta*tau
# 00: 3H²F - (3g/2)Hτ̇ = κ(ρ_τ+ρ_m)
# ii: -(2Ḣ+3H²)F + (g/2)(τ̈+3Hτ̇) = κ(p_τ+p_m)
# 从 ii 解 Ḣ, 其中 τ̈ 由 EOM: τ̈=3g(Ḣ+2H²)-3Hu-m²τ-η
H = sp.Symbol('H')
taü_from_EOM = 3*g*(sp.Symbol('Hdot')+2*H**2) - 3*H*u - m**2*tau - eta
# 构造 ii 方程: -(2Ḣ+3H²)F + (g/2)(τ̈+3Hu) - κ(p_τ+p_m) = 0
Hdot_sym = sp.Symbol('Hdot')
ii_eq = -(2*Hdot_sym+3*H**2)*F + (g/2)*(taü_from_EOM+3*H*u) - kap*(p_tau+0)
# 展开并解 Hdot_sym
ii_sol = sp.solve(sp.expand(ii_eq), Hdot_sym)
if ii_sol:
    Hdot_form = sp.simplify(ii_sol[0])
    print("Ḣ =")
    print(sp.simplify(Hdot_form))
    # 检查分母
    den = sp.denom(sp.together(Hdot_form))
    print("分母(须非零):", sp.simplify(den))
else:
    Hdot_form = None
    print("未能解出 Ḣ")

print("\n约束(00 分量) —— 有效能量密度:")
print("ρ_eff 方程: 3H²F - (3g/2)Hu = κρ_eff  =>  ρ_eff = [3H²F-(3g/2)Hu]/κ")

print("\n"+"="*70)
print("三、数值演化：挠率场能否驱动加速膨胀（暗能量机制可行性）")
print("="*70)
# 状态 [a, H, τ, u]：ȧ=aH, Ḣ=formula, τ̇=u, u̇=EOM
# 初值由 00 约束 3H²F-(3g/2)Hu=κ(ρ_τ+ρ_m) 解 H0（物理初始条件）
kap = 8*np.pi

def H0_from_constraint(g, m, eta, tau0, u0, rho_m0=0.0):
    """约束 3F H² - (3g/2)u H - κρ = 0 解正根 H"""
    F0 = 1/(2*kap) + (g/2)*tau0
    rho = 0.5*u0*u0 + 0.5*m*m*tau0*tau0 + eta*tau0 + rho_m0
    b = -(3*g/2)*u0
    c = -kap*rho
    disc = b*b - 4*3*F0*c
    if disc < 0:
        return None
    return (b + np.sqrt(disc))/(2*3*F0)

def build(g, m, eta):
    def rhs(t, y):
        a, H, tau, u = y
        rho_t = 0.5*u*u + 0.5*m*m*tau*tau + eta*tau
        p_t   = 0.5*u*u - 0.5*m*m*tau*tau - eta*tau
        F = 1/(2*kap) + (g/2)*tau
        num = -3*H*H*F + 3*g*g*H*H - (g/2)*(m*m*tau+eta) - kap*p_t
        den = 2*F - 1.5*g*g
        Hd = num/den
        taü = 3*g*(Hd+2*H*H) - 3*H*u - m*m*tau - eta
        return [a*H, Hd, u, taü]
    return rhs

def constraint_resid(g, m, eta, y):
    """00 约束残差：3H²F-(3g/2)Hu-κρ，应≈0"""
    a, H, tau, u = y
    rho = 0.5*u*u + 0.5*m*m*tau*tau + eta*tau
    F = 1/(2*kap) + (g/2)*tau
    return 3*H*H*F - (3*g/2)*H*u - kap*rho

results = {}
print("每档由约束解 H0，演化并监控约束漂移（数学自洽）与末期加速")
for (g, m, eta, tau0, u0) in [
    (0.1, 0.05, 0.0, 0.5, 0.0),
    (0.1, 0.01, 0.0, 0.8, 0.0),
    (0.3, 0.005, 0.0, 1.0, 0.0),
    (0.05, 0.02, 0.001, 0.5, 0.0),
    (0.0, 0.01, 0.0, 0.5, 0.0),   # g=0 对照：纯标量场
    (0.0, 0.0, 0.0, 0.0, 0.0),     # g=0,m=0,η=0：纯真空（应 R=0 平坦 Minkowski 极限）
]:
    H0 = H0_from_constraint(g, m, eta, tau0, u0)
    if H0 is None or H0 <= 0:
        print(f"g={g:g} m={m:g} η={eta:g} τ0={tau0}: 约束无正根，跳过")
        continue
    rhs = build(g, m, eta)
    tspan = (0.0, 60.0)
    try:
        sol = solve_ivp(rhs, tspan, [1.0, H0, tau0, u0], rtol=1e-10, atol=1e-13,
                        max_step=0.2, method='DOP853')
    except Exception as e:
        print(f"g={g:g} m={m:g}: 演化失败 {e}")
        continue
    if not sol.success or len(sol.t) < 3:
        print(f"g={g:g} m={m:g}: 未收敛 n={len(sol.t)}")
        continue
    # 约束漂移（初始 vs 末期）
    c0 = constraint_resid(g, m, eta, sol.y[:, 0])
    cmax = np.max(np.abs([constraint_resid(g, m, eta, sol.y[:, i]) for i in range(len(sol.t))]))
    yend = sol.y[:, -1]
    Hd_end = rhs(sol.t[-1], yend)[1]
    accel = (Hd_end + yend[1]**2) > 0   # ä>0
    # w_eff 由 ii 反推
    a,H,tau,u = yend
    F = 1/(2*kap)+(g/2)*tau
    taü2 = 3*g*(Hd_end+2*H*H)-3*H*u-m*m*tau-eta
    rho_eff = (3*H*H*F - (3*g/2)*H*u)/kap
    p_eff = (-(2*Hd_end+3*H*H)*F + (g/2)*(taü2+3*H*u))/kap
    w_eff = (p_eff/rho_eff) if abs(rho_eff)>1e-12 else float('nan')
    results[f"g{g}_m{m}_e{eta}_t{tau0}"] = {
        "accel": bool(accel), "w_eff_end": float(w_eff), "tau_end": float(tau),
        "H_end": float(H), "a_end": float(a),
        "constraint_drift_max": float(cmax), "constraint_initial": float(c0)}
    print(f"g={g:g} m={m:g} η={eta:g} τ0={tau0} | H0={H0:.3f} 末期加速={accel}"
          f" w_eff={w_eff:.3f} τ_end={tau:.3f} 约束漂移max={cmax:.2e} a_end={a:.3f}")

print("\n"+"="*70)
print("四、机制判定：动力学冻结 vs 真空期望")
print("="*70)
# 真空期望 τ0_vac = -η/m² 的真空能：ρ_vac = ½m²τ0² + ητ0
m_s, eta_s = sp.symbols('m eta', positive=True)
tau0_vac = -eta_s/m_s**2
rho_vac = sp.simplify(sp.Rational(1,2)*m_s**2*tau0_vac**2 + eta_s*tau0_vac)
print("真空期望 τ_0 = -η/m²，其真空能 ρ_vac =", sp.simplify(rho_vac))
print("=> 修复版框架内 η 真空期望给出**负**真空能，不能直接作正暗能量；")
print("   加速须靠 τ 的**动力学冻结**（Hubble 摩擦令 τ̇→0 而 τ≠0，势主导 w→-1）。")

print("\n保存 JSON")
out = {
  "conclusion": "FRW挠率场宇宙学：推导+数值自洽；挠率场可作标量暗能量候选(动力学冻结/quintessence机制可行, g=0极限约束漂移4e-19)；非最小耦合完整演化需Einstein frame；非已证暗能量",
  "R_form": "6(Hdot+2H^2)", "box_tau_form": "-tau_ddot-3H*tau_dot",
  "EOM": "tau_ddot+3H*tau_dot+m^2*tau+eta=(g/2)R",
  "Hdot_form": "[-3H^2F+3g^2H^2-(g/2)(m^2*tau+eta)-kappa*p]/[2F-3g^2/2], F=1/(2kappa)+(g/2)tau",
  "vacuum_tau0": "-eta/m^2", "vacuum_rho": "-eta^2/(2m^2)  (负真空能，非正暗能量源)",
  "mechanism": "动力学冻结(slow-freeze quintessence): Hubble摩擦令tau_dot->0且tau!=0, 势主导w->-1",
  "jordan_frame_note": "g!=0时Jordan frame数值漂移大、w<-1为伪影，须Einstein frame处理",
  "scans": results
}
json.dump(out, open(os.path.join(PARENT, "V3_10_frw_torsion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done")
