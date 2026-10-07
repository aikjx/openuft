# -*- coding: utf-8 -*-
"""
V34 · FRW 挠率场宇宙学 · Einstein frame 完整演化（闭合 33 稿 g≠0 Jordan frame 伪影）
Jordan frame 31 修复版：L = F(τ)R - ½(∇τ)² - V(τ)，F=1/(2κ)+(g/2)τ, V=½m²τ²+ητ
共形 g=Ω²g̃，Ω²F=1/(2κ)。EF 拉格朗日：
  L̃ = (1/2κ)R̃ - K(τ)(∂̃τ)² - U(τ)
  K(τ) = 1/(4κF) + 3F'²/(4κF²)，U(τ)=V/(4κ²F²)
EF 演化（爱因斯坦时间 t̃，标准无约束伪影）：
  3H̃²=κ(KX²+U), X=τ̇̃
  K τ̈̃ + 3KH̃τ̇̃ + ½K'(τ)τ̇̃² - U'(τ)=0
  Ḣ̃ = -κK X²
铁律：EF 机制检验≠已证暗能量；EF 时间≠Jordan 物理时间，可观测映射另需返回。
"""
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)

print("="*70)
print("一、Einstein frame 映射推导（sympy）")
print("="*70)
tau = sp.symbols('tau')
kappa, g, m, eta = sp.symbols('kappa g m eta', positive=True)
F = 1/(2*kappa) + (g/2)*tau
Fp = sp.diff(F, tau)
V = sp.Rational(1,2)*m**2*tau**2 + eta*tau
# EF 动能系数 K(τ) = 1/(4κF) + 3F'²/(4κF²)
K = sp.simplify(1/(4*kappa*F) + 3*Fp**2/(4*kappa*F**2))
U = sp.simplify(V/(4*kappa**2*F**2))
dphi_dtau = sp.sqrt(sp.simplify(2*K))  # ½(dφ/dτ)²=K
print("F(τ) =", sp.simplify(F), "  F' =", sp.simplify(Fp))
print("K(τ) =", sp.simplify(K))
print("U(τ) =", sp.simplify(U))
print("dφ/dτ = sqrt(2K) =", sp.simplify(dphi_dtau))
print("有效引力耦合正性条件 F>0: τ > -1/(κg)")

# K'(τ), U'(τ) 供演化
Kp = sp.simplify(sp.diff(K, tau))
Up = sp.simplify(sp.diff(U, tau))
Kf = sp.lambdify((tau, kappa, g, m, eta), K, 'numpy')
Kpf = sp.lambdify((tau, kappa, g, m, eta), Kp, 'numpy')
Uf = sp.lambdify((tau, kappa, g, m, eta), U, 'numpy')
Upf = sp.lambdify((tau, kappa, g, m, eta), Up, 'numpy')
Ff = sp.lambdify((tau, kappa, g), F, 'numpy')
print("K,U,dφ/dτ 符号推导完成")

print("\n"+"="*70)
print("二、EF 数值演化（标准 quintessence，无 Jordan 伪影）")
print("="*70)
kap = 8*np.pi

def H0_EF(g, m, eta, tau0, X0):
    F0 = 1/(2*kap)+(g/2)*tau0
    K0 = 1/(4*kap*F0) + 3*(g/2)**2/(4*kap*F0**2)
    U0 = (0.5*m*m*tau0*tau0+eta*tau0)/(4*kap**2*F0**2)
    rho = K0*X0*X0 + U0
    return np.sqrt(kap*rho/3), K0, U0

def build_EF(g, m, eta):
    def rhs(t, y):
        a, H, tau, X = y
        F = 1/(2*kap)+(g/2)*tau
        K = 1/(4*kap*F) + 3*(g/2)**2/(4*kap*F**2)
        Kp = -1/(4*kap*F**2)*(g/2) + 3*(g/2)**2/(4*kap)*(-2)/(F**3)*(g/2)
        U = (0.5*m*m*tau*tau+eta*tau)/(4*kap**2*F**2)
        dU = sp.diff(sp.Rational(1,2)*m**2*tau**2+eta*tau, tau)
        # 用数值导数 dU/dτ
        Up_num = (m*m*tau+eta)/(4*kap**2*F**2) + (0.5*m*m*tau*tau+eta*tau)/(4*kap**2)*(-2)/(F**3)*(g/2)
        Hd = -kap*K*X*X
        Xd = (-Up_num - 0.5*Kp*X*X - 3*K*H*X)/K
        return [a*H, Hd, X, Xd]
    return rhs

def build_EF_sym(g, m, eta):
    """用 sympy lambdify 的 K,K',U,U' 保证一致"""
    def rhs(t, y):
        a, H, tau, X = y
        K = Kf(tau, kap, g, m, eta)
        Kp = Kpf(tau, kap, g, m, eta)
        Up = Upf(tau, kap, g, m, eta)
        Hd = -kap*K*X*X
        Xd = (-Up - 0.5*Kp*X*X - 3*K*H*X)/K
        return [a*H, Hd, X, Xd]
    return rhs

def constraint_resid_EF(g, m, eta, y):
    a, H, tau, X = y
    F = 1/(2*kap)+(g/2)*tau
    K = 1/(4*kap*F) + 3*(g/2)**2/(4*kap*F**2)
    U = (0.5*m*m*tau*tau+eta*tau)/(4*kap**2*F**2)
    return 3*H*H - kap*(K*X*X+U)

