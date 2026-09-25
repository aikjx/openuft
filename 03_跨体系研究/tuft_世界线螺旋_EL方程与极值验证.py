# -*- coding: utf-8 -*-
"""
TUFT / openuft —— 世界线层：κ-τ 作用量的欧拉方程（直接路线）与极值验证。

配套文稿：tuft_世界线螺旋_EL方程_文稿.md
（接续 tuft_世界线螺旋_变分推导.py / _文稿.md 的"捷径"推导）

本脚本要验证两件不同的事，且刻意分开：
  (A) 链规则/降维正确性：对任意基曲线，第一变分满足
        δS = ∫₀ᴸ [ 2α(κ-κ0) δκ + 2β(τ-τ0) δτ ] ds
      即"直接对 R 变分"与"先变 κ,τ 再代回"完全等价。
      ——这一条在一条 *非* 极值曲线（圆，κ=1,τ=0）上用数值核对，确保不是空对空。
  (B) 螺旋是极值：在螺旋基曲线（κ=κ0,τ=τ0）上，直接对作用量变分 S'(ε=0)=0。
  (C) 敏感性：圆（非极值）在某扰动下 S'(0)≠0，说明 (B) 的非零结论非平凡。

红线：数学自洽 ≠ 实验证实；κ0,τ0 仍为外源锚定（见 _文稿.md B1）。
"""
import sympy as sp
import mpmath as mp

s, eps = sp.symbols('s eps', real=True)
a, b, k0, t0 = sp.symbols('a b kappa0 tau0', real=True, positive=True)


def kappa_of(R):
    """一般参数下的曲率 |R'×R''| / |R'|^3 （不假定单位速率）。"""
    Rp = sp.diff(R, s)
    Rpp = sp.diff(Rp, s)
    cr = Rp.cross(Rpp)
    return sp.sqrt(sp.simplify(cr.dot(cr))) / (Rp.dot(Rp)) ** sp.Rational(3, 2)


def tau_of(R):
    """一般参数下的挠率 (R'×R'')·R''' / |R'×R''|^2。"""
    Rp = sp.diff(R, s)
    Rpp = sp.diff(Rp, s)
    Rppp = sp.diff(Rpp, s)
    cr = Rp.cross(Rpp)
    return sp.simplify(cr.dot(Rppp)) / sp.simplify(cr.dot(cr))


def build_variation(base, pert, target_k0, target_t0, alpha=1, beta=1):
    """在 base(s) 上加 ε·pert(s)，返回 (S 作为 ε 的函数, 基曲线 κ/τ, δκ/δτ 在 ε=0)。"""
    Re = base + eps * pert
    ke = kappa_of(Re)
    te = tau_of(Re)
    # 基曲线 κ,τ（ε=0 处）
    kb = sp.simplify(ke.subs(eps, 0))
    tb = sp.simplify(te.subs(eps, 0))
    # 第一变分 δκ, δτ = d/dε 在 ε=0
    dk = sp.simplify(sp.diff(ke, eps).subs(eps, 0))
    dt = sp.simplify(sp.diff(te, eps).subs(eps, 0))
    # 直接作用量 S(ε) = ∫ [α(κ-κ0)^2 + β(τ-τ0)^2] ds
    integrand = alpha * (ke - target_k0) ** 2 + beta * (te - target_t0) ** 2
    return integrand, kb, tb, dk, dt


def numeric_Sprime(integrand, s_range, eps0=0.0, order=1):
    """对符号 integrand(含 s,eps) 数值求 S(ε) 在 eps0 处的 1 阶导数。"""
    f = sp.lambdify((s, eps), integrand, modules='mpmath')
    Sfun = lambda e: mp.quad(lambda ss: f(ss, e), s_range)
    return mp.diff(Sfun, eps0, order)


def numeric_shortcut_integral(base_k, base_t, dk, dt, s_range, target_k0, target_t0, alpha=1, beta=1):
    """捷径表达式 ∫ [2α(κ-κ0) δκ + 2β(τ-τ0) δτ] ds 的数值积分。"""
    expr = 2 * alpha * (base_k - target_k0) * dk + 2 * beta * (base_t - target_t0) * dt
    g = sp.lambdify(s, sp.simplify(expr), modules='mpmath')
    return mp.quad(lambda ss: g(ss), s_range)


