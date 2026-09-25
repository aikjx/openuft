# -*- coding: utf-8 -*-
"""
TUFT / openuft —— 世界线层：常曲率常挠率作用量 -> 圆柱螺旋 的严格变分推导与机器核对.

对应路线（用户第八层路线）：
    第一~六层：把"光速螺旋"从人为设定推进为变分问题的自然解.
    本脚本只验证"世界线(1D 曲线)层"的几何变分核，不触及 4D 场论提升(见 07_统一场方程).

核心结论（待核验）:
    S[R] = ∫ [ α (κ-κ0)^2 + β (τ-τ0)^2 ] ds        (s = 弧长参数; α,β>0, κ0,τ0 为预设常数)
    由"空间曲线基本定理"把 κ(s),τ(s) 视为独立变分场 =>
        δS=0  =>  κ(s)=κ0, τ(s)=τ0  (内部)
    再由 Frenet 方程自 κ0,τ0 常数 反解 => 唯一(至多刚体运动)曲线 = 圆柱螺旋.
    以 s=ct 回到时间参数 => 用户给出的速度分解 (rω)^2 + p^2 = c^2 自然浮现.

红线: 数学自洽 ≠ 实验证实; κ0,τ0 是外源锚定(开放性 O-SCALE), 不是作用量导出的.
"""
import sympy as sp

s, c, k0, t0 = sp.symbols('s c kappa0 tau0', real=True, positive=True)

# ---- 由预设 κ0,τ0 构造的圆柱螺旋 (弧长参数 s) ----
# ρ = 1/sqrt(κ0^2+τ0^2);  r = κ0/ρ^2 = κ0/(κ0^2+τ0^2);  Omega = sqrt(κ0^2+τ0^2);  z0 = τ0/ρ = τ0/sqrt(κ0^2+τ0^2)
Omega = sp.sqrt(k0**2 + t0**2)
r = k0 / (k0**2 + t0**2)
z0 = t0 / Omega

Rx = r * sp.cos(Omega * s)
Ry = r * sp.sin(Omega * s)
Rz = z0 * s
R = sp.Matrix([Rx, Ry, Rz])


def curvature_vec(R, s):
    T = sp.diff(R, s)
    dT = sp.diff(T, s)
    return T, dT


def curvature(R, s):
    T, dT = curvature_vec(R, s)
    return sp.simplify(sp.sqrt(sp.simplify((T.cross(dT)).dot(T.cross(dT)))))


def torsion(R, s):
    # 标准 Frenet 挠率 (符号仅表手性; 取 + 号使本参数化的螺旋给出 +tau0)
    T, dT = curvature_vec(R, s)
    ddT = sp.diff(dT, s)
    kappa = curvature(R, s)
    num = (T.cross(dT)).dot(ddT)
    return sp.simplify(num / kappa**2)


def speed(R, t):
    # s = c*t  => R(t) = R(c t)
    Rt = R.subs(s, c * t)
    dRdt = sp.diff(Rt, t)
    return sp.simplify(sp.sqrt(sp.simplify(dRdt.dot(dRdt))))


results = []
checks = {}

# ---- 核验 1: 该螺旋的曲率恰为 κ0 (常数) ----
kappa_helix = curvature(R, s)
checks['kappa_helix == kappa0'] = sp.simplify(kappa_helix - k0) == 0
results.append(('C1', 'helix curvature = kappa0 (constant)',
                str(kappa_helix), checks['kappa_helix == kappa0']))

# ---- 核验 2: 该螺旋的挠率恰为 τ0 (常数) ----
tau_helix = torsion(R, s)
checks['tau_helix == tau0'] = sp.simplify(tau_helix - t0) == 0
results.append(('C2', 'helix torsion = tau0 (constant)',
                str(tau_helix), checks['tau_helix == tau0']))

# ---- 核验 3: 弧长参数化 |R'(s)| = 1 ----
T, _ = curvature_vec(R, s)
checks['unit_speed'] = sp.simplify(T.dot(T) - 1) == 0
results.append(('C3', 'arclength parameterization |R"(s)|=1',
                str(sp.simplify(T.dot(T))), checks['unit_speed']))

# ---- 核验 4: 时间参数下 |dR/dt| = c (光速约束) ----
t = sp.symbols('t', real=True)
v = speed(R, t)
checks['lightspeed'] = sp.simplify(v - c) == 0
results.append(('C4', 'time parameterization |dR/dt| = c',
                str(v), checks['lightspeed']))

# ---- 核验 5: 速度分解 (rω)^2 + p^2 = c^2 ----
# ω = d(Ω s)/dt = Ω c ;  p = z0 c
omega = Omega * c
p = z0 * c
decomp = sp.simplify((r * omega)**2 + p**2 - c**2)
checks['speed_decomp'] = decomp == 0
results.append(('C5', 'user speed decomposition (rω)^2 + p^2 = c^2',
                '0' if decomp == 0 else str(decomp), checks['speed_decomp']))

# ---- 核验 6: 数值取样 (κ0=2, τ0=3, c=1) 确认 κ=2,τ=3, 速度分解=1 ----
# Omega=sqrt(13); r=2/13; z0=3/sqrt(13); omega=Omega*c=sqrt(13); p=z0*c=3/sqrt(13)
# (rω)^2 = (2/13*sqrt(13))^2 = 4/13 ; p^2 = 9/13 ; 和 = 1
subs = {k0: 2, t0: 3, c: 1}
k_num = float(kappa_helix.subs(s, 0.7).subs(subs).evalf())
t_num = float(tau_helix.subs(s, 0.7).subs(subs).evalf())
decomp_num = float(decomp.subs(subs).evalf())
results.append(('C6', 'numeric sample kappa', str(k_num), abs(k_num - 2) < 1e-9))
results.append(('C6b', 'numeric sample tau', str(t_num), abs(t_num - 3) < 1e-9))
results.append(('C6c', 'numeric speed decomposition = 1', str(decomp_num), abs(decomp_num) < 1e-9))


def report():
    print('=' * 78)
    print('TUFT 世界线螺旋 - 变分推导机器核对')
    print('=' * 78)
    for tag, desc, val, ok in results:
        flag = 'PASS' if ok else 'FAIL'
        print('[%-4s] %-44s -> %-18s %s' % (tag, desc, val[:18], flag))
    print('-' * 78)
    allok = all(ok for _, _, _, ok in results)
    print('VERDICT:', 'ALL PASS' if allok else 'HAS FAIL')
    print('=' * 78)
    return allok


if __name__ == '__main__':
    report()