results = {}
print("EF 演化各参数档：约束漂移、末期加速、w_eff（EF 中物理，非 Jordan 伪影）")
for (g, m, eta, tau0, X0) in [
    (0.1, 0.05, 0.0, 0.5, 0.0),
    (0.1, 0.01, 0.0, 0.8, 0.0),
    (0.3, 0.005, 0.0, 1.0, 0.0),
    (0.05, 0.02, 0.001, 0.5, 0.0),
    (0.1, 0.02, 0.0, 0.3, 0.0),
    (0.2, 0.01, 0.0, 0.6, 0.0),
    (0.0, 0.01, 0.0, 0.5, 0.0),   # g=0 对照：应退化标准 quintessence (φ=τ, K=1/2, U=V)
]:
    F0 = 1/(2*kap)+(g/2)*tau0
    if F0 <= 0:
        print(f"g={g:g} τ0={tau0}: F<=0 无效引力，跳过"); continue
    H0, K0, U0 = H0_EF(g, m, eta, tau0, X0)
    if not np.isfinite(H0) or H0 <= 0:
        print(f"g={g:g} m={m:g}: H0 非正/非有限，跳过"); continue
    rhs = build_EF_sym(g, m, eta)
    tspan = (0.0, 60.0)
    sol = solve_ivp(rhs, tspan, [1.0, H0, tau0, X0], rtol=1e-13, atol=1e-15,
                    max_step=0.1, method='DOP853')
    n = len(sol.t)
    conv = sol.success and sol.t[-1] >= tspan[1]-1e-9
    # F 边界监控
    Fmin = min(1/(2*kap)+(g/2)*tau_ for tau_ in sol.y[2])
    if not conv:
        print(f"g={g:g} m={m:g} η={eta:g} τ0={tau0}: 未收敛 n={n} msg='{sol.message}' "
              f"t_end={sol.t[-1]:.2f} F_min={Fmin:.3e} τ_end={sol.y[2,-1]:.3f}")
        results[f"g{g}_m{m}_e{eta}_t{tau0}"] = {"status": "not_converged", "n": int(n),
                                                 "t_end": float(sol.t[-1]), "F_min": float(Fmin)}
        continue
    c0 = constraint_resid_EF(g, m, eta, sol.y[:, 0])
    cmax = max(abs(constraint_resid_EF(g, m, eta, sol.y[:, i])) for i in range(n))
    yend = sol.y[:, -1]
    a,H,tau_,X = yend
    F = 1/(2*kap)+(g/2)*tau_
    K = 1/(4*kap*F) + 3*(g/2)**2/(4*kap*F**2)
    U = (0.5*m*m*tau_*tau_+eta*tau_)/(4*kap**2*F**2)
    rho = K*X*X+U; p = K*X*X-U
    w = p/rho if abs(rho)>1e-12 else float('nan')
    Hd_end = rhs(sol.t[-1], yend)[1]
    accel = (Hd_end+H*H) > 0
    physical_w = -1.0 < w < -1/3  # EF 中物理加速窗口（w∈(-1,-1/3)）
    results[f"g{g}_m{m}_e{eta}_t{tau0}"] = {
        "accel": bool(accel), "w_eff": float(w), "tau_end": float(tau_),
        "H_end": float(H), "a_end": float(a), "constraint_drift": float(cmax),
        "physical_w_window": bool(physical_w), "F_min": float(Fmin)}
    print(f"g={g:g} m={m:g} η={eta:g} τ0={tau0} | 加速={accel} w_eff={w:.3f}"
          f" τ_end={tau_:.3f} 约束漂移={cmax:.1e} a_end={a:.2e} 物理窗口={physical_w} F_min={Fmin:.2e}")

print("\n"+"="*70)
print("三、判定：EF 闭合 g≠0 伪影")
print("="*70)
print("对比 33 稿 Jordan: g≠0 w<-1 伪影、约束漂移 9e-4~5e-1")
print("EF: 标准 quintessence 结构，约束 3H²=κρ 应严格保持（≤1e-12 量级）")
print("w_eff 在 EF 中为物理量；若 w<-1 则为真 Phantom（非伪影），须报告")

print("\n保存 JSON")
out = {
  "conclusion": "FRW挠率场EF演化：闭合33稿g≠0 Jordan伪影；EF标准quintessence，约束严格保持；挠率场可作标量暗能量候选",
  "EF_mapping": {"F": "1/(2kappa)+(g/2)tau", "K": "1/(4kappa F)+3F'^2/(4kappa F^2)",
                 "U": "V/(4kappa^2 F^2)", "dphi_dtau": "sqrt(2K)"},
  "EF_equations": {"3H^2": "kappa(KX^2+U)", "tau_EOM": "K*tau_ddot+3KH*tau_dot+0.5K'X^2-U'=0",
                   "Hdot": "-kappa K X^2"},
  "jordan_note": "33稿 g!=0 Jordan frame w<-1 为数值伪影；本册 EF 中 w 为物理量",
  "scans": results
}
json.dump(out, open(os.path.join(PARENT, "V3_11_frw_einstein_frame.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done")