results = []
# =========================================================================
# 场景 1：圆为基曲线（κ=1, τ=0）—— 非极值，用于核对链规则/降维 + 敏感性
# 注意：用【开弧段】+ 不落在梯度核里的扰动，否则闭合圆上的某些扰动恰使 S'(0)=0（假阴性）。
# =========================================================================
R_circle = sp.Matrix([sp.cos(s), sp.sin(s), 0])          # R=1 的圆，κ=1, τ=0
target_k0, target_t0 = 2, 3                            # 靶值（与圆不同 ⇒ 圆非极值）
s_range_c = [mp.mpf(0), mp.pi]                          # 开弧段 [0, π]

# 两个扰动：一个改变 τ（出平面线性），一个改变 κ（切向余弦）
perturbations = [
    ('tau-pert',  sp.Matrix([0, 0, s]),        '出平面线性扰动(改变挠率)'),
    ('kappa-pert', sp.Matrix([sp.cos(s), 0, 0]), '切向余弦扰动(改变曲率)'),
]
chain_ok_all = True
sens_ok_all = True
for pname, pert_c, pdesc in perturbations:
    integ_c, kb_c, tb_c, dk_c, dt_c = build_variation(R_circle, pert_c, target_k0, target_t0)
    Sdir_c = numeric_Sprime(integ_c, s_range_c)
    Ssc_c = numeric_shortcut_integral(kb_c, tb_c, dk_c, dt_c, s_range_c, target_k0, target_t0)
    rel_err = abs(Sdir_c - Ssc_c) / max(1.0, abs(Sdir_c))
    chain_ok = rel_err < 1e-6
    chain_ok_all = chain_ok_all and chain_ok
    sens_ok = abs(Sdir_c) > 1e-3
    sens_ok_all = sens_ok_all and sens_ok
    results.append(('A', '圆[%s] 直接 S\'(0)' % pname, str(mp.nstr(Sdir_c, 4)), True))
    results.append(('A', '圆[%s] 捷径积分' % pname, str(mp.nstr(Ssc_c, 4)), True))
    results.append(('A', '圆[%s] 链规则相对误差<1e-6' % pname, str(mp.nstr(rel_err, 3)), chain_ok))
    results.append(('C', '圆[%s] S\'(0)非零(敏感性)' % pname, str(mp.nstr(Sdir_c, 4)), sens_ok))
results.append(('A*', '圆基: 链规则全部通过', 'chain', chain_ok_all))
results.append(('C*', '圆基: 敏感性全部通过', 'sens', sens_ok_all))

# =========================================================================
# 场景 2：螺旋为基曲线（κ=κ0, τ=τ0）—— 应为极值
# =========================================================================
k0v, t0v = 2, 3
Om = sp.sqrt(k0v ** 2 + t0v ** 2)
rv = k0v / (k0v ** 2 + t0v ** 2)
z0v = t0v / Om
R_helix = sp.Matrix([rv * sp.cos(Om * s), rv * sp.sin(Om * s), z0v * s])
pert_h = sp.Matrix([sp.sin(s), 0, 0])
integ_h, kb_h, tb_h, dk_h, dt_h = build_variation(R_helix, pert_h, k0v, t0v)
# 螺旋基的 κ,τ 应为靶值（常数）
base_const = (abs(float(kb_h) - k0v) < 1e-9) and (abs(float(tb_h) - t0v) < 1e-9)
results.append(('B0', '螺旋基 κ=κ0, τ=τ0 (常数)', 'k=%s t=%s' % (mp.nstr(float(kb_h), 4), mp.nstr(float(tb_h), 4)), base_const))
# (B) 直接变分 S'(0) 应为 0
Sdir_h = numeric_Sprime(integ_h, [mp.mpf(0), 4 * mp.pi])
helix_extremal = abs(Sdir_h) < 1e-6
results.append(('B1', '螺旋基 直接 S\'(0) ≈ 0 (是极值)', str(mp.nstr(Sdir_h, 4)), helix_extremal))
# 捷径也应给出 0（因为 κ-κ0=0, τ-τ0=0）
Ssc_h = numeric_shortcut_integral(kb_h, tb_h, dk_h, dt_h, [mp.mpf(0), 4 * mp.pi], k0v, t0v)
results.append(('B2', '螺旋基 捷径积分 ≈ 0 (一致)', str(mp.nstr(Ssc_h, 4)), abs(Ssc_h) < 1e-6))


def report():
    print('=' * 78)
    print('TUFT 世界线螺旋 - EL 方程与极值验证')
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
